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


# "Question 1", "Question 1:", "Question  3", "Q1.", "Q4", "Q.2", "Q. 3" — the
# SEC spells its question head six ways across ten schemes, and the period goes
# on either side of the number. The 2021 Ordinary scheme heads two of its three
# questions "Q.2" and "Q. 3"; missing them filed a whole paper under question 1
# and left 193 asks with nothing to pair against.
Q_HEAD = re.compile(r'^(?:Question|Ceist|Q)\s*[.]?\s*(\d{1,2})\s*[.:]?', re.I)
# A part head is an UPPERCASE letter at the margin, and what follows it is
# nothing, a tariff, or the part's own name. The schemes print their
# multiple-choice options in the same shape — "B. a maths teacher", "A. a
# smartphone case", "C. 1 week" — and reading those as part heads split 2025
# Ordinary's question 3 into six parts and lost the asks under the real ones.
PART_HEAD = re.compile(r'^(?:Part\s+([A-D])\s*[:.]?|([A-D])\s*[:.])\s*', re.I)
TASK_NAME = re.compile(r'\b(KANJI|GRAMMAR|GRAMADACH)\b', re.I)


def _task_name(rest):
    m = TASK_NAME.search(rest or '')
    return m.group(1).upper().replace('GRAMADACH', 'GRAMMAR') if m else None


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
WORD_COUNTS = {'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6,
               'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10, 'eleven': 11,
               'twelve': 12, 'thirteen': 13}
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
        self.part_heads = []        # every part head, in printed order
        self.part_marks = {}        # (component, q, part index) -> marks
        self.part_text = {}         # (component, q, part index) -> its head
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

    def _rate(self, leaf):
        """What one item of this part is worth, where the head says so."""
        key = (leaf.component, leaf.q, leaf.part)
        head = self.part_text.get(key, '')
        m = re.search(r'(\d{1,2})\s*marks?\s*each', head, re.I)
        if m:
            return int(m.group(1))
        m = re.search(r'any\s+(\w+)\s+(?:correct\s+)?answers?', head, re.I)
        total = self.part_marks.get(key)
        if not m or total is None:
            return None
        n = WORD_COUNTS.get(m.group(1).lower())
        if n is None and m.group(1).isdigit():
            n = int(m.group(1))
        if n and total % n == 0:
            return total // n
        return None

    def by_part(self):
        """{(component, question, part index): [leaf]} in printed order.

        Every part the scheme HEADS is a key, including one it heads and then
        answers with nothing.
        """
        out = collections.OrderedDict()
        for lf in self.leaves:
            out.setdefault((lf.component, lf.q, lf.part), []).append(lf)
        for head in self.part_heads:
            out.setdefault(head, [])
        return collections.OrderedDict(
            sorted(out.items(), key=lambda kv: (
                kv[1][0].order if kv[1] else self._head_order(kv[0]))))

    def _head_order(self, head):
        """Where an empty part head sits among the leaves that surround it."""
        after = [lf.order for lf in self.leaves
                 if (lf.component, lf.q) == head[:2]
                 and (lf.part or 0) < (head[2] or 0)]
        return max(after) + 0.5 if after else 0.0

    def _walk(self):
        component = None
        muted = False
        q = None
        part = None
        part_name = None
        part_form = None
        part_leaves = 0
        part_seq = 0
        cur_path = []
        leaves = []
        cur = None
        order = 0
        for pno, groups in doc_rows(self.path):
            xs = [x for x, _x1, _t in groups]
            # The scheme's own text, AS PRINTED. Only the head tests strip the
            # furigana, and only because a head carries it — 問題（もんだい）.
            # An ANSWER carries it too, and there it is content: the scheme
            # answers 2021 Higher's question 3 with 畳（たたみ）の部屋, and a
            # card printing 畳の部屋 has dropped a reading the SEC supplied.
            texts = [t for _x, _x1, t in groups]
            joined = plain(' '.join(texts))
            head0 = plain(texts[0])
            if FRONT.search(joined):
                continue
            if TAPESCRIPT.match(head0):
                component = None
                cur = None
                continue
            if GRID.match(head0):
                muted, cur = True, None
                continue
            if LISTENING.match(head0):
                component, q, part, part_seq = 'L', None, None, 0
                part_name, part_form, part_leaves = None, None, 0
                cur_path, cur, muted = [], None, False
                continue
            if READING.match(head0):
                component, q, part, part_seq = 'R', None, None, 0
                part_name, part_form, part_leaves = None, None, 0
                cur_path, cur, muted = [], None, False
                continue
            if WRITTEN.match(head0):
                component, q, part, part_seq = 'W', None, None, 0
                part_name, part_form, part_leaves = None, None, 0
                cur_path, cur, muted = [], None, False
                continue
            if component is None:
                continue
            # The page number, alone on a row. Absorbed into the answer above
            # it, it put a stray "6" on the end of an ask worth two marks.
            if all(re.fullmatch(r'\d{1,3}', plain(t).strip()) for t in texts):
                continue
            head = Q_HEAD.match(head0)
            if head:
                q = int(head.group(1))
                part, part_name, part_seq = None, None, 0
                part_form, part_leaves = None, 0
                cur_path, cur, muted = [], None, False
                m = MARKS.search(joined) or re.search(r'\b(\d{2,3})\s*marks\b',
                                                      joined, re.I)
                if m:
                    self.question_marks[(component, q)] = int(m.group(1))
                rest = _after(texts[0], head.end())
                if not rest or TARIFF_ONLY.match(rest) or MARKS.match(rest):
                    continue
                texts = [rest] + texts[1:]
                head0 = plain(rest)
            ph = PART_HEAD.match(head0)
            rest = _after(texts[0], ph.end()) if ph else ''
            if ph and (q is not None or component == 'L') \
                    and xs[0] <= PART_MARGIN \
                    and (not rest or PART_TAIL.match(rest)):
                letter = (ph.group(1) or ph.group(2)).upper()
                # "Part A:" followed by a bare "A:" is one part head printed
                # twice, not two parts. A NEW part is one whose letter differs
                # from the one open — OR one that NAMES a different task under
                # the same letter, which the SEC does: the 2021 Higher scheme
                # heads question 3's last two parts "C: KANJI" and
                # "C: GRAMMAR", and taking the letter alone welded them into
                # one part and lost the pairing for the whole paper.
                name = _task_name(rest)
                form = 'part' if ph.group(1) else 'bare'
                # A head written "Part B." after a head written "B." is the SEC
                # RESTARTING its lettering, not repeating it: the 2024 Ordinary
                # scheme heads question 2's four parts "A.", "B.", "Part B."
                # and "Part C.". Taking the letter alone welded the kanji
                # section onto the true/false section above it. The change of
                # FORM only counts once the part above has answers under it —
                # "Part A:" followed immediately by a bare "A:" is one head
                # printed twice, which is how Higher's question 1 opens.
                restarted = (form != part_form and part_leaves)
                if letter != part or (name and name != part_name) or restarted:
                    part_seq += 1
                    part, part_name, part_form = letter, name, form
                    part_leaves = 0
                    # Recorded even where the scheme lists nothing under it.
                    # The Ordinary culture section is headed "D: (4 marks)" and
                    # answered "2 marks each for any 2 points" — a part with a
                    # tariff and no answers — and leaving it out of the part
                    # list shifted every part after it onto the wrong ask.
                    self.part_heads.append((component, q, part_seq))
                    cur_path, cur = [], None
                    head_text = ' '.join([rest] + texts[1:])
                    self.part_text[(component, q, part_seq)] = head_text
                    m = MARKS.search(head_text)
                    if m:
                        self.part_marks[(component, q, part_seq)] = int(m.group(1))
                if not rest or TARIFF_ONLY.match(rest):
                    continue
                texts = [rest] + texts[1:]
                head0 = plain(rest)
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
                part_leaves += 1
                _absorb(cur, list(zip(tail_xs, tail)), True)
                continue
            if cur is not None:
                _absorb(cur, list(zip(xs, texts)), False)
        # The scheme sets a marker on a row of its own as often as it sets one
        # beside the question — "(i)" at the margin and "Tokyo Kart に乗る時、
        # 何をすると楽しくなりますか。" on the next row — so a leaf that opened
        # with no head takes the first line under it as its question, where
        # that line reads as one. Left in the answer it turned the question
        # into an accepted answer on the card.
        for lf in leaves:
            if not lf.head and lf.lines and _is_question(lf.lines[0]):
                lf.head = lf.lines.pop(0)
        # An instruction to the EXAMINER is not an ask. The scheme prints its
        # language penalty inside the numbering — 2024 Higher opens "3. Half
        # marks where there is strong evidence of extraneous material" right
        # where question 2's third item belongs — and read as a leaf it put one
        # more ask in the scheme than the paper prints, which broke the pairing
        # for that whole part in five sittings.
        leaves = [lf for lf in leaves
                  if lf.lines or not EXAMINER.search(lf.head)]
        leaves = _drop_heads(leaves)
        # ONE PRINTED ADDRESS IS ONE ASK. The SEC repeats one: the 2025 Higher
        # scheme numbers question 2's third ask "(c)" and then numbers the ask
        # after it "(c)" again, three marks each. The paper prints that address
        # once, so the two are folded into the one ask the paper prints, at the
        # tariff the scheme prints for it — 3 + 3, which is stated, not guessed.
        # A part that prints ONE RATE for every item under it prices the items
        # it does not price individually: "D: GRAMMAR (10 marks) (any 10
        # correct answers)" states one mark each, and the scheme then sets its
        # particles out in columns with the tariff on only some of them. That
        # is the SEC's own arithmetic on its own printed numbers, not a guess —
        # and where the head states no rate, nothing is filled in.
        for lf in leaves:
            if lf.marks is None:
                rate = self._rate(lf)
                if rate is not None:
                    lf.marks = rate
        out = []
        for lf in leaves:
            prev = out[-1] if out else None
            if prev is not None and (prev.component, prev.q, prev.part,
                                     prev.num, prev.letter, prev.roman) == \
                    (lf.component, lf.q, lf.part, lf.num, lf.letter, lf.roman):
                prev.head = prev.head or lf.head
                prev.lines += ([lf.head] if lf.head and lf.head != prev.head
                               else []) + lf.lines
                if prev.marks is not None and lf.marks is not None:
                    prev.marks += lf.marks
                else:
                    prev.marks = prev.marks or lf.marks
                continue
            out.append(lf)
        return out


# A line that reads as a question rather than an answer: it ends in a question
# mark, or in the Japanese one, or in か。 — which is how every Japanese-set ask
# in this paper ends.
QUESTION_LINE = re.compile(r'[?？]\s*$|か\s*[。｡]\s*$')


def _is_question(line):
    return bool(QUESTION_LINE.search(line or ''))


def _after(raw, consumed):
    """`raw` with its first `consumed` NON-RUBY characters removed."""
    from ja_paper import _after_marker
    return _after_marker(raw, consumed)


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
        got = _read_marker(plain(texts[i]), numbered_alone=True)
        if got is None:
            break
        toks, r = got
        found += toks
        i += 1
        if r:
            rest = _after(texts[i - 1],
                          len(plain(texts[i - 1])) - len(r))
            break
    return (found, rest, texts[i:]) if found else None


# Where the scheme sets a leaf's own tariff: out at the right measure, clear of
# the answer. A total printed at the LEFT margin on a row of its own belongs to
# the block BELOW it. Both are TARIFF_ONLY rows and only the x separates them.
RIGHT_MEASURE = 200.0
# The margin the scheme sets its own part heads at. Everything it indents past
# this is body: an answer, an option, a table cell.
PART_MARGIN = 110.0


# A tariff set INSIDE a line rather than beside it. The scheme prints both
# forms — "(1 mark)" and a bare "1 mark" run out with spaces — and where the
# gap between the tariff and the answer beside it fell under the column
# threshold the two arrived as one group: "(d) よにん   1 mark    4 people".
# Left in, the card's answer read "1 mark 4 people".
#
# It has to be set out with WHITE SPACE on both sides, because the same words
# appear inside the scheme's own choice notation — "(any 2, 2 + 1 mark)" — and
# stripping them there destroyed the notation that says what one answer is
# worth, which turned a menu of four accepted answers into one long string.
BARE_MARKS = re.compile(r'(?:^|(?<=\s\s))\(?\d{1,2}\s*marks?\)?'
                        r'(?=\s\s|\s*$)', re.I)


TRAILING_TARIFF = re.compile(r'\s{2,}\(?\s*(\d{1,3})\s*marks?\s*\)?[.\s]*$',
                             re.I)


def _strip_marks(text):
    return ' '.join(BARE_MARKS.sub(' ', MARKS.sub(' ', text)).split())


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
        last = i == len(groups) - 1
        if TARIFF_ONLY.match(t):
            m = MARKS.search(t) or re.search(r'(\d{1,3})', t)
            if last and (head_row or x >= RIGHT_MEASURE):
                leaf.marks = int(m.group(1))
            continue
        # A tariff set out at the right measure but NOT split into a group of
        # its own: where the answer runs long the gap in front of the tariff
        # falls under the column threshold and the two arrive together,
        # "3 June 2011                    (2 marks)". Thirty-one asks with a
        # printed answer and a printed tariff were refused for want of this.
        tail = TRAILING_TARIFF.search(t)
        if last and tail:
            leaf.marks = int(tail.group(1))
            t = t[:tail.start()]
        leaf.lines.append(_strip_marks(t))
    leaf.head = ' '.join(MARKS.sub(' ', leaf.head).split())
    leaf.lines = [' '.join(x.split()) for x in leaf.lines if x.strip()]


# What a numbered head says when it is a head: the INSTRUCTION for the items
# beneath it. The 2021 Ordinary scheme heads its matching task "1. Write the
# number of the link as in the example" and prices it ten marks over five
# romans, and a length test alone read that as an ask of its own.
INSTRUCTION = re.compile(
    r'^\s*(?:Write|Name|Complete|Translate|Circle|Insert|Answer|List|Give'
    r'|Match|Choose|Fill|Tick|Indicate|Provide|Mention)\b', re.I)
EXAMINER = re.compile(
    r'half\s*marks|1\s*/\s*2\s*marks|extraneous material'
    r'|if\s+(?:not\s+)?answered in|correct answers?\b|deduct', re.I)


def _drop_heads(leaves):
    """Drop the numbered HEADS, keeping the asks under them.

    A head carries a tariff, or the count and rate its items are marked at,
    and the answers live in the romans beneath it. But the SEC REUSES a number:
    the 2024 Higher scheme sets question 2's Japanese-answer items as
    "3. (i) … (ii) … (iii) …" and then sets the TRANSLATION as "3." again,
    with the passage under it. So where a number is printed bare more than
    once above the same romans, only the FIRST is the head — the later ones are
    asks the SEC numbered the same way, and dropping them lost the translation
    in three sittings.
    """
    bare = collections.OrderedDict()
    for lf in leaves:
        if lf.letter is None and lf.roman is None and lf.num is not None:
            bare.setdefault((lf.component, lf.q, lf.part, lf.num), []).append(lf)
    heads = set()
    for key, group in bare.items():
        if not any(o.num == key[3] and (o.letter or o.roman)
                   and (o.component, o.q, o.part) == key[:3] for o in leaves):
            continue
        for lf in group[:-1] if len(group) > 1 else group:
            heads.add(id(lf))
    return [lf for lf in leaves if id(lf) not in heads]


def _is_parent(leaf, leaves):
    """A numbered head whose own row carried a tariff and nothing else.

    A head says one of three things and none of them is an answer: a tariff,
    the count and rate the items beneath it are marked at ("Any FIVE correct
    answers  5 marks"), or their INSTRUCTION. What it never does is run to a
    paragraph of content — so a repeated number carrying one is not a head. The
    SEC reuses a number: the 2024 Higher scheme sets the Japanese-answer items
    as "3. (i) … (ii) … (iii) …" and then sets the TRANSLATION as "3." again,
    with the passage under it, and dropping every repeat lost that translation
    in three sittings — an ask the paper itself numbers 4.
    """
    if len(leaf.head) > 40 and not INSTRUCTION.match(leaf.head):
        return False
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
