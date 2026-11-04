"""Lifting helpers for the 2010-2020 (old-syllabus) Economics papers.

The old paper restarts Section B at Question 1, so every citation names its
section ("2019 HL Section B Q1(a)(i)") and every card id carries it ("-sa-",
"-sb-"). The schemes print their marks in a right-hand column, which the
extractor lifts into ⟨cells⟩; the word "graded" printed under a cell is NOT
lifted and can land in the middle of a sentence ("...the ability to price
graded set and not to price take."). The appended block-order rendering holds
those sentences whole, so a response that a marks word splits is sliced from
there (`bo`).

Nothing here types exam content. Every typed string is an ANCHOR: the text
returned is always a slice of the paper's text layer or of the scheme file the
provenance gate reads, and `traced` checks each slice against that file the way
the gate does before a card is written.
"""
import re

from econ_2026_lib import Deck, Sheet
from econ_lib import JUNK, as_option, defurnish, tidy

BLOCKS_MARK = '<!-- pdf-block-order: appended by append-scheme-blocks.py -->'
UNDERSCORES = re.compile(r'\s*_{2,}\s*')
TAIL = re.compile(r'(?:(?:\s+\d(?:st|nd|rd|th)\s*:\s*\d{1,2}\b)+|\s+(?:\d{1,2}\.|\((?:i{1,3}|iv|vi{0,3}|ix|x)\)|OR|or|graded|\+|&|(?:Q\s+)?Possible responses\s+Max(?:\s+Mark)?|Q\s+Possible responses(?:\s+\d{1,2})?)|\s*•)\s*$')
# The marks column's "graded" printed at the END of a line follows the slice
# rather than splitting it; cut there, the slice is still contiguous.
TRAILING_GRADED = re.compile(r'\s+(?:graded|&)\s*$')
# The 2019 HL scheme's text layer reports the "<" and ">" it prints (scheme p18,
# "PED <1", "PED > 1", drawn at full size by Calibri) as the modifier arrowheads
# U+02C2 and U+02C3, which the app's font sets as small raised marks a student
# can misread ("PED ˂1"). The page prints the signs, so the card shows them. The
# provenance gate's normalise() ignores both forms, so the slice still traces.
PRINTED_SIGNS = str.maketrans({'\u02c2': '<', '\u02c3': '>',
                               # The 2018 HL scheme's arrowhead sub-bullet (➢) is a private-use
                               # glyph the build's glyph map does not cover; set as the bullet it is.
                               '\uf0d8': '•'})


class Old(Sheet):
    """One old-syllabus paper and its scheme."""

    def __init__(self, year, level, fileid):
        super().__init__(year, level, fileid)
        body = self.full_md.split(BLOCKS_MARK, 1)
        self.block_md = body[1].split('<!-- markbank:', 1)[0] if len(body) > 1 else ''
        # One line, so an anchor matches across the rendering's line breaks.
        self.block_flat = tidy(self.block_md)
        cells = self.full_md.split('<!-- markbank:table-cells -->', 1)
        self.cell_flat = tidy(cells[1].split('<!-- /markbank:table-cells -->', 1)[0]) if len(cells) > 1 else ''
        self._comparable = self.comparable(self.full_md)

    @staticmethod
    def comparable(text):
        text = re.sub(r'⟨[^⟩]*⟩', ' ', text)
        text = re.sub(r'^##\s*Page\s*\d+\s*$', ' ', text, flags=re.M)
        text = re.sub(r'\d+\s*\|\s*P\s*a\s*g\s*e', ' ', text)
        return ' '.join(text.split())

    def traced(self, text):
        """The slice, refused unless the scheme file holds it contiguously.

        Also refused if it carries the marks column's "graded": that word is
        printed under a marks cell, never in a response, and a slice holding it
        has run across the column (slice it from the block order instead).
        """
        if re.search(r'\bgraded\b', text):
            raise ValueError(f'{self.year} {self.lvl}: slice carries the marks word "graded": {text[:90]!r}')
        if ' '.join(text.split()) not in self._comparable:
            raise ValueError(f'{self.year} {self.lvl}: not contiguous in the scheme file: {text[:90]!r}')
        return text.translate(PRINTED_SIGNS)

    # ── the paper ──────────────────────────────────────────────────────────
    def q(self, page, start, end=None, include_end=False):
        """The paper's words, with the ruled answer lines removed."""
        text = self.ask(page, start, end, include_end)
        return tidy(UNDERSCORES.sub(' ', text))

    # ── the scheme ─────────────────────────────────────────────────────────
    def opt(self, start, end, occ=None):
        """One response sliced from the primary rendering, marks cells removed.

        Where the marks column has split it ("graded" inside the slice), the
        same anchors slice it from the block order, which holds it whole.
        """
        text = TRAILING_GRADED.sub('', as_option(self.chunk(start, end, occ)))
        if not re.search(r'\bgraded\b', text):
            return self.traced(text)
        # The other renderings may not print the next part's marker where the
        # primary one does, so the end anchor is also tried without it.
        ends = dict.fromkeys([end.strip(), re.sub(r'^\([a-z]+\)\s*', '', end.strip())])
        for flat in (self.block_flat, self.cell_flat):
            for e in ends:
                try:
                    text = as_option(self._flat_raw(flat, start, e, occ))
                except ValueError:
                    continue
                if not re.search(r'\bgraded\b', text):
                    return self.traced(text)
        raise ValueError(f'every rendering splits {start!r} with the marks column')

    def bo(self, start, end, occ=None, include_end=False):
        """One response sliced from the block-order rendering (sentences whole)."""
        return self.traced(as_option(self._bo_raw(start, end, occ, include_end)))

    def cell(self, start, upto=None, whole=False, cells_only=False):
        """A whole table cell: the first line of the scheme file opening with `start`.

        `whole`: the line must BE `start` (a one-word cell such as "Land", which
        the primary rendering also opens a longer line with). `cells_only`: look
        only in the table-cell rendering, never in the primary one, whose lines
        interleave a two-column table ("Fairer distribution of Income
        Opportunity cost").
        """
        text = self.full_md
        if cells_only:
            text = text.split('<!-- markbank:table-cells -->', 1)[1].split('<!-- /markbank:table-cells -->', 1)[0]
        for line in text.splitlines():
            line = line.strip()
            if (line == start if whole else line.startswith(start)) and (upto is None or upto in line):
                if upto:
                    line = line[:line.index(upto) + len(upto)]
                return self.traced(tidy(line.replace('✓', '').replace('', '')))
        raise ValueError(f'no scheme line opens with {start!r}')

    def split(self, start, end, firsts, occ=None, source='auto'):
        """Responses printed as headed paragraphs, cut where each heading begins.

        From the primary rendering, unless the marks column runs through one of
        them ("graded" inside it, not merely after it), and then from the block
        order, which holds every paragraph whole. source='cells' slices the
        table-cell rendering instead.
        """
        if source in ('auto', 'primary'):
            opts = self._cut(tidy(defurnish(self.chunk(start, end, occ))), firsts, start)
            if source == 'primary' or not any(re.search(r'\bgraded\b', o) for o in opts):
                return [self.traced(o) for o in opts]
        if source == 'cells':
            # The table-cell rendering holds a response cell whole, clear of the
            # marks column's notes ("Two points in favour and two against"),
            # which both other renderings weave into the bullets beside them.
            opts = self._cut(tidy(defurnish(self._flat_raw(self.cell_flat, start, end.strip(), occ))), firsts, start)
            return [self.traced(o) for o in opts]
        opts = self._cut(tidy(defurnish(self._bo_raw(start, end.strip(), occ))), firsts, start)
        return [self.traced(o) for o in opts]

    @staticmethod
    def _cut(text, firsts, start):
        at, pos = [], 0
        for h in firsts:
            i = text.find(h, pos)
            if i < 0:
                raise ValueError(f'heading {h!r} not found after {pos} in {start!r}')
            at.append(i)
            pos = i + len(h)
        out = []
        for i, a in enumerate(at):
            b = at[i + 1] if i + 1 < len(at) else len(text)
            # The next item's own numeral or bullet is left at the end of this one.
            out.append(TAIL.sub('', as_option(text[a:b])).strip())
        return out

    def cut_cell(self, start, firsts):
        """One table cell that holds several headed responses, cut at each heading.

        The cell is the first line holding every heading, so a primary-rendering
        line that merely opens the same way is passed over.
        """
        line = next((ln.strip() for ln in self.full_md.splitlines()
                     if ln.strip().startswith(start) and all(h in ln for h in firsts)), None)
        if line is None:
            raise ValueError(f'no scheme line opens with {start!r} and holds every heading')
        line = self.traced(tidy(line))
        return [self.traced(o) for o in self._cut(line, firsts, start)]

    def bullets(self, start, end, occ=None):
        """The scheme's bullet-listed responses between two anchors, each traced.

        From the block order where the marks column runs through the list.
        """
        raw = self.chunk(start, end, occ)
        pieces = [TRAILING_GRADED.sub('', p) for p in re.split(r'\s*•\s*', defurnish(raw))]
        if any(re.search(r'\bgraded\b', p) for p in pieces):
            raw = self._bo_raw(start, end.strip(), occ).replace('\uf0b7', '•')
        out = []
        for x in re.split(r'\s*•\s*', tidy(defurnish(raw))):
            x = TAIL.sub('', as_option(x)).strip()
            if len(x) >= 12 and not JUNK.match(x):
                out.append(self.traced(x))
        return out

    def _bo_raw(self, start, end, occ=None, include_end=False):
        """A block-order slice. The block order may print a part marker apart
        from its text, so anchors are also tried without a leading marker."""
        bare = lambda a: re.sub(r'^\([a-z]+\)\s*', '', a.strip())
        last = None
        for s_ in dict.fromkeys([start, bare(start)]):
            for e_ in dict.fromkeys([end, bare(end)]):
                try:
                    return self._flat_raw(self.block_flat, s_, e_, occ, include_end)
                except ValueError as err:
                    last = err
        raise last

    @staticmethod
    def _flat_raw(flat, start, end, occ=None, include_end=False):
        hits = [m.start() for m in re.finditer(re.escape(start), flat)]
        if not hits or (len(hits) > 1 and occ is None):
            raise ValueError(f'{len(hits)} block-order matches for {start!r}')
        a = hits[occ or 0]
        b = flat.find(end, a + len(start))
        if b < 0:
            raise ValueError(f'end anchor {end!r} not found after {start!r}')
        return flat[a:b + (len(end) if include_end else 0)]


def beside_ask(card, key):
    """Bind the printed data (a diagram or table, never the whole question) that
    the student needs before the reveal, when the card's figure slot already
    holds its hidden solution. The typed stem and ask stay on the card
    (questionFigureIncludesPrompt false): a whole old-syllabus question set at
    phone width puts its text near 8 px, and the coordinator's rule (2026-11-04)
    is to crop to the part the ask needs wherever the text would fall under
    about 12 px on a 390 px phone."""
    if not card.get('figureKey'):
        raise ValueError(f"{card['id']}: no solution in the figure slot; bind the data as the figure")
    card['questionFigureKey'] = key
    card['questionFigureIncludesPrompt'] = False


class OldDeck(Deck):
    """Cards for one old-syllabus paper: citations and ids carry the section."""

    def ref(self, sec, q, parts='', route=''):
        r = f'{self.year} {self.lvl} Section {sec} Q{q}{parts}'
        return f'{r} — {route}' if route else r
