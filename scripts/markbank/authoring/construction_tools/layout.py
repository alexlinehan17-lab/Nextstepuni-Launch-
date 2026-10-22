"""Scheme page layout summary: layout.py PDF first last -> headings with y, content y/x extents, images"""
import sys, fitz, re
d = fitz.open(sys.argv[1])
for pg in range(int(sys.argv[2]), int(sys.argv[3]) + 1):
    p = d[pg - 1]
    heads = []
    tx = []
    for b in p.get_text('dict')['blocks']:
        for l in b.get('lines', []):
            t = ''.join(s['text'] for s in l['spans']).strip()
            if not t or l['bbox'][1] < 48 or l['bbox'][1] > 795: continue
            tx.append(l['bbox'])
            if re.match(r'^(Question|QUESTION)\s*\d|^\([abc]\)|^Any other', t):
                heads.append(f"{round(l['bbox'][1])}-{round(l['bbox'][3])}:{t[:28]}")
    ims = [[round(v) for v in im['bbox']] for im in p.get_image_info() if 48 < im['bbox'][3] and im['bbox'][1] < 795 and im['bbox'][3] - im['bbox'][1] > 3]
    dr = [x['rect'] for x in p.get_drawings() if 48 < x['rect'].y0 and x['rect'].y1 < 795 and x['rect'].width < 560]
    ys = [t[1] for t in tx] + [i[1] for i in ims] + [r.y0 for r in dr]
    ye = [t[3] for t in tx] + [i[3] for i in ims] + [r.y1 for r in dr]
    xs = [t[0] for t in tx] + [i[0] for i in ims] + [r.x0 for r in dr]
    xe = [t[2] for t in tx] + [i[2] for i in ims] + [r.x1 for r in dr]
    print(f'p{pg} y[{round(min(ys)) if ys else "-"},{round(max(ye)) if ye else "-"}] x[{round(min(xs)) if xs else "-"},{round(max(xe)) if xe else "-"}] imgs={len(ims)}', ' | '.join(heads))
    if len(ims) <= 6:
        print('     imgs', ims)
