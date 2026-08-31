#!/usr/bin/env python3
"""Read an Engineering marking scheme off the PAGE, not off flattened text.

    python3 scripts/markbank/authoring/eng_scheme.py             # coverage
    python3 scripts/markbank/authoring/eng_scheme.py 2025 hl 1   # one question

Engineering prints two documents inside one PDF and this module reads both.

THE TARIFF TABLE. Every scheme opens with a grid listing each question's parts
and what each is worth, and it is the paper's own arithmetic rather than
anything inferred:

    Question 1 - 50 marks   Question 2 - 50 marks    Question 3 - 50 marks
    Any ten @ 5 marks each  Answer all parts         Answer all parts
    (a)  3 + 2              (a) (i)   5              (a) (i)    4
    (b)  5                      (ii)   3 + 2             (ii)   4
    (e)  Any one @ 5        (e) Any two @ 5 + 5     (b) Any three @ 6 + 6 + 6

Higher Level sets it in THREE columns and Ordinary Level in two, and Ordinary
writes the same thing differently -- "Any two parts @ 7 marks" with the total
"(14)" in its own column. Flattened to text the columns weld into each other
and one line reads "(a) 3 + 2 (a) (i) 5 (a) Any two @ 8 + 8", which is three
questions' tariffs in a row. The columns are recovered from the x coordinates.

THE ANSWER BODY. Each part is then answered under a bold heading, either as
bulleted points or as a paragraph, with the tariff repeated bold and
right-aligned at the foot:

    (c)  Safety precautions to be observed when using cutting fluids:
         * Avoid splashes on skin, wash immediately, use skin barrier cream.
         * Wear eye protection.                                        3 + 2

The bold heading is the scheme's restatement of the ask, not a marking point;
the non-bold lines under it are the answer. Diagram callouts -- "inductor",
"Austenite surface layer" -- sit in the same text layer as the answer and are
NOT part of it, so a line that overlaps a picture is left out.
"""
import argparse
import collections
import os
import re
import sys

import pymupdf

DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, DIR)
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(DIR)))

from paper import unligature                                # noqa: E402

SCHEMES = os.path.join(ROOT, 'examiner-reports', 'engineering', 'schemes')

QHEAD = re.compile(r'^Question\s*(\d{1,2})\b', re.I)
# A rule that carries its own group total: "Three parts @ 2 marks (15)".
#
# It must be the total that follows THIS rule's own "marks", not the last one
# on the line. Ordinary sets the grid in columns narrow enough that the row
# join welds two cells together -- "Three parts @ 2 marks (15) (c) Any two
# parts @ 5 marks (10)" is two cells, and reading the line's last total closed
# the first cell against the SECOND cell's arithmetic. Six cells a corpus were
# discarded that way, each one read correctly and then thrown out.
TRAILING_TOTAL = re.compile(r'marks?\s*\((\d{1,3})\)', re.I)
# The summary table's own question head, which carries the total: "Question 1 -
# 50 marks" at Higher, "Question 1: 50 marks" at Ordinary.
SUMMARY_HEAD = re.compile(r'^Question\s*(\d{1,2})\s*[:\-–]\s*(\d{1,3})\s*marks', re.I)
# 'i' is NOT a letter here: alone it is a roman first. Without the exclusion
# "(i) Three parts @ 3 marks" priced a part (i) that does not exist, and the
# roman it really is went unpriced.
MARKER = re.compile(r'^\(([a-hj-z])\)')
# The Symbol-font bullet reaches the text layer as U+F0B7 and, once the glyph
# map has been applied, as an ordinary bullet. Either way it is a line of its
# own with the marking point on the line after it.
BULLET = re.compile(r'^[\u2022\uf0b7\uf0d8\u25cf\u00b7\u2023]\s*')
ROMAN = re.compile(r'^\((i{1,3}|iv|v|vi{1,3}|ix|x)\)')
# Both spellings of a tariff. Higher writes the split out -- "3 + 2", "8 + 1 +
# 1", "Any two @ 8 + 8" -- and Ordinary writes the rule and the total -- "Any
# two parts @ 7 marks" with "(14)" beside it.
SPLIT = re.compile(r'^\d{1,2}(?:\s*\+\s*\d{1,2})*$')
ANY_AT = re.compile(r'^Any\s+(\w+)(?:\s+parts?)?\s*@\s*(.+)$', re.I)
N_AT = re.compile(r'^(One|Two|Three|Four|Five|Six|Seven|Eight|Nine|Ten)\s+'
                  r'(?:[a-z]+s?\s+)?@\s*(\d{1,2})\s*marks?', re.I)
TOTAL_ONLY = re.compile(r'^\((\d{1,3})\)$')
WORD = {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6,
        'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10, 'eleven': 11,
        'twelve': 12, 'thirteen': 13}
OR_ROW = re.compile(r'^(?:Or|OR)$')
# The letter each of i, v and x follows, when a question is lettering
# rather than numbering its romans.
FOLLOWS = {'i': 'h', 'v': 'u', 'x': 'w'}
# Ordinary Level sets its answers in a two-column table with the mark cell
# beside the answer, and the cell lands wherever the row join puts it -- MID
# SENTENCE, in "Wear heat resistant gloves when preforming heat treatment of
# Total (8) Marks metals." It is the marking grid, never the answer, so it
# comes out before a point is assembled rather than off the end of one.
MARK_CELL = re.compile(r'\s*\bTotal\s*\(?\d{1,3}\)?\s*Marks?\b\s*', re.I)
# The running footer arrives the same way and welds onto the end of a point:
# "Stepper motors are driven by control circuits Page 18".
PAGE_FOOT = re.compile(r'\s*\bPage\s+\d{1,3}\b\s*', re.I)


def _lines(page, join='block'):
    """(x0, y0, x1, y1, text, bold) for every line, ligatures folded.

    Two pages, two assemblies, because the scheme really is two documents.

      join='block' -- the ANSWER BODY. Lines sharing a baseline inside one
        pymupdf block are joined, and the block boundary is the column
        boundary: 2021 Ordinary Level sets its answers in a two-column table
        with "Award 3 @ 3 Marks" beside the answer, and joining across the page
        welded the mark cell into the middle of the answer.

      join='row' -- the TARIFF TABLE. There the blocks are useless: one runs
        x46 to x564 and holds cells from all three columns in reading order,
        so the grid has to be rebuilt from the coordinates. Lines sharing a
        baseline anywhere on the page are joined while the gap between them
        stays under 60pt, which keeps "(a)" with its own "3 + 2" and away from
        the next column's marker 116pt to its right.

    Joining matters either way: the scheme sets a part's marker and its
    heading as two lines at the same y -- "(a)" at x=39 and "Advantages of
    voice activated technology include:" at x=75 -- and read apart the marker
    carries no text and the heading became a marking point.
    """
    out = []
    blocks = page.get_text('dict')['blocks']
    if join == 'row':
        blocks = [{'lines': [l for b in blocks for l in b.get('lines', [])],
                   'number': 0}]
    for block in blocks:
        rows = []
        for line in block.get('lines', []):
            spans = line['spans']
            text = unligature(' '.join(''.join(s['text'] for s in spans).split()))
            if not text:
                continue
            bold = any('Bold' in s.get('font', '') for s in spans)
            x0, y0, x1, y1 = line['bbox']
            rows.append((x0, y0, x1, y1, text, bold))
        rows.sort(key=lambda r: (round(r[1], 1), r[0]))
        for row in rows:
            close = (row[0] - out[-1][2] < 60) if (out and join == 'row') else True
            if out and out[-1][6] == block_id(block) and close and \
                    abs(out[-1][1] - row[1]) <= 2.0:
                p = out[-1]
                out[-1] = (p[0], min(p[1], row[1]), max(p[2], row[2]),
                           max(p[3], row[3]), f'{p[4]} {row[4]}'.strip(),
                           p[5] or row[5], p[6])
            else:
                out.append(row + (block_id(block),))
    out.sort(key=lambda r: (round(r[1], 1), r[0]))
    return [r[:6] for r in out]


def block_id(block):
    return block.get('number', id(block))


def _columns(rows, page_width):
    """Split the summary grid into its columns by x.

    The gaps between columns are the widest empty vertical bands on the page.
    Rather than guess at them, the column a line belongs to is decided by which
    QUESTION HEAD it sits under: the heads are the only lines that name a
    column, and every part below one belongs to it until the next head.
    """
    heads = [(x0, y0, SUMMARY_HEAD.match(t)) for x0, y0, _, _, t, _ in rows
             if SUMMARY_HEAD.match(t)]
    if not heads:
        return {}
    edges = sorted({round(x0) for x0, _, _ in heads})
    # Two heads a point apart are the same column printed on different rows.
    merged = [edges[0]]
    for e in edges[1:]:
        if e - merged[-1] > 40:
            merged.append(e)
    # A column's boundary is HALFWAY to the next one, not a fixed inset from
    # its own head. 2022 Higher indents its heads about eighteen points to the
    # RIGHT of the rows beneath them -- heads at x78, x252, x426 over content
    # at x60, x237, x410 -- so a fixed inset put every row in the column to
    # its left and dropped the first column's rows off the page entirely.
    # That paper read 29 part tariffs where 2023 read 64, and 289 leaves
    # across the subject were unpriced and climbing to their question.
    bands = []
    for i, left in enumerate(merged):
        lo = 0.0 if i == 0 else (merged[i - 1] + left) / 2.0
        hi = ((left + merged[i + 1]) / 2.0 if i + 1 < len(merged)
              else page_width + 1)
        bands.append((lo, hi))
    return bands


def _band(x0, bands):
    for i, (left, right) in enumerate(bands):
        if left <= x0 < right:
            return i
    return None


# Ordinary Level writes the same rule three ways across the years, and 2023
# and 2024 write it with the ask's own verb in front -- "Explain any two @ 7
# marks", "Name any three @ 5 marks" -- or with the thing counted in place of
# "parts": "Three materials @ 3 marks", "Two precautions @ 4 marks", "Two
# reasons @ 2 marks". Neither spelling parsed, so 2023 Ordinary Level yielded
# TWO priced parts out of a whole paper. The verb is stripped and the noun
# allowed; the arithmetic underneath is the same and still the paper's own.
LEAD_VERB = re.compile(
    r'^(?:award\s+)?(?:briefly\s+)?(?:calculate|compare|define|describe'
    r'|determine|differentiate|discuss|distinguish|draw|explain|give'
    r'|identify|indicate|label|list|name|outline|sketch|state|suggest)\b\s*',
    re.I)
# "Describe @ 12 marks" states one point worth twelve.
BARE_AT = re.compile(r'^@\s*(\d{1,2})\s*marks?', re.I)


def parse_tariff(text):
    """(notation, total marks, per-option rule) for one tariff cell, or None.

    Never invents a number. "3 + 2" is two marking points worth 3 and 2; "Any
    two @ 8 + 8" is any two of the points at 8 each; "Any three parts @ 5
    marks" is Ordinary's spelling of the same thing. A cell it cannot read
    returns None and the part goes unpriced rather than guessed.
    """
    t = ' '.join(text.split())
    t = LEAD_VERB.sub('', t).strip()
    m = BARE_AT.match(t)
    if m:
        return (t, int(m.group(1)), (1, int(m.group(1))))
    m = ANY_AT.match(t)
    if m:
        n = WORD.get(m.group(1).lower())
        rest = m.group(2).strip()
        parts = [int(x) for x in re.findall(r'\d{1,2}', rest)]
        if n and parts:
            # "8 + 8" repeats the per-option value; "5 marks" states it once.
            per = parts[0]
            if len(parts) > 1 and len(set(parts)) == 1 and len(parts) == n:
                return (t, per * n, (n, per))
            if len(parts) == 1:
                return (t, per * n, (n, per))
        return None
    m = N_AT.match(t)
    if m:
        n, per = WORD.get(m.group(1).lower()), int(m.group(2))
        if n:
            return (t, n * per, (n, per))
    if SPLIT.match(t):
        vals = [int(x) for x in re.findall(r'\d{1,2}', t)]
        return (t, sum(vals), None)
    return None


class EngScheme:
    """One sitting's marking scheme: its tariff table and its answers."""

    def __init__(self, year, level):
        self.year, self.level = year, level
        self.path = os.path.join(SCHEMES, f'{year}-{level}.pdf')
        self._tariffs = None
        self._per_part = None
        self._body = None

    # ── the tariff table ───────────────────────────────────────────────────
    def _summary_pages(self):
        with pymupdf.open(self.path) as doc:
            for n in range(min(14, doc.page_count)):
                rows = _lines(doc[n], join='row')
                heads = [t for *_, t, _ in rows if SUMMARY_HEAD.match(t)]
                if len(heads) >= 2:
                    yield n, rows, doc[n].rect.width

    def tariffs(self):
        """{(q, letter, roman): (notation, total, per-option rule)}"""
        if self._tariffs is not None:
            return self._tariffs
        out = {}
        for _, rows, width in self._summary_pages():
            bands = _columns(rows, width)
            if not bands:
                continue
            # Walk each column top to bottom in its own right: a row of the
            # grid holds one part from each of three DIFFERENT questions, so
            # reading the page in reading order interleaves them.
            per_col = collections.defaultdict(list)
            for r in rows:
                b = _band(r[0], bands)
                if b is not None:
                    per_col[b].append(r)
            for col in sorted(per_col):
                self._read_column(sorted(per_col[col], key=lambda r: r[1]), out)
        self._tariffs = out
        return out

    def _read_column(self, rows, out):
        """Walk one column of the grid, settling each part against its total.

        A part's rule may run over SEVERAL lines, and only the last of them
        carries the printed total:

            (a) - Three parts @ 3 marks
                  Three parts @ 2 marks    (15)

        (a) is worth 3x3 + 3x2 = 15, and reading the last line alone prices it
        at 6. The total in the margin is the paper's own arithmetic over the
        whole group, so it is the check: lines are ACCUMULATED until a printed
        total closes them, and the group is accepted only when what was read
        adds up to what was printed. Fourteen cells were mispriced this way.

        A group may span more than one key, and then the total is the parent's:

            (a) - (i) Two parts @ 5 marks
                  (ii) One part @ 10 marks   (20)

        (i) is 10 and (ii) is 10; the (20) belongs to (a).
        """
        q = letter = roman = None
        group = []              # [(key, notation, marks, rule)] since the marker

        def flush(printed=None):
            if not group:
                return
            per_key = collections.OrderedDict()
            lines_for = collections.Counter()
            for key, notation, marks, rule in group:
                lines_for[key] += 1
                if key in per_key:
                    note, tot, first = per_key[key]
                    per_key[key] = (f'{note}; {notation}', tot + marks, first)
                else:
                    per_key[key] = (notation, marks, rule)
            grand = sum(t for _, t, _ in per_key.values())
            if printed is not None and grand != printed:
                # The reader did not understand this cell. A tariff is never
                # guessed, so the part goes unpriced and its cards are refused.
                group.clear()
                return
            for key, (notation, tot, rule) in per_key.items():
                # "Any two @ 8 + 8" prices any TWO of the points at eight
                # each, and that per-option rule is what lets a card offer
                # them as alternatives. It survives whenever this key was
                # stated on a line of its own; only a key assembled from
                # several lines has no single rule to name.
                out.setdefault(key, (notation, tot,
                                     rule if lines_for[key] == 1 else None))
            if printed is not None and len(per_key) > 1:
                # One total over several romans prices their PARENT.
                parent = (q, letter, None)
                out.setdefault(parent, (f'{printed} marks', printed, None))
            group.clear()

        for x0, y0, x1, y1, text, _bold in rows:
            h = SUMMARY_HEAD.match(text)
            if h:
                flush()
                q, letter, roman = int(h.group(1)), None, None
                out.setdefault((q, None, None), (text, int(h.group(2)), None))
                continue
            if q is None:
                continue
            body = text
            m = MARKER.match(body)
            if m:
                flush()
                letter, roman = m.group(1), None
                body = body[m.end():].strip()
                # Ordinary separates a marker from its rule with a dash.
                # Left in place it defeated the parse, so the FIRST line of
                # every multi-line rule was dropped and the continuation
                # line priced the part on its own. It is stripped before
                # the roman test because "(a) - (i) Two parts @ 5 marks"
                # hides the roman behind it.
                body = re.sub(r'^[\u2010-\u2015\-]\s*', '', body).strip()
            r = ROMAN.match(body)
            if r and not m and r.group(1) in FOLLOWS and letter == FOLLOWS[r.group(1)] \
                    and roman is None:
                # "(i)" after "(h)" is the LETTER i, not roman one. The marker
                # pattern leaves i, v and x out because alone they are romans
                # far more often than letters -- but a question that runs (g),
                # (h), (i) is lettering, and Question 1 does exactly that in
                # every Higher paper. Read as a roman, part (i) was priced
                # under (g) and had no tariff of its own, so it resolved up to
                # the whole question and took all fourteen parts with it.
                letter, roman, r = r.group(1), None, None
                body = body[ROMAN.match(body).end():].strip()
            if r:
                # A roman on a line of its own CONTINUES the letter's group
                # rather than starting one: the total below covers them both.
                roman = r.group(1)
                body = body[r.end():].strip()
            if not body:
                continue
            if OR_ROW.match(body):
                flush()
                continue
            tot = TOTAL_ONLY.match(body)
            if tot:
                flush(int(tot.group(1)))
                continue
            parsed = parse_tariff(body)
            if parsed:
                group.append(((q, letter, roman),) + parsed)
                # A rule may carry its own total at the end of the line, and
                # that closes the group it completes.
                closing = TRAILING_TOTAL.search(body)
                if closing:
                    flush(int(closing.group(1)))
        flush()
        return out

    def per_part(self, q):
        """What EACH part of this question is worth, when the scheme says so.

        Question 1 is answered "any ten of the following" and the tariff table
        prices only the question -- "Question 1 - 50 marks" -- with the rule on
        the line beneath it: "Any ten @ 5 marks each", "Any eight parts @ 6
        marks each". Every part then resolves up to the question and one card
        carries all eighteen of them, which is not a card.

        The rule is the paper's own arithmetic and it says what a part is
        worth, so a part-level card can claim it. Only when it says EACH, and
        only when it names ONE value: 2021 Ordinary Level says "Any eight."
        and then "Two @ 7 marks, six @ 6 marks", which prices some parts at 7
        and some at 6 without saying which, and a tariff is never guessed.
        """
        if self._per_part is None:
            self._per_part = {}
            for _, rows, width in self._summary_pages():
                bands = _columns(rows, width)
                if not bands:
                    continue
                per_col = collections.defaultdict(list)
                for r in rows:
                    b = _band(r[0], bands)
                    if b is not None:
                        per_col[b].append(r)
                for col in sorted(per_col):
                    seq = sorted(per_col[col], key=lambda r: r[1])
                    for i, row in enumerate(seq):
                        h = SUMMARY_HEAD.match(row[4])
                        if not h:
                            continue
                        for nxt in seq[i + 1:i + 3]:
                            t = ' '.join(nxt[4].split())
                            if SUMMARY_HEAD.match(t) or MARKER.match(t):
                                break
                            if not re.search(r'\beach\b', t, re.I):
                                continue
                            if t.count('@') != 1:
                                continue
                            parsed = parse_tariff(t)
                            if parsed and parsed[2]:
                                self._per_part[int(h.group(1))] = parsed[2][1]
                            break
        return self._per_part.get(q)

    # ── the answer body ────────────────────────────────────────────────────
    def body(self):
        """{(q, letter, roman): {'lead': str, 'points': [str], 'marks': str}}"""
        if self._body is not None:
            return self._body
        out = collections.OrderedDict()
        summary = {n for n, _, _ in self._summary_pages()}
        with pymupdf.open(self.path) as doc:
            q = letter = roman = None
            or_branch = False
            for n in range(doc.page_count):
                if n in summary:
                    continue
                page = doc[n]
                rows = _lines(page)
                # The answer column's left edge: where the prose on this page
                # actually starts, not a guess at it.
                wide = [r[0] for r in rows if len(r[4]) > 40]
                margin = min(wide) if wide else 0.0
                art = self._artwork(page)
                right = page.rect.width - 60
                for x0, y0, x1, y1, text, bold in rows:
                    h = QHEAD.match(text)
                    if h and bold:
                        q, letter, roman = int(h.group(1)), None, None
                        continue
                    if q is None:
                        continue
                    # A bold number hard against the right margin is the
                    # tariff repeated at the foot of the part, not an answer.
                    if bold and x1 >= right and parse_tariff(text):
                        key = (q, letter, roman)
                        if key in out:
                            out[key]['marks'] = text
                        continue
                    if any(a[0] - 2 <= x0 and x1 <= a[2] + 2
                           and a[1] - 2 <= y0 and y1 <= a[3] + 2 for a in art):
                        continue          # a callout printed on a diagram
                    body_text = text
                    # The scheme sets an ALTERNATIVE the way the paper does: a
                    # standalone OR, then the same markers again. 2021 HL Q8
                    # answers (c)(i) and (c)(ii) on surface grinding, then OR,
                    # then (c)(i) and (c)(ii) on subtractive manufacturing.
                    if OR_ROW.match(body_text):
                        or_branch = True
                        continue
                    m = MARKER.match(body_text)
                    r = None
                    if m:
                        letter, roman = m.group(1), None
                        body_text = body_text[m.end():].strip()
                        r = ROMAN.match(body_text)
                    elif bold:
                        r = ROMAN.match(body_text)
                    if r:
                        roman = r.group(1)
                        body_text = body_text[r.end():].strip()
                    if m or r:
                        key = (q, letter, roman)
                        # Both branches land on one key, and joined with
                        # nothing between them the sentence assembly ran the
                        # tail of one into the middle of the next: "Both types
                        # can be turned on and off. process, this expands the
                        # tool carrying capacity of the machine." The paper's
                        # own word goes between them, and closes the point.
                        # A marker that re-opens a key which ALREADY HOLDS
                        # ANSWERS is itself the boundary, whether or not the
                        # scheme printed the OR: 2021 HL Q8 answers (c)(i) and
                        # (c)(ii) on surface grinding and then, with no OR at
                        # all, (c)(i) and (c)(ii) on subtractive manufacturing.
                        # Nothing else re-opens an answered key.
                        if out.get(key, {}).get('points'):
                            out[key]['points'].append('OR')
                            # The heading of the FIRST branch is the scheme
                            # restating the ask and is not a marking point.
                            # The second branch's is its answer opening --
                            # "Subtractive manufacturing is a term for various
                            # controlled machining and material removal" --
                            # and setdefault below keeps the first, so without
                            # this the branch begins mid-sentence: fourteen
                            # rows opened on a lowercase word.
                            if body_text:
                                out[key]['points'].append(body_text)
                        or_branch = False
                        out.setdefault(key, {'lead': body_text, 'points': [],
                                             'marks': None})
                        continue
                    key = (q, letter, roman)
                    if key not in out:
                        continue
                    # A callout printed on a diagram, identified by where it
                    # sits and what it is rather than by the artwork it
                    # labels: far to the right of the answer column, a word or
                    # two, closing on nothing. The answers run from the left
                    # margin; "impression" at x538 and "sample" at x442 are
                    # labels on a Vickers indentation diagram, and the
                    # sentence assembly ran them into "the length of the
                    # diagonals of the indentation are ... measured."
                    #
                    # All three conditions are needed. The right-hand column
                    # of a two-column list is also far right, and it is made
                    # of whole marking points, which is what the word count
                    # and the punctuation separate it from.
                    if x0 > margin + 250 and len(body_text.split()) <= 3 \
                            and not re.search(r'[.?!:]$', body_text.strip()):
                        continue
                    out[key]['points'].append(body_text)
        self._body = out
        return out

    @staticmethod
    def _artwork(page):
        out = []
        for im in page.get_images(full=True):
            for r in page.get_image_rects(im[0]):
                out.append((r.x0, r.y0, r.x1, r.y1))
        for d in page.get_drawings():
            r = d['rect']
            if r.width > 40 and r.height > 40:
                out.append((r.x0, r.y0, r.x1, r.y1))
        return out

    # ── what the author asks for ───────────────────────────────────────────
    def tariff(self, q, letter=None, roman=None):
        t = self.tariffs().get((q, letter, roman))
        return t[1] if t else None

    def notation(self, q, letter=None, roman=None):
        t = self.tariffs().get((q, letter, roman))
        return t[0] if t else None

    def rule(self, q, letter=None, roman=None):
        """(claim count, per-option marks) where the scheme prints 'Any N @'."""
        t = self.tariffs().get((q, letter, roman))
        return t[2] if t else None

    def points(self, q, letter=None, roman=None):
        """The part's marking points, one per point rather than per line.

        A bulleted answer gives one point per BULLET, with the lines that wrap
        under it joined back on -- read line by line, "Increased efficiency
        and productivity, users can accomplish various actions, such as
        setting" and "reminders, scheduling appointments, or searching for
        information" are two thirds of one sentence, and a card would have
        claimed a mark for each half.

        An answer with no bullets is ONE point: the scheme answers "Function
        of a heatsink" with a paragraph, and its four lines are four lines of
        one answer, not four things a candidate could have written.
        """
        b = self.body().get((q, letter, roman))
        if not b:
            return []
        lines = [PAGE_FOOT.sub(' ', MARK_CELL.sub(' ', x)) for x in b['points']]
        # The bold heading is the scheme's restatement of the ask and not a
        # marking point -- but only when it is a whole one. 2021 HL Q4(b)(iii)
        # sets "Point X is the eutectic point. This is where the liquid steel
        # turns into solid steel without" in bold and "going through a pasty
        # stage." underneath, and the boldness changes MID-SENTENCE. Cutting
        # there left the answer starting "going through a pasty stage", which
        # is what a student would screenshot. A lead that does not close, above
        # a point that does not open, is one sentence and is rejoined.
        lead = ' '.join((b.get('lead') or '').split())
        if lines and lead and not re.search(r'[.?!:]\s*$', lead) \
                and re.match(r'[a-z]', lines[0].strip()):
            lines = [f'{lead} {lines[0]}'.strip()] + list(lines[1:])
        if not any(BULLET.match(x) for x in lines):
            # One point per SENTENCE, not one per key. Joining every line a
            # key holds made points of 1,588 characters -- a whole column of
            # the Ordinary Level table welded together -- and no such string
            # appears in the scheme, so the provenance gate refused all of
            # them. A line that ends on a full stop ends its point.
            out, cur = [], []
            for n, line in enumerate(lines):
                if line.strip() in ('OR', 'Or'):
                    if cur:
                        out.append(' '.join(cur).strip())
                        cur = []
                    continue
                cur.append(line)
                # A full stop ends a point only when what follows STARTS one.
                # "It occurs at approx." ends a line on a period and the
                # sentence runs on, so splitting there left the next point
                # opening "1140°C and 4.3% carbon content" -- and a card whose
                # answer begins mid-sentence is a card a student screenshots.
                # 42 rows across the subject began that way.
                nxt = next((x.strip() for x in lines[n + 1:] if x.strip()), '')
                # ... but a lone lowercase WORD after a closed sentence is a
                # diagram callout, not the sentence running on: "TIG welding
                # is generally a manual operation." followed by "electrode".
                # Carried on, the label lands inside the marking point and no
                # such sentence is in the scheme, so the point is refused.
                runs_on = re.match(r'[a-z]', nxt) and len(nxt.split()) > 1
                if re.search(r'[.?!:]$', line.strip()) and not runs_on:
                    out.append(' '.join(cur).strip())
                    cur = []
            if cur:
                out.append(' '.join(cur).strip())
            return [x for x in out if x]
        out = []
        for line in lines:
            if BULLET.match(line):
                out.append(BULLET.sub('', line).strip())
            elif out:
                out[-1] = f'{out[-1]} {line}'.strip()
        return [x for x in out if x]

    def points_under(self, q, letter=None, roman=None):
        """This key's marking points AND every key beneath it, in page order.

        The scheme prices "(b) Any three @ 6 + 6 + 6" ONCE and then answers
        (b)(i), (b)(ii) and (b)(iii) underneath it. A card citing (b) claims
        the tariff for all three, so it has to carry all three; a card citing
        (b)(i) alone could not claim it.
        """
        out = []
        for key in self.body():
            if key[0] != q:
                continue
            if letter is not None and key[1] != letter:
                continue
            if roman is not None and key[2] != roman:
                continue
            out.extend(self.points(*key))
        return out

    def lead(self, q, letter=None, roman=None):
        b = self.body().get((q, letter, roman))
        return b['lead'] if b else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('year', nargs='?', type=int)
    ap.add_argument('level', nargs='?')
    ap.add_argument('q', nargs='?', type=int)
    args = ap.parse_args()

    if args.q:
        S = EngScheme(args.year, args.level)
        for key, v in S.body().items():
            if key[0] != args.q:
                continue
            print(f'{key}  tariff={S.notation(*key)!r} -> {S.tariff(*key)}'
                  f'  rule={S.rule(*key)}')
            print(f'    lead: {v["lead"][:90]!r}')
            for p in S.points(*key)[:6]:
                print(f'      - {p[:100]}')
        return 0

    sys.path.insert(0, DIR)
    import reconcile as R                                    # noqa: E402
    from paper_census import census_subject                  # noqa: E402
    idx = R.leaf_index(census_subject('engineering'))
    have = priced = stated = both = 0
    for (year, level, _), leaves in sorted(idx.items()):
        S = EngScheme(year, level)
        for leaf in leaves:
            key = (leaf[0], leaf[1], leaf[2])
            have += 1
            t = S.tariff(*key) is not None
            p = bool(S.points(*key))
            priced += t
            stated += p
            both += t and p
    print(f'{have} census asks: {priced} priced ({priced * 100 // have}%), '
          f'{stated} stated ({stated * 100 // have}%), '
          f'{both} BOTH ({both * 100 // have}%)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
