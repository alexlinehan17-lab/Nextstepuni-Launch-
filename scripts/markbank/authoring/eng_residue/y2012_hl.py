"""2012 Higher Level: the parts eng_all refuses or gets wrong, from the page.

Paper and scheme as the PDFs number their pages (the scheme's printed "Page 1"
is its pdf page 3). The marks grid is on scheme p4: Question 1 is Section A,
"Any ten @ 5 marks each", and Section B, "Answer all of the following", (n) to
(r); Questions 2-8 are 50 marks each. The scheme prints a part's marks under
its answer ("(Any two) 3 + 2", "(Any three) 6 + 6 + 6"). This sitting had no
cards before the lane: every card here is new, and a `replaces=` names the
automatic card it rebuilds before it ever shipped.
"""
from eng_lift import cells, join, lift

Y, L = 2012, 'hl'
NEW = 'never shipped: the automatic card '


def S(page, *rect):
    return lift(Y, L, 'scheme', page, rect)


def P(page, *rect, more=(), items=()):
    return lift(Y, L, 'paper', page, rect, more=more, items=items)


def _ck(page, part, lead):
    return (f'Paper p{page} prints {part} as one item of the list under "{lead}"; the '
            'semicolon ends the item, not the question.')


# Paper stems the parts are lifted with.
_N1 = (125, 106, 520, 172)            # p4: Q1(n), the laser technologies
_O1 = (125, 236, 465, 255)            # p4: Q1(o), "The principle of a simple laser ..."
_Q1 = (125, 537, 500, 570)            # p4: Q1(q), Lasik
_C3 = (125, 470, 485, 488)            # p6: Q3(c), the iron-carbon diagram
_B4 = (125, 281, 470, 314)            # p7: Q4(b), the table
_C4 = (125, 571, 395, 588)            # p7: Q4(c), the line defect
_A5 = (125, 96, 370, 129)             # p8: Q5(a), SAW
_C5B = (125, 641, 400, 676)           # p8: the robot spot-welding (c)
_B6 = (125, 431, 505, 464)            # p9: Q6(b), thermoplastics and thermosets
_C7B = (125, 691, 535, 722)           # p10: the computer technology (c)
_C8B = (125, 655, 495, 672)           # p11: the IC microchip (c)

_SA = "Section A is 'Any ten @ 5 marks each'."
_SB = 'Section B is "Answer all of the following".'
_OR5 = ('The paper sets two (c)s either side of an OR: TIG or MMA welding, "(Any one) 16", '
        'carded at the letter, and the robot spot-welding (c), whose (i) and (ii) are carded '
        'apart.')
_OR7 = ('The paper sets two (c)s either side of an OR: loading and glazing, and forming and '
        'generating, "4 + 4" each and both asked, carded at the letter, and the computer '
        'technology (c), whose (i)-(iii) are carded apart.')
_OR8 = ('The paper sets two (c)s either side of an OR: the all-terrain vehicle\'s drive, '
        '"16", carded at the letter, and the IC microchip (c), whose (i) and (ii) are carded '
        'apart.')
_A5B = "The scheme prints '(Any three) 6 + 6 + 6': each part answered earns 6."
_A7 = "The scheme prints '(Any three) 6 + 6 + 6': each part answered earns 6."
_TB6 = ('The scheme answers in a table, a column for thermoplastics and one for thermosetting '
        'plastics; each row here is a column\'s head and its cell, joined.')

# Scheme p17: the heads of the table's two columns.
_THP = S(17, 135, 96, 320, 117)       # "Thermoplastics"
_TSP = S(17, 324, 96, 480, 117)       # "Thermosetting plastics"

CROPS = {
    # ---- paper ------------------------------------------------------------
    'engineering-2012-HL-paper-q1g-crop': dict(
        doc='paper', page=3, rect=(490, 430, 567, 531), image=True, ref='2012 HL Q1(g)'),
    # The laser with A, B and C, and the beam leaving C.
    'engineering-2012-HL-paper-q1o-crop': dict(
        doc='paper', page=4, rect=(140, 256, 465, 350), ref='2012 HL Q1(o)',
        letters=('A', 'B', 'C')),
    # The two impact tests, captioned A and B.
    'engineering-2012-HL-paper-q2a-crop': dict(
        doc='paper', page=5, rect=(145, 150, 450, 294), ref='2012 HL Q2(a)',
        letters=('A', 'B')),
    'engineering-2012-HL-paper-q2b-crop': dict(
        doc='paper', page=5, rect=(70, 418, 556, 523), ref='2012 HL Q2(b)'),
    'engineering-2012-HL-paper-q3c-crop': dict(
        doc='paper', page=6, rect=(105, 500, 490, 735), ref='2012 HL Q3(c)',
        letters=('A', 'B', 'C', 'D', 'X', 'Y')),
    'engineering-2012-HL-paper-q4b-crop': dict(
        doc='paper', page=7, rect=(45, 324, 564, 418), ref='2012 HL Q4(b)'),
    # The lattice with the shear-force arrows either side.
    'engineering-2012-HL-paper-q4c-crop': dict(
        doc='paper', page=7, rect=(215, 588, 398, 701), ref='2012 HL Q4(c)'),
    'engineering-2012-HL-paper-q5a-crop': dict(
        doc='paper', page=8, rect=(360, 124, 553, 287), ref='2012 HL Q5(a)'),
    # The OR branch's welding robot.
    'engineering-2012-HL-paper-q5cor-crop': dict(
        doc='paper', page=8, rect=(433, 636, 550, 753), image=True, ref='2012 HL Q5(c)'),
    'engineering-2012-HL-paper-q7b-crop': dict(
        doc='paper', page=10, rect=(178, 327, 500, 449), ref='2012 HL Q7(b)'),
    # The two mechanisms with their captions (i) and (ii).
    'engineering-2012-HL-paper-q8a-crop': dict(
        doc='paper', page=11, rect=(140, 128, 474, 274), ref='2012 HL Q8(a)'),
    'engineering-2012-HL-paper-q8c-crop': dict(
        doc='paper', page=11, rect=(366, 457, 554, 581), image=True, ref='2012 HL Q8(c)'),
    # ---- scheme: the drawings and tables the answers are given with --------
    # The gearwheel on the motor shaft with its labels; the answer's own three
    # lines, set beside the drawing's foot, are whited out.
    'engineering-2012-HL-scheme-q1m-sol': dict(
        doc='scheme', page=6, rect=(205, 552, 490, 718), mask=[(204, 646, 248, 696)],
        solution=True, ref='2012 HL Q1(m)'),
    'engineering-2012-HL-scheme-q2aii-sol': dict(
        doc='scheme', page=9, rect=(135, 262, 486, 476), solution=True, ref='2012 HL Q2(a)(ii)'),
    'engineering-2012-HL-scheme-q2cii-sol': dict(
        doc='scheme', page=10, rect=(76, 104, 284, 306), solution=True, ref='2012 HL Q2(c)(ii)'),
    # The four drawings beside the four answers: the two solid solutions, the
    # cooling curve and the solvus lines.
    'engineering-2012-HL-scheme-q4a-sol': dict(
        doc='scheme', parts=[(12, (429, 105, 526, 201)), (12, (423, 237, 521, 332)),
                             (12, (105, 378, 250, 490)), (12, (385, 570, 511, 666))],
        layout='row', solution=True, ref='2012 HL Q4(a)'),
    'engineering-2012-HL-scheme-q4bi-sol': dict(
        doc='scheme', page=13, rect=(130, 105, 492, 352), solution=True, ref='2012 HL Q4(b)'),
    'engineering-2012-HL-scheme-q4cii-sol': dict(
        doc='scheme', page=14, rect=(100, 165, 526, 297), solution=True, ref='2012 HL Q4(c)(ii)'),
    # The SAW set-up with its labels; the ends of the answer's lines, which run
    # into the box at its left edge, are whited out.
    'engineering-2012-HL-scheme-q5ai-sol': dict(
        doc='scheme', page=14, rect=(349, 452, 548, 676), mask=[(348, 466, 377, 600)],
        solution=True, ref='2012 HL Q5(a)(i)'),
    'engineering-2012-HL-scheme-q5c-sol': dict(
        doc='scheme', parts=[(15, (100, 389, 232, 545)), (15, (125, 589, 485, 668))],
        layout='row', solution=True, ref='2012 HL Q5(c)'),
    # The table's two heads over the structures drawn under (iii).
    'engineering-2012-HL-scheme-q6biii-sol': dict(
        doc='scheme', parts=[(17, (130, 94, 500, 119)), (17, (130, 300, 500, 445))],
        solution=True, ref='2012 HL Q6(b)(iii)'),
    'engineering-2012-HL-scheme-q6c-sol': dict(
        doc='scheme', page=18, rect=(110, 103, 485, 280), solution=True, ref='2012 HL Q6(c)'),
    'engineering-2012-HL-scheme-q8b-sol': dict(
        doc='scheme', page=20, rect=(462, 580, 568, 662), solution=True, ref='2012 HL Q8(b)'),
    'engineering-2012-HL-scheme-q8c-sol': dict(
        doc='scheme', page=21, rect=(50, 328, 488, 525), solution=True, ref='2012 HL Q8(c)'),
}

SPLIT = {
    'eng-2012-hl-q7-a': 'never shipped: "Answer any three of the following" over five '
                        'separate questions, each priced at 6; the automatic card ran all '
                        'five answers into one ordered split at the letter',
}

CARDS = [
    # ---- Question 1, Section A ("Any ten @ 5 marks each") ------------------
    dict(key=(1, 'a', None),
         why='The helmet is photographed beside (a); scheme p5 answers in one line under '
             '"Helmet guard process:", "5".',
         topic='eng-2-13',
         lifted=[S(5, 104, 202, 525, 221)], marks=[5], total=5,
         question_figure='engineering-2012-HL-paper-q1a-art',
         notes="The scheme prints '5'. " + _SA),
    dict(key=(1, 'b', None),
         why='Scheme p5 explains allotropy in one paragraph, "5".',
         topic='eng-1-3',
         lifted=[S(5, 104, 257, 525, 359)], marks=[5], total=5,
         notes="The scheme prints '5'. " + _SA),
    dict(key=(1, 'c', None),
         why='The three signs are pictured and captioned (i)-(iii); scheme p5 names each '
             'after its roman, "(Any two) 3 + 2".',
         topic='eng-3-1',
         question_lift=P(3, 125, 214, 420, 232),
         lifted=[S(5, 104, 396, 300, 411.5), S(5, 104, 411.5, 300, 425),
                 S(5, 104, 425, 300, 441)],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         question_figure='engineering-2012-HL-paper-q1c-art',
         notes="The scheme prints '(Any two) 3 + 2'. " + _SA),
    dict(key=(1, 'd', None),
         why='Scheme p5 bullets three issues, "(Any two) 3 + 2".',
         topic='eng-1-9',
         lifted=[S(5, 115, 495, 400, 509.5), S(5, 115, 509.5, 400, 524),
                 S(5, 115, 524, 400, 540)],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         notes="The scheme prints '(Any two) 3 + 2'. " + _SA),
    dict(key=(1, 'e', None),
         why='Scheme p5 describes the bond in one sentence, "5".',
         topic='eng-1-3',
         lifted=[S(5, 104, 577, 525, 610)], marks=[5], total=5,
         notes="The scheme prints '5'. " + _SA),
    dict(key=(1, 'f', None),
         why='Scheme p5 gives each conductor a line, "3 + 2".',
         topic='eng-1-2',
         lifted=[S(5, 104, 632, 525, 649), S(5, 104, 649, 525, 663)],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         notes="The scheme prints '3 + 2'. " + _SA),
    dict(key=(1, 'g', None),
         why='The jewellery is photographed beside (g); scheme p5 lists silver\'s properties '
             'in one sentence over two lines, each lifted by its own word rectangle; "(Any '
             'two) 3 + 2".',
         topic='eng-1-5',
         lifted=[S(5, 104, 687, 287.5, 707), S(5, 287.5, 687, 360.5, 707),
                 join(S(5, 360.5, 687, 525, 707), S(5, 104, 701, 165.5, 721)),
                 S(5, 165.5, 701, 400, 721)],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         question_figure='engineering-2012-HL-paper-q1g-crop',
         notes="The scheme prints '(Any two) 3 + 2'. " + _SA),
    dict(key=(1, 'h', None),
         why='Scheme p5 defines the term in one sentence, "5".',
         topic='eng-3-8',
         lifted=[S(5, 104, 742, 525, 762)], marks=[5], total=5,
         notes="The scheme prints '5'. " + _SA),
    dict(key=(1, 'i', None),
         why='Scheme p6 describes each cylinder in turn, "3 + 2". The scheme breaks "this" '
             'over a line end as "t" and "his"; lifted as printed.',
         topic='eng-2-15',
         lifted=[S(6, 104, 68, 525, 101), S(6, 104, 101, 525, 143)],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         notes="The scheme prints '3 + 2'. " + _SA),
    dict(key=(1, 'j', None),
         why='Scheme p6 expands each abbreviation after its roman; "(Any two) 3 + 2".',
         topic='eng-3-14',
         lifted=[S(6, 104, 166, 400, 182), S(6, 104, 182, 400, 195.5),
                 S(6, 104, 195.5, 400, 209), S(6, 104, 209, 400, 223)],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         notes="The scheme prints '(Any two) 3 + 2'. " + _SA),
    dict(key=(1, 'k', None),
         why='A lead-in over three people set as romans, "any one"; scheme p6 writes a note '
             'on each after the name, "(Any one) 5".',
         topic='eng-3-14',
         lifted=[[S(6, 104, 248, 525, 309), S(6, 104, 317, 525, 364),
                  S(6, 104, 372, 525, 419)]],
         row_kind='anyN', group=(1, 5), marks=[5], tariff='fixed', total=5,
         notes="The scheme prints '(Any one) 5'. " + _SA),
    dict(key=(1, 'l', None),
         why='Scheme p6 answers in one paragraph under "Evaluation in design:", "5".',
         topic='eng-3-14',
         lifted=[S(6, 104, 441, 525, 530)], marks=[5], total=5,
         notes="The scheme prints '5'. " + _SA),
    dict(key=(1, 'm', None),
         why='The motor is photographed beside (m); scheme p6 gives a "suggested solution:", '
             'a labelled drawing, shown with the answer, and three lines under it; "5". The '
             'reader takes the page footer and Section B\'s heading for (m)\'s stem.',
         topic='eng-2-15', stem=False,
         lifted=[S(6, 104, 648, 250, 695)], marks=[5], total=5,
         question_figure='engineering-2012-HL-paper-q1m-art',
         figure='engineering-2012-HL-scheme-q1m-sol',
         notes="The scheme prints '5' under 'suggested solution:'. " + _SA),
    # ---- Question 1, Section B ("Answer all of the following") -------------
    dict(key=(1, 'n', 'i'),
         why='Scheme p7 bullets two examples under "Entertainment", "5 + 5", 5 for the part; '
             'one example asked.',
         topic='eng-3-14', stem=False,
         question_lift=P(4, *_N1, more=[(165, 176, 300, 193)]),
         lifted=[[S(7, 155, 127, 525, 142), S(7, 155, 142, 525, 158)]],
         row_kind='anyN', group=(1, 5), marks=[5], tariff='fixed', total=5,
         notes="The scheme prints '5 + 5', for (i) and (ii) in that order. " + _SB),
    dict(key=(1, 'n', 'ii'),
         why='Scheme p7 bullets four examples under "Industry", "5 + 5", 5 for the part; one '
             'example asked.',
         topic='eng-3-14', stem=False,
         question_lift=P(4, *_N1, more=[(165, 192, 300, 209)]),
         lifted=[[S(7, 155, 184, 525, 211), S(7, 155, 211, 525, 240), S(7, 155, 240, 525, 255),
                  S(7, 155, 255, 525, 270)]],
         row_kind='anyN', group=(1, 5), marks=[5], tariff='fixed', total=5,
         notes="The scheme prints '5 + 5', for (i) and (ii) in that order. " + _SB),
    dict(key=(1, 'o', 'i'),
         why='The laser is drawn with parts A, B and C; scheme p7 names each after its '
             'letter, "1 + 1 + 1".',
         topic='eng-3-14', stem=False,
         question_lift=P(4, *_O1, more=[(170, 348, 300, 365)]),
         lifted=[S(7, 140, 311, 525, 325), S(7, 140, 325, 525, 339), S(7, 140, 339, 525, 355)],
         marks=[1, 1, 1], total=3,
         labels={'A': S(7, 162, 311, 525, 325), 'B': S(7, 162, 325, 525, 339),
                 'C': S(7, 162, 339, 525, 355)},
         question_figure='engineering-2012-HL-paper-q1o-crop',
         notes="The scheme prints '1 + 1 + 1'. " + _SB),
    dict(key=(1, 'o', 'ii'),
         why='Scheme p7 describes the operation in four paragraphs under "Principle of '
             'operation:", "5".',
         topic='eng-3-14', stem=False,
         question_lift=P(4, *_O1, more=[(170, 364, 410, 381)]),
         lifted=[S(7, 140, 405, 525, 604)], marks=[5], total=5,
         question_figure='engineering-2012-HL-paper-q1o-crop',
         notes="The scheme prints '5'. " + _SB),
    dict(key=(1, 'o', 'iii'),
         why='Scheme p7 lists sources of energy on one line, each lifted by its own word '
             'rectangle; "1 + 1".',
         topic='eng-3-14', stem=False,
         question_lift=P(4, *_O1, more=[(170, 380, 395, 397)]),
         lifted=[S(7, 140, 653, 166.5, 673), S(7, 166.5, 653, 195.5, 673),
                 S(7, 195.5, 653, 220.5, 673), S(7, 220.5, 653, 349.5, 673),
                 S(7, 349.5, 653, 450, 673)],
         tariff='orderedSplit', notation='1 + 1', ladder=2, total=2,
         question_figure='engineering-2012-HL-paper-q1o-crop',
         notes="The scheme prints '1 + 1'. " + _SB),
    dict(key=(1, 'p', None),
         why='The three properties are bulleted on the paper; scheme p8 explains each under '
             'its name, "(Any two) 5 + 5". The question is lifted with its list on its lines, '
             'as printed.',
         topic='eng-3-14', stem=False,
         question_lift=P(4, 125, 423, 525, 441, items=[(165, 440, 300, 457),
                                                        (165, 457, 300, 474),
                                                        (165, 474, 300, 491),
                                                        (135, 489, 330, 507)]),
         lifted=[[S(8, 104, 67, 525, 115), S(8, 104, 123, 525, 156), S(8, 104, 164, 525, 211)]],
         row_kind='anyN', group=(2, 5), marks=[10], tariff='fixed', total=10,
         notes="The scheme prints '(Any two) 5 + 5'. " + _SB),
    dict(key=(1, 'q', 'i'),
         why='The eye is photographed beside (q); scheme p8 lists four properties on one '
             'line, each lifted by its own word rectangle; "3 + 2".',
         topic='eng-3-14', stem=False,
         question_lift=P(4, *_Q1, more=[(165, 574, 365, 607)]),
         lifted=[S(8, 140, 261, 194.5, 281), S(8, 194.5, 261, 244.5, 281),
                 S(8, 244.5, 261, 334.5, 281), S(8, 334.5, 261, 515, 281)],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         question_figure='engineering-2012-HL-paper-q1qi-art',
         notes="The scheme prints '3 + 2'. " + _SB),
    dict(key=(1, 'q', 'ii'),
         why='Scheme p8 bullets four advantages under a lead-in, "3 + 2".',
         topic='eng-3-14', stem=False,
         question_lift=P(4, *_Q1, more=[(165, 622, 365, 655)]),
         lifted=[S(8, 155, 334, 525, 348), S(8, 155, 348, 525, 362), S(8, 155, 362, 525, 391),
                 S(8, 155, 391, 525, 407)],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         question_figure='engineering-2012-HL-paper-q1qi-art',
         notes="The scheme prints '3 + 2'. " + _SB),
    dict(key=(1, 'r', None),
         why='A lead-in over three topics set as romans, "any two"; scheme p8 answers each '
             'under its roman, "(Any two) 5 + 5".',
         topic='eng-3-14',
         lifted=[[S(8, 140, 471, 525, 519), S(8, 140, 526, 525, 588), S(8, 140, 595, 525, 643)]],
         row_kind='anyN', group=(2, 5), marks=[10], tariff='fixed', total=10,
         notes="The scheme prints '(Any two) 5 + 5'. " + _SB),
    # ---- Question 2 --------------------------------------------------------
    dict(key=(2, 'a', 'ii'),
         why='The two tests are drawn and captioned A and B; scheme p9 compares them in a '
             'two-column table, shown with the answer, "10" for the part. Each row is the '
             'table\'s row, its two cells joined.',
         topic='eng-3-8',
         lifted=[cells(S(9, 140, 312, 320, 332), S(9, 320, 300, 520, 320)),
                 cells(S(9, 140, 338, 320, 358), S(9, 320, 338, 520, 358)),
                 cells(S(9, 140, 364, 320, 384), S(9, 320, 364, 520, 384)),
                 cells(S(9, 140, 391, 320, 424), S(9, 320, 391, 520, 424)),
                 cells(S(9, 140, 431, 320, 464), S(9, 320, 431, 520, 464))],
         tariff='questionTotal', total=10,
         question_figure='engineering-2012-HL-paper-q2a-crop',
         figure='engineering-2012-HL-scheme-q2aii-sol',
         notes="The scheme prints '10'. Its table is headed 'Impact test A' and 'Impact test "
               "B'; each row gives A's cell first."),
    dict(key=(2, 'b', 'i'),
         why='The three stress-strain graphs are drawn under (b); scheme p9 gives each metal '
             'a line, "3 + 3 + 3".',
         topic='eng-3-8',
         lifted=[S(9, 140, 538, 525, 555), S(9, 140, 555, 525, 569), S(9, 140, 569, 525, 584)],
         marks=[3, 3, 3], total=9,
         question_figure='engineering-2012-HL-paper-q2b-crop',
         notes="The scheme prints '3 + 3 + 3', for brass, copper and mild steel in that "
               "order."),
    dict(key=(2, 'c', 'i'),
         why='Scheme p9 names two tests after each heading on one line, each lifted by its '
             'own word rectangle with its heading; "2 + 2 + 2 + 2".',
         topic='eng-3-8',
         lifted=[join(S(9, 140, 731, 260.5, 748), S(9, 260.5, 731, 347.5, 748)),
                 join(S(9, 140, 731, 260.5, 748), S(9, 347.5, 731, 420, 748)),
                 join(S(9, 140, 748, 219.5, 765), S(9, 219.5, 748, 339.5, 765)),
                 join(S(9, 140, 748, 219.5, 765), S(9, 339.5, 748, 400, 765))],
         marks=[2, 2, 2, 2], total=8,
         notes="The scheme prints '2 + 2 + 2 + 2'."),
    dict(key=(2, 'c', 'ii'),
         replaces=NEW + 'set the ultrasonic sentence as a second point under one question '
                        'total, left out the drawing the description is set beside, and filed '
                        'the test under joining',
         why='Scheme p10 describes radiography beside a labelled drawing, shown with the '
             'answer; "10".',
         topic='eng-3-8',
         lifted=[join(S(10, 125, 82, 300, 102), S(10, 286, 109, 525, 253))],
         marks=[10], total=10,
         figure='engineering-2012-HL-scheme-q2cii-sol',
         notes="The scheme prints '10', and adds 'Ultrasonic testing is another suitable "
               "method to check for internal faults in welded joints.'"),
    # ---- Question 3 --------------------------------------------------------
    dict(key=(3, 'a', None),
         replaces=NEW + 'split the answers into ten options, one of them the scheme\'s '
                        '"(Any two) 8 + 8"',
         why='A lead-in over three processes set as romans, "any two"; scheme pp10-11 '
             'answer each under its roman, one option each, "(Any two) 8 + 8".',
         topic='eng-2-6',
         lifted=[[S(10, 140, 459, 525, 619), S(10, 140, 641, 525, 716),
                  S(11, 140, 83, 525, 241)]],
         row_kind='anyN', group=(2, 8), marks=[16], tariff='fixed', total=16,
         notes="The scheme prints '(Any two) 8 + 8'."),
    dict(key=(3, 'c', 'i'),
         why='The diagram is drawn with regions A-D; scheme p11 names each after its letter, '
             '"2 + 2 + 2 + 2".',
         topic='eng-1-3', stem=False,
         question_lift=P(6, *_C3, more=[(160, 734, 365, 751)]),
         lifted=[S(11, 140, 472, 525, 486), S(11, 140, 486, 525, 500), S(11, 140, 500, 525, 514),
                 S(11, 140, 514, 525, 528)],
         marks=[2, 2, 2, 2], total=8,
         labels={'A': S(11, 160, 472, 525, 486), 'B': S(11, 160, 486, 525, 500),
                 'C': S(11, 160, 500, 525, 514), 'D': S(11, 160, 514, 525, 528)},
         question_figure='engineering-2012-HL-paper-q3c-crop',
         notes="The scheme prints '2 + 2 + 2 + 2'."),
    dict(key=(3, 'c', 'ii'),
         replaces=NEW + 'read the scheme\'s "(Name and Describe) 3 + 2" into its rows, one of '
                        'them that tariff alone',
         why='Scheme p11 names each point after its letter and then describes it, "(Name and '
             'Describe) 3 + 2" under each; the name and the description are lifted apart.',
         topic='eng-1-3', stem=False,
         question_lift=P(6, *_C3, more=[(160, 755, 370, 772)]),
         lifted=[S(11, 140, 580, 247.5, 598),
                 join(S(11, 247.5, 580, 525, 596), S(11, 140, 596, 525, 627)),
                 S(11, 140, 649, 239.5, 667),
                 join(S(11, 239.5, 649, 525, 665), S(11, 140, 665, 525, 690))],
         marks=[3, 2, 3, 2], total=10,
         labels={'X': S(11, 162, 580, 247.5, 598), 'Y': S(11, 162, 649, 239.5, 667)},
         question_figure='engineering-2012-HL-paper-q3c-crop',
         notes="The scheme prints '(Name and Describe) 3 + 2' under each of X and Y."),
    # ---- Question 4 --------------------------------------------------------
    dict(key=(4, 'a', None),
         replaces=NEW + 'split the answers into nine options, one of them the scheme\'s '
                        '"(Any two) 8 + 8", and left out the solvus answer',
         why='A lead-in over four topics set as romans, "any two"; scheme p12 answers each '
             'under its roman, three of them beside drawings, shown with the answer; one '
             'option each, "(Any two) 8 + 8". The drawings\' own labels are left out of the '
             'words.',
         topic='eng-1-3',
         lifted=[[S(12, 140, 110, 426, 337),
                  join(S(12, 140, 358, 300, 378), S(12, 250, 386, 525, 433)),
                  S(12, 140, 510, 525, 543), S(12, 140, 565, 385, 668)]],
         row_kind='anyN', group=(2, 8), marks=[16], tariff='fixed', total=16,
         figure='engineering-2012-HL-scheme-q4a-sol',
         notes="The scheme prints '(Any two) 8 + 8'."),
    dict(key=(4, 'b', 'i'),
         why='"Draw the thermal equilibrium diagram": scheme p13 answers with the drawn '
             'diagram, shown with the answer, "10".',
         topic='eng-1-3', stem=False,
         question_lift=P(7, *_B4, more=[(160, 433, 510, 466)]),
         special={'kind': 'ask'}, total=10,
         question_figure='engineering-2012-HL-paper-q4b-crop',
         figure='engineering-2012-HL-scheme-q4bi-sol',
         notes="The scheme prints '10'."),
    dict(key=(4, 'b', 'ii'),
         why='Scheme p13 describes seven features, each under its name, which the diagram '
             'drawn for (i) labels, shown with the answer; "5 + 5" for the part.',
         topic='eng-1-3', stem=False,
         question_lift=P(7, *_B4, more=[(160, 473, 425, 490)]),
         lifted=[S(13, 140, 400, 525, 420), S(13, 140, 420, 525, 454), S(13, 140, 455, 525, 475),
                 S(13, 140, 475, 525, 495), S(13, 140, 496, 525, 530), S(13, 140, 531, 525, 578),
                 S(13, 140, 579, 525, 613)],
         tariff='questionTotal', total=10,
         question_figure='engineering-2012-HL-paper-q4b-crop',
         figure='engineering-2012-HL-scheme-q4bi-sol',
         notes="The scheme prints '5 + 5' for the part, without saying which marks the labels "
               "earn and which the descriptions."),
    dict(key=(4, 'c', 'i'),
         why='The line defect is drawn under (c); scheme p14 names it and then describes it, '
             '"4 + 4".',
         topic='eng-1-3', stem=False,
         question_lift=P(7, *_C4, more=[(160, 716, 330, 733)]),
         lifted=[S(14, 140, 69, 300, 89), S(14, 140, 83, 525, 144)],
         marks=[4, 4], total=8,
         question_figure='engineering-2012-HL-paper-q4c-crop',
         notes="The scheme prints '4 + 4', for the name and the description in that order."),
    dict(key=(4, 'c', 'ii'),
         why='Scheme p14 draws the dislocation moving under the shear force, shown with the '
             'answer, and explains it in one paragraph; "4".',
         topic='eng-1-3', stem=False,
         question_lift=P(7, *_C4, more=[(160, 737, 440, 754)]),
         lifted=[S(14, 140, 303, 525, 351)], marks=[4], total=4,
         question_figure='engineering-2012-HL-paper-q4c-crop',
         figure='engineering-2012-HL-scheme-q4cii-sol',
         notes="The scheme prints '4'."),
    # ---- Question 5 --------------------------------------------------------
    dict(key=(5, 'a', 'i'),
         replaces=NEW + 'left out the drawing the description is set beside, and the '
                        'question\'s own "is illustrated" and its picture',
         why='The SAW set-up is drawn beside (a); scheme p14 describes the process beside a '
             'labelled drawing, shown with the answer, "12". The drawing\'s labels are left '
             'out of the words.',
         topic='eng-2-10', stem=False,
         question_lift=P(8, *_A5, more=[(160, 136, 340, 167)]),
         lifted=[S(14, 140, 467, 377, 627)], marks=[12], total=12,
         question_figure='engineering-2012-HL-paper-q5a-crop',
         figure='engineering-2012-HL-scheme-q5ai-sol',
         notes="The scheme prints '12'."),
    dict(key=(5, 'b', 'i'),
         checked=_ck(8, '(b)(i)', 'Answer any three of the following:'),
         why='One of "Answer any three of the following": scheme p15 answers in one '
             'paragraph under its heading.',
         topic='eng-2-10',
         lifted=[S(15, 140, 69, 525, 116)], marks=[6], total=6, notes=_A5B),
    dict(key=(5, 'b', 'ii'),
         checked=_ck(8, '(b)(ii)', 'Answer any three of the following:'),
         why='One of "Answer any three of the following": scheme p15 gives four precautions, '
             'one a line, under its heading, the 6 for the part not split between them.',
         topic='eng-2-10',
         lifted=[S(15, 140, 155, 525, 168.5), S(15, 140, 168.5, 525, 182),
                 S(15, 140, 182, 525, 196), S(15, 140, 196, 525, 212)],
         tariff='questionTotal', total=6, notes=_A5B),
    dict(key=(5, 'b', 'iii'),
         checked=_ck(8, '(b)(iii)', 'Answer any three of the following:'),
         why='One of "Answer any three of the following": scheme p15 answers in one '
             'paragraph under its heading.',
         topic='eng-2-10',
         lifted=[S(15, 140, 220, 525, 282)], marks=[6], total=6, notes=_A5B),
    dict(key=(5, 'b', 'iv'),
         replaces=NEW + 'read the tariff "(Any three) 6 + 6 + 6" as its answer',
         why='One of "Answer any three of the following": scheme p15 names two types on one '
             'line, each lifted by its own word rectangle; one type asked.',
         topic='eng-2-10',
         lifted=[[S(15, 140, 289, 272.5, 309), S(15, 272.5, 289, 350, 309)]],
         row_kind='anyN', group=(1, 6), marks=[6], tariff='fixed', total=6, notes=_A5B),
    dict(key=(5, 'c', None),
         why='Paper p8 sets two alternative (c)s either side of an OR. This card is the '
             'first: "the main features of one of the following", TIG or MMA welding; scheme '
             'pp15-16 describe each beside a labelled drawing, shown with the answer, "(Any '
             'one) 16".',
         topic='eng-2-10', stem=False,
         question_lift=P(8, 125, 504, 490, 535, items=[(135, 539, 340, 556),
                                                       (135, 559, 340, 577)]),
         lifted=[[join(S(15, 140, 372, 340, 392), S(15, 268, 414, 525, 516)),
                  join(S(15, 140, 571, 340, 591), S(15, 140, 668, 525, 784),
                       S(16, 140, 68, 525, 129))]],
         row_kind='anyN', group=(1, 16), marks=[16], tariff='fixed', total=16,
         figure='engineering-2012-HL-scheme-q5c-sol',
         notes="The scheme prints '(Any one) 16'. " + _OR5),
    dict(key=(5, 'c', 'i'),
         replaces=NEW + 'ran the first branch\'s TIG answer and this branch\'s answer into one '
                        'question total',
         why='The OR branch\'s (i): scheme p16 gives four reasons, one a line, over one "8".',
         topic='eng-2-10', stem=False,
         question_lift=P(8, *_C5B, more=[(160, 682, 420, 715)]),
         lifted=[S(16, 140, 222, 525, 236.5), S(16, 140, 236.5, 525, 250),
                 S(16, 140, 250, 525, 264), S(16, 140, 264, 525, 280)],
         tariff='questionTotal', total=8,
         question_figure='engineering-2012-HL-paper-q5cor-crop',
         notes="The scheme prints '8'. " + _OR5),
    dict(key=(5, 'c', 'ii'),
         why='The OR branch\'s (ii): scheme p16 lists five processes on one line, each lifted '
             'by its own word rectangle; "4 + 4".',
         topic='eng-2-10', stem=False,
         question_lift=P(8, *_C5B, more=[(160, 720, 400, 754)]),
         lifted=[S(16, 140, 311, 188.5, 331), S(16, 188.5, 311, 272.5, 331),
                 S(16, 272.5, 311, 330.5, 331), S(16, 330.5, 311, 411.5, 331),
                 S(16, 411.5, 311, 510, 331)],
         tariff='orderedSplit', notation='4 + 4', ladder=8, total=8,
         question_figure='engineering-2012-HL-paper-q5cor-crop',
         notes="The scheme prints '4 + 4'. " + _OR5),
    # ---- Question 6 --------------------------------------------------------
    dict(key=(6, 'a', 'iii'),
         why='Scheme p16 names two components on one line, each lifted by its own word '
             'rectangle; one asked, "4".',
         topic='eng-1-9',
         lifted=[[S(16, 140, 725, 180.5, 745), S(16, 180.5, 725, 230, 745)]],
         row_kind='anyN', group=(1, 4), marks=[4], tariff='fixed', total=4,
         question_figure='engineering-2012-HL-paper-q6ai-art',
         notes="The scheme prints '4'."),
    dict(key=(6, 'b', 'i'),
         why='Scheme p17 answers in a table under the roman\'s heading, a cell for each kind '
             'of plastic, "2 + 2".',
         topic='eng-1-9', stem=False,
         question_lift=P(9, *_B6, more=[(170, 476, 300, 493)]),
         lifted=[cells(_THP, S(17, 135, 155, 320, 173)), cells(_TSP, S(17, 324, 155, 480, 173))],
         marks=[2, 2], total=4,
         notes="The scheme prints '2 + 2'. " + _TB6),
    dict(key=(6, 'b', 'ii'),
         why='Scheme p17 answers in a table under the roman\'s heading, a cell for each kind '
             'of plastic, "2 + 2".',
         topic='eng-1-9', stem=False,
         question_lift=P(9, *_B6, more=[(170, 497, 300, 514)]),
         lifted=[cells(_THP, S(17, 135, 197, 320, 242)), cells(_TSP, S(17, 324, 197, 505, 242))],
         marks=[2, 2], total=4,
         notes="The scheme prints '2 + 2'. " + _TB6),
    dict(key=(6, 'b', 'iii'),
         why='Scheme p17 answers in a table under the roman\'s heading, a cell for each kind '
             'of plastic, with the structures drawn under them, shown with the answer; '
             '"2 + 2".',
         topic='eng-1-9', stem=False,
         question_lift=P(9, *_B6, more=[(170, 517, 300, 535)]),
         lifted=[cells(_THP, S(17, 135, 266, 320, 298)), cells(_TSP, S(17, 324, 266, 495, 283))],
         marks=[2, 2], total=4,
         figure='engineering-2012-HL-scheme-q6biii-sol',
         notes="The scheme prints '2 + 2'. " + _TB6),
    dict(key=(6, 'b', 'iv'),
         replaces=NEW + 'ran the table\'s two columns of properties into one list, one '
                        'property split over two rows',
         why='Scheme p17 bullets each kind of plastic\'s properties in its own column of the '
             'table, "2 + 2": a property from each column, each with its column\'s head.',
         topic='eng-1-9', stem=False,
         question_lift=P(9, *_B6, more=[(170, 538, 300, 555)]),
         lifted=[[cells(_THP, S(17, 165, 489, 320, 503.5)), cells(_THP, S(17, 165, 503.5, 320, 518)),
                  cells(_THP, S(17, 165, 518, 320, 532.5)), cells(_THP, S(17, 165, 532.5, 320, 547)),
                  cells(_THP, S(17, 165, 547, 320, 589)), cells(_THP, S(17, 165, 589, 320, 605))],
                 [cells(_TSP, S(17, 355, 489, 535, 503.5)), cells(_TSP, S(17, 355, 503.5, 535, 518)),
                  cells(_TSP, S(17, 355, 518, 535, 532.5)), cells(_TSP, S(17, 355, 532.5, 535, 561)),
                  cells(_TSP, S(17, 355, 561, 535, 577))]],
         row_kind='anyN', group=[(1, 2), (1, 2)], marks=[2, 2], tariff='fixed', total=4,
         notes="The scheme prints '2 + 2'. " + _TB6),
    dict(key=(6, 'c', None),
         replaces=NEW + 'split the GRP answer into two options, cut blow moulding off at its '
                        'first sentence and took "(Any three) 6 + 6 + 6" for an option',
         why='A lead-in over five terms set as romans, "any three"; scheme pp17-18 answer '
             'each under its roman, blow moulding beside a labelled drawing, shown with the '
             'answer; one option each, "(Any three) 6 + 6 + 6".',
         topic='eng-1-9',
         lifted=[[S(17, 140, 647, 525, 709), S(17, 140, 716, 525, 750),
                  join(S(18, 140, 68, 525, 102), S(18, 140, 287, 525, 334)),
                  S(18, 140, 356, 525, 403), S(18, 140, 425, 525, 472)]],
         row_kind='anyN', group=(3, 6), marks=[18], tariff='fixed', total=18,
         figure='engineering-2012-HL-scheme-q6c-sol',
         notes="The scheme prints '(Any three) 6 + 6 + 6'."),
    # ---- Question 7 --------------------------------------------------------
    dict(key=(7, 'a', 'i'),
         checked=_ck(10, '(a)(i)', 'Answer any three of the following:'),
         why='One of "Answer any three of the following": scheme p18 gives three benefits, '
             'one a sentence, the 6 for the part not split between them.',
         topic='eng-2-11',
         lifted=[S(18, 140, 621, 525, 635), S(18, 140, 635, 525, 662), S(18, 140, 662, 525, 678)],
         tariff='questionTotal', total=6, notes=_A7),
    dict(key=(7, 'a', 'ii'),
         checked=_ck(10, '(a)(ii)', 'Answer any three of the following:'),
         why='One of "Answer any three of the following": scheme p18 answers in one '
             'paragraph.',
         topic='eng-2-11',
         lifted=[S(18, 140, 687, 525, 762)], marks=[6], total=6, notes=_A7),
    dict(key=(7, 'a', 'iii'),
         checked=_ck(10, '(a)(iii)', 'Answer any three of the following:'),
         why='One of "Answer any three of the following": scheme p19 answers in one '
             'paragraph.',
         topic='eng-3-12',
         lifted=[S(19, 140, 68, 525, 130)], marks=[6], total=6, notes=_A7),
    dict(key=(7, 'a', 'iv'),
         checked=_ck(10, '(a)(iv)', 'Answer any three of the following:'),
         why='One of "Answer any three of the following": scheme p19 answers in one '
             'sentence.',
         topic='eng-2-11',
         lifted=[S(19, 140, 137, 525, 171)], marks=[6], total=6, notes=_A7),
    dict(key=(7, 'a', 'v'),
         why='One of "Answer any three of the following": scheme p19 lists the advantages and '
             'the disadvantages after their headings, the 6 for the part not split.',
         topic='eng-2-11',
         lifted=[S(19, 140, 180, 525, 209), S(19, 140, 209, 525, 240)],
         tariff='questionTotal', total=6, notes=_A7),
    dict(key=(7, 'b', 'i'),
         why='The machine and its lubricant reservoir are pictured beside (b); scheme p19 '
             'gives three reasons, one a line, under "Two reasons explained such as:"; '
             '"4 + 4".',
         topic='eng-2-15',
         lifted=[S(19, 140, 306, 525, 320), S(19, 140, 320, 525, 334), S(19, 140, 334, 525, 350)],
         tariff='orderedSplit', notation='4 + 4', ladder=8, total=8,
         question_figure='engineering-2012-HL-paper-q7b-crop',
         notes="The scheme prints '4 + 4'."),
    dict(key=(7, 'b', 'ii'),
         why='Scheme p19 names three materials, one a line, "4 + 4".',
         topic='eng-2-15',
         lifted=[S(19, 140, 389, 525, 403), S(19, 140, 403, 525, 416.5),
                 S(19, 140, 416.5, 525, 432)],
         tariff='orderedSplit', notation='4 + 4', ladder=8, total=8,
         question_figure='engineering-2012-HL-paper-q7b-crop',
         notes="The scheme prints '4 + 4'."),
    dict(key=(7, 'c', None),
         why='Paper p10 sets two alternative (c)s either side of an OR. This card is the '
             'first, which asks both its romans: scheme p19 describes loading and glazing, '
             '"4 + 4", and forming and generating, "4 + 4", each term under its own name.',
         topic='eng-2-11', stem=False,
         question_lift=P(10, 125, 562, 495, 595, items=[(140, 601, 380, 618),
                                                        (140, 622, 360, 639)]),
         lifted=[S(19, 140, 468, 525, 512), S(19, 140, 512, 525, 584),
                 S(19, 140, 620, 525, 649), S(19, 140, 649, 525, 695)],
         marks=[4, 4, 4, 4], total=16,
         notes="The scheme prints '4 + 4' under (i) and '4 + 4' under (ii), for each term "
               "in the order the paper names them. " + _OR7),
    dict(key=(7, 'c', 'i'),
         why='The OR branch\'s (i): scheme p20 answers in one sentence after its heading, '
             '"6".',
         topic='eng-3-14', stem=False,
         question_lift=P(10, *_C7B, more=[(170, 725, 300, 743)]),
         lifted=[S(20, 140, 89, 512, 123)], marks=[6], total=6,
         notes="The scheme prints '6'. " + _OR7),
    dict(key=(7, 'c', 'ii'),
         why='The OR branch\'s (ii): scheme p20 answers in one sentence after its heading, '
             '"5".',
         topic='eng-3-14', stem=False,
         question_lift=P(10, *_C7B, more=[(170, 746, 300, 763)]),
         lifted=[S(20, 140, 131, 512, 177)], marks=[5], total=5,
         notes="The scheme prints '5'. " + _OR7),
    dict(key=(7, 'c', 'iii'),
         replaces=NEW + 'ran both branches\' questions into one',
         why='The OR branch\'s (iii): scheme p20 answers in one sentence after its heading, '
             '"5".',
         topic='eng-2-13', stem=False,
         question_lift=P(10, *_C7B, more=[(170, 767, 300, 784)]),
         lifted=[S(20, 140, 186, 525, 220)], marks=[5], total=5,
         notes="The scheme prints '5'. " + _OR7),
    # ---- Question 8 --------------------------------------------------------
    dict(key=(8, 'a', None),
         why='"Any one of the mechanisms shown", photographed and captioned (i) and (ii); '
             'scheme p20 names each under its roman and describes its operation, "(Any one) '
             'Name 8, Operation 8". The name and the operation are each any one of the two.',
         topic='eng-2-15',
         lifted=[[S(20, 140, 351, 260, 371), S(20, 140, 420, 300, 440)],
                 [S(20, 140, 365, 525, 413), S(20, 140, 434, 525, 468)]],
         marks=[8, 8], total=16,
         question_figure='engineering-2012-HL-paper-q8a-crop',
         notes="The scheme prints '(Any one) Name 8, Operation 8', for the mechanism "
               "chosen."),
    dict(key=(8, 'b', None),
         replaces=NEW + 'split the idler gear answer into two options and took "(Any three) '
                        '6 + 6 + 6" for an option',
         why='A lead-in over five topics set as romans, "any three"; scheme pp20-21 answer '
             'each under its heading, the idler gear beside a labelled picture, shown with the '
             'answer; one option each, "(Any three) 6 + 6 + 6". The headings, which restate '
             'the topics, are left out of the options.',
         topic='eng-2-15',
         lifted=[[S(20, 140, 545, 525, 564), S(20, 140, 586, 460, 661),
                  S(20, 140, 683, 525, 771), S(21, 140, 83, 525, 130),
                  S(21, 140, 152, 525, 185)]],
         row_kind='anyN', group=(3, 6), marks=[18], tariff='fixed', total=18,
         figure='engineering-2012-HL-scheme-q8b-sol',
         notes="The scheme prints '(Any three) 6 + 6 + 6'."),
    dict(key=(8, 'c', None),
         why='Paper p11 sets two alternative (c)s either side of an OR. This card is the '
             'first, the vehicle photographed beside it: scheme p21 answers in two '
             'paragraphs either side of a labelled drawing, shown with the answer; "16".',
         topic='eng-2-15', stem=False,
         question_lift=P(11, 125, 493, 360, 557),
         lifted=[join(S(21, 104, 234, 525, 268), S(21, 104, 538, 525, 585))],
         marks=[16], total=16,
         question_figure='engineering-2012-HL-paper-q8c-crop',
         figure='engineering-2012-HL-scheme-q8c-sol',
         notes="The scheme prints '16' and 'Suggested solution is based on the principle of "
               "the use of a separate drive to each wheel, other viable solutions are "
               "acceptable.' " + _OR8),
    dict(key=(8, 'c', 'i'),
         why='The OR branch\'s (i): scheme p21 names the material, "6".',
         topic='eng-2-16', stem=False,
         question_lift=P(11, *_C8B, more=[(165, 681, 395, 714)]),
         lifted=[S(21, 140, 634, 300, 654)], marks=[6], total=6,
         question_figure='engineering-2012-HL-paper-q8ci-art',
         notes="The scheme prints '6'. " + _OR8),
    dict(key=(8, 'c', 'ii'),
         replaces=NEW + 'carried the OR branch\'s answer without its stem',
         why='The OR branch\'s (ii): scheme p21 gives three advantages, one a line, "5 + 5".',
         topic='eng-2-16', stem=False,
         question_lift=P(11, *_C8B, more=[(165, 721, 435, 754)]),
         lifted=[S(21, 140, 679, 525, 693), S(21, 140, 693, 525, 707), S(21, 140, 707, 525, 722)],
         tariff='orderedSplit', notation='5 + 5', ladder=10, total=10,
         question_figure='engineering-2012-HL-paper-q8ci-art',
         notes="The scheme prints '5 + 5'. " + _OR8),
]

TOPICS = {
    'eng-2012-hl-q2-b-ii': ('eng-3-8', 'the elastic and plastic states in a tensile test; "mild '
                                       'steel" filed it under iron and steel'),
    'eng-2012-hl-q3-b-ii': ('eng-2-6', 'an application of flame hardening, a heat treatment; '
                                       '"lathe slideways" filed it under machining'),
    'eng-2012-hl-q6-a-i': ('eng-1-9', 'compression moulding, a plastics process; "principle '
                                      'of operation" filed it under testing'),
}

_COMP = ('Computer technology in industrial engineering (the OR branch of Q7(c)), which the '
         'reference files Q7 under; ')

ATLAS = {
    'eng-2012-hl-q1-a': dict(
        topics=['Welding'],
        note='The hurling helmet\'s face guard, its bars bent and welded; the card\'s syllabus '
             'heading is Manufacturing processes.'),
    'eng-2012-hl-q7-c-i': dict(
        topics=['Machining & Metrology'],
        note=_COMP + 'the card\'s syllabus heading is Technology.'),
    'eng-2012-hl-q7-c-ii': dict(
        topics=['Machining & Metrology'],
        note=_COMP + 'the card\'s syllabus heading is Technology.'),
    'eng-2012-hl-q7-c-iii': dict(
        topics=['Machining & Metrology'],
        note=_COMP + 'the card\'s syllabus heading is Manufacturing processes.'),
}
