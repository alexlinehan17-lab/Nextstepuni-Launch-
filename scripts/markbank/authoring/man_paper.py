#!/usr/bin/env python3
"""Mandarin Chinese question papers — the printed ask, and which is a leaf.

    python3 scripts/markbank/authoring/man_paper.py 2024 hl
    python3 scripts/markbank/authoring/man_paper.py 2025 ol --aural
    python3 scripts/markbank/authoring/man_paper.py --audit

The examination
---------------
Mandarin Chinese is SEC subject 566, first examined in 2022, and it is a
CURRICULAR modern language sat in two booklets on one afternoon:

    component 000   the written paper   Section A Reading, Section B Writing
    component A00   the Listening Comprehension Test, Sections A to E

Unlike French, German, Spanish, Italian, Russian and Japanese it is NOT printed
bilingually — the SEC publishes separate English ('E') and Irish ('I') editions
— so there are no columns to cut apart and the language letter 'B' never fires.

    Higher    Section A Reading 80   Q1-Q4, parts (a)…(g), romans under the
                                     true/false tables
              Section B Writing 80   Q5 (a) or (b) or (c), Q6 likewise
    Ordinary  Section A Reading 100  Q1-Q4
              Section B Writing 60   Q5 and Q6, each a choice of three

2022 is the SEC's own Covid reduction and the only sitting with a choice inside
Section A: Higher heads it "Answer either Question 1 OR Question 2" at 55 marks
and Ordinary at 74, and Higher's Question 4 sets a further "Answer either part
(f) OR part (g)". Both are read from the paper's own printed rubric.

THE TRAP THIS READER EXISTS FOR
-------------------------------
**The answer boxes are text.** The SEC prints a labelled box for a candidate to
write in — "Dublin Standard Time:", "Animal 1:", a bare "1." and "2." — and
those labels are ordinary text in their own blocks, which land in the page's
block order well after the ask they belong to. Read as rows they glue
themselves onto the NEXT question's text, and a bare "1." inside one is
indistinguishable from a numbered ask by anything in the line itself.

The page furniture settles it before any wording does. The SEC draws every
answer box as a BLACK-filled frame with white panels inside it and draws
nothing else that way; the section tab in the top margin is the same frame in
grey. So a row whose baseline sits inside a black frame is furniture, not an
ask — which is the same move Italian makes with its ruled answer lines.

**A part letter is never on the ask's own line.** The SEC sets "(a)" at x=57
and its text at x=85 as two blocks on one baseline, so a reader that takes
lines rather than baseline ROWS gets a marker with no ask and an ask with no
marker. Rows are cut by baseline in man_text.page_rows and the marker is the
row's first gap group.
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

import man_text                                              # noqa: E402

SUBJECT = 'mandarin-chinese'
LETTERS = 'abcdefghijkl'
# The x the SEC opens a question marker at on both booklets; its options and
# its answer-box labels are all set well to the right of it.
QUESTION_X = 72.0
ROMANS = ['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii']


def papers_dir(subject=SUBJECT):
    return os.path.join(ROOT, 'examiner-reports', subject, 'papers')


def paper_path(year, level, component='000', subject=SUBJECT):
    path = os.path.join(papers_dir(subject),
                        f'{year}-{level}-{component}-paper.pdf')
    return path if os.path.exists(path) else None


def sittings(subject=SUBJECT):
    out = set()
    for name in sorted(os.listdir(papers_dir(subject))):
        m = re.match(r'^(\d{4})-(hl|ol)-(\w+)-paper\.pdf$', name)
        if m:
            out.add((int(m.group(1)), m.group(2)))
    return sorted(out)


# --------------------------------------------------------------- markers ---
# "Question 1", "Question 1 (continued)". The SEC never numbers anything else
# this way on these papers.
Q_HEAD = re.compile(r'^Question\s*(\d{1,2})\b')
# The section tab, printed inside the grey frame in the top margin:
# "Section A    Reading    80 marks".
SECTION_TAB = re.compile(r'^Section\s+([AB])\b')
# The listening booklet's parts, which it heads "Section A" down the page
# rather than in a margin tab.
TARIFF = re.compile(r'(\d{1,3})\s*marks?\b', re.I)
# The listening booklet sets FIVE parts in nine of the ten sittings and SIX in
# 2022 Ordinary, which runs Section A to Section F. Capped at E, that
# sitting's Section F was read as more of Section E and its four asks
# collided with E's own, which is what the census's question-gap flag said.
AURAL_TAB = re.compile(r'^Section\s+([A-F])\b(?!.*\bmarks?\b.*Reading)')
LETTER = re.compile(r'^\(\s*([a-l])\s*\)\s*(.*)$')
ROMAN = re.compile(r'^\(\s*(i{1,3}|iv|vi{0,3}|ix|x)\s*\)\s*(.*)$')
# A bare number opening a row. On these papers that is ALWAYS an answer-box
# label ("1.", "2." beneath a "name any two" ask) and never a question — the
# questions are all headed "Question N" and their parts are all lettered — but
# it is only ever reached inside a box, where it is dropped anyway.
FURNITURE = re.compile(
    r'^Leaving\s+Certificate|^Mandarin\s+Chinese\s*[–—-]|^Coimisi[úu]n'
    r'|^State\s+Examinations|^\d{4}\s*\.?\s*M\d|^\d{4}L\d{3}[A-Za-z0-9]*$'
    r'|^Do\s+not\s+write\s+on\s+this\s+page|^Optional\s+additional\s+page'
    r'|^Copyright\s+notice|^This\s+examination\s+paper|^There\s+is\s+space\s+for'
    r'|^Page\s*\d+$|^\d{1,3}$|^For\s+Examiner\s+Only|^Examination\s+Number'
    r'|^Centre\s+Stamp|^Date\s+of\s+Birth|^Grade$|^Total$|^Paper\s*[12]$',
    re.I)
# The rubric the SEC prints between a question head and its first part, and
# between parts. It belongs to the question, not to any one ask.
RUBRIC = re.compile(
    r'^Answer\s+(?:the\s+questions|parts?|either|both|ALL|TWO|all)\b'
    r'|^Read\s+the\s+following\b|^Read\s+the\b|^Vocabulary\s*:'
    r'|^Where\s+answers\s+are\s+required\b|^You\s+may\s+only\s+use\b'
    r'|^Write\s+your\s+(?:examination|answers)\b|^Label\s+any\b'
    r'|^This\s+examination\s+booklet\b|^Anything\s+that\s+you\s+write\b'
    r'|^Instructions$|^There\s+are\s+two\s+sections\b', re.I)
# The paper's own choice rubric, which is what makes an ask a VARIANT rather
# than a duplicate. Read from the paper; never inferred from a repeated number.
CHOICE_Q = re.compile(r'Answer\s+either\s+Question\s+(\d)\s+OR\s+Question\s+(\d)',
                      re.I)
CHOICE_PART = re.compile(r'Answer\s+either\s+part\s*\(?([a-l])\)?\s*OR\s+part\s*'
                         r'\(?([a-l])\)?', re.I)


class Ask:
    __slots__ = ('section', 'q', 'letter', 'roman', 'text', 'stem', 'page',
                 'kind', 'rows', 'variant')

    def __init__(self, section, q, letter, roman, text, stem, page, kind):
        self.section, self.q = section, q
        self.letter, self.roman = letter, roman
        self.text, self.stem, self.page, self.kind = text, stem, page, kind
        self.rows = []
        # True where the paper prints "Answer either … OR …" over this ask.
        self.variant = False

    @property
    def key(self):
        return (self.section, self.q, self.letter, self.roman)

    @property
    def full_text(self):
        return f'{self.stem} {self.text}'.strip()

    def __repr__(self):
        return f'<Ask {self.key} {self.kind} {self.text[:44]!r}>'


class ManPaper:
    """One sitting: the written booklet, and the listening booklet beside it."""

    def __init__(self, year, level, subject=SUBJECT):
        self.year, self.level, self.subject = year, level, subject
        self.path = paper_path(year, level, '000', subject)
        self.aural_path = paper_path(year, level, 'A00', subject)
        if not self.path:
            raise FileNotFoundError(f'no {subject} written paper {year} {level}')
        self.section_marks = {}
        self.passages = {}          # (section, q) -> the printed stimulus
        self.passage_pages = {}     # (section, q) -> [page numbers]
        self.flags = []
        self.choices = []           # the paper's own printed choice rubrics
        self._asks = None

    # ------------------------------------------------------------ pages ---
    def _rows(self, path, component):
        """[(page, [gap groups], in_box)] for a whole booklet, printed order."""
        out = []
        with pymupdf.open(path) as doc:
            for pno in range(doc.page_count):
                page = doc[pno]
                got = man_text.page_rows(
                    page, (self.year, self.level), pno + 1, component)
                boxes = _frames(page, [(r['y'], ' '.join(
                    t for _x0, _x1, t in r['groups'])) for r in got])
                for row in got:
                    text = ' '.join(t for _x0, _x1, t in row['groups'])
                    text = re.sub(r'\s+', ' ', text).strip()
                    if not text:
                        continue
                    x0 = row['groups'][0][0]
                    out.append({'page': pno + 1, 'text': text,
                                'groups': row['groups'], 'y': row['y'],
                                'box': man_text.in_box(row['y'], boxes, x0)})
        return out

    # ------------------------------------------------------------- walk ---
    def asks(self):
        if self._asks is None:
            self._asks = self._walk()
        return self._asks

    def all_asks(self):
        return self.asks()

    def reading_asks(self):
        return [a for a in self.asks() if a.kind == 'reading']

    def _walk(self):
        rows = self._rows(self.path, '000')
        asks = self._walk_written(rows)
        if self.aural_path:
            asks += self._walk_aural()
        return asks

    def _walk_written(self, rows):
        """The written booklet, walked once, forward.

        Three decisions this makes that a looser walker got wrong on the first
        pass, each against a NAMED case:

        * **The section changes at the next QUESTION, not at the tab.** The
          Section B tab is printed in the top margin of the page Question 5
          opens on, and 2024 Higher prints Question 4's last two parts on the
          page before it — but a part is only closed when the next marker
          arrives, which is after the tab. Read at flush time, Q4(f) was
          censused as "Section B Q4(f)": a citation to a page of the paper
          that does not print it.
        * **"(i)" is the ninth letter here too.** A marker is a LETTER when it
          is the next letter of the run and a ROMAN otherwise, which is
          pl_paper's first condition; read as a letter, Question 1(c)'s three
          true/false statements became parts (i), (ii) and (iii) of a
          question that has no such parts and the real (c) vanished.
        * **A row continues an ask only from the ask's own text column.** The
          SEC sets Question 2(e)'s radical table with its cells at x=67, 200,
          325 and 441 where the ask's text stands at x=85. Taken as
          continuations they put "home 灬 眼 wood / tree" — four cells of the
          answer grid — inside the printed question.
        """
        section, pending, kind, auto_q = None, None, None, None
        q, letter, letter_x, text_x = None, None, None, None
        buf, open_at, out, stems = [], None, [], {}

        def flush():
            if open_at is None:
                return
            sec, qq, ll, rr, kk = open_at
            text = _clean(' '.join(buf))
            if rr is None:
                stems[(sec, qq, ll)] = text
            out.append((sec, qq, ll, rr, text, kk))

        def close_question():
            # A question the SEC sets NO lettered part under is one leaf, not
            # none. 2025 and 2026 Ordinary open Section A with a
            # picture-matching grid — "Match the following words and pictures
            # by filling in the grid below" — priced 8 marks as eight rows of
            # one, with no (a) anywhere on the page. Requiring a letter threw
            # the whole question away and censused the sitting at 17 reading
            # asks where the scheme answers 18.
            if q is None or letter is not None:
                return
            stem = ' '.join(t for t in self.passages.get((section, q), [])
                            if len(t) >= 12)
            if stem:
                out.append((section, q, None, None, _clean(stem), kind))

        for row in rows:
            text = row['text']
            if row['box']:
                m = SECTION_TAB.match(text)
                if m:
                    # The tab closes the section it ends as well as opening
                    # the next. 2024 Ordinary prints NO "Question 5" head at
                    # all — Section B opens straight into "Write down the
                    # missing character in each sentence below" — so a walker
                    # that waits for a question head kept the previous
                    # question open across the boundary and keyed Section B's
                    # (a)(i) as Section A Question 4(d)(i), twice over. What
                    # the paper does state is that its questions run on
                    # across the two sections: "Answer TWO questions —
                    # Question 5 … AND Question 6".
                    flush()
                    close_question()
                    buf, letter, letter_x, open_at = [], None, None, None
                    section, pending = m.group(1), None
                    auto_q, q = (q or 0) + 1, None
                    tar = TARIFF.search(text)
                    if tar:
                        self.section_marks[section] = int(tar.group(1))
                continue                      # every other boxed row is a box
            if FURNITURE.match(text) or FURNITURE.match(_spaced(text)):
                continue
            m = CHOICE_Q.search(text)
            if m:
                self.choices.append(('question', pending or section,
                                     int(m.group(1)), int(m.group(2))))
            m = CHOICE_PART.search(text)
            if m:
                self.choices.append(('part', section, q, m.group(1),
                                     m.group(2)))
            m = Q_HEAD.match(text)
            if m:
                flush()
                close_question()
                buf, letter, letter_x, open_at = [], None, None, None
                if pending:
                    section, pending = pending, None
                q, auto_q = int(m.group(1)), None
                kind = 'reading' if section == 'A' else 'writing'
                self.passages.setdefault((section, q), [])
                self.passage_pages.setdefault((section, q), [])
                rest = text[m.end():].strip()
                if rest and not RUBRIC.match(rest):
                    self.passages[(section, q)].append(rest)
                continue
            x0 = row['groups'][0][0]
            lm, rm = LETTER.match(text), ROMAN.match(text)
            if q is None and auto_q and lm and lm.group(1) == 'a':
                q, kind = auto_q, ('reading' if section == 'A' else 'writing')
                self.passages.setdefault((section, q), [])
                self.passage_pages.setdefault((section, q), [])
                self.flags.append({
                    'type': 'headless-question',
                    'where': f'{self.year} {self.level} Section {section} '
                             f'page {row["page"]}',
                    'detail': f'the paper prints no "Question {q}" head over '
                              f'this section; the number is the run the '
                              f'paper states on its own instruction page'})
            if q is None:
                continue
            if lm and lm.group(1) == _next_letter(letter):
                flush()
                letter, letter_x = lm.group(1), x0
                text_x = (row['groups'][1][0] if len(row['groups']) > 1
                          else x0 + 28)
                buf = [lm.group(2)]
                open_at = (section, q, letter, None, kind)
                continue
            if rm and letter is not None:
                flush()
                buf = [rm.group(2)]
                open_at = (section, q, letter, rm.group(1), kind)
                text_x = (row['groups'][1][0] if len(row['groups']) > 1
                          else x0 + 28)
                continue
            if lm or rm:
                self.flags.append({
                    'type': 'marker-out-of-run',
                    'where': f'{self.year} {self.level} Section {section} '
                             f'Q{q} page {row["page"]}',
                    'detail': f'{text[:60]!r} follows ({letter})'})
                continue
            if letter is None:
                if not RUBRIC.match(text):
                    self.passages[(section, q)].append(text)
                    if row['page'] not in self.passage_pages[(section, q)]:
                        self.passage_pages[(section, q)].append(row['page'])
                continue
            if _continues(row, text_x):
                buf.append(text)
        flush()
        close_question()
        return self._materialise(out, stems, rows)

    def _materialise(self, out, stems, rows):
        """The walk's rows -> Asks, with a letter that has romans dropped.

        A letter whose table the SEC numbers (i) to (iv) is a PARENT: the
        student answers the romans. Its own text is the table's instruction and
        rides on each roman as the stem, which is how the true/false rubric —
        and the tick glyph in it — reaches every card.
        """
        have_romans = {(s, q, l) for s, q, l, r, _t, _k in out
                       if r is not None}
        pages = self._pages_index(rows)
        asks = []
        for section, q, letter, roman, text, kind in out:
            if roman is None and (section, q, letter) in have_romans:
                continue                     # a parent, not a leaf
            stem = stems.get((section, q, letter), '') if roman else ''
            page = pages.get((section, q, letter, roman), 1)
            asks.append(Ask(section, q, letter, roman, _clean(text),
                            _clean(stem), page, kind))
        self._mark_variants(asks)
        for key, lines in list(self.passages.items()):
            self.passages[key] = '\n'.join(lines) if isinstance(lines, list) \
                else lines
        return asks

    def _pages_index(self, rows):
        """Which page each leaf's marker was printed on."""
        idx, q, letter, section, pending = {}, None, None, None, None
        for row in rows:
            text = row['text']
            if row['box']:
                m = SECTION_TAB.match(text)
                if m:
                    pending = m.group(1)
                continue
            m = Q_HEAD.match(text)
            if m:
                if pending:
                    section, pending = pending, None
                q, letter = int(m.group(1)), None
                continue
            lm, rm = LETTER.match(text), ROMAN.match(text)
            if lm and lm.group(1) == _next_letter(letter):
                letter = lm.group(1)
                idx[(section, q, letter, None)] = row['page']
                continue
            if rm and letter is not None:
                idx[(section, q, letter, rm.group(1))] = row['page']
        return idx

    def _mark_variants(self, asks):
        """The paper's own "Answer either … OR …" rubric, applied.

        A repeated marker after a printed OR is a choice VARIANT, not a
        duplicate — Law 3's third clause. 2022 is the only sitting that sets
        one inside Section A and it sets two: whole questions at Higher and
        Ordinary, and parts (f)/(g) of Higher's Question 4.
        """
        for kind, section, *rest in self.choices:
            if kind == 'question':
                _a, b = rest
                for ask in asks:
                    if ask.section == section and ask.q == b:
                        ask.variant = True
            else:
                # A PART-level choice — "Answer either part (f) OR part (g)" —
                # needs no -alt suffix: the two letters are distinct addresses
                # and nothing is repeated. The suffix exists to disambiguate a
                # repeated question NUMBER, which is the other kind.
                continue

    # ---------------------------------------------------------- listening --
    def _walk_aural(self):
        """The Listening Comprehension booklet, walked only to be COUNTED.

        Not one of these asks is carded — the recording IS the ask, which is
        the refusal every carded language in this bank makes — but the census
        denominator is the paper, so the booklet is read rather than assumed.
        """
        rows = self._rows(self.aural_path, 'A00')
        section, q, letter, buf, open_at = None, None, None, [], None
        out, stems = [], {}

        def flush():
            if open_at is None:
                return
            sec, qq, ll, rr = open_at
            text = _clean(' '.join(buf))
            if rr is None:
                stems[(sec, qq, ll)] = text
            out.append((sec, qq, ll, rr, text))

        for row in rows:
            text = row['text']
            m = AURAL_TAB.match(text)
            if m:
                # The listening booklet heads its parts inside the same black
                # frame the written paper tabs its sections in, so this test
                # comes BEFORE the box test rather than after it.
                flush()
                section, q, letter, buf, open_at = 'L' + m.group(1), None, \
                    None, [], None
                tar = TARIFF.search(text)
                if tar:
                    self.section_marks[section] = int(tar.group(1))
                continue
            if row['box'] or FURNITURE.match(text) \
                    or FURNITURE.match(_spaced(text)) or section is None:
                continue
            x0 = row['groups'][0][0]
            m = re.match(r'^(\d{1,2})\s*[.)]\s*(.*)$', text)
            if m and x0 > QUESTION_X:
                # A number that is not a marker. The listening booklet sets its
                # multiple-choice options forty points in from the question
                # they answer, and two of 2022 Ordinary's are "6.5 hours" and
                # "2.5 hours" — which a marker test on the LINE reads as
                # Question 6 and Question 2 with the answer "5 hours". Section
                # F censused questions 1, 2, 3, 4 and 6, which is what the
                # census's question-gap flag said. The question margin decides,
                # the way it decides every other marker on these papers.
                m = None
            if m:
                flush()
                q, letter, buf = int(m.group(1)), None, []
                open_at = (section, q, None, None)
                text = m.group(2).strip()
                if not text:
                    continue
            if q is None:
                continue
            lm, rm = LETTER.match(text), ROMAN.match(text)
            if lm and lm.group(1) == _next_letter(letter):
                flush()
                letter, buf = lm.group(1), [lm.group(2)]
                open_at = (section, q, letter, None)
                continue
            if rm:
                flush()
                buf = [rm.group(2)]
                open_at = (section, q, letter, rm.group(1))
                continue
            buf.append(text)
        flush()
        # A question whose parts are lettered is a parent, and so is a letter
        # whose true/false table is numbered in romans.
        parents = {(s, q) for s, q, l, _r, _t in out if l is not None}
        have_romans = {(s, q, l) for s, q, l, r, _t in out if r is not None}
        asks = []
        for section, q, letter, roman, text in out:
            if letter is None and (section, q) in parents:
                continue
            if roman is None and (section, q, letter) in have_romans:
                continue
            asks.append(Ask(section, q, letter, roman, text,
                            stems.get((section, q, letter), '')
                            if roman else '', 1, 'listening'))
        return asks


def _frames(page, rows):
    """The SEC's ANSWER BOXES, and only those.

    Every box on these pages is drawn the same way — a black-filled frame with
    white panels inside it — and so is the section tab in the top margin and,
    on some pages, the panel the READING PASSAGE itself is printed in. 2024
    Higher page 5 prints Question 2's whole Chinese text inside one, so a rule
    that drops every framed row drops the stimulus four cards depend on: the
    frame alone does not say which is which.

    What does is what is printed inside it. An answer box holds the labels a
    candidate writes beside — "Animal in the first paragraph:", "Weather:", a
    bare "(i)" over an empty rule — and never a Chinese character; a stimulus
    panel is Chinese prose. So a framed panel holding an ideograph is content
    and is read, and one holding none is furniture and is dropped.
    """
    boxes = []
    for drawing in page.get_drawings():
        if drawing.get('type') not in ('f', 'fs'):
            continue
        fill = drawing.get('fill')
        if not fill:
            continue
        r = drawing['rect']
        # A photograph's near-white background is a fill too; the SEC's frames
        # are black, and its section tab grey.
        if max(fill) < 0.9 and r.width > 200 and r.height > 8:
            boxes.append((r.x0, r.y0, r.x1, r.y1))
    out = []
    for box in boxes:
        inside = [t for y, t in rows if box[1] - 1 <= y <= box[3] + 1]
        if any(man_text._cjk(c) for t in inside for c in t):
            continue                       # a stimulus panel, not an answer box
        out.append(box)
    return out


def _next_letter(current):
    if current is None:
        return 'a'
    i = LETTERS.index(current)
    return LETTERS[i + 1] if i + 1 < len(LETTERS) else None


BULLET = ('-', '‐', '‑', '–', '—', '•', '●', '▶', '✎')


def _continues(row, text_x):
    """Does this row carry on the ask above it, or open something else?

    The ask's own text column answers it. A wrapped sentence resumes at the
    same x the ask's text started at; a table cell, a column header and an
    answer grid do not, and 2024 Higher's radical table put four of its cells
    inside the printed question until this was measured rather than assumed.
    """
    if text_x is None:
        return True
    groups = row['groups']
    x0 = groups[0][0]
    if len(groups) == 1:
        # A wrapped sentence resumes at the ask's own x, near enough exactly.
        # A MULTIPLE-CHOICE OPTION does not: the SEC indents its three options
        # forty to sixty points past the question they answer, each beside its
        # own tick box. Taken as continuations they became part of the printed
        # question — "Why does the author go to Shanghai? study tourism
        # business" — and the scheme's answer, "Study", was then read as more
        # of the question and the ask reported as having no answer at all.
        return abs(x0 - text_x) <= 14
    # "-  Where will the party be held?" — the SEC's own dash bullet under a
    # writing task, set as two groups on one row.
    return groups[0][2] in BULLET and x0 >= text_x - 4


def _spaced(text):
    """The row with its spaces put back where the type set none.

    Some SEC runs on these papers come back with no word space at all —
    "Optionaladditionalpages. Indicateclearlythenumberandpart…" — because the
    glyphs are set closer than a fifth of the type size. Nothing on a card is
    built from such a run; this exists only so the page furniture is still
    recognised as furniture and does not glue itself to the last ask.
    """
    return re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', text.replace(' ', ''))


def _clean(text):
    return re.sub(r'\s+', ' ', (text or '')).strip()


# ------------------------------------------------------------- wording -----
WORD = re.compile(r"[a-z']+")
STOP = {'the', 'a', 'an', 'of', 'to', 'in', 'and', 'or', 'for', 'is', 'are',
        'on', 'at', 'by', 'with', 'from', 'that', 'this', 'it', 'as', 'be',
        'following', 'above', 'below', 'your', 'you', 'answer', 'answers',
        'question', 'questions', 'chinese', 'english'}


def bag(text):
    return {w for w in WORD.findall((text or '').lower())
            if w not in STOP and len(w) > 2}


def score(a, b):
    if not a or not b:
        return 0.0
    return len(a & b) / min(len(a), len(b))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('year', nargs='?', type=int)
    ap.add_argument('level', nargs='?', default='hl')
    ap.add_argument('--audit', action='store_true')
    args = ap.parse_args()
    targets = sittings() if args.audit else [(args.year, args.level)]
    for year, level in targets:
        P = ManPaper(year, level)
        asks = P.asks()
        by = collections.Counter(a.kind for a in asks)
        print(f'{year} {level}: {len(asks)} asks {dict(by)} '
              f'sections {P.section_marks} choices {P.choices}')
        if not args.audit:
            for a in asks:
                print(f'  {str(a.key):26} {a.kind:10} '
                      f'{"VAR " if a.variant else "    "}{a.full_text[:80]}')
            for key, text in P.passages.items():
                print(f'  passage {key}: {len(text)} chars on '
                      f'{P.passage_pages.get(key)}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
