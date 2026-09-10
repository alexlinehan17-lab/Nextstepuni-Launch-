#!/usr/bin/env python3
"""French question papers — the printed ask, in the language it was printed in.

    python3 scripts/markbank/authoring/fr_paper.py 2024 hl
    python3 scripts/markbank/authoring/fr_paper.py 2021 ol --aural

Why this subject needs its own reader
-------------------------------------
**The paper is printed bilingually.** Every ask a candidate may answer in
Irish or English is set TWICE, Irish in a left column and English in a right
one, on the same printed lines:

    1.  Ainmnigh gníomhaíocht amháin faoin aer a    1.  Name one outdoor activity that French
        thaitníonn le muintir na Fraince. (Roinn 1)      people enjoy. (Section 1)

pymupdf reads that as one stream, so a naive extraction produces "1. Ainmnigh
gníomhaíocht amháin faoin aer a 1. Name one outdoor activity that French" —
the two languages interleaved, and every ask counted twice. The columns are
unambiguous on the PAGE, so the words are grouped on their baseline and each
row is cut at the white space BETWEEN the columns. A marker opening a column
opens an ask in that column.

**And the passage is numbered like the questions.** A reading comprehension
prints its passage in numbered paragraphs — "1. Billie vit en banlieue
parisienne…" — at the same left margin, in the same shape, as "1. (a) Comment
Billie décrit-elle sa ville…". Nothing in the layout separates them. So an ask
is not identified by its marker alone: every marker on the page is a
CANDIDATE, and the one this ask is printed at is the candidate whose wording
matches the cue the scheme reprints above its answer. That is align.py's rule
(Law 4) doing the work it was written for, in the one subject where the paper
itself sets a decoy under every question number.

**The bilingual ask is chosen, not merged.** Where an ask is printed in Irish
and again in English — the opinion question at the end of every Higher
comprehension prints them stacked rather than in columns — the card carries
the run of printed lines that matches the scheme's own reprint. Both halves
are the SEC's; the scheme marks one of them, and that is the one a student
reading this card is answering.
"""
import argparse
import os
import re
import sys
import unicodedata

import pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))

SUBJECT = 'french'


def papers_dir(subject=SUBJECT):
    return os.path.join(ROOT, 'examiner-reports', subject, 'papers')


# ------------------------------------------------------- wording matching ---
WORD = re.compile(r"[^\W\d_]+", re.UNICODE)
# Words too common to be evidence of anything, in the three languages the
# paper prints. align.py's own list is English-only; scoring a French cue
# against a French paper with it leaves "de", "la", "que" carrying weight.
STOP = {
    'the', 'a', 'an', 'of', 'to', 'in', 'and', 'or', 'for', 'is', 'are', 'on',
    'at', 'by', 'with', 'from', 'that', 'this', 'it', 'as', 'be', 'what',
    'which', 'how', 'why', 'does', 'do', 'did', 'was', 'were', 'has', 'have',
    'le', 'la', 'les', 'un', 'une', 'des', 'du', 'de', 'et', 'ou', 'que',
    'qui', 'quoi', 'est', 'ce', 'se', 'sa', 'son', 'ses', 'dans', 'pour',
    'par', 'sur', 'aux', 'au', 'avec', 'pas', 'ne', 'il', 'elle', 'ils',
    'elles', 'vous', 'nous', 'plus', 'sont', 'ont', 'fait', 'the',
    'an', 'na', 'agus', 'ar', 'le', 'do', 'sa', 'is', 'go', 'ag', 'seo',
}


def fold(text):
    """Lower-case and accent-stripped, so décrit and decrit are one word."""
    return ''.join(c for c in unicodedata.normalize('NFKD', (text or '').lower())
                   if not unicodedata.combining(c))


def bag(text):
    return {w for w in WORD.findall(fold(text)) if w not in STOP and len(w) > 2}


def score(a, b):
    """Shared content words over the LONGER side.

    align.py divides by the shorter side, which is right when both sides are
    whole parts. Here one side is a candidate sub-run of printed lines, and
    dividing by the shorter side scores a one-word run at 1.00: the 2024
    Ordinary cue "Quel était le travail du père de Lily et de Lucas ?" matched
    the single word "Lucas." lifted out of the passage, and that word shipped
    as the question. Dividing by the longer side scores it 0.17 and the ask
    itself 1.00.
    """
    if not a or not b:
        return 0.0
    return len(a & b) / max(len(a), len(b))


# ------------------------------------------------------------- the layout ---
# The white space between two printed columns. Words inside a line of prose sit
# three to six points apart at this size; the columns of a bilingual ask are set
# twenty or more apart.
COLUMN_GAP = 18.0
BASELINE_TOL = 3.5

# The head of a reading comprehension. The paper sets the Irish "C.1" (Ceist) in
# its left column and the English "Q.1" in its right, so both open the same one.
RC_HEAD = re.compile(r'^[QC]\s*\.\s*(\d)\b')
SECTION_A = re.compile(r'Section\s+A\b.*Compr[ée]hension|Roinn\s+A\b.*L[ée]amhthuiscint', re.I)
# The written-production section as it opens on its own page. The paper also
# names it on its instructions page — "Section B Written Production / Production
# Écrite 100 marks" — five pages before the section itself, and anchoring on the
# name alone starts Section B in the middle of Section A. The section's own head
# prices itself in POINTS, as the French half of the paper does throughout; the
# instruction page prices it in marks.
SECTION_B = re.compile(r'Section\s+B\b.*(?:Production|Expression)\s+[ÉE]crite.*points',
                       re.I)
# A written-production question and its printed alternatives.
# 2022 and 2023 Ordinary head each written-production question bilingually on
# one line — "Ceist 1/Question 1" — where every other sitting prints "Question
# 1" alone. Requiring the bare form censused those two sittings at zero.
B_QUESTION = re.compile(r'^(?:Ceist\s+\d\s*/\s*)?Question\s+(\d)\b\s*(.*)$')
B_LETTER = re.compile(r'^\(\s*([a-c])\s*\)\s*(.*)$')
B_RUBRIC = re.compile(
    r'^(?:OU$|N\.B\.|R[ée]pondez\b|Dans cette section|Choisissez|\(\d{1,3}\s*mots)', re.I)
# A-E: 2025 Higher sets a fifth listening section.
AURAL_SECTION = re.compile(r'^(?:SECTION|ROINN)\s+([A-E])\b')
# Where the listening booklet's examination material stops. Everything after
# it is the SEC's copyright notice, and the ask that happened to be open when
# it began swallowed it.
AURAL_END = re.compile(
    r'^(?:CR[ÍI]OCH|END)\s*$'
    r"|^(?:F[óo]gra c[óo]ipchirt|Copyright notice|Acknowledge)", re.I)

# A printed marker at the head of a column: "1.", "1. (a)", "(b)".
NUM_MARK = re.compile(r'^(\d{1,2})\s*\.\s*(?:\(\s*([a-h])\s*\)\s*)?(.*)$', re.S)
LETTER_MARK = re.compile(r'^\(\s*([a-h])\s*\)\s*(.*)$', re.S)

# Page furniture the SEC prints on every page.
FURNITURE = re.compile(
    r'^(?:Leaving Certificate Examination|Scr[úu]d[úu] na hArdteistim|French\s+[–-]|'
    r'Fraincis\s+[–-]|Do not write on this page|N[áa] scr[íi]obh ar an leathanach|'
    r'Page \d+$|\d{1,3}$)', re.I)


MARKER_START = re.compile(r'^(?:\d{1,2}\s*\.|\(\s*[a-h]\s*\)|[QC]\s*\.\s*\d)')


def _gap_groups(words):
    """Words cut into printed groups at the white space between columns."""
    groups = []
    for x0, x1, word in words:
        if groups and x0 - groups[-1][1] < COLUMN_GAP:
            groups[-1][1] = x1
            groups[-1][2].append(word)
        else:
            groups.append([x0, x1, [word]])
    return [(g[0], ' '.join(g[2])) for g in groups]


def _column_x(rows, width, marker=None):
    """Where the English column starts on this page, or None.

    The white space between the columns is usually wide enough to cut a row on
    its own, but not always: 2025 Ordinary Q.2 sets an Irish question long
    enough to reach within nine points of the English marker beside it, and the
    two fuse into "Cad dó a bhfaighidh tú inspioráid ar shuíomh 4. For what
    will you find inspiration on" — one ask carrying the opening of the other.

    So the page's own right-hand column is found first, from the markers
    printed down it, and every row is then cut on that x. It is an x-BOUND, not
    a gap, which is the only thing that separates two columns whose gap has
    closed.
    """
    marker = marker or MARKER_START
    xs = [x for _p, gs in rows for x, text in gs
          if x > width * 0.4 and marker.match(text)]
    # One marker is enough when it sits past the middle of the sheet. A page
    # whose questions are set in French alone prints exactly ONE bilingual ask
    # — the opinion question at its end — and requiring two markers left that
    # ask's two languages welded together: "8. “Fuair Bernard taithí ar go leor
    # rudaí le linn 8. “Bernard experienced a lot while".
    strong = [x for x in xs if x > width * 0.5]
    if len(xs) >= 2:
        return min(xs) - 1
    return min(strong) - 1 if strong else None


def _rows(path, page_from=0, page_to=None, marker=None, split_at=None):
    """[(page, [(x0, side, text), …])] — every row, cut into its columns.

    `marker` is what opens a printed column, and it is a parameter because the
    other bilingual language papers open one with markers French never prints:
    a German ask is addressed "(b) (i)" and a roman is not a letter.

    `split_at` overrides the bound this finds for itself, for a page whose
    right-hand column opens with a marker shape _column_x does not know. It is
    passed by it_paper.py, whose Ordinary matching task rules an answer box in
    front of every English marker.

    Both are None for French, so nothing about this subject changes.

    The SIDE is decided by the page's own column bound rather than by the
    middle of the sheet. 2024 Ordinary sets its English column at x=296 on a
    595-point page, four points left of the middle: read against the midpoint
    the English "1. Write the name of the person who" falls in the left column
    while its own "(a) volunteers in a restaurant" falls in the right, and the
    four parts of that ask are orphaned from the ask they belong to.
    """
    out = []
    with pymupdf.open(path) as doc:
        last = doc.page_count if page_to is None else page_to
        for pno in range(page_from, last):
            width = doc[pno].rect.width
            rows = []
            for x0, y0, x1, y1, word, *_ in doc[pno].get_text('words'):
                if not word.strip():
                    continue
                mid = (y0 + y1) / 2
                for row in rows:
                    if abs(row['mid'] - mid) <= BASELINE_TOL:
                        row['w'].append((x0, x1, word))
                        break
                else:
                    rows.append({'mid': mid, 'w': [(x0, x1, word)]})
            ordered = [sorted(row['w']) for row in sorted(rows, key=lambda r: r['mid'])]
            page = [(pno, _gap_groups(ws)) for ws in ordered]
            split = split_at if split_at is not None else _column_x(page, width, marker)
            if split is None:
                out.extend((pn, [(x, 'L', t) for x, t in gs]) for pn, gs in page)
                continue
            for ws in ordered:
                # A row is only cut on the column bound where the page leaves
                # white space there. A full-width line — the Higher opinion
                # question runs the whole measure — has a WORD sitting across
                # that x, and cutting it would slice the ask in half.
                left = [w for w in ws if w[0] < split]
                right = [w for w in ws if w[0] >= split]
                # A row is only cut on the column bound where the page leaves
                # white space there. A full-width line has a word ACROSS that
                # x, or its neighbours a word-space apart: 2021 Ordinary sets
                # "Pourquoi les odeurs au marché étaient-elles si fortes ?"
                # right through the bound, and cutting it lost the second half
                # of the ask. Two printed columns are never a word-space
                # apart; six points is twice the space this type sets and a
                # third of the narrowest column gap measured.
                seam = (min(w[0] for w in right) - max(w[1] for w in left)
                        if left and right else COLUMN_GAP)
                if seam < 6.0:
                    out.append((pno, [(x, 'R' if x >= split else 'L', t)
                                      for x, t in _gap_groups(ws)]))
                    continue
                out.append((pno, [(x, 'L', t) for x, t in _gap_groups(left)]
                            + [(x, 'R', t) for x, t in _gap_groups(right)]))
    return out


class Block:
    """One printed marker and the lines beneath it, in one column."""

    __slots__ = ('page', 'side', 'rc', 'item', 'letter', 'lines')

    def __init__(self, page, side, rc, item, letter):
        self.page, self.side, self.rc = page, side, rc
        self.item, self.letter = item, letter
        self.lines = []

    @property
    def text(self):
        return ' '.join(' '.join(self.lines).split())

    @property
    def printed(self):
        """The block with the paper's own line breaks kept.

        A multiple-choice ask prints one option per line, and joining them into
        a paragraph makes "le prof de physique-chimie a déclenché la sonnerie a
        critiqué les élèves a voulu devenir astronaute" — four choices read as
        one run-on sentence. The session screen sets question text `pre-line`
        for exactly this.
        """
        return '\n'.join(' '.join(l.split()) for l in self.lines if l.strip())

    def __repr__(self):
        return (f'<Block p{self.page + 1} {self.side} rc{self.rc} '
                f'{self.item}{self.letter or ""} {self.text[:40]!r}>')


class FrPaper:
    """One sitting's written booklet, read as printed blocks a scheme ask can
    be matched against, plus the page span each reading comprehension occupies.
    """

    def __init__(self, year, level, subject=SUBJECT):
        self.year, self.level, self.subject = year, level, subject
        self.path = self._written_path()
        self.aural_path = self._aural_path()
        self.width = self._width(self.path)
        self.blocks = []
        self.rc_pages = {}          # rc -> [1-based pages it is printed on]
        self.rc_lead = {}           # (rc, side) -> the paper's own introduction
        self.section_b_page = None
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
        for name in (f'{self.year}-{self.level}-A00-paper.pdf',
                     f'{self.year}-{self.level}-015-paper.pdf'):
            p = os.path.join(papers_dir(self.subject), name)
            if os.path.exists(p):
                return p
        return None

    @staticmethod
    def _width(path):
        with pymupdf.open(path) as doc:
            return doc[0].rect.width

    # -- the walk -----------------------------------------------------------
    def _read(self):
        section = None
        rc = None
        lead_page = -1
        cur_item = {}
        cur = {}
        lead = {}                # side -> the lines introducing this rc
        rc_first_page = {}
        rc_last_page = {}
        for pno, groups in _rows(self.path):
            joined = ' '.join(t for _x, _s, t in groups)
            if SECTION_A.search(joined):
                section, rc = 'A', None
                cur, cur_item = {}, {}
                continue
            if SECTION_B.search(joined):
                section, rc = 'B', None
                cur, cur_item = {}, {}
                if self.section_b_page is None:
                    self.section_b_page = pno
                continue
            heads = [i for i, (_x, _s, t) in enumerate(groups)
                     if RC_HEAD.match(t) and section == 'A']
            for i in heads:
                _x0, side, text = groups[i]
                rc = int(RC_HEAD.match(text).group(1))
                rc_first_page.setdefault(rc, pno)
                rc_last_page[rc] = pno
                cur, cur_item, lead = {}, {}, {}
                lead_page = pno
                # The comprehension's own printed introduction. At Higher it
                # sits in the SAME row as the head, in a group of its own
                # ("Q.1" at the margin, "Billie en a marre des clichés…"
                # beside it); at Ordinary the head opens a column and its
                # introduction runs down that column. Taking only the head
                # group's own tail left every Higher lead empty.
                tail = RC_HEAD.match(text).group(0)
                own = text[len(tail):].strip()
                same = [t for _x, s2, t in groups[i + 1:] if s2 == side]
                lead[side] = [t for t in ([own] + same) if t]
            if heads:
                for side, lines in lead.items():
                    if lines:
                        self.rc_lead.setdefault((rc, side), lines)
                continue
            for _x0, side, text in groups:
                if section != 'A' or rc is None:
                    continue
                if FURNITURE.match(text):
                    continue
                rc_last_page[rc] = max(rc_last_page.get(rc, pno), pno)
                item = letter = None
                rest = None
                m = NUM_MARK.match(text)
                if m:
                    item, letter, rest = int(m.group(1)), m.group(2), m.group(3)
                else:
                    m = LETTER_MARK.match(text)
                    if m and cur_item.get(side):
                        item, letter, rest = cur_item[side], m.group(1), m.group(2)
                if item is not None:
                    block = Block(pno, side, rc, item, letter)
                    if rest.strip():
                        block.lines.append(rest.strip())
                    self.blocks.append(block)
                    cur[side] = block
                    cur_item[side] = item
                    lead.pop(side, None)
                elif cur.get(side) is not None:
                    cur[side].lines.append(text)
                elif side in lead and pno == lead_page:
                    # The introduction is printed on the comprehension's FIRST
                    # page, above the passage. At Ordinary the passage is set in
                    # French in the left column only, so the English column's
                    # lead is never closed by a marker and ran on to the next
                    # page — where it collected the "ANSWER IN ENGLISH" header
                    # off the top of the question page.
                    lead[side].append(text)
                    self.rc_lead[(rc, side)] = lead[side]
        for rc, first in rc_first_page.items():
            last = rc_last_page.get(rc, first)
            self.rc_pages[rc] = list(range(first + 1, last + 2))

    def lead(self, rc):
        """The paper's own introduction to a comprehension.

        Printed twice at Ordinary — Irish in the left column, English in the
        right — and once, in French, at Higher. The right-hand column is taken
        where the paper prints one, because that is the rendering the scheme
        marks and the one the card's own question is set in.
        """
        lines = self.rc_lead.get((rc, 'R')) or self.rc_lead.get((rc, 'L')) or []
        text = ' '.join(' '.join(lines).split())
        return re.sub(r'^[QC]\s*\.\s*\d\s*', '', text).strip()

    # -- matching -----------------------------------------------------------
    def candidates(self, rc, item, letter):
        return [b for b in self.blocks
                if b.rc == rc and b.item == item and b.letter == letter]

    def find(self, rc, item, letter, cue, floor=0.34, whole=False):
        """The printed ask this scheme cue is marking: (text, page, score).

        Every marker on the page is a candidate — the passage's own numbered
        paragraphs included — so the cue decides, never the marker. A candidate
        that cannot beat the floor is refused rather than guessed at.

        `whole` returns the winning block ENTIRE rather than the run that best
        matches the cue. A multiple-choice ask needs it: the scheme reprints
        only the stem ("Selon la quatrième section, Milena") and names the
        right box by its position ("Second answer"), so matching the cue trims
        the four options off the question and leaves a card asking a student to
        choose between nothing.
        """
        want = bag(cue)
        best = (0.0, None)
        for block in self.candidates(rc, item, letter):
            text, sc = _best_run(block.lines, want)
            if sc > best[0]:
                best = (sc, (block.printed if whole else text, block.page + 1, sc))
        if best[1] is None or best[0] < floor:
            return None
        return best[1]

    # -- written production -------------------------------------------------
    def section_b_asks(self):
        """[(q, letter, text, page)] for Section B, from the paper's own heads.

        Higher prints Question 1 with three alternatives and Questions 2 to 6;
        Ordinary prints Questions 1, 2 and 3 with two alternatives each. Every
        one of them is an ask the paper prints and a candidate may answer, so
        every one is a census leaf — the fact that a candidate answers only two
        of them does not make the others unprinted.
        """
        if self.section_b_page is None:
            return []
        out = []
        q = None
        cur = None
        for pno, groups in _rows(self.path, self.section_b_page):
            for _x0, side, text in groups:
                if FURNITURE.match(text) or B_RUBRIC.match(text):
                    cur = None
                    continue
                m = B_QUESTION.match(text)
                if m:
                    q = int(m.group(1))
                    cur = None
                    rest = m.group(2).strip()
                    row = [q, None, [rest] if rest else [], pno + 1, side]
                    out.append(row)
                    cur = row
                    continue
                if q is None:
                    continue
                m = B_LETTER.match(text)
                if m:
                    rest = m.group(2).strip()
                    row = [q, m.group(1), [rest] if rest else [], pno + 1, side]
                    out.append(row)
                    cur = row
                    continue
                if cur is not None and cur[4] == side:
                    cur[2].append(text)
        # An ask printed in Irish and again in English is one ask. The English
        # rendering is kept: it is the one the card is set in.
        best = {}
        for qq, letter, lines, page, side in out:
            key = (qq, letter)
            text = ' '.join(' '.join(lines).split())
            prev = best.get(key)
            if prev is None or (side == 'R' and prev[2] != 'R') or (
                    side == prev[2] and len(text) > len(prev[0])):
                best[key] = (text, page, side)
        # A lettered question has no ask of its own: its alternatives are the
        # asks, and the head merely names the choice.
        lettered = {qq for qq, letter in best if letter}
        return [(qq, letter, best[(qq, letter)][0], best[(qq, letter)][1])
                for qq, letter in sorted(best, key=lambda k: (k[0], k[1] or ''))
                if letter or qq not in lettered]

    # -- the aural booklet --------------------------------------------------
    def aural_asks(self):
        """[(section, item, letter, text)] for the Listening Comprehension.

        Read for the census only: an ask here is answerable from the recording
        alone, and fr_all.py excludes every one of them with that evidence.
        """
        if not self.aural_path:
            return []
        out = []
        section = None
        cur = {}
        cur_item = {}
        for _pno, groups in _rows(self.aural_path):
            for _x0, side, text in groups:
                m = AURAL_SECTION.match(text)
                if m:
                    section = m.group(1).upper()
                    cur, cur_item = {}, {}
                    continue
                if AURAL_END.match(text):
                    section = None
                    cur, cur_item = {}, {}
                    continue
                if section is None or FURNITURE.match(text):
                    continue
                item = letter = None
                m = NUM_MARK.match(text)
                if m:
                    item, letter, rest = int(m.group(1)), m.group(2), m.group(3)
                else:
                    m = LETTER_MARK.match(text)
                    if m and cur_item.get(side):
                        item, letter, rest = cur_item[side], m.group(1), m.group(2)
                if item is None:
                    if cur.get(side):
                        cur[side][3].append(text)
                    continue
                row = [section, item, letter, [rest.strip()] if rest.strip() else []]
                out.append(row)
                cur[side] = row
                cur_item[side] = item
        seen = {}
        for section, item, letter, lines in out:
            key = (section, item, letter)
            text = ' '.join(' '.join(lines).split())
            # The same ask is printed in Irish and in English. Keep the longer
            # of the two renderings so the census row carries something a person
            # can read; the count is what it is for, and the count is one.
            if key not in seen or len(text) > len(seen[key]):
                seen[key] = text
        return [(k[0], k[1], k[2], v) for k, v in
                sorted(seen.items(), key=lambda kv: (kv[0][0], kv[0][1], kv[0][2] or ''))]


def _best_run(lines, want, margin=0.10):
    """The contiguous run of printed lines this cue is matching.

    Where an ask is printed in Irish and then again in English — every Higher
    comprehension's opinion question — the run that matches the scheme's own
    reprint is the half the scheme marks. Where the ask is printed once, the
    whole of it wins: a shorter run is only preferred when it beats the whole
    by a clear margin, so a trailing "(Section 4)" that the scheme happened to
    drop stays on the card where the paper printed it.
    """
    if not lines:
        return '', 0.0
    whole = ' '.join(' '.join(lines).split())
    best_text, best_score = whole, score(want, bag(whole))
    for i in range(len(lines)):
        for j in range(i + 1, len(lines) + 1):
            if i == 0 and j == len(lines):
                continue
            text = ' '.join(' '.join(lines[i:j]).split())
            sc = score(want, bag(text))
            if sc > best_score + margin or (sc > best_score and len(text) > len(best_text)):
                best_text, best_score = text, sc
    return best_text, best_score


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('year', type=int)
    ap.add_argument('level')
    ap.add_argument('--subject', default=SUBJECT)
    ap.add_argument('--aural', action='store_true')
    args = ap.parse_args()
    P = FrPaper(args.year, args.level, args.subject)
    if args.aural:
        asks = P.aural_asks()
        print(f'{args.year} {args.level.upper()} aural: {len(asks)} asks')
        for section, item, letter, text in asks:
            print(f'  Section {section} Q{item}{f"({letter})" if letter else ""}  {text[:90]}')
        return 0
    print(f'{args.year} {args.level.upper()}: {len(P.blocks)} printed blocks, '
          f'comprehensions {sorted(P.rc_pages)}')
    for rc, pages in sorted(P.rc_pages.items()):
        print(f'  Q.{rc} pages {pages}  lead: {P.lead(rc)[:90]}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
