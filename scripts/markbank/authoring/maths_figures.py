#!/usr/bin/env python3
"""Crop each Mathematics unit's model solution out of the scheme PDF.

    python3 scripts/markbank/authoring/maths_figures.py 2025 hl [--write]

The model solution is the one part of a Maths scheme that must NOT be text. Its
notation extracts readably but its structure does not -- fractions flatten,
limits detach, lines reorder -- so on a card it belongs as the image the SEC
printed. mathtext.py explains why; this cuts it out.

Every unit already knows its page and its vertical band, because the scheme is
segmented on the Scale lines in the marking-notes column. The crop is that band,
left of the column boundary, with a little air around it.
"""
import collections
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import maths_scheme                                          # noqa: E402
import mathtext                                              # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))))
# bind-figures.mjs reads from here and derives the subject, year and level from
# the FILE NAME, so both have to match what it expects. Nothing about a figure
# is passed to it by hand -- that is how both historical figure corruptions in
# this repo happened.
def out_dir(year, level):
    return os.path.join(ROOT, 'exam-papers', 'maths', 'figures', f'{year}-{level}')
# Scheme-front furniture that shares a page with the first marked unit.
HEADER = re.compile(
    r'^(?:Detailed marking notes|Model Solutions? (?:&|and) Marking Notes'
    r'|Note:|other correct solutions|particular candidate|Section [A-C]\b'
    r'|Model Solutions? & Detailed)', re.I)
TABLE_HEAD = re.compile(r'Model Solution\s*[–\u2013-]\s*\d+\s*Marks', re.I)
COLUMN = 300          # where the Marking Notes column starts
PAD = 6
LINE = 16          # a line's own height, so the last one is not sliced
DPI = 200


def key_slug(key):
    paper, q, letter, roman = key[0], key[1], key[2], key[3]
    s = f'{paper}-q{q}'
    if letter:
        s += f'-{letter}'
    if roman:
        s += f'-{roman}'
    if len(key) > 4:
        s += f'-{key[4]}'
    return s


def crop(year, level, write=False):
    import pymupdf
    S = maths_scheme.Scheme(year, level)
    made = []
    seen = collections.defaultdict(int)
    for key in S.parts():
        page_no, lo, hi = S.band(key)
        page = S.doc[page_no]
        # Crop to the INK, not to the band. The band runs from one scale to the
        # next, which on a page holding one unit is the whole page: the first
        # crops were 818pt of mostly white with the next row's "(a)" clipped in
        # at the foot. The solution's own lines say where it actually is.
        import mathtext
        left, _ = mathtext.placed(page)
        # The page number sits alone at the foot and is not part of the answer;
        # counting it padded every crop with an inch of white.
        # The running footer is not part of the answer either. On a page whose
        # band is the whole page, "Leaving Certificate 2021 / Marking Scheme"
        # at y=801 stretched a solution that ends at y=251 into a 783x2116
        # crop -- the worked solution legible only as a thumbnail, floating at
        # the top of an inch of white. maths_scheme already knows these lines.
        ys = [y for y, t in left if lo - 4 <= y < hi and t.strip()
              and not re.fullmatch(r'\[?\d{1,3}\]?', t.strip())
              and not maths_scheme.FURNITURE.match(t.strip())
              and not HEADER.match(t.strip())]
        # The first unit on a page has a band that starts at the page top, so
        # everything above the solution table — the page title, the "Model
        # Solutions & Marking Notes" heading, the examiner's note paragraph —
        # was cropped INTO the card. The table's own head row says where the
        # SEC's answer actually begins; nothing above it is the solution.
        heads = [y for y, t in left if lo - 4 <= y < hi
                 and TABLE_HEAD.search(t.strip())]
        if heads:
            ys = [y for y in ys if y >= min(heads) - 2]
        if not ys:
            continue
        # And a trailing line cut off from the rest by more than four lines of
        # white is furniture the list does not name, not a continuation.
        ys.sort()
        for a, b in zip(ys, ys[1:]):
            if b - a > 90:
                ys = [y for y in ys if y <= a]
                break
        top = max(0, min(ys) - PAD)
        bottom = min(page.rect.height - 24, max(ys) + LINE + PAD)
        if bottom - top < 18:
            continue
        # The right edge is where the solution's own text ends, not a fixed
        # column line: clipping at 296pt sliced "[for all x in the domain of
        # g(x)]" in half.
        # Bounded by where the NOTES column actually begins on this page, not by
        # a guessed offset: too tight sliced "[for all x in the domain of g(x)]"
        # in half, too loose let the first letters of the notes bleed in down
        # the right-hand edge.
        # Measured from THIS page's own notes column, not the 300 constant.
        # The solution's own lines can start past 300 -- a centred "OR", an
        # indented expression -- and counting one of those as the notes column
        # pulled the right edge in to 296 on 2022 HL page 35, slicing
        # "P(O).P(U) = P(O n U):" in half. mathtext.column_cut reads the
        # boundary off the page's "Marking Notes" header.
        column = mathtext.column_cut(page) + 12
        notes_x = [min(sp['bbox'][0] for sp in ln['spans'])
                   for b in page.get_text('dict')['blocks'] for ln in b.get('lines', [])
                   if min(sp['bbox'][0] for sp in ln['spans']) >= column
                   and top <= min(sp['bbox'][1] for sp in ln['spans']) <= bottom]
        right_edge = (min(notes_x) - 6) if notes_x else column - 4
        rect = pymupdf.Rect(30, top, right_edge, bottom)
        name = f'maths-{year}-{level.upper()}-paper-p{page_no:03d}-i{seen[page_no]}'
        seen[page_no] += 1
        if write:
            d = out_dir(year, level)
            os.makedirs(d, exist_ok=True)
            page.get_pixmap(clip=rect, dpi=DPI).save(os.path.join(d, f'{name}.png'))
        made.append((name, key, round(rect.height), S.solution(key)))
    return made


if __name__ == '__main__':
    year, level = int(sys.argv[1]), sys.argv[2]
    made = crop(year, level, '--write' in sys.argv)
    if '--catalogue' in sys.argv:
        import json
        out = []
        for name, key, h, sol in made:
            body = ' '.join(t for t in sol
                            if t and not t.startswith('Model Solution')
                            and not re.fullmatch(r'Q\d+|\(?[a-z]{1,4}\)?|\[?\d{1,3}\]?', t.strip()))
            body = re.sub(r'\s+', ' ', body).strip()
            ref = ('Paper ' + str(key[0]) + ' Q' + str(key[1])
                   + (f'({key[2]})' if key[2] else '') + (f'({key[3]})' if key[3] else ''))
            # The description is the solution's OWN lines, demangled, not a
            # guess about a picture: this is typeset mathematics, and what it
            # says is recoverable even though its layout is not.
            # The quote is dropped when the text layer cannot be read cleanly.
            # A handful of solutions use glyphs no font table resolves, and
            # quoting them put strings like "h^(ᇱᇱ)(x)" in front of a reader
            # -- while the crop itself, which is a picture of the page, was
            # perfectly legible. Better a description that says less than one
            # that says it wrongly, and better than dropping a sound card.
            desc = (f'The marking scheme\'s printed worked solution for '
                    f'{year} {level.upper()} {ref}, typeset as the State '
                    f'Examinations Commission set it.')
            if not mathtext.unreadable(body):
                desc += f' It reads: {body[:420]}'
            out.append({'file': f'{name}.png', 'kind': 'figure',
                        'truncated': False, 'description': desc,
                        # every maths crop IS the scheme's worked solution —
                        # the session screen must hold it until reveal
                        'solution': True})
        print(json.dumps(out, ensure_ascii=False, indent=1))
    else:
        print(f'{len(made)} model-solution crops')
        for name, key, h, _ in made[:6]:
            print(f'   {name}  {h}pt tall')


def names(year, level):
    """{unit key: figure name} — what the cropper called each unit's solution.

    Derived by re-running the same walk, so the name a card references can never
    drift from the name the crop was written under.
    """
    return {key: name for name, key, _, _ in crop(year, level, write=False)}
