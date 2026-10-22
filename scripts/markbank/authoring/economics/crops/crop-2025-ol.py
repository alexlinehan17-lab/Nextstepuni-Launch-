"""Render, catalogue and register the 2025 OL review figures (idempotent).

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
ATTR = 'SEC Leaving Certificate Economics 2025 Ordinary Level — © State Examinations Commission'
LIG = {'Ɵ': 'ti', 'Ŧ': 'ti', 'Ʃ': 'tt', 'ﬀ': 'ff', 'ﬁ': 'fi', 'ﬂ': 'fl'}
F = [
 ('scheme', 13, [180, 372, 430, 414], 'p13-q7i-working', '2025 OL Section A Q7(i)', True,
  'Official working: 243,700 over 589,500, times 100 over 1, equals 41.3 %.'),
 ('scheme', 20, [100, 400, 430, 446], 'p20-q12ai-working', '2025 OL Q12(a)(i)', True,
  'Official working with the mark for each step: €14.9 bn (6) over €105.4 bn (4), times 100 (2), equals 14.14 % (4).'),
 ('paper', 3, [52, 300, 545, 368], 'p03-q1-electricity-headline', '2025 OL Section A Q1(ii)', False,
  'A teal CSO headline banner reading: Wholesale electricity prices in August 2024 were down by almost 75% from the peak recorded in August 2022. Source www.cso.'),
 ('paper', 8, [60, 104, 545, 392], 'p08-q7-population', '2025 OL Section A Q7(ii)', False,
  'Bar chart titled Population - People aged 65 and over, Increase: 243,700. A green bar for 2014 at 589,500 and a purple bar for 2024 at 833,200. Adapted from cso.'),
 ('paper', 21, [60, 100, 545, 320], 'p21-q14b-oda', '2025 OL Q14(b)(i)', False,
  'Bar chart titled Ireland Overseas Development Assistance, Millions (€), on a 0 to 3000 axis: 2020 868, 2021 976, 2022 2291, 2023 2604. Adapted from ireland.ie.'),
 ('paper', 8, [52, 55, 545, 452], 'p08-q7i-question', '2025 OL Section A Q7(i)', False, 'p08-q7-population'),
 ('paper', 9, [52, 55, 545, 292], 'p09-q8-question', '2025 OL Section A Q8', False, 'p09-i1'),
 ('paper', 9, [52, 395, 565, 736], 'p09-q9-question', '2025 OL Section A Q9', False, 'p09-i2'),
 ('paper', 12, [52, 55, 565, 541], 'p12-q11bii-question', '2025 OL Q11(b)(ii)', False, 'p12-art'),
 ('paper', 14, [52, 55, 545, 372], 'p14-q12ai-question', '2025 OL Q12(a)(i)', False, 'p14-art'),
 ('paper', 18, [52, 55, 560, 522], 'p18-q13bi-question', '2025 OL Q13(b)(i)', False, 'p18-i0'),
 ('paper', 24, [52, 55, 545, 388], 'p24-q15bi-question', '2025 OL Q15(b)(i)', False, 'p24-art'),
]
QALT = {}


def tidy(s):
    for a, b in LIG.items():
        s = s.replace(a, b)
    return re.sub(r'\s+', ' ', re.sub(r'_{3,}', ' ', s.replace('\uf0fc', '✓'))).strip()


cat_path = f'{W}/scripts/markbank/authored/economics-completion-figures.json'
cat = json.load(open(cat_path))
_order = {c['file']: i for i, c in enumerate(cat)}
man_path = f'{W}/components/MarkBank/figures.json'
man_text = open(man_path).read()
man = json.loads(man_text)
add_entries = []
new_alts = {}
for kind, page, rect, slug, ref, solution, alt in F:
    key = f'economics-2025-OL-{kind}-{slug}'
    fname = key + '.png'
    src = f'paper-trail-corpus/{"markingschemes" if kind == "scheme" else "exampapers"}/2025/LC034GLP000EV.pdf'
    with fitz.open(f'{W}/{src}') as doc:
        pg = doc[page - 1]
        pg.get_pixmap(matrix=fitz.Matrix(SCALE, SCALE), clip=fitz.Rect(*rect)).save(f'{OUT}/{fname}')
        if kind == 'paper' and slug.endswith('-question'):
            data = QALT.get(slug) or (man.get(f'economics-2025-OL-paper-{alt}') or new_alts[alt])['alt']
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
    entry.update({'lettersVisible': [], 'labelMeanings': [], 'questionRef': ref, 'year': 2025,
                  'level': 'ordinary', 'attribution': ATTR})
    if key in man:
        if man[key] != entry:
            sys.exit(f'{key} already registered with different content — remove it by hand first')
        continue
    add_entries.append((key, entry))
    new_alts[slug] = entry
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
