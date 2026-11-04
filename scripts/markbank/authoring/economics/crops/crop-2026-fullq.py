"""Full printed-question crops for the six 2026 cards whose figure slot holds a solution.

A question-side crop REPLACES the typed stem and ask in the session screen, so it
must carry the whole printed question: stem, data and the ask itself. Where the
paper puts a sibling part between the data and this ask, the two regions are
rendered separately and stacked (same x-range, a white gap between). Catalogue
entries record every source region. Alt text = the chart description already
written for the data crop, plus the ask lifted from the paper's text layer.
Idempotent; manifest entries are APPENDED as raw text.
"""
from pathlib import Path
import hashlib, io, json, re, sys
import fitz
from PIL import Image

W = str(Path(__file__).resolve().parents[5])
OUT = f'{W}/public/exam-figures/economics/markbank'
SCALE = 4
GAP = 40
LEVEL = {'HL': ('higher', 'LC034ALP000EV', 'Higher'), 'OL': ('ordinary', 'LC034GLP000EV', 'Ordinary')}
LIG = {'Ɵ': 'ti', 'Ŧ': 'ti', 'Ʃ': 'tt', 'ﬀ': 'ff', 'ﬁ': 'fi', 'ﬂ': 'fl'}

# (level, slug, ref, data-crop key whose alt describes the chart, image regions, ask-text regions)
F = [
 ('HL', 'p20-q12ci-question', '2026 HL Q12(c)(i)', 'p20-q12c-oil-producers',
  [(20, [52, 54, 545, 335])], [(20, [52, 54, 545, 72]), (20, [52, 299, 545, 335])]),
 ('HL', 'p23-q13bii-question', '2026 HL Q13(b)(ii)', 'p23-q13b-surf-school-costs',
  [(23, [52, 54, 545, 240]), (23, [52, 442, 545, 775])], [(23, [52, 54, 545, 101]), (23, [52, 444, 545, 503])]),
 ('HL', 'p34-q16ai-question', '2026 HL Q16(a)(i)', 'p34-q16a-hotel-rooms',
  [(34, [52, 54, 545, 374])], [(34, [52, 54, 545, 116]), (34, [52, 326, 545, 372])]),
 ('HL', 'p35-q16bi-question', '2026 HL Q16(b)(i)', 'p35-q16b-visitors',
  [(35, [52, 54, 545, 343])], [(35, [52, 54, 545, 86]), (35, [52, 307, 545, 341])]),
 ('HL', 'p36-q16cii-question', '2026 HL Q16(c)(ii)', 'p36-q16c-ppf',
  [(36, [52, 307, 545, 600]), (37, [52, 54, 545, 110])], [(36, [52, 310, 545, 360]), (37, [52, 56, 545, 108])]),
 ('OL', 'p12-q11bii-question', '2026 OL Q11(b)(ii)', 'p12-q11b-monopoly-diagram',
  [(12, [52, 54, 560, 316]), (12, [52, 492, 560, 581])], [(12, [52, 54, 560, 86]), (12, [52, 494, 560, 579])]),
]


def tidy(s):
    for a, b in LIG.items():
        s = s.replace(a, b)
    s = s.replace('', '').replace('', '')
    return re.sub(r'\s+', ' ', s).strip()


cat_path = f'{W}/scripts/markbank/authored/economics-completion-figures.json'
cat = json.load(open(cat_path))
_order = {c['file']: i for i, c in enumerate(cat)}
man_path = f'{W}/components/MarkBank/figures.json'
man_text = open(man_path).read()
man = json.loads(man_text)
add_entries = []
for lv, slug, ref, data_slug, regions, text_regions in F:
    level, fileid, word = LEVEL[lv]
    key = f'economics-2026-{lv}-paper-{slug}'
    fname = key + '.png'
    src = f'paper-trail-corpus/exampapers/2026/{fileid}.pdf'
    with fitz.open(f'{W}/{src}') as doc:
        tiles = []
        for page, rect in regions:
            pix = doc[page - 1].get_pixmap(matrix=fitz.Matrix(SCALE, SCALE), clip=fitz.Rect(*rect))
            tiles.append(Image.open(io.BytesIO(pix.tobytes('png'))).convert('RGB'))
        ask = ' '.join(tidy(doc[page - 1].get_text('text', clip=fitz.Rect(*rect))) for page, rect in text_regions)
    width = max(t.width for t in tiles)
    height = sum(t.height for t in tiles) + GAP * (len(tiles) - 1)
    sheet = Image.new('RGB', (width, height), 'white')
    y = 0
    for t in tiles:
        sheet.paste(t, (0, y))
        y += t.height + GAP
    sheet.save(f'{OUT}/{fname}', optimize=True)
    md5 = hashlib.md5(open(f'{OUT}/{fname}', 'rb').read()).hexdigest()
    data_alt = man[f'economics-2026-{lv}-paper-{data_slug}']['alt']
    joined = ' Printed in two parts from the paper, the setup above and the ask below.' if len(tiles) > 1 else ''
    alt = f'The printed question as the paper sets it.{joined} {data_alt} The ask reads: {ask}'
    cat = [c for c in cat if c['file'] != fname]
    cat.append({'file': fname, 'kind': 'figure', 'truncated': False, 'drawingComplete': True,
                'solution': False, 'questionRef': ref, 'description': alt,
                'source': {'file': src, 'page': regions[0][0], 'rectPoints': regions[0][1], 'scale': SCALE,
                           'regions': [{'page': p, 'rectPoints': r} for p, r in regions], 'gapPx': GAP},
                'lettersVisible': [], 'labelMeanings': []})
    entry = {'src': f'/exam-figures/economics/markbank/{fname}', 'md5': md5, 'alt': alt,
             'lettersVisible': [], 'labelMeanings': [], 'questionRef': ref, 'year': 2026, 'level': level,
             'attribution': f'SEC Leaving Certificate Economics 2026 {word} Level — © State Examinations Commission'}
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
for k, e in add_entries:
    print(k, '|', e['alt'][-260:])
