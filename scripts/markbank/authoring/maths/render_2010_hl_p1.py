"""Render original source crops plus labelled calculations for all four fifth roots.

Run from the repository root with PyMuPDF, Pillow and matplotlib available.
This writes review images only; it never publishes or certifies them.
"""
import io
import math
from pathlib import Path
import fitz
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
from review_2010_hl_p1 import SOURCE, PRESENTATION, tasks, base_suffix

OUT = Path('tmp/pdfs/mathematics-2010-hl-p1-review/crops')
OUT.mkdir(parents=True, exist_ok=True)
plt.rcParams.update({'font.family': 'DejaVu Sans', 'mathtext.fontset': 'stix'})


def sheet(items, prefix):
    heights = [0, 0]; canvas = Image.new('RGB', (1600, 1860), '#eaeaea'); draw = ImageDraw.Draw(canvas); n = 1
    for suffix, im in items:
        scale = min(760 / im.width, 1500 / im.height, 1)
        thumb = im.resize((int(im.width * scale), int(im.height * scale)))
        col = 0 if heights[0] <= heights[1] else 1
        if heights[col] + thumb.height + 45 > 1840:
            canvas.save(OUT / f'{prefix}-sheet-{n:02}.jpg', quality=90)
            n += 1; canvas = Image.new('RGB', (1600, 1860), '#eaeaea'); draw = ImageDraw.Draw(canvas); heights = [0, 0]; col = 0
        x = col * 800 + 20; y = heights[col] + 8
        draw.text((x, y), prefix + ' ' + suffix, fill='black'); canvas.paste(thumb, (x, y + 25)); heights[col] += thumb.height + 45
    canvas.save(OUT / f'{prefix}-sheet-{n:02}.jpg', quality=90)


def stack(pieces):
    w = max(im.width for im in pieces)
    result = Image.new('RGB', (w + 24, sum(im.height for im in pieces) + 24 + 20 * (len(pieces) - 1)), 'white'); y = 12
    for im in pieces:
        result.paste(im, ((result.width - im.width) // 2, y)); y += im.height + 20
    return result


def supplement(suffix):
    n = int(suffix.rsplit('-', 1)[1]); a = 4*n; b = 6*n
    fig = plt.figure(figsize=(7.2, 4.0), dpi=200, facecolor='white')
    fig.text(.035, .93, f'NextStepUni worked route · fifth root {n}', fontsize=13, weight='bold', color='#242424')
    lines = [rf'$w=\cos\frac{{{2*n}\pi}}{{5}}+i\sin\frac{{{2*n}\pi}}{{5}}$',
             rf'$w^2+w^3=\cos\frac{{{a}\pi}}{{5}}+\cos\frac{{{b}\pi}}{{5}}+i\left(\sin\frac{{{a}\pi}}{{5}}+\sin\frac{{{b}\pi}}{{5}}\right)$',
             rf'$=2\cos({n}\pi)\cos\frac{{{n}\pi}}{{5}}+i\left(2\sin({n}\pi)\cos\frac{{{n}\pi}}{{5}}\right)$',
             rf'$={2*(-1)**n}\cos\frac{{{n}\pi}}{{5}}+0i\quad\in\mathbb{{R}}$']
    for y, line in zip([.76, .56, .36, .16], lines):fig.text(.04, y, line, fontsize=18, color='#171717')
    fig.text(.035, .035, 'Exact working for the selected root. The original SEC example and full marking notes follow.', fontsize=8.5, color='#383833')
    buf=io.BytesIO();fig.savefig(buf, format='png', dpi=200);plt.close(fig);buf.seek(0)
    return Image.open(buf).convert('RGB')


def main():
    docs = {'question': fitz.open('paper-trail-corpus/exampapers/2010/' + SOURCE['paperFileid']),
            'solution': fitz.open('paper-trail-corpus/markingschemes/2010/' + SOURCE['schemeFileid'])}
    for kind, field in [('question', 'questionRegions'), ('solution', 'schemeRegions')]:
        items = []
        for suffix, view in PRESENTATION['tasks'].items():
            pieces = []
            for r in view[field]:
                pix = docs[kind][r['page'] - 1].get_pixmap(clip=fitz.Rect(r['x0'], r['top'], r['x1'], r['bottom']), dpi=200)
                im = Image.open(io.BytesIO(pix.tobytes('png'))).convert('RGB')
                for x0, y0, x1, y1 in r.get('erase', []):
                    im.paste('white', tuple(round(v * 200 / 72) for v in (x0-r['x0'], y0-r['top'], x1-r['x0'], y1-r['top'])))
                pieces.append(im)
            result = stack(pieces); result.save(OUT / f'{kind}-{suffix}.png'); items.append((suffix, result))
        sheet(items, kind)
    supplements = []
    for task in tasks():
        s = task['suffix']
        if not task.get('selectionVariant'):continue
        extra = supplement(s); extra.save(OUT / f'route-{s}.png'); supplements.append((s, extra))
        original = Image.open(OUT / ('solution-' + base_suffix(s) + '.png')).convert('RGB')
        stack([extra, original]).save(OUT / f'solution-{s}.png')
    sheet(supplements, 'route')
    print('40 question crops, 40 SEC solution crops, 4 route supplements rendered')


if __name__ == '__main__':main()
