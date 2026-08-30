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
BARE_QHEAD = re.compile(r'^(\d{1,2})$')
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

# A two-rung scale (10B) heads its one band "Partial Credit:" with no
# Low/Mid/High qualifier. Requiring the qualifier meant the band never
# opened and its marking point was dropped on the floor -- 2025 OL Paper 1
# Q2(a)(i) shipped the DEDUCTION rule as the thing to claim, because that
# was the only header the reader recognised on the part.
CREDIT = re.compile(r'^(Low|Mid|High)?\s*Partial\s+Credit\s*:?\s*$', re.I)
FULL = re.compile(r'^Full\s+Credit\s*([-\u2010-\u2015\u2212]\s*\d+)?\s*:?\s*$', re.I)
# "Full Credit -1:" is a DEDUCTION rule, not a rung on the ladder. The scheme
# prints it with an EN DASH, so the hyphen-only pattern above never matched it
# and its bullet was swept into the band before it -- which is how
# 2021 HL P1 Q1(a)'s High Partial Credit option ended with "Full Credit -1: 0
# -i or -1i as solution, with k not identified."
DEDUCTION = re.compile(r'^Full\s+Credit\s*[-\u2010-\u2015\u2212]\s*\d+\s*:?\s*$', re.I)


SCALE_LINE = re.compile(r'Scale\s+\d+[A-Z]?\s*\(', re.I)
# Marking INSTRUCTIONS, printed in the same column at the same indent as the
# bullets. They are not alternatives a student can claim, and appending them to
# the bullet above -- which is what a plain continuation rule does -- produced
# "List with more than 10 terms but T10 = 22 not clearly identified Note: Accept
# correct answer without supporting work" on 25 cards.
ASIDE = re.compile(r'^(Note\s*:|Misreading|F\*\s|Accept\b|If\b.*:$)', re.I)
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
        # key -> every roman its one scale marks, where that is more than one
        self.spans = {}
        # key -> the part's marking instructions, filled in by _bands()
        self._asides = {}
        paper, q = 1, None
        for i, page in enumerate(self.doc):
            m = PAPER.search(page.get_text())
            if m:
                paper = int(m.group(1))
            left, right = mathtext.placed(page)
            # The table header prints once, on the page a question OPENS. A
            # question that runs on has its continuation page headed by nothing
            # at all -- so requiring "Marking Notes" threw away every part
            # printed after a page break. 2021 OL Paper 1 lost Q1(c) and Q1(d),
            # Q2(c) and Q5(c) that way, each of them priced on its own scale.
            # A page carrying a scale is a marked page whether it says so or not.
            if not any('Marking Notes' in t for _, t in right[:3]) \
                    and not any(SCALE_LINE.search(t) for _, t in right):
                continue
            # The FIRST head anywhere in the column, not the last of the first
            # six lines. A page that opens a section carries four lines of
            # instruction above the table, which pushed "Q1" to the seventh --
            # so Question 1 of the 2021 Ordinary paper was never seen at all
            # and neither were its four parts.
            for t in (t for _, t in left):
                h = QHEAD.match(t.strip())
                if h:
                    q = int(h.group(1))
                    break
            # Some schemes drop the Q. The 2023 Ordinary Paper 2 heads its
            # first two marked pages "Q2" and every page after that with a bare
            # "3", "4", "5", "6" in the same cell -- so from Question 3 on, ten
            # pages of four different questions were all filed under Question 2
            # and collided with each other. Read forward only, and not past the
            # next few, so a stray number in the working cannot claim the page.
            if left:
                for t in (t for _, t in left[:4]):
                    n = BARE_QHEAD.match(t.strip())
                    if n and q is not None and q <= int(n.group(1)) <= q + 3:
                        q = int(n.group(1))
                        break
            if q is None:
                continue
            scales = [y for y, t in right if SCALE_LINE.search(t)]
            if not scales:
                continue
            bounds = scales + [1e9]
            # A marker the PREVIOUS band saw and discarded as "the next unit's"
            # -- see below. It is handed forward rather than found again,
            # because the lookback that would find it varies: 2021 OL scheme
            # page 9 sets Q1(d)'s marker 14.6 points above its own scale line,
            # so the 8-point lookback missed it and the unit shipped LETTERLESS
            # -- keyed as the whole of Q1, carrying a crop of all four parts and
            # a 10-mark tariff against a 30-mark question. Widening the lookback
            # to suit would risk stealing the marker that genuinely belongs to
            # the band above; carrying forward what has already been identified
            # cannot.
            carried = None
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
                romans = []
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
                        if a not in romans:
                            romans.append(a)
                        continue
                    if letter is not None:
                        # A SECOND letter in this band is the next unit's, not
                        # this one's. Bands meet a few points apart and each one
                        # can see its neighbour's marker at its foot, so reading
                        # on named a unit after the one that follows it: 2021 OL
                        # Paper 1 Q3(b) was keyed as Q3(c), collided with the
                        # real Q3(c), and one of the two was dropped.
                        carried = (a, b or None)
                        break
                    letter, roman = a, (b or None)
                if letter is None and carried is not None:
                    letter, roman = carried
                    carried = None
                # One scale, several romans: the scheme heads a unit
                # "(a) (i) & (ii)" and marks both parts together. Keeping only
                # the last roman filed the unit under (ii) and left (i) with no
                # scheme at all — 36 units in the 2024 Ordinary scheme alone.
                # Key on the FIRST, and remember the span so the card can cite
                # every part it answers.
                if letter is not None and len(romans) > 1:
                    roman = romans[0]
                key = (paper, q, letter, roman)
                if key in self.units:
                    key = (paper, q, letter, roman, n)
                self.units[key] = (i, lo, hi)
                if letter is not None and len(romans) > 1:
                    self.spans[key] = list(romans)

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

    def _bands(self, key):
        """[(label, [bullet, ...])] — the notes column, keeping its structure.

        A credit band lists the ALTERNATIVE ways to reach that rung, one per
        bullet, and a bullet may wrap onto following lines. Joining every line
        in a band into one string welded those alternatives together: 2021 HL
        Paper 1 Q1(b)'s Low Partial Credit came out as "(a + bi)² = -5 + 12i a
        + bi = (-5 + 12i) 1/2 r or θ found -5 + 12i plotted on Argand diagram.
        Shows some knowledge of De Moivre's theorem" -- five separate ways to
        earn the rung, read as one sentence. 274 of the 799 cards said
        something like that.

        So a line beginning with the bullet OPENS an alternative and any line
        after it that does not continues the one before.
        """
        out, label, bullets, asides, in_aside = [], None, [], [], False
        for line in self.notes(key):
            t = line.strip()
            if CREDIT.match(t) or FULL.match(t):
                if label is not None:
                    out.append((label, bullets))
                label, bullets, in_aside = t.rstrip(':'), [], False
                continue
            if not t or t.startswith('Scale') or t == 'Marking Notes':
                continue
            if ASIDE.match(t):
                asides.append(t)
                in_aside = True
                continue
            if label is None:
                # Before the first band the scheme states the part's marking
                # instructions -- 2021 HL P1 Q5(b) sets out the four steps the
                # scale is counting. Dropping them lost real marking content.
                if asides:
                    asides[-1] = f'{asides[-1]} {t}'.strip()
                else:
                    asides.append(t)
                continue
            if t.startswith('\u2022'):
                bullets.append(t.lstrip('\u2022 ').strip())
                in_aside = False
            elif in_aside and asides:
                asides[-1] = f'{asides[-1]} {t}'.strip()
            elif bullets:
                bullets[-1] = f'{bullets[-1]} {t}'.strip()
            else:
                bullets.append(t)
        if label is not None:
            out.append((label, bullets))
        self._asides[key] = [a for a in asides if a]
        return [(lab, [b for b in bs if b]) for lab, bs in out]

    def part_notes(self, key):
        """The scheme's marking instructions for the part, in its own words."""
        if key not in self._asides:
            self._bands(key)
        return self._asides.get(key, [])

    def deductions(self, key):
        """The scheme's "Full Credit -1" rules — marking instructions, not rungs."""
        return [(lab, bs) for lab, bs in self._bands(key) if DEDUCTION.match(lab + ':')]

    def answer_rows(self, key):
        """[(label, text)] — the marking notes as a card's answer.

        One row per credit band, because that is what the ladder prices. The
        band's alternatives stay on separate lines inside it; the squash the
        provenance gate makes drops whitespace, so this still traces.
        """
        notes = self.notes(key)
        steps, _, _ = mathtext.steps_and_scale(notes)
        if steps:
            return [(f'Step {n}', t) for n, t in steps]
        return [(lab, '\n'.join(bs)) for lab, bs in self._bands(key)
                if bs and not DEDUCTION.match(lab + ':')]


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
