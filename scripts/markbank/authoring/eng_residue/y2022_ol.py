"""2022 Ordinary Level: the parts eng_all refuses or gets wrong, from the page.

Paper LC027GLP000EV; scheme pages as the PDF numbers them. Question 1 is
answered any eight at six marks each (eng_scheme per_part).
"""
from eng_lift import join, lift

Y, L = 2022, 'ol'


def S(page, *rect):
    return lift(Y, L, 'scheme', page, rect)


def P(page, *rect, more=()):
    return lift(Y, L, 'paper', page, rect, more=more)


_B_CUE = (75, 230, 410, 286)          # "(b) A hole and shaft are machined to the dimensions shown below."
_STATE = (76, 288, 135, 302)          # "State the:"

CROPS = {
    'engineering-2022-OL-paper-q1d-crop': dict(
        doc='paper', page=2, rect=(410, 132, 556, 240), ref='2022 OL Q1(d)',
        letters=('A', 'B', 'C')),
    'engineering-2022-OL-paper-q1i-crop': dict(
        doc='paper', page=2, rect=(68, 372, 566, 530), ref='2022 OL Q1(i)'),
    'engineering-2022-OL-paper-q2c-crop': dict(
        doc='paper', page=3, rect=(76, 258, 506, 608), ref='2022 OL Q2(c)'),
    'engineering-2022-OL-paper-q3c-crop': dict(
        doc='paper', page=4, rect=(355, 316, 547, 449), ref='2022 OL Q3(c)'),
    'engineering-2022-OL-paper-q4ai-crop': dict(
        doc='paper', page=5, rect=(130, 76, 404, 172), ref='2022 OL Q4(a)(i)',
        letters=('A', 'B')),
    'engineering-2022-OL-paper-q4ci-crop': dict(
        doc='paper', page=5, rect=(405, 476, 557, 584), ref='2022 OL Q4(c)(i)',
        letters=('A',)),
    'engineering-2022-OL-paper-q6a-crop': dict(
        doc='paper', page=7, rect=(130, 74, 425, 320), ref='2022 OL Q6(a)',
        letters=('A', 'B', 'C', 'D')),
    'engineering-2022-OL-paper-q6c-crop': dict(
        doc='paper', page=7, rect=(350, 413, 529, 565), ref='2022 OL Q6(c)'),
    'engineering-2022-OL-paper-q7a-crop': dict(
        doc='paper', page=8, rect=(46, 82, 562, 228), ref='2022 OL Q7(a)',
        letters=('A', 'B')),
    'engineering-2022-OL-paper-q7b-crop': dict(
        doc='paper', page=8, rect=(318, 274, 572, 422), mask=[(316, 285, 334, 382)],
        ref='2022 OL Q7(b)'),
    # Scheme pp12-14: each furnace's labelled diagram over its name, the four a
    # candidate may choose from.
    'engineering-2022-OL-scheme-q2b-sol': dict(
        doc='scheme', parts=[(12, (66, 515, 240, 706)), (13, (60, 132, 260, 353)),
                             (13, (68, 480, 265, 728)), (14, (48, 104, 262, 322))],
        layout='row', solution=True, ref='2022 OL Q2(b)'),
}

CARDS = [
    dict(key=(1, 'd', None),
         why='The gear train is drawn beside (d) with A, B, C and the caption '
             '"idler gear"; no crop had been cut. Scheme p7 answers in one line.',
         use=[0], marks=[6], total=6, figure='engineering-2022-OL-paper-q1d-crop',
         labels={'B': S(7, 119, 409, 170, 425)}),
    dict(key=(1, 'i', None),
         why='The ask is one line and the three choices are the captions under '
             'their photographs; the reader puts (d)\'s caption "idler gear" '
             'between them. Scheme pp8-9 describe each beside a diagram whose '
             'callouts the reader welds into the text, so each description is '
             'lifted by rectangle. "Describe 6 Marks".',
         topic='eng-2-11',
         question_lift=P(2, 62, 348, 390, 364, more=[(95, 513, 520, 529)]),
         lifted=[S(8, 70, 125, 456, 262), S(8, 70, 443, 456, 550),
                 S(9, 70, 92, 456, 199)],
         tariff='questionTotal', total=6,
         question_figure='engineering-2022-OL-paper-q1i-crop',
         notes="The scheme prints 'Describe 6 Marks'."),
    dict(key=(2, 'c', 'i'),
         why='Scheme p14 sets the three labelled parts as a table, each with a '
             'material (i) and a reason (ii); the reader keeps only the roll '
             'cage. "Material Award 3 @ 3 Marks".',
         lifted=[S(14, 80, 397, 312, 415), S(14, 80, 444, 312, 461),
                 S(14, 80, 488, 312, 506)],
         marks=[3, 3, 3], total=9,
         question_figure='engineering-2022-OL-paper-q2c-crop'),
    dict(key=(2, 'c', 'ii'),
         why='The same table; "Reason Award 3 @ 2 Marks". Each row carries the '
             'part and material the reason is for.',
         lifted=[S(14, 80, 397, 312, 431), S(14, 80, 444, 312, 479),
                 S(14, 80, 488, 312, 523)],
         marks=[2, 2, 2], total=6,
         question_figure='engineering-2022-OL-paper-q2c-crop'),
    dict(key=(3, 'c', None),
         why='"the hand-held angle grinder shown in the picture" is photographed '
             'beside (c); "PPE items Award 2 @ 5 Marks".',
         use=[[1, 2]], row_kind='anyN', group=(2, 5), marks=[10], tariff='fixed',
         total=10, question_figure='engineering-2022-OL-paper-q3c-crop',
         notes="The scheme prints 'Award 2 @ 5 Marks'."),
    dict(key=(3, 'd', None),
         replaces='the shipped question read "Explain any two of the following '
                  'metal properties: OR Give one example of the use of robotics in '
                  'any two of the following:" with both branches\' answers mixed '
                  'among its options',
         why='Paper p4 sets two alternative (d)s either side of an OR, and the '
             'reader files both under one key. This card is the first branch, '
             'the four properties; scheme p16 explains each, "Award 2 @ 6 Marks".',
         topic='eng-3-8', question_lift=P(4, 80, 479, 560, 519),
         lifted=[[S(16, 68, 361, 452, 407), S(16, 68, 418, 452, 464),
                  S(16, 68, 475, 452, 536), S(16, 68, 547, 452, 593)]],
         row_kind='anyN', group=(2, 6), marks=[12], tariff='fixed', total=12,
         notes="The scheme prints 'Award 2 @ 6 Marks'. The paper sets this (d) "
               "and the robotics (d) beneath it either side of an OR."),
    dict(key=(3, 'd', 'i'),
         replaces='the shipped question read "Brittleness, OR medicine; (ii) '
                  'gardening; (iii) manufacturing." under a cue naming both '
                  'branches, with a brittleness answer among its rows',
         why='The OR branch: "Give one example of the use of robotics in any two '
             'of the following:" over (i) medicine, (ii) gardening, (iii) '
             'manufacturing, carded per roman as the subject cards "any two of '
             'the following"; scheme p16, "Example Award 2 @ 6 Marks".',
         topic='eng-3-14',
         question_lift=P(4, 83, 578, 340, 612, more=[(83, 618, 200, 636)]),
         lifted=[S(16, 68, 663, 380, 683)], marks=[6], total=6,
         notes='The paper sets this (d) as the alternative, after an OR, to "(d) '
               'Explain any two of the following metal properties".'),
    dict(key=(3, 'd', 'ii'),
         why='The OR branch\'s (ii); see (d)(i).', topic='eng-3-14',
         question_lift=P(4, 83, 578, 340, 612, more=[(83, 653, 200, 671)]),
         lifted=[S(16, 68, 692, 300, 712)], marks=[6], total=6,
         notes='The paper sets this (d) as the alternative, after an OR, to "(d) '
               'Explain any two of the following metal properties".'),
    dict(key=(3, 'd', 'iii'),
         why='The OR branch\'s (iii); see (d)(i).', topic='eng-3-14',
         question_lift=P(4, 83, 578, 340, 612, more=[(83, 688, 220, 706)]),
         lifted=[S(16, 68, 722, 300, 742)], marks=[6], total=6,
         notes='The paper sets this (d) as the alternative, after an OR, to "(d) '
               'Explain any two of the following metal properties".'),
    dict(key=(4, 'a', 'i'),
         why='The torch is photographed with A and B arrowed; scheme p17 answers '
             'part A beside a copy of the photograph whose letters the reader '
             'welds into the line. "One part @ 3 marks; One part @ 2 marks".',
         lifted=[S(17, 77, 217, 445, 281), S(17, 77, 290, 445, 340)],
         marks=[3, 2], total=5, figure='engineering-2022-OL-paper-q4ai-crop',
         labels={'A': S(17, 140, 217, 218, 236), 'B': S(17, 129, 290, 157, 309)}),
    dict(key=(4, 'c', 'i'),
         why='Tool A is the G-clamp photographed and captioned on p5; priced by '
             '(c)\'s "Three parts @ 5 marks".',
         topic='eng-2-10',
         use=[0], marks=[5], total=5, figure='engineering-2022-OL-paper-q4ci-crop',
         labels={'A': S(18, 124, 215, 262, 234)}),
    dict(key=(6, 'a', None),
         why='The lathe\'s four parts are lettered A-D around the photograph and '
             'the automatic crop dropped the letters (eng_figures REJECTED). '
             'Scheme p22 names each on its own line; "One part @ 7 marks; Two '
             'parts @ 5 marks (17)".',
         lifted=[S(22, 75, 117, 210, 136), S(22, 75, 132, 210, 151),
                 S(22, 75, 146, 210, 165), S(22, 75, 161, 210, 180)],
         tariff='orderedSplit',
         notation='One part @ 7 marks; Two parts @ 5 marks (17)', ladder=17,
         figure='engineering-2022-OL-paper-q6a-crop',
         labels={'A': S(22, 105, 117, 200, 136), 'B': S(22, 104, 132, 140, 151),
                 'C': S(22, 104, 146, 155, 165), 'D': S(22, 104, 161, 155, 180)}),
    dict(key=(6, 'c', 'i'),
         why='"the lathe process shown" is the parting-off photograph beside '
             '(c); the automatic crop took it with the OR branch\'s laser-cut '
             'parts (eng_figures REJECTED).',
         use=[0], marks=[5], total=5,
         question_figure='engineering-2022-OL-paper-q6c-crop'),
    dict(key=(6, 'c', 'ii'),
         why='The same photograph; scheme p23 lists five steps for "one part @ 5 '
             'marks".',
         use=[0, 1, 2, 3, 4], tariff='questionTotal', total=5,
         question_figure='engineering-2022-OL-paper-q6c-crop',
         notes="The scheme prints 'one part @ 5 marks'."),
    dict(key=(7, 'a', None),
         why='The two fits are drawn at A and B with their dimensions; scheme '
             'p24 answers "A: Clearance fit B: Interference fit", "Two parts @ 6 '
             'marks (12)".',
         topic='eng-3-12',
         lifted=[S(24, 70, 182, 180, 201), S(24, 70, 211, 180, 230)],
         marks=[6, 6], total=12, stem=False,
         figure='engineering-2022-OL-paper-q7a-crop',
         labels={'A': S(24, 92, 182, 160, 201), 'B': S(24, 92, 211, 170, 230)}),
    *[dict(key=(7, 'b', r),
           why='The gear and shaft are drawn with both dimensions; the reader puts '
               'the shaft\'s dimension callout into (i)\'s text, so each roman\'s '
               'question is lifted from its own line under (b)\'s cue. Scheme p24, '
               '"20 marks", five a line.',
           topic='eng-3-12', stem=False,
           question_lift=P(8, *_B_CUE, more=[_STATE, line]),
           lifted=[S(24, 105, y0, 380, y1)], marks=[5], total=5,
           question_figure='engineering-2022-OL-paper-q7b-crop')
      for r, line, (y0, y1) in (
          ('i', (138, 287, 330, 303), (298, 317)),
          ('ii', (138, 311, 330, 329), (312, 331)),
          ('iii', (138, 337, 330, 355), (330, 349)),
          ('iv', (138, 363, 330, 381), (345, 364)))],
    dict(key=(2, 'b', None),
         replaces='the shipped card\'s options were fragments: the cupola and blast furnaces '
                  'cut to their first sentences, the basic oxygen furnace missing, the '
                  'electric arc furnace split in three with its drawing\'s labels "Furnace '
                  'lid Carbon electrodes" read into it and its caption an option of its own; '
                  'and it priced the description at the part\'s 12 where the scheme prints 6 '
                  'for the description and 6 for the labelled diagram',
         why='"Any one": scheme pp12-14 describe four furnaces, each beside its labelled '
             'diagram over the furnace\'s name, shown with the answer; "Describe Award 6 '
             'Marks", "Labelled diagram Award 6 Marks". Each option is the name joined to '
             'its description; the diagram row is the box\'s own heading.',
         topic='eng-1-4',
         lifted=[[join(S(12, 110, 689, 190, 705), S(12, 255, 489, 445, 714)),
                  join(S(13, 130, 336, 240, 352), S(13, 264, 136, 447, 317)),
                  join(S(13, 135, 711, 205, 727), S(13, 276, 507, 445, 718)),
                  join(S(14, 130, 305, 230, 321), S(14, 265, 102, 447, 313))],
                 S(12, 458, 491, 550, 506)],
         row_kind='anyN', group=[(1, 6), None], marks=[6, 6], tariff='fixed', total=12,
         figure='engineering-2022-OL-scheme-q2b-sol',
         notes="The scheme prints 'Describe Award 6 Marks' and 'Labelled diagram Award 6 "
               "Marks', 'Total (12) Marks', for the furnace chosen."),
]

# Question 1 parts the scheme prices half and half, which the automatic author
# read from the marks grid as one six-mark total; each row now carries the
# half printed beside it (eng_residue REPRICE). Opened on the scheme page named.
REPRICE = {
    'eng-2022-ol-q1-a': ([3, 3], 'Safety Precautions Award 3 + 3'),  # scheme p7
    'eng-2022-ol-q1-c': ([3, 3], 'Benefits Award 3 + 3'),  # scheme p7
    'eng-2022-ol-q1-g': ([3, 3], 'Explain & name Award 3 + 3'),  # scheme p7
    'eng-2022-ol-q1-k': ([3, 3], 'Definition & Name Award 3 + 3'),  # scheme p10
    'eng-2022-ol-q1-m': ([3, 3], 'Safety Precautions Award 3 + 3 Marks'),  # scheme p11
}

TOPICS = {
    'eng-2022-ol-q5-a-ii': ('eng-1-9', 'describing a plastic manufacturing process is '
                            'plastics processing, not manufacturing systems'),
}

ATLAS = {
    **{f'eng-2022-ol-q3-d-{p}': dict(
        topics=['Energy, Electronics & Robotics'],
        note='Robotics in medicine, gardening and manufacturing (the OR branch of '
             'Q3(d)); the card\'s syllabus heading is Technology, where the '
             'syllabus places robotics.') for p in ('i', 'ii', 'iii')},
}
