#!/usr/bin/env python3
"""Spanish question papers — the printed ask, and the pages it must be read on.

    python3 scripts/markbank/authoring/es_paper.py 2024 hl
    python3 scripts/markbank/authoring/es_paper.py 2024 hl --aural

Why this subject needs its own reader
-------------------------------------
**Each section is set in ONE language.** French prints its paper bilingually in
interleaved columns and needs a column reader; Spanish does not — a Spanish
section is printed once, and the language it is printed in IS the language the
answer must be given in. So the layout work here is different: the words are
grouped on their baselines (pymupdf's own reading order splits "(b)" from the
question beside it, because the marker sits in its own printed column at
x=56 and the ask begins at x=100), and nothing is merged across columns.

**A SECOND DOCUMENT carries Section B's text.** At Higher the Section B article
is not in the question paper at all: it is printed on a two-page loose sheet
with its own SEC file id (LC012ALP015EV), and the paper says so — "The
questions refer to the text on the loose sheet provided separately." A card
that bound its source to the question paper would open a student on the page
of QUESTIONS about an article they cannot see; a card that bound it to the
paper's own file id would do the same silently. `types/markBank.ts` warns about
exactly this on `CardSourceMaterial.sourceFileid`, and Section B cards set it.

**The passage is numbered like the questions.** Higher Section A's journalistic
text is printed in numbered paragraphs — "1. Desde hace mucho tiempo…" — at the
same margin and in the same shape as the question "1. Answer the following
questions in ENGLISH." Nothing in the layout separates them. The questions are
the LAST run of numbered markers in the region, which is what this reads: the
article is printed above its questions in every one of the ten sittings, and
the region's own text pages are everything before that run.

**A bare number is an answer box, not a question.** "Give three details" is
followed by "1.", "2." and "3." printed alone on the answer lines. A marker
with nothing after it is never an ask.
"""
import argparse
import os
import re
import sys

import pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))

SUBJECT = 'spanish'
# How far off a printed line's baseline a word may sit and still be part of it.
#
# Not a round number: the SEC sets a question's paragraph pointer against the
# RIGHT margin and 3.6 points below the marker it belongs to — "(a) ocio" at
# y=623.2 with "(para 2)" at y=626.8 — while the leading between two printed
# lines here is fourteen points. At three the pointer became a line of its own
# and attached itself to the ask ABOVE it: 2021 Higher Q.2(b) shipped carrying
# "(para 5)", which is part (c)'s paragraph, and part (c) shipped with no
# pointer at all. Four and a half is above every measured offset and a third of
# the narrowest leading.
BASELINE_TOL = 4.5


def papers_dir(subject=SUBJECT):
    return os.path.join(ROOT, 'examiner-reports', subject, 'papers')


# ------------------------------------------------------------- the layout ---
# A printed marker at the head of a line: "1.", "1. (a)", "(b)", "(iii)".
NUM_MARK = re.compile(r'^(\d{1,2})\s*\.\s*(?:\(\s*([a-h]|i{1,3}|iv|v)\s*\)\s*)?(.*)$', re.I)
LETTER_MARK = re.compile(r'^\(\s*([a-h]|i{1,3}|iv|v)\s*\)\s*(.*)$', re.I)

# The answer lines the paper prints UNDER an ask, which the baseline reader
# collects as continuation lines of that ask: "Mention three local businesses
# that will benefit." is followed by "1.", "2." and "3." on the ruled lines a
# candidate writes on, and a card that kept them asked the question with three
# empty numbers hanging off the end of it. A row that is nothing but markers is
# an answer box, never a word of the question.
ANSWER_LINE = re.compile(
    r'^(?:\d{1,2}\s*\.\s*)+$'
    r'|^(?:\(\s*(?:i{1,3}|iv|v|[a-h])\s*\)\s*)+$'
    r'|^(?:Day|Date|Time)\s*:\s*(?:(?:Day|Date|Time)\s*:\s*)*$', re.I)

# Page furniture the SEC prints on every page of every booklet.
FURNITURE = re.compile(
    r'^(?:Leaving Certificate Examination|Spanish\s*[–-]|Do not write on this page'
    r'|This is space for extra work|This question continues on the next page'
    r'|Write your answer to Section|Copyright notice|Page \d+$|\d{1,3}$)', re.I)

# The examination's own sections, as the paper heads them.
SECTION_HEAD = re.compile(r'^Section\s+([ABC])\b\s*(.*)$')
MARKS = re.compile(r'(\d{1,3})\s*marks\b', re.I)

# Higher Section A's two alternatives. 2024 prints "1. (a) Prescribed
# Literature: …"; the other four sittings print "(a) Prescribed Literature: …"
# with the question number on the line above, so the "1." is optional.
LIT_HEAD = re.compile(r'^(?:1\s*\.\s*)?\(\s*a\s*\)\s*Prescribed\s+Literature\b', re.I)
JOURNAL_HEAD = re.compile(
    r'^(?:Question\s+1\s*)?\(?\s*b\s*\)?\s*Journalistic\s+Text\b', re.I)
# "QUESTION 2 (20 marks)", "Question 2 (10 marks)".
Q_HEAD = re.compile(r'^(?:QUESTION|Question|Q)\s*\.?\s*(\d)\b\s*(.*)$')

# Higher Section C's four alternatives, as the paper prints their task text.
# The same four are also listed together in a CONTENTS block at the head of the
# section ("Question 1 (a) Dialogue Construction OR (25 marks)"), so the LAST
# printed occurrence is the task itself.
C_TASK = re.compile(r'^(?:Question|Q)?\s*\.?\s*([12])\s*\.?\s*\(\s*([ab])\s*\)\s*(.*)$')
C_BARE = re.compile(r'^\(\s*([ab])\s*\)\s*(.*)$')

# The listening booklet.
AURAL_Q = re.compile(r'^Question\s+(\d)\b\s*(.*)$')
AURAL_END = re.compile(r'^(?:Copyright notice|Acknowledge)', re.I)
# A part of a listening question. Letters ONLY: the booklet answers "(b) What
# are the minimum temperatures mentioned?" on two printed lines labelled "(i)"
# and "(ii)", and reading those as parts gave 2021 Ordinary a twenty-fourth ask
# that is an answer box. A part also has to say something — three letters of
# running text — for the same reason.
AURAL_PART = re.compile(r'^\(\s*([a-h])\s*\)\s*(.+)$')
AURAL_WORDS = re.compile(r'[A-Za-z]{3}')
# The answer lines the booklet prints under a part: "1." "2." "3." on their
# own, which the baseline reader joins onto the end of the ask.
ANSWER_LINES = re.compile(r'(?:\s*\d{1,2}\s*\.)+\s*$')

# The loose sheet: the title the SEC prints above the Section B article, which
# is the same string the marking scheme prints above its Section B answers and
# is therefore one of the three things the two documents are joined on.
INSERT_SKIP = re.compile(r'^(?:SECTION\s+B|ROINN\s+B|Leaving Certificate|Spanish\s*[–-])',
                         re.I)


def _rows(path, page_from=0, page_to=None):
    """[(page, x, text)] — every printed line, in reading order.

    Words are grouped on their baselines because the SEC sets a question's
    marker and its text as two printed columns: pymupdf's own block order
    returns "(b)" and "What happened when Bad Bunny went on stage" as separate
    lines, and a marker with no text after it is discarded by the reader below
    as an answer box.
    """
    out = []
    with pymupdf.open(path) as doc:
        last = doc.page_count if page_to is None else page_to
        for pno in range(page_from, last):
            rows = []
            for x0, y0, x1, y1, word, *_ in doc[pno].get_text('words'):
                if not word.strip():
                    continue
                mid = (y0 + y1) / 2
                for row in rows:
                    if abs(row['mid'] - mid) <= BASELINE_TOL:
                        row['w'].append((x0, word))
                        break
                else:
                    rows.append({'mid': mid, 'w': [(x0, word)]})
            for row in sorted(rows, key=lambda r: r['mid']):
                words = sorted(row['w'])
                text = ' '.join(w for _x, w in words)
                out.append((pno, words[0][0], ' '.join(text.split())))
    return out


class Block:
    """One printed marker and the lines beneath it."""

    __slots__ = ('page', 'item', 'tok', 'lines', 'row')

    def __init__(self, page, item, tok, row):
        self.page, self.item, self.tok, self.row = page, item, tok, row
        self.lines = []

    @property
    def text(self):
        return ' '.join(' '.join(self.lines).split())

    @property
    def printed(self):
        """The block with the paper's own line breaks kept.

        A choice ask prints one alternative per line — "(a) Hay que celebrar
        nuestra cultura. / O / (b) Vivir en otro país puede ser difícil." — and
        joining them into a paragraph reads as one run-on sentence. The session
        screen sets question text `pre-line` for exactly this.
        """
        return '\n'.join(l for l in self.lines if l.strip())

    @property
    def key(self):
        return (self.item, self.tok)

    @property
    def marks(self):
        """What the PAPER prices this block at, or None.

        The paper prints a question's tariff beside its own head — "2. Write in
        ENGLISH the meaning (in the context) of the following phrases: (15
        marks)" — and that number is independent of everything the scheme
        prints. The census compares the two.
        """
        m = MARKS.search(self.text)
        return int(m.group(1)) if m else None

    def __repr__(self):
        return f'<Block p{self.page + 1} {self.item}{self.tok or ""} {self.text[:40]!r}>'


class Region:
    """One addressable part of the paper: its questions and its source pages."""

    __slots__ = ('token', 'blocks', 'text_pages', 'pages', 'marks', 'title',
                 'lead_lines')

    def __init__(self, token):
        self.token = token
        self.blocks = []
        self.text_pages = []
        self.pages = []
        self.marks = None
        self.title = None
        self.lead_lines = []

    @property
    def lead(self):
        """Everything the paper prints above this region's first ask."""
        return ' '.join(' '.join(self.lead_lines).split())

    @property
    def instruction(self):
        """The region's own printed instruction, without the text beneath it.

        The lead runs from the question head straight into the article, and the
        article is what says which language the ARTICLE is in — not the answer.
        The instruction is the short lines above it: "Read about the Spanish
        Women's Football Team and answer the questions in English." A printed
        line of more than a hundred characters is prose, and prose is where the
        text starts.
        """
        out = []
        for line in self.lead_lines:
            if len(line) > 110:
                break
            out.append(line)
        return ' '.join(' '.join(out).split())

    def ask_blocks(self):
        """The region's blocks with the passage's own paragraphs dropped.

        Higher Section A's journalistic text is printed in numbered paragraphs
        at the same margin as the questions, so the region holds two runs of
        markers numbered from 1. The questions are the second — the article is
        printed above them in all ten sittings — so the asks begin at the LAST
        contiguous group of blocks numbered 1.
        """
        ones = [i for i, b in enumerate(self.blocks) if b.item == 1]
        if not ones:
            return list(self.blocks)
        start = ones[-1]
        while start > 0 and self.blocks[start - 1].item == 1:
            start -= 1
        return self.blocks[start:]

    def stems(self):
        """{question number: the Block that heads it} for lettered questions."""
        blocks = self.ask_blocks()
        parents = {b.item for b in blocks if b.tok is not None}
        return {b.item: b for b in blocks if b.tok is None and b.item in parents}

    def leaves(self):
        """[(question, part token, Block)] — what a candidate answers here.

        A block with lettered children is a STEM, not an ask: "3. Explain in
        ENGLISH the meaning of the following in their context:" is answered
        three times, at (a), (b) and (c).
        """
        blocks = self.ask_blocks()
        parents = {b.item for b in blocks if b.tok is not None}
        return [(b.item, b.tok, b) for b in blocks
                if b.tok is not None or b.item not in parents]

    def bind(self, wanted):
        """{(item, tok): Block} for the keys the scheme prices, or None each.

        Chosen from the END backwards, which is what separates a question from
        the passage paragraph printed under the same number: the article is set
        above its questions on every one of these papers, so the LAST block
        carrying a key is the ask and every earlier one is prose.
        """
        out = {}
        hi = len(self.blocks)
        for key in reversed(list(wanted)):
            found = None
            for i in range(hi - 1, -1, -1):
                if self.blocks[i].key == key:
                    found, hi = self.blocks[i], i
                    break
            out[key] = found
        return out

    def __repr__(self):
        return (f'<Region {self.token} {len(self.blocks)} blocks '
                f'pages {self.pages} text {self.text_pages}>')


class EsPaper:
    """One sitting's booklets: the written paper, the loose sheet, the aural."""

    def __init__(self, year, level, subject=SUBJECT):
        self.year, self.level, self.subject = year, level, subject
        self.path = self._path('000')
        self.insert_path = self._path('015', optional=True)
        self.aural_path = self._path('A00', optional=True)
        self.rows = _rows(self.path)
        self.section_marks = {}
        self.regions = {}
        self.insert_title = None
        self.insert_pages = []
        self._read()
        self._read_insert()

    def _path(self, component, optional=False):
        p = os.path.join(papers_dir(self.subject),
                         f'{self.year}-{self.level}-{component}-paper.pdf')
        if os.path.exists(p):
            return p
        if optional:
            return None
        raise FileNotFoundError(p)

    # -- the written paper --------------------------------------------------
    def _section_bounds(self):
        """{section letter: (first row, last row)} for A, B and C.

        The instructions page names all three sections in one list — "Section A
        Reading Comprehension 70 marks / Section B … / Section C …" — five
        pages before any of them begins. A page that names more than one
        section is that list, and is skipped: anchoring on the name alone
        starts Section B in the middle of Section A.
        """
        by_page = {}
        for i, (pno, _x, text) in enumerate(self.rows):
            m = SECTION_HEAD.match(text)
            if m:
                by_page.setdefault(pno, []).append((i, m.group(1), m.group(2)))
        heads = []
        for pno in sorted(by_page):
            found = by_page[pno]
            if len({letter for _i, letter, _rest in found}) > 1:
                continue                       # the instructions page
            i, letter, rest = found[0]
            if letter in {h[1] for h in heads}:
                continue
            heads.append((i, letter, rest))
        out = {}
        for n, (i, letter, rest) in enumerate(heads):
            end = heads[n + 1][0] if n + 1 < len(heads) else len(self.rows)
            out[letter] = (i, end)
            m = MARKS.search(rest) or MARKS.search(
                ' '.join(t for _p, _x, t in self.rows[i:i + 4]))
            if m:
                self.section_marks[letter] = int(m.group(1))
        return out

    def _read(self):
        bounds = self._section_bounds()
        if self.level == 'hl':
            self._read_hl_a(*bounds.get('A', (0, 0)))
            if 'B' in bounds:
                self._region('B', *bounds['B'])
            if 'C' in bounds:
                self._read_c(*bounds['C'])
        else:
            self._read_ol_a(*bounds.get('A', (0, 0)))
            if 'B' in bounds:
                self._read_ol_b(*bounds['B'])

    def _read_hl_a(self, start, end):
        """Section A: Question 1's two alternatives, then Question 2."""
        cuts = []
        for i in range(start, end):
            text = self.rows[i][2]
            if LIT_HEAD.match(text):
                cuts.append((i, 'A1a'))
            elif JOURNAL_HEAD.match(text):
                cuts.append((i, 'A1b'))
            else:
                m = Q_HEAD.match(text)
                if m and m.group(1) == '2' and MARKS.search(m.group(2)):
                    cuts.append((i, 'A2'))
        for n, (i, token) in enumerate(cuts):
            stop = cuts[n + 1][0] if n + 1 < len(cuts) else end
            if token == 'A2':
                self._read_q2(i, stop)
            else:
                self._region(token, i, stop)

    def _read_q2(self, start, end):
        """Question 2's two short texts, each with its own (i)-(iii)."""
        cuts = [(i, LETTER_MARK.match(self.rows[i][2]).group(1).lower())
                for i in range(start, end)
                if LETTER_MARK.match(self.rows[i][2])
                and LETTER_MARK.match(self.rows[i][2]).group(1).lower() in 'ab'
                and not LETTER_MARK.match(self.rows[i][2]).group(2).strip()]
        # The instruction that governs both texts — "Answer (a) AND (b) in
        # ENGLISH." — is printed once, above them, so it belongs to each. A
        # card that lost it would not say which language its answer must be in.
        head = [self.rows[i][2] for i in range(start, cuts[0][0] if cuts else end)
                if not FURNITURE.match(self.rows[i][2])]
        for n, (i, letter) in enumerate(cuts):
            stop = cuts[n + 1][0] if n + 1 < len(cuts) else end
            # The LETTER is this region's question, and its parts are the
            # romans printed beneath it, so a block keys ('a', 'ii').
            region = self._region(f'A2{letter}', i, stop, item=letter)
            region.lead_lines[:0] = [h for h in head if h]

    def _read_ol_a(self, start, end):
        """Ordinary Section A: five titled comprehensions, each with (a)-(h)."""
        cuts = []
        for i in range(start, end):
            m = Q_HEAD.match(self.rows[i][2])
            if m and m.group(1).isdigit():
                cuts.append((i, int(m.group(1))))
        for n, (i, q) in enumerate(cuts):
            stop = cuts[n + 1][0] if n + 1 < len(cuts) else end
            self._region(f'A{q}', i, stop, item=q)

    def _read_ol_b(self, start, end):
        """Ordinary Section B: the letter, and the note/diary alternatives."""
        cuts = []
        for i in range(start, end):
            m = Q_HEAD.match(self.rows[i][2])
            if m and m.group(1) in '12':
                cuts.append((i, int(m.group(1))))
        for n, (i, q) in enumerate(cuts):
            stop = cuts[n + 1][0] if n + 1 < len(cuts) else end
            self._region(f'B{q}', i, stop, item=q)

    def _read_c(self, start, end):
        """Higher Section C: Question 1 (a)/(b) and Question 2 (a)/(b).

        The section opens with a CONTENTS block naming all four alternatives on
        consecutive lines — "Question 1 (a) Dialogue Construction OR (25
        marks)" — five lines before the first task. The alternatives are read
        flat and the LAST printed occurrence of each wins, which is the task
        itself; the paper heads it four different ways across the five sittings
        ("Question 1 (a)", "Q 1 (a)", "Q 1. (b)", a bare "1. (b)") and all four
        are one shape with the question number and the letter optional-dotted.
        """
        found = {}
        cur_q = None
        for i in range(start, end):
            text = self.rows[i][2]
            m = C_TASK.match(text)
            if m and m.group(3).strip():
                cur_q = int(m.group(1))
                found[(cur_q, m.group(2).lower())] = (i, m.group(3).strip())
                continue
            m = Q_HEAD.match(text)
            if m and m.group(1) in '12':
                cur_q = int(m.group(1))
                continue
            m = C_BARE.match(text)
            if m and m.group(2).strip() and cur_q is not None:
                found[(cur_q, m.group(1).lower())] = (i, m.group(2).strip())
        order = sorted(found.items(), key=lambda kv: kv[1][0])
        for n, ((q, letter), (i, rest)) in enumerate(order):
            stop = order[n + 1][1][0] if n + 1 < len(order) else end
            region = self._region(f'C{q}{letter}', i, stop, item=q)
            block = Block(self.rows[i][0], q, letter, i)
            block.lines.append(rest)
            block.lines.extend(l for l in region.lead_lines if l.strip())
            region.blocks = [block] + [b for b in region.blocks if b.key != (q, letter)]

    # -- one region ---------------------------------------------------------
    def _region(self, token, start, end, item=None):
        """Cut one region into its printed marker blocks and its source pages.

        `item` fixes the question this region IS, so its parts key under it:
        the Ordinary comprehension number, the Section C question number, or —
        for Higher Section A Question 2 — the LETTER whose romans are its
        parts.

        The region's own head row is never read as a marker. Higher Section A
        heads its literature alternative "1. (a) Prescribed Literature: …" and
        runs the extract straight on from it, so reading the head as a marker
        made the whole extract one block keyed (1, 'a') — the same key as the
        ask "(a) aguantar" printed four inches below it.
        """
        region = Region(token)
        self.regions[token] = region
        cur = None
        cur_item = item
        first_ask = None
        for i in range(start, end):
            pno, _x, text = self.rows[i]
            region.pages.append(pno)
            if not text or FURNITURE.match(text):
                continue
            if i == start:
                region.lead_lines.append(text)
                continue
            key = None
            rest = None
            m = NUM_MARK.match(text)
            if m:
                # A bare "1." on an answer line is not a question. So is a
                # numbered paragraph of the passage — that one is settled by
                # Region.bind, which reads the LAST run of markers.
                if m.group(3).strip():
                    key = (int(m.group(1)), (m.group(2) or '').lower() or None)
                    if item is not None:
                        # Inside a region that IS one question, a numbered
                        # marker is a paragraph of that question's own text,
                        # never another question.
                        key = (item, key[1]) if key[1] else None
                    rest = m.group(3)
            if key is None:
                m = LETTER_MARK.match(text)
                if m and m.group(2).strip():
                    tok = m.group(1).lower()
                    key = (item if item is not None else cur_item, tok)
                    rest = m.group(2)
            if key is not None and key[0] is not None:
                block = Block(pno, key[0], key[1], i)
                if rest.strip():
                    block.lines.append(rest.strip())
                region.blocks.append(block)
                cur = block
                cur_item = key[0]
                if first_ask is None:
                    first_ask = i
                continue
            if ANSWER_LINE.match(text):
                continue
            if cur is not None:
                cur.lines.append(text)
            elif region.title is None and text.isupper() and len(text) > 8:
                region.title = text
                region.lead_lines.append(text)
            elif (region.title is not None and not region.blocks
                  and text.isupper() and 2 < len(text) <= 20
                  and region.lead_lines and region.lead_lines[-1] == region.title):
                # A long title set over two printed lines: 2024 Ordinary heads
                # its second text "ESPAÑA GANA EL / MUNDIAL", and taking the
                # first line alone named the text "ESPAÑA GANA EL" on every card
                # that quotes it.
                region.title = f'{region.title} {text}'
                region.lead_lines[-1] = region.title
            elif len(region.lead_lines) < 60:
                region.lead_lines.append(text)
        m = MARKS.search(region.instruction or region.lead)
        region.marks = int(m.group(1)) if m else None
        pages = sorted(set(region.pages))
        region.pages = [p + 1 for p in pages]
        if first_ask is not None:
            last_text_page = self.rows[first_ask][0]
            region.text_pages = [p + 1 for p in pages if p <= last_text_page]
        else:
            region.text_pages = region.pages
        return region

    # -- the loose sheet ----------------------------------------------------
    def _read_insert(self):
        if not self.insert_path:
            return
        with pymupdf.open(self.insert_path) as doc:
            self.insert_pages = list(range(1, doc.page_count + 1))
        for _pno, _x, text in _rows(self.insert_path):
            if INSERT_SKIP.match(text) or FURNITURE.match(text):
                continue
            if text.isupper() and len(text) > 8:
                self.insert_title = text
                return
            if re.match(r'^\d+\.', text):
                return

    # -- the census address -------------------------------------------------
    def leaves(self):
        """{(section, q, letter, roman): (text, region token, Block)}.

        The census key and the citation both come from here, so there is one
        statement in this directory of what a Spanish ask is called. The
        section token carries what the paper's own numbering cannot: Higher
        Section A sets TWO alternatives for its Question 1, each numbering its
        own questions from 1, so "A1a" is the prescribed-literature route and
        "A1b" the journalistic one, and "A2" is that section's second question,
        whose (a) and (b) are two separate texts.
        """
        out = {}
        for token, region in self.regions.items():
            for item, tok, block in region.leaves():
                key = self._key(token, item, tok)
                if key is not None:
                    out[key] = (block.printed, token, block)
            if not region.blocks and region.lead:
                key = self._key(token, None, None)
                if key is not None:
                    out[key] = (region.lead, token, None)
        return out

    @staticmethod
    def _key(token, item, tok):
        """(section, q, letter, roman) for one printed ask."""
        if token.startswith('A2') and len(token) == 3:
            return ('A2', None, token[2], tok)
        if token in ('A1a', 'A1b', 'B'):
            return (token, item, tok, None)
        if re.fullmatch(r'C[12][ab]', token):
            return ('C', int(token[1]), token[2], None)
        m = re.fullmatch(r'([AB])(\d)', token)
        if m:
            return (m.group(1), int(m.group(2)), tok, None)
        return None

    # -- the listening booklet ----------------------------------------------
    def aural_asks(self):
        """[(q, letter, text, page)] for the Listening Comprehension Test.

        Read for the census only: an ask here is answerable from the recording
        alone, and es_all.py excludes every one of them with that evidence.
        """
        if not self.aural_path:
            return []
        out = []
        q = None
        cur = None
        for pno, _x, text in _rows(self.aural_path):
            if AURAL_END.match(text):
                break
            if FURNITURE.match(text):
                continue
            m = AURAL_Q.match(text)
            if m:
                q, cur = int(m.group(1)), None
                continue
            if q is None:
                continue
            m = AURAL_PART.match(text)
            if m and AURAL_WORDS.search(m.group(2)):
                cur = [q, m.group(1).lower(), [m.group(2).strip()], pno + 1]
                out.append(cur)
            elif (cur is not None and not text.startswith('*')
                    and not ANSWER_LINE.match(text)):
                cur[2].append(text)
        return [(qq, letter, ANSWER_LINES.sub('', ' '.join(' '.join(lines).split())), page)
                for qq, letter, lines, page in out]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('year', type=int)
    ap.add_argument('level')
    ap.add_argument('--subject', default=SUBJECT)
    ap.add_argument('--aural', action='store_true')
    ap.add_argument('--full', action='store_true')
    args = ap.parse_args()
    P = EsPaper(args.year, args.level, args.subject)
    if args.aural:
        asks = P.aural_asks()
        print(f'{args.year} {args.level.upper()} listening: {len(asks)} asks')
        for q, letter, text, page in asks:
            print(f'  Q{q}({letter}) p{page}  {text[:90]}')
        return 0
    print(f'{args.year} {args.level.upper()}: sections {P.section_marks}, '
          f'insert {P.insert_title!r} pages {P.insert_pages}')
    for token, region in P.regions.items():
        print(f'  {token:5} pages {region.pages} text {region.text_pages} '
              f'title {str(region.title)[:40]!r} {len(region.blocks)} blocks')
        if args.full:
            for b in region.blocks:
                print(f'      {b.item}{b.tok or "":<3} p{b.page + 1} {b.text[:95]}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
