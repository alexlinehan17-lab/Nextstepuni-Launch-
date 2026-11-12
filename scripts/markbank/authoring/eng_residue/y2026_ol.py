"""2026 Ordinary Level: the parts eng_all refuses or gets wrong, from the page.

Paper LC027GLP000EV; scheme pages as the PDF numbers them. The marks grid is
on scheme p6: Question 1 is "Any eight parts @ 6 marks each" with "1 extra
mark for each of the first two correctly answered parts". This sitting had no
cards before the lane: every card here is new, and a `replaces=` names the
automatic card it rebuilds before it ever shipped.

Where the scheme's side column splits a part's six marks ("Award 3 + 3
Marks", "Name Award 3 Marks / Use Award 3 Marks"), each half is a row with its
own marks rather than one question total, so either half can be claimed.
"""
from eng_lift import join, lift

Y, L = 2026, 'ol'
NEW = 'never shipped: the automatic card '
OWNED = ('never shipped: the automatic author builds this card only from the lifts this '
         'entry records, so the entry owns it')


def S(page, *rect, more=()):
    return lift(Y, L, 'scheme', page, rect, more=more)


def P(page, *rect, more=()):
    return lift(Y, L, 'paper', page, rect, more=more)


# Paper p3: Question 2(a)'s cue and its instruction, over the three furnaces.
_A2 = (63, 62, 316, 78)              # "Three metal-producing furnaces are shown below:"
_SEL2 = (63, 233, 435, 249)          # "Select one of the furnaces named above and answer ..."
# Scheme pp12-13: each furnace's caption under its diagram.
_BOF = (12, 84, 409, 200, 425)       # "Basic Oxygen Furnace"
_EAF = (12, 70, 710, 196, 726)       # "Electric Arc Furnace"
_BF = (13, 76, 307, 180, 323)        # "Blast Furnace"
# Scheme p13: each labelled part of the mountain bike.
_SEAT = (13, 60, 492, 140, 508)      # "Saddle seat:"
_FRAME = (13, 59, 551, 112, 567)     # "Frame:"
_TYRE = (13, 59, 624, 102, 640)      # "Tyre:"
# Paper p4: Question 3's two (d)s.
_D3 = (63, 577, 235, 593)            # "Answer any two of the following:"
# Paper p7: Question 6's two (c)s and the OR between them.
_C6A = (63, 374, 413, 390)           # "The thumb screw shown opposite has been knurled ..."
_C6B = (63, 567, 533, 583)           # "Modern engineering workshops use a variety of CNC ..."
_OR6P = (288, 528, 313, 546)         # "OR"
# Paper p8: Question 7(b)'s cue and "State the:"; the PCB branch's cue.
_B7 = (63, 179, 526, 195)
_STATE7 = (63, 200, 117, 216)
_C7B = (63, 629, 451, 645)           # "The 555 Timer PCB (printed circuit board) shown, ..."

_OR3 = ('The paper sets this (d) as the alternative, after an OR, to "(d) Explain any two '
        'of the following material properties".')
_OR6 = ('The paper sets two (c)s either side of an OR, the knurled thumb screw and CNC '
        'machines, and the scheme prices them alike: (i) 6, (ii) 3 + 3, (iii) 4 + 4.')
_OR7 = ('The paper sets two (c)s either side of an OR, measuring instruments and the 555 '
        'timer PCB; the scheme prices their parts differently ((i) 3 + 3 + 3 against '
        '3 + 3, (ii) 5 against 6, (iii) 2 + 2 against 6), so each branch is a card of '
        'its own.')

CROPS = {
    # Paper p2: the eye bolt with its caption (the automatic crop took in
    # Q1(l)'s "(iii) Pilot hole." printed above it).
    'engineering-2026-OL-paper-q1m-crop': dict(
        doc='paper', page=2, rect=(362, 722, 470, 806), ref='2026 OL Q1(m)'),
    # Paper p7: the knurled thumb screw beside the CNC machine, the two (c)s'
    # pictures.
    'engineering-2026-OL-paper-q6c-crop': dict(
        doc='paper', page=7, parts=[(7, (410, 370, 556, 488)),
                                    (7, (378, 585, 540, 738))],
        layout='row', ref='2026 OL Q6(c)'),
    # Paper p8: the pneumatic fitting with both dimensions (the automatic crop
    # cut them off).
    'engineering-2026-OL-paper-q7b-crop': dict(
        doc='paper', page=8, rect=(300, 208, 556, 326), ref='2026 OL Q7(b)'),
    'engineering-2026-OL-paper-q7c-crop': dict(
        doc='paper', page=8, rect=(60, 364, 548, 501), ref='2026 OL Q7(c)(i)',
        letters=('A', 'B', 'C', 'D')),
    'engineering-2026-OL-paper-q7c-or-crop': dict(
        doc='paper', page=8, rect=(390, 646, 566, 798),
        ref='2026 OL Q7(c)(i) — 555 timer PCB'),
    # Scheme pp8-9: the 3D printer's labelled diagram and the wire tensioner's
    # ratchet and pawl, which its answer calls "the ratchet below".
    'engineering-2026-OL-scheme-q1h-sol': dict(
        doc='scheme', page=8, parts=[(8, (283, 534, 457, 729)),
                                     (9, (180, 180, 353, 317))],
        solution=True, ref='2026 OL Q1(h)'),
    # Scheme p9: the plain and threaded holes, captioned.
    'engineering-2026-OL-scheme-q1i-sol': dict(
        doc='scheme', page=9, rect=(110, 501, 402, 606), solution=True,
        ref='2026 OL Q1(i)'),
    # Scheme pp10-11: the ball bearing's labelled parts and the pilot hole.
    'engineering-2026-OL-scheme-q1l-sol': dict(
        doc='scheme', page=10, parts=[(10, (256, 496, 453, 738)),
                                      (11, (131, 130, 315, 240))],
        solution=True, ref='2026 OL Q1(l)'),
    # Scheme p11: "The eyebolt shown below is used to help tow a car."
    'engineering-2026-OL-scheme-q1m-sol': dict(
        doc='scheme', page=11, rect=(162, 380, 387, 538), solution=True,
        ref='2026 OL Q1(m)'),
    # Scheme pp12-13: the three furnaces' labelled diagrams, each with its
    # caption, stacked; the blast furnace's neighbouring "(ii)" and "(iii)"
    # headings edge into its box and are whited out.
    'engineering-2026-OL-scheme-q2ai-sol': dict(
        doc='scheme', page=12, parts=[(12, (14, 226, 240, 426)),
                                      (12, (25, 500, 262, 727)),
                                      (13, (50, 95, 270, 324))],
        mask=[(258, 120, 272, 140), (258, 183, 272, 203)],
        solution=True, ref='2026 OL Q2(a)(i)'),
    # Scheme pp20-21: the three processes' labelled diagrams under their
    # headings, stacked.
    'engineering-2026-OL-scheme-q5aii-sol': dict(
        doc='scheme', page=20, parts=[(20, (66, 350, 444, 566)),
                                      (21, (60, 72, 452, 263)),
                                      (21, (66, 412, 452, 612))],
        solution=True, ref='2026 OL Q5(a)(ii)'),
}

FOLDED = {
    'eng-2026-ol-q6-b-iv': NEW[:-1] + ' set "Feed." apart from the other three terms of '
                           '"Explain any three of the following in relation to machining:"; '
                           'the list is one printed choice, carded at Q6(b)',
}

CARDS = [
    # ---- Question 1 ------------------------------------------------------
    dict(key=(1, 'a', None),
         replaces=NEW + 'set the scheme\'s "Award 3 + 3 Marks" as one 6-mark total',
         why='Scheme p7 gives two precautions, "Safety Precautions Award 3 + 3 '
             'Marks"; one row each.',
         lifted=[S(7, 98, 241, 440, 272), S(7, 98, 286, 440, 316)],
         marks=[3, 3], total=6,
         notes="The scheme prints 'Award 3 + 3 Marks'."),
    dict(key=(1, 'b', None),
         replaces=NEW + 'set "Advantage Award 3 Marks" and "Disadvantage Award 3 Marks" '
                  'as one 6-mark total',
         why='Scheme p7 prices the advantage and the disadvantage 3 each.',
         lifted=[S(7, 97, 381, 440, 411), S(7, 97, 425, 440, 456)],
         marks=[3, 3], total=6,
         notes="The scheme prints 'Advantage Award 3 Marks, Disadvantage Award 3 Marks'."),
    dict(key=(1, 'c', None),
         why='Scheme p7 answers in one paragraph, "Explanation Award 6 Marks". '
             'Testing a design is the syllabus\'s design function, under '
             'Technology.',
         topic='eng-3-14',
         lifted=[S(7, 97, 505, 450, 551)], marks=[6], total=6,
         notes="The scheme prints 'Explanation Award 6 Marks'."),
    dict(key=(1, 'd', None),
         replaces=NEW + 'set "Name Award 3 Marks" and "Use Award 3 Marks" as one 6-mark '
                  'total',
         why='The countersink is photographed and captioned beside (d); scheme p7 '
             'names it and gives a use, 3 each.',
         lifted=[S(7, 98, 615, 330, 631), S(7, 95, 645, 440, 691)],
         marks=[3, 3], total=6,
         question_figure='engineering-2026-OL-paper-q1d-art',
         notes="The scheme prints 'Name Award 3 Marks, Use Award 3 Marks'."),
    dict(key=(1, 'e', None), replaces=OWNED,
         why='Scheme p8 answers in one sentence across two lines, "Explanation Award '
             '6 Marks"; the reader breaks it at the line.',
         lifted=[S(8, 97, 104, 445, 134)], marks=[6], total=6,
         notes="The scheme prints 'Explanation Award 6 Marks'."),
    dict(key=(1, 'g', None),
         replaces=NEW + 'set "Explanation Award 3 Marks" and "Example Award 3 Marks" as '
                  'one 6-mark total',
         why='Scheme p8 explains the term and gives copper as the example, 3 each.',
         lifted=[S(8, 98, 314, 430, 345), S(8, 97, 359, 430, 389)],
         marks=[3, 3], total=6,
         notes="The scheme prints 'Explanation Award 3 Marks, Example Award 3 Marks'."),
    dict(key=(1, 'h', None), replaces=OWNED,
         why='The three items are photographed and captioned under (h); scheme pp8-9 '
             'describe each in a paragraph, the 3D printer beside its labelled '
             'diagram and the wire tensioner over its ratchet ("The ratchet below"), '
             'both shown with the answer. "Description Award 6 Marks" for any one.',
         lifted=[[S(8, 61, 449, 445, 524), S(8, 61, 552, 280, 758),
                  S(9, 70, 87, 445, 176)]],
         row_kind='anyN', group=(1, 6), marks=[6], tariff='fixed', total=6,
         figure='engineering-2026-OL-scheme-q1h-sol',
         notes="The scheme prints 'Description Award 6 Marks'."),
    dict(key=(1, 'i', None),
         why='Scheme p9 explains each hole and draws both; "Ø10 mm hole Award 3 '
             'Marks, M10 mm hole Award 3 Marks". A tapped hole is cut on the '
             'drill, under Machining.',
         topic='eng-2-11',
         lifted=[S(9, 97, 382, 445, 426), S(9, 97, 441, 445, 500)],
         marks=[3, 3], total=6, figure='engineering-2026-OL-scheme-q1i-sol',
         notes="The scheme prints 'Ø10 mm hole Award 3 Marks, M10 mm hole Award 3 "
               "Marks'."),
    dict(key=(1, 'j', None),
         why='The symbol is printed beside (j). Scheme p9 identifies it in a sentence '
             'the scheme itself cuts off after "to be wo" (the page prints no more); '
             'the row is lifted up to "goggles", which is the identification. '
             '"Identification Award 6 Marks".',
         topic='eng-3-1',
         lifted=[join(S(9, 97, 659, 362, 674), S(9, 97, 674, 138, 689))],
         marks=[6], total=6, question_figure='engineering-2026-OL-paper-q1j-art',
         notes="The scheme prints 'Identification Award 6 Marks'. Its sentence breaks "
               "off after 'to be wo' on the page, so the answer is given up to "
               "'goggles'."),
    dict(key=(1, 'k', None), replaces=OWNED,
         why='Scheme p10 explains each of the three in a paragraph, "Explanation Award '
             '6 Marks" for any one.',
         topic='eng-3-14',
         lifted=[[S(10, 70, 112, 456, 187), S(10, 68, 211, 458, 300),
                  S(10, 68, 326, 458, 386)]],
         row_kind='anyN', group=(1, 6), marks=[6], tariff='fixed', total=6,
         notes="The scheme prints 'Explanation Award 6 Marks'."),
    dict(key=(1, 'l', None),
         replaces=NEW + 'split the ball bearing\'s one explanation into two answers and '
                  'set an any-one choice as one 6-mark total',
         why='Scheme pp10-11 explain each of the three, the ball bearing beside its '
             'labelled parts and the pilot hole over a drawing, both shown with the '
             'answer. "Explanation Award 6 Marks" for any one.',
         topic='eng-2-11',
         lifted=[[S(10, 64, 453, 456, 498), S(10, 64, 522, 257, 670),
                  S(11, 70, 87, 458, 118)]],
         row_kind='anyN', group=(1, 6), marks=[6], tariff='fixed', total=6,
         figure='engineering-2026-OL-scheme-q1l-sol',
         notes="The scheme prints 'Explanation Award 6 Marks'."),
    dict(key=(1, 'm', None),
         why='The eye bolt is photographed and captioned beside (m); scheme p11 gives '
             'its application and shows one towing a car ("The eyebolt shown below"). '
             '"Application Award 6 Marks". A threaded fastener, under Joining.',
         topic='eng-2-10',
         lifted=[S(11, 68, 302, 452, 362)], marks=[6], total=6,
         question_figure='engineering-2026-OL-paper-q1m-crop',
         figure='engineering-2026-OL-scheme-q1m-sol',
         notes="The scheme prints 'Application Award 6 Marks'."),
    # ---- Question 2 ------------------------------------------------------
    dict(key=(2, 'a', 'i'),
         replaces=NEW + 'answered "Draw a simple diagram" with the furnace\'s name, '
                  '"Basic Oxygen Furnace", as a 6-mark option',
         why='Scheme pp12-13 answer (i) with a labelled diagram of each furnace and '
             'print no words for it; the diagrams are shown with the answer. "(i) '
             'Diagram Award 6 Marks".',
         special={'kind': 'ask'}, total=6, stem=False,
         question_lift=P(3, *_A2, more=[_SEL2, (92, 252, 406, 268)]),
         question_figure='engineering-2026-OL-paper-q2ai-art',
         figure='engineering-2026-OL-scheme-q2ai-sol',
         notes="The scheme prints '(i) Diagram Award 6 Marks'."),
    dict(key=(2, 'a', 'ii'),
         replaces=NEW + 'answered "Name one metal produced" with "Electric Arc Furnace"',
         why='Scheme pp12-13 answer each furnace in its own block; each metal is '
             'lifted with the furnace\'s caption. "(ii) Metal Award 5 Marks", for the '
             'furnace selected.',
         question_lift=P(3, *_A2, more=[_SEL2, (92, 274, 232, 290)]), stem=False,
         lifted=[[join(S(*_BOF), S(12, 276, 263, 310, 279)),
                  join(S(*_EAF), S(12, 276, 541, 402, 557)),
                  join(S(*_BF), S(13, 275, 138, 300, 154))]],
         marks=[5], total=5, question_figure='engineering-2026-OL-paper-q2ai-art',
         notes="The scheme prints '(ii) Metal Award 5 Marks', for the furnace "
               "selected."),
    dict(key=(2, 'a', 'iii'),
         why='The same blocks; each removal is lifted with the furnace\'s caption. '
             '"(iii) Removal Award 4 Marks", for the furnace selected.',
         question_lift=P(3, *_A2, more=[_SEL2, (90, 294, 362, 312)]), stem=False,
         lifted=[[join(S(*_BOF), S(12, 276, 311, 442, 385)),
                  join(S(*_EAF), S(12, 278, 604, 450, 651)),
                  join(S(*_BF), S(13, 278, 200, 420, 264))]],
         marks=[4], total=4, question_figure='engineering-2026-OL-paper-q2ai-art',
         notes="The scheme prints '(iii) Removal Award 4 Marks', for the furnace "
               "selected."),
    dict(key=(2, 'b', None),
         replaces=NEW + 'kept the scheme\'s misprinted "(I)" on the first alloy and not '
                  'the numbering of the other two',
         why='Scheme p13 names each alloy\'s metals on one line; each is lifted '
             'without its number. "Name of metals Award 6 + 6 Marks" for any two.',
         lifted=[[S(13, 84, 370, 262, 386), S(13, 84, 400, 265, 416),
                  S(13, 84, 429, 247, 445)]],
         row_kind='anyN', group=(2, 6), marks=[12], tariff='fixed', total=12,
         notes="The scheme prints 'Name of metals Award 6 + 6 Marks'."),
    dict(key=(2, 'c', 'i'),
         why='The mountain bike is photographed with its three parts labelled on p3; '
             'scheme p13 answers each part as a small block, part, (i) material, (ii) '
             'reason. "Material Award 3 + 3 + 3 Marks".',
         stem=True,
         lifted=[join(S(*_SEAT), S(13, 100, 507, 292, 523)),
                 join(S(*_FRAME), S(13, 100, 566, 278, 582)),
                 join(S(*_TYRE), S(13, 100, 639, 190, 655))],
         marks=[3, 3, 3], total=9,
         question_figure='engineering-2026-OL-paper-q2ci-art',
         notes="The scheme prints 'Material Award 3 + 3 + 3 Marks'."),
    dict(key=(2, 'c', 'ii'),
         replaces=NEW + 'gave the three reasons without the part each is for',
         why='The same three blocks; each reason is lifted with its part. "Reason '
             'Award 2 + 2 + 2 Marks".',
         stem=True,
         lifted=[join(S(*_SEAT), S(13, 100, 522, 440, 538)),
                 join(S(*_FRAME), S(13, 100, 580, 427, 611)),
                 join(S(*_TYRE), S(13, 100, 653, 445, 684))],
         marks=[2, 2, 2], total=6,
         question_figure='engineering-2026-OL-paper-q2ci-art',
         notes="The scheme prints 'Reason Award 2 + 2 + 2 Marks'."),
    dict(key=(2, 'd', None), replaces=OWNED,
         why='The three mechanisms are photographed and captioned (i)-(iii) on p3; '
             'scheme p14 answers each with its name and a use, "Name and Application '
             'Award 4 + 4 Marks" for any two.',
         topic='eng-2-15',
         lifted=[[join(S(14, 67, 103, 142, 119), S(14, 67, 147, 320, 236)),
                  join(S(14, 67, 250, 147, 266), S(14, 67, 279, 315, 383)),
                  join(S(14, 67, 426, 150, 442), S(14, 67, 455, 302, 515))]],
         row_kind='anyN', group=(2, 4), marks=[8], tariff='fixed', total=8,
         question_figure='engineering-2026-OL-paper-q2d-art',
         notes="The scheme prints 'Name and Application Award 4 + 4 Marks'."),
    # ---- Question 3 ------------------------------------------------------
    dict(key=(3, 'b', 'i'), replaces=OWNED,
         why='Scheme p15 answers each process in a paragraph under its description; '
             '"Processes Award 7 + 7 Marks" for any two.',
         topic='eng-2-6',
         question_lift=P(4, 63, 145, 396, 161, more=[(92, 171, 432, 187)]),
         stem=False,
         lifted=[S(15, 70, 259, 449, 334)], marks=[7], total=7,
         notes="The scheme prints 'Processes Award 7 + 7 Marks'."),
    dict(key=(3, 'c', None), replaces=OWNED,
         why='Scheme pp15-16 explain each term in a paragraph, carbon content with '
             'the three steels\' percentages; "Heat treatment Award 7 + 7 Marks" for '
             'any two. The reader does not join the three terms to the ask, so it is '
             'lifted with them.',
         question_lift=P(4, 63, 287, 339, 320, more=[(63, 328, 180, 394)]),
         lifted=[[S(15, 73, 569, 453, 629), S(15, 70, 657, 449, 761),
                  join(S(16, 70, 87, 437, 103), S(16, 106, 117, 437, 164))]],
         row_kind='anyN', group=(2, 7), marks=[14], tariff='fixed', total=14,
         notes="The scheme prints 'Heat treatment Award 7 + 7 Marks'."),
    dict(key=(3, 'd', None),
         why='Paper p4 sets two alternative (d)s either side of an OR. This card is '
             'the first branch, the three properties; scheme p16 defines each under '
             'its name, "Explanations Award 6 + 6 Marks" for any two.',
         topic='eng-3-8',
         question_lift=P(4, 63, 451, 328, 467, more=[(63, 477, 548, 493)]),
         lifted=[[join(S(16, 88, 222, 153, 238), S(16, 75, 237, 443, 253)),
                  join(S(16, 88, 265, 143, 281), S(16, 75, 279, 430, 310)),
                  join(S(16, 90, 323, 178, 339), S(16, 75, 338, 416, 354))]],
         row_kind='anyN', group=(2, 6), marks=[12], tariff='fixed', total=12,
         notes="The scheme prints 'Explanations Award 6 + 6 Marks'. The paper sets this "
               "(d) and the robotics (d) beneath it either side of an OR."),
    dict(key=(3, 'd', 'i'),
         replaces=NEW + 'carried both OR branches, "Malleability, OR Describe two ways '
                  'that robotic technology ...", with both branches\' answers',
         why='The OR branch\'s (i); scheme p16 gives two ways, "(i) Safety Award 3 + 3 '
             'Marks".',
         topic='eng-3-14',
         question_lift=P(4, *_D3, more=[(92, 605, 330, 635)]), stem=False,
         lifted=[S(16, 120, 459, 454, 504), S(16, 120, 518, 454, 549)],
         marks=[3, 3], total=6, notes=_OR3),
    dict(key=(3, 'd', 'ii'),
         replaces=NEW + 'carried both OR branches, "Elasticity, OR Identify two '
                  'manufacturing processes ...", with both branches\' answers',
         why='The OR branch\'s (ii); scheme p16 gives two processes, "(ii) Two '
             'Processes Award 3 + 3 Marks".',
         topic='eng-3-14',
         question_lift=P(4, *_D3, more=[(92, 651, 319, 682)]), stem=False,
         lifted=[S(16, 119, 578, 454, 608), S(16, 119, 622, 454, 668)],
         marks=[3, 3], total=6, notes=_OR3),
    dict(key=(3, 'd', 'iii'),
         replaces=NEW + 'carried both OR branches, "Tensile strength. OR Explain the '
                  'term pneumatics.", with both branches\' answers',
         why='The OR branch\'s (iii); scheme p16 explains it in two bullets priced as '
             'one, "(iii) Explain Award 6 Marks".',
         topic='eng-3-14',
         question_lift=P(4, *_D3, more=[(89, 696, 243, 714)]), stem=False,
         lifted=[S(16, 120, 696, 454, 757)], marks=[6], total=6, notes=_OR3),
    # ---- Question 4 ------------------------------------------------------
    *[dict(key=(4, 'a', r),
           why='Scheme p17 names the flame for each condition on its own line, '
               '"Flames Award 2 + 2 + 2 Marks"; the question is lifted with (a)\'s cue.',
           question_lift=P(5, 63, 67, 504, 83, more=[line]), stem=False,
           lifted=[S(17, *ans)], marks=[2], total=2,
           notes="The scheme prints 'Flames Award 2 + 2 + 2 Marks'.")
      for r, line, ans in (
          ('i', (92, 93, 295, 109), (91, 181, 409, 197)),
          ('ii', (92, 115, 170, 131), (86, 210, 306, 226)))],
    dict(key=(4, 'b', None), replaces=OWNED,
         why='Scheme p17 describes each term in a paragraph, "Descriptions Award 3 + '
             '3" for any two.',
         lifted=[[S(17, 72, 330, 445, 376), S(17, 73, 418, 438, 464),
                  S(17, 75, 506, 440, 551), S(17, 75, 594, 439, 654)]],
         row_kind='anyN', group=(2, 3), marks=[6], tariff='fixed', total=6,
         notes="The scheme prints 'Descriptions Award 3 + 3'."),
    dict(key=(4, 'c', None),
         replaces=NEW + 'split the gas regulator\'s answer and the goggles\' answer into '
                  'two options each, so six options stood for four items',
         why='Scheme p18 answers each item in one block under its name; each block is '
             'lifted whole. "Function Award 5 + 5 + 5 Marks" for any three.',
         lifted=[[S(18, 75, 104, 420, 208), S(18, 77, 236, 448, 267),
                  S(18, 78, 295, 436, 354), S(18, 77, 382, 447, 413)]],
         row_kind='anyN', group=(3, 5), marks=[15], tariff='fixed', total=15,
         notes="The scheme prints 'Function Award 5 + 5 + 5 Marks'."),
    dict(key=(4, 'd', 'i'), replaces=OWNED,
         why='Scheme p18 answers under the question in two lines, "Explanations Award '
             '5 + 5 + 5 Marks" for any three.',
         lifted=[S(18, 89, 500, 421, 530)], marks=[5], total=5,
         notes="The scheme prints 'Explanations Award 5 + 5 + 5 Marks'."),
    dict(key=(4, 'e', None), replaces=OWNED,
         why='Scheme p19 gives two precautions, "Safety Precautions Award 4 + 4 '
             'Marks"; one row each.',
         lifted=[S(19, 106, 105, 441, 135), S(19, 106, 149, 441, 180)],
         marks=[4, 4], total=8,
         notes="The scheme prints 'Safety Precautions Award 4 + 4 Marks'."),
    # ---- Question 5 ------------------------------------------------------
    dict(key=(5, 'a', 'i'),
         replaces=NEW + 'set the three names as one row worth the whole 15',
         why='The three processes are drawn and lettered A-C on p6; scheme p20 names '
             'each, "(i) Name Award 5 + 5 + 5 Marks".',
         lifted=[S(20, 70, 168, 160, 184), S(20, 70, 197, 190, 213),
                 S(20, 70, 227, 200, 243)],
         marks=[5, 5, 5], total=15,
         question_figure='engineering-2026-OL-paper-q5ai-art',
         labels={'A': S(20, 96, 168, 160, 184), 'B': S(20, 96, 197, 190, 213),
                 'C': S(20, 96, 227, 200, 243)},
         notes="The scheme prints '(i) Name Award 5 + 5 + 5 Marks'."),
    dict(key=(5, 'a', 'ii'),
         why='Scheme pp20-21 describe each process under its heading beside a '
             'labelled diagram; heading and paragraph are lifted apart and joined, '
             'leaving the callouts out, and the diagrams are shown with the answer. '
             '"(ii) Description Award 5 Marks" for any one.',
         topic='eng-1-9',
         lifted=[[join(S(20, 70, 352, 142, 368), S(20, 70, 572, 448, 647)),
                  join(S(21, 70, 73, 180, 91), S(21, 70, 265, 460, 340)),
                  join(S(21, 70, 412, 190, 430), S(21, 70, 619, 463, 665))]],
         marks=[5], total=5,
         question_figure='engineering-2026-OL-paper-q5ai-art',
         figure='engineering-2026-OL-scheme-q5aii-sol',
         notes="The scheme prints '(ii) Description Award 5 Marks'."),
    dict(key=(5, 'b', None), replaces=OWNED,
         why='Scheme p22 describes each in a paragraph under its name; the two whose '
             'paragraph does not open with the term (the scheme prints "Bridgeable '
             'plastics" for biodegradable, and "This describes" for elastic memory) '
             'are lifted with their heading. "Descriptions Award 5 + 5 Marks" for any '
             'two.',
         lifted=[[S(22, 81, 131, 458, 176),
                  join(S(22, 77, 185, 190, 201), S(22, 78, 199, 453, 274)),
                  S(22, 82, 297, 396, 313),
                  join(S(22, 78, 321, 162, 337), S(22, 81, 346, 431, 391))]],
         row_kind='anyN', group=(2, 5), marks=[10], tariff='fixed', total=10,
         notes="The scheme prints 'Descriptions Award 5 + 5 Marks'."),
    # ---- Question 6 ------------------------------------------------------
    dict(key=(6, 'a', None),
         replaces=NEW + 'named the parts at A-D with no label on the picture saying '
                  'which letter is which part',
         why='The four lathe parts are photographed and lettered A-D on p7; scheme p23 '
             'names each, "Lathe parts Award 5 + 5 + 5 Marks" for any three.',
         lifted=[[S(23, 106, 183, 300, 199), S(23, 106, 212, 196, 228),
                  S(23, 106, 241, 193, 257), S(23, 106, 271, 200, 287)]],
         row_kind='anyN', group=(3, 5), marks=[15], tariff='fixed', total=15,
         question_figure='engineering-2026-OL-paper-q6a-art',
         labels={'A': S(23, 141, 183, 300, 199), 'B': S(23, 141, 212, 196, 228),
                 'C': S(23, 141, 241, 193, 257), 'D': S(23, 141, 271, 200, 287)},
         notes="The scheme prints 'Lathe parts Award 5 + 5 + 5 Marks'."),
    dict(key=(6, 'b', None),
         why='Scheme p23 explains each term in a paragraph under its name, '
             '"Explanations Award 5 + 5 + 5 Marks" for any three; the list is one '
             'printed choice (FOLDED above).',
         lifted=[[S(23, 81, 358, 378, 404), S(23, 86, 446, 280, 477),
                  S(23, 89, 529, 350, 575), S(23, 89, 627, 338, 658)]],
         row_kind='anyN', group=(3, 5), marks=[15], tariff='fixed', total=15,
         notes="The scheme prints 'Explanations Award 5 + 5 + 5 Marks'."),
    dict(key=(6, 'c', 'i'),
         replaces=NEW + 'carried both OR branches\' questions and answers at one '
                  'branch\'s price, with no route between them',
         why='Both (c)s price their (i) at 6 (scheme p24): the knurling process, or '
             'what CNC means. One card for the printed OR, each branch a route of its '
             'own; each question is lifted with its cue.',
         question_lift=P(7, *_C6A, more=[(92, 403, 260, 419), _OR6P, _C6B,
                                         (92, 596, 205, 612)]), stem=False,
         lifted=[S(24, 85, 131, 449, 221), S(24, 48, 548, 455, 593)],
         marks=[6, 6], routes=['a', 'b'], total=6,
         question_figure='engineering-2026-OL-paper-q6c-crop', notes=_OR6),
    dict(key=(6, 'c', 'ii'),
         replaces=NEW + 'carried both OR branches\' questions and offered the CNC '
                  'branch\'s "3D printer" among the lathe processes, with no route',
         why='Both (c)s price their (ii) "Award 3 + 3 Marks" (scheme p24): two lathe '
             'processes, or two CNC machines. One card, each branch a route.',
         question_lift=P(7, *_C6A, more=[(92, 433, 343, 463), _OR6P, _C6B,
                                         (92, 626, 326, 656)]), stem=False,
         lifted=[S(24, 106, 281, 242, 297), S(24, 106, 310, 165, 326),
                 S(24, 106, 636, 160, 652), S(24, 106, 651, 165, 667)],
         marks=[3, 3, 3, 3], routes=['a', 'a', 'b', 'b'], total=6,
         question_figure='engineering-2026-OL-paper-q6c-crop', notes=_OR6),
    dict(key=(6, 'c', 'iii'),
         replaces=NEW + 'carried both OR branches\' questions and mixed their answers in '
                  'one any-two list, with no route',
         why='Both (c)s price their (iii) "Award 4 + 4 Marks" (scheme p24): two lathe '
             'safety features, or two advantages of CNC. One card, each branch a '
             'route.',
         question_lift=P(7, *_C6A, more=[(89, 475, 342, 507), _OR6P, _C6B,
                                         (89, 668, 320, 700)]), stem=False,
         lifted=[S(24, 106, 370, 441, 415), S(24, 106, 429, 451, 474),
                 S(24, 106, 711, 434, 741), S(24, 106, 741, 431, 771)],
         marks=[4, 4, 4, 4], routes=['a', 'a', 'b', 'b'], total=8,
         question_figure='engineering-2026-OL-paper-q6c-crop', notes=_OR6),
    # ---- Question 7 ------------------------------------------------------
    dict(key=(7, 'a', None),
         why='Scheme p25 explains each term in two lines under its name, '
             '"Descriptions Award 6 + 6 Marks" for any two.',
         topic='eng-3-12',
         lifted=[[S(25, 105, 167, 444, 197), S(25, 105, 230, 423, 261),
                  S(25, 105, 294, 431, 324)]],
         row_kind='anyN', group=(2, 6), marks=[12], tariff='fixed', total=12,
         notes="The scheme prints 'Descriptions Award 6 + 6 Marks'."),
    *[dict(key=(7, 'b', r),
           why='The pneumatic fitting is photographed with the body and hole '
               'dimensions on p8; each roman\'s question is lifted with (b)\'s cue. '
               'Scheme p25, "Calculations Award 5+5+5+5 Marks".',
           topic='eng-3-12', stem=False,
           question_lift=P(8, *_B7, more=[_STATE7, line]),
           lifted=[S(25, *ans)], marks=[5], total=5,
           question_figure='engineering-2026-OL-paper-q7b-crop',
           notes="The scheme prints 'Calculations Award 5+5+5+5 Marks'.")
      for r, line, ans in (
          ('i', (141, 217, 299, 233), (322, 369, 428, 385)),
          ('ii', (141, 239, 290, 255), (322, 394, 428, 410)),
          ('iii', (137, 259, 299, 276), (322, 418, 428, 434)),
          ('iv', (135, 281, 255, 298), (322, 443, 369, 459)))],
    dict(key=(7, 'c', 'i'),
         why='The instruments branch of (c): four instruments photographed and '
             'lettered A-D on p8. Scheme p25 names each, "(i) Name Award 3+3+3 Marks" '
             'for any three.',
         topic='eng-3-12',
         question_lift=P(8, 92, 347, 420, 363), stem=False,
         lifted=[[S(25, 106, 550, 252, 566), S(25, 106, 574, 190, 590),
                  S(25, 106, 599, 229, 615), S(25, 106, 623, 252, 639)]],
         row_kind='anyN', group=(3, 3), marks=[9], tariff='fixed', total=9,
         question_figure='engineering-2026-OL-paper-q7c-crop',
         labels={'A': S(25, 142, 550, 252, 566), 'B': S(25, 142, 574, 190, 590),
                 'C': S(25, 142, 599, 229, 615), 'D': S(25, 142, 623, 252, 639)},
         notes="The scheme prints '(i) Name Award 3+3+3 Marks'. " + _OR7),
    dict(key=(7, 'c', 'ii'),
         why='The instruments branch\'s (ii); scheme p25 answers in one line, "(ii) '
             'Explanation Award 5 Marks".',
         topic='eng-3-12',
         question_lift=P(8, 92, 523, 407, 541), stem=False,
         lifted=[S(25, 84, 670, 403, 686)], marks=[5], total=5,
         notes="The scheme prints '(ii) Explanation Award 5 Marks'. " + _OR7),
    dict(key=(7, 'c', 'iii'),
         why='The instruments branch\'s (iii); scheme p25 gives two advantages, '
             '"Two Advantages Award 2 + 2 Marks".',
         topic='eng-3-12',
         question_lift=P(8, 89, 553, 430, 570), stem=False,
         lifted=[S(25, 127, 724, 294, 740), S(25, 127, 749, 449, 765)],
         marks=[2, 2], total=4,
         notes="The scheme prints 'Two Advantages Award 2 + 2 Marks'. " + _OR7),
    dict(key=(7, 'c', 'i'), id='eng-2026-ol-q7-c-i-or', ref_note='555 timer PCB',
         why='The PCB branch\'s (i), lifted with its cue; scheme p26 lists nine '
             'components, "(i) Components Award 3 + 3 Marks" for any two.',
         topic='eng-2-16',
         question_lift=P(8, *_C7B, more=[(85, 659, 388, 675)]), stem=False,
         lifted=[[S(26, 127, 168, 178, 184), S(26, 127, 182, 163, 198),
                  S(26, 127, 197, 196, 213), S(26, 127, 212, 149, 228),
                  S(26, 127, 226, 159, 242), S(26, 127, 241, 179, 257),
                  S(26, 127, 256, 210, 272), S(26, 127, 270, 235, 286),
                  S(26, 127, 285, 210, 301)]],
         row_kind='anyN', group=(2, 3), marks=[6], tariff='fixed', total=6,
         question_figure='engineering-2026-OL-paper-q7c-or-crop',
         notes="The scheme prints '(i) Components Award 3 + 3 Marks'. " + _OR7),
    dict(key=(7, 'c', 'ii'), id='eng-2026-ol-q7-c-ii-or', ref_note='555 timer PCB',
         why='The PCB branch\'s (ii), lifted with its cue; scheme p26 answers in one '
             'sentence, "(ii) Benefit Award 6 Marks".',
         topic='eng-2-16',
         question_lift=P(8, *_C7B, more=[(92, 688, 340, 704)]), stem=False,
         lifted=[S(26, 93, 358, 440, 403)], marks=[6], total=6,
         question_figure='engineering-2026-OL-paper-q7c-or-crop',
         notes="The scheme prints '(ii) Benefit Award 6 Marks'. " + _OR7),
    dict(key=(7, 'c', 'iii'), id='eng-2026-ol-q7-c-iii-or', ref_note='555 timer PCB',
         why='The PCB branch\'s (iii), lifted with its cue; scheme p26 answers in one '
             'sentence, "(iii) Application Award 6 Marks".',
         topic='eng-2-16',
         question_lift=P(8, *_C7B, more=[(88, 717, 318, 733)]), stem=False,
         lifted=[S(26, 127, 461, 453, 491)], marks=[6], total=6,
         question_figure='engineering-2026-OL-paper-q7c-or-crop',
         notes="The scheme prints '(iii) Application Award 6 Marks'. " + _OR7),
]

TOPICS = {
    'eng-2026-ol-q3-b-ii': ('eng-2-6', 'identifying a heat treatment process is heat '
                            'treatment; "high carbon steel" outvoted it'),
    'eng-2026-ol-q3-b-iii': ('eng-2-6', 'identifying a heat treatment process is heat '
                             'treatment; "carbon steel" outvoted it'),
    'eng-2026-ol-q4-d-ii': ('eng-2-10', 'a method of joining copper pipes is joining; '
                            '"copper" outvoted it'),
}

_ROB = 'Energy, Electronics & Robotics'

ATLAS = {
    'eng-2026-ol-q1-g': dict(
        topics=[_ROB],
        note='Electrical conductors and a conducting material, which the reference files '
             'with Q1\'s electronics parts; the card\'s syllabus heading is Classification '
             'and origin of metals.'),
    **{k: dict(
        topics=['Materials: Properties and Uses'],
        note='Choosing a material for each labelled part of the mountain bike, and why; '
             'the card\'s syllabus heading is Technology, where the syllabus places the '
             'selection of materials.')
       for k in ('eng-2026-ol-q2-c-i', 'eng-2026-ol-q2-c-ii')},
    **{f'eng-2026-ol-q3-d-{p}': dict(
        topics=[_ROB],
        note='Robotics in workplace safety and manufacturing, and pneumatics (the OR '
             'branch of Q3(d)); the card\'s syllabus heading is Technology, where the '
             'syllabus places robotics.') for p in ('i', 'ii', 'iii')},
}
