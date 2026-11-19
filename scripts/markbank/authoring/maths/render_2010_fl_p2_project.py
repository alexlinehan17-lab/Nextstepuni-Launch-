"""Render review-only original question/solution crops; never certify or publish."""
import io
from pathlib import Path
import fitz
from PIL import Image, ImageDraw
from review_2010_fl_p2_project import SOURCE, PRESENTATION

OUT = Path('tmp/pdfs/mathematics-2010-fl-p2-project-review/crops')


def stack(pieces):
    width = max(im.width for im in pieces)
    canvas = Image.new('RGB', (width + 24, sum(im.height for im in pieces) + 24 + 20 * (len(pieces) - 1)), 'white')
    y = 12
    for im in pieces:
        canvas.paste(im, ((canvas.width - im.width) // 2, y))
        y += im.height + 20
    return canvas


def sheet(items, prefix):
    for stale in OUT.glob(f'{prefix}-sheet-*.jpg'):
        stale.unlink()
    heights = [0, 0]
    canvas = Image.new('RGB', (1600, 1860), '#eaeaea')
    draw = ImageDraw.Draw(canvas)
    n = 1
    for suffix, im in items:
        scale = min(760 / im.width, 1500 / im.height, 1)
        thumb = im.resize((int(im.width * scale), int(im.height * scale)))
        col = 0 if heights[0] <= heights[1] else 1
        if heights[col] + thumb.height + 34 > 1840:
            canvas.save(OUT / f'{prefix}-sheet-{n:02}.jpg', quality=92)
            n += 1
            canvas = Image.new('RGB', (1600, 1860), '#eaeaea')
            draw = ImageDraw.Draw(canvas)
            heights = [0, 0]
            col = 0
        x = col * 800 + 20
        y = heights[col] + 8
        draw.text((x, y), prefix + ' ' + suffix, fill='black')
        canvas.paste(thumb, (x, y + 25))
        heights[col] += thumb.height + 34
    canvas.save(OUT / f'{prefix}-sheet-{n:02}.jpg', quality=92)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
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
            result = stack(pieces)
            result.save(OUT / f'{kind}-{suffix}.png')
            items.append((suffix, result))
        sheet(items, kind)
    print('34 question crops and 34 complete SEC solution crops rendered for inspection')


if __name__ == '__main__':
    main()
