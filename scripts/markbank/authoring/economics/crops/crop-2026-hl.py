"""Render, catalogue and register the 2026 HL figures (one-off; idempotent).

Each crop was inspected at 2x in the scratchpad before this run. Catalogue
entries record source page/rect/scale; manifest entries are APPENDED to
components/MarkBank/figures.json as raw text so no existing entry is reformatted.
"""
from pathlib import Path
import hashlib, json, os, re, sys
import fitz
W = str(Path(__file__).resolve().parents[5])
OUT = f'{W}/public/exam-figures/economics/markbank'
SCALE = 4
ATTR = 'SEC Leaving Certificate Economics 2026 Higher Level — © State Examinations Commission'
F = [
 ('scheme', 31, [88, 138, 522, 442], 'p31-q11bi-short-run-equilibrium', '2026 HL Q11(b)(i)', True, [],
  'Official short-run equilibrium of a firm in monopolistic competition, with Price / Costs and Quantity axes. MC (green) cuts MR (red) from below at E, giving output Q1. At Q1 the demand curve AR = D (yellow) gives price P1 at point P and the U-shaped AC (blue) gives average cost C1 at point C; the shaded rectangle between P1 and C1 is labelled SNPs (supernormal profits). W marks minimum AC, to the right of Q1.'),
 ('scheme', 33, [140, 138, 460, 336], 'p33-q11ci-yed-working', '2026 HL Q11(c)(i) — calculation', True, [],
  'Official midpoint income-elasticity working with both fraction bars intact: ΔQ/ΔY × (Y1 + Y2)/(Q1 + Q2), then +1/+100 × (400 + 500)/(2 + 3). Answer: +1.8.'),
 ('scheme', 42, [100, 290, 500, 462], 'p42-q12ci-oil-share-working', '2026 HL Q12(c)(i) — calculation', True, [],
  'Official working: top three producers 22.7m (US) + 10.7m (Saudi Arabia) + 10.5m (Russia) = 43.9m barrels a day; total world production 102.8m barrels a day; share = 43.9m/102.8m × 100 = 0.427 × 100. Answer: 42.7%.'),
 ('scheme', 50, [96, 98, 508, 372], 'p50-q13bii-cost-curves', '2026 HL Q13(b)(ii)', True, [],
  'Official total cost diagram drawn on a grid. The Costs (€) axis is marked 100 to 900 and the Quantity axis 0, 10, 20, 30 and 40. TFC is a horizontal red line at 300. TVC (blue) rises from 0 through 120, 210 and 360 to 600. TC (yellow) rises from 300 through 420, 510 and 660 to 900, always 300 above TVC.'),
 ('scheme', 64, [140, 138, 452, 360], 'p64-q14ci-demand-shift', '2026 HL Q14(c)(i)', True, [],
  'Official diagram: demand shifts right from D to D2 (arrows) along the unchanged upward-sloping supply curve S. The equilibrium price rises from Pe to Pe2 and the quantity rises from Qe to Qe2. Price and Quantity axes are labelled.'),
 ('scheme', 65, [148, 48, 452, 262], 'p65-q14cii-supply-shift', '2026 HL Q14(c)(ii)', True, [],
  'Official diagram: supply shifts right from S to S2 (arrows) along the unchanged demand curve D. The equilibrium price falls from Pe to Pe2 and the quantity rises from Qe to Qe2. Price and Quantity axes are labelled.'),
 ('scheme', 65, [148, 424, 452, 646], 'p65-q14ciii-supply-shift', '2026 HL Q14(c)(iii)', True, [],
  'Official diagram: supply shifts left from S to S2 (arrows) along the unchanged demand curve D. The equilibrium price rises from Pe to Pe2 and the quantity falls from Qe to Qe2. Price and Quantity axes are labelled; the word Explanation beneath the axis is the scheme heading for the written answer.'),
 ('scheme', 76, [120, 198, 485, 392], 'p76-q16ai-hotel-rooms', '2026 HL Q16(a)(i)', True, [],
  'Official diagram: the supply of hotel rooms S is vertical at Qe. Demand shifts right from D to D2 (arrows), moving equilibrium from E to E2: the price rises from Pe to Pe2 while the quantity of rooms per night stays at Qe.'),
 ('scheme', 78, [250, 336, 370, 410], 'p78-q16bi-france-share-working', '2026 HL Q16(b)(i)', True, [],
  'Official working with both fraction bars intact: 32,500/654,500 × 100/1. Answer: 4.96%.'),
 ('scheme', 81, [98, 95, 502, 336], 'p81-q16cii-ppf-shift', '2026 HL Q16(c)(ii)', True, [],
  'Official PPF diagram with Tobacco leaf on the vertical axis and Corn on the horizontal. A new frontier PPF2 is drawn inside the original PPF1; point B stays on PPF1 and point A, at QTL and QC, lies inside both curves.'),
 ('paper', 36, [88, 360, 522, 598], 'p36-q16c-ppf', '2026 HL Q16(c)(i)', False,
  [{'label': 'A', 'meaning': 'the blue point inside PPF1'}, {'label': 'B', 'meaning': 'the red point on PPF1'}],
  'The question\'s production possibility frontier PPF1 for Malawi, with Tobacco leaf on the vertical axis and Corn on the horizontal. A red point B lies on the curve; a blue point A lies inside it, with dashed guides to QTL on the tobacco-leaf axis and QC on the corn axis.'),

 # Question-side crops: the paper's own charts, tables and starting diagrams.
 ('paper', 5, [148, 110, 448, 290], 'p05-q3-fan-costs', '2026 HL Section A Q3(a)', False, [],
  'The question\'s cost table for following Cork and Tipperary to the 2025 All-Ireland hurling final, under the two county crests. Cork / item / Tipperary: Match Tickets €350 / €400; Match Programmes €38 / €43; Petrol €200 / €200; Tolls €23 / €27; Parking in Dublin €50 / €50; Food and drink €334 / €350; TOTAL €995 / €1,070.'),
 ('paper', 6, [80, 406, 515, 628], 'p06-q4-tshirt-price', '2026 HL Section A Q4(a)', False, [],
  'Pie chart titled Retail Price Breakdown of a T-Shirt Sold in Europe for €29: Workers in Bangladesh Receive Less Than 1%. Other costs are €28.82, 99.4%, of the pie; worker pay is a thin green slice, €0.18, 0.6%.'),
 ('paper', 10, [68, 395, 497, 560], 'p10-q7b-kuznets-curve', '2026 HL Section A Q7(b)', False, [],
  'The question\'s Environmental Kuznets Curve, with Damage to the environment on the vertical axis and Real GDP / Real income per head on the horizontal. A green inverted-U curve rises from the origin to a red dot labelled Turning point, then falls back towards the axis.'),
 ('paper', 12, [55, 112, 540, 318], 'p12-q9-gdp-charts', '2026 HL Section A Q9(a)', False, [],
  'Two bar charts of the GDP of the EU and the USA in current US dollars (trillions), each on a 0 to 35 axis. 2008: EU $16.4tn, USA $14.8tn. 2024: EU $19.4tn, USA $29.2tn.'),
 ('paper', 13, [104, 112, 472, 299], 'p13-q10-consumer-prices', '2026 HL Section A Q10(a)', False, [],
  'Bar chart titled Consumer Prices in Europe 2024 (Index, EU = 100), with a dashed reference line at 100 for the EU average: Ireland 138.1, Sweden 115.1, Bulgaria 59.7, Euro Area countries 104.3.'),
 ('paper', 14, [97, 170, 499, 374], 'p14-q11-sport-participation', '2026 HL Q11(a)(i)', False, [],
  'Bar chart titled Sports Participation in Ireland by Age, 2023 and 2024: 16-24 year-olds 71% then 73%; 25-44 year-olds 54% then 56%; 45-64 year-olds 40% then 40%; 65+ year-olds 28% then 31%.'),
 ('paper', 18, [61, 111, 534, 331], 'p18-q12-goods-trade', '2026 HL Q12(a)(i)', False, [],
  'Bar chart titled Value of Ireland\'s Total Goods Exports & Goods Imports, May 2024 and May 2025 (€ million). May 2024: exports €18,039, imports €11,041. May 2025: exports €23,333, imports €10,745.'),
 ('paper', 20, [109, 74, 486, 287], 'p20-q12c-oil-producers', '2026 HL Q12(c)(i)', False, [],
  'Graphic titled The World\'s Eight Largest Oil Producers, production of petroleum and other liquids in 2024 in million barrels per day: United States 22.7, Saudi Arabia 10.7, Russia 10.5, Canada 6.0, China 5.3, Iran 4.7, Iraq 4.5, Brazil 4.3. Total World Production: 102.8 million barrels.'),
 ('paper', 22, [96, 110, 499, 348], 'p22-q13-ecb-rate', '2026 HL Q13(a)(i)', False, [],
  'Step chart titled ECB Main Refinancing Rate (Base Rate), January 2024 - June 2025, on a 0% to 5% axis. The rate holds at 4.50% until June 2024, then steps down through 4.25%, 3.65%, 3.40%, 3.15%, 2.90%, 2.65% and 2.40% to 2.15% in June 2025. A red arrow under the months runs from June 2024 to June 2025.'),
 ('paper', 23, [83, 102, 541, 242], 'p23-q13b-surf-school-costs', '2026 HL Q13(b)(i)', False, [],
  'The question\'s cost table for the surf school. Daily output (number of lessons) / total fixed costs / total variable costs / total costs (€): 0 / 300 / 0 / 300; 10 / 300 / 120 / 420; 20 / 300 / 210 / 510; 30 / 300 / 360 / 660; 40 / 300 / 600 / 900.'),
 ('paper', 27, [60, 95, 524, 359], 'p27-q14b-circular-flow', '2026 HL Q14(b)(i)', False, [],
  'The question\'s circular flow of income in an open economy. A dotted flow, Income for supplying the factors of production, runs from Output of Firms to Household Incomes, and a dotted flow numbered 1 runs back from households to firms. Red leakages leave households: Tax to GOVERNMENT, a flow numbered 2 to FINANCIAL INSTITUTIONS, and Imports to a blank box numbered 3. Green injections return to firms: Government Spending, Investment, and a flow numbered 4 from box 3.'),
 ('paper', 30, [106, 105, 489, 299], 'p30-q15-budget-composition', '2026 HL Q15(a)(i)', False, [],
  'Donut chart titled Budget 2026, Composition of Government Expenditure: Current Expenditure 84% and Capital Expenditure 16%.'),
 ('paper', 32, [192, 92, 403, 253], 'p32-q15c-labour-productivity', '2026 HL Q15(c)(i)', False, [],
  'Graphic headed Labour Productivity beside a group of illustrated workers: Foreign Sector €411 per hour; Domestic Sector €60 per hour.'),
 ('paper', 34, [130, 122, 470, 305], 'p34-q16a-hotel-rooms', '2026 HL Q16(a)(i)', False, [],
  'The question\'s market for hotel rooms per night: a vertical supply curve S and a downward-sloping demand curve D meet at E, giving price Pe and quantity Qe. Price is on the vertical axis and Quantity of rooms per night on the horizontal.'),
 ('paper', 35, [117, 90, 478, 294], 'p35-q16b-visitors', '2026 HL Q16(b)(i)', False, [],
  'Horizontal bar chart titled Foreign Visitors to Ireland By Country, June 2025: Other 157,700; Italy 19,200; France 32,500 (highlighted in red); Germany 54,800; USA 166,300; Britain 224,000. The axis runs from 0 to 250,000, with illustrated travellers behind the bars.'),
]
cat_path = f'{W}/scripts/markbank/authored/economics-completion-figures.json'
cat = json.load(open(cat_path))
_order = {c['file']: i for i, c in enumerate(cat)}
man_path = f'{W}/components/MarkBank/figures.json'
man_text = open(man_path).read()
man = json.loads(man_text)
add_entries = []
for kind, page, rect, slug, ref, solution, meanings, alt in F:
    key = f'economics-2026-HL-{kind}-{slug}'
    fname = key + '.png'
    src = f'paper-trail-corpus/{"markingschemes" if kind == "scheme" else "exampapers"}/2026/LC034ALP000EV.pdf'
    with fitz.open(f'{W}/{src}') as doc:
        doc[page - 1].get_pixmap(matrix=fitz.Matrix(SCALE, SCALE), clip=fitz.Rect(*rect)).save(f'{OUT}/{fname}')
    md5 = hashlib.md5(open(f'{OUT}/{fname}', 'rb').read()).hexdigest()
    cat = [c for c in cat if c['file'] != fname]
    cat.append({'file': fname, 'kind': 'figure', 'truncated': False, 'drawingComplete': True,
                'solution': solution, 'questionRef': ref, 'description': alt,
                'source': {'file': src, 'page': page, 'rectPoints': rect, 'scale': SCALE},
                'lettersVisible': [m['label'] for m in meanings], 'labelMeanings': meanings})
    entry = {'src': f'/exam-figures/economics/markbank/{fname}', 'md5': md5, 'alt': alt}
    if solution:
        entry['solution'] = True
    entry.update({'lettersVisible': [m['label'] for m in meanings], 'labelMeanings': meanings,
                  'questionRef': ref, 'year': 2026, 'level': 'higher', 'attribution': ATTR})
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
    chunks = []
    for key, entry in add_entries:
        txt = json.dumps({key: entry}, ensure_ascii=False, indent=2)[1:-1].strip('\n')
        chunks.append(txt)
    body = body[:-1].rstrip() + ',\n' + ',\n'.join(chunks) + '\n}\n'
    json.loads(body)
    open(man_path, 'w').write(body)
print(len(F), 'figures;', len(add_entries), 'manifest entries appended')
