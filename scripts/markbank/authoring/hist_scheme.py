#!/usr/bin/env python3
"""History marking schemes — what the SEC states, and what it only bands.

    python3 scripts/markbank/authoring/hist_scheme.py 2021 hl lm

ONE DOCUMENT, TWO FIELDS OF STUDY
---------------------------------
The SEC publishes ONE scheme per year and level, and it answers BOTH fields:
"LEAVING CERTIFICATE 2021 / MARKING SCHEME / HISTORY / LATER MODERN" opens the
first half and the same title page with EARLY MODERN opens the second. The two
halves address their asks identically — "Section 1 ... 1. Comprehension ...
(a)", "Ireland: Topic 1 ... A1." — so reading the file whole would key each ask
twice and hand the Early Modern paper the Later Modern answers. The reader
splits on those title pages and returns one field.

WHAT THE SCHEME ACTUALLY STATES
-------------------------------
Two things, and they are not the same kind of thing:

*Stated answers.* The DBQ's comprehension parts get a flat right-hand tariff
list — "(a) To fight desegregation/maintain segregation 5M". The DBQ's
comparison and criticism parts get the examiner's own model answer, a lead
statement and then either bullets or a paragraph per document, priced 10M on
the ask with no per-point split. Ordinary Level's Part A gets five one-line
answers at (6) each. All of those are liftable.

*Bands.* Every essay on the paper — Higher Level's Sections 2 and 3, Ordinary
Level's parts B and C, and the DBQ's contextualisation part — is answered with
nothing but a ceiling: "Max. CM = 60 Max. OE = 40". There is no content to
lift, and none is invented: those asks are EXCLUDED, with that line as the
evidence, in exclusions/history.json.

THE BAND GRID IS DISCARDED, and audit() asserts it. The grid's rows are wordy
enough to survive any prose-length test — "Excellent: 11-12 marks Outstanding
piece of analysis, exposition or commentary" — and stage 0 counted 391 of them
as stated answers. Not one reaches a card.

THE TARIFF IS NEVER GUESSED. A comprehension part carries its own printed
marks and the card states them; a comparison or criticism part carries one
printed total and no split, so the card is `questionTotal` and its rows carry
`marks: null`. Nothing here divides a total the SEC left whole.
"""
import argparse
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))


def scheme_path(year, level):
    return os.path.join(ROOT, 'examiner-reports', 'history', 'schemes',
                        f'{year}-{level}.md')


# The two title pages that divide the document. They are printed alone on their
# own page, in capitals in 2021 and in title case afterwards.
FIELD_TITLE = {'lm': re.compile(r'^(?:LATER MODERN|Later Modern)\s*$'),
               'em': re.compile(r'^(?:EARLY MODERN|Early Modern)\s*$')}
# append-scheme-columns.py appends a second rendering of the whole file for the
# provenance gate. It is the same content flattened, so reading it would double
# every ask.
APPENDED = re.compile(r'^<!--\s*markbank:')
PAGE_MARK = re.compile(r'^## Page \d+\s*$')

DBQ_START = re.compile(r'^Section 1:\s*DOCUMENTS-BASED QUESTION', re.I)
# Where the marking of the paper stops. Every scheme closes with the SEC's
# bonus-mark table for candidates answering through Irish, and it carries no
# marker of its own — so the last Part A answer of the 2024 and 2025 Early
# Modern schemes swallowed the whole appendix.
END_OF_SCHEME = re.compile(
    r'^(?:Coimisi[u\u00fa]n na Scr[u\u00fa]duithe St[a\u00e1]it'
    r'|Marcanna Breise|Bain [u\u00fa]s[a\u00e1]id as|Bunmharc)', re.I)
DBQ_HEAD = re.compile(
    r'^(\d)\.\s+(Comprehension|Comparison|Criticism|Contextualisation)\b'
    r'\s*\((\d{2})\s*marks\)')
SEC_HEAD = re.compile(r'^SECTION\s+([23])\s*:')
# "Ireland: Topic 1", "Ireland:Topic 6", "Ireland:  Topic 2" — the SEC's own
# spacing varies and one year drops the space after the colon entirely.
TOPIC_HEAD = re.compile(
    r'^(Ireland|Europe and the wider world)\s*:\s*Topic\s+(\d)\b', re.I)
# A Higher Level essay: the whole scheme entry for a 100-mark question.
ESSAY = re.compile(r'^(\d)\.\s+Max\.?\s*CM\s*=?\s*(\d+)\s+Max\.?\s*OE\s*=?\s*(\d+)')
# The note the scheme prints under an essay's ceiling: "NOTE: TWO elements
# (during + after) If only ONE, Max. CM = 50". 2021 wraps its "If only ONE"
# clause onto a line of its own, and 2025 opens one NOTE with a stray "(".
NOTE_HEAD = re.compile(r'^\(?NOTE\s*:', re.I)
NOTE_CONT = re.compile(r'^If only\b', re.I)
# A NOTE's own aside on a line of its own, between its head and its ceiling:
# "NOTE: TWO elements" / "(two of the GAA, the Gaelic League and/or W.B.
# Yeats)" / "If only ONE, Max. CM = 50" (2020 Higher).
NOTE_ASIDE = re.compile(r'^\([^()]*\)$')
NOTE_MAX = re.compile(r'\bMax\.?\s*CM\s*=\s*(\d+)')
# Every ceiling a NOTE prints, in its own words and order: "If only ONE, Max.
# CM = 40 If only TWO, Max. CM = 50" (2023) and "If only TWO, Max CM = 50 If
# only ONE, Max CM = 40" (2025 Early Modern) are two ceilings each.
# The count may carry its noun: "If only ONE former colony, Max. CM = 50"
# (2020 Higher, Europe Topic 5 Q3, whose NOTE is "colonies (plural)").
NOTE_CAP = re.compile(r'(If only (?:ONE|TWO|THREE|FOUR)(?: [a-z][\w-]*)*)\s*,\s*Max\.?\s*CM\s*=\s*(\d+)', re.I)
# An ANSWERED split: the scheme names each component of a part with its
# price, prints the answer under the component that needs one, and closes on
# the split and its total. 2020 Ordinary Q3(a) is
#     "Document A is a primary source = 5M" / "Reason = 5M" / "It is the
#     recollection/words of a North Vietnamese soldier ... etc. 5M + 5M 10M"
# A component printed with nothing under it is its own answer; one with lines
# under it is answered by them. It is recognised only when the closing split
# names exactly the components' prices, in order, and adds up to its total.
COMPONENT = re.compile(r'^([A-Z][^=]{0,80}?)\s*=\s*(\d{1,3})M$')
SPLIT_TOTAL = re.compile(r'(?:^|\s)((?:\d{1,3})M(?:\s*\+\s*\d{1,3}M)+)\s+(\d{1,3})M$')


def _answered_split(text):
    """(total, [(component, marks, answer or None), ...]) or None."""
    lines = [' '.join(t.split()) for t in text]
    if not lines:
        return None
    m = SPLIT_TOTAL.search(lines[-1])
    if not m:
        return None
    terms = [int(x) for x in re.findall(r'(\d{1,3})M', m.group(1))]
    total = int(m.group(2))
    if sum(terms) != total:
        return None
    last = lines[-1][:m.start()].strip()
    comps = []
    for line in lines[:-1] + ([last] if last else []):
        c = COMPONENT.match(line)
        if c:
            comps.append([c.group(1).strip(), int(c.group(2)), []])
        elif comps:
            comps[-1][2].append(line)
        else:
            return None
    if len(comps) < 2 or [marks for _n, marks, _a in comps] != terms:
        return None
    return total, [(name, marks, ' '.join(answer) or None)
                   for name, marks, answer in comps]


# An Ordinary Level Part A answer.
A_LINE = re.compile(r'^A(\d)\.\s*(.*)$')
# The whole scheme entry for an Ordinary Level part B or C.
BC_LINE = re.compile(r'^([BC])\s*-\s*Max\s*CM\s*=\s*(\d+)\s*marks?\s*'
                     r'Max\s*OE\s*=\s*(\d+)\s*marks?')
EXTRA_HEAD = re.compile(
    r'^Extra (?:Section|Part) A questions on page \d+ of the '
    r'exam(?:ination)? paper', re.I)
LETTER_HEAD = re.compile(r'^\(([a-f])\)\s*(.*)$')
# SEC misprints in a scheme's own lettering, keyed (year, level, field):
# {(question, printed letter): (the paper's letter, a word the answer must
# contain)}. The paper wins on the address; the word guards the relabel so
# it can never move an answer that is not the one described.
SCHEME_MISPRINTS = {
    # 2026 Higher Early Modern letters its Criticism parts "(c)" and "(d)",
    # running on from Comparison's (a) and (b). The paper prints Q3(a) "Would
    # you consider document A to be an objective source?" and Q3(b) "In what
    # ways is document B a useful source ...", and the scheme's (c) answers
    # whether doc A is "objective" and its (d) opens "Doc B is a useful
    # historical source on the Laois Offaly Plantation".
    (2026, 'hl', 'em'): {(3, 'c'): ('a', 'objective'), (3, 'd'): ('b', 'useful')},
}
BULLET = re.compile(r'^[•●▪·]\s*(.*)$')
TRAILING_M = re.compile(r'\s*(\d{1,3})M\s*(?:max)?\s*$', re.I)
# The ask's CEILING, wherever the SEC writes it: "Max = 10M", "max 10M",
# "Max. 5m". It is the authority on what a part is worth, because the flat
# figures beside it are the split ("5M + 5M") or a partial-credit rule ("If
# only one doc, max. 5m") rather than the total.
MAX_M = re.compile(r'\bmax\.?\s*=?\s*(\d{1,3})M\b', re.I)
TRAILING_PAREN = re.compile(r'\s*\((\d{1,3})\)\s*$')
DOC_PARA = re.compile(r'^(Doc(?:ument)?\s+[AB])\s*:\s*(.*)$', re.I)
PAGE_FOOTER = re.compile(r'^\d{1,3}$')
# The TITLE PAGE of the field that follows. Splitting the file on the "Early
# Modern" line leaves the three lines printed above it — "LEAVING CERTIFICATE
# 2024 / MARKING SCHEME / HISTORY" — at the end of the Later Modern half, where
# they landed inside the last Part A answer and the provenance gate dropped
# three cards. Also the bonus-mark banner the 2025 schemes print on the same
# page.
SCHEME_FURNITURE = re.compile(
    r'^(?:LEAVING CERTIFICATE \d{4}$|MARKING SCHEME$|HISTORY$'
    r'|(?:HIGHER|ORDINARY) LEVEL$|\d{3}@\d{1,2}%$)', re.I)

# The cue that introduces the examiner's own list. Everything after it is
# content; the sentence before it is the scheme's own summary answer.
CUE = re.compile(
    r'^(?:Answers?|Points?|Reasons?|Supporting points?|The answer|'
    r'Relevant points?|Possible points?|Such points?)\b[^.]*'
    r'(?:include|contain)\b.*:?\s*$', re.I)

# The marking APPARATUS: the band grid, the tariff arithmetic and the
# instructions to the examiner. None of it is an answer, and all of it survives
# any prose-length test — which is why stage 0 counted 391 grid rows as stated
# answers. Kept as notes on the ask, never as a marking point.
GRID_LINE = re.compile(
    r'^(?:Each document to be marked'
    r'|Mark (?:the )?quality of'
    # Every printing of the sliding-scale instruction across the ten schemes:
    # "Mark on a sliding scale", "Mark each document on a sliding scale out of
    # 5:", "Mark the answer on a sliding scale out of 10:". The Early Modern
    # half words it differently from the Later Modern half in the same file,
    # and the narrower list let four band grids run on into the answer rows.
    r'|Marks?\b[^.]{0,60}\bsliding scale\b'
    r'|Mark by the principle of Core Statement'
    r'|Assess (?:the )?answer on'
    r'|Excellent\s*[:=]|Very good\s*[:=]|Good\s*[:=]|Fair\s*[:=]'
    r'|Weak\s*[:=]|Poor\s*[:=]'
    r'|Reference to (?:both|only|ALL|BOTH)'
    r'|Answer referring to'
    r'|Look for (?:two|three|ONE|TWO)\b'
    r'|One reason, well explained'
    r'|Max\.?\s*=|Max\.?\s*CM|Max\.?\s*OE'
    r'|\d+M\s*\+\s*\d+M'
    r'|Note that the question is looking for'
    r'|A Core Statement may be defined'
    r'|To apply the principle'
    r'|Here, in question \d'
    r'|In question \d, marking by paragraph'
    # "One opinion = 5M", "Explanation = 5M": the scheme dividing the tariff
    # and stating no content at all. 2021 Ordinary Q3(b) is nothing but these
    # two lines, and it is excluded rather than carded.
    r'|[A-Z][\w \u2019\'-]{0,34}=\s*\d{1,3}M\b)', re.I)

# The wording that proves a row came out of the band grid rather than the
# answer. audit() asserts no shipped row contains any of it.
GRID_WORDS = re.compile(
    r'sliding scale|Max\.?\s*CM|Max\.?\s*OE|Cumulative Mark|Overall Evaluation'
    r'|Excellent\s*[:=]|Very good\s*[:=]|Weak\s*[:=]|paragraph equivalent'
    r'|Core Statement|\bmks\b|award \d+ marks?\b|marked on a', re.I)

# An examiner instruction the SEC prints on the SAME line as the answer:
# "Bombing of homes/... Any TWO; if only ONE, award 3 marks." The clause is
# not part of the answer and must not be recited to a student as one, so it is
# lifted off the row and kept as the row's contextNote.
INSTRUCTION_TAIL = re.compile(
    # The clause may sit in brackets, "Dental services/spectacles/drugs (any
    # two for 3m + 3m)": its opening bracket goes with it, not left on the row.
    r'\s*\(?(?:Any (?:TWO|THREE|ONE)\b[^.]*\.?'
    r'|If only (?:ONE|TWO)\b[^.]*\.?'
    r'|\(?(?:any )?(?:one|two) elements? only = \d+m\)?'
    r'|\(?any two,? \d+m \+ \d+m\)?'
    r'|\(?\d+m \+ \d+m\)?'
    # The split with no unit, "Because they were young and well-educated. (4 +
    # 4) 8M" (2019, 2020 Ordinary): only ever in its brackets.
    r'|\(\d+ \+ \d+\))\s*$', re.I)

# A sentence that instructs the EXAMINER rather than answering the question.
# The SEC sets these in the same paragraph as its model answer — "Accept A or B
# and mark on the quality of the answer. Answers could include points such
# as:" — so they survive the line-level grid filter and reach a row. A student
# reading "Evaluate the answer on the quality of the points made" has been told
# nothing about the history.
INSTRUCTION_POINT = re.compile(
    r'^(?:Mark\b|Marks\b|Evaluate the answer|Assess\b|Award\b'
    r'|Accept\b[^.]{0,60}\bmark\b'
    r'|Examiners?\b|Reference to (?:both|only|ALL|BOTH)'
    r'|Look for\b|Answers? (?:could|may|might) include'
    r'|Points? could include|The answer could contain)', re.I)

# A sentence that tells the candidate or the examiner what the answer must
# do, set inside the scheme's model answer: "Candidates should refer to the doc
# in their answers.", "A clear understanding of the meaning of 'objective' is
# necessary to gain marks in the very good to excellent range.", "Points should
# be supported by reference to doc B.", "Accept either primary or secondary
# provided a valid reason is given". It is the scheme's own direction, so it is
# kept, but on the row beside it as its note: a student cannot claim it.
INSTRUCTION_OPENING = (r'(?:Candidates should\b|Answers? should\b|A clear understanding of\b'
                       r'|Points should be supported\b|Comments on the limitations\b'
                       r'|Accept (?:answers|either|both|any)\b|Do not award\b'
                       r'|Mark (?:the )?quality of\b)')
INSTRUCTION_SENTENCE = re.compile('^' + INSTRUCTION_OPENING, re.I)
# Where an instruction follows a sentence ending in a capital ("... the early
# history of the GAA. Points should be supported ..."), the sentence splitter
# keeps the two together to protect initials; an instruction opening is never
# an initial, so it starts a sentence of its own.
INSTRUCTION_BREAK = re.compile(r'(?<=[.?!])\s+(?=' + INSTRUCTION_OPENING + ')')
# The same instruction printed with no full stop before the answer it heads:
# "Answers should use both documents to support their points Doc A says ..."
INSTRUCTION_RUN_ON = re.compile(
    r'^((?:Answers? should|Candidates should)\b[^.]*?)\s+(Doc(?:ument)?\s+[AB]\b.*)$')

# The document label the SEC prints at the END of a printed line rather than on
# one of its own — "...be kept within the city walls, etc. Doc B" in the 2023
# Early Modern scheme. Left in place it closes a marking row with the heading
# of the NEXT one.
TRAILING_DOC_LABEL = re.compile(r'\s+(Doc\.?(?:ument)?\s*[AB])\s*[:.]?\s*$')

# A document heading the scheme sets over its own bullets ("Document A:" on a
# line of its own). It says which document the points under it come from, so it
# rides on those rows as their contextNote rather than becoming a row itself.
DOC_HEAD = re.compile(r'^(Doc(?:ument)?\s+[AB])\s*:\s*$', re.I)

# The contents listing the Ordinary scheme prints before the DBQ itself.
DBQ_CONTENTS = re.compile(r'^There are four parts in the Documents-based question')

# A sentence boundary that is safe to split on: a full stop, question mark or
# closing quote followed by a capital. Initials ("E. D. Nixon"), "e.g." and
# "Doc A." are excluded, because splitting there would leave a fragment that
# is not a point.
SENTENCE = re.compile(
    r'(?<![A-Z])(?<!e\.g)(?<!i\.e)(?<!Doc)(?<!Mr)(?<!Mrs)(?<!Dr)(?<!St)'
    r'(?<!Fr)(?<!Rev)(?<!Prof)(?<!Sr)(?<!Co)(?<!No)'
    r'[.?!]["\u201d]?\s+(?=[A-Z\u201c"])')

# The years the SEC set ONE field of study. In 2020 it set no Early Modern
# paper at either level (paper_census.py declares that sitting absent, with
# its evidence), and its two schemes print LATER MODERN alone.
ONE_FIELD = {2020: 'lm'}


def _field_bounds(lines, field, year):
    """The first and last-plus-one line of one field of study's half."""
    starts = {}
    for key, pat in FIELD_TITLE.items():
        hits = [i for i, l in enumerate(lines) if pat.match(l.strip())]
        expected = 1 if ONE_FIELD.get(year, key) == key else 0
        if len(hits) != expected:
            raise AssertionError(
                f'{key}: expected {expected} "{pat.pattern}" title line(s), '
                f'found {len(hits)}')
        if hits:
            starts[key] = hits[0]
    if field not in starts:
        raise AssertionError(f'{year} prints no {field} field of study')
    if 'em' in starts and 'lm' in starts and starts['lm'] >= starts['em']:
        raise AssertionError('Early Modern is printed before Later Modern')
    lo = starts[field]
    hi = starts['em'] if field == 'lm' and 'em' in starts else len(lines)
    return lo, hi


def _halve(raw, field, year):
    """The lines of ONE field of study, in order."""
    lines = []
    for line in raw.split('\n'):
        if APPENDED.match(line):
            break
        lines.append(line.rstrip())
    lo, hi = _field_bounds(lines, field, year)
    return [l.strip() for l in lines[lo:hi]]


# Marking by paragraph (the essays and the documents question's Q4). A
# printed line that opens one of these starts a new logical line; any other
# line continues the one above it, because the SEC wraps a band's descriptor
# at the measure ("Excellent: 11-12 marks Outstanding piece of analysis,
# exposition or commentary." / "Clearly expressed, accurate and substantial
# information.").
# The head over Sections 2 and 3's marking: "Section 2 and Section 3:" (2021,
# 2022, 2024, 2025 Higher), "Section 2: IRELAND and" over "Section 3: EUROPE
# AND THE WIDER WORLD" (2023 Higher and Ordinary), "Section 2 and Section 3"
# with no colon (2021, 2022, 2024 Ordinary). Never the upper-case "SECTION 2:
# IRELAND" that heads the topic-by-topic notes.
S23_HEAD = re.compile(r'^Section 2(?: and Section 3)?\s*(?::|$)')
SPLIT_CEILING_CM = re.compile(r'^\d\.\s+Max\.?\s*CM\s*=?\s*\d+$')
SPLIT_CEILING_OE = re.compile(r'^Max\.?\s*OE\s*=?\s*\d+$')
# Q4's own account of what the question asks, printed in 2018 and 2019 between
# its head and "In question 4, marking by paragraph begins.": "There are two
# elements in this question:" and the elements under it, line by line. 2018
# also prints a ceiling for an answer treating one of them, "Max of 20 marks
# CM if only one element is treated", under the CM and OE maxima.
Q4_ELEMENTS = re.compile(r'^There are (?:two|three|TWO|THREE) elements in this question:$')
Q4_MARKING_BEGINS = re.compile(r'^In question 4, marking by paragraph begins\.$')
Q4_ELEMENT_CAP = re.compile(r'^Max of (\d+) marks CM (if only (?:one|ONE) element is treated)$')
# A line of the elements block that starts a new printed item: after a line
# that ends in a colon, a question mark or a full stop, and at and after a
# one-line definition "Name = ..." ("Entertaining = music, comedy, etc").
Q4_ITEM = re.compile(r'^[A-Z][\w ]{0,30} = ')


def _q4_elements(lines):
    """Q4's elements block, one printed item a line, and the ceiling it prints if any."""
    start = next((i for i, l in enumerate(lines) if Q4_ELEMENTS.match(l)), None)
    if start is None:
        return None, []
    end = next(i for i in range(start, len(lines)) if Q4_MARKING_BEGINS.match(lines[i]))
    items = []
    for line in lines[start:end]:
        if not line or PAGE_MARK.match(line) or PAGE_FOOTER.match(line):
            continue
        if (not items or re.search(r'[:?.]$', items[-1]) or Q4_ITEM.match(line)
                or Q4_ITEM.match(items[-1])):
            items.append(line)
        else:
            items[-1] = f'{items[-1]} {line}'
    caps = []
    for line in lines[end:]:
        m = Q4_ELEMENT_CAP.match(line)
        if m:
            items.append(line)
            caps.append((m.group(2), int(m.group(1))))
        if S23_HEAD.match(line):
            break
    return '\n'.join(' '.join(x.split()) for x in items), caps


PARAGRAPH_LEAD_RUN_ON = re.compile(
    r'(?<=\.) (?=The examiner will divide the answer into paragraphs or '
    r'paragraph equivalents:$)')
# Marking by Core Statement: the printed lines that open a new logical line.
CS_START = re.compile(
    r'^(?:•|\d\.\s+Contextualisation|Mark by the principle|A Core Statement may be'
    r'|To apply the principle|Here, in question 4|Note\b|[ABC]\.\s|Cumulative Mark\b'
    r'|Overall Evaluation\b|This is the total mark|In awarding\b|The marking of parts'
    r'|Each Topic is divided|LC 20\d\d:|(?:Excellent|Very good|Good|Fair|Poor|Weak|Very weak):\s*\d'
    r'|\(maximum:|IRELAND and|Section [23]\b|\(\d{3} marks\))')
PM_BAND = re.compile(
    r'^(Excellent|Very good|Good|Fair|Poor|Weak|Very weak):\s*(\d+)-(\d+)\s*(marks?)\b\s*(.*)$')
PM_CEILING = re.compile(
    r'^Cumulative Mark = Max\.? (\d+) marks Overall Evaluation = Max\.? (\d+) marks$')
PM_START = re.compile(
    r'^(?:(?:Excellent|Very good|Good|Fair|Poor|Weak|Very weak):\s*\d'
    r'|\((?:i|ii|iii|iv|v|vi|vii)\)\s|\(Summation\b|•'
    r'|Cumulative Mark\b|Overall Evaluation\b|Maximum (?:CM|OE)\b'
    r'|Marking the Answer|In awarding\b|Having divided\b|The examiner will\b'
    r'|A paragraph or paragraph equivalent|These marks are awarded'
    r'|To mark the answer|In Sections 2 and 3|In question 4\b'
    r'|This principle\b|The proportion\b|IRELAND and EUROPE'
    r'|Section [23]\b|\d\.\s+Contextualisation|Would you\b'
    r'|Max of \d+ marks CM\b)')


def _note_caps(ask):
    """Read the ceilings off an essay's NOTE as it stands."""
    ask.note_caps = [(' '.join(when.split()), int(top))
                     for when, top in NOTE_CAP.findall(ask.note)]
    ask.note_max = ask.note_caps[0][1] if ask.note_caps else None


def _sentences_kept(text):
    """The sentences of one point, each with its own closing punctuation."""
    out, start = [], 0
    for m in SENTENCE.finditer(text):
        cut = m.start() + len(m.group(0).rstrip())
        out.append(text[start:cut].strip())
        start = cut
    out.append(text[start:].strip())
    return [part.strip() for piece in out for part in INSTRUCTION_BREAK.split(piece) if part.strip()]


def _directions_to_notes(points):
    """Move instruction sentences off the rows, onto the note of the row beside them.

    A point that is nothing but instructions gives them to the previous row
    (the summary they qualify), or to the next where it comes first.
    """
    kept, waiting = [], []
    for label, point, note in points:
        m = INSTRUCTION_RUN_ON.match(point)
        lead = [m.group(1)] if m else []
        if m:
            point = m.group(2)
        sentences = _sentences_kept(point)
        directions = lead + [x for x in sentences if INSTRUCTION_SENTENCE.match(x)]
        answer = ' '.join(x for x in sentences if not INSTRUCTION_SENTENCE.match(x))
        # Joined as hist_all joins a row's notes, with " — ": the splitter
        # that cut these points took their closing stops with it.
        if not answer:
            if kept:
                l, p, n = kept[-1]
                kept[-1] = (l, p, ' — '.join(x for x in (n, *directions) if x))
            else:
                waiting.extend(directions)
            continue
        kept.append((label, answer, ' — '.join(x for x in (*waiting, *directions, note) if x) or None))
        waiting = []
    if waiting and kept:
        l, p, n = kept[-1]
        kept[-1] = (l, p, ' — '.join(x for x in (n, *waiting) if x))
    return kept


def _halve_pages(raw, field, year):
    """The scheme page of every line _halve() returns, in the same order.

    The same boundaries as _halve(), read again with the "## Page N" markers
    counted, so a card can open the scheme at the page its marking is printed
    on rather than at a page typed beside it.
    """
    page, pages, lines = 0, [], []
    for line in raw.split('\n'):
        if APPENDED.match(line):
            break
        lines.append(line.rstrip())
        m = re.match(r'^## Page (\d+)\s*$', line)
        if m:
            page = int(m.group(1))
        pages.append(page)
    lo, hi = _field_bounds(lines, field, year)
    return pages[lo:hi]


class Ask:
    """One priced ask the scheme answers, or bands."""

    def __init__(self, key, kind, total, notation):
        self.key = key          # (section, q, letter, roman) — the paper's key
        self.kind = kind        # 'stated' | 'banded'
        self.total = total
        self.notation = notation
        self.lead = ''
        self.points = []
        self.notes = []
        self.evidence = ''
        self.cue = ''           # the scheme's own words, for the Law 4 join
        self.note = None        # an essay's printed NOTE, verbatim
        self.note_max = None    # the first CM ceiling that NOTE prints
        self.note_caps = []     # every ceiling it prints: [("If only ONE", 50)]
        self.cm_max = self.oe_max = None   # an essay's printed maxima
        self.page = None        # the scheme page the ask is priced on

    def __repr__(self):
        return f'<Ask {self.key} {self.kind} {self.total} {len(self.points)}pt>'


class HistScheme:
    def __init__(self, year, level, field):
        self.year, self.level, self.field = year, level, field
        self.path = scheme_path(year, level)
        if not os.path.exists(self.path):
            raise FileNotFoundError(self.path)
        with open(self.path, encoding='utf-8') as fh:
            self.raw = fh.read()
        self.lines = _halve(self.raw, field, year)
        self.pages = _halve_pages(self.raw, field, year)
        assert len(self.pages) == len(self.lines)
        # 2018 prints an essay's ceiling over two lines, "1. Max. CM = 60" and
        # "Max. OE = 40". They are one entry: the second is joined onto the
        # first and its own line left blank, so line and page stay paired.
        for i in range(len(self.lines) - 1):
            if (SPLIT_CEILING_CM.match(self.lines[i])
                    and SPLIT_CEILING_OE.match(self.lines[i + 1])):
                self.lines[i] = f'{self.lines[i]} {self.lines[i + 1]}'
                self.lines[i + 1] = ''
        self.asks = []
        self.by_key = {}
        self.refused = []
        self.dbq_totals = {}
        self.dbq_names = {}
        self.topic_titles = {}
        self._read()

    # -- reading ---------------------------------------------------------
    def _read(self):
        section = None
        topic = None
        extra = False
        dbq_q = None
        started = False
        listing = 0             # the Ordinary DBQ contents block
        want_title = None       # the topic title line expected next
        cur = None              # the open lettered/numbered block
        buf = []

        def close():
            nonlocal cur, buf
            if cur is not None:
                self._finish(cur, buf)
            cur, buf = None, []

        essay = None            # the essay whose NOTE may follow
        for index, line in enumerate(self.lines):
            if (not line or PAGE_MARK.match(line) or PAGE_FOOTER.match(line)
                    or SCHEME_FURNITURE.match(line)):
                continue
            # An essay's NOTE is printed on the line under its ceiling. It was
            # never read before: nothing is open after an essay's ceiling, so
            # these lines fell through every pattern and were dropped. They are
            # consumed here and nowhere else changes.
            if essay is not None:
                if NOTE_HEAD.match(line) and essay.note is None:
                    essay.note = line
                    _note_caps(essay)
                    continue
                # The rest of a NOTE the SEC wrapped: its ceilings on the next
                # line ("If only ONE, ..." or "If only TWO, ..."), or the end of
                # a bracket it broke mid-way ("(Civil Constitution of the
                # Clergy + Committee of Public" / "Safety)").
                if (essay.note is not None and essay.note_max is None
                        and (NOTE_CONT.match(line) or NOTE_ASIDE.match(line)
                             or essay.note.count('(') > essay.note.count(')'))
                        and not ESSAY.match(line) and not TOPIC_HEAD.match(line)):
                    essay.note = f'{essay.note} {line}'
                    _note_caps(essay)
                    continue
                essay = None
            if END_OF_SCHEME.match(line):
                close()
                break
            if DBQ_START.match(line):
                close()
                started, section, topic, extra = True, '1', None, False
                continue
            if not started:
                continue
            if DBQ_CONTENTS.match(line):
                # "There are four parts in the Documents-based question:" is
                # followed by the four heads as a CONTENTS listing, and the
                # first real head repeats them. Read as heads they price four
                # asks the scheme has not answered yet, and 2021 Ordinary's
                # Q4 was keyed twice.
                listing = 4
                continue
            m = SEC_HEAD.match(line)
            if m:
                close()
                section, topic, extra, dbq_q = m.group(1), None, False, None
                continue
            m = TOPIC_HEAD.match(line)
            if m:
                close()
                topic, extra = int(m.group(2)), False
                if section == '1':
                    section = '2' if m.group(1).lower() == 'ireland' else '3'
                # The topic's printed TITLE follows on the next line, exactly
                # as it does on the paper. hist_all.py joins the two documents
                # on it.
                want_title = f'{section} Topic {topic}'
                continue
            if want_title:
                self.topic_titles[want_title] = line
                want_title = None
                continue
            if EXTRA_HEAD.match(line):
                close()
                extra, topic = True, None
                continue
            m = ESSAY.match(line)
            if m:
                close()
                ask = Ask((f'{section} Topic {topic}', int(m.group(1)),
                           None, None), 'banded',
                          int(m.group(2)) + int(m.group(3)), line)
                ask.evidence = line
                ask.page = self.pages[index]
                ask.cm_max, ask.oe_max = int(m.group(2)), int(m.group(3))
                self._add(ask)
                essay = ask
                continue
            m = BC_LINE.match(line)
            if m:
                close()
                ask = Ask((f'{section} Topic {topic} {m.group(1)}',
                           None, None, None), 'banded',
                          int(m.group(2)) + int(m.group(3)), line)
                ask.evidence = line
                ask.page = self.pages[index]
                ask.cm_max, ask.oe_max = int(m.group(2)), int(m.group(3))
                self._add(ask)
                continue
            m = A_LINE.match(line)
            if m and (topic is not None or extra):
                close()
                unit = 'Extra A' if extra else f'{section} Topic {topic} A'
                cur = Ask((unit, int(m.group(1)), None, None), 'stated',
                          None, '')
                buf = [m.group(2)]
                continue
            if section == '1':
                m = DBQ_HEAD.match(line)
                if m:
                    if listing:
                        listing -= 1
                        continue
                    close()
                    dbq_q = int(m.group(1))
                    self.dbq_totals[dbq_q] = int(m.group(3))
                    self.dbq_names[dbq_q] = m.group(2)
                    if m.group(2) == 'Contextualisation':
                        # The scheme's whole answer here is the paragraph-band
                        # apparatus: "Cumulative Mark = Max. 24 marks Overall
                        # Evaluation = Max 16 marks" at Higher, the Core
                        # Statement rules at Ordinary. Nothing is stated. The
                        # block is still READ, so the exclusion's evidence is
                        # what the SEC actually prints under the head rather
                        # than the head alone.
                        cur = Ask(('1', dbq_q, None, None), 'banded',
                                  int(m.group(3)), line)
                        cur.evidence = line
                        cur.page = self.pages[index]
                        buf = []
                    continue
                m = LETTER_HEAD.match(line)
                if m and dbq_q is not None:
                    close()
                    letter = m.group(1)
                    fix = SCHEME_MISPRINTS.get((self.year, self.level, self.field), {}).get((dbq_q, letter))
                    if fix:
                        letter = fix[0]
                    cur = Ask(('1', dbq_q, letter, None), 'stated',
                              None, '')
                    cur.misprint_word = fix[1] if fix else None
                    buf = [m.group(2)]
                    continue
            if cur is not None:
                buf.append(line)
        close()

    def _add(self, ask):
        word = getattr(ask, 'misprint_word', None)
        if word and word not in ' '.join(p for _l, p, _n in ask.points).lower() + ask.cue.lower():
            raise AssertionError(f'{self.year} {self.level} {self.field} {ask.key}: '
                                 f'relabelled scheme answer does not mention {word!r}')
        if ask.key in self.by_key:
            self.refused.append((ask.key, 'the scheme prices this ask twice'))
            return
        self.by_key[ask.key] = ask
        self.asks.append(ask)

    # -- one block -------------------------------------------------------
    def _tariff(self, lines, parent_total=None, lettered=False):
        """What the SEC prices this ask at, and the lines without the tariff.

        The ceiling wins where the scheme states one. "5M + 5M Max = 10M" is a
        split and a total on one line, and reading the first figure prices a
        ten-mark part at five; so does "Point with quote/explanation can earn
        5m", which is a partial-credit rule. The LAST ceiling on the block is
        the ask's own — a line may state a partial credit ("If only one doc,
        max. 5m") before the real total.

        The one ceiling that is NOT the ask's own is the comprehension
        question's recap: the Ordinary paper prints each part's "8M" and then
        "Max = 40M" under the last of them, which prices the QUESTION. It is
        recognised by being equal to the parent question's own printed total on
        a lettered part, never by position.
        """
        ceiling = None
        flat = None
        out = []
        for line in lines:
            for m in MAX_M.finditer(line):
                value = int(m.group(1))
                if lettered and parent_total is not None and value == parent_total:
                    continue
                ceiling = value
            m = TRAILING_M.search(line)
            if m:
                if flat is None:
                    flat = int(m.group(1))
                line = TRAILING_M.sub('', line)
            else:
                m = TRAILING_PAREN.search(line)
                if m and flat is None:
                    flat = int(m.group(1))
                    line = TRAILING_PAREN.sub('', line)
            out.append(line.strip())
        return (ceiling if ceiling is not None else flat), out

    def _finish(self, ask, buf):
        text = [t for t in buf if t.strip()]
        if ask.kind == 'banded':
            # Already known to be a ceiling; the block is kept as the printed
            # evidence for its exclusion, trimmed to what fits a ledger entry.
            ask.evidence = ' '.join(
                (ask.evidence + ' ' + ' '.join(text[:4])).split())[:400]
            self._add(ask)
            return
        if not text:
            self.refused.append((ask.key, 'the scheme states nothing here'))
            return
        split = _answered_split(text)
        if split:
            ask.kind = 'split'
            ask.total, ask.components = split
            ask.notation = ' '.join(SPLIT_TOTAL.search(' '.join(text[-1].split())).group(0).split())
            ask.evidence = ' '.join(' '.join(text).split())[:400]
            ask.points = [(None, answer or name, f'{name} = {marks}M' if answer else None)
                          for name, marks, answer in ask.components]
            ask.cue = ' '.join(' '.join(p for _l, p, _n in ask.points).split())
            self._add(ask)
            return
        # The grid is classified on the PRINTED line, before its tariff is
        # stripped: "One opinion = 5M" is the scheme dividing a total, and once
        # the 5M has been removed "One opinion =" no longer looks like it.
        grid = [bool(GRID_LINE.match(line)) for line in text]
        parent = (self.dbq_totals.get(ask.key[1]) if ask.key[0] == '1'
                  else None)
        ask.total, cleaned = self._tariff(
            text, parent, lettered=bool(ask.key[2]))
        ask.notation = f'{ask.total}M' if ask.total is not None else ''

        lead, points, notes = [], [], []
        doc = None              # the document heading currently in force
        mode = 'lead'
        for is_grid, line in zip(grid, cleaned):
            if not line:
                continue
            if is_grid:
                notes.append(line)
                mode = 'grid'
                continue
            if CUE.match(line):
                notes.append(line)
                mode = 'points'
                continue
            m = DOC_HEAD.match(line)
            if m:
                doc, mode = m.group(1), 'points'
                continue
            m = BULLET.match(line)
            if m:
                mode = 'points'
                points.append([doc, [m.group(1)], True])
                continue
            m = DOC_PARA.match(line)
            if m:
                mode = 'points'
                points.append([m.group(1), [m.group(2)], False])
                continue
            if mode == 'grid':
                notes.append(line)
                continue
            if mode == 'points' and points:
                points[-1][1].append(line)
                continue
            lead.append(line)

        ask.lead = ' '.join(' '.join(lead).split())
        ask.notes = [' '.join(n.split()) for n in notes]
        ask.points = []
        for label, chunk, bulleted in points:
            joined = ' '.join(' '.join(chunk).split())
            # A BULLET is already the scheme's own unit, however many sentences
            # the examiner wrote inside it — splitting one further is inventing
            # a segmentation the SEC did not make, and it took 2022 Higher
            # Q3(a) from the eleven bullets the scheme prints to twenty-three
            # rows, past the deck's own ceiling. Only a paragraph the scheme
            # left unsegmented is split.
            if bulleted:
                ask.points.append((label, joined))
                continue
            for piece in self._sentences(joined):
                ask.points.append((label, piece))
        if not ask.points and ask.lead:
            # A flat comprehension answer, or an Ordinary Part A answer: the
            # block IS the marking point, and stays whole because the SEC set
            # it as one line.
            if ask.total is not None and ask.total <= 8:
                ask.points = [(None, ask.lead)]
            else:
                ask.points = [(None, p) for p in self._sentences(ask.lead)]
            ask.lead = ''
        elif ask.lead:
            # The scheme's own summary answer, printed before its list.
            ask.points = [(None, p) for p in self._sentences(ask.lead)] + ask.points
            ask.lead = ''
        # An examiner instruction printed on the answer's own line is lifted
        # off the row and kept beside it.
        repaired = []
        for label, point in ask.points:
            m = TRAILING_DOC_LABEL.search(point)
            if m:
                doc_label = ' '.join(m.group(1).replace('.', '. ').split())
                point = point[:m.start()].strip()
                ask.notes.append(f'the next points are from {doc_label}')
            if INSTRUCTION_POINT.match(point):
                ask.notes.append(point)
                continue
            note = None
            m = INSTRUCTION_TAIL.search(point)
            if m and len(point) - len(m.group(0)) >= 12:
                note = m.group(0).strip()
                point = point[:m.start()].strip().rstrip(';,')
            repaired.append((label, point, note))
        ask.points = _directions_to_notes(repaired)
        ask.cue = ' '.join((' '.join(p for _l, p, _n in ask.points)).split())
        if not ask.points:
            # Nothing but tariff arithmetic under this head — 2021 Ordinary
            # Q3(b) is exactly "One opinion = 5M / Explanation = 5M / Max =
            # 10M". The evidence is the PRINTED block, not the notes the
            # tariff stripper has already taken the figures out of.
            ask.kind = 'banded'
            ask.evidence = ' '.join(' '.join(text).split())[:400]
        self._add(ask)

    @staticmethod
    def _sentences(text):
        """One paragraph as the sentences the examiner set out in it.

        Segmentation, never composition: no word changes and none is added.
        A comparison or criticism answer is printed as a paragraph per
        document — "Police were told to \u201cbreak up\u201d the boycotter car pools...
        Also, all black people waiting for lifts were to be charged with
        \u201cloitering\u201d." — and each of those sentences is a point the examiner
        credits. Left whole it is one 110-word row that no student can claim
        against. Short paragraphs stay whole.
        """
        text = text.strip()
        if len(text) <= 220:
            return [text] if text else []
        pieces, out = SENTENCE.split(text), []
        for piece in pieces:
            piece = piece.strip()
            if not piece:
                continue
            # A fragment shorter than this is not a point; it is the tail of
            # the sentence before it, and it goes back onto that row.
            if out and len(piece) < 30:
                out[-1] = f'{out[-1]} {piece}'
            else:
                out.append(piece)
        return out or [text]

    # -- marking by paragraph --------------------------------------------
    def paragraph_marking(self, unit):
        """The scheme's marking-by-paragraph apparatus for one essay unit.

        `unit` is 'q4' (the documents question's contextualisation part) or
        'essay' (a Section 2 or 3 essay). Every string returned is the
        scheme's own printing, its lines joined; nothing is composed. Read
        only for a paper being carded, so no other sitting's reading changes.

        Raises AssertionError naming what is missing: a ladder that cannot
        be read whole is not shipped in part.
        """
        if unit == 'q4':
            lo = next(i for i, l in enumerate(self.lines)
                      if re.match(r'^4\.\s+Contextualisation\b', l))
            hi = next(i for i in range(lo, len(self.lines))
                      if S23_HEAD.match(self.lines[i]))
        else:
            lo = next(i for i, l in enumerate(self.lines) if S23_HEAD.match(l))
            hi = next(i for i in range(lo, len(self.lines))
                      if SEC_HEAD.match(self.lines[i]))
        logical, pages = [], set()
        for i in range(lo, hi):
            line = self.lines[i]
            if (not line or PAGE_MARK.match(line) or PAGE_FOOTER.match(line)
                    or SCHEME_FURNITURE.match(line)):
                continue
            pages.add(self.pages[i])
            if not logical or PM_START.match(line):
                logical.append(line)
            else:
                logical[-1] = f'{logical[-1]} {line}'
        logical = [' '.join(l.split()) for l in logical]
        # 2017-2019 print the paragraph list's lead at the end of the "To mark
        # the answer ..." paragraph rather than on a line of its own: "...
        # which the syllabus demands. The examiner will divide the answer into
        # paragraphs or paragraph equivalents:". It is the same sentence, so it
        # is cut off at its own full stop and read as the lead.
        logical = [piece for text in logical
                   for piece in PARAGRAPH_LEAD_RUN_ON.split(text)]
        out = {'schemeGuidance': [], 'cm': {'bands': [], 'directions': [],
                                            'paragraphKinds': []},
               'oe': {'bands': [], 'directions': []}, 'pages': sorted(pages)}
        state = None
        for text in logical:
            m = PM_CEILING.match(text)
            if m:
                out['cm']['max'], out['oe']['max'] = int(m.group(1)), int(m.group(2))
                continue
            m = re.match(r'^Maximum (CM|OE) = (\d+) marks\.$', text)
            if m:
                out[m.group(1).lower()]['max'] = int(m.group(2))
                continue
            if re.match(r'^Cumulative Mark \(CM\)(?: \(Maximum = \d+ marks\))?$', text):
                state = 'cm'
                continue
            if re.match(r'^Overall Evaluation \(OE\)(?: \(Maximum = \d+ marks\))?$', text):
                state = 'oe'
                continue
            m = PM_BAND.match(text)
            if m and state in ('cm', 'oe'):
                band = {'label': m.group(1),
                        'marks': list(range(int(m.group(2)), int(m.group(3)) + 1)),
                        'printed': f'{m.group(1)}: {m.group(2)}-{m.group(3)} {m.group(4)}'}
                if m.group(5).strip():
                    band['descriptor'] = m.group(5).strip()
                out[state]['bands'].append(band)
                continue
            if re.match(r'^\((?:i|ii|iii|iv|v|vi|vii)\)\s', text):
                out['cm']['paragraphKinds'].append(text)
                continue
            if re.match(r'^\(Summation which is mere repetition', text):
                out['cm']['directions'].append(text)
                continue
            if re.match(r'^(?:A paragraph or paragraph equivalent may be one of the following:'
                        r'|The examiner will divide the answer into paragraphs or paragraph equivalents:)$',
                        text):
                out['cm']['paragraphLead'] = text
                continue
            if text.startswith('• ') and state == 'oe':
                out['oe']['directions'].append(text[2:])
                continue
            if re.match(r'^In awarding the OE, the examiner will evaluate', text):
                out['oe']['directionsLead'] = text
                continue
            if re.match(r'^In awarding OE, the examiner will consider', text):
                out['oe']['lead'] = text
                continue
            if re.match(r'^In awarding OE marks, the examiner should not expect', text):
                out['oe']['directions'].append(text)
                continue
            if re.match(r'^(?:These marks are awarded for historical content'
                        r'|Cumulative Mark \(CM\) for historical content)', text):
                out['cm']['definition'] = text
                continue
            if re.match(r'^Overall Evaluation \(OE\) for the quality of the answer', text):
                out['oe']['definition'] = text
                continue
            # How the scheme says the answer is marked: it prints no model
            # answer, and these are its own words for what it does instead.
            # The "open mind" sentence is printed under Sections 2 and 3 and
            # only an essay carries it; Q4 carries its own two sentences.
            if re.match(r'^(?:To mark the answer, the examiner will approach the material'
                        r'|In question 4, marking by paragraph begins'
                        r'|The examiner will divide the answer into paragraphs or paragraph equivalents\.$)',
                        text):
                out['schemeGuidance'].append(text)
                continue
        # The annotation the online marking panel uses for a paragraph past
        # the CM maximum. The flattened table on its page welds a column into
        # the sentence; the column-run rendering appended to the .md holds it
        # whole.
        m = re.search(r'Where an answer has already scored the maximum CMs '
                      r'allowable[^.]*?\(e\.g\.[^)]*\)\.', self.raw)
        if m:
            out['cm']['directions'].append(m.group(0))
        missing = [name for name, ok in (
            ('the CM maximum', 'max' in out['cm']),
            ('the OE maximum', 'max' in out['oe']),
            ('the CM definition', 'definition' in out['cm']),
            ('the paragraph list', len(out['cm']['paragraphKinds']) == 7
             and 'paragraphLead' in out['cm']),
            ('the CM bands', len(out['cm']['bands']) == 5),
            ('the OE bands', len(out['oe']['bands']) == 6),
            ("the scheme's own statement of how the answer is marked",
             bool(out['schemeGuidance']))) if not ok]
        if missing:
            raise AssertionError(f'{self.year} {self.level} {self.field} {unit}: '
                                 f'could not read {", ".join(missing)}')
        if unit == 'q4':
            out['elements'], out['elementCaps'] = _q4_elements(self.lines[lo:hi])
        return out

    # -- marking by Core Statement (Ordinary Level) -----------------------
    def core_statement_marking(self, unit):
        """The scheme's marking-by-Core-Statement apparatus for one unit.

        `unit` is 'q4' (the documents question's contextualisation part) or
        'B' / 'C' (an Ordinary topic's short and longer paragraph). Q4 is
        "Mark by the principle of Core Statement. Max = 20M" and has no OE;
        B and C are "marked by the principle of Core Statement, as defined
        above" with a CM ceiling and an OE grading table of their own, so the
        Core Statement definition and procedure are read off the Q4 block.
        Every string returned is the scheme's own printing, its lines joined.
        """
        heads = [i for i, l in enumerate(self.lines) if re.match(r'^4\.\s+Contextualisation\b', l)]
        if not heads:
            raise AssertionError(f'{self.year} {self.level} {self.field}: no Q4 head')
        q4_lo = heads[-1]          # the first is the scheme's contents listing
        q4_hi = next(i for i in range(q4_lo, len(self.lines)) if S23_HEAD.match(self.lines[i]))
        s23_hi = next(i for i in range(q4_hi, len(self.lines))
                      if re.match(r'^(?:Notes on individual topics|SECTION 2\s*:)', self.lines[i]))

        def logical(lo, hi):
            out, pages = [], set()
            for i in range(lo, hi):
                line = self.lines[i]
                if (not line or PAGE_MARK.match(line) or PAGE_FOOTER.match(line)
                        or SCHEME_FURNITURE.match(line)):
                    continue
                pages.add(self.pages[i])
                if not out or CS_START.match(line):
                    out.append(line)
                else:
                    out[-1] = f'{out[-1]} {line}'
            return [' '.join(l.split()) for l in out], pages

        q4, q4_pages = logical(q4_lo, q4_hi)
        cs = {'statementKinds': [], 'procedure': []}
        q4_notes, q4_guidance, ceiling = [], [], None
        mode = None
        # The head; a reprinted question (2022 on) joins onto it, since it opens
        # no logical line of its own.
        for text in q4[1:]:
            m = re.match(r'^Mark by the principle of Core Statement\.\s*Max\s*=\s*(\d+)M$', text)
            if m:
                ceiling = int(m.group(1))
                q4_guidance.append(text)
                continue
            if re.match(r'^A Core Statement may be defined as one of the following:$', text):
                cs['statementLead'], mode = text, 'kinds'
                continue
            if re.match(r'^To apply the principle of marking by Core Statement', text):
                cs['procedureLead'], mode = text, 'procedure'
                continue
            if text.startswith('• '):
                cs['statementKinds' if mode == 'kinds' else 'procedure'].append(text[2:])
                continue
            # "of the DBQ" (2021 on); 2020 spells it "of the Documents-based Question".
            if re.match(r'^Here, in question 4 of the (?:DBQ|Documents-based Question)\b', text):
                q4_guidance.append(text)
                continue
            if re.match(r'^Note\b', text):
                q4_notes.append(text)
                continue
            raise AssertionError(f'{self.year} {self.level} {self.field} q4: unread line {text!r}')
        per = [int(m.group(1)) for p in cs['procedure']
               for m in [re.search(r'Each completed Core Statement is awarded (\d+) marks', p)] if m]
        part = [(int(m.group(1)), int(m.group(2))) for p in cs['procedure']
                for m in [re.search(r'incomplete Core Statement at the end of an answer may merit (\d+)-(\d+) marks', p)] if m]
        if len(per) != 1 or len(part) != 1 or len(cs['statementKinds']) != 3 or ceiling is None:
            raise AssertionError(f'{self.year} {self.level} {self.field}: Core Statement procedure not read whole')
        cs['perStatement'] = per[0]
        cs['incomplete'] = list(range(part[0][0], part[0][1] + 1))
        if unit == 'q4':
            return {'cm': {**cs, 'max': ceiling, 'directions': q4_notes},
                    'schemeGuidance': q4_guidance, 'oe': None, 'pages': sorted(q4_pages)}

        s23, s23_pages = logical(q4_hi, s23_hi)
        out = {'cm': {**cs, 'directions': []}, 'oe': {'bands': [], 'directions': []},
               'schemeGuidance': [], 'pages': sorted(s23_pages | q4_pages)}
        state = None
        for text in s23:
            m = re.match(rf'^{unit}\. This answer will be marked by the principle of Core Statement', text)
            if m:
                out['schemeGuidance'].append(text)
                mm = re.search(r'maximum Cumulative Mark of (\d+) will be allowed for Core Statements and a maximum of (\d+) marks', text)
                out['cm']['max'], out['oe']['max'] = int(mm.group(1)), int(mm.group(2))
                continue
            if re.match(r'^Cumulative Mark \(CM\)$', text):
                state = 'cm'
                continue
            if re.match(r'^Overall Evaluation \(OE\)$', text):
                state = 'oe'
                continue
            if state == 'cm' and re.match(r'^This is the total mark awarded for Core Statements', text):
                out['cm']['definition'] = text
                continue
            if state == 'oe' and re.match(r'^In awarding OE, the examiner will consider', text):
                out['oe']['lead'] = text
                continue
            m = PM_BAND.match(text)
            if m and state == 'oe':
                band = {'label': m.group(1), 'marks': list(range(int(m.group(2)), int(m.group(3)) + 1)),
                        'printed': f'{m.group(1)}: {m.group(2)}-{m.group(3)} {m.group(4)}'}
                if m.group(5).strip():
                    band['descriptor'] = m.group(5).strip()
                out['oe']['bands'].append(band)
                continue
            if re.match(r'^In awarding both CM and OE, the examiner will approach the material with an open mind', text):
                out['schemeGuidance'].append(text)
                continue
        missing = [name for name, ok in (('the part\'s maxima', 'max' in out['cm']),
                                         ('the CM definition', 'definition' in out['cm']),
                                         ('the OE table', len(out['oe']['bands']) >= 4))
                   if not ok]
        if missing:
            raise AssertionError(f'{self.year} {self.level} {self.field} {unit}: could not read {", ".join(missing)}')
        return out

    # -- the assertion ---------------------------------------------------
    def audit(self):
        bad = [(a.key, p) for a in self.asks for _l, p, _n in a.points
               if GRID_WORDS.search(p)]
        return bad


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('year', type=int)
    ap.add_argument('level', choices=('hl', 'ol'))
    ap.add_argument('field', choices=('lm', 'em'))
    args = ap.parse_args()
    S = HistScheme(args.year, args.level, args.field)
    stated = [a for a in S.asks if a.kind == 'stated']
    banded = [a for a in S.asks if a.kind == 'banded']
    for a in S.asks:
        print(f'{str(a.key):<34} {a.kind:<7} total={a.total} '
              f'{len(a.points)}pt  '
              f'{(a.points[0][1] if a.points else a.evidence)[:80]}')
    print(f'{len(stated)} stated, {len(banded)} banded, '
          f'{len(S.refused)} refused')
    for key, why in S.refused[:10]:
        print(f'   REFUSED {key} {why}')
    bad = S.audit()
    print(f'band-grid leakage: {len(bad)}')
    for key, p in bad[:10]:
        print(f'   {key} {p[:90]}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
