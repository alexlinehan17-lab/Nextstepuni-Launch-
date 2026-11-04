"""2024 Higher Level: the parts eng_all refuses or gets wrong, from the page.

Paper LC027ALP000EV; scheme pages as the PDF numbers them. The marks grid is
on scheme p6 (Question 1 "Any ten @ 5 marks each").
"""
from eng_lift import join, lift

Y, L = 2024, 'hl'


def S(page, *rect):
    return lift(Y, L, 'scheme', page, rect)


def P(page, *rect, more=()):
    return lift(Y, L, 'paper', page, rect, more=more)


CROPS = {
    # Paper p3: the roof bar and the car carrying it, captioned "Roof bar",
    # beside (g)-(i).
    'engineering-2024-HL-paper-q1g-crop': dict(
        doc='paper', page=3, rect=(395, 425, 585, 575), ref='2024 HL Q1(g)'),
    # Paper p3: the tilted solar panel photographed beside (m).
    'engineering-2024-HL-paper-q1m-crop': dict(
        doc='paper', page=3, rect=(424, 680, 556, 780), ref='2024 HL Q1(m)'),
    # Paper p5: (b)'s sentence and its table of tensile results, as printed.
    'engineering-2024-HL-paper-q3b-crop': dict(
        doc='paper', page=5, rect=(48, 346, 518, 424), ref='2024 HL Q3(b)'),
    # Paper p7: (b)'s sentence and its table of solidification temperatures.
    'engineering-2024-HL-paper-q5b-crop': dict(
        doc='paper', page=7, rect=(48, 238, 548, 346), ref='2024 HL Q5(b)'),
    # Scheme p9: "Tilting a solar panel: Suggested solution:" and its diagram.
    'engineering-2024-HL-scheme-q1m-sol': dict(
        doc='scheme', page=9, rect=(90, 605, 264, 760), solution=True,
        ref='2024 HL Q1(m)'),
    # Scheme p14: the stress-strain graph.
    'engineering-2024-HL-scheme-q3bi-sol': dict(
        doc='scheme', page=14, rect=(125, 92, 500, 372), solution=True,
        ref='2024 HL Q3(b)(i)'),
    # Scheme p14: Young's Modulus = stress/strain = 135/1.50 = 90 kN/mm2.
    'engineering-2024-HL-scheme-q3bii-sol': dict(
        doc='scheme', page=14, rect=(90, 388, 520, 424), solution=True,
        ref='2024 HL Q3(b)(ii)'),
    # Scheme p18: the equilibrium diagram, liquidus and solidus labelled.
    'engineering-2024-HL-scheme-q5bi-sol': dict(
        doc='scheme', page=18, rect=(80, 196, 545, 478), solution=True,
        ref='2024 HL Q5(b)(i)'),
    # Scheme p18: the cooling curve for 30% metal B.
    'engineering-2024-HL-scheme-q5bii-sol': dict(
        doc='scheme', page=18, rect=(150, 513, 420, 650), solution=True,
        ref='2024 HL Q5(b)(ii)'),
    # Scheme p20: the labelled TIG diagram and the photograph beside it.
    'engineering-2024-HL-scheme-q6aii-sol': dict(
        doc='scheme', page=20, rect=(34, 160, 572, 381), solution=True,
        ref='2024 HL Q6(a)(ii)'),
}

CARDS = [
    dict(key=(1, 'g', None),
         why='"the roof bar shown" is photographed and captioned beside (g); no '
             'crop had been cut. Scheme p8 answers both reasons in one line, '
             '"3 + 2".',
         lifted=[S(8, 90, 454, 515, 486)], tariff='questionTotal', total=5,
         stem=True,
         question_figure='engineering-2024-HL-paper-q1g-crop',
         notes="The scheme prints '3 + 2'."),
    dict(key=(1, 'l', None),
         why='Cordless power tools name no syllabus heading the topic rules know; '
             'they are workshop equipment whose advantages the scheme gives as '
             'safety and portability, under Health and safety. Scheme p9 sets '
             'advantages and disadvantages as a two-column table, "3 + 2" for one '
             'of each.',
         topic='eng-3-1',
         lifted=[[S(9, 120, 467, 300, 501), S(9, 120, 501, 300, 533),
                  S(9, 120, 533, 300, 566)],
                 [S(9, 312, 467, 500, 484), S(9, 312, 485, 500, 501),
                  S(9, 312, 501, 500, 534)]],
         marks=[3, 2], total=5,
         notes="The scheme prints '3 + 2': any one advantage, then any one "
               "disadvantage."),
    dict(key=(1, 'm', None),
         why='The solar panel is photographed beside (m). Scheme p9 answers with '
             'a "Suggested solution": a numbered diagram and its three numbered '
             'parts; the reader takes the parts for the diagram\'s callouts.',
         topic='eng-2-15',
         lifted=[S(9, 268, 611, 548, 627), S(9, 268, 626, 548, 674),
                 S(9, 268, 674, 548, 737)],
         tariff='questionTotal', total=5,
         question_figure='engineering-2024-HL-paper-q1m-crop',
         figure='engineering-2024-HL-scheme-q1m-sol',
         notes="The scheme prints 'Suggested solution', 5 marks."),
    dict(key=(3, 'b', 'i'),
         why='Scheme p14 answers "Draw stress-strain graph" with the graph and '
             'prints no words; the table of results is shown as printed.',
         special={'kind': 'ask'}, total=10, stem=False,
         question_figure='engineering-2024-HL-paper-q3b-crop',
         figure='engineering-2024-HL-scheme-q3bi-sol',
         notes="The scheme prints 'Draw stress-strain graph', 10 marks."),
    dict(key=(3, 'b', 'ii'),
         why='Scheme p14 sets Young\'s Modulus = stress / strain = 135 / 1.50 = '
             '90 kN/mm2 as stacked fractions, which the reader cannot trace.',
         special={'kind': 'ask'}, total=4, stem=False,
         question_figure='engineering-2024-HL-paper-q3b-crop',
         figure='engineering-2024-HL-scheme-q3bii-sol'),
    dict(key=(5, 'b', 'i'),
         why='Scheme p18 answers with the equilibrium diagram, liquidus and '
             'solidus labelled, and prints no words; the table is shown as '
             'printed.',
         special={'kind': 'ask'}, total=10, stem=False,
         question_figure='engineering-2024-HL-paper-q5b-crop',
         figure='engineering-2024-HL-scheme-q5bi-sol'),
    dict(key=(5, 'b', 'ii'),
         why='Scheme p18 answers with the sketched cooling curve, its start and '
             'end of solidification marked at 445 and 300 deg C.',
         special={'kind': 'ask'}, total=4, stem=False, topic='eng-1-3',
         question_figure='engineering-2024-HL-paper-q5b-crop',
         figure='engineering-2024-HL-scheme-q5bii-sol'),
    dict(key=(6, 'a', 'ii'),
         replaces='the automatic card (built in this lane once the page runs were '
                  'rendered, never shipped) carried the description without the '
                  'labelled diagram the question asks for',
         why='Scheme pp19-20: one paragraph over the page break, then the '
             'labelled TIG diagram; "10".',
         lifted=[join(S(19, 110, 708, 515, 741), S(20, 110, 60, 495, 142))],
         marks=[10], total=10,
         question_figure='engineering-2024-HL-paper-q6ai-art',
         figure='engineering-2024-HL-scheme-q6aii-sol'),
    dict(key=(6, 'b', 'iii'),
         replaces='never shipped: the page-run rendering starts this paragraph at '
                  'its second line, so the automatic author builds the card only '
                  'from the joined lift this entry records, and the entry owns it',
         why='Scheme pp20-21 answer in one paragraph over the page break, which '
             'the reader cuts in two; priced by (b)\'s "Any three @ 6 + 6 + 6".',
         lifted=[join(S(20, 111, 701, 500, 734), S(21, 110, 60, 500, 108))],
         tariff='questionTotal', total=6,
         notes="The scheme prints 'Any three @ 6 + 6 + 6'."),
    dict(key=(7, 'a', 'iii'),
         replaces='the shipped question read "... for each of the following: Hose '
                  'reel cover • increased flexibility ...", the photograph\'s '
                  'caption run into the ask',
         why='The ask is lifted from its own lines on paper p9, without the '
             'caption printed beside them.',
         question_lift=P(9, 105, 250, 362, 302, more=[(120, 306, 290, 341)]),
         lifted=[S(23, 111, 445, 470, 463), S(23, 111, 463, 480, 496)],
         marks=[3, 3], total=6,
         question_figure='engineering-2024-HL-paper-q7ai-art'),
    dict(key=(9, 'b', 'ii'),
         replaces='the shipped card\'s rows were the three "uses" bullets without '
                  'the mechanism they are uses of: scheme p28 heads them "(ii) '
                  'Universal Joint or Coupling, uses include:", and the ask is to '
                  'identify it',
         why='Scheme p28 names the mechanism, then three bullets; "6 marks".',
         lifted=[S(28, 118, 428, 255, 444), S(28, 120, 443, 545, 478),
                 S(28, 120, 477, 545, 494), S(28, 120, 494, 545, 529)],
         tariff='questionTotal', total=6,
         question_figure='engineering-2024-HL-paper-q9bii-art',
         notes="The scheme prints '6 marks'."),
]

TOPICS = {
    'eng-2024-hl-q3-c-ii': ('eng-3-8', 'a non-destructive test for internal flaws is '
                            'materials testing; "aluminium" outvoted it'),
    'eng-2024-hl-q5-c-iii': ('eng-1-3', 'why FCC crystal structures are ductile is the '
                             'structure of metals, not mechanical testing'),
    'eng-2024-hl-q7-a-ii': ('eng-1-9', 'the process that makes the polymer hose pipe is '
                            'plastics processing, not manufacturing systems'),
}

ATLAS = {
    'eng-2024-hl-q1-b': dict(
        topics=['Health and Safety'],
        note='The hazards of adhesives, which the reference files Q1(b) under; the '
             'card\'s syllabus heading is Joining, where adhesives sit.'),
    'eng-2024-hl-q2-c-i': dict(
        topics=['Q2 - Special Topic'],
        note='Cast bronze ship propellers, in the 2024 Higher special topic (container '
             'ships), which the reference files Q2 under; the card\'s syllabus heading '
             'is Non-ferrous metals.'),
    'eng-2024-hl-q3-a-i': dict(
        topics=['Testing of Materials and Products'],
        note='Custom-made carbon fibre shin guards, which the reference files with the '
             'rest of Q3 under testing; the card\'s syllabus heading is Plastics and '
             'composites.'),
    'eng-2024-hl-q6-c-i': dict(
        topics=['Energy, Electronics & Robotics'],
        note='Robots inspecting pipelines (the OR branch of Q6(c)), which the reference '
             'files Q6(c) under; the card\'s syllabus heading is Technology.'),
    'eng-2024-hl-q7-c-ii': dict(
        topics=['Graphics and Design'],
        note='Rapid prototyping in the design of new products, which the reference '
             'files Q7(c) under; the card\'s syllabus heading is Manufacturing '
             'processes.'),
}
