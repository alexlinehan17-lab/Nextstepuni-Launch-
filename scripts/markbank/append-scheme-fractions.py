#!/usr/bin/env python3
"""
Mark Bank — read stacked fractions back into one line.

    python3 scripts/markbank/append-scheme-fractions.py <subject> <year> <hl|ol>
    python3 scripts/markbank/append-scheme-fractions.py --all

A formula is the one thing a marking scheme states that is not written on a
line. The SEC sets

              εA
        C =  ────
               d

and every text extraction flattens it to "C = εA d", because the numerator, the
bar and the denominator are three separate objects. A card carrying the answer
the way a student writes it, "C = εA/d", is then untraceable — thirteen Physics
and roughly twenty-five Chemistry cards, every one of them a correct formula.

The bar is a drawn rule, so the three parts can be put back together: take the
words sitting on the rule, the words sitting under it, and splice them into the
rest of that line as "numerator/denominator" at the position the bar occupied.

A table's cell borders are rules too, and pairing the header above one with the
value below it would emit nonsense. They are told apart by repetition: a grid
draws the same column border again at every row, a fraction bar is drawn once.

Append-only, as append-scheme-tables.py and append-scheme-columns.py are:
comparableScheme() joins every line, so nothing that matches today can stop
matching, and every character emitted is a character the SEC printed.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import pymupdf

sys.path.insert(0, str(Path(__file__).resolve().parent))
from markbank_text import unligature  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
START = '<!-- markbank:fractions -->'
END = '<!-- /markbank:fractions -->'

# A fraction bar is a filled rule a few points high at most.
BAR_MAX_HEIGHT = 3.0
# Under this it is a stray tick; over it, on these schemes, it is always a table
# border or an underline spanning a column.
BAR_MIN_WIDTH = 4.0
BAR_MAX_WIDTH = 140.0
# How far above and below the bar its own numerator and denominator sit.
REACH = 16.0
# A table's column border is drawn again at every row, so the same x0..x1 turns
# up at several different heights. A fraction bar is drawn once. Adjacency was
# tried first and was wrong: two fractions printed side by side — which is how
# Coulomb's law is set, 1/4πε beside q₁q₂/d² — butt up just as a table's cells do.
SAME_COLUMN = 2.0
# Only a rule wide enough to BE a column border is tested for repetition. The
# bar over l/g is four points wide, and several of those at the same x on one
# page are several fractions, not a table.
GRID_MIN_WIDTH = 25.0
# Bars whose tops agree this closely are on the same line of the formula.
SAME_LINE = 6.0
# How far off the bar a word may sit and still be on the fraction's baseline.
BASELINE = 5.0
# Words are on the same printed line if their edges agree this closely.
LINE_TOL = 3.5


def bars(page):
    """The page's fraction bars: thin rules that are not part of a grid."""
    rules = []
    for d in page.get_drawings():
        r = d['rect']
        if r.height <= BAR_MAX_HEIGHT and BAR_MIN_WIDTH <= r.width <= BAR_MAX_WIDTH:
            rules.append(r)
    out = []
    for r in rules:
        repeated = r.width >= GRID_MIN_WIDTH and any(
            o is not r and abs(o.y0 - r.y0) > 2
            and abs(o.x0 - r.x0) <= SAME_COLUMN and abs(o.x1 - r.x1) <= SAME_COLUMN
            for o in rules
        )
        if not repeated:
            out.append(r)
    return out


def mid(word):
    """A word's vertical centre."""
    return (word[1] + word[3]) / 2


def nearest_line(candidates, key):
    """Only the printed line closest to the bar.

    A fixed reach above and below caught a second line as well: "F = G m1 m2/d²"
    came out with "of" as its denominator, read off "force of earth on moon"
    printed underneath. The numerator and the denominator are each ONE line.
    """
    if not candidates:
        return []
    candidates = sorted(candidates, key=key)
    edge = key(candidates[0])
    return [w for w in candidates if abs(key(w) - edge) <= LINE_TOL]


def spliced(page, band):
    """One line of formula, with each bar in `band` read as numerator/denominator."""
    words = [w for w in page.get_text('words') if w[4].strip()]
    pieces = []                                   # (x, text)
    claimed = []
    top = bottom = None
    for bar in band:
        x0, x1 = bar.x0 - 3, bar.x1 + 3
        # Sorted on the word's MIDPOINT, not its edges. "d²" sets its glyph box
        # from the top of the superscript, so the denominator of F = G m1 m2/d²
        # starts a tenth of a point ABOVE the bar and an edge test dropped it —
        # then took "of", from the line of prose below, as the denominator.
        above = [w for w in words if bar.y0 - REACH < mid(w) < bar.y0 and w[0] >= x0 and w[2] <= x1]
        below = [w for w in words if bar.y1 < mid(w) < bar.y1 + REACH and w[0] >= x0 and w[2] <= x1]
        num = nearest_line(above, key=lambda w: -mid(w))
        den = nearest_line(below, key=lambda w: mid(w))
        if not num or not den:
            continue
        claimed.extend(num + den)
        # The band is what the fraction ACTUALLY occupies, not the search reach.
        hi, lo = min(w[1] for w in num), max(w[3] for w in den)
        top = hi if top is None else min(top, hi)
        bottom = lo if bottom is None else max(bottom, lo)
        pieces.append((bar.x0, '{}/{}'.format(
            ' '.join(w[4] for w in sorted(num, key=lambda w: w[0])),
            ' '.join(w[4] for w in sorted(den, key=lambda w: w[0])))))
    if not pieces:
        return None
    # The rest of the formula — the "C =" before the fraction, the "= constant"
    # after it — is set on the fraction's own baseline, between numerator and
    # denominator. Searching the padded REACH band instead swept in whatever ran
    # above or below: "n = c1/c2" came out as "n light = c1/c2 = as they travel
    # through the block of glass", which no card can match.
    claimed_ids = {id(w) for w in claimed}
    core = list(pieces)
    for w in words:
        if id(w) in claimed_ids:
            continue
        centre = mid(w)
        if not top <= centre <= bottom:
            continue
        pieces.append((w[0], w[4]))
        # The "C =" of "C = εA/d" is set on the fraction's own baseline, level
        # with the bar. Whatever else shares the numerator's or denominator's
        # line usually is not part of the formula — "c2" is followed on its line
        # by "cred = 1.985 × 108", and a card quoting "n = c1/c2" cannot match
        # through that. So a second, baseline-only reading is emitted too.
        if any(bar.y0 - BASELINE <= centre <= bar.y1 + BASELINE for bar in band):
            core.append((w[0], w[4]))
    join = lambda ps: ' '.join(t for _, t in sorted(ps, key=lambda q: q[0]))
    return [join(pieces), join(core)]


def fractions(pdf: Path) -> list[str]:
    doc = pymupdf.open(pdf)
    out, seen = [], set()
    for page in doc:
        found = sorted(bars(page), key=lambda r: (r.y0, r.x0))
        band: list = []
        for bar in found + [None]:
            if band and (bar is None or bar.y0 - band[0].y0 > SAME_LINE):
                for line in spliced(page, band) or []:
                    text = unligature(re.sub(r'\s+', ' ', line).strip())
                    if len(text) >= 5 and text not in seen:
                        seen.add(text)
                        out.append(text)
                band = []
            if bar is not None:
                band.append(bar)
    doc.close()
    return out


def pdf_for(subject: str, year: int, level: str) -> Path | None:
    """The marking-scheme PDF for exactly this subject, year and level.

    Same resolution as append-scheme-columns.py, and for the same reason: the
    bare `<year>-marking-scheme.pdf` name is sometimes a DEFERRED paper.
    """
    d = ROOT / 'examiner-reports' / subject
    names = ([f'{year}-{level}-marking-scheme.pdf'] if level == 'ol'
             else [f'{year}-hl-marking-scheme.pdf', f'{year}-marking-scheme.pdf'])
    for name in names:
        path = d / name
        if not path.exists():
            continue
        with pymupdf.open(path) as doc:
            cover = ' '.join(doc[0].get_text().split())
        if 'Deferred' in cover:
            continue
        if ('Ordinary Level' if level == 'ol' else 'Higher Level') not in cover:
            continue
        return path
    return None


def apply(subject: str, year: int, level: str) -> None:
    md = ROOT / 'examiner-reports' / subject / 'schemes' / f'{year}-{level}.md'
    if not md.exists():
        raise SystemExit(f'no scheme markdown at {md}')
    pdf = pdf_for(subject, year, level)
    if pdf is None:
        raise SystemExit(f'no marking-scheme PDF for {subject} {year} {level}')
    lines = fractions(pdf)
    text = md.read_text(encoding='utf-8')
    if START in text:
        text = re.sub(re.escape(START) + r'.*?' + re.escape(END) + r'\n?', '', text, flags=re.S)
    if not lines:
        md.write_text(text.rstrip('\n') + '\n', encoding='utf-8')
        print(f'{subject} {year} {level}: no stacked fractions')
        return
    body = f'{START}\n' + '\n'.join(lines) + f'\n{END}\n'
    md.write_text(text.rstrip('\n') + '\n\n' + body, encoding='utf-8')
    print(f'{subject} {year} {level}: appended {len(lines)} reconstructed fractions')


def main() -> None:
    if sys.argv[1:2] == ['--all']:
        for md in sorted((ROOT / 'examiner-reports').glob('*/schemes/*.md')):
            subject = md.parents[1].name
            year, level = md.stem.split('-')
            if pdf_for(subject, int(year), level) is None:
                print(f'{subject} {year} {level}: no PDF, skipped')
                continue
            apply(subject, int(year), level)
        return
    if len(sys.argv) < 4:
        raise SystemExit('usage: append-scheme-fractions.py <subject> <year> <hl|ol>')
    apply(sys.argv[1], int(sys.argv[2]), sys.argv[3])


if __name__ == '__main__':
    main()
