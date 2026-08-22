#!/usr/bin/env python3
"""Check every Economics card's citation against the QUESTION PAPER.

    python3 scripts/markbank/authoring/econ_refcheck.py [authored/economics.json]

A card's claims are checked against the marking scheme by provcheck.mjs. Its
CITATION — "2023 HL Q15(b)(ii)" — is not, because the scheme is a table
flattened into one long line and the question number a part sits under is
exactly what that flattening loses. Where the scheme prints "6." at the foot of
one page and "⟨4⟩ (a)" at the head of the next, question 6's parts are counted
as more parts of question 5 and every card built from them cites the wrong
question. Nothing in the pipeline noticed: the claims still traced, because the
claims came from the right block of text.

So the citation is checked against the other document. The paper heads each
question "Question N" on its own line and every page after it belongs to that
question until the next heading, which is a far more reliable signal than
anything in the scheme. A card whose question text lands under a different
heading is reported with the number the paper actually gives it.

Page-aware on purpose. The paper is an answer booklet, so its flat text
interleaves question wording with answer space ("Explanation:", "1. 2.") and
running heads; scanning the flat text for the nearest preceding "Question N"
attributes a part to whichever heading happens to have been printed most
recently, which is not the same thing as which question it belongs to.
"""
import bisect
import collections
import json
import os
import re
import sys

import pymupdf

DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, DIR)
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(DIR)))
PAPERS = os.path.join(ROOT, 'examiner-reports', 'economics', 'papers')

from econ_refs import HAND_CHECKED  # noqa: E402

# The heading, on a line of its own — "Question 14". Matched loosely enough to
# survive the two papers that print it as "Question 14 (75 marks)".
# "Question 12" reaches the text layer as "Question 1 2" in the 2025 Higher
# paper, whose digits are kerned as separate runs. Both readings are offered to
# the sequence guard, which takes whichever one is the number it is looking for.
HEADING = re.compile(r'Question\s+(\d)(\s?\d)?\b')
# A part numeral. Romans before letters so "(i)" is not read as the letter i.
MARKER = re.compile(r'\((i{1,3}|iv|vi{0,3}|v|[a-e])\)')
ROMAN = ('i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii')
# Parts are lettered (a)-(e) and numbered (i)-(viii). No paper here letters a
# part (i), so a bare "(i)" is always the roman.
LETTERS = ('a', 'b', 'c', 'd', 'e')
# How many consecutive words of a card's question the paper must contain for
# the match to be believed. Six is long enough that no two parts of one paper
# share a run by accident.
RUN = 6
# A word this common in the paper is not worth trying as an anchor; the run is
# found from one of the card's other words instead.
ANCHOR_MAX = 200
REF = re.compile(r'^(\d{4})\s+(HL|OL)(\s+Section A)?\s+Q(\d{1,2})((?:\([a-z]+\))*)')


class Paper:
    """One question paper, indexed by where each question's heading falls.

    Indexed by offset, not by page. A page is not a question: the last part of
    question 3 is printed at the head of the page that starts question 4, and
    the first part of question 3 shares a page with the whole of question 2 —
    so attributing a part to the first heading printed on its page puts it
    under a question it is not from, which is the very mistake this file exists
    to catch.
    """

    def __init__(self, year, level):
        with pymupdf.open(os.path.join(PAPERS, f'{year}-{level}-paper.pdf')) as doc:
            # Every paper sets its headings with non-breaking spaces.
            # Non-breaking spaces in every paper's headings; and the 2025 pair
            # map the "ti" ligature to U+019F, so "Question" reaches the text
            # layer as "QuesƟon" and no word containing "ti" would ever match.
            raw = [p.get_text().replace('\xa0', ' ').replace('Ɵ', 'ti') for p in doc]
        self.text = ' '.join(re.sub(r'\s+', ' ', page) for page in raw)
        # Only headings that continue the sequence: a paper refers to its own
        # questions in the rubric ("Answer 3 out of 6"), and the numbers in a
        # data table are not headings either.
        self.heads, want = [], 1
        for m in HEADING.finditer(self.text):
            joined = m.group(1) + (m.group(2) or '').strip()
            if want in (int(m.group(1)), int(joined)):
                self.heads.append((m.start(), want))
                want += 1
        self.at = [o for o, _ in self.heads]
        self.spans = {n: (o, self.heads[i + 1][0] if i + 1 < len(self.heads) else len(self.text))
                      for i, (o, n) in enumerate(self.heads)}
        # Folded to letters and digits so an apostrophe, an en dash or a capital
        # cannot hide a match, and folded ONE CHARACTER AT A TIME so every
        # offset still points at the same place in self.text.
        self.norm = re.sub(r'[^0-9a-z]', ' ', self.text.lower())
        self.words = [(m.group(0), m.start()) for m in re.finditer(r'[0-9a-z]+', self.norm)]
        self.index = collections.defaultdict(list)
        for i, (w, _) in enumerate(self.words):
            self.index[w].append(i)

    def question_at(self, at):
        i = bisect.bisect_right(self.at, at) - 1
        return self.heads[i][1] if i >= 0 else None

    def page_at(self, at):
        """Kept for --show: which page of the PDF an offset falls on."""
        return bisect.bisect_right(self.at, at) - 1

    def markers(self, q):
        """Where each part of question q begins, as (offset, letter, roman).

        Only markers that continue the sequence count. An answer booklet prints
        "(i)" in places that are not the start of part (i) — "Based on the
        figure you calculated in (i) above", a lettered answer box — and taking
        the nearest preceding marker put a card under part (i) when the paper
        had already moved on to (ii). A part numeral that is not the next one
        expected is not a part numeral.
        """
        lo, hi = self.spans[q]
        out, want_l, want_r = [], 0, 0
        for m in MARKER.finditer(self.text[lo:hi]):
            v = m.group(1)
            if v in LETTERS and want_l < len(LETTERS) and v == LETTERS[want_l]:
                out.append((lo + m.start(), v, None))
                want_l, want_r = want_l + 1, 0
            elif v in ROMAN and want_r < len(ROMAN) and v == ROMAN[want_r]:
                out.append((lo + m.start(), None, v))
                want_r += 1
        return out

    def path_at(self, q, at):
        """The part path the paper prints for the text at `at`, e.g. "(c)(ii)"."""
        if q not in self.spans:
            return ''
        marks = [m for m in self.markers(q) if m[0] <= at]
        letter = next((v for _, v, r in reversed(marks) if v), None)
        start = next((o for o, v, r in reversed(marks) if v), -1)
        roman = next((r for o, v, r in reversed(marks) if r and o > start), None)
        return ''.join(f'({x})' for x in (letter, roman) if x)

    def locate(self, question):
        """Where in this paper the card's question is, or -1.

        A card's question text is written for a student and is rarely the
        paper's sentence word for word: a part reading "(ii) Outline two ways
        citizens in Ireland can behave more sustainably" is carded with its
        stem folded in and its lead-in rewritten. So the match is the longest
        run of the card's own words that the paper actually contains, grown
        outwards from the rarest word they share — which places a card the
        paper words differently, and refuses one it does not contain at all.
        """
        q = tokens(question)
        if len(q) < RUN:
            return -1
        # Every word of the card that is not ubiquitous in the paper is tried as
        # an anchor, not just the rarest few. A card whose distinctive words are
        # all in its stem — "More Irish consumers shopped online during 2020" —
        # has its matching run somewhere else entirely, and anchoring on the
        # five rarest words looked for it in the one place it was not.
        rare = {t for t in q if t in self.index and len(self.index[t]) <= ANCHOR_MAX}
        if not rare:
            rare = set(sorted((t for t in q if t in self.index),
                              key=lambda t: len(self.index[t]))[:5])
        best, where = 0, -1
        for j, t in enumerate(q):
            if t not in rare:
                continue
            for p in self.index[t]:
                a = b = 0
                while j - a > 0 and p - a > 0 and self.words[p - a - 1][0] == q[j - a - 1]:
                    a += 1
                while (j + b + 1 < len(q) and p + b + 1 < len(self.words)
                       and self.words[p + b + 1][0] == q[j + b + 1]):
                    b += 1
                if a + b + 1 > best:
                    best, where = a + b + 1, self.words[p - a][1]
        return where if best >= RUN else -1


def tokens(text):
    """A question as the words the paper would have to contain to be it."""
    return re.sub(r'[^0-9a-z]', ' ', text.lower()).split()


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    path = args[0] if args else os.path.join(
        ROOT, 'scripts/markbank/authored/economics.json')
    cards = json.load(open(path))
    show = '--show' in sys.argv
    papers, bad, lost = {}, [], []
    for c in cards:
        m = REF.match(c.get('questionRef', ''))
        if not m:
            lost.append(f"{c['id']}: unreadable reference {c.get('questionRef')!r}")
            continue
        year, lvl, want, path_ = m.group(1), m.group(2).lower(), int(m.group(4)), m.group(5)
        key = (year, lvl)
        if key not in papers:
            papers[key] = Paper(year, lvl)
        paper = papers[key]
        at = paper.locate(c['questionText'])
        if at < 0:
            lost.append(f"{c['id']}: not found in the {year} {lvl.upper()} paper"
                        + (f"\n            {c['questionText'][:150]}" if show else ''))
            continue
        got = paper.question_at(at)
        if got != want:
            bad.append(f"{c['id']}: cites Q{want}{path_}, the paper prints it under "
                       f"Question {got}{paper.path_at(got, at)}")
            if show:
                print(f"\n--- {c['id']}  in the {year} {lvl.upper()} paper, "
                      f"under Question {got}")
                print('   ', paper.text[max(0, at - 260):at + 160].strip())
    fresh = [line for line in lost if line.split(':')[0] not in HAND_CHECKED]
    for line in fresh:
        print('UNPLACED ', line)
    for line in bad:
        print('WRONG    ', line)
    print(f'\n{len(cards)} card(s): {len(bad)} wrong, '
          f'{len(cards) - len(bad) - len(lost)} confirmed against the paper, '
          f'{len(lost) - len(fresh)} read by hand (econ_refs.HAND_CHECKED), '
          f'{len(fresh)} unplaced')
    return 1 if bad or fresh else 0


if __name__ == '__main__':
    raise SystemExit(main())
