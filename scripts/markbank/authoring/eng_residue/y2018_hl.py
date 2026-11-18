"""2018 Higher Level: the parts eng_all refuses or gets wrong, from the page.

Paper and scheme as the PDFs number their pages. The marks grid is on scheme
p4: Question 1 is Section A, "Any ten @ 5 marks each", and Section B, "Answer
all of the following", (n) to (r); Questions 2-8 are 50 marks each. The scheme
prints a part's marks under its answer and an any-N tariff beside it ("Two
faults @ 4 + 4"), which the automatic author reads as an answer row more than
once. This sitting had no cards before the lane: every card here is new, and a
`replaces=` names the automatic card it rebuilds before it ever shipped.
"""
from eng_lift import join, lift

Y, L = 2018, 'hl'
NEW = 'never shipped: the automatic card '
OWNED = ('never shipped: the automatic author builds this card only from the lifts this '
         'entry records, so the entry owns it')


def S(page, *rect):
    return lift(Y, L, 'scheme', page, rect)


def P(page, *rect, more=()):
    return lift(Y, L, 'paper', page, rect, more=more)


# Paper stems the romans are lifted with.
_N1 = (97, 100, 370, 158)             # p4: Q1(n)
_O1 = (97, 243, 507, 300)             # p4: Q1(o)
_B2 = (97, 276, 508, 309)             # p5: Q2(b)
_B3 = (95, 243, 442, 259)             # p6: Q3(b)
_A4 = (100, 86, 374, 102)             # p7: Q4(a)
_B4 = (97, 358, 558, 391)             # p7: Q4(b)
_GRAPH4 = (97, 475, 260, 491)         # "Using the graph paper supplied:"
_C5 = (97, 429, 500, 462)             # p8: Q5(c), the flames
_C7A = (97, 426, 545, 459)            # p10: Q7(c), grinding wheels
_ORW7 = (307, 551, 328, 567)
_C7B = (97, 583, 525, 616)            # the CNC (c)
_C8A = (97, 467, 460, 500)            # p11: Q8(c), the golf cruiser
_C8B = (95, 629, 416, 645)            # the IC chips (c)

_OR5 = ('The paper sets two (c)s either side of an OR: the oxy-acetylene flames (c), '
        'answered at the letter for 16, and the robotic lawn mower (c), whose (i) and '
        '(ii) are carded apart.')
_OR7 = ('The paper sets two (c)s either side of an OR, grinding wheels and CNC '
        'technology; the scheme prices each (i) and each (ii) at 8.')
_OR8 = ('The paper sets two (c)s either side of an OR: the golf cruiser (c), (i) 8 and '
        '(ii) 4 + 4, and the IC chips (c), (i) 2 + 2, (ii) 4 and (iii) 4 + 4; priced '
        'differently, each branch is carded on its own.')


def _opts(page, y0, y1, *spans):
    """One option per word span on a printed line: (x0, x1) pairs."""
    return [S(page, x0, y0, x1, y1) for x0, x1 in spans]


CROPS = {
    # ---- paper ------------------------------------------------------------
    # The brake disk with its caption; the end of (d)'s first line runs into
    # the caption's edge and is whited out.
    'engineering-2018-HL-paper-q1d-crop': dict(
        doc='paper', page=3, rect=(444, 248, 580, 377),
        mask=[(442, 276, 456, 292), (442, 366, 466, 379)],
        ref='2018 HL Q1(d)'),
    # The helmet; the end of (h)'s first line runs under its bottom edge.
    'engineering-2018-HL-paper-q1g-crop': dict(
        doc='paper', page=3, rect=(465, 377, 560, 473), mask=[(463, 466, 492, 475)],
        ref='2018 HL Q1(g)'),
    # The quadcopter with all four propellers lettered and the arrow X (the
    # automatic crop cut off B and C).
    'engineering-2018-HL-paper-q1o-crop': dict(
        doc='paper', page=4, rect=(396, 283, 547, 422), ref='2018 HL Q1(o)',
        letters=('A', 'B', 'C', 'D', 'X')),
    # The three tensile graphs with both axes (the automatic crop lost strain).
    'engineering-2018-HL-paper-q2b-crop': dict(
        doc='paper', page=5, rect=(125, 308, 512, 482), ref='2018 HL Q2(b)',
        letters=('A', 'B', 'C')),
    'engineering-2018-HL-paper-q3b-crop': dict(
        doc='paper', page=6, rect=(88, 258, 470, 495), ref='2018 HL Q3(b)',
        letters=('A', 'B', 'C')),
    'engineering-2018-HL-paper-q4a-crop': dict(
        doc='paper', page=7, rect=(128, 108, 448, 262), ref='2018 HL Q4(a)',
        letters=('A', 'B', 'C', 'D', 'E', 'F')),
    'engineering-2018-HL-paper-q4b-crop': dict(
        doc='paper', page=7, rect=(80, 400, 568, 464), ref='2018 HL Q4(b)'),
    'engineering-2018-HL-paper-q8a-crop': dict(
        doc='paper', page=11, rect=(385, 134, 563, 262), ref='2018 HL Q8(a)'),
    # The golf cruiser; the ends of (c)'s two opening lines run into its
    # top-left corner and are whited out.
    'engineering-2018-HL-paper-q8c-crop': dict(
        doc='paper', page=11, rect=(378, 469, 543, 619),
        mask=[(376, 467, 456, 483), (376, 484, 407, 500)], ref='2018 HL Q8(c)'),
    # ---- scheme: the drawings the answers are given with -------------------
    'engineering-2018-HL-scheme-q1a-sol': dict(
        doc='scheme', page=5, rect=(328, 203, 580, 308), solution=True,
        ref='2018 HL Q1(a)'),
    'engineering-2018-HL-scheme-q1oi-sol': dict(
        doc='scheme', page=7, rect=(372, 600, 528, 722), solution=True,
        ref='2018 HL Q1(o)(i)'),
    'engineering-2018-HL-scheme-q1oii-sol': dict(
        doc='scheme', page=8, rect=(360, 60, 568, 212), solution=True,
        ref='2018 HL Q1(o)(ii)'),
    'engineering-2018-HL-scheme-q2aii-sol': dict(
        doc='scheme', page=10, parts=[(10, (405, 145, 545, 340)), (10, (60, 340, 580, 520))],
        solution=True, ref='2018 HL Q2(a)(ii)'),
    'engineering-2018-HL-scheme-q2cii-sol': dict(
        doc='scheme', page=11, rect=(105, 458, 450, 622), solution=True,
        ref='2018 HL Q2(c)(ii)'),
    'engineering-2018-HL-scheme-q3ai-sol': dict(
        doc='scheme', page=12, rect=(355, 98, 570, 274), solution=True,
        ref='2018 HL Q3(a)(i)'),
    'engineering-2018-HL-scheme-q3c-sol': dict(
        doc='scheme', page=13, parts=[(13, (125, 140, 515, 318)), (13, (40, 436, 547, 730))],
        solution=True, ref='2018 HL Q3(c)'),
    'engineering-2018-HL-scheme-q4aii-sol': dict(
        doc='scheme', page=14, rect=(115, 370, 595, 482), solution=True,
        ref='2018 HL Q4(a)(ii)'),
    # One drawn diagram answers three romans: (i)'s crop is the diagram
    # without the three labels (ii) asks for; (ii) and (iii) show it whole.
    'engineering-2018-HL-scheme-q4bi-sol': dict(
        doc='scheme', page=14, rect=(160, 560, 485, 772),
        mask=[(240, 570, 316, 586), (237, 659, 281, 692), (340, 659, 398, 675)],
        solution=True, ref='2018 HL Q4(b)(i)'),
    'engineering-2018-HL-scheme-q4bii-sol': dict(
        doc='scheme', page=14, rect=(160, 560, 485, 772), solution=True,
        ref='2018 HL Q4(b)(ii)'),
    'engineering-2018-HL-scheme-q5ai-sol': dict(
        doc='scheme', page=15, rect=(390, 565, 575, 752), mask=[(388, 712, 422, 756)],
        solution=True, ref='2018 HL Q5(a)(i)'),
    'engineering-2018-HL-scheme-q5c-sol': dict(
        doc='scheme', page=17, rect=(360, 222, 578, 536), solution=True,
        ref='2018 HL Q5(c)'),
    'engineering-2018-HL-scheme-q6ai-sol': dict(
        doc='scheme', page=18, rect=(94, 134, 525, 270), solution=True,
        ref='2018 HL Q6(a)(i)'),
    'engineering-2018-HL-scheme-q6cii-sol': dict(
        doc='scheme', page=20, rect=(80, 562, 500, 730), solution=True,
        ref='2018 HL Q6(c)(ii)'),
    'engineering-2018-HL-scheme-q7ci-sol': dict(
        doc='scheme', page=22, rect=(165, 555, 495, 672), solution=True,
        ref='2018 HL Q7(c)(i)'),
    'engineering-2018-HL-scheme-q7cii-sol': dict(
        doc='scheme', page=23, rect=(384, 92, 578, 226), solution=True,
        ref='2018 HL Q7(c)(ii)'),
    'engineering-2018-HL-scheme-q8ai-sol': dict(
        doc='scheme', page=24, rect=(348, 98, 552, 260), solution=True,
        ref='2018 HL Q8(a)(i)'),
    'engineering-2018-HL-scheme-q8aii-sol': dict(
        doc='scheme', page=24, rect=(165, 355, 478, 492), solution=True,
        ref='2018 HL Q8(a)(ii)'),
    'engineering-2018-HL-scheme-q8bv-sol': dict(
        doc='scheme', page=25, rect=(98, 370, 560, 452), solution=True,
        ref='2018 HL Q8(b)(v)'),
    'engineering-2018-HL-scheme-q8ci-sol': dict(
        doc='scheme', page=25, rect=(340, 532, 572, 694), solution=True,
        ref='2018 HL Q8(c)(i)'),
}

FOLDED = {
    'eng-2018-hl-q4-c-iii': NEW[:-1] + ' set "Ductility in BCC structures and ductility in '
                            'FCC structures" apart from the other two pairs of "Select any '
                            'two from (i), (ii) or (iii)"; the choice is one card, at Q4(c)',
}

CARDS = [
    # ---- Question 1, Section A ("Any ten @ 5 marks each") ------------------
    dict(key=(1, 'a', None),
         why='Scheme p5 answers in one paragraph beside a drawing of the sensor, the '
             'object and the waves, shown with the answer; "5".',
         topic='eng-2-16',
         lifted=[S(5, 70, 231, 316, 297)], marks=[5], total=5,
         figure='engineering-2018-HL-scheme-q1a-sol',
         notes="The scheme prints '5'."),
    dict(key=(1, 'b', None),
         why='Scheme p5 answers in one paragraph, "5".',
         topic='eng-3-8',
         lifted=[S(5, 70, 343, 528, 376)], marks=[5], total=5,
         notes="The scheme prints '5'."),
    dict(key=(1, 'c', None),
         why='Scheme p5 lists the benefits in one sentence; each is lifted by its own '
             'word rectangle. "3 + 2" for two.',
         topic='eng-1-5',
         lifted=[S(5, 200, 405, 261, 421), S(5, 261, 405, 297, 421),
                 S(5, 297, 405, 394, 421), S(5, 394, 405, 446, 421),
                 join(S(5, 446, 405, 545, 421), S(5, 70, 422, 248, 438)),
                 S(5, 248, 422, 309, 438),
                 join(S(5, 309, 422, 561, 438), S(5, 70, 438, 117, 454)),
                 S(5, 117, 438, 362, 454)],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         notes="The scheme prints '3 + 2'."),
    dict(key=(1, 'd', None),
         why='The brake disk is photographed and captioned beside (d); scheme p5 names '
             'three metals on one line, any one, each lifted by its own word rectangle. '
             '"5".',
         topic='eng-1-4',
         lifted=[[S(5, 70, 483, 119, 499), S(5, 119, 483, 254, 499),
                  S(5, 254, 483, 328, 499)]],
         row_kind='anyN', group=(1, 5), marks=[5], tariff='fixed', total=5,
         question_figure='engineering-2018-HL-paper-q1d-crop',
         notes="The scheme prints '5'."),
    dict(key=(1, 'e', None),
         why='Scheme p5 lists the reasons in one sentence; each is lifted by its own word '
             'rectangle. "3 + 2" for two.',
         topic='eng-3-14',
         lifted=[S(5, 70, 528, 183, 544), S(5, 183, 528, 424, 544),
                 join(S(5, 424, 528, 531, 544), S(5, 70, 545, 152, 561)),
                 S(5, 152, 545, 243, 561), S(5, 243, 545, 312, 561)],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         question_figure='engineering-2018-HL-paper-q1d-crop',
         notes="The scheme prints '3 + 2'."),
    dict(key=(1, 'f', None),
         why='Scheme p5 answers with the dimension, "5".',
         topic='eng-3-12',
         lifted=[S(5, 70, 590, 123, 606)], marks=[5], total=5,
         notes="The scheme prints '5'."),
    dict(key=(1, 'g', None),
         why='The helmet is photographed beside (g); scheme pp5-6 name either test and '
             'set out each under its heading, any one; each option is the opening line '
             'with one test. "5".',
         topic='eng-3-8',
         lifted=[[join(S(5, 70, 635, 361, 651), S(5, 88, 652, 137, 668),
                       S(5, 106, 669, 238, 685), S(5, 106, 686, 232, 702),
                       S(5, 106, 704, 272, 720), S(5, 106, 721, 307, 737),
                       S(5, 106, 739, 545, 755)),
                  join(S(5, 70, 635, 361, 651), S(6, 88, 57, 151, 73),
                       S(6, 106, 74, 238, 90), S(6, 106, 91, 245, 107),
                       S(6, 106, 109, 281, 125), S(6, 106, 126, 361, 142),
                       S(6, 106, 144, 545, 160))]],
         row_kind='anyN', group=(1, 5), marks=[5], tariff='fixed', total=5,
         question_figure='engineering-2018-HL-paper-q1g-crop',
         notes="The scheme prints '5'."),
    dict(key=(1, 'h', None),
         why='Scheme p6 writes on each of the three under their name, "Any one @ 5".',
         topic='eng-3-14',
         lifted=[[join(S(6, 106, 185, 175, 201), S(6, 70, 202, 551, 252)),
                  join(S(6, 106, 264, 189, 280), S(6, 70, 281, 551, 347)),
                  join(S(6, 106, 359, 167, 375), S(6, 70, 376, 536, 426))]],
         row_kind='anyN', group=(1, 5), marks=[5], tariff='fixed', total=5,
         notes="The scheme prints 'Any one @ 5'."),
    dict(key=(1, 'i', None),
         why='Scheme p6 answers in one paragraph, "5".',
         topic='eng-3-8',
         lifted=[S(6, 70, 460, 555, 510)], marks=[5], total=5,
         notes="The scheme prints '5'."),
    dict(key=(1, 'j', None),
         why='Scheme p6 answers in one paragraph, "5".',
         topic='eng-1-9',
         lifted=[S(6, 70, 539, 556, 589)], marks=[5], total=5,
         notes="The scheme prints '5'."),
    dict(key=(1, 'k', None),
         why='Scheme p6 bullets five reasons under a lead-in; "3 + 2" for two.',
         topic='eng-1-5',
         lifted=[S(6, 106, 629, 208, 645), S(6, 106, 644, 200, 660),
                 S(6, 106, 659, 134, 675), S(6, 106, 675, 177, 691),
                 S(6, 106, 690, 175, 706)],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         notes="The scheme prints '3 + 2'."),
    dict(key=(1, 'l', None),
         why='Scheme p6 names the reasons in one sentence; each is lifted by its own '
             'word rectangle. "3 + 2" for two.',
         topic='eng-1-4',
         lifted=[S(6, 327, 728, 423, 744), S(6, 423, 728, 501, 744),
                 join(S(6, 501, 728, 548, 744), S(6, 70, 745, 148, 761)),
                 S(6, 169, 745, 372, 761)],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         notes="The scheme prints '3 + 2'."),
    dict(key=(1, 'm', None),
         why='Scheme p7 bullets four advantages and four disadvantages under their '
             'headings; "3 + 2" for one of each. The reader files the Section B heading '
             'printed after (m) as its stem, so the card carries none.',
         topic='eng-3-14', stem=False,
         lifted=[join(S(7, 70, 57, 230, 73), S(7, 106, 74, 199, 90), S(7, 106, 91, 274, 107),
                      S(7, 106, 109, 202, 125), S(7, 106, 126, 209, 142)),
                 join(S(7, 70, 144, 244, 160), S(7, 106, 161, 180, 177),
                      S(7, 106, 178, 257, 194), S(7, 106, 196, 371, 212),
                      S(7, 106, 213, 213, 229))],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         notes="The scheme prints '3 + 2'."),
    # ---- Question 1, Section B ("Answer all of the following") -------------
    dict(key=(1, 'n', 'i'),
         why='Section B. Scheme p7 bullets five applications, "Two applications @ 3 + 2". '
             'The question is lifted with (n)\'s stimulus.',
         topic='eng-3-14', stem=False,
         question_lift=P(4, *_N1, more=[(112, 170, 298, 186)]),
         checked='paper page 4: "(i) Sporting and recreational activities;" under (n)\'s '
                 'lead-in; the semicolon is the list running on',
         lifted=[S(7, 142, 335, 334, 351), S(7, 142, 350, 212, 366),
                 S(7, 142, 365, 542, 396), S(7, 142, 395, 461, 411),
                 S(7, 142, 410, 528, 426)],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         notes="The scheme prints 'Two applications @ 3 + 2'."),
    dict(key=(1, 'n', 'ii'),
         why='Section B. Scheme p7 bullets seven applications, "Two applications @ 3 + 2".',
         topic='eng-3-14', stem=False,
         question_lift=P(4, *_N1, more=[(112, 188, 182, 204)]),
         lifted=[S(7, 142, 460, 252, 476), S(7, 142, 475, 189, 491),
                 S(7, 142, 490, 216, 506), S(7, 142, 505, 229, 521),
                 S(7, 142, 520, 194, 536), S(7, 142, 536, 231, 552),
                 S(7, 142, 552, 318, 568)],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         notes="The scheme prints 'Two applications @ 3 + 2'."),
    dict(key=(1, 'o', 'i'),
         why='Section B. Scheme p7 answers in one paragraph beside a drawing of the '
             'propellers\' rotation, shown with the answer; "5 + 5" for (o).',
         topic='eng-2-15', stem=False,
         question_lift=P(4, *_O1, more=[(115, 311, 309, 327)]),
         checked='paper page 4: "(i) Hovering in a fixed elevated position;" under (o)\'s '
                 'lead-in; the semicolon is the list running on',
         lifted=[S(7, 106, 617, 375, 717)], marks=[5], total=5,
         question_figure='engineering-2018-HL-paper-q1o-crop',
         figure='engineering-2018-HL-scheme-q1oi-sol',
         notes="The scheme prints '5 + 5' for (o)."),
    dict(key=(1, 'o', 'ii'),
         why='Section B. Scheme p8 answers in one paragraph beside a drawing marking the '
             'higher and lower speeds, shown with the answer; "5 + 5" for (o).',
         topic='eng-2-15', stem=False,
         question_lift=P(4, *_O1, more=[(115, 332, 359, 348)]),
         lifted=[S(8, 106, 91, 356, 174)], marks=[5], total=5,
         question_figure='engineering-2018-HL-paper-q1o-crop',
         figure='engineering-2018-HL-scheme-q1oii-sol',
         notes="The scheme prints '5 + 5' for (o)."),
    dict(key=(1, 'p', None),
         why='Section B. A lead-in over three sensors set as romans; scheme p8 explains '
             'each under its heading, "Any two @ 5 + 5".',
         topic='eng-2-16', stem=False,
         lifted=[[join(S(8, 106, 259, 241, 275), S(8, 106, 276, 551, 343)),
                  join(S(8, 106, 360, 220, 376), S(8, 106, 377, 556, 444)),
                  join(S(8, 106, 461, 306, 477), S(8, 106, 478, 556, 511))]],
         row_kind='anyN', group=(2, 5), marks=[10], tariff='fixed', total=10,
         notes="The scheme prints 'Any two @ 5 + 5'."),
    dict(key=(1, 'q', None),
         why='Section B. A lead-in over four terms set as romans; scheme pp8-9 describe '
             'each under its heading, "Any two @ 5 + 5".',
         topic='eng-3-14', stem=False,
         lifted=[[join(S(8, 106, 546, 175, 562), S(8, 106, 562, 435, 696)),
                  join(S(9, 106, 57, 203, 73), S(9, 106, 74, 560, 174)),
                  join(S(9, 106, 192, 200, 208), S(9, 106, 209, 549, 258)),
                  join(S(9, 106, 276, 159, 292), S(9, 106, 293, 546, 359))]],
         row_kind='anyN', group=(2, 5), marks=[10], tariff='fixed', total=10,
         notes="The scheme prints 'Any two @ 5 + 5'."),
    dict(key=(1, 'r', None),
         why='Section B. Scheme p9 bullets seven methods under a lead-in, "Two methods @ '
             '5 + 5".',
         topic='eng-3-14', stem=False,
         lifted=[[S(9, 106, 460, 464, 476), S(9, 106, 475, 370, 491),
                  S(9, 106, 491, 376, 507), S(9, 106, 506, 353, 522),
                  S(9, 106, 521, 522, 553), S(9, 106, 551, 490, 567),
                  S(9, 106, 566, 435, 582)]],
         row_kind='anyN', group=(2, 5), marks=[10], tariff='fixed', total=10,
         notes="The scheme prints 'Two methods @ 5 + 5'."),
    # ---- Question 2 --------------------------------------------------------
    dict(key=(2, 'a', 'ii'), topic='eng-3-8',
         replaces=NEW + 'gave the steps of the test without the drawings the part asks for',
         why='Scheme p10 bullets the test beside drawings of the machine, the specimens '
             'and the two fractures, shown with the answer; "8" for the part.',
         lifted=[S(10, 124, 175, 351, 191), S(10, 124, 193, 369, 226),
                 S(10, 124, 227, 373, 260), S(10, 124, 261, 395, 277),
                 S(10, 124, 279, 396, 295), S(10, 124, 296, 396, 330)],
         tariff='questionTotal', total=8,
         figure='engineering-2018-HL-scheme-q2aii-sol',
         notes="The scheme prints '8'."),
    dict(key=(2, 'b', 'i'),
         why='The three graphs are drawn and lettered; scheme p10 names a metal for each '
             'letter on its own line, "1 + 1 + 1".',
         topic='eng-3-8', stem=False,
         question_lift=P(5, *_B2, more=[(127, 489, 529, 520)]),
         lifted=[S(10, 106, 566, 163, 582), S(10, 106, 583, 196, 599),
                 S(10, 106, 600, 208, 616)],
         marks=[1, 1, 1], total=3,
         labels={'A': S(10, 125, 566, 163, 582), 'B': S(10, 124, 583, 196, 599),
                 'C': S(10, 124, 600, 208, 616)},
         question_figure='engineering-2018-HL-paper-q2b-crop',
         notes="The scheme prints '1 + 1 + 1'."),
    dict(key=(2, 'b', 'ii'), topic='eng-3-8', stem=False,
         replaces=NEW + 'carried no picture of the graphs it compares',
         why='Scheme pp10-11 compare the graphs in a paragraph each; "9" for the part.',
         question_lift=P(5, *_B2, more=[(127, 526, 476, 572)]),
         lifted=[S(10, 105, 650, 560, 716),
                 join(S(10, 105, 718, 562, 750), S(11, 105, 57, 556, 89))],
         tariff='questionTotal', total=9,
         question_figure='engineering-2018-HL-paper-q2b-crop',
         notes="The scheme prints '9'."),
    dict(key=(2, 'b', 'iii'),
         why='Scheme p11 answers with the stress read off graph B, "6".',
         topic='eng-3-8', stem=False,
         question_lift=P(5, *_B2, more=[(127, 578, 450, 594)]),
         lifted=[S(11, 105, 123, 165, 139)], marks=[6], total=6,
         question_figure='engineering-2018-HL-paper-q2b-crop',
         notes="The scheme prints '6'."),
    dict(key=(2, 'c', 'i'), topic='eng-3-8',
         replaces=NEW + 'welded the economic benefit, its mark and the safety benefit into '
                  'one row',
         why='Scheme p11 gives each benefit under its heading, "4" each.',
         lifted=[S(11, 106, 175, 552, 225), S(11, 106, 242, 566, 291)],
         marks=[4, 4], total=8,
         question_figure='engineering-2018-HL-paper-q2ci-art',
         notes="The scheme prints '4 + 4'."),
    dict(key=(2, 'c', 'ii'), topic='eng-3-8',
         replaces=NEW + 'gave the eddy current test without the drawing the part asks for',
         why='Scheme p11 names the test and describes it beside a drawing of the probe '
             'and the eddy currents, shown with the answer; "8".',
         lifted=[S(11, 106, 327, 558, 359), S(11, 106, 377, 563, 461)],
         tariff='questionTotal', total=8,
         question_figure='engineering-2018-HL-paper-q2ci-art',
         figure='engineering-2018-HL-scheme-q2cii-sol',
         notes="The scheme prints '8'."),
    # ---- Question 3 --------------------------------------------------------
    dict(key=(3, 'a', 'i'), replaces=OWNED,
         why='The sprocket is photographed beside (a); scheme p12 describes induction '
             'hardening in one paragraph beside a drawing of the coils and the water '
             'spray, shown with the answer; "8".',
         topic='eng-2-6',
         lifted=[join(S(12, 106, 91, 214, 107), S(12, 106, 108, 343, 275))],
         marks=[8], total=8,
         question_figure='engineering-2018-HL-paper-q3ai-art',
         figure='engineering-2018-HL-scheme-q3ai-sol',
         notes="The scheme prints '8'."),
    dict(key=(3, 'a', 'ii'), topic='eng-2-6',
         replaces=NEW + 'read the tariff "Two faults @ 4 + 4" as an answer row',
         why='Scheme p12 names the faults in one sentence; each is lifted by its own '
             'word rectangle. "Two faults @ 4 + 4".',
         lifted=[[S(12, 106, 310, 222, 326), S(12, 222, 310, 303, 326),
                  S(12, 303, 310, 549, 326), S(12, 106, 327, 233, 343),
                  S(12, 233, 327, 522, 343)]],
         row_kind='anyN', group=(2, 4), marks=[8], tariff='fixed', total=8,
         question_figure='engineering-2018-HL-paper-q3ai-art',
         notes="The scheme prints 'Two faults @ 4 + 4'."),
    dict(key=(3, 'b', 'i'), topic='eng-1-4', stem=False,
         replaces=NEW + 'welded both lines and their marks into one row, under the '
                  'diagram\'s axis labels read as its stem',
         why='Scheme p12 gives each line\'s name and transformation under its letter, '
             '"3 + 3".',
         question_lift=P(6, *_B3, more=[(126, 509, 463, 525)]),
         lifted=[join(S(12, 105, 411, 490, 427), S(12, 105, 428, 186, 444)),
                 join(S(12, 105, 445, 462, 461), S(12, 105, 461, 300, 477))],
         marks=[3, 3], total=6,
         question_figure='engineering-2018-HL-paper-q3b-crop',
         notes="The scheme prints '3 + 3'."),
    dict(key=(3, 'b', 'ii'), topic='eng-1-4', stem=False,
         replaces=NEW + 'took the diagram\'s axis labels for its stem and carried no '
                  'diagram',
         why='Scheme p12 answers in one paragraph, "6".',
         question_lift=P(6, *_B3, more=[(126, 535, 490, 551)]),
         lifted=[S(12, 106, 512, 558, 544)], marks=[6], total=6,
         question_figure='engineering-2018-HL-paper-q3b-crop',
         notes="The scheme prints '6'."),
    dict(key=(3, 'b', 'iii'), topic='eng-1-4', stem=False,
         replaces=NEW + 'took the diagram\'s axis labels for its stem and carried no '
                  'diagram',
         why='Scheme p12 answers in two paragraphs, the process and its effects; "6" for '
             'the part.',
         question_lift=P(6, *_B3, more=[(126, 560, 494, 624)]),
         lifted=[S(12, 106, 596, 562, 645), S(12, 106, 647, 528, 695)],
         tariff='questionTotal', total=6,
         question_figure='engineering-2018-HL-paper-q3b-crop',
         notes="The scheme prints '6'."),
    dict(key=(3, 'c', None), topic='eng-2-6',
         replaces=NEW + 'pooled the two methods the part offers as one answer, with the '
                  'drawing\'s caption as a row',
         why='"One method": scheme p13 describes the thermocouple pyrometer, then "OR" '
             'the optical pyrometer, each beside its drawing, shown with the answer; any '
             'one, "16".',
         lifted=[[join(S(13, 69, 57, 205, 73), S(13, 69, 74, 556, 139)),
                  S(13, 70, 360, 563, 426)]],
         row_kind='anyN', group=(1, 16), marks=[16], tariff='fixed', total=16,
         figure='engineering-2018-HL-scheme-q3c-sol',
         notes="The scheme prints '16', for either method."),
    # ---- Question 4 --------------------------------------------------------
    dict(key=(4, 'a', 'i'),
         why='The lattice is drawn with its defects lettered; scheme p14 names and '
             'describes four of them under their letters, "Name and describe three '
             'crystal point defects @ 4 + 4 + 4".',
         topic='eng-1-3', stem=False,
         question_lift=P(7, *_A4, more=[(126, 266, 424, 282)]),
         lifted=[[join(S(14, 106, 99, 220, 115), S(14, 106, 115, 413, 131)),
                  join(S(14, 106, 132, 215, 148), S(14, 106, 149, 536, 165)),
                  join(S(14, 106, 166, 265, 182), S(14, 106, 183, 375, 199)),
                  join(S(14, 106, 200, 202, 216), S(14, 106, 216, 560, 266))]],
         row_kind='anyN', group=(3, 4), marks=[12], tariff='fixed', total=12,
         question_figure='engineering-2018-HL-paper-q4a-crop',
         notes="The scheme prints 'Name and describe three crystal point defects @ 4 + 4 "
               "+ 4'."),
    dict(key=(4, 'a', 'ii'),
         why='Scheme p14 answers in one paragraph over a drawing of a line defect moving '
             'to the edge, shown with the answer; "4".',
         topic='eng-1-3', stem=False,
         question_lift=P(7, *_A4, more=[(126, 293, 433, 309)]),
         lifted=[S(14, 106, 301, 558, 367)], marks=[4], total=4,
         question_figure='engineering-2018-HL-paper-q4a-crop',
         figure='engineering-2018-HL-scheme-q4aii-sol',
         notes="The scheme prints '4'."),
    dict(key=(4, 'b', 'i'),
         why='Scheme p14 answers the drawing with the drawn diagram and prints no words; '
             'the diagram is shown with the answer, its labels whited out for (ii) to '
             'ask. "10".',
         topic='eng-1-3', stem=False,
         question_lift=P(7, *_B4, more=[_GRAPH4, (126, 499, 504, 532)]),
         special={'kind': 'ask'}, total=10,
         question_figure='engineering-2018-HL-paper-q4b-crop',
         figure='engineering-2018-HL-scheme-q4bi-sol',
         notes="The scheme prints '10'."),
    dict(key=(4, 'b', 'ii'),
         why='Scheme p15 prices "Labels on diagram 2 + 2 + 2"; the labels are the words '
             'on the drawn diagram (p14), each lifted from it, and the diagram is shown '
             'with them.',
         topic='eng-1-3', stem=False,
         question_lift=P(7, *_B4, more=[_GRAPH4, (126, 544, 434, 560)]),
         lifted=[S(14, 246, 570, 315, 586), S(14, 340, 659, 397, 675),
                 join(S(14, 237, 659, 280, 675), S(14, 237, 676, 267, 692))],
         marks=[2, 2, 2], total=6,
         question_figure='engineering-2018-HL-paper-q4b-crop',
         figure='engineering-2018-HL-scheme-q4bii-sol',
         notes="The scheme prints '2 + 2 + 2'."),
    dict(key=(4, 'b', 'iii'),
         why='Scheme p15 reads the points A, B and C and the ratio off the diagram, '
             'which is shown with them; "2".',
         topic='eng-1-3', stem=False,
         question_lift=P(7, *_B4, more=[_GRAPH4, (126, 570, 412, 605)]),
         lifted=[S(15, 106, 101, 204, 161)], marks=[2], total=2,
         question_figure='engineering-2018-HL-paper-q4b-crop',
         figure='engineering-2018-HL-scheme-q4bii-sol',
         notes="The scheme prints '2'."),
    dict(key=(4, 'c', None), topic='eng-1-3',
         replaces=NEW + 'set each pair\'s two terms as separate options, so one term of a '
                  'pair could be claimed for the 8 the pair is worth',
         why='"Select any two from (i), (ii) or (iii)": scheme p15 explains each pair '
             'under its roman; each option is the pair, "Any two @ 8 + 8".',
         lifted=[[S(15, 106, 189, 560, 272), S(15, 106, 290, 553, 372),
                  S(15, 106, 391, 560, 474)]],
         row_kind='anyN', group=(2, 8), marks=[16], tariff='fixed', total=16,
         notes="The scheme prints 'Any two @ 8 + 8'."),
    # ---- Question 5 --------------------------------------------------------
    dict(key=(5, 'a', 'i'), topic='eng-2-10',
         replaces=NEW + 'gave the process without the drawing the part asks for, and its '
                  'last row ended in the mark "10"',
         why='The roadster frame is photographed beside (a); scheme p15 describes MIG '
             'welding line by line beside a drawing of the torch, shown with the answer; '
             '"10" for the part.',
         lifted=[S(15, 106, 551, 490, 567), S(15, 106, 565, 350, 596),
                 S(15, 106, 596, 296, 610), S(15, 106, 610, 324, 624),
                 S(15, 106, 625, 332, 639), S(15, 106, 639, 243, 653),
                 S(15, 106, 654, 370, 684), S(15, 106, 684, 374, 712),
                 S(15, 106, 713, 411, 727), S(15, 106, 728, 420, 772)],
         tariff='questionTotal', total=10,
         question_figure='engineering-2018-HL-paper-q5ai-art',
         figure='engineering-2018-HL-scheme-q5ai-sol',
         notes="The scheme prints '10'."),
    dict(key=(5, 'a', 'ii'), topic='eng-2-10',
         replaces=NEW + 'read the tariff "Three safety features @ 2 + 2 + 2" as an answer '
                  'row',
         why='Scheme p16 states six features, one a line; "Three safety features @ 2 + 2 '
             '+ 2".',
         lifted=[[S(16, 106, 57, 548, 89), S(16, 106, 91, 295, 105),
                  S(16, 106, 108, 560, 140), S(16, 106, 141, 428, 155),
                  S(16, 106, 158, 430, 172), S(16, 106, 175, 312, 189)]],
         row_kind='anyN', group=(3, 2), marks=[6], tariff='fixed', total=6,
         question_figure='engineering-2018-HL-paper-q5ai-art',
         notes="The scheme prints 'Three safety features @ 2 + 2 + 2'."),
    dict(key=(5, 'c', None),
         why='Paper p8 sets two alternative (c)s either side of an OR. This card is the '
             'first branch, the oxy-acetylene flames, which has no romans; scheme p17 '
             'describes each flame under its name beside drawings of the three, shown '
             'with the answer. "16" for the part.',
         topic='eng-2-10', stem=False,
         question_lift=P(8, *_C5, more=[(126, 470, 390, 540)]),
         lifted=[join(S(17, 70, 225, 146, 241), S(17, 86, 242, 362, 344)),
                 join(S(17, 70, 345, 154, 361), S(17, 86, 362, 356, 430)),
                 join(S(17, 70, 432, 165, 448), S(17, 86, 449, 356, 534))],
         tariff='questionTotal', total=16,
         figure='engineering-2018-HL-scheme-q5c-sol', notes=_OR5),
    # ---- Question 6 --------------------------------------------------------
    dict(key=(6, 'a', 'i'), topic='eng-1-9',
         replaces=NEW + 'described the process without naming it, and without the '
                  'drawing the part asks for',
         why='The roof box is photographed beside (a); scheme p18 names injection '
             'moulding and describes it beside a labelled drawing, shown with the '
             'answer; "8" for the part.',
         lifted=[join(S(18, 106, 86, 204, 102), S(18, 106, 103, 540, 136)),
                 S(18, 106, 286, 368, 302), S(18, 106, 303, 560, 353),
                 S(18, 106, 354, 540, 387), S(18, 106, 387, 556, 420),
                 S(18, 106, 421, 550, 437)],
         tariff='questionTotal', total=8,
         question_figure='engineering-2018-HL-paper-q6ai-art',
         figure='engineering-2018-HL-scheme-q6ai-sol',
         notes="The scheme prints '8'."),
    dict(key=(6, 'b', None), topic='eng-1-9',
         replaces=NEW + 'split two of the five terms into several options each',
         why='A lead-in over five terms set as romans; scheme pp18-20 describe each under '
             'its heading, "Any three @ 6 + 6 + 6".',
         lifted=[[join(S(18, 106, 573, 173, 589), S(18, 105, 590, 534, 639)),
                  join(S(19, 106, 89, 243, 105), S(19, 106, 103, 556, 237)),
                  join(S(19, 106, 438, 261, 454), S(19, 106, 455, 550, 504)),
                  join(S(19, 106, 539, 212, 555), S(19, 106, 556, 560, 589)),
                  join(S(19, 106, 606, 213, 622), S(19, 106, 623, 562, 740),
                       S(20, 106, 57, 548, 90))]],
         row_kind='anyN', group=(3, 6), marks=[18], tariff='fixed', total=18,
         notes="The scheme prints 'Any three @ 6 + 6 + 6'."),
    dict(key=(6, 'c', 'ii'), topic='eng-1-9',
         replaces=NEW + 'set "Explain: 6" and "Reason: 2" as one question total, with the '
                  'mark read into its last row',
         why='Scheme p20 explains extrusion beside a labelled drawing, shown with the '
             'answer, "Explain: 6", and gives the reason on its own line, "Reason: 2".',
         lifted=[join(S(20, 106, 443, 160, 459), S(20, 106, 460, 535, 560)),
                 S(20, 106, 750, 490, 766)],
         marks=[6, 2], total=8,
         question_figure='engineering-2018-HL-paper-q6ci-art',
         figure='engineering-2018-HL-scheme-q6cii-sol',
         notes="The scheme prints 'Explain: 6' and 'Reason: 2'."),
    dict(key=(6, 'c', 'iii'), topic='eng-1-9',
         replaces=NEW + 'read the tariff "Two reasons @ 2 + 2" as an answer row',
         why='Scheme p21 bullets four reasons; "Two reasons @ 2 + 2".',
         lifted=[[S(21, 142, 74, 237, 90), S(21, 142, 89, 194, 105),
                  S(21, 142, 104, 300, 120), S(21, 142, 120, 324, 136)]],
         row_kind='anyN', group=(2, 2), marks=[4], tariff='fixed', total=4,
         question_figure='engineering-2018-HL-paper-q6ci-art',
         notes="The scheme prints 'Two reasons @ 2 + 2'."),
    # ---- Question 7 --------------------------------------------------------
    dict(key=(7, 'a', 'i'), topic='eng-2-11',
         replaces=NEW + 'joined the tariff "Two materials @ 4 + 4" to its last material',
         why='Scheme p21 bullets five materials; "Two materials @ 4 + 4".',
         lifted=[[S(21, 141, 271, 199, 287), S(21, 141, 287, 181, 303),
                  S(21, 141, 302, 170, 318), S(21, 141, 317, 174, 333),
                  S(21, 141, 332, 176, 348)]],
         row_kind='anyN', group=(2, 4), marks=[8], tariff='fixed', total=8,
         question_figure='engineering-2018-HL-paper-q7ai-art',
         notes="The scheme prints 'Two materials @ 4 + 4'."),
    dict(key=(7, 'c', 'i'), topic='eng-2-11', stem=False,
         replaces=NEW + 'carried both OR branches as one question total with no route '
                  'between them',
         why='Both (c)s price their (i) at 8 (scheme pp22-23): loading and glazing beside '
             'drawings of both, shown with the answer, or any two of three CNC terms, '
             '"Any two @ 4 + 4". One card for the printed OR, each branch a route.',
         question_lift=P(10, *_C7A, more=[(126, 471, 545, 504), _ORW7, _C7B,
                                          (126, 628, 390, 713)]),
         lifted=[S(22, 106, 453, 560, 569),
                 [S(23, 106, 337, 553, 369), S(23, 106, 387, 556, 453),
                  S(23, 106, 471, 562, 546)]],
         row_kind='anyN', group=[None, (2, 4)], marks=[8, 8], routes=['a', 'b'],
         tariff='fixed', total=8,
         figure='engineering-2018-HL-scheme-q7ci-sol', notes=_OR7),
    dict(key=(7, 'c', 'ii'), topic='eng-2-11', stem=False,
         replaces=NEW + 'carried both OR branches as one question total, with the tariff '
                  '"Two safety features @ 4 + 4" as an answer row',
         why='Both (c)s price their (ii) at 8 (scheme p23): wheel dressing beside a '
             'drawing of the star dresser, shown with the answer, or two of four CNC '
             'safety features, "Two safety features @ 4 + 4". One card, each branch a '
             'route.',
         question_lift=P(10, *_C7A, more=[(126, 512, 500, 528), _ORW7, _C7B,
                                          (126, 721, 356, 754)]),
         lifted=[S(23, 106, 57, 560, 274),
                 [S(23, 142, 576, 324, 592), S(23, 142, 591, 268, 607),
                  S(23, 142, 607, 236, 623), S(23, 142, 622, 238, 638)]],
         row_kind='anyN', group=[None, (2, 4)], marks=[8, 8], routes=['a', 'b'],
         tariff='fixed', total=8,
         figure='engineering-2018-HL-scheme-q7cii-sol', notes=_OR7),
    # ---- Question 8 --------------------------------------------------------
    dict(key=(8, 'a', 'i'),
         why='The bed is photographed with its mechanism arrowed; scheme p24 describes '
             'the scissor lift in one paragraph beside a labelled drawing, shown with the '
             'answer; "8".',
         topic='eng-2-15',
         lifted=[S(24, 106, 103, 325, 237)], marks=[8], total=8,
         question_figure='engineering-2018-HL-paper-q8a-crop',
         figure='engineering-2018-HL-scheme-q8ai-sol',
         notes="The scheme prints '8'."),
    dict(key=(8, 'a', 'ii'), topic='eng-2-15',
         replaces=NEW + 'gave the linkage without the drawing the part asks for',
         why='Scheme p24 answers in one paragraph over a drawing of the vertical links, '
             'shown with the answer; "8".',
         lifted=[S(24, 106, 311, 560, 343)], marks=[8], total=8,
         question_figure='engineering-2018-HL-paper-q8a-crop',
         figure='engineering-2018-HL-scheme-q8aii-sol',
         notes="The scheme prints '8'."),
    dict(key=(8, 'b', 'v'), topic='eng-2-15',
         replaces=NEW + 'read the drawing\'s captions "No compressed air Compressed air '
                  'applied" as an answer row',
         why='Scheme p25 answers in one paragraph over a drawing of the cylinder with and '
             'without air, shown with the answer; "Any three @ 6 + 6 + 6".',
         lifted=[S(25, 106, 333, 560, 362)], marks=[6], total=6,
         figure='engineering-2018-HL-scheme-q8bv-sol',
         notes="The scheme prints 'Any three @ 6 + 6 + 6'."),
    dict(key=(8, 'c', 'i'),
         why='The golf cruiser branch\'s (i); scheme p25 describes the steering in one '
             'paragraph beside a labelled drawing, shown with the answer; "8".',
         topic='eng-2-15', stem=False,
         question_lift=P(11, *_C8A, more=[(126, 509, 363, 542)]),
         lifted=[S(25, 106, 523, 325, 673)], marks=[8], total=8,
         question_figure='engineering-2018-HL-paper-q8c-crop',
         figure='engineering-2018-HL-scheme-q8ci-sol', notes=_OR8),
    dict(key=(8, 'c', 'ii'), topic='eng-2-15', stem=False,
         replaces=NEW + 'mixed the OR branch\'s heat sink answer among the advantages, '
                  'with the tariff joined to the last advantage',
         why='The golf cruiser branch\'s (ii); scheme p26 bullets four advantages, "Two '
             'advantages @ 4 + 4".',
         question_lift=P(11, *_C8A, more=[(126, 551, 370, 584)]),
         lifted=[[S(26, 141, 74, 296, 90), S(26, 141, 89, 368, 105),
                  S(26, 141, 104, 246, 120), S(26, 141, 120, 344, 136)]],
         row_kind='anyN', group=(2, 4), marks=[8], tariff='fixed', total=8,
         question_figure='engineering-2018-HL-paper-q8c-crop', notes=_OR8),
    dict(key=(8, 'c', 'i'), id='eng-2018-hl-q8-c-i-or', ref_note='IC chips',
         why='The IC chips branch\'s (i), lifted with its cue; scheme p26 bullets four '
             'benefits, "Two benefits @ 2 + 2".',
         topic='eng-2-16', stem=False,
         question_lift=P(11, *_C8B, more=[(126, 657, 323, 673)]),
         lifted=[[S(26, 142, 240, 246, 256), S(26, 142, 255, 211, 271),
                  S(26, 142, 270, 263, 286), S(26, 142, 286, 471, 302)]],
         row_kind='anyN', group=(2, 2), marks=[4], tariff='fixed', total=4,
         notes="The scheme prints 'Two benefits @ 2 + 2'. " + _OR8),
    dict(key=(8, 'c', 'ii'), id='eng-2018-hl-q8-c-ii-or', ref_note='IC chips',
         why='The IC chips branch\'s (ii), lifted with its cue; scheme p26 answers in one '
             'paragraph, "4".',
         topic='eng-2-16', stem=False,
         question_lift=P(11, *_C8B, more=[(126, 681, 354, 714)]),
         lifted=[S(26, 106, 345, 550, 395)], marks=[4], total=4,
         notes="The scheme prints '4'. " + _OR8),
    dict(key=(8, 'c', 'iii'), ref_note='IC chips', topic='eng-2-16', stem=False,
         replaces=NEW + 'set the list as one row and read the tariff "Two output '
                  'components @ 4 + 4" as a second',
         why='The IC chips branch\'s (iii), the only (iii) the paper sets, lifted with its '
             'cue; scheme p26 lists the components in one line, each lifted by its own '
             'word rectangle. "Two output components @ 4 + 4".',
         question_lift=P(11, *_C8B, more=[(126, 720, 363, 754)]),
         lifted=[[S(26, 245, 425, 270, 441), S(26, 270, 425, 302, 441),
                  S(26, 302, 425, 343, 441), S(26, 343, 425, 404, 441),
                  S(26, 404, 425, 436, 441)]],
         row_kind='anyN', group=(2, 4), marks=[8], tariff='fixed', total=8,
         notes="The scheme prints 'Two output components @ 4 + 4'. " + _OR8),
]

TOPICS = {
    'eng-2018-hl-q5-c-i': ('eng-3-14', 'robotic lawn mowers are robotics, which the syllabus '
                           'places under Technology; "sensors" outvoted it for electronics'),
}

_EQ = ('read off the iron-carbon diagram the part is printed under; the card\'s syllabus '
       'heading is Iron and steel.')
_ROB = 'Energy, Electronics & Robotics'

ATLAS = {
    'eng-2018-hl-q3-b-i': dict(topics=['Equilibrium Diagrams'],
                               note='The transformations along lines A and B, ' + _EQ),
    'eng-2018-hl-q3-b-ii': dict(topics=['Equilibrium Diagrams'],
                                note='The eutectoid point C, ' + _EQ),
    'eng-2018-hl-q3-b-iii': dict(
        topics=['Heat Treatment'],
        note='Annealing 1.2% carbon steel, a heat treatment, set under the iron-carbon '
             'diagram; the card\'s syllabus heading is Iron and steel.'),
    'eng-2018-hl-q5-c-i': dict(
        topics=[_ROB],
        note='Robotic lawn mowers (the OR branch of Q5(c)); the card\'s syllabus heading '
             'is Technology, where the syllabus places robotics.'),
    'eng-2018-hl-q5-c-ii': dict(
        topics=[_ROB],
        note='Robotic lawn mowers (the OR branch of Q5(c)); the card\'s syllabus heading '
             'is Technology, where the syllabus places robotics.'),
}
