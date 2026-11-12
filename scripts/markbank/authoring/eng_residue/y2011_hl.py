"""2011 Higher Level: the parts eng_all refuses or gets wrong, from the page.

Paper and scheme as the PDFs number their pages (the scheme's printed "Page 1"
is its pdf page 3). The marks grid is on scheme p4: Question 1 is Section A,
"Any ten @ 5 marks each", and Section B, "Answer all of the following", (n) to
(r); Questions 2-8 are 50 marks each. The scheme prints a part's marks under
its answer ("(Any two) 3 + 2", "(Any three) 6 + 6 + 6"). This sitting had no
cards before the lane: every card here is new, and a `replaces=` names the
automatic card it rebuilds before it ever shipped.
"""
from eng_lift import cells, join, lift

Y, L = 2011, 'hl'
NEW = 'never shipped: the automatic card '


def S(page, *rect):
    return lift(Y, L, 'scheme', page, rect)


def P(page, *rect, more=(), items=()):
    return lift(Y, L, 'paper', page, rect, more=more, items=items)


def _ck(page, part, lead):
    return (f'Paper p{page} prints {part} as one item of the list under "{lead}"; the '
            'semicolon ends the item, not the question.')


# Paper stems the parts are lifted with.
_N1 = (150, 117, 380, 229)            # p4: Q1(n), the Spittelau plant
_N1E = (150, 286, 400, 303)           # p4: "Briefly describe each of these pollution concerns."
_O1 = (150, 325, 515, 358)            # p4: Q1(o), dioxins
_B2 = (150, 408, 515, 441)            # p5: Q2(b), the tensile results
_B2U = (150, 545, 515, 562)           # p5: "Using the graph paper supplied, plot ..."
_B3 = (150, 236, 495, 253)            # p6: Q3(b), the iron-carbon diagram
_C3 = (150, 578, 520, 596)            # p6: Q3(c), the pyrometer readings
_B4 = (150, 294, 500, 347)            # p7: Q4(b), the table
_B4U = (150, 473, 315, 490)           # p7: "Using the graph paper supplied:"
_A5 = (150, 95, 420, 129)             # p8: Q5(a), MMA
_B6 = (150, 229, 490, 263)            # p9: Q6(b), the extruder
_B7 = (150, 296, 365, 361)            # p10: Q7(b), the cutting-tool inserts
_C8B = (150, 632, 515, 650)           # p11: the relay (c)

_SA = "Section A is 'Any ten @ 5 marks each'."
_SB = 'Section B is "Answer all of the following".'
_OR5 = ('The paper sets two (c)s either side of an OR: seam resistance or submerged arc '
        'welding, "(Any one) 16", carded at the letter, and the robotics (c), whose (i) and '
        '(ii) are carded apart.')
_OR7 = ('The paper sets two (c)s either side of an OR: the two milling cutters, "8 + 8" and '
        'both asked, carded at the letter, and the CNC safety (c), whose (i) and (ii) are '
        'carded apart.')
_OR8 = ('The paper sets two (c)s either side of an OR: the go-kart\'s steering, "16", carded '
        'at the letter, and the relay (c), whose (i) and (ii) are carded apart.')
_A3 = "The scheme prints '(Any two) 8 + 8': each part answered earns 8."
_A5B = "The scheme prints '(Any three) 6 + 6 + 6': each part answered earns 6."
_A7 = "The scheme prints '(Any three) 6 + 6 + 6': each part answered earns 6."
_ANY = 'Answer any three of the following:'

CROPS = {
    # ---- paper ------------------------------------------------------------
    'engineering-2011-HL-paper-q1a-crop': dict(
        doc='paper', page=3, rect=(439, 136, 539, 245), image=True, ref='2011 HL Q1(a)'),
    'engineering-2011-HL-paper-q1g-crop': dict(
        doc='paper', page=3, rect=(465, 317, 550, 430), image=True, ref='2011 HL Q1(g)'),
    # The two pneumatic components with their captions.
    'engineering-2011-HL-paper-q1k-crop': dict(
        doc='paper', page=3, rect=(195, 577, 425, 662), ref='2011 HL Q1(k)'),
    # The two threads with their captions, without the page footer.
    'engineering-2011-HL-paper-q1m-crop': dict(
        doc='paper', page=3, rect=(190, 732, 465, 789), ref='2011 HL Q1(m)'),
    'engineering-2011-HL-paper-q2a-crop': dict(
        doc='paper', page=5, rect=(155, 216, 450, 364), ref='2011 HL Q2(a)',
        letters=('A', 'B')),
    'engineering-2011-HL-paper-q2b-crop': dict(
        doc='paper', page=5, rect=(118, 460, 520, 520), ref='2011 HL Q2(b)'),
    'engineering-2011-HL-paper-q3b-crop': dict(
        doc='paper', page=6, rect=(145, 251.5, 490, 486), ref='2011 HL Q3(b)'),
    'engineering-2011-HL-paper-q3c-crop': dict(
        doc='paper', page=6, rect=(165, 595, 494, 699), ref='2011 HL Q3(c)',
        letters=('A', 'B', 'C')),
    # The two unit cells; the end of (iv)'s second line, which runs under the
    # first cell, is whited out.
    'engineering-2011-HL-paper-q4a-crop': dict(
        doc='paper', page=7, rect=(388, 156, 543, 236), mask=[(386, 221, 425, 237)],
        ref='2011 HL Q4(a)'),
    'engineering-2011-HL-paper-q4b-crop': dict(
        doc='paper', page=7, rect=(48, 370, 535, 450), ref='2011 HL Q4(b)'),
    'engineering-2011-HL-paper-q4c-crop': dict(
        doc='paper', page=7, rect=(185, 650, 468, 762), mask=[(184, 649, 300, 655)], ref='2011 HL Q4(c)',
        letters=('X', 'Y')),
    # The arc pictured with its label.
    'engineering-2011-HL-paper-q5ai-crop': dict(
        doc='paper', page=8, rect=(398, 95, 558, 176), ref='2011 HL Q5(a)(i)'),
    # The welding circuit with A, B and C.
    'engineering-2011-HL-paper-q5aii-crop': dict(
        doc='paper', page=8, rect=(170, 240, 545, 330), ref='2011 HL Q5(a)(ii)',
        letters=('A', 'B', 'C')),
    'engineering-2011-HL-paper-q5cor-crop': dict(
        doc='paper', page=8, rect=(436, 669, 560, 788), image=True, ref='2011 HL Q5(c)'),
    'engineering-2011-HL-paper-q7b-crop': dict(
        doc='paper', page=10, rect=(372, 251, 550, 366), image=True, ref='2011 HL Q7(b)'),
    # The two milling cutters with their captions.
    'engineering-2011-HL-paper-q7c-crop': dict(
        doc='paper', page=10, rect=(236, 519, 424, 666), ref='2011 HL Q7(c)'),
    # The two mechanisms with their captions (i) and (ii).
    'engineering-2011-HL-paper-q8a-crop': dict(
        doc='paper', page=11, rect=(158, 119, 477, 287), ref='2011 HL Q8(a)'),
    'engineering-2011-HL-paper-q8c-crop': dict(
        doc='paper', page=11, rect=(352, 461, 560, 569), image=True, ref='2011 HL Q8(c)'),
    'engineering-2011-HL-paper-q8cor-crop': dict(
        doc='paper', page=11, rect=(402, 655, 535, 775), image=True, ref='2011 HL Q8(c)'),
    # ---- scheme: the drawings, tables and workings the answers are given with
    'engineering-2011-HL-scheme-q1i-sol': dict(
        doc='scheme', page=6, rect=(175, 150, 400, 248), solution=True, ref='2011 HL Q1(i)'),
    'engineering-2011-HL-scheme-q1r-sol': dict(
        doc='scheme', page=9, rect=(165, 410, 496, 552), solution=True, ref='2011 HL Q1(r)'),
    'engineering-2011-HL-scheme-q2aii-sol': dict(
        doc='scheme', page=10, rect=(60, 250, 535, 420), solution=True, ref='2011 HL Q2(a)(ii)'),
    'engineering-2011-HL-scheme-q2b-sol': dict(
        doc='scheme', page=10, rect=(40, 485, 470, 740), solution=True, ref='2011 HL Q2(b)'),
    # Young's modulus worked as a stacked fraction the text layer flattens.
    'engineering-2011-HL-scheme-q2bi-sol': dict(
        doc='scheme', page=11, rect=(105, 83, 500, 128), solution=True, ref='2011 HL Q2(b)(i)'),
    'engineering-2011-HL-scheme-q2cii-sol': dict(
        doc='scheme', page=11, rect=(190, 400, 410, 546), solution=True, ref='2011 HL Q2(c)(ii)'),
    'engineering-2011-HL-scheme-q3ai-sol': dict(
        doc='scheme', page=12, rect=(215, 134, 510, 260), solution=True, ref='2011 HL Q3(a)(i)'),
    'engineering-2011-HL-scheme-q3cii-sol': dict(
        doc='scheme', page=13, rect=(135, 266, 460, 374), solution=True, ref='2011 HL Q3(c)(ii)'),
    'engineering-2011-HL-scheme-q4a-sol': dict(
        doc='scheme', page=14, rect=(430, 78, 526, 175), solution=True, ref='2011 HL Q4(a)'),
    'engineering-2011-HL-scheme-q4bi-sol': dict(
        doc='scheme', page=14, rect=(38, 459, 510, 736), solution=True, ref='2011 HL Q4(b)'),
    # The phase ratio worked as stacked fractions the text layer flattens.
    'engineering-2011-HL-scheme-q4biii-sol': dict(
        doc='scheme', page=15, rect=(100, 120, 500, 182), solution=True, ref='2011 HL Q4(b)(iii)'),
    'engineering-2011-HL-scheme-q4c-sol': dict(
        doc='scheme', page=15, rect=(96, 290, 520, 363), solution=True, ref='2011 HL Q4(c)'),
    'engineering-2011-HL-scheme-q5ai-sol': dict(
        doc='scheme', page=15, rect=(160, 498, 480, 582), solution=True, ref='2011 HL Q5(a)(i)'),
    'engineering-2011-HL-scheme-q5c-sol': dict(
        doc='scheme', parts=[(17, (418, 110, 556, 250)), (17, (222, 336, 415, 556))],
        layout='row', solution=True, ref='2011 HL Q5(c)'),
    # The robot inside its work envelope; the end of the answer's line that runs
    # under the drawing is whited out.
    'engineering-2011-HL-scheme-q5cor-sol': dict(
        doc='scheme', page=18, rect=(390, 150, 590, 290), mask=[(389, 279.5, 490, 292)],
        solution=True, ref='2011 HL Q5(c)(i)'),
    'engineering-2011-HL-scheme-q6ai-sol': dict(
        doc='scheme', page=18, rect=(70, 518, 542, 700), solution=True, ref='2011 HL Q6(a)(i)'),
    'engineering-2011-HL-scheme-q7c-sol': dict(
        doc='scheme', page=20, rect=(398, 578, 565, 734), solution=True, ref='2011 HL Q7(c)'),
    'engineering-2011-HL-scheme-q8c-sol': dict(
        doc='scheme', page=22, rect=(90, 270, 522, 415), solution=True, ref='2011 HL Q8(c)'),
    'engineering-2011-HL-scheme-q8cii-sol': dict(
        doc='scheme', page=22, rect=(352, 586, 552, 712), solution=True, ref='2011 HL Q8(c)(ii)'),
}

SPLIT = {
    'eng-2011-hl-q7-a': 'never shipped: "Answer any three of the following" over five '
                        'separate questions, each priced at 6; the automatic card ran all '
                        'five answers into one ordered split at the letter, one row the '
                        'scheme\'s "(Any three) 6 + 6 + 6"',
}

FOLDED = {
    'eng-2011-hl-q4-a-iv': 'never shipped: (iv) is one option of "Explain any two of the '
                           'following", carried by the Q4(a) card',
    'eng-2011-hl-q8-b-v': 'never shipped: (v) is one option of "Explain any three of the '
                          'following", carried by the Q8(b) card',
}

CARDS = [
    # ---- Question 1, Section A ("Any ten @ 5 marks each") ------------------
    dict(key=(1, 'a', None),
         why='The separator is pictured beside (a); scheme p5 describes magnetic separation '
             'in one paragraph under its heading, "5".',
         topic='eng-1-2',
         lifted=[S(5, 104, 192, 512, 263)], marks=[5], total=5,
         question_figure='engineering-2011-HL-paper-q1a-crop',
         notes="The scheme prints '5'. " + _SA),
    dict(key=(1, 'b', None),
         why='Scheme p5 explains the term in one paragraph under its heading, "5".',
         topic='eng-1-9',
         lifted=[S(5, 104, 289, 525, 360)], marks=[5], total=5,
         notes="The scheme prints '5'. " + _SA),
    dict(key=(1, 'c', None),
         why='Scheme p5 bullets five barrier methods, "(Any three) 2 + 2 +1".',
         topic='eng-3-7',
         lifted=[S(5, 120, 401, 520, 416), S(5, 120, 416, 520, 430.5),
                 S(5, 120, 430.5, 520, 445.5), S(5, 120, 445.5, 520, 460),
                 S(5, 120, 460, 520, 475)],
         tariff='orderedSplit', notation='2 + 2 + 1', ladder=5, total=5,
         notes="The scheme prints '(Any three) 2 + 2 +1'. " + _SA),
    dict(key=(1, 'd', None),
         why='Scheme p5 bullets four factors, "(Any three) 2 + 2 +1".',
         topic='eng-3-1',
         lifted=[S(5, 120, 516, 520, 531), S(5, 120, 531, 520, 545.5),
                 S(5, 120, 545.5, 520, 560), S(5, 120, 560, 520, 575)],
         tariff='orderedSplit', notation='2 + 2 + 1', ladder=5, total=5,
         notes="The scheme prints '(Any three) 2 + 2 +1'. " + _SA),
    dict(key=(1, 'e', None),
         why='Scheme p5 lists the properties in one sentence over two lines, each lifted by '
             'its own word rectangle; "(Any two) 3 + 2".',
         topic='eng-1-9',
         lifted=[S(5, 104, 601, 305.5, 615.5), S(5, 305.5, 601, 442.5, 615.5),
                 join(S(5, 442.5, 601, 525, 615.5), S(5, 104, 615.5, 153.5, 631)),
                 S(5, 153.5, 615.5, 330, 631)],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         notes="The scheme prints '(Any two) 3 + 2'. " + _SA),
    dict(key=(1, 'f', None),
         why='Scheme p5 gives each kind of conductor a line, "3 + 2".',
         topic='eng-1-2',
         lifted=[S(5, 104, 655, 525, 670.3), S(5, 104, 670.3, 525, 684.5)],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         notes="The scheme prints '3 + 2'. " + _SA),
    dict(key=(1, 'g', None),
         why='The table is photographed beside (g); scheme p5 lists the reasons in one '
             'sentence over two lines, each lifted by its own word rectangle; "(Any two) '
             '3 + 2". The scheme\'s "is has" is lifted as printed.',
         topic='eng-1-4',
         lifted=[S(5, 104, 712, 355.5, 726.5),
                 join(S(5, 355.5, 712, 525, 726.5), S(5, 104, 726.5, 229.5, 741)),
                 S(5, 229.5, 726.5, 304.5, 741), S(5, 304.5, 726.5, 440, 741)],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         question_figure='engineering-2011-HL-paper-q1g-crop',
         notes="The scheme prints '(Any two) 3 + 2'. " + _SA),
    dict(key=(1, 'h', None),
         why='Scheme p6 expands each abbreviation after its roman; "(Any two) 3 + 2".',
         topic='eng-3-14',
         lifted=[S(6, 104, 71, 400, 86), S(6, 104, 86, 400, 99.5), S(6, 104, 99.5, 400, 113.5),
                 S(6, 104, 113.5, 400, 128)],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         notes="The scheme prints '(Any two) 3 + 2'. " + _SA),
    dict(key=(1, 'i', None),
         why='Scheme p6 draws both fits, shown with the answer, and describes each in turn, '
             '"3 + 2".',
         topic='eng-3-12',
         lifted=[S(6, 104, 253, 525, 283.5), S(6, 104, 283.5, 525, 311)],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         figure='engineering-2011-HL-scheme-q1i-sol',
         notes="The scheme prints '3 + 2'. " + _SA),
    dict(key=(1, 'j', None),
         why='A lead-in over three people set as romans, "any one"; scheme p6 writes a note '
             'on each after the name, "(Any one) 5". The reader drops the people\'s line, so '
             'the question is lifted from the page.',
         topic='eng-3-14',
         question_lift=P(3, 150, 516, 515, 549),
         lifted=[[S(6, 104, 332, 525, 418), S(6, 104, 424, 525, 496), S(6, 104, 502, 525, 560)]],
         row_kind='anyN', group=(1, 5), marks=[5], tariff='fixed', total=5,
         notes="The scheme prints '(Any one) 5'. " + _SA),
    dict(key=(1, 'k', None),
         why='The two components are pictured and captioned (i) and (ii); scheme p6 names '
             'each after its roman, "(Any one) 5".',
         topic='eng-2-15',
         lifted=[[S(6, 104, 585, 400, 600.5), S(6, 104, 600.5, 400, 614)]],
         row_kind='anyN', group=(1, 5), marks=[5], tariff='fixed', total=5,
         question_figure='engineering-2011-HL-paper-q1k-crop',
         notes="The scheme prints '(Any one) 5'. " + _SA),
    dict(key=(1, 'l', None),
         why='Scheme p6 answers in one sentence, "5".',
         topic='eng-2-10',
         lifted=[S(6, 104, 640, 525, 669.5)], marks=[5], total=5,
         notes="The scheme prints '5'. " + _SA),
    dict(key=(1, 'm', None),
         why='The two threads are drawn and captioned (i) and (ii); scheme p6 compares them '
             'in one paragraph, "5".',
         topic='eng-2-13',
         lifted=[S(6, 104, 695, 525, 752.5)], marks=[5], total=5,
         question_figure='engineering-2011-HL-paper-q1m-crop',
         notes="The scheme prints '5'. " + _SA),
    # ---- Question 1, Section B ("Answer all of the following") -------------
    dict(key=(1, 'n', 'i'),
         why='Scheme p7 describes the concern in one paragraph under its heading; "4 + 3 + '
             '3", 4 for (i).',
         topic='eng-3-14', stem=False,
         question_lift=P(4, *_N1, more=[(172, 233, 330, 250), _N1E]),
         lifted=[S(7, 140, 126, 525, 198)], marks=[4], total=4,
         question_figure='engineering-2011-HL-paper-q1ni-art',
         notes="The scheme prints '4 + 3 + 3', for (i), (ii) and (iii) in that order. " + _SB),
    dict(key=(1, 'n', 'ii'),
         why='Scheme p7 describes the concern in one paragraph under its heading; "4 + 3 + '
             '3", 3 for (ii).',
         topic='eng-3-14', stem=False,
         question_lift=P(4, *_N1, more=[(172, 249, 330, 266), _N1E]),
         lifted=[S(7, 140, 222, 525, 295)], marks=[3], total=3,
         question_figure='engineering-2011-HL-paper-q1ni-art',
         notes="The scheme prints '4 + 3 + 3', for (i), (ii) and (iii) in that order. " + _SB),
    dict(key=(1, 'n', 'iii'),
         why='Scheme p7 describes the concern in three paragraphs under its heading; "4 + 3 '
             '+ 3", 3 for (iii).',
         topic='eng-3-14', stem=False,
         question_lift=P(4, *_N1, more=[(172, 265, 330, 282), _N1E]),
         lifted=[S(7, 140, 319, 525, 445)], marks=[3], total=3,
         question_figure='engineering-2011-HL-paper-q1ni-art',
         notes="The scheme prints '4 + 3 + 3', for (i), (ii) and (iii) in that order. " + _SB),
    dict(key=(1, 'o', 'i'),
         why='Scheme p7 bullets five effects under its heading, "3 + 3".',
         topic='eng-3-14', stem=False,
         question_lift=P(4, *_O1, more=[(172, 357, 510, 389)]),
         lifted=[S(7, 155, 499, 525, 543), S(7, 155, 543, 525, 571), S(7, 155, 571, 525, 600),
                 S(7, 155, 600, 525, 614), S(7, 155, 614, 525, 643)],
         tariff='orderedSplit', notation='3 + 3', ladder=6, total=6,
         notes="The scheme prints '3 + 3'. " + _SB),
    dict(key=(1, 'o', 'ii'),
         why='Scheme p7 explains in one paragraph under its heading, "4".',
         topic='eng-3-14', stem=False,
         question_lift=P(4, *_O1, more=[(172, 388, 455, 405)]),
         lifted=[S(7, 140, 668, 525, 726)], marks=[4], total=4,
         notes="The scheme prints '4'. " + _SB),
    dict(key=(1, 'p', None),
         why='The four elements are bulleted on the paper; scheme p8 describes each under its '
             'name, "4 + 3 + 3" for the three described. The question is lifted with its '
             'list on its lines, as printed.',
         topic='eng-3-14', stem=False,
         question_lift=P(4, 150, 429, 500, 478, items=[(180, 478, 300, 495),
                                                       (180, 494, 300, 511),
                                                       (180, 511, 300, 528),
                                                       (180, 528, 300, 545)]),
         lifted=[S(8, 104, 70, 525, 115), S(8, 104, 126, 525, 170), S(8, 104, 181, 525, 226),
                 S(8, 104, 236, 525, 294)],
         tariff='orderedSplit', notation='4 + 3 + 3', ladder=10, total=10,
         notes="The scheme prints '4 + 3 + 3'. " + _SB),
    dict(key=(1, 'q', None),
         why='The incinerator is drawn beside (q) with A-D; scheme p8 describes its operation '
             'in one paragraph under its heading, "10". The drawing\'s letters are left out '
             'of the words.',
         topic='eng-3-14', stem=False,
         question_lift=P(4, 150, 575, 360, 656),
         lifted=[join(S(8, 104, 331, 300, 350), S(8, 104, 356, 395, 483))], marks=[10],
         total=10,
         question_figure='engineering-2011-HL-paper-q1q-art',
         notes="The scheme prints '10'. " + _SB),
    dict(key=(1, 'r', None),
         why='A lead-in over three topics set as romans, "any two"; scheme pp8-9 answer each '
             'under its roman, the rotary kiln beside a lettered drawing, shown with the '
             'answer; "(Any two) 5 + 5". The drawing\'s letters are left out of the words.',
         topic='eng-3-14',
         lifted=[[S(8, 140, 552, 525, 681), S(9, 140, 69, 525, 258),
                  join(S(9, 140, 322, 525, 409), S(9, 140, 558, 525, 575))]],
         row_kind='anyN', group=(2, 5), marks=[10], tariff='fixed', total=10,
         figure='engineering-2011-HL-scheme-q1r-sol',
         notes="The scheme prints '(Any two) 5 + 5'. " + _SB),
    # ---- Question 2 --------------------------------------------------------
    dict(key=(2, 'a', 'ii'),
         why='The two tests are drawn as diagrams A and B; scheme p10 compares them in a '
             'table under the three headings the question gives, shown with the answer, '
             '"10" for the part. Each row is the table\'s row: its heading, then test A\'s '
             'cell, then test B\'s, joined.',
         topic='eng-3-8',
         lifted=[cells(S(10, 68, 289, 200, 305), S(10, 202, 289, 355, 318),
                       S(10, 358, 289, 520, 331.5)),
                 cells(S(10, 68, 331.5, 200, 346), S(10, 202, 331.5, 355, 374),
                       S(10, 358, 331.5, 520, 374)),
                 cells(S(10, 68, 374, 200, 388), S(10, 202, 374, 355, 416),
                       S(10, 358, 374, 520, 416))],
         tariff='questionTotal', total=10,
         question_figure='engineering-2011-HL-paper-q2a-crop',
         figure='engineering-2011-HL-scheme-q2aii-sol',
         notes="The scheme prints '10'. Its table is headed 'Hardness test A' and 'Hardness "
               "test B'; each row gives the heading, then A's cell, then B's."),
    dict(key=(2, 'b', None),
         why='"Plot the stress-strain graph": scheme p10 answers with the plotted graph, '
             'shown with the answer, "Plot graph 10" (the grid). The plot is asked at the '
             'letter, so the card is the letter\'s.',
         topic='eng-3-8', stem=False,
         question_lift=P(5, *_B2, more=[_B2U]),
         special={'kind': 'ask'}, total=10,
         question_figure='engineering-2011-HL-paper-q2b-crop',
         figure='engineering-2011-HL-scheme-q2b-sol',
         notes="The scheme prints 'Plot the graph:' and '10'."),
    dict(key=(2, 'b', 'i'),
         why='Scheme p11 works the modulus as a stacked fraction the text layer flattens; the '
             'working is shown as printed, "4".',
         topic='eng-3-8', stem=False,
         question_lift=P(5, *_B2, more=[_B2U, (180, 568, 400, 585)]),
         special={'kind': 'ask'}, total=4,
         question_figure='engineering-2011-HL-paper-q2b-crop',
         figure='engineering-2011-HL-scheme-q2bi-sol',
         notes="The scheme prints '4'."),
    dict(key=(2, 'b', 'ii'),
         why='Scheme p11 reads the proof stress off the graph in one line, "2"; the graph it '
             'is read from is shown with the answer.',
         topic='eng-3-8', stem=False,
         question_lift=P(5, *_B2, more=[_B2U, (180, 589, 300, 606)]),
         lifted=[S(11, 140, 165, 525, 184)], marks=[2], total=2,
         question_figure='engineering-2011-HL-paper-q2b-crop',
         figure='engineering-2011-HL-scheme-q2b-sol',
         notes="The scheme prints '2'."),
    dict(key=(2, 'c', 'ii'),
         replaces=NEW + 'gave the test without the drawing the part asks for',
         why='Scheme p9 describes ultrasonic testing under a labelled drawing, shown with the '
             'answer, "8".',
         topic='eng-3-8',
         lifted=[S(11, 140, 570, 525, 642)], marks=[8], total=8,
         figure='engineering-2011-HL-scheme-q2cii-sol',
         notes="The scheme prints '8'."),
    # ---- Question 3 --------------------------------------------------------
    dict(key=(3, 'a', 'i'),
         checked=_ck(6, '(a)(i)', 'Answer any two of the following:'),
         why='One of "Answer any two of the following": scheme p12 describes the process '
             'under a labelled drawing, shown with the answer.',
         topic='eng-2-6',
         lifted=[S(12, 140, 277, 525, 364)], marks=[8], total=8,
         figure='engineering-2011-HL-scheme-q3ai-sol', notes=_A3),
    dict(key=(3, 'a', 'ii'),
         checked=_ck(6, '(a)(ii)', 'Answer any two of the following:'),
         why='One of "Answer any two of the following": scheme p12 describes each iron under '
             'its heading, the 8 for the part not split between them.',
         topic='eng-1-4',
         lifted=[S(12, 140, 388, 525, 459), S(12, 140, 459, 525, 502)],
         tariff='questionTotal', total=8, notes=_A3),
    dict(key=(3, 'a', 'iii'),
         replaces=NEW + 'read the scheme\'s "(Any two) 8 + 8" as a third point',
         why='One of "Answer any two of the following": scheme p12 answers in one paragraph '
             'under its heading.',
         topic='eng-2-6',
         lifted=[S(12, 140, 539, 525, 598)], marks=[8], total=8, notes=_A3),
    dict(key=(3, 'b', 'i'),
         why='The diagram is drawn with regions 1-5; scheme p12 names each after its number, '
             '"2 + 2 + 2 + 2 + 2".',
         topic='eng-1-3', stem=False,
         question_lift=P(6, *_B3, more=[(176, 494, 425, 511)]),
         lifted=[S(12, 140, 651, 300, 665.5), S(12, 140, 665.5, 300, 679.5),
                 S(12, 140, 679.5, 300, 693.5), S(12, 140, 693.5, 300, 707),
                 S(12, 140, 707, 300, 721)],
         marks=[2, 2, 2, 2, 2], total=10,
         question_figure='engineering-2011-HL-paper-q3b-crop',
         notes="The scheme prints '2 + 2 + 2 + 2 + 2'."),
    dict(key=(3, 'c', 'i'),
         replaces=NEW + 'asked about "this pyrometer" without the readings that show it',
         why='The pyrometer\'s readings are drawn at A, B and C; scheme p13 names it and '
             'states its function under their headings, "3 +3".',
         topic='eng-2-6', stem=False,
         question_lift=P(6, *_C3, more=[(172, 703, 390, 720)]),
         lifted=[S(13, 140, 195, 525, 211), S(13, 140, 211, 525, 225)],
         marks=[3, 3], total=6,
         question_figure='engineering-2011-HL-paper-q3c-crop',
         notes="The scheme prints '3 +3', for the name and the function in that order."),
    dict(key=(3, 'c', 'ii'),
         replaces=NEW + 'opened with the diagrams\' letters "A B C"',
         why='Scheme p13 explains the pyrometer under the three readings it draws, shown with '
             'the answer; "10".',
         topic='eng-2-6', stem=False,
         question_lift=P(6, *_C3, more=[(172, 735, 475, 769)]),
         lifted=[S(13, 140, 370, 525, 443)], marks=[10], total=10,
         question_figure='engineering-2011-HL-paper-q3c-crop',
         figure='engineering-2011-HL-scheme-q3cii-sol',
         notes="The scheme prints '10'."),
    # ---- Question 4 --------------------------------------------------------
    dict(key=(4, 'a', None),
         replaces=NEW + 'split the answers into six options, cutting allotropy off after its '
                        'second sentence and taking amorphous and crystalline, and bcc and '
                        'fcc, as options of their own',
         why='A lead-in over four topics set as romans, "any two"; scheme pp13-14 answer each '
             'under its roman, the interstitial solution beside a drawing, shown with the '
             'answer; one option each, "(Any two) 8 + 8".',
         topic='eng-1-3',
         lifted=[[S(13, 140, 576, 525, 705), S(14, 140, 83, 428, 170), S(14, 140, 181, 525, 267),
                  S(14, 140, 276, 525, 377)]],
         row_kind='anyN', group=(2, 8), marks=[16], tariff='fixed', total=16,
         question_figure='engineering-2011-HL-paper-q4a-crop',
         figure='engineering-2011-HL-scheme-q4a-sol',
         notes="The scheme prints '(Any two) 8 + 8'."),
    dict(key=(4, 'b', 'i'),
         why='"Draw the thermal equilibrium diagram": scheme p14 answers with the drawn '
             'diagram, shown with the answer, "10".',
         topic='eng-1-3', stem=False,
         question_lift=P(7, *_B4, more=[_B4U, (172, 494, 505, 511)]),
         special={'kind': 'ask'}, total=10,
         question_figure='engineering-2011-HL-paper-q4b-crop',
         figure='engineering-2011-HL-scheme-q4bi-sol',
         notes="The scheme prints '10'."),
    dict(key=(4, 'b', 'ii'),
         why='Scheme p15 lists the five features in one line, which the diagram drawn for (i) '
             'labels, shown with the answer; "5".',
         topic='eng-1-3', stem=False,
         question_lift=P(7, *_B4, more=[_B4U, (172, 515, 370, 532)]),
         lifted=[S(15, 140, 84, 500, 100)], marks=[5], total=5,
         question_figure='engineering-2011-HL-paper-q4b-crop',
         figure='engineering-2011-HL-scheme-q4bi-sol',
         notes="The scheme prints '5'."),
    dict(key=(4, 'b', 'iii'),
         why='Scheme p15 works the ratio as stacked fractions the text layer flattens; the '
             'working is shown as printed, "3".',
         topic='eng-1-3', stem=False,
         question_lift=P(7, *_B4, more=[_B4U, (172, 535, 485, 570)]),
         special={'kind': 'ask'}, total=3,
         question_figure='engineering-2011-HL-paper-q4b-crop',
         figure='engineering-2011-HL-scheme-q4biii-sol',
         notes="The scheme prints '3'."),
    dict(key=(4, 'c', None),
         why='The cooling from X to Y is drawn under (c); scheme p15 describes the stages in '
             'one paragraph over drawings of them, shown with the answer; "16".',
         topic='eng-1-3',
         lifted=[S(15, 104, 232, 525, 290)], marks=[16], total=16,
         question_figure='engineering-2011-HL-paper-q4c-crop',
         figure='engineering-2011-HL-scheme-q4c-sol',
         notes="The scheme prints '16'."),
    # ---- Question 5 --------------------------------------------------------
    dict(key=(5, 'a', 'i'),
         why='The arc is pictured beside (a); scheme p15 describes the process under a '
             'labelled drawing, shown with the answer; "10".',
         topic='eng-2-10', stem=False,
         question_lift=P(8, *_A5, more=[(176, 140, 370, 173)]),
         lifted=[S(15, 140, 591, 512, 760)], marks=[10], total=10,
         question_figure='engineering-2011-HL-paper-q5ai-crop',
         figure='engineering-2011-HL-scheme-q5ai-sol',
         notes="The scheme prints '10'."),
    dict(key=(5, 'a', 'ii'),
         why='The circuit is drawn with A, B and C; scheme p16 names each part after its '
             'letter and states its function, "2 + 2 + 2".',
         topic='eng-2-10', stem=False,
         question_lift=P(8, *_A5, more=[(176, 183, 485, 217)]),
         lifted=[S(16, 140, 110, 525, 198), S(16, 140, 207, 525, 267), S(16, 140, 276, 525, 308)],
         marks=[2, 2, 2], total=6,
         labels={'A': S(16, 163, 110, 300, 128), 'B': S(16, 162, 207, 300, 225),
                 'C': S(16, 163, 276, 300, 294)},
         question_figure='engineering-2011-HL-paper-q5aii-crop',
         notes="The scheme prints '2 + 2 + 2', for A, B and C in that order."),
    dict(key=(5, 'b', 'i'),
         checked=_ck(8, '(b)(i)', _ANY),
         why='One of "Answer any three of the following": scheme p16 bullets five features, '
             'the 6 for the part not split between them.',
         topic='eng-3-1',
         lifted=[S(16, 155, 376, 525, 390.5), S(16, 155, 390.5, 525, 405),
                 S(16, 155, 405, 525, 420), S(16, 155, 420, 525, 434.5),
                 S(16, 155, 434.5, 525, 450)],
         tariff='questionTotal', total=6, notes=_A5B),
    dict(key=(5, 'b', 'ii'),
         checked=_ck(8, '(b)(ii)', _ANY),
         why='One of "Answer any three of the following": scheme p16 bullets four methods, '
             'the 6 for the part not split between them.',
         topic='eng-2-10',
         lifted=[S(16, 155, 476, 525, 519), S(16, 155, 519, 525, 534),
                 S(16, 155, 534, 525, 548.5), S(16, 155, 548.5, 525, 563)],
         tariff='questionTotal', total=6, notes=_A5B),
    dict(key=(5, 'b', 'iv'),
         replaces=NEW + 'read the scheme\'s "(Any three) 6 + 6 + 6" as a third point',
         why='One of "Answer any three of the following": scheme p16 answers in one paragraph '
             'under its heading.',
         topic='eng-2-10',
         lifted=[S(16, 140, 658, 525, 716)], marks=[6], total=6, notes=_A5B),
    dict(key=(5, 'c', None),
         why='Paper p8 sets two alternative (c)s either side of an OR. This card is the '
             'first: "the main features of one of the following", seam resistance or '
             'submerged arc welding; scheme p17 describes each beside a labelled drawing, '
             'shown with the answer, "(Any one) 16". The drawings\' labels are left out of '
             'the words.',
         topic='eng-2-10', stem=False,
         question_lift=P(8, 150, 548, 505, 581, items=[(150, 587, 310, 604),
                                                       (150, 608, 350, 625)]),
         lifted=[[S(17, 140, 112, 422, 253), S(17, 140, 573, 525, 701)]],
         row_kind='anyN', group=(1, 16), marks=[16], tariff='fixed', total=16,
         figure='engineering-2011-HL-scheme-q5c-sol',
         notes="The scheme prints '(Any one) 16'. " + _OR5),
    dict(key=(5, 'c', 'i'),
         replaces=NEW + 'ran the first branch\'s seam welding answer and this branch\'s '
                        'answer into one ordered split',
         why='The OR branch\'s (i), the robot pictured beside it: scheme p18 explains each '
             'term under its heading, the second beside a drawing of the work envelope, '
             'shown with the answer; "4 + 4". The drawing\'s label is left out of the words.',
         topic='eng-3-14', stem=False,
         question_lift=P(8, 175, 683, 380, 700, items=[(195, 700, 300, 717),
                                                       (195, 717, 300, 734)]),
         lifted=[S(18, 140, 152, 390, 198),
                 join(S(18, 140, 207, 390, 278.5), S(18, 140, 278.5, 490, 307))],
         marks=[4, 4], total=8,
         question_figure='engineering-2011-HL-paper-q5cor-crop',
         figure='engineering-2011-HL-scheme-q5cor-sol',
         notes="The scheme prints '4 + 4', for the work envelope and the degree of freedom "
               "in that order. " + _OR5),
    dict(key=(5, 'c', 'ii'),
         replaces=NEW + 'ran the first branch\'s SAW answer and this branch\'s answer into '
                        'one question total',
         why='The OR branch\'s (ii): scheme p18 answers in one sentence, "8".',
         topic='eng-3-14', stem=False,
         question_lift=P(8, 175, 742, 430, 775),
         lifted=[S(18, 125, 328, 525, 358)], marks=[8], total=8,
         question_figure='engineering-2011-HL-paper-q5cor-crop',
         notes="The scheme prints '8'. " + _OR5),
    # ---- Question 6 --------------------------------------------------------
    dict(key=(6, 'a', 'i'),
         why='Scheme pp18-19 describe the process in paragraphs either side of the labelled '
             'diagram, shown with the answer; "Description 5", "Diagram 5". The diagram has '
             'no words to claim, so the 10 is one total over the description, the diagram '
             'shown with it.',
         topic='eng-1-9',
         lifted=[join(S(18, 140, 480, 525, 511), S(18, 140, 717, 525, 760),
                      S(19, 140, 70, 525, 142))],
         tariff='questionTotal', total=10,
         figure='engineering-2011-HL-scheme-q6ai-sol',
         notes="The scheme prints 'Description 5' and 'Diagram 5'."),
    dict(key=(6, 'a', 'ii'),
         replaces=NEW + 'gave the answer to Q6(c)(ii), fillers, for this part',
         why='Scheme p19 names the polymer, "4".',
         topic='eng-1-9',
         lifted=[S(19, 125, 167, 300, 184)], marks=[4], total=4,
         notes="The scheme prints '4'."),
    dict(key=(6, 'b', 'i'),
         why='The extruder is drawn under (b); scheme p19 names the process and describes '
             'its operation under their headings, "Name 4", "Operation 8".',
         topic='eng-1-9', stem=False,
         question_lift=P(9, *_B6, more=[(185, 461, 470, 479)]),
         lifted=[S(19, 140, 222, 300, 239), S(19, 140, 236, 525, 307)],
         marks=[4, 8], total=12,
         question_figure='engineering-2011-HL-paper-q6bi-art',
         notes="The scheme prints 'Name 4' and 'Operation 8'."),
    dict(key=(6, 'b', 'ii'),
         why='Scheme p19 answers in one line, "2".',
         topic='eng-1-9', stem=False,
         question_lift=P(9, *_B6, more=[(185, 482, 415, 499)]),
         lifted=[S(19, 125, 346, 450, 364)], marks=[2], total=2,
         question_figure='engineering-2011-HL-paper-q6bi-art',
         notes="The scheme prints '2'."),
    dict(key=(6, 'c', None),
         why='A lead-in over five additives set as romans, "any three"; scheme p19 explains '
             'each under its name, one option each, "(Any three) 6 + 6 + 6". The scheme '
             'heads the part "(a)"; it is (c) on the paper.',
         topic='eng-1-9',
         lifted=[[S(19, 125, 443, 525, 488), S(19, 125, 498, 525, 557), S(19, 125, 567, 525, 612),
                  S(19, 125, 622, 525, 667), S(19, 125, 678, 525, 709)]],
         row_kind='anyN', group=(3, 6), marks=[18], tariff='fixed', total=18,
         notes="The scheme prints '(Any three) 6 + 6 + 6'."),
    # ---- Question 7 --------------------------------------------------------
    dict(key=(7, 'a', 'i'),
         checked=_ck(10, '(a)(i)', _ANY),
         why='One of "Answer any three of the following": scheme p20 bullets five '
             'precautions, the 6 for the part not split between them.',
         topic='eng-2-11',
         lifted=[S(20, 155, 114, 525, 128.5), S(20, 155, 128.5, 525, 143),
                 S(20, 155, 143, 525, 158), S(20, 155, 158, 525, 186),
                 S(20, 155, 186, 525, 201)],
         tariff='questionTotal', total=6, notes=_A7),
    dict(key=(7, 'a', 'ii'),
         checked=_ck(10, '(a)(ii)', _ANY),
         why='One of "Answer any three of the following": scheme p20 describes each kind of '
             'cutting in turn, the 6 for the part not split between them.',
         topic='eng-2-11',
         lifted=[S(20, 125, 213, 525, 242), S(20, 140, 242, 525, 285)],
         tariff='questionTotal', total=6, notes=_A7),
    dict(key=(7, 'a', 'iii'),
         checked=_ck(10, '(a)(iii)', _ANY),
         why='One of "Answer any three of the following": scheme p20 answers in one line.',
         topic='eng-3-12',
         lifted=[S(20, 125, 295, 525, 312)], marks=[6], total=6, notes=_A7),
    dict(key=(7, 'a', 'iv'),
         checked=_ck(10, '(a)(iv)', _ANY),
         why='One of "Answer any three of the following": scheme p20 answers in one '
             'paragraph under its heading.',
         topic='eng-2-11',
         lifted=[S(20, 125, 337, 525, 381)], marks=[6], total=6, notes=_A7),
    dict(key=(7, 'a', 'v'),
         why='One of "Answer any three of the following": scheme p20 answers in one line.',
         topic='eng-2-11',
         lifted=[S(20, 125, 392, 400, 409)], marks=[6], total=6, notes=_A7),
    dict(key=(7, 'c', None),
         why='Paper p10 sets two alternative (c)s either side of an OR. This card is the '
             'first, which asks for both cutters drawn: scheme p20 describes the slot drill '
             'and the dovetail cutter under their names, each beside a drawing, shown with '
             'the answer; "8 + 8". The drawings\' labels are left out of the words.',
         topic='eng-2-11', stem=False,
         question_lift=P(10, 150, 487, 485, 520),
         lifted=[S(20, 140, 598, 400, 657), S(20, 140, 667, 400, 712)],
         marks=[8, 8], total=16,
         question_figure='engineering-2011-HL-paper-q7c-crop',
         figure='engineering-2011-HL-scheme-q7c-sol',
         notes="The scheme prints '8 + 8', for (i) and (ii) in that order. " + _OR7),
    dict(key=(7, 'c', 'i'),
         replaces=NEW + 'read the scheme\'s "4 + 4 + 4" as a fifth point',
         why='The OR branch\'s (i): scheme p21 gives four features, one a line, "4 + 4 + 4".',
         topic='eng-2-11',
         lifted=[S(21, 140, 112, 525, 127.5), S(21, 140, 127.5, 525, 141),
                 S(21, 140, 141, 525, 154.5), S(21, 140, 154.5, 525, 183)],
         tariff='orderedSplit', notation='4 + 4 + 4', ladder=12, total=12,
         notes="The scheme prints '4 + 4 + 4'. " + _OR7),
    # ---- Question 8 --------------------------------------------------------
    dict(key=(8, 'a', None),
         why='"Any one of the mechanisms shown", photographed and captioned (i) and (ii); '
             'scheme p21 names each under its roman and describes its operation, "(Any one) '
             'Name 8, Operation 8". The name and the operation are each any one of the two.',
         topic='eng-2-15',
         lifted=[[S(21, 140, 346, 300, 363), S(21, 140, 402, 300, 419)],
                 [S(21, 140, 363, 525, 391), S(21, 140, 416, 525, 501)]],
         marks=[8, 8], total=16,
         question_figure='engineering-2011-HL-paper-q8a-crop',
         notes="The scheme prints '(Any one) Name 8, Operation 8', for the mechanism "
               "chosen."),
    dict(key=(8, 'b', None),
         replaces=NEW + 'split the vee-belt answer into four options and took "(Any three) '
                        '6 + 6 + 6" for an option',
         why='A lead-in over five topics set as romans, "any three"; scheme pp21-22 answer '
             'each under its heading, one option each, "(Any three) 6 + 6 + 6".',
         topic='eng-2-15',
         lifted=[[S(21, 140, 553, 525, 626), S(21, 140, 635, 525, 695), S(21, 140, 705, 525, 750),
                  S(22, 140, 69, 525, 115), S(22, 140, 126, 525, 157)]],
         row_kind='anyN', group=(3, 6), marks=[18], tariff='fixed', total=18,
         notes="The scheme prints '(Any three) 6 + 6 + 6'."),
    dict(key=(8, 'c', None),
         why='Paper p11 sets two alternative (c)s either side of an OR. This card is the '
             'first, the go-kart photographed beside it: scheme p22 answers in two '
             'paragraphs either side of labelled drawings, shown with the answer; "16".',
         topic='eng-2-15', stem=False,
         question_lift=P(11, 150, 486, 340, 535),
         lifted=[join(S(22, 104, 208, 525, 226), S(22, 104, 429, 525, 502))], marks=[16],
         total=16,
         question_figure='engineering-2011-HL-paper-q8c-crop',
         figure='engineering-2011-HL-scheme-q8c-sol',
         notes="The scheme prints '16' and '"
               + join(S(22, 104, 236, 525, 253), S(22, 104, 250, 300, 267)) + "' " + _OR8),
    dict(key=(8, 'c', 'i'),
         why='The OR branch\'s (i): scheme p22 names the component, "6".',
         topic='eng-2-16', stem=False,
         question_lift=P(11, *_C8B, more=[(180, 653, 340, 670)]),
         lifted=[S(22, 125, 553, 300, 570)], marks=[6], total=6,
         question_figure='engineering-2011-HL-paper-q8cor-crop',
         notes="The scheme prints '6'. " + _OR8),
    dict(key=(8, 'c', 'ii'),
         why='The OR branch\'s (ii): scheme p22 describes the relay\'s operation beside a '
             'labelled drawing, shown with the answer; "10". The drawing\'s labels are left '
             'out of the words.',
         topic='eng-2-16', stem=False,
         question_lift=P(11, *_C8B, more=[(180, 673, 390, 722)]),
         lifted=[join(S(22, 125, 593, 350, 709), S(22, 140, 719, 525, 750))], marks=[10],
         total=10,
         question_figure='engineering-2011-HL-paper-q8cor-crop',
         figure='engineering-2011-HL-scheme-q8cii-sol',
         notes="The scheme prints '10'. " + _OR8),
]

TOPICS = {
    'eng-2011-hl-q3-b-ii': ('eng-1-3', 'cooling 0.4% carbon steel quickly, read off the '
                                       'iron-carbon diagram of (b); "carbon steel" filed it '
                                       'under iron and steel'),
    'eng-2011-hl-q5-b-iii': ('eng-2-10', 'TIG welding of aluminium, a welding process; '
                                         '"aluminium" filed it under non-ferrous metals'),
}

_ROB = ('Robotic control (the OR branch of Q5(c)), which the reference files under Energy, '
        'Electronics & Robotics; the card\'s syllabus heading is Technology.')
_REL = ('The relay (the OR branch of Q8(c)), under the Mechanisms the reference files Q8 under; '
        'the card\'s syllabus heading is Electronics.')

ATLAS = {
    'eng-2011-hl-q1-m': dict(
        topics=['Machining & Metrology'],
        note='A machined thread against a rolled one; the card\'s syllabus heading is '
             'Manufacturing processes.'),
    'eng-2011-hl-q3-a-ii': dict(
        topics=['Heat Treatment'],
        note='Grey and white cast iron, set by their cooling, under Q3\'s Heat Treatment; the '
             'card\'s syllabus heading is Iron and steel.'),
    'eng-2011-hl-q5-c-i': dict(topics=['Energy, Electronics & Robotics'], note=_ROB),
    'eng-2011-hl-q5-c-ii': dict(topics=['Energy, Electronics & Robotics'], note=_ROB),
    'eng-2011-hl-q8-c-i': dict(topics=['Mechanisms'], note=_REL),
    'eng-2011-hl-q8-c-ii': dict(topics=['Mechanisms'], note=_REL),
}
