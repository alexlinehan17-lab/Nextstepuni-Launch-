"""Render, catalogue and register the 2023 OL review figures (idempotent).

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
ATTR = 'SEC Leaving Certificate Economics 2023 Ordinary Level — © State Examinations Commission'
LIG = {'Ɵ': 'ti', 'Ŧ': 'ti', 'Ʃ': 'tt', 'ﬀ': 'ff', 'ﬁ': 'fi', 'ﬂ': 'fl'}
F = [
 ('paper', 7, [104, 106, 456, 318], 'p07-q5-diagram', '2023 OL Section A Q5', False, 'DATA'),
 ('paper', 11, [60, 226, 540, 498], 'p11-q11b-diagram', '2023 OL Q11(b)', False, 'DATA'),
 ('paper', 11, [52, 55, 545, 593], 'p11-q11bii-question', '2023 OL Q11(b)(ii)', False, None),
 ('paper', 19, [54, 90, 536, 338], 'p19-q14-chart', '2023 OL Q14(a)', False, 'DATA'),
 ('paper', 25, [52, 55, 545, 707], 'p25-q16ai-question', '2023 OL Q16(a)(i)', False, None),
 ('scheme', 26, [90, 240, 524, 749], 'p26-q16ai-table', '2023 OL Q16(a)(i)', True,
  'The marking scheme\u2019s completed factors-of-production table for Keogh\u2019s Crisps, columns Factor of Production, Explanation and Example. 1. LAND, anything supplied by nature which helps in production, examples POTATOES, SALT and OIL. 2. LABOUR, the human effort involved in the production of a good or service, example Workers. 3. CAPITAL, anything made by humans which is used in production, example Machinery. 4. ENTERPRISE, takes a risk with an idea in setting up a business in return for profit, example TOM KEOGH. The six cells the candidate supplies are in capitals.'),
]
DIAGRAM = ('A cost-and-revenue diagram for a firm in long-run equilibrium, Price (\u20ac) on the vertical axis and the '
           'horizontal axis numbered 3. A blue U-shaped curve numbered 1; a yellow downward-sloping line numbered 2 '
           'that touches the blue curve at a marked point; a green curve labelled MC that cuts the blue curve at its '
           'lowest point, marked W; and a red, steeper downward-sloping line labelled MR, which MC cuts at point E.')
QALT = {
 'p11-q11bii-question': 'An answer table with rows 1, 2 and 3 for naming the numbered items. Below it: ' + DIAGRAM,
 'p25-q16ai-question': 'A four-row table headed Factor of Production, Explanation and Example. Row 1 LAND is explained as anything supplied by nature which helps in production, its example blank. Row 2 has its factor and explanation blank and the example Workers. Row 3 CAPITAL has its explanation blank and the example Machinery. Row 4 has its factor blank, the explanation \u2018Takes a risk with an idea in setting up a business in return for profit.\u2019 and its example blank.',
}
DATA_ALT = {
 'p07-q5-diagram': 'A supply diagram for Rugby World Cup tickets: Price on the vertical axis, No. of tickets on the horizontal axis, and a single vertical supply line labelled S1 standing to the right of the price axis.',
 'p11-q11b-diagram': DIAGRAM,
 'p19-q14-chart': 'A line chart headed \u2018Petrol Prices in Ireland: April - September 2022\u2019, vertical axis \u2018Price in cent (\u20ac)\u2019 from 160.00 to 220.00, horizontal axis \u2018Months\u2019 from Apr-22 to Sep-22. The line rises from about 181 in April to about 192 in May and peaks near 213 in June, then falls through about 199 in July to about 187 in August and 184 in September. Source: Adapted from theaa.ie.',
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
    key = f'economics-2023-OL-{kind}-{slug}'
    fname = key + '.png'
    src = f'paper-trail-corpus/{"markingschemes" if kind == "scheme" else "exampapers"}/2023/LC034GLP000EV.pdf'
    with fitz.open(f'{W}/{src}') as doc:
        pg = doc[page - 1]
        pg.get_pixmap(matrix=fitz.Matrix(SCALE, SCALE), clip=fitz.Rect(*rect)).save(f'{OUT}/{fname}')
        if kind == 'paper' and alt == 'DATA':
            alt = DATA_ALT[slug]
        elif kind == 'paper':
            data = QALT.get(slug) or man[f'economics-2023-OL-paper-{alt}']['alt']
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
    entry.update({'lettersVisible': [], 'labelMeanings': [], 'questionRef': ref, 'year': 2023,
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
