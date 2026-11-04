#!/usr/bin/env python3
"""Render, and publish, the crops each eng_residue sitting names by rectangle.

    python3 scripts/markbank/authoring/eng_crops.py 2021 hl --review DIR   # PNGs to look at
    python3 scripts/markbank/authoring/eng_crops.py 2021 hl --publish      # bind into the manifest

eng_figures.py finds crops by itself and is right most of the time; the parts
it gets wrong, or finds nothing for, are recorded in its REJECTED map and the
crop is measured by eye instead -- the rectangle read off a render of the
page, written into the sitting's CROPS, rendered and LOOKED AT before it is
published. Publishing goes through bind-figures.mjs, which hashes the bytes,
refuses a name that would change what it points at, and writes the manifest
the build resolves figure keys through. Nothing about a path is typed on a
card.

A solution crop is the scheme's own print of an answer the scheme gives as a
drawing, a graph or a stacked fraction. The manifest marks it `solution`, so
the session holds it back until the scheme is revealed.
"""
import argparse
import json
import os
import subprocess
import sys
import unicodedata

import pymupdf

DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, DIR)
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(DIR)))

import eng_residue                                          # noqa: E402
from eng_lift import path_for                               # noqa: E402

DPI = 200


def _boxes(spec):
    """[(page, rect)] this crop is cut from: one box, or several stacked."""
    return [tuple(b) for b in spec['parts']] if spec.get('parts') \
        else [(spec['page'], spec['rect'])]


def crop_words(year, level, spec):
    out = []
    masks = [pymupdf.Rect(*m) for m in spec.get('mask', ())]
    with pymupdf.open(path_for(year, level, spec['doc'])) as doc:
        for page_no, rect in _boxes(spec):
            page = doc[page_no - 1]
            r = pymupdf.Rect(*rect)
            words = [w for w in page.get_text('words')
                     if r.contains(pymupdf.Point((w[0] + w[2]) / 2, (w[1] + w[3]) / 2))
                     and not any(m.contains(pymupdf.Point((w[0] + w[2]) / 2,
                                                          (w[1] + w[3]) / 2))
                                 for m in masks)]
            words.sort(key=lambda w: (round(w[3]), w[0]))
            out.append(' '.join(w[4] for w in words))
    return ' '.join(out)


def describe(year, level, spec):
    ref = spec['ref']
    if spec.get('solution'):
        text = (f'The marking scheme\'s printed answer for {ref}, as the State '
                f'Examinations Commission set it.')
    else:
        text = (f'The table or diagram printed with {ref}, as the State '
                f'Examinations Commission set it.')
    # Combining marks and private-use code points are the PDF's broken font
    # subsets ("Temperature ( \u030aC)"), which the build refuses in alt text;
    # they come off the description, never the picture.
    words = ' '.join(''.join(
        ch for ch in crop_words(year, level, spec)
        if unicodedata.category(ch) not in ('Mn', 'Co')).split())
    if words:
        text += ' It reads: ' + words[:400] + '.'
    return text


def render(year, level, spec, out):
    with pymupdf.open(path_for(year, level, spec['doc'])) as doc:
        if spec.get('image'):
            page = doc[spec['page'] - 1]
            # The embedded photograph itself, where the page sets prose over
            # or against its edges and no rectangle takes the picture without
            # a fragment of a neighbouring line: the image whose placement on
            # the page is `rect`, drawn alone at the same resolution.
            want = pymupdf.Rect(*spec['rect'])
            for im in page.get_images(full=True):
                for r in page.get_image_rects(im[0]):
                    if abs(r.x0 - want.x0) < 2 and abs(r.y0 - want.y0) < 2 \
                            and abs(r.x1 - want.x1) < 2 and abs(r.y1 - want.y1) < 2:
                        pix = pymupdf.Pixmap(doc, im[0])
                        if pix.alpha or pix.n > 3:
                            pix = pymupdf.Pixmap(pymupdf.csRGB, pix)
                        scale = DPI / 72 * want.width / pix.width
                        if scale < 1:
                            pix.shrink(int(1 / scale).bit_length() - 1)
                        pix.save(out)
                        return
            raise SystemExit(f'{out}: no image placed at {spec["rect"]} on page {spec["page"]}')
        from PIL import Image, ImageDraw
        tiles = []
        for page_no, rect in _boxes(spec):
            pg = doc[page_no - 1]
            clip = pymupdf.Rect(*rect)
            pix = pg.get_pixmap(clip=clip, dpi=DPI)
            im = Image.frombytes('RGB', (pix.width, pix.height), pix.samples)
            # White out page text that falls inside the box but belongs to
            # the prose beside the picture -- the ask's own line running
            # into a photograph's top edge. Only page FURNITURE is masked,
            # and the mask is part of the reviewed spec, never a guess.
            k = DPI / 72
            draw = ImageDraw.Draw(im)
            for m in spec.get('mask', ()):
                mr = pymupdf.Rect(*m) & clip
                if not mr.is_empty:
                    draw.rectangle([(mr.x0 - clip.x0) * k, (mr.y0 - clip.y0) * k,
                                    (mr.x1 - clip.x0) * k, (mr.y1 - clip.y0) * k],
                                   fill='white')
            tiles.append(im)
        if len(tiles) == 1:
            tiles[0].save(out)
            return
        # Several boxes, one below the other, left-aligned with a band of
        # white between them: one answer the scheme prints in pieces (a
        # labelled diagram for each furnace a candidate may choose).
        gap = int(12 * DPI / 72)
        if spec.get('layout') == 'row':
            # Side by side, top-aligned: three diagrams of one height read
            # at a size a phone can show, where a column of them could not.
            sheet = Image.new('RGB', (sum(t.width for t in tiles) + gap * (len(tiles) - 1),
                                      max(t.height for t in tiles)), 'white')
            x = 0
            for t in tiles:
                sheet.paste(t, (x, 0))
                x += t.width + gap
        else:
            sheet = Image.new('RGB', (max(t.width for t in tiles),
                                      sum(t.height for t in tiles) + gap * (len(tiles) - 1)),
                              'white')
            y = 0
            for t in tiles:
                sheet.paste(t, (0, y))
                y += t.height + gap
        sheet.save(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('year', type=int)
    ap.add_argument('level')
    ap.add_argument('--review', help='render every crop into this directory')
    ap.add_argument('--publish', action='store_true',
                    help='stage the crops and bind them into the manifest')
    ap.add_argument('--replace', action='store_true',
                    help='pass --replace to bind-figures (a reviewed rect changed)')
    args = ap.parse_args()
    mod = eng_residue.module(args.year, args.level)
    crops = getattr(mod, 'CROPS', {}) if mod else {}
    if not crops:
        print('no crops for this sitting')
        return 0
    stem = f'engineering-{args.year}-{args.level.upper()}-'
    for name, spec in crops.items():
        if not name.startswith(stem):
            raise SystemExit(f'{name}: a {args.year} {args.level} crop is named {stem}...')
        if bool(spec.get('solution')) != (spec['doc'] == 'scheme'):
            raise SystemExit(f'{name}: a scheme crop is a solution and a paper crop is not')
    if args.review:
        os.makedirs(args.review, exist_ok=True)
        for name, spec in crops.items():
            render(args.year, args.level, spec, os.path.join(args.review, f'{name}.png'))
            print(os.path.join(args.review, f'{name}.png'))
    if args.publish:
        stage = os.path.join(ROOT, 'exam-papers', 'engineering', 'figures',
                             f'{args.year}-{args.level}')
        os.makedirs(stage, exist_ok=True)
        catalogue = []
        for name, spec in crops.items():
            render(args.year, args.level, spec, os.path.join(stage, f'{name}.png'))
            catalogue.append({
                'file': f'{name}.png', 'kind': 'figure', 'truncated': False,
                'questionRef': spec['ref'],
                'lettersVisible': list(spec.get('letters', ())),
                'description': describe(args.year, args.level, spec),
                **({'solution': True} if spec.get('solution') else {}),
            })
        cat = os.path.join(stage, 'residue-catalogue.json')
        with open(cat, 'w', encoding='utf-8') as fh:
            json.dump(catalogue, fh, ensure_ascii=False, indent=1)
        cmd = ['node', os.path.join(ROOT, 'scripts/markbank/bind-figures.mjs'), cat]
        if args.replace:
            cmd.append('--replace')
        subprocess.run(cmd, check=True, cwd=ROOT)
    return 0


if __name__ == '__main__':
    sys.exit(main())
