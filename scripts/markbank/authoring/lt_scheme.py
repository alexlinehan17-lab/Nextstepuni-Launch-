#!/usr/bin/env python3
"""Lithuanian marking schemes — the priced answer, and the question it reprints.

    python3 scripts/markbank/authoring/lt_scheme.py 2024 hl --full
    python3 scripts/markbank/authoring/lt_scheme.py --audit

What this document is
---------------------
From 2022 a Lithuanian scheme is four documents in one file, and only two of
them answer anything:

    SECTION A Reading Comprehension (100 Marks)  <- priced answers, question
                                                   reprinted above each
    SECTION B: Written Production (80 Marks)     <- a MARKING GRID
    Listening Comprehension Test (100 Marks)     <- priced answers, but the ask
                                                   needs the recording
    APPENDIX 2 CD SCRIPT                         <- the recording, in print

Before that it is a different examination and prints none of those heads:
"I DALIS (30 /100)" holds six numbered questions on one text, "II DALIS
(30/100)" a commentary and "III DALIS (40/100)" an essay. 2021 drops the
commentary and runs "I DALIS (30/70)" and "II DALIS (40/70)".

**The tariff is a column, not a suffix.** The SEC prints "Any two of:" at x≈75
and "4 marks" at x≈480 on the SAME printed line, and pymupdf reports them as
two separate lines. Read naively the directive has no tariff and the tariff has
no ask. So the page is gathered into ROWS by baseline first, exactly as
extract-scheme.py does — which is also what keeps a card's rows traceable in
the .md the provenance gate reads.

**The tariff notation is not one notation.** Twenty-two schemes print it in
seven ways — "5 marks", "4 Marks (2 x 2)", "(2 × 5 marks)", "10 Marks (5 x 2)",
"(1 taškas)", "(5 taškai)", "6 Marks (2 x 3)" — with U+00A0 for every space
from 2023 on, and the older files price in PUNKTAI (taškai) rather than marks
because that is what the old examination awarded. All of them are read; none is
guessed at. Where a directive and a tariff disagree about how many answers are
claimable — "Any three of:" over "(2 x 2)" — the ask carries a FAULT and is
refused, never averaged.

**"(i)" is the ninth letter here too.** 2024 Higher runs Reading Comprehension
2's parts to "(k)". The scheme settles it the same way the paper does, on the
printed column plus the letter sequence. See lt_paper.LtPaper._is_letter,
whose two conditions this mirrors.

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

SUBJECT = 'lithuanian'


def schemes_dir(subject=SUBJECT):
    return os.path.join(ROOT, 'examiner-reports', subject, 'schemes')


def scheme_path(year, level, subject=SUBJECT):
    path = os.path.join(schemes_dir(subject), f'{year}-{level}.pdf')
    return path if os.path.exists(path) else None


NBSP = '   '
SYMBOL_SPACE = ''


# The subject's own mangled-glyph repair, derived by lt_glyphs.py from the
# corpus and applied HERE, before anything reaches a card. It has to be applied
# at authoring time rather than left to build-deck's global map, because that
# map — derived from Maths and Chemistry — already claims one of these
# characters for a different letter: it reads U+01A1 as "l" where the SEC's
# Lithuanian subset draws "ė". A card repaired by it would say "Baidykll,
# šmlkla" and pass every gate, since the broken-glyph test only sees characters
# no map claims.
try:
    from lt_glyphs import load as _load_glyphs
except ImportError:                                     # pragma: no cover
    sys.path.insert(0, HERE)
    from lt_glyphs import load as _load_glyphs
_GLYPHS = {}


def _glyphs(subject):
    if subject not in _GLYPHS:
        _GLYPHS[subject] = _load_glyphs(subject)
    return _GLYPHS[subject]


def _norm(text, subject=SUBJECT):
    """One printed cell, with the SEC's broken font glyphs put back."""
    table = _glyphs(subject)
    out = ''.join(' ' if c in NBSP or c in SYMBOL_SPACE else table.get(c, c)
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
LETTER_TOL = 8.0


def _roman_of(m):
    """(roman, rest) from either printed form of a roman marker."""
    if m.group(1):
        return m.group(1).lower(), m.group(2)
    return m.group(3).lower(), m.group(4)


def next_letter(current):
    return 'a' if not current else chr(ord(current) + 1)

def _i_opens_a_roman_run(rows, idx):
    """Is the "(i)" on this row the first ROMAN, or the ninth LETTER?

    The page cannot always answer it. 2024 Ordinary sets the roman "(i) Žaidimo
    lenta" at x=90.5 and, eight rows later, the LETTER "(i) What are the
    benefits of the game Kondigno?" at x=88.9 — one and a half points apart, in
    the same question, both after a printed "(h)". A column test with any
    tolerance wide enough to hold the letters of that scheme reads the first as
    a letter, files (ii) to (v) beneath it, and reports five printed asks as
    unpriced.

    What separates them is what FOLLOWS. A roman "(i)" is the head of a run and
    "(ii)" comes next; a letter "(i)" is the last of its own run and the next
    marker is a letter or nothing at all. So the rows after it are read, up to
    the next marker of either kind, and the run decides.
    """
    for row in rows[idx + 1:]:
        text = row.text
        if re.match(r'^\(\s*ii\s*\)', text, re.I):
            return True
        if re.match(r'^\(?\s*[a-l]\s*\)[\s)]', text, re.I) \
                or re.match(r'^\(\s*i{1,3}\s*\)|^\(\s*iv\s*\)', text, re.I):
            return False
    return False



def read_rows(path, subject=SUBJECT):
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
                    text = _norm(''.join(s['text'] for s in line['spans']),
                                 subject)
                    if not text:
                        continue
                    x0, y0, x1, y1 = line['bbox']
                    lines.append((x0, (y0 + y1) / 2, text))
            for block in page.get_text('dict')['blocks']:
                if block.get('type') != 0:
                    continue
                for line in block['lines']:
                    for span in line['spans']:
                        text = _norm(span['text'], subject)
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


MARKER_ONLY = re.compile(r'^\(?\s*([a-z]{1,4}|\d{1,2})\s*\)\.?$', re.I)
CELL_TOL = 12.0


def _fold_marker_rows(rows):
    """A marker printed alone in its cell belongs to the row beside it."""
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
    """A tick set half a line below the statement it marks belongs to it."""
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
    cells = [(x, text) for x, _y, text in band]
    # A tick reaches this TWICE — once inside the line that holds it and once
    # as a span of its own, so that a row whose only content is a tick survives
    # the line pass at all — and pymupdf reports the two origins a fraction of
    # a point apart. The bare copy is dropped wherever the line beside it
    # already opens with the same tick.
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
UNIT_READING = re.compile(r'^SECTION\s+A\b\s*:?\s*Reading', re.I)
UNIT_WRITING = re.compile(r'^SECTION\s+B\b\s*:?\s*Written', re.I)
UNIT_LISTENING = re.compile(r'^Listening\s+comprehension\s+test\b', re.I)
# Everything from here is the CD script — the recording in print, in the ANSWER
# document — and its speaker turns are not marking points.
APPENDIX = re.compile(r'^APPENDIX\b', re.I)
# The old examination's own parts.
# The old examination's own parts, in each of the three languages: Lithuanian
# "I DALIS", Latvian "I daļa" and Czech "Část 1". Czech numbers them in arabic
# digits where the other two use Roman numerals, and PART_NUMBER folds the two
# spellings onto one token so the census keys, the citations and every
# continuity check read the same in all three.
PART_OLD = re.compile(r'^(I{1,3})\s*(?:DALIS|da[ļl]a)\b|^[ČC]ást\s*([123])\b',
                      re.I)
PART_NUMBER = {'I': 'I', 'II': 'II', 'III': 'III',
               '1': 'I', '2': 'II', '3': 'III'}


def part_token(m):
    return PART_NUMBER[(m.group(1) or m.group(2)).upper()]

# The scheme heads each reading task with the DIGIT the paper writes as a word:
# "Reading Comprehension 1 / Pirma užduotis" — and 2026 Ordinary sets it with
# no spaces around the solidus, "Reading Comprehension 2/Antra užduotis".
Q_HEAD = re.compile(r'^Reading\s+Comprehension\s*(\d{1,2})\b', re.I)
LISTEN_HEAD = re.compile(r'^Section\s+([A-F])\b', re.I)
LETTER = re.compile(r'^\(?\s*([a-l])\s*\)\s*(.*)$', re.I)
# A roman marker, bracketed — "(iii)" — or set with a full stop after it,
# "iii.", which is how the 2022 Ordinary scheme numbers the rows of a
# true/false table. The dotted form requires the text to follow on the same
# row, so a sentence opening "i." can only be a marker.
ROMAN = re.compile(
    r'^\(\s*([iI]{1,3}|[iI][vV]|[vV][iI]{0,3}|[iI][xX]|[xX])\s*\)\s*(.*)$|'
    # The dotted form is LOWER CASE and nothing else. Case-folded it read the
    # initial of a name as a roman: 2025 Ordinary prints "(g) V. Senkutė
    # išvyko į Ameriką dirbti." and the "V." opened a fifth sub-part of an ask
    # that has none, which the census reported as a roman-gap holding only (v).
    r'^(i{1,3}|iv|vi{0,3}|ix|x)\.\s+(\S.*)$')
NUMBERED = re.compile(r'^(\d{1,2})\s*\.\s*(.*)$')
ROMANS = ['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x']

# The tariff, in every notation the twenty-two schemes print:
#   (2 × 5 marks) (1 mark)          bracketed, with the unit
TARIFF = re.compile(
    r'\(\s*(?:(\d{1,2})\s*[x×]\s*)?(\d{1,2})\s*(?:m|marks?)\s*\.?\s*\)', re.I)
# "4 Marks", "5 marks" — the ordinary form, printed in the right-hand column
# with no brackets at all.
BARE_TARIFF = re.compile(r'(?:^|\s)(\d{1,2})\s*marks?\s*\.?$', re.I)
# The SPLIT the SEC prints beside that total: "4 Marks (2 x 2)",
# "10 Marks (5 x 2)". The unit is on the total, not on the split.
SPLIT = re.compile(
    r'[\(\[]\s*(\d{1,2})\s*[x×]\s*(\d{1,2})\s*'
    r'(?:m|marks?|ta[sš]k\w*|punkt\w*|bod\w*)?\s*[\)\]]', re.I)
# The same split with NO brackets at all, which is how several sittings print
# it: "(c) Radvilė rūpinasi Gabe… (2 dalis) 2 × 5 marks" and "Put a tick (✓) in
# the appropriate boxes. 5 x 1 mark". The unit is required here — without it
# "5 x 1" would match a paragraph reference or a date — and the lookbehind
# keeps it out of a bracketed form the patterns above already read.
SPLIT_BARE = re.compile(
    r'(?<![\d(])(\d{1,2})\s*[x×]\s*(\d{1,2})\s*'
    r'(?:m\b|marks?\b|ta[sš]k\w*|punkt\w*|bod\w*)', re.I)
# The old examination prices in TAŠKAI and prints the unit every time:
# "(1 taškas)", "(5 taškai)", "(30 taškų)".
# The opening bracket is OPTIONAL because the SEC drops it: the 2018 scheme
# prices Question 1(b) "grūmoja 1 taškas)" with a closing bracket and no
# opening one, and a strict pattern reported that one ask of that sitting had
# no tariff at all beside a printed taškas.
# The three languages price in three units and bracket them two ways:
# Lithuanian "(1 taškas)", Latvian "(5 punkti)" and Czech "[5 bodů]". The unit
# is REQUIRED — a bare "(5)" in these documents is a paragraph reference as
# often as it is a price — and the opening bracket is optional because the SEC
# drops it (2018 Lithuanian prices "grūmoja 1 taškas)").
PUNKTAI = re.compile(
    r'[\(\[]?\s*(\d{1,3})\s*(?:ta[sš]k\w*|punkt\w*|bod\w*)\s*[\)\]]', re.I)

COUNT_WORD = {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6}
DIRECTIVE = re.compile(
    r'^(?:any\s+)?(one|two|three|four|five|six)\s+(?:of|items?|details?)\b\s*:?',
    re.I)
ALL_OR_NOTHING = re.compile(r'^All\s+or\s+nothing\s*:?', re.I)
# Examiner rubric, which is never an answer.
NOTE = re.compile(r'^(?:Note\s*:|N\.?B\.?\b|PASTABA\b|Pastaba\b|Svarbu\b|Penalise\b|Accept\b|Allow\b|'
                  r'When\s+the\s+correct|When\s+more\s+than|Award\b|'
                  r'Candidates?\s+must\b|If\s+no\s+point\s+of\s+view\b|'
                  r'No\s+reference\s+to\s+the\s+text\b|Serious\s+missp|'
                  r'Excess\s+material\b|General\s+observations\b|'
                  r'Mark\s+content\b|Use\s+square\s+brackets\b|'
                  r'Put\s+a\s+tick\b|Tick\s+(?:the|one)\b|'
                  r'Pa[žz]ym[eė]kite\s*\(|Atsakykite\s+į\s+klausimus\b|'
                  r'Answer\s+(?:the\s+)?questions?\b)', re.I)
# The tick instruction alone. It is rubric — never a marking point — but the
# SEC prints the ASK's tariff at the end of it, so the price is taken off it
# before the line is dropped.
RUBRIC_TICK = re.compile(r'^(?:Pa[žz]ym[eė]kite\s*\(|Put\s+a\s+tick\b|'
                         r'Tick\s+(?:the|one)\b)', re.I)
# The tick, as the SEC's Wingdings subset leaves it in the text layer.
TICK = re.compile('^[✓✔]$')
# The bullet, in every glyph the SEC's Wingdings and Symbol subsets leave in
# the text layer as well as the real ones. U+F0D8 is the arrowhead that opens
# every part-credit rung under a "Svarbu:" heading — without it those rungs
# read as continuations of the answer above them and 2023 Higher Q2(h)
# reported no tariff at all.
BULLET = re.compile('^[‐‑‒–—•●▪✓✔\uf0d8\uf0b7\uf0a7-]\s*')
PAGE_ONLY = re.compile(r'^\d{1,3}$')
# A rank of bare numbers printed across one row — the column heads of a
# matching task's answer boxes, never an ask.
NUMBER_RANK = re.compile(r'\d{1,2}\s*\.?(?:\s+\d{1,2}\s*\.?)+')
FURNITURE = re.compile(r'^(?:Leaving\s+Certificate|Coimisi[úu]n|State\s+Examinations|'
                       r'Marking\s+Scheme|Lithuanian\s*$|Higher\s+Level\s*$|'
                       r'Ordinary\s+Level\s*$|MARKING\s+GRID\b|'
                       r'Annotation\b|Not\s+all\s+responses\b)', re.I)

TF_TRUE = re.compile(r'^(?:Teisingas|Teisingai|True)$', re.I)
TF_FALSE = re.compile(r'^(?:Neteisingas|Neteisingai|False)$', re.I)
COLUMN_TOL = 40.0
# A tick only answers something when it stands in a right-hand column of the
# page: the SEC also sets the same glyph as a BULLET in front of ordinary
# marking points, at the left margin.
TICK_MIN_X = 250.0
# A row that is only a reference to the passage — "(2 dalis)" — is the tail of
# the question, not an answer, and the marks printed beside it are the ASK's
# tariff.
REF_ONLY = re.compile(r'^\(\s*\d{1,2}\s*dal\w*\s*\)$', re.I)


def _tf_header(row):
    """(true_x, false_x, label_pair) if this row heads a true/false table."""
    true_x = next((x for x, t in row.cells if TF_TRUE.match(t)), None)
    false_x = next((x for x, t in row.cells if TF_FALSE.match(t)), None)
    if true_x is None or false_x is None:
        return None
    labels = (next(t for _x, t in row.cells if TF_TRUE.match(t)),
              next(t for _x, t in row.cells if TF_FALSE.match(t)))
    return (true_x, false_x, labels)


def _verdict(row, header):
    """Which column this row's tick stands in — the answer, in the SEC's word."""
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
                 'open_list', 'stem', 'ticks', 'steps', 'part', 'split',
                 'columns')

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
        self.ticks = []
        self.steps = None
        self.part = []
        # Whether the tariff the SEC printed states its own SPLIT ("4 Marks
        # (2 x 2)", "(2 × 5 marks)") rather than a bare total. See _absorb.
        self.split = False
        # Printed rows of an answer block the SEC set in two columns, banked
        # whole because a column cannot be read one row at a time. See _price.
        self.columns = []

    @property
    def key(self):
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


class LtScheme:
    def __init__(self, year, level, subject=SUBJECT):
        self.year, self.level, self.subject = year, level, subject
        self.path = scheme_path(year, level, subject)
        if self.path is None:
            raise FileNotFoundError(f'no Lithuanian scheme for {year} {level}')
        self.rows = read_rows(self.path, subject)
        # Read from the PAGE, never from the year — see LtPaper._era, which
        # makes the same call on the question paper. Latvian and Czech never
        # left the old examination.
        if any(UNIT_READING.match(r.text) for r in self.rows):
            self.era = 'new'
        else:
            parts = {part_token(PART_OLD.match(r.text)) for r in self.rows
                     if PART_OLD.match(r.text)}
            self.era = 'old2' if len(parts) == 2 else 'old3'
        self.letter_x_by_q = {}
        self.letter_x = self._letter_column()
        self.grid_lines = []
        self._listen_section = 'A'
        self._tf = None
        self._asks = self._walk() if self.era == 'new' else self._walk_old()
        _walk_down_splits(self._asks)

    def _letter_column(self):
        """Where a part LETTER is printed, PER QUESTION, from the markers that
        cannot lie — lt_paper._letter_column's rule, applied to the scheme."""
        by_q, inside, q = {}, False, None
        for row in self.rows:
            if UNIT_READING.match(row.text) or PART_OLD.match(row.text):
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

    def _is_letter(self, x, prev_letter, q=None, idx=None):
        """Is this "(i)" the ninth letter or the first roman? — see
        _i_opens_a_roman_run, which is what settles it where the column
        cannot."""
        if idx is not None and _i_opens_a_roman_run(self.rows, idx):
            return False
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

        for idx, row in enumerate(self.rows):
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
            section = 'A' if unit == 'A' else f'L{self._listen_section}'
            if q is None and unit == 'A':
                continue
            rm = ROMAN.match(text)
            lm = LETTER.match(text)
            nm = NUMBERED.match(text)
            marker = None
            header = _tf_header(row)
            if header is not None:
                self._tf = header
                continue
            column = self._column_for(q) if unit == 'A' else self.letter_x
            # A numbered row under a letter is a sub-ask, the way it is in the
            # paper: the scheme numbers a true/false table's statements "1." to
            # "5." and prices the letter above them "(3 x 1)".
            if unit == 'L' and nm and not lm and not rm and q is None:
                close()
                q, letter, roman = int(nm.group(1)), None, None
                rest = nm.group(2)
                inner = LETTER.match(rest)
                if inner:
                    letter, rest = _roman_of(inner)[0], _roman_of(inner)[1]
                current = Ask(section, q, letter, roman, rest, row.page)
                _head_tariff(current)
                continue
            if NUMBER_RANK.fullmatch(text):
                # "1. 2. 3." — the SEC's own column numbers over the answer
                # boxes of a sentence-matching task, printed as one row above
                # the letters that answer them. Read as a sub-ask it opened an
                # empty Q2(e)(1) and left the paper's (2) and (3) reporting as
                # unpriced.
                continue
            if unit == 'A' and nm and letter is not None and not rm \
                    and not lm:
                close()
                roman = nm.group(1)
                current = Ask(section, q, letter, roman, nm.group(2), row.page)
                _head_tariff(current)
                _absorb_tick(current, row, self._tf)
                continue
            if rm and not (_roman_of(rm)[0] == 'i'
                           and self._is_letter(row.x, letter, q, idx)):
                marker = ('roman', _roman_of(rm)[0], _roman_of(rm)[1])
            elif lm and (row.x <= column + LETTER_TOL
                         or lm.group(1).lower() == next_letter(letter)):
                marker = ('letter', lm.group(1).lower(), lm.group(2))
            if marker:
                kind, mark, rest = marker
                close()
                if kind == 'letter':
                    letter, roman = mark, None
                    inner = ROMAN.match(rest)
                    if inner:
                        roman, rest = _roman_of(inner)[0], _roman_of(inner)[1]
                    self._tf = None
                else:
                    roman = mark
                current = Ask(section, q, letter, roman, rest, row.page)
                _head_tariff(current)
                _absorb_tick(current, row, self._tf)
                continue
            if current is not None:
                if _absorb_tick(current, row, self._tf):
                    continue
                if _two_columns(row) or (current.columns and row.cells
                                         and not _tariff_only(text)
                                         and not NOTE.match(text)
                                         and not Q_HEAD.match(text)):
                    # The SEC sets this ask's answers in TWO COLUMNS and the
                    # row banding hands both back interleaved: 2025 Higher
                    # prints the AGREE menu beside the DISAGREE one and the
                    # rows read "• AGREE. He gets used to running • DISAGREE.
                    # He doesn't get the ball. He / faster, develops strategies
                    # to / falls down a lot still…", with every sentence cut in
                    # half. 2024 Higher Q1(h) does the same with single words —
                    # "• Dingdavo • Lesdavo".
                    #
                    # Both are recovered the same way and neither is guessed
                    # at: the printed CELLS are kept with their x, banked until
                    # the ask closes, and then read down each column before
                    # across. Every character on the card is still the SEC's,
                    # in the order the SEC set it. Once a two-column row has
                    # opened the ask, the rows under it are its continuations
                    # and are banked too — they carry no bullet of their own.
                    current.columns.append(row)
                    continue
                _absorb(current, text)
        close()
        return asks

    # The old examination: "I DALIS (30 /100)" numbers six questions straight
    # through, and the first lists five expressions a) to e), each priced.
    def _walk_old(self):
        asks, part, q, letter = [], None, None, None
        current = None

        def close():
            nonlocal current
            if current is not None:
                _price(current)
                asks.append(current)
                current = None

        for i, row in enumerate(self.rows):
            text = row.text
            if PAGE_ONLY.match(text) or FURNITURE.match(text):
                continue
            pm = PART_OLD.match(text)
            if pm:
                close()
                part, q, letter = part_token(pm), None, None
                continue
            if part is None:
                continue
            if part in ('II', 'III') and self.era == 'old3' and part == 'III':
                self.grid_lines.append(text)
            if part == 'II' and self.era == 'old2':
                self.grid_lines.append(text)
            nm = NUMBERED.match(text)
            lm = LETTER.match(text)
            # A numbered row opens a question only where it CONTINUES the run.
            # The old scheme answers Question 2 with a numbered list of its own
            # ("1. Gyvybė – sveikas juokas, tikri veidai"), and it closes
            # I DALIS with a PASTABA numbering the four qualities the essay
            # parts are judged on. Read as questions those gave 2012 seventeen
            # asks in a part that prints ten, four of them holding an essay
            # criterion where an answer belongs.
            #
            # The run alone is not enough: 2012 answers Question 2 with its own
            # numbered list of five, and its third item "3. Tikruma – tikros
            # vertybės…" both continues the run and stands where Question 3
            # would. What separates them is the PRICE — every question of
            # I DALIS is priced in taškai and no item of an answer list is —
            # so a numbered row opens a question only where a price is printed
            # before the next numbered row.
            #
            # The run test is ">" and not "== q + 1" on purpose. The 2021
            # scheme prints NO tariff beside its Question 2 — the paper prints
            # "(5 taškai)" and the scheme does not — so that question cannot
            # be opened here at all, and an exact-successor test then refused
            # Questions 3 to 6 as well and lost five of that sitting's ten
            # asks to one missing bracket. A question the scheme never priced
            # is reported by lt_flags as an unpriced ask, which is the truth
            # about the document, rather than swallowing the rest of the part.
            if nm and part == 'I' and int(nm.group(1)) > (q or 0) \
                    and _priced_before_next_number(self.rows, i):
                close()
                q, letter = int(nm.group(1)), None
                rest = nm.group(2)
                # The SEC glues a question number and its first LETTER onto
                # one printed row — see lt_paper, which reads the same page.
                inner = LETTER.match(rest)
                if inner:
                    letter, rest = _roman_of(inner)[0], _roman_of(inner)[1]
                current = Ask(part, q, letter, None, rest, row.page)
                _punktai_head(current)
                continue
            if lm and q is not None and part == 'I':
                close()
                letter = lm.group(1).lower()
                current = Ask(part, q, letter, None, lm.group(2), row.page)
                _punktai_head(current)
                if current.total is None:
                    # Only where the letter's own row carries NO price. Where
                    # it does, the dash is inside the expression the ask asks
                    # about and the answer is on the row below: 2021 sets
                    # "b) aš pati – ir be ribų, ir be krantų (1 taškas)", all
                    # of which is the quotation, and splitting it there made
                    # the card ask about "aš pati" and offer the rest of the
                    # SEC's own question as its answer.
                    _split_dash(current)
                continue
            if part == 'II' and self.era == 'old3':
                # The commentary task: one ask, keyed by its part alone, whose
                # every printed row belongs to it.
                if current is None:
                    current = Ask(part, None, None, None, text, row.page)
                else:
                    _absorb_old(current, text)
                continue
            if current is not None and part == 'I':
                _absorb_old(current, text)
        close()
        # Question 1's five expressions are priced one taškas each on their own
        # rows; the head above them prices nothing, so nothing is inherited.
        return asks

    # ---------------------------------------------------------------- API ---
    def reading(self):
        """The leaf asks of Section A (2022+) or I DALIS (before it)."""
        return _leaves([a for a in self._asks if a.section in ('A', 'I')])

    def listening(self):
        return _leaves([a for a in self._asks
                        if (a.section or '').startswith('L')])

    def all_asks(self):
        return _leaves(self._asks)

    def grid_quote(self, limit=6):
        """The band grid, in the SEC's own words, for the exclusion evidence."""
        wanted = [t for t in self.grid_lines
                  if re.search(r'Very\s+good|coherence|communicative|'
                               r'Vocabulary|Content\s+and\s+Communication|'
                               r'Language\b|argumentation|register', t, re.I)]
        return ' · '.join(w[:120] for w in wanted[:limit])


def _walk_down_splits(asks):
    """A split printed one level up, walked down to the parts it prices.

    The SEC prices a table on its PARENT and nowhere else: 2024 Ordinary heads
    "(h) Pažymėkite (✓) teisingus ir neteisingus teiginius (3 dalis) 3 Marks
    (3 x 1)" and then prints three numbered statements with a tick against each
    and no marks beside any of them. The tariff for each row is stated — it is
    the "1" of the "3 x 1" — but it is stated one level above the ask it
    belongs to, so a reader that only looks at the ask's own rows reports "the
    scheme states no tariff" about a document that priced it.

    Walked ONLY where the split and the parts agree in number. Where they do
    not, each part carries its own printed mark instead and nothing is
    inferred.
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
            kid.notation = (f'{a.notation} on the head of {a.ref_tail()}, '
                            f'walked down to its {a.count} parts')
            if kid.ticks and not kid.answers:
                tick = kid.ticks[0]
                if tick['verdict']:
                    kid.answers = [{'text': tick['verdict'], 'marks': a.per}]


def _priced_before_next_number(rows, i):
    """Is a taškai price printed under this numbered row, before the next one?

    Scanned over the rows themselves rather than assumed, because the SEC puts
    the price in three places: on the question's own row, alone in the
    right-hand column beneath it, and — for Question 1, which prices its five
    lettered expressions one taškas each — on the rows of the letters below.
    """
    for row in rows[i:]:
        if row is not rows[i] and NUMBERED.match(row.text):
            return False
        if PART_OLD.match(row.text):
            return False
        if PUNKTAI.search(row.text):
            return True
    return False


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
    """One printed row of an ask: its directive, its tariff, or an answer."""
    if RUBRIC_TICK.match(text):
        _read_tariff(ask, text)
        return
    if NOTE.match(text):
        # NEVER the ask's price. The SEC closes a discussion ask with
        # "No reference to the text – minus 1 Mark", and reading that line's
        # number as a tariff priced 2022 Higher Q1(i) at one mark against the
        # "(2 × 5 marks)" printed on its own head — a deduction read as the
        # award it is subtracted from.
        return
    d = DIRECTIVE.match(text)
    if d:
        ask.directive = text
        count = COUNT_WORD[d.group(1).lower()]
        # The DIRECTIVE says how many answers may be claimed only where the
        # scheme did not already print a SPLIT. Where it printed one the split
        # is the claim and the directive word names the menu the answers come
        # from: 2022 Ordinary heads Q1(c) "(2 × 3 marks)", writes "One of:"
        # over a list of nine, and the PAPER asks for two ("Parašykite du
        # dalykus"). Two documents say two and one loose word says one, so the
        # printed split wins and nothing is averaged.
        #
        # Where only a bare TOTAL was printed the directive is the only count
        # there is, and dividing the total by it is arithmetic on two printed
        # numbers rather than a guess: "(c) … 4 marks" over "Any two of:" is
        # two answers at two marks. A total that does not divide by the
        # directive's count is a FAULT and the ask is refused.
        if ask.split:
            if ask.count != count:
                ask.notation += f' (the scheme also writes "{text.strip()}")'
        elif ask.total is not None and count:
            if ask.total % count == 0:
                ask.count, ask.per = count, ask.total // count
            else:
                ask.fault = (f'the scheme prices this ask {ask.total} marks and '
                             f'writes {text.strip()!r} over it, and {ask.total} '
                             f'does not divide by {count}')
        else:
            ask.count = count
            _read_tariff(ask, text, directive_count=count)
        rest = TARIFF.sub('', text[d.end():]).strip(' :')
        rest = BARE_TARIFF.sub('', rest).strip(' :')
        if rest and not PAGE_ONLY.match(rest):
            _add_answer(ask, rest)
        return
    if ALL_OR_NOTHING.match(text):
        ask.directive = text
        ask.count = ask.count or 1
        _read_tariff(ask, text)
        return
    if _tariff_only(text):
        # A row that is nothing but a price. The SEC sets it in the right-hand
        # column of the page, on its own baseline, whenever the question it
        # belongs to has wrapped: 2024 Ordinary prints "(e) Suderinkite
        # sakinius … (2 dalis)" and then "6 Marks (3 x 2)" at x=465 on the row
        # below. Tested by SUBTRACTION rather than by one pattern, because the
        # row carries the total and its split together and no single pattern
        # matches both at once — which is how three asks a sitting reported no
        # tariff beside a printed one.
        _read_tariff(ask, text)
        return
    if BULLET.match(text) or ask.answers:
        _add_answer(ask, text)
        return
    if (TARIFF.search(text) or BARE_TARIFF.search(text)) \
            and ask.total is None and not ask.answers:
        # The reprinted question WRAPS, and the SEC sets the price in the
        # right-hand column of its last row: "(h) Su kokiais miesto
        # bendruomenės nariais bendrauja jaunimo centro darbuotojai? /
        # Parašykite du bendruomenės narius. (3 dalis) 4 marks". Read as an
        # answer — which is what a rule that says "a tariff means an answer"
        # does, and which is the right rule for Polish — the second half of
        # the question became the first thing on the card's answer menu and
        # the ask itself reported no tariff at all. Six a sitting in 2023.
        _read_tariff(ask, text)
        rest = _strip_tariffs(text)
        if rest:
            ask.cue = _norm(f'{ask.cue} {rest}')
        return
    if TARIFF.search(text) or BARE_TARIFF.search(text):
        _add_answer(ask, text)
        return
    if ask.total is not None:
        # The question ENDS where its price is printed. Everything after it
        # belongs to the answer, bulleted or not — and 2022 does not bullet:
        # it sets "(d) Ką reiškia žodis „įsižeidusi“? (2 dalis) 5 marks" and
        # then "Įskaudinta" on the row below with nothing in front of it.
        # Judged on its punctuation that word read as more of the question,
        # and seventeen asks reported a price with no answer under it.
        _add_answer(ask, text)
        return
    # Still the question: the SEC wraps a reprinted cue over two or three rows
    # and closes it with "(2 dalis)".
    ask.cue = _norm(f'{ask.cue} {text}')


def _strip_tariffs(text):
    """Every printed price taken out of a line, in the ONLY order that works.

    BARE_TARIFF is anchored to the end of the line, because "4" on its own is
    a paragraph reference and "4 marks" at the end of a row is a price — so it
    has to be applied AFTER the split beside it is removed. Applied first it
    matched nothing in "6 Marks (3 x 2)", and that row then failed every test
    for a price and was read as an answer, leaving three printed asks of 2024
    Ordinary reporting no tariff and their card question carrying "4 Marks" in
    its own words.
    """
    out = PUNKTAI.sub('', TARIFF.sub('', SPLIT_BARE.sub('', SPLIT.sub('', text))))
    return _norm(BARE_TARIFF.sub('', out))


def _tariff_only(text):
    """Is this printed row nothing but a tariff?"""
    rest = _strip_tariffs(text)
    return bool(text) and not re.sub(r'[\s.,:;()x×-]+', '', rest) \
        and (PUNKTAI.search(text) or SPLIT.search(text)
             or SPLIT_BARE.search(text) or BARE_TARIFF.search(text)
             or TARIFF.search(text))


DASH_SPLIT = re.compile(r'^(.{1,80}?)\s+[–—]\s+(\S.+)$')


def _split_dash(ask):
    """The 2010 scheme prints the answer on the ask's own row, after a dash.

    "a) vamzdis – funkcionali, tuščiavidurė struktūra, kuria gali kas nors
    tekėti." — the expression, an en dash, and its gloss. Split at that dash,
    which is the only one on the row: the expressions are single words or
    quoted phrases and never contain one. Left joined, five asks a sitting
    reported a price with no answer under it and their card question would
    have carried its own answer.
    """
    m = DASH_SPLIT.match(ask.cue)
    if not m or ask.answers:
        return
    ask.cue = _norm(m.group(1))
    ask.answers.append({'text': _norm(m.group(2)), 'marks': None})


def _absorb_old(ask, text):
    """A row of the old examination: the answer, or more of the question.

    The old scheme prints no bullets and no directives. It reprints the
    question, prices it in taškai, and sets its answer as continuous prose
    over as many rows as it needs — so the rows of an answer are joined back
    into the one marking point the SEC printed rather than cut at every
    capital letter.

    WHERE the price is printed moved over the decade and both places are read.
    2020 sets it on the question's own row — "a) buitinė lietuvių šneka
    (1 taškas)" — and 2012 sets it on the ANSWER's — "a) liūtis" then "Staiga
    užeinantis ir praeinantis labai smarkus lietus (1 taškas)". A reader that
    only knew the first treated 2012's answer as more of the question and
    reported four of its ten asks as unanswered.
    """
    if NOTE.match(text) or PAGE_ONLY.match(text):
        return
    if PUNKTAI.fullmatch(text):
        _read_tariff(ask, text)
        return
    pm = PUNKTAI.search(text)
    if pm:
        _read_tariff(ask, text)
        body = _norm(PUNKTAI.sub('', text))
        if body:
            ask.answers.append({'text': body, 'marks': None})
        return
    if ask.total is None and not ask.answers:
        ask.cue = _norm(f'{ask.cue} {text}')
        return
    if ask.answers:
        ask.answers[-1]['text'] = _norm(f'{ask.answers[-1]["text"]} {text}')
        return
    ask.answers.append({'text': _norm(BULLET.sub('', text)), 'marks': None})


def _absorb_tick(ask, row, header):
    """Record a ticked row: its statement, its verdict where there is one, and
    its price."""
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
    statement = row.text
    for _x, cell in row.cells:
        if TICK.fullmatch(cell) or BARE_TARIFF.fullmatch(cell) \
                or TARIFF.fullmatch(cell) or cell in '-‐–':
            statement = statement.replace(cell, ' ')
    statement = _norm(BULLET.sub('', statement))
    ask.ticks.append({'statement': statement, 'verdict': verdict,
                      'marks': marks})
    return True


def _read_columns(ask):
    """Read a banked two-column answer block DOWN each column, then across.

    The boundary is measured, not assumed: the bullets the SEC printed fall
    into two clusters of x, and the midpoint between the leftmost and the
    rightmost of them separates a cell of the left column from a cell of the
    right. A wrapped continuation carries no bullet and sits a few points in
    from its own column's, which the same boundary still places correctly.
    """
    bullets = sorted(x for row in ask.columns for x, t in row.cells
                     if BULLET.match(t))
    if len(bullets) < 2:
        ask.columns = []
        return
    boundary = (bullets[0] + bullets[-1]) / 2
    left, right = [], []
    for row in sorted(ask.columns, key=lambda r: (r.page, r.y)):
        for x, text in sorted(row.cells, key=lambda c: c[0]):
            (left if x < boundary else right).append(text)
    for column in (left, right):
        joined = _norm(' '.join(column))
        if not joined:
            continue
        # Cut at the SEC's own bullets, which is where one marking point ends
        # and the next begins inside a column.
        for piece in re.split(r'\s*(?=[•●▪‐‑‒–—])', joined):
            piece = piece.strip()
            if piece:
                _add_answer(ask, piece)
    ask.columns = []


def _two_columns(row):
    """Does this printed row hold two BULLETED columns rather than one?"""
    bullets = [x for x, t in row.cells if BULLET.match(t)]
    return len(bullets) > 1 and max(bullets) - min(bullets) > 100


def _head_tariff(ask):
    """The price the SEC prints on the reprinted question's own row.

    "(a) Kodėl pasakotoja išėjo pro duris pasiėmusi tik raktus? (1 dalis)
    5 marks" — the tariff sits in the right-hand column of the same printed
    row, and it is taken out of the cue so no card's question text carries its
    own marks.
    """
    if TARIFF.search(ask.cue) or BARE_TARIFF.search(ask.cue) \
            or SPLIT.search(ask.cue) or SPLIT_BARE.search(ask.cue) \
            or PUNKTAI.search(ask.cue):
        _read_tariff(ask, ask.cue)
        ask.cue = _strip_tariffs(ask.cue)


def _punktai_head(ask):
    """The old examination's own price: "(1 taškas)", "(5 taškai)"."""
    if PUNKTAI.search(ask.cue):
        _read_tariff(ask, ask.cue)
        ask.cue = _norm(PUNKTAI.sub('', ask.cue))


def _add_answer(ask, text):
    # Whether the SEC opened this row with a bullet, read BEFORE the bullet is
    # taken off — a bulleted row is a new marking point however it reads.
    #
    # A row carrying its OWN tariff is usually a new marking point too, but not
    # always: the SEC wraps a long answer and the marks land at the end of its
    # SECOND row — "• Jose pirkėjas pats produktus pasveria, įsipila ir įsideda
    # į savo atsineštus daugkartinio / naudojimo indus. 5 marks" — so the tail
    # opened a marking point of its own reading "naudojimo indus.", the ask's
    # answers stopped agreeing on their prices, and 2023 Higher Q2(d) reported
    # no tariff at all. The tail is told from a real new point by two things
    # the page states: it opens lower case, and the point above it has not been
    # priced yet. A part-credit rung under a priced answer satisfies neither.
    stripped = _norm(BULLET.sub('', _strip_tariffs(text)))
    has_tariff = bool(TARIFF.search(text) or BARE_TARIFF.search(text))
    opened = bool(BULLET.match(text))
    if not opened and has_tariff:
        opened = (_looks_new(stripped) or not ask.answers
                  or ask.answers[-1]['marks'] is not None)
    marks = None
    tm = TARIFF.search(text)
    bm = BARE_TARIFF.search(text)
    if tm:
        marks = int(tm.group(2)) * int(tm.group(1) or 1)
        text = TARIFF.sub('', text)
    elif bm:
        marks = int(bm.group(1))
        text = BARE_TARIFF.sub('', text)
    text = _norm(BULLET.sub('', text))
    if not text:
        return
    if re.fullmatch(r'(?:or|and|arba|ir|Etc\.?)\.?', text, re.I):
        # "Etc." is the SEC saying the list is not exhaustive, not an answer.
        ask.open_list = True
        return
    if ask.answers and not opened and not _looks_new(text):
        ask.answers[-1]['text'] = _norm(f'{ask.answers[-1]["text"]} {text}')
        if marks is not None and ask.answers[-1]['marks'] is None:
            ask.answers[-1]['marks'] = marks
        return
    ask.answers.append({'text': text, 'marks': marks})


CONTINUATION = re.compile(r'^[a-ząčęėįšųūž(]')


def _looks_new(text):
    """Is this row a marking point of its own, or the tail of the one above?"""
    return not CONTINUATION.match(text)


def _read_tariff(ask, text, directive_count=None):
    """Read the printed price, and never invent one.

    A row states the ask's total and its split together — "4 Marks (2 x 2)" —
    so both are read and CHECKED against each other. A split that does not
    multiply out to the total the SEC printed beside it is a fault on the ask,
    not a number to pick between.
    """
    pm = PUNKTAI.search(text)
    if pm and ask.per is None:
        ask.count, ask.per, ask.total = 1, int(pm.group(1)), int(pm.group(1))
        ask.notation = pm.group(0)
        return
    stated_total = None
    bm = BARE_TARIFF.search(SPLIT_BARE.sub('', SPLIT.sub('', TARIFF.sub('', text))))
    if bm:
        stated_total = int(bm.group(1))
    sm = SPLIT.search(text) or SPLIT_BARE.search(text)
    tm = TARIFF.search(text)
    if sm:
        count, per = int(sm.group(1)), int(sm.group(2))
        if directive_count is not None and count != directive_count:
            ask.fault = (f'the directive claims {directive_count} answer(s) and '
                         f'the split {sm.group(0)!r} prices {count}')
        ask.count, ask.per, ask.total = count, per, count * per
        ask.split = True
        ask.notation = _norm(f'{bm.group(0) if bm else ""} {sm.group(0)}')
        if stated_total is not None and stated_total != ask.total:
            ask.fault = (f'the scheme prints the total as {stated_total} marks '
                         f'and the split {sm.group(0)!r}, which is {ask.total}')
        return
    if tm:
        count = int(tm.group(1)) if tm.group(1) else None
        per = int(tm.group(2))
        if directive_count is not None and count is not None \
                and count != directive_count:
            ask.fault = (f'the directive claims {directive_count} answer(s) and '
                         f'the tariff {tm.group(0)!r} prices {count}')
        ask.count = count if count is not None else (directive_count or ask.count or 1)
        ask.per = per
        ask.total = ask.count * per
        ask.split = count is not None
        ask.notation = tm.group(0)
        if stated_total is not None and stated_total != ask.total:
            ask.fault = (f'the scheme prints the total as {stated_total} marks '
                         f'and the tariff {tm.group(0)!r}, which is {ask.total}')
        return
    if stated_total is not None and ask.per is None:
        ask.count = directive_count or ask.count or 1
        ask.total = stated_total
        ask.per = stated_total // ask.count if ask.count else stated_total
        ask.notation = bm.group(0).strip()
        if ask.per * ask.count != stated_total:
            ask.fault = (f'the printed total {stated_total} does not divide by '
                         f'the {ask.count} answers the scheme asks for')


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
    if ask.columns:
        _read_columns(ask)
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
        priced = [a['marks'] for a in ask.answers if a['marks'] is not None]
        if priced and len(priced) == len(ask.answers):
            # The FULL rate is the largest mark printed, and anything under it
            # is a PART-CREDIT rung, not a second thing to claim. 2023 Higher
            # answers Q1(c) "iš (paslaptingojo) užsienio / Amerikos / Lenkijos,
            # iš turgaus. 6 marks", then "iš užsienio ar Lenkijos 3 marks" and
            # "iš turgaus 3 marks" — one six-mark answer and two half answers.
            # Added up line by line the ask reported a twelve-mark tariff that
            # disagreed with itself, on a question the SEC prices at six.
            top = max(priced)
            full = [a for a in ask.answers if a['marks'] == top]
            rungs = [a for a in ask.answers if a['marks'] != top]
            ask.per = top
            ask.count = len(full)
            ask.total = top * len(full)
            ask.answers = full
            ask.part += rungs
            ask.notation = (f'{ask.count} × {ask.per} marks, priced line by line'
                            if ask.count > 1 else f'{ask.per} marks')
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
    ap.add_argument('--subject', default=SUBJECT)
    args = ap.parse_args()

    if args.audit:
        for year, level in sittings(args.subject):
            S = LtScheme(year, level, args.subject)
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

    S = LtScheme(args.year, args.level, args.subject)
    for a in S.all_asks():
        print(f'{a.section:4} {a.ref_tail():14} {a.notation:22} {a.cue[:80]}')
        if args.full:
            for ans in a.answers:
                print(f'         · {ans["text"][:110]}'
                      + (f'  [{ans["marks"]}m]' if ans['marks'] else ''))
        if a.fault:
            print(f'         FAULT {a.fault}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
