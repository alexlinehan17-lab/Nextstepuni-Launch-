#!/usr/bin/env python3
"""Italian question papers — the printed ask, and the page it was printed on.

    python3 scripts/markbank/authoring/it_paper.py 2024 hl
    python3 scripts/markbank/authoring/it_paper.py 2024 ol --aural

What this reader has to know
----------------------------
**The Ordinary paper is printed bilingually and the Higher paper is not.** An
Ordinary ask is set twice, Irish in a left column and English in a right one,
on the same printed lines; a Higher ask is set once, in Italian, because the
candidate answers it in Italian. The exception at Higher is the last ask of
every comprehension, which is set in Irish and again in English because it is
the one answered in one of those. So the column reader French needed is needed
here too — for one paper of the pair and one ask of the other — and it is
imported rather than copied: `fr_paper._rows` groups words on their baseline,
finds the page's own column BOUND from the markers printed down it and cuts
each row there, and only where the row leaves white space at that x.

**The stimulus and the questions are on facing pages, and the ANSWER RULE says
which is which.** A passage, an advertisement or a literary extract is printed
on a page of its own with nothing to write on; the questions are printed on the
next page with ruled lines under them. That alternation is exact on all twenty
pages of all ten sittings, and it is what tells the reader that the "1." at the
top of one page opens a paragraph of the passage while the "1." at the top of
the next opens the first ask. French had to settle the same question with
align.py, because its passage and its questions share a page.

The paper's own running head looked like the same signal and is not — see
ANSWER_RULE, which records what keying on it cost.

**The section a page belongs to is the section its own head last named.** All
ten sittings print ROINN A / SECTION A, ROINN B / SECTION B and ROINN C /
SECTION C, and Higher's Section B prints three routes a candidate chooses
between — the unseen passage, the prescribed novel (itself A or B) and the
essay — each with its own head. The question pages inside a section take its
sub-tokens in printed order, and the count of them is ASSERTED rather than
assumed: a sitting that prints a different number of them is flagged, not
quietly re-keyed.
"""
import argparse
import os
import re
import sys

import pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))

from fr_paper import _rows                                     # noqa: E402

SUBJECT = 'italian'


def papers_dir(subject=SUBJECT):
    return os.path.join(ROOT, 'examiner-reports', subject, 'papers')


# ------------------------------------------------------------- page heads ---
# What tells a question page from a stimulus page: the ANSWER RULE. Every page
# a candidate writes on prints ruled lines to write on and no page of printed
# matter does, and the alternation that gives is exact on all twenty pages of
# all ten sittings — Higher R.R.R.R.RRRRRRRRRRR., Ordinary R.R.R.R.R.R.R.RRRRR.
#
# The paper's own running head looked like the same signal and is not: the SEC
# heads its Ordinary question pages in Irish and its stimulus pages in English
# throughout, but 2024 Higher heads the Section B1 question page "Leaving
# Certificate Examination 2024" like a page of reading, and keying on that lost
# a whole comprehension.
#
# Eight underscores, because the matching task's answer boxes are short: it
# rules nine where a comprehension rules eighty, and a ten-character threshold
# left its page reading as printed matter in four Ordinary sittings.
ANSWER_RULE = re.compile(r'_{8,}')
SOURCE_PAGE = re.compile(r'Leaving\s+Certificate\s+Examination', re.I)

SECTION_A = re.compile(r'ROINN\s+A\b|SECTION\s+A\b')
SECTION_B = re.compile(r'ROINN\s+B\b|SECTION\s+B\b')
SECTION_C = re.compile(r'ROINN\s+C\b|SECTION\s+C\b')
# Higher's three Section B routes, each headed in Irish and in English.
B2_HEAD = re.compile(r'Sliocht\s+Liteartha\s+as\s+[ÚU]rsc[ée]al\s+Dualgais'
                     r'|Literary\s+Passage\s+from\s+Prescribed\s+Novel', re.I)
B3_HEAD = re.compile(r'Aiste\s+ar\s+th[ée]acs\s+dualgais'
                     r'|Essay\s+on\s+prescribed\s+text', re.I)
# The second prescribed novel, which the paper opens with a bare "B." beside
# its own "NÓ / OR".
B2B_HEAD = re.compile(r'^B\s*\.\s*$')

# Page furniture printed on every page of both booklets.
FURNITURE = re.compile(
    r'^(?:Leaving Certificate Examination|Scr[úu]d[úu] na hArdteistim'
    r'|Italian\s*[—–-]|Iod[áa]ilis\s*[—–-]|Rispondete in italiano'
    r'|Freagair|Answer\b|N[ÓO]$|OR$|Page \d+$|\d{1,3}$|_+$'
    r'|Is ceadmhach an leathanach|You may use this page'
    r'|D[ée]an cinnte|Make sure to label|Acknowledge|Admh[áa]lacha'
    r'|Copyright notice|F[óo]gra c[óo]ipchirt|Leathanach B[áa]n|Blank Page)',
    re.I)

# A printed marker: "1.", "1. (a)", "(b)", "a)".
NUM_MARK = re.compile(r'^(\d{1,2})\s*\.\s*(?:\(\s*([a-h])\s*\)\s*)?(.*)$', re.S)
LETTER_MARK = re.compile(r'^\(\s*([a-h])\s*\)\s*(.*)$', re.S)
PLAIN_LETTER = re.compile(r'^([a-h])\s*\)\s*(.*)$', re.S)
# The Ordinary matching task's English marker, printed behind its answer box.
RULED_MARKER = re.compile(r'^_{3,}\s*[a-h]\s*\)')
# The empty tick box the SEC prints beside "Cuir tic sa bhosca ceart / Tick the
# correct box". It reaches the text layer as U+F063, the Wingdings code point
# for an open square, and it is where the candidate writes rather than part of
# the ask — the same thing a ruled line is. Left in, the glyph gate rightly
# refused thirty-eight Ordinary cards for carrying an unreadable character.
TICK_BOX = re.compile('[\uf063\uf0a8\u2610\u25a1]')
# A multiple-choice option inside the aural Section A, and the Roman numerals
# the written paper prints for its circle-the-answer asks. Neither is an ask.
ROMAN = re.compile(r'^\(\s*(i{1,3}|iv|v)\s*\)\s*(.*)$', re.S)
# A block whose whole content is the tariff. Section C's rubric wraps its list
# of parts onto a line of its own — "(e).  (25 marks)" — which opens a block
# under the marker (e) that is not the ask (e) is.
TARIFF_ONLY = re.compile(r'^[.\s]*\(?\d{1,3}\s*(?:marks?|marc)\)?[.\s]*$', re.I)

# The order the sub-sections of one section are printed in, and how many
# question pages each level sets. Asserted, never assumed: a sitting printing a
# different number is flagged rather than re-keyed onto the wrong token.
LAYOUT = {
    # Higher sets one journalistic comprehension in Section A and three routes
    # in Section B, of which the first two print question pages of their own
    # and the third — the essay — prints its questions on the reading side.
    'hl': {'A': ['A'], 'B': ['B1', 'B2A', 'B2B']},
    # Ordinary sets two comprehensions and five publicity pieces.
    'ol': {'A': ['A1', 'A2'], 'B': ['B1', 'B2', 'B3', 'B4', 'B5']},
}


class Block:
    """One printed marker and the lines beneath it, in one column."""

    __slots__ = ('section', 'page', 'side', 'item', 'letter', 'lines')

    def __init__(self, section, page, side, item, letter):
        self.section, self.page, self.side = section, page, side
        self.item, self.letter = item, letter
        self.lines = []

    @property
    def text(self):
        return ' '.join(' '.join(self.lines).split())

    @property
    def printed(self):
        """The block with the paper's own line breaks kept.

        A circle-the-answer ask prints one option per line, and joining them
        into a paragraph makes "(i) istituzione (ii) planetario (iii) ricerca"
        read as a sentence. The session screen sets question text `pre-line`.
        """
        return '\n'.join(' '.join(l.split()) for l in self.lines if l.strip())

    def __repr__(self):
        return (f'<Block p{self.page} {self.section} '
                f'{self.item}{self.letter or ""} {self.text[:40]!r}>')


class ItPaper:
    """One sitting's two booklets, read as the asks they print."""

    def __init__(self, year, level, subject=SUBJECT):
        self.year, self.level, self.subject = year, level, subject
        self.path = self._written_path()
        self.aural_path = self._aural_path()
        self.width = self._page_width(self.path)
        self.blocks = []
        self.pages = {}          # section token -> the question pages it uses
        self.source_pages = {}   # section token -> the pages it prints to read
        self.flags = []
        self._read()

    # -- files --------------------------------------------------------------
    def _written_path(self):
        for name in (f'{self.year}-{self.level}-000-paper.pdf',
                     f'{self.year}-{self.level}-paper.pdf'):
            p = os.path.join(papers_dir(self.subject), name)
            if os.path.exists(p):
                return p
        raise FileNotFoundError(f'{self.subject} {self.year} {self.level} written paper')

    @staticmethod
    def _page_width(path):
        with pymupdf.open(path) as doc:
            return doc[0].rect.width

    def _aural_path(self):
        p = os.path.join(papers_dir(self.subject),
                         f'{self.year}-{self.level}-A00-paper.pdf')
        return p if os.path.exists(p) else None

    # -- the layout ---------------------------------------------------------
    def _page_texts(self, path):
        with pymupdf.open(path) as doc:
            return [doc[i].get_text() for i in range(doc.page_count)]

    def _layout(self):
        """(section token -> question pages, section token -> source pages).

        Read from the paper's own heads and its own running heads, and checked
        against the shape the level prints.
        """
        texts = self._page_texts(self.path)
        a_at = b_at = c_at = None
        b2_at = b3_at = None
        for i, text in enumerate(texts):
            if a_at is None and SECTION_A.search(text):
                a_at = i
            if b_at is None and i and SECTION_B.search(text):
                b_at = i
            if c_at is None and i and SECTION_C.search(text):
                c_at = i
            if self.level == 'hl':
                if b2_at is None and B2_HEAD.search(text):
                    b2_at = i
                if b3_at is None and B3_HEAD.search(text):
                    b3_at = i
        if a_at is None or b_at is None or c_at is None:
            self.flags.append('the paper does not print all three section heads')
            return {}, {}
        spans = [('A', a_at, b_at), ('B', b_at, c_at)]
        pages, source = {}, {}
        for unit, start, stop in spans:
            wanted = LAYOUT[self.level][unit]
            qpages = [i for i in range(start, stop)
                      if ANSWER_RULE.search(texts[i]) and _has_marker(texts[i])]
            if unit == 'B' and self.level == 'hl' and b3_at is not None:
                qpages = [i for i in qpages if i < b3_at]
            if len(qpages) != len(wanted):
                self.flags.append(
                    f'section {unit} prints {len(qpages)} question page(s) where '
                    f'this level sets {len(wanted)} ({wanted})')
                continue
            for token, page in zip(wanted, qpages):
                pages[token] = [page + 1]
                # The material an ask is answered from is printed on the pages
                # BEFORE its question page and after the previous one: one page
                # everywhere in this corpus, and read rather than assumed.
                prev = max([p for p in qpages if p < page] + [start - 1])
                source[token] = [i + 1 for i in range(prev + 1, page)
                                 if not ANSWER_RULE.search(texts[i])]
        if self.level == 'hl' and b3_at is not None:
            pages['B3'] = [b3_at + 1]
            source['B3'] = []
        pages['C'] = [i + 1 for i in range(c_at, len(texts))
                      if _has_marker(texts[i])]
        source['C'] = []
        return pages, source

    # -- the walk -----------------------------------------------------------
    def _read(self):
        self.pages, self.source_pages = self._layout()
        for token, pages in self.pages.items():
            # Section C, and the Higher essay on a prescribed text, are walked
            # separately because neither is answered: both are priced by a band
            # grid. Level-guarded, because "B3" at Ordinary is the third
            # publicity piece and skipping it by token alone lost four asks a
            # sitting from five sittings.
            if token == 'C' or (token == 'B3' and self.level == 'hl'):
                continue
            for page in pages:
                self._walk(token, page - 1)

    def _walk(self, token, pno):
        cur = {}
        # ONE current item across both columns, not one per column. The two
        # columns are the same questions in two languages, and the SEC numbers
        # them once: 2023 Ordinary prints "1. (a) Sa chéad fhógra…" in the
        # Irish column and only "(a) In the first advertisement…" in the
        # English one. Keyed per column, the English half of every such ask
        # belonged to no item and was dropped, and the card was set in Irish.
        cur_item = None
        rows = _rows(self.path, pno, pno + 1)
        bound = _ruled_bound(rows, self.width)
        if bound is not None:
            # Re-read the page on its own bound, so a row whose two languages
            # share a printed line is CUT there rather than sided whole.
            rows = _rows(self.path, pno, pno + 1, split_at=bound)
        for _p, groups in rows:
            for _x0, side, text in groups:
                s = _clean(text)
                if not s or FURNITURE.match(s):
                    continue
                # The right-hand column of the matching task, recovered from
                # the answer box printed in front of its marker. fr_paper finds
                # a page's column bound from the MARKERS printed down it, and
                # this page rules a box before each English marker —
                # "_________ a) Decide on the message" — so no marker opens
                # that column and the page reads as one: every one of its eight
                # asks carried both languages welded together on one row.
                #
                # Keyed on that printed box rather than on a fixed x. A
                # threshold looked simpler and was wrong: 2022 Higher indents
                # the whole of Section C Q3(a) to x=271 on a 595-point page,
                # past any sensible bound, and reading it as a right-hand
                # column would leave that ask with no text at all. The bound
                # here is the page's OWN — the leftmost ruled marker on it —
                # so it exists only on the pages that print them, and every
                # group on such a page is sided by it, continuation lines
                # included.
                if bound is not None:
                    side = 'R' if _x0 >= bound else 'L'
                if ROMAN.match(s):
                    # A circle-the-answer option. It belongs to the ask above
                    # it, which is why it is appended rather than keyed: the
                    # card has to show the boxes it offers.
                    if cur.get(side) is not None:
                        cur[side].lines.append(s)
                    continue
                item = letter = None
                opened = False
                m = NUM_MARK.match(s)
                if m:
                    item, letter, rest = int(m.group(1)), m.group(2), m.group(3)
                    opened = True
                else:
                    m = LETTER_MARK.match(s)
                    if m and cur_item:
                        item, letter, rest = cur_item, m.group(1), m.group(2)
                        opened = True
                    else:
                        m = PLAIN_LETTER.match(s)
                        if m:
                            # The matching task labels its eight asks "a)" to
                            # "h)" and numbers nothing above them.
                            item, letter, rest = None, m.group(1), m.group(2)
                            opened = True
                if not opened:
                    if cur.get(side) is not None:
                        cur[side].lines.append(s)
                    continue
                block = Block(token, pno + 1, side, item, letter)
                if rest.strip():
                    block.lines.append(rest.strip())
                self.blocks.append(block)
                cur[side] = block
                if item is not None:
                    cur_item = item

    # -- the asks -----------------------------------------------------------
    def asks(self):
        """[(section, item, letter, text, page)] — one row per printed ask.

        An ask printed in Irish and again in English is ONE ask, and the
        English rendering is kept: it is the one a card is set in. A Higher ask
        printed once, in Italian, keeps that.
        """
        best = {}
        order = []
        lettered = {(b.section, b.item) for b in self.blocks
                    if b.letter and b.item is not None}
        for b in self.blocks:
            if b.letter is None and (b.section, b.item) in lettered:
                continue          # a head whose lettered parts are the asks
            key = (b.section, b.item, b.letter)
            if key not in best:
                order.append(key)
            prev = best.get(key)
            if prev is None or (b.side == 'R' and prev.side != 'R') or (
                    b.side == prev.side and len(b.text) > len(prev.text)):
                best[key] = b
        # PRINTED order, not key order. The scheme is joined to this list
        # position by position — it numbers an ask the paper letters often
        # enough that a key join would mis-pair six asks in the corpus — so the
        # order has to be the order a candidate meets them in.
        return [(k[0], k[1], k[2], best[k].printed, best[k].page) for k in order
                if k in best]

    def matching_stem(self, token):
        """The instruction printed above the Ordinary matching task.

        It sits above the first "a)" on the question page, so no marker block
        holds it, and without it the card would show eight topics and never say
        what to do with them.

        Taken as the RIGHT-HAND group of each printed row rather than by the
        page's column bound. The bound is the markers' own left edge, and this
        instruction is set wider than they are — 2023 opens its English column
        at x=317 and its English markers at x=344 — so sided by the bound the
        instruction reads as Irish and the card carried both languages welded
        into one sentence.
        """
        pages = self.pages.get(token)
        if not pages:
            return None
        rows = []
        for _p, groups in _rows(self.path, pages[0] - 1, pages[0]):
            kept = [(x, _clean(t)) for x, _s, t in groups if _clean(t)
                    and not FURNITURE.match(_clean(t))]
            if not kept:
                continue
            if any(PLAIN_LETTER.match(re.sub(r'^_{3,}\s*', '', t))
                   or NUM_MARK.match(t) for _x, t in kept):
                break
            rows.append(kept)
        # The English column's own left edge, from the rows that print both
        # languages; a row that prints only one keeps it when it sits there.
        # 2025 breaks its instruction so that the first printed row carries the
        # English alone, and dropping single-group rows lost that line.
        rights = [max(k)[0] for k in rows if len(k) >= 2]
        if not rights:
            return None
        bound = min(rights) - 5
        # Re-read on that bound, so a row whose two languages share a printed
        # line is CUT there. 2025 sets the first line of its instruction as one
        # group — "Cad iad na pointí ar an leathanach roimhe seo Which of the
        # points in the previous page" — and read whole it is dropped as Irish.
        out = []
        for _p, groups in _rows(self.path, pages[0] - 1, pages[0],
                                split_at=bound):
            kept = [(x, _clean(t)) for x, side, t in groups
                    if _clean(t) and not FURNITURE.match(_clean(t))]
            if any(PLAIN_LETTER.match(re.sub(r'^_{3,}\s*', '', t))
                   or NUM_MARK.match(t) for _x, t in kept):
                break
            out += [t for x, t in kept if x >= bound]
        return ' '.join(' '.join(out).split()) or None

    def essay_asks(self):
        """[(route, item, text, page)] for the Higher essay on a prescribed text.

        The paper prints it as two novels, A and B, with two alternative essay
        titles under each, and the whole of it on ONE page in four columns —
        Irish beside English for each novel. Every title is an ask a candidate
        may answer, so every one is a census leaf; the scheme answers all four
        with the band descriptors of its Appendix 1.
        """
        pages = self.pages.get('B3')
        if not pages:
            return []
        page = pages[0]
        out = []
        route = None
        cur = None
        for _p, groups in _rows(self.path, page - 1, page):
            for _x0, side, text in groups:
                s = _clean(text)
                if not s or FURNITURE.match(s):
                    continue
                m = re.match(r'^([AB])\s*\.\s*(\S.*)$', s)
                if m:
                    route, cur = m.group(1), None
                    continue
                m = re.match(r'^(\d)\s*\.\s*(.*)$', s)
                if m and route:
                    cur = [route, int(m.group(1)), side,
                           [m.group(2).strip()] if m.group(2).strip() else []]
                    out.append(cur)
                    continue
                if cur is not None and cur[2] == side:
                    cur[3].append(s)
        best = {}
        for route, item, side, lines in out:
            text = ' '.join(' '.join(lines).split())
            key = (route, item)
            prev = best.get(key)
            if prev is None or len(text) > len(prev):
                best[key] = text
        return [(k[0], k[1], best[k], page) for k in sorted(best)]

    def writing_asks(self):
        """[(item, letter, text, page)] for Section C.

        Every alternative the paper prints is an ask a candidate may answer —
        Higher sets Q1 with five prompts to choose three of, Q2, and Q3 with
        two letters; Ordinary sets Q1 with two letters, Q2 and Q3 — so every
        one is a census leaf. The scheme answers all of them with the content
        and language descriptors of its Appendix 2.

        Two things are read rather than assumed. The section states how many
        questions it sets, on its own rubric line ("Answer all 3 questions"),
        and nothing numbered above that is an ask: the last Ordinary question
        is a picture story whose EIGHT ANSWER BOXES are numbered 1 to 8 down
        the page, and reading those as asks invented five questions a sitting.
        And the substantive prompt is the ITALIAN one — the task is set in
        Italian at both levels, with an Irish and English rubric beside it —
        so the longest printed rendering wins rather than the right-hand
        column, which here carries only the rubric.
        """
        out = []
        cur = {}
        cur_item = {}
        limit = self._writing_count()
        for page in self.pages.get('C', []):
            for _p, groups in _rows(self.path, page - 1, page):
                for _x0, side, text in groups:
                    s = _clean(text)
                    if not s or FURNITURE.match(s):
                        continue
                    item = letter = None
                    m = NUM_MARK.match(s)
                    if m:
                        item, letter, rest = int(m.group(1)), m.group(2), m.group(3)
                    else:
                        m = LETTER_MARK.match(s)
                        if m and cur_item.get(side):
                            item, letter, rest = cur_item[side], m.group(1), m.group(2)
                    if item is None:
                        if cur.get(side) is not None:
                            cur[side][3].append(s)
                        continue
                    if item > limit:
                        cur[side] = None
                        continue
                    row = [item, letter, page,
                           [rest.strip()] if rest.strip() else [], side]
                    out.append(row)
                    cur[side] = row
                    cur_item[side] = item
        best = {}
        for item, letter, page, lines, side in out:
            key = (item, letter)
            text = ' '.join(' '.join(lines).split())
            if TARIFF_ONLY.match(text):
                continue      # the rubric's own "(e). (25 marks)", not an ask
            prev = best.get(key)
            if prev is None or len(text) > len(prev[0]):
                best[key] = (text, page)
        lettered = {item for item, letter in best if letter}
        return [(item, letter, best[(item, letter)][0], best[(item, letter)][1])
                for item, letter in sorted(best, key=lambda k: (k[0], k[1] or ''))
                if letter or item not in lettered]

    def _writing_count(self):
        """How many questions Section C sets, from its own printed rubric."""
        with pymupdf.open(self.path) as doc:
            for page in self.pages.get('C', []):
                m = re.search(r'Answer\s+all\s+(\d)\s+questions',
                              doc[page - 1].get_text(), re.I)
                if m:
                    return int(m.group(1))
        return 3

    # -- the aural booklet --------------------------------------------------
    def aural_asks(self):
        """[(section, item, text)] for the Listening Comprehension Test.

        Read for the census only: every one of these is answerable from the
        recording alone, and it_all.py excludes each with that evidence.
        Section A's own (a)-(d) are the boxes ONE ask offers, not four asks —
        counting them would quadruple a fifth of the paper.
        """
        if not self.aural_path:
            return []
        texts = self._page_texts(self.aural_path)
        section = None
        out = []
        cur = {}
        for pno, groups in _rows(self.aural_path):
            head = texts[pno] if pno < len(texts) else ''
            if SECTION_A.search(head) and section is None:
                section = 'A'
            m = re.search(r'(?:Comhr[áa]|Dialogue)\s*(\d)', head)
            if m:
                section = f'B{m.group(1)}'
                cur = {}
            for _x0, side, text in groups:
                s = _clean(text)
                if not s or FURNITURE.match(s) or section is None:
                    continue
                if LETTER_MARK.match(s) or PLAIN_LETTER.match(s):
                    if cur.get(side) is not None:
                        cur[side][2].append(s)
                    continue
                m = NUM_MARK.match(s)
                if not m:
                    if cur.get(side) is not None:
                        cur[side][2].append(s)
                    continue
                row = [section, int(m.group(1)),
                       [m.group(3).strip()] if m.group(3).strip() else [], side]
                out.append(row)
                cur[side] = row
        best = {}
        for section, item, lines, side in out:
            key = (section, item)
            text = ' '.join(' '.join(lines).split())
            if key not in best or len(text) > len(best[key]):
                best[key] = text
        return [(k[0], k[1], best[k]) for k in sorted(best)]


def _ruled_bound(rows, width):
    """Where the English column starts on a matching-task page, or None.

    fr_paper._column_x finds a page's column bound from the markers printed
    down it, and finds none here, for two different reasons in two different
    years. 2024 and 2025 rule an answer box in FRONT of every English marker,
    so nothing on the right of the sheet looks like a marker at all; 2021 to
    2023 print the marker plainly as "a)" rather than "(a)", which is not a
    marker shape fr_paper knows. Either way the whole page reads as one column
    and each of the eight asks comes out carrying both languages welded
    together.

    So the bound is taken from the page's own BARE-LETTER markers — with or
    without a box in front of them — on the right-hand side of the sheet, and
    only where at least two are printed. No other page in this corpus prints
    one: a comprehension letters its parts "(a)", in brackets.
    """
    xs = sorted(x for _p, groups in rows for x, _s, t in groups
                if x > width * 0.35
                and PLAIN_LETTER.match(re.sub(r'^_{3,}\s*', '', t.strip())))
    # 0.35 of the sheet, not 0.4: 2021 sets its English column at x=232 on a
    # 595-point page, four points inside a 0.4 bound, and excluding it left
    # that sitting's eight asks bilingual. The Irish column's own markers sit
    # at x=62 and its continuations at x=84, so the bound has room to spare.
    return xs[0] - 1 if len(xs) >= 2 else None


def _clean(text):
    """One printed group, with the answer rules taken out of it.

    A ruled line is where the candidate writes, not part of the ask, and it
    lands inside a block whenever the SEC rules a box beside the question —
    "(i)__________________(ii) ________________" is the whole of what the paper
    prints under a two-answer ask.
    """
    return ' '.join(TICK_BOX.sub(' ', re.sub(r'_{3,}', ' ', text)).split())


def _has_marker(text):
    """Whether a page prints anything a census could key an ask to.

    The bare-letter marker counts. Ordinary's matching task is the one question
    page in the corpus that numbers nothing — its eight asks are labelled "a)"
    to "h)" — and requiring a numbered marker left it out of the layout in all
    five Ordinary sittings, which took a whole publicity piece with it.
    """
    for line in text.split('\n'):
        s = line.strip()
        if FURNITURE.match(s):
            continue
        if NUM_MARK.match(s) or PLAIN_LETTER.match(s):
            return True
    return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('year', type=int)
    ap.add_argument('level')
    ap.add_argument('--subject', default=SUBJECT)
    ap.add_argument('--aural', action='store_true')
    ap.add_argument('--full', action='store_true')
    args = ap.parse_args()
    P = ItPaper(args.year, args.level, args.subject)
    if args.aural:
        asks = P.aural_asks()
        print(f'{args.year} {args.level.upper()} aural: {len(asks)} asks')
        for section, item, text in asks:
            print(f'  Section {section} Q{item}  {text[:90]}')
        return 0
    print(f'{args.year} {args.level.upper()}: pages {P.pages}')
    if P.flags:
        for f in P.flags:
            print(f'  FLAG {f}')
    asks = P.asks()
    print(f'  {len(asks)} reading asks')
    for section, item, letter, text, page in asks:
        print(f'  {section:<4} Q{item}{f"({letter})" if letter else "":<4} p{page} '
              f' {text[:100]!r}')
    for route, item, text, page in P.essay_asks():
        print(f'  B3   {route}{item} p{page}  {text[:100]!r}')
    for item, letter, text, page in P.writing_asks():
        print(f'  C    Q{item}{f"({letter})" if letter else "":<4} p{page} '
              f' {text[:100]!r}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
