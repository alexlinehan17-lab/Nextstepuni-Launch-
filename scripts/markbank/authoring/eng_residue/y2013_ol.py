"""2013 Ordinary Level: every part, from the page.

Paper and scheme as the PDFs number their pages. As in 2014-2019, the automatic
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

Y, L = 2013, 'ol'


def S(page, *rect):
    return lift(Y, L, 'scheme', page, rect)


def P(page, *rect, more=(), items=()):
    return lift(Y, L, 'paper', page, rect, more=more, items=items)


_C6A = (95, 348, 375, 367)            # paper p5: the turning (c)
_ORW6 = (277, 589, 302, 609)          # paper p5: the OR between the two (c)s
_C6B = (95, 621, 560, 654)            # paper p5: the CNC (c)

_SB = ("Section B is 'Any three parts @ 12 + 12 + 11 Marks': the card carries the 12 a part "
       "earns answered first or second; answered third it earns 11.")
_OR3 = ('The paper sets two (d)s either side of an OR, the metal terms and pneumatics in '
        'manufacturing; the scheme prices both "Award 2 @ 4 Marks", so they are one card, each '
        'branch a route.')
_OR6 = ('The paper sets two (c)s either side of an OR: the turning (c), whose (i)-(iii) are '
        'carded apart, and the CNC (c), "Any three" of four labelled parts, carded at the '
        'letter.')
_OR7 = ('The paper sets two (c)s either side of an OR, the instruments and the electronic '
        'components, each "Any three" of four photographs captioned (i)-(iv); the scheme '
        'prices both "Award 3 @ 5 Marks", so they are one card, each branch a route.')

CROPS = {
    # ---- paper ------------------------------------------------------------
    'engineering-2013-OL-paper-q1a-crop': dict(
        doc='paper', page=2, rect=(493, 69, 540, 186), image=True, ref='2013 OL Q1(a)'),
    'engineering-2013-OL-paper-q1d-crop': dict(
        doc='paper', page=2, rect=(415, 185, 475, 229), image=True, ref='2013 OL Q1(d)'),
    'engineering-2013-OL-paper-q1h-crop': dict(
        doc='paper', page=2, rect=(442, 312, 538, 384), image=True, ref='2013 OL Q1(h)'),
    # The three machines pictured with their captions.
    'engineering-2013-OL-paper-q1i-crop': dict(
        doc='paper', page=2, rect=(55, 470, 562, 580), ref='2013 OL Q1(i)'),
    'engineering-2013-OL-paper-q1m-crop': dict(
        doc='paper', page=2, rect=(442, 752, 502, 815), image=True, ref='2013 OL Q1(m)'),
    # The buggy with its parts labelled A-D; the end of (c)'s own line, which
    # runs into the box, is whited out.
    'engineering-2013-OL-paper-q2c-crop': dict(
        doc='paper', page=3, rect=(190, 238, 450, 392), mask=[(190, 232, 226, 248)],
        ref='2013 OL Q2(c)', letters=('A', 'B', 'C', 'D')),
    'engineering-2013-OL-paper-q3b-crop': dict(
        doc='paper', page=3, rect=(115, 571, 445, 598), image=True, ref='2013 OL Q3(b)'),
    # The three flames drawn and captioned (i)-(iii).
    'engineering-2013-OL-paper-q4b-crop': dict(
        doc='paper', page=4, rect=(55, 136, 540, 190), ref='2013 OL Q4(b)'),
    'engineering-2013-OL-paper-q4cii-crop': dict(
        doc='paper', page=4, rect=(497, 225, 551, 274), image=True, ref='2013 OL Q4(c)(ii)'),
    'engineering-2013-OL-paper-q4d-crop': dict(
        doc='paper', page=4, rect=(472, 299, 541, 415), image=True, ref='2013 OL Q4(d)'),
    # The two processes drawn with A and B under them.
    'engineering-2013-OL-paper-q5a-crop': dict(
        doc='paper', page=4, rect=(110, 500, 470, 598), ref='2013 OL Q5(a)',
        letters=('A', 'B')),
    # The four turning operations drawn and captioned (i)-(iv).
    'engineering-2013-OL-paper-q6a-crop': dict(
        doc='paper', page=5, rect=(110, 82, 505, 157), ref='2013 OL Q6(a)'),
    # The four lathe parts photographed and captioned (i)-(iv).
    'engineering-2013-OL-paper-q6b-crop': dict(
        doc='paper', page=5, rect=(75, 212, 535, 320), ref='2013 OL Q6(b)'),
    # The turning set-up with part A.
    'engineering-2013-OL-paper-q6c-crop': dict(
        doc='paper', page=5, rect=(205, 366, 392, 502), ref='2013 OL Q6(c)', letters=('A',)),
    # The CNC lathe with its parts labelled A-D.
    'engineering-2013-OL-paper-q6cor-crop': dict(
        doc='paper', page=5, rect=(140, 650, 425, 795), ref='2013 OL Q6(c)',
        letters=('A', 'B', 'C', 'D')),
    'engineering-2013-OL-paper-q7b-crop': dict(
        doc='paper', page=6, rect=(355, 155, 575, 262), ref='2013 OL Q7(b)'),
    # Both (c)s' photographs, each row captioned (i)-(iv).
    'engineering-2013-OL-paper-q7c-crop': dict(
        doc='paper', parts=[(6, (55, 355, 565, 505)), (6, (95, 636, 505, 785))],
        ref='2013 OL Q7(c)'),
    # ---- scheme: the drawings the answers are given with -------------------
    'engineering-2013-OL-scheme-q2bii-sol': dict(
        doc='scheme', parts=[(9, (65, 115, 210, 298)), (9, (42, 312, 232, 535)),
                             (9, (25, 533, 215, 665))],
        layout='row', solution=True, ref='2013 OL Q2(b)(ii)'),
}

CARDS = [
    # ---- Question 1, Section A ("Any six @ 5 marks each") ------------------
    dict(key=(1, 'a', None),
         why='The pillar drill is photographed beside (a); scheme p5 numbers two '
             'precautions; "3 + 2 Marks".',
         topic='eng-3-1',
         lifted=[S(5, 78, 345, 460, 361), S(5, 80, 359, 460, 375)],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         question_figure='engineering-2013-OL-paper-q1a-crop',
         notes="The scheme prints '3 + 2 Marks'."),
    dict(key=(1, 'b', None),
         why='Scheme p5 names two metals on one line, each lifted by its own word '
             'rectangle; "3 + 2 Marks".',
         topic='eng-1-5',
         lifted=[S(5, 58, 387, 110, 403), S(5, 109, 387, 142, 403)],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         notes="The scheme prints '3 + 2 Marks'."),
    dict(key=(1, 'c', None),
         why='Scheme p5 numbers two advantages on one line, each lifted by its own word '
             'rectangle; "3 + 2 Marks".',
         topic='eng-2-11',
         lifted=[S(5, 75, 410, 148, 430), S(5, 168, 410, 302, 430)],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         notes="The scheme prints '3 + 2 Marks'."),
    dict(key=(1, 'd', None),
         why='The motor is photographed beside (d); scheme p5 names it and gives its use in '
             'one sentence, each lifted by its own word rectangle; "3 + 2 Marks".',
         topic='eng-2-16',
         lifted=[S(5, 60, 452, 126, 472), S(5, 126, 452, 420, 472)],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         question_figure='engineering-2013-OL-paper-q1d-crop',
         notes="The scheme prints '3 + 2 Marks'."),
    dict(key=(1, 'e', None),
         why='Scheme p5 gives two reasons in one sentence, each lifted by its own word '
             'rectangle; "3 + 2 Marks".',
         topic='eng-3-14',
         lifted=[S(5, 58, 492, 305, 512), join(S(5, 305, 492, 500, 512), S(5, 60, 507, 120, 527))],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         notes="The scheme prints '3 + 2 Marks'."),
    dict(key=(1, 'f', None),
         why='Scheme p5 explains each hole after its roman; "3 + 2 Marks".',
         topic='eng-2-11',
         lifted=[join(S(5, 75, 548, 440, 567), S(5, 75, 562, 250, 582)),
                 S(5, 78, 576, 505, 611)],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         notes="The scheme prints '3 + 2 Marks'."),
    dict(key=(1, 'g', None),
         why='Scheme p5 names each thread after its roman; "3 + 2 Marks".',
         topic='eng-2-11',
         lifted=[S(5, 75, 631, 300, 651), S(5, 80, 645, 345, 665)],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         notes="The scheme prints '3 + 2 Marks'."),
    dict(key=(1, 'h', None),
         why='The circuit boards are photographed beside (h); scheme p5 answers in one '
             'sentence, "5 Marks". The reader joins the Section B heading to (h), so the '
             'question is lifted from the page.',
         topic='eng-2-16',
         question_lift=P(2, 60, 313, 395, 333),
         lifted=[S(5, 60, 686, 330, 706)], marks=[5], total=5,
         question_figure='engineering-2013-OL-paper-q1h-crop',
         notes="The scheme prints '5 Marks'."),
    # ---- Question 1, Section B ("Any three parts @ 12 + 12 + 11 Marks") ----
    dict(key=(1, 'i', None),
         why='The three machines are pictured and captioned under (i); scheme p6 describes '
             'each under its name; "Any one", "Award 12 (11) Marks". The question is lifted '
             'with each caption on its own line, as the paper sets them under their '
             'pictures.',
         topic='eng-2-15', stem=False,
         question_lift=P(2, 60, 450, 565, 470, items=[(78, 560, 142, 580),
                                                      (212, 560, 360, 580),
                                                      (406, 560, 558, 580)]),
         lifted=[[S(6, 75, 128, 465, 258), S(6, 75, 321, 465, 437), S(6, 75, 486, 435, 575)]],
         row_kind='anyN', group=(1, 12), marks=[12], tariff='fixed', total=12,
         question_figure='engineering-2013-OL-paper-q1i-crop',
         notes="The scheme prints 'Any one: Good clear description Award 12 (11) Marks'. "
               + _SB),
    dict(key=(1, 'j', None),
         why='Scheme pp6-7 explain each term under its name, "Any two", "Award 6 + 6(5)".',
         topic='eng-3-14', stem=False,
         lifted=[[S(6, 75, 640, 528, 729), S(7, 75, 68, 490, 157), S(7, 75, 178, 525, 267),
                  S(7, 75, 289, 520, 391)]],
         row_kind='anyN', group=(2, 6), marks=[12], tariff='fixed', total=12,
         notes="The scheme prints 'Any two: Good clear description Award 6 + 6(5)'. " + _SB),
    dict(key=(1, 'k', None),
         why='Scheme p7 defines the term and gives examples, each under its heading; '
             '"Definition Award 6", "Example Award 6(5) Marks".',
         topic='eng-3-8', stem=False,
         lifted=[S(7, 72, 429, 445, 477), S(7, 72, 471, 445, 504)],
         marks=[6, 6], total=12,
         notes="The scheme prints 'Definition Award 6' and 'Example Award 6(5) Marks'. " + _SB),
    dict(key=(1, 'l', None),
         why='Scheme pp7-8 explain each term under its name, "Any two", "Award 6 + 6 (5) '
             'Marks".',
         topic='eng-3-14', stem=False,
         lifted=[[S(7, 75, 556, 445, 631), S(7, 75, 666, 470, 769), S(8, 75, 68, 512, 129),
                  S(8, 75, 137, 465, 198)]],
         row_kind='anyN', group=(2, 6), marks=[12], tariff='fixed', total=12,
         notes="The scheme prints 'Any two: Good description Award 6 + 6 (5) Marks'. " + _SB),
    dict(key=(1, 'm', None),
         why='The mechanism is photographed beside (m); scheme p8 names it and gives its '
             'application under their headings, "Name Award 6", "Application Award 6(5)".',
         topic='eng-2-15', stem=False,
         lifted=[S(8, 70, 279, 160, 313), S(8, 70, 321, 470, 368)],
         marks=[6, 6], total=12,
         question_figure='engineering-2013-OL-paper-q1m-crop',
         notes="The scheme prints 'Name Award 6' and 'Application Award 6(5)'. " + _SB),
    # ---- Question 2 --------------------------------------------------------
    dict(key=(2, 'a', None),
         why='A lead-in over four alloys set as romans, "any three"; scheme p8 names a '
             'component after each alloy, "Name Award 3 @ 4 Marks".',
         topic='eng-1-5',
         lifted=[[S(8, 110, 544, 330, 566), S(8, 110, 558, 330, 580), S(8, 110, 571, 330, 594),
                  S(8, 110, 585, 330, 608)]],
         row_kind='anyN', group=(3, 4), marks=[12], tariff='fixed', total=12,
         notes="The scheme prints 'Name Award 3 @ 4 Marks'."),
    dict(key=(2, 'b', 'i'),
         why='"Any two of the furnaces below": scheme p8 names each furnace\'s metal after '
             'it, "Award 2 @ 4 Marks".',
         topic='eng-1-4',
         lifted=[[S(8, 110, 654, 330, 674), S(8, 110, 668, 330, 688), S(8, 110, 682, 330, 702)]],
         row_kind='anyN', group=(2, 4), marks=[8], tariff='fixed', total=8,
         notes="The scheme prints 'Award 2 @ 4 Marks'."),
    dict(key=(2, 'b', 'ii'),
         why='"Any one description": scheme p9 describes the blast, cupola and electric arc '
             'furnace under their names, each beside a drawing of it, shown with the '
             'answer; "Good clear description", "Award 1 @ 10 Marks".',
         topic='eng-1-4',
         lifted=[[S(9, 260, 120, 515, 267), S(9, 260, 333, 495, 465), S(9, 260, 537, 535, 656)]],
         row_kind='anyN', group=(1, 10), marks=[10], tariff='fixed', total=10,
         figure='engineering-2013-OL-scheme-q2bii-sol',
         notes="The scheme prints 'Good clear description Award 1 @ 10 Marks'."),
    dict(key=(2, 'c', None),
         why='The buggy is photographed with parts labelled A-D; scheme p10 names a material '
             'for each after its letter, any three, "Name Award 3 @ 3 Marks".',
         topic='eng-3-8',
         lifted=[[S(10, 100, 109, 200, 129), S(10, 100, 123, 200, 143), S(10, 100, 137, 200, 157),
                  S(10, 100, 151, 200, 171)]],
         row_kind='anyN', group=(3, 3), marks=[9], tariff='fixed', total=9,
         labels={'A': S(10, 120, 109, 200, 129), 'B': S(10, 120, 123, 200, 143),
                 'C': S(10, 120, 137, 200, 157), 'D': S(10, 120, 151, 200, 171)},
         question_figure='engineering-2013-OL-paper-q2c-crop',
         notes="The scheme prints 'Name Award 3 @ 3 Marks'."),
    dict(key=(2, 'd', None),
         why='Scheme p10 names two methods after their romans, "Name Award 2 @ 3 Marks".',
         topic='eng-3-7',
         lifted=[S(10, 120, 261, 210, 281), S(10, 120, 275, 200, 295)],
         marks=[3, 3], total=6,
         notes="The scheme prints 'Name Award 2 @ 3 Marks'."),
    # ---- Question 3 --------------------------------------------------------
    dict(key=(3, 'a', 'i'),
         why='Scheme p10 describes hardening and annealing under their headings, "Any two '
             'descriptions", "Difference Award 2 @ 6 marks".',
         topic='eng-2-6',
         lifted=[S(10, 93, 553, 435, 628), S(10, 93, 636, 435, 697)],
         marks=[6, 6], total=12,
         notes="The scheme prints 'Difference Award 2 @ 6 marks', for hardening and "
               "annealing in that order."),
    dict(key=(3, 'a', 'ii'),
         why='Scheme p10 names the process, "Name Award 6 marks".',
         topic='eng-2-6',
         lifted=[S(10, 98, 719, 180, 741)], marks=[6], total=6,
         notes="The scheme prints 'Name Award 6 marks'."),
    dict(key=(3, 'b', 'i'),
         why='The twist drill is photographed under (b); scheme p11 describes the hardening '
             'under its heading, "Hardening Award 8 marks".',
         topic='eng-2-6',
         lifted=[S(11, 93, 82, 435, 143)], marks=[8], total=8,
         question_figure='engineering-2013-OL-paper-q3b-crop',
         notes="The scheme prints 'Hardening Award 8 marks'."),
    dict(key=(3, 'b', 'ii'),
         why='Scheme p11 names the process, "Name Award 5 marks".',
         topic='eng-2-6',
         lifted=[S(11, 95, 164, 160, 186)], marks=[5], total=5,
         question_figure='engineering-2013-OL-paper-q3b-crop',
         notes="The scheme prints 'Name Award 5 marks'."),
    dict(key=(3, 'c', None),
         why='Scheme p11 gives two precautions in a paragraph each, "Good Description Award '
             '2 @ 3 Marks".',
         topic='eng-3-1',
         lifted=[S(11, 93, 231, 440, 265), S(11, 93, 275, 440, 309)],
         marks=[3, 3], total=6,
         notes="The scheme prints 'Good Description Award 2 @ 3 Marks'."),
    dict(key=(3, 'd', None),
         why='Paper p3 sets two alternative (d)s either side of an OR. Scheme p11 explains '
             'each metal term under its name, "Any two terms", "Description Award 2 @ 4 '
             'Marks", and answers the pneumatics (i) and (ii) in a paragraph each, "Award 2 @ '
             '4 Marks": priced alike, one card with a route per branch.',
         topic='eng-3-8', stem=False,
         question_lift=P(3, 95, 684, 300, 703, more=[(97, 706, 470, 725), (270, 730, 297, 750),
                                                     (95, 755, 470, 775), (95, 775, 470, 795)]),
         lifted=[[S(11, 90, 358, 440, 433), S(11, 90, 468, 440, 515), S(11, 88, 551, 440, 598)],
                 S(11, 93, 682, 440, 716), S(11, 95, 723, 450, 771)],
         row_kind='anyN', group=[(2, 4), None, None], marks=[8, 4, 4],
         routes=['a', 'b', 'b'], tariff='fixed', total=8,
         notes="The scheme prints 'Description Award 2 @ 4 Marks' and, for the OR, 'Award 2 @ "
               "4 Marks'. " + _OR3),
    # ---- Question 4 --------------------------------------------------------
    dict(key=(4, 'a', 'i'),
         why='Scheme p12 describes gas welding and manual arc welding under their headings, '
             '"Differences Award 2 @ 4 Marks".',
         topic='eng-2-10',
         lifted=[S(12, 88, 116, 440, 191), S(12, 88, 199, 495, 274)],
         marks=[4, 4], total=8,
         notes="The scheme prints 'Differences Award 2 @ 4 Marks', for gas welding and manual "
               "arc welding in that order."),
    dict(key=(4, 'a', 'ii'),
         why='Scheme p12 sets each process beside its applications, "Applications Award 2 @ '
             '2 Marks".',
         topic='eng-2-10',
         lifted=[S(12, 94, 323, 465, 343), S(12, 94, 337, 375, 357)],
         marks=[2, 2], total=4,
         notes="The scheme prints 'Applications Award 2 @ 2 Marks'."),
    dict(key=(4, 'b', None),
         why='The three flames are drawn and captioned (i)-(iii); scheme p12 names and '
             'describes each after its roman, "Name & Describe Award 3 @ 5 Marks".',
         topic='eng-2-10',
         lifted=[S(12, 75, 391, 420, 410), S(12, 75, 418, 420, 438), S(12, 75, 447, 425, 481)],
         marks=[5, 5, 5], total=15,
         question_figure='engineering-2013-OL-paper-q4b-crop',
         notes="The scheme prints 'Name & Describe Award 3 @ 5 Marks'."),
    dict(key=(4, 'c', 'i'),
         why='One of "Answer any three of the following", "Award 3 @ 4 Marks": scheme p12 '
             'gives two advantages on two lines, the 4 for the part not split between them.',
         topic='eng-2-10',
         lifted=[S(12, 95, 544, 330, 563), S(12, 95, 558, 300, 577)],
         tariff='questionTotal', total=4,
         notes="The scheme prints 'Any three: Award 3 @ 4 Marks' for the three parts "
               "answered."),
    dict(key=(4, 'c', 'ii'),
         why='One of "Answer any three of the following": the nut is photographed beside it; '
             'scheme p12 names it and gives its advantage on two lines, the 4 not split '
             'between them.',
         topic='eng-2-10',
         lifted=[S(12, 95, 571, 150, 590), S(12, 95, 585, 225, 604)],
         tariff='questionTotal', total=4,
         question_figure='engineering-2013-OL-paper-q4cii-crop',
         notes="The scheme prints 'Any three: Award 3 @ 4 Marks' for the three parts "
               "answered."),
    dict(key=(4, 'c', 'iii'),
         why='One of "Answer any three of the following": scheme p12 gives both requirements '
             'on one line, one row for the part\'s 4.',
         topic='eng-2-10',
         lifted=[S(12, 95, 599, 275, 618)], marks=[4], total=4,
         notes="The scheme prints 'Any three: Award 3 @ 4 Marks' for the three parts "
               "answered."),
    dict(key=(4, 'c', 'iv'),
         why='One of "Answer any three of the following": scheme p12 answers in one line.',
         topic='eng-2-10',
         lifted=[S(12, 95, 613, 370, 632)], marks=[4], total=4,
         notes="The scheme prints 'Any three: Award 3 @ 4 Marks' for the three parts "
               "answered."),
    dict(key=(4, 'd', None),
         why='The equipment is photographed beside (d); scheme p12 gives two precautions, '
             'one a line, "Safety Award 2 @ 3 Marks".',
         topic='eng-3-1',
         lifted=[S(12, 75, 693, 440, 712), S(12, 75, 710, 220, 729)],
         marks=[3, 3], total=6,
         question_figure='engineering-2013-OL-paper-q4d-crop',
         notes="The scheme prints 'Safety Award 2 @ 3 Marks'."),
    # ---- Question 5 --------------------------------------------------------
    dict(key=(5, 'a', 'i'),
         why='The two processes are drawn at A and B; scheme p13 names each after its '
             'letter, "Name Award 2 @ 3 Marks".',
         topic='eng-1-9',
         lifted=[S(13, 84, 125, 200, 145), S(13, 84, 139, 200, 159)],
         marks=[3, 3], total=6,
         labels={'A': S(13, 110, 125, 200, 145), 'B': S(13, 110, 139, 200, 159)},
         question_figure='engineering-2013-OL-paper-q5a-crop',
         notes="The scheme prints 'Name Award 2 @ 3 Marks'."),
    dict(key=(5, 'a', 'ii'),
         why='"Any one process": scheme p13 describes each process under its name and ends '
             'each with the components it makes, "Process Award 9 Marks", "Component Award '
             '3 Marks". The description and the component sentence are each lifted by their '
             'own rectangles, whichever process.',
         topic='eng-1-9',
         lifted=[[S(13, 75, 208, 450, 311), S(13, 75, 346, 475, 435)],
                 [S(13, 75, 319, 410, 338), S(13, 75, 443, 315, 463)]],
         marks=[9, 3], total=12,
         question_figure='engineering-2013-OL-paper-q5a-crop',
         notes="The scheme prints 'Process Award 9 Marks' and 'Component Award 3 Marks', for "
               "the process chosen."),
    dict(key=(5, 'b', None),
         why='A lead-in over four terms set as romans, "any three"; scheme pp13-14 explain '
             'each under its name, "Explanation Award 3 @ 5 Marks".',
         topic='eng-1-9',
         lifted=[[S(13, 95, 498, 440, 559), S(13, 95, 567, 425, 683), S(13, 95, 705, 435, 766),
                  S(14, 95, 68, 445, 115)]],
         row_kind='anyN', group=(3, 5), marks=[15], tariff='fixed', total=15,
         notes="The scheme prints 'Any three: Explanation Award 3 @ 5 Marks'."),
    dict(key=(5, 'c', None),
         why='Scheme p14 names a plastic after each item, "Name Award 2 @ 3 Marks". One card '
             'at the letter, a row an item.',
         topic='eng-1-9',
         lifted=[S(14, 75, 164, 235, 184), S(14, 75, 178, 235, 198)],
         marks=[3, 3], total=6,
         notes="The scheme prints 'Name Award 2 @ 3 Marks'."),
    dict(key=(5, 'd', None),
         why='Scheme p14 bullets two precautions, "Safety precautions Award 2 @ 3 Marks".',
         topic='eng-3-1',
         lifted=[S(14, 100, 234, 445, 252), S(14, 100, 247, 445, 266)],
         marks=[3, 3], total=6,
         notes="The scheme prints 'Safety precautions Award 2 @ 3 Marks'."),
    # ---- Question 6 --------------------------------------------------------
    dict(key=(6, 'a', None),
         why='The four operations are drawn and captioned (i)-(iv); scheme p14 names each '
             'after its roman, any three, "Name Award 3 @ 4 Marks".',
         topic='eng-2-11',
         lifted=[[S(14, 72, 429, 130, 447), S(14, 72, 456, 140, 475), S(14, 72, 484, 152, 503),
                  S(14, 72, 512, 137, 531)]],
         row_kind='anyN', group=(3, 4), marks=[12], tariff='fixed', total=12,
         question_figure='engineering-2013-OL-paper-q6a-crop',
         notes="The scheme prints 'Any three operations: Name Award 3 @ 4 Marks'."),
    dict(key=(6, 'b', None),
         why='The four parts are photographed and captioned (i)-(iv); scheme p14 names each '
             'after its roman and gives its use on the next line, any three, "Name Award 3 @ '
             '4 Marks", "Use Award 3 @ 2 Marks", so a name is claimed without its use; each '
             'use is shown with the part it is for.',
         topic='eng-2-11', stem=False,
         lifted=[[S(14, 72, 578, 240, 597), S(14, 72, 636, 145, 656), S(14, 72, 677, 145, 697),
                  S(14, 72, 719, 165, 739)],
                 [S(14, 90, 592, 300, 612), S(14, 90, 650, 350, 670), S(14, 90, 691, 400, 711),
                  S(14, 90, 733, 395, 753)]],
         row_kind='anyN', group=[(3, 4), (3, 2)], marks=[12, 6], tariff='fixed', total=18,
         question_figure='engineering-2013-OL-paper-q6b-crop',
         notes="The scheme prints 'Any three lathe parts: Name Award 3 @ 4 Marks, Use Award 3 "
               "@ 2 Marks'."),
    dict(key=(6, 'c', 'i'),
         why='The turning branch\'s (i), lifted with its cue; scheme p15 names the process, '
             '"Name & description Award 3 @ 5 Marks".',
         topic='eng-2-11', stem=False,
         question_lift=P(5, *_C6A, more=[(118, 511, 250, 530)]),
         lifted=[S(15, 130, 109, 205, 129)], marks=[5], total=5,
         question_figure='engineering-2013-OL-paper-q6c-crop',
         notes="The scheme prints 'Name & description Award 3 @ 5 Marks'. " + _OR6),
    dict(key=(6, 'c', 'ii'),
         why='The turning branch\'s (ii): scheme p15 names part A, "Award 3 @ 5 Marks".',
         topic='eng-2-11', stem=False,
         question_lift=P(5, *_C6A, more=[(118, 532, 320, 551)]),
         lifted=[S(15, 135, 123, 250, 143)], marks=[5], total=5,
         labels={'A': S(15, 135, 123, 250, 143)},
         question_figure='engineering-2013-OL-paper-q6c-crop',
         notes="The scheme prints 'Name & description Award 3 @ 5 Marks'. " + _OR6),
    dict(key=(6, 'c', 'iii'),
         why='The turning branch\'s (iii): scheme p15 gives one precaution, "Award 3 @ 5 '
             'Marks".',
         topic='eng-3-1', stem=False,
         question_lift=P(5, *_C6A, more=[(118, 552, 535, 572)]),
         lifted=[S(15, 93, 151, 350, 171)], marks=[5], total=5,
         question_figure='engineering-2013-OL-paper-q6c-crop',
         notes="The scheme prints 'Name & description Award 3 @ 5 Marks'. " + _OR6),
    dict(key=(6, 'c', None),
         why='The OR branch: "Name any three of the parts labelled A, B, C and D" on the CNC '
             'lathe drawn beside it; scheme p15 names each after its letter, "Award 3 @ 5 '
             'Marks".',
         topic='eng-2-11', stem=False,
         question_lift=P(5, *_C6B),
         lifted=[[S(15, 75, 235, 170, 254), S(15, 75, 248, 170, 268), S(15, 75, 262, 170, 282),
                  S(15, 75, 277, 170, 297)]],
         row_kind='anyN', group=(3, 5), marks=[15], tariff='fixed', total=15,
         labels={'A': S(15, 95, 235, 170, 254), 'B': S(15, 95, 248, 170, 268),
                 'C': S(15, 95, 262, 170, 282), 'D': S(15, 95, 277, 170, 297)},
         question_figure='engineering-2013-OL-paper-q6cor-crop',
         notes="The scheme prints 'Any three: Award 3 @ 5 Marks'. " + _OR6),
    # ---- Question 7 --------------------------------------------------------
    dict(key=(7, 'a', None),
         why='"Name and describe any two types of fit"; scheme p15 describes three under '
             'their names, "Name & description Award 2 @ 5 Marks".',
         topic='eng-3-12',
         lifted=[[S(15, 90, 486, 445, 534), S(15, 93, 542, 440, 589), S(15, 96, 597, 445, 644)]],
         row_kind='anyN', group=(2, 5), marks=[10], tariff='fixed', total=10,
         notes="The scheme prints 'Any two: Name & description Award 2 @ 5 Marks'."),
    dict(key=(7, 'b', None),
         why='The shaft is drawn with its dimension beside (b); scheme p15 states each value '
             'after its roman, "Calculations Award 4 @ 5 Marks". The question is lifted with '
             'its romans, which the reader files as parts of their own.',
         topic='eng-3-12', stem=False,
         question_lift=P(6, 95, 141, 395, 160, more=[(97, 164, 345, 183), (168, 184, 345, 204),
                                                     (168, 205, 345, 224),
                                                     (168, 226, 345, 245)]),
         lifted=[S(15, 75, 679, 330, 699), S(15, 75, 693, 330, 713), S(15, 75, 707, 330, 727),
                 S(15, 75, 721, 330, 741)],
         marks=[5, 5, 5, 5], total=20,
         question_figure='engineering-2013-OL-paper-q7b-crop',
         notes="The scheme prints 'Calculations Award 4 @ 5 Marks'."),
    dict(key=(7, 'c', None),
         why='Paper p6 sets two alternative (c)s either side of an OR, each "any three" of '
             'four photographs captioned (i)-(iv) with no words. Scheme p16 names each '
             'instrument with an application, and each component with its use, after its '
             'roman, both "Award 3 @ 5 Marks": one card, each branch a route.',
         topic='eng-3-12', stem=False,
         question_lift=P(6, 95, 309, 560, 328, more=[(280, 548, 310, 570), (95, 605, 520, 638)]),
         lifted=[[S(16, 70, 95, 340, 115), S(16, 70, 109, 330, 129), S(16, 70, 123, 420, 143),
                  S(16, 70, 137, 445, 157)],
                 [S(16, 75, 293, 445, 313), S(16, 75, 307, 365, 327), S(16, 75, 321, 470, 341),
                  S(16, 75, 334, 395, 354)]],
         row_kind='anyN', group=[(3, 5), (3, 5)], marks=[15, 15], routes=['a', 'b'],
         tariff='fixed', total=15,
         question_figure='engineering-2013-OL-paper-q7c-crop',
         notes="The scheme prints 'Name & application Award 3 @ 5 Marks' and, for the OR, "
               "'Name & use Award 3 @ 5 Marks'. " + _OR7),
]

TOPICS = {}

ATLAS = {
    'eng-2013-ol-q3-d': dict(
        topics=['Heat Treatment', 'Pneumatics'],
        note='The two branches of the OR: work hardening, brittleness and tempering, under Q3\'s '
             'Heat Treatment, or pneumatics in manufacturing; the card\'s syllabus heading is '
             'Materials testing.'),
    'eng-2013-ol-q6-c-iii': dict(
        topics=['CNC & Centre Lathe'],
        note='A safety precaution when taper turning on the centre lathe; the card\'s syllabus '
             'heading is Health and safety.'),
}
