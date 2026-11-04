"""Render, catalogue and register the 2022 HL deferred-sitting figures (idempotent).

The deferred paper and scheme are filed under deferredexams/ and
deferredmarkingschemes/ with the June file id; every key here says
"deferred" ("economics-2022-HL-deferred-paper-p03-q1-chart"), so no crop can
be mistaken for June's. Solution crops come from the scheme and wait for the
reveal. Data crops show the paper's own chart, table or diagram: as the figure
beneath the typed ask, or, on a card whose figure slot holds the solution, as
its question figure with the typed ask kept (econ_legacy_lib.beside_ask). Each
crop starts just below the sentence printed above it and stops above the next
printed line or answer box; every one was rendered and looked at before its
description was written. Manifest entries are APPENDED as raw text.
"""
from pathlib import Path
import hashlib, json, sys
import fitz
W = str(Path(__file__).resolve().parents[5])
OUT = f'{W}/public/exam-figures/economics/markbank'
SCALE = 4
ATTR = ('SEC Leaving Certificate Economics 2022 Higher Level, deferred examination — '
        '© State Examinations Commission')
D = ' — Deferred sitting'
F = [
 ('paper', 3, [55, 159, 545, 353.7], 'p03-q1-chart', '2022 HL Section A Q1' + D, False,
  'A bar chart titled FOREIGN DIRECT INVESTMENT INTO IRELAND: eight bars against YEARS from 2008 to 2020 on '
  'the vertical axis, labelled along the horizontal axis € TRILLONS 0.3, 0.031, 0.38, 0.815, 0.805, 0.885, '
  '1.05 and 1.1, each bar taller than the one before. Adapted from cso.ie.'),
 ('paper', 4, [55, 134.6, 545, 378], 'p04-q2a-diagram', '2022 HL Section A Q2(a)' + D, False,
  'Two axes with no labels: a falling line and a rising line crossing in the middle.'),
 ('paper', 5, [55, 105.3, 545, 208.5], 'p05-q3-table', '2022 HL Section A Q3' + D, False,
  'A table with the columns Year, Income (€) and Mobile Phones (Units): 2020, 60,000 and 150; 2021, 65,000 '
  'and 275.'),
 ('paper', 9, [55, 222.4, 545, 734], 'p09-q6b-table', '2022 HL Section A Q6(b)' + D, False,
  'A table of Description and Value: Adjustments, including factor income of redomiciled companies, '
  'depreciation on R&D imports and trade in IP, and depreciation on aircraft leasing, €75.6bn; EU subsidies '
  '€1.5bn; EU taxes €0.4bn; Net factor income from abroad - €90.2bn. Then the question’s sentence: given that '
  'GDP at current market prices is €372bn, calculate ANY TWO of A, B or C, stating the relationships and '
  'showing all workings. Then an answer grid, Adjustments/Relationships and Answer € bn’s: Gross Domestic '
  'Product at Current Market Price, ANS: €372bn; space for workings and an empty answer for A, Gross '
  'National Product (GNP) at Current Market Prices; B, Gross National Income at Current Market Prices; '
  'and C, Modified Gross National Income at Current Market Prices.'),
 ('paper', 12, [55, 93.7, 545, 254.2], 'p12-q9-table', '2022 HL Section A Q9' + D, False,
  'A table with four columns, Quantity of Haircuts, Average Revenue, Total Revenue and Marginal Revenue: '
  '15 at €21, 18 at €19, 22 at €17 and 28 at €15. The Total Revenue and Marginal Revenue cells are empty, '
  'and the first Marginal Revenue cell is blacked out.'),
 ('paper', 14, [55, 87.7, 545, 308.3], 'p14-q10-chart', '2022 HL Section A Q10' + D, False,
  'A line chart titled Benchmark Interest Rate in Ireland, 2008 - 2020, Interest Rate % from 0 to 4.5 '
  'against the years 2008 to 2020. The line starts above 4 in 2008, falls to 1 in 2009, stays at 1 in 2010, '
  'rises to 1.5 in 2011, then falls through about 0.75 in 2012 and 0.5 in 2013 to near 0 by 2015, and stays '
  'at 0 to 2020. Adapted from the ECB.'),
 ('paper', 15, [50, 134.7, 550, 319.4], 'p15-q11-chart', '2022 HL Q11' + D, False,
  'A bar chart titled Government Revenue & Expenditure 2015 - 2020 in € billions, an Income bar and an '
  'Expenditure bar for each year: 2015, 71 and 76.4; 2016, 73.7 and 75.8; 2017, 76.9 and 78.2; 2018, 83.1 '
  'and 83; 2019, 88.1 and 87.1; 2020, 84.5 and 103.3. Adapted from revenue.ie.'),
 ('paper', 16, [55, 87.7, 545, 299.2], 'p16-q11b-pies', '2022 HL Q11(b)' + D, False,
  'Two pie charts. Share of Total Exports by Region: EU27 40%, US 29%, Rest of World 19%, Great Britain '
  '10%, Northern Ireland 2%. Share of Total Imports by Region: EU27 29%, Rest of World 29%, US 20%, Great '
  'Britain 18%, Northern Ireland 4%. Adapted from cso.ie.'),
 ('paper', 19, [55, 117, 545, 351.2], 'p19-q12-pies', '2022 HL Q12(a)' + D, False,
  'Two pie charts. MARKET SHARE 2008 has ten slices: AIB, Bank of Ireland, Permanent TSB, KBC Bank, Ulster '
  'Bank, Bank of Scotland, Anglo Irish Bank, Irish Nationwide Building Society, Danske Bank and ACC Bank. '
  'MARKET SHARE 2021 has four: AIB and Bank of Ireland, the two largest, then Permanent TSB and Others. '
  'Approximate data - adapted from BFI.'),
 ('paper', 23, [55, 102.4, 545, 265.3], 'p23-q13-chart', '2022 HL Q13(a)' + D, False,
  'An infographic titled Unemployment* forecast in Ireland: four bars, 2020 5.9%, 2021 7.3%, 2022 7.2% and '
  '2023 5.9%, footnoted *International Labour Organisation Definition. www.centralbank.ie.'),
 ('paper', 28, [55, 146.4, 545, 401.9], 'p28-q14b-ppf', '2022 HL Q14(b)(i)' + D, False,
  'A production possibility frontier, Mobile Phones (MP) on the vertical axis and Smartwatches (Sw) on the '
  'horizontal, the frontier bowed outwards. Point A sits on it, with dashed lines to MP1 on the vertical '
  'axis and Sw1 on the horizontal; an arrow runs along the horizontal axis from Sw1 to Sw2.'),
 ('paper', 29, [55, 161.0, 545, 437], 'p29-q14bii-ppf', '2022 HL Q14(b)(ii)' + D, False,
  'The same production possibility frontier, Mobile Phones (MP) against Smartwatches (Sw): point A on the '
  'frontier, with dashed lines to MP1 and Sw1.'),
 ('paper', 35, [55, 90.6, 545, 313.8], 'p35-q16-chart', '2022 HL Q16(a)' + D, False,
  'A line chart titled Corporation Tax Receipts 2011 - 2020 in € millions, from 0 to 14,000. The line rises '
  'slowly from about 3,500 in 2011 to about 4,600 in 2014, then more steeply to about 10,400 in 2018 and '
  'about 11,800 in 2020. Adapted from revenue.ie.'),
 ('scheme', 5, [100, 523.2, 505, 739.9], 'p05-q2a-diagram', '2022 HL Section A Q2(a)' + D, True,
  'The marking scheme’s diagram, Price on the vertical axis and Quantity on the horizontal: a falling demand '
  'line D, the original supply line S and a new supply line S2 to its left. E1, where D crosses S, gives P1 '
  'and Q1; E2, where D crosses S2, gives the higher price P2 and the smaller quantity Q2.'),
 ('scheme', 7, [100, 382.2, 505, 606.9], 'p07-q4b-diagram', '2022 HL Section A Q4(b)' + D, True,
  'The marking scheme’s diagram, P on the vertical axis and Q on the horizontal: a vertical supply line S '
  'rising from 82,300 on the quantity axis. S, Q and 82,300 each carry a small 1, the scheme’s mark for '
  'that label.'),
 ('scheme', 12, [100, 59.8, 505, 175.3], 'p12-q9a-table', '2022 HL Section A Q9(a)' + D, True,
  'The marking scheme’s completed table, Quantity, AR, TR and MR: 15, €21, €315, a dash; 18, €19, €342, '
  '€27; 22, €17, €374, €32; 28, €15, €420, €46, the answers in bold.'),
 ('scheme', 16, [86, 58.6, 512, 410.8], 'p16-q11ci-diagram', '2022 HL Q11(c)(i)' + D, True,
  'The marking scheme’s Circular Flow of Income for an open economy: ovals for Households (Incomes) and '
  'Firms (Output) at the top, and Government, Financial Institutions and Foreign Markets beneath. Incomes '
  'for supplying F.O.P’s flow from Firms to Households, and Spending on the output of firms from Households '
  'to Firms. From Households, Tax flows to Government, Savings to Financial Institutions and Imports to '
  'Foreign Markets; from these, Government Expenditure, Investment and Exports flow up to Firms.'),
 ('scheme', 18, [86, 59.8, 512, 395.5], 'p18-q12bi-diagram', '2022 HL Q12(b)(i)' + D, True,
  'The marking scheme’s diagram titled Firm, P on the vertical axis and Q on the horizontal: a U-shaped AC '
  'curve, an MC curve rising through its lowest point E, and a horizontal line D = AR = MR at P2 touching AC '
  'at E, with an arrow dropping from E to Q2. Beneath it a table headed 1 mark per label = 9 marks: Price, '
  'Quantity, P2, Q2, C2, E, D/AR, MC, AC.'),
 ('scheme', 26, [86, 208.9, 512, 461.6], 'p26-q14bi-ppf', '2022 HL Q14(b)(i)' + D, True,
  'The marking scheme’s production possibility frontier, Mobile Phones (MP) against Smartwatches (Sw): point '
  'A at MP1 and Sw1, and point B further down the frontier where Sw2 meets it, with a line across to MP2, '
  'below MP1, on the vertical axis.'),
 ('scheme', 27, [86, 103.9, 512, 379.8], 'p27-q14bii-ppf', '2022 HL Q14(b)(ii)' + D, True,
  'The marking scheme’s production possibility frontier, Mobile Phones (MP) against Smartwatches (Sw): the '
  'original frontier through point A (MP1, Sw1), and a second, thinner frontier inside it, an arrow '
  'pointing inwards to it.'),
 ('scheme', 27, [86, 484.8, 512, 712], 'p27-q14ci-curves', '2022 HL Q14(c)(i)' + D, True,
  'The marking scheme’s diagram, Cost on the vertical axis and output on the horizontal, from 0: a U-shaped '
  'AC curve, and an MC curve that falls, then rises steeply through the lowest point of AC.'),
 ('scheme', 29, [86, 121.9, 512, 380.9], 'p29-q15ai-diagram', '2022 HL Q15(a)(i)' + D, True,
  'The marking scheme’s diagram, Price on the vertical axis and Quantity on the horizontal: a falling '
  'Demand line and a rising Supply line crossing at P* and Q*.'),
 ('scheme', 30, [86, 109.9, 512, 326.7], 'p30-q15bi-diagram', '2022 HL Q15(b)(i)' + D, True,
  'The marking scheme’s diagram, P against Quantity: a supply line S, the original demand line D1 and a new '
  'demand line D2 to its right, an arrow showing the shift. The equilibrium moves from P1 and Q1 to the '
  'higher price P2 and the larger quantity Q2, with arrows showing the price rising and the quantity '
  'growing.'),
 ('scheme', 30, [86, 443.3, 512, 648.2], 'p30-q15bii-diagram', '2022 HL Q15(b)(ii)' + D, True,
  'The marking scheme’s diagram, P against Quantity: a demand line D, the original supply line S1 and a new '
  'supply line S2 to its right, an arrow showing the shift. The equilibrium moves from P1 and Q1 to the '
  'lower price P2 and the larger quantity Q2, with arrows showing the price falling and the quantity '
  'growing.'),
 ('scheme', 34, [86, 491, 512, 770], 'p34-q16bi-diagram', '2022 HL Q16(b)(i)' + D, True,
  'The marking scheme’s diagram, Price on the vertical axis and Quantity on the horizontal: a falling D1 and '
  'a rising S1 crossing at the equilibrium price PE and quantity QE. A horizontal line at Pmin, above PE, '
  'meets D1 at QD and S1 at QS, with dashed lines dropping to each.'),
 ('scheme', 36, [86, 477, 512, 646.9], 'p36-q16ciii-diagram', '2022 HL Q16(c)(iii)' + D, True,
  'The marking scheme’s diagram, Price on the vertical axis and Quantity on the horizontal: a vertical '
  'supply line S and a falling demand line D crossing it at the price P1.'),
]

cat_path = f'{W}/scripts/markbank/authored/economics-completion-figures.json'
cat = json.load(open(cat_path))
_order = {c['file']: i for i, c in enumerate(cat)}
man_path = f'{W}/components/MarkBank/figures.json'
man_text = open(man_path).read()
man = json.loads(man_text)
add_entries = []
for kind, page, rect, slug, ref, solution, alt in F:
    key = f'economics-2022-HL-deferred-{kind}-{slug}'
    fname = key + '.png'
    src = (f'paper-trail-corpus/{"deferredmarkingschemes" if kind == "scheme" else "deferredexams"}'
           '/2022/LC034ALP000EV.pdf')
    with fitz.open(f'{W}/{src}') as doc:
        doc[page - 1].get_pixmap(matrix=fitz.Matrix(SCALE, SCALE), clip=fitz.Rect(*rect)).save(f'{OUT}/{fname}')
    md5 = hashlib.md5(open(f'{OUT}/{fname}', 'rb').read()).hexdigest()
    cat = [c for c in cat if c['file'] != fname]
    cat.append({'file': fname, 'kind': 'figure', 'truncated': False, 'drawingComplete': True,
                'solution': solution, 'questionRef': ref, 'description': alt,
                'source': {'file': src, 'page': page, 'rectPoints': rect, 'scale': SCALE},
                'lettersVisible': [], 'labelMeanings': []})
    entry = {'src': f'/exam-figures/economics/markbank/{fname}', 'md5': md5, 'alt': alt}
    if solution:
        entry['solution'] = True
    entry.update({'lettersVisible': [], 'labelMeanings': [], 'questionRef': ref, 'year': 2022,
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
