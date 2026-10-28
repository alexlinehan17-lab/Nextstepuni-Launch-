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
    'technology-2024-OL-paper-secC-q2b-art': ('039', 4, (345, 230, 556, 370)),
}

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
}

# Solution crops that ARE the whole answer: the scheme answers in a TABLE,
# whose cells the text layer reads column by column into lines no student
# could claim ("Air transport Approx. 2% of global CO2 Nitrogen oxides...").
# The card's one row is the ask and the reveal shows the table itself.
ASK_ONLY = {
    'technology-2026-HL-scheme-secB-q3d',
    'technology-2026-HL-scheme-secC-q5d',
}

_WORDS = {}


def page_words(path, page):
    key = (path, page)
    if key not in _WORDS:
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


def paper_labels(year, level, key):
    """The words inside a BY_EYE crop, or an empty set for any other key."""
    if key not in BY_EYE:
        return set()
    booklet, page, rect = BY_EYE[key]
    return zone_words(paper_path(year, level, booklet), page, [rect])


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
