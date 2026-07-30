#!/usr/bin/env python3
"""Render each crop region from a sidecar to PNG for visual verification."""
import json, os, sys
import fitz

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
CORPUS = os.path.join(REPO, "paper-trail-corpus")
LIG = {"Ɵ": "ti", "Ʃ": "tt", "ϐ": "fi", "ﬀ": "ff", "ﬁ": "fi", "ﬂ": "fl"}

def delig(s):
    for k, v in LIG.items():
        s = s.replace(k, v)
    return s

year = sys.argv[1]
outdir = sys.argv[2] if len(sys.argv) > 2 else "/tmp/slcrops"
os.makedirs(outdir, exist_ok=True)
sc = json.load(open(os.path.join(HERE, "answers", str(year), "LB816CLP000EV.pdf.json")))
sd = fitz.open(os.path.join(CORPUS, "markingschemes", str(year), sc["schemeFileid"]))
for q in sc["q"]:
    for reg in q["region"]:
        p = reg["p"] - 1
        page = sd[p]
        W, H = page.rect.width, page.rect.height
        x0, y0, x1, y1 = reg["r"]
        rect = fitz.Rect(x0 * W, y0 * H, x1 * W, y1 * H)
        pix = page.get_pixmap(clip=rect, matrix=fitz.Matrix(2, 2))
        fn = os.path.join(outdir, f"{year}_q{q['n']}_p{reg['p']}.png")
        pix.save(fn)
        txt = delig(page.get_text("text", clip=rect))
        oneline = " ".join(l.strip() for l in txt.splitlines() if l.strip())
        print(f"Q{q['n']} -> {fn}")
        print(f"     TEXT: {oneline[:300]}")
