#!/usr/bin/env python3
"""Lifting helpers for the Chemistry papers set in the PRINTED layout.

The 2026 papers (and the pre-2021 ones) are printed, not tabled: the paper
numbers its questions "1." with italic part markers "(a)" "(i)" down the left,
and the scheme REPRINTS each question in plain type with its answers in bold
beneath, the marks in square brackets at the right margin ("[5+2]") and the
examiner's asides in bold italic brackets ("[any two]"). chem_scheme.py reads
the five-column tables of 2021-2025 and does not apply here.

Both documents number their parts the same way, so one reader splits each into
parts keyed (question, letter, roman, alternative). A card's question text is
the PAPER's print of its part, cut where the scheme's reprint of the same part
ends, so the lead-in the paper sets before the next part ("The solvent was
removed by distillation.") is carried to that next part as context rather than
glued to this one. Its marking points are the scheme's bold lines, closed by
the mark cell on their row.

Every string a card shows comes out of one of the two PDFs through this module.
The super/subscripts Chemistry is written in are read from the baseline
(chem_scheme._script_text), so "Na₂CO₃" and "Co²⁺" stay what the SEC printed.
Nothing here types exam content.

    P = Printed(2026, 'hl')
    P.ask(('1', 'a', 'i', None))        # the paper's words for Q1(a)(i)
    P.items(('1', 'a', 'i', None))      # the scheme's answers, with their cells
"""
import json
import os
import re
import subprocess
import sys
import unicodedata

import fitz

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chem_scheme import _script_text  # noqa: E402
from markbank_authoring import anyN, make_audit, make_card, make_emit, point, tidy  # noqa: E402

DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(DIR)))
PAPERS = os.path.join(ROOT, 'examiner-reports', 'chemistry', 'papers')
SCHEMES = os.path.join(ROOT, 'examiner-reports', 'chemistry', 'schemes')

FOOTER = re.compile(r'^(Leaving Certificate,? 20\d\d|Chemistry\s*[–-]\s*(Higher|Ordinary) Level'
                    r'|Marking Scheme|\d{1,2})\s*$')
# A mark cell at the scheme's right margin: "[2]", "[5+2]", "[6+2+2+2]", "[3×1 + 3]".
# The Ordinary scheme brackets a run of equal steps: "[12+10+(8×1)]".
_TERM = r'(?:\d{1,2}(?:\s*[×x]\s*\d{1,2})?|\(\s*\d{1,2}\s*[×x]\s*\d{1,2}\s*\))'
MARK_CELL = re.compile(r'^\[\s*' + _TERM + r'(?:\s*\+\s*' + _TERM + r')*\s*\]$')
ROUND_CELL = re.compile(r'^\(\s*' + _TERM + r'(?:\s*\+\s*' + _TERM + r')*\s*\)$')
TRAILING_ROUND = re.compile(r'\s+(\(\s*' + _TERM + r'(?:\s*\+\s*' + _TERM + r')*\s*\))$')
TRAILING_CELL = re.compile(r'\s*(\[\s*' + _TERM + r'(?:\s*\+\s*' + _TERM + r')*\s*\])$')
# The examiner's aside in brackets: "[any two]", "[do not accept clear]".
ASIDE = re.compile(r'^\[[^\]]*[a-zA-Z]{3}[^\]]*\]$')
ANY = re.compile(r'^\[any (two|three|four)\]$', re.I)
WORDS = {'two': 2, 'three': 3, 'four': 4}
MAX_OPTIONS = 14


class Line:
    __slots__ = ('page', 'x0', 'y0', 'x1', 'y1', 'text', 'bold', 'math')

    def __init__(self, page, bbox, text, bold, math=False):
        self.page = page
        self.x0, self.y0, self.x1, self.y1 = bbox
        self.text, self.bold, self.math = text, bold, math

    def __repr__(self):
        return (f'<p{self.page} {self.x0:.0f},{self.y0:.0f}-{self.x1:.0f} '
                f'{"B" if self.bold else "-"} {self.text!r}>')


def _bold_share(ln):
    total = sum(len(s['text'].strip()) for s in ln['spans'])
    if not total:
        return 0.0
    bold = sum(len(s['text'].strip()) for s in ln['spans']
               if s['flags'] & 16 or 'Bold' in s['font'])
    return bold / total


_LIGATURES = None


def ligatures():
    """The bank's own ligature table (schemeText.mjs LIGATURES): the SEC's
    fonts set "tt" as one glyph that extracts as "Ʃ", so "plotted" reads
    "ploƩed". Read from the module, never retyped."""
    global _LIGATURES
    if _LIGATURES is None:
        js = "import(process.argv[1]).then(m => console.log(JSON.stringify(m.LIGATURES)))"
        url = 'file://' + os.path.join(ROOT, 'scripts', 'markbank', 'schemeText.mjs')
        _LIGATURES = json.loads(subprocess.run(['node', '--input-type=module', '-e', js, url],
                                               capture_output=True, text=True, check=True).stdout)
    return _LIGATURES


def _spaced(spans):
    """Keep the spaces a script run carries. _script_text reads a small span
    as a super/subscript and strips it, so "cm" + "3 " + "portions" came out
    "cm³portions", and a space set in a smaller size between "HCl" and
    "needed" vanished. A trailing space is split off into a span of the line's
    own size, and a space-only span is read as one space of that size."""
    if not spans:
        return spans
    base = max(sp['size'] for sp in spans)
    out = []
    for sp in spans:
        t = sp['text']
        if t and not t.strip():
            # A no-break space set as a span of its own ("represented",
            # "\xa0", "by") is a space: _script_text keeps only " ".
            out.append(dict(sp, text=' ', size=base))
        elif t != t.rstrip() and sp['size'] < base - 1.0:
            out.append(dict(sp, text=t.rstrip()))
            out.append(dict(sp, text=' ', size=base))
        else:
            out.append(sp)
    return out


def read_lines(path, first=1, last=None):
    """Every printed line, page by page, rows clustered then read left to right."""
    lig = ligatures()
    doc = fitz.open(path)
    out = []
    for pno in range(first, (last or doc.page_count) + 1):
        page = doc[pno - 1]
        cells = []
        for bl in page.get_text('dict')['blocks']:
            for ln in bl.get('lines', []):
                # The equation font's digits are read as the digits they are
                # BEFORE the Maths demangler sees them: it collapses a doubled
                # maths character (a Maths-font quirk), which turned the
                # Chemistry scheme's "1000" into "10" and "26.55" into "26.5".
                ln = dict(ln, spans=_spaced([dict(sp, text=''.join(
                    unicodedata.normalize('NFKD', c) if 0x1D7CE <= ord(c) <= 0x1D7FF
                    else lig.get(c, c) for c in sp['text'])) for sp in ln['spans']]))
                text = ' '.join(_script_text(ln).split())
                # A full stop or comma set in the script's small size has no
                # script form; _script_text wraps it as "_(.)". Unwrap it.
                text = re.sub(r'[_^]\(([^0-9A-Za-z]+)\)', r'\1', text)
                if not text:
                    continue
                if ln['bbox'][1] > 770 and FOOTER.match(text):
                    continue
                # The schemes set worked arithmetic in an equation font, not in
                # bold: it is answer text all the same.
                math = any('Math' in sp['font'] for sp in ln['spans'] if sp['text'].strip())
                cells.append(Line(pno, ln['bbox'], text, _bold_share(ln) >= 0.6, math))
        # A printed row is not one y: a superscript starts higher than its
        # marker (chem_scheme._lines). Cluster at 5 points, then read across.
        cells.sort(key=lambda c: (c.y0, c.x0))
        row = []
        for c in cells:
            if row and c.y0 - row[0].y0 > 5.0:
                out.extend(sorted(row, key=lambda r: r.x0))
                row = []
            row.append(c)
        out.extend(sorted(row, key=lambda r: r.x0))
    return out


# ── splitting a document into its printed parts ─────────────────────────────
QNUM = re.compile(r'^(\d{1,2})\.?$')
HEADER = re.compile(r'^(Section [AB]|See page 1 for instructions.*'
                    r'|This question continues( on the next page)?\.?)$')
LETTER = re.compile(r'^\(([a-l])\)$')
ROMAN = re.compile(r'^\((i|ii|iii|iv|v|vi|vii|viii|ix|x)\)$')
ALTMARK = re.compile(r'^\(?([AB])\)?$')
PAPER_MARK = re.compile(r'^\((\d{1,2})\)$|^\(\d\s*×\s*\d{1,2}\)$')
TRAILING_MARK = re.compile(r'\s\((\d{1,2})\)$')
# "Answer part A or part B." -- some text layers drop the space ("Aor").
CHOICE_AB = re.compile(r'Answer part A\s*or part B')
LETTER_ALT = re.compile(r'^\(([a-l])\)\s*([AB])$')
LEAD_MARKER = re.compile(r'^(\([a-l]\)|\((?:i|ii|iii|iv|v|vi|vii|viii|ix|x)\))\s+(.+)$')


def _split_markers(lines):
    """A line the PDF set as one run, "(c) (i) State Le Chatelier's principle.",
    read as its markers and its text, the way the page prints them."""
    alt_letter = None
    for l in lines:
        t = l.text
        both = LETTER_ALT.match(t)
        if both and l.x0 < 100:
            # The 2025 Higher scheme sets "(d)A" as one run, and "(d)B" again
            # for the second alternative of the same letter: the letter is
            # read once, at its first alternative.
            if both.group(1) != alt_letter:
                yield Line(l.page, (l.x0, l.y0, l.x1, l.y1), f'({both.group(1)})', l.bold, l.math)
            alt_letter = both.group(1)
            yield Line(l.page, (l.x0 + 20, l.y0, l.x1, l.y1), f'({both.group(2)})', l.bold, l.math)
            continue
        m = LEAD_MARKER.match(t)
        while m and l.x0 < 100:
            yield Line(l.page, (l.x0, l.y0, l.x1, l.y1), m.group(1), l.bold, l.math)
            t = m.group(2)
            m = LEAD_MARKER.match(t)
        tc = TRAILING_CELL.search(t)
        if tc and tc.start() > 0:
            # "pyramidal [12+10+(8×1)]": a mark cell the PDF set in the same
            # run as the answer before it.
            x0 = l.x0 + (28 if t != l.text else 0)
            split = x0 + (l.x1 - x0) * tc.start() / len(t)
            yield Line(l.page, (x0, l.y0, split, l.y1), t[:tc.start()], l.bold, l.math)
            yield Line(l.page, (max(split, 460), l.y0, l.x1, l.y1), tc.group(1).strip(), True)
            continue
        yield l if t == l.text else Line(l.page, (l.x0 + 28, l.y0, l.x1, l.y1), t, l.bold, l.math)


class Seg:
    """One printed part: everything from its marker up to the next marker."""
    __slots__ = ('key', 'marker', 'text', 'answers', 'tail')

    def __init__(self, key, marker):
        self.key, self.marker = key, marker
        self.text, self.answers, self.tail = [], [], []

    def __repr__(self):
        return f'<Seg {self.key} {self.marker!r}>'


def joined(lines):
    return tidy(' '.join(l.text for l in lines))


def segments(lines, first_q='1', answers=True, alt_letters=()):
    """Split printed lines into parts keyed (q, letter, roman, alt).

    The PAPER and the SCHEME number parts the same way, so one reader serves
    both; only the scheme has answers (its bold lines and mark cells). The
    letter (i) and the roman (i) are told apart by what came before: (i)
    follows (h) only where it sits at the letters' own indent. A bare A or B is
    an alternative only inside a part that says "Answer part A or part B"; the
    scheme brackets its alternatives "(A)".
    `alt_letters` names the (question, letter) pairs the PAPER sets as
    alternatives: the 2025 Ordinary scheme heads Q11(d)'s alternatives "A" and
    "B" without printing "(d)", so an A there opens the next letter.
    Returns (ordered list of Seg, {(q, letter, None, None): printed marks}).
    """
    segs, marks = [], {}
    q = letter = roman = alt = None
    letter_x = None
    cur = None
    lines = list(_split_markers(lines))
    # A row of worked arithmetic set wholly in the equation font, priced by a
    # cell at its right, is an answer row although nothing on it is bold. A
    # numerator printed above a bold answer line is not: it stays out.
    math_rows = set()
    if answers:
        for l in lines:
            if not l.math:
                continue
            row = [m for m in lines if m.page == l.page and abs(m.y0 - l.y0) <= 5.0]
            words = [m for m in row if m.bold and not MARK_CELL.match(m.text)
                     and m.text.strip('/ ')]
            if any(MARK_CELL.match(m.text) for m in row) and not words:
                math_rows.add(id(l))
    for l in lines:
        t = l.text
        if HEADER.match(t):
            continue
        if not answers and t == 'Acknowledgements':
            break                    # the paper's back page: credits and copyright
        m = QNUM.match(t)
        want = first_q if q is None else str(int(q) + 1)
        if m and l.x0 < 70 and m.group(1) == want \
                and (not answers or not l.bold or l.x0 < 40):
            q, letter, roman, alt = m.group(1), None, None, None
            cur = Seg((q, None, None, None), t)
            segs.append(cur)
            continue
        if q is None:
            continue
        am = ALTMARK.match(t)
        nxt_letter = chr(ord(letter or '`') + 1)
        if am and am.group(1) == 'A' and l.x0 < 100 and (q, letter) not in alt_letters \
                and (q, nxt_letter) in alt_letters:
            letter, roman, alt = nxt_letter, None, None
            segs.append(Seg((q, letter, None, None), f'({letter})'))
        if am and l.x0 < 150 and (t.startswith('(') or (q, letter) in alt_letters or any(
                CHOICE_AB.search(joined(sg.text))
                for sg in segs if sg.key[:2] == (q, letter))):
            alt, roman = am.group(1), None
            cur = Seg((q, letter, None, alt), t)
            segs.append(cur)
            continue
        # A bold letter at the left margin is still a part marker when it is
        # the next letter: the 2026 Ordinary scheme sets "(b)" of Q10 in bold.
        # A bold "(i)" there is an answer's own label (Q4's "(i) 27").
        nxt = LETTER.match(t)
        bold_letter = bool(answers and l.bold and nxt and l.x0 < 100 and not ROMAN.match(t)
                           and nxt.group(1) == chr(ord(letter or '`') + 1))
        if not (answers and l.bold) or bold_letter:
            pm = PAPER_MARK.match(t)
            # A part's mark sits at the right margin, or -- where a diagram
            # takes the right of the page -- at the end of the text column.
            if pm and (l.x0 > 400 or (not answers and l.x0 > 250)):
                if pm.group(1):
                    marks[(q, letter, None, None)] = int(pm.group(1))
                continue
            lm = LETTER.match(t)
            rm = ROMAN.match(t)
            is_letter = lm and (letter is None or lm.group(1) > letter) and (
                not rm or (letter == 'h' and letter_x is not None and abs(l.x0 - letter_x) < 4))
            if is_letter:
                letter, roman, alt, letter_x = lm.group(1), None, None, l.x0
                cur = Seg((q, letter, None, None), t)
                segs.append(cur)
                continue
            if rm:
                roman = rm.group(1)
                cur = Seg((q, letter, roman, alt), t)
                segs.append(cur)
                continue
        if answers and (l.bold or MARK_CELL.match(t) or (l.math and id(l) in math_rows)):
            cur.answers.append(l)
        elif answers and cur.answers:
            cur.tail.append(l)
        else:
            tm = TRAILING_MARK.search(t)
            if tm and not answers:
                marks[(q, letter, None, None)] = int(tm.group(1))
                l = Line(l.page, (l.x0, l.y0, l.x1, l.y1), t[:tm.start()], l.bold)
            cur.text.append(l)
    return segs, marks


# ── matching the paper's words to the scheme's reprint ──────────────────────
_FOLD = str.maketrans('⁰¹²³⁴⁵⁶⁷⁸⁹₀₁₂₃₄₅₆₇₈₉', '01234567890123456789')
_DASHES = str.maketrans('—–−⁻₋', '-----')


def norm(t):
    """The provenance gate's normalise(), in Python: case, scripts and
    punctuation folded away, and the Mathematical Alphanumeric block the SEC
    sets stacked fractions in ("𝟎.𝟏𝟎") read as the digits it is
    (scripts/markbank/schemeText.mjs). A guide while authoring; the build's
    own gate is the judge."""
    t = ''.join(unicodedata.normalize('NFKD', c) if 0x1D400 <= ord(c) <= 0x1D7FF else c
                for c in t)
    return re.sub(r'[^a-z0-9Ā-ſ]+', '', t.translate(_FOLD).lower())


def cut_to(text, target):
    """The shortest prefix of `text` whose normalised form is `target`'s.

    Returns (prefix, rest, exact). Where the reprint differs from the paper by
    a letter -- the paper prints "chorine", the scheme "chlorine" -- no prefix
    matches exactly; the cut then falls at the sentence end nearest the
    reprint's length and `exact` is False, for the caller to report.
    """
    want = norm(target)
    n, best = 0, None
    for i, ch in enumerate(text):
        n += len(norm(ch))
        if n == len(want) and norm(text[:i + 1]) == want:
            # Take the closing punctuation with it: the reprint's "flask." ends
            # where the paper's does, not one character short.
            j = i + 1
            while j < len(text) and not text[j].isspace() and text[j] != '(' \
                    and not norm(text[j]):
                j += 1
            return text[:j].strip(), text[j:].strip(), True
        if ch in '.?' and (best is None or abs(n - len(want)) < best[0]):
            best = (abs(n - len(want)), i)
    if best is None or best[0] > 4:
        return None, None, False
    i = best[1]
    return text[:i + 1].strip(), text[i + 1:].strip(), False


# What a diagram's label looks like when its text runs into the prose beside
# it: a number ("14", "(18)"), an orbital ("4p"), one capitalised word
# ("Energy"), or a letter or two ("X", "pH"). A formula, an arrow or a sign is
# never one -- dropping "HCl + NaOH → NaCl + H₂O" because the scheme sets the
# equation apart from its reprint of the lead-in would lose the equation.
LABEL = re.compile(r'^(\(?\d+(\.\d+)?\)?|\d[spdf]|[A-Z][a-z]{1,7}|[A-Za-z]{1,2})$')


def without_labels(text, target):
    """(ask, rest) when the paper's words, less some diagram labels, are
    exactly the reprint's; else None."""
    import difflib
    pw, want = text.split(), norm(target)
    sw = target.split()
    for j in range(1, len(pw) + 1):
        if len(norm(' '.join(pw[:j]))) < len(want):
            continue
        sm = difflib.SequenceMatcher(None, [norm(w) for w in pw[:j]], [norm(w) for w in sw],
                                     autojunk=False)
        drop, ok = set(), True
        for op, a1, a2, b1, b2 in sm.get_opcodes():
            if op == 'equal':
                continue
            if op == 'delete' and all(LABEL.match(w) for w in pw[a1:a2]):
                drop.update(range(a1, a2))
                continue
            ok = False
            break
        if not ok:
            continue
        kept = [w for i, w in enumerate(pw[:j]) if i not in drop]
        if norm(' '.join(kept)) == want:
            return ' '.join(kept), ' '.join(pw[j:])
    return None


def cut_at_tail(text, target, n=12):
    """(prefix, rest) of `text` ending where `target`'s last `n` normalised
    characters end in it, or (None, None)."""
    tail = norm(target)[-n:]
    if len(tail) < n:
        return None, None
    acc, end = '', None
    for i, ch in enumerate(text):
        acc += norm(ch)
        if acc.endswith(tail):
            end = i + 1
    if end is None:
        return None, None
    while end < len(text) and not text[end].isspace() and text[end] != '(' and not norm(text[end]):
        end += 1
    return text[:end].strip(), text[end:].strip()


# ── the scheme's answers ────────────────────────────────────────────────────
class PRow:
    """One printed row of a scheme answer: its words, mark cell and asides."""
    __slots__ = ('text', 'cell', 'asides', 'x1', 'page', 'y')

    def __init__(self, text, cell, asides, x1, page, y):
        self.text, self.cell, self.asides = text, cell, asides
        self.x1, self.page, self.y = x1, page, y

    def __repr__(self):
        return f'<PRow {self.text!r} {self.cell} {self.asides} x1={self.x1:.0f}>'


def prows(lines):
    """Answer lines grouped into the rows they print on, read left to right."""
    out, used = [], set()
    for l in lines:
        if id(l) in used:
            continue
        row = [m for m in lines if m.page == l.page and abs(m.y0 - l.y0) <= 5.0
               and id(m) not in used]
        for m in row:
            used.add(id(m))
        row.sort(key=lambda m: m.x0)
        words = [m for m in row if not MARK_CELL.match(m.text) and not ASIDE.match(m.text)]
        cell = next((m.text for m in row if MARK_CELL.match(m.text)), None)
        asides = [m.text for m in row if ASIDE.match(m.text)]
        out.append(PRow(tidy(' '.join(m.text for m in words)), cell, asides,
                        max((m.x1 for m in words), default=0.0), l.page, l.y0))
    return out


class Item:
    """The rows one mark cell closes."""
    __slots__ = ('rows', 'cell', 'asides')

    def __init__(self, rows, cell, asides):
        self.rows, self.cell, self.asides = rows, cell, asides

    @property
    def text(self):
        return tidy(' '.join(r.text for r in self.rows))

    def points(self, wrap_x=440):
        """The separately printed marking points in this item.

        A row ending "//" closes its point, as does a short row: the scheme sets
        each point on its own line. A row that runs on to the margin and has no
        "//" wraps into the next one.
        """
        pts, cur = [], []
        for r in self.rows:
            if not r.text:
                continue
            if not cur and pts and re.fullmatch(r'\([^()]*\)', r.text):
                # "(only)" on a row of its own qualifies the point above it.
                pts[-1] = tidy(pts[-1] + ' ' + r.text)
                continue
            cur.append(r.text)
            t = r.text.rstrip()
            # "ethyne is insoluble in water /" runs on: a single solidus at the
            # end of a row offers the next row as an alternative.
            if t.endswith('/') and not t.endswith('//'):
                continue
            if t.endswith('//') or r.x1 < wrap_x:
                pts.append(tidy(' '.join(cur)).rstrip('/ ').strip())
                cur = []
        if cur:
            pts.append(tidy(' '.join(cur)).rstrip('/ ').strip())
        return [p for p in pts if p]

    def options(self):
        """Every answer the scheme separates with //, across all its rows."""
        return [o.strip() for o in self.text.split('//') if o.strip()]

    def __repr__(self):
        return f'<Item {self.text!r} {self.cell} {self.asides}>'


def items_of(lines):
    rows, out, cur, asides = prows(lines), [], [], []
    for r in rows:
        if not r.text and r.asides and not r.cell and not cur and out:
            out[-1].asides.extend(r.asides)
            continue
        cur.append(r)
        asides.extend(r.asides)
        if r.cell:
            out.append(Item(cur, r.cell, asides))
            cur, asides = [], []
    if cur or asides:
        out.append(Item(cur, None, asides))
    return out


def mark_value(cell):
    """The total a mark cell prints: "[5+2]" -> 7, "[3 × 3]" -> 9, "[3×1 + 3]" -> 6."""
    body = cell.strip('[] ')
    total = 0
    for term in re.split(r'\s*\+\s*', body):
        f = [int(n) for n in re.split(r'\s*[×x]\s*', term.strip('() '))]
        total += f[0] * (f[1] if len(f) > 1 else 1)
    return total


def mark_terms(cell):
    """"[5+2]" -> [5, 2]; "[2×3]" -> [3, 3]; "[3×1 + 3]" -> [1, 1, 1, 3]."""
    out = []
    for term in re.split(r'\s*\+\s*', cell.strip('[] ')):
        f = [int(n) for n in re.split(r'\s*[×x]\s*', term.strip('() '))]
        out += [f[1]] * f[0] if len(f) > 1 else [f[0]]
    return out


# Script letters with no Unicode subscript form, and the raised "o" the papers
# set for a degree sign. Display only: the provenance gate folds both away.
# A state symbol read half as subscript ("H₂O₍g)") is set as the plain
# bracket it is, and a raised exponent with no Unicode form ("10^(-2.8)") as
# a caret.
_SUP = str.maketrans('0123456789', '⁰¹²³⁴⁵⁶⁷⁸⁹')
_SUB = str.maketrans('0123456789', '₀₁₂₃₄₅₆₇₈₉')
# Some papers (2025 Higher) set a negative charge or power with a raised em
# dash, which the text layer reads as "—": "MnO₄—", "A—", "10^(—14)",
# "mol^—1". It is the minus the page prints raised. A dash between two
# symbols ("the Cl—Cl bond") is a bond and stays.
DISPLAY = [(re.compile(r'\^(?:\([—–](\d+)\)|[—–](\d+)(?!\d|\.\d))'),
            lambda m: '⁻' + (m.group(1) or m.group(2)).translate(_SUP)),
           (re.compile(r'(?<=[A-Za-z₀-₉⁰-⁹⁺)*])—(?=[\s),.;:(]|$)'), '⁻'),
           # A subscript with a full stop set in its size: "NF_(3.)".
           (re.compile(r'_\((\d+)([.,])\)'), lambda m: m.group(1).translate(_SUB) + m.group(2)),
           (re.compile(r'_\(([a-zA-Z])\)'), r'\1'), (re.compile(r'\^\(o\)C'), '°C'),
           (re.compile(r'₍([a-z]{1,3})\)'), r'(\1)'), (re.compile(r'\^\(([^()\s]+)\)'), r'^\1'),
           # The text layer drops the space after a script run ("C₅H₁₂including",
           # "cm³portions"); the page prints one.
           (re.compile(r'([₀-₉⁰-⁹⁺⁻])([a-z]{2,})'), r'\1 \2'), (re.compile(r'\b(and)(\d)'), r'\1 \2')]


# The glyphs an SEC equation font maps into the wrong Unicode block ("ൌ" for
# "=", "ሺ" for "("). The repair is the bank's own (schemeText.mjs
# repairGlyphs), asked once per sitting for the characters it actually holds,
# never a second hand-made table.
BROKEN = re.compile(r'[\u0100-\u1FFF\uE000-\uF8FF\uFB00-\uFB4F]')
REPAIR = {}


def learn_repairs(texts):
    chars = sorted({c for t in texts for c in t if BROKEN.match(c)} - set(REPAIR))
    if not chars:
        return
    js = ("import(process.argv[1]).then(m => { const cs = JSON.parse(process.argv[2]);"
          " console.log(JSON.stringify(cs.map(c => m.repairGlyphs(c)))); })")
    url = 'file://' + os.path.join(ROOT, 'scripts', 'markbank', 'schemeText.mjs')
    out = subprocess.run(['node', '--input-type=module', '-e', js, url, json.dumps(chars)],
                         capture_output=True, text=True, check=True).stdout
    for c, r in zip(chars, json.loads(out)):
        REPAIR[c] = r


def display(t):
    t = ''.join(REPAIR.get(c, c) for c in t)
    t = ''.join(unicodedata.normalize('NFKD', c) if 0x1D400 <= ord(c) <= 0x1D7FF else c for c in t)
    # The equation font spaces a decimal point from its digits: "26. 55".
    t = re.sub(r'(\d)\. (\d)', r'\1.\2', t)
    for rx, rep in DISPLAY:
        t = rx.sub(rep, t)
    return tidy(t)


class Printed:
    """One sitting in the printed layout: its paper and its scheme, split into parts."""

    def __init__(self, year, lvl, figures=False):
        self.year, self.lvl = year, lvl
        self.paper_path = os.path.join(PAPERS, f'{year}-{lvl}-paper.pdf')
        self.scheme_path = os.path.join(SCHEMES, f'{year}-{lvl}.pdf')
        self.paper_lines = read_lines(self.paper_path)
        self.figures = figures
        if figures:
            self.paper_lines = self._outside_figures(self.paper_lines)
        self.scheme_lines = read_lines(self.scheme_path)
        # The 2021-2025 schemes print their mark cells in round brackets,
        # "(3)", at the same right margin the 2026 schemes print "[3]" at.
        # Read there, and only there, they are the same cell.
        lines = []
        for l in self.scheme_lines:
            if (l.x0 > 480 or l.bold) and ROUND_CELL.match(l.text):
                l.text = '[' + l.text.strip()[1:-1] + ']'
            elif l.bold and l.x0 < 480:
                # Where a diagram takes the right margin the scheme sets the
                # cell at the end of the answer itself: "occupy singly (3)".
                m = TRAILING_ROUND.search(l.text)
                if m and m.start() > 0:
                    lines.append(Line(l.page, (l.x0, l.y0, l.x1 - 20, l.y1), l.text[:m.start()],
                                      l.bold, l.math))
                    l = Line(l.page, (max(l.x1 - 20, 481), l.y0, l.x1, l.y1),
                             '[' + m.group(1).strip()[1:-1] + ']', True)
            lines.append(l)
        self.scheme_lines = lines
        self.pseg, self.marks = segments(self.paper_lines, answers=False)
        alt_letters = {s.key[:2] for s in self.pseg if s.key[3]}
        self.sseg, _ = segments(self.scheme_lines, answers=True, alt_letters=alt_letters)
        self.scheme_md = open(os.path.join(SCHEMES, f'{year}-{lvl}.md')).read()
        self.scheme_norm = norm(self.scheme_md)
        learn_repairs(l.text for l in self.paper_lines + self.scheme_lines)
        self.inexact = []

    def _outside_figures(self, lines):
        """The paper's lines less those printed inside a figure the card shows.

        A diagram's labels ("steam from a steam generator", a graph's axis
        numbers, "molten PbBr2") are part of its picture, not of the question's
        words; where the sitting's cropped paper figures cover them
        (chem_print_figures.CROPS), they are read as the picture's and left
        out of the asks and lead-ins. A part marker or a mark inside a crop
        means the rectangle is wrong, and stops the run."""
        from chem_print_figures import CROPS
        boxes = [(page, rect) for _n, src, page, rect in CROPS.get((self.year, self.lvl), [])
                 if src in ('paper', 'paper-image', 'labels')]
        kept = []
        for l in lines:
            inside = any(l.page == page and l.x0 >= r[0] - 1 and l.y0 >= r[1] - 1
                         and l.x1 <= r[2] + 1 and l.y1 <= r[3] + 1 for page, r in boxes)
            if not inside:
                kept.append(l)
            elif LETTER.match(l.text) or ROMAN.match(l.text) or PAPER_MARK.match(l.text) \
                    or (QNUM.match(l.text) and l.x0 < 70):
                raise ValueError(f'a figure crop covers the marker {l.text!r} on page {l.page}')
        return kept

    def rearranged(self, text, old, new):
        """`text` with `old` set as `new`, where `new` is the same printed
        characters in the order the page shows them -- a nuclide's mass and
        atomic numbers the text layer reads after its symbol ("Cr³⁺ 52 ion? 24"
        for the printed ⁵²₂₄Cr³⁺). Refused unless the characters are the same."""
        def chars(t):
            return sorted(re.sub(r'\s+', '', t.translate(_FOLD)).translate(_DASHES))
        if old not in text:
            raise ValueError(f'{old!r} is not in {text!r}')
        if chars(old) != chars(new):
            raise ValueError(f'{new!r} is not a rearrangement of {old!r}')
        return text.replace(old, new)

    # ── lookup ───────────────────────────────────────────────────────────
    def _one(self, segs, key, what):
        hits = [s for s in segs if s.key == key]
        if len(hits) != 1:
            raise KeyError(f'{what}: {len(hits)} parts keyed {key}')
        return hits[0]

    def pseg_of(self, key):
        return self._one(self.pseg, key, 'paper')

    def sseg_of(self, key):
        return self._one(self.sseg, key, 'scheme')

    @staticmethod
    def _below(segs, key):
        """The part `key` and every part printed under it."""
        q, letter, roman, alt = key
        out = []
        for s in segs:
            k = s.key
            if k[0] != q or (letter and k[1] != letter) or (roman and k[2] != roman) \
                    or (alt and k[3] != alt):
                continue
            out.append(s)
        return out

    # ── the paper ────────────────────────────────────────────────────────
    def _split(self, key):
        """(the paper's ask for this part, the lead-in it prints after it)."""
        p = joined(self.pseg_of(key).text)
        try:
            s = joined(self.sseg_of(key).text)
        except KeyError:
            s = ''
        if not s:
            return p, ''
        ask, rest, exact = cut_to(p, s)
        if not exact:
            # A diagram set beside the ask puts its labels into the ask's
            # lines ("Draw the shape of the atomic 4p orbital ... in a 3d
            # bromine atom"). Where dropping a few short words from the paper
            # leaves exactly the scheme's reprint, those words were the
            # diagram's, and the ask is the paper's own remaining words.
            got = without_labels(p, s)
            if got:
                ask, rest, exact = got[0], got[1], True
        if ask is None:
            # The reprint words the part differently ("Name two" for the
            # paper's "Identify two"): end the ask where the reprint's last
            # words fall in the paper.
            ask, rest = cut_at_tail(p, s)
            exact = False
        if ask is None and norm(s).startswith(norm(p)):
            # The scheme reprints a part's sub-parts inline ("Name the scientist
            # who determined (i) ..."); the paper sets them as parts of their own.
            return p, ''
        if ask is None:
            raise ValueError(f'{key}: the paper and the scheme reprint disagree\n  P: {p}\n  S: {s}')
        if not exact:
            self.inexact.append((key, ask, s))
        return ask, rest

    def ask(self, key, deep=False, upto=None):
        """The paper's words for a part. `deep` takes the parts printed under
        it too, with their markers -- a Q4 item asks "(i) ..., (ii) ..." in one."""
        if not deep:
            text = self._split(key)[0]
        else:
            parts = []
            for s in self._below(self.pseg, key):
                t = self._split(s.key)[0]
                parts.append(t if s.key == key else f'{s.marker} {t}')
            text = tidy(' '.join(parts))
        if upto is not None:
            text = text[:text.index(upto) + len(upto)]
        return display(text)

    def lead(self, key):
        """What the paper prints after a part's ask and before the next part.

        A diagram beside the asks leaves its labels here too ("4s", "Energy",
        a graph's axis numbers). Where the scheme reprints the lead-in, the
        paper's words are kept only as far as they are the reprint's (less
        such labels); where it does not, a run with no sentence in it is a
        diagram's labels and is no lead-in."""
        rest = self._split(key)[1]
        try:
            tail = joined(self.sseg_of(key).tail)
        except KeyError:
            tail = ''
        if rest and tail:
            got = without_labels(rest, tail)
            if got:
                return display(got[0])
        if rest and not self.figures and not re.search(r'[A-Za-z]{3,}[^.?:]*\b\w+[.?:]', rest):
            # Without the sitting's figure rectangles, a run with no sentence
            # in it is read as a diagram's labels. With them, the labels are
            # already gone and such a run is an equation the paper prints.
            return ''
        return display(rest)

    def text(self, key, upto=None, drop=()):
        """A part's own printed text (a question's or a letter's lead-in)."""
        t = joined(self.pseg_of(key).text)
        if upto is not None:
            t = t[:t.index(upto) + len(upto)]
        for d in drop:
            if d not in t:
                raise ValueError(f'{key}: {d!r} is not in its text')
            t = t.replace(d, ' ')
        return display(t)

    # ── the scheme ───────────────────────────────────────────────────────
    def items(self, key, deep=False):
        segs = self._below(self.sseg, key) if deep else [self.sseg_of(key)]
        return items_of([l for s in segs for l in s.answers])

    def traceable(self, claim):
        return norm(claim) in self.scheme_norm


__all__ = ['Printed', 'Item', 'PRow', 'segments', 'items_of', 'prows', 'joined', 'norm',
           'cut_to', 'display', 'mark_value', 'mark_terms', 'anyN', 'point', 'make_audit',
           'make_card', 'make_emit', 'tidy', 'MARK_CELL', 'ASIDE', 'ANY', 'WORDS', 'MAX_OPTIONS',
           'Line', 'Seg', 'read_lines']


# ── cards ───────────────────────────────────────────────────────────────────
# The commit the Chemistry audit started from: origin/main when the worktree
# was cut. Every pre-audit card is read from here, never from the working
# deck, so a re-run compares against the same thing every time.
AUDIT_BASE = 'e7ec7a532de3c03f8511d416cf943354dfe3e74e'
_PRIOR = None


def prior_deck():
    global _PRIOR
    if _PRIOR is None:
        raw = subprocess.run(['git', 'show', f'{AUDIT_BASE}:scripts/markbank/authored/chemistry.json'],
                             cwd=ROOT, capture_output=True, text=True, check=True).stdout
        _PRIOR = {c['id']: c for c in json.loads(raw)}
    return _PRIOR


def prior_card(cid):
    return prior_deck().get(cid)

INLINE_ASIDE = re.compile(r'\s*(\[[^\]]*[a-zA-Z]{3}[^\]]*\])')
ROMAN_ORDER = ['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x']


class Refused(Exception):
    pass


def _asides_note(asides):
    asides = [a for a in asides if not ANY.match(a)]
    return ('The scheme adds: ' + ' '.join(asides)) if asides else ''


class Cards:
    """The cards one printed sitting yields, and the parts it leaves open."""

    def __init__(self, P):
        self.P = P
        self.cards, self.open = [], []
        self.level = 'higher' if P.lvl == 'hl' else 'ordinary'
        self.prefix = f'chem-{P.year}-{P.lvl}-'
        self._card = make_card('chemistry')
        self._fixes_used = set()

    def _fixes_applied(self, keys, fixes):
        """A fix is keyed by the reader's own text; if the reader changes, a
        fix that no longer matches would silently stop applying. Refuse it."""
        unused = set(fixes or {}) - self._fixes_used
        self._fixes_used = set()
        if unused:
            raise Refused(f'{keys}: fixes matched nothing: {sorted(unused)}')

    # ── naming ───────────────────────────────────────────────────────────
    @staticmethod
    def label(key):
        q, letter, roman, alt = key
        return (f'({letter})' if letter else '') + (alt or '') + (f'({roman})' if roman else '')

    def ref(self, keys):
        first, last = keys[0], keys[-1]
        r = f'{self.P.year} {self.P.lvl.upper()} Q{first[0]}{self.label(first)}'
        if last != first:
            r += '–' + (f'({last[2]})' if last[:2] == first[:2] and last[3] == first[3]
                        else self.label(last))
        return r

    @staticmethod
    def slug(key):
        q, letter, roman, alt = key
        return '-'.join(p for p in (f'q{q}', letter, alt and alt.lower(), roman) if p)

    def cid(self, keys):
        c = self.slug(keys[0])
        if keys[-1] != keys[0]:
            c += '-' + (keys[-1][2] or self.slug(keys[-1]))
        return c

    # ── text ─────────────────────────────────────────────────────────────
    def context(self, key, heads=True):
        """The paper's lead-ins above a part: its question's, its letter's, its
        alternative's, and any the paper prints between earlier parts. An
        instruction ("Answer part A or part B.") is not context and is left out;
        so is anything the paper prints after a lead-in's last sentence that the
        scheme does not reprint -- a diagram's labels."""
        P = self.P
        q, letter, roman, alt = key
        above = [(q, None, None, None)]
        if letter and (roman or alt):
            above.append((q, letter, None, None))
        if alt and roman:
            above.append((q, letter, None, alt))
        out = []
        for k in (above if heads else []):
            try:
                t = P.ask(k)
            except KeyError:
                continue
            if t and not t.startswith('Answer '):
                out.append(t)
            # What the paper prints after a lead-in and before the first part
            # under it -- an equation the scheme sets in bold, so its reprint
            # ends at "the following balanced chemical equation:" -- is the
            # lead-in's still.
            lead = P.lead(k) if k != key else ''
            if lead and lead != 'or':
                out.append(lead)
        if roman:
            for r in ROMAN_ORDER[:ROMAN_ORDER.index(roman)]:
                try:
                    lead = P.lead((q, letter, r, alt))
                except KeyError:
                    continue
                if lead and lead != 'or':
                    out.append(lead)
        return tidy(' '.join(out))

    def qtext(self, keys, deep=False):
        """One part's ask, or several parts' asks with their printed markers
        and any lead-in the paper sets between them."""
        if len(keys) == 1:
            return self.P.ask(keys[0], deep=deep)
        out = []
        for i, k in enumerate(keys):
            out.append(f'({k[2]}) {self.P.ask(k)}')
            lead = self.P.lead(k) if i < len(keys) - 1 else ''
            if lead and lead != 'or':
                out.append(lead)
        return tidy(' '.join(out))

    # ── rows ─────────────────────────────────────────────────────────────
    def _verbatim(self, text, fixes, where):
        notes = INLINE_ASIDE.findall(text)
        text = tidy(INLINE_ASIDE.sub('', text))
        for k in (text, display(text)):
            if k in fixes:
                self._fixes_used.add(k)
                text = fixes[k]
                break
        shown = display(text)
        if self.P.traceable(shown):
            text = shown
        if not self.P.traceable(text):
            raise Refused(f'{where}: "{text}" is not in the {self.P.year} {self.P.lvl} scheme')
        return text, notes

    def points(self, key, fixes=None, notes=None, deep=False, skip=()):
        """One fixed row per mark cell, worth what the cell prints. An item in
        `skip` is a line the scheme sets among the answers that answers
        nothing -- a reprint of the paper's next equation -- and is left out."""
        fixes, notes = fixes or {}, notes or {}
        rows, skipped = [], set()
        for it in self.P.items(key, deep=deep):
            if it.cell is None and display(it.text) in skip:
                skipped.add(display(it.text))
                continue
            if it.cell is None and rows and re.fullmatch(r'\[[^\[\]]*(\[[^\]]*\][^\[\]]*)*\]', it.text):
                # A bracketed line under the last cell: the scheme's own
                # aside, such as the whole balanced equation after its parts.
                rows[-1]['contextNote'] = tidy(rows[-1].get('contextNote', '') +
                                               ' The scheme adds: ' + it.text)
                continue
            if it.cell is None:
                raise Refused(f'{key}: "{it.text}" has no mark cell of its own')
            if '+' in it.cell and not re.search(r'×', it.cell):
                raise Refused(f'{key}: {it.cell} is a split, not a fixed point')
            text, inline = self._verbatim(it.text, fixes, key)
            note = ' '.join(x for x in [_asides_note(inline + it.asides),
                                        f'The scheme prices this point {it.cell}.'
                                        if mark_value(it.cell) != mark_terms(it.cell)[0] else '',
                                        notes.get(len(rows), '')] if x)
            rows.append(point(f'r-{len(rows) + 1}', text, mark_value(it.cell), note))
        if set(skip) - skipped:
            raise Refused(f'{key}: nothing to skip for {sorted(set(skip) - skipped)}')
        return rows

    def split(self, keys, fixes=None, notes=None, drawn=(), drop=(), criteria=()):
        """Points the scheme prices together ("[6+2+2+2]"): one null row each,
        a choice among them as one null anyN group. Returns (rows, cell).

        A part in `drawn` is one the scheme answers with a drawing: its row is
        the paper's own ask, and whatever words the scheme prints beside the
        drawing ride on that row's note."""
        fixes, notes = fixes or {}, notes or {}
        rows, cells, asides_all, dropped = [], [], [], set()
        for key in keys:
            if key in drawn:
                its = self.P.items(key)
                cells += [it.cell for it in its if it.cell]
                said = [display(it.text) for it in its if it.text] + [a for it in its for a in it.asides]
                ask = self.drawn_ask(key)
                rows.append(point(f'r-{len(rows) + 1}', ask, None, ' '.join(x for x in [
                    f'The scheme answers ({key[2]}) with a drawing; its own print is shown with '
                    f'the answer.', ('It adds: ' + ' '.join(said)) if said else '',
                    notes.get(len(rows), '')] if x)))
                continue
            for it in self.P.items(key):
                if it.cell:
                    cells.append(it.cell)
                anyk = next((WORDS[ANY.match(a).group(1).lower()] for a in it.asides if ANY.match(a)), None)
                inline_notes = []
                if anyk:
                    opts = []
                    for o in it.options():
                        t, inl = self._verbatim(o, fixes, key)
                        opts.append(t)
                        inline_notes += inl
                    r = {'id': f'r-{len(rows) + 1}', 'kind': 'anyN', 'verbatim': opts[0],
                         'marks': None, 'openList': True,
                         'contextNote': ' '.join(x for x in [f'Any {anyk} of these.',
                                                             _asides_note(inline_notes + it.asides),
                                                             notes.get(len(rows), '')] if x),
                         'group': {'claimMax': anyk, 'options': opts}}
                    rows.append(r)
                    continue
                pts = it.points()
                for crit in criteria:
                    # An instruction to the examiner ("any correct example"),
                    # not an answer: it goes on the card's notes, where it
                    # still tells the student what earns the mark.
                    if display(crit) in [display(x) for x in pts]:
                        pts = [x for x in pts if display(x) != display(crit)]
                        self._criteria.append(f'For ({key[2] or key[1]}) the scheme prints only '
                                              f'the criterion "{display(crit)}".')
                        dropped.add(crit)
                for d in drop:
                    if display(d) in [display(x) for x in pts]:
                        pts = [x for x in pts if display(x) != display(d)]
                        dropped.add(d)
                for j, ptext in enumerate(pts):
                    t, inl = self._verbatim(ptext, fixes, key)
                    note = ' '.join(x for x in [_asides_note(inl + (it.asides if j == len(pts) - 1 else [])),
                                                notes.get(len(rows), '')] if x)
                    r = point(f'r-{len(rows) + 1}', t, None, note)
                    rows.append(r)
        if (set(drop) | set(criteria)) - dropped:
            raise Refused(f'{keys}: nothing to drop for {sorted((set(drop) | set(criteria)) - dropped)}')
        if len(cells) != 1:
            raise Refused(f'{keys}: {len(cells)} mark cells across a split ({cells})')
        return rows, cells[0]

    def anyn(self, key, claim=None, fixes=None, note=''):
        """A printed menu the student picks from: one anyN row."""
        fixes = fixes or {}
        its = self.P.items(key)
        if len(its) != 1:
            raise Refused(f'{key}: {len(its)} items where one menu was expected')
        it = its[0]
        anyk = next((WORDS[ANY.match(a).group(1).lower()] for a in it.asides if ANY.match(a)), None)
        claim = claim or anyk
        if not claim:
            raise Refused(f'{key}: no claim limit printed or given')
        opts, inl = [], []
        for o in it.options():
            t, i = self._verbatim(o, fixes, key)
            opts.append(t)
            inl += i
        terms = mark_terms(it.cell)
        if len(terms) != claim:
            raise Refused(f'{key}: {it.cell} prices {len(terms)} answers, the student claims {claim}')
        steps = terms if len(set(terms)) > 1 else None
        nt = ' '.join(x for x in [_asides_note(inl + it.asides), note] if x)
        return [anyN('r-1', opts[0], sum(terms), claim, terms[0], opts, nt, steps=steps)], sum(terms)

    # ── cards ────────────────────────────────────────────────────────────
    def add(self, keys, topic, concept, rows, *, kind='fixed', notation=None, total=None,
            stem=None, notes='', figure='', deep=False, qtext=None, cid=None, label_key=None,
            ref_suffix=None):
        keys = [tuple(k) for k in keys]
        if total is None:
            total = sum(r['marks'] for r in rows) if kind == 'fixed' and not any(
                r['kind'] == 'anyN' for r in rows) else None
            if total is None:
                raise Refused(f'{keys}: give the total')
        q = int(keys[0][0])
        if stem is None:
            stem = self.context(keys[0])
        full = self.prefix + (cid or self.cid(keys))
        if topic is None or concept is None:
            # A card corrected in place keeps the syllabus filing and concept
            # its pre-audit version carried, unless the audit gives new ones.
            before = prior_card(full)
            if not before:
                raise Refused(f'{full}: no pre-audit card to inherit a topic or concept from')
            topic = topic or before['topicId']
            concept = concept or before['conceptId']
        # Two cards on one printed part -- a calculation whose steps outrun a
        # card's rows -- each name the part and which of its steps they hold
        # ("2025 HL Q10(c)(i) — steps 1–5"): the build keeps one card per
        # citation, and the reconciler reads only what precedes the " — ".
        ref = self.ref(keys) + (f' — {ref_suffix}' if ref_suffix else '')
        c = self._card(full, self.P.year, self.level, topic,
                       concept, ref, qtext or self.qtext(keys, deep=deep),
                       notation or '', total, rows, notes, stem=stem,
                       tariff_kind=kind, section='A' if q <= 3 else 'B', figure_key=figure,
                       label_key=label_key)
        if kind == 'orderedSplit':
            c['tariffModel'] = {'kind': 'orderedSplit', 'notation': notation}
        elif kind == 'fixed':
            c['tariffModel'] = {'kind': 'fixed'}
        c['keys'] = keys
        self.cards.append(c)
        return c

    def fixed(self, keys, topic, concept, **kw):
        fixes, notes, deep = kw.pop('fixes', None), kw.pop('row_notes', None), kw.get('deep', False)
        skip = kw.pop('skip', ())
        rows = []
        self._fixes_used = set()
        for k in keys:
            rows += self.points(tuple(k), fixes, notes, deep=deep, skip=skip)
        self._fixes_applied(keys, fixes)
        for i, r in enumerate(rows):
            r['id'] = f'r-{i + 1}'
        return self.add(keys, topic, concept, rows, **kw)

    def ordered(self, keys, topic, concept, **kw):
        self._criteria = []
        self._fixes_used = set()
        fixes = kw.pop('fixes', None)
        rows, cell = self.split([tuple(k) for k in keys], fixes,
                                kw.pop('row_notes', None), drawn=kw.pop('drawn', ()),
                                drop=kw.pop('drop', ()), criteria=kw.pop('criteria', ()))
        self._fixes_applied(keys, fixes)
        note = (f'The scheme prices these points together as {cell} without saying which '
                f'point earns which part, so no per-point value is shown.')
        kw['notes'] = tidy(' '.join([note] + self._criteria + [kw.get('notes', '')]))
        return self.add(keys, topic, concept, rows, kind='orderedSplit', notation=cell,
                        total=mark_value(cell), **kw)

    def priced_menu(self, keys, topic, concept, claim, options, **kw):
        """A choice the scheme prices as a whole ("[6]" for any two of five)
        without a value per option: one null anyN row, and the question's
        total as the only number (questionTotal)."""
        opts = []
        for o in options:
            if not self.P.traceable(o):
                raise Refused(f'{keys}: "{o}" is not in the scheme')
            opts.append(o)
        its = self.P.items(tuple(keys[0]))
        cells = [it.cell for it in its if it.cell]
        if len(cells) != 1:
            raise Refused(f'{keys}: {len(cells)} cells for a priced menu')
        note = kw.pop('note', '')
        row = {'id': 'r-1', 'kind': 'anyN', 'verbatim': opts[0], 'marks': None, 'openList': True,
               'contextNote': tidy(f'Any {claim} of these. ' + note),
               'group': {'claimMax': claim, 'options': opts}}
        c = self.add(keys, topic, concept, [row], kind='questionTotal',
                     total=mark_value(cells[0]), **kw)
        c['tariffModel'] = {'kind': 'questionTotal'}
        return c

    def menu(self, keys, topic, concept, claim=None, **kw):
        self._fixes_used = set()
        fixes = kw.pop('fixes', None)
        rows, total = self.anyn(tuple(keys[0]), claim, fixes, kw.pop('note', ''))
        self._fixes_applied(keys, fixes)
        return self.add(keys, topic, concept, rows, total=total, **kw)

    def drawn_ask(self, key):
        """The marking point for a drawn answer: the paper's ask, or -- where
        the scheme reprints it in other words -- the scheme's own reprint."""
        ask = self.P.ask(key)
        if self.P.traceable(ask):
            return ask
        reprint = display(joined(self.P.sseg_of(key).text))
        if not self.P.traceable(reprint):
            raise Refused(f'{key}: neither the ask nor its reprint is in the scheme')
        return reprint

    def drawn(self, keys, topic, concept, figure, **kw):
        """A part the scheme answers with a DRAWING and no words.

        The marking point is the part itself -- the paper's ask, which the
        scheme reprints, so the provenance gate finds it -- and the answer is
        the scheme's own drawing, cropped and published as a solution figure
        the session holds back until the student has committed. The mark is
        what the part's cells print, summed, with the cells quoted."""
        key = tuple(keys[0])
        its = self.P.items(key)
        cells = [it.cell for it in its if it.cell]
        if not cells:
            raise Refused(f'{key}: no mark cell for a drawn answer')
        asides = [a for it in its for a in it.asides]
        ask = self.drawn_ask(key)
        total = sum(mark_value(c) for c in cells)
        note = ' '.join(x for x in [
            "The scheme answers this part with a drawing or notation its text cannot carry; "
            "its own print is shown with the answer.",
            f"It prices the part {' and '.join(cells)}." if len(cells) > 1 or mark_value(cells[0]) != mark_terms(cells[0])[0] else '',
            _asides_note(asides)] if x)
        return self.add([key], topic, concept, [point('r-1', ask, total, note)], total=total,
                        figure=figure, **kw)

    def lifted(self, rid, text, marks, note=''):
        """A row whose text the reader could not assemble on its own (a line
        set wholly as fractions), given in the one form the provenance gate
        finds in the scheme. Refused if the gate would not find it."""
        if not self.P.traceable(text):
            raise Refused(f'"{text}" is not in the {self.P.year} {self.P.lvl} scheme')
        return point(rid, text, marks, note)

    def leave_open(self, keys, reason):
        self.open.append((self.ref([tuple(k) for k in keys]), reason))

    # ── checks ───────────────────────────────────────────────────────────
    def letter_totals(self):
        """Every letter's cards against the paper's printed mark for it."""
        got = {}
        for c in self.cards:
            k = c['keys'][0]
            got.setdefault((k[0], k[1], None, None), 0)
            got[(k[0], k[1], None, None)] += c['totalMarks']
        return {k: (got.get(k), v) for k, v in self.P.marks.items() if k[1]}

    def finish(self):
        for c in self.cards:
            c.pop('keys', None)
        return self.cards
