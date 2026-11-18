"""Render, catalogue and register the 2013 HL figures (idempotent).

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
ATTR = 'SEC Leaving Certificate Economics 2013 Higher Level — © State Examinations Commission'
LIG = {'Ɵ': 'ti', 'Ŧ': 'ti', 'Ʃ': 'tt', 'ﬀ': 'ff', 'ﬁ': 'fi', 'ﬂ': 'fl'}
F = [
 ('scheme', 7, [60, 543, 288, 640], 'p07-q8-working', '2013 HL Section A Q8', True,
  'The marking scheme’s working: €34,000* - €5,200* = €28,800*; €28,800 over €34,000 = 0.847 or 84.7%, the answer and the '
  'income it is divided by in bold.'),
 ('scheme', 10, [188, 88.5, 374, 229], 'p10-q1bi-diagram', '2013 HL Section B Q1(b)(i)', True,
  'The marking scheme’s diagram: P against Q, a rising S and a falling D1, with D2 to its left and an arrow pointing left. '
  'Arrows run left to P1 and to the lower P2, and down to Q1 and to the lower Q2.'),
 ('scheme', 10, [195, 336.5, 384, 476], 'p10-q1bii-diagram', '2013 HL Section B Q1(b)(ii)', True,
  'The marking scheme’s diagram: P against Q, a falling D and a rising S1, with S2 to its right and an arrow pointing right. '
  'Arrows run left to P1 and to the lower P2, and down to Q1 and to the higher Q2.'),
 ('scheme', 10, [205, 585, 376, 696], 'p10-q1biii-diagram', '2013 HL Section B Q1(b)(iii)', True,
  'The marking scheme’s diagram: P against Q, a rising S and a falling D1, with D2 to its right and an arrow pointing right. '
  'Arrows run left to P1 and to the higher P2, and down to Q1 and to the higher Q2.'),
 ('scheme', 14, [45, 85, 365, 352], 'p14-q2b-diagram', '2013 HL Section B Q2(b)', True,
  'The marking scheme’s diagram: Price against Qty, a falling AR line and a steeper MR line, a U-shaped AC curve and an MC '
  'curve rising through E, where it cuts MR. A line from Q1 rises through E to AC and to B on AR; arrows run left to C1 '
  'and P1 on the price axis.'),
 ('scheme', 17, [40, 108, 525, 688], 'p17-q3b-diagrams', '2013 HL Section B Q3(b)', True,
  'The marking scheme’s two labour market diagrams with their explanations. A free labour market: Wage Rate against Qty. '
  'of labour, S/C labour rising and D/C labour falling, crossing level with WE. A labour market where a trade union has '
  'negotiated a minimum wage: the S/C labour runs horizontally at WMIN and then rises; D/C labour falls through it.'),
 ('scheme', 23, [45, 388, 552, 702], 'p23-q5bi-diagram', '2013 HL Section B Q5(b)(i)', True,
  'The marking scheme’s circular flow of income for an open economy: HOUSEHOLDS (Incomes) and FIRMS (Output), with '
  'Incomes for supplying F.O.P’s from firms to households and Spending on the output of firms from households to firms. '
  'From households: Tax to GOVERNMENT, Savings to FINANCIAL INSTITUTIONS and Imports to FOREIGN MARKETS; to firms: '
  'Government Expenditure, Investment and Exports.'),
 ('scheme', 26, [25, 286, 572, 446], 'p26-q6ai-example', '2013 HL Section B Q6(a)(i)', True,
  'The marking scheme’s formula and numerical example: Increase in credit = Increase in Cash Deposits x 1 over Banks '
  'Reserve Ratio. A person deposits €100 into a bank; the reserve ratio is 10%: €100* x 1* over 10% = €1,000* [- €100 = '
  '€900*], 1 mark per asterisked figure.'),
 ('scheme', 26, [25, 482, 572, 640], 'p26-q6ai-balance-sheets', '2013 HL Section B Q6(a)(i)', True,
  'The marking scheme’s two balance sheets of a bank. The first (4 marks): cash lodged by X 100 against X’s deposit 100. '
  'The second (6 marks): cash lodged by X 100 and a loan of 900, total assets 1,000, against deposits 100 and new '
  'deposits 900, total liabilities 1,000.'),
 ('paper', 3, [296, 333, 542, 374], 'p03-q8-table', '2013 HL Section A Q8', False, 'DATA'),
]
MASK = {}
QALT = {}
DATA_ALT = {
 'p03-q8-table': 'A table: Year 2012; Disposable Income €34,000; Savings €5,200.',
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
    key = f'economics-2013-HL-{kind}-{slug}'
    fname = key + '.png'
    src = f'paper-trail-corpus/{"markingschemes" if kind == "scheme" else "exampapers"}/2013/LC034ALP000EV.pdf'
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
    entry.update({'lettersVisible': [], 'labelMeanings': [], 'questionRef': ref, 'year': 2013,
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
