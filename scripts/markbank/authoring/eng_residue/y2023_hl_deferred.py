"""2023 Higher Level, deferred sitting: the parts eng_all refuses or gets wrong.

The SEC's deferred 2023 Higher paper and scheme (deferredexams/ and
deferredmarkingschemes/ LC027ALP000EV; Paper Trail "LC027ALP000EV-deferred"),
read as a sitting of their own (eng_deferred): ids "eng-2023-hl-deferred-...",
citations "... — Deferred sitting". Paper and scheme pages as the PDFs number
them. The marks grid is on scheme p3: Question 1 "Any ten @ 5 marks each",
Questions 2-9 50 marks each, any six answered. This scheme prints a part's
marks at the right-hand end of its last answer line ("Greasing/oiling ...
3 + 2"), which the automatic author reads into the answer, so most cards here
are rebuilt by rectangle with the marks left out; a `replaces=` names the
automatic card rebuilt before it ever shipped.
"""
from eng_lift import join, lift

Y, L = 2023, 'hl-deferred'
NEW = 'never shipped: the automatic card '
TAIL = NEW + 'read the scheme\'s marks, printed at the end of the last answer line, into the answer'


def S(page, *rect):
    return lift(Y, L, 'scheme', page, rect)


def SB(page, *rect):
    # Lifted with its leading bullet: a run of bullets inside one answer keeps
    # every bullet, not all but the first.
    return lift(Y, L, 'scheme', page, rect, bullet=False)


def P(page, *rect, more=(), items=()):
    return lift(Y, L, 'paper', page, rect, more=more, items=items)


K = 'engineering-2023-HL-deferred-'
_SA = "Question 1 is 'Any ten @ 5 marks each'."
_A6 = "The scheme prints 'Any three @ 6 + 6 + 6': each part answered earns 6."
_OR6 = ('The paper sets two (c)s either side of an OR: MIG welding, "16", carded at the '
        'letter, and the farming robotics (c), whose (i) and (ii) are carded apart.')
_OR8 = ('The paper sets two (c)s either side of an OR: the carbide inserts (c), whose (i) '
        '"4 + 4" and (ii) "8" are carded together at the letter, and the CNC (c), whose (i) '
        'and (ii) are carded apart.')
_OR9 = ('The paper sets two (c)s either side of an OR: the lawnmower (c), whose (i) "10" and '
        '(ii) "6" are carded together at the letter, and the circuit board (c), whose (i), '
        '(ii) and (iii) are carded apart.')
_B5 = (95, 261, 520, 294)              # paper p7: Q5(b), the alloy table's lead-in
_B5U = (95, 414, 260, 430)             # paper p7: "Using the graph paper supplied:"
_C8B = (85, 632, 495, 662)             # paper p10: the laser cutting (c)
_C9B = (85, 641, 480, 674)             # paper p11: the circuit board (c)

CROPS = {
    # ---- paper ------------------------------------------------------------
    K + 'paper-q1e-crop': dict(doc='paper', page=3, rect=(439, 278, 563, 364),
                               ref='2023 HL deferred Q1(e)'),
    # The hand exerciser with "Spring".
    K + 'paper-q1h-crop': dict(doc='paper', page=3, rect=(430, 408, 568, 520),
                               ref='2023 HL deferred Q1(h)'),
    K + 'paper-q1k-crop': dict(doc='paper', page=3, rect=(490, 585, 555, 650),
                               ref='2023 HL deferred Q1(k)'),
    K + 'paper-q1m-crop': dict(doc='paper', page=3, rect=(451, 703, 569, 771),
                               ref='2023 HL deferred Q1(m)'),
    K + 'paper-q3a-crop': dict(doc='paper', page=5, rect=(390, 102, 565, 223),
                               ref='2023 HL deferred Q3(a)'),
    K + 'paper-q3b-crop': dict(doc='paper', page=5, rect=(439, 306, 550, 472),
                               ref='2023 HL deferred Q3(b)'),
    K + 'paper-q3cii-crop': dict(doc='paper', page=5, rect=(401, 611, 554, 720),
                                 ref='2023 HL deferred Q3(c)(ii)'),
    K + 'paper-q4b-crop': dict(doc='paper', page=6, rect=(115, 240, 500, 478),
                               ref='2023 HL deferred Q4(b)', letters=('A', 'B', 'C')),
    # The hydraulic ram with "Ram surface".
    K + 'paper-q4c-crop': dict(doc='paper', page=6, rect=(416, 656, 565, 790),
                               ref='2023 HL deferred Q4(c)'),
    K + 'paper-q5a-crop': dict(doc='paper', page=7, rect=(396, 115, 551, 205),
                               ref='2023 HL deferred Q5(a)', letters=('A', 'B')),
    # The table of solidification temperatures, as printed.
    K + 'paper-q5b-crop': dict(doc='paper', page=7, rect=(62, 308, 545, 392),
                               ref='2023 HL deferred Q5(b)'),
    K + 'paper-q6a-crop': dict(doc='paper', page=8, rect=(381, 109, 565, 215),
                               ref='2023 HL deferred Q6(a)'),
    K + 'paper-q6c-crop': dict(doc='paper', page=8, rect=(412, 460, 545, 552),
                               ref='2023 HL deferred Q6(c)'),
    # The window section with its caption.
    # The window section; the end of (i)'s "diagram", which runs into it, is
    # whited out.
    K + 'paper-q7a-crop': dict(doc='paper', page=9, rect=(418, 90, 578, 265),
                               mask=[(417, 164, 432, 182)], ref='2023 HL deferred Q7(a)'),
    K + 'paper-q7bi-crop': dict(doc='paper', page=9, rect=(472, 325, 541, 399),
                                ref='2023 HL deferred Q7(b)(i)'),
    K + 'paper-q7bv-crop': dict(doc='paper', page=9, rect=(491, 419, 546, 520),
                                ref='2023 HL deferred Q7(b)(v)'),
    # The milling cutter with its caption.
    K + 'paper-q8c-crop': dict(doc='paper', page=10, rect=(462, 447, 584, 575),
                               ref='2023 HL deferred Q8(c)'),
    K + 'paper-q8cor-crop': dict(doc='paper', page=10, rect=(396, 670, 555, 771),
                                 ref='2023 HL deferred Q8(c)'),
    # The litter picker with "Litter picker jaws".
    K + 'paper-q9a-crop': dict(doc='paper', page=11, rect=(392, 100, 568, 197),
                               ref='2023 HL deferred Q9(a)'),
    K + 'paper-q9c-crop': dict(doc='paper', page=11, rect=(388, 435, 552, 562),
                               ref='2023 HL deferred Q9(c)'),
    # The circuit board with X and Y.
    K + 'paper-q9cor-crop': dict(doc='paper', page=11, rect=(360, 660, 540, 795),
                                 ref='2023 HL deferred Q9(c)', letters=('X', 'Y')),
    # ---- scheme: the drawings and workings the answers are given with ------
    K + 'scheme-q2b-sol': dict(doc='scheme', parts=[(5, (440, 695, 570, 785)),
                                                    (6, (422, 122, 572, 210)),
                                                    (6, (386, 278, 570, 378))],
                               layout='row', solution=True, ref='2023 HL deferred Q2(b)'),
    K + 'scheme-q3ai-sol': dict(doc='scheme', parts=[(8, (365, 70, 570, 226)),
                                                     (8, (160, 236, 510, 498))],
                                solution=True, ref='2023 HL deferred Q3(a)(i)'),
    K + 'scheme-q3bii-sol': dict(doc='scheme', parts=[(9, (333, 236, 450, 318)),
                                                      (9, (438, 144, 545, 298)),
                                                      (9, (450, 348, 570, 456))],
                                 layout='row', solution=True, ref='2023 HL deferred Q3(b)(ii)'),
    K + 'scheme-q3biii-sol': dict(doc='scheme', parts=[(9, (412, 503, 510, 572)),
                                                       (9, (412, 612, 512, 687))],
                                  solution=True, ref='2023 HL deferred Q3(b)(iii)'),
    K + 'scheme-q3ci-sol': dict(doc='scheme', page=10, rect=(338, 172, 584, 283), solution=True,
                                ref='2023 HL deferred Q3(c)(i)'),
    K + 'scheme-q3cii-sol': dict(doc='scheme', page=10, rect=(365, 470, 566, 655), solution=True,
                                 ref='2023 HL deferred Q3(c)(ii)'),
    K + 'scheme-q4c-sol': dict(doc='scheme', parts=[(12, (432, 50, 578, 190)),
                                                    (12, (436, 226, 563, 323))],
                               solution=True, ref='2023 HL deferred Q4(c)(i)'),
    K + 'scheme-q4cii-sol': dict(doc='scheme', parts=[(12, (165, 540, 512, 762)),
                                                      (13, (165, 212, 510, 344))],
                                 solution=True, ref='2023 HL deferred Q4(c)(ii)'),
    K + 'scheme-q5aiii-sol': dict(doc='scheme', page=14, rect=(366, 55, 566, 216), solution=True,
                                  ref='2023 HL deferred Q5(a)(iii)'),
    K + 'scheme-q5bi-sol': dict(doc='scheme', page=14, rect=(138, 335, 531, 568), solution=True,
                                ref='2023 HL deferred Q5(b)'),
    # The ratio worked as stacked fractions the text layer flattens.
    K + 'scheme-q5bii-sol': dict(doc='scheme', page=14, rect=(160, 661, 330, 697), solution=True,
                                 ref='2023 HL deferred Q5(b)(ii)'),
    K + 'scheme-q5c-sol': dict(doc='scheme', page=15, rect=(420, 200, 545, 405), solution=True,
                               ref='2023 HL deferred Q5(c)(i)'),
    K + 'scheme-q6aii-sol': dict(doc='scheme', page=16, rect=(330, 148, 568, 305), solution=True,
                                 ref='2023 HL deferred Q6(a)(ii)'),
    K + 'scheme-q6bii-sol': dict(doc='scheme', page=16, rect=(430, 624, 560, 722), solution=True,
                                 ref='2023 HL deferred Q6(b)(ii)'),
    K + 'scheme-q6biii-sol': dict(doc='scheme', page=17, rect=(375, 57, 553, 188), solution=True,
                                  ref='2023 HL deferred Q6(b)(iii)'),
    K + 'scheme-q6c-sol': dict(doc='scheme', page=17, rect=(108, 612, 548, 778),
                               mask=[(536, 760, 556, 778)], solution=True,
                               ref='2023 HL deferred Q6(c)'),
    K + 'scheme-q7ai-sol': dict(doc='scheme', page=18, rect=(152, 570, 546, 737), solution=True,
                                ref='2023 HL deferred Q7(a)(i)'),
    K + 'scheme-q7biv-sol': dict(doc='scheme', page=19, rect=(402, 462, 570, 602), solution=True,
                                 ref='2023 HL deferred Q7(b)(iv)'),
    K + 'scheme-q7ciii-sol': dict(doc='scheme', page=20, rect=(155, 350, 530, 672), solution=True,
                                  ref='2023 HL deferred Q7(c)(iii)'),
    K + 'scheme-q8bii-sol': dict(doc='scheme', page=21, rect=(462, 560, 568, 780), solution=True,
                                 ref='2023 HL deferred Q8(b)(ii)'),
    K + 'scheme-q8biii-sol': dict(doc='scheme', page=22, rect=(155, 102, 540, 226), solution=True,
                                  ref='2023 HL deferred Q8(b)(iii)'),
    K + 'scheme-q8bv-sol': dict(doc='scheme', page=22, rect=(405, 315, 580, 450), solution=True,
                                ref='2023 HL deferred Q8(b)(v)'),
    K + 'scheme-q9ai-sol': dict(doc='scheme', page=23, rect=(362, 380, 572, 565), solution=True,
                                ref='2023 HL deferred Q9(a)(i)'),
    K + 'scheme-q9bi-sol': dict(doc='scheme', page=24, rect=(366, 48, 560, 120), solution=True,
                                ref='2023 HL deferred Q9(b)(i)'),
    K + 'scheme-q9bv-sol': dict(doc='scheme', page=24, rect=(404, 510, 522, 740), solution=True,
                                ref='2023 HL deferred Q9(b)(v)'),
    # The steering mechanisms and the seat switch; the ends of the answer's
    # lines beside the lower drawing are whited out.
    K + 'scheme-q9c-sol': dict(doc='scheme', parts=[(25, (330, 84, 568, 392)),
                                                    (25, (415, 522, 560, 628))],
                               mask=[(329, 286, 362, 337)],
                               solution=True, ref='2023 HL deferred Q9(c)'),
    K + 'scheme-q9cor-sol': dict(doc='scheme', page=26, rect=(378, 200, 566, 300), solution=True,
                                 ref='2023 HL deferred Q9(c)(ii)'),
}

SPLIT = {}

FOLDED = {
    'eng-2023-hl-deferred-q5-c-i': 'never shipped: (i) is one option of "Select any two from '
                                   '(i), (ii) or (iii) below and explain", carried by the Q5(c) '
                                   'card',
}

CARDS = [
    # ---- Question 1 ("Any ten @ 5 marks each") ------------------------------
    dict(key=(1, 'c', None), replaces=TAIL,
         why='Scheme p4 bullets four methods, "3 + 2" printed at the end of the last.',
         topic='eng-3-7',
         lifted=[S(4, 132, 306, 520, 322), S(4, 132, 323, 520, 338), S(4, 132, 339, 520, 355),
                 S(4, 132, 356, 520, 371)],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         notes="The scheme prints '3 + 2'. " + _SA),
    dict(key=(1, 'd', None), replaces=TAIL,
         why='Scheme p4 answers in one sentence, "5" printed at its end.',
         topic='eng-1-4',
         lifted=[S(4, 100, 388, 520, 403)], marks=[5], total=5,
         notes="The scheme prints '5'. " + _SA),
    dict(key=(1, 'e', None), replaces=TAIL,
         why='The bicycle is pictured beside (e); scheme p4 bullets three benefits, "3 + 2" '
             'printed at the end of the last.',
         topic='eng-2-16',
         lifted=[S(4, 132, 431, 520, 447), S(4, 132, 448, 520, 463), S(4, 132, 464, 520, 480)],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         question_figure=K + 'paper-q1e-crop',
         notes="The scheme prints '3 + 2'. " + _SA),
    dict(key=(1, 'f', None), replaces=TAIL,
         why='Scheme p4 answers in two sentences, "5" printed at the end of the last line.',
         topic='eng-2-10',
         lifted=[S(4, 100, 496, 540, 543)], marks=[5], total=5,
         notes="The scheme prints '5'. " + _SA),
    dict(key=(1, 'g', None), replaces=TAIL,
         why='Scheme p4 bullets four benefits, "3 + 2" printed at the end of the last.',
         topic='eng-2-13',
         lifted=[S(4, 132, 576, 520, 591), S(4, 132, 592, 520, 608), S(4, 132, 608, 520, 624),
                 S(4, 132, 625, 520, 640)],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         notes="The scheme prints '3 + 2'. " + _SA),
    dict(key=(1, 'h', None),
         why='The hand exerciser is pictured beside (h) with its spring labelled; scheme p4 '
             'answers in one paragraph, "5".',
         topic='eng-2-15',
         lifted=[S(4, 100, 657, 525, 704)], marks=[5], total=5,
         question_figure=K + 'paper-q1h-crop',
         notes="The scheme prints '5'. " + _SA),
    dict(key=(1, 'i', None), replaces=TAIL,
         why='Scheme p4 answers in two sentences, "5" printed at the end of the last line.',
         topic='eng-2-16',
         lifted=[S(4, 100, 724, 540, 754)], marks=[5], total=5,
         notes="The scheme prints '5'. " + _SA),
    dict(key=(1, 'k', None),
         why='The football is pictured beside (k); scheme p5 answers in one sentence, "5".',
         topic='eng-1-9',
         lifted=[S(5, 100, 123, 535, 138)], marks=[5], total=5,
         question_figure=K + 'paper-q1k-crop',
         notes="The scheme prints '5'. " + _SA),
    dict(key=(1, 'm', None), replaces=TAIL,
         why='The drone is pictured beside (m); scheme p5 bullets five properties, "3 + 2" '
             'printed at the end of the last.',
         topic='eng-3-14',
         lifted=[S(5, 132, 279, 520, 295), S(5, 132, 295, 520, 311), S(5, 132, 312, 520, 327),
                 S(5, 132, 328, 520, 344), S(5, 132, 345, 520, 360)],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         question_figure=K + 'paper-q1m-crop',
         notes="The scheme prints '3 + 2'. " + _SA),
    # ---- Question 2 ("Answer all parts of this question") -------------------
    dict(key=(2, 'a', 'i'), replaces=TAIL,
         why='Scheme p5 explains the term in one paragraph, "5" printed at its end.',
         topic='eng-3-14',
         lifted=[S(5, 150, 442, 540, 504)], marks=[5], total=5,
         notes="The scheme prints '5'."),
    dict(key=(2, 'a', 'ii'), replaces=TAIL,
         why='Scheme p5 bullets seven examples of XR, "3 + 2" printed at the end of the last; '
             'the paper asks how it could benefit the environment, and the scheme opens on '
             'its own lead-in, quoted in the note.',
         topic='eng-3-14',
         lifted=[S(5, 165, 553, 520, 568), S(5, 165, 569, 520, 585), S(5, 165, 586, 520, 601),
                 S(5, 165, 602, 520, 618), S(5, 165, 619, 520, 634), S(5, 165, 635, 520, 651),
                 S(5, 165, 651, 520, 667)],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         notes="The scheme prints '3 + 2', and opens: '" + S(5, 150, 529, 400, 545) + "'"),
    dict(key=(2, 'b', None),
         why='A lead-in over three technologies set as romans, "any two"; scheme pp5-6 '
             'explain each under its name beside a picture, shown with the answer; one option '
             'each, "Any two @ 5 + 5".',
         topic='eng-3-14',
         lifted=[[join(S(5, 150, 694, 430, 757), S(6, 150, 46, 525, 77)),
                  join(S(6, 150, 109, 455, 124), S(6, 150, 124, 420, 220), S(6, 150, 220, 525, 251)),
                  S(6, 150, 275, 385, 385)]],
         row_kind='anyN', group=(2, 5), marks=[10], tariff='fixed', total=10,
         figure=K + 'scheme-q2b-sol',
         notes="The scheme prints 'Any two @ 5 + 5'."),
    dict(key=(2, 'c', None),
         replaces=NEW + 'took the last sentence of the SLAM answer for an option of its own',
         why='A lead-in over three terms set as romans, "any two"; scheme p6 explains each '
             'under its name, one option each, "Any two @ 5 + 5".',
         topic='eng-3-14',
         lifted=[[S(6, 150, 426, 525, 520), S(6, 150, 529, 525, 607), S(6, 150, 616, 525, 725)]],
         row_kind='anyN', group=(2, 5), marks=[10], tariff='fixed', total=10,
         notes="The scheme prints 'Any two @ 5 + 5'."),
    dict(key=(2, 'd', None),
         replaces=NEW + 'took the last sentence of the tourism answer for an option of its own',
         why='A lead-in over four applications set as romans, "any two"; scheme p7 explains '
             'each under its name, one option each, "Any two @ 5 + 5".',
         topic='eng-3-14',
         lifted=[[S(7, 150, 78, 525, 156), S(7, 150, 165, 525, 290), S(7, 150, 299, 525, 409),
                  S(7, 150, 418, 545, 480)]],
         row_kind='anyN', group=(2, 5), marks=[10], tariff='fixed', total=10,
         notes="The scheme prints 'Any two @ 5 + 5'."),
    dict(key=(2, 'e', 'i'),
         checked=('Paper p4 prints (e)(i) as the bare item "Safety", no stop, under "Discuss the '
                  'main concerns regarding the use of XR technology, with reference to the following:"'),
         why='Scheme p7 explains the safety concerns in one paragraph under the heading, "5".',
         topic='eng-3-1',
         lifted=[S(7, 150, 528, 545, 607)], marks=[5], total=5,
         notes="The scheme prints '5'."),
    # ---- Question 3 ---------------------------------------------------------
    dict(key=(3, 'a', 'i'),
         replaces=NEW + 'gave the test without the drawings the part asks for',
         why='The zip line is pictured beside (a); scheme p8 describes the test beside a '
             'drawing of it, then the graph of three materials\' profiles, shown with the '
             'answer; "10" for the part not split between them.',
         topic='eng-3-8',
         lifted=[S(8, 150, 80, 365, 190), S(8, 150, 513, 520, 545), S(8, 185, 545, 525, 576),
                 S(8, 185, 585, 525, 617), S(8, 185, 626, 525, 659)],
         tariff='questionTotal', total=10,
         question_figure=K + 'paper-q3a-crop',
         figure=K + 'scheme-q3ai-sol',
         notes="The scheme prints '10'."),
    dict(key=(3, 'b', 'i'),
         why='The machine is pictured beside (b); scheme p9 names it in one sentence, "4".',
         topic='eng-3-8',
         lifted=[S(9, 150, 77, 525, 93)], marks=[4], total=4,
         question_figure=K + 'paper-q3b-crop',
         notes="The scheme prints '4'."),
    dict(key=(3, 'b', 'ii'),
         replaces=NEW + 'ran both tests\' answers as points of one total where one test is '
                        'asked',
         why='"Any test carried out on this machine": scheme p9 describes the Charpy and the '
             'Izod test under their names beside drawings, shown with the answer; one option '
             'each, "8".',
         topic='eng-3-8',
         lifted=[[join(S(9, 150, 170, 440, 224), S(9, 150, 224, 332, 303)), S(9, 150, 336, 450, 438)]],
         row_kind='anyN', group=(1, 8), marks=[8], tariff='fixed', total=8,
         question_figure=K + 'paper-q3b-crop',
         figure=K + 'scheme-q3bii-sol',
         notes="The scheme prints '8', and opens: '" + S(9, 150, 146, 525, 162) + "'"),
    dict(key=(3, 'b', 'iii'),
         why='Scheme p9 describes each fracture in turn beside a drawing of it, shown with '
             'the answer; "6" for the part not split between them.',
         topic='eng-3-8',
         lifted=[S(9, 150, 516, 410, 580), S(9, 150, 611, 410, 690)],
         tariff='questionTotal', total=6,
         figure=K + 'scheme-q3biii-sol',
         notes="The scheme prints '6'."),
    dict(key=(3, 'c', 'i'),
         replaces=NEW + 'gave the test without the scheme\'s drawings of it',
         why='Scheme p10 describes the test in a sentence and four bullets beside drawings, '
             'then bullets examples; "8" for the part not split between them.',
         topic='eng-3-8',
         lifted=[S(10, 150, 68, 495, 99), S(10, 180, 108, 495, 124), S(10, 180, 124, 495, 156),
                 S(10, 180, 157, 495, 172), S(10, 180, 173, 495, 236), S(10, 180, 237, 495, 300),
                 S(10, 182, 331, 495, 346), S(10, 182, 347, 495, 363), S(10, 182, 364, 495, 379),
                 S(10, 182, 380, 495, 396)],
         tariff='questionTotal', total=8,
         figure=K + 'scheme-q3ci-sol',
         notes="The scheme prints '8'."),
    dict(key=(3, 'c', 'ii'),
         replaces=NEW + 'gave the test without the drawing the part asks for',
         why='The connecting rod is pictured beside (ii); scheme p10 names X-ray testing, '
             'describes it beside a labelled drawing, shown with the answer, and names two '
             'other methods; "8" for the part not split between them.',
         topic='eng-3-8',
         lifted=[S(10, 150, 448, 525, 463), S(10, 150, 472, 360, 676), S(10, 150, 685, 525, 700)],
         tariff='questionTotal', total=8,
         question_figure=K + 'paper-q3cii-crop',
         figure=K + 'scheme-q3cii-sol',
         notes="The scheme prints '8'."),
    # ---- Question 4 ---------------------------------------------------------
    dict(key=(4, 'b', 'i'),
         why='Line X is drawn on the diagram; scheme p11 explains it in one paragraph, "6".',
         topic='eng-1-3',
         lifted=[S(11, 138, 436, 525, 483)], marks=[6], total=6,
         question_figure=K + 'paper-q4b-crop',
         notes="The scheme prints '6'."),
    dict(key=(4, 'b', 'ii'),
         why='The regions are drawn at A, B and C; scheme p11 names each after its letter, '
             '"2 + 2 + 2" printed at the end of the last.',
         topic='eng-1-3',
         lifted=[S(11, 138, 509, 300, 524.5), S(11, 138, 524.5, 300, 540),
                 S(11, 138, 540, 300, 556)],
         marks=[2, 2, 2], total=6,
         labels={'A': S(11, 164, 509, 300, 524.5), 'B': S(11, 164, 524.5, 300, 540),
                 'C': S(11, 164, 540, 300, 556)},
         question_figure=K + 'paper-q4b-crop',
         notes="The scheme prints '2 + 2 + 2', for A, B and C in that order."),
    dict(key=(4, 'b', 'iii'),
         replaces=NEW + 'set the diagram\'s axis labels as the stem',
         why='Scheme p11 bullets the three steps and states the effect, "6" for the part not '
             'split between them.',
         topic='eng-2-6', stem=False,
         lifted=[S(11, 150, 596, 525, 611), S(11, 150, 612, 525, 628), S(11, 150, 629, 525, 644),
                 S(11, 140, 653, 525, 668)],
         tariff='questionTotal', total=6,
         question_figure=K + 'paper-q4b-crop',
         notes="The scheme prints '6'."),
    dict(key=(4, 'c', 'i'),
         why='The ram is pictured beside (c); scheme p12 describes induction hardening, or '
             'flame hardening, each beside a drawing, shown with the answer; "8" for either. '
             'The drawings\' labels are left out of the words.',
         topic='eng-2-6',
         lifted=[[S(12, 138, 46, 430, 203), S(12, 140, 236, 430, 330)]],
         row_kind='anyN', group=(1, 8), marks=[8], tariff='fixed', total=8,
         question_figure=K + 'paper-q4c-crop',
         figure=K + 'scheme-q4c-sol',
         notes="The scheme prints '8' after the two processes, set either side of an 'OR'."),
    dict(key=(4, 'c', 'ii'),
         why='"One suitable method": scheme pp12-13 describe the optical pyrometer, or the '
             'thermocouple pyrometer, each with a labelled drawing, shown with the answer; '
             '"8" for either.',
         topic='eng-2-6',
         lifted=[[S(12, 138, 367, 525, 525), S(13, 140, 76, 525, 202)]],
         row_kind='anyN', group=(1, 8), marks=[8], tariff='fixed', total=8,
         figure=K + 'scheme-q4cii-sol',
         notes="The scheme prints '8' after the two pyrometers, set either side of an 'OR'."),
    # ---- Question 5 ---------------------------------------------------------
    dict(key=(5, 'a', 'i'),
         why='The structures are drawn at A and B; scheme p13 names each in a sentence after '
             'its letter, "3 + 3".',
         topic='eng-1-3',
         lifted=[S(13, 138, 470, 400, 486), S(13, 138, 486, 400, 501)], marks=[3, 3], total=6,
         labels={'A': S(13, 172, 470, 400, 486), 'B': S(13, 172, 486, 400, 501)},
         question_figure=K + 'paper-q5a-crop',
         notes="The scheme prints '3 + 3', for A and B in that order."),
    dict(key=(5, 'a', 'ii'),
         why='Scheme p13 bullets examples of each structure, "2 + 2"; one metal asked for '
             'each, the answer to each any one of its list.',
         topic='eng-1-3',
         lifted=[[S(13, 150, 545, 300, 561), S(13, 150, 561, 300, 578), S(13, 150, 578, 300, 594),
                  S(13, 150, 594, 300, 611)],
                 [S(13, 150, 642, 300, 659), S(13, 150, 659, 300, 675), S(13, 150, 675, 300, 692),
                  S(13, 150, 692, 300, 708), S(13, 150, 708, 300, 725)]],
         marks=[2, 2], total=4,
         question_figure=K + 'paper-q5a-crop',
         notes="The scheme prints '2 + 2', for the body centred and the face centred cubic "
               "structure in that order."),
    dict(key=(5, 'a', 'iii'),
         replaces=NEW + 'gave the answer without the scheme\'s drawing of the changes',
         why='Scheme p14 explains the transformation and bullets its three forms beside a '
             'drawing, shown with the answer; "6" for the part not split between them.',
         topic='eng-1-3',
         lifted=[S(14, 138, 46, 362, 92), S(14, 150, 111, 365, 127), S(14, 150, 128, 365, 174),
                 S(14, 150, 175, 365, 222)],
         tariff='questionTotal', total=6,
         figure=K + 'scheme-q5aiii-sol',
         notes="The scheme prints '6'."),
    dict(key=(5, 'b', 'i'),
         why='"Draw the equilibrium diagram ... and label the liquidus and solidus lines": '
             'scheme p14 answers with the drawn diagram, shown with the answer, "Diagram 8", '
             '"Label 1 + 1". The question is lifted from the page with the table shown.',
         topic='eng-1-3', stem=False,
         question_lift=P(7, *_B5, more=[_B5U, (126, 441, 525, 471)]),
         special={'kind': 'ask'}, total=10,
         question_figure=K + 'paper-q5b-crop',
         figure=K + 'scheme-q5bi-sol',
         notes="The scheme prints 'Diagram 8' and 'Label 1 + 1'."),
    dict(key=(5, 'b', 'ii'),
         why='Scheme p14 works the ratio as stacked fractions the text layer flattens; the '
             'working is shown as printed, "4".',
         topic='eng-1-3', stem=False,
         question_lift=P(7, *_B5, more=[_B5U, (126, 482, 505, 513)]),
         special={'kind': 'ask'}, total=4,
         question_figure=K + 'paper-q5b-crop',
         figure=K + 'scheme-q5bii-sol',
         notes="The scheme prints '4'."),
    dict(key=(5, 'c', None),
         replaces=NEW + 'took each bullet and each sentence for an option of its own',
         why='"Select any two from (i), (ii) or (iii)"; scheme p15 explains each, the defects '
             'beside drawings of them, shown with the answer; one option each, "Any two @ 8 '
             '+ 8". The drawings\' captions are left out of the words.',
         topic='eng-1-3',
         lifted=[[S(15, 138, 220, 420, 370),
                  join(S(15, 138, 426, 525, 442), SB(15, 145, 450, 525, 516)),
                  join(S(15, 138, 565, 525, 627), SB(15, 140, 636, 525, 716),
                       S(15, 140, 725, 525, 741))]],
         row_kind='anyN', group=(2, 8), marks=[16], tariff='fixed', total=16,
         figure=K + 'scheme-q5c-sol',
         notes="The scheme prints 'Any two @ 8 + 8'."),
    # ---- Question 6 ---------------------------------------------------------
    dict(key=(6, 'a', 'i'),
         why='The tank is pictured beside (a); scheme p16 answers in one sentence, "4".',
         topic='eng-2-10',
         lifted=[S(16, 138, 79, 530, 110)], marks=[4], total=4,
         question_figure=K + 'paper-q6a-crop',
         notes="The scheme prints '4'."),
    dict(key=(6, 'a', 'ii'),
         replaces=NEW + 'gave the principle without the drawing the part asks for',
         why='Scheme p16 bullets the principle beside a drawing of the welder, shown with the '
             'answer, "12" for the part not split between them.',
         topic='eng-2-10',
         lifted=[S(16, 150, 167, 330, 230), S(16, 150, 231, 330, 247), S(16, 150, 248, 330, 279),
                 S(16, 150, 280, 370, 327), S(16, 150, 328, 525, 344), S(16, 150, 344, 525, 391)],
         tariff='questionTotal', total=12,
         question_figure=K + 'paper-q6a-crop',
         figure=K + 'scheme-q6aii-sol',
         notes="The scheme prints '12'."),
    dict(key=(6, 'b', 'ii'),
         replaces=NEW + 'gave the principle without the drawing the part asks for',
         why='One of "Answer any three of the following": scheme p16 describes friction '
             'welding beside a drawing, shown with the answer. The drawing\'s label is left '
             'out of the words.',
         topic='eng-2-10',
         lifted=[S(16, 138, 625, 520, 719)], marks=[6], total=6,
         figure=K + 'scheme-q6bii-sol', notes=_A6),
    dict(key=(6, 'b', 'iii'),
         replaces=NEW + 'gave the answer without the scheme\'s drawing of the circuit',
         why='One of "Answer any three of the following": scheme p17 explains the rectifier '
             'beside a drawing of the bridge, shown with the answer.',
         topic='eng-2-16',
         lifted=[S(17, 138, 62, 375, 171)], marks=[6], total=6,
         figure=K + 'scheme-q6biii-sol', notes=_A6),
    dict(key=(6, 'c', None),
         why='Paper p8 sets two alternative (c)s either side of an OR. This card is the '
             'first: MIG welding with reference to four bullets; scheme p17 answers under the '
             'same headings over drawings, shown with the answer; "16".',
         topic='eng-2-10', stem=False,
         question_lift=P(8, 85, 435, 530, 466, items=[(170, 474, 240, 490), (170, 490, 255, 506),
                                                      (170, 505, 290, 521), (170, 520, 245, 537)]),
         lifted=[S(17, 110, 355, 530, 607)], marks=[16], total=16,
         question_figure=K + 'paper-q6c-crop',
         figure=K + 'scheme-q6c-sol',
         notes="The scheme prints '16'. " + _OR6),
    # ---- Question 7 ---------------------------------------------------------
    dict(key=(7, 'a', 'i'),
         why='The window section is drawn beside (a); scheme p18 names extrusion and bullets '
             'its steps over a drawing of the extruder, shown with the answer, "12".',
         topic='eng-1-9',
         lifted=[join(S(18, 138, 427, 530, 457), S(18, 168, 458, 530, 556))], marks=[12],
         total=12,
         question_figure=K + 'paper-q7a-crop',
         figure=K + 'scheme-q7ai-sol',
         notes="The scheme prints '12'."),
    dict(key=(7, 'b', 'i'),
         why='One of "Answer any three of the following", the watch pictured beside it: '
             'scheme p19 lists four materials, one asked; it prints no justification.',
         topic='eng-1-9', stem=False,
         question_lift=P(9, 125, 344, 470, 375),
         lifted=[[S(19, 168, 227, 525, 243), S(19, 168, 244, 525, 259), S(19, 168, 260, 525, 276),
                  S(19, 168, 277, 525, 292)]],
         row_kind='anyN', group=(1, 6), marks=[6], tariff='fixed', total=6,
         question_figure=K + 'paper-q7bi-crop',
         notes=_A6 + " The scheme lists materials and prints no justification for them."),
    dict(key=(7, 'b', 'iv'),
         why='One of "Answer any three of the following": scheme p19 explains calendering '
             'beside a drawing of the rollers, shown with the answer.',
         topic='eng-1-9',
         lifted=[S(19, 138, 467, 400, 561)], marks=[6], total=6,
         figure=K + 'scheme-q7biv-sol', notes=_A6),
    dict(key=(7, 'b', 'v'),
         why='One of "Answer any three of the following", the bottle pictured beside it: '
             'scheme p19 bullets four properties, the 6 for the part not split between them.',
         topic='eng-1-9',
         lifted=[S(19, 168, 626, 525, 641), S(19, 168, 642, 525, 658), S(19, 168, 659, 525, 674),
                 S(19, 168, 675, 525, 691)],
         tariff='questionTotal', total=6,
         question_figure=K + 'paper-q7bv-crop', notes=_A6),
    dict(key=(7, 'c', 'i'), replaces=TAIL,
         why='Scheme p20 bullets four applications, "3 + 3" printed at the end of the last.',
         topic='eng-2-13',
         lifted=[S(20, 170, 93, 515, 125), S(20, 170, 126, 515, 141), S(20, 170, 142, 515, 158),
                 S(20, 170, 159, 515, 190)],
         tariff='orderedSplit', notation='3 + 3', ladder=6, total=6,
         notes="The scheme prints '3 + 3'."),
    dict(key=(7, 'c', 'iii'),
         why='Scheme p20 answers in a two-column table, thermoplastics then thermosetting '
             'plastics, shown with the answer; "5" for the part not split between them. Each '
             'row is one column, its heading first.',
         topic='eng-1-9',
         lifted=[join(S(20, 170, 357, 340, 372), SB(20, 160, 386, 340, 670)),
                 join(S(20, 350, 357, 525, 372), SB(20, 352, 386, 525, 640))],
         tariff='questionTotal', total=5,
         figure=K + 'scheme-q7ciii-sol',
         notes="The scheme prints '5'."),
    # ---- Question 8 ---------------------------------------------------------
    dict(key=(8, 'b', 'ii'),
         why='One of "Answer any three of the following": scheme p21 explains forming and '
             'generating in turn beside drawings, shown with the answer; the 6 for the part '
             'not split between them. The drawings\' captions are left out of the words.',
         topic='eng-2-11',
         lifted=[S(21, 138, 580, 460, 643), S(21, 140, 687, 460, 733)],
         tariff='questionTotal', total=6,
         figure=K + 'scheme-q8bii-sol', notes=_A6),
    dict(key=(8, 'b', 'iii'),
         why='One of "Answer any three of the following": scheme p22 describes each cutter in '
             'a sentence over drawings of both, shown with the answer; the 6 for the part not '
             'split between them.',
         topic='eng-2-11',
         lifted=[S(22, 140, 46, 555, 77), S(22, 140, 85, 525, 100)],
         tariff='questionTotal', total=6,
         figure=K + 'scheme-q8biii-sol', notes=_A6),
    dict(key=(8, 'b', 'v'),
         replaces=NEW + 'gave the angles without the drawing the part asks for',
         why='One of "Answer any three of the following": scheme p22 describes each angle '
             'beside a labelled drawing, shown with the answer; the 6 for the part not split '
             'between them. The drawing\'s labels are left out of the words.',
         topic='eng-2-11',
         lifted=[S(22, 140, 315, 395, 378), S(22, 140, 386, 400, 418)],
         tariff='questionTotal', total=6,
         figure=K + 'scheme-q8bv-sol', notes=_A6),
    dict(key=(8, 'c', None),
         why='Paper p10 sets two alternative (c)s either side of an OR. This card is the '
             'first, the milling cutter pictured beside it: scheme p22 bullets three '
             'advantages of carbide inserts, "4 + 4", and describes their manufacture, "8".',
         topic='eng-2-11', stem=False,
         question_lift=P(10, 85, 475, 420, 491, items=[(95, 504, 440, 520), (95, 526, 440, 542)]),
         lifted=[[S(22, 168, 521, 540, 553), S(22, 168, 554, 540, 569), S(22, 168, 570, 540, 586)],
                 S(22, 140, 609, 550, 766)],
         row_kind='anyN', group=[(2, 4), None], marks=[8, 8], total=16,
         question_figure=K + 'paper-q8c-crop',
         notes="The scheme prints '4 + 4' for (i) and '8' for (ii). " + _OR8),
    dict(key=(8, 'c', 'i'),
         replaces=NEW + 'ran the first branch\'s carbide answer and this branch\'s answer into '
                        'one ordered split',
         why='The OR branch\'s (i), the laser cutter pictured beside it: scheme p23 answers in '
             'one paragraph beside a picture of the motor, "8".',
         topic='eng-2-16', stem=False,
         question_lift=P(10, *_C8B, more=[(113, 684, 390, 716)]),
         lifted=[S(23, 140, 84, 440, 165)], marks=[8], total=8,
         question_figure=K + 'paper-q8cor-crop',
         notes="The scheme prints '8'. " + _OR8),
    dict(key=(8, 'c', 'ii'),
         replaces=NEW + 'ran the first branch\'s manufacture answer and this branch\'s answer '
                        'into one question total',
         why='The OR branch\'s (ii): scheme p23 bullets four advantages, "4 + 4".',
         topic='eng-2-11', stem=False,
         question_lift=P(10, *_C8B, more=[(113, 727, 390, 758)]),
         lifted=[S(23, 168, 219, 520, 234), S(23, 168, 235, 520, 251), S(23, 168, 252, 520, 267),
                 S(23, 168, 268, 520, 284)],
         tariff='orderedSplit', notation='4 + 4', ladder=8, total=8,
         question_figure=K + 'paper-q8cor-crop',
         notes="The scheme prints '4 + 4'. " + _OR8),
    # ---- Question 9 ---------------------------------------------------------
    dict(key=(9, 'a', 'i'),
         replaces=NEW + 'gave the mechanism without the drawing the part asks for',
         why='The litter picker is pictured beside (a); scheme p23 bullets a mechanism beside '
             'a labelled drawing, shown with the answer, and names another; "8" for the part '
             'not split between them. The drawing\'s labels are left out of the words.',
         topic='eng-2-15',
         lifted=[S(23, 168, 403, 360, 435), S(23, 168, 435, 360, 467), S(23, 168, 468, 360, 515),
                 S(23, 168, 516, 360, 579), S(23, 140, 588, 360, 667)],
         tariff='questionTotal', total=8,
         question_figure=K + 'paper-q9a-crop',
         figure=K + 'scheme-q9ai-sol',
         notes="The scheme prints '8'."),
    dict(key=(9, 'a', 'ii'), replaces=TAIL,
         why='Scheme p23 names two materials and justifies each in a sentence, "4 + 4" '
             'printed at the end of the last.',
         topic='eng-1-9',
         lifted=[S(23, 138, 698, 525, 730), S(23, 140, 738, 520, 770)], marks=[4, 4], total=8,
         question_figure=K + 'paper-q9a-crop',
         notes="The scheme prints '4 + 4'."),
    dict(key=(9, 'b', 'i'),
         replaces=NEW + 'gave the cylinder without the drawing the part asks for',
         why='One of "Answer any three of the following": scheme p24 describes the cylinder '
             'beside a drawing of it, shown with the answer. The drawing\'s labels are left '
             'out of the words.',
         topic='eng-2-15',
         lifted=[S(24, 138, 46, 365, 141)], marks=[6], total=6,
         figure=K + 'scheme-q9bi-sol', notes=_A6),
    dict(key=(9, 'b', 'iii'),
         replaces=NEW + 'mixed the advantages\' and disadvantages\' columns',
         why='One of "Answer any three of the following": scheme p24 sets four advantages and '
             'four disadvantages in two columns, one of each asked; the 6 for the part not '
             'split between them.',
         topic='eng-2-15',
         lifted=[[S(24, 180, 264, 340, 280), S(24, 180, 280, 340, 295), S(24, 180, 295, 340, 310),
                  join(S(24, 180, 310, 340, 325), S(24, 180, 325, 340, 340))],
                 [S(24, 375, 264, 560, 280), S(24, 375, 280, 560, 295), S(24, 375, 295, 560, 310),
                  join(S(24, 375, 310, 560, 325), S(24, 375, 325, 560, 340))]],
         tariff='questionTotal', total=6, notes=_A6),
    dict(key=(9, 'b', 'v'),
         replaces=NEW + 'read the scheme\'s "Any three @ 6 + 6 + 6" as a third use',
         why='One of "Answer any three of the following": scheme p24 gives two uses beside '
             'drawings of them, shown with the answer; one asked.',
         topic='eng-2-15',
         lifted=[[S(24, 168, 546, 525, 578), S(24, 168, 674, 525, 705)]],
         row_kind='anyN', group=(1, 6), marks=[6], tariff='fixed', total=6,
         figure=K + 'scheme-q9bv-sol', notes=_A6),
    dict(key=(9, 'c', None),
         why='Paper p11 sets two alternative (c)s either side of an OR. This card is the '
             'first, the lawnmower pictured beside it: scheme p25 describes steering '
             'mechanisms beside labelled drawings, "10", and a seat safety switch beside a '
             'drawing, "6", shown with the answer. The drawings\' labels are left out of the '
             'words.',
         topic='eng-2-15', stem=False,
         question_lift=P(11, 85, 452, 390, 485, more=[(95, 496, 385, 545), (95, 555, 495, 588)]),
         lifted=[S(25, 140, 60, 410, 336),
                 join(S(25, 140, 450, 525, 497), S(25, 168, 514, 525, 706))],
         marks=[10, 6], total=16,
         question_figure=K + 'paper-q9c-crop',
         figure=K + 'scheme-q9c-sol',
         notes="The scheme prints '10' for (i) and '6' for (ii). " + _OR9),
    dict(key=(9, 'c', 'i'),
         replaces=NEW + 'ran the first branch\'s steering answer and this branch\'s answer '
                        'into one question total',
         why='The OR branch\'s (i), the board pictured with X and Y: scheme p26 names each '
             'component, "2 + 2" printed at the end of the last.',
         topic='eng-2-16', stem=False,
         question_lift=P(11, *_C9B, more=[(113, 685, 330, 701)]),
         lifted=[S(26, 138, 79, 525, 94), S(26, 138, 103, 520, 119)], marks=[2, 2], total=4,
         labels={'X': S(26, 236, 79, 525, 94), 'Y': S(26, 229, 103, 520, 119)},
         question_figure=K + 'paper-q9cor-crop',
         notes="The scheme prints '2 + 2', for X and Y in that order. " + _OR9),
    dict(key=(9, 'c', 'ii'),
         replaces=NEW + 'ran the first branch\'s safety answer and this branch\'s answer into '
                        'one question total',
         why='The OR branch\'s (ii), "X or Y": scheme p26 explains each component\'s function, '
             'the potentiometer beside drawings, shown with the answer; one asked, "6".',
         topic='eng-2-16', stem=False,
         question_lift=P(11, *_C9B, more=[(113, 712, 340, 728)]),
         lifted=[[S(26, 138, 156, 525, 203), S(26, 140, 211, 375, 273)]],
         row_kind='anyN', group=(1, 6), marks=[6], tariff='fixed', total=6,
         question_figure=K + 'paper-q9cor-crop',
         figure=K + 'scheme-q9cor-sol',
         notes="The scheme prints '6'. " + _OR9),
]

TOPICS = {}

ATLAS = {}
