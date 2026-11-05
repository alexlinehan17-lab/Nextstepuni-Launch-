#!/usr/bin/env python3
"""Computer Science cards authored part by part from the page (lane of 5 Nov 2026).

    python3 scripts/markbank/authoring/compsci_lane.py sheet 2026 hl      # worksheet
    python3 scripts/markbank/authoring/compsci_lane.py lines 2026 hl 038 3 # page lines + boxes
    python3 scripts/markbank/authoring/compsci_lane.py crops 2026 hl       # render + publish crops
    python3 scripts/markbank/authoring/compsci_lane.py build 2026 hl       # merge cards into the JSON
    python3 scripts/markbank/authoring/compsci_lane.py build all           # every sitting module

The 336 Computer Science cards that shipped in August came out of an automatic
author (computer_science_all.py) that never reached main. This lane does not
regenerate them. It adds a card for every printed ask the bank does not yet
hold, one module per sitting in compsci_sittings/, and each module says, part
by part, what the page shows and how its card is built:

  * the QUESTION is lifted from the paper's own text layer, by a pair of
    selectors that must both be found on the named page -- the text between
    them is the SEC's, never typed here;
  * every marking point is lifted the same way from the scheme's .md (the very
    file build-deck's provenance gate reads), so a row that is not the scheme's
    own words cannot be written;
  * the tariff is the one the scheme prints, and the module names where: either
    cs_scheme.CsScheme reads it on the part's own row, or `printed=` quotes the
    scheme's tariff cell, which must be found on the scheme page;
  * printed matter the ask depends on (a program, a table, a figure) is a crop
    of the paper page, rendered here and opened before it is published; an
    answer the scheme gives as a drawing is a crop of the scheme page, shown
    only after the reveal (`solution`).

A module's card for an id the bank already ships is an error unless it says
`replaces=` with the reason: shipped ids key students' review history.
"""
import hashlib
import importlib
import json
import os
import re
import sys

import pymupdf

DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, DIR)
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(DIR)))
SUBJECT = 'computer-science'
PAPERS = os.path.join(ROOT, 'examiner-reports', SUBJECT, 'papers')
SCHEMES = os.path.join(ROOT, 'examiner-reports', SUBJECT, 'schemes')
AUTHORED = os.path.join(ROOT, 'scripts', 'markbank', 'authored', f'{SUBJECT}.json')
FIGURES = os.path.join(ROOT, 'components', 'MarkBank', 'figures.json')
FIG_DIR = os.path.join(ROOT, 'public', 'exam-figures', SUBJECT, 'markbank')
FIG_SRC = f'/exam-figures/{SUBJECT}/markbank'
SCALE = 2.5          # crop resolution: 180 dpi, the shipped crops' own
# Previews go outside the repository; set COMPSCI_PREVIEW to choose where.
PREVIEW = os.environ.get('COMPSCI_PREVIEW', '/private/tmp/compsci-preview')

TOPICS = {'cs-1-1', 'cs-1-2', 'cs-1-3', 'cs-2-1', 'cs-2-2', 'cs-2-3', 'cs-2-4',
          'cs-2-5', 'cs-3-1', 'cs-3-2', 'cs-3-3', 'cs-3-4'}
UNPRINTED_ANSWER = 'The scheme prints no answer for this part.'
LEVEL_WORD = {'hl': 'higher', 'ol': 'ordinary'}
ROMANS = ['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x']


class LaneError(SystemExit):
    pass


# Private-use glyphs the SEC's symbol fonts leave in the text layer, each read
# by rendering the glyph it draws. Only these are folded; anything else in the
# private-use area still reaches build-deck, which refuses it.
#   U+F0E0  Wingdings 0xE0, a right arrow: "1 -> 3 -> 4 -> 2", 2026 HL scheme
#           p14 (Q14(a)(ii)) and 2023 HL scheme p13 (Q13(b)(i)), both rendered
#           and looked at.
#   U+F0B7  Symbol 0xB7, a bullet: the papers' clue and rule lists (2025 HL
#           Q3, Q9); glyphmap.json already reads it as U+2022.
#   U+F0FC  Wingdings 0xFC, a tick, and U+F04A, Wingdings 0x4A, a smiling
#           face: 2022 OL paper p12 (Q13(b)(i)), rendered at 150 dpi and looked
#           at; folded to U+2713 and U+263A.
#   U+0D45, U+0D46  Cambria's equation operators, which its text layer files
#           under Malayalam code points: 2020 HL Section C p3 (the scoring
#           rules, "+5 points") and p6 (Q16(a)(viii)'s tables, "+2 points",
#           "-2 points", "sun -1"), rendered at 160-200 dpi and looked at; they
#           draw a plus and a minus sign, folded to U+002B and U+2212.
#   U+F0A7  Wingdings 0xA7, a small square bullet: 2020 HL Section C p6
#           (Q16(a)(vi)'s three cases), rendered at 200 dpi and looked at;
#           folded to U+2022 as glyphmap.json already reads it.
#   U+F02D  Symbol 0x2D, a dash bullet: 2020 HL Section C p7 (part (b)'s two
#           differences), rendered at 200 dpi and looked at; folded to a
#           hyphen as glyphmap.json already reads it.
#   U+123A, U+123B, U+0D4D  Cambria's maths brackets and not-equals sign,
#           filed under Ethiopic and Malayalam code points: 2021 HL paper p22
#           (Q14(b)(iv) "state (n, m), where n != m", (v) "(n, n, n)"),
#           rendered at 170 dpi and looked at; folded to '(', ')' and U+2260.
LANE_GLYPHS = {'\uf0e0': '\u2192', '\uf0b7': '\u2022', '\uf0fc': '\u2713', '\uf04a': '\u263a',
               '\u0d45': '+', '\u0d46': '\u2212', '\uf0a7': '\u2022', '\uf02d': '-',
               '\u123a': '(', '\u123b': ')', '\u0d4d': '\u2260'}


def fold(text):
    for k, v in LANE_GLYPHS.items():
        text = text.replace(k, v)
    return text


def ws(text):
    return ' '.join(str(text).split())


def norm(text):
    """build-deck's normalise(): lower case, letters and digits only."""
    t = str(text).lower()
    t = re.sub(r'[‐-―]', '-', t)
    return re.sub(r'[^a-z0-9Ā-ſЀ-ӿ]+', '', t)


# ── what a module writes ────────────────────────────────────────────────────
class Lift:
    """A slice of a printed page, from `start` to `end` inclusive.

    `doc` is '038' (Sections A & B), '040' (Section C) or 'scheme'. `page` is
    the one-based page of that document. Both selectors are matched against
    the page's whitespace-normalised text; `nth` picks the nth occurrence of
    `start` (1-based) where the same words are printed twice on the page.
    """
    def __init__(self, doc, page, start, end=None, nth=1, end_nth=1):
        self.doc, self.page, self.start, self.end, self.nth = doc, page, start, end, nth
        self.end_nth = end_nth

    def __repr__(self):
        return f'Lift({self.doc!r}, {self.page}, {self.start[:30]!r}, {str(self.end)[:30]!r})'


def P(page, start, end=None, nth=1, end_nth=1):
    """A slice of the Sections A & B booklet (-038-)."""
    return Lift('038', page, start, end, nth, end_nth)


def C(page, start, end=None, nth=1, end_nth=1):
    """A slice of the Section C booklet (-040-)."""
    return Lift('040', page, start, end, nth, end_nth)


def S(page, start, end=None, nth=1, end_nth=1):
    """A slice of the marking scheme, as its .md prints it."""
    return Lift('scheme', page, start, end, nth, end_nth)


def T(page, start, end=None, nth=1, end_nth=1):
    """A slice of one scheme page's TABLE CELLS, read column by column (see
    append_cells): a rubric grid the flat text reads across."""
    return Lift('cells', page, start, end, nth, end_nth)


def G(page, start, end=None, nth=1, end_nth=1):
    """A slice of one scheme line READ BY GLYPH ID (see append_glyphs): a line
    whose text layer misreads its maths digits."""
    return Lift('glyphs', page, start, end, nth, end_nth)


class At:
    """The text printed inside one rectangle of a page, read by position: a
    table cell holding a single character ("e", "R", "?") that no selector
    could pick out of the page's text unambiguously. `rect` is in PDF points,
    measured on the page and opened before use."""
    def __init__(self, doc, page, rect):
        self.doc, self.page, self.rect = doc, page, rect


class GAt(At):
    """The text printed inside one rectangle of a page, READ BY GLYPH ID
    (read_glyph_line): a question whose maths the text layer misreads -- 2024
    HL Q14(c)(ii) prints "O(n²)" and the text layer reads the exponent as an
    Oriya letter. `rect` is (x0, y0, x1, y1) in PDF points; a glyph belongs to
    it by its baseline origin. `breaks` sets each bulleted line on a line of
    its own (read_glyph_line), for a question whose list has sub-bullets."""
    def __init__(self, doc, page, rect, breaks=False):
        super().__init__(doc, page, rect)
        self.breaks = breaks


class FigurePointer:
    """Where in the scheme's figure a bare value is printed: "First gate in the
    figure." The one text on a card that is not lifted, so it carries no exam
    content -- no question, no answer, no gate name -- only a place in the
    figure, in words fixed here. Allowed in a row's note and nowhere else
    (coordinator, 5 Nov: 2021 OL Q15(b)(i)'s answers "1" and "0" sit beside
    the scheme's image of two gates, which prints no label for either)."""
    ORDINALS = ('First', 'Second', 'Third', 'Fourth')
    NOUNS = ('gate',)

    def __init__(self, n, noun):
        if not 1 <= n <= len(self.ORDINALS) or noun not in self.NOUNS:
            raise LaneError(f'FigurePointer({n}, {noun!r}): not a fixed pointer')
        self.text = f'{self.ORDINALS[n - 1]} {noun} in the figure.'


class Pair:
    """A menu option that names its heading: "Validation examples (x 2) — Range
    check: ...". Both halves are lifted; build-deck traces each half on its own,
    which is how a label beside its value is checked (a scheme heading over a
    list prints the two apart)."""
    def __init__(self, label, value):
        self.label, self.value = label, value


def pt(text, marks, note=None, route=None, head=None):
    return {'kind': 'point', 'text': text, 'marks': marks, 'note': note, 'route': route,
            'head': head}


def allof(text, marks, note=None):
    return {'kind': 'allOf', 'text': text, 'marks': marks, 'note': note}


def crit(text, marks, steps, note=None, head=None, route=None, parts=None):
    """A judgement the scheme prices on printed steps ("Very good ... 3 marks /
    Fair ... 2 marks"). `steps` are the printed marks below the top one."""
    return {'kind': 'criterion', 'text': text, 'marks': marks, 'steps': steps,
            'note': note, 'head': head, 'route': route, 'parts': parts}


def anyn(options, claim, each, head, note=None, open_list=False, steps=None, route=None,
         instruction=None):
    """A bounded choice: any `claim` of the scheme's `options`, `each` marks
    apiece (or `steps`, a descending ladder the scheme prints).

    `instruction` is a line the scheme prints among its answers that is not an
    answer -- "Accept any relevant analogue input" -- lifted into the note,
    never offered as an option (coordinator, 5 Nov). The list is then open."""
    return {'kind': 'anyN', 'options': options, 'claim': claim, 'each': each,
            'head': head, 'note': note, 'open': open_list or instruction is not None,
            'steps': steps, 'route': route, 'instruction': instruction}


def ladder(options, items, head=None, note=None, instruction=None, route=None):
    """A menu the scheme prices on a good/fair ladder: "Any one of the above
    points: Good description 2 marks / Fair description 1 mark".

    A priced answer is claimable (Alex's rule), and an anyN option is claimed
    whole, so the fair price could not be. This is a criterion instead: its
    text is the scheme's first option, `accepts` its other options -- the
    alternatives the scheme prints -- and the marks are the printed steps.
    `items` holds one ladder per answer the part asks for, each the printed
    values above zero: [[1, 2]] for any one at 2 or 1, [[1, 2], [1, 2]] for any
    two at 2 or 1 each; the row's steps are every total those answers can
    make. `head` and `instruction` (a line that is not an answer, "Any other
    valid reason") are lifted into the note before the scheme's ladder."""
    return {'kind': 'ladder', 'options': options, 'items': items, 'head': head,
            'note': note, 'instruction': instruction, 'route': route}


def ofpart(label, row):
    """Tie a row of a whole-question card to its printed part (coordinator,
    5 Nov: a short question with parts stays one card, but each row must show
    which part it answers). `label` is the part's printed label lifted from
    the paper, P(page, '(a)'): it heads the row's text (a point or criterion)
    or its note (a menu, whose header is not its text)."""
    row = dict(row)
    row['part'] = label
    return row


def ask_row(steps=None, note=None):
    """The scheme answers with a drawing and prints no words to claim.

    Where the scheme prices the drawing by its parts -- "Each correct pass 1
    mark" -- the check row is stepped at that price (coordinator, 5 Nov): a
    criterion whose steps are the printed per-part totals below the whole
    (`steps`, as crit's) and whose note is the printed price; the drawing
    stays the answer."""
    return {'kind': 'ask', 'steps': steps, 'note': note}


def unprinted(note):
    return {'kind': 'unprinted', 'note': note}


# ── the documents ───────────────────────────────────────────────────────────
class Sitting:
    def __init__(self, year, level):
        self.year, self.level = year, level
        self.docs = {}
        for comp in ('038', '040'):
            path = os.path.join(PAPERS, f'{year}-{level}-{comp}-paper.pdf')
            if os.path.exists(path):
                self.docs[comp] = pymupdf.open(path)
        spath = os.path.join(SCHEMES, f'{year}-{level}.pdf')
        self.docs['scheme'] = pymupdf.open(spath) if os.path.exists(spath) else None
        md = open(os.path.join(SCHEMES, f'{year}-{level}.md'), encoding='utf8').read()
        self.md = md
        flat = re.split(f'{re.escape(CELLS_START)}|{re.escape(GLYPHS_START)}', md)[0]
        self.md_pages = {}
        for m in re.finditer(r'^## Page (\d+)\n(.*?)(?=^## Page \d+\n|\Z)', flat, re.S | re.M):
            self.md_pages[int(m.group(1))] = ws(fold(m.group(2)))
        self.cell_pages = {}
        for m in re.finditer(r'<!-- compsci:cells page (\d+) -->\n(.*?)(?=<!-- compsci:cells|\Z)',
                             md, re.S):
            self.cell_pages[int(m.group(1))] = ws(fold(m.group(2).split(CELLS_END)[0]))
        self.glyph_pages = {}
        for m in re.finditer(r'<!-- compsci:glyphs page (\d+) -->\n(.*?)(?=<!-- compsci:glyphs|<!-- /compsci:glyphs|\Z)',
                             md, re.S):
            self.glyph_pages[int(m.group(1))] = ws(m.group(2))
        self.md_norm = comparable(md)
        self._page_text = {}

    def text(self, doc, page):
        key = (doc, page)
        if key not in self._page_text:
            if doc == 'scheme':
                if page not in self.md_pages:
                    raise LaneError(f'{self.year} {self.level}: scheme .md has no page {page}')
                self._page_text[key] = self.md_pages[page]
            elif doc == 'glyphs':
                if page not in self.glyph_pages:
                    raise LaneError(f'{self.year} {self.level}: no glyph-id line read for scheme '
                                    f'page {page}; run glyphs')
                self._page_text[key] = self.glyph_pages[page]
            elif doc == 'cells':
                if page not in self.cell_pages:
                    raise LaneError(f'{self.year} {self.level}: no cells read for scheme page '
                                    f'{page}; run cells')
                self._page_text[key] = self.cell_pages[page]
            else:
                d = self.docs.get(doc)
                if d is None:
                    raise LaneError(f'{self.year} {self.level}: no {doc} booklet on disk')
                self._page_text[key] = ws(fold(d[page - 1].get_text()))
        return self._page_text[key]

    def lift(self, item, note=False):
        """Resolve a Lift, a list of Lifts (joined by a space), or None. A
        FigurePointer resolves only in a note."""
        if item is None:
            return None
        if isinstance(item, (list, tuple)):
            return ' '.join(self.lift(i, note) for i in item)
        if isinstance(item, FigurePointer):
            if not note:
                raise LaneError(f'{self.year} {self.level}: a figure pointer belongs in a note')
            return item.text
        if isinstance(item, Pair):
            return f'{self.lift(item.label)} — {self.lift(item.value)}'
        if isinstance(item, GAt):
            x0, y0, x1, y1 = item.rect
            return read_glyph_line(self.docs[item.doc][item.page - 1], y0, y1, x0, x1,
                                   breaks=item.breaks)
        if isinstance(item, At):
            d = self.docs[item.doc]
            out = ws(d[item.page - 1].get_textbox(pymupdf.Rect(*item.rect)))
            if not out:
                raise LaneError(f'{self.year} {self.level} At{item.rect}: nothing printed there')
            return out
        if not isinstance(item, Lift):
            raise LaneError(f'{item!r}: every printed word on a card is lifted (P/C/S), '
                            f'never typed')
        t = self.text(item.doc, item.page)
        start = ws(item.start)
        pos, i = -1, 0
        for _ in range(item.nth):
            pos = t.find(start, i)
            if pos < 0:
                break
            i = pos + 1
        if pos < 0:
            raise LaneError(f'{self.year} {self.level} {item}: start not found on page')
        if item.end is None:
            out = t[pos:pos + len(start)]
        else:
            end = ws(item.end)
            j = t.find(end, pos)
            # the end must close the slice AFTER the start begins
            while j >= 0 and j + len(end) < pos + len(start):
                j = t.find(end, j + 1)
            for _ in range(item.end_nth - 1):
                if j >= 0:
                    j = t.find(end, j + 1)
            if j < 0:
                raise LaneError(f'{self.year} {self.level} {item}: end not found after start')
            out = t[pos:j + len(end)]
        if len(out) > 4000:
            raise LaneError(f'{self.year} {self.level} {item}: slice of {len(out)} chars -- '
                            f'selectors too far apart')
        return out


CELLS_START = '<!-- compsci:cells -->'
CELLS_END = '<!-- /compsci:cells -->'


def append_cells(year, level, pages):
    """Append the table cells of the named scheme pages to the scheme .md.

    A rubric grid -- 2026 HL Q16(b)'s four criteria at three levels -- reads
    ACROSS the page in the flat extraction, so one criterion's items arrive
    interleaved with the other levels' and no card can quote them. find_tables()
    reads the cells whole; they are written COLUMN by column, top to bottom,
    so a criterion's own cells sit together. Append-only, the safety argument
    of append-scheme-tables.py: comparableScheme() joins every line, so a claim
    that traces now still traces after. Only the pages named are read --
    find_tables() over a page of prose returns word fragments, and those are
    not appended anywhere. Re-running replaces the block.
    """
    path = os.path.join(SCHEMES, f'{year}-{level}.md')
    flat, _, glyphs = _blocks(open(path, encoding='utf8').read())
    md = flat
    doc = pymupdf.open(os.path.join(SCHEMES, f'{year}-{level}.pdf'))
    out = [CELLS_START]
    for page in pages:
        out.append(f'<!-- compsci:cells page {page} -->')
        for table in doc[page - 1].find_tables().tables:
            grid = table.extract()
            width = max(len(r) for r in grid)
            for col in range(width):
                for row in grid:
                    cell = ws(row[col] or '') if col < len(row) else ''
                    if cell:
                        out.append(cell)
    out.append(CELLS_END)
    with open(path, 'w', encoding='utf8') as fh:
        fh.write(md + '\n'.join(out) + '\n' + glyphs)
    return len(out)


GLYPHS_START = '<!-- compsci:glyphs -->'
GLYPHS_END = '<!-- /compsci:glyphs -->'


def _blocks(md):
    """The scheme .md as (flat extraction, cells block, glyph block), each
    block ending in a newline, or '' where absent."""
    def take(text, start, end):
        if start not in text:
            return text, ''
        head, rest = text.split(start, 1)
        body, tail = rest.split(end, 1)
        return head + tail.lstrip('\n'), start + body + end + '\n'
    md, glyphs = take(md, GLYPHS_START, GLYPHS_END)
    md, cells = take(md, CELLS_START, CELLS_END)
    return md.rstrip('\n') + '\n', cells, glyphs


# Maths glyph ids whose reading is SETTLED, each by a sighting where the
# text layer reads it sanely and the maths confirms it (scheme pages scanned
# with get_texttrace(); scripts/markbank/derive_glyphs.py's method, applied to
# the one font the lane needs). The same font's text layer reads some of
# these ids as another digit elsewhere, which is the fault being repaired.
# Word embeds the maths glyphs under either name, CambriaMath or Cambria, and
# the ids are one set: 2023 HL scheme p19 draws "log" as 1812/1815/1807 and its
# subscript 2 as 2779 under the name Cambria, the ids settled below under
# CambriaMath on 2021 HL p4, and every id added on 5 Nov reads the same under
# both names across the corpus (counts below are corpus-wide, both names).
#   2778 '1', 2779 '2', 2780 '3', 2781 '4': 2021 HL scheme p4, "2^4 = 1.." and
#       "log2 8 = 3" (2780 is the 3, 2781 the exponent 4); 2779 is also read
#       '2' on 2020 HL p6, 2023 HL p19 and 2024 HL p19.
#   2784 '7': 2020 HL scheme p6, the exponent of "2^7".
#   2785 '8': 2021 HL scheme p4, "log2 8 = 3"; 2020 HL p6's text layer reads
#       the same id as '1' in "128".
#   2783 '6': read '6' 265 times across the corpus schemes (first sighting
#       2014 LC022ALP000EV p5); 2021 HL p4's text layer reads it '1' in "16".
#   1812 'l', 1815 'o', 1807 'g': the bold maths letters of "log" (2021 HL
#       p4, "log2 8 = 3"), read so in 2017 LC021ALP000EV p16 (1812), 2014
#       LC022ALP000EV p8 (1815, 1807); 2021 HL p4 reads all three as 'l'.
#   2170 'N', 2171 'O': bold italic N and O, 2023 HL p19 "O(log2 N)" and 2024
#       HL p19 "N2 - N"; read so every time they are read at all (22 and 24
#       sightings, first 2017 LC021ALP000EV p16 and 2019 LB830CLP000EV p6).
#   2196 'n', 2194 'l', 2197 'o', 2189 'g': bold italic n and "log", 2025 HL
#       p17 "O(n log n)"; read so 131, 42, 25 and 20 times, and on that page.
#   1866 'n': italic n, 2024 HL paper p17 "O(n2)"; read so 1,927 times.
#   2870 '2': the script-size 2 Word sets as an exponent, 2024 HL paper p17
#       "O(n2)", whose text layer reads it as Oriya U+0B36; read '2' 5,441
#       times (first 2014 LC022ALP000EV p5).
#   3398 '-' (minus), 3400 'x' (times), 3404 '=', 4666 '(', 4667 ')': the
#       operators and brackets the text layer files under Malayalam and
#       Ethiopic code points (U+0D46, U+0D48, U+0D4C, U+123A, U+123B); read so
#       12,743, 5,319, 30,613, 13,209 and 13,645 times.
#   Every line read with the ids added on 5 Nov (2022-2025 HL schemes, 2024 HL
#   paper p17) was rendered at 200 dpi and read against the page.
#   (tools: a scan of every corpus scheme's Cambria glyph ids, 5 Nov.)
LANE_GIDS = {('CambriaMath', 2778): '1', ('CambriaMath', 2779): '2', ('CambriaMath', 2780): '3',
             ('CambriaMath', 2781): '4', ('CambriaMath', 2783): '6', ('CambriaMath', 2784): '7',
             ('CambriaMath', 2785): '8', ('CambriaMath', 1812): 'l', ('CambriaMath', 1815): 'o',
             ('CambriaMath', 1807): 'g', ('CambriaMath', 2170): 'N', ('CambriaMath', 2171): 'O',
             ('CambriaMath', 2196): 'n', ('CambriaMath', 2194): 'l', ('CambriaMath', 2197): 'o',
             ('CambriaMath', 2189): 'g', ('CambriaMath', 1866): 'n', ('CambriaMath', 2870): '2',
             ('CambriaMath', 3398): '−', ('CambriaMath', 3400): '×',
             ('CambriaMath', 3404): '=', ('CambriaMath', 4666): '(', ('CambriaMath', 4667): ')'}
MATHS_FONTS = ('Cambria', 'CambriaMath')
SUPERSCRIPT = str.maketrans('0123456789', '⁰¹²³⁴⁵⁶⁷⁸⁹')
SUBSCRIPT = str.maketrans('0123456789', '₀₁₂₃₄₅₆₇₈₉')


def _glyph_reading(family, gid, codepoint):
    """What one drawn glyph says. A maths-font glyph is read by its id; any
    maths-font glyph outside plain Latin whose id is not settled stops the
    read rather than guess. Every other font's text layer is trusted, with
    the lane's code-point folds."""
    if family in MATHS_FONTS:
        if ('CambriaMath', gid) in LANE_GIDS:
            return LANE_GIDS[('CambriaMath', gid)]
        if codepoint > 0x7e:
            raise LaneError(f'{family} glyph {gid} ({chr(codepoint)!r}) has no settled reading')
    return fold(chr(codepoint))


def read_glyph_line(page, y0, y1, x0=None, x1=None, breaks=False):
    """The text printed inside one rectangle, read from the glyph trace rather
    than the text layer: one printed line, or several read in order.

    Each maths glyph may be drawn twice (the second copy has glyph id -1 at the
    same origin), and the maths font's text layer mis-maps digits, operators
    and brackets, so the trace is read once per real glyph and maths glyphs by
    LANE_GIDS. Printed lines are the baselines of the full-size glyphs; a
    digit set smaller than its line and raised (or lowered) against that
    baseline is written as a superscript (or subscript) -- O(n²), log₂ N -- and
    anything else set small stops the read. A gap wider than 2 pt between two
    glyphs is a space. Lines join with a space, except that a line ending in a
    hyphen joins the next line's lower-case word directly ("reverse-sorted").

    A list's second-level bullet is Word's Courier New "o", which the text
    layer reads as the letter o ("arise: o Who owns the data? o Can the
    data..."). A Courier New "o" that opens a printed line and stands apart
    from the word after it is that bullet, and is not read as a letter. With
    `breaks` (a question, which the app sets line by line), every bulleted
    line opens a line of its own -- a sub-bullet with no marker, a bullet
    with its "•" -- as does the first line after a list that starts left of
    the list's text; without it (a marking-scheme row, set as one run of
    text) the lines simply follow one another."""
    glyphs = []
    for t in page.get_texttrace():
        family = re.sub(r'^[A-Z]{6}\+', '', t['font']).split('-')[0].split(',')[0]
        # one trace span can run over several printed lines, so each glyph is
        # placed by its own baseline origin and box, never by its span's box
        for ch in t['chars']:
            if ch[1] < 0 or not y0 <= ch[2][1] <= y1:
                continue
            if x0 is not None and not (x0 <= ch[3][0] and ch[3][2] <= x1):
                continue
            glyphs.append((family, t['size'], ch))
    if not glyphs:
        raise LaneError(f'no glyphs drawn between y {y0} and {y1}')
    full = 0.85 * max(size for _, size, _ in glyphs)
    bases = []
    for y in sorted(ch[2][1] for _, size, ch in glyphs if size >= full):
        if not bases or y - bases[-1][-1] > 2:
            bases.append([y])
        else:
            bases[-1].append(y)
    bases = [sum(b) / len(b) for b in bases]
    lines = [[] for _ in bases]
    for g in glyphs:
        lines[min(range(len(bases)), key=lambda i: abs(g[2][2][1] - bases[i]))].append(g)
    out = []
    list_indent = None
    for base_y, line in zip(bases, lines):
        line = sorted(line, key=lambda g: g[2][2][0])
        inked = [g for g in line if chr(g[2][0]).strip()]
        if not inked:
            continue
        opens = None
        first = inked[0]
        if first[0].startswith('CourierNew') and chr(first[2][0]) == 'o' and len(inked) > 1 \
                and inked[1][2][3][0] - first[2][3][2] > 2:
            opens = 'sub'
            line = [g for g in line if g is not first]
        elif fold(chr(first[2][0])) == '\u2022':
            opens = 'bullet'
        start_x = inked[1][2][3][0] if opens and len(inked) > 1 else first[2][3][0]
        text, last_x = '', None
        for family, size, ch in line:
            x, y = ch[2]
            c = _glyph_reading(family, ch[1], ch[0])
            if size < full and c.strip():
                if not c.isdigit() or abs(y - base_y) <= 1:
                    raise LaneError(f'{c!r} set small at ({x:.1f}, {y:.1f}) is neither an '
                                    f'exponent nor a subscript digit')
                c = c.translate(SUPERSCRIPT if y < base_y else SUBSCRIPT)
            if last_x is not None and x - last_x > 2 and not text.endswith(' ') and c != ' ':
                text += ' '
            text += c
            last_x = x + (ch[3][2] - ch[3][0])
        text = ws(text)
        ended = list_indent is not None and not opens and start_x < list_indent - 3
        if opens:
            list_indent = start_x
        elif ended:
            list_indent = None
        if out and out[-1].endswith('-') and text[:1].islower():
            out[-1] += text
        elif out and breaks and (opens or ended):
            out.append('\n' + text)
        else:
            out.append(text)
    if breaks:
        return '\n'.join(ws(p) for p in ' '.join(out).split('\n'))
    return ws(' '.join(out))


def append_glyphs(year, level, page, y0, y1, x0=None, x1=None):
    """Append the scheme text inside one rectangle, read by glyph id, to the
    scheme .md's glyph block (as a new line of that page's entry): the text
    the provenance gate compares a G() row against. Append-only, as
    append_cells."""
    path = os.path.join(SCHEMES, f'{year}-{level}.md')
    flat, cells, glyphs = _blocks(open(path, encoding='utf8').read())
    doc = pymupdf.open(os.path.join(SCHEMES, f'{year}-{level}.pdf'))
    line = read_glyph_line(doc[page - 1], y0, y1, x0, x1)
    entries = dict(re.findall(r'<!-- compsci:glyphs page (\d+) -->\n(.*?)\n(?=<!--)', glyphs, re.S))
    have = entries.get(str(page), '')
    if line not in have.split('\n'):
        entries[str(page)] = (have + '\n' + line).strip('\n')
    block = [GLYPHS_START] + [x for k in sorted(entries, key=int)
                              for x in (f'<!-- compsci:glyphs page {k} -->', entries[k])] + [GLYPHS_END]
    with open(path, 'w', encoding='utf8') as fh:
        fh.write(flat + cells + '\n'.join(block) + '\n')
    return line


# build-deck's comparableScheme(), its first form: marks-only and label-only
# lines removed, the rest joined and normalised. A row that is found here is
# found by the build's provenance gate.
MARKS_ONLY = re.compile(r'^\s*\d+\s*(\(\s*\d+\s*\))?\s*$')
LABEL_ONLY = re.compile(r'^\s*\(?\s*([ivx]{1,4}|[a-z]|\d{1,2})\s*\)\s*$', re.I)
LEADING_LABEL = re.compile(r'^\s*\(\s*(?:[ivx]{1,4}|[a-z]|\d{1,2})\s*\)\s+(?=\S)', re.I)


def comparable(md):
    raw = re.sub(r'⟨[^⟩]*⟩', ' ', md)
    raw = re.sub(r'^##\s*Page\s*\d+\s*$', ' ', raw, flags=re.M)
    source = raw.split('\n')
    lines = [l for l in source if not MARKS_ONLY.match(l) and not LABEL_ONLY.match(l)]
    # schemeText.mjs's numericRuns: a run of two or more numeric-only lines
    # can itself be the answer (2025 OL Q10's flowchart outputs 0, 2, 4, 6, 8,
    # 10, one value per line), so each such run is a form of its own.
    runs, run = [], []
    for l in source + ['']:
        if MARKS_ONLY.match(l):
            run.append(l.strip())
        else:
            if len(run) >= 2:
                runs.append(norm(' '.join(run)))
            run = []
    return [norm(' '.join(lines)),
            norm(' '.join(LEADING_LABEL.sub('', l) for l in lines))] + runs


def traces(sitting, claim):
    c = norm(claim)
    return bool(c) and any(c in form for form in sitting.md_norm)


# ── cards ───────────────────────────────────────────────────────────────────
def part_id(year, level, q, letter=None, roman=None):
    return f'cs-{year}-{level}-q{q}' + (f'-{letter}' if letter else '') + (f'-{roman}' if roman else '')


def part_ref(year, level, q, letter=None, roman=None):
    return f'{year} {level.upper()} Q{q}' + (f'({letter})' if letter else '') + (f'({roman})' if roman else '')


STOP = {'the', 'a', 'an', 'of', 'to', 'and', 'in', 'on', 'for', 'is', 'that', 'this',
        'with', 'be', 'as', 'by', 'your', 'you', 'it', 'its', 'are', 'or', 'from', 'each',
        'any', 'one', 'two', 'three', 'which', 'what', 'how', 'why', 'used', 'below',
        'shown', 'following', 'state', 'explain', 'describe', 'outline', 'name', 'give',
        'identify', 'suggest', 'figure'}


def concept_for(text):
    words = [w for w in re.findall(r'[a-z0-9]+', text.lower()) if w not in STOP]
    return '-'.join(words[:6]) or 'question'


def section_for(q):
    return 'A' if q <= 12 else ('B' if q <= 15 else 'C')


def doc_for(q):
    return '040' if q >= 16 else '038'


def build_row(sitting, spec, i, question_text, where):
    if spec.get('part') is not None:
        label = sitting.lift(spec['part'])
        if not re.fullmatch(r'\([a-z]\)|\([ivx]+\)', label):
            raise LaneError(f'{where}: part label {label!r} is not a printed (a)/(i) label')
        spec = dict(spec)
        del spec['part']
        row = build_row(sitting, spec, i, question_text, where)
        if row['kind'] in ('anyN',) or spec['kind'] == 'ladder':
            row['contextNote'] = f"{label} {row.get('contextNote', '')}".strip()
        else:
            row['verbatim'] = f"{label} {row['verbatim']}" if ' — ' in row['verbatim'] \
                else f"{label} — {row['verbatim']}"
        return row
    rid = f'r-{i + 1}'
    kind = spec['kind']
    if kind == 'unprinted':
        return {'id': rid, 'kind': 'criterion', 'verbatim': UNPRINTED_ANSWER, 'marks': None,
                'unprinted': True, 'contextNote': sitting.lift(spec['note'])}
    if kind == 'ask':
        if spec.get('steps') is None:
            return {'id': rid, 'kind': 'point', 'verbatim': question_text, 'marks': None, 'ask': True}
        row = {'id': rid, 'kind': 'criterion', 'verbatim': question_text, 'marks': None,
               'permittedMarks': [0] + list(spec['steps']), 'ask': True}
        if spec.get('note') is None:
            raise LaneError(f'{where}: a stepped check row quotes the scheme\'s per-part price')
        row['contextNote'] = check_note(where, sitting.lift(spec['note'], note=True))
        return row
    if kind == 'anyN':
        options = [sitting.lift(o) for o in spec['options']]
        for o in options:
            halves = o.split(' — ')
            if not traces(sitting, o) and not (
                    len(halves) == 2 and all(traces(sitting, h) for h in halves)):
                raise LaneError(f'{where}: option not in the scheme .md: {o[:70]!r}')
        if spec['claim'] > len(options):
            raise LaneError(f'{where}: any {spec["claim"]} of {len(options)} options')
        head = sitting.lift(spec['head'])
        group = {'claimMax': spec['claim'], 'perOption': spec['each'], 'options': options}
        if spec.get('steps'):
            if len(spec['steps']) != spec['claim']:
                raise LaneError(f'{where}: steps must have one value per claim')
            group['perOptionSteps'] = spec['steps']
        row = {'id': rid, 'kind': 'anyN', 'verbatim': head, 'marks': None, 'group': group}
        if spec.get('open'):
            row['openList'] = True
        note = [n for n in (spec.get('note'), spec.get('instruction')) if n is not None]
        if note:
            row['contextNote'] = check_note(where, ' '.join(sitting.lift(n, note=True) for n in note))
        if spec.get('route'):
            row['route'] = spec['route']
        return row
    if kind == 'ladder':
        options = [sitting.lift(o) for o in spec['options']]
        for o in options:
            halves = o.split(' — ')
            if not traces(sitting, o) and not (
                    len(halves) == 2 and all(traces(sitting, h) for h in halves)):
                raise LaneError(f'{where}: option not in the scheme .md: {o[:70]!r}')
        if not traces(sitting, options[0].split(' — ')[-1]):
            raise LaneError(f'{where}: first option must trace on its own: {options[0][:70]!r}')
        sums = {0}
        for item in spec['items']:
            if not item or list(item) != sorted(set(item)) or item[0] <= 0:
                raise LaneError(f'{where}: ladder item {item} is not the printed values above zero')
            sums = {a + b for a in sums for b in [0] + list(item)}
        row = {'id': rid, 'kind': 'criterion', 'verbatim': options[0],
               'marks': sum(item[-1] for item in spec['items']), 'permittedMarks': sorted(sums)}
        if len(options) > 1:
            row['accepts'] = options[1:]
        note = [n for n in (spec.get('head'), spec.get('instruction'), spec.get('note')) if n is not None]
        if note:
            row['contextNote'] = check_note(where, ' '.join(sitting.lift(n, note=True) for n in note))
        if spec.get('route'):
            row['route'] = spec['route']
        return row
    text = sitting.lift(spec['text'])
    if spec.get('head') is not None:
        text = f"{sitting.lift(spec['head'])} — {text}"
    claim = text.split(' — ')[-1]
    if not traces(sitting, claim):
        raise LaneError(f'{where}: row not in the scheme .md: {text[:70]!r}')
    row = {'id': rid, 'kind': kind, 'verbatim': text, 'marks': spec['marks']}
    if kind == 'criterion' and spec.get('parts'):
        # Named components the scheme prices separately ("Name: 1 mark /
        # Explanation: 5 or 2"), each placed on its own printed steps.
        parts, sums = [], {0}
        for j, (lift, m, st) in enumerate(spec['parts']):
            ladder = [0] + list(st) + [m]
            parts.append({'id': f'p-{j + 1}', 'verbatim': sitting.lift(lift), 'marks': m,
                          'permittedMarks': ladder})
            sums = {a + b for a in sums for b in ladder}
        if sum(p['marks'] for p in parts) != spec['marks']:
            raise LaneError(f'{where}: parts do not add up to the row')
        row['parts'] = parts
        row['permittedMarks'] = sorted(sums)
    elif kind == 'criterion':
        steps = [0] + list(spec['steps']) + [spec['marks']]
        if steps != sorted(set(steps)):
            raise LaneError(f'{where}: criterion steps {steps} are not ascending')
        row['permittedMarks'] = steps
    if spec.get('note'):
        row['contextNote'] = check_note(where, sitting.lift(spec['note'], note=True))
    if spec.get('route'):
        row['route'] = spec['route']
    return row


def check_note(where, note):
    """A note is the scheme's direction for ONE part. A slice that runs into
    the next question's head took its start from an earlier part. 900
    characters holds the longest single part's own directions: 2020 HL
    Section C prints a descriptor list for every step of a scale, up to 828
    characters for Q16(b)(iii), each bounded by the part's head and its last
    descriptor."""
    if re.search(r'\bQuestion \d', note) or len(note) > 900:
        raise LaneError(f'{where}: note runs past its part: {note[:90]!r}')
    return note


def row_worth(row):
    if row['kind'] == 'anyN':
        g = row['group']
        if g.get('perOptionSteps'):
            return sum(g['perOptionSteps'][:g['claimMax']])
        return g['claimMax'] * g['perOption']
    return row['marks'] or 0


def build_card(sitting, mod, entry, figures):
    year, level = sitting.year, sitting.level
    q, letter, roman = entry['key']
    cid = entry.get('id') or part_id(year, level, q, letter, roman)
    where = f'{year} {level} {cid}'
    if not entry.get('why'):
        raise LaneError(f'{where}: say what the page shows (why=)')
    topic = entry.get('topic')
    if topic not in TOPICS:
        raise LaneError(f'{where}: topic {topic!r} is not a Computer Science topic')
    question = sitting.lift(entry['ask'])
    stem = sitting.lift(entry.get('stem'))
    tariff = entry.get('tariff', 'fixed')
    total = entry['total']
    printed = entry.get('printed')
    if printed is not None:
        page = printed.page if isinstance(printed, Lift) else None
        sitting.lift(printed)              # the tariff cell must be on the page
        # A part priced per item ("Each Correct Item 1 mark") for a printed
        # count ("Identify three"): tariff_note says how the total follows.
        if not entry.get('tariff_note') and str(total) not in ws(sitting.lift(printed)):
            raise LaneError(f'{where}: total {total} is not in the printed tariff '
                            f'{sitting.lift(printed)!r}')
    else:
        from cs_scheme import CsScheme
        sch = _scheme(year, level)
        read = sch.tariff(q, letter, roman)
        if read != total:
            raise LaneError(f'{where}: the scheme reads {read} marks for this part, the module '
                            f'says {total}; quote the tariff cell with printed=S(...)')
    rows = [build_row(sitting, spec, i, question, where) for i, spec in enumerate(entry['rows'])]
    if tariff == 'questionTotal':
        tariff_model = {'kind': 'questionTotal'}
        for r in rows:
            if r['kind'] != 'anyN':
                r['marks'] = None
    else:
        tariff_model = {'kind': 'fixed'}
        if not any(r.get('unprinted') or r.get('ask') for r in rows):
            common = sum(row_worth(r) for r in rows if not r.get('route'))
            routes = {}
            for r in rows:
                if r.get('route'):
                    routes[r['route']] = routes.get(r['route'], 0) + row_worth(r)
            for name, worth in (routes or {None: 0}).items():
                if common + worth != total:
                    raise LaneError(f'{where}: rows are worth {common + worth}'
                                    f'{" on route " + name if name else ""}, the tariff is {total}')
    if any(r.get('ask') for r in rows) and len(rows) == 1:
        rows[0]['marks'] = total
        if 'permittedMarks' in rows[0]:
            steps = rows[0]['permittedMarks'] + [total]
            if steps != sorted(set(steps)):
                raise LaneError(f'{where}: check-row steps {steps} are not ascending')
            rows[0]['permittedMarks'] = steps
    if any(r.get('unprinted') for r in rows):
        rows[0]['marks'] = total
    card = {
        'id': cid, 'topicId': topic,
        'conceptId': entry.get('concept') or concept_for(question),
        'level': LEVEL_WORD[level], 'year': year, 'subjectId': SUBJECT,
        'section': section_for(q), 'questionRef': part_ref(year, level, q, letter, roman),
        'questionText': question, 'tariffModel': tariff_model, 'totalMarks': total,
        'rows': rows,
    }
    if stem:
        card['stem'] = stem
    for field, name in (('figureKey', entry.get('figure')),
                        ('questionFigureKey', entry.get('qfigure'))):
        if name:
            key = figure_key(year, level, name)
            if key not in figures:
                raise LaneError(f'{where}: figure {key} is not published -- run crops')
            card[field] = key
    if entry.get('labels'):
        # A question naming a lettered symbol ("the symbol labelled A") needs
        # the letter decoded; the meaning is the scheme's own answer, shown in
        # the reveal's label key, never typed.
        if not card.get('figureKey'):
            raise LaneError(f'{where}: a labelled figure must be the card\'s figure')
        card['labelKey'] = [{'letter': k, 'meaning': sitting.lift(v), 'askedInThisQuestion': True}
                            for k, v in entry['labels'].items()]
    if card.get('questionFigureKey'):
        # The crop is the printed matter beside the ask, never the ask itself:
        # the lifted stem and question stay on the card around it.
        card['questionFigureIncludesPrompt'] = False
    if any(r.get('ask') for r in rows):
        if not card.get('figureKey') or not figures[card['figureKey']].get('solution'):
            raise LaneError(f'{where}: an ask row needs the scheme\'s drawing as a solution figure')
    return card


_SCHEMES = {}


def _scheme(year, level):
    from cs_scheme import CsScheme
    if (year, level) not in _SCHEMES:
        _SCHEMES[(year, level)] = CsScheme(year, level)
    return _SCHEMES[(year, level)]


# ── crops ───────────────────────────────────────────────────────────────────
def figure_key(year, level, name):
    """'q1-code' -> computer-science-2026-HL-paper-q1-code; 's-q3' -> ...-scheme-q3."""
    if name.startswith('s-'):
        return f'{SUBJECT}-{year}-{level.upper()}-scheme-{name[2:]}'
    return f'{SUBJECT}-{year}-{level.upper()}-paper-{name}'


def crop(doc, page, rect, alt, ref, solution=False, rotate=0):
    """One printed region: `doc` '038'/'040'/'scheme', one-based `page`, `rect`
    in PDF points (x0, y0, x1, y1), measured on the page and opened before use.
    `rotate` (degrees) turns a figure the paper prints on its side upright
    (2022 OL Figure 11: rotate=90)."""
    return {'parts': [(doc, page, rect)], 'alt': alt, 'ref': ref, 'solution': solution,
            'rotate': rotate}


def stack(parts, alt, ref, solution=False):
    """Several printed regions of ONE question, stacked top to bottom in the
    order the paper prints them, with a white gap: a question whose printed
    matter is spread across a page around its answer boxes (2026 HL Q14(a):
    Figure 3 at the top right, Figures 4 and 5 below, the table at the foot)."""
    return {'parts': parts, 'alt': alt, 'ref': ref, 'solution': solution}


GAP = 18


def render_crop(sitting, spec):
    pixes = []
    for doc, pageno, rect in spec['parts']:
        d = sitting.docs['scheme' if doc == 'scheme' else doc]
        page = d[pageno - 1]
        clip = pymupdf.Rect(*rect) & page.rect
        matrix = pymupdf.Matrix(SCALE, SCALE)
        if spec.get('rotate'):
            matrix = matrix.prerotate(spec['rotate'])
        pixes.append(page.get_pixmap(matrix=matrix, clip=clip, alpha=False))
    if len(pixes) == 1:
        return pixes[0]
    width = max(p.width for p in pixes)
    height = sum(p.height for p in pixes) + GAP * (len(pixes) - 1)
    out = pymupdf.Pixmap(pymupdf.csRGB, pymupdf.IRect(0, 0, width, height), False)
    out.set_rect(out.irect, (255, 255, 255))
    y = 0
    for p in pixes:
        p.set_origin(0, y)
        out.copy(p, p.irect)
        y += p.height + GAP
    return out


def publish_crops(sitting, mod, write=True, only=None):
    figures = json.load(open(FIGURES, encoding='utf8'))
    os.makedirs(FIG_DIR if write else PREVIEW, exist_ok=True)
    out = []
    word = 'Higher' if sitting.level == 'hl' else 'Ordinary'
    # build-deck reads figures-computer-science.json OVER figures.json and drops
    # a card whose crop no longer matches the md5 pinned there: those curated
    # crops are reused as they are, never re-rendered under the same key.
    curated_path = os.path.join(ROOT, 'components', 'MarkBank', f'figures-{SUBJECT}.json')
    curated = json.load(open(curated_path, encoding='utf8')) if os.path.exists(curated_path) else {}
    for name, spec in getattr(mod, 'CROPS', {}).items():
        if only and name not in only:
            continue
        key = figure_key(sitting.year, sitting.level, name)
        if write and key in curated:
            raise LaneError(f'{key} is a curated crop (figures-{SUBJECT}.json); name the new crop '
                            f'differently or reuse the curated one without a CROPS entry')
        pix = render_crop(sitting, spec)
        path = os.path.join(FIG_DIR, f'{key}.png')
        if write:
            pix.save(path)
            md5 = hashlib.md5(open(path, 'rb').read()).hexdigest()
            rec = {
                'src': f'{FIG_SRC}/{key}.png', 'md5': md5, 'alt': spec['alt'],
            }
            if spec.get('solution'):
                rec['solution'] = True
            rec.update({'lettersVisible': [], 'labelMeanings': [],
                        'questionRef': spec['ref'], 'year': sitting.year,
                        'level': LEVEL_WORD[sitting.level],
                        'attribution': f'SEC Leaving Certificate Computer Science {sitting.year} '
                                       f'{word} Level — © State Examinations Commission'})
            figures[key] = rec
        else:
            path = os.path.join(PREVIEW, f'{key}.png')
            pix.save(path)
        out.append((key, path, pix.width, pix.height))
    if write:
        with open(FIGURES, 'w', encoding='utf8') as fh:
            json.dump(figures, fh, ensure_ascii=False, indent=1)
            fh.write('\n')
    return out


# ── modules ─────────────────────────────────────────────────────────────────
def module(year, level):
    name = f'compsci_sittings.y{year}_{level}'
    try:
        return importlib.import_module(name)
    except ModuleNotFoundError as exc:
        if exc.name == name:
            return None
        raise


def sittings():
    out = []
    pkg = os.path.join(DIR, 'compsci_sittings')
    for f in sorted(os.listdir(pkg)):
        m = re.match(r'^y(\d{4})_(hl|ol)\.py$', f)
        if m:
            out.append((int(m.group(1)), m.group(2)))
    return out


def figure_index():
    """Every figure a card may name: figures.json, with the curated crops of
    figures-computer-science.json read over it, as build-deck reads them."""
    figures = json.load(open(FIGURES, encoding='utf8'))
    curated = os.path.join(ROOT, 'components', 'MarkBank', f'figures-{SUBJECT}.json')
    if os.path.exists(curated):
        figures.update(json.load(open(curated, encoding='utf8')))
    return figures


def build(targets):
    deck = json.load(open(AUTHORED, encoding='utf8'))
    figures = figure_index()
    lane_ids = set()
    made = []
    withdrawn = {}
    for year, level in targets:
        mod = module(year, level)
        if mod is None:
            raise LaneError(f'no module compsci_sittings/y{year}_{level}.py')
        sitting = Sitting(year, level)
        errors = []
        for entry in mod.CARDS:
            try:
                card = build_card(sitting, mod, entry, figures)
            except LaneError as exc:
                errors.append(str(exc))
                continue
            if card['id'] in lane_ids:
                raise LaneError(f'{card["id"]}: two module entries make this card')
            lane_ids.add(card['id'])
            made.append((entry, card))
        if errors:
            raise LaneError('\n'.join(errors))
        withdrawn.update(getattr(mod, 'WITHDRAWN', {}))
    aliases = card_aliases()
    for old, new in withdrawn.items():
        if new not in lane_ids:
            raise LaneError(f'{old}: withdrawn onto {new}, which no module entry makes')
        if aliases.get(old) != new:
            raise LaneError(f'{old}: withdrawn without the alias {old} -> {new} in '
                            f'components/MarkBank/cardAliases.ts (run: aliases YEAR LEVEL)')
    deck = [c for c in deck if c['id'] not in withdrawn]
    owned = _owned() - set(withdrawn)
    by_id = {c['id']: i for i, c in enumerate(deck)}
    for entry, card in made:
        cid = card['id']
        if cid in by_id and cid not in owned and not entry.get('replaces'):
            raise LaneError(f'{cid}: the bank already ships this id; a lane card for it '
                            f'must say replaces= and why')
        if cid in by_id:
            deck[by_id[cid]] = card
        else:
            by_id[cid] = len(deck)
            deck.append(card)
    _record_owned(owned | lane_ids)
    with open(AUTHORED, 'w', encoding='utf8') as fh:
        json.dump(deck, fh, ensure_ascii=False, indent=1)
        fh.write('\n')
    return [c for _, c in made]


OWNED = os.path.join(DIR, 'compsci_sittings', 'owned.json')
ALIASES = os.path.join(ROOT, 'components', 'MarkBank', 'cardAliases.ts')
ALIAS_LINE = re.compile(r'^  "([^"]+)": "([^"]+)",$', re.M)


def card_aliases():
    return dict(ALIAS_LINE.findall(open(ALIASES, encoding='utf8').read()))


def write_aliases(year, level):
    """Add a module's WITHDRAWN ids to cardAliases.ts, each onto its successor.

    A shipped whole-question card that duplicated part cards is withdrawn
    (coordinator, 5 Nov): its review history is read by the question's first
    new part card. Only Computer Science lines are added, in the file's own
    sorted order; nothing else in the file changes."""
    mod = module(year, level)
    want = getattr(mod, 'WITHDRAWN', {})
    text = open(ALIASES, encoding='utf8').read()
    have = card_aliases()
    lines = text.split('\n')
    for old, new in sorted(want.items()):
        if have.get(old) == new:
            continue
        if old in have:
            raise LaneError(f'{old} is already aliased onto {have[old]}')
        entry = f'  "{old}": "{new}",'
        idx = [i for i, l in enumerate(lines) if ALIAS_LINE.match(l)]
        after = [i for i in idx if ALIAS_LINE.match(lines[i]).group(1) > old]
        lines.insert(after[0] if after else idx[-1] + 1, entry)
    with open(ALIASES, 'w', encoding='utf8') as fh:
        fh.write('\n'.join(lines))
    return want


def _owned():
    return set(json.load(open(OWNED))) if os.path.exists(OWNED) else set()


def _record_owned(ids):
    with open(OWNED, 'w') as fh:
        json.dump(sorted(ids), fh, indent=1)
        fh.write('\n')


# ── worksheets ──────────────────────────────────────────────────────────────
def sheet(year, level):
    """Every census leaf of the sitting: open or covered, tariff, reader text."""
    import paper as PP
    import reconcile as R
    from paper_census import census_subject
    census = census_subject(SUBJECT)
    leaves = next(p['leaves'] for p in census['papers']
                  if p['year'] == year and p['level'] == level)
    res = R.reconcile_subject(SUBJECT, census)
    open_labels = set()
    for p in res['papers']:
        if p['year'] == year and p['level'] == level:
            open_labels |= set(p['open'])
    sch = _scheme(year, level)
    paper = PP.Paper(SUBJECT, year, level)
    for leaf in leaves:
        s, q, a, r = leaf['key']
        state = 'OPEN' if leaf['label'] in open_labels else 'cov '
        print(f"{state} {leaf['label']:<24} t={sch.tariff(q, a, r)!s:<4} "
              f"{ws(paper.text(q, a, r) or '')[:100]}")


def lines(year, level, doc, page):
    s = Sitting(year, level)
    d = s.docs[doc]
    p = d[page - 1]
    print(f'page {page}: {p.rect}')
    for b in p.get_text('dict')['blocks']:
        if b.get('type') == 1:
            print(f"  IMAGE {tuple(round(v) for v in b['bbox'])}")
            continue
        for ln in b.get('lines', []):
            t = ''.join(sp['text'] for sp in ln['spans']).strip()
            if t:
                print(f"  {tuple(round(v) for v in ln['bbox'])} {t[:90]}")
    rects = [dr['rect'] for dr in p.get_drawings() if dr['rect'].width > 30 or dr['rect'].height > 30]
    if rects:
        u = rects[0]
        for r in rects[1:]:
            u |= r
        print(f'  DRAWINGS {len(rects)} union {tuple(round(v) for v in u)}')


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    cmd = argv[1]
    if cmd == 'sheet':
        sheet(int(argv[2]), argv[3])
    elif cmd == 'lines':
        lines(int(argv[2]), argv[3], argv[4], int(argv[5]))
    elif cmd == 'crops':
        year, level = int(argv[2]), argv[3]
        only = set(argv[4].split(',')) if len(argv) > 4 else None
        mod = module(year, level)
        for key, path, w, h in publish_crops(Sitting(year, level), mod, only=only):
            print(f'{key} {w}x{h} {path}')
    elif cmd == 'preview':
        year, level = int(argv[2]), argv[3]
        only = set(argv[4].split(',')) if len(argv) > 4 else None
        mod = module(year, level)
        for key, path, w, h in publish_crops(Sitting(year, level), mod, write=False, only=only):
            print(f'{key} {w}x{h} {path}')
    elif cmd == 'aliases':
        for old, new in write_aliases(int(argv[2]), argv[3]).items():
            print(f'{old} -> {new}')
    elif cmd == 'glyphs':
        xs = [float(x) for x in argv[7:9]] if len(argv) > 8 else [None, None]
        print(append_glyphs(int(argv[2]), argv[3], int(argv[4]), float(argv[5]), float(argv[6]), *xs))
    elif cmd == 'cells':
        n = append_cells(int(argv[2]), argv[3], [int(x) for x in argv[4].split(',')])
        print(f'{n} lines in the cells block')
    elif cmd == 'build':
        targets = sittings() if argv[2] == 'all' else [(int(argv[2]), argv[3])]
        cards = build(targets)
        print(f'{len(cards)} lane card(s) written for {targets}')
    else:
        print(__doc__)
        return 2
    return 0


if __name__ == '__main__':
    # Run through the importable module, so the Lift class the sitting modules
    # build their entries from is the one this code checks against.
    import compsci_lane
    sys.exit(compsci_lane.main(sys.argv))
