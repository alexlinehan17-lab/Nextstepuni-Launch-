#!/usr/bin/env python3
"""Japanese marking schemes — the SEC's own question, answer and tariff.

    python3 scripts/markbank/authoring/ja_scheme.py 2024 hl
    python3 scripts/markbank/authoring/ja_scheme.py --all --summary

What the scheme prints
----------------------
Everything a card needs, and prints it for every ask: the question REPRINTED
(in English where the candidate answers in English or Irish, in Japanese where
the candidate answers in Japanese), the answers accepted, and a tariff in
brackets beside each one. It is one of the most completely stated schemes in
the bank — 2024 Higher prices all 220 marks down to the individual mark.

It also carries, at the back, the TAPESCRIPT: the full text of every recording
played in the Listening Comprehension Test. That is the answer document for
those asks, not their source, and it is why every listening ask is excluded.

Why the parts are paired by ORDER and not by their letters
-----------------------------------------------------------
Law 4. The scheme numbers its own sections independently of the paper, and in
this subject it visibly disagrees: the 2024 Ordinary scheme heads question 2's
four parts "A.", "B.", "Part B." and "Part C." where the paper heads them
"A.", "B.", "C. KANJI" and "D.". Joining on the letter would file the kanji
section under the true/false section.

So a question's scheme parts are paired to its paper parts in PRINTED ORDER,
under the two checks that make order safe (they are the census's own flags,
in paper_census.census_ja):

  * every question's scheme part tariffs sum to the total the PAPER prints on
    its own 問題 head, and
  * every part's scheme leaf count equals its paper leaf count.

Where either fails the sitting is flagged, never quietly re-keyed.
"""
import argparse
import collections
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))

from ja_text import doc_rows                                   # noqa: E402
from ja_paper import (NUM_MARK, LETTER_MARK, ROMAN_MARK, ROMANS,  # noqa: E402
                      plain, _read_marker)

SUBJECT = 'japanese'


def schemes_dir(subject=SUBJECT):
    return os.path.join(ROOT, 'examiner-reports', subject, 'schemes')


def scheme_path(year, level, subject=SUBJECT):
    return os.path.join(schemes_dir(subject), f'{year}-{level}.pdf')


# "Question 1", "Question 1:", "Question  3", "Q1.", "Q4" — five spellings of
# one head across ten schemes, and the Ordinary schemes of 2021 and 2022 use
# the short one throughout. Missing it filed a whole paper under one heading.
Q_HEAD = re.compile(r'^(?:Question|Ceist|Q)\s*(\d{1,2})\s*[.:]?', re.I)
# A part head is an UPPERCASE letter at the margin, and what follows it is
# nothing, a tariff, or the part's own name. The schemes print their
# multiple-choice options in the same shape — "B. a maths teacher", "A. a
# smartphone case", "C. 1 week" — and reading those as part heads split 2025
# Ordinary's question 3 into six parts and lost the asks under the real ones.
PART_HEAD = re.compile(r'^(?:Part\s+([A-D])\s*[:.]?|([A-D])\s*[:.])\s*', re.I)
PART_TAIL = re.compile(r'^(?:\(|KANJI|GRAMMAR|GRAMADACH|Half\s+marks'
                       r'|Any\s|\d{1,3}\s*marks?\b)', re.I)
MARKS = re.compile(r'\(\s*(\d{1,3})\s*marks?\s*\)', re.I)
# The banners that divide the scheme into its three examined components. The
# tapescript at the back is where the scheme stops answering and starts
# printing the recordings; nothing after it is an ask.
LISTENING = re.compile(r'^LISTENING\s+COMPREHENSION', re.I)
READING = re.compile(r'^READING\s+COMPREHENSION', re.I)
WRITTEN = re.compile(r'^WRITTEN\s+PRODUCTION', re.I)
TAPESCRIPT = re.compile(r'^TAPESCRIPT\b', re.I)
# The expression grid. It prices a composition on content and expression bands
# and prints no answer at all, so nothing between it and the next question head
# is an ask — but the scheme sets one grid between question 4 and question 5,
# and treating it as the end of the scheme lost question 5 in six sittings.
GRID = re.compile(r'^Marking\s+WRITTEN\s+EXPRESSION|^Expression\s*:', re.I)
FRONT = re.compile(r'Note to teachers and students|Marking schemes published'
                   r'|Future Marking Schemes|^Marking Scheme$', re.I)
TARIFF_ONLY = re.compile(r'^[\s.]*\(?\s*\d{1,3}\s*marks?\s*\)?[\s.]*$', re.I)


class Leaf:
    __slots__ = ('component', 'q', 'part', 'num', 'letter', 'roman',
                 'head', 'lines', 'marks', 'page', 'order')

    def __init__(self, component, q, part, num, letter, roman, head, page, order):
        self.component, self.q, self.part = component, q, part
        self.num, self.letter, self.roman = num, letter, roman
        self.head, self.page, self.order = head, page, order
        self.lines = []
        self.marks = None

    @property
    def address(self):
        a = f'{self.num}' if self.num is not None else ''
        if self.letter:
            a += f'({self.letter})'
        if self.roman:
            a += f'({self.roman})'
        return a or '-'

    @property
    def body(self):
        return ' '.join(' '.join(self.lines).split())

    def __repr__(self):
        return (f'<Leaf {self.component} Q{self.q}{self.part or ""} '
                f'{self.address} {self.marks}m {self.head[:40]!r}>')


class JaScheme:
    """One published marking scheme, read as an ordered list of leaves."""

    def __init__(self, year, level, subject=SUBJECT):
        self.year, self.level, self.subject = year, level, subject
        self.path = scheme_path(year, level, subject)
        self._leaves = None
        self.part_marks = {}        # (component, q, part index) -> marks
        self.question_marks = {}    # (component, q) -> marks

    @property
    def leaves(self):
        if self._leaves is None:
            self._leaves = self._walk()
        return self._leaves

    def parts(self, component=None):
        """[(component, q, part index)] in printed order."""
        out = []
        for lf in self.leaves:
            if component and lf.component != component:
                continue
            k = (lf.component, lf.q, lf.part)
            if k not in out:
                out.append(k)
        return out

    def by_part(self):
        out = collections.OrderedDict()
        for lf in self.leaves:
            out.setdefault((lf.component, lf.q, lf.part), []).append(lf)
        return out

    def _walk(self):
        component = None
        muted = False
        q = None
        part = None
        part_seq = 0
        cur_path = []
        leaves = []
        cur = None
        order = 0
        for pno, groups in doc_rows(self.path):
            xs = [x for x, _x1, _t in groups]
            texts = [plain(t) for _x, _x1, t in groups]
            joined = ' '.join(texts)
            if FRONT.search(joined):
                continue
            if TAPESCRIPT.match(texts[0]):
                component = None
                cur = None
                continue
            if GRID.match(texts[0]):
                muted, cur = True, None
                continue
            if LISTENING.match(texts[0]):
                component, q, part, part_seq = 'L', None, None, 0
                cur_path, cur, muted = [], None, False
                continue
            if READING.match(texts[0]):
                component, q, part, part_seq = 'R', None, None, 0
                cur_path, cur, muted = [], None, False
                continue
            if WRITTEN.match(texts[0]):
                component, q, part, part_seq = 'W', None, None, 0
                cur_path, cur, muted = [], None, False
                continue
            if component is None:
                continue
            head = Q_HEAD.match(texts[0])
            if head:
                q = int(head.group(1))
                part, part_seq = None, 0
                cur_path, cur, muted = [], None, False
                m = MARKS.search(joined) or re.search(r'\b(\d{2,3})\s*marks\b',
                                                      joined, re.I)
                if m:
                    self.question_marks[(component, q)] = int(m.group(1))
                rest = texts[0][head.end():].strip()
                if not rest or TARIFF_ONLY.match(rest) or MARKS.match(rest):
                    continue
                texts = [rest] + texts[1:]
                xs = list(xs)
            ph = PART_HEAD.match(texts[0])
            rest = texts[0][ph.end():].strip() if ph else ''
            if ph and (q is not None or component == 'L') \
                    and xs[0] <= PART_MARGIN \
                    and (not rest or PART_TAIL.match(rest)):
                letter = (ph.group(1) or ph.group(2)).upper()
                # "Part A:" followed by a bare "A:" is one part head printed
                # twice, not two parts. A NEW part is one whose letter differs
                # from the one open.
                if letter != part:
                    part_seq += 1
                    part = letter
                    cur_path, cur = [], None
                    m = MARKS.search(' '.join([rest] + texts[1:]))
                    if m:
                        self.part_marks[(component, q, part_seq)] = int(m.group(1))
                if not rest or TARIFF_ONLY.match(rest):
                    continue
                texts = [rest] + texts[1:]
                xs = list(xs)
            # A marker opens a leaf; anything else is the answer to the leaf
            # already open.
            if muted:
                continue
            got = _lead_markers(texts)
            if got:
                found, rest, tail = got
                tail_xs = xs[len(texts) - len(tail):]
                path = list(cur_path)
                for kind, tok in found:
                    if kind == 'num':
                        path = [(kind, tok)]
                        continue
                    at = next((j for j, (k, _t) in enumerate(path) if k == kind),
                              None)
                    if at is None and kind == 'letter' and path \
                            and path[-1][0] == 'roman':
                        continue
                    path = (path[:at] if at is not None else path) + [(kind, tok)]
                path = path[:2]
                cur_path = path
                num = letter = roman = None
                for kind, tok in path:
                    if kind == 'num':
                        num = tok
                    elif kind == 'letter':
                        letter = tok
                    else:
                        roman = tok
                order += 1
                cur = Leaf(component, q, part_seq or None, num, letter, roman,
                           rest, pno, order)
                leaves.append(cur)
                _absorb(cur, list(zip(tail_xs, tail)), True)
                continue
            if cur is not None:
                _absorb(cur, list(zip(xs, texts)), False)
        # A leaf whose own head row carried the tariff and nothing else is a
        # PARENT: the romans beneath it hold the answers. Parents are dropped
        # here so the ledger counts what the scheme actually priced.
        return [lf for lf in leaves if not _is_parent(lf, leaves)]


def _lead_markers(texts):
    """(address, the text after it, the groups still to be read) or None.

    The address is read across the row's LEADING gap groups: the scheme prints
    an item number and the roman under it in two groups of the same row -- "2."
    at the margin and "(i) What is the name of the non-alcoholic cocktail?"
    beside it -- and reading only the first group lost the first sub-item of
    every numbered ask in every sitting.
    """
    found, rest, i = [], '', 0
    while i < len(texts):
        got = _read_marker(texts[i])
        if got is None:
            break
        toks, r = got
        found += toks
        i += 1
        if r:
            rest = r
            break
    return (found, rest, texts[i:]) if found else None


# Where the scheme sets a leaf's own tariff: out at the right measure, clear of
# the answer. A total printed at the LEFT margin on a row of its own belongs to
# the block BELOW it. Both are TARIFF_ONLY rows and only the x separates them.
RIGHT_MEASURE = 200.0
# The margin the scheme sets its own part heads at. Everything it indents past
# this is body: an answer, an option, a table cell.
PART_MARGIN = 110.0


def _absorb(leaf, groups, head_row):
    """Fold one printed row into the leaf it belongs to.

    THE TARIFF IS THE ONE IN THE RIGHT-HAND COLUMN. The scheme prints three
    different things in brackets and they are not interchangeable:

      * the leaf's own tariff, set out on its own at the right measure --
        "When you're tired (1 mark) from work/study (1 mark)   (2 marks)";
      * the part-marks INSIDE the answer, which say how the tariff is divided
        and never how big it is;
      * a total standing alone on a row at the LEFT margin, which belongs to
        the block BELOW it -- "(14 marks)" opens question 1's second item.

    Reading the first bracket on the row gave 3(i) one mark where the scheme
    pays two; reading the last one anywhere gave the matching task fourteen.
    """
    for i, (x, t) in enumerate(groups):
        t = t.strip()
        if not t:
            continue
        if TARIFF_ONLY.match(t):
            m = MARKS.search(t) or re.search(r'(\d{1,3})', t)
            last = i == len(groups) - 1
            if last and (head_row or x >= RIGHT_MEASURE):
                leaf.marks = int(m.group(1))
            continue
        leaf.lines.append(t)
    leaf.head = ' '.join(MARKS.sub(' ', leaf.head).split())
    leaf.lines = [' '.join(x.split()) for x in leaf.lines if x.strip()]


def _is_parent(leaf, leaves):
    return any(o is not leaf and o.component == leaf.component
               and o.q == leaf.q and o.part == leaf.part
               and o.num == leaf.num
               and (leaf.letter is None and o.letter is not None
                    or leaf.roman is None and o.roman is not None)
               for o in leaves)


def sittings(subject=SUBJECT):
    out = []
    for f in sorted(os.listdir(schemes_dir(subject))):
        m = re.match(r'^(\d{4})-(hl|ol)\.pdf$', f)
        if m:
            out.append((int(m.group(1)), m.group(2)))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('year', nargs='?', type=int)
    ap.add_argument('level', nargs='?')
    ap.add_argument('--all', action='store_true')
    ap.add_argument('--summary', action='store_true')
    args = ap.parse_args()
    targets = sittings() if args.all else [(args.year, args.level)]
    for year, level in targets:
        S = JaScheme(year, level)
        parts = S.by_part()
        print(f'=== {year} {level.upper()}: {len(S.leaves)} priced leaves, '
              f'{len(parts)} parts')
        for (comp, q, part), leaves in parts.items():
            total = sum(lf.marks or 0 for lf in leaves)
            print(f'  {comp} Q{q} part {part}: {len(leaves)} leaves, {total} marks'
                  f'  (head total {S.part_marks.get((comp, q, part))},'
                  f' question {S.question_marks.get((comp, q))})')
            if not args.summary:
                for lf in leaves:
                    print(f'      {lf.address:>10} {str(lf.marks):>4}m '
                          f'{lf.head[:60]!r} -> {lf.body[:60]!r}')


if __name__ == '__main__':
    main()
