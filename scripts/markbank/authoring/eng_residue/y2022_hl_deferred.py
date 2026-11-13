"""2022 Higher Level, deferred sitting: the parts eng_all refuses or gets wrong.

The SEC's deferred 2022 Higher paper and scheme (deferredexams/ and
deferredmarkingschemes/ LC027ALP000EV; Paper Trail "LC027ALP000EV-deferred"),
read as a sitting of their own (eng_deferred): ids "eng-2022-hl-deferred-...",
citations "... — Deferred sitting". Paper and scheme pages as the PDFs number
them. The marks grid is on scheme p3: Question 1 "Any ten @ 5 marks each",
Questions 2-9 50 marks each, any five answered. This sitting had no cards
before the lane: a `replaces=` names the automatic card it rebuilds before it
ever shipped.
"""
from eng_lift import join, lift

Y, L = 2022, 'hl-deferred'
NEW = 'never shipped: the automatic card '


def S(page, *rect):
    return lift(Y, L, 'scheme', page, rect)


def SB(page, *rect):
    # Lifted with its leading bullet: a run of bullets inside one answer keeps
    # every bullet, not all but the first.
    return lift(Y, L, 'scheme', page, rect, bullet=False)


def P(page, *rect, more=(), items=()):
    return lift(Y, L, 'paper', page, rect, more=more, items=items)


def _ck(page, part, lead):
    return (f'Paper p{page} prints {part} as one item of the list under "{lead}"; the '
            'semicolon ends the item, not the question.')


K = 'engineering-2022-HL-deferred-'
_SA = "Question 1 is 'Any ten @ 5 marks each'."
_A5 = "The scheme prints 'Any two @ 8 + 8': each part answered earns 8."
_A6 = "The scheme prints 'Any three @ 6 + 6 + 6': each part answered earns 6."
_A8 = "The scheme prints 'Any three @ 6 + 6 + 6': each part answered earns 6."
_A9 = "The scheme prints '(Any three) 6 + 6 + 6': each part answered earns 6."
_OR6 = ('The paper sets two (c)s either side of an OR: submerged arc welding, "16", carded '
        'at the letter, and the robotics (c), whose (i) and (ii) are carded apart.')
_OR8 = ('The paper sets two (c)s either side of an OR: the magnetic chuck and up-cut '
        'milling, "8" each and both asked, carded at the letter, and the CNC (c), whose (i) '
        'and (ii) are carded apart.')
_OR9 = ('The paper sets two (c)s either side of an OR: the turntable\'s drive and support, '
        '"8 + 8", carded at the letter, and the relay and stepper motor (c), whose (i) and '
        '(ii) are carded apart.')
_B5 = (85, 257, 530, 290)              # paper p7: Q5(b), the alloy table's lead-in
_B5U = (95, 419, 260, 435)             # paper p7: "Using the graph paper supplied:"
_C8B = (85, 576, 395, 592)             # paper p10: the CNC (c)
_C9B = (85, 656, 440, 687)             # paper p11: the relay and stepper motor (c)

CROPS = {
    # ---- paper ------------------------------------------------------------
    K + 'paper-q1a-crop': dict(doc='paper', page=3, rect=(420, 96, 565, 179),
                               ref='2022 HL deferred Q1(a)'),
    # The headlamp, asked about by (g) and (h).
    K + 'paper-q1g-crop': dict(doc='paper', page=3, rect=(452, 407, 562, 461),
                               ref='2022 HL deferred Q1(g)'),
    K + 'paper-q1i-crop': dict(doc='paper', page=3, rect=(463, 510, 561, 570),
                               ref='2022 HL deferred Q1(i)'),
    K + 'paper-q1m-crop': dict(doc='paper', page=3, rect=(400, 692, 532, 768),
                               ref='2022 HL deferred Q1(m)'),
    K + 'paper-q3cii-crop': dict(doc='paper', page=5, rect=(427, 661, 537, 773),
                                 ref='2022 HL deferred Q3(c)(ii)'),
    K + 'paper-q4b-crop': dict(doc='paper', page=6, rect=(115, 296, 512, 552),
                               ref='2022 HL deferred Q4(b)', letters=('A', 'B', 'C', 'D')),
    # The crankshaft with "Machined surface".
    K + 'paper-q4c-crop': dict(doc='paper', page=6, rect=(390, 657, 563, 792),
                               ref='2022 HL deferred Q4(c)'),
    # The table of solidification temperatures, as printed.
    K + 'paper-q5b-crop': dict(doc='paper', page=7, rect=(92, 318, 535, 390),
                               ref='2022 HL deferred Q5(b)'),
    K + 'paper-q5c-crop': dict(doc='paper', page=7, rect=(335, 555, 560, 640),
                               ref='2022 HL deferred Q5(c)(i)', letters=('A', 'B', 'C')),
    K + 'paper-q6a-crop': dict(doc='paper', page=8, rect=(408, 125, 567, 234),
                               ref='2022 HL deferred Q6(a)'),
    K + 'paper-q6cor-crop': dict(doc='paper', page=8, rect=(398, 621, 556, 747),
                                 ref='2022 HL deferred Q6(c)'),
    K + 'paper-q7a-crop': dict(doc='paper', page=9, rect=(338, 150, 578, 258),
                               ref='2022 HL deferred Q7(a)'),
    K + 'paper-q7c-crop': dict(doc='paper', page=9, rect=(265, 583, 515, 665),
                               ref='2022 HL deferred Q7(c)(i)'),
    # The engine block with "X" and its caption.
    K + 'paper-q8b-crop': dict(doc='paper', page=10, rect=(382, 318, 560, 437),
                               ref='2022 HL deferred Q8(b)'),
    K + 'paper-q8cor-crop': dict(doc='paper', page=10, rect=(401, 589, 555, 696),
                                 ref='2022 HL deferred Q8(c)'),
    # The forklift with its X and Y directions.
    K + 'paper-q9a-crop': dict(doc='paper', page=11, rect=(365, 84, 560, 238),
                               ref='2022 HL deferred Q9(a)'),
    K + 'paper-q9c-crop': dict(doc='paper', page=11, rect=(398, 478, 560, 574),
                               ref='2022 HL deferred Q9(c)'),
    K + 'paper-q9cor-crop': dict(doc='paper', page=11, rect=(450, 575, 540, 772),
                                 ref='2022 HL deferred Q9(c)'),
    # ---- scheme: the drawings and workings the answers are given with ------
    # The separator; the end of the answer's first line, which runs into the
    # drawing, is whited out.
    K + 'scheme-q1c-sol': dict(doc='scheme', page=4, rect=(300, 300, 572, 440),
                               mask=[(300, 326, 353, 343)], solution=True,
                               ref='2022 HL deferred Q1(c)'),
    # Young's modulus worked as a stacked fraction the text layer flattens.
    K + 'scheme-q1l-sol': dict(doc='scheme', page=6, rect=(65, 322, 460, 357), solution=True,
                               ref='2022 HL deferred Q1(l)'),
    K + 'scheme-q2b-sol': dict(doc='scheme', page=7, rect=(118, 200, 570, 370), solution=True,
                               ref='2022 HL deferred Q2(b)'),
    K + 'scheme-q2dii-sol': dict(doc='scheme', page=9, rect=(292, 70, 582, 222), solution=True,
                                 ref='2022 HL deferred Q2(d)(ii)'),
    K + 'scheme-q3bi-sol': dict(doc='scheme', parts=[(10, (368, 276, 588, 511)),
                                                     (10, (405, 570, 565, 660))],
                                solution=True, ref='2022 HL deferred Q3(b)(i)'),
    K + 'scheme-q3ci-sol': dict(doc='scheme', page=11, rect=(452, 186, 566, 328), solution=True,
                                ref='2022 HL deferred Q3(c)(i)'),
    K + 'scheme-q3cii-sol': dict(doc='scheme', page=11, rect=(65, 550, 565, 714), solution=True,
                                 ref='2022 HL deferred Q3(c)(ii)'),
    # The pyrometers' drawings and the two steels on the diagram; the ends of
    # the (iv) answer's lines, which run beside the diagram, are whited out.
    K + 'scheme-q4a-sol': dict(doc='scheme', parts=[(12, (130, 332, 465, 530)),
                                                    (12, (180, 626, 520, 772)),
                                                    (13, (305, 150, 590, 326))],
                               mask=[(305, 165, 322, 270)],
                               solution=True, ref='2022 HL deferred Q4(a)'),
    K + 'scheme-q4cii-sol': dict(doc='scheme', page=14, rect=(110, 72, 372, 250), solution=True,
                                 ref='2022 HL deferred Q4(c)(ii)'),
    K + 'scheme-q5aii-sol': dict(doc='scheme', page=14, rect=(110, 462, 520, 552), solution=True,
                                 ref='2022 HL deferred Q5(a)(ii)'),
    K + 'scheme-q5bi-sol': dict(doc='scheme', page=15, rect=(90, 100, 560, 381), solution=True,
                                ref='2022 HL deferred Q5(b)'),
    # The ratio worked as stacked fractions the text layer flattens.
    K + 'scheme-q5biii-sol': dict(doc='scheme', page=15, rect=(140, 490, 410, 521),
                                  solution=True, ref='2022 HL deferred Q5(b)(iii)'),
    K + 'scheme-q6aii-sol': dict(doc='scheme', page=16, rect=(355, 272, 578, 478),
                                 mask=[(540, 458, 562, 476)], solution=True,
                                 ref='2022 HL deferred Q6(a)(ii)'),
    K + 'scheme-q6bii-sol': dict(doc='scheme', page=16, rect=(355, 552, 572, 755), solution=True,
                                 ref='2022 HL deferred Q6(b)(ii)'),
    K + 'scheme-q6c-sol': dict(doc='scheme', page=17, rect=(358, 330, 560, 540), solution=True,
                               ref='2022 HL deferred Q6(c)'),
    K + 'scheme-q7aii-sol': dict(doc='scheme', page=18, rect=(75, 400, 565, 549), solution=True,
                                 ref='2022 HL deferred Q7(a)(ii)'),
    K + 'scheme-q8aiv-sol': dict(doc='scheme', parts=[(21, (440, 72, 565, 178)),
                                                      (21, (72, 170, 315, 250))],
                                 layout='row', solution=True,
                                 ref='2022 HL deferred Q8(a)(iv)'),
    K + 'scheme-q8av-sol': dict(doc='scheme', page=21, rect=(185, 338, 440, 435), solution=True,
                                ref='2022 HL deferred Q8(a)(v)'),
    K + 'scheme-q8bi-sol': dict(doc='scheme', page=21, rect=(65, 528, 565, 718), solution=True,
                                ref='2022 HL deferred Q8(b)(i)'),
    K + 'scheme-q8c-sol': dict(doc='scheme', parts=[(22, (412, 305, 572, 415)),
                                                    (22, (380, 515, 572, 655))],
                               layout='row', solution=True, ref='2022 HL deferred Q8(c)'),
    K + 'scheme-q9ai-sol': dict(doc='scheme', page=23, rect=(55, 530, 570, 735), solution=True,
                                ref='2022 HL deferred Q9(a)(i)'),
    K + 'scheme-q9aii-sol': dict(doc='scheme', page=24, rect=(255, 88, 560, 315),
                                 mask=[(255, 95, 263, 270), (550, 303, 562, 320)], solution=True,
                                 ref='2022 HL deferred Q9(a)(ii)'),
    K + 'scheme-q9biv-sol': dict(doc='scheme', page=24, rect=(100, 600, 520, 716), solution=True,
                                 ref='2022 HL deferred Q9(b)(iv)'),
    K + 'scheme-q9bv-sol': dict(doc='scheme', page=25, rect=(450, 50, 565, 172), solution=True,
                                ref='2022 HL deferred Q9(b)(v)'),
    K + 'scheme-q9c-sol': dict(doc='scheme', page=25, rect=(75, 322, 560, 510), solution=True,
                               ref='2022 HL deferred Q9(c)'),
    K + 'scheme-q9cor-sol': dict(doc='scheme', page=25, rect=(405, 605, 572, 758),
                                 mask=[(550, 746, 566, 762)], solution=True,
                                 ref='2022 HL deferred Q9(c)(i)'),
}

SPLIT = {
    'eng-2022-hl-deferred-q8-a': 'never shipped: "Answer any three of the following" over '
                                 'five separate questions, each priced at 6; the automatic '
                                 'card ran their answers as options of one list, beside its '
                                 'own cards for (i)-(iii)',
}

FOLDED = {
    'eng-2022-hl-deferred-q4-a-iv': 'never shipped: (iv) is one option of "Select any two '
                                    'from (a)(i), (ii), (iii) or (iv)", carried by the Q4(a) '
                                    'card',
}

CARDS = [
    # ---- Question 1 ("Any ten @ 5 marks each") ------------------------------
    dict(key=(1, 'a', None),
         why='Hawk-Eye is pictured beside (a); scheme p4 bullets three advantages, one '
             'asked, "5".',
         topic='eng-3-14',
         lifted=[[S(4, 100, 121, 560, 139.5), S(4, 100, 139.5, 560, 156),
                  S(4, 100, 156, 560, 174)]],
         row_kind='anyN', group=(1, 5), marks=[5], tariff='fixed', total=5,
         question_figure=K + 'paper-q1a-crop',
         notes="The scheme prints '5'. " + _SA),
    dict(key=(1, 'b', None),
         replaces=NEW + 'dropped the first advantage, "Adhesives provide a sealed waterproof '
                        'joint."',
         why='Scheme p4 lists four advantages, one a line, "3 + 2".',
         topic='eng-2-10',
         lifted=[S(4, 60, 209, 560, 226), S(4, 60, 226, 560, 243), S(4, 60, 243, 560, 260),
                 S(4, 60, 260, 560, 277)],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         notes="The scheme prints '3 + 2'. " + _SA),
    dict(key=(1, 'c', None),
         replaces=NEW + 'gave the process without the scheme\'s drawing of it',
         why='Scheme p4 describes the process in three bullets beside a labelled drawing, '
             'shown with the answer, "5". Its first line runs into the drawing, so it is '
             'lifted apart; the drawing\'s labels are left out of the words.',
         topic='eng-1-2',
         lifted=[join(S(4, 100, 326, 352, 343), S(4, 100, 344, 303, 446))], marks=[5], total=5,
         figure=K + 'scheme-q1c-sol',
         notes="The scheme prints '5'. " + _SA),
    dict(key=(1, 'f', None),
         why='Scheme p5 sets four advantages and four disadvantages in two columns, "3 + 2"; '
             'one of each asked. The answer to each is any one of its column.',
         topic='eng-1-9',
         lifted=[[S(5, 75, 105, 300, 120.5), S(5, 75, 120.5, 300, 135.5),
                  S(5, 75, 135.5, 300, 150.5), S(5, 75, 150.5, 300, 165.5)],
                 [S(5, 320, 105, 560, 120.5), S(5, 320, 120.5, 560, 135.5),
                  S(5, 320, 135.5, 560, 150.5),
                  join(S(5, 320, 150.5, 560, 165.5), S(5, 320, 165.5, 560, 180))]],
         marks=[3, 2], total=5,
         notes="The scheme prints '3 + 2' under its columns of advantages and disadvantages, "
               "read here as 3 for the advantage and 2 for the disadvantage, in the order "
               "asked. " + _SA),
    dict(key=(1, 'g', None),
         why='The headlamp is pictured beside (g); scheme p5 bullets five advantages, '
             '"3 + 2".',
         topic='eng-2-16',
         lifted=[S(5, 100, 245, 560, 278), S(5, 100, 278, 560, 292.5), S(5, 100, 292.5, 560, 308),
                 S(5, 100, 308, 560, 323), S(5, 100, 323, 560, 339)],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         question_figure=K + 'paper-q1g-crop',
         notes="The scheme prints '3 + 2'. " + _SA),
    dict(key=(1, 'h', None),
         why='The headlamp is pictured beside (g), above (h); scheme p5 answers in one '
             'sentence, "5".',
         topic='eng-1-9',
         lifted=[S(5, 60, 372, 560, 388)], marks=[5], total=5,
         question_figure=K + 'paper-q1g-crop',
         notes="The scheme prints '5'. " + _SA),
    dict(key=(1, 'i', None),
         replaces=NEW + 'cut the answer to its last line, "6-12 V."',
         why='The charger is pictured beside (i); scheme p5 answers in one sentence over two '
             'lines, "5".',
         topic='eng-2-16',
         lifted=[S(5, 60, 423, 560, 455)], marks=[5], total=5,
         question_figure=K + 'paper-q1i-crop',
         notes="The scheme prints '5'. " + _SA),
    dict(key=(1, 'k', None),
         why='Scheme p6 describes three defects under their names, "3 + 2".',
         topic='eng-1-3',
         lifted=[S(6, 65, 157, 560, 189), S(6, 65, 190, 560, 240), S(6, 65, 241, 560, 290)],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         notes="The scheme prints '3 + 2'. " + _SA),
    dict(key=(1, 'l', None),
         why='Scheme p6 works the modulus as a stacked fraction the text layer flattens; the '
             'working is shown as printed, "5".',
         topic='eng-3-8',
         special={'kind': 'ask'}, total=5,
         figure=K + 'scheme-q1l-sol',
         notes="The scheme prints '5'. " + _SA),
    dict(key=(1, 'm', None),
         why='The car is pictured beside (m); scheme p6 bullets four advantages and four '
             'disadvantages in two columns, "3 + 2"; one of each asked.',
         topic='eng-3-14',
         lifted=[[S(6, 104, 409, 300, 427), S(6, 104, 427, 300, 444.5),
                  S(6, 104, 444.5, 300, 462), S(6, 104, 462, 300, 479)],
                 [S(6, 330, 409, 560, 427), S(6, 330, 427, 560, 444.5),
                  S(6, 330, 444.5, 560, 462), S(6, 330, 462, 560, 479)]],
         marks=[3, 2], total=5,
         question_figure=K + 'paper-q1m-crop',
         notes="The scheme prints '3 + 2' under its columns of advantages and disadvantages, "
               "read here as 3 for the advantage and 2 for the disadvantage, in the order "
               "asked. " + _SA),
    # ---- Question 2 ("Answer all parts of this question") -------------------
    dict(key=(2, 'a', 'i'),
         checked=_ck(4, '(a)(i)', '(a) Artificial Intelligence came to prominence ...'),
         why='Scheme p6 explains the term in one paragraph under its heading, "5".',
         topic='eng-3-14',
         lifted=[S(6, 104, 599, 560, 698)], marks=[5], total=5,
         notes="The scheme prints '5'."),
    dict(key=(2, 'a', 'ii'),
         replaces=NEW + 'read the scheme\'s "3 + 2" as one question total',
         why='Scheme pp6-7 bullet eight examples, "3 + 2".',
         topic='eng-3-14',
         lifted=[S(6, 126, 731, 560, 748), S(6, 126, 748, 560, 764), S(7, 126, 70, 560, 87.5),
                 S(7, 126, 87.5, 560, 102.5), S(7, 126, 102.5, 560, 118),
                 S(7, 126, 118, 560, 133), S(7, 126, 133, 560, 148), S(7, 126, 148, 560, 164)],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         notes="The scheme prints '3 + 2'."),
    dict(key=(2, 'b', 'i'),
         why='Scheme p7 explains machine learning in a paragraph and three types, under a '
             'diagram of the three terms, shown with the answer; "5". The reader joins the '
             'diagram\'s caption to the ask, so the question is lifted from the page.',
         topic='eng-3-14', stem=False,
         question_lift=P(4, 85, 271, 355, 305, more=[(112, 309, 230, 329)]),
         lifted=[join(S(7, 104, 388, 560, 462), S(7, 120, 462, 560, 579))], marks=[5], total=5,
         figure=K + 'scheme-q2b-sol',
         notes="The scheme prints '5'."),
    dict(key=(2, 'b', 'ii'),
         why='Scheme p7 explains deep learning in one paragraph, "5".',
         topic='eng-3-14', stem=False,
         question_lift=P(4, 85, 271, 355, 305, more=[(112, 329, 210, 351)]),
         lifted=[S(7, 104, 608, 560, 673)], marks=[5], total=5,
         figure=K + 'scheme-q2b-sol',
         notes="The scheme prints '5'."),
    dict(key=(2, 'c', None),
         replaces=NEW + 'took each bullet for an option of its own',
         why='A lead-in over four headings set as romans, "any two"; scheme pp7-8 bullet the '
             'benefits under each heading (the last a paragraph), one option each, "Any two '
             '@ 5 + 5".',
         topic='eng-3-14',
         lifted=[[join(S(7, 104, 709, 300, 724), SB(7, 112, 726, 560, 758),
                       SB(8, 112, 72, 560, 155)),
                  join(S(8, 104, 173, 300, 188), SB(8, 112, 190, 560, 273)),
                  join(S(8, 104, 291, 300, 306), SB(8, 112, 308, 560, 391)),
                  S(8, 104, 409, 560, 542)]],
         row_kind='anyN', group=(2, 5), marks=[10], tariff='fixed', total=10,
         notes="The scheme prints 'Any two @ 5 + 5'."),
    dict(key=(2, 'd', None),
         replaces=NEW + 'split the sensor answer into three options',
         why='A lead-in over three terms set as romans, "any two"; scheme pp8-9 explain each '
             'under its name, the IIoT beside a picture, shown with the answer; one option '
             'each, "Any two @ 5 + 5".',
         topic='eng-2-16',
         lifted=[[S(8, 104, 578, 560, 660),
                  join(S(9, 104, 72, 290, 222), S(9, 104, 224, 560, 240)),
                  S(9, 104, 258, 560, 374)]],
         row_kind='anyN', group=(2, 5), marks=[10], tariff='fixed', total=10,
         figure=K + 'scheme-q2dii-sol',
         notes="The scheme prints 'Any two @ 5 + 5'."),
    # ---- Question 3 ---------------------------------------------------------
    dict(key=(3, 'b', 'i'),
         replaces=NEW + 'ran both tests\' bullets as points of one total where one test is asked',
         why='"Describe one impact test": scheme p10 introduces both tests beside a drawing '
             'of the machine, then bullets the Izod test and the Charpy test, each beside a '
             'drawing, shown with the answer; "10". Each option is the introduction with one '
             'test. The drawings\' labels are left out of the words.',
         topic='eng-3-8',
         lifted=[[join(S(10, 104, 291, 365, 409), S(10, 104, 426, 370, 441),
                       S(10, 128, 443, 372, 509), S(10, 128, 510, 560, 560)),
                  join(S(10, 104, 291, 365, 409), S(10, 104, 576, 300, 592),
                       S(10, 128, 593, 405, 659), S(10, 128, 660, 560, 710))]],
         row_kind='anyN', group=(1, 10), marks=[10], tariff='fixed', total=10,
         figure=K + 'scheme-q3bi-sol',
         notes="The scheme prints '10'."),
    dict(key=(3, 'c', 'i'),
         replaces=NEW + 'gave the test without the scheme\'s drawings of it',
         why='Scheme p11 describes liquid penetrant testing in four steps beside drawings of '
             'them, shown with the answer, "8" for the part not split between them.',
         topic='eng-3-8',
         lifted=[S(11, 104, 188, 455, 232), S(11, 104, 232, 455, 262), S(11, 104, 262, 455, 293),
                 S(11, 104, 295, 455, 344)],
         tariff='questionTotal', total=8,
         figure=K + 'scheme-q3ci-sol',
         notes="The scheme prints '8'."),
    dict(key=(3, 'c', 'ii'),
         why='The casting is pictured beside (ii); scheme p11 describes radiography in one '
             'paragraph over a labelled drawing, shown with the answer, "8". The drawing\'s '
             'labels are left out of the words.',
         topic='eng-3-8',
         lifted=[S(11, 104, 379, 560, 529)], marks=[8], total=8,
         question_figure=K + 'paper-q3cii-crop',
         figure=K + 'scheme-q3cii-sol',
         notes="The scheme prints '8'."),
    # ---- Question 4 ---------------------------------------------------------
    dict(key=(4, 'a', None),
         replaces=NEW + 'took each term of a pair for an option of its own',
         why='"Select any two" of four pairs set as romans; scheme pp12-13 explain each pair, '
             'the pyrometers and the two steels beside drawings, shown with the answer; one '
             'option a pair, "Any two @ 8 + 8". The drawings\' labels are left out of the '
             'words.',
         topic='eng-2-6',
         lifted=[[S(12, 104, 106, 560, 188),
                  join(S(12, 104, 207, 560, 323), S(12, 104, 539, 560, 637.5)),
                  S(13, 104, 72, 560, 150),
                  S(13, 104, 169, 320, 269)]],
         row_kind='anyN', group=(2, 8), marks=[16], tariff='fixed', total=16,
         figure=K + 'scheme-q4a-sol',
         notes="The scheme prints 'Any two @ 8 + 8'."),
    dict(key=(4, 'b', 'i'),
         why='The diagram is drawn with regions A-D; scheme p13 names each after its letter, '
             '"2 + 2 + 2 + 2".',
         topic='eng-1-3',
         lifted=[S(13, 104, 364, 300, 380), S(13, 104, 380, 300, 397), S(13, 104, 397, 300, 414),
                 S(13, 104, 414, 300, 431)],
         marks=[2, 2, 2, 2], total=8,
         labels={'A': S(13, 124, 364, 300, 380), 'B': S(13, 121, 380, 300, 397),
                 'C': S(13, 123, 397, 300, 414), 'D': S(13, 124, 414, 300, 431)},
         question_figure=K + 'paper-q4b-crop',
         notes="The scheme prints '2 + 2 + 2 + 2', for A, B, C and D in that order."),
    dict(key=(4, 'b', 'ii'),
         replaces=NEW + 'priced X and Y as one total where the scheme prints "4 + 4", without '
                        'the diagram they are read off',
         why='The points X and Y are marked on the diagram; scheme p13 explains each after '
             'its letter, "4 + 4".',
         topic='eng-1-3',
         lifted=[S(13, 104, 465, 560, 497), S(13, 104, 499, 560, 531)], marks=[4, 4], total=8,
         question_figure=K + 'paper-q4b-crop',
         notes="The scheme prints '4 + 4', for X and Y in that order."),
    dict(key=(4, 'c', 'i'),
         replaces=NEW + 'asked about "the machined surfaces" without the crankshaft that shows '
                        'them',
         why='The crankshaft is pictured beside (c); scheme p13 answers in one sentence, "6".',
         topic='eng-2-6',
         lifted=[S(13, 104, 566, 540, 582)], marks=[6], total=6,
         question_figure=K + 'paper-q4c-crop',
         notes="The scheme prints '6'."),
    dict(key=(4, 'c', 'ii'),
         replaces=NEW + 'gave the process without the drawing the part asks for',
         why='Scheme pp13-14 describe induction hardening in three paragraphs over a labelled '
             'drawing, shown with the answer, "12" for the part not split between them.',
         topic='eng-2-6',
         lifted=[S(13, 104, 634, 560, 682), S(13, 104, 684, 560, 716), S(13, 104, 718, 560, 750)],
         tariff='questionTotal', total=12,
         question_figure=K + 'paper-q4c-crop',
         figure=K + 'scheme-q4cii-sol',
         notes="The scheme prints '12'."),
    # ---- Question 5 ---------------------------------------------------------
    dict(key=(5, 'a', 'i'),
         why='One of "Answer any two of the following": scheme p14 answers in one sentence.',
         topic='eng-2-13',
         lifted=[S(14, 104, 365, 560, 396)], marks=[8], total=8, notes=_A5),
    dict(key=(5, 'a', 'ii'),
         why='One of "Answer any two of the following": scheme p14 answers in one sentence '
             'over drawings of the two curves, shown with the answer. The drawings\' labels '
             'are left out of the words.',
         topic='eng-1-3',
         lifted=[S(14, 104, 415, 560, 447)], marks=[8], total=8,
         figure=K + 'scheme-q5aii-sol', notes=_A5),
    dict(key=(5, 'b', 'i'),
         checked=_ck(7, '(b)(i)', 'Using the graph paper supplied:'),
         why='"Draw the equilibrium diagram": scheme p15 answers with the drawn diagram, '
             'shown with the answer, "10". The reader flattens the table into the stem, so '
             'the question is lifted from the page with the table shown.',
         topic='eng-1-3', stem=False,
         question_lift=P(7, *_B5, more=[_B5U, (116, 445, 420, 461)]),
         special={'kind': 'ask'}, total=10,
         question_figure=K + 'paper-q5b-crop',
         figure=K + 'scheme-q5bi-sol',
         notes="The scheme prints '10'."),
    dict(key=(5, 'b', 'ii'),
         checked=_ck(7, '(b)(ii)', 'Using the graph paper supplied:'),
         why='Scheme p15 reads the points A and C off the diagram it draws, shown with the '
             'answer, "4" for the part not split between them.',
         topic='eng-1-3', stem=False,
         question_lift=P(7, *_B5, more=[_B5U, (116, 472, 555, 488)]),
         lifted=[S(15, 175, 425, 350, 440.5), S(15, 175, 440.5, 350, 457)],
         tariff='questionTotal', total=4,
         question_figure=K + 'paper-q5b-crop',
         figure=K + 'scheme-q5bi-sol',
         notes="The scheme prints '4'."),
    dict(key=(5, 'b', 'iii'),
         replaces=NEW + 'read the stacked fractions as one line of numbers',
         why='Scheme p15 works the ratio as stacked fractions the text layer flattens; the '
             'working is shown as printed, "4".',
         topic='eng-1-3', stem=False,
         question_lift=P(7, *_B5, more=[_B5U, (116, 497, 392, 513)]),
         special={'kind': 'ask'}, total=4,
         question_figure=K + 'paper-q5b-crop',
         figure=K + 'scheme-q5biii-sol',
         notes="The scheme prints '4'."),
    dict(key=(5, 'c', 'i'),
         why='The three defects are drawn at A, B and C; scheme p15 names and explains each '
             'after its letter, one option each, "Any two @ 4 + 4".',
         topic='eng-1-3',
         lifted=[[S(15, 104, 551, 560, 600), S(15, 104, 602, 560, 650), S(15, 104, 652, 560, 701)]],
         row_kind='anyN', group=(2, 4), marks=[8], tariff='fixed', total=8,
         labels={'A': S(15, 122, 551, 300, 567), 'B': S(15, 122, 602, 300, 618),
                 'C': S(15, 121, 652, 300, 668)},
         question_figure=K + 'paper-q5c-crop',
         notes="The scheme prints 'Any two @ 4 + 4'."),
    # ---- Question 6 ---------------------------------------------------------
    dict(key=(6, 'a', 'i'),
         replaces=NEW + 'asked about "the tubular mild steel structure" without the stadium '
                        'that shows it',
         why='The stadium is pictured beside (a); scheme p16 answers in one paragraph, "6".',
         topic='eng-2-10',
         lifted=[S(16, 104, 207, 560, 256)], marks=[6], total=6,
         question_figure=K + 'paper-q6a-crop',
         notes="The scheme prints '6'."),
    dict(key=(6, 'a', 'ii'),
         replaces=NEW + 'gave the process without the drawing the part asks for',
         why='Scheme p16 names the process and describes it beside a labelled drawing, shown '
             'with the answer, "10". The drawing\'s labels are left out of the words.',
         topic='eng-2-10',
         lifted=[S(16, 104, 275, 350, 424)], marks=[10], total=10,
         question_figure=K + 'paper-q6a-crop',
         figure=K + 'scheme-q6aii-sol',
         notes="The scheme prints '10'."),
    dict(key=(6, 'b', 'ii'),
         replaces=NEW + 'gave the process without the scheme\'s drawing of it',
         why='One of "Answer any three of the following": scheme pp16-17 describe the '
             'electrode, the procedure and the applications beside a labelled drawing, shown '
             'with the answer. The drawing\'s labels are left out of the words.',
         topic='eng-2-10',
         lifted=[join(S(16, 104, 578, 350, 744), S(17, 104, 72, 560, 121))], marks=[6], total=6,
         figure=K + 'scheme-q6bii-sol', notes=_A6),
    dict(key=(6, 'b', 'iv'),
         replaces=NEW + 'dropped the first method, "Formation of slag coat on cooling weld."',
         why='One of "Answer any three of the following": scheme p17 gives seven methods, one '
             'a line, the 6 for the part not split between them.',
         topic='eng-2-10',
         lifted=[S(17, 104, 167, 560, 183), S(17, 104, 183, 560, 198), S(17, 104, 198, 560, 215),
                 S(17, 104, 215, 560, 245), S(17, 104, 245, 560, 259), S(17, 104, 259, 560, 274),
                 S(17, 104, 274, 560, 289)],
         tariff='questionTotal', total=6, notes=_A6),
    dict(key=(6, 'c', None),
         why='Paper p8 sets two alternative (c)s either side of an OR. This card is the '
             'first: submerged arc welding with reference to four bullets; scheme p17 answers '
             'under the same four headings beside a labelled drawing, shown with the answer; '
             '"16". The drawing\'s labels are left out of the words.',
         topic='eng-2-10', stem=False,
         question_lift=P(8, 85, 456, 525, 487, items=[(115, 496, 240, 512), (115, 511, 240, 527),
                                                      (115, 526, 240, 542), (115, 541, 240, 558)]),
         lifted=[join(S(17, 104, 322, 365, 586), S(17, 104, 586, 560, 615))], marks=[16],
         total=16,
         figure=K + 'scheme-q6c-sol',
         notes="The scheme prints '16'. " + _OR6),
    dict(key=(6, 'c', 'i'),
         replaces=NEW + 'set the advantages as one row under "4 + 4"',
         why='The OR branch\'s (i), the robot pictured beside it: scheme p17 lists the '
             'advantages in one sentence, each lifted by its own word rectangle, "4 + 4".',
         topic='eng-2-16',
         lifted=[S(17, 104, 682.5, 550, 698), S(17, 104, 699.5, 224.5, 715),
                 S(17, 224.5, 699.5, 500.5, 715),
                 join(S(17, 500.5, 699.5, 545, 715), S(17, 104, 716.5, 298, 732)),
                 S(17, 298, 716.5, 464.5, 732),
                 join(S(17, 464.5, 716.5, 550, 732), S(17, 104, 733.5, 200, 749))],
         tariff='orderedSplit', notation='4 + 4', ladder=8, total=8,
         question_figure=K + 'paper-q6cor-crop',
         notes="The scheme prints '4 + 4'. " + _OR6),
    dict(key=(6, 'c', 'ii'),
         replaces=NEW + 'ran the second and third reasons into one row',
         why='The OR branch\'s (ii): scheme p18 gives three reasons, one a line, "4 + 4".',
         topic='eng-2-10',
         lifted=[S(18, 104, 72, 560, 88), S(18, 104, 89, 560, 105), S(18, 104, 106, 560, 139)],
         tariff='orderedSplit', notation='4 + 4', ladder=8, total=8,
         question_figure=K + 'paper-q6cor-crop',
         notes="The scheme prints '4 + 4'. " + _OR6),
    # ---- Question 7 ---------------------------------------------------------
    dict(key=(7, 'a', 'i'),
         replaces=NEW + 'set the properties as one row under "4 + 4"',
         why='The bumper is pictured beside (a); scheme p18 lists the properties in one '
             'sentence over four lines, each lifted by its own word rectangle, "4 + 4".',
         topic='eng-1-9',
         lifted=[S(18, 104, 217, 477.5, 233),
                 join(S(18, 477.5, 217, 560, 233), S(18, 104, 234.5, 426.5, 250)),
                 join(S(18, 426.5, 234.5, 530, 250), S(18, 104, 251.5, 239.5, 267)),
                 S(18, 239.5, 251.5, 397, 267),
                 join(S(18, 397, 251.5, 550, 267), S(18, 104, 268.5, 156.5, 284)),
                 S(18, 156.5, 268.5, 400.5, 284), S(18, 400.5, 268.5, 505, 284)],
         tariff='orderedSplit', notation='4 + 4', ladder=8, total=8,
         question_figure=K + 'paper-q7a-crop',
         notes="The scheme prints '4 + 4'."),
    dict(key=(7, 'a', 'ii'),
         why='Scheme p18 names the process and bullets its steps over a labelled drawing of '
             'the machine, shown with the answer, "8". The drawing\'s labels are left out of '
             'the words.',
         topic='eng-1-9',
         lifted=[join(S(18, 104, 301, 560, 316), S(18, 135, 316, 560, 386))], marks=[8], total=8,
         question_figure=K + 'paper-q7a-crop',
         figure=K + 'scheme-q7aii-sol',
         notes="The scheme prints '8'."),
    dict(key=(7, 'b', None),
         replaces=NEW + 'took each example of a copolymer, and each sentence of rapid '
                        'prototyping, for an option of its own',
         why='A lead-in over five terms set as romans, "any three"; scheme pp18-19 explain '
             'each under its name, one option each, "Any three @ 6 + 6 + 6".',
         topic='eng-1-9',
         lifted=[[join(S(18, 104, 598, 560, 630), S(18, 135, 630, 560, 718)),
                  S(19, 104, 72, 560, 121), S(19, 104, 140, 560, 222),
                  S(19, 104, 240, 560, 289), S(19, 104, 307, 560, 339)]],
         row_kind='anyN', group=(3, 6), marks=[18], tariff='fixed', total=18,
         notes="The scheme prints 'Any three @ 6 + 6 + 6'."),
    dict(key=(7, 'c', 'i'),
         replaces=NEW + 'opened mid-answer, the elastomer\'s heading dropped, and split its '
                        'lists of properties',
         why='The socket and the exercise band are pictured beside (c); scheme p19 describes '
             'the elastomer and the thermoset in turn under their names, "8" for the part '
             'not split between them.',
         topic='eng-1-9',
         lifted=[S(19, 104, 375, 560, 568), S(19, 104, 568, 560, 748)],
         tariff='questionTotal', total=8,
         question_figure=K + 'paper-q7c-crop',
         notes="The scheme prints '8'."),
    # ---- Question 8 ---------------------------------------------------------
    dict(key=(8, 'a', 'iv'),
         replaces=NEW + 'ran (v)\'s answer on the fits into this part\'s',
         why='One of "Answer any three of the following": scheme p21 explains eccentric '
             'turning beside labelled drawings, shown with the answer. The drawings\' labels '
             'are left out of the words.',
         topic='eng-2-11',
         lifted=[join(S(21, 104, 89, 450, 155), S(21, 315, 173, 560, 239))], marks=[6], total=6,
         figure=K + 'scheme-q8aiv-sol', notes=_A8),
    dict(key=(8, 'a', 'v'),
         why='One of "Answer any three of the following": scheme p21 describes each fit in '
             'turn over a drawing of both, shown with the answer. The scheme numbers the part '
             '"(iv)"; it is (v) on the paper. The reader joins "Answer any three of the '
             'following:" to the ask, so it is lifted from the page.',
         topic='eng-3-12',
         question_lift=P(10, 112, 234, 440, 264),
         lifted=[S(21, 65, 292, 560, 357)], marks=[6], total=6,
         figure=K + 'scheme-q8av-sol', notes=_A8),
    dict(key=(8, 'b', 'i'),
         replaces=NEW + 'gave the process without the engine block or the drawing the part '
                        'asks for',
         why='The engine block is pictured with surface X beside (b); scheme pp21-22 name the '
             'process and describe it either side of a labelled drawing, shown with the '
             'answer; "12" for the part not split between them.',
         topic='eng-2-11',
         lifted=[S(21, 104, 479, 560, 511), S(22, 104, 72, 560, 172)],
         tariff='questionTotal', total=12,
         question_figure=K + 'paper-q8b-crop',
         figure=K + 'scheme-q8bi-sol',
         notes="The scheme prints '12'."),
    dict(key=(8, 'b', 'ii'),
         replaces=NEW + 'set the precautions as one row under "2 + 2"',
         why='Scheme p22 lists the precautions in one sentence after "Safety:", each lifted '
             'by its own word rectangle, "2 + 2".',
         topic='eng-3-1',
         lifted=[S(22, 143, 207, 410.5, 223),
                 join(S(22, 410.5, 207, 550, 223), S(22, 104, 224.5, 288.5, 240)),
                 join(S(22, 288.5, 224.5, 562, 240), S(22, 104, 241.5, 190.5, 257)),
                 S(22, 190.5, 241.5, 298, 257), S(22, 298, 241.5, 535, 257)],
         tariff='orderedSplit', notation='2 + 2', ladder=4, total=4,
         question_figure=K + 'paper-q8b-crop',
         notes="The scheme prints '2 + 2'."),
    dict(key=(8, 'c', None),
         why='Paper p10 sets two alternative (c)s either side of an OR. This card is the '
             'first, which asks for each of the magnetic chuck and up-cut milling: scheme p22 '
             'describes each under its name beside a labelled drawing, shown with the answer; '
             '"8" each. The drawings\' labels are left out of the words.',
         topic='eng-2-11', stem=False,
         question_lift=P(10, 88, 458, 425, 489, items=[(95, 495, 215, 511), (95, 511, 210, 527)]),
         lifted=[join(S(22, 104, 291, 412, 424), S(22, 104, 424, 560, 497)),
                 S(22, 104, 530, 375, 629)],
         marks=[8, 8], total=16,
         figure=K + 'scheme-q8c-sol',
         notes="The scheme prints '8' under each, for (i) and (ii) in that order. " + _OR8),
    dict(key=(8, 'c', 'i'),
         replaces=NEW + 'ran the first branch\'s magnetic chuck answer and this branch\'s answer into one question total',
         why='The OR branch\'s (i), a CNC part pictured beside it: scheme pp22-23 bullet seven '
             'advantages, "4 + 4".',
         topic='eng-2-11', stem=False,
         question_lift=P(10, *_C8B, more=[(113, 600, 370, 631)]),
         lifted=[S(22, 120, 724, 560, 740), S(23, 120, 72, 560, 105), S(23, 120, 106, 560, 121),
                 S(23, 120, 123, 560, 138), S(23, 120, 140, 560, 155), S(23, 120, 157, 560, 188),
                 S(23, 120, 190, 560, 205)],
         tariff='orderedSplit', notation='4 + 4', ladder=8, total=8,
         question_figure=K + 'paper-q8cor-crop',
         notes="The scheme prints '4 + 4'. " + _OR8),
    dict(key=(8, 'c', 'ii'),
         replaces=NEW + 'ran the first branch\'s up-cut milling answer and this branch\'s '
                        'answer into one question total',
         why='The OR branch\'s (ii): scheme p23 explains simulation, then its benefit for the '
             'environment and for quality, a paragraph each, "4 + 4".',
         topic='eng-2-11', stem=False,
         question_lift=P(10, *_C8B, more=[(113, 644, 385, 660)],
                         items=[(133, 666, 215, 683), (133, 684, 230, 700)]),
         lifted=[S(23, 104, 300, 560, 344), S(23, 104, 344, 560, 402)], marks=[4, 4], total=8,
         question_figure=K + 'paper-q8cor-crop',
         notes="The scheme prints '4 + 4', for the environment and quality control in that "
               "order, and opens: '" + S(23, 104, 241, 560, 300) + "' " + _OR8),
    # ---- Question 9 ---------------------------------------------------------
    dict(key=(9, 'a', 'i'),
         why='The forklift is pictured with its X and Y directions; scheme p23 suggests a '
             'mechanism in one sentence over a labelled drawing, shown with the answer; the '
             'marks grid prices (a)(i) at 8. The drawing\'s labels are left out of the words.',
         topic='eng-2-15',
         lifted=[S(23, 104, 486, 560, 530)], marks=[8], total=8,
         question_figure=K + 'paper-q9a-crop',
         figure=K + 'scheme-q9ai-sol',
         notes="The scheme's marks grid prints '(a) (i) 8'; under the drawing it prints "
               "'8 8'."),
    dict(key=(9, 'a', 'ii'),
         why='Scheme p24 suggests a mechanism in a paragraph beside a labelled drawing, shown '
             'with the answer, "8". The drawing\'s labels are left out of the words.',
         topic='eng-2-15',
         lifted=[S(24, 104, 87, 340, 263)], marks=[8], total=8,
         question_figure=K + 'paper-q9a-crop',
         figure=K + 'scheme-q9aii-sol',
         notes="The scheme prints '8'. Its second sentence reads 'The fulcrum at the base of "
               "the will allow', a word missing as printed."),
    dict(key=(9, 'b', 'iv'),
         why='One of "Answer any three of the following": scheme p24 explains the switch over '
             'drawings of it open and closed, shown with the answer.',
         topic='eng-2-16',
         lifted=[S(24, 104, 541, 560, 590)], marks=[6], total=6,
         figure=K + 'scheme-q9biv-sol', notes=_A9),
    dict(key=(9, 'b', 'v'),
         why='One of "Answer any three of the following": scheme p25 explains the worm drive '
             'beside a labelled drawing, shown with the answer. The drawing\'s labels are '
             'left out of the words.',
         topic='eng-2-15',
         lifted=[S(25, 104, 72, 450, 138)], marks=[6], total=6,
         figure=K + 'scheme-q9bv-sol', notes=_A9),
    dict(key=(9, 'c', None),
         why='Paper p11 sets two alternative (c)s either side of an OR. This card is the '
             'first, the turntable pictured beside it: scheme p25 suggests a pin gear drive '
             'and stabilising wheels, a paragraph each either side of a labelled drawing, '
             'shown with the answer; "8 + 8". The drawing\'s labels are left out of the '
             'words.',
         topic='eng-2-15', stem=False,
         question_lift=P(11, 85, 478, 395, 538, items=[(95, 546, 250, 562), (95, 568, 240, 584)]),
         lifted=[S(25, 104, 285, 560, 317), S(25, 104, 521, 560, 569)], marks=[8, 8], total=16,
         question_figure=K + 'paper-q9c-crop',
         figure=K + 'scheme-q9c-sol',
         notes="The scheme prints '8 + 8', for (i) and (ii) in that order, and opens: '"
               + S(25, 104, 222, 560, 251) + "' " + _OR9),
    dict(key=(9, 'c', 'i'),
         replaces=NEW + 'ran the first branch\'s turntable answer and this branch\'s relay answer into one question total',
         why='The OR branch\'s (i), the relay pictured beside it: scheme pp25-26 explain its '
             'principle beside a labelled drawing, shown with the answer, "8". The drawing\'s '
             'labels are left out of the words.',
         topic='eng-2-16', stem=False,
         question_lift=P(11, *_C9B, more=[(113, 695, 430, 711)]),
         lifted=[join(S(25, 104, 639, 375, 741), S(26, 104, 72, 560, 102))], marks=[8], total=8,
         question_figure=K + 'paper-q9cor-crop',
         figure=K + 'scheme-q9cor-sol',
         notes="The scheme prints '8'. " + _OR9),
    dict(key=(9, 'c', 'ii'),
         replaces=NEW + 'ran the first branch\'s "(ii) Support and stability." and this '
                        'branch\'s ask into one question, its rows one total',
         why='The OR branch\'s (ii): scheme p26 bullets five advantages, "4 + 4".',
         topic='eng-2-16', stem=False,
         question_lift=P(11, *_C9B, more=[(113, 720, 430, 750)]),
         lifted=[S(26, 120, 117, 560, 134), S(26, 120, 134, 560, 151), S(26, 120, 151, 560, 168),
                 S(26, 120, 168, 560, 185), S(26, 120, 185, 560, 201)],
         tariff='orderedSplit', notation='4 + 4', ladder=8, total=8,
         question_figure=K + 'paper-q9cor-crop',
         notes="The scheme prints '4 + 4'. " + _OR9),
]

TOPICS = {
    'eng-2022-hl-deferred-q3-b-ii': ('eng-3-8', 'elastic against plastic deformation in metals, the '
                                                'behaviour a tensile test measures, as the rest of '
                                                'Q3 is filed; "plastic" filed it under plastics'),
}

# The Topic Atlas topic of each card the reference's headings do not settle
# (eng_atlas.py). The reference heads no part of this paper's Q2 or Q7: their
# cards are filed as June 2022's same questions are.
_AI = ('Artificial intelligence and smart manufacturing (the 2022 Higher special '
       'topic, set again in the deferred sitting), which the reference files June\'s '
       'Q2 under and heads no part of this paper\'s Q2; the card\'s syllabus heading '
       'is Technology, or Control technology and electronics.')
_POLY = ('Polymers: the bumper\'s polymer and its moulding, copolymers, parisons, '
         '3-D printing, fillers and stabilisers, thermosets against elastomers. The '
         'reference files June 2022\'s polymers question (Q7) under Polymers and heads '
         'no part of this paper\'s Q7.')

ATLAS = {
    'eng-2022-hl-deferred-q1-b': dict(
        topics=['Materials: Properties and Uses'],
        note='Adhesive bonding of windscreens and glass panels, which the reference '
             'files Q1(b) under; the card\'s syllabus heading is Joining of '
             'materials, where adhesives sit.'),
    **{f'eng-2022-hl-deferred-q2-{p}': dict(topics=['Energy, Electronics & Robotics'], note=_AI)
       for p in ('a-i', 'a-ii', 'b-i', 'b-ii', 'c', 'd', 'e')},
    'eng-2022-hl-deferred-q3-b-ii': dict(
        topics=['Testing of Materials and Products'],
        note='Elastic against plastic deformation in metals, the behaviour a tensile '
             'test measures, in the testing question the reference files whole under '
             'Testing of Materials and Products.'),
    'eng-2022-hl-deferred-q5-a-i': dict(
        topics=['Heat Treatment'],
        note='Strengthening sheet metal. The reference files Q5(a) under Corrosion of '
             'Metals ((iii), sacrificial protection), The Structure of Materials ((ii) '
             'and (iv)) and Heat Treatment, which is left to (i); the scheme answers '
             'with profiling (corrugating, folding, ribbing), and the card\'s syllabus '
             'heading is Manufacturing processes, which no outgoing-course topic covers.'),
    'eng-2022-hl-deferred-q5-c-ii': dict(
        topics=['The Structure of Materials'],
        note='Grain boundaries are crystal structure; the reference files Q5(a) and '
             '(b) under The Structure of Materials and heads no part (c). The card\'s '
             'syllabus heading is Materials testing (ductility).'),
    'eng-2022-hl-deferred-q6-c-i': dict(
        topics=['Energy, Electronics & Robotics'],
        note='Servo against DC motors in robotic control systems: the second (c), '
             'which the reference does not head (it files Q6(a), (b) and the first '
             '(c) under Welding). Energy, Electronics & Robotics, where it files the '
             'second (c) of Q8 and Q9, covers the card\'s syllabus heading, Control '
             'technology and electronics.'),
    **{f'eng-2022-hl-deferred-q7-{p}': dict(topics=['Polymers'], note=_POLY)
       for p in ('a-i', 'a-ii', 'b', 'c-i')},
    'eng-2022-hl-deferred-q7-c-ii': dict(
        topics=['Polymers', 'The Structure of Materials'],
        note='Crystalline against amorphous polymers: polymer structure, filed as '
             'June 2022\'s Q1(b) (amorphous against crystalline structures) is, under '
             'Polymers and The Structure of Materials; the card\'s syllabus heading is '
             'Structure of metals. ' + _POLY),
    'eng-2022-hl-deferred-q8-b-ii': dict(
        topics=['Health and Safety'],
        note='Safety precautions for surface grinding are machine safety; Q8 is '
             'otherwise filed under machining (as June 2022\'s Q8(b)(ii) and (v)).'),
}
