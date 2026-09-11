#!/usr/bin/env python3
"""Latin question papers — the printed ask, its printed tariff, its passage.

    python3 scripts/markbank/authoring/lat_paper.py 2025 hl
    python3 scripts/markbank/authoring/lat_paper.py 2023 ol --json

Why Latin needs its own reader
------------------------------
**It is a language, but not a MODERN one, and none of the six language readers
fit.** There is no Listening Comprehension Test, no second booklet, no
bilingual column layout and no answer-language rule: one booklet, five
questions, sat in English about Latin.

**Its address is four levels deep and its third level is a CHOICE.** Every
sitting prints the same skeleton:

    1.  Answer either Section A or Section B.                          [75]
        A.  Translate into Latin.            (Ordinary: five sentences (a)-(e))
        B.  Read the following passage and answer … (i) … (xii)
    2.  Translate into English … passages A, B, C, D  /  one from each Section
    3.  Answer either Section A or Section B.                          [90]
        A.  (i) Translate into English. (60)
            (ii) Answer any three of the five questions below. (30)
                 (a) … (e)
    4.  (i) [(a) or (b)]   (ii)   (iii)                                [20/30]
    5.  (i) … (vi) [(vi) may print (a), (b), (c)]                      [50/75]

So an ask is addressed by a question, a printed choice route, and up to two
levels beneath it — "3 A (ii) (a)" — and the route is a SECTION the paper names
itself ("Answer either Section A or Section B"). The census therefore keys
(section, q, letter, roman) with the route in the section slot, and the label
prints the roman before the letter because that is the order the paper prints
them in; see `ROMAN_MAJOR` in paper_census.py.

**Every marker is glued into its neighbour's block.** pymupdf reads the whole
of Question 1 Section A — rubric, English source, the standalone "OR", and the
Section B head — as ONE block, and reads a Section B route as another block
carrying its intro, its Latin passage, its vocabulary list and all twelve
questions. So markers are cut out of a joined stream, never read off block
boundaries, and every cut is FORWARD-ONLY: a question head must be the next
number, a route the same or the next letter, a roman or letter the next in its
own run. That is what stops "revocari C. Laelium placuit" — printed inside a
Question 4 grammar line — from opening a Section C that the paper never sets.

**The passage is the question.** A Section B comprehension ask cannot be
answered without the Latin it is about, and a "Translate into English" ask IS
its passage. Both are captured as the route's `stimulus`, with the pages it was
printed on, so a card can carry them.

**The photographs are pages of this same booklet.** Question 5(vi) sets two or
three questions on photographs printed on their own pages at the back, each
headed with its bare letter. `photo_pages()` reads that heading, so a card
naming "Photographs A and B" binds the page the SEC printed them on rather than
a crop nobody checked.
"""
import argparse
import json
import os
import re
import sys

import pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, os.path.dirname(HERE))

from markbank_text import unligature                          # noqa: E402

SUBJECT = 'latin'
ROMANS = ['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x',
          'xi', 'xii']
LETTERS = 'abcdef'
ROUTES = 'ABCD'

# Printed on the page, never part of an ask.
FURNITURE = re.compile(
    r'^Leaving\s+Certi[fi]+cate(?:\s+Examination)?\b'
    r'|^Latin\s*[–—-]\s*(?:Higher|Ordinary)\s+Level'
    r'|^Coimisi[úu]n\s+na\s+Scr[úu]duithe'
    r'|^\d{4}\s*\.?\s*M\s*\.?\s*\d\b'
    r'|^Acknowledgements\b|^Copyright notice\b'
    r'|^There is no examination material on this page'
    r'|^The image part with relationship'
    r'|^Page\s+\d+\s*[-:]|^Images?\s*$'
    r'|^\s*\d{1,3}\s*$', re.I)

# The 2022 Higher cover carries a broken image placeholder whose every letter
# is doubled — "TThhee imimagagee ppaarrtt" — which no furniture pattern
# written for the sane spelling can see. It is on the cover, before Question 1.
DOUBLED = re.compile(r'(?:([A-Za-z])\1){4,}')

# Where the booklet stops setting questions and starts talking about itself:
# the plates at the back, each headed with its bare letter, then the image
# credits and the copyright notice. Cutting here is not tidiness — the notice
# reads "in accordance with Section 53(5) of the Copyright and Related Rights
# Act, 2000", and "(5)" is a bare parenthesised number at the end of the last
# ask, which is exactly where this reader looks for a tariff. 2025 Higher
# Q5(vi)(c) was priced at five marks by that sentence.
BACK_MATTER = re.compile(
    # Lettered plate headings only. A bare "5." is Question 5's own head in
    # 2022 Ordinary, where the SEC sets the number on its own line, and a
    # numeric plate heading in this pattern cut that paper off at Question 5 —
    # six asks lost with a question-gap flag to show for it.
    r'^[A-E]\.$|^https?://|^Acknowledgements\b|^Images?\b'
    r'|^Page\s+\d+\b'
    r'|^This examination paper may contain|^Copyright notice\b'
    r'|^There is no examination material', re.I)


def papers_dir(subject=SUBJECT):
    return os.path.join(ROOT, 'examiner-reports', subject, 'papers')


def paper_path(year, level, subject=SUBJECT):
    path = os.path.join(papers_dir(subject), f'{year}-{level}-paper.pdf')
    if not os.path.exists(path):
        raise FileNotFoundError(f'no {subject} paper for {year} {level}')
    return path


# How far apart two drawn lines may be and still be ONE printed line. The SEC
# sets a marker in its own left-hand column and does not always set it on the
# text's own baseline: on page 3 of the 2021 Higher paper the intro to Section
# B of Question 2 is drawn at y=345 and the "B." that heads it at y=351, six
# points BELOW. Read as separate rows the route head landed after its own
# intro, and Section B's ask lost the sentence that says what the passage is
# about. Ordinary line spacing in these papers is twelve points or more, so
# eight separates a wrapped line from a hanging marker without merging two
# real ones. Lines inside a row are ordered left to right, which puts the
# marker in front of the text it marks.
ROW_BAND = 8
# The rows of a question are joined with this, so a marker can be required to
# open a PRINTED LINE. Every false marker the corpus prints sits mid-line: the
# rubric "Answer parts (i), (ii), and (iii)." enumerates the three parts it is
# about, "(i) Answer either (a) or (b)." names the choice beneath it, and a
# Livy passage prints "P. Cornelius cum omnibus matronis". A marker that opens
# a line is the SEC setting a part; one that does not is the SEC talking about
# one.
ROW = '\x00'


def _clean(text):
    # ROW is not whitespace to str.split, so it has to go explicitly or a
    # marking point ships with a NUL in the middle of it.
    text = unligature(' '.join(str(text).replace(ROW, ' ').split()))
    # The SEC hyphenates its rubric with a non-breaking hyphen and sets its
    # colons with one too: "in this question:‐". Folded so a rubric matches
    # whichever spelling a year used.
    return text.replace('‐', '-').replace('‑', '-').strip()


class Ask:
    """One printed ask: what the paper asks, where, and for how much."""
    __slots__ = ('section', 'q', 'letter', 'roman', 'text', 'stem', 'marks',
                 'page', 'inherited', 'route_kind')

    def __init__(self, section, q, letter, roman, text, stem, marks, page,
                 inherited=False, route_kind=None):
        self.section, self.q = section, q
        self.letter, self.roman = letter, roman
        self.text, self.stem, self.marks, self.page = text, stem, marks, page
        # True where the tariff was printed on the level ABOVE this ask rather
        # than on the ask. Question 4(i) prints "(10)" once over the "(a) or
        # (b)" a candidate chooses between, so each is worth ten; Question
        # 5(vi) prints twenty-five once over three parts a candidate answers
        # TWO of, so twenty-five is a ceiling and not a price. An inherited
        # tariff is never checked against the scheme's own.
        self.inherited = inherited
        # What kind of ask this is, read from the paper's own rubric: one of
        # 'translate-into-latin', 'translate-into-english', 'comprehension',
        # 'literature', 'grammar', 'essay'. It is the paper talking, not a
        # guess — the exclusions the schemes force fall exactly on the two
        # translation kinds.
        self.route_kind = route_kind

    @property
    def key(self):
        return (self.section, self.q, self.letter, self.roman)

    def __repr__(self):
        return f'<Ask {self.key} {self.marks}m {self.text[:48]!r}>'


# A question head: "1." opening a printed line.
# A question head: "1." opening a printed line. The rubric may be on the SAME
# printed line or on the NEXT one — 2022 Ordinary sets "5." alone on its line
# and "Answer any two parts of the six parts…" beneath it — so a row boundary
# counts as the space after the full stop. Without that, Question 5 was never
# opened and its six parts continued Question 4's roman run as (iv), (v), (vi).
QHEAD = re.compile(r'(?:^|\x00)\s*(\d)\.[\s\x00]+(?=[A-Z(\[])')
# A route head: "A." / "OR B." opening a printed line, or standing alone on it.
ROUTE = re.compile(r'(?:^|\x00)\s*(?:OR\s+)?([A-D])\.(?=\s|\x00|$)')
ROMAN = re.compile(r'(?:^|\x00)\s*\((' + '|'.join(ROMANS) + r')\)')
LETTER = re.compile(r'(?:^|\x00)\s*\((' + '|'.join(LETTERS) + r')\)')
# A bare parenthesised number is a tariff; a bracketed one is a question total.
TARIFF = re.compile(r'\((\d{1,3})\)')
TOTAL = re.compile(r'\[(\d{1,3})\]')
# "Each question carries ten marks", "(They carry ten marks each)",
# "(Each part carries twenty-five marks)". The paper states these in words and
# never in digits, and they are the only price the parts beneath them carry.
WORD_MARKS = {'ten': 10, 'twenty-five': 25, 'twenty‐five': 25, 'fifteen': 15,
              'twenty': 20, 'five': 5}
WORD_TARIFF = re.compile(
    r'\b(?:each|carries|carry)\b[^.]{0,40}?\b('
    + '|'.join(re.escape(w) for w in WORD_MARKS) + r'|\d{1,3}'
    + r')\b\s*marks?', re.I)


def _word_tariff(text):
    """The per-part price a question states in its rubric.

    Spelled out in most sittings — "Each question carries ten marks" — but in
    DIGITS in 2022 Ordinary: "(Each part carries 25 marks)". A words-only
    pattern left all six of that paper's Question 5 parts unpriced.
    """
    m = WORD_TARIFF.search(text)
    if not m:
        return None
    token = m.group(1).lower()
    return WORD_MARKS[token] if token in WORD_MARKS else int(token)


def _split_forward(text, pattern, order, from_start=False):
    """Cut `text` at every marker that continues `order`, and only those.

    Returns (head, [(marker, body, offset)]) — the text before the first
    accepted marker, then each unit with the offset its body begins at, so a
    caller can say which printed page the unit came from.

    Forward-only, because a marker that goes BACKWARDS is not a marker: a Livy
    passage prints "P. Cornelius cum omnibus matronis" and a Question 4
    grammar line prints "revocari C. Laelium placuit". Neither can open a part
    that the run before it has already passed. Where a run STARTS is the
    paper's business and not this reader's — 2023 Higher sets Question 2 as
    "A. (i) … OR A. (ii)", so the second Section A route opens at (ii) — so
    only the ORDER is enforced, unless `from_start` says the run must begin at
    the first token (a question's routes always open at A).
    """
    cuts, want = [], None
    for m in pattern.finditer(text):
        tok = m.group(1)
        if tok not in order:
            continue
        idx = order.index(tok)
        if want is None:
            if from_start and idx != 0:
                continue
            cuts.append((m.start(), m.end(), tok))
            want = idx + 1
        elif idx == want:
            # the next token opens the next unit
            cuts.append((m.start(), m.end(), tok))
            want = idx + 1
        elif idx == want - 1:
            # the same token again repeats the CURRENT unit
            cuts.append((m.start(), m.end(), tok))
    head = text[:cuts[0][0]] if cuts else text
    out = []
    for i, (_start, end, tok) in enumerate(cuts):
        stop = cuts[i + 1][0] if i + 1 < len(cuts) else len(text)
        out.append((tok, text[end:stop].strip(), end))
    return head.strip(), out


class LatPaper:
    def __init__(self, year, level, subject=SUBJECT):
        self.year, self.level, self.subject = year, level, subject
        self.path = paper_path(year, level, subject)
        self._doc = pymupdf.open(self.path)
        self._runs = None
        self._asks = None
        self._offsets = None
        self._joined = None
        self.last_question_end = 0
        self.question_marks = {}      # {q: the paper's own printed total}
        self.stimulus = {}            # {(section, q): {'text':…, 'pages':[…]}}

    # ------------------------------------------------------------- text ----
    def _stream(self):
        """[(page, text)] — one entry per PRINTED LINE, furniture dropped.

        Lines, not blocks. pymupdf glues the whole of a Section B route into
        one block, marker and passage and all twelve questions together, so a
        marker read off a block start is invisible for exactly the questions
        that have the most of them. Lines whose vertical centres agree are
        gathered back into one row and ordered left to right first, because
        the SEC sets the marker in its own left-hand column: "(i)" is drawn at
        x=57 and "How has Pliny's host tried to present himself?" at x=100, on
        the same printed line. That is the same reconstruction
        extract-scheme.py does for the schemes' tables, and for the same
        reason.
        """
        if self._runs is not None:
            return self._runs
        runs = []
        for pno in range(len(self._doc)):
            page = self._doc[pno]
            lines = []
            for block in page.get_text('dict')['blocks']:
                if block.get('type') != 0:
                    continue
                for line in block['lines']:
                    text = ''.join(s['text'] for s in line['spans'])
                    if not text.strip():
                        continue
                    x0, y0, _, y1 = line['bbox']
                    lines.append(((y0 + y1) / 2, x0, text))
            rows, anchor = [], None
            for y, x, text in sorted(lines):
                if anchor is None or y - anchor > ROW_BAND:
                    rows.append([])
                    anchor = y
                rows[-1].append((x, text))
            for row in rows:
                text = _clean(' '.join(t for _, t in sorted(row)))
                if not text or FURNITURE.match(text) or DOUBLED.search(text):
                    continue
                runs.append((pno + 1, text))
        self._runs = runs
        return runs

    def image_pages(self):
        """The pages of plates at the back, read off the PDF's own images.

        Question 5 does not always letter its plates: 2023 Ordinary numbers
        them "1." to "4." inside the very line that lists the four subjects to
        write on, so there is no heading to read. What there is, is the image
        itself — a page that carries raster artwork and sits at or after the
        page the last question opens on is a plate page, and that is evidence
        rather than a guess.
        """
        self.asks()                       # fills last_question_end
        first = self._page_at(self.last_question_end)
        out = []
        for n in range(len(self._doc)):
            if n + 1 < first or not self._doc[n].get_images():
                continue
            # The last page of every booklet carries the copyright notice and
            # the Commission's own crest, which is an image; bound as a plate
            # it opened the copyright notice beside the question.
            if re.search(r'^\s*Copyright notice|^\s*Acknowledgements',
                         self._doc[n].get_text(), re.M):
                continue
            out.append(n + 1)
        return out

    def photo_pages(self):
        """{photograph letter: page} for the plates at the back of the book.

        The SEC prints each plate on its own page under a bare letter, two to
        a page where they are small. The heading is the WHOLE printed line —
        "A." and nothing else — which is what separates it from the Section A
        head of Question 1, a letter followed by that section's rubric.
        """
        self.asks()                       # fills last_question_end
        out = {}
        for off, page in self._rows():
            if off < self.last_question_end:
                # Question 1 and Question 3 head their two routes "A." and
                # "B." on a line of their own too, and a plate heading read
                # before the last question was set bound Photograph A to the
                # page Section A of Question 1 opens on.
                continue
            text = self._joined[off:off + 4]
            m = re.match(r'([A-E])\.(?:\x00|$)', text)
            if m:
                out.setdefault(m.group(1), page)
        return out

    # ------------------------------------------------------------ asks -----
    def asks(self):
        if self._asks is None:
            self._asks = self._walk()
        return self._asks

    def _rows(self):
        """[(offset, page)] — where each printed row starts in the joined text."""
        if self._offsets is None:
            offsets, pos = [], 0
            for page, text in self._stream():
                offsets.append((pos, page))
                pos += len(text) + len(ROW)
            self._offsets = offsets
            self._joined = ROW.join(t for _, t in self._stream())
        return self._offsets

    def _page_at(self, offset):
        """The page the text at this offset was printed on."""
        page = self._rows()[0][1]
        for off, pg in self._rows():
            if off > offset:
                break
            page = pg
        return page

    def _pages_between(self, lo, hi):
        return sorted({pg for off, pg in self._rows() if lo <= off < hi}) \
            or [self._page_at(lo)]

    def _questions(self):
        """[(q, text, base offset, end offset)] — the five printed questions."""
        self._rows()
        joined = self._joined
        cuts, want = [], 1
        for m in QHEAD.finditer(joined):
            if int(m.group(1)) != want:
                continue
            cuts.append((m.start(), m.end(), want))
            want += 1
        end = len(joined)
        for off, _page in self._rows():
            # Past the END of the last question's head, not its start: the
            # head match opens on the row separator before "5.", so the row
            # holding "5." itself sits after cuts[-1][0] and a back-matter
            # test would examine the head it is anchored to.
            if not cuts or off < cuts[-1][1]:
                continue
            nxt = joined.find(ROW, off)
            row = joined[off:nxt if nxt != -1 else len(joined)]
            if BACK_MATTER.match(row):
                end = off
                break
        out = []
        for i, (lo, hi, q) in enumerate(cuts):
            stop = cuts[i + 1][0] if i + 1 < len(cuts) else end
            out.append((q, joined[hi:stop], hi, stop))
        self.last_question_end = cuts[-1][0] if cuts else 0
        return out

    def _walk(self):
        asks = []
        for q, text, base, stop in self._questions():
            total = TOTAL.search(text)
            if total:
                self.question_marks[q] = int(total.group(1))
            if q in (1, 2, 3):
                asks += self._routed(q, text, base)
            else:
                asks += self._plain(q, text, base)
        return asks

    # ---- Questions 1, 2 and 3: the paper prints a choice of routes ---------
    def _routed(self, q, text, base):
        _head, routes = _split_forward(text, ROUTE, ROUTES, from_start=True)
        out = []
        for i, (route, body, off) in enumerate(routes):
            stop = (base + routes[i + 1][2] if i + 1 < len(routes)
                    else base + len(text))
            out += self._route_asks(q, route, body, base + off, stop)
        return out

    def _route_asks(self, q, route, body, base, stop):
        pages = self._pages_between(base, stop)
        page = pages[0]
        head_marks = self.question_marks.get(q)
        rubric, romans = _split_forward(body, ROMAN, ROMANS)
        if not romans:
            head, letters = _split_forward(body, LETTER, LETTERS)
            if letters and q == 1:
                # Ordinary Question 1 Section A: five sentences to translate,
                # each priced on its own printed line.
                out = []
                for letter, sentence, off in letters:
                    marks, ask = self._split_marks(sentence)
                    out.append(Ask(route, q, letter, None, ask, _clean(head),
                                   marks, self._page_at(base + off),
                                   route_kind=self._kind(q, body)))
                return out
            marks, ask = self._split_marks(body)
            self.stimulus[(route, q, None)] = {'text': ask, 'pages': pages}
            return [Ask(route, q, None, None, ask, '',
                        marks if marks else head_marks, page,
                        inherited=marks is None,
                        route_kind=self._kind(q, body))]

        out = []
        for roman, rbody, roff in romans:
            _, letters = _split_forward(rbody, LETTER, LETTERS)
            kind = self._kind(q, rbody, rubric)
            rpage = self._page_at(base + roff)
            if not letters:
                marks, ask = self._split_marks(rbody)
                if kind == 'translate-into-english':
                    # A translation ask IS its passage: the Latin the card has
                    # to show is the ask's own printed text.
                    self.stimulus[(route, q, roman)] = {
                        'text': ask, 'pages': self._pages_between(
                            base + roff, stop)}
                out.append(Ask(route, q, None, roman, ask, _clean(rubric),
                               marks, rpage, route_kind=kind))
                continue
            stem_text, _ = _split_forward(rbody, LETTER, LETTERS)
            stem_marks, stem_text = self._split_marks(stem_text)
            per = _word_tariff(rbody) or stem_marks
            for letter, lbody, loff in letters:
                marks, ask = self._split_marks(lbody)
                out.append(Ask(route, q, letter, roman, ask, _clean(stem_text),
                               marks or per, self._page_at(base + roff + loff),
                               inherited=marks is None, route_kind=kind))
        # A comprehension route's stimulus is everything the paper printed
        # between the route's own head and its first question: the English
        # summary in brackets, the Latin passage, and the vocabulary the SEC
        # glosses it with. Without it its questions cannot be answered at all.
        if any(a.route_kind == 'comprehension' for a in out):
            self.stimulus[(route, q, None)] = {
                'text': _clean(rubric),
                'pages': self._pages_between(base, base + romans[0][2])}
        return out

    # ---- Questions 4 and 5: no routes ------------------------------------
    def _plain(self, q, text, base):
        rubric, romans = _split_forward(text, ROMAN, ROMANS)
        per = _word_tariff(rubric)
        kind = 'grammar' if q == 4 else 'essay'
        out = []
        for roman, rbody, roff in romans:
            _, letters = _split_forward(rbody, LETTER, LETTERS)
            rpage = self._page_at(base + roff)
            if not letters:
                marks, ask = self._split_marks(rbody)
                out.append(Ask(None, q, None, roman, ask, _clean(rubric),
                               marks or per, rpage, inherited=marks is None,
                               route_kind=kind))
                continue
            stem_text, _ = _split_forward(rbody, LETTER, LETTERS)
            stem_marks, stem_text = self._split_marks(stem_text)
            shared = self._alternatives_tariff(stem_text, letters)
            for letter, lbody, loff in letters:
                marks, ask = self._split_marks(lbody)
                if shared is not None:
                    marks, ask = None, _clean(lbody)
                out.append(Ask(None, q, letter, roman, ask, _clean(stem_text),
                               marks or shared or stem_marks or per,
                               self._page_at(base + roff + loff),
                               inherited=marks is None, route_kind=kind))
        return out

    @staticmethod
    def _alternatives_tariff(stem, letters):
        """The one tariff a printed CHOICE of parts shares, or None.

        Question 4(i) sets "Answer either (a) or (b)" and prints "(10)" once —
        hard right at the end of (b), because that is where the part ends on
        the page. It prices the PART, not (b): a candidate answers one of the
        two and either is worth ten. Read as (b)'s own tariff it left (a)
        unpriced in 2021 and 2022 Higher, which is a card that cannot ship.
        """
        if len(letters) < 2 or not re.search(r'\beither\b', stem, re.I):
            return None
        priced = [LatPaper._split_marks(body)[0] for _, body, _ in letters]
        found = [m for m in priced if m is not None]
        return found[0] if len(found) == 1 else None

    # ---------------------------------------------------------------------
    @staticmethod
    def _kind(q, body, rubric=''):
        """What the paper says this ask is for, in its own printed rubric.

        Per ASK, not per route: Question 3 Section A prints "(i) Translate
        into English" and "(ii) Answer any three of the five questions below"
        under one route head, and reading the route's opening words alone
        called both of them translation.
        """
        low = (body[:200] + ' ' + rubric[:200]).lower()
        if q == 1 and 'translate into latin' in low:
            return 'translate-into-latin'
        if 'translate into english' in low or 'translate the following' in low:
            return 'translate-into-english'
        if 'read the following passage' in low:
            return 'comprehension'
        if q == 2:
            return 'translate-into-english'
        return 'literature'

    @staticmethod
    def _trim_plate_labels(text):
        """Drop the plate captions the SEC prints under a question's options.

        2023 Ordinary Q5(vi) lists "1. Pont du Gard 2. Pantheon 3. Roman
        portrait sculpture 4. Roman mosaics" and then repeats "1. 2. 3. 4." as
        the headings of the four photographs beneath it. Left on, the ask read
        "…4. Roman mosaics 1. 2." on the card.
        """
        return re.sub(r'(?:\s+[1-9]\.)+\s*$', '', text).strip()

    @staticmethod
    def _split_marks(text):
        """The printed tariff, and the ask with the tariff taken off.

        The tariff is the LAST bare parenthesised number in the ask, which is
        where the SEC sets it — hard right on the ask's own last line. A
        vocabulary gloss "(m. pl.)" is not a number and an author credit
        "Virgil (65)" is the passage's own tariff, which is what a translation
        ask is worth.
        """
        text = _clean(text)
        found = list(TARIFF.finditer(text))
        if not found:
            return None, LatPaper._trim_plate_labels(text)
        m = found[-1]
        marks = int(m.group(1))
        return marks, LatPaper._trim_plate_labels(
            _clean(text[:m.start()] + ' ' + text[m.end():]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('year', type=int)
    ap.add_argument('level')
    ap.add_argument('--json', action='store_true')
    args = ap.parse_args()
    P = LatPaper(args.year, args.level)
    asks = P.asks()
    if args.json:
        json.dump([{'key': list(a.key), 'marks': a.marks, 'kind': a.route_kind,
                    'text': a.text, 'stem': a.stem, 'page': a.page}
                   for a in asks], sys.stdout, ensure_ascii=False, indent=1)
        return 0
    print(f'{args.year} {args.level}: {len(asks)} asks, '
          f'{sum(a.marks or 0 for a in asks)} marks printed, '
          f'photographs on {P.photo_pages()}')
    for a in asks:
        print(f'  {str(a.key):28} {str(a.marks or "-"):>4} {a.route_kind:22} '
              f'{a.text[:70]}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
