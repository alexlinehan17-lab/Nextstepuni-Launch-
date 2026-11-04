#!/usr/bin/env python3
"""History's question figures: the printed tables an Ordinary Part A is set on.

    python3 scripts/markbank/authoring/hist_figures.py          # write crops + manifest
    python3 scripts/markbank/authoring/hist_figures.py --check  # fail if any would change

A Part A set on a printed chart (the election results of 2015, 2016, 2018 and
2020 Ordinary Later Modern) asks its questions of the TABLE. Read as text, a
row of it is a run of words, "Fianna Fáil Eamon de Valera 69 77", which is not
a table a student can read. So the card's stem is the printed instruction
alone (hist_paper.HistPaper.tables keeps the chart's own lines), and the chart
itself is cropped from the paper's page here, at reading resolution, and shown
as the card's question figure beside the stem (includesPrompt: false: the
stem and the question stay visible).

The crop is the chart's title and its ruled grid, both found on the page: the
title is the chart's first printed line, the grid is the drawn rules around
the rows. Nothing is drawn, typed or redrawn. The alt text is the chart's own
cells, read off the grid row by row and column by column, so a screen reader
gets the table, not a run of words.

Every crop written here is LOOKED AT before it ships (lane rule): the manifest
records its md5, and build-deck refuses a figure whose file has changed since.
"""
import argparse
import hashlib
import json
import os
import sys

import pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))

from hist_paper import HistPaper, FIELDS, GLYPHS                  # noqa: E402

MANIFEST = os.path.join(ROOT, 'components', 'MarkBank', 'figures-history.json')
OUT_DIR = os.path.join(ROOT, 'public', 'exam-figures', 'history')
LEVEL_NAME = {'hl': 'Higher Level', 'ol': 'Ordinary Level'}
DPI = 200
PAD = 8.0


def unit_slug(unit):
    """'2 Topic 3 A' -> 's2t3a', as hist_all's card ids spell a unit."""
    section, _topic_word, topic, part = unit.split()
    return f's{section}t{topic}{part.lower()}'


def figure_key(year, level, field, unit):
    return f'history-{year}-{level}-{field}-{unit_slug(unit)}-table'


def _grid(page, lines):
    """The drawn rules that make the chart's grid, and their bounds."""
    top = min(l.top for l in lines) - 20
    bottom = max(l.bottom for l in lines) + 20
    xs, ys, rects = set(), set(), []
    for d in page.get_drawings():
        r = d['rect']
        if r.y1 < top or r.y0 > bottom:
            continue
        rects.append(r)
        if r.width < 2 and r.height > 4:
            xs.add(round((r.x0 + r.x1) / 2, 1))
        if r.height < 2 and r.width > 10:
            ys.add(round((r.y0 + r.y1) / 2, 1))
    if not rects:
        raise AssertionError('no drawn grid around the chart')
    bounds = rects[0]
    for r in rects[1:]:
        bounds |= r
    return sorted(_merge(xs)), sorted(_merge(ys)), bounds


def _merge(values, tol=2.0):
    """Rules drawn as several touching segments collapse to one position."""
    out = []
    for v in sorted(values):
        if out and v - out[-1] <= tol:
            continue
        out.append(v)
    return out


def _cells(page, xs, ys):
    """The chart's cells, row by row, each the words printed inside it."""
    words = [(x0, y0, x1, y1, w.translate(GLYPHS))
             for x0, y0, x1, y1, w, *_ in page.get_text('words')]
    rows = []
    for top, bottom in zip(ys, ys[1:]):
        row = []
        for left, right in zip(xs, xs[1:]):
            inside = sorted(((y0, x0), w) for x0, y0, x1, y1, w in words
                            if left <= (x0 + x1) / 2 <= right and top <= (y0 + y1) / 2 <= bottom)
            row.append(' '.join(w for _pos, w in inside))
        if any(row):
            rows.append(row)
    return rows


def crop(paper, unit):
    """(png bytes, alt, attribution, page) for one unit's printed table."""
    lines = paper.tables[unit]
    pages = {l.page for l in lines}
    if len(pages) != 1:
        raise AssertionError(f'{unit}: the chart runs over pages {sorted(pages)}')
    pno = pages.pop()
    with pymupdf.open(paper.path) as doc:
        page = doc[pno - 1]
        xs, ys, grid = _grid(page, lines)
        rows = _cells(page, xs, ys)
        above = [l for l in lines if l.bottom <= grid.y0 + 1]
        clip = pymupdf.Rect(grid)
        for l in above:
            clip |= pymupdf.Rect(l.x0, l.top, l.x1, l.bottom)
        # Pad, but never into the instruction printed just above the chart.
        above_text = [y1 for _x0, _y0, _x1, y1, *_ in page.get_text('words') if y1 <= clip.y0 - 0.5]
        head_room = min(PAD, (clip.y0 - max(above_text)) / 2) if above_text else PAD
        clip = pymupdf.Rect(clip.x0 - PAD, clip.y0 - head_room, clip.x1 + PAD, clip.y1 + PAD) & page.rect
        png = page.get_pixmap(clip=clip, dpi=DPI).tobytes('png')
    title = ' '.join(' '.join(l.text for l in above).split())
    header, body = rows[0], rows[1:]
    alt = (f'The chart printed on the paper{": " + title if title else ""}. '
           f'Columns: {" | ".join(header)}. '
           f'Rows: {"; ".join(" | ".join(cell or "(blank)" for cell in row) for row in body)}.')
    level = LEVEL_NAME[paper.level]
    attribution = (f'SEC Leaving Certificate History {paper.year} {level}, '
                   f'{FIELDS[paper.field]} paper, page {pno} — © State Examinations Commission.')
    return png, alt, attribution, pno


def build(papers):
    entries = {}
    files = {}
    for year, level, field in papers:
        paper = HistPaper(year, level, field)
        for unit in sorted(paper.tables):
            key = figure_key(year, level, field, unit)
            png, alt, attribution, _page = crop(paper, unit)
            name = f'{key}.png'
            files[name] = png
            entries[key] = {
                'src': f'/exam-figures/history/{name}',
                'md5': hashlib.md5(png).hexdigest(),
                'alt': alt,
                'attribution': attribution,
            }
    return entries, files


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true')
    args = ap.parse_args()
    from hist_all import PAPERS                                    # noqa: E402
    entries, files = build(PAPERS)
    current = {}
    if os.path.exists(MANIFEST):
        with open(MANIFEST, encoding='utf-8') as fh:
            current = json.load(fh)
    if args.check:
        stale = [k for k in set(entries) | set(current) if entries.get(k) != current.get(k)]
        stale += [n for n, b in files.items()
                  if not os.path.exists(os.path.join(OUT_DIR, n))
                  or open(os.path.join(OUT_DIR, n), 'rb').read() != b]
        if stale:
            print('stale History figures:', *sorted(set(stale)), sep='\n  ')
            return 1
        print(f'{len(entries)} History question figure(s) current')
        return 0
    os.makedirs(OUT_DIR, exist_ok=True)
    for name, png in files.items():
        with open(os.path.join(OUT_DIR, name), 'wb') as fh:
            fh.write(png)
    with open(MANIFEST, 'w', encoding='utf-8') as fh:
        json.dump(dict(sorted(entries.items())), fh, ensure_ascii=False, indent=1)
        fh.write('\n')
    print(f'{len(entries)} History question figure(s) written:', *sorted(entries), sep='\n  ')
    return 0


if __name__ == '__main__':
    sys.exit(main())
