"""2016 Ordinary Level: every part, from the page.

Paper and scheme as the PDFs number their pages. As in 2017-2019, the automatic
author prices nothing in this sitting: the scheme sets each answer in a left
column and its award in a box to the right ("Name Award 3 @ 4 Marks"), which
its reader does not join to the answer, so every card here is built from the
page by rectangle. The marks grid is on scheme p4: Question 1 is Section A,
"Any six @ 5 marks each", two-part answers 3 + 2, and Section B, "Any three
parts @ 12 + 12 + 11 marks"; Questions 2-7 are 45 marks each. A Section B card
carries the PRINTED primary price, the 12 the scheme awards a part answered
first or second ("Award 12 (11) Marks"), and says the third part answered
earns 11.
"""
from eng_lift import join, lift

Y, L = 2016, 'ol'
OWNED = ('never shipped: the automatic author builds this card only from the lifts this '
         'entry records, so the entry owns it')


def S(page, *rect):
    return lift(Y, L, 'scheme', page, rect)


def P(page, *rect, more=()):
    return lift(Y, L, 'paper', page, rect, more=more)


_C6 = (96, 418, 318, 435)             # paper p6: the knurling tool (c)
_C7B = (98, 602, 523, 633)            # paper p7: the electronic components (c)

_SB = ("Section B is 'Any three parts @ 12 + 12 + 11 marks': the card carries the 12 a part "
       "earns answered first or second; answered third it earns 11.")
_OR3 = ('The paper sets two (d)s either side of an OR, the material properties and the '
        'compressor\'s applications; the scheme prices both "Award 2 @ 4 Marks", so they are '
        'one card, each branch a route.')
_OR6 = ('The paper sets two (c)s either side of an OR: the knurling tool (c), whose (i)-(iii) '
        'are carded apart, and the CNC lathe (c), carded at the letter.')
_OR7 = ('The paper sets two (c)s either side of an OR: the instruments (c), carded at the '
        'letter, and the electronic components (c), one card for each component '
        'photographed and captioned (i)-(iii).')

CROPS = {
    # ---- paper ------------------------------------------------------------
    'engineering-2016-OL-paper-q1d-crop': dict(
        doc='paper', page=2, rect=(470, 175, 560, 217), image=True, ref='2016 OL Q1(d)'),
    # The three items under (i), each captioned.
    'engineering-2016-OL-paper-q1i-crop': dict(
        doc='paper', page=2, rect=(60, 436, 550, 550), ref='2016 OL Q1(i)'),
    'engineering-2016-OL-paper-q1m-crop': dict(
        doc='paper', page=2, rect=(198, 743, 365, 788), image=True, ref='2016 OL Q1(m)'),
    # The trike with its three parts labelled; the foot of the page's "(45
    # marks)" heading falls inside the box and is whited out.
    'engineering-2016-OL-paper-q2a-crop': dict(
        doc='paper', page=3, rect=(300, 30, 556, 203), mask=[(498, 26, 560, 40)],
        ref='2016 OL Q2(a)'),
    'engineering-2016-OL-paper-q3b-crop': dict(
        doc='paper', page=3, rect=(50, 548, 540, 647), ref='2016 OL Q3(b)'),
    # The three processes drawn and lettered A, B and C.
    'engineering-2016-OL-paper-q5a-crop': dict(
        doc='paper', page=5, rect=(90, 105, 533, 238), ref='2016 OL Q5(a)',
        letters=('A', 'B', 'C')),
    # The four lathe operations drawn and captioned (i)-(iv).
    'engineering-2016-OL-paper-q6a-crop': dict(
        doc='paper', page=6, rect=(50, 135, 550, 282), ref='2016 OL Q6(a)'),
    'engineering-2016-OL-paper-q6c-crop': dict(
        doc='paper', page=6, rect=(174, 445, 376, 575), image=True, ref='2016 OL Q6(c)'),
    'engineering-2016-OL-paper-q7b-crop': dict(
        doc='paper', page=7, rect=(380, 184, 566, 274), ref='2016 OL Q7(b)'),
    'engineering-2016-OL-paper-q7c-crop': dict(
        doc='paper', page=7, rect=(50, 350, 562, 537), ref='2016 OL Q7(c)'),
    # The OR branch's three components, captioned (i)-(iii).
    'engineering-2016-OL-paper-q7cor-crop': dict(
        doc='paper', page=7, rect=(100, 645, 500, 778), ref='2016 OL Q7(c)'),
    # ---- scheme: the drawings the answers are given with -------------------
    'engineering-2016-OL-scheme-q2c-sol': dict(
        doc='scheme', parts=[(9, (38, 443, 186, 591)), (9, (58, 630, 186, 792)),
                             (10, (47, 58, 209, 246))],
        layout='row', solution=True, ref='2016 OL Q2(c)'),
    'engineering-2016-OL-scheme-q4a-sol': dict(
        doc='scheme', parts=[(12, (100, 205, 435, 262)), (12, (84, 418, 438, 491)),
                             (12, (100, 610, 450, 682))],
        solution=True, ref='2016 OL Q4(a)'),
}

CARDS = [
    # ---- Question 1, Section A ("Any six @ 5 marks each") ------------------
    dict(key=(1, 'a', None),
         why='Scheme p5 numbers two precautions; "3 + 2 Marks".',
         topic='eng-3-1',
         lifted=[S(5, 93, 384, 217, 401), S(5, 93, 397, 263, 414)],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         notes="The scheme prints '3 + 2 Marks'."),
    dict(key=(1, 'b', None),
         why='Scheme p5 names the alloy, "5 Marks".',
         topic='eng-1-5',
         lifted=[S(5, 64, 425, 107, 443)], marks=[5], total=5,
         notes="The scheme prints '5 Marks'."),
    dict(key=(1, 'c', None),
         why='Scheme p5 names the material, "5 Marks".',
         topic='eng-1-9',
         lifted=[S(5, 64, 462, 196, 479)], marks=[5], total=5,
         notes="The scheme prints '5 Marks'."),
    dict(key=(1, 'd', None),
         why='The pulley is photographed beside (d); scheme p5 gives the name and the '
             'application under their headings; "3 + 2 Marks".',
         topic='eng-2-15',
         lifted=[join(S(5, 70, 494, 107, 512), S(5, 196, 494, 299, 512)),
                 join(S(5, 70, 508, 137, 525), S(5, 196, 508, 310, 525))],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         question_figure='engineering-2016-OL-paper-q1d-crop',
         notes="The scheme prints '3 + 2 Marks'."),
    dict(key=(1, 'e', None),
         why='Scheme p5 numbers two reasons; "3 + 2 Marks".',
         topic='eng-3-14',
         lifted=[S(5, 86, 550, 402, 567),
                 join(S(5, 86, 563, 472, 581), S(5, 86, 577, 162, 594))],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         notes="The scheme prints '3 + 2 Marks'."),
    dict(key=(1, 'f', None),
         why='Scheme p5 numbers two ways; "3 + 2 Marks".',
         topic='eng-2-13',
         lifted=[S(5, 86, 619, 450, 636), S(5, 86, 630, 429, 647)],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         notes="The scheme prints '3 + 2 Marks'."),
    dict(key=(1, 'g', None),
         why='Scheme p5 gives the name and the application on their own lines; "3 + 2 '
             'Marks".',
         topic='eng-2-11',
         lifted=[join(S(5, 80, 674, 117, 691), S(5, 196, 674, 278, 691)),
                 join(S(5, 83, 687, 149, 704), S(5, 196, 687, 251, 704))],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         notes="The scheme prints '3 + 2 Marks'."),
    dict(key=(1, 'h', None),
         why='Scheme p5 numbers two reasons; "3 + 2 Marks". The reader joins the Section B '
             'heading to (h), so the question is lifted from the page.',
         topic='eng-2-11',
         question_lift=P(2, 62, 289, 370, 307),
         lifted=[S(5, 84, 729, 310, 746), S(5, 84, 743, 382, 760)],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         notes="The scheme prints '3 + 2 Marks'."),
    # ---- Question 1, Section B ("Any three parts @ 12 + 12 + 11 marks") ----
    dict(key=(1, 'i', None),
         why='The three items are photographed and captioned under (i); scheme p6 '
             'describes each under its name, "Any one", "Award 12 (11) Marks".',
         topic='eng-2-15', stem=False,
         lifted=[[join(S(6, 88, 113, 240, 130), S(6, 88, 126, 471, 226)),
                  join(S(6, 88, 265, 138, 282), S(6, 88, 278, 474, 351)),
                  join(S(6, 88, 389, 225, 406), S(6, 88, 402, 479, 516))]],
         row_kind='anyN', group=(1, 12), marks=[12], tariff='fixed', total=12,
         question_figure='engineering-2016-OL-paper-q1i-crop',
         notes="The scheme prints 'Any one: Award 12 (11) Marks'. " + _SB),
    dict(key=(1, 'j', None),
         why='Scheme pp6-7 explain each term under its name, "Any two", "Award 6 + 6(5)".',
         topic='eng-3-14', stem=False,
         lifted=[[join(S(6, 88, 612, 123, 629), S(6, 88, 625, 479, 767)),
                  join(S(7, 85, 55, 141, 73), S(7, 85, 69, 450, 155)),
                  join(S(7, 88, 193, 120, 211), S(7, 88, 207, 431, 293)),
                  join(S(7, 88, 331, 198, 348), S(7, 88, 345, 450, 431))]],
         row_kind='anyN', group=(2, 6), marks=[12], tariff='fixed', total=12,
         notes="The scheme prints 'Any two: Award 6 + 6(5)'. " + _SB),
    dict(key=(1, 'k', None),
         why='Scheme p7 gives the definition under the term and two examples, either one, '
             'under "Example:", "Definition Award 6", "Example Award 6(5)".',
         topic='eng-3-8', stem=False,
         lifted=[join(S(7, 85, 527, 154, 544), S(7, 85, 540, 404, 571)),
                 [S(7, 85, 609, 112, 627), S(7, 118, 609, 145, 627)]],
         marks=[6, 6], total=12,
         notes="The scheme prints 'Definition Award 6, Example Award 6(5)'. " + _SB),
    dict(key=(1, 'l', None),
         why='Scheme p8 explains each term under its name, "Any two", "Award 6 + 6 (5)".',
         topic='eng-3-14', stem=False,
         lifted=[[join(S(8, 85, 82, 154, 99), S(8, 85, 96, 385, 144)),
                  join(S(8, 88, 237, 180, 254), S(8, 88, 251, 502, 282)),
                  join(S(8, 88, 348, 191, 365), S(8, 88, 362, 465, 407)),
                  join(S(8, 88, 445, 149, 462), S(8, 88, 458, 491, 531))]],
         row_kind='anyN', group=(2, 6), marks=[12], tariff='fixed', total=12,
         notes="The scheme prints 'Any two: Award 6 + 6 (5)'. " + _SB),
    dict(key=(1, 'm', None),
         why='The sleeve is photographed under (m); scheme p8 gives the name and the '
             'function under their headings, "Name Award 6", "Application Award 6(5)".',
         topic='eng-2-11', stem=False,
         lifted=[join(S(8, 85, 598, 122, 616), S(8, 85, 612, 190, 630)),
                 join(S(8, 85, 643, 138, 660), S(8, 85, 656, 464, 687))],
         marks=[6, 6], total=12,
         question_figure='engineering-2016-OL-paper-q1m-crop',
         notes="The scheme prints 'Name Award 6, Application Award 6(5)'. " + _SB),
    # ---- Question 2 --------------------------------------------------------
    dict(key=(2, 'a', None),
         why='(a) asks for a material for each labelled part and a reason for each; scheme '
             'p9 prices them together, "Part (a) (i) & (ii) Name & Reason Award 3 @ 5 '
             'Marks", so the two are one card at the letter, a row a part, each material '
             'with its reason.',
         topic='eng-3-14',
         question_lift=P(3, 96, 50, 282, 95, more=[(96, 133, 279, 164)]),
         lifted=[join(S(9, 88, 85, 117, 102), S(9, 196, 85, 235, 102),
                      S(9, 196, 168, 399, 199)),
                 join(S(9, 88, 99, 226, 116), S(9, 196, 209, 375, 240)),
                 join(S(9, 88, 112, 149, 130), S(9, 196, 112, 254, 130),
                      S(9, 196, 251, 407, 268))],
         marks=[5, 5, 5], total=15,
         question_figure='engineering-2016-OL-paper-q2a-crop',
         notes="The scheme prints 'Part (a) (i) & (ii) Name & Reason Award 3 @ 5 Marks'."),
    dict(key=(2, 'b', None),
         why='"For each of the metals listed below": scheme p9 names a furnace for each '
             'metal on its own line, "Name Award 3 @ 4 Marks". One card at the letter, a '
             'row a metal.',
         topic='eng-1-4',
         lifted=[join(S(9, 73, 318, 121, 336), S(9, 196, 318, 303, 336)),
                 join(S(9, 73, 332, 138, 350), S(9, 196, 332, 263, 350)),
                 join(S(9, 73, 346, 145, 364), S(9, 196, 346, 273, 364))],
         marks=[4, 4, 4], total=12,
         notes="The scheme prints 'Name Award 3 @ 4 Marks'."),
    dict(key=(2, 'c', None),
         why='"Describe the operation of one of the furnaces": scheme pp9-10 describe each '
             'under its name beside a drawing of it, shown with the answer; "Any one '
             'description", "Award 1 @ 10 Marks".',
         topic='eng-1-4',
         lifted=[[join(S(9, 209, 447, 330, 465), S(9, 209, 461, 443, 603)),
                  join(S(9, 209, 632, 285, 649), S(9, 210, 648, 464, 776)),
                  join(S(10, 218, 65, 302, 82), S(10, 219, 80, 449, 194))]],
         row_kind='anyN', group=(1, 10), marks=[10], tariff='fixed', total=10,
         figure='engineering-2016-OL-scheme-q2c-sol',
         notes="The scheme prints 'Any one description: Award 1 @ 10 Marks'."),
    dict(key=(2, 'd', None),
         why='Scheme p10 names two ferrous and two non-ferrous metals, a pair a line; '
             '"Name Award 2 @ 4 Marks".',
         topic='eng-1-5',
         lifted=[join(S(10, 82, 303, 188, 321), S(10, 230, 303, 317, 321)),
                 S(10, 82, 331, 339, 348)],
         marks=[4, 4], total=8,
         notes="The scheme prints 'Name Award 2 @ 4 Marks'."),
    # ---- Question 3 --------------------------------------------------------
    dict(key=(3, 'a', 'i'),
         why='Scheme p10 explains hardening and annealing under their names; "Part (a)(i) '
             'Difference @ 8 marks", one price for the part.',
         topic='eng-2-6',
         lifted=[join(S(10, 106, 515, 166, 532), S(10, 106, 529, 404, 573)),
                 join(S(10, 106, 584, 166, 601), S(10, 106, 598, 447, 643))],
         tariff='questionTotal', total=8,
         notes="The scheme prints 'Part (a)(i) Difference @ 8 marks'."),
    dict(key=(3, 'a', 'ii'),
         why='Scheme p10 describes each process under its name; "Part (a)(ii) Describe @ 4 '
             '+ 4 marks".',
         topic='eng-2-6',
         lifted=[join(S(10, 106, 653, 164, 670), S(10, 106, 666, 490, 698)),
                 join(S(10, 106, 709, 162, 726), S(10, 106, 723, 480, 768))],
         marks=[4, 4], total=8,
         notes="The scheme prints 'Part (a)(ii) Describe @ 4 + 4 marks'."),
    dict(key=(3, 'b', None),
         why='"For each of the following": scheme p11 names the process for each item on '
             'its own line, "Process Award 3 @ 5 marks". One card at the letter, a row an '
             'item.',
         topic='eng-2-6',
         lifted=[join(S(11, 88, 69, 153, 86), S(11, 232, 69, 354, 86)),
                 join(S(11, 88, 83, 179, 100), S(11, 232, 83, 285, 100)),
                 join(S(11, 88, 97, 209, 114), S(11, 232, 97, 309, 114))],
         marks=[5, 5, 5], total=15,
         question_figure='engineering-2016-OL-paper-q3b-crop',
         notes="The scheme prints 'Process Award 3 @ 5 marks'."),
    dict(key=(3, 'c', None),
         why='Scheme p11 bullets two precautions; "Precautions Award 2 @ 3 Marks".',
         topic='eng-3-1',
         lifted=[S(11, 104, 180, 412, 211), S(11, 104, 222, 436, 253)],
         marks=[3, 3], total=6,
         notes="The scheme prints 'Precautions Award 2 @ 3 Marks'."),
    dict(key=(3, 'd', None),
         why='Paper p3 sets two alternative (d)s either side of an OR, both at the letter. '
             'Scheme p11 explains each property under its name, "Description Award 2 @ 4 '
             'Marks", and bullets two compressor applications, "Applications Award 2 @ 4 '
             'Marks": priced alike, one card with a route per branch.',
         topic='eng-3-8', stem=False,
         question_lift=P(3, 96, 689, 364, 706, more=[(96, 712, 466, 729), (195, 735, 220, 755),
                                                     (96, 760, 349, 778)]),
         lifted=[[join(S(11, 103, 333, 167, 350), S(11, 104, 347, 414, 378)),
                  join(S(11, 103, 416, 157, 433), S(11, 104, 429, 438, 460)),
                  join(S(11, 103, 485, 171, 502), S(11, 104, 498, 450, 516))],
                 S(11, 104, 612, 313, 629), S(11, 104, 640, 363, 657)],
         row_kind='anyN', group=[(2, 4), None, None], marks=[8, 4, 4],
         routes=['a', 'b', 'b'], tariff='fixed', total=8, notes=_OR3),
    # ---- Question 4 --------------------------------------------------------
    dict(key=(4, 'a', None),
         why='"Describe each of the following" flames: scheme p12 describes each under its '
             'name beside a labelled drawing of the flame, shown with the answer; '
             '"Description Award 3 @ 4 Marks". One card at the letter, a row a flame.',
         topic='eng-2-10',
         lifted=[join(S(12, 104, 113, 181, 130), S(12, 104, 127, 415, 174)),
                 join(S(12, 104, 322, 190, 339), S(12, 104, 336, 448, 367)),
                 join(S(12, 104, 529, 206, 546), S(12, 104, 543, 447, 601))],
         marks=[4, 4, 4], total=12,
         figure='engineering-2016-OL-scheme-q4a-sol',
         notes="The scheme prints 'Description Award 3 @ 4 Marks'."),
    dict(key=(4, 'b', 'i'),
         why='Scheme p13 gives the function of each item under its name; "Function Award '
             'any 3 @ 3 Marks".',
         topic='eng-2-10',
         lifted=[[join(S(13, 88, 83, 140, 100), S(13, 88, 97, 421, 141)),
                  join(S(13, 88, 152, 165, 169), S(13, 88, 166, 416, 210)),
                  join(S(13, 88, 221, 110, 238), S(13, 88, 235, 434, 266)),
                  join(S(13, 88, 276, 144, 293), S(13, 88, 290, 450, 321))]],
         row_kind='anyN', group=(3, 3), marks=[9], tariff='fixed', total=9,
         notes="The scheme prints 'Function Award any 3 @ 3 Marks'."),
    dict(key=(4, 'b', 'ii'),
         why='Scheme p13 bullets three steps; "Steps Award 3 @ 2 Marks".',
         topic='eng-2-10',
         lifted=[S(13, 104, 358, 417, 375), S(13, 104, 374, 445, 391), S(13, 104, 389, 473, 406)],
         marks=[2, 2, 2], total=6,
         notes="The scheme prints 'Steps Award 3 @ 2 Marks'."),
    dict(key=(4, 'c', 'i'),
         why='"Answer any three of the following", four separate asks, carded per roman; '
             'the nut is photographed beside (c). Scheme p13 names it and its use, "Good '
             'explanation Award 3 @ 4 Marks".',
         topic='eng-2-10',
         lifted=[join(S(13, 105, 472, 154, 489), S(13, 112, 485, 416, 516))], marks=[4],
         total=4,
         question_figure='engineering-2016-OL-paper-q4ci-art',
         notes="The scheme prints 'Good explanation Award 3 @ 4 Marks', 4 for each part "
               "answered."),
    dict(key=(4, 'c', 'ii'),
         why='Scheme p13 answers in two sentences, "Good explanation Award 3 @ 4 Marks".',
         topic='eng-2-10',
         lifted=[S(13, 110, 520, 457, 565)], marks=[4], total=4,
         notes="The scheme prints 'Good explanation Award 3 @ 4 Marks', 4 for each part "
               "answered."),
    dict(key=(4, 'c', 'iii'),
         why='Scheme p13 gives two advantages, one a line, under "Good explanation Award 3 @ '
             '4 Marks", one price for the part.',
         topic='eng-2-10',
         lifted=[S(13, 119, 568, 373, 586), S(13, 121, 582, 268, 599)],
         tariff='questionTotal', total=4,
         notes="The scheme prints 'Good explanation Award 3 @ 4 Marks', 4 for each part "
               "answered."),
    dict(key=(4, 'c', 'iv'),
         why='Scheme p13 explains each joint in a sentence, under "Good explanation Award 3 '
             '@ 4 Marks", one price for the part.',
         topic='eng-2-10',
         lifted=[S(13, 115, 603, 448, 634), S(13, 115, 630, 459, 648)],
         tariff='questionTotal', total=4,
         notes="The scheme prints 'Good explanation Award 3 @ 4 Marks', 4 for each part "
               "answered."),
    dict(key=(4, 'd', None),
         why='Scheme p13 bullets two precautions; "Safety Award 2 @ 3 Marks".',
         topic='eng-3-1',
         lifted=[S(13, 104, 714, 321, 731), S(13, 104, 729, 390, 746)],
         marks=[3, 3], total=6,
         notes="The scheme prints 'Safety Award 2 @ 3 Marks'."),
    # ---- Question 5 --------------------------------------------------------
    dict(key=(5, 'a', 'i'),
         why='The three processes are drawn and lettered A, B and C; scheme p14 names each '
             'after its letter on its own line, "Name Award 3 @ 3 Marks".',
         topic='eng-1-9', stem=False,
         question_lift=P(5, 112, 241, 492, 258),
         lifted=[S(14, 97, 126, 238, 143), S(14, 97, 140, 255, 157), S(14, 97, 154, 274, 171)],
         marks=[3, 3, 3], total=9,
         labels={'A': S(14, 160, 126, 238, 143), 'B': S(14, 160, 140, 255, 157),
                 'C': S(14, 159, 154, 274, 171)},
         question_figure='engineering-2016-OL-paper-q5a-crop',
         notes="The scheme prints 'Name Award 3 @ 3 Marks'."),
    dict(key=(5, 'a', 'ii'),
         why='"Any one process from 5(a)(i)": scheme p14 describes each under its letter and '
             'name and ends each with the components it makes, "Description Award 9 Marks", '
             '"Component Award 3 Marks". The description and the component sentence are '
             'each lifted by their own rectangles, either process.',
         topic='eng-1-9', stem=False,
         question_lift=P(5, 116, 282, 547, 313),
         lifted=[[join(S(14, 88, 320, 190, 337), S(14, 88, 333, 485, 390),
                       S(14, 88, 389, 162, 406)),
                  join(S(14, 91, 444, 216, 461), S(14, 91, 458, 421, 486),
                       S(14, 91, 485, 273, 502)),
                  join(S(14, 91, 568, 238, 585), S(14, 91, 582, 422, 640))],
                 [S(14, 162, 389, 446, 406),
                  join(S(14, 273, 485, 421, 502), S(14, 91, 499, 427, 516),
                       S(14, 91, 513, 306, 530)),
                  S(14, 91, 637, 399, 668)]],
         marks=[9, 3], total=12,
         question_figure='engineering-2016-OL-paper-q5a-crop',
         notes="The scheme prints 'Description Award 9 Marks' and 'Component Award 3 "
               "Marks', for the process chosen."),
    dict(key=(5, 'b', None),
         why='Scheme p14 bullets two precautions; "Safety Award 2 @ 3 Marks".',
         topic='eng-3-1',
         lifted=[S(14, 95, 734, 423, 752), S(14, 95, 749, 376, 766)],
         marks=[3, 3], total=6,
         notes="The scheme prints 'Safety Award 2 @ 3 Marks'."),
    dict(key=(5, 'c', None),
         why='"Each of the components shown below": scheme p15 names a plastic for each on '
             'its own line, "Plastic Award 2 @ 4 Marks". One card at the letter, a row a '
             'component.',
         topic='eng-1-9',
         lifted=[join(S(15, 91, 83, 215, 100), S(15, 268, 83, 396, 100)),
                 join(S(15, 91, 97, 175, 114), S(15, 268, 97, 311, 114))],
         marks=[4, 4], total=8,
         question_figure='engineering-2016-OL-paper-q5ci-art',
         notes="The scheme prints 'Plastic Award 2 @ 4 Marks'."),
    dict(key=(5, 'd', 'i'),
         why='Scheme p15 answers in one sentence; "Part (d)(i) Name @ 5 marks".',
         topic='eng-1-9',
         lifted=[S(15, 106, 179, 327, 197)], marks=[5], total=5,
         notes="The scheme prints 'Part (d)(i) Name @ 5 marks'."),
    dict(key=(5, 'd', 'ii'),
         why='Scheme p15 answers in one sentence; "Part (d)(ii) Reason @ 5 marks".',
         topic='eng-1-9',
         lifted=[S(15, 109, 206, 411, 224)], marks=[5], total=5,
         notes="The scheme prints 'Part (d)(ii) Reason @ 5 marks'."),
    # ---- Question 6 --------------------------------------------------------
    dict(key=(6, 'a', None),
         why='Four lathe operations drawn and captioned (i)-(iv) with no words; scheme p15 '
             'names each after its roman, "Any three operations", "Name Award 3 @ 5 Marks".',
         topic='eng-2-11',
         lifted=[[S(15, 88, 501, 171, 519), S(15, 88, 529, 147, 546), S(15, 88, 556, 164, 574),
                  S(15, 88, 584, 189, 601)]],
         row_kind='anyN', group=(3, 5), marks=[15], tariff='fixed', total=15,
         question_figure='engineering-2016-OL-paper-q6a-crop',
         notes="The scheme prints 'Any three operations: Name Award 3 @ 5 Marks'."),
    dict(key=(6, 'b', None),
         why='A lead-in over four terms set as romans, "any three"; scheme pp15-16 describe '
             'each under its name, "Any three", "Description Award 3 @ 5 Marks".',
         topic='eng-2-11',
         lifted=[[join(S(15, 102, 667, 252, 684), S(15, 88, 681, 464, 781)),
                  join(S(16, 102, 69, 188, 86), S(16, 85, 83, 462, 128)),
                  join(S(16, 104, 152, 157, 169), S(16, 85, 166, 467, 210)),
                  join(S(16, 104, 235, 139, 252), S(16, 85, 248, 493, 279))]],
         row_kind='anyN', group=(3, 5), marks=[15], tariff='fixed', total=15,
         notes="The scheme prints 'Any three: Description Award 3 @ 5 Marks'."),
    dict(key=(6, 'c', 'i'),
         why='The knurling tool branch\'s (i), lifted with its cue; scheme p16 names the '
             'process, "Part (c)(i) Name @ 5 marks".',
         topic='eng-2-11', stem=False,
         question_lift=P(6, *_C6, more=[(113, 595, 387, 612)]),
         lifted=[S(16, 232, 426, 281, 443)], marks=[5], total=5,
         question_figure='engineering-2016-OL-paper-q6c-crop',
         notes="The scheme prints 'Part (c)(i) Name @ 5 marks'. " + _OR6),
    dict(key=(6, 'c', 'ii'),
         why='The knurling tool branch\'s (ii), lifted with its cue; scheme p16 gives two '
             'things, one a line, "Part (c)(ii) Two Things @ 3 + 2 marks".',
         topic='eng-2-11', stem=False,
         question_lift=P(6, *_C6, more=[(116, 616, 478, 633)]),
         lifted=[S(16, 240, 455, 458, 473), S(16, 240, 469, 454, 486)],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         question_figure='engineering-2016-OL-paper-q6c-crop',
         notes="The scheme prints 'Part (c)(ii) Two Things @ 3 + 2 marks'. " + _OR6),
    dict(key=(6, 'c', 'iii'),
         why='The knurling tool branch\'s (iii), lifted with its cue; scheme p16 gives one '
             'precaution, "Part (c)(iii) One Precaution @ 5 marks".',
         topic='eng-3-1', stem=False,
         question_lift=P(6, *_C6, more=[(119, 636, 514, 653)]),
         lifted=[S(16, 232, 497, 463, 514)], marks=[5], total=5,
         question_figure='engineering-2016-OL-paper-q6c-crop',
         notes="The scheme prints 'Part (c)(iii) One Precaution @ 5 marks'. " + _OR6),
    dict(key=(6, 'c', None),
         why='The OR branch, "State three advantages" of CNC with no romans; scheme p16 '
             'bullets three, "Advantages Award 3 @ 5 Marks".',
         topic='eng-2-13', stem=False,
         question_lift=P(6, 96, 736, 525, 767),
         lifted=[S(16, 88, 623, 440, 641), S(16, 88, 639, 314, 656), S(16, 88, 653, 257, 670)],
         marks=[5, 5, 5], total=15,
         notes="The scheme prints 'Advantages Award 3 @ 5 Marks'. " + _OR6),
    # ---- Question 7 --------------------------------------------------------
    dict(key=(7, 'a', None),
         why='A lead-in over three terms set as romans, "any two"; scheme p17 explains each '
             'under its name, "Explanation Award 2 @ 5 Marks".',
         topic='eng-3-12',
         lifted=[[join(S(17, 104, 126, 175, 143), S(17, 104, 140, 439, 185)),
                  join(S(17, 106, 196, 171, 213), S(17, 108, 209, 415, 226),
                       S(17, 225, 230, 346, 248)),
                  join(S(17, 108, 251, 180, 268), S(17, 108, 264, 455, 295))]],
         row_kind='anyN', group=(2, 5), marks=[10], tariff='fixed', total=10,
         notes="The scheme prints 'Explanation Award 2 @ 5 Marks'."),
    dict(key=(7, 'b', None),
         why='The shaft is drawn with its dimension; scheme p17 answers each of (i)-(iv) on '
             'its own line after the ask, "Calculations Award 4 @ 5 Marks". The question is '
             'lifted from the page with its four asks.',
         topic='eng-3-12',
         question_lift=P(7, 98, 183, 347, 200, more=[(98, 206, 351, 286)]),
         lifted=[S(17, 91, 347, 357, 364), S(17, 91, 361, 357, 378), S(17, 91, 375, 357, 392),
                 S(17, 91, 389, 357, 406)],
         marks=[5, 5, 5, 5], total=20,
         question_figure='engineering-2016-OL-paper-q7b-crop',
         notes="The scheme prints 'Calculations Award 4 @ 5 Marks'."),
    dict(key=(7, 'c', None),
         why='Paper p7 sets two alternative (c)s either side of an OR. This card is the '
             'first branch, four instruments photographed and captioned (i)-(iv) with no '
             'words; scheme p17 names each with an application after its roman, "Any '
             'three", "Name & application Award 3 @ 5 Marks". The reader runs the OR '
             'branch\'s ask on into this one, so the question is lifted from the page.',
         topic='eng-3-12', stem=False,
         question_lift=P(7, 98, 323, 563, 341),
         lifted=[[S(17, 88, 513, 451, 530),
                  S(17, 88, 540, 454, 558), S(17, 88, 568, 391, 585),
                  join(S(17, 88, 582, 468, 599), S(17, 220, 596, 321, 613))]],
         row_kind='anyN', group=(3, 5), marks=[15], tariff='fixed', total=15,
         question_figure='engineering-2016-OL-paper-q7c-crop',
         notes="The scheme prints 'Any three: Name & application Award 3 @ 5 Marks'. "
               + _OR7),
    dict(key=(7, 'c', 'i'),
         why='The OR branch: "Name each of the electronic components shown below and '
             'outline the function of each", three photographs captioned (i)-(iii); scheme '
             'p17 names each with its use after its roman, "Name & function Award 3 @ 5 '
             'Marks". The question is lifted with the caption it answers.',
         topic='eng-2-16', stem=False,
         question_lift=P(7, *_C7B, more=[(147, 761, 162, 778)]),
         lifted=[join(S(17, 88, 724, 140, 742), S(17, 235, 724, 465, 742))], marks=[5],
         total=5,
         question_figure='engineering-2016-OL-paper-q7cor-crop',
         notes="The scheme prints 'Name & function Award 3 @ 5 Marks'. " + _OR7),
    dict(key=(7, 'c', 'ii'),
         why='The OR branch\'s second component; scheme p17 names it with its use, "Name & '
             'function Award 3 @ 5 Marks".',
         topic='eng-2-16', stem=False,
         question_lift=P(7, *_C7B, more=[(299, 761, 318, 778)]),
         lifted=[join(S(17, 88, 738, 186, 755), S(17, 235, 738, 384, 755))], marks=[5],
         total=5,
         question_figure='engineering-2016-OL-paper-q7cor-crop',
         notes="The scheme prints 'Name & function Award 3 @ 5 Marks'. " + _OR7),
    dict(key=(7, 'c', 'iii'),
         why='The OR branch\'s third component; scheme p17 names it with its use, "Name & '
             'function Award 3 @ 5 Marks".',
         topic='eng-2-16', stem=False,
         question_lift=P(7, *_C7B, more=[(462, 761, 484, 779)]),
         lifted=[join(S(17, 88, 752, 186, 769), S(17, 234, 752, 473, 783))], marks=[5],
         total=5,
         question_figure='engineering-2016-OL-paper-q7cor-crop',
         notes="The scheme prints 'Name & function Award 3 @ 5 Marks'. " + _OR7),
]

TOPICS = {}

_MAT = 'Materials: Properties and Uses'

ATLAS = {
    'eng-2016-ol-q2-a': dict(
        topics=[_MAT],
        note='Choosing a material for each part of the trike, and why; the card\'s syllabus '
             'heading is Technology, as every Ordinary Q2 material-choice card\'s is.'),
    'eng-2016-ol-q6-c-iii': dict(
        topics=['CNC & Centre Lathe'],
        note='A safety precaution with the knurling tool on the centre lathe; the card\'s '
             'syllabus heading is Health and safety.'),
}
