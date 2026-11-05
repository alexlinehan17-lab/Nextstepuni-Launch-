"""2014 Higher Level: the parts eng_all refuses or gets wrong, from the page.

Paper and scheme as the PDFs number their pages. The marks grid is on scheme
p4: Question 1 is Section A, "Any ten @ 5 marks each", and Section B, "Answer
all of the following", (n) to (r); Questions 2-8 are 50 marks each. The scheme
prints a part's marks under its answer ("(Any two) 3 + 2", "(Any three) 6 + 6 +
6"). This sitting had no cards before the lane: every card here is new, and a
`replaces=` names the automatic card it rebuilds before it ever shipped.
"""
from eng_lift import join, lift

Y, L = 2014, 'hl'
NEW = 'never shipped: the automatic card '


def S(page, *rect):
    return lift(Y, L, 'scheme', page, rect)


def P(page, *rect, more=(), items=()):
    return lift(Y, L, 'paper', page, rect, more=more, items=items)


# Paper stems the romans are lifted with.
_O1 = (82, 255, 360, 275)             # p4: Q1(o), the nuclear power plant
_A2 = (82, 95, 365, 208)              # p5: Q2(a), the crash barrier and the three metals
_B2 = (82, 396, 480, 416)             # p5: Q2(b), the results
_GRAPH2 = (82, 506, 525, 525)         # "Using the graph paper supplied, plot ..."
_B3 = (82, 256, 425, 276)             # p6: Q3(b), the iron-carbon diagram
_B4 = (82, 275, 560, 295)             # p7: Q4(b), the table
_A5 = (82, 90, 560, 109)              # p8: Q5(a)'s lead-in
_C5A = (82, 575, 240, 595)            # p8: Q5(c), "Describe each of the following:"
_ORW5 = (276, 678, 302, 697)
_A6 = (82, 90, 560, 125)              # p9: Q6(a), the games controller
_C6 = (82, 594, 560, 630)             # p9: Q6(c), the kettle
_C7B = (82, 672, 410, 691)            # p10: the CNC (c)
_C8B = (82, 558, 325, 577)            # p11: the timer circuit (c)

_OR5 = ('The paper sets two (c)s either side of an OR, the flames and joint protection, '
        'and robotic welding; the scheme prices each (i) at 8 and each (ii) at 8, so each '
        'roman is one card, each branch a route.')
_OR7 = ('The paper sets two (c)s either side of an OR: "Answer part (i) or part (ii)" on '
        'cutting tools, "Any one @ 16", carded at the letter, and the CNC (c), whose (i)-(iii) '
        'are carded apart.')
_OR8 = ('The paper sets two (c)s either side of an OR: the gull-wing doors, answered at the '
        'letter for 16, and the timer circuit (c), whose (i) and (ii) are carded apart.')

CROPS = {
    # ---- paper ------------------------------------------------------------
    'engineering-2014-HL-paper-q1i-crop': dict(
        doc='paper', page=3, rect=(396, 487, 550, 572), image=True, ref='2014 HL Q1(i)'),
    # The steering column with its nylon inserts labelled; the ends of (m)'s
    # lines beside it are whited out.
    'engineering-2014-HL-paper-q1m-crop': dict(
        doc='paper', page=3, rect=(344, 680, 563, 790), mask=[(343, 694, 372, 738)],
        ref='2014 HL Q1(m)'),
    # The plant with A, B and C and its other labels (the automatic crop lost B).
    'engineering-2014-HL-paper-q1o-crop': dict(
        doc='paper', page=4, rect=(55, 330, 512, 512), ref='2014 HL Q1(o)',
        letters=('A', 'B', 'C')),
    # The barrier with posts X and Y, and the stress-strain curves A, B and C.
    'engineering-2014-HL-paper-q2a-crop': dict(
        doc='paper', page=5, rect=(370, 76, 585, 356), ref='2014 HL Q2(a)',
        letters=('A', 'B', 'C', 'X', 'Y')),
    'engineering-2014-HL-paper-q2b-crop': dict(
        doc='paper', page=5, rect=(95, 425, 508, 498), ref='2014 HL Q2(b)'),
    # The iron-carbon diagram with both axes (the automatic crop cut off the
    # temperatures).
    'engineering-2014-HL-paper-q3b-crop': dict(
        doc='paper', page=6, rect=(148, 286, 426, 458), ref='2014 HL Q3(b)',
        letters=('A', 'B', 'X', 'Y')),
    # The weather vane alone (the automatic crop took in the "(50 marks)").
    'engineering-2014-HL-paper-q4a-crop': dict(
        doc='paper', page=7, rect=(448, 83, 564, 193), image=True, ref='2014 HL Q4(a)'),
    'engineering-2014-HL-paper-q4b-crop': dict(
        doc='paper', page=7, rect=(50, 302, 553, 386), ref='2014 HL Q4(b)'),
    'engineering-2014-HL-paper-q5a-crop': dict(
        doc='paper', page=8, rect=(110, 112, 495, 240), ref='2014 HL Q5(a)',
        letters=('A', 'B', 'C')),
    'engineering-2014-HL-paper-q5b-crop': dict(
        doc='paper', page=8, rect=(342, 422, 518, 523), image=True, ref='2014 HL Q5(b)'),
    # The controller with its label (the automatic crop cut the label off).
    'engineering-2014-HL-paper-q6a-crop': dict(
        doc='paper', page=9, rect=(165, 138, 432, 265), ref='2014 HL Q6(a)'),
    'engineering-2014-HL-paper-q7c-crop': dict(
        doc='paper', page=10, rect=(405, 552, 520, 620), image=True, ref='2014 HL Q7(c)'),
    # The linkage with its pivots and lever labelled (the automatic crop took in
    # the "(50 marks)").
    'engineering-2014-HL-paper-q8a-crop': dict(
        doc='paper', page=11, rect=(265, 80, 560, 232), ref='2014 HL Q8(a)'),
    'engineering-2014-HL-paper-q8c-crop': dict(
        doc='paper', page=11, rect=(338, 334, 532, 524), ref='2014 HL Q8(c)'),
    'engineering-2014-HL-paper-q8cor-crop': dict(
        doc='paper', page=11, rect=(190, 622, 440, 795), ref='2014 HL Q8(c)'),
    # ---- scheme: the drawings the answers are given with -------------------
    # Q1(h)'s note on Marie Curie as printed: the text layer misreads her
    # surname on the note's first line, so the option is lifted from after it
    # and the note itself is shown with the answer (scheme pp5-6).
    'engineering-2014-HL-scheme-q1h-sol': dict(
        doc='scheme', parts=[(5, (100, 716, 560, 763)), (6, (100, 64, 560, 96))],
        solution=True, ref='2014 HL Q1(h)'),
    'engineering-2014-HL-scheme-q1l-sol': dict(
        doc='scheme', page=6, rect=(412, 437, 515, 477), image=True, solution=True,
        ref='2014 HL Q1(l)'),
    'engineering-2014-HL-scheme-q1p-sol': dict(
        doc='scheme', page=8, rect=(474, 62, 574, 233), image=True, solution=True,
        ref='2014 HL Q1(p)'),
    'engineering-2014-HL-scheme-q2b-sol': dict(
        doc='scheme', page=9, rect=(145, 488, 545, 735), solution=True, ref='2014 HL Q2(b)'),
    'engineering-2014-HL-scheme-q2bi-sol': dict(
        doc='scheme', page=10, rect=(135, 78, 470, 124), solution=True,
        ref='2014 HL Q2(b)(i)'),
    'engineering-2014-HL-scheme-q2cii-sol': dict(
        doc='scheme', page=10, rect=(362, 428, 596, 640), solution=True,
        ref='2014 HL Q2(c)(ii)'),
    'engineering-2014-HL-scheme-q3cii-sol': dict(
        doc='scheme', page=12, rect=(380, 85, 590, 200), solution=True,
        ref='2014 HL Q3(c)(ii)'),
    'engineering-2014-HL-scheme-q4bi-sol': dict(
        doc='scheme', page=12, rect=(150, 545, 520, 752), solution=True,
        ref='2014 HL Q4(b)(i)'),
    'engineering-2014-HL-scheme-q4ci-sol': dict(
        doc='scheme', page=13, rect=(476, 340, 592, 578), solution=True,
        ref='2014 HL Q4(c)(i)'),
    'engineering-2014-HL-scheme-q5bii-sol': dict(
        doc='scheme', page=14, rect=(434, 573, 567, 740), image=True, solution=True,
        ref='2014 HL Q5(b)(ii)'),
    # The three flames with their labels; the end of the neutral flame's last
    # line, "welding.", runs into the box and is whited out.
    'engineering-2014-HL-scheme-q5ci-sol': dict(
        doc='scheme', page=15, rect=(355, 85, 595, 415), mask=[(354, 166, 386, 184)],
        solution=True,
        ref='2014 HL Q5(c)(i)'),
    'engineering-2014-HL-scheme-q6aii-sol': dict(
        doc='scheme', page=16, rect=(75, 192, 512, 333), solution=True,
        ref='2014 HL Q6(a)(ii)'),
    'engineering-2014-HL-scheme-q7c-sol': dict(
        doc='scheme', page=18, rect=(100, 545, 555, 656), solution=True, ref='2014 HL Q7(c)'),
    'engineering-2014-HL-scheme-q8a-sol': dict(
        doc='scheme', page=20, rect=(78, 165, 500, 335), solution=True, ref='2014 HL Q8(a)'),
    'engineering-2014-HL-scheme-q8b-sol': dict(
        doc='scheme', page=20, rect=(432, 652, 598, 750), solution=True, ref='2014 HL Q8(b)'),
    'engineering-2014-HL-scheme-q8c-sol': dict(
        doc='scheme', parts=[(21, (105, 148, 548, 290)), (21, (445, 282, 506, 390))],
        solution=True, ref='2014 HL Q8(c)'),
}

FOLDED = {
    'eng-2014-hl-q8-b-i': 'never shipped: (i) is one option of "Describe any three of the '
                          'following", carried by the Q8(b) card',
}

CARDS = [
    # ---- Question 1, Section A ("Any ten @ 5 marks each") ------------------
    dict(key=(1, 'a', None),
         why='Scheme p5 lists the hazards in one sentence, each lifted by its own word '
             'rectangle. "(Any two) 3 + 2".',
         topic='eng-3-1',
         lifted=[S(5, 65, 177, 237, 195), S(5, 237, 177, 487, 195), S(5, 487, 177, 560, 195),
                 S(5, 65, 191, 295, 209)],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         notes="The scheme prints '(Any two) 3 + 2'."),
    dict(key=(1, 'b', None),
         why='The table is photographed beside (b); scheme p5 lists its features in one '
             'sentence, each lifted by its own word rectangle. "(Any two) 3 + 2".',
         topic='eng-3-14',
         lifted=[S(5, 66, 233, 214, 251), S(5, 214, 233, 349, 251), S(5, 349, 233, 533, 251),
                 join(S(5, 533, 233, 565, 251), S(5, 66, 247, 231, 265))],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         question_figure='engineering-2014-HL-paper-q1b-art',
         notes="The scheme prints '(Any two) 3 + 2'."),
    dict(key=(1, 'c', None),
         why='Scheme p5 gives the advantages in one sentence, "5".',
         topic='eng-3-14',
         lifted=[S(5, 66, 290, 540, 320)], marks=[5], total=5,
         notes="The scheme prints '5'."),
    dict(key=(1, 'd', None),
         why='Scheme p5 lists the reasons in one sentence, each lifted by its own word '
             'rectangle. "(Any two) 3 + 2".',
         topic='eng-3-8',
         lifted=[S(5, 66, 346, 163, 364), S(5, 163, 346, 283, 364), S(5, 283, 346, 440, 364),
                 S(5, 440, 346, 542, 364)],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         notes="The scheme prints '(Any two) 3 + 2'."),
    dict(key=(1, 'e', None),
         why='The tablet is photographed beside (e); scheme p5 gives the advantages and the '
             'disadvantages under their headings, over "3 + 2".',
         topic='eng-3-8',
         lifted=[S(5, 66, 388, 510, 418), S(5, 66, 416, 490, 432)],
         marks=[3, 2], total=5,
         question_figure='engineering-2014-HL-paper-q1e-art',
         notes="The scheme prints '3 + 2' under its advantages and disadvantages, in "
               "that order."),
    dict(key=(1, 'f', None),
         why='Scheme p5 explains the importance in one paragraph, "5".',
         topic='eng-1-3',
         lifted=[S(5, 66, 454, 560, 540)], marks=[5], total=5,
         notes="The scheme prints '5'."),
    dict(key=(1, 'g', None),
         why='Scheme p5 describes each structure in turn in one paragraph, "5".',
         topic='eng-1-3',
         lifted=[S(5, 66, 562, 565, 620)], marks=[5], total=5,
         notes="The scheme prints '5'."),
    dict(key=(1, 'h', None),
         why='A lead-in over three people set as romans, "any one"; scheme pp5-6 write a '
             'note on each under the name, "5". The text layer cannot read Marie Curie\'s '
             'surname on her note\'s first line (its "ł" has no Unicode in the font and '
             'reaches the layer as "á"), so that option keeps only what the layer reads '
             'correctly, lifted from after the name, and the note is shown as printed '
             'with the answer.',
         topic='eng-3-14',
         lifted=[[join(S(5, 102, 646, 165, 662), S(5, 102, 660, 565, 718)),
                  join(S(5, 102, 716, 172, 733), S(5, 229, 730, 565, 746),
                       S(5, 102, 744, 565, 761), S(6, 102, 65, 555, 95)),
                  join(S(6, 102, 93, 180, 109), S(6, 102, 107, 560, 151))]],
         row_kind='anyN', group=(1, 5), marks=[5], tariff='fixed', total=5,
         figure='engineering-2014-HL-scheme-q1h-sol',
         notes="The scheme prints '5'. The scheme's note on Marie Curie is shown as printed: "
               "the option for her is lifted from after her full name on the note's first "
               "line, which the scheme's text layer cannot read."),
    dict(key=(1, 'i', None),
         why='The hand is photographed beside (i); scheme p6 lists the reasons in one '
             'sentence, each lifted by its own word rectangle. "(Any two) 3 + 2".',
         topic='eng-3-14',
         lifted=[S(6, 66, 177, 283, 195), join(S(6, 283, 177, 548, 195), S(6, 66, 191, 119, 209)),
                 S(6, 119, 191, 328, 209), join(S(6, 328, 191, 560, 209), S(6, 66, 205, 115, 222))],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         question_figure='engineering-2014-HL-paper-q1i-crop',
         notes="The scheme prints '(Any two) 3 + 2'."),
    dict(key=(1, 'j', None),
         why='Scheme p6 lists the properties in one sentence, each lifted by its own word '
             'rectangle. "(Any two) 3 + 2".',
         topic='eng-3-8',
         lifted=[S(6, 238, 247, 266, 264), S(6, 266, 247, 303, 264), S(6, 303, 247, 412, 264),
                 S(6, 412, 247, 465, 264), join(S(6, 465, 247, 530, 264), S(6, 66, 262, 126, 278)),
                 S(6, 126, 262, 175, 278)],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         notes="The scheme prints '(Any two) 3 + 2'."),
    dict(key=(1, 'k', None),
         why='Scheme p6 bullets five advantages under a heading; "(Any two) 3 + 2".',
         topic='eng-2-15',
         lifted=[S(6, 100, 320, 520, 334), S(6, 100, 334, 520, 349), S(6, 100, 349, 520, 364),
                 S(6, 100, 364, 520, 379), S(6, 100, 379, 520, 394)],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         notes="The scheme prints '(Any two) 3 + 2'."),
    dict(key=(1, 'l', None),
         why='Scheme p6 explains the bond under its heading beside a drawing of it, shown '
             'with the answer; "5".',
         topic='eng-1-3',
         lifted=[join(S(6, 66, 421, 150, 437), S(6, 66, 435, 370, 479))], marks=[5], total=5,
         figure='engineering-2014-HL-scheme-q1l-sol',
         notes="The scheme prints '5'."),
    dict(key=(1, 'm', None),
         why='The steering column is drawn with its nylon inserts labelled; scheme p6 lists '
             'the reasons in one sentence, each lifted by its own word rectangle. "(Any two) '
             '3 + 2". The reader files the drawing\'s label, the page footer and the '
             'Section B heading printed after (m) as its stem, so the card carries none.',
         topic='eng-1-9', stem=False,
         lifted=[S(6, 66, 519, 178, 537), S(6, 178, 519, 260, 537), S(6, 260, 519, 359, 537),
                 S(6, 359, 519, 435, 537), S(6, 66, 533, 198, 551)],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         question_figure='engineering-2014-HL-paper-q1m-crop',
         notes="The scheme prints '(Any two) 3 + 2'."),
    # ---- Question 1, Section B ("Answer all of the following") -------------
    dict(key=(1, 'n', None),
         why='Section B. Scheme pp6-7 bullet the efficiency and the environmental impact '
             'under their headings, "5 + 5"; each heading is one row.',
         topic='eng-3-14', stem=False,
         lifted=[join(S(6, 66, 660, 125, 676), S(6, 100, 674, 520, 764)),
                 join(S(7, 66, 79, 190, 95), S(7, 100, 93, 562, 370))],
         marks=[5, 5], total=10,
         notes="The scheme prints '5 + 5', for the efficiency and the environmental impact "
               "in that order."),
    dict(key=(1, 'o', 'i'),
         why='Section B. The plant is drawn with A, B and C labelled; scheme p7 names each '
             'after its letter, "1 + 1 + 1". The question is lifted with (o)\'s stimulus.',
         topic='eng-3-14', stem=False,
         question_lift=P(4, *_O1, more=[(110, 276, 300, 295)]),
         lifted=[S(7, 100, 409, 300, 425), S(7, 100, 423, 300, 439), S(7, 100, 437, 300, 453)],
         marks=[1, 1, 1], total=3,
         labels={'A': S(7, 124, 409, 300, 425), 'B': S(7, 124, 423, 300, 439),
                 'C': S(7, 124, 437, 300, 453)},
         question_figure='engineering-2014-HL-paper-q1o-crop',
         notes="The scheme prints '1 + 1 + 1'."),
    dict(key=(1, 'o', 'ii'),
         why='Section B. Scheme p7 describes the principle under its heading, "7".',
         topic='eng-3-14', stem=False,
         question_lift=P(4, *_O1, more=[(110, 297, 410, 316)]),
         lifted=[join(S(7, 100, 480, 230, 496), S(7, 100, 494, 562, 693))], marks=[7], total=7,
         question_figure='engineering-2014-HL-paper-q1o-crop',
         notes="The scheme prints '7'."),
    dict(key=(1, 'p', None),
         why='Section B. Scheme p8 describes the fission process in four paragraphs beside a '
             'drawing of it, shown with the answer; "4 + 3 + 3" over them, no paragraph '
             'priced apart, so an ordered split of the paragraphs.',
         topic='eng-3-14', stem=False,
         lifted=[S(8, 66, 65, 460, 123), S(8, 66, 121, 455, 165), S(8, 66, 163, 455, 207),
                 S(8, 66, 205, 450, 236)],
         tariff='orderedSplit', notation='4 + 3 + 3', ladder=10, total=10,
         figure='engineering-2014-HL-scheme-q1p-sol',
         notes="The scheme prints '4 + 3 + 3'."),
    dict(key=(1, 'q', None),
         why='Section B. Scheme p8 bullets four consequences under a heading; "4 + 3 + 3".',
         topic='eng-3-14', stem=False,
         lifted=[S(8, 100, 290, 560, 335), S(8, 100, 335, 560, 378), S(8, 100, 378, 560, 421),
                 S(8, 100, 421, 560, 464)],
         tariff='orderedSplit', notation='4 + 3 + 3', ladder=10, total=10,
         notes="The scheme prints '4 + 3 + 3'."),
    dict(key=(1, 'r', None),
         why='Section B. A lead-in over three safety measures set as romans, "any two"; '
             'scheme pp8-9 write on each under its name, "(Any two) 5 + 5".',
         topic='eng-3-14', stem=False,
         lifted=[[S(8, 100, 504, 560, 655), S(8, 100, 681, 565, 754),
                  S(9, 100, 65, 565, 151)]],
         row_kind='anyN', group=(2, 5), marks=[10], tariff='fixed', total=10,
         notes="The scheme prints '(Any two) 5 + 5'."),
    # ---- Question 2 --------------------------------------------------------
    dict(key=(2, 'a', 'i'), topic='eng-3-8',
         replaces=NEW + 'carried no picture of the curves A, B and C it asks about',
         why='The barrier is photographed and the three metals\' stress-strain curves drawn '
             'and lettered beside (a); scheme p9 describes each metal after its letter, "2 + '
             '2 + 2". The question is lifted with (a)\'s stimulus.',
         stem=False,
         question_lift=P(5, *_A2, more=[(110, 214, 360, 233)]),
         lifted=[S(9, 100, 290, 440, 306), S(9, 100, 304, 365, 320), S(9, 100, 318, 480, 334)],
         marks=[2, 2, 2], total=6,
         labels={'A': S(9, 155, 290, 440, 306), 'B': S(9, 155, 304, 365, 320),
                 'C': S(9, 155, 318, 480, 334)},
         question_figure='engineering-2014-HL-paper-q2a-crop',
         notes="The scheme prints '2 + 2 + 2'."),
    dict(key=(2, 'a', 'ii'), topic='eng-3-8',
         replaces=NEW + 'priced the three reasons 2 each and left out the metal selected, '
                  '"Metal C", priced 2 on its own line',
         why='Scheme p9 names the metal on its line, "2", then bullets three reasons, "2 + '
             '2" for two. The question is lifted with (a)\'s stimulus.',
         stem=False,
         question_lift=P(5, *_A2, more=[(110, 238, 345, 290)]),
         lifted=[S(9, 100, 360, 150, 376),
                 [S(9, 120, 389, 420, 405), S(9, 120, 403, 420, 420), S(9, 120, 418, 420, 435)]],
         row_kind='anyN', group=[None, (2, 2)], marks=[2, 4], tariff='fixed', total=6,
         question_figure='engineering-2014-HL-paper-q2a-crop',
         notes="The scheme prints '2' for the metal and '2 + 2' for two reasons."),
    dict(key=(2, 'b', None),
         why='"Plot the Stress-Strain diagram": scheme p9 answers with the plotted graph, '
             '"Graph 12" in the grid; the ask is the row, the graph shown with the answer. '
             'Lifted with (b)\'s results.',
         topic='eng-3-8', stem=False,
         question_lift=P(5, *_B2, more=[_GRAPH2]),
         special={'kind': 'ask'}, total=12,
         question_figure='engineering-2014-HL-paper-q2b-crop',
         figure='engineering-2014-HL-scheme-q2b-sol',
         notes="The scheme prints '12' under the graph."),
    dict(key=(2, 'b', 'i'),
         why='Scheme p10 gives Young\'s modulus only as a stacked fraction of stress over '
             'strain; the ask is the row, its print shown with the answer, "4".',
         topic='eng-3-8', stem=False,
         question_lift=P(5, *_B2, more=[_GRAPH2, (110, 529, 265, 548)]),
         special={'kind': 'ask'}, total=4,
         question_figure='engineering-2014-HL-paper-q2b-crop',
         figure='engineering-2014-HL-scheme-q2bi-sol',
         notes="The scheme prints '4'."),
    dict(key=(2, 'b', 'ii'),
         why='Scheme p10 reads the proof stress off the graph in one line, "4".',
         topic='eng-3-8', stem=False,
         question_lift=P(5, *_B2, more=[_GRAPH2, (110, 549, 225, 569)]),
         lifted=[S(10, 138, 161, 305, 179)], marks=[4], total=4,
         question_figure='engineering-2014-HL-paper-q2b-crop',
         figure='engineering-2014-HL-scheme-q2b-sol',
         notes="The scheme prints '4'."),
    dict(key=(2, 'c', 'ii'),
         replaces=NEW + 'read the tariff, "(Name and Describe) 10", as a marking point and '
                  'left out the test\'s name, "X-ray / Radiography testing", and the drawing',
         why='Scheme p10 names the test and describes it beside a labelled drawing, shown '
             'with the answer; "(Name and Describe) 10".',
         topic='eng-3-8',
         lifted=[S(10, 100, 430, 365, 602)], marks=[10], total=10,
         question_figure='engineering-2014-HL-paper-q2ci-art',
         figure='engineering-2014-HL-scheme-q2cii-sol',
         notes="The scheme prints '(Name and Describe) 10'."),
    # ---- Question 3 --------------------------------------------------------
    dict(key=(3, 'a', 'iii'),
         why='One of "Answer any two of the following", "(Any two) 8 + 8": scheme p11 '
             'explains the term in one paragraph.',
         topic='eng-1-3',
         lifted=[S(11, 100, 233, 560, 292)], marks=[8], total=8,
         notes="The scheme prints '(Any two) 8 + 8' for the two parts answered."),
    dict(key=(3, 'a', 'iv'), topic='eng-1-4',
         replaces=NEW + 'read the "(Any two) 8 + 8" tariff as a marking point',
         why='One of "Answer any two of the following": scheme p11 gives the effect of five '
             'elements, each under its name; the 8 for the part is not split between the two '
             'asked for.',
         lifted=[S(11, 100, 346, 565, 390), S(11, 100, 388, 480, 404), S(11, 100, 402, 400, 418),
                 S(11, 100, 416, 525, 446), S(11, 100, 444, 545, 475)],
         tariff='questionTotal', total=8,
         notes="The scheme prints '(Any two) 8 + 8' for the two parts answered."),
    dict(key=(3, 'b', 'i'), topic='eng-1-3',
         replaces=NEW + 'carried no picture of the regions A and B it asks about',
         why='The diagram is drawn with its regions lettered A and B; scheme p11 names each '
             'after its letter, "4 + 4". The question is lifted with (b)\'s stimulus.',
         stem=False,
         question_lift=P(6, *_B3, more=[(110, 477, 256, 496)]),
         lifted=[S(11, 100, 515, 250, 531), S(11, 100, 529, 250, 545)],
         marks=[4, 4], total=8,
         labels={'A': S(11, 122, 515, 250, 531), 'B': S(11, 122, 529, 250, 545)},
         question_figure='engineering-2014-HL-paper-q3b-crop',
         notes="The scheme prints '4 + 4'."),
    dict(key=(3, 'b', 'ii'), topic='eng-1-3',
         replaces=NEW + 'carried no picture of the steels X and Y it asks about',
         why='Scheme p11 describes the steel at X and at Y after their letters, "4 + 4". The '
             'question is lifted with (b)\'s stimulus.',
         stem=False,
         question_lift=P(6, *_B3, more=[(110, 498, 456, 533)]),
         lifted=[S(11, 100, 571, 520, 587), S(11, 100, 585, 520, 601)],
         marks=[4, 4], total=8,
         question_figure='engineering-2014-HL-paper-q3b-crop',
         notes="The scheme prints '4 + 4', for X and Y in that order."),
    dict(key=(3, 'c', 'i'), topic='eng-2-6',
         replaces=NEW + 'left out the headings, "Height gauge tip." and "Surface plate.", '
                  'that say which answer is which',
         why='The height gauge is photographed with its tip and surface plate labelled; '
             'scheme p11 answers for each under its heading, "10" for the part.',
         lifted=[join(S(11, 100, 656, 195, 672), S(11, 100, 670, 520, 700)),
                 join(S(11, 100, 702, 180, 719), S(11, 100, 717, 565, 761))],
         tariff='questionTotal', total=10,
         question_figure='engineering-2014-HL-paper-q3ci-art',
         notes="The scheme prints '10'."),
    dict(key=(3, 'c', 'ii'), topic='eng-2-6',
         replaces=NEW + 'gave the process without the drawing the part asks for',
         why='Scheme p12 describes flame hardening beside a labelled drawing, shown with the '
             'answer; "8".',
         lifted=[join(S(12, 100, 93, 200, 109), S(12, 100, 107, 380, 137)),
                 S(12, 100, 135, 380, 165), S(12, 100, 163, 380, 179)],
         tariff='questionTotal', total=8,
         question_figure='engineering-2014-HL-paper-q3ci-art',
         figure='engineering-2014-HL-scheme-q3cii-sol',
         notes="The scheme prints '8'."),
    # ---- Question 4 --------------------------------------------------------
    dict(key=(4, 'a', 'i'),
         why='The weather vane is photographed beside (a); scheme p12 gives three factors, '
             'one a paragraph, "(Any two) 4 + 4".',
         topic='eng-3-7',
         lifted=[[S(12, 100, 332, 560, 362), S(12, 100, 360, 520, 390),
                  S(12, 100, 388, 460, 404)]],
         row_kind='anyN', group=(2, 4), marks=[8], tariff='fixed', total=8,
         question_figure='engineering-2014-HL-paper-q4a-crop',
         notes="The scheme prints '(Any two) 4 + 4'."),
    dict(key=(4, 'a', 'ii'),
         why='Scheme p12 gives four methods, one a line, "(Any two) 4 + 4".',
         topic='eng-3-7',
         lifted=[[S(12, 100, 431, 565, 446), S(12, 100, 446, 300, 461),
                  S(12, 100, 461, 430, 475), S(12, 100, 475, 300, 489)]],
         row_kind='anyN', group=(2, 4), marks=[8], tariff='fixed', total=8,
         question_figure='engineering-2014-HL-paper-q4a-crop',
         notes="The scheme prints '(Any two) 4 + 4'."),
    dict(key=(4, 'b', 'i'),
         why='The scheme answers with the drawn equilibrium diagram itself (p12), "8"; the '
             'ask is the row, the drawing shown with the answer. Lifted with (b)\'s table '
             'lead-in.',
         topic='eng-1-3', stem=False,
         question_lift=P(7, *_B4, more=[(110, 400, 455, 435)]),
         special={'kind': 'ask'}, total=8,
         question_figure='engineering-2014-HL-paper-q4b-crop',
         figure='engineering-2014-HL-scheme-q4bi-sol',
         notes="The scheme prints '8'."),
    dict(key=(4, 'b', 'ii'),
         why='Scheme pp12-13 label the drawn diagram (the labels are lifted off the drawing) '
             'and describe six features, "(Any three labels @ 1 mark each) 3", "(Any three '
             'descriptions @ 1 mark each) 3".',
         topic='eng-1-3', stem=False,
         question_lift=P(7, *_B4, more=[(110, 437, 370, 456)]),
         lifted=[[S(12, 230, 553, 266, 571), S(12, 288, 557, 360, 575),
                  S(12, 320, 592, 405, 610), S(12, 210, 600, 228, 619),
                  S(12, 298, 622, 360, 640), join(S(12, 233, 641, 280, 659),
                                                  S(12, 233, 657, 265, 675)),
                  S(12, 296, 682, 328, 700)],
                 [S(13, 100, 65, 440, 82), S(13, 100, 83, 560, 115), S(13, 100, 116, 562, 148),
                  S(13, 100, 149, 300, 166), S(13, 100, 168, 310, 185), S(13, 100, 187, 562, 217)]],
         row_kind='anyN', group=[(3, 1), (3, 1)], marks=[3, 3], tariff='fixed', total=6,
         question_figure='engineering-2014-HL-paper-q4b-crop',
         figure='engineering-2014-HL-scheme-q4bi-sol',
         notes="The scheme prints '(Any three labels @ 1 mark each) 3' and '(Any three "
               "descriptions @ 1 mark each) 3'."),
    dict(key=(4, 'c', 'i'), topic='eng-1-3',
         replaces=NEW + 'split the substitutional solution into three options and set them '
                  'beside the interstitial one under one ordered split',
         why='Scheme p13 describes each solid solution under its heading beside a drawing of '
             'it, shown with the answer; "4 + 4".',
         lifted=[join(S(13, 100, 356, 255, 372), S(13, 100, 370, 470, 442)),
                 join(S(13, 100, 482, 240, 498), S(13, 100, 496, 475, 554))],
         marks=[4, 4], total=8,
         figure='engineering-2014-HL-scheme-q4ci-sol',
         notes="The scheme prints '4 + 4', for the substitutional and the interstitial "
               "solution in that order."),
    dict(key=(5, 'a', 'i'),
         why='One of "answer any three of the following", "(Any three) 6 + 6 + 6": the '
             'circuit is drawn with A, B and C; scheme p14 names each after its letter, the '
             '6 not split between them. The question is lifted with (a)\'s lead-in.',
         topic='eng-2-10', stem=False,
         question_lift=P(8, *_A5, more=[(110, 256, 500, 275)]),
         lifted=[S(14, 100, 100, 200, 116), S(14, 100, 114, 200, 130), S(14, 100, 128, 200, 144)],
         tariff='questionTotal', total=6,
         labels={'A': S(14, 122, 100, 200, 116), 'B': S(14, 122, 114, 200, 130),
                 'C': S(14, 122, 128, 200, 144)},
         question_figure='engineering-2014-HL-paper-q5a-crop',
         notes="The scheme prints '(Any three) 6 + 6 + 6' for the three parts answered."),
    dict(key=(5, 'a', 'ii'), topic='eng-2-10',
         replaces=NEW + 'left the transformer\'s heading off its answer and carried no '
                  'picture of the components A, B and C it asks about',
         why='One of "answer any three": scheme p14 describes each component under its '
             'name; the 6 is not split between them. The question is lifted with (a)\'s '
             'lead-in.',
         stem=False,
         question_lift=P(8, *_A5, more=[(110, 276, 520, 295)]),
         lifted=[join(S(14, 100, 156, 180, 173), S(14, 100, 170, 560, 229)),
                 S(14, 100, 227, 560, 271), S(14, 100, 269, 480, 299)],
         tariff='questionTotal', total=6,
         labels={'A': S(14, 122, 100, 200, 116), 'B': S(14, 122, 114, 200, 130),
                 'C': S(14, 122, 128, 200, 144)},
         question_figure='engineering-2014-HL-paper-q5a-crop',
         notes="The scheme prints '(Any three) 6 + 6 + 6' for the three parts answered."),
    dict(key=(5, 'a', 'iv'), topic='eng-2-10',
         replaces=NEW + 'read the "(Any three) 6 + 6 + 6" tariff as a marking point',
         why='One of "answer any three": scheme p14 gives the advantages in three sentences '
             'under a heading; the 6 is not split between the two asked for.',
         lifted=[S(14, 100, 465, 500, 482), S(14, 100, 482, 540, 496), S(14, 100, 496, 510, 510)],
         tariff='questionTotal', total=6,
         notes="The scheme prints '(Any three) 6 + 6 + 6' for the three parts answered."),
    dict(key=(5, 'b', 'i'), topic='eng-2-10',
         replaces=NEW + 'took the part\'s tariff, "4", printed at the end of the line, into '
                  'the marking point',
         why='The exhaust is photographed beside (b); scheme p14 names the process on one '
             'line, "4".',
         lifted=[S(14, 100, 557, 320, 575)], marks=[4], total=4,
         question_figure='engineering-2014-HL-paper-q5b-crop',
         notes="The scheme prints '4'."),
    dict(key=(5, 'b', 'ii'), topic='eng-2-10',
         replaces=NEW + 'left out the filler metal, "A stainless steel filler metal is added '
                  'manually to the weld pool when necessary.", and the drawing the part asks '
                  'for',
         why='Scheme p14 describes TIG welding in one passage beside a drawing of the set, '
             'shown with the answer; "12".',
         lifted=[S(14, 100, 599, 400, 713)], marks=[12], total=12,
         question_figure='engineering-2014-HL-paper-q5b-crop',
         figure='engineering-2014-HL-scheme-q5bii-sol',
         notes="The scheme prints '12'."),
    dict(key=(5, 'c', 'i'), topic='eng-2-10', stem=False,
         replaces=NEW + 'set the twelve flame bullets as one question total and ran the OR '
                  'branch\'s ask into this one',
         why='Both (c)s price their (i) at 8 (scheme p15): the three flames under their '
             'names, beside labelled drawings shown with the answer, the 8 not split between '
             'them (one row); or two of three reasons for robotic welding on one line, "4 + '
             '4". One card for the printed OR, each branch a route.',
         question_lift=P(8, *_C5A, more=[(110, 596, 440, 631), _ORW5, (110, 713, 500, 748)]),
         lifted=[join(S(15, 66, 93, 150, 109), S(15, 80, 107, 400, 183),
                      S(15, 66, 223, 160, 239), S(15, 80, 237, 400, 299),
                      S(15, 66, 339, 175, 355), S(15, 80, 353, 400, 429)),
                 [S(15, 100, 690, 218, 708), S(15, 218, 690, 325, 708), S(15, 325, 690, 368, 708)]],
         row_kind='anyN', group=[None, (2, 4)], marks=[8, 8], routes=['a', 'b'], total=8,
         figure='engineering-2014-HL-scheme-q5ci-sol',
         notes="The scheme prints '8' for the flames and '4 + 4' for robotic welding. "
               + _OR5),
    dict(key=(5, 'c', 'ii'), topic='eng-2-10', stem=False,
         replaces=NEW + 'set the joint protection bullets beside the OR branch\'s answer under '
                  'one question total',
         why='Both (c)s price their (ii) at 8 (scheme p15): four methods of joint protection '
             'bulleted, the 8 not split between the three asked for (one row); or two of '
             'three robot drives on one line, "4 + 4". One card, each branch a route.',
         question_lift=P(8, *_C5A, more=[(110, 636, 375, 655), _ORW5, (110, 751, 440, 770)]),
         lifted=[S(15, 100, 469, 565, 643),
                 [S(15, 100, 728, 203, 746), S(15, 203, 728, 262, 746), S(15, 262, 728, 313, 746)]],
         row_kind='anyN', group=[None, (2, 4)], marks=[8, 8], routes=['a', 'b'], total=8,
         notes="The scheme prints '8' for joint protection and '4 + 4' for the robot "
               "drives. " + _OR5),
    # ---- Question 6 --------------------------------------------------------
    dict(key=(6, 'a', 'i'), topic='eng-1-9',
         replaces=NEW + 'set the process and its reason as one row under a question total; '
                  'the scheme prices them "3 + 3"',
         why='The controller is photographed with its casing labelled; scheme p16 names the '
             'process and gives the reason in the next sentence, "3 + 3". The question is '
             'lifted with (a)\'s stimulus.',
         stem=False,
         question_lift=P(9, *_A6, more=[(110, 285, 560, 318)]),
         lifted=[S(16, 100, 107, 205, 123), join(S(16, 205, 107, 560, 123),
                                                 S(16, 100, 121, 365, 137))],
         marks=[3, 3], total=6,
         question_figure='engineering-2014-HL-paper-q6a-crop',
         notes="The scheme prints '3 + 3', for the process and the reason in that order."),
    dict(key=(6, 'a', 'ii'),
         why='Scheme p16 describes injection moulding beside a labelled drawing of the '
             'machine, shown with the answer; "10".',
         topic='eng-1-9', stem=False,
         question_lift=P(9, *_A6, more=[(110, 326, 560, 345)]),
         lifted=[join(S(16, 100, 163, 525, 179), S(16, 100, 371, 565, 500))], marks=[10],
         total=10,
         question_figure='engineering-2014-HL-paper-q6a-crop',
         figure='engineering-2014-HL-scheme-q6aii-sol',
         notes="The scheme prints '10'."),
    dict(key=(6, 'b', None), topic='eng-1-9',
         replaces=NEW + 'offered the "(Any three) 6 + 6 + 6" tariff as an option',
         why='A lead-in over four items set as romans, "any three"; scheme p16 answers each '
             'in turn, "(Any three) 6 + 6 + 6".',
         lifted=[[S(16, 100, 568, 560, 598), S(16, 100, 610, 520, 640),
                  S(16, 100, 652, 560, 696), S(16, 100, 708, 560, 753)]],
         row_kind='anyN', group=(3, 6), marks=[18], tariff='fixed', total=18,
         notes="The scheme prints '(Any three) 6 + 6 + 6'."),
    dict(key=(6, 'c', 'i'), topic='eng-1-9',
         replaces=NEW + 'set the four reasons as one row under a question total',
         why='The kettle is photographed beside (c); scheme p17 gives the reasons in one '
             'sentence, each lifted by its own word rectangle. "4 + 4" for two. The '
             'question is lifted with (c)\'s stimulus.',
         stem=False,
         question_lift=P(9, *_C6, more=[(110, 642, 350, 677)]),
         lifted=[S(17, 197, 79, 350, 95), S(17, 350, 79, 472, 95),
                 join(S(17, 472, 79, 545, 95), S(17, 100, 93, 310, 109)),
                 S(17, 310, 93, 420, 109)],
         tariff='orderedSplit', notation='4 + 4', ladder=8, total=8,
         question_figure='engineering-2014-HL-paper-q6ci-art',
         notes="The scheme prints '4 + 4'."),
    # ---- Question 7 --------------------------------------------------------
    dict(key=(7, 'a', 'v'),
         why='One of "Answer any three of the following", "(Any three) 6 + 6 + 6": scheme '
             'p18 lists the causes in one sentence, each lifted by its own word rectangle; '
             'the 6 is not split between the two asked for.',
         topic='eng-3-12',
         lifted=[S(18, 296, 135, 455, 151), join(S(18, 455, 135, 530, 151),
                                                 S(18, 100, 149, 200, 165)),
                 S(18, 200, 149, 380, 165), S(18, 380, 149, 530, 165)],
         tariff='questionTotal', total=6,
         notes="The scheme prints '(Any three) 6 + 6 + 6' for the three parts answered."),
    dict(key=(7, 'b', 'ii'), topic='eng-2-11',
         replaces=NEW + 'took the part\'s tariff, "2 + 2 + 2", into the last function',
         why='Scheme p18 gives six functions, one a line, under a heading; "2 + 2 + 2" for '
             'three.',
         lifted=[S(18, 100, 402, 400, 418), S(18, 100, 418, 400, 432), S(18, 100, 432, 460, 446),
                 S(18, 100, 446, 300, 461), S(18, 100, 461, 300, 475), S(18, 100, 475, 300, 489)],
         tariff='orderedSplit', notation='2 + 2 + 2', ladder=6, total=6,
         notes="The scheme prints '2 + 2 + 2'."),
    dict(key=(7, 'c', None),
         why='Paper p10 sets two alternative (c)s either side of an OR. This card is the '
             'first, "Answer part (i) or part (ii)", "(Any one) 16": scheme pp18-19 answer (i) '
             'with a drawing of each tool under its heading, its name below (the drawings '
             'shown with the answer), and (ii) with the manufacture and the advantages. One '
             'option per part.',
         topic='eng-2-11', stem=False,
         question_lift=P(10, 82, 486, 220, 505, more=[(82, 518, 435, 537), (110, 532, 260, 581),
                                                      (82, 589, 385, 622)]),
         lifted=[[join(S(18, 100, 529, 230, 547), S(18, 100, 655, 235, 673),
                       S(18, 262, 529, 390, 547), S(18, 262, 655, 392, 673),
                       S(18, 430, 529, 545, 547), S(18, 442, 655, 545, 673)),
                  join(S(18, 100, 740, 565, 771), S(19, 100, 79, 565, 241),
                       S(19, 100, 267, 560, 367))]],
         row_kind='anyN', group=(1, 16), marks=[16], tariff='fixed', total=16,
         question_figure='engineering-2014-HL-paper-q7c-crop',
         figure='engineering-2014-HL-scheme-q7c-sol',
         notes="The scheme prints '(Any one) 16'. " + _OR7),
    dict(key=(7, 'c', 'i'), topic='eng-2-13', stem=False,
         replaces=NEW + 'ran the first (c)\'s tool names in with the CNC advantages',
         why='The CNC branch\'s (i), lifted with its cue: scheme p19 bullets three '
             'advantages, "3 + 3".',
         question_lift=P(10, *_C7B, more=[(110, 693, 410, 712)]),
         lifted=[S(19, 120, 450, 440, 466), S(19, 120, 465, 440, 481), S(19, 120, 480, 440, 496)],
         tariff='orderedSplit', notation='3 + 3', ladder=6, total=6,
         notes="The scheme prints '3 + 3'. " + _OR7),
    dict(key=(7, 'c', 'ii'), topic='eng-2-13', stem=False,
         replaces=NEW + 'ran the first (c)\'s carbide answer in with the CNC safety features',
         why='The CNC branch\'s (ii): scheme p19 bullets three features, "3 + 3".',
         question_lift=P(10, *_C7B, more=[(110, 717, 360, 736)]),
         lifted=[S(19, 120, 537, 400, 553), S(19, 120, 552, 480, 568), S(19, 120, 567, 400, 583)],
         tariff='orderedSplit', notation='3 + 3', ladder=6, total=6,
         notes="The scheme prints '3 + 3'. " + _OR7),
    dict(key=(7, 'c', 'iii'), topic='eng-2-13', stem=False,
         replaces=NEW + 'carried the first (c)\'s "Answer part (i) or part (ii):" as its '
                  'question',
         why='The CNC branch\'s (iii): scheme p19 explains simulation under its heading, "4".',
         question_lift=P(10, *_C7B, more=[(110, 740, 320, 760)]),
         lifted=[join(S(19, 100, 610, 170, 626), S(19, 100, 624, 560, 654))], marks=[4], total=4,
         notes="The scheme prints '4'. " + _OR7),
    # ---- Question 8 --------------------------------------------------------
    dict(key=(8, 'a', None),
         why='The linkage is drawn beside (a) with its pivots and lever labelled; scheme p20 '
             'describes the action in one paragraph over a labelled drawing, shown with the '
             'answer; "16".',
         topic='eng-2-15',
         lifted=[S(20, 66, 100, 565, 158)], marks=[16], total=16,
         question_figure='engineering-2014-HL-paper-q8a-crop',
         figure='engineering-2014-HL-scheme-q8a-sol',
         notes="The scheme prints '16'."),
    dict(key=(8, 'b', None), topic='eng-2-15',
         replaces=NEW + 'split the cylinder, rack and pinion and idler gear answers into one '
                  'option a paragraph and offered the "(Any three) 6 + 6 + 6" tariff as one',
         why='A lead-in over five items set as romans, "any three"; scheme p20 answers each '
             'in turn, the idler gears beside a labelled drawing shown with the answer, '
             '"(Any three) 6 + 6 + 6".',
         lifted=[[S(20, 100, 381, 530, 455), S(20, 100, 473, 545, 532), S(20, 100, 550, 390, 581),
                  S(20, 100, 593, 560, 638), S(20, 100, 670, 520, 756)]],
         row_kind='anyN', group=(3, 6), marks=[18], tariff='fixed', total=18,
         figure='engineering-2014-HL-scheme-q8b-sol',
         notes="The scheme prints '(Any three) 6 + 6 + 6'."),
    dict(key=(8, 'c', None),
         why='Paper p11 sets two alternative (c)s either side of an OR. This card is the '
             'first, the gull-wing doors: scheme p21 suggests a gear train, the drive '
             'described beside and under a labelled drawing (the drawing\'s own label "Gear '
             'directly connected to the gull-wing door." is left out of the words), shown '
             'with the answer, "Suggested solution - other viable solutions are '
             'acceptable."; "16".',
         topic='eng-2-15', stem=False,
         question_lift=P(11, 82, 417, 335, 499),
         lifted=[join(S(21, 66, 121, 300, 137), S(21, 400, 154, 540, 277),
                      S(21, 66, 321, 460, 365), S(21, 66, 405, 460, 421))],
         marks=[16], total=16,
         question_figure='engineering-2014-HL-paper-q8c-crop',
         figure='engineering-2014-HL-scheme-q8c-sol',
         notes="The scheme prints '16', and 'Suggested solution - other viable solutions are "
               "acceptable.' " + _OR8),
    dict(key=(8, 'c', 'i'), topic='eng-2-16', stem=False,
         replaces=NEW + 'set the three components as one row under a question total',
         why='The timer branch\'s (i), lifted with its cue: scheme p21 names the components '
             'on one line, each lifted by its own word rectangle; "4 + 4".',
         question_lift=P(11, *_C8B, more=[(110, 582, 415, 601)]),
         lifted=[S(21, 100, 490, 190, 508), S(21, 190, 490, 241, 508), S(21, 241, 490, 295, 508)],
         tariff='orderedSplit', notation='4 + 4', ladder=8, total=8,
         question_figure='engineering-2014-HL-paper-q8cor-crop',
         notes="The scheme prints '4 + 4'. " + _OR8),
]

TOPICS = {
    'eng-2014-hl-q4-b-iii': ('eng-1-3', 'the melting points are read off the equilibrium '
                             'diagram the part is printed under; "Zinc" outvoted it for '
                             'non-ferrous metals'),
    'eng-2014-hl-q4-c-ii': ('eng-1-3', 'the movement of a line defect (a dislocation) is '
                            'crystal structure; "shear force" outvoted it for testing'),
}

_CNC = ('CNC machining (the OR branch of Q7(c)), which the reference files Q7 under; the '
        'card\'s syllabus heading is Manufacturing systems.')

ATLAS = {
    'eng-2014-hl-q2-c-i': dict(
        topics=['Testing of Materials and Products'],
        note='Evaluating a weld sample\'s porosity, which the reference files Q2 under; the '
             'card\'s syllabus heading is Joining.'),
    'eng-2014-hl-q3-a-iv': dict(
        topics=['The Structure of Materials'],
        note='The effect of alloying elements on steel; the card\'s syllabus heading is Iron '
             'and steel.'),
    **{f'eng-2014-hl-q7-c-{r}': dict(topics=['Machining & Metrology'], note=_CNC)
       for r in ('i', 'ii', 'iii')},
}
