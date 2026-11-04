"""Render, catalogue and register the 2021 OL review figures (idempotent).

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
ATTR = 'SEC Leaving Certificate Economics 2021 Ordinary Level — © State Examinations Commission'
LIG = {'Ɵ': 'ti', 'Ŧ': 'ti', 'Ʃ': 'tt', 'ﬀ': 'ff', 'ﬁ': 'fi', 'ﬂ': 'fl'}
F = [
 ('paper', 4, [52, 55, 545, 193], 'p04-q2-question', '2021 OL Section A Q2', False, None),
 ('paper', 4, [52, 250, 545, 624], 'p04-q3-question', '2021 OL Section A Q3', False, None),
 ('paper', 5, [52, 55, 545, 187], 'p05-q4-question', '2021 OL Section A Q4', False, None),
 ('paper', 7, [52, 340, 545, 632], 'p07-q8-question', '2021 OL Section A Q8', False, None),
 ('scheme', 7, [110, 138, 400, 312], 'p07-q8-diagram', '2021 OL Section A Q8', True,
  'The marking scheme\u2019s completed diagram: Price on the vertical axis and Quantity on the horizontal. A thin '
  'demand line D1 and a thicker line D2 to its left, with arrows pointing left from D1 to D2. At the price P the '
  'quantity falls from Q1 on D1 to Q2 on D2.'),
 ('paper', 10, [52, 138, 545, 433], 'p10-q11-hdi-tables', '2021 OL Q11(a)', False, 'DATA'),
 ('paper', 13, [52, 55, 545, 641], 'p13-q12a-question', '2021 OL Q12(a)', False, None),
]
QALT = {
 'p04-q2-question': 'A two-row table headed Statement, Positive and Normative, with the two tick columns blank.',
 'p04-q3-question': 'The PED formula printed as two fractions, change in Q over change in P multiplied by P1 + P2 over Q1 + Q2, then a table with columns Units Purchased and Price (\u20ac): before the carbon tax increase 1000 litres at 800, after it 750 litres at 850, and the changes \u2212250 litres and + 50. A Workings box and an Answer line follow, then part (ii).',
 'p05-q4-question': 'A utility table for bags of crisps consumed 1 to 4: total utility 10, 25, 38 and 47; marginal utility 10, 15 and two heavily outlined blank boxes.',
 'p07-q8-question': 'A diagram with Price on the vertical axis and Quantity on the horizontal and one downward-sloping demand line labelled D.',
 'p13-q12a-question': 'A cost-and-revenue diagram for a firm in perfect competition: Price on the vertical axis and Quantity on the horizontal, a U-shaped AC curve and a rising MC curve meeting at a dot marked B on a horizontal line labelled D = AR = MR. Below it a table listing the labels MC, AC, AR and MR with blank answer cells, then part (ii) with three bullets.',
}
DATA_ALT = {
 'p10-q11-hdi-tables': 'Two one-row tables extracted from the Human Development Index. 2019: rank 3, Ireland, HDI value 0.951, life expectancy at birth 82.1 years, mean years of schooling 12.5. 2020: rank 2, Ireland, HDI value 0.955, life expectancy at birth 82.3 years, mean years of schooling 12.7. Source: Adapted from www.hdr.undp.org.',
}


def tidy(s):
    for a, b in LIG.items():
        s = s.replace(a, b)
    return re.sub(r'\s+', ' ', s.replace('', '✓')).strip()


cat_path = f'{W}/scripts/markbank/authored/economics-completion-figures.json'
cat = json.load(open(cat_path))
_order = {c['file']: i for i, c in enumerate(cat)}
man_path = f'{W}/components/MarkBank/figures.json'
man_text = open(man_path).read()
man = json.loads(man_text)
add_entries = []
for kind, page, rect, slug, ref, solution, alt in F:
    key = f'economics-2021-OL-{kind}-{slug}'
    fname = key + '.png'
    src = f'paper-trail-corpus/{"markingschemes" if kind == "scheme" else "exampapers"}/2021/LC034GLP000EV.pdf'
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
    entry.update({'lettersVisible': [], 'labelMeanings': [], 'questionRef': ref, 'year': 2021,
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
