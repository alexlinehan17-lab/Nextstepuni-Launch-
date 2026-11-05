"""2025 Higher Level: the parts eng_all refuses or gets wrong, from the page.

Paper LC027ALP000EV; scheme pages as the PDF numbers them. The marks grid is
on scheme p6 (Question 1 "Any ten @ 5 marks each").
"""
from eng_lift import lift

Y, L = 2025, 'hl'


def S(page, *rect):
    return lift(Y, L, 'scheme', page, rect)


def P(page, *rect, more=()):
    return lift(Y, L, 'paper', page, rect, more=more)


# Paper p11: the two (c)s of Question 9 either side of the OR.
_CA = (86, 447, 370, 479)            # "(c) Various mechanisms are used in the 3D printer ..."
_OR9 = (290, 626, 315, 644)          # "OR"
_CB = (86, 660, 357, 693)            # "(c) An Irish company EnergyServ ..."

CROPS = {
    'engineering-2025-HL-paper-q1m-crop': dict(
        doc='paper', page=3, rect=(442, 704, 560, 786), ref='2025 HL Q1(m)'),
    # Paper p5: (b)'s sentence and its table of tensile results, as printed.
    'engineering-2025-HL-paper-q3b-crop': dict(
        doc='paper', page=5, rect=(64, 324, 545, 424), ref='2025 HL Q3(b)'),
    'engineering-2025-HL-paper-q5a-crop': dict(
        doc='paper', page=7, rect=(388, 104, 556, 270), ref='2025 HL Q5(a)',
        letters=('A', 'B', 'C')),
    # Paper p7: (b)'s two sentences and its table of solidification temperatures.
    'engineering-2025-HL-paper-q5b-crop': dict(
        doc='paper', page=7, rect=(64, 294, 552, 430), ref='2025 HL Q5(b)'),
    'engineering-2025-HL-paper-q5c-crop': dict(
        doc='paper', page=7, rect=(288, 612, 566, 760), ref='2025 HL Q5(c)'),
    'engineering-2025-HL-paper-q7bi-crop': dict(
        doc='paper', page=9, rect=(440, 340, 562, 433), ref='2025 HL Q7(b)(i)'),
    # Paper p11: the 3D printer with its limit switch, beside the solar
    # carport, the two (c)s' pictures side by side; the ends of the first
    # (c)'s own lines run into its box and are whited out.
    'engineering-2025-HL-paper-q9c-crop': dict(
        doc='paper', page=11, parts=[(11, (334, 420, 566, 625)),
                                     (11, (370, 655, 548, 786))],
        mask=[(330, 445, 371, 480), (330, 486, 347, 536), (330, 540, 337, 576)],
        layout='row', ref='2025 HL Q9(c)'),
    # Scheme p13: the load-extension graph, its three points marked.
    'engineering-2025-HL-scheme-q3b-sol': dict(
        doc='scheme', page=13, rect=(62, 90, 500, 380), solution=True,
        ref='2025 HL Q3(b)(i)-(ii)'),
    # Scheme p13: UTS = Max Load / C.S.A = 181kN / 113.1 mm2 = 1.6 kN/mm2.
    'engineering-2025-HL-scheme-q3biii-sol': dict(
        doc='scheme', page=13, rect=(62, 448, 522, 490), solution=True,
        ref='2025 HL Q3(b)(iii)'),
    # Scheme p17: the equilibrium diagram, liquidus and solidus labelled.
    'engineering-2025-HL-scheme-q5bi-sol': dict(
        doc='scheme', page=17, rect=(95, 92, 512, 372), solution=True,
        ref='2025 HL Q5(b)(i)'),
    # Scheme p30: the suggested leadscrew mechanism, labelled.
    'engineering-2025-HL-scheme-q9ci-sol': dict(
        doc='scheme', page=30, rect=(330, 378, 535, 630), solution=True,
        ref='2025 HL Q9(c)(i)'),
    # Scheme p30: the single acting cylinder drawn with and without air, labelled.
    'engineering-2025-HL-scheme-q9biv-sol': dict(
        doc='scheme', page=30, rect=(100, 124, 540, 206), solution=True,
        ref='2025 HL Q9(b)(iv)'),
}

CARDS = [
    dict(key=(1, 'm', None),
         why='"the dental braces shown" are photographed and captioned beside '
             '(m); no crop had been cut. Scheme p9 answers both properties in one '
             'sentence, "3 + 2".',
         lifted=[S(9, 72, 490, 540, 522)], tariff='questionTotal', total=5,
         stem=True, question_figure='engineering-2025-HL-paper-q1m-crop',
         notes="The scheme prints '3 + 2'."),
    dict(key=(3, 'b', 'i'), ref_also=('ii',), topic='eng-3-8',
         why='Scheme p13 answers (i) "plot the load-extension diagram" and (ii) '
             '"indicate each of the following points on your graph" with one '
             'graph, "10" and "2 + 2 + 2", so one card carries both asks; its '
             'rows are the graph\'s heading and the three points\' own labels.',
         question_lift=P(5, 120, 437, 512, 453,
                         more=[(120, 466, 383, 482), (120, 486, 222, 541)]),
         lifted=[S(13, 84, 71, 202, 87), S(13, 198, 207, 262, 223),
                 S(13, 233, 106, 318, 122), S(13, 420, 170, 497, 186)],
         row_kind='criterion', marks=[10, 2, 2, 2], total=16, stem=False,
         question_figure='engineering-2025-HL-paper-q3b-crop',
         figure='engineering-2025-HL-scheme-q3b-sol',
         notes="The scheme prints '10' for the graph and '2 + 2 + 2' for the "
               "three points, which it marks on the graph."),
    dict(key=(3, 'b', 'iii'),
         replaces='the shipped card\'s only row was "C.S.A", the denominator of '
                  'the scheme\'s fraction, for four marks, under the results table '
                  'flattened into a line of numbers',
         why='Scheme p13 sets UTS = Max Load / C.S.A = 181kN / 113.1 mm2 = 1.6 '
             'kN/mm2 as stacked fractions; the table is shown as printed.',
         special={'kind': 'ask'}, total=4, stem=False,
         question_figure='engineering-2025-HL-paper-q3b-crop',
         figure='engineering-2025-HL-scheme-q3biii-sol'),
    dict(key=(5, 'a', 'ii'),
         why='The three unit cells are drawn and captioned "Structure A", "B" and '
             '"C" on p7; scheme p16 names each, "2 + 2 + 2".',
         lifted=[S(16, 86, 513, 352, 529), S(16, 86, 528, 352, 544),
                 S(16, 86, 543, 352, 559)],
         marks=[2, 2, 2], total=6,
         figure='engineering-2025-HL-paper-q5a-crop',
         labels={'A': S(16, 149, 513, 330, 529), 'B': S(16, 149, 528, 326, 544),
                 'C': S(16, 148, 543, 352, 559)}),
    dict(key=(5, 'a', 'iii'),
         why='Structures A and B are the unit cells drawn on p7; scheme p16 '
             'describes each in a paragraph, "6".',
         lifted=[S(16, 86, 590, 540, 635), S(16, 86, 649, 540, 709)],
         tariff='questionTotal', total=6,
         question_figure='engineering-2025-HL-paper-q5a-crop',
         labels={'A': S(16, 149, 513, 330, 529), 'B': S(16, 149, 528, 326, 544)},
         notes="The scheme prints '6'."),
    dict(key=(5, 'b', 'i'),
         why='Scheme p17 answers with the equilibrium diagram, priced "8 + 1 + 1": '
             'the diagram under its heading, then the liquidus and the solidus, '
             'labelled on it. The table is shown as printed.',
         lifted=[S(17, 86, 71, 332, 87), S(17, 216, 115, 286, 131),
                 S(17, 342, 228, 402, 244)],
         row_kind='criterion', marks=[8, 1, 1], total=10, stem=False,
         question_figure='engineering-2025-HL-paper-q5b-crop',
         figure='engineering-2025-HL-scheme-q5bi-sol',
         notes="The scheme prints '8 + 1 + 1'."),
    dict(key=(5, 'b', 'ii'),
         why='The diagram is the candidate\'s own from (b)(i), drawn from the '
             'table on p7, which the card shows; scheme p17 reads A, B and C off '
             'it and gives the ratio, "4".',
         topic='eng-1-3',
         lifted=[S(17, 86, 427, 200, 443), S(17, 86, 444, 200, 460),
                 S(17, 86, 461, 200, 477), S(17, 86, 478, 200, 494)],
         tariff='questionTotal', total=4, stem=False,
         question_figure='engineering-2025-HL-paper-q5b-crop',
         notes="The scheme prints '4'."),
    dict(key=(5, 'c', 'i'),
         why='"the metal recycling process shown" is the seven-stage diagram on '
             'p7; scheme pp17-18 describe all seven stages, of which the paper '
             'asks any four, priced as the part, "Any two @ 8 + 8".',
         lifted=[S(17, 86, 607, 555, 638), S(17, 86, 638, 555, 686),
                 S(17, 86, 686, 555, 749), S(18, 86, 71, 555, 103),
                 S(18, 86, 103, 555, 151), S(18, 86, 150, 555, 182),
                 S(18, 86, 182, 555, 214)],
         tariff='questionTotal', total=8,
         question_figure='engineering-2025-HL-paper-q5c-crop',
         notes="The scheme prints 'Any two @ 8 + 8'."),
    dict(key=(7, 'b', 'i'),
         why='"the eVTOL aircraft shown" is photographed beside (b)(i); scheme '
             'pp23-24 give four reasons, priced as the part, "Any three @ 6 + 6 + '
             '6".',
         lifted=[S(23, 94, 649, 545, 716), S(23, 94, 716, 545, 749),
                 S(24, 94, 71, 545, 121), S(24, 94, 122, 545, 171)],
         tariff='questionTotal', total=6,
         question_figure='engineering-2025-HL-paper-q7bi-crop',
         notes="The scheme prints 'Any three @ 6 + 6 + 6'."),
    dict(key=(9, 'c', 'i'),
         why='Both (c)s price their (i) at 8 (scheme pp30-31): the leadscrew, a '
             '"Suggested solution" with its diagram, or the two solar carport '
             'benefits at "4 + 4". One card for the printed OR, each branch a '
             'route of its own.',
         topic='eng-2-15',
         question_lift=P(11, *_CA, more=[(107, 488, 346, 535), _OR9, _CB,
                                         (107, 699, 353, 717)]),
         lifted=[S(30, 78, 389, 320, 538), S(31, 78, 121, 560, 203),
                 S(31, 78, 204, 560, 270)],
         marks=[8, 4, 4], routes=['a', 'b', 'b'], total=8, stem=False,
         question_figure='engineering-2025-HL-paper-q9c-crop',
         figure='engineering-2025-HL-scheme-q9ci-sol',
         notes="The paper sets two (c)s either side of an OR. The scheme prints "
               "'8' for the leadscrew, a suggested solution ('other viable "
               "solutions are acceptable'), and '4 + 4' for the solar carport's "
               "two benefits."),
    dict(key=(9, 'c', 'ii'),
         why='Both (c)s price their (ii) at 8 (scheme pp30-31): the limit '
             'switch\'s function, or how solar energy powers the vehicle. One card '
             'for the printed OR, each branch a route of its own.',
         topic='eng-2-16',
         question_lift=P(11, *_CA, more=[(107, 541, 335, 576), _OR9, _CB,
                                         (107, 723, 350, 756)]),
         lifted=[S(30, 78, 693, 550, 759), S(31, 78, 338, 572, 469)],
         marks=[8, 8], routes=['a', 'b'], total=8, stem=False,
         question_figure='engineering-2025-HL-paper-q9c-crop',
         notes="The paper sets two (c)s either side of an OR; the scheme prints "
               "'8' for each (ii)."),
    dict(key=(9, 'b', 'iv'),
         replaces='the shipped card\'s second row was the drawing\'s label and captions, '
                  '"Force of air moves ram No compressed air Compressed air applied"',
         why='Scheme p30 answers in one paragraph over a labelled, captioned drawing, '
             'shown with the answer; "6 marks".',
         topic='eng-2-15',
         lifted=[S(30, 80, 87, 545, 121)], marks=[6], total=6,
         figure='engineering-2025-HL-scheme-q9biv-sol',
         notes="The scheme prints '6 marks'."),
]

TOPICS = {
    'eng-2025-hl-q5-b-iii': ('eng-1-3', 'the eutectic point is read off the equilibrium '
                             'diagram; "zinc" outvoted it'),
    'eng-2025-hl-q7-b-ii': ('eng-1-9', 'elastic memory and elasticity in thermoplastics '
                            'are polymer properties, not mechanical testing'),
}

_Q4 = 'which the reference files with the rest of Q4 under heat treatment'
_Q5C = ('Q5(c) is metal production and recycling; the reference files Q5 under the '
        'structure of materials only.')
_ROB = 'Energy, Electronics & Robotics'

ATLAS = {
    'eng-2025-hl-q4-b-ii': dict(
        topics=['Heat Treatment'],
        note=f'Point C on the iron-carbon diagram and its transformation, {_Q4}; the '
             f'card\'s syllabus heading is Structure of metals.'),
    'eng-2025-hl-q4-c-iii': dict(
        topics=['Heat Treatment'],
        note=f'A benefit of forging metal components, {_Q4}; the card\'s syllabus '
             f'heading is Manufacturing processes.'),
    'eng-2025-hl-q5-c-i': dict(
        topics=['Metallurgy'],
        note='The stages of the metal recycling process. ' + _Q5C),
    'eng-2025-hl-q5-c-ii': dict(
        topics=['Metallurgy'],
        note='The benefits of upcycling metal components. ' + _Q5C),
    'eng-2025-hl-q5-c-iii': dict(
        topics=['Metallurgy'],
        note='The electrometallurgy of aluminium (extraction). ' + _Q5C),
    'eng-2025-hl-q9-a-ii': dict(
        topics=[_ROB],
        note='Uses for a remote-controlled inspection robot, which the reference '
             'files Q9 under; the card\'s syllabus heading is Technology.'),
    'eng-2025-hl-q9-b-ii': dict(
        topics=[_ROB],
        note='Thermostatic control in home heating, a control system, which the '
             'reference files Q9 under; the card\'s syllabus heading is Technology.'),
}
