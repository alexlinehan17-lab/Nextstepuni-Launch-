"""Render, catalogue and register the 2012 HL figures (idempotent).

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
ATTR = 'SEC Leaving Certificate Economics 2012 Higher Level — © State Examinations Commission'
LIG = {'Ɵ': 'ti', 'Ŧ': 'ti', 'Ʃ': 'tt', 'ﬀ': 'ff', 'ﬁ': 'fi', 'ﬂ': 'fl'}
F = [
 ('scheme', 6, [60, 397, 540, 500], 'p06-q4-ticks', '2012 HL Section A Q4', True,
  'The marking scheme’s completed table: a tick for Repetitive tasks, workers are bored under (b) Diseconomy of Scale, '
  'Internal; for R&D costs are shared by many firms under (a) Economy of Scale, External; for Discounts are available for '
  'bulk buying under (a) Economy of Scale, Internal; and for Inadequate infrastructure under (b) Diseconomy of Scale, External.'),
 ('scheme', 7, [40, 176, 540, 343], 'p07-q6i-working', '2012 HL Section A Q6(i)', True,
  'The marking scheme’s working for the MPS, two ways. Savings = Y – C: Year 1 €24,000 – €15,000 = €9,000, Year 2 '
  '€34,000 – €22,000 = €12,000, so MPS = €3,000 over €10,000 = 0.3 or 30%. Or the MPC: the rise in C €7,000 over the '
  'rise in Y €10,000 = 0.7 or 70%, and MPS = 1 – 0.7 = 0.3.'),
 ('scheme', 7, [40, 385, 540, 690], 'p07-q6ii-working', '2012 HL Section A Q6(ii)', True,
  'The marking scheme’s working for the multiplier. Increase in imports: €12,000 – €7,000 = €5,000; MPM = €5,000 over '
  '€10,000 = 0.5 or 50%. Method 1: 1 over (MPS + MPM) = 1 over (0.3 + 0.5) = 1 over 0.8 = 1.25. Method 2: MPC = 1 – MPS '
  '= 0.7, then 1 over (1 – (MPC – MPM)) = 1 over (1 – (0.7 – 0.5)) = 1 over 0.8 = 1.25.'),
 ('scheme', 11, [30, 196, 560, 620], 'p11-q1b-table', '2012 HL Section B Q1(b)', True,
  'The marking scheme’s table for the three products. Product A (-2.8): decrease price; elastic; the % rise in demand '
  'exceeds the % fall in price; total revenue will increase. Product B (-1.0): leave price unchanged; unit elastic; the % '
  'changes in demand and price are equal; revenue unchanged. Product C (-0.5): increase price; inelastic; the % rise in '
  'price exceeds the % fall in demand; revenue will increase. Beneath each, its demand curve: shallow for A, at 45 degrees '
  'for B, steep for C, each marked with the old and new price and quantity; 10 marks each.'),
 ('scheme', 14, [60, 155, 590, 440], 'p14-q2bi-diagram', '2012 HL Section B Q2(b)(i)', True,
  'The marking scheme’s diagram: P against Q, a horizontal D = AR = MR line at P1, a U-shaped AC curve and an MC curve '
  'rising through it. MC cuts D = AR = MR at A; a line from A drops to Q1, passing B on the AC curve below.'),
 ('scheme', 15, [28, 130, 575, 380], 'p15-q2bii-diagrams', '2012 HL Section B Q2(b)(ii)', True,
  'The marking scheme’s two diagrams. Market: P against Q, a falling D, supply shifting right from S1 to S2 (an arrow), '
  'the price falling from P1 to P2 (an arrow down). Firm: P against Q, the new D = AR = MR line at P2 touching the lowest '
  'point of the U-shaped AC curve at E, where MC crosses it; a line drops from E to Q2.'),
 ('scheme', 21, [28, 118, 560, 325], 'p21-q4ai-diagram', '2012 HL Section B Q4(a)(i)', True,
  'The marking scheme’s diagram: C against Q, a U-shaped LRAC curve and a smaller U-shaped SRAC curve touching it from '
  'above near its left end.'),
 ('scheme', 21, [28, 503, 440, 675], 'p21-q4aii-diagram', '2012 HL Section B Q4(a)(ii)', True,
  'The marking scheme’s diagram: C against Q, a U-shaped AC curve and an MC curve that falls, turns and rises steeply, '
  'cutting AC at its lowest point.'),
 ('scheme', 23, [125, 245, 395, 346], 'p23-q4ci-working', '2012 HL Section B Q4(c)(i)', True,
  'The marking scheme’s short-run working in euro: Raw Materials 2,000; Labour 1,600; Total variable costs 3,600, over 2; '
  'Minimum price per boat 1,800.'),
 ('scheme', 23, [125, 510, 395, 642], 'p23-q4cii-working', '2012 HL Section B Q4(c)(ii)', True,
  'The marking scheme’s long-run working in euro: Raw Materials 2,000; Labour 1,600; Rent 1,200; Normal profit 1,000; '
  'Total costs 5,800, over 2; Minimum price per boat 2,900.'),
 ('scheme', 32, [28, 450, 560, 688], 'p32-q7aiii-working', '2012 HL Section B Q7(a)(iii)', True,
  'The marking scheme’s working. UK: 1 unit of Food is the equivalent of 0.25 units of clothing; 1 unit of Clothing of 4 '
  'units of food. China: 1 unit of Food is the equivalent of 0.33 units of clothing; 1 item of Clothing of 3 units of food. '
  'So the possible terms of trade for FOOD lie between 0.25 and 0.3 units of clothing, and for CLOTHING between 4 and 3 '
  'units of food.'),
 ('paper', 2, [70, 483, 560, 594], 'p02-q4-table', '2012 HL Section A Q4', False, 'DATA'),
 ('paper', 3, [70, 47, 545, 97], 'p03-q6-table', '2012 HL Section A Q6', False, 'DATA'),
 ('paper', 6, [68, 117, 552, 178], 'p06-q5a-table', '2012 HL Section B Q5(a)', False, 'DATA'),
 ('paper', 7, [100, 86, 450, 178], 'p07-q7a-table', '2012 HL Section B Q7(a)', False, 'DATA'),
]
MASK = {}
QALT = {}
DATA_ALT = {
 'p02-q4-table': 'A table to tick: four statements (Repetitive tasks, workers are bored; R&D costs are shared by many firms; '
                 'Discounts are available for bulk buying; Inadequate infrastructure) against (a) Economy of Scale, Internal '
                 'and External, and (b) Diseconomy of Scale, Internal and External.',
 'p03-q6-table': 'A table: Year 1, National Income €24,000, Consumption €15,000, Investment €6,000, Exports €10,000, Imports '
                 '€7,000; Year 2, National Income €34,000, Consumption €22,000, Investment €8,000, Exports €16,000, Imports '
                 '€12,000.',
 'p06-q5a-table': 'A table: world population of 1 to 7 billion reached in 1804, 1927, 1960, 1974, 1987, 1999 and 2012, the '
                  'years elapsed between them -, 123, 33, 14, 13, 12 and 13.',
 'p07-q7a-table': 'A table of output per worker per week: United Kingdom, Food 40 units and Clothing 10 units; China, Food 60 '
                  'units and Clothing 20 units; Total Output, Food 100 units and Clothing 30 units.',
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
    key = f'economics-2012-HL-{kind}-{slug}'
    fname = key + '.png'
    src = f'paper-trail-corpus/{"markingschemes" if kind == "scheme" else "exampapers"}/2012/LC034ALP000EV.pdf'
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
    entry.update({'lettersVisible': [], 'labelMeanings': [], 'questionRef': ref, 'year': 2012,
                  'level': 'higher', 'attribution': ATTR})
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
