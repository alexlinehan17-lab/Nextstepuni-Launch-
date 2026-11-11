"""Render, catalogue and register the 2013 OL figures (idempotent).

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
from PIL import Image, ImageDraw
W = str(Path(__file__).resolve().parents[5])
OUT = f'{W}/public/exam-figures/economics/markbank'
SCALE = 4
ATTR = 'SEC Leaving Certificate Economics 2013 Ordinary Level — © State Examinations Commission'
LIG = {'Ɵ': 'ti', 'Ŧ': 'ti', 'Ʃ': 'tt', 'ﬀ': 'ff', 'ﬁ': 'fi', 'ﬂ': 'fl'}
F = [
 ('scheme', 8, [40, 80, 300, 228], 'p08-q8-diagram', '2013 OL Section A Q8(b)', True,
  'The marking scheme’s diagram: P against Q, curve 1 rising steeply, U-shaped curve 2, a falling D=AR line and a steeper '
  'falling curve 3. A line from Q1 rises to curve 2 and to D=AR; arrows run left from D=AR to P1 and from curve 2 to C1.'),
 ('scheme', 9, [22, 78, 573, 300], 'p09-q1a-diagram', '2013 OL Section B Q1(a)(ii)', True,
  'The marking scheme’s completed diagram: P against Q, a horizontal line D = AR = MR, a U-shaped AC curve touching it at E '
  'and an MC curve rising through E. The line is labelled P1 / C1 on the price axis, and an arrow runs down from E to Q1.'),
 ('scheme', 13, [28, 345, 561, 668], 'p13-q2a-graph', '2013 OL Section B Q2(a)', True,
  'The marking scheme’s completed graph: Price € 300 to 700 on the vertical axis and Quantity (units) 200 to 1,000 on the '
  'horizontal. A falling D/C through five dots and a rising S/C through five dots cross at 500 and 600; an arrow runs left '
  'to PE 500 and an arrow runs down to QE 600.'),
 ('paper', 2, [58, 84, 562, 152], 'p02-q1-table', '2013 OL Section A Q1', False, 'DATA'),
 ('paper', 3, [30, 481, 560, 632], 'p03-q8-diagram', '2013 OL Section A Q8', False, 'DATA'),
 ('paper', 4, [28, 160, 509, 372], 'p04-q1-diagram', '2013 OL Section B Q1(a)', False, 'DATA'),
 ('paper', 5, [85, 88, 470, 202], 'p05-q2a-table', '2013 OL Section B Q2(a)', False, 'DATA'),
 ('paper', 7, [64, 72, 509, 375], 'p07-q5-diagram', '2013 OL Section B Q5', False, 'DATA'),
]
MASK = {}
QALT = {}
DATA_ALT = {
 'p02-q1-table': 'Four items, Carpenter, Business Owner, Natural Gas and Buildings, above a table of the four factors, LAND, '
                 'LABOUR, CAPITAL and ENTERPRISE, each with a blank Represented by box.',
 'p03-q8-diagram': 'A diagram: P against Q, curve 1 rising steeply, U-shaped curve 2, a falling D=AR line and a steeper falling '
                   'curve 3, with a line down to Q1; beside it an answer box with rows for curves 1, 2 and 3 and a blank Name column.',
 'p04-q1-diagram': 'A diagram with P on the vertical axis and Q on the horizontal: a horizontal line D = AR = MR, a U-shaped AC '
                   'curve touching it at E and an MC curve rising through E. The labels P, Q, MC, AC, AR and MR are underlined.',
 'p05-q2a-table': 'A table: Price € 300, 400, 500, 600, 700; Quantity Demanded (units) 1,000, 800, 600, 400, 200; Quantity '
                  'Supplied (units) 200, 400, 600, 800, 1,000.',
 'p07-q5-diagram': 'A circular flow diagram of an open economy without government: Households and Firms joined by Supply '
                   'factors of production and Supply goods & services, with Financial Institutions and Foreign Markets below. '
                   'Line 1 runs from firms to households across the top, line 2 from households to firms, line 3 from '
                   'households to financial institutions, line 4 from households to foreign markets, and line 5 from foreign '
                   'markets up to firms; Investment runs from financial institutions to firms.',
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
    key = f'economics-2013-OL-{kind}-{slug}'
    fname = key + '.png'
    src = f'paper-trail-corpus/{"markingschemes" if kind == "scheme" else "exampapers"}/2013/LC034GLP000EV.pdf'
    with fitz.open(f'{W}/{src}') as doc:
        pg = doc[page - 1]
        pg.get_pixmap(matrix=fitz.Matrix(SCALE, SCALE), clip=fitz.Rect(*rect)).save(f'{OUT}/{fname}')
        if slug in MASK:
            im = Image.open(f'{OUT}/{fname}').convert('RGB')
            for x0, y0, x1, y1 in MASK[slug]:
                ImageDraw.Draw(im).rectangle([(x0 - rect[0]) * SCALE, (y0 - rect[1]) * SCALE,
                                              (x1 - rect[0]) * SCALE, (y1 - rect[1]) * SCALE], fill='white')
            im.save(f'{OUT}/{fname}')
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
    entry.update({'lettersVisible': [], 'labelMeanings': [], 'questionRef': ref, 'year': 2013,
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
