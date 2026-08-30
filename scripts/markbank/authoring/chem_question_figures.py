#!/usr/bin/env python3
"""Crop the printed matter a Chemistry question hands its parts.

    python3 scripts/markbank/authoring/chem_question_figures.py 2023 hl 8
    python3 scripts/markbank/authoring/chem_question_figures.py --write
    python3 scripts/markbank/authoring/chem_question_figures.py --catalogue

Forty-nine open Chemistry asks point at something printed -- "Identify the
elimination reaction in the scheme", "How does the geometry change during
conversion C?", "Each of A, B, C and D shown on the right is a graph of the
boiling points" -- and five of them have a figure keyed to them. Without the
picture those asks cannot be carded at all: the scheme's answer to the first
is the single letter "D", which means nothing on its own.

The raster extractor cannot supply them. A reaction scheme is drawn in VECTOR
strokes with its compound names set as ordinary text beside them, so the
images on the page are the arrow heads and the bond lines, not the diagram;
2023 HL page 9 holds thirteen of those fragments and twenty-two paths for what
a reader sees as one picture.

So this works the way a reader does. It takes every drawing and image rect on
the page, clusters them into bands with the gaps between them, then grows each
band to take in the text sitting inside it -- which is where "Ethene",
"Poly(ethene)" and "uv, Cl2" live. One band is one figure.

Nothing is invented and nothing is described from a model's guess: the alt
text is built from the question's own wording and the labels the crop actually
contains, and every crop is opened and looked at before it is bound.
"""
import argparse
import collections
import json
import os
import re
import sys

import pymupdf

DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, DIR)
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(DIR)))

import paper as PP                                          # noqa: E402
import reconcile as R                                       # noqa: E402

DPI = 150
PAD = 8.0
# A band narrower than this is a bond line or an arrow head on its own, not a
# figure. A band shorter than this is a rule or an underline.
MIN_W, MIN_H = 60.0, 34.0
# A last resort where no prose separates two runs of artwork: 2023 HL page 9
# sets its reaction scheme at y 86-170 and its boiling-point graphs at y
# 404-695 with the question's parts printed between them, so the prose test
# already splits those. This only catches artwork separated by white space
# alone.
BAND_GAP = 90.0
LABEL = re.compile(r'Q(\d+)(?:\(([a-z]+)\))?(?:\(([a-z]+)\))?$')
POINTS_AT = re.compile(
    r'\b(scheme|the table|the diagram|shown (?:above|below|on the right)|'
    r'these graphs|the graph|conversion [A-Z]\b|reaction [A-Z]\b|curve|'
    r'from the table|in the table|shown on the right)\b', re.I)
# Page furniture that sits inside a band's y range without belonging to it.
FURNITURE = re.compile(r'^(Leaving Certificate|Chemistry\s*[–-]|Page \d|\d{1,3})$')
# A part marker is the question's structure, never a label on its artwork.
PART_MARKER = re.compile(r'^\(([a-h]|i{1,3}|iv|v|vi{0,3}|ix|x)\)')
# Longest a figure label runs. "uv, Cl2" and "Poly(ethene)" are labels;
# "Consider the following straight-chain" is the question talking.
LABEL_MAX = 26
# A short LOWERCASE word is the tail of a sentence the crop clipped, not a
# label: growing to "of" pulled the left edge of 2022 OL Q1's apparatus
# diagram out into the question's prose. A real label is a capital ("A"), a
# formula ("KMnO4") or a named part ("water bath").
STRAY_WORD = re.compile(r'[a-z]{1,3}')


def artwork(page):
    """Every drawing and image rectangle on the page, as (x0, y0, x1, y1)."""
    out = []
    for d in page.get_drawings():
        r = d['rect']
        if r.width > 1 and r.height > 1:
            out.append((r.x0, r.y0, r.x1, r.y1))
    for im in page.get_images(full=True):
        for r in page.get_image_rects(im[0]):
            out.append((r.x0, r.y0, r.x1, r.y1))
    return out


def bands(page):
    """Artwork grouped into figures, each grown to hold the text inside it."""
    rects = sorted(artwork(page), key=lambda r: r[1])
    if not rects:
        return []
    prose = [ln for ln, text in text_lines(page)
             if len(text) > LABEL_MAX and not FURNITURE.match(text)]
    groups, cur = [], [rects[0]]
    for r in rects[1:]:
        foot = max(c[3] for c in cur)
        # Two runs of artwork are two FIGURES when the question's prose runs
        # between them, and one figure otherwise. No gap threshold can do
        # this: 2022 HL page 5 sets a Balmer energy-level diagram and a
        # photograph of a diamond 26 points apart and they answer different
        # parts, while the reaction scheme on 2023 HL page 9 has a 23-point
        # gap INSIDE it. What separates the first pair is the sentence
        # printed between them.
        split = any(foot < ln[1] and ln[3] < r[1] for ln in prose)
        if split or r[1] - foot > BAND_GAP:
            groups.append(cur)
            cur = []
        cur.append(r)
    groups.append(cur)

    out = []
    for g in groups:
        x0 = min(r[0] for r in g)
        y0 = min(r[1] for r in g)
        x1 = max(r[2] for r in g)
        y1 = max(r[3] for r in g)
        if x1 - x0 < MIN_W or y1 - y0 < MIN_H:
            continue
        # Grow to the labels printed among the artwork, then again in case a
        # label sits just outside the first box: "Poly(ethene)" is set to the
        # LEFT of everything drawn on 2023 HL page 9.
        labels = []
        for _ in range(2):
            for ln, text in text_lines(page):
                if FURNITURE.match(text) or PART_MARKER.match(text):
                    continue
                # A figure LABEL is short and sits inside the artwork. The
                # question's own prose is neither, and growing to anything
                # merely NEAR the band swallowed it: the first crop of 2023 HL
                # Q8's reaction scheme ran on down through "(a) (i) What is an
                # elimination reaction?" and would have shown the student the
                # questions along with the diagram.
                if len(text) > LABEL_MAX or STRAY_WORD.fullmatch(text):
                    continue
                lx0, ly0, lx1, ly1 = ln
                if ly0 < y0 - 4 or ly1 > y1 + 4:
                    continue
                if lx0 < x0 - 20 or lx0 > x1 + 20:
                    continue
                x0, y0 = min(x0, lx0), min(y0, ly0)
                x1, y1 = max(x1, lx1), max(y1, ly1)
                if text not in labels:
                    labels.append(text)
        # Clamp against the question's own prose above and below. The pad
        # that keeps a diagram off its own edge is enough to catch the top of
        # the next printed line, and 2023 HL Q8's boiling-point graphs came
        # out with a sliver of "...the boiling points" under the axis.
        keep = set(labels)
        for ln, text in text_lines(page):
            if text in keep or FURNITURE.match(text):
                continue
            lx0, ly0, lx1, ly1 = ln
            if lx1 < x0 - 4 or lx0 > x1 + 4:
                continue                       # beside the figure, not in it
            if ly1 <= y0:
                y0 = max(y0, ly1 + 2)
            elif ly0 >= y1:
                y1 = min(y1, ly0 - 2)
        out.append((x0, y0, x1, y1, labels))
    return out


def text_lines(page):
    for bl in page.get_text('dict')['blocks']:
        for ln in bl.get('lines', []):
            text = ' '.join(''.join(s['text'] for s in ln['spans']).split())
            if text:
                yield tuple(ln['bbox']), text


def open_questions():
    """{(year, level, q): [labels]} for open asks that point at printed matter."""
    want = collections.defaultdict(list)
    papers = {}
    for p in R.reconcile_subject('chemistry')['papers']:
        yr, lv = p['year'], p['level']
        for label in p.get('open', []):
            m = LABEL.match(label.strip())
            if not m:
                continue
            q = int(m.group(1))
            letter, roman = m.group(2), m.group(3)
            if letter and re.fullmatch(r'[ivx]+', letter) and not roman:
                letter, roman = None, letter
            P = papers.setdefault((yr, lv), PP.Paper('chemistry', yr, lv))
            try:
                ask = P.text(q, letter, roman) or ''
            except Exception:                                # noqa: BLE001
                ask = ''
            if ask.strip() and POINTS_AT.search(ask):
                want[(yr, lv, q)].append(label)
    return want


def pages_for(P, q):
    """Every page index whose text opens with this question's own head."""
    doc = pymupdf.open(P.files[0])
    hits = []
    for n in range(doc.page_count):
        head = doc[n].get_text()[:400]
        if re.search(rf'(?m)^\s*{q}\.\s', head):
            hits.append(n)
    doc.close()
    return hits


def crop(year, level, q, write=False):
    P = PP.Paper('chemistry', year, level)
    doc = pymupdf.open(P.files[0])
    made = []
    for n in pages_for(P, q):
        page = doc[n]
        for i, (x0, y0, x1, y1, labels) in enumerate(bands(page)):
            # Pad sideways only; the vertical edges are already clamped to
            # the prose above and below and must not grow back into it.
            rect = pymupdf.Rect(max(0, x0 - PAD), y0,
                                min(page.rect.width, x1 + PAD), y1)
            name = (f'chemistry-{year}-{level.upper()}-paper-'
                    f'q{q}-fig{i}')
            if write:
                d = os.path.join(ROOT, 'exam-papers', 'chemistry', 'figures',
                                 f'{year}-{level}')
                os.makedirs(d, exist_ok=True)
                page.get_pixmap(clip=rect, dpi=DPI).save(
                    os.path.join(d, f'{name}.png'))
            made.append((name, n, rect, labels))
    doc.close()
    return made


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('year', nargs='?', type=int)
    ap.add_argument('level', nargs='?')
    ap.add_argument('q', nargs='?', type=int)
    ap.add_argument('--write', action='store_true')
    ap.add_argument('--catalogue', action='store_true')
    args = ap.parse_args()

    if args.q:
        targets = {(args.year, args.level, args.q): []}
    else:
        targets = open_questions()

    catalogue = []
    for (year, level, q), asks in sorted(targets.items()):
        made = crop(year, level, q, write=args.write or args.catalogue)
        if args.catalogue:
            for name, page_no, rect, labels in made:
                catalogue.append({
                    'file': f'{name}.png', 'kind': 'figure', 'truncated': False,
                    'questionRef': f'{year} {level.upper()} Q{q}',
                    'labels': labels,
                    'page': page_no,
                    'size': [round(rect.width), round(rect.height)],
                })
        else:
            print(f'{year} {level.upper()} Q{q}: {len(made)} figure(s)'
                  + (f'  for {len(asks)} open ask(s)' if asks else ''))
            for name, page_no, rect, labels in made:
                print(f'   {name}  p{page_no}  '
                      f'{round(rect.width)}x{round(rect.height)}  '
                      f'labels={labels[:8]}')
    if args.catalogue:
        print(json.dumps(catalogue, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()
