#!/usr/bin/env python3
"""Render the official-document crops that reviewed Geography cards bind.

A review ledger names each crop (a task's question_figure or figure) as a
geography_review.Figure: the document
(the task's question booklet, the marking scheme, or a companion map, legend
or aerial photograph), the page and the rectangle in PDF points. This script
renders every one to public/exam-figures/geography/markbank/<name>.png from
the same files the generator reads; geography_cards.py records each PNG's MD5
on its card, so a crop that drifts fails `geography_cards.py --check`.

    python3 scripts/markbank/authoring/geography_figures.py          # check
    python3 scripts/markbank/authoring/geography_figures.py --write
"""

from __future__ import annotations

import os
import sys

import fitz

import geography_cards as GC
import geography_review as GR

# Wide enough to read a 1:50 000 symbol on a phone; never upscaled past this.
MAX_WIDTH = 900
MAX_ZOOM = 6.0


def document_for(sitting: GR.Sitting, task: GR.Task, figure: GR.Figure) -> fitz.Document:
    if figure.document == 'paper':
        return sitting.papers[task.part].doc
    if figure.document == 'scheme':
        return sitting.scheme.doc
    fileid = GC.COMPANIONS[sitting.year].get(figure.document)
    if not fileid:
        raise AssertionError(f'{figure.name}: {sitting.year} has no {figure.document} companion')
    return fitz.open(GC.companion_path(sitting.year, fileid))


def render(sitting: GR.Sitting, task: GR.Task, figure: GR.Figure) -> bytes:
    doc = document_for(sitting, task, figure)
    page = doc[figure.page - 1]
    rect = fitz.Rect(figure.rect)
    if not page.rect.contains(rect):
        raise AssertionError(f'{figure.name}: crop {tuple(rect)} leaves page {tuple(page.rect)}')
    zoom = min(MAX_ZOOM, MAX_WIDTH / rect.width)
    return page.get_pixmap(matrix=fitz.Matrix(zoom, zoom), clip=rect).tobytes('png')


def figures():
    for (year, level), review in sorted(GC.REVIEWED.items()):
        crops = [(task, figure) for task in review.TASKS
                 for figure in (task.question_figure, task.figure) if figure is not None]
        if not crops:
            continue
        sitting = GR.Sitting.open(year, level)
        for task, figure in crops:
            yield sitting, task, figure


def main() -> int:
    write = '--write' in sys.argv
    os.makedirs(GR.FIGURE_ROOT, exist_ok=True)
    names, stale = [], []
    for sitting, task, figure in figures():
        if figure.name in names:
            raise AssertionError(f'{figure.name}: two crops share one name')
        names.append(figure.name)
        data = render(sitting, task, figure)
        path = os.path.join(GR.FIGURE_ROOT, f'{figure.name}.png')
        current = open(path, 'rb').read() if os.path.exists(path) else b''
        if current == data:
            continue
        if write:
            with open(path, 'wb') as handle:
                handle.write(data)
            print(f'wrote {os.path.relpath(path, GR.ROOT)} ({len(data):,} bytes)')
        else:
            stale.append(figure.name)
    # Every PNG in the folder is a crop some ledger declares.
    orphans = sorted(set(name[:-4] for name in os.listdir(GR.FIGURE_ROOT) if name.endswith('.png'))
                     - set(names))
    if orphans:
        print('crops no ledger declares: ' + ', '.join(orphans), file=sys.stderr)
        return 1
    if stale:
        print('stale crops (run with --write): ' + ', '.join(stale), file=sys.stderr)
        return 1
    print(f'{len(names)} Geography crop(s) current.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
