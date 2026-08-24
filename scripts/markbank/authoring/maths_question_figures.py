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
import io
import json
import os
import re
import sys
from collections import OrderedDict

import pymupdf
from PIL import Image

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
# crop: {"card-id": {"qstem": true|false, "siblings": true|false}}.
OVERRIDES = os.path.join(HERE, 'maths_qfig_overrides.json')

DPI = 170
X0, X1 = 40.0, 556.0        # the text column, with room for diagram overhang
Y_TOP, Y_FOOT = 46.0, 792.0  # running footer starts at y ~= 799.7 everywhere
GAP = 18                     # px between stitched regions
PAD = 8                      # px of white retained around each trimmed region
WHITE = 247                  # a row whose darkest pixel is >= this is paper

LETTER = re.compile(r'^\(\s*([a-h])\s*\)')
ROMAN = re.compile(r'^\(\s*([ivx]{1,4})\s*\)')
QHEAD = re.compile(r'^Question\s+(\d{1,2})$')
TAIL_PAGE = re.compile(r'^(Page for extra work|Acknowledg|Copyright|Blank Page)', re.I)
# "Hence", "your answer to part (i)": the ask leans on the siblings before it.
NEEDS_SIBLINGS = re.compile(
    r'\bHence\b|\byour answers?\b|\b(?:in|from|to) parts? \(', re.I)
# The part reaches OUTSIDE its letter, back to the question's own setup: it
# names the stem's diagram/graph/table or a point/segment the stem defined.
# "the equation" is deliberately absent — a part that says "solve the
# equation ..." is quoting itself, and matching it dragged an unrelated
# cuboid diagram onto a logs question.
NEEDS_QSTEM = re.compile(
    r'\b(?:the|this) (?:diagram|graph|table|figure|curve|map|pattern|data)\b'
    r'|\babove\b|\bshown\b|\[\s*[A-Z]{2}\s*\]|\bpoint [A-Z]\b', )


def lines_of(doc):
    """Every printed line: (page, y0, y1, x0, text), footer excluded."""
    out = []
    for n in range(doc.page_count):
        for b in doc[n].get_text('dict')['blocks']:
            for ln in b.get('lines', []):
                txt = ''.join(s['text'] for s in ln['spans']).strip()
                if not txt:
                    continue
                x0 = min(s['bbox'][0] for s in ln['spans'])
                y0 = min(s['bbox'][1] for s in ln['spans'])
                y1 = max(s['bbox'][3] for s in ln['spans'])
                if y0 >= Y_FOOT - 4:
                    continue
                out.append((n, y0, y1, x0, txt))
    out.sort(key=lambda l: (l[0], round(l[1], 1), l[3]))
    return out


def _dark(color):
    return color is not None and max(color) < 0.6


class Sitting:
    def __init__(self, year, level, component):
        self.year, self.level, self.component = year, level, component
        self.paper_no = 1 if component == 100 else 2
        path = os.path.join(PAPERS, f'{year}-{level}-{component}-paper.pdf')
        self.doc = pymupdf.open(path)
        self.lines = lines_of(self.doc)
        self._ink = {}
        self._furniture = {}
        self._index()

    # ---- geometry index ----

    def _index(self):
        self.tail = None
        for n in range(self.doc.page_count):
            first = next((l for l in self.lines if l[0] == n), None)
            if first and TAIL_PAGE.match(first[4]):
                self.tail = (n, 0.0)
                break
        self.q = OrderedDict()
        current = None
        for (page, y0, y1, x0, txt) in self.lines:
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
        for d in drawings:
            r = d['rect']
            if r.width > 420 and r.height > 80:
                inside = [l for l in text_lines
                          if r.y0 - 2 <= l[1] and l[2] <= r.y1 + 2]
                if len(inside) <= 3 and sum(len(l[4]) for l in inside) < 60:
                    frames.append(r)
        self._furniture[page] = frames
        rects = []
        for d in drawings:
            r = d['rect']
            if r.width < 2 and r.height < 2:
                continue
            if r.width > 420 and r.height < 4:
                continue               # a full-column rule: page furniture
            if any(f.y0 - 1 <= r.y0 and r.y1 <= f.y1 + 1 for f in frames):
                continue               # the frame, or a mark inside one
            rects.append(r)
        for info in p.get_images(full=True):
            for r in p.get_image_rects(info[0]):
                if r.width > 470 and r.height > 700:
                    continue           # page-covering watermark, not content
                if any(f.y0 - 1 <= r.y0 and r.y1 <= f.y1 + 1 for f in frames):
                    continue
                rects.append(r)
        self._ink[page] = rects
        return rects

    def furniture_line(self, page, y0, y1):
        """True when a text line sits inside an excluded answer frame — the
        "Show:" prompt must not hold a window open for its dead grid."""
        self.ink(page)
        return any(f.y0 - 2 <= y0 and y1 <= f.y1 + 2
                   for f in self._furniture.get(page, []))

    def _q_end(self, qnum):
        nums = list(self.q)
        i = nums.index(qnum)
        if i + 1 < len(nums):
            return self.q[nums[i + 1]]['head'][:2]
        return self.tail or (self.doc.page_count, 0.0)

    def band_text(self, bands, limit=220):
        words = []
        for (sp, sy), (ep, ey) in bands:
            for (page, y0, y1, x0, txt) in self.lines:
                if (sp, sy - 1) <= (page, y0) and (page, y0) < (ep, ey) and \
                        not self.furniture_line(page, y0, y1):
                    words.append(txt)
        flat = ' '.join(' '.join(words).split())
        return flat[:limit]

    # ---- the per-card plan ----

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

        li = next((i for i, m in enumerate(marks)
                   if m[0] == 'letter' and m[1] == letter), None)
        if letter and li is None:
            return None, f'({letter}) not found in Q{qnum}'

        if letter and not roman:
            # A letter part leans on the question's setup as a rule — "find
            # the volume of the cuboid" is unanswerable without the cuboid.
            l_end = next((pos(m) for m in marks[li + 1:] if m[0] == 'letter'), q_end)
            bands = ([qstem] if qstem and force.get('qstem', True) else [])
            bands.append((pos(marks[li]), l_end))
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
        if letter and first_roman and first_roman > pos(scope[0]):
            bands.append((pos(scope[0]), first_roman))   # the letter's setup
            ctx.append(self.band_text(bands[-1:], 2000))
        siblings = force.get('siblings',
                             bool(NEEDS_SIBLINGS.search(part_text))) and ri > 0
        if siblings:
            bands.append((first_roman, pos(scope[ri])))
            ctx.append(self.band_text(bands[-1:], 2000))
        # The question stem rides along only when the part actually reaches
        # for it — a printed cuboid above a self-contained logs equation is
        # noise, and noise is what this tool exists to remove.
        want_qstem = force.get(
            'qstem',
            (not letter) or bool(NEEDS_QSTEM.search(' '.join(ctx) + ' ' + part_text)))
        if qstem and want_qstem:
            bands.insert(0, qstem)
        bands.append((pos(scope[ri]), r_end))
        return bands, 'roman part'

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
            for (pg, y0, y1, x0, txt) in self.lines:
                if pg == page and lo - 1 <= y0 < hi and \
                        not self.furniture_line(page, y0, y1):
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
                    if r.y1 > w_lo + 1 and r.y0 < w_hi - 1 and (
                            r.y0 < w_lo - 0.5 or r.y1 > w_hi + 0.5):
                        w_lo, w_hi = min(w_lo, r.y0), max(w_hi, r.y1)
                        grew = True
                for (pg, y0, y1, x0, txt) in self.lines:
                    if pg == page and y1 > w_lo - 1 and y0 < w_hi + 1 and (
                            y0 < w_lo - 0.5 or y1 > w_hi + 0.5) and \
                            not self.furniture_line(page, y0, y1):
                        w_lo, w_hi = min(w_lo, y0), max(w_hi, y1)
                        grew = True
                if not grew:
                    break
            windows.append((page, max(Y_TOP, w_lo - 2), min(Y_FOOT, w_hi + 2)))
        return windows

    def render(self, bands):
        pieces = []
        for band in bands:
            for (page, top, bot) in self._content_windows(band):
                clip = pymupdf.Rect(X0, top, X1, bot)
                pix = self.doc[page].get_pixmap(clip=clip, dpi=DPI)
                img = Image.open(io.BytesIO(pix.tobytes('png'))).convert('L')
                img = trim_rows(img)
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


def fig_name(year, level, paper, qnum, letter, roman):
    parts = [f'maths-{year}-{level}-ask-p{paper}-q{qnum}']
    if letter:
        parts.append(letter)
    if roman:
        parts.append(roman)
    return '-'.join(parts)


def run(cards, write=True, probe=False):
    sittings = {}
    overrides = json.load(open(OVERRIDES)) if os.path.exists(OVERRIDES) else {}
    sidecar = json.load(open(SIDECAR)) if os.path.exists(SIDECAR) else {}
    catalogue = json.load(open(CATALOGUE)) if os.path.exists(CATALOGUE) else []
    have = {c['file'] for c in catalogue}
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
        bands, note = S.plan(qnum, letter, roman, card.get('questionText', ''),
                             overrides.get(card['id']))
        if bands is None:
            fails.append((card['id'], note))
            continue
        name = fig_name(year, lvl.upper(), paper, qnum, letter, roman)
        if probe:
            print(f"{card['id']}: {note}")
            for b in bands:
                print(f'   p{b[0][0]} y{b[0][1]:.0f} -> p{b[1][0]} y{b[1][1]:.0f}')
        if f'{name}.png' in have and not probe:
            sidecar[card['id']] = name
            continue
        img = S.render(bands)
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
        img.save(os.path.join(d, f'{name}.png'), optimize=True)
        sidecar[card['id']] = name
        catalogue.append({
            'file': f'{name}.png',
            'kind': 'figure',
            'truncated': False,
            'questionRef': card['questionRef'],
            'description':
                'The question as printed on the paper — '
                f'{S.band_text(bands)}',
        })
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
