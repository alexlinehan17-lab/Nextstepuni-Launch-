"""Render, catalogue and register the 2019 OL figures (idempotent).

Solution crops come from the scheme and wait for the reveal; question crops are
the whole printed question (stem, data and ask) for cards whose figure slot
holds a solution, because a question crop replaces the typed ask. Data crops
show the paper's own table or diagram. Each crop was rendered at 2x and looked
at before its description was written. Manifest entries are APPENDED as raw text.
"""
from pathlib import Path
import hashlib, json, re, sys
import fitz
W = str(Path(__file__).resolve().parents[5])
OUT = f'{W}/public/exam-figures/economics/markbank'
SCALE = 4
ATTR = 'SEC Leaving Certificate Economics 2019 Ordinary Level — © State Examinations Commission'
LIG = {'Ɵ': 'ti', 'Ŧ': 'ti', 'Ʃ': 'tt', 'ﬀ': 'ff', 'ﬁ': 'fi', 'ﬂ': 'fl'}
F = [
 ('scheme', 6, [80, 505, 400, 668], 'p06-q2-diagram', '2019 OL Section A Q2', True,
  'The marking scheme’s completed diagram: P against Q, a horizontal line D = AR, a U-shaped curve 2 touching it '
  'from above and a curve 1 rising through the point where they meet. From that point an arrow runs left to P1 '
  'on the price axis and down to Q1 on the quantity axis.'),
 ('scheme', 7, [70, 585, 400, 692], 'p07-q5ii-working', '2019 OL Section A Q5(ii)', True,
  'The marking scheme’s working: €46.2 billion - €44 billion = €2.2 billion; then €2.2 billion over €44 billion, '
  'times 100 over 1; Answer: 5%.'),
 ('scheme', 8, [80, 205, 505, 300], 'p08-q6-table', '2019 OL Section A Q6', True,
  'The marking scheme’s completed table: under INJECTIONS, INVESTMENT EXPENDITURE and EXPORTS; under LEAKAGES, '
  'TAXATION and IMPORTS.'),
 ('scheme', 10, [55, 115, 526, 415], 'p10-q1a-diagram', '2019 OL Section B Q1(a)', True,
  'The marking scheme’s completed diagram: circled P on the vertical axis and Q on the horizontal, a downward-'
  'sloping AR line, a steeper MR line, a U-shaped AC curve and a Marginal Cost curve. Marginal cost crosses MR at '
  'X; a line up from X meets AR where AR touches AC, an arrow from there runs left to P1, and an arrow from X runs '
  'down to Q1.'),
 ('scheme', 13, [55, 363, 545, 745], 'p13-q2a-graph', '2019 OL Section B Q2(a)', True,
  'The marking scheme’s graph: Price from 3.00 to 5.00 against Quantity from 100 to 500. D/C falls through five '
  'plotted points from 5.00 at 100 to 3.00 at 500; S/C rises through five from 3.00 at 100 to 5.00 at 500. They '
  'cross at 4.00 and 300, marked P1 and Q1. Beneath: Graph: D/C: 5 points at 2 marks each = 10 marks; S/C: 5 '
  'points at 2 marks each = 10 marks; Labels: P, Q, D/C and S/C = 4 marks; P1 and Q1: 2 x 3 marks each = 6 marks.'),
 ('scheme', 32, [110, 412, 330, 505], 'p32-q7cii-working', '2019 OL Section B Q7(c)(ii)', True,
  'The marking scheme’s working set as a fraction: 1 over 0.1 + 0.4, and the answer 2.'),
 ('paper', 2, [45, 266, 545, 535], 'p02-q2-question', '2019 OL Section A Q2', False, None),
 ('paper', 3, [52, 486, 552, 700], 'p03-q6-question', '2019 OL Section A Q6', False, None),
 ('paper', 5, [55, 186, 525, 452], 'p05-q1a-diagram', '2019 OL Section B Q1(a)', False, 'DATA'),
 ('paper', 5, [52, 168, 552, 568], 'p05-q1a-question', '2019 OL Section B Q1(a)', False, None),
 ('paper', 6, [45, 55, 552, 408], 'p06-q2a-question', '2019 OL Section B Q2(a)', False, None),
 ('paper', 9, [80, 333, 440, 368], 'p09-q7c-formula', '2019 OL Section B Q7(c)', False, 'DATA'),
 ('paper', 9, [80, 333, 552, 492], 'p09-q7c-question', '2019 OL Section B Q7(c)', False, None),
]
QALT = {
 'p02-q2-question': 'A diagram with P on the vertical axis and Q on the horizontal: a horizontal line D = AR, a '
                    'U-shaped curve numbered 2 touching it and a rising curve numbered 1 through the point where they '
                    'meet; beside it an answer box with Number 1 and 2 and a blank Full label column.',
 'p03-q6-question': 'A row of four items, Taxation, Investment Expenditure, Exports and Imports, and a blank answer '
                    'table headed Injections and Leakages.',
 'p05-q1a-question': 'A diagram with circled P and Q on the axes: a downward-sloping line circled AR, a steeper line '
                     'circled MR, a U-shaped curve circled AC and a curve labelled Marginal Cost, which crosses MR at a '
                     'point marked X.',
 'p06-q2a-question': 'A table of Price (€) against Quantity Demanded and Quantity Supplied (units): 5.00, 100, 500; '
                     '4.50, 200, 400; 4.00, 300, 300; 3.50, 400, 200; 3.00, 500, 100.',
 'p09-q7c-question': 'The multiplier formula set as a fraction, 1 over MPS + MPM.',
}
DATA_ALT = {
 'p05-q1a-diagram': 'A diagram with circled P on the vertical axis and Q on the horizontal: a downward-sloping line '
                    'circled AR, a steeper line circled MR, a U-shaped curve circled AC and a curve labelled Marginal '
                    'Cost. Marginal Cost crosses MR at a point marked X, and AR touches AC at a second marked point.',
 'p09-q7c-formula': 'The printed formula: The Multiplier formula for an open economy is: 1 over MPS + MPM.',
}


def tidy(s):
    for a, b in LIG.items():
        s = s.replace(a, b)
    s = re.sub(r'_{3,}', ' ', s.replace('', '✓'))
    return re.sub(r'\s+', ' ', s).strip()


cat_path = f'{W}/scripts/markbank/authored/economics-completion-figures.json'
cat = json.load(open(cat_path))
_order = {c['file']: i for i, c in enumerate(cat)}
man_path = f'{W}/components/MarkBank/figures.json'
man_text = open(man_path).read()
man = json.loads(man_text)
add_entries = []
for kind, page, rect, slug, ref, solution, alt in F:
    key = f'economics-2019-OL-{kind}-{slug}'
    fname = key + '.png'
    src = f'paper-trail-corpus/{"markingschemes" if kind == "scheme" else "exampapers"}/2019/LC034GLP000EV.pdf'
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
    entry.update({'lettersVisible': [], 'labelMeanings': [], 'questionRef': ref, 'year': 2019,
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
