"""Render ruled page thumbnails: pages.py PDF OUTPREFIX first last [per_sheet]"""
import sys, fitz
from PIL import Image, ImageDraw
pdf, out, first, last = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
per = int(sys.argv[5]) if len(sys.argv) > 5 else 4
d = fitz.open(pdf)
pages = list(range(first, last + 1))
for n in range(0, len(pages), per):
    ims = []
    for pg in pages[n:n + per]:
        px = d[pg - 1].get_pixmap(matrix=fitz.Matrix(1, 1), alpha=False)
        im = Image.frombytes('RGB', (px.width, px.height), px.samples)
        dr = ImageDraw.Draw(im)
        for y in range(50, 842, 50):
            dr.line([(0, y), (12, y)], fill='red'); dr.text((14, y - 5), str(y), fill='red')
        dr.text((300, 5), f'p{pg}', fill='blue')
        ims.append(im)
    W = sum(i.width for i in ims); H = max(i.height for i in ims)
    s = Image.new('RGB', (W, H), 'white'); x = 0
    for i in ims:
        s.paste(i, (x, 0)); x += i.width
    s.save(f'{out}{n // per}.png'); print(f'{out}{n // per}.png', pages[n:n + per])
