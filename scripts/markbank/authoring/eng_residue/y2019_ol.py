"""2019 Ordinary Level: every part, from the page.

Paper and scheme as the PDFs number their pages. The automatic author prices
nothing in this sitting: the scheme sets each answer in a left column and its
award in a box to the right ("Name Award 3 @ 3 Marks", "Award any 2 @ 5
Marks"), which its reader does not join to the answer, so every card here is
built from the page by rectangle. The marks grid is on scheme p4: Question 1
is Section A, "Any six @ 5 marks each", two-part answers 3 + 2, and Section B,
"Any three parts @ 12 + 12 + 11 marks", two-part answers 6 + 6 or 6 + 5;
Questions 2-7 are 45 marks each. A Section B card carries the 12 the scheme
awards a part answered first or second ("Award 12 (11) Marks"), and says the
third part answered earns 11.
"""
from eng_lift import join, lift

Y, L = 2019, 'ol'
OWNED = ('never shipped: the automatic author builds this card only from the lifts this '
         'entry records, so the entry owns it')


def S(page, *rect):
    return lift(Y, L, 'scheme', page, rect)


def P(page, *rect, more=(), items=()):
    return lift(Y, L, 'paper', page, rect, more=more, items=items)


_B2 = (80, 202, 510, 235)        # paper p3: (b)'s lead-in
_C2 = (80, 360, 515, 376)        # (c)'s
_D2 = (80, 716, 336, 732)        # (d)'s

_C4 = (84, 595, 257, 611)        # paper p5: (c)'s "Answer any three of the following:"
_C6 = (80, 371, 520, 401)        # paper p7: the knurling (c)'s lead-in

_SB = ("Section B is 'Any three parts @ 12 + 12 + 11 marks': the card carries the 12 a part "
       "earns answered first or second; answered third it earns 11.")
_OR3 = ('The paper sets two (d)s either side of an OR: the metal properties (d), carded at '
        'the letter, and the robotics (d), whose (i) and (ii) are carded apart.')
_OR6 = ('The paper sets two (c)s either side of an OR: the knurling (c), whose (i)-(iii) are '
        'carded apart, and the chess piece (c), carded at the letter.')
_OR7 = ('The paper sets two (c)s either side of an OR: the instruments (c), carded at the '
        'letter, and the electronic components (c), whose (i) and (ii) are carded apart.')

CROPS = {
    # ---- paper ------------------------------------------------------------
    # The camera without the descender of (a)'s "bandsaw." above it.
    'engineering-2019-OL-paper-q1b-crop': dict(
        doc='paper', page=2, rect=(369, 122, 456, 187), ref='2019 OL Q1(b)'),
    'engineering-2019-OL-paper-q1h-crop': dict(
        doc='paper', page=2, rect=(418, 328, 500, 384), ref='2019 OL Q1(h)'),
    # The three tools with their captions; the ask's own line runs into the
    # tailstock's top edge and is whited out.
    'engineering-2019-OL-paper-q1i-crop': dict(
        doc='paper', page=2, rect=(36, 476, 560, 598), mask=[(36, 470, 400, 486)],
        ref='2019 OL Q1(i)'),
    'engineering-2019-OL-paper-q4a-crop': dict(
        doc='paper', page=5, rect=(125, 100, 465, 305), ref='2019 OL Q4(a)',
        letters=('A', 'B', 'C')),
    'engineering-2019-OL-paper-q4b-crop': dict(
        doc='paper', page=5, rect=(52, 418, 562, 546), ref='2019 OL Q4(b)'),
    'engineering-2019-OL-paper-q5a-crop': dict(
        doc='paper', page=6, rect=(55, 70, 560, 205), ref='2019 OL Q5(a)',
        letters=('A', 'B', 'C')),
    'engineering-2019-OL-paper-q5c-crop': dict(
        doc='paper', page=6, rect=(82, 508, 556, 655), ref='2019 OL Q5(c)'),
    # The four lathe parts with their captions, without the ask above them.
    'engineering-2019-OL-paper-q6a-crop': dict(
        doc='paper', page=7, rect=(30, 98, 580, 222), ref='2019 OL Q6(a)'),
    'engineering-2019-OL-paper-q6c-crop': dict(
        doc='paper', page=7, rect=(240, 620, 300, 730), ref='2019 OL Q6(c)'),
    'engineering-2019-OL-paper-q7c-crop': dict(
        doc='paper', page=8, rect=(25, 380, 585, 512), ref='2019 OL Q7(c)'),
    # The OR branch's rover and its four components A-D; "in 7(c)(i)." runs
    # into the rover's left edge and is whited out.
    'engineering-2019-OL-paper-q7cor-crop': dict(
        doc='paper', page=8, parts=[(8, (400, 536, 558, 670)), (8, (95, 675, 475, 776))],
        mask=[(398, 652, 416, 668)], ref='2019 OL Q7(c)', letters=('A', 'B', 'C', 'D')),
    # ---- scheme: the drawings the answers are given with -------------------
    # Each furnace's name over its labelled diagram, the three a candidate may
    # choose from.
    'engineering-2019-OL-scheme-q2bi-sol': dict(
        doc='scheme', page=8, parts=[(8, (55, 218, 140, 240)), (8, (45, 274, 275, 500)),
                                     (8, (60, 514, 145, 535)), (8, (30, 572, 325, 760)),
                                     (9, (48, 55, 165, 76)), (9, (15, 108, 350, 262))],
        solution=True, ref='2019 OL Q2(b)(i)'),
    'engineering-2019-OL-scheme-q5aii-sol': dict(
        doc='scheme', page=13, parts=[(13, (12, 278, 270, 410)), (13, (60, 440, 272, 602)),
                                      (13, (50, 615, 275, 770))],
        solution=True, ref='2019 OL Q5(a)(ii)'),
}

CARDS = [
    # ---- Question 1, Section A ("Any six @ 5 marks each") ------------------
    dict(key=(1, 'a', None),
         why='Scheme p5 numbers two precautions; "3 + 2 Marks".',
         topic='eng-3-1',
         lifted=[S(5, 72, 398, 200, 413), S(5, 73, 413, 336, 428)],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         notes="The scheme prints '3 + 2 Marks'."),
    dict(key=(1, 'b', None),
         why='The camera is photographed beside (b); scheme p5 answers in one line, '
             '"5 Marks".',
         topic='eng-3-8',
         lifted=[S(5, 58, 442, 372, 457)], marks=[5], total=5,
         question_figure='engineering-2019-OL-paper-q1b-crop',
         notes="The scheme prints '5 Marks'."),
    dict(key=(1, 'c', None),
         why='Scheme p5 numbers two properties; "3 + 2 Marks".',
         topic='eng-1-5',
         lifted=[S(5, 74, 471, 252, 486), S(5, 74, 486, 118, 500)],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         notes="The scheme prints '3 + 2 Marks'."),
    dict(key=(1, 'd', None),
         why='Scheme p5 answers in one line, "5 Marks".',
         topic='eng-3-14',
         lifted=[S(5, 58, 514, 376, 529)], marks=[5], total=5,
         notes="The scheme prints '5 Marks'."),
    dict(key=(1, 'e', None),
         why='(e) asks for an example of each of two joints; scheme p5 answers each on '
             'its own line under one "3 + 2 Marks", so the two are one card at the letter.',
         topic='eng-2-10',
         lifted=[S(5, 58, 558, 240, 573), S(5, 58, 573, 250, 587)],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         notes="The scheme prints '3 + 2 Marks'."),
    dict(key=(1, 'f', None),
         why='The rack and pinion is photographed beside (f); scheme p5 names it and its '
             'use on two lines, "3 + 2 Marks".',
         topic='eng-2-15',
         lifted=[S(5, 66, 617, 148, 632), S(5, 67, 632, 347, 647)],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         question_figure='engineering-2019-OL-paper-q1f-art',
         notes="The scheme prints '3 + 2 Marks'."),
    dict(key=(1, 'g', None),
         why='Scheme p5 answers in one line, "5 Marks".',
         topic='eng-1-9',
         lifted=[S(5, 58, 675, 394, 690)], marks=[5], total=5,
         notes="The scheme prints '5 Marks'."),
    dict(key=(1, 'h', None),
         why='The symbol is drawn beside (h); scheme p5 names the component and its use '
             'on two lines, "3 + 2 Marks".',
         topic='eng-2-16',
         lifted=[S(5, 66, 719, 110, 734), S(5, 66, 734, 313, 749)],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         question_figure='engineering-2019-OL-paper-q1h-crop',
         notes="The scheme prints '3 + 2 Marks'."),
    # ---- Question 1, Section B ("Any three parts @ 12 + 12 + 11 marks") ----
    dict(key=(1, 'i', None),
         why='The three tools are photographed and captioned under (i); scheme p6 '
             'describes each under its name, "Any one", "Award 12 (11) Marks". The '
             'question is lifted with each caption on its own line, as the paper '
             'sets them under their pictures.',
         topic='eng-2-11', stem=False,
         question_lift=P(2, 60, 469, 390, 487, items=[(60, 580, 155, 598), (270, 580, 320, 598),
                                                 (445, 580, 505, 598)]),
         lifted=[[join(S(6, 76, 118, 165, 133), S(6, 76, 133, 447, 236)),
                  join(S(6, 76, 250, 116, 265), S(6, 76, 265, 447, 338)),
                  join(S(6, 76, 353, 127, 368), S(6, 76, 368, 444, 455))]],
         row_kind='anyN', group=(1, 12), marks=[12], tariff='fixed', total=12,
         question_figure='engineering-2019-OL-paper-q1i-crop',
         notes="The scheme prints 'Describe Award 12 (11) Marks'. " + _SB),
    dict(key=(1, 'j', None),
         why='Scheme pp6-7 explain each term under its name, "Any two", "Award 6 + 6(5)".',
         topic='eng-3-14', stem=False,
         lifted=[[join(S(6, 76, 497, 122, 512), S(6, 76, 512, 447, 556)),
                  join(S(6, 74, 565, 151, 580), S(6, 76, 580, 451, 668)),
                  join(S(6, 76, 677, 176, 692), S(6, 76, 692, 438, 781)),
                  join(S(7, 76, 57, 112, 72), S(7, 76, 72, 429, 131))]],
         row_kind='anyN', group=(2, 6), marks=[12], tariff='fixed', total=12,
         notes="The scheme prints 'Explain Award 6 + 6(5)'. " + _SB),
    dict(key=(1, 'k', None),
         why='Scheme p7 gives the definition and the example under their headings, '
             '"Definition Award 6", "Example Award 6(5)".',
         topic='eng-3-1', stem=False,
         lifted=[join(S(7, 75, 176, 117, 191), S(7, 76, 191, 417, 221)),
                 join(S(7, 76, 235, 126, 250), S(7, 76, 250, 440, 265))],
         marks=[6, 6], total=12,
         notes="The scheme prints 'Definition Award 6, Example Award 6(5)'. " + _SB),
    dict(key=(1, 'l', None),
         why='Scheme p7 explains each term under its name, "Any two", "Award 6 + 6 (5)".',
         topic='eng-2-11', stem=False,
         lifted=[[join(S(7, 76, 340, 180, 355), S(7, 76, 355, 416, 399)),
                  join(S(7, 76, 414, 130, 429), S(7, 76, 429, 434, 473)),
                  join(S(7, 76, 487, 109, 502), S(7, 76, 502, 445, 546)),
                  join(S(7, 76, 560, 119, 575), S(7, 76, 575, 440, 634))]],
         row_kind='anyN', group=(2, 6), marks=[12], tariff='fixed', total=12,
         notes="The scheme prints 'Explain Award 6 + 6 (5)'. " + _SB),
    dict(key=(1, 'm', None),
         why='The chuck is photographed beside (m); scheme p7 gives the name and the '
             'application on their own lines, "Name Award 6", "Application Award 6(5)".',
         topic='eng-2-11', stem=False,
         lifted=[S(7, 60, 697, 254, 712), S(7, 60, 726, 415, 756)],
         marks=[6, 6], total=12,
         question_figure='engineering-2019-OL-paper-q1m-art',
         notes="The scheme prints 'Name Award 6, Application Award 6(5)'. " + _SB),
    # ---- Question 2 --------------------------------------------------------
    dict(key=(2, 'a', None),
         why='A lead-in over three furnaces set as romans; scheme p8 names the metal '
             'for each on its own line, "Name Award 3 @ 3 Marks".',
         topic='eng-1-4',
         lifted=[S(8, 57, 89, 160, 101), S(8, 57, 104, 145, 116), S(8, 57, 119, 145, 131)],
         marks=[3, 3, 3], total=9,
         notes="The scheme prints 'Name Award 3 @ 3 Marks'."),
    dict(key=(2, 'b', 'i'),
         why='"Select one of the furnaces": scheme pp8-9 give each furnace\'s labelled '
             'diagram under its name, shown with the answer; each option is the '
             'furnace\'s name with the labels on its diagram. "Diagram and Labels @ 6 '
             'Marks".',
         topic='eng-1-4',
         question_lift=P(3, *_B2, more=[(104, 247, 285, 263)]), stem=False,
         checked='paper page 3: "(i) Label the main parts of the furnace;" under (b)\'s lead-in; '
                 'the semicolon is the list running on',
         lifted=[[join(S(8, 57, 220, 138, 238), S(8, 86, 279, 122, 295), S(8, 163, 286, 219, 302),
                       S(8, 201, 377, 237, 393), S(8, 51, 408, 108, 424), S(8, 221, 424, 245, 440)),
                  join(S(8, 61, 516, 142, 533), S(8, 254, 576, 307, 592), S(8, 33, 599, 95, 628),
                       S(8, 33, 644, 93, 661), S(8, 231, 632, 311, 648), S(8, 250, 676, 274, 692),
                       S(8, 42, 695, 92, 711), S(8, 240, 713, 299, 729)),
                  join(S(9, 49, 55, 163, 76), S(9, 114, 112, 168, 128), S(9, 190, 116, 273, 132),
                       S(9, 275, 163, 343, 179), S(9, 18, 181, 90, 197), S(9, 272, 234, 307, 250),
                       S(9, 45, 243, 110, 259))]],
         row_kind='anyN', group=(1, 6), marks=[6], tariff='fixed', total=6,
         figure='engineering-2019-OL-scheme-q2bi-sol',
         notes="The scheme prints '(i) Diagram and Labels @ 6 Marks', for the furnace "
               "selected."),
    dict(key=(2, 'b', 'ii'),
         why='Scheme pp8-9 list each furnace\'s charge beside its diagram; each option is '
             'lifted with its furnace\'s name. "Materials in charge @ 4 Marks".',
         topic='eng-1-4',
         question_lift=P(3, *_B2, more=[(104, 276, 290, 292)]), stem=False,
         checked='paper page 3: "(ii) List the materials used in the charge;" under (b)\'s lead-in; '
                 'the semicolon is the list running on',
         lifted=[[join(S(8, 57, 220, 138, 238), S(8, 347, 322, 484, 338)),
                  join(S(8, 61, 516, 142, 533), S(8, 360, 593, 529, 609)),
                  join(S(9, 49, 55, 163, 76), S(9, 384, 143, 537, 159))]],
         row_kind='anyN', group=(1, 4), marks=[4], tariff='fixed', total=4,
         notes="The scheme prints '(ii) Materials in charge @ 4 Marks', for the furnace "
               "selected."),
    dict(key=(2, 'b', 'iii'),
         why='Scheme pp8-9 describe how each furnace\'s charge is heated beside its '
             'diagram; each option is lifted with its furnace\'s name. "Heating the '
             'charge @ 3 Marks".',
         topic='eng-1-4',
         question_lift=P(3, *_B2, more=[(104, 305, 280, 321)]), stem=False,
         lifted=[[join(S(8, 57, 220, 138, 238), S(8, 348, 366, 574, 411)),
                  join(S(8, 61, 516, 142, 533), S(8, 360, 637, 580, 682)),
                  join(S(9, 49, 55, 163, 76), S(9, 384, 187, 581, 247))]],
         row_kind='anyN', group=(1, 3), marks=[3], tariff='fixed', total=3,
         notes="The scheme prints '(iii) Heating the charge @ 3 Marks', for the furnace "
               "selected."),
    dict(key=(2, 'c', 'i'),
         why='Scheme p9 answers in a two-column table, Material and Reason, one row a '
             'part; each material is lifted with its part\'s name, and the three frame '
             'materials are alternatives. "Material Award 3 @ 3 Marks".',
         topic='eng-3-14',
         question_lift=P(3, *_C2, more=[(104, 385, 512, 415)]), stem=False,
         checked='paper page 3: "(i) Name a suitable material for each of the parts labelled '
                 'on the personal transporter shown below;" under (c)\'s lead-in; '
                 'the semicolon is the list running on',
         lifted=[join(S(9, 77, 311, 120, 323), S(9, 137, 311, 177, 323)),
                 [join(S(9, 77, 340, 116, 352), S(9, 136, 340, 201, 352)),
                  join(S(9, 77, 340, 116, 352), S(9, 137, 355, 208, 367)),
                  join(S(9, 77, 340, 116, 352), S(9, 136, 370, 230, 382))],
                 join(S(9, 75, 399, 136, 411), S(9, 137, 399, 192, 411))],
         marks=[3, 3, 3], total=9, question_figure='engineering-2019-OL-paper-q2ci-art',
         notes="The scheme prints 'Material Award 3 @ 3 Marks'."),
    dict(key=(2, 'c', 'ii'),
         why='The Reason column of the same table; each reason is lifted with its part\'s '
             'name. "Reason Award 3 @ 2 Marks".',
         topic='eng-3-14',
         question_lift=P(3, *_C2, more=[(104, 427, 360, 443)]), stem=False,
         lifted=[join(S(9, 77, 311, 120, 323), S(9, 252, 311, 399, 323)),
                 join(S(9, 77, 340, 116, 352), S(9, 251, 340, 320, 352)),
                 join(S(9, 75, 399, 136, 411), S(9, 252, 399, 348, 411))],
         marks=[2, 2, 2], total=6, question_figure='engineering-2019-OL-paper-q2ci-art',
         notes="The scheme prints 'Reason Award 3 @ 2 Marks'."),
    dict(key=(2, 'd', 'i'),
         why='Scheme p9 names two alloys on one line; each is lifted by its own word '
             'rectangle. "Award 2 @ 2Marks".',
         topic='eng-1-5',
         question_lift=P(3, *_D2, more=[(104, 740, 195, 756)]), stem=False,
         checked='paper page 3: "(i) Name two alloys;" under (d)\'s lead-in; '
                 'the semicolon is the list running on',
         lifted=[S(9, 85, 484, 114, 498), S(9, 125, 484, 159, 498)],
         marks=[2, 2], total=4,
         notes="The scheme prints '(i) Named alloy Award 2 @ 2Marks'."),
    dict(key=(2, 'd', 'ii'),
         why='Scheme p9 gives the metals of each alloy, brass "or" solder, "Award 2 + 2": '
             'each metal is lifted with its alloy\'s name, and each alloy is a route.',
         topic='eng-1-5',
         question_lift=P(3, *_D2, more=[(104, 762, 458, 778)]), stem=False,
         lifted=[join(S(9, 84, 513, 118, 527), S(9, 119, 513, 158, 527)),
                 join(S(9, 84, 513, 118, 527), S(9, 179, 513, 202, 527)),
                 join(S(9, 84, 545, 123, 557), S(9, 122, 545, 149, 557)),
                 join(S(9, 84, 545, 123, 557), S(9, 169, 545, 188, 557))],
         marks=[2, 2, 2, 2], routes=['a', 'a', 'b', 'b'], total=4,
         notes="The scheme prints '(ii) Metals used Award 2 + 2', for one alloy."),
    # ---- Question 3 --------------------------------------------------------
    dict(key=(3, 'a', 'i'),
         why='The chisel is photographed with A and B ringed; scheme p10 explains '
             'hardening and tempering in a paragraph each, "Award 2 @ 5 Marks".',
         topic='eng-2-6',
         lifted=[S(10, 89, 148, 400, 180), S(10, 76, 222, 435, 253)],
         marks=[5, 5], total=10, question_figure='engineering-2019-OL-paper-q3ai-art',
         notes="The scheme prints '(i) Explain Award 2 @ 5 Marks'."),
    dict(key=(3, 'a', 'ii'),
         why='Scheme p10 under "Mechanical properties", one line; "0ne Property @ 5 '
             'Marks".',
         topic='eng-2-6',
         lifted=[S(10, 93, 298, 250, 310)], marks=[5], total=5,
         question_figure='engineering-2019-OL-paper-q3ai-art',
         notes="The scheme prints '0ne Property @ 5 Marks'."),
    dict(key=(3, 'a', 'iii'),
         why='Scheme p10 under "Mechanical properties", one line; "0ne Property @ 5 '
             'Marks".',
         topic='eng-2-6',
         lifted=[S(10, 93, 313, 245, 325)], marks=[5], total=5,
         question_figure='engineering-2019-OL-paper-q3ai-art',
         notes="The scheme prints '0ne Property @ 5 Marks'."),
    dict(key=(3, 'b', None),
         why='(b) asks to describe each of two terms; scheme p10 prices them together, '
             '"Award 1 @ 6 Marks, Award 1 @ 5 Marks", so the two are one card at the '
             'letter, 6 for one and 5 for the other.',
         topic='eng-2-6',
         lifted=[S(10, 90, 444, 408, 473),
                 join(S(10, 90, 503, 172, 515), S(10, 90, 517, 503, 575))],
         tariff='orderedSplit', notation='6 + 5', ladder=11, total=11,
         notes="The scheme prints 'Describe (i) & (ii) Award 1 @ 6 Marks, Award 1 @ 5 "
               "Marks'."),
    dict(key=(3, 'c', None),
         why='Scheme p10 bullets two precautions; "Award 2 @ 3 Marks".',
         topic='eng-3-1',
         lifted=[S(10, 112, 649, 410, 678), S(10, 112, 694, 377, 708)],
         marks=[3, 3], total=6,
         notes="The scheme prints 'Safety Precautions Award 2 @ 3 Marks'."),
    dict(key=(3, 'd', None),
         why='Paper p4 sets two alternative (d)s either side of an OR, and the reader '
             'files both under one key. This card is the first branch, the three metal '
             'properties; scheme p11 explains each under its name, "Award any 2 @ 4 '
             'Marks".',
         topic='eng-3-8', stem=False,
         question_lift=P(4, 84, 536, 500, 584),
         lifted=[[join(S(11, 95, 102, 161, 116), S(11, 95, 117, 455, 131)),
                  join(S(11, 97, 146, 184, 160), S(11, 98, 161, 459, 189)),
                  join(S(11, 96, 205, 157, 219), S(11, 96, 220, 491, 249))]],
         row_kind='anyN', group=(2, 4), marks=[8], tariff='fixed', total=8,
         notes="The scheme prints 'Explain Award any 2 @ 4 Marks'. " + _OR3),
    dict(key=(3, 'd', 'i'),
         why='The OR branch\'s (i); scheme p11 names two processes on one line, each '
             'lifted by its own word rectangle. "(i) Processes Award 2 @ 2 Marks".',
         topic='eng-3-14', stem=False,
         question_lift=P(4, 100, 662, 290, 696),
         lifted=[S(11, 174, 327, 259, 341), S(11, 269, 327, 386, 341)],
         marks=[2, 2], total=4,
         notes="The scheme prints '(i) Processes Award 2 @ 2 Marks'. " + _OR3),
    dict(key=(3, 'd', 'ii'),
         why='The OR branch\'s (ii); scheme p11 names two advantages on one line, each '
             'lifted by its own word rectangle. "(ii) Advantages Award 2 @ 2 Marks".',
         topic='eng-3-14', stem=False,
         question_lift=P(4, 100, 715, 265, 749),
         lifted=[S(11, 184, 341, 313, 355), S(11, 313, 341, 415, 355)],
         marks=[2, 2], total=4,
         notes="The scheme prints '(ii) Advantages Award 2 @ 2 Marks'. " + _OR3),
    # ---- Question 4 --------------------------------------------------------
    dict(key=(4, 'a', 'i'),
         why='The three flames are drawn and lettered A, B and C; scheme p11 names each '
             'on its own line, "Name Award 3 @ 3 Marks".',
         topic='eng-2-10',
         lifted=[S(11, 112, 542, 227, 556), S(11, 112, 556, 238, 570),
                 S(11, 112, 571, 219, 585)],
         marks=[3, 3, 3], total=9, question_figure='engineering-2019-OL-paper-q4a-crop',
         labels={'A': S(11, 148, 542, 227, 556), 'B': S(11, 148, 556, 238, 570),
                 'C': S(11, 148, 571, 219, 585)},
         notes="The scheme prints 'Name Award 3 @ 3 Marks'."),
    dict(key=(4, 'a', 'ii'),
         why='Scheme p11 gives each flame\'s proportions under its letter and name; '
             '"Proportions Award 3 @ 3 Marks".',
         topic='eng-2-10',
         lifted=[S(11, 109, 644, 402, 673), S(11, 108, 688, 370, 717),
                 S(11, 108, 732, 411, 761)],
         marks=[3, 3, 3], total=9, question_figure='engineering-2019-OL-paper-q4a-crop',
         labels={'A': S(11, 148, 542, 227, 556), 'B': S(11, 148, 556, 238, 570),
                 'C': S(11, 148, 571, 219, 585)},
         notes="The scheme prints 'Proportions Award 3 @ 3 Marks'."),
    dict(key=(4, 'b', None),
         why='A lead-in over four photographed items captioned as romans; scheme p12 '
             'describes each under its name, "Description of any three", "Award any 3 @ '
             '3 Marks".',
         topic='eng-2-10',
         lifted=[[join(S(12, 92, 112, 159, 129), S(12, 76, 127, 505, 187)),
                  join(S(12, 94, 203, 190, 220), S(12, 76, 221, 420, 264)),
                  join(S(12, 95, 276, 123, 293), S(12, 76, 293, 391, 307)),
                  join(S(12, 95, 320, 149, 336), S(12, 76, 337, 501, 395))]],
         row_kind='anyN', group=(3, 3), marks=[9], tariff='fixed', total=9,
         question_figure='engineering-2019-OL-paper-q4b-crop',
         notes="The scheme prints 'Descriptions Award any 3 @ 3 Marks'."),
    dict(key=(4, 'c', 'i'),
         why='"Answer any three of the following", four separate asks, carded per roman; '
             'scheme p12 names three methods on one line, any one, each lifted by its '
             'own word rectangle. "Award any 3 @ 4 Marks".',
         topic='eng-2-10',
         question_lift=P(5, *_C4, more=[(104, 617, 347, 633)]), stem=False,
         lifted=[[S(12, 98, 468, 164, 482), S(12, 171, 468, 219, 482),
                  S(12, 226, 468, 311, 482)]],
         row_kind='anyN', group=(1, 4), marks=[4], tariff='fixed', total=4,
         notes="The scheme prints 'Explanations Award any 3 @ 4 Marks'."),
    dict(key=(4, 'c', 'ii'),
         why='Scheme p12 answers in one paragraph; "Award any 3 @ 4 Marks".',
         topic='eng-2-16',
         question_lift=P(5, *_C4, more=[(104, 642, 421, 658)]), stem=False,
         lifted=[S(12, 95, 512, 458, 556)], marks=[4], total=4,
         notes="The scheme prints 'Explanations Award any 3 @ 4 Marks'."),
    dict(key=(4, 'c', 'iii'),
         why='Scheme p12 answers in two sentences, one for each hole; "Award any 3 @ 4 '
             'Marks" for the part.',
         topic='eng-3-12',
         question_lift=P(5, *_C4, more=[(104, 667, 392, 683)]), stem=False,
         lifted=[S(12, 95, 585, 488, 614)], marks=[4], total=4,
         notes="The scheme prints 'Explanations Award any 3 @ 4 Marks'."),
    dict(key=(4, 'c', 'iv'),
         why='Scheme p12 answers in one paragraph; "Award any 3 @ 4 Marks".',
         topic='eng-3-1',
         question_lift=P(5, *_C4, more=[(104, 692, 510, 708)]), stem=False,
         lifted=[S(12, 94, 651, 468, 680)], marks=[4], total=4,
         notes="The scheme prints 'Explanations Award any 3 @ 4 Marks'."),
    dict(key=(4, 'd', None),
         why='Scheme p12 bullets two precautions; "Award 2 @ 3 Marks".',
         topic='eng-3-1',
         lifted=[S(12, 111, 739, 383, 753), S(12, 111, 769, 414, 783)],
         marks=[3, 3], total=6,
         notes="The scheme prints 'Safety precautions Award 2 @ 3 Marks'."),
    # ---- Question 5 --------------------------------------------------------
    dict(key=(5, 'a', 'i'),
         why='The three processes are drawn and lettered A, B and C; scheme p13 names '
             'each on its own line, "Name Award 3 @ 3 Marks".',
         topic='eng-1-9',
         lifted=[S(13, 95, 134, 210, 148), S(13, 95, 163, 192, 177),
                 S(13, 95, 192, 225, 206)],
         marks=[3, 3, 3], total=9, question_figure='engineering-2019-OL-paper-q5a-crop',
         labels={'A': S(13, 115, 134, 210, 148), 'B': S(13, 115, 163, 192, 177),
                 'C': S(13, 115, 192, 225, 206)},
         notes="The scheme prints 'Name Award 3 @ 3 Marks'."),
    dict(key=(5, 'a', 'ii'),
         why='Scheme p13 describes each process under its name beside a labelled '
             'diagram, shown with the answer; any one, "Describe Award 12 Marks".',
         topic='eng-1-9',
         lifted=[[join(S(13, 75, 280, 176, 294), S(13, 277, 314, 491, 401)),
                  join(S(13, 76, 441, 159, 455), S(13, 281, 465, 494, 597)),
                  join(S(13, 76, 617, 198, 631), S(13, 280, 652, 517, 784))]],
         row_kind='anyN', group=(1, 12), marks=[12], tariff='fixed', total=12,
         question_figure='engineering-2019-OL-paper-q5a-crop',
         figure='engineering-2019-OL-scheme-q5aii-sol',
         notes="The scheme prints 'Describe Award 12 Marks'."),
    dict(key=(5, 'b', None),
         why='A lead-in over three terms set as romans; scheme p14 describes each under '
             'its name, "Award any 2 @ 5 Marks".',
         topic='eng-1-9',
         lifted=[[join(S(14, 103, 102, 215, 116), S(14, 104, 117, 353, 131)),
                  join(S(14, 104, 146, 185, 160), S(14, 104, 161, 431, 204)),
                  join(S(14, 107, 219, 182, 233), S(14, 107, 234, 401, 263))]],
         row_kind='anyN', group=(2, 5), marks=[10], tariff='fixed', total=10,
         notes="The scheme prints 'Describe Award any 2 @ 5 Marks'."),
    dict(key=(5, 'c', None),
         why='A lead-in over three photographed products captioned as romans; scheme '
             'p14 names plastics for each on its own line, "Award any 2 @ 4 Marks".',
         topic='eng-1-9',
         lifted=[[S(14, 103, 336, 356, 350), S(14, 104, 366, 359, 380),
                  S(14, 104, 395, 421, 409)]],
         row_kind='anyN', group=(2, 4), marks=[8], tariff='fixed', total=8,
         question_figure='engineering-2019-OL-paper-q5c-crop',
         notes="The scheme prints 'Name of Plastic Award any 2 @ 4 Marks'."),
    dict(key=(5, 'd', None),
         why='Scheme p14 bullets two precautions; "Award 2 @ 3 Marks".',
         topic='eng-3-1',
         lifted=[S(14, 112, 483, 405, 497), S(14, 112, 513, 343, 527)],
         marks=[3, 3], total=6,
         notes="The scheme prints 'Safety Precautions Award 2 @ 3 Marks'."),
    # ---- Question 6 --------------------------------------------------------
    dict(key=(6, 'a', None),
         why='Four lathe parts photographed and captioned (i)-(iv) with no words; scheme '
             'p15 names each under its roman, "Award any 3 @ 5 Marks".',
         topic='eng-2-11',
         lifted=[[S(15, 76, 130, 230, 146), S(15, 76, 156, 250, 170),
                  S(15, 76, 178, 175, 192), S(15, 76, 200, 150, 214)]],
         row_kind='anyN', group=(3, 5), marks=[15], tariff='fixed', total=15,
         question_figure='engineering-2019-OL-paper-q6a-crop',
         notes="The scheme prints 'Name Award any 3 @ 5 Marks'."),
    dict(key=(6, 'b', None),
         why='A lead-in over four terms set as romans; scheme p15 explains each beside '
             'its name, "Award any 3 @ 5 Marks".',
         topic='eng-2-11',
         lifted=[[S(15, 104, 280, 422, 309), S(15, 104, 324, 483, 382),
                  S(15, 107, 395, 498, 441), S(15, 104, 456, 480, 514)]],
         row_kind='anyN', group=(3, 5), marks=[15], tariff='fixed', total=15,
         notes="The scheme prints 'Explain Award any 3 @ 5 Marks'."),
    dict(key=(6, 'c', 'i'),
         why='The knurled dumbbell bar is photographed beside (c); scheme p15 names the '
             'process, "(i) Name @ 5 Marks".',
         topic='eng-2-11',
         question_lift=P(7, *_C6, more=[(104, 422, 372, 438)]), stem=False,
         lifted=[S(15, 107, 603, 152, 617)], marks=[5], total=5,
         question_figure='engineering-2019-OL-paper-q6cii-art',
         notes="The scheme prints '(i) Name @ 5 Marks'. " + _OR6),
    dict(key=(6, 'c', 'ii'),
         why='Scheme p15 describes the process in one paragraph, "(ii) Describe @ 5 '
             'Marks".',
         topic='eng-2-11',
         question_lift=P(7, *_C6, more=[(104, 449, 241, 465)]), stem=False,
         lifted=[S(15, 106, 647, 503, 706)], marks=[5], total=5,
         question_figure='engineering-2019-OL-paper-q6cii-art',
         notes="The scheme prints '(ii) Describe @ 5 Marks'. " + _OR6),
    dict(key=(6, 'c', 'iii'),
         why='Scheme p15 prints "(iii) Safety Precautions @ 3 + 2 Marks" over one line '
             'holding both precautions, joined inside one word ("on the lathe/wear '
             'PPE"); no rectangle parts them, so the line is one row worth the part\'s '
             '5.',
         topic='eng-3-1',
         question_lift=P(7, *_C6, more=[(104, 476, 359, 506)]), stem=False,
         lifted=[S(15, 106, 722, 475, 736)], marks=[5], total=5,
         question_figure='engineering-2019-OL-paper-q6cii-art',
         notes="The scheme prints '(iii) Safety Precautions @ 3 + 2 Marks' beside one "
               "line that holds both precautions. " + _OR6),
    dict(key=(6, 'c', None),
         why='The OR branch, the chess piece, has no romans and is the letter card; '
             'scheme p16 bullets three advantages, "Advantages Award 3 @ 5 Marks".',
         topic='eng-2-11', stem=False,
         question_lift=P(7, 84, 600, 475, 616, more=[(84, 735, 510, 767)]),
         lifted=[S(16, 112, 139, 446, 153), S(16, 112, 161, 332, 175),
                 S(16, 112, 184, 212, 198)],
         marks=[5, 5, 5], total=15, question_figure='engineering-2019-OL-paper-q6c-crop',
         notes="The scheme prints 'Advantages Award 3 @ 5 Marks'. " + _OR6),
    # ---- Question 7 --------------------------------------------------------
    dict(key=(7, 'a', None),
         why='A lead-in over three terms set as romans; scheme p16 describes each under '
             'its name, "Award any 2 @ 5 Marks".',
         topic='eng-3-12',
         lifted=[[join(S(16, 110, 465, 189, 479), S(16, 84, 479, 398, 509)),
                  join(S(16, 112, 531, 179, 545), S(16, 85, 546, 407, 575)),
                  join(S(16, 112, 597, 172, 611), S(16, 85, 612, 357, 626))]],
         row_kind='anyN', group=(2, 5), marks=[10], tariff='fixed', total=10,
         notes="The scheme prints 'Describe Award any 2 @ 5 Marks'."),
    dict(key=(7, 'b', None),
         why='"State the:" over four romans read off the dimensions shown; scheme p16 '
             'answers each on its own line, "Calculations Award 4 @ 5 Marks".',
         topic='eng-3-12',
         question_lift=P(8, 84, 135, 330, 166, more=[(84, 189, 316, 271)]),
         lifted=[S(16, 84, 668, 346, 684), S(16, 84, 684, 346, 699),
                 S(16, 84, 699, 346, 713), S(16, 84, 713, 346, 728)],
         marks=[5, 5, 5, 5], total=20, question_figure='engineering-2019-OL-paper-q7bi-art',
         notes="The scheme prints 'Calculations Award 4 @ 5 Marks'."),
    dict(key=(7, 'c', None),
         why='The instruments branch of (c): four photographs captioned (i)-(iv). Scheme '
             'p17 prices name and application apart, "Name & application (3 + 2)", '
             '"Award any 3 @ 5 Marks", so a name is claimed without its application; '
             'each application is shown with the instrument it is for.',
         topic='eng-3-12', stem=False,
         question_lift=P(8, 84, 355, 552, 371),
         lifted=[[S(17, 76, 161, 154, 175), S(17, 76, 190, 182, 204),
                  S(17, 76, 234, 213, 248), S(17, 76, 293, 163, 307)],
                 [S(17, 76, 161, 412, 175), S(17, 76, 190, 504, 219),
                  S(17, 76, 234, 502, 277), S(17, 76, 293, 382, 307)]],
         row_kind='anyN', group=[(3, 3), (3, 2)], marks=[9, 6], tariff='fixed', total=15,
         question_figure='engineering-2019-OL-paper-q7c-crop',
         notes="The scheme prints 'Name & application (3 + 2) Award any 3 @ 5 Marks'. "
               + _OR7),
    dict(key=(7, 'c', 'i'),
         why='The OR branch\'s (i): scheme p17 answers (i) and (ii) together, one line a '
             'component, "Name & Function (2 + 3)", "Award 3 @ 5 Marks"; each name is '
             'lifted by its own word rectangle.',
         topic='eng-2-16', stem=False,
         question_lift=P(8, 84, 578, 340, 613, more=[(100, 625, 400, 641)]),
         lifted=[[S(17, 76, 412, 163, 426), S(17, 76, 441, 157, 455),
                  S(17, 76, 471, 156, 485), S(17, 76, 500, 242, 514)]],
         row_kind='anyN', group=(3, 2), marks=[6], tariff='fixed', total=6,
         question_figure='engineering-2019-OL-paper-q7cor-crop',
         notes="The scheme prints '(i) & (ii) Name & Function (2 + 3) Award 3 @ 5 Marks'. "
               + _OR7),
    dict(key=(7, 'c', 'ii'),
         why='The OR branch\'s (ii): each function is lifted with the component it is '
             'for, from the same lines. "Name & Function (2 + 3)".',
         topic='eng-2-16', stem=False,
         question_lift=P(8, 84, 578, 340, 613, more=[(102, 652, 416, 668)]),
         lifted=[[S(17, 76, 412, 370, 426), S(17, 76, 441, 364, 455),
                  S(17, 76, 471, 361, 485), S(17, 76, 500, 475, 514)]],
         row_kind='anyN', group=(3, 3), marks=[9], tariff='fixed', total=9,
         question_figure='engineering-2019-OL-paper-q7cor-crop',
         notes="The scheme prints '(i) & (ii) Name & Function (2 + 3) Award 3 @ 5 Marks'. "
               + _OR7),
]

TOPICS = {}

_MAT = 'Materials: Properties and Uses'
_ROB = 'Energy, Electronics & Robotics'

ATLAS = {
    'eng-2019-ol-q2-c-i': dict(
        topics=[_MAT],
        note='Choosing a material for each part of the personal transporter; the card\'s '
             'syllabus heading is Technology, as every Ordinary Q2(c) card\'s is.'),
    'eng-2019-ol-q2-c-ii': dict(
        topics=[_MAT],
        note='The reason for each material chosen in (c)(i); the card\'s syllabus heading '
             'is Technology, as every Ordinary Q2(c) card\'s is.'),
    'eng-2019-ol-q3-d-i': dict(
        topics=[_ROB],
        note='Robots in manufacturing (the OR branch of Q3(d)); the card\'s syllabus '
             'heading is Technology, where the syllabus places robotics.'),
    'eng-2019-ol-q3-d-ii': dict(
        topics=[_ROB],
        note='Robots in manufacturing (the OR branch of Q3(d)); the card\'s syllabus '
             'heading is Technology, where the syllabus places robotics.'),
    'eng-2019-ol-q4-c-ii': dict(
        topics=['Welding & Soldering'],
        note='Testing a circuit before it is soldered; the card\'s syllabus heading is '
             'Electronics.'),
    'eng-2019-ol-q4-c-iii': dict(
        topics=['Welding & Soldering'],
        note='A threaded M5 hole against a drilled 5 mm hole, set in the joining question; '
             'the reference lists no metrology topic for Q4. The card\'s syllabus heading '
             'is Metrology.'),
    'eng-2019-ol-q6-c-iii': dict(
        topics=['CNC & Centre Lathe'],
        note='Safety precautions while knurling on the lathe; the card\'s syllabus '
             'heading is Health and safety.'),
}
