#!/usr/bin/env python3
"""Irish (LC001) Paper 2 answer maps — section-level bespoke.

Irish had zero chips ("Irish-medium, no EV" was a category error). Paper 2 is
the same three/four top-level questions every year at both levels:

  Ceist 1  An Léamhthuiscint  (two reading texts, sub-questions with answers)
  Ceist 2  An Prós            (named/optional prose — indicative notes)
  Ceist 3  An Fhilíocht       (named/optional poetry — indicative notes)
  Ceist 4  (HL, some years)   extra literature section

and the combined scheme carries one block per section, findable by stable
keyword headers in every era observed (2012/2017/2022/2025, HL+OL):
"(CEIST 1 -) LÉAMHTHUISCINT", "(Ceist 2 / 2A) PRÓS", "(Ceist 3 / 3A)
FILÍOCHT". Chips are SECTION-level with honest labels ("Ceist 2 · Prós"),
each opening its section's full scheme block — the wave-10 labelled-chip
pattern. Every paper Ceist must find its scheme anchor or the paper drops.

Usage: python3 irish_sections.py <years...>
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

SECTION_PATTERNS = {
    1: (r"(?:CEIST\s*1\s*[-–—:]?\s*)?L[ÉE]AMHTHUISCINT", "Léamhthuiscint"),
    2: (r"(?:CEIST\s*2|2A)\s*[-–—:]?\s*(?:AN\s+)?PR[ÓO]S", "Prós"),
    3: (r"(?:CEIST\s*3|3A)\s*[-–—:]?\s*(?:AN\s+)?FHIL[ÍI]OCHT"
        r"|(?:CEIST\s*3|3A)\s*[-–—:]?\s*FIL[ÍI]OCHT", "Filíocht"),
    4: (r"CEIST\s*4\b", "Ceist 4"),
}


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


def paper_ceists(paper):
    """{n: (page0, yFrac)} — first real 'Ceist N' header past the contents box
    (page 3 onward; the page-2 contents lists every Ceist with a colon)."""
    seen = {}
    for pi in range(2, len(paper)):
        for txt, x0, y in lines_of(paper[pi]):
            m = re.match(r"^\s*C[Ee][Ii][Ss][Tt]\s+(\d)\b(?!\s*:)", txt)
            if m and x0 < 200:
                n = int(m.group(1))
                if 1 <= n <= 4 and n not in seen:
                    seen[n] = (pi, y)
    return seen


def scheme_sections(scheme, wanted):
    """{n: (page0, yFrac)} for each wanted section header, ordered."""
    found = {}
    for pi in range(len(scheme)):
        ls = lines_of(scheme[pi])
        # headers split across adjacent lines ("CEIST 2" / "- PRÓS – …"):
        # test each line joined with its successor too
        joined = [(a[0] + " " + b[0], a[1], a[2]) for a, b in zip(ls, ls[1:])]
        for txt, x0, y in ls + joined:
            up = txt.upper()
            for n, (pat, _label) in SECTION_PATTERNS.items():
                if n in found or n not in wanted:
                    continue
                if re.search(pat, up):
                    # Léamhthuiscint front-matter mentions its own name inside
                    # marking guidance ("Treoracha do mharcáil na
                    # léamhthuisceana") — require a header-ish line: short, or
                    # starting with the section word/CEIST/«NA».
                    if len(txt) > 70:
                        continue
                    found[n] = (pi, y)
    return found


def build(paper_path, scheme_path):
    paper, scheme = fitz.open(paper_path), fitz.open(scheme_path)
    pq = paper_ceists(paper)
    ns = sorted(pq)
    if not ns or ns[0] != 1 or ns != list(range(1, len(ns) + 1)):
        return None, f"paper Ceist headers not 1..N: {ns}"
    sec = scheme_sections(scheme, set(ns))
    missing = [n for n in ns if n not in sec]
    if missing:
        return None, f"scheme sections missing {missing}"
    pts = [sec[n] for n in ns]
    if any(b <= a for a, b in zip(pts, pts[1:])):
        return None, "scheme sections out of order"
    S = len(scheme)
    qs = []
    for i, n in enumerate(ns):
        sp, sy = sec[n]
        ep, ey = sec[ns[i + 1]] if i + 1 < len(ns) else (S, 0.0)
        segs = [{"p": sp + 1, "r": [0.0, round(sy, 4), 1.0, 1.0]}]
        for p in range(sp + 1, min(ep, sp + 7)):
            segs.append({"p": p + 1, "r": [0.0, 0.0, 1.0, 1.0]})
        if ep < sp + 7 and ey > 0.02:
            segs.append({"p": ep + 1, "r": [0.0, 0.0, 1.0, round(ey, 4)]})
        p_pi, p_y = pq[n]
        nxt = pq[ns[i + 1]] if i + 1 < len(ns) else (len(paper), 1.0)
        py1 = nxt[1] if nxt[0] == p_pi else 1.0
        qs.append({"n": str(n), "pP": p_pi + 1,
                   "pY": [round(p_y, 4), round(py1, 4)],
                   "region": segs, "mode": "crop", "conf": 1.0,
                   "label": f"Ceist {n} · {SECTION_PATTERNS[n][1]}"})
    sidecar = {"v": SIDECAR_V, "paperFileid": os.path.basename(paper_path),
               "schemeFileid": os.path.basename(scheme_path),
               "component": "200", "band": [1, S + 1],
               "copyright": COPYRIGHT, "q": qs}
    return sidecar, None


def main():
    years = [int(y) for y in sys.argv[1:]] or list(range(2010, 2027))
    ok = drop = 0
    for year in years:
        for lvl in "AG":
            f = f"LC001{lvl}LP200IV.pdf"
            pp = os.path.join(CORPUS, "exampapers", str(year), f)
            sp = None
            # 2026 names the combined scheme after Paper 1
            for s in (f"LC001{lvl}LP000IV.pdf", f"LC001{lvl}LP100IV.pdf"):
                cand = os.path.join(CORPUS, "markingschemes", str(year), s)
                if os.path.exists(cand):
                    sp = cand
                    break
            if not (os.path.exists(pp) and sp):
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
            print(f"OK   {year} {lvl}: {len(sidecar['q'])} sections")
            ok += 1
    print(f"\nmapped {ok} · dropped {drop}")


if __name__ == "__main__":
    main()
