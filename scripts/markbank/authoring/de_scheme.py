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
# 2018 Ordinary prints its first total unbracketed: "TEXT I: LESEVERSTÄNDNIS:
# 60 marks (21, 18, 16, 5)".
UNIT_LV = re.compile(
    r'^TEXT\s+(I{1,3}|[123])\s*:?\s*LESEVERST[ÄA]NDNIS\s*:?\s*'
    r'\(?(\d{1,3})(?:\s*marks?)?\)?\s*(?:\(([^)]*)\))?', re.I)
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
# (2013 Ordinary names a question's kind before its tariff: "4. True / False
# 10 marks: 5 x 2 marks".)
Q_HEAD_OL = re.compile(r'^(\d{1,2})\s*\.\s*(?:True\s*/\s*False\s+)?(\(?\s*\d{1,3}\s*marks?\b.*)$', re.I)
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
# The scheme's own statement that the two questions are alternatives.
GRAMMAR_OR = re.compile(r'^(?:OR|N[ÓO]/OR)$|\bquestion\s+1\s+OR\s+question\s+2\b', re.I)
# A grammar question's own head: "(15 marks: 5 x 3)", "1. (10 marks: 10 x 1 mark)".
# (2013 Ordinary prints the second unbracketed: "5 marks: 5 x 1 mark".)
QUESTION_TOTAL = re.compile(r'^(?:\d\.\s*)?(?:\((\d{1,2})\s+marks?\b|(\d{1,2})\s+marks?\s*:\s*\d)', re.I)


# "Compound words … say what words each compound word is made up of (5 marks)
# and what the underlined words mean. (5 marks)" — the only place a scheme that
# prints no mark on its compounds states what each is worth.
COMPOUND_HALVES = re.compile(
    r'(Compound words\b.*?made up of \((\d{1,2}) marks\).*?mean\.?\s*\((\d{1,2}) marks\))',
    re.I)


def _question_total(block):
    """The total a compulsory grammar question prints on its own head."""
    for line in block:
        m = QUESTION_TOTAL.match(line.strip())
        if m:
            return int(m.group(1) or m.group(2))
    return None

# A numbered answer line. The list restarts at 1 under every ask, so answers are
# only ever collected inside a block a head has closed.
ANSWER_NUM = re.compile(r'^(\d{1,2})\s*\.\s*(.*)$')
ANSWER_LETTER = re.compile(r'^\(\s*([a-z])\s*\)\s*(.+)$')
# (2017 Ordinary lists with hyphens: "- Warm clothing".)
BULLET = re.compile(r'^(?:[•\uf0b7]|-(?=\s))\s*(.+)$')
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
# (Or bracketed: "My real interest (2) (Allow: main)", 2017 Ordinary.)
TAIL_NOTE = re.compile(r'(\(\d{1,2}(?:\s*marks?)?\))\s*((?:\(\s*)?(?:N\.?B\.?|Note|Allow|'
                       r'Accept|Penalise|Deduct)\b.*)$', re.I)

# The named halves of one ask: "How:" over a two-mark list, "What:" over
# another. Both are answered — they are not alternatives.
# (A name may carry a digit, "MrWissen2go:", 2018 Ordinary.)
_LABEL = r'[A-Z][A-Za-z\u00c4\u00d6\u00dc\u00e4\u00f6\u00fc\u00df\u2019]{1,14}(?:\d[a-z]{1,4})?' \
         r'(?:\s+[a-z]{1,14}|\s+[A-Z][a-z\u00e4\u00f6\u00fc\u00df]{2,10})?'
# A segment label with a colon may carry its own answer on the same line:
# "Where: to the swimming pool (1)", "Wie lange: (etwas) mehr als ein Jahr
# (2 marks)".
SEGMENT = re.compile(rf'^({_LABEL})\s*:\s*(.*)$')
WQ_HEAD = re.compile(r'((?:Was|Wie|Wo|Warum|Wer|Welche[rsnm]?|Wann|Why|What|How|Where|When|Who|Which)'
                     r'\b[^:()?]{0,40}?)\s*:')
LETTER_ITEM = re.compile(r'^([a-h])\.\s+(\S.*)$')
CATEGORY_HEAD = re.compile(r'\(([a-h])\)\s+([A-Z][^:()]{1,40}):')
# A segment label written as a question — "Why? (2 marks)", "Where?" — may
# carry only its tariff. An ordinary sentence that happens to open with a
# capitalised word and a question mark is not a label, and 2021 Ordinary prints
# one inside its own answer list: "Texas? Without me! (2)" is the English of the
# paragraph heading above it, not a two-mark half of the ask.
SEGMENT_Q = re.compile(rf'^({_LABEL})\s*\?\s*:?\s*(.*)$')
SEGMENT_ASK = re.compile(r'^((?:Why|What|How|Where|When|Who|Which)\b[^:()]{0,40}?)\s*:\s*(\(.*\))\s*$')
# The Higher theme question lists its points under two headings and says on the
# paper that an answer may draw on either: "(Can be language use and/or
# content.)" So these label the list, they do not divide it.
SUBLIST = re.compile(r'^\(\s*(Content|Language use)\s*\)\s*$', re.I)
DIRECTIVE = re.compile(r'^(?:Allow|Accept|Either|Or)\s*:?\s*$', re.I)
NOTE = re.compile(r'^\(?\s*(?:N\.?B\.?|Note|Allow\b|Accept\b|Penalise|Deduct|'
                  r'Where answers|Answers in|Evidence needed|Quotation without|'
                  r'Award|Any three; no marks)\b'
                  r'|^\([^)]*\b(?:needed|required|only)\)\s*$'
                  # "(Incorrect pronoun = Penalise once; incorrect tense =
                  # penalise once)" (2017 Higher).
                  r'|^\((?=[^)]*\bpenalise\b)[^)]*\)\s*$', re.I)
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
# (2014 Ordinary separates the pairs with semicolons: "2 E; 3 F; 4 B; 5 A; 6 C".)
MATCH_KEY = re.compile(r'^(?:\d{1,2}\s*[-–—]?\s*[A-Fa-f](?=[\s;,]|$)[\s,;]*){3,}$')
MATCH_PAIR = re.compile(r'(\d{1,2})\s*[-–—]?\s*([A-Fa-f])(?=[\s;,]|$)')
# The row of empty mark boxes an Ordinary matching question prints above its
# key: "(1) (1) (1) (1) (1)". It is the examiner's tally, not an answer.
MARK_BOXES = re.compile(r'^(?:\(\d{1,2}\)\s*){2,}$')

# "Any three", "Any THREE details", "Any 3" — the claim count, wherever the SEC
# puts it in the rate line.
# ("Herr Seldersen’s reaction: (4 marks: 2, 2)", 2013 Ordinary, names a person.)
SEGMENT_RATED = re.compile(r'^([A-Z][\w’\']*(?:\s+[a-zäöüß][\w’\']*){1,4}'
                           r'|(?!Any\b)[A-Z][a-zäöüß][\w’\']*\s+[A-Z][a-zäöüß][\w’\']*(?:\s+[a-zäöüß][\w’\']*){1,3})'
                           r'\s*:\s*(.+)$')
BRACKET_HEADING = re.compile(r'^\((?!(?:Must|Allow|Accept|Any|Only|Not|No|Both|One|Two|Three|Plus|Also)\b)'
                             r'([A-Z][a-z]+(?:\s+[a-z]+){0,3}(?:\s+[A-Z][a-z]+)?)\)$')
# (Or the quoted answer straight before its price: "N.B. “I want to become an
# actor.” 1 mark only", 2017 Ordinary.)
NB_PARTIAL = re.compile(r'^N\.?\s?B\.?:?\s*(.+?)(?:\s*[:=]|(?<=”))\s*([1-9])\s*marks?(?:\s+only)?\.?$', re.I)
LABELLED_SUMMARY = re.compile(r'^\(\s*\d{1,3}\s*marks?\s*:\s*[A-Z][a-z]+\s*:\s*\d.*\)$'
                              # "(Two points for each: (2 x 2) + (2 x 2))" (2015 Higher)
                              r'|^\(\s*\w+ points? for each\s*:.*\)$', re.I)
INSTRUCTION_DE = re.compile(r'^(?:Schreiben|Geben|Nennen|Beschreiben|Erklären|Begründen|Finden)\s+Sie\b')
# "(Any TWO of the following details: 3 marks: 2, 1)" (2018 Ordinary).
ANY_N = re.compile(r'^(?:Plus\s+)?Any\s+(\w+)\s*(?:of\s+the\s+following\b\s*)?'
                   r'(?:details?|examples?|points?|items?|reasons?|countr(?:y|ies)|questions?|of)?\s*:?\s*', re.I)
COUNT_POINTS = re.compile(r'^(one|two|three|four|five)\s+(?:points?|details?)\s*:\s*(?=\d)', re.I)
# A rate spec, in every shape the ten schemes print.
SPEC_TIMES = re.compile(r'^(\d{1,2})\s*[x×]\s*(\d{1,2})(?:\s*marks?)?$', re.I)
SPEC_PLUS = re.compile(r'^\d{1,2}(?:\s*marks?)?(?:\s*\+\s*\d{1,2}(?:\s*marks?)?)+$', re.I)
SPEC_LIST = re.compile(r'^\d{1,2}(?:\s*,\s*\d{1,2})+(?:\s*marks?)?$', re.I)
SPEC_ONE = re.compile(r'^(\d{1,2})\s*marks?$', re.I)
# "(10 marks. 2 x 2 marks; 3 x 2 marks)" — the SEC separates a total from its
# spec with a colon almost always, a full stop once, and a semicolon once.
# "(4 marks 2 + 2 marks)" (2020 Higher) drops the colon before its split.
# (Or the split in brackets after the total: "9 marks (4, 3, 2)", 2014 Ordinary.)
TOTAL_THEN = re.compile(r'^(\d{1,3}|\w+)\s*marks?\s*(?:[:.;]\s*|\s+(?=\d{1,2}\s*[+x×,])'
                        r'|\s*(?=\(\s*\d{1,2}\s*[+x×,]))(.+)$', re.I)

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
    # "Any THREE details: 9 marks: 4, 3, 2," (2021 Ordinary): a stray comma
    # closing the list; "(2 marks):" (2019 Higher): a colon after the bracket.
    s = re.sub(r'(?<=\d),$', '', s)
    s = re.sub(r'(?<=\))\s*:$', '', s)
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
    # "Any THREE details: 9 marks: 4, 3, 2," (2021 Ordinary): a stray comma
    # closing the list; "(2 marks):" (2019 Higher): a colon after the bracket.
    s = re.sub(r'(?<=\d),$', '', s)
    s = re.sub(r'(?<=\))\s*:$', '', s)
    while s.startswith('(') and s.endswith(')'):
        s = s[1:-1].strip()
    # 2026 Higher prints "(Any four: 4 x 2 marks" with its bracket never
    # closed; the opening one alone is not part of the rate.
    if s.startswith('(') and s.count('(') == s.count(')') + 1:
        s = s[1:].strip()
    if not s:
        return None, None
    claimed = None
    # "(Two points: 3 + 3 marks)" (2015 Higher): the count, named without "Any".
    m = COUNT_POINTS.match(s)
    if m and _number(m.group(1)) is not None:
        claimed = _number(m.group(1))
        s = s[m.end():].strip()
        m = None
    else:
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
    # "Any TWO details: 3, 2 N.B. Allow use of past tense" (2020 Ordinary):
    # the aside runs on after the rate with no bracket round it.
    m = re.match(r'^(.*?\d)\s+(N\.\s?B\.?\s.+)$', s)
    if m:
        got, cnt = read_rate(m.group(1))
        if got is not None:
            return got, cnt, m.group(2)
    # "(Any three: 3 x 2) Wrong tense: penalise once only" (2016 Higher).
    m = re.match(r'^(\([^()]*\))\s+([A-Z][^()]*)$', s)
    if m:
        got, cnt = read_rate(m.group(1))
        if got is not None:
            return got, cnt, m.group(2)
    remark = []
    while True:
        # One bracket level inside the aside: "(Allow: Er sagt(e) followed
        # by direct quote.)" (2018 Higher).
        m = re.search(r'\s*(\((?:[^()]|\([^()]*\))*\))\s*$', s)
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
        "(16 marks: a = 10 marks; b = 6 marks)"     (2019 Higher)

    A clause naming no letter is a LEAF question and returns ({}, {}): "(10
    marks: Any two: 2 x 5 marks)" prices one ask, not two lettered ones.
    """
    s = clause or ''
    m = re.match(r'^\s*\(?\s*\d{1,3}\s*marks?\s*', s, re.I)
    if m:
        s = s[m.end():]
    # A letter's own breakdown in brackets after its total, "b = 8 marks (4 +
    # 4)" (2014 Higher), restates that total; it adds nothing to it.
    s = re.sub(r'(\d{1,3}\s*marks?)\s*\(\s*\d{1,2}(?:\s*[+x×]\s*\d{1,2})+\s*\)', r'\1', s, flags=re.I)
    letters, romans = {}, {}
    cur_letter = cur_roman = None
    pos = 0
    pattern = re.compile(
        r'\(\s*(?P<let>[a-h])\s*\)|(?:^|[:;,(]\s*)(?P<let2>[a-h])\s*[:=]'
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
            elif s[pos:m.start()].strip() == '+':
                # "b = 6 + 8 marks" (2015 Higher): the letter is the sum.
                letters[cur_letter] += n
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
                 'cue', 'notes', 'language', 'line', 'head_word', 'exhaustive', 'by_rate',
                 'bold')

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


SECTION_LANGUAGE = re.compile(
    r'^Answer Questions? \d+(?:,\s*\d+)*(?:\s+and\s+(?:Question\s+)?\d+)? in (?:English|German|Irish)\.?$',
    re.I)


class DeScheme:
    """One published German marking scheme, read as a list of priced leaves."""

    def __init__(self, year, level, subject=SUBJECT, sitting=None):
        self.year, self.level, self.subject = year, level, subject
        self.sitting = sitting
        self.path = os.path.join(schemes_dir(subject),
                                 f'{year}-{level}{"-deferred" if sitting == "deferred" else ""}.md')
        with open(self.path, encoding='utf-8') as fh:
            raw = fh.read()
        for old, new in MISPRINTS.get((year, level), ()):
            assert old in raw, f'{year} {level}: misprint {old!r} is not in the scheme'
            raw = raw.replace(old, new)
        # "Answer Question 2 and Question 3 in English." heads the English half
        # of a reading text and states no answer; read as text it ran on into
        # the last answer above it ("… Sie radeln, um Energie zu produzieren.
        # Answer Question 2"). It is blanked, keeping every line's place.
        # 2016's text layer carries its bullet as a control character, \x02
        # ("\x02 200 times (3)"): read as the bullet it prints.
        raw = raw.replace('\x02', '•')
        # 2010 and 2014 set the bullet as a letter "x": "x Award content marks
        # first.", "x erhält innerhalb einer Stunde einen Rückruf. (2)".
        raw = re.sub(r'(?m)^x (?=[A-Za-zÄÖÜäöü(])', '• ', raw)
        self.lines = ['' if SECTION_LANGUAGE.match(l.strip()) else l.rstrip()
                      for l in raw.split('\n')]
        self.asks = []
        self.refused = []
        self.flags = []
        self.refused_leaves = {}
        self.grammar_compulsory = False
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
        # The question's own number before its first lettered head: "1. (a)
        # Describe the hotel manager." (2014 Ordinary).
        block = [re.sub(rf'^(\s*){q}\s*\.\s*(?=\(\s*[a-h]\s*\))', r'\1', b) for b in block]
        total = head_total(clause)
        letters, romans = parse_head_clause(clause)
        if not letters:
            # "Frage 1 (18 marks: 6, 4, 4, 4)" (2016 Higher): the split as a
            # bare list, the letters only on the heads beneath it. Believed
            # where the heads run (a), (b), … one per printed share and each
            # head's own total is that share.
            shares = [int(n) for n in re.findall(r'\d{1,3}', (clause or '').split(':', 1)[1])] \
                if ':' in (clause or '') and not re.search(r'[a-h]\s*[:=)]|\bx\b', clause or '') else []
            if len(shares) > 1 and total is not None and sum(shares) == total:
                names = 'abcdefgh'[:len(shares)]
                found = _ordered_heads(block, L_HEAD, list(names))
                if (len(found) == len(shares)
                        and [head_total(c) for _i, _l, c in found] == shares):
                    letters = dict(zip(names, shares))
        if not letters:
            # A listening question split into romans with no letter above them:
            # 2025 Higher First Part "2. (8 marks: (i) 2 x 2 marks; (ii) 4 x 1
            # mark)", then "(i) What did Frau Glas do …" and "(ii) …". Each
            # roman is an ask of its own, priced by its own clause.
            tr = top_romans(clause)
            # (Only where the block prints a roman head: 2016 Ordinary prices
            # TEXT II Q3 "(6 marks: (i) 3; (ii): 3)" and prints its halves as
            # "Home country: 3 marks" and "Germany: 3 marks" under the one
            # question the paper sets.)
            if (tr and total is not None and sum(tr.values()) == total
                    and any(R_HEAD.match(b.strip()) for b in block)):
                self._read_letter(unit, q, None, total, clause, tr, word, block, line_no)
                return
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
        heads = _restated(block, _ordered_heads(block, R_HEAD, list(romans)), list(romans))
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
        # Until 2020 the section set TWO questions and a candidate answered
        # both: "TEXT I: ANGEWANDTE GRAMMATIK (25)" over "(15 marks: 5 x 3)"
        # and "(10 marks: 5 x 2 marks)", with no "OR" between them. Each is
        # then priced by its own head, and the two heads must add to the
        # section's. The choice is read from the scheme's own "OR" line.
        choice = any(GRAMMAR_OR.search(line.strip()) for line in body)
        self.grammar_compulsory = bool(heads) and not choice
        blocks = []
        for n, (i, q, rest) in enumerate(heads):
            end = heads[n + 1][0] if n + 1 < len(heads) else len(body)
            blocks.append((q, ([rest] if rest.strip() else []) + body[i + 1:end],
                           start + 1 + i))
        own = None
        if self.grammar_compulsory:
            own = {q: _question_total(block) for q, block, _ in blocks}
            section = self.unit_totals.get('AG')
            if None in own.values() or sum(own.values()) != section:
                for q, _block, line_no in blocks:
                    self._refuse(f'{unit} Q{q}', line_no,
                                 f'the section prices both questions {section} and '
                                 f'their own heads print {sorted(own.items())}')
                return
        for q, block, line_no in blocks:
            self._emit_grammar(unit, q, block, line_no,
                               own[q] if own is not None else None)

    def _emit_grammar(self, unit, q, block, line_no, own=None):
        cue, items, steps, notation = [], [], None, None
        preamble = []
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
            if got is None and steps is None and notation is None and QUESTION_TOTAL.match(s):
                # A tariff the rate reader cannot split, "(15 marks: 5 x (2+1)
                # marks)" (2016 Higher): the items below price themselves.
                notation = ' '.join(s.split())
                cur = None
                continue
            m = AG_ITEM.match(s)
            if m and (steps is not None or notation is not None):
                cur = {'text': s, 'marks': None}
                items.append(cur)
                continue
            if cur is not None:
                if re.fullmatch(r'\(\d{1,2}\)', s):
                    # A mark the line wrap left on a line of its own: "…
                    # hundred percent/ 100%" / "(1)" (2026 Ordinary). It is
                    # the item's price; the scheme's text layer keeps no
                    # bare "(1)" line to quote, so the answer is shown to
                    # the end of its words and priced with it.
                    cur['wrapped'] = cur.get('wrapped', '') + ' ' + s
                    continue
                cur['text'] = ' '.join(f"{cur['text']} {s}".split())
            elif steps is None:
                cue.append(s)
            elif not items:
                preamble.append(s)
        for item in items:
            # The marks the SEC prints ON the item, with its own marker taken
            # off first: "(1) Singular, maskulin, Akkusativ (1, 2, 2)" is item
            # one, priced five, and counting its marker would price it six.
            # Only a bracket holding nothing but digits is a mark — "(Abschnitt
            # 1)" names the paragraph the compound was printed in.
            body_text = AG_ITEM.match(item['text']).group(2) + item.get('wrapped', '')
            item['marks'] = sum(
                sum(int(n) for n in re.findall(r'\d{1,2}', g))
                for g in re.findall(r'\(\s*(\d[\d,\s\-]*)\)', body_text))
        notes = []
        by_rate = False
        bold = None
        if not items and steps and preamble:
            # 2015 Ordinary reprints each sentence whole, unlabelled, under
            # "(5 marks: 5 x 1 mark)", and sets the right preposition in bold:
            # "Sie will lieber zu / in / **nach** / auf Hause gehen, …"; 2014
            # circles it. The text layer keeps neither, so the choice is read
            # off the PDF.
            marked = self._marked_choices(preamble)
            if marked is not None and len(marked[1]) == len(steps):
                bold = marked[0]
                items = [{'text': f'{stem} — {word}', 'marks': step}
                         for (stem, word), step in zip(marked[1], steps)]
                by_rate = True
        if (items and not any(i['marks'] for i in items) and steps
                and len(steps) == len(items) and not COMPOUND_HALVES.search(' '.join(preamble))):
            # 2018 Ordinary prints the five prepositions bare, "(i) vor",
            # under "(5 marks: 5 x 1 mark)": five answers, one mark each.
            for i, step in zip(items, steps):
                i['marks'] = step
            by_rate = True
        halves = COMPOUND_HALVES.search(' '.join(' '.join(preamble).split()))
        if (items and not any(i['marks'] for i in items) and halves
                and steps and set(steps) == {1} and len(steps) == 2 * len(items)
                and int(halves.group(2)) == int(halves.group(3)) == len(items)):
            # 2019 Ordinary prints the compounds with no mark on any line:
            # "(i) Piratenschiff (Abschnitt 1) Piraten + Schiff pirate ship",
            # under "(10 marks: 10 x 1 mark)" and "say what words each
            # compound word is made up of (5 marks) and what the underlined
            # words mean. (5 marks)". Ten answers at one mark are the five
            # pairs of words and the five meanings, so each compound is two —
            # and the card carries the scheme's own sentence saying so.
            for i in items:
                i['marks'] = 2
            notes.append(halves.group(1))
        if (steps is None and own is not None and items and all(i['marks'] for i in items)
                and sum(i['marks'] for i in items) == own):
            # "(15 marks: 5 x (2+1) marks)" (2016 Higher) over items that
            # price themselves, "(1) Wen (2) wollte sie besuchen? (1)".
            steps = [i['marks'] for i in items]
        total = own if own is not None else self.unit_totals.get('AG')
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
            cue=' '.join(' '.join(cue).split()), notes=notes, language='German',
            line=line_no, head_word=None, exhaustive=True, by_rate=by_rate,
            bold=bold))

    def _marked_choices(self, lines):
        """((how, [(stem, word)]) for sentences the scheme reprints with the
        right choice marked on the page, read off the PDF, or None.

        2015 Ordinary sets the choice in bold ("Sie will lieber zu / in /
        **nach** / auf Hause gehen"); 2014 Ordinary draws a circle round it,
        as the candidate is told to. The text layer keeps neither, so the PDF
        is read: each sentence's first printed line (the one offering its
        choices "w / w / w / w") is found by its text, and exactly one choice
        on it must be bold, or ringed by exactly one drawn circle. Lines
        before the first sentence are the reprinted instruction; a line
        without choices after an unfinished sentence is its second line
        ("… auf dem / am / neben dem / zu dem" / "Tisch sitzen."). The stem is
        the sentence's own words before its choices, which the card shows
        beside the marked word."""
        sentences = []
        for line in (' '.join(l.split()) for l in lines):
            if ' / ' in line:
                sentences.append(line)
            elif sentences and not re.search(r'[.?!]$', sentences[-1]):
                continue                  # the sentence's second printed line
            elif sentences:
                return None
        if not sentences:
            return None
        pdf = self.path[:-len('.md')] + '.pdf'
        if not os.path.exists(pdf):
            return None
        import pymupdf
        found = {}
        with pymupdf.open(pdf) as doc:
            for page in doc:
                rows = []
                for block in page.get_text('dict')['blocks']:
                    for line in block.get('lines', []):
                        for span in line['spans']:
                            y = span['bbox'][1]
                            row = next((r for r in rows if abs(r[0] - y) <= 3), None)
                            if row is None:
                                row = [y, []]
                                rows.append(row)
                            row[1].append(span)
                rings = None
                for y, spans in rows:
                    spans.sort(key=lambda sp: sp['bbox'][0])
                    text = ' '.join(''.join(sp['text'] for sp in spans).split())
                    if text not in sentences or text in found:
                        continue
                    bold = [sp['text'].strip() for sp in spans if sp['flags'] & 16 and sp['text'].strip()]
                    if rings is None:
                        # Each circle is drawn as four curves; its box is the ring.
                        rings = []
                        for d in page.get_drawings():
                            curves = [it for it in d['items'] if it[0] == 'c']
                            for k in range(0, len(curves) - 3, 4):
                                pts = [pt for it in curves[k:k + 4] for pt in it[1:]]
                                rings.append((min(pt.x for pt in pts), min(pt.y for pt in pts),
                                              max(pt.x for pt in pts), max(pt.y for pt in pts)))
                    top = min(sp['bbox'][1] for sp in spans)
                    bottom = max(sp['bbox'][3] for sp in spans)
                    ringed = []
                    for x0, y0, x1, y1 in rings:
                        if not (y0 <= (top + bottom) / 2 <= y1):
                            continue
                        # A ring is drawn loosely and takes in the slashes
                        # beside its word, sometimes the next word's edge.
                        inside = [w[4] for w in page.get_text('words')
                                  if x0 <= (w[0] + w[2]) / 2 <= x1 and y0 <= (w[1] + w[3]) / 2 <= y1
                                  and w[4] != '/']
                        ringed.append(inside)
                    found[text] = (bold, ringed)
        out, how = [], set()
        for text in sentences:
            if text not in found:
                return None
            head = text.split(' / ')
            middle = head[1:-1]
            k = max(len(c.split()) for c in middle) if middle else 1
            words = head[0].split()
            if len(words) <= k:
                return None
            stem, first = ' '.join(words[:-k]), ' '.join(words[-k:])
            choices = [first] + [c.strip() for c in middle] + [' '.join(head[-1].split()[:k])]
            bold, rings_here = found[text]
            ringed = []
            for inside in rings_here:
                hit = [c for c in choices if all(t in inside for t in c.split())]
                hit = [c for c in hit if not any(c != o and c in o.split() for o in hit)]
                if len(hit) != 1:
                    return None
                ringed.append(hit[0])
            # (2015 both sets it in bold and rings it; the two must agree.)
            if len(bold) == 1 and bold[0] in choices and ringed in ([], [bold[0]]):
                out.append((stem, bold[0]))
                how.add('bold')
            elif not bold and len(ringed) == 1 and ringed[0] in choices:
                out.append((stem, ringed[0]))
                how.add('circled')
            else:
                return None
        return (how.pop(), out) if len(how) == 1 else None

    def _tick_columns(self, statements):
        """['True'|'False'] for each statement, from the column its X stands
        in on the scheme PDF, or None."""
        pdf = self.path[:-len('.md')] + '.pdf'
        if not os.path.exists(pdf):
            return None
        import pymupdf
        with pymupdf.open(pdf) as doc:
            for page in doc:
                words = page.get_text('words')
                heads = {w[4]: (w[0] + w[2]) / 2 for w in words if w[4] in ('True', 'False')}
                if len(heads) != 2:
                    continue
                rows = {}
                for w in words:
                    key = next((k for k in rows if abs(k - w[1]) <= 3), w[1])
                    rows.setdefault(key, []).append(w)
                out = []
                for st in statements:
                    want = ' '.join(st.split()[:4])
                    row = next((sorted(r, key=lambda w: w[0]) for r in rows.values()
                                if want in ' '.join(w[4] for w in sorted(r, key=lambda w: w[0]))), None)
                    marks = [w for w in row or [] if w[4] == 'X']
                    if len(marks) != 1:
                        out = None
                        break
                    x = (marks[0][0] + marks[0][2]) / 2
                    near = sorted(heads, key=lambda h: abs(heads[h] - x))
                    if abs(heads[near[0]] - x) * 2 > abs(heads[near[1]] - x):
                        out = None            # not clearly under one column
                        break
                    out.append(near[0])
                if out:
                    return out
        return None

    # -- the leaf -----------------------------------------------------------
    def _emit(self, unit, q, letter, roman, total, clause, block, line_no, word):
        ask = self._leaf(unit, q, letter, roman, total, clause, block, line_no,
                         word)
        if isinstance(ask, str):
            # Kept for the readers that can still card it another way: an
            # answer GRID (de_all, scheme_grid) prints no list this reads.
            self.refused_leaves[(unit, q, letter, roman)] = (total, clause, list(block))
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
        # The halves the part's own head prices by name: "(c) 9 marks:
        # Incident: 5 marks: 2, 3; Outcome: 4 marks: 2, 2" (2017 Ordinary).
        named = {lab: [int(n) for n in re.findall(r'\d{1,2}', split)]
                 for lab, split in re.findall(
                     r'\b([A-Z][a-z]+):\s*\d{1,2}\s*marks?:\s*([\d,\s]+?)\s*(?:;|$)', clause or '')}
        segments = [{'label': None, 'steps': None, 'answers': [],
                     'tentative': False}]
        overview = None
        pending = None
        cur = None
        phase = 'cue'
        note_open = False

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

        # A true/false table's statement wrapped past its X: "Yvonne macht
        # zum ersten Mal Campingurlaub mit ihren X (2)" / "Freundinnen."
        # (2013 Ordinary) is one statement, its X after it.
        if any(re.fullmatch(r'True\s+False', b.strip()) for b in block):
            joined = []
            for b in block:
                t = b.strip()
                prev = joined[-1] if joined else ''
                m = re.match(r'^(.*?\S)\s+(X(?:\s*\(\s*\d{1,2}\s*\))?)$', prev)
                if (m and t and not PAGE.match(t) and ' X' not in f' {t}'
                        and re.match(r'^[a-zäöüA-ZÄÖÜ]', t) and re.search(r'[.?!]$', t)):
                    joined[-1] = f'{m.group(1)} {t} {m.group(2)}'
                    continue
                joined.append(b)
            block = joined
        # Two lists priced by name in a summary above them: "8 marks: (4
        # marks: 2, 1, 1; and" / "4 marks: 2, 1, 1)" / "Any SIX details: Any
        # three food items: (4 marks: 2, 1, 1) and" / "Any three drink items:
        # (4 marks: 2, 1, 1)", then "Food: Any THREE" and "Drinks: Any THREE"
        # over their lists (2014 Ordinary TEXT II Q2(b)). Each heading takes
        # the rate its noun is named with; the summary is the card's note.
        named_rates, summary = {}, []
        flat = [' '.join(b.split()) for b in block]
        for k, line in enumerate(flat):
            for cnt, noun, tot, split in re.findall(
                    r'Any (\w+) (\w+) items?:\s*\((\d{1,2}) marks?:\s*([\d,\s]+?)\)', line, re.I):
                steps_ = [int(n) for n in re.findall(r'\d{1,2}', split)]
                if _number(cnt) == len(steps_) and sum(steps_) == int(tot):
                    named_rates[noun.lower()] = steps_
        if len(named_rates) > 1:
            heads_ = [k for k, line in enumerate(flat)
                      if re.fullmatch(r'([A-ZÄÖÜ][a-zäöü]+):\s*Any\s+\w+', line)
                      and any(line.lower().startswith(n) for n in named_rates)]
            if len(heads_) == len(named_rates):
                lead = [k for k in range(heads_[0]) if re.search(r'\bmarks?\b', flat[k])
                        and not CUE_END.search(flat[k])]
                summary = [k for k in lead if k >= min(lead)] if lead else []
            else:
                named_rates = {}
        if summary:
            notes.append(' '.join(flat[k] for k in summary if re.search(r'\bitems?:', flat[k])))
        for at, raw in enumerate(block):
            s = raw.strip()
            if not s or PAGE.match(s):
                continue
            if MARK_BOXES.match(s):
                continue
            if at in summary:
                phase = 'answers'
                continue
            head_ = re.fullmatch(r'([A-ZÄÖÜ][a-zäöü]+):\s*Any\s+(\w+)', ' '.join(s.split()))
            if head_ and named_rates:
                rate_ = next((v for n, v in named_rates.items() if head_.group(1).lower().startswith(n)), None)
                if rate_ is not None and _number(head_.group(2)) == len(rate_):
                    new_segment(head_.group(1), rate_)
                    phase = 'answers'
                    continue
            # A note's sentence runs on over lines of its own: "N.B. The four
            # details cannot all come from the same category (a) and (b) i.e.
            # only a" / "maximum of three details is allowed from one
            # category, the fourth detail must come from" / "the other
            # category." (2015 Ordinary). A line opening in lower case after a
            # note that has not ended is that note's.
            if note_open and notes and re.match(r'^[a-zäöüß]', s):
                notes[-1] = f'{notes[-1]} {s}'
                note_open = not re.search(r'[.!?)”"]$', s)
                continue
            note_open = False
            # The ask's own marker restated over its rate: "(i) What is the
            # narrator's plan? (lines 74 – 77)" / "(i) 2 marks: 1, 1" (2019
            # Ordinary). The second "(i)" is that roman's rate line.
            if roman:
                again = re.match(rf'^\(\s*{roman}\s*\)\s*(.+)$', s)
                if again and read_rate(again.group(1))[0] is not None:
                    s = again.group(1)
            # A theme heading printed bare, "Uncertainty" over "1. During her
            # school years …" (2019 Higher), is "Uncertainty:".
            following = next((x.strip() for x in block[at + 1:]
                              if x.strip() and not PAGE.match(x.strip())), '')
            if (phase == 'answers' and re.fullmatch(r'[A-ZÄÖÜ][a-zäöüß]{3,14}', s)
                    and re.match(r'^1\.\s', following)):
                s = f'{s}:'
            # A wrapped answer's last word with its question mark, "… Why was
            # Johnny alone in" / "Berlin?", is that answer's end, not a heading.
            if (cur is not None and SEGMENT_Q.fullmatch(s) and not SEGMENT_Q.match(s).group(2)
                    and not re.search(r'[.?!:)]$', cur['text'])):
                cur['text'] = f"{cur['text']} {s}"
                continue
            m = TAIL_NOTE.search(s)
            if m:
                notes.append(m.group(2))
                s = s[:m.start(2)].strip()
            if SUBLIST.match(s) or DIRECTIVE.match(s):
                cur = None
                continue
            if (NOTE.match(s) and cur is not None and segments[-1]['steps'] is not None
                    and NB_PARTIAL.match(s)):
                # "N.B. “What do you want to do?”: 1 mark only" under the answer
                # it is a cheaper form of (2017 Ordinary): carried on that
                # answer, where it is claimed in its place.
                cur['text'] = f"{cur['text']} {s}"
                cur = None
                continue
            if NOTE.match(s):
                notes.append(s)
                # Where it was printed: under a later half's list, it is that
                # half's ("Allow global “he asks himself questions” = 1 mark"
                # under "How?", 2015 Ordinary TEXT III Q1).
                segments[-1].setdefault('notes_here', []).append(s)
                note_open = not re.search(r'[.!?)”"]$', s)
                cur = None
                continue
            if LABELLED_SUMMARY.match(s):
                # "(6 marks: What: 3 marks; How: 3 marks)" (2017 Ordinary):
                # the halves' tariffs, each printed again on its own half.
                continue
            # The question with its own tariff after it: "What is his plan
            # for the following day? (3 marks: 1, 1, 1)" (2016 Ordinary).
            asked = re.fullmatch(r'(.*\?)\s*\((\d{1,2}\s*marks?\b[^()]*)\)', s)
            if (asked and phase == 'cue' and len(asked.group(1).split()) >= 4
                    and read_rate(asked.group(2))[0] is not None
                    and all(g['steps'] is None and not g['answers'] for g in segments)):
                cue_lines.append(asked.group(1))
                segments[-1]['steps'] = read_rate(asked.group(2))[0]
                phase = 'answers'
                continue
            # The question's own second sentence, after a first that ended
            # on its line reference: "… beschreiben? (Zeile 1 – 19 / 25 –
            # 27)" / "Schreiben Sie je drei kurze informative Sätze …" (2017
            # Higher), before any rate or answer.
            if (phase == 'answers' and cue_lines and INSTRUCTION_DE.match(s)
                    and all(g['steps'] is None and not g['answers'] for g in segments)):
                cue_lines.append(s)
                continue
            # A lettered category over part of the list, "(a) The school:" /
            # "(b) The first day:" (2015 Ordinary TEXT III Q3), under the one
            # rate the whole list shares: a label on that list, as a theme
            # heading is.
            # A half headed by its own question, its rate on the line below:
            # "Was macht die Erzählerin:" / "(Any two: 2 x 2 marks)" (2015
            # Higher TEXT I Q1(c)), after the answer to the first half.
            wq = WQ_HEAD.fullmatch(s)
            if wq and phase == 'answers' and read_rate_line(following)[0] is not None:
                new_segment(wq.group(1), None)
                continue
            # … or under the rate it heads: "(8 marks: 4 x 2 marks)" / "What
            # they do:" (2014 Higher).
            if (wq and phase == 'answers' and segments[-1]['steps'] is not None
                    and not segments[-1]['answers'] and segments[-1]['label'] is None):
                segments[-1]['label'] = wq.group(1)
                continue
            # An examiner's aside opened in a bracket that its own lines never
            # close: "(General statements not sufficient: candidates must give
            # an example … and must" / "have contrast. The list below is not
            # exhaustive." (2014 Higher). A note, run on as notes are.
            if (phase == 'answers' and re.match(r'^\((?![a-h]\)|[ivx]{1,4}\))[A-Z][a-z]+\s', s)
                    and ')' not in s and read_rate_line(s)[0] is None):
                notes.append(s)
                note_open = not re.search(r'[.!?)”"]$', s)
                cur = None
                continue
            cat = CATEGORY_HEAD.fullmatch(s)
            if cat and phase == 'answers' and any(g['steps'] is not None for g in segments):
                new_segment(f'({cat.group(1)}) {cat.group(2)}', None, tentative=True)
                continue
            # An unnumbered line opening a list, "Seems indifferent to the
            # world around him but…" over "1. …sits in furthest corner …", or
            # "Indifferent to the world around him = doesn’t care about
            # rules/consequences" over "a. does not buy a ticket" (2016 Higher
            # TEXT I Q4): the list's heading, priced nowhere.
            if (phase == 'answers' and unit.startswith('T') and following
                    and (re.match(r'^1\.\s*[.…]', following) or LETTER_ITEM.match(following)
                         or (re.search(r'(?:…|\.\.\.)$', s) and re.match(r'^1\.\s', following)
                             and not any(g['answers'] for g in segments)))
                    and not ANSWER_NUM.match(s) and not LETTER_ITEM.match(s)
                    and (cur is None or re.search(r'[.!?)]$', cur['text']))
                    and read_rate_line(s)[0] is None and not NOTE.match(s)
                    and any(g['steps'] is not None for g in segments)):
                new_segment(s, None, tentative=True)
                continue
            m = SEGMENT.match(s)
            inline = m is not None
            if m is None:
                m = SEGMENT_Q.match(s)
                inline = False
            if m is None:
                # A half headed by its own question, with its rate on the
                # line: "Why is it not realistic: (Any ONE detail: 2 marks)"
                # (2026 Ordinary TEXT I Q1(d)). Only where what follows the
                # colon IS a rate.
                m = SEGMENT_ASK.match(s)
                if m and read_rate(m.group(2))[0] is None:
                    m = None
                inline = False
            if m is None:
                # A longer heading, as long as a rate follows its colon:
                # "Planned for the summer: Any ONE detail: 2 marks" (2017
                # Ordinary).
                m = SEGMENT_RATED.match(s)
                if m and read_rate(m.group(2))[0] is None:
                    m = None
                inline = False
            if (m is None and phase == 'cue' and cue_lines and cue_lines[-1].endswith('?')
                    and BRACKET_HEADING.match(s)):
                phase = 'answers'            # the heading ends the question
            if m is None and phase == 'answers' and BRACKET_HEADING.match(s):
                # "(Holiday Plans)" / "(After his holidays)" over the answers
                # each half prints (2017 Ordinary): a heading, priced nowhere.
                new_segment(BRACKET_HEADING.match(s).group(1), None, tentative=True)
                continue
            if m:
                tail = m.group(2).strip()
                if re.fullmatch(r'\((?:Allow|Accept|N\.?\s?B)\b[^()]*\)', tail, re.I):
                    # "Stella: (Allow: sie)" (2018 Higher), "Was? (Allow
                    # Perfect / Imperfect)" (2017 Higher): the half's heading
                    # with an aside.
                    notes.append(tail)
                    tail = ''
                got, _cnt = read_rate(tail)
                if got is None and tail:
                    # "Gründe: (Any three: 3 x 2 marks) (Allow Present Tense)"
                    # (2019 Higher): the half's rate with an aside beside it.
                    got, _cnt, aside = read_rate_line(tail)
                    if got is not None and aside:
                        notes.append(aside)
                bare = re.fullmatch(r'\(\s*(\d{1,2})\s*(?:marks?)?\s*\)', tail)
                if got is None and bare and not inline:
                    # "Warum? (2)" over "Stella möchte Jason wiedersehen. (2)"
                    # (2018 Higher): the half priced by a bare mark.
                    got = [int(bare.group(1))]
                mark = TRAIL_MARK.search(tail) if inline else None
                last_seg = segments[-1]
                if (not tail and got is None and pending is None
                        and last_seg['steps'] is not None and not last_seg['answers']
                        and last_seg['label'] is None and cue_lines):
                    # The rate printed ABOVE its own heading: "(Any three: 3 x
                    # 2 marks)" then "Denmark:" (2026 Higher TEXT II Q3). The
                    # heading names the list that rate opened.
                    last_seg['label'] = m.group(1)
                    phase = 'answers'
                    continue
                if (got is None and not mark and tail and inline and phase == 'answers'
                        and not re.match(r'^Any\b', m.group(1), re.I)
                        and segments[-1]['answers'] == [] and segments[-1]['steps'] is not None
                        and not NOTE.match(tail) and not MARK_BOXES.match(tail)):
                    # "Was: Sie möchte sich neben ihn setzen …" / "neben Ihnen
                    # sitzen?“ (1)" (2018 Higher): a half whose one answer
                    # starts on its heading's line and is priced where it wraps.
                    new_segment(m.group(1), None, tentative=True)
                    cur = {'text': tail, 'n': None}
                    segments[-1]['answers'].append(cur)
                    continue
                if got is None and not mark and tail and inline and m.group(1) in named:
                    # "Incident: He cut Mrs. Pawlik's … hair (2) AND" / "he
                    # ruined/wrecked it/did a bad job. (3)": priced by the
                    # part's head, its answer begun on the heading's line.
                    phase = 'answers'
                    new_segment(m.group(1), named[m.group(1)])
                    pending = None
                    cur = {'text': tail, 'n': None}
                    segments[-1]['answers'].append(cur)
                    continue
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
            rate_here = next((g['steps'] for g in reversed(segments) if g['steps']), None)
            if (got is not None and cur is not None and cur.get('n') and rate_here
                    and len(set(rate_here)) == 1 and sum(got) == rate_here[0]
                    and re.match(rf'^{cur["n"] + 1}\.\s', following)):
                # "5. give information/ brochure about house/ neighbours/
                # beautiful destinations." / "(Any two: 1+1)" / "6. …" (2013
                # Higher): how answer 5's own two marks are earned, printed
                # under it, inside a list that goes on.
                cur['text'] = f"{cur['text']} {s}"
                continue
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
            if m is None and unit.startswith('T') and LETTER_ITEM.match(s) and any(
                    g.get('label') and g['tentative'] for g in segments[-1:]):
                # "a. does not buy a ticket" under its heading (2016 Higher).
                m = LETTER_ITEM.match(s)
            if m is None and cur is not None and cur.get('n'):
                # "1. He travels alone." / "2 He provokes the girls." (2019
                # Ordinary): the next number in the list, its full stop lost.
                m = re.match(rf'^({cur["n"] + 1})\s+([A-ZÄÖÜ(…].*)$', s)
            if m and not re.match(r'^\(?\s*\d{1,3}\s*marks?\b', m.group(2), re.I):
                answer = m.group(2).strip()
                # The number the SEC printed in front of it. Kept because some
                # answers ARE just a letter — the Ordinary multiple-choice key
                # prints "1. C / 2. D / 3. A" — and a card offering four
                # options reading "C", "D", "A", "D" says nothing at all.
                number = int(m.group(1)) if m.group(1).isdigit() else None
            elif BULLET.match(s) and not unit.startswith('L'):
                # 2026 sets a reading ask's answers behind bullets, under a
                # named half: "Frau Sommer: (Any one: 1 mark)" / "• beautiful".
                answer = BULLET.match(s).group(1).strip()
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

        # (Only where a half HAS declared a rate: under "(Any three: 3 x 4
        # marks)" the 2019 Higher theme question prints bare headings —
        # "Mystery:", "Darkness:" — which label its list and price nothing.)
        if overview is not None and len(segments) > 1 and any(
                g['steps'] is not None for g in segments if g is not overview):
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
        # A true/false key printed as a table, "True False" over "1. 23
        # Mädchen und Jungen hatten die Idee für die Mini-Firma. X (1)"
        # (2012-2014 Ordinary): the X stands in the column it answers, which
        # the text layer loses. Read off the PDF by position.
        # (A statement wrapped past its X runs on after it: "Yvonne macht zum
        # ersten Mal Campingurlaub mit ihren X (2)" / "Freundinnen.", 2013.)
        answers_ = [a for g in segments for a in g['answers']]
        tick = re.compile(r'^(.*?\S)\s+X(?:\s*\(\s*\d{1,2}\s*\))?(?:\s+(\S.*))?$')
        if (answers_ and all(tick.match(a['text']) for a in answers_)
                and any(re.fullmatch(r'True\s+False', b.strip()) for b in block)):
            said = [' '.join(x for x in tick.match(a['text']).groups() if x) for a in answers_]
            cols = self._tick_columns(said)
            if cols is None:
                return 'the scheme marks each statement with an X whose column this cannot read'
            for a, text, col in zip(answers_, said, cols):
                a['text'] = f'{text} — {col}'
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
        if len(segments) > 1 and any(g['steps'] is None for g in segments):
            # Halves under bracketed headings, each answer pricing itself, the
            # part's head the whole split: "(b) 6 marks: 1, 1, 1, 1, 2" over
            # "(Holiday Plans)" / "… Croatia (1) … (1) … (1) … (1)" and
            # "(After his holidays)" / "Work experience … (2)" (2017
            # Ordinary). One list, every answer required, read in order.
            want, _cnt = read_rate(clause or '')
            flat = []
            for g in segments:
                for a in g['answers']:
                    flat += ([a['marks']] if a['marks'] is not None
                             else [int(n) for n in INNER_MARK.findall(a['text'])])
            if want and flat == want and all(g['answers'] for g in segments):
                segments = [{'label': None, 'steps': want, 'tentative': False,
                             'labels': [g['label'] for g in segments],
                             'answers': [a for g in segments for a in g['answers']]}]

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
            if len(heads) < len(ROMAN_ORDER) and roman == ROMAN_ORDER[len(heads)]:
                heads.append((i, roman))
    if len(heads) < 2:
        # The questions listed first and printed again over their answers
        # (2016 Ordinary): the second printing, read below.
        pass
    listed = [(i, r, '') for i, r in heads]
    restated = _restated(block, listed[:2], ['i', 'ii']) if len(heads) >= 2 else listed
    if restated is not listed[:2] and len(heads) >= 2:
        heads = [(i, r) for i, r, _rest in restated]
    if len(heads) < 2:
        return {}
    out = {}
    for n, (i, roman) in enumerate(heads):
        end = heads[n + 1][0] if n + 1 < len(heads) else len(block)
        steps = None
        for line in block[i:end]:
            got, _cnt, _remark = read_rate_line(line.strip())
            if got is None:
                # The tariff at the end of the roman's own question: "(ii)
                # What is his plan for the following day? (3 marks: 1, 1, 1)".
                tail = re.search(r'\((\d{1,2}\s*marks?\b[^()]*)\)\s*$', line.strip())
                got = read_rate(tail.group(1))[0] if tail else None
            if got is not None:
                steps = got
                break
        if steps is None:
            return {}
        out[roman] = sum(steps)
    return out if sum(out.values()) == marks else {}


def _restated(block, heads, expected):
    """The romans' heads where the part first LISTS its questions, one line
    each, and then prints each again over its answers: "(i) How does Maik
    spend …?" / "(ii) What takes him by surprise?" and then "(i) … 6 marks:
    3, 2, 1" (2016 Ordinary). The second printing is the one with answers."""
    if (len(heads) == len(expected) > 1
            and all(heads[n + 1][0] == heads[n][0] + 1 for n in range(len(heads) - 1))):
        off = heads[-1][0] + 1
        again = _ordered_heads(block[off:], R_HEAD, expected)
        if len(again) == len(expected):
            return [(i + off, r, rest) for i, r, rest in again]
    return heads


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


def top_romans(clause):
    """{roman: marks} for a head that splits its question into romans with no
    letter: "(8 marks: (i) 2 x 2 marks; (ii) 4 x 1 mark)", "(4 marks: (i) 2 +
    2 marks; (ii) …)". Each roman's own clause states its worth: "N x M" is
    N times M, "a + b" their sum, a single figure itself. {} where any roman's
    worth is not stated."""
    s = clause or ''
    m = re.match(r'^\s*\(?\s*\d{1,3}\s*marks?\s*:?', s, re.I)
    body = s[m.end():] if m else s
    parts = re.split(r'\(\s*(i{1,3}|iv|vi{0,3}|v)\s*\)', body, flags=re.I)
    if len(parts) < 3 or re.search(r'\(\s*[a-h]\s*\)', parts[0], re.I):
        return {}
    out = {}
    for roman, seg in zip(parts[1::2], parts[2::2]):
        seg = seg.split(';')[0]
        times = re.search(r'(\d{1,2})\s*[x×]\s*(\d{1,2})', seg)
        if times:
            value = int(times.group(1)) * int(times.group(2))
        else:
            nums = [int(n) for n in re.findall(r'\d{1,3}', seg)]
            if not nums:
                return {}
            value = sum(nums) if '+' in seg else nums[0]
        out[roman.lower()] = value
    return out


def split_romans(clause):
    """The roman split a part head prints: "(i) 4 marks; (ii) 6 marks", or
    "(i) = 4 marks; (ii) = 6 marks" (2017 Higher)."""
    out = {}
    for roman, marks in re.findall(
            r'\(\s*(i{1,3}|iv|vi{0,3}|v)\s*\)\s*[:=]?\s*(\d{1,3})', clause or '', re.I):
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


# ---------------------------------------------------------- answer grids ----
GRID_ASK = re.compile(r'Fill in the information required in the box below|Fill in the grid below', re.I)
GRID_PRICE = re.compile(r'\(\s*(\d{1,2})\s*\)')
GRID_MENU = re.compile(r'^(Any\s+(?:\w+)\s+details?:\s*\d{1,2}\s*marks?(?::\s*\d(?:\s*,\s*\d)*)?)\s*(.*)$', re.I)


def _grid_words(path, find_page):
    """The words of the first page one of whose printed lines, read by
    position, `find_page` accepts."""
    import pymupdf
    with pymupdf.open(path) as doc:
        for pno in range(doc.page_count):
            words = doc[pno].get_text('words')
            rows = {}
            for x0, y0, _x1, _y1, w, *_ in words:
                rows.setdefault(round(y0), []).append((x0, w))
            if any(find_page(' '.join(w for _x, w in sorted(r))) for r in rows.values()):
                return words
    return None


FIELD_ASK = re.compile(r'\bFill in the information required\b', re.I)


def scheme_field_table(year, level, cue, total, subject=SUBJECT, sitting=None):
    """[(field, [answer lines])] for a two-column answer table, or None.

    2013 Ordinary TEXT II Q1 ("Fill in the information required.") answers
    in a ruled table: the field down the left ("Means of transport (1
    mark)"), its answer on the right ("Train (1)", or "Any TWO of the
    following details: 4 marks: 2, 2" over a numbered list). The text layer
    interleaves the two columns, so the table is read by position: its rows
    between the drawn rules under the ask, its columns either side of the
    one inner vertical rule. Believed only where the fields' printed marks
    add to the ask's total."""
    path = os.path.join(schemes_dir(subject),
                        f'{year}-{level}{"-deferred" if sitting == "deferred" else ""}.pdf')
    if not os.path.exists(path):
        return None
    import pymupdf
    want = ' '.join((cue or '').split())
    with pymupdf.open(path) as doc:
        for page in doc:
            words = page.get_text('words')
            rows = {}
            for w in words:
                key = next((k for k in rows if abs(k - w[1]) <= 3), w[1])
                rows.setdefault(key, []).append(w)
            top = next((k for k, r in rows.items()
                        if ' '.join(x[4] for x in sorted(r, key=lambda x: x[0])) in want and len(r) > 3
                        and want.startswith(' '.join(x[4] for x in sorted(r, key=lambda x: x[0])))), None)
            if top is None:
                continue
            draws = page.get_drawings()
            hs = sorted({round(d['rect'].y0) for d in draws
                         if d['rect'].height < 2 and d['rect'].width > 50 and d['rect'].y0 > top})
            vs = sorted({round(d['rect'].x0) for d in draws
                         if d['rect'].width < 2 and d['rect'].height > 20 and d['rect'].y0 > top})
            if len(vs) != 3 or len(hs) < 3:
                return None
            left, gutter, right = vs
            out = []
            for y0, y1 in zip(hs, hs[1:]):
                cell = [w for w in words if y0 < (w[1] + w[3]) / 2 < y1 and left < w[0] < right]
                if not cell:
                    continue

                def lines(ws):
                    got = {}
                    for w in sorted(ws, key=lambda x: (x[1], x[0])):
                        k = next((k for k in got if abs(k - w[1]) <= 3), w[1])
                        got.setdefault(k, []).append(w)
                    return [' '.join(x[4] for x in sorted(v, key=lambda x: x[0])) for _k, v in sorted(got.items())]
                field = ' '.join(lines([w for w in cell if w[0] < gutter]))
                answer = lines([w for w in cell if w[0] >= gutter])
                out.append((' '.join(field.split()), answer))
            priced = [re.search(r'\(\s*(\d{1,2})\s*marks?\s*\)\s*$', f) for f, _a in out]
            if not out or None in priced or sum(int(m.group(1)) for m in priced) != total:
                return None
            return out
    return None


def scheme_grid(year, level, steps=None, subject=SUBJECT, sitting=None, header=None):
    """[(column, [cell])] for an answer GRID, read off the scheme PDF by
    position, or None. A cell is (row label, answer, marks) or, where the
    scheme prints a choice inside the cell, (row label, None, (rate, steps,
    [answers])).

    2018 Ordinary TEXT II Q1 ("Fill in the information required in the box
    below"), 2016 Ordinary TEXT II Q1 and 2015 Ordinary TEXT II Q3 ("Fill in
    the grid below") answer with a table: a column per person, a row per
    field, each cell priced "(1)" — or, in its last row, "Any ONE detail: 3
    marks" over a numbered list. The text layer interleaves the columns, so
    the cells are read by position: the columns split at the white gutters
    between the heads, the rows between the labels down the left edge.
    Believed only where every column adds to the share it prints over itself
    ("(10 marks: 1, 1, 1, 2, 2, 3)") or, failing that, to `steps`.
    """
    path = os.path.join(schemes_dir(subject),
                        f'{year}-{level}{"-deferred" if sitting == "deferred" else ""}.pdf')
    if not os.path.exists(path):
        return None
    norm = lambda t: ' '.join(t.split())  # noqa: E731
    want = norm(header) if header else None
    words = _grid_words(path, (lambda t: norm(t) == want) if want else (lambda t: bool(GRID_ASK.search(t))))
    if not words:
        return None
    lines = {}
    for x0, y0, x1, _y1, w, *_ in sorted(words, key=lambda t: t[1]):
        # One printed line, though its words sit a point or two apart:
        # "architect" and its "(2)" (2015 Ordinary).
        key = next((k for k in lines if abs(k - y0) <= 3), round(y0))
        lines.setdefault(key, []).append((x0, x1, w))
    ys = sorted(lines)
    text_of = lambda y: ' '.join(w for _a, _b, w in sorted(lines[y]))  # noqa: E731
    if want:
        head_y = next((y for y in ys if norm(text_of(y)) == want), None)
    else:
        at = next(y for y in ys if GRID_ASK.search(text_of(y)))
        head_y = next((y for y in ys if y > at), None)
    if head_y is None:
        return None

    def label_split(y):
        """(label words, cell words) of one line: the label is the run of
        words at the left margin, each within a few points of the last."""
        ws = sorted(lines[y])
        label = []
        if ws and ws[0][0] < 100:
            label.append(ws[0])
            for w in ws[1:]:
                if w[0] - label[-1][1] < 10:
                    label.append(w)
                else:
                    break
        return label, ws[len(label):]

    head_label, head_cells = label_split(head_y)
    # The end of the grid: the next question, "2. (10 marks …".
    end_y = ys[-1] + 1
    for y in ys:
        if y > head_y and re.match(r'^\d{1,2}\.\s*\(', text_of(y)) and lines[y][0][0] < 100:
            end_y = y - 4
            break
    band = [y for y in ys if head_y < y < end_y and not re.fullmatch(r'\d{1,3}', text_of(y))]
    cell_words = [w for y in band for w in label_split(y)[1]] + head_cells
    # The columns: one per head, split at the white gutter between heads.
    heads = []
    for x0, x1, w in head_cells:
        if heads and x0 - heads[-1]['x1'] < 20:
            heads[-1]['name'] += f' {w}'
            heads[-1]['x1'] = x1
        else:
            heads.append({'x0': x0, 'x1': x1, 'name': w})
    if len(heads) < 2:
        return None
    edges = []
    for a, b in zip(heads, heads[1:]):
        lo, hi = (a['x0'] + a['x1']) / 2, (b['x0'] + b['x1']) / 2
        covered = sorted((x0, x1) for x0, x1, _w in cell_words if x1 > lo and x0 < hi)
        gap, cursor, best = None, lo, None
        for x0, x1 in covered:
            if x0 > cursor and (best is None or x0 - cursor > best[1] - best[0]):
                best = (cursor, x0)
            cursor = max(cursor, x1)
        if hi > cursor and (best is None or hi - cursor > best[1] - best[0]):
            best = (cursor, hi)
        if best is None:
            return None
        edges.append((best[0] + best[1]) / 2)
    edges = [-1] + edges + [10 ** 6]
    col = lambda x: next(k for k in range(len(heads)) if edges[k] <= x < edges[k + 1])  # noqa: E731
    # Each column's printed share, "(10 marks: …)" under its head.
    shares = None
    sub = [y for y in band if re.match(r'^\(\d{1,2}\s*marks', text_of(y).strip())
           or re.search(r'\(\d{1,2}\s+marks:', text_of(y))]
    if sub:
        got = {}
        for x0, _x1, w in label_split(sub[0])[1]:
            if re.fullmatch(r'\(\d{1,2}', w):
                got.setdefault(col(x0), int(w[1:]))
        if len(got) == len(heads):
            shares = [got[k] for k in range(len(heads))]
    # The rows: a label down the left edge runs on until it ends in "?" or
    # ":", and a row runs halfway to the labels above and below it.
    rows, cur = [], None
    for y in band:
        if sub and y <= sub[0]:
            continue
        label = ' '.join(w for _a, _b, w in label_split(y)[0])
        if not label:
            continue
        if cur is None:
            cur = {'y': y, 'last': y, 'label': label}
            rows.append(cur)
        else:
            cur['label'] += f' {label}'
            cur['last'] = y
        if re.search(r'[?:]$', cur['label']):
            cur = None
    if not rows or cur is not None:
        return None
    top = (sub[0] if sub else head_y) + 6
    bounds = [(top + rows[0]['y']) / 2 if rows[0]['y'] - top > 12 else top] + [
        (rows[n]['last'] + rows[n + 1]['y']) / 2 for n in range(len(rows) - 1)] + [end_y]
    out = [(h['name'], []) for h in heads]
    for n, row in enumerate(rows):
        lo, hi = bounds[n], bounds[n + 1]
        for c, (_name, cells) in enumerate(out):
            text = ' '.join(w for y in band if lo <= y < hi
                            for x0, _x1, w in sorted(label_split(y)[1]) if col(x0) == c)
            text = ' '.join(text.replace('•', ' ').split())
            if not text:
                continue
            menu = GRID_MENU.match(text)
            if menu:
                got, _cnt = read_rate(menu.group(1))
                # The list is numbered 1., 2., …: split at the next number
                # only ("Can go home at 3/ 3:30" is one answer).
                rest, answers, k = ' ' + menu.group(2), [], 1
                cut = re.search(rf'(?:^|\s){k}\.\s+', rest)
                while cut:
                    nxt = re.search(rf'\s{k + 1}\.\s+', rest[cut.end():])
                    end = cut.end() + nxt.start() if nxt else len(rest)
                    answers.append(rest[cut.end():end].strip(' /'))
                    rest, k = rest[end:], k + 1
                    cut = re.search(rf'(?:^|\s){k}\.\s+', rest)
                if got is None or len(answers) < len(got):
                    return None
                cells.append((row['label'], None, (menu.group(1), got, answers)))
                continue
            if re.search(r'\bAny\b', text):
                return None
            pos = 0
            for m in GRID_PRICE.finditer(text):
                answer = text[pos:m.start()].strip(' /')
                if not answer:
                    return None
                cells.append((row['label'], answer, int(m.group(1))))
                pos = m.end()
            if text[pos:].strip():
                return None
    sums = [sum((m if a is not None else sum(m[1])) for _l, a, m in cells) for _n, cells in out]
    if shares is not None and sums != shares:
        return None
    if shares is None and (steps is None or sums != list(steps)):
        return None
    return out
