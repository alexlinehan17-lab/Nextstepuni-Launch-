"""Render, catalogue and register the 2023 HL review figures (idempotent).

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
ATTR = 'SEC Leaving Certificate Economics 2023 Higher Level — © State Examinations Commission'
LIG = {'Ɵ': 'ti', 'Ŧ': 'ti', 'Ʃ': 'tt', 'ﬀ': 'ff', 'ﬁ': 'fi', 'ﬂ': 'fl'}
F = [
 ('paper', 5, [52, 55, 540, 182], 'p05-q3a-question', '2023 HL Section A Q3(a)', False, 'p05-i0'),
 ('paper', 5, [205, 552, 395, 592], 'p05-q3c-formula', '2023 HL Section A Q3(c)', False, 'DATA'),
 ('paper', 6, [52, 55, 540, 185], 'p06-q4a-question', '2023 HL Section A Q4(a)', False, 'p06-i0'),
 ('paper', 9, [52, 55, 545, 368], 'p09-q7a-question', '2023 HL Section A Q7(a)', False, 'p09-i0'),
 ('paper', 12, [52, 55, 545, 712], 'p12-q10-question', '2023 HL Section A Q10', False, None),
 ('paper', 13, [52, 112, 545, 408], 'p13-q11ai-question', '2023 HL Q11(a)(i)', False, None),
 ('paper', 19, [52, 55, 545, 275], 'p19-q12bi-question', '2023 HL Q12(b)(i)', False, None),
 ('paper', 19, [80, 88, 545, 230], 'p19-q12b-chart', '2023 HL Q12(b)', False, 'DATA'),
 ('paper', 30, [52, 55, 545, 482], 'p30-q15aiii-question', '2023 HL Q15(a)(iii)', False, 'p30-i0'),
]
QALT = {
 'p12-q10-question': 'A table adapted from Ireland’s National Accounts for 2021: Net factor income from abroad −€103bn; EU Subsidies €1.7bn; EU Taxes €0.5bn; Adjustments, including factor income of redomiciled companies, depreciation on R&D imports and trade in IP, and depreciation on aircraft leasing, €89bn. Below it a ladder from Gross Domestic Product (GDP) at Current Market Prices €426bn: A, Gross National Product, is completed (426.00 less 103.00, Ans €323 bn); B, Gross National Income, and C, Modified Gross National Income, are left blank.',
 'p13-q11ai-question': 'A CSO infographic of preliminary Census 2022 results: population 4,761,865 in 2016 and 5,123,536 in 2022, a total change of 361,671 (natural increase 171,338; net migration 190,333), with housing figures on the right. Below it a table: Population 2016 4,761,865; Population 2022 5,123,536; Total Change 361,671.',
 'p19-q12bi-question': 'A column chart headed ‘Market Share for Irish Dairy Producers’, the vertical axis in percent from 0 to 60. The bars read Kerry Group 48, Glanbia 27, Dairygold 8, Lakeland Dairies 7, Dale Farm 3, Aurivo 3, Arrabawn 2 and Tipperary Co-op 2. Source: Adapted from Top1000.ie.',
}
DATA_ALT = {
 'p05-q3c-formula': 'The formula printed in Question 3(c): MUx over Px equals 1800 over 10, and MUy over Py equals 3600 over 10.',
 'p19-q12b-chart': 'A column chart headed ‘Market Share for Irish Dairy Producers’, the vertical axis in percent from 0 to 60. The bars read Kerry Group 48, Glanbia 27, Dairygold 8, Lakeland Dairies 7, Dale Farm 3, Aurivo 3, Arrabawn 2 and Tipperary Co-op 2. Source: Adapted from Top1000.ie.',
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
    key = f'economics-2023-HL-{kind}-{slug}'
    fname = key + '.png'
    src = f'paper-trail-corpus/{"markingschemes" if kind == "scheme" else "exampapers"}/2023/LC034ALP000EV.pdf'
    with fitz.open(f'{W}/{src}') as doc:
        pg = doc[page - 1]
        pg.get_pixmap(matrix=fitz.Matrix(SCALE, SCALE), clip=fitz.Rect(*rect)).save(f'{OUT}/{fname}')
        if kind == 'paper' and alt == 'DATA':
            alt = DATA_ALT[slug]
        elif kind == 'paper':
            data = QALT.get(slug) or man[f'economics-2023-HL-paper-{alt}']['alt']
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
