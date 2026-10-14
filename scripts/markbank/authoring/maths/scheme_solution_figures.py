"""Crop a Mathematics part's printed model solution from a scheme that sets the paper out with its answers.

    python3 scripts/markbank/authoring/maths/scheme_solution_figures.py <year> <hl|ol> [--write]

Why: up to 2015 the SEC's Mathematics scheme is two documents in one. "Model
Solutions" reprints the question paper with each part's worked solution boxed
under it, and "Detailed marking notes" lists each scale's credit bands as
prose. The bands lift cleanly as text; the model solutions are MathType
equations whose text layer is scattered digits ("13 | 64 | 3 | 9 | 27"), so a
card cannot quote them. This attaches the SEC's own print instead: the part as
the scheme prints it, from its marker down to the next part's marker, with the
worked solution beneath it, shown only after the reveal (CardFigure.solution).
scheme_row_figures.py does the same for the 2016+ schemes, which set every part
in one ruled table row; this is its counterpart for the earlier layout.

How a part is found -- geometry, not prose: every part marker ("Question 3",
"(a)", "(b)  (i)", "(ii)") is printed at the left margin of the model-solution
pages. The crop runs from the card's first marker to the next marker that is
not part of the card, across a page break when the solution continues.

Outputs (with --write):
  exam-papers/maths/figures/<year>-<level>/maths-<year>-<LEVEL>-scheme-p<page>-i<n>.png
  scripts/markbank/authored/maths-scheme-row-figures-catalogue.json   (entries for this sitting)
and they publish with scheme_row_figures.py --publish, which reads that catalogue.
"""
import io
import json
import os
import re
import sys

import pymupdf
from PIL import Image

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..'))
LEVEL = {'hl': 'higher', 'ol': 'ordinary'}
LEVEL_WORD = {'hl': 'Higher Level', 'ol': 'Ordinary Level'}
SCHEME = {'hl': 'LC003ALP000EV.pdf', 'ol': 'LC003GLP000EV.pdf'}
CATALOGUE = os.path.join(ROOT, 'scripts', 'markbank', 'authored', 'maths-scheme-row-figures-catalogue.json')
DPI = 200
X0, X1 = 40.0, 560.0

# Each paper's model-solution pages and detailed-marking-notes pages (PDF
# positions, inclusive). A card's crop is its model solution with its marking
# notes printed under it, so the reveal shows every credit band even where the
# notes set a band in mangled maths that cannot be quoted.
SECTIONS = {
    (2015, 'hl'): {'p1': {'solutions': (7, 22), 'notes': (25, 34)}},
}
# The cards whose model solution the text layer cannot carry, per sitting.
AFFECTED = {}

MARK = re.compile(r'\((?:[a-h]|i{1,3}|iv|vi{0,3}|ix|x)\)')
QHEAD = re.compile(r'^Question\s+(\d{1,2})\b')
ROMAN = re.compile(r'^(?:i{1,3}|iv|vi{0,3}|ix|x)$')
FOOTER = re.compile(r'^\[\d+\]$')


def markers(doc, first, last):
    """[(q, letter, roman, page, y)] for every part marker at the left margin, in order."""
    out, q, letter = [], None, None
    for pno in range(first, last + 1):
        page = doc[pno - 1]
        lines = []
        for b in page.get_text('dict')['blocks']:
            for ln in b.get('lines', []):
                t = ''.join(s['text'] for s in ln['spans']).strip()
                if t:
                    lines.append((round(ln['bbox'][1], 1), ln['bbox'][0], t))
        for y, x, t in sorted(lines):
            if x > 140:
                continue
            m = QHEAD.match(t)
            if m:
                q, letter = int(m.group(1)), None
                out.append((q, None, None, pno, y))
                continue
            toks = []
            rest = t
            while True:
                mm = MARK.match(rest)
                if not mm:
                    break
                toks.append(mm.group(0)[1:-1])
                rest = rest[mm.end():].lstrip()
            if not toks or q is None:
                continue
            roman = None
            for tok in toks:
                # (i) after (h) would be a letter; Mathematics never runs that far.
                if ROMAN.match(tok) and (letter is not None or len(toks) > 1 and tok != toks[0]):
                    roman = tok
                else:
                    letter, roman = tok, None
            out.append((q, letter, roman, pno, y))
    return out


def parse_part(printed):
    m = re.match(r'^Q(\d+)(?:\(([a-h])\))?(?:\(([ivx]+)\))?$', printed)
    return int(m.group(1)), m.group(2), m.group(3)


def span(entries, printed):
    """(start entry index, end entry index or None) for a card's printed parts.

    The notes print a combined scale once ("(a)(i) and (ii) combined"), so a
    card's later parts need not have markers of their own; a question with no
    lettered parts runs to the next question.
    """
    q, letter, roman = parse_part(printed[0])
    start = next(i for i, e in enumerate(entries)
                 if e[0] == q and (e[1] == letter or letter is None) and (roman is None or e[2] == roman))
    if letter is None:
        end = next((j for j in range(start + 1, len(entries)) if entries[j][0] != q), None)
        return start, end
    last = start
    for part in printed:
        pq, pl, pr = parse_part(part)
        for i in range(start, len(entries)):
            e = entries[i]
            if e[0] == pq and e[1] == pl and (pr is None or e[2] == pr):
                last = max(last, i)
    lq, ll, lr = entries[last][0], entries[last][1], entries[last][2]
    lr = parse_part(printed[-1])[2] if parse_part(printed[-1])[2] else (lr if entries[last][2] else None)
    for j in range(last + 1, len(entries)):
        e = entries[j]
        if e[0] != lq or e[1] != ll or (lr is not None and e[2] != lr):
            return start, j
    return start, None


def content_bottom(page):
    ys = [b[1] for b in page.get_text('blocks') if FOOTER.match(b[4].strip())]
    return (min(ys) - 4) if ys else page.rect.height - 50


def crop(doc, a, b, last_page):
    """Image of the pages from entry a to entry b (or the section's end)."""
    (_, _, _, p0, y0) = a
    p1, y1 = (b[3], b[4]) if b else (last_page, None)
    pieces = []
    for pno in range(p0, p1 + 1):
        page = doc[pno - 1]
        top = (y0 - 5) if pno == p0 else 45.0
        bottom = (y1 - 5) if (pno == p1 and y1 is not None) else content_bottom(page)
        if bottom - top < 8:
            continue
        pix = page.get_pixmap(clip=pymupdf.Rect(X0, top, X1, bottom), dpi=DPI)
        im = Image.open(io.BytesIO(pix.tobytes('png'))).convert('L')
        rows = [y for y in range(im.height) if min(im.crop((0, y, im.width, y + 1)).getdata()) < 200]
        if rows:
            pieces.append(im.crop((0, max(0, rows[0] - 6), im.width, min(im.height, rows[-1] + 7))))
    out = Image.new('L', (max(p.width for p in pieces), sum(p.height for p in pieces) + 12 * (len(pieces) - 1)), 255)
    y = 0
    for p in pieces:
        out.paste(p, (0, y)); y += p.height + 12
    return out


def main():
    year, lv = int(sys.argv[1]), sys.argv[2]
    write = '--write' in sys.argv
    doc = pymupdf.open(os.path.join(ROOT, 'paper-trail-corpus', 'markingschemes', str(year), SCHEME[lv]))
    tasks = {}
    for key in ('p1', 'p2'):
        path = os.path.join(ROOT, 'scripts', 'markbank', 'mathematics', 'reviews', f'{year}-{LEVEL[lv]}-{key}.json')
        if os.path.exists(path):
            tasks.update({c['id']: c for c in json.load(open(path))['cards']})
    out_dir = os.path.join(ROOT, 'exam-papers', 'maths', 'figures', f'{year}-{lv}')
    if write:
        os.makedirs(out_dir, exist_ok=True)
    index = {k: {part: markers(doc, *rng) for part, rng in v.items()} for k, v in SECTIONS[(year, lv)].items()}
    per_page, entries = {}, []
    for cid in AFFECTED[(year, lv)]:
        task = tasks[cid]
        key = cid.split('-')[3]
        images, where = [], []
        for part in ('solutions', 'notes'):
            ents = index[key][part]
            a, b = span(ents, task['printedParts'])
            start, end = ents[a], (ents[b] if b is not None else None)
            images.append(crop(doc, start, end, SECTIONS[(year, lv)][key][part][1]))
            where.append((start, end))
        pno = where[0][0][3]
        n = per_page.get(pno, 0); per_page[pno] = n + 1
        name = f'maths-{year}-{lv.upper()}-scheme-p{pno:03d}-i{n}'
        paper_no = key[1]
        refs = ', '.join(task['printedParts'])
        desc = (f"The marking scheme's printed model solution and detailed marking notes for {year} {LEVEL_WORD[lv]} Paper {paper_no} {refs}, "
                f"as the State Examinations Commission set them: the part as printed with its worked solution beneath it, then the "
                f"scale and every credit band the notes give for it.")
        entries.append({'file': name + '.png', 'kind': 'figure', 'truncated': False, 'description': desc, 'solution': True,
                        'questionRef': f"{year} {lv.upper()} Paper {paper_no} {refs}"})
        fmt = lambda se: f"p{se[0][3]} y{se[0][4]:.0f} -> " + (f"p{se[1][3]} y{se[1][4]:.0f}" if se[1] else 'section end')
        print(f'{cid:32} solution {fmt(where[0])} | notes {fmt(where[1])}  {name}')
        if write:
            # The worked solution above, its marking notes below, ruled apart.
            w = max(im.width for im in images)
            out = Image.new('L', (w, sum(im.height for im in images) + 41), 255)
            out.paste(images[0], (0, 0))
            for x in range(10, w - 10):
                out.putpixel((x, images[0].height + 20), 120)
            out.paste(images[1], (0, images[0].height + 41))
            out.save(os.path.join(out_dir, name + '.png'))
    if write:
        cat = json.load(open(CATALOGUE)) if os.path.exists(CATALOGUE) else []
        keep = [e for e in cat if not e['file'].startswith(f'maths-{year}-{lv.upper()}-scheme-')]
        open(CATALOGUE, 'w').write(json.dumps(keep + entries, ensure_ascii=False, indent=1) + '\n')
        print(f'wrote {len(entries)} crops and catalogue entries')


if __name__ == '__main__':
    main()
