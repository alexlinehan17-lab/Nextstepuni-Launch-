"""Render, catalogue and register the 2011 HL figures (idempotent).

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
ATTR = 'SEC Leaving Certificate Economics 2011 Higher Level — © State Examinations Commission'
LIG = {'Ɵ': 'ti', 'Ŧ': 'ti', 'Ʃ': 'tt', 'ﬀ': 'ff', 'ﬁ': 'fi', 'ﬂ': 'fl'}
F = [
 ('scheme', 8, [200, 124, 460, 252], 'p08-q8-working', '2011 HL Section A Q8', True,
  'The marking scheme’s working: the formula, the change in QA over the change in PB, times (PB1 + PB2) over (QA1 + QA2); '
  'then -8 over €2, times (€8 + €10) (18) over (20 + 12) (32); = -2.25.'),
 ('scheme', 9, [40, 172, 550, 660], 'p09-q1aii-diagrams', '2011 HL Section B Q1(a)(ii)', True,
  'The marking scheme’s three demand diagrams, P against Q (units), each a falling D line through three points at €15, €10 '
  'and €5. Consumer A: 20, 40 and 60 units (3 marks). Consumer B: 40, 60 and 80 units (3 marks). Market: 60, 100 and 140 '
  'units (5 marks). Circled numbers mark the marks for each axis and curve.'),
 ('scheme', 10, [28, 155, 520, 456], 'p10-q1bi-diagrams', '2011 HL Section B Q1(b)(i)', True,
  'The marking scheme’s two diagrams. A movement along: one falling D/C, the price falling from P1 to P2 and the quantity '
  'rising from Q1 to Q2, an arrow down along the curve. A shift in a demand curve, with the scheme’s explanation: D/C 1 and '
  'D/C2 to its right, an arrow pointing right.'),
 ('scheme', 11, [240, 652, 360, 732], 'p11-q1cii-working', '2011 HL Section B Q1(c)(ii)', True,
  'The marking scheme’s working: 40 over 80 = X over 150; = 75 utils.'),
 ('scheme', 14, [40, 195, 560, 445], 'p14-q2b-diagram', '2011 HL Section B Q2(b)(i)–(ii)', True,
  'The marking scheme’s diagram with its list of nine elements (Price axis, Quantity axis, Kinked D/C, Distinct MR curve, MC, '
  'AC, P1, Q1, Point G): P against Q, a demand curve ABC kinked at B level with P1, an MR curve with a vertical gap from D '
  'to E below B, an MC curve rising through the gap and a U-shaped AC curve, meeting at G above Q1.'),
 ('scheme', 20, [25, 288, 500, 458], 'p20-q4ai-working', '2011 HL Section B Q4(a)(i)', True,
  'The marking scheme’s working. The marginal cost of the 4th unit: €3,300 – €2,250 = €1,050. The average cost of 5 units: '
  '€4,500 over 5 = €900. The profit selling 5 units at €1,200: 5 x €1,200 (€6,000) – €4,500 = €1,500.'),
 ('scheme', 20, [25, 498, 560, 745], 'p20-q4aii-diagram', '2011 HL Section B Q4(a)(ii)', True,
  'The marking scheme’s AC curve, Costs € against output (units): 1,000 at 1, 800 at 2, 750 at 3, 825 at 4 and 900 at 5, '
  'falling to its lowest at 3 units and rising after. Beside it the reasons: it slopes downward because of declining FC '
  'per unit or the specialisation of labour, and upward because of increasing VC per unit under the Law of Diminishing '
  'Marginal Returns.'),
 ('scheme', 30, [60, 266, 545, 516], 'p30-q7bii-working', '2011 HL Section B Q7(b)(ii)', True,
  'The marking scheme’s two methods, 8 marks each. Method 1: 1 over (MPS + MPT + MPM) = 1 over (0.28 + 0.22 + 0.3) = 1 '
  'over 0.8 = 1.25. Method 2: MPC = 1 – MPS = 1 – 0.28 = 0.72, then 1 over (1 – (MPC – MPT – MPM)) = 1 over (1 – (0.72 – '
  '0.22 – 0.3)) = 1 over 0.8 = 1.25.'),
 ('paper', 5, [60, 360, 515, 485], 'p05-q4-table', '2011 HL Section B Q4(a)', False, 'DATA'),
]
MASK = {}
QALT = {}
DATA_ALT = {
 'p05-q4-table': 'A table of a firm’s short-run costs in euro by number of units of output: 1 unit, Fixed Costs 400, Variable '
                 'Costs 600, Total Costs 1,000; 2 units, 400, 1,200, 1,600; 3 units, 400, 1,850, 2,250; 4 units, 400, 2,900, '
                 '3,300; 5 units, 400, 4,100, 4,500.',
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
    key = f'economics-2011-HL-{kind}-{slug}'
    fname = key + '.png'
    src = f'paper-trail-corpus/{"markingschemes" if kind == "scheme" else "exampapers"}/2011/LC034ALP000EV.pdf'
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
    entry.update({'lettersVisible': [], 'labelMeanings': [], 'questionRef': ref, 'year': 2011,
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
