"""2015 Higher Level: the parts eng_all refuses or gets wrong, from the page.

Paper and scheme as the PDFs number their pages. The marks grid is on scheme
p4: Question 1 is Section A, "Any ten @ 5 marks each", and Section B, "Answer
all of the following", (n) to (r); Questions 2-8 are 50 marks each. The scheme
prints a part's marks under its answer ("(Any two) 3 + 2", "(Any three) 6 + 6 +
6"). This sitting had no cards before the lane: every card here is new, and a
`replaces=` names the automatic card it rebuilds before it ever shipped.
"""
from eng_lift import join, lift

Y, L = 2015, 'hl'
NEW = 'never shipped: the automatic card '


def S(page, *rect):
    return lift(Y, L, 'scheme', page, rect)


def P(page, *rect, more=(), items=()):
    return lift(Y, L, 'paper', page, rect, more=more, items=items)


# Paper stems the romans are lifted with.
_O1 = (116, 210, 470, 229)            # p4: Q1(o), the fuel injection system
_P1 = (116, 471, 400, 504)            # p4: Q1(p), the fuel injector
_B2 = (116, 250, 500, 269)            # p5: Q2(b), the stress-strain graph
_B3 = (116, 246, 460, 266)            # p6: Q3(b), the iron-carbon diagram
_B4 = (116, 275, 520, 310)            # p7: Q4(b), the table
_GRAPH4 = (115, 427, 275, 446)        # "Using the graph paper supplied:"
_C4 = (116, 572, 517, 591)            # p7: Q4(c), the two crystal structures
_C7A = (116, 385, 475, 420)           # p10: Q7(c), the metal chips
_ORW7 = (298, 626, 326, 645)
_C7B = (118, 661, 455, 680)           # the CNC machining (c)
_A8 = (116, 82, 480, 116)             # p11: Q8(a), the volleyball net
_C8A = (115, 457, 350, 522)           # p11: Q8(c), the robot
_ORW8 = (298, 615, 326, 635)
_C8B = (118, 650, 535, 684)           # the relay (c)

_OR5 = ('The paper sets two (c)s either side of an OR: resistance seam and spot welding, '
        'answered at the letter for 16, and the Robocoaster (c), whose (i) and (ii) are '
        'carded apart.')
_OR7 = ('The paper sets two (c)s either side of an OR, the metal chips and CNC machining; '
        'the scheme prices each (i) at 8 and each (ii) at 8, so each roman is one card, '
        'each branch a route.')
_OR8 = ('The paper sets two (c)s either side of an OR, the robot and the relay; the '
        'scheme prices each (i) at 8 and each (ii) at 8, so each roman is one card, each '
        'branch a route.')

CROPS = {
    # ---- paper ------------------------------------------------------------
    # The return-less fuel system with its parts lettered A-E (the automatic
    # crop lost D and E).
    'engineering-2015-HL-paper-q1o-crop': dict(
        doc='paper', page=4, rect=(130, 274, 480, 456), ref='2015 HL Q1(o)',
        letters=('A', 'B', 'C', 'D', 'E')),
    # The injector with F, G and H printed beside it (the automatic crop lost
    # all three).
    'engineering-2015-HL-paper-q1p-crop': dict(
        doc='paper', page=4, rect=(472, 440, 575, 622), ref='2015 HL Q1(p)',
        letters=('F', 'G', 'H')),
    # The stress-strain graph with both axes and all three specimens.
    'engineering-2015-HL-paper-q2b-crop': dict(
        doc='paper', page=5, rect=(140, 292, 445, 472), ref='2015 HL Q2(b)',
        letters=('A', 'B', 'C')),
    # The iron-carbon diagram with both axes.
    'engineering-2015-HL-paper-q3b-crop': dict(
        doc='paper', page=6, rect=(128, 278, 485, 474), ref='2015 HL Q3(b)',
        letters=('A', 'B', 'C', 'D', 'X', 'Y')),
    'engineering-2015-HL-paper-q4b-crop': dict(
        doc='paper', page=7, rect=(70, 326, 576, 401), ref='2015 HL Q4(b)'),
    # The three polymer structures with their captions.
    'engineering-2015-HL-paper-q6c-crop': dict(
        doc='paper', page=9, rect=(130, 545, 520, 636), ref='2015 HL Q6(c)'),
    # Each (c) shows its own picture: the chips A-C, then the chess pieces.
    'engineering-2015-HL-paper-q7c-crop': dict(
        doc='paper', parts=[(10, (113, 425, 548, 530)), (10, (398, 680, 548, 782))],
        ref='2015 HL Q7(c)'),
    # The net and its worm gear; the end of (a)(ii)'s "method" is whited out.
    'engineering-2015-HL-paper-q8a-crop': dict(
        doc='paper', page=11, rect=(395, 100, 575, 305), mask=[(394, 188, 414, 224)],
        ref='2015 HL Q8(a)'),
    # Each (c) shows its own machine: the robot, then the relay (the robot's
    # box starts at x 387, past the end of (ii)'s "flat" at 385).
    'engineering-2015-HL-paper-q8c-crop': dict(
        doc='paper', parts=[(11, (387, 442, 550, 600)), (11, (408, 670, 520, 780))],
        layout='row', ref='2015 HL Q8(c)'),
    # ---- scheme: the drawings the answers are given with -------------------
    'engineering-2015-HL-scheme-q2aii-sol': dict(
        doc='scheme', page=9, rect=(420, 173, 559, 310), image=True, solution=True,
        ref='2015 HL Q2(a)(ii)'),
    'engineering-2015-HL-scheme-q2cii-sol': dict(
        doc='scheme', page=9, rect=(365, 545, 598, 740), solution=True,
        ref='2015 HL Q2(c)(ii)'),
    'engineering-2015-HL-scheme-q3c-sol': dict(
        doc='scheme', parts=[(10, (340, 515, 592, 742)), (11, (378, 85, 572, 336))],
        solution=True, ref='2015 HL Q3(c)'),
    'engineering-2015-HL-scheme-q4bi-sol': dict(
        doc='scheme', page=12, rect=(60, 310, 505, 602), solution=True,
        ref='2015 HL Q4(b)(i)'),
    'engineering-2015-HL-scheme-q4biii-sol': dict(
        doc='scheme', page=13, rect=(140, 90, 402, 128), solution=True,
        ref='2015 HL Q4(b)(iii)'),
    'engineering-2015-HL-scheme-q5bii-sol': dict(
        doc='scheme', page=14, rect=(420, 590, 585, 752), solution=True,
        ref='2015 HL Q5(b)(ii)'),
    'engineering-2015-HL-scheme-q5c-sol': dict(
        doc='scheme', page=15, rect=(78, 80, 560, 292), solution=True,
        ref='2015 HL Q5(c)'),
    'engineering-2015-HL-scheme-q6aii-sol': dict(
        doc='scheme', page=16, rect=(80, 505, 500, 646), solution=True,
        ref='2015 HL Q6(a)(ii)'),
    'engineering-2015-HL-scheme-q7aii-sol': dict(
        doc='scheme', page=18, rect=(150, 418, 430, 516), solution=True,
        ref='2015 HL Q7(a)(ii)'),
    'engineering-2015-HL-scheme-q7aiv-sol': dict(
        doc='scheme', page=18, rect=(425, 640, 545, 768), solution=True,
        ref='2015 HL Q7(a)(iv)'),
    'engineering-2015-HL-scheme-q7bi-sol': dict(
        doc='scheme', page=19, rect=(355, 205, 580, 400), solution=True,
        ref='2015 HL Q7(b)(i)'),
    'engineering-2015-HL-scheme-q8ai-sol': dict(
        doc='scheme', page=21, rect=(360, 98, 578, 222), solution=True,
        ref='2015 HL Q8(a)(i)'),
    'engineering-2015-HL-scheme-q8aii-sol': dict(
        doc='scheme', page=21, rect=(355, 245, 578, 362), solution=True,
        ref='2015 HL Q8(a)(ii)'),
    'engineering-2015-HL-scheme-q8ci-sol': dict(
        doc='scheme', parts=[(22, (250, 245, 535, 372)), (23, (380, 80, 560, 240))],
        solution=True, ref='2015 HL Q8(c)(i)'),
    'engineering-2015-HL-scheme-q8cii-sol': dict(
        doc='scheme', page=22, rect=(115, 470, 520, 605), solution=True,
        ref='2015 HL Q8(c)(ii)'),
}

FOLDED = {
    'eng-2015-hl-q3-c-iv': 'never shipped: (iv) is one option of "Select any two of the '
                           'following and distinguish between", carried by the Q3(c) card',
    'eng-2015-hl-q8-b-v': 'never shipped: (v) is one option of "Explain any three of the '
                          'following", carried by the Q8(b) card',
}

CARDS = [
    # ---- Question 1, Section A ("Any ten @ 5 marks each") ------------------
    dict(key=(1, 'a', None),
         why='The tablet is photographed beside (a); scheme p5 gives the advantages and '
             'the disadvantages under their headings, over "3 + 2".',
         topic='eng-3-14',
         lifted=[S(5, 70, 246, 540, 281), S(5, 70, 280, 560, 322)],
         marks=[3, 2], total=5,
         question_figure='engineering-2015-HL-paper-q1a-art',
         notes="The scheme prints '3 + 2' under its advantages and disadvantages, in "
               "that order."),
    dict(key=(1, 'b', None),
         why='Scheme p5 bullets five precautions under a lead-in; "(Any two) 3 + 2".',
         topic='eng-2-11',
         lifted=[S(5, 100, 360, 530, 376), S(5, 100, 376, 530, 390), S(5, 100, 390, 530, 405),
                 S(5, 100, 405, 530, 420), S(5, 100, 420, 530, 434)],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         notes="The scheme prints '(Any two) 3 + 2'."),
    dict(key=(1, 'c', None),
         why='Scheme p5 describes the process in one paragraph, "5".',
         topic='eng-1-2',
         lifted=[S(5, 70, 471, 562, 548)], marks=[5], total=5,
         notes="The scheme prints '5'."),
    dict(key=(1, 'd', None),
         why='The bicycle is photographed beside (d); scheme p5 lists the properties in '
             'one sentence, each lifted by its own word rectangle. "(Any two) 3 + 2".',
         topic='eng-1-9',
         lifted=[S(5, 70, 582, 192, 602), S(5, 192, 582, 346, 602), S(5, 346, 582, 446, 602),
                 S(5, 446, 582, 500, 602), S(5, 70, 598, 143, 616)],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         question_figure='engineering-2015-HL-paper-q1d-art',
         notes="The scheme prints '(Any two) 3 + 2'."),
    dict(key=(1, 'e', None),
         why='Scheme p5 gives the reasons in one sentence, each lifted by its own word '
             'rectangle. "(Any two) 3 + 2".',
         topic='eng-1-5',
         lifted=[S(5, 234, 651, 414, 671), S(5, 414, 651, 524, 671), S(5, 70, 666, 220, 684)],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         notes="The scheme prints '(Any two) 3 + 2'."),
    dict(key=(1, 'f', None),
         why='Scheme p5 explains the term in one paragraph, "5".',
         topic='eng-1-9',
         lifted=[S(5, 70, 720, 562, 768)], marks=[5], total=5,
         notes="The scheme prints '5'."),
    dict(key=(1, 'g', None),
         why='A lead-in over three people set as romans, "any one"; scheme p6 writes a '
             'note on each under the name, "(Any one) 5".',
         topic='eng-3-14',
         lifted=[[join(S(6, 106, 67, 180, 88), S(6, 106, 82, 560, 129)),
                  join(S(6, 106, 136, 185, 157), S(6, 106, 150, 560, 184)),
                  join(S(6, 106, 177, 200, 198), S(6, 106, 191, 560, 226))]],
         row_kind='anyN', group=(1, 5), marks=[5], tariff='fixed', total=5,
         notes="The scheme prints '(Any one) 5'."),
    dict(key=(1, 'h', None),
         why='Scheme p6 bullets five advantages under a lead-in; "(Any two) 3 + 2".',
         topic='eng-2-15',
         lifted=[S(6, 100, 264, 500, 280), S(6, 100, 280, 500, 294), S(6, 100, 294, 500, 309),
                 S(6, 100, 309, 500, 323), S(6, 100, 323, 500, 338)],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         notes="The scheme prints '(Any two) 3 + 2'."),
    dict(key=(1, 'i', None),
         why='Scheme p6 gives the advantages in one sentence over three lines, each lifted '
             'by its own word rectangle. "(Any two) 3 + 2".',
         topic='eng-1-9',
         lifted=[S(6, 70, 361, 282, 382), S(6, 282, 361, 530, 382), S(6, 70, 375, 315, 396),
                 join(S(6, 315, 375, 540, 396), S(6, 70, 389, 288, 409))],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         notes="The scheme prints '(Any two) 3 + 2'."),
    dict(key=(1, 'j', None),
         why='The dart is photographed beside (j) with its barrel labelled; scheme p6 lists '
             'the processes on one line, "5" for the part.',
         topic='eng-2-11',
         lifted=[S(6, 70, 430, 482, 452)], marks=[5], total=5,
         question_figure='engineering-2015-HL-paper-q1j-art',
         notes="The scheme prints '5'."),
    dict(key=(1, 'k', None),
         why='Scheme p6 lists the processes on one line, each lifted by its own word '
             'rectangle; "(Any one) 5".',
         topic='eng-2-10',
         lifted=[[S(6, 70, 471, 99, 492), S(6, 99, 471, 225, 492), S(6, 225, 471, 320, 492),
                  S(6, 320, 471, 424, 492), S(6, 424, 471, 506, 492)]],
         row_kind='anyN', group=(1, 5), marks=[5], tariff='fixed', total=5,
         notes="The scheme prints '(Any one) 5'."),
    dict(key=(1, 'l', None),
         why='The seat is photographed beside (l); scheme p6 names two mechanisms on one '
             'line, each lifted by its own word rectangle, "5" for the part.',
         topic='eng-2-15',
         lifted=[[S(6, 70, 513, 159, 534), S(6, 159, 513, 280, 534)]],
         row_kind='anyN', group=(1, 5), marks=[5], tariff='fixed', total=5,
         question_figure='engineering-2015-HL-paper-q1l-art',
         notes="The scheme prints '5'."),
    dict(key=(1, 'm', None),
         why='The seat photographed beside (l) is the one (m) asks about; scheme p6 lists '
             'the methods in one sentence, each lifted by its own word rectangle. "(Any '
             'two) 3 + 2". The reader files the page footer and the Section B heading '
             'printed after (m) as its stem, so the card carries none.',
         topic='eng-3-7', stem=False,
         lifted=[S(6, 70, 554, 134, 575), S(6, 134, 554, 179, 575), S(6, 179, 554, 256, 575),
                 S(6, 256, 554, 332, 575)],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         question_figure='engineering-2015-HL-paper-q1l-art',
         notes="The scheme prints '(Any two) 3 + 2'."),
    # ---- Question 1, Section B ("Answer all of the following") -------------
    dict(key=(1, 'n', None),
         why='Section B. Scheme p7 bullets seven benefits; "(Any two) 5 + 5".',
         topic='eng-2-15', stem=False,
         lifted=[[S(7, 100, 126, 540, 141), S(7, 100, 141, 540, 156), S(7, 100, 156, 540, 170),
                  S(7, 100, 170, 540, 185), S(7, 100, 185, 540, 200), S(7, 100, 200, 540, 214),
                  S(7, 100, 214, 540, 229)]],
         row_kind='anyN', group=(2, 5), marks=[10], tariff='fixed', total=10,
         notes="The scheme prints '(Any two) 5 + 5'."),
    dict(key=(1, 'o', 'i'),
         why='Section B. The system is drawn with its parts lettered; scheme p7 names each '
             'after its letter on its own line, "1 + 1 + 1 + 1 + 1". The question is lifted '
             'with (o)\'s stimulus.',
         topic='eng-2-15', stem=False,
         question_lift=P(4, *_O1, more=[(145, 233, 320, 252)]),
         lifted=[S(7, 106, 297, 300, 311), S(7, 106, 311, 300, 325), S(7, 106, 325, 300, 339),
                 S(7, 106, 339, 300, 353), S(7, 106, 353, 300, 367)],
         marks=[1, 1, 1, 1, 1], total=5,
         labels={'A': S(7, 127, 297, 300, 311), 'B': S(7, 127, 311, 300, 325),
                 'C': S(7, 127, 325, 300, 339), 'D': S(7, 127, 339, 300, 353),
                 'E': S(7, 127, 353, 300, 367)},
         question_figure='engineering-2015-HL-paper-q1o-crop',
         notes="The scheme prints '1 + 1 + 1 + 1 + 1'."),
    dict(key=(1, 'o', 'ii'),
         why='Section B. Scheme p7 describes the principle under its heading, "5".',
         topic='eng-2-15', stem=False,
         question_lift=P(4, *_O1, more=[(145, 249, 460, 268)]),
         lifted=[join(S(7, 104, 418, 230, 438), S(7, 104, 432, 560, 548))], marks=[5], total=5,
         question_figure='engineering-2015-HL-paper-q1o-crop',
         notes="The scheme prints '5'."),
    dict(key=(1, 'p', 'i'),
         why='Section B. The injector is drawn with F, G and H beside it; scheme p7 names '
             'each after its letter, "1 + 1 + 1". The question is lifted with (p)\'s lead-in.',
         topic='eng-2-15', stem=False,
         question_lift=P(4, *_P1, more=[(145, 504, 330, 523)]),
         lifted=[S(7, 106, 587, 330, 601), S(7, 106, 601, 330, 615), S(7, 106, 615, 330, 629)],
         marks=[1, 1, 1], total=3,
         labels={'F': S(7, 125, 587, 330, 601), 'G': S(7, 125, 601, 330, 615),
                 'H': S(7, 125, 615, 330, 629)},
         question_figure='engineering-2015-HL-paper-q1p-crop',
         notes="The scheme prints '1 + 1 + 1'."),
    dict(key=(1, 'p', 'ii'),
         why='Section B. Scheme p7 describes the principle under its heading, "7".',
         topic='eng-2-15', stem=False,
         question_lift=P(4, *_P1, more=[(145, 517, 395, 537)]),
         lifted=[join(S(7, 104, 666, 230, 686), S(7, 104, 680, 560, 741))], marks=[7], total=7,
         question_figure='engineering-2015-HL-paper-q1p-crop',
         notes="The scheme prints '7'."),
    dict(key=(1, 'q', None),
         why='Section B. A lead-in over four sensors set as romans, "any two"; scheme p8 '
             'describes each under its name, "(Any two) 5 + 5".',
         topic='eng-2-15', stem=False,
         lifted=[[join(S(8, 106, 67, 240, 88), S(8, 106, 81, 560, 129)),
                  join(S(8, 106, 136, 200, 157), S(8, 106, 150, 560, 212)),
                  join(S(8, 106, 219, 260, 240), S(8, 106, 232, 560, 281)),
                  join(S(8, 106, 288, 180, 309), S(8, 106, 301, 560, 364))]],
         row_kind='anyN', group=(2, 5), marks=[10], tariff='fixed', total=10,
         notes="The scheme prints '(Any two) 5 + 5'."),
    dict(key=(1, 'r', None),
         why='Section B. Scheme p8 opens with a paragraph on direct injection, then writes on '
             'each of the two headings the ask names under its own heading, "5 + 5"; one '
             'row per heading, the opening paragraph priced under neither.',
         topic='eng-2-15', stem=False,
         lifted=[join(S(8, 104, 485, 210, 505), S(8, 104, 499, 560, 602)),
                 join(S(8, 104, 600, 200, 620), S(8, 104, 614, 560, 758))],
         marks=[5, 5], total=10,
         notes="The scheme prints '5 + 5'."),
    # ---- Question 2 --------------------------------------------------------
    dict(key=(2, 'a', 'ii'), topic='eng-3-8',
         replaces=NEW + 'left out the name of the test, "Impact test", printed as the '
                  'answer\'s heading, and the drawing printed beside it',
         why='Scheme p9 names the impact test and describes it beside a drawing of the '
             'pendulum, shown with the answer; "10".',
         lifted=[S(9, 106, 163, 412, 322)], marks=[10], total=10,
         question_figure='engineering-2015-HL-paper-q2ai-art',
         figure='engineering-2015-HL-scheme-q2aii-sol',
         notes="The scheme prints '10'."),
    dict(key=(2, 'b', 'i'),
         why='The graph is drawn with A, B and C on its curve; scheme p9 names each point '
             'after its letter, "2 + 2 + 2". The question is lifted with (b)\'s stimulus.',
         topic='eng-3-8', stem=False,
         question_lift=P(5, *_B2, more=[(145, 493, 470, 512)]),
         lifted=[S(9, 106, 334, 300, 348), S(9, 106, 348, 300, 362), S(9, 106, 362, 300, 376)],
         marks=[2, 2, 2], total=6,
         labels={'A': S(9, 127, 334, 300, 348), 'B': S(9, 127, 348, 300, 362),
                 'C': S(9, 127, 362, 300, 376)},
         question_figure='engineering-2015-HL-paper-q2b-crop',
         notes="The scheme prints '2 + 2 + 2'."),
    dict(key=(2, 'b', 'ii'),
         why='Scheme p9 describes the specimen at B and at C in turn, "6 + 6". The question '
             'is lifted with (b)\'s stimulus.',
         topic='eng-3-8', stem=False,
         question_lift=P(5, *_B2, more=[(145, 514, 530, 547)]),
         lifted=[S(9, 106, 399, 560, 433), S(9, 106, 433, 560, 474)],
         marks=[6, 6], total=12,
         question_figure='engineering-2015-HL-paper-q2b-crop',
         notes="The scheme prints '6 + 6', for B and C in that order."),
    dict(key=(2, 'c', 'ii'), topic='eng-3-8',
         replaces=NEW + 'left out the test\'s name, "X-ray / Radiography testing", and read '
                  'a label of the drawing, "Darkened area when processed", as a marking '
                  'point',
         why='Scheme p9 names the test and describes it beside a labelled drawing, shown '
             'with the answer; "8".',
         lifted=[S(9, 106, 562, 370, 723)], marks=[8], total=8,
         question_figure='engineering-2015-HL-paper-q2ci-art',
         figure='engineering-2015-HL-scheme-q2cii-sol',
         notes="The scheme prints '8'."),
    # ---- Question 3 --------------------------------------------------------
    dict(key=(3, 'a', 'i'), topic='eng-2-6',
         replaces=NEW + 'took the part\'s tariff, "8", printed at the end of the answer\'s '
                  'last line, into the marking point',
         why='Scheme p10 answers in two sentences, "8" printed at the end of the second '
             'line.',
         lifted=[S(10, 106, 108, 545, 142)], marks=[8], total=8,
         notes="The scheme prints '8'."),
    dict(key=(3, 'b', 'i'),
         why='The diagram is drawn with its regions lettered A-D; scheme p10 names each '
             'after its letter, "2 + 2 + 2 + 2". The question is lifted with (b)\'s stimulus.',
         topic='eng-1-3', stem=False,
         question_lift=P(6, *_B3, more=[(145, 492, 350, 511)]),
         lifted=[S(10, 106, 288, 300, 302), S(10, 106, 302, 300, 315),
                 S(10, 106, 315, 300, 329), S(10, 106, 329, 300, 343)],
         marks=[2, 2, 2, 2], total=8,
         labels={'A': S(10, 125, 288, 300, 302), 'B': S(10, 125, 302, 300, 315),
                 'C': S(10, 125, 315, 300, 329), 'D': S(10, 125, 329, 300, 343)},
         question_figure='engineering-2015-HL-paper-q3b-crop',
         notes="The scheme prints '2 + 2 + 2 + 2'."),
    dict(key=(3, 'b', 'ii'), topic='eng-1-3',
         replaces=NEW + 'read the two-column table, Point X beside Point Y, as one row',
         why='Scheme p10 sets the answer as a table, a column for each point under the '
             'four headings; each column is lifted cell by cell with its row headings, '
             '"5 + 5" for X and Y.',
         lifted=[join(S(10, 125, 388, 205, 406), S(10, 205, 388, 385, 406),
                      S(10, 125, 406, 205, 421), S(10, 205, 406, 385, 438),
                      S(10, 125, 438, 205, 453), S(10, 205, 438, 385, 453),
                      S(10, 125, 453, 205, 470), S(10, 205, 453, 385, 470)),
                 join(S(10, 125, 388, 205, 406), S(10, 385, 388, 560, 406),
                      S(10, 125, 406, 205, 421), S(10, 385, 406, 560, 438),
                      S(10, 125, 438, 205, 453), S(10, 385, 438, 560, 453),
                      S(10, 125, 453, 205, 470), S(10, 385, 453, 560, 470))],
         marks=[5, 5], total=10,
         question_figure='engineering-2015-HL-paper-q3b-crop',
         notes="The scheme prints '5 + 5', for X and Y in that order."),
    dict(key=(3, 'c', None), topic='eng-2-6',
         replaces=NEW + 'split each pair into two options, kept one sentence of the '
                  'induction and flame hardening answer, and offered the "(Any two) 8 + 8" '
                  'tariff as an option',
         why='A lead-in over four pairs set as romans, "any two"; scheme pp10-11 answer each '
             'pair in turn, the pyrometers and the hardening methods beside labelled '
             'drawings, shown with the answer. "(Any two) 8 + 8".',
         lifted=[[join(S(10, 105, 511, 320, 625), S(10, 105, 638, 320, 739)),
                  join(S(11, 105, 67, 365, 230), S(11, 105, 239, 375, 329)),
                  S(11, 105, 349, 560, 426),
                  S(11, 105, 446, 560, 578)]],
         row_kind='anyN', group=(2, 8), marks=[16], tariff='fixed', total=16,
         figure='engineering-2015-HL-scheme-q3c-sol',
         notes="The scheme prints '(Any two) 8 + 8'."),
    # ---- Question 4 --------------------------------------------------------
    dict(key=(4, 'a', None),
         why='The two lattices are drawn and lettered A and B; scheme p12 names each '
             'imperfection and describes it under the name, "(Name) 4 + 4", "(Describe) '
             '4 + 4".',
         topic='eng-1-3',
         lifted=[S(12, 106, 108, 250, 128), S(12, 106, 122, 560, 184),
                 S(12, 106, 191, 250, 211), S(12, 106, 205, 560, 253)],
         marks=[4, 4, 4, 4], total=16,
         labels={'A': S(12, 106, 108, 250, 128), 'B': S(12, 106, 191, 250, 211)},
         question_figure='engineering-2015-HL-paper-q4a-art',
         notes="The scheme prints '(Name) 4 + 4' and '(Describe) 4 + 4': A's name and "
               "description, then B's."),
    dict(key=(4, 'b', 'i'),
         why='The scheme answers with the drawn equilibrium diagram itself (p12), "8"; the '
             'ask is the row, the drawing shown with the answer. Lifted with (b)\'s table '
             'lead-in.',
         topic='eng-1-3', stem=False,
         question_lift=P(7, *_B4, more=[_GRAPH4, (145, 455, 435, 474)]),
         special={'kind': 'ask'}, total=8,
         question_figure='engineering-2015-HL-paper-q4b-crop',
         figure='engineering-2015-HL-scheme-q4bi-sol',
         notes="The scheme prints '8'."),
    dict(key=(4, 'b', 'ii'),
         why='Scheme p12 labels its drawn diagram (the labels are lifted off the drawing, '
             'one a region or line) and describes five features, "(Any three labels) 3", '
             '"(Any three descriptions) 3".',
         topic='eng-1-3', stem=False,
         question_lift=P(7, *_B4, more=[_GRAPH4, (145, 475, 392, 495)]),
         lifted=[[S(12, 180, 334, 255, 355), S(12, 296, 334, 368, 355),
                  S(12, 305, 362, 374, 384), S(12, 190, 421, 256, 442),
                  S(12, 266, 484, 336, 506)],
                 [S(12, 106, 619, 432, 640), S(12, 106, 632, 560, 667),
                  S(12, 106, 660, 560, 695), S(12, 106, 688, 300, 708),
                  S(12, 106, 702, 300, 722)]],
         row_kind='anyN', group=[(3, 1), (3, 1)], marks=[3, 3], tariff='fixed', total=6,
         question_figure='engineering-2015-HL-paper-q4b-crop',
         figure='engineering-2015-HL-scheme-q4bi-sol',
         notes="The scheme prints '(Any three labels) 3' and '(Any three descriptions) 3'."),
    dict(key=(4, 'b', 'iii'),
         why='Scheme p13 gives the ratio only as a stacked fraction of the two masses; the '
             'ask is the row, its print shown with the answer, "4".',
         topic='eng-1-3', stem=False,
         question_lift=P(7, *_B4, more=[_GRAPH4, (145, 496, 520, 534)]),
         special={'kind': 'ask'}, total=4,
         question_figure='engineering-2015-HL-paper-q4b-crop',
         figure='engineering-2015-HL-scheme-q4biii-sol',
         notes="The scheme prints '4'."),
    dict(key=(4, 'c', 'i'),
         why='The two cells are drawn and lettered X and Y; scheme p13 names each structure '
             'after its letter, "2 + 2". The question is lifted with (c)\'s stimulus.',
         topic='eng-1-3', stem=False,
         question_lift=P(7, *_C4, more=[(145, 696, 395, 715)]),
         lifted=[S(13, 106, 152, 310, 168), S(13, 106, 168, 310, 184)],
         marks=[2, 2], total=4,
         labels={'X': S(13, 175, 152, 310, 168), 'Y': S(13, 175, 168, 310, 184)},
         question_figure='engineering-2015-HL-paper-q4ci-art',
         notes="The scheme prints '2 + 2'."),
    dict(key=(4, 'c', 'ii'), topic='eng-1-3', stem=False,
         replaces=NEW + 'carried no picture of the structure X it asks about',
         why='Scheme p13 explains in two sentences, BCC then FCC; "8" for the part. The '
             'question is lifted with (c)\'s stimulus.',
         question_lift=P(7, *_C4, more=[(145, 717, 490, 736)]),
         lifted=[S(13, 106, 207, 560, 241), S(13, 106, 241, 560, 282)],
         tariff='questionTotal', total=8,
         question_figure='engineering-2015-HL-paper-q4ci-art',
         notes="The scheme prints '8'."),
    dict(key=(4, 'c', 'iii'),
         why='Scheme p13 lists metals for each structure on its own line, "2 + 2".',
         topic='eng-1-3', stem=False,
         question_lift=P(7, *_C4, more=[(145, 738, 512, 757)]),
         lifted=[S(13, 106, 304, 400, 322), S(13, 106, 322, 400, 338)],
         marks=[2, 2], total=4,
         labels={'X': S(13, 175, 152, 310, 168), 'Y': S(13, 175, 168, 310, 184)},
         question_figure='engineering-2015-HL-paper-q4ci-art',
         notes="The scheme prints '2 + 2', for X and Y in that order."),
    # ---- Question 5 --------------------------------------------------------
    dict(key=(5, 'a', 'iv'), topic='eng-2-10',
         replaces=NEW + 'set the fumes heading as a row of its own and read the "(Any three) '
                  '6 + 6 + 6" tariff as a marking point',
         why='One of "Answer any three of the following", "(Any three) 6 + 6 + 6": scheme '
             'p14 answers each hazard in turn, the fumes as a heading over four bullets.',
         lifted=[S(14, 105, 208, 560, 257), S(14, 105, 277, 560, 353),
                 S(14, 105, 374, 500, 452)],
         tariff='questionTotal', total=6,
         notes="The scheme prints '(Any three) 6 + 6 + 6' for the three parts answered."),
    dict(key=(5, 'b', 'i'), topic='eng-2-10',
         replaces=NEW + 'set the process and its four reasons as five rows under a question '
                  'total; the scheme prices the name and one reason apart',
         why='The kart is photographed beside (b); scheme p14 names the process on its '
             'line and gives four reasons, one a line, "(Name) 3", "(Reason) 3".',
         lifted=[S(14, 106, 487, 500, 504),
                 [S(14, 106, 504, 500, 519), S(14, 106, 519, 500, 533),
                  S(14, 106, 533, 500, 547), S(14, 106, 547, 500, 561)]],
         marks=[3, 3], total=6,
         question_figure='engineering-2015-HL-paper-q5bi-art',
         notes="The scheme prints '(Name) 3' and '(Reason) 3'."),
    dict(key=(5, 'b', 'ii'),
         why='Scheme p14 describes MIG welding beside a drawing of the set, shown with the '
             'answer; "10". Three words of the drawing\'s labels sit under the picture in '
             'the text layer and are left out with it.',
         topic='eng-2-10',
         lifted=[S(14, 105, 584, 380, 732)], marks=[10], total=10,
         question_figure='engineering-2015-HL-paper-q5bi-art',
         figure='engineering-2015-HL-scheme-q5bii-sol',
         notes="The scheme prints '10'."),
    dict(key=(5, 'c', None),
         why='Paper p8 sets two alternative (c)s either side of an OR. This card is the '
             'first branch, seam and spot welding compared under four headings; scheme '
             'p15 answers in two columns under labelled drawings, shown with the answer. '
             'Each cell is lifted with its column\'s process and its heading. "16" for the '
             'part.',
         topic='eng-2-10', stem=False,
         question_lift=P(8, 118, 484, 465, 519, more=[(145, 522, 300, 590)]),
         lifted=[join(S(15, 100, 82, 230, 102), S(15, 250, 300, 345, 320),
                      S(15, 34, 328, 298, 362)),
                 join(S(15, 360, 82, 500, 102), S(15, 250, 300, 345, 320),
                      S(15, 300, 328, 560, 362)),
                 join(S(15, 100, 82, 230, 102), S(15, 235, 369, 360, 389),
                      S(15, 34, 397, 298, 514)),
                 join(S(15, 360, 82, 500, 102), S(15, 235, 369, 360, 389),
                      S(15, 300, 397, 560, 514)),
                 join(S(15, 100, 82, 230, 102), S(15, 265, 521, 330, 541),
                      S(15, 34, 549, 298, 583)),
                 join(S(15, 360, 82, 500, 102), S(15, 265, 521, 330, 541),
                      S(15, 300, 549, 560, 583)),
                 join(S(15, 100, 82, 230, 102), S(15, 260, 590, 335, 610),
                      S(15, 34, 618, 298, 652)),
                 join(S(15, 360, 82, 500, 102), S(15, 260, 590, 335, 610),
                      S(15, 300, 618, 560, 652))],
         tariff='questionTotal', total=16,
         figure='engineering-2015-HL-scheme-q5c-sol',
         notes="The scheme prints '16'. " + _OR5),
    dict(key=(5, 'c', 'i'),
         replaces=NEW + 'left the first term\'s heading, "Degree of freedom", off its row',
         why='The OR branch\'s (i): the Robocoaster is photographed beside it; scheme p16 '
             'writes on each term under its heading, "4 + 4".',
         topic='eng-3-14',
         lifted=[S(16, 106, 67, 560, 142), S(16, 106, 150, 560, 211)],
         marks=[4, 4], total=8,
         question_figure='engineering-2015-HL-paper-q5ci-art',
         notes="The scheme prints '4 + 4', for the degrees of freedom and the working "
               "envelope in that order. " + _OR5),
    dict(key=(5, 'c', 'ii'), topic='eng-3-14',
         replaces=NEW + 'left out the first reason, "Programmable robots allow for very '
                  'precise movements.", printed on the (ii) line',
         why='The OR branch\'s (ii): scheme p16 gives five reasons, one a line; "4 + 4" for '
             'two.',
         lifted=[S(16, 106, 231, 560, 246), S(16, 106, 246, 560, 259), S(16, 106, 259, 560, 273),
                 S(16, 106, 273, 560, 287), S(16, 106, 287, 560, 301)],
         tariff='orderedSplit', notation='4 + 4', ladder=8, total=8,
         question_figure='engineering-2015-HL-paper-q5ci-art',
         notes="The scheme prints '4 + 4'. " + _OR5),
    # ---- Question 6 --------------------------------------------------------
    dict(key=(6, 'a', 'i'), topic='eng-1-9',
         replaces=NEW + 'set the properties as one row under a question total',
         why='The mouthguard is photographed beside (a); scheme p16 states the properties '
             'in three sentences, each lifted by its own word rectangle. "4 + 4" for two.',
         lifted=[S(16, 106, 393, 292, 413), S(16, 294, 393, 490, 413), S(16, 106, 407, 242, 427),
                 S(16, 242, 407, 355, 427), S(16, 355, 407, 411, 427),
                 join(S(16, 432, 407, 485, 427), S(16, 106, 421, 188, 441)),
                 S(16, 188, 421, 335, 441)],
         tariff='orderedSplit', notation='4 + 4', ladder=8, total=8,
         question_figure='engineering-2015-HL-paper-q6ai-art',
         notes="The scheme prints '4 + 4'."),
    dict(key=(6, 'a', 'ii'),
         why='Scheme p16 names injection moulding and describes it beside a labelled '
             'drawing of the machine, shown with the answer; "8".',
         topic='eng-1-9',
         lifted=[join(S(16, 106, 462, 500, 497), S(16, 106, 652, 560, 756))], marks=[8], total=8,
         question_figure='engineering-2015-HL-paper-q6ai-art',
         figure='engineering-2015-HL-scheme-q6aii-sol',
         notes="The scheme prints '8'."),
    dict(key=(6, 'b', None), topic='eng-1-9',
         replaces=NEW + 'split each pair into two options and offered the "(Any two) 8 + 8" '
                  'tariff as an option',
         why='A lead-in over four pairs set as romans, "any two"; scheme p17 answers each '
             'pair in turn, "(Any two) 8 + 8".',
         lifted=[[S(17, 106, 67, 560, 115), S(17, 106, 122, 560, 212),
                  S(17, 106, 218, 560, 308), S(17, 106, 315, 560, 377)]],
         row_kind='anyN', group=(2, 8), marks=[16], tariff='fixed', total=16,
         notes="The scheme prints '(Any two) 8 + 8'."),
    dict(key=(6, 'c', 'i'), topic='eng-1-9',
         replaces=NEW + 'read "(For each: Structure @ 2, Property @ 2)" as a marking point '
                  'and set the three plastics as one ordered split',
         why='The three structures are drawn and captioned under (c); scheme p17 gives each '
             'plastic\'s structure in a sentence and its properties one a line, "4 + 4 + 4 '
             '(For each: Structure @ 2, Property @ 2)". The question is lifted with each '
             'caption on its own line, as the paper sets them under their pictures.',
         question_lift=P(9, 145, 500, 520, 536, items=[(140, 615, 225, 636),
                                                      (255, 615, 380, 636),
                                                      (440, 615, 510, 636)]),
         lifted=[join(S(17, 106, 412, 200, 432), S(17, 106, 426, 300, 446)),
                 [S(17, 175, 440, 480, 458), S(17, 175, 454, 480, 472), S(17, 175, 468, 480, 486),
                  S(17, 175, 482, 480, 500), S(17, 175, 496, 480, 514), S(17, 175, 509, 480, 529)],
                 join(S(17, 106, 536, 240, 557), S(17, 106, 550, 300, 570)),
                 [S(17, 175, 566, 480, 582), S(17, 175, 582, 480, 596), S(17, 175, 596, 480, 610),
                  S(17, 175, 610, 480, 624), S(17, 175, 624, 480, 640)],
                 join(S(17, 106, 633, 200, 654), S(17, 106, 646, 500, 667)),
                 [S(17, 175, 662, 560, 678), S(17, 175, 678, 560, 692), S(17, 175, 692, 560, 719),
                  S(17, 175, 719, 560, 733), S(17, 175, 733, 560, 749)]],
         marks=[2, 2, 2, 2, 2, 2], total=12,
         question_figure='engineering-2015-HL-paper-q6c-crop',
         notes="The scheme prints '4 + 4 + 4' and '(For each: Structure @ 2, Property @ 2)': "
               "each plastic's structure, then any one of its properties."),
    # ---- Question 7 --------------------------------------------------------
    dict(key=(7, 'a', 'i'),
         why='One of "Answer any three of the following", "(Any three) 6 + 6 + 6": scheme '
             'p18 names the materials on one line, each lifted by its own word rectangle.',
         topic='eng-2-15',
         checked='Paper p10 prints (a)(i) as one item of the list under "Answer any three '
                 'of the following:"; the semicolon ends the item, not the question.',
         lifted=[S(18, 106, 315, 127, 336), S(18, 127, 315, 164, 336), S(18, 164, 315, 209, 336)],
         tariff='questionTotal', total=6,
         notes="The scheme prints '(Any three) 6 + 6 + 6' for the three parts answered."),
    dict(key=(7, 'a', 'ii'),
         why='One of "Answer any three of the following": scheme p18 gives each gauge\'s '
             'function in a sentence beside drawings of both, shown with the answer.',
         topic='eng-3-12',
         checked='Paper p10 prints (a)(ii) as one item of the list under "Answer any three '
                 'of the following:"; the semicolon ends the item, not the question.',
         lifted=[S(18, 106, 356, 560, 390), S(18, 106, 390, 560, 419)],
         tariff='questionTotal', total=6,
         figure='engineering-2015-HL-scheme-q7aii-sol',
         notes="The scheme prints '(Any three) 6 + 6 + 6' for the three parts answered."),
    dict(key=(7, 'a', 'iii'),
         why='One of "Answer any three of the following": scheme p18 bullets five uses '
             'under a heading.',
         topic='eng-2-11',
         checked='Paper p10 prints (a)(iii) as one item of the list under "Answer any three '
                 'of the following:"; the semicolon ends the item, not the question.',
         lifted=[S(18, 140, 554, 500, 569), S(18, 140, 569, 500, 584), S(18, 140, 584, 500, 599),
                 S(18, 140, 599, 500, 613), S(18, 140, 613, 500, 628)],
         tariff='questionTotal', total=6,
         notes="The scheme prints '(Any three) 6 + 6 + 6' for the three parts answered."),
    dict(key=(7, 'a', 'iv'),
         why='One of "Answer any three of the following": scheme p18 describes each hole in '
             'a paragraph beside a drawing of it, shown with the answer.',
         topic='eng-2-11',
         checked='Paper p10 prints (a)(iv) as one item of the list under "Answer any three '
                 'of the following:"; the semicolon ends the item, not the question.',
         lifted=[S(18, 106, 651, 420, 699), S(18, 105, 708, 420, 761)],
         tariff='questionTotal', total=6,
         figure='engineering-2015-HL-scheme-q7aiv-sol',
         notes="The scheme prints '(Any three) 6 + 6 + 6' for the three parts answered."),
    dict(key=(7, 'a', 'v'), topic='eng-2-11',
         replaces=NEW + 'read the "(Any three) 6 + 6 + 6" tariff as a marking point',
         why='One of "Answer any three of the following": scheme p19 gives four properties, '
             'one a sentence.',
         lifted=[S(19, 106, 70, 560, 85), S(19, 106, 85, 560, 113), S(19, 106, 113, 560, 127),
                 S(19, 106, 127, 560, 142)],
         tariff='questionTotal', total=6,
         notes="The scheme prints '(Any three) 6 + 6 + 6' for the three parts answered."),
    dict(key=(7, 'b', 'i'), topic='eng-2-11',
         replaces=NEW + 'gave the process without the drawing the part asks for',
         why='Scheme p19 describes surface grinding beside a labelled drawing, shown with '
             'the answer; "8".',
         lifted=[S(19, 106, 218, 330, 350)], marks=[8], total=8,
         question_figure='engineering-2015-HL-paper-q7bi-art',
         figure='engineering-2015-HL-scheme-q7bi-sol',
         notes="The scheme prints '8'."),
    dict(key=(7, 'c', 'i'), topic='eng-2-11', stem=False,
         why='Both (c)s price their (i) at 8 (scheme pp19-20): the chips named after their '
             'letters with the material each comes from, "(Name) 2 + 2", "(Distinguish '
             'between) 2 + 2"; or two advantages and two disadvantages of CNC machining '
             'from bulleted lists, "2 + 2" each. One card for the printed OR, each branch a '
             'route.',
         question_lift=P(10, *_C7A, more=[(145, 538, 505, 572), _ORW7, _C7B,
                                          (150, 684, 390, 716)]),
         lifted=[S(19, 106, 590, 300, 610), S(19, 106, 605, 400, 623),
                 S(19, 106, 620, 300, 637), S(19, 106, 637, 400, 651),
                 [S(20, 140, 112, 560, 128), S(20, 140, 127, 560, 157), S(20, 140, 157, 560, 171),
                  S(20, 140, 171, 560, 186), S(20, 140, 186, 560, 200), S(20, 140, 200, 560, 229),
                  S(20, 140, 229, 560, 244)],
                 [S(20, 140, 298, 560, 313), S(20, 140, 313, 560, 328), S(20, 140, 328, 560, 342),
                  S(20, 140, 342, 560, 357), S(20, 140, 357, 560, 387)]],
         row_kind='anyN', group=[None, None, None, None, (2, 2), (2, 2)],
         marks=[2, 2, 2, 2, 4, 4], routes=['a', 'a', 'a', 'a', 'b', 'b'], total=8,
         labels={'A': S(19, 127, 590, 300, 610), 'B': S(19, 127, 617, 300, 637)},
         question_figure='engineering-2015-HL-paper-q7c-crop',
         notes="The scheme prints '(Name) 2 + 2' and '(Distinguish between) 2 + 2' for the "
               "chips, and '2 + 2' under the advantages and '2 + 2' under the "
               "disadvantages for CNC. " + _OR7),
    dict(key=(7, 'c', 'ii'), topic='eng-2-11', stem=False,
         why='Both (c)s price their (ii) at 8 (scheme pp19-20): the chip at C answered in one '
             'paragraph, "4 + 4" with no clause priced apart; or two of four factors, one a '
             'bullet, "4 + 4". One card for the printed OR, each branch a route.',
         question_lift=P(10, *_C7A, more=[(145, 578, 490, 612), _ORW7, _C7B,
                                          (150, 725, 395, 771)]),
         lifted=[S(19, 106, 714, 560, 762),
                 [S(20, 140, 440, 560, 455), S(20, 140, 455, 560, 470), S(20, 140, 470, 560, 485),
                  S(20, 140, 485, 560, 500)]],
         row_kind='anyN', group=[None, (2, 4)], marks=[8, 8], routes=['a', 'b'], total=8,
         question_figure='engineering-2015-HL-paper-q7c-crop',
         notes="The scheme prints '4 + 4' under each branch's answer; the chip at C is one "
               "paragraph, carried whole. " + _OR7),
    # ---- Question 8 --------------------------------------------------------
    dict(key=(8, 'a', 'i'),
         why='Scheme p21 describes the mechanism beside a labelled photograph, shown with '
             'the answer; "8". One word of the text layer, "precise", sits under the '
             'photograph and is left out with it. The question is lifted with (a)\'s '
             'stimulus.',
         topic='eng-2-15', stem=False,
         question_lift=P(11, *_A8, more=[(145, 127, 395, 178)]),
         lifted=[S(21, 106, 108, 345, 212)], marks=[8], total=8,
         question_figure='engineering-2015-HL-paper-q8a-crop',
         figure='engineering-2015-HL-scheme-q8ai-sol',
         notes="The scheme prints '8'."),
    dict(key=(8, 'a', 'ii'),
         why='Scheme p21 describes the method beside a labelled photograph, shown with the '
             'answer, "Suggested solution - other viable solutions are acceptable."; "8".',
         topic='eng-2-15', stem=False,
         question_lift=P(11, *_A8, more=[(145, 189, 395, 224)]),
         lifted=[S(21, 106, 259, 345, 333)], marks=[8], total=8,
         question_figure='engineering-2015-HL-paper-q8a-crop',
         figure='engineering-2015-HL-scheme-q8aii-sol',
         notes="The scheme prints '8', and 'Suggested solution - other viable solutions are "
               "acceptable.'"),
    dict(key=(8, 'b', None), topic='eng-2-15',
         replaces=NEW + 'split the roller bearing, DPDT and helical gear answers into one '
                  'option a bullet or sentence',
         why='A lead-in over five items set as romans, "any three"; scheme pp21-22 answer '
             'each in turn, "(Any three) 6 + 6 + 6".',
         lifted=[[S(21, 106, 425, 560, 494), S(21, 106, 525, 560, 619), S(21, 106, 640, 560, 675),
                  S(21, 106, 696, 560, 760), S(22, 106, 67, 560, 101)]],
         row_kind='anyN', group=(3, 6), marks=[18], tariff='fixed', total=18,
         notes="The scheme prints '(Any three) 6 + 6 + 6'."),
    dict(key=(8, 'c', 'i'), topic='eng-2-15', stem=False,
         replaces=NEW + 'took the label "Worm is connected to a" for the robot arm\'s '
                  'answer and set it beside the relay\'s under one question total',
         why='Both (c)s price their (i) at 8 (scheme pp22-23): a worm and wheel for the arm '
             'beside a labelled drawing, or the relay described beside a labelled drawing, '
             'both shown with the answer. One card for the printed OR, each branch a route.',
         question_lift=P(11, *_C8A, more=[(145, 528, 340, 547), _ORW8, _C8B,
                                          (145, 697, 400, 731)]),
         lifted=[join(S(22, 106, 232, 300, 252), S(22, 106, 263, 260, 378)),
                 S(23, 106, 80, 370, 239)],
         marks=[8, 8], routes=['a', 'b'], total=8,
         question_figure='engineering-2015-HL-paper-q8c-crop',
         figure='engineering-2015-HL-scheme-q8ci-sol',
         notes="The scheme prints '8' for each (i). " + _OR8),
    dict(key=(8, 'c', 'ii'), topic='eng-2-15', stem=False,
         replaces=NEW + 'set the robot\'s travel mechanism and the relay applications as '
                  'one question total, without the gear drive printed beside the drawing',
         why='Both (c)s price their (ii) at 8 (scheme pp22-23): the robot\'s drive, the text '
             'set beside and under a labelled drawing (the drawing\'s own label "Gear." is '
             'left out of the words), shown with the answer; or two of five applications, '
             'one a bullet, "4 + 4". One card for the printed OR, each branch a route.',
         question_lift=P(11, *_C8A, more=[(145, 549, 390, 583), _ORW8, _C8B,
                                          (145, 737, 330, 756)]),
         lifted=[join(S(22, 106, 450, 360, 470), S(22, 383, 471, 520, 505),
                      S(22, 383, 505, 520, 516), S(22, 383, 520, 520, 556),
                      S(22, 106, 643, 450, 692), S(22, 106, 712, 450, 733)),
                 [S(23, 140, 305, 560, 335), S(23, 140, 335, 560, 363), S(23, 140, 363, 560, 377),
                  S(23, 140, 377, 560, 392), S(23, 140, 392, 560, 422)]],
         row_kind='anyN', group=[None, (2, 4)], marks=[8, 8], routes=['a', 'b'], total=8,
         question_figure='engineering-2015-HL-paper-q8c-crop',
         figure='engineering-2015-HL-scheme-q8cii-sol',
         notes="The scheme prints '8' for the robot's (ii) and '4 + 4' for the relay's. "
               + _OR8),
]

TOPICS = {
    'eng-2015-hl-q5-a-iii': ('eng-2-10', 'the carburising flame is an oxy-acetylene welding '
                             'flame; "carburising" outvoted it for heat treatment'),
}

_ROB = 'Energy, Electronics & Robotics'
_RC = ('The Robocoaster (the OR branch of Q5(c)); the card\'s syllabus heading is '
       'Technology, where the syllabus places robotics.')

ATLAS = {
    'eng-2015-hl-q5-c-i': dict(topics=[_ROB], note=_RC),
    'eng-2015-hl-q5-c-ii': dict(topics=[_ROB], note=_RC),
    'eng-2015-hl-q7-a-i': dict(
        topics=['Machining & Metrology'],
        note='Lubricating materials for engineering machines, which the reference files Q7 '
             'under; the card\'s syllabus heading is Mechanisms.'),
}
