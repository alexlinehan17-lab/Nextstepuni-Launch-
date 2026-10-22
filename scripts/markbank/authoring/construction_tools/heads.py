"""Headings and image boxes per scheme page: heads.py PDF first last"""
import sys, re, fitz
d = fitz.open(sys.argv[1])
pat = re.compile(r'^(Ceist|CEIST|Question|QUESTION|Q\.?\s?\d|\(?[a-e]\)|Part|[0-9]+\s?\([a-e]\))', re.I)
for pg in range(int(sys.argv[2]), int(sys.argv[3]) + 1):
    p = d[pg - 1]; out = []
    for b in p.get_text('dict')['blocks']:
        for l in b.get('lines', []):
            t = ''.join(s['text'] for s in l['spans']).strip()
            bold = any('Bold' in s['font'] for s in l['spans'])
            if t and l['bbox'][1] > 48 and (pat.match(t) or (bold and len(t) > 3)):
                out.append(f"{round(l['bbox'][1])}:{t[:30]}")
    ims = sorted([[round(v) for v in im['bbox']] for im in p.get_image_info() if im['bbox'][3] - im['bbox'][1] > 8 and im['bbox'][2]-im['bbox'][0] > 8], key=lambda b: b[1])
    ys = [b for b in ims]
    print(pg, ' | '.join(out[:14]))
    if ims: print('    imgs y-ranges', [(b[1], b[3]) for b in ims][:12])
