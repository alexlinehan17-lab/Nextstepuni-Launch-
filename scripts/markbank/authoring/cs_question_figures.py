#!/usr/bin/env python3
"""Crop the code a Computer Science question prints, so its asks can be carded.

    python3 scripts/markbank/authoring/cs_question_figures.py 2024 hl 2
    python3 scripts/markbank/authoring/cs_question_figures.py --write
    python3 scripts/markbank/authoring/cs_question_figures.py --catalogue

Seventy-four open asks point at something printed, and in this subject that is
almost always a PROGRAM. The text layer hands a listing back as
"1 number = 27 2 while number < 39: 3 print(number, end=" ") 4 number = number
+ 3" -- the line numbers run into the code, the indentation gone, which is the
one thing a program cannot survive losing. No card can carry that as text.

Finding it needs no clustering or guesswork, unlike the diagrams in Chemistry:
the SEC sets code in Courier and nothing else on the page in Courier. The line
numbers are CourierNewPS-BoldMT at x=62 and the code CourierNewPSMT at x=83,
against Calibri prose at 12pt. So a code block is a run of consecutive Courier
lines, and its extent is exactly their bounding box.

The crop is the paper's own print, indentation and all. Alt text names the
question and quotes the first line, which is the most a description of a
program can honestly say without paraphrasing it.
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

DPI = 150
PAD_X, PAD_Y = 10.0, 6.0
MONO = re.compile(r'courier', re.I)
# A listing shorter than this is an inline token in Courier ("the variable
# `x`"), not a program the card has to show.
MIN_LINES = 2


def mono_runs(page):
    """[(x0, y0, x1, y1, [lines])] for each run of consecutive Courier lines."""
    rows = []
    for bl in page.get_text('dict')['blocks']:
        for ln in bl.get('lines', []):
            spans = ln.get('spans') or []
            if not spans:
                continue
            text = ''.join(s['text'] for s in spans)
            if not text.strip():
                continue
            mono = sum(len(s['text']) for s in spans if MONO.search(s['font']))
            rows.append((ln['bbox'], text, mono > 0))
    rows.sort(key=lambda r: (round(r[0][1], 1), r[0][0]))

    runs, cur = [], []
    for bbox, text, is_mono in rows:
        if is_mono:
            if cur and bbox[1] - cur[-1][0][3] > 18:
                runs.append(cur)
                cur = []
            cur.append((bbox, text))
        elif cur:
            runs.append(cur)
            cur = []
    if cur:
        runs.append(cur)

    out = []
    for run in runs:
        if len({round(b[1]) for b, _ in run}) < MIN_LINES:
            continue
        x0 = min(b[0] for b, _ in run)
        y0 = min(b[1] for b, _ in run)
        x1 = max(b[2] for b, _ in run)
        y1 = max(b[3] for b, _ in run)
        out.append((x0, y0, x1, y1, [t for _, t in run]))
    return out


def question_pages(P, q):
    """Page indexes carrying this question's head, in booklet order."""
    hits = []
    for path in P.files:
        with pymupdf.open(path) as doc:
            for n in range(doc.page_count):
                if re.search(rf'(?m)^\s*Question\s+{q}\b', doc[n].get_text()):
                    hits.append((path, n))
    return hits


def crop(year, level, q, write=False):
    P = PP.Paper('computer-science', year, level)
    made = []
    for path, n in question_pages(P, q):
        with pymupdf.open(path) as doc:
            page = doc[n]
            for i, (x0, y0, x1, y1, lines) in enumerate(mono_runs(page)):
                rect = pymupdf.Rect(max(0, x0 - PAD_X), max(0, y0 - PAD_Y),
                                    min(page.rect.width, x1 + PAD_X),
                                    min(page.rect.height, y1 + PAD_Y))
                name = (f'computer-science-{year}-{level.upper()}-paper-'
                        f'q{q}-code{i}')
                if write:
                    d = os.path.join(ROOT, 'exam-papers', 'computer-science',
                                     'figures', f'{year}-{level}')
                    os.makedirs(d, exist_ok=True)
                    page.get_pixmap(clip=rect, dpi=DPI).save(
                        os.path.join(d, f'{name}.png'))
                made.append((name, n, rect, lines))
    return made


def describe(year, level, q, lines):
    body = [' '.join(t.split()) for t in lines if t.strip()]
    opener = next((b for b in body if len(b) > 3), '')
    return (f'The program printed with {year} {level.upper()} Question {q}, '
            f'as the State Examinations Commission set it, with its line '
            f'numbers and indentation. It runs to {len(body)} lines and '
            f'begins: {opener[:120]}')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('year', nargs='?', type=int)
    ap.add_argument('level', nargs='?')
    ap.add_argument('q', nargs='?', type=int)
    ap.add_argument('--write', action='store_true')
    ap.add_argument('--catalogue', action='store_true')
    args = ap.parse_args()

    if args.q:
        targets = [(args.year, args.level, args.q)]
    else:
        sys.path.insert(0, DIR)
        import reconcile as R                                # noqa: E402
        from paper_census import census_subject              # noqa: E402
        idx = R.leaf_index(census_subject('computer-science'))
        seen = collections.OrderedDict()
        for (yr, lv, _), leaves in sorted(idx.items()):
            for leaf in leaves:
                seen.setdefault((yr, lv, leaf[1]), None)
        targets = list(seen)

    catalogue, total = [], 0
    for year, level, q in targets:
        try:
            made = crop(year, level, q, write=args.write or args.catalogue)
        except Exception as exc:                             # noqa: BLE001
            print(f'{year} {level} Q{q}: {type(exc).__name__}: {exc}')
            continue
        total += len(made)
        for name, page_no, rect, lines in made:
            if args.catalogue:
                catalogue.append({
                    'file': f'{name}.png', 'kind': 'figure', 'truncated': False,
                    'questionRef': f'{year} {level.upper()} Q{q}',
                    'description': describe(year, level, q, lines),
                })
            elif not args.write:
                print(f'{year} {level.upper()} Q{q}: {name}  p{page_no}  '
                      f'{len(lines)} lines  {round(rect.width)}x{round(rect.height)}')
    if args.catalogue:
        print(json.dumps(catalogue, ensure_ascii=False, indent=1))
    elif not args.q:
        print(f'TOTAL {total} code listing(s)')


if __name__ == '__main__':
    main()
