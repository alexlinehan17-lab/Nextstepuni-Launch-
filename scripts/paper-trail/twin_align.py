#!/usr/bin/env python3
# Copyright 2026 Nextstepuni
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Paper Trail — translated-twin ALIGNER: chip an Irish-edition paper from its
English twin's committed sidecar, by CONTENT, never by page identity.

Why: page-count borrowing is only safe when the twin is a page-for-page
translation, and the audit rounds proved most Irish schemes REFLOW — the same
answers land pages away (the Link Modules borrows and Construction 2010 were
deleted from the live bucket for exactly this). This tool treats the English
sidecar as a SPEC — which questions exist, in what order, and roughly where —
and re-anchors every chip independently on the Irish paper and Irish scheme by
finding that question's own printed marker (Ceist N / C.N / Q.N / N. / the
label's part token). A proportional position prior arbitrates duplicate
markers; strict ascent and full count-reconcile gate the result; any chip that
cannot anchor on BOTH sides drops the whole paper.

Link Modules' section-restart numbering rides the labels ("Section A · Q1"):
the marker searched is the intra-section number, fenced to begin after the
section's own header (Section/Roinn A|B|C) on each side.

Usage: python3 twin_align.py [--only LC462] [--dry-run]
       (reads the pair list from the twins.json census in the scratchpad)
"""
import argparse
import json
import os
import re
import sys

import fitz  # pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
CORPUS = os.path.join(REPO, "paper-trail-corpus")
ANSWERS_DIR = os.path.join(HERE, "answers")
TWINS = "/private/tmp/claude-501/-Users-alexlinehan/345a28d9-1b6f-47b5-829c-f6fca188a1e9/scratchpad/twins.json"
COPYRIGHT = "© State Examinations Commission"

MARKER = re.compile(
    r"^(?:Question|QUESTION|Ceist|CEIST|Pytanie|PYTANIE|[QC]\.?)\s*(\d{1,2})\b"
    r"|^(\d{1,2})\.(?:\s|$)")
SECTION_HDR = re.compile(r"^(?:Section|SECTION|Roinn|ROINN)\s+([A-C])\b")
LM_LABEL = re.compile(r"(?:Section|Roinn)\s+([A-C])\s*·\s*Q\.?\s*(\d{1,2})", re.I)


def lines_with_pos(page):
    W, H = page.rect.width, page.rect.height
    rows = {}
    for w in page.get_text("words"):
        rows.setdefault((w[5], w[6]), []).append(w)
    out = []
    for key in rows:
        ws = sorted(rows[key], key=lambda w: w[0])
        # The Music schemes weld their headings with non-breaking spaces
        # ("Ceist\xa01"); normalise so the marker regexes see plain text.
        # Clamp y: scanned pages can place words fractionally past the
        # MediaBox, and a 1.1 y poisons every rect derived from it.
        out.append((" ".join(w[4] for w in ws).replace("\xa0", " ").strip(),
                    ws[0][0] / W, min(1.0, max(0.0, min(w[1] for w in ws) / H))))
    out.sort(key=lambda t: (t[2], t[1]))
    return out


def harvest_markers(doc, xmax=0.55):
    """[(n, page1, y)] for every question-number marker, plus section fences.

    Returns (markers, sections) where sections = [(letter, page1, y)].
    """
    marks, sections = [], []
    for pi in range(len(doc)):
        for txt, x, y in lines_with_pos(doc[pi]):
            s = SECTION_HDR.match(txt)
            if s and x < 0.7:
                sections.append((s.group(1), pi + 1, y))
            if x > xmax:
                continue
            m = MARKER.match(txt)
            if m:
                n = int(m.group(1) or m.group(2))
                if 0 < n <= 30:
                    marks.append((n, pi + 1, y))
    return marks, sections


def section_fence(sections, letter, prior_pg, tol):
    cands = [(abs(pg - prior_pg), pg, y) for (L, pg, y) in sections if L == letter]
    cands = [c for c in cands if c[0] <= tol]
    return min(cands)[1:] if cands else None


def _wanted(chips, side):
    """[(marker_number, prior_page_key, fence_letter_or_None)] per chip.

    Sub-part chip specs ("Q1 (ii)") carry a main-question marker; consecutive
    chips sharing it are COARSENED later — here they just want the same marker.
    """
    out = []
    for ch in chips:
        lab = ch.get("label") or ""
        lm = LM_LABEL.search(lab)
        mq = re.search(r"Q\.?\s*(\d{1,2})\s*\(", lab)
        if lm:
            out.append((int(lm.group(2)), lm.group(1).upper()))
        elif mq:
            out.append((int(mq.group(1)), None))
        else:
            n = int(re.sub(r"\D", "", ch["n"]) or 0)
            if not n:
                return None
            out.append((n, None))
    return out


def align_side(chips, doc, ev_pages, side):
    """{chip_index: (page1, y)} — GLOBALLY optimal strict-ascending assignment.

    Greedy matching commits to the first plausible marker and dies later: the
    Accounting scheme numbers its workings tables, Business prints a cover
    contents list, and one bad early pick blocks every chip after it. This DP
    minimises total |page − prior| over all strictly-ascending assignments, so
    a decoy only wins if the WHOLE alignment is cheaper through it.
    """
    marks, sections = harvest_markers(doc)
    want = _wanted(chips, side)
    if want is None:
        return None
    scale = len(doc) / max(1, ev_pages)
    if any(f for _, f in want):
        # Section-restart papers (Link Modules): the fence resets the ascent
        # floor per section — the shape the greedy pass handles and the flat
        # strict-ascent DP cannot. Markers here must carry the C./Q. prefix:
        # the scheme numbers its ANSWER LIST ITEMS 1..7 inside every answer,
        # and a bare-number match anchored Section B's Q2 on a list item (the
        # render gate caught the off-by-one block).
        strict = re.compile(r"^(?:Question|Ceist|[QC]\.)\s*(\d{1,2})\b")
        smarks = []
        for pi in range(len(doc)):
            for txt, x, y in lines_with_pos(doc[pi]):
                if x > 0.55:
                    continue
                m = strict.match(txt)
                if m:
                    smarks.append((int(m.group(1)), pi + 1, y))
        marks = smarks
        out = {}
        after = (0, 0.0)
        cur = None
        for i, (n, fence) in enumerate(want):
            ev_pg = chips[i]["pP"] if side == "paper" else chips[i]["region"][0]["p"]
            prior = ev_pg * scale
            tol = max(3, int(len(doc) * 0.3))
            if fence and fence != cur:
                f = section_fence(sections, fence, prior, max(6, len(doc)))
                if f is None:
                    return None
                after = f
                cur = fence
            best = None
            for m, pg, y in marks:
                if m != n or (pg, y) <= after:
                    continue
                d = abs(pg - prior)
                if d <= tol and (best is None or d < best[0]):
                    best = (d, pg, y)
            if best is None:
                return None
            out[i] = (best[1], best[2])
            after = out[i]
        return out
    priors = []
    for ch in chips:
        ev_pg = ch["pP"] if side == "paper" else ch["region"][0]["p"]
        priors.append(ev_pg * scale)

    # Candidates per chip: same-number markers; a chip repeating the previous
    # marker (coarsened sub-parts) may REUSE the previous chip's position.
    cands = []
    for i, (n, fence) in enumerate(want):
        cs = [(pg, y) for (m, pg, y) in marks if m == n]
        if fence:
            f = section_fence(sections, fence, priors[i], max(4, len(doc)))
            if f:
                cs = [(pg, y) for (pg, y) in cs if (pg, y) > f]
        if not cs:
            return None
        cands.append(sorted(cs))

    INF = float("inf")
    # dp[i][j] = best cost using candidate j for chip i
    dp = [[INF] * len(c) for c in cands]
    back = [[-1] * len(c) for c in cands]
    for j, (pg, y) in enumerate(cands[0]):
        dp[0][j] = abs(pg - priors[0])
    for i in range(1, len(cands)):
        same_marker = want[i][0] == want[i - 1][0] and want[i][1] == want[i - 1][1]
        for j, (pg, y) in enumerate(cands[i]):
            for k, (ppg, py) in enumerate(cands[i - 1]):
                if dp[i - 1][k] == INF:
                    continue
                ok = (pg, y) > (ppg, py) or (same_marker and (pg, y) == (ppg, py))
                if not ok:
                    continue
                c = dp[i - 1][k] + abs(pg - priors[i])
                if c < dp[i][j]:
                    dp[i][j] = c
                    back[i][j] = k
    last = min(range(len(cands[-1])), key=lambda j: dp[-1][j])
    if dp[-1][last] == INF:
        return None
    out = {}
    j = last
    for i in range(len(cands) - 1, -1, -1):
        out[i] = cands[i][j]
        j = back[i][j]
    return out


def _thumb(page, w=36):
    """Normalised grayscale thumbnail as a flat float list (no numpy here)."""
    pm = page.get_pixmap(matrix=fitz.Matrix(w / max(1, page.rect.width),
                                            w / max(1, page.rect.width)),
                         colorspace=fitz.csGRAY)
    vals = list(pm.samples)
    n = len(vals)
    mean = sum(vals) / n
    var = sum((v - mean) ** 2 for v in vals) / n
    sd = var ** 0.5 or 1.0
    return ([(v - mean) / sd for v in vals], pm.height, pm.width)


def _corr(a, b):
    (av, ah, aw), (bv, bh, bw) = a, b
    h = min(ah, bh); w = min(aw, bw)
    s = 0.0
    for r in range(h):
        ao = r * aw; bo = r * bw
        row_a = av[ao:ao + w]; row_b = bv[bo:bo + w]
        s += sum(x * y for x, y in zip(row_a, row_b))
    return s / (h * w)


def image_page_map(ev_doc, iv_doc):
    """{ev_page1: iv_page1} by monotonic thumbnail correlation.

    For scanned Irish schemes with no text layer: the translation preserves
    every table, ledger and figure as graphics, so page identity is visible
    to a 40px grayscale thumbnail even when no text can be read. DP over a
    banded window keeps the mapping monotonic; a low-correlation match drops
    the pair rather than guessing.
    """
    et = [_thumb(ev_doc[i]) for i in range(len(ev_doc))]
    it = [_thumb(iv_doc[i]) for i in range(len(iv_doc))]
    n, m = len(et), len(it)
    band = max(4, abs(m - n) + 3)
    NEG = -1e9
    dp = [[NEG] * m for _ in range(n)]
    back = [[-1] * m for _ in range(n)]
    for j in range(m):
        if abs(j - 0) <= band:
            dp[0][j] = _corr(et[0], it[j])
    for i in range(1, n):
        prior = i * m / n
        for j in range(m):
            if abs(j - prior) > band:
                continue
            c = _corr(et[i], it[j])
            best = NEG
            arg = -1
            # non-strict: two English pages may share one Irish page (the
            # translation merged them), so k == j is a legal predecessor
            for k in range(max(0, j - band), j + 1):
                if dp[i - 1][k] > best:
                    best = dp[i - 1][k]
                    arg = k
            if best > NEG:
                dp[i][j] = best + c
                back[i][j] = arg
    j = max(range(m), key=lambda jj: dp[n - 1][jj])
    if dp[n - 1][j] <= NEG:
        return None, 0.0
    path = {}
    for i in range(n - 1, -1, -1):
        path[i + 1] = j + 1
        j = back[i][j]
        if j < 0 and i > 0:
            return None, 0.0
    mean = dp[n - 1][max(range(m), key=lambda jj: dp[n - 1][jj])] / n
    return path, mean


def align_side_image(chips, ev_doc, iv_doc, side):
    """Chip positions carried through an image page map (scanned twins)."""
    pmap, mean = image_page_map(ev_doc, iv_doc)
    if pmap is None or mean < 0.35:
        return None
    out = {}
    for i, ch in enumerate(chips):
        if side == "paper":
            pg = ch["pP"]
            if pg not in pmap:
                return None
            out[i] = (pmap[pg], ch["pY"][0])
        else:
            segs = []
            for seg in ch["region"]:
                if seg["p"] not in pmap:
                    return None
                # early-wave sidecars omit "r" for whole-page segments
                segs.append({"p": pmap[seg["p"]],
                             "r": list(seg.get("r", [0.0, 0.0, 1.0, 1.0]))})
            out[i] = segs
    return out


def build(pair, ev_sidecar):
    sid, year, level, label, ivdoc, ivsch = pair[:6]
    ppath = os.path.join(CORPUS, "exampapers", str(year), ivdoc)
    spath = os.path.join(CORPUS, "markingschemes", str(year), ivsch)
    if not (os.path.exists(ppath) and os.path.exists(spath)):
        return None, "corpus missing"
    paper, scheme = fitz.open(ppath), fitz.open(spath)
    ev = json.load(open(ev_sidecar))
    chips = ev["q"]
    ev_paper_pages = max(c["pP"] for c in chips)
    ev_scheme_pages = max(seg["p"] for c in chips for seg in c["region"])

    evdoc_name = os.path.basename(ev_sidecar)[:-5].replace("IV.pdf", "EV.pdf")
    ev_paper_path = os.path.join(CORPUS, "exampapers", str(year), ev["paperFileid"])
    ev_scheme_path = os.path.join(CORPUS, "markingschemes", str(year), ev["schemeFileid"])

    sparse_scheme = sum(len(scheme[i].get_text()) for i in range(len(scheme))) < 40 * len(scheme)
    sparse_paper = sum(len(paper[i].get_text()) for i in range(len(paper))) < 40 * len(paper)

    # Text alignment first; where it cannot reconcile — scanned twin, partial
    # text layer, welded markers — fall back to IMAGE page alignment against
    # the English documents, which sees the shared tables and figures even
    # when no text can be read.
    #
    # Three booklet families skip text alignment ENTIRELY: Accounting numbers
    # its workings tables, Business its true/false grids, Economics its
    # sub-items — decoys that text matching anchored chips on (both caught by
    # the render gate). Image alignment cannot be fooled by a printed number.
    force_image = ivdoc[:5] in {"LC032", "LC033", "LC034"}
    img_paper = img_scheme = None
    pa = None if (sparse_paper or force_image) else align_side(chips, paper, ev_paper_pages, "paper")
    if pa is None and os.path.exists(ev_paper_path):
        img_paper = align_side_image(chips, fitz.open(ev_paper_path), paper, "paper")
        pa = img_paper
    if pa is None:
        return None, "paper side would not reconcile (text and image)"
    sa = None if (sparse_scheme or force_image) else align_side(chips, scheme, ev_scheme_pages, "scheme")
    if sa is None and os.path.exists(ev_scheme_path):
        img_scheme = align_side_image(chips, fitz.open(ev_scheme_path), scheme, "scheme")
        sa = img_scheme
    if sa is None:
        return None, "scheme side would not reconcile (text and image)"

    q = []
    for i, ch in enumerate(chips):
        if img_scheme is not None:
            # regions carried through the page map, rects intact
            pg, y = pa[i]
            y_end = 1.0
            if i + 1 < len(chips) and pa[i + 1][0] == pg:
                y_end = pa[i + 1][1]
            nc = {"n": ch["n"], "conf": 1.0, "mode": "crop",
                  "pP": pg, "pY": [round(y, 4), round(y_end, 4)],
                  "region": sa[i]}
            if ch.get("label"):
                nc["label"] = ch["label"]
            q.append(nc)
            continue
        pg, y = pa[i]
        y_end = 1.0
        if i + 1 < len(chips) and pa[i + 1][0] == pg:
            y_end = pa[i + 1][1]
        spg, sy = sa[i]
        if i + 1 < len(chips):
            npg, ny = sa[i + 1]
        else:
            ev_len = len(set(seg["p"] for seg in ch["region"]))
            npg, ny = min(len(scheme), spg + ev_len - 1), 1.0
        region = []
        if npg == spg:
            region.append({"p": spg, "r": [0.0, round(max(0.0, sy - 0.012), 4),
                                           1.0, round(ny if ny > sy else 1.0, 4)]})
        else:
            region.append({"p": spg, "r": [0.0, round(max(0.0, sy - 0.012), 4), 1.0, 1.0]})
            for mid in range(spg + 1, npg):
                region.append({"p": mid, "r": [0.0, 0.0, 1.0, 1.0]})
            if i + 1 < len(chips) and ny > 0.04:
                region.append({"p": npg, "r": [0.0, 0.0, 1.0, round(ny, 4)]})
            elif i + 1 >= len(chips):
                region.append({"p": npg, "r": [0.0, 0.0, 1.0, 1.0]})
        nc = {"n": ch["n"], "conf": 1.0, "mode": "crop",
              "pP": pg, "pY": [round(y, 4), round(y_end, 4)], "region": region}
        if ch.get("label"):
            nc["label"] = ch["label"]
        q.append(nc)
    return {
        "v": 1, "paperFileid": ivdoc, "schemeFileid": ivsch,
        "component": ev.get("component", ""),
        "band": [1, len(scheme) + 1], "copyright": COPYRIGHT, "q": q,
    }, None


# Pairs the render gate REFUSED — regenerating them without fixing the cause
# would resurrect known-bad chips. Each entry names why.
REFUSED = {
    # EV sources are themselves mis-anchored (workings-table / grid decoys
    # from the early booklet-era waves) — both sides need rebuilding first.
    "LC032ALP000IV.pdf", "LC032GLP000IV.pdf",   # accounting
    "LC033ALP000IV.pdf", "LC033GLP000IV.pdf",   # business booklet era
    # Alignment matched a different section's like-numbered block on render.
    "LC004ALP000IV.pdf", "LC096ALP000IV.pdf",   # history / early-modern
    "LC462CLP000IV.pdf", "LC462CLPO00IV.pdf",   # link modules (list-item decoys)
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    pairs = json.load(open(TWINS))
    wrote = dropped = 0
    for pair in pairs:
        sid, year, level, label, ivdoc, ivsch = pair[:6]
        if args.only and not ivdoc.startswith(args.only):
            continue
        if ivdoc in REFUSED:
            continue
        evdoc = ivdoc.replace("IV.pdf", "EV.pdf").replace("O00IV", "000EV")
        ev_sidecar = os.path.join(ANSWERS_DIR, str(year), f"{evdoc}.json")
        if not os.path.exists(ev_sidecar):
            continue
        out = os.path.join(ANSWERS_DIR, str(year), f"{ivdoc}.json")
        if os.path.exists(out):
            continue
        sidecar, why = build(pair, ev_sidecar)
        tag = f"{sid} {year} {level}"
        if sidecar is None:
            print(f"DROP {tag} {ivdoc}: {why}")
            dropped += 1
            continue
        print(f"MAP  {tag} {ivdoc}: {len(sidecar['q'])} chips")
        if not args.dry_run:
            os.makedirs(os.path.dirname(out), exist_ok=True)
            with open(out, "w", encoding="utf-8") as fh:
                json.dump(sidecar, fh, ensure_ascii=False, sort_keys=True,
                          separators=(",", ":"))
            wrote += 1
    print(f"done: {wrote} written, {dropped} dropped")
    return 0


if __name__ == "__main__":
    sys.exit(main())
