"""Render, catalogue and register the 2016 HL figures (idempotent).

Solution crops come from the scheme and wait for the reveal. Data crops show
the paper's own table or diagram: as the figure beneath the typed ask, or, on a
card whose figure slot holds the solution, as its question figure with the typed
ask kept (econ_legacy_lib.beside_ask). No crop here is a whole printed question:
set at phone width a whole old-syllabus question's text falls near 8 px, so each
crop is the part the ask needs (coordinator rule, 2026-11-04). Each crop was rendered at 2x and looked
at before its description was written. Manifest entries are APPENDED as raw text.

Two crops blank a sliver of a neighbouring print that a rectangle cannot leave
out without cutting the diagram's own axis label (MASK): the paper's Q1 diagram
sits beside the last characters of its ask ("3?"), and the scheme's beside the
right edge of its answer table. Nothing of the diagram itself is touched.
"""
from pathlib import Path
import hashlib, json, re, sys
import fitz
from PIL import Image, ImageDraw
W = str(Path(__file__).resolve().parents[5])
OUT = f'{W}/public/exam-figures/economics/markbank'
SCALE = 4
ATTR = 'SEC Leaving Certificate Economics 2016 Higher Level — © State Examinations Commission'
LIG = {'Ɵ': 'ti', 'Ŧ': 'ti', 'Ʃ': 'tt', 'ﬀ': 'ff', 'ﬁ': 'fi', 'ﬂ': 'fl'}
F = [
 ('scheme', 5, [313, 118, 565, 305], 'p05-q1-diagram', '2016 HL Section A Q1(b)(i)', True,
  'The marking scheme’s completed diagram: Price against Quantity, line 1 rising steeply, U-shaped line 2 and horizontal '
  'line 3. Between line 3 and a lower horizontal line from the point where line 1 crosses line 2, a hatched rectangle is '
  'labelled SNPs, with an arrow pointing to it.'),
 ('scheme', 8, [125, 205, 470, 246], 'p08-q6i-working', '2016 HL Section A Q6(i)', True,
  'The marking scheme’s working: +100 over +€6,000, times €57,000 + €63,000 over 100 + 200, that is €120,000 over 300, '
  'equals +6.67. Each figure, the times sign and the answer’s + sign carry a raised 1.'),
 ('scheme', 11, [30, 432, 570, 599], 'p11-q1aii-diagrams', '2016 HL Section B Q1(a)(ii)', True,
  'The marking scheme’s two diagrams. Movement along a supply curve: one supply curve S labelled, a price rise from P1 to '
  'P2 moving the quantity supplied from Q1 to Q2 along it. Shift in a supply curve: the curve S0 with S Increase to its '
  'right and S decease to its left, arrows showing each shift.'),
 ('scheme', 13, [135, 105, 470, 300], 'p13-q1c-diagram', '2016 HL Section B Q1(c)', True,
  'The marking scheme’s diagram: P against Q, a vertical supply curve S at 30,000 and a falling demand curve D. They cross '
  'at P1. At the lower ticket price P2 the quantity demanded is more than 30,000, and the gap is labelled Excess Demand.'),
 ('scheme', 15, [160, 105, 480, 355], 'p15-q2aiii-diagram', '2016 HL Section B Q2(a)(iii)', True,
  'The marking scheme’s kinked demand curve: P against Q, a shallow segment from A to B and a steep segment from B to C, '
  'kinked at B, with P1 and Q1 marked at the kink.'),
 ('scheme', 22, [65, 140, 505, 256], 'p22-q4bii-table', '2016 HL Section B Q4(b)(ii)', True,
  'The marking scheme’s table: Output 1 to 5, Price 20, Total Revenue 20 to 100, Total Cost 42, 60, 77, 97, 130; MR '
  '40 - 20 = 20, 60 - 40 = 20, 80 - 60 = 20, 100 - 80 = 20; MC 60 - 42 = 18, 77 - 60 = 17, 97 - 77 = 20, 130 - 97 = 33. '
  'The row for output 4 is boxed.'),
 ('scheme', 22, [68, 338, 505, 600], 'p22-q4biii-graph', '2016 HL Section B Q4(b)(iii)', True,
  'The marking scheme’s graph, MC and MR: Price / Costs 0 to 45 against Quantity 1 to 5. MR is horizontal at 20; MC falls '
  'slightly from output 2 to 3 and then rises, crossing MR at output 4, where an arrow points down to the quantity axis.'),
 ('scheme', 26, [65, 438, 550, 612], 'p26-q5biii-working', '2016 HL Section B Q5(b)(iii)', True,
  'The marking scheme’s two methods. Method 1: 1 over 0.2 + 0.2, then 1 over 0.4, then 2.5. Method 2: 1 over 1 - (0.8 - '
  '0.2), then 1 over 1 - 0.6, then 2.5. A star marks each item worth 1 mark; the correct answer is 4 marks.'),
 ('scheme', 26, [70, 680, 470, 750], 'p26-q5biv-working', '2016 HL Section B Q5(b)(iv)', True,
  'The marking scheme’s working: Shortfall in national income: €620m - €500m = €120m; So the government must increase '
  'spending by: €120m over 2.5 = €48m. Each of the five figures carries a raised 2.'),
 ('paper', 2, [318, 118, 578, 296], 'p02-q1-diagram', '2016 HL Section A Q1', False, 'DATA'),
 ('paper', 6, [100, 415, 500, 510], 'p06-q4b-table', '2016 HL Section B Q4(b)', False, 'DATA'),
]
MASK = {
 'p02-q1-diagram': [(318, 145, 330.5, 159)],    # "3?", the end of the ask's own line
 'p05-q1-diagram': [(313, 190, 318, 280)],      # the answer table's right-hand border
}
QALT = {}
DATA_ALT = {
 'p02-q1-diagram': 'A diagram with Price on the vertical axis and Quantity on the horizontal: line 1 rises steeply, line 2 '
                   'is U-shaped and line 3 is horizontal, line 1 crossing line 2 below line 3.',
 'p06-q4b-table': 'A table: Output 1 to 5; Price (€) 20 at every output; Total Revenue (€) 20, 40, 60, 80, 100; Total '
                  'Cost (€) 42, 60, 77, 97, 130.',
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
    key = f'economics-2016-HL-{kind}-{slug}'
    fname = key + '.png'
    src = f'paper-trail-corpus/{"markingschemes" if kind == "scheme" else "exampapers"}/2016/LC034ALP000EV.pdf'
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
    entry.update({'lettersVisible': [], 'labelMeanings': [], 'questionRef': ref, 'year': 2016,
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
