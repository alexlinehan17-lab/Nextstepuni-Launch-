#!/usr/bin/env python3
"""Religious Education marking schemes — the answer, and only the answer.

    python3 scripts/markbank/authoring/re_scheme.py 2023 hl
    python3 scripts/markbank/authoring/re_scheme.py --audit

Why no existing parser fits
---------------------------
Every generic block parser in this directory keys a marking point to a mark
printed on or beside it. Religious Education prints no such thing. One ask is
one unit:

    Question 1 (a) (i) 20M            <- the head, carrying the whole tariff
    Imagine Plato was giving a talk about the nature of reality ...
    Marking Criteria and points of reference
    An excellent answer will show knowledge of ... e.g.        <- the lead-in
    • True reality and meaning is found through intellectual ideas etc.
    • True happiness is found through gaining wisdom and virtuous living etc.
    • Etc.
    Code MC✓ in left margin where the Marking Criteria is first evident ...
    A 1 (a) (i) EXCELLENT VERY GOOD GOOD FAIR WEAK POOR       <- the BAND GRID
    ... substantial evidence | very good evidence | good evidence ...
    20M   20 - 17   16 - 14   13 - 11   10 - 8   7 - 5   4 - 0

Not one of the ~990 content bullets in the corpus carries a mark of its own,
so no per-row mark exists to be read, and inventing one would be the guessed
tariff this bank has been burned by five times. The deck's shape for exactly
that is `questionTotal`: the tariff lives on the question, the rows carry
`marks: null`.

THE BAND GRID MUST BE DISCARDED. It is the biggest correctness risk in this
subject: read as marking points it ships "substantial evidence", "very good
evidence", "clearly relevant" and "no major errors(s)" as things a student is
supposed to have written. This parser stops dead at the first grid line and
asserts, in audit(), that no shipped point contains grid vocabulary.

Four head grammars, all read here:

    2018-2020     "A 1 a) i. How do I decide ... part of life? 20M"
                  the question text follows the marker ON the head line (or
                  starts on the next), tariff at the END of the question text;
                  many asks print the criteria with no points of reference
    2021          "A 1 a)"            tariff at the END of the question text
    2022          "Section A Question 1 (a)"          likewise
    2023-2025     "Question 1 (a) (i) 20M"            tariff ON the head
                  "Question B (b) (20M x 2)"
                  "Or Question E (c) 80M (40MX2)"     the alternative branch

Sections B-J print no question number at all — the section IS the question
there — so `q` is None for them and the citation reads "Section E Q(b)(ii)".
"""
import argparse
import glob
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))


def schemes_dir():
    return os.path.join(ROOT, 'examiner-reports', 'religious-education', 'schemes')


# ---------------------------------------------------------------- the head ---
# "Or " opens the alternative branch of a choice ("Or Question E (b) (i) 40M")
# and is the examiner's word for which route is being marked, not part of the
# address. Case varies: 2025 Higher prints "QUESTION B (c) (40M)" in capitals
# and "Question I (C) (20M x2)" with a capital part letter.
# 2026 adds three printings: the section letter set hard against its part
# ("Question D(b) (20M x 2)", "Eb (ii) (40M)") and a part letter with no
# bracket at all after the section letter ("Question E a (40Mx2)",
# "Question E b (i) (20M X2)"). The bare letter is read only straight after a
# section letter and before a space, so "a" or "b" inside prose never opens a
# head.
HEAD = re.compile(
    r'^(?:Or\s+)?'
    r'(?:(?:Section|SECTION)\s+([A-J])\b\s*)?'
    r'((?:Question|QUESTION)\s+)?'
    r'(?:([A-J])(?:\s+|(?=\(|[a-h]\b)))?'
    r'(\d)?\s*'
    r'(?:\(([A-Ha-h])\)|([a-h])\)|(?<=[A-J])([a-h])(?=\s)|(?<=[A-J]\s)([a-h])(?=\s))'
    r'(?:\s*(?:\(([ivxIVX]{1,3})\)|([ivx]{1,3})\.))?'
    r'\s*(.*)$')

SECTION_HEAD = re.compile(r'^(?:SECTION|Section)\s+([A-J])\b')
ROMAN_LINE = re.compile(r'^(i{1,3}|iv|v)\.\s+(\S.*)$')

# The tariff, as the SEC writes it. Whitespace and case vary freely ("20Mx2",
# "20M x 2", "(40 M)", "(20mx2)"); the shapes do not.
#   40M            one answer, forty marks
#   20Mx2          TWO answers at twenty each — the ask is worth forty
#   40M (20Mx2)    the same thing said twice: total, then the split
#   40M/20Mx2      marked either as one forty or as two twenties
TARIFF_ONE = re.compile(r'^\(?(\d{1,3})\s*M\s*(?:[x×]\s*(\d))?\)?$', re.I)
# The same tariff with the multiplier written BEFORE the M: 2022 Higher F(a)(ii)
# prints "20x2M" where every other ask prints "20Mx2". Both mean two answers at
# twenty, and the paper prices that part at 40.
TARIFF_PRE = re.compile(r'^\(?(\d{1,3})\s*[x×]\s*(\d)\s*M\)?$', re.I)
TARIFF_PAIR = re.compile(
    r'^\(?(\d{1,3})\s*M\)?\s*[/(]\s*(\d{1,3})\s*M\s*[x×]\s*(\d)\)?$', re.I)


# 2026 Higher prints one head's tariff as the paper prints it, a bare "(40)"
# with no M ("C (b) (40)"). Read on a HEAD only, where nothing else is printed.
TARIFF_BARE = re.compile(r'^\((\d{2})\)$')


# 2010-2012's margin tariff: a bare number ending a line of the question.
BARE_MARGIN = re.compile(r'(?:\s|^)(\d{2})\s*$')


def parse_tariff(text):
    """(total, notation) for a printed tariff, or None. Never a guess.

    Returns None for anything it does not recognise, and the caller then
    refuses the ask. No printed tariff, no card.
    """
    raw = ' '.join((text or '').split())
    if not raw:
        return None
    flat = raw.replace(' ', '')
    m = TARIFF_PAIR.match(flat)
    if m:
        total, each, times = int(m.group(1)), int(m.group(2)), int(m.group(3))
        # The bracketed split has to make the total it is bracketed under, or
        # the two halves of the tariff disagree and neither can be trusted.
        return (total, raw) if each * times == total else None
    m = TARIFF_ONE.match(flat)
    if m:
        each = int(m.group(1))
        times = int(m.group(2) or 1)
        return each * times, raw
    m = TARIFF_PRE.match(flat)
    if m:
        return int(m.group(1)) * int(m.group(2)), raw
    m = TARIFF_BARE.match(flat)
    if m:
        return int(m.group(1)), raw
    return None


# The tariff printed at the END of the question text, which is where 2021 and
# 2022 put it: "...associated with people who lived in ancient times. 20Mx2".
# The space before it is optional: 2022 Higher F(a)(i) prints "...that you
# have studied.40M" with the tariff welded to the full stop, and requiring a
# space refused two asks whose tariff is on the page.
_TAR = r'\d{1,3}\s*(?:M\s*[x×]\s*\d|[x×]\s*\d\s*M|M)'
# 2026 sets the trailing tariff in brackets: "...of his time in Palestine.
# (10M x 2)", "...religion in Ireland today. (20M x2)".
# 2020 Higher H(b)(ii) closes its tariff with a full stop: "...traditions. 20M."
TRAILING_TARIFF = re.compile(
    rf'(?:\s|(?<=[.?!:]))(\(?(?:{_TAR})(?:\s*/\s*(?:{_TAR}))?\)?)\.?\s*$', re.I)

LEAD = re.compile(r'^An excellent (?:answer|coursework)\b')
# 2010-2017 head the points of reference "Possible Points": the lead-in stops
# there. Read for those years only: 2025 Higher I(b) prints "Possible points:"
# inside its lead-in, and its shipped card keeps the lead-in as it was read.
POSSIBLE = re.compile(r'^Possible\s+Points\b', re.I)
# 2010-2017 print the heading as "Marking Criteria" alone ("Marking Criteria.").
MC_HEADING = re.compile(r'^Marking\s+Crit\w*(?:\s+and\s+points\s+of\s+reference|\s*[.:]?\s*$)', re.I)

# Where the marking points STOP. Each of these opens the examiner's apparatus
# rather than the answer.
CODE_LINE = re.compile(r'^Code\s+MC', re.I)
GRID_HEAD = re.compile(r'(?:EXCELLENT|Excellent)\s+(?:VERY\s+GOOD|Very\s+Good)', re.I)
GRID_ROW = re.compile(
    r'^Evidence of MC\b'
    r'|^Use of skill\(s\)'
    r'|^(?:Factual\s+)?(?:Accuracy|accuracy)\b'
    r'|^Relevance\s*&'
    r'|errors\(s\)'
    r'|^\(?\d{1,3}\s*Marks?\s*(?:[x×]\s*\d)?\)?\s+\d{1,3}\s*[-–]\s*\d{1,3}\b'
    r'|^\d{1,3}\s*M(?:\s*[x×]\s*\d)?\s+\d{1,3}\s*[-–]\s*\d{1,3}\b')
NOTE = re.compile(r'^(?:Note|N\.B\.|Consult your Advising Examiner)\b', re.I)
# Page furniture. The bare page number must be anchored at BOTH ends: without
# the closing anchor "40Mx2" reads as page 40, and the tariff line 2021 prints
# on its own was thrown away — four asks refused for having no tariff while
# the tariff sat on the line above.
PAGE = re.compile(r'^(?:##\s*Page\s*\d+\s*$|\d{1,3}\s*$|Page\s+\d{1,3}\s*$|Leaving Certificate\b'
                  r'|Religious Education\b|Coimisi|State Examinations)', re.I)

# A sitting whose scheme draws its point bullet in a symbol font with no
# Unicode, so the bullet reaches the text as another character at the head
# of the line. Each settled by cropping the glyph: a round bullet.
SITTING_BULLET = {
    (2016, 'hl'): 'x',          # SymbolMT, 67 lines
    (2014, 'hl'): '\x9a',       # Symbol, 73 lines
    (2014, 'ol'): '\x9a',       # Symbol, 100 lines
}

BULLETS = '•●▪■'
BULLET = re.compile(rf'^[{BULLETS}]\s*')
ETC_ONLY = re.compile(rf'^[{BULLETS}]?\s*Etc\.?\s*$', re.I)

# Two asks in the corpus set their points with NO bullet at all: the examiner
# lists them by the religion each belongs to, indented under a LIST heading,
# and the PDF confirms there is no bullet glyph to find (2021 Higher C(b),
# 2021 Ordinary C(c)). The dash after a named religion is the SEC's own
# separator between an answer's subject and the answer, so it opens a point in
# exactly the way a bullet does. Used ONLY where the body produced no bullets
# and EVERY line of it opens this way — anything less and the segmentation
# would be invented rather than read.
NAMED_POINT = re.compile(
    r'^(?:(?:LIST|List)\s+[AB]:\s*)?'
    r'[A-Z][A-Za-z\u2019\' ]{2,24}?\s*[\u2013\u2014-]\s+\S')

# Vocabulary that belongs to the six-column band grid and can never be a
# marking point. audit() asserts no shipped point contains any of it.
GRID_WORDS = re.compile(
    r'\b(?:substantial evidence|very good evidence|good evidence'
    r'|adequate evidence|inadequate evidence|clearly relevant'
    r'|generally relevant|limited relevance|little relevance'
    r'|no major errors|errors\(s\)|NO GRADE)\b', re.I)

ROMANS = ['i', 'ii', 'iii', 'iv', 'v']


class Ask:
    __slots__ = ('section', 'q', 'letter', 'roman', 'total', 'notation',
                 'cue', 'lead', 'points', 'open_list', 'notes', 'line')

    def __init__(self, **kw):
        for k in self.__slots__:
            setattr(self, k, kw.get(k))

    @property
    def key(self):
        return (self.section, self.q, self.letter, self.roman)

    def __repr__(self):
        return f'<Ask {self.section} {self.q} {self.letter} {self.roman} {self.notation}>'


def _lead_span(lines):
    """How many opening lines are still the lead-in paragraph.

    The lead-in ends on the SEC's own "e.g."; where the scheme prints no
    lead-in at all there is nothing to skip.
    """
    for j, line in enumerate(lines):
        if re.search(r'\be\.g\.\s*$', line):
            return j + 1
    return 0


class ReScheme:
    """One published scheme, read as a list of asks."""

    def __init__(self, year, level):
        self.year, self.level = year, level
        self.path = os.path.join(schemes_dir(), f'{year}-{level}.md')
        with open(self.path, encoding='utf-8') as fh:
            # a glyph drawn with no Unicode reaches the text layer as a control
            # character: 2016 Higher C(b) prints its tariff "40M\x03"
            self.lines = [re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', ' ', l).strip()
                          for l in fh.read().split('\n')]
        glyph = SITTING_BULLET.get((year, level))
        if glyph:
            self.lines = [re.sub(rf'^{re.escape(glyph)}\s+', '• ', l) for l in self.lines]
        if year <= 2012:
            # 2010-2012 set sub-points with a Courier "o" ("o Ineffable i.e.
            # ...", "o Etc."): each is a point of its own, as printed
            self.lines = [re.sub(r'^o\s+(?=[A-Z])', '• ', l) for l in self.lines]
        self.asks = []
        self.refused = []
        self._read()

    # -- segmentation -------------------------------------------------------
    def _heads(self):
        """(line index, section, q, letter, roman, head tail) for every ask head.

        A head is a marker line whose tail is EMPTY or a tariff. That test is
        what keeps the band grid out: its rows open with the very same marker
        ("A 1 (a) EXCELLENT VERY GOOD ...", "G (b) EXCELLENT ..."), and a
        marker regex alone reads 153 of them as asks.
        """
        section = None
        prev_section = False
        out = []
        for i, line in enumerate(self.lines):
            s = SECTION_HEAD.match(line)
            if s:
                section = s.group(1)
            m = HEAD.match(self._normalise(line, section))
            if not m and self.year <= 2012 and section and prev_section:
                # a section that prints ONE ask, its head the section letter on
                # the line under the section's heading: "3 E ♦ BUDDHISM ... 80",
                # "J ● GOD OF THE GAPS ...", "I After Saint Patrick ..."
                one = re.match(rf'^(?:[123]\s+)?{section}\s+(?![a-h]\))(\S.*)$', line)
                if one:
                    out.append((i, section, None, None, None, one.group(1).strip()))
                    prev_section = False
                    continue
            if line:
                prev_section = bool(s)
            if not m:
                # 2014-2017 set a part's romans as lines of their own under its
                # stem: "G a) Outline ... headings:" / "i. The origins ... 20M"
                # / ... / "ii. Meditation techniques ... 20M". Each roman is an
                # ask of that part.
                r = ROMAN_LINE.match(line) if self.year <= 2017 else None
                # "i. AUTHORITATIVE SOURCE ii. PRIMARY OR SECONDARY SOURCE"
                # (2014 Ordinary B(c)) lists the headings ONE answer is written
                # under: a line naming two romans is not an ask
                if r and re.search(r'\s(?:i{1,3}|iv|v)\.\s', r.group(2)):
                    r = None
                if r and out and out[-1][3] is not None:
                    _i, sec, q, letter, _roman, _t = out[-1]
                    out.append((i, sec, q, letter, r.group(1), r.group(2).strip()))
                continue
            tail = (m.group(11) or '').strip()
            if tail and parse_tariff(tail) is None and not self._text_head(m):
                continue
            # A head names itself: it carries the word Question or Section, or
            # its own section letter, or a question number. A BARE marker line
            # — "(a) (i)" — is a wrapped band-grid cell, not an ask. 2025
            # Ordinary prints exactly that inside F(a)(ii)'s grid, and reading
            # it as a head handed F(a)(i) the grid's own text.
            if not (m.group(1) or m.group(2) or m.group(3) or m.group(4)):
                continue
            if (m.group(7) or m.group(8)) and not m.group(3):
                continue
            sec = m.group(1) or m.group(3) or section
            if sec is None:
                continue
            q = int(m.group(4)) if m.group(4) else None
            letter = (m.group(5) or m.group(6) or m.group(7) or m.group(8)).lower()
            roman = (m.group(9) or m.group(10) or '')
            roman = roman.lower() or None
            out.append((i, sec, q, letter, roman, tail))
        return out

    def _normalise(self, line, section=None):
        """2014-2017 print the same address four other ways; each is put in the
        2018-2020 form before HEAD reads it:
            "1 A 1 a) ..."  the UNIT number before the section letter (dropped)
            "1 1 a) ..."    the unit and question number, no section letter
                            (2017 Ordinary Section A: the section is the one
                            the page is in)
            "1 A2 b) ..."   the question number welded to the section (spaced)
            "A 1 a i) ..."  the part letter bare and the roman bracketed
                            (read as "A 1 a) i.")"""
        if self.year > 2017:
            return line
        if self.year <= 2012:
            # 2010-2012 also print "1 1b)" (part letter welded to the
            # question), "2 a)" (Section A's question with no unit or
            # section), and "B a)i" / "2 a)ii" (a roman with no full stop)
            line = re.sub(r'^([123]\s+\d)([a-h]\))', r'\1 \2', line)
            line = re.sub(r'^((?:[123]\s+)?[A-J])([a-h]\))', r'\1 \2', line)      # "3 Fb)i"
            if section and section != 'A':
                # 2011 Ordinary prints Section I's (b) as "1 1 b)", Section A's
                # numbering; outside Section A no question number is printed
                line = re.sub(r'^[123]\s+\d\s+(?=[a-h]\))', f'{section} ', line)
            if section == 'A':
                line = re.sub(r'^(\d)\s+(?=[a-h]\))', r'A \1 ', line)
            line = re.sub(r'^((?:[123]\s+)?(?:[A-J]\s+)?(?:\d\s+)?[a-h]\))\s*(i{1,3}|iv|v)(?=\s)', r'\1 \2.', line)
        if section:
            line = re.sub(r'^[123]\s+(\d)\s+(?=[a-h]\))', rf'{section} \1 ', line)
        line = re.sub(r'^((?:Or\s+)?)[123]\s+(?=[A-J]\s?\d?\s*\(?[a-h][\s)])', r'\1', line)
        line = re.sub(r'^((?:Or\s+)?[A-J])(\d)\s', r'\1 \2 ', line)
        line = re.sub(r'^((?:Or\s+)?[A-J](?:\s\d)?\s)([a-h])\s+(i{1,3}|iv|v)\)', r'\1\2) \3.', line)
        return line

    def _text_head(self, m):
        """2018-2020 print the question text on the head line itself ("A 1 a)
        i. How do I decide ..."), so a text tail is allowed there -- and only
        on a marker naming its own section letter with a ")"-closed part
        letter, the full printed address. The band grids of those years open
        their rows with bullets, never with a marker."""
        return self.year <= 2020 and bool(m.group(3)) and bool(m.group(6))

    def _read(self):
        heads = self._heads()
        stem_tariff = None
        for n, (i, sec, q, letter, roman, tail) in enumerate(heads):
            end = heads[n + 1][0] if n + 1 < len(heads) else len(self.lines)
            block = self.lines[i + 1:end]
            nxt = heads[n + 1] if n + 1 < len(heads) else None
            # a part head that carries only the stem its romans share (or
            # repeats a roman's stem before the roman's own line, 2015
            # Ordinary H(b)(ii)); a tariff printed on it is its first roman's
            # (2014 Higher G(a): "... using the following headings: 20M")
            if nxt is not None and nxt[1:4] == (sec, q, letter) and nxt[4] and roman in (None, nxt[4]) \
                    and not any(LEAD.match(l) or MC_HEADING.match(l) for l in block):
                m = TRAILING_TARIFF.search(tail or '')
                stem_tariff = m.group(1) if m and roman is None else None
                continue
            ask = self._parse_block(sec, q, letter, roman, tail, block, i, stem_tariff)
            stem_tariff = None
            if isinstance(ask, str):
                self.refused.append((sec, q, letter, roman, i, ask))
            else:
                self.asks.append(ask)

    def _parse_block(self, sec, q, letter, roman, tail, block, line_no, stem_tariff=None):
        # Where the answer starts: the lead-in paragraph, or failing that the
        # "Marking Criteria" heading. 2023 Ordinary Section G(c) prints the
        # lead-in and the bullets with NO heading above them, so anchoring on
        # the heading alone loses a whole ask.
        lead_at = next((j for j, l in enumerate(block) if LEAD.match(l)), None)
        mc_at = next((j for j, l in enumerate(block) if MC_HEADING.match(l)), None)
        if lead_at is None and mc_at is None:
            return 'no marking criteria in this block'
        start = lead_at if lead_at is not None else mc_at + 1

        # The cue: what the scheme reprints of the question, above the answer.
        # Used to PAIR this ask with the paper's (align.py's argument), never
        # to write a card — the paper's own wording is what a student read.
        cue_lines = [l for l in block[:start]
                     if l and not PAGE.match(l) and not MC_HEADING.match(l)]
        if tail and parse_tariff(tail) is None:
            cue_lines = [tail] + cue_lines      # 2018-2020: the text starts on the head line
        cue = ' '.join(' '.join(cue_lines).split())

        total = notation = None
        if tail:
            parsed = parse_tariff(tail)
            if parsed:
                total, notation = parsed
            elif self.year <= 2017:
                # 2014 sets the tariff at the right end of the HEAD line, the
                # question running on below it: "1 A 1 a) Profile how ... in
                # two of the 40M" / "following: ..."
                m = TRAILING_TARIFF.search(tail)
                if m and parse_tariff(m.group(1).split('/')[0]):
                    total, notation = parse_tariff(m.group(1).split('/')[0])[0], m.group(1).strip()
                    cue_lines[0] = tail[:m.start()].strip()
                    cue = ' '.join(' '.join(cue_lines).split())
        if total is None and self.year <= 2017:
            # 2014-2017 set the tariff at the right margin of whichever line
            # it shares (2014 Ordinary D(c): "Discuss this statement ... 40M" /
            # "a person's moral decision-making."): one line of the cue, and
            # only one, may end with it
            if self.year <= 2012:
                # 2010-2012 print the part's marks as a bare number at the right
                # margin with "Graded" beneath it: "... nature of reality. 40" /
                # "Graded". "Graded" is the scheme's word, never the question's.
                cue_lines = [re.sub(r'\s*\bGraded\b\s*', ' ', l).strip() for l in cue_lines]
                cue_lines = [l for l in cue_lines if l]
            def margin(line):
                m = TRAILING_TARIFF.search(line)
                if m and parse_tariff(m.group(1).split('/')[0]):
                    return m, parse_tariff(m.group(1).split('/')[0])[0], m.group(1).strip()
                m = BARE_MARGIN.search(line) if self.year <= 2012 else None
                if m:
                    return m, int(m.group(1)), m.group(1)
                return None
            ends = [(j, hit) for j, l in enumerate(cue_lines) for hit in [margin(l)] if hit]
            # 2010-2012 stack the part's marks and their split down the margin:
            # "40" / "(20Mx2)" / "Graded" -- one tariff printed twice
            if (self.year <= 2012 and len(ends) == 2 and ends[1][0] == ends[0][0] + 1
                    and ends[0][1][2].isdigit() and ends[0][1][1] == ends[1][1][1]):
                (j0, (m0, total, n0)), (j1, (m1, _t, n1)) = ends
                cue_lines[j1] = cue_lines[j1][:m1.start()].strip()
                ends = [(j0, (m0, total, f'{n0} {n1}'))]
            if len(ends) == 1:
                j, (m, total, notation) = ends[0]
                cue_lines[j] = cue_lines[j][:m.start()].strip()
                cue = ' '.join(' '.join(cue_lines).split())
            elif not ends and stem_tariff and parse_tariff(stem_tariff.split('/')[0]):
                total, notation = parse_tariff(stem_tariff.split('/')[0])[0], stem_tariff.strip()
        if total is None:
            # 2021 and 2022 print the tariff at the end of the question text.
            m = TRAILING_TARIFF.search(cue)
            if m:
                # "40M/20Mx2" is one tariff written two ways; take the total.
                first = m.group(1).split('/')[0]
                parsed = parse_tariff(first)
                if parsed:
                    total, notation = parsed[0], m.group(1).strip()
                    cue = cue[:m.start()].strip()
        if total is None:
            return 'no printed tariff'

        points, notes = [], []
        open_list = False
        cur = None
        body = []
        for line in block[start:]:
            if not line or PAGE.match(line):
                continue
            if CODE_LINE.match(line) or GRID_HEAD.search(line) or GRID_ROW.search(line):
                break                       # the band grid — discard it whole
            body.append(line)
        # The examiner's note closes the list. Everything from it to the grid
        # is the note and its wrapped continuation — "Note: Allow implicit
        # reference to religious belief in a rite marking a key moment in life
        # for / members of two religions as listed in the question." Treating
        # only the "Note:" LINE as the note left the continuation looking like
        # part of the last marking point, and welded "members of two religions
        # as listed in the question." onto the end of an answer about the
        # Aqiqah ceremony — which the provenance gate then refused, correctly.
        note_at = next((j for j, l in enumerate(body) if NOTE.match(l)), None)
        if note_at is not None:
            notes = [' '.join(' '.join(body[note_at:]).split())]
            body = body[:note_at]
        for line in body:
            if LEAD.match(line):
                cur = None                  # the lead-in, kept separately
                continue
            if BULLET.match(line):
                if ETC_ONLY.match(line):
                    open_list = True        # the scheme's own "and so on"
                    cur = None
                    continue
                cur = [BULLET.sub('', line).strip()]
                points.append(cur)
                continue
            if cur is not None:
                cur.append(line)
        if not points:
            # The unbulleted variant. Everything between the lead-in and the
            # grid has to open with a named subject and a dash, or the split
            # is not something the scheme printed.
            rest = [l for l in body if not LEAD.match(l)]
            rest = rest[_lead_span(rest):]
            starts = [j for j, l in enumerate(rest) if NAMED_POINT.match(l)]
            if starts and starts[0] == 0:
                for a, b in zip(starts, starts[1:] + [len(rest)]):
                    points.append(rest[a:b])

        # The lead-in: the examiner's statement of what an excellent answer
        # has to SHOW, which is the requirement the bullets are examples of.
        # It ships as the first row's contextNote — verbatim, from the scheme.
        lead = ''
        if lead_at is not None:
            first_point = points[0][0] if points else None
            lead_lines = []
            for line in block[lead_at:]:
                if BULLET.match(line) or CODE_LINE.match(line) \
                        or GRID_HEAD.search(line) or GRID_ROW.search(line) \
                        or NOTE.match(line) or line == first_point \
                        or (self.year <= 2017 and POSSIBLE.match(line)):
                    break
                if line and not PAGE.match(line):
                    lead_lines.append(line)
            lead = ' '.join(' '.join(lead_lines).split())

        joined = [' '.join(' '.join(p).split()) for p in points]
        # A bullet that is only the scheme's escape hatch, however it is
        # spelled ("Etc.", "etc."), is not an answer.
        joined = [p for p in joined if not re.fullmatch(r'Etc\.?', p, re.I)]
        if not joined and not (self.year <= 2020 and lead):
            # 2018-2020 often print the criteria alone, with no points of
            # reference under them: the card then carries the criteria only.
            return 'no marking points under the criteria heading'
        return Ask(section=sec, q=q, letter=letter, roman=roman,
                   total=total, notation=notation, cue=cue, lead=lead,
                   points=joined, open_list=open_list, notes=notes,
                   line=line_no)

    # -- lookups ------------------------------------------------------------
    def by_key(self):
        out = {}
        for a in self.asks:
            out.setdefault(a.key, []).append(a)
        return out

    def ref(self, ask):
        head = f'{self.year} {self.level.upper()} Section {ask.section} Q'
        if ask.q is not None:
            head += str(ask.q)
        if ask.letter:
            head += f'({ask.letter})'
        if ask.roman:
            head += f'({ask.roman})'
        return head


def audit():
    """Every scheme, with the two assertions that matter.

    1. No shipped marking point contains band-grid vocabulary. The grid is
       the one thing in this document that looks like content and is not.
    2. Every ask carries a tariff that was PRINTED, and the sum of the asks
       agrees with the number of 'Marking Criteria' blocks the file holds.
    """
    bad = 0
    for path in sorted(glob.glob(os.path.join(schemes_dir(), '*.md'))):
        stem = os.path.basename(path)[:-3]
        year, level = int(stem[:4]), stem[5:]
        S = ReScheme(year, level)
        blocks = sum(1 for l in S.lines if MC_HEADING.match(l))
        grid = [(S.ref(a), p) for a in S.asks for p in a.points
                if GRID_WORDS.search(p)]
        points = sum(len(a.points) for a in S.asks)
        print(f'{stem}: {len(S.asks)} asks ({blocks} criteria blocks), '
              f'{points} points, {len(S.refused)} refused, '
              f'{len(grid)} band-grid leak(s)')
        for sec, q, letter, roman, line, why in S.refused:
            print(f'    REFUSED {sec} {q} {letter} {roman} (line {line}): {why}')
        for ref, p in grid[:5]:
            print(f'    GRID LEAK {ref}: {p[:80]!r}')
            bad += 1
    return 1 if bad else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('year', nargs='?', type=int)
    ap.add_argument('level', nargs='?')
    ap.add_argument('--audit', action='store_true')
    ap.add_argument('--full', action='store_true')
    args = ap.parse_args()
    if args.audit or not args.year:
        return audit()
    S = ReScheme(args.year, args.level)
    print(f'{args.year} {args.level.upper()}: {len(S.asks)} asks, '
          f'{len(S.refused)} refused')
    for a in S.asks:
        print(f'  {S.ref(a):<30} {a.notation:<14} {a.total:>3}M  '
              f'{len(a.points)} pts{" +etc" if a.open_list else ""}')
        if args.full:
            print(f'      LEAD {a.lead[:150]}')
            for p in a.points:
                print(f'      *    {p[:150]}')
            for note in a.notes:
                print(f'      NOTE {note[:120]}')
    for sec, q, letter, roman, line, why in S.refused:
        print(f'  REFUSED {sec} {q} {letter} {roman} (line {line}): {why}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
