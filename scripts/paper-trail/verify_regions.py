#!/usr/bin/env python3
"""Independent region verifier for committed answer sidecars.

For each (or a code-filtered subset of) committed sidecar, clips the scheme PDF to
each question's region rectangle and reports the text that actually falls inside —
so a human/agent can confirm question N's crop really shows question N's answer.
Optionally renders crops to PNG for eyeballing.

Usage:
  python3 verify_regions.py LC005            # text spot-check all Geography sidecars
  python3 verify_regions.py LC027 --render   # + render every crop to /tmp/ptverify
"""
import json, os, re, sys
import fitz

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
CORPUS = os.path.join(REPO, "paper-trail-corpus")
ANS = os.path.join(HERE, "answers")
LIG = {"Ɵ": "ti", "Ʃ": "tt", "ϐ": "fi", "ﬀ": "ff", "ﬁ": "fi", "ﬂ": "fl", "ﬃ": "ffi", "ﬄ": "ffl"}


def delig(s):
    for k, v in LIG.items():
        s = s.replace(k, v)
    return s


def clip_text(pg, r):
    W, H = pg.rect.width, pg.rect.height
    x0, y0, x1, y1 = r
    return pg.get_text("text", clip=fitz.Rect(x0 * W, y0 * H, x1 * W, min(1.0, y1) * H))


def main():
    prefix = sys.argv[1] if len(sys.argv) > 1 else ""
    render = "--render" in sys.argv
    if render:
        os.makedirs("/tmp/ptverify", exist_ok=True)
    total = good = 0
    for yd in sorted(os.listdir(ANS)):
        d = os.path.join(ANS, yd)
        if not os.path.isdir(d):
            continue
        for fn in sorted(os.listdir(d)):
            if prefix and not fn.startswith(prefix):
                continue
            sc = json.load(open(os.path.join(d, fn)))
            sd = fitz.open(os.path.join(CORPUS, "markingschemes", yd, sc["schemeFileid"]))
            print(f"\n### {yd}/{fn}  scheme={sc['schemeFileid']} band={sc['band']}")
            for q in sc["q"]:
                n = int(q["n"]); total += 1
                seg0 = q["region"][0]
                if "r" in seg0:
                    txt = delig(clip_text(sd[seg0["p"] - 1], seg0["r"]))
                else:
                    txt = delig(sd[seg0["p"] - 1].get_text("text"))
                line0 = " ".join(t.strip() for t in txt.splitlines() if t.strip())[:64]
                ms = [int(m) for m in re.findall(r"Question\s+(\d+)", txt)]
                start_ok = bool(ms) and ms[0] == n
                good += start_ok
                mark = "ok " if start_ok else "BAD"
                print(f"  [{mark}] Q{n:>2} {q['mode'][:4]} p{seg0['p']}: {line0}")
                if render and "r" in seg0:
                    pg = sd[seg0["p"] - 1]; W, H = pg.rect.width, pg.rect.height
                    x0, y0, x1, y1 = seg0["r"]
                    pix = pg.get_pixmap(matrix=fitz.Matrix(1.4, 1.4),
                                        clip=fitz.Rect(x0 * W, y0 * H, x1 * W, min(1.0, y1) * H))
                    pix.save(f"/tmp/ptverify/{fn[:9]}_{yd}_Q{n}.png")
            sd.close()
    print(f"\n=== {good}/{total} question crops START at their own 'Question n' header ===")
    return 0 if good == total else 1


if __name__ == "__main__":
    sys.exit(main())
