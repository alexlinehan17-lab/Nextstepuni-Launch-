#!/usr/bin/env python3
"""English (LC002) ORDINARY Paper 2 — lettered text-block bespoke.

The OL P2 paper and its scheme mirror each other block for block: Section I
Single Text options "A AMERICANAH", "B THE HANDMAID'S TALE" …, Section II
Comparative modes "A RELATIONSHIPS" …, Section III poetry. Chips are per
lettered block with the title as the label ("Single Text A · Americanah"),
each opening the scheme block that restates that text's questions with
indicative material.

Usage: python3 english_p2_ol.py <years...>
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

SEC_RE = re.compile(r"\bSECTION\s+(I{1,3})\b", re.I)
# Lettered block header: a lone capital + an UPPERCASE title (≥4 chars)
BLOCK_RE = re.compile(r"^([A-H])\s+([A-Z][A-Z’'&.,\- ]{3,60})$")
SEC_NAMES = {"I": "Single Text", "II": "Comparative", "III": "Poetry"}


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


def blocks_of(doc, start_page, stop_page=None):
    """[(sec, letter, title, page0, y)] in print order, deduped."""
    out, sec = [], None
    stop = stop_page if stop_page is not None else len(doc)
    for pi in range(start_page, stop):
        for txt, x0, y in lines_of(doc[pi]):
            sm = SEC_RE.search(txt)
            if sm:
                sec = sm.group(1).upper()
                continue
            if sec is None:
                continue
            bm = BLOCK_RE.match(txt.strip())
            if not bm:
                # single-line mixed-case header with a title–author dash
                # ("A By the Bog of Cats – Marina Carr", often centred)
                m2 = re.match(r"^([A-H])\s+([A-Z][\w’'&.,!:()\u2010\- ]{2,60}\s+[–—-]\s+.{2,40})$", txt.strip())
                if not m2 and sec == "III":
                    # poetry blocks head with the poet's name alone
                    m2 = re.match(r"^([A-H])\s+([A-Z][a-z’']+(?:\s+[A-Z][\w’'.\-]+){1,3})$", txt.strip())
                if m2:
                    bm = m2
            if bm and x0 < 320:
                title = bm.group(2).strip().rstrip(" –-").title()
                out.append((sec, bm.group(1), title, pi, y))
        # the letter often sits on its OWN line beside the title line — pair a
        # lone capital with the next line's uppercase-led title at the same y
        ls = lines_of(doc[pi])
        for j, (txt, x0, y) in enumerate(ls):
            if sec is None or not re.fullmatch(r"[A-H]", txt.strip()) or x0 > 120:
                continue
            for txt2, x2, y2 in ls[j + 1:j + 3]:
                if abs(y2 - y) < 0.02 and re.match(r"^[A-Z]", txt2):
                    title = re.split(r"\s+[–-]\s+", txt2.strip())[0].rstrip(" –-").title()
                    out.append((sec, txt.strip(), title[:44], pi, y))
                    break
    return out


def scheme_p2_page(scheme):
    for pi in range(len(scheme)):
        t = scheme[pi].get_text()
        if re.search(r"Paper\s+(Two|II|2)\b.{0,60}Single\s+Text", t, re.S | re.I):
            return pi
    return None


def build(paper_path, scheme_path):
    paper, scheme = fitz.open(paper_path), fitz.open(scheme_path)
    S = len(scheme)
    pb = blocks_of(paper, 1)
    seenb, pb2 = set(), []
    for b in sorted(pb, key=lambda b: (b[3], b[4])):
        if (b[0], b[1]) not in seenb:
            seenb.add((b[0], b[1]))
            pb2.append(b)
    pb = pb2
    if len(pb) < 6:
        return None, f"too few paper blocks: {len(pb)}"
    p2 = scheme_p2_page(scheme)
    if p2 is None:
        return None, "no Paper Two start in scheme"
    sb = blocks_of(scheme, p2)
    smap = {}
    for sec, L, title, pi, y in sb:
        smap.setdefault((sec, L), (pi, y, title))
    missing = [(sec, L) for sec, L, *_ in pb if (sec, L) not in smap]
    if missing:
        return None, f"scheme blocks missing {missing[:6]}"
    # scheme blocks must be monotonic in the paper's block order
    pts = [smap[(sec, L)][:2] for sec, L, *_ in pb]
    if any(b <= a for a, b in zip(pts, pts[1:])):
        return None, "scheme blocks not monotonic in paper order"
    qs = []
    for i, (sec, L, title, p_pi, p_y) in enumerate(pb):
        sp, sy, _ = smap[(sec, L)]
        ep, ey = pts[i + 1] if i + 1 < len(pb) else (S, 0.0)
        segs = [{"p": sp + 1, "r": [0.0, round(sy, 4), 1.0, 1.0]}]
        for p in range(sp + 1, min(ep, sp + 6)):
            segs.append({"p": p + 1, "r": [0.0, 0.0, 1.0, 1.0]})
        if ep < sp + 6 and ey > 0.02:
            segs.append({"p": ep + 1, "r": [0.0, 0.0, 1.0, round(ey, 4)]})
        nxt = (pb[i + 1][3], pb[i + 1][4]) if i + 1 < len(pb) else (len(paper), 1.0)
        py1 = nxt[1] if nxt[0] == p_pi else 1.0
        qs.append({"n": str(i + 1), "pP": p_pi + 1,
                   "pY": [round(p_y, 4), round(py1, 4)],
                   "region": segs, "mode": "crop", "conf": 1.0,
                   "label": f"{SEC_NAMES.get(sec, sec)} {L} · {title[:36]}"})
    sidecar = {"v": SIDECAR_V, "paperFileid": os.path.basename(paper_path),
               "schemeFileid": os.path.basename(scheme_path),
               "component": "200", "band": [p2 + 1, S + 1],
               "copyright": COPYRIGHT, "q": qs}
    return sidecar, None


def main():
    years = [int(y) for y in sys.argv[1:]] or list(range(2010, 2027))
    ok = drop = 0
    for year in years:
        f = "LC002GLP200EV.pdf"
        s = "LC002GLP000EV.pdf"
        pp = os.path.join(CORPUS, "exampapers", str(year), f)
        sp = os.path.join(CORPUS, "markingschemes", str(year), s)
        if not (os.path.exists(pp) and os.path.exists(sp)):
            continue
        dst = os.path.join(ANSWERS, str(year), f"{f}.json")
        if os.path.exists(dst):
            continue
        sidecar, err = build(pp, sp)
        if sidecar is None:
            print(f"DROP {year}: {err}")
            drop += 1
            continue
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        json.dump(sidecar, open(dst, "w"), sort_keys=True, separators=(",", ":"))
        print(f"OK   {year}: {len(sidecar['q'])} blocks")
        ok += 1
    print(f"\nmapped {ok} · dropped {drop}")


if __name__ == "__main__":
    main()
