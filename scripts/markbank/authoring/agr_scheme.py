#!/usr/bin/env python3
"""Ancient Greek marking schemes — the tariff table and the stated answers.

    python3 scripts/markbank/authoring/agr_scheme.py 2023 hl
    python3 scripts/markbank/authoring/agr_scheme.py --survey

An Ancient Greek scheme is TWO documents bound together, and only the second
one answers anything.

**The tariff table** comes first and prices every ask in the paper's own
address. For the translation questions it prices the SOURCE — the Greek the
candidate is GIVEN, cut into units with a mark after each::

    A (i)  ἔπειτα δὲ γίγνεται .................. πορεύεσθαι·        7
           οὐ γὰρ ............................... ἐπιτήδεια.        4

That is Latin's finding, in Greek: nothing there is an answer, and the same
goes for Question 1 Section A, where the priced text is the ENGLISH the
candidate has to turn into Greek. For the literature questions it prices them
in bands the candidate's own answer is measured against: "Impression ex 10",
"5 + 5", "8 + 8 + 7 + 7". Those ARE tariffs, and the printed expression rides
on the card's note verbatim — it tells a student the examiner splits thirty
marks four ways.

**"Additional notes and indicative answers"** comes second and is where the
subject becomes cardable. It states, in English, what the answer is::

    Qu. 1B
    (a) He decided to climb a tower.
    ...
    Qu 3A(ii)
    (a) Alcibiades was recalled to face charges of profaning the Mysteries
        and mutilating the Hermae.

Thirteen of the sixteen schemes on disk carry that section: every Higher
scheme, and one of the three Ordinary ones (2015). 2019 and 2023 Ordinary print
the tariff table and stop — so their literature asks have a printed price and
no stated answer, which is an exclusion with the scheme as its evidence and not
a reader fault. `--survey` counts it.

Heading spellings the SEC has used for the same thing, all of them in this
corpus: "Qu. 1B", "Qu.  3A (ii)", "Qu 3A(ii)", "Q.  3B (ii)", "Qu  4A",
"Q. 4B", "Qu. 4", "Qu. 2. (ii).", "Qu. 3. B".
"""
import argparse
import os
import re
import sys

import pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))

import agr_text                                               # noqa: E402
from markbank_text import unligature                          # noqa: E402

SUBJECT = 'ancient-greek'
ROMANS = ['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x']
LETTERS = 'abcdefgh'
ROW_BAND = 5

# The head of the answers section, in every spelling the corpus prints.
NOTES = re.compile(r'^ADDITIONAL\s+NOTES|^Additional\s+[Nn]otes', re.I)
# "Qu. 1B", "Q. 3A (ii)", "Qu 3A(ii)", "Qu. 2. (ii).", "Qu. 3. B", "Qu. 4"
NOTE_HEAD = re.compile(
    r'^Qu?\s*\.?\s*(\d)\s*\.?\s*([AB])?\s*\.?\s*'
    r'(?:\(\s*(' + '|'.join(ROMANS) + r')\s*\)?\.?)?\s*(?![\dA-Za-z])')
# A question head in the TARIFF table: the digit comes first there, and the
# letter first in the answers section. That one difference is what separates
# the two halves of the document without needing the "ADDITIONAL NOTES"
# heading, which three of the schemes do not print at all.
# The route letter must carry its own full stop. Without that, "4. Answer any
# three questions" handed back route "A" — the A of "Answer" — and every
# Question 4 tariff in the 2021-2024 schemes was filed under a Section A that
# those papers do not print.
# The route letter must carry its own full stop, or stand at the end of the
# row. Without the stop rule, "4. Answer any three questions" handed back route
# "A" — the A of "Answer" — and every Question 4 tariff in the 2021-2024
# schemes was filed under a Section A that those papers do not print. Without
# the end-of-row rule, 2023's "1.B" (no stop at all) lost Section B and filed
# the whole comprehension under no route.
Q_HEAD = re.compile(
    r'^(\d)\s*\.\s*(?:([A-D])\s*(?:\.|(?=\s*(?:$|\[))))?\s*(?![\d])')
ROUTE_HEAD = re.compile(r'^([A-D])\s*\.?\s*(?:$|\(|Either|Answer|Translate)')
MARKER = re.compile(r'^\(?\s*(' + '|'.join(ROMANS) + '|[' + LETTERS
                    + r'])\s*\)\.?\s*')
# A per-part rate the scheme states on a head: "(3 x 10 marks)", "(4 x 10)".
RATE = re.compile(r'\(\s*(\d)\s*[x×]\s*(\d{1,3})\s*(?:marks?)?\s*\)', re.I)
# A positive integer that is not part of a year, a century or a deduction.
NUM = re.compile(r'(?<![-\dA-Za-z.])(\d{1,3})(?![\d])')


# Rows the SEC itself printed wrong. Each is keyed by the sitting and matched
# against the whole printed row, never by a heuristic — the correction is what
# the PAPER prints at that address, which is the evidence for each one.
MISPRINTS = {
    # The Question 4 head, set as a roman. The paper heads it "4. Answer any
    # two of the following questions. (Each question carries thirty marks)"
    # and prints [60] on it, which is the total this row states. Read as a
    # roman it opened an eighth part of Question 3 Section B and carried
    # Question 4's whole run of eight topics into it.
    (2022, 'hl'): [('(iii) Answer two questions. (2 x 30) [60]',
                    '4. Answer two questions. (2 x 30) [60]')],
    # A roman set as a letter the schemes never use. "Qu 4A" runs (i), (ii),
    # (iii) and then this; the paper's Question 4 Section A runs (i) to (iv)
    # and its (iv) asks about a dramatist, which is what the row answers.
    (2018, 'hl'): [
        # A roman set as a letter the schemes never use, under "Qu. 4B" whose
        # run then continues (ii), (iii), (iv). The paper's Question 4 Section
        # B(i) asks a candidate to "write briefly about the life and works of
        # the dramatist who, in your view, made the greatest contribution",
        # which is what this row answers.
        ('(j) Dramastist: Life; Works; Contribution; Justify',
         '(i) Dramastist: Life; Works; Contribution; Justify'),
        # Question 4 Section A(iv)'s answer, printed with no marker at all so
        # that it reads as a continuation of (iii)'s. The paper's 4A(iv) asks
        # "What were the main features of the ancient Spartan system of
        # government? Explain briefly your own view", which is this row and
        # the line under it.
        ('Spartan Government: Kings; Gerousia; Apella; Ephors; Militaristic '
         'culture.',
         '(iv) Spartan Government: Kings; Gerousia; Apella; Ephors; '
         'Militaristic culture.'),
    ],
    # Question 3's eighth topic, numbered (vii) a second time. The paper prints
    # (i) to (viii) and the scheme prices eight rows; the two (vii)s carry
    # different splits, so the row is named by its own text and not by which
    # of the two it is.
    (2023, 'ol'): [('(vii) (8 + 7) + (8 + 7)', '(viii) (8 + 7) + (8 + 7)')],
}


def scheme_path(year, level, subject=SUBJECT):
    path = os.path.join(ROOT, 'examiner-reports', subject, 'schemes',
                        f'{year}-{level}.pdf')
    if not os.path.exists(path):
        raise FileNotFoundError(f'no {subject} scheme for {year} {level}')
    return path


def has_scheme(year, level, subject=SUBJECT):
    return os.path.exists(os.path.join(ROOT, 'examiner-reports', subject,
                                       'schemes', f'{year}-{level}.pdf'))


def _clean(text):
    return unligature(' '.join(str(text).split())).replace('‐', '-').strip()


class Entry:
    """One address in the scheme: what it prices, and what it states."""
    __slots__ = ('section', 'q', 'letter', 'roman', 'marks', 'note', 'answer')

    def __init__(self, section, q, letter, roman):
        self.section, self.q = section, q
        self.letter, self.roman = letter, roman
        self.marks = None
        # The scheme's own printed split, verbatim — "8 + 8 + 7 + 7",
        # "Impression ex 10", "Each incorrect quantity: -2." It is a
        # partial-credit ladder and rides on the card's row note; it is NEVER
        # turned into a RowKind of its own.
        self.note = None
        self.answer = None

    @property
    def key(self):
        return (self.section, self.q, self.letter, self.roman)

    def __repr__(self):
        return (f'<Entry {self.key} {self.marks}m note={self.note!r} '
                f'ans={(self.answer or "")[:40]!r}>')


class AgrScheme:
    def __init__(self, year, level, subject=SUBJECT):
        self.year, self.level, self.subject = year, level, subject
        self.path = scheme_path(year, level, subject)
        self._doc = pymupdf.open(self.path)
        self._entries = None
        self.question_marks = {}
        self.states_answers = False

    # ------------------------------------------------------------- text ----
    def _rows(self):
        """Printed rows, SPIonic decoded, a table row rebuilt from its cells.

        The scheme is a TABLE: "(a)" sits in one cell and "6" in another, on
        the same visual row. Read cell by cell, every tariff in the document is
        a line holding one bare number and nothing else.
        """
        out = []
        for pno in range(len(self._doc)):
            page = self._doc[pno]
            lines = []
            for block in page.get_text('dict')['blocks']:
                if block.get('type') != 0:
                    continue
                for line in block['lines']:
                    text = ''.join(
                        agr_text.decode(s['text'])
                        if agr_text.FONT in s['font'] else s['text']
                        for s in line['spans'])
                    if not text.strip():
                        continue
                    x0, y0, _, y1 = line['bbox']
                    lines.append(((y0 + y1) / 2, x0, text))
            rows, anchor = [], None
            for y, x, text in sorted(lines):
                if anchor is None or y - anchor > ROW_BAND:
                    rows.append([])
                    anchor = y
                rows[-1].append((x, text))
            for row in rows:
                text = _clean(' '.join(t for _, t in sorted(row)))
                if text:
                    out.append((pno + 1, text))
        fixes = MISPRINTS.get((self.year, self.level), [])
        if fixes:
            done = set()
            for i, (pg, text) in enumerate(out):
                for wrong, right in fixes:
                    if text == wrong and wrong not in done:
                        out[i] = (pg, right)
                        done.add(wrong)
            missing = [w for w, _ in fixes if w not in done]
            if missing:
                raise AssertionError(
                    f'{self.year} {self.level}: misprint row not found, so the '
                    f'correction is stale: {missing[0]!r}')
        return out

    # ----------------------------------------------------------- parsing ---
    def entries(self):
        if self._entries is None:
            self._entries = self._parse()
        return self._entries

    def _parse(self):
        rows = self._rows()
        # Where the answers begin: the "ADDITIONAL NOTES" heading if the
        # scheme prints one, otherwise the first heading whose LETTER comes
        # before its digit ("Q. 1B"), which is the shape only the answers
        # section uses.
        split = len(rows)
        for i, (_pg, text) in enumerate(rows):
            if NOTES.match(text):
                split = i
                break
            if NOTE_HEAD.match(text) and not Q_HEAD.match(text):
                split = i
                break
        entries = {}
        self._table(rows[:split], entries)
        self.states_answers = split < len(rows)
        if self.states_answers:
            self._notes(rows[split:], entries)
        return entries

    def _get(self, entries, key):
        if key not in entries:
            entries[key] = Entry(*key)
        return entries[key]

    def _table(self, rows, entries):
        """The tariff half: question, route, roman, letter, and its price."""
        q = route = roman = None
        rate = {}
        seen = set()          # (q, route, roman) already priced
        for _pg, text in rows:
            m = Q_HEAD.match(text)
            if m:
                q, route, roman = int(m.group(1)), m.group(2), None
                seen = set()
                total = re.search(r'\[\s*(\d{1,3})\s*\]', text)
                if total:
                    self.question_marks[q] = int(total.group(1))
                text = text[m.end():].strip()
                r = RATE.search(text)
                if r:
                    rate[(q, route, roman)] = int(r.group(2))
                if not text:
                    continue
            m = ROUTE_HEAD.match(text)
            if m and q is not None:
                route, roman = m.group(1), None
                text = text[m.end(1):].lstrip(' .').strip()
            if q is None:
                continue
            m = MARKER.match(text)
            if not m:
                continue
            tok, rest = m.group(1), text[m.end():].strip()
            if tok in ROMANS and (tok not in LETTERS or roman is None):
                # A lone "i" or "v" is a roman here: the schemes never letter
                # past (h), and the two runs never collide inside one unit.
                if route is not None and (q, route, tok) in seen:
                    # The roman run RESTARTED, which is the scheme opening the
                    # question's next route with no head to say so: 2017 sets
                    # "3. Section A or Section B", heads Section A, and then
                    # prints Section B's "(i) Translate into English. (50)"
                    # with no "B." above it. Read without this, Section B's
                    # five literature parts had no tariff at all and Section
                    # A's kept the first of the two.
                    route = chr(ord(route) + 1)
                roman, letter = tok, None
            else:
                letter = tok
            seen.add((q, route, roman))
            # A roman and the first letter beneath it are set on ONE printed
            # row: 2023 Higher prices "(viii) (a) 5 + (5 + 5)". Read as one
            # marker the fifteen marks landed on (viii) itself and (a) was
            # never priced at all.
            m2 = MARKER.match(rest)
            if m2 and letter is None and m2.group(1) in LETTERS \
                    and m2.group(1) not in ROMANS:
                letter, rest = m2.group(1), rest[m2.end():].strip()
            r = RATE.search(rest)
            if r:
                rate[(q, route, roman)] = int(r.group(2))
            key = (route, q, letter, roman)
            entry = self._get(entries, key)
            marks, note = self._value(rest)
            if marks is None and note is not None:
                marks = rate.get((q, route, roman)) \
                    or rate.get((q, route, None)) or rate.get((q, None, None))
            if marks is not None and entry.marks is None:
                entry.marks = marks
            if note and entry.note is None:
                entry.note = note
        return entries

    @staticmethod
    def _value(text):
        """(marks, printed note) for one priced line of the tariff table.

        "6" is six marks and no note. "Impression ex 10", "5 + 5",
        "8 + 8 + 7 + 7" and "(8 + 7) + (8 + 7)" are the scheme's own splits:
        the marks are their sum and the printed expression is the note, kept
        VERBATIM. "Each incorrect quantity: -2." states a deduction and no
        total at all, so it is a note with no marks and the rate stated on the
        head above it prices the ask.
        """
        text = text.strip().rstrip('.').strip()
        if not text:
            return None, None
        if re.fullmatch(r'\d{1,3}', text):
            return int(text), None
        # A line of Greek priced per unit is the SOURCE, not an answer.
        if re.search(r'[Ͱ-Ͽἀ-῿]', text) or '…' in text or '....' in text:
            return None, None
        if re.search(r'\b(?:Translate|Answer|Either|marks?\))', text):
            return None, None
        nums = [int(n) for n in NUM.findall(text)]
        total = sum(nums) if nums else None
        return total or None, _clean(text)

    def _notes(self, rows, entries):
        """The answers half: an English answer under each printed address."""
        q = route = roman = letter = None
        buf = []

        def flush():
            if q is None or not buf:
                return
            if route is None and roman is None and letter is None:
                # A note attached to the QUESTION and to no part of it is the
                # scheme talking to examiners, not answering an ask: "Qu. 2 -
                # Each mark allocation represents a complete unit of meaning
                # to be translated." Filed as an entry it reported an orphan
                # at an address the paper does not print.
                return
            text = _clean(' '.join(buf))
            if not text:
                return
            entry = self._get(entries, (route, q, letter, roman))
            entry.answer = text if entry.answer is None \
                else f'{entry.answer} {text}'

        for _pg, text in rows:
            if NOTES.match(text):
                continue
            if re.fullmatch(r'(?:Page\s+\d+\s+of\s+\d+|\d{1,3}|NB:.*)', text):
                continue
            m = NOTE_HEAD.match(text)
            if m and not Q_HEAD.match(text):
                flush()
                buf = []
                q, route = int(m.group(1)), m.group(2)
                roman, letter = m.group(3), None
                rest = text[m.end():].strip()
                if rest:
                    text = rest
                else:
                    continue
            if q is None:
                continue
            m = MARKER.match(text)
            if m:
                tok = m.group(1)
                # A roman printed AFTER a letter is the SEC cutting one
                # answer in two, not an address: 2010 answers Question 1
                # Section B(c) "(i) He had been a slave. (ii) He recognized
                # the language of the people." Read as addresses, five of the
                # comprehension's answers were filed under parts the paper
                # never printed and their own asks had none.
                is_roman = tok in ROMANS and letter is None
                if is_roman or tok in LETTERS:
                    flush()
                    buf = []
                    if is_roman:
                        roman, letter = tok, None
                    else:
                        letter = tok
                    text = text[m.end():].strip()
                    # "(iv) (a) Archaic period." — a roman and the first
                    # letter beneath it on ONE row, which is how every routed
                    # Question 4 states its photograph answers. Read as one
                    # marker, (a)'s answer was filed on (iv) and the ask that
                    # cites (a) had none.
                    m2 = MARKER.match(text)
                    if m2 and is_roman and m2.group(1) in LETTERS \
                            and m2.group(1) not in ROMANS:
                        letter, text = m2.group(1), text[m2.end():].strip()
            buf.append(text)
        flush()
        return entries

    # ---------------------------------------------------------------------
    def priced(self):
        return {k: e for k, e in self.entries().items() if e.marks is not None}

    def answered(self):
        return {k: e for k, e in self.entries().items() if e.answer}


def survey():
    from agr_paper import sittings
    print(f"{'sitting':10} {'scheme':>7} {'priced':>7} {'answered':>9}  notes")
    for year, level in sittings():
        if not has_scheme(year, level):
            print(f'{year} {level:<5} {"—":>7}  no marking scheme published '
                  f'for this sitting')
            continue
        S = AgrScheme(year, level)
        S.entries()
        print(f'{year} {level:<5} {"yes":>7} {len(S.priced()):>7} '
              f'{len(S.answered()):>9}  '
              f'{"states answers" if S.states_answers else "TARIFFS ONLY"}')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('year', nargs='?', type=int)
    ap.add_argument('level', nargs='?')
    ap.add_argument('--survey', action='store_true')
    args = ap.parse_args()
    if args.survey:
        survey()
        return 0
    S = AgrScheme(args.year, args.level)
    for key in sorted(S.entries(), key=lambda k: (k[1], str(k[0]), str(k[3]),
                                                  str(k[2]))):
        e = S.entries()[key]
        print(f'  {str(key):26} {str(e.marks or "-"):>4} {str(e.note or "")[:24]:24} '
              f'{(e.answer or "")[:60]}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
