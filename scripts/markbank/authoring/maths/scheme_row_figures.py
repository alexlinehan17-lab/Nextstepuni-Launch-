"""Crop a Mathematics part's whole printed scheme row -- model solution AND marking notes.

    python3 scripts/markbank/authoring/maths/scheme_row_figures.py <year> <hl|ol> [--write | --publish]

Why: the 2019 Ordinary Level scheme's text layer cannot carry everything it
prints. Its subscripts and superscripts extract as unrelated ASCII (z2 reads as
"z8", f' as "fL", 2^(2x-1) as "28TE;"), which no glyph map can repair because
the characters are ordinary ASCII, and a stacked fraction's denominator sits on
a line of its own that the provenance reader filters as a mark cell. Marking
points that depend on either cannot be lifted as text, so they were left out of
the card's rows. This attaches the SEC's own print of the part instead: the
table row holding the part's model solution and its marking notes (every credit
band the scheme prints), cropped from the scheme PDF and shown only after the
reveal (CardFigure.solution).

How a row is found -- geometry, not prose: the scheme is a three-column table
(part label | model solution | marking notes) ruled by horizontal lines. The
part's label sits in the label column ("(a)(iii)", "(a)(i)+(ii)", "(b)"), on
the scheme page the review names; the row runs from the rule above the label
to the next rule below it. Nothing is typed: the crop is the printed row.

Outputs (with --write):
  exam-papers/maths/figures/<year>-<level>/maths-<year>-<LEVEL>-scheme-p<page>-i<n>.png
  scripts/markbank/authored/maths-scheme-row-figures-catalogue.json   (entries for this sitting)
The catalogue's descriptions are machine-drafted from the row's own text and
then checked by opening each crop.

With --publish the inspected crops are copied to public/exam-figures/maths/markbank/
and entered in components/MarkBank/figures.json in the shape bind-figures.mjs
writes. The entries are inserted textually: figures.json mixes escaped and raw
Unicode from earlier writers, so rewriting the whole object would restyle
thousands of unrelated lines in a file every subject shares.
"""
import hashlib
import shutil
import json
import os
import re
import sys

import pymupdf

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..'))
LEVEL = {'hl': 'higher', 'ol': 'ordinary'}
LEVEL_WORD = {'hl': 'Higher Level', 'ol': 'Ordinary Level'}
SCHEME = {'hl': 'LC003ALP000EV.pdf', 'ol': 'LC003GLP000EV.pdf'}
CATALOGUE = os.path.join(ROOT, 'scripts', 'markbank', 'authored', 'maths-scheme-row-figures-catalogue.json')
DPI = 200

# The cards whose printed scheme content could not be lifted as text, per sitting.
AFFECTED = {
    (2019, 'ol'): [
        'maths-2019-ol-p1-q2-a-i', 'maths-2019-ol-p1-q2-a-iii', 'maths-2019-ol-p1-q2-b', 'maths-2019-ol-p1-q3-b',
        'maths-2019-ol-p1-q4-b', 'maths-2019-ol-p1-q5-a', 'maths-2019-ol-p1-q6-b', 'maths-2019-ol-p1-q7-c-i',
        'maths-2019-ol-p1-q7-d-i', 'maths-2019-ol-p1-q7-d-ii', 'maths-2019-ol-p1-q7-d-iii', 'maths-2019-ol-p1-q8-a-i',
        'maths-2019-ol-p1-q8-b-ii', 'maths-2019-ol-p1-q8-b-iii', 'maths-2019-ol-p1-q8-b-iv', 'maths-2019-ol-p1-q8-b-v',
        'maths-2019-ol-p1-q8-b-vi', 'maths-2019-ol-p1-q9-a', 'maths-2019-ol-p1-q9-b', 'maths-2019-ol-p1-q9-c-iii',
        'maths-2019-ol-p1-q9-d',
        'maths-2019-ol-p2-q1-a', 'maths-2019-ol-p2-q1-b', 'maths-2019-ol-p2-q1-c-i', 'maths-2019-ol-p2-q1-c-ii',
        'maths-2019-ol-p2-q2-a', 'maths-2019-ol-p2-q2-b', 'maths-2019-ol-p2-q2-d', 'maths-2019-ol-p2-q3-d',
        'maths-2019-ol-p2-q4-b', 'maths-2019-ol-p2-q4-c', 'maths-2019-ol-p2-q4-d', 'maths-2019-ol-p2-q5-a',
        'maths-2019-ol-p2-q5-b', 'maths-2019-ol-p2-q7-c-i', 'maths-2019-ol-p2-q8-a-i', 'maths-2019-ol-p2-q8-a-ii',
        'maths-2019-ol-p2-q8-a-iii', 'maths-2019-ol-p2-q8-b-i', 'maths-2019-ol-p2-q8-b-ii', 'maths-2019-ol-p2-q8-b-iii',
        'maths-2019-ol-p2-q9-a', 'maths-2019-ol-p2-q9-b', 'maths-2019-ol-p2-q9-c', 'maths-2019-ol-p2-q9-d-i',
        'maths-2019-ol-p2-q9-d-ii', 'maths-2019-ol-p2-q9-d-iii',
    ],
    # 2018 Higher: model-solution lines whose stacked-fraction numerator extracts
    # as a lone "1" (filtered as a mark cell), integral limits the text layer
    # drops (Q3(b)), and model solutions printed as images (the Q9(a) table, the
    # Q6(b)(ii), Q7(c) and Q7(d) graphs).
    (2018, 'hl'): [
        'maths-2018-hl-p1-q3-b', 'maths-2018-hl-p1-q6-b-ii', 'maths-2018-hl-p1-q7-c', 'maths-2018-hl-p1-q7-d', 'maths-2018-hl-p1-q7-e-ii',
        'maths-2018-hl-p1-q8-a', 'maths-2018-hl-p1-q8-b', 'maths-2018-hl-p1-q8-c', 'maths-2018-hl-p1-q8-d',
        'maths-2018-hl-p1-q9-a', 'maths-2018-hl-p1-q9-c-i',
        # Paper 2: working that refers to a diagram or graph in the scheme, the
        # Q8(b)(i) tick table, and the Q8(c) present-value sum.
        'maths-2018-hl-p2-q4-b', 'maths-2018-hl-p2-q6-a', 'maths-2018-hl-p2-q7-d', 'maths-2018-hl-p2-q8-b-i',
        'maths-2018-hl-p2-q8-c', 'maths-2018-hl-p2-q9-b-iii',
    ],
}
BANDS = ['Low Partial Credit', 'Mid Partial Credit', 'High Partial Credit', 'Partial Credit', 'Full Credit',
         'Zero Credit', 'No Credit', 'Note', 'Special Case', 'Misreading']


def norm_label(t):
    return re.sub(r'\s+', '', t).replace('&', '+')


def part_label(printed):
    """'Q2(a)(iii)' -> '(a)(iii)'; several printed parts join with '+'."""
    first = re.sub(r'^Q\d+', '', printed[0])
    rest = [re.sub(r'^Q\d+(\([a-z]\))?', '', p) for p in printed[1:]]
    return first + ''.join('+' + r for r in rest)


def hsegments(page):
    segs = []
    for d in page.get_drawings():
        for it in d['items']:
            if it[0] == 'l':
                p1, p2 = it[1], it[2]
                if abs(p1.y - p2.y) < 0.6 and abs(p1.x - p2.x) > 60:
                    segs.append((round(p1.y, 1), min(p1.x, p2.x), max(p1.x, p2.x)))
            elif it[0] == 're':
                r = it[1]
                if r.height < 1.6 and r.width > 60:
                    segs.append((round((r.y0 + r.y1) / 2, 1), r.x0, r.x1))
    return segs


def rules(page):
    """y of each rule of the scheme's own table.

    A table inside a model solution (a stem-and-leaf plot, a probability table)
    draws rules of its own, so only a rule that starts and ends on a column
    boundary of the scheme table counts. The boundaries come from the table's
    header rule, the first rule on the page. A rule drawn as two abutting
    segments (one per cell, as under the 2018 Higher Q9(b)(iii) graph) is one rule.
    """
    segs = []
    for y, a, b in sorted(hsegments(page)):
        if segs and segs[-1][0] == y and a - segs[-1][2] <= 2:
            segs[-1] = (y, segs[-1][1], max(b, segs[-1][2]))
        else:
            segs.append((y, a, b))
    top = min(y for y, _, _ in segs)
    bounds = sorted({round(x, 0) for y, a, b in segs if y <= top + 25 for x in (a, b)})
    on = lambda x: any(abs(x - b) < 3 for b in bounds)
    return sorted({y for y, a, b in segs if on(a) and on(b) and b - a > 150})


def table_x(page):
    xs = []
    for d in page.get_drawings():
        for it in d['items']:
            if it[0] == 'l' and abs(it[1].x - it[2].x) < 0.6 and abs(it[1].y - it[2].y) > 20:
                xs.append(it[1].x)
            elif it[0] == 're' and it[1].width < 1.6 and it[1].height > 20:
                xs.append(it[1].x0)
    return min(xs), max(xs)


def vertical_xs(page):
    xs = set()
    for d in page.get_drawings():
        for it in d['items']:
            if it[0] == 'l' and abs(it[1].x - it[2].x) < 0.6 and abs(it[1].y - it[2].y) > 20:
                xs.add(round(it[1].x))
            elif it[0] == 're' and it[1].width < 1.6 and it[1].height > 20:
                xs.add(round(it[1].x0))
    return sorted(xs)


def find_row(page, label):
    """The ruled row whose label-column words read `label`, with its continuation rows.

    A part's scheme content can run over more than one ruled row: a model-solution
    table in one row and its marking notes in an unlabelled row below it (2018
    Higher Q9(a)), or the same label printed again over a second row holding the
    graph (2018 Higher Q7(c)). Rows that follow the labelled row and read either
    nothing or the same label belong to the part; the span stops at the first row
    labelled with anything else.
    """
    want = norm_label(label)
    xs = vertical_xs(page)
    label_right = xs[1] + 1
    words = [w for w in page.get_text('words') if w[2] <= label_right]
    rs = rules(page)
    rows = []
    for top, bottom in zip(rs, rs[1:]):
        if bottom - top < 15:
            continue
        got = norm_label(''.join(w[4] for w in sorted(words, key=lambda w: (round(w[1]), w[0])) if top <= w[1] < bottom))
        rows.append((top, bottom, got))
    hits = [i for i, r in enumerate(rows) if r[2] == want]
    if not hits:
        raise SystemExit(f'label {label!r}: no ruled row reads that label on page {page.number + 1}')
    i = j = hits[0]
    while j + 1 < len(rows) and rows[j + 1][2] in ('', want) and rows[j + 1][0] == rows[j][1]:
        j += 1
    if any(h > j for h in hits):
        raise SystemExit(f'label {label!r}: {len(hits)} separate ruled rows read that label on page {page.number + 1}')
    return rows[i][0], rows[j][1]


def main():
    year, lv = int(sys.argv[1]), sys.argv[2]
    write = '--write' in sys.argv
    ids = AFFECTED[(year, lv)]
    doc = pymupdf.open(os.path.join(ROOT, 'paper-trail-corpus', 'markingschemes', str(year), SCHEME[lv]))
    tasks = {}
    for key in ('p1', 'p2'):
        path = os.path.join(ROOT, 'scripts', 'markbank', 'mathematics', 'reviews', f'{year}-{LEVEL[lv]}-{key}.json')
        if os.path.exists(path):
            tasks.update({c['id']: c for c in json.load(open(path))['cards']})
    out_dir = os.path.join(ROOT, 'exam-papers', 'maths', 'figures', f'{year}-{lv}')
    if write:
        os.makedirs(out_dir, exist_ok=True)
    per_page = {}
    entries, binding = [], {}
    for cid in ids:
        task = tasks[cid]
        assert len(task['schemePages']) == 1, (cid, task['schemePages'])
        pno = task['schemePages'][0]
        page = doc[pno - 1]
        label = part_label(task['printedParts'])
        top, bottom = find_row(page, label)
        x0, x1 = table_x(page)
        clip = pymupdf.Rect(x0 - 2, top - 2, x1 + 2, bottom + 2)
        n = per_page.get(pno, 0); per_page[pno] = n + 1
        name = f'maths-{year}-{lv.upper()}-scheme-p{pno:03d}-i{n}'
        text = ' '.join(page.get_text('text', clip=clip).split())
        scale = re.search(r'Scale ?\d+[A-E] ?\([\d, ]+\)', text)
        bands = [b for b in BANDS if re.search(r'\b' + b + r'\b', text) and not (b == 'Partial Credit' and re.search(r'(Low|Mid|High) Partial Credit', text) and not re.search(r'(?<!Low )(?<!Mid )(?<!High )Partial Credit', text))]
        paper_no = cid.split('-')[3][1]
        desc = (f"The marking scheme's printed row for {year} {LEVEL_WORD[lv]} Paper {paper_no} {', '.join(task['printedParts'])}, "
                f"as the State Examinations Commission set it: the part label, the model solution, and the marking notes"
                + (f" for {scale.group(0)}" if scale else '')
                + (f", listing {', '.join(bands)}" if bands else '') + '.')
        entries.append({'file': name + '.png', 'kind': 'figure', 'truncated': False, 'description': desc, 'solution': True,
                        'questionRef': f"{year} {lv.upper()} Paper {paper_no} {', '.join(task['printedParts'])}"})
        binding[cid] = name
        print(f'{cid:32} p{pno} rows {top:.0f}-{bottom:.0f} {name}')
        if write:
            page.get_pixmap(clip=clip, dpi=DPI).save(os.path.join(out_dir, name + '.png'))
    if write:
        cat = json.load(open(CATALOGUE)) if os.path.exists(CATALOGUE) else []
        keep = [e for e in cat if not e['file'].startswith(f'maths-{year}-{lv.upper()}-scheme-')]
        open(CATALOGUE, 'w').write(json.dumps(keep + entries, ensure_ascii=False, indent=1) + '\n')
        print(f'wrote {len(entries)} crops and catalogue entries')
    return binding


def publish(year, lv):
    manifest_path = os.path.join(ROOT, 'components', 'MarkBank', 'figures.json')
    raw = open(manifest_path, encoding='utf-8').read()
    manifest = json.loads(raw)
    by_md5 = {v['md5']: k for k, v in manifest.items()}
    cat = [e for e in json.load(open(CATALOGUE)) if e['file'].startswith(f'maths-{year}-{lv.upper()}-scheme-')]
    dest = os.path.join(ROOT, 'public', 'exam-figures', 'maths', 'markbank')
    added = []
    for e in cat:
        assert e['kind'] == 'figure' and not e['truncated'] and len(e['description']) >= 40, e['file']
        src = os.path.join(ROOT, 'exam-papers', 'maths', 'figures', f'{year}-{lv}', e['file'])
        md5 = hashlib.md5(open(src, 'rb').read()).hexdigest()
        name = e['file'][:-4]
        if name in manifest:
            if manifest[name]['md5'] != md5:
                raise SystemExit(f'{name}: already published with different bytes')
            continue
        if md5 in by_md5:
            raise SystemExit(f'{name}: identical bytes to {by_md5[md5]}')
        shutil.copyfile(src, os.path.join(dest, e['file']))
        added.append((name, {
            'src': f'/exam-figures/maths/markbank/{e["file"]}', 'md5': md5, 'alt': e['description'], 'solution': True,
            'lettersVisible': [], 'labelMeanings': [], 'questionRef': e['questionRef'], 'year': year,
            'level': LEVEL[lv], 'attribution': f'SEC Leaving Certificate Mathematics {year} {LEVEL_WORD[lv].split()[0]} Level — © State Examinations Commission',
        }))
    if added:
        tail = raw.rstrip()
        assert tail.endswith('}\n}'), 'unexpected manifest ending'
        block = ''.join(',\n ' + json.dumps(k, ensure_ascii=False) + ': ' + json.dumps(v, ensure_ascii=False, indent=1).replace('\n', '\n ')
                        for k, v in added)
        out = tail[:-2] + block + '\n}\n'
        json.loads(out)
        open(manifest_path, 'w', encoding='utf-8').write(out)
    print(f'published {len(added)} crops into figures.json')


if __name__ == '__main__':
    if '--publish' in sys.argv:
        publish(int(sys.argv[1]), sys.argv[2])
    else:
        main()
