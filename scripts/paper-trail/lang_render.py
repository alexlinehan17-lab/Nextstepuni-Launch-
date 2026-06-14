#!/usr/bin/env python3
"""Render every crop of a (staged) language reading sidecar to PNGs for review.

Usage: python3 lang_render.py <sidecar.json>
Writes /tmp/lr/<paperFileid>/<n>_<label>.png and prints each crop's text.
"""
import json, os, sys, re
import fitz

HERE = os.path.dirname(os.path.abspath(__file__))
CORPUS = os.path.join(os.path.dirname(os.path.dirname(HERE)), "paper-trail-corpus")


def main():
    sc = json.load(open(sys.argv[1]))
    # find year from path: .../<year>/<file>.json, else scan corpus
    year = None
    m = re.search(r"/(\d{4})/", os.path.abspath(sys.argv[1]))
    if m:
        year = m.group(1)
    sp = None
    if year:
        cand = os.path.join(CORPUS, "markingschemes", year, sc["schemeFileid"])
        if os.path.exists(cand):
            sp = cand
    if sp is None:
        for yd in os.listdir(os.path.join(CORPUS, "markingschemes")):
            cand = os.path.join(CORPUS, "markingschemes", yd, sc["schemeFileid"])
            if os.path.exists(cand):
                sp = cand
                break
    sd = fitz.open(sp)
    out = os.path.join("/tmp/lr", sc["paperFileid"])
    os.makedirs(out, exist_ok=True)
    for q in sc["q"]:
        seg = q["region"][0]
        pg = sd[seg["p"] - 1]
        H, W = pg.rect.height, pg.rect.width
        r = seg.get("r", [0, 0, 1, 1])
        clip = fitz.Rect(0, r[1] * H, W, min(1.0, r[3]) * H)
        safe = re.sub(r"[^A-Za-z0-9]+", "_", q.get("label", q["n"]))[:30]
        png = os.path.join(out, f"{int(q['n']):02d}_{safe}.png")
        pg.get_pixmap(matrix=fitz.Matrix(1.4, 1.4), clip=clip).save(png)
        txt = " ".join(pg.get_text("text", clip=clip).split())[:90]
        print(f"n{q['n']} [{q.get('label','')}] segs={len(q['region'])} -> {png}")
        print(f"     {txt}")
    print(f"\nRendered {len(sc['q'])} crops to {out}/")


if __name__ == "__main__":
    main()
