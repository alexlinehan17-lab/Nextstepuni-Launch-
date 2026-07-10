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


def _cluster_count(rects, pad=12):
    """Union-find cluster rects by proximity; return (union_rect, member_count)
    per cluster. A dense cluster of many small paths is a line diagram."""
    n = len(rects)
    parent = list(range(n))

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    def union(i, j):
        parent[find(i)] = find(j)

    for i in range(n):
        for j in range(i + 1, n):
            if _overlaps(rects[i], rects[j], pad=pad):
                union(i, j)
    groups = {}
    for i in range(n):
        groups.setdefault(find(i), []).append(rects[i])
    out_rects, out_counts = [], []
    for members in groups.values():
        u = fitz.Rect(members[0])
        for r in members[1:]:
            u |= r
        out_rects.append(u)
        out_counts.append(len(members))
    return out_rects, out_counts


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
            if w > pr.width * 0.9 and h > pr.height * 0.9:
                continue                       # full-page scan / cover image
            if h / max(w, 1) > 8 or w / max(h, 1) > 10:
                continue                       # extreme sliver
            rects.append(r)
        # ── vector-drawing clusters (circuits, apparatus, ray/geometry
        #    diagrams, graphs, maps) ── these are drawn as MANY small line/curve
        #    paths, not a few big rects, so cluster ALL paths by proximity and
        #    keep dense clusters. Hairlines and full-width table rules dropped.
        paths = []
        for d in page.get_drawings():
            r = fitz.Rect(d['rect'])
            if r.width < 2 and r.height < 2:
                continue                                  # dot / hairline
            if r.width > pr.width * 0.8 and r.height < 3:
                continue                                  # full-width rule (table)
            if r.width > pr.width * 0.92 and r.height > pr.height * 0.92:
                continue                                  # page border
            paths.append(r)
        vrects = []
        if len(paths) >= 10:
            clusters, counts = _cluster_count(paths, pad=12)
            for r, n in zip(clusters, counts):
                if n < 10:
                    continue                              # too few strokes to be a diagram
                if r.width * r.height < max(min_area * 2, 18000):
                    continue
                if r.width < 90 or r.height < 70:
                    continue
                if r.width > pr.width * 0.95 and r.height > pr.height * 0.9:
                    continue                              # whole-page cluster
                vrects.append(r)

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
