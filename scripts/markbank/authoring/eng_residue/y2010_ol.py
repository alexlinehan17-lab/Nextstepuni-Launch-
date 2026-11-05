"""2010 Ordinary Level: every part, from the page.

Paper and scheme as the PDFs number their pages. As in 2011-2019, the automatic
author prices nothing in this sitting: the scheme sets each answer in a left
column and its award in a box to the right ("Award 3 @ 6 Marks"), which its
reader does not join to the answer, so every card here is built from the page
by rectangle, and the few cards the automatic author does build from this
scheme's marks grid (whole questions, a letter over two separate romans)
are split or replaced below. The marks grid is on scheme p4: Question 1 is Section A, "Any
six @ 5 marks each", two-part answers 3 + 2, and Section B, "Any three parts
@ 12 + 12 + 11 marks", two-part answers "6 + 6 or 6 + 5"; Questions 2-7 are 45
marks each. A Section B card carries the PRINTED primary price, the 12 the
scheme awards a part answered first or second ("Award 12 (11) Marks"), and
says the third part answered earns 11.
"""
from eng_lift import join, lift

Y, L = 2010, 'ol'
NEW = 'never shipped: the automatic card '


def S(page, *rect):
    return lift(Y, L, 'scheme', page, rect)


def P(page, *rect, more=(), items=()):
    return lift(Y, L, 'paper', page, rect, more=more, items=items)


def _ck(page, part, lead):
    return (f'Paper p{page} prints {part} as one item of the list under "{lead}"; the '
            'semicolon ends the item, not the question.')


_SB = ("Section B is 'Any three parts @ 12 + 12 + 11 marks': the card carries the 12 a part "
       "earns answered first or second; answered third it earns 11.")
_SA = "Section A is 'Any six @ 5 marks each'."
_OR3 = ('The paper sets two (d)s either side of an OR, the two steels and robotics in car '
        'manufacture; the scheme prices both "Award 1 @ 5 Marks, Award 1 @ 4 Marks", so they '
        'are one card, each branch a route.')
_OR6 = ('The paper sets two (c)s either side of an OR, one method of taper turning and the '
        'advantages of a CNC lathe; each is priced at 12, so they are one card, each branch a '
        'route.')
_OR7 = ('The paper sets two (c)s either side of an OR, the tools and the circuit components, '
        'each "any three" of four; the scheme prices both "Award 3 @ 5 Marks", so they are one '
        'card, each branch a route.')
_B4 = "The scheme prints 'Any three: Explanation Award 3 @ 4 Marks' for the three parts answered."

CROPS = {
    # ---- paper ------------------------------------------------------------
    'engineering-2010-OL-paper-q1b-crop': dict(
        doc='paper', page=2, rect=(462, 130, 500, 244), ref='2010 OL Q1(b)'),
    # The jack and the vice; the end of (g)'s "improve", which runs under the jack,
    # is whited out.
    'engineering-2010-OL-paper-q1f-crop': dict(
        doc='paper', page=2, rect=(384, 256, 548, 328), mask=[(383, 313, 403, 331)],
        ref='2010 OL Q1(f)'),
    'engineering-2010-OL-paper-q1h-crop': dict(
        doc='paper', page=2, rect=(378, 334, 494, 420), ref='2010 OL Q1(h)'),
    'engineering-2010-OL-paper-q1m-crop': dict(
        doc='paper', page=2, rect=(366, 706, 480, 806), ref='2010 OL Q1(m)'),
    # The four objects in a row.
    'engineering-2010-OL-paper-q2c-crop': dict(
        doc='paper', page=3, rect=(78, 286, 548, 350), ref='2010 OL Q2(c)'),
    # The screwdriver with "Shaft".
    'engineering-2010-OL-paper-q3b-crop': dict(
        doc='paper', page=3, rect=(105, 568, 472, 628), ref='2010 OL Q3(b)'),
    'engineering-2010-OL-paper-q3dor-crop': dict(
        doc='paper', page=3, rect=(384, 712, 473, 808), ref='2010 OL Q3(d)'),
    'engineering-2010-OL-paper-q4b-crop': dict(
        doc='paper', page=4, rect=(476, 130, 560, 272), ref='2010 OL Q4(b)'),
    # The three components with their captions.
    'engineering-2010-OL-paper-q5a-crop': dict(
        doc='paper', page=4, rect=(110, 488, 495, 628), ref='2010 OL Q5(a)'),
    # The four lathe parts with their captions (i)-(iv).
    'engineering-2010-OL-paper-q6a-crop': dict(
        doc='paper', page=5, rect=(36, 128, 566, 245), ref='2010 OL Q6(a)'),
    'engineering-2010-OL-paper-q6cor-crop': dict(
        doc='paper', page=5, rect=(70, 572, 542, 778), ref='2010 OL Q6(c)'),
    # The hole with its dimension; the end of (b)'s "dimensions shown:" is whited
    # out.
    'engineering-2010-OL-paper-q7b-crop': dict(
        doc='paper', page=6, rect=(365, 158, 562, 252), mask=[(364, 159, 428, 178)],
        ref='2010 OL Q7(b)'),
    # The four tools with their captions, then the OR branch's circuit.
    'engineering-2010-OL-paper-q7c-crop': dict(
        doc='paper', parts=[(6, (26, 388, 562, 528)), (6, (360, 605, 550, 740))],
        ref='2010 OL Q7(c)'),
    # ---- scheme: the drawings the answers are given with -------------------
    'engineering-2010-OL-scheme-q1k-sol': dict(
        doc='scheme', page=7, rect=(130, 625, 400, 650), solution=True, ref='2010 OL Q1(k)'),
    'engineering-2010-OL-scheme-q2a-sol': dict(
        doc='scheme', page=9, rect=(10, 160, 170, 610), solution=True, ref='2010 OL Q2(a)(i)'),
    'engineering-2010-OL-scheme-q5a-sol': dict(
        doc='scheme', parts=[(13, (200, 322, 350, 374)), (13, (180, 483, 380, 553)),
                             (13, (190, 653, 356, 733))],
        layout='row', solution=True, ref='2010 OL Q5(a)(ii)'),
    'engineering-2010-OL-scheme-q6c-sol': dict(
        doc='scheme', page=16, rect=(180, 200, 372, 376), solution=True, ref='2010 OL Q6(c)'),
}

SPLIT = {
    'eng-2010-ol-q2': 'never shipped: a card for the whole of Question 2 under the grid\'s '
                      '"Question 2 - 45 marks", its rows the answers to (a) and (b) in one '
                      'ordered split; the module cards its parts',
    'eng-2010-ol-q4': 'never shipped: a card for the whole of Question 4 under the grid\'s '
                      '"Question 4 - 45 marks", its rows the answers to (a), (b) and (c) in '
                      'one ordered split; the module cards its parts',
    'eng-2010-ol-q2-a': 'never shipped: (a)(i) and (a)(ii) are questions of their own, '
                        'priced 8 and 6; the automatic card ran (i)\'s three furnaces as '
                        'options at 8 under a question that joins both',
}

CARDS = [
    # ---- Question 1, Section A ("Any six @ 5 marks each") ------------------
    dict(key=(1, 'a', None),
         why='Scheme p5 numbers two precautions; "3 + 2 Marks".',
         topic='eng-3-1',
         lifted=[S(5, 90, 457, 450, 473), S(5, 90, 471, 450, 487)],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         notes="The scheme prints '3 + 2 Marks'. " + _SA),
    dict(key=(1, 'b', None),
         why='The LED is pictured beside (b); scheme p5 answers in one sentence, "5 Marks".',
         topic='eng-2-16',
         lifted=[S(5, 74, 498, 450, 527)], marks=[5], total=5,
         question_figure='engineering-2010-OL-paper-q1b-crop',
         notes="The scheme prints '5 Marks'. " + _SA),
    dict(key=(1, 'c', None),
         why='Scheme p5 answers in one sentence, "5 Marks".',
         topic='eng-2-11',
         lifted=[S(5, 74, 537, 450, 553)], marks=[5], total=5,
         notes="The scheme prints '5 Marks'. " + _SA),
    dict(key=(1, 'd', None),
         why='Scheme p5 answers in one sentence, "5 Marks".',
         topic='eng-3-8',
         lifted=[S(5, 74, 564, 450, 580)], marks=[5], total=5,
         notes="The scheme prints '5 Marks'. " + _SA),
    dict(key=(1, 'e', None),
         why='Scheme p5 answers in one sentence, "5 Marks".',
         topic='eng-3-12',
         lifted=[S(5, 74, 590, 450, 607)], marks=[5], total=5,
         notes="The scheme prints '5 Marks'. " + _SA),
    dict(key=(1, 'f', None),
         why='The jack and the vice are pictured beside (f); scheme p5 names a thread form '
             'for each after its roman, "3 + 2 Marks".',
         topic='eng-2-11',
         lifted=[S(5, 90, 619, 165, 634), S(5, 184, 619, 300, 634)],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         question_figure='engineering-2010-OL-paper-q1f-crop',
         notes="The scheme prints '3 + 2 Marks', for (i) and (ii). " + _SA),
    dict(key=(1, 'g', None),
         why='Scheme p5 numbers two ways; "3 +2 Marks".',
         topic='eng-3-14',
         lifted=[S(5, 90, 645, 450, 660.5), S(5, 90, 660.5, 455, 676)],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         notes="The scheme prints '3 +2 Marks'. " + _SA),
    dict(key=(1, 'h', None),
         why='The rack and pinion is pictured beside (h); scheme p5 numbers two machines; '
             '"3+2 Marks". The reader files the Section B heading as (h)\'s stem, so the '
             'card carries none.',
         topic='eng-2-15', stem=False,
         lifted=[S(5, 88, 686, 490, 713), S(5, 88, 713, 455, 728)],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         question_figure='engineering-2010-OL-paper-q1h-crop',
         notes="The scheme prints '3+2 Marks'. " + _SA),
    # ---- Question 1, Section B ("Any three parts @ 12 + 12 + 11 marks") ----
    dict(key=(1, 'i', None),
         why='Scheme p6 describes each of the three under its name, "Any one", "Award 12 '
             '(11) Marks".',
         topic='eng-2-15', stem=False,
         lifted=[[S(6, 78, 194, 462, 317), S(6, 76, 368, 475, 491), S(6, 78, 543, 492, 666)]],
         row_kind='anyN', group=(1, 12), marks=[12], tariff='fixed', total=12,
         notes="The scheme prints 'Any one: Good clear description Award 12 (11) Marks'. "
               + _SB),
    dict(key=(1, 'j', None),
         why='Scheme p7 explains each term under its name, "Any two", "Award 6 + 6(5)".',
         topic='eng-3-14', stem=False,
         lifted=[[S(7, 80, 133, 510, 203), S(7, 80, 227, 510, 324), S(7, 80, 348, 510, 431),
                  S(7, 80, 455, 510, 511)]],
         row_kind='anyN', group=(2, 6), marks=[12], tariff='fixed', total=12,
         notes="The scheme prints 'Any two: Good clear description Award 6 + 6(5)'. " + _SB),
    dict(key=(1, 'k', None),
         why='Scheme p7 defines the property beside a drawing of it, shown with the answer, '
             'then gives an application; "Award 6 + 6 (5)".',
         topic='eng-3-8', stem=False,
         lifted=[S(7, 80, 578, 455, 608), S(7, 80, 672, 470, 702)], marks=[6, 6], total=12,
         figure='engineering-2010-OL-scheme-q1k-sol',
         notes="The scheme prints 'Good description Award 6 + 6 (5)', for the definition "
               "and the application in that order. " + _SB),
    dict(key=(1, 'l', None),
         why='Scheme p8 explains each term under its name, "Any two", "Award 6 + 6(5)".',
         topic='eng-2-15', stem=False,
         lifted=[[S(8, 80, 133, 455, 230), S(8, 80, 241, 470, 337), S(8, 80, 348, 470, 444),
                  S(8, 80, 455, 475, 538)]],
         row_kind='anyN', group=(2, 6), marks=[12], tariff='fixed', total=12,
         notes="The scheme prints 'Any two: Good clear description Award 6 + 6(5)'. " + _SB),
    dict(key=(1, 'm', None),
         why='The mechanism is pictured beside (m); scheme p8 names it and describes its '
             'operation under their headings, "Name Award 6 (5) Marks", "Operation Award '
             '6(5) Marks".',
         topic='eng-2-15', stem=False,
         lifted=[S(8, 80, 594, 300, 612), S(8, 80, 634, 500, 731)], marks=[6, 6], total=12,
         question_figure='engineering-2010-OL-paper-q1m-crop',
         notes="The scheme prints 'Name Award 6 (5) Marks' and 'Operation Award 6(5) Marks'. "
               + _SB),
    # ---- Question 2 --------------------------------------------------------
    dict(key=(2, 'a', 'i'),
         why='"Any one" furnace: scheme p9 describes each beside a drawing of it, shown with '
             'the answer; "(i) Sketch & Operation Award 8 Marks".',
         topic='eng-1-4', stem=False,
         question_lift=P(3, 112, 73, 530, 90, more=[(112, 87, 165, 104), (112, 105, 530, 122)]),
         lifted=[[S(9, 178, 169, 420, 279), S(9, 180, 326, 470, 436), S(9, 180, 468, 440, 604)]],
         row_kind='anyN', group=(1, 8), marks=[8], tariff='fixed', total=8,
         figure='engineering-2010-OL-scheme-q2a-sol',
         notes="The scheme prints '(i) Sketch & Operation Award 8 Marks'."),
    dict(key=(2, 'a', 'ii'),
         why='Scheme p9 gives each furnace\'s material and an application in one line, "Any '
             'one", "(ii) Name & Application Award 6 Marks".',
         topic='eng-1-4', stem=False,
         lifted=[[S(9, 128, 670, 525, 686), S(9, 128, 684, 525, 699.5),
                  S(9, 128, 699.5, 525, 713)]],
         row_kind='anyN', group=(1, 6), marks=[6], tariff='fixed', total=6,
         notes="The scheme prints '(ii) Name & Application Award 6 Marks'; its marks grid "
               "prints 'Two parts @ 3 each'."),
    dict(key=(2, 'b', None),
         why='A lead-in over four alloys set as romans, "any three"; scheme p10 gives each '
             'alloy\'s metals after it, "Award 3 @ 6 Marks".',
         topic='eng-1-5',
         lifted=[[S(10, 128, 131, 440, 146.5), S(10, 128, 146.5, 440, 160),
                  S(10, 128, 160, 440, 173.5), S(10, 128, 173.5, 440, 187)]],
         row_kind='anyN', group=(3, 6), marks=[18], tariff='fixed', total=18,
         notes="The scheme prints 'Any three alloys: Alloy Award 3 @ 6 Marks'."),
    dict(key=(2, 'c', None),
         why='A lead-in over four objects set as romans, each pictured, "any three"; scheme '
             'p10 gives each a material, "Award 3 @ 3 Marks".',
         topic='eng-1-4',
         lifted=[[S(10, 128, 305, 440, 320.5), S(10, 128, 320.5, 440, 334),
                  S(10, 128, 334, 440, 347.5), S(10, 128, 347.5, 440, 362)]],
         row_kind='anyN', group=(3, 3), marks=[9], tariff='fixed', total=9,
         question_figure='engineering-2010-OL-paper-q2c-crop',
         notes="The scheme prints 'Any three materials: Materials Award 3 @ 3 Marks'."),
    dict(key=(2, 'd', None),
         why='Scheme p10 lists six metals in one line, each lifted by its own word '
             'rectangle; "Award 2 @ 2 Marks".',
         topic='eng-1-5',
         lifted=[S(10, 118, 466, 156, 482), S(10, 161, 466, 191, 482), S(10, 196, 466, 216, 482),
                 S(10, 221, 466, 279, 482), S(10, 284, 466, 322, 482),
                 S(10, 327, 466, 374, 482)],
         tariff='orderedSplit', notation='2 + 2', ladder=4, total=4,
         notes="The scheme prints 'Any two non-ferrous metals: Award 2 @ 2 Marks', after "
               "'Copper / Brass / Tin / Aluminium / Bronze / Lead etc.'"),
    # ---- Question 3 --------------------------------------------------------
    dict(key=(3, 'a', 'i'),
         why='Scheme p11 names the process, then describes it under its heading; "Award 2 @ '
             '8 Marks", 8 for (i).',
         topic='eng-2-6', stem=False,
         checked=('Paper p3 prints (a)(i) as one item of the list under "each of the '
                  'following:"; the semicolon ends the item, not the question.'),
         question_lift=P(3, 95, 464, 530, 481, more=[(118, 487, 280, 504)]),
         lifted=[join(S(11, 123, 160, 300, 176), S(11, 130, 200, 482, 243))], marks=[8],
         total=8,
         notes="The scheme prints 'Good clear description Award 2 @ 8 Marks', for (i) and "
               "(ii)."),
    dict(key=(3, 'a', 'ii'),
         why='Scheme p11 names the process, then describes it under its heading; "Award 2 @ '
             '8 Marks", 8 for (ii).',
         topic='eng-2-6', stem=False,
         question_lift=P(3, 95, 464, 530, 481, more=[(118, 514, 370, 532)]),
         lifted=[join(S(11, 123, 254, 300, 270), S(11, 128, 294, 505, 364))], marks=[8],
         total=8,
         notes="The scheme prints 'Good clear description Award 2 @ 8 Marks', for (i) and "
               "(ii)."),
    dict(key=(3, 'b', None),
         why='The screwdriver is drawn beside (b); scheme p11 describes case hardening in '
             'one paragraph under its heading, "Award 12 Marks".',
         topic='eng-2-6',
         lifted=[S(11, 130, 402, 455, 511)], marks=[12], total=12,
         question_figure='engineering-2010-OL-paper-q3b-crop',
         notes="The scheme prints 'Good clear description Award 12 Marks'."),
    dict(key=(3, 'c', None),
         why='Scheme p11 bullets two reasons, "Award 2 @ 4 Marks".',
         topic='eng-3-1',
         lifted=[S(11, 150, 537, 455, 553), S(11, 150, 551, 455, 580)], marks=[4, 4], total=8,
         notes="The scheme prints 'Reasons Award 2 @ 4 Marks'."),
    dict(key=(3, 'd', None),
         why='Paper p3 sets two alternative (d)s either side of an OR. Scheme p11 bullets two '
             'differences between the steels and, for the OR, two robotics applications, '
             'each "Award 1 @ 5 Marks, Award 1 @ 4 Marks": priced alike, one card with a '
             'route per branch.',
         topic='eng-1-4', stem=False,
         question_lift=P(3, 95, 694, 460, 711, more=[(190, 726, 220, 746),
                                                     (95, 760, 300, 791)]),
         lifted=[S(11, 150, 605, 455, 622), S(11, 150, 622, 455, 637),
                 S(11, 150, 699, 455, 716), S(11, 150, 716, 455, 731)],
         marks=[5, 4, 5, 4], routes=['a', 'a', 'b', 'b'], total=9,
         question_figure='engineering-2010-OL-paper-q3dor-crop',
         notes="The scheme prints 'Description Award 1 @ 5 Marks, Award 1 @ 4 Marks' for "
               "each branch. " + _OR3),
    # ---- Question 4 --------------------------------------------------------
    dict(key=(4, 'a', 'i'),
         why='Scheme p12 describes each process in a paragraph under its name, '
             '"Differences Award 2 @ 5 Marks".',
         topic='eng-2-10',
         lifted=[S(12, 130, 149, 455, 218), S(12, 130, 229, 470, 299)], marks=[5, 5],
         total=10,
         notes="The scheme prints 'Differences Award 2 @ 5 Marks', for manual metal arc "
               "welding and adhesive bonding in that order."),
    dict(key=(4, 'a', 'ii'),
         why='Scheme p12 gives each process\'s applications in a line, "Application Award '
             '2 @ 3 Marks".',
         topic='eng-2-10',
         lifted=[S(12, 130, 310, 490, 326), S(12, 130, 323, 490, 339)], marks=[3, 3],
         total=6,
         notes="The scheme prints 'Application Award 2 @ 3 Marks', for manual metal arc "
               "welding and adhesive bonding in that order."),
    dict(key=(4, 'b', 'i'),
         checked=_ck(4, '(b)(i)', 'Answer any three of the following in relation to gas welding:'),
         why='One of "Answer any three of the following": scheme p12 names the gases in one '
             'line, "Award 3 @ 4 Marks".',
         topic='eng-2-10',
         lifted=[S(12, 128, 377, 455, 393)], marks=[4], total=4,
         question_figure='engineering-2010-OL-paper-q4b-crop', notes=_B4),
    dict(key=(4, 'b', 'ii'),
         why='One of "Answer any three of the following": scheme p12 answers in one '
             'paragraph.',
         topic='eng-2-10',
         question_lift=P(4, 115, 181, 350, 198),
         lifted=[S(12, 128, 404, 456, 447)], marks=[4], total=4,
         question_figure='engineering-2010-OL-paper-q4b-crop', notes=_B4),
    dict(key=(4, 'b', 'iii'),
         checked=_ck(4, '(b)(iii)', 'Answer any three of the following in relation to gas welding:'),
         why='One of "Answer any three of the following": scheme p12 names the flame.',
         topic='eng-2-10',
         lifted=[S(12, 128, 457, 300, 473)], marks=[4], total=4,
         question_figure='engineering-2010-OL-paper-q4b-crop', notes=_B4),
    dict(key=(4, 'b', 'iv'),
         why='One of "Answer any three of the following": scheme p12 answers in one '
             'sentence.',
         topic='eng-3-1',
         lifted=[S(12, 128, 484, 490, 514)], marks=[4], total=4,
         question_figure='engineering-2010-OL-paper-q4b-crop', notes=_B4),
    dict(key=(4, 'c', None),
         why='Scheme p12 numbers three steps, "Steps Award 3 @ 4 Marks".',
         topic='eng-2-10',
         lifted=[S(12, 128, 551, 465, 568), S(12, 128, 578, 465, 608), S(12, 128, 619, 505, 648)],
         marks=[4, 4, 4], total=12,
         notes="The scheme prints 'Three steps: Steps Award 3 @ 4 Marks'."),
    dict(key=(4, 'd', None),
         replaces=NEW + 'cut the one-paragraph answer into two alternatives',
         why='Scheme p12 answers in one paragraph, "Reason Award 5 Marks".',
         topic='eng-3-1',
         lifted=[S(12, 110, 672, 455, 715)], marks=[5], total=5,
         notes="The scheme prints 'Reason Award 5 Marks'."),
    # ---- Question 5 --------------------------------------------------------
    dict(key=(5, 'a', 'i'),
         checked=_ck(4, '(a)(i)', 'For any one of the plastic components shown below:'),
         why='"For any one of the plastic components shown": scheme p13 names the process '
             'for each, "Any one", "Name Award 4 Marks".',
         topic='eng-1-9', stem=False,
         question_lift=P(4, 95, 422, 360, 439, more=[(115, 445, 385, 462)]),
         lifted=[[S(13, 125, 160, 360, 176), S(13, 125, 176, 360, 189.5),
                  S(13, 125, 189.5, 360, 205)]],
         row_kind='anyN', group=(1, 4), marks=[4], tariff='fixed', total=4,
         question_figure='engineering-2010-OL-paper-q5a-crop',
         notes="The scheme prints 'Any one: Name Award 4 Marks'."),
    dict(key=(5, 'a', 'ii'),
         why='Scheme p13 describes each process under its name over a drawing of it, shown '
             'with the answer; "Description of any one", "Award 14 Marks".',
         topic='eng-1-9', stem=False,
         question_lift=P(4, 95, 422, 360, 439, more=[(115, 466, 510, 483)]),
         lifted=[[S(13, 120, 241, 450, 310), S(13, 120, 375, 495, 471), S(13, 128, 563, 440, 646)]],
         row_kind='anyN', group=(1, 14), marks=[14], tariff='fixed', total=14,
         question_figure='engineering-2010-OL-paper-q5a-crop',
         figure='engineering-2010-OL-scheme-q5a-sol',
         notes="The scheme prints 'Description of any one: Good description Award 14 Marks'."),
    dict(key=(5, 'b', None),
         why='Scheme p14 bullets two precautions, "Precautions Award 2 @ 3 Marks".',
         topic='eng-3-1',
         lifted=[S(14, 135, 159, 450, 188), S(14, 135, 200, 450, 216)], marks=[3, 3], total=6,
         notes="The scheme prints 'Precautions Award 2 @ 3 Marks'."),
    dict(key=(5, 'c', None),
         why='A lead-in over four terms set as romans, "any three"; scheme p14 explains each '
             'under its name, "Terms Award 3 @ 5 Marks".',
         topic='eng-1-9',
         lifted=[[S(14, 128, 294, 455, 350), S(14, 128, 361, 465, 403), S(14, 128, 415, 455, 444),
                  S(14, 128, 455, 455, 511)]],
         row_kind='anyN', group=(3, 5), marks=[15], tariff='fixed', total=15,
         notes="The scheme prints 'Any three: Terms Award 3 @ 5 Marks'."),
    dict(key=(5, 'd', None),
         why='Scheme p14 names a material after each roman, "Material Award 2 @ 3 Marks".',
         topic='eng-1-9',
         lifted=[S(14, 150, 562, 400, 578), S(14, 150, 576, 400, 591)], marks=[3, 3], total=6,
         notes="The scheme prints 'Material Award 2 @ 3 Marks', for (i) and (ii) in that "
               "order."),
    # ---- Question 6 --------------------------------------------------------
    dict(key=(6, 'a', None),
         why='The four parts are pictured and captioned (i)-(iv); scheme p15 names each '
             'after its roman, "Any three", "Award 3 @ 6 Marks". The reader joins the '
             'captions to the question, so it is lifted from the page.',
         topic='eng-2-11',
         question_lift=P(5, 95, 87, 310, 104),
         lifted=[[S(15, 120, 174, 300, 189), S(15, 120, 189, 300, 202), S(15, 120, 202, 300, 215.5),
                  S(15, 120, 215.5, 300, 230)]],
         row_kind='anyN', group=(3, 6), marks=[18], tariff='fixed', total=18,
         question_figure='engineering-2010-OL-paper-q6a-crop',
         notes="The scheme prints 'Any three lathe parts: Operations Award 3 @ 6 Marks'."),
    dict(key=(6, 'b', None),
         why='A lead-in over four terms set as romans, "any three"; scheme p15 explains each '
             'under its name, "Award 3 @ 5 Marks".',
         topic='eng-2-11',
         lifted=[[S(15, 112, 308, 440, 364), S(15, 110, 388, 500, 444), S(15, 110, 469, 485, 498),
                  S(15, 108, 523, 510, 579)]],
         row_kind='anyN', group=(3, 5), marks=[15], tariff='fixed', total=15,
         notes="The scheme prints 'Any three: Operations Award 3 @ 5 Marks'."),
    dict(key=(6, 'c', None),
         replaces=NEW + 'ran both branches into one ordered split, priced from the grid',
         why='Paper p5 sets two alternative (c)s either side of an OR. Scheme p16 describes '
             'taper turning by the compound slide beside a drawing, shown with the answer, '
             'then a safety precaution, "Award 8 Marks" and "Award 4 Marks"; and, for the OR, '
             'bullets six advantages of CNC, "Award 3 @ 4 Marks". Each is priced at 12: one '
             'card, each branch a route.',
         topic='eng-2-11', stem=False,
         question_lift=P(5, 90, 390, 530, 421, more=[(275, 459, 305, 479), (90, 503, 470, 534)]),
         lifted=[S(16, 105, 144, 410, 189), S(16, 105, 426, 510, 456),
                 [S(16, 112, 550, 460, 566), S(16, 112, 566, 460, 580), S(16, 112, 580, 460, 594),
                  S(16, 112, 594, 460, 609), S(16, 112, 609, 460, 623), S(16, 112, 623, 460, 637)]],
         row_kind='anyN', group=[None, None, (3, 4)], marks=[8, 4, 12],
         routes=['a', 'a', 'b'], total=12,
         question_figure='engineering-2010-OL-paper-q6cor-crop',
         figure='engineering-2010-OL-scheme-q6c-sol',
         notes="The scheme prints 'Good description Award 8 Marks' and 'Safety precaution "
               "Award 4 Marks' for taper turning, and 'Advantages Award 3 @ 4 Marks' for the "
               "OR. " + _OR6),
    # ---- Question 7 --------------------------------------------------------
    dict(key=(7, 'a', None),
         why='Scheme p17 bullets two advantages, "Advantages Award 2 @ 5 Marks".',
         topic='eng-3-12',
         lifted=[S(17, 112, 174, 455, 190), S(17, 112, 189, 455, 204)], marks=[5, 5], total=10,
         notes="The scheme prints 'Advantages Award 2 @ 5 Marks'."),
    dict(key=(7, 'b', None),
         why='The hole is drawn beside (b) with its dimension; scheme p17 states each value '
             'after its roman, "Calculations Award 4 @ 5 Marks". The question is lifted with '
             'its romans, which the reader files as parts of their own.',
         topic='eng-3-12', stem=False,
         question_lift=P(6, 95, 160, 430, 177, more=[(95, 202, 150, 219)],
                         items=[(170, 202, 360, 219), (170, 222, 360, 239),
                                (170, 243, 360, 260), (170, 264, 320, 281)]),
         lifted=[S(17, 138, 270, 400, 287), S(17, 138, 296, 400, 314), S(17, 138, 323, 400, 339),
                 S(17, 138, 350, 400, 366)],
         marks=[5, 5, 5, 5], total=20,
         question_figure='engineering-2010-OL-paper-q7b-crop',
         notes="The scheme prints 'Calculations Award 4 @ 5 Marks'."),
    dict(key=(7, 'c', None),
         why='Paper p6 sets two alternative (c)s either side of an OR: four tools pictured '
             'and captioned (i)-(iv), or a circuit with components A-D; scheme p17 names '
             'each tool with a use, or each component after its letter, both "Award 3 @ 5 '
             'Marks": one card, a route per branch.',
         topic='eng-3-12', stem=False,
         question_lift=P(6, 95, 335, 420, 352, more=[(280, 567, 310, 587), (95, 638, 335, 670)]),
         lifted=[[S(17, 138, 430, 455, 460), S(17, 138, 457, 455, 473), S(17, 138, 470, 455, 486),
                  S(17, 138, 484, 455, 513)],
                 [S(17, 138, 593, 455, 609.5), S(17, 138, 609.5, 455, 622.5),
                  S(17, 138, 622.5, 455, 635.5), S(17, 138, 635.5, 455, 650)]],
         row_kind='anyN', group=[(3, 5), (3, 5)], marks=[15, 15], routes=['a', 'b'], total=15,
         question_figure='engineering-2010-OL-paper-q7c-crop',
         notes="The scheme prints 'Illustrations Award 3 @ 5 Marks' and, for the OR, "
               "'Symbols Award 3 @ 5 Marks'. " + _OR7),
]

TOPICS = {}

ATLAS = {
    'eng-2010-ol-q4-b-iv': dict(
        topics=['Welding & Soldering'],
        note='A safety precaution for gas welding, one of Q4(b)\'s gas welding parts, under '
             'Q4\'s Welding & Soldering; the card\'s syllabus heading is Safety.'),
    'eng-2010-ol-q4-d': dict(
        topics=['Welding & Soldering'],
        note='Ventilation when bonding with adhesives, a joining process, under Q4\'s Welding '
             '& Soldering; the card\'s syllabus heading is Safety.'),
}
