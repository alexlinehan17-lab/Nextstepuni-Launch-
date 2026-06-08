#!/usr/bin/env python3
"""
extract_exam_figure.py — pull a figure (diagram, map, comprehension passage)
out of an SEC exam paper PDF and save it as a PNG asset for the app.

Used by the Catch-Up Lane / Command-Word content pipeline so a genuinely visual
question can SHOW the real figure instead of describing it. SEC material is used
under NextStepUni's agreement with the State Examinations Commission; every asset
must carry an SEC attribution in the card's `figure.source`.

Requires PyMuPDF (fitz), already in the project env.

Usage:
  # 1. See the page so you can choose a crop box (renders the whole page):
  python3 tools/extract_exam_figure.py page <pdf> <page1based> <out.png> [dpi]

  # 2. List embedded raster images on a page (clean auto-crop for photo/diagram figures):
  python3 tools/extract_exam_figure.py list <pdf> <page1based>

  # 3. Crop a region (coords are FRACTIONS of the page: x0 y0 x1 y1, each 0..1):
  python3 tools/extract_exam_figure.py crop <pdf> <page1based> <x0> <y0> <x1> <y1> <out.png> [dpi]
"""
import sys, os
import fitz  # PyMuPDF


def _open(pdf, page1):
    doc = fitz.open(pdf)
    page = doc[page1 - 1]
    return doc, page


def render_page(pdf, page1, out, dpi=150):
    _, page = _open(pdf, page1)
    page.get_pixmap(dpi=int(dpi)).save(out)
    print(f"rendered page {page1} -> {out} ({os.path.getsize(out)} bytes)")


def list_images(pdf, page1):
    doc, page = _open(pdf, page1)
    imgs = page.get_images(full=True)
    print(f"page {page1}: {len(imgs)} embedded image(s)")
    for idx, info in enumerate(imgs):
        xref = info[0]
        rects = page.get_image_rects(xref)
        bbox = rects[0] if rects else None
        print(f"  [{idx}] xref={xref} {info[2]}x{info[3]}px bbox={bbox}")


def crop(pdf, page1, x0, y0, x1, y1, out, dpi=200):
    _, page = _open(pdf, page1)
    r = page.rect  # page size in points
    clip = fitz.Rect(r.x0 + float(x0) * r.width, r.y0 + float(y0) * r.height,
                     r.x0 + float(x1) * r.width, r.y0 + float(y1) * r.height)
    os.makedirs(os.path.dirname(out) or '.', exist_ok=True)
    page.get_pixmap(clip=clip, dpi=int(dpi)).save(out)
    print(f"cropped page {page1} {clip} -> {out} ({os.path.getsize(out)} bytes)")


if __name__ == '__main__':
    a = sys.argv[1:]
    if not a:
        print(__doc__); sys.exit(1)
    mode = a[0]
    if mode == 'page':
        render_page(a[1], int(a[2]), a[3], *(a[4:5] or []))
    elif mode == 'list':
        list_images(a[1], int(a[2]))
    elif mode == 'crop':
        crop(a[1], int(a[2]), a[3], a[4], a[5], a[6], a[7], *(a[8:9] or []))
    else:
        print(f"unknown mode: {mode}\n{__doc__}"); sys.exit(1)
