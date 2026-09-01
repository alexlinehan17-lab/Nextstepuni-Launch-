#!/usr/bin/env python3
"""Music (LC067) answer maps — component-banded bespoke.

The single Music scheme bundles COMPOSING (component 006), LISTENING (008) and
elective material, and each component restarts Q1..N — which is why the generic
engine mis-bands or drops these papers (and why 2026's composing chips once
opened listening answers). The reliable structure is the RUNNING PAGE HEADER:
every scheme page names its component ("… Marking Scheme Composing – Higher
level – Core", "Listening - Higher Level – Core", Irish "Cumadóireacht" /
"Éisteacht"). So:

  1. Band the scheme by running-header keyword, EXCLUDING elective pages.
  2. Within the band, find question starts by any of the observed marker styles:
       'Q.N TITLE' headers (composing, 2010s), a leading 'Q N' pair opening a
       per-question marks table (listening), 'C.N' section heads (2018-era),
       or restated 'Question N' blocks (2020s).
  3. Chip regions run marker → next marker / band end. Count-reconcile against
     the paper's detected questions; drop on any mismatch.

Usage: python3 music_sections.py <years...>   (corpus + answers/ layout paths)
Writes sidecars only for (paper, scheme) pairs that fully reconcile.
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
MAX_REGION_PAGES = 6

COMPONENT_WORDS = {
    "006": ("composing", "cumad"),      # Cumadóireacht
    "008": ("listening", "éisteacht", "eisteacht"),
}
ELECTIVE_WORDS = ("elective", "roghnach")

# The 2026 composing trap: that scheme's composing section is NOT a per-question
# block structure and the generic engine shipped listening answers for it once.
# Until a year's composing section is verified by render, refuse re-emission for
# the known-bad year.
NEVER = {("006", 2026)}


def page_header_text(page):
    H = page.rect.height
    words = [w[4] for w in page.get_text("words") if w[1] < H * 0.12]
    return " ".join(words).lower()


def component_band(scheme, comp):
    keys = COMPONENT_WORDS[comp]
    pages = []
    for pi in range(len(scheme)):
        hdr = page_header_text(scheme[pi])
        if any(k in hdr for k in keys) and not any(e in hdr for e in ELECTIVE_WORDS):
            pages.append(pi)
    if not pages:
        return None
    # contiguous run containing the most pages (running headers make this dense)
    runs, start = [], pages[0]
    for a, b in zip(pages, pages[1:] + [None]):
        if b is None or b > a + 1:
            runs.append((start, a))
            start = b
    lo, hi = max(runs, key=lambda r: r[1] - r[0])
    return lo, hi + 1  # [lo, hi)


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


def scheme_markers(scheme, lo, hi):
    """{n: (page0, yFrac)} across the band, first occurrence, any style."""
    seen = {}
    for pi in range(lo, hi):
        for txt, x0, y in lines_of(scheme[pi]):
            m = re.match(r"^(?:Question|Ceist)\s+(\d{1,2})\b", txt, re.I)
            if m is None:
                if x0 > 150:
                    continue
                m = (re.match(r"^Q\.?\s*(\d{1,2})\b", txt)
                     or re.match(r"^C\.?\s*(\d{1,2})\b", txt))
            if m:
                n = int(m.group(1))
                if 1 <= n <= 20 and n not in seen:
                    seen[n] = (pi, y)
        # 'Q' and its number can extract as ADJACENT one-word lines (the 2015
        # listening tables): pair a lone left-margin 'Q' with the nearest digit
        # word just right/below it.
        # Table style (2015-era listening): the page is one question's marks
        # table; 'Q' heads a column and the question number sits in that column
        # far below. Take the topmost lone digit in the leftmost column as the
        # page's question number.
        H = scheme[pi].rect.height
        words = sorted(scheme[pi].get_text("words"), key=lambda w: w[1])
        hdr_has_q = any(w[4] in ("Q", "C") and w[0] < 80 for w in words[:24])
        if hdr_has_q:
            for w in words:
                if (re.fullmatch(r"\d{1,2}", w[4]) and w[0] < 75
                        and w[1] > H * 0.08):
                    n = int(w[4])
                    if 1 <= n <= 20 and n not in seen:
                        seen[n] = (pi, 0.0)
                    break
    return seen


def paper_questions(paper):
    seen = {}
    for pi in range(len(paper)):
        for txt, x0, y in lines_of(paper[pi]):
            m = (re.match(r"^(?:Question|Ceist)\s+(\d{1,2})\b", txt, re.I)
                 or re.match(r"^Q\.?\s*(\d{1,2})\b", txt)
                 or re.match(r"^(\d{1,2})\.\s", txt))
            if m and x0 < 150:
                n = int(m.group(1))
                if 1 <= n <= 20 and n not in seen:
                    seen[n] = (pi, y)
    return seen


def region_between(start, end, hi):
    (sp, sy), e = start, end if end else (hi, 0.0)
    ep, ey = e
    segs = []
    if ep == sp:
        if ey <= sy:
            return None
        return [{"p": sp + 1, "r": [0.0, round(sy, 4), 1.0, round(ey, 4)]}]
    segs.append({"p": sp + 1, "r": [0.0, round(sy, 4), 1.0, 1.0]})
    for p in range(sp + 1, min(ep, sp + MAX_REGION_PAGES - 1)):
        segs.append({"p": p + 1, "r": [0.0, 0.0, 1.0, 1.0]})
    if ep < sp + MAX_REGION_PAGES - 1 and ey > 0.02:
        segs.append({"p": ep + 1, "r": [0.0, 0.0, 1.0, round(ey, 4)]})
    return segs


def build(paper_path, scheme_path, comp, year):
    if (comp, year) in NEVER:
        return None, "NEVER (verified-bad year for this component)"
    paper, scheme = fitz.open(paper_path), fitz.open(scheme_path)
    band = component_band(scheme, comp)
    if not band:
        return None, "no component band in scheme"
    lo, hi = band
    pq = paper_questions(paper)
    ns = sorted(pq)
    if not ns or ns != list(range(1, len(ns) + 1)):
        return None, f"paper questions not 1..N: {ns}"
    ppts = [pq[n] for n in ns]
    if any(b <= a for a, b in zip(ppts, ppts[1:])):
        return None, "paper anchors not monotonic (decoy numbering)"
    sm = scheme_markers(scheme, lo, hi)
    missing = [n for n in ns if n not in sm]
    if missing:
        return None, f"scheme markers missing {missing} in band {lo}-{hi}"
    pts = [sm[n] for n in ns]
    if any(b <= a for a, b in zip(pts, pts[1:])):
        return None, "scheme markers not monotonic in band"
    qs = []
    for i, n in enumerate(ns):
        nxt = sm[ns[i + 1]] if i + 1 < len(ns) else None
        segs = region_between(sm[n], nxt, hi)
        if not segs:
            return None, f"empty region Q{n}"
        p_pi, p_y = pq[n]
        nxt_p = pq[ns[i + 1]] if i + 1 < len(ns) else (len(paper), 1.0)
        py1 = nxt_p[1] if nxt_p[0] == p_pi else 1.0
        qs.append({"n": str(n), "pP": p_pi + 1,
                   "pY": [round(p_y, 4), round(py1, 4)],
                   "region": segs, "mode": "crop", "conf": 1.0})
    sidecar = {"v": SIDECAR_V, "paperFileid": os.path.basename(paper_path),
               "schemeFileid": os.path.basename(scheme_path),
               "component": comp, "band": [lo + 1, hi + 1],
               "copyright": COPYRIGHT, "q": qs}
    return sidecar, None


def main():
    years = [int(y) for y in sys.argv[1:]] or list(range(2010, 2026))
    ok = drop = 0
    for year in years:
        for lvl in "AG":
            for comp in ("006", "008"):
                for lang in ("EV", "IV"):
                    f = f"LC067{lvl}LP{comp}{lang}.pdf"
                    s = f"LC067{lvl}LP000{lang}.pdf"
                    pp = os.path.join(CORPUS, "exampapers", str(year), f)
                    sp = os.path.join(CORPUS, "markingschemes", str(year), s)
                    if not (os.path.exists(pp) and os.path.exists(sp)):
                        continue
                    dst = os.path.join(ANSWERS, str(year), f"{f}.json")
                    if os.path.exists(dst):
                        continue  # committed (earlier verified maps stay)
                    sidecar, err = build(pp, sp, comp, year)
                    if sidecar is None:
                        print(f"DROP {year} {lvl} {comp} {lang}: {err}")
                        drop += 1
                        continue
                    os.makedirs(os.path.dirname(dst), exist_ok=True)
                    json.dump(sidecar, open(dst, "w"), sort_keys=True,
                              separators=(",", ":"))
                    print(f"OK   {year} {lvl} {comp} {lang}: {len(sidecar['q'])} q")
                    ok += 1
    print(f"\nmapped {ok} · dropped {drop}")


if __name__ == "__main__":
    main()
