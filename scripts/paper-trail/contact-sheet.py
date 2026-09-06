#!/usr/bin/env python3
"""
Paper Trail — Phase 5 QA contact sheet.

Renders, for every committed answer sidecar, each question's PAPER anchor strip
beside the SCHEME region it maps to — so a human can confirm at a glance that
"Question N on the paper" lines up with "QN's solution in the scheme" (and that
Paper 1 never pulls Paper 2's region). Output: out/contact-sheet.pdf.

This is the human gate before a grammar profile's `answers` flag ships. Run
after anchor-map.py.
"""

import argparse
import json
import os
import fitz
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
ANSWERS_DIR = os.path.join(HERE, "answers")
CORPUS = os.path.join(REPO, "paper-trail-corpus")
OUT = os.path.join(HERE, "out", "contact-sheet.pdf")

DPI = 130
COL_W = 720           # px width of each rendered strip
PAPER_BAND = 0.085    # fraction of paper page height to show below the anchor
SCHEME_BAND = 0.16    # fraction of scheme page height to show from the region top
PAD = 14
LABEL_H = 26

try:
    FONT = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 18)
    SMALL = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 15)
except Exception:
    FONT = SMALL = ImageFont.load_default()


def render_strip(page, y0_frac, band_frac):
    """Render `page` at DPI, return a PIL crop [y0_frac, y0_frac+band] full width."""
    pix = page.get_pixmap(dpi=DPI)
    img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    H = pix.height
    top = max(0, int(y0_frac * H))
    bot = min(H, int((y0_frac + band_frac) * H))
    crop = img.crop((0, top, pix.width, bot))
    # scale to COL_W
    w, h = crop.size
    return crop.resize((COL_W, max(1, int(h * COL_W / w))))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prefix", default="", help="paper file-name prefix")
    parser.add_argument("--files", default="", help="comma-separated exact paper file names")
    parser.add_argument("--label", default="", help="only cards whose display label contains this text")
    parser.add_argument("--years", default="", help="comma-separated exam years to include")
    parser.add_argument("--out", default=OUT)
    args = parser.parse_args()
    selected_years = {int(value) for value in args.years.split(",") if value.strip()}
    selected_files = {value.strip() for value in args.files.split(",") if value.strip()}
    sidecars = []
    for year in sorted(os.listdir(ANSWERS_DIR)):
        ydir = os.path.join(ANSWERS_DIR, year)
        if not os.path.isdir(ydir):
            continue
        if selected_years and int(year) not in selected_years:
            continue
        for f in sorted(os.listdir(ydir)):
            paper_file = f[:-5] if f.endswith(".json") else ""
            if (f.endswith(".json")
                    and (not args.prefix or f.startswith(args.prefix))
                    and (not selected_files or paper_file in selected_files)):
                sidecars.append((int(year), json.load(open(os.path.join(ydir, f)))))
    sidecars.sort(key=lambda x: (x[0], x[1]["component"]))

    pages = []
    for year, sc in sidecars:
        comp = sc["component"]
        component_label = comp[0] if comp else "single"
        paper = fitz.open(os.path.join(CORPUS, "exampapers", str(year), sc["paperFileid"]))
        scheme = fitz.open(os.path.join(CORPUS, "markingschemes", str(year), sc["schemeFileid"]))
        rows = []
        selected_questions = [q for q in sc["q"] if (
            not args.label or args.label.lower() in q.get("label", "").lower()
        )]
        if not selected_questions:
            paper.close()
            scheme.close()
            continue
        for q in selected_questions:
            p_strip = render_strip(paper[q["pP"] - 1], q["pY"][0], PAPER_BAND)
            displayed_region = q.get("schemeRegion") or q["region"]
            seg0 = displayed_region[0]
            s_y = seg0.get("r", [0, 0, 1, 1])[1]
            s_strip = render_strip(scheme[seg0["p"] - 1], s_y, SCHEME_BAND)
            label = (f"Paper Q{q['n']} (p{q['pP']})   →   Scheme p{seg0['p']}"
                     f"   ·   {'corrected crop' if q.get('schemeRegion') else q['mode']}")
            rows.append((label, p_strip, s_strip))

        # compose one tall page image for this paper
        row_hs = [LABEL_H + r[1].height + r[2].height + PAD for r in rows]
        page_h = LABEL_H + 14 + sum(row_hs) + PAD
        page_w = COL_W + 2 * PAD
        canvas = Image.new("RGB", (page_w, page_h), "white")
        d = ImageDraw.Draw(canvas)
        d.text((PAD, 8), f"{year}  ·  {sc['paperFileid']}  ·  Paper {component_label}  ·  band {sc['band']}",
               fill="black", font=FONT)
        y = LABEL_H + 14
        for label, ps, ss in rows:
            d.rectangle([PAD, y, PAD + COL_W, y + LABEL_H - 4], fill="#FDEEDF")
            d.text((PAD + 6, y + 3), label, fill="#B54D14", font=SMALL)
            y += LABEL_H
            canvas.paste(ps, (PAD, y)); y += ps.height
            canvas.paste(ss, (PAD, y)); y += ss.height + PAD
        pages.append(canvas)
        paper.close()
        scheme.close()

    if pages:
        pages[0].save(args.out, save_all=True, append_images=pages[1:], resolution=150)
        print(f"wrote {args.out} ({len(pages)} paper sheets)")
    else:
        print("no sidecars found")


if __name__ == "__main__":
    main()
