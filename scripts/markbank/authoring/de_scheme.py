#!/usr/bin/env python3
"""German marking schemes — the priced answer, reached by walking a split.

    python3 scripts/markbank/authoring/de_scheme.py 2024 hl --full
    python3 scripts/markbank/authoring/de_scheme.py --audit

Why this is not fr_scheme.py
----------------------------
A French scheme prices an ask on the ask's own head — "1.(a) ……… 5 Marks" — and
states every accepted answer on a bulleted line carrying its own mark. A German
scheme does neither. It prints THREE LEVELS of head, and the tariff on each of
them is a SPLIT rather than a value:

    TEXT I: LESEVERSTÄNDNIS (60 marks) (14, 18, 18, 10)   <- the four questions
    Frage 1: (14 marks: (a) 6 marks; (b) 4 marks; (c) 4 marks)
    (a) (6 marks)
    Was erfahren Sie zu Beginn des Textes über den Autor?  (Zeile 1 – 9)
    (Any three: 3 x 2 marks)                              <- the leaf's own rate
    1. Er hat(te) ein glückliches Geheimnis.
    2. Er war vor (fast) 30 Jahren 24 Jahre alt.

So an ask's tariff is not printed beside the ask: it is reached by walking down
from the section head, and the reader has to carry each head's own arithmetic
to the leaf. Every level of that walk is CHECKED against the level above it —
`(14, 18, 18, 10)` must add to 60, `(a) 6; (b) 4; (c) 4` must add to 14, and
`3 x 2` must add to 6. A split that does not sum is a reader fault or an SEC
misprint, and averaging it would price a card at a number the SEC never wrote;
`--audit` prints every disagreement and the ask is refused rather than priced.

The answers are a NUMBERED LIST, not bullets, and the marks are on the rate
line above them rather than on each line, so the French "the mark on the line
decides" rule has nothing to decide here. What the rate line prints is kept in
printed ORDER, because German pays a DESCENDING ladder for a list — "(Any THREE
details: 7 marks: 3, 2, 2)" is three answers worth three, two and two, not
three worth 7/3 — and `MarkRow.group.perOptionSteps` exists for exactly that.

A leaf may also be printed in SEGMENTS. "How does Till feel and what does he do
after gamescom?" is one four-mark ask whose scheme prints "How:" over a two-mark
list and "What:" over another. Both are answered; they are not alternatives, so
they are not `route`s (which lock each other) but two marking rows of one card.

THE ANSWER LANGUAGE IS PART OF THE ASK, AND IT IS NOT A SUBJECT CONSTANT
------------------------------------------------------------------------
Within ONE reading comprehension, "Frage 1" is answered in German and
"Question 2" in English or Irish. The scheme says so twice over — in the head
word it chooses and in the language it reprints the question in — and it prices
the difference: "Answers in language not specified = half marks". So the
language rides on the ask (`Ask.language`), never on the subject.

WHAT IS NOT AN ANSWER
---------------------
Äußerung zum Thema and Schriftliche Produktion are read too, so their refusal
is counted rather than assumed: both are answered by a content/expression GRID
— "Content = 13 (A = 3; B = 4; C = 4; Dis. 2)", "Satz 1: 1 mark" — which prices
the candidate's own sentences and states no answer. So is the listening test,
whose only printed source is this same document's `Teil 1` transcript. See
de_all.py, which turns each into an exclusion quoting that evidence.
"""
import argparse
import glob
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))

SUBJECT = 'german'

WORD_COUNT = {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6,
              'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10, 'eleven': 11,
              'twelve': 12, 'fifteen': 15}


def schemes_dir(subject=SUBJECT):
    return os.path.join(ROOT, 'examiner-reports', subject, 'schemes')


# ------------------------------------------------------------- the units ----
# "TEXT I: LESEVERSTÄNDNIS (60 marks) (14, 18, 18, 10)" and, at Ordinary,
# "TEXT I: LESEVERSTÄNDNIS: (60 marks) (17, 22, 16, 5)" — the colon after the
# word is the Ordinary house style, in all five Ordinary sittings.
UNIT_LV = re.compile(
    r'^TEXT\s+(I{1,3}|[123])\s*:?\s*LESEVERST[ÄA]NDNIS\s*:?\s*'
    r'\((\d{1,3})(?:\s*marks?)?\)\s*(?:\(([^)]*)\))?', re.I)
# "TEXT I: ANGEWANDTE GRAMMATIK (25)" / "TEXT 1: ANGEWANDTE GRAMMATIK (15 marks)".
# The SEC sets the text number as a Roman numeral in some years and an Arabic
# digit in others, inside one document.
UNIT_AG = re.compile(
    r'^TEXT\s+(I{1,3}|[123])\s*:?\s*ANGEWANDTE\s+GRAMMATIK\s*:?\s*'
    r'\((\d{1,3})(?:\s*marks?)?\)', re.I)
UNIT_AT = re.compile(
    r'^TEXT\s+(I{1,3}|[123])\s*:?\s*[ÄA]U[ßSs]{1,2}ERUNG\s+ZUM\s+THEMA', re.I)
UNIT_SP = re.compile(r'^SCHRIFTLICHE\s+PRODUKTION', re.I)
UNIT_LISTEN = re.compile(r'^LISTENING\s+COMPREHENSION\s+TEST\s*:?\s*'
                         r'(?:\((\d{1,3})\s*marks?\s*:?\s*([^)]*)\))?', re.I)
# One part of the listening test: "First Part: Interview (22 marks: 8, 4, 2, 4, 4)".
# The SEC capitalises "Part" in some of the four and not others, every sitting.
LISTEN_PART = re.compile(
    r'^(First|Second|Third|Fourth|Fifth)\s+[Pp]art\s*:?\s*([^(]*)'
    r'(?:\((\d{1,3})\s*marks?\s*:?\s*([^)]*)\))?', re.I)
# Where the scheme stops marking and starts transcribing: the CD script, headed
# "Teil 1" / "Teil I". Reading past it would key the recording's own speaker
# turns as marking points — and hand a student the answers with the question.
TRANSCRIPT = re.compile(r'^Teil\s+(?:I{1,3}|[1-5])\b')
# Where a unit stops and the examiner's marking guidance begins. 2021 Ordinary
# sets "Guidelines for marking Expression in Äußerung zum Thema (a) and (b)…"
# between its last reading answer and the next section head, and a unit that
# ran to the next HEAD swallowed all of it: the answer "C" to the last
# multiple-choice item came out three hundred words long.
GUIDANCE = re.compile(
    r'^(?:Guidelines for marking|Marking Written Expression|'
    r'Marking (?:the )?Expression|[ÄA]u[ßs]{1,2}erung Or\b|'
    r'Reasonable Accommodations)', re.I)
PART_NAMES = {'first': 1, 'second': 2, 'third': 3, 'fourth': 4, 'fifth': 5}
TEXT_NUM = {'i': 1, 'ii': 2, 'iii': 3, '1': 1, '2': 2, '3': 3}

# ------------------------------------------------------------- the heads ----
# A question head, in the two forms the two levels print:
#   Higher    "Frage 1: (14 marks: (a) 6 marks; …)"  "Question 3: 11 marks: (a): 3 marks"
#   Ordinary  "1. (17 marks: (a) 6; …)"  "3. 2 marks"  "4. 6 marks: 3, 3"
# The head WORD is kept: "Frage" is the SEC saying this question is answered in
# German and "Question" that it is answered in English or Irish, and one
# comprehension uses both.
Q_HEAD_HL = re.compile(r'^(Frage|Question|Ceist)\s*(\d{1,2})\s*:?\s*'
                       r'(\(?\s*\d{1,3}\s*marks?\b.*)$', re.I)
Q_HEAD_OL = re.compile(r'^(\d{1,2})\s*\.\s*(\(?\s*\d{1,3}\s*marks?\b.*)$', re.I)
# A lettered head. Higher wraps its tariff in its own brackets — "(a) (6
# marks)" — Ordinary does not — "(a) 6 marks: (i) 4 marks, (ii) 2 marks)",
# whose trailing bracket is unbalanced in the SEC's own file — and 2023
# Ordinary prints no tariff on the head at all: "(a) Describe the origin of
# Bike-Polo. Give details. (Par. 3)", where the only price is the one the
# question head above it already stated. So the head is matched on the marker
# alone, and the letters of a split are consumed IN ORDER, which is what keeps
# a stray "(a)" inside another part's answers from opening a part.
L_HEAD = re.compile(r'^\(\s*([a-h])\s*\)\s*:?\s*(.*)$', re.I)
R_HEAD = re.compile(r'^\(\s*(i{1,3}|iv|vi{0,3}|v)\s*\)\s*(.*)$', re.I)
# An applied-grammar alternative: "1." or "2." opening the OR-choice. At Higher
# the question text comes first and the tariff two lines below it; at Ordinary
# the tariff is on the head. Both are read.
AG_HEAD = re.compile(r'^(\d)\s*\.\s*(.*)$')
AG_ITEM = re.compile(r'^\(\s*(\d{1,2}|i{1,3}|iv|vi{0,3}|v)\s*\)\s*(.+)$', re.I)

# A numbered answer line. The list restarts at 1 under every ask, so answers are
# only ever collected inside a block a head has closed.
ANSWER_NUM = re.compile(r'^(\d{1,2})\s*\.\s*(.*)$')
ANSWER_LETTER = re.compile(r'^\(\s*([a-z])\s*\)\s*(.+)$')
# The continuation the SEC prints for details sharing one opening: "2. … war
# sehr klein / hatte nur 30 Quadratmeter". The ellipsis stands in for the first
# answer's subject and is kept verbatim.
ELLIPSIS = re.compile(r'^[.…]{1,4}\s')
# The mark the SEC prints at the end of an answer line, in brackets: "1. Er
# zahlte wenig Miete. (2)". A line carrying one is its own answer even where
# the SEC did not number it — joining it to the line above welded a paragraph
# heading to its own English translation and priced the pair at one of the two.
TRAIL_MARK = re.compile(r'\s*\((\d{1,2})(?:\s*marks?)?\)\s*$', re.I)
# Any bracketed bare number anywhere in a line. Where one survives after the
# trailing mark is taken off, the mark was part of the ANSWER's own wording —
# "Three years (1) ago (1)" prices two elements of one answer — and taking it
# off would print a half-quoted answer.
INNER_MARK = re.compile(r'\((\d{1,2})(?:\s*marks?)?\)')
# An examiner's remark printed AFTER the mark, on the answer's own line: "A
# rebel 500 years ago (2) NB. '…for 500 years' is incorrect". It is an
# instruction, not part of the answer, and left attached it hid the mark that
# precedes it and cost the whole ask its tariff.
TAIL_NOTE = re.compile(r'(\(\d{1,2}(?:\s*marks?)?\))\s*((?:N\.?B\.?|Note|Allow|'
                       r'Accept|Penalise|Deduct)\b.*)$', re.I)

# The named halves of one ask: "How:" over a two-mark list, "What:" over
# another. Both are answered — they are not alternatives.
_LABEL = r'[A-Z][A-Za-z\u00c4\u00d6\u00dc\u00e4\u00f6\u00fc\u00df]{1,14}' \
         r'(?:\s+[a-z]{1,10})?'
# A segment label with a colon may carry its own answer on the same line:
# "Where: to the swimming pool (1)", "Wie lange: (etwas) mehr als ein Jahr
# (2 marks)".
SEGMENT = re.compile(rf'^({_LABEL})\s*:\s*(.*)$')
# A segment label written as a question — "Why? (2 marks)", "Where?" — may
# carry only its tariff. An ordinary sentence that happens to open with a
# capitalised word and a question mark is not a label, and 2021 Ordinary prints
# one inside its own answer list: "Texas? Without me! (2)" is the English of the
# paragraph heading above it, not a two-mark half of the ask.
SEGMENT_Q = re.compile(rf'^({_LABEL})\s*\?\s*:?\s*(.*)$')
# The Higher theme question lists its points under two headings and says on the
# paper that an answer may draw on either: "(Can be language use and/or
# content.)" So these label the list, they do not divide it.
SUBLIST = re.compile(r'^\(\s*(Content|Language use)\s*\)\s*$', re.I)
DIRECTIVE = re.compile(r'^(?:Allow|Accept|Either|Or)\s*:?\s*$', re.I)
NOTE = re.compile(r'^\(?\s*(?:N\.?B\.?|Note|Allow\b|Accept\b|Penalise|Deduct|'
                  r'Where answers|Answers in|Evidence needed|Quotation without|'
                  r'Award|Any three; no marks)\b'
                  r'|^\([^)]*\b(?:needed|required|only)\)\s*$', re.I)
PAGE = re.compile(r'^(?:##\s*Page\s*\d+\s*$|\d{1,3}\s*$)')
# Where a reprinted German reading question STOPS. Every one of them closes
# with the place in the text its answer is found — "(Zeile 1 – 9)", "(lines 30
# ‒ 37)", "(Par. 4)", "(Abschnitt 2)", "(Introduction)", "(Headline)" — and
# nothing else in the block does. Without it, an ask whose answer the SEC
# printed unnumbered ("(a) 3 marks" over one line of answer) kept the answer in
# the question and shipped a card with nothing to claim.
CUE_END = re.compile(
    r'\((?:Zeile[n]?|line|lines|l\.|Par\.|Absatz|Abschnitt|Introduction|'
    r'Einleitung|R[ée]amhr[áa]|Headline|Tipp|Schlagzeile)[^)]*\)\s*\??\s*$', re.I)
# The answer to a matching question, printed as the key alone: "2 d 3 a 4 c 5 f
# 6 b". Nothing else in a scheme block looks like this.
MATCH_KEY = re.compile(r'^(?:\d{1,2}\s*[-–—]?\s*[A-Fa-f](?:\s|$)[\s,]*){3,}$')
MATCH_PAIR = re.compile(r'(\d{1,2})\s*[-–—]?\s*([A-Fa-f])(?=\s|$)')
# The row of empty mark boxes an Ordinary matching question prints above its
# key: "(1) (1) (1) (1) (1)". It is the examiner's tally, not an answer.
MARK_BOXES = re.compile(r'^(?:\(\d{1,2}\)\s*){2,}$')

# "Any three", "Any THREE details", "Any 3" — the claim count, wherever the SEC
# puts it in the rate line.
ANY_N = re.compile(r'^(?:Plus\s+)?Any\s+(\w+)\s*'
                   r'(?:details?|examples?|points?|of)?\s*:?\s*', re.I)
# A rate spec, in every shape the ten schemes print.
SPEC_TIMES = re.compile(r'^(\d{1,2})\s*[x×]\s*(\d{1,2})(?:\s*marks?)?$', re.I)
SPEC_PLUS = re.compile(r'^\d{1,2}(?:\s*marks?)?(?:\s*\+\s*\d{1,2}(?:\s*marks?)?)+$', re.I)
SPEC_LIST = re.compile(r'^\d{1,2}(?:\s*,\s*\d{1,2})+(?:\s*marks?)?$', re.I)
SPEC_ONE = re.compile(r'^(\d{1,2})\s*marks?$', re.I)
# "(10 marks. 2 x 2 marks; 3 x 2 marks)" — the SEC separates a total from its
# spec with a colon almost always, a full stop once, and a semicolon once.
TOTAL_THEN = re.compile(r'^(\d{1,3}|\w+)\s*marks?\s*[:.;]\s*(.+)$', re.I)

# The words a reprinted question is written in. Both signals are read and they
# must agree; the reprint wins, because it is the ask itself.
GERMAN_WORDS = re.compile(
    r'\b(?:warum|wie|was|wer|welche[rsnm]?|wo|wann|beschreiben|nennen|geben|'
    r'schreiben|erkl[äa]ren|sie|der|die|das|des|dem|den|ein[ers]?|und|ist|'
    r'sind|hat|haben|f[üu]r|mit|von|auf|im|zu|nicht|dieser|diese[nsm]?|'
    r'passen|zusammen|s[äa]tze|details)\b', re.I)
ENGLISH_WORDS = re.compile(
    r'\b(?:what|how|why|who|which|where|when|describe|give|name|state|write|'
    r'mention|explain|details?|the|and|does|did|do|is|are|has|have|his|her|'
    r'their|about|from|for|with|according|list|choose)\b', re.I)


# ------------------------------------------------------------ the tariffs ---
def parse_spec(text):
    """A printed rate spec -> the per-answer marks it names, in printed order.

    Never a guess: an unrecognised spec returns None and the caller refuses the
    ask rather than pricing it. The spec is read as a list of TERMS separated by
    "+", "," or ";", because the SEC adds a fixed answer to a menu on one line
    and nests the brackets while doing it. Every shape below is printed:

        "3 x 2 marks"              three answers at two        [2, 2, 2]
        "2 + 2 marks"              two answers at two          [2, 2]
        "3, 2, 2"                  three, descending           [3, 2, 2]
        "7 marks: 3, 2, 2"         the same, with its total    [3, 2, 2]
        "2 marks"                  one answer at two           [2]
        "1 mark, 3 x 1 mark"       a fixed answer then three   [1, 1, 1, 1]
        "2 marks + (2 x 2) marks"  the same, bracketed         [2, 2, 2]
        "2 x 2 marks; 3 x 2 marks" two menus of one ask        [2, 2, 2, 2, 2]
    """
    s = ' '.join((text or '').split()).strip()
    while s.startswith('(') and s.endswith(')'):
        s = s[1:-1].strip()
    if not s:
        return None
    m = TOTAL_THEN.match(s)
    if m:
        total = _number(m.group(1))
        inner = parse_spec(ANY_N.sub('', m.group(2).strip(), count=1))
        if total is not None and inner is not None and sum(inner) == total:
            return inner
        return None
    # The brackets carry no meaning once the total is off: "2 marks + (2 x 2)
    # marks" and "2 marks + 2 x 2 marks" are the same tariff, and 2023 Higher
    # prints both within four lines of each other.
    s = s.replace('(', ' ').replace(')', ' ')
    out = []
    for term in re.split(r'\s*[+,;]\s*', s):
        term = term.strip()
        if not term:
            return None
        m = SPEC_TIMES.match(term)
        if m:
            out.extend([int(m.group(2))] * int(m.group(1)))
            continue
        m = SPEC_ONE.match(term)
        if m:
            out.append(int(m.group(1)))
            continue
        if re.fullmatch(r'\d{1,2}', term):
            out.append(int(term))
            continue
        return None
    return out or None


def _number(token):
    t = (token or '').strip().lower()
    if t.isdigit():
        return int(t)
    return WORD_COUNT.get(t)


def read_rate(text):
    """(steps, claimMax) for a printed rate line, or (None, None).

    The claim count and the per-answer values are printed separately and both
    are read, so that a line whose two halves disagree — "Any three: 2 x 5
    marks" would be one — is refused instead of being half believed.
    """
    s = ' '.join((text or '').split()).strip()
    while s.startswith('(') and s.endswith(')'):
        s = s[1:-1].strip()
    if not s:
        return None, None
    claimed = None
    m = ANY_N.match(s)
    if m:
        claimed = _number(m.group(1))
        if claimed is None:
            return None, None
        s = s[m.end():].strip()
        m2 = TOTAL_THEN.match(s)
        if m2 and _number(m2.group(1)) is not None:
            pass                       # parse_spec reads the total itself
    else:
        m2 = TOTAL_THEN.match(s)
        if m2:
            inner = m2.group(2).strip()
            m3 = ANY_N.match(inner)
            if m3:
                claimed = _number(m3.group(1))
                s = f'{m2.group(1)} marks: {inner[m3.end():].strip()}'
        elif not re.fullmatch(r'[\d\s,.;:x×+()]*(?:marks?[\d\s,.;:x×+()]*)*',
                              s, re.I):
            # A rate line holds nothing but numbers, the word "marks" and the
            # punctuation that joins them. One "marks" was not enough: 2023
            # Higher prints "(2 marks + (2 x 2) marks)" and its whole ask was
            # refused for want of a tariff it states twice over.
            return None, None
    if claimed is None and not re.search(r'marks?\b|[x×]', s, re.I):
        # A rate line always SAYS what it is: "Any three", "x", or the word
        # "marks". Without that test the row of blank mark boxes an Ordinary
        # matching question prints — "(1) (1) (1) (1) (1)" — read as a
        # one-answer tariff and took the ask's real 5 x 1 off it.
        return None, None
    steps = parse_spec(s)
    if steps is None:
        return None, None
    if claimed is not None and len(steps) != claimed:
        return None, None
    return steps, claimed or len(steps)


def read_rate_line(text):
    """(steps, claimMax, remark) for a whole printed line.

    The SEC sets an examiner's aside beside the rate — "(Any four: 4 x 1 mark)
    (Present Tense = 0)" — and a rate reader that will not tolerate it read the
    whole line as a marking point and offered "(Any four: 4 x 1 mark)" to a
    student as an answer.
    """
    s = ' '.join((text or '').split())
    got, cnt = read_rate(s)
    if got is not None:
        return got, cnt, None
    remark = []
    while True:
        m = re.search(r'\s*(\([^()]*\))\s*$', s)
        if not m:
            return None, None, None
        remark.insert(0, m.group(1))
        s = s[:m.start()].strip()
        if not s:
            return None, None, None
        got, cnt = read_rate(s)
        if got is not None:
            return got, cnt, ' '.join(remark)


def head_total(clause):
    """The total a head prints before its split: "(14 marks: …" -> 14."""
    m = re.match(r'^\s*\(?\s*(\d{1,3})\s*marks?\b', clause or '', re.I)
    return int(m.group(1)) if m else None


LETTER_TOK = re.compile(r'\(\s*([a-h])\s*\)|(?:^|[:;,(]\s*)([a-h])\s*:')
ROMAN_TOK = re.compile(r'\(\s*(i{1,3}|iv|vi{0,3}|v)\s*\)', re.I)
NUM_TOK = re.compile(r'(\d{1,3})')


def parse_head_clause(clause):
    """A head's own split: ({letter: marks}, {letter: {roman: marks}}).

    Scanned as a token stream rather than matched as a pattern, because the SEC
    nests one level inside the other on the same line and does it four ways in
    five sittings:

        "(14 marks: (a) 6 marks; (b) 4 marks; (c) 4 marks)"
        "(22 marks: (a) (i) 8 marks; (ii) 6 marks; (b) 8 marks)"
        "(18 marks: a: 4 marks; b: 6 marks; c: 8 marks)"
        "(17 marks: (a) 6; (b) 2; (c) 5; (d) 4)"

    A clause naming no letter is a LEAF question and returns ({}, {}): "(10
    marks: Any two: 2 x 5 marks)" prices one ask, not two lettered ones.
    """
    s = clause or ''
    m = re.match(r'^\s*\(?\s*\d{1,3}\s*marks?\s*', s, re.I)
    if m:
        s = s[m.end():]
    letters, romans = {}, {}
    cur_letter = cur_roman = None
    pos = 0
    pattern = re.compile(
        r'\(\s*(?P<let>[a-h])\s*\)|(?:^|[:;,(]\s*)(?P<let2>[a-h])\s*:'
        r'|\(\s*(?P<rom>i{1,3}|iv|vi{0,3}|v)\s*\)|(?P<num>\d{1,3})', re.I)
    for m in pattern.finditer(s):
        if m.group('let') or m.group('let2'):
            cur_letter = (m.group('let') or m.group('let2')).lower()
            cur_roman = None
            letters.setdefault(cur_letter, None)
        elif m.group('rom'):
            cur_roman = m.group('rom').lower()
        elif m.group('num'):
            if cur_letter is None:
                continue
            n = int(m.group('num'))
            if cur_roman is not None:
                romans.setdefault(cur_letter, {}).setdefault(cur_roman, n)
                cur_roman = None
            elif letters.get(cur_letter) is None:
                letters[cur_letter] = n
        pos = m.end()
    del pos
    for letter, kids in romans.items():
        if letters.get(letter) is None:
            letters[letter] = sum(kids.values())
    if any(v is None for v in letters.values()):
        return {}, {}
    return letters, romans


# SEC misprints, keyed by the sitting. Never repaired by a heuristic: each is a
# line whose own document contradicts it somewhere a person can read.
MISPRINTS = {
    # 2024 Higher prices TEXT I question 2 as "(a) 4 marks; (b) 14 marks" and
    # splits that 14 as "(i) 4; (ii) 6; (iii) 4" — but the PAPER prints no
    # 2(b)(iii). It prints 2(a), 2(b)(i), 2(b)(ii) and then a part of its own,
    # "(c) What are the results of this? Give details. (lines 67 ‒ 82)", and
    # the scheme reprints that question under that very marker four lines
    # below its own "(iii)". The paper wins: the third part is 2(c), worth the
    # 4 the scheme prices, and the question is 4 + 10 + 4.
    (2024, 'hl'): [
        ('Question 2: (18 marks: (a) 4 marks; (b) 14 marks) (Allow Present Tense)',
         'Question 2: (18 marks: (a) 4 marks; (b) 10 marks; (c) 4 marks) '
         '(Allow Present Tense)'),
        ('(b) (14 marks: (i) 4 marks; (ii) 6 marks; (iii) 4 marks)',
         '(b) (10 marks: (i) 4 marks; (ii) 6 marks)'),
    ],
    # The Ordinary applied-grammar alternative is priced "5 x 3 marks" — five
    # answers at three, which is fifteen — under a head that says five. The
    # paper heads the whole section "ANGEWANDTE GRAMMATIK (15)", the first
    # alternative beside it is "(15 marks: 15 x 1 mark)", and the 2021, 2022,
    # 2023 and 2025 Ordinary schemes all print "2. (15 marks: 5 x 3 marks)".
    (2024, 'ol'): [('2. (5 marks: 5 x 3 marks)', '2. (15 marks: 5 x 3 marks)')],
}


class Ask:
    """One leaf ask, exactly as the scheme prices it."""

    __slots__ = ('unit', 'q', 'letter', 'roman', 'total', 'segments', 'notation',
                 'cue', 'notes', 'language', 'line', 'head_word', 'exhaustive')

    def __init__(self, **kw):
        for k in self.__slots__:
            setattr(self, k, kw.get(k))

    @property
    def key(self):
        return (self.unit, self.q, self.letter, self.roman)

    @property
    def answers(self):
        return [a for seg in self.segments for a in seg['answers']]

    def __repr__(self):
        return f'<Ask {self.unit} {self.q}{self.letter or ""}{self.roman or ""}>'


class DeScheme:
    """One published German marking scheme, read as a list of priced leaves."""

    def __init__(self, year, level, subject=SUBJECT):
        self.year, self.level, self.subject = year, level, subject
        self.path = os.path.join(schemes_dir(subject), f'{year}-{level}.md')
        with open(self.path, encoding='utf-8') as fh:
            raw = fh.read()
        for old, new in MISPRINTS.get((year, level), ()):
            assert old in raw, f'{year} {level}: misprint {old!r} is not in the scheme'
            raw = raw.replace(old, new)
        self.lines = [l.rstrip() for l in raw.split('\n')]
        self.asks = []
        self.refused = []
        self.flags = []
        self.unit_totals = {}      # unit token -> the total it prints
        self.unit_splits = {}      # unit token -> [the question totals it prints]
        self.written = []          # ('AT'|'SP', line, head) — read, never carded
        self._read()

    # -- segmentation -------------------------------------------------------
    def _segments(self):
        """[(unit token, head line, end line)] over the whole document."""
        marks = []
        stop = len(self.lines)
        seen_listening = False
        for i, line in enumerate(self.lines):
            s = line.strip()
            if not s:
                continue
            if seen_listening and TRANSCRIPT.match(s):
                stop = i
                break
            m = UNIT_LV.match(s)
            if m:
                unit = f'T{TEXT_NUM[m.group(1).lower()]}'
                self.unit_totals[unit] = int(m.group(2))
                if m.group(3):
                    self.unit_splits[unit] = [
                        int(n) for n in re.findall(r'\d{1,3}', m.group(3))]
                marks.append((unit, i))
                continue
            m = UNIT_AG.match(s)
            if m:
                self.unit_totals['AG'] = int(m.group(2))
                marks.append(('AG', i))
                continue
            if UNIT_AT.match(s):
                marks.append(('AT', i))
                continue
            if UNIT_SP.match(s):
                marks.append(('SP', i))
                continue
            if GUIDANCE.match(s):
                marks.append(('GUIDE', i))
                continue
            m = UNIT_LISTEN.match(s)
            if m:
                seen_listening = True
                if m.group(1):
                    self.unit_totals['L'] = int(m.group(1))
                marks.append(('L', i))
                continue
            if seen_listening:
                m = LISTEN_PART.match(s)
                if m:
                    unit = f'L{PART_NAMES[m.group(1).lower()]}'
                    if m.group(3):
                        self.unit_totals[unit] = int(m.group(3))
                        self.unit_splits[unit] = [
                            int(n) for n in re.findall(r'\d{1,3}', m.group(4) or '')]
                    marks.append((unit, i))
        out = []
        for n, (unit, i) in enumerate(marks):
            end = marks[n + 1][1] if n + 1 < len(marks) else stop
            if i < stop:
                out.append((unit, i, min(end, stop)))
        return out

    def _read(self):
        for unit, start, end in self._segments():
            body = self.lines[start + 1:end]
            if unit == 'GUIDE':
                continue                  # examiner guidance, priced nowhere
            if unit in ('AT', 'SP'):
                self.written.append((unit, start, self.lines[start].strip()))
            elif unit == 'AG':
                self._read_grammar(unit, body, start)
            elif unit == 'L':
                continue                  # the four parts are its real units
            else:
                self._read_unit(unit, body, start)
        self._checksum()

    # -- one reading or listening unit --------------------------------------
    def _read_unit(self, unit, body, start):
        heads = []
        for i, line in enumerate(body):
            s = line.strip()
            if not s or PAGE.match(s):
                continue
            m = Q_HEAD_HL.match(s)
            if m:
                heads.append((i, int(m.group(2)), m.group(3), m.group(1)))
                continue
            m = Q_HEAD_OL.match(s)
            if m:
                heads.append((i, int(m.group(1)), m.group(2), None))
        for n, (i, q, clause, word) in enumerate(heads):
            end = heads[n + 1][0] if n + 1 < len(heads) else len(body)
            self._read_question(unit, q, clause, word, body[i + 1:end],
                                start + 1 + i)

    def _read_question(self, unit, q, clause, word, block, line_no):
        total = head_total(clause)
        letters, romans = parse_head_clause(clause)
        if not letters:
            self._emit(unit, q, None, None, total, clause, block, line_no, word)
            return
        if total is not None and sum(letters.values()) != total:
            self._refuse(f'{unit} Q{q}', line_no,
                         f'the question head prices itself {total} and its own '
                         f'letter split adds to {sum(letters.values())}')
            return
        heads = _ordered_heads(block, L_HEAD, list(letters))
        seen = {h[1] for h in heads}
        for letter in letters:
            if letter not in seen:
                self._refuse(f'{unit} Q{q}({letter})', line_no,
                             f'the question head prices ({letter}) at '
                             f'{letters[letter]} and the scheme prints no such '
                             f'lettered head beneath it')
        for n, (i, letter, lclause) in enumerate(heads):
            end = heads[n + 1][0] if n + 1 < len(heads) else len(block)
            self._read_letter(unit, q, letter, letters[letter], lclause,
                              romans.get(letter) or {}, word,
                              block[i + 1:end], line_no + 1 + i)

    def _read_letter(self, unit, q, letter, marks, clause, romans, word, block,
                     line_no):
        printed = head_total(clause)
        if printed is not None and printed != marks:
            self._refuse(f'{unit} Q{q}({letter})', line_no,
                         f'the question head prices this part {marks} and the '
                         f"part's own head prices it {printed}")
            return
        romans = romans or split_romans(clause) or _infer_romans(block, marks)
        if not romans:
            # 2023 Ordinary and 2024 Higher print the ask itself on the part's
            # own head — "(c) What are the results of this? Give details.
            # (lines 67 ‒ 82)" — where every other sitting prints only a
            # tariff there. Dropping it shipped a card with no question on it.
            tail = (clause or '').strip()
            if tail and head_total(tail) is None and read_rate(tail)[0] is None:
                block = [tail] + list(block)
            self._emit(unit, q, letter, None, marks, clause, block, line_no, word)
            return
        if sum(romans.values()) != marks:
            self._refuse(f'{unit} Q{q}({letter})', line_no,
                         f'the part head prices itself {marks} and its own roman '
                         f'split adds to {sum(romans.values())}')
            return
        # 2021 Higher sets the first roman head on the LETTER's own line —
        # "(a) (i) (8 marks)" — so the letter head's own remainder is offered
        # to the roman walk as though it were the line beneath it. Without
        # that, (i) has no head and the whole 22-mark question is refused.
        pre = [clause] if R_HEAD.match((clause or '').strip()) else []
        block = pre + list(block)
        heads = _ordered_heads(block, R_HEAD, list(romans))
        seen = {h[1] for h in heads}
        for roman in romans:
            if roman not in seen:
                self._refuse(f'{unit} Q{q}({letter})({roman})', line_no,
                             f'the part head prices ({roman}) at {romans[roman]} '
                             f'and the scheme prints no such head beneath it')
        for n, (i, roman, rest) in enumerate(heads):
            end = heads[n + 1][0] if n + 1 < len(heads) else len(block)
            body = ([rest] if rest.strip() else []) + block[i + 1:end]
            self._emit(unit, q, letter, roman, romans[roman], rest, body,
                       line_no + 1 + i - len(pre), word)

    # -- applied grammar ----------------------------------------------------
    def _read_grammar(self, unit, body, start):
        """"Answer question 1 OR question 2" — two alternatives, both printed.

        Higher prints the question first and the tariff two lines below it;
        Ordinary prints the tariff on the head. Both alternatives are asks a
        candidate may answer, so both are leaves, exactly as a French Section B
        alternative is.
        """
        heads = []
        for i, line in enumerate(body):
            s = line.strip()
            m = AG_HEAD.match(s)
            if m and m.group(1) in '12' and int(m.group(1)) not in [h[1] for h in heads]:
                heads.append((i, int(m.group(1)), m.group(2)))
        for n, (i, q, rest) in enumerate(heads):
            end = heads[n + 1][0] if n + 1 < len(heads) else len(body)
            block = ([rest] if rest.strip() else []) + body[i + 1:end]
            self._emit_grammar(unit, q, block, start + 1 + i)

    def _emit_grammar(self, unit, q, block, line_no):
        cue, items, steps, notation = [], [], None, None
        cur = None
        for raw in block:
            s = raw.strip()
            if not s or PAGE.match(s) or s.upper() in ('OR', 'NÓ/OR'):
                continue
            got, _cnt = read_rate(s)
            if got is not None and steps is None:
                steps, notation = got, ' '.join(s.split())
                cur = None
                continue
            m = AG_ITEM.match(s)
            if m and steps is not None:
                cur = {'text': s, 'marks': None}
                items.append(cur)
                continue
            if cur is not None:
                cur['text'] = ' '.join(f"{cur['text']} {s}".split())
            elif steps is None:
                cue.append(s)
        for item in items:
            # The marks the SEC prints ON the item, with its own marker taken
            # off first: "(1) Singular, maskulin, Akkusativ (1, 2, 2)" is item
            # one, priced five, and counting its marker would price it six.
            # Only a bracket holding nothing but digits is a mark — "(Abschnitt
            # 1)" names the paragraph the compound was printed in.
            body_text = AG_ITEM.match(item['text']).group(2)
            item['marks'] = sum(
                sum(int(n) for n in re.findall(r'\d{1,2}', g))
                for g in re.findall(r'\(\s*(\d[\d,\s\-]*)\)', body_text))
        total = self.unit_totals.get('AG')
        if not items or steps is None:
            self._refuse(f'{unit} Q{q}', line_no,
                         'the scheme prints no rate line and no priced items for '
                         'this alternative')
            return
        got = sum(i['marks'] for i in items)
        if total is not None and got != total:
            self._refuse(f'{unit} Q{q}', line_no,
                         f'the section prices this alternative {total} and the '
                         f'marks printed on its own items add to {got}')
            return
        segments = [{'label': None, 'steps': [i['marks'] for i in items],
                     'answers': [{'text': i['text'], 'marks': i['marks']}
                                 for i in items]}]
        self.asks.append(Ask(
            unit=unit, q=q, letter=None, roman=None, total=total,
            segments=segments, notation=notation,
            cue=' '.join(' '.join(cue).split()), notes=[], language='German',
            line=line_no, head_word=None, exhaustive=True))

    # -- the leaf -----------------------------------------------------------
    def _emit(self, unit, q, letter, roman, total, clause, block, line_no, word):
        ask = self._leaf(unit, q, letter, roman, total, clause, block, line_no,
                         word)
        if isinstance(ask, str):
            tail = f'Q{q}' + (f'({letter})' if letter else '') + \
                   (f'({roman})' if roman else '')
            self._refuse(f'{unit} {tail}', line_no, ask)
        else:
            self.asks.append(ask)

    def _leaf(self, unit, q, letter, roman, total, clause, block, line_no, word):
        """One priced ask: its reprinted question, its rate line(s), its answers.

        The body is walked into SEGMENTS. Most asks have one; an ask the SEC
        divides between named halves — "How:" over a two-mark list and "What:"
        over another — has one per half, and each carries its own rate. A rate
        line arriving after a segment already holds answers belongs to the NEXT
        segment, because that is where the SEC prints "(Plus any two: 2 x 2
        marks)": under the fixed answer it is adding to.
        """
        cue_lines, notes = [], []
        segments = [{'label': None, 'steps': None, 'answers': [],
                     'tentative': False}]
        overview = None
        pending = None
        cur = None
        phase = 'cue'

        def new_segment(label, steps, tentative=False):
            nonlocal cur
            seg = segments[-1]
            if seg['steps'] is None and not seg['answers'] and seg['label'] is None:
                seg['label'], seg['steps'] = label, steps
                seg['tentative'] = tentative
            else:
                segments.append({'label': label, 'steps': steps, 'answers': [],
                                 'tentative': tentative})
            cur = None

        for raw in block:
            s = raw.strip()
            if not s or PAGE.match(s):
                continue
            if MARK_BOXES.match(s):
                continue
            m = TAIL_NOTE.search(s)
            if m:
                notes.append(m.group(2))
                s = s[:m.start(2)].strip()
            if SUBLIST.match(s) or DIRECTIVE.match(s):
                cur = None
                continue
            if NOTE.match(s):
                notes.append(s)
                cur = None
                continue
            m = SEGMENT.match(s)
            inline = m is not None
            if m is None:
                m = SEGMENT_Q.match(s)
                inline = False
            if m:
                tail = m.group(2).strip()
                got, _cnt = read_rate(tail)
                mark = TRAIL_MARK.search(tail) if inline else None
                if got is not None or mark or not tail:
                    phase = 'answers'
                    steps = got if got is not None else (
                        [int(mark.group(1))] if mark else pending)
                    new_segment(m.group(1), steps, tentative=steps is None)
                    pending = None
                    if got is None and mark:
                        cur = {'text': TRAIL_MARK.sub('', tail).strip()}
                        segments[-1]['answers'].append(cur)
                    continue
            got, _cnt, remark = read_rate_line(s)
            if got is not None:
                if remark:
                    notes.append(remark)
                # A rate printed ABOVE the question does not close the question:
                # 2023 Ordinary sets "4 marks: 2, 2 marks" on the line between
                # the head and the ask it prices, and treating that as the end
                # of the question read the question itself as the answer.
                if cue_lines:
                    phase = 'answers'
                if segments[-1]['answers']:
                    pending = got
                else:
                    # 2021 Higher prints the part tariff again on its own line
                    # — "(a) (i) (8 marks)" then "(Any four: 4 x 2 marks)" —
                    # so a second rate before any answer REPLACES the first:
                    # the later line is the one that says what an answer buys.
                    segments[-1]['steps'] = got
                    if segments[-1] is segments[0]:
                        overview = (segments[0] if total is not None
                                    and sum(got) == total else None)
                cur = None
                continue
            answer = None
            number = None
            m = ANSWER_NUM.match(s)
            if m and not re.match(r'^\(?\s*\d{1,3}\s*marks?\b', m.group(2), re.I):
                answer = m.group(2).strip()
                # The number the SEC printed in front of it. Kept because some
                # answers ARE just a letter — the Ordinary multiple-choice key
                # prints "1. C / 2. D / 3. A" — and a card offering four
                # options reading "C", "D", "A", "D" says nothing at all.
                number = int(m.group(1))
            elif unit.startswith('L') and ANSWER_LETTER.match(s):
                # Only the listening test letters its answers. A reading scheme
                # numbers them, and 2023 Higher reprints the PART MARKER above
                # its own question — "(a) (4 marks)" then "(a) Warum kommt
                # Lena…" — so reading a lettered line as an answer there put
                # the question itself in the answer list and left the ask with
                # no rate line at all.
                answer = ANSWER_LETTER.match(s).group(2).strip()
            elif TRAIL_MARK.search(s) and not MATCH_KEY.match(s) and (
                    cur is None or TRAIL_MARK.search(cur['text'])):
                # A line closing with its own mark is its own answer — unless
                # the answer above it has not been paid yet, in which case this
                # is its second printed line: 2023 Higher breaks "Since then
                # she is/has been often ignored… belong to the group /
                # anymore. (2)" across two lines and pays it once.
                answer = s
            elif ELLIPSIS.match(s) and segments[-1]['answers']:
                answer = s
            elif MATCH_KEY.match(s):
                for pair in MATCH_PAIR.finditer(s):
                    segments[-1]['answers'].append(
                        {'text': f'{pair.group(1)} — {pair.group(2)}',
                         'n': int(pair.group(1))})
                segments[-1]['matched'] = True
                phase, cur = 'answers', None
                continue
            elif phase == 'answers' and cur is None and not segments[-1]['answers']:
                # A segment whose single answer the SEC did not number: "How: 2
                # marks" over "(Her aunt suggests) Leonora could move in with
                # Sabine."
                answer = s
            if answer is not None:
                if pending is not None and segments[-1]['answers']:
                    new_segment(None, pending)
                    pending = None
                cur = {'text': answer, 'n': number}
                segments[-1]['answers'].append(cur)
                phase = 'answers'
                continue
            if phase == 'cue':
                cue_lines.append(s)
                if CUE_END.search(s):
                    phase = 'answers'
            elif cur is not None:
                # A wrapped answer: the SEC breaks a long marking point across
                # two printed lines and numbers the first only.
                cur['text'] = ' '.join(f"{cur['text']} {s}".split())

        if overview is not None and len(segments) > 1:
            # The rate the SEC prints above a divided ask states the WHOLE of
            # it — "(2 marks + (2 x 2) marks)" over a fixed answer and a menu —
            # so once the halves have declared their own rates it is a summary,
            # not this segment's tariff. Left in place it doubled the ask.
            overview['steps'] = None
        for seg in segments:
            for a in seg['answers']:
                m = TRAIL_MARK.search(a['text'])
                stripped = TRAIL_MARK.sub('', a['text']).strip()
                if m and not INNER_MARK.search(stripped):
                    a['marks'], a['text'] = int(m.group(1)), stripped
                else:
                    a['marks'] = None
            seg['answers'] = [a for a in seg['answers'] if a['text']]
        for seg in segments:
            if seg['steps'] is None:
                marks = [a['marks'] for a in seg['answers']]
                if marks and all(m is not None for m in marks):
                    seg['steps'] = marks
        # A bare heading over an unpriced list — "Love:" and "Loss:" over the
        # points of the Higher theme question — is a LABEL on that list, not a
        # division of the tariff: the paper itself says "You may refer to a
        # theme more than once." So it folds back into the list above it,
        # keeping its heading on each point it introduced, exactly as printed.
        merged = []
        for seg in segments:
            if seg['tentative'] and seg['steps'] is None and merged:
                # The heading is kept BESIDE the list rather than on each
                # point: the provenance gate searches the scheme for a card's
                # own words, and "Love: Little love shown between Esther's
                # parents" is a sentence the SEC never printed — it prints the
                # heading on its own line and numbers the points beneath it.
                merged[-1].setdefault('labels', []).append(seg['label'])
                merged[-1]['answers'].extend(seg['answers'])
                continue
            merged.append(seg)
        for seg in merged:
            if seg.get('labels'):
                seg['labels'] = ([seg['label']] if seg['label'] else []) \
                    + seg['labels']
                seg['label'] = None
        segments = [g for g in merged if g['steps'] is not None or g['answers']]
        if not segments:
            return 'the scheme prints no rate line and no answers for this ask'

        exhaustive = False
        if len(segments) == 1 and segments[0]['steps'] is None:
            got, _cnt = read_rate(clause or '')
            if got is not None:
                segments[0]['steps'] = got
        for seg in segments:
            if seg['steps'] is None:
                return ('the scheme prints no rate line this reads for the ask, '
                        'so what one answer is worth is not stated')
            # The key of a matching question names one more pair than the ask
            # is worth, because the paper prints the first pair already filled
            # in as its worked example — "1 d" is on the 2024 Ordinary page.
            # The card offers the pairs a candidate actually supplies.
            if seg.get('matched') and len(seg['answers']) == len(seg['steps']) + 1:
                seg['example'] = seg['answers'].pop(0)['text']
        if all(len(g['steps']) == len(g['answers']) for g in segments) and (
                any(a['marks'] is not None for g in segments for a in g['answers'])
                or any(g.get('matched') for g in segments)
                or all(a.get('n') for g in segments for a in g['answers'])):
            # Every answer priced on its own line and none of them optional:
            # the ask wants all of them. "2 marks per heading, 2 marks for
            # correct explanation" over eight priced lines is the Ordinary
            # paragraph-headings question, and it is not a menu.
            exhaustive = True
        got = sum(sum(g['steps']) for g in segments)
        if total is not None and got != total:
            return (f'the head prices this ask {total} and its own rate line(s) '
                    f'add to {got}')
        cue = ' '.join(' '.join(cue_lines).split())
        return Ask(unit=unit, q=q, letter=letter, roman=roman,
                   total=total if total is not None else got,
                   segments=segments,
                   notation='; '.join(
                       (f"{g['label']}: " if g['label'] else '')
                       + ' + '.join(str(n) for n in g['steps'])
                       for g in segments),
                   cue=cue, notes=notes, language=_language_of(cue, word),
                   line=line_no, head_word=word, exhaustive=exhaustive)

    def _refuse(self, ref, line, why):
        self.refused.append((ref, why, line))

    # -- the SEC's own arithmetic -------------------------------------------
    def _checksum(self):
        """Every split against the level above it.

        A unit prints its questions' totals on its own head — "(14, 18, 18, 10)"
        — and that is the only independent statement this document makes about
        whether a question was missed or a tariff mis-read.
        """
        for unit, printed in sorted(self.unit_splits.items()):
            got = {}
            for a in self.asks:
                if a.unit == unit:
                    got[a.q] = got.get(a.q, 0) + (a.total or 0)
            for n, want in enumerate(printed, start=1):
                have = got.get(n)
                if have is None:
                    self.flags.append(
                        (unit, n, f'the unit head prices Q{n} at {want} and the '
                                  f'reader found no priced ask under it'))
                elif have != want:
                    self.flags.append(
                        (unit, n, f'the unit head prices Q{n} at {want} and its '
                                  f'own asks add to {have}'))
        for unit, total in sorted(self.unit_totals.items()):
            if unit in self.unit_splits and sum(self.unit_splits[unit]) != total:
                self.flags.append(
                    (unit, None, f'the unit prints {total} and its own question '
                                 f'split adds to {sum(self.unit_splits[unit])}'))

    # -- lookups ------------------------------------------------------------
    def ref(self, ask):
        tail = f'Q{ask.q}'
        if ask.letter:
            tail += f'({ask.letter})'
        if ask.roman:
            tail += f'({ask.roman})'
        return f'{self.year} {self.level.upper()} Section {ask.unit} {tail}'

    def reading(self):
        return [a for a in self.asks if a.unit.startswith('T')]

    def grammar(self):
        return [a for a in self.asks if a.unit == 'AG']

    def listening(self):
        return [a for a in self.asks if a.unit.startswith('L')]

    def by_key(self):
        return {a.key: a for a in self.asks}


ROMAN_ORDER = ['i', 'ii', 'iii', 'iv', 'v', 'vi']


def _infer_romans(block, marks):
    """{roman: marks} where the SEC left the roman split off its own head.

    2025 Ordinary prices TEXT II question 3 as "(a) 8 marks; (b) 6 marks" and
    then prints TWO questions under (a), "(i) What videos are shared on
    TikTok?" and "(ii) What do young people talk about…", each with its own
    rate line of "3, 1 marks". The paper prints them as 3(a)(i) and 3(a)(ii).
    The split is not a guess: it is each part's own printed rate, and it is
    only believed when the parts run i, ii, … in order and their rates add to
    exactly what the head already said the letter is worth.
    """
    heads = []
    for i, line in enumerate(block):
        m = R_HEAD.match(line.strip())
        if m:
            roman = m.group(1).lower()
            if roman == ROMAN_ORDER[len(heads)]:
                heads.append((i, roman))
    if len(heads) < 2:
        return {}
    out = {}
    for n, (i, roman) in enumerate(heads):
        end = heads[n + 1][0] if n + 1 < len(heads) else len(block)
        steps = None
        for line in block[i:end]:
            got, _cnt, _remark = read_rate_line(line.strip())
            if got is not None:
                steps = got
                break
        if steps is None:
            return {}
        out[roman] = sum(steps)
    return out if sum(out.values()) == marks else {}


def _ordered_heads(block, pattern, expected):
    """[(index, marker, remainder)] for the markers of a split, IN ORDER.

    The split says which markers exist and in what order. Consuming them in
    that order is what stops an "(a)" printed inside another part's answers —
    or a "(b)" the SEC used as an answer label — from opening a part: a marker
    only opens the next expected one.
    """
    out = []
    wanted = list(expected)
    for i, line in enumerate(block):
        if not wanted:
            break
        m = pattern.match(line.strip())
        if m and m.group(1).lower() == wanted[0]:
            out.append((i, wanted.pop(0), m.group(2)))
    return out


def split_romans(clause):
    """The roman split a part head prints: "(i) 4 marks; (ii) 6 marks"."""
    out = {}
    for roman, marks in re.findall(
            r'\(\s*(i{1,3}|iv|vi{0,3}|v)\s*\)\s*:?\s*(\d{1,3})', clause or '', re.I):
        out.setdefault(roman.lower(), int(marks))
    return out


def _language_of(cue, head_word):
    """'German' or 'English or Irish' — what this ask must be answered in.

    Two printed signals, and they agree. The scheme's head word says it —
    "Frage 1" opens the German-answered question and "Question 2" the
    English-answered one, in the same comprehension — and the reprinted question
    is set in that language. The head word is printed at Higher only, so the
    reprint decides at Ordinary; where both are printed the reprint wins,
    because it is the ask itself.
    """
    de = len(GERMAN_WORDS.findall(cue or ''))
    en = len(ENGLISH_WORDS.findall(cue or ''))
    if de or en:
        return 'German' if de > en else 'English or Irish'
    if head_word:
        return 'German' if head_word.lower() in ('frage', 'ceist') else 'English or Irish'
    return 'English or Irish'


# ---------------------------------------------------------------- audit ----
def audit(subject=SUBJECT):
    bad = 0
    for path in sorted(glob.glob(os.path.join(schemes_dir(subject), '*.md'))):
        stem = os.path.basename(path)[:-3]
        year, level = int(stem[:4]), stem[5:]
        S = DeScheme(year, level, subject)
        written = [a for a in S.asks if not a.unit.startswith('L')]
        flags = [f for f in S.flags if not f[0].startswith('L')]
        refused = [r for r in S.refused if not r[0].startswith('L')]
        print(f'{stem}: {len(S.reading())} reading, {len(S.grammar())} grammar, '
              f'{len(S.listening())} listening | {len(flags)} flag(s), '
              f'{len(refused)} refused (written paper)')
        for unit, q, why in flags:
            bad += 1
            print(f'    FLAG {unit}{f" Q{q}" if q else ""}: {why}')
        for ref, why, line in refused:
            bad += 1
            print(f'    REFUSED {ref} (line {line}): {why}')
        for a in written:
            if not a.answers:
                bad += 1
                print(f'    NO ANSWERS {S.ref(a)}: {a.cue[:80]!r}')
    return 1 if bad else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('year', nargs='?', type=int)
    ap.add_argument('level', nargs='?')
    ap.add_argument('--subject', default=SUBJECT)
    ap.add_argument('--audit', action='store_true')
    ap.add_argument('--full', action='store_true')
    ap.add_argument('--unit')
    args = ap.parse_args()
    if args.audit or not args.year:
        return audit(args.subject)
    S = DeScheme(args.year, args.level, args.subject)
    asks = [a for a in S.asks if not args.unit or a.unit == args.unit]
    print(f'{args.year} {args.level.upper()}: {len(asks)} asks')
    for a in asks:
        print(f'  {S.ref(a):<34} {a.total:>3} [{a.notation}] ({a.language})')
        print(f'      ASK  {a.cue[:150]}')
        if args.full:
            for seg in a.segments:
                if seg['label']:
                    print(f'      -- {seg["label"]}: {seg["steps"]}')
                for b in seg['answers']:
                    print(f'      *  {b["text"][:120]}')
            for n in a.notes:
                print(f'      NOTE {n[:110]}')
    for unit, q, why in S.flags:
        print(f'  FLAG {unit}{f" Q{q}" if q else ""}: {why}')
    for ref, why, line in S.refused:
        print(f'  REFUSED {ref} (line {line}): {why}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
