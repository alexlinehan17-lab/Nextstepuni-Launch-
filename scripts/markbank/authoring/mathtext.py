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
GLYPH = {'න': '∫', '൤': '[', '൨': ']', 'ൣ': '[', '൧': ']',
         '൬': '(', '൰': ')', 'ඈ': '{', 'ඉ': '}',
         'ඥ': '√', 'ඩ': '√', 'ℎ': 'h', '': ''}


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
    return ''.join(out).strip()


def columns(page, cut=300):
    """(model solution lines, marking-notes lines) for one scheme page."""
    left, right = [], []
    for b in page.get_text('dict')['blocks']:
        for ln in b.get('lines', []):
            t = line_text(ln)
            if not t:
                continue
            x = min(s['bbox'][0] for s in ln['spans'])
            y = min(s['bbox'][1] for s in ln['spans'])
            (right if x >= cut else left).append((y, t))
    return ([t for _, t in sorted(left)], [t for _, t in sorted(right)])


SCALE = re.compile(r'Scale\s+(\d+)([A-Z]?)\s*\(([\d,\s]+)\)')
STEP = re.compile(r'^Step\s+(\d+)\.\s*(.+)$')


def steps_and_scale(notes):
    """The marking steps and the partial-credit ladder — a card's answer."""
    steps = [(int(m.group(1)), m.group(2).strip())
             for line in notes if (m := STEP.match(line))]
    scale = next((m for line in notes if (m := SCALE.search(line))), None)
    ladder = [int(v) for v in scale.group(3).split(',')] if scale else None
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
