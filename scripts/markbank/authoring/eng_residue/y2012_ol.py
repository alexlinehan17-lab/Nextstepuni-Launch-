"""2012 Ordinary Level: every part, from the page.

Paper and scheme as the PDFs number their pages. As in 2013-2019, the automatic
author prices nothing in this sitting: the scheme sets each answer in a left
column and its award in a box to the right ("Name Award 3 @ 4 Marks"), which
its reader does not join to the answer, so every card here is built from the
page by rectangle. The marks grid is on scheme p4: Question 1 is Section A,
"Any six @ 5 marks each. Two part answers 3 + 2", and Section B, "Any three
parts @ 12 + 12 + 11 Marks", two-part answers "6 + 6 or 6 + 5"; Questions 2-7
are 45 marks each. A Section B card carries the PRINTED primary price, the 12
the scheme awards a part answered first or second ("Award 12 (11) Marks"), and
says the third part answered earns 11.
"""
from eng_lift import join, lift

Y, L = 2012, 'ol'


def S(page, *rect):
    return lift(Y, L, 'scheme', page, rect)


def P(page, *rect, more=(), items=()):
    return lift(Y, L, 'paper', page, rect, more=more, items=items)


_C6A = (95, 312, 465, 330)            # paper p5: the work-holding (c)
_C6B = (95, 712, 530, 730)            # paper p5: the CNC (c)

_SB = ("Section B is 'Any three parts @ 12 + 12 + 11 Marks': the card carries the 12 a part "
       "earns answered first or second; answered third it earns 11.")
_OR3 = ('The paper sets two (d)s either side of an OR, the metal properties and robotics in '
        'manufacturing; the scheme prices both "Award 2 @ 4 Marks", so they are one card, each '
        'branch a route.')
_OR6 = ('The paper sets two (c)s either side of an OR: the work-holding (c), whose (i)-(iii) '
        'are carded apart, and the CNC (c), "Any three" of four terms, carded at the letter.')
_OR7 = ('The paper sets two (c)s either side of an OR, the instruments and the circuit '
        'symbols, each "any three" of four; the scheme prices both "Award 3 @ 5 Marks", so '
        'they are one card, each branch a route.')
_B4 = "The scheme prints 'Any three: Award 3 @ 4 Marks' for the three parts answered."

CROPS = {
    # ---- paper ------------------------------------------------------------
    'engineering-2012-OL-paper-q1a-crop': dict(
        doc='paper', page=2, rect=(469, 73, 559, 145), image=True, ref='2012 OL Q1(a)'),
    'engineering-2012-OL-paper-q1b-crop': dict(
        doc='paper', page=2, rect=(486, 155, 527, 193), ref='2012 OL Q1(b)'),
    'engineering-2012-OL-paper-q1f-crop': dict(
        doc='paper', page=2, rect=(424, 227, 568, 308), image=True, ref='2012 OL Q1(f)'),
    'engineering-2012-OL-paper-q1h-crop': dict(
        doc='paper', page=2, rect=(406, 326, 550, 394), image=True, ref='2012 OL Q1(h)'),
    'engineering-2012-OL-paper-q1m-crop': dict(
        doc='paper', page=2, rect=(361, 726, 433, 791), image=True, ref='2012 OL Q1(m)'),
    # The scriber, radiator and step ladder pictured over their romans.
    'engineering-2012-OL-paper-q2a-crop': dict(
        doc='paper', page=3, rect=(95, 105, 505, 176), ref='2012 OL Q2(a)'),
    # The chisel with point A circled; the end of (b)(i)'s own line, which runs
    # into the box, is whited out.
    'engineering-2012-OL-paper-q3b-crop': dict(
        doc='paper', page=3, rect=(150, 506, 540, 580), mask=[(149, 505, 470, 514)],
        ref='2012 OL Q3(b)', letters=('A',)),
    'engineering-2012-OL-paper-q3dor-crop': dict(
        doc='paper', page=3, rect=(478, 694, 565, 812), image=True, ref='2012 OL Q3(d)'),
    'engineering-2012-OL-paper-q4a-crop': dict(
        doc='paper', page=4, rect=(475, 62, 522, 145), ref='2012 OL Q4(a)'),
    'engineering-2012-OL-paper-q4bi-crop': dict(
        doc='paper', page=4, rect=(464, 151, 563, 210), image=True, ref='2012 OL Q4(b)(i)'),
    'engineering-2012-OL-paper-q4biv-crop': dict(
        doc='paper', page=4, rect=(473, 229, 529, 284), image=True, ref='2012 OL Q4(b)(iv)'),
    'engineering-2012-OL-paper-q4d-crop': dict(
        doc='paper', page=4, rect=(478, 317, 559, 394), image=True, ref='2012 OL Q4(d)'),
    # The three components pictured with their captions.
    'engineering-2012-OL-paper-q5a-crop': dict(
        doc='paper', page=4, rect=(35, 480, 500, 600), ref='2012 OL Q5(a)'),
    'engineering-2012-OL-paper-q6a-crop': dict(
        doc='paper', page=5, rect=(195, 100, 345, 215), ref='2012 OL Q6(a)'),
    'engineering-2012-OL-paper-q6c-crop': dict(
        doc='paper', page=5, rect=(76, 340, 528, 496), ref='2012 OL Q6(c)'),
    # The hole and shaft with their dimensions; the end of (b)'s own line, which
    # runs into the box, is whited out.
    'engineering-2012-OL-paper-q7b-crop': dict(
        doc='paper', page=6, rect=(377, 145, 576, 296), mask=[(376, 190, 393, 208)],
        ref='2012 OL Q7(b)'),
    # Both (c)s' pictures: the instruments captioned (i)-(iv), and the
    # components under their names.
    'engineering-2012-OL-paper-q7c-crop': dict(
        doc='paper', parts=[(6, (30, 375, 565, 562)), (6, (60, 648, 560, 790))],
        ref='2012 OL Q7(c)'),
    # ---- scheme: the drawings the answers are given with -------------------
    # The dip-coating tank with its labels; the ends of the answer's own lines,
    # which run into the box at its left edge, are whited out.
    'engineering-2012-OL-scheme-q1i-sol': dict(
        doc='scheme', page=6, rect=(355, 350, 580, 480.5),
        mask=[(354, 349, 423, 385), (352, 464, 380, 480.5)], solution=True,
        ref='2012 OL Q1(i)'),
    'engineering-2012-OL-scheme-q2bii-sol': dict(
        doc='scheme', parts=[(9, (78, 325, 222, 506)), (9, (56, 523, 244, 744)),
                             (10, (41, 65, 229, 201))],
        layout='row', solution=True, ref='2012 OL Q2(b)(ii)'),
    # Each flame's name with its sketch beside it.
    'engineering-2012-OL-scheme-q4a-sol': dict(
        doc='scheme', page=13, rect=(75, 108, 432, 292), solution=True, ref='2012 OL Q4(a)'),
    'engineering-2012-OL-scheme-q5aii-sol': dict(
        doc='scheme', parts=[(14, (266, 308, 450, 378)), (14, (281, 469, 424, 576)),
                             (14, (290, 667, 405, 787))],
        layout='row', solution=True, ref='2012 OL Q5(a)(ii)'),
    'engineering-2012-OL-scheme-q7c-sol': dict(
        doc='scheme', page=18, rect=(85, 712, 502, 776), solution=True, ref='2012 OL Q7(c)'),
}

CARDS = [
    # ---- Question 1, Section A ("Any six @ 5 marks each") ------------------
    dict(key=(1, 'a', None),
         why='The CNC lathe is photographed beside (a); scheme p5 numbers two precautions; '
             '"3 + 2 Marks".',
         topic='eng-3-1',
         lifted=[S(5, 91, 371, 460, 386), S(5, 91, 387, 460, 403)],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         question_figure='engineering-2012-OL-paper-q1a-crop',
         notes="The scheme prints '3 + 2 Marks'."),
    dict(key=(1, 'b', None),
         why='The symbol is drawn beside (b); scheme p5 names the component and gives an '
             'application in the next sentence, each lifted by its own rectangle; "3 + 2 '
             'Marks".',
         topic='eng-2-16',
         lifted=[S(5, 61, 425, 231.5, 445), join(S(5, 231.5, 425, 460, 445),
                                               S(5, 61, 444, 460, 458))],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         question_figure='engineering-2012-OL-paper-q1b-crop',
         notes="The scheme prints '3 + 2 Marks'."),
    dict(key=(1, 'c', None),
         why='Scheme p5 defines the term in one sentence, "5 Marks".',
         topic='eng-3-8',
         lifted=[S(5, 61, 480, 460, 500)], marks=[5], total=5,
         notes="The scheme prints '5 Marks'."),
    dict(key=(1, 'd', None),
         why='Scheme p5 answers in one sentence, "5 Marks".',
         topic='eng-2-16',
         lifted=[S(5, 70, 522, 460, 542)], marks=[5], total=5,
         notes="The scheme prints '5 Marks'."),
    dict(key=(1, 'e', None),
         why='Scheme p5 answers in one sentence, "5 Marks".',
         topic='eng-1-9',
         lifted=[S(5, 70, 563, 460, 583)], marks=[5], total=5,
         notes="The scheme prints '5 Marks'."),
    dict(key=(1, 'f', None),
         why='The mechanism is photographed beside (f); scheme p5 names it and gives its use '
             'in one sentence, each lifted by its own word rectangle; "3 + 2 Marks".',
         topic='eng-2-15',
         lifted=[S(5, 70, 605, 159.5, 625), S(5, 159.5, 605, 460, 625)],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         question_figure='engineering-2012-OL-paper-q1f-crop',
         notes="The scheme prints '3 + 2 Marks'."),
    dict(key=(1, 'g', None),
         why='Scheme p5 describes a device after each roman; "3 + 2 Marks".',
         topic='eng-3-14',
         lifted=[S(5, 85, 647, 460, 663), S(5, 85, 663, 460, 679)],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         notes="The scheme prints '3 + 2 Marks'."),
    dict(key=(1, 'h', None),
         why='The instrument is photographed beside (h); scheme p5 names it, "5 Marks". The '
             'reader joins the Section B heading to (h), so the question is lifted from the '
             'page.',
         topic='eng-3-12',
         question_lift=P(2, 60, 342, 280, 359),
         lifted=[S(5, 61, 701, 460, 721)], marks=[5], total=5,
         question_figure='engineering-2012-OL-paper-q1h-crop',
         notes="The scheme prints '5 Marks'."),
    # ---- Question 1, Section B ("Any three parts @ 12 + 12 + 11 Marks") ----
    dict(key=(1, 'i', None),
         why='Scheme p6 describes each of the three under its name, the dip-coating tank '
             'beside a labelled drawing, shown with the answer; "Any one", "Award 12 (11) '
             'Marks".',
         topic='eng-2-15', stem=False,
         lifted=[[S(6, 85, 158, 460, 275), S(6, 85, 324, 510, 523), S(6, 85, 572, 510, 703)]],
         row_kind='anyN', group=(1, 12), marks=[12], tariff='fixed', total=12,
         figure='engineering-2012-OL-scheme-q1i-sol',
         notes="The scheme prints 'Any one: Good clear description Award 12 (11) Marks'. "
               + _SB),
    dict(key=(1, 'j', None),
         why='Scheme p7 explains each term under its name, "Any two", "Award 6 + 6(5)".',
         topic='eng-3-14', stem=False,
         lifted=[[S(7, 85, 99, 430, 215), S(7, 85, 223, 470, 312), S(7, 85, 319, 500, 519),
                  S(7, 85, 527, 470, 643)]],
         row_kind='anyN', group=(2, 6), marks=[12], tariff='fixed', total=12,
         notes="The scheme prints 'Any two: Good clear description Award 6 + 6(5)'. " + _SB),
    dict(key=(1, 'k', None),
         why='Scheme p7 defines the term and gives examples, each under its heading; '
             '"Definition Award 6", "Example Award 6(5)".',
         topic='eng-3-8', stem=False,
         lifted=[S(7, 85, 666, 432, 712), S(7, 85, 712, 432, 756)],
         marks=[6, 6], total=12,
         notes="The scheme prints 'Definition Award 6' and 'Example Award 6(5)'. " + _SB),
    dict(key=(1, 'l', None),
         why='Scheme p8 explains each term under its name, "Any two", "Award 6 + 6 (5)".',
         topic='eng-2-15', stem=False,
         lifted=[[S(8, 80, 126, 495, 229), S(8, 80, 237, 470, 339), S(8, 80, 347, 470, 436),
                  S(8, 80, 444, 470, 546)]],
         row_kind='anyN', group=(2, 6), marks=[12], tariff='fixed', total=12,
         notes="The scheme prints 'Any two: Good description Award 6 + 6 (5)'. " + _SB),
    dict(key=(1, 'm', None),
         why='The die is photographed beside (m); scheme p8 names it and gives its function '
             'under their headings, over one "Good clear description Award 12 (11) Marks", '
             'not split between them.',
         topic='eng-2-11', stem=False,
         lifted=[S(8, 80, 600, 420, 620), S(8, 80, 642, 470, 703)],
         tariff='questionTotal', total=12,
         question_figure='engineering-2012-OL-paper-q1m-crop',
         notes="The scheme prints 'Good clear description Award 12 (11) Marks'. " + _SB),
    # ---- Question 2 --------------------------------------------------------
    dict(key=(2, 'a', None),
         why='The three items are pictured over their romans; scheme p9 names a material '
             'after each, "Name Award 3 @ 4 Marks".',
         topic='eng-1-4',
         lifted=[S(9, 85, 126, 410, 141), S(9, 85, 141, 410, 155), S(9, 85, 155, 410, 172)],
         marks=[4, 4, 4], total=12,
         question_figure='engineering-2012-OL-paper-q2a-crop',
         notes="The scheme prints 'Name Award 3 @ 4 Marks'."),
    dict(key=(2, 'b', 'i'),
         why='Scheme p9 names a furnace after each metal, "Award 3 @ 3 Marks".',
         topic='eng-1-4',
         lifted=[S(9, 120, 226, 420, 240), S(9, 120, 240, 420, 253.5),
                 S(9, 120, 253.5, 420, 268)],
         marks=[3, 3, 3], total=9,
         notes="The scheme prints 'Award 3 @ 3 Marks'."),
    dict(key=(2, 'b', 'ii'),
         why='"Any one description": scheme pp9-10 describe the blast, cupola and electric '
             'arc furnace under their names, each beside a drawing of it, shown with the '
             'answer; "Good clear description", "Award 1 @ 9 Marks".',
         topic='eng-1-4',
         lifted=[[S(9, 270, 330, 530, 477), S(9, 270, 529, 530, 661), S(10, 280, 67, 555, 185)]],
         row_kind='anyN', group=(1, 9), marks=[9], tariff='fixed', total=9,
         figure='engineering-2012-OL-scheme-q2bii-sol',
         notes="The scheme prints 'Good clear description Award 1 @ 9 Marks'."),
    dict(key=(2, 'c', None),
         why='A lead-in over four metals set as romans, "any three"; scheme p10 states each '
             'after its roman, "Name Award 3 @ 3 Marks".',
         topic='eng-1-2',
         lifted=[[S(10, 110, 306, 390, 320), S(10, 110, 320, 390, 334), S(10, 110, 334, 390, 348),
                  S(10, 110, 348, 390, 363)]],
         row_kind='anyN', group=(3, 3), marks=[9], tariff='fixed', total=9,
         notes="The scheme prints 'Name Award 3 @ 3 Marks'."),
    dict(key=(2, 'd', None),
         why='Scheme p10 names two alloys, one a line, "Name Award 2 @ 3 Marks".',
         topic='eng-1-5',
         lifted=[S(10, 270, 458, 380, 472), S(10, 270, 472, 380, 488)],
         marks=[3, 3], total=6,
         notes="The scheme prints 'Name Award 2 @ 3 Marks'."),
    # ---- Question 3 --------------------------------------------------------
    dict(key=(3, 'a', None),
         why='A lead-in over three terms set as romans, "any two"; scheme p11 describes each '
             'under its name, "Any two descriptions", "Description Award 2 @ 7 marks".',
         topic='eng-2-6',
         lifted=[[join(S(11, 104, 126, 430, 146), S(11, 104, 146, 470, 257)),
                  S(11, 104, 264, 470, 326), S(11, 104, 333, 475, 408)]],
         row_kind='anyN', group=(2, 7), marks=[14], tariff='fixed', total=14,
         notes="The scheme prints 'Any two descriptions: Description Award 2 @ 7 marks'."),
    dict(key=(3, 'b', 'i'),
         why='The chisel is photographed with point A circled; scheme p11 describes the '
             'hardening and the tempering under their headings, "Good clear description '
             'Award 2 @ 6 Marks".',
         topic='eng-2-6',
         lifted=[S(11, 104, 430, 436, 519), S(11, 100, 526, 470, 615)],
         marks=[6, 6], total=12,
         question_figure='engineering-2012-OL-paper-q3b-crop',
         notes="The scheme prints 'Good clear description Award 2 @ 6 Marks', for the "
               "hardening and the tempering in that order."),
    dict(key=(3, 'b', 'ii'),
         why='Scheme p11 gives the reason in one paragraph, "Reason Award 5 Marks".',
         topic='eng-2-6',
         lifted=[S(11, 104, 648, 436, 712)], marks=[5], total=5,
         question_figure='engineering-2012-OL-paper-q3b-crop',
         notes="The scheme prints 'Reason Award 5 Marks'."),
    dict(key=(3, 'c', None),
         why='Scheme p12 gives two precautions in a paragraph each, "Good Description Award '
             '2 @ 3 Marks".',
         topic='eng-3-1',
         lifted=[S(12, 104, 97, 432, 130), S(12, 104, 152, 460, 185)],
         marks=[3, 3], total=6,
         notes="The scheme prints 'Good Description Award 2 @ 3 Marks'."),
    dict(key=(3, 'd', None),
         why='Paper p3 sets two alternative (d)s either side of an OR. Scheme p12 explains '
             'each property under its name, "Any two material properties", "Description '
             'Award 2 @ 4 Marks", and answers the robotics (i) and (ii) a paragraph each, '
             '"Safety Award 2 @ 4 Marks": priced alike, one card with a route per branch.',
         topic='eng-3-8', stem=False,
         question_lift=P(3, 95, 678, 350, 697, more=[(97, 700, 470, 720), (285, 728, 315, 748),
                                                     (95, 754, 450, 772), (95, 774, 455, 792)]),
         lifted=[[S(12, 96, 266, 460, 296), S(12, 96, 317, 460, 378), S(12, 96, 400, 480, 447)],
                 S(12, 104, 526, 430, 560), S(12, 108, 568, 460, 588)],
         row_kind='anyN', group=[(2, 4), None, None], marks=[8, 4, 4],
         routes=['a', 'b', 'b'], tariff='fixed', total=8,
         question_figure='engineering-2012-OL-paper-q3dor-crop',
         notes="The scheme prints 'Description Award 2 @ 4 Marks' and, for the OR, 'Safety "
               "Award 2 @ 4 Marks'. " + _OR3),
    # ---- Question 4 --------------------------------------------------------
    dict(key=(4, 'a', None),
         why='Scheme p13 names each flame under its setting and sketches it beside the name, '
             'shown with the answer; "Name & Sketch Award 3 @ 5 Marks". Each row is the '
             'setting\'s heading and the flame\'s name.',
         topic='eng-2-10',
         lifted=[join(S(13, 95, 113, 200, 131), S(13, 95, 141, 230, 159)),
                 join(S(13, 95, 182, 200, 200), S(13, 95, 210, 230, 228)),
                 join(S(13, 95, 238, 200, 256), S(13, 95, 265, 230, 283))],
         marks=[5, 5, 5], total=15,
         question_figure='engineering-2012-OL-paper-q4a-crop',
         figure='engineering-2012-OL-scheme-q4a-sol',
         notes="The scheme prints 'Name & Sketch Award 3 @ 5 Marks'."),
    dict(key=(4, 'b', 'i'),
         why='One of "Answer any three of the following": the spot welder is photographed '
             'beside it; scheme p13 gives two advantages on two lines, the 4 for the part not '
             'split between them.',
         topic='eng-2-10',
         lifted=[S(13, 115, 333, 430, 348.5), S(13, 115, 348.5, 430, 362)],
         tariff='questionTotal', total=4,
         question_figure='engineering-2012-OL-paper-q4bi-crop',
         notes=_B4),
    dict(key=(4, 'b', 'ii'),
         why='One of "Answer any three of the following": scheme p13 gives two requirements '
             'on two lines, the 4 for the part not split between them.',
         topic='eng-2-10',
         lifted=[S(13, 115, 362, 430, 378), S(13, 115, 378, 430, 392)],
         tariff='questionTotal', total=4, notes=_B4),
    dict(key=(4, 'b', 'iii'),
         why='One of "Answer any three of the following": scheme p13 answers in one line.',
         topic='eng-2-10',
         lifted=[S(13, 115, 389, 430, 405)], marks=[4], total=4, notes=_B4),
    dict(key=(4, 'b', 'iv'),
         why='One of "Answer any three of the following": the locknut is photographed beside '
             'it; scheme p13 answers in one sentence.',
         topic='eng-2-10',
         lifted=[S(13, 115, 403, 430, 449)], marks=[4], total=4,
         question_figure='engineering-2012-OL-paper-q4biv-crop',
         notes=_B4),
    dict(key=(4, 'c', 'i'),
         why='Scheme p13 gives three functions, one a line or two, "Good description Award '
             '3 @ 4 Marks", two asked here.',
         topic='eng-2-10',
         lifted=[S(13, 95, 485, 432, 517.5), S(13, 95, 517.5, 432, 545), S(13, 95, 545, 432, 560)],
         tariff='orderedSplit', notation='4 + 4', ladder=8, total=8,
         notes="The scheme prints 'Good description Award 3 @ 4 Marks' for (c): two parts "
               "here, one at (ii)."),
    dict(key=(4, 'c', 'ii'),
         why='Scheme p13 describes the passive flux and then the active flux, a paragraph '
             'each, the third of "Award 3 @ 4 Marks", not split between them.',
         topic='eng-2-10',
         lifted=[S(13, 95, 582, 470, 628), S(13, 95, 628, 480, 670)],
         tariff='questionTotal', total=4,
         notes="The scheme prints 'Good description Award 3 @ 4 Marks' for (c): two parts at "
               "(i), one here."),
    dict(key=(4, 'd', None),
         why='The welder is photographed beside (d); scheme p13 gives two precautions in two '
             'sentences, each lifted by its own rectangle; "Reasons Award 2 @ 3 Marks".',
         topic='eng-3-1',
         lifted=[join(S(13, 95, 706, 430, 723), S(13, 95, 723, 177.5, 738)),
                 S(13, 177.5, 723, 432, 738)],
         marks=[3, 3], total=6,
         question_figure='engineering-2012-OL-paper-q4d-crop',
         notes="The scheme prints 'Reasons Award 2 @ 3 Marks'."),
    # ---- Question 5 --------------------------------------------------------
    dict(key=(5, 'a', 'i'),
         why='The three components are pictured and captioned; scheme p14 names the process '
             'after each, "Any one process", "Name Award 1 @ 4 Marks".',
         topic='eng-1-9',
         lifted=[[S(14, 95, 140, 430, 156), S(14, 95, 156, 430, 170), S(14, 95, 170, 430, 190)]],
         row_kind='anyN', group=(1, 4), marks=[4], tariff='fixed', total=4,
         question_figure='engineering-2012-OL-paper-q5a-crop',
         notes="The scheme prints 'Name Award 1 @ 4 Marks'."),
    dict(key=(5, 'a', 'ii'),
         why='"Any one process": scheme p14 describes each process under its name over a '
             'drawing of it, shown with the answer; "Good description Award 12 Marks".',
         topic='eng-1-9',
         lifted=[[S(14, 80, 225, 432, 300), S(14, 80, 391, 490, 480), S(14, 80, 584, 420, 659)]],
         row_kind='anyN', group=(1, 12), marks=[12], tariff='fixed', total=12,
         question_figure='engineering-2012-OL-paper-q5a-crop',
         figure='engineering-2012-OL-scheme-q5aii-sol',
         notes="The scheme prints 'Good description Award 12 Marks'."),
    dict(key=(5, 'b', None),
         why='Scheme p15 bullets two precautions, "Safety precautions Award 2 @ 3 Marks".',
         topic='eng-3-1',
         lifted=[S(15, 85, 125, 428, 159), S(15, 85, 167, 430, 201)],
         marks=[3, 3], total=6,
         notes="The scheme prints 'Safety precautions Award 2 @ 3 Marks'."),
    dict(key=(5, 'c', None),
         why='A lead-in over four terms set as romans, "any three"; scheme p15 explains each '
             'under its name, "Explanation Award 3 @ 5 Marks".',
         topic='eng-1-9',
         lifted=[[join(S(15, 104, 277, 428, 306), S(15, 104, 306, 460, 339)),
                  S(15, 104, 346, 460, 394), S(15, 104, 402, 460, 463), S(15, 104, 471, 460, 504)]],
         row_kind='anyN', group=(3, 5), marks=[15], tariff='fixed', total=15,
         notes="The scheme prints 'Any three: Explanation Award 3 @ 5 Marks'."),
    dict(key=(5, 'd', None),
         why='Scheme p15 bullets two reasons, a paragraph each, "Good description Award 2 @ '
             '4 Marks".',
         topic='eng-1-9',
         lifted=[S(15, 85, 582, 445, 643), S(15, 85, 652, 445, 699)],
         marks=[4, 4], total=8,
         notes="The scheme prints 'Good description Award 2 @ 4 Marks'."),
    # ---- Question 6 --------------------------------------------------------
    dict(key=(6, 'a', None),
         why='The control knob is drawn under (a); scheme p16 describes six operations under '
             'their names, any three, "Name Award 3 @ 5 Marks".',
         topic='eng-2-11',
         lifted=[[S(16, 75, 160, 470, 217), S(16, 75, 225, 470, 273), S(16, 75, 280, 470, 328),
                  S(16, 75, 336, 470, 383), S(16, 75, 391, 470, 424), S(16, 75, 432, 480, 480)]],
         row_kind='anyN', group=(3, 5), marks=[15], tariff='fixed', total=15,
         question_figure='engineering-2012-OL-paper-q6a-crop',
         notes="The scheme prints 'Any three operations: Name Award 3 @ 5 Marks'."),
    dict(key=(6, 'b', None),
         why='A lead-in over four terms set as romans, "any three"; scheme pp16-17 describe '
             'each under its name, "Award 3 @ 5 Marks".',
         topic='eng-2-11',
         lifted=[[join(S(16, 75, 543, 425, 560), S(16, 75, 560, 470, 604)),
                  S(16, 75, 625, 470, 687), S(16, 75, 708, 500, 769), S(17, 75, 69, 495, 130)]],
         row_kind='anyN', group=(3, 5), marks=[15], tariff='fixed', total=15,
         notes="The scheme prints 'Any three: Award 3 @ 5 Marks' (under the box's heading "
               "'Cutting fluids')."),
    dict(key=(6, 'c', 'i'),
         why='The work-holding branch\'s (i), lifted with its cue; scheme p17 names the '
             'method, "Name & description Award 3 @ 5 Marks".',
         topic='eng-2-11', stem=False,
         question_lift=P(5, *_C6A, more=[(118, 519, 320, 537)]),
         lifted=[S(17, 230, 223, 360, 237)], marks=[5], total=5,
         question_figure='engineering-2012-OL-paper-q6c-crop',
         notes="The scheme prints 'Name & description Award 3 @ 5 Marks'. " + _OR6),
    dict(key=(6, 'c', 'ii'),
         why='The work-holding branch\'s (ii): scheme p17 names two methods on one line, each '
             'lifted by its own word rectangle, both asked for the part\'s 5.',
         topic='eng-2-11', stem=False,
         question_lift=P(5, *_C6A, more=[(118, 540, 395, 558)]),
         lifted=[S(17, 230, 237, 318.5, 251), S(17, 318.5, 237, 460, 251)],
         tariff='questionTotal', total=5,
         question_figure='engineering-2012-OL-paper-q6c-crop',
         notes="The scheme prints 'Name & description Award 3 @ 5 Marks'. " + _OR6),
    dict(key=(6, 'c', 'iii'),
         why='The work-holding branch\'s (iii): scheme p17 gives two precautions under "Two '
             'safety precautions:"; the paper asks one, "Award 3 @ 5 Marks".',
         topic='eng-3-1', stem=False,
         question_lift=P(5, *_C6A, more=[(118, 560, 455, 598)]),
         lifted=[[S(17, 100, 262, 400, 295), S(17, 100, 295, 400, 309)]],
         row_kind='anyN', group=(1, 5), marks=[5], tariff='fixed', total=5,
         question_figure='engineering-2012-OL-paper-q6c-crop',
         notes="The scheme prints 'Name & description Award 3 @ 5 Marks'. " + _OR6),
    dict(key=(6, 'c', None),
         why='The OR branch: "Explain any three of the following" four CNC terms; scheme p17 '
             'explains each under its name, "Explanation Award 3 @ 5 Marks". The scheme '
             'numbers CAD/CAM "(iv)"; the romans are left out of the options.',
         topic='eng-2-11', stem=False,
         question_lift=P(5, *_C6B, more=[(85, 740, 525, 757)]),
         lifted=[[S(17, 100, 422, 455, 491), S(17, 100, 513, 455, 574), S(17, 100, 595, 460, 657),
                  S(17, 100, 678, 460, 739)]],
         row_kind='anyN', group=(3, 5), marks=[15], tariff='fixed', total=15,
         notes="The scheme prints 'Any three: Explanation Award 3 @ 5 Marks'. " + _OR6),
    # ---- Question 7 --------------------------------------------------------
    dict(key=(7, 'a', None),
         why='A lead-in over three terms set as romans, "any two"; scheme p18 describes each '
             'under its name, "Good description Award 2 @ 5 Marks".',
         topic='eng-3-12',
         lifted=[[S(18, 100, 158, 425, 217), S(18, 100, 225, 470, 273), S(18, 100, 280, 420, 314)]],
         row_kind='anyN', group=(2, 5), marks=[10], tariff='fixed', total=10,
         notes="The scheme prints 'Any two: Good description Award 2 @ 5 Marks'."),
    dict(key=(7, 'b', None),
         why='The hole and shaft are drawn with their dimensions beside (b); scheme p18 states '
             'each value after its roman, "Calculations Award 4 @ 5 Marks". The question is '
             'lifted with its romans, which the reader files as parts of their own.',
         topic='eng-3-12', stem=False,
         question_lift=P(6, 95, 190, 395, 208, more=[(97, 213, 345, 231), (168, 234, 345, 252),
                                                     (168, 254, 345, 273),
                                                     (168, 275, 380, 320)]),
         lifted=[S(18, 85, 366, 425, 380), S(18, 85, 380, 425, 394), S(18, 85, 394, 425, 408),
                 S(18, 85, 408, 425, 422)],
         marks=[5, 5, 5, 5], total=20,
         question_figure='engineering-2012-OL-paper-q7b-crop',
         notes="The scheme prints 'Calculations Award 4 @ 5 Marks'."),
    dict(key=(7, 'c', None),
         why='Paper p6 sets two alternative (c)s either side of an OR, each "any three" of '
             'four. Scheme p18 names each instrument with an application after its roman, '
             '"Name & application Award 3 @ 5 Marks", and draws each component\'s symbol '
             'under its name, shown with the answer, "Symbols Award 3 @ 5 Marks": one card, '
             'each branch a route; a symbol row carries the component it is for.',
         topic='eng-3-12', stem=False,
         question_lift=P(6, 95, 358, 450, 376, more=[(280, 584, 310, 603), (95, 613, 485, 631),
                                                     (80, 650, 558, 668)]),
         lifted=[[S(18, 80, 504, 500, 518), S(18, 80, 518, 500, 532), S(18, 80, 532, 500, 546),
                  S(18, 80, 546, 500, 560)],
                 [S(18, 80, 671, 160, 691), S(18, 175, 671, 300, 691), S(18, 305, 671, 400, 691),
                  S(18, 405, 671, 520, 691)]],
         row_kind='anyN', group=[(3, 5), (3, 5)], marks=[15, 15], routes=['a', 'b'],
         tariff='fixed', total=15,
         question_figure='engineering-2012-OL-paper-q7c-crop',
         figure='engineering-2012-OL-scheme-q7c-sol',
         notes="The scheme prints 'Name & application Award 3 @ 5 Marks' and, for the OR, "
               "'Symbols Award 3 @ 5 Marks'. " + _OR7),
]

TOPICS = {}

ATLAS = {
    'eng-2012-ol-q6-c-iii': dict(
        topics=['CNC & Centre Lathe'],
        note='A safety precaution when turning long shafts between centres on the centre lathe; '
             'the card\'s syllabus heading is Health and safety.'),
}
