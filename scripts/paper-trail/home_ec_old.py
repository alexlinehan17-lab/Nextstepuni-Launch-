#!/usr/bin/env python3
"""Home Economics S&S (LC098) old-era LP000 papers — per-question bespoke.

Both sides share the skeleton: centred 'Section A/B/C' dividers with numbered
questions inside (A: 1-12 short, B: 1-5, C: electives).  The generic engine's
lead_int reconcile kept rejecting 3 of A's 12 blocks; matching each section's
ascending run on both sides directly is exact.

Chips are per question, keyed (section, n), intersected across sides with
monotonic + minimum-count gates.

Usage: python3 home_ec_old.py <years...>
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

SEC = re.compile(r"^(?:Section|Roinn)\s+([ABC])\s*$", re.I)
# Older schemes vary between `3.`, `(3)`, and an unpunctuated number followed
# by the opening quotation mark of the question.  Keep the last form narrow so
# mark-allocation lines such as `4 points` cannot advance the question run.
NUM = re.compile(r"^\(?(\d{1,2})\)?(?:\s*[\.\)]|\s+(?=[‘'\"])|\s*$)")
CAPS = {"A": 12, "B": 5, "C": 5}


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


def collect(doc, start=1):
    """{(sec, n): (pi, y)} — ascending run per section."""
    found, sec, num = {}, None, 0
    for pi in range(start, len(doc)):
        for txt, x0, y in lines_of(doc[pi]):
            t = txt.strip()
            m = SEC.match(t)
            if m and x0 > 150:
                sec, num = m.group(1).upper(), 0
                found[("hdr", sec)] = (pi, y)
                continue
            if re.match(r"^Elective\s+1\b", t, re.I):
                # A few scanned Ordinary papers lose the `Section C` line in
                # extraction, but retain the unique Elective 1 divider.
                sec, num = "C", 0
                found[("hdr", sec)] = (pi, y)
                continue
            if sec == "B" and num == 5 and re.match(r"^1\s*\.\s*\(?a\)?", t, re.I):
                # 2011 Ordinary loses both words of the Section C / Elective 1
                # heading, but the numbered elective starts cleanly at 1(a).
                sec, num = "C", 0
                found[("hdr", sec)] = (pi, y)
            if sec is None:
                continue
            nm = NUM.match(t)
            if nm and x0 < 120:
                n = int(nm.group(1))
                if n == num + 1 and n <= CAPS[sec]:
                    num = n
                    found[(sec, n)] = (pi, y)
    return found


def build(paper_path, scheme_path, iv):
    paper, scheme = fitz.open(paper_path), fitz.open(scheme_path)
    S = len(scheme)
    pf = collect(paper)
    sf = collect(scheme)
    keys = [k for k in sorted(pf) if k[0] != "hdr" and k in sf]
    # sections must keep their print order; drop stragglers via longest run
    keys.sort(key=lambda k: pf[k])
    best = []
    for i in range(len(keys)):
        cand, last = [keys[i]], sf[keys[i]]
        for j in range(i + 1, len(keys)):
            if sf[keys[j]] > last:
                cand.append(keys[j])
                last = sf[keys[j]]
        if len(cand) > len(best):
            best = cand
    keys = best
    if len(keys) < 10:
        return None, f"too few both-side questions: {len(keys)}"
    word = "Roinn" if iv else "Section"
    q_word = "Ceist" if iv else "Q"
    qs = []
    for i, k in enumerate(keys):
        sp, sy = sf[k]
        ep, ey = sf[keys[i + 1]] if i + 1 < len(keys) else (S, 0.0)
        segs = [{"p": sp + 1, "r": [0.0, round(sy, 4), 1.0, 1.0]}]
        for p in range(sp + 1, min(ep, sp + 5)):
            segs.append({"p": p + 1, "r": [0.0, 0.0, 1.0, 1.0]})
        if ep < sp + 5 and ey > 0.02:
            segs.append({"p": ep + 1, "r": [0.0, 0.0, 1.0, round(ey, 4)]})
        p_pi, p_y = pf[k]
        nxt = pf[keys[i + 1]] if i + 1 < len(keys) else (len(paper), 1.0)
        py1 = nxt[1] if nxt[0] == p_pi else 1.0
        qs.append({"n": str(i + 1), "pP": p_pi + 1,
                   "pY": [round(p_y, 4), round(py1, 4)],
                   "region": segs, "mode": "crop", "conf": 1.0,
                   "label": f"{word} {k[0]} · {q_word}{k[1]}"})
    sidecar = {"v": SIDECAR_V, "paperFileid": os.path.basename(paper_path),
               "schemeFileid": os.path.basename(scheme_path),
               "component": "000", "band": [1, S + 1],
               "copyright": COPYRIGHT, "q": qs}
    return sidecar, None


def main():
    years = [int(y) for y in sys.argv[1:] if y.isdigit()] or list(range(2010, 2020))
    ok = drop = 0
    for year in years:
        for lvl in "AG":
            for lang in ("EV", "IV"):
                f = f"LC098{lvl}LP000{lang}.pdf"
                pp = os.path.join(CORPUS, "exampapers", str(year), f)
                sp = os.path.join(CORPUS, "markingschemes", str(year), f)
                if not (os.path.exists(pp) and os.path.exists(sp)):
                    continue
                dst = os.path.join(ANSWERS, str(year), f"{f}.json")
                if os.path.exists(dst):
                    continue
                sidecar, err = build(pp, sp, lang == "IV")
                if sidecar is None:
                    print(f"DROP {year} {lvl} {lang}: {err}")
                    drop += 1
                    continue
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                json.dump(sidecar, open(dst, "w"), sort_keys=True,
                          separators=(",", ":"))
                print(f"OK   {year} {lvl} {lang}: {len(sidecar['q'])} chips")
                ok += 1
    print(f"\nmapped {ok} · dropped {drop}")


if __name__ == "__main__":
    main()
