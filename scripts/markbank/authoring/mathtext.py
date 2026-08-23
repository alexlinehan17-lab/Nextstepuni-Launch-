#!/usr/bin/env python3
"""Read a Mathematics marking scheme without the notation turning to mush.

    python3 scripts/markbank/authoring/mathtext.py <scheme.pdf> <page>

WHY THIS EXISTS, and what it decided about the subject.

A Maths scheme extracts as "𝑥𝑥−3 ≤12" with a Sinhala letter where the square
root should be, which is why the subject was written off at Stage 0. That was
half right. The mangling is a deterministic FONT fault, not lost information:
CambriaMath emits each italic variable twice and its ToUnicode map lands several
glyphs in the wrong Unicode block. Both are reversible.

More important, the page is TWO COLUMNS and only one of them is affected:

    Model Solution - 30 Marks        |  Marking Notes
    ∫e^5x dx = [1/5 e^5x]            |  Scale 15D (0, 4, 7, 10, 15)
    ...                              |  Step 1. Integrates e^5x
                                     |  Step 2. Substitutes in limits
                                     |  Step 3. Isolates e^5k
                                     |  Step 4. Finds k

The Marking Notes are near-plain English and, once demangled, come out clean.
They are also the better answer for a card: a student loses marks by missing a
STEP, not by failing to reproduce a typeset solution. The model solution is
structurally scrambled by extraction -- fractions and limits flatten, lines
reorder -- so it belongs on a card as a cropped IMAGE, not as text.

One paper carries 179 numbered marking steps and 85 partial-credit scales.

Two things to get right, both learned by getting them wrong:
  * Collapse the doubled letters ONLY among maths glyphs, and BEFORE mapping
    them to ASCII. Done after, it turns "correct" into "corect" and "Full" into
    "Ful".
  * Superscripts are a smaller span on a raised baseline, not a character.
    Ignore that and "e^5x" reads as "e5x".
"""
import re
import sys
import unicodedata

MATH_LO, MATH_HI = 0x1D400, 0x1D7FF
DIGITS = {'ZERO': '0', 'ONE': '1', 'TWO': '2', 'THREE': '3', 'FOUR': '4',
          'FIVE': '5', 'SIX': '6', 'SEVEN': '7', 'EIGHT': '8', 'NINE': '9'}
# Glyphs whose ToUnicode map put them in the wrong block entirely.
# A second font subset, used from 2023, maps its digits into the Oriya block in
# a contiguous run and its brackets into Ethiopic. Verified by reading the
# results back: "m^ଶ−4ሺ3ሻሺ3ሻ= 0" becomes "m²−4(3)(3) = 0", which is the
# discriminant it plainly is, and "(ସିଶ)" becomes "(4−2)".
GLYPH = {chr(0x0B34 + i): str(i) for i in range(10)}
GLYPH.update({'\u0b3e': '+', '\u0b3f': '−',
              'ሺ': '(', 'ሻ': ')', 'ቀ': '(', 'ቁ': ')'})
GLYPH.update({'න': '∫', '൤': '[', '൨': ']', 'ൣ': '[', '൧': ']',
              '൬': '(', '൰': ')', 'ඈ': '{', 'ඉ': '}', '൫': '(', '൯': ')',
              '൛': '(', 'ඌ': '|',
              'ඥ': '√', 'ඩ': '√', 'ℎ': 'h', '': ''})


def _is_math(ch):
    return MATH_LO <= ord(ch) <= MATH_HI


def _plain(ch):
    try:
        name = unicodedata.name(ch)
    except ValueError:
        return ch
    # "MATHEMATICAL ITALIC SMALL E" -- note there is no "LETTER" in the name.
    m = re.search(r'(?:SMALL|CAPITAL)\s+([A-Z])$', name)
    if m:
        return m.group(1).lower() if 'SMALL' in name else m.group(1)
    m = re.search(r'DIGIT\s+([A-Z]+)$', name)
    if m:
        return DIGITS.get(m.group(1), ch)
    return ch


def demangle(text):
    """Plain text for a run extracted from a Maths scheme."""
    out = []
    for ch in text:
        if out and ch == out[-1] and _is_math(ch):
            continue
        out.append(ch)
    return ''.join(_plain(c) if _is_math(c) else GLYPH.get(c, c) for c in out)


def line_text(line):
    """One line of a scheme page, with superscripts marked.

    A superscript is a span set smaller than its neighbours and sitting higher.
    Without this "Integrates e^5x" reads as "Integrates e5x", which is a
    different claim about the maths.
    """
    spans = [s for s in line['spans'] if s['text'].strip() or s['text'] == ' ']
    if not spans:
        return ''
    base = max(s['size'] for s in spans)
    out = []
    for i, s in enumerate(spans):
        t = demangle(s['text'])
        # Compared against the span it FOLLOWS, not the smallest baseline on the
        # line. A line mixes fonts -- Calibri prose sits higher than the
        # CambriaMath variable beside it -- so a line-wide minimum said the
        # exponent was not raised and "Integrates e^(5x)" read as "e5x".
        prev = spans[i - 1] if i else None
        raised = (s['size'] < base - 1.5 and prev is not None
                  and s['bbox'][1] < prev['bbox'][1] - 0.8)
        out.append(f'^({t.strip()})' if raised and t.strip() else t)
    return spacing(superscripts(''.join(out).strip()))


def placed(page, cut=300):
    """([(y, text)] left, [(y, text)] right) — columns WITH their positions.

    A Maths scheme page is a table, and one page frequently holds several
    parts: 25 of the 61 marked pages of the 2025 Higher scheme carry more than
    one part marker. Dropping the y coordinate collapses those into a single
    part and loses the rest, so the position is kept and the caller segments on
    it.
    """
    left, right = [], []
    for b in page.get_text('dict')['blocks']:
        for ln in b.get('lines', []):
            t = line_text(ln)
            if not t:
                continue
            x = min(s['bbox'][0] for s in ln['spans'])
            y = min(s['bbox'][1] for s in ln['spans'])
            (right if x >= cut else left).append((y, t))
    return sorted(left), sorted(right)


def columns(page, cut=300):
    """(model solution lines, marking-notes lines) for one scheme page."""
    left, right = placed(page, cut)
    return ([t for _, t in left], [t for _, t in right])


SCALE = re.compile(r'Scale\s+(\d+)([A-Z]?)\s*\(([\d,\s]+)\)')
STEP = re.compile(r'^Step\s+(\d+)\.\s*(.+)$')


def steps_and_scale(notes):
    """The marking steps and the partial-credit ladder — a card's answer."""
    steps = [(int(m.group(1)), m.group(2).strip())
             for line in notes if (m := STEP.match(line))]
    scale = next((m for line in notes if (m := SCALE.search(line))), None)
    ladder = ([int(v) for v in scale.group(3).split(',') if v.strip().isdigit()]
               if scale else None)
    return steps, (int(scale.group(1)) if scale else None), ladder


if __name__ == '__main__':
    import pymupdf
    doc = pymupdf.open(sys.argv[1])
    page = doc[int(sys.argv[2])]
    sol, notes = columns(page)
    steps, total, ladder = steps_and_scale(notes)
    print(f'tariff: {total} marks, ladder {ladder}')
    print('steps:')
    for n, t in steps:
        print(f'   {n}. {t}')
    print('\nmodel solution (belongs on the card as an image):')
    for l in sol[:8]:
        print(f'   {l[:70]}')


_DOCCACHE = {}


def clean_document(paths):
    """[(clean line, plain line)] for every line of the paper, in order.

    Kept as PARALLEL lines, not two joined strings. The search has to run over
    the PLAIN text -- that is what paper.py handed us -- while what comes back
    has to be the CLEAN text. Indexing the clean side instead loses exactly the
    characters the repair introduced: "4x³" squashes to "4x" where the plain
    "4x3" squashes to "4x3", so no fragment with an exponent could ever match.
    """
    import pymupdf
    key = tuple(paths)
    if key in _DOCCACHE:
        return _DOCCACHE[key]
    rows = []
    for path in paths:
        with pymupdf.open(path) as doc:
            for page in doc:
                for b in page.get_text('dict')['blocks']:
                    for ln in b.get('lines', []):
                        plain = ''.join(sp['text'] for sp in ln['spans'])
                        if plain.strip():
                            rows.append((line_text(ln), plain))
    _DOCCACHE[key] = rows
    return rows


def _squash(t):
    return re.sub(r'[^a-z0-9]+', '', (t or '').lower())


def clean_like(paths, fragment):
    """The span-aware form of `fragment` as paper.py extracted it.

    Returns the fragment merely demangled when it cannot be located -- better a
    readable line than none, though it will be missing its exponents.
    """
    rows = clean_document(paths)
    want = _squash(demangle(fragment))
    if len(want) < 12:
        return demangle(fragment)
    hay, owner = [], []
    for i, (_, plain) in enumerate(rows):
        sq = _squash(demangle(plain))
        hay.append(sq)
        owner.extend([i] * len(sq))
    hay = ''.join(hay)
    # The floor has to be below len(want), or the range is EMPTY and the match
    # never runs: a 34-character fragment against a floor of 40 gave range(34,
    # 39, -10), no iterations, and a silent fallback to the unrepaired text.
    at, floor = -1, min(40, len(want)) - 1
    for n in range(min(len(want), 200), floor, -10):
        at = hay.find(want[:n])
        if at >= 0:
            break
    if at < 0:
        return demangle(fragment)
    end = min(at + len(want), len(owner)) - 1
    lines = rows[owner[at]:owner[end] + 1]
    return spacing(' '.join(' '.join(c for c, _ in lines).split()))


SUP = {'0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴', '5': '⁵',
       '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹', '+': '⁺', '-': '⁻',
       'n': 'ⁿ', 'i': 'ⁱ', '(': '⁽', ')': '⁾'}


OPERATOR = re.compile(r'(?<=[A-Za-z0-9)\]|²³⁴⁵⁶⁷⁸⁹¹⁰])\s*([=+×÷≤≥<>≠])\s*')


def spacing(text):
    """Put the space back on both sides of an operator.

    The PDF kerns these so the space lands after the operator and not before:
    "x= 0", "2x+ 3", "0 <x<4". On a card that reads as a typo, and it is the
    first thing anyone notices.

    Deliberately does NOT touch the minus sign. In this notation "−" is as often
    a negation as a subtraction -- "e5k−1", "f(−2)" -- and spacing it wrongly
    would be worse than leaving it.
    """
    out = OPERATOR.sub(lambda m: f' {m.group(1)} ', text or '')
    return re.sub(r'\s{2,}', ' ', out).strip()


def superscripts(text):
    """Render "^(2)" as "²" where every character has a superscript form.

    A card shows this to a student, so "4x²" is worth having over "4x^(2)".
    Anything without a real superscript glyph -- "^(5x)" -- keeps the caret
    form rather than being flattened, because flattening changes the maths.
    """
    def one(m):
        body = m.group(1)
        if body and all(c in SUP for c in body):
            return ''.join(SUP[c] for c in body)
        return f'^({body})' if len(body) > 1 else f'^{body}'
    return re.sub(r'\^\(([^)]*)\)', one, text)
