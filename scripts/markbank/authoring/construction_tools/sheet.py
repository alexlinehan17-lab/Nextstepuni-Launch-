"""Contact sheets of a draft dir's crops: sheet.py DIR OUTPREFIX [per] [width]"""
import sys, glob, re
from PIL import Image, ImageDraw
d, out = sys.argv[1], sys.argv[2]
per = int(sys.argv[3]) if len(sys.argv) > 3 else 10
w = int(sys.argv[4]) if len(sys.argv) > 4 else 300
fs = sorted(glob.glob(d + '/construction-studies-*.png'))
for n in range(0, len(fs), per):
    th = []
    for f in fs[n:n + per]:
        im = Image.open(f).convert('RGB'); h = int(im.height * w / im.width); t = im.resize((w, h))
        c = Image.new('RGB', (w + 4, h + 20), 'red'); c.paste(t, (2, 18)); ImageDraw.Draw(c).text((4, 2), re.split(r'-(?:HL|OL)-', f)[-1][:40], fill='white'); th.append(c)
    half = (len(th) + 1) // 2
    rows = [th[:half], th[half:]]
    W = max(sum(t.width for t in r) for r in rows); H = sum(max((t.height for t in r), default=0) for r in rows)
    s = Image.new('RGB', (W, H), 'white'); y = 0
    for r in rows:
        x = 0
        for t in r: s.paste(t, (x, y)); x += t.width
        y += max((t.height for t in r), default=0)
    s.save(f'{out}{n // per}.png'); print(f'{out}{n // per}.png', s.size, [re.split(r'-(?:HL|OL)-', f)[-1] for f in fs[n:n + per]])
