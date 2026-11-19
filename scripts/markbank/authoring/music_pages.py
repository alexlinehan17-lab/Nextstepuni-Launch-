#!/usr/bin/env python3
"""Reading aid for a Music sitting (music lane): renders pages and prints each
line of the text layer with its position as page fractions, so a reader can
set an ask's crop box from where its label and the next label sit.

    python3 music_pages.py lines <pdf> <page> [<page> ...]
    python3 music_pages.py render <pdf> <outdir> [dpi] [<page> ...]
    python3 music_pages.py find <pdf> "<text>"       # every page and box where the text layer prints it

Boxes are [x0, y0, x1, y1] as fractions of the page, the form the reading files use.
"""
import os
import sys

import fitz


def lines(pdf, pages):
    doc = fitz.open(pdf)
    for p in pages:
        pg = doc[p - 1]
        W, H = pg.rect.width, pg.rect.height
        print(f'=== page {p} ({W:.0f} x {H:.0f})')
        for b in pg.get_text('dict')['blocks']:
            for ln in b.get('lines', []):
                text = ''.join(s['text'] for s in ln['spans']).strip()
                if not text:
                    continue
                x0, y0, x1, y1 = ln['bbox']
                print(f'  [{x0 / W:.3f}, {y0 / H:.3f}, {x1 / W:.3f}, {y1 / H:.3f}]  {text}')


def render(pdf, out, dpi, pages):
    doc = fitz.open(pdf)
    os.makedirs(out, exist_ok=True)
    stem = os.path.splitext(os.path.basename(pdf))[0]
    for p in pages or range(1, doc.page_count + 1):
        path = os.path.join(out, f'{stem}-p{p:02d}.png')
        doc[p - 1].get_pixmap(dpi=dpi).save(path)
        print(path)


def find(pdf, text):
    doc = fitz.open(pdf)
    for i, pg in enumerate(doc):
        W, H = pg.rect.width, pg.rect.height
        for r in pg.search_for(text):
            print(f'page {i + 1}: [{r.x0 / W:.3f}, {r.y0 / H:.3f}, {r.x1 / W:.3f}, {r.y1 / H:.3f}]')


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'lines':
        lines(sys.argv[2], [int(x) for x in sys.argv[3:]])
    elif cmd == 'render':
        dpi = int(sys.argv[4]) if len(sys.argv) > 4 else 100
        render(sys.argv[2], sys.argv[3], dpi, [int(x) for x in sys.argv[5:]])
    elif cmd == 'find':
        find(sys.argv[2], sys.argv[3])
    else:
        raise SystemExit(__doc__)
