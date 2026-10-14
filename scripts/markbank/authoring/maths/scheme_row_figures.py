"""Crop a Mathematics part's whole printed scheme row -- model solution AND marking notes.

    python3 scripts/markbank/authoring/maths/scheme_row_figures.py <year> <hl|ol> [--write | --publish [p1|p2]]

Why: the 2019 Ordinary Level scheme's text layer cannot carry everything it
prints. Its subscripts and superscripts extract as unrelated ASCII (z2 reads as
"z8", f' as "fL", 2^(2x-1) as "28TE;"), which no glyph map can repair because
the characters are ordinary ASCII, and a stacked fraction's denominator sits on
a line of its own that the provenance reader filters as a mark cell. Marking
points that depend on either cannot be lifted as text, so they were left out of
the card's rows. This attaches the SEC's own print of the part instead: the
table row holding the part's model solution and its marking notes (every credit
band the scheme prints), cropped from the scheme PDF and shown only after the
reveal (CardFigure.solution).

How a row is found -- geometry, not prose: the scheme is a three-column table
(part label | model solution | marking notes) ruled by horizontal lines. The
part's label sits in the label column ("(a)(iii)", "(a)(i)+(ii)", "(b)"), on
the scheme page the review names; the row runs from the rule above the label
to the next rule below it. Nothing is typed: the crop is the printed row.

Outputs (with --write):
  exam-papers/maths/figures/<year>-<level>/maths-<year>-<LEVEL>-scheme-p<page>-i<n>.png
  scripts/markbank/authored/maths-scheme-row-figures-catalogue.json   (entries for this sitting)
The catalogue's descriptions are machine-drafted from the row's own text and
then checked by opening each crop.

With --publish the inspected crops are copied to public/exam-figures/maths/markbank/
and entered in components/MarkBank/figures.json in the shape bind-figures.mjs
writes. The entries are inserted textually: figures.json mixes escaped and raw
Unicode from earlier writers, so rewriting the whole object would restyle
thousands of unrelated lines in a file every subject shares.
"""
import hashlib
import shutil
import json
import os
import re
import sys

import pymupdf

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..'))
LEVEL = {'hl': 'higher', 'ol': 'ordinary'}
LEVEL_WORD = {'hl': 'Higher Level', 'ol': 'Ordinary Level'}
SCHEME = {'hl': 'LC003ALP000EV.pdf', 'ol': 'LC003GLP000EV.pdf'}
CATALOGUE = os.path.join(ROOT, 'scripts', 'markbank', 'authored', 'maths-scheme-row-figures-catalogue.json')
DPI = 200

# The cards whose printed scheme content could not be lifted as text, per sitting.
AFFECTED = {
    (2019, 'ol'): [
        'maths-2019-ol-p1-q2-a-i', 'maths-2019-ol-p1-q2-a-iii', 'maths-2019-ol-p1-q2-b', 'maths-2019-ol-p1-q3-b',
        'maths-2019-ol-p1-q4-b', 'maths-2019-ol-p1-q5-a', 'maths-2019-ol-p1-q6-b', 'maths-2019-ol-p1-q7-c-i',
        'maths-2019-ol-p1-q7-d-i', 'maths-2019-ol-p1-q7-d-ii', 'maths-2019-ol-p1-q7-d-iii', 'maths-2019-ol-p1-q8-a-i',
        'maths-2019-ol-p1-q8-b-ii', 'maths-2019-ol-p1-q8-b-iii', 'maths-2019-ol-p1-q8-b-iv', 'maths-2019-ol-p1-q8-b-v',
        'maths-2019-ol-p1-q8-b-vi', 'maths-2019-ol-p1-q9-a', 'maths-2019-ol-p1-q9-b', 'maths-2019-ol-p1-q9-c-iii',
        'maths-2019-ol-p1-q9-d',
        'maths-2019-ol-p2-q1-a', 'maths-2019-ol-p2-q1-b', 'maths-2019-ol-p2-q1-c-i', 'maths-2019-ol-p2-q1-c-ii',
        'maths-2019-ol-p2-q2-a', 'maths-2019-ol-p2-q2-b', 'maths-2019-ol-p2-q2-d', 'maths-2019-ol-p2-q3-d',
        'maths-2019-ol-p2-q4-b', 'maths-2019-ol-p2-q4-c', 'maths-2019-ol-p2-q4-d', 'maths-2019-ol-p2-q5-a',
        'maths-2019-ol-p2-q5-b', 'maths-2019-ol-p2-q7-c-i', 'maths-2019-ol-p2-q8-a-i', 'maths-2019-ol-p2-q8-a-ii',
        'maths-2019-ol-p2-q8-a-iii', 'maths-2019-ol-p2-q8-b-i', 'maths-2019-ol-p2-q8-b-ii', 'maths-2019-ol-p2-q8-b-iii',
        'maths-2019-ol-p2-q9-a', 'maths-2019-ol-p2-q9-b', 'maths-2019-ol-p2-q9-c', 'maths-2019-ol-p2-q9-d-i',
        'maths-2019-ol-p2-q9-d-ii', 'maths-2019-ol-p2-q9-d-iii',
    ],
    # 2018 Higher: model-solution lines whose stacked-fraction numerator extracts
    # as a lone "1" (filtered as a mark cell), integral limits the text layer
    # drops (Q3(b)), and model solutions printed as images (the Q9(a) table, the
    # Q6(b)(ii), Q7(c) and Q7(d) graphs).
    (2018, 'hl'): [
        'maths-2018-hl-p1-q3-b', 'maths-2018-hl-p1-q6-b-ii', 'maths-2018-hl-p1-q7-c', 'maths-2018-hl-p1-q7-d', 'maths-2018-hl-p1-q7-e-ii',
        'maths-2018-hl-p1-q8-a', 'maths-2018-hl-p1-q8-b', 'maths-2018-hl-p1-q8-c', 'maths-2018-hl-p1-q8-d',
        'maths-2018-hl-p1-q9-a', 'maths-2018-hl-p1-q9-c-i',
        # Paper 2: working that refers to a diagram or graph in the scheme, the
        # Q8(b)(i) tick table, and the Q8(c) present-value sum.
        'maths-2018-hl-p2-q4-b', 'maths-2018-hl-p2-q6-a', 'maths-2018-hl-p2-q7-d', 'maths-2018-hl-p2-q8-b-i',
        'maths-2018-hl-p2-q8-c', 'maths-2018-hl-p2-q9-b-iii',
    ],
    # 2018 Ordinary: model solutions printed as images (the P1 Q2(a) Argand
    # diagram, Q4(a) tile diagram, Q8(c) graph) and the P1 Q3(a) roots formula,
    # whose denominator is filtered as a mark cell.
    (2018, 'ol'): [
        'maths-2018-ol-p1-q2-a', 'maths-2018-ol-p1-q3-a', 'maths-2018-ol-p1-q4-a', 'maths-2018-ol-p1-q8-c',
        # Paper 2: a completed table, a construction, a scatterplot and a tick box
        # printed as images, and stacked fractions filtered as mark cells.
        'maths-2018-ol-p2-q1-a-i', 'maths-2018-ol-p2-q6-a-i', 'maths-2018-ol-p2-q7-f-i', 'maths-2018-ol-p2-q7-f-ii',
        'maths-2018-ol-p2-q8-e', 'maths-2018-ol-p2-q8-f', 'maths-2018-ol-p2-q9-a-i', 'maths-2018-ol-p2-q9-a-iii',
        'maths-2018-ol-p2-q9-b-i',
    ],
    # 2017 Higher Paper 1: stacked fractions filtered as mark cells, the Q3(b)
    # high partial credit whose f and g extract as unassigned code points, and
    # model solutions printed as images (the Q5(a) long division, the Q6 and Q9(a)
    # graphs).
    # 2017 Ordinary Paper 1: stacked fractions filtered as mark cells, the Q7(a)
    # tile pattern and the Q8(c)(ii) graph.
    (2017, 'ol'): [
        'maths-2017-ol-p1-q1-b', 'maths-2017-ol-p1-q1-c', 'maths-2017-ol-p1-q2-a-iii', 'maths-2017-ol-p1-q3-a', 'maths-2017-ol-p1-q3-b',
        'maths-2017-ol-p1-q5-a', 'maths-2017-ol-p1-q5-b', 'maths-2017-ol-p1-q6-b', 'maths-2017-ol-p1-q7-a', 'maths-2017-ol-p1-q7-d-i',
        'maths-2017-ol-p1-q7-d-ii', 'maths-2017-ol-p1-q8-c-ii', 'maths-2017-ol-p1-q8-d', 'maths-2017-ol-p1-q9-c', 'maths-2017-ol-p1-q9-e-i',
        'maths-2017-ol-p1-q9-e-ii', 'maths-2017-ol-p1-q9-e-iii',
        # Paper 2: stacked fractions, mangled bold maths and image-only solutions.
        'maths-2017-ol-p2-q1-a-ii', 'maths-2017-ol-p2-q1-b-i', 'maths-2017-ol-p2-q1-c-i', 'maths-2017-ol-p2-q2-b-ii', 'maths-2017-ol-p2-q2-c',
        'maths-2017-ol-p2-q3-a-ii', 'maths-2017-ol-p2-q3-b', 'maths-2017-ol-p2-q3-c', 'maths-2017-ol-p2-q4-a', 'maths-2017-ol-p2-q4-b-ii',
        'maths-2017-ol-p2-q5-a-ii', 'maths-2017-ol-p2-q5-b', 'maths-2017-ol-p2-q6-a', 'maths-2017-ol-p2-q7-b-ii', 'maths-2017-ol-p2-q7-b-iii',
        'maths-2017-ol-p2-q7-c-i', 'maths-2017-ol-p2-q8-b', 'maths-2017-ol-p2-q8-c-i', 'maths-2017-ol-p2-q8-c-iii', 'maths-2017-ol-p2-q9-a-ii',
        'maths-2017-ol-p2-q9-b-i', 'maths-2017-ol-p2-q9-b-ii', 'maths-2017-ol-p2-q9-c-i', 'maths-2017-ol-p2-q9-c-ii',
    ],
    (2017, 'hl'): [
        'maths-2017-hl-p1-q1-c-ii', 'maths-2017-hl-p1-q3-b', 'maths-2017-hl-p1-q4-b', 'maths-2017-hl-p1-q5-a',
        'maths-2017-hl-p1-q6-a', 'maths-2017-hl-p1-q6-b', 'maths-2017-hl-p1-q7-f', 'maths-2017-hl-p1-q8-a',
        'maths-2017-hl-p1-q8-b-v', 'maths-2017-hl-p1-q9-a', 'maths-2017-hl-p1-q9-b-ii',
        # Paper 2 sets most of its working as stacked fractions, binomial
        # coefficients and diagrams: every part that lost a line or a band.
        'maths-2017-hl-p2-q1-a', 'maths-2017-hl-p2-q1-b', 'maths-2017-hl-p2-q1-c', 'maths-2017-hl-p2-q1-d', 'maths-2017-hl-p2-q2-b',
        'maths-2017-hl-p2-q2-d-i', 'maths-2017-hl-p2-q2-d-ii', 'maths-2017-hl-p2-q3-a', 'maths-2017-hl-p2-q3-b', 'maths-2017-hl-p2-q3-c',
        'maths-2017-hl-p2-q4-a', 'maths-2017-hl-p2-q4-b', 'maths-2017-hl-p2-q5-b', 'maths-2017-hl-p2-q5-c', 'maths-2017-hl-p2-q5-d',
        'maths-2017-hl-p2-q6-b', 'maths-2017-hl-p2-q7-a', 'maths-2017-hl-p2-q7-b-ii', 'maths-2017-hl-p2-q7-c', 'maths-2017-hl-p2-q8-a-i',
        'maths-2017-hl-p2-q8-a-ii', 'maths-2017-hl-p2-q8-a-iii', 'maths-2017-hl-p2-q8-b-i', 'maths-2017-hl-p2-q8-b-ii', 'maths-2017-hl-p2-q8-b-iii',
        'maths-2017-hl-p2-q9-a', 'maths-2017-hl-p2-q9-b', 'maths-2017-hl-p2-q9-c', 'maths-2017-hl-p2-q9-e', 'maths-2017-hl-p2-q9-f',
    ],
    # 2016 Higher: model solutions printed as images or layouts the text layer
    # cannot carry (graphs, tables, a construction, the long division, the
    # first-principles and sum-to-product working) and bands that cannot be
    # quoted (P1 Q4(b)(ii)'s log_a a). P1 Q1(c), P2 Q3(b) and P2 Q9(a)(iii)
    # continue onto the next page in an unlabelled row.
    (2016, 'hl'): [
        'maths-2016-hl-p1-q1-c', 'maths-2016-hl-p1-q2-a', 'maths-2016-hl-p1-q3-a-i', 'maths-2016-hl-p1-q3-a-ii', 'maths-2016-hl-p1-q3-a-iii',
        'maths-2016-hl-p1-q4-b-ii', 'maths-2016-hl-p1-q6-a', 'maths-2016-hl-p1-q6-b-i', 'maths-2016-hl-p1-q7-b-ii', 'maths-2016-hl-p1-q8-a-iv',
        'maths-2016-hl-p1-q9-a-i', 'maths-2016-hl-p1-q9-a-ii', 'maths-2016-hl-p1-q9-a-iii', 'maths-2016-hl-p1-q9-b-iii',
        'maths-2016-hl-p2-q3-a', 'maths-2016-hl-p2-q3-b', 'maths-2016-hl-p2-q4-a-ii', 'maths-2016-hl-p2-q4-b', 'maths-2016-hl-p2-q5-a-i',
        'maths-2016-hl-p2-q6-b', 'maths-2016-hl-p2-q8-d-i', 'maths-2016-hl-p2-q8-d-ii', 'maths-2016-hl-p2-q9-a-iii',
    ],
    # 2016 Ordinary: model solutions printed as an Argand diagram, completed
    # tables, graphs, a construction, a stem-and-leaf plot, a pie chart and a
    # tree diagram, and bands that cannot be quoted (Q5(b)'s Un, mixed numbers,
    # an italic Q and h the text layer mangles).
    (2016, 'ol'): [
        'maths-2016-ol-p1-q2-b', 'maths-2016-ol-p1-q5-a-i', 'maths-2016-ol-p1-q5-b', 'maths-2016-ol-p1-q8-b-i', 'maths-2016-ol-p1-q8-b-ii',
        'maths-2016-ol-p1-q9-a-i', 'maths-2016-ol-p1-q9-a-ii',
        'maths-2016-ol-p2-q1-a-i', 'maths-2016-ol-p2-q1-a-ii', 'maths-2016-ol-p2-q1-b', 'maths-2016-ol-p2-q3-b', 'maths-2016-ol-p2-q4-b',
        'maths-2016-ol-p2-q4-c', 'maths-2016-ol-p2-q5-b', 'maths-2016-ol-p2-q5-c', 'maths-2016-ol-p2-q6-a-i', 'maths-2016-ol-p2-q8-b-i',
        'maths-2016-ol-p2-q8-b-ii', 'maths-2016-ol-p2-q8-c-i', 'maths-2016-ol-p2-q8-c-ii', 'maths-2016-ol-p2-q8-d', 'maths-2016-ol-p2-q9-a-ii',
        'maths-2016-ol-p2-q9-d', 'maths-2016-ol-p2-q9-e',
    ],
}
# Labels the scheme prints differently from the paper's part label.
PRINTED_LABEL = {
    'maths-2017-hl-p1-q1-c-ii': 'c(ii)',  # printed without the brackets round c
    'maths-2017-hl-p1-q8-b-v': '(v)',     # printed without its (b)
}
# The same label on two rows of one page (2016 Higher P1 page 19 prints (ii)
# under (a) and again under (b)): (label, which occurrence).
PRINTED_LABEL.update({
    'maths-2016-hl-p1-q3-a-i': '(i)', 'maths-2016-hl-p1-q3-a-ii': '(ii)', 'maths-2016-hl-p1-q3-a-iii': '(iii)',
    'maths-2016-hl-p1-q4-b-ii': '(ii)', 'maths-2016-hl-p1-q8-a-iv': '(iv)', 'maths-2016-hl-p1-q7-b-ii': ('(ii)', 2),
    'maths-2016-ol-p1-q8-b-i': 'b(i)', 'maths-2016-ol-p2-q6-a-i': '(a)(i)(ii)',
})
# Rows the label search cannot place, given as visually verified (page, top,
# bottom) table rules: 2016 Higher P1 Q9(a)(iii) prints its change-in-x/y
# table above its labelled row, and P2 Q8(d)(i) sets its model-solution table
# in a box of its own above an unlabelled marking-notes row.
ROW_SPAN = {
    'maths-2016-hl-p1-q9-a-iii': (24, 99.0, 442.6),
    'maths-2016-hl-p2-q8-d-i': (42, 56.9, 322.0),
    # 2016 Ordinary P1 Q5(a)(i)+(ii): one 5C scale over two labelled rows.
    'maths-2016-ol-p1-q5-a-i': (11, 77.2, 571.6),
}
BANDS = ['Low Partial Credit', 'Mid Partial Credit', 'High Partial Credit', 'Partial Credit', 'Full Credit',
         'Zero Credit', 'No Credit', 'Note', 'Special Case', 'Misreading']


def norm_label(t):
    return re.sub(r'\s+', '', t).replace('&', '+')


def part_label(printed):
    """'Q2(a)(iii)' -> '(a)(iii)'; several printed parts join with '+'."""
    first = re.sub(r'^Q\d+', '', printed[0])
    rest = [re.sub(r'^Q\d+(\([a-z]\))?', '', p) for p in printed[1:]]
    return first + ''.join('+' + r for r in rest)


def part_label_long(printed):
    """'Q6(a)(i)','Q6(a)(ii)' -> '(a)(i)+(a)(ii)': the 2018 Ordinary scheme repeats the letter."""
    return '+'.join(re.sub(r'^Q\d+', '', p) for p in printed)


def hsegments(page, min_width=60, max_width=None):
    segs = []
    for d in page.get_drawings():
        for it in d['items']:
            if it[0] == 'l':
                p1, p2 = it[1], it[2]
                w = abs(p1.x - p2.x)
                if abs(p1.y - p2.y) < 0.6 and w > min_width and (max_width is None or w <= max_width):
                    segs.append((round(p1.y, 1), min(p1.x, p2.x), max(p1.x, p2.x)))
            elif it[0] == 're':
                r = it[1]
                if r.height < 1.6 and r.width > min_width and (max_width is None or r.width <= max_width):
                    segs.append((round((r.y0 + r.y1) / 2, 1), r.x0, r.x1))
    return segs


def rules(page):
    """y of each rule of the scheme's own table.

    A table inside a model solution (a stem-and-leaf plot, a probability table)
    draws rules of its own, so only a rule that starts and ends on a column
    boundary of the scheme table counts. The boundaries come from the table's
    header rule, the first rule on the page. A rule drawn as two abutting
    segments (one per cell, as under the 2018 Higher Q9(b)(iii) graph) is one rule.
    """
    segs = []
    for y, a, b in sorted(hsegments(page)):
        if segs and segs[-1][0] == y and a - segs[-1][2] <= 2:
            segs[-1] = (y, segs[-1][1], max(b, segs[-1][2]))
        else:
            segs.append((y, a, b))
    top = min(y for y, _, _ in segs)
    bounds = sorted({round(x, 0) for y, a, b in segs if y <= top + 25 for x in (a, b)})
    # A rule whose label-column piece is drawn as its own short segment (2017
    # Higher Q1(c)(ii)'s bottom border) starts left of the long piece: a rule that
    # misses a header boundary is extended by short segments that abut it.
    shorts = hsegments(page, min_width=5, max_width=60)
    def extend(y, a, b):
        for y2, a2, b2 in shorts:
            if abs(y2 - y) <= 0.3 and abs(b2 - a) <= 2:
                a = a2
            if abs(y2 - y) <= 0.3 and abs(a2 - b) <= 2:
                b = b2
        return y, a, b
    segs = [seg if any(abs(seg[1] - x) < 3 for x in bounds) else extend(*seg) for seg in segs]
    on = lambda x: any(abs(x - b) < 3 for b in bounds)
    # The table can narrow below the header (2018 Ordinary P1 Q8 ends its lower
    # rows at a border left of the header's), so a rule may also END on any of the
    # table's vertical lines; it must still START on a header column boundary,
    # which is what keeps a table drawn inside a model solution out.
    edges = vertical_xs(page)
    ends = lambda x: on(x) or any(abs(x - e) < 3 for e in edges)
    # The header rule's label-column piece is narrower than hsegments' 60pt
    # floor, so in the 2016 Higher scheme the header's first boundary reads as
    # 86, not the table's left border at 57, and a full-width rule drawn as one
    # piece from that border (Q1(c)'s, under its (b)) was dropped. A rule may
    # also start on the table's own left border; a table inside a model
    # solution never reaches it.
    left = min(edges) if edges else None
    starts = lambda x: on(x) or (left is not None and abs(x - left) < 3)
    return sorted({y for y, a, b in segs if starts(a) and ends(b) and b - a > 150})


def table_x(page):
    xs = []
    for d in page.get_drawings():
        for it in d['items']:
            if it[0] == 'l' and abs(it[1].x - it[2].x) < 0.6 and abs(it[1].y - it[2].y) > 20:
                xs.append(it[1].x)
            elif it[0] == 're' and it[1].width < 1.6 and it[1].height > 20:
                xs.append(it[1].x0)
    return min(xs), max(xs)


def vertical_xs(page):
    xs = set()
    for d in page.get_drawings():
        for it in d['items']:
            if it[0] == 'l' and abs(it[1].x - it[2].x) < 0.6 and abs(it[1].y - it[2].y) > 20:
                xs.add(round(it[1].x))
            elif it[0] == 're' and it[1].width < 1.6 and it[1].height > 20:
                xs.add(round(it[1].x0))
    return sorted(xs)


def find_row(page, label, alt=None):
    """The ruled row whose label-column words read `label`, with its continuation rows.

    A part's scheme content can run over more than one ruled row: a model-solution
    table in one row and its marking notes in an unlabelled row below it (2018
    Higher Q9(a)), or the same label printed again over a second row holding the
    graph (2018 Higher Q7(c)). Rows that follow the labelled row and read either
    nothing or the same label belong to the part; the span stops at the first row
    labelled with anything else.
    """
    nth = None
    if isinstance(label, tuple):
        label, nth = label
    want = norm_label(label)
    wants = {want, norm_label(alt)} if alt else {want}
    xs = vertical_xs(page)
    label_right = xs[1] + 1
    words = [w for w in page.get_text('words') if w[2] <= label_right]
    rs = rules(page)
    rows = []
    for top, bottom in zip(rs, rs[1:]):
        if bottom - top < 15:
            continue
        got = norm_label(''.join(w[4] for w in sorted(words, key=lambda w: (round(w[1]), w[0])) if top <= w[1] < bottom))
        rows.append((top, bottom, got))
    hits = [i for i, r in enumerate(rows) if r[2] in wants]
    if not hits:
        raise SystemExit(f'label {label!r}: no ruled row reads that label on page {page.number + 1}')
    if nth is not None:
        # Only rows labelled exactly this, counted down the page.
        hits = [h for h in hits if rows[h][2] == want][nth - 1:]
    i = j = hits[0]
    while j + 1 < len(rows) and (rows[j + 1][2] == '' or rows[j + 1][2] in wants) and abs(rows[j + 1][0] - rows[j][1]) <= 2:
        j += 1
    if any(h > j for h in hits):
        raise SystemExit(f'label {label!r}: {len(hits)} separate ruled rows read that label on page {page.number + 1}')
    return rows[i][0], rows[j][1]


def continuation_rows(page):
    """The rows at the top of a page that carry on the previous page's part.

    2016 Higher Paper 1 Q1(c) prints its root-formula and sum-of-roots methods
    on one page and three more methods on the next, in a row whose label column
    is empty. The continuation runs from the page's first rule through every
    unlabelled row that follows without a gap, and stops at the first label.
    """
    xs = vertical_xs(page)
    label_right = xs[1] + 1
    words = [w for w in page.get_text('words') if w[2] <= label_right]
    rs = rules(page)
    rows = []
    for top, bottom in zip(rs, rs[1:]):
        if bottom - top < 15:
            continue
        got = norm_label(''.join(w[4] for w in sorted(words, key=lambda w: (round(w[1]), w[0])) if top <= w[1] < bottom))
        rows.append((top, bottom, got))
    if not rows or rows[0][2] != '':
        raise SystemExit(f'page {page.number + 1}: no unlabelled continuation row at the top')
    j = 0
    while j + 1 < len(rows) and rows[j + 1][2] == '' and abs(rows[j + 1][0] - rows[j][1]) <= 2:
        j += 1
    return rows[0][0], rows[j][1]


def main():
    year, lv = int(sys.argv[1]), sys.argv[2]
    write = '--write' in sys.argv
    ids = AFFECTED[(year, lv)]
    doc = pymupdf.open(os.path.join(ROOT, 'paper-trail-corpus', 'markingschemes', str(year), SCHEME[lv]))
    tasks = {}
    for key in ('p1', 'p2'):
        path = os.path.join(ROOT, 'scripts', 'markbank', 'mathematics', 'reviews', f'{year}-{LEVEL[lv]}-{key}.json')
        if os.path.exists(path):
            tasks.update({c['id']: c for c in json.load(open(path))['cards']})
    out_dir = os.path.join(ROOT, 'exam-papers', 'maths', 'figures', f'{year}-{lv}')
    if write:
        os.makedirs(out_dir, exist_ok=True)
    per_page = {}
    entries, binding = [], {}
    for cid in ids:
        task = tasks[cid]
        # A part runs over at most one page break, onto the very next page.
        assert len(task['schemePages']) == 1 or (len(task['schemePages']) == 2 and
                                                 task['schemePages'][1] == task['schemePages'][0] + 1), (cid, task['schemePages'])
        pno = task['schemePages'][0]
        page = doc[pno - 1]
        label = PRINTED_LABEL.get(cid) or part_label(task['printedParts'])
        if cid in ROW_SPAN:
            assert ROW_SPAN[cid][0] == pno, (cid, pno)
            top, bottom = ROW_SPAN[cid][1:]
        else:
            top, bottom = find_row(page, label, part_label_long(task['printedParts']))
        x0, x1 = table_x(page)
        clip = pymupdf.Rect(x0 - 2, top - 2, x1 + 2, bottom + 2)
        n = per_page.get(pno, 0); per_page[pno] = n + 1
        name = f'maths-{year}-{lv.upper()}-scheme-p{pno:03d}-i{n}'
        text = ' '.join(page.get_text('text', clip=clip).split())
        more = None
        if len(task['schemePages']) == 2:
            page2 = doc[task['schemePages'][1] - 1]
            top2, bottom2 = continuation_rows(page2)
            a2, b2 = table_x(page2)
            more = (page2, pymupdf.Rect(a2 - 2, top2 - 2, b2 + 2, bottom2 + 2))
            text += ' ' + ' '.join(page2.get_text('text', clip=more[1]).split())
        scale = re.search(r'Scale ?\d+[A-E] ?\([\d, ]+\)', text)
        bands = [b for b in BANDS if re.search(r'\b' + b + r'\b', text) and not (b == 'Partial Credit' and re.search(r'(Low|Mid|High) Partial Credit', text) and not re.search(r'(?<!Low )(?<!Mid )(?<!High )Partial Credit', text))]
        paper_no = cid.split('-')[3][1]
        desc = (f"The marking scheme's printed row for {year} {LEVEL_WORD[lv]} Paper {paper_no} {', '.join(task['printedParts'])}, "
                f"as the State Examinations Commission set it: the part label, the model solution, and the marking notes"
                + (f" for {scale.group(0)}" if scale else '')
                + (f", listing {', '.join(bands)}" if bands else '') + '.')
        entries.append({'file': name + '.png', 'kind': 'figure', 'truncated': False, 'description': desc, 'solution': True,
                        'questionRef': f"{year} {lv.upper()} Paper {paper_no} {', '.join(task['printedParts'])}"})
        binding[cid] = name
        print(f'{cid:32} p{pno} rows {top:.0f}-{bottom:.0f} {name}' + (f' + p{pno + 1} rows {more[1].y0 + 2:.0f}-{more[1].y1 - 2:.0f}' if more else ''))
        if write and more is None:
            page.get_pixmap(clip=clip, dpi=DPI).save(os.path.join(out_dir, name + '.png'))
        elif write:
            # The two pages' rows, one above the other, as the part reads.
            from PIL import Image
            import io
            parts = [Image.open(io.BytesIO(pg.get_pixmap(clip=c, dpi=DPI).tobytes('png'))).convert('RGB')
                     for pg, c in ((page, clip), more)]
            out = Image.new('RGB', (max(im.width for im in parts), sum(im.height for im in parts)), 'white')
            y = 0
            for im in parts:
                out.paste(im, (0, y)); y += im.height
            out.save(os.path.join(out_dir, name + '.png'))
    if write:
        cat = json.load(open(CATALOGUE)) if os.path.exists(CATALOGUE) else []
        keep = [e for e in cat if not e['file'].startswith(f'maths-{year}-{lv.upper()}-scheme-')]
        open(CATALOGUE, 'w').write(json.dumps(keep + entries, ensure_ascii=False, indent=1) + '\n')
        print(f'wrote {len(entries)} crops and catalogue entries')
    return binding


def publish(year, lv, paper=None):
    manifest_path = os.path.join(ROOT, 'components', 'MarkBank', 'figures.json')
    raw = open(manifest_path, encoding='utf-8').read()
    manifest = json.loads(raw)
    by_md5 = {v['md5']: k for k, v in manifest.items()}
    cat = [e for e in json.load(open(CATALOGUE)) if e['file'].startswith(f'maths-{year}-{lv.upper()}-scheme-')
           and (paper is None or f' Paper {paper[1]} ' in e['questionRef'])]
    dest = os.path.join(ROOT, 'public', 'exam-figures', 'maths', 'markbank')
    added = []
    for e in cat:
        assert e['kind'] == 'figure' and not e['truncated'] and len(e['description']) >= 40, e['file']
        src = os.path.join(ROOT, 'exam-papers', 'maths', 'figures', f'{year}-{lv}', e['file'])
        md5 = hashlib.md5(open(src, 'rb').read()).hexdigest()
        name = e['file'][:-4]
        if name in manifest:
            if manifest[name]['md5'] != md5:
                raise SystemExit(f'{name}: already published with different bytes')
            continue
        if md5 in by_md5:
            raise SystemExit(f'{name}: identical bytes to {by_md5[md5]}')
        shutil.copyfile(src, os.path.join(dest, e['file']))
        added.append((name, {
            'src': f'/exam-figures/maths/markbank/{e["file"]}', 'md5': md5, 'alt': e['description'], 'solution': True,
            'lettersVisible': [], 'labelMeanings': [], 'questionRef': e['questionRef'], 'year': year,
            'level': LEVEL[lv], 'attribution': f'SEC Leaving Certificate Mathematics {year} {LEVEL_WORD[lv].split()[0]} Level — © State Examinations Commission',
        }))
    if added:
        tail = raw.rstrip()
        assert tail.endswith('}\n}'), 'unexpected manifest ending'
        block = ''.join(',\n ' + json.dumps(k, ensure_ascii=False) + ': ' + json.dumps(v, ensure_ascii=False, indent=1).replace('\n', '\n ')
                        for k, v in added)
        out = tail[:-2] + block + '\n}\n'
        json.loads(out)
        open(manifest_path, 'w', encoding='utf-8').write(out)
    print(f'published {len(added)} crops into figures.json')


if __name__ == '__main__':
    if '--publish' in sys.argv:
        rest = sys.argv[sys.argv.index('--publish') + 1:]
        publish(int(sys.argv[1]), sys.argv[2], rest[0] if rest else None)
    else:
        main()
