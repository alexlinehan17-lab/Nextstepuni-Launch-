"""Render explicit, source-reviewed rectangles for pre-scale Maths papers.

Preview only: never changes the deck, catalogues or published images. Inspect
all crops before copying the declarations through the normal publishers.
Usage: python3 .../legacy_presentation_figures.py 2012-hl-p1
"""
import hashlib
import io
import json
import sys
from pathlib import Path
import fitz
from PIL import Image, ImageChops, ImageDraw

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[3]


def render(doc, regions, dpi):
    pieces = []
    for r in regions:
        page = doc[r['page'] - 1]
        clip = fitz.Rect(r['x0'], r['top'], r['x1'], r['bottom'])
        assert page.rect.contains(clip), r
        im = Image.open(io.BytesIO(page.get_pixmap(clip=clip, dpi=dpi).tobytes('png'))).convert('RGB')
        box = ImageChops.difference(im, Image.new('RGB', im.size, 'white')).getbbox()
        assert box, r
        # Retain column width and eight pixels above/below ink; no formula reflow.
        im = im.crop((0, max(0, box[1] - 8), im.width, min(im.height, box[3] + 8)))
        pieces.append(im)
    width = max(im.width for im in pieces)
    out = Image.new('RGB', (width, sum(im.height for im in pieces) + 24 * (len(pieces)-1)), 'white')
    y = 0
    for im in pieces:
        out.paste(im, ((width-im.width)//2, y)); y += im.height + 24
    return out


def main(key):
    source = json.loads((BASE / f'{key}-source-review.json').read_text())
    plan = json.loads((BASE / f'{key}-presentation.json').read_text())
    year = key.split('-')[0]
    paths = [ROOT / 'paper-trail-corpus' / kind / year / source[field] for kind, field in
             [('exampapers', 'paperFileid'), ('markingschemes', 'schemeFileid')]]
    for path, field in zip(paths, ['paperSha256', 'schemeSha256']):
        assert hashlib.sha256(path.read_bytes()).hexdigest() == source[field], path
    docs = [fitz.open(p) for p in paths]
    out = ROOT / 'tmp' / 'pdfs' / f'mathematics-{key}-review' / 'crops'
    out.mkdir(parents=True, exist_ok=True)
    for kind, doc, field in zip(['question', 'solution'], docs, ['questionRegions', 'schemeRegions']):
        for task in source['tasks']:
            suffix = task['suffix']
            render(doc, plan['tasks'][suffix][field], 200).save(out / f'{kind}-{suffix}.png')
        # Two-column sheets preserve readable equations for every individual crop.
        groups, group, height = [], [], 0
        for task in source['tasks']:
            suffix = task['suffix']; im = Image.open(out / f'{kind}-{suffix}.png')
            w = 820; h = round(im.height*w/im.width)
            if height+h > 2500 and group: groups.append(group); group=[];height=0
            group.append((suffix, im.resize((w,h))));height+=h+36
        if group:groups.append(group)
        for index in range(0,len(groups),2):
            cols=groups[index:index+2]
            sheet=Image.new('RGB',(1680,max(sum(im.height+36 for _,im in col) for col in cols)+20),'white')
            draw=ImageDraw.Draw(sheet)
            for col, entries in enumerate(cols):
                y=10
                for suffix,im in entries:
                    draw.text((col*840+10,y),f'{kind} {suffix}',fill='black');y+=26
                    sheet.paste(im,(col*840+10,y));y+=im.height+10
            sheet.save(out/f'{kind}-qa-{index//2+1:02}.jpg',quality=92)
        print(kind, len(source['tasks']), 'crops', (len(groups)+1)//2, 'QA sheets')


if __name__ == '__main__':
    main(sys.argv[1])
