"""Horizontal content extents per page: xext.py PDF first last"""
import sys, fitz
d = fitz.open(sys.argv[1])
for pg in range(int(sys.argv[2]), int(sys.argv[3]) + 1):
    p = d[pg - 1]
    ims = [im['bbox'] for im in p.get_image_info() if im['bbox'][3] - im['bbox'][1] < 780]
    dr = [x['rect'] for x in p.get_drawings() if x['rect'].y1 < 790 and x['rect'].y0 > 50 and x['rect'].width < 560]
    tx = [l['bbox'] for b in p.get_text('dict')['blocks'] for l in b.get('lines', []) if ''.join(s['text'] for s in l['spans']).strip() and 50 < l['bbox'][1] < 790]
    allx0 = [r.x0 for r in dr] + [i[0] for i in ims] + [t[0] for t in tx]
    allx1 = [r.x1 for r in dr] + [i[2] for i in ims] + [t[2] for t in tx]
    flag = '  <-- outside 51..545' if (allx0 and min(allx0) < 50) or (allx1 and max(allx1) > 546) else ''
    print(pg, round(min(allx0)) if allx0 else None, round(max(allx1)) if allx1 else None, flag)
