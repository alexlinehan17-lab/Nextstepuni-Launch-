"""Render, catalogue and register the 2020 HL figures (idempotent).

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
ATTR = 'SEC Leaving Certificate Economics 2020 Higher Level — © State Examinations Commission'
LIG = {'Ɵ': 'ti', 'Ŧ': 'ti', 'Ʃ': 'tt', 'ﬀ': 'ff', 'ﬁ': 'fi', 'ﬂ': 'fl'}
F = [
 ('scheme', 6, [110, 462, 390, 625], 'p06-q4i-diagram', '2020 HL Section A Q4(i)', True,
  'The marking scheme’s completed diagram: Price against Quantity, a downward-sloping demand line D1 and two '
  'upward-sloping supply lines, S1 and S2 to its right, with arrows pointing right. Dashed lines run from E1 to P1 '
  'and Q1, and from E2 to the lower price P2 and the higher quantity Q2.'),
 ('scheme', 11, [318, 118, 530, 295], 'p11-q9-diagram', '2020 HL Section A Q9(ii)', True,
  'The marking scheme’s completed diagram: Price against Quantity, a kinked demand curve D=AR with a broken MR line '
  'below the kink and a U-shaped MC curve passing through the gap in MR at E. A dashed line from the kink meets the '
  'price axis at P1, and a dashed line down from the kink through E meets the quantity axis at Q1.'),
 ('scheme', 13, [115, 95, 380, 262], 'p13-q1bi-diagram', '2020 HL Section B Q1(b)(i)', True,
  'The marking scheme’s diagram: Price against Quantity, an upward-sloping supply curve S and two downward-sloping '
  'demand curves, D1 and D2 to its left. The equilibrium moves from E1 (P1, Q1) to E2 at a lower price P2 and a lower '
  'quantity Q2, with a downward arrow beside the price axis.'),
 ('scheme', 17, [68, 115, 508, 422], 'p17-q2bi-diagram', '2020 HL Section B Q2(b)(i)', True,
  'The marking scheme’s completed diagram: Price against Quantity, a downward-sloping D=AR line, a steeper MR line, a '
  'U-shaped AC curve and an MC curve rising through the lowest point of AC. MC crosses MR at E; a dashed line up from '
  'E meets AC at Y and D=AR at X, and down to Q1. Dashed lines from X and Y meet the price axis at P1 and C1, and the '
  'rectangle between them is labelled SNP. Beneath it a row of nine cells reads D=AR, MR, MC, AC, Correct Equilibrium '
  'point - E, P1, C1, Q1, SNP accurately shown.'),
 ('scheme', 18, [115, 145, 415, 372], 'p18-q2bii-diagram', '2020 HL Section B Q2(b)(ii)', True,
  'The marking scheme’s diagram: Price against Quantity, a demand line D2=AR2 and its MR line, a U-shaped ATC curve '
  'and an MC curve. D2=AR2 just touches ATC at A; MC crosses MR at E directly below A. A dashed line from A meets the '
  'price axis at P1/C1 and a dashed line down through E meets the quantity axis at Q1.'),
 ('scheme', 25, [100, 122, 475, 245], 'p25-q4bi-table', '2020 HL Section B Q4(b)(i)', True,
  'The marking scheme’s completed table. Output 0 to 5; Total Cost 10, 20, 27, 36, 52, 80; Marginal Cost -, 10, 7, '
  '9, 16, 28; Average Total Cost -, 20, 13.5, 12, 13, 16.'),
 ('scheme', 25, [70, 388, 498, 602], 'p25-q4bii-graph', '2020 HL Section B Q4(b)(ii)', True,
  'The marking scheme’s graph, Marginal Cost vs Average Cost: € Cost from 0 to 30 against Output from 1 to 6. MC '
  'passes through 10, 7, 9, 16 and 28 at outputs 1 to 5; ATC through 20, 13.5, 12, 13 and 16. MC falls below ATC, '
  'then rises through ATC at its lowest point, between outputs 3 and 4.'),
 ('scheme', 39, [105, 370, 440, 408], 'p39-q8biv-working', '2020 HL Section B Q8(b)(iv)', True,
  'The marking scheme’s working set as fractions: change in imports over change in income equals 65,000 – 60,000 over '
  '250,000 – 200,000, equals 5,000 over 50,000, equals 0.1.'),
 ('scheme', 39, [75, 460, 500, 645], 'p39-q8bv-working', '2020 HL Section B Q8(b)(v)', True,
  'The marking scheme’s workings set as fractions. Change in consumption over change in income equals 105,000 – '
  '70,000 over 250,000 – 200,000, equals 35,000 over 50,000, equals 0.7; MPS = 1 – 0.7 = 0.3. Left: 1 over (1-MPC) + '
  'MPM, then 1 over (1-0.7) + 0.1, Multiplier = 2.5. Right: 1 over MPS + MPM, then 1 over 0.3 + 0.1, Multiplier = 2.5.'),
 ('paper', 3, [150, 385, 405, 540], 'p03-q4-diagram', '2020 HL Section A Q4', False, 'DATA'),
 ('paper', 6, [343, 95, 545, 271], 'p06-q9-diagram', '2020 HL Section A Q9', False, 'DATA'),
 ('paper', 7, [93, 194, 504, 256], 'p07-q1a-table', '2020 HL Section B Q1(a)', False, 'DATA'),
 ('paper', 9, [113, 218, 513, 261], 'p09-q4b-table', '2020 HL Section B Q4(b)', False, 'DATA'),
 ('paper', 10, [121, 199, 526, 369], 'p10-q5b-table', '2020 HL Section B Q5(b)', False, 'DATA'),
 ('paper', 10, [131, 539, 521, 586], 'p10-q5c-table', '2020 HL Section B Q5(c)', False, 'DATA'),
 ('paper', 12, [136, 206, 519, 259], 'p12-q8b-table', '2020 HL Section B Q8(b)', False, 'DATA'),
]
QALT = {}
DATA_ALT = {
 'p03-q4-diagram': 'A diagram with Price on the vertical axis and Quantity on the horizontal: a downward-sloping line D1 '
                   'and two upward-sloping lines, S1 and S2 to its right, with arrows pointing right. D1 crosses S1 at '
                   'E1 and S2 at E2, lower and to the right.',
 'p06-q9-diagram': 'A diagram with Quantity on the horizontal axis and three lines numbered 1 to 3: line 2 a demand '
                   'curve with a kink, line 3 a marginal revenue line that drops vertically below the kink and then '
                   'falls again, and line 1 a U-shaped curve rising through the vertical gap.',
 'p07-q1a-table': 'A table: No. of Units Consumed 1, 2, 3, 4, 5; Total Utility in Units / Utils 10, 25, 37, 47, 54; '
                  'Marginal Utility in Units / Utils 10, A, B, C, D.',
 'p09-q4b-table': 'A table: Output (Q) 0, 1, 2, 3, 4, 5; Total Cost (TC) 10, 20, 27, 36, 52, 80.',
 'p10-q5b-table': 'A table of seven rows headed Units of labour employed, Total output per week (units), Marginal '
                  'product (units), Price of output, Marginal revenue product of labour and Marginal cost of labour. '
                  'Units 1 to 7 give total output 10, 25, 45, 60, 70, 77 and 82; price €20 and marginal cost €140 in '
                  'every row; the first row alone shows marginal product 10 and marginal revenue product €200, the '
                  'rest blank.',
 'p10-q5c-table': 'A table with columns EU and US: Price elasticity of demand –0.8 and –2.4; Income elasticity of '
                  'demand +0.72 and +2.8.',
 'p12-q8b-table': 'A table with columns Y, C, I, G, X and M. 2018: €200,000, €70,000, €50,000, ?, €80,000, €60,000. '
                  '2019: ?, €105,000, €55,000, €65,000, €90,000, €65,000.',
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
    key = f'economics-2020-HL-{kind}-{slug}'
    fname = key + '.png'
    src = f'paper-trail-corpus/{"markingschemes" if kind == "scheme" else "exampapers"}/2020/LC034ALP000EV.pdf'
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
    entry.update({'lettersVisible': [], 'labelMeanings': [], 'questionRef': ref, 'year': 2020,
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
