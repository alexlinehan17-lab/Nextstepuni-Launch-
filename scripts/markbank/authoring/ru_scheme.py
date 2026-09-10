#!/usr/bin/env python3
"""Russian marking schemes — the reprinted ask, its tariff, and the stated answer.

    python3 scripts/markbank/authoring/ru_scheme.py 2024 hl --full
    python3 scripts/markbank/authoring/ru_scheme.py --audit

What this document is
---------------------
A Russian scheme is four documents stapled together and only two of them are
answers::

    SECTION I – 120 MARKS                          <- priced answers
      Question 1.1 – Comprehension (text) (40 marks)
        1. (i) Describe how the fishermen spent their days. Give two details. 2x2 marks
        assign 2 marks:
        • they spent all days on the lake shore / from morning to the darkness
        • they swam
        2. (i) What did the boys tell the fishermen during breakfast? … 1x2 marks
        assign 2 marks:
        • they saw a cat with a fish
        assign 1 mark:                               <- the part-credit rung
        • they saw a cat
    SECTION II GRAMMAR, LANGUAGE USE AND GUIDED WRITING – 100 marks
        Question 1. Grammar                          <- priced answers, in brackets
        Question 2. Short Essay / Question 3. Guided writing   <- a BAND GRID
    LISTENING COMPREHENSION – 80 MARKS             <- priced answers, but the
                                                      ask needs the recording
    APPENDIX 2: AURAL TEXTS                        <- the recording, in print

Unlike French, this scheme REPRINTS the English half of every comprehension
ask above its answers, so the paper and the scheme are joined on wording
(Law 4) with no order-only pairing anywhere in the subject.

THE TARIFF IS PRINTED THREE WAYS, AND NEVER GUESSED
---------------------------------------------------
1. ``2x2 marks`` — two answers at two marks each. Read straight.
2. ``6 marks`` under a unit that states its own rate — "Allocate 2 marks for
   each correct idea/concept" — where the ask's own printed count agrees:
   "Give three details. 6 marks" is three answers at two. Both halves must
   agree or the ask is refused: the rate is not applied to a count this reader
   inferred, and a count is not divided into a total that does not divide.
3. Nothing at all. 2021 Ordinary Text 2 heads every ask "(i) Give three
   details about this luxury villa." with no tariff on the line, and prices
   the WHOLE text at 30 marks. That is only read where the unit's own printed
   total is reached exactly by the rate times the counts of its own asks
   (`_checksum`), which it is in every unit where this reader uses it. A unit
   that does not add up carries a `fault` and nothing in it is priced.

THE ANSWERS ARE STATED FOUR WAYS
--------------------------------
* bulleted, one per line, sometimes two or three to a line where the SEC set
  them in columns and the extractor flattened the row;
* bulleted with a lesser value printed on the same line ("• Cheap 1 mark");
* under an ``assign N marks:`` heading, which is the same answer at a lower
  rung and is disclosed on the card as a note, never offered as a full answer;
* joined by ``+`` under "Main points:", which is how the Higher summary-writing
  question lists what a paragraph must contain.

Sections the scheme answers with a BAND GRID — the short essay, the guided
writing, Ordinary's short answers and extended writing — are read too, so that
the refusals this bank records are counted rather than assumed. So is the
listening test, whose asks are priced and answered but can only be reached
from the recording. See ru_all.py, which turns both into exclusions carrying
the scheme's own words as evidence.
"""
import argparse
import os
import re
import sys

import pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))

SUBJECT = 'russian'


def schemes_dir(subject=SUBJECT):
    return os.path.join(ROOT, 'examiner-reports', subject, 'schemes')


# --------------------------------------------------------------- the units --
# A unit is one printed question of the paper, named by what it IS rather than
# by a number, because the paper numbers Question 1 three times over — once in
# Section I, once in Section II and once in the listening test — and a section
# token in a citation may hold no dot (reconcile.py's HEAD reads
# [A-Za-z0-9]+).
UNIT_NAME = {
    'C1': 'Question 1.1 — Comprehension',
    'C2': 'Question 2.1 — Comprehension: summary writing',
    'LA1': 'Question 1.2 — Language awareness',
    'LA2': 'Question 2.2 — Language awareness',
    'CA1': 'Question 1.3 — Cultural awareness',
    'SD': 'Structuring discourse',
    'GR': 'Grammar',
    'SE': 'Short essay — cultural awareness',
    'GW': 'Guided writing',
    'IR1': 'Section I(A) Question 1 — Information retrieval',
    'IR2': 'Section I(A) Question 2 — Information retrieval',
    'MM': 'Section I(B) — Mix and match',
    'CD': 'Section I(D) — Comprehension',
    'SA': 'Section II(A) — Short answers: cultural awareness',
    'EW': 'Section II(B) — Extended writing',
    'L1': 'Listening Comprehension Section I',
    'L2': 'Listening Comprehension Section II',
    'L3': 'Listening Comprehension Section III',
    'L4': 'Listening Comprehension Section IV',
}

# Where the answer document stops being an answer document. Everything from
# here is the Modified Marking Scheme and the transcript of the recording,
# printed inside the ANSWER document; reading past it would key the
# transcript's own "SECTION I" as a listening section and its speaker turns as
# marking points.
APPENDIX = re.compile(r'^APPENDIX\b', re.I)
SEC_I = re.compile(r'^SECTION\s+I\b\s*[–—-]?\s*\d*\s*MARKS?\b', re.I)
SEC_II = re.compile(r'^SECTION\s+II\b', re.I)
LISTENING = re.compile(r'^LISTENING\s+COMPREHENSION\b', re.I)
LISTEN_SECTION = re.compile(r'^SECTION\s+(IV|III|II|I)\b(?!\s*[–—-]?\s*\d*\s*MARKS)', re.I)
ROMAN_UNIT = {'I': 'L1', 'II': 'L2', 'III': 'L3', 'IV': 'L4'}

# The head of a unit, inside the section it belongs to.
#   "Question 1.1 – Comprehension (text) (40 marks)"   2023-2025 Higher
#   "Q.1. Comprehension 40 marks"                      2021-2022 Higher
#   "Q. 1.2 Language awareness 10 marks"
#   "A. INFORMATION RETRIEVAL (30 marks): Text 1 = 30 marks"   Ordinary
Q = r'(?:Q(?:uestion)?\s*\.?\s*)'
HL_UNITS_I = [
    (re.compile(rf'^{Q}1\s*\.\s*1\b', re.I), 'C1'),
    (re.compile(rf'^{Q}1\s*\.\s*2\b', re.I), 'LA1'),
    (re.compile(rf'^{Q}1\s*\.\s*3\b', re.I), 'CA1'),
    (re.compile(rf'^{Q}2\s*\.\s*1\b', re.I), 'C2'),
    (re.compile(rf'^{Q}2\s*\.\s*2\b', re.I), 'LA2'),
    (re.compile(rf'^{Q}3\b.*Structuring', re.I), 'SD'),
    # 2021 and 2022 head the comprehension itself "Q.1. Comprehension 40
    # marks" and the summary "Q.2 Summary writing 40 marks", with the 1.1 and
    # 2.1 sub-heads left off entirely. Matched AFTER the dotted forms so
    # "Q.1.2" is never read as "Q.1".
    (re.compile(rf'^{Q}1\b.*Comprehension', re.I), 'C1'),
    (re.compile(rf'^{Q}2\b.*Summary\s+writing', re.I), 'C2'),
]
HL_UNITS_II = [
    (re.compile(rf'^{Q}1\b', re.I), 'GR'),
    (re.compile(rf'^{Q}2\b', re.I), 'SE'),
    (re.compile(rf'^{Q}3\b', re.I), 'GW'),
]
OL_UNITS_I = [
    (re.compile(r'^Text\s*1\b', re.I), 'IR1'),
    (re.compile(r'^Text\s*2\b', re.I), 'IR2'),
    (re.compile(rf'^{Q}1\b', re.I), 'IR1'),
    (re.compile(rf'^{Q}2\b', re.I), 'IR2'),
    (re.compile(r'^B\.\s*MIX\s+AND\s+MATCH', re.I), 'MM'),
    (re.compile(r'^C\.\s*STRUCTURING\s+DISCOURSE', re.I), 'SD'),
    (re.compile(r'^D\.\s*COMPREHENSION', re.I), 'CD'),
    # The language-awareness task the SEC prints at the end of each retrieval
    # text and prices separately. It has no letter and no number of its own,
    # so it is named after the text it belongs to.
    (re.compile(r'^Language\s+awareness\b', re.I), 'LA'),
]
OL_UNITS_II = [
    (re.compile(r'^A\.\s*Short\s+answers', re.I), 'SA'),
    (re.compile(r'^B\.\s*Extended\s+Writing', re.I), 'EW'),
]

# The unit's own printed total: "40 marks", "(30 marks)", "30 marks (24 + 6
# marks)" — the last of which prices content and coherence separately and
# whose FIRST number is the whole.
UNIT_TOTAL = re.compile(r'\(?(\d{1,3})\s*marks?\)?', re.I)
# The head that prices a unit's two halves separately: "Q.1 30 marks (24 + 6
# marks)" is twenty-four marks of reading and six of language awareness.
CONTENT_SHARE = re.compile(r'\(\s*(\d{1,3})\s*\+\s*(\d{1,3})\s*marks?\s*\)', re.I)

# The rate a unit states for itself, above its own asks.
#   "Allocate 2 marks for each correct idea/concept unless otherwise stated"
#   "• Award 2 marks per detail."
#   "Award 2 marks for each detail"
WORD_RATE = {'one': 1, 'two': 2, 'three': 3}
RATE = re.compile(
    r'(?:Allocate|Award|Give)\s+(\d{1,2}|one|two|three)\s+marks?\s+'
    r'(?:for\s+|per\s+)(?:each\s+)?(?:of\s+)?'
    r'(?:correct\s+)?(?:idea|concept|detail|answer|correct\s+answer|'
    r'correct\s+form|phrase|word)', re.I)

# The tariff as the scheme prints it at the end of an ask's own head.
#   "2x2 marks"  "3 x 2 marks"  "(2 x 2 marks)"  "4 marks"  "10 marks"
TARIFF = re.compile(
    r'\(?\s*(\d{1,2})\s*(?:[x×]\s*(\d{1,2})\s*)?marks?\s*\)?\s*$', re.I)

# A rung: the same answer, shorter, worth less. "assign 2 marks:" heads the
# full-mark answers and "assign 1 mark:" the lesser ones.
ASSIGN = re.compile(r'^assign\s+(\d{1,2})\s+marks?\s*:?\s*$', re.I)
# The same thing printed at the END of a bullet: "• Cheap 1 mark".
TRAILING_MARK = re.compile(r'\s+(\d{1,2})\s*marks?\.?\s*$', re.I)

BULLETS = '•●▪■○◦'
BULLET = re.compile(rf'^[{BULLETS}]\s*')
SPLIT_BULLET = re.compile(rf'\s*[{BULLETS}]\s*')
# The Higher summary question lists what a paragraph must contain as one
# plus-joined run under "Main points:". "Secondary details:" beneath it is a
# SECOND list the scheme pays the same rate for.
MAIN_POINTS = re.compile(r'^(Main\s+points|Secondary\s+details)\s*:\s*(.*)$', re.I)

# An ask's own head, inside a unit.
#   "1. (i) Describe how the fishermen spent their days. Give two details."
#   "(ii) Give two details about the local cat called ‘The Thief’."
#   "4. Name two things scooter users should remember…"
#   "Part 1. What does Masha think about her work experience so far?"
ROMAN = r'(?:i{1,3}|iv|vi{0,3}|ix|x)'
ASK_NUM = re.compile(rf'^(?:Part\s+)?(\d{{1,2}})\s*\.\s*(?:\(\s*({ROMAN})\s*\)\s*)?(.*)$', re.I)
ASK_ROMAN = re.compile(rf'^\(\s*({ROMAN})\s*\)\s*(.*)$', re.I)

# The number of answers an ask asks for, printed in its own words. The scheme
# and the paper both print it, in English, in every ask that wants more than
# one. "two details", "FOUR details", "three of these countries".
COUNTS = {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6,
          'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10}
# How many answers the ask wants, printed in its own words. Both documents
# print it, in English, in every ask that wants more than one: "two details",
# "FOUR details", "three of these countries", "two creative activities".
#
# Up to two words may stand between the number and the noun — "two creative
# activities", "three factual details" — because the SEC qualifies the noun
# freely and a fixed list of adjectives priced "Name two creative activities
# Dina participated in" as a one-answer ask worth two marks where the paper
# pays four.
COUNT_WORD = re.compile(
    r'\b(one|two|three|four|five|six|seven|eight|nine|ten)\b\s+'
    r"(?:(?!marks?\b)[\w\u2019'-]+\s+){0,2}?"
    r'(?:details?|reasons?|examples?|things?|countr(?:y|ies)|colou?rs?|'
    r'activit(?:y|ies)|places?|words?|sentences?|advantages?|disadvantages?|'
    r'items?|points?|names?|pets?|expressions?|phrases?|verbs?|nouns?|'
    r'aspects?|benefits?|subjects?|ways?|facts?|features?|steps?|sections?)\b',
    re.I)

# Examiner instructions, never answers.
NOTE = re.compile(
    r'^(?:Note\s*:|N\.?B\.?\b|Penalise\b|Do not\b|Accept\b|Allow\b|'
    r'No mark\b|No marks\b|Marks are awarded\b|Award\b|Allocate\b|Give \w+ marks?\b|'
    r'Take a global view\b|This list is not exhaustive\b|\*|'
    r'Where a candidate\b|Single marks\b|Discretionary\b|If a candidate\b|'
    r'The quality of\b|Read the\b|Read through\b|Answer in\b|Answer the\b|'
    r'Write a paragraph\b|Write \d|Each answer\b|Marks:|Content of each\b|'
    r'For full marks\b|Main points\s*:\s*$|Secondary details\s*:\s*$|'
    r'General\s*:|Segment\s+\d|Answer ONE\b|In the text\b|Indicate the case\b|'
    r'Supply the infinitive\b|Match the\b|Put the words\b|Insert the\b|'
    r'Three phrases\b|Two of the following\b|Sampla\b|Example\b|OR$|N[ÓO]\b)', re.I)
PAGE = re.compile(r'^(?:##\s*Page\s*\d+\s*$|\d{1,3}\s*$)')


# The white space that separates two printed COLUMNS of a scheme table from
# the words inside one. Answers set side by side are twenty or more points
# apart; the words of a sentence at this size are three to six.
#
# This is why the scheme is read from the PDF and not only from the markdown.
# extract-scheme.py joins a printed ROW left to right, which is right for a
# question and the marks beside it and wrong for a menu: 2022 Ordinary Text 1
# sets its answers in two columns and the markdown reads "They are flexible
# Learn moves quickly" — one line holding two separate answers, either of
# which earns the two marks on its own. Offered as printed it is a card that
# says a student must write both.
COLUMN_GAP = 20.0
BASELINE_TOL = 3.5
# How close to the page's widest right edge a row must reach to be reading as
# a line that WRAPPED rather than one that ended.
MEASURE_TOL = 14.0


def _pdf_rows(path):
    """[(page, [group, …], full_measure)] — every printed row, cut into its
    columns, and whether it runs to the page's own right-hand measure.

    The measure is what says whether the next row CONTINUES this one. A
    Russian scheme heads some asks without a question mark and without a full
    stop — 2021 Ordinary prints "1.(iii). Give two details about Dina's life
    when the family moved to Yekaterinburg" — so punctuation cannot decide it,
    and reading every short row beneath such a head as more of the question
    swallowed the next ask whole. A wrapped line follows a line that reached
    the measure; an answer follows one that stopped short.
    """
    out = []
    with pymupdf.open(path) as doc:
        for pno in range(doc.page_count):
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
            measure = max((max(w[1] for w in r['w']) for r in rows),
                          default=0.0)
            for row in sorted(rows, key=lambda r: r['mid']):
                groups = []
                for x0, x1, word in sorted(row['w']):
                    if groups and x0 - groups[-1][1] < COLUMN_GAP:
                        groups[-1][1] = x1
                        groups[-1][2].append(word)
                    else:
                        groups.append([x0, x1, [word]])
                full = groups and groups[-1][1] >= measure - MEASURE_TOL
                out.append((pno + 1, [' '.join(g[2]) for g in groups],
                            bool(full)))
    return out


def _repair(group, repairs):
    for old, new in repairs:
        group = group.replace(old, new)
    return group


def _rate_on(line):
    """The per-answer rate a line states for the unit it is printed under."""
    m = RATE.search(line)
    if not m:
        return None
    tok = m.group(1).lower()
    return int(tok) if tok.isdigit() else WORD_RATE[tok]


class Part:
    """One priced component of an ask: a rung of answers at one rate."""

    __slots__ = ('rate', 'answers', 'claim', 'label')

    def __init__(self, rate, claim=None, label=None):
        self.rate, self.claim, self.label = rate, claim, label
        self.answers = []


class Ask:
    """One reprinted ask, with the tariff and answers printed beneath it."""

    __slots__ = ('unit', 'item', 'roman', 'cue', 'notation', 'total', 'claim',
                 'per', 'answers', 'rungs', 'fault', 'line', 'page',
                 'full_rung')

    def __init__(self, unit, item, roman, cue, line, page):
        self.unit, self.item, self.roman = unit, item, roman
        self.cue, self.line, self.page = cue, line, page
        self.notation = None
        self.total = self.claim = self.per = None
        self.answers = []          # [(text, marks_or_None)]
        self.rungs = []            # [(text, marks)] worth less than full
        self.fault = None
        self.full_rung = None

    @property
    def key(self):
        return (self.unit, self.item, self.roman)

    @property
    def label(self):
        ref = f'Q{self.item}' if self.item is not None else 'Q'
        if self.roman:
            ref += f'({self.roman})'
        return ref

    def __repr__(self):
        return (f'<Ask {self.unit} {self.label} {self.notation} '
                f'{len(self.answers)}a {self.cue[:40]!r}>')


class RuScheme:
    """One sitting's marking scheme, read as priced asks under named units."""

    def __init__(self, year, level, subject=SUBJECT):
        self.year, self.level, self.subject = year, level, subject
        self.path = os.path.join(schemes_dir(subject), f'{year}-{level}.md')
        self.pdf_path = os.path.join(schemes_dir(subject), f'{year}-{level}.pdf')
        self.asks = []
        self.unit_totals = {}
        self.unit_rates = {}
        self.unit_tariffs = {}
        self.unit_content = {}
        self.unit_lines = {}
        self.unit_faults = {}
        self.band_units = set()
        self._read()
        self._price()

    # -- the walk -----------------------------------------------------------
    def _read(self):
        rows = _pdf_rows(self.pdf_path)
        repairs = MISPRINTS.get((self.subject, self.year, self.level), ())
        for old, new in repairs:
            assert any(old in g for _p, gs, _f in rows for g in gs), \
                f'{self.pdf_path}: misprint {old!r} not found'
        if repairs:
            rows = [(p, [_repair(g, repairs) for g in gs], f)
                    for p, gs, f in rows]
        # The walk opens INSIDE Section I. 2021 and 2022 Ordinary print no
        # "SECTION I" head at all — the scheme opens straight on "A.
        # INFORMATION RETRIEVAL (30 marks)" — and a reader that waits for one
        # read those two sittings' whole first section as nothing.
        section = 'I'
        unit = None
        page = 0
        cur = None
        rung = None
        pending = None       # an ask head whose tariff is on the next line
        pending_wrapped = False
        # The number an ask inherits from the one above it. The SEC prints
        # "2. (i) …" and then "(ii) …" with the 2 left off, exactly as the
        # paper does, so a roman with no number of its own belongs to the
        # last number printed in that unit. Without this the scheme's
        # "(ii)" was keyed at no question at all and matched no printed ask.
        last_item = {}
        for page, groups, full in rows:
            groups = [' '.join(g.split()) for g in groups if g.strip()]
            if not groups:
                continue
            line = ' '.join(groups)
            if APPENDIX.match(line):
                break
            if LISTENING.match(line):
                section, unit, cur, pending = 'L', None, None, None
                continue
            if section != 'L':
                if SEC_I.match(line):
                    section, unit, cur, pending = 'I', None, None, None
                    continue
                if SEC_II.match(line):
                    section, unit, cur, pending = 'II', None, None, None
                    continue
            elif LISTEN_SECTION.match(line):
                unit = ROMAN_UNIT[LISTEN_SECTION.match(line).group(1).upper()]
                cur, rung, pending = None, None, None
                continue
            hit = self._unit_head(section, line, unit)
            if hit:
                unit, cur, rung, pending = hit, None, None, None
                self.unit_lines.setdefault(unit, [])
                total = self._total_on(line)
                if total is not None:
                    # LAST head wins. The Higher scheme heads its first
                    # comprehension twice — "Question 1. Comprehension (40 + 10
                    # = 50 marks)" and then "Question 1.1 – Comprehension
                    # (text) (40 marks)" — and the outer head prices the
                    # language-awareness question with it. Keeping the first
                    # made every reading unit's own asks look ten marks short.
                    self.unit_totals[unit] = total
                rate = _rate_on(line)
                if rate:
                    self.unit_rates.setdefault(unit, rate)
                tariff = _split_tariff(line)
                if tariff:
                    self.unit_tariffs.setdefault(unit, tariff)
                share = CONTENT_SHARE.search(line)
                if share:
                    # "Q.1 30 marks (24 + 6 marks)": the head prices the
                    # reading half and the language-awareness half separately,
                    # and the first of the two is what its own asks add up to.
                    self.unit_content[unit] = int(share.group(1))
                continue
            if unit is None:
                continue
            self.unit_lines.setdefault(unit, []).append((page, line))
            rate = _rate_on(line)
            if rate and cur is None:
                self.unit_rates.setdefault(unit, rate)
            tariff = _split_tariff(line)
            if tariff and cur is None:
                self.unit_tariffs.setdefault(unit, tariff)
            if self.unit_totals.get(unit) is None and cur is None \
                    and len(line) < 40 and not NOTE.match(line):
                t = self._total_on(line)
                if t is not None:
                    self.unit_totals[unit] = t
            if PAGE.match(line):
                continue
            if unit not in READING_UNITS and unit not in LISTENING_UNITS:
                # Every other unit is read by a reader of its own, from these
                # lines. Running the generic ask parser over them keyed a
                # cultural-awareness word list ("1. альбом", "2. певица") as
                # eighteen separate asks.
                continue

            # A head that wrapped. Its continuation carries the rest of the
            # question and, in 2021, the tariff: "1. Tolya is uncertain about
            # some aspects of his future and certain about others." then
            # "Give four details. 10 marks".
            if pending is not None:
                t = TARIFF.search(line)
                if t and (TARIFF.fullmatch(line) or t.start() > 0):
                    pending.notation = t.group(0).strip()
                    tail = line[:t.start()].strip()
                    if tail:
                        pending.cue = f'{pending.cue} {tail}'.strip()
                    pending = None
                    continue
                # The rest of a wrapped question, but only where the row
                # cannot be an answer: a BULLET opens the scheme's answers and
                # never continues its question. 2022 Ordinary Text 2 heads
                # "(i) Give three details which should be include in the
                # Personal and Contact information section" — no question
                # mark, no full stop — and swallowing the "• Name" beneath it
                # cost the whole text its answers.
                if pending_wrapped and not BULLET.match(line) \
                        and self._ask_head(line, unit) is None:
                    pending.cue = f'{pending.cue} {line}'.strip()
                    pending_wrapped = full
                    if not full:
                        pending = None
                    continue
                pending = None

            head = self._ask_head(line, unit, last_item.get(unit))
            if head is not None:
                cur, rung = head, None
                if head.item is not None:
                    last_item[unit] = head.item
                cur.page = page
                self.asks.append(cur)
                # A head is complete the moment it carries its own tariff,
                # whatever its punctuation. Treating an untariffed-looking
                # sentence as unfinished swallowed the answers beneath it:
                # 2022 Ordinary heads "(i) What makes this school unique 1 x 2
                # marks" with no question mark, and its four answers were read
                # as the rest of the question.
                pending = cur if cur.notation is None else None
                pending_wrapped = full
                continue
            if cur is None:
                continue
            m = ASSIGN.match(line)
            if m:
                rung = int(m.group(1))
                continue
            if NOTE.match(line):
                continue
            for txt, marks in self._answers_on(groups):
                # A line under an "assign N marks:" heading, or one carrying
                # its own smaller mark, is a RUNG — the same answer, shorter,
                # worth less — and never an answer a card may offer in full.
                # The full rate is the FIRST the ask prints, because the SEC
                # prints the ladder from the top down.
                if rung is not None:
                    if cur.full_rung is None:
                        cur.full_rung = rung
                    if rung < cur.full_rung:
                        cur.rungs.append((txt, rung))
                    else:
                        cur.answers.append((txt, None))
                elif marks is not None and cur.answers:
                    cur.rungs.append((txt, marks))
                else:
                    cur.answers.append((txt, marks))

    def _unit_head(self, section, line, unit):
        if section == 'I':
            table = HL_UNITS_I if self.level == 'hl' else OL_UNITS_I
        elif section == 'II':
            table = HL_UNITS_II if self.level == 'hl' else OL_UNITS_II
        else:
            return None
        for rx, token in table:
            if rx.match(line):
                if token == 'LA':
                    # The Ordinary language-awareness task is named after the
                    # retrieval text it is printed under.
                    return 'LA1' if unit in (None, 'IR1', 'LA1') else 'LA2'
                return token
        return None

    @staticmethod
    def _total_on(line):
        """The whole a printed head prices, or None.

        "10 x 4 marks" is a whole of FORTY, not of four: the Higher
        summary-writing question heads itself that way and reading the last
        number alone priced a forty-mark question at four.
        """
        split = _split_tariff(line)
        if split:
            return split[2]
        m = UNIT_TOTAL.search(line)
        return int(m.group(1)) if m else None

    def _ask_head(self, line, unit, inherited=None):
        """An ask's own head, or None. The tariff may be on the next line."""
        item = roman = None
        m = ASK_NUM.match(line)
        if m:
            item, roman, rest = int(m.group(1)), m.group(2), m.group(3)
        else:
            m = ASK_ROMAN.match(line)
            if not m:
                return None
            roman, rest = m.group(1), m.group(2)
            item = inherited
        rest = rest.strip()
        if re.match(r'^\d{1,2}\s*\.', rest):
            # "2.1. Read the following four texts about career choice." is the
            # sub-head of the summary-writing question, not an ask inside it;
            # read as one it shipped the section's own instructions as a
            # question three times over.
            return None
        notation = None
        t = TARIFF.search(rest)
        if t:
            notation = t.group(0).strip()
            rest = rest[:t.start()].strip()
        if not rest or len(rest) < 6:
            return None
        if BULLET.match(rest):
            return None
        rest = rest.lstrip('. ')
        ask = Ask(unit, item, roman.lower() if roman else None, rest, line, 0)
        ask.notation = notation
        return ask

    @staticmethod
    def _answers_on(groups):
        """[(text, marks or None)] — the answers this printed ROW states.

        One per printed COLUMN, and one per bullet inside a column. A bullet
        is not required: 2021 and 2022 Ordinary print every comprehension
        answer as a bare line ("India", "USA", "Saudi Arabia"), and reading
        only bulleted lines left both sittings' whole comprehension unanswered
        while its asks were priced.
        """
        m = MAIN_POINTS.match(' '.join(groups))
        if m:
            return [(p.strip(), None) for p in m.group(2).split('+') if p.strip()]
        out = []
        for chunk in [c for g in groups for c in SPLIT_BULLET.split(g)]:
            chunk = chunk.strip()
            if not chunk:
                continue
            marks = None
            t = TRAILING_MARK.search(chunk)
            if t:
                marks = int(t.group(1))
                chunk = chunk[:t.start()].strip()
            if chunk:
                out.append((chunk, marks))
        return out

    # -- pricing ------------------------------------------------------------
    def _price(self):
        for ask in self.asks:
            self._price_one(ask)

    def _price_one(self, ask):
        rate = self.unit_rates.get(ask.unit)
        want = self._count_wanted(ask.cue)
        if ask.notation:
            m = TARIFF.search(ask.notation)
            n, per = int(m.group(1)), m.group(2)
            if per:
                ask.claim, ask.per = n, int(per)
                ask.total = n * int(per)
            elif rate and n % rate == 0 and n // rate > 1:
                # "6 marks" under "Allocate 2 marks for each correct idea".
                # Read only where the ask's OWN printed count agrees with the
                # division: the SEC states both, and a disagreement is a fault
                # to report, never a number to choose between.
                claim = n // rate
                if want is not None and want != claim:
                    ask.fault = (f'the head prices {n} marks at the unit rate of '
                                 f'{rate}, which is {claim} answers, but the ask '
                                 f'itself asks for {want}')
                    return
                ask.claim, ask.per, ask.total = claim, rate, n
            else:
                ask.claim, ask.per, ask.total = 1, n, n
            return
        if rate and want:
            ask.claim, ask.per, ask.total = want, rate, want * rate
            return
        if rate and want is None:
            ask.claim, ask.per, ask.total = 1, rate, rate

    @staticmethod
    def _count_wanted(cue):
        m = COUNT_WORD.search(cue or '')
        return COUNTS[m.group(1).lower()] if m else None

    # -- the checksum -------------------------------------------------------
    # Ordinary's two retrieval texts are priced 30 marks EACH, and six of
    # those thirty belong to the language-awareness task the SEC prints under
    # the text and prices as a task of its own ("Q.1 30 marks (24 + 6
    # marks)"). The reading half is therefore twenty-four, and comparing the
    # asks against the thirty on the head reported a six-mark shortfall in
    # every one of the ten Ordinary retrieval texts in the corpus.
    LANGUAGE_HALF = {'IR1': 'LA1', 'IR2': 'LA2'}

    def expected_total(self, unit):
        """What this unit's own asks should add up to, from printed totals."""
        total = self.unit_totals.get(unit)
        if total is None:
            return None
        if unit in self.unit_content:
            return self.unit_content[unit]
        other = self.LANGUAGE_HALF.get(unit)
        if other:
            share = self.unit_totals.get(other)
            if share:
                return total - share
        return total

    def checksum(self):
        """[(unit, printed total, the asks' own totals, ask count)]."""
        out = []
        for unit in sorted({a.unit for a in self.asks}):
            asks = [a for a in self.asks if a.unit == unit]
            got = sum(a.total for a in asks if a.total)
            out.append((unit, self.expected_total(unit), got, len(asks)))
        return out

    def reading(self):
        return [a for a in self.asks if a.unit in READING_UNITS]

    def ref(self, ask):
        return f'{self.year} {self.level.upper()} Section {ask.unit} {ask.label}'


READING_UNITS = {'C1', 'C2', 'IR1', 'IR2', 'CD'}
LISTENING_UNITS = {'L1', 'L2', 'L3', 'L4'}
# The units the scheme answers with a BAND GRID and nothing else.
BAND_UNITS = {'SE', 'GW', 'SA', 'EW'}
# A cue that has reached the end of its own sentence. Used to decide whether
# the next printed line continues a wrapped question or opens its answers.
CLOSED = re.compile(r'[.?:!\u2026]\s*$')


def _split_tariff(line):
    """(claim, per, total) where a line prints a whole task's split rate.

    "5x2 marks", "10 x 4 marks", "15 x 2 marks", "(5 x 2 marks)" — the form
    the SEC uses to price a table, a matching task or a gap-fill whole. A
    single "6 marks" is NOT one of these: it states a total and says nothing
    about how many answers reach it.
    """
    m = re.search(r'\(?\s*(\d{1,2})\s*[x\u00d7]\s*(\d{1,2})\s*marks?\s*\)?', line, re.I)
    if not m:
        return None
    n, per = int(m.group(1)), int(m.group(2))
    return (n, per, n * per)

# SEC misprints, keyed by the sitting, never repaired by a heuristic.
MISPRINTS = {}


def _sittings(subject=SUBJECT):
    out = []
    for name in sorted(os.listdir(schemes_dir(subject))):
        m = re.match(r'^(\d{4})-(hl|ol)\.md$', name)
        if m:
            out.append((int(m.group(1)), m.group(2)))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('year', nargs='?', type=int)
    ap.add_argument('level', nargs='?')
    ap.add_argument('--full', action='store_true')
    ap.add_argument('--audit', action='store_true')
    args = ap.parse_args()
    if args.audit:
        for year, level in _sittings():
            S = RuScheme(year, level)
            print(f'== {year} {level}')
            for unit, printed, got, n in S.checksum():
                flag = '' if printed in (None, got) else '   <-- DISAGREES'
                print(f'   {unit:4} printed {str(printed):>5}  asks {n:3} '
                      f'sum {got:5}{flag}')
        return 0
    S = RuScheme(args.year, args.level)
    for ask in S.asks:
        print(f'{ask.unit:4} {ask.label:10} {str(ask.notation):12} '
              f'total={ask.total} claim={ask.claim} per={ask.per} '
              f'{len(ask.answers)}a {len(ask.rungs)}r  {ask.cue[:70]}')
        if args.full:
            for t, m in ask.answers:
                print(f'        • {t}  [{m}]')
            for t, m in ask.rungs:
                print(f'        - {t}  [{m}]')
    return 0


if __name__ == '__main__':
    sys.exit(main())
