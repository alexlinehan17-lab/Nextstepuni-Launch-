#!/usr/bin/env python3
"""The Arabic marking scheme, read as a table of priced answers.

    python3 scripts/markbank/authoring/ara_scheme.py 2025 hl
    python3 scripts/markbank/authoring/ara_scheme.py --report

The scheme is one table across every page, printed right to left: the QUESTION
column at the right names the question in English words — One, Two, … Fifteen —
the MARKS column sits beside it, and the ANSWER fills the rest of the measure
in Arabic. Its fifteen questions are the paper's fifteen, in order.

HOW IT IS JOINED TO THE PAPER (Law 4)
-------------------------------------
Not on wording: the scheme never reprints the question it is answering. On the
NUMBER and, under it, on the printed PART LETTER — and only because two counts
that do not depend on each other agree first, which is the check Italian had to
pass before its order-join was allowed:

  * every question the scheme prices is priced the same as the paper prices it,
    in all ten sittings and all 370 asks; and
  * the part letters the scheme prints under a question are the same letters,
    in the same order, as the paper prints — with the one exception the SEC
    itself makes, 2023 Ordinary lettering its fifth part ذ where the paper
    letters it ه, which is checked and named rather than silently accepted.

WHAT IT STATES AND WHAT IT DOES NOT
-----------------------------------
Two of its fifteen questions state an answer a card can lift:

  * Q1-4, the comprehension key. The scheme prints the option letter it accepts
    and, in most sittings, that option's text as well.
  * Q10-14, the grammar. "(أ) تسافر: مضارع منصوب بأٔن." against a printed 3
    marks, and Q11's own split stated under the table: "2 marks allocated for
    each ending accent and 1 mark for the justification".

The other eleven — Q5, Q6, the nine literature alternatives of Q7-9, and the
composition Q15 — are marked by a Communication-and-Content grid over a
non-exhaustive list headed "تجدر الإشارة إلى:" ("it should be noted"). That is
the same written-production exclusion the six carded languages carry.
"""
import argparse
import collections
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))

import pymupdf                                                # noqa: E402
import ara_text                                               # noqa: E402
from ara_paper import LETTERS                                 # noqa: E402

SCHEMES = os.path.join(ROOT, 'examiner-reports', 'arabic', 'schemes')

WORDS = ['One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight',
         'Nine', 'Ten', 'Eleven', 'Twelve', 'Thirteen', 'Fourteen', 'Fifteen']
WORD_NO = {w: i + 1 for i, w in enumerate(WORDS)}
# A starred question is still that question: the SEC stars Nine to mark the
# alternative set a candidate may take instead of Seven or Eight.
QWORD = re.compile(r'\*?\b(' + '|'.join(WORDS) + r')\b')
TOTAL = re.compile(r'(\d+)\s*[Mm]arks?\s*Total')
MARKS = re.compile(r'(\d+)\s*[Mm]arks?\b')
# A part letter, with the stray digit the SEC sometimes leaves inside the
# bracket — 2021 Higher prints "(ب٠)تقرأ" and 2025 Higher "0(أ) تسافر".
# A part letter, delimited. It must close with a bracket or a dash: a bare
# letter and a space matched the alef that OPENS الكتاب and cut the word in
# half. The SEC vowels its part letters as often as not — "بِ- الغرفة",
# "(أٔ)َ زميله" — so a diacritic is allowed anywhere in the token, and the
# stray digit it sometimes leaves in the bracket with them.
# The brackets are not always the right way round: Word stores the mirrored
# character for a parenthesis that OPENS an Arabic clause, so the same scheme
# prints "(ج)" on one row and "ج(" on the next. Both are the same label.
MARK = r'[\u064B-\u0655\u0670]*'
LETTER = r'أ|ا|ب|ج|د|هـ|ه|ذ'
PART = re.compile(rf'^[\s0-9٠-٩۰-۹]*(?:'
                  rf'[()]\s*(?P<b>{LETTER}){MARK}\s*[٠-٩۰-۹]?{MARK}\s*[()]{MARK}'
                  rf'|(?P<d>{LETTER}){MARK}\s*[-–—()]'
                  rf')\s*[-–—]?\s*(?P<rest>.*)$')
# The scheme's own front matter, which prices nothing.
FURNITURE = re.compile(
    r'Coimisi|State Examinations|Marking Scheme|Leaving Certificate|'
    r'Note to teachers|marking schemes|Future Marking|^Answer$|^Marks$|'
    r'^Question$|^Arabic$|^(Higher|Ordinary) Level$', re.I)
# The three rows of the content-and-expression grid, and the head that opens
# the non-exhaustive list above it.
GRID = re.compile(r'Communication and Content|Knowledge and Application of '
                  r'Language|Accuracy of Language|For any answered essay', re.I)
INDICATIVE = 'تجدر الإشارة'
# How far BELOW a row its own question label may be printed. The label is set
# in the middle of a cell two or three lines deep, so it can fall a few points
# under the answer's baseline — seven, on 2023 Higher page 3 and 2021 Higher
# page 13. Nothing in the corpus puts a label further under its own row, and
# the next question's label is a hundred points away.
LABEL_GRACE_PT = 15.0

# The SEC's own mis-lettering, keyed (subject, year, level) -> {(question,
# row index from the top): the letter the PAPER prints}. 2025 Ordinary letters
# both the fourth and the fifth part of Q13 "(د)"; the paper letters them (د)
# and (ه), and the paper wins. Listed, never inferred: a rule that renumbered
# any repeated letter would quietly rewrite a scheme that meant it.
SCHEME_MISPRINTS = {
    ('arabic', 2025, 'ol'): {(13, 4): 'e'},
}


class Row:
    """One priced line of the scheme."""

    __slots__ = ('question', 'letter', 'arabic_letter', 'text', 'marks',
                 'page', 'y')

    def __init__(self, question, arabic_letter, text, marks, page, y=0.0):
        self.question = question
        self.arabic_letter = arabic_letter
        self.letter = LETTERS.get(arabic_letter) if arabic_letter else None
        self.text = text
        self.marks = marks
        self.page = page
        self.y = y

    @property
    def key(self):
        return (self.question, self.letter)

    def __repr__(self):
        return f'<Row Q{self.question}({self.letter}) {self.marks} {self.text[:30]!r}>'


class AraScheme:
    """One sitting's marking scheme."""

    def __init__(self, year, level):
        self.year, self.level = year, level
        self.path = os.path.join(SCHEMES, f'{year}-{level}.pdf')
        if not os.path.exists(self.path):
            raise FileNotFoundError(self.path)
        self.rows = []
        self.totals = {}            # question -> the "N marks Total" it prints
        self.grid = set()           # questions marked by the C&E grid
        self.notes = {}             # question -> the split it states in English
        self._read()

    def _read(self):
        """Walk each page as a table and give every row the label beside it.

        The question label sits in the rightmost column and is set in the
        MIDDLE of its cell, so it does not always share a baseline with the
        answer it names: the 2023 Higher comprehension prints "One" beside its
        answer, "Two" on the line BELOW its answer, and "Three" beside its own
        again. Treating a label as opening everything after it put Q11's first
        part under Q10 and left Q2 with no answer at all.

        So a row takes the LAST label printed at or above it, with one line's
        grace below — the label is set in the middle of a cell that is often
        two lines deep, and "Two" is printed seven points below the answer it
        names. A hundred points below is a different question: on 2025 Higher
        page 13, "Eleven" sits ninety-nine points under Q10's fifth part, and
        a nearest-label rule handed that part to Q11.

        The order-join this rests on is the one Italian had to earn, and it is
        earned here by the two checks in flags(): the scheme's totals agree
        with the paper's tariffs, and its part letters agree with the paper's.
        """
        doc = pymupdf.open(self.path)
        current = 0
        try:
            for pno, page in enumerate(doc, 1):
                entries, labels = [], []
                lines = ara_text.page_lines(page)
                marks_x = self._marks_column(lines)
                for line in lines:
                    text = line['text']
                    y = (line['bbox'][1] + line['bbox'][3]) / 2
                    if FURNITURE.search(text):
                        continue
                    for qm in QWORD.finditer(text):
                        labels.append((y, WORD_NO[qm.group(1)]))
                    text = QWORD.sub(' ', text).strip()
                    tm = TOTAL.search(text)
                    total = int(tm.group(1)) if tm else None
                    if tm:
                        text = TOTAL.sub(' ', text).strip()
                    grid = bool(GRID.search(text))
                    marks = None
                    mm = MARKS.search(text)
                    if mm and not grid:
                        marks = int(mm.group(1))
                        text = MARKS.sub(' ', text).strip()
                    text = re.sub(r'\s+', ' ', text).strip(' .••·')
                    if (marks is None and marks_x is not None
                            and line['bbox'][2] > marks_x
                            and re.match(r'^\d{1,3}\s+\S', text)):
                        # The marks cell sits at the RIGHT of the row, which is
                        # where a right-to-left line begins, so its bare number
                        # lands at the head of the assembled text.
                        head, text = text.split(None, 1)
                        marks = int(head)
                    elif (marks is None and marks_x is not None
                            and text.isdigit() and len(text) <= 3
                            and abs(line['bbox'][0] - marks_x) < 2.0):
                        # 2021 Ordinary prices its parsing ask with a bare "5"
                        # in the marks column and no word beside it. A number
                        # standing alone in that column is a tariff; the same
                        # number anywhere else on the page is the folio.
                        marks, text = int(text), ''
                    entries.append({'y': y, 'text': text, 'marks': marks,
                                    'page': pno, 'grid': grid, 'total': total})
                current = self._place(entries, labels, current)
        finally:
            doc.close()

    @staticmethod
    def _marks_column(lines):
        """Where this page sets its marks cells, read off the ones that say so."""
        xs = collections.Counter(round(l['bbox'][0], 1) for l in lines
                                 if MARKS.search(l['text']))
        if not xs:
            return None
        x, n = xs.most_common(1)[0]
        return x if n >= 2 else None

    def _place(self, entries, labels, current):
        pending = [None]
        for entry in entries:
            above = [q for y, q in labels if y <= entry['y'] + LABEL_GRACE_PT]
            if above and above[-1] >= current:
                current = above[-1]
            if not current:
                continue
            q = current
            if entry['total'] is not None:
                self.totals[q] = entry['total']
            if entry['grid']:
                self.grid.add(q)
                continue
            text = entry['text']
            if not text:
                # A tariff printed in the marks column on its own baseline.
                # It belongs to whichever of its neighbours has none: the SEC
                # sets the cell a point above its answer as often as a point
                # below it.
                if entry['marks'] is not None:
                    # The cell belongs to whichever neighbour shares its
                    # printed row. A tariff two lines up is the tariff of a
                    # DIFFERENT answer: 2021 Ordinary sets the first "5" of its
                    # parsing ask above the table's own head, and attaching it
                    # there lost a marking point and left the ask short.
                    if (self.rows and self.rows[-1].question == q
                            and self.rows[-1].marks is None
                            and abs(self.rows[-1].y - entry['y']) < 8.0):
                        self.rows[-1].marks = entry['marks']
                    else:
                        pending[0] = entry['marks']
                continue
            if text.isdigit():           # a page number, not an answer
                continue
            if self._is_english_note(text):
                self.notes.setdefault(q, []).append(text)
                continue
            pm = PART.match(text)
            marks = entry['marks']
            if marks is None and pending[0] is not None:
                marks, pending[0] = pending[0], None
            if pm:
                # A comprehension key states the OPTION LETTER and nothing
                # else: 2024 Higher answers its four asks "(أ) (ب) (ج) (ج)".
                # A row with a letter and no words is that answer, not a row
                # to be dropped for having no text.
                self.rows.append(Row(q, pm.group('b') or pm.group('d'),
                                     pm.group('rest').strip(), marks,
                                     entry['page'], entry['y']))
            else:
                self.rows.append(Row(q, None, text, marks, entry['page'],
                                     entry['y']))
        return current

    @staticmethod
    def _is_english_note(text):
        """A line of English under the table: what the scheme says about marking."""
        letters = [c for c in text if c.isalpha()]
        if not letters:
            return False
        return (sum(1 for c in letters if c.isascii()) / len(letters) > 0.8
                and len(text) > 12)

    # ----------------------------------------------------------------- views
    def aligned(self, question, paper_letters):
        """The scheme's rows for one question, against the paper's parts.

        Where the scheme letters its rows and those letters are the paper's,
        the letter is the join. Where it does not — 2021 Ordinary leaves the
        bracket off Q10's second part — the rows are taken in printed ORDER,
        which is safe here only because the counts match and the tariffs agree
        (see flags()). Returns (paper letter, row) pairs, and raises nothing:
        a question whose counts do not match comes back empty and is refused
        by name in ara_all.
        """
        rows = [r for r in self.by_question().get(question, [])
                if r.text or r.letter]
        fixes = SCHEME_MISPRINTS.get(('arabic', self.year, self.level), {})
        for i, r in enumerate(rows):
            if (question, i) in fixes:
                r.letter = fixes[(question, i)]
        if not paper_letters:
            return [(None, r) for r in rows]
        if len(rows) != len(paper_letters):
            return []
        printed = [r.letter for r in rows]
        if printed == paper_letters:
            return list(zip(paper_letters, rows))
        if all(p is None or p in paper_letters for p in printed):
            return list(zip(paper_letters, rows))
        return []

    def by_question(self):
        out = collections.defaultdict(list)
        for r in self.rows:
            out[r.question].append(r)
        return out

    def indicative(self, question):
        """Is this question marked by the grid rather than a stated answer?"""
        return question in self.grid

    def flags(self, paper):
        """Everything about this sitting the paper and the scheme disagree on."""
        out = []
        by_q = self.by_question()
        for q in range(1, 16):
            if q not in by_q and q not in self.grid:
                out.append(f'Q{q}: the scheme prices nothing')
        # The comprehension closes Q1-4 with ONE total, 20 marks for the four
        # asks it prices at 5 each; that is not a disagreement with the paper.
        for q in (1, 2, 3, 4):
            if self.totals.get(q) == 20:
                self.totals.pop(q)
        # The two independent counts that make the number-join safe.
        for q, total in self.totals.items():
            want = paper.question_marks.get(q)
            if want is None:
                asks = [a for a in paper.asks if a.question == q and a.marks]
                want = asks[0].marks if len(asks) == 1 else None
            if want is not None and total != want:
                out.append(f'Q{q}: the scheme totals {total} and the paper '
                           f'prices it {want}')
        for q in (10, 11, 12, 13):
            paper_letters = [a.letter for a in paper.asks
                             if a.question == q and a.letter]
            scheme_letters = [r.letter for r in by_q.get(q, []) if r.letter]
            if paper_letters and scheme_letters and \
                    scheme_letters != paper_letters:
                listed = any(k[0] == q for k in SCHEME_MISPRINTS.get(
                    ('arabic', self.year, self.level), {}))
                out.append(
                    f'Q{q}: the scheme letters {scheme_letters} and the paper '
                    f'letters {paper_letters}'
                    + (' — an SEC mis-lettering, listed in SCHEME_MISPRINTS '
                       'and corrected to the paper\'s' if listed else ''))
        return out


def report():
    from ara_paper import AraPaper
    rows = []
    for year in range(2021, 2026):
        for level in ('hl', 'ol'):
            try:
                S = AraScheme(year, level)
                P = AraPaper(year, level)
            except FileNotFoundError:
                continue
            flags = S.flags(P)
            stated = sum(1 for r in S.rows if r.question in (1, 2, 3, 4)
                         or 10 <= r.question <= 14)
            rows.append((year, level, len(S.rows), stated,
                         sorted(S.grid), flags))
    print(f'{"sitting":<10}{"rows":>6}{"stated":>8}  grid questions')
    for year, level, n, stated, grid, flags in rows:
        print(f'{year} {level.upper():<5}{n:>6}{stated:>8}  {grid}')
        for f in flags:
            print(f'      FLAG {f}')
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('year', nargs='?', type=int)
    ap.add_argument('level', nargs='?')
    ap.add_argument('--report', action='store_true')
    args = ap.parse_args()
    if args.report or not args.year:
        return report()
    S = AraScheme(args.year, args.level)
    for r in S.rows:
        print(f'Q{r.question}{f"({r.letter})" if r.letter else "":<5} '
              f'p{r.page:<3} {str(r.marks or "-"):>4}  {r.text[:90]}')
    print('\ngrid questions:', sorted(S.grid))
    print('totals:', dict(sorted(S.totals.items())))
    for q, notes in sorted(S.notes.items()):
        for n in notes:
            print(f'note Q{q}: {n[:100]}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
