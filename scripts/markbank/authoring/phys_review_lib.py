#!/usr/bin/env python3
"""Physics paper-by-paper review: the lifting and checking machinery.

Adapted from bio_review_lib.py (the Biology lane's, left untouched) for the
Physics papers and schemes, which differ from Biology's in three ways the
reader has to know about:

* The scheme prices an answer in a MARK CELL printed at the right margin on
  the answer's own baseline ("[3]", "[3 + 2]", "(3)", "6 or 3", "any two
  [4 + 4]"), set as a separate text object. The reader takes each cell off
  the line it shares a baseline with and records it beside that line
  (Src.cells), so a selection never carries a tariff and the runner can
  check every task's marks against the cells printed against its rows.
* Physics is written in powers and indices: "10" followed by a raised "-6"
  is ten to the minus six. A span the PDF sets raised and smaller is read as
  superscript characters, a lowered smaller one as subscript characters,
  when every character has a Unicode form ("2.5 x 10\u207b\u2076 m",
  "T\u00b2"); otherwise it is left as printed. A line holding a raised and a
  lowered span over the same x (a stacked fraction) is left as printed.
* Physics numbers its parts roman-major ("2. (iv) (a)") as well as
  letter-major ("14. (a) (iii)").

A reviewed sitting is written as a LEDGER (phys_review_<year>_<level>.py): one
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
import unicodedata
import json
import os
import re
import sys
from collections import Counter

import fitz  # PyMuPDF
from collections import defaultdict

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
_LEAD = re.compile(r'^(?:\s*(?:\([a-l]\)|\((?:i|ii|iii|iv|v|vi|vii|viii|ix|x|xi|xii)\)|\d{1,2}\.|[A-Z]:|\*))*\s*$')
# ...or a whole earlier SENTENCE on the same printed line: a selection may open
# at a sentence boundary ("...of the leaf.  To which tissue type...").
_AFTER_SENTENCE = re.compile(r'[.?!:]\s+$')
# What may follow a selection on its line: nothing, a new sentence, or the
# scheme's own tariff cell glued to the end of a menu ("... / pole Any three 3(1)").
_TARIFF_TAIL = re.compile(r'^\s*(?:Any\s+\w+\s*|\([Aa]ny\s+\w+\)\s*)?(?:\d+\(\d\)|\d\+\d|\d{1,2})?\s*$')

# A Physics mark cell, as the scheme prints it in its right-hand column:
# "[3]", "[3 + 2]", "[2 + 2 + 1 + 1 + 1]", "(3)", "(4+2)", "6", "6 or 3",
# "2 × 3", "3 + 6", and a menu's "any two [4 + 4]".
_NUM = r'\d{1,2}'
_SUM = rf'{_NUM}(?:\s*[+×x]\s*{_NUM})*'
# The menu's tally may sit before the bracket ("any two lines [4 + 3]") or
# inside it ("[any two 6 + 3]", "[any 3 x 3]"); 2025 Ordinary misprints one
# cell "[7)".
_ANY = r'(?:[Aa]ny|ANY)\s+(?:(?:one|two|three|four|five|six|ONE|TWO|THREE|FOUR|FIVE|SIX)\s+)?'
CELL = re.compile(rf'(?:{_ANY}(?:[a-z]+\s+)?)?'
                  rf'(?:\[\s*(?:{_ANY})?{_SUM}\s*[\])]|\(\s*{_SUM}\s*\)|{_NUM}(?:\s*(?:or|\+|×|x)\s*\(?{_NUM}\)?)*)')


def cell_value(text):
    """What a printed cell is worth in full: "[3 + 2]" 5, "any two [4 + 4]" 8,
    "6 or 3" 6 (the full mark; the second is the partial), "2 × 3" 6."""
    m = re.search(r'\[([^\]\)]*)[\])]', text)
    t = m.group(1) if m else text.strip()
    t = re.sub(rf'^\s*{_ANY}', '', t).strip('[]() ')
    t = re.split(r'\s+or\s+', t)[0].strip('() ')
    total = 0
    for term in re.split(r'\s*\+\s*', t):
        m = re.fullmatch(r'\(?(\d{1,2})\)?(?:\s*[×x]\s*\(?(\d{1,2})\)?)?', term.strip())
        if not m:
            raise ValueError(f'unreadable mark cell {text!r}')
        total += int(m.group(1)) * (int(m.group(2)) if m.group(2) else 1)
    return total


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
    # A character the scheme's font has no glyph for reaches the text layer as
    # NUL and prints as an empty box: 2015 Higher scheme p18 sets "'+' and
    # '\u25a1' (hyphae)" (rendered and looked at). It reads as the box printed.
    if o == 0:
        return '\u25a1'
    # The 2012 and 2013 schemes' Times New Roman and Arial subsets map the
    # single quotes, glyph ids 181 and 182, to U+201E and U+201F; every other
    # Biology scheme reads the same ids as U+2018 and U+2019, and the page
    # prints ‘ and ’ ("Dog’s", "‘occupation’": cropped and looked at). A font
    # artefact, not exam wording: read as the quotes printed. No other
    # Biology paper or scheme carries either character.
    if o in (0x201E, 0x201F) and font in ('Times#20New#20Roman', 'Arial'):
        return '\u2018' if o == 0x201E else '\u2019'
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


# The bank's table of characters a broken subset font left behind and what each
# stands for, derived from glyph ids across the corpus (derive_glyphs.py) and
# applied by the deck build to every string on a card. Physics reads it here,
# BEFORE a raised span is turned into superscripts, so "10" followed by a raised
# "ି18" (the equation font's broken minus) reads "10⁻¹⁸", not "10−18". "Ɵ" is
# left to _norm, which tells the theta from the "ti" ligature.
_GLYPHMAP = {k: v for k, v in json.load(open(os.path.join(HERE, 'glyphmap.json'), encoding='utf-8')).items()
             if k != '\u019f' and len(k) == 1}


def repair(text):
    """A string with the bank's broken-font characters read as what they stand for."""
    return ''.join(_GLYPHMAP.get(c, c) for c in text)


def _span_text(spans, i):
    """One span's text. The 2021 and 2022 booklets set the degree sign as a
    superscript letter o before the C ("4 oC" in the text layer); the page
    shows a degree sign, so that span reads "°". Nothing else is changed."""
    sp = spans[i]
    nxt = spans[i + 1]['text'] if i + 1 < len(spans) else ''
    if sp['flags'] & 1 and sp['text'].strip() == 'o' and nxt.lstrip().startswith('C'):
        return '°'
    return ''.join(_GLYPHMAP.get(c, c) for c in (_decode_symbol(c, sp['font']) for c in sp['text']))


SUP_MAP = dict(zip('0123456789+-–−=()ni', '⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁻⁻⁼⁽⁾ⁿⁱ'))
SUB_MAP = dict(zip('0123456789+-–−=()aeoxhklmnpst',
                   '₀₁₂₃₄₅₆₇₈₉₊₋₋₋₌₍₎'
                   'ₐₑₒₓₕₖₗₘₙₚₛₜ'))


def _script(text, table):
    """A raised or lowered span in Unicode super/subscript characters, or None
    when any printed character has no such form (it is then left as printed)."""
    core = text.strip()
    # A digit or letter set in the Mathematical Alphanumeric block (CambriaMath
    # "𝟐" for 2) is that digit: folded before its raised or lowered form is
    # chosen, so "d" with a raised "𝟐" reads "d²", not "d𝟐".
    core = ''.join(unicodedata.normalize('NFKD', c) if 0x1D400 <= ord(c) <= 0x1D7FF else c for c in core)
    if not core or any(c not in table for c in core):
        return None
    lead = text[:len(text) - len(text.lstrip())]
    tail = text[len(text.rstrip()):]
    return lead + ''.join(table[c] for c in core) + tail


def _line_text(ln):
    """One printed line's text: symbol glyphs decoded by their font, and a
    span set raised (superscript flag, or origin above the line's baseline) and
    smaller than the line's own type read as superscript, a lowered smaller one
    as subscript, unless the line stacks a raised and a lowered span over the
    same x (a fraction), which is left as printed."""
    spans = ln['spans']
    main = max(spans, key=lambda s: (s['size'], len(s['text'].strip())))
    base, size = main['origin'][1], main['size']
    kinds = []
    for s in spans:
        small = s['size'] < 0.85 * size and s['text'].strip()
        if small and (s['flags'] & 1 or s['origin'][1] < base - 0.8):
            kinds.append('sup')
        elif small and s['origin'][1] > base + 0.8:
            kinds.append('sub')
        else:
            kinds.append(None)
    sups = [s['bbox'] for s, k in zip(spans, kinds) if k == 'sup']
    subs = [s['bbox'] for s, k in zip(spans, kinds) if k == 'sub']
    stacked = any(a[0] < b[2] - 0.5 and b[0] < a[2] - 0.5 for a in sups for b in subs)
    out = []
    for i, (s, k) in enumerate(zip(spans, kinds)):
        t = _span_text(spans, i)
        if k and not stacked and t != '°':
            t = _script(t, SUP_MAP if k == 'sup' else SUB_MAP) or t
        out.append(t)
    return ''.join(out)




# Glyphs a subset font's ToUnicode map gets WRONG, set right by glyph id. The
# 2023 Higher scheme's CambriaMath maps glyph 2195 (m), 2203 (u) and 2204 (v)
# all to "m", and 2183 (a) to "k", so "F ∝ (mv − mu)/t" reads "F ∝ (mm − mm)/t".
# A ledger names each such glyph it has looked at on the rendered page:
# GLYPHS = {'CambriaMath': {2204: 'v', 2203: 'u', 2183: 'a'}}. The glyph's id is
# taken from the page's text trace at the glyph's own origin (the duplicate a
# maths font draws at the same origin with id -1 never overrides a real id).
def _page_dict(page, glyphs=None, clip=None):
    """page.get_text('dict') (optionally clipped), every span's text rebuilt from
    its characters: a maths font draws each glyph TWICE, the copy a zero-width
    character at the real one's advance or gathered at the line's end (2023
    Higher p13 "F ∝ (mv − mu)/t" reads "FF∝ (mmvm − mmum)/tt" otherwise), so a
    zero-width base character is dropped; and the ledger's glyph-id
    corrections apply."""
    gid_at = {}
    if glyphs:
        for sp in page.get_texttrace():
            for ch in sp['chars']:
                key = (sp['font'], round(ch[2][0], 1), round(ch[2][1], 1))
                if ch[1] >= 0 or key not in gid_at:
                    gid_at[key] = ch[1]
    raw = page.get_text('rawdict', clip=clip) if clip is not None else page.get_text('rawdict')
    for b in raw['blocks']:
        for ln in b.get('lines', []):
            for sp in ln['spans']:
                fix = next((m for f, m in (glyphs or {}).items() if f in sp['font']), None)
                out, prev, glyphs_at = [], None, []
                for ch in sp['chars']:
                    c = ch['c']
                    if (c.strip() and ch['bbox'][2] - ch['bbox'][0] < 0.05
                            and not unicodedata.combining(c) and 'Cambria' in sp['font']):
                        # A base glyph of no width prints nothing: the maths
                        # font's duplicate, set beside its glyph or gathered
                        # at the end of the line. Only the maths font does this:
                        # a text font's ligature hands back its second letter
                        # at zero width ("Certiﬁcate"), and combining marks (a
                        # recurring decimal's dot) are zero-width by nature.
                        sp['doubled'] = True
                        continue
                    prev = c
                    if fix:
                        gid = gid_at.get((sp['font'], round(ch['origin'][0], 1), round(ch['origin'][1], 1)))
                        c = fix.get(gid, c)
                    out.append(c)
                    glyphs_at.append((ch['bbox'][0], c))
                sp['text'] = ''.join(out)
                sp['glyphs'] = glyphs_at   # each kept glyph with its x, for equation_text
    return raw


def _page_rows(page, paper=False, total_x=None, glyphs=None):
    """The page's printed lines in the PDF's reading order, each as
    (text, cell): a mark cell printed on the same baseline as a line of text to
    its left is taken off as that line's cell; a cell with no text beside it
    stays a line of its own and is its own cell. A cell set inside the same
    text object as its line, after a wide gap, is taken off the same way."""
    raw = []
    for b in _page_dict(page, glyphs)['blocks']:
        for ln in b.get('lines', []):
            if not ln['spans']:
                continue
            spans = ln['spans']
            # A trailing cell inside the line object, after a wide gap.
            cut = None
            for j in range(len(spans) - 1, 0, -1):
                if spans[j]['bbox'][0] - spans[j - 1]['bbox'][2] > 30:
                    tail = ''.join(s['text'] for s in spans[j:]).strip()
                    if _CELL_ONLY.fullmatch(_norm(tail)):
                        cut = j
                    break
            if cut:
                head = dict(ln, spans=spans[:cut])
                dbl = any(sp.get('doubled') for sp in spans)
                headbox = [min(s['bbox'][0] for s in spans[:cut]), ln['bbox'][1],
                           max(s['bbox'][2] for s in spans[:cut]), ln['bbox'][3]]
                tailbox = [spans[cut]['bbox'][0], ln['bbox'][1], ln['bbox'][2], ln['bbox'][3]]
                raw.append([_line_text(head), headbox, spans[0]['origin'][1], dbl])
                raw.append([''.join(s['text'] for s in spans[cut:]), tailbox, spans[cut]['origin'][1], False])
            else:
                main = max(spans, key=lambda s: (s['size'], len(s['text'].strip())))
                raw.append([_line_text(ln), list(ln['bbox']), main['origin'][1],
                            any(sp.get('doubled') for sp in spans)])
    for r in raw:
        r[0] = _norm(r[0])
    raw = [r for r in raw if r[0]]
    width = page.rect.width
    # A scheme that prints a second marks column of PART totals at the far
    # right (2020 Higher: "With emission of radiation 3 6"): a bare number at
    # or right of total_x (the ledger's TOTAL_COLUMN_X, in points) is that
    # part's printed total, kept beside its line (Src.totals) and never read as
    # a cell, so the row's own cell is not mistaken for half a table row.
    totals = {}
    if total_x is not None:
        keep = []
        for r in raw:
            if re.fullmatch(r'\d{1,2}', r[0]) and r[1][0] >= total_x:
                partner = [q for q in raw if q is not r and abs(q[2] - r[2]) <= 2.5 and q[1][2] <= r[1][0] + 1
                           and not (re.fullmatch(r'\d{1,2}', q[0]) and q[1][0] >= total_x)
                           and not re.fullmatch(r'\d{1,2}', q[0])]
                if partner:
                    totals[id(max(partner, key=lambda q: q[1][2]))] = r[0]
                    continue
            keep.append(r)
        raw = keep
    bracketed = re.compile(r'(?:(?:[Aa]ny|ANY)\s+\w+\s+(?:[a-z]+\s+)?)?[\[(].*[\])]')

    def is_cell(r):
        if not _CELL_ONLY.fullmatch(r[0]):
            return False
        if bracketed.fullmatch(r[0]):
            return r[1][0] >= 0.55 * width
        # A bare number ("6", "6 or 3") is a cell only in the right-hand marks
        # column of a SCHEME; a paper prints its marks in brackets.
        return not paper and r[1][0] >= 0.8 * width
    cells = [i for i, r in enumerate(raw) if is_cell(r)]
    # A baseline holding several bare numbers is a table row ("n 2 1 0 1 2"),
    # not a marks column, which prints one cell per row.
    by_base = defaultdict(list)
    for i in cells:
        if not bracketed.fullmatch(raw[i][0]):
            by_base[round(raw[i][2])].append(i)
    table = {i for v in by_base.values() if len(v) > 1 for i in v}
    # ...and so is a bare number sharing its baseline with any other number.
    for i in cells:
        if not bracketed.fullmatch(raw[i][0]) and any(
                j != i and abs(r[2] - raw[i][2]) <= 2.5 and re.fullmatch(r'[\d.,\s–-]+', r[0])
                for j, r in enumerate(raw)):
            table.add(i)
    cells = [i for i in cells if i not in table]
    owner = {}
    for i in cells:
        x0, base = raw[i][1][0], raw[i][2]
        best = None
        for j, r in enumerate(raw):
            if j == i or j in cells:
                continue
            # The partner is a line of WORDS: a bare-number cell beside another
            # number is a table, not a marks column.
            if abs(r[2] - base) <= 2.5 and r[1][2] <= x0 + 1 and (
                    bracketed.fullmatch(raw[i][0]) or re.search(r'[A-Za-z]', r[0])):
                if best is None or r[1][2] > raw[best][1][2]:
                    best = j
        if best is not None:
            owner[i] = best
    out = []
    attached = defaultdict(list)
    for i, j in owner.items():
        attached[j].append(raw[i][0])
    for k, r in enumerate(raw):
        if k in owner:
            continue
        if k in cells:
            out.append((r[0], r[0], r[1], None, False))
        else:
            out.append((r[0], ' '.join(attached[k]) if attached.get(k) else None, r[1], totals.get(id(r)), r[3]))
    return out


def _page_lines(page, paper=False):
    """The page's printed lines with their cells taken off (see _page_rows)."""
    return [t for t, _, _, _, _ in _page_rows(page, paper)]


def _norm(line):
    # A "Ɵ" standing alone (no letter either side) is a THETA: 2017 Ordinary's
    # scheme sets "with its temperature Ɵ." in Calibri, 2025 Higher's
    # "Ɵ/°C = T/K – 273.15" in Times New Roman. Between letters the same code
    # point is Calibri's "ti" ligature ("invesƟgated"), which unligature restores.
    line = re.sub(r'(?<![A-Za-z])\u019f(?![A-Za-z])', '\u03b8', line)
    # CambriaMath sets every digit and letter of a formula as a Mathematical
    # Alphanumeric code point ("𝟕𝟑/𝟏𝟐𝟎𝟎", "𝑽𝒓𝒎𝒔"): the same characters in a
    # maths style. They are read as the plain characters they are -- a styled
    # "𝟎𝟎" is otherwise indistinguishable from the doubled-glyph font defect
    # the deck build refuses, and the provenance gate folds them the same way.
    line = ''.join(unicodedata.normalize('NFKD', c) if 0x1D400 <= ord(c) <= 0x1D7FF else c for c in line)
    line = unligature(line.replace(' ', ' ').replace(' ', ' '))
    return re.sub(r'\s+', ' ', line).strip()


from paper import STRIP_SET_PAGES, strip_set_lines  # noqa: E402
_STRIP_SET = {name: pages for (subject, _y, _l), files in STRIP_SET_PAGES.items() if subject == 'physics'
              for name, pages in files.items()}


class Src:
    """One SEC PDF read as printed lines, page by page (1-based pages)."""

    def __init__(self, path, label, total_x=None, glyphs=None):
        self.path, self.label = path, label
        self.glyphs = glyphs
        self.doc = fitz.open(path)
        self.sha = sha256(path)
        self.bytes = os.path.getsize(path)
        self.pages = self.doc.page_count
        self.lines = {}
        # page -> {line index: the mark cell printed on that line's baseline}
        self.cells = {}
        self.boxes = {}
        self.totals = {}
        self.doubled = {}
        strips = _STRIP_SET.get(os.path.basename(path), ())
        for i, page in enumerate(self.doc):
            if i + 1 in strips:
                # Text layer set in overlapping strips (paper.STRIP_SET_PAGES):
                # read the rebuilt lines.
                self.lines[i + 1] = [n for n in (_norm(t) for _, t in strip_set_lines(page)) if n]
                self.cells[i + 1] = {}
                self.boxes[i + 1] = []
                self.totals[i + 1] = {}
                self.doubled[i + 1] = set()
                continue
            rows = _page_rows(page, paper=label != 'scheme', total_x=total_x, glyphs=glyphs)
            self.lines[i + 1] = [t for t, _, _, _, _ in rows]
            self.cells[i + 1] = {k: c for k, (_, c, _, _, _) in enumerate(rows) if c}
            self.boxes[i + 1] = [b for _, _, b, _, _ in rows]
            self.totals[i + 1] = {k: t for k, (_, _, _, t, _) in enumerate(rows) if t}
            # Lines set in a maths font that draws each glyph twice: the copy is
            # dropped, but the same fonts mis-map digits ("94" can read "99"),
            # so the runner lifts such a line only once the ledger has checked it.
            self.doubled[i + 1] = {k for k, (_, _, _, _, d) in enumerate(rows) if d}

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
               skip_marks=False, wordbreak=False):
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
                            mid = [m for m in mid if not (re.fullmatch(r'\d{1,2}(?:\(\d\))?|\d,\d|\d\+\d', m)
                                                          or CELL.fullmatch(m))]
                        seg = [L[i][off:]] + mid + [L[j][:k + len(end)]]
                    if wordbreak:
                        a, b = (x.strip() for x in seg) if len(seg) == 2 else ('', '')
                        if not (a[-1:].isalpha() and b[:1].isalpha()):
                            raise LookupError(f'{self.label} p{page}: wordbreak needs two printed lines broken '
                                              f'between letters; got {seg!r}')
                        return a + b, {**meta, 'lines': [i, j]}
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


def M(marker, page, doc=None, br=False):
    """A printed part marker ("(ii)", "1.") placed before a lifted earlier ask
    in a stem, so the stem reads as the paper sets it. Checked to be a marker
    and to be printed on that page. `br` starts it on a new line, as a
    whole-part card sets each of its printed asks."""
    if not re.fullmatch(r'\((?:[a-l]|i|ii|iii|iv|v|vi|vii|viii|ix|x|xi|xii)\)|\d{1,2}\.', marker):
        raise ValueError(f'{marker!r} is not a part marker')
    return {'src': 'marker', 'text': marker, 'page': page, 'doc': doc, **({'br': True} if br else {})}


def SQ(page, start, end=None, after=None, nth=1, paired=None, bare=False, path=None, welded=False):
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
    question and letter, not by counting. `welded` (with `bare`) anchors a part
    whose marker opens its own answer's line ("(a) Protein"): the marker is the
    anchor and the rows are read from that line on."""
    return {'page': page, 'start': start, 'end': end, 'after': after, 'nth': nth,
            **({'paired': paired} if paired else {}), **({'bare': True} if bare else {}),
            **({'path': list(path)} if path else {}), **({'welded': True} if welded else {})}


def S(start, end=None, page=None, after=None, before=None, nth=1, skip_marks=False, piece=None, psep=None,
      wordbreak=False):
    """A slice of the SCHEME (page defaults to the task's scheme page, and the
    search starts after the task's own reprinted question). `skip_marks`
    leaves out a mark cell printed on its own line inside the answer. `piece`
    keeps one entry of a printed list cut at the scheme's own separator
    ("A = Larynx/ B = Trachea/ ..." piece 2 is "B = Trachea"); a list of
    pieces with a list of separators (`psep`) cuts again inside it. `wordbreak`
    joins a selection of exactly two printed lines with no space, for a word the
    scheme breaks across the lines of a narrow cell with no hyphen (2010 Higher
    p12 sets "1. Chlorophy" over "ll"): the break must fall between two letters."""
    return {'src': 'scheme', 'page': page, 'start': start, 'end': end,
            'after': after, 'before': before, 'nth': nth, **({'skip_marks': True} if skip_marks else {}),
            **({'piece': piece, 'psep': psep} if piece else {}), **({'wordbreak': True} if wordbreak else {})}


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
      item=None, id=None, tariff=None, cells=None):
    """One reviewed task -> one card, or, with `excluded` (the reason) and
    `evidence` (what the SEC documents print), a reviewed and priced task kept
    out of the bank on purpose and recorded as excluded.

    `route` names one option of a closed choose-one pool: the pool's cards are
    alternatives and its tariff counts once. `item` = (slug, label) names one
    separately priced entry of a printed list carded on its own: every item
    counts. `id` keeps a pre-existing card's id for the task it is corrected to.

    `tariff='questionTotal'` cards a whole printed part whose scheme prints its
    answers but no per-response tariff that the answers fit (2019 Ordinary
    Q13(c): 24 marks, no split): the task's total is the part's printed total,
    every row is unpriced (marks None), a menu is one row per printed option,
    and the student assesses the whole response against the printed total.
    No per-answer mark is ever derived."""
    return dict(key=key, ref=ref, sec=sec, q=q, rows=rows, topic=topic, concept=concept,
                sq=sq, total=total, stem=stem or [], fig=fig, qfig=qfig, labels=labels or [],
                source_pages=source_pages, route=route, notes=notes, decision=decision,
                paper_pages=paper_pages, scheme_pages=scheme_pages, leaf=leaf,
                excluded=excluded, evidence=evidence, id=id,
                item=item, tariff=tariff, **({'cells': cells} if cells else {}))


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


ROMAN = ['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x', 'xi', 'xii']
_R = r'(?:i|ii|iii|iv|v|vi|vii|viii|ix|x|xi|xii)'


# Questions whose first-level parts are LETTERS, declared by the ledger
# (LETTERED = {6, 14}) and set by the runner before it reads a ref. (i), (v) and
# (x) are both letters and romans: Section B's Q6 runs (a)-(l), so its ninth
# part is the letter (i), while (i) under a roman-major question is a roman.
LETTERED = set()


def parse_ref(ref):
    """A Physics task address -> (question, letter, roman, sub).

    Letter-major, as the paper prints Q6's (a)-(l) and the long questions'
    (a)-(d): 'Q14(a)(iii)' -> (14, 'a', 'iii', None); 'Q6(l)' -> (6, 'l', None,
    None); 'Q6(i)' -> (6, 'i', None, None) when Q6 is in LETTERED. Roman-major,
    as most Physics questions run: 'Q2(iv)' -> (2, None, 'iv', None), and a
    letter the paper prints INSIDE a roman is the sub-part: 'Q2(iv)(a)' ->
    (2, None, 'iv', 'a'). A letter-major ask may also have a lettered sub-part:
    'Q14(a)(iii)(b)'. The census keys a Physics leaf (question, letter, roman);
    `sub` never reaches it."""
    m = re.fullmatch(r'Q(\d+)((?:\([a-z]{1,4}\))*)', ref)
    if not m:
        raise ValueError(f'unparseable ref {ref!r}')
    q = int(m.group(1))
    toks = re.findall(r'\(([a-z]{1,4})\)', m.group(2))
    romans = set(ROMAN)
    letter = roman = sub = None
    if q in LETTERED:
        if toks:
            letter, toks = toks[0], toks[1:]
            if len(letter) != 1:
                raise ValueError(f'{ref!r}: Q{q} is lettered, {letter!r} is no letter')
        if toks and toks[0] in romans:
            roman, toks = toks[0], toks[1:]
    else:
        if toks and toks[0] in romans:
            roman, toks = toks[0], toks[1:]
        elif toks and len(toks[0]) == 1:
            letter, toks = toks[0], toks[1:]
            if toks and toks[0] in romans:
                roman, toks = toks[0], toks[1:]
    if toks and len(toks[0]) == 1 and roman:
        sub, toks = toks[0], toks[1:]
    if toks:
        raise ValueError(f'unparseable ref {ref!r}')
    return q, letter, roman, sub


def card_id(year, level, ref, route=None):
    q, letter, roman, sub = parse_ref(ref)
    parts = [f'phys-{year}-{level}-q{q}']
    parts += [p for p in (letter, roman, sub) if p]
    if route:
        parts.append(route)
    return '-'.join(parts)


UNPRINTED = 'The scheme prints no answer for this part.'


def unprinted(marks, note):
    """The one row of a card for a printed ask the scheme prints NO answer row
    for (Alex, 2026-10-28: every printed ask gets a card). It shows exactly
    UNPRINTED, at the marks the scheme's tariff or ladder gives the part, with
    the reviewer's `note` (what the scheme page prints instead) under it. The
    runner refuses it unless it is the task's only row and the task carries its
    page `evidence`."""
    if not note:
        raise ValueError('an unprinted row needs its note')
    return {'type': 'unprinted', 'marks': marks, 'note': note}


_CELL_ONLY = re.compile(CELL.pattern)


# ------------------------------------------------------------ fractions --
# A stacked fraction: the numerator's glyphs printed above a drawn bar, the
# denominator's below it, set smaller than the line around it. The text layer
# hands the three pieces back as separate lines ("C =" / "q" / "V"), and joined
# they read "C = q V" -- a different formula. fraction_text() reads each bar's
# numerator and denominator from where they are PRINTED and writes the fraction
# on one line with a solidus: "C = q/V". An operand of more than one symbol is
# bracketed ("1/(4πε)") so the line cannot be read any other way. Every glyph
# is the SEC's; the solidus and brackets only say what the bar said.
_ATOM = re.compile(r'^(?:\d+(?:\.\d+)?|[A-Za-z\u0370-\u03ff\U0001d400-\U0001d7ff][\u00b2\u00b3\u00b9\u2070-\u209f]*)$')


def _region_text(spans):
    """Spans of one region (left to right), super/subscripts read against the
    region's own largest type."""
    if not any(sp['text'].strip() for sp in spans):
        return ''
    spans = sorted(spans, key=lambda s: s['bbox'][0])
    out = _line_text({'spans': spans})
    return _norm(out)


def _wrap(text, den=False):
    t = text.strip()
    if _ATOM.match(t):
        return t
    if not den and not re.search(r'[\s+\-\u2013\u2212×]', t):
        return t
    return f'({t})'


def fraction_text(page, clip, glyphs=None):
    """The text inside `clip` with every stacked fraction written on one line."""
    clip = fitz.Rect(*clip)
    bars = [fitz.Rect(d['rect']) for d in page.get_drawings()
            if d['rect'].height < 1.6 and d['rect'].width > 3 and clip.contains(fitz.Rect(d['rect']))]
    bars.sort(key=lambda r: r.x0)
    spans = []
    for b in _page_dict(page, glyphs, clip)['blocks']:
        for ln in b.get('lines', []):
            for sp in ln['spans']:
                r = fitz.Rect(sp['bbox'])
                cx, cy = (r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2
                if not (clip.x0 <= cx <= clip.x1 and clip.y0 <= cy <= clip.y1):
                    continue
                spans.append(sp)
    # A root sign's overbar is drawn as a bar too (2025 Higher p21 "I₀/√2": a
    # bar over the "2" whose left end meets the "√"). It is no fraction: the
    # radicand stays where it is printed, under the root.
    roots = [b for b in bars if any(sp['text'].rstrip().endswith('\u221a')
                                    and abs(sp['bbox'][2] - b.x0) <= 2
                                    and sp['bbox'][1] - 1 <= b.y0 <= sp['bbox'][3] + 1 for sp in spans)]
    bars = [b for b in bars if b not in roots]
    if not bars:
        raise LookupError(f'no fraction bar inside {list(clip)}')
    owner = {}
    for i, sp in enumerate(spans):
        if not sp['text'].strip():
            continue          # a space belongs to the line around the fraction
        r = fitz.Rect(sp['bbox'])
        cx = (r.x0 + r.x1) / 2
        # The glyph's own extent, not its line's: a trailing space set at full
        # size widens a denominator's box past the bar.
        for j, bar in enumerate(bars):
            if bar.x0 - 1.5 <= cx <= bar.x1 + 1.5:
                gy = (r.y0 + r.y1) / 2
                owner[i] = (j, 'num' if gy < bar.y0 else 'den')
                break
    tokens = []   # (x, text)
    outside = [sp for i, sp in enumerate(spans) if i not in owner]
    # Outside text is grouped into runs separated by the bars.
    for j, bar in enumerate(bars):
        num = _region_text([sp for i, sp in enumerate(spans) if owner.get(i) == (j, 'num')])
        den = _region_text([sp for i, sp in enumerate(spans) if owner.get(i) == (j, 'den')])
        if not num or not den:
            raise LookupError(f'fraction bar {list(bar)} has numerator {num!r}, denominator {den!r}')
        tokens.append((bar.x0, f'{_wrap(num)}/{_wrap(den, den=True)}'))
    edges = [b.x0 for b in bars] + [1e9]
    lo = -1e9
    for k, hi in enumerate(edges):
        run = [sp for sp in outside if lo <= sp['bbox'][0] < hi]
        if run:
            tokens.append((run[0]['bbox'][0], _region_text(run)))
        lo = bars[k].x1 if k < len(bars) else hi
    tokens.sort()
    return _norm(' '.join(t for _, t in tokens))


# ------------------------------------------------------- nuclear equations --
# A nuclide's mass number is printed small ABOVE and its atomic number small
# BELOW, both to the LEFT of its symbol, as two separate text objects the text
# layer hands back out of order ("H + Li -> He + He", then "2 4 2 4 3 7 1 1").
# equation_text() puts each stack back in front of the symbol it stands at:
# "¹₁H + ⁷₃Li → ⁴₂He + ⁴₂He". A stack with no symbol close on its right is
# a postscript of the symbol before it (a charge, "β⁻"). Every glyph is the
# SEC's; the Unicode super/subscripts only say where it was printed.

def equation_text(page, clip, glyphs=None):
    clip = fitz.Rect(*clip)
    spans = []
    for b in _page_dict(page, glyphs, clip)['blocks']:
        for ln in b.get('lines', []):
            for sp in ln['spans']:
                r = fitz.Rect(sp['bbox'])
                cx, cy = (r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2
                if clip.x0 <= cx <= clip.x1 and clip.y0 <= cy <= clip.y1:
                    spans.append(sp)
    if not any(sp['text'].strip() for sp in spans):
        raise LookupError(f'nothing printed inside {list(clip)}')
    size = max(sp['size'] for sp in spans if sp['text'].strip())
    main = [sp for sp in spans if sp['size'] >= 0.85 * size]
    small = [sp for sp in spans if sp['size'] < 0.85 * size and sp['text'].strip()]
    mid = sorted((sp['bbox'][1] + sp['bbox'][3]) / 2 for sp in main if sp['text'].strip())
    cy = mid[len(mid) // 2]
    stacks = []
    for sp in sorted(small, key=lambda s: s['bbox'][0]):
        if stacks and sp['bbox'][0] < stacks[-1]['x1'] - 0.5:
            st = stacks[-1]
            st['spans'].append(sp)
            st['x1'] = max(st['x1'], sp['bbox'][2])
        else:
            stacks.append({'x0': sp['bbox'][0], 'x1': sp['bbox'][2], 'spans': [sp]})

    def script(st):
        up = [s for s in st['spans'] if (s['bbox'][1] + s['bbox'][3]) / 2 < cy]
        lo = [s for s in st['spans'] if (s['bbox'][1] + s['bbox'][3]) / 2 >= cy]
        txt = lambda ss: _norm(''.join(_span_text(sorted(ss, key=lambda s: s['bbox'][0]), i)
                                       for i in range(len(ss))))
        u, l = txt(up), txt(lo)
        return (_script(u, SUP_MAP) or u if u else '') + (_script(l, SUB_MAP) or l if l else '')
    # The main line read glyph by glyph, each at its own x: a nuclide's stack
    # is often printed INSIDE a span (" + He" holds He's 4/2), and placed by the
    # span's start it would land after the whole span.
    tokens = []
    for sp in main:
        for x, c in sp.get('glyphs') or [(sp['bbox'][0], sp['text'])]:
            tokens.append((x, _GLYPHMAP.get(_decode_symbol(c, sp['font']), _decode_symbol(c, sp['font'])), 'main'))
    glyphs = [t for t in tokens if t[1].strip()]
    for st in stacks:
        after = [t for t in glyphs if 0 <= t[0] - st['x1'] <= 3]
        x = st['x1'] - 0.01 if after else st['x0']
        tokens.append((x, script(st), 'script'))
    tokens.sort(key=lambda t: t[0])
    out = _norm(''.join(t for _, t, _ in tokens))
    # A span's leading space shares its x with the glyph after it and can sort
    # between a nuclide's stack and its symbol ("²³⁴₉₂ U"): a pre-script is
    # closed up to its symbol, and "+" and "→" are set with a space either side.
    out = re.sub(r'([\u00b2\u00b3\u00b9\u2070-\u209f]) +(?=[A-Za-z\u0370-\u03ff])', r'\1', out)
    out = re.sub(r'\s*([+→])\s*', r' \1 ', out)
    return _norm(out)
