"""2017 Higher Level: the parts eng_all refuses or gets wrong, from the page.

Paper and scheme as the PDFs number their pages. The marks grid is on scheme
p4: Question 1 is Section A, "Any ten @ 5 marks each", and Section B, "Answer
all of the following", (n) to (r); Questions 2-8 are 50 marks each. The scheme
prints a part's marks under its answer ("(Any two) 3 + 2", "(Any three) 6 + 6 +
6"), and a "(Any three)" tariff closes each list of romans, which the automatic
author reads as an answer row. This sitting had no cards before the lane: every
card here is new, and a `replaces=` names the automatic card it rebuilds before
it ever shipped.
"""
from eng_lift import join, lift

Y, L = 2017, 'hl'
NEW = 'never shipped: the automatic card '
OWNED = ('never shipped: the automatic author builds this card only from the lifts this '
         'entry records, so the entry owns it')


def S(page, *rect):
    return lift(Y, L, 'scheme', page, rect)


def P(page, *rect, more=()):
    return lift(Y, L, 'paper', page, rect, more=more)


# Paper stems the romans are lifted with.
_P1 = (90, 356, 355, 385)             # p4: Q1(p), "as shown opposite"
_A2 = (90, 100, 527, 150)             # p5: Q2(a), the survival cell
_B2 = (90, 321, 530, 354)             # p5: Q2(b), the specimen
_B3 = (90, 286, 430, 302)             # p6: Q3(b), the iron-carbon diagram
_B4 = (90, 287, 530, 303)             # p7: Q4(b), the table
_GRAPH4 = (90, 417, 250, 433)         # "Using the graph paper supplied:"
_C5A = (90, 506, 475, 522)            # p8: Q5(c), the welding (c)
_C5B = (90, 647, 500, 680)            # the Dyson (c)
_C7A = (90, 466, 520, 501)            # p10: Q7(c), magnetic chucks
_ORW7 = (290, 604, 316, 623)
_C7B = (90, 644, 510, 676)            # the 3-D printer (c)
_C8A = (90, 435, 362, 453)            # p11: Q8(c), the wheelchair car
_ORW8 = (290, 601, 316, 620)
_C8B = (90, 646, 490, 662)            # the PCB (c)

_OR5 = ('The paper sets two (c)s either side of an OR: the welding (c), any one of (i) '
        'and (ii) for 16, answered at the letter, and the robotic vacuum cleaner (c), '
        'whose (i) and (ii) are carded apart.')
_OR7 = ('The paper sets two (c)s either side of an OR, magnetic chucks and CNC 3-D '
        'printers; the scheme prices each (i) at 8 and each (ii) at 4 + 4.')
_SERVO = ("The scheme adds 'Servo motors and Stepper motor could also be considered for "
          "both parts of the question.'")
_OR8 = ('The paper sets two (c)s either side of an OR, the wheelchair car and the PCB; '
        'the scheme prices (i) at 8 for the car and 4 + 4 for the PCB, and each (ii) at '
        "8, under 'Suggested solutions, suitable alternatives are considered'.")

CROPS = {
    # ---- paper ------------------------------------------------------------
    # The results table (b)'s three romans are worked from.
    'engineering-2017-HL-paper-q2b-crop': dict(
        doc='paper', page=5, rect=(90, 368, 513, 419), ref='2017 HL Q2(b)'),
    # The iron-carbon diagram with both axes (the automatic crop lost the
    # % Carbon axis and its values).
    'engineering-2017-HL-paper-q3b-crop': dict(
        doc='paper', page=6, rect=(80, 305, 470, 522), ref='2017 HL Q3(b)',
        letters=('A', 'B', 'C', 'D', 'E')),
    'engineering-2017-HL-paper-q3c-crop': dict(
        doc='paper', page=6, rect=(396, 648, 558, 770), image=True, ref='2017 HL Q3(c)'),
    # The spring alone (the automatic crop took in (a)'s prose).
    'engineering-2017-HL-paper-q4a-crop': dict(
        doc='paper', page=7, rect=(425, 107, 538, 220), image=True, ref='2017 HL Q4(a)'),
    # The solidification table (b)'s romans are worked from.
    'engineering-2017-HL-paper-q4b-crop': dict(
        doc='paper', page=7, rect=(53, 317, 573, 397), ref='2017 HL Q4(b)'),
    # The tent and the close-up of its tube and joint.
    'engineering-2017-HL-paper-q6a-crop': dict(
        doc='paper', page=9, rect=(112, 138, 515, 248), ref='2017 HL Q6(a)'),
    # Each (c) shows its own machine: the magnetic chuck, then the 3-D printer.
    'engineering-2017-HL-paper-q7c-crop': dict(
        doc='paper', parts=[(10, (402, 494, 555, 610)), (10, (380, 675, 518, 790))],
        layout='row', ref='2017 HL Q7(c)'),
    # The wheelchair car with its "sliding door" label, then the PCB; the end
    # of (c)(i)'s first line runs into the car's left edge and is whited out.
    'engineering-2017-HL-paper-q8c-crop': dict(
        doc='paper', parts=[(11, (331, 462, 572, 598)), (11, (412, 662, 559, 769))],
        mask=[(329, 482, 344, 498)], layout='row', ref='2017 HL Q8(c)'),
    # ---- scheme: the drawings the answers are given with -------------------
    'engineering-2017-HL-scheme-q1k-sol': dict(
        doc='scheme', page=6, rect=(70, 374, 520, 460), solution=True,
        ref='2017 HL Q1(k)'),
    'engineering-2017-HL-scheme-q1o-sol': dict(
        doc='scheme', page=7, rect=(320, 405, 554, 560), image=True, solution=True,
        ref='2017 HL Q1(o)'),
    'engineering-2017-HL-scheme-q2ai-sol': dict(
        doc='scheme', page=10, rect=(388, 204, 582, 366), solution=True,
        ref='2017 HL Q2(a)(i)'),
    'engineering-2017-HL-scheme-q2aii-sol': dict(
        doc='scheme', page=10, rect=(310, 512, 562, 666), solution=True,
        ref='2017 HL Q2(a)(ii)'),
    'engineering-2017-HL-scheme-q2b-sol': dict(
        doc='scheme', page=11, rect=(86, 96, 542, 392), solution=True,
        ref='2017 HL Q2(b)'),
    # The X-ray drawing; the ends of two lines of the answer run into its
    # left edge and are whited out.
    'engineering-2017-HL-scheme-q2ci-sol': dict(
        doc='scheme', page=11, rect=(353, 544, 568, 742),
        mask=[(351, 673, 368, 704)], solution=True, ref='2017 HL Q2(c)(i)'),
    'engineering-2017-HL-scheme-q3cii-sol': dict(
        doc='scheme', page=13, rect=(128, 365, 444, 508), solution=True,
        ref='2017 HL Q3(c)(ii)'),
    'engineering-2017-HL-scheme-q4b-sol': dict(
        doc='scheme', page=14, rect=(86, 368, 508, 627), solution=True,
        ref='2017 HL Q4(b)'),
    # The two drawings: the crystalline and amorphous arrangements of (i) and
    # the BCC and FCC cells of (iii), each under its heading.
    'engineering-2017-HL-scheme-q4c-sol': dict(
        doc='scheme', parts=[(15, (150, 70, 490, 186)), (15, (165, 274, 442, 376))],
        mask=[(163, 309, 192, 355), (414, 309, 444, 340)], solution=True,
        ref='2017 HL Q4(c)'),
    'engineering-2017-HL-scheme-q5aii-sol': dict(
        doc='scheme', page=15, rect=(372, 550, 568, 754), solution=True,
        ref='2017 HL Q5(a)(ii)'),
    'engineering-2017-HL-scheme-q5c-sol': dict(
        doc='scheme', parts=[(17, (155, 90, 478, 200)), (17, (436, 366, 558, 521)),
                             (17, (432, 542, 558, 698))],
        solution=True, ref='2017 HL Q5(c)'),
    'engineering-2017-HL-scheme-q6aii-sol': dict(
        doc='scheme', page=18, rect=(92, 519, 536, 646), solution=True,
        ref='2017 HL Q6(a)(ii)'),
    'engineering-2017-HL-scheme-q6biii-sol': dict(
        doc='scheme', page=19, rect=(114, 420, 496, 510), solution=True,
        ref='2017 HL Q6(b)(iii)'),
    'engineering-2017-HL-scheme-q6c-sol': dict(
        doc='scheme', page=20, rect=(110, 106, 532, 262), solution=True,
        ref='2017 HL Q6(c)(ii)'),
    'engineering-2017-HL-scheme-q7ci-sol': dict(
        doc='scheme', page=21, rect=(204, 535, 595, 636), solution=True,
        ref='2017 HL Q7(c)(i)'),
    'engineering-2017-HL-scheme-q8ai-sol': dict(
        doc='scheme', page=22, rect=(414, 600, 584, 717), solution=True,
        ref='2017 HL Q8(a)(i)'),
    'engineering-2017-HL-scheme-q8ci-sol': dict(
        doc='scheme', page=23, rect=(90, 610, 522, 756), solution=True,
        ref='2017 HL Q8(c)(i)'),
    'engineering-2017-HL-scheme-q8cii-sol': dict(
        doc='scheme', page=24, rect=(105, 178, 508, 316), solution=True,
        ref='2017 HL Q8(c)(ii)'),
}

FOLDED = {
    'eng-2017-hl-q4-c-iii': NEW[:-1] + ' set "Body Centre Cubic (BCC) and Face Centre '
                            'Cubic (FCC) structures" apart from the other two pairs of '
                            '"Select any two from (i), (ii) or (iii)", with the tariff as '
                            'its answer; the choice is one card, at Q4(c)',
}

CARDS = [
    # ---- Question 1, Section A ("Any ten @ 5 marks each") ------------------
    dict(key=(1, 'a', None),
         why='Scheme p5 bullets three advantages; "(Any two) 3 + 2".',
         topic='eng-3-14',
         lifted=[S(5, 106, 243, 380, 259), S(5, 106, 260, 260, 276),
                 S(5, 106, 278, 275, 294)],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         notes="The scheme prints '(Any two) 3 + 2'."),
    dict(key=(1, 'b', None),
         why='Scheme p5 names the metals on one line; each is lifted by its own word '
             'rectangle. "(Any two) 3 + 2".',
         topic='eng-3-7',
         lifted=[S(5, 70, 325, 96, 341), S(5, 96, 325, 115, 341), S(5, 115, 325, 154, 341),
                 S(5, 154, 325, 210, 341), S(5, 210, 325, 237, 341),
                 S(5, 237, 325, 269, 341)],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         notes="The scheme prints '(Any two) 3 + 2'."),
    dict(key=(1, 'c', None),
         why='Scheme p5 lists the devices in one sentence; each is lifted by its own word '
             'rectangle. "(Any two) 3 + 2".',
         topic='eng-3-14',
         lifted=[S(5, 70, 369, 145, 385), S(5, 145, 369, 227, 385),
                 S(5, 227, 369, 370, 385),
                 join(S(5, 370, 369, 546, 385), S(5, 70, 385, 122, 401))],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         notes="The scheme prints '(Any two) 3 + 2'."),
    dict(key=(1, 'd', None),
         why='The EcoHelmet is photographed beside (d); scheme p5 lists the advantages in '
             'one sentence, each lifted by its own word rectangle. "(Any two) 3 + 2".',
         topic='eng-3-14',
         lifted=[S(5, 70, 432, 251, 448),
                 join(S(5, 251, 432, 537, 448), S(5, 70, 448, 110, 464)),
                 S(5, 110, 448, 170, 464), S(5, 170, 448, 262, 464)],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         question_figure='engineering-2017-HL-paper-q1d-art',
         notes="The scheme prints '(Any two) 3 + 2'."),
    dict(key=(1, 'e', None),
         why='Scheme p5 lists the reasons in one sentence; each is lifted by its own word '
             'rectangle. "(Any two) 3 + 2".',
         topic='eng-1-4',
         lifted=[S(5, 70, 495, 308, 511), S(5, 308, 495, 360, 511),
                 S(5, 360, 495, 394, 511), S(5, 394, 495, 507, 511)],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         notes="The scheme prints '(Any two) 3 + 2'."),
    dict(key=(1, 'f', None),
         why='Scheme p5 lists the methods in one sentence over three lines; each is '
             'lifted by its own word rectangle. "(Any two) 3 + 2".',
         topic='eng-2-13',
         lifted=[S(5, 70, 541, 377, 557), S(5, 377, 541, 531, 557),
                 S(5, 70, 555, 415, 571),
                 join(S(5, 415, 555, 536, 571), S(5, 70, 570, 224, 586)),
                 S(5, 224, 570, 405, 586)],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         notes="The scheme prints '(Any two) 3 + 2'."),
    dict(key=(1, 'g', None),
         why='A lead-in over three people set as romans, "any one"; scheme pp5-6 write a '
             'note on each under the name, "(Any one) 5".',
         topic='eng-3-14',
         lifted=[[join(S(5, 106, 614, 176, 630), S(5, 106, 629, 550, 674)),
                  join(S(5, 106, 687, 167, 703), S(5, 106, 702, 550, 762)),
                  join(S(6, 106, 72, 172, 88), S(6, 106, 87, 547, 118))]],
         row_kind='anyN', group=(1, 5), marks=[5], tariff='fixed', total=5,
         notes="The scheme prints '(Any one) 5'."),
    dict(key=(1, 'h', None),
         why='Scheme p6 gives three benefits, one a line; "(Any two) 3 + 2".',
         topic='eng-3-8',
         lifted=[join(S(6, 70, 146, 554, 162), S(6, 70, 162, 117, 178)),
                 S(6, 70, 179, 505, 195), S(6, 70, 196, 336, 212)],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         notes="The scheme prints '(Any two) 3 + 2'."),
    dict(key=(1, 'i', None),
         why='Scheme p6 names two advantages and two disadvantages, each lifted by its '
             'own word rectangle, over "3 + 2".',
         topic='eng-3-14',
         lifted=[[S(6, 133, 242, 230, 258), S(6, 230, 242, 392, 258)],
                 [S(6, 146, 257, 380, 273),
                  join(S(6, 380, 257, 529, 273), S(6, 70, 272, 102, 288))]],
         marks=[3, 2], total=5,
         notes="The scheme prints '3 + 2' under its advantages and disadvantages, in "
               "that order."),
    dict(key=(1, 'j', None),
         why='Scheme p6 answers in one paragraph, "5".',
         topic='eng-3-8',
         lifted=[S(6, 70, 316, 549, 348)], marks=[5], total=5,
         notes="The scheme prints '5'."),
    dict(key=(1, 'k', None),
         why='Scheme p6 sets the two gauges side by side, each drawn under its name with '
             'its use beneath, shown with the answer; "5" for the difference.',
         topic='eng-3-12',
         lifted=[join(S(6, 70, 379, 125, 395), S(6, 70, 466, 288, 482)),
                 join(S(6, 318, 379, 374, 395), S(6, 322, 466, 506, 482))],
         tariff='questionTotal', total=5,
         figure='engineering-2017-HL-scheme-q1k-sol',
         notes="The scheme prints '5'."),
    dict(key=(1, 'l', None),
         why='Scheme p6 answers in one paragraph, "5".',
         topic='eng-2-15',
         lifted=[S(6, 70, 510, 548, 556)], marks=[5], total=5,
         notes="The scheme prints '5'."),
    dict(key=(1, 'm', None),
         why='Scheme p6 answers in one paragraph, "5". The reader files the shaft\'s label, '
             'the page footer and the Section B heading printed after (m) as its stem, so '
             'the card carries none.',
         topic='eng-3-14', stem=False,
         lifted=[S(6, 70, 584, 555, 633)], marks=[5], total=5,
         notes="The scheme prints '5'."),
    # ---- Question 1, Section B ("Answer all of the following") -------------
    dict(key=(1, 'n', 'i'),
         why='Section B. Scheme p7 bullets five advantages; "6" for the part.',
         topic='eng-3-14', stem=False,
         lifted=[S(7, 118, 131, 286, 147), S(7, 118, 146, 209, 162),
                 S(7, 118, 162, 226, 178), S(7, 118, 177, 224, 193),
                 S(7, 118, 192, 477, 208)],
         tariff='questionTotal', total=6,
         notes="The scheme prints '6'."),
    dict(key=(1, 'n', 'ii'),
         why='Section B. Scheme p7 bullets seven applications; "2 + 2" for two.',
         topic='eng-3-14', stem=False,
         lifted=[[S(7, 118, 256, 261, 272), S(7, 118, 271, 223, 287),
                  S(7, 118, 286, 228, 302), S(7, 118, 302, 192, 318),
                  S(7, 118, 317, 534, 333), S(7, 118, 332, 284, 348),
                  S(7, 118, 347, 345, 363)]],
         row_kind='anyN', group=(2, 2), marks=[4], tariff='fixed', total=4,
         notes="The scheme prints '2 + 2'."),
    dict(key=(1, 'o', None),
         why='Section B. Scheme p7 answers in three paragraphs beside a photograph of a '
             'welding robot at a car body, shown with the answer; "10".',
         topic='eng-2-10', stem=False,
         lifted=[S(7, 70, 402, 558, 638)], marks=[10], total=10,
         figure='engineering-2017-HL-scheme-q1o-sol',
         notes="The scheme prints '10'."),
    dict(key=(1, 'p', 'i'),
         why='Section B. The arm is photographed with Part A arrowed; scheme p7 bullets two '
             'motors, either one, "2". The question is lifted with (p)\'s stimulus.',
         topic='eng-2-16', stem=False,
         question_lift=P(4, *_P1, more=[(118, 392, 333, 408)]),
         checked='paper page 4: "(i) Identify a type of motor suitable for Part A;" under '
                 '(p)\'s lead-in; the semicolon is the list running on',
         lifted=[[S(7, 118, 679, 183, 695), S(7, 118, 694, 194, 710)]],
         row_kind='anyN', group=(1, 2), marks=[2], tariff='fixed', total=2,
         question_figure='engineering-2017-HL-paper-q1pi-art',
         notes="The scheme prints '2'."),
    dict(key=(1, 'p', 'ii'),
         why='Section B. "This motor" is the one named in (i): scheme p8 bullets the '
             'features of a servo motor and of a stepper motor, each under its heading; '
             'either set answers the part, "6".',
         topic='eng-2-16', stem=False,
         question_lift=P(4, *_P1, more=[(118, 414, 324, 430)]),
         checked='paper page 4: "(ii) Describe the main features of this motor;" under '
                 '(p)\'s lead-in; the semicolon is the list running on',
         lifted=[[join(S(8, 100, 72, 256, 88), S(8, 118, 87, 546, 224)),
                  join(S(8, 100, 228, 270, 244), S(8, 118, 243, 401, 381))]],
         row_kind='anyN', group=(1, 6), marks=[6], tariff='fixed', total=6,
         question_figure='engineering-2017-HL-paper-q1pi-art',
         notes="The scheme prints '6'. 'This motor' is the one named in (p)(i); the "
               "scheme gives the features of a servo motor and of a stepper motor."),
    dict(key=(1, 'p', 'iii'),
         why='Section B. Scheme p8 answers in one line, "2".',
         topic='eng-2-16',
         lifted=[S(8, 100, 410, 390, 426)], marks=[2], total=2,
         notes="The scheme prints '2'."),
    dict(key=(1, 'q', None),
         why='Section B. A lead-in over three processes set as romans, "any one"; scheme '
             'p8 describes each under its heading, "(Any one) 10".',
         topic='eng-3-14', stem=False,
         lifted=[[join(S(8, 100, 468, 180, 484), S(8, 100, 483, 559, 558)),
                  join(S(8, 100, 571, 186, 587), S(8, 100, 586, 551, 645)),
                  join(S(8, 100, 659, 223, 675), S(8, 100, 673, 558, 733))]],
         row_kind='anyN', group=(1, 10), marks=[10], tariff='fixed', total=10,
         notes="The scheme prints '(Any one) 10'."),
    dict(key=(1, 'r', None),
         why='Section B. A lead-in over four terms set as romans, "any two"; scheme p9 '
             'describes each under its heading, "(Any two) 5 +5". The labels of the '
             'drawing beside (i) are left out of its answer.',
         topic='eng-3-14',
         lifted=[[join(S(9, 100, 102, 212, 118), S(9, 100, 116, 424, 191)),
                  join(S(9, 100, 234, 211, 250), S(9, 100, 248, 493, 416)),
                  join(S(9, 100, 446, 203, 462), S(9, 100, 461, 441, 491)),
                  join(S(9, 100, 519, 448, 535), S(9, 118, 536, 550, 746))]],
         row_kind='anyN', group=(2, 5), marks=[10], tariff='fixed', total=10,
         notes="The scheme prints '(Any two) 5 +5'."),
    # ---- Question 2 --------------------------------------------------------
    dict(key=(2, 'a', 'i'), topic='eng-3-8', stem=False,
         replaces=NEW + 'read the scheme\'s note on car impact tests as an answer row, '
                  'split both tests into unpriced lines and carried no drawing',
         why='Scheme p10 names either test and bullets each under its heading, beside a '
             'drawing of the Izod tester, shown with the answer; "8" for one. The '
             'question is lifted with (a)\'s stimulus.',
         question_lift=P(5, *_A2, more=[(118, 162, 370, 211)]),
         lifted=[[join(S(10, 100, 167, 153, 183), S(10, 140, 184, 349, 302)),
                  join(S(10, 100, 322, 168, 338), S(10, 140, 339, 396, 459))]],
         row_kind='anyN', group=(1, 8), marks=[8], tariff='fixed', total=8,
         figure='engineering-2017-HL-scheme-q2ai-sol',
         notes="The scheme prints '8' and 'Descriptions of car impact tests will be "
               "accepted.'"),
    dict(key=(2, 'a', 'ii'), replaces=OWNED,
         why='Scheme p10 describes each fracture under its heading beside a photograph of '
             'the broken specimens, labelled and shown with the answer; "8" for the part.',
         topic='eng-3-8',
         lifted=[join(S(10, 100, 504, 187, 520), S(10, 100, 520, 310, 570)),
                 join(S(10, 100, 588, 187, 604), S(10, 100, 605, 310, 654))],
         tariff='questionTotal', total=8,
         figure='engineering-2017-HL-scheme-q2aii-sol',
         notes="The scheme prints '8'."),
    dict(key=(2, 'b', 'i'),
         why='Scheme p11 answers with the plotted graph and prints no words; one ask row '
             'worth the part, with the scheme\'s graph shown. The question is lifted '
             'with (b)\'s stimulus and the table.',
         topic='eng-3-8', stem=False,
         question_lift=P(5, *_B2, more=[(118, 435, 440, 451)]),
         special={'kind': 'ask'}, total=10,
         question_figure='engineering-2017-HL-paper-q2b-crop',
         figure='engineering-2017-HL-scheme-q2b-sol',
         notes="The scheme prints '10' under its plotted graph."),
    dict(key=(2, 'b', 'ii'),
         why='Scheme p11 marks the three points on its graph, each labelled, "On graph 2 + '
             '2 + 2"; each label is lifted from the graph. The reader joined the results '
             'table to this part\'s question, so it is lifted from the page.',
         topic='eng-3-8', stem=False,
         question_lift=P(5, *_B2, more=[(118, 468, 336, 484), (118, 491, 213, 544)]),
         lifted=[S(11, 230, 209, 292, 225), S(11, 278, 104, 360, 120),
                 S(11, 459, 172, 532, 188)],
         marks=[2, 2, 2], total=6,
         question_figure='engineering-2017-HL-paper-q2b-crop',
         figure='engineering-2017-HL-scheme-q2b-sol',
         notes="The scheme prints 'On graph 2 + 2 + 2'."),
    dict(key=(2, 'b', 'iii'), topic='eng-3-8', stem=False,
         replaces=NEW + 'carried its mark "2" inside the answer and dropped the formula '
                  'line',
         why='Scheme p11 works the UTS in three lines, "2". The question is lifted with '
             '(b)\'s stimulus, which gives the specimen\'s diameter.',
         question_lift=P(5, *_B2, more=[(118, 562, 393, 578)]),
         lifted=[join(S(11, 100, 468, 230, 484), S(11, 275, 468, 367, 484),
                      S(11, 275, 483, 386, 499), S(11, 275, 497, 348, 513))],
         marks=[2], total=2,
         question_figure='engineering-2017-HL-paper-q2b-crop',
         notes="The scheme prints '2'."),
    dict(key=(2, 'c', 'i'),
         why='The device is photographed beside (c); scheme p11 describes X-ray testing '
             'in one paragraph beside a labelled drawing, shown with the answer; "8".',
         topic='eng-3-8',
         lifted=[join(S(11, 100, 541, 157, 557), S(11, 100, 570, 360, 733))],
         marks=[8], total=8,
         question_figure='engineering-2017-HL-paper-q2ci-art',
         figure='engineering-2017-HL-scheme-q2ci-sol',
         notes="The scheme prints '8'."),
    dict(key=(2, 'c', 'ii'),
         why='Scheme p12 bullets four precautions under a lead-in; "4 + 4" for two.',
         topic='eng-3-8',
         lifted=[[S(12, 143, 106, 492, 122), S(12, 143, 124, 542, 140),
                  S(12, 143, 141, 449, 157), S(12, 143, 159, 558, 192)]],
         row_kind='anyN', group=(2, 4), marks=[8], tariff='fixed', total=8,
         question_figure='engineering-2017-HL-paper-q2ci-art',
         notes="The scheme prints '4 + 4'."),
    # ---- Question 3 --------------------------------------------------------
    dict(key=(3, 'b', 'i'),
         why='The diagram is printed under (b) with its regions lettered; scheme p12 names '
             'each region after its letter, one a line, "1 + 1 + 1 + 1". The question is '
             'lifted with (b)\'s stimulus.',
         topic='eng-1-4', stem=False,
         question_lift=P(6, *_B3, more=[(118, 539, 323, 557)]),
         lifted=[S(12, 100, 599, 155, 615), S(12, 100, 613, 172, 629),
                 S(12, 100, 628, 218, 644), S(12, 100, 643, 247, 659)],
         marks=[1, 1, 1, 1], total=4,
         labels={'A': S(12, 122, 599, 155, 615), 'B': S(12, 122, 613, 172, 629),
                 'C': S(12, 122, 628, 218, 644), 'D': S(12, 122, 643, 247, 659)},
         question_figure='engineering-2017-HL-paper-q3b-crop',
         notes="The scheme prints '1 + 1 + 1 + 1'."),
    dict(key=(3, 'b', 'ii'), topic='eng-1-4', stem=False,
         replaces=NEW + 'carried the mark "4" inside its first answer and no picture of '
                  'the diagram',
         why='Scheme p12 names the point beside its mark and describes it on the next '
             'line, "4 + 4". The question is lifted with (b)\'s stimulus.',
         question_lift=P(6, *_B3, more=[(118, 564, 352, 581)]),
         lifted=[S(12, 100, 687, 178, 703), S(12, 100, 712, 541, 728)],
         marks=[4, 4], total=8,
         question_figure='engineering-2017-HL-paper-q3b-crop',
         notes="The scheme prints '4 + 4'."),
    dict(key=(3, 'c', 'i'), topic='eng-2-6',
         replaces=NEW + 'carried no picture of the gear wheels it asks about',
         why='The gearbox is photographed beside (c); scheme p13 gives three reasons, '
             '"4 + 4" for two.',
         lifted=[[S(13, 105, 234, 535, 267), S(13, 105, 268, 541, 301),
                  S(13, 105, 302, 320, 318)]],
         row_kind='anyN', group=(2, 4), marks=[8], tariff='fixed', total=8,
         question_figure='engineering-2017-HL-paper-q3c-crop',
         notes="The scheme prints '4 + 4'."),
    dict(key=(3, 'c', 'ii'), topic='eng-2-6',
         replaces=NEW + 'gave the process without its name, "Pack Method Carburising", '
                  'and without the drawing of the sealed container',
         why='Scheme p13 names pack carburising and describes it under a labelled '
             'drawing, shown with the answer; "8" for the part.',
         lifted=[join(S(13, 100, 350, 234, 366), S(13, 100, 518, 537, 551)),
                 S(13, 100, 552, 554, 568), S(13, 100, 569, 318, 585),
                 S(13, 100, 586, 544, 619)],
         tariff='questionTotal', total=8,
         question_figure='engineering-2017-HL-paper-q3c-crop',
         figure='engineering-2017-HL-scheme-q3cii-sol',
         notes="The scheme prints '8'."),
    # ---- Question 4 --------------------------------------------------------
    dict(key=(4, 'a', 'ii'),
         why='The spring is photographed beside (a); scheme p14 bullets five benefits '
             'under a lead-in, "4 + 4" for two.',
         topic='eng-2-6',
         lifted=[[S(14, 140, 234, 214, 250), S(14, 140, 249, 248, 265),
                  S(14, 140, 264, 187, 280), S(14, 140, 279, 209, 295),
                  S(14, 140, 295, 198, 311)]],
         row_kind='anyN', group=(2, 4), marks=[8], tariff='fixed', total=8,
         question_figure='engineering-2017-HL-paper-q4a-crop',
         notes="The scheme prints '4 + 4'."),
    dict(key=(4, 'b', 'i'),
         why='Scheme p14 answers with the drawn diagram, its liquidus and solidus lines '
             'labelled, and prints no words: "Draw the thermal equilibrium diagram: 8" '
             'and "Label: 1 + 1". One ask row worth the part, with the scheme\'s diagram '
             'shown. The question is lifted with (b)\'s stimulus and the table.',
         topic='eng-1-3', stem=False,
         question_lift=P(7, *_B4, more=[_GRAPH4, (118, 445, 506, 478)]),
         special={'kind': 'ask'}, total=10,
         question_figure='engineering-2017-HL-paper-q4b-crop',
         figure='engineering-2017-HL-scheme-q4b-sol',
         notes="The scheme prints 'Draw the thermal equilibrium diagram: 8' and 'Label: 1 "
               "+ 1'."),
    dict(key=(4, 'b', 'iii'),
         why='Scheme p14 gives the composition at the points A and C of its diagram, one a '
             'line, shown with the answer; "4" for the part.',
         topic='eng-1-3',
         lifted=[S(14, 140, 730, 388, 746), S(14, 140, 747, 388, 763)],
         tariff='questionTotal', total=4,
         question_figure='engineering-2017-HL-paper-q4b-crop',
         figure='engineering-2017-HL-scheme-q4b-sol',
         notes="The scheme prints '4'."),
    dict(key=(4, 'c', None), topic='eng-1-3',
         replaces=NEW + 'split (ii)\'s two lines into separate options, left (iii) out and '
                  'read the tariff "(Any two) 8 + 8" as an option',
         why='"Select any two from (i), (ii) or (iii)": scheme p15 answers each pair under '
             'its roman, (i) and (iii) beneath drawings of both structures, shown with the '
             'answer; each option is the pair, "(Any two) 8 + 8".',
         lifted=[[S(15, 96, 185, 536, 201), S(15, 100, 217, 524, 262),
                  join(S(15, 96, 309, 191, 355), S(15, 414, 309, 534, 340))]],
         row_kind='anyN', group=(2, 8), marks=[16], tariff='fixed', total=16,
         figure='engineering-2017-HL-scheme-q4c-sol',
         notes="The scheme prints '(Any two) 8 + 8'."),
    # ---- Question 5 --------------------------------------------------------
    dict(key=(5, 'a', 'i'),
         why='The pipe is photographed beside (a); scheme p15 names the process and '
             'justifies it in one sentence, "2 + 6": the name and the reason are lifted '
             'by their own word rectangles.',
         topic='eng-2-10',
         lifted=[S(15, 100, 490, 257, 506),
                 join(S(15, 257, 490, 544, 506), S(15, 100, 505, 400, 521))],
         marks=[2, 6], total=8,
         question_figure='engineering-2017-HL-paper-q5ai-art',
         notes="The scheme prints '2 + 6'."),
    dict(key=(5, 'a', 'ii'), topic='eng-2-10',
         replaces=NEW + 'gave the process without the drawing the part asks for',
         why='Scheme p15 describes submerged arc welding and its applications beside a '
             'labelled drawing, shown with the answer; "8" for the part.',
         lifted=[S(15, 100, 550, 356, 712), S(15, 100, 711, 356, 756)],
         tariff='questionTotal', total=8,
         question_figure='engineering-2017-HL-paper-q5ai-art',
         figure='engineering-2017-HL-scheme-q5aii-sol',
         notes="The scheme prints '8'."),
    dict(key=(5, 'b', 'v'), topic='eng-2-10',
         replaces=NEW + 'read the tariff "(Any three) 6 + 6 + 6" as an answer row',
         why='Scheme p16 bullets five benefits; "(Any three) 6 + 6 + 6", 6 for the part.',
         lifted=[S(16, 118, 632, 231, 648), S(16, 118, 649, 224, 665),
                 S(16, 118, 667, 213, 683), S(16, 118, 684, 288, 700),
                 S(16, 118, 702, 188, 718)],
         tariff='questionTotal', total=6,
         notes="The scheme prints '(Any three) 6 + 6 + 6'."),
    dict(key=(5, 'c', None), topic='eng-2-10', stem=False,
         replaces=NEW + 'carried both OR branches as one question total, every answer of '
                  'both an unpriced row',
         why='Paper p8 sets two alternative (c)s either side of an OR. This card is the '
             'first branch, "any one of the following", (i) and (ii); scheme p17 answers '
             'each beside its drawings (the circuit, the MIG and the TIG set-ups), shown '
             'with the answer, "(Any one) 16".',
         question_lift=P(8, *_C5A, more=[(90, 531, 449, 549), (90, 560, 466, 593)]),
         lifted=[[join(S(17, 100, 72, 440, 88), S(17, 100, 207, 552, 341)),
                  join(S(17, 100, 376, 176, 392), S(17, 100, 392, 424, 661))]],
         row_kind='anyN', group=(1, 16), marks=[16], tariff='fixed', total=16,
         figure='engineering-2017-HL-scheme-q5c-sol',
         notes="The scheme prints '(Any one) 16'. " + _OR5),
    dict(key=(5, 'c', 'i'), topic='eng-3-14', stem=False,
         replaces=NEW + 'mixed the welding branch\'s transformer-rectifier answer in with '
                  'the vacuum cleaner\'s advantages and disadvantages',
         why='The robotic vacuum cleaner branch\'s (i), lifted with its cue; scheme p18 '
             'bullets four advantages and two disadvantages under their headings, '
             '"4 + 4".',
         question_lift=P(8, *_C5B, more=[(118, 691, 358, 725)]),
         lifted=[[S(18, 118, 87, 517, 118), S(18, 118, 117, 494, 133),
                  S(18, 118, 132, 283, 148), S(18, 118, 148, 431, 164)],
                 [S(18, 118, 197, 534, 213), S(18, 118, 214, 535, 230)]],
         marks=[4, 4], total=8,
         notes="The scheme prints '4 + 4'. " + _OR5),
    dict(key=(5, 'c', 'ii'),
         why='The robotic vacuum cleaner branch\'s (ii), lifted with its cue; scheme p18 '
             'answers in one paragraph, "8".',
         topic='eng-3-14', stem=False,
         question_lift=P(8, *_C5B, more=[(118, 741, 340, 776)]),
         lifted=[S(18, 100, 259, 552, 348)], marks=[8], total=8,
         notes="The scheme prints '8'. " + _OR5),
    # ---- Question 6 --------------------------------------------------------
    dict(key=(6, 'a', 'i'), topic='eng-1-9',
         replaces=NEW + 'repeated the tubes\' answer inside the joints\' row',
         why='The tent is photographed with its tube and joint labelled; scheme p18 names '
             'a process for each on its own line, "2 + 2".',
         lifted=[S(18, 100, 447, 264, 463), S(18, 100, 461, 309, 477)],
         marks=[2, 2], total=4,
         question_figure='engineering-2017-HL-paper-q6a-crop',
         notes="The scheme prints '2 + 2'."),
    dict(key=(6, 'a', 'ii'),
         why='Scheme p18 names extrusion and describes it under a labelled drawing, shown '
             'with the answer; "10".',
         topic='eng-1-9',
         lifted=[join(S(18, 100, 505, 156, 521), S(18, 100, 652, 559, 726))],
         marks=[10], total=10,
         question_figure='engineering-2017-HL-paper-q6a-crop',
         figure='engineering-2017-HL-scheme-q6aii-sol',
         notes="The scheme prints '10'."),
    dict(key=(6, 'a', 'iii'),
         why='Scheme p18 names nylon and three reasons in one sentence, "2 + 2": the '
             'material is lifted by its own word rectangle, and each reason by its own, '
             'any one.',
         topic='eng-1-9',
         lifted=[S(18, 100, 740, 138, 756),
                 [S(18, 148, 740, 185, 756), S(18, 185, 740, 268, 756),
                  S(18, 289, 740, 346, 756)]],
         marks=[2, 2], total=4,
         question_figure='engineering-2017-HL-paper-q6a-crop',
         notes="The scheme prints 'Nylon is strong, difficult to break and lightweight' "
               "and '2 + 2'."),
    dict(key=(6, 'b', 'iii'), topic='eng-1-9',
         replaces=NEW + 'gave the polymerisation without the three monomers the scheme '
                  'draws beneath it',
         why='Scheme p19 explains addition polymerisation in two paragraphs over drawings '
             'of the three monomers, shown with the answer; "4".',
         lifted=[S(19, 100, 276, 551, 375), S(19, 100, 377, 551, 410)],
         tariff='questionTotal', total=4,
         figure='engineering-2017-HL-scheme-q6biii-sol',
         notes="The scheme prints '4'."),
    dict(key=(6, 'c', None), topic='eng-1-9',
         replaces=NEW + 'split compression moulding into two options and read the tariff '
                  '"(Any three) 6 + 6 + 6" as a sixth',
         why='A lead-in over five terms set as romans; scheme pp19-20 describe each under '
             'its roman, pultrusion beside a labelled drawing, shown with the answer; '
             '"(Any three) 6 + 6 + 6".',
         lifted=[[join(S(19, 100, 533, 169, 549), S(19, 100, 548, 547, 597)),
                  join(S(19, 100, 615, 199, 631), S(19, 100, 630, 553, 748),
                       S(20, 100, 72, 554, 103)),
                  S(20, 100, 277, 524, 308), S(20, 100, 321, 503, 352),
                  S(20, 100, 365, 556, 455)]],
         row_kind='anyN', group=(3, 6), marks=[18], tariff='fixed', total=18,
         figure='engineering-2017-HL-scheme-q6c-sol',
         notes="The scheme prints '(Any three) 6 + 6 + 6'."),
    # ---- Question 7 --------------------------------------------------------
    dict(key=(7, 'a', 'v'), topic='eng-2-11',
         replaces=NEW + 'read the tariff "(Any three) 6 + 6 + 6" as an answer row',
         why='Scheme p21 answers in one paragraph; "(Any three) 6 + 6 + 6".',
         lifted=[S(21, 100, 278, 551, 353)], marks=[6], total=6,
         notes="The scheme prints '(Any three) 6 + 6 + 6'."),
    dict(key=(7, 'b', 'i'), topic='eng-2-11',
         replaces=NEW + 'set the four fluids as one line under a question total',
         why='Scheme p21 names the fluids on one line, each lifted by its own word '
             'rectangle; "4 + 4" for two.',
         lifted=[[S(21, 100, 383, 167, 399), S(21, 167, 383, 204, 399),
                  S(21, 204, 383, 284, 399), S(21, 284, 383, 306, 399)]],
         row_kind='anyN', group=(2, 4), marks=[8], tariff='fixed', total=8,
         notes="The scheme prints '4 + 4'."),
    dict(key=(7, 'c', 'i'), topic='eng-2-11', stem=False,
         replaces=NEW + 'carried both OR branches as one question total with no route '
                  'between them',
         why='Both (c)s price their (i) at 8 (scheme pp21-22): the magnetic chuck in two '
             'paragraphs under a drawing, shown with the answer, or three reasons for '
             'stepper motors over one "8". One card for the printed OR, each branch a '
             'route.',
         question_lift=P(10, *_C7A, more=[(118, 511, 350, 544), _ORW7, _C7B,
                                          (118, 685, 356, 720)]),
         lifted=[join(S(21, 100, 532, 187, 548), S(21, 100, 649, 556, 767),
                      S(22, 100, 72, 553, 139)),
                 S(22, 100, 388, 412, 437)],
         marks=[8, 8], routes=['a', 'b'], total=8,
         question_figure='engineering-2017-HL-paper-q7c-crop',
         figure='engineering-2017-HL-scheme-q7ci-sol', notes=_OR7),
    dict(key=(7, 'c', 'ii'), topic='eng-2-11', stem=False,
         replaces=NEW + 'carried both OR branches as one "4 + 4" split across the '
                  'magnetic chuck\'s advantages and the CNC machines',
         why='Both (c)s price their (ii) at 4 + 4 (scheme p22): one of three advantages and '
             'one of two disadvantages of magnetic chucks, or two of three CNC machines '
             'named on one line, each lifted by its own word rectangle. One card, each '
             'branch a route.',
         question_lift=P(10, *_C7A, more=[(118, 550, 350, 583), _ORW7, _C7B,
                                          (118, 730, 340, 763)]),
         lifted=[[S(22, 140, 190, 364, 206), S(22, 140, 208, 403, 224),
                  S(22, 140, 225, 424, 241)],
                 [S(22, 140, 275, 305, 291), S(22, 140, 293, 548, 326)],
                 [S(22, 100, 470, 160, 486), S(22, 160, 470, 225, 486),
                  S(22, 225, 470, 288, 486)]],
         row_kind='anyN', group=[None, None, (2, 4)], marks=[4, 4, 8],
         routes=['a', 'a', 'b'], tariff='fixed', total=8,
         question_figure='engineering-2017-HL-paper-q7c-crop', notes=_OR7),
    # ---- Question 8 --------------------------------------------------------
    dict(key=(8, 'a', 'i'), topic='eng-2-15',
         replaces=NEW + 'gave the mechanism without the drawing the part asks for',
         why='Scheme p22 describes the ratchet and pawl beside a labelled drawing, shown '
             'with the answer, under "Suggested solutions - other viable solutions are '
             'acceptable."; "8".',
         lifted=[join(S(22, 100, 645, 370, 695), S(22, 100, 723, 450, 739))],
         marks=[8], total=8,
         figure='engineering-2017-HL-scheme-q8ai-sol',
         notes="The scheme prints '8' under 'Suggested solutions - other viable solutions "
               "are acceptable.'"),
    dict(key=(8, 'b', 'i'), topic='eng-2-15',
         replaces=NEW + 'set the two mechanisms as one question total, when either one '
                  'answers the part',
         why='Scheme p23 bullets two mechanisms, either one; "(Any three) 6 + 6 + 6".',
         lifted=[[S(23, 140, 179, 252, 195), S(23, 140, 197, 201, 213)]],
         row_kind='anyN', group=(1, 6), marks=[6], tariff='fixed', total=6,
         notes="The scheme prints '(Any three) 6 + 6 + 6'."),
    dict(key=(8, 'b', 'v'), topic='eng-2-16',
         replaces=NEW + 'read the tariff "(Any three) 6 + 6 + 6" as an answer row',
         why='Scheme p23 answers in one paragraph; "(Any three) 6 + 6 + 6".',
         lifted=[S(23, 100, 433, 417, 464)], marks=[6], total=6,
         notes="The scheme prints '(Any three) 6 + 6 + 6'."),
    dict(key=(8, 'c', 'i'), topic='eng-2-15', stem=False,
         why='Both (c)s price their (i) at 8 (scheme pp23-24): the toothed belt and pulley '
             'in one paragraph over a labelled photograph, shown with the answer, or the '
             'two terms IC and PCB, one a line, "4 + 4". One card for the printed OR, '
             'each branch a route.',
         question_lift=P(11, *_C8A, more=[(118, 463, 343, 515), _ORW8, _C8B,
                                          (118, 677, 268, 695)]),
         lifted=[S(23, 100, 540, 554, 590), S(24, 100, 452, 215, 468),
                 S(24, 100, 466, 241, 482)],
         marks=[8, 4, 4], routes=['a', 'b', 'b'], total=8,
         question_figure='engineering-2017-HL-paper-q8c-crop',
         figure='engineering-2017-HL-scheme-q8ci-sol', notes=_OR8 + ' ' + _SERVO),
    dict(key=(8, 'c', 'ii'), topic='eng-2-15', stem=False,
         why='Both (c)s price their (ii) at 8 (scheme p24): the worm and worm wheel in one '
             'paragraph over a photograph of the gears and the DPDT switch circuit, '
             'shown with the answer, or the soldering procedure under its safety, '
             'equipment and procedure headings, over one "8". One card, each branch a '
             'route.',
         question_lift=P(11, *_C8A, more=[(118, 531, 320, 582), _ORW8, _C8B,
                                          (118, 709, 402, 761)]),
         lifted=[S(24, 100, 72, 557, 173),
                 join(S(24, 100, 525, 542, 570), S(24, 140, 569, 550, 690))],
         marks=[8, 8], routes=['a', 'b'], total=8,
         question_figure='engineering-2017-HL-paper-q8c-crop',
         figure='engineering-2017-HL-scheme-q8cii-sol', notes=_OR8 + ' ' + _SERVO),
]

_ROB = 'Energy, Electronics & Robotics'

ATLAS = {
    'eng-2017-hl-q1-f': dict(
        topics=['Testing of Materials and Products'],
        note='Quality control during manufacture: checking and testing the product '
             '(dimensions, X-ray, mechanical and stress tests), which the reference files '
             'Q1 under; the card\'s syllabus heading is Manufacturing systems.'),
    'eng-2017-hl-q1-o': dict(
        topics=[_ROB],
        note='Robotic welding in car manufacture (Section B\'s robotics topic); the '
             'card\'s syllabus heading is Welding and joining, the method the scheme '
             'gives.'),
    'eng-2017-hl-q5-c-i': dict(
        topics=[_ROB],
        note='The robotic vacuum cleaner (the OR branch of Q5(c)); the card\'s syllabus '
             'heading is Technology, where the syllabus places robotics.'),
    'eng-2017-hl-q5-c-ii': dict(
        topics=[_ROB],
        note='The robotic vacuum cleaner (the OR branch of Q5(c)); the card\'s syllabus '
             'heading is Technology, where the syllabus places robotics.'),
}
