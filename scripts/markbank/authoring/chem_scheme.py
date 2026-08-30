#!/usr/bin/env python3
"""The Chemistry marking scheme, read as the TABLE it is printed as.

    python3 scripts/markbank/authoring/chem_scheme.py 2022 hl        # summary
    python3 scripts/markbank/authoring/chem_scheme.py 2022 hl 2 b ii # one part

Why a subject-specific reader, when scheme.py and scheme_pdf.py already exist:
each is wrong about this subject in its own way, and neither is repairable
without breaking the eight subjects that depend on it.

  * scheme.Scheme reads the flattened markdown. A Chemistry scheme page is a
    five-column table and flattening interleaves the columns, so a marking
    point comes back as "compou nd of carb on (C) a nd hydrog en (H)" -- and
    the MARK cell, printed 450 points to the right, lands in the middle of the
    answer. It also picks up the running page footer as an answer: several
    keys return nothing but "Higher Level Chemistry 2022 Page".
  * scheme_pdf.SchemePdf keeps the cells apart but takes its question number
    from whichever block last looked like a heading, so the numbered marking
    preamble claims a "Question 4" and much of Sections A and B lands under
    its Q4 and Q8 letters.

The page is a table with a fixed column grid, and reading it as one makes both
problems disappear. Two layouts, sharing that grid:

  A -- 2021 to 2023, CUE style. "QUESTION 2" heads the question; the letter
       sits in the first column, the roman in the second or third, then an
       examiner cue in capitals (DRAW: STATE: WHAT: WHY: IDENTIFY: NAME:
       DESCRIBE: EXPLAIN: GIVE: HOW:), then the answer, then the mark cell.
       The question itself is NOT reprinted.

  B -- 2024 and 2025, REPRINT style. A bare "1." heads the question and the
       scheme reprints the ask above its answer, so a part can be confirmed
       against the paper's own words.

Both put the mark cell in the right margin (x > 470) and a running footer at
the foot (y > 770). Alternatives are separated by the scheme's own " / " and
" // "; bracketed text is an examiner instruction, not an answer, and is
returned separately by asides().

Lifts only. Nothing here composes an answer, and points() returns candidates,
not verdicts -- a key can hold half an ask's answer (2021 OL Q8(b)(ii) asks
what is added to ethene in reactions A and B and the scheme names only B) and
the caller has to read the ask beside them.
"""
import collections
import os
import re
import sys

import pymupdf

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mathtext                                              # noqa: E402

DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(DIR)))
SCHEMES = os.path.join(ROOT, 'examiner-reports', 'chemistry', 'schemes')

QUESTION_WORD = re.compile(r'^QUESTION\s+(\d{1,2})\b', re.I)
QUESTION_NUM = re.compile(r'^(\d{1,2})\.\s*$')
LETTER = re.compile(r'^\(([a-h])\)')
ROMAN = re.compile(r'^\((i{1,3}|iv|v|vi{1,3}|ix|x)\)')
# The mark the examiner awards, printed alone in the right margin: "(3)",
# "(2 × 3)", "(6 + 5)". Never part of an answer.
MARK_CELL = re.compile(r'^\(\s*(\d{1,2})(?:\s*[×x+]\s*(\d{1,2}))?\s*\)\s*$')
# The examiner's cue, in capitals with a colon. It says what KIND of answer is
# wanted, which is a restatement of the ask, not the answer to it.
CUE = re.compile(r'^([A-Z][A-Z’\'/ ]{1,18}):\s*')
ASIDE = re.compile(r'\[[^\]]*\]')
FOOTER = re.compile(r'^(Higher|Ordinary)\s+Level$|^Chemistry\s+20\d\d$|^Page\s+\d+$'
                    r'|^Leaving Certificate|^Chemistry\s*[–-]\s*(Higher|Ordinary)')
BLANK_RUN = re.compile(r'^[\s.…_]*$')
ROMAN_ORDER = {r: i + 1 for i, r in enumerate(
    ['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x'])}


def _squash(text):
    return re.sub(r'[^a-z0-9]', '', (text or '').lower())


def _lines(page):
    """(x, y, text) for every printed line, in reading order, footer dropped."""
    out = []
    for bl in page.get_text('dict')['blocks']:
        for ln in bl.get('lines', []):
            # Through mathtext, which reads a span set smaller and raised (or
            # dropped) as a super/subscript. Chemistry is written in them, and
            # flat text does not merely dull a formula, it FALSIFIES it: the
            # 2022 Ordinary scheme's "1.0 × 10²³ molecules O₂" comes out of a
            # plain span join as "1.0 × 1023 molecules O2", which is a
            # different number and a different substance.
            text = ' '.join(_script_text(ln).split())
            # The scheme labels an alternative "A: bromine"; the space after
            # the colon is its own span and line_text drops it.
            text = re.sub(r'\b([A-Z]):(?=\S)', r'\1: ', text)
            if not text or BLANK_RUN.match(text):
                continue
            x0, y, x1 = ln['bbox'][0], ln['bbox'][1], ln['bbox'][2]
            if y > 770 or FOOTER.match(text):
                continue
            out.append((x0, y, text, x1))
    # A printed ROW is not a single y. The 2023 Ordinary scheme sets the
    # roman "(ii)" at y=143.7 and the answer beside it at y=143.6, so sorting
    # on y to a decimal put the answer BEFORE the marker that opens its part
    # -- and it was filed under the part above. Cluster into rows first, then
    # read each row left to right, which is how the table is printed.
    out.sort(key=lambda r: (r[1], r[0]))
    rows, cur = [], []
    for cell in out:
        if cur and cell[1] - cur[0][1] > 3.0:
            rows.append(sorted(cur, key=lambda r: r[0]))
            cur = []
        cur.append(cell)
    if cur:
        rows.append(sorted(cur, key=lambda r: r[0]))
    return [cell for row in rows for cell in row]


def _script_text(line):
    """A scheme line with Chemistry's super/subscripts read from the BASELINE.

    mathtext.line_text decides by the top of the bounding box, which is right
    for the Mathematics schemes and wrong for these: a smaller glyph's top sits
    LOWER than its neighbour's even when its baseline is raised, so "20.0 cm³"
    came back "20.0 cm₃" and -- far worse -- the iron(II) ion "Fe²⁺" came back
    "Fe₂₊", which is not a charge at all. Ion charges, powers of ten and units
    are most of what a Chemistry scheme prints.

    The baseline is the honest measure: a superscript's origin sits ABOVE its
    neighbour's, a subscript's below. Reading it that way corrects 89 lines
    across the ten schemes.

    This is deliberately NOT a change to mathtext. The bbox rule it uses is
    load-bearing for Mathematics -- every variant of a baseline rule tried
    against both corpora fixed one and broke the other, turning "log₃t" into
    "log³t" and "cos45°" into "cos45_°". Two fonts, two rules.
    """
    spans = [s for s in line['spans'] if s['text'].strip() or s['text'] == ' ']
    if not spans:
        return ''
    weight = {}
    for sp in spans:
        weight[sp['size']] = weight.get(sp['size'], 0) + len(sp['text'].strip())
    base = max(weight, key=lambda k: (weight[k], k)) if any(weight.values()) \
        else max(sp['size'] for sp in spans)
    out = []
    for i, sp in enumerate(spans):
        t = mathtext.demangle(sp['text'])
        prev = spans[i - 1] if i else None
        body = t.strip()
        small = sp['size'] <= base - 1.5 and prev is not None
        shift = (prev['origin'][1] - sp['origin'][1]) if prev else 0.0
        if small and len(body) <= 8 and not re.search(r'[A-Za-z]{2,}', body):
            if shift > 0.12 * sp['size']:
                out.append(mathtext.superscript(body) if hasattr(mathtext, 'superscript')
                           else _wrap(body, True))
                continue
            if shift < -0.12 * sp['size']:
                out.append(_wrap(body, False))
                continue
        out.append(t)
    return ''.join(out)


SUP = str.maketrans('0123456789+-–()n', '⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁻⁽⁾ⁿ')
SUB = str.maketrans('0123456789+-–()n', '₀₁₂₃₄₅₆₇₈₉₊₋₋₍₎ₙ')


def _wrap(body, up):
    """The scheme's own characters, set as the script it printed them as."""
    table = SUP if up else SUB
    if all(c in '0123456789+-–()n' for c in body):
        return body.translate(table)
    return f'^({body})' if up else f'_({body})'


class ChemScheme:
    """One Chemistry marking scheme, keyed the way the PAPER numbers it."""

    def __init__(self, year, level):
        self.year, self.level = year, level
        self.path = os.path.join(SCHEMES, f'{year}-{level}.pdf')
        if not os.path.exists(self.path):
            raise FileNotFoundError(self.path)
        self.doc = pymupdf.open(self.path)
        self._answers = collections.defaultdict(list)
        self._marks = collections.defaultdict(list)
        self._asides = collections.defaultdict(list)
        self._question = {}
        self.mark_x = self._mark_column()
        self.letter_x, self.roman_x = self._marker_columns()
        self._read()

    # ── geometry ──────────────────────────────────────────────────────────
    def _mark_column(self):
        """The RIGHT edge the margin's mark cells are set flush to.

        Measured, not assumed -- it is 511 in the 2021 Ordinary scheme and 538
        in the 2023 Higher. And measured on the right edge, because the cells
        are right-ALIGNED: "(3)" opens at x=519 and "(2 x 3)" at x=503, and
        taking the leftmost opening put the column boundary at 244, which
        swallowed half the answer column. A parenthesised formula in the middle
        of an answer -- "(3)" is a plausible thing for a scheme to print -- is
        excluded by the same edge test.
        """
        edges = collections.Counter(
            round(x1) for n in range(len(self.doc))
            for _, _, t, x1 in _lines(self.doc[n]) if MARK_CELL.match(t))
        return float(edges.most_common(1)[0][0]) if edges else 520.0

    def _marker_columns(self):
        """The x of the LETTER column and of the roman column beside it.

        Taken as the two most common indents at which a marker opens a line.
        The letter is always the leftmost of the two -- a roman is set one
        column deeper than the letter it belongs to, in every one of the ten.
        """
        letters, romans = collections.Counter(), collections.Counter()
        for n in range(len(self.doc)):
            for x, _, t, _x1 in _lines(self.doc[n]):
                if x >= self.mark_x - 60:
                    continue
                if LETTER.match(t):
                    letters[round(x)] += 1
                elif ROMAN.match(t):
                    romans[round(x)] += 1
        lx = letters.most_common(1)[0][0] if letters else 56.0
        rx = romans.most_common(1)[0][0] if romans else lx + 28
        return float(lx), float(rx)

    # ── the walk ──────────────────────────────────────────────────────────
    def _read(self):
        q = letter = roman = None
        key = None
        for n in range(len(self.doc)):
            for x, y, text, x1 in _lines(self.doc[n]):
                # The right margin prices whatever part is open.
                m = MARK_CELL.match(text)
                if m:
                    # A line that is a mark cell and nothing else is never an
                    # answer, wherever it is printed. Only one set in the right
                    # margin is the part's TARIFF though: the working of a
                    # calculation carries its own "(3)" beside each step, and
                    # counting those as the tariff priced 2022 OL Q10(c)(iii)
                    # at three times what the paper pays for it.
                    if key and x1 >= self.mark_x - 6:
                        a, b = int(m.group(1)), m.group(2)
                        self._marks[key].append(a * int(b) if b else a)
                    continue

                head = QUESTION_WORD.match(text) or (
                    QUESTION_NUM.match(text) if x < self.letter_x + 4 else None)
                if head:
                    q, letter, roman = int(head.group(1)), None, None
                    key = None
                    rest = text[head.end():].strip()
                    if not rest:
                        continue
                    text, x = rest, self.letter_x

                if q is None:
                    continue

                # A marker column entry opens a part. Letter and roman can
                # share the line with each other, with the cue, and with the
                # answer -- "(iv) IDENTIFY: 1,2-dibromoethane (BrCH2CH2Br)".
                opened = False
                while True:
                    lm = LETTER.match(text)
                    if lm and x <= self.roman_x - 4:
                        letter, roman = lm.group(1), None
                        text = text[lm.end():].strip()
                        opened = True
                        continue
                    rm = ROMAN.match(text)
                    if rm and x <= self.mark_x - 100:
                        roman = rm.group(1)
                        text = text[rm.end():].strip()
                        opened = True
                        continue
                    break
                if opened:
                    key = (q, letter, roman)
                    self._answers.setdefault(key, [])

                if key is None:
                    continue

                # The cue names the KIND of answer wanted. It restates the ask
                # and belongs on no card: "STATE:", "IDENTIFY:", "DRAW:".
                cm = CUE.match(text)
                if cm:
                    text = text[cm.end():].strip()
                    # A cue can be followed by its own roman: "STATE:   (i)".
                    rm = ROMAN.match(text)
                    if rm:
                        roman = rm.group(1)
                        key = (q, letter, roman)
                        self._answers.setdefault(key, [])
                        text = text[rm.end():].strip()

                for note in ASIDE.findall(text):
                    self._asides[key].append(note.strip('[]').strip())
                text = ASIDE.sub(' ', text)
                text = ' '.join(text.split())
                if text and not BLANK_RUN.match(text):
                    self._answers[key].append(text)

    # ── the interface ─────────────────────────────────────────────────────
    def parts(self):
        return sorted((k for k in self._answers
                       if k[1] is not None or k[2] is not None),
                      key=lambda k: (k[0], k[1] or '', ROMAN_ORDER.get(k[2], 0)))

    def points(self, q, letter=None, roman=None):
        """The scheme's own answer lines for this part, furniture removed."""
        return list(self._answers.get((q, letter, roman), []))

    def marks(self, q, letter=None, roman=None):
        return list(self._marks.get((q, letter, roman), []))

    def asides(self, q, letter=None, roman=None):
        return list(self._asides.get((q, letter, roman), []))

    def tariff(self, q, letter=None, roman=None, rows=None):
        """What the paper pays for this part, or None where it is not certain.

        NEVER GUESSED. A part collects every mark cell printed in its span, and
        that is not always one number:

          * one cell            -- the tariff.
          * a total then its own breakdown, "15" over "3 3 3 3 3" -- the total.
          * equal cells, one per answer row -- the scheme is pricing each row
            ("A: bromine (3)", "B: hydrogen chloride (3)"), so they sum.

        Anything else returns None and the part is reported rather than priced.
        2021 HL Q8(b)(ii) collects [3, 6] and no reading of that is safe.
        """
        marks = self.marks(q, letter, roman)
        if not marks:
            return None
        if len(marks) == 1:
            return marks[0]
        # Tested BEFORE the total rule, which "[3, 3]" also satisfies: two
        # equal cells over two answer rows is the scheme pricing each row, and
        # reading the first as a total of the second halved the part.
        if len(set(marks)) == 1 and rows is not None and len(marks) == rows:
            return sum(marks)
        if marks[0] == sum(marks[1:]):
            return marks[0]
        return None

    def text(self, q, letter=None, roman=None):
        """One string, as the scheme prints it."""
        return ' '.join(self.points(q, letter, roman))

    def answer(self, q, letter=None, roman=None, ask=None):
        """The marking points with any REPRINTED question removed.

        The 2024 and 2025 schemes reprint the ask above its answer, at the same
        indent, so nothing in the geometry separates them -- 2025 HL Q1(a)
        returns "Identify a primary standard that the student could have used
        to standardise the solution of potassium manganate(VII)." and then
        "ammonium iron(II) sulfate / (NH4)2SO4.FeSO4.6H2O", and only the second
        is an answer.

        Pass the PAPER's wording for the part and the lines that reproduce it
        are dropped. That makes the split self-confirming rather than a guess
        about layout: a line is discarded only because a second document shows
        it is the question. Without an ask, every point is returned.
        """
        points = self.points(q, letter, roman)
        if not ask:
            return points
        want = _squash(ask)
        if not want:
            return points
        out = []
        for line in points:
            token = _squash(line)
            if token and len(token) > 8 and token in want:
                continue        # the scheme is reprinting the question here
            out.append(line)
        return out or points

    def alternatives(self, q, letter=None, roman=None):
        """The accepted answers as the scheme separates them: " / " and " // ".

        Kept as printed. The scheme's slash is its own notation for "either of
        these earns the mark", and joining them would state something it never
        said.
        """
        out = []
        for line in self.points(q, letter, roman):
            for piece in re.split(r'\s*//\s*|\s+/\s+', line):
                piece = piece.strip(' /')
                if piece:
                    out.append(piece)
        return out


def main():
    if len(sys.argv) < 3:
        print(__doc__.strip().splitlines()[2].strip())
        raise SystemExit(2)
    year, level = int(sys.argv[1]), sys.argv[2]
    S = ChemScheme(year, level)
    if len(sys.argv) > 3:
        q = int(sys.argv[3])
        letter = sys.argv[4] if len(sys.argv) > 4 and sys.argv[4] != '-' else None
        roman = sys.argv[5] if len(sys.argv) > 5 and sys.argv[5] != '-' else None
        print(f'{year} {level.upper()} Q{q}'
              + (f'({letter})' if letter else '') + (f'({roman})' if roman else ''))
        print(f'  marks   {S.marks(q, letter, roman)}')
        ask = None
        try:
            sys.path.insert(0, DIR)
            import paper as _paper
            ask = _paper.Paper('chemistry', year, level).text(q, letter, roman)
        except Exception:                                    # noqa: BLE001
            pass
        if ask:
            print(f'  ASK     {ask[:160]}')
        for p in S.answer(q, letter, roman, ask=ask):
            print(f'  answer  {p}')
        for a in S.asides(q, letter, roman):
            print(f'  aside   [{a}]')
        return
    parts = S.parts()
    print(f'{year} {level}: {len(parts)} parts, mark right edge {S.mark_x:.0f}, '
          f'letters x={S.letter_x:.0f}, romans x={S.roman_x:.0f}')
    priced = sum(1 for k in parts if S.marks(*k))
    print(f'   {priced} priced, {sum(1 for k in parts if S.points(*k))} with text')
    for k in parts[:8]:
        print(f'   Q{k[0]}({k[1] or "-"})({k[2] or "-"}) {S.marks(*k)} '
              f'{S.text(*k)[:80]!r}')


if __name__ == '__main__':
    main()
