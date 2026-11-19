"""Render inspected source crops plus clearly labelled calculations for Q4 routes.

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
from review_2011_hl_p1_project import SOURCE, PRESENTATION, tasks, base_suffix, fit_pair, VALUES

OUT = Path('tmp/pdfs/mathematics-2011-hl-p1-project-review/crops')
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
    parts = suffix.split('-'); i, j = parts[3:5]; A, rate = fit_pair(i, j)
    fig = plt.figure(figsize=(7.2, 3.4), dpi=200, facecolor='white')
    fig.text(.035, .92, f'NextStepUni worked route · t = {i} and {j}', fontsize=13, weight='bold', color='#242424')
    if suffix.startswith('4-a-'):
        lines = [rf'$b=\frac{{\ln({VALUES[int(i)]:.3f}/{VALUES[int(j)]:.3f})}}{{{int(j)-int(i)}}}\approx {rate:.6f}$',
                 rf'$A={VALUES[int(i)]:.3f}\,e^{{{i}b}}\approx {A:.6f}$',
                 rf'$A={A:.3f},\qquad b={rate:.3f}\quad\mathrm{{(3\ decimal\ places)}}$']
        footer = 'Calculated from the selected pair. The SEC example below uses t = 0 and 1.'
    else:
        k = int(parts[-1]); ar, br = round(A, 3), round(rate, 3); predicted = ar * math.exp(-br * k)
        lines = [rf'$A={ar:.3f},\quad b={br:.3f},\quad t={k}\ \mathrm{{was\ not\ used}}$',
                 rf'$Q({k})\approx {ar:.3f}\,e^{{-{br:.3f}\times {k}}}={predicted:.6f}$',
                 rf'$\mathrm{{Printed}}\ Q({k})={VALUES[k]:.3f};\quad |\mathrm{{difference}}|\approx {abs(predicted-VALUES[k]):.6f}$']
        footer = 'Approximate check: the table and fitted parameters are rounded.\nThe SEC accepts values carried from part (a); its original example follows.'
    for y, line in zip([.69, .46, .23], lines):fig.text(.04, y, line, fontsize=20, color='#171717')
    fig.text(.035, .045, footer, fontsize=8.5, color='#383833', linespacing=1.5)
    buf = io.BytesIO(); fig.savefig(buf, format='png', dpi=200); plt.close(fig); buf.seek(0)
    return Image.open(buf).convert('RGB')


def main():
    docs = {'question': fitz.open('paper-trail-corpus/exampapers/2011/' + SOURCE['paperFileid']),
            'solution': fitz.open('paper-trail-corpus/markingschemes/2011/' + SOURCE['schemeFileid'])}
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
    print('36 question crops, 36 SEC solution crops, 40 route supplements rendered')


if __name__ == '__main__':main()
