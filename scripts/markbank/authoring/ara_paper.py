#!/usr/bin/env python3
"""The Arabic question paper, read as the SEC prints it.

    python3 scripts/markbank/authoring/ara_paper.py 2025 hl
    python3 scripts/markbank/authoring/ara_paper.py --report

Arabic is the simplest paper of the modern-language family and the only one
that is a SINGLE booklet: there is no separate Listening Comprehension Test,
because the subject is examined by one written paper. Its numbering runs ON
across the whole booklet, 1 to 15, so — unlike French, German, Spanish,
Italian, Russian and Japanese, every one of which restarts inside a section —
an ask needs no section token at all. A citation is "2025 HL Q11(a)".

The four parts, which every sitting at both levels prints identically:

    الجزء الأول    Part 1, reading comprehension: a passage, then Q1-4 as
                   multiple choice at 5 marks each, then Q5 and Q6 as ~40-word
                   written answers at 30 marks each.
    الجزء الثاني   Part 2, literature, 140 marks: three prescribed sections —
                   Qur'an, poetry, modern literature — set as Q7, Q8 and Q9,
                   each with three alternatives (أ) (ب) (ج). Nine questions,
                   of which a candidate answers FOUR at 35 marks.
    الجزء الثالث   Part 3, grammar, 80 marks: Q10-13 with five sub-asks each
                   at 15 marks the question, and Q14, one parsing ask at 20.
    الجزء الرابع   Part 4, 100 marks: Q15, a composition on one of six titles.

That is 37 leaf asks a sitting — 4 + 2 + 9 + 20 + 1 + 1 — and the tariffs sum
to the 400 marks the cover prints.

THE ONE THING THE LETTERS DO NOT MEAN
-------------------------------------
(أ) (ب) (ج) (د) under Q1-4 are the OPTIONS of a multiple choice, not sub-asks;
under Q10-13 the same letters are sub-asks. Nothing in the tariff separates
them — both print one tariff for the whole question — so the paper's own rubric
does: Q1-4 sit under "اختر الإجابة الصحيحة" ("choose the correct answer"), and
they carry four options where a grammar question carries five parts. Both
signals are checked, and a sitting where they disagree is flagged rather than
guessed at.

A part letter is cited a-e, in the abjad order the SEC itself uses when it
writes them out (أ ب ج د ه). The Arabic letter is what the card shows; the
Latin letter is only the address, the way Japanese cites "Section 2B Q1(i)".
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

PAPERS = os.path.join(ROOT, 'examiner-reports', 'arabic', 'papers')

# The four printed part heads. The number is the part, not the question.
# The part head OPENS its line. The front cover names all four parts inside
# its instructions to candidates — "أجب عن أسئلة الجزء الأول" — and numbers
# those instructions ١. to ٥., which look exactly like question heads. Nothing
# on the cover is an ask, so the walk starts at the first part head that opens
# a line and everything before it is furniture.
PART_HEAD = re.compile(r'^\s*الجزء\s+(الأول|الثاني|الثالث|الرابع)')
PART_NO = {'الأول': 1, 'الثاني': 2, 'الثالث': 3, 'الرابع': 4}

# Arabic-Indic digits, which is what the SEC numbers this paper in — in BOTH
# of Unicode's two sets. The 2021 papers number their questions with the
# EXTENDED forms (U+06F0 ۰, the Persian/Urdu zero) and everything else with the
# ordinary ones (U+0660 ٠), and the two are indistinguishable on the page. A
# reader that knew only the ordinary set found no question at all in Part 3 of
# either 2021 sitting, because "١۰." mixes the two.
AR_DIGITS = {chr(0x0660 + i): str(i) for i in range(10)}
AR_DIGITS.update({chr(0x06F0 + i): str(i) for i in range(10)})
DIGIT = '٠-٩۰-۹'
# The part letters, in the abjad order the SEC writes them, and the Latin
# letter each is cited as.
LETTERS = {'أ': 'a', 'ا': 'a', 'ب': 'b', 'ج': 'c', 'د': 'd',
           'ه': 'e', 'هـ': 'e', 'ذ': 'e'}

# A question head is its number and a separator. The separator is usually a
# full stop — but Part 2's heads print "٨ (أ)" with none at all in 2022 and
# 2023 Ordinary, so a bare space counts where a part letter follows.
# A question head is its number and a separator. The separator is usually a
# full stop, and where the SEC leaves it out the number itself has to carry
# the head, which it only does in two shapes the corpus actually prints: a
# part letter follows it ("٨ (أ)", 2022 and 2023 Ordinary), or the number is
# two digits ("١٠ املأ", 2023 Higher's grammar section). Letting a bare
# single digit open a question read the "١" that starts a line of the 2021
# passage as Question 1 and swallowed the whole of Part 1 into it.
QHEAD = re.compile(
    rf'^[\s.،]*([{DIGIT}]{{1,2}})'
    rf'(?:\s*[.،]\s*|\s+(?=\()|(?<=[{DIGIT}][{DIGIT}])\s+)(.+)$')
PARTHEAD = re.compile(r'^\(?\s*(أ|ا|ب|ج|د|هـ|ه|ذ)\s*\)\s*(.*)$')
# The scheme's own way of lettering a part, which some papers copy: "أ- ".
PARTDASH = re.compile(r'^(أ|ا|ب|ج|د|هـ|ه|ذ)\s*[-–—]\s*(.*)$')
MARKS = re.compile(rf'[()]\s*([{DIGIT}]{{1,3}})\s*(?:درجة|درجات)\s*[()]')
MCQ_RUBRIC = 'اختر الإجابة الصحيحة'
# The composition question lists its titles as ١. ٢. ٣. …, which look exactly
# like question heads. Inside Part 4 they are titles.
COMPOSITION_Q = 15
# What the cover claims, at both levels, in every sitting of the window.
COVER_MARKS = 400

# Which questions each printed part sets. The paper numbers 1 to 15 straight
# through, so the part says what number may open next — and that is what keeps
# the NUMBERED LINES INSIDE a question from being read as questions. 2023
# Ordinary sets its poem as nine numbered verses, ١. to ٩., on the page between
# Q7 and Q8; a rule that accepted any ascending number read verse ٨ as
# question 8 and lost the three alternatives the SEC actually prints there.
PART_QUESTIONS = {1: range(1, 7), 2: range(7, 10), 3: range(10, 15),
                  4: range(15, 16)}

# The SEC's own mis-keying, keyed (year, level) -> {what the text layer holds:
# what the paper means}. Arabic-Indic ZERO is a dot, ٠, and so is a full stop,
# so a question head typed "٤٠" is indistinguishable from "٤." on the page —
# 2022 Higher and 2021 Ordinary both key their fourth question that way. A
# misprint is listed, never inferred from a heuristic: the alternative is a
# rule that would silently renumber a genuine question 40 if a paper ever set
# one.
# The value is what the head should read, as the paper's own numbering
# demands; the key is the exact opening the text layer holds.
MISPRINTS = {
    ('arabic', 2022, 'hl'): [('٠٤ ', '٤. ')],
    ('arabic', 2024, 'hl'): [('٠٤ ', '٤. ')],
}


def arabic_int(text):
    return int(''.join(AR_DIGITS.get(c, c) for c in text))


class Ask:
    """One leaf the paper prints."""

    __slots__ = ('question', 'letter', 'arabic_letter', 'text', 'page',
                 'marks', 'options', 'part')

    def __init__(self, question, letter, arabic_letter, text, page, part):
        self.question = question
        self.letter = letter
        self.arabic_letter = arabic_letter
        self.text = text
        self.page = page
        self.part = part
        self.marks = None
        self.options = []          # (arabic letter, text) for a multiple choice

    @property
    def key(self):
        return (self.question, self.letter)

    @property
    def ref(self):
        return f'Q{self.question}' + (f'({self.letter})' if self.letter else '')

    def __repr__(self):
        return f'<Ask {self.ref} p{self.page} {self.marks} marks>'


class AraPaper:
    """One sitting's question paper."""

    def __init__(self, year, level):
        self.year, self.level = year, level
        self.path = os.path.join(PAPERS, f'{year}-{level}-paper.pdf')
        if not os.path.exists(self.path):
            raise FileNotFoundError(self.path)
        self.lines = []
        doc = pymupdf.open(self.path)
        try:
            for pno, page in enumerate(doc, 1):
                for line in ara_text.page_lines(page):
                    self.lines.append((pno, line['text']))
        finally:
            doc.close()
        self.part_pages = {}
        self.passage_pages = []
        self.asks = []
        self.odd_heads = []
        self.part_marks = {}
        self.question_marks = {}
        self._walk()

    # ------------------------------------------------------------------ walk
    def _walk(self):
        misprints = MISPRINTS.get(('arabic', self.year, self.level), [])
        part = None
        question = None
        current = None
        mcq = False
        started = False
        for pno, text in self.lines:
            if 'There is no examination material' in text:
                continue
            for wrong, right in misprints:
                if text.startswith(wrong):
                    text = right + text[len(wrong):]
            if not started:
                if not PART_HEAD.search(text):
                    continue
                started = True
            m = PART_HEAD.search(text)
            if m:
                part = PART_NO[m.group(1)]
                self.part_pages.setdefault(part, []).append(pno)
                mk = MARKS.search(text)
                if mk:
                    self.part_marks[part] = arabic_int(mk.group(1))
                # A part head closes the ask before it. Part 4 prints its own
                # subtitle, التعبير, on the line after the head and before the
                # composition's number, and with the previous ask still open
                # that word was read as the last word of Q14.
                current = None
                continue
            if part:
                self.part_pages.setdefault(part, []).append(pno)
            if MCQ_RUBRIC in text:
                mcq = True
                continue
            if part == 4 and question == COMPOSITION_Q:
                # Everything after Q15's head is one of its printed titles.
                if current is not None and not self._is_furniture(text):
                    current.text = (current.text + ' ' + text).strip()
                    self._marks(current, text)
                continue
            qm = QHEAD.match(text)
            if qm:
                n = arabic_int(qm.group(1))
                rest = qm.group(2).strip()
                pm = PARTHEAD.match(rest)
                if self._opens_question(part, question, n, pm):
                    question = n
                    if pm:
                        current = self._open(question, pm.group(1),
                                             pm.group(2), pno, part)
                    else:
                        current = self._open(question, None, rest, pno, part)
                    self._marks(current, text)
                    continue
                if (part != 2 and n not in PART_QUESTIONS.get(part, ())
                        and 1 <= n <= 15):
                    # Part 2 is left out on purpose: the SEC sets its poems as
                    # numbered verses, ١. to ٩., down the page between one
                    # question and the next, and those are printed matter, not
                    # mis-keyed heads.
                    self.odd_heads.append((pno, text[:80]))
            pm = PARTHEAD.match(text) or PARTDASH.match(text)
            if pm and question is not None:
                letter, rest = pm.group(1), pm.group(2).strip()
                # Part 1's Q1-4 are the multiple choice at every sitting and
                # both levels; Q5 and Q6 are the written answers. The printed
                # rubric "اختر الإجابة الصحيحة" says so wherever it appears —
                # 2024 Ordinary omits it altogether — and the option count is
                # checked against it in flags().
                if part == 1 and question <= 4:
                    if current is not None:
                        mk = MARKS.search(rest)
                        current.options.append(
                            (letter, (rest[:mk.start()] if mk else rest).strip()))
                        self._marks(current, text)
                    continue
                if part in (3,) or (part == 2 and current is not None
                                    and current.letter is None):
                    mk = MARKS.search(rest)
                    current = self._open(question, letter,
                                         rest[:mk.start()] if mk else rest,
                                         pno, part)
                    self._marks(current, text)
                    continue
            if current is not None and text.strip():
                mk = MARKS.search(text)
                if mk:
                    self._marks(current, text)
                if not self._is_furniture(text):
                    # The tariff closes the ask. Anything printed after it on
                    # the same line belongs to the next thing on the page —
                    # 2021 Ordinary runs "التعبير", the head of Part 4, onto
                    # the end of Q14's tariff.
                    add = text[:mk.start()] if mk else text
                    current.text = (current.text + ' ' + add).strip()
        self._lift_question_marks()
        first = min((a.page for a in self.asks), default=None)
        if first:
            self.passage_pages = list(range(1, first + 1))

    def _lift_question_marks(self):
        """A tariff printed once under a set of parts prices the QUESTION.

        Q10 to Q13 print "(١٥ درجة)" once, at the foot of their five sub-asks,
        and it is the question's tariff, not the fifth part's — the scheme
        splits it three marks a part. Leaving it on the last part would have
        priced Q10(e) at fifteen and the other four at nothing. Q15 is the same
        shape one level up: its hundred marks are printed on the PART head,
        because Part 4 sets exactly one question.
        """
        by_q = collections.defaultdict(list)
        for a in self.asks:
            by_q[a.question].append(a)
        for q, asks in by_q.items():
            lettered = [a for a in asks if a.letter]
            if len(lettered) > 1:
                priced = [a for a in lettered if a.marks is not None]
                if len(priced) == 1:
                    self.question_marks[q] = priced[0].marks
                    priced[0].marks = None
        for part, marks in self.part_marks.items():
            qs = {a.question for a in self.asks if a.part == part}
            if len(qs) == 1:
                q = qs.pop()
                if all(a.marks is None for a in by_q[q]):
                    self.question_marks.setdefault(q, marks)

    @staticmethod
    def _opens_question(part, question, n, partmatch):
        """Is this numbered line a QUESTION head, or a line inside one?

        The paper numbers straight through, so the only number that may open a
        question is the next one its part sets — or, in Part 2, the SAME one
        again when a part letter follows it, because Q7, Q8 and Q9 each print
        three alternatives under one number.
        """
        allowed = PART_QUESTIONS.get(part)
        if allowed is None or n not in allowed:
            return False
        if part == 2 and partmatch is None:
            # Q7, Q8 and Q9 ALWAYS print a part letter on the head — "٧. (أ)".
            # Part 2 is also where the SEC sets its poem, whose verses are
            # numbered ١. to ٩. down the page between one question and the
            # next; without this, verse ٨ opened question 8 and the three
            # alternatives the SEC prints under it were lost.
            return False
        if question is None:
            return n == allowed[0]
        if n == question:
            return part == 2 and partmatch is not None
        return n == question + 1

    @staticmethod
    def _is_furniture(text):
        return bool(re.match(r'^\s*(Leaving Certificate|Arabic\s*[-–]|Source:)',
                             text)) or re.fullmatch(r'\s*\d{1,2}\s*', text)

    def _open(self, question, arabic_letter, text, page, part):
        letter = LETTERS.get(arabic_letter) if arabic_letter else None
        ask = Ask(question, letter, arabic_letter, text.strip(), page, part)
        self.asks.append(ask)
        return ask

    @staticmethod
    def _marks(ask, text):
        m = MARKS.search(text)
        if m and ask.marks is None:
            ask.marks = arabic_int(m.group(1))

    # ----------------------------------------------------------------- views
    @property
    def leaves(self):
        """A stem that has lettered parts is a parent, not a leaf.

        Q10's own line — "املأ كل فراغ بما هو مطلوب منك بين الأقواس" — is the
        instruction its five sub-asks are answered under. Counting it as a
        sixth leaf would price a question the paper does not set.
        """
        lettered = {a.question for a in self.asks if a.letter}
        return [a for a in self.asks
                if a.letter or a.question not in lettered]

    def by_key(self):
        return {a.key: a for a in self.asks}

    def flags(self):
        """Everything about this sitting that does not look like the others."""
        out = []
        asks = self.leaves
        qs = sorted({a.question for a in self.asks})
        if qs != list(range(1, 16)):
            out.append(f'questions printed: {qs} (expected 1-15)')
        counts = collections.Counter(a.question for a in asks)
        for q in range(1, 5):
            if counts.get(q) != 1:
                out.append(f'Q{q} is a multiple choice and should be one leaf, '
                           f'not {counts.get(q)}')
            opts = [a for a in asks if a.question == q]
            if opts and len(opts[0].options) != 4:
                out.append(f'Q{q} prints {len(opts[0].options)} options, not 4')
        for q in (5, 6, 14, 15):
            if counts.get(q) != 1:
                out.append(f'Q{q} should be one leaf, not {counts.get(q)}')
        for q in (7, 8, 9):
            if counts.get(q) != 3:
                out.append(f'Q{q} should print three alternatives, not '
                           f'{counts.get(q)}')
        for q in (10, 11, 12, 13):
            if counts.get(q) != 5:
                out.append(f'Q{q} should print five parts, not {counts.get(q)}')
        for pno, text in self.odd_heads:
            out.append(f'numbered line inside a question, p{pno}: {text!r}')
        # Part 2 is a CHOICE — nine alternatives of which a candidate answers
        # four — so adding every printed tariff counts questions nobody sits.
        # The checksum is what the paper's own cover states.
        chosen = sum(sorted((a.marks or 0 for a in asks
                             if a.part == 2), reverse=True)[:4])
        total = (sum(a.marks or 0 for a in asks if a.part != 2)
                 + sum(self.question_marks.values()) + chosen)
        if total != COVER_MARKS:
            out.append(f'tariffs sum to {total}, and the cover prints '
                       f'{COVER_MARKS}')
        return out, total


def report():
    rows = []
    for year in range(2021, 2026):
        for level in ('hl', 'ol'):
            try:
                P = AraPaper(year, level)
            except FileNotFoundError:
                continue
            flags, total = P.flags()
            rows.append((year, level, len(P.leaves), total, flags))
    print(f'{"sitting":<10}{"leaves":>8}{"marks":>8}  flags')
    for year, level, n, total, flags in rows:
        print(f'{year} {level.upper():<5}{n:>8}{total:>8}  '
              f'{"; ".join(flags) if flags else "-"}')
    print(f'\n{sum(r[2] for r in rows)} leaf asks over {len(rows)} sittings')
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('year', nargs='?', type=int)
    ap.add_argument('level', nargs='?')
    ap.add_argument('--report', action='store_true')
    args = ap.parse_args()
    if args.report or not args.year:
        return report()
    P = AraPaper(args.year, args.level)
    for a in P.asks:
        print(f'{a.ref:<10} p{a.page:<3} {str(a.marks or "-"):>4}  '
              f'{a.text[:100]}')
        for letter, text in a.options:
            print(f'              ({letter}) {text[:80]}')
    flags, total = P.flags()
    print(f'\n{len(P.asks)} leaves, {total} marks')
    for f in flags:
        print('  FLAG', f)
    return 0


if __name__ == '__main__':
    sys.exit(main())
