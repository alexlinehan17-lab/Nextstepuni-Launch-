"""Render, catalogue and register the 2024 HL review figures (idempotent).

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
ATTR = 'SEC Leaving Certificate Economics 2024 Higher Level — © State Examinations Commission'
LIG = {'Ɵ': 'ti', 'Ŧ': 'ti', 'Ʃ': 'tt', 'ﬀ': 'ff', 'ﬁ': 'fi', 'ﬂ': 'fl'}
F = [
 ('paper', 5, [52, 55, 545, 418], 'p05-q3a-question', '2024 HL Section A Q3(a)', False, None),
 ('paper', 6, [52, 55, 545, 256], 'p06-q4a-question', '2024 HL Section A Q4(a)', False, 'p06-i0'),
 ('paper', 12, [52, 55, 545, 540], 'p12-q10a-question', '2024 HL Section A Q10(a)', False, None),
 ('paper', 18, [52, 386, 548, 740], 'p18-q12bii-question', '2024 HL Q12(b)(ii)', False, 'p18-i0'),
 ('paper', 33, [80, 102, 542, 293], 'p33-art', '2024 HL Q16(a)', False, 'DATA'),
]
QALT = {
 'p05-q3a-question': 'The question’s demand and supply diagram of the electricity market: Price MWh on the vertical axis and Quantity of Electricity on the horizontal; a downward-sloping demand curve D crosses an upward-sloping supply curve S at the equilibrium, with dashed guides to €600 Pe on the price axis and Qe on the quantity axis.',
 'p12-q10a-question': 'A table adapted from Ireland’s National Accounts: Net factor income from abroad −€105bn; EU Subsidies €2bn; EU Taxes €0.5bn. Below it a national income ladder from Gross Domestic Product (GDP) at Current Market Prices €430bn: step (i) is completed (430.00 less net factor income from abroad 105.00 gives Gross National Product at Current Market Prices, €325 bn) and step (ii), Gross National Income at Current Market Prices, is left blank.',
}
DATA_ALT = {
 'p33-art': 'A column chart headed ‘Number of homeless people in Ireland’. The vertical axis, ‘Number of homeless people’, runs from 0 to 14,000 in steps of 2,000; the horizontal axis, ‘Years’, shows 2021, 2022 and 2023. The 2021 bar (red) stands at just over 8,000; the 2022 bar (green) and the 2023 bar (blue) each stand just under 13,000. Source: Adapted from Independent.ie.',
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
    key = f'economics-2024-HL-{kind}-{slug}'
    fname = key + '.png'
    src = f'paper-trail-corpus/{"markingschemes" if kind == "scheme" else "exampapers"}/2024/LC034ALP000EV.pdf'
    with fitz.open(f'{W}/{src}') as doc:
        pg = doc[page - 1]
        pg.get_pixmap(matrix=fitz.Matrix(SCALE, SCALE), clip=fitz.Rect(*rect)).save(f'{OUT}/{fname}')
        if kind == 'paper' and alt == 'DATA':
            alt = DATA_ALT[slug]
        elif kind == 'paper':
            data = QALT.get(slug) or man[f'economics-2024-HL-paper-{alt}']['alt']
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
    entry.update({'lettersVisible': [], 'labelMeanings': [], 'questionRef': ref, 'year': 2024,
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
