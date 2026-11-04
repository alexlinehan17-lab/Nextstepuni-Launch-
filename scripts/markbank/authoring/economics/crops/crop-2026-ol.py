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
ATTR = 'SEC Leaving Certificate Economics 2026 Ordinary Level — © State Examinations Commission'
F = [
 ('scheme', 17, [130, 258, 480, 484], 'p17-q11bii-price-and-cost', '2026 OL Q11(b)(ii)', True, [],
  'Official monopoly diagram completed for the answer. MC (yellow), AC (green), AR (red) and MR (blue) on Price and Quantity axes. Above output Q1, the dashed line meets MR and MC at E, AC at C1 and AR higher up; dashed guides from C1 and from the AR point read AC1 and P1 on the price axis, with P1 above AC1.'),
 ('scheme', 35, [115, 672, 458, 772], 'p35-q15biii-cost-and-profit', '2026 OL Q15(b)(iii)', True, [],
  'Official working in two columns. Total cost: €5,000, €25,000, €2,000 and €3,000 summed to €35,000. Profit: €100,000 minus €35,000 equals €65,000.'),
 ('paper', 8, [56, 300, 548, 472], 'p08-q7-canons-table', '2026 OL Section A Q7', False, [],
  'The question\'s two tables. Canons A Convenience, B Certainty, C Economy, D Equity beside explanations 1 to 4: 1 the system should take a higher proportion of income in tax as income rises / the ability of each person to pay must be considered; 2 tax should be levied at a convenient time and manner for the taxpayer; 3 the amount paid should be clear and straightforward; 4 the revenue collected should be greater than the cost of collection. The answer table has A completed as 2 and B, C and D blank.'),
 ('paper', 9, [64, 112, 532, 380], 'p09-q9-employment-growth', '2026 OL Section A Q9', False, [],
  'Bar chart titled Percentage growth in Ireland\'s employment 2023 – 2025, percentage growth for each half year: 2023H1 3.9%, 2023H2 3.5%, 2024H1 2.3%, 2024H2 3.1%, 2025H1 2.8%.'),
 ('paper', 10, [64, 112, 548, 348], 'p10-q10-expenditure', '2026 OL Section A Q10(i)', False, [],
  'Bar chart titled Government Expenditure for 2025 in €billion: Social Protection 27, Health 25, Housing 8, Education 12, Transport 4, Justice 4, EU Payments 15, Other 25.'),
 ('paper', 12, [140, 78, 486, 312], 'p12-q11b-monopoly-diagram', '2026 OL Q11(b)(i)', False, [],
  'The question\'s monopoly diagram with Price and Quantity axes: a downward red AR line, a steeper blue MR line, a yellow MC curve rising through E where it meets MR, and a green U-shaped AC curve. A dashed line drops from E to output Q1.'),
 ('paper', 13, [122, 110, 514, 346], 'p13-q11c-supermarket-shares', '2026 OL Q11(c)(i)', False, [],
  'Pie chart titled Recent percentage share of the main supermarkets in Ireland: Dunnes Stores 23.9%, Tesco 23.7%, SuperValu 19.5%, Lidl 14.2%, Aldi 11.6%, Other 7.1%.'),
 ('paper', 17, [128, 88, 503, 317], 'p17-q13a-corporation-tax', '2026 OL Q13(a)(ii)', False, [],
  'Bar chart titled Ireland\'s Corporation Tax Receipts 2018 – 2024 €billion: 2018 10.4, 2019 10.9, 2020 11.8, 2021 15.3, 2022 22.6, 2023 23.8, 2024 28.1.'),
 ('paper', 20, [64, 112, 532, 402], 'p20-q14-cpi-inflation', '2026 OL Q14(a)(ii)', False, [],
  'Line chart titled Rate of price inflation in Ireland from the CPI, annual % change from September 2024 to September 2025: 0.7% in September 2024, rising to about 1.9% in January 2025 and about 2.2% in April, dipping to about 1.7%, then rising to 2.7% in September 2025.'),
 ('paper', 21, [226, 520, 351, 616], 'p21-q14biii-modified-domestic-demand', '2026 OL Q14(b)(iii)', False, [],
  'Two bars showing growth in Modified Domestic Demand: 2024 2.7% and 2025 2.0%.'),
]
cat_path = f'{W}/scripts/markbank/authored/economics-completion-figures.json'
cat = json.load(open(cat_path))
_order = {c['file']: i for i, c in enumerate(cat)}
man_path = f'{W}/components/MarkBank/figures.json'
man_text = open(man_path).read()
man = json.loads(man_text)
add_entries = []
for kind, page, rect, slug, ref, solution, meanings, alt in F:
    key = f'economics-2026-OL-{kind}-{slug}'
    fname = key + '.png'
    src = f'paper-trail-corpus/{"markingschemes" if kind == "scheme" else "exampapers"}/2026/LC034GLP000EV.pdf'
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
                  'questionRef': ref, 'year': 2026, 'level': 'ordinary', 'attribution': ATTR})
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
