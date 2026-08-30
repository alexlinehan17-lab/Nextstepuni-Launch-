#!/usr/bin/env python3
"""Crop the printed matter a PART is built on, for any subject.

    python3 scripts/markbank/authoring/question_art.py agricultural-science
    python3 scripts/markbank/authoring/question_art.py agricultural-science --write
    python3 scripts/markbank/authoring/question_art.py <subject> --catalogue

The worklist is the deck itself: every card whose text points at something
printed -- "Identify the conditions necessary for germination by placing a tick
in the correct box", "From your diagram above" -- and which carries no figure.
Those cards cannot be answered by a student, and the crop is the missing input.

The geometry is cs_question_figures'. It was written for Computer Science and
every hard part of it is subject-agnostic: which bands of a page are printed
matter rather than the ruled space a candidate writes in, how to follow a
table down through its own rules, how to trim a blank answer box off the top,
the foot or the side. Importing it is the point -- a second copy would drift,
and the rules it encodes were each found by opening a crop and looking at it.

What this adds is the PART BAND. Computer Science crops one figure per
question; here the worklist is per part, and a question's parts each have
their own table -- Agricultural Science 2025 OL Q5 prints a soil diagram for
(a) and (b) and a three-row tick-box for (c). So the page is cut at the part
markers and only the bands inside the part's own slice are considered.
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
import cs_question_figures as G                             # noqa: E402

DPI = 150
PAD = 8.0
# The same test the audit uses: a reference to something PRINTED that the card
# would have to show. Kept here rather than imported so the two can be read
# side by side.
POINTS_AT = re.compile(
    r'\b(?:from your |in your |the )?(?:diagram|graph|chart|sketch|figure|fig\.?'
    r'|table|photograph|photo|image|picture|drawing|flowchart|map|extract'
    r'|passage|text|cartoon|label(?:led)?)\b[^.]{0,40}?'
    r'\b(?:above|below|shown|opposite|following|provided|supplied|attached)\b'
    r'|\b(?:above|below|opposite|shown)\b[^.]{0,20}\b(?:diagram|graph|table|figure)\b'
    r'|\bfrom (?:your|the) (?:diagram|graph|table|figure)\b'
    r'|\btick\b[^.]{0,30}\b(?:box|table|column)\b'
    r'|\brefer(?:ring)? to the (?:diagram|graph|table|figure|extract|passage)\b',
    re.I)
REF = re.compile(r'^(\d{4})\s+(HL|OL)\s+(?:Paper\s*\d+\s+)?Q(\d{1,2})'
                 r'(?:\(([a-z])\))?(?:\(([ivxlc]+)\))?', re.I)
MARKER = re.compile(r'^\(([a-z]{1,4})\)')


def worklist(subject):
    """(year, level, q, letter, roman, card id) for every bare pointing card."""
    path = os.path.join(ROOT, 'scripts', 'markbank', 'authored', f'{subject}.json')
    out = []
    for card in json.load(open(path, encoding='utf-8')):
        if card.get('figureKey') or card.get('questionFigureKey'):
            continue
        text = ' '.join(f"{card.get('questionText') or ''} "
                        f"{card.get('stem') or ''}".split())
        if not POINTS_AT.search(text):
            continue
        m = REF.match(card.get('questionRef') or '')
        if not m:
            continue
        out.append((int(m.group(1)), m.group(2).lower(), int(m.group(3)),
                    m.group(4), m.group(5), card['id']))
    return out


def part_band(page, q, letter, roman):
    """(top, bottom) of the slice of this page the part owns, or None.

    Cut at the PART MARKERS. A question's parts each have their own printed
    matter and the page has to be divided between them, or (c)'s tick-box
    table is cropped for (a) as well.
    """
    marks = []
    for (x0, y0, x1, y1), text in G.text_lines(page):
        m = MARKER.match(text.strip())
        if m and x0 < page.rect.width * 0.35:
            marks.append((y0, m.group(1)))
    want = roman or letter
    if want is None:
        # A card citing the whole QUESTION cannot say which of its parts the
        # picture belongs to, and taking the page entire crops whatever else
        # is on it: 2024 OL Q3 came out as a grazing diagram with parts (b),
        # (c) and (d)'s empty answer boxes stacked underneath. Those need a
        # figure bound by hand.
        return None
    marks.sort()
    for i, (y, label) in enumerate(marks):
        if label != want:
            continue
        nxt = marks[i + 1][0] if i + 1 < len(marks) else page.rect.height
        return y, nxt
    return None


def pages_for(P, q):
    """Page indexes carrying this question, in booklet order."""
    hits = []
    for path in P.files:
        with pymupdf.open(path) as doc:
            for n in range(doc.page_count):
                # Any page the question could be on. Precision comes from the
                # PART BAND below, not from here: a page that does not carry
                # this part's marker yields no band and is passed over.
                if re.search(rf'(?m)^\s*(?:Question\s+)?{q}[.\s]',
                             doc[n].get_text()):
                    hits.append((path, n))
    return hits


def crop_part(subject, year, level, q, letter, roman, write=False):
    """The one crop this part needs, or None."""
    P = PP.Paper(subject, year, level)
    for path, n in pages_for(P, q):
        with pymupdf.open(path) as doc:
            page = doc[n]
            band = part_band(page, q, letter, roman)
            if band is None:
                continue
            top, bottom = band
            runs = G.mono_runs(page)
            bands = [b for b in G.figure_bands(page, runs)
                     if b[1] >= top - 6 and b[3] <= bottom + 6]
            if not bands:
                continue
            # Several bands are one picture only if what lies BETWEEN them is
            # not the candidate's answer space. 2024 OL Q3 spans a grazing
            # diagram, then part (b)'s ruled box, then (c)'s and (d)'s, and
            # the union of all of it is a crop of three empty boxes with a
            # fragment of diagram on top. A wrong crop is worse than none.
            rows = list(G.text_lines(page))
            bands.sort(key=lambda b: b[1])
            clear = True
            for a, nxt in zip(bands, bands[1:]):
                if nxt[1] - a[3] <= 4.0:
                    continue
                if not G.gap_is_clear(page, min(a[0], nxt[0]), a[3],
                                      max(a[2], nxt[2]), nxt[1], rows):
                    clear = False
                    break
            if not clear:
                continue
            x0 = min(b[0] for b in bands)
            y0 = min(b[1] for b in bands)
            x1 = max(b[2] for b in bands)
            y1 = max(b[3] for b in bands)
            # The union can still end inside the candidate's answer space when
            # the box sits hard against the picture: 2022 OL Q4(b) prints its
            # composition table and a photograph, then "Protein: / Fibre:"
            # over six ruled lines with no gap between.
            y1 = G.trim_answer_box(page, x0, y0, x1, y1, rows)
            top, bot = max(0.0, y0 - PAD), min(page.rect.height, y1 + PAD)
            # A crop may leave a line of type out; it must not show the top
            # half of one. Applied AFTER the padding, because it is the
            # padding that reaches back into the line above.
            for (lx0, ly0, lx1, ly1), _ in rows:
                if lx1 < x0 - 2 or lx0 > x1 + 2:
                    continue
                if ly0 < top < ly1:
                    top = ly1 + 1
                if ly0 < bot < ly1:
                    bot = ly0 - 1
            rect = pymupdf.Rect(max(0.0, x0 - PAD), top,
                                min(page.rect.width, x1 + PAD), bot)
            part = (f'q{q}' + (f'{letter}' if letter else '')
                    + (f'{roman}' if roman else ''))
            name = (f'{subject}-{year}-{level.upper()}-paper-{part}-art')
            if write:
                d = os.path.join(ROOT, 'exam-papers', subject, 'figures',
                                 f'{year}-{level}')
                os.makedirs(d, exist_ok=True)
                page.get_pixmap(clip=rect, dpi=DPI).save(
                    os.path.join(d, f'{name}.png'))
            labels = [t for b in bands for t in b[4]]
            return name, rect, labels
    return None


def describe(subject, year, level, q, letter, roman, labels):
    ref = (f'{year} {level.upper()} Question {q}'
           + (f'({letter})' if letter else '') + (f'({roman})' if roman else ''))
    text = (f'The table or diagram printed with {ref}, as the State '
            f'Examinations Commission set it.')
    if labels:
        text += ' It reads: ' + ', '.join(labels[:14])[:400] + '.'
    return text


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('subject')
    ap.add_argument('--write', action='store_true')
    ap.add_argument('--catalogue', action='store_true')
    args = ap.parse_args()

    made, missed, catalogue = [], [], []
    for year, level, q, letter, roman, cid in worklist(args.subject):
        try:
            got = crop_part(args.subject, year, level, q, letter, roman,
                            write=args.write or args.catalogue)
        except Exception as exc:                             # noqa: BLE001
            print(f'{cid}: {type(exc).__name__}: {exc}', file=sys.stderr)
            got = None
        if not got:
            missed.append((cid, f'{year} {level.upper()} Q{q}'
                                f'{f"({letter})" if letter else ""}'
                                f'{f"({roman})" if roman else ""}'))
            continue
        name, rect, labels = got
        made.append((cid, name, round(rect.width), round(rect.height)))
        if args.catalogue:
            catalogue.append({
                'file': f'{name}.png', 'kind': 'figure', 'truncated': False,
                'questionRef': (f'{year} {level.upper()} Q{q}'
                                + (f'({letter})' if letter else '')
                                + (f'({roman})' if roman else '')),
                'cardId': cid,
                'description': describe(args.subject, year, level, q, letter,
                                        roman, labels),
            })
    if args.catalogue:
        print(json.dumps(catalogue, ensure_ascii=False, indent=1))
        return 0
    print(f'{len(made)} cropped, {len(missed)} with nothing to crop')
    for cid, name, w, h in made:
        print(f'   {cid:26} {w:4}x{h:<4} {name}')
    for cid, ref in missed:
        print(f'   MISSED {cid:20} {ref}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
