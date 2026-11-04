"""Render, catalogue and register the 2019 HL figures (idempotent).

Solution crops come from the scheme and wait for the reveal; question crops are
the whole printed question (stem, data and ask) for cards whose figure slot
holds a solution, because a question crop replaces the typed ask. Data crops
show the paper's own table or diagram. Each crop was rendered at 2x and looked
at before its description was written. Manifest entries are APPENDED as raw text.
"""
from pathlib import Path
import hashlib, json, re, sys
import fitz
W = str(Path(__file__).resolve().parents[5])
OUT = f'{W}/public/exam-figures/economics/markbank'
SCALE = 4
ATTR = 'SEC Leaving Certificate Economics 2019 Higher Level — © State Examinations Commission'
LIG = {'Ɵ': 'ti', 'Ŧ': 'ti', 'Ʃ': 'tt', 'ﬀ': 'ff', 'ﬁ': 'fi', 'ﬂ': 'fl'}
F = [
 ('scheme', 6, [78, 236, 350, 328], 'p06-q1b-working', '2019 HL Section A Q1(b)', True,
  'The marking scheme’s working set as fractions: MU of A over P of A equals MU of O over P of O; then 9 over '
  '0.90 equals MU of O over 0.50; then 0.50 times 9, over 0.90, equals MU of O; MU of O = 5 utils.'),
 ('scheme', 6, [98, 403, 482, 552], 'p06-q2-ticks', '2019 HL Section A Q2', True,
  'The marking scheme’s completed table: four numbered statements with TRUE and FALSE columns. Ticks: 1 TRUE '
  '(the demand for labour is a derived demand), 2 FALSE (the Live Register is the most accurate measure of '
  'Ireland’s unemployment rate), 3 TRUE (cyclical unemployment is caused by a recession), 4 TRUE (the backward '
  'bending labour supply curve).'),
 ('scheme', 7, [80, 420, 482, 722], 'p07-q5-diagram', '2019 HL Section A Q5', True,
  'The marking scheme’s answer: a table labelling line 1 Marginal Cost, 2 Average Cost, 3 Marginal Revenue and '
  '4 Demand / Average Revenue, over the completed diagram, Price on the vertical axis and Quantity on the '
  'horizontal. A dashed line from the point where line 4 touches the U-shaped average cost curve 2 meets the '
  'vertical axis at P1/C1, and a dashed line down from it meets the horizontal axis at Q1, directly above the '
  'point where marginal cost 1 crosses marginal revenue 3.'),
 ('scheme', 11, [100, 120, 455, 330], 'p11-q1bi-diagram', '2019 HL Section B Q1(b)(i)', True,
  'The marking scheme’s diagram: Price against Quantity, a downward-sloping demand curve D1 and two upward-sloping '
  'supply curves, S1 and S2 to its left, with arrows pointing left. The equilibrium moves from P1, Q1 to a higher '
  'price P2 and a lower quantity Q2, with an upward arrow beside the price axis.'),
 ('scheme', 12, [100, 60, 455, 272], 'p12-q1bii-diagram', '2019 HL Section B Q1(b)(ii)', True,
  'The marking scheme’s diagram: Price against Quantity, an upward-sloping supply curve S1 and two downward-sloping '
  'demand curves, D1 and D2 to its left, with arrows pointing left. The equilibrium moves from P1, Q1 to a lower '
  'price P2 and a lower quantity Q2, with a downward arrow beside the price axis.'),
 ('scheme', 12, [100, 420, 460, 636], 'p12-q1biii-diagram', '2019 HL Section B Q1(b)(iii)', True,
  'The marking scheme’s diagram: Price against Quantity, a downward-sloping demand curve D1 and two upward-sloping '
  'supply curves, S1 and S2 to its right, with arrows pointing right. The equilibrium moves from P1, Q1 to a lower '
  'price P2 and a higher quantity Q2, with a downward arrow beside the price axis.'),
 ('scheme', 15, [70, 98, 505, 372], 'p15-q2bi-diagram', '2019 HL Section B Q2(b)(i)', True,
  'The marking scheme’s completed diagram: Price against Quantity, a downward-sloping D=AR line, a steeper MR line '
  'below it, a U-shaped AC curve and an MC curve rising through the lowest point of AC. MC crosses MR at E; a dashed '
  'line up from E meets AC at Y and D=AR at X, and down to Q1 on the quantity axis. Dashed lines from X and Y meet '
  'the price axis at P1 and C1, and the rectangle between them is labelled SNP. Beneath it a row of eleven cells '
  'reads Price axis, Quantity axis, D=AR, MR, MC, AC, Equilibrium Point E, P1, Q1, C1, SNPs.'),
 ('scheme', 18, [65, 305, 497, 580], 'p18-q3bii-diagrams', '2019 HL Section B Q3(b)(ii)', True,
  'The marking scheme’s two diagrams. Diagram 1: Inelastic Demand, a steep demand line D on which a fall in price '
  'from P1 to P2 raises quantity only a little, from Q1 to Q2. Diagram 2: Elastic Demand, a flat demand line D on '
  'which a small fall in price from P1 to P2 raises quantity a lot, from Q1 to Q2.'),
 ('scheme', 19, [65, 269, 500, 382], 'p19-q3ci-working', '2019 HL Section B Q3(c)(i)', True,
  'The marking scheme’s working set as fractions: the change in quantity of X over the change in the tablet’s '
  'price, times the sum of the tablet prices over the sum of the quantities of X; then -15,000 over -150, times '
  '500 + 350 (850) over 10,000 + 25,000 (35,000), equals + 2.42857 = + 2.43.'),
 ('scheme', 32, [65, 188, 435, 281], 'p32-q7biii-working', '2019 HL Section B Q7(b)(iii)', True,
  'The marking scheme’s two workings set as fractions. Left: 1 over (1-MPC) + MPM + MPT, then 1 over (1-0.6) + 0.2 '
  '+ 0.2 = 1.25. Right: 1 over MPS + MPM + MPT, then 1 over 0.4 + 0.2 + 0.2 = 1.25.'),
 ('paper', 2, [52, 389, 545, 580], 'p02-q2-question', '2019 HL Section A Q2', False, None),
 ('paper', 3, [52, 268, 553, 590], 'p03-q5-question', '2019 HL Section A Q5', False, None),
 ('paper', 6, [118, 412, 541, 600], 'p06-q1c-diagram', '2019 HL Section B Q1(c)', False, 'DATA'),
 ('paper', 8, [109, 210, 499, 398], 'p08-q4b-table', '2019 HL Section B Q4(b)', False, 'DATA'),
 ('paper', 9, [105, 472, 490, 582], 'p09-q6a-table', '2019 HL Section B Q6(a)(iii)', False, 'DATA'),
 ('paper', 10, [111, 151, 540, 235], 'p10-q7b-table', '2019 HL Section B Q7(b)', False, 'DATA'),
 ('paper', 10, [80, 128, 545, 370], 'p10-q7b-question', '2019 HL Section B Q7(b)', False, None),
]
QALT = {
 'p02-q2-question': 'A table of four numbered statements with TRUE and FALSE tick columns, both blank.',
 'p03-q5-question': 'Beside the parts, a diagram with Price on the vertical axis and Quantity on the horizontal, '
                    'four unlabelled lines numbered 1 to 4 (two U-shaped curves and two downward-sloping lines), '
                    'and an answer box with Number 1 to 4 and a blank Label column.',
 'p10-q7b-question': 'A table of five rows: MPC 0.6, MPM 0.2, MPT 0.2, the current equilibrium level of national '
                     'income €100 bn and the level that would give full employment €150 bn.',
}
DATA_ALT = {
 'p06-q1c-diagram': 'A diagram with Price on the vertical axis and Quantity (’000s properties) on the horizontal, '
                    'marked 200, 400 and 600. An upward-sloping Supply line and a downward-sloping Demand line cross '
                    'at PE and 400. A horizontal line at PMax, below PE, is labelled Rent Control / Price Ceiling; it '
                    'meets Supply at 200 and Demand at 600.',
 'p08-q4b-table': 'A table headed Quantity of output (units), Average Variable Cost (AVC) and Average Fixed Cost '
                  '(AFC). Output 0: blank. 1: 200 and 600. 2: 150 and 300. 3: 158.33 and 200. 4: 187.5 and 150. '
                  '5: 240 and 120. 6: 300 and 100.',
 'p09-q6a-table': 'A table headed Consumer Price Index (CPI) and Wage Inflation in Ireland, with columns Year, CPI '
                  'Annual % Change, Nominal Wage Rate Annual % Change and Real Wage Rate Annual % Change. 2014: 0.3, '
                  '-0.2, ?. 2015: - 0.3, 1.2, ?. 2016: 0.0, 1.1, ?.',
 'p10-q7b-table': 'A table of five rows: Marginal propensity to consume (MPC) 0.6; Marginal propensity to import '
                  '(MPM) 0.2; Marginal propensity to pay tax (MPT) 0.2; Current equilibrium level of National Income '
                  '€100 bn; Level of National Income that would give full employment €150 bn.',
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
    key = f'economics-2019-HL-{kind}-{slug}'
    fname = key + '.png'
    src = f'paper-trail-corpus/{"markingschemes" if kind == "scheme" else "exampapers"}/2019/LC034ALP000EV.pdf'
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
    entry.update({'lettersVisible': [], 'labelMeanings': [], 'questionRef': ref, 'year': 2019,
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
