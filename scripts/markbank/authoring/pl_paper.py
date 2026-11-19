#!/usr/bin/env python3
"""Polish question papers — the printed ask, and which of them is a leaf.

    python3 scripts/markbank/authoring/pl_paper.py 2024 hl
    python3 scripts/markbank/authoring/pl_paper.py 2022 ol --aural
    python3 scripts/markbank/authoring/pl_paper.py --audit

Why this subject needs its own reader
-------------------------------------
Polish is a NON-CURRICULAR EU LANGUAGE (SEC subject 548), and almost nothing
about its booklets is the shape the six carded languages print.

**It is not bilingual.** French, German, Spanish, Italian, Russian and Japanese
each publish ONE booklet with the Irish and English rubrics set in columns —
language letter 'B' — and every one of those readers exists mostly to cut the
columns apart. Polish publishes two SEPARATE editions instead, `…EV.pdf` in
English and `…IV.pdf` in Irish, so there are no columns to cut and the page is
read straight.

**Its passage is not a decoy.** The French reader has to score wording against
the scheme to say which "1." on the page opens an ask, because the reading
passage is set in numbered paragraphs at the same margin. Polish numbers its
passage paragraphs too — "1. Droga blogerko…" — but it letters its questions,
"(a)" to "(k)", so no marker is ever ambiguous between the two.

**One marker IS ambiguous, and only one.** "(i)" is both the ninth letter and
the first roman, and this paper prints it as both: 2022 Higher runs its
Question 1 parts to "(k)", so its "(i)" is a letter, while 2023 Higher sets
"(i)" and "(ii)" under "(h)" as romans. The page settles it and the wording
never has to: a letter is printed at the question's own left margin (x≈56.7)
and a roman is indented past it. Both conditions are required — the marker
stands at the letter column AND the letter before it was "h" — because the
Ordinary true/false tables set their romans only five points in from the
margin, close enough that indent alone would read them as letters.

**Two levels, and only since 2022.** Up to and including 2021 Polish is sat at
ONE level, and the SEC's file id says so with the level letter 'A' and its
cover with the words "Higher Level" — it is Higher-only, not the common level
'C' that LCVP carries. It is also a different examination: one 70-mark booklet
of six numbered questions on a text plus an essay, with no listening test at
all. From 2022 it is sat at two levels as three documents' worth of assessment
in two booklets — Section A Reading and Section B Written Production in the
written booklet (component 000), and a Listening Comprehension Test in its own
(component A00). So the 2021 sitting is walked by its own path.

The section is read from the paper TWICE and the two must agree: from the
"Część A"/"Część B" tab the SEC prints beside the first question of each, and
from the question numbers themselves. A paper where they disagree has lost a
section boundary, and `--audit` says so rather than guessing.
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

SUBJECT = 'polish'


def papers_dir(subject=SUBJECT):
    return os.path.join(ROOT, 'examiner-reports', subject, 'papers')


def paper_path(year, level, component=None, subject=SUBJECT):
    """The booklet on disk, whatever the fetcher called it.

    2021 is a single booklet and lands as `2021-hl-paper.pdf` with no component
    token; every later sitting prints two and lands as `…-000-paper.pdf` and
    `…-A00-paper.pdf`. Requiring the component silently found nothing for 2021.
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
# reads all five sittings.
NBSP = '   '
# The Symbol and Wingdings space, which those fonts encode in the private-use
# area. It is a space and nothing else, and left as itself it reaches a card
# as an unresolvable glyph the build refuses.
SYMBOL_SPACE = '\uf020\uf0a0'
# Page furniture: the running head and foot every page carries.
# The page NUMBER is the whole line and nothing else. Written as an
# alternative inside the run of names it was `\d{1,3}\b`, which matches the
# "1." opening an ask — so every listening item whose question ran under sixty
# characters was thrown away as furniture, and four fifths of the Listening
# Comprehension Test censused as absent.
FURNITURE = re.compile(
    r'^(?:Leaving\s+Certificate|Polish\s*[–—-]\s*(?:Higher|Ordinary)|'
    r'Coimisi[úu]n|State\s+Examinations|Page\s*\d+)\b|^\d{1,3}$', re.I)
# The tail the SEC prints under a reading text, which is not part of any ask.
SOURCE_LINE = re.compile(r'^(?:Opracowano|Na podstawie|Tekst\s+(?:zaczerpni|opracow))',
                         re.I)


# A bare mark the SEC prints at the end of an ask, in the right-hand column:
# "(5)", "(5 × 1)". It is the price, not part of the question.
TRAILING_MARK = re.compile(r'\s*\(\s*\d{1,2}\s*(?:[x×]\s*\d{1,2}\s*)?\)\s*$')


def _norm(text):
    """One printed line, with the SEC's broken font glyphs put back.

    `unligature` is the bank's shared map and is used rather than a local one:
    these papers print the tick INSIDE their own rubric — "Put a tick (✓) in
    the appropriate box" — as the Wingdings U+F0FC, and the 2024 and 2025
    Ordinary papers set "secƟon" and "quesƟons" with the same font's ti
    ligature. A card carrying either read "Put a tick () in the appropriate
    box" and "(secƟon 6)".
    """
    out = ''.join(' ' if c in NBSP or c in SYMBOL_SPACE else c
                  for c in unligature(text))
    return re.sub(r'\s+', ' ', out).strip()


class Line:
    __slots__ = ('page', 'x', 'y', 'x1', 'text')

    def __init__(self, page, x, y, x1, text):
        self.page, self.x, self.y, self.x1, self.text = page, x, y, x1, text

    def __repr__(self):
        return f'Line(p{self.page} x={self.x:.1f} y={self.y:.1f} {self.text[:60]!r})'


def read_lines(path):
    """Every printed line, in reading order, with the marker column intact.

    A part marker is set in its own table cell — "(b)" at x=56.7 and its
    question at x=85.1 on the same baseline — so the two are joined back
    together here. Left apart, every lettered ask in the corpus reads as an
    empty leaf.
    """
    out = []
    with pymupdf.open(path) as doc:
        for pno, page in enumerate(doc, 1):
            raw = []
            for block in page.get_text('dict')['blocks']:
                if block.get('type') != 0:
                    continue
                for line in block['lines']:
                    text = _norm(''.join(s['text'] for s in line['spans']))
                    if not text:
                        continue
                    x0, y0, x1, y1 = line['bbox']
                    raw.append(Line(pno, x0, (y0 + y1) / 2, x1, text))
            raw.sort(key=lambda l: (round(l.y, 0), l.x))
            out += _join_markers(raw)
    return out


MARKER_ONLY = re.compile(r'^\(\s*([a-z]{1,4})\s*\)\.?$|^(\d{1,2})\s*\.$', re.I)
# How far above or below its own baseline the text beside a marker may sit.
# A marker is set CENTRED in its table cell while the sentence beside it wraps
# around it: 2024 Higher Q2(i)(i) prints "(i)" at y=645 with "Our level of
# happiness depends on the number of friends we have." at y=638 and
# "(paragraph 4)" at y=652. Looking forward on one baseline kept the second
# half and threw the statement itself away, and the ask censused as the empty
# leaf "(paragraph 4)". So the whole cell is gathered, above and below.
CELL_TOL = 20.0

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


def _join_markers(lines):
    """Glue a marker printed alone in its cell onto the text beside it."""
    out, used = [], set()
    for i, line in enumerate(lines):
        if i in used:
            continue
        if MARKER_ONLY.match(line.text):
            mates = [j for j in range(max(0, i - 4), min(i + 5, len(lines)))
                     if j != i and j not in used and lines[j].x > line.x + 4
                     and abs(lines[j].y - line.y) <= CELL_TOL
                     and not MARKER_ONLY.match(lines[j].text)]
            if mates:
                # Only the marker's OWN column. A table sets the marker in a
                # narrow cell and the question beside it wraps over three
                # lines, but the page also carries a wider rubric at a
                # different margin within the same band, and a purely vertical
                # window pulled that in instead of the question.
                near = min(mates, key=lambda j: abs(lines[j].y - line.y))
                column = lines[near].x
                mates = [j for j in mates if abs(lines[j].x - column) <= 8]
                mates.sort(key=lambda j: (lines[j].y, lines[j].x))
                used.update(mates)
                body = ' '.join(lines[j].text for j in mates)
                out.append(Line(line.page, line.x,
                                min([line.y] + [lines[j].y for j in mates]),
                                max(lines[j].x1 for j in mates),
                                f'{line.text} {body}'))
                continue
        out.append(line)
    return out


# ------------------------------------------------------------- the markers ---
# The head of a reading text or a written-production task. Higher heads them
# "Pytanie 1"; Ordinary heads them "Zadanie 1: Tekst 1" in Section A and
# "Zadanie 4" in Section B.
Q_HEAD = re.compile(r'^(?:Pytanie|Zadanie)\s*(\d{1,2})\b')
# The section tab, printed once beside the first question of each section.
SECTION_TAB = re.compile(r'^Cz[eę][sś][cć]\s+([AB])\b')
# 2021's own two parts, printed in Roman numerals.
PART_2021 = re.compile(r'^Cz[eę][sś][cć]\s+(I{1,2})\b')
# The examination up to 2020 prints THREE parts, and 2011 and 2012 set their
# heads in capitals, "CZĘŚĆ I". PART_2021 knows neither: it is case-sensitive
# and stops at "II", so those two sittings found no part at all and every other
# year lost Część III, and with it both essay titles.
PART_CLASSIC = re.compile(r'^Cz[eę][sś][cć]\s+(I{1,3})\b', re.I)
# The share of the paper printed beside each part head, "(30/100)". It is the
# part's price, not part of the prompt beneath it.
PART_SHARE = re.compile(r'^\(\s*\d{1,3}\s*/\s*\d{1,3}\s*\)$')
# The word the SEC prints between the two essay titles of the last part.
CHOICE_WORD = re.compile(r'^(?:ALBO|LUB)$', re.I)
# A lettered part of the 100-mark examination, which sets it "a)" in most
# years and "a." in 2020 ("a. cała gama (akapit 1)"). A letter is only ever
# taken here when it is the NEXT letter of its question, so the dot cannot turn
# a line of a question's own words into a part.
LETTER_CLASSIC = re.compile(r'^\(?\s*([a-l])\s*[.)]\s*(.*)$', re.I)
# Parts printed INSIDE their question's sentence: 2019 Question 3 reads "W
# świetle artykułu, a) jak wygląda, i b) jak działa robot-zapylacz…", and the
# scheme gives (a) 2 marks and (b) 3. Both markers have to be there, in order,
# each after a space, so a lone bracketed letter in a quotation is left alone.
INLINE_PARTS = re.compile(r'^(.*?)(?:^|\s)a\)\s+(.+?)\s+b\)\s+(.+)$')
# A 2021 essay title: the SEC prints it as a quotation attributed to its author.
ESSAY_TITLE = re.compile(r'^[„“"]')
AURAL_TAB = re.compile(r'^Cz[eę][sś][cć]\s+([A-F])\b')
# A lettered sub-question in the listening booklet. Only (a)-(h): "(i)" there
# is always a roman, an answer box or a table row.
AURAL_LETTER = re.compile(r'^\(\s*([a-h])\s*\)\s*(\S.*)$')
LETTER = re.compile(r'^\(?\s*([a-l])\s*\)\s*(.*)$', re.I)
ROMAN = re.compile(r'^\(\s*(i{1,3}|iv|vi{0,3}|ix|x)\s*\)\s*(.*)$', re.I)
NUMBERED = re.compile(r'^(\d{1,2})\s*\.\s*(.*)$')
ROMANS = ['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x']
LETTERS = 'abcdefghijkl'
# Rubric printed between asks, which belongs to no ask.
RUBRIC = re.compile(
    r'^(?:Answer\b|Odpowiedz\b|Odpowiedzi\b|Uwaga\b|Note\b|Wszystkie\b|'
    r'Napisz\s+(?:jedno|na)\b|Przeczytaj\b|W\s+swojej\b)', re.I)
# How far below a kept line the next one may sit and still be the same ask.
# Below the ask comes the answer space, which is blank.
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
        """The address the PAPER prints: its section tab, then its number.

        The written booklet numbers its questions 1 to 5 straight THROUGH its
        two sections, so the section carries no information an ask needs — and
        it was keyed None for exactly that reason, until the listening booklet
        showed why it cannot be. A citation with no section token matches any
        leaf the census keyed with none, and reconcile then read "2022 HL
        Q2(i)(i)" onto the LISTENING booklet's Section A question 2, which
        numbers from 1 inside each of its own five parts. Fourteen asks
        reported open while their exclusions reported stale, both for the same
        reason. The section is part of the address wherever a paper prints one.
        """
        return (self.section, self.q, self.letter, self.roman)

    @property
    def full_text(self):
        """The ask as a reader meets it: its parent's stem, then its own.

        A table cell is an ask whose printed words are "matka", "Igor" or
        "Data" — the question is in the row above it, and without it the census
        reports an empty leaf and a card would ask nothing at all.
        """
        if self.stem and len(self.text) < 60:
            return _norm(f'{self.stem} {self.text}')
        return self.text

    def __repr__(self):
        return f'Ask({self.key} {self.text[:60]!r})'


class PlPaper:
    """One sitting's booklets, walked into the leaf asks they print."""

    def __init__(self, year, level, subject=SUBJECT):
        self.year, self.level, self.subject = year, level, subject
        self.path = paper_path(year, level, None, subject)
        if self.path is None:
            raise FileNotFoundError(f'no Polish written paper for {year} {level}')
        self.aural_path = paper_path(year, level, 'A00', subject)
        self.lines = read_lines(self.path)
        self.letter_x = self._letter_column()
        self.flags = []
        self.text_pages = {}          # question number -> [pages of its text]
        self.leads = {}               # question number -> its printed title
        self._asks = (self._walk_classic() if year <= 2020
                      else self._walk_2021() if year == 2021
                      else self._walk())
        self._aural = self._walk_aural() if self.aural_path else []

    # ------------------------------------------------------------ layout ---
    def _letter_column(self):
        """Where a part LETTER is printed, measured from the unambiguous ones.

        a-h and j-l are letters and nothing else; only "(i)" can be read two
        ways. So the column is measured from the markers that cannot lie, and
        "(i)" is then tested against it.

        The MODE, never the minimum. 2024 Ordinary sets one marker four points
        left of the column its other thirty sit in — "(a) Dopasuj śródtytuły"
        at x=52.7 where the rest stand at 56.7 — and a minimum took that
        outlier as the column, put every real letter outside the tolerance and
        lost all thirty-one lettered asks in that sitting with no flag raised.
        """
        by_q, q = {}, None
        for line in self.lines:
            head = Q_HEAD.match(line.text)
            if head:
                q = int(head.group(1))
                continue
            if re.match(r'^\(?\s*[a-hj-l]\s*\)\s', line.text):
                by_q.setdefault(q, []).append(round(line.x))
        self.letter_x_by_q = {k: max(set(v), key=v.count) for k, v in by_q.items()}
        every = [x for v in by_q.values() for x in v]
        return max(set(every), key=every.count) if every else 56.7

    def _is_letter(self, x, prev_letter, q=None):
        """Is this "(i)" the ninth letter or the first roman?

        Both conditions, never one. Indent alone reads an Ordinary true/false
        table's "(i)" — five points in from the margin — as a letter; sequence
        alone reads 2023 Higher's "(h)(i)" as the letter after (h).
        """
        return x <= self._column_for(q) + LETTER_TOL and prev_letter == 'h'

    def _column_for(self, q):
        return self.letter_x_by_q.get(q, self.letter_x)

    # ------------------------------------------------------------- walking --
    def _walk(self):
        asks, section, q = [], None, None
        letter = roman = None
        current = None                       # the ask being accumulated
        last_y = None
        text_pages, leads = {}, {}

        def close():
            nonlocal current
            if current is not None:
                current.text = _norm(current.text)
                asks.append(current)
                current = None

        # The Część tab is printed in the MARGIN of the page its section opens
        # on, and pymupdf reports it after the questions beside it. Read in
        # stream order it arrives too late to file a single ask, which is how
        # the Ordinary Section B asks first censused as zero. It is a property
        # of the PAGE, so it is resolved per page before the walk.
        by_page = self._section_by_page(self.lines, SECTION_TAB)

        for line in self.lines:
            if FURNITURE.match(line.text) and len(line.text) < 60:
                continue
            section = by_page.get(line.page, section)
            if SECTION_TAB.match(line.text):
                continue
            head = Q_HEAD.match(line.text)
            if head:
                close()
                q = int(head.group(1))
                letter = roman = None
                last_y = None
                leads[q] = line.text
                continue
            if q is None:
                continue
            new_page = last_y is None or line.page != getattr(current, 'page', line.page)
            lm = LETTER.match(line.text)
            rm = ROMAN.match(line.text)
            marker = None
            if rm and not (rm.group(1).lower() == 'i'
                           and self._is_letter(line.x, letter, q)):
                marker = ('roman', rm.group(1).lower(), rm.group(2))
            elif lm and (not rm or self._is_letter(line.x, letter, q)):
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
                    # "(e) (i) Name two places in Kraków…" — the SEC glues a
                    # letter and its first roman onto one printed line, and
                    # reading only the letter lost the roman entirely: 2023
                    # Ordinary Q3(e) censused romans ['ii'] with no (i).
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
            # Everything printed before the first ask of a question is its
            # reading text, and the card carries those pages beside the ask.
            if letter is None and not SOURCE_LINE.match(line.text):
                text_pages.setdefault(q, [])
                if line.page not in text_pages[q]:
                    text_pages[q].append(line.page)
        close()
        self.text_pages, self.leads = text_pages, leads
        self._check_sections(asks)
        return asks

    @staticmethod
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

    def _check_sections(self, asks):
        """The tab and the question numbers must tell the same story."""
        by_q = {}
        for a in asks:
            by_q.setdefault(a.q, set()).add(a.section)
        for q, secs in sorted(by_q.items()):
            if len(secs) > 1:
                self.flags.append(
                    {'type': 'section-split',
                     'where': f'Q{q}',
                     'detail': f'the same question is tabbed {sorted(secs)}'})
        reading = sorted(q for q, s in by_q.items() if s == {'A'})
        writing = sorted(q for q, s in by_q.items() if s == {'B'})
        if reading and writing and max(reading) >= min(writing):
            self.flags.append(
                {'type': 'section-order', 'where': '',
                 'detail': f'Section A holds {reading} and Section B {writing}'})
        if None in {a.section for a in asks}:
            self.flags.append({'type': 'section-missing', 'where': '',
                               'detail': 'an ask was printed before any Część tab'})

    # 2021 is a different examination: Część I sets six numbered questions on
    # one text and Część II two essay titles. There are no lettered parts
    # anywhere except question 1, which lists five expressions a) to e).
    def _walk_2021(self):
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
            pm = PART_2021.match(line.text)
            if pm:
                close()
                part, q, letter = pm.group(1).upper(), None, None
                continue
            if part is None:
                continue
            nm = NUMBERED.match(line.text)
            lm = LETTER.match(line.text)
            # Część II sets its two essay titles as bare QUOTATIONS with "ALBO"
            # between them — the paper numbers neither, though the scheme
            # answers them "1." and "2.". So the option is opened by the
            # opening quotation mark, in the printed order the scheme numbers.
            if part == 'II' and ESSAY_TITLE.match(line.text):
                close()
                q = (q or 0) + 1
                current = Ask(part, q, None, None, line.text, line.page)
                last_y = line.y
                continue
            if part == 'II':
                if current is not None and last_y is not None \
                        and 0 <= line.y - last_y <= LINE_GAP:
                    current.text += ' ' + line.text
                    last_y = line.y
                continue
            # In Część I the passage is printed BEFORE the questions and its
            # paragraphs are numbered the same way. The questions come after
            # the source line, which is the boundary the SEC itself prints.
            if nm and self._past_source:
                close()
                q, letter = int(nm.group(1)), None
                current = Ask(part, q, None, None, nm.group(2), line.page)
                last_y = line.y
                continue
            if lm and q is not None and part == 'I':
                close()
                letter = lm.group(1).lower()
                current = Ask(part, q, letter, None, lm.group(2), line.page)
                last_y = line.y
                continue
            if SOURCE_LINE.match(line.text):
                close()
                self._past_source = True
                continue
            if current is not None and last_y is not None \
                    and 0 <= line.y - last_y <= LINE_GAP \
                    and line.page == current.page:
                current.text += ' ' + line.text
                last_y = line.y
                continue
            close()
            if q is None:
                text_pages.setdefault(1, [])
                if line.page not in text_pages[1]:
                    text_pages[1].append(line.page)
        close()
        self.text_pages = text_pages
        self.leads = {}
        return asks

    _past_source = False

    # 2010 to 2020 is the 100-mark examination: the reading text and the line
    # crediting its source come FIRST, then "ZADANIA" and three parts. Część I
    # (30/100) sets six numbered questions on the text, some lettered a) to e);
    # Część II (30/100) is one comment on a quotation; Część III (40/100) is an
    # essay on one of two numbered titles with "ALBO" between them.
    #
    # Walked by `_walk_2021` these sittings censused as nothing, for three
    # reasons the page shows: that walk ignores every line before the first
    # part head, so the source line that opens its questions was never seen;
    # its head pattern is case-sensitive, so the capitals of 2011 and 2012
    # matched no part at all; and it stops at "II", so Część III was read as
    # more of Część II. Here nothing waits on the source line, because no
    # passage is printed inside a part: every numbered line of Część I that is
    # the next number in the run IS a question.
    #
    # Keyed like the rest of this family: 'I' with its question numbers,
    # Część II's single prompt as Question 1 (as eu_paper keys a part that
    # prints one prompt, and as Polish 2021 numbers its Section II), and
    # Część III's two titles by the numbers the paper prints.
    def _walk_classic(self):
        asks, part, q, letter = [], None, None, None
        current, last_y = None, None
        text_pages = {}
        prompt, prompt_page = [], None

        def close():
            nonlocal current
            if current is not None:
                current.text = TRAILING_MARK.sub('', _norm(current.text))
                inline = (INLINE_PARTS.match(current.text)
                          if current.section == 'I' and current.letter is None
                          else None)
                if inline:
                    # The question is the parent; its two parts are the leaves.
                    stem, a_text, b_text = (s.strip() for s in inline.groups())
                    current.text = stem
                    asks.append(current)
                    for mark, words in (('a', a_text), ('b', b_text)):
                        asks.append(Ask(current.section, current.q, mark, None,
                                        words, current.page))
                else:
                    asks.append(current)
                current = None

        def close_part():
            nonlocal prompt, prompt_page
            close()
            if part == 'II' and prompt:
                asks.append(Ask('II', 1, None, None,
                                TRAILING_MARK.sub('', _norm(' '.join(prompt))),
                                prompt_page))
            prompt, prompt_page = [], None

        for line in self.lines:
            if FURNITURE.match(line.text) and len(line.text) < 60:
                continue
            pm = PART_CLASSIC.match(line.text)
            if pm:
                close_part()
                part, q, letter = pm.group(1).upper(), None, None
                continue
            if part is None:
                # The reading text, which every question of Część I is about.
                # Page 1 is the cover in every one of these sittings.
                if line.page > 1 and not SOURCE_LINE.match(line.text) \
                        and line.text != 'ZADANIA':
                    text_pages.setdefault(1, [])
                    if line.page not in text_pages[1]:
                        text_pages[1].append(line.page)
                continue
            if PART_SHARE.match(line.text):
                continue
            if CHOICE_WORD.match(line.text):
                close()
                continue
            nm = NUMBERED.match(line.text)
            if part == 'II':
                # One ask: the quotation and the instruction under it. 2010
                # numbers it "1." and the other years do not.
                prompt.append(nm.group(2) if nm and not prompt
                              and nm.group(1) == '1' else line.text)
                prompt_page = prompt_page or line.page
                continue
            if nm and int(nm.group(1)) == (q or 0) + 1:
                close()
                q, letter = int(nm.group(1)), None
                first = LETTER_CLASSIC.match(nm.group(2)) if part == 'I' else None
                if first and first.group(1).lower() == 'a':
                    # "5. a) Jak daleko…" — the question's own line opens its
                    # first part, and (b) follows on a line of its own. Read
                    # whole, (a) swallowed (b) and 2019 Questions 5 and 6
                    # censused as one ask each where the scheme prices two.
                    asks.append(Ask(part, q, None, None, '', line.page))
                    letter = 'a'
                    current = Ask(part, q, 'a', None, first.group(2), line.page)
                else:
                    current = Ask(part, q, None, None, nm.group(2), line.page)
                last_y = line.y
                continue
            lm = LETTER_CLASSIC.match(line.text)
            if lm and part == 'I' and q is not None \
                    and lm.group(1).lower() == next_letter(letter):
                close()
                letter = lm.group(1).lower()
                current = Ask(part, q, letter, None, lm.group(2), line.page)
                last_y = line.y
                continue
            if current is not None and last_y is not None \
                    and 0 <= line.y - last_y <= LINE_GAP \
                    and line.page == current.page:
                current.text += ' ' + line.text
                last_y = line.y
                continue
            close()
        close_part()
        self.text_pages = text_pages
        self.leads = {}
        return asks

    # ----------------------------------------------------------- listening --
    def _walk_aural(self):
        """The Listening Comprehension booklet's own asks.

        Counted, never carded: the ask can only be answered from the recording.
        The count is what the denominator needs and what the exclusions ledger
        has to match one for one.
        """
        asks, section, item, roman = [], None, None, None
        letter = None
        current, last_y = None, None

        def close():
            nonlocal current
            if current is not None:
                current.text = _norm(current.text)
                asks.append(current)
                current = None

        lines = read_lines(self.aural_path)
        by_page = self._section_by_page(lines, AURAL_TAB)
        for line in lines:
            if FURNITURE.match(line.text) and len(line.text) < 60:
                continue
            page_section = by_page.get(line.page)
            if page_section != section:
                close()
                section, item, roman = page_section, None, None
            if AURAL_TAB.match(line.text):
                continue
            if section is None:
                continue
            nm = NUMBERED.match(line.text)
            if nm:
                close()
                item, roman, letter = int(nm.group(1)), None, None
                rest = nm.group(2)
                # "4. (i) Zaznacz…" opens the item AND its first roman.
                inner = ROMAN.match(rest)
                if inner:
                    roman, rest = inner.group(1).lower(), inner.group(2)
                current = Ask(f'L{section}', item, None, roman, rest, line.page)
                last_y = line.y
                continue
            rm = ROMAN.match(line.text)
            if rm and item is not None and not rm.group(2).strip():
                # A bare "(i)" is an ANSWER BOX, not an ask: "(b) Wymień 2
                # zalety Joanny Bator:" sets two boxes, (i) and (ii), for the
                # two answers it asks for, and the scheme prices the letter
                # "Any two of: (2 x 2 m)". Keyed as asks, the boxes stood in
                # for the questions above them: 2026 Higher Część A Q3 read as
                # Q3(i) and Q3(ii), and lost its (a) and (b).
                continue
            lm = AURAL_LETTER.match(line.text)
            if lm and item is not None:
                # A lettered sub-question with words of its own: "(a) Type of
                # movie.", "(b) Wymień 2 zalety Joanny Bator:". Read before
                # this walker knew letters, its words joined the item above
                # and its answer boxes were counted in its place.
                close()
                letter, roman = lm.group(1).lower(), None
                current = Ask(f'L{section}', item, letter, None, lm.group(2),
                              line.page)
                last_y = line.y
                continue
            if rm and item is not None:
                close()
                roman = rm.group(1).lower()
                current = Ask(f'L{section}', item, letter, roman, rm.group(2),
                              line.page)
                last_y = line.y
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
        return [a for a in self.all_asks() if (a.section or '').startswith('A')
                or a.section == 'I']

    def writing_asks(self):
        return [a for a in self.all_asks() if a.section in ('B', 'II', 'III')]

    def aural_asks(self):
        return [a for a in self.all_asks() if (a.section or '').startswith('L')]

    def lead(self, q):
        return self.leads.get(q, '')

    def pages_for(self, q):
        """The pages of the reading text this question is set on.

        The 2021 examination sets ONE text and asks six questions about it, so
        every question of Część I shares the same pages — they are collected
        under the first and handed to all of them. Keyed strictly by question
        number, two of its six cards shipped with no text at all beside an ask
        that quotes one.
        """
        pages = self.text_pages.get(q)
        if not pages and self.year <= 2021 and self.text_pages:
            pages = next(iter(self.text_pages.values()))
        return pages or []

    def cover_marks(self):
        """What the two booklets say on their own covers, added."""
        total = 0
        for path in [self.path] + ([self.aural_path] if self.aural_path else []):
            with pymupdf.open(path) as doc:
                m = re.search(r'(\d{2,3})\s*marks\b', _norm(doc[0].get_text()), re.I)
            if m:
                total += int(m.group(1))
        return total


# --------------------------------------------------------------- matching ---
WORD = re.compile(r"[^\W\d_]+", re.UNICODE)
# Words too common in Polish or English to be evidence of anything.
STOP = {
    'the', 'a', 'an', 'of', 'to', 'in', 'and', 'or', 'for', 'is', 'are', 'on',
    'at', 'by', 'with', 'from', 'that', 'this', 'it', 'as', 'be', 'what',
    'which', 'how', 'why', 'does', 'do', 'did', 'was', 'were', 'has', 'have',
    'give', 'details', 'detail', 'about', 'his', 'her', 'him', 'she', 'they',
    'sie', 'nie', 'jest', 'jak', 'czy', 'the', 'nad', 'pod', 'przy', 'oraz',
    'que', 'nia', 'ktore', 'ktory', 'ktora', 'nich', 'tym', 'nim', 'dla',
    'nas', 'ich', 'nam', 'nas', 'nasz', 'nasza', 'podaj', 'wymien',
}


def fold(text):
    """Lower-cased and accent-stripped, so że and ze are one word.

    Polish diacritics survive the text layer intact — ą ć ę ł ń ó ś ź ż all
    reach it — so this is a matching convenience, not a repair. ł has no
    combining decomposition, so it is mapped by hand.
    """
    text = (text or '').lower().replace('ł', 'l')
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
    args = ap.parse_args()

    if args.audit:
        for year, level in sittings():
            P = PlPaper(year, level)
            reading = P.reading_asks()
            print(f'{year} {level.upper():2}  {len(P.all_asks()):4} leaves '
                  f'({len(reading)} reading, {len(P.writing_asks())} writing, '
                  f'{len(P.aural_asks())} listening)  cover {P.cover_marks()} marks'
                  f'  letter column x={P.letter_x:.1f}')
            for f in P.flags:
                print(f'      FLAG {f["type"]} {f["where"]} — {f["detail"]}')
        return 0

    P = PlPaper(args.year, args.level)
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
