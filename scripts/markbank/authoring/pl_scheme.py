#!/usr/bin/env python3
"""Polish marking schemes — the priced answer, and the question it reprints.

    python3 scripts/markbank/authoring/pl_scheme.py 2024 hl --full
    python3 scripts/markbank/authoring/pl_scheme.py --audit

What this document is
---------------------
From 2022 a Polish scheme is four documents in one file, and only two of them
answer anything:

    Część A   Czytanie      100 punktów   <- priced answers, question reprinted
    Część B   Pisanie        80 punktów   <- a CONTENT and EXPRESSION grid
    Listening Comprehension 100 marks     <- priced answers, but the ask needs
                                             the recording
    APPENDIX 2 CD SCRIPT                  <- the recording, in print

The 2021 scheme is a different examination and prints neither section head:
"Część I (30/70)" holds six numbered questions on one text and "CZĘŚĆ II
(40/70)" two essay titles under a list of four qualities.

**The tariff is a column, not a suffix.** The SEC prints "Two of:" at x≈75 and
"(2 x 2m)" at x≈489 on the SAME printed line, and pymupdf reports them as two
separate lines. Read naively the directive has no tariff and the tariff has no
ask. So the page is gathered into ROWS by baseline first, exactly as
extract-scheme.py does — which is also what keeps a card's rows traceable in
the .md the provenance gate reads.

**The tariff notation is not one notation.** Nine schemes print it eleven ways
— "2m", "2 m", "2 marks", "2 x 2m", "2 × 3 m", "3 x 2 marks", "1m + 1m" — with
U+00A0 for every space from 2023 on. All of them are read; none is guessed at.
Where a directive and a tariff disagree about how many answers are claimable —
"Three of:" over "(2 x 2m)" — the ask carries a FAULT and is refused, never
averaged.

**"(i)" is the ninth letter here too.** 2022 Higher runs Question 1's parts to
"(k)". The scheme settles it the same way the paper does, on the printed
column: the letters stand at the file's own letter margin and the romans are
indented past it. See pl_paper.PlPaper._is_letter, whose two conditions this
mirrors.

Section B and the listening test are read too — not to be carded, but so the
refusals this bank records are counted from the document rather than assumed.
"""
import argparse
import collections
import glob
import os
import re
import sys

import pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))
from markbank_text import unligature                            # noqa: E402

SUBJECT = 'polish'


def schemes_dir(subject=SUBJECT):
    return os.path.join(ROOT, 'examiner-reports', subject, 'schemes')


def scheme_path(year, level, subject=SUBJECT):
    path = os.path.join(schemes_dir(subject), f'{year}-{level}.pdf')
    return path if os.path.exists(path) else None


NBSP = '   '
# The Symbol and Wingdings space, which those fonts encode in the private-use
# area. It is a space and nothing else, and left as itself it reaches a card
# as an unresolvable glyph the build refuses.
SYMBOL_SPACE = '\uf020\uf0a0'


def _norm(text):
    """One printed cell, with the SEC's broken font glyphs put back.

    The bank's shared map (markbank_text.unligature), not a local one: the four
    Ordinary schemes bullet every marking point with the Wingdings U+F0FC and
    set "quesƟons" with the same font's ti ligature.
    """
    out = ''.join(' ' if c in NBSP or c in SYMBOL_SPACE else c
                  for c in unligature(text))
    return re.sub(r'\s+', ' ', out).strip()


class Row:
    __slots__ = ('page', 'x', 'y', 'text', 'cells')

    def __init__(self, page, x, y, text, cells=()):
        self.page, self.x, self.y, self.text = page, x, y, text
        # (x, text) for every printed cell of the row, kept because a
        # true/false answer is not in the words at all: it is a TICK, and which
        # column it stands in is the answer.
        self.cells = list(cells)

    def __repr__(self):
        return f'Row(p{self.page} x={self.x:.1f} {self.text[:70]!r})'


ROW_TOL = 4.0

# How far right of the letter column a marker may still be a LETTER.
# Measured, not guessed: the 2025 Higher scheme sets Question 1's letters at
# x=50.0, 53.2 and 57.1 in one page — the SEC's own table cells drift — so a
# three-point window read "(b)" as body text, swallowed its directive into the
# ask above and reported that ask's tariff as disagreeing with itself. Widening
# it is safe because the ONLY marker that can be read two ways is "(i)", and
# that one has to satisfy the sequence test as well.
LETTER_TOL = 8.0


# The SEC's own numbering, used as a second way in. A marker that is the NEXT
# letter after the one before it IS that letter, wherever the cell puts it:
# 2025 Ordinary sets Zadanie 3's letters at x=72 and then prints "(g)" at
# x=90, eighteen points right of its own column, and a column test alone read
# it as body text and filed its five romans under (f) — every one of them off
# by a letter, which is a wrong citation that passes every downstream gate.
# "(i)" is excluded from this path on purpose: it is the one marker that can be
# a roman, so it still has to satisfy BOTH the column and the sequence.
def next_letter(current):
    return 'a' if not current else chr(ord(current) + 1)


def read_rows(path):
    """The scheme's pages as printed ROWS, left to right, with the left margin.

    A marking point and the marks it earns sit in different cells of one
    printed row. Emitting a cell per line separates an answer from its price,
    which is how "the scheme prints no tariff" gets said about a document that
    prices every line.
    """
    out = []
    with pymupdf.open(path) as doc:
        for pno, page in enumerate(doc, 1):
            lines = []
            for block in page.get_text('dict')['blocks']:
                if block.get('type') != 0:
                    continue
                for line in block['lines']:
                    text = _norm(''.join(s['text'] for s in line['spans']))
                    if not text:
                        continue
                    x0, y0, x1, y1 = line['bbox']
                    lines.append((x0, (y0 + y1) / 2, text))
            for block in page.get_text('dict')['blocks']:
                if block.get('type') != 0:
                    continue
                for line in block['lines']:
                    for span in line['spans']:
                        text = _norm(span['text'])
                        if text and TICK.fullmatch(text):
                            lines.append((span['bbox'][0],
                                          (span['bbox'][1] + span['bbox'][3]) / 2,
                                          text))
            lines.sort(key=lambda l: (l[1], l[0]))
            band = []
            for x, y, text in lines:
                if band and abs(y - band[0][1]) <= ROW_TOL:
                    band.append((x, y, text))
                    continue
                if band:
                    out.append(_row(pno, band))
                band = [(x, y, text)]
            if band:
                out.append(_row(pno, band))
    return _fold_tick_rows(_fold_marker_rows(out))


MARKER_ONLY = re.compile(r'^\(\s*([a-z]{1,4})\s*\)\.?$', re.I)
CELL_TOL = 12.0


def _fold_marker_rows(rows):
    """A marker printed alone in its cell belongs to the row beside it.

    2023 Higher sets Question 1(h)'s true/false table with the statement on
    one baseline, the roman marker half a line below it and the rest of the
    statement below that — three rows for one printed cell. Left apart the
    marker opens an ask with no words in it and the statement, with the tick
    that answers it, is filed under the ask above.
    """
    out, used = [], set()
    for i, row in enumerate(rows):
        if i in used:
            continue
        if len(row.cells) == 1 and MARKER_ONLY.match(row.cells[0][1]):
            mates = [j for j in range(max(0, i - 3), min(i + 4, len(rows)))
                     if j != i and j not in used
                     and rows[j].page == row.page
                     and abs(rows[j].y - row.y) <= CELL_TOL
                     and rows[j].cells[0][0] > row.x + 4
                     and not MARKER_ONLY.match(rows[j].cells[0][1])]
            if mates:
                mates.sort(key=lambda j: rows[j].y)
                used.update(mates)
                # A mate ABOVE the marker is already in `out` — the SEC sets
                # the marker below the first line of the cell it labels — so
                # it is taken back out rather than left there twice.
                for j in mates:
                    if rows[j] in out:
                        out.remove(rows[j])
                cells = list(row.cells)
                for j in mates:
                    cells += rows[j].cells
                cells.sort(key=lambda c: c[0])
                row = Row(row.page, row.x,
                          min([row.y] + [rows[j].y for j in mates]),
                          _norm(' '.join(t for _x, t in cells)), cells)
        out.append(row)
    out.sort(key=lambda r: (r.page, r.y, r.x))
    return out


TICK_ROW_TOL = 14.0


def _fold_tick_rows(rows):
    """A tick set half a line below the statement it marks belongs to it.

    The SEC centres the tick in its table cell while the statement beside it
    wraps, so 2024 Ordinary prints "(i) Pan Alojzy z łatwością podjął decyzję"
    at y=517 and its tick at y=523 — six points apart, which a four-point band
    keeps separate. Left separate the verdict has no statement and the
    statement has no verdict.
    """
    out = []
    for row in rows:
        only_marks = row.cells and all(
            TICK.fullmatch(t) or BARE_TARIFF.fullmatch(t) or TARIFF.fullmatch(t)
            or t in '-‐–' for _x, t in row.cells)
        if only_marks and out and row.page == out[-1].page \
                and 0 <= row.y - out[-1].y <= TICK_ROW_TOL:
            prev = out[-1]
            prev.cells = sorted(prev.cells + row.cells, key=lambda c: c[0])
            prev.text = _norm(' '.join(t for _x, t in prev.cells))
            continue
        out.append(row)
    return out


def _row(page, band):
    band = sorted(band, key=lambda t: t[0])
    # De-duplicate: a tick is collected twice, once inside its own line and
    # once as a span, so that a row whose only content is a tick survives the
    # line-level pass at all.
    cells = [(x, text) for x, _y, text in band]
    # A tick reaches this TWICE — once inside the line that holds it and once
    # as a span of its own, so that a row whose only content is a tick survives
    # the line pass at all — and pymupdf reports the two origins a fraction of
    # a point apart. The bare copy is dropped wherever the line beside it
    # already opens with the same tick; left in, every Ordinary marking point
    # shipped with the bullet glyph welded to its front twice over.
    keep = []
    for i, (x, text) in enumerate(cells):
        if TICK.fullmatch(text) and any(
                j != i and abs(cells[j][0] - x) < 3.0
                and len(cells[j][1]) > 1 and TICK.match(cells[j][1][0])
                for j in range(len(cells))):
            continue
        keep.append((x, text))
    cells = keep
    return Row(page, cells[0][0], band[0][1],
               _norm(' '.join(t[1] for t in cells)), cells)


# ---------------------------------------------------------------- the units --
UNIT_READING = re.compile(r'^Cz[eę][sś][cć]\s+A\b.*(?:Czytanie|Reading)|'
                          r'^Section\s+A\b.*Reading', re.I)
UNIT_WRITING = re.compile(r'^Cz[eę][sś][cć]\s+B\b.*(?:Pisanie|Writing)|'
                          r'^Section\s+B\b.*Writing', re.I)
UNIT_LISTENING = re.compile(r'^Listening\s+comprehension\b', re.I)
# Everything from here is the CD script — the recording in print, in the ANSWER
# document — and its speaker turns are not marking points.
APPENDIX = re.compile(r'^APPENDIX\b', re.I)
# 2021's own two parts.
PART_2021 = re.compile(r'^CZ[EĘ][SŚ][CĆ]\s+(I{1,2})\b', re.I)

Q_HEAD = re.compile(r'^(?:Question|Pytanie|Zadanie)\s*(\d{1,2})\b')
LISTEN_HEAD = re.compile(r'^Cz[eę][sś][cć]\s+([A-F])\b')
LETTER = re.compile(r'^\(?\s*([a-l])\s*\)\s*(.*)$', re.I)
ROMAN = re.compile(r'^\(\s*(i{1,3}|iv|vi{0,3}|ix|x)\s*\)\s*(.*)$', re.I)
NUMBERED = re.compile(r'^(\d{1,2})\s*\.\s*(.*)$')
ROMANS = ['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x']

# The tariff, in every notation the nine schemes print:
#   (2m) (2 m) (2 marks) (1 mark)          one answer
#   (2 x 2m) (3 × 2 marks) (2 x 1 mark)    N answers at M each
TARIFF = re.compile(
    r'\(\s*(?:(\d{1,2})\s*[x×]\s*)?(\d{1,2})\s*(?:m|marks?)\s*\.?\s*\)', re.I)
# The same tariff with no brackets at all, which is how a true/false table
# prices its rows: "Franek chętnie kupował książki. ✓ 2 marks".
BARE_TARIFF = re.compile(r'(?:^|\s)(\d{1,2})\s*marks?\s*$', re.I)
# "(1m + 1m)" — two answers at one mark each, written as a sum. 2022 Higher
# Question 1(c)(iv) is the only one, and reading it as "1 mark" alone would
# under-price the ask by half.
SUM_TARIFF = re.compile(r'\(\s*(\d{1,2})\s*m\s*\+\s*(\d{1,2})\s*m\s*\)', re.I)
# The 2021 examination prices in PUNKTY and writes the unit nowhere: its heads
# read "(5)" and "(5 × 1)" in the right-hand column, and its rate is a sentence
# under them. Read only for that sitting, because a bare number in brackets is
# a paragraph reference everywhere else — "(p. 1)", "(akapit 4)".
PUNKTY = re.compile(r'^\(\s*(\d{1,2})\s*(?:[x×]\s*(\d{1,2})\s*)?\)$')
# The rate the 2021 scheme states in words, under the head that carries the
# total. Two of the four shapes it prints are flat or descending and can be
# read; the other two pay one rate for the content and another for the opinion
# beside it, which is not a ladder and is refused rather than averaged.
RATE_FLAT = re.compile(r'^(\d{1,2})\s+punkt\w*\s+za\s+każde\b', re.I)
RATE_DESC = re.compile(r'^(\d{1,2})\s+punkt\w*\s+za\s+jeden\s+\w+,\s*po\s+'
                       r'(\d{1,2})\s+punkcie\s+za\s+każdy\s+następny', re.I)

COUNT_WORD = {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6,
              'jeden': 1, 'dwa': 2, 'trzy': 3, 'cztery': 4}
DIRECTIVE = re.compile(
    r'^(?:any\s+)?(one|two|three|four|five|six)\s+(?:of|items?|details?)\b\s*:?',
    re.I)
ALL_OR_NOTHING = re.compile(r'^All\s+or\s+nothing\s*:?', re.I)
EITHER = re.compile(r'^Either\b|^or\s*$|^lub\s*$', re.I)
# Examiner rubric, which is never an answer. The tick instructions are here
# because the SEC prints them BETWEEN the question and its answers — "Put a
# tick (✓) in the appropriate box. Choose one statement only." — and left in
# they become the first marking point of every tick-one-box ask in the corpus.
NOTE = re.compile(r'^(?:Note\s*:|N\.?B\.?\b|Uwaga\b|Penalise\b|Accept\b|Allow\b|'
                  r'When\s+the\s+correct|When\s+more\s+than|'
                  r'Put\s+a\s+tick\b|Tick\s+(?:the|one)\b|'
                  r'Zaznacz\s*\(|Odpowiedzi\s+zaznacz\b|'
                  r'Mark\s*\(.\)\s+the\s+correct)', re.I)
# The tick instruction alone. It is rubric — never a marking point — but the
# SEC prints the ASK's tariff at the end of it, "Put a tick (✓) in the
# appropriate box. Choose one statement only. (2m)", so the price is taken off
# it before the line is dropped. Thrown away whole, every tick-one-box ask in
# the corpus read as unpriced.
RUBRIC_TICK = re.compile(r'^(?:Put\s+a\s+tick\b|Tick\s+(?:the|one)\b|'
                         r'Zaznacz\s*\(|Odpowiedzi\s+zaznacz\b)', re.I)
# The tick, as the SEC's Wingdings subset leaves it in the text layer. U+F0FC
# is what pymupdf returns where extract-scheme.py's glyph fold prints "✓", and
# U+F0B7 is the same font's bullet. Left out of the bullet class, every answer
# in the four Ordinary schemes ships with a private-use glyph welded to its
# front, which the build's own broken-glyph gate refuses.
TICK = re.compile('^[\uf0fc\u2713\u2714]$')
BULLET = re.compile('^[‐‑‒–—•●▪✓✔\uf0fc\uf0b7\uf0a7\uf0d8-]\s*')
PAGE_ONLY = re.compile(r'^\d{1,3}$')
FURNITURE = re.compile(r'^(?:Leaving\s+Certificate|Coimisi[úu]n|State\s+Examinations|'
                       r'Marking\s+Scheme|Polish\s*$|Higher\s+Level\s*$|'
                       r'Ordinary\s+Level\s*$)', re.I)


TF_TRUE = re.compile(r'^(?:Prawda|True)$', re.I)
TF_FALSE = re.compile(r'^(?:Fa[lł]sz|False)$', re.I)
# How far a tick may stand from the left edge of the column word above it and
# still belong to that column. Measured: the true/false ticks in the corpus sit
# between 6 and 17 points right of their own heading and never within 40 of the
# other one.
COLUMN_TOL = 40.0
# A tick only answers something when it stands in a right-hand column of the
# page. The SEC's Ordinary schemes set the SAME Wingdings glyph as the bullet
# in front of every ordinary marking point, at x≈92-118, so without a floor
# every answer in those files would be read as a verdict.
TICK_MIN_X = 300.0
# A row that is only a reference to the passage — "(akapit 5)" — is the tail of
# the question, not an answer, and the marks printed beside it are the ASK's
# tariff. Kept as an answer it cost 2024 Higher Q1(d) both its parts: the ask
# read as unpriced while its price sat on a marking point that says nothing.
REF_ONLY = re.compile(r'^\((?:akapit\w*|akapity|paragraphs?|sections?|'
                      r'cz[eę][sś][cć]\w*|p)\b[^)]*\)$', re.I)


def _tf_header(row):
    """(true_x, false_x, label_pair) if this row heads a true/false table."""
    true_x = next((x for x, t in row.cells if TF_TRUE.match(t)), None)
    false_x = next((x for x, t in row.cells if TF_FALSE.match(t)), None)
    if true_x is None or false_x is None:
        return None
    labels = (next(t for _x, t in row.cells if TF_TRUE.match(_x and t or t)),
              next(t for _x, t in row.cells if TF_FALSE.match(t)))
    return (true_x, false_x, labels)


def _verdict(row, header):
    """Which column this row's tick stands in — the answer, in the SEC's word.

    A true/false ask is answered GRAPHICALLY: the scheme prints the statement
    and a tick, and nothing in the words says which of the two it is. The
    column does, and the column is the only place it is written down.
    """
    if header is None:
        return None
    true_x, false_x, labels = header
    tick = next((x for x, t in row.cells
                 if TICK.fullmatch(t) and x >= TICK_MIN_X), None)
    if tick is None:
        return None
    d_true, d_false = abs(tick - true_x), abs(tick - false_x)
    if min(d_true, d_false) > COLUMN_TOL:
        return None
    return labels[0] if d_true <= d_false else labels[1]


class Ask:
    """One priced ask of a marking scheme."""

    __slots__ = ('section', 'q', 'letter', 'roman', 'cue', 'directive', 'count',
                 'per', 'total', 'notation', 'answers', 'fault', 'page',
                 'open_list', 'stem', 'ticks', 'steps', 'part')

    def __init__(self, section, q, letter, roman, cue, page):
        self.section, self.q = section, q
        self.letter, self.roman = letter, roman
        self.cue, self.page = cue, page
        self.directive = None
        self.count = self.per = self.total = None
        self.notation = ''
        self.answers = []
        self.fault = None
        self.open_list = False
        self.stem = ''
        # (statement, verdict, marks) for every row of a true/false table this
        # ask holds. The verdict is read from the COLUMN the tick stands in.
        self.ticks = []
        # A DESCENDING ladder, where the scheme pays the first answer more than
        # the ones after it: 2021 prices "3 punkty za jeden przykład, po 1
        # punkcie za każdy następny" over a printed total of 5, which is
        # 3 + 1 + 1. Carried as the steps the SEC printed, never flattened to
        # an average — the deck's own group model has perOptionSteps for it.
        self.steps = None
        # PART-CREDIT rungs: a shorter form of the answer above, priced BELOW
        # the ask's own rate. The SEC prints them under an "or" — "hide in the
        # woods so that no one can find him / or / hide in the woods (1 mark)"
        # on a two-mark ask — and they are not things a student may claim
        # beside the full answer. Kept, and disclosed on the card as a note,
        # because the deck has no row kind for a rung worth less than the row
        # above it (see fr_scheme, which reached the same conclusion).
        self.part = []

    @property
    def key(self):
        """The paper's own address — see pl_paper.Ask.key, which this mirrors."""
        return (self.section, self.q, self.letter, self.roman)

    def ref_tail(self):
        tail = f'Q{self.q}' if self.q is not None else 'Q'
        if self.letter:
            tail += f'({self.letter})'
        if self.roman:
            tail += f'({self.roman})'
        return tail

    def __repr__(self):
        return f'Ask({self.key} {self.notation!r} {len(self.answers)} answers)'


class PlScheme:
    def __init__(self, year, level, subject=SUBJECT):
        self.year, self.level, self.subject = year, level, subject
        self.path = scheme_path(year, level, subject)
        if self.path is None:
            raise FileNotFoundError(f'no Polish scheme for {year} {level}')
        self.rows = read_rows(self.path)
        self.letter_x = self._letter_column()
        self.grid_lines = []
        self._asks = self._walk_2021() if year <= 2021 else self._walk()
        _walk_down_splits(self._asks)

    def _letter_column(self):
        """Where a part LETTER is printed, PER QUESTION, from the markers that
        cannot lie.

        Per question, because the SEC's own table cells move: the 2024 Ordinary
        scheme sets Zadanie 1's letters at x=78, Zadanie 2's at x=64 and
        Zadanie 3's at x=57 in one file. A single file-wide column took the
        middle of the three, put Zadanie 1's letters outside its window, and
        every letter from (d) onward was read as body text — four asks lost
        their marker, inherited the next ask's directive and then reported a
        tariff disagreeing with itself.

        a-h and j-l are letters and nothing else; only "(i)" can be read two
        ways, and it has to pass the sequence test as well.
        """
        by_q, inside, q = {}, False, None
        for row in self.rows:
            if UNIT_READING.match(row.text) or PART_2021.match(row.text):
                inside, q = True, None
                continue
            if UNIT_WRITING.match(row.text) or UNIT_LISTENING.match(row.text) \
                    or APPENDIX.match(row.text):
                inside = False
                continue
            if not inside:
                continue
            head = Q_HEAD.match(row.text)
            if head:
                q = int(head.group(1))
                continue
            if re.match(r'^\(?\s*[a-hj-l]\s*\)\s', row.text):
                by_q.setdefault(q, []).append(round(row.x))
        self.letter_x_by_q = {k: max(set(v), key=v.count)
                              for k, v in by_q.items()}
        every = [x for v in by_q.values() for x in v]
        return max(set(every), key=every.count) if every else 56.7

    def _column_for(self, q):
        return self.letter_x_by_q.get(q, self.letter_x)

    def _is_letter(self, x, prev_letter, q=None):
        return x <= self._column_for(q) + LETTER_TOL and prev_letter == 'h'

    # --------------------------------------------------------------- walk ---
    def _walk(self):
        asks, unit, q, letter, roman = [], None, None, None, None
        current = None

        def close():
            nonlocal current
            if current is not None:
                _price(current)
                asks.append(current)
                current = None

        for row in self.rows:
            text = row.text
            if APPENDIX.match(text):
                break
            if PAGE_ONLY.match(text) or FURNITURE.match(text):
                continue
            if UNIT_READING.match(text):
                close()
                unit, q, letter, roman = 'A', None, None, None
                continue
            if UNIT_WRITING.match(text):
                close()
                unit, q, letter, roman = 'B', None, None, None
                continue
            if UNIT_LISTENING.match(text):
                close()
                unit, q, letter, roman = 'L', None, None, None
                continue
            if unit == 'B':
                self.grid_lines.append(text)
                continue
            if unit is None:
                continue
            if unit == 'L':
                lh = LISTEN_HEAD.match(text)
                if lh:
                    close()
                    self._listen_section = lh.group(1).upper()
                    q = letter = roman = None
                    continue
            head = Q_HEAD.match(text)
            if head and unit == 'A':
                close()
                q, letter, roman = int(head.group(1)), None, None
                continue
            section = ('A' if unit == 'A'
                       else f'L{getattr(self, "_listen_section", "A")}')
            if unit == 'L':
                nm = NUMBERED.match(text)
                if nm:
                    close()
                    q, letter, roman = int(nm.group(1)), None, None
                    rest = nm.group(2)
                    inner = ROMAN.match(rest)
                    if inner:
                        roman, rest = inner.group(1).lower(), inner.group(2)
                    current = Ask(section, q, None, roman, rest, row.page)
                    _head_tariff(current)
                    continue
            if q is None and unit == 'A':
                continue
            rm = ROMAN.match(text)
            lm = LETTER.match(text)
            marker = None
            header = _tf_header(row)
            if header is not None:
                self._tf = header
                continue
            column = self._column_for(q) if unit == 'A' else self.letter_x
            if rm and not (rm.group(1).lower() == 'i'
                           and self._is_letter(row.x, letter, q)):
                marker = ('roman', rm.group(1).lower(), rm.group(2))
            elif lm and unit == 'A' and (row.x <= column + LETTER_TOL
                                         or lm.group(1).lower() == next_letter(letter)):
                marker = ('letter', lm.group(1).lower(), lm.group(2))
            if marker:
                kind, mark, rest = marker
                close()
                if kind == 'letter':
                    letter, roman = mark, None
                    inner = ROMAN.match(rest)
                    if inner:
                        roman, rest = inner.group(1).lower(), inner.group(2)
                else:
                    roman = mark
                if kind == 'letter':
                    self._tf = None
                current = Ask(section, q, letter, roman, rest, row.page)
                _head_tariff(current)
                _absorb_tick(current, row, getattr(self, '_tf', None))
                continue
            if current is not None:
                if _absorb_tick(current, row, getattr(self, '_tf', None)):
                    continue
                _absorb(current, text)
        close()
        return asks

    # 2021: "Część I (30/70)" numbers six questions straight through, and the
    # first lists five expressions a) to e) under one rate line.
    def _walk_2021(self):
        asks, part, q, letter = [], None, None, None
        current = None
        self._rate = None

        def close():
            nonlocal current
            if current is not None:
                _price(current)
                asks.append(current)
                current = None

        for row in self.rows:
            text = row.text
            if PAGE_ONLY.match(text) or FURNITURE.match(text):
                continue
            pm = PART_2021.match(text)
            if pm:
                close()
                part, q, letter = pm.group(1).upper(), None, None
                continue
            if part is None:
                continue
            if part == 'II':
                self.grid_lines.append(text)
            nm = NUMBERED.match(text)
            lm = LETTER.match(text)
            if nm:
                close()
                q, letter = int(nm.group(1)), None
                current = Ask(part, q, None, None, nm.group(2), row.page)
                _punkty_head(current)
                continue
            if lm and q is not None and part == 'I':
                close()
                letter = lm.group(1).lower()
                current = Ask(part, q, letter, None, lm.group(2), row.page)
                _split_dash(current)
                continue
            if current is not None:
                _absorb_2021(current, text)
        close()
        # Question 1's five expressions are priced by ONE rate line above them
        # — "1 punkt za każde słowo lub wyrażenie" under a printed "(5)" — so
        # the letters inherit the rate their parent states.
        for parent in [a for a in asks if a.letter is None]:
            kids = [a for a in asks if a.q == parent.q and a.letter]
            if not kids or parent.per is None:
                continue
            for kid in kids:
                if kid.per is None:
                    kid.count, kid.per, kid.total = 1, parent.per, parent.per
                    kid.notation = f'{parent.notation} on the head of Q{parent.q}'
                    kid.directive = parent.directive
        return asks

    # ---------------------------------------------------------------- API ---
    def reading(self):
        """The leaf asks of Section A (2022+) or Część I (2021)."""
        asks = [a for a in self._asks if a.section in ('A', 'I')]
        return _leaves(asks)

    def listening(self):
        return _leaves([a for a in self._asks
                        if (a.section or '').startswith('L')])

    def all_asks(self):
        return _leaves(self._asks)

    def grid_quote(self, limit=6):
        """The band grid, in the SEC's own words, for the exclusion evidence."""
        wanted = [t for t in self.grid_lines
                  if re.search(r'Very\s+good|Coherence|Communicative|Idiomatic|'
                               r'Vocabulary|Content\s*\(C\)|Expression|'
                               r'Znajomo[sś][cć]|Sp[oó]jno[sś][cć]', t, re.I)]
        return ' · '.join(w[:120] for w in wanted[:limit])


def _walk_down_splits(asks):
    """A split printed one level up, walked down to the parts it prices.

    The SEC prices a two-part ask on its PARENT and nowhere else: 2023 Higher
    heads "(f) Wyjaśnij znaczenie podanych wyrażeń w kontekście przeczytanego
    tekstu: (2 x 2m)" and then prints "(i)" and "(ii)" with an answer under
    each and no marks beside either. The tariff for each part is stated — it is
    the "2m" of the "2 x 2m" — but it is stated one level above the ask it
    belongs to, so a reader that only looks at the ask's own rows reports "the
    scheme states no tariff" about a document that priced it.

    Walked ONLY where the split and the parts agree in number: "2 x 2m" over
    exactly two parts. Where they do not — 2022 Ordinary prices "(e) 10 marks
    (5 x 2 marks)" over SIX romans because the first is the worked example —
    each part carries its own printed mark instead, and nothing is inferred.
    """
    children = collections.defaultdict(list)
    for a in asks:
        if a.roman:
            children[(a.section, a.q, a.letter)].append(a)
    for a in asks:
        if a.roman or a.answers or a.count is None or a.per is None:
            continue
        kids = children.get((a.section, a.q, a.letter))
        if not kids or len(kids) != a.count:
            continue
        if any(kid.per is not None for kid in kids):
            continue
        for kid in kids:
            kid.count, kid.per, kid.total = 1, a.per, a.per
            kid.notation = (f'{a.notation} on the head of '
                            f'{a.ref_tail()[:-len(kid.roman) - 2]}, '
                            f'walked down to its {a.count} parts')
            if kid.ticks and not kid.answers:
                tick = kid.ticks[0]
                kid.answers = [{'text': tick['verdict'], 'marks': a.per}]


def _leaves(asks):
    has_roman = {(a.section, a.q, a.letter) for a in asks if a.roman}
    has_letter = {(a.section, a.q) for a in asks if a.letter}
    parents = {(a.section, a.q, a.letter): a for a in asks if a.roman is None}
    out = []
    for a in asks:
        if a.roman:
            parent = parents.get((a.section, a.q, a.letter))
            if parent is not None and parent is not a:
                a.stem = parent.cue
            out.append(a)
        elif a.letter:
            if (a.section, a.q, a.letter) not in has_roman:
                out.append(a)
        elif (a.section, a.q) not in has_letter \
                and (a.section, a.q, None) not in has_roman:
            out.append(a)
    return out


def _absorb(ask, text):
    """One printed row of an ask: its directive, its tariff, or an answer.

    The order of these tests is the whole reader. A row that carries a TARIFF
    and is not a directive is an answer, because in nine schemes a reprinted
    question never carries one — the SEC prints the price beside the answer or
    on the marker row, never in the middle of the question it is repeating.
    Testing "does it look like prose" instead swallowed 2022 Higher's
    "padać na kolana/podziwiać/rozpływać się w pochwałach/ (2m)" into the
    question it answers.
    """
    if RUBRIC_TICK.match(text):
        _read_tariff(ask, text)
        return
    if NOTE.match(text):
        return
    d = DIRECTIVE.match(text)
    if d:
        ask.directive = text
        count = COUNT_WORD[d.group(1).lower()]
        if ask.count is not None and ask.count != count:
            ask.fault = (f'the directive {text!r} claims {count} answer(s) and '
                         f'the tariff {ask.notation!r} prices {ask.count}')
        ask.count = ask.count if ask.fault else count
        _read_tariff(ask, text, directive_count=count)
        rest = TARIFF.sub('', text[d.end():]).strip(' :')
        if rest and not PAGE_ONLY.match(rest):
            _add_answer(ask, rest)
        return
    if ALL_OR_NOTHING.match(text):
        ask.directive = text
        ask.count = ask.count or 1
        _read_tariff(ask, text)
        return
    if TARIFF.fullmatch(text) or SUM_TARIFF.fullmatch(text) \
            or BARE_TARIFF.fullmatch(text):
        _read_tariff(ask, text)
        return
    if BULLET.match(text) or ask.answers:
        _add_answer(ask, text)
        return
    if TARIFF.search(text) or SUM_TARIFF.search(text) or BARE_TARIFF.search(text):
        _add_answer(ask, text)
        return
    # Still the question: the SEC wraps a reprinted cue over two or three rows
    # and closes it with "(akapit 4)".
    ask.cue = _norm(f'{ask.cue} {text}')


def _punkty_head(ask, text=None):
    """The 2021 head's own price: "(5)" or "(5 × 1)", printed in punkty.

    The SEC sets it in a right-hand column, so it reaches the reader either on
    the head's own row or on a row of its own beneath it; both are read.
    """
    source = ask.cue if text is None else text
    m = next((PUNKTY.match(part) for part in source.split()
              if PUNKTY.match(part)), None)
    if not m:
        return
    if text is None:
        ask.cue = _norm(ask.cue.replace(m.group(0), ' '))
    if m.group(2):
        ask.count, ask.per = int(m.group(1)), int(m.group(2))
        ask.total = ask.count * ask.per
    else:
        ask.total = int(m.group(1))
    ask.notation = m.group(0)


def _split_dash(ask):
    """The 2021 vocabulary asks print the answer on the ask's own line.

    "a) łatwy kąsek (p. 1) – przysmak, smakołyk, kawałek": the expression, the
    paragraph it comes from, an en dash, and the accepted synonyms. Split at
    the dash that follows the paragraph reference, which is the only dash on
    the line that is not inside an expression.
    """
    m = re.match(r'^(.*\((?:p\.|akapit)[^)]*\))\s*[–—-]\s*(.+)$', ask.cue)
    if not m:
        return
    ask.cue = _norm(m.group(1))
    ask.answers.append({'text': _norm(m.group(2)), 'marks': None})


def _absorb_2021(ask, text):
    """A 2021 row: the head's rate sentence, or an answer under it."""
    flat = RATE_FLAT.match(text)
    desc = RATE_DESC.match(text)
    if flat or desc:
        ask.directive = text
        if flat:
            ask.per = int(flat.group(1))
            if ask.total:
                ask.count = ask.total // ask.per
        else:
            first, rest = int(desc.group(1)), int(desc.group(2))
            ask.per = first
            if ask.total:
                steps = [first]
                while sum(steps) + rest <= ask.total:
                    steps.append(rest)
                ask.count = len(steps)
                ask.steps = steps
                ask.open_list = True
                ask.notation = (f'{ask.notation} — {first} for the first, '
                                f'{rest} for each after it')
        return
    if PUNKTY.fullmatch(text):
        _punkty_head(ask, text)
        return
    _absorb(ask, text)


def _absorb_tick(ask, row, header):
    """Record a ticked row: its statement, its verdict where there is one, and
    its price.

    Two shapes. Under a Prawda/Fałsz heading the COLUMN the tick stands in is
    the verdict. Under no heading at all — "Put a tick in the appropriate box.
    Choose one statement only." — the tick simply says THIS option is the
    right one, and the verdict is None.
    """
    verdict = _verdict(row, header)
    if verdict is None:
        if not any(TICK.fullmatch(t) and x >= TICK_MIN_X for x, t in row.cells):
            return False
        if len(_norm(row.text)) < 4:
            return False
    marks = None
    bm = BARE_TARIFF.search(row.text)
    tm = TARIFF.search(row.text)
    if tm:
        marks = int(tm.group(2)) * int(tm.group(1) or 1)
    elif bm:
        marks = int(bm.group(1))
    else:
        # 2022 Ordinary heads its true/false table's third column "marks" and
        # then prints the digit ALONE in every row of it — "✓ 2" — so a
        # pattern that needs the word finds nothing, and six asks a sitting
        # report "the scheme states no tariff" beside a printed 2.
        digit = next((t for x, t in row.cells
                      if re.fullmatch(r'\d{1,2}', t) and x > 300), None)
        if digit:
            marks = int(digit)
    statement = row.text
    for _x, cell in row.cells:
        if TICK.fullmatch(cell) or BARE_TARIFF.fullmatch(cell) \
                or TARIFF.fullmatch(cell) or cell in '-‐–':
            statement = statement.replace(cell, ' ')
    statement = _norm(BULLET.sub('', statement))
    ask.ticks.append({'statement': statement, 'verdict': verdict,
                      'marks': marks})
    return True


def _head_tariff(ask):
    """The price the Ordinary schemes print on the marker row itself.

    Higher heads an ask "(a) Narratorka znalazła nowy profil…" and prices it
    further down; Ordinary heads it "(a) 4 marks (2 x 2 marks)" and reprints
    the question on the row BELOW. Both are read here, and the tariff is taken
    out of the cue so no card's question text carries its own marks.
    """
    if TARIFF.search(ask.cue) or BARE_TARIFF.search(ask.cue) \
            or SUM_TARIFF.search(ask.cue):
        _read_tariff(ask, ask.cue)
        ask.cue = _norm(BARE_TARIFF.sub('', TARIFF.sub('', ask.cue)))


def _add_answer(ask, text):
    # Whether the SEC opened this row with a bullet, read BEFORE the bullet is
    # taken off. A bulleted row is a new marking point however it reads: 2021
    # sets "‐ skraca życie" at the head of a page and, judged on its words
    # alone — lower case, two of them — it was welded onto the answer that
    # ended the page before it.
    # A row that carries its OWN tariff is a new marking point, whatever its
    # first letter: 2025 Ordinary prints the part-credit alternative "hide in
    # the woods (1 mark)" lower case under an "or", and judged on its wording
    # alone it was welded onto the full answer above it — which then quoted a
    # sentence the scheme never printed and was refused by the build.
    opened = bool(BULLET.match(text)) or bool(
        TARIFF.search(text) or SUM_TARIFF.search(text) or BARE_TARIFF.search(text))
    marks = None
    sm = SUM_TARIFF.search(text)
    tm = TARIFF.search(text)
    bm = BARE_TARIFF.search(text)
    if sm:
        marks = int(sm.group(1)) + int(sm.group(2))
        text = SUM_TARIFF.sub('', text)
    elif tm:
        marks = int(tm.group(2)) * int(tm.group(1) or 1)
        text = TARIFF.sub('', text)
    elif bm:
        marks = int(bm.group(1))
        text = BARE_TARIFF.sub('', text)
    text = _norm(BULLET.sub('', text))
    if not text:
        return
    if re.fullmatch(r'(?:or|lub|albo|and|i)\.?', text, re.I):
        return
    # A wrapped answer continues the one above it: the SEC breaks a marking
    # point over two rows and the second half is not an answer of its own.
    # A row that starts with no bullet, opens lower case and follows an answer
    # is a continuation — the same cut the Italian reader had to make.
    if ask.answers and not opened and not _looks_new(text):
        ask.answers[-1]['text'] = _norm(f'{ask.answers[-1]["text"]} {text}')
        if marks is not None and ask.answers[-1]['marks'] is None:
            ask.answers[-1]['marks'] = marks
        return
    ask.answers.append({'text': text, 'marks': marks})


CONTINUATION = re.compile(r'^[a-ząćęłńóśźż(]')


def _looks_new(text):
    """Is this row a marking point of its own, or the tail of the one above?

    Only the shape of the first character decides, and only for rows the SEC
    opened with NO bullet: a marking point starts with a capital or a digit,
    and a wrapped line starts lower case. A word-count escape hatch was here
    too — anything over three words counted as new — and it split "Myślał, że
    będzie ochroniarzem Adama w dosłownym tego słowa znaczeniu, czyli że /
    będzie robił groźne miny." into two answers, offering half a sentence as a
    thing to claim.
    """
    return not CONTINUATION.match(text)


def _read_tariff(ask, text, directive_count=None):
    """Read the printed price, and never invent one.

    An Ordinary marker row states the ask's total and its split together —
    "(e) 10 marks (5 x 2 marks)" — so both are read and CHECKED against each
    other. A split that does not multiply out to the total the SEC printed
    beside it is a fault on the ask, not a number to pick between.
    """
    sm = SUM_TARIFF.search(text)
    if sm:
        ask.count, ask.per = 2, int(sm.group(1))
        ask.total = int(sm.group(1)) + int(sm.group(2))
        ask.notation = sm.group(0)
        return
    stated_total = None
    bm = BARE_TARIFF.search(TARIFF.sub('', text))
    if bm:
        stated_total = int(bm.group(1))
    tm = TARIFF.search(text)
    if not tm:
        if stated_total is not None and ask.per is None:
            ask.count = directive_count or ask.count or 1
            ask.total = stated_total
            ask.per = stated_total // ask.count if ask.count else stated_total
            ask.notation = bm.group(0).strip()
            if ask.per * ask.count != stated_total:
                ask.fault = (f'the printed total {stated_total} does not divide '
                             f'by the {ask.count} answers the scheme asks for')
        return
    count = int(tm.group(1)) if tm.group(1) else None
    per = int(tm.group(2))
    if directive_count is not None and count is not None and count != directive_count:
        ask.fault = (f'the directive claims {directive_count} answer(s) and the '
                     f'tariff {tm.group(0)!r} prices {count}')
    ask.count = count if count is not None else (directive_count or ask.count or 1)
    ask.per = per
    ask.total = ask.count * per
    ask.notation = tm.group(0)
    if stated_total is not None and stated_total != ask.total:
        ask.fault = (f'the scheme prints the total as {stated_total} marks and '
                     f'the split {tm.group(0)!r}, which is {ask.total}')
    ask.notation = tm.group(0)


def _take_ref_marks(ask, answer):
    """A reference row's marks belong to the ask, and its words to the cue."""
    if answer['marks'] is not None and ask.per is None:
        ask.count, ask.per, ask.total = 1, answer['marks'], answer['marks']
        ask.notation = ask.notation or f'{answer["marks"]} marks'
    if answer['text'] not in ask.cue:
        ask.cue = _norm(f'{ask.cue} {answer["text"]}')
    return True


def _price(ask):
    ask.cue = _norm(ask.cue)
    if ask.per is not None:
        rungs = [a for a in ask.answers
                 if a['marks'] is not None and a['marks'] < ask.per]
        if rungs:
            ask.part = rungs
            ask.answers = [a for a in ask.answers if a not in rungs]
    ask.answers = [a for a in ask.answers
                   if not (REF_ONLY.match(a['text'])
                           and (_take_ref_marks(ask, a) or True))]
    if ask.ticks and not ask.answers and len(ask.ticks) == 1 \
            and ask.ticks[0]['verdict']:
        tick = ask.ticks[0]
        if ask.cue and tick['statement'] and tick['statement'] not in ask.cue:
            ask.cue = _norm(f'{ask.cue} {tick["statement"]}')
        elif not ask.cue:
            ask.cue = tick['statement']
        if tick['marks'] is not None:
            ask.count, ask.per, ask.total = 1, tick['marks'], tick['marks']
            ask.notation = ask.notation or f'{tick["marks"]} marks'
        ask.answers = [{'text': tick['verdict'], 'marks': tick['marks']}]
    if ask.total is None and ask.per is not None:
        ask.total = (ask.count or 1) * ask.per
    if ask.answers and ask.per is None:
        # Every answer priced on its own line and none priced above them:
        # a true/false table. The ask is worth what its rows add up to.
        priced = [a['marks'] for a in ask.answers if a['marks'] is not None]
        if priced and len(priced) == len(ask.answers):
            ask.per = priced[0]
            ask.count = len(priced)
            ask.total = sum(priced)
            ask.notation = f'{ask.count} × {ask.per} marks, priced line by line'
    if ask.steps:
        return
    if ask.count is not None and ask.per is not None \
            and ask.total != ask.count * ask.per:
        ask.fault = (f'the printed tariff {ask.notation!r} does not multiply '
                     f'out to the {ask.total} it states')


# ----------------------------------------------------------------- the CLI ---
def sittings(subject=SUBJECT):
    out = []
    for path in sorted(glob.glob(os.path.join(schemes_dir(subject), '*.pdf'))):
        m = re.match(r'(\d{4})-(hl|ol|cl)\.pdf', os.path.basename(path))
        if m:
            out.append((int(m.group(1)), m.group(2)))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('year', nargs='?', type=int)
    ap.add_argument('level', nargs='?')
    ap.add_argument('--full', action='store_true')
    ap.add_argument('--audit', action='store_true')
    args = ap.parse_args()

    if args.audit:
        for year, level in sittings():
            S = PlScheme(year, level)
            reading = S.reading()
            priced = [a for a in reading if a.total]
            answered = [a for a in priced if a.answers]
            faults = [a for a in reading if a.fault]
            print(f'{year} {level.upper():2}  {len(reading):3} reading asks, '
                  f'{len(priced):3} priced, {len(answered):3} with stated '
                  f'answers, {len(faults)} fault(s), '
                  f'{len(S.listening()):3} listening asks')
            for a in faults[:4]:
                print(f'      FAULT {a.ref_tail()} — {a.fault}')
        return 0

    S = PlScheme(args.year, args.level)
    for a in S.all_asks():
        print(f'{a.section:4} {a.ref_tail():14} {a.notation:22} '
              f'{a.cue[:80]}')
        if args.full:
            for ans in a.answers:
                print(f'         · {ans["text"][:100]}'
                      + (f'  [{ans["marks"]}m]' if ans['marks'] else ''))
        if a.fault:
            print(f'         FAULT {a.fault}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
