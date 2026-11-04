"""Render, catalogue and register the 2022 HL review figures (idempotent).

Solution crops come from the scheme and wait for the reveal; question crops are
the whole printed question (stem, data and ask) for cards whose figure slot
holds a solution, because a question crop replaces the typed ask. Each crop was
inspected at 2x before registration. Manifest entries are APPENDED as raw text.
"""
from pathlib import Path
import hashlib, json, re, sys
import fitz
W = str(Path(__file__).resolve().parents[5])
OUT = f'{W}/public/exam-figures/economics/markbank'
SCALE = 4
ATTR = 'SEC Leaving Certificate Economics 2022 Higher Level — © State Examinations Commission'
LIG = {'Ɵ': 'ti', 'Ŧ': 'ti', 'Ʃ': 'tt', 'ﬀ': 'ff', 'ﬁ': 'fi', 'ﬂ': 'fl'}
F = [
 ('paper', 3, [52, 124, 545, 368], 'p03-q1a-question', '2022 HL Section A Q1(a)', False, None),
 ('paper', 3, [54, 186, 539, 367], 'p03-q1-graph', '2022 HL Section A Q1', False, 'DATA'),
 ('paper', 4, [52, 91, 545, 314], 'p04-q2-infographic', '2022 HL Section A Q2', False, 'DATA'),
 ('paper', 6, [52, 72, 545, 216], 'p06-q4a-question', '2022 HL Section A Q4(a)', False, None),
 ('paper', 13, [54, 154, 537, 328], 'p13-q10-data', '2022 HL Section A Q10', False, 'DATA'),
 ('paper', 14, [52, 174, 545, 417], 'p14-q11-infographic', '2022 HL Q11', False, 'DATA'),
 ('paper', 18, [52, 103, 545, 351], 'p18-q12-charts', '2022 HL Q12(a)', False, 'DATA'),
 ('paper', 22, [52, 103, 545, 322], 'p22-q13-infographic', '2022 HL Q13', False, 'DATA'),
 ('paper', 26, [52, 361, 545, 709], 'p26-q14aii-question', '2022 HL Q14(a)(ii)', False, None),
 ('paper', 27, [52, 55, 545, 382], 'p27-q14b-question', '2022 HL Q14(b)', False, None),
 ('paper', 28, [116, 300, 545, 558], 'p28-q14c-chart', '2022 HL Q14(c)', False, 'DATA'),
 ('paper', 30, [52, 87, 545, 318], 'p30-q15a-chart', '2022 HL Q15(a)', False, 'DATA'),
 ('paper', 31, [52, 70, 545, 421], 'p31-q15aiii-question', '2022 HL Q15(a)(iii)', False, None),
 ('paper', 32, [52, 104, 545, 316], 'p32-q15b-chart', '2022 HL Q15(b)', False, 'DATA'),
 ('paper', 33, [52, 310, 545, 599], 'p33-q15c-chart', '2022 HL Q15(c)', False, 'DATA'),
]
QALT = {
 'p03-q1a-question': 'A demand curve headed DEMAND FOR FACE MASKS, the vertical axis PRICE IN EURO € from 0 to 7 and the horizontal axis QUANTITY DEMANDED from 0 to 20. A red line falls from €6 at quantity 2 to €1 at quantity 20, with red dots marking €5 at quantity 4 and €4 at quantity 8.',
 'p27-q14b-question': 'A costs table for a housebuilder with columns Units of Housing, Fixed Cost (€), Variable Cost (€), Total Cost (€), Average Total Cost (€) and Marginal Cost (€). Row 1: 100,000; 260,000; A; 360,000; -. Row 2: 100,000; 300,000; 400,000; B; 40,000. Row 3: 100,000; 350,000; 450,000; 150,000; C. Row 4: 100,000; 405,000; 505,000; 126,250; 55,000. Below it a Calculations box for A, B and C, each with an Answer line.',
}
QKEY = {'p06-q4a-question': 'p06-i0', 'p26-q14aii-question': 'p26-i0', 'p31-q15aiii-question': 'p31-art'}
DATA_ALT = {
 'p03-q1-graph': 'A demand curve headed DEMAND FOR FACE MASKS, the vertical axis PRICE IN EURO € from 0 to 7 and the horizontal axis QUANTITY DEMANDED from 0 to 20. A red line falls from €6 at quantity 2 to €1 at quantity 20, with red dots marking €5 at quantity 4 and €4 at quantity 8.',
 'p04-q2-infographic': 'A CSO infographic headed Quarterly National Accounts Q2 2021. Down the left: GNP up 6.7%, GDP up 6.3% (€109.4bn) and MDD up 8.4%. Panels with growth figures: Industry excl. Construction 3.6%, Construction 22.9%, Distribution, Transport, Hotels & Restaurants 0.7%, Information & Comm. 6.2%, Financial & Insurance Activities 2.4%, Professional, Admin. & Support Services 4.1%, Personal Consumption 12.6%, Government Expenditure 0.9%, Investment 5.8%, Exports 6.4%, Imports 5.4%. Footnote: % growth Q2 2021 vs Q1 2021. Source www.cso.ie.',
 'p13-q10-data': 'Left, a production possibility schedule with columns Doritos million (kg) and Tropicana million (l): A 0 and 90; B 20 and 80; C 38 and 70; D 50 and 62 (in red); E 60 and 55; F 70 and 48; G 80 and 35; H 90 and 0 (in red). Right, a chart headed PepsiCo Production Possibility Frontier (PPF), the vertical axis Tropicana Litres (Millions) from 0 to 100 and the horizontal axis Doritos Kilograms (Millions) from 0 to 100. The frontier runs through points A to H, with D and H marked, and a green point X sits inside the frontier at 20, 20.',
 'p14-q11-infographic': 'An RTB infographic headed Highest and lowest standardised average rents Q2 2021. By county: Dublin €1,848 per month and Donegal €677 per month. By LEA: Ballymote, Tobercurry Co. Sligo €645 per month and Stillorgan LEA, Co. Dublin €2,440 per month. A map headed Rents in cities Q2 2021: Galway City €1,355, Dublin City €1,775, Limerick City €1,196, Cork City €1,344, Waterford City €969. Source www.rtb.ie.',
 'p18-q12-charts': 'Two pie charts. Left, MARKET SHARE OF DOMESTIC ELECTRICITY SUPPLIERS IN IRELAND 2005: one solid circle, ESB (Now Electric Ireland), captioned HHI in 2005 was 10,000. Right, the same heading for 2019: Electric Ireland (Formerly ESB) 53%, Bord Gáis Energy 16%, SSE Airtricity 12%, Energia 8%, PrePayPower 7%, Panda 2%, Pinergy 1%, Others 1%, captioned HHI in 2019 was 3,328. Source: Adapted from Statista.com.',
 'p22-q13-infographic': 'The CSO infographic Government Income & Expenditure 2020, shown as two euro coins. Sources of Income (per euro): Taxes 74c, PRSI 19c, Fees for Services 5c, Other Income 2c. Areas of Expenditure (per euro): Social Benefits 37c, Pay 24c, Goods and Services 14c, Capital Assets 9c, Subsidies 6c, Interest 4c, Grants and Other Payments 4c, Payments to the EU 2c. Source www.cso.ie.',
 'p28-q14c-chart': 'A horizontal bar chart headed Gender Pay Gap: How much less do women earn than men? Estonia 21.7, Germany 19.2, Denmark 14, Ireland 11.3, Luxemburg 1.3. Source: Adapted from Eurostat.',
 'p30-q15a-chart': 'A line chart headed Evolution of Irish Milk Production, the vertical axis Million litres from 2,000 to 9,000 and the horizontal axis 1975 to 2020. The line rises from about 3,200 in 1975 to about 5,500 in the mid-1980s, stays near 5,000 until about 2010, then climbs steeply to the annotated 2020 estimate 8.3bn litres. Arrows mark 1973 Ireland Joined the EEC, 1984 Introduction of milk quotas and 2015 Removal of milk quotas. Source: CSO.',
 'p32-q15b-chart': 'A line chart headed Euro (€) to Pound Sterling (£) exchange rate, the vertical axis €/£ EXCHANGE RATE from 0.5 to 0.95 and the horizontal axis Dec-12 to Dec-21. The line is about 0.81 in December 2012, 0.83 in 2013, 0.78 in 2014, 0.74 in 2015, 0.85 in 2016, 0.89 in 2017, 0.90 in 2018, 0.85 in 2019, 0.89 in 2020 and 0.86 in 2021. Source: Adapted from ecb.europa.eu.',
 'p33-q15c-chart': 'A column chart headed Net Beneficiaries from the EU budget, by member state (2018, in million euros), the vertical axis Net benefit in € millions from -20000 to 15000. Below zero (net contributors): Germany about -17,000, France about -7,500, Italy about -6,600, Sweden about -2,000, Ireland about -500. Above zero (net beneficiaries): Spain about 400, Croatia about 600, Luxembourg about 1,600, Hungary about 5,000, Poland about 11,500. Source: Adapted from www.statista.com.',
}


def tidy(s):
    for a, b in LIG.items():
        s = s.replace(a, b)
    return re.sub(r'\s+', ' ', s.replace('\uf0fc', '✓')).strip()


cat_path = f'{W}/scripts/markbank/authored/economics-completion-figures.json'
cat = json.load(open(cat_path))
_order = {c['file']: i for i, c in enumerate(cat)}
man_path = f'{W}/components/MarkBank/figures.json'
man_text = open(man_path).read()
man = json.loads(man_text)
add_entries = []
for kind, page, rect, slug, ref, solution, alt in F:
    key = f'economics-2022-HL-{kind}-{slug}'
    fname = key + '.png'
    src = f'paper-trail-corpus/{"markingschemes" if kind == "scheme" else "exampapers"}/2022/LC034ALP000EV.pdf'
    with fitz.open(f'{W}/{src}') as doc:
        pg = doc[page - 1]
        pg.get_pixmap(matrix=fitz.Matrix(SCALE, SCALE), clip=fitz.Rect(*rect)).save(f'{OUT}/{fname}')
        if kind == 'paper' and alt == 'DATA':
            alt = DATA_ALT[slug]
        elif kind == 'paper':
            data = QALT.get(slug) or man[f'economics-2022-HL-paper-{QKEY[slug]}']['alt']
            words = tidy(pg.get_text('text', clip=fitz.Rect(*rect)))
            alt = f'The printed question as the paper sets it. {data} The printed text reads: {words}'
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
