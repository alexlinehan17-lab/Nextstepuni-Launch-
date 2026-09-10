#!/usr/bin/env python3
"""Non-curricular EU language marking schemes — the priced answer.

    python3 scripts/markbank/authoring/eu_scheme.py portuguese 2024 hl --full
    python3 scripts/markbank/authoring/eu_scheme.py portuguese --audit

What this document is
---------------------
A MODERN scheme (Portuguese 2022 onward) is four documents in one file, and
only one of them answers a question a card can ask:

    Reading Comprehension        <- priced answers, question reprinted
    Written Production           <- a CONTENT and LANGUAGE band grid
    Listening Comprehension      <- priced answers, but the ask needs the audio
    APPENDIX 2 Audio Scripts     <- the recording, in print

A CLASSIC scheme (Portuguese 2021, and every Romanian and Dutch sitting) is a
list of answers under the paper's own numbering with NO marks anywhere: its
head reads "Tópicos de correcção · Parte I (30 pontos)" and then "1. a) …".
The price for those sittings is printed on the QUESTION PAPER, which is where
eu_paper.py reads it, and nothing here invents one.

**The tariff is a column, not a suffix, and it is CENTRED on its group.**
The SEC sets four bulleted answers between y=190 and y=249 and prints
"6 marks: 3 x 2 mark" at y=211 — the middle of the group, on no answer's own
baseline — with "(any 3)" beneath it. Read line by line the answers have no
price and the price has no answer. So the page is gathered into ROWS by
baseline, and a row printed wholly in the price column is read as the ASK's
tariff rather than as any one answer's.

**Where the total is written down.** Two ways, and both are read:
* 2022 and 2023 head every ask "Answer | N Marks" — a table header whose second
  cell is the ask's own total.
* 2024 and 2025 drop that header and print only the split, "6 marks: 3 x 2
  marks". The total is the number in front of the colon.
Where an ask prints several splits — three alternative answers each priced
"4 marks: 2 x 2 marks" and a shorter one priced "2 marks" — the ask is worth
the LARGEST, because alternatives are mutually exclusive. That is not a guess:
`--audit` adds the leaf totals of every question and checks them against the
"Question 1  50 marks" head the scheme prints above them, and they agree.
"""
import argparse
import collections
import glob
import itertools
import os
import re
import sys

import pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))
from markbank_text import unligature                            # noqa: E402
from eu_paper import (LANGS, cfg, next_letter,                   # noqa: E402
                      LETTER_COLON, letter_pattern, letters_for)


def schemes_dir(subject):
    return os.path.join(ROOT, 'examiner-reports', subject, 'schemes')


def scheme_path(year, level, subject):
    path = os.path.join(schemes_dir(subject), f'{year}-{level}.pdf')
    return path if os.path.exists(path) else None


NBSP = '\u00a0\u2000\u2001\u2002\u2003\u2007\u2009\u200a\u202f\u2060\ufeff'
SYMBOL_SPACE = '\uf020\uf0a0'


def _norm(text):
    out = ''.join(' ' if c in NBSP or c in SYMBOL_SPACE else c
                  for c in unligature(text))
    return re.sub(r'\s+', ' ', out).strip()


class Row:
    __slots__ = ('page', 'x', 'y', 'text', 'cells')

    def __init__(self, page, x, y, text, cells=()):
        self.page, self.x, self.y, self.text = page, x, y, text
        self.cells = list(cells)

    def __repr__(self):
        return f'Row(p{self.page} x={self.x:.1f} {self.text[:70]!r})'


ROW_TOL = 4.0
# Where the SEC's marks column starts. Measured from the corpus: every printed
# tariff cell in the nine Portuguese schemes stands at x >= 405 and no answer
# text does. Below it a "4 marks" is part of a sentence, not a price.
PRICE_X = 380.0
LETTER_TOL = 8.0


def read_rows(path):
    """The scheme's pages as printed ROWS, left to right, with the margin.

    A marking point and the marks it earns sit in different cells of one
    printed row, and pymupdf reports them as two lines. Emitting a cell per
    line separates an answer from its price, which is how "the scheme prints no
    tariff" gets said about a document that prices every line.
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
                                          (span['bbox'][1]
                                           + span['bbox'][3]) / 2, text))
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
    return _fold_marker_rows(out)


MARKER_ONLY = re.compile(r'^\(\s*([a-z]{1,4})\s*\)\.?$', re.I)
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


def _row(page, band):
    band = sorted(band, key=lambda t: t[0])
    cells = [(x, text) for x, _y, text in band]
    keep = []
    for i, (x, text) in enumerate(cells):
        if TICK.fullmatch(text) and any(
                j != i and abs(cells[j][0] - x) < 3.0
                and len(cells[j][1]) > 1 and TICK.match(cells[j][1][0])
                for j in range(len(cells))):
            continue
        keep.append((x, text))
    # A bracket printed alone in a cell is not content. The 2025 Ordinary
    # scheme sets one at x=-3.1 — off the page altogether — in front of
    # Question 2(f)(i), and joined to the row it turned "(i) Tick (✓) the
    # correct answers:" into "( (i) Tick…", which no roman pattern matches:
    # the ask, and the four marks the SEC prices it, censused as absent.
    cells = [(x, t) for x, t in keep if t not in '()' and x > 5] or keep
    return Row(page, cells[0][0], band[0][1],
               _norm(' '.join(t[1] for t in cells)), cells)


# ---------------------------------------------------------------- the units --
UNIT_READING = re.compile(
    r'^(?:Part\s+A\s+Reading|Reading\s+Comprehension\s*$|Reading\s*$|'
    r'Part\s+A\s+Reading\s+Comprehension)', re.I)
UNIT_WRITING = re.compile(
    r'^(?:Written\s+Production|Part\s+B\s+(?:Writing|Written))', re.I)
UNIT_LISTENING = re.compile(r'^Listening\s+Comprehension\b', re.I)
APPENDIX = re.compile(r'^APPENDIX\b', re.I)

Q_HEAD = re.compile(r'^Question\s*(\d{1,2})\b')
LISTEN_HEAD = re.compile(r'^Part[e]?\s+([A-F])\b', re.I)
LETTER = re.compile(r'^\(?\s*([a-l])\s*\)\s*(.*)$', re.I)
ROMAN = re.compile(r'^\(\s*(i{1,3}|iv|vi{0,3}|ix|x)\s*\)\s*(.*)$', re.I)
# The same marker with its OPENING bracket dropped. 2023 Higher prints
# Question 2(f)'s fourth part as "iv) Andreas levará apenas uma garrafa…" and
# the mark it earns went with it. Accepted ONLY where the token is the roman
# after the one already open, which no line of prose ever is.
ROMAN_HALF = re.compile(r'^(i{1,3}|iv|vi{0,3}|ix|x)\s*\)\s*(.*)$', re.I)
NUMBERED = re.compile(r'^\(?(\d{1,2})\s*[.)]\s*(.*)$')
ROMANS = ['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x']

# The tariff, in the two notations this family prints:
#   "6 marks: 3 x 2 marks"   the total, then the split that makes it
#   "3 marks", "1 mark"      the total alone
SPLIT = re.compile(
    r'(\d{1,2})\s*marks?\s*[:;]\s*(\d{1,2})\s*[x×]\s*(\d{1,2})\s*marks?', re.I)
FLAT = re.compile(r'(?:^|\s|\()(\d{1,2})\s*marks?\b', re.I)
# The table header the 2022 and 2023 schemes print above every ask's answers.
# Its second cell is the ask's own total, and it is the only place those two
# sittings state one.
ANSWER_HEAD = re.compile(r'^Answer\b\s*(\d{1,2})?\s*(?:marks?)?\s*'
                         r'(?:[:;]\s*(\d{1,2})\s*[x×]\s*(\d{1,2})\s*marks?)?$',
                         re.I)
# "(any 3)", "(Any 4)", "any 2" — how many of the listed answers may be claimed.
ANY_N = re.compile(r'\(?\s*any\s+(\d{1,2})\s*\)?', re.I)

TICK = re.compile('^[\uf0fc\u2713\u2714]$')
BULLET = re.compile('^[\u2010\u2011\u2012\u2013\u2014\u2022\u25cf\u25aa\u2713\u2714\uf0fc\uf0b7\uf0a7\uf0d8-]\\s*')
PAGE_ONLY = re.compile(r'^\d{1,3}$')
FURNITURE = re.compile(
    r'^(?:Leaving\s+Certificate|Coimisi[úu]n|State\s+Examinations|'
    r'Marking\s+Scheme|Higher\s+Level\s*$|Ordinary\s+Level\s*$|'
    r'\[Escreva aqui\])', re.I)
# Examiner rubric, which is never an answer.
NOTE = re.compile(r'^(?:Note?[ăa]?\s*:|N\.?B\.?\b|Accept\b|Allow\b|Penali[sz]e\b|'
                  r'If\s+the\s+candidate\b|Answer\s+questions?\b|'
                  r'Responda\b|Based\s+on\b|Baseado\b|Tick\s*\(|'
                  r'Assinale\b|Complete\s+the\s+table\b)', re.I)
# A row that is only a reference to the passage — "(Parágrafo 5)", "(Parte 2)"
# — is the tail of the reprinted question, not an answer.
REF_ONLY = re.compile(r'^\((?:par[áa]grafos?|paragraphs?|parte|part|'
                      r'alinea|alínea|sections?)\b[^)]*\)$', re.I)
# A row that is ONLY a part's own share of the paper — "(30 pont / 100 pont)",
# "(40/100)". The SEC prints that cell against a part head and nowhere else,
# so where the head itself is missing the cell is what says the part changed:
# the 2020 Hungarian scheme heads its first part with a bare "I" and its
# second and third with no banner at all, only this cell, and read without it
# Part II's model commentary and Part III's essay titles shipped inside the
# answer to Question 6.
# The sentence that introduces the criteria table the written parts are
# marked by. It is printed at the END of Part I in nine of the twelve subjects
# on this reader — "A II. és III. részben elérhető pontok az alábbi szempontok
# szerint oszlanak meg:", "II ja III ülesande hindamisel arvestatakse
# järgmisi kriteeriume:" — and everything after it belongs to no ask, so read
# without it the last question of the sitting shipped the whole grid inside
# its answer. Recognised two ways, both printed: a line that NAMES the later
# parts and ends in a colon, and a criterion line whose percentage is
# introduced by a dash. A percentage inside an answer ("A diplomások 41%-a")
# has neither.
CRITERIA_PERCENT = re.compile(r'[\u2013\u2014\-:]\s*\d{1,3}\s*%')
PART_PRICE_ONLY = re.compile(
    r'^[(\[]\s*(\d{1,3})\s*\w*\s*/\s*(\d{1,3})\s*\w*\s*[)\]]$')
PART_ORDER = ['I', 'II', 'III']
# The classic scheme's own head, which prices a PART and nothing under it.
CLASSIC_PART = re.compile(
    r'^(?:Parte|PARTEA|Deel)\s+(I{1,3}|a\s*I{1,2}I?\s*[-‐–]\s*a|[123])\b',
    re.I)


class Ask:
    """One priced ask of a marking scheme."""

    __slots__ = ('section', 'q', 'letter', 'roman', 'cue', 'page', 'stem',
                 'answers', 'splits', 'header_total', 'any_n', 'fault',
                 'notation', 'total', 'count', 'per', 'part', 'ticks',
                 'price_frags', 'settled', 'cue_x', 'seen_head',
                 'additive', 'in_note')

    def __init__(self, section, q, letter, roman, cue, page):
        self.section, self.q = section, q
        self.letter, self.roman = letter, roman
        self.cue, self.page = cue, page
        self.stem = ''
        # {'text': str, 'marks': int|None} for every marking point printed
        # under this ask.
        self.answers = []
        # (total, count, per) for every tariff cell printed against it.
        self.splits = []
        # Every fragment of the marks COLUMN printed beside this ask, in
        # printed order, with the answer whose row it began on. The SEC breaks
        # one tariff cell over three baselines — "8 marks:" / "4 x 2 marks" /
        # "(any 4)" — so a fragment is not a tariff until they are put back
        # together (see _assemble_tariffs).
        self.price_frags = []
        self.settled = None
        # Where the REPRINTED QUESTION is set, and whether the SEC has printed
        # its "Answer | N Marks" table header yet. Both are how a row under an
        # ask is told from the question it answers — see _classify.
        self.cue_x = None
        self.seen_head = False
        # Whether the marks printed beside this ask's answers ADD UP to what
        # the ask is worth. Where they do, each answer is one ITEM of the ask
        # — "Age: 30 | 2 marks" and "Clothes: blue uniform | 4 marks" under a
        # six-mark head — and none of them is a part-credit rung.
        self.additive = False
        # Whether the row just read was examiner rubric. The SEC wraps its
        # notes — "If the candidate doesn't use the word soul but understands
        # the / meaning of the text." — and dropping only the first row welded
        # "meaning of the text." onto the answer above it, which then quoted a
        # sentence the scheme never printed.
        self.in_note = False
        self.header_total = None
        self.any_n = None
        self.fault = None
        self.notation = ''
        self.total = self.count = self.per = None
        # Answers priced BELOW the ask's own total: a shorter form of the
        # answer above, which is not something a student may claim beside the
        # full one. Kept, and disclosed on the card as a note.
        self.part = []
        self.ticks = []

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
        return (f'Ask({self.key} {self.notation!r} '
                f'{len(self.answers)} answers)')


MARKER_HEAD = re.compile(r'^\(\s*([a-z]{1,4})\s*\)', re.I)


def _next_roman(current):
    """The roman after this one, in the SEC's own run."""
    if current in ROMANS:
        i = ROMANS.index(current)
        if i + 1 < len(ROMANS):
            return ROMANS[i + 1]
    return None


def _next_marker(rows, i):
    """The next bracketed marker printed after row i, or None."""
    for row in rows[i + 1:i + 40]:
        m = MARKER_HEAD.match(row.text)
        if m:
            return m.group(1).lower()
    return None


class EuScheme:
    def __init__(self, year, level, subject):
        self.year, self.level, self.subject = year, level, subject
        self.path = scheme_path(year, level, subject)
        if self.path is None:
            raise FileNotFoundError(f'no {subject} scheme for {year} {level}')
        self.rows = read_rows(self.path)
        self.grid_lines = []
        self.question_totals = {}       # (section, q) -> the head's own total
        # The alphabet this subject's markers are set in — Latin everywhere
        # but Bulgarian, whose Question 1 is lettered "а) б) в) г) д)".
        self.first_letter = letters_for(subject)[0]
        self.era = 'modern' if self._has_units() else 'classic'
        self.letter_x = self._letter_column()
        self.answer_x = self._answer_column()
        # Does this scheme head every ask with its own "Answer | N Marks"
        # table header? The 2022 and 2023 schemes do and the 2024 and 2025
        # schemes do not, and where it is printed it is the boundary between
        # the question and the answers — better evidence than any column.
        self.has_answer_heads = sum(
            1 for r in self.rows
            if ANSWER_HEAD.match(_norm(' '.join(t for x, t in r.cells
                                                if x < PRICE_X)))
            and any(x >= PRICE_X for x, _t in r.cells)) >= 3
        self._asks = (self._walk() if self.era == 'modern'
                      else self._walk_classic())
        if self.era == 'classic' and not self._asks:
            # A classic scheme that heads NO part at all. Three Croatian
            # sittings — 2019, 2025 and 2026 — open "Croatian Marking Scheme
            # 2025" and then go straight to "1. Objasnite svojim riječima…",
            # with no "I. dio" anywhere in the document, and read strictly
            # each of them answered nothing. The only part a classic scheme
            # answers is the first, so the walk is repeated with that assumed;
            # the criteria line and the part-price cell still close it, which
            # is what keeps Parts II and III out of the last question.
            self._asks = self._walk_classic(assume_part='I')
        for ask in self._asks:
            _assemble_tariffs(ask)
            _price(ask)
        _walk_down_splits(self._asks)
        self.unsettled = self._settle()
        for ask in self._asks:
            _price(ask)
        _walk_down_splits(self._asks)
        for ask in self._asks:
            _split_rungs(ask)

    def _settle(self):
        """Close each question's arithmetic against the total it prints.

        Law 3's independent check, on the one number this reader has to choose
        rather than read: an ask that prints the same price beside several
        answers is either alternatives or a list, and the question's own head
        total says which. Returns the questions whose arithmetic did NOT
        close, for the census to flag.
        """
        open_questions = []
        by_q = collections.defaultdict(list)
        for a in self.reading():
            by_q[(a.section, a.q)].append(a)
        for key, want in sorted(self.question_totals.items(), key=str):
            leaves = by_q.get(key) or []
            if not leaves:
                continue
            got = sum(a.total or 0 for a in leaves)
            if got == want:
                continue
            if not _settle_question(leaves, want):
                open_questions.append((key, want, got))
        return open_questions

    def _has_units(self):
        """Does this file print the modern scheme's section heads?"""
        return any(UNIT_READING.match(r.text) or UNIT_LISTENING.match(r.text)
                   for r in self.rows)

    def _letter_column(self):
        by_q, inside, q = {}, self.era == 'classic', None
        for row in self.rows:
            if UNIT_READING.match(row.text):
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

    def _answer_column(self):
        """Where a MARKING POINT is set, as against the question above it.

        The two are five or six points apart and never further: 2024 Higher
        reprints its questions at x=85.1 and bullets its answers at x=90.9,
        2023 at 72.0 and 77.6, 2022 at 92.7 and 97.3. Five points is not a
        margin anyone would design, but it is the one the SEC prints, and it
        is the only thing on the page that separates "Por que razão? Dê
        detalhes." — the second line of a question — from the answer beneath
        it. Measured from the rows the SEC bulleted, which are answers and
        nothing else.
        """
        rows = self._reading_rows()
        xs = [round(r.x, 1) for r in rows if BULLET.match(r.text)]
        if len(xs) < 4:
            xs += [round(r.x, 1) for r in rows
                   if any(x >= PRICE_X for x, _t in r.cells)
                   and any(x < PRICE_X for x, _t in r.cells)]
        return max(set(xs), key=xs.count) if xs else None

    def _reading_rows(self):
        """Only the rows of the Reading unit.

        Measured over the whole file the answer column comes out of the
        WRITTEN PRODUCTION grid, which bullets forty band descriptors at its
        own margin — 63.6 in the 2024 Higher scheme, where every reading answer
        stands at 90.9 — and every reading answer was then read as more of the
        question it answers.
        """
        out, inside = [], False
        for row in self.rows:
            if UNIT_READING.match(row.text):
                inside = True
                continue
            if UNIT_WRITING.match(row.text) or UNIT_LISTENING.match(row.text) \
                    or APPENDIX.match(row.text):
                inside = False
                continue
            if inside:
                out.append(row)
        return out

    def _column_for(self, q):
        return self.letter_x_by_q.get(q, self.letter_x)

    def _is_letter(self, x, prev_letter, q=None):
        return x <= self._column_for(q) + LETTER_TOL and prev_letter == 'h'

    # --------------------------------------------------------------- walk ---
    def _walk(self):
        asks, unit, q, letter, roman = [], None, None, None, None
        current = None
        listen_section = 'A'

        def close():
            nonlocal current
            if current is not None:
                asks.append(current)
                current = None

        for index, row in enumerate(self.rows):
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
            section = 'A' if unit == 'A' else f'L{listen_section}'
            if unit == 'L':
                lh = LISTEN_HEAD.match(text)
                if lh:
                    close()
                    listen_section = lh.group(1).upper()
                    q = letter = roman = None
                    continue
            head = Q_HEAD.match(text)
            if head and unit == 'A':
                close()
                q, letter, roman = int(head.group(1)), None, None
                total = _head_total(text)
                if total:
                    self.question_totals[('A', q)] = total
                continue
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
                    _absorb_price_cells(current, row)
                    continue
            if q is None and unit == 'A':
                continue
            rm = ROMAN.match(text)
            if rm is None and roman is not None:
                half = ROMAN_HALF.match(text)
                if half and half.group(1).lower() == _next_roman(roman):
                    rm = half
            lm = LETTER.match(text)
            marker = None
            column = self._column_for(q) if unit == 'A' else self.letter_x
            # "(i)" is both the ninth letter and the first roman, and a
            # scheme prints it as BOTH at the same column: 2023 Higher sets
            # "(h)", then "(i)" and "(ii)" beneath it, then the LETTER "(i)",
            # then "(j)" — all four at x=72.0, where the paper indents the
            # romans past the letters. The column cannot settle it, so the
            # SEC's own numbering does: an "(i)" followed by "(ii)" opens a
            # roman run, and one followed by anything else is the letter after
            # (h). Read on the column alone, the whole of Question 1(h) was
            # filed under a letter (i) that does not exist and three of the
            # question's fifty marks vanished.
            ambiguous = rm and rm.group(1).lower() == 'i' \
                and self._is_letter(row.x, letter, q)
            if ambiguous and _next_marker(self.rows, index) == 'ii':
                ambiguous = False
            if rm and not ambiguous:
                marker = ('roman', rm.group(1).lower(), rm.group(2))
            elif lm and unit == 'A' \
                    and (row.x <= column + LETTER_TOL
                         or lm.group(1).lower() == next_letter(
                             letter, self.first_letter)):
                marker = ('letter', lm.group(1).lower(), lm.group(2))
            # A marker that REPEATS the one before it is the SEC misnumbering,
            # not a new ask: 2022 Ordinary prints Question 1(f) as "(i) (ii)
            # (iii) (iii) (iii)" where the paper prints three romans and the
            # scheme's own head prices them "9 marks". Read as five asks it
            # priced the question at thirteen; read as one ask with three
            # answers it prices it at nine, which is what the head says.
            if marker and current is not None \
                    and ((marker[0] == 'roman' and marker[1] == roman)
                         or (marker[0] == 'letter' and marker[1] == letter
                             and roman is None)):
                # The words only, never the marks column beside them: read off
                # the joined row, "(iii) Acostumo" and its price arrived as one
                # answer reading "Acostumo 2 marks", which is a tariff on a
                # card where an answer belongs.
                rest = _norm(' '.join(t for x, t in row.cells if x < PRICE_X))
                rest = re.sub(r'^\(?\s*[a-z]{1,4}\s*\)\s*', '', rest,
                              flags=re.I)
                _add_answer(current, rest, opened=bool(BULLET.match(rest)))
                for x, t in row.cells:
                    if x >= PRICE_X:
                        current.price_frags.append(
                            {'text': t,
                             'answer': current.answers[-1]
                             if current.answers else None})
                continue
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
                current = Ask(section, q, letter, roman, rest, row.page)
                current.cue_x = next((x for x, _t in row.cells
                                      if x < PRICE_X and x > row.x + 4),
                                     row.x)
                _absorb_price_cells(current, row)
                continue
            if current is not None:
                _absorb(current, row, self.has_answer_heads)
        close()
        return asks

    def _walk_classic(self, assume_part=None):
        """A classic scheme: answers under the paper's own numbering, unpriced.

        Its head is "Tópicos de correcção · Parte I (30 pontos)" and then "1.
        a) …". No line of it carries marks, so nothing here reads a tariff —
        the price for these sittings is printed on the QUESTION PAPER and
        eu_paper.py reads it there.
        """
        asks, part, q, letter = [], assume_part, None, None
        current = None
        broke = False
        noted = False
        # Whether the row just read was a part head, and how many bare part
        # price cells have opened a part so far — see PART_PRICE_ONLY.
        headed = False
        seen_prices = 0
        # The Dutch scheme letters its first question's parts with a COLON,
        # exactly as its paper does — "a: 'Het' in de zin:" — so the two
        # documents are read with the same marker form or they do not pair.
        # The same is true of Hungarian's comma, Finnish's full stop and
        # Bulgarian's Cyrillic alphabet: one table in eu_paper.LANGS decides
        # the form for BOTH documents, which is what makes the pair possible.
        letter_pat = letter_pattern(self.subject)
        # The part head, in this subject's own language. Nine of the twelve
        # subjects on this reader head their parts in words CLASSIC_PART does
        # not know — "I. RÉSZ", "Първа част", "ČASŤ I", "Del I", "I ÜLESANNE",
        # "I TEHTÄVÄ", "I. dio", "Opgave I", "1. DEL" — and their schemes head
        # them the same way their papers do, so the paper's own pattern is
        # what is read here.
        own = (cfg(self.subject, 'scheme_part')
               or cfg(self.subject, 'classic_part'))
        part_pat = (re.compile(own, re.I) if own and self.subject not in
                    ('portuguese', 'romanian', 'dutch') else CLASSIC_PART)

        def close():
            nonlocal current
            if current is not None:
                asks.append(current)
                current = None

        for row in self.rows:
            text = row.text
            if PAGE_ONLY.match(text) or FURNITURE.match(text):
                continue
            pm = part_pat.match(text)
            if pm is None and len(text) < 40:
                # A head the SEC LETTERSPACED — see eu_paper._walk_classic,
                # which reads the same heads out of the question paper.
                pm = part_pat.match(re.sub(r'\s+', '', text))
            if pm:
                close()
                token = next((g for g in pm.groups() if g), None)
                part = ((cfg(self.subject, 'classic_part_map') or {})
                        .get((token or '').lower())
                        or _classic_part_token(token or ''))
                q, letter = None, None
                headed = True
                continue
            if part == 'I' and len(text) > 25 \
                    and (CRITERIA_PERCENT.search(text)
                         or (text.rstrip().endswith(':')
                             and part_pat.search(text))):
                close()
                noted = True
                continue
            if PART_PRICE_ONLY.match(text):
                # The cell belongs to the head above it wherever the SEC
                # printed one; only where it stands alone does it open a part.
                if headed:
                    headed = False
                    continue
                close()
                seen_prices += 1
                part = PART_ORDER[min(seen_prices - 1, len(PART_ORDER) - 1)]
                q, letter = None, None
                continue
            headed = False
            if part is None:
                continue
            if part != 'I':
                self.grid_lines.append(text)
                continue
            # The examiner's NOTE closes the ask above it and everything after
            # it belongs to no ask at all: the Romanian scheme heads the four
            # criteria it prices the written parts by "Notă:", and read as
            # more of Question 6 that whole table shipped inside the answer.
            if NOTE.match(text):
                close()
                noted = True
                continue
            nm = NUMBERED.match(text)
            lm = letter_pat.match(text)
            if nm and int(nm.group(1)) == (q or 0) + 1:
                close()
                noted = False
                q, letter = int(nm.group(1)), None
                rest = nm.group(2)
                inner = letter_pat.match(rest)
                if inner:
                    letter, rest = inner.group(1).lower(), inner.group(2)
                current = Ask(part, q, letter, None, '', row.page)
                broke = False
                if rest:
                    current.answers.append({'text': rest, 'marks': None})
                continue
            if lm and q is not None \
                    and lm.group(1).lower() == next_letter(
                        letter, self.first_letter):
                close()
                noted = False
                letter = lm.group(1).lower()
                current = Ask(part, q, letter, None, '', row.page)
                broke = False
                if lm.group(2):
                    current.answers.append({'text': lm.group(2),
                                            'marks': None})
                continue
            # A row that is only a paragraph reference or only a price is a
            # BOUNDARY, not an answer: the classic schemes print the question,
            # then "(alinea 1) (1 punt)", then the answer. Dropped silently the
            # answer after it read as a wrapped continuation of the question
            # above — "mogelijk, iets wat een probleem kan worden" was welded
            # onto the sentence it answers and two Dutch asks shipped none.
            if row.cells and all(REF_ONLY.match(c) or _is_price_only(c)
                                 for _x, c in row.cells):
                broke = True
                continue
            if noted:
                continue
            if current is not None:
                # A bulleted row is a marking point of its own however it
                # reads: the 2021 Dutch scheme answers Question 2 with six
                # one-word bullets — "‐ rouw", "‐ ellende", "‐ verdriet" — and
                # judged on their first letter alone every one of them was
                # welded onto the question above.
                _add_answer(current, text,
                            opened=broke or bool(BULLET.match(text)))
                broke = False
        close()
        return asks

    # ---------------------------------------------------------------- API ---
    def reading(self):
        return _leaves([a for a in self._asks if a.section in ('A', 'I')])

    def listening(self):
        return _leaves([a for a in self._asks
                        if (a.section or '').startswith('L')])

    def all_asks(self):
        return _leaves(self._asks)

    def grid_quote(self, limit=6):
        """The band grid, in the SEC's own words, for the exclusion evidence.

        Two shapes, and both are the scheme's own printed lines rather than
        anything written here. Portuguese prints an English band grid; the
        nine non-curricular languages added in September 2026 print a table
        of four QUALITIES against percentages in their own language —
        "1. Megértés – A válaszadó megérti a kérdéseket… – 30%", "3. Nyelvi
        képesség… – 30%", "4. Nyelvhelyesség – Nyelvi és helyesírási
        szabályok. – 10%" — which says the same thing and is what the
        exclusions ledger for those subjects quotes.
        """
        wanted = [t for t in self.grid_lines
                  if re.search(r'Very\s+good|coherence|communicative\s+task|'
                               r'range\s+of\s+vocabulary|register|'
                               r'TOP\b|MIDDLE\b|BOTTOM\b|Content\s+and',
                               t, re.I)]
        if not wanted:
            wanted = [t for t in self.grid_lines
                      if re.search(r'\d{1,3}\s*%', t) and len(t) > 12]
        return ' · '.join(w[:120] for w in wanted[:limit])


def pair_leaves(paper_leaves, scheme_leaves):
    """{paper key: the scheme ask that answers it}, and how the pair was made.

    Law 4: never join paper to scheme on the part key alone. Eight of the nine
    Portuguese sittings letter the two documents identically, and the ninth
    does not — the 2022 Ordinary scheme letters Question 3 "(a)(b)(c)(d) (g)(h)
    (i)(j)" where the paper letters it "(a)…(h)", skipping (e) and (f), and its
    own rubric says so: the paper heads a page "Answer questions (e) – (h) in
    English" and the scheme heads the same page "Answer questions (g) – (j) in
    English". Joined on the key, four printed asks reported unpriced and two
    priced answers reported orphaned, all six for a question where every ask
    is printed and every ask is answered.

    So the address is TRIED and then checked: where every paper leaf of a
    question has a scheme leaf at the same address and there is nothing left
    over, the address is the join. Where it is not, the two are joined in
    printed ORDER — safe only because the caller scores every pair on wording
    and refuses a pair that does not agree, which is exactly what the address
    join is spared having to do.
    """
    by_key = {a.key: a for a in scheme_leaves}
    if len(by_key) == len(paper_leaves) \
            and all(p.key in by_key for p in paper_leaves):
        return {p.key: by_key[p.key] for p in paper_leaves}, 'address'
    if paper_leaves and len(paper_leaves) == len(scheme_leaves):
        return ({p.key: sch for p, sch in zip(paper_leaves, scheme_leaves)},
                'order')
    return {p.key: by_key.get(p.key) for p in paper_leaves}, 'address'


def pairs_by_question(paper_leaves, scheme_leaves):
    """The same, done question by question, which is the scope the SEC
    renumbers within."""
    groups = collections.defaultdict(lambda: ([], []))
    for a in paper_leaves:
        groups[(a.section, a.q)][0].append(a)
    for a in scheme_leaves:
        groups[(a.section, a.q)][1].append(a)
    out, how = {}, {}
    for key, (papers, schemes) in groups.items():
        made, kind = pair_leaves(papers, schemes)
        out.update(made)
        how[key] = kind
    return out, how


# A row that states only a price, in any of the family's words for one.
PRICE_ONLY = re.compile(
    r'^\(?\s*(?:\d{1,2}\s*[x×]\s*)?\d{1,3}\s*'
    r'(?:puncte|punct|punten|punt|pontos|ponto|marks?)\s*\)?\.?$', re.I)


def _is_price_only(text):
    return bool(PRICE_ONLY.match(text.strip()))


def _classic_part_token(raw):
    """"I", "a II-a", "2" — the part number, as a Roman numeral token."""
    raw = raw.strip().lower().replace(' ', '').replace('-', '')
    table = {'i': 'I', 'ii': 'II', 'iii': 'III',
             'aiia': 'II', 'aiiia': 'III',
             '1': 'I', '2': 'II', '3': 'III'}
    return table.get(raw, raw.upper())


def _head_total(text):
    m = re.search(r'(\d{2,3})\s*marks?\b', text, re.I)
    return int(m.group(1)) if m else None


def _absorb_price_cells(ask, row):
    """Take the tariff out of a marker row before the question is kept.

    The Ordinary schemes head an ask "(a)  4 marks" and reprint the question
    beside it, so the price arrives welded to the cue; left there, the card's
    question text carries its own marks.
    """
    price = [t for x, t in row.cells if x >= PRICE_X]
    for text in price:
        ask.price_frags.append({'text': text, 'answer': None})
    if price:
        ask.cue = _norm(' '.join(t for x, t in row.cells if x < PRICE_X))
        ask.cue = re.sub(r'^\(?\s*[a-l]\s*\)\s*', '', ask.cue, flags=re.I)
        ask.cue = re.sub(r'^\(\s*[ivx]{1,4}\s*\)\s*', '', ask.cue, flags=re.I)


def _absorb(ask, row, has_heads=False):
    """One printed row under an ask: its header, its tariff, or an answer."""
    text = row.text
    price_cells = [t for x, t in row.cells if x >= PRICE_X]
    body_cells = [t for x, t in row.cells if x < PRICE_X]
    body = _norm(' '.join(body_cells))

    def price(answer=None, header=False):
        for cell in price_cells:
            ask.price_frags.append({'text': cell, 'answer': answer,
                                    'header': header})

    # A row printed WHOLLY in the marks column prices the ask, and belongs to
    # no single answer: the SEC centres it on the group it prices.
    if price_cells and not body:
        price()
        return
    head = ANSWER_HEAD.match(body)
    if head and (head.group(1) or price_cells):
        price(header=True)
        if head.group(1):
            ask.price_frags.append({'text': body, 'answer': None,
                                    'header': True})
        ask.seen_head = True
        return
    if NOTE.match(body):
        price()
        ask.in_note = True
        return
    if ask.in_note and not _looks_new(body):
        price()
        return
    ask.in_note = False
    if REF_ONLY.match(body):
        # The tail of the reprinted question. Its words belong to the cue and
        # the marks beside it to the ask.
        price()
        if not ask.answers:
            ask.cue = _norm(f'{ask.cue} {body}')
        return
    if _continues_cue(ask, row, body, has_heads, price_cells):
        price()
        ask.cue = _norm(f'{ask.cue} {body}')
        return
    answer = _add_answer(ask, body, opened=bool(BULLET.match(body)))
    price(answer=answer)


# A row that continues the reprinted QUESTION rather than starting an answer.
# Three signals, and any one settles it; everything else under an ask is an
# ANSWER, because that is what the rest of the page is.
#   * The SEC has not yet printed this ask's "Answer | N Marks" table header,
#     and this row stands at the QUESTION's own column. The 2024 and 2025
#     schemes drop that header, and then the column is all there is: "Por que
#     razão? Dê detalhes." is the second line of Question 1(e) and stands at
#     x=85.1 with the question above it, while every answer stands at 90.9.
#   * The row is the paragraph reference the SEC closes a question with.
#   * The cue so far does not end in terminal punctuation and this row opens
#     lower case, which is one sentence broken over two rows.
def _continues_cue(ask, row, body, has_heads, price_cells):
    if ask.answers or ask.seen_head or BULLET.match(body):
        return False
    if has_heads:
        # This file prints an "Answer | N Marks" header over every ask's
        # answers, and this ask has not reached its own yet: everything up to
        # it is the question. 2022 Ordinary reprints the two sentences
        # Question 1(e) asks about between the ask and its header, and read on
        # the column they became the first two things a student could claim.
        return True
    if price_cells:
        # A row carrying its own price is a marking point. The 2024 schemes
        # set the answer at the question's own column, one point apart —
        # "Para buscar uma vida melhor. | 2 marks" at x=98.4 under a question
        # at x=98.9 — and the column alone read the answer as more question.
        return False
    body_x = next((x for x, _t in row.cells if x < PRICE_X), row.x)
    if ask.cue_x is not None and abs(body_x - ask.cue_x) <= 2.0:
        return True
    if ask.cue and ask.cue[-1] not in '.?!:' and not _looks_new(body):
        return True
    return False


def _looks_new(text):
    """A marking point starts with a capital or a digit; a wrapped line does
    not. Only the first character decides, and only for rows the SEC opened
    with no bullet.

    Tested with `islower()` rather than against a character RANGE. The range
    that was here — a-z plus U+00E0 to U+024F — is the accented block's LOWER
    half plus half its upper half, so Romanian's "Ținând cont de ideile
    regăsite în text" opened with what Unicode calls U+021A, inside the range,
    and a reprinted question was welded onto the examiner's criterion above it
    and shipped as the answer.
    """
    body = text.lstrip()
    if not body or body[0] == '(':
        return False
    # The FIRST character, not the first letter in the line: an alternative
    # answer opening "“…uma biblioteca de pessoas que promove eventos" begins
    # with a quotation mark and an ellipsis, and skipping to the first letter
    # made it a continuation of the answer above it and merged two things a
    # candidate chooses between into one.
    if body[0].isalpha():
        return not body[0].islower()
    return True


def _add_answer(ask, text, opened=False):
    """Record one marking point, and return the dict the price attaches to."""
    text = _norm(BULLET.sub('', text))
    if not text or PAGE_ONLY.match(text):
        return ask.answers[-1] if ask.answers else None
    if re.fullmatch(r'(?:or|ou|and|e|of)\.?', text, re.I):
        return ask.answers[-1] if ask.answers else None
    if ask.answers and not opened and not _looks_new(text):
        ask.answers[-1]['text'] = _norm(f'{ask.answers[-1]["text"]} {text}')
        return ask.answers[-1]
    ask.answers.append({'text': text, 'marks': None})
    return ask.answers[-1]


# A price fragment that is not a tariff on its own, and the one it completes.
# The SEC sets a narrow marks column and breaks one cell over three baselines:
# "8 marks:" / "4 x 2 marks" / "(any 4)". Read apart, the first states a total
# with no split, the second a split with no total, and the third nothing at
# all — and 2025 Ordinary Question 1(a) reported "1 mark" for an ask the SEC
# priced at eight.
NEEDS_MORE = re.compile(r'[:;]\s*$')
IS_SPLIT_TAIL = re.compile(r'^\(?\s*\d{1,2}\s*[x×]\s*\d{1,2}\s*marks?\s*\)?$',
                           re.I)
IS_ANY_TAIL = re.compile(r'^\(?\s*any\s+\d{1,2}\s*\)?\.?$', re.I)


def _assemble_tariffs(ask):
    """Put the marks column back together, then read each complete tariff."""
    joined = []
    for frag in ask.price_frags:
        text = frag['text']
        if joined and (NEEDS_MORE.search(joined[-1]['text'])
                       or IS_SPLIT_TAIL.match(text)
                       or IS_ANY_TAIL.match(text)):
            joined[-1]['text'] = _norm(f'{joined[-1]["text"]} {text}')
            joined[-1]['header'] = joined[-1].get('header') or frag.get('header')
            continue
        joined.append(dict(frag))
    for cell in joined:
        total = _read_tariff(ask, cell['text'], header=cell.get('header'))
        if total is not None and cell.get('answer') is not None \
                and cell['answer'].get('marks') is None:
            cell['answer']['marks'] = total


def _read_tariff(ask, text, header=False):
    """Read a printed price, and never invent one.

    Returns the total this cell states, so a row that carries both an answer
    and its own price can put the marks on that answer.
    """
    any_n = ANY_N.search(text)
    if any_n:
        ask.any_n = int(any_n.group(1))
    sm = SPLIT.search(text)
    if sm:
        total, count, per = (int(sm.group(1)), int(sm.group(2)),
                             int(sm.group(3)))
        if count * per != total:
            ask.fault = (f'the scheme prints the tariff {sm.group(0)!r}, whose '
                         f'split does not multiply out to the {total} it '
                         f'states')
        ask.splits.append((total, count, per))
        if header:
            ask.header_total = total
        return total
    fm = FLAT.search(text)
    if fm:
        total = int(fm.group(1))
        ask.splits.append((total, 1, total))
        if header:
            ask.header_total = total
        return total
    return None


def _price(ask):
    """What the ask is worth, and how the SEC says it is earned."""
    ask.cue = _norm(ask.cue)
    if not ask.splits:
        return
    totals = [t for t, _c, _p in ask.splits]
    ask.total = ask.settled or ask.header_total or max(totals)
    if ask.header_total is not None and max(totals) > ask.header_total:
        ask.fault = (f'the scheme heads this ask "Answer {ask.header_total} '
                     f'Marks" and then prices a line of it {max(totals)}')
    items = [a for a in ask.answers if a['marks'] is not None]
    # Every stated answer priced, and the prices ADDING UP to the ask's total:
    # then each answer is one item of a list the paper prints as one ask, not
    # an alternative wording of the whole. "Age: 30 | 2 marks" and "Clothes:
    # blue uniform / shirt / jumper and tie | 4 marks" under "Answer 6 marks"
    # are both required; read as alternatives they became part-credit rungs
    # and the card offered no answer at all.
    ask.additive = (len(items) > 1
                    and sum(a['marks'] for a in items) == ask.total)
    # Among the prices that state this ask's total, the one that also states
    # how it is EARNED. 2023 Ordinary heads Question 1(e) "Answer 4 marks" and
    # prices it "4 marks: 4 x 1 mark" in the column beside it; taking the
    # header's flat (4, 1, 4) left the ask claiming one answer worth four,
    # and its four true/false rows — which the split names — unpriced.
    same = [s for s in ask.splits if s[0] == ask.total]
    best = (max(same, key=lambda s: s[1]) if same
            else max(ask.splits, key=lambda s: s[0]))
    if ask.additive:
        ask.count = len(items)
        pers = {a['marks'] for a in items}
        ask.per = pers.pop() if len(pers) == 1 else None
        ask.notation = (
            f'{ask.total} marks: {ask.count} x {ask.per} '
            f'{"mark" if ask.per == 1 else "marks"}, one for each item the '
            f'ask lists' if ask.per is not None else
            f'{ask.total} marks, priced item by item: '
            + ' + '.join(str(a['marks']) for a in items))
    else:
        _total, ask.count, ask.per = best
        ask.notation = (f'{best[0]} marks: {best[1]} x {best[2]} marks'
                        if best[1] > 1 else
                        f'{best[0]} {"mark" if best[0] == 1 else "marks"}')
    if ask.any_n:
        ask.notation += f' (any {ask.any_n})'
    ask.part = []


def _split_rungs(ask):
    """Answers priced BELOW the ask's total are PART-CREDIT rungs.

    A shorter form of the answer above it, worth less: "Biólogo. 3 marks"
    under "Era biólogo molecular. 4 marks". They are not things a student may
    claim beside the full answer, so they leave the claimable list and are
    disclosed on the card as a note instead. Done AFTER the question's
    arithmetic is settled, because which answers are rungs depends on what the
    ask turned out to be worth — and never where the prices ADD UP to that
    total, which means the answers are items and not rungs at all.
    """
    if ask.total is None or ask.additive:
        return
    rungs = [a for a in ask.answers
             if a['marks'] is not None and a['marks'] < ask.total]
    if rungs:
        ask.part = rungs
        ask.answers = [a for a in ask.answers if a not in rungs]


# How many readings of one question's asks may be tried before the question is
# left unsettled. Two readings per ambiguous ask, and no question in the corpus
# has more than a handful.
MAX_COMBINATIONS = 4096


def _settle_question(leaves, head_total):
    """Which reading of each ask's printed prices adds up to the head total.

    An ask that prints the same price beside several answers means one of two
    things, and the words do not say which: three alternative wordings of ONE
    four-mark answer (2024 Higher 1(e)), or four items of ONE list, each worth
    three (2024 Ordinary 1(f)). Both readings use only numbers the SEC printed;
    what chooses between them is the total the scheme prints on the QUESTION's
    own head, which every leaf of that question must add up to.

    Returns True where exactly one combination of readings hits that total.
    Where none does, or several do, nothing is settled and the caller flags it
    — a question whose arithmetic does not close is not a place to guess.
    """
    options = []
    for a in leaves:
        if not a.splits:
            if a.total is None:
                return False             # an unpriced leaf: nothing to settle
            options.append([a.total])    # priced by a split one level up
            continue
        if a.header_total is not None:
            options.append([a.header_total])
            continue
        cands = {max(t for t, _c, _p in a.splits)}
        priced = [x['marks'] for x in a.answers if x['marks'] is not None]
        if len(priced) > 1:
            cands.add(sum(priced))
        options.append(sorted(cands))
    size = 1
    for o in options:
        size *= len(o)
    if size > MAX_COMBINATIONS:
        return False
    hits = [combo for combo in itertools.product(*options)
            if sum(combo) == head_total]
    if len(hits) != 1:
        return False
    for ask, total in zip(leaves, hits[0]):
        ask.settled = total
    return True


def _walk_down_splits(asks):
    """A split printed one level up, walked down to the parts it prices.

    The SEC prices a lettered ask once — "(d) Encontre no texto palavras … |
    Answer 5 Marks" — and then prints five romans beneath it with one mark
    each. Walked ONLY where the split and the parts agree in number; where they
    do not, each part keeps its own printed mark and nothing is inferred.
    """
    children = collections.defaultdict(list)
    for a in asks:
        if a.roman:
            children[(a.section, a.q, a.letter)].append(a)
    for a in asks:
        if a.roman or a.total is None or a.count is None:
            continue
        kids = children.get((a.section, a.q, a.letter))
        if not kids or len(kids) != a.count:
            continue
        if any(kid.total is not None for kid in kids):
            continue
        for kid in kids:
            kid.total, kid.count, kid.per = a.per, 1, a.per
            kid.notation = (f'{a.notation} on the head of '
                            f'{a.ref_tail()}, walked down to its '
                            f'{a.count} parts')


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


# ----------------------------------------------------------------- the CLI ---
def sittings(subject):
    out = []
    for path in sorted(glob.glob(os.path.join(schemes_dir(subject), '*.pdf'))):
        m = re.match(r'(\d{4})-(hl|ol|cl)\.pdf', os.path.basename(path))
        if m:
            out.append((int(m.group(1)), m.group(2)))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('subject')
    ap.add_argument('year', nargs='?', type=int)
    ap.add_argument('level', nargs='?')
    ap.add_argument('--full', action='store_true')
    ap.add_argument('--audit', action='store_true')
    args = ap.parse_args()

    if args.audit:
        for year, level in sittings(args.subject):
            S = EuScheme(year, level, args.subject)
            reading = S.reading()
            priced = [a for a in reading if a.total]
            answered = [a for a in priced if a.answers]
            faults = [a for a in reading if a.fault]
            print(f'{year} {level.upper():2}  {S.era:7} {len(reading):3} '
                  f'reading asks, {len(priced):3} priced, {len(answered):3} '
                  f'with stated answers, {len(faults)} fault(s), '
                  f'{len(S.listening()):3} listening asks')
            # The independent check on "the ask is worth the LARGEST of the
            # prices printed against it": the leaf totals of a question must
            # add up to the total the scheme prints on that question's head.
            by_q = collections.defaultdict(int)
            for a in reading:
                if a.total:
                    by_q[(a.section, a.q)] += a.total
            for key, want in sorted(S.question_totals.items(), key=str):
                got = by_q.get(key)
                mark = 'OK ' if got == want else 'XX '
                print(f'      {mark} Q{key[1]} head says {want}, leaves add '
                      f'to {got}')
            for a in faults[:4]:
                print(f'      FAULT {a.ref_tail()} — {a.fault}')
        return 0

    S = EuScheme(args.year, args.level, args.subject)
    for a in S.all_asks():
        print(f'{a.section:4} {a.ref_tail():14} {a.notation:26} {a.cue[:70]}')
        if args.full:
            for ans in a.answers:
                print(f'         · {ans["text"][:100]}'
                      + (f'  [{ans["marks"]}m]' if ans['marks'] else ''))
            for ans in a.part:
                print(f'      rung· {ans["text"][:100]}  [{ans["marks"]}m]')
        if a.fault:
            print(f'         FAULT {a.fault}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
