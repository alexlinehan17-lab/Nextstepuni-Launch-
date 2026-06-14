#!/usr/bin/env python3
"""Dump, for a flagged sidecar, the evidence needed to judge each question:
the PAPER stem (clipped at the sidecar's stored paper band), the SCHEME CROP
text the sidecar actually shows, and the full text of the scheme pages around
the crop — so a verifier can decide by CONTENT whether crop(Qn) answers the
paper's question N.

Usage: python3 pt_inspect.py <year>/<paperFileid-without-.json>   e.g.
       python3 pt_inspect.py 2017/LC025GLP000EV
       python3 pt_inspect.py 2025/LC219ALP040EV --all   # every q, not just flagged
"""
import json, os, re, sys
import fitz
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
CORPUS = os.path.join(REPO, "paper-trail-corpus")
ANS = os.environ.get("PTANS_DIR") or os.path.join(HERE, "answers")
LIG = {"Ɵ": "ti", "Ʃ": "tt", "ϐ": "fi", "ﬀ": "ff", "ﬁ": "fi", "ﬂ": "fl",
       "ﬃ": "ffi", "ﬄ": "ffl", "ﬅ": "ft", "ﬆ": "st"}


def delig(s):
    for k, v in LIG.items():
        if k in s:
            s = s.replace(k, v)
    return s


def squash(s, lim):
    return " ".join(t.strip() for t in delig(s).splitlines() if t.strip())[:lim]


def clip(pg, r):
    W, H = pg.rect.width, pg.rect.height
    x0, y0, x1, y1 = r
    return pg.get_text("text", clip=fitz.Rect(x0 * W, y0 * H, x1 * W, min(1.0, y1) * H))


def main():
    code = sys.argv[1]
    show_all = "--all" in sys.argv
    flagged = json.load(open("/tmp/pt_flagged.json")) if os.path.exists("/tmp/pt_flagged.json") else {}
    yd, fid = code.split("/")
    if not fid.endswith(".pdf"):
        fid += ".pdf"
    path = os.path.join(ANS, yd, fid + ".json")
    sc = json.load(open(path))
    sd = fitz.open(os.path.join(CORPUS, "markingschemes", yd, sc["schemeFileid"]))
    pd = fitz.open(os.path.join(CORPUS, "exampapers", yd, sc["paperFileid"]))
    flag_ns = {f["n"] for f in flagged.get(yd + "/" + fid, {}).get("flagged", [])}
    print(f"# {code}  paper={sc['paperFileid']} ({len(pd)}pp)  scheme={sc['schemeFileid']} ({len(sd)}pp)  band={sc['band']}")
    print(f"# {len(sc['q'])} questions; flagged: {sorted(flag_ns, key=lambda x:int(x)) if flag_ns else 'ALL (run with --all)'}\n")
    for q in sc["q"]:
        if not show_all and flag_ns and q["n"] not in flag_ns:
            continue
        n = q["n"]
        pP = q["pP"]; pY = q.get("pY", [0, 1])
        paper_stem = clip(pd[pP - 1], [0.0, pY[0], 1.0, pY[1]])
        print(f"================= Q{n}  (paper p{pP} y{pY[0]:.2f}-{pY[1]:.2f}) =================")
        print(f"PAPER Q{n} STEM: {squash(paper_stem, 360)}")
        for si, seg in enumerate(q["region"]):
            if "r" in seg:
                ct = clip(sd[seg["p"] - 1], seg["r"])
                print(f"SCHEME CROP seg{si} p{seg['p']} y{seg['r'][1]:.2f}-{seg['r'][3]:.2f}: {squash(ct, 420)}")
            else:
                print(f"SCHEME CROP seg{si} p{seg['p']} WHOLE PAGE: {squash(sd[seg['p']-1].get_text('text'), 420)}")
        # context: the crop's first scheme page in full + the one before/after
        p0 = q["region"][0]["p"]
        for pp in (p0 - 1, p0, p0 + 1):
            if 1 <= pp <= len(sd):
                print(f"  -- scheme p{pp} full: {squash(sd[pp-1].get_text('text'), 240)}")
        print()
    sd.close(); pd.close()


if __name__ == "__main__":
    main()
