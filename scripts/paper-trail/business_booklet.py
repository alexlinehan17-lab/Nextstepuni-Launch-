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
Paper Trail — Business HIGHER "Section 2 & 3" long-answer booklet (LC033ALP041EV),
2021–2025: SECTION-3-BANDED maps.

Why bespoke: the long booklet shares ONE scheme file (LC033ALP000EV) with the
Section 1 short-answer paper (LC033ALP032EV). The scheme is laid out as
  outline (marks breakdown, pp~4–13) → Section 1 detail (pp~14–20, answers
  numbered "1."–"10." at the left margin) → Section 2 ABQ detail → Section 3
  detail (Question 1–8, the long booklet's answers).
In 2020 the Section 3 detail headers are LEFT-MARGIN "Question N" lines, so the
generic engine mapped it (shipped in wave 8). From 2021 the SEC re-set those
headers as CENTERED MIXED-CASE "Question N" lines (2021/22/25) or dropped them
entirely in favour of a "Question | Possible Responses | Max. Mark" table whose
question number sits in the left column (2023/24). The engine's centered-header
detection only accepts UPPERCASE "QUESTION N", so its scheme-marker pass fell
through to the lead_int detector and reconciled the booklet's Q1–8 against
SECTION 1's "1."–"8." short-answer markers — a confident, monotonic and
completely WRONG map identical to the Section-1 sidecar's coords (2025 landed
on the Section 3 outline instead; 2023 dropped on count). Hence wave 8's
"the other long booklets reuse Section-1 coords and are dropped".

This generator pins the band to the SECTION 3 DETAIL divider (the first
top-of-page "Section 3" line AFTER the last "Section 2"/ABQ detail divider;
2025 has no such divider and anchors on the first centered "Question 1" after
the ABQ detail) and reconciles two marker shapes inside that band only:
  * centered standalone "Question N" header lines (2021, 2022, 2025), and
  * the table layout's left-column question number (2023, 2024) —
cross-checked against each other when both exist (2021 Q2–7 agree page-for-
page). 2021's missing "Question 1" header is pinned to the Section 3 divider
itself (its answer starts immediately under it — content-verified).

Safety posture identical to anchor-map.py / hem_history.py: COUNT RECONCILE —
every paper question (Q1–8) must land a strictly monotonic in-band marker or
the year drops. The last question extends only across consecutive non-blank
pages and stops before the marking-annotations appendix. Coordinates only,
sidecar schema v1. Never overwrites an existing sidecar (2020 is shipped).

Usage: python3 business_booklet.py         # maps corpus years, writes answers/<year>/
       python3 business_booklet.py --qa    # + full paper-question vs crop text dump
"""
import json
import os
import re
import sys

import fitz  # pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
CORPUS = os.path.join(REPO, "paper-trail-corpus")
ANSWERS_DIR = os.path.join(HERE, "answers")

SIDECAR_V = 1
COPYRIGHT = "© State Examinations Commission"
YEARS = range(2021, 2026)              # 2020 shipped in wave 8 — untouched
PAPER_FID = "LC033ALP041EV.pdf"
SCHEME_FID = "LC033ALP000EV.pdf"
MAX_TAIL_SPAN = 6                      # last question: max continuation pages
TOP_FRAC = 0.5                         # a divider line sits in the top half

# paper headers use a non-breaking space: 'Question\xa01'
PAPER_Q_RE = re.compile(r"^Question[\s\xa0]+(\d{1,2})\b")
CENTERED_Q_RE = re.compile(r"^Question[\s\xa0]+(\d{1,2})$")
TABLECOL_RE = re.compile(r"^(\d{1,2})(\s|$)")
SEC2_RE = re.compile(r"^SECTION\s*2\b|^Section\s*2\b")
SEC3_RE = re.compile(r"^SECTION\s*3\b|^Section\s*3\b")
ANNOTATIONS_RE = re.compile(r"annotations\s+used\s+for\s+marking", re.I)


def lines_with_pos(page):
    """[(text, x0, yFrac)] of every text line, top-to-bottom."""
    H = page.rect.height
    out = []
    for blk in page.get_text("dict")["blocks"]:
        if blk.get("type") != 0:
            continue
        for ln in blk.get("lines", []):
            txt = "".join(sp["text"] for sp in ln.get("spans", [])).strip()
            if txt:
                out.append((txt, ln["bbox"][0], ln["bbox"][1] / H))
    out.sort(key=lambda t: t[2])
    return out


def paper_headers(doc):
    """{n: (page0, yFrac)} for the booklet's left-margin 'Question N' headers,
    contiguous 1..N (N ≥ 7) and strictly monotonic, else None."""
    found = {}
    for pi in range(len(doc)):
        for t, x, y in lines_with_pos(doc[pi]):
            m = PAPER_Q_RE.match(t)
            if m and x < 140:
                n = int(m.group(1))
                if n not in found:
                    found[n] = (pi, y)
    ns = sorted(found)
    if len(ns) < 7 or ns != list(range(1, len(ns) + 1)):
        return None
    pts = [found[n] for n in ns]
    if not all(pts[i] < pts[i + 1] for i in range(len(pts) - 1)):
        return None
    return found


def section3_band_start(scheme):
    """(0-based page, divider yFrac or None) of the SECTION 3 DETAIL start.

    The scheme mentions 'Section 2'/'Section 3' twice (outline + detail), so the
    detail Section 3 is the first top-of-page 'Section 3' AFTER the LAST
    top-of-page 'Section 2' (the ABQ detail divider). 2025 carries no Section 3
    detail divider at all → (None, None); the caller anchors on 'Question 1'."""
    sec2_last = None
    for pi in range(len(scheme)):
        for t, x, y in lines_with_pos(scheme[pi]):
            if y >= TOP_FRAC:
                break
            if SEC2_RE.match(t):
                sec2_last = pi
    if sec2_last is None:
        return None, None, None
    for pi in range(sec2_last + 1, len(scheme)):
        for t, x, y in lines_with_pos(scheme[pi]):
            if y >= TOP_FRAC:
                break
            if SEC3_RE.match(t):
                return pi, y, sec2_last
    return None, None, sec2_last


def scheme_markers(scheme, start, want_ns):
    """{n: (page0, yFrac)} in [start, end): first centered standalone
    'Question N' header per n, cross-checked against the first left-column
    table question-number per n (both exist in 2021; only headers in 2022/25;
    only the table column in 2023/24). Returns (markers, err)."""
    centered, tablecol = {}, {}
    for pi in range(start, len(scheme)):
        for t, x, y in lines_with_pos(scheme[pi]):
            m = CENTERED_Q_RE.match(t)
            if m and 150 < x < 420:
                n = int(m.group(1))
                if n not in centered:
                    centered[n] = (pi, y)
            m = TABLECOL_RE.match(t)
            if m and x < 100:
                n = int(m.group(1))
                if n not in tablecol:
                    tablecol[n] = (pi, y)
    markers = {}
    for n in sorted(want_ns):
        c, tc = centered.get(n), tablecol.get(n)
        if c and tc:
            if c[0] != tc[0]:
                return None, (f"Q{n} centered header p{c[0] + 1} disagrees with "
                              f"table column p{tc[0] + 1}")
            markers[n] = min(c, tc)
        elif c or tc:
            markers[n] = c or tc
    return markers, None


def is_blank(page):
    return not page.get_text().strip()


def build_sidecar(paper_path, scheme_path):
    paper = fitz.open(paper_path)
    scheme = fitz.open(scheme_path)

    headers = paper_headers(paper)
    if headers is None:
        return None, "no clean 1..N left-margin 'Question N' run on the paper"
    want_ns = set(headers)
    N = max(want_ns)

    band_start, div_y, sec2_last = section3_band_start(scheme)
    if band_start is None:
        if sec2_last is None:
            return None, "no Section 2 (ABQ) detail divider in scheme"
        # 2025 shape: no Section 3 detail divider — anchor on 'Question 1'
        markers, err = scheme_markers(scheme, sec2_last + 1, want_ns)
        if err:
            return None, err
        if markers.get(1) is None:
            return None, "no Section 3 divider and no 'Question 1' header"
        band_start = markers[1][0]
        markers = {n: m for n, m in markers.items() if m >= (band_start, 0.0)}
    else:
        markers, err = scheme_markers(scheme, band_start, want_ns)
        if err:
            return None, err
        # 2021 shape: Q1's header is missing; its answer starts directly under
        # the Section 3 detail divider — pin Q1 to the divider line.
        if 1 not in markers and markers.get(2, (band_start, 0))[0] > band_start:
            markers[1] = (band_start, div_y)
        # Q1 marker on the divider page: start the crop at the divider line
        # (between them sit only the section title / table header rows).
        elif markers.get(1, (None,))[0] == band_start:
            markers[1] = (band_start, min(markers[1][1], div_y))

    if sorted(markers) != sorted(want_ns):
        missing = sorted(want_ns - set(markers))
        return None, f"count reconcile: no in-band marker for Q{missing}"
    pts = [markers[n] for n in sorted(want_ns)]
    if not all(pts[i] < pts[i + 1] for i in range(len(pts) - 1)):
        return None, "scheme markers not strictly monotonic"

    # last content page: stop before blank filler / the annotations appendix
    def usable(pi):
        return (pi < len(scheme) and not is_blank(scheme[pi])
                and not ANNOTATIONS_RE.search(scheme[pi].get_text()))

    qout = []
    for n in sorted(want_ns):
        p_pi, p_y = headers[n]
        nxt_same = min((y for m, (pp, y) in headers.items()
                        if pp == p_pi and y > p_y + 1e-6), default=1.0)
        s_pi, s_y = markers[n]
        if n < N:
            e_pi, e_y = markers[n + 1]
        else:
            e_pi = s_pi
            while e_pi - s_pi < MAX_TAIL_SPAN and usable(e_pi + 1):
                e_pi += 1
            e_y = 1.0
        region = []
        if e_pi == s_pi:
            region.append({"p": s_pi + 1, "r": [0.0, round(s_y, 4), 1.0, round(e_y, 4)]})
        else:
            region.append({"p": s_pi + 1, "r": [0.0, round(s_y, 4), 1.0, 1.0]})
            for mid in range(s_pi + 1, e_pi):
                if not is_blank(scheme[mid]):
                    region.append({"p": mid + 1, "r": [0.0, 0.0, 1.0, 1.0]})
            if e_y > 0.0 and not is_blank(scheme[e_pi]):
                region.append({"p": e_pi + 1, "r": [0.0, 0.0, 1.0, round(e_y, 4)]})
        qout.append({"n": str(n), "pP": p_pi + 1,
                     "pY": [round(p_y, 4), round(nxt_same, 4)],
                     "region": region, "mode": "crop", "conf": 1.0})

    return {
        "v": SIDECAR_V,
        "paperFileid": os.path.basename(paper_path),
        "schemeFileid": os.path.basename(scheme_path),
        "component": "",
        "band": [band_start + 1, len(scheme) + 1],
        "copyright": COPYRIGHT,
        "q": qout,
    }, None


def crop_text(scheme, q):
    parts = []
    for seg in q["region"]:
        pg = scheme[seg["p"] - 1]
        W, H = pg.rect.width, pg.rect.height
        x0, y0, x1, y1 = seg["r"]
        parts.append(pg.get_text("text", clip=fitz.Rect(x0 * W, y0 * H, x1 * W, y1 * H)))
    return "\n".join(parts)


def main():
    qa = "--qa" in sys.argv[1:]
    wrote = 0
    for year in YEARS:
        ppath = os.path.join(CORPUS, "exampapers", str(year), PAPER_FID)
        spath = os.path.join(CORPUS, "markingschemes", str(year), SCHEME_FID)
        if not (os.path.exists(ppath) and os.path.exists(spath)):
            print(f"SKIP {year}: paper/scheme not in corpus")
            continue
        out = os.path.join(ANSWERS_DIR, str(year), f"{PAPER_FID}.json")
        if os.path.exists(out):
            print(f"SKIP {year}: sidecar already committed ({out})")
            continue
        sidecar, reason = build_sidecar(ppath, spath)
        if sidecar is None:
            print(f"DROP {year} {PAPER_FID}: {reason}")
            continue
        paper, scheme = fitz.open(ppath), fitz.open(spath)
        for q in sidecar["q"]:
            seg = q["region"][0]
            pages = [s["p"] for s in q["region"]]
            t = crop_text(scheme, q)
            first = next((l.strip() for l in t.splitlines() if l.strip()), "")
            print(f"  {year} Q{q['n']} scheme pp{pages[0]}-{pages[-1]} starts: {first[:64]!r}")
            if qa:
                pg = paper[q["pP"] - 1]
                W, H = pg.rect.width, pg.rect.height
                y0, y1 = q["pY"]
                pt = pg.get_text("text", clip=fitz.Rect(0, y0 * H, W, y1 * H))
                print(f"    PAPER Q{q['n']} (p{q['pP']} y{q['pY']}):")
                for l in pt.splitlines():
                    if l.strip():
                        print(f"      | {l.strip()[:96]}")
                print(f"    SCHEME crop text (first 40 non-empty lines):")
                shown = 0
                for l in t.splitlines():
                    if l.strip():
                        print(f"      > {l.strip()[:96]}")
                        shown += 1
                        if shown >= 40:
                            break
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with open(out, "w", encoding="utf-8") as fh:
            json.dump(sidecar, fh, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"))
        print(f"WROTE {out}")
        wrote += 1
    print(f"done: {wrote} sidecars")
    return 0


if __name__ == "__main__":
    sys.exit(main())
