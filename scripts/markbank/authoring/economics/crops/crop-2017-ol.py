"""Render, catalogue and register the 2017 OL figures (idempotent).

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
W = str(Path(__file__).resolve().parents[5])
OUT = f'{W}/public/exam-figures/economics/markbank'
SCALE = 4
ATTR = 'SEC Leaving Certificate Economics 2017 Ordinary Level — © State Examinations Commission'
LIG = {'Ɵ': 'ti', 'Ŧ': 'ti', 'Ʃ': 'tt', 'ﬀ': 'ff', 'ﬁ': 'fi', 'ﬂ': 'fl'}
F = [
 ('scheme', 5, [75, 415, 562, 580], 'p05-q2-graph', '2017 OL Section A Q2(i)', True,
  'The marking scheme’s completed graph: € Costs on the vertical axis and Quantity (Units) 1 to 4 on the horizontal. '
  'A horizontal line at €3,000, labelled Fixed Costs, runs across from the costs axis.'),
 ('scheme', 7, [395, 362, 548, 484], 'p07-q7-diagram', '2017 OL Section A Q7(i)', True,
  'The marking scheme’s completed diagram: P on the vertical axis and Q on the horizontal. The demand curve D slopes down '
  'from left to right, and a second downward-sloping curve D1 lies to its right.'),
 ('scheme', 9, [30, 125, 505, 392], 'p09-q1a-diagram', '2017 OL Section B Q1(a)(ii)', True,
  'The marking scheme’s completed monopoly diagram: P/C against Q, a falling AR line, a steeper falling MR line, a U-shaped '
  'AC curve and an MC curve rising through G, where MC meets MR above Q1. From Q1 a line rises to AR, and arrows run left '
  'from AR to P1 and from AC to C1 on the vertical axis, C1 below P1.'),
 ('scheme', 13, [55, 330, 580, 660], 'p13-q2b-graph', '2017 OL Section B Q2(b)', True,
  'The marking scheme’s completed graph: Price € 400 to 800 against Quantity (units) 400 to 1,200. Demand D falls through '
  'five points from (400, 800) to (1,200, 400); supply S rises through five points from (400, 400) to (1,200, 800). They '
  'cross at a price of 600, marked P1 on the price axis, and a quantity of 800, marked Q1 on the quantity axis.'),
 ('scheme', 21, [250, 262, 560, 370], 'p21-q5aii-working', '2017 OL Section B Q5(a)(ii)', True,
  'The marking scheme’s working: 1 over MPS + MPM; then 1 over 0.15 + 0.25, the 1 marked with a raised 2 and each of 0.15 '
  'and 0.25 with a raised 3; then 2.5, marked with a raised 2; 10 marks.'),
 ('scheme', 21, [215, 425, 470, 452], 'p21-q5aiii-working', '2017 OL Section B Q5(a)(iii)', True,
  'The marking scheme’s working: €10 million x 2.5 = €25 million, each of the three figures marked with a raised 2.'),
 ('scheme', 24, [70, 183, 400, 228], 'p24-q6ai-working', '2017 OL Section B Q6(a)(i)', True,
  'The marking scheme’s working: Current budget surplus: €53,245m minus €50,548m = €2,697m. The two figures and the minus '
  'sign each carry a raised 1, and the answer a raised 2.'),
 ('scheme', 28, [75, 490, 420, 578], 'p28-q7aiii-working', '2017 OL Section B Q7(a)(iii)', True,
  'The marking scheme’s working: New visible exports: €22,000m + €2,000m = €24,000m; New Balance of Trade: €24,000m - '
  '€23,500m = €500m, each of the six figures marked with a raised 1; It is a surplus, marked with a raised 2.'),
 ('paper', 2, [62, 118, 562, 232], 'p02-q1-table', '2017 OL Section A Q1', False, 'DATA'),
 ('paper', 2, [62, 330, 562, 372], 'p02-q2-table', '2017 OL Section A Q2', False, 'DATA'),
 ('paper', 3, [62, 288, 562, 466], 'p03-q4-table', '2017 OL Section A Q4', False, 'DATA'),
 ('paper', 4, [418, 70, 562, 190], 'p04-q7-diagram', '2017 OL Section A Q7', False, 'DATA'),
 ('paper', 4, [55, 505, 565, 668], 'p04-q9-diagram', '2017 OL Section A Q9', False, 'DATA'),
 ('paper', 5, [36, 188, 510, 466], 'p05-q1-diagram', '2017 OL Section B Q1(a)', False, 'DATA'),
 ('paper', 6, [120, 236, 515, 352], 'p06-q2b-table', '2017 OL Section B Q2(b)', False, 'DATA'),
 ('paper', 6, [262, 538, 360, 578], 'p06-q2c-formula', '2017 OL Section B Q2(c)', False, 'DATA'),
 ('paper', 8, [228, 62, 312, 100], 'p08-q5a-formula', '2017 OL Section B Q5(a)', False, 'DATA'),
 ('paper', 8, [88, 246, 508, 560], 'p08-q5b-diagram', '2017 OL Section B Q5(b)', False, 'DATA'),
 ('paper', 9, [88, 438, 490, 490], 'p09-q7a-table', '2017 OL Section B Q7(a)', False, 'DATA'),
]
QALT = {}
DATA_ALT = {
 'p02-q1-table': 'A table: Tax A VAT, B DIRT, C PAYE, D Customs duty; Explanation 1 A tax on income, 2 A tax on goods imported '
                 'into a country, 3 A tax on the profit made on disposal of an asset, 4 A tax on interest earned on deposits in '
                 'financial institutions, 5 A tax on purchases of goods and services.',
 'p02-q2-table': 'A table: Quantity (units of output) 1, 2, 3, 4; Fixed costs in € 3,000, 3,000, 3,000, 3,000.',
 'p03-q4-table': 'A table to tick: four statements, each with a box under Visible exports, Invisible exports, Visible imports '
                 'and Invisible imports. The statements: Expenditure of Irish soccer supporters having travelled to Austria; '
                 'Irish firms selling cheese in Germany; Foreign tourists using Ryanair to travel to Ireland; Irish consumers '
                 'buying cars in the UK and bringing them back to Ireland.',
 'p04-q7-diagram': 'A diagram with P on the vertical axis and Q on the horizontal: one demand curve D sloping down from left to right.',
 'p04-q9-diagram': 'A diagram with P on the vertical axis and Q on the horizontal: line 1 rises steeply, line 2 is U-shaped and '
                   'line 3 is horizontal at P1; lines 1 and 2 meet on line 3 above Q1. Beside it an answer box: Number 1, 2, 3 '
                   'and a blank Full label column.',
 'p05-q1-diagram': 'A diagram with P on the vertical axis and Q on the horizontal: a falling AR line, a steeper falling MR line, '
                   'a U-shaped AC curve and an MC curve rising through point G, where MC meets MR above Q1. A vertical line '
                   'runs from Q1 up to AR. The labels P, MC, AC, AR, MR and Q are underlined.',
 'p06-q2b-table': 'A table: Price € 400, 500, 600, 700, 800; Quantity Demanded (units) 1,200, 1,000, 800, 600, 400; Quantity '
                  'Supplied (units) 400, 600, 800, 1,000, 1,200.',
 'p06-q2c-formula': 'The printed formula: ∆Q over ∆Y, times Y1 + Y2 over Q1 + Q2.',
 'p08-q5a-formula': 'The printed formula: 1 over MPS + MPM.',
 'p08-q5b-diagram': 'A circular flow diagram: Households and Firms joined by arrows labelled Supply factors of production, '
                    'Supply goods and services and Spending on goods and services; an arrow from Firms to Households numbered '
                    '1; from Households an arrow numbered 2 to Financial Institutions, and from there Investments to Firms; '
                    'from Households Imports to Foreign Markets, and from Foreign Markets an arrow numbered 3 to Firms.',
 'p09-q7a-table': 'A table: Visible Exports €m 22,000; Visible Imports €m 23,500.',
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
    key = f'economics-2017-OL-{kind}-{slug}'
    fname = key + '.png'
    src = f'paper-trail-corpus/{"markingschemes" if kind == "scheme" else "exampapers"}/2017/LC034GLP000EV.pdf'
    with fitz.open(f'{W}/{src}') as doc:
        pg = doc[page - 1]
        pg.get_pixmap(matrix=fitz.Matrix(SCALE, SCALE), clip=fitz.Rect(*rect)).save(f'{OUT}/{fname}')
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
    entry.update({'lettersVisible': [], 'labelMeanings': [], 'questionRef': ref, 'year': 2017,
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
