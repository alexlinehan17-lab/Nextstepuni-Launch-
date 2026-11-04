#!/usr/bin/env python3
"""What was measured by eye on a rendered page, for Technology's crops.

Two kinds of rectangle live here, both in PDF points on the page they name,
each measured on a render of that page and then cut at 150 dpi and looked at
before it was written down:

  BY_EYE     the picture a PAPER ask points at, where tech_figures.py's own
             geometry found nothing or cut the wrong thing. 2026 Higher sets
             its circuit INSIDE the ruled answer box the cropper refuses, its
             lever is two arrows and a line that fail every ink test, and the
             op-amp's wires reach past the triangle the cropper found.
  SOLUTIONS  the SCHEME's own drawn answer -- a flowchart, a control chart, a
             comparator circuit, a cam -- cut from the marking scheme page and
             published as a solution figure, which the session screen holds
             back until the student has committed to an answer. This is the
             rule Chemistry used for its dot-and-cross diagrams
             (chem_figures.py): where the examiner answers with a picture, the
             card shows the examiner's picture.

LABEL_ZONES are scheme regions that are a drawing's labels and nothing else,
published or not. The 2026 Higher scheme sets its lever diagram beside its
worked calculation and the text layer reads the two as one row -- "Effort =
50 N Fulcrum" -- so a marking point that ENDS in words printed inside such a
zone is the point with the drawing's labels welded on, and the labels come
off. Only a trailing run comes off, never a word the scheme closes with
punctuation: "...fed into the barrel from the hopper." ends in a label's word
and is a sentence. A line made of nothing but a zone's words is the drawing's
own lettering ("plastic granules hopper heaters mould cavity casing mould")
and is not a marking point at all; the crop carries it.

Nothing here is typed into a card. A rectangle selects what the SEC printed;
the REVIEWED alt text in tech_figures.py says what was seen.
"""
import os
import re

import pymupdf

DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(DIR)))
PAPERS = os.path.join(ROOT, 'examiner-reports', 'technology', 'papers')
SCHEMES = os.path.join(ROOT, 'examiner-reports', 'technology', 'schemes')

PAPER_KEY = re.compile(r'technology-(\d{4})-(HL|OL)-paper-sec([ABC])-q(\d{1,2})'
                       r'([a-d])?(?:-(i{1,3}|iv|v))?-art')
SOLUTION_KEY = re.compile(r'technology-(\d{4})-(HL|OL)-scheme-sec([ABC])-q(\d{1,2})'
                          r'([a-d])?(?:-(i{1,3}|iv|v))?')


def parse_key(key):
    """(year, level, section, q, letter, roman) for either kind of key."""
    m = PAPER_KEY.fullmatch(key) or SOLUTION_KEY.fullmatch(key)
    if not m:
        return None
    return (int(m.group(1)), m.group(2).lower(), m.group(3), int(m.group(4)),
            m.group(5), m.group(6))


def paper_path(year, level, booklet):
    return os.path.join(PAPERS, f'{year}-{level}-{booklet}-paper.pdf')


def scheme_path(year, level):
    return os.path.join(SCHEMES, f'{year}-{level}.pdf')


# PAPER crops: key -> (booklet, page index, rect). Pages are 0-based.
BY_EYE = {
    # Section A booklet (014). The circuit is printed inside the ruled
    # "Calculation:" box, which is_answer_box() rightly refuses as a whole.
    'technology-2026-HL-paper-secA-q3-art': ('014', 2, (56, 616, 244, 744)),
    # The drill: the cropper's own crop, kept because it was looked at.
    'technology-2026-HL-paper-secA-q8-art': ('014', 4, (74.9, 368.4, 537.4, 738.4)),
    # The lever: arrows, a line, two labels -- too little ink for artwork().
    'technology-2026-HL-paper-secA-q9-art': ('014', 5, (348, 272, 558, 382)),
    # The jigsaw: the cropper's rect reached the answer box's ruled edge.
    'technology-2026-HL-paper-secA-q10-art': ('014', 5, (396, 460, 554, 602)),
    # The fishbone diagram, printed full-width above the answer boxes.
    'technology-2026-HL-paper-secA-q11-art': ('014', 6, (118, 148, 542, 402)),
    # The automaton photograph and the dotted drawing box with its centre dot,
    # which the ask names ("In the box below ... The black dot represents").
    'technology-2026-HL-paper-secA-q13-art': ('014', 7, (82.5, 132.0, 555.8, 357.1)),
    # The climbing arch, printed inside the full-page drawing box.
    'technology-2026-HL-paper-secA-q15-art': ('014', 8, (344, 94, 546, 254)),
    # Sections B and C booklet (039). The op-amp with its rails and inputs;
    # the cropper found the triangle alone.
    'technology-2026-HL-paper-secC-q2b-art': ('039', 4, (396, 288, 534, 422)),
    # The defects table 4(b)'s three parts calculate from.
    'technology-2026-HL-paper-secC-q4b-art': ('039', 6, (70, 428, 550, 507)),
    # The gardening tool with its "Safety guard" label and inset.
    'technology-2026-HL-paper-secC-q5b-art': ('039', 8, (70, 220, 244, 424)),
    # The three modular heads; the cropper found the bottom one alone.
    'technology-2026-HL-paper-secC-q5c-art': ('039', 8, (420, 434, 552, 572)),
    # In-window parts whose cards shipped without the picture their stem
    # names ("The prototype circuit shown..."), found once the stem was read
    # in full. Circuits of thin wire fail the cropper's ink tests.
    'technology-2021-HL-paper-secB-q3b-art': ('039', 2, (372, 255, 562, 414)),
    'technology-2021-HL-paper-secC-q2b-art': ('039', 4, (358, 224, 548, 382)),
    'technology-2021-HL-paper-secC-q4c-art': ('039', 7, (106, 132, 478, 316)),
    'technology-2021-OL-paper-secC-q2b-art': ('039', 4, (349, 204, 562, 408)),
    'technology-2023-HL-paper-secC-q4d-art': ('039', 7, (118, 368, 482, 542)),
    'technology-2024-OL-paper-secC-q2b-art': ('039', 4, (338, 230, 556, 370)),
    # 2026 Ordinary. The cropper's own cuts for Q1, Q3 and Q11 took both
    # asks and their answer boxes; these are the pictures alone.
    'technology-2026-OL-paper-secA-q1-art': ('014', 2, (452, 132, 546, 318)),
    'technology-2026-OL-paper-secA-q3-art': ('014', 2, (428, 596, 546, 694)),
    'technology-2026-OL-paper-secA-q4-art': ('014', 3, (82, 92, 244, 254)),
    # The lever diagram only (ii) asks about; (i) names the see-saw.
    'technology-2026-OL-paper-secA-q6-ii-art': ('014', 3, (78, 618, 262, 734)),
    # The cropper's own cut, kept here so the stem loses "Switch A".
    'technology-2026-OL-paper-secA-q9-art': ('014', 4, (357.7, 595.3, 546.4, 732.8)),
    'technology-2026-OL-paper-secA-q11-art': ('014', 5, (62, 298, 174, 446)),
    'technology-2026-OL-paper-secB-q2b-art': ('039', 1, (496, 262, 552, 386)),
    # 2020 Higher (the paper boxes each short question; pictures sit inside).
    'technology-2020-HL-paper-secA-q13-art': ('014', 5, (112, 490, 292, 740)),
    # The lamp photograph for 2(b); its roller-and-groove inset, which (ii) asks
    # about, sits over the prose column and is cut at its left edge for (ii).
    'technology-2020-HL-paper-secB-q2b-art': ('039', 1, (402, 282, 548, 478)),
    'technology-2020-HL-paper-secB-q2b-ii-art': ('039', 1, (348, 326, 402, 404)),
    'technology-2020-HL-paper-secB-q3b-art': ('039', 2, (395, 245, 562, 372)),
    'technology-2020-HL-paper-secB-q3c-art': ('039', 2, (495, 436, 548, 565)),
    'technology-2020-HL-paper-secC-q1d-art': ('039', 3, (395, 655, 562, 762)),
    # 2(b)'s op-amp circuit for (i) and (ii); the surface-mount IC photograph
    # is (iii)'s alone.
    'technology-2020-HL-paper-secC-q2b-art': ('039', 4, (372, 226, 562, 375)),
    'technology-2020-HL-paper-secC-q2b-iii-art': ('039', 4, (92, 371, 160, 422)),
    'technology-2020-HL-paper-secC-q2d-art': ('039', 4, (325, 664, 562, 782)),
}

# In-window parts measured by the residue authors (2026-10-28), one agent per
# year, each crop rendered and looked at before its rect was written.
BY_EYE.update({
    # The whole 555 circuit 2(b)(i) asks the student to redraw; the cropper's
    # cut held the chip alone.
    'technology-2024-HL-paper-secC-q2b-art': ('039', 4, (372, 251, 561, 363)),
    'technology-2021-HL-paper-secA-q11-art': ('014', 4, (310, 486, 563, 645)),
    'technology-2021-HL-paper-secA-q12-art': ('014', 5, (70, 121.5, 504, 287)),
    'technology-2021-HL-paper-secA-q6-art': ('014', 2, (409, 614, 531, 753)),
    'technology-2021-HL-paper-secA-q8-art': ('014', 3, (384, 355, 554, 528)),
    'technology-2021-HL-paper-secC-q1b-art': ('039', 3, (420, 183, 556, 461)),
    'technology-2021-HL-paper-secC-q1d-art': ('039', 3, (447, 650, 553, 781)),
    'technology-2021-HL-paper-secC-q3c-art': ('039', 5, (387.8, 406, 558, 586)),
    'technology-2021-OL-paper-secA-q11-i-art': ('014', 4, (412, 297.5, 524, 409)),
    'technology-2021-OL-paper-secA-q11-ii-art': ('014', 4, (376, 440, 522, 528)),
    'technology-2021-OL-paper-secA-q12-art': ('014', 4, (170, 580, 422, 770.5)),
    'technology-2021-OL-paper-secA-q5-art': ('014', 2, (62, 339.8, 180, 453)),
    'technology-2021-OL-paper-secA-q7-art': ('014', 3, (145, 141.8, 256, 284.5)),
    'technology-2021-OL-paper-secC-q1b-art': ('039', 3, (382, 237, 462.2, 351)),
    'technology-2021-OL-paper-secC-q1c-art': ('039', 3, (377.8, 436, 560, 569.5)),
    'technology-2021-OL-paper-secC-q4d-art': ('039', 6, (476, 704, 573, 788)),
    'technology-2021-OL-paper-secC-q5a-art': ('039', 7, (133, 202, 508, 293)),
    'technology-2022-HL-paper-secA-q10-art': ('014', 5, (60, 78, 538, 351)),
    'technology-2022-HL-paper-secA-q5-art': ('014', 3, (430, 316, 543, 514)),
    'technology-2022-HL-paper-secA-q6-art': ('014', 3, (54, 562, 140, 724)),
    'technology-2022-HL-paper-secB-q2c-art': ('039', 1, (474.5, 256, 572, 430)),
    'technology-2022-HL-paper-secB-q3a-art': ('039', 2, (398, 212, 536, 392.5)),
    # One point wider than 3(a)'s cut of the same photograph: bind-figures
    # refuses a second name for identical bytes, and 3(b) needs its own.
    'technology-2022-HL-paper-secB-q3b-art': ('039', 2, (397, 212, 536, 392.5)),
    'technology-2022-HL-paper-secC-q5c-art': ('039', 8, (62, 310, 247, 442)),
    'technology-2022-OL-paper-secA-q8-art': ('014', 4, (80, 436, 536, 538)),
    'technology-2022-OL-paper-secB-q3b-art': ('039', 2, (394, 247, 562, 381)),
    'technology-2022-OL-paper-secB-q3d-art': ('039', 2, (358, 634.5, 561, 751)),
    'technology-2022-OL-paper-secC-q2a-art': ('039', 4, (312, 114, 390, 191)),
    'technology-2023-HL-paper-secA-q13-art': ('014', 7, (388, 429, 540, 585)),
    'technology-2023-HL-paper-secA-q8-art': ('014', 5, (152, 136, 502, 274)),
    'technology-2023-HL-paper-secB-q2c-art': ('039', 1, (384, 506, 546, 614)),
    'technology-2023-HL-paper-secC-q2b-art': ('039', 4, (300, 272, 570, 446)),
    'technology-2023-OL-paper-secA-q7-art': ('014', 4, (84, 119.6, 272, 292)),
    'technology-2023-OL-paper-secB-q2a-art': ('039', 1, (399.2, 131, 541, 246)),
    'technology-2023-OL-paper-secC-q1c-art': ('039', 3, (60, 559, 141, 639)),
    'technology-2023-OL-paper-secC-q4a-art': ('039', 6, (420, 111.4, 579, 229)),
    'technology-2024-HL-paper-secA-q10-art': ('014', 5, (411, 403, 533, 499)),
    'technology-2024-HL-paper-secA-q11-art': ('014', 6, (362, 90, 546, 229)),
    'technology-2024-HL-paper-secA-q12-art': ('014', 6, (366, 404, 536, 519)),
    'technology-2024-HL-paper-secA-q15-art': ('014', 8, (209, 132, 355, 258)),
    'technology-2024-HL-paper-secA-q3-art': ('014', 2, (385, 571, 553, 666.5)),
    'technology-2024-HL-paper-secA-q7-art': ('014', 4, (351.8, 96, 566, 247)),
    'technology-2024-HL-paper-secC-q2a-art': ('039', 4, (431, 92, 537, 207)),
    'technology-2024-HL-paper-secC-q2d-art': ('039', 4, (368, 650, 560, 739)),
    'technology-2024-HL-paper-secC-q4d-art': ('039', 7, (155, 358, 376, 484)),
    'technology-2024-HL-paper-secC-q4d-ii-art': ('039', 7, (155, 542, 381, 670.5)),
    'technology-2024-HL-paper-secC-q5c-art': ('039', 8, (438, 432, 562, 557)),
    'technology-2024-OL-paper-secA-q1-art': ('014', 2, (447, 140, 548, 237)),
    'technology-2024-OL-paper-secA-q6-art': ('014', 3, (372.3, 508, 541, 603)),
    'technology-2024-OL-paper-secA-q7-art': ('014', 4, (142, 124, 272, 265)),
    'technology-2024-OL-paper-secA-q8-art': ('014', 4, (398, 298, 528, 408)),
    'technology-2024-OL-paper-secB-q3c-art': ('039', 2, (372, 403, 560, 576)),
    'technology-2024-OL-paper-secC-q1b-art': ('039', 3, (449, 296, 551, 388.8)),
    'technology-2024-OL-paper-secC-q2d-art': ('039', 4, (399.5, 628, 546, 696)),
    'technology-2025-HL-paper-secA-q12-art': ('014', 6, (362, 421, 552, 562)),
    'technology-2025-HL-paper-secA-q15-art': ('014', 8, (100, 141, 255, 306)),
    'technology-2025-HL-paper-secA-q7-art': ('014', 4, (340, 52, 518, 213)),
    'technology-2025-HL-paper-secB-q3b-art': ('039', 2, (407, 231, 556, 358)),
    'technology-2025-HL-paper-secC-q2b-art': ('039', 4, (355, 245, 572, 397)),
    'technology-2025-HL-paper-secC-q2d-art': ('039', 4, (446, 637, 570, 775)),
    'technology-2025-OL-paper-secA-q1-art': ('014', 2, (448, 145, 545, 307)),
    'technology-2025-OL-paper-secA-q3-art': ('014', 2, (427, 571, 549, 668)),
    'technology-2025-OL-paper-secA-q4-art': ('014', 3, (72, 108, 275, 279)),
    'technology-2025-OL-paper-secC-q2c-art': ('039', 4, (387, 423, 557, 562)),
    'technology-2025-OL-paper-secC-q5b-art': ('039', 7, (70, 247, 222, 398)),
})

# In-window parts measured by the residue authors (2026-10-28), one agent per
# year, each crop rendered and looked at before its rect was written.
BY_EYE.update({
})

# The whole-bank audit (2026-10-28), one agent per year: pictures the asks name that
# no card carried, and crops re-measured where a label, inset or caption was cut.
BY_EYE.update({
    'technology-2020-HL-paper-secA-q13-art': ('014', 5, (94, 498, 254, 734)),
    'technology-2020-HL-paper-secA-q14-art': ('014', 6, (383, 135, 557, 298)),
    'technology-2020-HL-paper-secA-q5-art': ('014', 2, (422, 378, 552, 512)),
    'technology-2020-HL-paper-secB-q2b-art': ('039', 1, (315.8, 287.2, 562.4, 482.9)),
    'technology-2020-HL-paper-secB-q2b-ii-art': ('039', 1, (315.8, 334.6, 399.2, 412.9)),
    'technology-2020-HL-paper-secB-q2d-art': ('039', 1, (430, 659, 564, 792)),
    'technology-2020-HL-paper-secB-q3b-art': ('039', 2, (377, 245, 572, 376)),
    'technology-2020-HL-paper-secB-q3c-art': ('039', 2, (492, 433, 560, 590)),
    'technology-2020-HL-paper-secB-q3d-art': ('039', 2, (92, 664, 530, 758)),
    'technology-2020-HL-paper-secC-q1d-art': ('039', 3, (398, 655, 572, 784)),
    'technology-2020-HL-paper-secC-q2b-art': ('039', 4, (362.8, 229, 568.5, 373)),
    'technology-2020-HL-paper-secC-q2b-iii-art': ('039', 4, (93, 373.5, 235, 421)),
    'technology-2020-HL-paper-secC-q2c-art': ('039', 4, (380, 464, 572, 588)),
    'technology-2020-HL-paper-secC-q5b-art': ('039', 8, (379.5, 251.5, 567, 416)),
    'technology-2021-HL-paper-secA-q10-art': ('014', 4, (378, 103, 567.5, 264)),
    'technology-2021-HL-paper-secC-q2c-art': ('039', 4, (365, 444, 541, 573)),
    'technology-2021-HL-paper-secC-q4a-art': ('039', 6, (424, 100, 528, 299)),
    'technology-2021-HL-paper-secC-q4b-art': ('039', 6, (416.2, 426, 572, 553)),
    'technology-2021-HL-paper-secC-q5b-art': ('039', 8, (381, 205, 569, 428)),
    'technology-2021-OL-paper-secA-q10-art': ('014', 4, (431, 106.5, 534.5, 186.5)),
    'technology-2021-OL-paper-secA-q2-art': ('014', 1, (81, 361, 219.5, 531.5)),
    'technology-2021-OL-paper-secA-q3-art': ('014', 1, (405, 589, 538, 717)),
    'technology-2021-OL-paper-secA-q4-art': ('014', 2, (429.5, 66.8, 529.6, 267.5)),
    'technology-2021-OL-paper-secA-q8-art': ('014', 3, (412, 337, 523, 399.5)),
    'technology-2021-OL-paper-secB-q2a-art': ('039', 1, (414, 59, 544, 196)),
    'technology-2021-OL-paper-secB-q2b-art': ('039', 1, (373, 247.5, 550, 351)),
    'technology-2021-OL-paper-secB-q3c-art': ('039', 2, (80, 476, 185, 573)),
    'technology-2021-OL-paper-secC-q1a-art': ('039', 3, (436, 73, 530, 177)),
    'technology-2021-OL-paper-secC-q1b-art': ('039', 3, (381, 226, 556.5, 410.5)),
    'technology-2021-OL-paper-secC-q1c-art': ('039', 3, (377.8, 436, 560, 569.5)),
    'technology-2021-OL-paper-secC-q1d-art': ('039', 3, (77.5, 658.5, 198, 765.5)),
    'technology-2021-OL-paper-secC-q2a-art': ('039', 4, (30.5, 113, 165, 206)),
    'technology-2021-OL-paper-secC-q2b-art': ('039', 4, (333, 205, 579, 409)),
    'technology-2021-OL-paper-secC-q2c-art': ('039', 4, (63, 457, 236, 631)),
    'technology-2021-OL-paper-secC-q3c-art': ('039', 5, (80, 493, 261.5, 596.5)),
    'technology-2021-OL-paper-secC-q4b-art': ('039', 6, (456.5, 206, 568, 304.5)),
    'technology-2022-HL-paper-secA-q12-art': ('014', 6, (62, 101, 276, 296)),
    'technology-2022-HL-paper-secA-q15-art': ('014', 7, (154, 499, 486, 683)),
    'technology-2022-HL-paper-secA-q7-art': ('014', 4, (370.5, 77, 537.7, 145.2)),
    'technology-2022-HL-paper-secA-q9-art': ('014', 4, (380, 513, 538.5, 583.5)),
    'technology-2022-HL-paper-secB-q2c-art': ('039', 1, (474.5, 256, 572, 430)),
    'technology-2022-HL-paper-secC-q1b-art': ('039', 3, (57, 261, 161, 363)),
    'technology-2022-HL-paper-secC-q1c-art': ('039', 3, (395, 489, 541, 602)),
    'technology-2022-HL-paper-secC-q2b-art': ('039', 4, (336, 222, 547, 345)),
    'technology-2022-HL-paper-secC-q3b-art': ('039', 5, (65, 316, 189, 417)),
    'technology-2022-HL-paper-secC-q4a-art': ('039', 6, (64, 138, 538, 302)),
    'technology-2022-HL-paper-secC-q4b-art': ('039', 6, (420, 450, 529, 577)),
    'technology-2022-HL-paper-secC-q4c-art': ('039', 7, (354, 202, 520, 347)),
    'technology-2022-HL-paper-secC-q4d-art': ('039', 7, (89, 540, 381, 648)),
    'technology-2022-HL-paper-secC-q5a-art': ('039', 8, (398, 107, 532, 266)),
    'technology-2022-OL-paper-secA-q1-art': ('014', 2, (441.3, 143, 538, 240.5)),
    'technology-2022-OL-paper-secA-q12-art': ('014', 5, (156, 569, 435, 678)),
    'technology-2022-OL-paper-secA-q7-art': ('014', 4, (47, 157, 228, 299)),
    'technology-2022-OL-paper-secA-q9-art': ('014', 4, (423, 536, 546, 652.5)),
    'technology-2022-OL-paper-secB-q2a-art': ('039', 1, (388.5, 148.4, 557, 259.5)),
    'technology-2022-OL-paper-secB-q2b-art': ('039', 1, (55, 318, 217, 454)),
    'technology-2022-OL-paper-secB-q3c-art': ('039', 2, (45, 459, 221, 562)),
    'technology-2022-OL-paper-secC-q1b-i-art': ('039', 3, (431, 387, 536, 483)),
    'technology-2022-OL-paper-secC-q1c-art': ('039', 3, (467, 514, 538, 613)),
    'technology-2022-OL-paper-secC-q1d-art': ('039', 3, (451, 630, 539, 746)),
    'technology-2022-OL-paper-secC-q2a-i-art': ('039', 4, (418, 81, 543, 241)),
    'technology-2022-OL-paper-secC-q2c-art': ('039', 4, (61, 467, 174, 578)),
    'technology-2022-OL-paper-secC-q4a-art': ('039', 6, (452, 86, 552, 171.2)),
    'technology-2022-OL-paper-secC-q4c-art': ('039', 6, (401, 459, 536, 550)),
    'technology-2022-OL-paper-secC-q5d-art': ('039', 7, (411, 656, 532, 750)),
    'technology-2023-HL-paper-secA-q11-art': ('014', 6, (408, 430, 562, 584)),
    'technology-2023-HL-paper-secA-q15-art': ('014', 8, (92, 430, 204, 553)),
    'technology-2023-HL-paper-secA-q6-art': ('014', 4, (358, 64, 541, 158)),
    'technology-2023-HL-paper-secA-q7-art': ('014', 4, (341, 461, 550, 535)),
    'technology-2023-HL-paper-secB-q2b-art': ('039', 1, (419, 326, 571, 418)),
    'technology-2023-HL-paper-secB-q3b-art': ('039', 2, (342, 246, 540, 384)),
    'technology-2023-HL-paper-secC-q4b-art': ('039', 6, (61, 515.5, 539, 579.5)),
    'technology-2023-HL-paper-secC-q5b-art': ('039', 8, (403, 286, 546, 442.5)),
    'technology-2023-OL-paper-secA-q1-art': ('014', 2, (86, 155, 540, 241)),
    'technology-2023-OL-paper-secA-q11-art': ('014', 5, (78, 258, 216, 368)),
    'technology-2023-OL-paper-secA-q6-art': ('014', 3, (77, 576, 191, 690)),
    'technology-2023-OL-paper-secA-q8-art': ('014', 4, (432, 314, 543, 422)),
    'technology-2023-OL-paper-secA-q9-art': ('014', 4, (426, 534, 538, 652)),
    'technology-2023-OL-paper-secB-q3a-art': ('039', 2, (414, 58, 566, 162)),
    'technology-2023-OL-paper-secB-q3b-art': ('039', 2, (380, 206.3, 553, 300.5)),
    'technology-2023-OL-paper-secB-q3c-art': ('039', 2, (50, 478, 208, 570)),
    'technology-2023-OL-paper-secC-q1b-art': ('039', 3, (432, 254, 551, 458)),
    'technology-2023-OL-paper-secC-q2a-art': ('039', 4, (411, 102, 551, 196)),
    'technology-2023-OL-paper-secC-q5b-ii-art': ('039', 7, (361.3, 322.5, 448.5, 405.5)),
    'technology-2024-HL-paper-secA-q12-art': ('014', 6, (368, 406, 533.5, 517.5)),
    'technology-2024-HL-paper-secA-q5-art': ('014', 3, (110, 253, 548, 480)),
    'technology-2024-HL-paper-secA-q8-art': ('014', 4, (120, 385, 225, 709)),
    'technology-2024-HL-paper-secA-q9-art': ('014', 5, (82, 87, 528, 156)),
    'technology-2024-HL-paper-secB-q2b-art': ('039', 1, (414, 303, 551, 406)),
    'technology-2024-HL-paper-secB-q3d-art': ('039', 2, (430, 632, 556, 762)),
    'technology-2024-HL-paper-secC-q1b-art': ('039', 3, (424, 282.5, 551, 391)),
    'technology-2024-HL-paper-secC-q1d-art': ('039', 3, (393, 657, 546, 763)),
    'technology-2024-HL-paper-secC-q2c-art': ('039', 4, (377, 445, 566, 597)),
    'technology-2024-HL-paper-secC-q4a-art': ('039', 6, (431.5, 140, 534, 259)),
    'technology-2024-HL-paper-secC-q4c-art': ('039', 7, (371, 137, 563, 265)),
    'technology-2024-HL-paper-secC-q5b-art': ('039', 8, (445, 267, 549, 379)),
    'technology-2024-OL-paper-secA-q10-art': ('014', 5, (413, 74, 534, 160)),
    'technology-2024-OL-paper-secA-q11-art': ('014', 5, (357, 260, 544, 350)),
    'technology-2024-OL-paper-secA-q12-art': ('014', 5, (218, 525, 400, 741)),
    'technology-2024-OL-paper-secA-q2-art': ('014', 2, (483, 356, 543, 458)),
    'technology-2024-OL-paper-secA-q4-art': ('014', 3, (80, 98, 197.5, 188)),
    'technology-2024-OL-paper-secA-q5-art': ('014', 3, (388, 292, 540, 414.5)),
    'technology-2024-OL-paper-secA-q9-art': ('014', 4, (415, 510, 541, 640)),
    'technology-2024-OL-paper-secB-q2b-art': ('039', 1, (421, 291, 555, 416)),
    'technology-2024-OL-paper-secB-q3c-art': ('039', 2, (326, 404, 562, 577)),
    'technology-2024-OL-paper-secC-q1a-art': ('039', 3, (432, 137, 546, 251)),
    'technology-2024-OL-paper-secC-q1c-art': ('039', 3, (462, 507, 556, 603)),
    'technology-2024-OL-paper-secC-q1d-art': ('039', 3, (52, 680, 200, 735)),
    'technology-2024-OL-paper-secC-q2a-art': ('039', 4, (53, 128, 131, 219)),
    'technology-2024-OL-paper-secC-q2b-art': ('039', 4, (342.5, 232, 569, 367)),
    'technology-2024-OL-paper-secC-q3a-art': ('039', 5, (410, 93, 536, 188)),
    'technology-2024-OL-paper-secC-q4b-art': ('039', 6, (64, 258, 239, 370)),
    'technology-2024-OL-paper-secC-q5c-art': ('039', 7, (431, 481, 532, 579)),
    'technology-2024-OL-paper-secC-q5d-art': ('039', 7, (368, 646.5, 550, 721)),
    'technology-2025-HL-paper-secA-q10-art': ('014', 5, (405, 424, 532, 551)),
    'technology-2025-HL-paper-secC-q1d-art': ('039', 3, (411, 641, 542, 751)),
    'technology-2025-HL-paper-secC-q4b-art': ('039', 6, (99, 361, 438, 513)),
    'technology-2025-HL-paper-secC-q4d-art': ('039', 7, (160, 494, 467, 646)),
    'technology-2025-HL-paper-secC-q5d-art': ('039', 8, (226, 594, 369, 704)),
    'technology-2025-OL-paper-secA-q5-art': ('014', 3, (422, 293, 532, 403)),
    'technology-2025-OL-paper-secA-q6-art': ('014', 3, (399, 554, 534, 670)),
    'technology-2025-OL-paper-secA-q7-art': ('014', 4, (415, 58, 545, 156)),
    'technology-2025-OL-paper-secA-q8-art': ('014', 4, (427, 246, 535, 341)),
    'technology-2025-OL-paper-secA-q9-art': ('014', 4, (74, 520, 248, 680)),
    'technology-2025-OL-paper-secC-q1b-art': ('039', 3, (449, 235, 557, 430)),
    'technology-2025-OL-paper-secC-q1c-art': ('039', 3, (83, 489, 167, 578)),
    'technology-2025-OL-paper-secC-q1d-art': ('039', 3, (430, 611, 546, 708)),
    'technology-2025-OL-paper-secC-q2a-art': ('039', 4, (439, 110, 548, 194)),
    'technology-2025-OL-paper-secC-q2b-art': ('039', 4, (437, 229, 553, 324)),
    'technology-2025-OL-paper-secC-q2d-art': ('039', 4, (65, 637, 184, 730)),
    'technology-2025-OL-paper-secC-q3d-art': ('039', 5, (377, 594, 543, 690)),
    'technology-2025-OL-paper-secC-q4a-art': ('039', 6, (388, 90, 504, 184)),
    'technology-2025-OL-paper-secC-q5c-art': ('039', 7, (63, 496, 161, 593)),
    'technology-2026-HL-paper-secA-q15-art': ('014', 8, (355, 98, 536, 245)),
    'technology-2026-HL-paper-secA-q3-art': ('014', 2, (60, 616, 239, 744)),
    'technology-2026-HL-paper-secA-q8-art': ('014', 4, (128, 378, 479, 728)),
    'technology-2026-HL-paper-secC-q5a-art': ('039', 8, (413, 95.5, 550.5, 186)),
    'technology-2026-HL-paper-secC-q5b-art': ('039', 8, (66, 226, 280, 432)),
    'technology-2026-HL-paper-secC-q5c-art': ('039', 8, (417.4, 437.4, 541.2, 565.4)),
    'technology-2026-OL-paper-secA-q12-art': ('014', 5, (249, 521, 367, 721)),
    'technology-2026-OL-paper-secA-q5-art': ('014', 3, (461.5, 266.5, 561, 375)),
    'technology-2026-OL-paper-secA-q6-art': ('014', 3, (389.5, 481.8, 547.5, 559.5)),
    'technology-2026-OL-paper-secA-q7-art': ('014', 4, (426, 36, 558, 165)),
    'technology-2026-OL-paper-secA-q8-art': ('014', 4, (58, 341, 193, 476)),
    'technology-2026-OL-paper-secB-q2b-art': ('039', 1, (486.5, 252, 548, 374)),
    'technology-2026-OL-paper-secB-q3d-art': ('039', 2, (419, 643, 538.5, 750)),
    'technology-2026-OL-paper-secC-q1b-art': ('039', 3, (53, 277.5, 198.5, 391.5)),
    'technology-2026-OL-paper-secC-q1c-art': ('039', 3, (416, 486, 545, 583)),
    'technology-2026-OL-paper-secC-q1d-art': ('039', 3, (432.5, 638.5, 545.5, 730.5)),
    'technology-2026-OL-paper-secC-q2b-art': ('039', 4, (394.5, 232.5, 555, 372.5)),
    'technology-2026-OL-paper-secC-q2d-art': ('039', 4, (434.9, 610, 544, 734)),
    'technology-2026-OL-paper-secC-q4b-art': ('039', 6, (53.5, 252.5, 228, 367)),
    'technology-2026-OL-paper-secC-q5a-art': ('039', 7, (413, 85, 544, 203.5)),
    'technology-2026-OL-paper-secC-q5b-art': ('039', 7, (82.5, 248.3, 187.5, 380)),
})

# SCHEME crops: key -> (page index, rect, what was seen). Published with
# solution: true. A caption the scheme prints UNDER its drawing ("Snail or
# drop cam") is left outside the rectangle: it is the scheme's words for the
# part and the card's claimable row, while the words INSIDE the drawing are
# its lettering and the crop carries them.
## solution: true. The description is the alt text and must say what the
# print shows; it quotes the scheme's own words where it prints any.
SOLUTIONS = {
    'technology-2026-HL-scheme-secA-q8': (5, (185, 278, 410, 436),
        "The marking scheme's own answer to 2026 HL Section A Q8, as the State "
        "Examinations Commission printed it: the cordless drill redrawn in "
        "outline with the line weights varied. The scheme captions it: Two "
        "graphic techniques demonstrated."),
    'technology-2026-HL-scheme-secA-q13': (7, (100, 168, 255, 333),
        "The marking scheme's own answer to 2026 HL Section A Q13, as the State "
        "Examinations Commission printed it: a shaded three-dimensional cam, "
        "circular with one radial step cut into its rim and a centre hole. The "
        "scheme captions it: Snail or drop cam."),
    'technology-2026-HL-scheme-secA-q15': (8, (105, 185, 340, 450),
        "The marking scheme's own answer to 2026 HL Section A Q15, as the State "
        "Examinations Commission printed it: a front elevation of the climbing "
        "arch as an inverted U with a ring at each foot, above a plan showing "
        "the two side rails and the rungs between them. The scheme prints "
        "beside it: Suggested Solution: Any valid alternative solution accepted."),
    'technology-2026-HL-scheme-secC-q1b-i': (13, (225, 332, 530, 590),
        "The marking scheme's own answer to 2026 HL Section C Q1(b)(i), as the "
        "State Examinations Commission printed it: a flowchart from Start "
        "through Move to a shelf, Turn on camera and Scan stock to the decision "
        "Is stock full, whose No branch leads to Send alert and whose Yes branch "
        "leads to Move to next shelf and loops back to Move to a shelf. The "
        "scheme prints beside it: Suggested solution, Alternatives accepted."),
    'technology-2026-HL-scheme-secC-q2a-i': (15, (88, 186, 530, 278),
        "The marking scheme's own answer to 2026 HL Section C Q2(a)(i), as the "
        "State Examinations Commission printed it: a logic circuit in which "
        "Fingerprint sensor and PIN Code feed an OR gate, whose output and "
        "Power Level feed an AND gate, whose output is Unlock. The scheme prints "
        "beside it: Suggested solution, Alternatives accepted."),
    'technology-2026-HL-scheme-secC-q2a-ii': (15, (105, 312, 487, 452),
        "The marking scheme's own answer to 2026 HL Section C Q2(a)(ii), as the "
        "State Examinations Commission printed it: a truth table with columns "
        "Fingerprint sensor, PIN Code, Power Level and Unlock, eight rows from "
        "0 0 0 0 to 1 1 1 1, with Unlock at 1 in the rows 0 1 1, 1 0 1 and 1 1 1."),
    'technology-2026-HL-scheme-secC-q2b-ii': (15, (88, 596, 548, 752),
        "The marking scheme's own answer to 2026 HL Section C Q2(b)(ii), as the "
        "State Examinations Commission printed it: the op-amp wired as a "
        "comparator between 9 V and 0 V rails, a potential divider of a "
        "variable resistor and an LDR feeding the inverting input A, R1 and R2 "
        "feeding the non-inverting input B, and the output driving an LED "
        "through a resistor, labelled Input: Potential divider eg variable "
        "resistor with LDR shown, and LED output."),
    'technology-2026-HL-scheme-secC-q4b-ii': (19, (305, 514, 572, 690),
        "The marking scheme's own answer to 2026 HL Section C Q4(b)(ii), as the "
        "State Examinations Commission printed it: a control chart titled "
        "Control chart, the twelve daily defect counts plotted as a line on a "
        "0 to 8 scale, a solid Mean line at 4 and dashed UCL and LCL lines at "
        "7.3 and 0.7."),
    'technology-2026-HL-scheme-secC-q5b-ii': (21, (120, 400, 500, 548),
        "The marking scheme's own answer to 2026 HL Section C Q5(b)(ii), as the "
        "State Examinations Commission printed it: a sectioned injection "
        "moulding machine labelled plastic granules, hopper, heaters, mould "
        "cavity, casing mould, screw, barrel, nozzle and moveable plate."),
    'technology-2026-HL-scheme-secB-q3d': (12, (58, 135, 540, 362),
        "The marking scheme's own answer to 2026 HL Section B Q3(d), as the "
        "State Examinations Commission printed it: a table with rows Air "
        "transport, Land transport and Sea transport against columns Carbon "
        "emissions and Pollution, giving each mode's share of global CO2 and "
        "grams of CO2 per tonne-km, and the pollutants it emits."),
    'technology-2026-HL-scheme-secC-q5d': (22, (110, 418, 554, 722),
        "The marking scheme's own answer to 2026 HL Section C Q5(d), as the "
        "State Examinations Commission printed it: a table comparing Composite "
        "materials with Treated softwood timber row by row under Fabrication "
        "techniques, Maintenance and Sustainability."),
    # 2020 Higher.
    'technology-2020-HL-scheme-secC-q1b-i': (12, (80, 258, 358, 622),
        "The marking scheme's own answer to 2020 HL Section C Q1(b)(i), as the "
        "State Examinations Commission printed it: a flowchart from Power On "
        "through Wait 3 and Green LED to three decisions Pollutant A?, B? and "
        "C? whose Y branches reach Amber LED x3, then three decisions Threshold "
        "A?, B? and C? whose Y branches reach Red LED x3 and Buzzer, looping "
        "back. The scheme prints beneath it: Any valid alternative solution "
        "accepted."),
    'technology-2020-HL-scheme-secC-q2b-i': (14, (270, 136, 505, 242),
        "The marking scheme's own answer to 2020 HL Section C Q2(b)(i), as the "
        "State Examinations Commission printed it: the op-amp circuit completed "
        "between +9 V and 0 V rails, a variable resistor and an LDR as the "
        "input potential divider, 66 kΩ and 33 kΩ resistors feeding point A, "
        "and an LED with its resistor on the output."),
    'technology-2020-HL-scheme-secC-q2d-i': (14, (80, 672, 285, 762),
        "The marking scheme's own answer to 2020 HL Section C Q2(d)(i), as the "
        "State Examinations Commission printed it: a logic circuit in which "
        "Keypad (A) and Keypad (B) feed an OR gate, its output and Switch (C) "
        "feed a second OR gate E, and E with Switch (S) feed an AND gate whose "
        "output is F."),
    'technology-2020-HL-scheme-secC-q2d-ii': (14, (355, 646, 515, 772),
        "The marking scheme's own answer to 2020 HL Section C Q2(d)(ii), as the "
        "State Examinations Commission printed it: a truth table with columns "
        "A, B, C, E, S and F over eight rows from 0 0 0 0 0 0 to 1 1 1 1 1 1."),
    # 2026 Ordinary.
    'technology-2026-OL-scheme-secA-q4': (4, (295, 100, 440, 235),
        "The marking scheme's own answer to 2026 OL Section A Q4, as the State "
        "Examinations Commission printed it: an elevation of the three-tiered "
        "planter box in outline, three shelves of equal width stepped one above "
        "the other between two uprights. The scheme prices it by quality: "
        "(8,6,4,2 Marks)."),
    'technology-2026-OL-scheme-secB-q2b-iii': (7, (418, 388, 556, 472),
        "The marking scheme's own answer to 2026 OL Section B Q2(b)(iii), as the "
        "State Examinations Commission printed it: a sectioned injection "
        "moulding machine labelled Hopper, Heater, Ram, Mould, Hydraulic fluid, "
        "Screw and Motor, beside the words Injection moulded."),
    'technology-2026-OL-scheme-secC-q1b-i': (9, (40, 340, 180, 745),
        "The marking scheme's own answer to 2026 OL Section C Q1(b)(i), as the "
        "State Examinations Commission printed it: a flowchart from Start to "
        "the decision Button?, whose N branch loops back and whose Y branch "
        "runs LEDs On, Wait 2, Motor On, Melody On (dashed), Wait 15, LEDs "
        "Off, Motor Off and Melody Off (dashed) before looping back to Start; "
        "the dashed boxes are the modification (iii) asks for."),
    # In-window drawn answers that shipped as fragment rows or stayed open.
    'technology-2021-HL-scheme-secC-q2a-ii': (16, (85, 190, 462, 302),
        "The marking scheme's own answer to 2021 HL Section C Q2(a)(ii), as the "
        "State Examinations Commission printed it: a square wave labelled A "
        "Digital signal above a sine wave labelled An Analogue signal."),
    'technology-2021-HL-scheme-secC-q2b-iii': (16, (130, 440, 420, 595),
        "The marking scheme's own answer to 2021 HL Section C Q2(b)(iii), as the "
        "State Examinations Commission printed it: the 555 astable circuit "
        "between 6V and 0V rails with R1, R2, C1 and C2, its pin 3 output "
        "driving a transistor through a resistor and an LED in the collector "
        "line. The scheme prints beside the part: See diagram above."),
    'technology-2023-OL-scheme-secC-q1b-i': (11, (52, 292, 192, 612),
        "The marking scheme's own answer to 2023 OL Section C Q1(b)(i), as the "
        "State Examinations Commission printed it: a flowchart from Start to "
        "the decision On?, whose N branch loops back and whose Y branch runs "
        "LED On, Wait 2s, Motor On, Wait 30s, Motor Off, LED On and back to "
        "the decision."),
    'technology-2023-OL-scheme-secC-q1b-ii': (11, (430, 365, 562, 722),
        "The marking scheme's own answer to 2023 OL Section C Q1(b)(ii), as the "
        "State Examinations Commission printed it: the flowchart modified so "
        "that after Start and the decision On?, the Y branch runs LED On, Wait "
        "2s, Motor On, Music On, Wait 30s, Motor/Music Off, LED On and loops "
        "back. The scheme prints beside it: Any valid alternative solution "
        "accepted."),
    'technology-2025-OL-scheme-secC-q1b-i': (9, (420, 328, 562, 630),
        "The marking scheme's own answer to 2025 OL Section C Q1(b)(i), as the "
        "State Examinations Commission printed it: a flowchart from Start to "
        "the decision Button, whose N branch loops back and whose Y branch runs "
        "Gate opens, Wait 30, the decision Object?, Gate closes, Wait 10 and "
        "back to Start; the dashed Y branch leaving Object? is cut at the "
        "edge."),
    'technology-2025-OL-scheme-secC-q1b-iii': (9, (343, 496, 562, 652),
        "The marking scheme's own answer to 2025 OL Section C Q1(b)(iii), as "
        "the State Examinations Commission printed it: the lower part of its "
        "flowchart, where the decision Object? after Wait 30 sends a Y branch, "
        "drawn dashed, to a red Stop box before Gate closes and Wait 10. The "
        "scheme prints beneath it: Any valid alternative solution accepted."),
}

SOLUTIONS.update({
    'technology-2021-HL-scheme-secA-q12': (7, (211, 126, 464, 257),
        "The marking scheme's own answer to 2021 HL Section A Q12, as the State Examinations Commission printed it: the gearbox drawing relettered for the calculation. The DC motor drives the small red gear lettered A; the large gear B and the small gear C share the second shaft, the large gear D and the small gear E share the third, and the large red gear F sits on the shaft labelled Output shaft."),
    'technology-2021-HL-scheme-secC-q1b-ii': (14, (64, 476, 415, 754),
        "The marking scheme's own answer to 2021 HL Section C Q1(b)(ii), as the State Examinations Commission printed it: a flowchart. Start leads to Power on, then to the decision Hopper empty?. Its Yes branch leads to Buzzer on, which loops back into itself. Its No branch leads to the decision Is tray less than half full?, whose No branch loops back above the same decision and whose Yes branch leads to Fill and then Wait 6, after which a line returns to the main line just below Power on. The scheme prints beneath it: Any valid alternative solution accepted."),
    'technology-2021-HL-scheme-secC-q1d-i': (15, (129, 497, 516, 670),
        "The marking scheme's own answer to 2021 HL Section C Q1(d)(i), as the State Examinations Commission printed it: a pneumatic circuit. A cylinder at the top has both ends piped down to a 5/2 valve that has a manual actuator on its left, a spring on its right and the air supply and exhausts beneath it; a one-way flow control valve (a variable restrictor with a check valve beside it) sits in the line to the cylinder's left-hand end. The scheme prints beside it: Attach cylinder ram to bottle cap supply. 5/2 valve allow the cylinder to move back and forth once."),
    'technology-2021-HL-scheme-secC-q2d-i': (17, (114, 484, 445, 573),
        "The marking scheme's own answer to 2021 HL Section C Q2(d)(i), as the State Examinations Commission printed it: a logic circuit. Inputs labelled Propeller and Heat feed a two-input AND gate; its output and an input labelled Batteries feed a second two-input AND gate, whose output passes through a NOT gate to an output box labelled Deploy Parachute."),
    'technology-2021-OL-scheme-secA-q11-i': (6, (412, 297.5, 524, 409),
        "The marking scheme's own answer to 2021 OL Section A Q11(i), as the State Examinations Commission printed it: the spade photograph labelled with arrows: F points to the D-shaped grip at the top of the handle, E points to the shaft just below the yellow handle, and L points to the blade."),
    'technology-2021-OL-scheme-secA-q7': (5, (380, 70, 482, 249),
        "The marking scheme's own answer to 2021 OL Section A Q7, as the State Examinations Commission printed it: a line sketch in two views. Above, the elevation of the birdhouse: a pitched roof with overhanging eaves over a rectangular front with a round entrance hole, a small circle for the perch beneath it and a strip across the base. Below, the plan: a rectangle divided down the middle by the roof ridge line. The scheme prints beneath it: (Very good sketch - 8 marks, Fair sketch - 4 marks)."),
    'technology-2021-OL-scheme-secC-q1b-i': (10, (345.3, 203.5, 577.5, 550.5),
        "The marking scheme's own answer to 2021 OL Section C Q1(b)(i), as the State Examinations Commission printed it: a flowchart. Start leads to the decision On?, whose N branch loops back above it; Y leads to Capsule Inserted, then to the decision Large coffee?. Its Y branch leads to Coffee pours and then Stop; its N branch leads to the decision Small coffee?, whose N branch loops back above Large coffee? and whose Y branch leads to Coffee pours and then Stop. The scheme prints beneath it: Any valid alternative solution accepted."),
    'technology-2021-OL-scheme-secC-q1b-ii': (10, (70, 450, 307, 775),
        "The marking scheme's own answer to 2021 OL Section C Q1(b)(ii), as the State Examinations Commission printed it: the flowchart modified for an empty water container. Start leads to the decision On?, whose N branch loops back above it; Y leads to a new decision Water?, whose N branch leads to Refill and loops back above Water?, and whose Y branch leads to Capsule Inserted, then the decision Large coffee?. Its Y branch leads to Coffee pours and then Stop; its N branch leads to Small coffee?, whose N branch loops back above Large coffee? and whose Y branch leads to Coffee pours and then Stop."),
    'technology-2021-OL-scheme-secC-q5a-ii': (15, (133, 179.5, 501.5, 270),
        "The marking scheme's own answer to 2021 OL Section C Q5(a)(ii), as the State Examinations Commission printed it: the completed table. Seat: Fabric, Leather. Tyre: Composite, Steel reinforced rubber. Headlight lens: Ceramic, Glass. The three entries the candidate supplies, Leather, Composite and Glass, are printed in bold."),
    'technology-2022-HL-scheme-secA-q7': (5, (112, 80, 484, 244),
        "The marking scheme's own answer to 2022 HL Section A Q7, as the State Examinations Commission printed it: a Gantt chart (the scheme heads it 'Suggested chart') with Task/Month down the left and months 1 to 6 across the top. Blue bars show Foundations in month 1; Pillars across months 2 and 3; Pre-cast Beam from month 1 into month 3; Install Beam in month 4; Install Railings in month 5; Safety Inspections in month 6."),
    'technology-2022-HL-scheme-secC-q1b-i': (13, (116, 432, 563, 775.5),
        "The marking scheme's own answer to 2022 HL Section C Q1(b)(i), as the State Examinations Commission printed it: a flowchart. Start leads to an input 'Power on', then a decision 'Toner empty'; Yes leads to 'Replace toner', which loops back above 'Toner empty'. No leads to a decision 'Fuser temp. correct'; No leads to 'Wait', which loops back above that decision. Yes leads to a decision 'Is paper in machine?'; No leads to 'Red Flashing Led', which loops back above it. Yes leads to 'Motor on', then a decision 'Sheet Jam?'; Yes leads to 'Buzzer on', which loops back above 'Sheet Jam?'; No leads to 'Copy complete'. The scheme prints beneath it: Any valid alternative solution accepted."),
    'technology-2022-HL-scheme-secC-q2b-ii': (15, (373.5, 402.5, 541, 484),
        "The marking scheme's own answer to 2022 HL Section C Q2(b)(ii), as the State Examinations Commission printed it: a truth table with columns Input 1, Input 2 and Output. Rows: 0 and 0 give 0; 0 and 1 give 1; 1 and 0 give 1; 1 and 1 give 1."),
    'technology-2022-HL-scheme-secC-q2c-ii': (16, (205, 62, 353, 207),
        "The marking scheme's own answer to 2022 HL Section C Q2(c)(ii), as the State Examinations Commission printed it: a circuit diagram of a 555 timer IC wired in astable mode between a top and a bottom supply rail. Resistor R1 runs from the top rail to a node joined to pin 7; resistor R2 runs from that node down to a node joined to pins 2 and 6; capacitor C runs from there to the bottom rail. Pins 8 and 4 are joined to the top rail, pin 1 goes to the bottom rail, and pin 3 is the output on the right."),
    'technology-2022-HL-scheme-secC-q4b-i': (19, (108, 411.5, 424, 668),
        "The marking scheme's own answer to 2022 HL Section C Q4(b)(i), as the State Examinations Commission printed it: a graph with Cost (€) up the vertical axis, marked 2000 at its foot and rising in steps of 2000 to 12000, and Quantity along the horizontal axis, marked 0, 10000 and 20000. A green straight line labelled '3D Printing' rises steeply from the foot of the axes; a blue line labelled 'Injection moulding' starts at the 8000 mark and rises gently. The lines cross at about 10000 units, where a red arrow labelled 'BEQ' points to the crossing."),
    'technology-2022-OL-scheme-secA-q7': (5, (290, 140, 436, 280),
        "The marking scheme's own answer to 2022 OL Section A Q7, as the State Examinations Commission printed it: a 2D line sketch of the Stockholm toddler chair viewed in the direction of arrow A: a square outline with a doubled vertical line down each side for the side panels, a doubled horizontal band across the middle for the seat, and short dashed marks near the top and bottom of each side. The scheme prints beside it: (Very good sketch- 8 marks, fair sketch 4 marks)."),
    'technology-2022-OL-scheme-secC-q1b-i': (9, (48, 379, 182, 693),
        "The marking scheme's own answer to 2022 OL Section C Q1(b)(i), as the State Examinations Commission printed it: the completed flowchart. Start leads to a decision 'On'; N loops back round to Start. Y leads in turn to 'Motor On', 'Sprayer On', 'Wait 15s', 'Motor Off', 'Sprayer Off' and finally 'Stop'."),
    'technology-2022-OL-scheme-secC-q1b-ii': (9, (229, 407.5, 416.6, 766.9),
        "The marking scheme's own answer to 2022 OL Section C Q1(b)(ii), as the State Examinations Commission printed it: the modified flowchart. Start leads to a decision 'On'; N loops back round to Start. Y leads to a new decision 'Stain Low'; its Y branch leads left to an output 'LED On', which loops back up into the 'On' decision. Its N branch leads down through 'Motor On', 'Sprayer On', 'Wait 15s', 'Motor Off' and 'Sprayer Off' to 'Stop'."),
    'technology-2023-HL-scheme-secA-q8': (5, (106, 488, 497, 625.5),
        "The marking scheme's own answer to 2023 HL Section A Q8, as the State Examinations Commission printed it: the completed cause and effect diagram. The spine points to 'Drone will not lift.' and the bones are 'Machine', 'Environment', 'User' and 'Materials'. 'Propellers' (given) sits under Machine, and the scheme's suggested factors fill the other three: 'Wind' under Environment, 'Expertise' under User and 'Weight' under Materials. The scheme prints above it: Three appropriate factors selected. Suggested solution:"),
    'technology-2023-HL-scheme-secC-q1b-i': (13, (176, 382, 536, 674),
        "The marking scheme's own answer to 2023 HL Section C Q1(b)(i), as the State Examinations Commission printed it: a flowchart. Start; an input box 'Power on'; a process box 'Green LED on'; a decision 'Temp. level check' whose No branch goes to 'Heater On' and loops back to the temperature check; its Yes branch goes to a decision 'Water quality check' whose No branch goes to 'Drain water' then 'Refill tank' and loops back to above 'Green LED on'; its Yes branch goes to 'Display Water temperature' then 'Display water pH', which loops back up to above 'Green LED on'. The scheme prints beside it: Any valid alternative solution accepted."),
    'technology-2023-HL-scheme-secC-q1b-ii': (13, (220, 718, 364, 770),
        "The marking scheme's own answer to 2023 HL Section C Q1(b)(ii), as the State Examinations Commission printed it: a flowchart fragment: a decision diamond 'Check light level' whose No branch leads right to a box 'Light on' and whose Yes branch continues downward. The scheme prints above it: Add light sensor check with light switching option."),
    'technology-2023-HL-scheme-secC-q2b-iii': (16, (124, 80, 466.5, 252.5),
        "The marking scheme's own answer to 2023 HL Section C Q2(b)(iii), as the State Examinations Commission printed it: the 2(b) circuit redrawn with the change: the same 9 V and 0 V rails, the A and B divider, the two 10kΩ resistors, the IC, the resistor and the transistor with its buzzer, now with a relay coil placed in the transistor's collector line from the 9 V rail. The relay's switch contacts sit in a separate circuit on the right that holds a motor (M) and an AC supply (~)."),
    'technology-2023-HL-scheme-secC-q2d-i': (16, (108, 562, 582, 655),
        "The marking scheme's own answer to 2023 HL Section C Q2(d)(i), as the State Examinations Commission printed it: a logic gate circuit. Inputs 'Pod in place' and 'Cup in place' enter an AND gate; its output and a third input, 'Temp correct', enter a second AND gate. The second gate's output branches: one branch is labelled 'Coffee machine operates.', the other passes through a NOT gate to a light-emitting diode."),
    'technology-2023-OL-scheme-secA-q7': (6, (308, 84, 539, 245),
        "The marking scheme's own answer to 2023 OL Section A Q7, as the State Examinations Commission printed it: a 2D line sketch, inside a ruled box, of the cookbook stand seen from the side: a tall flat back board leaning back at an angle with its foot on a short base piece, and a support strut running from a small block on the back of the board down to a notched rack (four notches) that slopes along the base."),
    'technology-2023-OL-scheme-secC-q1c-ii': (12, (304, 203, 444, 292),
        "The marking scheme's own answer to 2023 OL Section C Q1(c)(ii), as the State Examinations Commission printed it: a sketch of an 8-pin dual in-line chip seen from above, four pins on each side, with a notch at its top end and a small dot beside the top-left pin; a red arrow from the label 'Pin 1' points to that top-left pin."),
    'technology-2023-OL-scheme-secC-q2d-ii': (13, (426, 644, 504, 732),
        "The marking scheme's own answer to 2023 OL Section C Q2(d)(ii), as the State Examinations Commission printed it: a transistor symbol: a circle containing a vertical bar, with the base lead entering from the left labelled B, the collector lead leaving at the top labelled C, and the emitter lead, carrying an outward-pointing arrow, leaving at the bottom labelled E."),
    'technology-2024-HL-scheme-secC-q1b-i': (13, (220, 321, 488, 640),
        "The marking scheme's own answer to 2024 HL Section C Q1(b)(i), as the State Examinations Commission printed it: a flowchart from Start through Power on to the decision Check for movement., whose No branch loops back to repeat the check and whose Yes branch runs Red LED on, Sound on and Wait 60 seconds. to a second decision Check for movement.; its No branch runs Sound Off then Red LED off, and its Yes branch loops back up to Red LED on."),
    'technology-2024-HL-scheme-secC-q2b-i': (15, (193, 285.5, 450, 395),
        "The marking scheme's own answer to 2024 HL Section C Q2(b)(i), as the State Examinations Commission printed it: the 555 astable circuit redrawn between its two supply rails, R1 and R2 in series to pins 7, 6 and 2 with capacitor C to the lower rail, pins 4 and 8 to the upper rail and pin 1 to the lower, and the output added at pin 3: a polarised capacitor marked + in series with a loudspeaker that returns to the lower rail."),
    'technology-2024-OL-scheme-secA-q7': (5, (372, 84, 510, 208),
        "The marking scheme's own answer to 2024 OL Section A Q7, as the State Examinations Commission printed it: a 2D line sketch of the machine tool stand seen in the direction of arrow A: a flat top overhanging two splayed legs, a rail under the top, a lower cross rail at shelf height and a small foot at the bottom of each leg. The scheme prices it beneath its box: (Very good sketch- 8 marks, fair sketch 4 marks)."),
    'technology-2024-OL-scheme-secC-q1b-i': (9, (443, 253, 558, 518),
        "The marking scheme's own answer to 2024 OL Section C Q1(b)(i), as the State Examinations Commission printed it: a flowchart from Start to the decision Button, whose N branch loops back to Start and whose Y branch runs Motor On, then a second Button decision that loops on itself on N, a third Button decision that loops on itself on N, and Motor Off, which returns to Start. The scheme prints beneath the page's drawings: Any valid alternative solution accepted."),
    'technology-2024-OL-scheme-secC-q1b-ii': (9, (303, 372, 420, 687),
        "The marking scheme's own answer to 2024 OL Section C Q1(b)(ii), as the State Examinations Commission printed it: the flowchart modified with a decision Solution? after the first Button: Start, the decision Button (N back to Start), the decision Solution? (N back to Start), then Motor On, a Button decision looping on itself on N, a second Button decision looping on itself on N, and Motor Off, which returns to Start. The scheme prints beneath it: Any valid alternative solution accepted."),
    'technology-2025-HL-scheme-secC-q1b-i': (12, (308, 312, 560, 652),
        "The marking scheme's own answer to 2025 HL Section C Q1(b)(i), as the State Examinations Commission printed it: a flowchart from Start through Touch screen ON and Place item on conveyor to the decision Barcode read, whose No branch goes to a Reject box and whose Yes branch reaches the decision Is it a plastic bottle?; its Yes branch goes to Send to servo 1 and its No branch to the decision Is it an aluminium can?, whose No branch loops back above that decision and whose Yes branch runs Send to servo 2 and Stop/Print voucher, which loops back to above Touch screen ON. A red arrow labelled Modification points at the Reject box. The scheme prints beside it: Suggested solution, Alternatives accepted:"),
    'technology-2025-HL-scheme-secC-q2b-ii': (14, (60, 441, 513, 593),
        "The marking scheme's own answer to 2025 HL Section C Q2(b)(ii), as the State Examinations Commission printed it: the circuit completed with a variable resistor above an LDR (a resistor in a circle with light arrows pointing in) forming a potential divider whose junction feeds the - input A of the IC, R1 and R2 setting the + input B, and the IC's output driving a resistor in series with an LED (arrows pointing out) down to the 0 V rail. The scheme prints beside it: Input: Potential divider LDR / Variable resistor, and LED output."),
    'technology-2025-HL-scheme-secC-q2c-i': (15, (92, 135, 490, 240),
        "The marking scheme's own answer to 2025 HL Section C Q2(c)(i), as the State Examinations Commission printed it: a logic gate circuit in which Filament in nozzle 1 (B) and Filament in nozzle 2 (C) enter an OR gate; the OR gate's output and Switch on (A) enter an AND gate; that AND gate's output and Temperature sensor for 400°C (D) enter a second AND gate, whose output is E."),
    'technology-2025-HL-scheme-secC-q2c-ii': (15, (235, 289, 404, 540),
        "The marking scheme's own answer to 2025 HL Section C Q2(c)(ii), as the State Examinations Commission printed it: a truth table headed A, B, C, D, E listing all sixteen combinations of A to D from 0 0 0 0 to 1 1 1 1, alternate rows shaded green; E is 1 only in the rows 1 0 1 1, 1 1 0 1 and 1 1 1 1, and 0 in every other row."),
    'technology-2025-OL-scheme-secA-q4': (4, (327, 102, 561, 310),
        "The marking scheme's own answer to 2025 OL Section A Q4, as the State Examinations Commission printed it: a box holding a line sketch of the toy's elevation: the seat drawn as a long rounded bar, the handlebar as a thin upright post topped with a black dot at the left, a short leg down to the left wheel and a curved support down to the right wheel, each wheel drawn as two concentric circles. The scheme prints beneath it: (Very good sketch- 8 marks, good sketch- 6 marks, fair sketch 4 marks)"),
    'technology-2025-OL-scheme-secC-q2c-ii': (11, (462, 465, 546, 542),
        "The marking scheme's own answer to 2025 OL Section C Q2(c)(ii), as the State Examinations Commission printed it: a truth table headed A, B, C, D with the rows 0 0 0 1, 0 1 0 1, 1 0 0 1 and 1 1 1 0."),
})

SOLUTIONS.update({
    'technology-2021-OL-scheme-secB-q2b-ii': (8, (302, 282, 567, 365),
        "The marking scheme's own answer to 2021 OL Section B Q2(b)(ii), as the State Examinations Commission printed it: a circuit diagram with no word labels: a single cell on the left; the top wire runs through a switch and then a resistor; three LEDs (each a diode in a circle with two arrows pointing out) are connected in parallel between that wire and the bottom wire back to the cell."),
    'technology-2022-HL-scheme-secA-q10': (6, (52, 112, 540, 430),
        "The marking scheme's own answer to 2022 HL Section A Q10, as the State Examinations Commission printed it: a table titled 'Risk Assessment – Technology Room – Soldering iron' with six columns: Hazards; Is the hazard present? Y/N; What is the risk?; Risk rating (H = High, M = Medium, L = Low); Control measures; Is this control in place? Y/N. Row 1: Hot soldering iron; Y; Burns; H; 'Use soldering iron stand. Warning signs present.'; Y, Y. Row 2: Damaged power lead; Y; 'Electrocution. Injury/burn. Death.'; H; 'Correct Amp rating fuse fitted and surge protection in place. Use soldering stand.'; last cell blank. Row 3: Fumes; Y; 'Inhalation of toxic fumes.'; H; 'Ventilated area. Fume extraction.'; last cell blank. The entries the scheme fills in for rows 2 and 3 are printed in bold."),
    'technology-2022-HL-scheme-secB-q3b-ii': (11, (164, 513, 428, 659),
        "The marking scheme's own answer to 2022 HL Section B Q3(b)(ii), as the State Examinations Commission printed it: a circuit diagram with no word labels. A battery of cells on the left feeds the top rail through a switch. From the top rail a variable resistor (a resistor crossed by a diagonal arrow) runs down to a junction, and a light-dependent resistor (a resistor in a circle with two arrows pointing in) runs from that junction to the bottom rail. The junction feeds a fixed resistor into the base of an NPN transistor whose emitter goes to the bottom rail. Three LEDs (each a diode in a circle with two arrows pointing out) are connected in parallel between the top rail and the transistor's collector."),
    'technology-2022-HL-scheme-secC-q2d-i': (16, (176, 315, 425, 488),
        "The marking scheme's own answer to 2022 HL Section C Q2(d)(i), as the State Examinations Commission printed it: a circuit diagram with no word labels. A battery of cells on the left feeds the top rail through a switch. From the top rail a thermistor (a resistor crossed by a line with a short flat foot) runs down to a junction, and a variable resistor (a resistor crossed by a diagonal arrow) runs from that junction to the bottom rail. The junction feeds a fixed resistor into the base of the first of two NPN transistors wired as a Darlington pair: its emitter drives the second transistor's base, the two collectors are joined, and the second emitter goes to the bottom rail. The joined collectors connect up to a relay coil (a rectangle) hanging from the top rail, with a diode drawn in parallel across the coil. To the right, a separate loop runs through the relay's switch contacts, a motor (a circle marked M) and a second battery of cells."),
    'technology-2022-OL-scheme-secA-q8': (5, (66, 442, 528, 551),
        "The marking scheme's own answer to 2022 OL Section A Q8, as the State Examinations Commission printed it: a work breakdown structure of three rows of boxes joined left to right by arrows. Row 1: Back, Cut out, Sand, Paint. Row 2: Sides, Cut out, Drill, Sand/Paint. Row 3: Roller, Cut out, Sand, Paint. Arrows from the last box of each row meet at one box, Assemble. The steps the scheme adds (rows 2 and 3 after the part name, and Assemble) are in larger bold type; the Back row and the part names are in the question's own smaller type."),
    'technology-2023-OL-scheme-secC-q2b-ii': (13, (366.2, 237, 530, 339),
        "The marking scheme's own answer to 2023 OL Section C Q2(b)(ii), as the State Examinations Commission printed it: a circuit diagram. Terminals +V (top) and -V (bottom) on the left run to the two moving arms of a double-pole double-throw switch, the arms linked by a dashed line. The two middle contacts are joined and wired to one side of a motor (a circle marked M). The top and bottom contacts each run through a push switch (two contact circles with a T-shaped plunger above and a bar beneath) to a wire down the right side, which joins the motor's other side."),
    'technology-2024-HL-scheme-secA-q8': (5, (228, 440, 318, 647),
        "The marking scheme's own answer to 2024 HL Section A Q8, as the State Examinations Commission printed it: a shaded colour picture of the assembled garden lantern standing upright: a thin wire carrying handle looped over a dark green domed cap, a pale yellow glass chamber below it, a green collar, a grey metal band, and a dark green domed base. The scheme prints no words for Q8 beyond the ask and its tariff."),
    'technology-2024-HL-scheme-secC-q2d-i': (16, (110, 309, 396, 491),
        "The marking scheme's own answer to 2024 HL Section C Q2(d)(i), as the State Examinations Commission printed it: the label 'Truth table:' beside a table with a green header row A, B, C, O and alternate rows shaded light green; the output column O is in bold. Rows (A B C, then O): 0 0 0 gives 0; 0 0 1 gives 1; 0 1 0 gives 0; 0 1 1 gives 1; 1 0 0 gives 0; 1 0 1 gives 0; 1 1 0 gives 1; 1 1 1 gives 1."),
    'technology-2024-OL-scheme-secA-q4-ii': (4, (412, 147, 497, 227),
        "The marking scheme's own answer to 2024 OL Section A Q4(ii), as the State Examinations Commission printed it: the circuit symbol for a buzzer, drawn inside the scheme's reprint of the answer box (the box frame is left out): two parallel horizontal leads enter the curved side of a half-circle whose flat side stands upright on the right."),
    'technology-2024-OL-scheme-secB-q3b-iii': (8, (369, 287, 532, 382),
        "The marking scheme's own answer to 2024 OL Section B Q3(b)(iii), as the State Examinations Commission printed it: a circuit diagram with no word labels: two supply terminals (small circles) on the left of a top and a bottom rail, and four branches in parallel between the rails. Two branches are each a resistor above an LED (a diode in a circle with two arrows pointing out); the other two are each a motor (a circle marked M)."),
    'technology-2024-OL-scheme-secC-q2b-iii': (11, (347, 212, 560, 352),
        "The marking scheme's own answer to 2024 OL Section C Q2(b)(iii), as the State Examinations Commission printed it: a 555 timer circuit drawn between a top rail, which reaches the +V terminal through a switch at the right, and a 0 V rail. The IC is a box with pins 6, 8, 4 along its top, 7 and 2 on its left and 1 at the bottom; pins 8 and 4 go to the top rail and pin 1 to the 0 V rail. A resistor from the top rail feeds pin 2, which a push switch on the left connects down to 0 V; a second resistor from the top rail feeds pins 6 and 7 and a capacitor C (marked +) that runs down to 0 V. The output, pin 3 (labelled 3 in bold), runs through a resistor to an LED (a diode in a circle with two arrows pointing out) and on to the 0 V rail."),
    'technology-2025-HL-scheme-secA-q15': (7, (251, 527.5, 531.2, 730),
        "The marking scheme's own answer to 2025 HL Section A Q15, as the State Examinations Commission printed it: an exploded line drawing of a butt hinge, each part ringed by a soft pink outline and labelled in bold. Hinge plate 1, on the left, is a plate with screw holes and three knuckles; the Hinge pin stands apart in the middle as a long thin rod with a round head, with a small round cap drawn below the left plate; Hinge plate 2, on the right, is a plate with screw holes and two knuckles. Pink leader lines join the labels Hinge plate 1 and Hinge plate 2 to their parts."),
    'technology-2025-HL-scheme-secA-q7': (4, (82, 603, 516, 718),
        "The marking scheme's own answer to 2025 HL Section A Q7, as the State Examinations Commission printed it: a three-column table with a green header row Part, Material, Properties and the Part column shaded green. Sail: Nylon/Kevlar; Hard wearing, high tensile strength, etc. Mast: Aluminium alloy/ Carbon Fibre; Tempered for strength, lightweight, strong, etc. Hull: Fibreglass/Aluminium; Strength, resistance to corrosion, etc. The Material and Properties entries are in bold."),
    'technology-2025-OL-scheme-secA-q9': (5, (300, 506, 472, 606),
        "The marking scheme's own answer to 2025 OL Section A Q9, as the State Examinations Commission printed it: a circuit diagram drawn inside the scheme's answer box (the box frame is left out): a single cell on the left, a push-to-make switch (two contact circles under a bar and plunger) on the top wire, and a motor (a circle marked M) on the bottom wire, all in one series loop."),
    'technology-2025-OL-scheme-secC-q2b-ii': (11, (397.5, 240, 555, 310),
        "The marking scheme's own answer to 2025 OL Section C Q2(b)(ii), as the State Examinations Commission printed it: a circuit diagram with no word labels: a single cell on the left whose two leads run to the two moving arms of a double-pole double-throw switch, the arms linked by a dashed line. The two middle contacts are joined and wired to one side of a motor (a circle marked M); the top and bottom contacts are joined by a wire down the right side, which also meets the motor's other side."),
    'technology-2022-OL-scheme-secC-q2d-ii': (11, (106, 624, 203, 726),
        "The marking scheme's own answer to 2022 OL Section C Q2(d)(ii), as the State Examinations Commission printed it: a completed truth table captioned 'Truth Table', with a yellow header row A, B, C, D and the C and D columns in red. Rows (A B, then C D): 0 0 gives 0 1; 0 1 gives 1 0; 1 0 gives 1 0; 1 1 gives 1 0."),
    'technology-2024-HL-scheme-secC-q4b-ii': (20, (306, 599, 575, 782),
        "The marking scheme's own answer to 2024 HL Section C Q4(b)(ii), as the State Examinations Commission printed it: a graph of Cost (€) on the vertical axis, 0 to 700 in steps of 100, against Quantity on the horizontal axis, 0 to 60 in steps of 10. A red line for option A rises in a straight line from the origin; a blue line for option B starts at about 500 and rises gently. The two lines cross at a quantity of 50, where a dashed vertical line is drawn and the point (50,507.5) is labelled with an arrow; the point (50,425) on the red line is labelled with a second arrow below it, and the crossing is marked (BEQ) at the right."),
    # Working the text layer cannot carry: a stacked fraction reads as two
    # lines ("R = V = 4.05" / "I 0.015 = 270 Ω"), and a side-by-side "Alt:"
    # column interleaves with the main working line by line.
    'technology-2020-HL-scheme-secA-q11': (6, (80, 525, 316, 702),
        "The marking scheme's own answer to 2020 HL Section A Q11, as the State Examinations Commission printed it: a boxed calculation headed 'Calculation:'. V = 6 - 1.95 = 4.05 V. I = 15 mA = 0.015 A. R = V over I = 4.05 over 0.015 (written as stacked fractions), = 270 Ω."),
    'technology-2020-HL-scheme-secA-q14-ii': (8, (122, 252, 548, 342),
        "The marking scheme's own answer to 2020 HL Section A Q14(ii), as the State Examinations Commission printed it, in bold: Gear ratio = 12 : 96 = 1 : 8. Then 2750 x 12 = o/p x 96; o/p = (2750 x 12) / 96; = 343.75 RPM. Beside it an alternative headed 'Alt:': Driven Speed = G.R x input speed; 1/8 x 2750 = 343.75 RPM."),
    'technology-2026-HL-scheme-secA-q9-ii': (5, (118, 670, 250, 705),
        "The marking scheme's own answer to 2026 HL Section A Q9(ii), as the State Examinations Commission printed it, in bold: M.A. = Load over Effort = 250 over 50 = 5, the two fractions written as stacked numerators and denominators."),
    'technology-2025-OL-scheme-secC-q2d-ii': (11, (459, 631, 516, 698),
        "The marking scheme's own answer to 2025 OL Section C Q2(d)(ii), as the State Examinations Commission printed it: the circuit symbol for a phototransistor: a transistor in a circle, with a base lead entering from the left to an upright bar, the collector line leaving at the top right and the emitter leaving at the bottom right with an arrow pointing outward, and two parallel arrows pointing in at the circle's upper left for the light falling on it."),
})

SOLUTIONS.update({
    'technology-2020-HL-scheme-secB-q2a-ii': (10, (385.5, 108.4, 521, 204),
        "The marking scheme's own answer to 2020 HL Section B Q2(a)(ii), as the State Examinations Commission printed it: side and front views of a person wearing a leg exoskeleton strapped on with orange bands at the waist, thigh and shank. Labels read 'Identical joint for each DOF' (pointing to red circular joints at hip, knee and ankle), 'Interfaces' (pointing to the orange straps), 'Additional module' (cut to 'Additiona' at the picture's edge as printed), 'Thigh segment' and 'Shank segment'."),
    'technology-2020-HL-scheme-secB-q2b-ii': (10, (448, 295, 554, 404),
        "The marking scheme's own answer to 2020 HL Section B Q2(b)(ii), as the State Examinations Commission printed it: two photos beside its text, a black moulded roller wheel with a metal ball bearing at its centre, and below it a length of grey aluminium extruded groove profile."),
    'technology-2020-HL-scheme-secC-q1b-i': (12, (78, 256, 363.2, 624),
        "The marking scheme's own answer to 2020 HL Section C Q1(b)(i), as the State Examinations Commission printed it: a flowchart. Power On, Wait 3, then output Green LED. Decisions Pollutant A?, Pollutant B? and Pollutant C? in a row, each N leading to the next and Pollutant C?'s N looping back above Pollutant A?; any Y leads to output Amber LED x3. Then decisions Threshold A?, Threshold B? and Threshold C? in a row, each N leading to the next and Threshold C?'s N looping back to the top loop; any Y leads to Red LED x3, then Buzzer, which loops back above Threshold A?. Beneath it: Any valid alternative solution accepted."),
    'technology-2020-HL-scheme-secC-q1c-ii': (13, (429, 152, 527, 225),
        "The marking scheme's own answer to 2020 HL Section C Q1(c)(ii), as the State Examinations Commission printed it: a photo of a robotic end-effector, a mechanical gripper with two red padded fingers closing around a ripe strawberry on its stalk, with more strawberries beside it."),
    'technology-2020-HL-scheme-secC-q2b-i': (14, (270, 139, 503, 241.5),
        "The marking scheme's own answer to 2020 HL Section C Q2(b)(i), as the State Examinations Commission printed it: the completed circuit. A switch in the +9 V rail; a resistor above an LDR (a circle with two incoming arrows) forms the input divider, joined to the − input at A; the 66 kΩ and 33 kΩ divider feeds the + input of the IC; the IC output goes through a resistor to an LED (diode in a circle with two outgoing arrows) returning to the 0 V rail."),
    'technology-2021-HL-scheme-secA-q4': (4, (75, 125, 352, 248),
        "The marking scheme's own answer to 2021 HL Section A Q4, as the State Examinations Commission printed it: a boxed calculation headed Calculation:. Torque = Force x Distance. Force = Torque over Distance = 206 over 0.7 = 294N."),
    'technology-2021-HL-scheme-secA-q5': (4, (50, 342, 545, 530),
        "The marking scheme's own answer to 2021 HL Section A Q5, as the State Examinations Commission printed it: headed Suggestion -other solutions and formats accepted, a work breakdown structure chart. The top box Face shield branches to 1. Research and design, 2. Select materials and 3. Make the product; 3. Make the product branches to 3.1 Cut plastic sheet, 3.2 3D print headband and 3.3 Assemble parts; 3.1 Cut plastic sheet leads down to 3.1.1 Punch/drill holes. A small reprint of the faceshield photograph sits at top right."),
    'technology-2021-HL-scheme-secA-q9': (5, (66, 594, 534, 724),
        "The marking scheme's own answer to 2021 HL Section A Q9, as the State Examinations Commission printed it: the completed table with columns Category, Material, Electrical Property and Use. Conductor: Copper; Allows current to pass through.; Electrical wire. Insulator: PVC and Silicon; Prevents current flow; Coating on wire. Semi-conductor: Silicon; Allows some current to flow under certain conditions; IC / Transistors. The entries the candidate supplies are printed in bold."),
    'technology-2021-HL-scheme-secB-q2b-ii': (10, (30, 512, 550, 648),
        "The marking scheme's own answer to 2021 HL Section B Q2(b)(ii), as the State Examinations Commission printed it: a photograph of the Crew Demo-2 seats with four red arrows to callouts. Left: Head rests are made to fit the operator. Space in front of the occupant allows movement. Right: Seats are measured to fit the operator; they can tilt back into a flat configuration. The footrests can adjust to the length of the operator legs."),
    'technology-2021-HL-scheme-secB-q2c-ii': (11, (238, 198, 579, 358),
        "The marking scheme's own answer to 2021 HL Section B Q2(c)(ii), as the State Examinations Commission printed it: a side-view line sketch of the tilting touchscreen. A tall panel (the screen) leans on a mounting at its back; a red arrow points to the Mounting plate at the top of the mechanism and another to the Motor with screw mechanism below it, a coil-like screw driven against a wedge so that turning it tilts the panel. Only the tip of the arrow from the scheme's 'screen' label shows at the left edge."),
    'technology-2021-HL-scheme-secB-q3c': (13, (412, 120, 590, 462),
        "The marking scheme's own answer to 2021 HL Section B Q3(c), as the State Examinations Commission printed it: three sketches stacked. Top: a multimeter reading 61.28 with its red and black probes across a resistor labelled Resistor. Middle: a multimeter reading 12.60 with its leads on the terminals of a battery. Bottom: a multimeter reading 0.548 with its red probe on the end of a diode marked + and Anode and its black probe on the end marked - and Cathode."),
    'technology-2021-HL-scheme-secC-q2c-i': (17, (86, 98, 376, 159),
        "The marking scheme's own answer to 2021 HL Section C Q2(c)(i), as the State Examinations Commission printed it: C = BC107. Transistor Gain = Collector current over Base current = 0.1 over 0.001 = 100."),
    'technology-2021-HL-scheme-secC-q2c-ii': (17, (86, 207, 336, 314),
        "The marking scheme's own answer to 2021 HL Section C Q2(c)(ii), as the State Examinations Commission printed it: Transistor Gain = Collector current over Base current. Collector current = Transistor Gain x Base Current. Collector current = 20 x 0.0003 = 0.006A or 6mA."),
    'technology-2021-HL-scheme-secC-q4b-i': (20, (90, 573, 505, 649),
        "The marking scheme's own answer to 2021 HL Section C Q4(b)(i), as the State Examinations Commission printed it: Manufacturer A Cp = Tolerance Range over 6δ = (39.95 – 39.85) over (6 × 0.04077) = 0.1 over 0.24462 = 0.409. Manufacturer B Cp = Tolerance Range over 6δ = (39.95 – 39.85) over (6 × 0.01620) = 0.1 over 0.0972 = 1.029."),
    'technology-2021-HL-scheme-secC-q4d-i': (21, (200, 290, 377, 387),
        "The marking scheme's own answer to 2021 HL Section C Q4(d)(i), as the State Examinations Commission printed it: a product life cycle chart. A red vertical axis (sales) and a red horizontal axis labelled time; a blue S-shaped curve rises slowly, climbs, levels to a peak and then falls. Dotted vertical lines divide it into four stages lettered A, B, C and D from left to right."),
    'technology-2021-HL-scheme-secC-q5b-ii': (22, (358, 332, 562, 428),
        "The marking scheme's own answer to 2021 HL Section C Q5(b)(ii), as the State Examinations Commission printed it: a sketch of an injection-moulding machine. A Plastic hopper feeds a barrel holding a screw; red arrows above and below mark the Heated chamber with screw; a blue Motor drive turns the screw at the right end, and at the left end the barrel narrows into a green two-part mould."),
    'technology-2021-OL-scheme-secB-q2d-ii': (8, (374, 741.5, 469, 791),
        "The marking scheme's own answer to 2021 OL Section B Q2(d)(ii), as the State Examinations Commission printed it: a picture of a piece of corrugated cardboard cut to show its edge, two wavy fluted layers between flat liner sheets, captioned Double Wall Corrugated."),
    'technology-2021-OL-scheme-secC-q1d-ii': (11, (292, 557, 486, 676),
        "The marking scheme's own answer to 2021 OL Section C Q1(d)(ii), as the State Examinations Commission printed it: a photograph of a mechanical gripper, two upright jaws on a parallel linkage driven by meshing gears; labels point to the Jaw, the Parallel linkage (circled in red) and the Gear, and beneath it the caption Mechanical gripper."),
    'technology-2021-OL-scheme-secC-q2b-iii': (12, (335, 198, 582, 399),
        "The marking scheme's own answer to 2021 OL Section C Q2(b)(iii), as the State Examinations Commission printed it: the timer circuit redrawn with an indicator added. From +V through the switch, a new branch of a resistor and an LED runs straight down to 0V, so it lights as soon as the switch closes; the rest is the timer circuit with resistor R, capacitor A, transistor B and output LED C."),
    'technology-2022-HL-scheme-secA-q8': (5, (372, 335, 495, 453),
        "The marking scheme's own answer to 2022 HL Section A Q8, as the State Examinations Commission printed it: a shaded pictorial view of the assembled castor wheel, the flat top mounting plate with four bolt holes sitting on two side brackets that hold the wheel on its axle, captioned 'assembled castor wheel'."),
    'technology-2022-HL-scheme-secB-q2b-iii': (9, (110, 583, 332, 683),
        "The marking scheme's own answer to 2022 HL Section B Q2(b)(iii), as the State Examinations Commission printed it: under the italic heading 'Suggested solution:', a sketch of rack-and-pinion steering seen from above: two wheels joined by a track rod, a steering column dropping onto a pinion on the rack with a double-headed arrow along it, a separate close-up of the pinion turning on the toothed rack, and red double-headed arrows at each wheel showing them turning."),
    'technology-2022-HL-scheme-secB-q2c-i': (10, (80, 146, 270, 246),
        "The marking scheme's own answer to 2022 HL Section B Q2(c)(i), as the State Examinations Commission printed it: a product life cycle graph with Sales up the vertical axis and Time along the horizontal axis. A bell-shaped curve rises slowly, then steeply, peaks and falls away; the area under it is split into four coloured bands numbered 1 (blue, the slow start), 2 (green, the steep rise), 3 (yellow, the peak) and 4 (red, the fall)."),
    'technology-2022-HL-scheme-secB-q2d-i': (10, (366, 459, 552, 558),
        "The marking scheme's own answer to 2022 HL Section B Q2(d)(i), as the State Examinations Commission printed it: a cut-away picture of a fibre-reinforced sheet peeled back in layers, showing yellow and blue fibre layers laid in different directions between grey outer skins, labelled 'Fibre layers in bonding plastic'."),
    'technology-2022-HL-scheme-secB-q2d-ii': (10, (376, 587, 562, 703),
        "The marking scheme's own answer to 2022 HL Section B Q2(d)(ii), as the State Examinations Commission printed it: an exploded view of laminated glass, two pale green wavy-edged glass sheets with a thin interlayer between them, with leader lines labelling the outer sheets 'Glass' and the middle sheet 'Interlayer'."),
    'technology-2022-HL-scheme-secB-q3b-i': (11, (268, 338, 556, 442),
        "The marking scheme's own answer to 2022 HL Section B Q3(b)(i), as the State Examinations Commission printed it: a photograph of the e-scooter folded flat, its handlebar column hinged down over the deck, with a red box round the hinge at the top of the column and red lines leading to an enlarged close-up of the hinge mechanism on the left."),
    'technology-2022-HL-scheme-secC-q1c-i': (14, (436, 270, 546, 366),
        "The marking scheme's own answer to 2022 HL Section C Q1(c)(i), as the State Examinations Commission printed it: a line sketch of a gantry-style machine frame with a print head, and three arrows marking the axes: Z (blue) pointing up, X (red) pointing right and Y (green) pointing forward and left."),
    'technology-2022-HL-scheme-secC-q1d-i': (14, (317, 520, 576, 686),
        "The marking scheme's own answer to 2022 HL Section C Q1(d)(i), as the State Examinations Commission printed it: a pneumatic circuit. A double-acting cylinder at the top is fed through two flow control valves, one of them marked by a red arrow from the label 'Flow control valve', from a 5/2 valve, which is piloted from each side by a spring-return 3/2 push-button valve."),
    'technology-2022-HL-scheme-secC-q3b-iii': (17, (338, 607, 410, 762),
        "The marking scheme's own answer to 2022 HL Section C Q3(b)(iii), as the State Examinations Commission printed it: two framed example pictures, one above the other. Top, the bitmap example: a letter S in grey and black whose curved edges break up into visible square pixels, with a small s in the lower left corner. Bottom, the vector example: the same letter S drawn in dark blue with smooth, crisp curved edges, with a small s in the lower left corner."),
    'technology-2022-HL-scheme-secC-q5b-ii': (21, (360, 505, 534, 671),
        "The marking scheme's own answer to 2022 HL Section C Q5(b)(ii), as the State Examinations Commission printed it: a photograph of a pendulum impact tester (a red striker on a swinging arm above a round dial on an upright post, on a flat base), annotated with red arrows: 'Striker at a predetermined height.', 'Dial records energy expended, or distance moved by striker' and 'Clamping device for each material'."),
    'technology-2022-HL-scheme-secC-q5b-iii': (22, (100, 87, 522, 162),
        "The marking scheme's own answer to 2022 HL Section C Q5(b)(iii), as the State Examinations Commission printed it: three captioned pictures in a row: a brown wavy roofing sheet captioned 'Corrugated sheet'; a close-up of a fibre-filled surface captioned 'Fibre-reinforcement'; and three grey open plastic trays, the second and third with a grid of strengthening ribs inside, captioned 'Impact of ribbed products'."),
    'technology-2022-HL-scheme-secC-q5c-ii': (22, (362, 326, 577, 431),
        "The marking scheme's own answer to 2022 HL Section C Q5(c)(ii), as the State Examinations Commission printed it: a cross-section of an injection moulding machine: a blue 'Motor drive' block on the right turns a screw inside a barrel labelled 'Heated chamber with screw' (red arrows marking the heaters), a 'Plastic hopper' feeds the barrel from above, and the nozzle at the left injects into a green two-part 'mould'."),
    'technology-2022-OL-scheme-secB-q2b-iii': (7, (47, 342, 192, 460),
        "The marking scheme's own answer to 2022 OL Section B Q2(b)(iii), as the State Examinations Commission printed it: a circuit diagram with no word labels: a battery on the left feeds the top rail through a switch; from the top rail two open probe contacts (the water-level sensor) run down to a junction above a variable resistor to the bottom rail; the junction feeds a resistor into the base of an NPN transistor, and a buzzer hangs from the top rail on the right into the transistor's collector."),
    'technology-2022-OL-scheme-secC-q1b-ii': (9, (229, 407.5, 416.6, 768.6),
        "The marking scheme's own answer to 2022 OL Section C Q1(b)(ii), as the State Examinations Commission printed it: the modified flowchart. Start leads to a decision 'On'; N loops back round to Start. Y leads to a new decision 'Stain Low'; its Y branch leads left to an output 'LED On', which loops back up into the 'On' decision. Its N branch leads down through 'Motor On', 'Sprayer On', 'Wait 15s', 'Motor Off' and 'Sprayer Off' to 'Stop'."),
    'technology-2022-OL-scheme-secC-q1c-ii': (10, (224, 248, 443, 348),
        "The marking scheme's own answer to 2022 OL Section C Q1(c)(ii), as the State Examinations Commission printed it: the symbol for a single-acting cylinder: a rectangular barrel with a piston and its rod projecting out of the right end, a zig-zag return spring on the rod side, and an air port at the left end labelled A; red arrows label the rod 'Piston' and the zig-zag 'Spring'."),
    'technology-2022-OL-scheme-secC-q2b-iii': (11, (385, 242, 569, 382),
        "The marking scheme's own answer to 2022 OL Section C Q2(b)(iii), as the State Examinations Commission printed it: the 2(b) circuit redrawn between the 6V and 0V rails (variable resistor A over thermistor B feeding a transistor, buzzer C in its collector line, a switch in the top rail) with a voltmeter, a circle marked V, connected by red leads across both ends of buzzer C."),
    'technology-2023-HL-scheme-secA-q15': (8, (305, 598, 466, 778),
        "The marking scheme's own answer to 2023 HL Section A Q15, as the State Examinations Commission printed it: three stippled orthographic views of Eileen Gray's non-conformist chair on its tubular steel frame. Top left, a face-on view of the padded backrest above the ribbed seat with the armrest at one side; top right, a side view showing the curved tube of the frame and the seat; below left, a third view of the backrest roll and the ribbed seat between the frame tubes."),
    'technology-2023-HL-scheme-secA-q6': (4, (272, 608, 460, 740),
        "The marking scheme's own answer to 2023 HL Section A Q6(ii), as the State Examinations Commission printed it: the words 'Suggestion: Gear is attached using a grub screw.' above a photograph of a metal spur gear on a hub, with a grub screw standing out of a threaded hole in the hub and a red arrow pointing at it."),
    'technology-2023-HL-scheme-secA-q9': (6, (317, 64, 516, 275),
        "The marking scheme's own answer to 2023 HL Section A Q9, as the State Examinations Commission printed it: the wind turbine line drawing enhanced by hand, one rotor blade and the cylindrical tower shaded in red, the nacelle cross-hatched in blue, with the labels Rotor, Nacelle (contains gears and generator) and Cylindrical tower and their arrows."),
    'technology-2023-HL-scheme-secB-q2b-ii': (9, (240, 500, 522, 621),
        "The marking scheme's own answer to 2023 HL Section B Q2(b)(ii), as the State Examinations Commission printed it: an exploded drawing of a battery compartment, a teal open-topped housing with a small connector board to its right, two pink cylindrical batteries below it and a flat teal cover at the bottom, labelled housing, connector, batteries and 'Cover to click into place keeping batteries secure.'"),
    'technology-2023-HL-scheme-secB-q3b-i': (11, (110, 333, 577, 493),
        "The marking scheme's own answer to 2023 HL Section B Q3(b)(i), as the State Examinations Commission printed it: under 'Suggested solution:', a white jointed robot arm with a black cable along it. A red arrow from 'Charging point has sensors to align with car.' points at the arm's end; three red arrows from 'Robot arms can be controlled by stepper motors for precise movement.' point at its three joints. A box beside it reads 'Alternative solutions acceptable: Servo motors, gearbox system etc.'"),
    'technology-2023-HL-scheme-secC-q1c-ii': (14, (360.3, 329, 522, 473),
        "The marking scheme's own answer to 2023 HL Section C Q1(c)(ii), as the State Examinations Commission printed it: a polar robot, a box-shaped base with a telescopic arm and gripper, inside a partial hollow sphere showing its work envelope; curved arrows mark rotation theta about the vertical axis and tilt theta about a horizontal axis, and a straight double arrow Y marks the arm's extension."),
    'technology-2023-HL-scheme-secC-q2b-iii': (16, (127, 82, 467, 254),
        "The marking scheme's own answer to 2023 HL Section C Q2(b)(iii), as the State Examinations Commission printed it: the 9 V temperature circuit redrawn with a relay. A switch on the 9 V rail feeds the potential divider of variable resistor A over thermistor B and the 10kΩ-10kΩ reference divider into the IC comparator, whose output drives a transistor through a resistor. The relay coil sits in the transistor's collector line, with the buzzer in its emitter line, and the relay's switch closes a separate mains loop (marked with an AC symbol) through a motor M for the fan. 0 V rail along the bottom."),
    'technology-2023-HL-scheme-secC-q4b-ii': (19, (149, 497, 426, 676),
        "The marking scheme's own answer to 2023 HL Section C Q4(b)(ii), as the State Examinations Commission printed it: a control chart titled 'Control chart' with a vertical scale from 0 to 14. A brown line plots the daily defects 9, 11, 8, 9, 10, 8, 8; a solid blue Mean line runs at 9, and dashed blue lines mark the UCL at about 13 and the LCL at about 5, each labelled on the right."),
    'technology-2023-HL-scheme-secC-q5b-ii': (21, (250, 506, 577, 648),
        "The marking scheme's own answer to 2023 HL Section C Q5(b)(ii), as the State Examinations Commission printed it: a section through an injection moulding machine, a green mould on the left fed by a nozzle, a barrel containing a screw with red heater arrows above and below, a plastic hopper on top, a blue motor drive and a ram on the right. Labels: mould, Plastic hopper, Motor drive, Ram, Heated chamber with screw."),
    'technology-2023-HL-scheme-secC-q5b-iii': (22, (387, 89, 553, 187),
        "The marking scheme's own answer to 2023 HL Section C Q5(b)(iii), as the State Examinations Commission printed it: a section through a snap-fit joint, the hooked lip of the casing clipped over a ledge on the base, with arrows from the labels 'Casing' and 'Base of mouse'."),
    'technology-2023-HL-scheme-secC-q5c-i': (22, (135, 285.5, 266, 417),
        "The marking scheme's own answer to 2023 HL Section C Q5(c)(i), as the State Examinations Commission printed it: a photograph of a fatigue-testing machine, a tall frame with a test head above a plunger that presses repeatedly on a computer mouse on the bed, a red double-headed arrow showing the up-and-down action and a control box on the right."),
    'technology-2023-OL-scheme-secB-q3b-iii': (10, (97, 324, 477, 398.4),
        "The marking scheme's own answer to 2023 OL Section B Q3(b)(iii), as the State Examinations Commission printed it: two AA 1.5 V cells joined end to end in one line, captioned 'Batteries in Series', and two AA cells stacked one above the other with their ends joined by wires to a common line on each side, captioned 'Batteries in Parallel'."),
    'technology-2023-OL-scheme-secC-q2b-ii': (13, (365, 238, 529, 340),
        "The marking scheme's own answer to 2023 OL Section C Q2(b)(ii), as the State Examinations Commission printed it: a DPDT switch wired for forward and reverse motor control. The +V and -V supply lines go to the switch's two poles; its contacts are cross-connected so that a motor M between them is fed one way in one switch position and the other way in the other, with a push switch in each of the top and bottom lines."),
    'technology-2023-OL-scheme-secC-q3b-i': (14, (351, 256.5, 552, 354.5),
        "The marking scheme's own answer to 2023 OL Section C Q3(b)(i), as the State Examinations Commission printed it: two network diagrams. Star Topology: six devices (Device 1 to Device 6), each linked by its own line to a central hub. Ring Topology: six devices linked one to the next in a closed circle."),
    'technology-2023-OL-scheme-secC-q5b-ii': (16, (469.5, 285.5, 562.5, 404.3),
        "The marking scheme's own answer to 2023 OL Section C Q5(b)(ii), as the State Examinations Commission printed it: photographs of three steel wire-rope ends with fittings, two forked clevis ends with cross pins and one eye socket with a pin, the kind of sling end that bolts to a bracket on the deck."),
    'technology-2024-HL-scheme-secA-q15': (8, (145, 573, 315, 709),
        "The marking scheme's own answer to 2024 HL Section A Q15, as the State Examinations Commission printed it: three orthographic views of the fireside stool drawn in blue line. A front elevation shows the overhanging top and tapered splayed legs joined by a low shelf rail, an end elevation shows the tapered side panel with an arched cut-out at its foot, and a plan below shows the rectangular top with dashed hidden lines for the legs and shelf."),
    'technology-2024-HL-scheme-secB-q2c-i': (10, (70, 44, 534, 218),
        "The marking scheme's own answer to 2024 HL Section B Q2(c)(i), as the State Examinations Commission printed it: on the left a photograph of a red tubular motor fitted into the end of a grey roller blind tube, with a red arrow and the caption 'Electric motor directly connected to blinds.'; on the right a circuit with a motor M at the top connected through a DPDT change-over switch to a battery, labelled Motor, DPDT c/o switch and Power, captioned 'A relay can be used for higher voltages (including mains)'."),
    'technology-2024-HL-scheme-secB-q3b-i': (11, (115, 272, 505, 439),
        "The marking scheme's own answer to 2024 HL Section B Q3(b)(i), as the State Examinations Commission printed it: a wiring diagram of the e-bike charging system. A solar panel is wired through a solar panel control unit and a current sensor to a pair of batteries; a mains charger is plugged into the motor controller, which is also wired to the batteries and drives the e-bike. Labels: Solar panel, Mains charger, Motor, e-bike, Solar panel control, Battery."),
    'technology-2024-HL-scheme-secB-q3b-ii': (11, (347, 578, 522, 656),
        "The marking scheme's own answer to 2024 HL Section B Q3(b)(ii), as the State Examinations Commission printed it: a rendering of a hollow bicycle frame folded and pressed from sheet metal, two triangular frame halves joined at a central node, with no welded tube joints."),
    'technology-2024-HL-scheme-secB-q3c-ii': (12, (77, 273, 557, 435),
        "The marking scheme's own answer to 2024 HL Section B Q3(c)(ii), as the State Examinations Commission printed it: a comparison table with columns Fabrication, Integration of features and Aesthetic appeal. Tubular metal: cut and weld, time consuming for large production; space for features can be added or cut out of tubes; welding of tubes can be unsightly or a feature on some metals e.g. stainless steel. Carbon fibre: can be shaped in a single piece; features can be integrated into design shape; finish can be coloured, tactile material."),
    'technology-2024-HL-scheme-secC-q1d-i': (14, (143, 322, 484, 527),
        "The marking scheme's own answer to 2024 HL Section C Q1(d)(i), as the State Examinations Commission printed it: a pneumatic circuit. A double-acting cylinder at the top, labelled 'Double acting cylinder', is piped from both ends to a 5/2 valve below, which has a push-button actuator on the left and a spring return on the right, and is labelled '5/2 valve allow the cylinder to move back and forth'. A flow control valve with a bypass check valve sits in the line to the cylinder's rear port, and a red arrow from the lower left points to it."),
    'technology-2024-HL-scheme-secC-q2b-iii': (15, (111, 635, 514, 721.5),
        "The marking scheme's own answer to 2024 HL Section C Q2(b)(iii), as the State Examinations Commission printed it: four numbered sketches of soldering a component pin to a PCB pad. 1, 'Soldering iron heats the pad and component pin'; 2, 'Solder is introduced'; 3, 'Solder build-up', showing a cone-shaped joint; 4, 'Allow to cool'."),
    'technology-2024-HL-scheme-secC-q5b-ii': (23, (128, 447, 532, 587),
        "The marking scheme's own answer to 2024 HL Section C Q5(b)(ii), as the State Examinations Commission printed it: a cross-section of an injection moulding machine. Plastic granules fall from a hopper into a barrel containing a screw; heaters around the barrel melt the polymer, which is forced through a nozzle into a mould cavity between the casing mould halves, one held on a moveable plate. Labels: plastic granules, hopper, heaters, mould cavity, casing mould, Screw, barrel, nozzle, moveable plate."),
    'technology-2024-HL-scheme-secC-q5d-ii': (24, (107, 517, 524, 636),
        "The marking scheme's own answer to 2024 HL Section C Q5(d)(ii), as the State Examinations Commission printed it: two vacuum-forming sketches. Left: a red heated plastic sheet, with heat lines above it, is held above a raised mould on the machine bed; labels 'Heated plastic sheet' and 'mould'. Right: the sheet is clamped at both ends and drawn down tightly over the mould; labels 'clamp' and 'Air is vacuum drawn' at an outlet below the bed."),
    'technology-2025-HL-scheme-secA-q11': (6, (78, 180, 574, 410),
        "The marking scheme's own answer to 2025 HL Section A Q11, as the State Examinations Commission printed it: a Work Breakdown Structure tree of blue-outlined boxes. Bench at the top branches into 1. Research and design, 2. Select materials and 3. Make the product. 3. Make the product branches into 3.1 Cut composite pieces to size (then Drill bolt holes), 3.2 Produce concrete leg moulds (then Pour concrete into moulds, then Remove concrete legs) and 3.3 Assemble legs and composite parts with bolts. The scheme heads it: Suggested solution – alternative formats acceptable."),
    'technology-2025-HL-scheme-secA-q13': (7, (345.5, 130, 517, 279),
        "The marking scheme's own answer to 2025 HL Section A Q13, as the State Examinations Commission printed it: a colour photograph of a pale green diving springboard over a pool. Its rear end rests on a white toothed adjusting wheel mounted in a low stand, and a red arrow points to the wheel."),
    'technology-2025-HL-scheme-secA-q15': (7, (250, 526, 533, 736),
        "The marking scheme's own answer to 2025 HL Section A Q15, as the State Examinations Commission printed it: an exploded line drawing of a butt hinge, each part ringed by a soft pink outline and labelled in bold. Hinge plate 1, on the left, is a plate with screw holes and three knuckles. The Hinge pin stands apart in the middle as a long thin rod with a round head, with a small round cap drawn below the left plate. Hinge plate 2, on the right, is a plate with screw holes and two knuckles. Pink leader lines join the labels Hinge plate 1 and Hinge plate 2 to their parts."),
    'technology-2025-HL-scheme-secB-q2d-i': (9, (194, 514, 429, 642),
        "The marking scheme's own answer to 2025 HL Section B Q2(d)(i), as the State Examinations Commission printed it: a colour photograph of a green Xyloband with a pale woven strap looped through a green buckle. A red arrow runs to the buckle from the annotation: Tightness can be adjusted. Fast secure locking buckle."),
    'technology-2025-HL-scheme-secB-q3c-ii': (11, (74, 251, 560, 425),
        "The marking scheme's own answer to 2025 HL Section B Q3(c)(ii), as the State Examinations Commission printed it, under the heading Suggested solutions, alternatives accepted. On the left, a line drawing of a seated rider on the personal pod, with curved orange arrows at the front and rear wheels and two red arrows to the pivot points. It is annotated: The personal pod has two pivot points that allow the device to fold in the directions shown. A red block arrow leads to a photograph of the pod folded upright with its rear wheels tucked in. On the right, a photograph of an R clip and pin, annotated: R Clip and Pin to secure the wheels in place when in use."),
    'technology-2025-HL-scheme-secC-q1b-i': (12, (308, 312, 560, 652),
        "The marking scheme's own answer to 2025 HL Section C Q1(b)(i), as the State Examinations Commission printed it: a flowchart from Start through Touch screen ON and Place item on conveyor to the decision Barcode read. Its No branch goes to a Reject box; its Yes branch reaches the decision Is it a plastic bottle?. That decision's Yes branch goes to Send to servo 1 and its No branch to the decision Is it an aluminium can?, whose No branch loops back above that decision. Its Yes branch runs Send to servo 2 and Stop/Print voucher, which loops back to above Touch screen ON. A red arrow labelled Modification points at the Reject box. The scheme prints beside it: Suggested solution, Alternatives accepted:"),
    'technology-2025-HL-scheme-secC-q1c-i': (13, (369.5, 122, 547, 261),
        "The marking scheme's own answer to 2025 HL Section C Q1(c)(i), as the State Examinations Commission printed it: two cut-away pneumatic cylinders. Above, a single-acting cylinder with a spring around the piston rod and one port at the left, labelled Air. Below, a double-acting cylinder with no spring and a port at each end, labelled Air in pushes piston out under the left port and Air then returns piston under the right."),
    'technology-2025-HL-scheme-secC-q2c-ii': (15, (235, 289, 404, 540),
        "The marking scheme's own answer to 2025 HL Section C Q2(c)(ii), as the State Examinations Commission printed it: a truth table headed A, B, C, D, E in yellow, with alternate rows shaded green. It has fifteen rows from 0 0 0 0 to 1 1 1 1; the scheme leaves out the row A=0, B=1, C=1, D=0. E is 1, in bold, only in the rows 1 0 1 1, 1 1 0 1 and 1 1 1 1, and 0 in every other row."),
    'technology-2025-HL-scheme-secC-q3b-i': (16, (107, 298, 405, 448),
        "The marking scheme's own answer to 2025 HL Section C Q3(b)(i), as the State Examinations Commission printed it: a wireless network diagram in blue and orange on a grey panel. A globe labelled Internet connection is wired down to a box labelled Router, which is wired to an orange box with radio waves, labelled Wireless access point. Dashed lines fan out from it to a laptop, a phone and a desktop monitor, labelled Wireless."),
    'technology-2025-HL-scheme-secC-q5b-ii': (20, (60, 402, 528, 516),
        "The marking scheme's own answer to 2025 HL Section C Q5(b)(ii), as the State Examinations Commission printed it, titled Blow moulding: six stages left to right. A navy split mould with an orange plastic tube lowered into it is labelled Plastic tube (Parison) inserted from extruder. Heat marks at the top are labelled Heat to soften. In the next stages the tube swells to fill the bottle-shaped cavity, labelled Air blown in. The mould opens, and a separate orange bottle is labelled Finished product."),
    'technology-2025-OL-scheme-secB-q3b-i': (8, (358, 254, 519, 285),
        "The marking scheme's own answer to 2025 OL Section B Q3(b)(i), as the State Examinations Commission printed it: a diagram of compression. A grey rectangular bar has a red arrow at each end pointing inward, pushing on the bar from both sides."),
    'technology-2025-OL-scheme-secC-q1b-i': (9, (342, 329, 558, 626),
        "The marking scheme's own answer to 2025 OL Section C Q1(b)(i), as the State Examinations Commission printed it: a flowchart. A green Start box leads to the purple decision Button, whose N branch loops back up the right-hand side to Start. Its Y branch runs Gate opens, Wait 30, then a dashed decision Object?, whose dashed Y branch goes left to a red Stop box. Its N branch continues to Gate closes and Wait 10, which loops back up the right-hand side to Start. The dashed decision and the Stop box are the modification the scheme gives for part (iii)."),
    'technology-2025-OL-scheme-secC-q1b-iii': (9, (309, 496, 562, 654),
        "The marking scheme's own answer to 2025 OL Section C Q1(b)(iii), as the State Examinations Commission printed it: the lower part of its flowchart. After Wait 30, a dashed decision Object? sends a dashed Y branch to a red Stop box, and its N branch runs on to Gate closes and Wait 10, which loops back up. The scheme prints beneath it: Any valid alternative solution accepted."),
    'technology-2026-HL-scheme-secB-q2b-i': (9, (330, 335, 475, 451),
        "The marking scheme's own answer to 2026 HL Section B Q2(b)(i), as the State Examinations Commission printed it: a photograph of a 3D construction printer standing in a white room: a rectangular gantry of aluminium lattice towers and beams, with the print-head carriage hung from a lattice platform that spans the frame between the towers and can travel up and down them."),
    'technology-2026-HL-scheme-secB-q2b-iii': (9, (100, 578, 536, 714),
        "The marking scheme's own answer to 2026 HL Section B Q2(b)(iii), as the State Examinations Commission printed it: two sketches of triangulated frames. On the left a Warren truss, a long beam of equal triangles between a top and a bottom chord. On the right a roof truss resting on two hatched supports, with a vertical member from the apex to the middle of the bottom chord: an arrow labelled 'load' presses down on the apex, arrows along both sloping members are labelled 'compression', and outward arrows along the bottom chord are labelled 'tension'."),
    'technology-2026-HL-scheme-secB-q2d-i': (10, (438, 317, 537, 410),
        "The marking scheme's own answer to 2026 HL Section B Q2(d)(i), as the State Examinations Commission printed it: a close-up photograph of a 3D printer's heated nozzle, under a metal print head with a yellow hot-surface warning sticker, depositing material on top of a black cone-shaped object built up from many thin horizontal layers."),
    'technology-2026-HL-scheme-secB-q3b-i': (11, (389.9, 279, 552, 370),
        "The marking scheme's own answer to 2026 HL Section B Q3(b)(i), as the State Examinations Commission printed it: a cut-away photograph of a worm gearbox, its green and red housing opened to show a horizontal worm screw meshing with a large worm wheel under a vertical output shaft. An arrow labelled 'Worm gear' points to the worm, and an arrow labelled 'Motor drive' points to the input shaft sticking out to the right."),
    'technology-2026-HL-scheme-secC-q1b-i': (13, (228, 333.5, 540, 590),
        "The marking scheme's own answer to 2026 HL Section C Q1(b)(i), as the State Examinations Commission printed it: a flowchart. A green Start terminal leads to the process boxes 'Move to a shelf', 'Turn on camera' and 'Scan stock', then a decision diamond 'Is stock full'. Its No branch goes right to 'Send alert'; its Yes branch goes down to 'Move to next shelf', from which a line runs back up the left side to re-enter above 'Move to a shelf'. Beside it: 'Suggested solution, Alternatives accepted:'."),
    'technology-2026-HL-scheme-secC-q1c-ii': (14, (145, 211, 523, 428),
        "The marking scheme's own answer to 2026 HL Section C Q1(c)(ii), as the State Examinations Commission printed it: a pneumatic circuit. A double-acting cylinder at the top, annotated 'Attach piston to cylinder', has both ports piped down through a flow control valve each (a check valve beside an adjustable restrictor), annotated 'Flow control valves to control the speed of the ram.', to a 5/2 valve at the bottom with a push-button actuator on the left, spring return on the right and exhaust ports below, annotated '5/2 valve allow the cylinder to move back and forth.'"),
    'technology-2026-HL-scheme-secC-q2a-i': (15, (90, 171, 432.6, 268.5),
        "The marking scheme's own answer to 2026 HL Section C Q2(a)(i), as the State Examinations Commission printed it: a logic circuit. Inputs 'Fingerprint sensor' and 'PIN Code' feed an OR gate; the OR gate's output and the input 'Power Level' feed an AND gate, whose output goes to 'Unlock'."),
    'technology-2026-HL-scheme-secC-q4d': (20, (324.6, 409, 553, 766),
        "The marking scheme's own answer to 2026 HL Section C Q4(d), as the State Examinations Commission printed it: three layout diagrams, one above the other. The product layout is a line of stations joined by arrows: 'Assemble chassis', 'Install circuit board', 'Install flat screen', 'Install speakers', 'Final Assembly' and 'Inspected by' (a red '42' inspection stamp). The process layout is a floor plan of departments side by side, 'Receiving and raw materials storage', 'Foundry', 'Rough machine', 'Fabrication', 'Painting', 'Packaging and shipping', with 'Shear and punch', 'Finish machine', 'Debur' and 'Assembly' below, and numbered blue and red production operations joined by arrows; a key reads 'Product or material flow' and 'Production operations'. The fixed position layout shows a large round structure at the centre with arrows pointing in from the people and resources brought to it: 'General contractor', 'Architect', 'Mechanical contractor', 'Electrical contractor', 'Plumbing contractor', 'General labor', 'Equipment (bulldozers, cranes, etc)' and 'Materials (steel, glass, cement, etc.)'."),
    'technology-2026-OL-scheme-secC-q1b-iii': (9, (40, 340, 180, 745),
        "The marking scheme's own answer to 2026 OL Section C Q1(b)(iii), as the State Examinations Commission printed it: the scheme's flowchart for the turntable, with the melody added in dashed, lighter boxes: Start, a 'Button?' decision (N loops back to Start, Y continues), LEDs On, Wait 2, Motor On, the dashed 'Melody On', Wait 15, LEDs Off, Motor Off, the dashed 'Melody Off', then a line back up to Start."),
    'technology-2026-OL-scheme-secC-q1c-ii': (10, (91, 205.2, 245, 331),
        "The marking scheme's own answer to 2026 OL Section C Q1(c)(ii), as the State Examinations Commission printed it: a line sketch of a robot on a base with an upright column, a horizontal arm and a gripper, drawn beside a large transparent box that marks the work envelope, the space the gripper can reach."),
})

# Scheme regions whose words are a drawing's labels, not published as a crop.
LABEL_ZONES = {
    (2026, 'hl'): [
        # Page 4: the circuit reprinted beside Q3's potential-divider working.
        (3, (368, 545, 552, 662)),
        # Page 6: the lever diagram reprinted beside 9(i)'s worked calculation.
        (5, (340, 528, 548, 634)),
        # Page 10: the triangulated roof sketch under 2(b)(iii), its load,
        # compression and tension arrows lettered.
        (9, (300, 580, 525, 710)),
        # Page 12: the worm-gear picture beside 3(b)(i), lettered Worm gear
        # and Motor drive.
        (11, (395, 275, 548, 352)),
    ],
    (2026, 'ol'): [
        # Page 5: the lever diagram beside 6(ii)'s calculation (40 N, F, 1M, 4M).
        (4, (80, 580, 262, 700)),
        # Page 6: the saucepan photograph beside 7(i), captioned Handle.
        (5, (418, 48, 562, 176)),
        # Page 10: the flowchart in the margin of Option 1(b).
        (9, (40, 340, 180, 745)),
        # Page 12: the dark-sensing circuit beside 2(b), lettered A and B.
        (11, (425, 228, 562, 352)),
        # Page 14: the life-cycle graph beside 4(b), lettered 1 2 3 4, Sales, Time.
        (13, (40, 228, 228, 348)),
        # Page 15: the coffee-table photograph beside 5(b), captioned Leg assembly.
        (14, (445, 236, 548, 370)),
    ],
}

# Solution crops that ARE the whole answer: the scheme answers in a TABLE,
# whose cells the text layer reads column by column into lines no student
# could claim ("Air transport Approx. 2% of global CO2 Nitrogen oxides...").
# The card's one row is the ask and the reveal shows the table itself.
ASK_ONLY = {
    'technology-2026-HL-scheme-secB-q3d',
    'technology-2026-HL-scheme-secC-q5d',
}

# What the scheme says each printed letter is, for an ask that names labelled
# parts ("Name component A and component B"): the card needs the picture AND
# the letters decoded (build-deck's namesLetters gate), and the decoding is the
# scheme's own words for each letter, lifted from its page by the residue
# authors. Keyed by (year, level, section, q, letter).
LABEL_KEYS = {}

# Boxes blanked to white inside a BY_EYE crop before it is rendered: where
# the paper's prose wraps around a picture, no rectangle holds the picture
# whole without the ends of a few prose lines on the white ground beside it
# (2020 Higher's lamp and its inset). key -> [rect, ...], in PDF points.
WHITEOUT = {}

# Lettering printed on a PAPER page beside the prose the walker read it into
# (2025 Higher Q13's "Ladder Springboard Tilt Angle" after its ask): the words
# inside these come off a stem or ask the same way a crop's own do, for any
# card whose crop is on that page. (year, level, booklet) -> [(page, rect)].
PAPER_ZONES = {}

# A part whose drawn answer the scheme prints INSIDE a sibling's crop: 2025
# Higher 1(b)(ii)'s modification is drawn on the 1(b)(i) flowchart. The
# part's card binds the sibling's crop (its rows stay; the crop joins them).
# alias key (the part's own would-be key) -> the published key.
SOLUTION_SHARED = {}

# The same for a PAPER picture printed for one part and published under a
# neighbour's key (2022 Higher's Adibot photo, cut for 2(c), is what 2(b)
# names): alias key (the part's own would-be key) -> the published key.
FIGURE_SHARED = {}

# Masks the 2025 auditor asked for on two scheme crops no rectangle can keep
# clean: the ask's tail and '(6 ma' beside the hinge drawing, a sliver of the
# reprinted bench photo above the WBS tree.
WHITEOUT.update({
    'technology-2025-HL-scheme-secA-q15': [(250, 526, 350, 542), (505, 703, 533, 720)],
    'technology-2025-HL-scheme-secA-q11': [(419, 181, 470, 202)],
})

for _yl, _zs in {
    (2021, 'ol'): [
        (4, (62, 339.8, 180, 453)),  # 2021 OL Section A Q5: worm-gear photograph lettering 'A' (y 345.4) and 'B' (y 433.2) beside the reprinted Q5 ask lines; 'A' is level with '(i) Name component A and component B.' and 'B' with 'manufacturing electro-mechanical control elements' (scheme 2021-ol.pdf)
        (6, (412, 297.5, 524, 409)),  # 2021 OL Section A Q11(i): spade labels F (y 304), E (y 326), L (y 353.5) beside the (i) ask; 'L' is welded into the shipped card's only row 'fulcrum when the spade is in use. L' (scheme 2021-ol.pdf)
        (6, (376, 440, 492, 526)),  # 2021 OL Section A Q11(ii): lever-diagram lettering 50 N, 0.3 M, 0.5 M, F beside the calculation box; '50 N' (y 443.3) is level with 'F x 0.5 M = 50 N x 0.8 M'. The tariff '(4+4 marks)' (x 463.6-524.3, y 519.9-531.9) clips the zone's corner but its centre lies outside; keep it (scheme 2021-ol.pdf)
        (11, (372, 178, 560, 283)),  # 2021 OL Section C Q1(c)(i): shuttle-valve symbol lettering A (y 245.6), B (y 241.0), C (y 218.0) beside the answer prose; 'C' is level with 'and exiting at port C. If both input ports A and B' and 'A'/'B' with 'with the higher pressure takes precedence' (scheme 2021-ol.pdf)
    ],
    (2022, 'hl'): [
        (4, (472, 482, 557, 606)),  # 2022 HL scheme, Section A Q6: the reprinted question picture's letter A (text layer) sits beside the 6(i)/(ii) answers; the .md welds it onto 'A = Follower A'
        (4, (536, 608, 557, 624)),  # 2022 HL scheme, Section A Q6: the reprinted question picture's letter B (text layer) beside the 6(ii) answer; the .md welds it onto '...the follower (A) to B'
        (14, (318, 571, 574, 684)),  # 2022 HL scheme, Section C Q1(d)(i): pneumatic circuit answer with the text-layer label 'Flow control valve' printed beside the 1(d) prose; the .md puts 'Flow control valve' between the 1(d)(i) ask and (ii)
        (15, (373.5, 402.5, 541, 484)),  # 2022 HL scheme, Section C Q2(b)(ii): the truth table answer sits beside the ask; the .md welds its header 'Input 1 Input 2 Output' onto the ask line
    ],
    (2022, 'ol'): [
        (5, (48, 145, 228, 284)),  # 2022 OL scheme, Section A Q7: reprinted Stockholm chair picture with its text-layer arrow letter 'A' beside the sketch answer
        (9, (48, 379, 182, 693)),  # 2022 OL scheme, Section C Q1(b)(i) flowchart lettering (Start, On, N, Y, Motor On...) printed beside the 1(b)(ii) ask
        (9, (229, 407.5, 409, 764)),  # 2022 OL scheme, Section C Q1(b)(ii) flowchart lettering printed beside the 1(b)(iii) prose ask and answer ('Infra-red motion sensor, LDR, etc.'); the .md interleaves them line by line
        (10, (225, 240, 446, 350)),  # 2022 OL scheme, Section C Q1(c)(ii) (seen in passing, not in this input): single-acting cylinder symbol with text-layer labels Piston, A, Spring printed under the answer prose
        (10, (473, 499, 534, 527)),  # 2022 OL scheme, Section C Q1(d) (seen in passing, not in this input): caption 'Mechanical Gripper' of the reprinted question picture beside the 1(d)(i) answer
        (11, (396, 600, 558, 644)),  # 2022 OL scheme, Section C Q2(d): the reprinted logic diagram's lettering (A, B, X, C, Y, D) printed beside the (i) and (ii) asks; its B sat on the (i) ask's line
    ],
    (2023, 'hl'): [
        (13, (220, 718, 364, 770)),  # HL C1(b)(ii): mini flowchart ('Check light level' / 'No' / 'Light on' / 'Yes') under the answer 'Add light sensor check with light switching option.'; card tech-2023-hl-c1b-ii carries its lettering as two rows, 'Check light No' and 'Light on level'
        (16, (124, 80, 466.5, 252.5)),  # HL C2(b)(iii): the modified circuit's lettering (9 V, A, B, 10kΩ, IC, 0 V); card tech-2023-hl-c2b-iii carries 'B 10kΩ 0 V' as a 4-mark point
        (5, (106, 488, 497, 625.5)),  # HL A8: fishbone lettering (Machine, Environment, Propellers, Wind, Drone will not lift., Expertise, Weight, User, Materials) under 'Three appropriate factors selected. Suggested solution:' (schemes/2023-hl.md lines 156-161)
    ],
    (2023, 'ol'): [
        (13, (426, 644, 504, 732)),  # OL C2(d): transistor symbol labels C, B, E; the 'C' sits on the line of 2(d)(i)'s answer, and card tech-2023-ol-c2d-i reads 'Automatic switch, current amlifier, etc. C'
        (12, (304, 203, 444, 292)),  # OL C1(c)(ii): 'Pin 1' label on the chip sketch, under the ask
    ],
    (2024, 'hl'): [
        (4, (134, 260, 302, 338)),  # HL scheme page 4 (printed 3): the resistor photograph and its Resistor bands: Brown Black Red Gold list, reprinted beside 5(i)'s answer Value: 1000 Ω
        (4, (336, 264, 436, 372)),  # HL scheme page 4: the Tolerance code table (Brown 1%, Red 2%, Gold 5%, Silver 10%) reprinted beside 5(i); its words weld onto 'Value: 1000 Ω Silver 10% Yellow 4'
        (4, (438, 252, 542, 480)),  # HL scheme page 4: the Colour code table (Black 0 to White 9) reprinted beside 5(i) and 5(ii); its words weld onto the (ii) ask and the Maximum/Minimum value rows
        (4, (380, 558, 544, 654)),  # HL scheme page 4: the network node (EST, EFT, Task:, LST, LFT) reprinted beside Q6; it welds 'Task:' onto 'LFT: Latest Finish Time' and 'LST LFT' onto the (ii) ask
    ],
    (2024, 'ol'): [
        (5, (142, 103, 280, 247)),  # OL scheme page 5: the machine tool stand photograph and its arrow label A reprinted beside Q7; the A welds onto the tariff line '(Very good sketch- 8 marks,'
    ],
    (2025, 'hl'): [
        (12, (345, 665, 415, 766)),  # 2025 HL scheme: WHITE (invisible) flowchart text 'User stops machine' and 'End' below the drawn flowchart; nothing renders here, but the text layer carries the words next to the 1(b)(iii) answer
        (7, (384, 529, 440, 547)),  # 2025 HL scheme Q15: drawing label 'Hinge pin', on the same line as the Q15 ask
        (7, (462, 556, 534, 574)),  # 2025 HL scheme Q15: drawing label 'Hinge plate 2'
        (7, (256, 698, 298, 730)),  # 2025 HL scheme Q15: drawing label 'Hinge plate 1' (the text layer reads these three labels BEFORE Q13 on the page)
    ],
    (2025, 'ol'): [
        (14, (53, 204, 203, 355)),  # 2025 OL scheme: the 3D printer picture, lettered A to E, reprinted beside the 5(b)(i) and (ii) answers
        (11, (276, 425, 442, 486)),  # 2025 OL scheme: the logic-gate picture, lettered A, B, X, C, Y, D, reprinted beside the 2(c)(i) answer X = And Y = Not
    ],
}.items():
    LABEL_ZONES.setdefault(_yl, []).extend(_zs)
ASK_ONLY.update({
    # 2025 Higher Q7's table: its cells wrap in the text layer, so the crop is
    # the answer and the card's row is the ask.
    'technology-2025-HL-scheme-secA-q7',
    'technology-2021-HL-scheme-secC-q1b-ii',
    'technology-2021-HL-scheme-secC-q2d-i',
    'technology-2021-OL-scheme-secA-q11-i',
    'technology-2021-OL-scheme-secA-q7',
    'technology-2021-OL-scheme-secC-q1b-i',
    'technology-2021-OL-scheme-secC-q1b-ii',
    'technology-2022-HL-scheme-secA-q7',
    'technology-2022-HL-scheme-secC-q1b-i',
    'technology-2022-HL-scheme-secC-q2b-ii',
    'technology-2022-HL-scheme-secC-q2c-ii',
    'technology-2022-HL-scheme-secC-q4b-i',
    'technology-2022-OL-scheme-secA-q7',
    'technology-2022-OL-scheme-secC-q1b-i',
    'technology-2022-OL-scheme-secC-q1b-ii',
    'technology-2023-HL-scheme-secC-q1b-i',
    'technology-2023-HL-scheme-secC-q2b-iii',
    'technology-2023-HL-scheme-secC-q2d-i',
    'technology-2023-OL-scheme-secA-q7',
    'technology-2023-OL-scheme-secC-q1c-ii',
    'technology-2023-OL-scheme-secC-q2d-ii',
    'technology-2024-HL-scheme-secC-q1b-i',
    'technology-2024-HL-scheme-secC-q2b-i',
    'technology-2024-HL-scheme-secC-q4b-ii',
    'technology-2022-OL-scheme-secC-q2d-ii',
    'technology-2020-HL-scheme-secA-q11',
    'technology-2020-HL-scheme-secA-q14-ii',
    'technology-2026-HL-scheme-secA-q9-ii',
    'technology-2024-OL-scheme-secA-q7',
    'technology-2024-OL-scheme-secC-q1b-i',
    'technology-2024-OL-scheme-secC-q1b-ii',
    'technology-2025-HL-scheme-secC-q1b-i',
    'technology-2025-HL-scheme-secC-q2b-ii',
    'technology-2025-HL-scheme-secC-q2c-i',
    'technology-2025-HL-scheme-secC-q2c-ii',
    'technology-2025-OL-scheme-secA-q4',
    'technology-2025-OL-scheme-secC-q2c-ii',
})
LABEL_KEYS.update({
    (2021, 'ol', 'A', 5, None): [{'letter': 'A', 'meaning': 'Worm'}, {'letter': 'B', 'meaning': 'Worm wheel'}],
    (2021, 'ol', 'C', 1, 'c'): [{'letter': 'A', 'meaning': 'Input port'}, {'letter': 'B', 'meaning': 'Input port'}, {'letter': 'C', 'meaning': 'Output port'}],
    (2022, 'hl', 'A', 6, None): [{'letter': 'A', 'meaning': 'Follower'}, {'letter': 'B', 'meaning': 'Cam'}],
    (2023, 'hl', 'C', 2, 'b'): [{'letter': 'A', 'meaning': 'Variable Resistor'}, {'letter': 'B', 'meaning': 'Thermistor'}],
    (2025, 'ol', 'C', 5, 'b'): [{'letter': 'A', 'meaning': 'Filament spool'}, {'letter': 'B', 'meaning': 'The extruder'}, {'letter': 'C', 'meaning': 'The heater block'}, {'letter': 'D', 'meaning': 'The part'}, {'letter': 'E', 'meaning': 'The bed'}],
})

for _yl, _zs in {
    (2022, 'hl'): [
        (4, (474, 483, 557, 620)),  # 2022 HL scheme, Section A Q6: the whole cam-and-follower picture reprinted beside the 6(i)/(ii) answers (blue follower rod, spring and guide plate, green cam, two red arrows lettered A and B). It covers the A and B letters that the two existing 2022 HL page-4 zones hold. No prose inside: the 6(ii) line '...the follower (A) to' ends at x 473.1 and 'rise and fall ... contact with' starts at y 620.8.
        (22, (358, 320, 580, 433)),  # 2022 HL scheme, Section C Q5(c)(ii): the injection-moulding sketch with its labels Plastic hopper, mould, Motor drive and Heated chamber with screw, beside the answer prose. The prose runs to x 353.3 at most, and the ask line above ends at y 315.2.
    ],
    (2024, 'hl'): [
        (5, (361, 80, 570, 213)),  # 2024 HL scheme, Section A Q7: the compound gear-train picture with its labels Driven Gear and 75 Teeth and most of 15 Teeth. The (i)/(ii) ask lines end at x 359.1, so the zone starts at 361. Its two side zones below hold the labels that stand further left.
        (5, (347, 127, 390, 155)),  # 2024 HL scheme, Section A Q7: the label 'Gear A' (it lands as a row of its own in the .md). It sits above the (ii) ask line, which starts at y 156.9.
        (5, (352, 189, 405, 213)),  # 2024 HL scheme, Section A Q7: the label '15 Teeth', which welds onto 'Calculation:' with '75 Teeth'. It sits below the (ii) ask, whose last line ends at y 187.7.
        (22, (360, 319, 557, 459)),  # 2024 HL scheme, Section C Q4(d): the lifecycle graph reprinted beside (ii)'s answer, with stage letters A, B, C and the axis label Time. 'Time' welds onto 'Enhanced features may have been added.' The scheme reprints one graph only, the updated lifecycle. The prose word 'at' ends at x 357.9, and the 'marketing campaign.' line starts at y 459.1.
        (22, (350, 333, 368, 364)),  # 2024 HL scheme, Section C Q4(d): the graph's rotated y-axis label 'Sales', which welds into 'Sales A B C'. It is a separate rectangle because the prose word 'at' (x 348.2-357.9, y 365.4+) sits directly below it.
    ],
    (2024, 'ol'): [
        (11, (397, 640, 530, 699)),  # 2024 OL scheme, Section C Q2(d)(ii): the partial circuit (8 Ω in series with two 10 Ω in parallel) beside the calculation. It welds as 'R = 5 Ω 8 Ω', '= 13 Ω 10 Ω' and '...circuit shown. 10 Ω'. The ask word 'shown.' ends at x 395.9.
    ],
    (2025, 'hl'): [
        (6, (394, 474, 574, 612)),  # 2025 HL scheme, Section A Q12: the resistor network R1 = 6kΩ, R2 = 8kΩ, R3 = 4kΩ, R4 = 12kΩ beside the calculation box. The box border is at x 388.5.
        (10, (379, 379, 540, 514)),  # 2025 HL scheme, Section B Q3(b): the gearbox graphic with labels D, B, motor, A, output, C beside (ii)'s calculation. 'output C' welds onto '... x 630'. The (i) answer line above ends at y 376.2.
        (12, (311, 313, 438, 639)),  # 2025 HL scheme, Section C Q1(b)(i): the flowchart ONLY, part 1 of 2. This is the main column (Start to Stop/Print voucher), with its left return loop, its Yes/No labels and the aluminium-can No loop. It replaces the zone [308,312,560,652]. The hidden-text zone [345,665,415,766] stays as it is.
        (12, (431, 430.5, 497, 506)),  # 2025 HL scheme, Section C Q1(b)(i): the flowchart ONLY, part 2 of 2. These are the side boxes Reject and Send to servo 1, split off so the zone holds neither the Modification label above nor the caption below.
        (12, (478, 398, 558, 431)),  # 2025 HL scheme, Section C Q1(b): the drawing's own label 'Modification' and its red arrow to the Reject box. It is separate from the flowchart zone, so it can be dropped if unwanted. Without it, a stray 'Modification' line stays in the text.
        (12, (446, 619, 571, 654)),  # 2025 HL scheme, Section C Q1(b): the flowchart's caption 'Suggested solution, Alternatives accepted:'. It is separate from the flowchart zone. Without it, the caption welds onto the 1(b)(iii) answer ('LDR and LED voucher Suggested solution,' / 'Distance/Motion sensor. Alternatives accepted:').
    ],
}.items():
    LABEL_ZONES.setdefault(_yl, []).extend(_zs)
ASK_ONLY.update({
    'technology-2021-OL-scheme-secB-q2b-ii',
    'technology-2022-HL-scheme-secA-q10',
    'technology-2022-HL-scheme-secB-q3b-ii',
    'technology-2022-HL-scheme-secC-q2d-i',
    'technology-2022-OL-scheme-secA-q8',
    'technology-2023-OL-scheme-secC-q2b-ii',
    'technology-2024-HL-scheme-secA-q8',
    'technology-2024-HL-scheme-secC-q2d-i',
    'technology-2024-OL-scheme-secA-q4-ii',
    'technology-2024-OL-scheme-secB-q3b-iii',
    'technology-2024-OL-scheme-secC-q2b-iii',
    'technology-2025-HL-scheme-secA-q15',
    'technology-2025-HL-scheme-secA-q7',
    'technology-2025-OL-scheme-secA-q9',
    'technology-2025-OL-scheme-secC-q2b-ii',
    'technology-2025-OL-scheme-secC-q2d-ii',
})
LABEL_KEYS.update({
})

# 2022 Higher Option 1(d)(i): the scheme answers with a pneumatic circuit (a
# double-acting cylinder, two flow control valves, a 5/2 valve and two 3/2
# valves); the "Flow control valve" label stands in the prose column and is
# left to the label zone beside it.
SOLUTIONS['technology-2022-HL-scheme-secC-q1d-i'] = (14, (412, 518, 575, 684),
    "The marking scheme's own answer to 2022 HL Section C Q1(d)(i), as the State "
    "Examinations Commission printed it: a pneumatic circuit in which a "
    "double-acting cylinder is fed through two flow control valves from a 5/2 "
    "valve, itself piloted by two spring-return 3/2 push-button valves.")
ASK_ONLY.add('technology-2022-HL-scheme-secC-q1d-i')

# 2020 Higher, measured on the rendered scheme pages after the first pass.
LABEL_ZONES.setdefault((2020, 'hl'), []).extend([
    # Page 5: the potential-divider circuit reprinted beside 5(i)'s working.
    (4, (428, 352, 562, 498)),
    # Page 8: the analytics graph and its figures above Q12's terms.
    (7, (130, 128, 460, 208)),
])
SOLUTIONS.update({
    'technology-2020-HL-scheme-secA-q7': (5, (80, 104, 472, 162),
        "The marking scheme's own answer to 2020 HL Section A Q7, as the State "
        "Examinations Commission printed it: a work breakdown structure of four "
        "boxes in a row joined by arrows, Mark out sheet material, Cut sheet "
        "material, Edge finish sheet material and Bend sheet material."),
    'technology-2020-HL-scheme-secA-q13': (7, (222, 505, 440, 672),
        "The marking scheme's own answer to 2020 HL Section A Q13, as the State "
        "Examinations Commission printed it: a red arrow pointing at the "
        "assembled bulb, drawn as a shaded pictorial view with its dome, finned "
        "body and screw cap together."),
    'technology-2020-HL-scheme-secB-q2d-i': (10, (378, 560, 535, 658),
        "The marking scheme's own answer to 2020 HL Section B Q2(d)(i), as the "
        "State Examinations Commission printed it: a product life cycle graph of "
        "sales against time, a curve rising, peaking and falling with the four "
        "stages marked off by dashed lines."),
})
ASK_ONLY.update({
    'technology-2020-HL-scheme-secA-q7',
    'technology-2020-HL-scheme-secA-q13',
    'technology-2020-HL-scheme-secB-q2d-i',
})
# The analytics table 12's terms refer to, cut from the paper.
BY_EYE['technology-2020-HL-paper-secA-q12-art'] = ('014', 5, (82, 138, 532, 192))

SOLUTIONS['technology-2020-HL-scheme-secC-q1d-i'] = (13, (72, 335, 562, 492),
    "The marking scheme's own answer to 2020 HL Section C Q1(d)(i), as the State "
    "Examinations Commission printed it: a pneumatic circuit with a double-acting "
    "cylinder fed through two flow control valves from a 5/2 valve with its air "
    "inlet, and beside it an alternative solution, the cylinder driven by two "
    "spring-return 3/2 valves.")
ASK_ONLY.add('technology-2020-HL-scheme-secC-q1d-i')

# 2020 Higher Option 4(b)(i): the cost graph is the scheme's answer to "Draw a
# graph"; the BEQ working beneath it stays as rows, so the crop is not ask-only.
SOLUTIONS['technology-2020-HL-scheme-secC-q4b-i'] = (16, (88, 330, 500, 552),
    "The marking scheme's own answer to 2020 HL Section C Q4(b)(i), as the State "
    "Examinations Commission printed it: a graph of Cost against Quantity, a red "
    "Skilled Labour line from the origin and a green Unskilled Labour line from "
    "about 3,300, crossing at the BEQ marked with a dashed line between 1,250 and "
    "2,500.")

# 2020 Higher Option 5(b)(ii): the injection-moulding sketch beside the answer
# prose, its labels (Plastic hopper, mould, Motor drive, Heated chamber with
# screw drive) welded onto the lines; shown at the reveal beside the rows.
SOLUTIONS['technology-2020-HL-scheme-secC-q5b-ii'] = (18, (383, 292, 582, 382),
    "The marking scheme's own answer to 2020 HL Section C Q5(b)(ii), as the State "
    "Examinations Commission printed it: a sectioned injection moulding machine "
    "labelled Plastic hopper, mould, Motor drive and Heated chamber with screw "
    "drive.")

# 2023 Ordinary: the perceptual map beside Option 4(a), whose axis words and
# letters A, B and C were welded onto both parts' lines.
LABEL_ZONES.setdefault((2023, 'ol'), []).append((15, (428, 92, 592, 228)))
LABEL_KEYS[(2023, 'ol', 'C', 4, 'a')] = [
    {'letter': 'A', 'meaning': 'Low cost/high quality, likely to sell.'},
    {'letter': 'B', 'meaning': 'High cost/high quality, likely to sell but cost could impede sales.'},
    {'letter': 'C', 'meaning': 'Low cost/low quality, poor sales likely as a result'},
]

for _yl, _zs in {
    (2021, 'hl'): [
        (11, (440, 200, 578, 356)),  # 2021 HL Section B Q2(c)(ii): tilting-screen drawing lettering 'Mounting plate' (y 207) and 'Motor with screw mechanism' (y 322-349) beside the prose 'As the motor turns the screw, the wedge will make the screen tilt.'; 'Motor with screw mechanism' is welded into the card's only row. The prose ends at x 421.3, left of the zone.
        (21, (203, 292, 375, 383)),  # 2021 HL Section C Q4(d)(i): product life cycle chart lettering 'sales' (y 296), 'A B C D' (y 314) and 'time' (y 374-386) beside the reprinted 'Explain each stage of the chart' (x 85.8-229.5, y 378.4-390); 'sales' and 'time' are shipped as rows. y1 383 keeps the reprint's centre (y 384.2) outside the zone; the reprint row must be dropped separately.
        (22, (358, 333, 562, 427)),  # 2021 HL Section C Q5(b)(ii): injection-moulding drawing lettering 'Plastic hopper' (y 337), 'mould' (y 357), 'Motor' (y 371), 'drive' (y 385), 'Heated chamber with screw' (y 414) beside the prose; 'Motor' and 'drive' are welded into the prose row and the other two are rows. The prose ends at x 355.8.
    ],
    (2021, 'ol'): [
        (8, (466, 172, 533, 190)),  # 2021 OL Section B Q2(a)(ii): the scheme photo's caption 'Support legs' (x 469.4-530.2, y 175.2-187.2) level with the answer 'Aluminium, ABS– lightweight, strong, etc.'; it is welded onto the end of the card's only row.
        (11, (292, 570, 470, 676)),  # 2021 OL Section C Q1(d)(ii): gripper photo lettering 'Jaw' (y 574), 'Parallel linkage' (y 591-619), 'Gear' (y 644), 'Mechanical gripper' (y 661) below the prose 'Any relevant example with a description, etc.' (y 522-534); 'Parallel linkage' and 'Gear' ship as rows.
        (12, (405, 200, 585, 398)),  # 2021 OL Section C Q2(b): circuit lettering R (y 276), C (y 271), B (y 313), A (y 348) beside the (ii) prose; R, C and B are welded into the (ii) rows. The prose ends at x 399.9.
        (12, (336, 200, 353, 218)),  # 2021 OL Section C Q2(b): the circuit's '+V' (x 339.3-351, y 205-216), level with '(i) ... B: Transistor' (ends x 320.3); welded onto the (i) row.
        (12, (336, 384.6, 353, 398)),  # 2021 OL Section C Q2(b): the circuit's '0V' (x 339.3-351.2, y 385-396), level with the wrapped ask tail 'closed.' (x < 160); shipped as the (iii) row 'closed. 0V'.
        (12, (134, 579, 171, 609)),  # 2021 OL Section C Q2(c): the scheme photo's callout 'Fuse in holder' (x 136.9-168.2, y 581.9-606.5); shipped as the (ii) card's row 3.
        (15, (538, 305, 556, 324)),  # 2021 OL Section C Q5(b)(i): an invisible white 'A' (Calibri-Bold 14, colour #FFFFFF, x 541.2-552.8, y 308.2-322.2) level with 'chips or solid'; welded into the card's row as '...chips or solid A timber...'.
    ],
    (2022, 'hl'): [
        (7, (70, 140, 310, 312)),  # crane diagram lettering (9850 kg, 4.1m, 7.6m) beside 12(i); the .md welds '4.1m 7.6m' onto the row 'Load × 7.6 = 40,385'
        (10, (80, 146, 270, 246)),  # product life cycle graph lettering (Sales, 1 2 3 4, Time) beside 2(c)(i); the .md welds it into the four stage rows
        (10, (500, 470, 552, 532)),  # label 'Fibre layers in bonding plastic' beside 2(d)(i); the .md interleaves it word by word with the answer lines
        (10, (376, 606, 562, 694)),  # laminated-glass diagram labels (Glass, Interlayer, Glass) beside 2(d)(ii); the .md interleaves them with the answer lines
        (21, (360, 505, 460, 671)),  # impact-tester photo labels (Striker at a predetermined height. / Dial records energy expended, or distance moved by striker / Clamping device for each material) beside 5(b)(ii); the .md interleaves them with the answer lines
        (22, (100, 145, 522, 161)),  # captions 'Corrugated sheet', 'Fibre-reinforcement', 'Impact of ribbed products' under the 5(b)(iii) pictures; the .md makes them a row
    ],
    (2022, 'ol'): [
        (11, (385, 242, 569, 382)),  # redrawn 2(b) circuit lettering (6V, V, A, C, B, 0V) beside 2(b)(i)-(iii); the .md welds 'V' onto the 2(b)(i) row and '0V' onto the 2(b)(iii) ask reprint
        (11, (452, 146, 468, 164)),  # resistor label 'R' beside 2(a)(i); the .md welds it onto the row '1000Ω'
        (14, (474, 310, 556, 414)),  # reprinted 5(b) photograph with its panel labels A and B beside 5(b)(i); the .md welds 'A' onto the row
    ],
    (2023, 'hl'): [
        (5, (150, 446, 470, 688)),  # 014 booklet: wind turbine drawing lettering (Rotor, Nacelle (contains gears and generator), Cylindrical tower) for Section A Q9
        (6, (88, 78, 500, 182)),  # 014 booklet: compound gear train lettering (Gear B (24 teeth), Gear C (8 teeth), Gear D (24 teeth), Driver Gear A (8 teeth) (450 RPM)) for Section A Q10
        (1, (425, 395, 560, 414)),  # 039 booklet: 'Replaceable battery pack' label under the 2(b) drone photo (leaked into the 2(d) stem)
        (1, (380, 508, 540, 612)),  # 039 booklet: product lifecycle graph lettering '1 2 3 4', 'Sales', 'Time' for 2(c) (leaked into the 2(d) stem)
        (2, (355, 366, 505, 386)),  # 039 booklet: 'Robot casing' and 'Robot arm' labels under the 3(b) photo
        (10, (400, 84, 546, 178)),  # SCHEME page: lifecycle graph lettering '1 2 3 4', 'Sales', 'Time' beside 2(c)(i) ('Time' leaked into the 2(c)(i) row)
        (6, (61, 515.5, 539, 579.5)),  # 039 booklet: 4(b) defects table cells (leaked into the 4(b) stems)
        (19, (149, 497, 426, 676)),  # SCHEME page: control chart lettering 0-14, Control chart, UCL, Mean, LCL beside 4(b)(ii) (leaked into the 4(b)(ii) row)
        (22, (387, 89, 553, 187)),  # SCHEME page: snap-fit sketch labels 'Casing', 'Base of mouse' beside 5(b)(iii) (leaked into its rows)
        (9, (240, 500, 522, 621)),  # SCHEME page: exploded battery-compartment labels housing, connector, batteries, Cover to click into place keeping batteries secure (became the 2(b)(ii) rows)
        (11, (110, 333, 577, 493)),  # SCHEME page: robot-arm annotations and 'Alternative solutions acceptable' box beside 3(b)(i) (interleaved into its rows)
    ],
    (2023, 'ol'): [
        (9, (447, 252, 550, 357)),  # SCHEME page: oak-tree photo with its printed caption 'Irish Oak' beside 2(b) (caption leaked into the 2(b)(ii) row)
    ],
    (2024, 'hl'): [
        (4, (135, 262, 302, 338)),  # 2024 HL scheme p4: Q5 reprint of the 'Resistor bands: Brown Black Red Gold' list and resistor photo beside 5(i)'s answer
        (4, (336, 266, 436, 372)),  # 2024 HL scheme p4: Q5 reprint of the Tolerance code table
        (4, (452, 252, 542, 480)),  # 2024 HL scheme p4: Q5 reprint of the Colour code table beside 5(ii)'s answer
        (4, (384, 560, 542, 652)),  # 2024 HL scheme p4: Q6 reprint of the network node (EST EFT Task: LST LFT) beside 6(i)'s answer
        (5, (347, 80, 570, 152)),  # 2024 HL scheme p5: Q7 gear-train reprint lettered 'Driven Gear' and 'Gear A' beside 7(i)
        (5, (357, 186, 570, 213)),  # 2024 HL scheme p5: Q7 gear-train reprint lettered '15 Teeth' and '75 Teeth' beside 7(ii)'s working
        (6, (88, 105, 528, 170)),  # 2024 HL scheme p6: Q9 reprint of the LED voltage-drop table
        (7, (265, 400, 360, 434)),  # 2024 HL scheme p7: Q12 photo caption 'alternator bracket for a vintage car'
        (22, (349, 318, 560, 364)),  # 2024 HL scheme p22: 4(d)(ii) updated-lifecycle graph reprint lettered 'Sales' and 'A B C' beside the reasons list
        (22, (480, 440, 525, 463)),  # 2024 HL scheme p22: 4(d)(ii) lifecycle graph axis label 'Time' beside the reasons list
    ],
    (2024, 'ol'): [
        (6, (356, 266, 545, 356.5)),  # 2024 OL scheme p6: Q11 bathtub-curve reprint lettered A B C D, Failure Rate, Time
        (7, (450, 118, 560, 240)),  # 2024 OL scheme p7: 2(a) skateboarder photo labelled 'Helmet'
        (7, (428, 290, 562, 395)),  # 2024 OL scheme p7: 2(b) skateboard photo labelled 'Truck'
        (8, (393.5, 428, 582, 558)),  # 2024 OL scheme p8: 3(c) wing diagram reprint lettered Fulcrum, 3 m, 50 N, Motor beside the 3(c) answers
        (11, (405, 636, 520, 690)),  # 2024 OL scheme p11: 2(d)(ii) resistor network reprint lettered 8 Ω, 10 Ω, 10 Ω beside the working
    ],
    (2025, 'hl'): [
        (6, (78, 180, 574, 410)),  # SCHEME page 6: Q11's WBS box lettering (Bench, 1. Research and design ... Remove concrete legs), read out of order into Q11's rows.
        (9, (194, 514, 429, 642)),  # SCHEME page 9: Q2(d)(i) photo annotation 'Tightness can be adjusted. Fast secure locking buckle', read in as the card's rows.
        (11, (74, 251, 560, 425)),  # SCHEME page 11: Q3(c)(ii) annotated pictures ('The personal pod has two pivot points ...', 'pivot points', 'R Clip and Pin ...'), read in as the card's rows.
        (13, (369.5, 122, 547, 261)),  # SCHEME page 13: Q1(c)(i) cylinder lettering 'Air', 'Air in pushes piston out', 'Air then returns piston', welded into the prose rows.
        (16, (107, 298, 405, 448)),  # SCHEME page 16: Q3(b)(i) network diagram lettering 'Internet connection', 'Router', 'Wireless access point', 'Wireless', read in as rows 1-2.
        (20, (60, 402, 528, 516)),  # SCHEME page 20: Q5(b)(ii) blow-moulding drawing labels 'Heat to soften', 'Air blown in', 'Plastic tube (Parison) inserted from extruder', 'Finished product', read in as rows. Keep 'Blow moulding' (y 407-419, x 87-192) as the prose row.
    ],
    (2026, 'hl'): [
        (14, (145, 211, 523, 428)),  # the pneumatic circuit beside 1(c)(ii), its three annotation boxes (Attach piston to cylinder; Flow control valves to control the speed of the ram.; 5/2 valve allow the cylinder to move back and forth.)
    ],
}.items():
    LABEL_ZONES.setdefault(_yl, []).extend(_zs)
ASK_ONLY.update({
    'technology-2020-HL-scheme-secC-q1b-i',
    'technology-2020-HL-scheme-secC-q2b-i',
    'technology-2021-HL-scheme-secA-q5',
    'technology-2021-HL-scheme-secA-q9',
    'technology-2021-OL-scheme-secC-q2b-iii',
    'technology-2022-HL-scheme-secA-q8',
    'technology-2022-HL-scheme-secC-q1d-i',
    'technology-2022-OL-scheme-secB-q2b-iii',
    'technology-2022-OL-scheme-secC-q1b-ii',
    'technology-2022-OL-scheme-secC-q2b-iii',
    'technology-2023-HL-scheme-secA-q15',
    'technology-2023-HL-scheme-secB-q2b-ii',
    'technology-2023-HL-scheme-secC-q2b-iii',
    'technology-2023-HL-scheme-secC-q4b-ii',
    'technology-2023-OL-scheme-secB-q3b-iii',
    'technology-2023-OL-scheme-secC-q2b-ii',
    'technology-2024-HL-scheme-secC-q1d-i',
    'technology-2025-HL-scheme-secA-q11',
    'technology-2025-HL-scheme-secA-q15',
    'technology-2025-HL-scheme-secB-q2d-i',
    'technology-2025-HL-scheme-secB-q3c-ii',
    'technology-2025-HL-scheme-secC-q1b-i',
    'technology-2025-HL-scheme-secC-q2c-ii',
    'technology-2025-OL-scheme-secC-q1b-i',
    'technology-2025-OL-scheme-secC-q1b-iii',
    'technology-2026-HL-scheme-secC-q1b-i',
    'technology-2026-HL-scheme-secC-q1c-ii',
    'technology-2026-HL-scheme-secC-q2a-i',
})
WHITEOUT.update({
    'technology-2020-HL-paper-secB-q2b-art': [(315.8, 287.2, 334.0, 295.0), (315.8, 297.5, 393.0, 309.6), (315.8, 319.5, 345.0, 331.6), (315.8, 334.1, 323.2, 346.2), (315.8, 413.3, 371.2, 424.3)],
    'technology-2020-HL-paper-secB-q2b-ii-art': [(295.5, 334.1, 322.9, 346.1), (315.8, 334.6, 323.2, 346.2)],
    'technology-2020-HL-paper-secC-q2b-art': [(362.8, 338.2, 370.5, 350.2)],
    'technology-2020-HL-paper-secC-q5b-art': [(379.5, 294.5, 386.0, 308.0)],
    'technology-2021-HL-scheme-secA-q5': [(484.0, 517.0, 532.0, 531.0), (469.0, 344.5, 536.0, 416.5)],
    'technology-2021-HL-scheme-secB-q2c-ii': [(220.0, 212.0, 379.0, 256.0)],
    'technology-2021-HL-scheme-secC-q4d-i': [(85.8, 378.4, 229.6, 390.0)],
    'technology-2021-OL-paper-secA-q3-art': [(376.0, 687.0, 443.6, 699.6)],
    'technology-2021-OL-paper-secC-q1b-art': [(382.0, 237.0, 462.2, 351.0), (370.4, 391.0, 409.5, 403.0)],
    'technology-2021-OL-paper-secC-q1c-art': [(345.9, 483.3, 383.7, 495.3)],
    'technology-2021-OL-paper-secC-q2b-art': [(349.0, 204.0, 562.0, 408.0), (318.0, 352.4, 342.6, 379.8)],
    'technology-2021-OL-paper-secC-q2c-art': [(134.0, 459.0, 240.0, 490.0)],
    'technology-2021-OL-scheme-secC-q2b-iii': [(320.0, 224.0, 402.0, 384.2)],
    'technology-2022-HL-scheme-secC-q1d-i': [(316.5, 540.5, 334.6, 570.5)],
    'technology-2022-HL-scheme-secC-q3b-iii': [(337.0, 672.2, 411.0, 698.6)],
    'technology-2022-OL-scheme-secC-q1b-ii': [(410.4, 588.5, 417.1, 602.2), (289.5, 765.8, 306.5, 769.2)],
    'technology-2023-HL-scheme-secA-q15': [(390.0, 700.5, 466.0, 731.0)],
    'technology-2023-HL-scheme-secC-q2b-iii': [(439.0, 249.0, 467.0, 254.5)],
    'technology-2023-OL-paper-secB-q3a-art': [(414.0, 143.5, 435.5, 157.0)],
    'technology-2023-OL-paper-secC-q1b-art': [(432.0, 445.0, 468.5, 458.0)],
    'technology-2023-OL-scheme-secC-q2b-ii': [(365.0, 271.0, 376.9, 285.0)],
    'technology-2024-HL-paper-secA-q5-art': [(110.0, 255.0, 316.0, 284.0), (109.0, 366.5, 304.0, 395.0), (109.0, 413.0, 407.0, 443.0), (109.0, 460.0, 422.0, 481.0)],
    'technology-2024-OL-paper-secB-q3c-art': [(326.0, 473.0, 369.0, 538.0)],
    'technology-2024-OL-paper-secC-q1c-art': [(460.0, 515.5, 479.5, 545.0)],
    'technology-2025-OL-scheme-secC-q1b-i': [(342.0, 357.5, 404.0, 371.0), (342.0, 407.5, 401.5, 421.0), (342.0, 457.5, 413.0, 471.0)],
    'technology-2026-HL-paper-secC-q5b-art': [(247.1, 237.5, 258.0, 250.1), (275.5, 237.5, 313.9, 250.1), (275.5, 252.2, 305.7, 264.8), (247.1, 276.6, 261.0, 289.2), (275.5, 276.6, 321.5, 289.2), (275.5, 291.2, 339.1, 303.8), (247.1, 315.7, 263.9, 328.3), (275.5, 315.7, 313.9, 328.3), (275.5, 330.3, 322.3, 342.9)],
    'technology-2026-HL-paper-secC-q5c-art': [(395.8, 544.6, 452.9, 557.2)],
    'technology-2026-HL-scheme-secB-q2b-iii': [(96.3, 578.2, 296.4, 641.3)],
    'technology-2026-HL-scheme-secC-q4d': [(326.4, 424.2, 353.4, 436.8), (451.1, 746.6, 547.8, 759.2)],
})
SOLUTION_SHARED.update({
    'technology-2023-HL-scheme-secA-q6-ii': 'technology-2023-HL-scheme-secA-q6',
    'technology-2025-HL-scheme-secC-q1b-ii': 'technology-2025-HL-scheme-secC-q1b-i',
})
FIGURE_SHARED.update({
    'technology-2022-HL-paper-secB-q2b-art': 'technology-2022-HL-paper-secB-q2c-art',
})
for _ylb, _zs in {
    (2025, 'hl', '014'): [
        (4, (85.0, 185.0, 545.0, 306.0)),  # PAPER booklet 014, page 4 (not the scheme): Q7's photo labels Mast/Hull/Sail and its answer table Part/Materia
        (6, (376.0, 425.0, 548.0, 532.0)),  # PAPER booklet 014, page 6: Q12's circuit lettering R1 = 6 kΩ ... R4 = 12 kΩ. 'R1 = 6 kΩ' sits above the Q12 ma
        (7, (390.0, 183.0, 538.0, 291.0)),  # PAPER booklet 014, page 7: Q13 diving-board lettering Ladder / Springboard / Tilt Angle, leaking into Q13's qu
    ],
}.items():
    PAPER_ZONES.setdefault(_ylb, []).extend(_zs)
LABEL_KEYS.update({
    (2020, 'hl', 'A', 14, None): [{'letter': 'A', 'meaning': "Gear A, the driven gear (96 teeth) on the e-scooter's rear wheel hub, driven by chain from the 12-tooth motor gear"}],
    (2020, 'hl', 'A', 5, None): [{'letter': 'A', 'meaning': 'The output terminal at the junction between R1 (120 Ω) and R2, where the 5 V supply is taken'}],
    (2020, 'hl', 'B', 2, 'b'): [{'letter': 'A', 'meaning': "Height A: the up-and-down adjustment of the lamp's horizontal arm (red double arrow at the arm's end); the scheme answers it with a rack and pinion system"}, {'letter': 'B', 'meaning': 'Rotary movement B: the lamp turning about its round base (curved red arrow); the scheme answers it with a worm/worm wheel system or servo motor'}],
    (2020, 'hl', 'B', 3, 'b'): [{'letter': 'A', 'meaning': 'The upper white nylon gear (50 teeth), a worm wheel driven by the worm on the motor shaft'}, {'letter': 'B', 'meaning': 'The lower white nylon gear (50 teeth), driven by the same worm; together A and B turn the beater shafts (gear ratio 50:1, 40 RPM at 2000 RPM)'}],
    (2020, 'hl', 'C', 2, 'b'): [{'letter': 'A', 'meaning': "The op-amp's inverting (−) input, V−, at the junction of the input potential divider (the resistor and LDR in the scheme's completed circuit); its voltage varies with the light level"}],
    (2020, 'hl', 'C', 2, 'd'): [{'letter': 'A', 'meaning': 'Keypad A, on the gate pillar (one of the two keypads that open the gates)'}, {'letter': 'B', 'meaning': 'Keypad B, the box on the wall beside the gate (the other keypad)'}, {'letter': 'C', 'meaning': 'The gate opening switch at the house'}, {'letter': 'S', 'meaning': 'The master on/off switch at the house'}, {'letter': 'E', 'meaning': "In the scheme's circuit, the output of the OR gates combining Keypad (A), Keypad (B) and Switch (C)"}, {'letter': 'F', 'meaning': "In the scheme's circuit, the output of the AND gate combining E with Switch (S): the signal that opens the gates"}],
    (2021, 'ol', 'A', 5, None): [{'letter': 'A', 'meaning': 'Worm'}, {'letter': 'B', 'meaning': 'Worm wheel'}],
    (2021, 'ol', 'C', 1, 'c'): [{'letter': 'A', 'meaning': 'Input port'}, {'letter': 'B', 'meaning': 'Input port'}, {'letter': 'C', 'meaning': 'Output port'}],
    (2021, 'ol', 'C', 2, 'b'): [{'letter': 'A', 'meaning': 'Electrolytic Capacitor'}, {'letter': 'B', 'meaning': 'Transistor'}],
    (2022, 'hl', 'A', 6, None): [{'letter': 'A', 'meaning': 'Follower'}, {'letter': 'B', 'meaning': 'Cam'}],
    (2022, 'hl', 'C', 2, 'b'): [{'letter': 'A', 'meaning': "not named in the scheme's answer (drawn on the paper as a variable resistor)"}, {'letter': 'B', 'meaning': 'Thermistor'}, {'letter': 'C', 'meaning': 'Push-to-make switch'}, {'letter': 'D', 'meaning': 'OR gate'}],
    (2022, 'hl', 'C', 4, 'd'): [{'letter': 'A', 'meaning': 'Decreasing failure rate, known as early failures'}, {'letter': 'B', 'meaning': 'Constant failure rate, known as random failures'}, {'letter': 'C', 'meaning': 'Increasing failure rate, known as wear-out failures'}],
    (2022, 'ol', 'A', 11, None): [{'letter': 'R', 'meaning': "the resistor in series with the LED; the scheme: 'To protect the LED by reducing the current flow'"}],
    (2022, 'ol', 'A', 7, None): [{'letter': 'A', 'meaning': 'the arrow on the photograph giving the viewing direction for the 2D sketch (the scheme answers with the view from that direction)'}],
    (2022, 'ol', 'C', 1, 'c'): [{'letter': 'A', 'meaning': "the air port of the single-acting cylinder in the scheme's drawn symbol ('Compressed air enters through Port A')"}],
    (2022, 'ol', 'C', 2, 'a'): [{'letter': 'R', 'meaning': 'the resistor whose bands are brown, black, red, gold: 1000Ω'}],
    (2022, 'ol', 'C', 2, 'b'): [{'letter': 'A', 'meaning': 'Variable resistor'}, {'letter': 'B', 'meaning': 'Thermistor'}, {'letter': 'C', 'meaning': 'Buzzer (named in the 2(b)(iii) ask)'}],
    (2022, 'ol', 'C', 2, 'd'): [{'letter': 'X', 'meaning': 'OR gate'}, {'letter': 'Y', 'meaning': 'NOT gate'}],
    (2022, 'ol', 'C', 5, 'b'): [{'letter': 'A', 'meaning': 'the exterior CLT panel being lowered into place (named in the ask)'}, {'letter': 'B', 'meaning': 'the concrete floor (named in the ask)'}],
    (2023, 'hl', 'C', 2, 'b'): [{'letter': 'A', 'meaning': 'Variable Resistor'}, {'letter': 'B', 'meaning': 'Thermistor'}],
    (2023, 'ol', 'A', 1, None): [{'letter': 'A', 'meaning': 'Medical/First Aid (the green sign with the white cross)'}, {'letter': 'B', 'meaning': 'No entry (the round red prohibition sign)'}],
    (2023, 'ol', 'A', 7, None): [{'letter': 'A', 'meaning': "The arrow giving the viewing direction for the 2D sketch; the scheme's sketch is the side view of the stand"}],
    (2023, 'ol', 'A', 8, None): [{'letter': 'A', 'meaning': 'The wiper (or slider): the middle pin, a moveable contact'}],
    (2023, 'ol', 'C', 4, 'a'): [{'letter': 'A', 'meaning': 'Low cost/high quality, likely to sell.'}, {'letter': 'B', 'meaning': 'High cost/high quality, likely to sell but cost could impede sales.'}, {'letter': 'C', 'meaning': 'Low cost/low quality, poor sales likely as a result'}],
    (2024, 'hl', 'C', 4, 'c'): [{'letter': 'A', 'meaning': 'Early failure stage: failure rate decreases quickly as faults are corrected; some early products have inadequate reliability'}, {'letter': 'B', 'meaning': 'Low failure rate; the product is reliable'}, {'letter': 'C', 'meaning': 'Wear-out phase: failures increase and the product becomes less reliable, usually due to extended service'}],
    (2024, 'hl', 'C', 4, 'd'): [{'letter': 'A', 'meaning': 'Introduction'}, {'letter': 'B', 'meaning': 'Growth'}, {'letter': 'C', 'meaning': 'Maturity'}, {'letter': 'D', 'meaning': 'Decline'}],
    (2024, 'ol', 'A', 11, None): [{'letter': 'A-B', 'meaning': 'Early stage in the life of a product: faults are more likely to occur; as problems are resolved, the failure rate begins to fall'}, {'letter': 'C-D', 'meaning': 'The product is approaching its end of life and faults increase due to failing parts within the product'}],
    (2025, 'hl', 'B', 3, 'b'): [{'letter': 'A', 'meaning': 'the 20-tooth gear on the motor shaft (driver)'}, {'letter': 'B', 'meaning': 'the 60-tooth gear driven by A'}, {'letter': 'C', 'meaning': "the 30-tooth gear on B's shaft (driver)"}, {'letter': 'D', 'meaning': 'the 60-tooth gear on the output shaft (driven by C)'}],
    (2025, 'hl', 'C', 2, 'b'): [{'letter': 'A', 'meaning': "the IC's − input, fed by the LDR / variable resistor potential divider ('the voltage from A feeding into the Op-Amp')"}, {'letter': 'B', 'meaning': "the IC's + input, the reference voltage set by the R1 and R2 potential divider"}],
    (2025, 'hl', 'C', 2, 'c'): [{'letter': 'A', 'meaning': 'Switch on'}, {'letter': 'B', 'meaning': 'Filament in nozzle 1'}, {'letter': 'C', 'meaning': 'Filament in nozzle 2'}, {'letter': 'D', 'meaning': 'Temperature sensor for 400°C'}, {'letter': 'E', 'meaning': 'the output of the final AND gate: the printer operates'}],
    (2025, 'hl', 'C', 2, 'd'): [{'letter': 'A', 'meaning': 'Meter A – Ammeter – reads current in Amps'}, {'letter': 'V', 'meaning': 'Meter V – Voltmeter – reads voltage in Volts'}],
    (2025, 'hl', 'C', 4, 'b'): [{'letter': 'A', 'meaning': 'Line A: the cost of manufacturing by skilled labour (€20 per unit, from 8000/400)'}, {'letter': 'B', 'meaning': 'Line B: the cost with automated computerised machinery (fixed cost €3000)'}, {'letter': 'C', 'meaning': 'Point C: where lines A and B intersect, the break-even quantity of 200 units'}, {'letter': 'X', 'meaning': 'Region X, before the BEQ: the automated process makes a loss'}, {'letter': 'Y', 'meaning': 'Region Y, after the BEQ: the automated process is profitable, and profit grows with volume'}],
    (2025, 'hl', 'C', 4, 'd'): [{'letter': 'A', 'meaning': 'Once-off projects'}, {'letter': 'B', 'meaning': 'Batch production'}, {'letter': 'C', 'meaning': 'Mass production'}, {'letter': 'D', 'meaning': 'Continuous production'}],
    (2025, 'ol', 'C', 2, 'c'): [{'letter': 'X', 'meaning': 'AND gate'}, {'letter': 'Y', 'meaning': 'NOT gate'}, {'letter': 'A', 'meaning': 'input to gate X'}, {'letter': 'B', 'meaning': 'input to gate X'}, {'letter': 'C', 'meaning': 'output of X (A AND B), input to Y'}, {'letter': 'D', 'meaning': 'output of Y (NOT C)'}],
    (2026, 'ol', 'A', 4, None): [{'letter': 'A', 'meaning': "The white arrow on the planter-box photograph giving the viewing direction; the scheme's answer is the elevation seen along it (three stacked troughs between two upright legs)"}],
    (2026, 'ol', 'A', 9, None): [{'letter': 'A', 'meaning': 'Switch A, the switch inside the dashed red box in the motor circuit: a Double Pole Double Throw (DPDT) switch'}],
    (2026, 'ol', 'C', 2, 'b'): [{'letter': 'A', 'meaning': 'Variable resistor'}, {'letter': 'B', 'meaning': 'LDR (light dependent resistor)'}],
    (2026, 'ol', 'C', 4, 'b'): [{'letter': '1', 'meaning': 'Introduction'}, {'letter': '2', 'meaning': 'Growth'}, {'letter': '3', 'meaning': 'Maturity'}, {'letter': '4', 'meaning': 'Decline'}],
})

_WORDS = {}


# Sittings whose scheme text layer is not what the page prints: 2022 Higher's
# subset fonts report the wrong character for every glyph (tech_glyphs.py
# rebuilt its .md from glyph ids), and 2020 Higher's Calibri reports a space
# for r, w, v and g. Their words are read the same way the .md was, by glyph
# id, or no line of the .md could ever be found again on the page.
GLYPH_REPAIRED = {(2022, 'hl'), (2020, 'hl')}
_GLYPH_TRUTH = []


def _sitting_of(path):
    m = re.search(r'(\d{4})-(hl|ol)', os.path.basename(path))
    return (int(m.group(1)), m.group(2)) if m else None


def _repaired_words(path, page):
    """Words of a glyph-repaired page: (x0, y0, x1, y1, text, block, line)."""
    import tech_glyphs as TG
    if not _GLYPH_TRUTH:
        _GLYPH_TRUTH.append(TG.truth_table())
    truth, by_family = _GLYPH_TRUTH[0]
    out = []
    with pymupdf.open(path) as doc:
        pg = doc[page]
        broken = TG.mangled_fonts(doc)
        glyphs = TG._glyphs(pg)
        for bi, blk in enumerate(pg.get_text('rawdict')['blocks']):
            if blk.get('type') != 0:
                continue
            for li, line in enumerate(blk.get('lines', [])):
                cur, box = [], None

                def flush():
                    if cur and box:
                        out.append((box[0], box[1], box[2], box[3], ''.join(cur), bi, li))
                for sp in line.get('spans', []):
                    for ch in sp['chars']:
                        c = ch['c']
                        key = (round(ch['origin'][0], 2), round(ch['origin'][1], 2))
                        if key in glyphs:
                            (font, gid), _seen = glyphs[key]
                            if font in broken or c == ' ' or ord(c) < 0x20:
                                real = (truth.get((font, gid))
                                        or by_family[TG.family(font)].get(gid)
                                        or TG.LOOKED_AT.get((font, gid)))
                                if real:
                                    c = real
                        if c.isspace():
                            flush()
                            cur, box = [], None
                            continue
                        x0, y0, x1, y1 = ch['bbox']
                        cur.append(c)
                        box = (x0, y0, x1, y1) if box is None else (
                            min(box[0], x0), min(box[1], y0), max(box[2], x1), max(box[3], y1))
                flush()
    return out


def page_words(path, page):
    key = (path, page)
    if key not in _WORDS:
        if _sitting_of(path) in GLYPH_REPAIRED and '/schemes/' in path:
            _WORDS[key] = _repaired_words(path, page)
        else:
            with pymupdf.open(path) as doc:
                _WORDS[key] = [tuple(w[:7]) for w in doc[page].get_text('words')]
    return _WORDS[key]


def _bare(token):
    return re.sub(r'^[\(\[“"\'•]+|[\)\]”"\'.,;:!?]+$', '', token)


def zone_words(path, page, rects):
    """The words printed inside these rectangles, bare of punctuation.

    By text LINE, not by word: a line of prose whose last word happens to
    reach into the rectangle -- "...generally supplied from" beside the
    2023 Ordinary flowchart -- is prose, and taking "from" off the end of
    its marking point lost the word. A drawing's label is a line of its own,
    inside the drawing from end to end.
    """
    lines = {}
    for x0, y0, x1, y1, text, block, line in page_words(path, page):
        lines.setdefault((block, line), []).append((x0, y0, x1, y1, text))
    out = set()
    for words in lines.values():
        if all(any(r[0] <= (x0 + x1) / 2 <= r[2] and r[1] <= (y0 + y1) / 2 <= r[3]
                   for r in rects)
               for x0, y0, x1, y1, _t in words):
            out.update(_bare(t) for _x0, _y0, _x1, _y1, t in words)
    out.discard('')
    return out



_CATALOGUE = {}


def _catalogue_rect(key):
    """(booklet, page, rect) the cropper recorded for a published crop."""
    if not _CATALOGUE:
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'authored',
                            'technology-figures.json')
        try:
            import json
            with open(path, encoding='utf-8') as fh:
                for e in json.load(fh):
                    if 'rect' in e:
                        _CATALOGUE[e['file'][:-4]] = (e['booklet'], e['page'], tuple(e['rect']))
        except FileNotFoundError:
            pass
    return _CATALOGUE.get(key)


def paper_labels(year, level, key):
    """The words inside a crop: a BY_EYE rect, or the cropper's own as the
    catalogue records it. Empty for a key with neither."""
    hit = BY_EYE.get(key) or _catalogue_rect(key)
    if not hit:
        return set()
    booklet, page, rect = hit
    rects = [rect] + [r for p, r in PAPER_ZONES.get((year, level, booklet), []) if p == page]
    words = zone_words(paper_path(year, level, booklet), page, rects)
    if WHITEOUT.get(key):
        # The blanked boxes hold the ask's own prose, not the picture's
        # lettering: they must not come off the ask.
        words -= zone_words(paper_path(year, level, booklet), page, WHITEOUT[key])
    return words


def scheme_zones(year, level, page):
    """Every solution crop and label zone on a scheme page."""
    rects = [rect for k, (p, rect, _d) in SOLUTIONS.items()
             if parse_key(k)[:2] == (year, level) and p == page]
    rects += [rect for p, rect in LABEL_ZONES.get((year, level), []) if p == page]
    return rects


def scheme_labels(year, level, page):
    """The words inside every solution crop and label zone on a scheme page.

    Less any word the page also prints in prose outside them: "load" is a
    label on the 2026 Higher roof sketch and the last word of the marking
    point beside it, and taking it off the point lost it. The fallback for
    a line strip_row_labels cannot place.
    """
    rects = scheme_zones(year, level, page)
    if not rects:
        return set()
    path = scheme_path(year, level)
    inside = zone_words(path, page, rects)
    outside = set()
    for row in page_rows(path, page):
        for line in row:
            if not _inside(line, rects):
                outside.update(_bare(w[4]) for w in line)
    return inside - outside


def strip_scheme_line(text, year, level, pages, keep_numbers=False):
    """A scheme line with a drawing's lettering taken off, by row where it can be."""
    for page in sorted(pages):
        rects = scheme_zones(year, level, page)
        if not rects:
            continue
        got = strip_row_labels(text, scheme_path(year, level), page, rects)
        if got is not None:
            return got
    labels = set()
    for page in pages:
        labels |= scheme_labels(year, level, page)
    return strip_labels(text, labels, keep_numbers=keep_numbers)


def _norm(text):
    return re.sub(r'[^a-z0-9]+', '', text.lower())


_ROWS = {}


def page_rows(path, page):
    """The page's visual rows: pymupdf lines sharing a vertical centre, left to right.

    This is the extractor's own assembly rule (extract-scheme.py gathers lines
    whose vertical centres agree into one row), so a scheme .md line can be
    found again on the page as the row it came from, and the lines INSIDE a
    drawing told apart from the prose beside them by where each is printed.
    """
    key = (path, page)
    if key not in _ROWS:
        lines = {}
        for x0, y0, x1, y1, text, block, line in page_words(path, page):
            lines.setdefault((block, line), []).append((x0, y0, x1, y1, text))
        items = []
        for words in lines.values():
            words.sort(key=lambda w: w[0])
            yc = sum((w[1] + w[3]) / 2 for w in words) / len(words)
            items.append((yc, min(w[0] for w in words), words))
        # extract-scheme.py's own rule, line for line: sorted by centre then
        # left edge, a line joins the row while its centre is within
        # max(3, 0.6 x the row's first line height) of that first line's.
        items.sort(key=lambda it: (round(it[0], 1), it[1]))
        rows, current, row_y, row_h = [], [], None, 10.0
        for yc, x0, words in items:
            if row_y is not None and abs(yc - row_y) > max(3.0, row_h * 0.6):
                rows.append(current)
                current = []
            if not current:
                row_y = yc
                row_h = max(w[3] for w in words) - min(w[1] for w in words)
            current.append((x0, words))
        if current:
            rows.append(current)
        _ROWS[key] = [[words for _x0, words in sorted(row, key=lambda it: it[0])]
                      for row in rows]
    return _ROWS[key]


def _inside(words, rects):
    return all(any(r[0] <= (x0 + x1) / 2 <= r[2] and r[1] <= (y0 + y1) / 2 <= r[3]
                   for r in rects) for x0, y0, x1, y1, _t in words)


def strip_row_labels(text, path, page, rects):
    """`text`, a scheme line, with the lines printed INSIDE a drawing on its row taken off.

    Returns None where the line is not found as a row of the page, so the
    caller can fall back to strip_labels. A line that is nothing but a
    drawing's lettering comes back as ''.
    """
    if not rects or not text:
        return None
    want = _norm(text)
    for row in page_rows(path, page):
        if _norm(' '.join(w[4] for line in row for w in line)) != want:
            continue
        kept = [line for line in row if not _inside(line, rects)]
        if len(kept) == len(row):
            return text
        return ' '.join(w[4] for line in kept for w in line)
    return None


def strip_labels(text, labels, keep_numbers=False):
    """`text` with a drawing's labels taken off its end, or '' if it was all labels.

    A trailing word comes off only while it is a zone word AND carries no
    closing punctuation; a leading run comes off only when it is four or more
    zone words long, which is a table's cells and never a sentence's opening.
    With keep_numbers, a trailing run of bare numbers stays.
    """
    if not labels or not text:
        return text
    tokens = text.split()
    if all(_bare(t) in labels for t in tokens):
        return ''
    lo, hi = 0, len(tokens)
    while hi > lo and _bare(tokens[hi - 1]) in labels \
            and not re.search(r'[.!?;:,]$', tokens[hi - 1]):
        hi -= 1
    if hi == len(tokens) - 1 and re.fullmatch(r'[A-Za-z]', _bare(tokens[-1])) \
            and not re.search(r'[.?!]$', tokens[-2] if len(tokens) > 1 else ''):
        # A lone letter at the end is the sentence's own: "Note: f = 1.44 /
        # (R1 + 2R2) × C" ends in the capacitor's name, which the 555's
        # crop also letters. Unless a full stop stands before it -- "...in
        # the direction of arrow A. A" is the arrow's own letter read after
        # the sentence closed.
        hi = len(tokens)
    if hi == len(tokens) and len(tokens) >= 4:
        # A caption inside the picture, read after the ask's last sentence:
        # "...and recyclability. Box B. Made from cardboard. Box A. Made from
        # expanded polystyrene." Every word of the run is lettering and the
        # run starts where a sentence ended, so punctuation is no bar here.
        j = len(tokens)
        while j > 0 and _bare(tokens[j - 1]) in labels:
            j -= 1
        if 0 < j < len(tokens) - 2 and re.search(r'[.?!]$', tokens[j - 1]):
            hi = j
    if keep_numbers and all(re.fullmatch(r'[\d.,]+', t) for t in tokens[hi:]):
        # "Mean: 2+3+...+4 = 48 = 4" ends in the mean, which is also an
        # axis label on the control chart beside it. A bare number closing
        # a calculation is its answer; only a run with a unit or a word in
        # it ("250N", "Load Effort") is lettering.
        hi = len(tokens)
    run = 0
    while lo + run < hi and _bare(tokens[lo + run]) in labels \
            and not re.search(r'[.!?;:,]$', tokens[lo + run]):
        run += 1
    if run >= 4:
        lo += run
    return ' '.join(tokens[lo:hi])
