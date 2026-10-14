#!/usr/bin/env python3
"""Biology paper-by-paper review: the lifting and checking machinery.

A reviewed sitting is written as a LEDGER (bio_review_<year>_<level>.py): one
entry per independently practicable task at the scheme's own mark boundary,
with the page it is printed on, the page its scheme prices it on, its tariff,
its topic and the reason for every non-obvious decision. This module turns a
ledger into Mark Bank cards and refuses, loudly, whenever the ledger and the
SEC documents disagree.

What it guarantees, and how:

* Every word a student reads as the SEC's is a SLICE of the SEC's own PDF.
  Selectors name where a slice starts and ends; the text between comes out of
  the PDF's text layer. A selector must open at the start of a printed line
  (after nothing but a part marker) and close at the end of one, so a
  selection is always whole printed cells and lines, never a fragment of one
  and never typed words checked afterwards (lift-never-write-exam-content).
* Paper and scheme are paired by WORDING, not by part labels: each task names
  the scheme's reprint of its question and the pairing must share most of its
  words with the paper's own ask.
* Tariffs are summed per task and per question against the printed totals,
  and the scheme's own tick-annotation checksum ("6 x 3 + 1 x 2") is matched
  against the mark units of the rows authored under it.
* Every census leaf the independent paper reader finds is claimed by at least
  one task, and every task resolves to a census leaf.
"""
import hashlib
import json
import os
import re
import sys
from collections import Counter

import fitz  # PyMuPDF

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))

from markbank_text import unligature  # noqa: E402

LEVEL_TOKEN = {'hl': 'HL', 'ol': 'OL'}
LEVEL_WORD = {'hl': 'higher', 'ol': 'ordinary'}

# What may stand in front of a selection on its printed line: part markers
# ("(b)", "(iii)", "2.") and the scheme's asterisk. Anything else in front means
# the selector cut into a sentence, which is refused.
_LEAD = re.compile(r'^(?:\s*(?:\([a-h]\)|\((?:i|ii|iii|iv|v|vi|vii|viii|ix|x)\)|\d{1,2}\.|[A-Z]:|\*))*\s*$')
# ...or a whole earlier SENTENCE on the same printed line: a selection may open
# at a sentence boundary ("...of the leaf.  To which tissue type...").
_AFTER_SENTENCE = re.compile(r'[.?!:]\s+$')
# What may follow a selection on its line: nothing, a new sentence, or the
# scheme's own tariff cell glued to the end of a menu ("... / pole Any three 3(1)").
_TARIFF_TAIL = re.compile(r'^\s*(?:Any\s+\w+\s*|\([Aa]ny\s+\w+\)\s*)?(?:\d+\(\d\)|\d\+\d|\d{1,2})?\s*$')


def _closes(text_after, end):
    if text_after.strip() == '':
        return True
    # A scheme note glued to the end of its row ("... other correct Must
    # match named organ 3") starts a new printed statement.
    if re.match(r'\s+Must match\b', text_after):
        return True
    if end[-1:] in '.?:' and text_after[:1].isspace():
        return True
    return bool(_TARIFF_TAIL.match(text_after))


def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as fh:
        for chunk in iter(lambda: fh.read(1 << 16), b''):
            h.update(chunk)
    return h.hexdigest()


# Symbol-font glyphs, decoded by the font they are set in. A PDF stores a
# Wingdings character at 0xF000 + its code, and the code means different things
# in different symbol fonts (0xF081 is a circled 1 in Wingdings and a bullet in
# another), so the font is read with the character. Wingdings numbers its
# circled digits 0x81-0x8A for 1-10; 0xFC is its check mark, as is Wingdings 2's
# 0x50 (the same mapping derive_glyphs.LIGATURE records for the bank).
def _decode_symbol(ch, font):
    o = ord(ch)
    if 'Wingdings' in font and 'Wingdings2' not in font.replace(' ', ''):
        if 0xF081 <= o <= 0xF08A:
            return chr(0x2460 + o - 0xF081)
        if o == 0xF0FC:
            return '\u2713'
    if 'Wingdings2' in font.replace(' ', '') and o == 0xF050:
        return '\u2713'
    # Wingdings 3 right arrows, each cropped out of the 2023 Higher scheme and
    # looked at: 0x67 in "ADP + P + Energy -> ATP + H2O" (derive_glyphs.py
    # maps it the same way) and 0x8E in "Ash -> Moth -> Robin".
    if 'Wingdings3' in font.replace(' ', '') and o in (0xF067, 0xF08E):
        return '\u2192'
    # The Symbol font's arrowright (0xAE), the arrow of the 2019 Higher
    # scheme's photosynthesis equation.
    if font.replace(' ', '').startswith('Symbol') and o == 0xF0AE:
        return '\u2192'
    return ch


def _span_text(spans, i):
    """One span's text. The 2021 and 2022 booklets set the degree sign as a
    superscript letter o before the C ("4 oC" in the text layer); the page
    shows a degree sign, so that span reads "°". Nothing else is changed."""
    sp = spans[i]
    nxt = spans[i + 1]['text'] if i + 1 < len(spans) else ''
    if sp['flags'] & 1 and sp['text'].strip() == 'o' and nxt.lstrip().startswith('C'):
        return '°'
    return ''.join(_decode_symbol(c, sp['font']) for c in sp['text'])


def _page_lines(page):
    """The page's printed lines, as page.get_text() returns them, with each
    symbol-font glyph decoded by its own font."""
    out = []
    for b in page.get_text('dict')['blocks']:
        for ln in b.get('lines', []):
            out.append(''.join(_span_text(ln['spans'], i) for i in range(len(ln['spans']))))
    return out


def _norm(line):
    line = unligature(line.replace(' ', ' ').replace(' ', ' '))
    return re.sub(r'\s+', ' ', line).strip()


class Src:
    """One SEC PDF read as printed lines, page by page (1-based pages)."""

    def __init__(self, path, label):
        self.path, self.label = path, label
        self.doc = fitz.open(path)
        self.sha = sha256(path)
        self.bytes = os.path.getsize(path)
        self.pages = self.doc.page_count
        self.lines = {}
        for i, page in enumerate(self.doc):
            self.lines[i + 1] = [n for n in (_norm(l) for l in _page_lines(page)) if n]

    def page_text(self, page):
        return ' '.join(self.lines[page])

    # ---- geometry: answers the scheme prints as a mark, not as words ------
    def find_box(self, page, text, clip=None):
        """Bounding boxes of `text` on the page (inside `clip` when given)."""
        pg = self.doc[page - 1]
        hits = [fitz.Rect(h) for h in pg.search_for(text)]
        return [h for h in hits if clip is None or self._inside(h, clip)]

    def find_exact(self, page, text, clip=None):
        """As find_box, but case-sensitive: the box must read exactly `text`
        (PyMuPDF's search ignores case, so "True" also finds "true or false")."""
        pg = self.doc[page - 1]
        # One hit comes back in pieces where its line changes font part-way
        # (the 2022 schemes set each "or" in bold): pieces that continue one
        # another on the same line are joined back into the one hit.
        hits = []
        for h in (fitz.Rect(r) for r in pg.search_for(text)):
            prev = hits[-1] if hits else None
            if (prev is not None and h.y0 < prev.y1 and h.y1 > prev.y0 and -2 < h.x0 - prev.x1 < 12
                    and (h.x0 - prev.x1 < 1
                         or not pg.get_textbox(fitz.Rect(prev.x1 + 0.5, prev.y0, h.x0 - 0.5, prev.y1)).strip())):
                hits[-1] = prev | h
            else:
                hits.append(h)
        # A large symbol glyph printed just under a header (an examiner's tick
        # under "True") can reach into the header's box; symbol-font glyphs
        # are not words, so they are left out of the comparison.
        return [b for b in hits if (clip is None or self._inside(b, clip))
                and _norm(re.sub('[\uf000-\uf0ff]', '', pg.get_textbox(b))) == text]

    # A glyph belongs to a clip when its CENTRE is inside it. PyMuPDF's own
    # clip keeps anything that merely touches the rectangle, so two adjacent
    # clips (one row of a table and the next) could both claim a glyph.
    @staticmethod
    def _inside(r, clip):
        cx, cy = (r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2
        return clip[0] <= cx <= clip[2] and clip[1] <= cy <= clip[3]

    def _chars(self, page, clip):
        pg = self.doc[page - 1]
        for b in pg.get_text('rawdict')['blocks']:
            for ln in b.get('lines', []):
                for sp in ln['spans']:
                    for ch in sp['chars']:
                        r = fitz.Rect(ch['bbox'])
                        if self._inside(r, clip):
                            yield r, ch['c'], sp['font']

    def answer_ticks(self, page, clip):
        """The examiner's answer ticks: the Wingdings check mark (U+F0FC), or
        the Wingdings 2 one (U+F050, its "P"), drawn at answer size. The same
        glyph printed small inside a question's own "(tick)" instruction is
        ignored by its height."""
        return [r for r, c, font in self._chars(page, clip)
                if (c in ('\uf0fc', '\u2713')
                    or (c == '\uf050' and 'Wingdings2' in font.replace(' ', '')))
                and r.height > 18]

    def wingdings_digits(self, page, clip):
        """Circled numbers set in Wingdings (U+F081 = 1 ... U+F08A = 10), with
        their boxes, decoded by the font's own encoding."""
        return [(r, ord(c) - 0xF080) for r, c, font in self._chars(page, clip)
                if 'Wingdings' in font and 0xF081 <= ord(c) <= 0xF08A]

    def words(self, page, clip):
        pg = self.doc[page - 1]
        return [(fitz.Rect(w[:4]), w[4]) for w in pg.get_text('words')
                if self._inside(fitz.Rect(w[:4]), clip)]

    def _line_of(self, page, anchor, lo, hi, what):
        L = self.lines[page]
        hits = [i for i in range(lo, hi) if anchor in L[i]]
        if not hits:
            raise LookupError(f'{self.label} p{page}: {what} {anchor!r} not found')
        return hits[0]

    def select(self, page, start, end=None, after=None, before=None, nth=1, lo=0, end_nth=1,
               skip_marks=False):
        """The printed text from `start` to `end` on one page.

        Returns (text, meta) where meta records the line span and whether the
        scheme's asterisk (exact term required) opened the selection.
        """
        if page not in self.lines:
            raise LookupError(f'{self.label}: no page {page}')
        L = self.lines[page]
        hi = len(L)
        if after:
            lo = self._line_of(page, after, lo, hi, 'after-anchor') + 1
        if before:
            hi = self._line_of(page, before, lo, hi, 'before-anchor')
        hits = []
        for i in range(lo, hi):
            off = L[i].find(start)
            while off >= 0:
                lead = L[i][:off]
                if _LEAD.match(lead) or _AFTER_SENTENCE.search(lead):
                    hits.append((i, off))
                    break
                off = L[i].find(start, off + 1)
        if len(hits) < nth:
            raise LookupError(f'{self.label} p{page}: start {start!r} does not open a printed '
                              f'line (after={after!r}, before={before!r}); found {len(hits)}')
        i, off = hits[nth - 1]
        starred = '*' in L[i][:off]
        meta = {'page': page, 'starred': starred}
        if end is None:
            # The whole rest of the line, short of a tariff cell glued to it.
            rest = L[i][off:]
            m = re.search(r'\s+(?:Any\s+\w+\s*)?(?:\d+\(\d\)|\d\+\d)\s*$', rest)
            if m:
                rest = rest[:m.start()]
            return rest.strip(), {**meta, 'lines': [i, i]}
        seen = 0
        for j in range(i, hi):
            base = off if j == i else 0
            k = L[j].find(end, base)
            while k >= 0:
                if _closes(L[j][k + len(end):], end) and (seen := seen + 1) == end_nth:
                    if j == i:
                        seg = [L[i][off:k + len(end)]]
                    else:
                        mid = L[i + 1:j]
                        if skip_marks:
                            # A mark cell the scheme prints between two lines
                            # of one answer ("... (the glomerulus" / "3" /
                            # "wall) or ...") is not part of the answer.
                            mid = [m for m in mid if not re.fullmatch(r'\d{1,2}(?:\(\d\))?|\d,\d|\d\+\d', m)]
                        seg = [L[i][off:]] + mid + [L[j][:k + len(end)]]
                    return join_lines(seg), {**meta, 'lines': [i, j]}
                k = L[j].find(end, k + 1)
        raise LookupError(f'{self.label} p{page}: end {end!r} closes no printed line after '
                          f'{start!r}')


def join_lines(segments):
    """Printed lines joined as the reader reads them: with a space, except
    where a word is broken over the line end by its own hyphen ("three-" /
    "base sequences" is the one word "three-base")."""
    out = ''
    for seg in (s.strip() for s in segments):
        if not seg:
            continue
        if out.endswith(('-', '\u2010')) and len(out) > 1 and out[-2].isalpha():
            out += seg
        else:
            out = f'{out} {seg}' if out else seg
    return out


# --------------------------------------------------------------- ledger API --
# The ledger is data. These constructors only record selectors; nothing is
# lifted until build() runs against the PDFs.

def Q(page, start, end=None, doc=None, after=None, before=None, nth=1, br=False, end_nth=1,
      piece=None, psep=None):
    """A slice of the QUESTION paper (doc defaults to the task's booklet).
    `br` starts it on a new line, as the paper sets printed options; `end_nth`
    closes on the nth printed close of `end` (a sentence ending the same way
    earlier in the ask). `piece`/`psep` keep one entry of a line the paper
    sets with several numbered asks side by side ("1. The initial decrease in
    mass   2. The subsequent increase in mass."), as S() does for the scheme."""
    return {'src': 'paper', 'doc': doc, 'page': page, 'start': start, 'end': end,
            'after': after, 'before': before, 'nth': nth, 'br': br,
            **({'end_nth': end_nth} if end_nth != 1 else {}),
            **({'piece': piece, 'psep': psep} if piece else {})}


def M(marker, page, doc=None):
    """A printed part marker ("(ii)", "1.") placed before a lifted earlier ask
    in a stem, so the stem reads as the paper sets it. Checked to be a marker
    and to be printed on that page."""
    if not re.fullmatch(r'\((?:[a-h]|i|ii|iii|iv|v|vi|vii|viii|ix|x)\)|\d\.', marker):
        raise ValueError(f'{marker!r} is not a part marker')
    return {'src': 'marker', 'text': marker, 'page': page, 'doc': doc}


def SQ(page, start, end=None, after=None, nth=1, paired=None, bare=False, path=None):
    """The scheme's reprint of the task's question: the pairing anchor.
    `paired` is the reviewer's reason for a pairing whose reprint rewords the
    paper's ask too far for the wording check (the scheme's "Put steps in
    correct order." for the paper's "Place each of the numbers ..."); it is
    recorded in the audit and still needs a quarter of the words shared.
    `bare` anchors a task whose scheme prints no reprint at all, only the
    part's own marker over its answer (the 2020 Higher true/false key's
    "(c)" over "T"): the anchor must be that marker alone, and `paired` must
    say why. `path` walks the scheme's own numbering down to the anchor: each
    entry is a printed line read exactly ("11", "(c)"), and the anchor is the
    first `start` after the last of them -- for a scheme that prints no
    reprints at all (2020 Ordinary) the part's marker is found under its own
    question and letter, not by counting."""
    return {'page': page, 'start': start, 'end': end, 'after': after, 'nth': nth,
            **({'paired': paired} if paired else {}), **({'bare': True} if bare else {}),
            **({'path': list(path)} if path else {})}


def S(start, end=None, page=None, after=None, before=None, nth=1, skip_marks=False, piece=None, psep=None):
    """A slice of the SCHEME (page defaults to the task's scheme page, and the
    search starts after the task's own reprinted question). `skip_marks`
    leaves out a mark cell printed on its own line inside the answer. `piece`
    keeps one entry of a printed list cut at the scheme's own separator
    ("A = Larynx/ B = Trachea/ ..." piece 2 is "B = Trachea"); a list of
    pieces with a list of separators (`psep`) cuts again inside it."""
    return {'src': 'scheme', 'page': page, 'start': start, 'end': end,
            'after': after, 'before': before, 'nth': nth, **({'skip_marks': True} if skip_marks else {}),
            **({'piece': piece, 'psep': psep} if piece else {})}


def pt(sel, marks, label=None, kind=None, note=None, units=None, first_alt=False,
       note_sel=None, note_lead=None, whole=False):
    """One marking row lifted whole from the scheme. `whole` keeps a printed
    "Word: ..." line as one answer instead of reading "Word" as its label."""
    return {'type': 'pt', 'sel': sel, 'marks': marks, 'label': label, 'kind': kind,
            'note': note, 'units': units or [marks], 'first_alt': first_alt,
            'note_sel': note_sel, 'note_lead': note_lead, 'whole': whole}


def anyn(sel, claim, per, steps=None, note=None, options=None, note_sel=None, open_list=False, sep=None):
    """A bounded menu: "Any two 2(3)". `sel` is the whole printed list, cut
    into options at the SEC's own solidus; or `options` is a list of
    selectors, one per option, for menus printed one per line. `open_list`
    marks a menu the scheme prints as examples ("e.g.")."""
    return {'type': 'anyn', 'sel': sel, 'claim': claim, 'per': per, 'steps': steps,
            'note': note, 'options': options, 'note_sel': note_sel, 'open_list': open_list, 'sep': sep}


def allof(parts, marks, note=None, note_sel=None):
    """One row for several answers printed on separate lines and priced
    together ("All three 3"): `parts` is a list of (label selector or None,
    answer selector)."""
    return {'type': 'allof', 'parts': parts, 'marks': marks, 'note': note, 'note_sel': note_sel}


def G(kind, page=None, clip=None, expect=None, **kw):
    """A row whose answer the scheme prints as a MARK rather than as words: a
    tick in a box, a circled number, letters in boxes. The value is read from
    the glyphs' positions on the scheme page; `expect` is the reviewer's own
    reading of the rendered page, and the two must agree."""
    return {'type': 'geo', 'kind': kind, 'page': page, 'clip': clip, 'expect': expect, **kw}


def T(key, ref, sec, q, rows, topic, concept, sq, total, stem=None, fig=None,
      qfig=None, labels=None, source_pages=None, route=None, notes='', decision='',
      paper_pages=None, scheme_pages=None, leaf=None, excluded=None, evidence=None,
      item=None, id=None):
    """One reviewed task -> one card, or, with `excluded` (the reason) and
    `evidence` (what the SEC documents print), a reviewed and priced task kept
    out of the bank on purpose and recorded as excluded.

    `route` names one option of a closed choose-one pool: the pool's cards are
    alternatives and its tariff counts once. `item` = (slug, label) names one
    separately priced entry of a printed list carded on its own: every item
    counts. `id` keeps a pre-existing card's id for the task it is corrected to."""
    return dict(key=key, ref=ref, sec=sec, q=q, rows=rows, topic=topic, concept=concept,
                sq=sq, total=total, stem=stem or [], fig=fig, qfig=qfig, labels=labels or [],
                source_pages=source_pages, route=route, notes=notes, decision=decision,
                paper_pages=paper_pages, scheme_pages=scheme_pages, leaf=leaf,
                excluded=excluded, evidence=evidence, id=id,
                item=item)


def L(letter, meaning_sel, asked):
    """One letter of a lettered figure, its meaning lifted from a document."""
    return {'letter': letter, 'sel': meaning_sel, 'asked': asked}


# ------------------------------------------------------------------ helpers --

WORD = re.compile(r"[a-z0-9]+")
STOP = set('the a an of to in and or is are be for this that which what how why does do '
           'on as by its it with from at your you named name state give'.split())


def _stem(w):
    """Fold a word's inflection ("labelling", "locations") so a scheme reprint
    that rewords the paper's own verbs still pairs with it. Applied to both
    sides, it can only raise a score."""
    return re.sub(r'(?:ling|ing|ed|es|s)$', '', w) if len(w) > 4 else w


def overlap(a, b):
    wa = [_stem(w) for w in WORD.findall(a.lower()) if w not in STOP]
    wb = set(_stem(w) for w in WORD.findall(b.lower()) if w not in STOP)
    if not wa:
        return 1.0
    return sum(1 for w in wa if w in wb) / len(wa)


def strip_star(text):
    return re.sub(r'\s*\*\s*', ' ', text).strip() if text.startswith('*') or ' *' in text \
        else text


def clean_option(text):
    return text.strip().strip('/').strip()


ROMAN = ['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii']


def parse_ref(ref):
    """'Q11(b)(iii)1' -> (11, 'b', 'iii', '1')."""
    m = re.fullmatch(r'Q(\d+)(?:\(([a-h])\))?(?:\(((?:i|ii|iii|iv|v|vi|vii|viii|ix|x))\))?(\d)?', ref)
    if not m:
        raise ValueError(f'unparseable ref {ref!r}')
    return int(m.group(1)), m.group(2), m.group(3), m.group(4)


def card_id(year, level, ref, route=None):
    q, letter, roman, item = parse_ref(ref)
    parts = [f'bio-{year}-{level}-q{q}']
    parts += [p for p in (letter, roman, item) if p]
    if route:
        parts.append(route)
    return '-'.join(parts)
