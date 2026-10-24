#!/usr/bin/env python3
"""Render labelled English review spreads without altering source PDFs."""
import argparse
from pathlib import Path
import fitz
from PIL import Image, ImageDraw
from english_complete import ROOT, inventory


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('year', type=int)
    parser.add_argument('level', choices=['hl', 'ol'])
    parser.add_argument('paper', type=int, choices=[1, 2])
    parser.add_argument('pages', nargs='*', type=int)
    parser.add_argument('--scheme', action='store_true')
    args = parser.parse_args()
    key = f'english-{args.year}-{args.level}-p{args.paper}'
    record = next(p for p in inventory()['papers'] if p['id'] == key)
    source = record['markingScheme' if args.scheme else 'questionPaper']
    doc = fitz.open(ROOT / source['path'])
    pages = args.pages or list(range(1, len(doc) + 1))
    kind = 'scheme' if args.scheme else 'paper'
    out = ROOT / 'tmp/english-audit/review' / key
    out.mkdir(parents=True, exist_ok=True)
    for offset in range(0, len(pages), 2):
        selected = pages[offset:offset + 2]
        spread = Image.new('RGB', (1000 * len(selected), 1450), '#dddddd')
        draw = ImageDraw.Draw(spread)
        for column, page in enumerate(selected):
            pdf_page = doc[page - 1]
            pixmap = pdf_page.get_pixmap(matrix=fitz.Matrix(980 / pdf_page.rect.width, 980 / pdf_page.rect.width))
            tile = Image.frombytes('RGB', (pixmap.width, pixmap.height), pixmap.samples)
            spread.paste(tile, (1000 * column + 10, 30))
            draw.text((1000 * column + 10, 8), f'{key} {kind} PDF p.{page}', fill='black')
        filename = out / f'{kind}-{selected[0]:02d}-{selected[-1]:02d}.jpg'
        spread.save(filename, quality=93)
        print(filename.relative_to(ROOT))


if __name__ == '__main__':
    main()
