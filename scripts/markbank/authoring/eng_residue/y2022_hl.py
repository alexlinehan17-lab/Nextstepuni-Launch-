"""2022 Higher Level: the parts eng_all refuses or gets wrong, from the page.

Paper LC027ALP000EV; scheme pages as the PDF numbers them. The marks grid is
on scheme p6 (Question 1 "Any ten @ 5 marks each").
"""
from eng_lift import lift

Y, L = 2022, 'hl'


def S(page, *rect):
    return lift(Y, L, 'scheme', page, rect)


def P(page, *rect, more=()):
    return lift(Y, L, 'paper', page, rect, more=more)


CROPS = {
    # Paper p3: the gearbox motor and its caption "output shaft", printed
    # beside (d) and asked about by (d) and (e).
    'engineering-2022-HL-paper-q1d-crop': dict(
        doc='paper', page=3, rect=(426, 244, 576, 354), ref='2022 HL Q1(d)'),
    # Paper p3: the golf club photographed beside (k).
    'engineering-2022-HL-paper-q1k-crop': dict(
        doc='paper', page=3, rect=(422, 552, 557, 631), ref='2022 HL Q1(k)'),
    # Paper p3: the solar farm photographed beside (m).
    'engineering-2022-HL-paper-q1m-crop': dict(
        doc='paper', page=3, rect=(427, 669, 556, 746), ref='2022 HL Q1(m)'),
    # Paper p7: Q5(b)'s table of solidification temperatures, as printed.
    'engineering-2022-HL-paper-q5b-crop': dict(
        doc='paper', page=7, rect=(50, 296, 562, 410), ref='2022 HL Q5(b)'),
    # Paper p10: the step cone drill bit photographed beside (b)(iv).
    'engineering-2022-HL-paper-q8biv-crop': dict(
        doc='paper', page=10, rect=(513, 291, 546, 382), image=True,
        ref='2022 HL Q8(b)(iv)'),
    # Paper p11: the guitar's tuning pegs photographed beside (a).
    'engineering-2022-HL-paper-q9a-crop': dict(
        doc='paper', page=11, rect=(406, 98, 567, 249), ref='2022 HL Q9(a)'),
    # Scheme p8: the motor's flat output shaft and the pulley's grub screw.
    'engineering-2022-HL-scheme-q1e-sol': dict(
        doc='scheme', page=8, rect=(90, 72, 485, 206), solution=True,
        ref='2022 HL Q1(e)'),
    # Scheme p10: the AI / machine learning / deep learning diagram and its
    # three captions.
    'engineering-2022-HL-scheme-q2aii-sol': dict(
        doc='scheme', page=10, rect=(112, 360, 566, 530), solution=True,
        ref='2022 HL Q2(a)(ii)'),
    # Scheme p13: the two stress-strain graphs on one set of axes.
    'engineering-2022-HL-scheme-q3bi-sol': dict(
        doc='scheme', page=13, rect=(88, 463, 440, 750), solution=True,
        ref='2022 HL Q3(b)(i)'),
    # Scheme p17: the equilibrium diagram, liquidus and solidus labelled.
    'engineering-2022-HL-scheme-q5bi-sol': dict(
        doc='scheme', page=17, rect=(60, 466, 546, 752), solution=True,
        ref='2022 HL Q5(b)(i)'),
    # Scheme p18: |AB|/|BC| = (70 - 44)/(88 - 70) = 26/18.
    'engineering-2022-HL-scheme-q5bii-sol': dict(
        doc='scheme', page=18, rect=(100, 70, 490, 106), solution=True,
        ref='2022 HL Q5(b)(ii)'),
    # Scheme p26: the suggested clamping device photographed.
    'engineering-2022-HL-scheme-q8cii-sol': dict(
        doc='scheme', page=26, rect=(85, 95, 270, 216), solution=True,
        ref='2022 HL Q8(c)(ii)'),
}

CARDS = [
    dict(key=(1, 'd', None),
         why='"The single ratio gearbox motor shown opposite" is photographed '
             'beside (d) with the caption "output shaft"; no crop had been cut.',
         use=[0], marks=[5], total=5,
         question_figure='engineering-2022-HL-paper-q1d-crop'),
    dict(key=(1, 'e', None),
         why='"the output shaft of the gearbox motor shown" is the same '
             'photograph; scheme pp7-8 answer in two sentences and a drawing of '
             'the flat shaft and the pulley\'s grub screw.',
         use=[0, 1], tariff='questionTotal', total=5,
         question_figure='engineering-2022-HL-paper-q1d-crop',
         figure='engineering-2022-HL-scheme-q1e-sol',
         notes="The scheme prints '5'."),
    dict(key=(1, 'k', None),
         why='"modern golf clubs, as shown" is the club photographed beside (k); '
             'scheme p9 answers both reasons in one paragraph, "3 + 2".',
         use=[0], tariff='questionTotal', total=5,
         question_figure='engineering-2022-HL-paper-q1k-crop',
         notes="The scheme prints '3 + 2'."),
    dict(key=(1, 'm', None),
         why='"a large array of solar panels, as shown" is the solar farm '
             'photographed beside (m); scheme p9 sets advantages and '
             'disadvantages as a two-column table, "3 + 2" for one of each, and '
             'the reader reads it across the columns.',
         use=[[1, 3, 5, 7], [2, 4, 6, 8]], marks=[3, 2], total=5,
         question_figure='engineering-2022-HL-paper-q1m-crop',
         notes="The scheme prints '3 + 2': any one advantage, then any one "
               "disadvantage."),
    dict(key=(2, 'a', 'ii'),
         why='Scheme p10 answers in two paragraphs and a diagram whose captions '
             'the reader welds into a third point that cannot trace.',
         use=[0, 1], tariff='questionTotal', total=5,
         figure='engineering-2022-HL-scheme-q2aii-sol',
         notes="The scheme prints '5'."),
    dict(key=(3, 'b', 'i'),
         replaces='the shipped card\'s only row was "2 4 6 8", the graph\'s strain '
                  'axis, for ten marks',
         why='Scheme p13 answers "Draw graphs on same axes" with the two graphs.',
         special={'kind': 'ask'}, total=10,
         question_figure='engineering-2022-HL-paper-q3bi-art',
         figure='engineering-2022-HL-scheme-q3bi-sol',
         notes="The scheme prints 'Draw graphs on same axes', 10 marks."),
    dict(key=(5, 'b', 'i'),
         why='Scheme p17 answers with the equilibrium diagram and prints no '
             'words; the reader finds no answer at (b)(i). The table is shown '
             'as printed rather than as a flattened stem.',
         special={'kind': 'ask'}, total=10, stem=False,
         question_figure='engineering-2022-HL-paper-q5b-crop',
         figure='engineering-2022-HL-scheme-q5bi-sol'),
    dict(key=(5, 'b', 'ii'),
         why='The diagram is the candidate\'s own from (b)(i); scheme p18 answers '
             'with stacked fractions read off its own diagram (A, B, C at '
             '1400 deg C).',
         special={'kind': 'ask'}, total=4, stem=False, topic='eng-1-3',
         question_figure='engineering-2022-HL-paper-q5b-crop',
         figure='engineering-2022-HL-scheme-q5bii-sol'),
    dict(key=(5, 'b', 'iii'),
         replaces='the shipped card carried the table as a line of numbers, "% of '
                  'metal B in the alloy 0 10 20 ... Start of solidification (C) 1120 '
                  '1225 ...", which the melting points are read from',
         why='The melting points are the table\'s 0% and 100% columns (and the '
             'diagram\'s ends); the table is shown as printed. Scheme p18, "2 + 2". '
             'The melting points of the two metals are read off the equilibrium '
             'diagram, so the card files under it ("alloy" outvoted it).',
         topic='eng-1-3',
         lifted=[S(18, 105, 140, 170, 156), S(18, 105, 157, 170, 173)],
         marks=[2, 2], total=4, stem=False,
         question_figure='engineering-2022-HL-paper-q5b-crop'),
    dict(key=(8, 'b', 'iv'),
         why='"a step cone drill bit as shown" is photographed beside (b); '
             'priced by "Any three @ 6 + 6 + 6".',
         use=[0, 1, 2, 3, 4, 5], tariff='questionTotal', total=6,
         question_figure='engineering-2022-HL-paper-q8biv-crop',
         notes="The scheme prints '6 marks'."),
    dict(key=(8, 'c', 'ii'),
         why='One card for the printed OR, as (c)(i) is: the bandsaw clamping '
             'method (scheme pp25-26, a paragraph and a "Suggested description" '
             'beside a photograph of the device, which the reader welds) or the '
             'two CNC terms (scheme p26). The grid prices the first branch\'s '
             '(ii) 10 and the OR branch\'s (ii) "4 + 4".',
         lifted=[S(25, 104, 690, 562, 740), S(26, 280, 70, 558, 190),
                 S(26, 108, 423, 560, 529), S(26, 108, 542, 560, 587)],
         tariff='questionTotal', total=10,
         figure='engineering-2022-HL-scheme-q8cii-sol',
         notes="The scheme prints '10' for the bandsaw branch and '4 + 4' for "
               "the CNC branch's (ii)."),
    dict(key=(9, 'a', 'ii'),
         why='"the musical instrument shown" is the guitar photographed beside '
             '(a); scheme p27 lists three advantages for "4 + 4".',
         use=[0, 1, 2], tariff='orderedSplit', notation='4 + 4', ladder=8,
         question_figure='engineering-2022-HL-paper-q9a-crop'),
]

TOPICS = {
    'eng-2022-hl-q5-c-ii': ('eng-3-7', 'the corrosive effects of the environment on '
                            'metal objects is corrosion; "environment" outvoted it'),
}

_AI = ('Artificial intelligence and smart manufacturing (the 2022 Higher special '
       'topic), which the reference files Q2 under; the card\'s syllabus heading '
       'is Technology, or Manufacturing processes for smart manufacturing.')

ATLAS = {
    **{f'eng-2022-hl-q2-{p}': dict(topics=['Energy, Electronics & Robotics'], note=_AI)
       for p in ('a-i', 'a-ii', 'b', 'c', 'd', 'e')},
    'eng-2022-hl-q3-a-iii': dict(
        topics=['Testing of Materials and Products'],
        note='Quality control: inspecting and testing products against a '
             'standard, which the reference files Q3(a) under.'),
    'eng-2022-hl-q5-c': dict(
        topics=['The Structure of Materials', 'Corrosion of Metals', 'Metallurgy'],
        note='Any two of dislocations (structure), the environment\'s corrosive '
             'effects (corrosion) and the refining of aluminium (metallurgy); Q5 '
             'is otherwise filed under structure and equilibrium diagrams only.'),
    'eng-2022-hl-q5-c-ii': dict(
        topics=['Corrosion of Metals'],
        note='The corrosive effects of the environment on metal objects.'),
    'eng-2022-hl-q7-b-iv': dict(
        topics=['Polymers'],
        note='Recycling plastic mobile phone covers, which the reference files '
             'Q7(b) under; the card\'s syllabus heading is Technology '
             '(recycling and sustainability).'),
    'eng-2022-hl-q7-c-i': dict(
        topics=['Polymers'],
        note='Glass against polycarbonate for screen protectors: a polymer\'s '
             'properties, which the reference files Q7(c) under.'),
    **{f'eng-2022-hl-q8-b-{p}': dict(
        topics=['Health and Safety'],
        note='Interlocking guards and electrical isolating switches are machine '
             'and workshop safety; Q8 is otherwise filed under machining.')
       for p in ('ii', 'v')},
}
