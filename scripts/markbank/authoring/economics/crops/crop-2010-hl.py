"""Render, catalogue and register the 2010 HL figures (idempotent).

Solution crops come from the scheme and wait for the reveal. Data crops show
the paper's own table or diagram: as the figure beneath the typed ask, or, on a
card whose figure slot holds the solution, as its question figure with the typed
ask kept (econ_legacy_lib.beside_ask). No crop here is a whole printed question:
set at phone width a whole old-syllabus question's text falls near 8 px, so each
crop is the part the ask needs (coordinator rule, 2026-11-04). Each crop was rendered at 1.5x and looked
at before its description was written. Manifest entries are APPENDED as raw text.

The Section B Q1(a) diagram is the solution to both (a)(i) and (a)(iii): the
scheme draws the supply curve and the new one on one diagram. The Section B
Q2(c) diagram's first circled mark sits level with the reprinted question's
last line ("• Efficiency." and "(30 marks)"), so that line is masked white.
"""
from pathlib import Path
import hashlib, json, re, sys
import fitz
from PIL import Image, ImageDraw
W = str(Path(__file__).resolve().parents[5])
OUT = f'{W}/public/exam-figures/economics/markbank'
SCALE = 4
ATTR = 'SEC Leaving Certificate Economics 2010 Higher Level — © State Examinations Commission'
LIG = {'Ɵ': 'ti', 'Ŧ': 'ti', 'Ʃ': 'tt', 'ﬀ': 'ff', 'ﬁ': 'fi', 'ﬂ': 'fl'}
F = [
 ('scheme', 4, [38, 86, 440, 242], 'p04-q3-working', '2010 HL Section A Q3', True,
  'The marking scheme’s working. Quantity 1: €200 / €2 = 100 units. Quantity 2: €200 / €2.50 = 80 units. Then -20* over '
  '50*, times €2 + €2.50 (4.50)* over 100 + 80 (180)*, = -* 1.0*; beneath it, 6 * at 2 marks each = 12 marks.'),
 ('scheme', 6, [45, 70, 400, 128], 'p06-q6-working', '2010 HL Section A Q6', True,
  'The marking scheme’s working: 1 over (0.25 + 0.3 + 0.2) = 1.33; beneath it, 5 marks: 1 mark for each item.'),
 ('scheme', 8, [84, 325, 511, 528], 'p08-q1a-diagram', '2010 HL Section B Q1(a)', True,
  'The marking scheme’s diagram, P (1.75 to 3.00) against Q (/1000 units, 5 to 60). The demand curve D falls through 3.00 '
  'at 5, 2.75 at 10, 2.50 at 20, 2.25 at 30 and 2.00 at 40. The supply curve S1 rises through 2.00 at 5, 2.25 at 10, 2.50 '
  'at 20, 2.75 at 30 and 3.00 at 40, and the new supply curve S2 through 2.00 at 25, 2.25 at 30, 2.50 at 40, 2.75 at 50 '
  'and 3.00 at 60. The two equilibrium points are circled, with arrows to both axes: 2.50 and 20 where D meets S1, 2.25 '
  'and 30 where D meets S2.'),
 ('scheme', 13, [26, 99, 572, 534], 'p13-q2c-diagram', '2010 HL Section B Q2(c)', True,
  'The marking scheme’s diagram, P against Q, a circled mark beside each item. A U-shaped AC curve and an MC curve rising '
  'through its lowest point. The perfectly competitive firm’s horizontal D = AR=MR line at PC touches the lowest point of '
  'AC at E, with an arrow down to Qc. The monopoly’s falling D = AR [M] line and the steeper MR line beneath it; MC '
  'crosses MR at F, with an arrow down to QM, and the line up from QM meets D = AR [M] level with PM. Circled 1 beside P, '
  'Q, MC, AC, PM, PC, F, E, QM and Qc; circled 2 beside D = AR=MR, D = AR [M] and MR. Beneath: Diagram, 10 items at 1 '
  'mark each + 3 items at 2 marks each = 16 marks.'),
 ('scheme', 20, [58, 162, 552, 262], 'p20-q5ai-working', '2010 HL Section B Q5(a)(i)', True,
  'The marking scheme’s working for (i) Gross National Product at Factor Cost – 10 marks: GNP @ Market Prices + Price '
  'Subsidies – Indirect Taxes = GNP @ Factor Cost; €200 million + €5 million – €30 million = €175 million*, an arrow from '
  'each figure to its marks: 2 marks, 2 marks, 2 marks and 4 marks.'),
 ('scheme', 20, [58, 300, 552, 416], 'p20-q5aii-working', '2010 HL Section B Q5(a)(ii)', True,
  'The marking scheme’s working for (ii) Net National Product at Factor Cost/National Income – 10 marks: GNP @ Factor '
  'Cost – Depreciation = NNP @ FC; €175 million* – €12 million = €163 million, an arrow from each figure to its marks: 3 '
  'marks, 3 marks and 4 marks.'),
 ('paper', 4, [120, 174, 528, 287], 'p04-q1a-table', '2010 HL Section B Q1(a)', False, 'DATA'),
]
MASK = {'p13-q2c-diagram': [(68, 90, 79, 102.2), (99, 90, 160, 106.4), (508, 90, 572, 106.4)]}
QALT = {}
DATA_ALT = {
 'p04-q1a-table': 'A table of the market schedules for Quencher: Price (€) 2.00, 2.25, 2.50, 2.75 and 3.00; Quantity '
                  'Demanded (’000 units) 40, 30, 20, 10 and 5; Quantity Supplied (’000 units) 5, 10, 20, 30 and 40.',
}

def tidy(s):
    for a, b in LIG.items():
        s = s.replace(a, b)
    s = re.sub(r'_{3,}', ' ', s.replace('', '✓'))
    return re.sub(r'\s+', ' ', s).strip()


cat_path = f'{W}/scripts/markbank/authored/economics-completion-figures.json'
cat = json.load(open(cat_path))
_order = {c['file']: i for i, c in enumerate(cat)}
man_path = f'{W}/components/MarkBank/figures.json'
man_text = open(man_path).read()
man = json.loads(man_text)
add_entries = []
for kind, page, rect, slug, ref, solution, alt in F:
    key = f'economics-2010-HL-{kind}-{slug}'
    fname = key + '.png'
    src = f'paper-trail-corpus/{"markingschemes" if kind == "scheme" else "exampapers"}/2010/LC034ALP000EV.pdf'
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
    entry.update({'lettersVisible': [], 'labelMeanings': [], 'questionRef': ref, 'year': 2010,
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
