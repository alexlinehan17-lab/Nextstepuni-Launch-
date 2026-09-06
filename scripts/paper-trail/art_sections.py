#!/usr/bin/env python3
"""Art Visual Studies (LC014, new-spec 2023+) — section/descriptor bespoke.

The restyled H&A ("Visual Studies") scheme carries three kinds of content:
  • per-question indicative answers for SOME Section A questions
    ("Question 1 Answer (a) …"),
  • ONE common descriptor for all Section A short questions,
  • common band descriptors shared by every Section B and C question.

So chips follow the wave-10 labelled pattern: a Section A question opens its
own block when the scheme has one, else the common short-question descriptor
(labelled honestly); B/C questions open the shared band descriptors. The paper
side is 'Question N' headers; numbering is continuous across sections.

Usage: python3 art_sections.py <years...>
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


def paper_questions(paper):
    """{n: (page0,yFrac)} 'Question N' (EN) / 'Ceist N' (IV) headers + which
    section each belongs to, from the running 'Section X' headers."""
    seen, sections, cur = {}, {}, "A"
    for pi in range(1, len(paper)):
        for txt, x0, y in lines_of(paper[pi]):
            sm = re.match(r"^(?:Section|Roinn)\s+([ABC])\b", txt, re.I)
            if sm and y < 0.25:
                # real section dividers head their page; the instructions page
                # lists every section mid-page in a contents box — ignore those
                cur = sm.group(1).upper()
            m = re.match(r"^(?:Question|Ceist)\s+(\d{1,2})\b", txt)
            if m and x0 < 200:
                n = int(m.group(1))
                if 1 <= n <= 30 and n not in seen:
                    seen[n] = (pi, y)
                    sections[n] = cur
    return seen, sections


def scheme_anchors(scheme, iv):
    """(specific {n:(p,y)}, shortA (p,y) or None, bands (p,y) or None)."""
    specific, shortA, bands = {}, None, None
    for pi in range(len(scheme)):
        for txt, x0, y in lines_of(scheme[pi]):
            m = re.match(r"^(?:Question|Ceist)\s+(\d{1,2})\s+(?:Answer|Freagra)", txt, re.I)
            if m:
                n = int(m.group(1))
                if n not in specific:
                    specific[n] = (pi, y)
            if shortA is None and re.search(
                    r"Descriptor for short questions|Tuairisc[íi]n le haghaidh ceisteanna gearra", txt, re.I):
                shortA = (pi, y)
            if bands is None and re.search(
                    r"Band Descriptor for Section B|Tuairisc[íi]n[íi]? (?:ar na Bandaí|Banda) .*Roinn B", txt, re.I):
                bands = (pi, y)
    return specific, shortA, bands


def region_from(start, end, S, maxp=6):
    (sp, sy), e = start, end if end else (S, 0.0)
    ep, ey = e
    segs = [{"p": sp + 1, "r": [0.0, round(sy, 4), 1.0, 1.0]}]
    for p in range(sp + 1, min(ep, sp + maxp)):
        segs.append({"p": p + 1, "r": [0.0, 0.0, 1.0, 1.0]})
    if ep < sp + maxp and ey > 0.02:
        segs.append({"p": ep + 1, "r": [0.0, 0.0, 1.0, round(ey, 4)]})
    return segs


def build(paper_path, scheme_path, iv):
    paper, scheme = fitz.open(paper_path), fitz.open(scheme_path)
    S = len(scheme)
    pq, sections = paper_questions(paper)
    ns = sorted(pq)
    if not ns or ns != list(range(1, len(ns) + 1)):
        return None, f"paper questions not 1..N: {ns}"
    # Some papers (IV, and EV 2026) carry no per-page section dividers — only
    # the instructions-page contents box, which poisons the running tracker.
    # The new-spec structure is fixed (A: Q1-7 answer-five, B: Q8-13, C:
    # Q14-19), verified against every divider-carrying EV paper; apply it
    # whenever the derived assignment is not a sane forward partition.
    derived_ok = (len(ns) == 19
                  and all(sections[n] == "A" for n in range(1, 8))
                  and all(sections[n] == "B" for n in range(8, 14))
                  and all(sections[n] == "C" for n in range(14, 20)))
    if len(ns) == 19 and not derived_ok:
        sections = {n: ("A" if n <= 7 else "B" if n <= 13 else "C") for n in ns}
    elif not derived_ok:
        return None, f"unexpected structure: {len(ns)} questions"
    specific, shortA, bands = scheme_anchors(scheme, iv)
    if bands is None:
        return None, "no Section B/C band descriptor block"
    if any(sections[n] == "A" for n in ns) and shortA is None and not specific:
        return None, "no Section A content in scheme"
    spec_ns = sorted(n for n in specific if n in pq)
    band_end = None  # bands run to end of scheme
    qs = []
    word = "Ceist" if iv else "Question"
    for n in ns:
        sec = sections[n]
        if sec == "A":
            if n in specific:
                nxt = next((specific[m] for m in spec_ns if m > n), (shortA or bands))
                segs = region_from(specific[n], nxt, S)
                label = None
            else:
                anchor = shortA or bands
                segs = region_from(anchor, bands if (shortA and bands > shortA) else None, S, maxp=2)
                label = (f"{word} {n} · " +
                         ("tuairiscín coiteann na gceisteanna gearra" if iv
                          else "common short-question descriptor"))
        else:
            segs = region_from(bands, band_end, S)
            label = (f"{word} {n} · " +
                     ("tuairiscíní coiteanna Roinn B/C" if iv
                      else "Section B/C — common band descriptors"))
        p_pi, p_y = pq[n]
        nxt_p = pq[n + 1] if (n + 1) in pq else (len(paper), 1.0)
        py1 = nxt_p[1] if nxt_p[0] == p_pi else 1.0
        q = {"n": str(n), "pP": p_pi + 1, "pY": [round(p_y, 4), round(py1, 4)],
             "region": segs, "mode": "crop", "conf": 1.0}
        # The printed booklet inserts several blank answer pages between
        # Sections B and C. Without an explicit boundary Q13 appears to span
        # six pages and the runtime correctly refuses that implausible crop.
        # Section-ending questions finish on their own printed page.
        if (n + 1) in sections and sections[n + 1] != sec:
            q["endP"] = p_pi + 1
            q["endY"] = round(py1, 4)
        if label:
            q["label"] = label
        qs.append(q)
    sidecar = {"v": SIDECAR_V, "paperFileid": os.path.basename(paper_path),
               "schemeFileid": os.path.basename(scheme_path),
               "component": "013", "band": [1, S + 1],
               "copyright": COPYRIGHT, "q": qs}
    return sidecar, None


def main():
    refresh = "--refresh" in sys.argv[1:]
    years = [int(y) for y in sys.argv[1:] if y != "--refresh"] or [2023, 2024, 2025, 2026]
    ok = drop = 0
    for year in years:
        for lvl in "AG":
            for lang in ("EV", "IV"):
                for comp in ("000", "013"):
                    f = f"LC014{lvl}LP{comp}{lang}.pdf"
                    s = f"LC014{lvl}LP000{lang}.pdf"
                    pp = os.path.join(CORPUS, "exampapers", str(year), f)
                    sp = os.path.join(CORPUS, "markingschemes", str(year), s)
                    if not (os.path.exists(pp) and os.path.exists(sp)):
                        continue
                    dst = os.path.join(ANSWERS, str(year), f"{f}.json")
                    if os.path.exists(dst) and not refresh:
                        continue
                    sidecar, err = build(pp, sp, lang == "IV")
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
