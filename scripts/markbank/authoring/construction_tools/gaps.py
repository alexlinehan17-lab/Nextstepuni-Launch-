"""White horizontal bands on a page: gaps.py PDF page y0 y1 [x0 x1] -> blank row ranges (pt)"""
import sys, fitz
from PIL import Image
pdf, pg, y0, y1 = sys.argv[1], int(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4])
x0, x1 = (float(sys.argv[5]), float(sys.argv[6])) if len(sys.argv) > 6 else (25, 580)
d = fitz.open(pdf)
px = d[pg - 1].get_pixmap(matrix=fitz.Matrix(2, 2), clip=fitz.Rect(x0, y0, x1, y1), alpha=False)
im = Image.frombytes('RGB', (px.width, px.height), px.samples).convert('L')
w, h = im.size
blank = []
for y in range(h):
    row = im.crop((0, y, w, y + 1))
    if min(row.getdata()) > 245:
        blank.append(y)
runs, start = [], None
for i, y in enumerate(blank):
    if start is None: start = y
    if i + 1 == len(blank) or blank[i + 1] != y + 1:
        runs.append((round(y0 + start / 2, 1), round(y0 + (y + 1) / 2, 1))); start = None
print([r for r in runs if r[1] - r[0] >= 1.5])
