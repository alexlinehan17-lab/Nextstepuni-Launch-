"""Render every distinct paper/scheme crop pair of a reviewed paper module for visual inspection.
usage: python3 scripts/markbank/agricultural-science-audit/render_pairs.py <module> <year> <fileid> <outdir> [per-sheet]"""
import fitz, json, pathlib, sys, importlib
from PIL import Image, ImageDraw
sys.path.insert(0, 'scripts/markbank/authoring')
module, year, fileid, outdir = sys.argv[1:5]
per = int(sys.argv[5]) if len(sys.argv) > 5 else 4
root = pathlib.Path(outdir); root.mkdir(exist_ok=True, parents=True)
mod = importlib.import_module(module)
try:
    _, tasks = mod.reviewed_tasks()
except TypeError:
    _ex = {c['id']: c for c in json.load(open('scripts/markbank/authored/agricultural-science.json'))}
    _, tasks, _c = mod.reviewed_tasks(_ex)
pdfs = {k: fitz.open(f'paper-trail-corpus/{k}/{year}/{fileid}') for k in ['exampapers', 'markingschemes']}
unique = {}
for task in tasks:
    unique.setdefault(json.dumps([task['paperRegions'], task['schemeRegions']]), task)
def strip(regions, kind):
    pieces = []
    for r in regions:
        p = pdfs[kind][r['p']-1]; a, b, c, d = r['r']
        pix = p.get_pixmap(matrix=fitz.Matrix(1.2, 1.2), clip=fitz.Rect(a*p.rect.width, b*p.rect.height, c*p.rect.width, d*p.rect.height))
        pieces.append(Image.frombytes('RGB', [pix.width, pix.height], pix.samples))
    canvas = Image.new('RGB', (720, sum(x.height for x in pieces) + 6*len(pieces)), 'white'); y = 0
    for img in pieces:
        canvas.paste(img, (0, y)); y += img.height + 6
    return canvas
rows = []
for task in unique.values():
    a = strip(task['paperRegions'], 'exampapers'); b = strip(task['schemeRegions'], 'markingschemes'); h = max(a.height, b.height) + 35
    row = Image.new('RGB', (1460, h), 'white'); ImageDraw.Draw(row).text((10, 5), task['questionRef'][:120], fill='black')
    row.paste(a, (0, 30)); row.paste(b, (740, 30)); rows.append(row)
n = 0
for n, start in enumerate(range(0, len(rows), per)):
    subset = rows[start:start+per]; canvas = Image.new('RGB', (1460, sum(x.height+15 for x in subset)), '#ddd'); y = 0
    for row in subset:
        canvas.paste(row, (0, y)); y += row.height + 15
    canvas.save(root/f'review-{n+1:02}.png')
print(len(unique), 'distinct pairs in', n+1, 'sheets')
