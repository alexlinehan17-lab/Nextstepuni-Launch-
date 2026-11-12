"""Render, catalogue and register the 2017 HL figures (idempotent).

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
ATTR = 'SEC Leaving Certificate Economics 2017 Higher Level — © State Examinations Commission'
LIG = {'Ɵ': 'ti', 'Ŧ': 'ti', 'Ʃ': 'tt', 'ﬀ': 'ff', 'ﬁ': 'fi', 'ﬂ': 'fl'}
F = [
 ('scheme', 5, [33, 350, 563, 478], 'p05-q2-ticks', '2017 HL Section A Q2', True,
  'The marking scheme’s completed table of four statements with TRUE and FALSE columns. Ticks: the labour force '
  'includes part-time workers, TRUE; quasi-rent is economic rent earned in the long run, FALSE; an existing bond’s '
  'market value rises if the rate of interest falls, TRUE; capital widening, TRUE.'),
 ('scheme', 6, [52, 500, 563, 700], 'p06-q6-diagram', '2017 HL Section A Q6', True,
  'The marking scheme’s completed diagram and explanation: Price / Costs against Quantity, a downward-sloping AR line, '
  'a steeper MR line, a U-shaped AC curve and an MC curve. MC crosses MR above Q1; dashed lines meet the price axis at '
  'P1 on AR and C1 on AC, and the area between them is marked SNP. Beside it: (i) Equilibrium is where MC = MR; (ii) '
  'Firms produces Q1 and sells it at P1; (iii) Costs are shown at C1; (iv) SNPs are being earned as AR > AC / barriers '
  'to entry exist, or the firm is not efficient as it is not producing at the lowest point of AC.'),
 ('scheme', 7, [150, 128, 450, 222], 'p07-q7a-working', '2017 HL Section A Q7(a)', True,
  'The marking scheme’s working set as fractions: 40 over −10, times 100 + 90 (190) over 80 + 120 (200); = −4 x 0.95; '
  '= −3.8.'),
 ('scheme', 10, [34, 50, 450, 200], 'p10-q1bi-diagram', '2017 HL Section B Q1(b)(i)', True,
  'The marking scheme’s diagram: P against Quantity, a downward-sloping demand line D and two upward-sloping supply '
  'lines, S1 and S2 to its right, with a bold arrow pointing right. The equilibrium moves from P1, Q1 to a lower price '
  'P2 and a higher quantity Q2, with a downward arrow beside the price axis and a right arrow under the quantity axis.'),
 ('scheme', 10, [34, 410, 450, 560], 'p10-q1bii-diagram', '2017 HL Section B Q1(b)(ii)', True,
  'The marking scheme’s diagram: P against Quantity, an upward-sloping supply line S and two downward-sloping demand '
  'lines, D1 and D2 to its right, with a bold arrow pointing right. The equilibrium moves from P1, Q1 to a higher price '
  'P2 and a higher quantity Q2, with an upward arrow beside the price axis.'),
 ('scheme', 11, [34, 45, 450, 200], 'p11-q1biii-diagram', '2017 HL Section B Q1(b)(iii)', True,
  'The marking scheme’s diagram: P against Quantity, an upward-sloping supply line S and two downward-sloping demand '
  'lines, D1 and D2 to its left, with a bold arrow pointing left. The equilibrium moves from P1, Q1 to a lower price P2 '
  'and a lower quantity Q2, with a downward arrow beside the price axis.'),
 ('scheme', 11, [34, 505, 545, 745], 'p11-q1ci-diagram', '2017 HL Section B Q1(c)(i)', True,
  'The marking scheme’s diagram: P/Rent against Q, a rising Supply line and a falling Demand line crossing at €1,078 '
  'and QE. A bold line at €715 marks the maximum rent / price ceiling; it meets Supply at S1 and Demand at D1, and the '
  'gap between them is the excess demand (D1 minus S1).'),
 ('scheme', 13, [34, 128, 545, 736], 'p13-q2ai-diagrams', '2017 HL Section B Q2(a)(i)', True,
  'The marking scheme’s two diagrams. Short run: Price / Cost against Quantity (units), a horizontal D = AR = MR line at '
  'P1, a U-shaped AC curve below it and an MC curve rising through A on the line; dashed lines show C1 on AC and Q1 below '
  'A, so the firm earns supernormal profit. Long run: the price line falls from P1 (MR1, AR1) to P2 / C2 (MR2 = AR2), '
  'which just touches the lowest point of AC at A, where MC crosses; output falls from Q1 to Q2.'),
 ('scheme', 16, [34, 400, 565, 778], 'p16-q3aiv-graph', '2017 HL Section B Q3(a)(iv)', True,
  'The marking scheme’s completed table and graph. Output 0 to 6,000; Total Cost 5,000 to 60,000; Average Cost -, 13, 9, '
  '8, 8, 9, 10; Marginal Cost -, 8, 5, 6, 8, 13, 15. The graph plots Costs from 0 to 16 against Quantity / Output / '
  'Units: AC falls from 13 to 8 and rises to 10; MC falls from 8 to 5 and rises to 15, crossing AC at its lowest point. '
  'Beneath it: Points on AC curve: 6m; Points on MC curve: 6m; Labels of Axes; Costs / Quantity / MC / AC: 4 at 1 mark.'),
 ('scheme', 17, [34, 450, 562, 620], 'p17-q3ci-diagram', '2017 HL Section B Q3(c)(i)', True,
  'The marking scheme’s diagram: MRP / Wage (€) against Quantity of labour / No. of workers, a downward-sloping line '
  'labelled MRPL = DL. A wage W on the vertical axis meets the line, and a line down from that point meets the '
  'horizontal axis at QL.'),
 ('scheme', 20, [34, 150, 565, 478], 'p20-q4bi-diagram', '2017 HL Section B Q4(b)(i)', True,
  'The marking scheme’s circular flow diagram: HOUSEHOLDS (Incomes) and FIRMS (Output), with Incomes for supplying '
  'F.O.P’s from firms to households and Spending on the output of firms from households to firms. From households, Tax '
  'runs to GOVERNMENT, Savings to FINANCIAL INSTITUTIONS and Imports to FOREIGN MARKETS; from these, Government '
  'Expenditure, Investment and Exports run back to firms.'),
 ('paper', 2, [60, 317, 562, 466], 'p02-q2-table', '2017 HL Section A Q2', False, 'DATA'),
 ('paper', 3, [88, 540, 302, 732], 'p03-q6-diagram', '2017 HL Section A Q6', False, 'DATA'),
 ('paper', 5, [105, 597, 540, 635], 'p05-q2b-table', '2017 HL Section B Q2(b)', False, 'DATA'),
 ('paper', 6, [108, 110, 535, 147], 'p06-q3a-table', '2017 HL Section B Q3(a)', False, 'DATA'),
 ('paper', 7, [115, 292, 548, 374], 'p07-q5c-table', '2017 HL Section B Q5(c)', False, 'DATA'),
 ('paper', 8, [108, 425, 512, 473], 'p08-q8a-table', '2017 HL Section B Q8(a)', False, 'DATA'),
]
QALT = {}
DATA_ALT = {
 'p02-q2-table': 'A table of four statements with blank TRUE and FALSE columns: The labour force includes part-time '
                 'workers; Quasi-rent is economic rent earned by a factor of production in the long run; The market value '
                 'of an existing bond rises if the rate of interest falls; Capital Widening refers to the situation where '
                 'the capital stock is increasing at the same rate as the labour force.',
 'p03-q6-diagram': 'A diagram with Price / Cost on the vertical axis and Quantity on the horizontal: four unlabelled lines '
                   'and curves apart from a U-shaped curve labelled AC, two lines falling from the left and a curve rising '
                   'steeply through the lowest part of AC.',
 'p05-q2b-table': 'A table: Average Revenue (€) 50; Average Variable Cost (€) 40; Average Total Cost (€) 60.',
 'p06-q3a-table': 'A table: Output (units) 0, 1,000, 2,000, 3,000, 4,000, 5,000, 6,000; Total Cost (€) 5,000, 13,000, '
                  '18,000, 24,000, 32,000, 45,000, 60,000.',
 'p07-q5c-table': 'A table with columns Year, Index of Export prices, Index of Import prices and Terms of Trade. 2010: 100, '
                  '100, 100. 2011: 96.6, 98.7, ?. 2015: 106.8, 100.3, 106.5.',
 'p08-q8a-table': 'A table: Population (2011) 4,588,252; Population (2016) 4,757,976; Natural Increase (2011-2016) 198,282; '
                  'Net Migration ?.',
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
    key = f'economics-2017-HL-{kind}-{slug}'
    fname = key + '.png'
    src = f'paper-trail-corpus/{"markingschemes" if kind == "scheme" else "exampapers"}/2017/LC034ALP000EV.pdf'
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
