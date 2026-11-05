"""2013 Higher Level: the parts eng_all refuses or gets wrong, from the page.

Paper and scheme as the PDFs number their pages. The marks grid is on scheme
p4: Question 1 is Section A, "Any ten @ 5 marks each", and Section B, "Answer
all of the following", (n) to (r); Questions 2-8 are 50 marks each. The scheme
prints a part's marks under its answer ("(Any two) 3 + 2", "(Any three) 6 + 6 +
6"). This sitting had no cards before the lane: every card here is new, and a
`replaces=` names the automatic card it rebuilds before it ever shipped.
"""
from eng_lift import join, lift

Y, L = 2013, 'hl'
NEW = 'never shipped: the automatic card '


def S(page, *rect):
    return lift(Y, L, 'scheme', page, rect)


def P(page, *rect, more=(), items=()):
    return lift(Y, L, 'paper', page, rect, more=more, items=items)


# Paper stems the parts are lifted with.
_O1 = (125, 163, 315, 182)            # p4: Q1(o), "A simplified Stirling engine is shown."
_B2 = (125, 422, 440, 455)            # p5: Q2(b), "Using the graph paper supplied, plot ..."
_B3 = (125, 319, 470, 338)            # p6: Q3(b), the iron-carbon diagram
_B4 = (125, 257, 500, 292)            # p7: Q4(b), the table
_C5B = (125, 634, 510, 669)           # p8: the robotic welding (c)
_C6 = (125, 579, 450, 598)            # p9: Q6(c), the structures X and Y
_C6W = (130, 696, 415, 716)           # "With reference to the two polymer structures at X and Y:"

_SA = "Section A is 'Any ten @ 5 marks each'."
_SB = 'Section B is "Answer all of the following".'
_OR5 = ('The paper sets two (c)s either side of an OR: the MIG and electro-slag (c), "(Any '
        'one) 16", carded at the letter, and the robotic welding (c), whose (i) and (ii) are '
        'carded apart.')
_OR7 = ('The paper sets two (c)s either side of an OR: gang and straddle milling, "16", '
        'carded at the letter, and the CNC (c), whose (i) and (ii) are carded apart.')
_OR8 = ('The paper sets two (c)s either side of an OR: the computer-controlled machine\'s '
        'drives, "16", carded at the letter, and the IC circuit (c), whose (i) and (ii) are '
        'carded apart.')
_A7 = "The scheme prints '(Any three) 6 + 6 + 6': each part answered earns 6."
_XY = ('The scheme answers under A and B; the paper prints the two structures as X and Y, '
       'the linear one first.')

CROPS = {
    # ---- paper ------------------------------------------------------------
    'engineering-2013-HL-paper-q1f-crop': dict(
        doc='paper', page=3, rect=(506, 357, 559, 490), image=True, ref='2013 HL Q1(f)'),
    # The guitar and its tuning mechanism, with A and its arrow.
    'engineering-2013-HL-paper-q1m-crop': dict(
        doc='paper', page=3, rect=(150, 698, 475, 786), ref='2013 HL Q1(m)', letters=('A',)),
    # The Stirling engine with its zones A, B and C.
    'engineering-2013-HL-paper-q1o-crop': dict(
        doc='paper', page=4, rect=(128, 232, 470, 415), ref='2013 HL Q1(o)',
        letters=('A', 'B', 'C')),
    'engineering-2013-HL-paper-q1q-crop': dict(
        doc='paper', page=4, rect=(380, 526, 540, 649), image=True, ref='2013 HL Q1(q)'),
    # The tensile results, as the table prints them.
    'engineering-2013-HL-paper-q2b-crop': dict(
        doc='paper', page=5, rect=(105, 336, 545, 396), ref='2013 HL Q2(b)'),
    'engineering-2013-HL-paper-q2cii-crop': dict(
        doc='paper', page=5, rect=(159, 608, 454, 763), image=True, ref='2013 HL Q2(c)(ii)'),
    # Q3(a)'s two screwdrivers and their heat treatments, read by both romans.
    'engineering-2013-HL-paper-q3a-art': dict(
        doc='paper', page=6, rect=(125, 100, 526, 206), ref='2013 HL Q3(a)'),
    'engineering-2013-HL-paper-q3b-crop': dict(
        doc='paper', page=6, rect=(150, 355, 470, 525), ref='2013 HL Q3(b)',
        letters=('A', 'B', 'C', 'D', 'X')),
    'engineering-2013-HL-paper-q4b-crop': dict(
        doc='paper', page=7, rect=(140, 308, 485, 392), ref='2013 HL Q4(b)'),
    # The seam welder, read by all three romans of (b).
    'engineering-2013-HL-paper-q5b-art': dict(
        doc='paper', page=8, rect=(389, 314, 529, 465), image=True, ref='2013 HL Q5(b)'),
    'engineering-2013-HL-paper-q5ci-crop': dict(
        doc='paper', page=8, rect=(370, 673, 534, 784), image=True, ref='2013 HL Q5(c)'),
    # The two processes A and B with their labels, read by all three romans.
    'engineering-2013-HL-paper-q6a-art': dict(
        doc='paper', page=9, rect=(45, 120, 555, 270), ref='2013 HL Q6(a)',
        letters=('A', 'B')),
    'engineering-2013-HL-paper-q6c-crop': dict(
        doc='paper', page=9, rect=(100, 600, 482, 682), ref='2013 HL Q6(c)',
        letters=('X', 'Y')),
    'engineering-2013-HL-paper-q7b-crop': dict(
        doc='paper', page=10, rect=(60, 340, 555, 492), ref='2013 HL Q7(b)',
        letters=('A', 'B')),
    'engineering-2013-HL-paper-q8c-crop': dict(
        doc='paper', page=11, rect=(349, 376, 540, 540), image=True, ref='2013 HL Q8(c)'),
    # The OR branch's IC circuit with component A.
    'engineering-2013-HL-paper-q8ci-art': dict(
        doc='paper', page=11, rect=(140, 638, 445, 785), ref='2013 HL Q8(c)(i)',
        letters=('A',)),
    # ---- scheme: the drawings the answers are given with -------------------
    'engineering-2013-HL-scheme-q1k-sol': dict(
        doc='scheme', page=6, rect=(330, 322, 578, 412), solution=True, ref='2013 HL Q1(k)'),
    # Q1(p)'s efficiency formula, a stacked fraction the text layer flattens.
    'engineering-2013-HL-scheme-q1p-sol': dict(
        doc='scheme', page=7, rect=(100, 265.5, 430, 296), solution=True, ref='2013 HL Q1(p)'),
    'engineering-2013-HL-scheme-q2b-sol': dict(
        doc='scheme', page=9, rect=(100, 355, 500, 600), solution=True, ref='2013 HL Q2(b)'),
    'engineering-2013-HL-scheme-q2bi-sol': dict(
        doc='scheme', page=9, rect=(100, 618, 470, 668), solution=True,
        ref='2013 HL Q2(b)(i)'),
    'engineering-2013-HL-scheme-q2bii-sol': dict(
        doc='scheme', page=9, rect=(100, 677, 500, 764), solution=True,
        ref='2013 HL Q2(b)(ii)'),
    'engineering-2013-HL-scheme-q3ciii-sol': dict(
        doc='scheme', page=11, rect=(130, 436, 465, 543), solution=True,
        ref='2013 HL Q3(c)(iii)'),
    'engineering-2013-HL-scheme-q4b-sol': dict(
        doc='scheme', page=12, rect=(125, 520, 512, 766), solution=True, ref='2013 HL Q4(b)'),
    'engineering-2013-HL-scheme-q5c-sol': dict(
        doc='scheme', parts=[(15, (420, 96, 545, 254)), (15, (360, 344, 565, 504))],
        layout='row', solution=True, ref='2013 HL Q5(c)'),
    'engineering-2013-HL-scheme-q7bi-sol': dict(
        doc='scheme', page=18, rect=(355, 370, 590, 545), solution=True,
        ref='2013 HL Q7(b)(i)'),
    'engineering-2013-HL-scheme-q7c-sol': dict(
        doc='scheme', parts=[(19, (310, 88, 540, 192)), (19, (315, 255, 540, 368))],
        solution=True, ref='2013 HL Q7(c)'),
    'engineering-2013-HL-scheme-q8c-sol': dict(
        doc='scheme', page=21, rect=(75, 205, 420, 450), solution=True, ref='2013 HL Q8(c)'),
}

SPLIT = {
    'eng-2013-hl-q7-a': 'never shipped: "Answer any three of the following" over five '
                        'separate questions, each priced at 6; the automatic card ran all '
                        'five answers into one ordered split at the letter',
}

CARDS = [
    dict(key=(2, 'a', 'i'),
         replaces=NEW + 'took (a)(ii)\'s last sentence, "For each of the tests A, B and C, '
                        'identify and describe the metal properties under examination.", for '
                        'its stem',
         why='Scheme p9 explains fatigue and then creep, "4 + 3".',
         topic='eng-3-8', stem=False,
         lifted=[S(9, 140, 111, 525, 155), S(9, 140, 152, 525, 197)],
         marks=[4, 3], total=7,
         notes="The scheme prints '4 + 3', for fatigue and creep in that order."),
    # ---- Question 1, Section A ("Any ten @ 5 marks each") ------------------
    dict(key=(1, 'a', None),
         why='Scheme p5 names three materials on one line, each lifted by its own word '
             'rectangle; "3 + 2".',
         topic='eng-2-11',
         lifted=[S(5, 104, 166, 127, 185), S(5, 127, 166, 163, 185), S(5, 163, 166, 210, 185)],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         notes="The scheme prints '3 + 2'. " + _SA),
    dict(key=(1, 'b', None),
         why='The three signs are pictured and captioned (i)-(iii); scheme p5 names each '
             'after its roman, "(Any two) 3 + 2".',
         topic='eng-3-1',
         question_lift=P(3, 125, 172, 400, 191),
         lifted=[S(5, 105, 221, 225, 238), S(5, 105, 235, 215, 252), S(5, 105, 249, 220, 266)],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         question_figure='engineering-2013-HL-paper-q1b-art',
         notes="The scheme prints '(Any two) 3 + 2'. " + _SA),
    dict(key=(1, 'c', None),
         why='Scheme p5 names three methods on one line, each lifted by its own word '
             'rectangle; "(Any two) 3+2".',
         topic='eng-1-2',
         lifted=[S(5, 105, 304, 210, 323), S(5, 210, 304, 256, 323), S(5, 256, 304, 365, 323)],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         notes="The scheme prints '(Any two) 3+2'. " + _SA),
    dict(key=(1, 'd', None),
         why='Scheme p5 names three factors on one line, each lifted by its own word '
             'rectangle; "(Any two) 3+2".',
         topic='eng-3-7',
         lifted=[S(5, 105, 345, 157, 365), S(5, 157, 345, 205, 365), S(5, 205, 345, 275, 365)],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         notes="The scheme prints '(Any two) 3+2'. " + _SA),
    dict(key=(1, 'e', None),
         why='Scheme p5 compares the two in one paragraph, "5".',
         topic='eng-1-9',
         lifted=[S(5, 105, 387, 520, 444)], marks=[5], total=5,
         notes="The scheme prints '5'. " + _SA),
    dict(key=(1, 'f', None),
         why='The heater is photographed beside (f); scheme p5 explains the control in one '
             'paragraph, "5".',
         topic='eng-3-14',
         lifted=[S(5, 105, 469, 520, 514)], marks=[5], total=5,
         question_figure='engineering-2013-HL-paper-q1f-crop',
         notes="The scheme prints '5'. " + _SA),
    dict(key=(1, 'g', None),
         why='Scheme p5 differentiates the two in one paragraph, "5".',
         topic='eng-3-1',
         lifted=[S(5, 105, 538, 520, 596)], marks=[5], total=5,
         notes="The scheme prints '5'. " + _SA),
    dict(key=(1, 'h', None),
         why='A lead-in over three people set as romans, "any one"; scheme p5 writes a note '
             'on each under the name, "5".',
         topic='eng-3-14',
         lifted=[[S(5, 140, 621, 505, 666), S(5, 140, 663, 525, 721),
                  S(5, 140, 718, 510, 763)]],
         row_kind='anyN', group=(1, 5), marks=[5], tariff='fixed', total=5,
         notes="The scheme prints '5'. " + _SA),
    dict(key=(1, 'i', None),
         why='Scheme p6 bullets eight applications under a lead-in; "(Any three) 2 + 2 + 1".',
         topic='eng-2-15',
         lifted=[S(6, 140, 84, 500, 101), S(6, 140, 99, 500, 116), S(6, 140, 113, 500, 130),
                 S(6, 140, 128, 500, 145), S(6, 140, 143, 500, 160), S(6, 140, 157, 500, 174),
                 S(6, 140, 172, 500, 189), S(6, 140, 187, 500, 204)],
         tariff='orderedSplit', notation='2 + 2 + 1', ladder=5, total=5,
         notes="The scheme prints '(Any three) 2 + 2 + 1'. " + _SA),
    dict(key=(1, 'j', None),
         why='Scheme p6 explains anodising in one paragraph under its heading, "5".',
         topic='eng-3-7',
         lifted=[S(6, 105, 228, 505, 300)], marks=[5], total=5,
         notes="The scheme prints '5'. " + _SA),
    dict(key=(1, 'k', None),
         why='Scheme p6 describes the flame beside a labelled drawing of it, shown with the '
             'answer; "5".',
         topic='eng-2-10',
         lifted=[S(6, 105, 325, 300, 411)], marks=[5], total=5,
         figure='engineering-2013-HL-scheme-q1k-sol',
         notes="The scheme prints '5'. " + _SA),
    dict(key=(1, 'l', None),
         why='Scheme p6 expands each abbreviation after its roman; "(Any two) 3 + 2".',
         topic='eng-3-14',
         lifted=[S(6, 105, 435, 390, 452), S(6, 105, 449, 390, 466), S(6, 105, 463, 390, 480),
                 S(6, 105, 476, 390, 494)],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         notes="The scheme prints '(Any two) 3 + 2'. " + _SA),
    dict(key=(1, 'm', None),
         why='The guitar and its tuning mechanism are photographed with A; scheme p6 names '
             'the mechanism, "5".',
         topic='eng-2-15', stem=False,
         lifted=[S(6, 105, 518, 230, 535)], marks=[5], total=5,
         labels={'A': S(6, 105, 518, 230, 535)},
         question_figure='engineering-2013-HL-paper-q1m-crop',
         notes="The scheme prints '5'. " + _SA),
    # ---- Question 1, Section B ("Answer all of the following") -------------
    dict(key=(1, 'n', None),
         why='Scheme p6 lists heat sources on one line, each lifted by its own word '
             'rectangle; "4 + 3 + 3". The reader keeps only (n)\'s first sentence, so the '
             'question is lifted from the page.',
         topic='eng-3-14', stem=False,
         question_lift=P(4, 125, 106, 460, 146),
         lifted=[S(6, 204, 642, 229, 661), S(6, 229, 642, 256, 661), S(6, 256, 642, 282, 661),
                 S(6, 282, 642, 410, 661), S(6, 410, 642, 487, 661)],
         tariff='orderedSplit', notation='4 + 3 + 3', ladder=10, total=10,
         notes="The scheme prints '4 + 3 + 3'. " + _SB),
    dict(key=(1, 'o', 'i'),
         why='The engine is drawn with zones A, B and C; scheme p6 names each zone after its '
             'letter, "1 + 1 + 1".',
         topic='eng-3-14', stem=False,
         question_lift=P(4, *_O1, more=[(150, 184, 310, 203)]),
         lifted=[S(6, 140, 683, 230, 700), S(6, 140, 697, 230, 714), S(6, 140, 711, 230, 728)],
         marks=[1, 1, 1], total=3,
         labels={'A': S(6, 163, 683, 230, 700), 'B': S(6, 160, 697, 230, 714),
                 'C': S(6, 162, 711, 230, 728)},
         question_figure='engineering-2013-HL-paper-q1o-crop',
         notes="The scheme prints '1 + 1 + 1'. " + _SB),
    dict(key=(1, 'o', 'ii'),
         why='Scheme p7 describes the alpha Stirling engine\'s operation in two paragraphs '
             'under "Principle of operation:", "7".',
         topic='eng-3-14', stem=False,
         question_lift=P(4, *_O1, more=[(150, 205, 400, 224)]),
         lifted=[S(7, 140, 83, 520, 141), S(7, 140, 138, 520, 225)],
         tariff='questionTotal', total=7,
         question_figure='engineering-2013-HL-paper-q1o-crop',
         notes="The scheme prints '7'. " + _SB),
    dict(key=(1, 'p', None),
         why='Scheme pp7-8 answer under the two headings the question gives, "5 + 5": engine '
             'efficiency, with the advantages and disadvantages set under it, and the range '
             'of applications, with its own. The efficiency formula is a stacked fraction '
             'the text layer flattens, so it is shown as printed and the row is lifted around '
             'it.',
         topic='eng-3-14', stem=False,
         lifted=[join(S(7, 105, 249, 205, 265), S(7, 105, 290, 515, 333),
                      S(7, 105, 344, 500, 546)),
                 join(S(7, 105, 557, 500, 761),
                      lift(Y, L, 'scheme', 8, (105, 70, 525, 226), bullet=False))],
         marks=[5, 5], total=10,
         figure='engineering-2013-HL-scheme-q1p-sol',
         notes="The scheme prints '5 + 5', for engine efficiency and the range of "
               "applications in that order. " + _SB),
    dict(key=(1, 'q', None),
         why='The engine on a circuit board is photographed beside (q); scheme p8 explains its '
             'function in one paragraph, "10". The reader keeps only (q)\'s first sentence, so '
             'the question is lifted from the page.',
         topic='eng-3-14', stem=False,
         question_lift=P(4, 125, 550, 370, 625),
         lifted=[S(8, 105, 275, 520, 320)], marks=[10], total=10,
         question_figure='engineering-2013-HL-paper-q1q-crop',
         notes="The scheme prints '10'. " + _SB),
    dict(key=(1, 'r', None),
         why='A lead-in over three topics set as romans, "any two"; scheme p8 answers each '
             'under its roman, "(Any two) 5 + 5". The labels of the drawing beside (i) are '
             'left out of its answer.',
         topic='eng-3-14',
         lifted=[[S(8, 140, 400, 450, 555), S(8, 140, 565, 505, 662),
                  S(8, 140, 672, 525, 729)]],
         row_kind='anyN', group=(2, 5), marks=[10], tariff='fixed', total=10,
         notes="The scheme prints '(Any two) 5 + 5'. " + _SB),
    # ---- Question 2 --------------------------------------------------------
    dict(key=(2, 'a', 'ii'),
         replaces=NEW + 'read the scheme\'s "3 + 3 + 3" as a fourth point and split the '
                        'question in two, its last sentence before its first',
         why='Scheme p9 describes each test under its letter and name, "3 + 3 + 3". The '
             'question is lifted with the three tests on their lines, as printed.',
         topic='eng-3-8', stem=False,
         question_lift=P(5, 150, 135, 460, 168, items=[(150, 166, 240, 184),
                                                       (150, 182, 240, 199),
                                                       (150, 198, 240, 215),
                                                       (150, 219, 520, 252)]),
         lifted=[S(9, 140, 221, 500, 266), S(9, 140, 263, 430, 294), S(9, 140, 290, 475, 321)],
         marks=[3, 3, 3], total=9,
         notes="The scheme prints '3 + 3 + 3', for the tests A, B and C in that order."),
    dict(key=(2, 'b', None),
         why='"Plot the load-extension diagram": scheme p9 answers with the plotted graph, '
             'shown with the answer, "Draw graph", "10" (the grid\'s "Graph 10"). The plot is '
             'asked at the letter, so the card is the letter\'s.',
         topic='eng-3-8', stem=False,
         question_lift=P(5, 125, 292, 520, 327, more=[(125, 422, 440, 439)]),
         special={'kind': 'ask'}, total=10,
         question_figure='engineering-2013-HL-paper-q2b-crop',
         figure='engineering-2013-HL-scheme-q2b-sol',
         notes="The scheme prints 'Draw graph' and '10'."),
    dict(key=(2, 'b', 'i'),
         why='Scheme p9 works the UTS as a stacked fraction the text layer flattens; the '
             'working is shown as printed, "4".',
         topic='eng-3-8', stem=False,
         question_lift=P(5, *_B2, more=[(150, 454, 330, 471)]),
         special={'kind': 'ask'}, total=4,
         question_figure='engineering-2013-HL-paper-q2b-crop',
         figure='engineering-2013-HL-scheme-q2bi-sol',
         notes="The scheme prints '4'."),
    dict(key=(2, 'b', 'ii'),
         why='Scheme p9 works the proof stress in three lines, the last a stacked fraction '
             'the text layer flattens; the working is shown as printed, "4".',
         topic='eng-3-8', stem=False,
         question_lift=P(5, *_B2, more=[(150, 474, 265, 492)]),
         special={'kind': 'ask'}, total=4,
         question_figure='engineering-2013-HL-paper-q2b-crop',
         figure='engineering-2013-HL-scheme-q2bii-sol',
         notes="The scheme prints '4'."),
    dict(key=(2, 'c', 'i'),
         replaces=NEW + 'read the scheme\'s "2 + 2 + 2" as a fourth point',
         why='Scheme p10 bullets three advantages under a lead-in, "2 + 2 + 2".',
         topic='eng-3-8',
         lifted=[S(10, 190, 98, 515, 115), S(10, 190, 112, 515, 130), S(10, 190, 127, 515, 144)],
         marks=[2, 2, 2], total=6,
         notes="The scheme prints '2 + 2 + 2'."),
    dict(key=(2, 'c', 'ii'),
         why='The test is drawn under (c)(ii); scheme p10 names it and then describes it, '
             '"(Name and Describe) 2 + 8".',
         topic='eng-3-8',
         lifted=[S(10, 140, 182, 255, 199), S(10, 140, 196, 435, 310)],
         marks=[2, 8], total=10,
         question_figure='engineering-2013-HL-paper-q2cii-crop',
         notes="The scheme prints '(Name and Describe) 2 + 8'."),
    # ---- Question 3 --------------------------------------------------------
    dict(key=(3, 'b', 'i'),
         why='The diagram is drawn with regions A-D and point X; scheme p10 names each after '
             'its letter, "2 + 2 + 2 + 2 + 2".',
         topic='eng-1-3', stem=False,
         question_lift=P(6, *_B3, more=[(150, 537, 410, 556)]),
         lifted=[S(10, 140, 628, 300, 645), S(10, 140, 642, 300, 659), S(10, 140, 656, 300, 673),
                 S(10, 140, 670, 300, 687), S(10, 140, 684, 300, 701)],
         marks=[2, 2, 2, 2, 2], total=10,
         labels={'A': S(10, 163, 628, 300, 645), 'B': S(10, 162, 642, 300, 659),
                 'C': S(10, 163, 656, 300, 673), 'D': S(10, 163, 670, 300, 687),
                 'X': S(10, 163, 684, 300, 701)},
         question_figure='engineering-2013-HL-paper-q3b-crop',
         notes="The scheme prints '2 + 2 + 2 + 2 + 2'."),
    dict(key=(3, 'b', 'ii'),
         replaces=NEW + 'carried the part\'s "8" in its one row',
         why='Scheme p10 answers each heading on its own line, "8" for the part. The '
             'question is lifted with its headings on their lines, as printed.',
         topic='eng-1-3', stem=False,
         question_lift=P(6, *_B3, more=[(150, 557, 460, 575)],
                         items=[(160, 574, 250, 591), (160, 591, 250, 608),
                                (160, 608, 250, 625)]),
         lifted=[S(10, 140, 725, 425, 742), S(10, 140, 739, 285, 756), S(10, 140, 752, 245, 768)],
         tariff='questionTotal', total=8,
         question_figure='engineering-2013-HL-paper-q3b-crop',
         labels={'X': S(10, 163, 684, 300, 701)},
         notes="The scheme prints '8'."),
    dict(key=(3, 'c', 'iii'),
         replaces=NEW + 'opened with the diagrams\' letters "A B C"',
         why='Scheme p11 explains the pyrometer under three lettered diagrams, shown with the '
             'answer; "(Any two) 8 + 8", 8 for the part.',
         topic='eng-2-6',
         lifted=[S(11, 140, 538, 525, 555), S(11, 140, 552, 525, 611)],
         tariff='questionTotal', total=8,
         figure='engineering-2013-HL-scheme-q3ciii-sol',
         notes="The scheme prints '(Any two) 8 + 8': each part answered earns 8."),
    dict(key=(3, 'c', 'iv'),
         replaces=NEW + 'read the scheme\'s "(Any two) 8 + 8" as a second point',
         why='Scheme p11 answers in one paragraph; "(Any two) 8 + 8", 8 for the part.',
         topic='eng-1-4',
         lifted=[S(11, 140, 621, 525, 680)], marks=[8], total=8,
         notes="The scheme prints '(Any two) 8 + 8': each part answered earns 8."),
    # ---- Question 4 --------------------------------------------------------
    dict(key=(4, 'a', None),
         replaces=NEW + 'split the answers into ten options, one of them the scheme\'s '
                        '"(Any two) 8 + 8"',
         why='A lead-in over four topics set as romans, "any two"; scheme p12 answers each '
             'under its roman, one option each, "(Any two) 8 + 8".',
         topic='eng-1-3',
         lifted=[[S(12, 140, 97, 500, 183), S(12, 140, 189, 525, 275),
                  S(12, 140, 281, 475, 381), S(12, 140, 387, 525, 459)]],
         row_kind='anyN', group=(2, 8), marks=[16], tariff='fixed', total=16,
         notes="The scheme prints '(Any two) 8 + 8'."),
    dict(key=(4, 'b', 'i'),
         why='"Draw the thermal equilibrium diagram": scheme p12 answers with the drawn '
             'diagram, shown with the answer, "8".',
         topic='eng-1-3', stem=False,
         question_lift=P(7, *_B4, more=[(150, 405, 500, 440)]),
         special={'kind': 'ask'}, total=8,
         question_figure='engineering-2013-HL-paper-q4b-crop',
         figure='engineering-2013-HL-scheme-q4b-sol',
         notes="The scheme prints '8'."),
    dict(key=(4, 'b', 'ii'),
         why='Scheme p13 describes five features, one a line, which the diagram on p12 '
             'labels, shown with the answer; "(Any three) 3 + 3" for the part, not split '
             'between them.',
         topic='eng-1-3', stem=False,
         question_lift=P(7, *_B4, more=[(150, 442, 410, 461)]),
         lifted=[S(13, 140, 84, 470, 99), S(13, 140, 98, 490, 127), S(13, 140, 126, 495, 155),
                 S(13, 140, 154, 380, 168), S(13, 140, 167, 290, 183)],
         tariff='questionTotal', total=6,
         question_figure='engineering-2013-HL-paper-q4b-crop',
         figure='engineering-2013-HL-scheme-q4b-sol',
         notes="The scheme prints '(Any three) 3 + 3'."),
    dict(key=(4, 'b', 'iii'),
         replaces=NEW + 'carried the part\'s "4" in its one row',
         why='Scheme p13 reads the two phases off the diagram, X and Y marked on it at 450 '
             '˚C, shown with the answer; "4" for the part.',
         topic='eng-1-3', stem=False,
         question_lift=P(7, *_B4, more=[(150, 462, 505, 496)]),
         lifted=[S(13, 140, 231, 340, 248), S(13, 140, 245, 330, 262)],
         tariff='questionTotal', total=4,
         question_figure='engineering-2013-HL-paper-q4b-crop',
         figure='engineering-2013-HL-scheme-q4b-sol',
         notes="The scheme prints '4'."),
    # ---- Question 5 --------------------------------------------------------
    dict(key=(5, 'a', 'ii'),
         replaces=NEW + 'left the transformer\'s answer without its heading, "Transformer", '
                        'which the other two answers carry',
         why='Scheme p14 explains the transformer, the rectifier and the capacitor, each under '
             'its heading; "(Any three) 6 + 6 + 6", 6 for the part.',
         topic='eng-2-10',
         lifted=[S(14, 140, 98, 525, 184), S(14, 140, 181, 500, 239), S(14, 140, 236, 505, 267)],
         tariff='questionTotal', total=6,
         notes="The scheme prints '(Any three) 6 + 6 + 6': each part answered earns 6."),
    dict(key=(5, 'a', 'iv'),
         replaces=NEW + 'left out the TIG answer and read "(Any three) 6 + 6 + 6" into the '
                        'oxy-acetylene answer',
         why='Scheme p14 gives a use for each process after its name, one a line; "(Any '
             'three) 6 + 6 + 6", 6 for the part.',
         topic='eng-2-10',
         lifted=[S(14, 140, 404, 515, 421), S(14, 140, 418, 515, 449), S(14, 140, 445, 480, 462)],
         tariff='questionTotal', total=6,
         notes="The scheme prints '(Any three) 6 + 6 + 6': each part answered earns 6."),
    dict(key=(5, 'c', None),
         why='Paper p8 sets two alternative (c)s either side of an OR. This card is the '
             'first: "the main features of one of the following", MIG or electro-slag '
             'welding; scheme p15 describes each beside a drawing, shown with the answer, '
             '"(Any one) 16".',
         topic='eng-2-10', stem=False,
         question_lift=P(8, 125, 496, 490, 529, items=[(125, 530, 305, 550),
                                                       (125, 551, 256, 570)]),
         lifted=[[S(15, 140, 111, 410, 252), S(15, 140, 332, 305, 501)]],
         row_kind='anyN', group=(1, 16), marks=[16], tariff='fixed', total=16,
         figure='engineering-2013-HL-scheme-q5c-sol',
         notes="The scheme prints '(Any one) 16'. " + _OR5),
    dict(key=(5, 'c', 'i'),
         replaces=NEW + 'ran the first branch\'s MIG answer and this branch\'s answer into '
                        'one ordered split',
         why='The OR branch\'s (i): scheme p15 lists five types on one line, each lifted by '
             'its own word rectangle; "4 + 4".',
         topic='eng-2-10', stem=False,
         question_lift=P(8, *_C5B, more=[(145, 674, 360, 709)]),
         lifted=[S(15, 140, 594, 216, 613), S(15, 216, 594, 284, 613), S(15, 284, 594, 381, 613),
                 S(15, 381, 594, 410, 613), S(15, 410, 594, 442, 613)],
         tariff='orderedSplit', notation='4 + 4', ladder=8, total=8,
         question_figure='engineering-2013-HL-paper-q5ci-crop',
         notes="The scheme prints '4 + 4'. " + _OR5),
    dict(key=(5, 'c', 'ii'),
         replaces=NEW + 'ran the first branch\'s electro-slag answer and this branch\'s '
                        'answer into two rows',
         why='The OR branch\'s (ii): scheme p15 lists five processes on one line, each lifted '
             'by its own word rectangle; "4 + 4".',
         topic='eng-2-10', stem=False,
         question_lift=P(8, *_C5B, more=[(145, 712, 360, 747)]),
         lifted=[S(15, 140, 631, 189, 650), S(15, 189, 631, 273, 650), S(15, 273, 631, 331, 650),
                 S(15, 331, 631, 412, 650), S(15, 412, 631, 505, 650)],
         tariff='orderedSplit', notation='4 + 4', ladder=8, total=8,
         question_figure='engineering-2013-HL-paper-q5ci-crop',
         notes="The scheme prints '4 + 4'. " + _OR5),
    # ---- Question 6 --------------------------------------------------------
    dict(key=(6, 'a', 'i'),
         replaces=NEW + 'carried no key for the letters A and B the drawing is labelled with',
         why='The two processes are drawn at A and B; scheme p16 names the one selected '
             'after its letter, "6". The other is named at (a)(iii).',
         topic='eng-1-9',
         lifted=[S(16, 140, 97, 260, 114)], marks=[6], total=6,
         labels={'A': S(16, 393, 221, 486, 238), 'B': S(16, 162, 97, 256, 114)},
         question_figure='engineering-2013-HL-paper-q6a-art',
         notes="The scheme prints '6'."),
    dict(key=(6, 'b', None),
         replaces=NEW + 'split the answers into twelve options, one of them the scheme\'s '
                        '"(Any three) 6 + 6 + 6"',
         why='A lead-in over four pairs set as romans, "any three"; scheme pp16-17 answer '
             'each under its roman, one option each, "(Any three) 6 + 6 + 6".',
         topic='eng-1-9',
         lifted=[[S(16, 140, 318, 525, 597), S(16, 140, 607, 525, 680),
                  join(S(16, 140, 690, 525, 749), S(17, 140, 69, 525, 211)),
                  S(17, 140, 221, 525, 307)]],
         row_kind='anyN', group=(3, 6), marks=[18], tariff='fixed', total=18,
         notes="The scheme prints '(Any three) 6 + 6 + 6'."),
    dict(key=(6, 'c', 'i'),
         why='The two structures are drawn at X and Y; scheme p17 names each, "2 + 2".',
         topic='eng-1-9', stem=False,
         question_lift=P(9, *_C6, more=[_C6W, (150, 717, 265, 736)]),
         lifted=[S(17, 140, 332, 300, 349), S(17, 140, 345, 300, 362)],
         marks=[2, 2], total=4,
         labels={'X': S(17, 163, 332, 300, 349), 'Y': S(17, 162, 345, 300, 362)},
         question_figure='engineering-2013-HL-paper-q6c-crop',
         notes="The scheme prints '2 + 2'. " + _XY),
    dict(key=(6, 'c', 'ii'),
         why='Scheme p17 gives a polymer for each structure, "2 + 2".',
         topic='eng-1-9', stem=False,
         question_lift=P(9, *_C6, more=[_C6W, (150, 738, 415, 757)]),
         lifted=[S(17, 140, 373, 375, 390), S(17, 140, 387, 320, 404)],
         marks=[2, 2], total=4,
         labels={'X': S(17, 163, 332, 300, 349), 'Y': S(17, 162, 345, 300, 362)},
         question_figure='engineering-2013-HL-paper-q6c-crop',
         notes="The scheme prints '2 + 2'. " + _XY),
    dict(key=(6, 'c', 'iii'),
         replaces=NEW + 'ran both structures\' properties into one row for "4 + 4"',
         why='Scheme p17 gives each structure\'s properties in a paragraph each, "4 + 4".',
         topic='eng-1-9', stem=False,
         question_lift=P(9, *_C6, more=[_C6W, (150, 758, 410, 778)]),
         lifted=[S(17, 140, 428, 510, 459), S(17, 140, 469, 520, 514)],
         marks=[4, 4], total=8,
         labels={'X': S(17, 163, 332, 300, 349), 'Y': S(17, 162, 345, 300, 362)},
         question_figure='engineering-2013-HL-paper-q6c-crop',
         notes="The scheme prints '4 + 4'. " + _XY),
    # ---- Question 7 --------------------------------------------------------
    dict(key=(7, 'a', 'i'),
         why='One of "Answer any three of the following": scheme p17 bullets four features, '
             'the 6 for the part not split between them.',
         topic='eng-3-1',
         lifted=[S(17, 175, 636, 450, 653), S(17, 175, 651, 450, 668), S(17, 175, 665, 450, 682),
                 S(17, 175, 680, 450, 697)],
         tariff='questionTotal', total=6, notes=_A7),
    dict(key=(7, 'a', 'ii'),
         why='One of "Answer any three of the following": scheme p17 answers in one '
             'paragraph under its heading.',
         topic='eng-3-12',
         lifted=[S(17, 140, 708, 410, 752)], marks=[6], total=6, notes=_A7),
    dict(key=(7, 'a', 'iii'),
         why='One of "Answer any three of the following": scheme p18 bullets three types of '
             'chip, the 6 for the part not split between them.',
         topic='eng-2-11',
         lifted=[S(18, 175, 84, 300, 101), S(18, 175, 99, 300, 116), S(18, 175, 113, 300, 130)],
         tariff='questionTotal', total=6, notes=_A7),
    dict(key=(7, 'a', 'iv'),
         why='One of "Answer any three of the following": scheme p18 bullets five methods, '
             'the 6 for the part not split between them.',
         topic='eng-2-11',
         lifted=[S(18, 178, 169, 250, 187), S(18, 178, 184, 280, 201), S(18, 178, 199, 290, 216),
                 S(18, 178, 213, 230, 230), S(18, 178, 228, 250, 245)],
         tariff='questionTotal', total=6, notes=_A7),
    dict(key=(7, 'a', 'v'),
         why='One of "Answer any three of the following": scheme p18 lists the advantages and '
             'the disadvantages under their headings, the 6 for the part not split.',
         topic='eng-2-11',
         lifted=[S(18, 140, 269, 525, 301), S(18, 140, 297, 525, 328)],
         tariff='questionTotal', total=6, notes=_A7),
    dict(key=(7, 'b', 'i'),
         replaces=NEW + 'took the two pictures\' captions for its stem',
         why='The grinding processes are pictured and captioned at A and B; scheme p18 '
             'describes the machine beside a labelled drawing, shown with the answer; "10".',
         topic='eng-2-11', stem=False,
         lifted=[S(18, 140, 394, 345, 425), S(18, 140, 421, 345, 521)],
         tariff='questionTotal', total=10,
         question_figure='engineering-2013-HL-paper-q7b-crop',
         figure='engineering-2013-HL-scheme-q7bi-sol',
         notes="The scheme prints '10'."),
    dict(key=(7, 'b', 'ii'),
         replaces=NEW + 'took the two pictures\' captions for its stem and read the scheme\'s '
                        '"2 + 2 + 2" as a fifth point',
         why='Scheme p18 bullets four hazards, "2 + 2 + 2".',
         topic='eng-2-11', stem=False,
         lifted=[S(18, 175, 588, 525, 619), S(18, 175, 616, 525, 647), S(18, 175, 645, 525, 676),
                 S(18, 175, 673, 525, 704)],
         tariff='orderedSplit', notation='2 + 2 + 2', ladder=6, total=6,
         question_figure='engineering-2013-HL-paper-q7b-crop',
         notes="The scheme prints '2 + 2 + 2'."),
    dict(key=(7, 'c', None),
         why='Paper p10 sets two alternative (c)s either side of an OR. This card is the '
             'first: scheme p19 describes gang and straddle milling under their headings, '
             'each beside a drawing, shown with the answer; "16" for the part.',
         topic='eng-2-11', stem=False,
         question_lift=P(10, 125, 600, 465, 633),
         lifted=[S(19, 105, 97, 305, 197), S(19, 105, 263, 300, 335)],
         tariff='questionTotal', total=16,
         figure='engineering-2013-HL-scheme-q7c-sol',
         notes="The scheme prints '16'. " + _OR7),
    # ---- Question 8 --------------------------------------------------------
    dict(key=(8, 'a', None),
         replaces=NEW + 'left out both names and took "(Any one) Name 8" for an answer, and '
                        'priced the part as one 16',
         why='"Any one of the mechanisms shown", photographed and captioned (i) and (ii); '
             'scheme p20 names each under its roman and describes its operation, "(Any one) '
             'Name 8, Operation 8". The name and the operation are each any one of the two.',
         topic='eng-2-15',
         lifted=[[S(20, 140, 111, 230, 128), S(20, 140, 180, 280, 197)],
                 [S(20, 140, 125, 525, 169), S(20, 140, 194, 525, 280)]],
         marks=[8, 8], total=16,
         question_figure='engineering-2013-HL-paper-q8a-art',
         notes="The scheme prints '(Any one) Name 8, Operation 8', for the mechanism "
               "chosen."),
    dict(key=(8, 'b', None),
         replaces=NEW + 'split the answers into eight options, one of them the scheme\'s '
                        '"(Any three) 6 + 6 + 6"',
         why='A lead-in over five topics set as romans, "any three"; scheme p20 answers each '
             'under its roman, one option each, "(Any three) 6 + 6 + 6".',
         topic='eng-2-15',
         lifted=[[S(20, 140, 318, 525, 376), S(20, 140, 387, 525, 459),
                  S(20, 140, 470, 525, 501), S(20, 140, 511, 365, 556),
                  S(20, 140, 566, 525, 611)]],
         row_kind='anyN', group=(3, 6), marks=[18], tariff='fixed', total=18,
         notes="The scheme prints '(Any three) 6 + 6 + 6'."),
    dict(key=(8, 'c', None),
         why='Paper p11 sets two alternative (c)s either side of an OR. This card is the '
             'first, the computer-controlled machine photographed beside it: scheme p21 '
             'suggests a rack and pinion drive, "Suggested solution - other viable solutions '
             'are acceptable.", described in one paragraph over a drawing, shown with the '
             'answer; "16".',
         topic='eng-2-15', stem=False,
         question_lift=P(11, 125, 426, 340, 507),
         lifted=[S(21, 110, 125, 505, 198)], marks=[16], total=16,
         question_figure='engineering-2013-HL-paper-q8c-crop',
         figure='engineering-2013-HL-scheme-q8c-sol',
         notes="The scheme prints '16' and 'Suggested solution - other viable solutions are "
               "acceptable.' " + _OR8),
    dict(key=(8, 'c', 'ii'),
         replaces=NEW + 'read the scheme\'s "(Name and Describe) 4 + 4" as a third point',
         why='The OR branch\'s circuit is drawn with A; scheme p21 names the relay and gives '
             'its function in two sentences, "(Name and Describe) 4 + 4".',
         topic='eng-2-16',
         lifted=[S(21, 140, 525, 460, 542), S(21, 140, 538, 460, 556)],
         marks=[4, 4], total=8,
         labels={'A': S(21, 164, 525, 195, 542)},
         question_figure='engineering-2013-HL-paper-q8ci-art',
         notes="The scheme prints '(Name and Describe) 4 + 4'. " + _OR8),
]

TOPICS = {
    'eng-2013-hl-q6-a-iii': ('eng-1-9', 'the split mould of the injection moulding process A, '
                                        'a plastics process; "mould" filed it under '
                                        'manufacturing processes'),
    'eng-2013-hl-q7-c-ii': ('eng-2-11', 'stepper motors in CNC machines, machining; the '
                                        'question\'s wording filed it under manufacturing '
                                        'processes'),
}

ATLAS = {
    'eng-2013-hl-q3-c-iv': dict(
        topics=['Heat Treatment'],
        note='The properties and use of 18/10 stainless steel, under Q3, which the reference '
             'files under Heat Treatment; the card\'s syllabus heading is Iron and steel.'),
}
