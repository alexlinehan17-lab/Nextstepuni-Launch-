"""Question-number lines and content extents on paper pages: qlines.py PDF"""
import sys, fitz, re
d = fitz.open(sys.argv[1])
for i, p in enumerate(d):
    if i == 0: continue
    marks = []
    ys = []
    for b in p.get_text('dict')['blocks']:
        for l in b.get('lines', []):
            t = ''.join(s['text'] for s in l['spans']).strip()
            if not t: continue
            y0, y1 = l['bbox'][1], l['bbox'][3]
            if y1 < 800: ys.append(y1)
            if re.match(r'^(\d{1,2})\.$|^(\d{1,2})\.\s', t) and l['bbox'][0] < 80: marks.append((round(y0), t[:40]))
            if t.startswith('OR'): marks.append((round(y0), 'OR'))
    imgs = [[round(v) for v in im['bbox']] for im in p.get_image_info() if im['bbox'][3] - im['bbox'][1] < 700]
    print(f'p{i+1}', 'marks', marks, 'maxText', round(max(ys)) if ys else None, 'imgs', imgs)
