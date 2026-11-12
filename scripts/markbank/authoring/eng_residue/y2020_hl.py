"""2020 Higher Level: the parts eng_all refuses or gets wrong, from the page.

Paper and scheme as the PDFs number their pages. The marks grid is on scheme
p3: Question 1 is Section A, "Any ten @ 5 marks each", and Section B, "Answer
all of the following", (n) to (r); Questions 2-8 are 50 marks each. The scheme
prints a part's marks once, under its answer ("3 + 2", "Any two @ 3 + 3"),
not beside each line. This sitting had no cards before the lane: every card
here is new, and a `replaces=` names the automatic card it rebuilds before it
ever shipped.
"""
from eng_lift import join, lift

Y, L = 2020, 'hl'
NEW = 'never shipped: the automatic card '
OWNED = ('never shipped: the automatic author builds this card only from the lifts this '
         'entry records, so the entry owns it')


def S(page, *rect):
    return lift(Y, L, 'scheme', page, rect)


def P(page, *rect, more=()):
    return lift(Y, L, 'paper', page, rect, more=more)


# Paper p4: Section B's (n) stimulus.
_N1 = (97, 100, 409, 158)
# Paper p8: Question 5's OR branch cue; p10: Question 7's; p11: Question 8's.
_C5B = (97, 596, 517, 629)
_C7A = (97, 425, 436, 441)
_C7B = (97, 614, 539, 647)
_C8A = (97, 426, 348, 476)
_C8B = (97, 622, 492, 655)
_OR7P = (283, 568, 304, 584)
_OR8P = (283, 593, 304, 609)
# Scheme p22-23: the cordless tool's advantage and disadvantage headings.
_ADV8 = (22, 106, 645, 291, 661)
_DIS8 = (23, 106, 72, 305, 88)
# Scheme p24: the PV panels' headings.
_ADVPV = (24, 106, 424, 309, 440)
_DISPV = (24, 70, 584, 263, 600)
# Scheme p10: the comparison table's column heads.
_XR = (10, 150, 150, 215, 166)
_US = (10, 389, 150, 470, 166)

_OR5 = ('The paper sets two (c)s either side of an OR: the submerged arc welding (c), '
        'answered at the letter for 16, and the robotic cleaner (c), whose (i) and (ii) '
        'are 4 + 4 each.')
_OR7 = ('The paper sets two (c)s either side of an OR, the camera handle and CNC '
        'technology; the scheme prices them differently ((i) 3 + 3 + 3 against 4 + 4, '
        '(ii) 7 against 4 + 4), so each branch is a card of its own.')
_OR8 = ('The paper sets two (c)s either side of an OR, the surveillance vehicle and the '
        'photovoltaic panels; the scheme prices each (i) and each (ii) at 8.')

CROPS = {
    # ---- paper ------------------------------------------------------------
    'engineering-2020-HL-paper-q1d-crop': dict(
        doc='paper', page=3, rect=(438, 262, 566, 429), mask=[(436, 403, 458, 423)],
        ref='2020 HL Q1(d)'),
    'engineering-2020-HL-paper-q1o-crop': dict(
        doc='paper', page=4, rect=(322, 272, 538, 378), ref='2020 HL Q1(o)'),
    'engineering-2020-HL-paper-q2b-crop': dict(
        doc='paper', page=5, rect=(110, 388, 542, 434), ref='2020 HL Q2(b)'),
    'engineering-2020-HL-paper-q3b-crop': dict(
        doc='paper', page=6, rect=(75, 280, 495, 509), ref='2020 HL Q3(b)',
        letters=('A', 'B', 'C', 'D')),
    'engineering-2020-HL-paper-q4b-crop': dict(
        doc='paper', page=7, rect=(50, 336, 562, 413), ref='2020 HL Q4(b)'),
    'engineering-2020-HL-paper-q5c-crop': dict(
        doc='paper', page=8, rect=(362, 437, 564, 556), ref='2020 HL Q5(c)'),
    'engineering-2020-HL-paper-q7c-or-crop': dict(
        doc='paper', page=10, rect=(390, 640, 556, 769), mask=[(388, 655, 422, 675)],
        ref='2020 HL Q7(c)(i) — CNC technology'),
    # The saw without the "d" of the ask beside it (the automatic crop's).
    'engineering-2020-HL-paper-q8a-crop': dict(
        doc='paper', page=11, rect=(389, 130, 566, 220), ref='2020 HL Q8(a)'),
    # The surveillance vehicle beside the PV beacon, the two (c)s' pictures.
    'engineering-2020-HL-paper-q8c-crop': dict(
        doc='paper', page=11, parts=[(11, (367, 386, 566, 579)),
                                     (11, (386, 640, 503, 792))],
        layout='row', ref='2020 HL Q8(c)'),
    # ---- scheme: the drawings the answers are given with -------------------
    'engineering-2020-HL-scheme-q1f-sol': dict(
        doc='scheme', page=5, rect=(330, 78, 562, 206),
        mask=[(328, 86, 364, 158)], solution=True, ref='2020 HL Q1(f)'),
    'engineering-2020-HL-scheme-q1g-sol': dict(
        doc='scheme', page=5, rect=(330, 230, 552, 330), solution=True,
        ref='2020 HL Q1(g)'),
    'engineering-2020-HL-scheme-q2ai-sol': dict(
        doc='scheme', page=8, parts=[(8, (388, 482, 584, 632)),
                                     (8, (366, 680, 550, 753)),
                                     (9, (408, 62, 564, 146))],
        solution=True, ref='2020 HL Q2(a)(i)'),
    # Scheme p9: one graph answers (b)(i) and (ii). (i)'s plot is shown with the
    # band of region labels and arrows above the curve whited out, (ii)'s with
    # them: two answers, two crops.
    'engineering-2020-HL-scheme-q2bi-sol': dict(
        doc='scheme', page=9, rect=(128, 432, 525, 676),
        mask=[(170, 432, 526, 471)],
        solution=True, ref='2020 HL Q2(b)(i)'),
    'engineering-2020-HL-scheme-q2bii-sol': dict(
        doc='scheme', page=9, rect=(128, 432, 525, 676), solution=True,
        ref='2020 HL Q2(b)(ii)'),
    'engineering-2020-HL-scheme-q2biii-sol': dict(
        doc='scheme', page=10, rect=(104, 70, 498, 106), solution=True,
        ref='2020 HL Q2(b)(iii)'),
    'engineering-2020-HL-scheme-q2c-sol': dict(
        doc='scheme', page=10, rect=(74, 208, 552, 356), solution=True,
        ref='2020 HL Q2(c)'),
    'engineering-2020-HL-scheme-q3cii-sol': dict(
        doc='scheme', page=12, rect=(110, 196, 530, 466), solution=True,
        ref='2020 HL Q3(c)(ii)'),
    # Scheme p13: the diagram for (b)(i); for (ii), the same diagram with the
    # ratio printed under it, read off its A, B and C.
    'engineering-2020-HL-scheme-q4bi-sol': dict(
        doc='scheme', page=13, rect=(88, 300, 548, 545), solution=True,
        ref='2020 HL Q4(b)(i)'),
    'engineering-2020-HL-scheme-q4bii-sol': dict(
        doc='scheme', page=13, rect=(88, 300, 548, 596), solution=True,
        ref='2020 HL Q4(b)(ii)'),
    'engineering-2020-HL-scheme-q4biii-sol': dict(
        doc='scheme', page=13, rect=(225, 630, 476, 760), solution=True,
        ref='2020 HL Q4(b)(iii)'),
    'engineering-2020-HL-scheme-q5ai-sol': dict(
        doc='scheme', page=14, rect=(24, 536, 590, 750), mask=[(544, 728, 568, 750)],
        solution=True,
        ref='2020 HL Q5(a)(i)'),
    'engineering-2020-HL-scheme-q5c-sol': dict(
        doc='scheme', page=16, rect=(350, 88, 550, 280), solution=True,
        ref='2020 HL Q5(c)'),
    'engineering-2020-HL-scheme-q6ai-sol': dict(
        doc='scheme', page=17, rect=(86, 240, 522, 396), solution=True,
        ref='2020 HL Q6(a)(i)'),
    'engineering-2020-HL-scheme-q6bii-sol': dict(
        doc='scheme', page=18, rect=(280, 92, 564, 228), solution=True,
        ref='2020 HL Q6(b)(ii)'),
    'engineering-2020-HL-scheme-q6biv-sol': dict(
        doc='scheme', page=18, rect=(60, 390, 572, 658), solution=True,
        ref='2020 HL Q6(b)(iv)'),
    'engineering-2020-HL-scheme-q6cii-sol': dict(
        doc='scheme', page=19, rect=(92, 160, 545, 296), solution=True,
        ref='2020 HL Q6(c)(ii)'),
    'engineering-2020-HL-scheme-q7ai-sol': dict(
        doc='scheme', page=19, rect=(410, 490, 548, 732), solution=True,
        ref='2020 HL Q7(a)(i)'),
    'engineering-2020-HL-scheme-q7ci-sol': dict(
        doc='scheme', page=21, rect=(84, 68, 580, 394), solution=True,
        ref='2020 HL Q7(c)(i)'),
    'engineering-2020-HL-scheme-q7cii-sol': dict(
        doc='scheme', page=21, rect=(372, 434, 580, 694), solution=True,
        ref='2020 HL Q7(c)(ii)'),
    'engineering-2020-HL-scheme-q8ai-sol': dict(
        doc='scheme', page=22, rect=(80, 440, 565, 620), solution=True,
        ref='2020 HL Q8(a)(i)'),
    'engineering-2020-HL-scheme-q8bi-sol': dict(
        doc='scheme', page=23, rect=(415, 204, 574, 302), solution=True,
        ref='2020 HL Q8(b)(i)'),
    'engineering-2020-HL-scheme-q8bv-sol': dict(
        doc='scheme', page=23, rect=(145, 582, 478, 684), solution=True,
        ref='2020 HL Q8(b)(v)'),
    'engineering-2020-HL-scheme-q8ci-sol': dict(
        doc='scheme', page=24, rect=(355, 64, 560, 192), solution=True,
        ref='2020 HL Q8(c)(i)'),
    'engineering-2020-HL-scheme-q8cii-sol': dict(
        doc='scheme', page=24, rect=(368, 200, 523, 331), solution=True,
        ref='2020 HL Q8(c)(ii)'),
}

CARDS = [
    # ---- Question 1, Section A ("Any ten @ 5 marks each") ------------------
    dict(key=(1, 'a', None),
         why='Scheme p4 answers in one line, "5".',
         topic='eng-3-14',
         lifted=[S(4, 70, 190, 245, 206)], marks=[5], total=5,
         notes="The scheme prints '5'."),
    dict(key=(1, 'b', None),
         why='Scheme p4 answers in one paragraph, "5".',
         topic='eng-3-14',
         lifted=[S(4, 70, 241, 545, 307)], marks=[5], total=5,
         notes="The scheme prints '5'."),
    dict(key=(1, 'c', None),
         why='Scheme p4 gives a paragraph on each of the three, "Any one @ 5".',
         topic='eng-3-14',
         question_lift=P(3, 100, 232, 489, 265),
         lifted=[[S(4, 106, 359, 560, 425), S(4, 106, 443, 556, 476),
                  S(4, 105, 494, 562, 543)]],
         row_kind='anyN', group=(1, 5), marks=[5], tariff='fixed', total=5,
         notes="The scheme prints 'Any one @ 5'."),
    dict(key=(1, 'd', None),
         why='The wheelchair is photographed with its castors labelled beside (d); '
             'scheme p4 answers in one sentence, "5".',
         topic='eng-2-15',
         lifted=[S(4, 70, 595, 364, 644)], marks=[5], total=5,
         question_figure='engineering-2020-HL-paper-q1d-crop',
         notes="The scheme prints '5'."),
    dict(key=(1, 'e', None),
         why='Scheme p4 answers in one line, "5".',
         topic='eng-3-12',
         lifted=[S(4, 70, 713, 492, 729)], marks=[5], total=5,
         notes="The scheme prints '5'."),
    dict(key=(1, 'f', None),
         why='Scheme p5 answers in three bullets beside a labelled diagram, which is '
             'shown with the answer; "5" for the part.',
         topic='eng-1-2',
         lifted=[S(5, 96, 88, 346, 123), S(5, 96, 122, 363, 157),
                 S(5, 96, 157, 330, 191)],
         tariff='questionTotal', total=5,
         figure='engineering-2020-HL-scheme-q1f-sol',
         notes="The scheme prints '5'."),
    dict(key=(1, 'g', None),
         why='Scheme p5 answers in two sentences beside drawings of both structures, '
             'which are shown with the answer; "5" for the part.',
         topic='eng-1-3',
         lifted=[S(5, 70, 243, 324, 276), S(5, 70, 276, 302, 309)],
         tariff='questionTotal', total=5,
         figure='engineering-2020-HL-scheme-q1g-sol',
         notes="The scheme prints '5'."),
    dict(key=(1, 'h', None),
         why='Scheme p5 suggests the material and lists four properties; "3 + 1 + 1": '
             'the material 3, then any two properties at 1 each.',
         topic='eng-1-9',
         lifted=[S(5, 70, 344, 456, 360),
                 [S(5, 96, 359, 230, 377), S(5, 96, 377, 200, 395),
                  S(5, 96, 394, 407, 412), S(5, 96, 412, 533, 447)]],
         row_kind='anyN', group=[None, (2, 1)], marks=[3, 2], tariff='fixed', total=5,
         notes="The scheme prints '3 + 1 + 1'."),
    dict(key=(1, 'i', None),
         why='Scheme p5 answers in one sentence over two lines, "5".',
         topic='eng-1-9',
         lifted=[S(5, 70, 481, 522, 514)], marks=[5], total=5,
         notes="The scheme prints '5'."),
    dict(key=(1, 'j', None),
         why='Scheme p5 names the properties inside one sentence; each is lifted by its '
             'own word rectangle. "3 + 2" for two.',
         topic='eng-1-5',
         lifted=[join(S(5, 471, 549, 537, 565), S(5, 70, 565, 120, 581)),
                 S(5, 212, 565, 311, 581), S(5, 355, 565, 499, 581)],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         notes="The scheme prints '3 + 2'."),
    dict(key=(1, 'k', None),
         why='Scheme p5 lists four benefits under a heading, "3 + 2" for two.',
         topic='eng-3-14',
         lifted=[S(5, 96, 632, 416, 649), S(5, 96, 649, 299, 667),
                 S(5, 96, 667, 326, 684), S(5, 96, 684, 170, 702)],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         notes="The scheme prints '3 + 2'."),
    dict(key=(1, 'l', None),
         why='The Formula E car is photographed beside (l). Scheme p6 answers in one '
             'paragraph naming two factors, lightweight robust materials (with why) '
             'and strength to weight ratio with impact resistance; each is lifted by '
             'word rectangle. "3 + 2".',
         topic='eng-3-14',
         lifted=[join(S(6, 70, 72, 548, 88), S(6, 70, 89, 121, 105),
                      S(6, 307, 106, 548, 122), S(6, 70, 123, 545, 139),
                      S(6, 70, 140, 150, 156)),
                 join(S(6, 122, 89, 556, 105), S(6, 70, 106, 307, 122))],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         question_figure='engineering-2020-HL-paper-q1l-art',
         notes="The scheme prints '3 + 2'."),
    dict(key=(1, 'm', None),
         why='Scheme p6 lists four materials under a heading, "3 + 2" for two. The '
             'reader files the Section B heading printed after (m) as its stem, so the '
             'card carries none.',
         topic='eng-3-14', stem=False,
         lifted=[S(6, 96, 206, 232, 223), S(6, 96, 223, 209, 241),
                 S(6, 96, 241, 197, 258), S(6, 96, 258, 146, 276)],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         question_figure='engineering-2020-HL-paper-q1l-art',
         notes="The scheme prints '3 + 2'."),
    # ---- Question 1, Section B ("Answer all of the following") -------------
    dict(key=(1, 'n', 'i'),
         why='Section B. Scheme p6 answers under the term in one paragraph; (n) is '
             '"5 + 5". The question is lifted with (n)\'s stimulus.',
         topic='eng-3-14', stem=False,
         question_lift=P(4, *_N1, more=[(118, 170, 314, 186)]),
         lifted=[S(6, 106, 361, 558, 411)], marks=[5], total=5,
         notes="The scheme prints '5 + 5' for (n)."),
    dict(key=(1, 'n', 'ii'),
         why='Section B. Scheme p6 answers industry and agriculture in one block, '
             'priced as the part; (n) is "5 + 5".',
         topic='eng-3-14', stem=False,
         question_lift=P(4, *_N1, more=[(118, 188, 354, 222)]),
         lifted=[S(6, 106, 412, 560, 495), S(6, 106, 496, 557, 546)],
         tariff='questionTotal', total=5,
         notes="The scheme prints '5 + 5' for (n)."),
    dict(key=(1, 'o', None),
         why='Section B. The car is drawn with its sensors labelled beside (o); scheme '
             'pp6-7 explain each feature under its name, each lifted with its name, '
             '"4 + 3 + 3". The reader '
             'takes the drawing\'s labels for part of the question, so it is lifted '
             'from its own lines.',
         topic='eng-2-16', stem=False,
         question_lift=P(4, 97, 258, 465, 274, more=[(97, 284, 186, 334)]),
         lifted=[S(6, 106, 580, 560, 664), S(6, 106, 665, 560, 714),
                 join(S(6, 106, 715, 562, 765), S(7, 106, 72, 544, 105))],
         marks=[4, 3, 3], total=10,
         question_figure='engineering-2020-HL-paper-q1o-crop',
         notes="The scheme prints '4 + 3 + 3'."),
    dict(key=(1, 'p', None),
         why='Section B. Scheme p7 describes each under its name, "5 + 5".',
         topic='eng-3-14', stem=False,
         question_lift=P(4, 97, 394, 490, 424, more=[(97, 433, 256, 465)]),
         lifted=[S(7, 106, 140, 564, 240), S(7, 106, 258, 558, 375)],
         marks=[5, 5], total=10,
         notes="The scheme prints '5 + 5'."),
    dict(key=(1, 'q', None),
         why='Section B. Scheme p7 describes each level under its name, "Any two @ 5 + '
             '5"; each answer is lifted with its name.',
         topic='eng-3-14', stem=False,
         question_lift=P(4, 88, 524, 478, 558, more=[(97, 566, 292, 620)]),
         lifted=[[S(7, 106, 409, 524, 476), S(7, 106, 477, 564, 526),
                  S(7, 106, 527, 539, 594)]],
         row_kind='anyN', group=(2, 5), marks=[10], tariff='fixed', total=10,
         notes="The scheme prints 'Any two @ 5 + 5'."),
    dict(key=(1, 'r', None),
         why='Section B. Scheme pp7-8 discuss each under its name, "Any two @ 5 + 5"; '
             'each answer is lifted with its name.',
         topic='eng-3-14', stem=False,
         question_lift=P(4, 97, 656, 349, 687, more=[(97, 695, 233, 745)]),
         lifted=[[S(7, 106, 628, 556, 745), S(8, 106, 72, 563, 341),
                  S(8, 106, 342, 557, 425)]],
         row_kind='anyN', group=(2, 5), marks=[10], tariff='fixed', total=10,
         notes="The scheme prints 'Any two @ 5 + 5'."),
    # ---- Question 2 --------------------------------------------------------
    dict(key=(2, 'a', 'i'),
         why='Scheme pp8-9 describe the impact test and then the Izod and Charpy tests '
             'in bullets beside their drawings, which are shown with the answer; "10" '
             'for the part.',
         topic='eng-3-8',
         lifted=[S(8, 105, 494, 387, 627),
                 join(S(8, 106, 645, 160, 661), S(8, 128, 662, 380, 762)),
                 join(S(9, 106, 72, 172, 88), S(9, 128, 89, 395, 189))],
         tariff='questionTotal', total=10,
         figure='engineering-2020-HL-scheme-q2ai-sol',
         notes="The scheme prints '10'."),
    dict(key=(2, 'a', 'ii'),
         replaces=NEW + 'gave the three definitions without the property each defines',
         why='Scheme p9 defines each property under its name; each is lifted with its '
             'name. "2 + 2 + 2".',
         lifted=[join(S(9, 106, 224, 228, 240), S(9, 106, 241, 327, 257)),
                 join(S(9, 106, 275, 200, 291), S(9, 106, 291, 397, 307)),
                 join(S(9, 106, 325, 190, 341), S(9, 105, 342, 422, 375))],
         marks=[2, 2, 2], total=6,
         notes="The scheme prints '2 + 2 + 2'."),
    dict(key=(2, 'b', 'i'),
         why='Scheme p9 answers the plot with the load-extension graph and prints no '
             'words; the graph is shown with the answer. "10". The results table is '
             'shown as printed.',
         topic='eng-3-8', stem=False,
         question_lift=P(5, 97, 339, 498, 372, more=[(127, 451, 448, 467)]),
         special={'kind': 'ask'}, total=10,
         question_figure='engineering-2020-HL-paper-q2b-crop',
         figure='engineering-2020-HL-scheme-q2bi-sol',
         notes="The scheme prints '10'."),
    dict(key=(2, 'b', 'ii'),
         why='Scheme p9 names the three regions in one line under the graph, "shown on '
             'graph"; each is lifted by word rectangle and the graph is shown with the '
             'answer. "2 + 2 + 2".',
         topic='eng-3-8', stem=False,
         question_lift=P(5, 97, 339, 498, 372, more=[(126, 479, 387, 547)]),
         lifted=[S(9, 106, 729, 177, 745), S(9, 177, 729, 245, 745),
                 S(9, 266, 729, 341, 745)],
         marks=[2, 2, 2], total=6,
         question_figure='engineering-2020-HL-paper-q2b-crop',
         figure='engineering-2020-HL-scheme-q2bii-sol',
         notes="The scheme prints '2 + 2 + 2'."),
    dict(key=(2, 'b', 'iii'),
         replaces=NEW + 'carried the results table as a line of numbers for a stem and '
                  'took the bottom of a stacked fraction, "C.S.A. π. (5²)", for its '
                  'answer',
         why='Scheme p10 sets U.T.S. = Max. Load / C.S.A. = 108kN / π.(5²) = '
             '1.38kN/mm² as stacked fractions, shown as printed; "2".',
         special={'kind': 'ask'}, total=2, stem=False,
         question_lift=P(5, 97, 339, 498, 372, more=[(126, 560, 469, 576)]),
         question_figure='engineering-2020-HL-paper-q2b-crop',
         figure='engineering-2020-HL-scheme-q2biii-sol',
         notes="The scheme prints '2'."),
    dict(key=(2, 'c', None),
         replaces=NEW + 'read the scheme\'s two-column table across, welding the X-ray '
                  'and ultrasonic answers into one another',
         why='Scheme p10 answers in a two-column table, X-ray beside ultrasonic; each '
             'cell is lifted by its own rectangle with its column head. The equipment '
             'row is drawings only, shown with the answer. "16".',
         lifted=[join(S(*_XR), S(10, 75, 413, 293, 605)),
                 join(S(*_US), S(10, 300, 428, 557, 547)),
                 join(S(*_XR), S(10, 75, 648, 285, 708)),
                 join(S(*_US), S(10, 300, 648, 558, 693))],
         tariff='questionTotal', total=16,
         figure='engineering-2020-HL-scheme-q2c-sol',
         notes="The scheme prints '16'."),
    # ---- Question 3 --------------------------------------------------------
    dict(key=(3, 'a', 'i'),
         replaces=NEW + 'gave the two processes without the names "Hardening" and '
                  '"Tempering", so its rows read as two descriptions of one process',
         why='Scheme p11 describes each process under its name; each is lifted with '
             'its name. "10".',
         lifted=[join(S(11, 106, 106, 170, 122), S(11, 106, 123, 553, 173)),
                 join(S(11, 106, 173, 170, 189), S(11, 106, 190, 542, 240))],
         tariff='questionTotal', total=10,
         notes="The scheme prints '10'."),
    dict(key=(3, 'a', 'ii'),
         replaces=NEW + 'set "Any two @ 3 + 3" over one row holding both reasons',
         why='Scheme p11 gives the two reasons in one sentence, either side of "but"; '
             'each is lifted by word rectangle. "Any two @ 3 + 3".',
         lifted=[S(11, 106, 287, 522, 303), S(11, 106, 304, 420, 320)],
         marks=[3, 3], total=6,
         notes="The scheme prints 'Any two @ 3 + 3'."),
    dict(key=(3, 'b', 'i'),
         why='The equilibrium diagram is printed with its regions lettered A-D; scheme '
             'p11 names each, "2 + 2 + 2 + 2".',
         topic='eng-2-6', stem=False,
         lifted=[S(11, 106, 354, 190, 370), S(11, 105, 371, 185, 387),
                 S(11, 105, 388, 176, 404), S(11, 105, 405, 243, 421)],
         marks=[2, 2, 2, 2], total=8,
         question_figure='engineering-2020-HL-paper-q3b-crop',
         labels={'A': S(11, 124, 354, 190, 370), 'B': S(11, 123, 371, 185, 387),
                 'C': S(11, 123, 388, 176, 404), 'D': S(11, 123, 405, 243, 421)},
         notes="The scheme prints '2 + 2 + 2 + 2'."),
    dict(key=(3, 'b', 'ii'),
         why='The 0.5% carbon line is marked on the diagram; scheme p11 answers in one '
             'paragraph, "6".',
         topic='eng-2-6', stem=False,
         lifted=[S(11, 106, 455, 557, 539)], marks=[6], total=6,
         question_figure='engineering-2020-HL-paper-q3b-crop',
         notes="The scheme prints '6'."),
    dict(key=(3, 'b', 'iii'),
         replaces=NEW + 'carried the diagram\'s axis numbers as its stem',
         why='Scheme p11 answers in one line, "4".',
         stem=False,
         lifted=[S(11, 106, 573, 383, 589)], marks=[4], total=4,
         notes="The scheme prints '4'."),
    dict(key=(3, 'c', 'ii'),
         replaces=NEW + 'gave the description without the drawing the part asks for',
         why='Scheme p12 describes the pyrometer and draws it with the three filament '
             'readings; the drawing is shown with the answer. "10".',
         lifted=[S(12, 106, 89, 556, 189)], marks=[10], total=10,
         figure='engineering-2020-HL-scheme-q3cii-sol',
         notes="The scheme prints '10'."),
    # ---- Question 4 --------------------------------------------------------
    dict(key=(4, 'a', 'i'),
         replaces=NEW + 'showed (a)(ii)\'s two structures, which (a)(i) does not use',
         why='Scheme p12 answers in one paragraph, "4".',
         lifted=[S(12, 106, 581, 556, 631)], marks=[4], total=4,
         notes="The scheme prints '4'."),
    dict(key=(4, 'a', 'ii'),
         replaces=NEW + 'repeated structure A in its second row',
         why='The two structures are drawn and captioned A and B beside (a); scheme '
             'p12 names each, "2 + 2".',
         lifted=[S(12, 106, 665, 245, 681), S(12, 106, 682, 241, 698)],
         marks=[2, 2], total=4,
         question_figure='engineering-2020-HL-paper-q4ai-art',
         labels={'A': S(12, 120, 665, 245, 681), 'B': S(12, 120, 682, 241, 698)},
         notes="The scheme prints '2 + 2'."),
    dict(key=(4, 'a', 'iii'),
         why='Scheme p13 describes each structure under its name ("BCC Structure", '
             '"FCC Structure"); each is lifted with its name. "4 + 4".',
         topic='eng-1-3',
         lifted=[S(13, 106, 72, 427, 156),
                 join(S(13, 69, 176, 143, 192), S(13, 106, 193, 434, 276))],
         marks=[4, 4], total=8,
         question_figure='engineering-2020-HL-paper-q4ai-art',
         labels={'A': S(13, 106, 72, 181, 88), 'B': S(13, 69, 176, 143, 192)},
         notes="The scheme prints '4 + 4'."),
    dict(key=(4, 'b', 'i'),
         why='Scheme p13 answers with the equilibrium diagram drawn and its liquidus '
             'and solidus lines labelled, and prints no other words; the diagram is '
             'shown with the answer. "10". The table is shown as printed.',
         topic='eng-1-3', stem=False,
         question_lift=P(7, 97, 305, 537, 321, more=[(97, 427, 260, 443),
                                                    (126, 455, 540, 488)]),
         special={'kind': 'ask'}, total=10,
         question_figure='engineering-2020-HL-paper-q4b-crop',
         figure='engineering-2020-HL-scheme-q4bi-sol',
         notes="The scheme prints '10'."),
    dict(key=(4, 'b', 'ii'),
         why='Scheme p13 reads the ratio off the diagram at A, B and C in one line; the '
             'diagram is shown with the answer. "4".',
         topic='eng-1-3', stem=False,
         question_lift=P(7, 97, 305, 537, 321, more=[(97, 427, 260, 443),
                                                    (126, 500, 503, 532)]),
         lifted=[S(13, 106, 578, 338, 594)], marks=[4], total=4,
         question_figure='engineering-2020-HL-paper-q4b-crop',
         figure='engineering-2020-HL-scheme-q4bii-sol',
         notes="The scheme prints '4'."),
    dict(key=(4, 'b', 'iii'),
         why='Scheme p13 answers with a cooling curve and prints no words beyond its '
             'labels; the curve is shown with the answer. "4".',
         topic='eng-1-3', stem=False,
         question_lift=P(7, 97, 305, 537, 321, more=[(97, 427, 260, 443),
                                                    (126, 544, 479, 577)]),
         special={'kind': 'ask'}, total=4,
         question_figure='engineering-2020-HL-paper-q4b-crop',
         figure='engineering-2020-HL-scheme-q4biii-sol',
         notes="The scheme prints '4'."),
    dict(key=(4, 'c', None),
         replaces=NEW + 'read (i)\'s two columns across, "the alloying atoms replace the '
                  'the alloying atoms fit in between"',
         why='Scheme p14 answers (i) in two columns under their heads, each column '
             'lifted by its own rectangle; (ii) and (iii) in paragraphs. "Any two @ 8 + '
             '8".',
         topic='eng-1-3',
         lifted=[[join(S(14, 106, 72, 312, 88), S(14, 72, 89, 262, 122),
                       S(14, 322, 72, 452, 88), S(14, 322, 89, 489, 122)),
                  S(14, 106, 200, 550, 260),
                  join(S(14, 106, 276, 227, 292), S(14, 106, 290, 547, 336))]],
         row_kind='anyN', group=(2, 8), marks=[16], tariff='fixed', total=16,
         notes="The scheme prints 'Any two @ 8 + 8'."),
    # ---- Question 5 --------------------------------------------------------
    dict(key=(5, 'a', 'i'),
         replaces=NEW + 'carried the diagram\'s label "Wire reel" as an answer and not '
                  'the diagram',
         why='The roll cage is photographed beside (a); scheme p14 describes MIG '
             'welding in one paragraph over a labelled diagram, which is shown with '
             'the answer. "10".',
         lifted=[join(S(14, 106, 419, 182, 435), S(14, 106, 435, 552, 536))],
         marks=[10], total=10,
         question_figure='engineering-2020-HL-paper-q5ai-art',
         figure='engineering-2020-HL-scheme-q5ai-sol',
         notes="The scheme prints '10'."),
    dict(key=(5, 'c', None),
         why='Paper p8 sets two alternative (c)s either side of an OR. This card is the '
             'first branch, submerged arc welding, which has no romans; scheme p16 '
             'describes it in one paragraph and its applications in another beside a '
             'labelled diagram, shown with the answer. "16".',
         topic='eng-2-10', stem=False,
         question_lift=P(8, 97, 461, 360, 511),
         lifted=[S(16, 69, 89, 333, 257), S(16, 69, 258, 332, 307)],
         tariff='questionTotal', total=16,
         question_figure='engineering-2020-HL-paper-q5c-crop',
         figure='engineering-2020-HL-scheme-q5c-sol', notes=_OR5),
    dict(key=(5, 'c', 'i'),
         replaces=NEW + 'carried one sensor\'s answer without its name and the other\'s '
                  'with it, and did not say the part is the OR branch',
         why='The OR branch\'s (i), lifted with its cue; scheme p16 explains each sensor '
             'under its name, "4 + 4".',
         topic='eng-2-16', stem=False,
         question_lift=P(8, *_C5B, more=[(126, 641, 393, 691)]),
         lifted=[join(S(16, 106, 376, 205, 392), S(16, 106, 390, 549, 423)),
                 S(16, 106, 424, 564, 474)],
         marks=[4, 4], total=8, notes=_OR5),
    dict(key=(5, 'c', 'ii'),
         replaces=NEW + 'set "4 + 4" over five equal options as an ordered split',
         why='The OR branch\'s (ii), lifted with its cue; scheme p16 lists five '
             'advantages, "4 + 4" for any two.',
         topic='eng-3-14', stem=False,
         question_lift=P(8, *_C5B, more=[(126, 700, 388, 733)]),
         lifted=[[S(16, 132, 524, 305, 541), S(16, 132, 539, 394, 556),
                  S(16, 132, 554, 348, 571), S(16, 132, 570, 476, 587),
                  S(16, 132, 585, 514, 617)]],
         row_kind='anyN', group=(2, 4), marks=[8], tariff='fixed', total=8,
         notes=_OR5),
    # ---- Question 6 --------------------------------------------------------
    dict(key=(6, 'a', 'i'),
         replaces=NEW + 'described the process without naming it, and without the '
                  'diagram the part asks for',
         why='Scheme p17 names injection moulding and describes it in bullets over a '
             'labelled diagram, which is shown with the answer. "10".',
         lifted=[S(17, 106, 106, 210, 122), S(17, 130, 122, 504, 140),
                 S(17, 130, 139, 338, 157), S(17, 130, 157, 318, 175),
                 S(17, 130, 174, 562, 192), S(17, 130, 192, 536, 210)],
         tariff='questionTotal', total=10,
         figure='engineering-2020-HL-scheme-q6ai-sol',
         notes="The scheme prints '10'."),
    dict(key=(6, 'b', 'ii'), replaces=OWNED,
         why='Scheme p18 explains addition polymerisation in one paragraph beside a '
             'labelled diagram of the monomers, shown with the answer; "Any three @ 6 '
             '+ 6 + 6".',
         lifted=[join(S(18, 105, 89, 306, 240), S(18, 105, 241, 561, 307))],
         marks=[6], total=6,
         figure='engineering-2020-HL-scheme-q6bii-sol',
         notes="The scheme prints 'Any three @ 6 + 6 + 6'."),
    dict(key=(6, 'b', 'iv'),
         why='Scheme p18 answers with six captioned drawings of the process and no other '
             'words; each caption is lifted by its own rectangle and the drawings are '
             'shown with the answer. "Any three @ 6 + 6 + 6".',
         lifted=[S(18, 69, 488, 205, 504), S(18, 243, 489, 379, 505),
                 S(18, 393, 489, 559, 518), S(18, 69, 615, 213, 644),
                 S(18, 237, 615, 383, 643), S(18, 410, 615, 552, 657)],
         tariff='questionTotal', total=6,
         figure='engineering-2020-HL-scheme-q6biv-sol',
         notes="The scheme prints 'Any three @ 6 + 6 + 6'."),
    dict(key=(6, 'b', 'v'),
         why='Scheme p18 answers in one paragraph, "Any three @ 6 + 6 + 6".',
         topic='eng-1-9',
         lifted=[S(18, 106, 679, 550, 729)], marks=[6], total=6,
         notes="The scheme prints 'Any three @ 6 + 6 + 6'."),
    dict(key=(6, 'c', 'ii'),
         replaces=NEW + 'described the process without naming it',
         why='Scheme p19 names extrusion and describes it in bullets under a labelled '
             'diagram, which is shown with the answer. "10".',
         lifted=[S(19, 106, 173, 160, 189), S(19, 132, 307, 506, 325),
                 S(19, 132, 325, 340, 342), S(19, 132, 342, 320, 360),
                 S(19, 132, 359, 555, 394), S(19, 132, 394, 424, 412)],
         tariff='questionTotal', total=10,
         figure='engineering-2020-HL-scheme-q6cii-sol',
         notes="The scheme prints '10'."),
    # ---- Question 7 --------------------------------------------------------
    dict(key=(7, 'a', 'i'),
         why='Scheme p19 describes each chip in a paragraph beside a drawing, shown '
             'with the answer; "5 + 5".',
         topic='eng-2-11',
         lifted=[S(19, 105, 497, 404, 614), S(19, 105, 631, 398, 715)],
         marks=[5, 5], total=10,
         figure='engineering-2020-HL-scheme-q7ai-sol',
         notes="The scheme prints '5 + 5'."),
    dict(key=(7, 'b', 'ii'),
         why='Scheme p20 lists four hazards under a heading; the part is priced "Any '
             'three @ 6 + 6 + 6".',
         topic='eng-3-1',
         lifted=[S(20, 132, 324, 277, 342), S(20, 132, 339, 324, 357),
                 S(20, 132, 354, 232, 372), S(20, 132, 370, 179, 388)],
         tariff='questionTotal', total=6,
         notes="The scheme prints 'Any three @ 6 + 6 + 6'."),
    dict(key=(7, 'c', 'i'),
         replaces=NEW + 'carried both OR branches, and read the six operations\' '
                  'captions across their columns',
         why='The camera-handle branch\'s (i), lifted with its cue. Scheme p21 draws six '
             'lathe operations, each captioned; each caption is lifted by its column\'s '
             'rectangle and the drawings are shown with the answer. "Any three @ 3 + 3 '
             '+ 3".',
         question_lift=P(10, *_C7A, more=[(126, 453, 410, 485)]), stem=False,
         lifted=[[S(21, 106, 173, 240, 206), S(21, 248, 173, 385, 206),
                  S(21, 394, 173, 560, 206), S(21, 106, 325, 240, 392),
                  S(21, 248, 342, 385, 375), S(21, 394, 342, 560, 392)]],
         row_kind='anyN', group=(3, 3), marks=[9], tariff='fixed', total=9,
         question_figure='engineering-2020-HL-paper-q7ci-art',
         figure='engineering-2020-HL-scheme-q7ci-sol', notes=_OR7),
    dict(key=(7, 'c', 'ii'),
         replaces=NEW + 'carried both OR branches\' questions and answers at the first '
                  'branch\'s total',
         why='The camera-handle branch\'s (ii), lifted with its cue; scheme p21 explains '
             'each beside a drawing, shown with the answer. "7".',
         question_lift=P(10, *_C7A, more=[(126, 498, 414, 530)]), stem=False,
         lifted=[S(21, 106, 443, 367, 510), S(21, 106, 561, 358, 611)],
         tariff='questionTotal', total=7,
         question_figure='engineering-2020-HL-paper-q7ci-art',
         figure='engineering-2020-HL-scheme-q7cii-sol', notes=_OR7),
    dict(key=(7, 'c', 'i'), id='eng-2020-hl-q7-c-i-or', ref_note='CNC technology',
         why='The CNC branch\'s (i), lifted with its cue; scheme p22 explains each term '
             'in a paragraph, "4 + 4".',
         topic='eng-2-11', stem=False,
         question_lift=P(10, *_C7B, more=[(127, 657, 420, 708)]),
         lifted=[S(22, 106, 89, 560, 156), S(22, 106, 173, 560, 223)],
         marks=[4, 4], total=8,
         question_figure='engineering-2020-HL-paper-q7c-or-crop', notes=_OR7),
    dict(key=(7, 'c', 'ii'), id='eng-2020-hl-q7-c-ii-or', ref_note='CNC technology',
         why='The CNC branch\'s (ii), lifted with its cue; scheme p22 gives two benefits '
             'in two paragraphs, "4 + 4".',
         topic='eng-2-11', stem=False,
         question_lift=P(10, *_C7B, more=[(126, 720, 372, 754)]),
         lifted=[S(22, 106, 258, 553, 307), S(22, 106, 308, 550, 341)],
         marks=[4, 4], total=8,
         question_figure='engineering-2020-HL-paper-q7c-or-crop', notes=_OR7),
    # ---- Question 8 --------------------------------------------------------
    dict(key=(8, 'a', 'i'),
         replaces=NEW + 'gave the one-sentence answer without the diagram the part asks '
                  'for',
         why='The saw is photographed beside (a); scheme p22 answers in one sentence '
             'over a labelled diagram, which is shown with the answer. "8".',
         lifted=[S(22, 106, 409, 559, 442)], marks=[8], total=8,
         question_figure='engineering-2020-HL-paper-q8a-crop',
         figure='engineering-2020-HL-scheme-q8ai-sol',
         notes="The scheme prints '8'."),
    dict(key=(8, 'a', 'ii'),
         replaces=NEW + 'set advantages and disadvantages in one list as an ordered '
                  'split, so two advantages could take both halves',
         why='Scheme pp22-23 list five advantages and three disadvantages under their '
             'headings, "4 + 4": one of each. Each option is lifted with its heading.',
         question_figure='engineering-2020-HL-paper-q8a-crop',
         lifted=[[join(S(*_ADV8), S(22, 132, 659, 274, 676)),
                  join(S(*_ADV8), S(22, 132, 674, 559, 706)),
                  join(S(*_ADV8), S(22, 132, 704, 202, 722)),
                  join(S(*_ADV8), S(22, 132, 719, 275, 737)),
                  join(S(*_ADV8), S(22, 132, 734, 182, 752))],
                 [join(S(*_DIS8), S(23, 132, 86, 551, 133)),
                  join(S(*_DIS8), S(23, 132, 130, 200, 148)),
                  join(S(*_DIS8), S(23, 132, 146, 211, 164))]],
         group=[(1, 4), (1, 4)], marks=[4, 4], total=8,
         notes="The scheme prints '4 + 4'."),
    dict(key=(8, 'b', 'i'),
         replaces=NEW + 'carried the drawing\'s captions "Helical gear spur gear" as an '
                  'answer',
         why='Scheme p23 answers in two sentences beside drawings of both gears, shown '
             'with the answer; "Any three @ 6 + 6 + 6".',
         lifted=[S(23, 106, 205, 387, 221), S(23, 106, 219, 401, 279)],
         tariff='questionTotal', total=6,
         figure='engineering-2020-HL-scheme-q8bi-sol',
         notes="The scheme prints 'Any three @ 6 + 6 + 6'."),
    dict(key=(8, 'b', 'iii'),
         why='Scheme p23 answers in one paragraph, "Any three @ 6 + 6 + 6".',
         topic='eng-2-15',
         lifted=[S(23, 106, 398, 364, 487)], marks=[6], total=6,
         notes="The scheme prints 'Any three @ 6 + 6 + 6'."),
    dict(key=(8, 'b', 'v'),
         replaces=NEW + 'carried the scheme\'s tariff "(Any three) 6 + 6 + 6" as an '
                  'answer',
         why='Scheme p23 answers in one sentence over drawings of both strokes, shown '
             'with the answer; "(Any three) 6 + 6 + 6".',
         lifted=[S(23, 106, 543, 559, 574)], marks=[6], total=6,
         figure='engineering-2020-HL-scheme-q8bv-sol',
         notes="The scheme prints '(Any three) 6 + 6 + 6'."),
    dict(key=(8, 'c', 'i'),
         replaces=NEW + 'carried both OR branches as one question total with no route '
                  'between them',
         why='Both (c)s price their (i) at 8 (scheme p24): the worm drive beside its '
             'photograph (shown with the answer), or the PV panel\'s energy '
             'conversion. One card for the printed OR, each branch a route of its own.',
         question_lift=P(11, *_C8A, more=[(126, 485, 354, 518), _OR8P, _C8B,
                                          (126, 667, 371, 700)]), stem=False,
         lifted=[S(24, 106, 72, 325, 176), S(24, 105, 365, 558, 411)],
         marks=[8, 8], routes=['a', 'b'], total=8,
         question_figure='engineering-2020-HL-paper-q8c-crop',
         figure='engineering-2020-HL-scheme-q8ci-sol', notes=_OR8),
    dict(key=(8, 'c', 'ii'),
         replaces=NEW + 'carried both OR branches as one question total, with the PV '
                  'advantages and disadvantages in one list',
         why='Both (c)s price their (ii) at 8 (scheme p24): the bevel gear mechanism '
             'beside its photograph (shown with the answer), or one PV advantage and '
             'one disadvantage, "4 + 4", each option lifted with its heading. One card '
             'for the printed OR, each branch a route of its own.',
         question_lift=P(11, *_C8A, more=[(126, 527, 354, 577), _OR8P, _C8B,
                                          (126, 707, 358, 740)]), stem=False,
         lifted=[S(24, 105, 204, 326, 293),
                 [join(S(*_ADVPV), S(24, 133, 439, 561, 484)),
                  join(S(*_ADVPV), S(24, 133, 483, 413, 499)),
                  join(S(*_ADVPV), S(24, 133, 497, 545, 528)),
                  join(S(*_ADVPV), S(24, 133, 526, 404, 542)),
                  join(S(*_ADVPV), S(24, 133, 541, 547, 572))],
                 [join(S(*_DISPV), S(24, 137, 600, 528, 645)),
                  join(S(*_DISPV), S(24, 137, 644, 549, 690)),
                  join(S(*_DISPV), S(24, 137, 689, 554, 734))]],
         group=[None, (1, 4), (1, 4)], marks=[8, 4, 4], routes=['a', 'b', 'b'],
         total=8,
         question_figure='engineering-2020-HL-paper-q8c-crop',
         figure='engineering-2020-HL-scheme-q8cii-sol', notes=_OR8),
]

TOPICS = {
    'eng-2020-hl-q8-b-iv': ('eng-2-15', 'lubricating geared mechanisms is mechanisms; '
                            '"lubricants" outvoted it'),
}

_MM = 'Machining & Metrology'

ATLAS = {
    'eng-2020-hl-q1-e': dict(
        topics=['Testing of Materials and Products'],
        note='The tolerance of the wheel rim, a quality measure; the reference lists no '
             'metrology topic for Q1. The card\'s syllabus heading is Metrology.'),
    'eng-2020-hl-q3-b-iii': dict(
        topics=['Equilibrium Diagrams'],
        note='The material between 2.0% and 4.0% carbon, read off the iron-carbon '
             'diagram the part is printed under; the card\'s syllabus heading is Iron and '
             'steel.'),
    'eng-2020-hl-q5-c-ii': dict(
        topics=['Energy, Electronics & Robotics'],
        note='Robotic cleaners against human cleaning (the OR branch of Q5(c)); the '
             'card\'s syllabus heading is Technology, where the syllabus places robotics.'),
    'eng-2020-hl-q7-b-ii': dict(
        topics=[_MM],
        note='Hazards of laser cutting, a machining process, which the reference files '
             'with the rest of Q7; the card\'s syllabus heading is Health and safety.'),
    'eng-2020-hl-q7-b-iii': dict(
        topics=[_MM],
        note='Thread rolling, which the reference files with the rest of Q7 under '
             'machining; the card\'s syllabus heading is Manufacturing processes.'),
}
