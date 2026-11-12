"""2011 Ordinary Level: every part, from the page.

Paper and scheme as the PDFs number their pages. As in 2012-2019, the automatic
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

Y, L = 2011, 'ol'


def S(page, *rect):
    return lift(Y, L, 'scheme', page, rect)


def P(page, *rect, more=(), items=()):
    return lift(Y, L, 'paper', page, rect, more=more, items=items)


_A5 = (75, 483, 390, 500)             # paper p4: Q5(a), processes A and B

_SB = ("Section B is 'Any three parts @ 12 + 12 + 11 Marks': the card carries the 12 a part "
       "earns answered first or second; answered third it earns 11.")
_SA = "Section A is 'Any six @ 5 marks each'."
_OR3 = ('The paper sets two (d)s either side of an OR: the material properties, "Award 1 @ 5 '
        'Marks, Award 1 @ 4 Marks", carded at the letter, and pneumatics, whose (i) and (ii) '
        'are carded apart.')
_OR6 = ('The paper sets two (c)s either side of an OR: the cutting-tool angles (c), whose (i) '
        'and (ii) are carded apart, and the CNC (c), "Any three" of four terms, carded at the '
        'letter.')
_OR7 = ('The paper sets two (c)s either side of an OR, the instruments and the circuit '
        'symbols, each "any three" of four; the scheme prices both "Award 3 @ 5 Marks", so '
        'they are one card, each branch a route.')
_B4 = "The scheme prints 'Any three: Award 3 @ 4 Marks' for the three parts answered."

CROPS = {
    # ---- paper ------------------------------------------------------------
    'engineering-2011-OL-paper-q1a-crop': dict(
        doc='paper', page=2, rect=(498, 110, 560, 173), image=True, ref='2011 OL Q1(a)'),
    'engineering-2011-OL-paper-q1e-crop': dict(
        doc='paper', page=2, rect=(510, 206, 549, 283), image=True, ref='2011 OL Q1(e)'),
    'engineering-2011-OL-paper-q1h-crop': dict(
        doc='paper', page=2, rect=(452, 319, 546, 406), image=True, ref='2011 OL Q1(h)'),
    'engineering-2011-OL-paper-q1m-crop': dict(
        doc='paper', page=2, rect=(275, 728, 450, 790), mask=[(264, 727, 326, 743)],
        ref='2011 OL Q1(m)'),
    # The four furnaces drawn under their captions (i)-(iv).
    'engineering-2011-OL-paper-q2a-crop': dict(
        doc='paper', page=3, rect=(92, 100, 560, 197), ref='2011 OL Q2(a)'),
    # The centre punch with its point A.
    'engineering-2011-OL-paper-q3b-crop': dict(
        doc='paper', page=3, rect=(110, 496, 550, 566), mask=[(109, 490, 500, 508.5)],
        ref='2011 OL Q3(b)', letters=('A',)),
    'engineering-2011-OL-paper-q3dor-crop': dict(
        doc='paper', page=3, rect=(398, 704, 519, 797), image=True, ref='2011 OL Q3(d)'),
    # The two nuts, A and B.
    'engineering-2011-OL-paper-q4biv-crop': dict(
        doc='paper', page=4, rect=(148, 268, 360, 328), ref='2011 OL Q4(b)(iv)',
        letters=('A', 'B')),
    'engineering-2011-OL-paper-q4d-crop': dict(
        doc='paper', page=4, rect=(464, 381, 512, 425), ref='2011 OL Q4(d)'),
    # The two processes, A and B.
    'engineering-2011-OL-paper-q5a-crop': dict(
        doc='paper', page=4, rect=(114, 499, 462, 598), ref='2011 OL Q5(a)', letters=('A', 'B')),
    # The four work-holding methods photographed and captioned (i)-(iv).
    'engineering-2011-OL-paper-q6a-crop': dict(
        doc='paper', page=5, rect=(36, 105, 563, 224), ref='2011 OL Q6(a)'),
    # The cutting tool with its angles A and B.
    'engineering-2011-OL-paper-q6c-crop': dict(
        doc='paper', page=5, rect=(145, 410, 442, 652), ref='2011 OL Q6(c)', letters=('A', 'B')),
    # The two fits drawn at A and B.
    'engineering-2011-OL-paper-q7a-crop': dict(
        doc='paper', page=6, rect=(105, 104, 480, 218), ref='2011 OL Q7(a)', letters=('A', 'B')),
    'engineering-2011-OL-paper-q7b-crop': dict(
        doc='paper', page=6, rect=(385, 245, 573, 388), ref='2011 OL Q7(b)'),
    # Both (c)s' pictures: the instruments captioned (i)-(iv), and the
    # components under their names.
    'engineering-2011-OL-paper-q7c-crop': dict(
        doc='paper', parts=[(6, (50, 428, 570, 565)), (6, (95, 690, 510, 790))],
        ref='2011 OL Q7(c)'),
    # ---- scheme: the drawings the answers are given with -------------------
    'engineering-2011-OL-scheme-q7c-sol': dict(
        doc='scheme', page=16, rect=(80, 652, 515, 714), solution=True, ref='2011 OL Q7(c)'),
}

CARDS = [
    # ---- Question 1, Section A ("Any six @ 5 marks each") ------------------
    dict(key=(1, 'a', None),
         why='The sign is pictured beside (a); scheme p5 numbers two reasons; "3 + 2 Marks".',
         topic='eng-3-1',
         lifted=[S(5, 89, 359, 488, 375), S(5, 92, 385, 488, 402)],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         question_figure='engineering-2011-OL-paper-q1a-crop',
         notes="The scheme prints '3 + 2 Marks'. " + _SA),
    dict(key=(1, 'b', None),
         why='Scheme p5 names the alloy in one sentence, "5 Marks".',
         topic='eng-1-5',
         lifted=[S(5, 61, 413, 480, 430)], marks=[5], total=5,
         notes="The scheme prints '5 Marks'. " + _SA),
    dict(key=(1, 'c', None),
         why='Scheme p5 answers in one sentence, "5 Marks".',
         topic='eng-2-11',
         lifted=[S(5, 61, 441, 480, 471)], marks=[5], total=5,
         notes="The scheme prints '5 Marks'. " + _SA),
    dict(key=(1, 'd', None),
         why='Scheme p5 names a thread form and its use in one sentence, "5 Marks".',
         topic='eng-2-11',
         lifted=[S(5, 61, 482, 480, 512)], marks=[5], total=5,
         notes="The scheme prints '5 Marks'. " + _SA),
    dict(key=(1, 'e', None),
         why='The switch is pictured beside (e); scheme p5 answers in one sentence, "5 '
             'Marks".',
         topic='eng-2-16',
         lifted=[S(5, 61, 523, 480, 541)], marks=[5], total=5,
         question_figure='engineering-2011-OL-paper-q1e-crop',
         notes="The scheme prints '5 Marks'. " + _SA),
    dict(key=(1, 'f', None),
         why='Scheme p5 answers in one sentence and prints no mark under it; Section A is '
             '"Any six @ 5 marks each".',
         topic='eng-3-7',
         lifted=[S(5, 61, 551, 480, 568)], marks=[5], total=5,
         notes="The scheme prints no mark under (f); its grid prints 'Any six @ 5 marks "
               "each'."),
    dict(key=(1, 'g', None),
         why='Scheme p5 gives two advantages after their romans, "3 +2 Marks".',
         topic='eng-3-14',
         lifted=[S(5, 84, 579, 488, 609), S(5, 86, 620, 488, 650)],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         notes="The scheme prints '3 +2 Marks'. " + _SA),
    dict(key=(1, 'h', None),
         why='The gears are pictured beside (h); scheme p5 names the mechanism and then its '
             'use, after their romans; "3+2 Marks".',
         topic='eng-2-15',
         question_lift=P(2, 60, 328, 385, 345),
         lifted=[S(5, 82, 661, 488, 678), S(5, 83, 689, 488, 720)],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         question_figure='engineering-2011-OL-paper-q1h-crop',
         notes="The scheme prints '3+2 Marks'. " + _SA),
    # ---- Question 1, Section B ("Any three parts @ 12 + 12 + 11 Marks") ----
    dict(key=(1, 'i', None),
         why='Scheme p6 describes each of the three under its name; "Any one", "Award 12 '
             '(11) Marks".',
         topic='eng-2-15', stem=False,
         lifted=[[S(6, 85, 146, 440, 246), S(6, 85, 326, 440, 440), S(6, 85, 519, 440, 633)]],
         row_kind='anyN', group=(1, 12), marks=[12], tariff='fixed', total=12,
         notes="The scheme prints 'Any one: Good clear description Award 12 (11) Marks'. "
               + _SB),
    dict(key=(1, 'j', None),
         why='Scheme p7 explains each term under its name, "Any two", "Award 6 + 6(5)".',
         topic='eng-3-14', stem=False,
         lifted=[[S(7, 85, 149, 460, 221), S(7, 85, 259, 460, 373), S(7, 85, 411, 460, 511),
                  S(7, 85, 549, 460, 649)]],
         row_kind='anyN', group=(2, 6), marks=[12], tariff='fixed', total=12,
         notes="The scheme prints 'Any two: Good clear description Award 6 + 6(5)'. " + _SB),
    dict(key=(1, 'k', None),
         why='Scheme p8 defines the term under its heading and gives an example, "Definition '
             'Award 6(5) Marks", "Eample Award 6(5) Marks" (the scheme\'s spelling).',
         topic='eng-3-8', stem=False,
         lifted=[S(8, 85, 87, 440, 131), S(8, 85, 142, 440, 187)],
         marks=[6, 6], total=12,
         notes="The scheme prints 'Definition Award 6(5) Marks' and 'Eample Award 6(5) Marks'. "
               + _SB),
    dict(key=(1, 'l', None),
         why='Scheme p8 explains each term under its name, "Any two", "Award 6 + 6 (5)".',
         topic='eng-3-14', stem=False,
         lifted=[[S(8, 85, 241, 460, 313), S(8, 85, 323, 480, 410), S(8, 85, 420, 505, 479),
                  S(8, 85, 489, 470, 548)]],
         row_kind='anyN', group=(2, 6), marks=[12], tariff='fixed', total=12,
         notes="The scheme prints 'Any two: Good description Award 6 + 6 (5)'. " + _SB),
    dict(key=(1, 'm', None),
         why='The tool is drawn beside (m); scheme p8 names it and gives its function under '
             'their headings, "Name Award 6(5) Marks", "Function Award 6(5) Marks".',
         topic='eng-2-11', stem=False,
         lifted=[S(8, 82, 603, 425, 621), S(8, 82, 645, 470, 704)],
         marks=[6, 6], total=12,
         question_figure='engineering-2011-OL-paper-q1m-crop',
         notes="The scheme prints 'Name Award 6(5) Marks' and 'Function Award 6(5) Marks'. "
               + _SB),
    # ---- Question 2 --------------------------------------------------------
    dict(key=(2, 'a', None),
         why='The four furnaces are drawn and captioned (i)-(iv) with no words; scheme p9 '
             'names each and states its function after its roman, any three, "Name and '
             'function Award 3 @ 5 Marks".',
         topic='eng-1-4',
         lifted=[[S(9, 70, 128, 448, 158), S(9, 66, 155, 448, 186), S(9, 66, 183, 448, 214),
                  S(9, 66, 211, 448, 242)]],
         row_kind='anyN', group=(3, 5), marks=[15], tariff='fixed', total=15,
         question_figure='engineering-2011-OL-paper-q2a-crop',
         notes="The scheme prints 'Any three: Name and function Award 3 @ 5 Marks'."),
    dict(key=(2, 'b', None),
         why='A lead-in over four terms set as romans, "any three"; scheme p9 describes each '
             'under its name, "Good clear description Award 3 @ 5 Marks".',
         topic='eng-1-4',
         lifted=[[S(9, 66, 273, 445, 315), S(9, 64, 328, 460, 373), S(9, 64, 383, 445, 442),
                  S(9, 60, 452, 465, 497)]],
         row_kind='anyN', group=(3, 5), marks=[15], tariff='fixed', total=15,
         notes="The scheme prints 'Any three descriptions: Good clear description Award 3 @ 5 "
               "Marks'."),
    dict(key=(2, 'c', None),
         why='A lead-in over four metals set as romans, "any three"; scheme p9 names a '
             'component after each metal, "Component Award 3 @ 3 Marks". The scheme\'s '
             '"Aiuminium" and "(vi)" are lifted as printed.',
         topic='eng-1-2',
         lifted=[[S(9, 70, 549, 425, 566), S(9, 70, 563, 425, 579.5), S(9, 70, 579.5, 425, 593),
                  S(9, 70, 593, 425, 607)]],
         row_kind='anyN', group=(3, 3), marks=[9], tariff='fixed', total=9,
         notes="The scheme prints 'Any three metals: Component Award 3 @ 3 Marks'. It spells "
               "aluminium 'Aiuminium' and numbers high-speed steel '(vi)', the paper's (iv)."),
    dict(key=(2, 'd', None),
         why='Scheme p9 bullets two advantages under an opening sentence, "Advantages Award 2 '
             '@ 3 Marks".',
         topic='eng-1-2',
         lifted=[S(9, 66, 660, 435, 690), S(9, 66, 689, 435, 718)],
         marks=[3, 3], total=6,
         notes="The scheme prints 'Advantages Award 2 @ 3 Marks', and opens: '"
               + S(9, 66, 645, 435, 662) + "'"),
    # ---- Question 3 --------------------------------------------------------
    dict(key=(3, 'a', None),
         why='A lead-in over three processes set as romans, "any two"; scheme p10 describes '
             'each under its name, "Good clear description Award 2 @ 8 Marks".',
         topic='eng-2-6',
         lifted=[[S(10, 70, 128, 435, 199), S(10, 66, 211, 450, 268), S(10, 70, 280, 460, 379)]],
         row_kind='anyN', group=(2, 8), marks=[16], tariff='fixed', total=16,
         notes="The scheme prints 'Any two descriptions: Good clear description Award 2 @ 8 "
               "Marks'."),
    dict(key=(3, 'b', 'i'),
         why='The centre punch is pictured with its point at A; scheme p10 gives the reason '
             'under "One reason", "Reason Award 5 Marks".',
         topic='eng-2-6',
         lifted=[S(10, 92, 431, 440, 476)], marks=[5], total=5,
         question_figure='engineering-2011-OL-paper-q3b-crop',
         notes="The scheme prints 'Reason Award 5 Marks'."),
    dict(key=(3, 'b', 'ii'),
         why='Scheme p10 gives the method under "One method", "Method Award 5 Marks".',
         topic='eng-2-6',
         lifted=[S(10, 92, 500, 440, 532)], marks=[5], total=5,
         question_figure='engineering-2011-OL-paper-q3b-crop',
         notes="The scheme prints 'Method Award 5 Marks'."),
    dict(key=(3, 'c', None),
         why='Scheme p10 bullets two precautions, "Safety Award 2 @ 5 Marks".',
         topic='eng-3-1',
         lifted=[S(10, 85, 584, 445, 615), S(10, 85, 626, 445, 657)],
         marks=[5, 5], total=10,
         notes="The scheme prints 'Safety Award 2 @ 5 Marks'."),
    dict(key=(3, 'd', None),
         why='Paper p3 sets two alternative (d)s either side of an OR. This card is the '
             'first: scheme pp10-11 describe each property under its name, any two, '
             '"Description Award 1 @ 5 Marks, Award 1 @ 4 Marks".',
         topic='eng-3-8', stem=False,
         question_lift=P(3, 95, 652, 380, 670, more=[(97, 680, 420, 697)]),
         lifted=[S(10, 75, 723, 440, 768), S(11, 72, 84, 490, 129), S(11, 70, 139, 465, 184)],
         tariff='orderedSplit', notation='5 + 4', ladder=9, total=9,
         notes="The scheme prints 'Description Award 1 @ 5 Marks, Award 1 @ 4 Marks'. " + _OR3),
    dict(key=(3, 'd', 'i'),
         why='The OR branch\'s (i), the robot pictured beside it: scheme p11 explains the term '
             'under its heading; the grid prices the branch "Two parts 5 & 4".',
         topic='eng-2-15', stem=False,
         question_lift=P(3, 115, 733, 385, 750),
         lifted=[S(11, 90, 238, 490, 268)], marks=[5], total=5,
         question_figure='engineering-2011-OL-paper-q3dor-crop',
         notes="The scheme's grid prints '(d) Two parts 5 & 4 (9)' for the OR branch. " + _OR3),
    dict(key=(3, 'd', 'ii'),
         why='The OR branch\'s (ii): scheme p11 answers in one sentence; the grid prices the '
             'branch "Two parts 5 & 4".',
         topic='eng-2-15', stem=False,
         question_lift=P(3, 115, 760, 345, 778),
         lifted=[S(11, 88, 280, 500, 310)], marks=[4], total=4,
         question_figure='engineering-2011-OL-paper-q3dor-crop',
         notes="The scheme's grid prints '(d) Two parts 5 & 4 (9)' for the OR branch. " + _OR3),
    # ---- Question 4 --------------------------------------------------------
    dict(key=(4, 'a', None),
         why='Scheme p11 names the three flames on one line under (i) and gives each one\'s '
             'proportions on a line of its own under (ii), "Name & proportions Award 3 @ 5 '
             'Marks": each flame\'s name, lifted by its own word rectangle, with its '
             'proportions.',
         topic='eng-2-10', stem=False,
         question_lift=P(4, 75, 64, 310, 81, items=[(99, 87, 390, 104), (99, 110, 390, 143)]),
         lifted=[join(S(11, 100, 422, 170, 440), S(11, 100, 464, 400, 480)),
                 join(S(11, 182, 422, 263, 440), S(11, 100, 478, 400, 494)),
                 join(S(11, 270, 422, 365, 440), S(11, 100, 492, 400, 508))],
         marks=[5, 5, 5], total=15,
         notes="The scheme prints 'Name & proportions Award 3 @ 5 Marks'."),
    dict(key=(4, 'b', 'i'),
         why='One of "Answer any three of the following": scheme p11 gives two advantages in '
             'two sentences, each lifted by its own rectangle, the 4 for the part not split '
             'between them.',
         topic='eng-2-10',
         lifted=[S(11, 98, 546, 318.5, 563), join(S(11, 318.5, 546, 438, 563),
                                                 S(11, 98, 563, 438, 577))],
         tariff='questionTotal', total=4, notes=_B4),
    dict(key=(4, 'b', 'ii'),
         why='One of "Answer any three of the following": scheme p11 answers in one sentence.',
         topic='eng-2-10',
         question_lift=P(4, 120, 217, 515, 234),
         lifted=[S(11, 98, 574, 440, 605)], marks=[4], total=4, notes=_B4),
    dict(key=(4, 'b', 'iii'),
         why='One of "Answer any three of the following": scheme p11 gives both precautions '
             'in one sentence, one row for the part\'s 4.',
         topic='eng-3-1',
         lifted=[S(11, 98, 602, 480, 618)], marks=[4], total=4, notes=_B4),
    dict(key=(4, 'b', 'iv'),
         why='One of "Answer any three of the following": the two nuts are photographed at A '
             'and B; scheme p11 names and describes each in a sentence, one row for the '
             'part\'s 4.',
         topic='eng-2-10',
         lifted=[S(11, 98, 616, 480, 646)], marks=[4], total=4,
         question_figure='engineering-2011-OL-paper-q4biv-crop',
         notes=_B4),
    dict(key=(4, 'c', None),
         why='A lead-in over four terms set as romans, "any three"; scheme pp11-12 explain '
             'each under its name, "Description Award 3 @ 4 Marks".',
         topic='eng-2-10',
         lifted=[[S(11, 96, 698, 438, 757), S(12, 96, 84, 450, 143), S(12, 96, 167, 455, 226),
                  S(12, 96, 250, 455, 336)]],
         row_kind='anyN', group=(3, 4), marks=[12], tariff='fixed', total=12,
         notes="The scheme prints 'Any three terms: Description Award 3 @ 4 Marks'."),
    dict(key=(4, 'd', None),
         why='The goggles are pictured beside (d); scheme p12 gives two reasons after their '
             'romans, "Reasons Award 2 @ 3 Marks".',
         topic='eng-3-1',
         lifted=[S(12, 92, 415, 438, 446), S(12, 92, 457, 470, 474)],
         marks=[3, 3], total=6,
         question_figure='engineering-2011-OL-paper-q4d-crop',
         notes="The scheme prints 'Reasons Award 2 @ 3 Marks'."),
    # ---- Question 5 --------------------------------------------------------
    dict(key=(5, 'a', 'i'),
         why='The two processes are drawn at A and B; scheme p12 names each after its letter, '
             '"Name Award 2 @ 2 Marks".',
         topic='eng-1-9', stem=False,
         question_lift=P(4, *_A5, more=[(115, 593, 230, 610)]),
         lifted=[S(12, 95, 652, 300, 666.5), S(12, 95, 666.5, 300, 683)],
         marks=[2, 2], total=4,
         labels={'A': S(12, 110, 652, 300, 666.5), 'B': S(12, 110, 666.5, 300, 683)},
         question_figure='engineering-2011-OL-paper-q5a-crop',
         notes="The scheme prints 'Name Award 2 @ 2 Marks'."),
    dict(key=(5, 'a', 'ii'),
         why='Scheme pp12-13 describe each process under its name, "Differences Award 2 @ 5 '
             'Marks".',
         topic='eng-1-9', stem=False,
         question_lift=P(4, *_A5, more=[(115, 614, 445, 631)]),
         lifted=[join(S(12, 85, 721, 438, 766), S(13, 85, 70, 445, 143)),
                 S(13, 85, 153, 490, 239)],
         marks=[5, 5], total=10,
         labels={'A': S(12, 110, 652, 300, 666.5), 'B': S(12, 110, 666.5, 300, 683)},
         question_figure='engineering-2011-OL-paper-q5a-crop',
         notes="The scheme prints 'Differences Award 2 @ 5 Marks', for A and B in that "
               "order."),
    dict(key=(5, 'a', 'iii'),
         why='Scheme p13 gives each process\'s products on a line of its own, "End-product '
             'Award 2 @ 2 Marks".',
         topic='eng-1-9', stem=False,
         question_lift=P(4, *_A5, more=[(115, 635, 355, 652)]),
         lifted=[S(13, 85, 277, 438, 293), S(13, 85, 293, 438, 308)],
         marks=[2, 2], total=4,
         question_figure='engineering-2011-OL-paper-q5a-crop',
         notes="The scheme prints 'End-product Award 2 @ 2 Marks'."),
    dict(key=(5, 'b', None),
         why='Scheme p13 gives two precautions in a paragraph each, "Safety precautions Award '
             '2 @ 3 Marks".',
         topic='eng-1-9',
         lifted=[S(13, 85, 374, 438, 433), S(13, 85, 443, 445, 488)],
         marks=[3, 3], total=6,
         notes="The scheme prints 'Safety precautions Award 2 @ 3 Marks'."),
    dict(key=(5, 'c', None),
         why='A lead-in over four terms set as romans, "any three"; scheme pp13-14 explain '
             'each under its name, "Explanation Award 3 @ 5 Marks".',
         topic='eng-1-9',
         lifted=[[S(13, 85, 567, 438, 640), S(13, 85, 650, 450, 722),
                  join(S(13, 85, 733, 445, 764), S(14, 100, 70, 470, 115)),
                  S(14, 85, 126, 480, 226)]],
         row_kind='anyN', group=(3, 5), marks=[15], tariff='fixed', total=15,
         notes="The scheme prints 'Any three: Explanation Award 3 @ 5 Marks'."),
    dict(key=(5, 'd', None),
         why='Scheme p14 names two materials after their romans, "Material Award 2 @ 3 '
             'Marks".',
         topic='eng-1-9',
         lifted=[S(14, 85, 319, 300, 336), S(14, 85, 346, 300, 364)],
         marks=[3, 3], total=6,
         notes="The scheme prints 'Material Award 2 @ 3 Marks'."),
    # ---- Question 6 --------------------------------------------------------
    dict(key=(6, 'a', None),
         why='The four work-holding methods are photographed and captioned (i)-(iv) with no '
             'words; scheme p14 names each after its roman, any three, "Name Award 3 @ 5 '
             'Marks".',
         topic='eng-2-11',
         lifted=[[S(14, 78, 556, 300, 572), S(14, 78, 569, 300, 585), S(14, 78, 583, 300, 599),
                  S(14, 78, 597, 300, 613)]],
         row_kind='anyN', group=(3, 5), marks=[15], tariff='fixed', total=15,
         question_figure='engineering-2011-OL-paper-q6a-crop',
         notes="The scheme prints 'Any three lathe parts: Name Award 3 @ 5 Marks'."),
    dict(key=(6, 'b', 'i'),
         why='Scheme p14 gives two reasons, one a line, "Award 3 @ 5 Marks" for the three '
             'parts of (b).',
         topic='eng-2-11',
         lifted=[S(14, 95, 707, 300, 724), S(14, 95, 721, 300, 738)],
         marks=[5, 5], total=10,
         notes="The scheme prints 'Cutting fluids Award 3 @ 5 Marks' for (b): two parts here, "
               "one at (ii)."),
    dict(key=(6, 'b', 'ii'),
         why='Scheme p15 gives one precaution, the third part of "Award 3 @ 5 Marks".',
         topic='eng-3-1',
         lifted=[S(15, 95, 70, 400, 88)], marks=[5], total=5,
         notes="The scheme prints 'Cutting fluids Award 3 @ 5 Marks' for (b): two parts at "
               "(i), one here."),
    dict(key=(6, 'c', 'i'),
         why='The angles are drawn at A and B; scheme p15 names each after its letter, the '
             'first two parts of "Name & description Award 3 @ 5 Marks".',
         topic='eng-2-11', stem=False,
         question_lift=P(5, 110, 340, 345, 357),
         lifted=[S(15, 95, 126, 300, 141), S(15, 95, 141, 300, 156)],
         marks=[5, 5], total=10,
         labels={'A': S(15, 145, 126, 300, 141), 'B': S(15, 145, 141, 300, 156)},
         question_figure='engineering-2011-OL-paper-q6c-crop',
         notes="The scheme prints 'Name & description Award 3 @ 5 Marks' for the turning (c): "
               "two parts here, one at (ii). " + _OR6),
    dict(key=(6, 'c', 'ii'),
         why='Scheme p15 gives each angle\'s function under its name; any one, the third '
             'part of "Award 3 @ 5 Marks".',
         topic='eng-2-11', stem=False,
         question_lift=P(5, 112, 367, 425, 384),
         lifted=[[S(15, 104, 195, 485, 238), S(15, 104, 250, 485, 307)]],
         row_kind='anyN', group=(1, 5), marks=[5], tariff='fixed', total=5,
         question_figure='engineering-2011-OL-paper-q6c-crop',
         notes="The scheme prints 'Name & description Award 3 @ 5 Marks' for the turning (c): "
               "two parts at (i), one here. " + _OR6),
    dict(key=(6, 'c', None),
         why='The OR branch: "Explain any three of the following" four CNC terms; scheme p15 '
             'explains each under its name, "Explanation Award 3 @ 5 Marks". The scheme\'s '
             'last line breaks off at "co-ordinat"; lifted as printed.',
         topic='eng-2-11', stem=False,
         question_lift=P(5, 75, 712, 530, 729, more=[(85, 740, 532, 757)]),
         lifted=[[S(15, 85, 459, 445, 532), S(15, 85, 542, 495, 601), S(15, 85, 611, 460, 670),
                  S(15, 85, 680, 495, 766)]],
         row_kind='anyN', group=(3, 5), marks=[15], tariff='fixed', total=15,
         notes="The scheme prints 'Any three: Explanation Award 3 @ 5 Marks'. " + _OR6),
    # ---- Question 7 --------------------------------------------------------
    dict(key=(7, 'a', None),
         why='The two fits are drawn at A and B; scheme p16 names and describes each after '
             'its letter, "Name & description Award 2 @ 5 Marks".',
         topic='eng-3-12',
         lifted=[S(16, 85, 156, 438, 200), S(16, 85, 211, 438, 256)],
         marks=[5, 5], total=10,
         labels={'A': S(16, 141, 156, 300, 172), 'B': S(16, 140.5, 211, 300, 228)},
         question_figure='engineering-2011-OL-paper-q7a-crop',
         notes="The scheme prints 'Name & description Award 2 @ 5 Marks', for A and B in that "
               "order."),
    dict(key=(7, 'b', None),
         why='Figure 1 dimensions the hole and shaft beside (b); scheme p16 states each value '
             'after its roman, "Calculations Award 4 @ 5 Marks". The question is lifted with '
             'its romans, which the reader files as parts of their own.',
         topic='eng-3-12', stem=False,
         question_lift=P(6, 75, 229, 360, 246, more=[(168, 257, 352, 274), (168, 277, 352, 295),
                                                     (168, 298, 350, 315),
                                                     (168, 319, 390, 364)]),
         lifted=[S(16, 80, 293, 438, 309), S(16, 80, 309, 438, 323), S(16, 78, 323, 438, 334),
                 S(16, 78, 334, 438, 349)],
         marks=[5, 5, 5, 5], total=20,
         question_figure='engineering-2011-OL-paper-q7b-crop',
         notes="The scheme prints 'Calculations Award 4 @ 5 Marks'."),
    dict(key=(7, 'c', None),
         why='Paper p6 sets two alternative (c)s either side of an OR, each "any three" of '
             'four. Scheme p16 names each instrument with an application after its roman, '
             '"Name & application Award 3 @ 5 Marks", and draws each component\'s symbol '
             'under its name, shown with the answer, "Symbols Award 3 @ 5 Marks": one card, '
             'each branch a route; a symbol row carries the component it is for.',
         topic='eng-3-12', stem=False,
         question_lift=P(6, 75, 402, 480, 419, more=[(280, 586, 310, 605), (75, 629, 485, 647),
                                                     (80, 671, 518, 688)]),
         lifted=[[S(16, 78, 418, 438, 434), S(16, 78, 431, 438, 448), S(16, 78, 445, 438, 462),
                  S(16, 78, 459, 438, 476)],
                 [S(16, 80, 632, 150, 649), S(16, 150, 632, 300, 649), S(16, 300, 632, 410, 649),
                  S(16, 410, 632, 495, 649)]],
         row_kind='anyN', group=[(3, 5), (3, 5)], marks=[15, 15], routes=['a', 'b'],
         tariff='fixed', total=15,
         question_figure='engineering-2011-OL-paper-q7c-crop',
         figure='engineering-2011-OL-scheme-q7c-sol',
         notes="The scheme prints 'Name & application Award 3 @ 5 Marks' and, for the OR, "
               "'Symbols Award 3 @ 5 Marks'. " + _OR7),
]

TOPICS = {}

ATLAS = {
    'eng-2011-ol-q4-b-iii': dict(
        topics=['Mechanical Joining & Assembly'],
        note='Bonding acrylic with adhesive, a joining method, one of Q4(b)\'s joining parts; '
             'the card\'s syllabus heading is Safety.'),
    'eng-2011-ol-q4-d': dict(
        topics=['Welding & Soldering'],
        note='Goggles for brazing, a hot joining process, under Q4\'s Welding & Soldering; the '
             'card\'s syllabus heading is Safety.'),
}
