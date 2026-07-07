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
Paper Trail — Link Modules (LCVP, LC462): SECTION-RESTART Q-token maps.

Why bespoke (COVERAGE.md: "needs per-subject grammar"): the paper numbers its
questions per SECTION — Section A (Audio Visual) Q.1–Q.8, Section B (Case
Study) Q.1–Q.3, Section C (General Questions) Q.1–Q.6/7 — so the generic
engine's single monotonic 1..N gate can never reconcile it. The marking scheme
mirrors the identical Section A/B/C + `Q.n` block structure (and mostly repeats
the question text verbatim), so a wave10-style section-anchored map is exact.

Grammar wrinkles handled here:
  * The paper prints Section C's numbers up to three times: a menu list
    ("answer any …"), the full questions with answer space, and (pre-2018) an
    examiner marks grid on the back page. Numbering restarts split the
    section's markers into PASSES; chips anchor on the pass that spans the
    most pages — the full-question pages (menu and grid each collapse onto
    one or two pages).
  * Multi-part questions repeat their marker ("Q.7 (i)", "Q.7 (ii)"): a
    marker equal to the last accepted number is a continuation and is ignored.
  * Some schemes embed the Section C menu inside an answer (2019 p10). A page
    where the section's numbering RESTARTS (a lower number after real
    answers) is blacklisted as an embedded menu/table page.
  * `n` must stay globally sequential/unique (types/paperTrail.ts), so chips
    carry `label: "Section X · Q n"` like the shipped language sidecars.
    (This also means verify_all.py's strict first-marker==n screen reports the
    B/C chips as mismatches by construction, exactly as it does for the shipped
    French/German section-restart maps — the QA gate for this subject is the
    paper-text↔crop-text echo check this script prints.)

Safety: COUNT RECONCILE per section — every paper question in every section
must land a monotonic in-band scheme block or the whole paper is DROPPED.
Coordinates only, sidecar schema v1.

Usage: python3 link_modules.py          # maps corpus years, writes answers/<year>/
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
FILEID = "LC462CLP000EV.pdf"
# 2016/2017 papers were archived under a letter-O component fileid
# (LC462CLPO00EV.pdf) while their schemes use the usual zero form.
PAPER_FILEID_BY_YEAR = {2016: "LC462CLPO00EV.pdf", 2017: "LC462CLPO00EV.pdf"}
YEARS = range(2010, 2026)
MARK_X = 200          # section headers / Q tokens start left of this (points)
MAX_REGION_PAGES = 6

SEC_RE = re.compile(r"^Section\s+([ABC])\b")
Q_RE = re.compile(r"^Q\.?\s?(\d{1,2})\*?[.:]?(\s|$)")


def lines_with_pos(page):
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


def is_blank(page):
    t = page.get_text().strip()
    return (not t) or re.fullmatch(r"\d{1,3}(\s+Blank\s+Page)?", " ".join(t.split()), re.I) is not None


def walk(doc, header_top_only):
    """Linear walk → (markers, section_pages).
    markers: [(sec, n, page0, yFrac, text)] in reading order, only after the
    Section A header. section_pages: {sec: (page0, yFrac)} first header hit."""
    markers, sections = [], {}
    order = "ABC"
    cur = None
    for pi in range(len(doc)):
        for t, x, y in lines_with_pos(doc[pi]):
            if x >= MARK_X:
                continue
            m = SEC_RE.match(t)
            if m and "and Section" not in t:
                sec = m.group(1)
                want = order[len(sections)] if len(sections) < 3 else None
                if sec == want and (not header_top_only or y < 0.2):
                    sections[sec] = (pi, y)
                    cur = sec
                continue
            if cur is None:
                continue
            q = Q_RE.match(t)
            if q:
                markers.append((cur, int(q.group(1)), pi, y, t))
    return markers, sections


def paper_anchors(doc):
    """{(sec,n): (page0,yFrac,text)} choosing, per section, the marker PASS
    that spans the most distinct pages (full-question pages beat the menu and
    the marks grid). Continuations ("Q.7 (ii)" after "Q.7 (i)") are ignored.
    None if any section lacks a clean 1..N pass."""
    markers, sections = walk(doc, header_top_only=True)
    if len(sections) != 3:
        return None, "paper: Section A/B/C headers not found"
    out = {}
    for sec in "ABC":
        secm = [m for m in markers if m[0] == sec]
        passes, cur = [], []
        for _, n, pi, y, t in secm:
            if cur and n == cur[-1][0]:
                continue                      # continuation marker
            if n == len(cur) + 1:
                cur.append((n, pi, y, t))
            elif n < len(cur) + 1:
                passes.append(cur)            # restart → new pass
                cur = [(n, pi, y, t)] if n == 1 else []
            else:
                return None, f"paper: Section {sec} jumps to Q{n} after Q{len(cur)}"
        passes.append(cur)
        complete = [p for p in passes if p and p[0][0] == 1]
        if not complete:
            return None, f"paper: Section {sec} has no 1..N pass"
        want_n = max(len(p) for p in complete)
        complete = [p for p in complete if len(p) == want_n]
        best = max(complete, key=lambda p: (len({pi for _, pi, _, _ in p}),
                                            complete.index(p)))
        pts = [(pi, y) for _, pi, y, _ in best]
        if any(pts[i] >= pts[i + 1] for i in range(len(pts) - 1)):
            return None, f"paper: Section {sec} anchors not monotonic"
        for n, pi, y, t in best:
            out[(sec, n)] = (pi, y, t)
    return out, None


def scheme_blocks(doc, want):
    """{(sec,n): (page0,yFrac,text)} from the scheme walk with the embedded-menu
    page blacklist; must exactly reconcile with `want` (the paper's set).
    Returns (blocks, orderedKeys, err)."""
    markers, sections = walk(doc, header_top_only=False)
    if len(sections) != 3:
        return None, None, "scheme: Section A/B/C headers not found"
    blocks, ordered = {}, []
    count = {"A": 0, "B": 0, "C": 0}
    bad_pages = set()
    for sec, n, pi, y, t in markers:
        if (sec, pi) in bad_pages:
            continue
        if n == count[sec] + 1:
            blocks[(sec, n)] = (pi, y, t)
            ordered.append((sec, n))
            count[sec] += 1
        elif n == count[sec]:
            continue                          # continuation ("Q.7 (ii)")
        elif n < count[sec]:
            # numbering restarts mid-section → embedded menu/summary page:
            # drop everything on this page (incl. any already-accepted marker
            # from it) and never trust the page again.
            bad_pages.add((sec, pi))
            for k in [k for k in ordered if blocks[k][0] == pi and k[0] == sec]:
                ordered.remove(k)
                del blocks[k]
                count[sec] -= 1
        else:
            return None, None, f"scheme: Section {sec} jumps to Q{n} after Q{count[sec]}"
    if set(blocks) != set(want):
        missing = sorted(set(want) - set(blocks))
        extra = sorted(set(blocks) - set(want))
        return None, None, f"scheme: reconcile failed (missing {missing}, extra {extra})"
    pts = [blocks[k][:2] for k in ordered]
    if any(pts[i] >= pts[i + 1] for i in range(len(pts) - 1)):
        return None, None, "scheme: accepted blocks not monotonic"
    return blocks, ordered, None


def build_sidecar(paper_path, scheme_path):
    paper = fitz.open(paper_path)
    scheme = fitz.open(scheme_path)

    anchors, err = paper_anchors(paper)
    if err:
        return None, err
    blocks, ordered, err = scheme_blocks(scheme, set(anchors))
    if err:
        return None, err

    # paper y-band ends (next anchor on the same paper page, else page bottom)
    by_page = {}
    for (sec, n), (pi, y, t) in anchors.items():
        by_page.setdefault(pi, []).append(y)
    for pi in by_page:
        by_page[pi].sort()

    qout = []
    seq = 0
    for i, key in enumerate(ordered):
        sec, n = key
        s_pi, s_y, _ = blocks[key]
        if i + 1 < len(ordered):
            e_pi, e_y = blocks[ordered[i + 1]][:2]
        else:
            e_pi = s_pi
            while (e_pi + 1 < len(scheme) and e_pi - s_pi < MAX_REGION_PAGES - 1
                   and not is_blank(scheme[e_pi + 1])):
                e_pi += 1
            e_y = 1.0
        if e_pi - s_pi > MAX_REGION_PAGES:
            return None, f"scheme: Section {sec} Q{n} region spans {e_pi - s_pi + 1} pages"
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

        p_pi, p_y, _ = anchors[key]
        nxt = next((yy for yy in by_page[p_pi] if yy > p_y + 1e-6), 1.0)
        seq += 1
        qout.append({"n": str(seq), "label": f"Section {sec} · Q{n}",
                     "pP": p_pi + 1, "pY": [round(p_y, 4), round(nxt, 4)],
                     "region": region, "mode": "crop", "conf": 1.0})

    return {
        "v": SIDECAR_V,
        "paperFileid": os.path.basename(paper_path),
        "schemeFileid": os.path.basename(scheme_path),
        "component": "",
        "band": [1, len(scheme) + 1],
        "copyright": COPYRIGHT,
        "q": qout,
    }, None


def qa_echo(paper_path, scheme_path, sidecar):
    """Print paper-question text beside the crop's opening text for eyeballing."""
    paper, scheme = fitz.open(paper_path), fitz.open(scheme_path)
    for q in sidecar["q"]:
        pg = paper[q["pP"] - 1]
        W, H = pg.rect.width, pg.rect.height
        pt = pg.get_text(clip=fitz.Rect(0, q["pY"][0] * H, W, min(q["pY"][0] + 0.08, 1) * H))
        pt = " ".join(pt.split())[:58]
        seg = q["region"][0]
        sg = scheme[seg["p"] - 1]
        W, H = sg.rect.width, sg.rect.height
        x0, y0, x1, y1 = seg["r"]
        st = sg.get_text(clip=fitz.Rect(x0 * W, y0 * H, x1 * W, min(y0 + 0.08, y1) * H))
        st = " ".join(st.split())[:58]
        print(f"    {q['label']:<16} paper: {pt!r}")
        print(f"    {'':<16} crop : {st!r}")


def main():
    wrote = 0
    for year in YEARS:
        paper_fid = PAPER_FILEID_BY_YEAR.get(year, FILEID)
        ppath = os.path.join(CORPUS, "exampapers", str(year), paper_fid)
        spath = os.path.join(CORPUS, "markingschemes", str(year), FILEID)
        if not (os.path.exists(ppath) and os.path.exists(spath)):
            continue
        sidecar, reason = build_sidecar(ppath, spath)
        if sidecar is None:
            print(f"DROP {year}: {reason}")
            continue
        print(f"MAP  {year}: {len(sidecar['q'])} questions")
        qa_echo(ppath, spath, sidecar)
        ydir = os.path.join(ANSWERS_DIR, str(year))
        os.makedirs(ydir, exist_ok=True)
        with open(os.path.join(ydir, f"{paper_fid}.json"), "w", encoding="utf-8") as fh:
            json.dump(sidecar, fh, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"))
        wrote += 1
    print(f"done: {wrote} sidecars")
    return 0


if __name__ == "__main__":
    sys.exit(main())
