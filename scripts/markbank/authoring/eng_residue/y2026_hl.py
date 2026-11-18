"""2026 Higher Level: the parts eng_all refuses or gets wrong, from the page.

Paper LC027ALP000EV; scheme pages as the PDF numbers them. The marks grid is
on scheme p6 (Question 1 "Any ten @ 5 marks each"). This sitting had no cards
before the lane: every card here is new, and a `replaces=` names the
automatic card it rebuilds before it ever shipped.
"""
from eng_lift import join, lift

Y, L = 2026, 'hl'
NEW = 'never shipped: the automatic card '


def S(page, *rect):
    return lift(Y, L, 'scheme', page, rect)


def P(page, *rect, more=()):
    return lift(Y, L, 'paper', page, rect, more=more)


# Paper p8: Question 6's two (c)s; p10: Question 8's; p11: Question 9's.
_C6A = (90, 456, 422, 472)           # "Welding defects include porosity, cracking and incomplete fusion."
_C6B = (90, 628, 396, 661)           # "The Dexai robotic arm shown is a collaborative robot ..."
_C8A = (90, 458, 323, 474)           # "Face milling is a common machining process."
_C8B = (90, 622, 322, 652)           # "CNC machines have revolutionised engineering practices ..."
_C9A = (90, 467, 367, 500)           # "The Easyrig camera system shown opposite ..."
_C9B = (90, 650, 423, 683)           # "The outdoor wall light shown includes ..."
_OR8 = ('The paper sets this (c) as the alternative, after an OR, to "(c) Face milling is a '
        'common machining process".')
_OR6 = ('The paper sets two (c)s either side of an OR, welding defects and the Dexai robotic '
        'arm; the scheme prices their (i)s and (ii)s differently, so each branch is a card '
        'of its own.')

CROPS = {
    # Paper p3: the Wash+Dry tap with both its labels (the automatic crop
    # clipped "dryer").
    'engineering-2026-HL-paper-q1f-crop': dict(
        doc='paper', page=3, rect=(437, 312, 566, 432), ref='2026 HL Q1(f)'),
    'engineering-2026-HL-paper-q1i-crop': dict(
        doc='paper', page=3, rect=(435, 473, 566, 574), ref='2026 HL Q1(i)'),
    # Paper p5: (b)'s sentence and its table of tensile results, as printed.
    'engineering-2026-HL-paper-q3b-crop': dict(
        doc='paper', page=5, rect=(64, 370, 560, 460), ref='2026 HL Q3(b)'),
    # Paper p6: (a)'s sentence and its table of the two axes' treatments.
    'engineering-2026-HL-paper-q4a-crop': dict(
        doc='paper', page=6, rect=(64, 86, 400, 182), ref='2026 HL Q4(a)'),
    # Paper p6: the iron-carbon diagram with its axes and letters.
    'engineering-2026-HL-paper-q4b-crop': dict(
        doc='paper', page=6, rect=(96, 326, 460, 533), ref='2026 HL Q4(b)',
        letters=('A', 'B', 'C', 'D', 'X', 'Y')),
    # Paper p7: (b)'s sentence and its table of solidification temperatures.
    'engineering-2026-HL-paper-q5b-crop': dict(
        doc='paper', page=7, rect=(64, 300, 575, 414), ref='2026 HL Q5(b)'),
    'engineering-2026-HL-paper-q6a-crop': dict(
        doc='paper', page=8, rect=(420, 76, 566, 268), ref='2026 HL Q6(a)'),
    'engineering-2026-HL-paper-q6c-crop': dict(
        doc='paper', page=8, rect=(388, 445, 568, 582), mask=[(386, 445, 424, 474)],
        ref='2026 HL Q6(c)'),
    'engineering-2026-HL-paper-q6c-or-crop': dict(
        doc='paper', page=8, rect=(432, 625, 562, 735), ref='2026 HL Q6(c) OR'),
    'engineering-2026-HL-paper-q7bv-crop': dict(
        doc='paper', page=9, rect=(420, 452, 572, 560), ref='2026 HL Q7(b)(v)'),
    'engineering-2026-HL-paper-q7ciii-crop': dict(
        doc='paper', page=9, rect=(402, 602, 560, 758), ref='2026 HL Q7(c)(iii)'),
    'engineering-2026-HL-paper-q8ci-crop': dict(
        doc='paper', page=10, rect=(378, 450, 520, 576), ref='2026 HL Q8(c)(i)'),
    'engineering-2026-HL-paper-q9aii-crop': dict(
        doc='paper', page=11, rect=(395, 176, 562, 296), ref='2026 HL Q9(a)(ii)'),
    # Paper p11: the Easyrig beside the wall light, the two (c)s' pictures.
    'engineering-2026-HL-paper-q9c-crop': dict(
        doc='paper', page=11, parts=[(11, (380, 432, 566, 628)),
                                     (11, (410, 640, 566, 770))],
        mask=[(406, 645, 424, 690)], layout='row', ref='2026 HL Q9(c)'),
    # Scheme crops: each answer's own drawing.
    'engineering-2026-HL-scheme-q1c-sol': dict(
        doc='scheme', page=7, rect=(340, 515, 525, 682), solution=True,
        ref='2026 HL Q1(c)'),
    'engineering-2026-HL-scheme-q1d-sol': dict(
        doc='scheme', page=8, rect=(330, 80, 545, 175), solution=True,
        ref='2026 HL Q1(d)'),
    'engineering-2026-HL-scheme-q1e-sol': dict(
        doc='scheme', page=8, rect=(75, 222, 530, 306), solution=True,
        ref='2026 HL Q1(e)'),
    'engineering-2026-HL-scheme-q2d-sol': dict(
        doc='scheme', page=11, rect=(94, 420, 540, 590), solution=True,
        ref='2026 HL Q2(d)'),
    'engineering-2026-HL-scheme-q3bi-sol': dict(
        doc='scheme', page=14, rect=(120, 78, 520, 484), solution=True,
        ref='2026 HL Q3(b)(i)'),
    'engineering-2026-HL-scheme-q3bii-sol': dict(
        doc='scheme', page=14, rect=(94, 528, 472, 578), solution=True,
        ref='2026 HL Q3(b)(ii)'),
    'engineering-2026-HL-scheme-q4biii-sol': dict(
        doc='scheme', page=17, parts=[(17, (104, 56, 520, 212)), (17, (160, 294, 480, 378))],
        solution=True,
        ref='2026 HL Q4(b)(iii)'),
    'engineering-2026-HL-scheme-q5bi-sol': dict(
        doc='scheme', page=18, rect=(100, 478, 470, 760), solution=True,
        ref='2026 HL Q5(b)(i)'),
    'engineering-2026-HL-scheme-q5bii-sol': dict(
        doc='scheme', page=19, rect=(120, 58, 440, 112), solution=True,
        ref='2026 HL Q5(b)(ii)'),
    'engineering-2026-HL-scheme-q5biii-sol': dict(
        doc='scheme', page=19, rect=(185, 176, 480, 300), solution=True,
        ref='2026 HL Q5(b)(iii)'),
    'engineering-2026-HL-scheme-q8bi-sol': dict(
        doc='scheme', page=26, rect=(355, 235, 560, 440), solution=True,
        ref='2026 HL Q8(b)(i)'),
    'engineering-2026-HL-scheme-q9ai-sol': dict(
        doc='scheme', page=28, parts=[(28, (180, 120, 545, 240)), (28, (200, 455, 545, 592))],
        solution=True,
        ref='2026 HL Q9(a)(i)'),
    'engineering-2026-HL-scheme-q9aii-sol': dict(
        doc='scheme', page=29, rect=(50, 60, 545, 258), solution=True,
        ref='2026 HL Q9(a)(ii)'),
    'engineering-2026-HL-scheme-q9bv-sol': dict(
        doc='scheme', page=30, rect=(390, 50, 545, 160), solution=True,
        ref='2026 HL Q9(b)(v)'),
    'engineering-2026-HL-scheme-q9ci-sol': dict(
        doc='scheme', page=30, rect=(90, 276, 540, 748), solution=True,
        ref='2026 HL Q9(c)(i)'),
    'engineering-2026-HL-scheme-q9cii-sol': dict(
        doc='scheme', page=31, rect=(350, 365, 560, 478), solution=True,
        ref='2026 HL Q9(c)(ii)'),
}

CARDS = [
    # ---- Question 1 ------------------------------------------------------
    dict(key=(1, 'a', None),
         why='QR codes in engineering name no syllabus heading the topic rules '
             'know; they are information technology, under Technology. Scheme '
             'p7 lists three advantages for "3 + 2".',
         topic='eng-3-14', stem=True,
         lifted=[S(7, 94, 218, 520, 268), S(7, 94, 269, 520, 302),
                 S(7, 94, 303, 520, 319)],
         tariff='orderedSplit', notation='3 + 2', ladder=5),
    dict(key=(1, 'c', None),
         why='Magnetic separation of an ore names no syllabus heading the topic '
             'rules know; it is the extraction of iron, under Ferrous metals. '
             'Scheme p7 answers in one paragraph beside a labelled diagram, "5".',
         topic='eng-1-4', stem=True,
         lifted=[S(7, 94, 556, 332, 655)], marks=[5], total=5,
         figure='engineering-2026-HL-scheme-q1c-sol'),
    dict(key=(1, 'd', None),
         why='"the lifting platform shown" is photographed beside (d); scheme p8 '
             'answers in one paragraph beside a diagram whose label "Hydraulic '
             'cylinder" the reader welds into it. "5".',
         stem=True, lifted=[S(8, 94, 88, 320, 137)], marks=[5], total=5,
         question_figure='engineering-2026-HL-paper-q1d-art',
         figure='engineering-2026-HL-scheme-q1d-sol'),
    dict(key=(1, 'e', None),
         replaces=NEW + 'read the scheme\'s two columns across, "A clearance fit has '
                  'a gap between the parts An interference fit requires force to '
                  'allow allowing them to move freely."',
         why='Scheme p8 answers in two columns under two drawings; each column is '
             'lifted by its own rectangle. "5".',
         stem=True,
         lifted=[S(8, 72, 306, 292, 338), S(8, 296, 306, 530, 338)],
         tariff='questionTotal', total=5,
         figure='engineering-2026-HL-scheme-q1e-sol',
         notes="The scheme prints '5'."),
    dict(key=(1, 'f', None),
         topic='eng-3-14',
         why='"The Dyson Airblade Wash+Dry hand dryer, shown opposite" is '
             'photographed with "tap" and "dryer" labelled; the automatic crop '
             'clipped "dryer". Scheme p8 lists five attributes for "3 + 2".',
         stem=True,
         lifted=[S(8, 94, 390, 500, 406), S(8, 94, 407, 500, 423),
                 S(8, 94, 424, 500, 441), S(8, 94, 442, 500, 458),
                 S(8, 94, 459, 500, 475)],
         tariff='orderedSplit', notation='3 + 2', ladder=5,
         question_figure='engineering-2026-HL-paper-q1f-crop'),
    dict(key=(1, 'g', None),
         topic='eng-1-4',
         why='"the Wash+Dry appliance shown" is the same photograph; scheme p8 '
             'names the material and justifies it, "3 + 2".',
         stem=True,
         lifted=[S(8, 94, 527, 300, 543), S(8, 94, 544, 532, 609)],
         marks=[3, 2], total=5,
         question_figure='engineering-2026-HL-paper-q1f-crop'),
    dict(key=(1, 'i', None),
         topic='eng-3-14',
         why='"the lounge chair shown" is photographed and captioned beside (i); '
             'scheme p9 lists three benefits for "3 + 2".',
         stem=True,
         lifted=[S(9, 116, 172, 530, 205), S(9, 116, 206, 530, 239),
                 S(9, 116, 240, 530, 256)],
         tariff='orderedSplit', notation='3 + 2', ladder=5,
         question_figure='engineering-2026-HL-paper-q1i-crop'),
    # ---- Question 2 ------------------------------------------------------
    dict(key=(2, 'a', None),
         why='Smartphone functions that depend on semiconductors are the special '
             'topic (semiconductor technology), under Electronics. Scheme p10 '
             'lists seven for "4 + 3 + 3".',
         topic='eng-2-16',
         lifted=[S(10, 128, 122, 540, 155), S(10, 128, 156, 540, 172),
                 S(10, 128, 173, 540, 189), S(10, 128, 190, 540, 206),
                 S(10, 128, 207, 540, 224), S(10, 128, 225, 540, 241),
                 S(10, 128, 242, 540, 258)],
         tariff='orderedSplit', notation='4 + 3 + 3', ladder=10),
    dict(key=(2, 'd', None),
         replaces=NEW + 'opened its second row with the diagram\'s label "Depletion '
                  'region", welded into "N-type doping adds atoms like '
                  'phosphorus ..."',
         why='Scheme p11 answers in three paragraphs either side of a labelled '
             'diagram; each is lifted by its own rectangle and the diagram is shown '
             'with the answer. "10".',
         lifted=[S(11, 94, 356, 540, 422), S(11, 94, 591, 540, 673),
                 S(11, 94, 673, 540, 756)],
         tariff='questionTotal', total=10,
         figure='engineering-2026-HL-scheme-q2d-sol',
         notes="The scheme prints '10'."),
    # ---- Question 3 ------------------------------------------------------
    dict(key=(3, 'b', 'i'),
         why='Scheme p14 answers "Stress-strain graph" with the graph and prints no '
             'words; the table of results is shown as printed.',
         special={'kind': 'ask'}, total=10, stem=False,
         question_figure='engineering-2026-HL-paper-q3b-crop',
         figure='engineering-2026-HL-scheme-q3bi-sol',
         notes="The scheme prints 'Stress-strain graph', 10 marks."),
    dict(key=(3, 'b', 'ii'),
         why='Scheme p14 sets Young\'s Modulus = stress / strain = 110 / 1.25 = '
             '88 kN/mm2 as stacked fractions.',
         special={'kind': 'ask'}, total=4, stem=False,
         question_figure='engineering-2026-HL-paper-q3b-crop',
         figure='engineering-2026-HL-scheme-q3bii-sol'),
    dict(key=(3, 'b', 'iii'),
         replaces=NEW + 'carried the results table as a line of numbers over a part '
                  'that does not use it',
         why='Scheme p14 answers in one paragraph and two sentences; "4".',
         stem=False,
         lifted=[S(14, 120, 614, 510, 647), S(14, 120, 647, 395, 697),
                 S(14, 120, 697, 395, 746)],
         tariff='questionTotal', total=4, notes="The scheme prints '4'."),
    # ---- Question 4 ------------------------------------------------------
    *[dict(key=(4, 'a', r),
           replaces=NEW + 'showed the axe photograph but not the table that sets out '
                    'how axes A and B were treated, which the part depends on',
           why='The two treatments are printed as a table under (a)\'s sentence on '
               'p6; the table is shown as printed.',
           stem=False, lifted=rows, **price,
           question_figure='engineering-2026-HL-paper-q4a-crop')
      for r, rows, price in (
          ('i', [S(16, 115, 94, 430, 158), S(16, 115, 160, 430, 226)],
           dict(tariff='questionTotal', total=4, notes="The scheme prints '4'.")),
          ('ii', [S(16, 114, 260, 152, 276),
                  join(S(16, 153, 260, 515, 276), S(16, 115, 277, 528, 293))],
           dict(marks=[2, 6], total=8)),
          ('iii', [S(16, 116, 344, 530, 377), S(16, 115, 377, 535, 410)],
           dict(marks=[2, 2], total=4)))],
    dict(key=(4, 'b', 'i'),
         why='The iron-carbon diagram is printed with its regions lettered A-D; '
             'scheme p16 names each, "1 + 1 + 1 + 1".',
         lifted=[S(16, 114, 444, 300, 460), S(16, 114, 461, 300, 477),
                 S(16, 114, 478, 300, 494), S(16, 114, 495, 300, 511)],
         marks=[1, 1, 1, 1], total=4, figure='engineering-2026-HL-paper-q4b-crop',
         labels={'A': S(16, 134, 444, 300, 460), 'B': S(16, 134, 461, 300, 477),
                 'C': S(16, 134, 478, 300, 494), 'D': S(16, 134, 495, 300, 511)}),
    dict(key=(4, 'b', 'ii'),
         why='Points X and Y are marked on the same diagram; scheme p16 names each '
             'and explains it, "Identify 2 + 2, Explain 2 + 2".',
         lifted=[S(16, 114, 545, 287, 561),
                 join(S(16, 287, 545, 527, 561), S(16, 114, 562, 527, 594)),
                 S(16, 114, 595, 293, 611),
                 join(S(16, 293, 595, 527, 611), S(16, 114, 611, 527, 627))],
         marks=[2, 2, 2, 2], total=8,
         question_figure='engineering-2026-HL-paper-q4b-crop',
         labels={'X': S(16, 194, 545, 287, 561), 'Y': S(16, 193, 595, 293, 611)},
         notes="The scheme prints 'Identify 2 + 2, Explain 2 + 2'."),
    dict(key=(4, 'b', 'iii'),
         replaces=NEW + 'carried the diagram\'s labels and axis numbers as its stem '
                  'and the pyrometer drawing\'s captions "Temperature too low '
                  'Correct Temperature too high" as a row',
         why='Scheme pp16-17 answer in two paragraphs around a drawing of the '
             'optical pyrometer and its three filament views; the drawing is shown '
             'with the answer. "6".',
         stem=False,
         lifted=[S(16, 114, 679, 530, 728), S(17, 114, 228, 525, 294)],
         tariff='questionTotal', total=6,
         figure='engineering-2026-HL-scheme-q4biii-sol',
         notes="The scheme prints '6'."),
    # ---- Question 5 ------------------------------------------------------
    dict(key=(5, 'b', 'i'),
         why='Scheme p18 answers with the equilibrium diagram, priced "8 + 1 + 1": '
             'the diagram under its heading, then the liquidus and solidus labelled '
             'on it. The table is shown as printed.',
         lifted=[S(18, 115, 460, 415, 476), S(18, 216, 508, 287, 524),
                 S(18, 363, 582, 428, 598)],
         row_kind='criterion', marks=[8, 1, 1], total=10, stem=False,
         question_figure='engineering-2026-HL-paper-q5b-crop',
         figure='engineering-2026-HL-scheme-q5bi-sol',
         notes="The scheme prints '8 + 1 + 1'."),
    dict(key=(5, 'b', 'ii'),
         why='The diagram is the candidate\'s own from (b)(i); scheme p19 reads the '
             'masses off it as stacked fractions, "4".',
         special={'kind': 'ask'}, total=4, stem=False, topic='eng-1-3',
         question_figure='engineering-2026-HL-paper-q5b-crop',
         figure='engineering-2026-HL-scheme-q5bii-sol'),
    dict(key=(5, 'b', 'iii'),
         why='Scheme p19 answers with the cooling curve and one sentence of its two '
             'temperatures, "4"; the table is shown as printed.',
         stem=False, topic='eng-1-3',
         lifted=[S(19, 120, 144, 525, 177)], marks=[4], total=4,
         question_figure='engineering-2026-HL-paper-q5b-crop',
         figure='engineering-2026-HL-scheme-q5biii-sol'),
    dict(key=(5, 'c', 'iii'),
         why='Cold working names no syllabus heading the topic rules know; its '
             'effect on the internal structure (dislocations, strain hardening) is '
             'the structure of metals. Scheme p19, "Any two @ 8 + 8".',
         topic='eng-1-3',
         lifted=[S(19, 108, 696, 540, 762)], marks=[8], total=8,
         notes="The scheme prints 'Any two @ 8 + 8'."),
    # ---- Question 6 ------------------------------------------------------
    dict(key=(6, 'a', 'i'),
         why='"the lighting truss shown" is photographed and labelled beside (a); '
             'scheme p20 gives two reasons, "2 + 2".',
         lifted=[S(20, 126, 110, 535, 160), S(20, 126, 161, 535, 211)],
         marks=[2, 2], total=4,
         question_figure='engineering-2026-HL-paper-q6a-crop'),
    dict(key=(6, 'a', 'ii'),
         replaces=NEW + 'set "Name 2, Reason 2" as one 4-mark total',
         why='Scheme p20 names the process and gives a reason, "Name 2, Reason 2".',
         lifted=[S(20, 115, 245, 410, 261), S(20, 115, 262, 505, 311)],
         marks=[2, 2], total=4),
    dict(key=(6, 'b', 'i'),
         replaces=NEW + 'showed (b)(ii)\'s welding helmet, which (b)(i) does not '
                  'mention',
         why='Scheme p21 answers in two paragraphs, priced by (b)\'s "Any three @ '
             '6 + 6 + 6".',
         lifted=[S(21, 108, 60, 532, 109), S(21, 108, 110, 532, 159)],
         tariff='questionTotal', total=6,
         notes="The scheme prints 'Any three @ 6 + 6 + 6'."),
    dict(key=(6, 'c', 'i'),
         replaces=NEW + 'carried both OR branches\' questions and answers at the '
                  'first branch\'s total, with the scheme\'s tariff "Methods 2 + 2" '
                  'as one of its rows',
         why='The welding-defects branch\'s (i), lifted with its cue; scheme p22 '
             'prices it "Meaning 6, Methods 2 + 2".',
         question_lift=P(8, *_C6A, more=[(120, 478, 370, 528)]), stem=False,
         lifted=[S(22, 105, 60, 535, 109), S(22, 115, 127, 535, 160),
                 S(22, 115, 160, 535, 193)],
         marks=[6, 2, 2], total=10,
         question_figure='engineering-2026-HL-paper-q6c-crop', notes=_OR6),
    dict(key=(6, 'c', 'i'), id='eng-2026-hl-q6-c-i-or', ref_note='robotic arms',
         why='The robotic-arm branch\'s (i), lifted with its cue; scheme p22 lists '
             'three areas, "4 + 4".',
         question_lift=P(8, *_C6B, more=[(120, 668, 404, 701)]), stem=False,
         lifted=[[S(22, 104, 412, 540, 445), S(22, 104, 446, 540, 479),
                  S(22, 104, 480, 540, 529)]],
         row_kind='anyN', group=(2, 4), marks=[8], tariff='fixed', total=8,
         question_figure='engineering-2026-HL-paper-q6c-or-crop', notes=_OR6),
    dict(key=(6, 'c', 'ii'),
         replaces=NEW + 'carried both OR branches\' questions and answers, and the '
                  'photograph\'s caption "Dexai robotic arm" ran into the second '
                  'branch\'s terms',
         why='The welding-defects branch\'s (ii): cracks OR incomplete fusion, '
             'either one; scheme p22, "6".',
         question_lift=P(8, *_C6A, more=[(120, 536, 376, 568)]), stem=False,
         lifted=[[S(22, 108, 245, 540, 277), S(22, 108, 278, 540, 327)]],
         marks=[6], total=6,
         question_figure='engineering-2026-HL-paper-q6c-crop', notes=_OR6),
    dict(key=(6, 'c', 'ii'), id='eng-2026-hl-q6-c-ii-or', ref_note='robotic arms',
         why='The robotic-arm branch\'s (ii), lifted with its cue and its two '
             'terms (the caption printed beside them left out); scheme p22 explains '
             'each, "4 + 4".',
         question_lift=P(8, *_C6B, more=[(120, 707, 430, 758)]), stem=False,
         lifted=[S(22, 100, 564, 380, 662), S(22, 100, 663, 512, 746)],
         marks=[4, 4], total=8,
         question_figure='engineering-2026-HL-paper-q6c-or-crop', notes=_OR6),
    # ---- Question 7 ------------------------------------------------------
    dict(key=(7, 'b', 'iii'),
         why='Scheme p24 answers in two columns, linear beside cross-linked; each '
             'is lifted by its own rectangle. "Any three @ 6 + 6 + 6".',
         lifted=[S(24, 106, 136, 290, 303), S(24, 316, 136, 490, 303)],
         tariff='questionTotal', total=6,
         notes="The scheme prints 'Any three @ 6 + 6 + 6'."),
    dict(key=(7, 'b', 'v'),
         replaces=NEW + 'showed (b)(i)\'s machine guard as "the mulch film shown"',
         why='The mulch film is photographed and labelled beside (b)(v); scheme '
             'p24 lists four reasons.',
         lifted=[S(24, 108, 570, 530, 604), S(24, 108, 604, 530, 638),
                 S(24, 108, 638, 530, 672), S(24, 108, 672, 530, 706)],
         tariff='questionTotal', total=6,
         question_figure='engineering-2026-HL-paper-q7bv-crop',
         notes="The scheme prints 'Any three @ 6 + 6 + 6'."),
    dict(key=(7, 'c', 'iii'),
         why='"the saddle seat shown" is photographed beside (c); scheme p25 lists '
             'four advantages for "3 + 3".',
         lifted=[S(25, 101, 244, 535, 277), S(25, 101, 278, 535, 294),
                 S(25, 101, 295, 535, 311), S(25, 101, 312, 535, 328)],
         tariff='orderedSplit', notation='3 + 3', ladder=6,
         question_figure='engineering-2026-HL-paper-q7ciii-crop'),
    # ---- Question 8 ------------------------------------------------------
    dict(key=(8, 'a', 'i'),
         why='Scheme p25 describes loading and glazing in two paragraphs beside a '
             'drawing whose label "Loading" the reader welds in; "6".',
         lifted=[S(25, 87, 430, 400, 496), S(25, 87, 530, 400, 613)],
         tariff='questionTotal', total=6, notes="The scheme prints '6'."),
    dict(key=(8, 'b', 'i'),
         why='Forming and generating name no syllabus heading the topic rules know; '
             'they are machining. Scheme p26 answers in two paragraphs beside '
             'labelled drawings, shown with the answer.',
         topic='eng-2-11',
         lifted=[S(26, 90, 248, 350, 298), S(26, 90, 366, 350, 432)],
         tariff='questionTotal', total=6,
         figure='engineering-2026-HL-scheme-q8bi-sol',
         notes="The scheme prints 'Any three @ 6 + 6 + 6'."),
    dict(key=(8, 'c', None),
         why='Paper p10 sets two (c)s either side of an OR. This card is the second '
             'branch, the four CNC features, which has no romans of its own; scheme '
             'p27 describes each, "4 + 4 + 4 + 4".',
         topic='eng-2-11', question_lift=P(10, *_C8B, more=[(90, 659, 310, 739)]),
         lifted=[S(27, 72, 602, 530, 633), S(27, 72, 632, 530, 663),
                 S(27, 72, 662, 530, 692), S(27, 72, 692, 530, 722)],
         marks=[4, 4, 4, 4], total=16, stem=False, notes=_OR8),
    dict(key=(8, 'c', 'i'),
         replaces=NEW + 'carried the OR branch\'s CNC question and the photograph\'s '
                  'caption as its stem',
         why='The face-milling branch\'s (i), lifted with its cue; the cutting tool '
             'is photographed beside it. Scheme p27, "8".',
         question_lift=P(10, *_C8A, more=[(120, 483, 330, 514)]), stem=False,
         lifted=[S(27, 94, 144, 510, 210), S(27, 94, 210, 345, 243),
                 S(27, 94, 244, 345, 277), S(27, 94, 278, 345, 311),
                 S(27, 94, 329, 350, 378)],
         tariff='questionTotal', total=8,
         question_figure='engineering-2026-HL-paper-q8ci-crop',
         notes="The scheme prints '8'. " + _OR8.replace('this (c) as the alternative, '
               'after an OR, to "(c) Face milling is a common machining process"',
               'a second (c), on CNC features, after an OR')),
    dict(key=(8, 'c', 'ii'),
         replaces=NEW + 'carried the OR branch\'s CNC question and the photograph\'s '
                  'caption as its stem',
         why='The face-milling branch\'s (ii), lifted with its cue; scheme p27, '
             '"4 + 4".',
         question_lift=P(10, *_C8A, more=[(120, 521, 330, 576)]), stem=False,
         lifted=[S(27, 94, 446, 380, 496), S(27, 94, 496, 380, 546)],
         marks=[4, 4], total=8,
         notes='The paper sets a second (c), on CNC features, after an OR.'),
    # ---- Question 9 ------------------------------------------------------
    dict(key=(9, 'a', 'i'),
         why='Scheme p28 answers in two paragraphs under a labelled drawing of the '
             'conveyor, whose labels the reader welds in; the drawing is shown with '
             'the answer. "8".',
         lifted=[S(28, 94, 245, 540, 310), S(28, 94, 328, 540, 443)],
         tariff='questionTotal', total=8,
         figure='engineering-2026-HL-scheme-q9ai-sol',
         notes="The scheme prints '8'."),
    dict(key=(9, 'a', 'ii'),
         why='"the can crusher shown opposite" is photographed and captioned; scheme '
             'pp28-29 answer with a crank and slider, a paragraph and a "Suggested '
             'solution" drawing. "8".',
         lifted=[S(28, 94, 645, 540, 761)], marks=[8], total=8,
         question_figure='engineering-2026-HL-paper-q9aii-crop',
         figure='engineering-2026-HL-scheme-q9aii-sol',
         notes="The scheme prints 'Suggested solution - other viable solutions are "
               "acceptable', 8 marks."),
    dict(key=(9, 'b', 'i'),
         replaces=NEW + 'showed (b)(iii)\'s universal joint, which (b)(i) does not '
                  'mention',
         why='Scheme p29 answers in two paragraphs, priced by (b)\'s "Any three @ '
             '6 + 6 + 6".',
         lifted=[S(29, 94, 325, 385, 374), S(29, 94, 375, 385, 424)],
         tariff='questionTotal', total=6,
         notes="The scheme prints 'Any three @ 6 + 6 + 6'."),
    dict(key=(9, 'b', 'v'),
         replaces='never shipped: the automatic author builds this card only from the '
                  'lifts this entry records, so the entry owns it',
         why='Scheme pp29-30 answer in two paragraphs over the page break beside a '
             'drawing labelled "worm" and "gear"; the drawing is shown with the '
             'answer.',
         lifted=[S(29, 94, 725, 495, 758), S(30, 94, 60, 385, 142)],
         tariff='questionTotal', total=6,
         figure='engineering-2026-HL-scheme-q9bv-sol',
         notes="The scheme prints 'Any three @ 6 + 6 + 6'."),
    dict(key=(9, 'c', 'i'),
         why='Both (c)s price their (i) at 8 (scheme pp30-31): the camera boom, a '
             '"Suggested solution" with its drawing, or the wall light\'s energy '
             'conversions in one paragraph ("4 + 4"). One card for the printed OR, '
             'each branch a route of its own.',
         topic='eng-2-15',
         question_lift=P(11, *_C9A, more=[(120, 511, 362, 556), (290, 618, 315, 636),
                                          _C9B, (120, 690, 366, 720)]),
         lifted=[S(30, 88, 194, 530, 226), S(31, 94, 261, 535, 326)],
         marks=[8, 8], routes=['a', 'b'], total=8, stem=False,
         question_figure='engineering-2026-HL-paper-q9c-crop',
         figure='engineering-2026-HL-scheme-q9ci-sol',
         notes="The paper sets two (c)s either side of an OR. The scheme prints '8' "
               "for the camera boom, a suggested solution ('other viable solutions "
               "are acceptable'), and '4 + 4' for the wall light's conversions."),
    dict(key=(9, 'c', 'ii'),
         why='Both (c)s price their (ii) at 8 (scheme p31): two Easyrig features, '
             '"4 + 4", or the LDR\'s purpose in one paragraph beside its graph, '
             '"8". One card for the printed OR, each branch a route of its own.',
         topic='eng-2-16',
         question_lift=P(11, *_C9A, more=[(120, 560, 368, 592), (290, 618, 315, 636),
                                          _C9B, (120, 725, 340, 755)]),
         lifted=[S(31, 94, 94, 535, 143), S(31, 94, 143, 540, 193),
                 S(31, 94, 361, 345, 509)],
         marks=[4, 4, 8], routes=['a', 'a', 'b'], total=8, stem=False,
         question_figure='engineering-2026-HL-paper-q9c-crop',
         figure='engineering-2026-HL-scheme-q9cii-sol',
         notes="The paper sets two (c)s either side of an OR; the scheme prints "
               "'4 + 4' for the Easyrig features and '8' for the LDR."),
]

TOPICS = {
    'eng-2026-hl-q4-c-i': ('eng-2-6', 'annealing silver is heat treatment; "silver" '
                           'outvoted it'),
    'eng-2026-hl-q5-a-ii': ('eng-3-7', 'sacrificial protection is corrosion; "bronze" '
                            'outvoted it'),
    'eng-2026-hl-q7-b-i': ('eng-1-9', 'the properties of polycarbonate are plastics; '
                           '"machine guard" outvoted it'),
}

_SEMI = ('Semiconductor technology, the 2026 Higher special topic, which the reference '
         'files Q2 under; the card\'s syllabus heading is Electronics.')

ATLAS = {
    **{f'eng-2026-hl-q2-{p}': dict(topics=['Q2 - Special Topic'], note=_SEMI)
       for p in ('a', 'b-i', 'b-ii', 'c-i', 'c-ii', 'd', 'e-ii')},
    'eng-2026-hl-q3-a-iii': dict(
        topics=['Testing of Materials and Products'],
        note='Torsional forces and fatigue in the crankshaft, which the reference files '
             'with the rest of Q3 under testing; the card\'s syllabus heading is '
             'Mechanisms.'),
    'eng-2026-hl-q3-c-i': dict(
        topics=['Testing of Materials and Products'],
        note='Quality control of motorcycle components, which the reference files Q3(c) '
             'under; the card\'s syllabus heading is Manufacturing processes.'),
    'eng-2026-hl-q4-c-iii': dict(
        topics=['Materials: Properties and Uses'],
        note='Applications of cast iron and why: a material\'s properties and uses. The '
             'reference files Q4 under heat treatment and equilibrium diagrams only.'),
    'eng-2026-hl-q5-a-i': dict(
        topics=['Corrosion of Metals'],
        note='Why bronze suits a ship\'s propeller (corrosion resistance in seawater '
             'first), which the reference files Q5(a) under; the card\'s syllabus '
             'heading is Non-ferrous metals.'),
    'eng-2026-hl-q6-a-i': dict(
        topics=['Materials: Properties and Uses'],
        note='Why tubular aluminium suits the truss: a material\'s properties and uses. '
             'The reference files Q6 under welding only.'),
}
