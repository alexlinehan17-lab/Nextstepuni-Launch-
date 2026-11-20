#!/usr/bin/env python3
"""Text for a Music booklet the SEC printed with no text layer (2012, and the
listening booklets of 2019, 2020, 2022, 2023 Higher and 2023, 2025 Ordinary):
each page rendered at 200 and at 300 dpi, and in four overlapping bands at 400 dpi, and read by Apple's Vision text recogniser
(music_ocr.swift, compiled on first use). The output is what the reading file's
question lines are checked against, in place of a text layer; the card shows a
crop of the printed page, so a student always sees the SEC's own print.

    python3 music_ocr.py <pdf> <out.json> [--lines <positions.txt>]

out.json: {"<page>": "<the page's recognised lines, top to bottom>"}.
--lines also writes every line with its box as page fractions (for crops).
macOS only (Vision); nothing in CI reads the PDF or runs this.
"""
import json
import os
import subprocess
import sys
import tempfile

import fitz

HERE = os.path.dirname(os.path.abspath(__file__))
BIN = '/private/tmp/claude-501/music-ocr-bin'


def ocr_binary():
    if not os.path.exists(BIN):
        os.makedirs(os.path.dirname(BIN), exist_ok=True)
        subprocess.run(['swiftc', '-O', os.path.join(HERE, 'music_ocr.swift'), '-o', BIN], check=True)
    return BIN


def reading_order(found):
    """Lines on one printed row, left to right, rows top to bottom. Vision
    reports lines by their top edge, so a part label set a hair lower than its
    question's first line ("(a)") fell between that line and the next."""
    rows = []
    for box, text in sorted(found, key=lambda f: (f[0][1] + f[0][3]) / 2):
        mid, h = (box[1] + box[3]) / 2, box[3] - box[1]
        row = rows[-1] if rows else None
        if row and abs(mid - row['mid']) <= 0.5 * min(h, row['h']):
            row['items'].append((box, text))
        else:
            rows.append({'mid': mid, 'h': h, 'items': [(box, text)]})
    return [item for row in rows for item in sorted(row['items'], key=lambda f: f[0][0])]


def main(pdf, out, lines_path=None):
    binary = ocr_binary()
    doc = fitz.open(pdf)
    pages, positions = {}, []
    with tempfile.TemporaryDirectory() as tmp:
        for i, pg in enumerate(doc):
            readings = []
            # Two independent readings, 200 and 300 dpi: each misses a word now
            # and then (2023 HL page 6 lost "excerpt." at 200); a line is the
            # SEC's if either reading holds it.
            for dpi in (200, 300):
                png = os.path.join(tmp, f'p{i + 1}-{dpi}.png')
                pg.get_pixmap(dpi=dpi).save(png)
                res = subprocess.run([binary, png], capture_output=True, text=True, check=True).stdout
                found = []
                for line in res.splitlines():
                    box, _, text = line.partition('\t')
                    found.append(([float(v) for v in box.split()], text))
                texts = []
                for box, text in reading_order(found):
                    texts.append(text)
                    if dpi == 200:
                        positions.append(f'p{i + 1} [{", ".join(f"{v:.3f}" for v in box)}]  {text}')
                readings.append('\n'.join(texts))
            # A third reading at 400 dpi, a quarter of the page at a time (with
            # overlap): a whole page is shrunk before it is read, and small
            # left-margin labels ("Line 1") dropped out (2019 OL page 6).
            band_texts = []
            for b in range(4):
                y0, y1 = max(0.0, b * 0.25 - 0.03), min(1.0, (b + 1) * 0.25 + 0.03)
                W, H = pg.rect.width, pg.rect.height
                png = os.path.join(tmp, f'p{i + 1}-band{b}.png')
                pg.get_pixmap(dpi=400, clip=fitz.Rect(0, y0 * H, W, y1 * H)).save(png)
                res = subprocess.run([binary, png], capture_output=True, text=True, check=True).stdout
                found = []
                for line in res.splitlines():
                    box, _, text = line.partition('\t')
                    found.append(([float(v) for v in box.split()], text))
                band_texts += [text for _, text in reading_order(found)]
            readings.append('\n'.join(band_texts))
            pages[str(i + 1)] = '\n\n'.join(readings)
    json.dump(pages, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    open(out, 'a').write('\n')
    if lines_path:
        open(lines_path, 'w', encoding='utf-8').write('\n'.join(positions) + '\n')


if __name__ == '__main__':
    args = sys.argv[1:]
    lines = None
    if '--lines' in args:
        i = args.index('--lines')
        lines = args[i + 1]
        del args[i:i + 2]
    main(args[0], args[1], lines)
