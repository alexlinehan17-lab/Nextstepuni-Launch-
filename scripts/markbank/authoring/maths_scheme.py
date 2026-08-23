#!/usr/bin/env python3
"""The Mathematics marking scheme, read page by page.

    python3 scripts/markbank/authoring/maths_scheme.py 2025 hl

A Maths scheme is one page per part, set as two columns: the Model Solution on
the left and the Marking Notes on the right. See mathtext.py for why only the
left column is damaged by extraction and why the right one is the better answer
for a card.

A page carries:
  * which paper it belongs to -- the year sets TWO papers and both number their
    questions from 1, so a part is keyed (paper, question, letter);
  * the question and part it answers, printed as "Q3" and "(c)";
  * a partial-credit ladder, "Scale 15D (0, 4, 7, 10, 15)", which is the tariff;
  * either a numbered step list or Low/High Partial Credit descriptors, which
    are what a card can carry as text;
  * the model solution's bounding box, for cropping it as a figure.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mathtext                                              # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))))
SCHEMES = os.path.join(ROOT, 'examiner-reports/maths/schemes')

QHEAD = re.compile(r'^Q\s*(\d{1,2})\b')
PART = re.compile(r'^\(([a-h])\)\s*$')
ROMAN = re.compile(r'^\((i{1,3}|iv|v|vi{0,3})\)\s*$', re.I)
PAPER = re.compile(r'\bPaper\s*([12])\b')
# The running header and footer sit inside the notes column's band and get
# welded onto whatever marking point precedes them -- "3 steps correct
# Mathematics Higher Level" -- which the provenance gate is right to refuse
# because the scheme never printed that string. 282 of 530 cards were being
# dropped on it.
# The running footer is set as TWO lines -- "Mathematics" on one and "Higher
# Level" on the next -- so a pattern for the phrase matches neither. Each half
# has to be matched on its own.
FURNITURE = re.compile(
    r'^(Mathematics|(Higher|Ordinary|Foundation)\s+Level'
    r'|Mathematics\s+(Higher|Ordinary|Foundation)\s+Level'
    r'|Leaving Certificate.*|Coimisi.*|State Examinations.*'
    r'|Page \d+|\[?\d{1,3}\]?|Marking Notes|Marking scheme.*|Model Solution.*)\s*$', re.I)

CREDIT = re.compile(r'^(Low|Mid|High)\s+Partial\s+Credit\s*:?\s*$', re.I)
FULL = re.compile(r'^Full\s+Credit\s*(-\s*\d+)?\s*:?\s*$', re.I)


SCALE_LINE = re.compile(r'Scale\s+\d+[A-Z]?\s*\(', re.I)
# "(a)", "(i)", and "(b)(i)" -- the scheme frequently prints the letter and the
# roman on ONE line, sometimes with the solution's first words after them.
# Requiring the whole line to be a single marker left those units unnamed, and
# a unit with no part is a unit with no question.
MARKER = re.compile(r'^\(([a-h]|i{1,3}|iv|v|vi{0,3})\)\s*(?:\(([a-h]|i{1,3}|iv|v|vi{0,3})\))?',
                    re.I)
ROMANS = {'i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii'}


class Scheme:
    """Every marked unit of a Mathematics scheme.

    The unit is a SCALE, not a page. A page is a table and one page commonly
    holds several parts -- 23 of the 61 marked pages of the 2025 Higher scheme
    carry two scales -- so reading a page as one part found 50 units where the
    paper has 84. Each "Scale 15D (0, 4, 7, 10, 15)" opens a new one, and the
    part it belongs to is named by the left-column markers beside it.
    """

    def __init__(self, year, level):
        import pymupdf
        self.year, self.level = year, level
        self.path = os.path.join(SCHEMES, f'{year}-{level}.pdf')
        self.doc = pymupdf.open(self.path)
        self.units = {}
        paper, q = 1, None
        for i, page in enumerate(self.doc):
            m = PAPER.search(page.get_text())
            if m:
                paper = int(m.group(1))
            left, right = mathtext.placed(page)
            if not any('Marking Notes' in t for _, t in right[:3]):
                continue
            for t in (t for _, t in left[:6]):
                h = QHEAD.match(t.strip())
                if h:
                    q = int(h.group(1))
            if q is None:
                continue
            scales = [y for y, t in right if SCALE_LINE.search(t)]
            if not scales:
                continue
            bounds = scales + [1e9]
            for n, y0 in enumerate(scales):
                # A unit runs from ITS OWN scale to the next, not from the
                # previous one: using the previous scale shifted every band up
                # by a unit, so a crop of Q3(b) opened with Q3(a)'s answer
                # sitting above it. The small lookback keeps the part marker,
                # which the scheme prints a few points higher than the scale.
                lo = y0 - 8 if n else 0
                hi = bounds[n + 1] - 8 if bounds[n + 1] < 1e8 else bounds[n + 1]
                # The markers that name this unit sit beside its scale, between
                # the previous scale and the next.
                letter = roman = None
                for y, t in left:
                    if not (lo - 4 <= y < hi):
                        continue
                    mk = MARKER.match(t.strip())
                    if not mk:
                        continue
                    a = mk.group(1).lower()
                    b = (mk.group(2) or '').lower()
                    if a in ROMANS and not b:
                        # The roman belongs to the letter printed above it: the
                        # scheme sets "(a)" on one line and "(ii)" on the next,
                        # so the two have to be read together.
                        roman = a
                        continue
                    if letter is not None:
                        # A SECOND letter in this band is the next unit's, not
                        # this one's. Bands meet a few points apart and each one
                        # can see its neighbour's marker at its foot, so reading
                        # on named a unit after the one that follows it: 2021 OL
                        # Paper 1 Q3(b) was keyed as Q3(c), collided with the
                        # real Q3(c), and one of the two was dropped.
                        break
                    letter, roman = a, (b or None)
                key = (paper, q, letter, roman)
                if key in self.units:
                    key = (paper, q, letter, roman, n)
                self.units[key] = (i, lo, hi)

    def parts(self):
        def order(k):
            return (k[0], k[1], k[2] or '', k[3] or '')
        return sorted(self.units, key=order)

    def _band(self, key, side):
        i, lo, hi = self.units[key]
        left, right = mathtext.placed(self.doc[i])
        rows = right if side == 'notes' else left
        return [t for y, t in rows
                if lo - 4 <= y < hi and not FURNITURE.search(t.strip())]

    def notes(self, key):
        return self._band(key, 'notes')

    def solution(self, key):
        return self._band(key, 'solution')

    def band(self, key):
        """(page index, y0, y1) — for cropping the model solution."""
        return self.units[key]

    def tariff(self, key):
        _, total, ladder = mathtext.steps_and_scale(self.notes(key))
        return total, ladder

    def answer_rows(self, key):
        """[(label, text)] — the marking notes as a card's answer."""
        notes = self.notes(key)
        steps, _, _ = mathtext.steps_and_scale(notes)
        if steps:
            return [(f'Step {n}', t) for n, t in steps]
        out, label, buf = [], None, []
        for line in notes:
            t = line.strip()
            if CREDIT.match(t) or FULL.match(t):
                if label and buf:
                    out.append((label, ' '.join(buf).strip()))
                label, buf = t.rstrip(':'), []
                continue
            if label and t and not t.startswith('Scale') and t != 'Marking Notes':
                buf.append(t.lstrip('• ').strip())
        if label and buf:
            out.append((label, ' '.join(buf).strip()))
        return out


if __name__ == '__main__':
    S = Scheme(int(sys.argv[1]), sys.argv[2])
    print(f'{len(S.parts())} marked units across {len(S.doc)} pages')
    for key in S.parts()[:8]:
        total, ladder = S.tariff(key)
        rows = S.answer_rows(key)
        p, q, l = key[0], key[1], (key[2] or '') + (f'({key[3]})' if key[3] else '')
        print(f'  P{p} Q{q}({l or "-"})  {total} marks, ladder {ladder}, {len(rows)} rows')
        for lab, txt in rows[:3]:
            print(f'        {lab}: {txt[:66]}')
