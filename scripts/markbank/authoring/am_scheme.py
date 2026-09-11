#!/usr/bin/env python3
"""The Applied Mathematics marking scheme, read as priced solution steps.

    python3 scripts/markbank/authoring/am_scheme.py 2024 hl
    python3 scripts/markbank/authoring/am_scheme.py --audit
    python3 scripts/markbank/authoring/am_scheme.py --append      # the gate's copy

Why maths_scheme.py cannot read this
------------------------------------
maths_scheme.py segments a page on `Scale 15D (0, 4, 7, 10, 15)` lines printed
in a right-hand Marking Notes column. Applied Mathematics prints neither: it
returns ZERO units on every page of all ten schemes. This scheme is ONE column
-- the model solution at the left margin -- with the mark for each step alone
in the right margin:

    1(c)
    s_J = 10t + t^2                                              5
    s_K = 4(t-1) + 2(t-1)^2                                      5
    s_J = s_K + 21 + 4                                           5
    t = 5 +- sqrt(2) s                                           5

So the unit here is a STEP, and the tariff is printed against it. Nothing is
divided, inferred or apportioned: a leaf ask is worth the sum of the marks the
scheme prints inside it, and where the scheme also prints the part's own total
-- the 2021 and 2022 schemes do, in a second right-hand column -- that total is
checked against the sum rather than replacing it.

The notation is the same CambriaMath/Word-subset wreckage Mathematics has, so
mathtext.py does the reading: doubled italics collapsed, glyphs remapped from
glyphmap.json, exponents and indices recovered from span geometry, and stacked
fractions spliced back into one line.

The syllabus break
------------------
2021 and 2022 are the old syllabus ("Applied Mathematics - Higher Level"). The
scheme REPRINTS the paper's question above each solution, prices each step
"(5)" and closes each part with its own total "(25)". 2023-2025 are the M31/M32
specification: no reprint, bare marks, and a head that names the leaf outright
("1(b) (ii)", or "1bii" where the 2025 Ordinary font drops its brackets).

Both are read here, because both are the same document with the marks column in
a different place, and because a subject cannot be half-carded across a break a
student sits either side of.

What is DISCARDED, and why
--------------------------
  * The Mathematical Modelling Project rubric, which closes every 2023-2025
    scheme. It is a four-column band grid -- "Very basic 0 - 5 / Little or no
    evidence of innovation" -- for the 20% coursework, not the written paper,
    and read as marking points it ships "Very basic" as something a student is
    supposed to have written. Religious Education's band grid taught this bank
    that lesson; the cut is made at the SEC's own heading.
  * Anything printed inside a diagram. The force diagrams and networks are
    drawn, and their labels ("R_1", "W = mg", "73") extract as text rows that
    would otherwise be lifted as the step's own working. Rows are dropped where
    they sit inside drawn or raster ink, and a leaf whose whole answer is
    inside that ink is REFUSED as answered by a drawing -- never guessed at.
  * Every row after the leaf's last printed mark. The scheme's examiner asides
    ("Deduct 3 marks if the algorithm used is not correctly named.") and its
    diagrams sit there, and nothing there carries a tariff.
"""
import argparse
import collections
import glob
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import am_glyphs                                             # noqa: E402
import mathtext                                              # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
SCHEMES = os.path.join(ROOT, 'examiner-reports', 'applied-maths', 'schemes')

OLD_YEARS = (2021, 2022)

# Where the marks column starts. Read from the page rather than assumed -- the
# old schemes set it at x=414-431 and the new ones at x=520-533 -- but the
# READER's split only has to sit between the widest solution line and the
# narrowest mark, and it must never move right of the marks or a mark line is
# read as working.
MARK_CUT = {'old': 400.0, 'new': 470.0}

# A cell in the marks column, in every shape the schemes print:
#   (5)          old syllabus, one step
#   (25)         old syllabus, the part's own total, in a second column
#   5            new specification
#   5, 5         two things marked at five each on one row
#   10 [0/4/7]   a marking SCALE: ten marks, awarded 0, 4, 7 or 10
#   (5), (5)     two things marked at five each, in ONE cell
MARK_CELL = re.compile(
    r'^\(?\s*(\d{1,3})\s*\)?'
    r'(?:\s*,\s*\(?\s*\d{1,3}\s*\)?)*'
    r'(?:\s*\[[\d/\s,]+\])?\s*$')
MARK_NUM = re.compile(r'\d{1,3}')
SCALE_TAIL = re.compile(r'\[([\d/\s,]+)\]')

# The head of a leaf, as the new specification prints it: "1(b) (ii)". The
# 2025 Ordinary scheme's font drops the brackets and prints "1bii", and the
# 2025 Higher one sets two spaces where the others set one -- the letters a-h
# and the romans i,ii,iii,iv,v,vi cannot be confused, so both parse the same.
NEW_HEAD = re.compile(
    r'^(\d{1,2})\s*\(?([a-h])?\)?\s*\(?(i{1,3}|iv|vi{0,3}|ix|x)?\)?$')
# The head of a part, as the old syllabus prints it: "1." alone, or "1. (b)"
# with the letter welded on, or "1." with "(b)" printed as its own cell beside
# it.
# "1." alone, "1. (b)" with the letter welded on, and — where a part carries
# onto a new page — "1. (b) A ball E is thrown vertically upwards ..." with the
# question it reprints welded on as well. The tail is handed back so the walk
# can read it as the reprint it is.
OLD_HEAD = re.compile(r'^(\d{1,2})\.\s*(?:\(([a-h])\))?\s*(.*)$')
BARE_LETTER = re.compile(r'^\(([a-h])\)[\s.,:]*$')
BARE_ROMAN = re.compile(r'^\((i{1,3}|iv|vi{0,3}|ix|x)\)[\s.,:]*$')
MARKER_ONLY = re.compile(r'^\(?(?:[a-h]|i{1,3}|iv|vi{0,3}|ix|x)\)?[\s.,:]*$')
LEADING_MARKER = re.compile(r'^\(([a-h]|i{1,3}|iv|vi{0,3}|ix|x)\)\s+(?=\S)')
# A step's own mark, printed at the end of the line the step ends on.
WELDED_MARK = re.compile(r'^(.*\S)\s+(\d{1,3})\s*$')
# How far below a mark cell the words it is printed AGAINST may start.
# The page sorts by the top of each row, and a mark's digits are set in a font
# whose box opens a sixth of a point higher than the solution's lowercase —
# "5" at y=461.472 against "e.g. increase in initial speed" at y=461.628 — so
# the tariff sorts BEFORE the step it prices and the step was read as priced
# at nothing. A spliced fraction widens the same gap to about a point, because
# its row is placed at the top of its NUMERATOR: 2022 Higher Q9(b)(i) sets its
# "(5)" at y=419.515 against a line recorded at y=420.624. Nothing in this
# corpus sets two printed lines closer than 14 points, so 2.5 cannot reach the
# line below.
SAME_ROW = 2.5

FURNITURE = re.compile(
    r'^(?:Leaving\s+Certificate.*|Applied\s+Mathematics.*|Marking\s+Scheme'
    r'|Coimisi.*|State\s+Examinations.*|Page\s+\d+)\s*$', re.I)
# The running footer's page number is a bare number, and so is the head of a
# question the scheme numbers without a part ("4" over "(i)"). Neither shape
# tells them apart -- dropping every bare number as furniture lost Questions 4
# to 10 of the 2024 Higher scheme outright -- so the footer is identified by
# where it is printed instead.
FOOTER_BAND = 55.0

# Where the written paper's scheme stops and the coursework rubric begins.
PROJECT = re.compile(r'Mathematical\s+Modelling\s+Project', re.I)

ROMANS = ['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x']

# This subject's own broken-glyph table, derived by derive_glyphs.py from its
# own PDFs (`--subject applied-maths`). Applied HERE rather than folded into
# glyphmap.json, for the reason derive_glyphs gives about Technology: a
# subject's map is additive and must not be able to move another subject's,
# and mathtext.demangle()'s table is shared with Mathematics.
with open(os.path.join(HERE, 'glyphmap-applied-maths.json'), encoding='utf-8') as _fh:
    AM_GLYPHS = {ord(k): v for k, v in json.load(_fh).items()}

# The survivors of that derivation: glyphs whose id is never once printed with
# a sane ToUnicode anywhere in this corpus, so nothing can be learned from it.
# Each was settled the way the bank's own memory says to settle one — the glyph
# was CROPPED out of the page at 600dpi and looked at — and the evidence is the
# line it was cropped from, recorded here so the call can be re-checked.
AM_GLYPHS.update({ord(k): v for k, v in {
    '\u0c08': '\u03b1',   # 2021 HL paper p.3: "u² sin 2α" over g
    '\u0bda': '\U0001d454',  # 2021 HL paper p.4: the g of "3mg/l"
    '\u0c20': '\u03c9',   # 2025 HL scheme p.6: the omega under "2π/ω"
    '\u0d47': '\u00b1',   # 2025 HL scheme p.10: "p = ±1/√2"
    '\u0d6d': '(', '\u0d71': ')',   # 2024 HL paper p.3: a matrix's tall brackets
    '\u0d6e': '(', '\u0d72': ')',   # 2024 OL paper p.17: the same pair, one size up
    '\u0cb2': 'A', '\u0cb3': 'B',   # 2025 HL scheme p.9: the subscripts of v_B - v_A
    '\u0cc1': 'P', '\u0cc2': 'Q',   # 2025 OL scheme p.10: the subscripts of v_P - v_Q
    '\u0d24': '\U0001d466\u0305',   # 2022 OL scheme p.13: y-bar, the mean of y
}.items()})


def repair(text):
    return text.translate(AM_GLYPHS) if text else text


def _squash(t):
    # Demangled first. The paper sets its unit vectors in the Mathematical
    # Alphanumeric block and the scheme's font subset does not, so "26𝚤 + 40𝚥"
    # and "26i + 40j" squashed to different strings and the scheme's reprint of
    # the question could not be recognised as one.
    return re.sub(r'[^a-z0-9]+', '', mathtext.demangle(t or '').lower())


def _lines(page, fix):
    """The page's lines with every glyph the CMap misnamed put right.

    Read from rawdict, which carries each glyph's own origin, so am_glyphs's
    table can be applied character by character; the span's text is then rebuilt
    from the corrected characters and handed to mathtext.line_text() unchanged,
    which is what keeps the exponent and subscript reading identical to
    Mathematics'.
    """
    for bi, b in enumerate(page.get_text('rawdict')['blocks']):
        for li, ln in enumerate(b.get('lines', [])):
            spans = []
            for si, sp in enumerate(ln.get('spans', [])):
                out = []
                for ci, c in enumerate(sp['chars']):
                    ch = fix.get((bi, li, si, ci), c['c'])
                    if ch is not None:
                        out.append(ch)
                spans.append(dict(sp, text=''.join(out)))
            if spans:
                yield dict(ln, spans=spans)


# The pieces a stacked expression's brackets are DRAWN from, each printed with
# a line to itself: the tall brace the 2023 Higher scheme sets beside the three
# lines of Q5(b), and the corner and stem glyphs of a matrix's parentheses.
BRACKET_PARTS = ('()[]{}|⎛⎜⎝⎞⎟⎠⎡⎢'
                 '⎣⎤⎥⎦⎧⎨⎩⎪⎫'
                 '⎬⎭⎮⎰⎱')


def _bracket_only(text):
    """Is this row nothing but a stacked expression's bracket?

    It states nothing, so it is not a marking point; and read as one it leaves
    the step's brackets unbalanced, which is the same shape a torn expression
    has — 2023 Higher Q5(b) was refused for a lone "}" printed beside its
    working.
    """
    t = text.strip()
    return bool(t) and all(c in BRACKET_PARTS or c.isspace() for c in t)


# Two runs printed level with each other SHARE most of their height: the whole
# of the shorter box in the usual case, 61% of it where a lower limit hangs
# below its operator. Two consecutive lines of prose share a little, because
# the box of a line carrying a subscript reaches into the line beneath it —
# the reprint of 2022 Ordinary Q1 is set on 13.4-point leading and its boxes
# overlap by 1.5 points, 12% of the shorter. The cut is made between 13% and
# 57%, which is the widest gap in that evidence.
SHARED_HEIGHT = 0.45
# And two runs printed level with each other barely overlap in x: 11% of the
# longer at most across this corpus, because they are set BESIDE each other
# and touch only where an index sits on its host's last glyph. Two lines of
# one paragraph overlap by 98%, which is the same statement read the other way.
SHARED_WIDTH = 0.4


def _one_printed_line(a, b, cut):
    """Are these two text runs two parts of ONE printed line?

    Measured, both ways, and both tests are needed. The vertical one says they
    were printed level; the horizontal one says they were printed BESIDE each
    other rather than under each other, which is what tells a stacked limit
    from the next line of the paragraph and keeps the two alternative solutions
    these schemes set side by side ("Kruskal's algorithm" left, "Prim's
    algorithm" right) from being welded into one.
    """
    if (a['x0'] >= cut) != (b['x0'] >= cut):
        return False
    share = min(a['y1'], b['y1']) - max(a['y0'], b['y0'])
    if share < SHARED_HEIGHT * min(a['y1'] - a['y0'], b['y1'] - b['y0']):
        return False
    lap = min(a['x1'], b['x1']) - max(a['x0'], b['x0'])
    return -2.0 <= lap <= SHARED_WIDTH * max(a['x1'] - a['x0'], b['x1'] - b['x0'])


def _restack(lines, cut):
    """[[line]] — the page's runs grouped into the lines the page prints.

    A stacked expression is several text runs on several baselines: the limits
    of an integral, the limits on a definite integral's square bracket, an
    index Word sets on a baseline of its own. PyMuPDF reports each as a line,
    and sorted by y they interleave with each other and with the marks column.
    The 2022 Higher scheme prints

        [ln N]_N^x = −k[t]_0^t

    as three runs, and the reader read three rows — "t", "x = −k[t]_0" and
    "[ln N]_N" — three marking points, in the wrong order, one of them a single
    letter that took a five-mark tariff of its own and was reported as a step
    that "did not survive the scheme's font".

    A mark cell, a part marker and a head are never joined to anything: the
    walk reads each of those by its own shape and its own position on the page,
    and a head welded into the working beside it stops opening its leaf.
    """
    def structural(i, ln):
        t = ln['text']
        if MARKER_ONLY.match(t) or OLD_HEAD.match(t) or FURNITURE.match(t):
            return True
        # A mark cell only where the walk would read one: in the marks band.
        # An integral's lower limit is a bare "0" printed in the middle of the
        # working, and refusing to join THAT left the limit standing as a row.
        if MARK_CELL.match(t) and ln['x1'] >= cut - 45:
            return True
        m = NEW_HEAD.match(t)
        if m and (m.group(2) or m.group(3)):
            return True
        # A bare number is a head only when the part it belongs to is printed
        # beside it — _page_heads() reads the pair together — and a head welded
        # into the working beside it stops opening its leaf.
        return bool(m and any(
            (BARE_ROMAN.match(o['text']) or BARE_LETTER.match(o['text']))
            and abs(o['y0'] - ln['y0']) <= 4 and ln['x0'] < o['x0'] <= ln['x0'] + 70
            for j, o in enumerate(lines) if j != i))

    joinable = [i for i, ln in enumerate(lines) if not structural(i, ln)]
    parent = {i: i for i in joinable}

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    for n, i in enumerate(joinable):
        for j in joinable[n + 1:]:
            if _one_printed_line(lines[i], lines[j], cut):
                parent[find(i)] = find(j)
    buckets = collections.OrderedDict()
    for i, ln in enumerate(lines):
        buckets.setdefault(find(i) if i in parent else ('alone', i), []).append(ln)
    return list(buckets.values())


def rows(page, cut, fix=None):
    """[(y, x0, x1, text)] — one scheme page, read the way a card must read it.

    Fractions are spliced back into a line first (mathtext does the geometry),
    then every line the splice did not consume is read span-aware so exponents
    and indices survive. `cut` separates the marks column from the solution, so
    a mark printed level with a fraction is not swallowed by it. What the
    splice leaves behind is regrouped by _restack() into the lines the page
    prints, because a stacked expression's other halves are lines of their own
    to every reader but the eye.
    """
    fix = {} if fix is None else fix
    # radicals=True: this scheme's sqrt signs are drawn touching their own
    # overbar, and without the wider test that bar is spliced as a fraction —
    # 2024 Higher Q1(c)'s "t = 5 ± √2 s" and the priced step above it came back
    # as one unreadable row, and 2023 Ordinary Q3(iii)'s two moduli as another.
    spans = mathtext.fractions(page, cut, fix, radicals=True)
    # A spliced fraction knows where it STARTS but not where it ends, and the
    # marks column is placed by the right edge — so the band's own right edge
    # is measured from the lines it consumed. Without it a step whose mark is
    # printed on the same line as its last words ("... ds as required  5") had
    # no right edge at all and its tariff was read as part of the working.
    reach = {}
    for ln in _lines(page, fix):
        lx0 = min(sp['bbox'][0] for sp in ln['spans'])
        y = min(sp['bbox'][1] for sp in ln['spans'])
        centre = (y + max(sp['bbox'][3] for sp in ln['spans'])) / 2
        x1 = max(sp['bbox'][2] for sp in ln['spans'])
        for i, (fx, top, bottom, _t) in enumerate(spans):
            # Only the lines the splice CONSUMED, which are the ones on its own
            # side of the cut. A mark printed level with a fraction is on the
            # other side, and counting it made every such fraction look as if
            # it reached the marks column — so its last number was stripped off
            # as a tariff it had already been given separately.
            if top <= centre <= bottom and (lx0 >= cut) == (fx >= cut):
                reach[i] = max(reach.get(i, 0.0), x1)
    out = [(top, x0, max(reach.get(i, x0), x0), repair(text))
           for i, (x0, top, bottom, text) in enumerate(spans)]
    left = []
    for ln in _lines(page, fix):
        t = mathtext.line_text(ln)
        if not t:
            continue
        x0 = min(s['bbox'][0] for s in ln['spans'])
        x1 = max(s['bbox'][2] for s in ln['spans'])
        y = min(s['bbox'][1] for s in ln['spans'])
        y1 = max(s['bbox'][3] for s in ln['spans'])
        centre = (y + y1) / 2
        if any(top <= centre <= bottom and (fx >= cut) == (x0 >= cut)
               for fx, top, bottom, _ in spans):
            continue
        left.append({'line': ln, 'x0': x0, 'x1': x1, 'y0': y, 'y1': y1,
                     'text': repair(t).replace('\xa0', ' ').strip()})
    for group in _restack(left, cut):
        if len(group) == 1:
            ln = group[0]
            if _bracket_only(ln['text']):
                continue
            out.append((ln['y0'], ln['x0'], ln['x1'], ln['text']))
            continue
        # One printed line, read in the order the page prints it: every run's
        # spans in x order, then line_text() as for any other line — which is
        # what marks the limits it now sees as raised or lowered.
        merged = sorted((s for ln in group for s in ln['line']['spans']),
                        key=lambda s: (s['bbox'][0], s['bbox'][1]))
        text = repair(mathtext.line_text({'spans': merged}))
        text = text.replace('\xa0', ' ').strip()
        if not text or _bracket_only(text):
            continue
        out.append((min(ln['y0'] for ln in group),
                    min(ln['x0'] for ln in group),
                    max(ln['x1'] for ln in group), text))
    return sorted(out, key=lambda r: (r[0], r[1]))


def ink(page):
    """The rectangles a diagram occupies: drawn strokes and placed images.

    A fraction BAR is a drawn stroke too, so the same test mathtext makes for
    one is made here in reverse — anything that thin and that short is
    notation, not a picture. Without the exclusion every stacked fraction on
    the page would blank out the line it belongs to.
    """
    boxes = []
    for d in page.get_drawings():
        r = d['rect']
        if r.height <= mathtext.BAR_MAX_HEIGHT and r.width <= mathtext.BAR_MAX_WIDTH:
            continue
        if r.width < 6 or r.height < 6:
            continue
        boxes.append((r.x0, r.y0, r.x1, r.y1))
    for info in page.get_image_info():
        r = info['bbox']
        boxes.append((r[0], r[1], r[2], r[3]))
    return _merge(boxes)


def _merge(boxes):
    """Overlapping or touching rectangles joined, so a diagram drawn as forty
    strokes is one region rather than forty."""
    boxes = [list(b) for b in boxes]
    changed = True
    while changed:
        changed = False
        for i in range(len(boxes)):
            for j in range(i + 1, len(boxes)):
                a, b = boxes[i], boxes[j]
                if a[0] <= b[2] + 6 and b[0] <= a[2] + 6 \
                        and a[1] <= b[3] + 6 and b[1] <= a[3] + 6:
                    boxes[i] = [min(a[0], b[0]), min(a[1], b[1]),
                                max(a[2], b[2]), max(a[3], b[3])]
                    boxes.pop(j)
                    changed = True
                    break
            if changed:
                break
    return boxes


class Unit:
    """One leaf ask of one scheme."""

    __slots__ = ('key', 'groups', 'part_total', 'cue', 'page', 'y0', 'y1',
                 'scales', 'drawn', 'asides', 'drawn_rows')

    def __init__(self, key, page):
        self.key = key
        self.groups = []          # [(text, marks)]
        self.part_total = None
        self.cue = ''
        self.page = page
        self.y0 = self.y1 = None
        self.scales = []          # the "[0/4/7]" ladders, where printed
        self.drawn = False        # every priced row was inside a diagram
        self.asides = []
        # The rows this leaf's band prints INSIDE drawn or raster ink, with
        # the page and coordinate each was read at. Kept so an ask refused as
        # answered-by-a-drawing can show what the scheme actually printed
        # rather than only assert that it printed nothing liftable.
        self.drawn_rows = []

    @property
    def total(self):
        return sum(m for _, m in self.groups)

    def __repr__(self):
        return f'<Unit {self.key} {self.total}m {len(self.groups)} steps>'


class AmScheme:
    def __init__(self, year, level, paper_text=None):
        import pymupdf
        self.year, self.level = year, level
        self.old = year in OLD_YEARS
        self.cut = MARK_CUT['old' if self.old else 'new']
        self.path = os.path.join(SCHEMES, f'{year}-{level}.pdf')
        self.doc = pymupdf.open(self.path)
        # The font's own letters, recovered from the glyph ids. Derived once
        # per document; see am_glyphs.py for the fault it repairs.
        self.glyphs, self.glyph_stats = am_glyphs.derive(self.doc)
        self._fix = {}
        # {q: squashed paper text}, used ONLY to tell the old scheme's reprint
        # of the question from the solution below it. Never read for an answer.
        self.paper_text = paper_text or {}
        self.units = collections.OrderedDict()
        self.refused = []
        self._read()

    # ------------------------------------------------------------------ read
    def rows(self, page):
        if page.number not in self._fix:
            self._fix[page.number] = am_glyphs.page_fix(page, self.glyphs)
        return rows(page, self.cut, self._fix[page.number])

    def _mark_columns(self):
        """(step column x0, part-total column x0) for this scheme.

        Measured, not assumed: the old schemes set the step marks at x=414 in
        2021 Ordinary and x=431 in 2021 Higher, and each puts the part's own
        total in a second column 70 points further right.
        """
        seen = collections.Counter()
        for page in self.doc:
            for y, x0, x1, t in self.rows(page):
                if x1 >= self.cut and MARK_CELL.match(t):
                    seen[round(x1)] += 1
        if not seen:
            return None, None
        # Cluster the right edges: a cell's own width moves it a point or two,
        # and the old schemes' step column moves with the table it is in, but a
        # COLUMN is a run of edges within a few points of each other.
        clusters, run = [], []
        for x in sorted(seen):
            if run and x - run[-1] > 6:
                clusters.append(run)
                run = []
            run.append(x)
        if run:
            clusters.append(run)
        # A cluster is named by its BUSIEST edge, not its widest: 2025
        # Ordinary prints one stray line whose right edge is six points past
        # the marks column, and naming the cluster after that put the column
        # at 547 where 75 cells are printed at 541 — and not one mark on the
        # paper was read.
        weight = {max(c, key=lambda x: (seen[x], x)): sum(seen[x] for x in c)
                  for c in clusters}
        step = max(weight, key=lambda k: (weight[k], -k))
        # The part total is the RIGHTMOST column, not the next one along: the
        # old schemes print a second, narrower step column between the two, and
        # taking the leftmost of what lies right of the steps read every
        # part total "(25)" as another step and doubled the paper.
        right = [k for k in weight
                 if k > step + 40 and 5 <= weight[k] < weight[step]]
        return step, (max(right) if right else None)

    def _is_step(self, x0, x1):
        """Is a mark cell at this position a STEP's mark?

        The old syllabus sets its table's step column wherever the table's own
        widths put it — 2022 Higher prints Q1(a)'s marks at x=452 and Q1(b)'s,
        on the very next page, at x=416 — so a scheme-wide column loses one of
        the two. What IS stable is the part-total column at the right margin,
        so the step marks are read as "in the marks band and not the total".
        The new specification right-aligns every cell on one column and its
        pages carry bare numbers that are network weights, so there the column
        is held to.
        """
        if self.old:
            return x0 >= self.cut
        # The new specification right-aligns every cell on ONE edge, and its
        # pages carry tables whose values reach almost that far: the 2023
        # Higher critical-path table sets a "34" whose right edge is seven
        # points short of the column, and a loose tolerance read it as a
        # 34-mark step.
        return abs(x1 - self.step_x1) <= 3.5

    def _margins(self):
        """(head indent, part-letter indent) for this scheme.

        Measured from the pages. Every scheme sets its heads at one x — 56.7
        in the new specification, 53.9 or 70.6 in the old — and the old
        syllabus sets a part letter one tab in from it. A bare number anywhere
        else on the page is a matrix entry, a table value or a network weight,
        and taking those for heads walked the 2024 Higher scheme up to a
        Question 13 that does not exist.
        """
        heads, letters = collections.Counter(), collections.Counter()
        for page in self.doc:
            floor = page.rect.height - FOOTER_BAND
            for y, x0, x1, t in self.rows(page):
                if y >= floor:
                    continue
                if self.old:
                    if OLD_HEAD.match(t):
                        heads[round(x0)] += 1
                    elif BARE_LETTER.match(t):
                        letters[round(x0)] += 1
                else:
                    m = NEW_HEAD.match(t)
                    if m and (m.group(2) or m.group(3)):
                        heads[round(x0)] += 1
        head_x = heads.most_common(1)[0][0] if heads else 0
        letter_x = None
        if letters:
            near = [x for x in letters if head_x < x <= head_x + 60]
            if near:
                letter_x = max(near, key=lambda x: letters[x])
        return head_x, letter_x

    def _page_heads(self, page_rows, head_x, letter_x):
        """{row index: (q, letter, roman) or ('letter', tok)} for one page.

        A question the scheme numbers without a part prints its roman BESIDE
        the number — "4" at the margin and "(i)" one tab in, on the same row —
        so a bare number is only read as a head when that companion is there.
        """
        out = {}
        for i, (y, x0, x1, t) in enumerate(page_rows):
            if abs(x0 - head_x) > 3:
                if letter_x is not None and abs(x0 - letter_x) <= 3 \
                        and BARE_LETTER.match(t):
                    out[i] = ('letter', BARE_LETTER.match(t).group(1), None, '')
                continue
            companion = None
            for j, (y2, x2, _x3, t2) in enumerate(page_rows):
                if j == i or abs(y2 - y) > 4 or not (x0 < x2 <= x0 + 70):
                    continue
                m2 = BARE_ROMAN.match(t2) or BARE_LETTER.match(t2)
                if m2:
                    companion = m2.group(1)
                    break
            if self.old:
                m = OLD_HEAD.match(t)
                if not m:
                    continue
                tail = (m.group(3) or '').strip()
                if tail and not m.group(2):
                    continue          # "1. and then" — prose, not a head
                token = m.group(2) or (companion if companion
                                       and re.fullmatch(r'[a-h]', companion) else None)
                out[i] = (int(m.group(1)), token, None, tail)
                continue
            m = NEW_HEAD.match(t)
            if not m:
                continue
            letter, roman = m.group(2), m.group(3)
            if companion and not roman:
                if re.fullmatch(r'[a-h]', companion) and not letter:
                    letter = companion
                elif not re.fullmatch(r'[a-h]', companion):
                    roman = companion
            if not letter and not roman:
                continue          # a bare number with no part beside it
            out[i] = (int(m.group(1)), letter, roman, '')
        return out

    def _read(self):
        self.step_x1 = self.total_x1 = None
        step_x1, total_x1 = self._mark_columns()
        self.step_x1, self.total_x1 = step_x1, total_x1
        head_x, letter_x = self._margins()
        self.head_x, self.letter_x = head_x, letter_x
        q = letter = roman = None
        cur = None
        pending = []              # text rows waiting for their mark
        markers = []              # marker rows held until their text arrives
        in_cue = False
        started = False
        for i, page in enumerate(self.doc):
            page_rows = self.rows(page)
            if any(PROJECT.search(t) for _, _, _, t in page_rows):
                break             # the coursework rubric — never a card
            boxes = ink(page)
            floor = page.rect.height - FOOTER_BAND
            heads = self._page_heads(page_rows, head_x, letter_x)
            # The old syllabus closes a part by printing its total BESIDE the
            # last step's mark — "(5)      (25)" on one row — and it sets that
            # column wherever the page's table puts it, so a scheme-wide
            # column missed it on four pages and read "(25)" as a 25-mark
            # step. Two mark cells on one row is the shape, wherever they are.
            # The old syllabus closes a part by printing its total BESIDE the
            # last step's mark — "(5)      (25)" on one row — and it sets that
            # column wherever the page's table puts it. Two mark cells on one
            # row is the shape, wherever they are: the RIGHT one is the total
            # and the LEFT one is a step, even where the table has pulled the
            # step column left of the reader's boundary (2022 Higher sets
            # Q8(b)(ii)'s "(5)" at x=380 and its "(30)" at x=416, and reading
            # the pair as one 30-mark step made Question 8 worth 75).
            cells = [(y, x0, x1) for y, x0, x1, t in page_rows
                     if MARK_CELL.match(t) and x1 >= self.cut - 45] \
                if self.old else []
            totals, paired = set(), set()
            for y_, x0_, _x1 in cells:
                left = [o for o in cells if abs(o[0] - y_) <= 2 and o[1] < x0_ - 10]
                if left:
                    totals.add((round(y_, 1), round(x0_, 1)))
                    for o in left:
                        paired.add((round(o[0], 1), round(o[1], 1)))
            if not started:
                # The front matter numbers its own paragraphs at the very
                # indent a head is printed at, and the Irish bonus-marks table
                # ("Bunmharc / Marc Bónais") fills the marks column with the
                # bonus for each band. Read as a question and its steps, that
                # table PRICED a Question 4 before the paper began, and the
                # real Question 1 three pages later was then rejected for
                # going backwards — 2022 Higher lost Q1, Q2 and Q3 whole and
                # Q4 came out worth 185 marks.
                # The scheme proper is where PARTS appear: a head that names
                # one, or a marker printed on its own line. No preamble page
                # in the corpus has either.
                if not (any(h[1] or h[2] for h in heads.values())
                        or any(MARKER_ONLY.match(t) and
                               (BARE_LETTER.match(t) or BARE_ROMAN.match(t))
                               for _, _, _, t in page_rows)):
                    continue
                started = True

            def drawn(y, x0):
                return any(bx0 - 4 <= x0 <= bx1 + 4 and by0 - 4 <= y <= by1 + 4
                           for bx0, by0, bx1, by1 in boxes)

            taken = set()         # rows a mark above them has already claimed
            for n, (y, x0, x1, text) in enumerate(page_rows):
                if not text or y >= floor or n in taken:
                    continue
                # ---- the marks column. Placed by its RIGHT edge, because the
                # schemes right-align it: "10 [0/4/7]" opens 45 points left of
                # the "5" printed under it, and an x0 test loses every scale on
                # the paper. Tested BEFORE the page furniture, because most
                # cells here are a bare "5".
                cell = (round(y, 1), round(x0, 1))
                on_column = self._is_step(x0, x1) or cell in paired
                if MARK_CELL.match(text) and x1 >= self.cut - 45 \
                        and (on_column or cell in totals):
                    if cur is None:
                        continue
                    if cell in totals:
                        cur.part_total = int(MARK_NUM.search(text).group(0))
                        continue
                    # A marker still in hand belongs to THIS step. 2021 Higher
                    # Q3(b)(i) is answered by a drawing, so its "(i)" is
                    # followed by no prose at all before its "(5)" — and a
                    # marker only flushed by prose was thrown away here, which
                    # filed every step of (i) under the part above it.
                    if markers:
                        cur, q, letter, roman = self._flush(
                            markers, cur, q, letter, roman, i)
                        markers = []
                    body = ' '.join(t for t in pending).strip()
                    if not body:
                        # Nothing is pending because the words this mark is
                        # printed against sort AFTER it: they are on the SAME
                        # printed line, and the page is walked by the top of
                        # each row. See SAME_ROW. Sixteen steps of this corpus
                        # are set that way — "e.g. increase in initial speed or
                        # change initial angle   5" — and every one of them was
                        # read as a step the scheme priced and left blank.
                        body, cur, q, letter, roman = self._same_row(
                            page_rows, n, y, drawn, taken, cur, q, letter,
                            roman, i, in_cue)
                        if body:
                            in_cue = False
                    value = sum(int(v) for v in MARK_NUM.findall(
                        SCALE_TAIL.sub('', text)))
                    # The SEC prices every step of this paper in FIVES: of the
                    # 826 marks printed across the ten schemes, 825 are a
                    # multiple of five and the one that is not is a "13" in a
                    # centre-of-gravity table that happened to line up with the
                    # column. A value that is not a multiple of five is that
                    # kind of number, not a tariff.
                    if not value or value % 5:
                        continue
                    scale = SCALE_TAIL.search(text)
                    if scale:
                        cur.scales.append(scale.group(1).strip())
                    # A step whose rows were all inside the diagram, or which
                    # printed no rows at all, is a step the scheme answered by
                    # DRAWING. It keeps its printed mark — the tariff is on the
                    # page — and _finish() refuses the whole leaf if every one
                    # of its steps is like that.
                    cur.groups.append((body, value))
                    cur.y1 = y
                    pending, markers = [], []
                    continue
                # ---- heads
                if n in heads:
                    head = heads[n]
                    # The front matter numbers its own paragraphs "1." to "9."
                    # in exactly the head's shape, and the 2022 schemes head
                    # their annotation-symbols table "3." — so the walker
                    # reached Question 3 before the paper began and then
                    # rejected the real Question 1 for going backwards, losing
                    # a third of the scheme. A head arriving while not one unit
                    # has been priced proves everything read so far was
                    # furniture: start again from it. (paper.py makes the same
                    # argument about instruction pages.)
                    if head[0] != 'letter' and q is not None and head[0] <= q \
                            and not any(u.groups for u in self.units.values()):
                        self.units.clear()
                        q = letter = roman = None
                        cur = None
                    if head[0] == 'letter':
                        if q is None:
                            continue
                        cur = self._open(q, head[1], None, q, letter, roman, i, y)
                    else:
                        cur = self._open(head[0], head[1], head[2],
                                         q, letter, roman, i, y)
                    if cur is not None:
                        q, letter, roman = cur.key
                        pending, markers = [], []
                        in_cue = self.old
                        if head[3] and in_cue and self._is_cue(q, head[3]):
                            cur.cue = head[3]
                    continue
                if FURNITURE.match(text):
                    continue
                if x0 >= self.cut:
                    continue          # a stray number or a diagram label
                # A step whose last words reach the marks column carries its
                # mark on the same printed line: 2024 Higher Q10(a)(iii) sets
                # "one where a delay ... overall project     5" as one row, and
                # 2025 Higher Q2(iii) ends "... as required  5". Read whole,
                # the step was priced at nothing and the leaf was refused.
                welded = WELDED_MARK.match(text) if on_column else None
                if welded and cur is not None:
                    text = welded.group(1).strip()
                    weld_mark = int(welded.group(2))
                else:
                    weld_mark = None
                if cur is None:
                    continue
                # ---- a marker inside the solution opens the next leaf
                m = BARE_ROMAN.match(text) or BARE_LETTER.match(text)
                if m and MARKER_ONLY.match(text):
                    markers.append((m.group(1), y))
                    continue
                # A marker WELDED to the first line of its own working. The
                # fraction splice joins the two — 2021 Higher Q1(a) reads
                # "(i) s = ut + 1/2 at²" as one row — and read as prose the
                # leaf it opens is never opened at all: every step of (i) was
                # filed under (ii) and (i) shipped nothing.
                lead = LEADING_MARKER.match(text)
                if lead:
                    markers.append((lead.group(1), y))
                    text = text[lead.end():].strip()
                    if not text:
                        continue
                # ---- text
                if in_cue:
                    if self._is_cue(q, text):
                        cur.cue = f'{cur.cue} {text}'.strip()
                        markers = []
                        continue
                    # A row too short to be evidence either way — the scheme's
                    # own "Find", "Calculate", "C", "D" — neither extends the
                    # reprint nor ends it. Ending on one closed the reprint at
                    # "Find" and turned the question's own (i) and (ii) into
                    # solution markers, which handed every step of (a)(i) to
                    # (a)(ii).
                    if len(_squash(text)) < 6 and '=' not in text:
                        continue
                    in_cue = False
                if markers:
                    cur, q, letter, roman = self._flush(
                        markers, cur, q, letter, roman, i)
                    markers = []
                if cur is None:
                    continue
                if drawn(y, x0):
                    if len(cur.drawn_rows) < 40:
                        cur.drawn_rows.append((i, round(y, 1), round(x0, 1),
                                               text))
                    continue
                if cur.y0 is None:
                    cur.y0 = y
                pending.append(text)
                if weld_mark is not None:
                    cur.groups.append((' '.join(pending).strip(), weld_mark))
                    cur.y1 = y
                    pending = []
        self._finish()

    def solution_lines(self):
        """Every line of the model-solution column, in printing order.

        The same rows the walk above keeps: not the marks, not the footer, not
        the text inside a diagram. Used to give the provenance gate a copy of
        the scheme it can actually read.
        """
        out = []
        for page in self.doc:
            page_rows = self.rows(page)
            if any(PROJECT.search(t) for _, _, _, t in page_rows):
                break
            boxes = ink(page)
            floor = page.rect.height - FOOTER_BAND
            for y, x0, x1, text in page_rows:
                if not text or y >= floor or x0 >= self.cut:
                    continue
                if MARK_CELL.match(text) and x1 >= self.cut:
                    continue
                if FURNITURE.match(text):
                    continue
                if any(bx0 - 4 <= x0 <= bx1 + 4 and by0 - 4 <= y <= by1 + 4
                       for bx0, by0, bx1, by1 in boxes):
                    continue
                out.append(text)
        return out

    def _same_row(self, page_rows, n, y, drawn, taken, cur, q, letter, roman,
                  page, in_cue):
        """The solution words printed on the same line as the mark at row n.

        Only ever called when nothing is pending, so it cannot take words away
        from a step that already has them: the most it can do is give a step
        the scheme plainly priced the words the scheme plainly printed beside
        it. Rows it takes are recorded in `taken` so the walk does not read
        them again as the next step's working.

        A marker on that line opens its leaf first, exactly as one on its own
        line does: 2022 Ordinary Q5 sets "(i)   PCM   2(6) + 3(2) = 2v₁ + 3v₂
        (5)" on one line, and the (5) sorting first filed that step under the
        question instead of under (i).
        """
        found, markers, rows = [], [], []
        for j in range(n + 1, len(page_rows)):
            y2, x2, _x3, t2 = page_rows[j]
            if y2 - y > SAME_ROW:
                break
            if not t2 or x2 >= self.cut or drawn(y2, x2) or FURNITURE.match(t2):
                continue
            m = BARE_ROMAN.match(t2) or BARE_LETTER.match(t2)
            if m and MARKER_ONLY.match(t2):
                markers.append((m.group(1), y2))
                found.append(j)
                continue
            lead = LEADING_MARKER.match(t2)
            if lead:
                markers.append((lead.group(1), y2))
                t2 = t2[lead.end():].strip()
                if not t2:
                    found.append(j)
                    continue
            # The old syllabus reprints the question above its solution, and a
            # reprinted line is never a marking point. Told apart against the
            # PAPER, the way the walk itself tells them apart.
            if in_cue and self._is_cue(q, t2):
                continue
            rows.append((x2, t2))
            found.append(j)
        if not rows:
            return '', cur, q, letter, roman
        if markers:
            cur, q, letter, roman = self._flush(markers, cur, q, letter,
                                                roman, page)
        taken.update(found)
        # Read ACROSS the line, not down the page. The page is sorted by the
        # top of each row, and on one line that is not reading order: the
        # scheme labels its method in a column of its own — "PCM   7(1) +
        # 3(−5) = 7v₁ + 3v₂" — and the label's row opens a fraction of a point
        # below the equation's, so joining by y printed the label last.
        return ' '.join(t for _x, t in sorted(rows)).strip(), \
            cur, q, letter, roman

    def _flush(self, markers, cur, q, letter, roman, page):
        """Open the leaves the markers held since the last step."""
        for tok, my in markers:
            if re.fullmatch(r'[a-h]', tok):
                nxt = self._open(q, tok, None, q, letter, roman, page, my)
            else:
                nxt = self._open(q, letter, tok, q, letter, roman, page, my)
            if nxt is not None:
                cur = nxt
                q, letter, roman = cur.key
        return cur, q, letter, roman

    def _open(self, q, letter, roman, prev_q, prev_l, prev_r, page, y):
        if q is None:
            return None
        # Questions and their parts run FORWARD. A key that goes backwards is
        # something else that looks like one — a table value, a network weight
        # — and the run is the only thing that says so.
        if prev_q is not None:
            if q < prev_q or q > prev_q + 1:
                return None
            if q == prev_q:
                # The old syllabus reprints a WHOLE question — (a) and then
                # (b) — before it answers any of it, so the letters run a, b,
                # a, b down one page. A forward-only letter guard rejected the
                # second (a) and filed all of Q3(a)'s working under Q3(b);
                # every part of the 2021 Ordinary Q3 and Q5 was lost that way.
                if letter and prev_l and letter < prev_l and not self.old:
                    return None
                if letter == prev_l and roman and prev_r \
                        and _rank(roman) < _rank(prev_r):
                    return None
        key = (q, letter, roman)
        if key in self.units:
            return self.units[key]
        unit = Unit(key, page)
        unit.y0 = y
        self.units[key] = unit
        return unit

    def _is_cue(self, q, text):
        """Is this row part of the question the old scheme reprints?

        Decided against the PAPER — the scheme reprints the paper's own
        sentences word for word — which is also the evidence that this unit is
        paired with the ask it claims. A row the paper does not print is where
        the reprint stops and the solution starts.
        """
        sq = _squash(text)
        if len(sq) < 6:
            return False
        if any(sq in want for want in
               (self.paper_text.get(q) or '', self.paper_text.get(None) or '')):
            return True
        # The reprint carries the question's own NOTATION, and a stacked
        # fraction inside it does not always survive the reading: 2021 Higher
        # reprints Q5(b)(i) as "Show that k = √3(1−e)/(2(1 + e))" and the
        # reader returns "Show that k = (^√³⁽¹^−^e^))/(2(1 + e))" — the same
        # sentence with the fraction's digits raised. Unrecognised, that line
        # CLOSED the reprint, and the two lines of the question below it were
        # then read as the first marking point of (b)(ii).
        #
        # Compared on LETTERS alone the two are one string, because the digits
        # are all the mangling touched. Held to the question's own text rather
        # than the whole paper, and to a run of ten letters: the longest line
        # of the solution on that page reduces to nine, so no step can meet
        # this by accident.
        letters = re.sub(r'\d+', '', sq)
        return (len(letters) >= 10
                and letters in re.sub(r'\d+', '', self.paper_text.get(q) or ''))

    def _finish(self):
        # A key the head opened that carries no mark of its own, while the
        # parts UNDER it do, is a parent — "1(a)" over "1(a)(i)" and
        # "1(a)(ii)" — not a refusal. Reporting those as refusals buried the
        # real ones under fifty parents.
        priced = {k for k, u in self.units.items() if u.groups}
        for key, unit in list(self.units.items()):
            if not unit.groups:
                # A key is a PARENT only of keys strictly beneath it: a
                # question over its parts, or a part over its romans. A leaf
                # with a roman of its own is nobody's parent — treating it as
                # one (because a letterless question's key has no letter
                # either) swallowed 2025 Higher Q2(iii) silently instead of
                # reporting that its mark had not been read.
                if key[2] is not None:
                    parent = False
                elif key[1] is not None:
                    parent = any(o[0] == key[0] and o[1] == key[1]
                                 and o[2] is not None for o in priced)
                else:
                    parent = any(o[0] == key[0] and o != key for o in priced)
                if not parent:
                    self.refused.append(
                        (key, 'the scheme prints no mark for this ask'))
                del self.units[key]
                continue
            if all(not t for t, _ in unit.groups):
                unit.drawn = True

    # --------------------------------------------------------------- lookups
    def ref(self, key):
        q, letter, roman = key
        tail = f'Q{q}'
        if letter:
            tail += f'({letter})'
        if roman:
            tail += f'({roman})'
        return f'{self.year} {self.level.upper()} {tail}'

    def question_totals(self):
        out = collections.Counter()
        for key, unit in self.units.items():
            out[key[0]] += unit.total
        return out


def _rank(roman):
    return ROMANS.index(roman) if roman in ROMANS else 99


# --------------------------------------------------------------- the gate ---
START = '<!-- markbank:applied-maths-solution -->'
END = '<!-- /markbank:applied-maths-solution -->'


def append(year, level):
    """Write this scheme's repaired rendering into its markdown, for the gate.

    The same argument append-scheme-notation.py makes for Mathematics. The
    converted markdown holds the scheme with its fractions in halves, its
    italics doubled and half its letters named wrongly by the font — "1 / (i)
    𝑠𝑠= 𝑢𝑢𝑡𝑡+ 2 𝑎𝑎𝑡𝑡2" across two lines — so a step lifted correctly from the
    PDF cannot be traced to the gate's copy of it.

    What is appended is the SOLUTION COLUMN, every line of it, in the order the
    page prints it: no line is selected for being on a card, and none is
    rewritten. What is left out is the other column and the page's furniture —
    the marks, the running footer, and the text inside a diagram — because
    those are not the answer and, left in, they sit BETWEEN two lines of one
    step and stop comparableScheme() (which joins consecutive lines with a
    space) from seeing the step whole.
    """
    md = os.path.join(SCHEMES, f'{year}-{level}.md')
    S = AmScheme(year, level, paper_text=_paper_index(year, level))
    # Two renderings, in this order: every line of the solution column, and
    # then each PRICED STEP as the page sets it out — the run of lines the mark
    # in the margin is printed against, joined. The second is not a selection
    # or a rewrite; it is the same lines with the line breaks taken out, which
    # is how a reader sees a step and how a card has to quote it. It is needed
    # because a step's lines are not always adjacent in the first rendering:
    # two-dimensional working (a matrix, a stacked fraction, a table) puts a
    # numerator, a bracket or a table cell between them, and comparableScheme()
    # can only join lines that are neighbours.
    lines = S.solution_lines()
    lines += [t for u in S.units.values() for t, _m in u.groups if t]
    body = f'{START}\n' + '\n'.join(lines) + f'\n{END}\n'
    text = open(md, encoding='utf-8').read()
    if START in text:
        text = re.sub(re.escape(START) + r'.*?' + re.escape(END) + r'\n?', '',
                      text, flags=re.S)
    open(md, 'w', encoding='utf-8').write(text.rstrip('\n') + '\n\n' + body)
    return f'{year} {level}: appended {len(lines)} repaired lines'


def _paper_index(year, level):
    """What the paper prints, squashed, for telling a reprint from a solution.

    Keyed by question, and keyed by None for the paper WHOLE. The per-question
    text is assembled from paper.py's parts and stems, which is enough to say
    which ask a reprint belongs to, but not to say whether a given LINE was
    printed: a line of the paper regularly straddles two of those blocks, and
    the concatenation puts them in key order rather than reading order. The
    whole-paper reading has no seams, so a reprinted line is a contiguous
    substring of it exactly when the paper printed it.
    """
    import paper as PP
    P = PP.Paper('applied-maths', year, level)
    out = collections.defaultdict(str)
    for key, lines in P.parts.items():
        out[key[0]] += _squash(' '.join(lines))
    for key, lines in P.stems.items():
        out[key[0]] += _squash(' '.join(lines))
    import pymupdf
    whole = []
    for path in P.files:
        with pymupdf.open(path) as doc:
            for page in doc:
                whole.append(PP.unligature(PP._repair(page.get_text(),
                                                      'applied-maths')))
    out[None] = _squash(' '.join(whole))
    return out


def audit():
    bad = 0
    for path in sorted(glob.glob(os.path.join(SCHEMES, '*.pdf'))):
        stem = os.path.basename(path)[:-4]
        year, level = int(stem[:4]), stem[5:]
        S = AmScheme(year, level, paper_text=_paper_index(year, level))
        totals = S.question_totals()
        odd = {q: v for q, v in totals.items() if v != 50}
        drawn = sum(1 for u in S.units.values() if u.drawn)
        # A printed total closes either a PART or the whole QUESTION — 2021
        # Ordinary prints "(50)" at the foot of Q3 and "(30)"/"(20)" for Q4's
        # two parts — so it is checked against whichever of the two it names.
        parts, whole = collections.defaultdict(int), collections.defaultdict(int)
        for k, u in S.units.items():
            parts[k[:2]] += u.total
            whole[k[0]] += u.total
        mismatch = []
        for k, u in S.units.items():
            if u.part_total is None:
                continue
            want = whole[k[0]] if u.part_total == whole[k[0]] else parts[k[:2]]
            if u.part_total != want:
                mismatch.append(f'{S.ref(k)} says {u.part_total}, '
                                f'steps make {parts[k[:2]]}')
        print(f'{stem}: {len(S.units)} units, {sum(u.total for u in S.units.values())} '
              f'marks, {drawn} drawing-only, {len(S.refused)} refused')
        if odd:
            print(f'    QUESTION TOTALS not 50: {dict(sorted(odd.items()))}')
            bad += len(odd)
        if mismatch:
            print(f'    PART TOTAL disagrees: {mismatch[:6]}')
            bad += len(mismatch)
        for key, why in S.refused[:5]:
            print(f'    REFUSED {S.ref(key)}: {why}')
    return 1 if bad else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('year', nargs='?', type=int)
    ap.add_argument('level', nargs='?')
    ap.add_argument('--audit', action='store_true')
    ap.add_argument('--append', action='store_true')
    ap.add_argument('--full', action='store_true')
    args = ap.parse_args()
    if args.append:
        for path in sorted(glob.glob(os.path.join(SCHEMES, '*.pdf'))):
            stem = os.path.basename(path)[:-4]
            print(append(int(stem[:4]), stem[5:]))
        return 0
    if args.audit or not args.year:
        return audit()
    S = AmScheme(args.year, args.level,
                 paper_text=_paper_index(args.year, args.level))
    print(f'{args.year} {args.level.upper()}: {len(S.units)} units')
    for key, unit in S.units.items():
        print(f'  {S.ref(key):<22} {unit.total:>3}m  {len(unit.groups)} steps'
              f'{"  DRAWN" if unit.drawn else ""}'
              f'{"  total=" + str(unit.part_total) if unit.part_total else ""}')
        if args.full:
            if unit.cue:
                print(f'      CUE  {unit.cue[:140]}')
            for t, m in unit.groups:
                print(f'      {m:>3}  {t[:120]}')
    for key, why in S.refused:
        print(f'  REFUSED {S.ref(key)}: {why}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
