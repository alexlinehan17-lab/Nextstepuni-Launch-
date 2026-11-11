"""Render, catalogue and register the 2011 OL figures (idempotent).

Solution crops come from the scheme and wait for the reveal. Data crops show
the paper's own table or diagram: as the figure beneath the typed ask, or, on a
card whose figure slot holds the solution, as its question figure with the typed
ask kept (econ_legacy_lib.beside_ask). No crop here is a whole printed question:
set at phone width a whole old-syllabus question's text falls near 8 px, so each
crop is the part the ask needs (coordinator rule, 2026-11-04). Each crop was rendered at 2x and looked
at before its description was written. Manifest entries are APPENDED as raw text.

"""
from pathlib import Path
import hashlib, json, re, sys
import fitz
from PIL import Image, ImageDraw
W = str(Path(__file__).resolve().parents[5])
OUT = f'{W}/public/exam-figures/economics/markbank'
SCALE = 4
ATTR = 'SEC Leaving Certificate Economics 2011 Ordinary Level — © State Examinations Commission'
LIG = {'Ɵ': 'ti', 'Ŧ': 'ti', 'Ʃ': 'tt', 'ﬀ': 'ff', 'ﬁ': 'fi', 'ﬂ': 'fl'}
F = [
 ('scheme', 5, [28, 95, 330, 272], 'p05-q4-diagram', '2011 OL Section A Q4(b)', True,
  'The marking scheme’s diagram: lines 1 to 5 as the paper numbers them, with a line dropped from where the rising curve 2 '
  'cuts the lowest point of the U-shaped curve 3, on the horizontal line 4, down to the axis 5.'),
 ('scheme', 6, [130, 605, 540, 680], 'p06-q9-working', '2011 OL Section A Q9', True,
  'The marking scheme’s working: Y = C + I + G + X – M; Y = €2,400m + €300m - €200m. Answer: €2,500 m.'),
 ('scheme', 7, [110, 125, 380, 322], 'p07-q1a-diagram', '2011 OL Section B Q1(a)(ii)', True,
  'The marking scheme’s monopoly diagram: P against Q, a falling AR line and a steeper MR line, a U-shaped AC curve and an '
  'MC curve rising through MR. A line rises from the output where MC cuts MR to the AC curve and on to AR; arrows run left '
  'to C1 from the AC curve and to P1 from AR.'),
 ('scheme', 11, [60, 335, 580, 658], 'p11-q2a-graph', '2011 OL Section B Q2(a)(i)–(iii)', True,
  'The marking scheme’s graph: Price € against Quantity (units), a D/C falling through the five points of the schedule '
  'from (200, 5) to (600, 1) and an S/C rising from (200, 1) to (600, 5). They cross at 3 and 400, marked PE on the price '
  'axis and QE on the quantity axis.'),
 ('scheme', 17, [40, 600, 490, 656], 'p17-q4aii-working', '2011 OL Section B Q4(a)(ii)', True,
  'The marking scheme’s working: Visible Exports = €24,000m; Less: Visible Imports: €23,600m + €600m = €24,200m; (€200m).'),
 ('paper', 2, [30, 605, 562, 798], 'p02-q4-diagram', '2011 OL Section A Q4', False, 'DATA'),
 ('paper', 4, [140, 170, 420, 362], 'p04-q1-diagram', '2011 OL Section B Q1(a)', False, 'DATA'),
 ('paper', 5, [140, 124, 460, 229], 'p05-q2-table', '2011 OL Section B Q2', False, 'DATA'),
 ('paper', 6, [60, 429, 560, 478], 'p06-q4-table', '2011 OL Section B Q4(a)', False, 'DATA'),
]
# The question's own "(16 marks)" sits inside the answer box's rectangle.
MASK = {'p02-q4-diagram': [(496, 756, 562, 778)]}
QALT = {}
DATA_ALT = {
 'p02-q4-diagram': 'A diagram of a firm in perfect competition with five numbered lines: 1 the vertical axis, 2 a curve rising '
                   'steeply, 3 a U-shaped curve, 4 a horizontal line touching the bottom of the U where curve 2 cuts it, and 5 the '
                   'horizontal axis; beside it an answer box numbered 1 to 5 with a column for each name.',
 'p04-q1-diagram': 'A monopoly diagram: P against Q, a falling AR line, a steeper falling MR line, a U-shaped AC curve and an MC '
                   'curve rising through MR; a line from Q1 rises through the point where MC cuts MR to AC and AR.',
 'p05-q2-table': 'A table of the umbrella market: at €1.00, 600 demanded and 200 supplied; €2.00, 500 and 300; €3.00, 400 and 400; '
                 '€4.00, 300 and 500; €5.00, 200 and 600.',
 'p06-q4-table': 'A table of a country’s trade in € million: Visible Exports 24,000, Visible Imports 23,600, Balance of Trade 400, '
                 'Surplus.',
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
    key = f'economics-2011-OL-{kind}-{slug}'
    fname = key + '.png'
    src = f'paper-trail-corpus/{"markingschemes" if kind == "scheme" else "exampapers"}/2011/LC034GLP000EV.pdf'
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
    entry.update({'lettersVisible': [], 'labelMeanings': [], 'questionRef': ref, 'year': 2011,
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
