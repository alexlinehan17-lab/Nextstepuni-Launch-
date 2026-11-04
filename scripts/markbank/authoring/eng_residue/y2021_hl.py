"""2021 Higher Level: the parts eng_all refuses or gets wrong, from the page.

Paper LC027ALP000EV, scheme pages as the PDF numbers them (the scheme's own
footer reads one lower: PDF page 11 is printed "Page 10").
"""
from eng_lift import join, lift

Y, L = 2021, 'hl'


def S(page, *rect):
    return lift(Y, L, 'scheme', page, rect)


def P(page, *rect, more=()):
    return lift(Y, L, 'paper', page, rect, more=more)


CROPS = {
    # Scheme p11: the stress-strain graph the scheme answers Q3(b)(i) with,
    # axes, plotted points and the 0.1% offset line; the "10" beside it is
    # left out.
    'engineering-2021-HL-scheme-q3bi-sol': dict(
        doc='scheme', page=11, rect=(100, 214, 542, 490), solution=True,
        ref='2021 HL Q3(b)(i)'),
    # Scheme p11: Young's modulus set as two stacked fractions.
    'engineering-2021-HL-scheme-q3biii-sol': dict(
        doc='scheme', page=11, rect=(100, 560, 365, 593), solution=True,
        ref='2021 HL Q3(b)(iii)'),
    # Scheme p16: Graph 7, the Cadmium-Bismuth equilibrium diagram with its
    # liquidus, solidus and eutectic point labelled and A, B, C at 200 deg C.
    'engineering-2021-HL-scheme-q5bi-sol': dict(
        doc='scheme', page=16, rect=(100, 496, 566, 726), solution=True,
        ref='2021 HL Q5(b)(i)'),
    # Scheme p17: |AB| over |BC| = (75 - 52) over (100 - 75) = 23 over 25.
    'engineering-2021-HL-scheme-q5bii-sol': dict(
        doc='scheme', page=17, rect=(100, 78, 495, 112), solution=True,
        ref='2021 HL Q5(b)(ii)'),
    # Scheme p17: the cooling curve with its two solidification temperatures.
    'engineering-2021-HL-scheme-q5biii-sol': dict(
        doc='scheme', page=17, rect=(325, 128, 578, 252), solution=True,
        ref='2021 HL Q5(b)(iii)'),
    # Scheme p22: the blow-moulding diagram, stages 1 to 4.
    'engineering-2021-HL-scheme-q7ci-sol': dict(
        doc='scheme', page=22, rect=(280, 415, 566, 598), solution=True,
        ref='2021 HL Q7(c)(i)'),
    # Scheme p25: the suggested scissor-lift solution, photograph and callouts.
    'engineering-2021-HL-scheme-q9aii-sol': dict(
        doc='scheme', page=25, rect=(75, 300, 310, 490), solution=True,
        ref='2021 HL Q9(a)(ii)'),
    # Paper p7: Q5(b)'s stimulus as printed -- the sentence giving the two
    # melting points and the table of solidification temperatures. Flattened
    # into a stem the table is a run of bare numbers (card lint's label-junk)
    # and the melting points, which the diagram needs, are on no card at all.
    'engineering-2021-HL-paper-q5b-crop': dict(
        doc='paper', page=7, rect=(66, 294, 532, 430), ref='2021 HL Q5(b)'),
    # Paper p11: the toggle clamp photographed right of Q9(b)(ii). Named -crop,
    # not -art, so eng_all does not also hand it to (b)'s other romans. The
    # photograph itself (image=True): the line above it ends inside its box
    # and the one below starts there, so any rectangle carries a fragment.
    'engineering-2021-HL-paper-q9bii-crop': dict(
        doc='paper', page=11, rect=(465, 282, 554, 371), image=True,
        ref='2021 HL Q9(b)(ii)'),
}

CARDS = [
    dict(key=(3, 'a', 'i'),
         replaces='the shipped rows were the two tests\' bullet lists with neither '
                  'heading, so "A hardened Steel or Tungsten Carbide ball indenter is '
                  'used in this hardness test" did not say which test',
         why='Scheme p10 lists six points under "Brinell hardness test:" and six '
             'under "Vickers hardness test:"; each list\'s first point is lifted with '
             'its heading, and the diagrams\' captions beside them are left out.',
         lifted=[join(S(10, 100, 97, 220, 113), S(10, 120, 114, 420, 145)),
                 S(10, 120, 145, 440, 160), S(10, 120, 160, 380, 175),
                 S(10, 120, 175, 420, 206), S(10, 120, 205, 405, 235),
                 S(10, 120, 235, 405, 250),
                 join(S(10, 100, 266, 225, 282), S(10, 120, 283, 385, 314)),
                 S(10, 120, 314, 300, 329), S(10, 120, 329, 432, 359),
                 S(10, 120, 359, 405, 389), S(10, 120, 389, 405, 419),
                 S(10, 120, 419, 520, 434)],
         tariff='questionTotal', total=8,
         notes="The scheme prints '8 marks'."),
    dict(key=(3, 'a', 'iii'),
         replaces='the shipped rows were the two tests\' bullet lists with neither '
                  'heading, so nothing said which five points are Izod\'s and which '
                  'Charpy\'s (the last point is the same in both)',
         why='Scheme pp10-11 list five points under "Izod impact test:" and five '
             'under "Charpy Test:"; each list\'s first point is lifted with its '
             'heading, and the diagram captions beside them are left out.',
         lifted=[join(S(10, 100, 602, 200, 618), S(10, 120, 619, 300, 635)),
                 S(10, 120, 636, 300, 652), S(10, 120, 653, 320, 669),
                 S(10, 120, 669, 335, 685), S(10, 120, 686, 395, 719),
                 join(S(11, 100, 63, 180, 79), S(11, 120, 80, 300, 96)),
                 S(11, 120, 97, 300, 113), S(11, 120, 114, 330, 130),
                 S(11, 120, 131, 395, 147), S(11, 120, 148, 395, 180)],
         tariff='questionTotal', total=8,
         notes="The scheme prints '8 marks'."),
    dict(key=(3, 'b', 'i'),
         why='Scheme p11 answers the plot with the graph itself and heads it '
             '"(b) (ii) Plot the graph." -- a second (ii), where its own marks '
             'grid (p3) prices (b)(i) 10, (ii) 4, (iii) 4 and the paper sets the '
             'plot as (b)(i). The reader files the plot under (ii) and loses '
             '(i), so both refused as unpriced.',
         special={'kind': 'ask'}, total=10, stem=True,
         figure='engineering-2021-HL-scheme-q3bi-sol',
         notes='The scheme heads this answer "(b) (ii)"; its marks grid prices '
               'the plot as (b)(i), 10 marks.'),
    dict(key=(3, 'b', 'ii'),
         why='The same misnumbered heading: the proof stress line is the '
             'second "(ii)" on p11 and the reader keeps only the first.',
         lifted=[S(11, 100, 510, 400, 528)], marks=[4], total=4, stem=True),
    dict(key=(3, 'b', 'iii'),
         replaces='the shipped row flattened the two stacked fractions to '
                  '"Young\'s modulus = stress = 260 = 87 N/mm² strain 3.0"',
         why='Scheme p11 sets Young\'s modulus = stress/strain = 260/3.0 = 87 '
             'N/mm² as stacked fractions; the text layer reads them row by row.',
         special={'kind': 'ask'}, total=4, stem=True,
         figure='engineering-2021-HL-scheme-q3biii-sol'),
    dict(key=(4, 'c', 'i'),
         why='Scheme p14 answers with two paragraphs, the optical pyrometer and '
             'the thermocouple pyrometer, each beside its diagram; the reader '
             'welds the diagram callouts ("optical lens filter filament optical '
             'lens ... too low correct too high") into one point that cannot '
             'trace. Priced by the grid\'s "Any two @ 8 + 8", as (c)(iii) is.',
         lifted=[S(14, 100, 96, 560, 197), S(14, 100, 466, 560, 568)],
         tariff='questionTotal', total=8, notes="The scheme prints '8 marks'."),
    dict(key=(4, 'c', 'ii'),
         why='"Grey cast iron and white cast iron;" reads like a list item, so '
             'the author climbs to (c) and refuses there on (c)(i)\'s callouts. '
             'Scheme p14 answers it in three points under (ii).',
         use=[0, 1, 2], tariff='questionTotal', total=8,
         checked='paper page 6, the second line of Q4(c)\'s list: "Grey cast '
                 'iron and white cast iron;" with "(iii) Upper critical '
                 'temperature (UCT) and lower critical temperature (LCT)." '
                 'beneath it; the semicolon is the list running on',
         notes="The scheme prints '8 marks'."),
    dict(key=(5, 'b', 'i'),
         replaces='the shipped card\'s only row was the tariff "Labels 1 + 1 + 1" '
                  'for ten marks',
         why='Scheme p16 answers with Graph 7 and prices it "Graph 7, Labels '
             '1 + 1 + 1"; no answer is written in words.',
         special={'kind': 'ask'}, total=10, stem=False,
         question_figure='engineering-2021-HL-paper-q5b-crop',
         figure='engineering-2021-HL-scheme-q5bi-sol',
         notes="The scheme prints 'Graph 7' and 'Labels 1 + 1 + 1'."),
    dict(key=(5, 'b', 'ii'),
         why='The diagram is the one the candidate draws in (b)(i) from the '
             'table printed above; scheme p17 answers with |AB|/|BC| = '
             '(75 - 52)/(100 - 75) = 23/25 as stacked fractions, read off its '
             'own Graph 7 (A, B, C at 200 deg C).',
         special={'kind': 'ask'}, total=4, stem=False, topic='eng-1-3',
         question_figure='engineering-2021-HL-paper-q5b-crop',
         figure='engineering-2021-HL-scheme-q5bii-sol'),
    dict(key=(5, 'b', 'iii'),
         replaces='the shipped row "205°C and becomes a solid alloy at 140°C" '
                  'was the second half of the scheme\'s sentence',
         why='Scheme p17 answers with one sentence over two lines and the '
             'cooling curve beside it.',
         lifted=[S(17, 100, 156, 336, 190)], marks=[4], total=4, stem=False,
         question_figure='engineering-2021-HL-paper-q5b-crop',
         figure='engineering-2021-HL-scheme-q5biii-sol'),
    dict(key=(7, 'c', 'i'),
         replaces='the shipped card carried the diagram\'s stage labels "1. '
                  'Parison 2. Clamping 3. Moulding 4. Finished" as a fifth '
                  'marking point and showed no diagram',
         why='Scheme p22 answers "Blow moulding:" in four numbered steps beside '
             'a diagram of the four stages.',
         lifted=[S(22, 100, 434, 290, 467), S(22, 100, 463, 290, 495),
                 S(22, 100, 493, 290, 525), S(22, 100, 522, 290, 555)],
         tariff='questionTotal', total=8,
         figure='engineering-2021-HL-scheme-q7ci-sol',
         notes="The scheme prints '8'."),
    dict(key=(9, 'a', 'ii'),
         why='Scheme p25 gives a "Suggested solution - other viable solutions '
             'are acceptable." -- a photograph of a scissor lift with callouts '
             'and a paragraph beside it; the reader drops the paragraph\'s '
             'second line and the markdown welds the callout "scissor" into its '
             'last, so the paragraph is lifted by rectangle.',
         lifted=[S(25, 300, 320, 550, 395)], marks=[8], total=8,
         figure='engineering-2021-HL-scheme-q9aii-sol',
         notes='The scheme prints: Suggested solution - other viable solutions '
               'are acceptable.'),
    dict(key=(9, 'b', 'ii'),
         why='"the toggle mechanism shown opposite" is the toggle clamp '
             'photographed on paper p11; no crop had been cut for it. Priced by '
             '"Any three @ 6 + 6 + 6" at (b).',
         use=[0], marks=[6], total=6,
         question_figure='engineering-2021-HL-paper-q9bii-crop'),
    dict(key=(2, 'd', 'ii'),
         replaces='the shipped card split the scheme\'s list "powered in three '
                  'different ways: either directly by the engine, by the '
                  'electric motor alone, or by both power sources working '
                  'together" into two fragment rows and dropped the third way',
         why='Scheme p9 answers in three paragraphs, the second ending on a '
             'three-bullet list; each paragraph is one row.',
         lifted=[S(9, 100, 112, 550, 165), S(9, 100, 162, 550, 246),
                 S(9, 100, 243, 550, 345)],
         tariff='questionTotal', total=8, question_figure='engineering-2021-HL-paper-q2di-art',
         notes="The scheme prints '8'."),
    dict(key=(2, 'e', None),
         replaces='the shipped question read "(i) Vehicle ownership; '
                  'transmission engine (ii) Environmental considerations; ..." '
                  '-- the hybrid diagram\'s callouts "transmission" and '
                  '"engine", printed just above (e), swept into its list',
         why='Paper p4 sets (e) and its three romans on five lines below the '
             '(d) diagram; the question is lifted from those lines alone.',
         question_lift=P(4, 95, 666, 570, 753),
         use=[[0, 1, 2]], row_kind='anyN', group=(2, 5), marks=[10],
         tariff='fixed', total=10, notes="The scheme prints 'Any two @ 5 + 5'."),
]

# Cards the automatic author files under the wrong syllabus heading.
TOPICS = {
    'eng-2021-hl-q3-c-ii': ('eng-3-8', 'a non-destructive test to locate internal '
                           'cavities in a welded joint is materials testing, not '
                           'joining; "weld" outvoted it'),
    'eng-2021-hl-q8-a-ii': ('eng-1-9', 'the scheme answers with polycarbonate\'s '
                           'properties -- transparent, tough, will not shatter -- '
                           'which the syllabus places under Plastics; "guards" '
                           'outvoted it'),
    'eng-2021-hl-q8-c-ii': ('eng-2-11', 'holding ferrous work for surface grinding '
                            '(a magnetic chuck), or the OR branch\'s CNC terms: '
                            'machining; "ferrous" outvoted it'),
}

_HYBRID = ('Hybrid vehicle technology. The reference files 2021 Higher Q2 under '
           'Energy, Electronics & Robotics, where hybrid drive belongs; the card\'s '
           'syllabus heading is Technology, where the syllabus lists hybrid vehicles.')

# Topic Atlas: cards whose question is not filed under a topic covering the
# card's syllabus heading, each decided on the card's content.
ATLAS = {
    **{f'eng-2021-hl-q2-{p}': dict(topics=['Energy, Electronics & Robotics'], note=_HYBRID)
       for p in ('a-i', 'a-ii', 'b-i', 'b-ii', 'b-iii', 'c', 'd-i', 'd-ii', 'e')},
    'eng-2021-hl-q4-b-ii': dict(
        topics=['Equilibrium Diagrams'],
        note='Reads pearlite off the iron-carbon diagram at 0.83% carbon, which '
             'is equilibrium-diagram work; the reference files Q4(b) there.'),
    'eng-2021-hl-q4-c-ii': dict(
        topics=['Metallurgy'],
        note='Grey and white cast iron: how each forms and what it is like. '
             'Neither topic Q4 is filed under (Equilibrium Diagrams, Heat '
             'Treatment) covers cast irons; Metallurgy, whose syllabus headings '
             'include Iron and steel, does.'),
    **{f'eng-2021-hl-q6-c-{p}': dict(
        topics=['Energy, Electronics & Robotics'],
        note='Robotic assisted surgery and the stepper motors that drive robotic '
             'arms: robotics, which the reference files Q6(c) under.')
       for p in ('i', 'ii')},
    'eng-2021-hl-q8-a-ii': dict(
        topics=['Polymers'],
        note='The advantages of polycarbonate for machine guards are a plastic\'s '
             'properties; Q8 is otherwise filed under Machining & Metrology only.'),
    'eng-2021-hl-q9-c-ii': dict(
        topics=['Mechanisms', 'Energy, Electronics & Robotics'],
        note='One card for the printed OR: the multi-directional forklift\'s design '
             '(Mechanisms) or offshore wind energy (Energy, Electronics & '
             'Robotics); the reference files Q9(c) under both.'),
}
