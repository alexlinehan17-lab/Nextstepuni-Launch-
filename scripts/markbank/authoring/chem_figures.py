#!/usr/bin/env python3
"""Crop the Chemistry scheme's own drawn answers as solution figures.

    python3 scripts/markbank/authoring/chem_figures.py 2021 ol           # list
    python3 scripts/markbank/authoring/chem_figures.py 2021 ol --write   # crop
    python3 scripts/markbank/authoring/chem_figures.py --catalogue       # all ten

Thirty-one of the open Chemistry asks want something DRAWN -- a molecular
structure, a dot-and-cross diagram, a completed nuclear equation -- and the
scheme answers every one of them with a picture. The text layer under that
picture is its scattered labels: "H H H H H H" for a benzene ring,
"/ 86 84 2 222 218 4" for an alpha decay. None of that can go on a card.

The scheme's own drawing can. This is the mechanism Economics used for its
worked calculations: crop the marking scheme's answer and publish it as a
figure marked `solution: true`, which the session screen holds back until the
student has committed to an answer. The crop is the SEC's own print, so it
states exactly what the examiner accepted and nothing else -- including, as
2021 OL Q5(d)(ii) shows, BOTH accepted representations of an O2 dot-and-cross
side by side, and the criteria beneath them.

The region comes from chem_scheme.crop_bounds(), which runs a part's cell from
its own marker row to the next part's -- the same boundary the table's ruling
draws. Cropping to the text the reader filed under the key would be useless
here: where the answer is a picture, that text is two points tall.

Nothing is invented. The alt text names the part and quotes the scheme's own
marking criteria where it prints any in words.
"""
import argparse
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
from chem_scheme import ChemScheme                          # noqa: E402

DPI = 150
LEFT, RIGHT = 40, 40
# The ask wants something drawn or an equation completed on the page.
WANTS_ARTWORK = re.compile(
    r'\b(draw|copy and complete|complete the following|dot and cross|'
    r'sketch|label(?:led)? diagram)\b', re.I)
LABEL = re.compile(r'Q(\d+)(?:\(([a-z]+)\))?(?:\(([a-z]+)\))?$')
# Text under the crop that states what the drawing must SHOW. Quoted into the
# alt text so a screen reader gets the criteria, not just "a diagram".
CRITERION = re.compile(r'\b(shown|show|labelled|indicated|correct|essential|'
                       r'need not|acceptable|allow)\b', re.I)


def out_dir(year, level):
    # bind-figures.mjs resolves a crop's source as
    # exam-papers/<subject>/figures/<year>-<level>/<file>, taking the year and
    # level from the FILENAME. The directory has to match that or the bind
    # skips with "source missing"; the crops are told apart from the paper's
    # own figures by the "-scheme-" in their names, not by their folder.
    return os.path.join(ROOT, 'exam-papers', 'chemistry', 'figures',
                        f'{year}-{level}')


def open_asks(year=None, level=None):
    """Every open ask whose answer the scheme draws."""
    out = []
    for p in R.reconcile_subject('chemistry')['papers']:
        if year and (p['year'] != year or p['level'] != level):
            continue
        for label in p.get('open', []):
            m = LABEL.match(label.strip())
            if not m:
                continue
            q = int(m.group(1))
            letter, roman = m.group(2), m.group(3)
            if letter and re.fullmatch(r'[ivx]+', letter) and not roman:
                letter, roman = None, letter
            out.append((p['year'], p['level'], q, letter, roman, label))
    return out


def crop(year, level, write=False):
    """[(name, key, ask, criteria, tariff)] for each drawn answer croppable."""
    S = ChemScheme(year, level)
    P = PP.Paper('chemistry', year, level)
    made = []
    for yr, lv, q, letter, roman, label in open_asks(year, level):
        try:
            ask = P.text(q, letter, roman) or ''
        except Exception:                                    # noqa: BLE001
            ask = ''
        if not ask.strip() or not WANTS_ARTWORK.search(ask):
            continue
        bounds = S.crop_bounds(q, letter, roman)
        if not bounds:
            continue
        page_no, y0, y1 = bounds
        if y1 - y0 < 24:
            continue                    # nothing but the marker row
        page = S.doc[page_no]
        rect = pymupdf.Rect(LEFT, y0, page.rect.width - RIGHT, min(y1, 782.0))
        name = (f'chemistry-{year}-{level.upper()}-scheme-'
                f'q{q}' + (f'{letter}' if letter else '')
                + (f'-{roman}' if roman else ''))
        if write:
            d = out_dir(year, level)
            os.makedirs(d, exist_ok=True)
            page.get_pixmap(clip=rect, dpi=DPI).save(os.path.join(d, f'{name}.png'))
        criteria = [t for t in S.points(q, letter, roman)
                    if CRITERION.search(t) and len(t.split()) >= 3]
        criteria += [a for a in S.asides(q, letter, roman) if len(a.split()) >= 3]
        made.append((name, (q, letter, roman), ask,
                     criteria, S.tariff(q, letter, roman, rows=1),
                     round(rect.height)))
    return made


def describe(year, level, name, key, ask, criteria):
    q, letter, roman = key
    ref = (f'{year} {level.upper()} Q{q}' + (f'({letter})' if letter else '')
           + (f'({roman})' if roman else ''))
    text = (f"The marking scheme's own answer to {ref}, drawn as the State "
            f'Examinations Commission printed it. The question asks: '
            f'{" ".join(ask.split())[:180]}')
    if criteria:
        joined = ' '.join(' '.join(c.split()) for c in criteria)
        text += f' The scheme requires: {joined[:300]}'
    return text


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('year', nargs='?', type=int)
    ap.add_argument('level', nargs='?')
    ap.add_argument('--write', action='store_true')
    ap.add_argument('--catalogue', action='store_true')
    args = ap.parse_args()

    sittings = ([(args.year, args.level)] if args.year
                else [(y, l) for y in range(2021, 2026) for l in ('hl', 'ol')])
    catalogue, total = [], 0
    for year, level in sittings:
        made = crop(year, level, write=args.write or args.catalogue)
        total += len(made)
        if args.catalogue:
            for name, key, ask, criteria, tariff, height in made:
                catalogue.append({
                    'file': f'{name}.png', 'kind': 'figure', 'truncated': False,
                    'description': describe(year, level, name, key, ask, criteria),
                    # Every crop here IS the marking scheme's answer, so the
                    # session screen must hold it back until the student has
                    # committed to one of their own.
                    'solution': True,
                })
        else:
            print(f'{year} {level}: {len(made)} drawn answer(s)')
            for name, key, ask, criteria, tariff, height in made[:6]:
                print(f'   {name}  {height}pt  tariff={tariff}  '
                      f'{" ".join(ask.split())[:60]!r}')
    if args.catalogue:
        print(json.dumps(catalogue, ensure_ascii=False, indent=1))
    else:
        print(f'TOTAL {total}')


if __name__ == '__main__':
    main()
