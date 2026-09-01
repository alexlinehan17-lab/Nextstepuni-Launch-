#!/usr/bin/env python3
"""Latin (LC006) Higher Level — five-question bespoke.

The HL paper numbers its five questions '1.'-'5.' (some glued to the stem,
some lone); the scheme mixes '1.' with 'Q2.'/'Q3'/'Q4.' prefixes, which is
why the generic engine's single-detector reconcile kept failing.  Both sides
are matched as an ascending 1..5 run (Q-prefix optional on the scheme), with
the usual completeness + monotonic gates.

Usage: python3 latin_hl.py <years...>
"""
import json
import os
import re
import sys
from collections import defaultdict

import fitz

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
CORPUS = os.path.join(REPO, "paper-trail-corpus")
ANSWERS = os.path.join(HERE, "answers")
SIDECAR_V = 1
COPYRIGHT = "© State Examinations Commission"

P_Q = re.compile(r"^([1-5])\s*\.")
S_Q = re.compile(r"^(?:[QC]\s*\.?\s*)?([1-5])\s*[\.\:]?(\s|$)")


def lines_of(page):
    lines = defaultdict(list)
    for w in page.get_text("words"):
        lines[(w[5], w[6])].append(w)
    out = []
    H = page.rect.height
    for k in sorted(lines):
        lw = sorted(lines[k], key=lambda w: w[0])
        out.append((" ".join(w[4] for w in lw), lw[0][0], lw[0][1] / H))
    out.sort(key=lambda t: t[2])
    return out


def run_of(doc, rx, xmax, start=1):
    found, num = {}, 0
    for pi in range(start, len(doc)):
        for txt, x0, y in lines_of(doc[pi]):
            m = rx.match(txt.strip())
            if m and x0 < xmax and int(m.group(1)) == num + 1:
                num += 1
                found[num] = (pi, y)
    return found


def build(paper_path, scheme_path, iv):
    paper, scheme = fitz.open(paper_path), fitz.open(scheme_path)
    S = len(scheme)
    pf = run_of(paper, P_Q, 95)
    sf = run_of(scheme, S_Q, 110)
    keys = sorted(pf)
    if len(keys) < 4:
        return None, f"too few paper questions: {keys}"
    missing = [n for n in keys if n not in sf]
    if missing:
        return None, f"scheme questions missing {missing} (has {sorted(sf)})"
    for seq, side in ((pf, "paper"), (sf, "scheme")):
        pts = [seq[n] for n in keys]
        if any(b <= a for a, b in zip(pts, pts[1:])):
            return None, f"{side} anchors not monotonic"
    word = "Ceist" if iv else "Question"
    qs = []
    for i, n in enumerate(keys):
        sp, sy = sf[n]
        ep, ey = sf[keys[i + 1]] if i + 1 < len(keys) else (S, 0.0)
        segs = [{"p": sp + 1, "r": [0.0, round(sy, 4), 1.0, 1.0]}]
        for p in range(sp + 1, min(ep, sp + 5)):
            segs.append({"p": p + 1, "r": [0.0, 0.0, 1.0, 1.0]})
        if ep < sp + 5 and ey > 0.02:
            segs.append({"p": ep + 1, "r": [0.0, 0.0, 1.0, round(ey, 4)]})
        p_pi, p_y = pf[n]
        nxt = pf[keys[i + 1]] if i + 1 < len(keys) else (len(paper), 1.0)
        py1 = nxt[1] if nxt[0] == p_pi else 1.0
        qs.append({"n": str(n), "pP": p_pi + 1,
                   "pY": [round(p_y, 4), round(py1, 4)],
                   "region": segs, "mode": "crop", "conf": 1.0,
                   "label": f"{word} {n}"})
    sidecar = {"v": SIDECAR_V, "paperFileid": os.path.basename(paper_path),
               "schemeFileid": os.path.basename(scheme_path),
               "component": "000", "band": [1, S + 1],
               "copyright": COPYRIGHT, "q": qs}
    return sidecar, None


def main():
    years = [int(y) for y in sys.argv[1:] if y.isdigit()] or list(range(2010, 2027))
    ok = drop = 0
    for year in years:
        for lang in ("EV", "IV"):
            f = f"LC006ALP000{lang}.pdf"
            pp = os.path.join(CORPUS, "exampapers", str(year), f)
            sp = os.path.join(CORPUS, "markingschemes", str(year), f)
            if not (os.path.exists(pp) and os.path.exists(sp)):
                continue
            dst = os.path.join(ANSWERS, str(year), f"{f}.json")
            if os.path.exists(dst):
                continue
            sidecar, err = build(pp, sp, lang == "IV")
            if sidecar is None:
                print(f"DROP {year} {lang}: {err}")
                drop += 1
                continue
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            json.dump(sidecar, open(dst, "w"), sort_keys=True,
                      separators=(",", ":"))
            print(f"OK   {year} {lang}: {len(sidecar['q'])} questions")
            ok += 1
    print(f"\nmapped {ok} · dropped {drop}")


if __name__ == "__main__":
    main()
