#!/usr/bin/env python3
"""Cut the printed drawing each DCG question is answered from.

    python3 scripts/markbank/authoring/dcg_figures.py --cut
    python3 scripts/markbank/authoring/dcg_figures.py --sheets   # to look at
    python3 scripts/markbank/authoring/dcg_figures.py --catalogue alt.json

EVERY DCG QUESTION NEEDS ITS DRAWING. "Complete the elevation of the display
stand, including all hidden detail" cannot be answered, or even understood,
without the plan and part-elevation printed beside it -- this is a graphics
examination, and the words are captions on the artwork rather than the other
way round. So one crop is cut per QUESTION and every card of that question
carries it, which is the same rule Computer Science's question crops follow:
the SEC prints the drawing once for the whole question.

WHAT IS CROPPED IS A PAGE OR A QUADRANT, not an extracted figure.

  Sections B and C set ONE question to a page, so the crop is that page inside
  its margins -- the running head, the foliation and the section rubric come
  off, everything the candidate reads and draws from stays. Cutting the
  artwork out of it instead would drop the dimensioned stimulus photograph at
  the top of most questions, which the question's own first sentence points at
  ("The image on the right shows the Virgin Media sports studio desk").

  Section A sets FOUR questions in ruled quadrants on one sideways A3 sheet,
  so the crop is the quadrant. Its bounds come from the question markers
  themselves -- the sheet's two columns and two rows are where the SEC put
  "A-1" to "A-4" -- taken back through the page rotation, because the sheet is
  /Rotate 90 with its text drawn at dir (0,-1).

The contour map that Section C's Geologic Geometry question is answered on is
printed on the BACK PAGE OF THE SECTION A BOOKLET, not with the question. No
crop of the question's own page can show it, so the card says where it is
printed rather than pretending the crop is complete.

NOTHING IS CATALOGUED UNSEEN. --cut writes the PNGs and --sheets lays them out
for inspection; the manifest entry, with its alt text and its md5, is written
by --catalogue from a file of descriptions written after LOOKING at them.
"""
import argparse
import collections
import hashlib
import json
import os
import re
import sys

import pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, HERE)

import dcg_paper as DP                                       # noqa: E402
import paper_census as PC                                    # noqa: E402

SUBJECT = 'dcg'
OUT_DIR = os.path.join(ROOT, 'public', 'exam-figures', SUBJECT, 'markbank')
MANIFEST = os.path.join(ROOT, 'components', 'MarkBank', f'figures-{SUBJECT}.json')
SHEET_DIR = os.path.join(ROOT, '.dcg-figure-sheets')
DPI = 110
LEVEL_WORD = {'hl': 'Higher', 'ol': 'Ordinary'}
TITLE = 'Design and Communication Graphics'

# The side margins a Sections B and C page is cropped inside. The TOP and
# BOTTOM are read from the page rather than fixed: a fixed head margin cut the
# first line off every question whose marker sits high ("B-2 The image on the
# right shows the ... Bridge in Drogheda") and left the section rubric on
# every question that opens a section.
PAGE_SIDES = (34, 26)                   # left, right

# The running foot: the sitting, the foliation and the paper's own name. It is
# printed BELOW the question on every Sections B and C page.
#
# The bare page NUMBER is deliberately not in this pattern. A dimension label
# on a detail drawing is also a bare one- or two-digit number -- "84", "16",
# "8" -- and matched here every one of them counted as running foot: the 2026
# Ordinary C-5 crop stopped at y=543 on an 842pt page because a "35" beside
# part 1 was read as the foliation, and half the parts of the assembly were
# cut off the picture. The foliation is identified by WHERE it is instead, in
# the bottom tenth of the page, by foliation() below.
RUNNING_FOOT = re.compile(
    r'^(?:Leaving Certificate\b|Page\s+\d+\s+of\s+\d+'
    r'|Design\s*&\s*Comm)', re.I)
FOOT_BAND = 0.90


def foliation(row, height):
    """Is this row the page number, rather than a number on a drawing?"""
    text = row[3].strip()
    return text.isdigit() and len(text) <= 3 and row[0] > height * FOOT_BAND

# The banner the SEC rules across the foot of the A3 sheet. It is not part of
# any question, and a quadrant cut to a fixed margin caught the top of its
# letters on the bottom row of every sitting.
FOOT_BANNER = re.compile(
    r'This examination paper must be returned|Do not hand this up', re.I)


def key_for(year, level, section, q):
    return f'{SUBJECT}-{year}-{level.upper()}-paper-sec{section}-q{q}-art'


def _render_box(page, rows_):
    """A (vy, vx) reading-coordinate box put back into the page's own space."""
    vy0 = min(r[0] for r in rows_)
    vy1 = max(r[0] for r in rows_)
    vx0 = min(r[1] for r in rows_)
    vx1 = max(r[2] for r in rows_)
    return vy0, vy1, vx0, vx1


def quadrants(page):
    """{(section, q): Rect} for the A3 sheet that sets four questions at once.

    The markers name the sheet's columns and rows; a quadrant runs from just
    above and left of its own marker to just short of the next one, and to the
    sheet's own margin where there is no next one.
    """
    rows_ = DP.rows(page)
    heads = [(r, DP.QHEAD.match(r[3])) for r in rows_]
    heads = [(r, m) for r, m in heads if m]
    if not heads:
        return {}
    rotated = page.rotation == 90
    W, H = page.rect.width, page.rect.height

    def to_x(vx):
        return W + vx if rotated else vx

    cols = sorted({round(to_x(r[1])) for r, _m in heads})
    rows = sorted({round(r[0]) for r, _m in heads})
    cols = _thin(cols, 120)
    rows = _thin(rows, 80)
    foot = min([r[0] for r in rows_ if FOOT_BANNER.search(r[3])]
               + [H - 34], default=H - 34) - 8
    out = {}
    for r, m in heads:
        x = to_x(r[1])
        y = r[0]
        ci = max(i for i, c in enumerate(cols) if c <= x + 8)
        ri = max(i for i, c in enumerate(rows) if c <= y + 6)
        x0 = cols[ci] - 14 if ci else 18
        x1 = cols[ci + 1] - 14 if ci + 1 < len(cols) else W - 18
        y0 = rows[ri] - 14 if ri else rows[0] - 16
        y1 = rows[ri + 1] - 14 if ri + 1 < len(rows) else foot
        out[(m.group(1), int(m.group(2)))] = pymupdf.Rect(x0, y0, x1, y1)
    return out


def page_box(page, page_rows, head):
    """The crop for a page that sets ONE question: head to running foot.

    The top is the highest thing belonging to the question -- its own marker,
    or the Applied Graphics option banner the SEC prints above it -- and the
    bottom is the running foot, wherever the SEC set it that year.
    """
    H = page.rect.height
    top = head[0]
    for row in page_rows:
        if row[3].strip().lower() in DP.OPTIONS and row[0] < top:
            top = row[0]
    def is_foot(row):
        return RUNNING_FOOT.match(row[3]) or foliation(row, H)

    feet = [row[0] for row in page_rows
            if row[0] > head[0] and is_foot(row)]
    content = [row[0] for row in page_rows
               if row[0] > head[0] and not is_foot(row)]
    bottom = (min(feet) - 10) if feet else H - 46
    # An assembly question's PARTS LIST runs down beside the running foot --
    # 2019 Higher C-5 sets its last row, "13 Transparent Top Cover", at y=776
    # while the page number sits at y=781 in the middle of the page. Cut above
    # the foot, five of the thirteen parts went with it. Where the question's
    # own content reaches into the foot band the crop follows the content and
    # takes a line of running foot with it, which is the cheaper loss.
    if content and max(content) > bottom - 4:
        bottom = max(content) + 13
    return pymupdf.Rect(PAGE_SIDES[0], max(top - 14, 18),
                        page.rect.width - PAGE_SIDES[1], min(bottom, H - 26))


def _thin(values, gap):
    out = []
    for v in values:
        if not out or v - out[-1] >= gap:
            out.append(v)
    return out


def cut(census=None):
    """Write one PNG per question. Returns [(key, path, year, level, sec, q)]."""
    os.makedirs(OUT_DIR, exist_ok=True)
    census = census or PC.census_subject(SUBJECT)
    made = []
    for paper in census['papers']:
        year, level = paper['year'], paper['level']
        P = DP.load(year, level, SUBJECT)
        for path in P.files:
            doc = pymupdf.open(path)
            for page in doc:
                page_rows = DP.rows(page)
                heads = [r for r in page_rows if DP.QHEAD.match(r[3])]
                if not heads:
                    continue
                if len(heads) == 1:
                    m = DP.QHEAD.match(heads[0][3])
                    boxes = {(m.group(1), int(m.group(2))):
                             page_box(page, page_rows, heads[0])}
                else:
                    boxes = quadrants(page)
                for (section, q), rect in boxes.items():
                    key = key_for(year, level, section, q)
                    out = os.path.join(OUT_DIR, f'{key}.png')
                    pix = page.get_pixmap(dpi=DPI, clip=rect)
                    pix.save(out)
                    made.append((key, out, year, level, section, q))
            doc.close()
    return made


def sheets(made):
    """Contact sheets, two questions to a sheet, for inspection."""
    os.makedirs(SHEET_DIR, exist_ok=True)
    made = sorted(made, key=lambda r: (r[2], r[3], r[4], r[5]))
    n = 0
    for i in range(0, len(made), 2):
        batch = made[i:i + 2]
        pages = [pymupdf.open(row[1]) for row in batch]
        pix = [p[0].get_pixmap() for p in pages]
        width = sum(x.width for x in pix) + 20
        height = max(x.height for x in pix)
        sheet = pymupdf.open()
        page = sheet.new_page(width=width, height=height)
        x = 0
        for row, image in zip(batch, pix):
            page.insert_image(pymupdf.Rect(x, 0, x + image.width, image.height),
                              filename=row[1])
            x += image.width + 20
        name = '__'.join(r[0] for r in batch)
        page.get_pixmap().save(os.path.join(SHEET_DIR, f'{name}.png'))
        for p in pages:
            p.close()
        sheet.close()
        n += 1
    return n


def catalogue(alt_path):
    """Write the manifest from descriptions that were written after looking."""
    with open(alt_path, encoding='utf-8') as fh:
        alt = json.load(fh)
    manifest = {}
    if os.path.exists(MANIFEST):
        with open(MANIFEST, encoding='utf-8') as fh:
            manifest = json.load(fh)
    missing, written = [], 0
    for key, text in sorted(alt.items()):
        path = os.path.join(OUT_DIR, f'{key}.png')
        if not os.path.exists(path):
            missing.append(key)
            continue
        m = re.fullmatch(r'dcg-(\d{4})-(HL|OL)-paper-sec([ABC])-q(\d)-art', key)
        year, level, section, q = (int(m.group(1)), m.group(2).lower(),
                                   m.group(3), int(m.group(4)))
        with open(path, 'rb') as fh:
            md5 = hashlib.md5(fh.read()).hexdigest()
        manifest[key] = {
            'src': f'/exam-figures/{SUBJECT}/markbank/{key}.png',
            'md5': md5,
            'alt': ' '.join(text.split()),
            'lettersVisible': [],
            'labelMeanings': [],
            'questionRef': f'{year} {level.upper()} Section {section} Q{q}',
            'year': year,
            'level': 'higher' if level == 'hl' else 'ordinary',
            'attribution': (f'SEC Leaving Certificate {TITLE} {year} '
                            f'{LEVEL_WORD[level]} Level '
                            '— © State Examinations Commission'),
        }
        written += 1
    with open(MANIFEST, 'w', encoding='utf-8') as fh:
        json.dump(manifest, fh, ensure_ascii=False, indent=1, sort_keys=True)
        fh.write('\n')
    print(f'{written} entries written to {MANIFEST}')
    for key in missing:
        print(f'  NO CROP for {key}')
    return len(missing)


def worklist():
    """Every question crop that has no inspected description yet."""
    manifest = {}
    if os.path.exists(MANIFEST):
        with open(MANIFEST, encoding='utf-8') as fh:
            manifest = json.load(fh)
    out = []
    for name in sorted(os.listdir(OUT_DIR)) if os.path.exists(OUT_DIR) else []:
        key = name[:-4]
        if name.endswith('.png') and key not in manifest:
            out.append(key)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--cut', action='store_true')
    ap.add_argument('--sheets', action='store_true')
    ap.add_argument('--worklist', action='store_true')
    ap.add_argument('--catalogue')
    args = ap.parse_args()
    if args.cut or args.sheets:
        made = cut()
        print(f'{len(made)} question crop(s) written to {OUT_DIR}')
        by = collections.Counter((r[2], r[3]) for r in made)
        for k in sorted(by):
            if by[k] != 12:
                print(f'  {k}: {by[k]} crops, expected 12')
        if args.sheets:
            print(f'{sheets(made)} contact sheet(s) in {SHEET_DIR}')
    if args.worklist:
        for key in worklist():
            print(key)
    if args.catalogue:
        return 1 if catalogue(args.catalogue) else 0
    return 0


if __name__ == '__main__':
    sys.exit(main())
