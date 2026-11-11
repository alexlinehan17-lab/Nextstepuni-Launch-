"""Render, catalogue and register the 2015 HL figures (idempotent).

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
ATTR = 'SEC Leaving Certificate Economics 2015 Higher Level — © State Examinations Commission'
LIG = {'Ɵ': 'ti', 'Ŧ': 'ti', 'Ʃ': 'tt', 'ﬀ': 'ff', 'ﬁ': 'fi', 'ﬂ': 'fl'}
F = [
 ('scheme', 5, [110, 340, 470, 405], 'p05-q2b-working', '2015 HL Section A Q2(b)', True,
  'The marking scheme’s working: MU of water over its price equals MU of bagels over theirs; 5 over €2.50 = x over €3; '
  'x = 6 utils (the marginal utility of the 8th bagel).'),
 ('scheme', 9, [70, 370, 560, 675], 'p09-q1ai-graph', '2015 HL Section B Q1(a)(i)', True,
  'The marking scheme’s graph: Price € 0 to 1,000 against Quantity 10 to 120. The demand curve D/C falls through five '
  'points from (20, 1,000) to (120, 200); the supply curve S/C rises through five points from (20, 200) to (120, 1,000). '
  'They cross at a price of 600, marked PE, and a quantity of 50, marked QE.'),
 ('scheme', 10, [195, 485, 395, 625], 'p10-q1bi-diagram', '2015 HL Section B Q1(b)(i)', True,
  'The marking scheme’s diagram: P against Qty, a demand curve D and a supply curve S1 crossing at X; a new supply curve '
  'S2 to the left, with an arrow pointing left, crosses D at Y. The price rises from PE1 to PE2 and the quantity falls from '
  'QE1 to QE2.'),
 ('scheme', 11, [100, 90, 420, 255], 'p11-q1bii-diagram', '2015 HL Section B Q1(b)(ii)', True,
  'The marking scheme’s diagram: P against Qty, a supply curve S and a demand curve D1; a new demand curve D2 to the left, '
  'with an arrow pointing left. The price falls from PE1 to PE2 and the quantity falls from QE1 to QE2.'),
 ('scheme', 11, [100, 450, 420, 640], 'p11-q1biii-diagram', '2015 HL Section B Q1(b)(iii)', True,
  'The marking scheme’s diagram: P against Qty, a demand curve D and a supply curve S1; a new supply curve S2 to the right, '
  'with an arrow pointing right. The price falls from PE1 to PE2 and the quantity rises from QE1 to QE2.'),
 ('scheme', 14, [30, 118, 520, 400], 'p14-q2aii-diagram', '2015 HL Section B Q2(a)(ii)', True,
  'The marking scheme’s monopoly diagram: Price against Quantity, a falling AR line and a steeper MR line, a U-shaped AC '
  'curve and an MC curve rising through E, where MC meets MR above Q1. From Q1 a line rises to B on AR, marked P1, and to D '
  'on AC, marked C1; the hatched rectangle P1 B D C1 is labelled SNP.'),
 ('scheme', 18, [75, 170, 590, 215], 'p18-q3bi-working', '2015 HL Section B Q3(b)(i)', True,
  'The marking scheme’s working: Average cost of 400 loaves = Total cost over Total output = €360 over 400 = €0.90 per '
  'loaf, 3 marks.'),
 ('scheme', 18, [55, 292, 560, 535], 'p18-q3bii-graph', '2015 HL Section B Q3(b)(ii)', True,
  'The marking scheme’s graph, Total Costs: Costs 0 to 900 against Quantity 0 to 700. FC is a horizontal line at 100; TC '
  'rises from 100 through 200, 280, 330, 360, 450 and 600 to 770; VC rises from 0 below TC, the same distance below it '
  'throughout, to 670.'),
 ('scheme', 30, [30, 115, 570, 440], 'p30-q7ai-diagram', '2015 HL Section B Q7(a)(i)', True,
  'The marking scheme’s circular flow of income for an open economy: Households (Incomes) and Firms (Output) joined by '
  'Incomes for supplying F.O.P’s and Spending on the output of firms; from Households, Tax to Government, Savings to '
  'Financial Institutions and Imports to Foreign Markets; and to Firms, Government Expenditure, Investment and Exports.'),
 ('paper', 5, [120, 250, 485, 425], 'p05-q1a-table', '2015 HL Section B Q1(a)', False, 'DATA'),
 ('paper', 6, [210, 395, 400, 535], 'p06-q3b-table', '2015 HL Section B Q3(b)', False, 'DATA'),
]
MASK = {}
QALT = {}
DATA_ALT = {
 'p05-q1a-table': 'A table: Price (€) 1,000, 800, 600, 400, 200; Quantity Demanded (’000 units) 20, 30, 50, 80, 120; Quantity '
                  'Supplied (’000 units) 120, 80, 50, 30, 20.',
 'p06-q3b-table': 'A table: Units of Bread 0 to 700 in hundreds; Total Costs (€) 100, 200, 280, 330, 360, 450, 600, 770.',
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
    key = f'economics-2015-HL-{kind}-{slug}'
    fname = key + '.png'
    src = f'paper-trail-corpus/{"markingschemes" if kind == "scheme" else "exampapers"}/2015/LC034ALP000EV.pdf'
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
    entry.update({'lettersVisible': [], 'labelMeanings': [], 'questionRef': ref, 'year': 2015,
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
