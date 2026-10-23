"""Lifting helpers for the 2026 Economics papers.

The 2026 schemes print every response as a bold heading, a dash and an
explanation. The headings are read from the PDF's own bold runs, so a menu is
split where the SEC split it, and every option is then SLICED from the scheme
markdown that the provenance gate reads. Question wording and stems are sliced
from the question paper's text layer. Nothing here types exam content.
"""
import re

import fitz

from econ_lib import _load, anyN, as_option, block, card, defurnish, load, tidy
from econ_glyphfill import fill

CORPUS = 'paper-trail-corpus'
LIGATURES = {'\u019f': 'ti', '\u0166': 'ti', '\u01a9': 'tt', '\ufb00': 'ff', '\ufb01': 'fi',
             '\ufb02': 'fl', '\ufb03': 'ffi', '\ufb04': 'ffl', '\ufb05': 'st', '\ufb06': 'st'}
TICK = re.compile(r'\(\s*[✓✔]?\s*\)')


def sheet(year, level, fileid):
    return Sheet(year, level, fileid)


class Sheet:
    def __init__(self, year, level, fileid):
        self.year, self.level = year, level
        self.lvl = 'hl' if level == 'higher' else 'ol'
        self.scheme_md = load(year, level)
        # The whole file, appended renderings included (table cells, columns,
        # fractions, filled glyphs): what the provenance gate compares against.
        self.full_md = _load(year, level)
        self.scheme_pdf = fitz.open(f'{CORPUS}/markingschemes/{year}/{fileid}.pdf')
        self.paper_pdf = fitz.open(f'{CORPUS}/exampapers/{year}/{fileid}.pdf')
        self._bold = {}

    # ── the paper ──────────────────────────────────────────────────────────
    def page_text(self, page):
        """One paper page as a single tidied line (the tick glyph repaired)."""
        raw = self.paper_pdf[page - 1].get_text(sort=True)
        text = tidy(raw.replace('', '✓').replace('', '•'))
        # The paper's font draws some letter pairs as one ligature glyph; read
        # them back as the letters (the same fold schemeText.mjs applies).
        for lig, letters in LIGATURES.items():
            text = text.replace(lig, letters)
        return text

    def ask(self, page, start, end=None, include_end=False):
        """The paper's own words from `start` up to (not including) `end`."""
        text = self.page_text(page)
        hits = [m.start() for m in re.finditer(re.escape(start), text)]
        if len(hits) != 1:
            raise ValueError(f'paper p{page}: {len(hits)} matches for {start!r}')
        a = hits[0]
        if end is None:
            return text[a:].strip()
        b = text.index(end, a + len(start))
        return text[a:b + (len(end) if include_end else 0)].strip()

    def clip(self, page, rect):
        """Text inside a rectangle of a paper page, read top to bottom."""
        return tidy(self.paper_pdf[page - 1].get_text('text', clip=fitz.Rect(*rect)))

    # ── the scheme ─────────────────────────────────────────────────────────
    def bold_heads(self, pages):
        """Every bold run that opens a response paragraph, in page order.

        A heading wrapped over two lines arrives as two bold line-starts; a
        line that was bold to its end is continued by the next bold start.
        """
        out = []
        for page in pages:
            if page in self._bold:
                out.extend(self._bold[page])
                continue
            heads, carry, prev = [], False, None
            for b in self.scheme_pdf[page - 1].get_text('dict')['blocks']:
                for line in b.get('lines', []):
                    spans = [s for s in line['spans'] if s['text'].strip()]
                    if not spans:
                        continue
                    lead = []
                    for s in spans:
                        if s['flags'] & 16 or 'Bold' in s['font']:
                            lead.append(s['text'])
                        else:
                            break
                    text = tidy(''.join(lead))
                    whole = len(lead) == len(spans)
                    box = line['bbox']
                    # A heading continues only onto the line directly beneath it.
                    below = prev is not None and 0 <= box[1] - prev[3] < 6 and abs(box[0] - prev[0]) < 30
                    if text and carry and heads and below:
                        heads[-1] = tidy(heads[-1] + ' ' + text)
                    elif text and len(text) >= 4 and spans[0]['bbox'][0] > 75:
                        heads.append(text)
                    carry = bool(text) and whole
                    prev = box
            self._bold[page] = heads
            out.extend(heads)
        return out

    def chunk(self, start, end, occ=None):
        return block(self.scheme_md, start, end, occ)

    def menu(self, start, end, pages, occ=None, drop=(), first=None, trim=None, full=False):
        """The response paragraphs between two scheme anchors.

        Split at the bold headings the PDF prints on `pages` that fall inside
        the chunk, in the order they appear. `first` names a heading the chunk
        must open with (a sanity check that nothing was skipped).
        """
        raw = block(self.full_md, start, end, occ) if full else self.chunk(start, end, occ)
        found = []
        pos = 0
        for h in self.bold_heads(pages):
            if any(d in h for d in drop):
                continue
            # A heading ending in a colon labels a list ("Private Benefits:",
            # "Agree:"); it is not itself a response.
            if h.rstrip().endswith(':'):
                continue
            # A response heading opens a line and is followed by its dash (or
            # a colon); a bold word inside a sentence ("price elastic demand",
            # "other businesses in the local economy") is neither.
            # Span joins can lose a space ("forfirms"), so any character may be
            # followed by whitespace. A one- or two-word heading must reach its
            # dash on the same line; longer ones may run on ("Physical demands
            # / safety risks / unpredictable weather –").
            body = r'\s*'.join(re.escape(ch) for ch in h if not ch.isspace())
            dash = ('' if h.rstrip().endswith(('–', '—', '-', ':'))
                    else r'[^\n]{0,80}?\s*[–—:-]' if len(h.split()) >= 3
                    else r'(?:\s*/[^\n]{0,80}?)?\s*[–—:-]')
            pat = re.compile(r'(?:^|\n)(?:\([a-c]\)\s*)?(?:\((?:i{1,3}|iv)\)\s*)?(' + body + r')' + dash)
            m = pat.search(raw, pos)
            if not m:
                continue
            found.append((h, m.start(1)))
            pos = m.end(1)
        if not found:
            raise ValueError(f'no bold headings between {start!r} and {end!r}')
        if first and not found[0][0].startswith(first):
            raise ValueError(f'menu opens with {found[0][0]!r}, expected {first!r}')
        opts = []
        for i, (h, at) in enumerate(found):
            stop = found[i + 1][1] if i + 1 < len(found) else len(raw)
            o = as_option(tidy(raw[at:stop]))
            if trim:
                o = o.split(trim)[0].strip()
            opts.append(fill(o, self.year, self.lvl))
        return opts

    def run(self, start, end, occ=None):
        """One contiguous scheme run from `start` up to (not including) `end`."""
        return fill(defurnish(self.chunk(start, end, occ)), self.year, self.lvl)


class Deck:
    """The card constructors one 2026 paper script uses, bound to its level."""

    def __init__(self, year, level):
        self.year, self.level = year, level
        self.lvl = 'HL' if level == 'higher' else 'OL'
        self.prefix = f'econ-{year}-{self.lvl.lower()}-'
        self.cards = []

    def add(self, cid, topic, concept, ref, qtext, notation, total, rows, *, kind='fixed',
            stem='', section='B', figure='', notes=''):
        c = card(self.prefix + cid, self.year, self.level, 'economics-' + topic, concept, ref,
                 qtext, notation, total, rows, notes, stem=stem, tariff_kind=kind,
                 section=section, figure_key=figure)
        self.cards.append(c)
        return c

    def pick(self, cid, topic, concept, ref, qtext, label, options, claim, per, note, *,
             stem='', section='B', figure='', notes=''):
        """An open menu: any `claim` of the scheme's responses at `per` each."""
        return self.add(cid, topic, concept, ref, qtext, f'{claim} @ {per}', claim * per,
                        [anyN('r-1', label, claim * per, claim, per, options, note)],
                        kind='bestNofParts', stem=stem, section=section, figure=figure,
                        notes=notes)

    @staticmethod
    def heading(rid, label, options, per, note):
        """One required heading: any one of its responses at `per`."""
        return anyN(rid, label, per, 1, per, options, note)

    def ref(self, q, parts='', route='', sa=False):
        r = f'{self.year} {self.lvl}{" Section A" if sa else ""} Q{q}{parts}'
        return f'{r} — {route}' if route else r

    def stance(self, prefix, choices, topic, concept, q, parts, qtext, per, *, sa=False,
               stem='', section='B'):
        """A printed either/or choice whose scheme credits each side: one card each."""
        for suffix, word, label, options in choices:
            self.pick(f'{prefix}-{suffix}', topic, concept, self.ref(q, parts, word, sa),
                      f'{qtext} Justify the choice: {word.upper()}.', label, options, 1, per,
                      f'One developed justification for the {word} position, {per} marks. The '
                      f'scheme credits both positions; these are its examples, not a closed list.',
                      stem=stem, section=section)


def show_before_reveal(card, key, full_question=None):
    """Bind a paper crop the student sees before the reveal.

    The session screen sets a card's `figure` beneath its typed stem and ask,
    but a `questionFigure` REPLACES both. So a crop of the data alone takes the
    figure slot. Only when that slot already holds the card's hidden solution
    does the card take a question crop, and that crop must then be the WHOLE
    printed question: stem, data and ask.
    """
    if not card.get('figureKey'):
        card['figureKey'] = key
    elif full_question:
        card['questionFigureKey'] = full_question
    else:
        raise ValueError(f"{card['id']}: figure slot holds {card['figureKey']}; "
                         'a printed-question crop is needed')
