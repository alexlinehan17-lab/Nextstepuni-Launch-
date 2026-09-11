#!/usr/bin/env python3
"""Read one Physical Education marking scheme into parts, tariffs and answers.

    python3 scripts/markbank/authoring/pe_scheme.py 2024 hl        # print parts
    python3 scripts/markbank/authoring/pe_scheme.py 2024 hl --raw  # print lines
    python3 scripts/markbank/authoring/pe_scheme.py --audit        # every sitting

WHY THE BLOCK RENDERING AND NOT THE PDF DIRECTLY.  An earlier reader cut the
scheme out of `pymupdf.get_text('blocks')` itself and spent most of its code
undoing what a TABLE does to that: a welded block was taken whole, so a list
of answers welded into the middle of a criterion was never seen at all, and
2022 reported 15% of its parts as stating an answer when nearly half of them
do.  append-scheme-blocks.py has already appended that same block order to the
scheme markdown in examiner-reports/, and that file is ALSO the text the
build's provenance gate searches — so a marking point lifted from it is
traceable by construction, and every table cell arrives on one line instead of
wrapped across four with the marks column glued into the middle of a sentence.

WHAT THE DOCUMENT LOOKS LIKE.  Each question is a run of two-column tables,
and in block order the Description cell and the Marks cell are separate lines:

    Question 2 (8 marks)
    (a) Define the concept of physical activity, leisure and recreation.
    Description Marks
    Defines the concept of physical activity, leisure and recreation. 2 marks
    Clear and accurate definition. 2
    Some accuracy in the definition. 1
    (b) Discuss two barriers to physical activity participation in the community.
    Description Marks
    Discusses barriers to physical activity participation in the community 6 (2 x 3 marks)
    Detailed discussion of named barrier 3 marks
    Barrier named 1 mark
    Barriers may include:
    -Facilities
    -Access
    -Finance

The Description column states what the examiner must SEE.  Part (a)'s rows
state no answer — "Clear and accurate definition" is a grade, not a definition
— while part (b) ends in the SEC's own list of barriers, which is an answer a
student could have written.  That division is the whole subject, and it is
what `answers` and `band_only()` report.

LAYOUT DRIFT.  Thirteen sittings do not print the same page, and every shape
is read here rather than special-cased anywhere else:

  * 2020-2022 do NOT reprint the ask.  A part opens "(a)" and goes straight
    into "Description Marks"; the evidence a pairing is right has to come
    from the criterion rows, which are the ask rewritten (see pe_lib).
  * 2022 welds a whole question into one block and prints a SUMMARY of its
    parts before the parts themselves — "Description Marks (a) 4 marks
    Definition of sponsorship (b) 4 marks Definition of merchandising" — so a
    block is cut at the markers inside it and one address opens twice, the
    two openings being ONE part, merged in printed order.
  * 2023 onward reprints the ask, sometimes above the table and sometimes
    inside it under the "Description Marks" heading.
  * 2025 Ordinary addresses Section C parts with the question number in
    front — "14 (b) (ii) Give a reason why..." — and 2024 Ordinary refers
    back to a part mid-sentence ("...identified by you in Question 4 (a)").
    A question head only opens a question when its number goes FORWARD.

Nothing here decides what a card says.  It reports what the scheme prints;
pe_all.py refuses whatever it cannot read one way.
"""
import os
import re
import sys

DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(DIR)))
SCHEMES = os.path.join(ROOT, 'examiner-reports', 'physical-education', 'schemes')

SITTINGS = [(2020, 'hl')] + [(y, lv) for y in range(2021, 2027)
                             for lv in ('hl', 'ol')]

ROMAN = r'i{1,3}|iv|vi{0,3}|ix|x'
QHEAD = re.compile(r'^Question\s+(\d{1,2})\b\s*[.\-–]?\s*'
                   r'(?:\(\s*(\d{1,3})\s*marks?\s*\))?', re.I)
# A part marker opening a line, in every shape the corpus prints it:
#   "(a)", "(a) (i)", "(i)", "a)", "14 (a) (i)", "14(c) (i)"
PART = re.compile(
    rf'^(?:(?P<q>\d{{1,2}})\s*)?\(\s*(?P<L>[a-h])\s*\)\s*(?:\(\s*(?P<R>{ROMAN})\s*\))?(?![a-z])'
    rf'|^(?:(?P<q2>\d{{1,2}})\s*)?(?P<L2>[a-h])\)\s*(?:\(?\s*(?P<R2>{ROMAN})\s*\)?)?(?![a-z])'
    rf'|^\(\s*(?P<R3>{ROMAN})\s*\)(?![a-z])', re.I)
# The table's own column heading, in every spelling the corpus prints:
# "Description Marks", "Description Mark", "Description 8 Marks".
TABLE_HEAD = re.compile(r'^Description\s*(?:\d{1,2}\s*)?Marks?\b', re.I)
# Where the written paper's scheme stops and the coursework project and the
# physical performance assessment begin. Both are marked from work this corpus
# does not hold, and neither is a question any paper prints. The two phrases
# are the SEC's own titles for those components and appear nowhere inside the
# written paper's scheme — checked over all thirteen sittings.
END = re.compile(r'Physical Activity Project|Performance Assessment', re.I)
FURNITURE = re.compile(
    r'^(?:Page\s*\|\s*\d+|Leaving Certificate|Coimisi|State Examinations'
    r'|Physical Education\s*[–-]|Marking Scheme|Blank Page'
    r'|Section\s+[ABC]\b|\d{1,3}$|There are \d+ questions|Any \d+ questions'
    r'|Answer any|Candidates (?:must|are required to) answer'
    r'|(?:Three|Two|Five|Ten|Any) [a-z]* ?questions to be answered)', re.I)
PAGE_MARK = re.compile(r'^##\s*Page\s*\d+\s*$', re.I)
# The SEC's own per-question price, printed on a section's instruction line
# rather than on each question head: "Answer any 5 questions from 1-12. 8 marks
# per question." 2022 and 2023 Ordinary price whole sections that way and print
# nothing on the heads, so without this every Section A question in 2022 has no
# printed total at all and 24 asks are refused for a tariff the SEC did print.
PER_QUESTION = re.compile(r'\b(\d{1,3})\s*marks?\s+per\s+question\b', re.I)


def tidy(s):
    return ' '.join((s or '').split())


# ------------------------------------------------------------- the tariff ---
# Every form below is the SEC's own printed arithmetic. Nothing is derived by
# dividing a total by a count the scheme did not state.
#   "8 (2 x 4 marks)", "2 x 2 Marks", "2x1marks=2", "2 x 2 (1+1) marks"
GROUP = re.compile(
    r'\b(\d{1,2})\s*(?:x|×)\s*(\d{1,2})\s*'
    r'(?:\(\s*\d{1,2}(?:\s*\+\s*\d{1,2})+\s*\)\s*)?(?:marks?|m)\b', re.I)
#   "4 marks (x2)", "2 marks (x2)"
GROUP_PAREN = re.compile(r'\b(\d{1,2})\s*marks?\s*\(\s*x\s*(\d{1,2})\s*\)', re.I)
#   "3 marks + 3 marks", "2 marks + 1 mark + 1 mark"
REPEAT = re.compile(r'\b(\d{1,2})\s*marks?(?:\s*\+\s*(\d{1,2})\s*marks?)+', re.I)
#   "2 + 2", "1 + 1 mark", "3+3+2+2"
BARE_REPEAT = re.compile(r'(?<![\d.])(\d{1,2})(?:\s*\+\s*\d{1,2})+\s*(?:marks?|m)?\s*$', re.I)
MARKS = re.compile(r'\b(\d{1,3})\s*marks?\b', re.I)
# "5-6 m", "3-4 marks", "1-2" — a BAND of quality, never a tariff.
BAND_RANGE = re.compile(r'\b\d{1,2}\s*[-–]\s*\d{1,2}\s*(?:m\b|marks?\b)?\s*$', re.I)
# A Description row that opens a BAND of quality rather than a criterion.
BAND_OPENER = re.compile(
    r'^(?:very good|good\b|fair\b|poor\b|weak\b|excellent|clear\b|accurate'
    r'|detailed|some\b|somewhat|limited|little|brief|vague|basic|full and'
    r'|in depth|mostly|no relevant)', re.I)
# A tariff cell that landed on a line of its own in the marks column.
TARIFF_ONLY = re.compile(
    r'^(?:\(?\s*\d{1,3}\s*(?:marks?|m)?\s*\)?'
    r'|\d{1,2}\s*[x×]\s*\d{1,2}\s*(?:\(\s*\d{1,2}(?:\s*\+\s*\d{1,2})+\s*\)\s*)?'
    r'(?:marks?|m)?(?:\s*=\s*\d{1,3})?'
    r'|\d{1,3}\s*\(\s*\d{1,2}\s*[x×]\s*\d{1,2}\s*marks?\s*\)'
    r'|\+|[-–]|\d{1,2}\s*[-–]\s*\d{1,2}\s*(?:marks?|m)?'
    r'|\d{1,2}(?:\s*\+\s*\d{1,2})+\s*(?:marks?|m)?)'
    r'[\s.+]*$', re.I)


def tariffs_in(text):
    """Every printed group tariff in one line, as (claim, per)."""
    out = []
    for m in GROUP.finditer(text):
        out.append((int(m.group(1)), int(m.group(2))))
    for m in GROUP_PAREN.finditer(text):
        out.append((int(m.group(2)), int(m.group(1))))
    for m in REPEAT.finditer(text):
        values = [int(x) for x in re.findall(r'(\d{1,2})\s*marks?', m.group(0), re.I)]
        if len(values) > 1 and len(set(values)) == 1:
            out.append((len(values), values[0]))
    if not out:
        # The SEC's repeat with the marks column wrapped off the end of it:
        # the page prints "4 marks + 4 marks" and the converter breaks the
        # line after the second number, leaving "4 marks + 4" on one line and
        # "marks" glued to the head of the next. Read with the mark words
        # taken out, the arithmetic is unchanged and still the SEC's own.
        for candidate in (text, re.sub(r'\s*\b(?:marks?|m)\b', '', text, flags=re.I)):
            m = BARE_REPEAT.search(candidate)
            if not m:
                continue
            values = [int(x) for x in re.findall(r'\d{1,2}', m.group(0))]
            if len(values) > 1 and len(set(values)) == 1:
                out.append((len(values), values[0]))
            break
    return out


def steps_in(text):
    """A DESCENDING printed tariff — "3+3+2+2" — as its own list of steps.

    The SEC's own note explains the form: "there may be three parts to a
    question, and a total of 12 marks allocated... 6 + 3 + 3. This means the
    first correct answer encountered is awarded 6 marks and each subsequent
    correct answer is awarded 3 marks." It is not a best-of — two answers at
    six is not the nine that 6-then-3 pays — so it rides `perOptionSteps`.
    """
    for candidate in (text, re.sub(r'\s*\b(?:marks?|m)\b', '', text, flags=re.I)):
        m = BARE_REPEAT.search(candidate)
        if not m:
            continue
        values = [int(x) for x in re.findall(r'\d{1,2}', m.group(0))]
        if len(values) > 1 and len(set(values)) > 1 and values == sorted(
                values, reverse=True):
            return values
    return []


# ------------------------------------------------------------ row classes ---
# The examiner's own vocabulary: the words a scheme uses to say how WELL a
# thing was done rather than what the thing is. A Description row carrying any
# of them is grading an answer; a row carrying none of them, once its tariff
# cell is off, is stating one. Derived from the corpus, not guessed — every
# opener of every priced row across the thirteen schemes was listed and the
# graders separated from the content by hand once.
EXAMINER_VOCAB = re.compile(
    r'\b(?:accurate|accurately|accuracy|inaccurate|appropriate|appropriately'
    r'|award|awarded|band|brief|briefly|candidate|candidates|clear|clearly'
    r'|correct|correctly|incorrect|demonstrates?|describe[sd]?|describing'
    r'|description|detail|details|detailed|discuss|discusses|discussed'
    r'|discussion|evidence|examiner|examiners|excellent|explain|explains'
    r'|explained|explanation|fair|given|good|identif(?:y|ies|ied)|knowledge'
    r'|limited|mark|marks|must|name[sd]?|outline[sd]?|outlines|poor'
    r'|present(?:ed|s)?|provide[sd]?|providing|relevant|some|somewhat'
    r'|state[sd]?|statement|understanding|vague|vaguely|valid|weak'
    r'|response|responses|answer|answers|credit|reference|referenced'
    r'|sufficient|no marks|little|effort|level|levels of detail|quality)\b',
    re.I)
# An instruction to the examiner. It is printed inside the table and reads like
# content — "Note: type of feedback explained must be appropriate for an
# athlete with a visual impairment" — but it states a CONDITION on the answer.
EXAMINER_NOTE = re.compile(
    r'^(?:note\b|n\.?b\.?\b|award\b|marks? (?:awarded|available|allocated)'
    r'|do not\b|don\'t accept|no marks?\b|max(?:imum)?\b|deduct\b'
    r'|accept any (?:valid|other|reasonable|relevant)\b'
    r'|candidates? (?:must|should|may not|are not|to answer)\b|examiners?\b'
    r'|if the\b|total\b|where the candidate|must be\b|answers? must\b'
    r'|this (?:is|must)\b|only\b|one mark\b|marks for\b|or$)', re.I)
# The SEC's own lead-in to a list of answers, printed on a line of its own.
LEAD_IN = re.compile(
    r'^(?:e\.?\s?g\.?|eg\.?|for example|accept(?:able)?(?: any of the following)?'
    r'|possible (?:candidate )?(?:response|answer)s?'
    r'|suggested (?:response|answer)s?|sample (?:response|answer)s?'
    r'|examples?|answers? may include|[A-Z][^.?!]{0,70}?\b(?:may|might|could)'
    r'\s+(?:include|be)|candidates? (?:may|might|could|to)[^.?!]{0,60}?'
    r'\b(?:include|use|answer|name|state)[^.?!]{0,20})\s*[:.]?\s*$', re.I)
# The same lead-in printed at the head of its own list on one line:
# "Accept: continuous training; weight training; plyometrics".
LEAD_IN_INLINE = re.compile(
    r'^(?:e\.?\s?g\.?|eg\.?|for example|accept(?: any of the following)?'
    r'|possible (?:candidate )?(?:response|answer)s?'
    r'|suggested (?:response|answer)s?|sample (?:response|answer)s?'
    r'|answers? may include|examples? (?:include|may include))'
    r'\s*[:.]?\s+(?=\S)', re.I)
# And the same lead-in printed PART WAY ALONG a row, which is how 2022 sets
# every one of its lists: "Correctly identifies a characteristic of skilled
# performance Eg. Kinaesthetic awareness, Anticipation, Consistency".
LEAD_IN_MID = re.compile(
    r'\s(?:e\.?\s?g\.?|eg\.?|possible candidate response)\s*[:.]?\s+(?=[A-Za-z])',
    re.I)
BULLET = re.compile(r'^[ \t]*(?:[-•·▪‣●→–—*]|\d{1,2}\.\d{1,2}(?=\s))[ \t]*')
# What ENDS a list the SEC opened. A part often prices two or three criteria in
# one table and gives each its own examples:
#
#     Accurate definition of skill                          1 mark
#     e.g. learned behaviour "A learned action/behaviour..."
#     Accurate definition of ability                        1 mark
#     e.g. natural/ inbuilt.
#     Accurate discussion of statement
#     Good discussion 4 m                                   4 marks
#
# so a list that runs to the end of the part swallows the next criterion and
# the band ladder under it. The openers below are the ones the corpus prints at
# the head of a criterion row. Deliberately NOT among them: "State", "Name" and
# "Level", which open real answers — "State anxiety is an immediate emotional
# state characterised by apprehension..." is the SEC's own definition, and
# closing a list on it would throw the answer away to save a criterion.
CLOSES_LIST = re.compile(
    r"^(?:very good|good\b|fair\b|poor\b|weak\b|excellent|accurate|accurately"
    r"|clear\b|clearly|correct(?:ly)?\b|appropriate(?:ly)?\b|some\s|somewhat"
    r"|limited\b|little or no|brief\b|briefly|detailed\b|in depth|full and"
    r"|relevant\b|vague|basic\b|identif(?:y|ies|ied)\b|explains?\b|explanation"
    r"|describ(?:e|es|ed)\b|description\b|discuss(?:es|ed)?\b|discussion\b"
    r"|outlines?\b|outline of|defines?\b|definition\b|award\b|note\b|do not"
    r"|don't\b|no relevant|no marks|knowledge is|information is|analysis is"
    r"|candidates?\b|two\s|three\s|four\s|five\s|marks?\s|max\b)", re.I)
# A bare colon is NOT a lead-in. "Barriers may include:" opens a list and
# "Define the following types of goals related to physical activity:" opens the
# QUESTION, and the two are indistinguishable by punctuation — reading every
# colon as a lead-in filed the ask's own words and the criterion rows beneath
# it as answers, 31 of them in 2025 Higher alone. A row with a colon in it is
# left as a row, and stated() takes what follows the colon only when what
# follows carries no examiner vocabulary at all.
# A line that CONTINUES the one above it. The converter wraps a table cell the
# way the page prints it, and the marks column lands glued to the end of the
# wrapped line: "Clear and accurate description of the plane of movement
# provided. A 3" / "correct sporting example is used to support the
# description." Read one line at a time, the SEC's sentence arrives in halves
# with a tariff between them and no card can quote it. A continuation opens
# LOWER CASE — every row of a PE scheme table opens with a capital, a bullet,
# a part marker or a digit. A part marker is the exception that has to be
# written down: 2022 Ordinary letters its case study "a)", "b)", "c)", "d)"
# with no bracket in front, so the whole of Question 13 joined onto the line
# above it and eleven of its asks lost the letter they were printed under.
CONTINUES = re.compile(r'^(?:[‘“’]?[a-z]'
                       rf'|\((?!\s*(?:[a-h]|{ROMAN})\s*\)))', re.U)
# The other half of the same wrap, where the break falls before a capitalised
# word: "Kinaesthetic awareness, Anticipation, Consistency, Accuracy in" /
# "Technique/skill/movement pattern". Case says nothing there; what does is
# that the line above ENDS on a function word, which no printed row of a
# marking scheme does. Read one line at a time, the SEC's four characteristics
# were two, and a question paying 4 x 2 marks was refused for stating only
# two answers.
HANGS = re.compile(
    r'\b(?:in|of|the|a|an|and|or|to|for|with|on|at|by|from|that|this|as|is'
    r'|are|be|their|its|his|her|your|our|it|not|into|over|under|between'
    r'|during|about|than|when|which|who|whose|where|how|so|but|if|per|via'
    r'|used|such)$', re.I)
# The marks cell the converter glued to the end of a wrapped line. Taken off
# when the next line continues the sentence, and KEPT beside the part so the
# tariff it carries is still read. Never trusted blind: every joined answer is
# re-checked against the scheme markdown before it is lifted, and the block
# rendering appended to the same file holds the unwrapped cell, so a correct
# join traces and a wrong one does not.
GLUED_CELL = re.compile(
    r'\s+(?:\d{1,2}\s*[x×]\s*\d{1,2}\s*marks?\s*=\s*\d{1,3}'
    r'|\d{1,2}\s*[-–]\s*\d{1,2}\s*(?:marks?|m)?'
    r'|\d{1,3}\s*(?:marks?|m)?)$', re.I)


class Part:
    """One printed part of one scheme, merged over every table that opens it."""

    def __init__(self, index, address, qtotal):
        self.index = index
        self.address = address
        self.qtotal = qtotal        # marks printed on the question head
        self.cue = ''               # the ask, where the scheme reprints it
        self.rows = []              # Description-column rows, in printed order
        self.answers = []           # stated answers the examiner published
        self.cells = []             # marks-column cells, in printed order
        self.tariffs = []

    @property
    def key(self):
        return self.address

    def label(self):
        q, l, r = self.address
        return f'Q{q}' + (f'({l})' if l else '') + (f'({r})' if r else '')

    @property
    def total(self):
        """The marks the SEC prints for this part, or None. Never derived.

        Read in the order the document makes reliable, settled against the
        corpus rather than picked:

        1. the tariff the SEC prints at the head of the part's own line —
           "(a) 4 marks Definition of sponsorship", "3 marks - Identifies the
           stage of learning..." — which is the part's price and not its
           question's.
        2. ONE printed group: "2 x 4 marks" is eight marks and says so.
        3. the sum of the marks column down a table of separate criteria:
           "Example of safety equipment... 3 marks" printed twice is six. A
           table with a BAND ladder in it is not summed — a ladder prices one
           thing four times over, and adding those would treble the question.
        4. the marks column's own bare cell.
        5. the marks printed on the QUESTION head, for a part that IS the
           whole question.
        6. the ceiling of the SEC's own top band. "Very good discussion 5-6 m"
           is the SEC printing six as the most this earns. Read late, because
           where a part pays a group the ladder prices ONE answer and not the
           part — over the corpus, 44 of the 73 parts printing both disagree
           for exactly that reason.
        7. the single marks value printed anywhere in the part, where every
           value printed in it agrees.
        """
        for pattern in (r'^\(?\s*(\d{1,3})\s*marks?\)?\s',
                        r'\((\d{1,3})\s*marks?\)\s*$'):
            m = re.search(pattern, self.cue or '', re.I)
            if m:
                return int(m.group(1))
        groups = sorted(set(self.tariffs))
        if len(groups) == 1:
            return groups[0][0] * groups[0][1]
        prices = self.row_prices()
        if prices:
            return sum(prices)
        cells = set()
        for cell in self.cells:
            m = re.fullmatch(r'\(?\s*(\d{1,3})\s*(?:marks?)?\s*\)?', cell.strip(), re.I)
            if m:
                cells.add(int(m.group(1)))
        if len(cells) == 1:
            return next(iter(cells))
        if not cells and self.address[1] is None and self.address[2] is None \
                and self.qtotal:
            return self.qtotal
        ceiling = None
        for row in self.rows:
            if not BAND_OPENER.match(row):
                continue
            m = re.search(r'\b(\d{1,2})\s*[-–]\s*(\d{1,2})\s*(?:marks?|m)\b', row, re.I)
            value = int(m.group(2)) if m else None
            if value is None:
                m = re.search(r'\b(\d{1,2})\s*(?:marks?|m)\b', row, re.I)
                value = int(m.group(1)) if m else None
            if value is not None:
                ceiling = value if ceiling is None else max(ceiling, value)
        if ceiling is not None:
            return ceiling
        values = {int(m.group(1))
                  for text in [self.cue] + self.rows + self.answers + self.cells
                  for m in re.finditer(r'(\d{1,2})\s*(?:marks?|m)\b', text or '', re.I)}
        return next(iter(values)) if len(values) == 1 else None

    def row_prices(self):
        """The marks printed at the end of each criterion row, in order.

        Empty where the table holds a BAND ladder: a ladder prints the same
        answer at four qualities, so its values are alternatives and summing
        them would price the part three times over.
        """
        out = []
        for row in self.rows:
            if BAND_OPENER.match(row) or BAND_RANGE.search(row):
                return []
            m = re.search(r'(\d{1,2})\s*marks?\s*$', row, re.I)
            if m:
                out.append(int(m.group(1)))
        return out

    def __repr__(self):
        return (f'<{self.label()} qtotal={self.qtotal} rows={len(self.rows)} '
                f'answers={len(self.answers)}>')


def lines(year, level):
    """The scheme's printed lines for the WRITTEN PAPER, as (text, cells).

    Read from the CONVERTED markdown — the same text the build's provenance
    gate searches — with the converter's line wrapping undone, so a table cell
    arrives whole rather than in halves with the marks column between them.
    `cells` holds the marks-column fragments taken out of a joined line.
    """
    path = os.path.join(SCHEMES, f'{year}-{level}.md')
    raw = open(path, encoding='utf-8').read().split('<!-- pdf-block-order')[0]
    rows = [tidy(x) for x in raw.split('\n')]
    start = next(i for i, x in enumerate(rows)
                 if QHEAD.match(x) and int(QHEAD.match(x).group(1)) == 1)
    end = len(rows)
    for i in range(start, len(rows)):
        if END.search(rows[i]):
            end = i
            break
    out, cells = [], []
    for text in rows[start:end]:
        if not text or PAGE_MARK.match(text):
            continue
        if FURNITURE.match(text) and not PER_QUESTION.search(text):
            continue
        joins = CONTINUES.match(text) or (out and HANGS.search(out[-1]))
        if (out and joins and not TARIFF_ONLY.match(text)
                and not BULLET.match(text) and not TABLE_HEAD.match(text)
                and not QHEAD.match(text) and not LEAD_IN.match(text)
                and not LEAD_IN_INLINE.match(text) and not PART.match(text)):
            base = out[-1]
            m = GLUED_CELL.search(base)
            if m:
                cells[-1].append(tidy(m.group(0)))
                base = base[:m.start()]
            out[-1] = tidy(base + ' ' + text)
            continue
        out.append(text)
        cells.append([])
    return list(zip(out, cells))


def _marker(text, q):
    """(letter, roman, rest) where `text` opens with a part marker, else None."""
    m = PART.match(text)
    if not m:
        return None
    qq = m.group('q') or m.group('q2')
    if qq and int(qq) != q:
        return None
    letter = (m.group('L') or m.group('L2') or '').lower() or None
    roman = (m.group('R') or m.group('R2') or m.group('R3') or '').lower() or None
    return letter, roman, tidy(text[m.end():])


def read(year, level):
    """Every part the scheme prints, in document order, merged by address."""
    parts, order = {}, []
    q = 0
    qtotal = None
    letter = roman = None
    part = None
    in_table = False
    listing = False

    def open_part(address):
        nonlocal part, in_table, listing
        if address not in parts:
            parts[address] = Part(len(order), address, qtotal)
            order.append(address)
        part = parts[address]
        if part.qtotal is None:
            part.qtotal = qtotal
        in_table = False
        listing = False
        return part

    per_question = None
    for text, cells in lines(year, level):
        rate = PER_QUESTION.search(text)
        if rate:
            per_question = int(rate.group(1))
            if not QHEAD.match(text):
                continue
        head = QHEAD.match(text)
        if head and int(head.group(1)) > q:
            q = int(head.group(1))
            qtotal = int(head.group(2)) if head.group(2) else per_question
            letter = roman = None
            part = open_part((q, None, None))
            rest = tidy(text[head.end():])
            mk = _marker(rest, q) if rest else None
            if mk:
                letter, roman, rest = mk
                part = open_part((q, letter, roman))
            part.cells.extend(cells)
            if rest and TABLE_HEAD.match(rest):
                in_table = True
                rest = tidy(rest[TABLE_HEAD.match(rest).end():])
            if rest:
                if in_table:
                    listing = _file(part, rest, listing)
                else:
                    part.cue = rest
            continue
        if q == 0:
            continue

        mk = _marker(text, q)
        if mk:
            lt, rm, rest = mk
            # A bare roman stays under the letter it was printed beneath.
            if lt:
                letter, roman = lt, rm
            else:
                roman = rm
            part = open_part((q, letter, roman))
            part.cells.extend(cells)
            if rest and TABLE_HEAD.match(rest):
                in_table = True
                rest = tidy(rest[TABLE_HEAD.match(rest).end():])
                if rest:
                    listing = _file(part, rest, listing)
                continue
            if rest:
                # The ask, where the scheme reprints it; otherwise the first
                # criterion row of a table that opened on the marker's line.
                if in_table or part.cue or part.rows or part.answers:
                    listing = _file(part, rest, listing)
                else:
                    part.cue = rest
            continue

        if part is None:
            part = open_part((q, None, None))
        part.cells.extend(cells)

        if TABLE_HEAD.match(text):
            in_table = True
            listing = False
            rest = tidy(text[TABLE_HEAD.match(text).end():])
            if rest:
                listing = _file(part, rest, listing)
            continue

        if not in_table and not part.cue and not part.rows and not part.answers:
            part.cue = text
            continue

        listing = _file(part, text, listing)

    out = [parts[a] for a in order]
    for p in out:
        seen = []
        for text in [p.cue] + p.rows + p.answers + p.cells:
            for t in tariffs_in(text or ''):
                if t not in seen:
                    seen.append(t)
        p.tariffs = seen
    return out


def _file(part, text, listing):
    """File one printed line as a criterion row or as a stated answer.

    Returns whether the part is now inside a LIST the SEC opened with one of
    its own lead-ins, so the lines after it are filed as answers too.
    """
    text = tidy(text)
    if not text:
        return listing
    if TARIFF_ONLY.match(text):
        part.cells.append(text)
        return listing
    inline = LEAD_IN_INLINE.match(text)
    if inline:
        body = tidy(text[inline.end():])
        if body:
            part.answers.append(body)
        return True
    if LEAD_IN.match(text):
        part.rows.append(text)
        return True
    if BULLET.match(text):
        part.answers.append(tidy(BULLET.sub('', text)))
        return True
    mid = LEAD_IN_MID.search(text)
    if mid and len(tidy(text[mid.end():])) >= 8:
        head = tidy(text[:mid.start()])
        if head:
            part.rows.append(head)
        part.answers.append(tidy(text[mid.end():]))
        return True
    if listing and not EXAMINER_NOTE.match(text) and not CLOSES_LIST.match(text):
        part.answers.append(text)
        return True
    part.rows.append(text)
    return False


# What a Description row states, where it states anything: the SEC prints the
# answer after a colon or a dash inside the row itself. "Correct plane named-
# 1 mark: Transverse plane" is an answer; "Identifies test to measure
# flexibility 1 mark" is not.
STATED = re.compile(r':\s*(?P<body>[^:]{4,})$')


def strip_tariff(text):
    """One printed row with its marks-column arithmetic taken off."""
    out = tidy(text)
    for pattern in (
            r'\s*\(?\s*\d{1,3}\s*\(\s*\d{1,2}\s*[x×]\s*\d{1,2}\s*marks?\s*\)\s*\)?',
            r'\s*\(?\s*\d{1,2}\s*[x×]\s*\d{1,2}\s*(?:\(\s*\d{1,2}(?:\s*\+\s*\d{1,2})+\s*\)\s*)?'
            r'(?:marks?|m)?(?:\s*=\s*\d{1,3})?\s*\)?',
            r'\s*[-–]?\s*\d{1,2}\s*[-–]\s*\d{1,2}\s*(?:marks?|m)\b',
            r'\s*[-–]?\s*\b\d{1,3}\s*marks?\b',
            r'\s*[-–]\s*\d{1,2}\s*m\b',
            r'\s+\d{1,2}\s*[-–]\s*\d{1,2}\s*$',
            r'\s+\d{1,3}\s*$'):
        out = tidy(re.sub(pattern, ' ', out, flags=re.I))
    return tidy(out).strip(' .;:,-')


def is_content(text):
    """True where a printed line states an answer rather than grading one."""
    body = strip_tariff(text)
    if len(body) < 4:
        return False
    if TABLE_HEAD.match(body) or EXAMINER_NOTE.match(body) or LEAD_IN.match(body):
        return False
    return not EXAMINER_VOCAB.search(body)


def stated(row):
    """The answer a Description row states after its own colon, or ''."""
    text = tidy(row)
    if TABLE_HEAD.match(text) or EXAMINER_NOTE.match(text) or LEAD_IN.match(text):
        return ''
    m = STATED.search(strip_tariff(text) if MARKS.search(text) else text)
    if not m:
        return ''
    body = tidy(m.group('body')).strip(' .;:,-')
    if len(body) < 4 or EXAMINER_VOCAB.search(body):
        return ''
    return body


def answers_of(part):
    """Every answer the scheme states for one part, in printed order."""
    out = []
    for text in part.answers:
        body = strip_tariff(text)
        if body and body not in out:
            out.append(body)
    for row in part.rows:
        said = stated(row)
        if said and said not in out:
            out.append(said)
            continue
        if is_content(row):
            body = strip_tariff(row)
            if body not in out:
                out.append(body)
    return out


def band_only(part):
    """True where every priced row grades an answer and none states one."""
    return not answers_of(part)


def _audit():
    tot = ans = band = 0
    for year, level in SITTINGS:
        parts = read(year, level)
        a = sum(1 for p in parts if answers_of(p))
        tot += len(parts)
        ans += a
        band += len(parts) - a
        print(f'{year} {level.upper()}: {len(parts):>3} parts, {a:>3} state an '
              f'answer, {len(parts) - a:>3} band-only')
    print(f'\n{ans}/{tot} parts state an answer; {band} band-only')


if __name__ == '__main__':
    if '--audit' in sys.argv:
        _audit()
        raise SystemExit
    year, level = int(sys.argv[1]), sys.argv[2]
    if '--raw' in sys.argv:
        for text, cells in lines(year, level):
            print(repr(text), cells or '')
        raise SystemExit
    parts = read(year, level)
    print(f'{year} {level.upper()}: {len(parts)} part(s)')
    for p in parts:
        print(f'  {p!r} {"BAND-ONLY" if band_only(p) else ""} '
              f'total={p.total} tariffs={p.tariffs} cells={p.cells}')
        if p.cue:
            print(f'      cue: {p.cue[:140]}')
        for row in p.rows:
            print(f'      row: {row[:140]}')
        for a in answers_of(p):
            print(f'      ANS: {a[:140]}')
