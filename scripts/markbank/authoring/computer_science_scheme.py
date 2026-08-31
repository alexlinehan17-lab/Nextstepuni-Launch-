#!/usr/bin/env python3
"""The Computer Science marking scheme, read by its own column grid.

    python3 scripts/markbank/authoring/cs_scheme.py 2024 hl        # summary
    python3 scripts/markbank/authoring/cs_scheme.py 2024 hl 13 a i # one part

Why not the generic readers: scheme.Scheme flattens the page, so Question 2
comes back as "Answer: 27 30 33 Each correct value in order (x 4) 1 mark Space
between each value 2 marks" -- the answer, the criteria and the mark cells run
together in one string. Worse, it reads Question 1's logic-gate OUTPUTS, the
column of 0s and 1s the candidate has to fill in, as the question's mark
values. SchemePdf raises UnboundLocalError on the first scheme it is given.

The page is a three-column grid and reading it as one is straightforward:

    Question 13                                    38 (11, 15, 12) marks
    (a)                                            11 (3,3,3, 2) marks
        (i)                                                    3 marks
    Any response that captures the essence of any of the following:
      * Artificial intelligence can be defined as the science and ...
      * The design and study of systems that appear to mimic ...
    Very good explanation - clear understanding demonstrated       3 marks
    Fair explanation - limited understanding                       2 marks

The marker sits at the left, the TARIFF in the right margin, and between them
the answer. Two things follow from that layout and both matter:

  * The tariff is printed for every part AND split on the head above it, so
    nothing here is ever inferred. "38 (11, 15, 12)" is the question's total
    over its three letters; "11 (3,3,3, 2)" is (a)'s total over its parts.
  * The credit BANDS at the foot of a part -- "Very good explanation ...
    3 marks" -- are the rubric, not the answer. They say how well the thing
    was done, never what it was. They are kept apart from the marking points
    and returned by bands(), because a card built from "Fair explanation"
    tells a student nothing.

The bullet is Symbol-font U+F0B7, not U+2022; it is folded here so a marking
point does not ship with a private-use glyph in it.
"""
import collections
import os
import re
import sys

import pymupdf

DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, DIR)
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(DIR)))
SCHEMES = os.path.join(ROOT, 'examiner-reports', 'computer-science', 'schemes')

QUESTION = re.compile(r'^Question\s+(\d{1,2})\b', re.I)
LETTER = re.compile(r'^\(([a-h])\)\s*$')
ROMAN = re.compile(r'^\((i{1,3}|iv|v|vi{0,3}|ix|x)\)\s*$')
# "6 marks", "38 (11, 15, 12) marks", "11 (3,3,3, 2) marks", "2 mark".
TARIFF = re.compile(r'^(\d{1,3})\s*(?:\(([\d,\s]+)\))?\s*marks?\s*$', re.I)
# The rubric at the foot of a part. It grades the response; it never states it.
BAND = re.compile(r'^\s*(very good|good|fair|excellent|weak|poor|full correct|'
                  r'response with some merit|correct|incorrect|no |partially|'
                  r'almost|some merit|any \d+ (?:from|of)|award)',
                  re.I)
SECTION = re.compile(r'^Section\s+([A-C])\b')
PAGE_NO = re.compile(r'^\d{1,3}$')
# "Section A / Short Answer Questions / Attempt any nine questions / 54 marks /
# All questions carry equal marks" -- the paper's own pricing of a section whose
# questions the scheme prices individually nowhere.
SECTION_RUBRIC = re.compile(
    r'Section\s+([AB])\s+(?:Short Answer Questions|Long Questions)\s+'
    r'Attempt any (\w+) questions?\s+(\d{1,3})\s*marks\s+'
    r'(All questions carry equal marks)?', re.I)
COUNT_WORD = {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5,
              'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10}
ROMAN_ORDER = {r: i + 1 for i, r in enumerate(
    ['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x'])}
BULLET = ''


def _lines(page):
    """(x, y, text) for every printed line, page number dropped."""
    out = []
    for bl in page.get_text('dict')['blocks']:
        for ln in bl.get('lines', []):
            text = ''.join(s['text'] for s in ln['spans'])
            text = ' '.join(text.replace(BULLET, '•').split())
            if not text:
                continue
            x, y = ln['bbox'][0], ln['bbox'][1]
            if y > 750 and PAGE_NO.match(text):
                continue
            out.append((x, y, text))
    out.sort(key=lambda r: (round(r[1], 1), r[0]))
    return out


class CsScheme:
    """One Computer Science marking scheme, keyed as the paper numbers it."""

    def __init__(self, year, level):
        self.year, self.level = year, level
        self.path = os.path.join(SCHEMES, f'{year}-{level}.pdf')
        if not os.path.exists(self.path):
            raise FileNotFoundError(self.path)
        self.doc = pymupdf.open(self.path)
        self._rate = self._section_rates()
        self._points = collections.defaultdict(list)
        self._bands = collections.defaultdict(list)
        self._tariff = {}
        self._split = {}
        self._section = {}
        self._read()

    def _section_rates(self):
        """{section: marks per question} from the PAPER's own rubric.

        Section A prints "Short Answer Questions / Attempt any nine questions /
        54 marks / All questions carry equal marks", and the scheme then prices
        none of those nine individually. A printed total over a printed count,
        with the paper stating in as many words that the questions are equal,
        is the one division the rules allow -- and it is the only thing that
        prices Section A at all. Recorded ONLY where that clause is present.
        """
        paper = os.path.join(ROOT, 'examiner-reports', 'computer-science',
                             'papers', f'{self.year}-{self.level}-038-paper.pdf')
        if not os.path.exists(paper):
            return {}
        with pymupdf.open(paper) as doc:
            head = ' '.join(doc[1].get_text().split()) if doc.page_count > 1 else ''
        out = {}
        for sec, word, marks, equal in SECTION_RUBRIC.findall(head):
            n = COUNT_WORD.get(word.lower())
            if n and equal and int(marks) % n == 0:
                out[sec] = int(marks) // n
        return out

    @staticmethod
    def _rows(page):
        """The page's lines grouped into printed ROWS, left to right.

        A part's tariff is the mark cell on its OWN row -- the layout sets
        "Question 13" and "38 (11, 15, 12) marks" on one line, "(a)" and
        "11 (3,3,3, 2) marks" on the next. That is exact, where a column
        threshold is not: mark cells appear at a dozen different x positions
        in one scheme (60, 283, 396, 425, 482) because the bands beneath a
        part carry their own, and taking the leftmost as the boundary put it
        at x=40 and swallowed the whole page.
        """
        rows, cur = [], []
        for cell in _lines(page):
            if cur and cell[1] - cur[0][1] > 4.0:
                rows.append(sorted(cur, key=lambda c: c[0]))
                cur = []
            cur.append(cell)
        if cur:
            rows.append(sorted(cur, key=lambda c: c[0]))
        return rows

    def _read(self):
        q = letter = roman = None
        key = None
        section = None
        for n in range(len(self.doc)):
            for row in self._rows(self.doc[n]):
                head_x, _, head_t = row[0]
                # The tariff on THIS row, if the row carries one to its right.
                tar = None
                for x, _, t in row[1:]:
                    m = TARIFF.match(t)
                    if m and x > head_x + 40:
                        tar = m
                        break

                sec = SECTION.match(head_t)
                if sec and head_x < 100:
                    section = sec.group(1)
                    continue

                opened = False
                hm = QUESTION.match(head_t)
                if hm and head_x < 100:
                    q, letter, roman = int(hm.group(1)), None, None
                    key, opened = (q, None, None), True
                elif q is not None:
                    lm = LETTER.match(head_t)
                    rm = ROMAN.match(head_t)
                    if lm and head_x < 100:
                        letter, roman = lm.group(1), None
                        key, opened = (q, letter, None), True
                    elif rm and head_x < 130:
                        roman = rm.group(1)
                        key, opened = (q, letter, roman), True
                if opened:
                    self._points.setdefault(key, [])
                    self._section[key] = section
                    if tar:
                        self._tariff[key] = int(tar.group(1))
                        if tar.group(2):
                            self._split[key] = [int(v) for v in
                                                re.findall(r'\d+', tar.group(2))]
                    continue

                if q is None or key is None:
                    continue
                # Everything else on the row is answer or rubric. A row that is
                # ONLY a mark cell prices the band above it and states nothing.
                body = ' '.join(t for _, _, t in row if not TARIFF.match(t)).strip()
                if not body:
                    continue
                if BAND.match(body):
                    self._bands[key].append(body)
                else:
                    self._points[key].append(body)

    # ── the interface ─────────────────────────────────────────────────────
    def parts(self):
        return sorted(self._points, key=lambda k: (k[0], k[1] or '', k[2] or ''))

    def points(self, q, letter=None, roman=None):
        """The scheme's stated answer for this part, as MARKING POINTS.

        A point is a bullet and the lines that wrap under it. A part whose
        answer is prose with no bullets returns its lines unchanged.
        """
        raw = self._points.get((q, letter, roman), [])
        out, cur = [], []
        for line in raw:
            if line.startswith('•'):
                if cur:
                    out.append(' '.join(cur))
                cur = [line.lstrip('• ').strip()]
            elif cur:
                cur.append(line)
            else:
                out.append(line)
        if cur:
            out.append(' '.join(cur))
        return [p for p in out if p.strip()]

    def bands(self, q, letter=None, roman=None):
        """The rubric lines. Never an answer -- kept so a caller can see them."""
        return list(self._bands.get((q, letter, roman), []))

    def tariff(self, q, letter=None, roman=None):
        """What the paper pays for this part, or None.

        Printed on the part's own row wherever the scheme states it. Where it
        does not, the PARENT's row prints the split -- 2024 HL Q11 heads
        "6 (4, 2) marks" over its (a) and (b) -- and the component in this
        part's position is taken from it. That is a printed total over a
        printed count, which is the one division the rules allow, and only
        where the split has exactly one entry per sibling. Never inferred any
        other way: 2024 HL Q16(a) is 50 marks over seven romans with no split
        printed, and every one of those returns None.
        """
        own = self._tariff.get((q, letter, roman))
        if own is not None:
            return own
        if letter is None and roman is None:
            # A whole question the scheme never prices: the paper's rubric
            # does, at the section's equal-marks rate.
            return self._rate.get(self._section.get((q, None, None)))
        parent = (q, None, None) if roman is None else (q, letter, None)
        split = self._split.get(parent)
        if not split:
            return None
        sibs = [k for k in self._points
                if k[0] == q
                and (k[1] == letter if roman is not None else k[1] is not None)
                and (k[2] is not None if roman is not None else k[2] is None)]
        sibs.sort(key=lambda k: (k[1] or '', ROMAN_ORDER.get(k[2], 0)))
        if len(sibs) != len(split):
            return None
        try:
            return split[sibs.index((q, letter, roman))]
        except ValueError:
            return None

    def split(self, q, letter=None, roman=None):
        """The per-part split the head prints, e.g. [11, 15, 12]."""
        return list(self._split.get((q, letter, roman), []))

    def section(self, q, letter=None, roman=None):
        return self._section.get((q, letter, roman))


def main():
    if len(sys.argv) < 3:
        print(__doc__.strip().splitlines()[2].strip())
        raise SystemExit(2)
    year, level = int(sys.argv[1]), sys.argv[2]
    S = CsScheme(year, level)
    if len(sys.argv) > 3:
        q = int(sys.argv[3])
        letter = sys.argv[4] if len(sys.argv) > 4 and sys.argv[4] != '-' else None
        roman = sys.argv[5] if len(sys.argv) > 5 and sys.argv[5] != '-' else None
        print(f'{year} {level.upper()} Q{q}'
              + (f'({letter})' if letter else '') + (f'({roman})' if roman else '')
              + f'   section {S.section(q, letter, roman)}')
        print(f'  tariff  {S.tariff(q, letter, roman)}  split {S.split(q, letter, roman)}')
        for p in S.points(q, letter, roman):
            print(f'  point   {p[:150]}')
        for b in S.bands(q, letter, roman):
            print(f'  band    {b[:120]}')
        return
    parts = S.parts()
    priced = sum(1 for k in parts if S.tariff(*k))
    stated = sum(1 for k in parts if S.points(*k))
    print(f'{year} {level}: {len(parts)} parts, {priced} priced, {stated} with text')
    for k in parts[:8]:
        print(f'   Q{k[0]}({k[1] or "-"})({k[2] or "-"}) {S.tariff(*k)}m '
              f'{len(S.points(*k))} point(s)  {(S.points(*k) or [""])[0][:60]!r}')


if __name__ == '__main__':
    main()
