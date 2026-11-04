"""2025 Ordinary Level: the parts eng_all refuses or gets wrong, from the page.

Paper LC027GLP000EV; scheme pages as the PDF numbers them (the scheme prints
its own page numbers five lower). Question 1 is answered any eight at six
marks each, "1 extra mark for each of the two question parts answered
correctly" (scheme p7).
"""
from eng_lift import join, lift

Y, L = 2025, 'ol'


def S(page, *rect):
    return lift(Y, L, 'scheme', page, rect)


def P(page, *rect, more=()):
    return lift(Y, L, 'paper', page, rect, more=more)


# Scheme pp12-13: each furnace's heading, over its (i)-(iii).
_FA = (12, 58, 281, 200, 301)        # "Furnace A – Blast furnace"
_FB = (12, 58, 505, 250, 523)        # "Furnace B – Electrical Arc furnace: -"
_FC = (13, 58, 73, 250, 91)          # "Furnace C – Basic Oxygen furnace: -"
_B2 = (76, 229, 498, 245)            # paper p3: "(b) Select one of the furnaces ..."
# Scheme p14: each mechanism's heading.
_MA, _MB, _MC = (14, 66, 101, 152, 117), (14, 66, 277, 152, 293), (14, 66, 438, 152, 454)
# Paper p8: (b)'s cue and "State the:".
_B7 = (76, 229, 440, 245)
_STATE7 = (76, 258, 132, 274)
_OR3 = ('The paper sets this (d) as the alternative, after an OR, to "(d) Explain '
        'any two of the following metal properties".')
_OR6 = ('The paper sets two (c)s either side of an OR, the stunt bike pegs and CAD/'
        'CNC, and the scheme prices their (iii)s alike, "Award 2 @ 4 Marks".')

CROPS = {
    'engineering-2025-OL-paper-q1m-crop': dict(
        doc='paper', page=2, rect=(420, 731, 480, 801), ref='2025 OL Q1(m)'),
    'engineering-2025-OL-paper-q2a-crop': dict(
        doc='paper', page=3, rect=(66, 78, 516, 212), ref='2025 OL Q2(a)',
        letters=('A', 'B', 'C')),
    # The mini excavator with its three parts arrowed and its caption whole
    # (the automatic crop cut the caption in half).
    'engineering-2025-OL-paper-q2c-crop': dict(
        doc='paper', page=3, rect=(125, 405, 432, 614), ref='2025 OL Q2(c)'),
    'engineering-2025-OL-paper-q2d-crop': dict(
        doc='paper', page=3, rect=(88, 668, 550, 768), ref='2025 OL Q2(d)',
        letters=('A', 'B', 'C')),
    'engineering-2025-OL-paper-q3di-crop': dict(
        doc='paper', page=4, rect=(54, 602, 187, 727), ref='2025 OL Q3(d)(i)'),
    'engineering-2025-OL-paper-q3dii-crop': dict(
        doc='paper', page=4, rect=(231, 611, 387, 727), ref='2025 OL Q3(d)(ii)'),
    'engineering-2025-OL-paper-q3diii-crop': dict(
        doc='paper', page=4, rect=(406, 597, 562, 723), ref='2025 OL Q3(d)(iii)'),
    'engineering-2025-OL-paper-q4a-crop': dict(
        doc='paper', page=5, rect=(355, 60, 552, 185), ref='2025 OL Q4(a)',
        letters=('A', 'B', 'C')),
    # The R-clip; the shipped card showed tool A (the Allen key) instead.
    'engineering-2025-OL-paper-q4ci-crop': dict(
        doc='paper', page=5, rect=(402, 460, 558, 556), ref='2025 OL Q4(c)(i)'),
    # Tool A with its caption whole (the automatic crop cut the "A").
    'engineering-2025-OL-paper-q4civ-crop': dict(
        doc='paper', page=5, rect=(462, 565, 530, 638), ref='2025 OL Q4(c)(iv)',
        letters=('A',)),
    # The four items with all four captions (the automatic crop cut (iii)'s
    # and (iv)'s).
    'engineering-2025-OL-paper-q5d-crop': dict(
        doc='paper', page=6, rect=(105, 530, 540, 770), ref='2025 OL Q5(d)'),
    'engineering-2025-OL-paper-q6a-crop': dict(
        doc='paper', page=7, rect=(45, 102, 562, 228), ref='2025 OL Q6(a)',
        letters=('A', 'B', 'C', 'D')),
    # The stunt bike pegs beside the CAD screen: the two (c)s' pictures.
    'engineering-2025-OL-paper-q6c-crop': dict(
        doc='paper', page=7, parts=[(7, (400, 278, 556, 562)),
                                    (7, (395, 618, 562, 757))],
        layout='row', ref='2025 OL Q6(c)'),
    # The pipe assembly with both dimensions; (b)'s own romans run into the
    # box on the left and are whited out.
    'engineering-2025-OL-paper-q7b-crop': dict(
        doc='paper', page=8, rect=(284, 252, 566, 398), mask=[(282, 255, 336, 360)],
        ref='2025 OL Q7(b)'),
    'engineering-2025-OL-paper-q7c-crop': dict(
        doc='paper', page=8, rect=(60, 433, 556, 578), ref='2025 OL Q7(c)'),
    # Scheme pp19-20: the three processes' labelled diagrams, stacked; the
    # blow-moulding heading and paragraph edge into its box and are whited out.
    'engineering-2025-OL-scheme-q5aii-sol': dict(
        doc='scheme', page=19, parts=[(19, (80, 299, 460, 428)),
                                      (19, (80, 552, 460, 676)),
                                      (20, (80, 178, 460, 318))],
        mask=[(80, 549, 180, 567), (80, 666, 352, 682)],
        solution=True, ref='2025 OL Q5(a)(ii)'),
}

CARDS = [
    dict(key=(1, 'l', None),
         replaces='the shipped card listed two diagrams\' callouts, "External '
                  'thread Internal thread" and "Countersunk machine screw '
                  'Countersunk hole", as answers',
         why='Scheme pp10-11 explain each of the three beside a diagram; each '
             'explanation is lifted by its own rectangle. "Any one explanation '
             'Award 6 Marks".',
         topic='eng-2-11', concept='any-following-internal-thread-blind-hole',
         lifted=[S(10, 90, 596, 460, 704), S(11, 90, 84, 460, 118),
                 S(11, 90, 230, 460, 309)],
         tariff='questionTotal', total=6,
         notes="The scheme prints 'Any one explanation Award 6 Marks'."),
    dict(key=(1, 'm', None),
         why='"the type of nut shown" is photographed and captioned beside (m); '
             'a locknut is mechanical fastening, under Joining. Scheme p11, '
             '"Name Award 3 Marks", "Application Award 3 Marks".',
         topic='eng-2-10',
         lifted=[S(11, 68, 466, 300, 497), S(11, 68, 510, 460, 630)],
         marks=[3, 3], total=6, stem=True,
         question_figure='engineering-2025-OL-paper-q1m-crop'),
    dict(key=(2, 'a', None),
         why='The three furnaces are drawn and lettered A-C on p3; scheme p12 '
             'names each, "Award 3 @ 5 Marks".',
         lifted=[S(12, 92, 144, 300, 164), S(12, 92, 174, 300, 194),
                 S(12, 92, 204, 300, 224)],
         marks=[5, 5, 5], total=15, figure='engineering-2025-OL-paper-q2a-crop',
         labels={'A': S(12, 159, 144, 300, 164), 'B': S(12, 159, 174, 300, 194),
                 'C': S(12, 159, 204, 300, 224)}),
    *[dict(key=(2, 'b', r),
           why='Scheme pp12-13 answer the three furnaces as three blocks, each '
               'with its own (i)-(iii); each furnace\'s answer is lifted with its '
               f'heading. "{price}".',
           question_lift=P(3, *_B2, more=[line]), stem=False,
           lifted=[[join(S(*_FA), S(12, *a)), join(S(*_FB), S(12, *b)),
                    join(S(*_FC), S(13, *c))]],
           marks=[m], total=m,
           notes=f"The scheme prints '{price}', for the furnace selected.")
      for r, line, a, b, c, m, price in (
          ('i', (118, 249, 306, 265), (200, 325, 300, 375), (200, 547, 300, 597),
           (188, 115, 300, 165), 3, '(i) Materials Award 3 Marks'),
          ('ii', (118, 271, 298, 287), (200, 413, 400, 433), (110, 635, 460, 685),
           (188, 189, 400, 238), 6, '(ii) Heat Award 6 Marks'),
          ('iii', (116, 291, 258, 309), (195, 457, 260, 477), (190, 708, 260, 729),
           (188, 262, 240, 282), 3, '(iii) Metal Award 3 Marks'))],
    dict(key=(2, 'c', 'i'), id='eng-2025-ol-q2-c-i-v2',
         why='The withdrawn eng-2025-ol-q2-c-i kept one material of three. Scheme '
             'p13 answers the three labelled parts as three small blocks, part, '
             '(i) material, (ii) reason; "(i) Material Award 3 @ 3 Marks".',
         lifted=[S(13, 62, 321, 400, 352), S(13, 62, 395, 400, 425),
                 S(13, 62, 468, 400, 498)],
         marks=[3, 3, 3], total=9,
         question_figure='engineering-2025-OL-paper-q2c-crop'),
    dict(key=(2, 'c', 'ii'),
         replaces='the shipped "any three @ 2" offered "Tracks: -" and "Reason: '
                  'Light, flexible and shock absorption Digging bucket: -" as '
                  'options, and had no seat reason at all',
         why='The same three blocks; "(ii) Reason Award 3 @ 2 Marks". Each row '
             'carries the part and material the reason is for.',
         lifted=[S(13, 62, 321, 400, 366), S(13, 62, 395, 400, 440),
                 S(13, 62, 468, 400, 513)],
         marks=[2, 2, 2], total=6,
         question_figure='engineering-2025-OL-paper-q2c-crop'),
    dict(key=(2, 'd', None),
         why='The three mechanisms are photographed and lettered A-C on p3; '
             'scheme p14 prices name and use apart, "Name Award 2 @ 2 Marks, Use '
             'Award 2 @ 2 Marks", so a name is claimed without its use; each use '
             'is shown with the mechanism it is for.',
         topic='eng-2-15',
         lifted=[[join(S(*_MA), S(14, 95, 142, 240, 160)),
                  join(S(*_MB), S(14, 93, 303, 215, 321)),
                  join(S(*_MC), S(14, 90, 464, 220, 482))],
                 [join(S(*_MA), S(14, 95, 142, 262, 176)),
                  join(S(*_MB), S(14, 93, 303, 255, 351)),
                  join(S(*_MC), S(14, 90, 464, 278, 512))]],
         row_kind='anyN', group=[(2, 2), (2, 2)], marks=[4, 4], tariff='fixed',
         total=8, figure='engineering-2025-OL-paper-q2d-crop',
         labels={'A': S(14, 135, 142, 240, 160), 'B': S(14, 132, 303, 215, 321),
                 'C': S(14, 130, 464, 220, 482)},
         notes="The scheme prints 'Name Award 2 @ 2 Marks, Use Award 2 @ 2 Marks'."),
    dict(key=(3, 'a', None),
         replaces='the shipped card set "Award 2 @ 7 Marks" as one whole-question '
                  'tariff, so explaining one of the two could not be claimed',
         why='Scheme p15 explains each, "Explain Award 2 @ 7 Marks"; the paper asks '
             'for each.',
         lifted=[S(15, 98, 164, 460, 228), S(15, 98, 254, 460, 333)],
         marks=[7, 7], total=14,
         notes="The scheme prints 'Award 2 @ 7 Marks'."),
    dict(key=(3, 'b', None),
         why='The paper reader takes the concrete saw photograph\'s captions for '
             'part of option (i), so the question is lifted from its own lines '
             '(the photograph is decorative: eng_all NO_FIGURE). Scheme p15 '
             'describes each, "Describe Award 2 @ 7 Marks".',
         topic='eng-2-6',
         question_lift=P(4, 76, 184, 280, 234, more=[(76, 264, 306, 280),
                                                    (90, 289, 185, 355)]),
         lifted=[[S(15, 98, 385, 462, 464), S(15, 98, 488, 462, 522),
                  S(15, 98, 546, 462, 610)]],
         row_kind='anyN', group=(2, 7), marks=[14], tariff='fixed', total=14,
         notes="The scheme prints 'Award 2 @ 7 Marks'."),
    dict(key=(3, 'd', None),
         why='Paper p4 sets two alternative (d)s either side of an OR. This card '
             'is the first branch, the three properties; scheme p16 explains each, '
             '"Explain Award 2 @ 6 Marks".',
         topic='eng-3-8', question_lift=P(4, 76, 462, 555, 504),
         lifted=[[S(16, 105, 115, 460, 176), S(16, 105, 185, 460, 233),
                  S(16, 105, 243, 460, 291)]],
         row_kind='anyN', group=(2, 6), marks=[12], tariff='fixed', total=12,
         notes="The scheme prints 'Award 2 @ 6 Marks'. The paper sets this (d) "
               "and the robotics (d) beneath it either side of an OR."),
    *[dict(key=(3, 'd', r),
           why='The OR branch: "Explain how robotic technology has changed each of '
               'the areas shown below:" over three photographs, captioned (i)-(iii); '
               'scheme p16, "Explanation Award 3 @ 4 Marks".',
           topic='eng-3-14',
           question_lift=P(4, 76, 569, 460, 585, more=[cap]),
           lifted=[S(16, 100, y0, 460, y1)], marks=[4], total=4,
           question_figure=f'engineering-2025-OL-paper-q3d{r}-crop', notes=_OR3)
      for r, cap, (y0, y1) in (
          ('i', (92, 728, 182, 746), (347, 437)),
          ('ii', (264, 730, 376, 746), (450, 525)),
          ('iii', (450, 730, 546, 746), (538, 613)))],
    dict(key=(4, 'a', 'i'),
         why='The three flames are drawn and lettered A-C on p5; scheme p17 names '
             'each, "(i) Name Award 3 @ 2 Marks".',
         lifted=[S(17, 90, 146, 300, 166), S(17, 90, 205, 300, 225),
                 S(17, 90, 264, 300, 284)],
         marks=[2, 2, 2], total=6, figure='engineering-2025-OL-paper-q4a-crop',
         labels={'A': S(17, 143, 146, 300, 166), 'B': S(17, 143, 205, 300, 225),
                 'C': S(17, 143, 264, 300, 284)}),
    dict(key=(4, 'a', 'ii'),
         why='The same flames; scheme p17 (which numbers this part "(i)" a second '
             'time) gives each flame\'s proportions, "(ii) Proportions Award 3 @ 2 '
             'Marks".',
         lifted=[S(17, 86, 323, 400, 343), S(17, 86, 353, 400, 373),
                 S(17, 86, 383, 400, 403)],
         marks=[2, 2, 2], total=6,
         question_figure='engineering-2025-OL-paper-q4a-crop',
         labels={'A': S(17, 143, 146, 300, 166), 'B': S(17, 143, 205, 300, 225),
                 'C': S(17, 143, 264, 300, 284)}),
    dict(key=(4, 'c', 'i'),
         replaces='the shipped card showed tool A, the Allen key, as "the R-clip '
                  'shown"',
         why='The R-clip is photographed and captioned on p5; scheme p18 answers in '
             'two sentences, "Award 3 @ 5 Marks".',
         lifted=[S(18, 98, 114, 405, 133), S(18, 98, 129, 405, 192)],
         tariff='questionTotal', total=5,
         question_figure='engineering-2025-OL-paper-q4ci-crop',
         notes="The scheme prints 'Award 3 @ 5 Marks'."),
    dict(key=(4, 'c', 'iv'),
         replaces='the shipped picture cut the caption "tool A" through its letter, '
                  'and the card did not say what A is',
         why='Tool A is photographed and captioned on p5; scheme p18 names it and '
             'gives a use, priced by (c)\'s "Award 3 @ 5 Marks".',
         lifted=[S(18, 108, 399, 200, 419), S(18, 108, 433, 460, 504)],
         tariff='questionTotal', total=5,
         figure='engineering-2025-OL-paper-q4civ-crop',
         labels={'A': S(18, 147, 399, 200, 419)},
         notes="The scheme prints 'Award 3 @ 5 Marks'."),
    dict(key=(4, 'd', None),
         why='Scheme p18 heads (d) "Two safety precautions:" and prices it "Award 2 '
             '@ 4 Marks" (the summary grid\'s "One part @ 8" is one row out of '
             'line): one row per precaution.',
         topic='eng-2-10',
         lifted=[S(18, 120, 561, 420, 596), S(18, 120, 606, 420, 640)],
         marks=[4, 4], total=8,
         notes="The scheme prints 'Award 2 @ 4 Marks'."),
    dict(key=(5, 'a', 'i'),
         replaces='the shipped "any three @ 3" had one option, "A: Compression '
                  'moulding B: Blow moulding C: Vacuum forming. ii) Describe any one '
                  'plastic manufacturing process:", with (ii)\'s heading in it',
         why='The three processes are drawn and lettered A-C on p6; scheme p19 '
             'names each, "(i) Name Award 3 @ 3 Marks".',
         lifted=[S(19, 80, 163, 300, 183), S(19, 80, 193, 300, 213),
                 S(19, 80, 222, 300, 242)],
         marks=[3, 3, 3], total=9,
         question_figure='engineering-2025-OL-paper-q5ai-art',
         labels={'A': S(19, 118, 163, 300, 183), 'B': S(19, 118, 193, 300, 213),
                 'C': S(19, 118, 222, 300, 242)}),
    dict(key=(5, 'a', 'ii'),
         why='Scheme pp19-20 describe each process under its heading beside a '
             'labelled diagram, "(ii) Describe Award 1 @ 11 Marks"; heading and '
             'paragraph are lifted apart and joined, leaving the callouts out. The '
             'diagrams are shown with the answer.',
         topic='eng-1-9',
         lifted=[[join(S(19, 80, 283, 230, 301), S(19, 80, 428, 460, 522)),
                  join(S(19, 80, 549, 180, 567), S(19, 80, 669, 460, 748)),
                  S(20, 80, 72, 450, 177)]],
         marks=[11], total=11,
         question_figure='engineering-2025-OL-paper-q5ai-art',
         figure='engineering-2025-OL-scheme-q5aii-sol',
         notes="The scheme prints 'Award 1 @ 11 Marks'."),
    dict(key=(5, 'c', None),
         why='Scheme p21 heads the two precautions with a sentence the reader takes '
             'for the first answer; each precaution is lifted by its own rectangle. '
             '"Award 2 @ 5 Marks".',
         topic='eng-3-1',
         lifted=[S(21, 112, 135, 455, 185), S(21, 112, 195, 455, 259)],
         marks=[5, 5], total=10,
         notes="The scheme prints 'Award 2 @ 5 Marks'."),
    dict(key=(5, 'd', None),
         replaces='the shipped picture cut the captions of items (iii) and (iv)',
         why='The four items are photographed and captioned on p6; scheme p21 names '
             'a plastic for each, "Award 2 @ 5 Marks".',
         lifted=[[S(21, 125, 330, 340, 346), S(21, 125, 356, 340, 376),
                  S(21, 125, 387, 340, 405), S(21, 125, 415, 340, 435)]],
         row_kind='anyN', group=(2, 5), marks=[10], tariff='fixed', total=10,
         question_figure='engineering-2025-OL-paper-q5d-crop',
         notes="The scheme prints 'Award 2 @ 5 Marks'."),
    dict(key=(6, 'a', None),
         why='The four lathe parts are photographed and lettered A-D on p7; scheme '
             'p22 names each, "Identify Award 3 @ 5 Marks".',
         lifted=[[S(22, 112, 146, 300, 166), S(22, 112, 175, 300, 195),
                  S(22, 112, 206, 300, 226), S(22, 112, 234, 300, 254)]],
         row_kind='anyN', group=(3, 5), marks=[15], tariff='fixed', total=15,
         figure='engineering-2025-OL-paper-q6a-crop',
         labels={'A': S(22, 129, 146, 300, 166), 'B': S(22, 129, 175, 300, 195),
                 'C': S(22, 129, 206, 300, 226), 'D': S(22, 129, 234, 300, 254)},
         notes="The scheme prints 'Award 3 @ 5 Marks'."),
    dict(key=(6, 'c', 'i'),
         replaces='the shipped "any two @ 3" offered the CAD branch\'s answer among '
                  'the lathe processes, so it scored 3 where that branch pays 6',
         why='Both (c)s price their (i) at 6 (scheme p23): two lathe processes, '
             '"Award 2 @ 3 Marks", or one advantage of CAD, "Award 1 @ 6 Marks". '
             'One card for the printed OR, each branch a route of its own.',
         lifted=[S(23, 133, 99, 185, 118), S(23, 133, 114, 185, 134),
                 S(23, 112, 503, 415, 537)],
         marks=[3, 3, 6], routes=['a', 'a', 'b'], total=6,
         question_figure='engineering-2025-OL-paper-q6c-crop',
         notes="The paper sets two (c)s either side of an OR; the scheme prints "
               "'Award 2 @ 3 Marks' for the lathe processes and 'Award 1 @ 6 "
               "Marks' for the advantage of CAD."),
    dict(key=(6, 'c', 'iii'),
         replaces='the shipped "any two @ 4" mixed the branches, and the CNC '
                  'branch\'s one line holds both its advantages, so that branch '
                  'could claim 4 of its 8',
         why='Both (c)s price their (iii) "Award 2 @ 4 Marks" (scheme p23). The CNC '
             'branch prints its two advantages in one line joined by "and"; each '
             'is lifted by its own rectangle. One card, each branch a route.',
         lifted=[S(23, 124, 375, 300, 395), S(23, 124, 404, 300, 424),
                 S(23, 112, 594, 185, 610), S(23, 206, 594, 420, 610)],
         marks=[4, 4, 4, 4], routes=['a', 'a', 'b', 'b'], total=8,
         question_figure='engineering-2025-OL-paper-q6c-crop', notes=_OR6),
    dict(key=(7, 'a', 'ii'),
         why='Scheme p24 (which numbers this part "(iv)") names one other fit and '
             'an application for it, "(ii) Name Award 1 @ 4 Marks, (ii) Application '
             'Award 1 @ 4 Marks".',
         lifted=[S(24, 112, 182, 400, 201), S(24, 112, 197, 400, 216)],
         marks=[4, 4], total=8),
    *[dict(key=(7, 'b', r),
           why='The pipe assembly is drawn with the flange and hole dimensions on '
               'p8; each roman\'s question is lifted with (b)\'s cue. Scheme p24, '
               '"Calculations Award 4 @ 5 Marks".',
           topic='eng-3-12', stem=False,
           question_lift=P(8, *_B7, more=[_STATE7, line]),
           lifted=[S(24, 110, y0, 385, y1)], marks=[5], total=5,
           question_figure='engineering-2025-OL-paper-q7b-crop')
      for r, line, (y0, y1) in (
          ('i', (158, 258, 334, 274), (349, 368)),
          ('ii', (158, 286, 325, 302), (378, 397)),
          ('iii', (158, 314, 318, 330), (407, 426)),
          ('iv', (158, 342, 285, 358), (437, 456)))],
    dict(key=(7, 'c', None),
         why='The instruments branch of (c): four photographs captioned (i)-(iv). '
             'Scheme pp24-25 price name and application apart, "Name Award 3 @ 3 '
             'Marks, Application Award 3 @ 3 Marks", so a name is claimed without '
             'its application; each application is shown with the instrument it '
             'is for.',
         topic='eng-3-12', question_lift=P(8, 76, 417, 550, 433),
         lifted=[[S(24, 75, 508, 255, 528), S(24, 75, 633, 250, 649),
                  S(25, 75, 72, 210, 88), S(25, 75, 187, 260, 203)],
                 [S(24, 75, 508, 340, 586), S(24, 75, 633, 340, 664),
                  S(25, 75, 72, 340, 162), S(25, 75, 187, 345, 219)]],
         row_kind='anyN', group=[(3, 3), (3, 3)], marks=[9, 9], tariff='fixed',
         total=18, question_figure='engineering-2025-OL-paper-q7c-crop',
         notes="The scheme prints 'Name Award 3 @ 3 Marks, Application Award 3 @ 3 "
               "Marks'."),
]

TOPICS = {
    'eng-2025-ol-q4-c-ii': ('eng-2-10', 'a method of joining sheet aluminium is joining; '
                            '"aluminium" outvoted it'),
}

_ROB = 'Energy, Electronics & Robotics'

ATLAS = {
    'eng-2025-ol-q1-a': dict(
        topics=['Health and Safety'],
        note='Safety precautions when using a bandsaw, which the reference files '
             'Q1(a) under; the card\'s syllabus heading is Machining.'),
    'eng-2025-ol-q1-i': dict(
        topics=['Mechanical Joining & Assembly'],
        note='Why metal edges are deburred, which the reference files Q1(i) under; '
             'the card\'s syllabus heading is Machining.'),
    'eng-2025-ol-q1-j': dict(
        topics=[_ROB],
        note='AI, renewable energy or virtual reality, which the reference files '
             'Q1(j) under; the card\'s syllabus heading is Machining.'),
    'eng-2025-ol-q1-l': dict(
        topics=['Mechanical Joining & Assembly'],
        note='Internal threads, blind and countersunk holes, which the reference '
             'files Q1(l) under; the card\'s syllabus heading is Machining.'),
    **{k: dict(
        topics=['Materials: Properties and Uses'],
        note='Choosing a material for each part of the mini excavator, and why; the '
             'reference files Q2(c) under tools and mechanisms only. The card\'s '
             'syllabus heading is Technology.')
       for k in ('eng-2025-ol-q2-c-i-v2', 'eng-2025-ol-q2-c-ii')},
    **{f'eng-2025-ol-q3-d-{p}': dict(
        topics=[_ROB],
        note='Robotics in parcel delivery, medicine and mass production (the OR '
             'branch of Q3(d)); the card\'s syllabus heading is Technology, where the '
             'syllabus places robotics.') for p in ('i', 'ii', 'iii')},
}
