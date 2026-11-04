"""Render, catalogue and register the 2021 HL review figures (idempotent).

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
ATTR = 'SEC Leaving Certificate Economics 2021 Higher Level — © State Examinations Commission'
LIG = {'Ɵ': 'ti', 'Ŧ': 'ti', 'Ʃ': 'tt', 'ﬀ': 'ff', 'ﬁ': 'fi', 'ﬂ': 'fl'}
F = [
 ('paper', 4, [52, 55, 545, 276], 'p04-q2-question', '2021 HL Section A Q2', False, None),
 ('paper', 4, [108, 362, 462, 527], 'p04-q3-chart', '2021 HL Section A Q3', False, 'DATA'),
 ('paper', 12, [130, 100, 420, 143], 'p12-q8-ratios', '2021 HL Section A Q8', False, 'DATA'),
 ('paper', 22, [52, 55, 545, 496], 'p22-q13a-question', '2021 HL Q13(a)', False, None),
 ('scheme', 22, [100, 196, 510, 512], 'p22-q13ai-diagram', '2021 HL Q13(a)(i)', True,
  'The marking scheme’s completed diagram: Price/€ on the vertical axis and Quantity on the horizontal. '
  'A vertical supply line S1 stands at QE; a downward-sloping demand line D1 cuts it at the equilibrium price P1. '
  'A dashed line at €500, below P1, meets D1 at QX, to the right of QE, and a brace under the axis from QE '
  'to QX is labelled Excess Demand. Beneath it a table reads: 1 mark for each of the following correctly '
  'labelled points = 8 marks: Price, Quantity, QE, QX, D1, S1, P = €500, Excess Demand from QE to QX.'),
 ('scheme', 24, [150, 450, 430, 488], 'p24-q13ci-working', '2021 HL Q13(c)(i)', True,
  'The marking scheme’s working set as fractions: +5000 over −35, multiplied by 160 + 125 (285) over '
  '10,000 + 15,000 (25,000), equals −1.63.'),
 ('scheme', 30, [66, 626, 510, 781], 'p30-q15cii-working', '2021 HL Q15(c)(ii)', True,
  'The marking scheme’s working in two columns. Left: 1 over (1 − MPC) + MPM + MPT, then 1 over '
  '(1 − 0.65) + 0.25 + 0.10, Multiplier = 1.43. Right: MPS = 1 − 0.65 = 0.35, then 1 over MPS + MPM + '
  'MPT, then 1 over 0.35 + 0.25 + 0.10, Multiplier = 1.43.'),
]
QALT = {
 'p04-q2-question': 'A four-row table headed Statement, Positive Statement and Normative Statement, with the two tick columns blank.',
 'p22-q13a-question': 'A blank diagram box holding only two axes and a vertical line rising from the horizontal axis, with no labels.',
}
DATA_ALT = {
 'p04-q3-chart': 'A column chart headed Netlfix Subscription per month (US $), the vertical axis US dollars $ from 0 to 15 and the horizontal axis Country. Switzerland about 12.4, Ireland about 8.8, Australia about 5.9, Denmark about 11.6 and Rwanda about 8.0.',
 'p12-q8-ratios': 'The ratios printed as fractions: MUx over Px = 2500 over 200 = MUy over Py = 1250 over 100 = MUz over Pz = 75 over ?.',
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
    key = f'economics-2021-HL-{kind}-{slug}'
    fname = key + '.png'
    src = f'paper-trail-corpus/{"markingschemes" if kind == "scheme" else "exampapers"}/2021/LC034ALP000EV.pdf'
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
