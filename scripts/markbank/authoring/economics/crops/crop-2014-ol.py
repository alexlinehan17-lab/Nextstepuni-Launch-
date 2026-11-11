"""Render, catalogue and register the 2014 OL figures (idempotent).

Solution crops come from the scheme and wait for the reveal. Data crops show
the paper's own table or diagram: as the figure beneath the typed ask, or, on a
card whose figure slot holds the solution, as its question figure with the typed
ask kept (econ_legacy_lib.beside_ask). No crop here is a whole printed question:
set at phone width a whole old-syllabus question's text falls near 8 px, so each
crop is the part the ask needs (coordinator rule, 2026-11-04). Each crop was rendered at 2x and looked
at before its description was written. Manifest entries are APPENDED as raw text.

One crop blanks the text printed beside its print (MASK): the paper's A Q9 formula
sits at the end of its stem's line, above the ask's own line, so both lines are
blanked and the formula and the table are left untouched.
"""
from pathlib import Path
import hashlib, json, re, sys
import fitz
from PIL import Image, ImageDraw
W = str(Path(__file__).resolve().parents[5])
OUT = f'{W}/public/exam-figures/economics/markbank'
SCALE = 4
ATTR = 'SEC Leaving Certificate Economics 2014 Ordinary Level — © State Examinations Commission'
LIG = {'Ɵ': 'ti', 'Ŧ': 'ti', 'Ʃ': 'tt', 'ﬀ': 'ff', 'ﬁ': 'fi', 'ﬂ': 'fl'}
F = [
 ('scheme', 6, [55, 112, 562, 190], 'p06-q5-working', '2014 OL Section A Q5', True,
  'The marking scheme’s answer table. Workings: Y = C + I + G + X – M; Y = €3,200m + €500m - €400m. Answer: €3,300m.'),
 ('scheme', 9, [24, 96, 500, 380], 'p09-q1a-diagram', '2014 OL Section B Q1(a)(ii)', True,
  'The marking scheme’s completed diagram: P against Quantity, a falling AR line, a steeper MR line, a U-shaped AC curve '
  'and an MC curve rising through E, where it cuts MR. A vertical line from Q1 rises through E to AC and AR; arrows run '
  'left from AC to C1 and from AR to P1 on the price axis.'),
 ('paper', 3, [120, 508, 370, 622], 'p03-q6-diagram', '2014 OL Section A Q6', False, 'DATA'),
 ('paper', 4, [55, 524, 562, 752], 'p04-q9-table', '2014 OL Section A Q9', False, 'DATA'),
 ('paper', 5, [24, 210, 500, 490], 'p05-q1-diagram', '2014 OL Section B Q1(a)', False, 'DATA'),
 ('paper', 6, [92, 214, 345, 390], 'p06-q2b-diagram', '2014 OL Section B Q2(b)', False, 'DATA'),
]
MASK = {
 'p04-q9-table': [(55, 524, 456, 557), (55, 557.5, 476, 572)],   # the stem's line and the ask's line
}
QALT = {}
DATA_ALT = {
 'p03-q6-diagram': 'A diagram: Wage Rate on the vertical axis and Quantity of labour on the horizontal. The supply curve '
                   'S runs horizontally at W1 and then rises.',
 'p04-q9-table': 'The printed formula, ∆Q over ∆P times P1 + P2 over Q1 + Q2, and a table of its six symbols: ∆Q, P1, P2 '
                 'and Q2 blank; ∆P Change in the price of the good; Q1 Original quantity demanded of the good.',
 'p05-q1-diagram': 'A diagram with P on the vertical axis and Quantity on the horizontal: a falling AR line, a steeper MR '
                   'line, a U-shaped AC curve and an MC curve rising through E, where it cuts MR. A vertical line rises '
                   'from Q1 through E to dots on AC and AR. The labels P, MC, AC, AR and MR are circled.',
 'p06-q2b-diagram': 'A diagram: P against Q, a falling line D1 and a parallel falling line D2 to its right, with an arrow '
                    'pointing from D1 to D2.',
}

def tidy(s):
    for a, b in LIG.items():
        s = s.replace(a, b)
    s = re.sub(r'_{3,}', ' ', s.replace('', '✓'))
    return re.sub(r'\s+', ' ', s).strip()


cat_path = f'{W}/scripts/markbank/authored/economics-completion-figures.json'
cat = json.load(open(cat_path))
_order = {c['file']: i for i, c in enumerate(cat)}
man_path = f'{W}/components/MarkBank/figures.json'
man_text = open(man_path).read()
man = json.loads(man_text)
add_entries = []
for kind, page, rect, slug, ref, solution, alt in F:
    key = f'economics-2014-OL-{kind}-{slug}'
    fname = key + '.png'
    src = f'paper-trail-corpus/{"markingschemes" if kind == "scheme" else "exampapers"}/2014/LC034GLP000EV.pdf'
    with fitz.open(f'{W}/{src}') as doc:
        pg = doc[page - 1]
        pg.get_pixmap(matrix=fitz.Matrix(SCALE, SCALE), clip=fitz.Rect(*rect)).save(f'{OUT}/{fname}')
        if slug in MASK:
            im = Image.open(f'{OUT}/{fname}').convert('RGB')
            for x0, y0, x1, y1 in MASK[slug]:
                ImageDraw.Draw(im).rectangle([(x0 - rect[0]) * SCALE, (y0 - rect[1]) * SCALE,
                                              (x1 - rect[0]) * SCALE, (y1 - rect[1]) * SCALE], fill='white')
            im.save(f'{OUT}/{fname}')
        if kind == 'paper' and alt == 'DATA':
            alt = DATA_ALT[slug]
        elif kind == 'paper':
            words = tidy(pg.get_text('text', clip=fitz.Rect(*rect)))
            alt = f'The printed question as the paper sets it. {QALT[slug]} The printed text reads: {words}'
    md5 = hashlib.md5(open(f'{OUT}/{fname}', 'rb').read()).hexdigest()
    cat = [c for c in cat if c['file'] != fname]
    cat.append({'file': fname, 'kind': 'figure', 'truncated': False, 'drawingComplete': True,
                'solution': solution, 'questionRef': ref, 'description': alt,
                'source': {'file': src, 'page': page, 'rectPoints': rect, 'scale': SCALE},
                'lettersVisible': [], 'labelMeanings': []})
    entry = {'src': f'/exam-figures/economics/markbank/{fname}', 'md5': md5, 'alt': alt}
    if solution:
        entry['solution'] = True
    entry.update({'lettersVisible': [], 'labelMeanings': [], 'questionRef': ref, 'year': 2014,
                  'level': 'ordinary', 'attribution': ATTR})
    if key in man:
        if man[key] != entry:
            sys.exit(f'{key} already registered with different content — remove it by hand first')
        continue
    add_entries.append((key, entry))
cat.sort(key=lambda c: _order.get(c['file'], len(_order)))
json.dump(cat, open(cat_path, 'w'), ensure_ascii=False, indent=2)
open(cat_path, 'a').write('\n')
if add_entries:
    body = man_text.rstrip()
    assert body.endswith('}')
    chunks = [json.dumps({k: e}, ensure_ascii=False, indent=2)[1:-1].strip('\n') for k, e in add_entries]
    body = body[:-1].rstrip() + ',\n' + ',\n'.join(chunks) + '\n}\n'
    json.loads(body)
    open(man_path, 'w').write(body)
print(len(F), 'figures;', len(add_entries), 'manifest entries appended')
