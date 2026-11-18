"""Render, catalogue and register the 2018 HL figures (idempotent).

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
ATTR = 'SEC Leaving Certificate Economics 2018 Higher Level — © State Examinations Commission'
LIG = {'Ɵ': 'ti', 'Ŧ': 'ti', 'Ʃ': 'tt', 'ﬀ': 'ff', 'ﬁ': 'fi', 'ﬂ': 'fl'}
F = [
 ('scheme', 8, [65, 100, 500, 282], 'p08-q5-ticks', '2018 HL Section A Q5', True,
  'The marking scheme’s completed table: four statements with TRUE and FALSE columns. Ticks: double counting could '
  'occur when activity is measured by the expenditure method, FALSE; exports are an injection into the circular flow, '
  'TRUE; GDP includes a provision for depreciation, FALSE; primary teacher salaries are transfer payments, FALSE.'),
 ('scheme', 11, [125, 330, 490, 575], 'p11-q1aii-diagram', '2018 HL Section B Q1(a)(ii)', True,
  'The marking scheme’s diagram: Price against Quantity, a rising supply line S and a falling demand line D crossing '
  'at the equilibrium price PE. At the higher price P1 a horizontal line marks the surplus between QD on D and QS on '
  'S, with a downward arrow from the surplus towards PE. Each of the nine labels carries a raised 1, its mark.'),
 ('scheme', 12, [85, 205, 470, 520], 'p12-q1bi-diagram', '2018 HL Section B Q1(b)(i)', True,
  'The marking scheme’s diagram: Price (€) from 20 to 100 against Quantity (units) from 0 to 800. A vertical supply '
  'curve S/C at 400 and a falling demand curve D/C through five plotted points, (0, 100), (200, 80), (400, 60), '
  '(600, 40) and (800, 20), meet at PE 60 and QE 400. The triangle above 60 and left of 400 is shaded as Consumer '
  'Surplus, and the rectangle below 60 and left of 400 as Total Revenue.'),
 ('scheme', 16, [90, 155, 480, 445], 'p16-q2bi-diagram', '2018 HL Section B Q2(b)(i)', True,
  'The marking scheme’s diagram: P against Q, a demand curve kinked at B (A to B shallow, B to C steep, D = AR) and '
  'a marginal revenue line with a vertical gap between D and E below the kink. A U-shaped AC curve touches the '
  'demand curve near G, and the MC curve rises through the gap. Dashed lines from B meet the price axis at P1 and the '
  'quantity axis at Q1.'),
 ('scheme', 18, [40, 418, 505, 690], 'p18-q3a-graph', '2018 HL Section B Q3(a)(ii)', True,
  'The marking scheme’s graph, MC / MR: Costs/Revenue (€) from 0 to 60 against output from 1 to 7. MC passes through '
  '20, 10, 15, 20, 30, 45 and 50 at outputs 1 to 7; MR is a horizontal line at 30. They cross at output 5, marked '
  'with an arrow down to the output axis.'),
 ('scheme', 44, [70, 525, 500, 765], 'p44-q8aiv-working', '2018 HL Section B Q8(a)(iv)', True,
  'The marking scheme’s workings set as fractions. MPC = change in C over change in Y = 20,000 over 50,000 = 0.4; MPM '
  '= 10,000 over 50,000 = 0.2; MPS = 1 – MPC = 0.6. Method 1: 1 over MPS + MPM, 1 over 0.6 + 0.2, 1 over 0.8, 1.25. '
  'Method 2: 1 over 1 – (MPC – MPM), 1 over 1 – (0.4 – 0.2), 1 over 0.8, 1.25. Also: MUL = increase in income over '
  'increase in injections, 50,000 over 10,000 + 30,000, 1.25.'),
 ('paper', 3, [85, 322, 545, 460], 'p03-q5-table', '2018 HL Section A Q5', False, 'DATA'),
 ('paper', 6, [133, 336, 540, 440], 'p06-q1b-table', '2018 HL Section B Q1(b)', False, 'DATA'),
 ('paper', 7, [124, 424, 520, 466], 'p07-q3a-table', '2018 HL Section B Q3(a)', False, 'DATA'),
 ('paper', 10, [122, 97, 495, 152], 'p10-q8a-table', '2018 HL Section B Q8(a)', False, 'DATA'),
]
QALT = {}
DATA_ALT = {
 'p03-q5-table': 'A table of four statements with blank TRUE and FALSE columns: ‘Double counting’ could occur when '
                 'economic activity is measured using the expenditure method; Exports represent an injection into the '
                 'circular flow of income; Gross Domestic Product (GDP) includes a provision for depreciation; Primary '
                 'school teacher salaries are categorised as transfer payments in Ireland.',
 'p06-q1b-table': 'A table: Price (€) €100, €80, €60, €40, €20; Quantity Demanded 0, 200, 400, 600, 800; Quantity '
                  'Supplied 400 at every price.',
 'p07-q3a-table': 'A table: Output (units) 0 to 7; Total Cost (€) 20, 40, 50, 65, 85, 115, 160, 210.',
 'p10-q8a-table': 'A table with columns Y, C, I, X and M. 2016: ?, 80,000, 20,000, 90,000, 90,000. 2017: 150,000, '
                  '100,000, 30,000, 120,000, ?.',
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
    key = f'economics-2018-HL-{kind}-{slug}'
    fname = key + '.png'
    src = f'paper-trail-corpus/{"markingschemes" if kind == "scheme" else "exampapers"}/2018/LC034ALP000EV.pdf'
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
