"""2016 Higher Level: the parts eng_all refuses or gets wrong, from the page.

Paper and scheme as the PDFs number their pages. The marks grid is on scheme
p4: Question 1 is Section A, "Any ten @ 5 marks each", and Section B, "Answer
all of the following", (n) to (r); Questions 2-8 are 50 marks each. The scheme
prints a part's marks under its answer ("(Any two) 3 + 2", "(Any three) 6 + 6 +
6"). This sitting had no cards before the lane: every card here is new, and a
`replaces=` names the automatic card it rebuilds before it ever shipped.
"""
from eng_lift import join, lift

Y, L = 2016, 'hl'
NEW = 'never shipped: the automatic card '
OWNED = ('never shipped: the automatic author builds this card only from the lifts this '
         'entry records, so the entry owns it')


def S(page, *rect):
    return lift(Y, L, 'scheme', page, rect)


def P(page, *rect, more=()):
    return lift(Y, L, 'paper', page, rect, more=more)


# Paper stems the romans are lifted with.
_O1 = (98, 281, 360, 314)             # p4: Q1(o), the FDM printer
_P1 = (98, 441, 523, 474)             # p4: Q1(p)'s lead-in
_B2 = (104, 294, 516, 327)            # p5: Q2(b), the two metals
_B3 = (104, 230, 447, 247)            # p6: Q3(b), the iron-carbon diagram
_B4 = (104, 277, 541, 295)            # p7: Q4(b), the table
_GRAPH4 = (104, 401, 262, 418)        # "Using the graph paper supplied:"
_C5A = (104, 454, 530, 487)           # p8: Q5(c), oxy-acetylene welding
_C7A = (104, 451, 517, 468)           # p10: Q7(c), the face milling cutter
_ORW7 = (308, 581, 330, 599)
_C7B = (104, 636, 528, 670)           # the CNC or manual machining (c)
_C8A = (104, 451, 366, 485)           # p11: Q8(c), the kart
_ORW8 = (290, 606, 312, 623)
_C8B = (104, 647, 326, 665)           # the solar phone charger (c)

_OR5 = ('The paper sets two (c)s either side of an OR: the oxy-acetylene welding (c), '
        'answered at the letter for 16, and the robotic milking machine (c), whose (i) and '
        '(ii) are carded apart.')
_OR7 = ('The paper sets two (c)s either side of an OR: the tungsten carbide inserts (c), '
        'whose (i) and (ii) are carded apart, and the CNC or manual machining (c), "6 + 6 '
        '+ 4" over its three applications, carded at the letter.')
_OR8 = ('The paper sets two (c)s either side of an OR, the kart and the solar phone '
        'charger; the scheme prices each (i) at 8 and each (ii) at 8 (4 + 4 for the '
        'charger\'s), so each roman is one card, each branch a route.')

CROPS = {
    # ---- paper ------------------------------------------------------------
    'engineering-2016-HL-paper-q1d-crop': dict(
        doc='paper', page=3, rect=(461, 256, 574, 370), image=True, ref='2016 HL Q1(d)'),
    # The FDM printer with its parts lettered A-D (the automatic crop lost D).
    'engineering-2016-HL-paper-q1o-crop': dict(
        doc='paper', page=4, rect=(385, 236, 562, 428), ref='2016 HL Q1(o)',
        letters=('A', 'B', 'C', 'D')),
    # The knee joint with its parts labelled; the end of (a)'s first line runs
    # into the picture's top-left corner and is whited out.
    'engineering-2016-HL-paper-q2a-crop': dict(
        doc='paper', page=5, rect=(405, 80, 591, 276), mask=[(403, 96, 427, 113)],
        ref='2016 HL Q2(a)'),
    # The results table, then the axes sketch "as shown opposite".
    'engineering-2016-HL-paper-q2b-crop': dict(
        doc='paper', parts=[(5, (61, 340, 541, 412)), (5, (480, 427, 547, 512))],
        ref='2016 HL Q2(b)'),
    # The camshaft; the ends of the lines either side of it are whited out.
    'engineering-2016-HL-paper-q3a-crop': dict(
        doc='paper', page=6, rect=(413, 104, 569, 205),
        mask=[(411, 98, 512, 114), (411, 193, 498, 210)], ref='2016 HL Q3(a)'),
    # The iron-carbon diagram with both axes (the automatic crop cut off the
    # % Carbon values).
    'engineering-2016-HL-paper-q3b-crop': dict(
        doc='paper', page=6, rect=(138, 250, 448, 512), ref='2016 HL Q3(b)'),
    'engineering-2016-HL-paper-q3c-crop': dict(
        doc='paper', page=6, rect=(432, 622, 581, 768), image=True, ref='2016 HL Q3(c)'),
    # The two stages drawn under (a), with their captions.
    'engineering-2016-HL-paper-q4a-crop': dict(
        doc='paper', page=7, rect=(130, 135, 505, 216), ref='2016 HL Q4(a)'),
    'engineering-2016-HL-paper-q4b-crop': dict(
        doc='paper', page=7, rect=(53, 311, 571, 384), ref='2016 HL Q4(b)'),
    # The cooling curve with X and Y, without (c)'s prose (the automatic crop
    # took it in).
    'engineering-2016-HL-paper-q4c-crop': dict(
        doc='paper', page=7, rect=(376, 566, 548, 730), ref='2016 HL Q4(c)',
        letters=('X', 'Y')),
    # Each (c) shows its own machine: the kart, then the solar charger.
    'engineering-2016-HL-paper-q8c-crop': dict(
        doc='paper', parts=[(11, (386, 451, 568, 592)), (11, (380, 642, 556, 778))],
        layout='row', ref='2016 HL Q8(c)'),
    # ---- scheme: the drawings the answers are given with -------------------
    'engineering-2016-HL-scheme-q1i-sol': dict(
        doc='scheme', page=6, rect=(473, 239, 558, 332), image=True, solution=True,
        ref='2016 HL Q1(i)'),
    'engineering-2016-HL-scheme-q1q-sol': dict(
        doc='scheme', parts=[(8, (140, 440, 508, 592)), (9, (180, 172, 482, 397))],
        solution=True, ref='2016 HL Q1(q)'),
    'engineering-2016-HL-scheme-q2aii-sol': dict(
        doc='scheme', page=10, rect=(368, 178, 592, 327), solution=True,
        ref='2016 HL Q2(a)(ii)'),
    'engineering-2016-HL-scheme-q2b-sol': dict(
        doc='scheme', page=10, rect=(118, 452, 540, 744), solution=True,
        ref='2016 HL Q2(b)'),
    'engineering-2016-HL-scheme-q2ci-sol': dict(
        doc='scheme', page=11, rect=(148, 258, 548, 436), solution=True,
        ref='2016 HL Q2(c)(i)'),
    # The induction coils round the camshaft; the foot of the page's "(50
    # Marks)" heading falls inside the box and is whited out.
    'engineering-2016-HL-scheme-q3ai-sol': dict(
        doc='scheme', page=12, rect=(384, 60, 570, 243), mask=[(495, 58, 560, 65)],
        solution=True, ref='2016 HL Q3(a)(i)'),
    'engineering-2016-HL-scheme-q3ci-sol': dict(
        doc='scheme', page=13, rect=(100, 140, 482, 310), solution=True,
        ref='2016 HL Q3(c)(i)'),
    'engineering-2016-HL-scheme-q3cii-sol': dict(
        doc='scheme', parts=[(13, (370, 388, 572, 463)), (13, (58, 494, 500, 634))],
        solution=True, ref='2016 HL Q3(c)(ii)'),
    'engineering-2016-HL-scheme-q4a-sol': dict(
        doc='scheme', page=14, rect=(57, 145, 557, 223), solution=True,
        ref='2016 HL Q4(a)'),
    'engineering-2016-HL-scheme-q4b-sol': dict(
        doc='scheme', page=14, rect=(88, 322, 560, 586), solution=True,
        ref='2016 HL Q4(b)'),
    # The ratio, printed as a stacked fraction.
    'engineering-2016-HL-scheme-q4biii-sol': dict(
        doc='scheme', page=15, rect=(143, 62, 352, 95), solution=True,
        ref='2016 HL Q4(b)(iii)'),
    'engineering-2016-HL-scheme-q5aii-sol': dict(
        doc='scheme', page=15, rect=(393, 373, 544, 526), solution=True,
        ref='2016 HL Q5(a)(ii)'),
    'engineering-2016-HL-scheme-q5c-sol': dict(
        doc='scheme', page=16, rect=(299, 396, 559, 604), solution=True,
        ref='2016 HL Q5(c)'),
    'engineering-2016-HL-scheme-q6aii-sol': dict(
        doc='scheme', page=18, rect=(310, 226, 575, 370), solution=True,
        ref='2016 HL Q6(a)(ii)'),
    'engineering-2016-HL-scheme-q7av-sol': dict(
        doc='scheme', page=20, rect=(455, 132, 566, 253), solution=True,
        ref='2016 HL Q7(a)(v)'),
    'engineering-2016-HL-scheme-q8ai-sol': dict(
        doc='scheme', page=21, rect=(357, 543, 588, 732), solution=True,
        ref='2016 HL Q8(a)(i)'),
    'engineering-2016-HL-scheme-q8aii-sol': dict(
        doc='scheme', page=22, rect=(145, 98, 540, 248), solution=True,
        ref='2016 HL Q8(a)(ii)'),
    'engineering-2016-HL-scheme-q8b-sol': dict(
        doc='scheme', parts=[(22, (339, 262, 565, 358)), (22, (430, 638, 560, 719))],
        layout='row', solution=True, ref='2016 HL Q8(b)'),
    'engineering-2016-HL-scheme-q8ci-sol': dict(
        doc='scheme', page=23, rect=(350, 72, 572, 232), solution=True,
        ref='2016 HL Q8(c)(i)'),
    'engineering-2016-HL-scheme-q8cii-sol': dict(
        doc='scheme', page=23, rect=(363, 298, 556, 428), solution=True,
        ref='2016 HL Q8(c)(ii)'),
}

CARDS = [
    # ---- Question 1, Section A ("Any ten @ 5 marks each") ------------------
    dict(key=(1, 'a', None),
         why='Scheme p5 lists the factors on one line; each is lifted by its own word '
             'rectangle. "(Any two) 3 + 2".',
         topic='eng-3-8',
         lifted=[S(5, 70, 232, 153, 249), S(5, 153, 232, 242, 249), S(5, 242, 232, 356, 249),
                 S(5, 356, 232, 381, 249), S(5, 381, 232, 445, 249)],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         notes="The scheme prints '(Any two) 3 + 2'."),
    dict(key=(1, 'b', None),
         why='Scheme p5 names the media at the end of one sentence; each is lifted by its '
             'own word rectangle. "(Any three) 2 + 2 + 1".',
         topic='eng-2-6',
         lifted=[S(5, 358, 280, 390, 298), S(5, 390, 280, 421, 298), S(5, 421, 280, 440, 298),
                 S(5, 440, 280, 464, 298), S(5, 484, 280, 503, 298)],
         tariff='orderedSplit', notation='2 + 2 + 1', ladder=5, total=5,
         notes="The scheme prints '(Any three) 2 + 2 + 1'."),
    dict(key=(1, 'c', None),
         why='A lead-in over three people set as romans, "any one"; scheme p5 writes a '
             'note on each under the name, "(Any one) 5".',
         topic='eng-3-14',
         lifted=[[join(S(5, 106, 329, 160, 346), S(5, 106, 344, 543, 378)),
                  join(S(5, 106, 376, 176, 394), S(5, 106, 391, 544, 441)),
                  join(S(5, 106, 440, 206, 457), S(5, 106, 456, 526, 487))]],
         row_kind='anyN', group=(1, 5), marks=[5], tariff='fixed', total=5,
         notes="The scheme prints '(Any one) 5'."),
    dict(key=(1, 'd', None),
         why='The selfie stick is photographed beside (d); scheme p5 lists the reasons on '
             'one line, each lifted by its own word rectangle. "(Any two) 3 + 2".',
         topic='eng-1-5',
         lifted=[S(5, 70, 518, 192, 535), S(5, 192, 518, 346, 535), S(5, 346, 518, 446, 535),
                 S(5, 446, 518, 510, 535)],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         question_figure='engineering-2016-HL-paper-q1d-crop',
         notes="The scheme prints '(Any two) 3 + 2'."),
    dict(key=(1, 'e', None),
         why='Scheme p5 gives the advantages and the disadvantages under their headings, '
             'over "3 + 2".',
         topic='eng-2-11',
         lifted=[S(5, 70, 566, 530, 599), S(5, 70, 598, 548, 631)],
         marks=[3, 2], total=5,
         notes="The scheme prints '3 + 2' under its advantages and disadvantages, in "
               "that order."),
    dict(key=(1, 'f', None),
         why='Scheme p5 lists the reasons in one sentence over three lines; each is lifted '
             'by its own word rectangle. "(Any two) 3 + 2".',
         topic='eng-3-14',
         lifted=[S(5, 70, 664, 449, 681), S(5, 449, 664, 511, 681),
                 join(S(5, 511, 664, 546, 681), S(5, 70, 678, 228, 695)),
                 join(S(5, 228, 678, 554, 695), S(5, 70, 691, 212, 709))],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         notes="The scheme prints '(Any two) 3 + 2'."),
    dict(key=(1, 'g', None),
         why='The helmet is photographed beside (g); scheme p6 answers in one paragraph, '
             '"5".',
         topic='eng-1-9',
         lifted=[S(6, 70, 48, 558, 93)], marks=[5], total=5,
         question_figure='engineering-2016-HL-paper-q1g-art',
         notes="The scheme prints '5'."),
    dict(key=(1, 'h', None),
         why='Scheme p6 bullets three advantages under a lead-in; "(Any two) 3 + 2".',
         topic='eng-2-15',
         lifted=[S(6, 104, 145, 549, 177), S(6, 104, 174, 331, 191), S(6, 104, 189, 247, 208)],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         notes="The scheme prints '(Any two) 3 + 2'."),
    dict(key=(1, 'i', None),
         why='Scheme p6 describes the method under its name beside a drawing of the drum, '
             'shown with the answer; "5".',
         topic='eng-1-2',
         lifted=[join(S(6, 70, 248, 177, 265), S(6, 69, 262, 423, 320))], marks=[5], total=5,
         figure='engineering-2016-HL-scheme-q1i-sol',
         notes="The scheme prints '5'."),
    dict(key=(1, 'j', None),
         why='The statue is photographed beside (j); scheme p6 explains the term and gives '
             'the reasons on their own lines, "4 + 1".',
         topic='eng-1-5',
         lifted=[S(6, 70, 358, 518, 376), S(6, 70, 374, 540, 407)],
         marks=[4, 1], total=5,
         question_figure='engineering-2016-HL-paper-q1j-art',
         notes="The scheme prints '4 + 1'."),
    dict(key=(1, 'k', None),
         why='Scheme p6 answers in one paragraph, "5".',
         topic='eng-3-8',
         lifted=[S(6, 70, 447, 557, 506)], marks=[5], total=5,
         notes="The scheme prints '5'."),
    dict(key=(1, 'l', None),
         why='Scheme p6 lists the reasons in one sentence over three lines; each is lifted '
             'by its own word rectangle. "(Any two) 3 + 2".',
         topic='eng-3-7',
         lifted=[S(6, 233, 544, 380, 561), S(6, 380, 544, 548, 561), S(6, 70, 558, 266, 575),
                 S(6, 266, 558, 443, 575),
                 join(S(6, 463, 558, 552, 575), S(6, 70, 571, 123, 589))],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         notes="The scheme prints '(Any two) 3 + 2'."),
    dict(key=(1, 'm', None),
         why='The shoes are photographed beside (m); scheme p6 gives the advantages in '
             'three clauses, each lifted by its own word rectangle. "(Any two) 3 + 2". The '
             'reader files the page footer and the Section B heading printed after (m) as '
             'its stem, so the card carries none.',
         topic='eng-3-8', stem=False,
         lifted=[S(6, 70, 627, 426, 644),
                 join(S(6, 446, 627, 555, 644), S(6, 70, 640, 315, 658)),
                 join(S(6, 318, 640, 534, 658), S(6, 70, 654, 236, 672))],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         question_figure='engineering-2016-HL-paper-q1m-art',
         notes="The scheme prints '(Any two) 3 + 2'."),
    # ---- Question 1, Section B ("Answer all of the following") -------------
    dict(key=(1, 'n', None),
         why='Section B. Scheme p7 bullets nine advantages; "(Any three) 4 + 3 + 3".',
         topic='eng-2-13', stem=False,
         lifted=[S(7, 104, 106, 380, 123), S(7, 104, 126, 241, 143), S(7, 104, 145, 349, 162),
                 S(7, 104, 164, 524, 196), S(7, 104, 198, 382, 215), S(7, 104, 217, 318, 234),
                 S(7, 104, 236, 235, 254), S(7, 104, 256, 224, 273), S(7, 104, 275, 392, 292)],
         tariff='orderedSplit', notation='4 + 3 + 3', ladder=10, total=10,
         notes="The scheme prints '(Any three) 4 + 3 + 3'."),
    dict(key=(1, 'o', 'i'),
         why='Section B. The printer is drawn with its parts lettered; scheme p7 names each '
             'after its letter on its own line, "1 + 1 + 1 + 1". The question is lifted '
             'with (o)\'s stimulus.',
         topic='eng-2-13', stem=False,
         question_lift=P(4, *_O1, more=[(126, 322, 278, 339)]),
         lifted=[S(7, 106, 335, 198, 352), S(7, 106, 356, 162, 373), S(7, 106, 377, 165, 394),
                 S(7, 106, 397, 202, 415)],
         marks=[1, 1, 1, 1], total=4,
         labels={'A': S(7, 127, 335, 198, 352), 'B': S(7, 127, 356, 162, 373),
                 'C': S(7, 127, 377, 165, 394), 'D': S(7, 127, 397, 202, 415)},
         question_figure='engineering-2016-HL-paper-q1o-crop',
         notes="The scheme prints '1 + 1 + 1 + 1'."),
    dict(key=(1, 'o', 'ii'),
         why='Section B. Scheme p7 describes the principle under its heading, "4".',
         topic='eng-2-13', stem=False,
         question_lift=P(4, *_O1, more=[(126, 338, 300, 356)]),
         lifted=[join(S(7, 104, 466, 222, 484), S(7, 104, 480, 558, 622))], marks=[4], total=4,
         question_figure='engineering-2016-HL-paper-q1o-crop',
         notes="The scheme prints '4'."),
    dict(key=(1, 'o', 'iii'),
         why='Section B. Scheme p7 lists the materials in one sentence, each lifted by its '
             'own word rectangle; any one, "2".',
         topic='eng-1-9', stem=False,
         question_lift=P(4, *_O1, more=[(126, 352, 317, 370)]),
         lifted=[[S(7, 237, 659, 431, 677), S(7, 431, 659, 541, 677), S(7, 104, 673, 206, 691),
                  S(7, 206, 673, 290, 691), S(7, 290, 673, 377, 691)]],
         row_kind='anyN', group=(1, 2), marks=[2], tariff='fixed', total=2,
         question_figure='engineering-2016-HL-paper-q1o-crop',
         notes="The scheme prints '2'."),
    dict(key=(1, 'p', 'i'),
         why='Section B. Scheme p8 writes on each field under its name, "5" each. The '
             'question is lifted with (p)\'s lead-in.',
         topic='eng-2-13', stem=False,
         question_lift=P(4, *_P1, more=[(126, 483, 189, 500)]),
         lifted=[join(S(8, 106, 76, 190, 93), S(8, 106, 89, 557, 203))], marks=[5], total=5,
         notes="The scheme prints '5'."),
    dict(key=(1, 'p', 'ii'),
         why='Section B. Scheme p8 writes on each field under its name, "5" each.',
         topic='eng-2-13', stem=False,
         question_lift=P(4, *_P1, more=[(126, 499, 233, 516)]),
         lifted=[join(S(8, 104, 227, 216, 245), S(8, 104, 241, 557, 314))], marks=[5], total=5,
         notes="The scheme prints '5'."),
    dict(key=(1, 'q', None),
         why='Section B. "Explain one of these processes": scheme pp8-9 explain each under '
             'its name, each beside a drawing, shown with the answer; "(Any one) 10". The '
             'question is lifted from the page without the bullets\' font glyphs.',
         topic='eng-2-13', stem=False,
         question_lift=P(4, 98, 544, 520, 575, more=[(130, 581, 245, 633)]),
         lifted=[[join(S(8, 104, 352, 237, 369), S(8, 104, 365, 555, 424),
                       S(8, 104, 614, 559, 728)),
                  join(S(9, 104, 48, 270, 65), S(9, 104, 62, 555, 176),
                       S(9, 104, 407, 516, 438))]],
         row_kind='anyN', group=(1, 10), marks=[10], tariff='fixed', total=10,
         figure='engineering-2016-HL-scheme-q1q-sol',
         notes="The scheme prints '(Any one) 10'."),
    dict(key=(1, 'r', None),
         why='Section B. A lead-in over four terms set as romans, "any two"; scheme p9 '
             'describes each under its heading, "(Any two) 5 +5".',
         topic='eng-2-13', stem=False,
         lifted=[[join(S(9, 104, 476, 176, 493), S(9, 104, 490, 555, 534)),
                  join(S(9, 104, 545, 191, 562), S(9, 104, 559, 555, 603)),
                  join(S(9, 104, 614, 195, 631), S(9, 104, 628, 542, 659)),
                  join(S(9, 104, 669, 423, 686), S(9, 120, 684, 464, 745))]],
         row_kind='anyN', group=(2, 5), marks=[10], tariff='fixed', total=10,
         notes="The scheme prints '(Any two) 5 +5'."),
    # ---- Question 2 --------------------------------------------------------
    dict(key=(2, 'a', 'i'), topic='eng-1-9',
         replaces=NEW + 'left out the first property, "All implant materials need to be '
                  'biocompatible.", printed on the (a)(i) line',
         why='The knee joint is photographed with its parts labelled; scheme p10 states '
             'four properties, one a line; "4 + 4" for two.',
         lifted=[[S(10, 104, 89, 338, 107), S(10, 104, 103, 441, 120),
                  S(10, 104, 117, 195, 134), S(10, 104, 131, 316, 148)]],
         row_kind='anyN', group=(2, 4), marks=[8], tariff='fixed', total=8,
         question_figure='engineering-2016-HL-paper-q2a-crop',
         notes="The scheme prints '4 + 4'."),
    dict(key=(2, 'a', 'ii'), replaces=OWNED,
         why='Scheme p10 names the Vickers test and describes it beside a labelled drawing '
             'of the indenter, shown with the answer; "8".',
         topic='eng-3-8',
         lifted=[join(S(10, 104, 172, 179, 190), S(10, 104, 188, 356, 330),
                      S(10, 104, 331, 545, 396))],
         marks=[8], total=8,
         question_figure='engineering-2016-HL-paper-q2a-crop',
         figure='engineering-2016-HL-scheme-q2aii-sol',
         notes="The scheme prints '8'."),
    dict(key=(2, 'b', 'i'),
         why='Scheme p10 answers with the plotted graph and prints no words; one ask row '
             'worth the part, with the scheme\'s graph shown. The question is lifted with '
             '(b)\'s stimulus and the table.',
         topic='eng-3-8', stem=False,
         question_lift=P(5, *_B2, more=[(133, 436, 432, 485)]),
         special={'kind': 'ask'}, total=10,
         question_figure='engineering-2016-HL-paper-q2b-crop',
         figure='engineering-2016-HL-scheme-q2b-sol',
         notes="The scheme prints '10' under its plotted graph."),
    dict(key=(2, 'b', 'ii'), topic='eng-3-8', stem=False,
         replaces=NEW + 'carried the results table as its stem, read flat',
         why='Scheme p11 gives each metal\'s tensile strength on its own line, "2 + 2". '
             'The question is lifted with (b)\'s stimulus and shows the table.',
         question_lift=P(5, *_B2, more=[(133, 500, 422, 533)]),
         lifted=[S(11, 104, 62, 345, 79), S(11, 104, 76, 339, 93)],
         marks=[2, 2], total=4,
         question_figure='engineering-2016-HL-paper-q2b-crop',
         figure='engineering-2016-HL-scheme-q2b-sol',
         notes="The scheme prints '2 + 2'."),
    dict(key=(2, 'b', 'iii'), topic='eng-3-8', stem=False,
         replaces=NEW + 'carried the results table as its stem, read flat, and the '
                  'headings\' bullets as unreadable font glyphs',
         why='Scheme p11 compares the metals in a sentence each, "2 + 2". The question is '
             'lifted with (b)\'s stimulus, without the bullets\' glyphs.',
         question_lift=P(5, *_B2, more=[(133, 547, 434, 565), (168, 563, 253, 598)]),
         lifted=[S(11, 104, 131, 434, 148), S(11, 104, 145, 548, 176)],
         marks=[2, 2], total=4,
         question_figure='engineering-2016-HL-paper-q2b-crop',
         notes="The scheme prints '2 + 2'."),
    dict(key=(2, 'c', 'i'), topic='eng-3-8',
         replaces=NEW + 'gave the test without its name and without the drawing the part '
                  'asks for',
         why='The device is photographed beside (c); scheme p11 names the test and '
             'describes it in two paragraphs under a drawing of the probe and the eddy '
             'currents, shown with the answer; "8" for the part.',
         lifted=[join(S(11, 104, 227, 200, 245), S(11, 104, 462, 550, 507)),
                 S(11, 104, 503, 548, 534)],
         tariff='questionTotal', total=8,
         question_figure='engineering-2016-HL-paper-q2ci-art',
         figure='engineering-2016-HL-scheme-q2ci-sol',
         notes="The scheme prints '8'."),
    dict(key=(2, 'c', 'ii'), topic='eng-3-8',
         replaces=NEW + 'read "4 + 4" as the definition of NDT for one 4 and every reason '
                  'together for the other',
         why='Scheme p11 answers in one paragraph that opens by defining NDT and then '
             'gives three reasons, each lifted by its own rectangles; "4 + 4" for two.',
         lifted=[[join(S(11, 100, 614, 548, 630), S(11, 100, 628, 498, 645)),
                  join(S(11, 500, 628, 560, 645), S(11, 100, 641, 359, 659)),
                  join(S(11, 360, 641, 552, 659), S(11, 100, 655, 218, 672))]],
         row_kind='anyN', group=(2, 4), marks=[8], tariff='fixed', total=8,
         question_figure='engineering-2016-HL-paper-q2ci-art',
         notes="The scheme prints '4 + 4'."),
    # ---- Question 3 --------------------------------------------------------
    dict(key=(3, 'a', 'i'), topic='eng-2-6',
         replaces=NEW + 'gave the process without its name and without the drawing the '
                  'part asks for',
         why='The camshaft is photographed beside (a); scheme p12 names induction '
             'hardening and describes it in one paragraph beside a labelled drawing, shown '
             'with the answer; "10".',
         lifted=[join(S(12, 104, 103, 218, 121), S(12, 104, 117, 376, 231))],
         marks=[10], total=10,
         question_figure='engineering-2016-HL-paper-q3a-crop',
         figure='engineering-2016-HL-scheme-q3ai-sol',
         notes="The scheme prints '10'."),
    dict(key=(3, 'a', 'ii'), topic='eng-2-6',
         replaces=NEW + 'carried no picture of the camshaft it refers to',
         why='Scheme p12 answers in one paragraph; "6" for the part.',
         lifted=[S(12, 104, 287, 531, 304), S(12, 104, 301, 557, 360)],
         tariff='questionTotal', total=6,
         question_figure='engineering-2016-HL-paper-q3a-crop',
         notes="The scheme prints '6'."),
    dict(key=(3, 'b', 'i'),
         why='The diagram is printed under (b) with its regions numbered; scheme p12 names '
             'each region after its number, one a line, "1 + 1 + 1 + 1 + 1". The question '
             'is lifted with (b)\'s stimulus.',
         topic='eng-1-4', stem=False,
         question_lift=P(6, *_B3, more=[(133, 518, 342, 535)]),
         lifted=[S(12, 104, 418, 226, 435), S(12, 104, 431, 171, 449), S(12, 104, 445, 244, 462),
                 S(12, 104, 459, 217, 476), S(12, 104, 473, 234, 490)],
         marks=[1, 1, 1, 1, 1], total=5,
         question_figure='engineering-2016-HL-paper-q3b-crop',
         notes="The scheme prints '1 + 1 + 1 + 1 + 1'."),
    dict(key=(3, 'b', 'ii'), topic='eng-2-6', stem=False,
         replaces=NEW + 'carried the diagram\'s axis labels as its stem',
         why='Scheme p12 describes annealing under its heading in one paragraph, "8".',
         lifted=[join(S(12, 104, 528, 256, 545), S(12, 104, 544, 535, 616))], marks=[8],
         total=8, notes="The scheme prints '8'."),
    dict(key=(3, 'b', 'iii'), topic='eng-2-6', stem=False,
         replaces=NEW + 'carried the diagram\'s axis labels as its stem and set the '
                  'benefits as one unpriced row',
         why='Scheme p12 lists the benefits in one sentence; each is lifted by its own '
             'word rectangle. "3 + 2".',
         lifted=[S(12, 104, 664, 304, 682), S(12, 304, 664, 397, 682), S(12, 397, 664, 500, 682),
                 S(12, 104, 678, 232, 695)],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         notes="The scheme prints '3 + 2'."),
    dict(key=(3, 'c', 'i'), topic='eng-2-6',
         replaces=NEW + 'gave the principle without its name and without the drawing the '
                  'part asks for',
         why='The pyrometer is photographed beside (c); scheme p13 names the thermocouple '
             'pyrometer and describes it over a labelled drawing, shown with the answer; '
             '"8".',
         lifted=[join(S(13, 104, 48, 240, 65), S(13, 104, 64, 541, 81)),
                 S(13, 104, 80, 547, 129)],
         tariff='questionTotal', total=8,
         question_figure='engineering-2016-HL-paper-q3c-crop',
         figure='engineering-2016-HL-scheme-q3ci-sol',
         notes="The scheme prints '8'."),
    dict(key=(3, 'c', 'ii'), topic='eng-2-6',
         replaces=NEW + 'carried a drawing\'s caption in its description and left out the '
                  'name the part asks for',
         why='Scheme p13 names two methods on one line, either one, "Name 4", and '
             'describes the optical pyrometer beside drawings of it, shown with the answer, '
             '"Describe 4".',
         lifted=[[S(13, 143, 367, 210, 384), S(13, 210, 367, 302, 384)],
                 S(13, 104, 383, 362, 469)],
         marks=[4, 4], total=8,
         question_figure='engineering-2016-HL-paper-q3c-crop',
         figure='engineering-2016-HL-scheme-q3cii-sol',
         notes="The scheme prints 'Name 4' and 'Describe 4'."),
    # ---- Question 4 --------------------------------------------------------
    dict(key=(4, 'a', None),
         why='Two stages are drawn and captioned under (a); scheme p14 describes dendritic '
             'growth in one paragraph over drawings of its stages, shown with the answer; '
             '"16". The reader joins the captions to the question, so it is lifted from '
             'the page.',
         topic='eng-1-3', stem=False,
         question_lift=P(7, 104, 103, 513, 136),
         lifted=[S(14, 104, 89, 555, 134)], marks=[16], total=16,
         question_figure='engineering-2016-HL-paper-q4a-crop',
         figure='engineering-2016-HL-scheme-q4a-sol',
         notes="The scheme prints '16'."),
    dict(key=(4, 'b', 'i'),
         why='Scheme p14 answers with the drawn diagram and prints no words; one ask row '
             'worth the part, with the scheme\'s diagram shown. The question is lifted with '
             '(b)\'s stimulus and the table.',
         topic='eng-1-3', stem=False,
         question_lift=P(7, *_B4, more=[_GRAPH4, (133, 425, 418, 442)]),
         special={'kind': 'ask'}, total=8,
         question_figure='engineering-2016-HL-paper-q4b-crop',
         figure='engineering-2016-HL-scheme-q4b-sol',
         notes="The scheme prints '8' under its drawn diagram."),
    dict(key=(4, 'b', 'ii'),
         why='Scheme p14 labels its diagram (shown with the answer) and describes six '
             'features, one a line; "4 + 4" for the part, no split printed against the '
             'features, so one price for the part.',
         topic='eng-1-3', stem=False,
         question_lift=P(7, *_B4, more=[_GRAPH4, (133, 448, 373, 466)]),
         lifted=[S(14, 104, 614, 430, 631), S(14, 104, 628, 551, 659), S(14, 104, 655, 551, 686),
                 S(14, 104, 683, 298, 700), S(14, 104, 697, 245, 714), S(14, 104, 710, 553, 741)],
         tariff='questionTotal', total=8,
         question_figure='engineering-2016-HL-paper-q4b-crop',
         figure='engineering-2016-HL-scheme-q4b-sol',
         notes="The scheme prints '4 + 4'."),
    dict(key=(4, 'b', 'iii'),
         why='Scheme p15 gives the ratio as a stacked fraction, shown with the answer, and '
             'prints it nowhere as a line; one ask row worth the part, "2".',
         topic='eng-1-3', stem=False,
         question_lift=P(7, *_B4, more=[_GRAPH4, (133, 472, 450, 505)]),
         special={'kind': 'ask'}, total=2,
         question_figure='engineering-2016-HL-paper-q4b-crop',
         figure='engineering-2016-HL-scheme-q4biii-sol',
         notes="The scheme prints '2'."),
    dict(key=(4, 'c', 'i'),
         why='The cooling curve is drawn with X and Y marked; scheme p15 names each point '
             'on its own line, "4 + 4".',
         topic='eng-1-3', stem=False,
         question_lift=P(7, 104, 567, 377, 585, more=[(133, 595, 334, 632)]),
         lifted=[S(15, 104, 119, 269, 136), S(15, 104, 133, 265, 150)],
         marks=[4, 4], total=8,
         labels={'X': S(15, 158, 119, 269, 136), 'Y': S(15, 158, 133, 265, 150)},
         question_figure='engineering-2016-HL-paper-q4c-crop',
         notes="The scheme prints '4 + 4'."),
    dict(key=(4, 'c', 'ii'), topic='eng-1-3',
         replaces=NEW + 'set the four defects as one row and read the tariff "(Any two) 4 + '
                  '4" as a second',
         why='Scheme p15 names the defects on one line, each lifted by its own word '
             'rectangle; "(Any two) 4 + 4".',
         lifted=[[S(15, 104, 178, 154, 196), S(15, 154, 178, 238, 196),
                  S(15, 238, 178, 322, 196), S(15, 343, 178, 434, 196)]],
         row_kind='anyN', group=(2, 4), marks=[8], tariff='fixed', total=8,
         notes="The scheme prints '(Any two) 4 + 4'."),
    # ---- Question 5 --------------------------------------------------------
    dict(key=(5, 'a', 'ii'), topic='eng-2-10',
         replaces=NEW + 'gave the process without the drawing the part asks for',
         why='Scheme p15 describes TIG welding in one paragraph beside a drawing of the '
             'set-up, shown with the answer; "8".',
         lifted=[S(15, 104, 413, 381, 513)], marks=[8], total=8,
         question_figure='engineering-2016-HL-paper-q5ai-art',
         figure='engineering-2016-HL-scheme-q5aii-sol',
         notes="The scheme prints '8'."),
    dict(key=(5, 'b', 'v'), topic='eng-2-10',
         replaces=NEW + 'read the tariff "(Any three) 6 + 6 + 6" as an answer row',
         why='Scheme p16 bullets two advantages under a heading; "(Any three) 6 + 6 + 6", '
             '6 for the part.',
         lifted=[S(16, 104, 280, 541, 311), S(16, 104, 309, 536, 326)],
         tariff='questionTotal', total=6,
         notes="The scheme prints '(Any three) 6 + 6 + 6'."),
    dict(key=(5, 'c', None),
         why='Paper p8 sets two alternative (c)s either side of an OR. This card is the '
             'first branch, oxy-acetylene welding "with reference to each of" four '
             'headings; scheme pp16-17 answer each under its heading, the equipment beside '
             'a labelled drawing, shown with the answer. "16" for the part. The question '
             'is lifted without the bullets\' font glyphs.',
         topic='eng-2-10', stem=False,
         question_lift=P(8, *_C5A, more=[(170, 485, 300, 554)]),
         lifted=[join(S(16, 70, 405, 248, 423), S(16, 104, 422, 245, 512)),
                 join(S(16, 70, 551, 168, 568), S(16, 70, 564, 287, 613)),
                 join(S(16, 70, 640, 208, 657), S(16, 100, 654, 543, 744)),
                 join(S(17, 70, 48, 142, 65), S(17, 70, 64, 522, 145))],
         tariff='questionTotal', total=16,
         figure='engineering-2016-HL-scheme-q5c-sol',
         notes="The scheme prints '16'. " + _OR5),
    dict(key=(5, 'c', 'i'), topic='eng-3-14',
         replaces=NEW + 'set the advantages and disadvantages as one ordered list and split '
                  'one disadvantage in two',
         why='The robotic milking branch\'s (i): scheme p17 gives four advantages and three '
             'disadvantages under their headings, "4 + 4".',
         lifted=[[S(17, 104, 226, 545, 259), S(17, 104, 258, 549, 291),
                  S(17, 104, 290, 535, 323), S(17, 104, 321, 555, 354)],
                 [S(17, 104, 379, 554, 444), S(17, 104, 442, 554, 476),
                  S(17, 104, 474, 551, 571)]],
         marks=[4, 4], total=8,
         question_figure='engineering-2016-HL-paper-q5ci-art',
         notes="The scheme prints '4 + 4'. " + _OR5),
    # ---- Question 6 --------------------------------------------------------
    dict(key=(6, 'a', 'i'), topic='eng-1-9',
         replaces=NEW + 'set both reasons as one row under a question total',
         why='The pool balls are photographed beside (a); scheme p18 gives two reasons in '
             'a sentence each, "4 + 4".',
         lifted=[join(S(18, 104, 89, 545, 106), S(18, 104, 103, 368, 120)),
                 join(S(18, 369, 103, 553, 120), S(18, 104, 117, 336, 134))],
         marks=[4, 4], total=8,
         question_figure='engineering-2016-HL-paper-q6ai-art',
         notes="The scheme prints '4 + 4'."),
    dict(key=(6, 'a', 'ii'), topic='eng-1-9',
         replaces=NEW + 'gave the process without the drawing the part asks for',
         why='Scheme p18 names compression moulding and describes it beside a labelled '
             'drawing of the mould, shown with the answer; "8" for the part.',
         lifted=[S(18, 104, 172, 532, 203),
                 join(S(18, 104, 227, 306, 383), S(18, 104, 379, 519, 410))],
         tariff='questionTotal', total=8,
         question_figure='engineering-2016-HL-paper-q6ai-art',
         figure='engineering-2016-HL-scheme-q6aii-sol',
         notes="The scheme prints '8'."),
    dict(key=(6, 'b', 'i'), topic='eng-1-9',
         replaces=NEW + 'joined two of the three reasons into one row',
         why='The machine and the kicking tee are drawn under (b); scheme p18 gives three '
             'reasons in a sentence each, "2 + 2" for two.',
         lifted=[[S(18, 104, 448, 546, 465), S(18, 104, 462, 391, 479),
                  join(S(18, 392, 462, 512, 479), S(18, 104, 476, 257, 493))]],
         row_kind='anyN', group=(2, 2), marks=[4], tariff='fixed', total=4,
         question_figure='engineering-2016-HL-paper-q6bi-art',
         notes="The scheme prints '2 + 2'."),
    dict(key=(6, 'b', 'ii'), topic='eng-1-9',
         replaces=NEW + 'left out the first step, "Plastic granules are fed from the '
                  'hopper.", printed on the (ii) line',
         why='Scheme p18 sets the operation out a step a line; "10" for the part.',
         lifted=[S(18, 104, 531, 304, 548), S(18, 104, 545, 531, 576),
                 S(18, 104, 572, 554, 603), S(18, 104, 600, 545, 631),
                 S(18, 104, 628, 542, 645)],
         tariff='questionTotal', total=10,
         question_figure='engineering-2016-HL-paper-q6bi-art',
         notes="The scheme prints '10'."),
    # ---- Question 7 --------------------------------------------------------
    dict(key=(7, 'a', 'ii'), topic='eng-3-12',
         replaces=NEW + 'set the lead-in "Errors in measurement can occur ... reasons:" as '
                  'an answer row',
         why='Scheme p19 bullets four reasons under a lead-in; "(Any three) 6 + 6 + 6", 6 '
             'for the part.',
         lifted=[S(19, 124, 574, 395, 591), S(19, 124, 589, 269, 606),
                 S(19, 124, 603, 358, 621), S(19, 124, 618, 400, 635)],
         tariff='questionTotal', total=6,
         notes="The scheme prints '(Any three) 6 + 6 + 6'."),
    dict(key=(7, 'a', 'v'), topic='eng-2-11',
         replaces=NEW + 'read the tariff "(Any three) 6 + 6 + 6" as an answer row, and '
                  'carried no drawing',
         why='Scheme p20 explains each angle beside a drawing of the tool marking both, '
             'shown with the answer; "(Any three) 6 + 6 + 6", 6 for the part.',
         lifted=[S(20, 104, 153, 437, 170), S(20, 104, 167, 408, 184),
                 S(20, 104, 180, 332, 198), S(20, 104, 208, 433, 239)],
         tariff='questionTotal', total=6,
         figure='engineering-2016-HL-scheme-q7av-sol',
         notes="The scheme prints '(Any three) 6 + 6 + 6'."),
    dict(key=(7, 'b', 'ii'), topic='eng-2-15',
         replaces=NEW + 'set the four materials as one line under a question total',
         why='Scheme p20 names the materials on one line, each lifted by its own word '
             'rectangle; "4 + 4" for two.',
         lifted=[[S(20, 104, 410, 127, 427), S(20, 127, 410, 164, 427),
                  S(20, 164, 410, 209, 427), S(20, 209, 410, 243, 427)]],
         row_kind='anyN', group=(2, 4), marks=[8], tariff='fixed', total=8,
         notes="The scheme prints '4 + 4'."),
    dict(key=(7, 'c', 'i'),
         why='The tungsten carbide branch\'s (i), lifted with its cue; scheme p20 sets out '
             'the manufacture in a paragraph and its steps, "8" for the part.',
         topic='eng-2-11', stem=False,
         question_lift=P(10, *_C7A, more=[(133, 480, 462, 498)]),
         lifted=[S(20, 104, 479, 559, 512),
                 join(S(20, 104, 510, 175, 528), S(20, 104, 526, 549, 559)),
                 S(20, 104, 558, 371, 575), S(20, 104, 574, 467, 591),
                 S(20, 104, 590, 438, 607), S(20, 104, 606, 545, 639),
                 S(20, 104, 637, 536, 686)],
         tariff='questionTotal', total=8,
         question_figure='engineering-2016-HL-paper-q7ci-art',
         notes="The scheme prints '8'. " + _OR7),
    dict(key=(7, 'c', 'ii'),
         why='The tungsten carbide branch\'s (ii), lifted with its cue; scheme pp20-21 '
             'bullet four advantages and three disadvantages under their headings, "4 + '
             '4".',
         topic='eng-2-11', stem=False,
         question_lift=P(10, *_C7A, more=[(133, 508, 363, 541)]),
         lifted=[[S(20, 124, 733, 522, 764), S(21, 124, 49, 386, 66),
                  S(21, 124, 64, 543, 95), S(21, 124, 92, 485, 109)],
                 [S(21, 124, 135, 497, 152), S(21, 124, 149, 357, 166),
                  S(21, 124, 164, 372, 181)]],
         marks=[4, 4], total=8,
         question_figure='engineering-2016-HL-paper-q7ci-art',
         notes="The scheme prints '4 + 4'. " + _OR7),
    dict(key=(7, 'c', None), replaces=OWNED,
         why='The OR branch: CNC or manual machining "for each of the following '
             'applications", (i)-(iii) priced together, "6 + 6 + 4"; scheme p21 answers '
             'each after its roman. One card at the letter, a row each.',
         topic='eng-2-13', stem=False,
         question_lift=P(10, *_C7B, more=[(104, 677, 314, 695), (104, 698, 301, 715),
                                          (104, 719, 313, 736)]),
         lifted=[S(21, 104, 235, 457, 252), S(21, 104, 263, 546, 307),
                 S(21, 104, 318, 540, 375)],
         marks=[6, 6, 4], total=16,
         notes="The scheme prints '6 + 6 + 4'. " + _OR7),
    # ---- Question 8 --------------------------------------------------------
    dict(key=(8, 'a', 'i'), topic='eng-2-15',
         replaces=NEW + 'welded a label of the drawing into its last row, and carried no '
                  'drawing',
         why='The lift is photographed beside (a); scheme p21 describes the scissor lift '
             'beside a labelled photograph, shown with the answer, under "Suggested '
             'solutions - other viable solutions are acceptable."; "8" for the part.',
         lifted=[S(21, 104, 594, 345, 666), S(21, 104, 677, 345, 721)],
         tariff='questionTotal', total=8,
         question_figure='engineering-2016-HL-paper-q8ai-art',
         figure='engineering-2016-HL-scheme-q8ai-sol',
         notes="The scheme prints '8' under 'Suggested solutions - other viable solutions "
               "are acceptable.'"),
    dict(key=(8, 'a', 'ii'), topic='eng-2-15',
         replaces=NEW + 'gave the screw drive without the photograph the scheme labels',
         why='Scheme p22 answers in one paragraph over a labelled photograph of the screw '
             'drive, shown with the answer; "8".',
         lifted=[S(22, 104, 62, 527, 93)], marks=[8], total=8,
         question_figure='engineering-2016-HL-paper-q8ai-art',
         figure='engineering-2016-HL-scheme-q8aii-sol',
         notes="The scheme prints '8'."),
    dict(key=(8, 'b', None), replaces=OWNED,
         why='A lead-in over five terms set as romans, "any three"; scheme p22 describes '
             'each after its roman, the crank and slider and the idler gear beside '
             'drawings, shown with the answer; "(Any three) 6 + 6 + 6".',
         topic='eng-2-15',
         lifted=[[S(22, 104, 269, 330, 382),
                  join(S(22, 104, 416, 348, 433), S(22, 140, 433, 556, 493)),
                  S(22, 104, 536, 556, 567), S(22, 104, 605, 375, 622),
                  S(22, 104, 660, 394, 705)]],
         row_kind='anyN', group=(3, 6), marks=[18], tariff='fixed', total=18,
         figure='engineering-2016-HL-scheme-q8b-sol',
         notes="The scheme prints '(Any three) 6 + 6 + 6'."),
    dict(key=(8, 'c', 'i'), topic='eng-2-15', stem=False,
         why='Both (c)s price their (i) at 8 (scheme p23): the rack and pinion beside a '
             'labelled drawing, shown with the answer, or one of three energy conversions. '
             'One card for the printed OR, each branch a route.',
         question_lift=P(11, *_C8A, more=[(133, 499, 375, 532), _ORW8, _C8B,
                                          (133, 679, 375, 712)]),
         lifted=[S(23, 104, 62, 340, 216),
                 [S(23, 104, 511, 268, 528), S(23, 104, 525, 289, 542),
                  S(23, 104, 539, 269, 556)]],
         marks=[8, 8], routes=['a', 'b'], total=8,
         question_figure='engineering-2016-HL-paper-q8c-crop',
         figure='engineering-2016-HL-scheme-q8ci-sol', notes=_OR8),
    dict(key=(8, 'c', 'ii'), topic='eng-2-15', stem=False, replaces=OWNED,
         why='Both (c)s price their (ii) at 8 (scheme p23): the chain and sprocket drive '
             'beside a labelled photograph, shown with the answer, or two of four charging '
             'methods, one a line, "4 + 4". One card, each branch a route.',
         question_lift=P(11, *_C8A, more=[(133, 547, 383, 580), _ORW8, _C8B,
                                          (133, 725, 374, 758)]),
         lifted=[S(23, 104, 290, 352, 404),
                 [S(23, 104, 594, 312, 611), S(23, 104, 608, 187, 625),
                  S(23, 104, 622, 136, 639), S(23, 104, 635, 252, 653)]],
         row_kind='anyN', group=[None, (2, 4)], marks=[8, 8], routes=['a', 'b'],
         tariff='fixed', total=8,
         question_figure='engineering-2016-HL-paper-q8c-crop',
         figure='engineering-2016-HL-scheme-q8cii-sol', notes=_OR8),
]

TOPICS = {
    'eng-2016-hl-q5-a-i': ('eng-2-10', 'selecting a welding process for the drum is '
                           'joining; "stainless steel" outvoted it for iron and steel'),
    'eng-2016-hl-q5-c-ii': ('eng-3-14', 'the robotic milking machine\'s working envelope '
                            'and sensors are robotics, which the syllabus places under '
                            'Technology; "sensors" outvoted it for electronics'),
}

_ROB = 'Energy, Electronics & Robotics'
_RP = ('Rapid prototyping in the design of new products (the 2016 Higher Section B '
       'topic), which the reference files Q1 under Graphics and Design; the card\'s '
       'syllabus heading is Manufacturing systems.')
_EQ = ('read off the iron-carbon diagram the part is printed under; the card\'s syllabus '
       'heading is Iron and steel.')

ATLAS = {
    **{f'eng-2016-hl-q1-{p}': dict(topics=['Graphics and Design'], note=_RP)
       for p in ('n', 'o-i', 'o-ii', 'p-i', 'p-ii', 'q', 'r')},
    'eng-2016-hl-q2-a-i': dict(
        topics=['Polymers'],
        note='The properties of polyethylene as a bearing material; the reference files Q2 '
             'under testing only. The card\'s syllabus heading is Plastics.'),
    'eng-2016-hl-q3-b-i': dict(
        topics=['Equilibrium Diagrams'], note='The regions 1 to 5, ' + _EQ),
    'eng-2016-hl-q5-c-i': dict(
        topics=[_ROB],
        note='The robotic milking machine (the OR branch of Q5(c)); the card\'s syllabus '
             'heading is Technology, where the syllabus places robotics.'),
    'eng-2016-hl-q5-c-ii': dict(
        topics=[_ROB],
        note='The robotic milking machine (the OR branch of Q5(c)); the card\'s syllabus '
             'heading is Technology, where the syllabus places robotics.'),
    'eng-2016-hl-q7-b-i': dict(
        topics=['Machining & Metrology'],
        note='Lubricating a machine\'s rotating shaft, which the reference files Q7 under; '
             'the card\'s syllabus heading is Mechanisms.'),
    'eng-2016-hl-q7-b-ii': dict(
        topics=['Machining & Metrology'],
        note='Lubricating materials for engineering machines, which the reference files Q7 '
             'under; the card\'s syllabus heading is Mechanisms.'),
    'eng-2016-hl-q7-c': dict(
        topics=['Machining & Metrology'],
        note='CNC or manual machining for three applications (the OR branch of Q7(c)); the '
             'card\'s syllabus heading is Manufacturing systems.'),
}
