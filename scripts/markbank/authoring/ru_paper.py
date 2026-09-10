#!/usr/bin/env python3
"""Russian question papers — the printed ask, in the column it was printed in.

    python3 scripts/markbank/authoring/ru_paper.py 2024 hl
    python3 scripts/markbank/authoring/ru_paper.py 2021 ol --aural

Why this subject needs its own reader
-------------------------------------
**The paper is printed bilingually**, exactly as French's is: every ask a
candidate may answer in Irish or English is set TWICE on the same printed
lines, Irish in a left column and English in a right one. The column-cutting
in `fr_paper._rows` is what reads that, and this module reuses it rather than
copying it.

**Its markers are romans, not letters.** A Russian ask is addressed "1. (i)"
and "(ii)", never "(a)", so the marker that opens a printed column is a
different shape from French's — which is exactly the parameter `_rows` takes.

**And the passage is numbered like the questions**, again as in French: a
comprehension prints its passage in numbered paragraphs ("1. Дом был
маленький…") at the same margin, in the same shape, as "1. (i) Describe how
the fishermen spent their days." So a reading ask is not identified by its
marker alone: every marker in the unit is a CANDIDATE and the one this ask is
printed at is the candidate whose wording matches the question the scheme
reprints above its answers. That is align.py's rule (Law 4), and it is
stronger here than in any other language of the family because the Russian
scheme reprints the paper's English column verbatim.

**The units are named, not numbered.** The paper numbers "Question 1" three
times in one sitting — once in Section I, once in Section II and once in the
Listening Comprehension Test — so a bare question number addresses nothing.
Each printed question is keyed by what it IS: C1 is the Higher comprehension,
GR the grammar, MM Ordinary's mix-and-match, L2 the listening test's second
section. See UNIT_NAME in ru_scheme.py.
"""
import argparse
import os
import re
import sys

import pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, HERE)

from fr_paper import _rows, bag, score                       # noqa: E402

SUBJECT = 'russian'


def papers_dir(subject=SUBJECT):
    return os.path.join(ROOT, 'examiner-reports', subject, 'papers')


# A printed marker at the head of a column: "1.", "1. (i)", "(ii)". Romans,
# because that is how this paper addresses a part; a bare letter is never a
# marker here and reading one as a marker keyed the passage's own "a." lines.
ROMAN = r'(?:i{1,3}|iv|vi{0,3}|ix|x)'
# "1." and "1. (i)". The full stop after the number is REQUIRED when nothing
# follows it, or every "14 лет" in the passage would open an ask — but it is
# optional when a roman follows, because 2023 Ordinary prints "2 (ii) Pavel's
# parents helped him on his way to college" with no stop at all and the ask
# was read as more of the question above it.
NUM_MARK = re.compile(rf'^(\d{{1,2}})\s*\.\s*(?:\(\s*({ROMAN})\s*\)\s*)?(.*)$', re.S | re.I)
NUM_ROMAN_MARK = re.compile(rf'^(\d{{1,2}})\s*\.?\s*\(\s*({ROMAN})\s*\)\s*(.*)$', re.S | re.I)
ROMAN_MARK = re.compile(rf'^\(\s*({ROMAN})\s*\)\s*(.*)$', re.S | re.I)
MARKER_START = re.compile(
    rf'^(?:\d{{1,2}}\s*\.|\d{{1,2}}\s*\(\s*{ROMAN}\s*\)|\(\s*{ROMAN}\s*\))', re.I)

# The unit each printed head opens, in the ENGLISH column. Ordered: the dotted
# Higher forms are tested before the bare ones so "Question 1.2" is never read
# as "Question 1".
HL_HEADS = [
    (re.compile(r'^Question\s*1\s*\.\s*1\b', re.I), 'C1'),
    (re.compile(r'^Question\s*1\s*\.\s*2\b', re.I), 'LA1'),
    (re.compile(r'^Question\s*1\s*\.\s*3\b', re.I), 'CA1'),
    (re.compile(r'^Question\s*2\s*\.\s*1\b', re.I), 'C2'),
    (re.compile(r'^Question\s*2\s*\.\s*2\b', re.I), 'LA2'),
    (re.compile(r'^Question\s*3\b.*Structuring', re.I), 'SD'),
    (re.compile(r'^Question\s*1\b.*Grammar', re.I), 'GR'),
    (re.compile(r'^Question\s*2\b.*(?:Short\s+Essay|Cultural)', re.I), 'SE'),
    (re.compile(r'^Question\s*3\b.*Guided', re.I), 'GW'),
]
# Ordinary's four Section I parts are headed either by their letter or by the
# section token the SEC prints beside it, and 2021 heads the third
# "Section (C)" with the I dropped. Kept in a table of its OWN rather than one
# table filtered by level: "C." opens Ordinary's structuring discourse and
# also opens a HIGHER paper's "C. 1.2(i) Scríobh síos an t-infinideach", which
# is the Irish column of the language-awareness ask. Read from one table the
# Higher comprehension's first page was filed under Ordinary's Section I(C).
OL_HEADS = [
    (re.compile(r'^QUESTION\s*1\s*:\s*INFORMATION', re.I), 'IR1'),
    (re.compile(r'^QUESTION\s*2\s*:\s*INFORMATION', re.I), 'IR2'),
    (re.compile(r'^Language\s+awareness\b', re.I), 'LA'),
    (re.compile(r'^(?:B\.\s*Mix\s+and\s+Match|Section\s+I?\s*\(B\))', re.I), 'MM'),
    (re.compile(r'^(?:C\.\s*Structuring|Section\s+I?\s*\(C\))', re.I), 'SD'),
    (re.compile(r'^(?:D\.\s*Comprehension|Section\s+I?\s*\(D\))', re.I), 'CD'),
    (re.compile(r'^(?:A\.\s*Short\s+answers|Section\s+II\s*\(A\))', re.I), 'SA'),
    (re.compile(r'^(?:B\.\s*Extended\s+Writing|Section\s+II\s*\(B\))', re.I), 'EW'),
]
# Which of those tables is in force. Section II reuses the letters A and B
# that Section I(A)/(B) already used, so the letter alone is ambiguous and the
# section the reader is standing in decides.
SECTION_II = re.compile(r'^SECTION\s+II\b', re.I)
SECTION_I = re.compile(r'^SECTION\s+I\b(?!I)', re.I)
HL_I = {'C1', 'LA1', 'CA1', 'C2', 'LA2', 'SD'}
HL_II = {'GR', 'SE', 'GW'}
OL_I = {'IR1', 'IR2', 'LA', 'MM', 'SD', 'CD'}
OL_II = {'SA', 'EW'}

# Page furniture the SEC prints on every page.
FURNITURE = re.compile(
    r'^(?:Leaving Certificate Examination|Scr[úu]d[úu] na hArdteistim|'
    r'Russian\s*[–-]|R[úu]isis\s*[–-]|Page \d+$|\d{1,3}$|_+$|'
    r'Do not write|N[áa] scr[íi]obh)', re.I)

# The listening booklet's own sections, in the English column.
# "Q. 1.2(i)", "Question 2.2(ii)", and the bare "2.2(ii)" the SEC prints in
# its own rubric — "Answer ONE of the following: Q. 2.2(i) or 2.2(ii)" — where
# only the first of the pair carries the Q.
CHOICE_HEAD = re.compile(
    rf'(?:Q(?:uestion)?\s*\.?\s*)?\b\d\s*\.\s*\d\s*\(\s*({ROMAN})\s*\)', re.I)

AURAL_SECTION = re.compile(r'^(?:SECTION|ROINN)\s+(IV|III|II|I)\b', re.I)
AURAL_SEGMENT = re.compile(r'^(?:Segment|M[íi]r)\s*(\d{1,2})\b', re.I)
AURAL_END = re.compile(
    r'^(?:CR[ÍI]OCH|END)\s*$|^(?:F[óo]gra c[óo]ipchirt|Copyright notice|'
    r'Acknowledge)', re.I)
ROMAN_UNIT = {'I': 'L1', 'II': 'L2', 'III': 'L3', 'IV': 'L4'}


def _deweld(text):
    """One printed group split where the SAME marker opens it twice.

    The two columns of a bilingual ask fuse when the Irish line runs right up
    to the English marker beside it, and fr_paper._rows deliberately refuses
    to cut a row whose halves are a word-space apart — a full-measure line
    would be sliced in two. What is safe to cut is a group that opens
    "2.(i)" and prints "2.(i)" again inside itself: no sentence repeats its
    own question number, and the second is the English column's own marker.
    2021 Ordinary's listening Section III loses its Segment 2 ask without
    this ("2.(i) Tabhair sonra amháin faoi na cábáin ar an 2.(i) Give one
    detail about the cabins on the").
    """
    m = MARKER_START.match(text)
    if not m:
        return [text]
    token = m.group(0)
    at = text.find(token, len(token))
    if at <= 0 or text[at - 1] not in ' \t':
        return [text]
    return [text[:at].rstrip(), text[at:]]


def _dewelded(groups):
    """The row's groups, with a fused bilingual pair cut into its two columns.

    The tail of a cut takes the RIGHT side, because that is the column it was
    printed in: left where it stands, the English half of the ask is thrown
    away by the rule that keeps the English column and drops the Irish.
    """
    out = []
    for x, side, text in groups:
        parts = _deweld(text)
        out.append((x, side, parts[0]))
        for tail in parts[1:]:
            out.append((x, 'R', tail))
    return out


class Block:
    """One printed marker and the lines beneath it, in one column."""

    __slots__ = ('page', 'side', 'unit', 'item', 'roman', 'lines')

    def __init__(self, page, side, unit, item, roman):
        self.page, self.side, self.unit = page, side, unit
        self.item, self.roman = item, roman
        self.lines = []

    @property
    def text(self):
        return ' '.join(' '.join(self.lines).split())

    @property
    def printed(self):
        return '\n'.join(' '.join(l.split()) for l in self.lines if l.strip())

    def __repr__(self):
        return (f'<Block p{self.page + 1} {self.side} {self.unit} '
                f'{self.item}{f"({self.roman})" if self.roman else ""} '
                f'{self.text[:40]!r}>')


class RuPaper:
    """One sitting's two booklets, read as printed blocks under named units."""

    def __init__(self, year, level, subject=SUBJECT):
        self.year, self.level, self.subject = year, level, subject
        self.path = self._written_path()
        self.aural_path = self._aural_path()
        self.blocks = []
        self.unit_pages = {}        # unit -> [1-based pages it is printed on]
        self.unit_head = {}         # unit -> its own printed introduction
        self._read()

    # -- files --------------------------------------------------------------
    def _written_path(self):
        for name in (f'{self.year}-{self.level}-000-paper.pdf',
                     f'{self.year}-{self.level}-paper.pdf'):
            p = os.path.join(papers_dir(self.subject), name)
            if os.path.exists(p):
                return p
        raise FileNotFoundError(f'{self.subject} {self.year} {self.level} written paper')

    def _aural_path(self):
        p = os.path.join(papers_dir(self.subject),
                         f'{self.year}-{self.level}-A00-paper.pdf')
        return p if os.path.exists(p) else None

    def _split(self, path):
        """The x the ENGLISH column opens at, over the whole booklet.

        `fr_paper._column_x` finds it a page at a time, and a Russian page
        often gives it nothing to find: the summary-writing question sets its
        four asks with the two columns fused ("1. Cad a cheapann Masha … 1.
        What does Masha think about her work"), so no marker stands alone past
        the middle of the sheet and the page is read as one column with both
        languages welded together. The booklet as a whole always has markers
        to measure, and its columns do not move from page to page.

        Measured past the MIDDLE of the sheet, not past 0.45 of it. 2022
        Ordinary prints one marker at x=272 on a 595-point page whose English
        column opens at 305, and a bound set thirty points too far left read
        every Irish line long enough to reach past 272 as the start of the
        English column: five asks in that sitting then matched no printed
        question at all. A printed column of a bilingual paper always opens
        past the middle; a stray marker in the Irish measure does not.
        """
        xs = []
        with pymupdf.open(path) as doc:
            width = doc[0].rect.width
        for _pno, groups in _rows(path, marker=MARKER_START):
            for x, _side, text in groups:
                if x > width * 0.5 and MARKER_START.match(text):
                    xs.append(x)
        return min(xs) - 1 if xs else None

    # -- the walk -----------------------------------------------------------
    def _read(self):
        split = self._split(self.path)
        section = None
        unit = None
        cur = {}
        cur_item = {}
        # From page 2. The cover is a MARK TABLE that names every section of
        # the paper at once — "Roinn I (120 marc)" beside "Section II (100
        # marks)" — so a reader that takes its section from the cover starts
        # the booklet already standing in Section II, and every Section I head
        # is then filtered out as one that cannot belong there.
        for pno, groups in _rows(self.path, 1, marker=MARKER_START,
                                 fallback_split=split):
            # The section token is looked for in each printed GROUP, never in
            # the row joined back together: the SEC sets "ROINN II (60 MARC)"
            # in the Irish column and "SECTION II (60 MARKS)" beside it, and a
            # pattern anchored at the start of the joined row never sees the
            # English one at all — Ordinary's Section II heads then never
            # fired and its comprehension ran to the back cover.
            for _x, _s, t in groups:
                if SECTION_II.match(t):
                    section, unit = 'II', None
                    cur, cur_item = {}, {}
                elif SECTION_I.match(t) and section != 'II':
                    section = 'I'
            for _x, _side, text in groups:
                hit = self._head(section, text, unit)
                if hit:
                    unit = hit
                    cur, cur_item = {}, {}
                    self.unit_pages.setdefault(unit, [])
                    self.unit_head.setdefault(unit, text)
            if unit is None:
                continue
            if pno + 1 not in self.unit_pages[unit]:
                self.unit_pages[unit].append(pno + 1)
            for _x, side, text in _dewelded(groups):
                if FURNITURE.match(text) or not text.strip():
                    continue
                item = roman = None
                m = NUM_ROMAN_MARK.match(text) or NUM_MARK.match(text)
                if m:
                    item, roman, rest = int(m.group(1)), m.group(2), m.group(3)
                    found = True
                else:
                    m = ROMAN_MARK.match(text)
                    found = bool(m)
                    if m:
                        # A roman with no number of its own inherits the last
                        # number printed in this unit — and where the paper
                        # printed none at all it keeps None, because 2021 and
                        # 2022 Ordinary address the whole retrieval text
                        # "(i)" to "(viii)" with no question number anywhere.
                        # Requiring one keyed those two sittings at zero asks.
                        item, roman, rest = (cur_item.get('n'), m.group(1),
                                             m.group(2))
                if found:
                    block = Block(pno, side, unit, item,
                                  roman.lower() if roman else None)
                    if rest.strip():
                        block.lines.append(rest.strip())
                    self.blocks.append(block)
                    cur[side] = block
                    if item is not None:
                        # One number for BOTH columns, not one per column.
                        # The paper sets the number once, in the Irish column
                        # ("1. (i) Déan cur síos …"), and the English beside
                        # it opens with the roman alone. Kept per column, the
                        # English half of every ask lost its question number
                        # and the first roman of each question collided with
                        # the first roman of the next.
                        cur_item['n'] = item
                elif cur.get(side) is not None:
                    cur[side].lines.append(text)

    def _head(self, section, text, unit):
        table = HL_HEADS if self.level == 'hl' else OL_HEADS
        second = HL_II if self.level == 'hl' else OL_II
        first = HL_I if self.level == 'hl' else OL_I
        for rx, token in table:
            if not rx.match(text):
                continue
            if token in second and section != 'II':
                continue
            if token in first and section == 'II':
                continue
            if token == 'LA':
                return 'LA1' if unit in ('IR1', 'LA1', None) else 'LA2'
            return token
        return None

    # -- the join -----------------------------------------------------------
    def candidates(self, unit, item, roman):
        return [b for b in self.blocks if b.unit == unit and b.item == item
                and b.roman == roman]

    def find(self, unit, item, roman, cue, claimed=()):
        """(text, page, block) for the printed ask the scheme's cue names.

        The candidates are the blocks printed at that address; the winner is
        the one whose wording matches the cue. A comprehension's passage is
        numbered in the same shape as its questions, so a marker alone is not
        evidence that a block is an ask.

        Where the address itself does not agree — 2021 and 2022 Ordinary
        number the retrieval text's asks "(i)" to "(vi)" in the scheme and
        "1.(i)", "2.(i)" in the paper — the search widens, first to every
        block in the unit carrying that roman and then to every block in the
        unit at all. A wider search is only allowed to win on WORDING, and at
        a higher bar than the address-matched one: the paper is what a
        student is holding, so its own address is cited whatever the scheme
        calls it (see census_ru, which flags the disagreement).
        """
        for cands, bar, margin in (
                (self.candidates(unit, item, roman), 0.34, 0.0),
                ([b for b in self.blocks
                  if b.unit == unit and b.roman == roman], 0.5, 0.0),
                ([b for b in self.blocks if b.unit == unit], 0.40, 0.12)):
            cands = [b for b in cands if id(b) not in claimed]
            if not cands:
                continue
            want = bag(cue)
            ranked = sorted(((score(want, bag(b.text)), i, b)
                             for i, b in enumerate(cands)), reverse=True)
            best_s, _i, best = ranked[0]
            runner = ranked[1][0] if len(ranked) > 1 else 0.0
            # The widest search must produce a CLEAR winner, not merely the
            # best of a bad field. 2022 Ordinary numbers its retrieval asks
            # "(i)" to "(vi)" in the scheme and "1." to "6." in the paper, so
            # nothing but the wording joins them, and two of its asks open
            # with the same three words ("Name two additional subjects
            # available" against "Name three subjects taught at the school").
            # Every one of the six is its own top candidate by at least
            # fourteen points; a pairing closer than twelve is not evidence.
            if best_s >= bar and best_s >= runner + margin:
                return best.printed, best.page + 1, best
        return None

    def choice_romans(self, unit):
        """The alternatives a unit prints as "Q. 1.2(i) … OR Q. 1.2(ii) …".

        Higher's two language-awareness questions each print a choice of two
        tasks and a candidate answers one. Both are printed, both are priced,
        and both are asks the paper sets — so both are census leaves. They
        are read from the paper's own head rather than from the scheme
        because the census denominator is the paper.
        """
        found = []
        for page in self.unit_pages.get(unit, []):
            with pymupdf.open(self.path) as doc:
                text = doc[page - 1].get_text()
            for m in CHOICE_HEAD.finditer(text):
                r = m.group(1).lower()
                if r not in found:
                    found.append(r)
        return found

    def unit_items(self, unit):
        """The question numbers a unit prints in its English column."""
        sides = {b.side for b in self.blocks if b.unit == unit}
        want = 'R' if 'R' in sides else 'L'
        return sorted({b.item for b in self.blocks
                       if b.unit == unit and b.side == want
                       and b.item is not None})

    # -- the other booklets -------------------------------------------------
    def aural_asks(self):
        """[(unit, item, roman, text)] — the listening booklet's own asks."""
        if not self.aural_path:
            return []
        out = []
        split = self._split(self.aural_path)
        unit = None
        cur = {}
        cur_item = {}
        stop = False
        for pno, groups in _rows(self.aural_path, marker=MARKER_START,
                                 fallback_split=split):
            if stop:
                break
            for _x, side, text in _dewelded(groups):
                if AURAL_END.match(text):
                    stop = True
                    break
                m = AURAL_SECTION.match(text)
                if m:
                    unit = ROMAN_UNIT[m.group(1).upper()]
                    cur, cur_item = {}, {}
                    continue
                if unit is None or FURNITURE.match(text) \
                        or AURAL_SEGMENT.match(text):
                    continue
                item = roman = None
                m = NUM_ROMAN_MARK.match(text) or NUM_MARK.match(text)
                found = bool(m)
                if m:
                    item, roman, rest = int(m.group(1)), m.group(2), m.group(3)
                else:
                    m = ROMAN_MARK.match(text)
                    found = bool(m)
                    if m:
                        item, roman, rest = (cur_item.get('n'), m.group(1),
                                             m.group(2))
                if found:
                    b = Block(pno, side, unit, item,
                              roman.lower() if roman else None)
                    if rest.strip():
                        b.lines.append(rest.strip())
                    out.append(b)
                    cur[side] = b
                    if item is not None:
                        cur_item['n'] = item
                elif cur.get(side) is not None:
                    cur[side].lines.append(text)
        # The English column is the one a card carries — but the choice is
        # made PAGE by PAGE. 2025 Ordinary sets its first listening page with
        # the two columns close enough to fuse, so that page produced no
        # right-hand blocks at all; dropping every left-hand block in the
        # booklet because a LATER page had a right-hand one lost the whole of
        # its first two segments from the denominator.
        by_page = {}
        for b in out:
            by_page.setdefault(b.page, []).append(b)
        keep = []
        for _page, blocks in sorted(by_page.items()):
            sides = {b.side for b in blocks}
            keep += [b for b in blocks
                     if b.side == ('R' if 'R' in sides else 'L')]
        seen = set()
        asks = []
        for b in keep:
            key = (b.unit, b.item, b.roman)
            # A marker with nothing under it is not an ask. Cutting a fused
            # bilingual row can leave the English marker alone on its line
            # when the question itself wrapped, and keying it added three
            # empty leaves to the denominator.
            if key in seen or not b.printed.strip():
                continue
            seen.add(key)
            asks.append((b.unit, b.item, b.roman, b.printed))
        return asks


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('year', type=int)
    ap.add_argument('level')
    ap.add_argument('--aural', action='store_true')
    args = ap.parse_args()
    P = RuPaper(args.year, args.level)
    if args.aural:
        for unit, item, roman, text in P.aural_asks():
            addr = f'{item}({roman})' if roman else str(item)
            print(f'{unit:4} {addr:8} {text[:90]}')
        return 0
    for unit, pages in P.unit_pages.items():
        print(f'{unit:4} pages {pages}')
    for b in P.blocks:
        addr = f'{b.item}({b.roman})' if b.roman else str(b.item)
        print(f'  {b.unit:4} p{b.page + 1:<3} {b.side} {addr:8} {b.text[:80]}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
