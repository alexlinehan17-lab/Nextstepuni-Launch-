"""2023 Higher Level: the parts eng_all refuses or gets wrong, from the page.

Paper LC027ALP000EV; scheme pages as the PDF numbers them.
"""
from eng_lift import lift

Y, L = 2023, 'hl'


def S(page, *rect):
    return lift(Y, L, 'scheme', page, rect)


CROPS = {
    # Paper p5: (b)'s sentence and its table of tensile results, as printed
    # (the cards had carried it as a line of numbers).
    'engineering-2023-HL-paper-q3b-crop': dict(
        doc='paper', page=5, rect=(66, 372, 545, 478), ref='2023 HL Q3(b)'),
    'engineering-2023-HL-paper-q1d-crop': dict(
        doc='paper', page=3, rect=(440, 200, 568, 310), ref='2023 HL Q1(d)'),
    'engineering-2023-HL-paper-q1g-crop': dict(
        doc='paper', page=3, rect=(484, 385, 560, 503), ref='2023 HL Q1(g)'),
    'engineering-2023-HL-paper-q1k-crop': dict(
        doc='paper', page=3, rect=(449, 556, 565, 671), ref='2023 HL Q1(k)'),
    'engineering-2023-HL-paper-q1m-crop': dict(
        doc='paper', page=3, rect=(408, 696, 571, 790), ref='2023 HL Q1(m)'),
    'engineering-2023-HL-paper-q5b-crop': dict(
        doc='paper', page=7, rect=(55, 303, 565, 410), ref='2023 HL Q5(b)'),
    # The component's own photograph: "machine." of (b)(ii) sets right under it.
    'engineering-2023-HL-paper-q8bi-crop': dict(
        doc='paper', page=10, rect=(481, 291, 556, 332), image=True,
        ref='2023 HL Q8(b)(i)'),
    'engineering-2023-HL-paper-q9bii-crop': dict(
        doc='paper', page=11, rect=(426, 237, 562, 335), ref='2023 HL Q9(b)(ii)'),
    'engineering-2023-HL-scheme-q3bi-sol': dict(
        doc='scheme', page=13, rect=(100, 92, 566, 391), solution=True,
        ref='2023 HL Q3(b)(i)'),
    'engineering-2023-HL-scheme-q3bii-sol': dict(
        doc='scheme', page=13, rect=(100, 458, 545, 494), solution=True,
        ref='2023 HL Q3(b)(ii)'),
    'engineering-2023-HL-scheme-q3biii-sol': dict(
        doc='scheme', page=13, rect=(100, 542, 545, 595), solution=True,
        ref='2023 HL Q3(b)(iii)'),
    'engineering-2023-HL-scheme-q4ai-sol': dict(
        doc='scheme', page=14, rect=(104, 424, 480, 590), solution=True,
        ref='2023 HL Q4(a)(i)'),
    'engineering-2023-HL-scheme-q4cii-sol': dict(
        doc='scheme', page=16, rect=(110, 350, 555, 520), solution=True,
        ref='2023 HL Q4(c)(ii)'),
    'engineering-2023-HL-scheme-q5bi-sol': dict(
        doc='scheme', page=17, rect=(80, 370, 560, 662), solution=True,
        ref='2023 HL Q5(b)(i)'),
    'engineering-2023-HL-scheme-q5bii-sol': dict(
        doc='scheme', page=18, rect=(100, 70, 400, 106), solution=True,
        ref='2023 HL Q5(b)(ii)'),
    'engineering-2023-HL-scheme-q5cii-sol': dict(
        doc='scheme', page=18, rect=(110, 470, 530, 568), solution=True,
        ref='2023 HL Q5(c)(ii)'),
    # Scheme p27: the compound and simple gear trains drawn and captioned.
    'engineering-2023-HL-scheme-q9bv-sol': dict(
        doc='scheme', page=27, rect=(100, 512, 500, 632), solution=True,
        ref='2023 HL Q9(b)(v)'),
}

CARDS = [
    dict(key=(1, 'd', None),
         why='"exercise foam rollers, as shown opposite" is the roller '
             'photographed and captioned beside (d); no crop had been cut. Scheme '
             'answers both properties in one line, "3 + 2".',
         use=[0], tariff='questionTotal', total=5,
         question_figure='engineering-2023-HL-paper-q1d-crop',
         notes="The scheme prints '3 + 2'."),
    dict(key=(1, 'g', None),
         why='"the Dyson air purifier shown" is photographed beside (g); the '
             'scheme lists three benefits for "3 + 2".',
         use=[0, 1, 2], tariff='orderedSplit', notation='3 + 2', ladder=5,
         question_figure='engineering-2023-HL-paper-q1g-crop'),
    dict(key=(1, 'k', None),
         why='"the wireless charging station shown opposite" is photographed '
             'beside (k); both benefits in one line, "3 + 2".',
         use=[0], tariff='questionTotal', total=5,
         question_figure='engineering-2023-HL-paper-q1k-crop',
         notes="The scheme prints '3 + 2'."),
    dict(key=(1, 'm', None),
         why='Wave energy names no syllabus heading the topic rules know; it is '
             'renewable energy, under Technology. The buoy is photographed '
             'beside (m).',
         topic='eng-3-14', use=[0], tariff='questionTotal', total=5,
         question_figure='engineering-2023-HL-paper-q1m-crop',
         notes="The scheme prints '3 + 2'."),
    dict(key=(3, 'b', 'i'),
         replaces='the shipped card\'s only row was the graph\'s axis numbers '
                  '"120 100 80 60 40 20 0.08 1.0 2.0 ..." for ten marks',
         why='Scheme p13 answers "Draw load-extension graph" with the graph.',
         special={'kind': 'ask'}, total=10, stem=False,
         question_figure='engineering-2023-HL-paper-q3b-crop',
         figure='engineering-2023-HL-scheme-q3bi-sol',
         notes="The scheme prints 'Draw load-extension graph', 10 marks."),
    dict(key=(3, 'b', 'ii'),
         replaces='the shipped card\'s only row was "C.S.A. π. (8²)", the '
                  'denominator of the scheme\'s fraction',
         why='Scheme p13 sets U.T.S. = Max. Load / C.S.A. = 135 / π(8²) = 0.67 '
             'kN/mm² as stacked fractions.',
         special={'kind': 'ask'}, total=4, stem=False,
         question_figure='engineering-2023-HL-paper-q3b-crop',
         figure='engineering-2023-HL-scheme-q3bii-sol'),
    dict(key=(3, 'b', 'iii'),
         replaces='the shipped row flattened the stacked fraction to "0.1% proof '
                  'stress = 84 = 0.42 kN/mm2 C.S.A" and lost "From the graph: 84 kN"',
         why='Scheme p13 reads 84 kN off the graph and divides by the C.S.A., as '
             'stacked fractions.',
         special={'kind': 'ask'}, total=4, stem=False,
         question_figure='engineering-2023-HL-paper-q3b-crop',
         figure='engineering-2023-HL-scheme-q3biii-sol'),
    dict(key=(4, 'a', 'i'),
         why='Scheme p14 gives a "Suggested answer other solutions accepted": '
             'pack carburising, a labelled diagram and four sentences; the reader '
             'welds the diagram\'s callouts into the first.',
         lifted=[S(14, 104, 595, 558, 627), S(14, 104, 628, 558, 644),
                 S(14, 104, 645, 558, 661), S(14, 104, 662, 558, 695)],
         tariff='questionTotal', total=8,
         figure='engineering-2023-HL-scheme-q4ai-sol',
         notes='The scheme prints: Suggested answer other solutions accepted. 8 marks.'),
    dict(key=(4, 'c', 'ii'),
         why='Scheme p16 answers in a two-column table, induction hardening '
             'beside flame hardening, with a diagram of each; the reader reads '
             'across the columns.',
         lifted=[S(16, 110, 174, 336, 337), S(16, 338, 174, 556, 322)],
         tariff='questionTotal', total=8,
         figure='engineering-2023-HL-scheme-q4cii-sol',
         notes="The scheme prints '8 marks'."),
    dict(key=(5, 'b', 'i'),
         why='Scheme p17 answers with the equilibrium diagram and prices it in '
             'two printed criteria, "Draw equilibrium diagram 9" and "Identify '
             'liquidus, solidus lines and eutectic point 3"; the reader welds the '
             'graph\'s axis into them.',
         lifted=[S(17, 410, 671, 548, 687), S(17, 300, 686, 548, 702)],
         row_kind='criterion', marks=[9, 3], total=12, stem=False,
         question_figure='engineering-2023-HL-paper-q5b-crop',
         figure='engineering-2023-HL-scheme-q5bi-sol'),
    dict(key=(5, 'b', 'ii'),
         why='The diagram is the candidate\'s own from (b)(i); scheme p18 '
             'answers |AB|/|BC| = 30/35 as stacked fractions.',
         special={'kind': 'ask'}, total=3, stem=False, topic='eng-1-3',
         question_figure='engineering-2023-HL-paper-q5b-crop',
         figure='engineering-2023-HL-scheme-q5bii-sol'),
    dict(key=(5, 'c', 'ii'),
         why='Scheme p18 answers in one sentence and two labelled cooling curves '
             'whose labels the reader welds into a second point.',
         use=[0], tariff='questionTotal', total=8,
         figure='engineering-2023-HL-scheme-q5cii-sol',
         notes="The scheme prints '8 marks'."),
    dict(key=(8, 'b', 'i'),
         why='"the component shown" is photographed beside (b)(i); the automatic '
             'crop clipped the next line\'s "machine" (eng_figures REJECTED).',
         use=[0, 1, 2], tariff='questionTotal', total=6,
         question_figure='engineering-2023-HL-paper-q8bi-crop',
         notes="The scheme prints '6 marks'."),
    dict(key=(9, 'b', 'ii'),
         why='"the amusement ride shown" is photographed beside (b); scheme p27 '
             'names three forces, any one of them the answer, and the reader '
             'takes the first for a heading.',
         lifted=[[S(27, 104, 72, 420, 88), S(27, 104, 89, 420, 105),
                  S(27, 104, 106, 420, 122)]],
         marks=[6], total=6,
         question_figure='engineering-2023-HL-paper-q9bii-crop',
         notes="The scheme prints '6 marks'."),
    dict(key=(9, 'b', 'v'),
         replaces='the shipped card\'s fourth row was the two drawings\' captions and the '
                  'tariff printed under them, "Compound gear reduction 9:1 Simple gear '
                  'reduction 3:1 (Any three) 6 + 6 + 6"',
         why='Scheme p27 answers in three paragraphs over two captioned drawings, shown '
             'with the answer; the part earns 6, "(Any three) 6 + 6 + 6" for (b).',
         topic='eng-2-15',
         lifted=[S(27, 105, 411, 545, 445), S(27, 105, 445, 545, 479),
                 S(27, 105, 478, 545, 512)],
         tariff='questionTotal', total=6,
         figure='engineering-2023-HL-scheme-q9bv-sol',
         notes="The scheme prints '(Any three) 6 + 6 + 6' for (b): each part answered earns 6."),
]

TOPICS = {
    'eng-2023-hl-q1-c': ('eng-3-12', 'specifying limits on component drawings is limits '
                         'and fits; "manufacture" outvoted it'),
}

_XR = ('Extended Reality (the 2023 Higher special topic), which the reference files '
       'Q2 under; the card\'s syllabus heading is Technology.')

ATLAS = {
    'eng-2023-hl-q1-b': dict(
        topics=['Energy, Electronics & Robotics'],
        note='A bridge rectifier is an electronic circuit, here in an arc welding '
             'set; the reference files Q1(b) under Energy, Electronics & Robotics.'),
    **{f'eng-2023-hl-q2-{p}': dict(topics=['Energy, Electronics & Robotics'], note=_XR)
       for p in ('a-i', 'a-ii', 'b', 'c', 'd', 'e')},
    'eng-2023-hl-q8-b-iv': dict(
        topics=['Machining & Metrology'],
        note='Additive manufacture against subtractive manufacture (machining), '
             'which the reference files Q8(b) under.'),
}
