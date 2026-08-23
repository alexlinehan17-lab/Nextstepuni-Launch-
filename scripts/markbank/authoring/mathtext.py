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
import json
import os
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
GLYPH.update({'\u0b3e': '+', '\u0b3f': '−', 'ᇱ': '′', '\u11f1': '′',
              'ሺ': '(', 'ሻ': ')', 'ቀ': '(', 'ቁ': ')'})
# Nine glyphs the derivation below cannot reach, kept as a fallback.
GLYPH.update({'ඈ': '{', 'ඉ': '}', '൛': '(', 'ඌ': '|', 'ൣ': '[', '൧': ']',
              'ඥ': '√', 'ඩ': '√', 'ℎ': 'h', '': '•'})

# The rest of the table is derived from the schemes, not written here. Hand
# mapping did not converge -- ten Maths schemes alone printed 147 distinct
# broken glyphs, and a wrong guess quietly changes what a marking point says.
# derive_glyphs.py reads each glyph's id, which is reliable where the PDF's
# ToUnicode map is not, and learns the character from the schemes that happen
# to spell it correctly. It reproduces every entry written by hand above and
# adds ninety more. Re-derive with:
#     python3 scripts/markbank/authoring/derive_glyphs.py --write
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       'glyphmap.json'), encoding='utf-8') as _fh:
    GLYPH.update(json.load(_fh))


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
    # Glyph map first, plain letters second. The other order leaves anything
    # the map resolves TO a maths-italic letter untouched, so the x of dy/dx
    # arrived repaired but still unreadable.
    mapped = ''.join(GLYPH.get(c, c) for c in out)
    return ''.join(_plain(c) if _is_math(c) else c for c in mapped)


def unreadable(text):
    """The glyphs in `text` that no font table resolved, if any.

    Greek is genuinely Greek in these schemes, and the two combining marks
    carry p-hat and z-bar; everything else left in these blocks is a subset
    font's wreckage and must not reach a reader.
    """
    return sorted({c for c in text
                   if (0x0100 <= ord(c) < 0x2000 or 0xE000 <= ord(c) < 0xF900
                       or 0xFB00 <= ord(c) < 0xFB50)
                   and not 0x0370 <= ord(c) < 0x0400
                   and ord(c) not in (0x0302, 0x0305)})


def line_text(line):
    """One line of a scheme page, with superscripts marked.

    A superscript is a span set smaller than its neighbours and sitting higher.
    Without this "Integrates e^5x" reads as "Integrates e5x", which is a
    different claim about the maths.
    """
    spans = [s for s in line['spans'] if s['text'].strip() or s['text'] == ' ']
    if not spans:
        return ''
    # The DOMINANT size, weighted by how much text is set in it -- not the
    # largest. A line whose bullet is 12pt and whose body is 8.5pt has a
    # maximum of 12, which made the entire body "raised": the marking point
    # "4 - 2i = -4k + 2ki" came back as one giant exponent.
    weight = {}
    for s_ in spans:
        weight[s_['size']] = weight.get(s_['size'], 0) + len(s_['text'].strip())
    base = max(weight, key=lambda k: (weight[k], k)) if any(weight.values()) \
        else max(s_['size'] for s_ in spans)
    out = []
    for i, s in enumerate(spans):
        t = demangle(s['text'])
        # Compared against the span it FOLLOWS, not the smallest baseline on the
        # line. A line mixes fonts -- Calibri prose sits higher than the
        # CambriaMath variable beside it -- so a line-wide minimum said the
        # exponent was not raised and "Integrates e^(5x)" read as "e5x".
        prev = spans[i - 1] if i else None
        # Smaller by 1.5 or more, not strictly more than 1.5: the cosine rule
        # in 2021 HL Paper 2 Q7(c) sets its exponents at 9pt against a 10.5pt
        # base, exactly 1.5 apart, and "28^2 + 4^2 - 30^2" shipped as
        # "282 + 42-302".
        # A superscript is a smaller span that is NOT lower than the one it
        # follows. Demanding it be 0.8pt higher missed this font, which raises
        # its exponents by 0.59: "−2(x²−2x−3)" came out "−2(x2−2x−3)", which is
        # a different expression. A subscript sits LOWER and is still excluded.
        raised = (s['size'] <= base - 1.5 and prev is not None
                  and s['bbox'][1] <= prev['bbox'][1] + 0.2)
        # An exponent is short. Prose set a size smaller than the body -- an
        # examiner's aside, a footnote -- is not an exponent, and wrapping it
        # turned "In a C scale where" into "^(C scale)^(where)".
        # The other direction: a smaller span sitting LOWER is a subscript. It
        # was excluded outright, which spelled a logarithm's base into the
        # number beside it -- "log_3 7" came out "log37".
        lowered = (s['size'] <= base - 1.5 and prev is not None
                   and s['bbox'][1] > prev['bbox'][1] + 0.2)
        body = t.strip()
        if len(body) > 8 or re.search(r'[A-Za-z]{2,}', body):
            raised = lowered = False
        # The space around the span belongs to the line, not to the exponent.
        # Stripping it into the wrapper closed a gap the scheme prints:
        # "Tn = p" came out "T_n= p".
        lead, trail = t[:len(t) - len(t.lstrip())], t[len(t.rstrip()):]
        if raised and body:
            out.append(f'{lead}^({body}){trail}')
        elif lowered and body:
            out.append(f'{lead}_({body}){trail}')
        else:
            out.append(t)
    return spacing(subscripts(superscripts(''.join(out).strip())))


# A stacked fraction is three objects -- a numerator, a drawn rule and a
# denominator -- so reading a page line by line splits one expression across
# two of them. In the Maths schemes that broke marking points in half:
# "r(2) = 10 + 1.5 + sin(pi/5) + 1.5 + sin(2pi/5)" arrived as "r(2) = 10 + 1.5
# + sin" with "5 + 1.5 + sin" offered underneath as a separate answer. The
# geometry is append-scheme-fractions.py's, which has read these bars across
# seven subjects; what differs is the answer, which is the text AND the band it
# occupies, so placed() can drop the lines it consumed.
BAR_MAX_HEIGHT, BAR_MIN_WIDTH, BAR_MAX_WIDTH = 3.0, 4.0, 140.0
REACH, SAME_COLUMN, GRID_MIN_WIDTH, SAME_LINE, LINE_TOL = 16.0, 2.0, 25.0, 6.0, 3.5


def _bars(page):
    """Thin rules that are not part of a grid: a table redraws its column
    border at every row, a fraction bar is drawn once."""
    rules = [d['rect'] for d in page.get_drawings()
             if d['rect'].height <= BAR_MAX_HEIGHT
             and BAR_MIN_WIDTH <= d['rect'].width <= BAR_MAX_WIDTH]
    return [r for r in rules
            if not (r.width >= GRID_MIN_WIDTH and any(
                o is not r and abs(o.y0 - r.y0) > 2
                and abs(o.x0 - r.x0) <= SAME_COLUMN
                and abs(o.x1 - r.x1) <= SAME_COLUMN for o in rules))]


def _mid(w):
    return (w[1] + w[3]) / 2


def _one_line(candidates, key):
    """The printed line nearest the bar, and only that one -- a numerator and
    a denominator are each a single line."""
    if not candidates:
        return []
    edge = key(sorted(candidates, key=key)[0])
    return [w for w in candidates if abs(key(w) - edge) <= LINE_TOL]


def _close(cur):
    x0 = min(bb[0] for bb, _ in cur)
    y0 = min(bb[1] for bb, _ in cur)
    x1 = max(bb[2] for bb, _ in cur)
    y1 = max(bb[3] for bb, _ in cur)
    return (x0, y0, x1, y1, subscripts(superscripts(''.join(t for _, t in cur))))


def words(page):
    """The page's words, each already read the way line_text() reads a line.

    PyMuPDF's own get_text('words') carries no font size, so an exponent inside
    a fraction was flattened -- the scheme's "(28^2 + 4^2 - 30^2)/(2(28)(4))"
    came back as "282 + 42-302/2(28)(4)", a different expression. Built from the
    character stream instead, so each word knows which of its characters were
    raised or lowered. Same 5-tuple shape as get_text('words'), so the fraction
    splice reads it unchanged.
    """
    out = []
    for b in page.get_text('rawdict')['blocks']:
        for ln in b.get('lines', []):
            weight = {}
            for sp in ln.get('spans', []):
                for ch in sp['chars']:
                    if ch['c'].strip():
                        weight[sp['size']] = weight.get(sp['size'], 0) + 1
            if not weight:
                continue
            base = max(weight, key=lambda k: (weight[k], k))
            cur, prev_y, prev_x1 = [], None, None
            for sp in ln.get('spans', []):
                for ch in sp['chars']:
                    box = ch['bbox']
                    if not ch['c'].strip() or (prev_x1 is not None
                                               and box[0] - prev_x1 > 1.2):
                        if cur:
                            out.append(_close(cur))
                            cur = []
                    prev_x1 = box[2]
                    if not ch['c'].strip():
                        continue
                    t = demangle(ch['c'])
                    small = sp['size'] <= base - 1.5 and prev_y is not None
                    if small and box[1] <= prev_y + 0.2:
                        t = f'^({t})'
                    elif small and box[1] > prev_y + 0.2:
                        t = f'_({t})'
                    else:
                        prev_y = box[1]
                    cur.append((box, t))
            if cur:
                out.append(_close(cur))
    return out


def fractions(page, cut=300):
    """[(x0, top, bottom, text)] -- each stacked fraction read back into a line."""
    found = [w for w in words(page) if w[4].strip()]
    out, band = [], []
    for bar in sorted(_bars(page), key=lambda r: (r.y0, r.x0)) + [None]:
        if band and (bar is None or bar.y0 - band[0].y0 > SAME_LINE):
            piece = _splice(found, band, cut)
            if piece:
                out.append(piece)
            band = []
        if bar is not None:
            band.append(bar)
    return out


def _over(w, x0, x1):
    """Does this word sit on the bar? Overlap, not containment: the extractor
    joins a denominator to whatever follows it when the PDF sets no space
    between them, so the "5" under pi/5 arrives as the word "5+" and reaches
    past the bar's right edge. Requiring containment dropped it and left the
    fraction unread."""
    lap = min(w[2], x1) - max(w[0], x0)
    return lap > 0 and lap >= 0.5 * min(w[2] - w[0], x1 - x0)


def _splice(words, band, cut=300):
    pieces, claimed, top, bottom = [], [], None, None
    side = band[0].x0 >= cut
    words = [w for w in words if (w[0] >= cut) == side]
    for bar in band:
        x0, x1 = bar.x0 - 3, bar.x1 + 3
        # Sorted on the word's MIDPOINT: an exponent sets its glyph box from the
        # top, so a denominator like "d^2" starts fractionally ABOVE the bar.
        above = [w for w in words
                 if bar.y0 - REACH < _mid(w) < bar.y0 and _over(w, x0, x1)]
        below = [w for w in words
                 if bar.y1 < _mid(w) < bar.y1 + REACH and _over(w, x0, x1)]
        num = _one_line(above, key=lambda w: -_mid(w))
        den = _one_line(below, key=lambda w: _mid(w))
        if not num or not den:
            continue
        claimed.extend(num + den)
        hi, lo = min(w[1] for w in num), max(w[3] for w in den)
        top = hi if top is None else min(top, hi)
        bottom = lo if bottom is None else max(bottom, lo)
        pieces.append((bar.x0, '{}/{}'.format(
            ' '.join(w[4] for w in sorted(num, key=lambda w: w[0])),
            ' '.join(w[4] for w in sorted(den, key=lambda w: w[0])))))
    if not pieces:
        return None
    # The rest of the expression -- the "r(2) =" before the fraction -- is set
    # on the fraction's own baseline, between numerator and denominator.
    held = {id(w) for w in claimed}
    for w in words:
        if id(w) not in held and top <= _mid(w) <= bottom:
            pieces.append((w[0], w[4]))
    text = ' '.join(t for _, t in sorted(pieces, key=lambda q: q[0]))
    return (min(x for x, _ in pieces), top, bottom,
            spacing(re.sub(r'\s+', ' ', text).strip()))


def placed(page, cut=300):
    """([(y, text)] left, [(y, text)] right) — columns WITH their positions.

    A Maths scheme page is a table, and one page frequently holds several
    parts: 25 of the 61 marked pages of the 2025 Higher scheme carry more than
    one part marker. Dropping the y coordinate collapses those into a single
    part and loses the rest, so the position is kept and the caller segments on
    it.
    """
    left, right = [], []
    spans = fractions(page, cut)
    for x0, top, bottom, text in spans:
        (right if x0 >= cut else left).append((top, text))
    for b in page.get_text('dict')['blocks']:
        for ln in b.get('lines', []):
            t = line_text(ln)
            if not t:
                continue
            x = min(s['bbox'][0] for s in ln['spans'])
            y = min(s['bbox'][1] for s in ln['spans'])
            # A line the fraction reader already consumed would otherwise be
            # emitted a second time, in halves.
            centre = (min(s['bbox'][1] for s in ln['spans'])
                      + max(s['bbox'][3] for s in ln['spans'])) / 2
            if any(top <= centre <= bottom and abs(x0 - x) < 200
                   for x0, top, bottom, _ in spans):
                continue
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
                # A paper sets its fractions stacked too: 2021 HL Paper 1 Q5(b)
                # asks for the tangent "at the point where x = pi/6", and read
                # line by line that arrives as "x = pi 6". The lines a fraction
                # occupies collapse into one row, whose clean side is the
                # fraction and whose plain side is still every character
                # paper.py saw, in the order it saw them -- clean_like searches
                # the plain side and returns the clean one, so both must hold.
                spans = fractions(page)
                buckets, loose = {}, []
                for b in page.get_text('dict')['blocks']:
                    for ln in b.get('lines', []):
                        plain = ''.join(sp['text'] for sp in ln['spans'])
                        if not plain.strip():
                            continue
                        y0 = min(sp['bbox'][1] for sp in ln['spans'])
                        centre = (y0 + max(sp['bbox'][3] for sp in ln['spans'])) / 2
                        x0 = min(sp['bbox'][0] for sp in ln['spans'])
                        at = next((i for i, f in enumerate(spans)
                                   if f[1] <= centre <= f[2] and abs(f[0] - x0) < 200),
                                  None)
                        if at is None:
                            loose.append((y0, line_text(ln), plain))
                        else:
                            buckets.setdefault(at, []).append((y0, plain))
                merged = [(min(y for y, _ in v), spans[i][3],
                           ''.join(t for _, t in sorted(v)))
                          for i, v in buckets.items()]
                rows.extend((c, p) for _, c, p in sorted(loose + merged,
                                                        key=lambda r: r[0]))
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


# The character before the operator can be a raised or lowered one -- a
# subscript n, an exponent, a prime. Listing only the superscript digits
# left "T_n= p" unspaced once subscripts started being read at all.
OPERATOR = re.compile(
    r'(?<=[A-Za-z0-9)\]|\u00b2\u00b3\u2074-\u2079\u00b9\u2070\u207f'
    r'\u2080-\u208e\u2090-\u209c\u1d62\u1d63\u2032\u2033])'
    r'\s*([=+\u00d7\u00f7\u2264\u2265<>\u2260])\s*')


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


SUB = {c: chr(0x2080 + i) for i, c in enumerate('0123456789')}
SUB.update({'+': '\u208a', '-': '\u208b', '\u2212': '\u208b',
            '(': '\u208d', ')': '\u208e',
            'a': '\u2090', 'e': '\u2091', 'i': '\u1d62', 'n': '\u2099',
            'x': '\u2093', 'r': '\u1d63', 't': '\u209c'})


def subscripts(text):
    """Render "_(3)" as a real subscript where every character has one.

    The same argument as superscripts(), for the other direction: the scheme
    writes a logarithm's base under the line, and dropping it spelled
    "log-base-3 of 7" as "log37", which reads as thirty-seven. Anything with no
    subscript glyph keeps the underscore form rather than being flattened,
    because flattening changes the maths.
    """
    def one(m):
        body = m.group(1)
        if body and all(c in SUB for c in body):
            return ''.join(SUB[c] for c in body)
        return f'_({body})' if len(body) > 1 else f'_{body}'
    return re.sub(r'_\(([^)]*)\)', one, text)


def superscripts(text):
    """Render "^(2)" as "²" where every character has a superscript form.

    A card shows this to a student, so "4x²" is worth having over "4x^(2)".
    Anything without a real superscript glyph -- "^(5x)" -- keeps the caret
    form rather than being flattened, because flattening changes the maths.
    """
    def one(m):
        body = m.group(1)
        # A prime is already a raised glyph; wrapping it as an exponent gives
        # "h^(′)(x)" where the scheme prints "h′(x)".
        if body and set(body) <= {'′', '″'}:
            return body
        if body and all(c in SUP for c in body):
            return ''.join(SUP[c] for c in body)
        return f'^({body})' if len(body) > 1 else f'^{body}'
    return re.sub(r'\^\(([^)]*)\)', one, text)
