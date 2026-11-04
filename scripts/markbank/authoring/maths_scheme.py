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


# A heading is the marker alone; the scheme may punctuate it ("(a),").
BARE_MARKER = re.compile(r'^\(([a-h]|i{1,3}|iv|v|vi{0,3})\)'
                         r'(\s*\(([a-h]|i{1,3}|iv|v|vi{0,3})\))?[\s.,;:]*$')
LETTER_SPAN = 20.0   # points: a second letter this close heads the SAME unit
# The space after "Scale" is not always printed: the 2021 Ordinary scheme
# sets "Scale10D (0, 3, 5, 8, 10)" ten times and the 2023 Higher once.
# Requiring it cost those units their scale, and with it their whole band --
# 2021 OL Paper 2 Q2(b) had a marker, a solution and a full credit ladder
# printed, and no card.
SCALE_LINE = re.compile(r'Scale\s*\d+[A-Z]?\s*\(', re.I)
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

# A continuation that omits its parent letter can only inherit the previous
# one mechanically.  This reviewed page changes from Q2(b) to Q2(c)(i) at the
# break while printing only ``(i)``; the paper and the visible scheme heading
# establish the correction.
KEY_CORRECTIONS = {
    (2021, 'hl', 2, 2, 'b', 'i'): (2, 2, 'c', 'i'),
}



_MARKER_ROWS = {}


def raw_scale_rows(page):
    """[(y, side, exact scale text)] read before fraction reconstruction.

    The fraction repair intentionally merges stacked maths with nearby text.
    On 2023 HL page 54 it turns the perfectly printed line
    ``Scale 10C (0, 4, 7, 10)`` into ``Scale Note: 10C If (0, /√64 ...`` by
    splicing the note below through it.  A scale is ordinary one-dimensional
    text in the raw PDF, so read it directly from its own spans and leave the
    fraction repair to the actual solution.
    """
    cut = mathtext.reader_cut(page)
    rows = []
    for block in page.get_text('dict')['blocks']:
        for line in block.get('lines', []):
            spans = sorted(line.get('spans') or [], key=lambda s: s['bbox'][0])
            for n, span in enumerate(spans):
                if 'scale' not in span.get('text', '').lower():
                    continue
                tail = ''.join(s.get('text', '') for s in spans[n:]).strip()
                found = SCALE_LINE.search(tail)
                if not found:
                    continue
                y = min(s['bbox'][1] for s in spans[n:])
                x = span['bbox'][0]
                rows.append((y, 'right' if x >= cut else 'left', tail))
                break
    return rows


def marker_rows(page):
    """[(y, token, in_marker_column)] for every part marker printed on a page.

    The model solution restates its part marker mid-answer: 2022 HL scheme
    page 23 prints a second bare "(b)" 53 points below the heading, and page
    20 prints "(b) h'(x) = 3(2x^2) - 2(28.5x) + 105". Taking either for the
    next unit's heading handed that letter to the band below, which then
    carried the REAL next letter past the last band and dropped it -- Q7 and
    Q8 both lost their (c), and Q8 shipped two cards claiming (b).

    Neither wording nor distance separates the two: the echo is sometimes bare
    and sits anywhere in the answer. The COLUMN does. A heading is printed at
    the table's marker indent (x = 62.3 on those pages), an echo at the
    solution indent (x = 90.7). The indent varies by scheme -- 56.6 in 2022
    Ordinary, 62.4 in 2024 Higher -- so it is measured per page.

    Read from the RAW lines, because placed() merges a marker with the
    solution text beside it and reports the merged row a few points off: 2023
    HL page 20 prints "(b)" at y=80.6 and placed() gives the row as 77.1.
    Callers match on the NEAREST row carrying the same token rather than on a
    y tolerance, which would have to be tight enough to separate a heading
    from an echo six points below it and loose enough to survive that merge.
    """
    key = (page.parent.name, page.number)
    if key not in _MARKER_ROWS:
        rows = []
        for bl in page.get_text('dict')['blocks']:
            for ln in bl.get('lines', []):
                t = ''.join(sp['text'] for sp in ln['spans']).strip()
                mk = MARKER.match(t)
                if mk:
                    rows.append((ln['bbox'][1], mk.group(1).lower(),
                                 ln['spans'][0]['bbox'][0]))
        mx = min((x for _, _, x in rows), default=0.0)
        _MARKER_ROWS[key] = [(y, tok, x <= mx + 6) for y, tok, x in rows]
    return _MARKER_ROWS[key]


def in_marker_column(page, y, tok):
    """Is the marker read at this row PRINTED as a heading, or echoed in the
    answer? Decided by the nearest raw row carrying the same token."""
    near = [(abs(y - my), col) for my, mt, col in marker_rows(page)
            if mt == tok]
    if not near:
        return True
    # A heading and the model solution can begin on exactly the same baseline:
    # 2022 HL Q8 prints the marker-column ``(a)`` beside a solution-column
    # ``(a)(v)``.  Sorting ``(distance, bool)`` chose False on that tie and
    # discarded the genuine heading.  If any raw marker at the nearest
    # baseline is in the marker column, the placed row is a heading.
    distance = min(d for d, _ in near)
    return any(col for d, col in near if abs(d - distance) < 0.5)


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
        # Most schemes put the scale and its credit bands in the right-hand
        # Marking Notes column.  A handful of graphical answers use the full
        # table width and put those notes BELOW the drawing in the left text
        # flow instead.  Keep the source side and the two distinct vertical
        # bands so notes never absorb the drawing and the model-solution crop
        # never absorbs the notes.
        self._notes_side = {}
        self._notes_bounds = {}
        self._solution_bounds = {}
        self._scale_text = {}
        # A second scale can be an alternative METHOD for the same printed
        # part, not a second selectable question.  Retain those source bands
        # for audit without exposing a duplicate card.
        self.alternate_units = {}
        # key -> every roman its one scale marks, where that is more than one
        self.spans = {}
        # key -> the part's marking instructions, filled in by _bands()
        self._asides = {}
        # key -> every LETTER its one scale marks, where that is more than one
        self.letter_spans = {}
        paper, q = 1, None
        last_unit_by_question = {}
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
            page_scales = raw_scale_rows(page)
            if not any('Marking Notes' in t for _, t in right[:3]) \
                    and not page_scales:
                continue
            # The FIRST head anywhere in the column, not the last of the first
            # six lines. A page that opens a section carries four lines of
            # instruction above the table, which pushed "Q1" to the seventh --
            # so Question 1 of the 2021 Ordinary paper was never seen at all
            # and neither were its four parts.
            # EVERY head in the column, with the y it is printed at. A page
            # usually carries one, but not always: 2023 HL scheme page 20
            # heads "Q6" at y=62 and "Q7" at y=330, and filing the whole page
            # under the first put Q7(a) and Q7(b) under Question 6 -- where
            # the second collided with the real Q6(b) and one of the two was
            # dropped as a duplicate id.
            heads = [(y, int(h.group(1))) for y, t in left
                     for h in [QHEAD.match(t.strip())] if h]
            if heads:
                q = heads[0][1]
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
            # The page's opening head governs from the top of the page, which
            # is where a question CONTINUED from the page before begins.
            heads = [(-1e9, q)] + heads[1:]
            right_scales = [(y, side, t) for y, side, t in page_scales
                            if side == 'right']
            left_scales = [(y, side, t) for y, side, t in page_scales
                           if side == 'left']
            # A scale in the left flow is not necessarily a duplicate of the
            # right flow.  2023 HL P2 Q2(a) is a full-width proof whose scale
            # sits below it on the left; Q2(b), lower on the SAME page, uses
            # the normal right column.  Merge both and de-duplicate only rows
            # that truly share a baseline.
            scale_rows = []
            for y, side, scale_text in sorted(right_scales + left_scales):
                if scale_rows and abs(y - scale_rows[-1][0]) < 2:
                    # Prefer the conventional right source when both columns
                    # contain the same scale line.
                    if side == 'right':
                        scale_rows[-1] = (y, side, scale_text)
                    continue
                scale_rows.append((y, side, scale_text))
            scales = [y for y, _, _ in scale_rows]
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
            last_unit_key = None
            q = heads[-1][1]
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
                # A letter handed on by the band above starts this one, so a
                # roman met before any letter of our own still knows which
                # letter it belongs to. Applied BEFORE the scan, not after it:
                # applied after, 2021 OL P2 Q2 read "(ii)" and then "(b)" from
                # the band below, adopted the "(b)" because no letter had been
                # set, and DISCARDED the roman with it -- so (a)(ii) vanished
                # and the unit shipped as a duplicate (b).
                # The LAST letter heading printed above the next scale is
                # the only one that can head the next unit; every other letter
                # in this band shares this band's scale. Distance cannot decide
                # it -- 2023 OL scheme page 39 sets "(a)" and "(b)" 32 points
                # apart over one Scale 10D, while 2021 OL page 11 sets "(a)"
                # and "(b)" 225 points apart over two -- but position relative
                # to the scales can, and that is what the table encodes.
                nxt = bounds[n + 1]
                last_letter_y = None
                # Only a band with another scale below it can see the NEXT
                # unit's marker.  On the final scale, every marker remaining
                # in the band belongs to that one scale.  Treating the final
                # letter as a future marker hid shared units such as 2021 OL
                # Q8(d)+(e), 2024 HL P2 Q1(b)+(c), and 2024 OL P2 Q2(c)+(d).
                if nxt < 1e8:
                    for yy, tt in left:
                        mk2 = MARKER.match(tt.strip())
                        if not mk2:
                            continue
                        a2 = mk2.group(1).lower()
                        b2 = (mk2.group(2) or '').lower()
                        if a2 in ROMANS and (not b2 or b2 in ROMANS):
                            continue
                        if yy >= nxt + 6 or not in_marker_column(page, yy, a2):
                            continue
                        last_letter_y = yy
                letter = roman = None
                own_letter = False
                letters = []
                letter_y = None
                carried_letter = None
                if carried is not None:
                    # Carried means the band ABOVE identified it as not its
                    # own, so it is this band's letter and any further letter
                    # belongs to the band below. Without that, 2021 OL P2 Q2's
                    # second unit read the "(b)" printed 200 points further
                    # down as its own and shipped (b)(ii) where the paper
                    # prints (a)(ii).
                    letter, roman = carried
                    own_letter = True
                    carried_letter = letter
                    carried = None
                romans = []
                for y, t in left:
                    if not (lo - 4 <= y < hi):
                        continue
                    mk = MARKER.match(t.strip())
                    if not mk:
                        continue
                    a = mk.group(1).lower()
                    b = (mk.group(2) or '').lower()
                    if a in ROMANS and (not b or b in ROMANS):
                        # The roman belongs to the letter printed above it: the
                        # scheme sets "(a)" on one line and "(ii)" on the next,
                        # so the two have to be read together. One line can
                        # also head TWO romans -- 2025 OL p39 prints "(i)(ii)"
                        # over a single scale -- and reading the second as a
                        # LETTER cited 2025 OL Q10 as "(c), (i)".
                        roman = a
                        for r in (a, b):
                            if r and r not in romans:
                                romans.append(r)
                        continue
                    # A LETTER is only a heading where the scheme prints
                    # it: in the marker column, not at the solution indent.
                    # Romans are exempt -- a roman is often indented UNDER its
                    # letter (2024 HL scheme page 17 sets "(b)" at x=62.6 and
                    # its "(i)" at x=103.0).
                    if not in_marker_column(page, y, a):
                        continue
                    if own_letter:
                        if a == letter and b:
                            # The SAME letter again carrying a new roman:
                            # "(a)(i)" and then "(a)(ii)" over one scale.
                            # Taken for the next unit's heading it was carried
                            # down, and the band that really marks 2024 HL
                            # Paper 2 Q7(b)(i) was keyed (a)(ii) -- so (b)(i)
                            # had no scheme and (a)(ii) answered the wrong ask.
                            # A BARE repeat still carries: 2021 OL page 34
                            # prints "(a)" again 14 points above the next
                            # scale, where it does head the next unit.
                            # When it is the final heading before ANOTHER
                            # scale, however, it heads that next scale.  2021
                            # OL P2 Q6 prints (b)(ii) 15 points above its own
                            # Scale 10C; folding it into (b)(i)'s Scale 5B
                            # both lost ten marks and created an anonymous
                            # second unit.
                            if last_letter_y is not None \
                                    and abs(y - last_letter_y) <= 0.5:
                                carried = (a, b)
                                break
                            if b not in romans:
                                romans.append(b)
                            if roman is None:
                                roman = b
                            continue
                        if a == carried_letter and letter_y is None:
                            # This band was HANDED its letter by the band above,
                            # which saw the marker in its own foot-lookback --
                            # so meeting it here is this band's OWN marker, not
                            # the next unit's. Re-carrying it instead keyed the
                            # band after this one by the same letter and shifted
                            # every later letter up one: 2021 OL Paper 1 Q3
                            # emitted (b) twice and dropped (c) as a duplicate.
                            letter_y, carried_letter = y, None
                            letters = [a]
                            continue
                        # Any letter that is NOT the last one above the next
                        # scale is marked by THIS band's scale, exactly as
                        # "(a) (i) & (ii)" is for romans: the scheme sets
                        # "(a), (b)" over one scale and marks both together.
                        if last_letter_y is None or abs(y - last_letter_y) > 0.5:
                            if a not in letters:
                                letters.append(a)
                            continue
                        # Bands meet a few points apart and each one can see
                        # its neighbour's marker at its foot, so reading on
                        # named a unit after the one that follows it: 2021 OL
                        # Paper 1 Q3(b) was keyed as Q3(c), collided with the
                        # real Q3(c), and one of the two was dropped.
                        carried = (a, b or None)
                        break
                    # The band's own letter outranks one handed down to it.
                    letter, own_letter, letter_y = a, True, y
                    letters = [a]
                    if b and b not in ROMANS:
                        # Two LETTERS on one heading line -- 2025 HL scheme
                        # page 8 sets "(c)(d)" over a single scale. Putting the
                        # second in the ROMAN slot cited the unit as "Q8(c)(d)"
                        # and the paper reader, asked for a part (d) under a
                        # letter (c), found no question text at all.
                        if b not in letters:
                            letters.append(b)
                        roman = None
                    elif b:
                        # The roman counts toward the band's SPAN even when it
                        # arrives welded to its letter. 2024 HL scheme page 39
                        # prints the heading and the first line of working as
                        # one row -- "(a) (i) zz = (50 - 48.2)/10.6" -- so the
                        # (i) never reached the roman list, and the "(a)(ii)"
                        # marked by the same scale looked like the only one.
                        roman = b
                        if b not in romans:
                            romans.append(b)
                    elif not romans:
                        roman = None
                # One scale, several romans: the scheme heads a unit
                # "(a) (i) & (ii)" and marks both parts together. Keeping only
                # the last roman filed the unit under (ii) and left (i) with no
                # scheme at all — 36 units in the 2024 Ordinary scheme alone.
                # Key on the FIRST, and remember the span so the card can cite
                # every part it answers.
                if letter is not None and len(romans) > 1:
                    roman = romans[0]
                # A head governs every band printed BELOW it.
                qb = heads[0][1]
                for hy, hq in heads:
                    if hy < y0:
                        qb = hq
                key = (paper, qb, letter, roman)
                # A continuation page often repeats only the roman marker.
                # The letter remains the one that opened immediately above:
                # 2023 HL Q4(a)(ii), Q8(b)(ii), 2025 HL Q2(a)(ii), and 2021
                # HL Q2(c)(i) are all printed this way.  Carry it only within
                # the same paper and question, so a genuine top-level roman
                # cannot inherit from an unrelated ask.
                prior = last_unit_key or last_unit_by_question.get((paper, qb))
                if letter is None and roman is not None and prior \
                        and prior[:2] == (paper, qb) and prior[2] is not None:
                    letter = prior[2]
                    key = (paper, qb, letter, roman)
                key = KEY_CORRECTIONS.get(
                    (self.year, self.level, *key[:4]), key)
                letter, roman = key[2], key[3]
                # A later scale with no new marker continues the part directly
                # above it.  2021 OL P2 Q3(a) gives a coordinate method and an
                # algebraic method, each with its own Scale 10D; Q3(b)(ii)
                # likewise gives algebraic and graphical routes.  They are
                # alternative marking routes for ONE ask, not anonymous extra
                # questions and not duplicate cards.
                if letter is None and roman is None and last_unit_key \
                        and last_unit_key[:2] == (paper, qb):
                    self.alternate_units.setdefault(last_unit_key, []).append(
                        (i, lo, hi, scale_rows[n][1]))
                    continue
                if key in self.units:
                    key = (paper, qb, letter, roman, n)
                self.units[key] = (i, lo, hi)
                last_unit_key = key
                last_unit_by_question[(paper, qb)] = key
                side = scale_rows[n][1]
                self._scale_text[key] = scale_rows[n][2]
                self._notes_side[key] = side
                if side == 'left':
                    # The drawing/proof ends where its scale begins; the
                    # marking ladder begins there.  Four points of lookback
                    # retains the scale line itself.
                    self._solution_bounds[key] = (i, lo, max(lo, y0 - 5))
                    self._notes_bounds[key] = (i, y0 - 4, hi)
                else:
                    self._solution_bounds[key] = (i, lo, hi)
                    self._notes_bounds[key] = (i, lo, hi)
                if letter is not None and len(romans) > 1:
                    self.spans[key] = list(romans)
                if len(letters) > 1:
                    self.letter_spans[key] = list(letters)

    def parts(self):
        def order(k):
            return (k[0], k[1], k[2] or '', k[3] or '')
        return sorted(self.units, key=order)

    def _band(self, key, side):
        if side == 'notes':
            i, lo, hi = self._notes_bounds.get(key, self.units[key])
        else:
            i, lo, hi = self._solution_bounds.get(key, self.units[key])
        left, right = mathtext.placed(self.doc[i])
        rows = (right if self._notes_side.get(key, 'right') == 'right' else left) \
            if side == 'notes' else left
        return [t for y, t in rows
                if lo - 4 <= y < hi and not FURNITURE.search(t.strip())]

    def notes(self, key):
        return self._band(key, 'notes')

    def solution(self, key):
        return self._band(key, 'solution')

    def band(self, key):
        """(page index, y0, y1) — for cropping the model solution."""
        return self._solution_bounds.get(key, self.units[key])

    def covered_parts(self, key):
        """[(letter, roman)] covered by this one official scale.

        Most combined units are rectangular: several romans under one letter,
        or several letters with no roman.  One reviewed SEC unit is irregular:
        2022 HL P2 Q8 jointly prices (a)(v) and (b).  Keeping that shape here
        lets the question text, citation and reconciliation all describe what
        the examiner actually marked without inventing a second tariff.
        """
        special = {
            (2022, 'hl', 2, 8, 'a', 'v'): [('a', 'v'), ('b', None)],
        }.get((self.year, self.level, *key[:4]))
        if special:
            return special
        romans = self.spans.get(key)
        if romans:
            return [(key[2], r) for r in romans]
        letters = self.letter_spans.get(key)
        if letters and key[3] is None:
            return [(letter, None) for letter in letters]
        return [(key[2], key[3])]

    def tariff(self, key):
        # Use the pristine raw scale line.  notes() is the fraction-aware text
        # flow and can legitimately mangle a nearby scale while repairing a
        # stacked radical or fraction.
        _, total, ladder = mathtext.steps_and_scale(
            [self._scale_text.get(key, '')])
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
            # Several accepted METHODS repeat Step 1..Step n. They are routes
            # to the same full-credit answer, not sixteen independently
            # claimable checkboxes. Keep the first complete official route;
            # the model-solution figure still shows every accepted method.
            route, seen = [], set()
            for n, text in steps:
                if n in seen:
                    break
                seen.add(n)
                route.append((f'Step {n}', text))
            return route
        route, seen = [], set()
        for lab, bs in self._bands(key):
            if not bs or DEDUCTION.match(lab + ':'):
                continue
            # A second Low/Mid/High sequence marks an alternative method.
            # Mixing both sequences lets a student claim one rung from each
            # route, so stop when the ladder restarts.
            rung = re.sub(r'\W+', '', lab.lower())
            if rung in seen:
                break
            seen.add(rung)
            route.append((lab, '\n'.join(bs)))
        return route


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
