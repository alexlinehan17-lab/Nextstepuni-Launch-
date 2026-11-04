"""2024 Ordinary Level: the parts eng_all refuses or gets wrong, from the page.

Paper LC027GLP000EV; scheme pages as the PDF numbers them. Question 1 is
answered any eight at six marks each, "1 extra mark for each of the first two
correctly answered parts" (scheme p6).
"""
from eng_lift import join, lift

Y, L = 2024, 'ol'


def S(page, *rect):
    return lift(Y, L, 'scheme', page, rect)


def P(page, *rect, more=()):
    return lift(Y, L, 'paper', page, rect, more=more)


# Paper p7: the two (c)s either side of the OR, cue lines and romans.
_CA = (82, 424, 305, 440)            # "(c) A part for a centre lathe is shown opposite."
_CB = (82, 606, 340, 637)            # "(c) CNC Laser cutting is frequently used ..."
_OR6 = ('The paper sets two (c)s either side of an OR, the centre lathe part and '
        'CNC laser cutting; the scheme prices their (ii)s and (iii)s differently, '
        'so each branch is a card of its own.')
_OR3 = ('The paper sets this (d) as the alternative, after an OR, to "(d) Explain '
        'any two of the following metal properties".')
_OR7 = ('The paper sets this (c) as the alternative, after an OR, to "(c) Name any '
        'three of the instruments shown".')
# Paper p8: (c)'s OR branch cue, over the test circuit.
_C7 = (82, 605, 362, 621)
# Scheme pp12-13: each furnace's caption, under its diagram.
_BLAST, _CUPOLA, _EAF = (12, 110, 526, 190, 546), (12, 109, 725, 192, 745), (13, 107, 235, 210, 256)
_B7 = (82, 131, 430, 147)            # "(b) A waste pipe and plug are machined ..."
_B2 = (82, 136, 495, 152)            # "(b) Select one of the furnaces listed at Q2 (a) ..."

CROPS = {
    'engineering-2024-OL-paper-q1h-crop': dict(
        doc='paper', page=2, rect=(474, 331, 561, 431), ref='2024 OL Q1(h)'),
    # The coil spring; the ends of (b)'s own lines run into the box and are
    # whited out.
    'engineering-2024-OL-paper-q3b-crop': dict(
        doc='paper', page=4, rect=(385, 128, 556, 322), mask=[(383, 138, 418, 210)],
        ref='2024 OL Q3(b)'),
    'engineering-2024-OL-paper-q3di-crop': dict(
        doc='paper', page=4, rect=(48, 566, 180, 688), ref='2024 OL Q3(d)(i)'),
    'engineering-2024-OL-paper-q3dii-crop': dict(
        doc='paper', page=4, rect=(233, 566, 344, 685), ref='2024 OL Q3(d)(ii)'),
    'engineering-2024-OL-paper-q3diii-crop': dict(
        doc='paper', page=4, rect=(405, 563, 544, 682), ref='2024 OL Q3(d)(iii)'),
    'engineering-2024-OL-paper-q5a-crop': dict(
        doc='paper', page=6, rect=(78, 78, 535, 240), ref='2024 OL Q5(a)'),
    'engineering-2024-OL-paper-q6ci-crop': dict(
        doc='paper', page=7, rect=(378, 404, 558, 546), ref='2024 OL Q6(c)(i)'),
    'engineering-2024-OL-paper-q6cii-or-crop': dict(
        doc='paper', page=7, rect=(352, 606, 568, 753), ref='2024 OL Q6(c) OR'),
    'engineering-2024-OL-paper-q7c-crop': dict(
        doc='paper', page=8, rect=(60, 420, 545, 556), ref='2024 OL Q7(c)'),
    'engineering-2024-OL-paper-q7ci-crop': dict(
        doc='paper', page=8, rect=(370, 610, 580, 788), ref='2024 OL Q7(c)(i)',
        letters=('A', 'B', 'C')),
    # Scheme pp12-13: the three furnaces' labelled diagrams, side by side; the
    # romans of the list beside the cupola furnace are whited out.
    'engineering-2024-OL-scheme-q2bi-sol': dict(
        doc='scheme', page=12, parts=[(12, (75, 374, 217, 546)),
                                      (12, (76, 592, 233, 745)),
                                      (13, (74, 70, 231, 256))],
        mask=[(226, 586, 236, 608), (226, 689, 236, 710)],
        layout='row', solution=True, ref='2024 OL Q2(b)(i)'),
    # Scheme pp19-20: the three processes' labelled diagrams, stacked.
    'engineering-2024-OL-scheme-q5aii-sol': dict(
        doc='scheme', page=19, parts=[(19, (95, 289, 400, 446)),
                                      (19, (93, 538, 370, 682)),
                                      (20, (90, 82, 440, 217))],
        solution=True, ref='2024 OL Q5(a)(ii)'),
    # Scheme p25: the battery, toggle switch and LED symbols.
    'engineering-2024-OL-scheme-q7cii-sol': dict(
        doc='scheme', page=25, rect=(140, 576, 356, 753), solution=True,
        ref='2024 OL Q7(c)(ii)'),
}

CARDS = [
    dict(key=(1, 'h', None),
         why='"the type of chuck shown" is photographed and captioned beside (h); '
             'no crop had been cut. Scheme p8 answers the name and the use, '
             '"Award 3 Marks" each.',
         lifted=[S(8, 100, 84, 400, 104), S(8, 100, 100, 400, 134)],
         marks=[3, 3], total=6,
         question_figure='engineering-2024-OL-paper-q1h-crop'),
    dict(key=(1, 'k', None),
         replaces='the shipped card listed the scheme\'s photograph caption '
                  '"Autonomous vehicles for Digital Warehousing ." among the '
                  'answers',
         why='Scheme pp9-10 explain each of the three, "Any one explanation: Award '
             '6 Marks"; each explanation is lifted by its own rectangle.',
         topic='eng-3-14', concept='any-following-drone-technology-autonomous-vehicle',
         lifted=[S(9, 90, 435, 445, 543), S(10, 90, 84, 440, 177),
                 S(10, 90, 421, 446, 470)],
         tariff='questionTotal', total=6,
         notes="The scheme prints 'Any one explanation: Award 6 Marks'."),
    dict(key=(2, 'b', 'i'),
         question_lift=P(3, *_B2, more=[(110, 167, 356, 183)]), stem=False,
         why='Scheme pp12-13 answer "(i) Labelled diagram" with a labelled diagram '
             'of each furnace and no words; "Any one", "Award 6 Marks".',
         special={'kind': 'ask'}, total=6,
         figure='engineering-2024-OL-scheme-q2bi-sol',
         notes="The scheme prints '(i) Labelled diagram Award 6 Marks', for any "
               "one of the three furnaces."),
    dict(key=(2, 'b', 'ii'),
         question_lift=P(3, *_B2, more=[(110, 189, 298, 205)]), stem=False,
         why='Scheme pp12-13 list each furnace\'s charge beside its diagram; each '
             'list is lifted with the furnace\'s own caption. "Award 3 Marks".',
         lifted=[[join(S(*_BLAST), S(12, 322, 413, 400, 465)),
                  join(S(*_CUPOLA), S(12, 320, 600, 400, 680)),
                  join(S(*_EAF), S(13, 330, 107, 420, 157))]],
         marks=[3], total=3,
         notes="The scheme prints 'Award 3 Marks', for the furnace selected."),
    dict(key=(2, 'b', 'iii'),
         question_lift=P(3, *_B2, more=[(108, 209, 290, 227)]), stem=False,
         replaces='the shipped card accepted the diagram\'s caption "Cupola '
                  'furnace" as an answer to how the charge is heated',
         why='Each furnace\'s answer, lifted with its caption; "Award 3 Marks".',
         lifted=[[join(S(*_BLAST), S(12, 242, 488, 425, 508)),
                  join(S(*_CUPOLA), S(12, 244, 704, 425, 724)),
                  join(S(*_EAF), S(13, 250, 181, 425, 230))]],
         marks=[3], total=3,
         notes="The scheme prints 'Award 3 Marks', for the furnace selected."),
    dict(key=(2, 'c', 'i'),
         why='Scheme p13 answers the three labelled parts as three small tables, '
             'part, (i) material, (ii) reason; "(i) Material (Award 3 @ 3 Marks)".',
         lifted=[S(13, 74, 360, 400, 394), S(13, 74, 418, 400, 452),
                 S(13, 74, 477, 400, 511)],
         marks=[3, 3, 3], total=9,
         question_figure='engineering-2024-OL-paper-q2ci-art'),
    dict(key=(2, 'c', 'ii'),
         replaces='the shipped card\'s row was the heading "Frame", with "Reason: '
                  'Light, but strong Weighted plates" as its alternative',
         why='The same three tables; "(ii) Reason (Award 3 @ 2 Marks)". Each row '
             'carries the part and material the reason is for.',
         lifted=[S(13, 74, 360, 400, 409), S(13, 74, 418, 400, 467),
                 S(13, 74, 477, 400, 526)],
         marks=[2, 2, 2], total=6,
         question_figure='engineering-2024-OL-paper-q2ci-art'),
    dict(key=(3, 'a', None),
         replaces='the shipped "any two @ 7" offered seven options: normalising '
                  'split in two and carbon content in four, so one explanation '
                  'could be claimed twice',
         why='Scheme p15 explains each of the three, "(Award 2 @ 7 Marks)"; each '
             'explanation is lifted whole.',
         lifted=[[S(15, 97, 151, 435, 216), S(15, 97, 225, 435, 274),
                  S(15, 97, 283, 435, 408)]],
         row_kind='anyN', group=(2, 7), marks=[14], tariff='fixed', total=14,
         notes="The scheme prints 'Award 2 @ 7 Marks'."),
    dict(key=(3, 'b', None),
         why='"The coil spring shown" is photographed beside (b); scheme p15 '
             'describes each process, "(Award 2 @ 7 Marks)".',
         lifted=[[S(15, 97, 451, 435, 559), S(15, 97, 568, 435, 647),
                  S(15, 97, 656, 435, 764)]],
         topic='eng-2-6', question_lift=P(4, 82, 140, 416, 286),
         row_kind='anyN', group=(2, 7), marks=[14], tariff='fixed', total=14,
         question_figure='engineering-2024-OL-paper-q3b-crop',
         notes="The scheme prints 'Award 2 @ 7 Marks'."),
    dict(key=(3, 'd', None),
         why='Paper p4 sets two alternative (d)s either side of an OR. This card '
             'is the first branch, the three properties; scheme p16 explains '
             'each, "(Award 2 @ 6 Marks)".',
         topic='eng-3-8', question_lift=P(4, 82, 373, 540, 416),
         lifted=[[S(16, 97, 223, 440, 287), S(16, 97, 296, 440, 346),
                  S(16, 97, 355, 440, 419)]],
         row_kind='anyN', group=(2, 6), marks=[12], tariff='fixed', total=12,
         notes="The scheme prints 'Award 2 @ 6 Marks'. The paper sets this (d) "
               "and the robotics (d) beneath it either side of an OR."),
    *[dict(key=(3, 'd', r),
           why='The OR branch: "State one advantage for each of the robotic '
               'processes shown below:" over three photographs, captioned (i)-'
               '(iii); scheme p16, "Advantage (Award 3 @ 4 Marks)".',
           topic='eng-3-14',
           question_lift=P(4, 82, 519, 425, 535, more=[cap]),
           lifted=[S(16, 97, y0, 440, y1)], marks=[4], total=4,
           question_figure=f'engineering-2024-OL-paper-q3d{r}-crop', notes=_OR3)
      for r, cap, (y0, y1) in (
          ('i', (63, 710, 178, 726), (504, 553)),
          ('ii', (244, 710, 358, 726), (562, 626)),
          ('iii', (445, 710, 532, 726), (635, 700)))],
    dict(key=(5, 'a', 'i'),
         why='The three items are photographed and captioned on p6; scheme p19 '
             'names a process for each, "(Award 3 @ 3 Marks)".',
         lifted=[S(19, 112, 175, 300, 195), S(19, 112, 204, 300, 225),
                 S(19, 112, 233, 300, 254)],
         marks=[3, 3, 3], total=9,
         question_figure='engineering-2024-OL-paper-q5a-crop'),
    dict(key=(5, 'a', 'ii'),
         replaces='the shipped vacuum-forming answer began with the diagram\'s '
                  'callouts, "Final shape Mould Vacuum A vacuum former ...", and it '
                  'was filed under manufacturing processes, not plastics',
         why='Scheme pp19-20 describe each process under its heading beside a '
             'labelled diagram, "(ii) Description (Award 1 @ 11 Marks)"; heading '
             'and paragraph are lifted apart and joined, leaving the callouts '
             'out. The diagrams are shown with the answer.',
         topic='eng-1-9',
         lifted=[[join(S(19, 95, 289, 200, 310), S(19, 75, 450, 440, 514)),
                  join(S(19, 93, 538, 180, 558), S(19, 75, 682, 440, 760)),
                  join(S(20, 95, 82, 185, 102), S(20, 75, 218, 440, 370))]],
         marks=[11], total=11,
         question_figure='engineering-2024-OL-paper-q5a-crop',
         figure='engineering-2024-OL-scheme-q5aii-sol',
         notes="The scheme prints '(Award 1 @ 11 Marks)'."),
    dict(key=(6, 'a', None),
         replaces='the shipped card set the seven processes as one line under a '
                  'whole-question tariff, so naming one or two of them could not '
                  'be claimed; scheme p22 prices "Award 3 @ 5 Marks"',
         why='Each process lifted by its own rectangle from the scheme\'s one line; '
             'any three at five each.',
         lifted=[[S(22, 91, 149, 169, 169), S(22, 176, 149, 210, 169),
                  S(22, 217, 149, 261, 169), S(22, 268, 149, 305, 169),
                  S(22, 312, 149, 380, 169), S(22, 91, 163, 145, 183),
                  S(22, 152, 163, 225, 183)]],
         row_kind='anyN', group=(3, 5), marks=[15], tariff='fixed', total=15,
         question_figure='engineering-2024-OL-paper-q6a-art',
         notes="The scheme prints 'Award 3 @ 5 Marks'."),
    dict(key=(6, 'b', None),
         replaces='the shipped question read "(i) Rake angle, engineering component '
                  '(ii) Chuck key", the photograph\'s caption run in, and the '
                  'pilot-hole explanation was split into two options',
         why='The ask is lifted from its own lines on paper p7; scheme pp22-23 '
             'explain each term beside a picture, "(Award 3 @ 5 Marks)".',
         question_lift=P(7, 82, 248, 380, 382),
         concept='any-following-relation-machining-rake-angle',
         lifted=[[S(22, 97, 300, 320, 364), S(22, 97, 461, 275, 540),
                  S(22, 97, 622, 290, 686), S(23, 97, 69, 240, 177)]],
         row_kind='anyN', group=(3, 5), marks=[15], tariff='fixed', total=15,
         notes="The scheme prints 'Award 3 @ 5 Marks'."),
    dict(key=(6, 'c', 'i'),
         why='Both (c)s ask a (i) at "(Award 1 @ 6 Marks)" (scheme p23): the '
             'tailstock (the scheme numbers its line "(ii)") or what CNC stands '
             'for. One card for the printed OR, each branch a route of its own.',
         question_lift=P(7, *_CA, more=[(110, 454, 290, 470), (280, 559, 310, 577),
                                        _CB, (110, 650, 226, 666)]),
         lifted=[S(23, 105, 267, 160, 287), S(23, 105, 516, 285, 536)],
         marks=[6, 6], routes=['a', 'b'], total=6, stem=False,
         question_figure='engineering-2024-OL-paper-q6ci-crop',
         notes="The paper sets two (c)s either side of an OR; the scheme prints "
               "'Award 1 @ 6 Marks' for each (i)."),
    dict(key=(6, 'c', 'ii'),
         replaces='the shipped card answered the centre-lathe branch\'s "Identify '
                  'one use for this centre lathe part" with the CNC branch\'s two '
                  'advantages, one of them enough for all 6 marks',
         why='The centre-lathe branch\'s (ii), lifted with its cue; scheme p23 '
             '"(ii) Use (Award 1 @ 6 Marks)".',
         question_lift=P(7, *_CA, more=[(110, 483, 325, 499)]),
         lifted=[S(23, 105, 311, 372, 331)], marks=[6], total=6, stem=False,
         question_figure='engineering-2024-OL-paper-q6ci-crop', notes=_OR6),
    dict(key=(6, 'c', 'ii'), id='eng-2024-ol-q6-c-ii-or',
         ref_note='CNC laser cutting',
         why='The CNC branch\'s (ii), lifted with its cue; scheme p23 "(ii) Two '
             'advantages (Award 2 @ 4 Marks)".',
         question_lift=P(7, *_CB, more=[(110, 679, 348, 712)]),
         lifted=[S(23, 130, 575, 310, 594), S(23, 130, 590, 300, 609)],
         marks=[4, 4], total=8, stem=False,
         question_figure='engineering-2024-OL-paper-q6cii-or-crop', notes=_OR6),
    dict(key=(6, 'c', 'iii'),
         replaces='the shipped card offered the CNC branch\'s one precaution among '
                  'the centre-lathe branch\'s two, at 4 where that branch pays 6',
         why='The centre-lathe branch\'s (iii), lifted with its cue; scheme p23 '
             '"(iii) Safety precautions (Award 2 @ 4 Marks)".',
         question_lift=P(7, *_CA, more=[(110, 510, 365, 545)]),
         lifted=[S(23, 128, 370, 240, 389), S(23, 128, 386, 300, 404)],
         marks=[4, 4], total=8, stem=False,
         question_figure='engineering-2024-OL-paper-q6ci-crop', notes=_OR6),
    dict(key=(6, 'c', 'iii'), id='eng-2024-ol-q6-c-iii-or',
         ref_note='CNC laser cutting',
         why='The CNC branch\'s (iii), lifted with its cue; scheme p23 "(iii) '
             'Safety (Award 1 @ 6 Marks)".',
         question_lift=P(7, *_CB, more=[(110, 726, 345, 760)]),
         lifted=[S(23, 130, 650, 418, 670)], marks=[6], total=6, stem=False,
         question_figure='engineering-2024-OL-paper-q6cii-or-crop', notes=_OR6),
    dict(key=(7, 'a', 'i'),
         replaces='the shipped card set the three fits as one line under a '
                  'whole-question tariff, so naming one of them could not be '
                  'claimed; scheme p24 prices "(Award 2 @ 3 Marks)"',
         why='Each fit lifted by its own rectangle from the scheme\'s one line; '
             'any two at three each.',
         lifted=[[S(24, 98, 149, 150, 169), S(24, 157, 149, 220, 169),
                  S(24, 228, 149, 295, 169)]],
         row_kind='anyN', group=(2, 3), marks=[6], tariff='fixed', total=6,
         notes="The scheme prints 'Award 2 @ 3 Marks'."),
    dict(key=(7, 'b', None),
         replaces='the shipped question was only the sentence over the drawing, '
                  'with no "State the: (i) ... (iii)" asks, and its four rows, '
                  '(iv) among them, sat under one 20-mark total; (iv) has its own '
                  'card',
         why='The waste pipe and plug are drawn with their dimensions on p8; the '
             'card asks (i)-(iii), lifted with (b)\'s cue, and scheme p24 prices '
             'each "(Award 4 @ 5 Marks)".',
         topic='eng-3-12', stem=False,
         question_lift=P(8, *_B7, more=[(82, 277, 325, 293), (140, 297, 328, 315),
                                        (140, 319, 318, 337)]),
         lifted=[S(24, 96, 315, 412, 334), S(24, 96, 344, 412, 363),
                 S(24, 96, 374, 412, 393)],
         marks=[5, 5, 5], total=15,
         question_figure='engineering-2024-OL-paper-q7bi-art',
         notes="The scheme prints 'Award 4 @ 5 Marks' for (i)-(iv); (iv) is "
               "carded on its own."),
    dict(key=(7, 'b', 'iv'),
         replaces='the shipped row read "Type of fit; Interference fit", the '
                  'scheme\'s label welded to its answer',
         why='The question lifted with (b)\'s cue; scheme p24 answers in the right '
             'column, "Interference fit".',
         topic='eng-3-12', stem=False,
         question_lift=P(8, *_B7, more=[(82, 277, 140, 293), (156, 341, 522, 373)]),
         lifted=[S(24, 330, 403, 412, 423)], marks=[5], total=5,
         question_figure='engineering-2024-OL-paper-q7bi-art',
         notes="The scheme prints 'Award 4 @ 5 Marks' for (i)-(iv)."),
    dict(key=(7, 'c', None),
         why='The instruments branch of (c): four photographs captioned (i)-(iv); '
             'the question is lifted from its own line. Scheme pp24-25 price name '
             'and application apart, "Name Award 3 @ 3 Marks, Application Award 3 '
             '@ 3 Marks", so a name is claimed without its application; each '
             'application is shown with the instrument it is for.',
         topic='eng-3-12', question_lift=P(8, 82, 396, 556, 412),
         lifted=[[S(24, 75, 498, 185, 518), S(24, 75, 647, 185, 667),
                  S(25, 75, 69, 212, 89), S(25, 75, 216, 212, 236)],
                 [S(24, 75, 498, 440, 533), S(24, 75, 647, 440, 696),
                  S(25, 75, 69, 440, 180), S(25, 75, 216, 440, 282)]],
         row_kind='anyN', group=[(3, 3), (3, 3)], marks=[9, 9], tariff='fixed',
         total=18, question_figure='engineering-2024-OL-paper-q7c-crop',
         notes="The scheme prints 'Name Award 3 @ 3 Marks, Application Award 3 @ 3 "
               "Marks'."),
    dict(key=(7, 'c', 'i'),
         why='The OR branch\'s (i): the test circuit is photographed with A, B and '
             'C arrowed; scheme p25 names each, "(Award 3 @ 2 Marks)".',
         topic='eng-2-16',
         question_lift=P(8, *_C7, more=[(110, 632, 315, 665)]),
         lifted=[S(25, 133, 455, 230, 475), S(25, 133, 484, 230, 504),
                 S(25, 133, 513, 230, 534)],
         marks=[2, 2, 2], total=6, stem=False,
         figure='engineering-2024-OL-paper-q7ci-crop',
         labels={'A': S(25, 148, 455, 190, 475), 'B': S(25, 148, 484, 220, 504),
                 'C': S(25, 148, 513, 180, 534)},
         notes=_OR7),
    dict(key=(7, 'c', 'ii'),
         why='The OR branch\'s (ii): scheme p25 draws the three symbols under their '
             'names, "(ii) symbols (Award 3 @ 2 Marks)"; each name is the row its '
             'drawn symbol is claimed against.',
         topic='eng-2-16',
         question_lift=P(8, *_C7, more=[(110, 683, 328, 716)]),
         lifted=[S(25, 150, 587, 196, 607), S(25, 149, 660, 222, 680),
                 S(25, 150, 719, 186, 739)],
         row_kind='criterion', marks=[2, 2, 2], total=6, stem=False,
         question_figure='engineering-2024-OL-paper-q7ci-crop',
         figure='engineering-2024-OL-scheme-q7cii-sol', notes=_OR7),
]

TOPICS = {
    'eng-2024-ol-q4-d': ('eng-2-10', 'safety when soldering copper pipes is soldering, '
                         'joining; "copper" outvoted it'),
}

ATLAS = {
    **{f'eng-2024-ol-q2-c-{p}': dict(
        topics=['Materials: Properties and Uses'],
        note='Choosing a material for each part of the leg press machine, and why, '
             'which the reference files Q2(c) under; the card\'s syllabus heading is '
             'Technology.') for p in ('i', 'ii')},
    **{f'eng-2024-ol-q3-d-{p}': dict(
        topics=['Energy, Electronics & Robotics'],
        note='Robotic lawn mowing, waste sorting and welding (the OR branch of '
             'Q3(d)); the card\'s syllabus heading is Technology, where the '
             'syllabus places robotics.') for p in ('i', 'ii', 'iii')},
}
