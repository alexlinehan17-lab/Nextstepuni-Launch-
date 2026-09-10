#!/usr/bin/env python3
"""Ancient Greek question papers — the printed ask, its tariff, its passage.

    python3 scripts/markbank/authoring/agr_paper.py 2023 hl
    python3 scripts/markbank/authoring/agr_paper.py 2015 hl --json

Ancient Greek is Latin's sibling and this reader is `lat_paper` re-cut, not a
fork of the modern-language readers: one booklet, no Listening Comprehension
Test, no bilingual column, no answer-language rule, and a printed CHOICE of
routes at the third level of the address. What it does NOT share with Latin is
its alphabet — see `agr_text`, which is what makes a page before 2023 readable
at all.

The skeleton, in the paper's own words
--------------------------------------
Higher, every sitting 2010-2024::

    1.  Answer Section A or Section B.                                  [50]
        A.  Translate into Greek.
        B.  Read the following passage and answer, in English … (a)-(h)
    2.  Translate into English one passage from Section A and one from B  [180]
        A. (i) / (ii)        B. (i) / (ii)
    3.  Answer either Section A or Section B.                           [80]
        A. (i) Translate into English.  (50)
           (ii) Answer any three … (a)-(g), ten marks each   (30)
        B. likewise
    4.  Answer any three … thirty marks each                            [90]
        2010-2019: routed A. (i)-(iv) and B. (i)-(iv)
        2021-2024: unrouted (i)-(viii)
        the last part sets (a), (b), (c) on photographs at the back

Ordinary::

    1.  Translate into English any two of the passages A, B, C, D.     [210]
    2.  (i) Translate into English.  (ii) Answer any four … (a)-(h)    [100]
    3.  Answer any three … thirty marks each                            [90]
        2010-2019: routed A. (i)-(iv) and B. (i)-(iv)
        2021-2023: unrouted (i)-(viii)

Three things this reader has to get right
-----------------------------------------
**The route is a CHOICE, not a scope.** "Section A" under Question 1 and
"Section A" under Question 3 are different routes through the same paper, and
the questions run 1-4 across all of them — so the census keys the route in the
section slot and checks the question run ONCE over the paper
(`'numbering': 'continuous'`), exactly as Latin does.

**Question 4 changed shape in 2021** and the reader must not impose either
shape. Before it, eight essay topics are printed as two routes of four; after
it, as one run of eight. Routes are detected, never assumed: a question with no
"A."/"B." head is walked as a flat run of romans.

**The passage IS the ask** for translation, and the ask is unanswerable without
it for comprehension. Both are captured as the route's `stimulus` with the
pages they were printed on, decoded out of SPIonic where the sitting predates
2023.
"""
import argparse
import json
import os
import re
import sys

import pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))

import agr_text                                               # noqa: E402
from markbank_text import unligature                          # noqa: E402

SUBJECT = 'ancient-greek'
ROMANS = ['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x']
LETTERS = 'abcdefgh'
ROUTES = 'ABCD'

FURNITURE = re.compile(
    r'^Leaving\s+Certi[fi]+cate(?:\s+Examination)?\b'
    r'|^Ancient\s+Greek\s*[–—\-‐]\s*(?:Higher|Ordinary)\s+Level'
    r'|^Ancient\s+Greek\s*$'
    r'|^Coimisi[úu]n\s+na\s+Scr[úu]duithe'
    r'|^\d{4}\s*\.?\s*M\s*\.?\s*\d\b|^\d{4}L\d{3}[A-Z0-9]+\s*$'
    r'|^Acknowledgements\b|^Copyright notice\b|^Images?\s*$'
    r'|^There is no examination material on this page'
    r'|^Page\s+\d+\s+of\s+\d+\s*$'
    r'|^https?://|^\s*\d{1,3}\s*$', re.I)

# Where the booklet stops setting questions. The plates at the back are headed
# with a bare letter on its own line, and the copyright notice reads "Section
# 53(5) of the Copyright and Related Rights Act" — a bare "(5)" exactly where
# this reader looks for a tariff, which is why the cut has to happen first.
BACK_MATTER = re.compile(
    r'^https?://|^Acknowledgements\b|^Images?\b'
    r'|^This examination paper may contain|^Copyright notice\b'
    r'|^There is no examination material|^Blank Page', re.I)
# A plate at the back is headed with a bare letter on a line of its own — and
# so is every route in the paper ("A.", "OR B."). What separates them is that
# NOTHING is asked after a plate heading: it comes after the last (roman) or
# (letter) the booklet prints. Treating any bare letter as back matter cut the
# 2010 Ordinary paper off at Question 3's own Section A head and lost all eight
# of its essay topics, with no flag to show for it.
PLATE = re.compile(r'^([A-E])\.?$')

# See lat_paper: the SEC does not always set a marker on its text's own
# baseline, and ordinary line spacing in these papers is twelve points or more.
ROW_BAND = 8
ROW = '\x00'


def papers_dir(subject=SUBJECT):
    return os.path.join(ROOT, 'examiner-reports', subject, 'papers')


def paper_path(year, level, subject=SUBJECT):
    path = os.path.join(papers_dir(subject), f'{year}-{level}-paper.pdf')
    if not os.path.exists(path):
        raise FileNotFoundError(f'no {subject} paper for {year} {level}')
    return path


def sittings(subject=SUBJECT):
    out = []
    for name in sorted(os.listdir(papers_dir(subject))):
        m = re.match(r'^(\d{4})-(hl|ol)-paper\.pdf$', name)
        if m:
            out.append((int(m.group(1)), m.group(2)))
    return out


def _clean(text):
    text = unligature(' '.join(str(text).replace(ROW, ' ').split()))
    return text.replace('‐', '-').replace('‑', '-').strip()


class Ask:
    """One printed ask: what the paper asks, where, and for how much."""
    __slots__ = ('section', 'q', 'letter', 'roman', 'text', 'stem', 'marks',
                 'page', 'inherited', 'kind')

    def __init__(self, section, q, letter, roman, text, stem, marks, page,
                 inherited=False, kind=None):
        self.section, self.q = section, q
        self.letter, self.roman = letter, roman
        self.text, self.stem, self.marks, self.page = text, stem, marks, page
        self.inherited = inherited
        # What the paper's own rubric says this ask is for, one of
        # 'translate-into-greek', 'translate-into-english', 'comprehension',
        # 'literature'. The exclusions the schemes force fall exactly on the
        # two translation kinds, so this is read off the paper rather than
        # inferred from a question number that changed shape in 2021.
        self.kind = kind

    @property
    def key(self):
        return (self.section, self.q, self.letter, self.roman)

    def __repr__(self):
        return f'<Ask {self.key} {self.marks}m {self.text[:48]!r}>'


QHEAD = re.compile(r'(?:^|\x00)\s*(\d)\.[\s\x00]+(?=[A-Z(\[])')
# A route head: "A." / "OR B." opening a printed line — or the letter ALONE on
# its line with no full stop at all, which is how 2015, 2017 and 2019 Higher
# set Question 3's second route. Requiring the stop lost Section B's whole
# translation ask in each of those three sittings, and left its five literature
# parts hanging under Section A.
ROUTE = re.compile(
    r'(?:^|\x00)\s*(?:OR\s+)?([A-D])(?:\.(?=\s|\x00|$)|(?=\s*(?:\x00|$)))')
# The SEC sets a space INSIDE the bracket often enough that a tight pattern
# loses whole asks and leaves no gap to see it by: 2010 Higher prints "(c )"
# and 2018 Higher prints "(f  )" — with non-breaking spaces — in the middle of
# Question 1 Section B. Read tight, the forward-only cut stopped at (b) and (e)
# respectively and six comprehension asks a year went missing silently.
ROMAN = re.compile(r'(?:^|\x00)\s*\(\s*(' + '|'.join(ROMANS) + r')\s*\)')
LETTER = re.compile(r'(?:^|\x00)\s*\(\s*(' + '|'.join(LETTERS) + r')\s*\)')
TARIFF = re.compile(r'\(\s*(\d{1,3})\s*\)')
TOTAL = re.compile(r'\[\s*(\d{1,3})\s*\]')

WORD_MARKS = {'ten': 10, 'thirty': 30, 'twenty': 20, 'fifteen': 15,
              'twenty-five': 25, 'five': 5, 'forty': 40, 'fifty': 50}
WORD_TARIFF = re.compile(
    r'\b(?:each|carries|carry)\b[^.]{0,40}?\b('
    + '|'.join(re.escape(w) for w in WORD_MARKS) + r'|\d{1,3}'
    + r')\b\s*marks?', re.I)


def _word_tariff(text):
    """The per-part price a question states in its own rubric.

    "They carry ten marks each", "Each question carries thirty marks". The SEC
    writes these in words for the whole corpus, and they are the ONLY price the
    parts beneath them carry: Question 4 prints "[90]" on the question and
    nothing at all on its eight topics.
    """
    m = WORD_TARIFF.search(text)
    if not m:
        return None
    token = m.group(1).lower()
    return WORD_MARKS[token] if token in WORD_MARKS else int(token)


def _split_forward(text, pattern, order, from_start=False):
    """Cut `text` at every marker that continues `order`, and only those.

    Forward-only, for the reason lat_paper gives: a marker that goes BACKWARDS
    is not a marker. Here the false ones are inside the Greek — a vocabulary
    gloss line reads "(i)" nowhere, but an English bracketed summary sets
    "(Zeus, Poseidon, and Pluto divide their father's kingdom)" and a rubric
    enumerates the parts it is about.
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
            cuts.append((m.start(), m.end(), tok))
            want = idx + 1
        elif idx == want - 1:
            cuts.append((m.start(), m.end(), tok))
    head = text[:cuts[0][0]] if cuts else text
    out = []
    for i, (_start, end, tok) in enumerate(cuts):
        stop = cuts[i + 1][0] if i + 1 < len(cuts) else len(text)
        out.append((tok, text[end:stop].strip(), end))
    return head.strip(), out


class AgrPaper:
    def __init__(self, year, level, subject=SUBJECT):
        self.year, self.level, self.subject = year, level, subject
        self.path = paper_path(year, level, subject)
        self._doc = pymupdf.open(self.path)
        self._runs = None
        self._asks = None
        self._offsets = None
        self._joined = None
        self.last_question_end = 0
        self.question_marks = {}
        self.stimulus = {}
        self.flags = []

    # ------------------------------------------------------------- text ----
    def _stream(self):
        """[(page, text)] — one entry per PRINTED LINE, furniture dropped.

        Every span is put through `agr_text.decode` if it is set in SPIonic, so
        a 2015 line comes out as "ἦν δέ τις ἐν τῇ στρατιᾷ Ξενοφῶν" and not as
        "h]n de/ tij e0n th=| stratia=| Cenofw~n". Lines whose vertical centres
        agree are gathered into one row and ordered left to right, because the
        SEC sets a marker in its own left-hand column.
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
                    text = ''.join(
                        agr_text.decode(s['text'])
                        if agr_text.FONT in s['font'] else s['text']
                        for s in line['spans'])
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
                if not text or FURNITURE.match(text):
                    continue
                runs.append((pno + 1, text))
        self._runs = runs
        return runs

    def _rows(self):
        if self._offsets is None:
            offsets, pos = [], 0
            for page, text in self._stream():
                offsets.append((pos, page))
                pos += len(text) + len(ROW)
            self._offsets = offsets
            self._joined = ROW.join(t for _, t in self._stream())
        return self._offsets

    def _page_at(self, offset):
        page = self._rows()[0][1]
        for off, pg in self._rows():
            if off > offset:
                break
            page = pg
        return page

    def _pages_between(self, lo, hi):
        return sorted({pg for off, pg in self._rows() if lo <= off < hi}) \
            or [self._page_at(lo)]

    def photo_pages(self):
        """{plate letter: page} for the photographs at the back.

        Each plate is printed under a bare letter on a line of its own, which
        is what separates it from the "A." that heads a route — a letter
        followed by that route's rubric. Read only after the last part marker
        the booklet prints, because Question 3 at Ordinary heads its two routes
        "A." and "B." on lines of their own AFTER the last question opens, and
        those were bound as photographs on a paper that prints none.
        """
        self.asks()
        out = {}
        for off, page in self._rows():
            if off < max(self.last_question_end, self._last_marker()):
                continue
            text = self._joined[off:off + 4]
            m = PLATE.match(text.split(ROW)[0])
            if m:
                out.setdefault(m.group(1), page)
        return out

    def _last_marker(self):
        self._rows()
        marks = [m.end() for m in ROMAN.finditer(self._joined)] \
            + [m.end() for m in LETTER.finditer(self._joined)]
        return max(marks) if marks else 0

    def cover_marks(self):
        """The total the paper states on its own cover — the checksum.

        Read from the first TWO pages: 2011 Ordinary prints nothing but the
        examination's name on page one and states "(400 marks)" on page two,
        and a cover-page-only read reported no total for that sitting.
        """
        text = ''.join(self._doc[n].get_text()
                       for n in range(min(2, len(self._doc))))
        m = re.search(r'\((\d{3})\s*marks\)', text, re.I)
        return int(m.group(1)) if m else None

    # ------------------------------------------------------------ asks -----
    def asks(self):
        if self._asks is None:
            self._asks = self._walk()
        return self._asks

    def _questions(self):
        self._rows()
        joined = self._joined
        cuts, want = [], 1
        for m in QHEAD.finditer(joined):
            if int(m.group(1)) != want:
                continue
            cuts.append((m.start(), m.end(), want))
            want += 1
        end = len(joined)
        last_marker = self._last_marker()
        for off, _page in self._rows():
            if not cuts or off < cuts[-1][1]:
                continue
            nxt = joined.find(ROW, off)
            row = joined[off:nxt if nxt != -1 else len(joined)]
            if BACK_MATTER.match(row) or (off > last_marker
                                          and PLATE.match(row)):
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
            _head, routes = _split_forward(text, ROUTE, ROUTES,
                                           from_start=True)
            if routes:
                for i, (route, body, off) in enumerate(routes):
                    rstop = (base + routes[i + 1][2] if i + 1 < len(routes)
                             else stop)
                    asks += self._unit(q, route, body, base + off, rstop, text)
            else:
                asks += self._unit(q, None, text, base, stop, text)
        return asks

    def _unit(self, q, route, body, base, stop, qtext):
        """One route (or a whole unrouted question) -> its asks."""
        per = _word_tariff(qtext) or _word_tariff(body)
        rubric, romans = _split_forward(body, ROMAN, ROMANS)
        if not romans:
            return self._leaf_or_letters(q, route, None, body, base, stop, '',
                                         per, qtext)
        out = []
        for i, (roman, rbody, roff) in enumerate(romans):
            rstop = (base + romans[i + 1][2] if i + 1 < len(romans) else stop)
            out += self._leaf_or_letters(q, route, roman, rbody,
                                         base + roff, rstop, rubric, per,
                                         qtext)
        return out

    def _leaf_or_letters(self, q, route, roman, body, base, stop, rubric, per,
                         qtext):
        kind = self._kind(q, body, rubric, qtext)
        # A letter run OPENS at (a) — every one this paper prints does. Without
        # that, 2012 Higher Question 4 Section B(iii) — "Distinguish between
        # (a) a Geometric Greek vase, (b) a Black Figure Greek vase and (c) a
        # Red Figure Greek vase" — had its (c) read as a part, because (c)
        # happened to open a printed line while (a) and (b) sat mid-line. One
        # ask became a part named after an item in its own list, and the ask
        # itself was lost.
        stem_text, letters = _split_forward(body, LETTER, LETTERS,
                                            from_start=True)
        page = self._page_at(base)
        if not letters:
            marks, ask = self._split_marks(body)
            if kind in ('translate-into-english', 'translate-into-greek'):
                # A translation ask IS its passage.
                self.stimulus[(route, q, None, roman)] = {
                    'text': ask, 'pages': self._pages_between(base, stop)}
            return [Ask(route, q, None, roman, ask, _clean(rubric),
                        marks if marks is not None else per, page,
                        inherited=marks is None, kind=kind)]
        stem_marks, stem_text = self._split_marks(stem_text)
        sub_per = _word_tariff(body) or per
        out = []
        for letter, lbody, loff in letters:
            marks, ask = self._split_marks(lbody)
            out.append(Ask(route, q, letter, roman, ask, _clean(stem_text),
                           marks if marks is not None else sub_per,
                           self._page_at(base + loff),
                           inherited=marks is None, kind=kind))
        if kind == 'comprehension':
            # The comprehension's stimulus is everything printed between the
            # route's own head and its first question: the English summary in
            # brackets, the Greek passage, and the vocabulary the SEC glosses
            # it with. Without it none of (a)-(h) can be answered.
            self.stimulus[(route, q, None, roman)] = {
                'text': _clean(stem_text),
                'pages': self._pages_between(base, base + letters[0][2])}
        return out

    # ---------------------------------------------------------------------
    @staticmethod
    def _kind(q, body, rubric='', qtext=''):
        """What the paper says this ask is for, in its own printed rubric.

        Read per ASK, not per route: Question 3 Section A sets "(i) Translate
        into English." and "(ii) Answer any three of the following questions"
        under ONE route head, and reading the route's opening words alone
        called both of them translation — which would have excluded every
        literature ask in the paper.
        """
        low = (body[:220] + ' ' + rubric[:220]).lower()
        if 'translate into greek' in low:
            return 'translate-into-greek'
        if 'translate into english' in low or 'translate this passage' in low:
            return 'translate-into-english'
        if 'read the following passage' in low:
            return 'comprehension'
        qlow = qtext[:200].lower()
        if q == 1 and 'translate into english any' in qlow:
            return 'translate-into-english'       # Ordinary Question 1's A-D
        if q == 2 and re.search(r'translate into english .{0,30}passage', qlow):
            # Higher Question 2's four routes, whose rubric reads "Translate
            # into English one passage from Section A and one from Section B".
            # Matching "translate into english" alone made every literature
            # part of ORDINARY Question 2(ii) a translation ask, because that
            # question's own (i) is a translation and the two share a head.
            return 'translate-into-english'
        if q == 1 and 'read the following passage' in qlow:
            return 'comprehension'
        return 'literature'

    @staticmethod
    def _split_marks(text):
        """The printed tariff, and the ask with the tariff taken off.

        The tariff is the LAST bare parenthesised number in the ask, hard right
        on its own last line. A vocabulary gloss is never a bare number, and
        an author credit line "XENOPHON (90)" IS the passage's tariff.
        """
        text = _clean(text)
        found = list(TARIFF.finditer(text))
        if not found:
            return None, text
        m = found[-1]
        return int(m.group(1)), _clean(text[:m.start()] + ' ' + text[m.end():])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('year', type=int)
    ap.add_argument('level')
    ap.add_argument('--json', action='store_true')
    args = ap.parse_args()
    P = AgrPaper(args.year, args.level)
    asks = P.asks()
    if args.json:
        json.dump([{'key': list(a.key), 'marks': a.marks, 'kind': a.kind,
                    'text': a.text, 'stem': a.stem, 'page': a.page}
                   for a in asks], sys.stdout, ensure_ascii=False, indent=1)
        return 0
    print(f'{args.year} {args.level}: {len(asks)} asks, cover '
          f'{P.cover_marks()} marks, plates {P.photo_pages()}')
    for a in asks:
        print(f'  {str(a.key):26} {str(a.marks or "-"):>4} {a.kind:22} '
              f'{a.text[:64]}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
