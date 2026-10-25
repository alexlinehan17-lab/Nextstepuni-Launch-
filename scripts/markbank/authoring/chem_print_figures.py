#!/usr/bin/env python3
"""Crop the figures the printed-layout Chemistry papers (2026 on) hand their parts.

    python3 scripts/markbank/authoring/chem_print_figures.py 2026 hl          # crop
    python3 scripts/markbank/authoring/chem_print_figures.py 2026 hl --check  # verify

Each crop is a rectangle on one page of the paper (a diagram, a data table, a
reaction scheme) or of the marking scheme (a worked answer the text layer
cannot carry, such as a stacked fraction). The rectangles were measured from
the PDFs' own image and drawing boxes and every crop was opened and looked at
before its catalogue entry was written. The catalogue in
scripts/markbank/authored/chemistry-print-figures-catalogue.json holds the alt
text; bind-figures.mjs publishes what this writes.

A crop is named for its question, not its page index:
chemistry-2026-HL-paper-q8.png, chemistry-2026-HL-scheme-q7b-iv.png. The
"-scheme-" crops are marked `solution: true` in the catalogue, which the session
holds back until the student has committed to an answer.

--check re-renders every crop in memory and compares it to the published copy
in public/exam-figures/chemistry/markbank, so a changed rectangle or renderer
cannot slip a different picture under a published name.
"""
import argparse
import hashlib
import json
import os
import re
import sys

import fitz

DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(DIR)))
PAPERS = os.path.join(ROOT, 'examiner-reports', 'chemistry', 'papers')
SCHEMES = os.path.join(ROOT, 'examiner-reports', 'chemistry', 'schemes')
DPI = 150
PANEL_GAP = 14

# (name suffix, source, page, (x0, y0, x1, y1) in PDF points). A source of
# 'labels' marks a picture's region whose printed words are its labels (see
# chem_print.Printed._outside_figures) and is not itself published. A source of
# 'paper-image' takes the raster the paper embeds at that rectangle as it is,
# for a picture whose page text runs across it. 2026 HL Q4(i)'s raster was cut
# from a page and carries the tails of two neighbouring lines ("e", "ound") at
# its left edge; MASKS whites out exactly those pixel boxes, which were found
# by scanning the raster for dark pixels clear of the structure's own bonds.
CROPS = {
    (2026, 'hl'): [
        ('paper-q2a', 'paper', 3, (378, 50, 544, 192)),
        ('paper-q4i', 'paper-image', 5, (448, 352, 539, 477)),
        ('paper-q6b', 'paper', 7, (125, 226, 420, 292)),
        ('paper-q8', 'paper', 9, (130, 78, 466, 196)),
        ('paper-q9a', 'paper', 10, (80, 156, 545, 234)),
        ('paper-q9c', 'paper', 10, (460, 526, 546, 660)),
        ('paper-q11a', 'paper', 12, (165, 96, 412, 146)),
        ('paper-q11c', 'paper', 12, (128, 507, 467, 566)),
        ('paper-q11d-b', 'paper', 13, (135, 438, 490, 550)),
        ('scheme-q4c', 'scheme', 9, (50, 197.6, 200, 214)),
        ('scheme-q4k', 'scheme', 9, (50, 603, 200, 640)),
        ('scheme-q5b-iii', 'scheme', 10, (100, 468, 420, 540)),
        ('scheme-q6b-iv', 'scheme', 11, (60, 401, 420, 470)),
        ('scheme-q8b-i', 'scheme', 13, (100, 300, 470, 372)),
        ('scheme-q11a-iv', 'scheme', 17, (100, 224, 330, 292)),
        ('scheme-q11a-v', 'scheme', 17, (100, 351, 330, 404)),
        ('scheme-q7b-iv', 'scheme', 12, (100, 375, 560, 414)),
        ('scheme-q7b-v', 'scheme', 12, (100, 450, 560, 534)),
    ],
    (2026, 'ol'): [
        ('paper-q1', 'paper', 2, (110, 150, 485, 275)),
        ('paper-q2', 'paper', 3, (495, 52, 545, 270)),
        ('paper-q2c', 'paper', 3, (52, 365, 545, 428)),
        ('paper-q3', 'paper', 4, (52, 259, 545, 326)),
        ('paper-q6', 'paper', 7, (205, 92, 390, 235)),
        ('paper-q8', 'paper', 9, (65, 75, 530, 140)),
        ('paper-q9c', 'paper', 10, (280, 490, 372, 532)),
        ('paper-q10b', 'paper-image', 11, (468, 320, 540, 421)),
        ('paper-q11c', 'paper', 12, (52, 412, 545, 700)),
        # Q8(a)(iii)/(iv): the question's print -- its opening line and the
        # reaction series that says what Z is -- above the one ask, as the
        # card's question picture; the scheme's drawing is its answer.
        ('paper-q8a-iii', 'paper-panels', 9, ((24, 55, 545, 143), (80, 190, 545, 208))),
        ('paper-q8a-iv', 'paper-panels', 9, ((24, 55, 545, 143), (80, 211, 545, 229))),
        ('scheme-q8a-iii', 'scheme', 13, (82, 226.5, 165, 299)),
        ('scheme-q8a-iv', 'scheme', 13, (82, 314.5, 165, 391)),
        ('scheme-q1c-ii', 'scheme', 6, (108, 507, 275, 588)),
        ('scheme-q2c-ii', 'scheme', 7, (105, 531, 560, 614)),
        ('scheme-q4j', 'scheme', 9, (80, 446, 248, 489)),
        ('scheme-q5a-iv', 'scheme', 10, (108, 322, 228, 424)),
        ('scheme-q6c-i', 'scheme', 11, (110, 378.5, 260, 401)),
        ('scheme-q6d-ii', 'scheme', 11, (109, 531.5, 320, 609)),
        ('scheme-q9a-ii', 'scheme', 14, (108, 178.5, 330, 217)),
    ],
    # 2025 Higher: corrected in place by chem_audit_2025_hl.py. Its paper
    # crops also say which printed words are a picture's labels rather than
    # the question's (Printed(..., figures=True)).
    (2025, 'hl'): [
        ('paper-q2', 'paper', 3, (80, 90, 520, 342)),
        ('paper-q3', 'paper', 4, (88, 227, 508, 291)),
        ('paper-q4l-b', 'paper', 5, (336, 556, 545, 675)),
        ('paper-q5b', 'paper', 6, (298, 228, 545, 568)),
        ('paper-q7d-eq', 'paper', 8, (215, 372, 380, 410)),
        # Q7(d)(ii) is shown the indicator's equation and the pH curve, the
        # two things its lead-in points at, stacked; the curve's own rectangle
        # is listed as 'labels' so its axis numbers stay out of the lead-in.
        ('q7d-curve', 'labels', 8, (300, 458, 545, 702)),
        ('paper-q7d-ii', 'paper-panels', 8, ((215, 372, 380, 410), (300, 458, 545, 702))),
        ('paper-q8', 'paper', 9, (110, 76, 484, 200)),
        ('paper-q11c-eq', 'paper', 13, (255, 471, 372, 496)),
        ('paper-q11d-b', 'paper', 14, (384, 380, 545, 603)),
        ('scheme-q2c-ii', 'scheme', 7, (105, 511.5, 200, 614)),
        ('scheme-q4g', 'scheme', 10, (80, 351.5, 320, 403.5)),
        ('scheme-q5b-ii', 'scheme', 11, (105, 365, 145, 396)),
        ('scheme-q8c-i', 'scheme', 14, (105, 365.5, 200, 408)),
        ('scheme-q8c-ii', 'scheme', 14, (105, 421, 200, 467)),
        ('scheme-q8c-iii', 'scheme', 14, (105, 494.5, 205, 551)),
        ('scheme-q9b-iii', 'scheme', 15, (105, 314, 165, 340)),
        ('scheme-q9b-iv', 'scheme', 15, (105, 412, 290, 438)),
        ('scheme-q10a-ii', 'scheme', 16, (105, 121.5, 210, 179)),
        ('scheme-q10a-iv', 'scheme', 16, (105, 254, 175, 336)),
        ('scheme-q10b-i', 'scheme', 16, (105, 449.5, 170, 496)),
        ('scheme-q10b-iv', 'scheme', 16, (105, 618.5, 210, 669)),
    ],
    # 2025 Ordinary: corrected in place by chem_audit_2025_ol.py. Q8's reaction
    # scheme keeps its published crop (chemistry-2025-OL-paper-q8-fig0); its
    # rectangle is listed here only so its labels stay out of the text.
    (2025, 'ol'): [
        ('paper-q1', 'paper', 2, (70, 244, 525, 478)),
        ('paper-q1e', 'paper', 2, (388, 648, 545, 742)),
        ('paper-q2', 'paper', 3, (440, 88, 545, 345)),
        ('q3-flasks', 'labels', 4, (186, 142, 410, 316)),
        ('q3-table', 'labels', 4, (52, 428, 543, 491)),
        ('paper-q3', 'paper-panels', 4, ((186, 142, 410, 316), (52, 428, 543, 491))),
        ('paper-q6c', 'paper', 7, (405, 270, 545, 450)),
        ('q7b-photo', 'labels', 8, (190, 150, 392, 320)),
        ('q7c-bottle', 'labels', 8, (444, 498, 543, 658)),
        ('q8-scheme', 'labels', 9, (92, 82, 510, 256)),
        ('paper-q9c', 'paper', 10, (424, 303, 544, 478)),
        ('paper-q10a', 'paper', 11, (76, 102, 516, 216)),
        ('paper-q11a', 'paper', 12, (88, 137, 540, 172)),
        ('q11b-table', 'labels', 12, (80, 430, 544, 522)),
        # Q11(b)(vi) is answered with a drawing, so the card's figure is the
        # scheme's; the table the asks read from travels with the question's
        # own print, which is the card's question picture.
        ('paper-q11b-print', 'paper-panels', 12, ((52, 404, 545, 670),)),
        ('paper-q11d-a', 'paper', 14, (86, 105, 508, 296)),
        ('scheme-q2d', 'scheme', 7, (80, 641.5, 545, 713.5)),
        ('scheme-q6b-iii', 'scheme', 11, (105, 248, 210, 321)),
        ('scheme-q8a-ii', 'scheme', 13, (105, 298.5, 240, 377)),
        ('scheme-q11b-vi', 'scheme', 17, (105, 701.5, 390, 744)),
        ('scheme-q11c-ii', 'scheme', 18, (105, 186, 180, 216)),
    ],
}



def _load_sitting_crops():
    """Each sitting carded after 2025 keeps its rectangles in a file of its own,
    chemistry/crops/<year>-<lvl>.json: a list of [suffix, source, page, rect],
    where rect is [x0, y0, x1, y1], or a list of those for 'paper-panels'."""
    folder = os.path.join(DIR, 'chemistry', 'crops')
    if not os.path.isdir(folder):
        return
    for name in sorted(os.listdir(folder)):
        m = re.match(r'^(\d{4})-(hl|ol)\.json$', name)
        if not m:
            continue
        key = (int(m.group(1)), m.group(2))
        if key in CROPS:
            raise SystemExit(f'{name}: {key} is already in CROPS')
        rows = json.load(open(os.path.join(folder, name)))
        CROPS[key] = [(suf, src, page, tuple(tuple(r) for r in rect) if src.endswith('-panels')
                       else tuple(rect)) for suf, src, page, rect in rows]


_load_sitting_crops()


MASKS = {
    'chemistry-2026-HL-paper-q4i.png': [(0, 350, 20, 386), (0, 489, 92, 515)],
    # 2021 HL scheme Q8(b): (i)'s drawing of propanone, on the right, prints
    # level with the top of (ii)'s drawing on the left, so each crop whites out
    # the other part's corner (pixel boxes at DPI, from the page's drawing boxes).
    'chemistry-2021-HL-scheme-q8b-i.png': [(62, 93, 448, 146)],
    'chemistry-2021-HL-scheme-q8b-ii.png': [(614, 0, 823, 50)],
    # 2021 OL Q10(b): the cell's diagram sits beside the ends of three lines of
    # the question ("electrolysed", "transfer.", "electrodes.", "place?"), whited out here; the
    # crop is a one-panel print so that those words stay in the question text.
    'chemistry-2021-OL-paper-q10b.png': [(0, 10, 11, 45), (0, 204, 49, 369)],
    # 2020 HL scheme Q8(d)(i): its drawing of X stands beside (d)(ii)'s answer
    # and cell, whited out here.
    'chemistry-2020-HL-scheme-q8d-i.png': [(0, 115, 729, 203), (937, 131, 1041, 183)],
    # 2020 OL Q1(a): the test tube stands beside the end of "through", the question's mark "(17)" and
    # the words "distinctive flame." of (b)'s lead-in.
    'chemistry-2020-OL-paper-q1a.png': [(0, 249, 28, 278), (104, 323, 149, 351), (0, 385, 132, 413)],
    # 2019 OL Q6(e): the print of (e) starts at the top of its apparatus, level with the foot of
    # (d)(ii)'s line "(ii) is carcinogenic? (9)", and holds (e)'s mark "(9)"; both whited out.
    'chemistry-2019-OL-paper-q6e-print.png': [(60, 0, 668, 23), (630, 191, 669, 218)],
    # 2019 OL Q7: the flask on its balance stands beside the ends of three lines of the question
    # ("took place", "(CaCO3)", "eggshell"), whited out here.
    'chemistry-2019-OL-paper-q7.png': [(0, 46, 33, 75), (0, 76, 33, 106), (0, 192, 22, 223)],
    # 2021 OL Q3(d): the last letter of "provided" prints at the pictogram's corner.
    'chemistry-2021-OL-paper-q3d.png': [(0, 0, 15, 31)],
    # 2019 HL Q9: the graph (second panel) stands beside the ends of the marks "(6)" of (a) and of
    # (b) and the full stop of "catalysis." in (c); their glyphs fall in the panel's first five
    # pixel columns, clear of the axis title, which starts at column 11.
    'chemistry-2019-HL-paper-q9.png': [(0, 305, 8, 330), (0, 470, 8, 495), (0, 520, 4, 528)],
    # 2018 OL Q2(f) and Q10(a): the part's mark, "(12)" and "(25)", prints at the end of its last
    # line, under the right end of the line above; whited out (dark pixels at 903-938 x 434-454 and
    # 903-939 x 338-358).
    'chemistry-2018-OL-paper-q2f-print.png': [(898, 428, 946, 460)],
    'chemistry-2018-OL-paper-q10a-print.png': [(898, 332, 946, 364)],
    # 2018 HL Q9(d): the part's mark "(15)" prints at the end of its last line, under the end of
    # the line above ("temperature", dark to x 912, y 280-299); whited out (dark pixels at 917-931
    # x 310-332, the panel's right edge cutting the mark after "(1").
    'chemistry-2018-HL-paper-q9d-print.png': [(914, 304, 932, 337)],
}


def out_dir(year, lvl):
    # bind-figures.mjs resolves a crop as exam-papers/<subject>/figures/<year>-<level>/.
    return os.path.join(ROOT, 'exam-papers', 'chemistry', 'figures', f'{year}-{lvl}')


suffix_of = {(src, pg, rect): suf for crops in CROPS.values() for suf, src, pg, rect in crops}


def render(year, lvl, source, page, rect):
    path = os.path.join(PAPERS, f'{year}-{lvl}-paper.pdf') if source.startswith('paper') \
        else os.path.join(SCHEMES, f'{year}-{lvl}.pdf')
    doc = fitz.open(path)
    pg = doc[page - 1]
    if source in ('paper-panels', 'scheme-panels'):
        # Several regions of one page stacked into one picture, the way the
        # page prints them top to bottom: the question's setup and diagram,
        # then the one ask the card is for, without the sibling asks between.
        import io
        from PIL import Image
        # A region given as five numbers names its own page first: a scheme's
        # working that runs over a page break (2022 HL Q7(b)(ii)).
        ims = [Image.open(io.BytesIO(
            (doc[int(r[0]) - 1] if len(r) == 5 else pg).get_pixmap(
                dpi=DPI, clip=fitz.Rect(*(r[1:] if len(r) == 5 else r))).tobytes('png')))
               for r in rect]
        out = Image.new('RGB', (max(i.width for i in ims), sum(i.height for i in ims)
                                + PANEL_GAP * (len(ims) - 1)), 'white')
        y = 0
        for im in ims:
            out.paste(im.convert('RGB'), (0, y))
            y += im.height + PANEL_GAP
        from PIL import ImageDraw
        for box in MASKS.get(name(year, lvl, suffix_of[(source, page, rect)]), []):
            ImageDraw.Draw(out).rectangle((box[0], box[1], box[2] - 1, box[3] - 1), fill='white')
        buf = io.BytesIO()
        out.save(buf, format='PNG')
        return buf.getvalue()
    if source == 'paper-image':
        want = fitz.Rect(*rect)
        hits = [img[0] for img in pg.get_images(full=True)
                if any(want.contains(r) for r in pg.get_image_rects(img[0]))]
        if len(hits) != 1:
            raise SystemExit(f'p{page}: {len(hits)} images inside {rect}')
        pix = fitz.Pixmap(doc, hits[0])
        for box in MASKS.get(name(year, lvl, suffix_of[(source, page, rect)]), []):
            pix.set_rect(fitz.IRect(*box), (255,) * pix.n)
        return pix.tobytes('png')
    pix = pg.get_pixmap(dpi=DPI, clip=fitz.Rect(*rect))
    for box in MASKS.get(name(year, lvl, suffix_of[(source, page, rect)]), []):
        # A clipped pixmap keeps the page's pixel origin: boxes are crop-relative.
        x0, y0, x1, y1 = box
        pix.set_rect(fitz.IRect(x0 + pix.x, y0 + pix.y, x1 + pix.x, y1 + pix.y), (255,) * pix.n)
    return pix.tobytes('png')


def name(year, lvl, suffix):
    return f'chemistry-{year}-{lvl.upper()}-{suffix}.png'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('year', type=int)
    ap.add_argument('lvl', choices=['hl', 'ol'])
    ap.add_argument('--check', action='store_true')
    args = ap.parse_args()
    crops = CROPS.get((args.year, args.lvl), [])
    od = out_dir(args.year, args.lvl)
    os.makedirs(od, exist_ok=True)
    bad = 0
    for suffix, source, page, rect in crops:
        if source in ('labels', 'scheme-labels'):
            continue                 # a region read as a picture's, never published alone
        png = render(args.year, args.lvl, source, page, rect)
        dest = os.path.join(od, name(args.year, args.lvl, suffix))
        if args.check:
            # The committed copy is the one bind-figures.mjs published.
            dest = os.path.join(ROOT, 'public', 'exam-figures', 'chemistry', 'markbank',
                                name(args.year, args.lvl, suffix))
            ok = os.path.exists(dest) and open(dest, 'rb').read() == png
            bad += not ok
            print(('ok   ' if ok else 'DIFF ') + os.path.basename(dest))
        else:
            with open(dest, 'wb') as f:
                f.write(png)
            print(os.path.basename(dest), hashlib.md5(png).hexdigest())
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
