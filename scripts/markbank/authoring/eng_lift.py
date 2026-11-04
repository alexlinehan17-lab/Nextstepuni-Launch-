#!/usr/bin/env python3
"""Lift Engineering text off the printed page by RECTANGLE, never by typing.

    python3 scripts/markbank/authoring/eng_lift.py 2021 hl scheme 14            # every line, with its box
    python3 scripts/markbank/authoring/eng_lift.py 2021 hl scheme 14 36 60 560 120   # what a box lifts

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


def lift(year, level, doc, page, rect, *, bullet=True):
    """The text inside rect on page (1-based) of the paper or scheme."""
    rows = _lines(year, level, doc, page, rect)
    text = ' '.join(' '.join(w[4] for w in ws) for _, ws in rows)
    text = unligature(' '.join(text.replace('\xa0', ' ').split()))
    if bullet:
        text = BULLET.sub('', text).strip()
    if not text:
        raise ValueError(f'{year} {level} {doc} p{page} {rect}: the box lifts nothing')
    return Lift(text, (year, level, doc, page, tuple(rect)))


def dump(year, level, doc, page):
    pg = _doc(year, level, doc)[page - 1]
    for b in pg.get_text('dict')['blocks']:
        for ln in b.get('lines', []):
            t = ''.join(s['text'] for s in ln['spans'])
            if t.strip():
                print([round(v) for v in ln['bbox']], repr(t))


if __name__ == '__main__':
    y, l, d, p = int(sys.argv[1]), sys.argv[2], sys.argv[3], int(sys.argv[4])
    if len(sys.argv) > 8:
        print(repr(lift(y, l, d, p, [float(v) for v in sys.argv[5:9]])))
    else:
        dump(y, l, d, p)
