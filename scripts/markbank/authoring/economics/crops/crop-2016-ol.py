"""Render, catalogue and register the 2016 OL figures (idempotent).

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
ATTR = 'SEC Leaving Certificate Economics 2016 Ordinary Level — © State Examinations Commission'
LIG = {'Ɵ': 'ti', 'Ŧ': 'ti', 'Ʃ': 'tt', 'ﬀ': 'ff', 'ﬁ': 'fi', 'ﬂ': 'fl'}
F = [
 ('scheme', 10, [100, 120, 535, 330], 'p10-q1a-diagram', '2016 OL Section B Q1(a)(ii)', True,
  'The marking scheme’s completed diagram: P against Q, a horizontal line D = AR = MR, a U-shaped AC curve touching it '
  'at G and an MC curve rising through G. The line is marked P1 on the price axis, and an arrow runs down from G to Q1.'),
 ('scheme', 13, [150, 288, 460, 462], 'p13-q2a-diagram', '2016 OL Section B Q2(a)', True,
  'The marking scheme’s completed diagram: Price on the vertical axis and Quantity on the horizontal, a falling Demand '
  'curve and a rising supply curve crossing where an arrow runs left to P1 and an arrow runs down to Q1.'),
 ('paper', 2, [55, 248, 560, 484], 'p02-q2-table', '2016 OL Section A Q2', False, 'DATA'),
 ('paper', 2, [55, 552, 560, 613], 'p02-q3-table', '2016 OL Section A Q3', False, 'DATA'),
 ('paper', 3, [55, 378, 520, 470], 'p03-q5-lists', '2016 OL Section A Q5', False, 'DATA'),
 ('paper', 4, [55, 532, 560, 724], 'p04-q9-table', '2016 OL Section A Q9', False, 'DATA'),
 ('paper', 5, [100, 215, 540, 402], 'p05-q1-diagram', '2016 OL Section B Q1(a)', False, 'DATA'),
 ('paper', 6, [175, 65, 395, 220], 'p06-q2a-diagram', '2016 OL Section B Q2(a)', False, 'DATA'),
]
QALT = {}
DATA_ALT = {
 'p02-q2-table': 'A table to tick: four statements, each with a box under Embargo, Quota, Tariff and Subsidy. The statements: '
                 'A tax on goods imported into the country; A complete ban on the importation of certain goods; A physical '
                 'limit placed by the government on the amount of goods that can be imported; Any payment or assistance given '
                 'by the government to Irish producers of goods or services.',
 'p02-q3-table': 'A table: Number of units consumed 1 to 6; Total utility in units 15, 40, 70, 85, 95, 100; Marginal utility in '
                 'units 15, 25, blank, 15, blank, blank.',
 'p03-q5-lists': 'Two lists. Economic Idea: A The Multiplier; B Law of Comparative Advantage; C Laissez Faire; D Worker '
                 'exploitation in a capitalist system. Economist: 1 Karl Marx; 2 Adam Smith; 3 John Maynard Keynes; 4 David Ricardo.',
 'p04-q9-table': 'The printed formula, ∆Q over ∆Y times Y1 + Y2 over Q1 + Q2, and a table of its six symbols: ∆Q, ∆Y, Y2 and Q1 '
                 'blank; Y1 Consumer’s original income; Q2 New quantity demanded of the good.',
 'p05-q1-diagram': 'A diagram with P on the vertical axis and Q on the horizontal: a horizontal line labelled D = AR = MR, a '
                   'U-shaped AC curve touching it at G and an MC curve rising through G. The labels P, MC, AC, AR, MR and Q '
                   'are underlined.',
 'p06-q2a-diagram': 'A diagram: a vertical axis numbered 1 and a horizontal axis numbered 2, a rising line labelled Supply and '
                    'a falling line numbered 3 crossing it.',
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
    key = f'economics-2016-OL-{kind}-{slug}'
    fname = key + '.png'
    src = f'paper-trail-corpus/{"markingschemes" if kind == "scheme" else "exampapers"}/2016/LC034GLP000EV.pdf'
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
    entry.update({'lettersVisible': [], 'labelMeanings': [], 'questionRef': ref, 'year': 2016,
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
