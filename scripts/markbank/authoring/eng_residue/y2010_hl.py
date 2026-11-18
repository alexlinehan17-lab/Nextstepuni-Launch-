"""2010 Higher Level: the parts eng_all refuses or gets wrong, from the page.

Paper and scheme as the PDFs number their pages (the scheme's printed "Page 1"
is its pdf page 3). The marks grid is on scheme p4: Question 1 is Section A,
"Any ten @ 5 marks each", and Section B, "Answer all of the following", (n) to
(r); Questions 2-8 are 50 marks each. The scheme prints a part's marks under
its answer ("(Any two) 3 + 2", "(Any three) 6 + 6 + 6"), as 2011 does. This
sitting had no cards before the lane: every card here is new, and a
`replaces=` names the automatic card it rebuilds before it ever shipped.
"""
from eng_lift import cells, join, lift

Y, L = 2010, 'hl'
NEW = 'never shipped: the automatic card '


def S(page, *rect):
    return lift(Y, L, 'scheme', page, rect)


def P(page, *rect, more=(), items=()):
    return lift(Y, L, 'paper', page, rect, more=more, items=items)


def _ck(page, part, lead):
    return (f'Paper p{page} prints {part} as one item of the list under "{lead}"; the '
            'semicolon ends the item, not the question.')


# Paper stems the parts are lifted with.
_N1 = (150, 130, 620, 147)            # p4: Q1(n), "Outline the benefits ... each of the"
_N1F = (150, 147, 280, 163)           # p4: "following applications:"
_A2 = (180, 137, 385, 196)            # p5: Q2(a)(ii), the test in the diagram
_B2 = (150, 318, 510, 366)            # p5: Q2(b), the tensile results
_B2U = (150, 489, 465, 520)           # p5: "Using the graph paper supplied, plot ..."
_C2 = (150, 625, 590, 662)            # p5: Q2(c), the two NDTs
_B3 = (150, 280, 495, 297)            # p6: Q3(b), the iron-carbon diagram
_C3 = (148, 639, 515, 656)            # p6: Q3(c), the lathe bed's guideways
_B4 = (150, 268, 395, 285)            # p7: Q4(b), the lead-tin diagram
_A5 = (150, 96, 475, 113)             # p8: Q5(a), processes A and B
_C5B = (150, 655, 450, 686)           # p8: the robotics (c)
_A6 = (150, 96, 402, 113)             # p9: Q6(a), the polymer process
_B7 = (150, 264, 495, 295)            # p10: Q7(b), the chips
_C8B = (150, 553, 490, 570)           # p11: the circuit (c)

_SA = "Section A is 'Any ten @ 5 marks each'."
_SB = 'Section B is "Answer all of the following".'
_A3 = "The scheme prints '(Any two) 8 + 8': each part answered earns 8."
_A5B = "The scheme prints '(Any three) 6 + 6 + 6': each part answered earns 6."
_A7 = "The scheme prints '(Any three) 6 + 6 + 6': each part answered earns 6."
_OR5 = ('The paper sets two (c)s either side of an OR: electro-slag or oxyacetylene '
        'welding, "(Any one) 16", carded at the letter, and the robotics (c), whose (i), '
        '(ii) and (iii) are carded apart.')
_OR7 = ('The paper sets two (c)s either side of an OR: the magnetic or four-jaw chuck, "Any '
        'one @ 16", carded at the letter, and the CNC (c), whose (i) and (ii) are carded '
        'apart.')
_OR8 = ('The paper sets two (c)s either side of an OR: the dental chair\'s mechanism, "16", '
        'carded at the letter, and the parking-light circuit (c), whose (i) and (ii) are '
        'carded apart.')

CROPS = {
    # ---- paper ------------------------------------------------------------
    # The three signs with their captions.
    'engineering-2010-HL-paper-q1a-crop': dict(
        doc='paper', page=3, rect=(180, 185, 428, 258), ref='2010 HL Q1(a)'),
    'engineering-2010-HL-paper-q1e-crop': dict(
        doc='paper', page=3, rect=(265, 390, 412, 425), ref='2010 HL Q1(e)'),
    # The cooling curve A and the diagram B, without the page footer.
    'engineering-2010-HL-paper-q1m-crop': dict(
        doc='paper', page=3, rect=(305, 678, 572, 797), mask=[(304, 792.5, 340, 798)],
        ref='2010 HL Q1(m)', letters=('A', 'B')),
    'engineering-2010-HL-paper-q1n-crop': dict(
        doc='paper', page=4, rect=(280, 148, 470, 226), ref='2010 HL Q1(n)'),
    'engineering-2010-HL-paper-q1p-crop': dict(
        doc='paper', page=4, rect=(148, 436, 560, 568), ref='2010 HL Q1(p)'),
    'engineering-2010-HL-paper-q1r-crop': dict(
        doc='paper', page=4, rect=(460, 706, 556, 800), ref='2010 HL Q1(r)'),
    'engineering-2010-HL-paper-q2a-crop': dict(
        doc='paper', page=5, rect=(388, 116, 536, 260), ref='2010 HL Q2(a)(ii)'),
    # The table of loads and extensions.
    'engineering-2010-HL-paper-q2b-crop': dict(
        doc='paper', page=5, rect=(45, 405, 562, 470), ref='2010 HL Q2(b)'),
    'engineering-2010-HL-paper-q3b-crop': dict(
        doc='paper', page=6, rect=(140, 315, 535, 522), ref='2010 HL Q3(b)',
        letters=('A', 'B', 'C', 'D')),
    'engineering-2010-HL-paper-q4b-crop': dict(
        doc='paper', page=7, rect=(175, 298, 468, 468), ref='2010 HL Q4(b)',
        letters=('A', 'B', 'C', 'D')),
    'engineering-2010-HL-paper-q5a-crop': dict(
        doc='paper', page=8, rect=(150, 115, 520, 267), ref='2010 HL Q5(a)',
        letters=('A', 'B')),
    'engineering-2010-HL-paper-q5cor-crop': dict(
        doc='paper', page=8, rect=(452, 668, 553, 775), ref='2010 HL Q5(c)'),
    'engineering-2010-HL-paper-q6a-crop': dict(
        doc='paper', page=9, rect=(118, 115, 500, 268), ref='2010 HL Q6(a)'),
    # The three chips with their letters and "Built-up edge".
    'engineering-2010-HL-paper-q7b-crop': dict(
        doc='paper', page=10, rect=(115, 290, 560, 399), ref='2010 HL Q7(b)',
        letters=('A', 'B', 'C')),
    'engineering-2010-HL-paper-q8c-crop': dict(
        doc='paper', page=11, rect=(415, 390, 535, 515), ref='2010 HL Q8(c)'),
    'engineering-2010-HL-paper-q8cor-crop': dict(
        doc='paper', page=11, rect=(120, 620, 545, 780), ref='2010 HL Q8(c)',
        letters=('A', 'B', 'C', 'D')),
    # ---- scheme: the drawings, tables and workings the answers are given with
    'engineering-2010-HL-scheme-q1b-sol': dict(
        doc='scheme', page=5, rect=(118, 359, 440, 498), solution=True, ref='2010 HL Q1(b)'),
    'engineering-2010-HL-scheme-q1m-sol': dict(
        doc='scheme', page=7, rect=(150, 282, 485, 446), solution=True, ref='2010 HL Q1(m)'),
    'engineering-2010-HL-scheme-q1o-sol': dict(
        doc='scheme', page=8, rect=(474, 38, 540, 318), solution=True, ref='2010 HL Q1(o)'),
    'engineering-2010-HL-scheme-q1q-sol': dict(
        doc='scheme', page=9, rect=(366, 158, 588, 263), solution=True, ref='2010 HL Q1(q)'),
    'engineering-2010-HL-scheme-q2b-sol': dict(
        doc='scheme', page=10, rect=(60, 60, 580, 320), solution=True, ref='2010 HL Q2(b)'),
    # The UTS worked as a stacked fraction the text layer flattens.
    'engineering-2010-HL-scheme-q2bi-sol': dict(
        doc='scheme', page=10, rect=(100, 380, 480, 422), solution=True, ref='2010 HL Q2(b)(i)'),
    # The proof stress worked as a stacked fraction the text layer flattens.
    'engineering-2010-HL-scheme-q2bii-sol': dict(
        doc='scheme', page=10, rect=(100, 470, 480, 545), solution=True, ref='2010 HL Q2(b)(ii)'),
    'engineering-2010-HL-scheme-q2ci-sol': dict(
        doc='scheme', page=10, rect=(440, 592, 555, 728), solution=True, ref='2010 HL Q2(c)(i)'),
    'engineering-2010-HL-scheme-q2cii-sol': dict(
        doc='scheme', page=11, rect=(380, 55, 597, 258), mask=[(512, 246, 528, 262)], solution=True, ref='2010 HL Q2(c)(ii)'),
    'engineering-2010-HL-scheme-q3aii-sol': dict(
        doc='scheme', page=11, rect=(383, 465, 585, 675), solution=True, ref='2010 HL Q3(a)(ii)'),
    'engineering-2010-HL-scheme-q3bii-sol': dict(
        doc='scheme', page=12, rect=(140, 166, 200, 226), solution=True, ref='2010 HL Q3(b)(ii)'),
    'engineering-2010-HL-scheme-q3cii-sol': dict(
        doc='scheme', page=12, rect=(380, 294, 592, 452), solution=True, ref='2010 HL Q3(c)(ii)'),
    'engineering-2010-HL-scheme-q4a-sol': dict(
        doc='scheme', page=12, rect=(408, 532, 535, 645), solution=True, ref='2010 HL Q4(a)(i)'),
    'engineering-2010-HL-scheme-q4biii-sol': dict(
        doc='scheme', page=13, rect=(155, 553, 462, 722), solution=True, ref='2010 HL Q4(b)(iii)'),
    'engineering-2010-HL-scheme-q5aiii-sol': dict(
        doc='scheme', parts=[(14, (412, 548, 545, 712)), (15, (95, 87, 222, 240))],
        layout='row', solution=True, ref='2010 HL Q5(a)(iii)'),
    'engineering-2010-HL-scheme-q5c-sol': dict(
        doc='scheme', parts=[(16, (320, 96, 555, 255)), (16, (155, 285, 420, 472))],
        layout='row', solution=True, ref='2010 HL Q5(c)'),
    # The whole comparison table, with its drawings of the chains.
    'engineering-2010-HL-scheme-q6b-sol': dict(
        doc='scheme', page=17, rect=(130, 262, 532, 720), solution=True, ref='2010 HL Q6(b)'),
    'engineering-2010-HL-scheme-q7aii-sol': dict(
        doc='scheme', page=18, rect=(378, 640, 552, 782), solution=True, ref='2010 HL Q7(a)(ii)'),
    'engineering-2010-HL-scheme-q7c-sol': dict(
        doc='scheme', parts=[(19, (395, 618, 510, 667)), (20, (462, 170, 552, 264))],
        layout='row', solution=True, ref='2010 HL Q7(c)'),
    'engineering-2010-HL-scheme-q8c-sol': dict(
        doc='scheme', page=21, rect=(120, 622, 515, 780), solution=True, ref='2010 HL Q8(c)'),
}

SPLIT = {
    'eng-2010-hl-q7-a': 'never shipped: "Answer any three of the following" over five '
                        'separate questions, each priced at 6; the automatic card ran all '
                        'five answers into one ordered split at the letter, one row the '
                        'scheme\'s "(Any three) 6 + 6 + 6"',
}

FOLDED = {}

CARDS = [
    # ---- Question 1, Section A ("Any ten @ 5 marks each") ------------------
    dict(key=(1, 'a', None),
         why='The three signs are pictured and captioned (i)-(iii); scheme p5 gives each '
             'sign\'s purpose under it, "(Any two) 3 + 2".',
         topic='eng-3-1',
         lifted=[S(5, 100, 286, 240, 302), S(5, 245, 286, 385, 316), S(5, 390, 286, 515, 316)],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         question_figure='engineering-2010-HL-paper-q1a-crop',
         notes="The scheme prints '(Any two) 3 + 2', for the signs' purposes under (i), (ii) "
               "and (iii). " + _SA),
    dict(key=(1, 'b', None),
         why='Scheme p5 describes the process under a labelled drawing, shown with the '
             'answer, "5". The drawing\'s labels are left out of the words.',
         topic='eng-1-2',
         lifted=[S(5, 104, 506, 525, 550)], marks=[5], total=5,
         figure='engineering-2010-HL-scheme-q1b-sol',
         notes="The scheme prints '5'. " + _SA),
    dict(key=(1, 'c', None),
         why='Scheme p5 bullets four reasons, "(Any two) 3 + 2".',
         topic='eng-3-14',
         lifted=[S(5, 140, 586, 525, 615.5), S(5, 140, 615.5, 525, 630),
                 S(5, 140, 630, 525, 644.5), S(5, 140, 644.5, 525, 658.5)],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         notes="The scheme prints '(Any two) 3 + 2'. " + _SA),
    dict(key=(1, 'd', None),
         why='Scheme p5 bullets five treatments, "(Any two) 3 + 2".',
         topic='eng-3-7',
         lifted=[S(5, 140, 695, 300, 711), S(5, 140, 711, 300, 725.5),
                 S(5, 140, 725.5, 300, 740), S(5, 140, 740, 300, 754.5),
                 S(5, 140, 754.5, 300, 770)],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         notes="The scheme prints '(Any two) 3 + 2'. " + _SA),
    dict(key=(1, 'e', None),
         why='The broken specimen is pictured beside (e); scheme p6 describes the fracture in '
             'one paragraph, "5".',
         topic='eng-3-8',
         lifted=[S(6, 104, 84, 525, 128)], marks=[5], total=5,
         question_figure='engineering-2010-HL-paper-q1e-crop',
         notes="The scheme prints '5'. " + _SA),
    dict(key=(1, 'f', None),
         why='Scheme p6 bullets eight applications, "(Any three) 2 + 2+ 1".',
         topic='eng-2-15',
         lifted=[S(6, 140, 168, 525, 184), S(6, 140, 184, 525, 198.5), S(6, 140, 198.5, 525, 213),
                 S(6, 140, 213, 525, 227.5), S(6, 140, 227.5, 525, 242.5),
                 S(6, 140, 242.5, 525, 257), S(6, 140, 257, 525, 271.5),
                 S(6, 140, 271.5, 525, 286.5)],
         tariff='orderedSplit', notation='2 + 2 + 1', ladder=5, total=5,
         notes="The scheme prints '(Any three) 2 + 2+ 1'. " + _SA),
    dict(key=(1, 'g', None),
         why='Scheme p6 expands each abbreviation after its roman; "(Any two) 3 + 2".',
         topic='eng-3-14',
         lifted=[S(6, 140, 312, 400, 328), S(6, 140, 328, 400, 341.5),
                 S(6, 140, 341.5, 400, 355.5), S(6, 140, 355.5, 400, 369)],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         notes="The scheme prints '(Any two) 3 + 2'. " + _SA),
    dict(key=(1, 'h', None),
         why='Scheme p6 answers in one paragraph, "5".',
         topic='eng-2-11',
         lifted=[S(6, 104, 395, 525, 452)], marks=[5], total=5,
         notes="The scheme prints '5'. " + _SA),
    dict(key=(1, 'i', None),
         why='A lead-in over three people set as romans, "any one"; scheme p6 writes a note '
             'on each after the name, "(Any one) 5". The question is lifted from the page '
             'with the people\'s line.',
         topic='eng-3-14',
         question_lift=P(3, 150, 529, 490, 560),
         lifted=[[join(S(6, 140, 477, 525, 492.5), S(6, 104, 492.5, 525, 535)),
                  join(S(6, 140, 546, 525, 561.5), S(6, 104, 561.5, 525, 576)),
                  join(S(6, 140, 588, 525, 603.5), S(6, 104, 603.5, 525, 631.5))]],
         row_kind='anyN', group=(1, 5), marks=[5], tariff='fixed', total=5,
         notes="The scheme prints '(Any one) 5'. " + _SA),
    dict(key=(1, 'j', None),
         why='Scheme p6 bullets four methods, "3 + 2".',
         topic='eng-2-10',
         lifted=[S(6, 140, 671, 300, 687.5), S(6, 140, 687.5, 300, 702),
                 S(6, 140, 702, 300, 716.5), S(6, 140, 716.5, 300, 731)],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         notes="The scheme prints '3 + 2'. " + _SA),
    dict(key=(1, 'k', None),
         why='Scheme p7 answers in one paragraph, "5".',
         topic='eng-3-8',
         lifted=[S(7, 104, 70, 525, 128)], marks=[5], total=5,
         notes="The scheme prints '5'. " + _SA),
    dict(key=(1, 'l', None),
         why='Scheme p7 bullets the three defects, "2 + 2 + 1".',
         topic='eng-1-3',
         lifted=[S(7, 140, 168, 300, 184), S(7, 140, 184, 300, 198.5), S(7, 140, 198.5, 300, 213)],
         tariff='orderedSplit', notation='2 + 2 + 1', ladder=5, total=5,
         notes="The scheme prints '2 + 2 + 1'. " + _SA),
    dict(key=(1, 'm', None),
         why='The cooling curve A and the diagram B are drawn beside (m); scheme p7 answers '
             'in two paragraphs either side of a drawing, shown with the answer, "5". The '
             'drawing\'s labels are left out of the words.',
         topic='eng-1-3',
         lifted=[join(S(7, 104, 239, 525, 282), S(7, 104, 454, 525, 484))], marks=[5], total=5,
         question_figure='engineering-2010-HL-paper-q1m-crop',
         figure='engineering-2010-HL-scheme-q1m-sol',
         notes="The scheme prints '5'. " + _SA),
    # ---- Question 1, Section B ("Answer all of the following") -------------
    dict(key=(1, 'n', 'i'),
         why='Scheme p7 answers in one paragraph under its heading; "8 + 7", 8 for (i).',
         topic='eng-3-14', stem=False,
         question_lift=P(4, *_N1, more=[_N1F, (172, 162, 280, 179)]),
         lifted=[S(7, 104, 592, 525, 636)], marks=[8], total=8,
         question_figure='engineering-2010-HL-paper-q1n-crop',
         notes="The scheme prints '8 + 7', for (i) and (ii) in that order. " + _SB),
    dict(key=(1, 'n', 'ii'),
         why='Scheme p7 answers in one paragraph under its heading; "8 + 7", 7 for (ii).',
         topic='eng-3-14', stem=False,
         question_lift=P(4, *_N1, more=[_N1F, (172, 183, 280, 200)]),
         lifted=[S(7, 104, 661, 525, 718)], marks=[7], total=7,
         question_figure='engineering-2010-HL-paper-q1n-crop',
         notes="The scheme prints '8 + 7', for (i) and (ii) in that order. " + _SB),
    dict(key=(1, 'o', None),
         why='A lead-in over five movements set as romans, "any three"; scheme p8 explains '
             'each under its name beside a small drawing of it, shown with the answer; '
             '"(Any three) 4 + 3 + 3".',
         topic='eng-3-14', stem=False,
         lifted=[S(8, 140, 70, 470, 100), S(8, 140, 112, 470, 142), S(8, 140, 165, 470, 195),
                 S(8, 140, 215, 470, 245), S(8, 140, 257, 470, 287)],
         tariff='orderedSplit', notation='4 + 3 + 3', ladder=10, total=10,
         figure='engineering-2010-HL-scheme-q1o-sol',
         notes="The scheme prints '(Any three) 4 + 3 + 3'. It numbers rotation '(iv)', the "
               "paper's (v). " + _SB),
    dict(key=(1, 'p', None),
         why='The accelerometer is pictured under (p); scheme p8 describes its principle in '
             'paragraphs under its heading, "5".',
         topic='eng-3-14', stem=False,
         lifted=[join(S(8, 104, 367, 525, 437.5), S(8, 104, 437.5, 385, 549))], marks=[5],
         total=5,
         question_figure='engineering-2010-HL-paper-q1p-crop',
         notes="The scheme prints '5'. " + _SB),
    dict(key=(1, 'q', None),
         why='A lead-in over three topics set as romans, "any two"; scheme pp8-9 answer each '
             'under its roman, the hot gas sensor beside drawings, shown with the answer; '
             '"(Any two) 5 + 5".',
         topic='eng-3-14', stem=False,
         lifted=[[S(8, 140, 588, 525, 748), S(9, 140, 70, 525, 128),
                  join(S(9, 140, 139, 525, 155.5), S(9, 140, 155.5, 362, 280))]],
         row_kind='anyN', group=(2, 5), marks=[10], tariff='fixed', total=10,
         figure='engineering-2010-HL-scheme-q1q-sol',
         notes="The scheme prints '(Any two) 5 + 5'. " + _SB),
    dict(key=(1, 'r', None),
         why='The game controller is pictured beside (r); scheme p9 explains each force in a '
             'paragraph, "5 + 5".',
         topic='eng-3-14', stem=False,
         lifted=[S(9, 104, 319, 525, 337), S(9, 104, 346, 525, 376)], marks=[5, 5], total=10,
         question_figure='engineering-2010-HL-paper-q1r-crop',
         notes="The scheme prints '5 + 5', for static and dynamic forces in that order. " + _SB),
    # ---- Question 2 --------------------------------------------------------
    dict(key=(2, 'a', 'i'),
         why='Scheme p9 bullets four reasons, "4 + 4".',
         topic='eng-3-8',
         lifted=[S(9, 175, 499, 525, 528.5), S(9, 175, 528.5, 525, 543.5),
                 S(9, 175, 543.5, 525, 558), S(9, 175, 558, 525, 573)],
         tariff='orderedSplit', notation='4 + 4', ladder=8, total=8,
         notes="The scheme prints '4 + 4'."),
    dict(key=(2, 'a', 'ii'),
         why='The impact tester is drawn beside (ii); scheme p9 states the purpose, then '
             'describes the operation; "10", which the grid on p4 prices "Purpose 4", '
             '"Operation 6".',
         topic='eng-3-8', stem=False,
         question_lift=P(5, *_A2, items=[(195, 200, 320, 217), (195, 222, 320, 239)]),
         lifted=[S(9, 140, 612, 525, 641.5), S(9, 140, 641.5, 525, 724.5)],
         marks=[4, 6], total=10,
         question_figure='engineering-2010-HL-paper-q2a-crop',
         notes="The scheme prints '10' under the answer; its marks grid prints 'Purpose 4' and "
               "'Operation 6'."),
    dict(key=(2, 'b', None),
         why='"Plot the load-extension diagram": scheme p10 answers with the plotted graph, '
             'shown with the answer, "10" (the grid\'s "Plot graph 10"). The plot is asked '
             'at the letter, so the card is the letter\'s.',
         topic='eng-3-8', stem=False,
         question_lift=P(5, *_B2, more=[_B2U]),
         special={'kind': 'ask'}, total=10,
         question_figure='engineering-2010-HL-paper-q2b-crop',
         figure='engineering-2010-HL-scheme-q2b-sol',
         notes="The scheme prints 'Plot the graph' and '10'."),
    dict(key=(2, 'b', 'i'),
         why='Scheme p10 works the UTS as a stacked fraction the text layer flattens; the '
             'working is shown as printed, "4".',
         topic='eng-3-8', stem=False,
         question_lift=P(5, *_B2, more=[_B2U, (180, 522, 360, 539)]),
         special={'kind': 'ask'}, total=4,
         question_figure='engineering-2010-HL-paper-q2b-crop',
         figure='engineering-2010-HL-scheme-q2bi-sol',
         notes="The scheme prints '4'."),
    dict(key=(2, 'b', 'ii'),
         why='Scheme p10 works the proof stress as a stacked fraction the text layer '
             'flattens; the working is shown as printed, "2".',
         topic='eng-3-8', stem=False,
         question_lift=P(5, *_B2, more=[_B2U, (180, 542, 295, 560)]),
         special={'kind': 'ask'}, total=2,
         question_figure='engineering-2010-HL-paper-q2b-crop',
         figure='engineering-2010-HL-scheme-q2bii-sol',
         notes="The scheme prints '2'."),
    dict(key=(2, 'c', 'i'),
         why='Scheme p10 describes eddy current testing beside a drawing, shown with the '
             'answer, "8".',
         topic='eng-3-8', stem=False,
         question_lift=P(5, *_C2, more=[(178, 667, 285, 684)]),
         lifted=[S(10, 140, 636, 436, 749)], marks=[8], total=8,
         figure='engineering-2010-HL-scheme-q2ci-sol',
         notes="The scheme prints '8'."),
    dict(key=(2, 'c', 'ii'),
         why='Scheme p11 describes radiography beside a labelled drawing, shown with the '
             'answer, "8". The drawing\'s labels are left out of the words.',
         topic='eng-3-8', stem=False,
         question_lift=P(5, *_C2, more=[(178, 687, 320, 704)]),
         lifted=[S(11, 140, 98, 390, 238)], marks=[8], total=8,
         figure='engineering-2010-HL-scheme-q2cii-sol',
         notes="The scheme prints '8'."),
    # ---- Question 3 --------------------------------------------------------
    dict(key=(3, 'a', 'i'),
         checked=_ck(6, '(a)(i)', 'Select any two of the following:'),
         why='One of "Select any two of the following": scheme p11 answers in two paragraphs '
             'under its heading.',
         topic='eng-2-6',
         lifted=[S(11, 140, 342, 525, 455)], marks=[8], total=8, notes=_A3),
    dict(key=(3, 'a', 'ii'),
         checked=_ck(6, '(a)(ii)', 'Select any two of the following:'),
         why='One of "Select any two of the following": scheme p11 describes each pyrometer '
             'beside a drawing of it, shown with the answer, the 8 for the part not split '
             'between them.',
         topic='eng-2-6',
         lifted=[S(11, 140, 466, 390, 565), S(11, 140, 576, 390, 662)],
         tariff='questionTotal', total=8,
         figure='engineering-2010-HL-scheme-q3aii-sol', notes=_A3),
    dict(key=(3, 'a', 'iii'),
         replaces=NEW + 'read the scheme\'s "(Any two) 8 + 8" as a second point',
         why='One of "Select any two of the following": scheme p11 answers in one paragraph '
             'under its heading. Its first line sets the o of "40 o C" so high that a lift '
             'reads it as a line of its own, so the line is lifted in three pieces, in the '
             'order printed.',
         topic='eng-2-6',
         lifted=[join(S(11, 140, 699, 270.2, 710), S(11, 270, 690, 276.5, 703),
                      S(11, 276.5, 699, 525, 710), S(11, 140, 710, 525, 751))],
         marks=[8], total=8, notes=_A3),
    dict(key=(3, 'b', 'i'),
         why='The diagram is drawn with regions A-D; scheme p12 names each after its letter, '
             '"2 + 2 + 2 + 2".',
         topic='eng-1-3', stem=False,
         question_lift=P(6, *_B3, more=[(176, 541, 395, 558)]),
         lifted=[S(12, 140, 70, 300, 86), S(12, 140, 86, 300, 100), S(12, 140, 100, 300, 113.5),
                 S(12, 140, 113.5, 300, 128)],
         marks=[2, 2, 2, 2], total=8,
         labels={'A': S(12, 163, 70, 300, 86), 'B': S(12, 162, 86, 300, 100),
                 'C': S(12, 163, 100, 300, 113.5), 'D': S(12, 163, 113.5, 300, 128)},
         question_figure='engineering-2010-HL-paper-q3b-crop',
         notes="The scheme prints '2 + 2 + 2 + 2', for A, B, C and D in that order."),
    dict(key=(3, 'b', 'ii'),
         replaces=NEW + 'gave the martensite answer without the drawing the part asks for',
         why='Scheme p12 describes martensite beside a drawing of it, shown with the answer, '
             '"10".',
         topic='eng-1-3', stem=False,
         question_lift=P(6, *_B3, more=[(176, 568, 465, 601)]),
         lifted=[join(S(12, 140, 153, 525, 168.5), S(12, 240, 168.5, 525, 212))], marks=[10],
         total=10,
         figure='engineering-2010-HL-scheme-q3bii-sol',
         notes="The scheme prints '10'."),
    dict(key=(3, 'c', 'i'),
         replaces=NEW + 'asked about "the guideways" without the lathe bed that shows them',
         why='The lathe bed is drawn beside (c); scheme p12 answers in one sentence, "4".',
         topic='eng-2-6', stem=False,
         question_lift=P(6, *_C3, more=[(172, 672, 420, 721)]),
         lifted=[S(12, 140, 250, 525, 280)], marks=[4], total=4,
         question_figure='engineering-2010-HL-paper-q3ci-art',
         notes="The scheme prints '4'."),
    dict(key=(3, 'c', 'ii'),
         replaces=NEW + 'gave the answer without the drawing the part asks for',
         why='Scheme p12 describes induction hardening beside a labelled drawing, shown with '
             'the answer, "12". The drawing\'s labels are left out of the words.',
         topic='eng-2-6', stem=False,
         question_lift=P(6, *_C3, more=[(170, 731, 360, 765)]),
         lifted=[S(12, 140, 319, 378, 445)], marks=[12], total=12,
         question_figure='engineering-2010-HL-paper-q3ci-art',
         figure='engineering-2010-HL-scheme-q3cii-sol',
         notes="The scheme prints '12'."),
    # ---- Question 4 --------------------------------------------------------
    dict(key=(4, 'a', None),
         replaces=NEW + 'split the dislocation and age hardening answers into options of '
                        'their own and took "(Any two) 8 + 8" for an option',
         why='A lead-in over four terms set as romans, "any two"; scheme pp12-13 explain '
             'each under its roman, the dislocation beside a drawing, shown with the answer; '
             'one option each, "(Any two) 8 + 8".',
         topic='eng-1-3',
         lifted=[[S(12, 140, 553, 400, 639), S(12, 140, 664, 525, 735), S(13, 140, 84, 525, 142),
                  S(13, 140, 160, 525, 190)]],
         row_kind='anyN', group=(2, 8), marks=[16], tariff='fixed', total=16,
         figure='engineering-2010-HL-scheme-q4a-sol',
         notes="The scheme prints '(Any two) 8 + 8'."),
    dict(key=(4, 'b', 'i'),
         replaces=NEW + 'ran the four answers and "2 + 2 + 2 + 2" into one row',
         why='The diagram is drawn with point A and lines B-D; scheme p13 names each after '
             'its letter, "2 + 2 + 2 + 2".',
         topic='eng-1-3', stem=False,
         question_lift=P(7, *_B4, more=[(176, 489, 402, 506)]),
         lifted=[S(13, 140, 215, 300, 231), S(13, 140, 231, 300, 245), S(13, 140, 245, 300, 259),
                 S(13, 140, 259, 300, 273)],
         marks=[2, 2, 2, 2], total=8,
         labels={'A': S(13, 163, 215, 300, 231), 'B': S(13, 162, 231, 300, 245),
                 'C': S(13, 163, 245, 300, 259), 'D': S(13, 163, 259, 300, 273)},
         question_figure='engineering-2010-HL-paper-q4b-crop',
         notes="The scheme prints '2 + 2 + 2 + 2', for A, B, C and D in that order."),
    dict(key=(4, 'b', 'ii'),
         why='Scheme p13 describes seven features, each under its name, "6" for the part not '
             'split between them.',
         topic='eng-1-3', stem=False,
         question_lift=P(7, *_B4, more=[(176, 510, 387, 527)]),
         lifted=[S(13, 140, 298, 525, 328), S(13, 140, 333, 525, 362), S(13, 140, 367, 525, 397),
                 S(13, 140, 402, 525, 418), S(13, 140, 422, 525, 438), S(13, 140, 443, 525, 473),
                 S(13, 140, 477, 525, 493)],
         tariff='questionTotal', total=6,
         question_figure='engineering-2010-HL-paper-q4b-crop',
         notes="The scheme prints '6'."),
    dict(key=(4, 'b', 'iii'),
         why='Scheme p13 reads both phases off the diagram it draws, shown with the answer, '
             '"4" for the part not split between them.',
         topic='eng-1-3', stem=False,
         question_lift=P(7, *_B4, more=[(176, 531, 590, 563)]),
         lifted=[S(13, 140, 737, 525, 751.5), S(13, 140, 751.5, 505, 766)],
         tariff='questionTotal', total=4,
         question_figure='engineering-2010-HL-paper-q4b-crop',
         figure='engineering-2010-HL-scheme-q4biii-sol',
         notes="The scheme prints '4'."),
    # ---- Question 5 --------------------------------------------------------
    dict(key=(5, 'a', 'i'),
         why='The two processes are drawn at A and B; scheme p14 names each after its '
             'letter, "2 + 2".',
         topic='eng-2-10', stem=False,
         question_lift=P(8, *_A5, more=[(176, 267, 345, 284)]),
         lifted=[S(14, 140, 388, 300, 404), S(14, 140, 404, 300, 417.5)],
         marks=[2, 2], total=4,
         labels={'A': S(14, 163, 388, 300, 404), 'B': S(14, 162, 404, 300, 417.5)},
         question_figure='engineering-2010-HL-paper-q5a-crop',
         notes="The scheme prints '2 + 2', for A and B in that order."),
    dict(key=(5, 'a', 'ii'),
         why='Scheme p14 gives an application of each process in a paragraph, "2 + 2".',
         topic='eng-2-10', stem=False,
         question_lift=P(8, *_A5, more=[(176, 287, 385, 305)]),
         lifted=[S(14, 140, 443, 525, 486), S(14, 140, 486, 525, 527)],
         marks=[2, 2], total=4,
         question_figure='engineering-2010-HL-paper-q5a-crop',
         notes="The scheme prints '2 + 2', for MIG (A) and TIG (B) in that order."),
    dict(key=(5, 'a', 'iii'),
         replaces=NEW + 'cut the MIG answer in two and took its second half for a third '
                        'option',
         why='"Any one of these welding processes": scheme pp14-15 describe each beside a '
             'drawing of it, shown with the answer, "(Any one) 8".',
         topic='eng-2-10', stem=False,
         question_lift=P(8, *_A5, more=[(176, 308, 455, 339)]),
         lifted=[[S(14, 140, 553, 412, 694),
                  join(S(15, 140, 70, 525, 86), S(15, 258, 86, 525, 169))]],
         row_kind='anyN', group=(1, 8), marks=[8], tariff='fixed', total=8,
         question_figure='engineering-2010-HL-paper-q5a-crop',
         figure='engineering-2010-HL-scheme-q5aiii-sol',
         notes="The scheme prints '(Any one) 8'."),
    dict(key=(5, 'b', 'i'),
         checked=_ck(8, '(b)(i)', 'Answer any three of the following:'),
         why='One of "Answer any three of the following": scheme p15 bullets seven features, '
             'the 6 for the part not split between them.',
         topic='eng-3-1',
         lifted=[S(15, 175, 278, 525, 308), S(15, 175, 308, 525, 322.5),
                 S(15, 175, 322.5, 525, 337), S(15, 175, 337, 525, 352),
                 S(15, 175, 352, 525, 366.5), S(15, 175, 366.5, 525, 381),
                 S(15, 175, 381, 525, 396)],
         tariff='questionTotal', total=6, notes=_A5B),
    dict(key=(5, 'b', 'ii'),
         checked=_ck(8, '(b)(ii)', 'Answer any three of the following:'),
         why='One of "Answer any three of the following": scheme p15 bullets four functions, '
             'the 6 for the part not split between them.',
         topic='eng-2-10',
         lifted=[S(15, 175, 436, 525, 452), S(15, 175, 452, 525, 466.5),
                 S(15, 175, 466.5, 525, 481), S(15, 175, 481, 525, 496)],
         tariff='questionTotal', total=6, notes=_A5B),
    dict(key=(5, 'b', 'iii'),
         checked=_ck(8, '(b)(iii)', 'Answer any three of the following:'),
         why='One of "Answer any three of the following": scheme p15 answers in one '
             'sentence.',
         topic='eng-2-10',
         lifted=[S(15, 140, 521, 525, 551)], marks=[6], total=6, notes=_A5B),
    dict(key=(5, 'b', 'iv'),
         replaces=NEW + 'cut the answer in two and read the scheme\'s "(Any three) 6 + 6 + 6" '
                        'as a third point',
         why='One of "Answer any three of the following": scheme p15 answers in one '
             'paragraph under its heading.',
         topic='eng-2-10',
         lifted=[S(15, 140, 604, 525, 731)], marks=[6], total=6, notes=_A5B),
    dict(key=(5, 'c', None),
         why='Paper p8 sets two alternative (c)s either side of an OR. This card is the '
             'first: "the main features of one of the following", electro-slag or '
             'oxyacetylene welding; scheme p16 describes each beside a labelled drawing, '
             'shown with the answer, "(Any one) 16". The drawings\' labels are left out of '
             'the words.',
         topic='eng-2-10', stem=False,
         question_lift=P(8, 150, 545, 500, 576, items=[(150, 579, 290, 597),
                                                       (150, 600, 295, 617)]),
         lifted=[[S(16, 140, 84, 340, 252), S(16, 140, 468, 525, 541)]],
         row_kind='anyN', group=(1, 16), marks=[16], tariff='fixed', total=16,
         figure='engineering-2010-HL-scheme-q5c-sol',
         notes="The scheme prints '(Any one) 16'. " + _OR5),
    dict(key=(5, 'c', 'i'),
         why='The OR branch\'s (i), the robot pictured beside it: scheme p16 answers under '
             'its heading; "6 + 5 + 5", 6 for (i).',
         topic='eng-3-14', stem=False,
         question_lift=P(8, *_C5B, more=[(175, 690, 360, 707)]),
         lifted=[S(16, 140, 620, 525, 650)], marks=[6], total=6,
         question_figure='engineering-2010-HL-paper-q5cor-crop',
         notes="The scheme prints '6 + 5 + 5', for (i), (ii) and (iii) in that order. " + _OR5),
    dict(key=(5, 'c', 'ii'),
         why='The OR branch\'s (ii): scheme p16 answers under its heading; "6 + 5 + 5", 5 '
             'for (ii).',
         topic='eng-3-14', stem=False,
         question_lift=P(8, *_C5B, more=[(175, 710, 300, 728)]),
         lifted=[S(16, 140, 671, 525, 701)], marks=[5], total=5,
         question_figure='engineering-2010-HL-paper-q5cor-crop',
         notes="The scheme prints '6 + 5 + 5', for (i), (ii) and (iii) in that order. " + _OR5),
    dict(key=(5, 'c', 'iii'),
         why='The OR branch\'s (iii): scheme p16 answers under its heading; "6 + 5 + 5", 5 '
             'for (iii).',
         topic='eng-3-14', stem=False,
         question_lift=P(8, *_C5B, more=[(175, 731, 450, 748)]),
         lifted=[S(16, 140, 726, 525, 756)], marks=[5], total=5,
         question_figure='engineering-2010-HL-paper-q5cor-crop',
         notes="The scheme prints '6 + 5 + 5', for (i), (ii) and (iii) in that order. " + _OR5),
    # ---- Question 6 --------------------------------------------------------
    dict(key=(6, 'a', 'i'),
         why='The process is drawn under (a); scheme p17 names it and describes its '
             'operation under their headings, "4" and "8".',
         topic='eng-1-9', stem=False,
         question_lift=P(9, *_A6, more=[(176, 274, 460, 291)]),
         lifted=[S(17, 140, 98, 300, 114), S(17, 140, 139, 525, 197)],
         marks=[4, 8], total=12,
         question_figure='engineering-2010-HL-paper-q6a-crop',
         notes="The scheme prints '4' under the name and '8' under the operation."),
    dict(key=(6, 'a', 'ii'),
         replaces=NEW + 'asked about "this process" without the drawing that shows it',
         why='Scheme p17 lists applications in one line, "(Any one) 4".',
         topic='eng-1-9', stem=False,
         question_lift=P(9, *_A6, more=[(176, 294, 425, 311)]),
         lifted=[S(17, 140, 222, 525, 238)], marks=[4], total=4,
         question_figure='engineering-2010-HL-paper-q6a-crop',
         notes="The scheme prints '(Any one) 4'."),
    dict(key=(6, 'b', None),
         replaces=NEW + 'took the table\'s lines one by one, the two columns mixed',
         why='A lead-in over three headings set as romans; scheme p17 answers in a two-column '
             'table under the same headings, shown with the answer, "16" for the part. Each '
             'row is the table\'s row: its heading, then the thermoplastics cell, then the '
             'thermosetting cell, joined.',
         topic='eng-1-9',
         lifted=[cells(S(17, 150, 296, 250, 312), S(17, 135, 310, 322, 353),
                       S(17, 325, 310, 525, 353)),
                 cells(S(17, 155, 378, 250, 395), S(17, 135, 393, 322, 422),
                       S(17, 325, 393, 525, 422)),
                 cells(S(17, 157, 585, 215, 602), S(17, 150, 600, 322, 717),
                       S(17, 340, 600, 525, 690))],
         tariff='questionTotal', total=16,
         figure='engineering-2010-HL-scheme-q6b-sol',
         notes="The scheme prints '16'. Its table is headed 'Thermoplastics' and "
               "'Thermosetting plastics'; each row gives the heading, then the thermoplastics "
               "cell, then the thermosetting cell."),
    dict(key=(6, 'c', None),
         replaces=NEW + 'read the scheme\'s "(Any three) 6 + 6 + 6" as a sixth point',
         why='A lead-in over five terms set as romans, "any three"; scheme p18 explains each '
             'under its name, one option each, "(Any three) 6 + 6 + 6".',
         topic='eng-1-9',
         lifted=[[S(18, 140, 70, 525, 114), S(18, 140, 126, 525, 197), S(18, 140, 208, 525, 307),
                  S(18, 140, 319, 525, 376), S(18, 140, 388, 525, 459)]],
         row_kind='anyN', group=(3, 6), marks=[18], tariff='fixed', total=18,
         notes="The scheme prints '(Any three) 6 + 6 + 6'."),
    # ---- Question 7 --------------------------------------------------------
    dict(key=(7, 'a', 'i'),
         checked=_ck(10, '(a)(i)', 'Answer any three of the following:'),
         why='One of "Answer any three of the following": scheme p18 lists three materials, '
             'one a line, the 6 for the part not split between them.',
         topic='eng-2-11',
         lifted=[S(18, 140, 581, 300, 596.5), S(18, 140, 596.5, 300, 610.5),
                 S(18, 140, 610.5, 300, 625)],
         tariff='questionTotal', total=6, notes=_A7),
    dict(key=(7, 'a', 'ii'),
         checked=_ck(10, '(a)(ii)', 'Answer any three of the following:'),
         why='One of "Answer any three of the following": scheme p18 describes the process '
             'beside a drawing of it, shown with the answer.',
         topic='eng-2-11',
         lifted=[S(18, 140, 664, 380, 750)], marks=[6], total=6,
         figure='engineering-2010-HL-scheme-q7aii-sol', notes=_A7),
    dict(key=(7, 'a', 'iii'),
         checked=_ck(10, '(a)(iii)', 'Answer any three of the following:'),
         why='One of "Answer any three of the following": scheme p19 describes each kind of '
             'machining in turn, the 6 for the part.',
         topic='eng-2-11',
         lifted=[S(19, 140, 70, 525, 142)], marks=[6], total=6, notes=_A7),
    dict(key=(7, 'a', 'iv'),
         checked=_ck(10, '(a)(iv)', 'Answer any three of the following:'),
         why='One of "Answer any three of the following": scheme p19 bullets three reasons, '
             'the 6 for the part not split between them.',
         topic='eng-2-11',
         lifted=[S(19, 175, 168, 525, 197.5), S(19, 175, 197.5, 525, 253.5),
                 S(19, 175, 253.5, 525, 268)],
         tariff='questionTotal', total=6, notes=_A7),
    dict(key=(7, 'a', 'v'),
         why='One of "Answer any three of the following": scheme p19 describes each fit in '
             'turn, the 6 for the part not split between them.',
         topic='eng-3-12',
         lifted=[S(19, 140, 280, 525, 310), S(19, 140, 321, 525, 351)],
         tariff='questionTotal', total=6, notes=_A7),
    dict(key=(7, 'b', 'i'),
         replaces=NEW + 'asked about the chips at A and B without the drawing that shows them',
         why='The chips are drawn at A, B and C; scheme p19 names A\'s and B\'s after their '
             'letters, "3 + 3".',
         topic='eng-2-11', stem=False,
         question_lift=P(10, *_B7, more=[(176, 402, 460, 433)]),
         lifted=[S(19, 140, 390, 300, 406), S(19, 140, 406, 300, 420)],
         marks=[3, 3], total=6,
         labels={'A': S(19, 163, 390, 300, 406), 'B': S(19, 162, 406, 300, 420)},
         question_figure='engineering-2010-HL-paper-q7b-crop',
         notes="The scheme prints '3 + 3', for A and B in that order."),
    dict(key=(7, 'b', 'ii'),
         replaces=NEW + 'asked about the chips at A and B without the drawing that shows them',
         why='Scheme p19 describes the material for A\'s chip and for B\'s after their '
             'letters, "2 + 2".',
         topic='eng-2-11', stem=False,
         question_lift=P(10, *_B7, more=[(176, 439, 495, 471)]),
         lifted=[S(19, 140, 432, 420, 448), S(19, 140, 448, 420, 461.5)],
         marks=[2, 2], total=4,
         question_figure='engineering-2010-HL-paper-q7b-crop',
         notes="The scheme prints '2 + 2', for A and B in that order."),
    dict(key=(7, 'b', 'iii'),
         why='Scheme p19 bullets five precautions, "2 + 2 + 2".',
         topic='eng-2-11', stem=False,
         question_lift=P(10, *_B7, more=[(176, 478, 510, 511)]),
         lifted=[S(19, 175, 488, 525, 504), S(19, 175, 504, 525, 518.5),
                 S(19, 175, 518.5, 525, 533), S(19, 175, 533, 525, 561.5),
                 S(19, 175, 561.5, 525, 576)],
         tariff='orderedSplit', notation='2 + 2 + 2', ladder=6, total=6,
         question_figure='engineering-2010-HL-paper-q7b-crop',
         notes="The scheme prints '2 + 2 + 2'."),
    dict(key=(7, 'c', None),
         why='Paper p10 sets two alternative (c)s either side of an OR. This card is the '
             'first: "the essential features of one of the following", the magnetic or the '
             'four-jaw chuck; scheme pp19-20 describe each under its name beside a picture, '
             'shown with the answer, "Any one @ 16".',
         topic='eng-2-11', stem=False,
         question_lift=P(10, 150, 551, 470, 584, items=[(150, 588, 262, 605),
                                                        (150, 609, 260, 626)]),
         lifted=[[join(S(19, 140, 629, 392, 672.5), S(19, 140, 672.5, 525, 757),
                       S(20, 140, 70, 525, 142)),
                  join(S(20, 140, 181, 460, 282.5), S(20, 140, 282.5, 525, 448))]],
         row_kind='anyN', group=(1, 16), marks=[16], tariff='fixed', total=16,
         figure='engineering-2010-HL-scheme-q7c-sol',
         notes="The scheme prints 'Any one @ 16'. " + _OR7),
    dict(key=(7, 'c', 'i'),
         replaces=NEW + 'ran the first branch\'s magnetic chuck answer and this branch\'s '
                        'answer into one question total',
         why='The OR branch\'s (i): scheme p20 answers in one sentence, "4".',
         topic='eng-2-11', stem=False,
         question_lift=P(10, 178, 674, 300, 691),
         lifted=[S(20, 140, 543, 525, 572)], marks=[4], total=4,
         notes="The scheme prints '4'. " + _OR7),
    dict(key=(7, 'c', 'ii'),
         replaces=NEW + 'ran the first branch\'s four-jaw chuck answer and this branch\'s '
                        'answer into one ordered split',
         why='The OR branch\'s (ii): scheme p20 answers each heading in turn, "4 + 4 + 4".',
         topic='eng-2-11', stem=False,
         question_lift=P(10, 178, 695, 510, 728, items=[(195, 733, 252, 750),
                                                        (195, 747, 248, 764),
                                                        (195, 762, 226, 779)]),
         lifted=[S(20, 140, 584, 525, 613.5), S(20, 140, 613.5, 525, 627.5),
                 S(20, 140, 627.5, 525, 670)],
         marks=[4, 4, 4], total=12,
         notes="The scheme prints '4 + 4 + 4', for efficiency, accuracy and cost in that "
               "order. " + _OR7),
    # ---- Question 8 --------------------------------------------------------
    dict(key=(8, 'a', None),
         why='"Any one of the mechanisms shown", pictured and captioned (i) and (ii); scheme '
             'p21 names each under its roman and describes it, "(Any one) Name 8, '
             'Application 8". The name and the description are each any one of the two. The '
             'reader joins the caption "(ii)" to the question, so it is lifted from the page.',
         topic='eng-2-15',
         question_lift=P(11, 150, 96, 505, 113),
         lifted=[[S(21, 140, 112, 300, 128), S(21, 140, 153, 300, 169)],
                 [S(21, 140, 126, 525, 142), S(21, 140, 167, 525, 183)]],
         marks=[8, 8], total=16,
         question_figure='engineering-2010-HL-paper-q8a-art',
         notes="The scheme prints '(Any one) Name 8' and 'Application 8', for the mechanism "
               "chosen."),
    dict(key=(8, 'b', None),
         replaces=NEW + 'took "(Any three) 6 + 6 + 6" for an option',
         why='A lead-in over five topics set as romans, "any three"; scheme p21 answers each '
             'under its heading, one option each, "(Any three) 6 + 6 + 6".',
         topic='eng-2-15',
         lifted=[[S(21, 140, 236, 525, 266), S(21, 140, 277, 525, 335), S(21, 140, 346, 525, 404),
                  S(21, 140, 415, 525, 487), S(21, 140, 498, 525, 542)]],
         row_kind='anyN', group=(3, 6), marks=[18], tariff='fixed', total=18,
         notes="The scheme prints '(Any three) 6 + 6 + 6'."),
    dict(key=(8, 'c', None),
         why='Paper p11 sets two alternative (c)s either side of an OR. This card is the '
             'first, the dental chair pictured beside it: scheme pp21-22 answer in '
             'paragraphs after a labelled drawing, shown with the answer; "16". The '
             'bullets\' glyphs are left out of the words.',
         topic='eng-2-15', stem=False,
         question_lift=P(11, 150, 453, 480, 498),
         lifted=[join(S(22, 104, 70, 525, 155.5), S(22, 140, 155.5, 525, 184.5),
                      S(22, 104, 184.5, 525, 199))], marks=[16], total=16,
         question_figure='engineering-2010-HL-paper-q8c-crop',
         figure='engineering-2010-HL-scheme-q8c-sol',
         notes="The scheme prints '16' and '"
               + join(S(21, 104, 581, 525, 597), S(21, 104, 609, 525, 625)) + "' " + _OR8),
    dict(key=(8, 'c', 'i'),
         replaces=NEW + 'ran the four answers into one row and read "2 + 2 + 2 + 2" as a '
                        'second',
         why='The OR branch\'s (i), the circuit drawn with A-D: scheme p22 names each after '
             'its letter, "2 + 2 + 2 + 2".',
         topic='eng-2-16', stem=False,
         question_lift=P(11, *_C8B, more=[(178, 574, 430, 591)]),
         lifted=[S(22, 140, 251, 300, 267), S(22, 140, 267, 300, 281), S(22, 140, 281, 300, 295),
                 S(22, 140, 295, 300, 309)],
         marks=[2, 2, 2, 2], total=8,
         labels={'A': S(22, 163, 251, 300, 267), 'B': S(22, 162, 267, 300, 281),
                 'C': S(22, 163, 281, 300, 295), 'D': S(22, 163, 295, 300, 309)},
         question_figure='engineering-2010-HL-paper-q8cor-crop',
         notes="The scheme prints '2 + 2 + 2 + 2', for A, B, C and D in that order. " + _OR8),
    dict(key=(8, 'c', 'ii'),
         why='The OR branch\'s (ii): scheme p22 gives the two functions one a line, "4 + 4".',
         topic='eng-2-16', stem=False,
         question_lift=P(11, *_C8B, more=[(178, 594, 450, 612)]),
         lifted=[S(22, 140, 348, 525, 363.5), S(22, 140, 363.5, 525, 378)],
         marks=[4, 4], total=8,
         question_figure='engineering-2010-HL-paper-q8cor-crop',
         notes="The scheme prints '4 + 4'. " + _OR8),
]

TOPICS = {}

_ROB = ('Robotic control (the OR branch of Q5(c)), which the reference files under Energy, '
        'Electronics & Robotics; the card\'s syllabus heading is Technology and society.')

ATLAS = {
    'eng-2010-hl-q1-j': dict(
        topics=['Machining & Metrology'],
        note='Locking nuts against vibration, a fastening the reference files with Section A\'s '
             'Machining & Metrology parts; the card\'s syllabus heading is Welding and joining.'),
    'eng-2010-hl-q5-c-i': dict(topics=['Energy, Electronics & Robotics'], note=_ROB),
    'eng-2010-hl-q5-c-ii': dict(topics=['Energy, Electronics & Robotics'], note=_ROB),
    'eng-2010-hl-q5-c-iii': dict(topics=['Energy, Electronics & Robotics'], note=_ROB),
}
