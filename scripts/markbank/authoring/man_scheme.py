#!/usr/bin/env python3
"""Mandarin Chinese marking schemes — the priced answer, and the ask it names.

    python3 scripts/markbank/authoring/man_scheme.py 2024 hl --full
    python3 scripts/markbank/authoring/man_scheme.py --audit

What this document is
---------------------
One file, three documents, and only one of them answers a question a card can
ask:

    READING: 80 MARKS            <- priced answers, question reprinted verbatim
    WRITING - 80 MARKS           <- a COMMUNICATION and LANGUAGE band grid
    LISTENING COMPREHENSION      <- priced answers, but the ask is the recording

**The tariff is a column, not a suffix.** The SEC prints "(a) What time is it
now?" at x=85 and "(2 x 2 marks)" at x=454 on the SAME printed line, and
pymupdf reports them as two lines. Read naively the ask has no tariff and the
tariff has no ask, which is how "the scheme prints no tariff" gets said about a
document that prices every line. So the page is gathered into ROWS by baseline
first, and a cell standing at or past the marks column is read as a price.

**A roman under a letter is an ASK only when it carries its own price.** The
SEC uses the same "(i) (ii) (iii)" for two different things one page apart:
Question 1(c)'s three true/false statements are three asks and each is priced
"3 marks", while Question 2(d)'s "(i)" and "(ii)" are the two ANSWER LINES of a
single ask priced "(2 x 2 marks)" once. Nothing in the marker separates them.
The printed price does, and the question paper agrees with it: 2(d)'s romans
are printed inside the answer box and 1(c)'s are not.

**A tick is answered by its COLUMN.** Every true/false table in the corpus is
marked by a lone "✓" set on its own, and which of True and False it means is
its x — the SEC prints the two headers at x=437 and x=496 and the tick under
one of them. Read without the column, a "✓" is not an answer at all; read with
it, five sittings' worth of true/false asks card verbatim.
"""
import argparse
import collections
import os
import re
import sys

import pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, HERE)

import man_text                                              # noqa: E402
from man_paper import LETTERS, _next_letter                  # noqa: E402

SUBJECT = 'mandarin-chinese'
# Where the SEC's marks column starts. Measured from the corpus: every printed
# tariff cell in the ten schemes stands at x >= 420 and no answer text opens
# there. Below it a "3 marks" is part of a sentence, not a price.
PRICE_X = 420.0


def schemes_dir(subject=SUBJECT):
    return os.path.join(ROOT, 'examiner-reports', subject, 'schemes')


def scheme_path(year, level, subject=SUBJECT):
    path = os.path.join(schemes_dir(subject), f'{year}-{level}.pdf')
    return path if os.path.exists(path) else None


def has_scheme(year, level, subject=SUBJECT):
    return scheme_path(year, level, subject) is not None


# --------------------------------------------------------------- markers ---
UNIT_READING = re.compile(r'^READING\s*[:\-–—]\s*\d+\s*MARKS', re.I)
UNIT_WRITING = re.compile(r'^WRITING\s*[:\-–—]\s*\d+\s*MARKS', re.I)
UNIT_LISTENING = re.compile(r'^LISTENING\s+COMPREHENSION', re.I)
APPENDIX = re.compile(r'^APPENDIX\b|^CD\s+SCRIPT\b|^Audio\s+Script', re.I)
Q_HEAD = re.compile(r'^Question\s*(\d{1,2})\s*[-–—]\s*(\d{1,3})\s*marks?\b',
                    re.I)
Q_BARE = re.compile(r'^Question\s*(\d{1,2})\b')
SECTION_HEAD = re.compile(r'^Section\s+([A-F])\s*[:\-–—]?\s*(\d{1,3})?\s*marks?',
                          re.I)
LETTER = re.compile(r'^\(\s*([a-l])\s*\)\s*(.*)$')
ROMAN = re.compile(r'^\(\s*(i{1,3}|iv|vi{0,3}|ix|x)\s*\)\s*(.*)$')
NUMBERED = re.compile(r'^(\d{1,2})\s*[.)]\s*(.*)$')
# Every notation the ten schemes print, and nothing wider: "(2 x 2 marks)",
# "(1 x 1 mark)", "(1 mark)", "(3 marks)", "(2 × 2 marks)", "(1mark)",
# "(4 x 5 marks)", "3 marks" with no brackets at all in the true/false tables.
RATE = re.compile(r'\(?\s*(\d{1,2})\s*[x×]\s*(\d{1,2})\s*marks?\s*\)?', re.I)
FLAT = re.compile(r'\(?\s*(\d{1,3})\s*marks?\s*\)?$', re.I)
ANY_PRICE = re.compile(r'\d{1,3}\s*marks?\b', re.I)
# "(1+ 3 marks)" — 2023 Higher prices Question 3's three parts as a colour
# plus a reason, and states the split rather than the total. Read as a flat
# "3 marks" the question came to 23 where its own head prints 26.
SUM = re.compile(r'\(\s*(\d{1,2})\s*\+\s*(\d{1,2})\s*marks?\s*\)', re.I)
TICK = re.compile(r'^[✓✔]$')
TF_HEADER = re.compile(r'^(True|False)$', re.I)
# The SEC answers three different tick tables in this corpus and only one of
# them is headed True/False: 2022 Higher's Question 2(g) heads its columns
# "Room A | Room B | Room C" and 2025 Ordinary's "Left-to-right structure |
# Top-bottom structure | Enclosed structure | Single structure". A tick means
# the column it stands under whatever that column is called, so the header is
# recognised by its SHAPE — two or more short cells set in the marks half of
# the measure, with no sentence among them — rather than by its words. Read
# only as True/False, Question 2(g)'s three column names were shipped as its
# three marking points.
COLUMN_X = 280.0


def _is_header(cells):
    if len(cells) < 2:
        return False
    if all(TF_HEADER.match(t) for _x0, _x1, t in cells):
        return True
    return (all(len(t) <= 26 and not t.endswith(('.', '?', ':'))
                for _x0, _x1, t in cells)
            and min(x0 for x0, _x1, _t in cells) >= COLUMN_X)
# A directive the SEC prints under a menu of answers. It bounds what a student
# may claim and rides on the card; it is never itself a marking point.
DIRECTIVE = re.compile(r'^\(\s*(?:Answer\s+any|Any\s+|Accept\s+|Award\s+'
                       r'|\d+\s*marks?\s+for\b|Answer\s+either)', re.I)
CHOICE_PART = re.compile(r'Answer\s+either\s+part\s*\(?([a-l])\)?\s*OR\s*'
                         r'(?:part\s*)?\(?([a-l])\)?', re.I)
RUBRIC_ONLY = re.compile(
    r'^Answer\s+(?:Parts?|either|the\s+following|both|all)\b'
    r'|^Answer\s+Question\s+\d|^Read\s+the\b', re.I)
FURNITURE = re.compile(
    r'^Leaving\s+Certificate|^Coimisi[úu]n|^State\s+Examinations'
    r'|^Marking\s+Scheme$|^Mandarin\s+Chinese$|^(Higher|Ordinary)\s+Level$'
    r'|^Note\s+to\s+teachers|^Marking\s+schemes\s+published'
    r'|^\d{1,3}$|^Answer\s+Question\s+\d', re.I)


class SchemeAsk:
    __slots__ = ('unit', 'section', 'q', 'letter', 'roman', 'cue', 'marks',
                 'notation', 'answers', 'directives', 'page', 'table',
                 'lines', 'ordinal', 'raw', 'wide')

    def __init__(self, unit, section, q, letter, roman, cue, page):
        self.unit, self.section = unit, section
        self.q, self.letter, self.roman = q, letter, roman
        self.cue, self.page = cue, page
        self.marks, self.notation = None, None
        self.answers, self.directives = [], []
        # True where the answer is set in a printed GRID rather than in lines.
        self.table = False
        self.wide = False
        # Every printed line of the block, in order, with the tariff taken out
        # and a lone tick resolved to the column it stands in. The block is
        # what the SEC printed: its question REPRINTED and its answer under it.
        # man_all pairs the two documents by SUBTRACTION over this — the paper's
        # own wording taken off the front — rather than by guessing which line
        # is which from the layout, because the layout differs between sittings
        # (2022 Ordinary sets the tariff AFTER the answer, every other sitting
        # before it).
        self.lines = []
        # Position of this row inside its true/false table, where it is one.
        self.ordinal = None
        # [(text, marks, verdict)] — every printed row of the block in order,
        # with its own price. Where the cue ends and the answer begins is not
        # decidable from this document alone (2022 Ordinary sets the tariff
        # after the answer and every other sitting before it), so the split is
        # made against the QUESTION PAPER in `split_against`.
        self.raw = []

    @property
    def key(self):
        return (self.section, self.q, self.letter, self.roman)

    def __repr__(self):
        return (f'<SchemeAsk {self.unit} {self.key} {self.marks}m '
                f'{len(self.answers)} answer(s)>')


class ManScheme:
    def __init__(self, year, level, subject=SUBJECT):
        self.year, self.level, self.subject = year, level, subject
        self.path = scheme_path(year, level, subject)
        if not self.path:
            raise FileNotFoundError(f'no {subject} scheme for {year} {level}')
        self.unit_marks = {}
        self.question_marks = {}
        # The scheme's own printed choice rubric: "Answer either part (h) OR
        # (i)". A question whose parts include a choice is not the SUM of its
        # parts — a candidate sits one route — and 2022 Ordinary's Question 4
        # prints 24 where its nine parts price 26, which is 18 plus one of two
        # six-mark alternatives. Read from the document, never inferred.
        self.choices = []
        self.flags = []
        self._asks = None

    def asks(self):
        if self._asks is None:
            self._asks = self._walk()
        return self._asks

    def reading(self):
        return [a for a in self.asks() if a.unit == 'reading']

    def leaves(self):
        """The asks a student answers: a letter whose romans the SEC prices is
        a PARENT, and its own row is the table's instruction."""
        asks = self.asks()
        parents = {(a.section, a.q, a.letter) for a in asks
                   if a.roman is not None}
        return [a for a in asks
                if a.roman is not None
                or (a.section, a.q, a.letter) not in parents]

    def listening(self):
        return [a for a in self.asks() if a.unit == 'listening']

    # ------------------------------------------------------------- rows ---
    def _rows(self):
        out = []
        with pymupdf.open(self.path) as doc:
            for pno in range(doc.page_count):
                for row in man_text.page_rows(doc[pno]):
                    out.append({'page': pno + 1, 'groups': row['groups'],
                                'y': row['y']})
        return out

    # ------------------------------------------------------------- walk ---
    def _walk(self):
        """Cut the priced units into ask BLOCKS, then parse each block.

        Read row by row this document is unparseable, because the SEC sets one
        true/false statement across THREE printed rows in a fixed order — the
        tick alone on its own baseline, then the statement, then the price —
        and a walker that decides what a row is as it passes it has to guess
        forwards. Cutting at the markers first and reading each block whole
        removes the guess: inside a block the tick, the statement and the price
        are all present at once.
        """
        blocks = self._blocks()
        asks = []
        for block in blocks:
            ask = self._parse(block)
            if ask is not None:
                asks.append(ask)
        asks = self._settle(asks)
        self._close(asks)
        return asks

    def _blocks(self):
        """[(unit, section, q, letter, roman, header, [rows])] in printed order."""
        unit, section, q, letter, header = None, None, None, None, None
        out, cur, pending_tick = [], None, None
        letter_x, table_rows = 0.0, 0
        for row in self._rows():
            groups = row['groups']
            text = _join(groups)
            if not text or FURNITURE.match(text):
                continue
            if APPENDIX.match(text):
                unit, cur = 'appendix', None
                continue
            for pat, name, sec in ((UNIT_READING, 'reading', 'A'),
                                   (UNIT_WRITING, 'writing', 'B'),
                                   (UNIT_LISTENING, 'listening', None)):
                if pat.match(text):
                    unit, section, q, letter, header, cur = \
                        name, sec, None, None, None, None
                    self.unit_marks[name] = _first_int(text)
                    break
            else:
                pass
            if any(p.match(text) for p in
                   (UNIT_READING, UNIT_WRITING, UNIT_LISTENING)):
                continue
            if unit not in ('reading', 'listening'):
                continue
            m = CHOICE_PART.search(text)
            if m and q is not None:
                self.choices.append((section, q, m.group(1), m.group(2)))
            m = SECTION_HEAD.match(text)
            if m and unit == 'listening':
                section = 'L' + m.group(1).upper()
                if m.group(2):
                    self.unit_marks[section] = int(m.group(2))
                q, letter, header, cur = None, None, None, None
                continue
            m = Q_HEAD.match(text)
            if not m and unit == 'reading':
                m = Q_BARE.match(text)
                if m and not text[m.end():].strip():
                    self.question_marks.setdefault((section, int(m.group(1))),
                                                   None)
            if m and unit == 'reading':
                q, letter, header, cur = int(m.group(1)), None, None, None
                letter_x, table_rows = 0.0, 0
                if m.re is Q_HEAD:
                    self.question_marks[(section, q)] = int(m.group(2))
                continue
            if unit == 'listening':
                m = NUMBERED.match(text)
                if m:
                    q, letter, header, cur = int(m.group(1)), None, None, None
                    groups = _rest_groups(groups, NUMBERED)
                    text = _join(groups)
                    if not text:
                        continue
            if q is None:
                continue
            cells = list(groups)
            if self._tick_only(cells):
                # The SEC sets a true/false verdict on its OWN baseline, ABOVE
                # the statement it answers — tick, statement, price, in that
                # order down the page. Held at the end of the block it follows,
                # every verdict in the corpus landed on the statement before
                # its own: Question 1(c)(i) was marked with (ii)'s tick and
                # (iii) with nothing at all. It belongs to the block that
                # opens next.
                pending_tick = cells
                continue
            if cells and _is_header(cells):
                # The header the ticks under it are read against. It also says
                # that the romans BELOW it number asks rather than answer
                # lines: a table with a True/False head prices every row.
                header = [(x0, x1, t.lower()) for x0, x1, t in cells]
                continue
            lm = LETTER.match(text)
            rm = ROMAN.match(text)
            x0 = groups[0][0] if groups else 0
            if (lm or rm) and header is not None and x0 > letter_x + 2:
                # A row of a TRUE/FALSE table, and the SEC numbers those two
                # different ways in one corpus: romans "(i)…(iv)" in most
                # sittings and LETTERS restarting at "(a)" in 2022 Higher's
                # Question 4(f), where the paper prints romans for the same
                # four rows. Neither document wins on the marker; what both
                # print is the ORDER, so a table row is keyed by its printed
                # token and carries its ordinal for man_all to pair on.
                token = (lm or rm).group(1)
                cur = (unit, section, q, letter, token, header, [], table_rows)
                out.append(cur)
                if pending_tick:
                    cur[6].append((pending_tick, row['page']))
                    pending_tick = None
                cur[6].append((_rest_groups(groups, lm and LETTER or ROMAN),
                               row['page']))
                table_rows += 1
                continue
            if lm and lm.group(1) == _next_letter(letter):
                letter, letter_x = lm.group(1), x0
                header, table_rows = None, 0
                cur = (unit, section, q, letter, None, header, [], None)
                out.append(cur)
                if pending_tick:
                    cur[6].append((pending_tick, row['page']))
                    pending_tick = None
                cur[6].append((_rest_groups(groups, LETTER), row['page']))
                continue
            if rm and header is not None:
                cur = (unit, section, q, letter, rm.group(1), header, [],
                       None)
                out.append(cur)
                if pending_tick:
                    cur[6].append((pending_tick, row['page']))
                    pending_tick = None
                cur[6].append((_rest_groups(groups, ROMAN), row['page']))
                continue
            if cur is None:
                # A question the SEC prices whole and letters nowhere — the
                # Ordinary picture-matching grid, whose eight rows are its
                # answer.
                cur = (unit, section, q, None, None, header, [], None)
                out.append(cur)
            cur[6].append((groups, row['page']))
        return out

    @staticmethod
    def _tick_only(groups):
        return bool(groups) and all(TICK.match(t) for _x0, _x1, t in groups)

    def _parse(self, block):
        unit, section, q, letter, roman, header, rows, ordinal = block
        page = rows[0][1] if rows else 1
        ask = SchemeAsk(unit, section, q, letter, roman, '', page)
        ask.ordinal = ordinal
        cue, answers, lines, raw, seen_price = [], [], [], [], False
        pending = None
        for groups, _page in rows:
            cells = list(groups)
            ticks = [(x0, x1) for x0, x1, t in cells if TICK.match(t)]
            rest = [(x0, x1, t) for x0, x1, t in cells if not TICK.match(t)]
            verdict = _verdict(ticks, header)
            price = _price_cells(rest)
            printed = ' '.join(t for _x0, _x1, t in rest).strip()
            text = _strip_price(printed)
            if price and ask.marks is None:
                ask.marks, ask.notation = price
                seen_price = True
                if text:
                    # The SEC sets the tariff on the LAST line of the ask it
                    # prices, so text on the pricing row is the tail of the
                    # QUESTION, not the head of the answer. Read as an answer
                    # it put "body parts." — the second half of Question 2(c)'s
                    # own wording — on the card as a marking point.
                    cue.append(text)
                    lines.append(text)
                raw.append((text, price[0] if price else None, verdict))
                if verdict:
                    answers.append(verdict)
                continue
            if verdict and not text:
                pending = verdict
                continue
            if not text:
                continue
            if DIRECTIVE.match(printed) or RUBRIC_ONLY.match(printed):
                # A note to the examiner, or the rubric the SEC prints between
                # two questions — "Answer either part (f) OR part (g)", "(1
                # mark for the number, 1 mark for the measure word)". Tested on
                # the line AS PRINTED, before the tariff is taken out of it,
                # because stripping first leaves debris that matches nothing:
                # "( mark for the number, mark for the measure word)" shipped
                # as a marking point on 2023 Higher's Question 2(c).
                if not RUBRIC_ONLY.match(printed):
                    ask.directives.append(printed)
                continue
            lines.append(text)
            raw.append((text, None, verdict))
            if not seen_price:
                cue.append(text)
            else:
                answers.append(text)
            if verdict:
                answers.append(verdict)
            elif pending:
                answers.append(pending)
                pending = None
        if pending and not answers:
            answers.append(pending)
        ask.raw = raw
        ask.lines = [line for line in lines if line]
        ask.cue = re.sub(r'\s+', ' ', ' '.join(cue)).strip()
        ask.answers = [a for a in answers if a]
        heads = [groups for groups, _p in rows
                 if TABLE_HEAD.search(_join(groups))
                 or any(TABLE_HEAD.search(t) for _x0, _x1, t in groups)]
        ask.table = bool(heads)
        # ONE grid in this corpus comes back intact, and it is the one the SEC
        # sets in two columns: the Ordinary paper's word-and-picture matching
        # question, whose eight rows read "苹果 C" and whose eight one-mark
        # prices sum to the eight its head prints. Every other grid here has
        # three or four columns — character, meaning, radical, meaning of the
        # radical — and its cells arrive in the wrong ROWS, so nothing in it
        # can be paired. The distinction is measured, not assumed: a grid is
        # narrow only where its own head is "Word | Letter" AND every row it
        # sets is one word beside one capital letter.
        grid_rows = [line for line in ask.lines if GRID_ROW.match(line)]
        ask.wide = ask.table and not (
            any(WORD_LETTER.match(_join(g)) for g in heads) and grid_rows)
        if ask.table and not ask.wide:
            # The SEC never reprints this question — the block opens straight
            # on "Word | Letter" — so there is nothing to subtract and the
            # rows ARE the answer, one word beside one letter.
            ask.cue = ''
            ask.answers = grid_rows
        if ask.table:
            # A grid states no total; it prices each blank a candidate fills.
            # Summing them is the SEC's own arithmetic and it is what closes
            # the question total the head prints — 2024 Higher's Question 2 is
            # 1 + 2 + 3 + 4 + twelve one-mark blanks = 22.
            everything = [c for groups, _p in rows for c in groups]
            got = _price_cells(everything, all_of_them=True, grid=True)
            if got:
                ask.marks, ask.notation = got
        return ask

    def _apply(self, ask, price, verdict):
        if ask is None:
            return
        if price and ask.marks is None:
            ask.marks, ask.notation = price
        if verdict:
            ask.answers.append(verdict)

    @staticmethod
    def _settle(asks):
        """Two things the walk cannot do until every block is read.

        **A rubric is not an ask.** "Answer Parts (a) to (g)" and "Answer
        either part (h) OR (i)" are printed under a question head with no
        marker of their own, so the block cutter opens a block for them. They
        state nothing and price nothing and are dropped.

        **A parent's RATE prices its rows.** 2022 Higher prices Question 4(f)
        once — "(4 x 3 marks)" — and prints nothing on the four true/false
        rows beneath it. Three marks each is the SEC's own split, not an
        average: it is checked against the parent's total and against the
        number of rows, and where either disagrees the rows stay unpriced and
        the question-total flag says so.
        """
        out = [a for a in asks
               if (a.letter or a.roman or a.answers or a.marks)
               and not (a.letter is None and a.roman is None
                        and not a.answers
                        and RUBRIC_ONLY.match(a.cue or ''))]
        by_parent = collections.defaultdict(list)
        for ask in out:
            if ask.roman is not None:
                by_parent[(ask.section, ask.q, ask.letter)].append(ask)
        for ask in out:
            if ask.roman is not None or not ask.notation:
                continue
            rows = by_parent.get((ask.section, ask.q, ask.letter)) or []
            unpriced = [r for r in rows if r.marks is None]
            m = re.fullmatch(r'(\d+) × (\d+)', ask.notation)
            if not (m and rows and len(unpriced) == len(rows)):
                continue
            n, per = int(m.group(1)), int(m.group(2))
            if n != len(rows) or n * per != ask.marks:
                continue
            for r in rows:
                r.marks, r.notation = per, None
        return out

    def split_against(self, paper_text_for):
        """Cut every block into the question the SEC REPRINTED and the answer
        it set under it, using the question paper as the knife.

        The scheme reprints the paper's own wording verbatim above its answer,
        so the answer is the block with the paper's text taken off the front —
        mgr_all's subtraction, and the only rule that survives both layouts in
        this corpus. 2022 Ordinary prints "(f) Translate the following
        sentences." then both sentences, both translations and both one-mark
        tariffs; 2024 Higher prints the ask, its tariff, then the answers.
        Split by "everything before the first tariff", the first put two
        Chinese sentences and their English on the card as marking points and
        priced the whole ask at one mark where the SEC prints two.

        The tariff follows the same cut: a price printed on a QUESTION row is
        the ask's own tariff, and prices printed on ANSWER rows are summed,
        which is what closes 2022 Ordinary's Question 4 on its printed 24.
        """
        for ask in self.asks():
            text = paper_text_for(ask.key)
            if not text:
                continue
            want = _fold(text)
            cut, seen = 0, ''
            for i, (line, _price, _verdict) in enumerate(ask.raw):
                nxt = seen + _fold(line)
                # An exact prefix, with no slack. A tolerance of eight
                # characters let the ANSWER be absorbed into the question
                # wherever the answer was short: "Where was 李小龙 born? Answer
                # in Chinese." followed by "美国" is three characters longer
                # than the question, and eighteen cards across four sittings
                # were refused for "stating nothing" while their answer sat
                # inside their own question text.
                if nxt and want.startswith(nxt):
                    seen, cut = nxt, i + 1
                    continue
                break
            if not cut:
                continue
            head = ask.raw[:cut]
            tail = ask.raw[cut:]
            ask.cue = re.sub(r'\s+', ' ',
                             ' '.join(t for t, _m, _v in head)).strip()
            answers = []
            for t, _m, verdict in tail:
                if DIRECTIVE.match(t):
                    continue
                if t:
                    answers.append(t)
                if verdict:
                    answers.append(verdict)
            if answers or not ask.answers:
                ask.answers = answers
            if ask.table:
                continue
            own = [m for _t, m, _v in head if m]
            tails = [m for _t, m, _v in tail if m]
            if own:
                ask.marks = own[0]
            elif tails:
                ask.marks = sum(tails)
                ask.notation = (f'{len(tails)} × {tails[0]}'
                                if len(set(tails)) == 1 and len(tails) > 1
                                else ask.notation)
        self.flags = []
        self._close(self.asks())

    def _close(self, asks):
        """Every check the two documents can make on each other, here."""
        parents = {(a.section, a.q, a.letter) for a in asks
                   if a.roman is not None}
        for ask in asks:
            if ask.unit != 'reading':
                continue
            if ask.roman is None and (ask.section, ask.q, ask.letter) in parents:
                continue                     # a parent, priced through its rows
            if ask.marks is None:
                self.flags.append({
                    'type': 'unpriced-ask',
                    'where': f'{self.year} {self.level} '
                             f'Q{ask.q}{_lbl(ask)}',
                    'detail': 'the scheme states no tariff on this ask'})
        # The question head states its own total, and the parts under it must
        # add up to it. A question that does not close is flagged, never
        # averaged: it is the arithmetic that says whether a roman is an ask or
        # an answer line.
        by_q = collections.defaultdict(int)
        for ask in asks:
            if ask.unit != 'reading' or not ask.marks:
                continue
            if ask.roman is None and (ask.section, ask.q, ask.letter) in parents:
                continue
            by_q[(ask.section, ask.q)] += ask.marks
        for section, q, _a, b in self.choices:
            for ask in asks:
                if (ask.section, ask.q, ask.letter) == (section, q, b) \
                        and ask.marks:
                    by_q[(section, q)] -= ask.marks
                    break
        for key, total in sorted(self.question_marks.items()):
            got = by_q.get(key)
            if got is not None and got != total:
                self.flags.append({
                    'type': 'question-total',
                    'where': f'{self.year} {self.level} Q{key[1]}',
                    'detail': f'its parts price {got}, its head prints {total}'})


def _fold(text):
    """The comparable shape of a printed line: letters and digits only."""
    return re.sub(r'[^0-9a-z\u4e00-\u9fff]+', '', (text or '').lower())


def _lbl(ask):
    out = f'({ask.letter})' if ask.letter else ''
    return out + (f'({ask.roman})' if ask.roman else '')


def _join(groups):
    return re.sub(r'\s+', ' ',
                  ' '.join(t for _x0, _x1, t in groups)).strip()


def _rest_groups(groups, pattern):
    """The row with its marker taken off the front, x positions preserved.

    The marker is usually a gap group of its own — the SEC sets "(a)" at x=57
    and its text at x=85 — but not always: a wrapped statement puts "(iii)
    Wednesday will be…" in one group. Both are handled by stripping the
    pattern from the FIRST group and dropping that group only if nothing is
    left of it, which keeps the tariff cell at x=454 where it was.
    """
    out = []
    for i, (x0, x1, t) in enumerate(groups):
        if i == 0:
            m = pattern.match(t)
            t = m.group(m.lastindex).strip() if m and m.lastindex and \
                m.lastindex > 1 else (t[m.end():].strip() if m else t)
            if not t:
                continue
        out.append((x0, x1, t))
    return out


# A printed GRID rather than a list of answers: the radical table and the
# character-structure table both head their columns this way.
WORD_LETTER = re.compile(r'^Word\s+Letter$')
# One word beside one capital letter. The word may itself hold a space:
# 2024 Ordinary sets "T恤" as "T 恤", and a \\S-only test dropped that row
# and left the grid seven answers against its printed eight marks.
GRID_ROW = re.compile(r'^\S[^\s]{0,3}(?:\s\S{1,3})?\s+[A-J]$')
TABLE_HEAD = re.compile(
    r'^\(Answer in (?:Chinese|English)\)|^Radical of the character'
    r'|^Radical of the$|^Meaning of the character|^Meaning of the radical'
    r'|^Meaning of the$|^Left-to-right|^Top-bottom|^Enclosed structure'
    r'|^Character in the|^Word Letter$')
# Case-sensitive and anchored, because "Meaning of the" is also four ordinary
# words: 2022 Ordinary's Question 4(i) asks a candidate to "provide the meaning
# of the words in English", and a loose test read that ask as a printed GRID
# and priced it by summing every "1 mark" on the page.


def _first_int(text):
    m = re.search(r'(\d{1,3})', text)
    return int(m.group(1)) if m else None


def _verdict(ticks, header):
    """Which column a lone tick stands in — "True" or "False"."""
    if not ticks or not header:
        return None
    x0, x1 = ticks[0]
    mid = (x0 + x1) / 2
    best = min(header, key=lambda h: abs((h[0] + h[1]) / 2 - mid))
    return best[2].capitalize()


def _price_cells(cells, all_of_them=False, grid=False):
    """(marks, notation) read from what stands in the MARKS COLUMN.

    Two shapes, both printed and neither inferred. Usually the tariff is a cell
    of its own at x>=420 — "(2 x 2 marks)" beside the ask it prices. Sometimes
    the gap between the ask and its tariff falls below the column threshold and
    the two arrive as ONE cell running from x=85 to x=516: 2024 Higher's
    Question 4(d) is that, and read strictly it was the only unpriced ask on a
    page where the SEC prices everything. So a price inside a wide cell is read
    where its own position in the cell — interpolated across the cell's printed
    width — falls in the marks column.

    `all_of_them` sums every price in the block instead of taking the first,
    which is what a priced GRID needs: the radical table prices twelve blanks
    at one mark each and states no total anywhere else.
    """
    total, notation, found = 0, None, False
    for x0, x1, t in cells:
        body = t.strip()
        for m in PRICE_ANY.finditer(body):
            span = body[m.start():m.end()]
            if not ANY_PRICE.search(span):
                continue
            at = x0 + (x1 - x0) * (m.start() / max(len(body), 1))
            whole = re.fullmatch(
                r'\(?\s*(?:\d{1,2}\s*[x×]\s*|\d{1,2}\s*\+\s*)?'
                r'\d{1,3}\s*marks?\s*\)?', body, re.I)
            if at < PRICE_X and not whole and not grid:
                # Inside a printed GRID the price is set in the cell it
                # prices — "苹果 | C (1 mark)" — so the marks column
                # says nothing there and the eight rows of every
                # Ordinary picture-matching question were unpriced.
                continue
            summed = SUM.search(body)
            if summed and summed.start() <= m.start() <= summed.end():
                a, b = int(summed.group(1)), int(summed.group(2))
                found = True
                if not all_of_them:
                    return a + b, f'{a} + {b}'
                total += a + b
                notation = notation or f'{a} + {b}'
                continue
            rate = RATE.search(span)
            if rate:
                n, per = int(rate.group(1)), int(rate.group(2))
                value, note = n * per, f'{n} × {per}'
            else:
                flat = FLAT.search(span)
                if not flat:
                    continue
                value, note = int(flat.group(1)), None
            found = True
            if not all_of_them:
                return value, note
            total += value
            notation = notation or note
    if found and all_of_them:
        return total, notation
    return None


PRICE_ANY = re.compile(
    r'\(?\s*(?:\d{1,2}\s*[x×]\s*|\d{1,2}\s*\+\s*)?'
    r'\d{1,3}\s*marks?\s*\)?', re.I)


def _strip_price(text):
    return re.sub(r'\s+', ' ', PRICE_ANY.sub(' ', text or '')).strip()


def sittings(subject=SUBJECT):
    out = []
    for name in sorted(os.listdir(schemes_dir(subject))):
        m = re.match(r'^(\d{4})-(hl|ol)\.pdf$', name)
        if m:
            out.append((int(m.group(1)), m.group(2)))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('year', nargs='?', type=int)
    ap.add_argument('level', nargs='?', default='hl')
    ap.add_argument('--full', action='store_true')
    ap.add_argument('--audit', action='store_true')
    args = ap.parse_args()
    targets = sittings() if args.audit else [(args.year, args.level)]
    for year, level in targets:
        S = ManScheme(year, level)
        asks = S.asks()
        read = S.reading()
        print(f'{year} {level}: {len(asks)} scheme asks '
              f'({len(read)} reading, {len(S.listening())} listening) '
              f'units {S.unit_marks} flags {len(S.flags)}')
        for f in S.flags:
            print(f'    FLAG {f["type"]}: {f["where"]} — {f["detail"]}')
        if args.full:
            for a in asks:
                if a.unit != 'reading':
                    continue
                print(f'  Q{a.q}{_lbl(a)} {str(a.marks):>4}m '
                      f'{a.notation or "":>6}  {a.cue[:60]!r}')
                for ans in a.answers:
                    print(f'        · {ans[:100]}')
                for d in a.directives:
                    print(f'        [{d}]')
    return 0


if __name__ == '__main__':
    sys.exit(main())
