#!/usr/bin/env python3
"""Irish (LC001) Paper 1 — Cluastuiscint + Ceapadóireacht bands.

P1 is Cuid I An Chluastuiscint (Cuid A/B/C answer books) + Cuid II An
Cheapadóireacht.  The combined scheme (LC001xLP000IV, named LP100IV in 2026)
opens with Páipéar 1: per-Cuid aural answers, then the Ceapadóireacht
criteria, before the Páipéar 2 half that the committed P2 sidecars already
band.  Chips: Cuid A / Cuid B / Cuid C / An Cheapadóireacht.

Anchors are required on both sides in print order; the Páipéar 2 header caps
the last band.

Usage: python3 irish_p1.py <years...>
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

CUID = re.compile(r"^Cuid\s+([ABC])\s*(\(|$)", re.I)
CEAP = re.compile(r"^(Cuid\s+II\s*[-:–—]*\s*(An\s+)?Ch?eapad[óo]ireacht|CEAPAD[ÓO]IREACHT)", re.I)
P2 = re.compile(r"^P[áa]ip[ée]ar\s+(2|II)\b", re.I)
LABELS = {
    "A": "Cluastuiscint · Cuid A",
    "B": "Cluastuiscint · Cuid B",
    "C": "Cluastuiscint · Cuid C",
    "CEAP": "An Cheapadóireacht",
}
ORDER = ["A", "B", "C", "CEAP"]


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


def anchors(doc, stop_at_p2):
    """Paper: first occurrence per key.  Scheme (stop_at_p2): LAST occurrence
    before the Ceapadóireacht — old schemes print tapescripts first, answers
    after, and the answers are what a chip should open."""
    found, end = {}, None
    for pi in range(1, len(doc)):
        for txt, x0, y in lines_of(doc[pi]):
            t = txt.replace("\xa0", " ").strip()
            if stop_at_p2 and P2.match(t):
                end = (pi, y)
                return found, end
            m = CUID.match(t)
            if m and "CEAP" not in found:
                k = m.group(1).upper()
                if stop_at_p2 or k not in found:
                    found[k] = (pi, y)
                continue
            if "CEAP" not in found and (
                    CEAP.match(t)
                    or (stop_at_p2 and re.match(r"^CUID\s+II\s*$", t, re.I))):
                found["CEAP"] = (pi, y)
    return found, end


def build(paper_path, scheme_path):
    paper, scheme = fitz.open(paper_path), fitz.open(scheme_path)
    S = len(scheme)
    pf, _ = anchors(paper, stop_at_p2=False)
    sf, send = anchors(scheme, stop_at_p2=True)
    keys = [k for k in ORDER if k in pf]
    if len(keys) < 3 or "CEAP" not in keys:
        return None, f"too few paper anchors: {keys}"
    missing = [k for k in keys if k not in sf]
    if missing:
        return None, f"scheme anchors missing {missing}"
    for seq, side in ((pf, "paper"), (sf, "scheme")):
        pts = [seq[k] for k in keys]
        if any(b <= a for a, b in zip(pts, pts[1:])):
            return None, f"{side} anchors not monotonic"
    end = send or (S, 0.0)
    qs = []
    for i, k in enumerate(keys):
        sp, sy = sf[k]
        ep, ey = sf[keys[i + 1]] if i + 1 < len(keys) else end
        segs = [{"p": sp + 1, "r": [0.0, round(sy, 4), 1.0, 1.0]}]
        for p in range(sp + 1, min(ep, sp + 6)):
            segs.append({"p": p + 1, "r": [0.0, 0.0, 1.0, 1.0]})
        if ep < sp + 6 and ey > 0.02:
            segs.append({"p": ep + 1, "r": [0.0, 0.0, 1.0, round(ey, 4)]})
        p_pi, p_y = pf[k]
        nxt = pf[keys[i + 1]] if i + 1 < len(keys) else (len(paper), 1.0)
        py1 = nxt[1] if nxt[0] == p_pi else 1.0
        qs.append({"n": str(i + 1), "pP": p_pi + 1,
                   "pY": [round(p_y, 4), round(py1, 4)],
                   "region": segs, "mode": "crop", "conf": 1.0,
                   "label": LABELS[k]})
    sidecar = {"v": SIDECAR_V, "paperFileid": os.path.basename(paper_path),
               "schemeFileid": os.path.basename(scheme_path),
               "component": "100", "band": [1, S + 1],
               "copyright": COPYRIGHT, "q": qs}
    return sidecar, None


def main():
    years = [int(y) for y in sys.argv[1:] if y.isdigit()] or list(range(2010, 2027))
    ok = drop = 0
    for year in years:
        for lvl in "AG":
            f = f"LC001{lvl}LP100IV.pdf"
            pp = os.path.join(CORPUS, "exampapers", str(year), f)
            if not os.path.exists(pp):
                continue
            sp = None
            for sname in (f"LC001{lvl}LP000IV.pdf", f"LC001{lvl}LP100IV.pdf"):
                cand = os.path.join(CORPUS, "markingschemes", str(year), sname)
                if os.path.exists(cand):
                    sp = cand
                    break
            if sp is None:
                continue
            dst = os.path.join(ANSWERS, str(year), f"{f}.json")
            if os.path.exists(dst):
                continue
            sidecar, err = build(pp, sp)
            if sidecar is None:
                print(f"DROP {year} {lvl}: {err}")
                drop += 1
                continue
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            json.dump(sidecar, open(dst, "w"), sort_keys=True,
                      separators=(",", ":"))
            print(f"OK   {year} {lvl}: {len(sidecar['q'])} bands "
                  f"(scheme {os.path.basename(sp)})")
            ok += 1
    print(f"\nmapped {ok} · dropped {drop}")


if __name__ == "__main__":
    main()
