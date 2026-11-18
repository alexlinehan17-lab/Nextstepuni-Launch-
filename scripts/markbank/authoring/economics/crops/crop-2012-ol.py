"""Render, catalogue and register the 2012 OL figures (idempotent).

Solution crops come from the scheme and wait for the reveal. Data crops show
the paper's own table, formula or diagram: as the figure beneath the typed ask,
or, on a card whose figure slot holds the solution, as its question figure with
the typed ask kept (econ_legacy_lib.beside_ask). No crop here is a whole printed
question: set at phone width a whole old-syllabus question's text falls near
8 px, so each crop is the part the ask needs (coordinator rule, 2026-11-04).
Each crop was rendered and looked at before its description was written; the
two diagram crops start just below the sentence printed above them, so none of
its descenders shows. Manifest entries are APPENDED as raw text.

"""
from pathlib import Path
import hashlib, json, re, sys
import fitz
from PIL import Image, ImageDraw
W = str(Path(__file__).resolve().parents[5])
OUT = f'{W}/public/exam-figures/economics/markbank'
SCALE = 4
ATTR = 'SEC Leaving Certificate Economics 2012 Ordinary Level — © State Examinations Commission'
LIG = {'Ɵ': 'ti', 'Ŧ': 'ti', 'Ʃ': 'tt', 'ﬀ': 'ff', 'ﬁ': 'fi', 'ﬂ': 'fl'}
F = [
 ('scheme', 9, [17, 68.5, 505, 345], 'p09-q1a-diagram', '2012 OL Section B Q1(a)(ii)', True,
  'The marking scheme’s diagram: the vertical axis numbered 1 and the horizontal axis 5, a thick falling line 4, a steeper '
  'falling line labelled MR, a U-shaped curve 3 just touching line 4 at a dot, and a curve 2 rising steeply through the dot '
  'E where it crosses MR. An arrow runs left from the dot on line 4 to P1 / C1 on the vertical axis, and a line drops from '
  'that dot through E to Q1 on the horizontal axis; a second Q1 is printed at the left end of the horizontal axis.'),
 ('scheme', 12, [165, 104, 392, 270], 'p12-q2a-diagram', '2012 OL Section B Q2(a)(ii)', True,
  'The marking scheme’s diagram: the vertical axis numbered 1 and the horizontal axis 2, a falling line labelled Demand and '
  'a vertical line 3 crossing it. An arrow runs left from the crossing to P1 on the vertical axis, and Q1 is marked on the '
  'horizontal axis below the vertical line.'),
 ('scheme', 24, [255, 210, 332, 276], 'p24-q5bii-working', '2012 OL Section B Q5(b)(ii)', True,
  'The marking scheme’s working: 1 over 0.3 + 0.2, = 2.'),
 ('scheme', 29, [38, 576, 560, 666], 'p29-q7aiii-working', '2012 OL Section B Q7(a)(iii)', True,
  'The marking scheme’s table of output after specialisation. Germany: Wine 0, Cars 1200* x 2* = 2400*. France: Wine '
  '800* x 2* = 1600*, Cars 0. Total Output: Wine 1600*, Cars 2400*. Its Marks column reads 3 figures x 1 mark each for '
  'Germany and for France, and 2 figures x 1 marks each for the total; each starred figure earns a mark.'),
 ('paper', 2, [32, 160, 576, 250], 'p02-q1b-table', '2012 OL Section A Q1(b)', False, 'DATA'),
 ('paper', 3, [46, 40, 564, 213], 'p03-q6-table', '2012 OL Section A Q6', False, 'DATA'),
 ('paper', 4, [22, 174.5, 496, 442], 'p04-q1-diagram', '2012 OL Section B Q1(a)', False, 'DATA'),
 ('paper', 5, [170, 96, 395, 243], 'p05-q2a-diagram', '2012 OL Section B Q2(a)', False, 'DATA'),
 ('paper', 5, [142, 393, 415, 542], 'p05-q2b-diagram', '2012 OL Section B Q2(b)', False, 'DATA'),
 ('paper', 7, [328, 129, 408, 161], 'p07-q5b-formula', '2012 OL Section B Q5(b)', False, 'DATA'),
 ('paper', 8, [96, 78, 564, 203], 'p08-q7a-table', '2012 OL Section B Q7(a)', False, 'DATA'),
]
MASK = {}
QALT = {}
DATA_ALT = {
 'p02-q1b-table': 'A table of four canons beside four explanations, printed in rows A 1, B 2, C 3 and D 4: A Equity, B '
                  'Certainty, C Convenience and D Economy; 1 The tax revenue collected should be greater than the costs of '
                  'collection; 2 The tax should be collected in a way and at a time which accommodates the taxpayer; 3 Takes a '
                  'higher proportion of an individual’s income in tax as income increases; 4 An individual’s tax bill should be '
                  'clear.',
 'p03-q6-table': 'The printed formula, ∆Q over ∆P times P1 + P2 over Q1 + Q2; the sentence “Complete the following table to '
                 'indicate what each of the above symbols stands for:”; and a table of the six symbols ∆Q, ∆P, P1, P2, Q1 and '
                 'Q2, each with a space beside it. Two are filled in: ∆Q, Change in the quantity demanded of the good, and Q1, '
                 'Original quantity of the good demanded.',
 'p04-q1-diagram': 'A diagram with the vertical axis numbered 1 and the horizontal axis 5: a thick falling line 4, a steeper '
                   'falling line labelled MR, a U-shaped curve 3 touching line 4 at a dot, and a curve 2 rising steeply through '
                   'a dot labelled E where it crosses MR.',
 'p05-q2a-diagram': 'A diagram with the vertical axis numbered 1 and the horizontal axis 2: a falling line labelled Demand and a '
                    'vertical line 3 crossing it.',
 'p05-q2b-diagram': 'A diagram with the vertical axis numbered 1 and the horizontal axis 2: a vertical line 3 and two parallel '
                    'falling lines, Demand 1 and Demand 2 to its right, with arrows pointing right from Demand 1 towards '
                    'Demand 2.',
 'p07-q5b-formula': 'The printed formula: 1 over MPS + MPM.',
 'p08-q7a-table': 'A table of output per worker per week: Germany, Wine 1600 litres and Cars 1200 units; France, Wine 800 '
                  'litres and Cars 400 units; Total Output, Wine 2400 litres and Cars 1600 units.',
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
    key = f'economics-2012-OL-{kind}-{slug}'
    fname = key + '.png'
    src = f'paper-trail-corpus/{"markingschemes" if kind == "scheme" else "exampapers"}/2012/LC034GLP000EV.pdf'
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
    entry.update({'lettersVisible': [], 'labelMeanings': [], 'questionRef': ref, 'year': 2012,
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
