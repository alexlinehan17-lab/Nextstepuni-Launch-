"""Render, catalogue and register the 2018 OL figures (idempotent).

Solution crops come from the scheme and wait for the reveal. Data crops show
the paper's own table or diagram: as the figure beneath the typed ask, or, on a
card whose figure slot holds the solution, as its question figure with the typed
ask kept (econ_legacy_lib.beside_ask). No crop here is a whole printed question:
set at phone width a whole old-syllabus question's text falls near 8 px, so each
crop is the part the ask needs (coordinator rule, 2026-11-04). Each crop was rendered at 2x and looked
at before its description was written. Manifest entries are APPENDED as raw text.
"""
from pathlib import Path
import hashlib, json, re, sys
import fitz
W = str(Path(__file__).resolve().parents[5])
OUT = f'{W}/public/exam-figures/economics/markbank'
SCALE = 4
ATTR = 'SEC Leaving Certificate Economics 2018 Ordinary Level — © State Examinations Commission'
LIG = {'Ɵ': 'ti', 'Ŧ': 'ti', 'Ʃ': 'tt', 'ﬀ': 'ff', 'ﬁ': 'fi', 'ﬂ': 'fl'}
F = [
 ('scheme', 11, [60, 130, 524, 350], 'p11-q1a-diagram', '2018 OL Section B Q1(a)(ii)', True,
  'The marking scheme’s completed diagram: Price against Quantity, a horizontal line D = AR = MR, a U-shaped AC curve '
  'touching it at B and an MC curve rising through B. From B a line runs left to P1 on the price axis and an arrow '
  'runs down to Q1 on the quantity axis.'),
 ('paper', 2, [85, 318, 300, 475], 'p02-q2-diagram', '2018 OL Section A Q2', False, 'DATA'),
 ('paper', 4, [115, 102, 530, 358], 'p04-q8-diagram', '2018 OL Section A Q8', False, 'DATA'),
 ('paper', 5, [60, 225, 545, 430], 'p05-q1-diagram', '2018 OL Section B Q1(a)', False, 'DATA'),
 ('paper', 6, [72, 185, 530, 268], 'p06-q2a-table', '2018 OL Section B Q2(a)', False, 'DATA'),
 ('paper', 6, [160, 318, 445, 476], 'p06-q2b-diagram', '2018 OL Section B Q2(b)', False, 'DATA'),
 ('paper', 7, [85, 215, 545, 275], 'p07-q3b-table', '2018 OL Section B Q3(b)', False, 'DATA'),
 ('paper', 8, [80, 92, 545, 128], 'p08-q5a-table', '2018 OL Section B Q5(a)', False, 'DATA'),
]
QALT = {}
DATA_ALT = {
 'p02-q2-diagram': 'A diagram with P on the vertical axis and Q on the horizontal: three lines numbered 1 to 3 and a line '
                   'labelled MR. Line 1 rises steeply, line 2 is U-shaped and line 3 falls from left to right. From the '
                   'point where line 1 crosses line 2, an arrow runs left to P1 and an arrow runs down to Q1.',
 'p04-q8-diagram': 'A circular flow diagram: Households and Firms joined by arrows labelled Supply factors of production, '
                   'Supply goods and services and Spending on goods and services; an arrow from Firms to Households '
                   'numbered 1; from Households to Financial Institutions an arrow numbered 2, and from there '
                   'Investments to Firms; from Households Imports to Foreign Markets, and from Foreign Markets an arrow '
                   'numbered 3 to Firms.',
 'p05-q1-diagram': 'A diagram with Price on the vertical axis and Quantity on the horizontal: a horizontal line labelled '
                   'D = AR = MR, a U-shaped AC curve touching it at point B and an MC curve rising through B. The labels '
                   'MC, AC, D, AR and MR are underlined.',
 'p06-q2a-table': 'A table: Number of units consumed 1 to 6; Total utility in units/utils 15, 35, 70, 110, 130, 140; '
                  'Marginal Utility in units/utils 15, 20, 35, A, B, C.',
 'p06-q2b-diagram': 'A diagram with Price on the vertical axis and Quantity on the horizontal: a bold downward-sloping '
                    'demand curve D1 and a parallel demand curve D2 to its right, with arrows pointing right from D1 to D2.',
 'p07-q3b-table': 'A table: Output (units) 0, 100, 200, 300, 400; Total Cost (€) 300, 500, 600, 1,050, 1,500; Total '
                  'Revenue (€) 0, 1,000, A, B, C.',
 'p08-q5a-table': 'A table: Government Current Income €67.4 bn; Government Current Expenditure €70.1 bn.',
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
    key = f'economics-2018-OL-{kind}-{slug}'
    fname = key + '.png'
    src = f'paper-trail-corpus/{"markingschemes" if kind == "scheme" else "exampapers"}/2018/LC034GLP000EV.pdf'
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
    entry.update({'lettersVisible': [], 'labelMeanings': [], 'questionRef': ref, 'year': 2018,
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
