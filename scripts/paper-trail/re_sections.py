#!/usr/bin/env python3
"""Religious Education (LC223) — lettered-section bespoke.

Both sides speak in lettered SECTIONS (A..K spread across three UNITs): the
paper prints "SECTION A — THE SEARCH FOR MEANING AND VALUES" menus and the
scheme opens a matching block per letter ("SECTION A …", answers coded by
marking criteria). Chips are per SECTION with the letter as the label; n is
the letter's ordinal so the print-order gates hold.

Usage: python3 re_sections.py <years...>
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

SEC_RE = re.compile(r"^\s*SECTION\s+([A-K])\b[\s\-–—:]*(.{0,60})", re.I)


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


def find_sections(doc, start_page=0):
    seen = {}
    titles = {}
    for pi in range(start_page, len(doc)):
        for txt, x0, y in lines_of(doc[pi]):
            m = SEC_RE.match(txt)
            if m:
                L = m.group(1).upper()
                if L not in seen:
                    seen[L] = (pi, y)
                    t = m.group(2).strip().rstrip(".–-— ").title()
                    titles[L] = t
    return seen, titles


def build(paper_path, scheme_path):
    paper, scheme = fitz.open(paper_path), fitz.open(scheme_path)
    S = len(scheme)
    pq, ptitles = find_sections(paper, start_page=1)
    letters = sorted(pq, key=lambda L: pq[L])
    if len(letters) < 4:
        return None, f"too few paper sections: {letters}"
    # letters must be in alphabetical order as printed (the RE structure)
    if letters != sorted(letters):
        return None, f"paper sections out of order: {letters}"
    sq, _ = find_sections(scheme, start_page=2)
    missing = [L for L in letters if L not in sq]
    if missing:
        return None, f"scheme sections missing {missing}"
    pts = [sq[L] for L in letters]
    if any(b <= a for a, b in zip(pts, pts[1:])):
        return None, "scheme sections not monotonic"
    qs = []
    for i, L in enumerate(letters):
        sp, sy = sq[L]
        ep, ey = sq[letters[i + 1]] if i + 1 < len(letters) else (S, 0.0)
        segs = [{"p": sp + 1, "r": [0.0, round(sy, 4), 1.0, 1.0]}]
        for p in range(sp + 1, min(ep, sp + 6)):
            segs.append({"p": p + 1, "r": [0.0, 0.0, 1.0, 1.0]})
        if ep < sp + 6 and ey > 0.02:
            segs.append({"p": ep + 1, "r": [0.0, 0.0, 1.0, round(ey, 4)]})
        p_pi, p_y = pq[L]
        nxt = pq[letters[i + 1]] if i + 1 < len(letters) else (len(paper), 1.0)
        py1 = nxt[1] if nxt[0] == p_pi else 1.0
        title = (ptitles.get(L) or "").strip()
        label = f"Section {L}" + (f" · {title[:40]}" if title else "")
        qs.append({"n": str(i + 1), "pP": p_pi + 1,
                   "pY": [round(p_y, 4), round(py1, 4)],
                   "region": segs, "mode": "crop", "conf": 1.0,
                   "label": label})
    sidecar = {"v": SIDECAR_V, "paperFileid": os.path.basename(paper_path),
               "schemeFileid": os.path.basename(scheme_path),
               "component": "000", "band": [1, S + 1],
               "copyright": COPYRIGHT, "q": qs}
    return sidecar, None


def main():
    years = [int(y) for y in sys.argv[1:]] or list(range(2010, 2027))
    ok = drop = 0
    for year in years:
        for lvl in "AG":
            for lang in ("EV", "IV"):
                f = f"LC223{lvl}LP000{lang}.pdf"
                pp = os.path.join(CORPUS, "exampapers", str(year), f)
                sp = os.path.join(CORPUS, "markingschemes", str(year), f)
                if not (os.path.exists(pp) and os.path.exists(sp)):
                    continue
                dst = os.path.join(ANSWERS, str(year), f"{f}.json")
                if os.path.exists(dst):
                    continue
                sidecar, err = build(pp, sp)
                if sidecar is None:
                    print(f"DROP {year} {lvl} {lang}: {err}")
                    drop += 1
                    continue
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                json.dump(sidecar, open(dst, "w"), sort_keys=True,
                          separators=(",", ":"))
                print(f"OK   {year} {lvl} {lang}: {len(sidecar['q'])} sections")
                ok += 1
    print(f"\nmapped {ok} · dropped {drop}")


if __name__ == "__main__":
    main()
