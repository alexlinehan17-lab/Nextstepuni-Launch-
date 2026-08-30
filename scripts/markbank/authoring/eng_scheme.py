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
                  r'(?:parts?\s+)?@\s*(\d{1,2})\s*marks?', re.I)
TOTAL_ONLY = re.compile(r'^\((\d{1,3})\)$')
WORD = {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6,
        'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10, 'eleven': 11,
        'twelve': 12, 'thirteen': 13}
OR_ROW = re.compile(r'^(?:Or|OR)$')


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
    # A column owns the x range from its own left edge to the next one.
    bands = []
    for i, left in enumerate(edges):
        right = edges[i + 1] if i + 1 < len(edges) else page_width + 1
        bands.append((left - 12, right - 12))
    return bands


def _band(x0, bands):
    for i, (left, right) in enumerate(bands):
        if left <= x0 < right:
            return i
    return None


def parse_tariff(text):
    """(notation, total marks, per-option rule) for one tariff cell, or None.

    Never invents a number. "3 + 2" is two marking points worth 3 and 2; "Any
    two @ 8 + 8" is any two of the points at 8 each; "Any three parts @ 5
    marks" is Ordinary's spelling of the same thing. A cell it cannot read
    returns None and the part goes unpriced rather than guessed.
    """
    t = ' '.join(text.split())
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
        q = letter = roman = None
        pending = None          # a marker whose tariff is on a later line
        for x0, y0, x1, y1, text, _bold in rows:
            h = SUMMARY_HEAD.match(text)
            if h:
                q, letter, roman, pending = int(h.group(1)), None, None, None
                out.setdefault((q, None, None), (text, int(h.group(2)), None))
                continue
            if q is None:
                continue
            body = text
            m = MARKER.match(body)
            if m:
                letter, roman = m.group(1), None
                body = body[m.end():].strip()
            r = ROMAN.match(body)
            if r:
                roman = r.group(1)
                body = body[r.end():].strip()
            if not body:
                pending = (letter, roman)
                continue
            if OR_ROW.match(body):
                continue
            tot = TOTAL_ONLY.match(body)
            if tot and pending is not None:
                # Ordinary prints the total in a column of its own, against
                # the rule it belongs to rather than against the marker.
                key = (q, pending[0], pending[1])
                if key in out and out[key][1] is None:
                    out[key] = (out[key][0], int(tot.group(1)), out[key][2])
                continue
            if tot:
                continue
            parsed = parse_tariff(body)
            if parsed:
                key = (q, letter if not m else m.group(1), roman)
                out.setdefault(key, parsed)
                pending = (key[1], key[2])
        return out

    # ── the answer body ────────────────────────────────────────────────────
    def body(self):
        """{(q, letter, roman): {'lead': str, 'points': [str], 'marks': str}}"""
        if self._body is not None:
            return self._body
        out = collections.OrderedDict()
        summary = {n for n, _, _ in self._summary_pages()}
        with pymupdf.open(self.path) as doc:
            q = letter = roman = None
            for n in range(doc.page_count):
                if n in summary:
                    continue
                page = doc[n]
                rows = _lines(page)
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
                        out.setdefault((q, letter, roman),
                                       {'lead': body_text, 'points': [],
                                        'marks': None})
                        continue
                    key = (q, letter, roman)
                    if key not in out:
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
        lines = b['points']
        if not any(BULLET.match(x) for x in lines):
            # One point per SENTENCE, not one per key. Joining every line a
            # key holds made points of 1,588 characters -- a whole column of
            # the Ordinary Level table welded together -- and no such string
            # appears in the scheme, so the provenance gate refused all of
            # them. A line that ends on a full stop ends its point.
            out, cur = [], []
            for line in lines:
                cur.append(line)
                if re.search(r'[.?!:]$', line.strip()):
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
