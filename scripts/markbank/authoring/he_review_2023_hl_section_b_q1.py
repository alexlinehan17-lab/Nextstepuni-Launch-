#!/usr/bin/env python3
"""Review the 80-mark 2023 Higher nutrition question without changing IDs."""
import hashlib
import json
import re
import sys

import fitz
from he_review_2023_hl import ROOT, PAPER, SCHEME, HASHES, tidy, between, criterion

FIGURE = 'home-economics-2023-hl-sb-q1a-chart'
FIGURE_SHA256 = 'f1f84567a87258e8adb5b4ea3b675d618764575838586c7f4a4a0e7cde9177d4'


def build():
    for path, sha in HASHES.items():
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == sha
    paper = fitz.open(ROOT / PAPER)
    scheme = fitz.open(ROOT / SCHEME)
    p2 = tidy(paper[1].get_text())
    s10 = tidy(scheme[9].get_text())
    s11 = tidy(scheme[10].get_text())
    a = between(s10, '4 points @ 5 marks (graded 5:4:3:2:1:0)', '(b)')
    headings = ['Breakfast cereals 22%', 'Meat & meat products 20%', 'Bread & rolls 14%',
                'Grains, rice & pasta 10%', 'Vegetables & potatoes 9%', 'Confectionary 11%', 'Other 14%']
    guidance = []
    for i, heading in enumerate(headings):
        assert a.count(heading) == 1, heading
        paragraph = a.split(heading, 1)[1].split(headings[i + 1], 1)[0] if i + 1 < len(headings) else a.split(heading, 1)[1]
        assert paragraph.strip().endswith('etc.'), heading
        guidance.append(heading + ' ' + paragraph.strip())
    question = between(p2, '(a)', '(20 marks)')
    assert question.count('four sources') == 1
    stem = tidy(paper[1].get_text(clip=fitz.Rect(50, 150, 545, 214))).split('Question 1', 1)[1].strip()
    assert stem.startswith('‘Adequate micronutrient intake ') and 'Report 2021' in stem
    corrections = {
        'he-2023-hl-sb-q1a': dict(
            questionText=question, stem=stem,
            questionFigureKey=FIGURE, questionFigureIncludesPrompt=False,
            tariffModel=dict(kind='fixed', notation='4 points × 5 marks (5:4:3:2:1:0)'),
            rows=[criterion('sources', 'different sources of iron', 4, [0, 1, 2, 3, 4, 5],
                            'Comment and elaborate on four different chart sources. Mark each source separately using the published 5:4:3:2:1:0 steps.\n\n' + '\n\n'.join(guidance))]),
        'he-2023-hl-sb-q1b': dict(
            tariffModel=dict(kind='fixed', notation='4 factors × 5 marks (5:4:3:0)'),
            rows=[criterion('factors', 'factors that affect the absorption of iron', 4, [0, 3, 4, 5],
                            'Identify and describe four factors. Each is graded 5:4:3:0; there are no 1- or 2-mark bands. Published guidance: ' + s10.split('4 factors @ 5 marks (graded 5:4:3:0)', 1)[1].strip())]),
        'he-2023-hl-sb-q1d': dict(
            tariffModel=dict(kind='fixed', notation='5 points × 4 marks (4:2:0)'),
            rows=[criterion('guidelines', 'guidelines', 5, [0, 2, 4],
                            'Discuss five guidelines, referring to both the restricted budget and nutritional needs. Each is graded 4:2:0. Published guidance: ' +
                            s11.split('refer to restricted budget and nutritional needs', 1)[1].strip())]),
    }
    # No truncation to an arbitrary option cap: the complete final scheme point
    # and the seven chart sources must remain visible.
    assert corrections['he-2023-hl-sb-q1d']['rows'][0]['contextNote'].endswith('budget constraints; etc.')
    assert corrections['he-2023-hl-sb-q1b']['rows'][0]['contextNote'].endswith('excess alcohol; etc.')
    # Q1(c)'s 4×3 + 2×2 + 2×2 are already correctly binary (3:0 / 2:0).
    # Independently check that every printed semicolon-delimited option remains.
    authored = json.loads((ROOT / 'scripts/markbank/authored/home-economics.json').read_text())
    c = next(c for c in authored if c['id'] == 'he-2023-hl-sb-q1c')
    for row, start, end in zip(c['rows'],
                               ['production of collagen;', 'collagen production affected;', 'crystalline;'],
                               ['• effects of deficiency', '• properties', '(d)']):
        published = start + between(s11, start, end)
        expected = [p.strip() for p in published.split(';') if p.strip() and p.strip() != 'etc.']
        assert row['group']['options'] == expected, row['id']
    return {key: dict(reason='Independent 2023 Higher B1 paper/scheme review: inline original chart, full source wording, untruncated guidance and published partial marks. See he_review_2023_hl_section_b_q1.py.', set=value)
            for key, value in corrections.items()}


def write():
    corrections = build()
    path = ROOT / 'scripts/markbank/card-corrections.json'
    saved = json.loads(path.read_text())
    saved['home-economics'].update(corrections)
    path.write_text(json.dumps(saved, ensure_ascii=False, indent=1) + '\n')
    bindings_path = ROOT / 'scripts/markbank/card-source-bindings.json'
    bindings = json.loads(bindings_path.read_text())
    bindings['home-economics']['he-2023-hl-sb-q1a']['stripStem'] = False
    bindings_path.write_text(json.dumps(bindings, ensure_ascii=False, indent=2) + '\n')
    crop = ROOT / f'public/exam-figures/home-economics/{FIGURE}.png'
    if not crop.exists():
        crop.parent.mkdir(parents=True, exist_ok=True)
        fitz.open(ROOT / PAPER)[1].get_pixmap(matrix=fitz.Matrix(2, 2), clip=fitz.Rect(74, 214, 520, 437)).save(crop)
    assert hashlib.sha256(crop.read_bytes()).hexdigest() == FIGURE_SHA256, 'Inspected chart changed'
    path = ROOT / 'components/MarkBank/figures-home-economics.json'
    manifest = json.loads(path.read_text())
    manifest[FIGURE] = dict(src=f'/exam-figures/home-economics/{FIGURE}.png',
                            md5=hashlib.md5(crop.read_bytes()).hexdigest(),
                            alt='Sources of iron in Irish teenagers aged 13–18 years. Breakfast cereals 22%; meat and meat products 20%; breads and rolls 14%; grains, rice and pasta 10%; vegetables and potatoes 9%; confectionery, biscuits and preserves 11%; other 14%.',
                            attribution='SEC Home Economics 2023 Higher Level examination paper, Sections B and C page 2 — © State Examinations Commission.',
                            sourceNote='Complete original question chart, visually checked with title, all seven labels and percentages, and all borders. No marking-scheme material. Bounds [74,214,520,437], 2×.')
    path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    print('B1: three cards corrected, Vitamin C card verified unchanged; all 80 published marks retained.')


if __name__ == '__main__':
    if '--write' in sys.argv:
        write()
    else:
        print(json.dumps(build(), ensure_ascii=False, indent=2))
