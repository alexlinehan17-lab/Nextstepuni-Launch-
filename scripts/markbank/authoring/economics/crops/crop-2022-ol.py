"""Render, catalogue and register the 2022 OL review figures (idempotent).

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
ATTR = 'SEC Leaving Certificate Economics 2022 Ordinary Level — © State Examinations Commission'
LIG = {'Ɵ': 'ti', 'Ŧ': 'ti', 'Ʃ': 'tt', 'ﬀ': 'ff', 'ﬁ': 'fi', 'ﬂ': 'fl'}
F = [
 ('paper', 3, [118, 141, 530, 347], 'p03-q1-infographic', '2022 OL Section A Q1', False, 'DATA'),
 ('paper', 5, [52, 70, 545, 254], 'p05-q4-question', '2022 OL Section A Q4', False, None),
 ('paper', 7, [52, 245, 545, 373], 'p07-q7aii-question', '2022 OL Section A Q7(a)(ii)', False, None),
 ('paper', 7, [52, 288, 545, 550], 'p07-q7b-question', '2022 OL Section A Q7(b)', False, None),
 ('paper', 8, [52, 415, 545, 523], 'p08-q9i-question', '2022 OL Section A Q9(i)', False, None),
 ('paper', 9, [112, 118, 541, 344], 'p09-q10-chart', '2022 OL Section A Q10', False, 'DATA'),
 ('paper', 11, [106, 236, 510, 534], 'p11-q11b-diagram', '2022 OL Q11(b)', False, 'DATA'),
 ('paper', 11, [52, 55, 545, 672], 'p11-q11bii-question', '2022 OL Q11(b)(ii)', False, None),
 ('paper', 13, [52, 55, 545, 678], 'p13-q12a-question', '2022 OL Q12(a)', False, None),
 ('paper', 14, [92, 74, 446, 310], 'p14-q12b-diagram', '2022 OL Q12(b)', False, 'DATA'),
 ('paper', 14, [52, 55, 545, 568], 'p14-q12b-question', '2022 OL Q12(b)', False, None),
 ('paper', 16, [52, 105, 545, 338], 'p16-q13-chart', '2022 OL Q13(a)', False, 'DATA'),
 ('paper', 16, [52, 55, 545, 373], 'p16-q13ai-question', '2022 OL Q13(a)(i)', False, None),
 ('paper', 17, [52, 207, 545, 300], 'p17-q13bii-question', '2022 OL Q13(b)(ii)', False, None),
 ('paper', 19, [52, 55, 545, 701], 'p19-q14ai-question', '2022 OL Q14(a)(i)', False, None),
 ('paper', 22, [52, 94, 545, 325], 'p22-q15a-chart', '2022 OL Q15(a)', False, 'DATA'),
 ('paper', 24, [52, 92, 545, 296], 'p24-q15c-chart', '2022 OL Q15(c)', False, 'DATA'),
]
MONO = ('A cost-and-revenue diagram for a firm in monopoly with Quantity on the horizontal axis and the vertical axis '
        'numbered 1. Two downward-sloping straight lines: the flatter one labelled AR and a steeper one numbered 3. Two '
        'U-shaped curves: one labelled AC and a steeper one numbered 2, which cuts the line numbered 3 at a large dot '
        'marked G.')
QALT = {
 'p05-q4-question': 'A table headed Substitute Goods and Complementary Goods with blank tick columns for Samsung S21, iPhone 13 case, iPhone charging plug and Google Pixel 4A smartphone.',
 'p07-q7aii-question': 'A table headed Fixed Cost and Variable Cost with blank tick columns for Wages €1,000, Raw materials €1,500, Light & heat €300 and Rent of the premises €750.',
 'p07-q7b-question': 'The cost table from part (a): Wages €1,000, Raw materials €1,500, Light & heat €300 and Rent of the premises €750, under the headings Fixed Cost and Variable Cost, then the OR and part (b).',
 'p08-q9i-question': 'The PED formula printed beside the stem: change in Q over change in P, multiplied by P1 + P2 over Q1 + Q2.',
 'p11-q11bii-question': 'A three-row answer table numbered 1 to 3, then ' + MONO[0].lower() + MONO[1:],
 'p13-q12a-question': 'A schedule: Price €9, 10,000 demanded, 50,000 supplied; €8, 20,000 and 40,000; €7, 30,000 and 30,000; €6, 40,000 and 20,000; €5, 50,000 and 10,000. Below the instructions, a blank graph headed Demand and Supply Curves Reusable Coffee Cups, Price € from 4 to 10 on the vertical axis and Units (000’s) from 0 to 60 on the horizontal.',
 'p14-q12b-question': 'A demand and supply diagram: Price on the vertical axis and Quantity on the horizontal, a downward-sloping line D and an upward-sloping line S crossing at a dot, with dotted lines to P1 on the price axis and Q1 on the quantity axis.',
 'p16-q13ai-question': 'A pie chart headed Total Government Expenditure: €82.92 Billion, with Current €71.82 Billion and Capital €11.1 Billion. Source: Adapted from gov.ie.',
 'p17-q13bii-question': 'The multiplier formula printed as a fraction: 1 over MPS + MPM.',
 'p19-q14ai-question': 'A four-row table headed Factor of Production, Explanation and Example. Row 1 Land, row 2 blank with the example Workers, row 3 Capital, and row 4 blank with the explanation ‘Takes a risk with an idea in setting up a business in return for profit.’ The other cells are blank.',
}
QKEY = {}
DATA_ALT = {
 'p03-q1-infographic': 'A Central Bank of Ireland infographic headed Forecast growth* in Irish economy, with a map of Ireland and four columns: 2020 -4.9%, 2021 5.5%, 2022 7.1% and 2023 4.1%. Footnote: *Modified domestic demand. Source www.centralbank.ie.',
 'p09-q10-chart': 'A column chart headed General Government Debt - interest paid/forecasted, the vertical axis € billions from 0.00 to 6.00. 2018 5.32, 2019 4.62, 2020 3.83, 2021 3.30, 2022 3.40, 2023 3.58, 2024 3.51. Source: Adapted from ntma.ie.',
 'p11-q11b-diagram': MONO,
 'p14-q12b-diagram': 'A demand and supply diagram for Gym + Coffee clothing: Price on the vertical axis and Quantity on the horizontal, a downward-sloping line D and an upward-sloping line S crossing at a dot, with dotted lines to P1 on the price axis and Q1 on the quantity axis.',
 'p16-q13-chart': 'A pie chart headed Total Government Expenditure: €82.92 Billion, with Current €71.82 Billion and Capital €11.1 Billion. Source: Adapted from gov.ie.',
 'p22-q15a-chart': 'A line chart headed Corporation Tax Receipts, the vertical axis € millions from 0 to 14,000 and the horizontal axis 2011 to 2020. The line rises from about 3,500 in 2011 to about 4,200 in 2012 and 2013 and 4,600 in 2014, about 6,900 in 2015, 7,300 in 2016, 8,200 in 2017, 10,400 in 2018, 10,900 in 2019 and about 11,800 in 2020. Source: Adapted from revenue.ie.',
 'p24-q15c-chart': 'A column chart headed Exports from Ireland to the US and the UK, € Billions from 0 to 6, January to December 2021. US exports run between about 3.6 and 4.6 billion most months, peaking at about 5.7 in October and 5 in November and ending at about 4.1 in December. UK exports run between about 1.1 and 2.0 billion, highest in November. Source: Adapted from the cso.ie.',
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
    key = f'economics-2022-OL-{kind}-{slug}'
    fname = key + '.png'
    src = f'paper-trail-corpus/{"markingschemes" if kind == "scheme" else "exampapers"}/2022/LC034GLP000EV.pdf'
    with fitz.open(f'{W}/{src}') as doc:
        pg = doc[page - 1]
        pg.get_pixmap(matrix=fitz.Matrix(SCALE, SCALE), clip=fitz.Rect(*rect)).save(f'{OUT}/{fname}')
        if kind == 'paper' and alt == 'DATA':
            alt = DATA_ALT[slug]
        elif kind == 'paper':
            data = QALT[slug]
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
