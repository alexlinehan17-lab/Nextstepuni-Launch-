#!/usr/bin/env python3
"""Render + text evidence for a STAGED answer sidecar so a verifier can judge by
eye whether each crop shows the marking-scheme ANSWER to the paper's question
(not a reading passage, a question restatement, a blank, or the wrong paper).

Renders the first-region crop of the first / middle / last question to PNG and
prints, for those questions, the paper stem text + the crop text.

Usage: python3 pt_stage_evidence.py <year>/<paperFileid>   # e.g. 2014/LC014ALP000EV
Outputs PNGs under /tmp/ptstage/ and prints their paths + the text evidence.
"""
import json, os, sys
import fitz
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
CORPUS = os.path.join(REPO, "paper-trail-corpus")
STAGE = os.path.join(HERE, "answers_staging")
OUT = "/tmp/ptstage"
LIG = {"Ɵ": "ti", "Ʃ": "tt", "ϐ": "fi", "ﬀ": "ff", "ﬁ": "fi", "ﬂ": "fl",
       "ﬃ": "ffi", "ﬄ": "ffl", "ﬅ": "ft", "ﬆ": "st"}


def delig(s):
    for k, v in LIG.items():
        if k in s:
            s = s.replace(k, v)
    return s


def squash(s, n):
    return " ".join(t.strip() for t in delig(s).splitlines() if t.strip())[:n]


def clip(pg, r):
    W, H = pg.rect.width, pg.rect.height
    x0, y0, x1, y1 = r
    return fitz.Rect(x0 * W, y0 * H, x1 * W, min(1.0, y1) * H)


def main():
    os.makedirs(OUT, exist_ok=True)
    code = sys.argv[1]
    yd, fid = code.split("/")
    if not fid.endswith(".pdf"):
        fid += ".pdf"
    sc = json.load(open(os.path.join(STAGE, yd, fid + ".json")))
    sd = fitz.open(os.path.join(CORPUS, "markingschemes", yd, sc["schemeFileid"]))
    pd = fitz.open(os.path.join(CORPUS, "exampapers", yd, sc["paperFileid"]))
    qs = sc["q"]
    idxs = sorted(set([0, len(qs) // 2, len(qs) - 1]))
    print(f"# {code}  paper={sc['paperFileid']}({len(pd)}pp) scheme={sc['schemeFileid']}({len(sd)}pp) {len(qs)}Q")
    for i in idxs:
        q = qs[i]; n = q["n"]; seg = q["region"][0]
        pP = q["pP"]; pY = q.get("pY", [0, 1])
        stem = pd[pP - 1].get_text("text", clip=clip(pd[pP - 1], [0, pY[0], 1, pY[1]]))
        print(f"== Q{n} (paper p{pP}) ==")
        print(f"  PAPER asks: {squash(stem, 240)}")
        if "r" in seg:
            ct = sd[seg["p"] - 1].get_text("text", clip=clip(sd[seg["p"] - 1], seg["r"]))
            print(f"  SCHEME crop p{seg['p']} mode={q['mode']}: {squash(ct, 300)}")
            pg = sd[seg["p"] - 1]
            pix = pg.get_pixmap(matrix=fitz.Matrix(1.6, 1.6), clip=clip(pg, seg["r"]))
            png = os.path.join(OUT, f"{fid[:-4]}_Q{n}.png")
            pix.save(png)
            print(f"  RENDER: {png}")
        else:
            print(f"  SCHEME crop p{seg['p']} mode={q['mode']} WHOLE/pagejump")
    sd.close(); pd.close()


if __name__ == "__main__":
    main()
