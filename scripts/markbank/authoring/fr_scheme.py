#!/usr/bin/env python3
"""French marking schemes — the priced answer, and the ladder beneath it.

    python3 scripts/markbank/authoring/fr_scheme.py 2024 hl --full
    python3 scripts/markbank/authoring/fr_scheme.py --audit

What this document is
---------------------
A French scheme is three documents stapled together, and only one of them is
an answer:

    SECTION A : COMPRÉHENSION ÉCRITE (120 Marks)     <- priced answers
      Q.1 (60 Marks)                                    reading comprehension 1
        1.(a) .............................. 5 Marks    <- the head, with tariff
        Comment Billie décrit-elle sa ville ? (Section 1)   <- the reprinted ask
        • (D'après elle, la ville où elle habite est) super calme ..... 5 Marks
        - (D'après elle, la ville où elle habite est) calme ........... 4 Marks
        - (D'après elle, la ville où elle habite est) super ........... 0 Marks
    SECTION B : PRODUCTION ÉCRITE (100 Marks)        <- a BAND GRID, no answer
    Listening Comprehension Test (80 Marks)          <- priced answers, but the
                                                        ask needs the recording
    APPENDIX 2 CD Script                             <- the recording, in print

**The MARK on the line decides, not the glyph in front of it.** The scheme's
own explanatory page says "a bullet point indicates an answer which is worth
full Marks, a dash indicates an answer which is worth partial Marks or 0
Marks" — and its own Ordinary papers break that rule: 2022 Ordinary Q.3 sets
four part-credit lines with a bullet, one of them worth a single mark on a
four-mark ask ("• (des) jeux video ... 1 Mark"). Trusting the glyph offers a
student a one-mark fragment as a full answer. So the full-mark answers are the
lines carrying the HIGHEST printed mark in their ask, and everything printed
below that is the part-credit ladder. The glyph is still read, and kept, but it
decides nothing.

The dash itself is printed as four different characters across the five years —
the Symbol font's U+F02D in 2021, U+2212 in 2022-2023 and a plain hyphen in
2024-2025 — which is the other reason it cannot be the test.

The full-mark lines are what a card offers as answers. The rungs beneath are
the same answer, shorter, at 4, 3, 2, 1 or 0 marks; they are kept here and
disclosed on the card as a note, because the deck has no row kind for a rung
worth less than the row above it and inventing one without a renderer is how a
card the UI cannot display ships.

Sections B and the Listening test are read too, so that the refusals this bank
records are counted rather than assumed — see fr_all.py, which turns them into
exclusions with the scheme evidence quoted.
"""
import argparse
import glob
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))

SUBJECT = 'french'


def schemes_dir(subject=SUBJECT):
    return os.path.join(ROOT, 'examiner-reports', subject, 'schemes')


# ------------------------------------------------------------- the parts ----
# The reading comprehension the scheme is marking. "Q.1 (60 Marks)" at Higher,
# "Q.1 (40 marks)" at Ordinary, where the paper sets four rather than two.
RC_HEAD = re.compile(r'^Q\.\s*(\d)\s*\((\d{1,3})\s*(?:marks?|points?)\)\s*$', re.I)

UNIT_A = re.compile(r'^SECTION\s+A\b\s*[:.]?\s*COMPR', re.I)
# 2023 Higher sets "SECTION B" on its own line with "PRODUCTION ÉCRITE (100
# Marks)" beneath it, so requiring both words on one line left Section A open
# to the end of the file and welded the marking grid onto the last ask. The
# bare form is enough BECAUSE this is only consulted while the reader is in
# Section A: inside the listening test "Section B (21 Marks)" is a listening
# section, and the negative lookahead keeps 2021 Ordinary's "Section B
# Listening Comprehension" with the listening test where it belongs.
UNIT_B = re.compile(r'^SECTION\s+B\b(?!\s+Listening)', re.I)
# 2021 and 2022 Ordinary head the listening test "Section B Listening
# Comprehension 100 points" — the SEC numbers it as a section of the whole
# examination. Anchoring on "Listening" alone missed it, and both sittings
# censused zero listening asks while the paper prints twenty.
UNIT_L = re.compile(r'^(?:Section\s+[A-Z]\s+)?Listening\s+Comprehension\b', re.I)
# Everything from here is the Modified Marking Scheme and the CD Script: the
# transcript of the recording, printed in the ANSWER document. Reading past it
# would key the transcript's own "Section A" as a listening section and its
# speaker turns as marking points.
APPENDIX = re.compile(r'^APPENDIX\b', re.I)

# A listening section head, INSIDE the listening test: "Section A (12 Marks)".
# A-E, not A-D: 2025 Higher sets five listening sections where every other
# sitting sets four, and reading only A-D filed Section E's three asks under
# Section D, colliding with D's own Q1-Q3.
LISTEN_SECTION = re.compile(r'^Section\s+([A-E])\s*\((\d{1,3})\s*Marks?\)', re.I)
# A listening ask opens with its number alone, sometimes with the speaker's
# name on the same line ("1. Danielle"). No dotted leader and no head tariff:
# the marks are on the bullets.
LISTEN_ITEM = re.compile(r'^(\d{1,2})\s*\.\s*(?:\(([a-h])\)\s*)?(.*)$')

# The head of a priced reading-comprehension ask. The dotted leader is set with
# full stops in some years and with U+2026 ellipses in others, and 2021 sets
# every space in it as U+00A0, so the leader is a character CLASS of at least
# four rather than a literal run of dots.
ITEM_HEAD = re.compile(
    r'^(\d{1,2})\s*\.?\s*'
    r'(?:\(\s*([a-h])\s*(?:[-–‐]\s*([a-h])\s*)?\)\s*\.?)?'
    r'\s*[.…\s‐-]{4,}\s*'
    r'(\d{1,2}(?:\s*[+x×]\s*\d{1,2})?\s*Marks?)\s*$', re.I)

# The tariff, as the scheme writes it above the answer.
#   5 Marks      one answer, five marks
#   5+5 Marks    two answers at five each — the ask is worth ten
#   4 x 4 Marks  four answers at four each — the ask is worth sixteen
TARIFF = re.compile(r'^(\d{1,2})(?:\s*([+x×])\s*(\d{1,2}))?\s*Marks?$', re.I)

# What the SEC prints at the end of a marking line. The leader between the
# answer and its mark is dots in some years and U+2026 in others, and 2023
# prints "1 Mark" where every other line prints "Marks".
LINE_MARKS = re.compile(r'\s*[.…\s‐]*[.…]\s*\.?\s*(\d{1,2})\s*Marks?\.?\s*$', re.I)
# The same tariff with no leader at all: "• Walks 4 Marks" happens where the
# leader collapsed in extraction.
BARE_MARKS = re.compile(r'\s+(\d{1,2})\s*Marks?\.?\s*$', re.I)

FULL = '•●▪■'                     # a full-mark bullet
# Every character the five years use for the partial-credit dash. U+F02D is the
# Symbol font's hyphen, which is what 2021 leaves in the text layer.
# The hyphen is LAST on purpose. Written between two characters it is a
# character-class RANGE, and '\u2014-\u2043' silently swallowed U+2014 to
# U+2043 while leaving the plain ASCII hyphen out of the class entirely --
# which is the dash the 2024 and 2025 schemes actually print. Every one of
# their part-credit lines was then read as a continuation of the full-mark
# answer above it, and thirty cards shipped an answer with the next three
# rungs of its own ladder welded onto the end.
# U+F02D is the Symbol font's own hyphen, which is what the 2021 schemes leave
# in the text layer where every other year prints a real dash.
PART = '\u2212\u2013\u2014\u2043\u25cb\u25e6\uf02d-'
FULL_BULLET = re.compile(rf'^[{FULL}]\s*')
PART_BULLET = re.compile(rf'^[{PART}]\s+')
# The Wingdings arrow the SEC sets under "Note:", which reaches the text layer
# as U+F0D8. It opens an examiner instruction, never an answer. Spelling it as
# the real arrow matched nothing at all, and the note lines were kept out only
# by the "Note:" heading above them -- which is why an ask whose Note comes
# BEFORE its answers lost every answer it had.
NOTE_BULLET = re.compile('^[\uf0d8\u27a2\u2794]\\s*')

DIRECTIVE = re.compile(
    r'^(?:One of|Two of|Three of|Any (?:two|three|four|one)\s*(?:of)?|Either)\s*:?\s*$'
    r'|^Appropriate direct quotation\b'
    r'|^Candidates? (?:may|must)\b'
    r'|^Accept\b|^Allow\b'
    r'|^Agree\s*:?\s*$|^Disagree\s*:?\s*$'
    r'|^Etc\.?,?\s*etc\.?\s*$',
    re.I)
NOTE = re.compile(r'^(?:Note\s*:|N\.?B\.?\b|Penalise\b|Penalties\b)', re.I)
# A bulletless answer: the accepted forms separated by solidi, which is how the
# scheme answers "find a verb in the imperfect" and "find an infinitive". Two
# solidi at least, and no sentence punctuation -- a question is never written
# this way and an answer list never ends in a question mark.
SOLIDUS_LIST = re.compile(r'^[^?.!]*/[^?.!]*/[^?.!]*$')
PAGE = re.compile(r'^(?:##\s*Page\s*\d+\s*$|\d{1,3}\s*$)')

# The two answer routes an opinion ask prints: the scheme lists the points for
# agreeing and the points for disagreeing separately, and a candidate takes one
# side. Read as one list they would offer a student both sides of an argument
# as though either could be claimed beside the other.
ROUTE = re.compile(r'^(Agree|Disagree)\s*:?\s*$', re.I)
OPEN_LIST = re.compile(r'^Etc\.?,?\s*etc\.?\s*$|^Etc\.?\s*$', re.I)

# An ask that demands more than one answer, in any of the three languages the
# paper sets its questions in. "deuxième" is not "deux": the word boundaries
# matter, and without them every "Trouvez dans la deuxième section" would be
# read as a two-answer ask.
MULTI_ANSWER = re.compile(
    r'\b(?:two|three|deux|trois|dh[áa]|tr[íi]|dh[áa]\s+phointe)\b', re.I)

# SEC misprints, keyed by the sitting, never repaired by a heuristic. The 2024
# Ordinary scheme prints its seventh head as "7.4 ……4 Marks": the tariff's own
# digit is duplicated onto the marker. The line's real tariff is printed at its
# end, which is where every other head in the file carries it.
# The Ordinary written-production gap-fill, which is the one part of Section B
# that states an answer. "(a) Filling Gaps – 30 marks", then "10 gaps for 3
# marks each", then the ten words in two printed columns the extractor
# flattens onto one line ("1. en 6. desserts").
GAP_HEAD = re.compile(r'^\(a\)\s*Filling\s+Gaps\s*[–—-]\s*(\d{1,3})\s*marks?', re.I)
GAP_RATE = re.compile(r'^(\d{1,2})\s+gaps?\s+for\s+(\d{1,2})\s+marks?\s+each', re.I)
GAP_ANSWER = re.compile(r'(\d{1,2})\.\s*([^\s\d][^\s]*)')

MISPRINTS = {
    (2024, 'ol'): [('7.4 …', '7. …')],
    # The 2025 Ordinary gap-fill prints its sixth answer "maqnifiques". The
    # same scheme spells it "magnifiques" in the completed letter it prints
    # three lines below, and the paper's own word list — the ten words a
    # candidate chooses from — prints "magnifiques" too. A card offering
    # "maqnifiques" as the right answer would be teaching a typo.
    (2025, 'ol'): [('6. maqnifiques', '6. magnifiques')],
    # 2023 Higher heads its first reading comprehension "Q,1" with a comma.
    # Read literally the whole comprehension has no head, and its eleven asks
    # are attributed to nothing: the sitting censused 11 asks where the paper
    # prints 22.
    (2023, 'hl'): [('Q,1 (60 Marks)', 'Q.1 (60 Marks)')],
}


def parse_tariff(text):
    """(total, per-answer, count, notation) for a printed tariff, or None.

    Never a guess: an unrecognised notation returns None and the caller refuses
    the ask rather than pricing it.
    """
    raw = ' '.join((text or '').split())
    m = TARIFF.match(raw)
    if not m:
        return None
    first = int(m.group(1))
    op, second = m.group(2), m.group(3)
    if op is None:
        return first, first, 1, raw
    second = int(second)
    if op == '+':
        # "5+5" is two answers at five. The SEC only ever writes it with equal
        # halves; unequal halves would be a split this cannot price.
        if first != second:
            return None
        return first + second, first, 2, raw
    # "4 x 4" is four answers at four.
    return first * second, first, second, raw


def _strip_marks(line):
    """(text, marks) for a marking line — the mark taken off, never invented."""
    m = LINE_MARKS.search(line)
    if not m:
        m = BARE_MARKS.search(line)
    if not m:
        return ' '.join(line.split()), None
    return ' '.join(line[:m.start()].split()), int(m.group(1))


class Ask:
    """One priced ask, exactly as the scheme states it."""

    __slots__ = ('unit', 'rc', 'section', 'item', 'letter', 'letter_to',
                 'total', 'per', 'count', 'notation', 'cue', 'directives',
                 'answers', 'full', 'part', 'routes', 'notes', 'open_list',
                 'line', 'fault')

    def __init__(self, **kw):
        for k in self.__slots__:
            setattr(self, k, kw.get(k))

    @property
    def key(self):
        """(section token, item, letter, None) — the census key shape."""
        return (self.section, self.item, self.letter, None)

    def __repr__(self):
        return f'<Ask {self.section} {self.item}{self.letter or ""} {self.notation}>'


class FrScheme:
    """One published French marking scheme, read as a list of asks."""

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
        self.rc_totals = {}                # RC number -> the tariff it prints
        self.listen_totals = {}            # listening section -> its tariff
        self._read()

    # -- segmentation -------------------------------------------------------
    def _heads(self):
        """Every ask head in the file, with the unit it belongs to."""
        unit = None
        rc = None
        lsec = None
        out = []
        for i, line in enumerate(self.lines):
            if APPENDIX.match(line):
                break
            if UNIT_A.match(line):
                unit, rc, lsec = 'A', None, None
                continue
            if UNIT_L.match(line):
                unit, rc, lsec = 'L', None, None
                continue
            if unit != 'L' and UNIT_B.match(line):
                unit, rc, lsec = 'B', None, None
                continue
            if unit == 'A':
                m = RC_HEAD.match(line)
                if m:
                    rc = int(m.group(1))
                    self.rc_totals[rc] = int(m.group(2))
                    continue
                m = ITEM_HEAD.match(line)
                if m and rc is not None:
                    out.append((i, 'A', rc, None, int(m.group(1)),
                                m.group(2), m.group(3), m.group(4)))
                continue
            if unit == 'L':
                m = LISTEN_SECTION.match(line)
                if m:
                    lsec = m.group(1).upper()
                    self.listen_totals[lsec] = int(m.group(2))
                    continue
                m = LISTEN_ITEM.match(line)
                if m and lsec is not None:
                    out.append((i, 'L', None, lsec, int(m.group(1)),
                                m.group(2), None, None))
                continue
        return out

    def _stops(self):
        """Every line a block may not run past.

        A head alone is not enough. The last ask of Section A is followed by
        Section B's MARKING GRID and then by the listening test's own heads,
        and a block that ends only at the next ASK swallowed all of it: one
        2024 Higher marking point came out carrying "30 Marks 20 Marks" from
        the grid, priced at 30 on a five-mark question.
        """
        stops = set()
        for i, line in enumerate(self.lines):
            if (APPENDIX.match(line) or UNIT_A.match(line) or UNIT_B.match(line)
                    or UNIT_L.match(line) or RC_HEAD.match(line)
                    or LISTEN_SECTION.match(line)):
                stops.add(i)
        return stops

    def _read(self):
        heads = self._heads()
        stops = self._stops() | {h[0] for h in heads}
        for n, head in enumerate(heads):
            i = head[0]
            later = [s for s in stops if s > i]
            end = min(later) if later else len(self.lines)
            ask = self._parse(head, self.lines[i + 1:end])
            if isinstance(ask, str):
                self.refused.append((head, ask))
            else:
                self.asks.append(ask)
        self._checksum()

    def _checksum(self):
        """The SEC's own arithmetic, applied to each reading comprehension.

        A comprehension prints its total on its head — "Q.3 (40 marks)" — and
        that total is the only independent check this document offers on the
        item tariffs beneath it. Five comprehensions in the corpus fall exactly
        one answer short of their own total, and in every one of them the ask
        that is short DEMANDS TWO ANSWERS while its head prices one: 2021
        Ordinary Q.3(5) prints "Donnez deux exemples ... 4 Marks" and lists ten
        answers at four marks each, so the ask is worth eight and the head says
        four.

        Eight is not printed anywhere, so it is not used. The ask is faulted,
        and fr_all.py excludes it with this evidence rather than pricing a card
        at a number the SEC never wrote. Where the shortfall cannot be pinned
        on a specific ask, every ask in that comprehension is faulted: an
        unexplained disagreement means the reader may have lost an ask, and
        neither half of the tariff can be trusted then.
        """
        for rc, printed in self.rc_totals.items():
            asks = [a for a in self.asks if a.unit == 'A' and a.rc == rc]
            got = sum(a.total for a in asks if a.total)
            if got == printed:
                continue
            short = printed - got
            suspects = [a for a in asks
                        if a.count == 1 and a.per and MULTI_ANSWER.search(a.cue)]
            if short > 0 and suspects and sum(a.per for a in suspects) == short:
                for a in suspects:
                    a.fault = (
                        f'the head prices this ask {a.total} while the ask '
                        f'demands more than one answer and Q.{rc} prices its '
                        f'items {got} against its own printed {printed}; the '
                        f'value this ask is really worth is not printed')
                continue
            for a in asks:
                a.fault = a.fault or (
                    f'Q.{rc} prices its items {got} against its own printed '
                    f'{printed} and the difference cannot be pinned on one ask')

    def _appendix_at(self):
        for i, line in enumerate(self.lines):
            if APPENDIX.match(line):
                return i
        return len(self.lines)

    def _parse(self, head, block):
        _i, unit, rc, lsec, item, letter, letter_to, tariff = head
        section = f'A{rc}' if unit == 'A' else f'L{lsec}'

        total = per = count = notation = None
        if tariff:
            parsed = parse_tariff(tariff)
            if parsed is None:
                return f'the head tariff {tariff!r} is not a notation this reads'
            total, per, count, notation = parsed

        cue_lines, directives, notes = [], [], []
        answers, routes = [], []
        route = None
        cur = None                       # the marking line still accumulating
        open_list = False
        seen_answer = False
        in_note = False
        for line in block:
            s = line.strip()
            if not s or PAGE.match(s):
                continue
            if NOTE.match(s):
                in_note = True
                notes.append(s)
                continue
            if in_note and not (FULL_BULLET.match(s) or PART_BULLET.match(s)):
                # Everything from "Note:" to the next ask is the examiner's
                # instruction and its wrapped continuation -- unless a BULLET
                # opens beneath it, which closes the note. 2023 Higher Q.1 4(a)
                # prints its Note above "One of:" and its six answers, and a
                # note that ran to the end of the block swallowed all six.
                notes.append(NOTE_BULLET.sub('', s))
                continue
            if NOTE_BULLET.match(s):
                notes.append(NOTE_BULLET.sub('', s))
                continue
            m = ROUTE.match(s)
            if m:
                route = m.group(1).lower()
                routes.append(route)
                continue
            if OPEN_LIST.match(s):
                open_list = True
                continue
            if FULL_BULLET.match(s) or PART_BULLET.match(s):
                # A bullet closes the examiner's note. 2023 Higher Q.1 4(a)
                # prints "Note: / Two correct points = 5 Marks / One correct
                # point = 4 Marks" ABOVE "One of:" and its six answers, and a
                # note that ran to the end of the block swallowed all six.
                in_note = False
                bullet = bool(FULL_BULLET.match(s))
                body = (FULL_BULLET if bullet else PART_BULLET).sub('', s)
                text, marks = _strip_marks(body)
                cur = {'text': text, 'marks': marks, 'route': route,
                       'bullet': bullet}
                answers.append(cur)
                seen_answer = True
                continue
            if DIRECTIVE.match(s):
                directives.append(s)
                cur = None
                continue
            if not seen_answer:
                cue_lines.append(s)
            elif cur is not None:
                # A wrapped marking line. The SEC breaks a long answer across
                # two printed lines and sets the bullet on the first only, so
                # the second belongs to the line above it -- welding it to the
                # NEXT bullet instead is how an answer about one thing ends up
                # carrying the opening clause of another.
                text, marks = _strip_marks(s)
                cur['text'] = ' '.join(f"{cur['text']} {text}".split())
                if cur['marks'] is None:
                    cur['marks'] = marks

        if not answers and cue_lines:
            # The SEC's other way of stating an answer: a solidus list on a
            # line of its own, with no bullet in front of it. 2025 Ordinary
            # Q.4(5) answers "Relevez un verbe a l'infinitif" with "Voir /
            # (S')amuser / Descendre / (Se) laisser / Porter / Ramer/ Etre" --
            # every accepted answer, on one line, at the head tariff. Read as
            # part of the question it left the ask with no answer at all.
            if SOLIDUS_LIST.match(cue_lines[-1]):
                answers = [{'text': cue_lines[-1], 'marks': None,
                            'route': None, 'bullet': False}]
                cue_lines = cue_lines[:-1]

        cue = ' '.join(' '.join(cue_lines).split())
        answers = [a for a in answers if a['text']]
        # The per-answer value, read from the answers themselves wherever the
        # scheme prices them. The head states the ask's TOTAL — "4 Marks",
        # "4+4 Marks", "4 x 4 Marks" — and the number of answers it buys is the
        # total divided by what one answer is worth. Reading the head's first
        # number as the per-answer value instead priced 2024 Ordinary Q.1's
        # seventh ask at one answer when its own four options are printed at
        # two marks each and the paper prints two answer lines.
        priced = [a['marks'] for a in answers if a['marks'] is not None]
        fault = None
        if priced:
            per = max(priced)
        if total is not None and per:
            if total % per:
                fault = (f'the head prices this ask {total} and its answers '
                         f'{per} each, which does not divide')
            else:
                count = total // per
        full = [a for a in answers if a['marks'] is None or a['marks'] == per]
        part = [a for a in answers if a['marks'] is not None and a['marks'] < per]
        return Ask(unit=unit, rc=rc, section=section, item=item,
                   letter=letter, letter_to=letter_to, total=total, per=per,
                   count=count, notation=notation, cue=cue,
                   directives=directives, answers=answers, full=full,
                   part=part, routes=routes, notes=notes,
                   open_list=open_list, line=_i, fault=fault)

    # -- lookups ------------------------------------------------------------
    def ref(self, ask):
        tail = f'Q{ask.item}'
        if ask.letter:
            tail += f'({ask.letter})'
            if ask.letter_to:
                tail += f'–({ask.letter_to})'
        return f'{self.year} {self.level.upper()} Section {ask.section} {tail}'

    def gap_fill(self):
        """The Ordinary written-production cloze, or None.

        Section B is a band grid everywhere else — Communication and Language,
        TOP/MIDDLE/BOTTOM — but its first Ordinary alternative is a gap-fill,
        and the scheme prints the ten words themselves against a printed
        tariff: "(a) Filling Gaps – 30 marks / 10 gaps for 3 marks each".
        That is an answer, and excluding it with the rest of Section B would be
        a claim about this document that is not true.
        """
        head = mult = None
        answers = {}
        for i, line in enumerate(self.lines):
            if head is None:
                m = GAP_HEAD.match(line.strip())
                if m:
                    head = int(m.group(1))
                continue
            if mult is None:
                m = GAP_RATE.match(line.strip())
                if m:
                    gaps, per = int(m.group(1)), int(m.group(2))
                    if gaps * per != head:
                        return None      # the two halves of the tariff disagree
                    mult = (gaps, per)
                continue
            for n, word in GAP_ANSWER.findall(line):
                answers.setdefault(int(n), word.strip())
            if len(answers) >= mult[0]:
                break
        if not mult or len(answers) != mult[0]:
            return None
        gaps, per = mult
        return {'total': head, 'per': per, 'gaps': gaps,
                'answers': [(n, answers[n]) for n in sorted(answers)]}

    def reading(self):
        return [a for a in self.asks if a.unit == 'A']

    def listening(self):
        return [a for a in self.asks if a.unit == 'L']


def audit(subject=SUBJECT):
    """Every scheme, with the checks that would catch a mis-read.

    1. The item tariffs inside one reading comprehension must add up to the
       total that comprehension prints on its own head. That is the SEC's own
       arithmetic, and it is the only independent check this document offers
       on whether an ask was missed or a tariff mis-read.
    2. Every full-mark bullet in an ask carries the same printed mark, and it
       is the per-answer value the head states.
    """
    bad = 0
    for path in sorted(glob.glob(os.path.join(schemes_dir(subject), '*.md'))):
        stem = os.path.basename(path)[:-3]
        year, level = int(stem[:4]), stem[5:]
        S = FrScheme(year, level, subject)
        read = S.reading()
        print(f'{stem}: {len(read)} reading asks, {len(S.listening())} listening '
              f'asks, {len(S.refused)} refused')
        for rc, printed in sorted(S.rc_totals.items()):
            got = sum(a.total for a in read if a.rc == rc)
            flag = '' if got == printed else '   <-- MISMATCH'
            if got != printed:
                bad += 1
            print(f'    Q.{rc}: heads sum {got}, the scheme prints {printed}{flag}')
        for a in read:
            if a.fault:
                bad += 1
                print(f'    {S.ref(a)}: {a.fault}')
            marks = {b['marks'] for b in a.full if b['marks'] is not None}
            if marks and marks != {a.per}:
                bad += 1
                print(f'    {S.ref(a)}: full answers priced {sorted(marks)}, '
                      f'per-answer value is {a.per}')
        for head, why in S.refused:
            print(f'    REFUSED line {head[0]}: {why}')
    return 1 if bad else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('year', nargs='?', type=int)
    ap.add_argument('level', nargs='?')
    ap.add_argument('--subject', default=SUBJECT)
    ap.add_argument('--audit', action='store_true')
    ap.add_argument('--full', action='store_true')
    ap.add_argument('--listening', action='store_true')
    args = ap.parse_args()
    if args.audit or not args.year:
        return audit(args.subject)
    S = FrScheme(args.year, args.level, args.subject)
    asks = S.listening() if args.listening else S.reading()
    print(f'{args.year} {args.level.upper()}: {len(asks)} asks')
    for a in asks:
        print(f'  {S.ref(a):<32} {str(a.notation):<12} '
              f'{len(a.full)} full, {len(a.part)} part'
              f'{" +etc" if a.open_list else ""}')
        print(f'      ASK  {a.cue[:150]}')
        if args.full:
            for b in a.full:
                print(f'      *    [{b["marks"]}] {b["text"][:130]}')
            for b in a.part:
                print(f'      -    [{b["marks"]}] {b["text"][:130]}')
            for n in a.notes:
                print(f'      NOTE {n[:120]}')
    for head, why in S.refused:
        print(f'  REFUSED line {head[0]}: {why}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
