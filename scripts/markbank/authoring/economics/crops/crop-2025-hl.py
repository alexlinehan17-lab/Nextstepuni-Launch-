"""Render, catalogue and register the 2025 HL review figures (idempotent).

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
ATTR = 'SEC Leaving Certificate Economics 2025 Higher Level — © State Examinations Commission'
LIG = {'Ɵ': 'ti', 'Ŧ': 'ti', 'Ʃ': 'tt', 'ﬀ': 'ff', 'ﬁ': 'fi', 'ﬂ': 'fl'}
F = [
 ('scheme', 6, [86, 265, 520, 432], 'p06-q2a-working', '2025 HL Section A Q2(a)', True,
  'Official working: household savings over household total disposable income, times 100 over 1; €6.59 bn over €43.91 bn times 100 over 1. Answer: 15 %. Deduct 1 mark if % omitted.'),
 ('scheme', 17, [95, 314, 500, 540], 'p17-q6b-labour-market', '2025 HL Section A Q6(b)', True,
  'Official labour-market diagram. Wage rate on the vertical axis, quantity of workers on the horizontal. Supply SL and demand DL cross at E, giving WE and QE. A horizontal line at NMW / €13.50 above WE meets DL at QD and SL at QS; the gap between QD and QS is labelled Unemployment gap / Excess supply of labour.'),
 ('scheme', 24, [86, 495, 520, 646], 'p24-q11ai-hhi-working', '2025 HL Q11(a)(i)', True,
  'Official HHI working. 49% squared = 2,401; 28% squared = 784; 20% squared = 400; 3% squared = 9; 2,401 + 784 + 400 + 9 = 3,594.'),
 ('scheme', 26, [86, 178, 510, 442], 'p26-q11bi-patent-monopoly', '2025 HL Q11(b)(i)', True,
  'Official long-run monopoly diagram. Price / Cost € on the vertical axis, Quantity on the horizontal. MC rises through E where it meets MR; output Q1. AR = D is above at Z giving price P1; AC is at Y giving cost C1; the shaded rectangle between P1 and C1 is SNPs; W marks the minimum point of AC.'),
 ('scheme', 39, [86, 422, 420, 662], 'p39-q13ai-working', '2025 HL Q13(a)(i)', True,
  'Official working: Ireland’s exports to the US over Ireland’s total goods exports, times 100 over 1; €34 bn over €108 bn times 100 over 1. Answer: 31.48% / 32%. Deduct 1 mark for omission of %.'),
 ('scheme', 52, [86, 164, 410, 300], 'p52-q14bii-ped-working', '2025 HL Q14(b)(ii)', True,
  'Official PED working: change in Q over change in P, times (P1 + P2) over (Q1 + Q2); minus 10,000 over 0.50 times (2.00 + 2.50) over (30,000 + 20,000). Answer: minus 1.8.'),
 ('scheme', 65, [86, 355, 420, 575], 'p65-q16ai-working', '2025 HL Q16(a)(i)', True,
  'Official working. Label A: total cost minus fixed cost = variable cost, €70 − €60 = €10. Label B: average cost = total cost over output of smoothies = €115 over 60. Answer = €1.92.'),
 ('scheme', 68, [86, 186, 520, 420], 'p68-q16bii-lrac', '2025 HL Q16(b)(ii)', True,
  'Official LRAC diagram. Average cost on the vertical axis, Output on the horizontal. Five U-shaped short-run curves SRAC1 to SRAC5 at outputs Q1 to Q5; the LRAC envelope touches each, falling to its minimum at Q3 and rising after it.'),
 ('paper', 8, [52, 268, 545, 560], 'p08-q6b-question', '2025 HL Section A Q6(b)', False, None),
 ('paper', 13, [52, 117, 545, 424], 'p13-q11ai-question', '2025 HL Q11(a)(i)', False, 'p13-i0'),
 ('paper', 21, [52, 55, 545, 343], 'p21-q13ai-question', '2025 HL Q13(a)(i)', False, 'p21-i0'),
 ('paper', 26, [52, 256, 545, 756], 'p26-q14bi-question', '2025 HL Q14(b)(i)', False, 'p26-i0'),
 ('paper', 30, [52, 55, 545, 338], 'p30-q15bi-question', '2025 HL Q15(b)(i)', False, 'p30-i0'),
 ('paper', 33, [52, 55, 545, 270], 'p33-q16ai-question', '2025 HL Q16(a)(i)', False, 'p33-i0'),
 ('paper', 34, [52, 256, 548, 602], 'p34-q16bii-question', '2025 HL Q16(b)(ii)', False, 'p34-i0'),
]
QALT = {
 'p08-q6b-question': 'The question’s free labour market diagram: wage rate on the vertical axis, quantity of workers on the horizontal; supply SL and demand DL cross at the equilibrium wage WE and quantity QE.',
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
    key = f'economics-2025-HL-{kind}-{slug}'
    fname = key + '.png'
    src = f'paper-trail-corpus/{"markingschemes" if kind == "scheme" else "exampapers"}/2025/LC034ALP000EV.pdf'
    with fitz.open(f'{W}/{src}') as doc:
        pg = doc[page - 1]
        pg.get_pixmap(matrix=fitz.Matrix(SCALE, SCALE), clip=fitz.Rect(*rect)).save(f'{OUT}/{fname}')
        if kind == 'paper':
            data = QALT.get(slug) or man[f'economics-2025-HL-paper-{alt}']['alt']
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
