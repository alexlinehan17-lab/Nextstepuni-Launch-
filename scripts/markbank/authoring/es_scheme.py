#!/usr/bin/env python3
"""Spanish marking schemes — the priced answer, read twice over.

    python3 scripts/markbank/authoring/es_scheme.py 2024 hl --full
    python3 scripts/markbank/authoring/es_scheme.py --audit

What this document is
---------------------
A Spanish scheme is four documents stapled together, and only two of them
state answers:

    SECTION A (70 MARKS)                              <- priced answers
      1. (a) Prescribed literature – Relato… (50 marks)
        Q. 1 3 x 3m = 9 marks
        (a) soportar (3m)                             <- the answer, priced
      1. (b) Journalistic Text: EL TRIUNFO… (50 marks)
      2. (a) AND (b) = 20 marks
    SECTION B (100 MARKS)                             <- priced answers
      Q. 4 (2+1) + (2+2+2) + (2+2+2) = 15 marks       <- per-PART tariff
      Section B: Question 5 TOTAL MARKS: 50           <- a BAND GRID
    SECTION C TOTAL MARKS: 50                         <- BAND GRIDS
    LISTENING COMPREHENSION (80 MARKS)                <- priced, but the ask
                                                         needs the recording

Unlike French, the scheme NEVER reprints the question. What both documents
print is the address (section, question number, part letter), the question's
TITLE, and the tariff — so that is what the paper is joined on, and every join
is checked against all three (Law 4: join on whatever BOTH documents print).

TWO INDEPENDENT TARIFFS, AND THE ONE THAT WINS
----------------------------------------------
A question head prices its own parts:

    Q. 4 (2+1) + (2+2+2) + (2+2+2) = 15 marks

Three top-level groups for three lettered parts, in order: (a) is worth 2+1,
(b) 2+2+2, (c) 2+2+2. Every part ALSO prints its own tariff at the end of its
body — "(2+2+2m)" — and the two must agree. They are read separately and
compared, because each catches a different fault: a part whose body ran into
its neighbour loses its trailing tariff, and a head whose groups were mis-split
disagrees with every part beneath it. Where they disagree the ask is FAULTED
and refused, never priced at the more convenient of the two.

The head's groups map to parts only when the counts match. Higher Section A's
Q.3 prints "4 + 3 + 3 = 10 marks" with no lettered parts at all: there the
whole head is one ask's ladder — the first correct answer at 4, the next two at
3 — and the scheme says so in its own bracket, "[First correct answer=4m]".

WHAT A SLASH MEANS, AND WHEN IT STOPS MEANING IT
------------------------------------------------
The scheme's own explanatory page says "A forward slash / before an answer
indicates that the answer is synonymous with that which preceded it… Answers
separated by a forward slash cannot therefore be taken as different answers. A
dash - before an answer indicates that the answer is a separate answer."

Its own answers break that rule the moment it prints a quota: "Two of:
delfines/estrellas de mar/tortugas marinas (3+3m)" asks for two DIFFERENT
animals from three, and reading the slash as the scheme's page describes it
would offer a student one answer where the SEC accepts two. So the quota
decides: under "Two of:", "Three of:" or "One of:" the separators are options;
with no quota printed, a slash is a synonym inside one answer and the answer is
one row.

The dash itself is four different characters across the five years — a plain
hyphen, U+2010, U+2011 and an en dash — which is the second reason it cannot be
the test on its own.
"""
import argparse
import glob
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))

SUBJECT = 'spanish'


def schemes_dir(subject=SUBJECT):
    return os.path.join(ROOT, 'examiner-reports', subject, 'schemes')


# ------------------------------------------------------------- the units ----
# The examination's own sections. Spelled in CAPITALS on purpose: the scheme
# also prints "Section B: Question 5 TOTAL MARKS: 50" in mixed case as a
# sub-head INSIDE Section B, and a case-insensitive match there closes Section
# B four lines before its last priced ask.
UNIT = re.compile(r'^SECTION\s+([ABC])\b')
UNIT_L = re.compile(r'^LISTENING\s+COMPREHENSION\b', re.I)
# Everything from here is the Modified Marking Scheme and the scheme's own
# contents index, which reprints "Section A", "Section B" and "Section C" as
# plain lines. Reading past it re-opens a unit that has already been read.
APPENDIX = re.compile(r'^APPENDIX\b', re.I)

# Higher Section A's two alternatives, and its second question.
#   1. (a) Prescribed literature – Relato de un náufrago (50 marks)
#   1. (b) Journalistic Text: EL TRIUNFO DE LA MÚSICA EN ESPAÑOL (50 marks)
#   2. (a) AND (b) = 20 marks     /  2. (a) OR (b) =10 marks
CHOICE_HEAD = re.compile(
    r'^1\s*\.\s*\(\s*([ab])\s*\)\s*(.*?)\s*\((\d{1,3})\s*marks?\)\s*$', re.I)
Q2_HEAD = re.compile(r'^2\s*\.\s*\(\s*a\s*\)\s*(?:AND|OR)\s*\(\s*b\s*\)\s*=?\s*'
                     r'(\d{1,3})\s*marks?\s*$', re.I)
# Inside Question 2, each alternative is a titled 10-mark text.
#   (a) LA ABEJA ES DECLARADA EL SER VIVO MÁS IMPORTANTE DEL PLANETA (10 marks)
Q2_LETTER = re.compile(
    r'^\(\s*([ab])\s*\)\s*(.*?)\s*\((\d{1,3})\s*marks?\)\s*$', re.I)

# A question head inside Higher Section A or B.
#   Q. 1 3 × 3m = 9 marks        Q.4 (6 marks)
#   Q. 4 (2+1) + (2+2+2) + (2+2+2) = 15 marks
HL_Q_HEAD = re.compile(r'^Q\s*\.?\s*(\d)\s+(.*?)\s*$')
# An Ordinary Section A head: the question number, the text's own TITLE and the
# tariff. The title is what the paper prints above the text, and is the second
# thing the two documents share.
OL_Q_HEAD = re.compile(
    r'^Question\s+(\d)\s*\.\s*(.*?)\s*\((\d{1,3})\s*marks?\)\s*$', re.I)
# The listening test heads each item by number and title, with the tariff on
# the line beneath. Read for the exclusion evidence only.
L_HEAD = re.compile(r'^(\d)\s*\.\s*(?:(?:Anuncio|Di[áa]logo|Descriptivo|'
                    r'El Tiempo|Una Noticia)\s*[-–—]\s*)?(.+?)\s*$', re.I)

# A part of a question: "(a) …", "(i) …". Roman numerals only appear under
# Higher Section A Question 2, where the paper prints (i), (ii), (iii).
PART = re.compile(r'^\(\s*(i{1,3}|iv|v|[a-h])\s*\)\s*(.*)$', re.I)

# The tariff a part prints at the END of its own body: "(5m)", "(4+3+3m)",
# "(2+2+2 marks)", "(3+3m)".
PART_TARIFF = re.compile(
    r'\((\d{1,2}(?:\s*\+\s*\d{1,2})*)\s*(?:m|marks?)\s*\)\s*$', re.I)
# The same shape read anywhere in a line, used only to strip an inline
# sub-tariff off an answer's text once the part tariff is already known.
INLINE_TARIFF = re.compile(r'\s*\((\d{1,2}(?:\s*\+\s*\d{1,2})*)\s*(?:m|marks?)\s*\)', re.I)

# A question head's own decomposition. Two notations:
#   3 × 3m = 9 marks        n answers at m each
#   (2+1) + (2+2+2) = …     one bracketed group per lettered part
TIMES = re.compile(r'^(\d{1,2})\s*[x×]\s*(\d{1,2})\s*(?:m|marks?)?\s*=\s*'
                   r'(\d{1,3})\s*marks?\s*$', re.I)
SUM = re.compile(r'^(.+?)\s*=\s*(\d{1,3})\s*marks?\s*$', re.I)
BARE_TOTAL = re.compile(r'^\((\d{1,3})\s*marks?\)\s*$', re.I)

# A quota: the scheme's own statement of how many of the listed answers a
# candidate must give. "Any three of:" and "Three of:" are the same thing.
QUOTA = re.compile(r'^(?:Any\s+)?(one|two|three|four|five)\s+of\s*:?\s*(.*)$', re.I)
QUOTA_WORDS = {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5}
# A question numbered from (i) is numbered in ROMANS; one numbered from (a) is
# numbered in letters, and its ninth part is the letter i.
ROMANS = ('i', 'ii', 'iii', 'iv', 'v')

# Every character the five years use to open a separate answer. The plain
# hyphen is LAST: written between two characters inside a class it would be a
# RANGE, and the range that swallowed U+2013 to U+2043 in the French reader
# left the ASCII hyphen — the commonest of the four here — outside the class.
DASH = '‐‑‒–—−●•-'
# What opens a separate answer: one of the four dashes, or the scheme's own
# "(1)" numbering, which 2021 Ordinary uses where the other years use dashes.
ANSWER_START = re.compile(rf'^(?:[{DASH}]\s*|\(\s*\d{{1,2}}\s*\)\s+)')

# An examiner instruction or a part-credit line, which the scheme prints in
# square brackets: "[First correct answer=4m]", "[No marks awarded if extra
# words are added]", "[It makes Spain unique/welcoming=2m]". They are kept and
# disclosed on the card, and never read as an answer. The brackets are the
# scheme's own convention -- its explanatory page says "Square brackets [ ] show
# a breakdown of marks within the question or give further clarifications" --
# so a bracket is never part of an answer, wherever on the line it falls.
BRACKET_OPEN = re.compile(r'\[')
INLINE_BRACKET = re.compile(r'\[[^\]]*\]')

# The instruction the Ordinary scheme prints BETWEEN two questions, inside the
# block that belongs to the question above it: "Questions 2, 3, 4. [ONE
# Question to be answered...]". Read as an answer it welded the whole rubric
# onto 2021 Ordinary Q1(h)'s last option and took that part's tariff with it.
BETWEEN_QUESTIONS = re.compile(r'^Questions?\s+\d[\d,\s]*(?:and\s*\d\s*)?\.', re.I)
# A standing instruction that applies to the whole question rather than to one
# answer, printed between the head and its first part.
HEAD_NOTE = re.compile(r'^\[|^All answers must be|^Language manipulation|'
                       r'^If \(a\)|^Note\s*:|^N\.?B\.?\b', re.I)
PAGE = re.compile(r'^(?:##\s*Page\s*\d+\s*$|\d{1,3}\s*$)')
# The line the scheme closes a listening test with: "9+12+13+13+13+8+12 = 80
# marks". It is arithmetic, not an answer.
CHECKSUM_LINE = re.compile(r'^[\d\s+]+=\s*\d{1,3}\s*marks?\s*$', re.I)

# The scheme's own statement of the language rule, quoted onto every card.
LANGUAGE_RULE = re.compile(
    r'^Questions must be answered in the language indicated', re.I)

# Section B's linked opinion question and Section C's written production: band
# grids, read here so the refusal they earn is counted rather than assumed.
GRID_B5 = re.compile(r'^Section\s+B\s*:\s*Question\s+5\b', re.I)
GRID_C = re.compile(r'^Question\s+([12])\s*\.?\s*\(?\s*([ab])\s*\)?\s+'
                    r'(DIALOGUE CONSTRUCTION|LETTER\s*/\s*EMAIL|DIARY ENTRY|NOTE)\b',
                    re.I)
GRID_OL_B1 = re.compile(r'^Q\s*\.?\s*1\s*\.\s*LETTER\s*:', re.I)
GRID_OL_B2 = re.compile(r'^Q\s*\.?\s*2\s*\.\s*\(\s*a\s*\)\s*NOTE\b', re.I)

# SEC misprints, keyed by the sitting and never repaired by a heuristic.
MISPRINTS = {
    # The 2021 Higher scheme heads its literature alternative "Prescribed
    # literatura" — the English noun replaced by its Spanish cognate. The same
    # head is spelled "Prescribed literature" in the other four Higher schemes
    # and on the paper itself. Nothing downstream reads the word, but the head
    # is one of the three things the paper is joined on, so it is repaired here
    # where the repair is visible rather than tolerated by a loose pattern.
    (2021, 'hl'): [('Prescribed literatura:', 'Prescribed literature:')],
}


def _split_notes(body):
    """(answer lines, note lines) for one part's printed block.

    The scheme's square brackets can open on one line and close two lines
    later — 2022 Higher's listening Q5(c) prints a three-line part-credit
    bracket — so the state is carried across lines rather than tested per line.
    A bracket that never closes runs to the end of the part, which is what the
    SEC prints.
    """
    kept, notes = [], []
    depth = 0
    for raw in body:
        s = ' '.join((raw or '').split())
        if not s or PAGE.match(s) or CHECKSUM_LINE.match(s):
            continue
        if BETWEEN_QUESTIONS.match(s):
            break
        if depth:
            notes.append(s.rstrip(']'))
            if ']' in s:
                depth = 0
            continue
        s = INLINE_BRACKET.sub(lambda m: (notes.append(m.group(0).strip('[] ')) or ' '), s)
        s = ' '.join(s.split())
        if BRACKET_OPEN.search(s):
            head, _open, tail = s.partition('[')
            if head.strip():
                kept.append(head.strip())
            notes.append(tail.strip())
            depth = 1
            continue
        if s:
            kept.append(s)
    return kept, notes


def parse_head_tariff(text):
    """(total, [group terms]) for a question head's own decomposition.

    A group is what ONE lettered part is worth: "(2+1) + (2+2+2) + (2+2+2)"
    is three groups. "3 × 3m" is three groups of one term each. Anything the
    two notations do not cover returns (total, None) — the parts are then
    priced from their own printed tariffs alone, and never from a guess.
    """
    raw = ' '.join((text or '').split())
    m = BARE_TOTAL.match(raw)
    if m:
        return int(m.group(1)), None
    m = TIMES.match(raw)
    if m:
        n, per, total = int(m.group(1)), int(m.group(2)), int(m.group(3))
        if n * per != total:
            return total, None
        return total, [[per] for _ in range(n)]
    m = SUM.match(raw)
    if not m:
        return None, None
    total = int(m.group(2))
    body = m.group(1)
    groups = []
    for chunk in re.split(r'\+(?![^(]*\))', body):
        chunk = chunk.strip()
        if not chunk:
            return total, None
        terms = re.findall(r'\d{1,2}', chunk)
        if not terms:
            return total, None
        groups.append([int(t) for t in terms])
    if sum(sum(g) for g in groups) != total:
        return total, None
    return total, groups


def parse_part_tariff(text):
    """([terms], text without the tariff) for one part's printed body."""
    m = PART_TARIFF.search(text)
    if not m:
        return None, text
    terms = [int(t) for t in re.findall(r'\d{1,2}', m.group(1))]
    return terms, text[:m.start()].rstrip()


class Ask:
    """One priced ask, exactly as the scheme states it."""

    __slots__ = ('section', 'q', 'letter', 'roman', 'title', 'terms', 'total',
                 'quota', 'options', 'points', 'notes', 'line', 'fault',
                 'head_notation')

    def __init__(self, **kw):
        for k in self.__slots__:
            setattr(self, k, kw.get(k))

    @property
    def key(self):
        return (self.section, self.q, self.letter, self.roman)

    @property
    def mode(self):
        """'anyN', 'points' or 'none' — what shape of card this ask is."""
        if self.quota:
            return 'anyN'
        if self.points:
            return 'points'
        return 'none'

    def __repr__(self):
        return f'<Ask {self.section} {self.q}{self.letter or ""}{self.roman or ""}>'


class EsScheme:
    """One published Spanish marking scheme, read as a list of asks."""

    def __init__(self, year, level, subject=SUBJECT):
        self.year, self.level, self.subject = year, level, subject
        self.path = os.path.join(schemes_dir(subject), f'{year}-{level}.md')
        with open(self.path, encoding='utf-8') as fh:
            raw = fh.read()
        # The 2025 schemes set every space inside a heading as U+00A0, so
        # "DIALOGUE\u00a0CONSTRUCTION" is not the string "DIALOGUE CONSTRUCTION"
        # any literal in this file spells. Two of that sitting's four Section C
        # band grids were invisible, and a grid nobody sees is an exclusion
        # nobody writes. Folded to ordinary spaces: a whitespace normalisation,
        # never a change of content.
        raw = raw.replace('\u00a0', ' ').replace('\u2009', ' ').replace('\u202f', ' ')
        for old, new in MISPRINTS.get((year, level), ()):
            assert old in raw, f'{year} {level}: misprint {old!r} is not in the scheme'
            raw = raw.replace(old, new)
        self.lines = [l.rstrip() for l in raw.split('\n')]
        self.asks = []
        self.refused = []
        self.unit_totals = {}        # 'A' -> the total the unit prints
        self.q_totals = {}           # (section, q) -> the total the head prints
        self.titles = {}             # (section, q) -> the title the head prints
        self.grids = {}              # key -> the grid line that stands for it
        self.language_rule = None
        self.unit_rules = {}         # unit -> the language rule it prints
        self._read()

    # -- segmentation -------------------------------------------------------
    def _units(self):
        """[(first line, last line, unit letter)] for A, B, C and L."""
        marks = []
        for i, line in enumerate(self.lines):
            if APPENDIX.match(line):
                marks.append((i, None))
                break
            m = UNIT.match(line)
            if m:
                marks.append((i, m.group(1)))
                continue
            if UNIT_L.match(line):
                marks.append((i, 'L'))
        out = []
        for n, (i, unit) in enumerate(marks):
            if unit is None:
                continue
            end = marks[n + 1][0] if n + 1 < len(marks) else len(self.lines)
            out.append((i, end, unit))
        return out

    def _read(self):
        for line in self.lines:
            if LANGUAGE_RULE.match(line):
                self.language_rule = ' '.join(line.split())
                break
        for start, end, unit in self._units():
            head = self.lines[start]
            m = re.search(r'(\d{1,3})\s*MARKS', head, re.I)
            if m:
                self.unit_totals[unit] = int(m.group(1))
            block = self.lines[start + 1:end]
            self._read_rule(unit, block)
            if unit == 'A':
                if self.level == 'hl':
                    self._read_hl_a(block, start + 1)
                else:
                    self._read_ol_a(block, start + 1)
            elif unit == 'B':
                if self.level == 'hl':
                    self._read_hl_b(block, start + 1)
                else:
                    self._read_ol_b(block, start + 1)
            elif unit == 'C':
                self._read_grids_c(block, start + 1)
            else:
                self._read_listening(block, start + 1)

    def _read_rule(self, unit, block):
        """The language rule this unit prints, verbatim.

        Every unit reprints it on its own head — "Questions must be answered in
        the language indicated on the examination paper for full marks" — and
        Ordinary follows it with the three penalties it applies. It rides on
        every card in that unit, because a card that does not say which
        language is wanted marks a right answer wrong.
        """
        out = []
        for line in block[:14]:
            s = ' '.join(line.split())
            if not out:
                if LANGUAGE_RULE.match(s):
                    out.append(s)
                continue
            if s.startswith('•') or out[-1].endswith((':', ',')) or \
                    re.match(r'^(?:In Section|vice versa|language|50%|per the)', s):
                out.append(s.lstrip('• ').strip())
                continue
            break
        if out:
            self.unit_rules[unit] = ' '.join(' '.join(out).split())

    # -- Higher Section A ---------------------------------------------------
    def _read_hl_a(self, block, offset):
        """Question 1's two alternatives and Question 2's two texts."""
        spans = []                        # (section token, first, last)
        for i, line in enumerate(block):
            m = CHOICE_HEAD.match(line.strip())
            if m:
                spans.append((f'A1{m.group(1).lower()}', i, m.group(2),
                              int(m.group(3))))
                continue
            m = Q2_HEAD.match(line.strip())
            if m:
                spans.append(('A2', i, None, int(m.group(1))))
        for n, (section, i, title, total) in enumerate(spans):
            end = spans[n + 1][1] if n + 1 < len(spans) else len(block)
            if title is not None:
                self.titles[(section, None)] = _clean_title(title)
            self.unit_totals.setdefault(section, total)
            if section == 'A2':
                self._read_q2(block[i + 1:end], offset + i + 1)
            else:
                self._read_hl_questions(section, block[i + 1:end], offset + i + 1)

    def _read_q2(self, block, offset):
        """Higher Section A Question 2: two titled texts, each with (i)-(iii)."""
        heads = [(i, m) for i, m in
                 ((i, Q2_LETTER.match(l.strip())) for i, l in enumerate(block)) if m]
        for n, (i, m) in enumerate(heads):
            end = heads[n + 1][0] if n + 1 < len(heads) else len(block)
            letter = m.group(1).lower()
            self.titles[('A2', letter)] = _clean_title(m.group(2))
            self.q_totals[('A2', letter)] = int(m.group(3))
            self._read_parts('A2', None, letter, None,
                             block[i + 1:end], offset + i + 1, int(m.group(3)))

    def _read_hl_questions(self, section, block, offset):
        """"Q. 1 3 × 3m = 9 marks" and the parts beneath it."""
        heads = [(i, m) for i, m in
                 ((i, HL_Q_HEAD.match(l.strip())) for i, l in enumerate(block)) if m]
        for n, (i, m) in enumerate(heads):
            end = heads[n + 1][0] if n + 1 < len(heads) else len(block)
            q = int(m.group(1))
            total, groups = parse_head_tariff(m.group(2))
            if total is not None:
                self.q_totals[(section, q)] = total
            self._read_parts(section, q, None, None, block[i + 1:end],
                             offset + i + 1, total, groups, m.group(2))

    # -- Higher Section B ---------------------------------------------------
    def _read_hl_b(self, block, offset):
        """Section B's four priced questions, and the band grid that is Q5."""
        stop = len(block)
        for i, line in enumerate(block):
            if GRID_B5.match(line.strip()):
                stop = i
                self.grids[('B', 5, None, None)] = ' '.join(line.split())
                break
        # The text's own TITLE is printed on its own line above Q.1, exactly as
        # the paper prints it above the loose sheet's article.
        for line in block[:stop]:
            s = line.strip()
            if s and not PAGE.match(s) and not HEAD_NOTE.match(s) \
                    and not HL_Q_HEAD.match(s) and not LANGUAGE_RULE.match(s):
                self.titles[('B', None)] = _clean_title(s)
                break
        self._read_hl_questions('B', block[:stop], offset)

    def _read_grids_c(self, block, offset):
        for line in block:
            m = GRID_C.match(line.strip())
            if m:
                key = ('C', int(m.group(1)), m.group(2).lower(), None)
                self.grids.setdefault(key, ' '.join(line.split()))

    # -- Ordinary -----------------------------------------------------------
    def _read_ol_a(self, block, offset):
        heads = [(i, m) for i, m in
                 ((i, OL_Q_HEAD.match(l.strip())) for i, l in enumerate(block)) if m]
        for n, (i, m) in enumerate(heads):
            end = heads[n + 1][0] if n + 1 < len(heads) else len(block)
            q = int(m.group(1))
            self.titles[('A', q)] = _clean_title(m.group(2))
            self.q_totals[('A', q)] = int(m.group(3))
            self._read_parts('A', q, None, None, block[i + 1:end],
                             offset + i + 1, int(m.group(3)))

    def _read_ol_b(self, block, offset):
        for line in block:
            s = line.strip()
            if GRID_OL_B1.match(s):
                self.grids.setdefault(('B', 1, None, None), ' '.join(s.split()))
            elif GRID_OL_B2.match(s):
                # One line heads both alternatives: "Q.2. (a) NOTE Q.2. (b)
                # DIARY ENTRY (20 marks)", and the scheme says beneath it
                # "Identical allocation in each case."
                for letter in ('a', 'b'):
                    self.grids.setdefault(('B', 2, letter, None), ' '.join(s.split()))

    # -- the listening test -------------------------------------------------
    def _read_listening(self, block, offset):
        heads = []
        for i, line in enumerate(block):
            s = line.strip()
            if not s or PAGE.match(s) or CHECKSUM_LINE.match(s):
                continue
            m = L_HEAD.match(s)
            if m and 1 <= int(m.group(1)) <= 9 and not PART.match(s):
                heads.append((i, int(m.group(1)), _clean_title(m.group(2))))
        for n, (i, q, title) in enumerate(heads):
            end = heads[n + 1][0] if n + 1 < len(heads) else len(block)
            self.titles[('L', q)] = title
            body = block[i + 1:end]
            total = None
            for line in body:
                _t, groups = parse_head_tariff(line.strip())
                if _t is not None:
                    total = _t
                    break
            if total is not None:
                self.q_totals[('L', q)] = total
            self._read_parts('L', q, None, None, body, offset + i + 1, total)

    # -- one question's parts -----------------------------------------------
    def _read_parts(self, section, q, letter0, roman0, block, offset,
                    total=None, groups=None, notation=None):
        """Cut a question's block at its part markers and price each part.

        `letter0` is set where the question itself IS a letter (Higher Section
        A Question 2, whose (a) and (b) are two separate texts): its parts are
        then romans beneath that letter.
        """
        heads = []
        for i, line in enumerate(block):
            s = line.strip()
            if PAGE.match(s):
                continue
            m = PART.match(s)
            if m:
                heads.append((i, m.group(1).lower(), m.group(2)))
        if not heads:
            # A question with no lettered parts is one ask: Higher Section A's
            # Q.3 and Q.4 ("Give three details"), and its Q.4 journalistic
            # ask, which the scheme prices but does not answer.
            ask = self._parse_part(section, q, letter0, roman0,
                                   [l.strip() for l in block], offset,
                                   sum(sum(g) for g in groups) if groups else total,
                                   [t for g in (groups or []) for t in g] or None,
                                   notation)
            if ask is not None:
                self.asks.append(ask)
            return
        # Letters or romans? Decided ONCE for the whole question, from its
        # first printed marker. 2025 Ordinary Question 1 runs (a) to (i): nine
        # lettered parts, whose ninth marker is the letter i and not roman one.
        # Read per token, that part became ('Q1', None, 'i') while the paper
        # printed it under (1, 'i'), and the ask went unbound.
        as_roman = heads[0][1] in ROMANS

        # The head's own decomposition prices the parts only when it has one
        # group per part. Anything else and each part is priced from the tariff
        # printed at the end of its own body.
        per_part = groups if groups and len(groups) == len(heads) else None
        got = []
        for n, (i, tok, rest) in enumerate(heads):
            end = heads[n + 1][0] if n + 1 < len(heads) else len(block)
            body = [rest] + [l.strip() for l in block[i + 1:end]]
            terms = per_part[n] if per_part else None
            if letter0 is not None:
                letter, roman = letter0, tok
            elif as_roman:
                letter, roman = None, tok
            else:
                letter, roman = tok, None
            ask = self._parse_part(section, q, letter, roman, body,
                                   offset + i, sum(terms) if terms else None,
                                   terms, notation)
            if ask is not None:
                got.append(ask)
        # The SEC's own arithmetic: the parts must add up to the total the head
        # prints. Where they do not, every part of that question is faulted —
        # a disagreement means a part may have been lost, and neither half of
        # the tariff can be trusted then.
        if total is not None and got:
            summed = sum(a.total for a in got if a.total is not None)
            if summed != total or any(a.total is None for a in got):
                for a in got:
                    a.fault = a.fault or (
                        f'the head prices this question {total} while its parts '
                        f'price {summed}; the value this part is really worth is '
                        f'not printed')
        self.asks.extend(got)

    def _parse_part(self, section, q, letter, roman, body, line, total,
                    terms, notation):
        """One part, read into its answers, its quota and its notes."""
        kept, notes = _split_notes(body)
        if not kept and total is None:
            return None

        # The part's own printed tariff. Read from every line, because the SEC
        # prices a part in two different places: once at the END of the whole
        # part, and — where the part lists several REQUIRED answers — once on
        # each answer's own line. 2024 Higher Section B Q.4(a) prints
        # "- It was too costly … (2m)" and "- those made in Argentina broke
        # (easily) (1m)", which is 3 marks split 2 and 1, not a 1-mark part.
        line_terms = []
        stripped = []
        for s_ in kept:
            t, rest = parse_part_tariff(s_)
            line_terms.append(t)
            stripped.append(rest.strip())
        answer_at = [i for i, s_ in enumerate(kept) if ANSWER_START.match(s_)]
        own_terms = None
        per_answer = None
        if (len(answer_at) >= 2
                and all(line_terms[i] and len(line_terms[i]) == 1 for i in answer_at)):
            own_terms = [line_terms[i][0] for i in answer_at]
            per_answer = True
            kept = stripped
        else:
            last = max((i for i, t in enumerate(line_terms) if t), default=None)
            if last is not None:
                own_terms = line_terms[last]
                # Everything printed AFTER a part's price is examiner guidance
                # for that part, not another answer: 2025 Higher Section A
                # Q2(b)(iii) closes with "If only answering:" and a part-credit
                # line, and reading the price off the LAST line alone left that
                # ask unpriced and faulted the whole question.
                notes.extend(k for k in kept[last + 1:] if k)
                kept = [k for k in stripped[:last + 1] if k]
            else:
                kept = [k for k in stripped if k]

        fault = None
        if terms is None:
            terms = own_terms
        elif own_terms is not None and sum(own_terms) != sum(terms):
            fault = (f'the question head prices this part {"+".join(map(str, terms))} '
                     f'and the part itself {"+".join(map(str, own_terms))}')
        # The two agree on what the part is worth but not on how it is split —
        # Higher Q.5 heads itself "4 + 4 + 4 = 12 marks" and closes the ask
        # "(12m)". The head's split is the finer of the two and is what the
        # examiner pays by, so it is kept; the disagreement is not a fault,
        # because the number that could be wrong on a card is the total.
        if terms is not None:
            total = sum(terms)

        quota = None
        rest = []
        for s_ in kept:
            m = QUOTA.match(s_)
            if m:
                quota = QUOTA_WORDS[m.group(1).lower()]
                tail = m.group(2).strip()
                if tail:
                    rest.append(tail)
                continue
            rest.append(s_)

        # An answer opens with a dash or with the scheme's own "(1)" numbering;
        # a line carrying neither is the wrapped continuation of the line above
        # it, and welding it to the NEXT answer instead is how one answer ends
        # up carrying the opening clause of another.
        answers = []
        marked = 0
        for s_ in rest:
            if ANSWER_START.match(s_):
                answers.append(ANSWER_START.sub('', s_).strip())
                marked += 1
            elif answers:
                answers[-1] = ' '.join(f'{answers[-1]} {s_}'.split())
            else:
                answers.append(s_)
        answers = [INLINE_TARIFF.sub('', a).strip() for a in answers]
        answers = [a for a in answers if a]

        options, points = [], []
        if quota:
            options = answers
            if len(options) < quota:
                # One dash opening a list whose members are separated by
                # slashes: 2022 Ordinary listening Q1(c) prints "Three of: -
                # English / Spanish / French /German (2+2+2m)". The quota is
                # the scheme's own count of how many distinct answers it has
                # stated, so it is what decides that the slashes are separators
                # here and synonyms everywhere a quota is absent.
                joined = ' '.join(' '.join(answers).split())
                split = [o.strip() for o in joined.split('/') if o.strip()]
                if len(split) >= quota:
                    options = split
            if len(options) < quota:
                fault = fault or (
                    f'the scheme asks for {quota} answers and states {len(options)}')
        elif marked >= 2 and terms and len(terms) == len(answers):
            # Several answers, all required, priced in the order the scheme
            # lists them: "- Fresh ingredients / - Traditional ways of cooking
            # (2+1m)" is two answers at 2 and 1, not one answer worth 3.
            points = list(zip(answers, terms))
        elif answers:
            # One answer, however many marks it is worth. "(5+5m)" on a single
            # printed line is the SEC splitting ONE answer's marks across its
            # two halves, not two answers.
            points = [(' '.join(' '.join(answers).split()), total)]

        return Ask(section=section, q=q, letter=letter, roman=roman,
                   title=self.titles.get((section, q)), terms=terms, total=total,
                   quota=quota, options=options, points=points, notes=notes,
                   line=line, fault=fault, head_notation=notation)

    # -- lookups ------------------------------------------------------------
    def ref(self, ask):
        return ref_for(self.year, self.level, ask.section, ask.q, ask.letter,
                       ask.roman)

    def by_key(self):
        return {a.key: a for a in self.asks}


def _clean_title(text):
    return ' '.join((text or '').replace('–', '-').split()).strip(' :-')


def ref_for(year, level, section, q, letter, roman):
    """The card's citation: the sitting, then the paper's own address."""
    ref = f'{year} {level.upper()} Section {section} Q'
    if q is not None:
        ref += str(q)
    if letter:
        ref += f'({letter})'
    if roman:
        ref += f'({roman})'
    return ref


def audit(subject=SUBJECT):
    """Every scheme, with the checks that would catch a mis-read."""
    bad = 0
    for path in sorted(glob.glob(os.path.join(schemes_dir(subject), '*.md'))):
        stem = os.path.basename(path)[:-3]
        year, level = int(stem[:4]), stem[5:]
        S = EsScheme(year, level, subject)
        priced = [a for a in S.asks if a.section != 'L']
        print(f'{stem}: {len(priced)} priced asks, '
              f'{len([a for a in S.asks if a.section == "L"])} listening asks, '
              f'{len(S.grids)} band grid(s)')
        for unit in ('A', 'B'):
            printed = S.unit_totals.get(unit)
            if printed is None:
                continue
            got = _unit_sum(S, unit)
            note = ''
            if got != printed:
                # 2021 and 2022 Ordinary print five Section A questions worth
                # 160 under a head that says 110, because the paper sets a
                # CHOICE: "Answer Question 1 AND Question 5 and any ONE of
                # Questions 2, 3 OR 4." Every printed question is still an ask
                # the paper prints, so all five are censused; the unit total is
                # what one candidate answers, and the check is whether some
                # subset of the printed questions reaches it.
                note = ('   <-- choice: a subset of the printed questions reaches '
                        'this total' if _reaches(S, unit, printed)
                        else '   <-- MISMATCH')
                if 'MISMATCH' in note:
                    bad += 1
            print(f'    Section {unit}: asks sum {got}, the scheme prints '
                  f'{printed}{note}')
        for a in S.asks:
            if a.fault:
                bad += 1
                print(f'    {S.ref(a)}: {a.fault}')
    return 1 if bad else 0


def _reaches(S, unit, printed):
    """Can some subset of this unit's printed question totals make `printed`?"""
    totals = [t for (sec, q), t in S.q_totals.items()
              if (sec[0] if sec else '') == unit and q is not None]
    reach = {0}
    for t in totals:
        reach |= {r + t for r in reach}
    return printed in reach


def _unit_sum(S, unit):
    """What one unit's priced asks add up to, plus the grids it prints.

    Section B's Question 5 is a 50-mark band grid and Section A's Higher
    Question 1 is a CHOICE between two 50-mark alternatives, so the sum is
    taken over what a candidate actually answers: one alternative, plus every
    grid the unit prints.
    """
    total = 0
    seen = set()
    for a in S.asks:
        if a.section == 'L' or a.total is None:
            continue
        base = 'A' if a.section.startswith('A') else a.section
        if base != unit:
            continue
        # Question 1's alternatives are answered one or the other: count (a).
        if a.section == 'A1b':
            continue
        # Question 2's own alternatives, where the paper prints "(a) OR (b)".
        if a.section == 'A2' and S.unit_totals.get('A2') == 10 and a.letter == 'b':
            continue
        total += a.total
        seen.add(a.key)
    for key, _line in S.grids.items():
        if key[0] != unit:
            continue
        if unit == 'B' and key[1] == 5:
            total += 50
        elif unit == 'C':
            total += 0                    # Section C's grids print their own
        elif unit == 'B' and key[1] in (1, 2) and key[2] in (None, 'a'):
            total += 40 if key[1] == 1 else 20
    return total


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('year', nargs='?', type=int)
    ap.add_argument('level', nargs='?')
    ap.add_argument('--subject', default=SUBJECT)
    ap.add_argument('--audit', action='store_true')
    ap.add_argument('--full', action='store_true')
    args = ap.parse_args()
    if args.audit or not args.year:
        return audit(args.subject)
    S = EsScheme(args.year, args.level, args.subject)
    print(f'{args.year} {args.level.upper()}: {len(S.asks)} asks, '
          f'{len(S.grids)} grid(s); units {S.unit_totals}')
    for a in S.asks:
        print(f'  {S.ref(a):<28} {str(a.terms):<16} {a.mode:<7} '
              f'{"FAULT " + a.fault if a.fault else ""}')
        if args.full:
            for o in a.options:
                print(f'      OPT  {o[:110]}')
            for p, m in (a.points or []):
                print(f'      PT   [{m}] {p[:110]}')
            for n in a.notes:
                print(f'      NOTE {n[:110]}')
    for key, line in sorted(S.grids.items(), key=lambda kv: str(kv[0])):
        print(f'  GRID {key}: {line[:90]}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
