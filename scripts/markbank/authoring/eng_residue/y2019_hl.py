"""2019 Higher Level: the parts eng_all refuses or gets wrong, from the page.

Paper and scheme as the PDFs number their pages. The marks grid is on scheme
p4: Question 1 is Section A, "Any ten @ 5 marks each", and Section B, "Answer
all of the following", (n) to (r); Questions 2-8 are 50 marks each. The grid
letters Question 2's parts (a), (b), (c), (d) against the paper's (a), (b),
(c); the answers on pp10-12 follow the paper. The scheme prints a part's marks
under its answer ("3 + 2", "Any three @ 2 + 2 + 1"). This sitting had no cards
before the lane: every card here is new, and a `replaces=` names the automatic
card it rebuilds before it ever shipped.
"""
from eng_lift import join, lift

Y, L = 2019, 'hl'
NEW = 'never shipped: the automatic card '
OWNED = ('never shipped: the automatic author builds this card only from the lifts this '
         'entry records, so the entry owns it')


def S(page, *rect):
    return lift(Y, L, 'scheme', page, rect)


def P(page, *rect, more=()):
    return lift(Y, L, 'paper', page, rect, more=more)


# Paper p4: Section B stems; p5: Question 2's (b) and (c) stems; p7: Q4(b).
_N1 = (107, 113, 383, 179)
_Q1 = (107, 514, 393, 547)
_B2 = (102, 295, 528, 327)
_C2 = (102, 594, 541, 627)
_B4 = (102, 274, 507, 307)
_GRAPH4 = (104, 414, 267, 430)        # "Using the graph paper supplied:"
# Paper p10: Question 7's two (c)s; p11: Question 8's.
_C7A = (104, 446, 421, 479)
_C7B = (104, 593, 486, 626)
_OR7 = (310, 564, 331, 580)
_C8A = (104, 474, 529, 507)
_C8B = (100, 660, 399, 692)
_OR8 = (292, 624, 313, 640)
# Scheme p18: the comparison table's column and row heads.
_SPOT, _SEAM = (18, 75, 60, 201, 79), (18, 323, 60, 454, 79)
_ES, _WP, _AP, _SC = ((18, 75, 313, 164, 332), (18, 75, 380, 180, 399),
                      (18, 75, 565, 147, 585), (18, 73, 641, 191, 660))

_OR5 = ('The paper sets two (c)s either side of an OR: the resistance welding (c), '
        'answered at the letter for 16, and the exoskeleton suit (c), whose (i) and '
        '(ii) are 4 + 4 each.')
_OR7N = ('The paper sets two (c)s either side of an OR, tungsten carbide inserts and CNC '
         'technology; the scheme prices each (i) and each (ii) at 8.')
_OR8N = ('The paper sets two (c)s either side of an OR, the crop sprayer and the control '
         'circuit; the scheme prices each (i) and each (ii) at 8.')


def _opts(page, y0, y1, *spans):
    """One option per word span on a printed line: (x0, x1) pairs."""
    return [S(page, x0, y0, x1, y1) for x0, x1 in spans]


CROPS = {
    # ---- paper ------------------------------------------------------------
    'engineering-2019-HL-paper-q1i-crop': dict(
        doc='paper', page=3, rect=(492, 518, 570, 680), ref='2019 HL Q1(i)'),
    'engineering-2019-HL-paper-q2b-crop': dict(
        doc='paper', page=5, rect=(88, 338, 548, 404), ref='2019 HL Q2(b)'),
    'engineering-2019-HL-paper-q3b-crop': dict(
        doc='paper', page=6, rect=(150, 345, 450, 522), ref='2019 HL Q3(b)',
        letters=('A', 'B', 'C', 'X', 'Y')),
    'engineering-2019-HL-paper-q4b-crop': dict(
        doc='paper', page=7, rect=(98, 320, 548, 395), ref='2019 HL Q4(b)'),
    # The slide without the page's "(50 marks)" heading (the automatic crop's).
    'engineering-2019-HL-paper-q5a-crop': dict(
        doc='paper', page=8, rect=(398, 82, 575, 292), ref='2019 HL Q5(a)'),
    'engineering-2019-HL-paper-q6a-crop': dict(
        doc='paper', page=9, rect=(420, 287, 576, 434), mask=[(418, 324, 427, 340)],
        ref='2019 HL Q6(a)'),
    'engineering-2019-HL-paper-q8a-crop': dict(
        doc='paper', page=11, rect=(388, 86, 582, 298), mask=[(386, 99, 397, 115)],
        ref='2019 HL Q8(a)'),
    # The crop sprayer beside the control circuit, the two (c)s' pictures.
    'engineering-2019-HL-paper-q8c-crop': dict(
        doc='paper', page=11, parts=[(11, (372, 486, 586, 615)),
                                     (11, (412, 646, 575, 790))],
        layout='row', ref='2019 HL Q8(c)'),
    # ---- scheme: the drawings the answers are given with -------------------
    'engineering-2019-HL-scheme-q1b-sol': dict(
        doc='scheme', page=5, rect=(130, 224, 475, 368), solution=True,
        ref='2019 HL Q1(b)'),
    'engineering-2019-HL-scheme-q1e-sol': dict(
        doc='scheme', page=6, rect=(200, 82, 372, 208), mask=[(198, 82, 228, 146)],
        solution=True,
        ref='2019 HL Q1(e)'),
    'engineering-2019-HL-scheme-q1g-sol': dict(
        doc='scheme', page=6, rect=(175, 323, 440, 418), solution=True,
        ref='2019 HL Q1(g)'),
    'engineering-2019-HL-scheme-q1j-sol': dict(
        doc='scheme', page=6, rect=(355, 560, 512, 640), solution=True,
        ref='2019 HL Q1(j)'),
    'engineering-2019-HL-scheme-q1n-sol': dict(
        doc='scheme', page=7, rect=(150, 432, 490, 594), solution=True,
        ref='2019 HL Q1(n)(ii)'),
    'engineering-2019-HL-scheme-q1o-sol': dict(
        doc='scheme', page=8, parts=[(8, (66, 88, 492, 302)), (8, (66, 440, 560, 672))],
        solution=True, ref='2019 HL Q1(o)'),
    'engineering-2019-HL-scheme-q1q-sol': dict(
        doc='scheme', page=9, rect=(155, 362, 448, 460), solution=True,
        ref='2019 HL Q1(q)(i)'),
    'engineering-2019-HL-scheme-q2aii-sol': dict(
        doc='scheme', page=11, rect=(356, 74, 582, 224),
        mask=[(354, 104, 364, 145), (354, 145, 369, 206)], solution=True,
        ref='2019 HL Q2(a)(ii)'),
    'engineering-2019-HL-scheme-q2bi-sol': dict(
        doc='scheme', page=11, rect=(90, 326, 525, 606), solution=True,
        ref='2019 HL Q2(b)(i)'),
    'engineering-2019-HL-scheme-q2bii-sol': dict(
        doc='scheme', page=11, rect=(150, 648, 520, 750), solution=True,
        ref='2019 HL Q2(b)(ii)'),
    'engineering-2019-HL-scheme-q2cii-sol': dict(
        doc='scheme', page=12, rect=(352, 238, 586, 458),
        mask=[(350, 286, 363, 302), (350, 374, 370, 406)], solution=True,
        ref='2019 HL Q2(c)(ii)'),
    'engineering-2019-HL-scheme-q3c-sol': dict(
        doc='scheme', page=13, rect=(350, 355, 595, 630), mask=[(348, 491, 442, 507)],
        solution=True, ref='2019 HL Q3(c)'),
    'engineering-2019-HL-scheme-q4a-sol': dict(
        doc='scheme', page=14, rect=(100, 155, 540, 515), solution=True,
        ref='2019 HL Q4(a)'),
    'engineering-2019-HL-scheme-q4bi-sol': dict(
        doc='scheme', page=15, rect=(150, 88, 520, 338), solution=True,
        ref='2019 HL Q4(b)(i)'),
    'engineering-2019-HL-scheme-q4ci-sol': dict(
        doc='scheme', page=15, rect=(90, 610, 548, 686), solution=True,
        ref='2019 HL Q4(c)(i)'),
    'engineering-2019-HL-scheme-q4cii-sol': dict(
        doc='scheme', page=16, rect=(428, 76, 585, 252), solution=True,
        ref='2019 HL Q4(c)(ii)'),
    'engineering-2019-HL-scheme-q5ai-sol': dict(
        doc='scheme', page=16, rect=(390, 330, 568, 486), mask=[(388, 466, 443, 482)],
        solution=True, ref='2019 HL Q5(a)(i)'),
    'engineering-2019-HL-scheme-q5biii-sol': dict(
        doc='scheme', page=17, parts=[(17, (336, 102, 578, 276)), (17, (60, 290, 302, 400)),
                                      (17, (318, 405, 578, 530))],
        mask=[(316, 432, 336, 484)], solution=True, ref='2019 HL Q5(b)(iii)'),
    'engineering-2019-HL-scheme-q5c-sol': dict(
        doc='scheme', page=18, rect=(70, 82, 572, 292), solution=True,
        ref='2019 HL Q5(c)'),
    'engineering-2019-HL-scheme-q6aii-sol': dict(
        doc='scheme', page=19, rect=(98, 596, 530, 735), solution=True,
        ref='2019 HL Q6(a)(ii)'),
    'engineering-2019-HL-scheme-q7bi-sol': dict(
        doc='scheme', page=21, rect=(104, 556, 520, 712), solution=True,
        ref='2019 HL Q7(b)(i)'),
    'engineering-2019-HL-scheme-q7biv-sol': dict(
        doc='scheme', page=22, rect=(445, 208, 568, 330), solution=True,
        ref='2019 HL Q7(b)(iv)'),
    'engineering-2019-HL-scheme-q7bv-sol': dict(
        doc='scheme', page=22, rect=(265, 330, 545, 460), mask=[(263, 344, 310, 380)],
        solution=True, ref='2019 HL Q7(b)(v)'),
    'engineering-2019-HL-scheme-q8ai-sol': dict(
        doc='scheme', page=23, rect=(322, 452, 548, 600), solution=True,
        ref='2019 HL Q8(a)(i)'),
    'engineering-2019-HL-scheme-q8aii-sol': dict(
        doc='scheme', page=23, rect=(317, 615, 530, 720), solution=True,
        ref='2019 HL Q8(a)(ii)'),
    'engineering-2019-HL-scheme-q8bi-sol': dict(
        doc='scheme', page=24, rect=(358, 72, 555, 153), solution=True,
        ref='2019 HL Q8(b)(i)'),
    'engineering-2019-HL-scheme-q8biv-sol': dict(
        doc='scheme', page=24, rect=(400, 248, 565, 333), solution=True,
        ref='2019 HL Q8(b)(iv)'),
    'engineering-2019-HL-scheme-q8bv-sol': dict(
        doc='scheme', page=24, rect=(358, 336, 578, 428), solution=True,
        ref='2019 HL Q8(b)(v)'),
    'engineering-2019-HL-scheme-q8ci-sol': dict(
        doc='scheme', page=24, rect=(48, 500, 570, 640), solution=True,
        ref='2019 HL Q8(c)(i)'),
}

FOLDED = {
    'eng-2019-hl-q4-a-ii': NEW[:-1] + ' set "Amorphous materials and crystalline materials" '
                           'apart from the other two pairs of "Select any two from (i), (ii) or '
                           '(iii)"; the choice is one card, at Q4(a)',
}

CARDS = [
    # ---- Question 1, Section A ("Any ten @ 5 marks each") ------------------
    dict(key=(1, 'a', None),
         why='Scheme p5 names the reasons in one line; each is lifted by its own word '
             'rectangle. "3 + 2" for two.',
         topic='eng-1-9',
         lifted=_opts(5, 157, 177, (70, 175), (175, 235), (235, 339), (339, 417),
                      (417, 514)),
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         notes="The scheme prints '3 + 2'."),
    dict(key=(1, 'b', None),
         why='Scheme p5 describes the process in one paragraph under a labelled diagram, '
             'which is shown with the answer; "5".',
         topic='eng-1-2',
         lifted=[S(5, 70, 398, 557, 431)], marks=[5], total=5,
         figure='engineering-2019-HL-scheme-q1b-sol',
         notes="The scheme prints '5'."),
    dict(key=(1, 'c', None),
         why='Scheme p5 names the advantages in one sentence; each is lifted by its own '
             'word rectangle. "Any two @ 3 + 2".',
         topic='eng-2-15',
         lifted=[S(5, 70, 466, 207, 482), S(5, 207, 466, 456, 482),
                 join(S(5, 456, 466, 557, 482), S(5, 70, 482, 194, 498))],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         notes="The scheme prints 'Any two @ 3 + 2'."),
    dict(key=(1, 'd', None),
         why='Scheme p5 gives a paragraph on each of the three, "Any one @ 5".',
         topic='eng-3-14',
         question_lift=P(3, 107, 309, 496, 342),
         lifted=[[S(5, 106, 530, 564, 634), S(5, 106, 648, 540, 684),
                  S(5, 106, 699, 549, 734)]],
         row_kind='anyN', group=(1, 5), marks=[5], tariff='fixed', total=5,
         notes="The scheme prints 'Any one @ 5'."),
    dict(key=(1, 'e', None),
         why='The wheel is photographed beside (e); scheme p6 answers beside a picture of '
             'the keyed wheel, shown with the answer, "Alternative suggestions '
             'accepted". "5".',
         topic='eng-2-10',
         lifted=[S(6, 77, 96, 230, 146)], marks=[5], total=5,
         question_figure='engineering-2019-HL-paper-q1e-art',
         figure='engineering-2019-HL-scheme-q1e-sol',
         notes="The scheme prints '5', and 'Alternative suggestions accepted'."),
    dict(key=(1, 'f', None),
         why='Scheme p6 names the advantages in one line; each is lifted by its own word '
             'rectangle. "3 + 2" for two.',
         topic='eng-1-9',
         lifted=_opts(6, 222, 242, (70, 195), (195, 270), (270, 355), (355, 503)),
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         question_figure='engineering-2019-HL-paper-q1e-art',
         notes="The scheme prints '3 + 2'."),
    dict(key=(1, 'g', None),
         why='Scheme p6 explains each fit in a sentence over drawings of both, shown with '
             'the answer; "5" for the part.',
         topic='eng-3-12',
         lifted=[S(6, 70, 272, 557, 307), S(6, 70, 306, 561, 341)],
         tariff='questionTotal', total=5,
         figure='engineering-2019-HL-scheme-q1g-sol',
         notes="The scheme prints '5'."),
    dict(key=(1, 'h', None),
         why='Scheme p6 names the media in one line; each is lifted by its own word '
             'rectangle. "Any three @ 2 + 2 + 1".',
         topic='eng-2-6',
         lifted=_opts(6, 451, 471, (70, 89), (89, 124), (124, 155), (155, 211),
                      (211, 292), (292, 319)),
         tariff='orderedSplit', notation='2 + 2 + 1', ladder=5, total=5,
         notes="The scheme prints 'Any three @ 2 + 2 + 1'."),
    dict(key=(1, 'i', None),
         why='The hiking stick is photographed beside (i); scheme p6 answers in one '
             'sentence, "5".',
         topic='eng-3-7',
         lifted=[S(6, 70, 503, 559, 536)], marks=[5], total=5,
         question_figure='engineering-2019-HL-paper-q1i-crop',
         notes="The scheme prints '5'."),
    dict(key=(1, 'j', None),
         why='Scheme p6 gives a "Suggested solution, other feasible solutions accepted" '
             'beside a drawing of the tightening pin, shown with the answer; "5".',
         topic='eng-2-15',
         lifted=[S(6, 70, 587, 345, 637)], marks=[5], total=5,
         figure='engineering-2019-HL-scheme-q1j-sol',
         notes="The scheme prints '5', for a suggested solution: 'other feasible solutions "
               "accepted'."),
    dict(key=(1, 'k', None),
         why='Scheme p6 answers in one paragraph, "5".',
         topic='eng-2-16',
         lifted=[join(S(6, 70, 652, 555, 687), S(6, 70, 687, 540, 705))], marks=[5], total=5,
         notes="The scheme prints '5'."),
    dict(key=(1, 'l', None),
         why='Scheme p6 names the details in one line; each is lifted by its own word '
             'rectangle. "Any three @ 2 + 2 + 1".',
         topic='eng-3-14',
         lifted=_opts(6, 720, 740, (70, 167), (167, 229), (229, 314), (314, 403),
                      (403, 511)),
         tariff='orderedSplit', notation='2 + 2 + 1', ladder=5, total=5,
         notes="The scheme prints 'Any three @ 2 + 2 + 1'."),
    dict(key=(1, 'm', None),
         why='The four safety signs are printed beside (m); scheme p7 explains the '
             'colours in a lead-in, four bullets and a closing sentence; "5" for the part. '
             'The reader files the Section B heading printed after (m) as its stem, so the '
             'card carries none.',
         topic='eng-3-1', stem=False,
         lifted=[S(7, 70, 89, 545, 122), S(7, 106, 124, 330, 140),
                 S(7, 106, 141, 330, 157), S(7, 106, 158, 374, 174),
                 S(7, 106, 176, 348, 192), S(7, 62, 193, 557, 209)],
         tariff='questionTotal', total=5,
         question_figure='engineering-2019-HL-paper-q1m-art',
         notes="The scheme prints '5'."),
    # ---- Question 1, Section B ("Answer all of the following") -------------
    dict(key=(1, 'n', 'i'),
         why='Section B. Scheme p7 answers in one paragraph; (n) is "5 + 5". The question '
             'is lifted with (n)\'s stimulus, which points at the buckyball "shown '
             'opposite", so the card carries it.',
         topic='eng-3-14', stem=False,
         question_lift=P(4, *_N1, more=[(143, 189, 319, 205)]),
         lifted=[S(7, 106, 291, 537, 361)], marks=[5], total=5,
         question_figure='engineering-2019-HL-paper-q1ni-art',
         notes="The scheme prints '5 + 5' for (n)."),
    dict(key=(1, 'n', 'ii'),
         why='Section B. Scheme p7 answers the structure and the properties in '
             'paragraphs beside a labelled drawing of a buckyball, shown with the answer; '
             '(n) is "5 + 5".',
         topic='eng-3-14', stem=False,
         question_lift=P(4, *_N1, more=[(143, 211, 396, 227)]),
         lifted=[S(7, 106, 375, 559, 428), S(7, 106, 597, 558, 647),
                 S(7, 106, 645, 562, 748)],
         tariff='questionTotal', total=5,
         question_figure='engineering-2019-HL-paper-q1ni-art',
         figure='engineering-2019-HL-scheme-q1n-sol',
         notes="The scheme prints '5 + 5' for (n)."),
    dict(key=(1, 'o', None),
         why='Section B. Scheme p8 describes each microscope under its name beside a '
             'labelled diagram, both shown with the answer; "Any one @ 10".',
         topic='eng-3-14', stem=False,
         question_lift=P(4, 107, 264, 478, 296, more=[(107, 306, 338, 344)]),
         lifted=[[join(S(8, 106, 70, 276, 89), S(8, 106, 308, 559, 413)),
                  join(S(8, 106, 420, 300, 439), S(8, 106, 675, 561, 742))]],
         row_kind='anyN', group=(1, 10), marks=[10], tariff='fixed', total=10,
         figure='engineering-2019-HL-scheme-q1o-sol',
         notes="The scheme prints 'Any one @ 10'."),
    dict(key=(1, 'p', None),
         why='Section B. Scheme p9 answers each application under its name, "4 + 3 + 3".',
         topic='eng-3-14', stem=False,
         question_lift=P(4, 107, 390, 477, 406, more=[(140, 415, 318, 477)]),
         lifted=[S(9, 69, 87, 554, 173), S(9, 69, 188, 548, 223), S(9, 69, 238, 547, 290)],
         marks=[4, 3, 3], total=10,
         notes="The scheme prints '4 + 3 + 3'."),
    dict(key=(1, 'q', 'i'),
         why='Section B. Scheme p9 answers in one paragraph under a drawing of a graphene '
             'sheet rolled into a nanotube, shown with the answer; "4".',
         topic='eng-3-14', stem=False,
         question_lift=P(4, *_Q1, more=[(143, 556, 379, 572)]),
         lifted=[S(9, 106, 477, 558, 560)], marks=[4], total=4,
         figure='engineering-2019-HL-scheme-q1q-sol',
         notes="The scheme prints '4'."),
    dict(key=(1, 'q', 'ii'),
         why='Section B. Scheme p9 lists six properties, "2 + 2 + 2" for three.',
         topic='eng-3-14', stem=False,
         question_lift=P(4, *_Q1, more=[(143, 578, 423, 594)]),
         lifted=[[S(9, 142, y - 2, 340, y + 14) for y in (597, 612, 628, 643, 658, 674)]],
         row_kind='anyN', group=(3, 2), marks=[6], tariff='fixed', total=6,
         notes="The scheme prints '2 + 2 + 2'."),
    dict(key=(1, 'r', None),
         why='Section B. Scheme p10 answers each area under its name, "Any two @ 5 + 5"; '
             'each answer is lifted with its name.',
         topic='eng-3-14', stem=False,
         question_lift=P(4, 107, 640, 451, 656, more=[(107, 666, 275, 747)]),
         lifted=[[join(S(10, 86, 70, 145, 89), S(10, 70, 89, 558, 257)),
                  join(S(10, 88, 272, 224, 291), S(10, 70, 291, 561, 358)),
                  join(S(10, 92, 373, 138, 392), S(10, 70, 392, 549, 459)),
                  join(S(10, 90, 474, 157, 493), S(10, 70, 493, 553, 577))]],
         row_kind='anyN', group=(2, 5), marks=[10], tariff='fixed', total=10,
         notes="The scheme prints 'Any two @ 5 + 5'."),
    # ---- Question 2 --------------------------------------------------------
    dict(key=(2, 'a', 'ii'), replaces=OWNED,
         why='Scheme p11 describes "Any suitable hardness test, Vickers test is shown" in '
             'two paragraphs beside a labelled drawing, shown with the answer; "10".',
         topic='eng-3-8',
         lifted=[S(11, 106, 106, 363, 205),
                 join(S(11, 106, 207, 330, 223), S(11, 106, 224, 556, 273),
                      S(11, 106, 273, 540, 290))],
         tariff='questionTotal', total=10,
         figure='engineering-2019-HL-scheme-q2aii-sol',
         notes="The scheme prints '10' for 'Any suitable hardness test, Vickers test is "
               "shown'."),
    dict(key=(2, 'b', 'i'),
         why='Scheme p11 answers the plot with both stress-strain graphs on one set of '
             'axes and prints no words; the graphs are shown with the answer. "10". The '
             'results table is shown as printed.',
         topic='eng-3-8', stem=False,
         question_lift=P(5, *_B2, more=[(138, 421, 461, 467)]),
         special={'kind': 'ask'}, total=10,
         question_figure='engineering-2019-HL-paper-q2b-crop',
         figure='engineering-2019-HL-scheme-q2bi-sol',
         notes="The scheme prints '10'."),
    dict(key=(2, 'b', 'ii'), topic='eng-3-8',
         replaces=NEW + 'carried the results table as a line of numbers for a stem and '
                  'the photographs\' captions "Brittle fracture Ductile fracture" as an '
                  'answer',
         why='Scheme p11 names both fractures in one sentence, either side of its comma; '
             'each is lifted by word rectangle and the photographs are shown with the '
             'answer. "2 + 2".',
         stem=False,
         question_lift=P(5, *_B2, more=[(138, 476, 413, 522)]),
         lifted=[S(11, 102, 628, 342, 644), S(11, 342, 628, 560, 644)],
         marks=[2, 2], total=4,
         question_figure='engineering-2019-HL-paper-q2b-crop',
         figure='engineering-2019-HL-scheme-q2bii-sol',
         notes="The scheme prints '2 + 2'."),
    dict(key=(2, 'b', 'iii'),
         why='Scheme p12 names a metal for each graph, "2 + 2".',
         topic='eng-3-8', stem=False,
         question_lift=P(5, *_B2, more=[(138, 529, 520, 563)]),
         lifted=[S(12, 106, 70, 165, 89), S(12, 106, 87, 237, 106)],
         marks=[2, 2], total=4,
         question_figure='engineering-2019-HL-paper-q2b-crop',
         notes="The scheme prints '2 + 2'."),
    dict(key=(2, 'c', 'i'),
         why='Scheme p12 gives an application for each method on its own line, "2 + 2 + 2 '
             '+ 2".',
         topic='eng-3-8',
         question_lift=P(5, *_C2, more=[(138, 641, 465, 727)]), stem=False,
         lifted=[S(12, 106, 140, 320, 156), S(12, 106, 157, 302, 173),
                 S(12, 106, 173, 419, 189), S(12, 106, 190, 451, 206)],
         marks=[2, 2, 2, 2], total=8,
         notes="The scheme prints '2 + 2 + 2 + 2'."),
    dict(key=(2, 'c', 'ii'),
         why='Scheme p12 describes the radiography test beside a labelled diagram, shown '
             'with the answer; "8".',
         topic='eng-3-8',
         lifted=[join(S(12, 106, 272, 360, 406), S(12, 106, 419, 273, 435))],
         marks=[8], total=8,
         figure='engineering-2019-HL-scheme-q2cii-sol',
         notes="The scheme prints '8'."),
    # ---- Question 3 --------------------------------------------------------
    dict(key=(3, 'b', 'i'), topic='eng-1-4',
         replaces=NEW + 'gave region A twice, once with region B and the tariff "3 + 3" '
                  'welded in',
         why='The diagram is printed with regions A and B lettered; scheme p12 names '
             'each, "3 + 3".',
         stem=False,
         lifted=[S(12, 106, 711, 173, 730), S(12, 106, 727, 238, 747)],
         marks=[3, 3], total=6,
         question_figure='engineering-2019-HL-paper-q3b-crop',
         labels={'A': S(12, 120, 711, 173, 730), 'B': S(12, 120, 727, 238, 747)},
         notes="The scheme prints '3 + 3'."),
    dict(key=(3, 'b', 'ii'), topic='eng-1-4',
         replaces=NEW + 'read the scheme\'s two columns as one list, with X\'s heading '
                  'missing and Y\'s bullets among X\'s',
         why='Scheme p13 answers in two columns, X and Y, each a heading over bullets; '
             'each column is lifted whole. "6".',
         stem=False,
         lifted=[join(S(13, 106, 87, 296, 106), S(13, 142, 107, 300, 214)),
                 join(S(13, 332, 87, 546, 106), S(13, 368, 107, 522, 214))],
         tariff='questionTotal', total=6,
         question_figure='engineering-2019-HL-paper-q3b-crop',
         notes="The scheme prints '6'."),
    dict(key=(3, 'b', 'iii'), topic='eng-1-4',
         replaces=NEW + 'did not show the diagram whose point C the part asks about',
         why='Point C is marked on the diagram; scheme p13 answers in three lines, "6".',
         stem=False,
         lifted=[S(13, 106, 272, 375, 322)], marks=[6], total=6,
         question_figure='engineering-2019-HL-paper-q3b-crop',
         notes="The scheme prints '6'."),
    dict(key=(3, 'c', None), replaces=OWNED,
         why='Scheme p13 describes each process under its name beside a labelled '
             'drawing, both shown with the answer; "16".',
         topic='eng-2-6',
         lifted=[join(S(13, 69, 354, 174, 373), S(13, 69, 373, 337, 490),
                      S(13, 69, 491, 442, 507)),
                 join(S(13, 69, 522, 157, 541), S(13, 69, 542, 345, 625))],
         tariff='questionTotal', total=16,
         figure='engineering-2019-HL-scheme-q3c-sol',
         notes="The scheme prints '16'."),
    # ---- Question 4 --------------------------------------------------------
    dict(key=(4, 'a', None), topic='eng-1-3',
         replaces=NEW + 'split (iii)\'s eutectic and eutectoid points into two options '
                  'and gave (ii) without its "Crystalline solid structures" heading',
         why='Scheme p14 answers each pair with its drawings, shown with the answer; '
             'each pair is lifted whole. "Any two @ 8 + 8".',
         lifted=[[S(14, 106, 114, 540, 147),
                  join(S(14, 106, 282, 239, 298), S(14, 106, 333, 323, 349),
                       S(14, 106, 400, 247, 416), S(14, 103, 451, 268, 484)),
                  join(S(14, 106, 552, 543, 602), S(14, 106, 619, 554, 686))]],
         row_kind='anyN', group=(2, 8), marks=[16], tariff='fixed', total=16,
         figure='engineering-2019-HL-scheme-q4a-sol',
         notes="The scheme prints 'Any two @ 8 + 8'."),
    dict(key=(4, 'b', 'i'),
         why='Scheme p15 answers with the equilibrium diagram drawn and labelled, and '
             'prints no other words; the diagram is shown with the answer. "10". The '
             'table is shown as printed.',
         topic='eng-1-3', stem=False,
         question_lift=P(7, *_B4, more=[_GRAPH4, (133, 442, 387, 458)]),
         special={'kind': 'ask'}, total=10,
         question_figure='engineering-2019-HL-paper-q4b-crop',
         figure='engineering-2019-HL-scheme-q4bi-sol',
         notes="The scheme prints '10'."),
    dict(key=(4, 'b', 'ii'),
         why='Scheme p15 describes eight features of the diagram, each under its name, '
             '"Any three @ 2 + 2 + 2".',
         topic='eng-1-3', stem=False,
         question_lift=P(7, *_B4, more=[_GRAPH4, (133, 470, 387, 486)]),
         lifted=[[S(15, 106, 349, 437, 365), S(15, 106, 365, 559, 395),
                  S(15, 106, 395, 334, 409), S(15, 106, 409, 344, 424),
                  S(15, 106, 424, 552, 453), S(15, 106, 453, 556, 483),
                  S(15, 106, 483, 249, 497), S(15, 106, 497, 555, 527)]],
         row_kind='anyN', group=(3, 2), marks=[6], tariff='fixed', total=6,
         question_figure='engineering-2019-HL-paper-q4b-crop',
         notes="The scheme prints 'Any three @ 2 + 2 + 2'."),
    dict(key=(4, 'c', 'i'), topic='eng-1-3',
         replaces=NEW + 'gave the description without the drawings the part asks for',
         why='Scheme p15 draws the stages and describes them in one paragraph; the '
             'drawings are shown with the answer. "8".',
         lifted=[S(15, 106, 690, 562, 739)], marks=[8], total=8,
         figure='engineering-2019-HL-scheme-q4ci-sol',
         notes="The scheme prints '8'."),
    dict(key=(4, 'c', 'ii'), replaces=OWNED,
         why='Scheme p16 describes three defects under their names beside drawings, '
             'shown with the answer; "Any two @ 4 + 4".',
         topic='eng-1-3',
         lifted=[[S(16, 106, 89, 385, 122), S(16, 106, 140, 410, 189),
                  S(16, 106, 207, 400, 240)]],
         row_kind='anyN', group=(2, 4), marks=[8], tariff='fixed', total=8,
         figure='engineering-2019-HL-scheme-q4cii-sol',
         notes="The scheme prints 'Any two @ 4 + 4'."),
    # ---- Question 5 --------------------------------------------------------
    dict(key=(5, 'a', 'i'), topic='eng-2-10',
         replaces=NEW + 'gave the description without the diagram the part asks for',
         why='The slide is photographed beside (a); scheme p16 describes TIG welding in '
             'three sentences beside a labelled diagram, shown with the answer. "8".',
         lifted=[S(16, 106, 365, 345, 397), S(16, 106, 398, 366, 465),
                 S(16, 106, 466, 443, 482)],
         tariff='questionTotal', total=8,
         question_figure='engineering-2019-HL-paper-q5a-crop',
         figure='engineering-2019-HL-scheme-q5ai-sol',
         notes="The scheme prints '8'."),
    dict(key=(5, 'a', 'ii'), topic='eng-2-10',
         replaces=NEW + 'set "4 + 4" over three equal reasons as an ordered split',
         why='Scheme p16 lists three reasons, "4 + 4" for two.',
         lifted=[[S(16, 142, 534, 355, 550), S(16, 142, 551, 474, 567),
                  S(16, 142, 569, 364, 585)]],
         row_kind='anyN', group=(2, 4), marks=[8], tariff='fixed', total=8,
         notes="The scheme prints '4 + 4'."),
    dict(key=(5, 'b', 'iii'),
         why='Scheme p17 introduces friction welding and describes three kinds beside '
             'their drawings, which are shown with the answer; "Any Three @ 6 + 6 + 6".',
         topic='eng-2-10',
         lifted=[S(17, 106, 72, 545, 105), S(17, 107, 143, 336, 243),
                 S(17, 322, 291, 553, 391), S(17, 107, 433, 333, 483)],
         tariff='questionTotal', total=6,
         figure='engineering-2019-HL-scheme-q5biii-sol',
         notes="The scheme prints 'Any Three @ 6 + 6 + 6'."),
    dict(key=(5, 'c', None),
         why='Paper p8 sets two alternative (c)s either side of an OR. This card is the '
             'first branch, resistance welding, which has no romans; scheme p18 answers '
             'in a two-column table under four headings beside drawings of both, shown '
             'with the answer. Each cell is lifted with its column and row heads. "16".',
         topic='eng-2-10', stem=False,
         question_lift=P(8, 107, 465, 514, 576),
         lifted=[join(S(*_SPOT), S(*_ES), S(18, 75, 332, 318, 365)),
                 join(S(*_SEAM), S(*_ES), S(18, 323, 332, 556, 365)),
                 join(S(*_SPOT), S(*_WP), S(18, 76, 399, 316, 550)),
                 join(S(*_SEAM), S(*_WP), S(18, 324, 399, 558, 533)),
                 join(S(*_SPOT), S(*_AP), S(18, 75, 585, 313, 618)),
                 join(S(*_SEAM), S(*_AP), S(18, 323, 585, 548, 618)),
                 join(S(*_SPOT), S(*_SC), S(18, 74, 661, 303, 710)),
                 join(S(*_SEAM), S(*_SC), S(18, 322, 661, 553, 710))],
         tariff='questionTotal', total=16,
         figure='engineering-2019-HL-scheme-q5c-sol', notes=_OR5),
    dict(key=(5, 'c', 'ii'), topic='eng-3-14',
         replaces=NEW + 'set "4 + 4" over one row holding every application',
         why='The OR branch\'s (ii); scheme p19 names the applications in one sentence; '
             'each is lifted by word rectangle. "4 + 4" for two.',
         lifted=[[S(19, 106, 215, 190, 231), S(19, 190, 215, 260, 231),
                  join(S(19, 260, 215, 523, 231), S(19, 106, 230, 249, 246)),
                  join(S(19, 249, 230, 532, 246), S(19, 106, 244, 152, 260)),
                  S(19, 152, 244, 480, 260),
                  join(S(19, 480, 244, 542, 260), S(19, 106, 259, 203, 275))]],
         row_kind='anyN', group=(2, 4), marks=[8], tariff='fixed', total=8,
         question_figure='engineering-2019-HL-paper-q5ci-art', notes=_OR5),
    # ---- Question 6 --------------------------------------------------------
    dict(key=(6, 'a', 'i'),
         why='The oarlock body is photographed and captioned beside (a); scheme p19 '
             'lists the properties after "Properties:"; each is lifted by word rectangle. '
             '"3 + 3" for two.',
         topic='eng-1-9',
         lifted=[[S(19, 164, 482, 324, 498), S(19, 324, 482, 400, 498),
                  S(19, 400, 482, 512, 498),
                  join(S(19, 512, 482, 558, 498), S(19, 106, 499, 227, 515)),
                  S(19, 227, 499, 452, 515)]],
         row_kind='anyN', group=(2, 3), marks=[6], tariff='fixed', total=6,
         question_figure='engineering-2019-HL-paper-q6a-crop',
         notes="The scheme prints '3 + 3'."),
    dict(key=(6, 'a', 'ii'),
         why='Scheme pp19-20 name injection moulding and describe it in paragraphs beside '
             'a labelled diagram, shown with the answer; "10".',
         topic='eng-1-9',
         lifted=[S(19, 106, 547, 208, 566), S(19, 106, 566, 538, 599),
                 S(19, 106, 749, 392, 765), S(20, 106, 72, 564, 122),
                 S(20, 106, 123, 541, 156), S(20, 106, 157, 555, 206)],
         tariff='questionTotal', total=10,
         question_figure='engineering-2019-HL-paper-q6a-crop',
         figure='engineering-2019-HL-scheme-q6aii-sol',
         notes="The scheme prints '10'."),
    # ---- Question 7 --------------------------------------------------------
    dict(key=(7, 'b', 'i'), topic='eng-2-11',
         replaces=NEW + 'gave down-cut milling without its "Down-cut milling" heading, '
                  'and without the diagrams the part asks for',
         why='Scheme p21 describes each method under its name over drawings of both, '
             'shown with the answer; "Any three @ 6 + 6 + 6".',
         lifted=[S(21, 106, 421, 564, 473),
                 join(S(21, 106, 471, 201, 490), S(21, 106, 491, 564, 558))],
         tariff='questionTotal', total=6,
         figure='engineering-2019-HL-scheme-q7bi-sol',
         notes="The scheme prints 'Any three @ 6 + 6 + 6'."),
    dict(key=(7, 'b', 'ii'),
         why='Scheme pp21-22 list four features under a heading; the part is priced '
             '"Any three @ 6 + 6 + 6".',
         topic='eng-3-1',
         lifted=[S(21, 142, 746, 517, 762), S(22, 142, 73, 482, 89),
                 S(22, 142, 90, 377, 106), S(22, 142, 108, 499, 124)],
         tariff='questionTotal', total=6,
         notes="The scheme prints 'Any three @ 6 + 6 + 6'."),
    dict(key=(7, 'b', 'iv'), topic='eng-2-11',
         replaces=NEW + 'gave the explanation without the diagram the part asks for',
         why='Scheme p22 explains both angles beside a labelled drawing, shown with the '
             'answer; "Any three @ 6 + 6 + 6".',
         lifted=[S(22, 106, 231, 441, 251), S(22, 106, 251, 410, 267),
                 S(22, 106, 268, 334, 284), S(22, 106, 293, 436, 329)],
         tariff='questionTotal', total=6,
         figure='engineering-2019-HL-scheme-q7biv-sol',
         notes="The scheme prints 'Any three @ 6 + 6 + 6'."),
    dict(key=(7, 'b', 'v'), topic='eng-2-11',
         replaces=NEW + 'carried the drawing\'s label "Nut and bolt on vice" as a second '
                  'answer',
         why='Scheme p22 answers in one sentence beside a drawing of the bolted vice, '
             'shown with the answer; "Any three @ 6 + 6 + 6".',
         lifted=[S(22, 106, 346, 309, 379)], marks=[6], total=6,
         figure='engineering-2019-HL-scheme-q7bv-sol',
         notes="The scheme prints 'Any three @ 6 + 6 + 6'."),
    dict(key=(7, 'c', 'i'), topic='eng-2-11',
         replaces=NEW + 'carried both OR branches as one question total with no route '
                  'between them',
         why='Both (c)s price their (i) at 8 (scheme pp22-23): the insert-making process, '
             'or productivity and reliability, "4 + 4". One card for the printed OR, each '
             'branch a route of its own.',
         question_lift=P(10, *_C7A, more=[(133, 491, 425, 507), _OR7, _C7B,
                                          (133, 638, 374, 689)]), stem=False,
         lifted=[S(22, 106, 493, 564, 712), S(23, 106, 194, 561, 245),
                 join(S(23, 106, 244, 561, 262), S(23, 106, 262, 500, 280))],
         marks=[8, 4, 4], routes=['a', 'b', 'b'], total=8, notes=_OR7N),
    dict(key=(7, 'c', 'ii'), topic='eng-2-11',
         replaces=NEW + 'carried both OR branches as one ordered split, so a CNC answer '
                  'counted against the inserts and the tariff "4 + 4" was an answer',
         why='Both (c)s price their (ii) "4 + 4" (scheme p23): two of four insert '
             'advantages, or the two CNC operations. One card, each branch a route.',
         question_lift=P(10, *_C7A, more=[(133, 520, 459, 536), _OR7, _C7B,
                                          (134, 707, 382, 757)]), stem=False,
         lifted=[[S(23, 142, 73, 532, 103), S(23, 142, 103, 389, 118),
                  S(23, 142, 118, 551, 148), S(23, 142, 148, 495, 164)],
                 S(23, 106, 293, 557, 344), S(23, 106, 343, 527, 395)],
         row_kind='anyN', group=[(2, 4), None, None], marks=[8, 4, 4],
         routes=['a', 'b', 'b'], tariff='fixed', total=8, notes=_OR7N),
    # ---- Question 8 --------------------------------------------------------
    dict(key=(8, 'a', 'i'), topic='eng-2-15',
         replaces=NEW + 'gave the description without the diagram the part asks for',
         why='The 3D printer is photographed beside (a); scheme p23 describes the '
             'leadscrew beside a labelled diagram, shown with the answer; "8".',
         lifted=[S(23, 106, 462, 295, 596)], marks=[8], total=8,
         question_figure='engineering-2019-HL-paper-q8a-crop',
         figure='engineering-2019-HL-scheme-q8ai-sol',
         notes="The scheme prints '8'."),
    dict(key=(8, 'a', 'ii'), topic='eng-2-15',
         replaces=NEW + 'gave the description without the diagram the part asks for',
         why='Scheme p23 describes the toothed belt drive beside a labelled diagram, shown '
             'with the answer; "8".',
         lifted=[S(23, 106, 628, 289, 677), S(23, 106, 678, 318, 694)],
         tariff='questionTotal', total=8,
         question_figure='engineering-2019-HL-paper-q8a-crop',
         figure='engineering-2019-HL-scheme-q8aii-sol',
         notes="The scheme prints '8'."),
    dict(key=(8, 'b', 'i'), replaces=OWNED,
         why='Scheme p24 answers in one paragraph beside a labelled worm and worm gear, '
             'shown with the answer; "Any three @ 6 + 6 + 6".',
         topic='eng-2-15',
         lifted=[S(24, 106, 72, 318, 132)], marks=[6], total=6,
         figure='engineering-2019-HL-scheme-q8bi-sol',
         notes="The scheme prints 'Any three @ 6 + 6 + 6'."),
    dict(key=(8, 'b', 'iv'), topic='eng-2-15',
         replaces=NEW + 'gave the description without the diagram the part asks for',
         why='Scheme p24 answers in one paragraph beside a labelled idler gear, shown with '
             'the answer; "Any three @ 6 + 6 + 6".',
         lifted=[S(24, 106, 259, 397, 311)], marks=[6], total=6,
         figure='engineering-2019-HL-scheme-q8biv-sol',
         notes="The scheme prints 'Any three @ 6 + 6 + 6'."),
    dict(key=(8, 'b', 'v'), topic='eng-2-15',
         replaces=NEW + 'did not show the ratchet and pawl drawing its answer is given '
                  'beside',
         why='Scheme p24 answers in two sentences beside a labelled ratchet and pawl, '
             'shown with the answer; "Any three @ 6 + 6 + 6".',
         lifted=[S(24, 106, 341, 355, 371), S(24, 106, 370, 345, 401)],
         tariff='questionTotal', total=6,
         figure='engineering-2019-HL-scheme-q8bv-sol',
         notes="The scheme prints 'Any three @ 6 + 6 + 6'."),
    dict(key=(8, 'c', 'i'),
         why='Both (c)s price their (i) at 8 (scheme pp24-25): the folding boom beside '
             'its labelled drawings (shown with the answer), or the transformer\'s '
             'function. One card for the printed OR, each branch a route of its own.',
         topic='eng-2-15',
         question_lift=P(11, *_C8A, more=[(134, 518, 363, 550), _OR8, _C8B,
                                          (134, 703, 402, 736)]), stem=False,
         lifted=[S(24, 106, 458, 527, 491), S(25, 105, 116, 540, 149)],
         marks=[8, 8], routes=['a', 'b'], total=8,
         question_figure='engineering-2019-HL-paper-q8c-crop',
         figure='engineering-2019-HL-scheme-q8ci-sol', notes=_OR8N),
    dict(key=(8, 'c', 'ii'),
         why='Both (c)s price their (ii) at 8 (scheme pp24-25): an advantage and a '
             'disadvantage of the boom, "4 + 4", or any one component of the circuit, '
             'each lifted by word rectangle from its list. One card, each branch a route.',
         topic='eng-2-15',
         question_lift=P(11, *_C8A, more=[(134, 561, 368, 594), _OR8, _C8B,
                                          (134, 747, 390, 763)]), stem=False,
         lifted=[S(24, 105, 667, 543, 703),
                 join(S(24, 105, 701, 549, 737), S(24, 105, 737, 345, 753)),
                 [S(25, 106, 165, 131, 181), S(25, 131, 165, 187, 181),
                  S(25, 187, 165, 220, 181), S(25, 220, 165, 298, 181),
                  S(25, 298, 165, 366, 181)]],
         marks=[4, 4, 8], routes=['a', 'a', 'b'], total=8,
         question_figure='engineering-2019-HL-paper-q8c-crop', notes=_OR8N),
]

TOPICS = {
    'eng-2019-hl-q6-b-ii': ('eng-1-9', 'elastic memory and elasticity in thermoplastics is '
                            'plastics; "elasticity" outvoted it for testing'),
}

_MM = 'Machining & Metrology'

ATLAS = {
    'eng-2019-hl-q1-e': dict(
        topics=['Mechanisms'],
        note='A keyway and grub screw fixing the conveyor wheel to the stepper motor '
             'shaft; the reference lists no joining topic for Q1. The card\'s syllabus '
             'heading is Joining of materials.'),
    'eng-2019-hl-q3-b-i': dict(
        topics=['Equilibrium Diagrams'],
        note='The regions A and B, read off the iron-carbon diagram the part is printed under; the '
             'card\'s syllabus heading is Iron and steel.'),
    'eng-2019-hl-q3-b-ii': dict(
        topics=['Equilibrium Diagrams'],
        note='Steels X and Y at 0.2% and 1.5% carbon, read off the iron-carbon diagram the part is printed under; the '
             'card\'s syllabus heading is Iron and steel.'),
    'eng-2019-hl-q3-b-iii': dict(
        topics=['Equilibrium Diagrams'],
        note='The point C, read off the iron-carbon diagram the part is printed under; the '
             'card\'s syllabus heading is Iron and steel.'),
    'eng-2019-hl-q5-c-i': dict(
        topics=['Energy, Electronics & Robotics'],
        note='The robotic exoskeleton suit (the OR branch of Q5(c)); the card\'s '
             'syllabus heading is Technology, where the syllabus places robotics.'),
    'eng-2019-hl-q5-c-ii': dict(
        topics=['Energy, Electronics & Robotics'],
        note='Robotic control in medicine (the OR branch of Q5(c)); the card\'s '
             'syllabus heading is Technology, where the syllabus places robotics.'),
    'eng-2019-hl-q7-b-ii': dict(
        topics=[_MM],
        note='Safety features of a bench grinder, a machine tool, which the reference '
             'files with the rest of Q7; the card\'s syllabus heading is Health and '
             'safety.'),
}
