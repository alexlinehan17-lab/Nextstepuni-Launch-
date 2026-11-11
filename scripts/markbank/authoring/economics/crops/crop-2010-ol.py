"""Render, catalogue and register the 2010 OL figures (idempotent).

Solution crops come from the scheme and wait for the reveal. Data crops show
the paper's own table or diagram: as the figure beneath the typed ask, or, on a
card whose figure slot holds the solution, as its question figure with the
typed ask kept (econ_legacy_lib.beside_ask). No crop here is a whole printed
question: set at phone width a whole old-syllabus question's text falls near
8 px, so each crop is the part the ask needs (coordinator rule, 2026-11-04).
Each crop was rendered and looked at before its description was written; the
diagram crops start just below the sentence printed above them, so none of its
descenders shows. Manifest entries are APPENDED as raw text.

"""
from pathlib import Path
import hashlib, json, re, sys
import fitz
from PIL import Image, ImageDraw
W = str(Path(__file__).resolve().parents[5])
OUT = f'{W}/public/exam-figures/economics/markbank'
SCALE = 4
ATTR = 'SEC Leaving Certificate Economics 2010 Ordinary Level — © State Examinations Commission'
LIG = {'Ɵ': 'ti', 'Ŧ': 'ti', 'Ʃ': 'tt', 'ﬀ': 'ff', 'ﬁ': 'fi', 'ﬂ': 'fl'}
F = [
 ('scheme', 9, [16, 140, 548, 426], 'p09-q1a-diagram', '2010 OL Section B Q1(a)(ii)', True,
  'The marking scheme’s diagram titled Monopoly, the vertical axis Price and the horizontal axis Quantity: a straight falling '
  'line AR, a steeper falling line labelled Marginal Revenue, a U-shaped curve labelled Average Cost, and a curve labelled '
  'Marginal Cost rising steeply through the point E where it crosses Marginal Revenue. A line rises from Q1 on the horizontal '
  'axis through E to a dot on the AR line, from which an arrow runs left to P1 on the vertical axis; a second arrow runs left '
  'to C1 from a lower dot, where the same line meets the Average Cost curve.'),
 ('scheme', 10, [35, 170, 571, 532], 'p10-q1b-table', '2010 OL Section B Q1(b)', True,
  'The marking scheme’s table of the three barriers, each explanation beside its examples. Patents and Copyrights: A patent/ '
  'copyright confers the sole right on a business to a particular manufacturing process for a particular commodity; examples '
  'iPad and Apple iPhone. Legal monopolies / state monopolies: The government may grant to a company the sole right to supply '
  'a good or service so that there is a legal restriction on competition; examples Provision of bus services in Dublin City by '
  'Dublin Bus, An Post letter post and Iarnród Eireann. Economies of scale: Arise where the largest supplier in an industry has '
  'a significant cost advantage over competitors because of its large size. It is unlikely that a potential competitor would '
  'be willing to make the capital investment needed to enter the monopolist\'s market; examples Gas pipeline, Eircom: '
  'telephone lines, ESB: Grid lines and Iarnrod Eireann: Train tracks.'),
 ('scheme', 12, [64, 586, 542, 641], 'p12-q2aiii-table', '2010 OL Section B Q2(a)(iii)', True,
  'The marking scheme’s completed table. Number of units consumed 1 to 6; Total utility in units 10, 35, 75, 95, 110 and '
  '115; Marginal utility in units 10, 25 and 40, then the three answers in large bold type: 20, 15 and 5.'),
 ('scheme', 16, [170, 68, 512, 203], 'p16-q3b-diagram', '2010 OL Section B Q3(b)(ii)–(iii)', True,
  'The marking scheme’s diagram, the vertical axis P and the horizontal axis Q: a rising line labelled 1 - SUPPLY, a falling '
  'line labelled 2 - DEMAND crossing it, and a thick rising line labelled NEW SUPPLY CURVE to the right of line 1. Arrows run '
  'left to P1 from where the demand line crosses line 1, and to P2, lower, from where it crosses the new supply curve; arrows '
  'drop from the same two points to Q1 and to Q2, further right, on the horizontal axis.'),
 ('scheme', 19, [82, 160, 552, 256], 'p19-q4bi-working', '2010 OL Section B Q4(b)(i)', True,
  'The marking scheme’s working, in two columns. WORKINGS: Y = €1,500m + X – M., then €1,500m + €70m - €100m with each of '
  'its five parts underlined (€1,500m, the plus, €70m, the minus and €100m), and beneath them “Each correct underlined '
  'component 2 mark = 10 marks.” ANSWER: €1,470m, 2 marks.'),
 ('paper', 3, [58, 243, 568, 401.5], 'p03-q7-table', '2010 OL Section A Q7', False, 'DATA'),
 ('paper', 4, [22, 178, 470, 464], 'p04-q1-diagram', '2010 OL Section B Q1(a)', False, 'DATA'),
 ('paper', 5, [88, 156, 562, 206], 'p05-q2a-table', '2010 OL Section B Q2(a)(iii)', False, 'DATA'),
 ('paper', 5, [170, 282, 440, 421], 'p05-q2b-diagram', '2010 OL Section B Q2(b)', False, 'DATA'),
 ('paper', 6, [180, 112, 385, 234], 'p06-q3b-diagram', '2010 OL Section B Q3(b)', False, 'DATA'),
 ('paper', 7, [100, 72, 484, 358], 'p07-q4a-diagram', '2010 OL Section B Q4(a)', False, 'DATA'),
]
MASK = {}
QALT = {}
DATA_ALT = {
 'p03-q7-table': 'A row of four items: Mobile Credit, e-mail, Landline Telephone and Mobile Ringtones & Apps. Then “Answer:” and '
                 'a grid of two rows, Substitutes for mobile phone and Complements for mobile phone, each with two empty spaces '
                 'numbered (1) and (2).',
 'p04-q1-diagram': 'A diagram titled Monopoly, the vertical axis Price and the horizontal axis Quantity: a straight falling line '
                   'labelled AR, a steeper falling line 3, a U-shaped curve 2 and a curve 1 rising steeply. A line rises from Q1 on '
                   'the horizontal axis to a dot on the AR line, passing a second dot where it meets curve 2.',
 'p05-q2a-table': 'A table: Number of units consumed 1 to 6; Total utility in units 10, 35, 75, 95, 110 and 115; Marginal utility '
                  'in units 10, 25 and 40, then a question mark for each of units 4, 5 and 6.',
 'p05-q2b-diagram': 'A diagram, the vertical axis Price and the horizontal axis No. of seats, with a thick vertical line S1 rising '
                    'from the horizontal axis.',
 'p06-q3b-diagram': 'A diagram, the vertical axis P and the horizontal axis Q, with a rising line 1 and a falling line 2 crossing it.',
 'p07-q4a-diagram': 'The Circular Flow of Income in an open economy without Government: ovals for Households, Firms and two '
                    'Foreign Markets. Line 1 runs along the top from Firms to Households. Between the two, an arrow labelled Supply '
                    'factors of production runs from Households to Firms, line 2 runs back from Firms to Households, and an arrow '
                    'labelled Spending on domestic goods/services runs from Households to Firms beneath it. Line 3 runs from '
                    'Households down to the first Foreign Markets, and line 4 from the second Foreign Markets up to Firms.',
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
    key = f'economics-2010-OL-{kind}-{slug}'
    fname = key + '.png'
    src = f'paper-trail-corpus/{"markingschemes" if kind == "scheme" else "exampapers"}/2010/LC034GLP000EV.pdf'
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
