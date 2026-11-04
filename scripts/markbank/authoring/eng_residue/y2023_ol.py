"""2023 Ordinary Level: the parts eng_all refuses or gets wrong, from the page.

Paper LC027GLP000EV; scheme pages as the PDF numbers them.
"""
from eng_lift import join, lift

Y, L = 2023, 'ol'


def S(page, *rect):
    return lift(Y, L, 'scheme', page, rect)


def P(page, *rect, more=()):
    return lift(Y, L, 'paper', page, rect, more=more)


_B_CUE = (80, 130, 480, 146)      # "(b) A copper fitting and a steel shaft are machined ..."
_STATE = (80, 288, 140, 304)      # "State the:"
_OR_D = ('The paper sets this (d) as the alternative, after an OR, to "(d) Explain '
         'any two of the following metal properties".')
_OR_C = ('The paper sets this (c) as the alternative, after an OR, to "(c) Name any '
         'three of the instruments shown".')

CROPS = {
    'engineering-2023-OL-paper-q1f-crop': dict(
        doc='paper', page=2, rect=(422, 250, 522, 312), ref='2023 OL Q1(f)',
        letters=('A',)),
    'engineering-2023-OL-paper-q2c-crop': dict(
        doc='paper', page=3, rect=(84, 334, 507, 615), ref='2023 OL Q2(c)'),
    # The exoskeleton photograph; the (d) branch's own lines run into the box
    # on the left and are whited out.
    'engineering-2023-OL-paper-q3dii-crop': dict(
        doc='paper', page=4, rect=(358, 590, 567, 744), mask=[(356, 606, 440, 676)],
        ref='2023 OL Q3(d)(ii)'),
    # Scheme pp20-21: the three processes' labelled diagrams, each under its
    # heading, stacked.
    'engineering-2023-OL-scheme-q5aii-sol': dict(
        doc='scheme', page=20, parts=[(20, (90, 294, 380, 436)),
                                      (20, (90, 543, 440, 676)),
                                      (21, (88, 144, 375, 298))],
        solution=True, ref='2023 OL Q5(a)(ii)'),
    'engineering-2023-OL-paper-q7b-crop': dict(
        doc='paper', page=8, rect=(100, 148, 485, 285), ref='2023 OL Q7(b)'),
    'engineering-2023-OL-paper-q7c-crop': dict(
        doc='paper', page=8, rect=(35, 415, 540, 560), ref='2023 OL Q7(c)'),
    'engineering-2023-OL-paper-q7ci-crop': dict(
        doc='paper', page=8, rect=(250, 619, 353, 689), ref='2023 OL Q7(c)(i)'),
    # The LED; the end of (ii)'s own line runs into the box and is whited out.
    'engineering-2023-OL-paper-q7cii-crop': dict(
        doc='paper', page=8, rect=(462, 615, 582, 742), mask=[(460, 686, 493, 704)],
        ref='2023 OL Q7(c)(ii)'),
    'engineering-2023-OL-paper-q7ciii-crop': dict(
        doc='paper', page=8, rect=(320, 731, 490, 786), ref='2023 OL Q7(c)(iii)'),
}

CARDS = [
    dict(key=(1, 'f', None),
         why='Tool A is the socket ratchet photographed and captioned on p2, which '
             'names no syllabus topic; tightening and loosening nuts is mechanical '
             'fastening, under Joining (as the 2021 Ordinary spanner is). Scheme p8 '
             'answers the name and the use in two bullets.',
         topic='eng-2-10',
         lifted=[S(8, 82, 72, 430, 88), S(8, 82, 87, 430, 118)],
         marks=[3, 3], total=6, figure='engineering-2023-OL-paper-q1f-crop',
         labels={'A': S(8, 150, 72, 216, 88)}),
    dict(key=(2, 'c', 'i'),
         why='Scheme p14 answers the three labelled parts as three small tables, '
             'part, (i) material, (ii) reason; the reader keeps one material. '
             '"Award 3 @ 3 Marks".',
         lifted=[S(14, 74, 93, 420, 125), S(14, 74, 162, 420, 192),
                 S(14, 74, 221, 420, 250)],
         marks=[3, 3, 3], total=9,
         question_figure='engineering-2023-OL-paper-q2c-crop'),
    dict(key=(2, 'c', 'ii'),
         replaces='the shipped card\'s "any three" options included the scheme\'s '
                  'bare part headings ("Back support:", "Chassis:") among the reasons, '
                  'and it showed no picture of the go-kart',
         why='The same three tables; "Award 3 @ 2 Marks". Each row carries the part '
             'and material the reason is for.',
         lifted=[S(14, 74, 93, 420, 149), S(14, 74, 162, 420, 207),
                 S(14, 74, 221, 420, 266)],
         marks=[2, 2, 2], total=6,
         question_figure='engineering-2023-OL-paper-q2c-crop'),
    dict(key=(3, 'd', None),
         why='Paper p4 sets two alternative (d)s either side of an OR (the '
             'automatic author withholds the letter for that reason). This card '
             'is the first branch, the three properties; scheme p16 explains '
             'each, "Award 2 @ 6 Marks".',
         topic='eng-3-8', question_lift=P(4, 82, 458, 560, 505),
         lifted=[[S(16, 75, 112, 440, 176), S(16, 75, 171, 440, 249),
                  S(16, 75, 244, 440, 278)]],
         row_kind='anyN', group=(2, 6), marks=[12], tariff='fixed', total=12,
         notes="The scheme prints 'Award 2 @ 6 Marks'. The paper sets this (d) "
               "and the robotics (d) beneath it either side of an OR."),
    dict(key=(3, 'd', 'i'),
         replaces='the shipped question read "Explain any two of the following '
                  'metal properties: Toughness, OR Describe two areas where robotic '
                  'technology is used in health care." with a toughness answer '
                  'among its rows',
         why='The OR branch\'s (i), lifted from its own line on paper p4; scheme '
             'p16 answers in two bullets beside photographs, "Award 2 @ 3 Marks".',
         topic='eng-3-14', question_lift=P(4, 100, 608, 440, 626),
         lifted=[S(16, 105, 411, 315, 516), S(16, 105, 574, 315, 693)],
         marks=[3, 3], total=6, notes=_OR_D),
    dict(key=(3, 'd', 'ii'),
         replaces='the shipped question read "Explain any two of the following '
                  'metal properties: Ductility, OR State two ways in which '
                  'exoskeleton suits can help the recovery process." with a '
                  'ductility answer among its rows',
         why='The OR branch\'s (ii), lifted from its two lines on paper p4; scheme '
             'p17 answers in two bullets, "Award 2 @ 3 Marks".',
         topic='eng-3-14', question_lift=P(4, 102, 642, 365, 674),
         lifted=[S(17, 110, 72, 320, 176), S(17, 110, 204, 320, 265)],
         marks=[3, 3], total=6,
         question_figure='engineering-2023-OL-paper-q3dii-crop', notes=_OR_D),
    dict(key=(5, 'a', 'ii'),
         replaces='the shipped vacuum-forming answer began mid-paragraph, at "This '
                  'causes the plastic sheet to pull against the mould": the page '
                  'break had cut off its first seven lines. It was filed under '
                  'manufacturing processes, not plastics',
         why='Scheme pp20-21 describe each of the three processes under its '
             'heading, beside a labelled diagram, "(ii) Describe (Award 1 @ 11 '
             'Marks)"; the vacuum-forming paragraph runs over the page break, so '
             'it is lifted in pieces and joined. The diagrams are shown with the '
             'answer.',
         topic='eng-1-9',
         lifted=[[S(20, 75, 294, 440, 515),
                  join(S(20, 90, 543, 190, 560), S(20, 75, 680, 440, 769),
                       S(21, 75, 57, 440, 117)),
                  S(21, 75, 145, 440, 366)]],
         marks=[11], total=11,
         question_figure='engineering-2023-OL-paper-q5ai-art',
         figure='engineering-2023-OL-scheme-q5aii-sol',
         notes="The scheme prints '(Award 1 @ 11 Marks)'."),
    dict(key=(6, 'c', 'i'),
         replaces='the shipped card offered "Knurling / Parting off." and the OR '
                  'branch\'s "CNC - Computer Numerical Control." as any two at 3 '
                  'each, so naming both lathe processes scored 3 of 6 and the CNC '
                  'answer 3 of its 6; it was filed under Joining',
         why='Scheme p24 prices the lathe branch "(i) Name (Award 2 @ 3 Marks)", '
             'the two processes printed on one line, and the OR branch "(i) CNC '
             '(Award 1 @ 6 Marks)". One card for the printed OR, each branch a '
             'route of its own.',
         topic='eng-2-11',
         lifted=[S(24, 90, 74, 135, 90), S(24, 142, 74, 200, 90),
                 S(24, 92, 576, 272, 592)],
         marks=[3, 3, 6], routes=['a', 'a', 'b'], total=6,
         notes="The paper sets two (c)s either side of an OR. The scheme prints "
               "'Award 2 @ 3 Marks' for the two lathe processes and 'Award 1 @ 6 "
               "Marks' for what CNC stands for."),
    *[dict(key=(7, 'b', r),
           **({'replaces': 'the shipped card asked for a dimension with no drawing of '
                           'the fitting and shaft, and filed it under non-ferrous '
                           'metals'} if r in ('i', 'iv') else {}),
           why='The copper fitting and steel shaft are drawn with their dimensions '
               'on p8; each roman\'s question is lifted with (b)\'s cue. Scheme p25, '
               '"Award 4 @ 5 Marks".',
           topic='eng-3-12', stem=False,
           question_lift=P(8, *_B_CUE, more=[_STATE, line] if r != 'i' else [line]),
           lifted=[S(25, 95, y0, 410, y1)], marks=[5], total=5,
           question_figure='engineering-2023-OL-paper-q7b-crop')
      for r, line, (y0, y1) in (
          ('i', (80, 288, 412, 304), (317, 333)),
          ('ii', (138, 307, 320, 325), (346, 362)),
          ('iii', (138, 328, 320, 345), (376, 392)),
          ('iv', (138, 348, 376, 366), (405, 421)))],
    dict(key=(7, 'c', None),
         why='The instruments branch of (c): four photographs captioned (i)-(iv); '
             'the reader runs the OR branch into its question, so the question is '
             'lifted from its own line. Scheme pp25-26 set name beside application '
             'in two columns and price them apart, "Name Award 3 @ 3 Marks, '
             'Application Award 3 @ 3 Marks", so a name is claimed without its '
             'application; each application is shown with the instrument it is '
             'for.',
         topic='eng-3-12', question_lift=P(8, 82, 400, 556, 416),
         lifted=[[S(25, 75, 573, 215, 589), S(25, 75, 661, 215, 677),
                  S(26, 75, 57, 215, 73), S(26, 75, 160, 215, 176)],
                 [S(25, 75, 573, 432, 648), S(25, 75, 661, 432, 750),
                  S(26, 75, 54, 420, 132), S(26, 75, 156, 420, 205)]],
         row_kind='anyN', group=[(3, 3), (3, 3)], marks=[9, 9], tariff='fixed',
         total=18,
         question_figure='engineering-2023-OL-paper-q7c-crop',
         notes="The scheme prints 'Name (Award 3 @ 3 Marks), Application (Award 3 @ "
               "3 Marks)'."),
    dict(key=(7, 'c', 'i'),
         why='The OR branch\'s (i); scheme p26 answers beside a photograph whose '
             'caption the reader welds in. "(i) Solenoid use Award 1 @ 6 Marks".',
         topic='eng-2-16', lifted=[S(26, 232, 356, 420, 445)], marks=[6], total=6,
         question_figure='engineering-2023-OL-paper-q7ci-crop', notes=_OR_C),
    dict(key=(7, 'c', 'ii'),
         why='The OR branch\'s (ii): the LED photographed with its long and short '
             'legs labelled; the reader runs the instruments branch into its '
             'question, so it is lifted from its own line. "(ii) Reason Award 1 @ '
             '6 Marks".',
         topic='eng-2-16', lifted=[S(26, 236, 517, 436, 607)], marks=[6], total=6,
         question_lift=P(8, 100, 686, 494, 704),
         question_figure='engineering-2023-OL-paper-q7cii-crop', notes=_OR_C),
    dict(key=(7, 'c', 'iii'),
         why='The OR branch\'s (iii): the resistor photographed with its colour '
             'bands labelled; the scheme gives the function and a worked example. '
             '"(iii) Function Award 1 @ 6 Marks".',
         topic='eng-2-16',
         lifted=[S(26, 240, 649, 430, 694), S(26, 82, 713, 330, 758)],
         tariff='questionTotal', total=6,
         question_figure='engineering-2023-OL-paper-q7ciii-crop',
         notes="The scheme prints 'Award 1 @ 6 Marks'. " + _OR_C),
]

TOPICS = {
    'eng-2023-ol-q6-c-ii': ('eng-2-11', 'describing knurling or parting off is lathe '
                            'work, machining; "manufacture" outvoted it'),
}

ATLAS = {
    **{f'eng-2023-ol-q2-c-{p}': dict(
        topics=['Materials: Properties and Uses'],
        note='Choosing a material for each part of the go-kart, and why, which the '
             'reference files Q2(c) under; the card\'s syllabus heading is '
             'Technology, the electric go-kart being the question\'s subject.')
       for p in ('i', 'ii')},
    **{f'eng-2023-ol-q3-d-{p}': dict(
        topics=['Energy, Electronics & Robotics'],
        note='Robotics in health care and exoskeleton suits (the OR branch of '
             'Q3(d)); the card\'s syllabus heading is Technology, where the '
             'syllabus places robotics.') for p in ('i', 'ii')},
}
