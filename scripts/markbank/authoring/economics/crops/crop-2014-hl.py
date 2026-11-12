"""Render, catalogue and register the 2014 HL figures (idempotent).

Solution crops come from the scheme and wait for the reveal. Data crops show
the paper's own table or diagram: as the figure beneath the typed ask, or, on a
card whose figure slot holds the solution, as its question figure with the typed
ask kept (econ_legacy_lib.beside_ask). No crop here is a whole printed question:
set at phone width a whole old-syllabus question's text falls near 8 px, so each
crop is the part the ask needs (coordinator rule, 2026-11-04). Each crop was rendered at 2x and looked
at before its description was written. Manifest entries are APPENDED as raw text.

One crop blanks a sliver of a neighbouring print that a rectangle cannot leave
out without cutting the diagram's own axis labels (MASK): the scheme's B2(b)(i)
diagram sits above its "Explanation of long run equilibrium:" heading, level with
the Q2 and Quantity labels. Nothing of the diagram itself is touched.
"""
from pathlib import Path
import hashlib, json, re, sys
import fitz
from PIL import Image, ImageDraw
W = str(Path(__file__).resolve().parents[5])
OUT = f'{W}/public/exam-figures/economics/markbank'
SCALE = 4
ATTR = 'SEC Leaving Certificate Economics 2014 Higher Level — © State Examinations Commission'
LIG = {'Ɵ': 'ti', 'Ŧ': 'ti', 'Ʃ': 'tt', 'ﬀ': 'ff', 'ﬁ': 'fi', 'ﬂ': 'fl'}
F = [
 ('scheme', 10, [185, 316, 380, 462], 'p10-q1bi-diagram', '2014 HL Section B Q1(b)(i)', True,
  'The marking scheme’s diagram: P on the vertical axis and Q on the horizontal, and a straight line rising to the right '
  'labelled Supply.'),
 ('scheme', 11, [70, 543, 515, 702], 'p11-q1biii-diagrams', '2014 HL Section B Q1(b)(iii)', True,
  'The marking scheme’s two diagrams, each P against Q. Increase in quantity supplied: S2 to the right of S1, with an '
  'arrow from S1 to S2. Decrease in quantity supplied: S2 to the left of S1, with an arrow from S1 to S2.'),
 ('scheme', 12, [160, 148, 375, 290], 'p12-q1ci-diagram', '2014 HL Section B Q1(c)(i)', True,
  'The marking scheme’s diagram: P against Q, a vertical Supply line at 80,000 and a falling Demand line crossing it level '
  'with €65 on the price axis.'),
 ('scheme', 14, [135, 80, 395, 280], 'p14-q2bi-diagram', '2014 HL Section B Q2(b)(i)', True,
  'The marking scheme’s diagram: Price against Quantity, a falling D=AR line and a steeper MR line, a U-shaped AC curve '
  'touching D=AR at C and an MC curve rising through X, where it cuts MR, and through W, the lowest point of AC. Dashed '
  'lines run from C to P2 on the price axis and from C down through X to Q2.'),
 ('scheme', 17, [140, 150, 440, 190], 'p17-q3b-working', '2014 HL Section B Q3(b)', True,
  'The marking scheme’s working: -1 over 10c, times €1.60 + €1.70 (€3.30) over 20 + 19 (39), = -0.846 (-0.85).'),
 ('scheme', 23, [58, 250, 360, 335], 'p23-q5ai-working', '2014 HL Section B Q5(a)(i)', True,
  'The marking scheme’s working, headed (i) Consumption in 2013: Y = C + I + G + X – M; 80,000 = C + 10,000 + 40,000 + '
  '100,000 – 120,000; 80,000 = C + 30,000; 80,000 – 30,000 = C; C = 50,000.'),
 ('scheme', 23, [58, 378, 270, 462], 'p23-q5aii-working', '2014 HL Section B Q5(a)(ii)', True,
  'The marking scheme’s working, headed (ii) Marginal Propensity to Consume: MPC = ΔC over ΔY; MPC = 6,000 over 10,000 '
  '= 0.6 (60%).'),
 ('scheme', 23, [58, 505, 360, 585], 'p23-q5aiii-working', '2014 HL Section B Q5(a)(iii)', True,
  'The marking scheme’s working, headed (iii) Imports in 2014: Y = C + I + G + X – M; 90,000 = 56,000 + 15,000 + 34,000 '
  '+ 110,000 – M; 90,000 = 215,000 – M; M = 125,000.'),
 ('scheme', 23, [58, 637, 270, 722], 'p23-q5aiv-working', '2014 HL Section B Q5(a)(iv)', True,
  'The marking scheme’s working, headed (iv) Marginal Propensity to Import: MPM = ΔM over ΔY; MPM = 5,000 over 10,000 '
  '= 0.5 (50%).'),
 ('scheme', 25, [40, 416, 572, 695], 'p25-q5cii-response', '2014 HL Section B Q5(c)(ii)', True,
  'The marking scheme’s possible response, six bullets: GNP = GDP + Net Factor Income from Abroad (NFIA); GDP measures '
  'the value of all goods and services produced in the country in the period, the fundamental measure of economic '
  'activity; the difference between GDP and GNP is significant in Ireland as NFIA is a relatively large negative; NFIA '
  'is negative because the profits repatriated by MNCs exceed those returned by Irish MNCs abroad, and interest on Irish '
  'debt held by non-residents adds to it; these outflows keep GDP consistently and considerably larger than GNP in '
  'Ireland; although GDP is used for comparison with other EU countries, GNP is probably a better measure of Irish '
  'economic activity, as it reflects only the part produced and shared by Irish nationals.'),
 ('paper', 5, [100, 205, 505, 278], 'p05-q1a-table', '2014 HL Section B Q1(a)', False, 'DATA'),
 ('paper', 7, [82, 108, 522, 177], 'p07-q5a-table', '2014 HL Section B Q5(a)', False, 'DATA'),
]
MASK = {
 'p14-q2bi-diagram': [(135, 255, 243, 271)],   # "Explanation of long run equilibrium:", the heading below
}
QALT = {}
DATA_ALT = {
 'p05-q1a-table': 'A table: No of Units Consumed 1, 2, 3, 4, 5; Total Utility in Units/Utils 20, 45, 60, 70, 75; '
                  'Marginal Utility in Units/Utils 20, 25, 15, 10, 5.',
 'p07-q5a-table': 'A table of Y, C, I, G, X and M. 2013: €80,000, €?, €10,000, €40,000, €100,000, €120,000. 2014: '
                  '€90,000, €56,000, €15,000, €34,000, €110,000, €?.',
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
    key = f'economics-2014-HL-{kind}-{slug}'
    fname = key + '.png'
    src = f'paper-trail-corpus/{"markingschemes" if kind == "scheme" else "exampapers"}/2014/LC034ALP000EV.pdf'
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
    entry.update({'lettersVisible': [], 'labelMeanings': [], 'questionRef': ref, 'year': 2014,
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
