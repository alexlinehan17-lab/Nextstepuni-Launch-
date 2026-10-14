"""The printed question itself, cropped from the paper, for every Maths card.

Text stems failed Maths twice over: the extractor attached the WRONG part's
context ("The diagram shows a cuboid" above a logs equation), and even a right
stem arrives with its notation mangled (3^(2m+1) for a typeset power) and its
diagram missing. The fix is to stop retelling the paper and show it: each card
gets a stitched crop of the SEC's own print — the letter's setup where the part
sits under one, the earlier sibling parts when the ask says "Hence", the
question's own setup when the part actually leans on it, and the part itself.
A crop cannot assert a context the paper does not print.

Geometry, not prose, drives the cropping. On every modern Maths paper the
letters sit at the left margin (x ~= 56.7) and the romans indent to x ~= 85;
letters run (a)-(f) and romans are drawn from {i, v, x}, so the two marker
alphabets cannot collide below (i). What bounds each region is its CONTENT,
not the next marker: the blank answer boxes the booklet prints under every
part are light-grey grids inside a large empty border, so a band ends at its
last dark ink — text, diagram, or table — and the answer furniture never
ships. Ink that overflows a band's top (a diagram set beside the marker,
started higher up the page) extends the band to carry the whole drawing.

Usage:
  python3 maths_question_figures.py --probe "2021 HL Paper 1 Q3(b)(ii)"
  python3 maths_question_figures.py --sitting 2021 hl
  python3 maths_question_figures.py --all
"""
import hashlib
import io
import json
import os
import re
import sys
from collections import OrderedDict

import pymupdf
from PIL import Image

import mathtext

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
PAPERS = os.path.join(ROOT, 'examiner-reports', 'maths', 'papers')
OUT = os.path.join(ROOT, 'exam-papers', 'maths', 'figures')
AUTHORED = os.path.join(ROOT, 'scripts', 'markbank', 'authored', 'maths.json')
SIDECAR = os.path.join(ROOT, 'scripts', 'markbank', 'authored',
                       'maths-question-figures.json')
CATALOGUE = os.path.join(ROOT, 'scripts', 'markbank', 'authored',
                         'maths-question-figures-catalogue.json')
# Per-card corrections to the automatic plan, written after LOOKING at a bad
# crop. Alongside planning switches, a verified override may provide explicit
# one-based PDF page regions. Those regions are useful where a two-column
# diagram and its prompt need to be stacked cleanly instead of carrying an
# answer grid or a neighbouring ask into the crop.
OVERRIDES = os.path.join(HERE, 'maths_qfig_overrides.json')
MANIFEST_JSON = os.path.join(ROOT, 'components', 'MarkBank', 'figures.json')
# The deck build repairs a subset font's broken ToUnicode map from this table
# (build-deck.mjs repairText), and a legacy crop's description is repaired the
# same way. Where the table cannot spell the band -- the 2019 Higher Paper 1
# font extracts digits as Greek numeral signs and a modifier prime ("(ʹx + ͳ)"
# for "(2x + 3)"), the 2018 papers set alpha and beta in NKo code points, the
# 2019 axis labels' middle dot is U+0D49 -- the description is the card's own
# lifted stem and prompt instead: alt text reading "f(x) = \u0375^x" is the
# wrong text, and a guessed digit would be worse.
GLYPHMAP = json.load(open(os.path.join(HERE, 'glyphmap.json'), encoding='utf-8'))
UNSPELT = re.compile('[\u02B9\u0370-\u0377\u0700-\u08FF\u0A80-\u0DFF\uE000-\uF8FF]')


def _glyphs(text):
    return ''.join(GLYPHMAP.get(ch, ch) for ch in text)


def _legacy_description(card, text):
    text = _glyphs(text)
    if UNSPELT.search(text):
        text = ' '.join(t for t in (card.get('stem'), card.get('questionText')) if t)
    return text


DPI = 170
SCALE = DPI / 72.0
# 28 on the left: a diagram's label can sit outside the prose margin — the
# "Trail" caption of 2021 OL P1 Q10(b) starts at x~32 and a 40pt clip printed
# it as "ail".
X0, X1 = 28.0, 560.0        # the text column, with room for diagram overhang
Y_TOP, Y_FOOT = 46.0, 792.0  # running footer starts at y ~= 799.7 everywhere
GAP = 18                     # px between stitched regions
PAD = 8                      # px of white retained around each trimmed region
WHITE = 247                  # a row whose darkest pixel is >= this is paper

LETTER = re.compile(r'^\(\s*([a-h])\s*\)')
ROMAN = re.compile(r'^\(\s*([ivx]{1,4})\s*\)')
QHEAD = re.compile(r'^Question\s+(\d{1,2})$')
TAIL_PAGE = re.compile(r'^(Page for extra work|Acknowledg|Copyright|Blank Page)', re.I)
# Booklets up to 2020 ("legacy") differ in three ways, each handled ONLY when
# Sitting.legacy is set, so every 2021+ crop is unchanged by construction:
#   * the extra-work pages open "You may use this page for extra work.";
#   * answer areas are bare light-grey grids with no dark frame round them;
#   * each spread prints a "previous | page | running" mark box in the bottom
#     margin, and the footer is set as "[ 3 ]" / "Mathematics" / "Paper 2 – ...".
LEGACY_TAIL = re.compile(r'^You may use this page for extra work'
                         r'|^Leaving Certi\S* \d{4} [–-] (?:Higher|Ordinary) Level', re.I)
LEGACY_DEAD = re.compile(r'^(?:previous|page|running)$'
                         r'|^(?:Concepts and skills|Contexts and applications?)$'
                         r'|^\(\d{1,3} marks\)$'
                         r'|^This question is continued on the next page\.?$', re.I)
# A legacy answer prompt: a label that ends in "=" or ":" once its writing
# space ("( , )", "____") is removed -- "Period =", "Centre: ( , )", "k:".
LEGACY_PROMPT = re.compile(r'^[^=:]{0,30}[=:]$')
LEGACY_FOOTER = re.compile(r'^(?:\[?\s*\d{1,2}\s*\]?|Mathematics|Paper \d\b.*|Leaving Certi.*)$')
# The running footer's y varies by booklet (783.4 on 2021 P2, 799.7 on 2021
# P1), so it is matched by TEXT, not by a fixed line: a static cutoff at 792
# half-cut the low footers into every deep crop on Paper 2.
FOOTER = re.compile(r'^(Leaving Certificate|Mathematics,? Paper|\d{1,2}$)')
# Lines that are page apparatus, not question content, wherever they sit:
# the continuation notice under a deep part, and the next section's banner
# stitched after a question's last ask.
DEAD_TEXT = re.compile(
    r'^This question continues on the next page\.?$'
    r'|^Section [A-Z]$'
    r'|^(?:Concepts and Skills|Contexts and Applications)$'
    r'|^\d{2,3} marks$'
    r'|^Answer (?:all|any) .{0,50}questions?(?: from this section)?\.?$'
    r'|^There is space for (?:more|extra) work .{0,40}$'
    r'|^\(?Continued (?:overleaf|on the next page)\)?\.?$')
# "Hence", "your answer to part (i)": the ask leans on the siblings before it.
# The ask CHAINS on an earlier part. "your answer" alone is not enough:
# "Give your answer in km" is a formatting instruction, and reading it as a
# chain suppressed the question stem on cards like 2021 OL P2 Q9(a)(i),
# which then shipped a bare one-line ask with its runway diagram left behind.
# A real chain names a part.
NEEDS_SIBLINGS = re.compile(
    r'\bHence\b'
    r'|\byour (?:answers?|values?|results?|graph|diagram)\s+(?:to|from|in)\s+part'
    r'|\b(?:in|from|to) parts? \('
    r'|\bpart \((?:[ivx]+|[a-h])\)', re.I)
# The part reaches OUTSIDE its letter, back to the question's own setup: it
# names the stem's diagram/graph/table or a point/segment the stem defined.
# "the equation" is deliberately absent — a part that says "solve the
# equation ..." is quoting itself, and matching it dragged an unrelated
# cuboid diagram onto a logs question.
NEEDS_QSTEM = re.compile(
    r'\b(?:the|this) (?:diagram|graph|table|figure|curve|map|pattern|data)\b'
    # citation-style only: "the model above", "shown above" — never the
    # spatial prose of "height above level ground".
    r'|\b(?:shown|given|defined|described)\s+above\b'
    r'|\b(?:diagram|table|graph|figure|model|equation|function)\s+above\b'
    r'|\bshown\b|\[\s*[A-Z]{2}\s*\]|\bpoint [A-Z]\b', )


def lines_of(doc, legacy=False):
    """Printed lines: (page, y0, y1, x0, text), furniture split out."""
    out = []
    dead = []
    for n in range(doc.page_count):
        for b in doc[n].get_text('dict')['blocks']:
            for ln in b.get('lines', []):
                txt = ''.join(s['text'] for s in ln['spans']).strip()
                if not txt:
                    continue
                x0 = min(s['bbox'][0] for s in ln['spans'])
                x1 = max(s['bbox'][2] for s in ln['spans'])
                y0 = min(s['bbox'][1] for s in ln['spans'])
                y1 = max(s['bbox'][3] for s in ln['spans'])
                if y0 >= Y_FOOT - 4:
                    continue
                if y0 > 700 and FOOTER.match(txt):
                    continue
                if legacy and y0 > 740 and LEGACY_FOOTER.match(txt):
                    continue
                if DEAD_TEXT.match(txt) or (legacy and LEGACY_DEAD.match(txt)):
                    dead.append((n, y0, y1, x0, txt, x1))
                    continue
                out.append((n, y0, y1, x0, txt, x1))
    out.sort(key=lambda l: (l[0], round(l[1], 1), l[3]))
    dead.sort(key=lambda l: (l[0], round(l[1], 1), l[3]))
    return out, dead


def _ascii(text):
    """Fold mathematical alphanumeric symbols to ASCII for matching.

    The paper's text layer sets variables in Mathematical Italic (U+1D400
    block) and Planck-constant ℎ for the letter h, so an ASCII search for
    "h =" finds nothing in the very line that defines h(x)."""
    out = []
    for ch in text:
        o = ord(ch)
        if 0x1D400 <= o <= 0x1D7FF:
            for base, first in ((0x1D400, 'A'), (0x1D41A, 'a'), (0x1D434, 'A'),
                                (0x1D44E, 'a'), (0x1D468, 'A'), (0x1D482, 'a'),
                                (0x1D5A0, 'A'), (0x1D5BA, 'a'), (0x1D7CE, '0'),
                                (0x1D7E2, '0')):
                span = 10 if first == '0' else 26
                if base <= o < base + span:
                    out.append(chr(ord(first) + o - base))
                    break
            else:
                out.append(ch)
        elif ch == '\u210e':
            out.append('h')
        elif ch == '\u2113':
            out.append('l')
        elif ch == '\u212f':
            out.append('e')
        else:
            out.append(ch)
    return ''.join(out)


def _dark(color):
    return color is not None and max(color) < 0.6


class Sitting:
    def __init__(self, year, level, component):
        self.year, self.level, self.component = year, level, component
        self.paper_no = 1 if component == 100 else 2
        path = os.path.join(PAPERS, f'{year}-{level}-{component}-paper.pdf')
        self.path = path
        self.doc = pymupdf.open(path)
        self.legacy = int(year) <= 2020
        self.lines, self.dead = lines_of(self.doc, self.legacy)
        # Where this booklet's footer actually starts, per page.
        self.foot = {}
        for n in range(self.doc.page_count):
            for b in self.doc[n].get_text('blocks'):
                t = ' '.join(b[4].split())
                if b[1] > 700 and FOOTER.match(t):
                    self.foot[n] = min(self.foot.get(n, Y_FOOT), b[1] - 2)
        self._ink = {}
        self._furniture = {}
        self._boxes = {}
        self._rules = {}
        self._all_bands = []
        self._index()

    # ---- geometry index ----

    def _index(self):
        self.tail = None
        for n in range(self.doc.page_count):
            first = next((l for l in self.lines if l[0] == n), None)
            if first and (TAIL_PAGE.match(first[4])
                          or (self.legacy and LEGACY_TAIL.match(first[4]))):
                self.tail = (n, 0.0)
                break
        self.q = OrderedDict()
        current = None
        for (page, y0, y1, x0, txt, x1) in self.lines:
            if self.tail and (page, y0) >= self.tail:
                break
            h = QHEAD.match(txt)
            if h and x0 < 120:
                current = int(h.group(1))
                self.q[current] = {'head': (page, y0, y1), 'markers': []}
                continue
            if current is None:
                continue
            m = LETTER.match(txt)
            if m and x0 < 72:
                rest = txt[m.end():].strip()
                self.q[current]['markers'].append(('letter', m.group(1), page, y0))
                rm = ROMAN.match(rest)
                if rm:   # "(b)  (i)" welded on one line
                    self.q[current]['markers'].append(('roman', rm.group(1), page, y0))
                continue
            m = ROMAN.match(txt)
            if m and x0 < 118:
                self.q[current]['markers'].append(('roman', m.group(1), page, y0))

    def ink(self, page):
        """Dark drawings and raster images worth keeping, as rects.

        The answer boxes the booklet prints are excluded by signature: a wide,
        tall, DARK border rect with not a single line of text inside is answer
        furniture — a data table or a completed diagram always holds text.
        Its grid interior is light grey and fails the darkness test on its own.
        """
        if page in self._ink:
            return self._ink[page]
        p = self.doc[page]
        text_lines = [l for l in self.lines if l[0] == page]
        drawings = [d for d in p.get_drawings()
                    if _dark(d.get('color')) or _dark(d.get('fill'))]
        # The answer frames first, so ink INSIDE one — the little corner
        # mark some booklets print in the writing space — dies with its frame.
        # A frame is furniture even when it is not empty: 2021 P1 Q2(b) prints
        # "Show:" and a "Roots = ( , , )" template inside its grid. What tells
        # furniture from a data table or a labelled graph is how LITTLE text
        # the frame holds — a prompt or two, against a table's many cells.
        frames = []
        boxes = []
        for d in drawings:
            r = d['rect']
            # Not every answer box spans the column: 2022 Higher Level
            # Q6(c) sets a half-width grid beside the working, and a
            # 420pt floor let every one of those through.
            # Answer boxes come in every size: the "Period: / Range:" box of
            # 2021 HL P2 Q9(b) is 57pt tall, and 2021 OL P1 Q8(f) sets three
            # 138x34 boxes beside its sub-parts. What they share is being an
            # EMPTY RECTANGLE — a rect in the path, no bézier, no text and no
            # drawing inside. A figure fails at least one of those.
            if r.width > 80 and r.height > 20:
                # Inside means inside BOTH ways. Testing only the vertical
                # span counted a neighbouring figure's labels as the box's
                # contents: the Argand diagram beside 2021 OL P1 Q2's answer
                # box lent it 17 axis numbers, so the box read as a data
                # table and shipped blank on every card of that question.
                inside = [l for l in text_lines
                          if r.y0 - 2 <= l[1] and l[2] <= r.y1 + 2
                          and r.x0 - 2 <= l[3] <= r.x1 + 2]
                # A prompt or two ("Show:", "Roots = ( , , )") or a template
                # of bare labels ("Diagram: / Given: / To Prove: / Proof:")
                # is furniture; a data table or a labelled plot holds more.
                # Measure the line's INK, not its length: the answer template
                # "x = ______ , ______ , or ______" runs 53 characters of
                # which six are writing, and a raw length test let every 2022
                # Higher Level answer box through.
                ink = [re.sub(r'[_\s.·]+', '', l[4]) for l in inside]
                # An answer box is EMPTY: its grid is light grey, so no dark
                # ink lies inside it. A plot area is the opposite — a curve
                # and its axes are dark ink inside exactly such a rectangle,
                # and with only sparse labels ("y", "x", "A(0, k)") it passes
                # every text test an answer box passes. Without this the mask
                # painted out the sine curve of 2021 HL Q5(b) and left a
                # stranded arrowhead.
                # An answer box IS a rectangle: its path is a single 're'
                # plus a few rules. A drawn figure is not — the sine curve of
                # 2021 HL Q5(b) is 39 line segments and 11 béziers, and on
                # extent alone it looked exactly like an answer box, so the
                # mask painted the graph out and left a stranded arrowhead.
                # A rectangle in the path is the answer box's signature. Across
                # the whole corpus 961 answer boxes carry one and not a single
                # figure does: the 29 candidates without a rect are all
                # geometry — triangles labelled A, C, D, E, a field diagram
                # with 35 m and 50 degrees — and a "few items" fallback was
                # masking every one of them.
                kinds = [i[0] for i in d.get('items', ())]
                boxlike = 'c' not in kinds and kinds.count('re') >= 1
                drawn_inside = any(
                    o is not d
                    and r.x0 - 1 <= o['rect'].x0 and o['rect'].x1 <= r.x1 + 1
                    and r.y0 - 1 <= o['rect'].y0 and o['rect'].y1 <= r.y1 + 1
                    and (o['rect'].width > 10 or o['rect'].height > 10)
                    for o in drawings)
                sparse = (len(inside) <= 6 and sum(len(t) for t in ink) < 60
                          and all(len(t) < 28 for t in ink))
                big = r.width > 170 and r.height > 45
                if self.legacy and boxlike and big and drawn_inside:
                    # Legacy booklets set the diagram INSIDE the answer box
                    # (2019 P2 Q3(b): the circle sits top-right of the grid).
                    # The box is furniture; the drawing inside it is not.
                    # Thin rules inside (a "Mean | Median" divider) are not
                    # a drawing: such a box is an answer template.
                    art = [o['rect'] for o in drawings
                           if o is not d
                           and r.x0 - 1 <= o['rect'].x0 and o['rect'].x1 <= r.x1 + 1
                           and r.y0 - 1 <= o['rect'].y0 and o['rect'].y1 <= r.y1 + 1
                           and o['rect'].width > 12 and o['rect'].height > 12
                           and not (abs(o['rect'].width - r.width) < 4
                                    and abs(o['rect'].height - r.height) < 4)]
                    if art:
                        boxes.append((r, art))
                    elif sparse:
                        frames.append(r)
                    continue
                if boxlike and not drawn_inside and (
                        not inside or (big and sparse)):
                    frames.append(r)
        # An erased dotted answer rule leaves its end marks behind: tiny dark
        # specks sitting alone in the white. A mark under 4pt with no other
        # ink within 25pt is not part of any drawing, and reads as dirt on
        # the page. Erase those too.
        # Neighbours are CONTENT, not furniture: the specks left by an erased
        # answer rule sit right beside the box they belonged to, so counting
        # that box as a neighbour kept every speck alive.
        kept = [d['rect'] for d in drawings
                if (d['rect'].width >= 4 or d['rect'].height >= 4)
                and not any(f.x0 - 1 <= d['rect'].x0 and d['rect'].x1 <= f.x1 + 1
                            and f.y0 - 1 <= d['rect'].y0 and d['rect'].y1 <= f.y1 + 1
                            for f in frames)]
        for d in drawings:
            r = d['rect']
            if r.width < 4 and r.height < 4 and not any(
                    o.y0 - 25 <= r.y0 <= o.y1 + 25
                    and o.x0 - 25 <= r.x0 <= o.x1 + 25 for o in kept):
                frames.append(pymupdf.Rect(r.x0 - 2, r.y0 - 2,
                                           r.x1 + 2, r.y1 + 2))
        mark_box = None
        lframes = []
        if self.legacy:
            lframes = self._legacy_grid_frames(p, text_lines)
            frames += lframes
            # The spread's mark box (bottom right) is drawn even where its
            # "previous | page | running" labels are not printed.
            for d in drawings:
                r = d['rect']
                if r.y0 >= 735 and r.x0 >= 380 and r.y1 <= 805 and (r.width < 3 or r.height < 3):
                    lframes.append(pymupdf.Rect(r.x0 - 1, r.y0 - 1, r.x1 + 1, r.y1 + 1))
                    frames.append(lframes[-1])
            marks = [l for l in self.dead if l[0] == page and LEGACY_DEAD.match(l[4])]
            if marks:
                mark_box = pymupdf.Rect(min(l[3] for l in marks) - 30, min(l[1] for l in marks) - 12,
                                        max(l[5] for l in marks) + 30, max(l[2] for l in marks) + 30)
        self._furniture[page] = frames
        self._boxes[page] = boxes
        rects = []
        for d in drawings:
            r = d['rect']
            if r.width < 2 and r.height < 2:
                continue
            if r.width > 420 and r.height < 4:
                # A long thin rule is page furniture and must not anchor a
                # window — but it is still INK, and a graph's x-axis looks
                # exactly like one. Excluding it outright let the mask paint
                # over the axis of 2021 HL Q5(b), leaving a floating
                # arrowhead beside a graph with no x-axis.
                self._rules.setdefault(page, []).append(r)
                continue
            if any(f.y0 - 1 <= r.y0 and r.y1 <= f.y1 + 1
                   for f in frames if not any(f is g for g in lframes)):
                continue               # the frame, or a mark inside one
            if any(pymupdf.Rect(f.x0 - 4, f.y0 - 4, f.x1 + 4, f.y1 + 4).contains(r) for f in lframes):
                continue               # a legacy grid's own hairlines, or the mark box
            if mark_box is not None and mark_box.contains(r):
                continue               # legacy "previous | page | running" box
            if any(abs(r.x0 - b.x0) < 1 and abs(r.y0 - b.y0) < 1
                   and abs(r.x1 - b.x1) < 1 and abs(r.y1 - b.y1) < 1 for b, _ in boxes):
                continue               # a legacy answer box's own border
            if self.legacy and not p.rect.contains(r):
                # 2019's printer's crop marks run off the page; the page-sized
                # one counted as ink spared EVERY row from the furniture mask.
                continue
            rects.append(r)
        for info in p.get_images(full=True):
            for r in p.get_image_rects(info[0]):
                if r.width > 470 and r.height > 700:
                    continue           # page-covering watermark, not content
                if any(f.y0 - 1 <= r.y0 and r.y1 <= f.y1 + 1 for f in frames):
                    continue
                if mark_box is not None and mark_box.intersects(r):
                    continue
                if self.legacy and r.y0 >= 760 and r.height < 30:
                    continue           # 2019's bottom-margin barcode strip
                rects.append(r)
        self._ink[page] = rects
        return rects

    def _legacy_grid_frames(self, p, text_lines):
        """Legacy answer areas: clusters of light-grey hairlines with no frame.

        A cluster is answer furniture when nothing dark is drawn inside it and
        it holds at most a prompt or two ("k:", "Answer:") -- a plotting grid
        carries dark axes and a data table carries many cells of text, and
        both are kept exactly as the paper prints them.
        """
        hair = []
        dark = []
        dark_hair = []
        for d in p.get_drawings():
            r, f = d['rect'], d.get('fill') or d.get('color')
            if f is None:
                continue
            thin = r.width < 2.5 or r.height < 2.5
            if 0.6 <= min(f) and max(f) <= 0.92 and thin:
                hair.append(pymupdf.Rect(r))
            elif max(f) < 0.6:
                if thin and max(r.width, r.height) > 8:
                    dark_hair.append(pymupdf.Rect(r))
                if r.width >= 2 or r.height >= 2:
                    dark.append(r)

        def cluster(rects):
            clusters = []
            for r in sorted(rects, key=lambda r: (r.y0, r.x0)):
                g = pymupdf.Rect(r.x0 - 3, r.y0 - 3, r.x1 + 3, r.y1 + 3)
                for c in [c for c in clusters if c.intersects(g)]:
                    clusters.remove(c)
                    g |= c
                clusters.append(g)
            return clusters

        def inside_text(c):
            inside = [l for l in text_lines
                      if c.y0 - 2 <= l[1] and l[2] <= c.y1 + 2 and c.x0 - 2 <= l[3] <= c.x1 + 2]
            return inside, [re.sub(r'[_\s.·]+', '', l[4]) for l in inside]

        out = []
        for c in cluster(hair):
            if c.width < 80 or c.height < 20:
                continue
            # A plotting grid carries its own dark axes INSIDE it; a sketching
            # grid set beside a diagram merely overlaps that diagram's edge.
            def contained(r):
                inter = pymupdf.Rect(r) & c
                return (r.width > 6 and r.height > 6 and not inter.is_empty
                        and inter.width * inter.height >= 0.8 * r.width * r.height)
            if any(contained(r) for r in dark):
                continue
            inside, ink = inside_text(c)
            if len(inside) <= 6 and sum(len(t) for t in ink) < 80:
                out.append(pymupdf.Rect(c.x0 + 3, c.y0 + 3, c.x1 - 3, c.y1 - 3))
        # A dark-ruled answer template ("Period = | Range =", "a = | b =",
        # "Correlation Coefficient = |   |"): every line inside it is a prompt
        # that ends in "=" or ":". A data or tick table holds values, and stays.
        for c in cluster(dark_hair):
            if c.width < 60 or c.height < 14:
                continue
            inside, ink = inside_text(c)
            if not inside or len(inside) > 8:
                continue
            prompts = [re.sub(r'[(),\s_.]+', '', l[4]) for l in inside]
            if all(LEGACY_PROMPT.match(t) for t in prompts if t):
                out.append(pymupdf.Rect(c.x0 + 2, c.y0 + 2, c.x1 - 2, c.y1 - 2))
        return out

    def furniture_line(self, page, y0, y1, x0=None):
        """True when a text line sits inside an excluded answer frame — the
        "Show:" prompt must not hold a window open for its dead grid.

        Inside means inside BOTH ways. Judging on the vertical span alone
        made an ask furniture because a small answer box sat beside it at the
        same height: 2021 OL P1 Q8(f)(iii) lost its own question that way.
        """
        self.ink(page)
        if any(f.y0 - 2 <= y0 and y1 <= f.y1 + 2
               and (x0 is None or f.x0 - 2 <= x0 <= f.x1 + 2)
               for f in self._furniture.get(page, [])):
            return True
        for box, art in self._boxes.get(page, []):
            if box.y0 - 2 <= y0 and y1 <= box.y1 + 2 and (
                    x0 is None or box.x0 - 2 <= x0 <= box.x1 + 2):
                if x0 is None or not any(
                        a.x0 - 15 <= x0 <= a.x1 + 15 and a.y0 - 15 <= y0 and y1 <= a.y1 + 15
                        for a in art):
                    return True
        return False

    def _q_end(self, qnum):
        nums = list(self.q)
        i = nums.index(qnum)
        if i + 1 < len(nums):
            return self.q[nums[i + 1]]['head'][:2]
        return self.tail or (self.doc.page_count, 0.0)

    def band_text(self, bands, limit=None):
        if self.legacy:
            flat = self._legacy_band_text(bands)
            return flat if limit is None else flat[:limit]
        words = []
        for (sp, sy), (ep, ey) in bands:
            for (page, y0, y1, x0, txt, x1) in self.lines:
                if (sp, sy - 1) <= (page, y0) and (page, y0) < (ep, ey) and \
                        not self.furniture_line(page, y0, y1, x0):
                    words.append(txt)
        flat = ' '.join(' '.join(words).split())
        # This is a screen reader's only description of the crop, and raw it is
        # the font's mangling verbatim: "(\u0b36\u0b3e\u0b38\u0b5c) = 0 + \U0001d458\U0001d456, where
        # \U0001d458\u2208\u2124". Demangled it says what the paper says.
        try:
            flat = mathtext.clean_like([self.path], flat) or flat
        except Exception:                                   # noqa: BLE001
            flat = mathtext.demangle(flat)
        return flat if limit is None else flat[:limit]

    def _repair(self, fragment):
        """`fragment` demangled and, where the paper allows, repaired — but
        never a repair that says more or less than the fragment does.

        clean_like locates a fragment by its PREFIX and then takes as many
        document characters as the fragment has. When the fragment skips a
        row the document prints between its pieces, that reads the skipped row
        back in: 2017 OL P1 Q6(b) masks "(a) Find his total income..." in the
        picture and its alt text still said it, and 2017 HL P2 Q7(b)(ii)'s
        described (i)'s ask word-interleaved with its own."""
        plain = mathtext.spacing(mathtext.demangle(fragment))
        try:
            fixed = mathtext.clean_like([self.path], fragment) or plain
        except Exception:                                   # noqa: BLE001
            return plain
        if abs(len(mathtext._squash(fixed)) - len(mathtext._squash(plain))) > 3:
            return None
        return fixed

    def _legacy_band_text(self, bands):
        """The words a legacy crop shows, each band repaired on its own and
        each row once: two bands that share rows (a stem band and the art band
        that reaches back over it) described the stem twice."""
        groups = []
        for (sp, sy), (ep, ey) in bands:
            groups.append([l for l in self.lines
                           if (sp, sy - 1) <= (l[0], l[1]) < (ep, ey)])
        return self._describe_rows(groups)

    def region_text(self, regions):
        """The words an explicit-region crop shows. A region can be narrowed
        to a column (x0/x1) and can erase rectangles, and the text beside or
        under them is not in the picture: 2017 HL P2 Q3(a) keeps the triangle
        column down to B, and its alt text read out "(b) Find the
        co-ordinates of B" from the column beside it."""
        groups = []
        for region in regions:
            page = int(region['page']) - 1
            top, bottom = float(region['top']), float(region['bottom'])
            rx0, rx1 = float(region.get('x0', X0)), float(region.get('x1', 600))
            erase = [pymupdf.Rect(*r) for r in region.get('erase', [])]
            rows = []
            for l in self.lines:
                if l[0] != page or not (top - 1 <= l[1] and l[2] <= bottom + 1):
                    continue
                cx, cy = (l[3] + l[5]) / 2, (l[1] + l[2]) / 2
                if not (rx0 <= cx <= rx1):
                    continue
                if any(e.contains(pymupdf.Point(cx, cy)) for e in erase):
                    continue
                rows.append(l)
            groups.append(rows)
        return self._describe_rows(groups)

    def _describe_rows(self, groups):
        seen, out = set(), []
        for rows in groups:
            rows = [l for l in rows
                    if not self.furniture_line(l[0], l[1], l[2], l[3])
                    and (l[0], l[1], l[3]) not in seen]
            seen.update((l[0], l[1], l[3]) for l in rows)
            if not rows:
                continue
            frag = ' '.join(' '.join(l[4] for l in rows).split())
            whole = self._repair(frag)
            if whole is None:
                whole = ' '.join(self._repair(l[4]) or
                                 mathtext.spacing(mathtext.demangle(l[4]))
                                 for l in rows)
            out.append(whole)
        return ' '.join(' '.join(out).split())

    # ---- the per-card plan ----

    def _art_span(self, band):
        """The band narrowed to the artwork inside it, or None if it has none."""
        (sp, sy), (ep, ey) = band
        hits = []
        for page in range(sp, min(ep, self.doc.page_count - 1) + 1):
            lo = sy if page == sp else Y_TOP
            hi = ey if page == ep else Y_FOOT
            for r in self.ink(page):
                if r.y0 >= lo - 1 and r.y1 <= hi + 1 and (r.width > 30 or r.height > 30):
                    hits.append((page, r.y0, r.y1))
        if not hits:
            return None
        top = min(hits, key=lambda h: (h[0], h[1]))
        bot = max(hits, key=lambda h: (h[0], h[2]))
        return ((top[0], max(Y_TOP, top[1] - 6)), (bot[0], min(Y_FOOT, bot[2] + 6)))

    def plan(self, qnum, letter, roman, part_text='', force=None):
        """(bands, note): the page/y bands whose stitch is the card's context."""
        force = force or {}
        info = self.q.get(qnum)
        if not info:
            return None, f'Q{qnum} not indexed'
        head_page, head_y0, head_y1 = info['head']
        q_end = self._q_end(qnum)
        marks = info['markers']

        def pos(m):
            # The marker prints a hair BELOW its row's own text ("(a)" at
            # y324.6 beside its ask at y322.2), so a boundary at the marker's
            # y would split the row between two bands. Sit it just above.
            return (m[2], m[3] - 4.0)

        if not letter and not roman:
            return [((head_page, head_y1), q_end)], 'whole question'

        first_marker = pos(marks[0]) if marks else q_end
        qstem = ((head_page, head_y1), first_marker) \
            if first_marker > (head_page, head_y1) else None
        # A band between the head and the first marker is not automatically a
        # question stem. 2021 HL Q1 sets part (a)'s fraction on two lines that
        # begin ABOVE the "(a)" marker, so the band holds nothing but the spill
        # of a sibling — and shipping it put an unrelated complex-division
        # problem on top of every other part of Q1. A real stem is set at the
        # margin (x <= 60) or is a drawing; part text is indented past 80.
        if qstem and not self._stem_is_real(qstem):
            qstem = None

        li = next((i for i, m in enumerate(marks)
                   if m[0] == 'letter' and m[1] == letter), None)
        if letter and li is None:
            return None, f'({letter}) not found in Q{qnum}'

        if letter and not roman:
            # A letter part leans on the question's setup as a rule — "find
            # the volume of the cuboid" is unanswerable without the cuboid.
            l_end = next((pos(m) for m in marks[li + 1:] if m[0] == 'letter'), q_end)
            nxt = next((m for m in marks[li + 1:] if m[0] == 'letter'), None)
            own = self._trim_next_setup((pos(marks[li]), l_end), nxt)
            # A letter part usually leans on the question's setup — "find the
            # volume of the cuboid" needs the cuboid — but not always: 2021 HL
            # P2 Q10(b) is a self-contained expected-value problem printed
            # under a stem about O-negative blood donors, and carrying that
            # stem put an 8% distractor above an unrelated ask. Carry it when
            # the two share a subject, or when the part is too short to stand
            # on its own.
            own_text = self.band_text([own], 4000)
            take = force.get('qstem',
                             self._shares_subject(own_text,
                                                  self.band_text([qstem], 4000))
                             or len(own_text) < 120) if qstem else False
            bands = [qstem] if take else []
            bands.append(own)
            bands = self._hunt_definitions(bands, marks, li, qstem, part_text,
                                           force, q_end)
            return bands, 'letter part'

        scope = marks[li:] if letter else marks
        if letter:
            nl = next((j for j, m in enumerate(scope[1:], 1) if m[0] == 'letter'),
                      len(scope))
            scope = scope[:nl]
        ri = next((i for i, m in enumerate(scope)
                   if m[0] == 'roman' and m[1] == roman), None)
        if ri is None:
            return None, f'({letter or ""})({roman}) not found in Q{qnum}'
        r_end = pos(scope[ri + 1]) if ri + 1 < len(scope) else (
            next((pos(m) for m in marks[li + 1:] if m[0] == 'letter'), q_end)
            if letter else q_end)
        first_roman = next((pos(m) for m in scope if m[0] == 'roman'), None)

        bands, ctx = [], []
        has_letter_stem = False
        if letter and first_roman and first_roman > pos(scope[0]):
            stem_band = (pos(scope[0]), first_roman)
            # A band can be geometrically present and hold nothing at all —
            # "(a) (i)" set on one line leaves a zero-height letter stem. An
            # empty band counted as context, so the "nothing else carries
            # setup" rule never fired and 2021 OL Q9 shipped a bare ask with
            # its runway diagram left on the page.
            if self.band_text([stem_band], 40).strip():
                bands.append(stem_band)
                ctx.append(self.band_text(bands[-1:], 2000))
                has_letter_stem = True
        # Siblings ride along when the ask chains on them ("Hence", "your
        # answer") — and also when the letter's setup points BELOW itself
        # ("as shown in the diagram below"): the diagram it promises is
        # printed under an earlier sibling, so the chain must come too.
        # "Use your graph to estimate each of the following values" introduces
        # the sub-parts, not printed matter below them — reading "following"
        # as a pointer pulled every sibling into every crop of 2021 OL Q8(f)
        # and its like. A real pointer names what is below.
        stem_points_down = bool(re.search(
            r'\b(?:shown|diagram|graph|table|figure|picture|drawing)\s+below\b'
            r'|\bbelow\s+(?:shows?|is|are)\b|\bas shown\b',
            ' '.join(ctx), re.I))
        # Sibling parts ride along only on an explicit chain. Shared content
        # words are useless here — parts of one question always talk about the
        # same thing, so that test pulled every earlier sibling into every
        # crop and the audit fleet called it irrelevant context 120 times.
        # A sibling is another QUESTION on the card. Showing one leaves the
        # student unable to tell which of the two the card is asking, so it
        # rides along only where the paper itself makes it necessary:
        #
        #   * the ask CHAINS on it -- "Hence", "your answer to part (i)" --
        #     and cannot be attempted without it, or
        #   * the setup promises something printed below AND that band really
        #     does carry artwork.
        #
        # The second test used to be the promise alone, which is only a form of
        # words: "shown below" pulled the previous part onto 67 cards whose ask
        # needed nothing from it, among them "Find h'(x), the derivative of
        # h(x)" carrying part (a)'s whole table.
        sib_band = (first_roman, pos(scope[ri])) if (first_roman and ri > 0) else None

        def _band_has_art(band):
            if not band:
                return False
            (sp, sy), (ep, ey) = band
            for page in range(sp, min(ep, self.doc.page_count - 1) + 1):
                lo = sy if page == sp else Y_TOP
                hi = ey if page == ep else Y_FOOT
                for r in self.ink(page):
                    if r.y0 >= lo - 1 and r.y1 <= hi + 1 and (
                            r.width > 30 or r.height > 30):
                        return True
            return False

        chains = bool(NEEDS_SIBLINGS.search(part_text))
        siblings = force.get('siblings',
                             chains or (stem_points_down and _band_has_art(sib_band))
                             ) and ri > 0
        if siblings:
            band = (first_roman, pos(scope[ri]))
            if not chains:
                # The sibling is here for the DIAGRAM its setup promised, not
                # for its question. Taking the whole band brought that question
                # along too, and the card then showed two asks with nothing
                # saying which one it wanted -- 27 cards did that.
                #
                # So narrow to the artwork. And where the sibling holds NO
                # artwork, drop it: the promised diagram is already in the
                # letter's own setup above it (2021 OL P1 Q9(a) prints the dot
                # patterns under "(a)", so the (i) band is nothing but (i)'s
                # question). Where the ask CHAINS -- "Hence" -- the sibling
                # stays whole, because the paper has made it part of this ask.
                band = self._art_span(band)
            if band:
                bands.append(band)
            ctx.append(self.band_text(bands[-1:], 2000))
        # The question stem rides along when the part reaches for it by name
        # ("the diagram", "above") — and, since the 2021 OL "the lake" audit
        # finding, whenever NOTHING else carries any setup: a one-line ask
        # about a definite thing must not ship bare. The price is an
        # occasionally redundant printed stem, which is faithful noise; a
        # missing diagram is an unanswerable card.
        # The fallback — carry the question stem when nothing else holds any
        # setup — must still be RELEVANT. A printed cuboid above a
        # self-contained logs equation is the exact defect this tool exists to
        # remove, so the fallback fires only when the ask and the stem share a
        # content word: "the runway" is answered by the stem that draws the
        # runway; "find the two roots of f(x) = 3x^2 + 8x - 35" shares nothing
        # with a cuboid and travels alone.
        bare = not has_letter_stem and not siblings
        # The question stem rides along when the part reaches for it by name
        # ("the diagram", "shown above") OR when it is plainly this ask's
        # subject — 2021 HL Q7(b) asks about swings whose 45 cm arc and 90%
        # ratio are printed only in the Q7 stem, and requiring the ask to be
        # otherwise BARE kept that stem off every card under a lettered part.
        # Shared content words decide: the cuboid stays with "find the volume
        # of the cuboid" and stays off a logs equation.
        qstem_text = self.band_text([qstem], 4000) if qstem else ''
        want_qstem = force.get(
            'qstem',
            (not letter)
            or bool(NEEDS_QSTEM.search(' '.join(ctx) + ' ' + part_text))
            or (qstem is not None
                and self._shares_subject(' '.join(ctx) + ' ' + part_text,
                                         qstem_text)))
        if qstem and want_qstem:
            bands.insert(0, qstem)
        nxt = (scope[ri + 1] if ri + 1 < len(scope)
               else next((m for m in marks[li + 1:] if m[0] == 'letter'), None)
               if letter else None)
        bands.append(self._trim_next_setup((pos(scope[ri]), r_end), nxt))
        bands = self._hunt_definitions(bands, marks, li, qstem, part_text,
                                       force, q_end)
        return bands, 'roman part'

    # Words every exam question uses; they say nothing about WHICH question.
    GENERIC = frozenset("""
        find give show state write down using calculate work answer answers value
        values correct decimal place places form where hence otherwise also
        following first second third next same total number numbers point points
        line lines graph area volume length width height radius diagram table
        question part parts marks each other into from that this with your these
        those there their when what which will would could must have been they
        them then than terms term above below shown solution solutions method
        nearest units unit degrees exactly least greatest maximum minimum
        """.split())

    def _shares_subject(self, ask, stem):
        """Do the ask and the question stem talk about the same thing?

        Content words only: a shared "runway", "lake" or "cuboid" means the
        stem is this ask's setup; sharing nothing but exam furniture means it
        is a different question printed above.
        """
        def words(t):
            return {w for w in re.findall(r"[A-Za-z']{4,}", _ascii(t).lower())
                    if w not in self.GENERIC}
        return bool(words(ask) & words(stem))

    def _stem_is_real(self, band):
        """Does this band hold question-level setup, or a sibling's spill?"""
        (sp, sy), (ep, ey) = band
        for (pg, y0, y1, x0, txt, x1) in self.lines:
            if (sp, sy - 1) <= (pg, y0) < (ep, ey) and x0 <= 60.0 \
                    and not QHEAD.match(txt) and not LETTER.match(txt) \
                    and not ROMAN.match(txt) and len(txt) > 12:
                return True
        for page in range(sp, min(ep, self.doc.page_count - 1) + 1):
            lo = sy if page == sp else Y_TOP
            hi = ey if page == ep else Y_FOOT
            for r in self.ink(page):
                if r.y0 >= lo - 1 and r.y1 <= hi + 1 and (
                        r.width > 30 or r.height > 30):
                    return True
        return False

    def _hunt_definitions(self, bands, marks, li, qstem, part_text, force, q_end):
        """The ask names a function or quantity — h(x), T(t), V1 — that no
        included band defines. The definition is printed under an EARLIER
        letter ('h(x) = 0.001x^3 ...' set in part (a), differentiated in
        (b)), which the default plan deliberately skips. Hunt it down and
        carry the defining region along. Overrides may also force whole
        letters in with {"letters": ["a"]}."""

        def pos(m):
            return (m[2], m[3] - 4.0)

        # Whole letters forced by override.
        for want in force.get('letters', []):
            for i, m in enumerate(marks):
                if m[0] == 'letter' and m[1] == want:
                    end = next((pos(x) for x in marks[i + 1:]
                                if x[0] == 'letter'), q_end)
                    bands.insert(1 if qstem and bands and bands[0] == qstem
                                 else 0, (pos(m), end))
                    break
        included = _ascii(' '.join(self.band_text([b], 4000) for b in bands))
        syms = set(re.findall(r'\b([A-Za-z]\w{0,3})\s*[\u2032\u2019\']{0,2}\s*\(\s*[a-z]\s*\)', part_text))
        syms |= set(re.findall(r'\b([A-Z]\d)\b', part_text))
        missing = [sym for sym in syms
                   if not re.search(re.escape(sym)
                                    + r'\s*(?:\(\s*[a-z]\s*\))?\s*[=\u2248]',
                                    included)]
        bands = self._hunt_artwork(bands, marks, li, qstem, part_text, q_end)
        if not missing:
            return bands
        # Candidate defining regions, in print order: the question stem, then
        # every marker-to-marker segment before our letter.
        segs = ([qstem] if qstem and qstem not in bands else [])
        upto = marks[:li] if li is not None else marks
        for i, m in enumerate(upto):
            end = pos(marks[i + 1]) if i + 1 < len(marks) else q_end
            segs.append((pos(m), end))
        added = 0
        for sym in missing:
            for seg in segs:
                if seg in bands:
                    continue
                text = _ascii(self.band_text([seg], 4000))
                if re.search(re.escape(sym)
                             + r'\s*(?:\(\s*[a-z]\s*\))?\s*[=\u2248]', text):
                    bands.insert(1 if qstem and bands and bands[0] == qstem
                                 else 0, seg)
                    added += 1
                    break
            if added >= 2:
                break
        return bands

    def _hunt_artwork(self, bands, marks, li, qstem, part_text, q_end):
        """The ask points at printed artwork ("the graph above", "the diagram")
        that none of the included bands actually draws.

        The picture is usually printed under an EARLIER sibling — 2022 Higher
        Level Q7 sets its h(x) graph under part (c) and part (d) says "you may
        also use information from the graph above" — so the default plan, which
        skips earlier siblings, shipped the ask with nothing to read. Walk back
        through the earlier regions and carry the first one that holds ink.
        """
        if not NEEDS_QSTEM.search(part_text):
            return bands

        def pos(m):
            return (m[2], m[3] - 4.0)

        def has_ink(band):
            (sp, sy), (ep, ey) = band
            for page in range(sp, min(ep, self.doc.page_count - 1) + 1):
                lo = sy if page == sp else Y_TOP
                hi = ey if page == ep else Y_FOOT
                for r in self.ink(page):
                    if r.y0 >= lo - 1 and r.y1 <= hi + 1 and (
                            r.width > 30 or r.height > 30):
                        return True
            return False

        if any(has_ink(b) for b in bands):
            return bands
        # Earlier regions, nearest first: every marker segment before ours,
        # then the question stem.
        segs = []
        upto = marks[:li] if li is not None else marks
        for i, m in enumerate(upto):
            end = pos(marks[i + 1]) if i + 1 < len(marks) else q_end
            segs.append((pos(m), end))
        segs.reverse()
        if qstem:
            segs.append(qstem)
        for seg in segs:
            if seg in bands:
                continue
            if has_ink(seg):
                bands.insert(1 if qstem and bands and bands[0] == qstem else 0, seg)
                break
        return bands

    # ---- rendering ----

    def _content_windows(self, band):
        """The printed matter inside a band: per page, the y-window that holds
        its text and kept ink — nothing else ships. Ink that overflows the
        band's top (a diagram set beside the marker) extends the window."""
        (sp, sy), (ep, ey) = band
        windows = []
        for page in range(sp, min(ep, self.doc.page_count - 1) + 1):
            lo = sy if page == sp else Y_TOP
            hi = ey if page == ep else Y_FOOT
            if hi - lo < 3:
                continue
            tops, bots = [], []
            # Legacy booklets set a stacked fraction's numerator a few points
            # ABOVE the next part's marker (2020 HL P2 Q5(a)(ii)'s "11/12"),
            # so it straddles the band end. It belongs to the next row.
            straddle = set()
            if self.legacy and page == ep:
                straddle = {(y0, x0) for (pg, y0, y1, x0, txt, x1) in self.lines
                            if pg == page and hi - 16 < y0 < hi and y1 > hi + 0.5
                            and y0 > lo + 6 and (y0 + y1) / 2 > hi - 2.5}
            for (pg, y0, y1, x0, txt, x1) in self.lines:
                if pg == page and lo - 1 <= y0 < hi and \
                        not self.furniture_line(page, y0, y1, x0) and \
                        (y0, x0) not in straddle:
                    tops.append(y0)
                    bots.append(y1)
            if not tops:
                continue
            # Grow to a fixed point: ink intersecting the window pulls the
            # window over the whole drawing, which can reach a label (the S
            # atop a diagram's arrow) that then grows the window again.
            w_lo, w_hi = min(tops), max(bots)
            for _ in range(4):
                grew = False
                for r in self.ink(page):
                    # A drawing may overflow the band and pull the window with
                    # it — but only a drawing ANCHORED in the band: one that
                    # starts inside may finish below (a tall diagram), one that
                    # ends inside may begin above (the arrow over the marker).
                    # Ink that merely brushes the window otherwise belongs to a
                    # neighbouring part, and following it duplicated whole
                    # blocks into two sibling crops.
                    up = r.y1 > lo and r.y1 <= hi and r.y0 < w_lo - 0.5
                    down = r.y0 >= lo and r.y0 < hi and r.y1 > w_hi + 0.5
                    if up or down:
                        w_lo, w_hi = min(w_lo, r.y0), max(w_hi, r.y1)
                        grew = True
                for (pg, y0, y1, x0, txt, x1) in self.lines:
                    # Text joins only ABOVE the band (a diagram's topmost
                    # label); growing downward through text walks into the
                    # next part's print.
                    if pg == page and y0 < w_lo - 0.5 and y1 > w_lo - 14 and \
                            not self.furniture_line(page, y0, y1, x0):
                        # Legacy: an axis label of a graph that sits ABOVE the
                        # band (2020 OL P1 Q5(b)(ii)'s "-7") is that graph's,
                        # not this band's.
                        if self.legacy and any(
                                r.y0 < lo - 20 and r.x0 - 15 <= x0 <= r.x1 + 15
                                and r.y0 - 4 <= y0 <= r.y1 + 6
                                for r in self.ink(page)):
                            continue
                        # Legacy booklets set a part's rows 12-15pt apart, so
                        # the chain walked up through the PREVIOUS part's asks
                        # (2018 OL P2 Q7(a)'s (i)-(iii)). A row that carries a
                        # part marker is another part's ask, never a label.
                        if self.legacy and any(
                                l2[0] == page and abs(l2[1] - y0) < 1.5
                                and (LETTER.match(l2[4]) or ROMAN.match(l2[4]))
                                for l2 in self.lines):
                            continue
                        w_lo = y0
                        grew = True
                if not grew:
                    break
            bottom = min(self.foot.get(page, Y_FOOT), w_hi + 2)
            # Snap to whole lines. A boundary that lands inside a text row
            # shaves the glyph tops or bottoms, which reads as damage; the
            # audit fleet called it out 35 times. Push the edge just clear of
            # any line it would otherwise cut.
            for (pg, y0, y1, x0, txt, x1) in self.lines:
                if pg != page:
                    continue
                if y0 < w_lo - 2 < y1:
                    w_lo = y0 if (y1 - w_lo) > (w_lo - y0) else y1
                if y0 < bottom < y1:
                    # Snap to whichever edge keeps the crop honest: a row this
                    # band owns is taken whole, a row belonging to the NEXT
                    # part is cut above rather than sliced through its glyphs.
                    owns = (page, y0) < (ep, ey) and (y0, x0) not in straddle
                    bottom = y1 if owns else y0
            windows.append((page, max(Y_TOP, w_lo - 2), bottom))
        return windows

    def _mask_frames(self, img, page, top, bot, band_hi=None):
        """(see below) — `self._all_bands` is the whole plan, so a line this
        window shows but a LATER band owns is never erased."""
        """Paint the answer furniture white where the window could not avoid
        it. A window's EXTENT never follows a furniture frame, but a tall
        diagram beside one (the 2021 P2 sphere) can stretch the window across
        the frame's rows — so the frame is erased pixel-row by pixel-row,
        sparing the x-spans where kept ink or real text actually prints."""
        self.ink(page)
        frames = [f for f in self._furniture.get(page, [])
                  if f.y1 > top + 1 and f.y0 < bot - 1]
        frames += [pymupdf.Rect(b) for b, _ in self._boxes.get(page, [])
                   if b.y1 > top + 1 and b.y0 < bot - 1]
        # A neighbouring part's text row can sit under ink the band grew over
        # (the sphere's bottom arc crosses the "(ii)" line) — those rows are
        # erased the same way, sparing only the grown ink's own pixels.
        if band_hi is not None and not self._all_bands:
            # Only rows that sit CLEARLY below the band. A marker's y is nudged
            # 4pt up so its own row is not split, which put the boundary a hair
            # above legitimate rows: masking at band_hi erased the denominator
            # of a spliced fraction and half of "= 0 + ki, where k in Z",
            # leaving an unreadable card. The tolerance keeps the band's own
            # last line — including anything set alongside it — intact.
            frames += [pymupdf.Rect(X0, y0, X1, y1)
                       for (pg, y0, y1, x0, txt, x1) in self.lines
                       if pg == page and y0 >= band_hi + 7.0
                       and y1 > top + 1 and y0 < bot - 1]
        frames += [pymupdf.Rect(X0, y0, X1, y1)
                   for (pg, y0, y1, x0, txt, x1) in self.dead
                   if pg == page and y1 > top + 1 and y0 < bot - 1]
        # A window grows past its band to carry a diagram whole, and the text
        # it then shows may belong to another band of the SAME crop: 2021 HL
        # P2 Q5(a) grew over the sphere and masking ate two lines of the (i)
        # ask, leaving "Prove that the volume of the remaining space inside"
        # hanging. Mask a row only when no band in the plan owns it.
        foreign = []
        if self._all_bands:
            owned = []
            for (sp2, sy2), (ep2, ey2) in self._all_bands:
                for (pg, y0, y1, x0, txt, x1) in self.lines:
                    if pg == page and (sp2, sy2 - 1) <= (pg, y0) < (ep2, ey2):
                        owned.append((y0, y1))
            # A diagram's own labels ("Trail", "0·5 km", an axis name) belong
            # to no band — they sit beside the drawing, outside the part's
            # text — so masking unowned rows ate them, sparing only the few
            # pixels that happened to overlap the ink and printing "Trail" as
            # "ail". A row that a kept drawing reaches across is part of that
            # drawing.
            def labels_a_drawing(y0, y1, x0=None, x1=None):
                # Legacy booklets set a part's ask BESIDE the stem's picture
                # (2020 OL P1 Q8's "(a) Find the height..." runs alongside the
                # swimmer photo), so there a label must also sit near the
                # drawing horizontally, not merely share its rows.
                return any(r.y0 - 4 <= y1 and y0 <= r.y1 + 4
                           and (not self.legacy or x0 is None
                                or (x0 <= r.x1 + 25 and x1 >= r.x0 - 25))
                           for r in self.ink(page))
            foreign = [pymupdf.Rect(X0 if not self.legacy else x0 - 1, y0,
                                    X1 if not self.legacy else x1 + 1, y1)
                       for (pg, y0, y1, x0, txt, x1) in self.lines
                       if pg == page and y1 > top + 1 and y0 < bot - 1
                       and not any(abs(y0 - a) < 0.6 for a, _ in owned)
                       and not labels_a_drawing(y0, y1, x0, x1)]
            frames += foreign
        if not frames:
            return img
        keep = list(self.ink(page)) + self._rules.get(page, [])
        # A row's keep-span ends where the row ends. Running it to the page
        # edge spared every answer box printed beside a line of question text.
        keep += [pymupdf.Rect(x0, y0, x1, y1)
                 for (pg, y0, y1, x0, txt, x1) in self.lines
                 if pg == page and not self.furniture_line(page, y0, y1, x0)
                 and (band_hi is None or y0 < band_hi - 0.5)
                 and not (self.legacy and self._all_bands and any(
                     abs(f.y0 - y0) < 0.6 and abs(f.x0 - (x0 - 1)) < 0.6 for f in foreign))]
        w, h = img.size
        px = img.load()
        for f in frames:
            # 2.5pt of margin, not 1: a box's own border is drawn ON its
            # bounds, and erasing to the bound left the rule itself behind as
            # a hairline along the crop's edge.
            fy0 = max(0, _px(max(f.y0 - 2.5, top), top))
            fy1 = min(h, _px(min(f.y1 + 2.5, bot), top))
            fx0 = max(0, _px(f.x0 - 2.5, X0))
            fx1 = min(w, _px(f.x1 + 2.5, X0))
            for y in range(fy0, fy1):
                page_y = top + y / SCALE
                # BOTH ends clamp to the frame. Clamping only the right end
                # let a keep-rect starting beyond the frame set a paint target
                # past it: the answer box of 2021 OL P1 Q10(b) reached across
                # to the circle beside it and erased "Tr" from "Trail".
                # A dotted answer rule is a run of tiny marks. Sparing them
                # left a trail of specks across an otherwise erased box, so
                # ink under 4pt across is not content worth protecting.
                spans = [(min(fx1, max(fx0, _px(k.x0 - 1, X0))),
                          min(fx1, max(fx0, _px(k.x1 + 1, X0))))
                         for k in keep if k.y0 - 1 <= page_y <= k.y1 + 1
                         and (k.width >= 4 or k.height >= 4)]
                x = fx0
                for (kx0, kx1) in sorted(spans):
                    for xx in range(x, max(x, kx0)):
                        px[xx, y] = 255
                    x = max(x, kx1)
                for xx in range(x, fx1):
                    px[xx, y] = 255
        return img

    def _trim_next_setup(self, band, next_marker):
        """Drop a trailing paragraph that is really the NEXT part's setup.

        Maths prints a part's lead-in ABOVE its marker — "Bruno, Karen, and
        Martha start a training session..." sits over the "(f)" — so it falls
        inside the previous part's band and shipped as that part's context.
        The paper distinguishes the two by indent: a part's own text is set in
        from the margin (x >= 80) while question- and letter-level setup runs
        at the margin (x ~= 56.7). A run of margin-set lines immediately above
        the next marker introduces that marker, not the band it sits in.
        """
        if next_marker is None:
            return band
        (sp, sy), (ep, ey) = band
        inside = [l for l in self.lines
                  if (sp, sy - 1) <= (l[0], l[1]) < (ep, ey)]
        if len(inside) < 2:
            return band
        cut = None
        for l in reversed(inside):
            if self.legacy and (LETTER.match(l[4]) or ROMAN.match(l[4])):
                # Legacy booklets print a part's own marker a few points BELOW
                # the top of its ask line, so the marker can be the band's last
                # line; it is this part's own, not the next part's setup.
                break
            if l[3] <= 60.0:            # margin-set: setup prose
                cut = (l[0], l[1])
            elif l[3] >= 80.0:          # indented: this part's own text
                break
        # The cut is a PAGE and a y. Keeping only the y and pairing it with the
        # band's end page turned a trim into an extension whenever a band
        # spanned a page break, which is how 2021 HL Q3(a) came to carry the
        # whole of part (b).
        if cut is None or cut <= (sp, sy + 1):
            return band
        indented_before = any(l[3] >= 80.0 and (l[0], l[1]) < cut for l in inside)
        return ((sp, sy), cut) if indented_before else band

    def _stop_at_foreign_ask(self, page, top, bot, ):
        """Cut a window short at another part's QUESTION.

        A window grows to cover ink anchored in its band, and the growth is a
        contiguous y-range -- so a diagram that reaches down past the next part
        marker drags that part's question into the crop with it. The card then
        shows two asks and says nothing about which one it wants. 2021 OL
        Paper 1 Q9(a)(ii) shipped "(i) Draw the fourth pattern..." above its
        own ask for exactly that reason.

        Only ever cut where NO kept ink lies below the marker inside this
        window: if the diagram itself runs past it, the drawing is what the
        window is for and the marker line is the price of carrying it.
        """
        own = getattr(self, 'own_marks', set())
        best = None
        for (pg, y0, y1, x0, txt, x1) in self.lines:
            if pg != page or not (top < y0 < bot):
                continue
            t = txt.strip()
            mk = LETTER.match(t) or ROMAN.match(t)
            if not mk:
                continue
            names = {g.lower() for g in mk.groups() if g}
            if names and not (names & own):
                if best is None or y0 < best:
                    best = y0
        if best is None:
            return bot
        for r in self.ink(page):
            if r.y1 > best + 2 and r.y0 < bot and (r.width > 30 or r.height > 30):
                return bot
        return max(top, best - 3)

    def render(self, bands):
        self._all_bands = list(bands)
        pieces = []
        covered = {}
        for band in bands:
            (_, _), (ep_, ey) = band
            for (page, top, bot) in self._content_windows(band):
                # A window that overlaps what an earlier band already rendered
                # is trimmed to the remainder — two bands whose growth met in
                # the middle were printing the same block twice.
                for (ct, cb) in covered.get(page, []):
                    if top < cb and bot > ct:
                        if top >= ct - 1:
                            top = max(top, cb)
                        else:
                            bot = min(bot, ct)
                bot = self._stop_at_foreign_ask(page, top, bot)
                if bot - top < 4:
                    continue
                covered.setdefault(page, []).append((top, bot))
                clip = pymupdf.Rect(X0, top, X1 if not self.legacy else 588.0, bot)
                pix = self.doc[page].get_pixmap(clip=clip, dpi=DPI)
                img = Image.open(io.BytesIO(pix.tobytes('png'))).convert('L')
                band_hi = ey if page == ep_ else None
                img = self._mask_frames(img, page, top, bot, band_hi)
                img = trim_rows(img)
                if img is not None and self.legacy:
                    img = squeeze_blank_rows(img)
                if img is not None:
                    pieces.append(img)
        if not pieces:
            return None
        w = max(p.width for p in pieces)
        h = sum(p.height for p in pieces) + GAP * (len(pieces) - 1)
        out = Image.new('L', (w, h), 255)
        y = 0
        for p in pieces:
            out.paste(p, (0, y))
            y += p.height + GAP
        return out

    def render_regions(self, regions):
        """Render visually verified page rectangles without inferred masking.

        Override pages are one-based, matching the number printed in these
        SEC booklets. Each rectangle was inspected against the primary paper,
        so it deliberately excludes answer furniture and neighbouring parts.
        Narrow diagram rectangles are centred in the final vertical stitch.
        """
        pieces = []
        for region in regions:
            page = int(region['page']) - 1
            if page < 0 or page >= self.doc.page_count:
                raise ValueError(f'override page {page + 1} is outside {self.path}')
            x0 = float(region.get('x0', X0))
            x1 = float(region.get('x1', X1))
            top = float(region['top'])
            bottom = float(region['bottom'])
            if x1 <= x0 or bottom <= top:
                raise ValueError(f'invalid override region {region!r}')
            clip = pymupdf.Rect(x0, top, x1, bottom)
            pix = self.doc[page].get_pixmap(clip=clip, dpi=DPI)
            img = Image.open(io.BytesIO(pix.tobytes('png'))).convert('L')
            # An optional "erase" list paints answer furniture white inside a
            # region whose diagram and writing space share rows (the legacy
            # booklets set a grid beside a figure). Each entry is [x0, top,
            # x1, bottom] in page points, checked against the page.
            for ex0, etop, ex1, ebot in region.get('erase', []):
                img.paste(255, (max(0, _px(ex0, x0)), max(0, _px(etop, top)),
                                min(img.width, _px(ex1, x0)), min(img.height, _px(ebot, top))))
            img = trim_rows(img)
            if img is not None:
                pieces.append(img)
        if not pieces:
            return None
        width = max(piece.width for piece in pieces)
        height = sum(piece.height for piece in pieces) + GAP * (len(pieces) - 1)
        out = Image.new('L', (width, height), 255)
        y = 0
        for piece in pieces:
            out.paste(piece, ((width - piece.width) // 2, y))
            y += piece.height + GAP
        return out


ANON = object()


def _px(v, origin):
    return int(round((v - origin) * SCALE))


def squeeze_blank_rows(img, longest=110, keep=40):
    """Legacy booklets leave the answer space INSIDE a band (no frame marks
    it), so a crop carried tall white runs. Shorten any fully blank run longer
    than `longest` px to `keep` px; nothing printed is moved apart or cut."""
    w, h = img.size
    px = img.load()
    blank = [all(px[x, y] >= WHITE for x in range(0, w, 2)) for y in range(h)]
    rows, y = [], 0
    while y < h:
        if blank[y]:
            z = y
            while z < h and blank[z]:
                z += 1
            run = list(range(y, z))
            rows += run if len(run) <= longest else run[:keep // 2] + run[-(keep - keep // 2):]
            y = z
        else:
            rows.append(y)
            y += 1
    if len(rows) == h:
        return img
    out = Image.new(img.mode, (w, len(rows)), 255)
    for i, y in enumerate(rows):
        out.paste(img.crop((0, y, w, y + 1)), (0, i))
    return out


def trim_rows(img):
    """Strip blank paper rows above and below the printed matter."""
    px = img.load()
    w, h = img.size

    def blank(y):
        return all(px[x, y] >= WHITE for x in range(0, w, 2))

    top = 0
    while top < h and blank(top):
        top += 1
    if top >= h:
        return None
    bot = h - 1
    while bot > top and blank(bot):
        bot -= 1
    if bot - top < 6:
        return None
    return img.crop((0, max(0, top - PAD), w, min(h, bot + 1 + PAD)))


REF = re.compile(
    r'^(\d{4}) (HL|OL) Paper (\d) Q(\d{1,2})(?:\(([a-h])\))?(?:\(([ivx]{1,4})\))?')
# "Q1(a)(i), (ii)" — one scale marking two parts, so the crop must print both.
SPAN = re.compile(r'\(([ivx]{1,4})\)(?:\s*[,–-]\s*\(([ivx]{1,4})\))+')
LAST_ROMAN = re.compile(r'\(([ivx]{1,4})\)\s*$')


def fig_name(year, level, paper, qnum, letter, roman):
    parts = [f'maths-{year}-{level}-ask-p{paper}-q{qnum}']
    if letter:
        parts.append(letter)
    if roman:
        parts.append(roman)
    return '-'.join(parts)


def run(cards, write=True, probe=False, replace=False):
    sittings = {}
    overrides = json.load(open(OVERRIDES)) if os.path.exists(OVERRIDES) else {}
    sidecar = json.load(open(SIDECAR)) if os.path.exists(SIDECAR) else {}
    catalogue = json.load(open(CATALOGUE)) if os.path.exists(CATALOGUE) else []
    have = {c['file'] for c in catalogue}
    # Every crop already on disk or in the manifest, by content, so a second
    # card covering the same span reuses the published name.
    by_hash = {}
    if os.path.exists(MANIFEST_JSON):
        with open(MANIFEST_JSON) as fh:
            for key, rec in json.load(fh).items():
                if key.startswith('maths-') and '-ask-' in key:
                    by_hash[rec['md5']] = key
    fails = []
    for card in cards:
        m = REF.match(card['questionRef'])
        if not m:
            fails.append((card['id'], 'unparseable ref'))
            continue
        year, lvl = m.group(1), m.group(2).lower()
        paper, qnum = int(m.group(3)), int(m.group(4))
        letter, roman = m.group(5), m.group(6)
        key = (year, lvl, 100 if paper == 1 else 200)
        if key not in sittings:
            sittings[key] = Sitting(*key)
        S = sittings[key]
        force = overrides.get(card['id'], {})
        explicit_regions = force.get('regions')
        bands, note = S.plan(qnum, letter, roman, card.get('questionText', ''),
                             force)
        if explicit_regions:
            bands = [((int(region['page']) - 1, float(region['top'])),
                      (int(region['page']) - 1, float(region['bottom'])))
                     for region in explicit_regions]
            note = 'visually verified explicit regions'
        # A span citation answers several parts from one scale. The crop has to
        # show all of them, so the last band runs to whatever follows the LAST
        # roman named rather than stopping at the first.
        tail_m = LAST_ROMAN.search(card['questionRef'])
        last = tail_m.group(1) if tail_m else None
        if bands and last and last != roman:
            wide, _ = S.plan(qnum, letter, last, card.get('questionText', ''),
                             overrides.get(card['id']))
            if wide:
                bands = bands[:-1] + [(bands[-1][0], wide[-1][1])]
        if bands is None:
            fails.append((card['id'], note))
            continue
        name = fig_name(year, lvl.upper(), paper, qnum, letter, roman)
        if probe:
            print(f"{card['id']}: {note}")
            for b in bands:
                print(f'   p{b[0][0]} y{b[0][1]:.0f} -> p{b[1][0]} y{b[1][1]:.0f}')
        if f'{name}.png' in have and not probe and not replace:
            sidecar[card['id']] = name
            continue
        S.own_marks = {x.lower() for x in re.findall(
            r'\(([a-h]|i{1,3}|iv|vi{0,3})\)', card['questionRef'])}
        img = (S.render_regions(explicit_regions)
               if explicit_regions else S.render(bands))
        if img is None:
            fails.append((card['id'], 'nothing printed in the planned bands'))
            continue
        if probe:
            path = os.path.join(os.environ.get('PROBE_DIR', '/tmp'), f'{name}.png')
            img.save(path, optimize=True)
            print('   ->', path, img.size)
            continue
        d = os.path.join(OUT, f'{year}-{lvl}')
        os.makedirs(d, exist_ok=True)
        path = os.path.join(d, f'{name}.png')
        img.save(path, optimize=True)
        # Two cards whose spans cover the same region render the same pixels,
        # and the manifest refuses a second name for identical bytes — rightly,
        # since that is how a figure gets duplicated under two ids. Point the
        # card at the crop that already exists instead of publishing a twin.
        digest = hashlib.md5(open(path, 'rb').read()).hexdigest()
        twin = by_hash.get(digest)
        if twin and twin != name:
            os.remove(path)
            sidecar[card['id']] = twin
            continue
        by_hash[digest] = name
        sidecar[card['id']] = name
        catalogue_record = {
            'file': f'{name}.png',
            'kind': 'figure',
            'truncated': False,
            'questionRef': card['questionRef'],
            'description':
                'The question as printed on the paper — '
                f'{force.get("description") or (_legacy_description(card, S.region_text(explicit_regions) if explicit_regions else S.band_text(bands)) if S.legacy else S.band_text(bands))}',
        }
        existing = next((i for i, item in enumerate(catalogue)
                         if item['file'] == catalogue_record['file']), None)
        if existing is None:
            catalogue.append(catalogue_record)
        else:
            catalogue[existing] = catalogue_record
        have.add(f'{name}.png')
    if write and not probe:
        json.dump(sidecar, open(SIDECAR, 'w'), indent=1)
        json.dump(catalogue, open(CATALOGUE, 'w'), indent=1)
    return fails


def main():
    cards = json.load(open(AUTHORED))
    args = sys.argv[1:]
    if args and args[0] == '--probe':
        ref = args[1]
        subset = [c for c in cards if c['questionRef'].startswith(ref)][:1] or [
            {'id': 'probe', 'questionRef': ref, 'questionText': ''}]
        fails = run(subset, write=False, probe=True)
    elif args and args[0] == '--replace-card':
        card_id = args[1]
        subset = [c for c in cards if c['id'] == card_id]
        if not subset:
            print(f'unknown card id: {card_id}')
            sys.exit(1)
        fails = run(subset, replace=True)
        print(f'{len(subset) - len(fails)}/{len(subset)} replaced')
    elif args and args[0] == '--sitting':
        year, lvl = args[1], args[2].lower()
        subset = [c for c in cards
                  if c['questionRef'].startswith(f'{year} {lvl.upper()} ')]
        fails = run(subset)
        print(f'{len(subset) - len(fails)}/{len(subset)} planned')
    else:
        fails = run(cards)
        print(f'{len(cards) - len(fails)}/{len(cards)} planned')
    for cid, why in fails:
        print(f'  FAIL {cid}: {why}')
    sys.exit(1 if fails else 0)


if __name__ == '__main__':
    main()
