"""Render, catalogue and register the 2015 OL figures (idempotent).

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
ATTR = 'SEC Leaving Certificate Economics 2015 Ordinary Level — © State Examinations Commission'
LIG = {'Ɵ': 'ti', 'Ŧ': 'ti', 'Ʃ': 'tt', 'ﬀ': 'ff', 'ﬁ': 'fi', 'ﬂ': 'fl'}
F = [
 ('scheme', 9, [24, 72, 498, 370], 'p09-q1a-diagram', '2015 OL Section B Q1(a)(ii)', True,
  'The marking scheme’s completed diagram: P against Q, a falling AR line, a steeper falling MR line, a U-shaped AC curve '
  'touching AR at a dot and an MC curve rising through S, where MC meets MR. An arrow runs down from S to Q1 on the '
  'quantity axis, and from the dot on AR an arrow runs left to P1 on the price axis.'),
 ('scheme', 12, [60, 333, 576, 655], 'p12-q2a-graph', '2015 OL Section B Q2(a)', True,
  'The marking scheme’s completed graph: Price € 100 to 500 on the vertical axis and Quantity (units) 10,000 to 50,000 on '
  'the horizontal. A falling line D/C through five dots and a rising line S/C through five dots cross at 300 and 30,000; '
  'an arrow runs left from the crossing to P1 300 and an arrow runs down to Q1 30,000.'),
 ('scheme', 22, [78, 558, 435, 642], 'p22-q5aiii-working', '2015 OL Section B Q5(a)(iii)', True,
  'The marking scheme’s working: New visible imports: €24,200 m + €1,000 m = €25,200 m; New Balance of Trade: €25,000 m '
  '- €25,200 m = - €200; It is a deficit. A raised 1 sits beside each figure added or subtracted and a raised 2 beside '
  'each result and beside deficit.'),
 ('scheme', 25, [185, 220, 410, 250], 'p25-q6ai-working', '2015 OL Section B Q6(a)(i)', True,
  'The marking scheme’s working: €45,255 m - €48,985 m = (€ 3,730), with a raised 1 beside €45,255, beside the minus sign '
  'and beside €48,985, and a raised 2 beside the answer.'),
 ('scheme', 33, [245, 458, 350, 538], 'p33-q8cii-working', '2015 OL Section B Q8(c)(ii)', True,
  'The marking scheme’s working: 1* over 0.3* + 0.2*, and beneath it the answer 2*.'),
 ('paper', 2, [60, 186, 562, 255], 'p02-q1-table', '2015 OL Section A Q1', False, 'DATA'),
 ('paper', 5, [24, 203, 498, 468], 'p05-q1-diagram', '2015 OL Section B Q1(a)', False, 'DATA'),
 ('paper', 6, [100, 76, 500, 262], 'p06-q2-table', '2015 OL Section B Q2(a)', False, 'DATA'),
 ('paper', 7, [60, 84, 558, 190], 'p07-q3-table', '2015 OL Section B Q3(a)(ii)', False, 'DATA'),
 ('paper', 8, [94, 91, 575, 140], 'p08-q5a-table', '2015 OL Section B Q5(a)', False, 'DATA'),
 ('paper', 10, [70, 95, 512, 282], 'p10-q8a-diagram', '2015 OL Section B Q8(a)', False, 'DATA'),
 ('paper', 10, [328, 549, 410, 583], 'p10-q8c-formula', '2015 OL Section B Q8(c)', False, 'DATA'),
]
QALT = {}
DATA_ALT = {
 'p02-q1-table': 'A table of two rows. Factor of Production: LAND, (ii) blank, CAPITAL, (iv) blank. Example: (i) blank, '
                 'TEACHER, (iii) blank, BUSINESS OWNER.',
 'p05-q1-diagram': 'A diagram with P on the vertical axis and Q on the horizontal: a falling AR line, a steeper falling line '
                   'marked Marginal Revenue, a U-shaped AC curve touching AR at a dot and an MC curve rising through the '
                   'point S, where it meets the Marginal Revenue line. The labels P, Q, AC, MC and AR are circled.',
 'p06-q2-table': 'A table: Price € 100, 200, 300, 400, 500; Quantity Demanded (units) 50,000, 40,000, 30,000, 20,000, '
                 '10,000; Quantity Supplied (units) 10,000, 20,000, 30,000, 40,000, 50,000.',
 'p07-q3-table': 'A table in €: for 1 to 4 units of output, Fixed Costs 2,000 each; Variable Costs 1,000, 1,800, 3,300, '
                 '5,000; Total Costs 3,000, 3,800, A, B; Total Revenue 2,800, 4,300, 6,500, 8,800; Total Profit/Loss (200), '
                 '500, C, D.',
 'p08-q5a-table': 'A table of one row: Visible Exports €million 25,000; Visible Imports €million 24,200; Balance of Trade '
                  '€million ?; Surplus or Deficit ?.',
 'p10-q8a-diagram': 'A circular flow diagram: Households on the left and Firms on the right. A curved line along the top, '
                    'labelled Production of domestic goods/services, has its arrow pointing to Households. Below it line 1 '
                    'runs from Households to Firms; beneath the ovals line 2 runs from Households to Firms and line 3 from '
                    'Firms to Households.',
 'p10-q8c-formula': 'The printed formula: 1 over MPS + MPM.',
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
    key = f'economics-2015-OL-{kind}-{slug}'
    fname = key + '.png'
    src = f'paper-trail-corpus/{"markingschemes" if kind == "scheme" else "exampapers"}/2015/LC034GLP000EV.pdf'
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
    entry.update({'lettersVisible': [], 'labelMeanings': [], 'questionRef': ref, 'year': 2015,
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
