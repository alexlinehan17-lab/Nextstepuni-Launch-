#!/usr/bin/env python3
"""Read one Physical Education marking scheme into parts, tariffs and answers.

    python3 scripts/markbank/authoring/pe_scheme.py 2024 hl        # print parts
    python3 scripts/markbank/authoring/pe_scheme.py 2024 hl --raw  # print blocks

PE's scheme is a TWO-COLUMN TABLE, printed once per part: a "Description"
column of examiner-facing rows and a "Marks" column beside it.  Under the table
the examiner then prints, for many parts, the answers themselves — introduced
by the SEC's own lead-ins ("e.g.:", "Accept:", "Barriers may include:",
"Candidates may use words such as:") or set as bulleted or dashed lines.

That division is the whole subject.  A Description row states what the examiner
must SEE — "Clear and detailed explanation of the term related to physical
activities. 4" — and states no answer; the list under it states the answer:

    Barriers may include:
    -Facilities
    -Access
    -Finance

So a PE part is cardable exactly when the scheme prints such a list, or answers
inside a Description row itself ("Identifies axis as longitudinal (also accept
vertical/ mediolateral axis) 1 mark", "Correct plane named- 1 mark: Transverse
plane").  A part whose whole table is a band ladder and nothing else states
nothing a student could have written, and is refused rather than dressed up.

Nothing here decides what a card says.  It reports what the scheme prints, and
pe_all.py refuses whatever it cannot read one way.

LAYOUT DRIFT.  Thirteen sittings do not print the same page.

  * 2020 and 2021 do NOT reprint the ask.  A part opens "Question 3 (6 Marks)"
    and "(a)" and goes straight into the table, so there is no cue to align on
    and the pairing evidence has to come from the answer rows themselves (see
    pe_lib.pair).
  * 2022 hands back whole tables welded into ONE pymupdf block — "Question 6
    Description Marks Explanation of how two of the body's energy systems
    contribute to performance in chosen activity" — so a block is cut at the
    markers it holds, not taken whole.
  * 2023 onward reprints the ask above the table, which is a real cue.
  * 2026 glues the question head, the part marker and the ask into one block.

All four are read here; none is special-cased anywhere else.
"""
import os
import re
import sys

DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(DIR)))
SCHEMES = os.path.join(ROOT, 'examiner-reports', 'physical-education', 'schemes')

import pymupdf                                                  # noqa: E402

# "Question 12", "Question 13 (50 marks)", "Question 1 (8 marks)".
QHEAD = re.compile(r'^Question\s+(\d{1,2})\b\s*(?:\(\s*(\d{1,3})\s*marks?\s*\))?',
                   re.I)
# A part marker at the head of a run: "(a)", "a)", "(i)", "(a) (i)".
MARKER = re.compile(r'^\(?([a-h])\)|^\(?(i{1,3}|iv|vi{0,3}|ix|x)\)')
LETTER_TOKEN = re.compile(r'^\(?([a-h])\)\s*')
ROMAN_TOKEN = re.compile(r'^\(?(i{1,3}|iv|vi{0,3}|ix|x)\)\s*')
# The same markers found part way along a welded block.  Required to follow
# whitespace and to be followed by a capital, a further marker or a table
# heading, which is what keeps "(also accept vertical)" and "(2 x 2 marks)" out.
INLINE = re.compile(
    r'\s(?=Question\s+\d{1,2}\b)'
    r'|\s(?=\([a-h]\)\s*(?:\((?:i{1,3}|iv|vi{0,3})\)\s*)?(?:[A-Z(]|Description\b))'
    r'|\s(?=\((?:i{1,3}|iv|vi{0,3})\)\s*[A-Z(])')
# The table's own column heading, in the four spellings the corpus prints.
TABLE_HEAD = re.compile(r'^Description\s*(?:\d{1,2}\s*)?Marks?\b', re.I)
# Running page furniture.
FURNITURE = re.compile(
    r'^(?:Page\s*\|\s*\d+|Leaving Certificate|Coimisi|State Examinations'
    r'|Physical Education\s*[–-]|Marking Scheme|Section\s+[ABC]\b|\d{1,3}$'
    r'|Do not write|Answer any|Any \d+ questions|There are \d+ questions'
    r'|Note to teachers|Blank Page)', re.I)

# ------------------------------------------------------------- the tariff ---
# Every form below is the SEC's own printed arithmetic.  None is derived by
# dividing a total by a count the scheme did not state.
# "2 x 2 marks", and "2 x 2 (1+1) marks" — the SEC frequently prints the split
# of each answer INSIDE the group, and requiring "marks" to follow the second
# number immediately lost every one of those.
GROUP = re.compile(
    r'\b(\d{1,2})\s*(?:x|×)\s*(\d{1,2})\s*'
    r'(?:\(\s*\d{1,2}(?:\s*\+\s*\d{1,2})+\s*\)\s*)?marks?\b', re.I)
# The same arithmetic written in words and a rate: "Two principles of ethical
# practice identified – 1 m", "Three appropriate demands ... 2 marks". The
# count is the SEC's own and so is the rate; nothing is divided.
COUNTS = {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6}
COUNT_RATE = re.compile(
    r'\b(one|two|three|four|five|six)\b[^.]{0,70}?[–-]\s*(\d{1,2})\s*m\b'
    r'|\b(one|two|three|four|five|six)\b[^.]{0,70}?\s(\d{1,2})\s*marks?\b', re.I)
GROUP_PAREN = re.compile(r'\b(\d{1,2})\s*marks?\s*\(\s*x\s*(\d{1,2})\s*\)', re.I)
REPEAT = re.compile(r'\b(\d{1,2})\s*marks?(?:\s*\+\s*(\d{1,2})\s*marks?)+', re.I)
MARKS = re.compile(r'\b(\d{1,3})\s*marks?\b', re.I)
BAND_RANGE = re.compile(r'\b\d{1,2}\s*[-–]\s*\d{1,2}\s*(?:m\b|marks?\b)', re.I)

# A Description row that grades the same answer rather than stating one.  These
# are the bands: they price presentation, not content.
BAND_ROW = re.compile(
    r'^(?:very good|good|fair|poor|excellent|clear and (?:detailed|accurate)'
    r'|detailed and accurate|some (?:accuracy|level|degree|of the)'
    r'|somewhat accurate|mostly accurate|little detail|accurate and detailed'
    r'|information is|discussion lacks|brief |limited )', re.I)

# The SEC's own lead-ins to a list of answers.  Everything after one of these,
# to the end of the part, is the answer the examiner published.
LEAD_IN = re.compile(
    r'^(?:e\.?\s?g\.?\s*[:.]?$|eg\.?\s*[:.]?$|accept\s*[:.]?$'
    r'|accept any of the following\s*[:.]?$'
    r'|candidates? (?:may|might|to) [^.]*?(?:include|use|answer)[^.]*[:.]?$'
    r'|[A-Z][^.?!]{0,70}\bmay include\s*[:.]?$'
    r'|[A-Z][^.?!]{0,70}\bmay be\s*[:.]?$'
    r'|[A-Z][^.?!]{0,70}\binclude\s*[:.]?$'
    r'|possible candidate response\s*[:.]?$'
    r'|(?:strategies|barriers|factors|examples?|methods?|reasons?|benefits?'
    r'|advantages?|disadvantages?|supports?|answers?|responses?|criteria'
    r'|aspects?)\s+(?:may|might|could)\s+include\s*[:.]?$)', re.I)
# The same lead-in printed at the head of its own list on one line:
# "Accept: continuous training; weight training; plyometrics".
# The punctuation after "e.g" is NOT reliable and must not be required: 2024
# Ordinary prints "e.g Game day ear pieces; Concurrent feedback, Instinct lost"
# and "e.g anabolic agents; peptide hormones ..." with no colon and no full
# stop at all. Demanding one read that whole sitting as band-only — eight
# stated lists thrown away, and the level's share reported at 10% when it is
# 48%. The lead-ins themselves were taken from the corpus, not guessed: "e.g"
# 52 times, "example" 11, "accept" 8, "Possible candidate response" 6.
LEAD_IN_INLINE = re.compile(
    r'^(?:e\.?\s?g\.?|eg\.?|accept|accept any of the following'
    r'|possible candidate response|possible responses?|suggested responses?)'
    r'\s*[:.]?\s+(?=\S)', re.I)
# And the same lead-in printed PART WAY ALONG a row, which is how 2022 sets
# every one of its lists: "Correctly identifies a characteristic of skilled
# performance Eg. Kinaesthetic awareness, Anticipation, Consistency". The row
# before it is the criterion; everything after it is the SEC's own answer.
LEAD_IN_MID = re.compile(
    r'\s(?:e\.?\s?g\.?|eg\.?|possible candidate response)\s*[:.]?\s+(?=[A-Za-z])',
    re.I)
BULLET = re.compile('^[ \t]*[-•·▪‣●→–][ \t]*')
# An instruction to the examiner rather than an answer. It is printed inside
# the table and reads like content — "Note: type of feedback explained must be
# appropriate for an athlete with a visual impairment" — but it states a
# CONDITION on the answer, not the answer itself.
EXAMINER_NOTE = re.compile(
    r'^(?:note\b|n\.b\.|award\b|marks? (?:awarded|available)|do not\b'
    r'|no marks?\b|max(?:imum)?\b|accept any (?:valid|other|reasonable)\b'
    r'|candidates? (?:must|should|may not)\b|examiners?\b|if the\b)', re.I)


def tidy(s):
    return ' '.join((s or '').split())


class Part:
    """One printed part of one scheme, in document order."""

    def __init__(self, index, q, letter, roman, total):
        self.index = index
        self.address = (q, letter, roman)
        self.total = total
        self.cue = ''
        self.rows = []          # Description-column rows, in printed order
        self.answers = []       # stated answers the examiner published
        self.tariffs = []       # every printed tariff, in order

    @property
    def key(self):
        return self.address

    def __repr__(self):
        q, l, r = self.address
        label = f'Q{q}' + (f'({l})' if l else '') + (f'({r})' if r else '')
        return (f'<{label} total={self.total} rows={len(self.rows)} '
                f'answers={len(self.answers)}>')


def blocks(year, level):
    """The scheme's text blocks, in reading order, cut at inline markers."""
    pdf = os.path.join(SCHEMES, f'{year}-{level}.pdf')
    out = []
    with pymupdf.open(pdf) as doc:
        for n in range(doc.page_count):
            for b in sorted(doc[n].get_text('blocks'),
                            key=lambda b: (round(b[1], 1), b[0])):
                text = tidy(b[4])
                if not text:
                    continue
                for piece in INLINE.split(text):
                    piece = tidy(piece)
                    if piece:
                        out.append(piece)
    return out


def _start_at(chunks):
    """Skip the scheme's front matter.

    Every PE scheme opens with three pages of notes to teachers, and those
    pages carry no "Question N" head at all — so the first one is the boundary
    and nothing has to be guessed about the preamble's numbering.
    """
    for i, text in enumerate(chunks):
        if QHEAD.match(text):
            return i
    return len(chunks)


def _split_markers(text):
    """('a', 'i', rest) for a chunk opening with part markers."""
    letter = roman = None
    m = LETTER_TOKEN.match(text)
    if m:
        letter, text = m.group(1), text[m.end():]
    m = ROMAN_TOKEN.match(text)
    if m:
        roman, text = m.group(1), text[m.end():]
    return letter, roman, tidy(text)


def _add(part, text):
    """File one line of a part's table as a row or as a stated answer.

    Every branch of the walk goes through here. It did not, once: the branch
    that opens a table — "Description Marks Identifies 4 interpersonal skills
    desirable for effective coaching 8marks Interpersonal skill identified Eg.
    Communication ..." is ONE pymupdf block in 2022 — appended its remainder
    straight to the rows, so the "Eg." list welded into that block was never
    seen and the whole sitting reported 15% stated.
    """
    text = tidy(text)
    if not text:
        return False
    inline = LEAD_IN_INLINE.match(text)
    if inline:
        part.answers.append(tidy(text[inline.end():]))
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
    part.rows.append(text)
    return False


def _tariffs(text):
    """Every printed tariff in one line, as (claim, per) or (1, total)."""
    out = []
    for m in GROUP.finditer(text):
        out.append((int(m.group(1)), int(m.group(2))))
    for m in GROUP_PAREN.finditer(text):
        out.append((int(m.group(2)), int(m.group(1))))
    for m in REPEAT.finditer(text):
        values = [int(x) for x in re.findall(r'(\d{1,2})\s*marks?', m.group(0), re.I)]
        if len(values) > 1 and len(set(values)) == 1:
            out.append((len(values), values[0]))
    return out


def read(year, level):
    """Every part the scheme prints, in document order."""
    chunks = blocks(year, level)
    parts, index = [], 0
    q = letter = roman = None
    total = None
    part = None
    in_table = False
    pending_answers = False

    def open_part(qn, lt, rm, tot):
        nonlocal part, index, in_table, pending_answers
        part = Part(index, qn, lt, rm, tot)
        index += 1
        parts.append(part)
        in_table = False
        pending_answers = False
        return part

    for text in chunks[_start_at(chunks):]:
        if FURNITURE.match(text):
            continue

        head = QHEAD.match(text)
        if head:
            q = int(head.group(1))
            total = int(head.group(2)) if head.group(2) else None
            letter = roman = None
            rest = tidy(text[head.end():])
            lt, rm, rest = _split_markers(rest)
            letter, roman = lt, rm
            part = open_part(q, letter, roman, total)
            if rest and not TABLE_HEAD.match(rest):
                part.cue = rest
            elif rest:
                in_table = True
            continue

        if q is None:
            continue

        if MARKER.match(text):
            lt, rm, rest = _split_markers(text)
            if lt:
                letter, roman = lt, rm
            elif rm:
                roman = rm
            part = open_part(q, letter, roman, total)
            if rest and TABLE_HEAD.match(rest):
                in_table = True
                rest = tidy(rest[TABLE_HEAD.match(rest).end():])
            if rest:
                if in_table:
                    _add(part, rest)
                else:
                    part.cue = rest
            continue

        if part is None:
            part = open_part(q, letter, roman, total)

        if TABLE_HEAD.match(text):
            in_table = True
            rest = tidy(text[TABLE_HEAD.match(text).end():])
            if rest:
                _add(part, rest)
            continue

        if not in_table and not part.cue:
            part.cue = text
            continue

        # Inside the table.  A lead-in opens the answer list; everything after
        # it belongs to the answers, as do bullets wherever they appear.
        if LEAD_IN.match(text):
            pending_answers = True
            part.rows.append(text)
            continue
        if LEAD_IN_INLINE.match(text) or BULLET.match(text):
            pending_answers = True
            _add(part, text)
            continue
        if pending_answers:
            part.answers.append(text)
            continue
        _add(part, text)

    for p in parts:
        p.tariffs = [t for row in p.rows + p.answers for t in _tariffs(row)]
        # The count-and-rate form is a FALLBACK, read only where the part
        # prints no explicit group. Read alongside one it manufactured a
        # second, different tariff out of the same sentence and made every
        # such part ambiguous — one card lost for each one it found.
        if not p.tariffs:
            for row in p.rows + p.answers:
                m = COUNT_RATE.search(row)
                if not m:
                    continue
                word = (m.group(1) or m.group(3) or '').lower()
                rate = int(m.group(2) or m.group(4))
                if word in COUNTS and rate:
                    p.tariffs.append((COUNTS[word], rate))
                    break
    # A question head that opens nothing — "Question 3 (6 Marks)" immediately
    # followed by "(a)" — is furniture, not a part. Kept as a part it would
    # report a phantom band-only ask per lettered question in every sitting.
    return [p for p in parts if p.rows or p.answers or p.cue]


def band_only(part):
    """True where every priced row grades an answer and none states one."""
    if part.answers:
        return False
    for row in part.rows:
        if TABLE_HEAD.match(row) or LEAD_IN.match(row):
            continue
        if BAND_ROW.match(row) or BAND_RANGE.search(row):
            continue
        if stated(row):
            return False
    return True


# What a Description row states, where it states anything: the SEC prints the
# answer after a colon or a dash inside the row itself.  "Identifies axis as
# longitudinal (also accept vertical/ mediolateral axis) 1 mark" is the answer;
# "Identifies test to measure flexibility 1 mark" is not.
# The separator is matched but never CONSUMED past itself: an early version
# used "[-–]\s*[A-Z]" and ate the capital, shipping "oad – javelin" where the
# scheme printed "Load – javelin".
STATED = re.compile(
    r'(?::\s*|\bas\s+|\b(?:also\s+)?accept\s+|\bsuch as\s+|\bincluding\s+)'
    r'(?P<body>[^:]{4,})$', re.I)
# An examiner-facing verb with nothing after it but its own tariff.
CRITERION = re.compile(
    r'^(?:identifies|identify|explains?|explanation|describes?|description'
    r'|discusses?|discussion|outlines?|outline|names?|states?|statement'
    r'|defines?|definition|correct|accurate|appropriate|two|three|four|five'
    r'|candidate|award|marks?)\b', re.I)


def stated(row):
    """The answer a Description row states, or ''.

    The test is whether anything survives once the row's examiner-facing lead
    and its tariff are taken off, and whether what survives reads as content
    rather than as a second criterion.
    """
    text = tidy(row)
    if (TABLE_HEAD.match(text) or BAND_ROW.match(text) or BAND_RANGE.search(text)
            or EXAMINER_NOTE.match(text)):
        return ''
    m = STATED.search(MARKS.sub('', text).strip(' .;:,-'))
    if not m:
        return ''
    body = tidy(m.group('body')).strip(' .;:,-')
    if len(body) < 4 or CRITERION.match(body):
        return ''
    return body


if __name__ == '__main__':
    year, level = int(sys.argv[1]), sys.argv[2]
    if '--raw' in sys.argv:
        for text in blocks(year, level):
            print(repr(text[:160]))
        raise SystemExit
    parts = read(year, level)
    print(f'{year} {level.upper()}: {len(parts)} part(s)')
    for p in parts:
        flag = 'BAND-ONLY' if band_only(p) else ''
        print(f'  {p!r} {flag}')
        if p.cue:
            print(f'      cue: {p.cue[:110]}')
        for row in p.rows:
            said = stated(row)
            print(f'      row: {row[:110]}' + (f'   >>{said[:60]}' if said else ''))
        for a in p.answers:
            print(f'      ANS: {a[:110]}')
