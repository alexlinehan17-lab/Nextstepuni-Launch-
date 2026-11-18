#!/usr/bin/env python3
"""Lift Engineering text off the printed page by RECTANGLE, never by typing.

    python3 scripts/markbank/authoring/eng_lift.py 2021 hl scheme 14            # every line, with its box
    python3 scripts/markbank/authoring/eng_lift.py 2021 hl scheme 14 36 60 560 120   # what a box lifts
    python3 scripts/markbank/authoring/eng_lift.py --record 2021 hl   # the sitting's lifts into its .md
    python3 scripts/markbank/authoring/eng_lift.py --check 2021 hl    # re-lift every recorded line

The automatic author (eng_all.py) reads the scheme through eng_scheme, and on
the parts it refuses the reader is usually what is wrong, not the scheme: a
diagram's callouts welded into the answer ("optical lens filter filament
optical lens" in the middle of the optical pyrometer paragraph), two
paragraphs read as one point, a heading taken for an answer. Re-teaching the
reader for one page at a time rewrites cards that already ship, so the parts
it refuses are authored in eng_residue/ instead -- and what a residue card
says has to come from the same two documents, by the same rule: question from
the paper, every marking point from the scheme.

A Lift is the text inside a rectangle of a PDF page: the words whose centre
falls inside it, in printed line order, joined with single spaces. Choosing
the rectangle is editorial -- which lines of the scheme answer this part --
and the words are the SEC's. Nothing here accepts a string in place of a
rectangle, and lib.card only accepts Lift objects for `lifted=`.
"""
import os
import re
import sys

import pymupdf

DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, DIR)
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(DIR)))

from paper import unligature                                # noqa: E402

BASE = os.path.join(ROOT, 'examiner-reports', 'engineering')
# The Symbol-font bullet and its repaired forms, which open a scheme line and
# are not part of what it says (eng_scheme.BULLET reads the same set).
BULLET = re.compile(r'^[•●·‣➢▪\-]\s*')
# How far apart two words' baselines may be and still be one printed line.
LINE_TOL = 3.0

_DOCS = {}
# U+F0FB: a private-use code the text layer gives one glyph of 2015 HL scheme
# p11 ("heated to 850?C", x 313-343, y 256-272). Cropped out of the page and
# looked at, it is the degree ring; it is the only U+F0FB in the 60 Engineering
# papers and schemes, so the repair can reach nothing else.
#
# U+030A, COMBINING RING ABOVE: the 2022 Higher deferred scheme's Calibri sets
# the degree sign as a ring over a no-break space, twice on p13 ("727  ̊C" at
# x 294, y 137-149 and "1147  ̊C" at x 403, y 484-496). Rendered at 400 dpi it
# is the degree ring. The only other U+030A in the 62 Engineering papers and
# schemes is 2021 HL scheme p16's graph axis title "Temperature (  ̊C)", which
# no lift reads; the deck refuses the bare glyph as a broken-font mark.
ENG_GLYPHS = {'\u019e': 'tf', '\uf0fb': '\u00b0', '\u030a': '\u00b0'}


def path_for(year, level, doc):
    if doc == 'paper':
        return os.path.join(BASE, 'papers', f'{year}-{level}-paper.pdf')
    if doc == 'scheme':
        return os.path.join(BASE, 'schemes', f'{year}-{level}.pdf')
    raise ValueError(f'unknown document {doc!r}: paper or scheme')


def _doc(year, level, doc):
    key = (year, level, doc)
    if key not in _DOCS:
        _DOCS[key] = pymupdf.open(path_for(year, level, doc))
    return _DOCS[key]


class Lift(str):
    """Text lifted from a rectangle of an SEC page. `source` says which."""

    def __new__(cls, text, source):
        obj = super().__new__(cls, text)
        obj.source = source
        return obj


def _lines(year, level, doc, page, rect):
    """[(y, [words...])] for the words whose centre lies inside rect."""
    pg = _doc(year, level, doc)[page - 1]
    x0, y0, x1, y1 = rect
    words = []
    for w in pg.get_text('words'):
        cx, cy = (w[0] + w[2]) / 2, (w[1] + w[3]) / 2
        if x0 <= cx <= x1 and y0 <= cy <= y1:
            words.append(w)
    # Printed line order: by baseline, a tolerance wide, then left to right.
    words.sort(key=lambda w: (round(w[3], 1), w[0]))
    rows = []
    for w in words:
        if rows and abs(rows[-1][0] - w[3]) <= LINE_TOL:
            rows[-1][1].append(w)
        else:
            rows.append([w[3], [w]])
    return [(y, sorted(ws, key=lambda w: w[0])) for y, ws in rows]


def _clean(text):
    text = unligature(' '.join(text.replace('\xa0', ' ').split()))
    # Glyphs the shared ligature fold (schemeText.mjs) does not know, as the
    # 2026 Engineering schemes set them: Calibri's "tf" ligature reaches the
    # text layer as U+019E, so "platform" reads "plaƞorm". Repaired here, for
    # Engineering's own lifts only; the recorded lift carries the repaired
    # word into the .md, where the provenance gate finds it.
    for glyph, letters in ENG_GLYPHS.items():
        text = text.replace(glyph, letters)
    return text


def lift(year, level, doc, page, rect, *, bullet=True, more=(), items=()):
    """The text inside rect on page (1-based) of the paper or scheme.

    `more` adds further rectangles on the same page, read in turn: a printed
    sentence whose own column is interrupted by a picture's caption ("any one
    of the following:" with "electronic component" set beside it, over the
    captions of the three pictures it means).

    `items` are rectangles each holding ONE printed list item -- a line whose
    bullet the font draws (Symbol's U+F0B7, which the text layer drops) or one
    of several captions set side by side under their pictures. Each is set on
    a line of its own after the text above it, so "with reference to each of
    the following: equipment used flame types ..." keeps the list the paper
    prints instead of running its items into one phrase. Only line breaks are
    added; every word is still the page's.
    """
    rows = []
    for r in (rect, *more):
        rows += _lines(year, level, doc, page, r)
    text = _clean(' '.join(' '.join(w[4] for w in ws) for _, ws in rows))
    lines = []
    for r in items:
        line = _clean(' '.join(' '.join(w[4] for w in ws)
                               for _, ws in _lines(year, level, doc, page, r)))
        if not line:
            raise ValueError(f'{year} {level} {doc} p{page} {r}: the item box lifts nothing')
        lines.append(line)
    if bullet:
        text = BULLET.sub('', text).strip()
    if not text:
        raise ValueError(f'{year} {level} {doc} p{page} {rect}: the box lifts nothing')
    if lines:
        if doc != 'paper':
            raise ValueError('items= sets a printed list on its lines: paper questions only')
        return Lift('\n'.join([text] + lines),
                    (year, level, doc, page, tuple(rect), tuple(map(tuple, more)),
                     ('items',) + tuple(map(tuple, items))))
    obj = Lift(text, (year, level, doc, page, tuple(rect))
               if not more else (year, level, doc, page, tuple(rect), tuple(map(tuple, more))))
    # A piece that opens on a printed bullet and keeps it (bullet=False) --
    # the first item of a list carried over a page break -- is recorded with
    # a "•" after its rectangle, so `check` lifts it again the same way.
    obj.keeps_bullet = not bullet
    return obj


def join(*parts):
    """One printed paragraph that runs over a page break, as its pieces.

    Each piece is a Lift of its own page; the paragraph is their words in
    turn. `record` writes it as one line naming every piece's page and
    rectangle, and `check` lifts each piece again and joins them.
    """
    if len(parts) < 2 or not all(hasattr(p, 'source') and not hasattr(p, 'parts')
                                 for p in parts):
        raise ValueError('join takes two or more single-page lifts')
    if len({p.source[:3] for p in parts}) != 1:
        raise ValueError('join reads one document')
    obj = Lift(' '.join(parts), ('join',) + tuple(p.source for p in parts))
    obj.parts = parts
    return obj


def cells(*parts):
    """One table row the scheme prints as cells side by side, as its cells.

    The text layer runs a row's cells together ("Charpy Test Izod Test"), and
    a cell that wraps runs into its neighbour line by line. Each piece is a
    Lift of ONE cell -- a row's cells in turn, or a column's head and a cell
    under it -- and the row reads them joined with " — ", the table's rule set
    as a dash: layout, not words. `record` writes the pieces with " — "
    between them, and `check` lifts each again and joins them the same way.
    """
    if len(parts) < 2 or not all(hasattr(p, 'source') and not hasattr(p, 'parts')
                                 for p in parts):
        raise ValueError('cells takes two or more single-page lifts')
    if len({p.source[:3] for p in parts}) != 1:
        raise ValueError('cells reads one document')
    obj = Lift(' — '.join(parts), ('cells',) + tuple(p.source for p in parts))
    obj.parts = parts
    obj.sep = ' — '
    return obj


START = '<!-- markbank:eng-lifts -->'
END = '<!-- /markbank:eng-lifts -->'


def _lifts_in(obj, out):
    # Duck-typed: run as __main__ this module's Lift is not the class the
    # residue module imported, and isinstance would see no lifts at all.
    if isinstance(obj, str) and hasattr(obj, 'source'):
        out.append(obj)
    elif isinstance(obj, dict):
        for v in obj.values():
            _lifts_in(v, out)
    elif isinstance(obj, (list, tuple)):
        for v in obj:
            _lifts_in(v, out)
    return out


def record(year, level):
    """Append (idempotently) the sitting's scheme lifts to its .md.

    The provenance gate reads the markdown, and the flat extraction welds a
    diagram's callouts into the prose printed beside it ("the scissor arm is
    scissor pushed upwards raising the platform"), so a row lifted cleanly by
    rectangle cannot trace there although the SEC printed every word of it in
    order. Each lift the sitting's eng_residue module uses is written into an
    APPEND-ONLY block with the page and rectangle it came from, so a reviewer
    can lift it again and get the same words -- `check` below does exactly
    that. Like the column and page-run renderings, it only adds lines: every
    claim that traces today still traces.
    """
    import re as _re
    import eng_residue
    mod = eng_residue.module(year, level)
    lifts = _lifts_in(getattr(mod, 'CARDS', []), []) if mod else []
    lines, seen = [], set()
    for lf in lifts:
        pieces = getattr(lf, 'parts', None) or [lf]
        y, l, doc = pieces[0].source[:3]
        if doc != 'scheme' or (y, l) != (year, level) or str(lf) in seen:
            continue
        if any(len(pc.source) > 5 for pc in pieces):
            raise SystemExit(f'{lf[:40]!r}: a scheme row is one rectangle a page')
        seen.add(str(lf))
        where = getattr(lf, 'sep', ' + ').join(f'p{pc.source[3]} [{", ".join(f"{v:g}" for v in pc.source[4])}]'
                           + ('•' if getattr(pc, 'keeps_bullet', False) else '')
                           for pc in pieces)
        lines.append(f'{where} {lf}')
    md = os.path.join(BASE, 'schemes', f'{year}-{level}.md')
    text = open(md, encoding='utf-8').read()
    if START in text:
        text = _re.sub(_re.escape(START) + r'.*?' + _re.escape(END) + r'\n?', '',
                       text, flags=_re.S)
    body = f'{START}\n' + '\n'.join(lines) + f'\n{END}\n'
    with open(md, 'w', encoding='utf-8') as fh:
        fh.write(text.rstrip('\n') + '\n\n' + body)
    print(f'engineering {year} {level}: recorded {len(lines)} lifts in {os.path.basename(md)}')


def check(year, level):
    """Every recorded lift, lifted again from its page: the same words?"""
    import re as _re
    md = os.path.join(BASE, 'schemes', f'{year}-{level}.md')
    text = open(md, encoding='utf-8').read()
    m = _re.search(_re.escape(START) + r'\n(.*?)' + _re.escape(END), text, _re.S)
    bad = 0
    for line in (m.group(1).splitlines() if m else []):
        if not line.strip():
            continue
        g = _re.match(r'^((?:p\d+ \[[^\]]+\]•?(?: \+ | — )?)+) (.*)$', line)
        pieces = [lift(year, level, 'scheme', int(pg), [float(v) for v in r.split(',')],
                       bullet=not kept)
                  for pg, r, kept in _re.findall(r'p(\d+) \[([^\]]+)\](•?)', g.group(1))]
        glue = cells if '] — p' in g.group(1) or ']• — p' in g.group(1) else join
        again = pieces[0] if len(pieces) == 1 else glue(*pieces)
        if str(again) != g.group(2):
            bad += 1
            print(f'MISMATCH {g.group(1)}: {g.group(2)[:60]!r} != {again[:60]!r}')
    print(f'engineering {year} {level}: {len((m.group(1).splitlines()) if m else [])} '
          f'recorded lifts, {bad} mismatched')
    return bad


def dump(year, level, doc, page):
    pg = _doc(year, level, doc)[page - 1]
    for b in pg.get_text('dict')['blocks']:
        for ln in b.get('lines', []):
            t = ''.join(s['text'] for s in ln['spans'])
            if t.strip():
                print([round(v) for v in ln['bbox']], repr(t))


if __name__ == '__main__':
    if sys.argv[1] in ('--record', '--check'):
        fn = record if sys.argv[1] == '--record' else check
        sys.exit(1 if fn(int(sys.argv[2]), sys.argv[3]) else 0)
    y, l, d, p = int(sys.argv[1]), sys.argv[2], sys.argv[3], int(sys.argv[4])
    if len(sys.argv) > 8:
        print(repr(lift(y, l, d, p, [float(v) for v in sys.argv[5:9]])))
    else:
        dump(y, l, d, p)
