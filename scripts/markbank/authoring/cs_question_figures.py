#!/usr/bin/env python3
"""Crop the code a Computer Science question prints, so its asks can be carded.

    python3 scripts/markbank/authoring/cs_question_figures.py 2024 hl 2
    python3 scripts/markbank/authoring/cs_question_figures.py --write
    python3 scripts/markbank/authoring/cs_question_figures.py --catalogue

Seventy-four open asks point at something printed, and in this subject that is
almost always a PROGRAM. The text layer hands a listing back as
"1 number = 27 2 while number < 39: 3 print(number, end=" ") 4 number = number
+ 3" -- the line numbers run into the code, the indentation gone, which is the
one thing a program cannot survive losing. No card can carry that as text.

Finding it needs no clustering or guesswork, unlike the diagrams in Chemistry:
the SEC sets code in Courier and nothing else on the page in Courier. The line
numbers are CourierNewPS-BoldMT at x=62 and the code CourierNewPSMT at x=83,
against Calibri prose at 12pt. So a code block is a run of consecutive Courier
lines, and its extent is exactly their bounding box.

The crop is the paper's own print, indentation and all. Alt text names the
question and quotes the first line, which is the most a description of a
program can honestly say without paraphrasing it.

It also crops the TABLES and DIAGRAMS -- truth tables, flowcharts, trace
tables, the BOOKS relational table, a row of numbered discs -- which is the
other half of what these questions point at. That half works the way
chem_question_figures does, and for the same reason: the artwork is vector
rules and images with its labels set as ordinary text beside them, so a figure
is a run of drawing and image rectangles uninterrupted by the question's prose.
The two are deliberately separate files rather than one shared one, because
what they must EXCLUDE differs -- here a code listing's grey background box is
a drawing rectangle enclosing a figure that is already cropped as code, and
cropping it twice would put the same program on the card under two names.
"""
import argparse
import collections
import json
import os
import re
import sys

import pymupdf

DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, DIR)
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(DIR)))

import paper as PP                                          # noqa: E402

DPI = 150
PAD_X, PAD_Y = 10.0, 6.0
MONO = re.compile(r'courier', re.I)
# A band this small is a rule, a tick box or a single cell border.
MIN_W, MIN_H = 70.0, 30.0
LABEL_MAX = 26
PART_MARKER = re.compile(r'^\(([a-h]|i{1,3}|iv|v|vi{0,3}|ix|x)\)')
FURNITURE = re.compile(r'^(Leaving Certificate|Computer Science|Page \d|\d{1,3})$')
# A band carrying any of these is the page's own furniture, not the question's
# figure: the section banner is a wide shaded rectangle and clusters with
# whatever is printed under it. 2025 OL Question 16's first band came out as
# the "Section C / Programming / 80 marks" bar, the instruction to save your
# file, and a decorative photograph of a plasterer.
BANNER = re.compile(r'^(Section [A-C]|Programming|Short Answer|Long Questions|'
                    r'\d{1,3} marks|Answer all|Answer any|Question \d{1,2})$', re.I)
# The ruled box a candidate WRITES in. Its labels are prompts -- "Role 1:",
# "Explanation:", "1." -- and it is empty by design, which is exactly what a
# crop of it would show the student. Most of what the band finder returns on
# these papers is this, not a figure.
PROMPT = re.compile(r'.*:$|^\d{1,2}[.)]$', re.I)
FIGURE_REF = re.compile(r'^(figure|fig\.?)\s*\d', re.I)
STRAY_WORD = re.compile(r'[a-z]{1,3}')
# A listing shorter than this is an inline token in Courier ("the variable
# `x`"), not a program the card has to show.
MIN_LINES = 2


def mono_runs(page):
    """[(x0, y0, x1, y1, [lines])] for each run of consecutive Courier lines."""
    rows = []
    for bl in page.get_text('dict')['blocks']:
        for ln in bl.get('lines', []):
            spans = ln.get('spans') or []
            if not spans:
                continue
            text = ''.join(s['text'] for s in spans)
            if not text.strip():
                continue
            mono = sum(len(s['text']) for s in spans if MONO.search(s['font']))
            rows.append((ln['bbox'], text, mono > 0))
    rows.sort(key=lambda r: (round(r[0][1], 1), r[0][0]))

    runs, cur = [], []
    for bbox, text, is_mono in rows:
        if is_mono:
            if cur and bbox[1] - cur[-1][0][3] > 18:
                runs.append(cur)
                cur = []
            cur.append((bbox, text))
        elif cur:
            runs.append(cur)
            cur = []
    if cur:
        runs.append(cur)

    out = []
    for run in runs:
        if len({round(b[1]) for b, _ in run}) < MIN_LINES:
            continue
        # An ANSWER SPACE set in the paper's monospace face is not a program.
        # 2024 OL Q13 prints "Choose suitable data types for the variables A
        # and B." over two ruled lines labelled "A:" and "B:", all in Courier;
        # taken as a second listing it put a blank box between the question's
        # two bands and cost the question its figure altogether.
        body = [' '.join(t.split()) for _, t in run]
        if sum(1 for t in body if len(t) >= 3 and not PROMPT.match(t)) < 2:
            continue
        x0 = min(b[0] for b, _ in run)
        y0 = min(b[1] for b, _ in run)
        x1 = max(b[2] for b, _ in run)
        y1 = max(b[3] for b, _ in run)
        out.append((x0, y0, x1, y1, [t for _, t in run]))
    return out


def artwork(page):
    out = []
    for d in page.get_drawings():
        r = d['rect']
        if r.width > 2 and r.height > 2:
            out.append((r.x0, r.y0, r.x1, r.y1))
    for im in page.get_images(full=True):
        for r in page.get_image_rects(im[0]):
            out.append((r.x0, r.y0, r.x1, r.y1))
    return out


def rules(page):
    """The thin wide strokes a ruled table draws its rows with.

    artwork() drops anything under 2pt tall, which is right for band-finding
    -- a rule is furniture -- but it means a table whose BODY is only ruled
    rows came out as its shaded header and nothing else. 2023 OL Q9 shipped as
    a 34pt strip reading "Column A / Column B" with the eight data examples the
    question asks about left outside the crop.
    """
    out = []
    for d in page.get_drawings():
        r = d['rect']
        if r.height <= 2.0 and r.width >= 40.0:
            out.append((r.x0, r.y0, r.x1, r.y1))
    return sorted(out, key=lambda r: r[1])


def rule_rows(page):
    """Rules merged across the row they share.

    A two-column table draws each row as one rule PER COLUMN, so no single
    stroke spans the table and a width test against one of them fails on
    every ruled table with more than one column. Strokes whose tops agree
    within 2pt are one row.
    """
    rows = []
    for x0, y0, x1, y1 in rules(page):
        for row in rows:
            if abs(row[1] - y0) <= 2.0:
                row[0] = min(row[0], x0)
                row[2] = max(row[2], x1)
                row[3] = max(row[3], y1)
                break
        else:
            rows.append([x0, y0, x1, y1])
    return sorted(rows, key=lambda r: r[1])


def follow_table(page, x0, y0, x1, y1, prose=()):
    """Extend a band down through the rows of its own ruled table.

    A band is a ruled table when a rule lies along its TOP or its foot. From
    there the crop follows the chain of rules down, row by row, and stops at
    the first line of the question's PROSE -- which is what separates one
    table from the next table further down the same page.

    Requiring the band to END on a rule was not enough: 2024 HL Q1 draws a
    logic gate in each row, so the band's foot is the last gate rather than
    the last rule, and the table's own closing border then read as a
    different table starting -- leaving a crop of the header and nothing else.
    """
    rows = [r for r in rule_rows(page) if x0 - 6.0 <= r[0] and r[2] <= x1 + 6.0]
    anchor = next((r for r in rows
                   if abs(r[1] - y0) <= 4.0 or abs(r[3] - y1) <= 3.0), None)
    if anchor is None:
        return y1
    # Width is measured against the ANCHORING RULE, not the band. 2025 OL Q14
    # prints a photograph of the vending machine beside its price table, so
    # the band is half as wide again as the table, and testing the table's own
    # rules against the band's width rejected every one of them.
    width = anchor[2] - anchor[0]
    rows = [r for r in rows
            if min(r[2], anchor[2]) - max(r[0], anchor[0]) >= 0.8 * width]
    for _ in range(40):
        nxt = [r for r in rows if 0 < r[1] - y1 <= 90.0]
        if not nxt:
            break
        r = min(nxt, key=lambda r: r[1])
        # The question's own prose begins hard against the table's left
        # edge; a CELL's text is indented inside it. Without that distinction
        # every table whose cells hold sentences -- "The number of players in
        # a football squad" -- stopped at its first data row.
        if any(y1 < ln[1] and ln[3] < r[1] and ln[0] <= x0 + 3.0
               for ln in prose):
            break
        y1 = r[3]
    return y1


def is_blank_box(page, r, text_rows):
    """Nothing in this rectangle but prompts and its own furniture.

    Three things make a box full, and none of them is a rectangle: a word of
    its own that is not a prompt; a curve, which no ruled box draws; or a
    sub-cell carrying a word. Testing for "any rectangle inside" instead kept
    every answer box on the paper, because the box tints the strip behind
    "Answer:" and that tint is a rectangle.
    """
    words = [(bb, t) for bb, t in text_rows
             if r.x0 - 2 < bb[0] and bb[2] < r.x1 + 2
             and r.y0 - 2 < bb[1] and bb[3] < r.y1 + 2
             and not PROMPT.match(t)]
    if words:
        return False
    for d in page.get_drawings():
        c = d['rect']
        if not (r.x0 - 2 < c.x0 and c.x1 < r.x1 + 2
                and r.y0 - 2 < c.y0 and c.y1 < r.y1 + 2):
            continue
        if any(it[0] in ('c', 'qu') for it in d.get('items', [])):
            return False
    # A PHOTOGRAPH is not a drawing. 2022 OL Q13(a) prints its binary digits
    # beside a picture of the alarm clock the question is about, and cutting
    # "the blank thing on the right" took the clock with it. A ruled line
    # placed as an image is still furniture.
    for im in page.get_images(full=True):
        for ir in page.get_image_rects(im[0]):
            if is_a_rule(ir.x0, ir.y0, ir.x1, ir.y1):
                continue
            if (r.x0 - 2 < ir.x0 and ir.x1 < r.x1 + 2
                    and r.y0 - 2 < ir.y0 and ir.y1 < r.y1 + 2):
                return False
    return True


def answer_table_top(page, x0, y0, x1, y1, text_rows):
    """Where a ruled table with an EMPTY BODY starts, or None.

    The papers print two kinds of ruled table and they look identical to a
    geometry test. One carries the matter the question is about -- the six
    data examples, the truth table's input rows, the three logic gates. The
    other is where the candidate writes, and its body is blank under a filled
    header: 2022 HL Q5 prints "Letter | Missing Text" with A to E down the
    side and nothing else, and 2022 OL Q11 prints one under its photographs.

    A body carries content if any cell holds a word rather than a single
    character, if two or more columns hold anything at all, or if anything is
    drawn or photographed inside it. A column of bare letters is an index, and
    an index alone is not content.
    """
    rows = [r for r in rule_rows(page)
            if y0 - 2 <= r[1] <= y1 + 2 and r[2] - r[0] >= 0.5 * (x1 - x0)]
    if len(rows) < 3:
        return None
    top = rows[0]
    body_top = rows[1][3]
    inside = [(bb, t) for bb, t in text_rows
              if body_top - 2 < bb[1] and bb[3] < y1 + 2
              and top[0] - 4 < bb[0] and bb[2] < top[2] + 4]
    if any(len(t.strip()) > 1 and not PROMPT.match(t) for _, t in inside):
        return None
    if columns([(bb[0], t) for bb, t in inside]) >= 2:
        return None
    for d in page.get_drawings():
        r = d['rect']
        # A ROW of the table is not content in it. Agricultural Science draws
        # its answer boxes as one rectangle per ruled line, and counting those
        # as "something is drawn in the body" made every blank box on the
        # paper read as a table with content -- a card for "Identify the
        # correct explanation for marbling by placing a tick in the correct
        # box" came out carrying an empty two-line box.
        if r.width >= 0.8 * (top[2] - top[0]) and r.height <= 30.0:
            continue
        if (r.width > 4 and r.height > 4 and body_top < r.y0
                and r.y1 < y1 + 2 and top[0] - 4 < r.x0 and r.x1 < top[2] + 4):
            return None
    for im in page.get_images(full=True):
        for ir in page.get_image_rects(im[0]):
            if is_a_rule(ir.x0, ir.y0, ir.x1, ir.y1):
                continue
            if (body_top < ir.y0 and ir.y1 < y1 + 2
                    and top[0] - 4 < ir.x0 and ir.x1 < top[2] + 4):
                return None
    return top[1]


def clipped_table_top(page, x0, y0, x1, y1):
    """Where a table the band CUT IN HALF starts, or None.

    2022 OL Q11 prints three photographs and, under them, the table the
    candidate names the components in. The band stopped in the middle of that
    table's header, so the crop was three photographs plus two-thirds of a
    row. A figure is never half a table: where the table's own rules carry on
    past the foot of the band, the table is not part of the figure and the
    crop ends above it.
    """
    rows = [r for r in rule_rows(page) if r[2] - r[0] >= 0.5 * (x1 - x0)]
    inside = [r for r in rows if y0 + 4 < r[1] < y1 - 2]
    if not inside:
        return None
    top = min(inside, key=lambda r: r[1])
    width = top[2] - top[0]
    below = [r for r in rows
             if 0 < r[1] - y1 <= 45.0
             and min(r[2], top[2]) - max(r[0], top[0]) >= 0.8 * width]
    return top[1] if below else None


def trim_blank_box_right(page, x0, y0, x1, y1, text_rows):
    """Cut a blank ruled box off the RIGHT of a band.

    2022 OL Q13(b) prints its binary digits with the candidate's "Answer:" box
    beside them rather than beneath, so trimming only the foot left the blank
    box in the crop. Half the band's height is what separates an answer box
    standing alongside the figure from a cell inside it.
    """
    for _ in range(4):
        cut = None
        for d in page.get_drawings():
            r = d['rect']
            # Vertically inside this band too. Without it, 2022 OL Q13(a)
            # was trimmed by the answer box belonging to (b) further down the
            # page -- the x test alone matched a rectangle 40pt below the
            # band and took the photograph of the clock with it.
            if not (y0 - 2.0 <= r.y0 and r.y1 <= y1 + 2.0):
                continue
            if not (x0 + 10.0 < r.x0 < x1 - 20.0 and x1 - 6.0 <= r.x1 <= x1 + 6.0):
                continue
            if r.height < 0.5 * (y1 - y0) or r.width < 40.0:
                continue
            if not is_blank_box(page, r, text_rows):
                continue
            # A blank COLUMN of the same table is not a box standing beside
            # it. Agricultural Science's tick-box tables put the options in
            # one column and the box to tick in the next, and cutting the
            # second left the student a table with its answer column sliced
            # off. A horizontal rule that runs from the band's left edge
            # across the box is the table's own rule, and says so.
            if any(row[0] <= x0 + 4 and row[2] >= r.x1 - 4
                   and r.y0 - 4 <= row[1] <= r.y1 + 4
                   for row in rule_rows(page)):
                continue
            cut = r.x0 - 8.0 if cut is None else min(cut, r.x0 - 8.0)
        if cut is None or cut <= x0:
            break
        x1 = cut
    return x1


def trim_blank_tail(page, x0, y0, x1, y1, text_rows):
    """Cut empty writing space off the foot of a band.

    2021 HL Q8 prints "1F44D" over a row of boxes with the first four bits
    filled in, inside one tall rectangle the candidate completes. The given
    bits are printed matter and the crop must keep them; the 300pt of blank
    paper under them is where the student writes, and showing it is just a
    large empty box under the answer.

    Only whitespace goes. The band's own enclosing frame is ignored when
    looking for the last ink, since its bottom edge is the very thing being
    trimmed away from.
    """
    bottom = None
    for bb, _ in text_rows:
        if y0 - 2 < bb[1] and bb[3] < y1 + 2 and x0 - 2 < bb[0] and bb[2] < x1 + 2:
            bottom = bb[3] if bottom is None else max(bottom, bb[3])
    for d in page.get_drawings():
        r = d['rect']
        if r.height >= 0.9 * (y1 - y0) or r.width >= 0.98 * (x1 - x0):
            continue
        if y0 - 2 < r.y0 and r.y1 < y1 + 2 and x0 - 2 < r.x0 and r.x1 < x1 + 2:
            bottom = r.y1 if bottom is None else max(bottom, r.y1)
    for im in page.get_images(full=True):
        for ir in page.get_image_rects(im[0]):
            if is_a_rule(ir.x0, ir.y0, ir.x1, ir.y1):
                continue
            if y0 - 2 < ir.y0 and ir.y1 < y1 + 2 and x0 - 2 < ir.x0 and ir.x1 < x1 + 2:
                bottom = ir.y1 if bottom is None else max(bottom, ir.y1)
    if bottom is None or y1 - bottom < 60.0:
        return y1
    return min(y1, bottom + 10.0)


def trim_answer_box_top(page, x0, y0, x1, y1, text_rows):
    """Cut a blank ruled box off the TOP of a band.

    The same box, at the other end. 2023 HL Q13's crop opened with the ruled
    space part (a) is answered in and only then reached Figure 8, because the
    trims cut from the foot and the right and never from the head.
    """
    for _ in range(12):
        cut = None
        for d in page.get_drawings():
            r = d['rect']
            if not (y0 - 6.0 <= r.y0 <= y0 + 6.0 and y0 + 10.0 < r.y1 < y1 - 2.0):
                continue
            if not (x0 - 2.0 <= r.x0 and r.x1 <= x1 + 2.0):
                continue
            if r.width < 0.8 * (x1 - x0) or r.height < 20.0:
                continue
            if not is_blank_box(page, r, text_rows):
                continue
            cut = r.y1 + 2.0 if cut is None else max(cut, r.y1 + 2.0)
        if cut is None or cut >= y1:
            break
        y0 = cut
    return y0


def trim_answer_box(page, x0, y0, x1, y1, text_rows):
    """Cut a blank ruled box off the bottom of a band.

    2021 OL Q8 prints a flowchart and, directly beneath it, the box the
    candidate writes their trace in. They cluster as one band, and the crop
    showed the student a flowchart with an empty box under it. A rectangle
    that spans the band, runs to its foot, and holds no text at all is that
    box. The width test is what keeps it off a TABLE, whose last row has an
    empty answer cell spanning only its own column.
    """
    for _ in range(12):
        cut = None
        for d in page.get_drawings():
            r = d['rect']
            # Starting inside the band and ending at its foot OR BELOW IT.
            # A band often stops part way down an answer box -- 2021 OL Q13's
            # crop kept the top two centimetres of the "Activity 1:" box under
            # Figure 4 -- and a test that wanted the box to END at the foot
            # could never see those. The upper bound on r.y0 is what keeps a
            # box printed entirely BELOW the band from matching and pulling
            # the crop down into it.
            if not (y0 + 2.0 < r.y0 < y1 - 10.0 and r.y1 >= y1 - 6.0):
                continue
            # 20pt, not 40: an answer box is drawn as one rect PER RULED
            # ROW, each about a line high, so a tall-box test found nothing
            # to cut and the whole stack shipped under the figure. The loop
            # above takes them off one row at a time.
            if not (x0 - 2.0 <= r.x0 and r.x1 <= x1 + 2.0):
                continue
            if r.width < 0.8 * (x1 - x0) or r.height < 20.0:
                continue
            # PROMPTS do not make a box full. "Explain:", "Example 1:",
            # "Role 1:" are printed IN the ruled space to tell the candidate
            # what to write there; a box holding only those is still blank,
            # and 2023 HL Q14 shipped its answer box under the von Neumann
            # diagram because three prompts read as content.
            if any(r.y0 - 2 < ly0 and ly1 < r.y1 + 2
                   and r.x0 - 2 < lx0 and lx1 < r.x1 + 2
                   and not PROMPT.match(txt)
                   for (lx0, ly0, lx1, ly1), txt in text_rows):
                continue
            # Empty of DRAWING as well as of text. 2024 HL Q4 frames its
            # figure in a plain rectangle and draws the state inside it as
            # vector strokes with no text at all, so a text-only test called
            # the figure an answer box and cut it down to its caption. A
            # ruled line is the box's own furniture and does not count.
            inner = [d2['rect'] for d2 in page.get_drawings()
                     if d2['rect'].width > 2.0 and d2['rect'].height > 2.0
                     and r.x0 - 2 < d2['rect'].x0 and d2['rect'].x1 < r.x1 + 2
                     and r.y0 + 2 < d2['rect'].y0 and d2['rect'].y1 < r.y1 - 2]
            # A shaded ROW is the box's own furniture, not content. 2023 HL
            # Q14 tints the "Explain:" row, and that one strip -- full width,
            # a line high -- made the answer box look like a drawing and kept
            # it in the crop under the von Neumann diagram.
            inner = [c for c in inner
                     if not (c.width >= 0.8 * r.width and c.height <= 30.0)]
            if inner:
                continue
            cut = r.y0 - 2.0 if cut is None else min(cut, r.y0 - 2.0)
        if cut is None or cut <= y0:
            break
        y1 = cut
    return y1


def is_a_rule(x0, y0, x1, y1):
    """A ruled line, drawn or placed as an image.

    The answer boxes on these papers draw their rules as wafer-thin full-width
    IMAGES, so "this band contains an image" said yes to every empty box on the
    paper. A rule is furniture whichever way it is printed.
    """
    return (y1 - y0) <= 20.0 and (x1 - x0) >= 200.0


def columns(placed):
    """How many text columns the band holds, from label x positions.

    A table has headers at several x positions across a row -- "INPUTS OUTPUT",
    "A B A AND B". An answer box has one column of prompts hard against its
    left edge and nothing else. Positions within 25pt are the same column.
    """
    xs = sorted(x for x, t in placed if not PROMPT.match(t))
    cols = []
    for x in xs:
        if not cols or x - cols[-1] > 25.0:
            cols.append(x)
    return len(cols)


def has_drawn_shape(page, band):
    """Any stroke in the band that a ruled box could not have made.

    A flowchart has ellipses and diagonal arrows; a logic gate has curves. An
    answer box is rectangles and horizontal rules and nothing else. Curves and
    quads count outright; a line counts when it runs neither across nor down.
    """
    x0, y0, x1, y1 = band
    for d in page.get_drawings():
        r = d['rect']
        if r.x1 < x0 or r.x0 > x1 or r.y1 < y0 or r.y0 > y1:
            continue
        for it in d.get('items', []):
            if it[0] in ('c', 'qu'):
                return True
            if it[0] == 'l':
                (ax, ay), (bx, by) = it[1], it[2]
                if abs(bx - ax) > 2.0 and abs(by - ay) > 2.0:
                    return True
    return False


def prose_inside(page, band):
    """Full sentences of the question printed level with the band.

    A figure's interior is labels and captions. Where whole lines of the
    question's own prose sit inside the band, the band is the QUESTION with a
    picture beside it: 2021 HL Q14 prints a photograph of matchsticks to the
    right of its rules, and the band came out as four lines of the stem with a
    stock photo attached.
    """
    x0, y0, x1, y1 = band
    return sum(1 for ln, t in text_lines(page)
               if len(t) > 40 and y0 - 2 < (ln[1] + ln[3]) / 2 < y1 + 2)


def is_answer_grid(page, band):
    """A column of empty tick boxes standing under a heading.

    2025 OL Q9 and 2024 OL Q14 print "True" and "False" over two columns of
    empty squares. Two headings at two x positions is exactly what a table
    looks like to a column count, so they shipped as figures -- a student
    would have been shown twelve blank boxes. What gives them away is that
    every word in the band is in the heading and nothing is written below it.
    """
    x0, y0, x1, y1 = band
    inside = [ln for ln, _ in text_lines(page)
              if y0 - 2 < ln[1] and ln[3] < y1 + 2
              and x0 - 4 < ln[0] and ln[2] < x1 + 4]
    if not inside:
        return False
    return not any(ln[1] > y0 + 0.3 * (y1 - y0) for ln in inside)


def is_a_figure(labels, has_image, placed=(), page=None, band=None,
                text_rows=()):
    """Does this band hold PRINTED MATTER, or is it an empty answer box?

    Four things say printed matter, and a band needs one of them: it contains
    a real image (not a ruled line placed as one); it names itself ("Figure
    3"); it is laid out in columns, which is what a table is; or it carries a
    stroke no ruled box could make. Everything else on these papers is space
    for the candidate to write in, and cropping it would show a student a
    blank box.
    """
    named = any(FIGURE_REF.match(t) for t in labels)
    if named:
        return True
    if has_image:
        return not (page is not None and band is not None
                    and prose_inside(page, band) >= 2)
    if columns(placed) >= 2:
        return not (page is not None and band is not None
                    and is_answer_grid(page, band))
    # A ruled table whose BODY HOLDS WORDS is printed matter, whatever its
    # column count. This is the exact inverse of answer_table_top(), which
    # refuses a table whose body is empty under a filled header, and without
    # it a single-column table of options reads as an answer box: Agricultural
    # Science asks "Identify the conditions necessary for germination by
    # placing a tick in the correct box" over three rows reading "Light, heat
    # and oxygen", "Water, light and heat", "Water, heat and oxygen", and a
    # card that cannot show them cannot be answered.
    if page is not None and band is not None:
        rows = [r for r in rule_rows(page)
                if band[1] - 4 <= r[1] <= band[3] + 4]
        # POSITIVE evidence, not the absence of a verdict. Asking whether
        # answer_table_top() declined to call it an answer table was wrong:
        # that function returns None both for "this table has content" and for
        # "fewer than three rules, I cannot tell", and a three-line empty
        # answer box has two. What makes a table printed matter is words in
        # it, so that is what is tested.
        words = [t for (bx0, by0, bx1, by1), t in text_rows
                 if band[0] - 4 < bx0 and bx1 < band[2] + 4
                 and band[1] - 2 < by0 and by1 < band[3] + 2
                 and len(t.strip()) > 1 and not PROMPT.match(t)]
        if len(rows) >= 2 and words:
            return True
    if page is not None and band is not None and has_drawn_shape(page, band):
        return True
    return False


def figure_bands(page, mono):
    """Tables and diagrams: artwork runs the question's prose does not break.

    `mono` is the code runs already cropped from this page. A listing sits in
    a shaded box, and that box is a drawing rectangle -- without excluding it
    the same program ships twice, once as code and once as a figure.
    """
    rects = sorted(artwork(page), key=lambda r: r[1])
    if not rects:
        return []
    images = []
    for im in page.get_images(full=True):
        for r in page.get_image_rects(im[0]):
            if is_a_rule(r.x0, r.y0, r.x1, r.y1):
                continue
            images.append((r.x0, r.y0, r.x1, r.y1))
    text_rows = [(ln, t) for ln, t in text_lines(page)]
    prose = [ln for ln, t in text_rows
             if len(t) > LABEL_MAX and not FURNITURE.match(t)]

    groups, cur = [], [rects[0]]
    for r in rects[1:]:
        foot = max(c[3] for c in cur)
        split = any(foot < ln[1] and ln[3] < r[1] for ln in prose)
        if split or r[1] - foot > 90:
            groups.append(cur)
            cur = []
        cur.append(r)
    groups.append(cur)

    out = []
    for g in groups:
        x0 = min(r[0] for r in g)
        y0 = min(r[1] for r in g)
        x1 = max(r[2] for r in g)
        y1 = max(r[3] for r in g)
        y1 = follow_table(page, x0, y0, x1, y1, prose)
        # A table is as wide as its own RULES. artwork() keeps only strokes
        # over 2pt, which is right for finding bands and wrong for the width:
        # Agricultural Science shades the option cells of a tick-box table and
        # draws the box to tick as thin outlines, so the band stopped at the
        # options and the crop showed a table with its answer column sliced
        # off. Only rules that already overlap the band count, so a rule
        # belonging to something else on the page cannot widen it.
        spanning = [r for r in rule_rows(page)
                    if y0 - 4 <= r[1] <= y1 + 4
                    and min(r[2], x1) - max(r[0], x0) > 0]
        if spanning:
            x0 = min([x0] + [r[0] for r in spanning])
            x1 = max([x1] + [r[2] for r in spanning])
        if x1 - x0 < MIN_W or y1 - y0 < MIN_H:
            continue
        # Wholly inside a code run already cropped: that is its shading.
        if any(y0 >= my0 - 6 and y1 <= my1 + 6 for _, my0, _, my1, _ in mono):
            continue
        labels, placed = [], []
        for _ in range(2):
            for ln, text in text_rows:
                if (FURNITURE.match(text) or PART_MARKER.match(text)
                        or len(text) > LABEL_MAX or STRAY_WORD.fullmatch(text)):
                    continue
                lx0, ly0, lx1, ly1 = ln
                if ly0 < y0 - 4 or ly1 > y1 + 4:
                    continue
                if lx0 < x0 - 20 or lx0 > x1 + 20:
                    continue
                x0, y0 = min(x0, lx0), min(y0, ly0)
                x1, y1 = max(x1, lx1), max(y1, ly1)
                if text not in labels:
                    labels.append(text)
                    placed.append((lx0, text))
        # Clamp to the prose above and below rather than padding into it.
        for ln, text in text_rows:
            if text in labels or FURNITURE.match(text):
                continue
            lx0, ly0, lx1, ly1 = ln
            if lx1 < x0 - 4 or lx0 > x1 + 4:
                continue
            if ly1 <= y0:
                y0 = max(y0, ly1 + 2)
            elif ly0 >= y1:
                y1 = min(y1, ly0 - 2)
        y0 = trim_answer_box_top(page, x0, y0, x1, y1, text_rows)
        y1 = trim_blank_tail(page, x0, y0, x1, y1, text_rows)
        y1 = trim_answer_box(page, x0, y0, x1, y1, text_rows)
        x1 = trim_blank_box_right(page, x0, y0, x1, y1, text_rows)
        # An empty-bodied answer table is not part of the figure. Where
        # cutting it leaves nothing, the band WAS the answer table and there
        # is no figure here at all.
        cut = answer_table_top(page, x0, y0, x1, y1, text_rows)
        if cut is not None:
            if cut - 2.0 - y0 < MIN_H:
                continue
            y1 = cut - 2.0
        else:
            cut = clipped_table_top(page, x0, y0, x1, y1)
            if cut is not None and cut - 2.0 - y0 >= MIN_H:
                y1 = cut - 2.0
        if any(BANNER.match(t) for t in labels):
            continue
        # Contained on ALL four sides. The earlier test bounded only the left
        # and the vertical, so an answer box printed beside a photograph
        # counted as holding it and shipped as a figure.
        has_image = any(ix0 >= x0 - 2 and ix1 <= x1 + 2
                        and iy0 >= y0 - 2 and iy1 <= y1 + 2
                        for ix0, iy0, ix1, iy1 in images)
        if not is_a_figure(labels, has_image, placed, page, (x0, y0, x1, y1),
                           text_rows):
            continue
        if y1 - y0 >= MIN_H:
            out.append((x0, y0, x1, y1, labels))
    return out


def text_lines(page):
    for bl in page.get_text('dict')['blocks']:
        for ln in bl.get('lines', []):
            text = ' '.join(''.join(s['text'] for s in ln['spans']).split())
            if text:
                yield tuple(ln['bbox']), text


QHEAD_LINE = re.compile(r'^\s*Question\s+(\d{1,2})\b')


_HEADINGS = {}


def _headings(P):
    """(path, page, height, [(y, question no)]) for every page of a paper.

    Cached. Without it every question rescanned every page of its paper, and
    the authoring run -- which asks for one question's crop at a time -- went
    from seconds to minutes.
    """
    key = tuple(P.files)
    if key not in _HEADINGS:
        pages = []
        for path in P.files:
            with pymupdf.open(path) as doc:
                for n in range(doc.page_count):
                    heads = []
                    for bb, text in text_lines(doc[n]):
                        m = QHEAD_LINE.match(text)
                        if m:
                            heads.append((bb[1], int(m.group(1))))
                    pages.append((path, n, doc[n].rect.height, sorted(heads)))
        _HEADINGS[key] = pages
    return _HEADINGS[key]


def question_regions(P, q):
    """(path, page index, top, bottom) for everything Question q owns.

    A question owns the paper from its own heading to the NEXT question's
    heading, and that often runs onto the following page: 2021 HL Q13 prints
    "This question continues on the next page" and its eircode listing is over
    the fold. Matching only pages that carry the heading missed every one of
    those, so the listing was never cropped and stayed in the card's stem as
    "1 def is_valid_eircode(test_eircode): 2 3 # This function checks".
    """
    pages = _headings(P)
    out, open_at = [], None
    for path, n, height, heads in pages:
        mine = next((y for y, num in heads if num == q), None)
        if mine is not None:
            open_at = mine
        elif open_at is None:
            continue
        else:
            open_at = 0.0
        if open_at is None:
            continue
        later = [y for y, num in heads if num != q and y > open_at + 2]
        bottom = min(later) if later else height
        out.append((path, n, open_at, bottom))
        if later:
            open_at = None
            break
        open_at = 0.0
    return out


def question_span(page, q):
    """The vertical slice of this page that belongs to Question q.

    Two questions often share a page, and matching the page alone gave each of
    them BOTH figures: 2023 OL Q9's discrete-data table and Q10's OR gate came
    back against Q9 and against Q10. The span runs from this question's own
    heading to the next question's heading, or to the foot of the page.
    """
    heads = []
    for bb, text in text_lines(page):
        m = QHEAD_LINE.match(text)
        if m:
            heads.append((bb[1], int(m.group(1))))
    heads.sort()
    top = next((y for y, n in heads if n == q), None)
    if top is None:
        return 0.0, page.rect.height
    later = [y for y, n in heads if y > top + 2]
    return top, (min(later) if later else page.rect.height)


def crop(year, level, q, write=False):
    P = PP.Paper('computer-science', year, level)
    made = []
    for path, n, top, bot in question_regions(P, q):
        with pymupdf.open(path) as doc:
            page = doc[n]
            # The span bounds the CODE too. Bounding only the figure bands
            # gave every question the listing printed for the one above it
            # when the two shared a page -- 2024 HL Q2's crop came out byte
            # for byte identical to Q1's.
            all_runs = mono_runs(page)
            runs = [r for r in all_runs if top - 4 <= r[1] and r[3] <= bot + 4]
            for i, (x0, y0, x1, y1, lines) in enumerate(runs):
                rect = pymupdf.Rect(max(0, x0 - PAD_X), max(0, y0 - PAD_Y),
                                    min(page.rect.width, x1 + PAD_X),
                                    min(page.rect.height, y1 + PAD_Y))
                name = (f'computer-science-{year}-{level.upper()}-paper-'
                        f'q{q}-code{i}')
                if write:
                    d = os.path.join(ROOT, 'exam-papers', 'computer-science',
                                     'figures', f'{year}-{level}')
                    os.makedirs(d, exist_ok=True)
                    page.get_pixmap(clip=rect, dpi=DPI).save(
                        os.path.join(d, f'{name}.png'))
                made.append((name, n, rect, lines, 'code'))
            # figure_bands is given ALL the page's code runs, not just this
            # question's: a listing belonging to the question above still
            # shades a rectangle this one must not mistake for a figure.
            bands = [b for b in figure_bands(page, all_runs)
                     if top - 4 <= b[1] and b[3] <= bot + 4]
            for i, (x0, y0, x1, y1, labels) in enumerate(bands):
                # A few points of air. Without it the crop lands exactly on
                # the table's last rule and the row beneath the final gate is
                # shaved off, which reads as a clipped drawing.
                rect = pymupdf.Rect(max(0, x0 - PAD_X), max(0, y0 - 3.0),
                                    min(page.rect.width, x1 + PAD_X),
                                    min(page.rect.height, y1 + 4.0))
                name = (f'computer-science-{year}-{level.upper()}-paper-'
                        f'q{q}-fig{i}')
                if write:
                    d = os.path.join(ROOT, 'exam-papers', 'computer-science',
                                     'figures', f'{year}-{level}')
                    os.makedirs(d, exist_ok=True)
                    page.get_pixmap(clip=rect, dpi=DPI).save(
                        os.path.join(d, f'{name}.png'))
                made.append((name, n, rect, labels, 'fig'))
    return made


def describe(year, level, q, lines):
    body = [' '.join(t.split()) for t in lines if t.strip()]
    opener = next((b for b in body if len(b) > 3), '')
    return (f'The program printed with {year} {level.upper()} Question {q}, '
            f'as the State Examinations Commission set it, with its line '
            f'numbers and indentation. It runs to {len(body)} lines and '
            f'begins: {opener[:120]}')


def describe_figure(year, level, q, labels):
    """What a table or diagram crop says to a screen reader.

    Names the question and lists the labels the crop actually contains, which
    is all that can be said about a picture without describing it from a guess.
    Every crop is opened and looked at before it is bound.
    """
    text = (f'The table or diagram printed with {year} {level.upper()} '
            f'Question {q}, as the State Examinations Commission set it.')
    if labels:
        text += ' It is labelled: ' + ', '.join(labels[:14]) + '.'
    return text


def gap_is_clear(page, x0, y0, x1, y1, text_rows):
    """Is the space between two bands free of the candidate's answer space?

    Distance alone was the wrong test. Section C prints three listings down a
    page with the ask between them, and refusing to join them cost twelve
    questions a figure they already shipped with. What must not end up inside
    a joined crop is a BLANK BOX -- the ruled space the candidate writes in.
    """
    for d in page.get_drawings():
        r = d['rect']
        if r.width < 60.0 or r.height < 20.0:
            continue
        if r.y1 <= y0 or r.y0 >= y1 or r.x1 <= x0 or r.x0 >= x1:
            continue
        if is_blank_box(page, r, text_rows):
            return False
    return True


def describe_question_figure(year, level, q, made):
    """What the question's single crop says to a screen reader.

    A crop of one kind keeps that kind's own wording -- a listing is described
    by its length and opening line, a diagram by the labels it carries. Only a
    crop holding both needs a sentence of its own.
    """
    kinds = {k for _, _, _, _, k in made}
    lines = [t for _, _, _, ls, k in made for t in ls]
    if kinds == {'code'}:
        return describe(year, level, q, lines)
    if kinds == {'fig'}:
        return describe_figure(year, level, q, lines)
    text = (f'The program and the table or diagram printed with {year} '
            f'{level.upper()} Question {q}, as the State Examinations '
            f'Commission set it.')
    labels = [' '.join(t.split()) for _, _, _, ls, k in made if k == 'fig'
              for t in ls if t.strip()]
    if labels:
        text += ' The table or diagram is labelled: ' + ', '.join(labels[:14]) + '.'
    return text


def whole_lines(year, level, q, page_no, rect):
    """Widen a joined crop so no line of type is sliced down the middle.

    The union of two bands is only as wide as the wider band, and the
    question's own sentence printed between them then came out cut mid-word:
    "ts of 7, 3 and 8 for n, complete the trace table". A crop may leave a
    line out, but it must not show half of one.
    """
    P = PP.Paper('computer-science', year, level)
    path = next(p for p, n, _, _ in question_regions(P, q) if n == page_no)
    with pymupdf.open(path) as doc:
        page = doc[page_no]
        x0, x1 = rect.x0, rect.x1
        for (lx0, ly0, lx1, ly1), _ in text_lines(page):
            if ly1 <= rect.y0 or ly0 >= rect.y1:
                continue
            if lx1 <= x0 or lx0 >= x1:
                continue
            x0, x1 = min(x0, lx0 - 2), max(x1, lx1 + 2)
        return pymupdf.Rect(max(0.0, x0), rect.y0,
                            min(page.rect.width, x1), rect.y1)


LETTER = re.compile(r'^\(?([A-H])\)?$')


def letters_in(page, rect):
    """Standalone capital letters printed INSIDE the crop.

    Card lint refuses a card that names a lettered part unless the figure it
    carries records the letters it shows -- otherwise a student is asked about
    "the symbol labelled A" with no A in front of them. This reads them off
    the crop rather than taking anyone's word: 2022 OL Q6 prints an A inside
    one of its flowchart's decision diamonds.
    """
    out = []
    for (lx0, ly0, lx1, ly1), text in text_lines(page):
        if rect.x0 - 2 > lx0 or lx1 > rect.x1 + 2:
            continue
        if rect.y0 - 2 > ly0 or ly1 > rect.y1 + 2:
            continue
        m = LETTER.match(text.strip())
        if m and m.group(1) not in out:
            out.append(m.group(1))
    return sorted(out)


def question_figure(year, level, q, write=False):
    """The ONE image a card for this question may carry, or None.

    A card cites a part, and the part cannot be matched to a band on the page
    with any certainty. So a question with several bands gets ONE crop holding
    all of them, and never a subset: attaching the topmost band would have
    shown 2022 OL Q13(b) the four binary digits printed for (a), which is
    worse than showing nothing.

    Where the bands are far apart, the space between them is the candidate's
    answer space or another part's ask, and there is no honest single crop.
    The question then carries no figure and its asks stay open.
    """
    made = crop(year, level, q, write=False)
    if not made:
        return None
    # A question can now own several pages, and its figure comes from the one
    # carrying its HEADING -- that is where the paper prints the stimulus the
    # question is built on. A later page holds the parts' own material, and
    # picking across pages would put one part's listing on another's card.
    head = min(n for _, n, _, _, _ in made)
    made = [m for m in made if m[1] == head]
    made = sorted(made, key=lambda m: m[2].y0)
    page_no = made[0][1]
    if len(made) > 1:
        P = PP.Paper('computer-science', year, level)
        path = next(p for p, n, _, _ in question_regions(P, q) if n == page_no)
        with pymupdf.open(path) as doc:
            page = doc[page_no]
            rows = list(text_lines(page))
            for a, b in zip(made, made[1:]):
                if b[2].y0 - a[2].y1 <= 4.0:
                    continue
                if not gap_is_clear(page, min(a[2].x0, b[2].x0), a[2].y1,
                                    max(a[2].x1, b[2].x1), b[2].y0, rows):
                    # The candidate's answer space sits between them, so no
                    # single rectangle holds both and there is no honest
                    # crop. Stacking the two bands into one sheet was tried
                    # and is worse: the bands overlap each other, so each
                    # table came out twice with the answer box between them.
                    return None
    if len(made) == 1:
        name, rect = made[0][0], made[0][2]
    else:
        name = f'computer-science-{year}-{level.upper()}-paper-q{q}-figure'
        rect = pymupdf.Rect(min(m[2].x0 for m in made), min(m[2].y0 for m in made),
                            max(m[2].x1 for m in made), max(m[2].y1 for m in made))
        rect = whole_lines(year, level, q, page_no, rect)
    if write:
        P = PP.Paper('computer-science', year, level)
        path = next(p for p, n, _, _ in question_regions(P, q) if n == page_no)
        d = os.path.join(ROOT, 'exam-papers', 'computer-science', 'figures',
                         f'{year}-{level}')
        os.makedirs(d, exist_ok=True)
        with pymupdf.open(path) as doc:
            doc[page_no].get_pixmap(clip=rect, dpi=DPI).save(
                os.path.join(d, f'{name}.png'))
    P = PP.Paper('computer-science', year, level)
    path = next(p for p, n, _, _ in question_regions(P, q) if n == page_no)
    with pymupdf.open(path) as doc:
        letters = letters_in(doc[page_no], rect)
    # The lines THIS crop carries, split by kind. Only these may be taken out
    # of a card's question text: a listing the bound crop does not show is
    # still the only place a student can read it, and removing it would leave
    # "Explain what the following code does:" with no code anywhere.
    code = [t for _, _, _, ls, k in made if k == 'code' for t in ls]
    labels = [t for _, _, _, ls, k in made if k == 'fig' for t in ls]
    return (name, rect, describe_question_figure(year, level, q, made),
            letters, code, labels)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('year', nargs='?', type=int)
    ap.add_argument('level', nargs='?')
    ap.add_argument('q', nargs='?', type=int)
    ap.add_argument('--write', action='store_true')
    ap.add_argument('--catalogue', action='store_true')
    args = ap.parse_args()

    if args.q:
        targets = [(args.year, args.level, args.q)]
    else:
        sys.path.insert(0, DIR)
        import reconcile as R                                # noqa: E402
        from paper_census import census_subject              # noqa: E402
        idx = R.leaf_index(census_subject('computer-science'))
        seen = collections.OrderedDict()
        for (yr, lv, _), leaves in sorted(idx.items()):
            for leaf in leaves:
                seen.setdefault((yr, lv, leaf[1]), None)
        targets = list(seen)

    catalogue, total = [], 0
    for year, level, q in targets:
        try:
            chosen = question_figure(year, level, q,
                                     write=args.write or args.catalogue)
        except Exception as exc:                             # noqa: BLE001
            print(f'{year} {level} Q{q}: {type(exc).__name__}: {exc}')
            continue
        if chosen is None:
            continue
        name, rect, description, letters = chosen[:4]
        total += 1
        if args.catalogue:
            catalogue.append({
                'file': f'{name}.png', 'kind': 'figure', 'truncated': False,
                'questionRef': f'{year} {level.upper()} Q{q}',
                'description': description,
                'lettersVisible': letters,
            })
        elif not args.write:
            print(f'{year} {level.upper()} Q{q}: {name}  '
                  f'{round(rect.width)}x{round(rect.height)}')
    if args.catalogue:
        print(json.dumps(catalogue, ensure_ascii=False, indent=1))
    elif not args.q:
        print(f'TOTAL {total} question figure(s)')


if __name__ == '__main__':
    main()
