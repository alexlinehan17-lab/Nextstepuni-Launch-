#!/usr/bin/env python3
"""Lithuanian question papers — the printed ask, and which of them is a leaf.

    python3 scripts/markbank/authoring/lt_paper.py 2024 hl
    python3 scripts/markbank/authoring/lt_paper.py 2024 hl --aural
    python3 scripts/markbank/authoring/lt_paper.py --audit

Why this subject needs its own reader
-------------------------------------
Lithuanian is a NON-CURRICULAR EU LANGUAGE (SEC subject 550) and the closest
paper in the bank to Polish, which is the reader this one is modelled on. Three
things about it are its own, and each of them is why `pl_paper` could not
simply be pointed at the files.

**It is THREE examinations, not two.** Polish has an old paper and a new one.
Lithuanian has three, and the corpus holds all of them because it runs from
2010 rather than from 2021:

    2010-2020   I DALIS (30/100) six questions on one text
                II DALIS (30/100) a commentary of 100-150 words
                III DALIS (40/100) an essay, two titles
    2021        I DALIS (30/70) six questions on one text
                II DALIS (40/70) an essay, two titles — no commentary
    2022-2026   Dalis A Skaitymas + Dalis B Rašymas in one booklet,
                and a Listening Comprehension Test in its own ('A00')

**Its questions are numbered in WORDS.** The new paper never prints "1."
against a question. It heads each task with a Lithuanian ordinal — "Pirma
užduotis", "Antra užduotis", "Trečia užduotis" — and the number is in the word.
The scheme prints the digit beside it ("Reading Comprehension 1 / Pirma
užduotis") and the booklet's own English instruction page names the same five:
"Answer Reading Comprehension 1 AND Reading Comprehension 2", then "Question 3
(a) or (b) or (c), Question 4 … AND Question 5". So the ordinal IS the question
number, and both documents say so.

**The digits on the page are answer boxes.** Every ask in the new paper is
followed by numbered ruled lines for the candidate — a bare "1." and "2." at
x≈65, a few points below the ask they belong to. Read as text they are absorbed
into the question ("… Parašykite dvi detales. (3 dalis) 1. 2."); read as
markers they open questions the paper does not ask. A bare number that is a
whole printed row is an answer box in every sitting of this corpus and is
dropped, which is safe because a real question number is printed WITH its
question on the same baseline ("2. Kas Akvilinai Australijoje patinka?").

The page is otherwise read the way `pl_paper` reads Polish, and for the same
reasons: Lithuanian is published as SEPARATE English ('E') and Irish ('I')
editions rather than the bilingual booklet the curricular languages print, so
there are no columns to cut apart; and "(i)" is both the ninth letter and the
first roman here too — 2024 Higher runs Reading Comprehension 2's parts to
"(k)" — so it is settled on the printed column plus the letter sequence, never
on wording.
"""
import argparse
import glob
import os
import re
import sys
import unicodedata

import pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, os.path.dirname(HERE))
from markbank_text import unligature                            # noqa: E402

SUBJECT = 'lithuanian'


def papers_dir(subject=SUBJECT):
    return os.path.join(ROOT, 'examiner-reports', subject, 'papers')


def paper_path(year, level, component=None, subject=SUBJECT):
    """The booklet on disk, whatever the fetcher called it.

    Up to 2021 a sitting is ONE booklet and lands as `2021-hl-paper.pdf` with
    no component token; every later sitting prints two and lands as
    `…-000-paper.pdf` and `…-A00-paper.pdf`.
    """
    stem = f'{year}-{level}'
    for name in ([f'{stem}-{component}-paper.pdf'] if component else
                 [f'{stem}-paper.pdf', f'{stem}-000-paper.pdf']):
        path = os.path.join(papers_dir(subject), name)
        if os.path.exists(path):
            return path
    return None


# --------------------------------------------------------------- the page ---
# The SEC sets these booklets with U+00A0 between every word from 2023 onward
# and with ordinary spaces before that. Folded here so one set of patterns
# reads all seventeen sittings.
NBSP = '   '
# The Symbol and Wingdings space, which those fonts encode in the private-use
# area. It is a space and nothing else, and left as itself it reaches a card as
# an unresolvable glyph the build refuses.
SYMBOL_SPACE = ''
# Page furniture: the running head and foot every page carries.
FURNITURE = re.compile(
    r'^(?:Leaving\s+Certificate|Lithuanian\s*[–—-]\s*(?:Higher|Ordinary)|'
    r'Lithuanian,\s+Listening|Coimisi[úu]n|State\s+Examinations|'
    r'Page\s*\d+|Do\s+not\s+write)\b|^\d{1,3}$', re.I)
# A ruled answer line's own number — "1." alone in a printed row. See the
# module docstring: this is a box for the candidate, never an ask.
# The SEC also rules them ACROSS a row rather than down a column, and the row
# banding then hands back "1. 2. 3." as one printed row: 2024 Ordinary sets
# the answer boxes of its sentence-matching task that way, and a pattern that
# only knew a single number opened a second, empty Q3(e)(1) beside the real
# one. A row whose every cell is a bare number is a rank of answer boxes.
ANSWER_BOX = re.compile(r'^\d{1,2}\s*\.?(?:\s+\d{1,2}\s*\.?)*$')
# The tail the SEC prints under a reading text, which is not part of any ask.
SOURCE_LINE = re.compile(
    r'^(?:Adaptuota|Pagal\b|Parengta\s+pagal|Tekstas?\s+(?:pagal|iš)|'
    r'Šaltinis|Nuotraukos?\s+i[sš]|www\.|https?://)', re.I)
# A bare tariff the SEC prints at the end of an ask, in the right-hand column:
# "(5 taškai)", "(1 taškas)", "(30 taškų)", "5 marks".
TRAILING_MARK = re.compile(
    r'\s*\(?\s*\d{1,3}\s*(?:ta[sš]k\w*|marks?)\s*\)?\s*$', re.I)


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
    """One printed line, with the SEC's broken font glyphs put back.

    `unligature` is the bank's shared map and is used rather than a local one:
    these papers print the tick INSIDE their own rubric — "Pažymėkite (✓)
    teisingą atsakymą" — as the Wingdings U+F0FC, and several sittings set
    "quesƟons" with the same font's ti ligature.
    """
    table = _glyphs(subject)
    out = ''.join(' ' if c in NBSP or c in SYMBOL_SPACE else table.get(c, c)
                  for c in unligature(text))
    return re.sub(r'\s+', ' ', out).strip()


class Line:
    __slots__ = ('page', 'x', 'y', 'x1', 'text', 'cells')

    def __init__(self, page, x, y, x1, text, cells=()):
        self.page, self.x, self.y, self.x1, self.text = page, x, y, x1, text
        self.cells = list(cells)

    def __repr__(self):
        return f'Line(p{self.page} x={self.x:.1f} y={self.y:.1f} {self.text[:60]!r})'


# How far apart two printed lines may sit and still be one printed ROW.
# The SEC sets the marker cell a couple of points off its question's own
# baseline — "(a)" at y=203.5 with its question at y=205.4 — and it sets the
# tariff in a right-hand column on the question's baseline. Both have to be
# gathered or the ask has no marker and the marker has no price.
ROW_TOL = 4.5
# How far above or below its own baseline the text beside a MARKER may sit
# when the two are not on one baseline at all. A marker is set centred in its
# table cell while the sentence beside it wraps around it.
CELL_TOL = 20.0


def read_lines(path, subject=SUBJECT):
    """Every printed row of the booklet, in reading order, marker included."""
    out = []
    with pymupdf.open(path) as doc:
        for pno, page in enumerate(doc, 1):
            raw = []
            for block in page.get_text('dict')['blocks']:
                if block.get('type') != 0:
                    continue
                for line in block['lines']:
                    text = _norm(''.join(s['text'] for s in line['spans']), subject)
                    if not text:
                        continue
                    x0, y0, x1, y1 = line['bbox']
                    raw.append((x0, (y0 + y1) / 2, x1, text))
            raw.sort(key=lambda t: (t[1], t[0]))
            band = []
            for item in raw:
                if band and abs(item[1] - band[0][1]) <= ROW_TOL:
                    band.append(item)
                    continue
                if band:
                    out.append(_row(pno, band))
                band = [item]
            if band:
                out.append(_row(pno, band))
    return _join_markers(out)


def _row(page, band):
    band = sorted(band, key=lambda t: t[0])
    cells = [(x, text) for x, _y, _x1, text in band]
    return Line(page, cells[0][0], band[0][1], max(t[2] for t in band),
                _norm(' '.join(t for _x, t in cells)), cells)


MARKER_ONLY = re.compile(r'^\(?\s*([a-z]{1,4})\s*\)\.?$', re.I)


def _join_markers(rows):
    """Glue a marker printed alone in its cell onto the text beside it.

    Only where the two are NOT already one row: the row banding above has
    already joined every marker the SEC set on its question's own baseline,
    and this catches the rest — a true/false table's roman set half a line
    below the statement it labels.
    """
    out, used = [], set()
    for i, row in enumerate(rows):
        if i in used:
            continue
        if len(row.cells) == 1 and MARKER_ONLY.match(row.cells[0][1]):
            mates = [j for j in range(max(0, i - 4), min(i + 5, len(rows)))
                     if j != i and j not in used
                     and rows[j].page == row.page
                     and rows[j].x > row.x + 4
                     and abs(rows[j].y - row.y) <= CELL_TOL
                     and not MARKER_ONLY.match(rows[j].cells[0][1])
                     and not ANSWER_BOX.match(rows[j].text)]
            if mates:
                # Only the marker's OWN column. A table sets the marker in a
                # narrow cell and the question beside it wraps over three
                # lines, but the page also carries a wider rubric at a
                # different margin within the same band.
                near = min(mates, key=lambda j: abs(rows[j].y - row.y))
                column = rows[near].x
                mates = [j for j in mates if abs(rows[j].x - column) <= 8]
                mates.sort(key=lambda j: (rows[j].y, rows[j].x))
                used.update(mates)
                cells = list(row.cells)
                for j in mates:
                    cells += rows[j].cells
                cells.sort(key=lambda c: c[0])
                row = Line(row.page, row.x,
                           min([row.y] + [rows[j].y for j in mates]),
                           max([row.x1] + [rows[j].x1 for j in mates]),
                           _norm(' '.join(t for _x, t in cells)), cells)
        out.append(row)
    out.sort(key=lambda r: (r.page, r.y, r.x))
    return out


# ------------------------------------------------------------- the markers ---
# The ordinal that heads a task. The SEC numbers nothing on the new paper: it
# writes the number as a word, and the marking scheme prints the digit beside
# the same word ("Reading Comprehension 1 / Pirma užduotis").
ORDINALS = {'pirma': 1, 'antra': 2, 'trečia': 3, 'trecia': 3, 'ketvirta': 4,
            'penkta': 5, 'šešta': 6, 'sesta': 6}
Q_HEAD = re.compile(
    r'^(Pirma|Antra|Tre[čc]ia|Ketvirta|Penkta|[Šš]e[šs]ta)\s+u[žz]duot',
    re.I)
# The section banner the SEC prints across the top of the page each section
# opens on: "Dalis A   Skaitymas   100 taškų".
SECTION_TAB = re.compile(r'^Dalis\s+([AB])\b', re.I)
# The old examination's own parts, printed in Roman numerals.
PART_OLD = re.compile(r'^(I{1,3})\s*DALIS\b', re.I)
# The listening booklet's part tab, printed in the page margin.
AURAL_TAB = re.compile(r'^Section\s+([A-F])\s*$', re.I)
LETTER = re.compile(r'^\(?\s*([a-l])\s*\)\s*(.*)$', re.I)
ROMAN = re.compile(r'^\(\s*(i{1,3}|iv|vi{0,3}|ix|x)\s*\)\s*(.*)$', re.I)
NUMBERED = re.compile(r'^(\d{1,2})\s*\.\s*(.+)$')
LETTERS = 'abcdefghijkl'
# Rubric printed between asks, which belongs to no ask.
RUBRIC = re.compile(
    r'^(?:Atsakykite\s+į\s+klausim|Answer\s+(?:the\s+)?question|'
    r'Pa[žz]ym[eė]kite\s*\(|Answer\s+multiple|You\s+will\s+hear|'
    r'The\s+(?:conversation|material|item)\b|Perskaitykite\s+tekst|'
    r'Atlikite\b|Pasirinkite\b|Remdamiesi\s+tekstu\s+atsakykite|'
    r'ARBA\s*$|arba\s*$|Item\s+\d)', re.I)
# How far below a kept line the next one may sit and still be the same ask.
LINE_GAP = 32.0


class Ask:
    __slots__ = ('section', 'q', 'letter', 'roman', 'text', 'page', 'stem')

    def __init__(self, section, q, letter, roman, text, page):
        self.section, self.q = section, q
        self.letter, self.roman = letter, roman
        self.text, self.page = text, page
        self.stem = ''

    @property
    def key(self):
        """The address the PAPER prints: its part tab, then its number.

        The section is part of the address wherever a paper prints one — see
        pl_paper.Ask.key, whose reasoning this follows. Here it carries more
        than a tab: the old examination's I/II/III DALIS restart their
        numbering, and the listening booklet numbers from 1 inside each of its
        five sections.
        """
        return (self.section, self.q, self.letter, self.roman)

    @property
    def full_text(self):
        """The ask as a reader meets it: its parent's stem, then its own."""
        if self.stem and len(self.text) < 60:
            return _norm(f'{self.stem} {self.text}')
        return self.text

    def __repr__(self):
        return f'Ask({self.key} {self.text[:60]!r})'


class LtPaper:
    """One sitting's booklets, walked into the leaf asks they print."""

    def __init__(self, year, level, subject=SUBJECT):
        self.year, self.level, self.subject = year, level, subject
        self.path = paper_path(year, level, None, subject)
        if self.path is None:
            raise FileNotFoundError(f'no Lithuanian paper for {year} {level}')
        self.aural_path = paper_path(year, level, 'A00', subject)
        self.lines = [l for l in read_lines(self.path, subject)
                      if not ANSWER_BOX.match(l.text)]
        self.flags = []
        self.text_pages = {}          # (section, q) -> [pages of its text]
        self.leads = {}               # (section, q) -> its printed title
        self.letter_x_by_q = {}
        self.letter_x = self._letter_column()
        self.era = 'new' if year >= 2022 else ('old2' if year == 2021 else 'old3')
        self._asks = self._walk() if self.era == 'new' else self._walk_old()
        self._aural = self._walk_aural() if self.aural_path else []

    # ------------------------------------------------------------ layout ---
    def _letter_column(self):
        """Where a part LETTER is printed, PER QUESTION, from the markers that
        cannot lie.

        a-h and j-l are letters and nothing else; only "(i)" can be read two
        ways, and it has to pass the sequence test as well. The MODE, never
        the minimum — see pl_paper._letter_column, which paid for that.
        """
        by_q, q = {}, None
        for line in self.lines:
            head = Q_HEAD.match(line.text)
            if head:
                q = ORDINALS[_fold_key(head.group(1))]
                continue
            if re.match(r'^\(?\s*[a-hj-l]\s*\)[\s)]', line.text):
                by_q.setdefault(q, []).append(round(line.x))
        self.letter_x_by_q = {k: max(set(v), key=v.count) for k, v in by_q.items()}
        every = [x for v in by_q.values() for x in v]
        return max(set(every), key=every.count) if every else 56.7

    def _column_for(self, q):
        return self.letter_x_by_q.get(q, self.letter_x)

    def _is_letter(self, x, prev_letter, q=None, idx=None):
        """Is this "(i)" the ninth letter or the first roman?

        Three conditions, never one — pl_paper._is_letter's two, plus the run
        test that reads what follows (see _i_opens_a_roman_run). An indented
        true/false roman sits close enough to the margin that indent alone
        would read it as a letter, and a question that runs to (i) makes the
        sequence test agree with the wrong answer.
        """
        if idx is not None and _i_opens_a_roman_run(self.lines, idx):
            return False
        return x <= self._column_for(q) + LETTER_TOL and prev_letter == 'h'

    # ------------------------------------------------------------- walking --
    def _walk(self):
        """2022 onward: Dalis A Skaitymas and Dalis B Rašymas in one booklet."""
        asks, section, q = [], None, None
        letter = roman = None
        current, last_y = None, None
        text_pages, leads = {}, {}

        def close():
            nonlocal current
            if current is not None:
                current.text = TRAILING_MARK.sub('', _norm(current.text))
                asks.append(current)
                current = None

        # The Dalis banner is a property of the PAGE its section opens on, and
        # pymupdf may report it after the questions beside it. Resolved per
        # page before the walk — pl_paper._section_by_page's reasoning.
        by_page = _section_by_page(self.lines, SECTION_TAB)

        for idx, line in enumerate(self.lines):
            if FURNITURE.match(line.text) and len(line.text) < 60:
                continue
            section = by_page.get(line.page, section)
            if SECTION_TAB.match(line.text):
                continue
            head = Q_HEAD.match(line.text)
            if head:
                close()
                q = ORDINALS[_fold_key(head.group(1))]
                letter = roman = None
                last_y = None
                leads[(section, q)] = TRAILING_MARK.sub('', line.text)
                continue
            if q is None:
                continue
            lm = LETTER.match(line.text)
            rm = ROMAN.match(line.text)
            nm = NUMBERED.match(line.text)
            marker = None
            # A numbered row UNDER a letter is a sub-ask, not a paragraph.
            # The SEC numbers the rows of a true/false table and of a
            # sentence-matching task "1." to "5." where it numbers the rows of
            # an ordering task "(i)" to "(vi)", and both are addresses a
            # candidate answers separately: 2026 Ordinary prices Q1(h)
            # "3 Marks (3 x 1)" over three numbered statements, each with its
            # own tick. Read as prose they were absorbed into the rubric above
            # them and three asks a sitting censused as one. Only under a
            # letter, because the reading TEXT is set in numbered paragraphs
            # too — and those are printed before any letter of their task.
            # Dalis A only, because in Dalis B a numbered row is a PROMPT
            # inside one written task rather than an ask of its own: the SEC
            # sets Question 5's form-filling task as four numbered questions
            # and its neighbour Question 4 as four bulleted ones, and the
            # scheme prices each task once, whole, against a marking grid.
            if nm and letter is not None and section == 'A' \
                    and not lm and not rm:
                close()
                roman = nm.group(1)
                current = Ask(section, q, letter, roman, nm.group(2), line.page)
                last_y = line.y
                continue
            if rm and not (rm.group(1).lower() == 'i'
                           and self._is_letter(line.x, letter, q, idx)):
                marker = ('roman', rm.group(1).lower(), rm.group(2))
            elif lm and (not rm or self._is_letter(line.x, letter, q, idx)):
                # A letter marker stands at the question's own left margin. A
                # word that merely begins with a bracketed letter does not.
                if line.x <= self._column_for(q) + LETTER_TOL \
                        or lm.group(1).lower() == next_letter(letter):
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
                current = Ask(section, q, letter, roman, rest, line.page)
                last_y = line.y
                continue
            if current is not None and line.page == current.page \
                    and last_y is not None and 0 <= line.y - last_y <= LINE_GAP \
                    and not RUBRIC.match(line.text):
                current.text += ' ' + line.text
                last_y = line.y
                continue
            close()
            # Everything printed before the first ask of a task is its reading
            # text, and the card carries those pages beside the ask.
            if letter is None and not SOURCE_LINE.match(line.text):
                text_pages.setdefault((section, q), [])
                if line.page not in text_pages[(section, q)]:
                    text_pages[(section, q)].append(line.page)
        close()
        self.text_pages, self.leads = text_pages, leads
        self._check_sections(asks)
        return asks

    # The old examination sets ONE text and asks six numbered questions about
    # it in I DALIS; the first lists five expressions a) to e). II and III
    # DALIS are writing tasks — a commentary and an essay before 2021, an
    # essay alone in 2021.
    def _walk_old(self):
        asks, part, q, letter = [], None, None, None
        current, last_y = None, None
        text_pages = {}

        def close():
            nonlocal current
            if current is not None:
                current.text = TRAILING_MARK.sub('', _norm(current.text))
                asks.append(current)
                current = None

        for line in self.lines:
            if FURNITURE.match(line.text) and len(line.text) < 60:
                continue
            pm = PART_OLD.match(line.text)
            if pm:
                close()
                part, q, letter = pm.group(1).upper(), None, None
                last_y = None
                continue
            if part is None:
                # Everything before I DALIS is the reading text.
                if not SOURCE_LINE.match(line.text):
                    text_pages.setdefault('text', [])
                    if line.page not in text_pages['text']:
                        text_pages['text'].append(line.page)
                continue
            nm = NUMBERED.match(line.text)
            lm = LETTER.match(line.text)
            if nm:
                close()
                q, letter = int(nm.group(1)), None
                rest = nm.group(2)
                # "2. a) Kas yra Sigitas Tamkevičius? (1 taškas)" — the SEC
                # glues a question number and its first LETTER onto one
                # printed row. Reading only the number filed that ask under
                # the question itself and left its sibling "b)" as the only
                # letter of Question 2, which the census reported as a
                # letter-gap starting at (b).
                inner = LETTER.match(rest)
                if inner and part == 'I':
                    letter, rest = inner.group(1).lower(), inner.group(2)
                current = Ask(part, q, letter, None, rest, line.page)
                last_y = line.y
                continue
            if lm and q is not None and part == 'I':
                close()
                letter = lm.group(1).lower()
                current = Ask(part, q, letter, None, lm.group(2), line.page)
                last_y = line.y
                continue
            if RUBRIC.match(line.text) and current is None:
                continue
            if current is not None and last_y is not None \
                    and 0 <= line.y - last_y <= LINE_GAP \
                    and line.page == current.page:
                current.text += ' ' + line.text
                last_y = line.y
                continue
            # II DALIS before 2021 is ONE unnumbered task: the SEC prints the
            # instruction and, under it, the extract to comment on. The two
            # are set far enough apart that a line-gap test closes between
            # them, and closing there censused ONE printed task as two asks in
            # 2014. The part holds one ask and everything printed in it
            # belongs to that ask.
            if part == 'II' and self.era == 'old3' and q is None:
                if current is None:
                    current = Ask(part, None, None, None, line.text, line.page)
                else:
                    current.text += ' ' + line.text
                last_y = line.y
                continue
            close()
        close()
        self.text_pages = {('I', qq): text_pages.get('text', [])
                           for qq in range(1, 7)}
        self.leads = {}
        return asks

    def _check_sections(self, asks):
        """The banner and the question numbers must tell the same story."""
        by_q = {}
        for a in asks:
            by_q.setdefault(a.q, set()).add(a.section)
        for q, secs in sorted(by_q.items(), key=lambda t: (t[0] is None, t[0])):
            if len(secs) > 1:
                self.flags.append(
                    {'type': 'section-split', 'where': f'Q{q}',
                     'detail': f'the same question is tabbed {sorted(secs)}'})
        reading = sorted(q for q, s in by_q.items() if s == {'A'})
        writing = sorted(q for q, s in by_q.items() if s == {'B'})
        if reading and writing and max(reading) >= min(writing):
            self.flags.append(
                {'type': 'section-order', 'where': '',
                 'detail': f'Dalis A holds {reading} and Dalis B {writing}'})
        if None in {a.section for a in asks}:
            self.flags.append({'type': 'section-missing', 'where': '',
                               'detail': 'an ask was printed before any Dalis banner'})

    # ----------------------------------------------------------- listening --
    def _walk_aural(self):
        """The Listening Comprehension booklet's own asks.

        Counted, never carded: the ask can only be answered from the recording.
        The count is what the denominator needs and what the exclusions ledger
        has to match one for one.
        """
        asks, section, item, letter = [], None, None, None
        current, last_y = None, None

        def close():
            nonlocal current
            if current is not None:
                current.text = _norm(current.text)
                asks.append(current)
                current = None

        raw = read_lines(self.aural_path, self.subject)
        # An ITEM HEAD is a bare number too. Section E of 2026 Ordinary sets
        # "1. (a) Juneta was 20 years old." and then a bare "2." above its own
        # (a) and (b), and dropping every bare number as an answer box lost
        # that head — so the second item's parts were filed under the first
        # and the census keyed two printed asks onto one address. The two are
        # told apart by the COLUMN: an item head stands at the margin its own
        # section's numbered asks stand at (x=80.2 there, x=56.7 in 2024
        # Higher), and an answer box is indented past it (x=65.4 under a head
        # at 56.7). The column is measured from the item heads that carry
        # their own text, which cannot be anything else.
        item_xs = [round(l.x) for l in raw
                   if re.match(r'^\d{1,2}\.\s+\S', l.text)]
        item_x = max(set(item_xs), key=item_xs.count) if item_xs else None
        lines = [l for l in raw
                 if not ANSWER_BOX.match(l.text)
                 or (item_x is not None and abs(l.x - item_x) <= 4
                     and re.fullmatch(r'\d{1,2}\s*\.?', l.text))]
        by_page = _section_by_page(lines, AURAL_TAB)
        for line in lines:
            if FURNITURE.match(line.text) and len(line.text) < 60:
                continue
            page_section = by_page.get(line.page)
            if page_section != section:
                close()
                section, item, letter = page_section, None, None
            if AURAL_TAB.match(line.text):
                continue
            if section is None:
                continue
            nm = NUMBERED.match(line.text)
            lm = LETTER.match(line.text)
            rm = ROMAN.match(line.text)
            if re.fullmatch(r'\d{1,2}\s*\.?', line.text):
                close()
                item, letter = int(line.text.rstrip('.')), None
                continue
            if nm:
                close()
                item = int(nm.group(1))
                rest = nm.group(2)
                letter = None
                inner = LETTER.match(rest)
                if inner:
                    letter, rest = inner.group(1).lower(), inner.group(2)
                current = Ask(f'L{section}', item, letter, None, rest, line.page)
                last_y = line.y
                continue
            # A roman under a letter is a sub-ask here as well: 2026 Ordinary
            # Section C heads "2.(a) Indicate whether the following statements
            # are True or False" and prints three statements "(i)" to "(iii)"
            # beneath it. Welded into the letter they censused as one ask
            # where the booklet prints three.
            if rm and item is not None and letter is not None:
                close()
                current = Ask(f'L{section}', item, letter,
                              rm.group(1).lower(), rm.group(2), line.page)
                last_y = line.y
                continue
            if lm and item is not None:
                close()
                letter = lm.group(1).lower()
                current = Ask(f'L{section}', item, letter, None,
                              lm.group(2), line.page)
                last_y = line.y
                continue
            if RUBRIC.match(line.text):
                close()
                continue
            if current is not None and last_y is not None \
                    and 0 <= line.y - last_y <= LINE_GAP \
                    and line.page == current.page:
                current.text += ' ' + line.text
                last_y = line.y
                continue
            close()
        close()
        return asks

    # ------------------------------------------------------------- the API --
    def all_asks(self):
        """Every leaf the booklets print: a lettered ask with romans under it
        is not a leaf, its romans are."""
        asks = self._asks + self._aural
        has_roman = {(a.section, a.q, a.letter) for a in asks if a.roman}
        has_letter = {(a.section, a.q) for a in asks if a.letter}
        parents = {(a.section, a.q, a.letter): a for a in asks
                   if a.roman is None}
        parents.update({(a.section, a.q, None): a for a in asks
                        if a.letter is None and a.roman is None})
        out = []
        for a in asks:
            if a.roman:
                parent = parents.get((a.section, a.q, a.letter))
                a.stem = parent.text if parent is not None else ''
                out.append(a)
            elif a.letter:
                parent = parents.get((a.section, a.q, None))
                if parent is not None and parent is not a:
                    a.stem = parent.text
                if (a.section, a.q, a.letter) not in has_roman:
                    out.append(a)
            elif (a.section, a.q) not in has_letter \
                    and (a.section, a.q, None) not in has_roman:
                out.append(a)
        return out

    def reading_asks(self):
        return [a for a in self.all_asks() if a.section in ('A', 'I')]

    def writing_asks(self):
        return [a for a in self.all_asks() if a.section in ('B', 'II', 'III')]

    def aural_asks(self):
        return [a for a in self.all_asks() if (a.section or '').startswith('L')]

    def lead(self, section, q):
        return self.leads.get((section, q), '')

    def pages_for(self, section, q):
        """The pages of the reading text this task is set on."""
        return self.text_pages.get((section, q)) or []

    PART_TOTAL = re.compile(r'\(\s*(\d{2,3})\s*/\s*(\d{2,3})\s*\)')

    def cover_marks(self):
        """What the paper states its own total is.

        The old examination prints no "N marks" line on its cover at all — it
        prints "3 hours" — and states its total instead on the head of every
        part, as a fraction of the whole: "I DALIS (30 /100)", "II DALIS
        (30/100)", "III DALIS (40/100)". The DENOMINATOR of that fraction is
        the paper's own total and it is stated three times over, so it is read
        from the head and checked against the parts that share it. Left to the
        cover-line reader every sitting before 2022 reported a total of zero
        and the cross-year checksum had nothing to compare.
        """
        if self.era != 'new':
            wholes, parts = set(), 0
            for line in self.lines:
                if not PART_OLD.match(line.text):
                    continue
                m = self.PART_TOTAL.search(line.text)
                if m:
                    wholes.add(int(m.group(2)))
                    parts += int(m.group(1))
            if len(wholes) == 1:
                whole = next(iter(wholes))
                if parts != whole:
                    self.flags.append(
                        {'type': 'marks-parts', 'where': '',
                         'detail': f'the part heads add to {parts} against a '
                                   f'stated total of {whole}'})
                return whole
            return 0
        total = 0
        for path in [self.path] + ([self.aural_path] if self.aural_path else []):
            with pymupdf.open(path) as doc:
                m = re.search(r'(\d{2,3})\s*marks\b', _norm(doc[0].get_text()), re.I)
            if m:
                total += int(m.group(1))
        return total


# How far right of the letter column a marker may still be a LETTER.
# Measured, not guessed — pl_paper.LETTER_TOL's reasoning, and the same eight
# points: the SEC's own table cells drift by three to five points inside one
# page, and the only marker that can be read two ways is "(i)", which has to
# satisfy the sequence test as well.
LETTER_TOL = 8.0


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



def _fold_key(word):
    return unicodedata.normalize('NFKD', word.lower())[0:1] and word.lower()


def _section_by_page(lines, pattern):
    """{page: section}, the tab carrying forward until the next one."""
    seen, out, current = {}, {}, None
    for line in lines:
        m = pattern.match(line.text)
        if m and line.page not in seen:
            seen[line.page] = m.group(1).upper()
    for page in range(1, max((l.page for l in lines), default=0) + 1):
        current = seen.get(page, current)
        out[page] = current
    return out


# --------------------------------------------------------------- matching ---
WORD = re.compile(r"[^\W\d_]+", re.UNICODE)
# Words too common in Lithuanian or English to be evidence of anything.
STOP = {
    'the', 'a', 'an', 'of', 'to', 'in', 'and', 'or', 'for', 'is', 'are', 'on',
    'at', 'by', 'with', 'from', 'that', 'this', 'it', 'as', 'be', 'what',
    'which', 'how', 'why', 'does', 'do', 'did', 'was', 'were', 'has', 'have',
    'give', 'details', 'detail', 'about', 'his', 'her', 'him', 'she', 'they',
    'yra', 'nes', 'kad', 'bet', 'apie', 'kaip', 'kai', 'del', 'del', 'jis',
    'jos', 'jam', 'jai', 'tai', 'tas', 'tos', 'sio', 'siu', 'ir', 'su',
    'parasykite', 'nurodykite', 'detales', 'detale', 'dalis', 'tekste',
    'tekstu', 'teksto',
}


def fold(text):
    """Lower-cased and accent-stripped, so ė and e are one word.

    Lithuanian diacritics survive the text layer intact — ą č ę ė į š ų ū ž
    all reach it, and every one of them is Latin Extended-A — so this is a
    matching convenience, not a repair.
    """
    text = (text or '').lower()
    return ''.join(c for c in unicodedata.normalize('NFKD', text)
                   if not unicodedata.combining(c))


def bag(text):
    return {w for w in WORD.findall(fold(text)) if w not in STOP and len(w) > 2}


def score(a, b):
    """Shared content words over the LONGER side — fr_paper.score's reasoning."""
    if not a or not b:
        return 0.0
    return len(a & b) / max(len(a), len(b))


# ----------------------------------------------------------------- the CLI ---
def sittings(subject=SUBJECT):
    out = set()
    for path in glob.glob(os.path.join(papers_dir(subject), '*-paper.pdf')):
        m = re.match(r'(\d{4})-(hl|ol|cl)', os.path.basename(path))
        if m:
            out.add((int(m.group(1)), m.group(2)))
    return sorted(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('year', nargs='?', type=int)
    ap.add_argument('level', nargs='?')
    ap.add_argument('--aural', action='store_true')
    ap.add_argument('--audit', action='store_true')
    ap.add_argument('--subject', default=SUBJECT)
    args = ap.parse_args()

    if args.audit:
        for year, level in sittings(args.subject):
            P = LtPaper(year, level, args.subject)
            print(f'{year} {level.upper():2} {P.era:5} {len(P.all_asks()):4} leaves '
                  f'({len(P.reading_asks())} reading, {len(P.writing_asks())} writing, '
                  f'{len(P.aural_asks())} listening)  cover {P.cover_marks()} marks'
                  f'  letter column x={P.letter_x:.1f}')
            for f in P.flags:
                print(f'      FLAG {f["type"]} {f["where"]} — {f["detail"]}')
        return 0

    P = LtPaper(args.year, args.level, args.subject)
    asks = P.aural_asks() if args.aural else [
        a for a in P.all_asks() if not (a.section or '').startswith('L')]
    for a in asks:
        label = f'{a.section} Q{a.q}' + (f'({a.letter})' if a.letter else '')
        label += f'({a.roman})' if a.roman else ''
        print(f'p{a.page:<3} {label:22} {a.text[:110]}')
    print(f'\n{len(asks)} leaf ask(s)')
    for f in P.flags:
        print(f'FLAG {f["type"]} {f["where"]} — {f["detail"]}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
