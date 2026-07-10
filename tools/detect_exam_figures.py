#!/usr/bin/env python3
"""
detect_exam_figures.py — find candidate figure regions in an SEC exam paper PDF
so the Diagram Vault extraction pipeline can crop + (agent-)verify each one.

Emits JSON: a list of candidates, each { page (1-based), x0,y0,x1,y1 (page
fractions), kind ('raster'|'vector'), w, h (points), near (nearby text snippet
to help identify the question) }. Noise is filtered (SEC header rules, page
banners, hairlines, tiny marks); tables and decorative rules may still slip
through — the human/agent verify step is the final gate, never this script.

Usage:
  python3 tools/detect_exam_figures.py <pdf> [--min-area PTS2] [--json out.json]
"""
import sys, json
import fitz  # PyMuPDF


def _rect_frac(r, page):
    pr = page.rect
    return [round((r.x0 - pr.x0) / pr.width, 4), round((r.y0 - pr.y0) / pr.height, 4),
            round((r.x1 - pr.x0) / pr.width, 4), round((r.y1 - pr.y0) / pr.height, 4)]


def _overlaps(a, b, pad=3):
    return not (a.x1 + pad < b.x0 or b.x1 + pad < a.x0 or a.y1 + pad < b.y0 or b.y1 + pad < a.y0)


def _merge(rects):
    """Union overlapping/adjacent rects (a diagram split into image tiles)."""
    out = []
    for r in sorted(rects, key=lambda r: (r.y0, r.x0)):
        placed = False
        for i, o in enumerate(out):
            if _overlaps(r, o, pad=6):
                out[i] = o | r  # union
                placed = True
                break
        if not placed:
            out.append(fitz.Rect(r))
    # second pass to catch chains
    changed = True
    while changed:
        changed = False
        for i in range(len(out)):
            for j in range(i + 1, len(out)):
                if _overlaps(out[i], out[j], pad=6):
                    out[i] = out[i] | out[j]
                    del out[j]
                    changed = True
                    break
            if changed:
                break
    return out


def detect(pdf, min_area=11000):
    doc = fitz.open(pdf)
    cands = []
    for pi in range(doc.page_count):
        page = doc[pi]
        pr = page.rect
        rects = []
        # ── raster images ──
        for info in page.get_image_info():
            b = info['bbox']
            r = fitz.Rect(b)
            w, h = r.width, r.height
            if w < 85 or h < 60:
                continue                       # hairline rule / tiny mark
            if w * h < min_area:
                continue
            if w / pr.width > 0.85 and h < 45:
                continue                       # full-width header banner
            if h / max(w, 1) > 8 or w / max(h, 1) > 10:
                continue                       # extreme sliver
            rects.append(r)
        # ── vector-drawing clusters (graphs, geometry, maps, apparatus) ──
        big = [fitz.Rect(d['rect']) for d in page.get_drawings()
               if fitz.Rect(d['rect']).width * fitz.Rect(d['rect']).height > 2500
               and fitz.Rect(d['rect']).width > 40 and fitz.Rect(d['rect']).height > 40]
        vclusters = _merge(big) if len(big) >= 6 else []
        vrects = [r for r in vclusters if r.width * r.height >= max(min_area * 2, 20000)
                  and r.width > 110 and r.height > 90]

        for kind, group in (('raster', _merge(rects)), ('vector', vrects)):
            for r in group:
                if r.width * r.height < min_area:
                    continue
                # nearest text above the region — helps name the question.
                near = ''
                try:
                    band = fitz.Rect(pr.x0, max(pr.y0, r.y0 - 46), pr.x1, r.y0 + 6)
                    near = ' '.join(page.get_textbox(band).split())[:90]
                except Exception:
                    pass
                cands.append({
                    'page': pi + 1, 'kind': kind,
                    'x0': _rect_frac(r, page)[0], 'y0': _rect_frac(r, page)[1],
                    'x1': _rect_frac(r, page)[2], 'y1': _rect_frac(r, page)[3],
                    'w': round(r.width), 'h': round(r.height), 'near': near,
                })
    return cands


if __name__ == '__main__':
    args = sys.argv[1:]
    if not args:
        print(__doc__); sys.exit(1)
    pdf = args[0]
    min_area = 11000
    out = None
    if '--min-area' in args:
        min_area = float(args[args.index('--min-area') + 1])
    if '--json' in args:
        out = args[args.index('--json') + 1]
    result = detect(pdf, min_area)
    text = json.dumps(result, indent=1)
    if out:
        with open(out, 'w') as f:
            f.write(text)
        print(f"{len(result)} candidate(s) -> {out}")
    else:
        print(text)
