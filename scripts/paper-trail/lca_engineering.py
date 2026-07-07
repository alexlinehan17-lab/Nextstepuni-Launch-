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
Paper Trail — LCA Engineering (LB836): Q-token maps for the written exam.

Why bespoke (AUDIT-2026-07: record REFUTED — this is a WRITTEN 240-mark exam,
not "visual/drawing"): the scheme is an answered copy of the paper with the
identical page grammar — Section 1 Q1–Q3 short/structured answers, Section 2
Q4–Q7 structured questions, and Q7's five choose-two topic pages "Q7 (a)"…
"Q7 (e)" — so a marker-to-marker map is exact. The generic engine can't take
it because the question marker is fused into a section header line on most
years ("Section 1  Q1.") and Q7's topics repeat the Q7 number.

Grammar (verified identical on all 14 EV scheme years, 2011–2019 + 2021–2025):
  * Marker line, left column (x < 200): `Section N  Qn.` (2011–2024, one fused
    line) or a bare `Qn.` beside a separate `Section N` line (2025).
  * Q7's topics print `Q7 (a) <Topic Name>` … `Q7 (e) <Topic Name>` — one page
    per topic on BOTH sides. They are mapped as their own chips (n=8..12 with
    a `Q7 (x) · <name>` label per types/paperTrail.ts) because Q7's own page
    is just the topic menu; the Q7 chip maps menu page → scheme menu page.

Safety (a wrong region is the worst failure — drop, never guess):
  * Both sides must yield EXACTLY Q1..Q7 once each, in order, page-monotonic,
    plus EXACTLY topics (a)..(e) after Q7 — any other shape drops the year.
  * Inline `Section N` prefixes, where fused, must agree with the fixed
    Q1–3 → Section 1 / Q4–7 → Section 2 split, or the year drops.
  * Topic NAMES are string-reconciled paper↔scheme per letter — a mismatch
    drops the year (guards against a re-ordered topic menu).
  * The last topic's answer must fit its own page: every scheme page after
    Q7 (e) must be junk (blank, or a stray `Page N of M` footer page, as on
    the 2011/2012 schemes) or the year drops.

Coordinates only, sidecar schema v1.

Usage: python3 lca_engineering.py        # maps corpus years, writes answers/<year>/
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
FILEID = "LB836CLP000EV.pdf"
YEARS = range(2010, 2026)
MARK_X = 200          # marker lines start left of this (points)
N_QUESTIONS = 7       # Section 1 Q1–Q3 + Section 2 Q4–Q7, every verified year
TOPICS = "abcde"      # Q7's five choose-two topics, every verified year
MAX_REGION_PAGES = 5  # widest real region is Q1 (scheme pp.4–7)

# `Section 1  Q1.` / `Q1.` / `Section 2  Q7 (a) Computer Aided Design (CAD)`.
# The topic name may be an empty tail: some years (2013) emit it as a separate
# same-y text line, recovered by same_y_name().
MARK_RE = re.compile(
    r"^(?:Section\s+(\d)\s+)?Q\.?\s*(\d{1,2})\s*"
    r"(?:\.\s*$|\(([a-z])\)\s*(.*)$)"
)
MARKS_RE = re.compile(r"^\d{1,3}\s*marks?$", re.I)
JUNK_RE = re.compile(r"^(?:Page\s+\d+\s+of\s+\d+|\d{1,3}(?:\s+Blank\s+Page)?)$", re.I)


def lines_with_pos(page):
    H = page.rect.height
    out = []
    for blk in page.get_text("dict")["blocks"]:
        if blk.get("type") != 0:
            continue
        for ln in blk.get("lines", []):
            txt = " ".join("".join(sp["text"] for sp in ln.get("spans", [])).split())
            if txt:
                out.append((txt, ln["bbox"][0], ln["bbox"][1] / H))
    out.sort(key=lambda t: t[2])
    return out


def is_junk(page):
    t = " ".join(page.get_text().split())
    return (not t) or JUNK_RE.fullmatch(t) is not None


def norm_topic(s):
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


def same_y_name(lines, marker_y, marker_x):
    """Topic name emitted as its own text line (2013): the non-marks line
    sitting on the marker's row, right of the marker."""
    cands = [t for t, x, y in lines
             if abs(y - marker_y) < 0.008 and x > marker_x
             and not MARKS_RE.match(t) and not MARK_RE.match(t)]
    return cands[0] if len(cands) == 1 else None


def walk(doc):
    """Linear walk → validated anchors, or (None, err).

    Returns {key: (page0, yFrac, text)} for keys 1..7 (questions) and
    ("t", letter, normName) (Q7 topics), plus the ordered key list."""
    anchors, ordered = {}, []
    qn = 0            # questions accepted so far
    topics = []       # letters accepted so far
    for pi in range(len(doc)):
        page_lines = lines_with_pos(doc[pi])
        for t, x, y in page_lines:
            if x >= MARK_X:
                continue
            m = MARK_RE.match(t)
            if not m:
                continue
            sec, n, letter, name = m.group(1), int(m.group(2)), m.group(3), m.group(4)
            if letter is not None and not (name or "").strip():
                name = same_y_name(page_lines, y, x)
                if name is None:
                    return None, None, f"topic ({letter}) p{pi + 1}: name not found"
                t = f"{t} {name}"
            if letter is None:
                if n != qn + 1:
                    return None, None, f"Q{n} after Q{qn} (expected Q{qn + 1})"
                if topics:
                    return None, None, f"Q{n} after topic pages"
                want_sec = "1" if n <= 3 else "2"
                if sec is not None and sec != want_sec:
                    return None, None, f"Q{n} under Section {sec}"
                qn = n
                key = n
            else:
                if n != N_QUESTIONS or qn != N_QUESTIONS:
                    return None, None, f"topic ({letter}) on Q{n} after Q{qn}"
                if len(topics) >= len(TOPICS) or letter != TOPICS[len(topics)]:
                    return None, None, f"topic ({letter}) out of order after {topics}"
                if sec is not None and sec != "2":
                    return None, None, f"topic ({letter}) under Section {sec}"
                topics.append(letter)
                key = ("t", letter, norm_topic(name))
            anchors[key] = (pi, y, t)
            ordered.append(key)
    if qn != N_QUESTIONS:
        return None, None, f"found {qn} questions, expected {N_QUESTIONS}"
    if len(topics) != len(TOPICS):
        return None, None, f"found {len(topics)} Q7 topics, expected {len(TOPICS)}"
    pts = [anchors[k][:2] for k in ordered]
    if any(pts[i] >= pts[i + 1] for i in range(len(pts) - 1)):
        return None, None, "anchors not page-monotonic"
    return anchors, ordered, None


def topic_display(text):
    """`Section 2  Q7 (a) Computer Aided Design (CAD)` → `(a) · Computer Aided Design (CAD)`."""
    m = re.search(r"Q\.?\s*\d+\s*\(([a-z])\)\s*(.+)$", text)
    return f"Q7 ({m.group(1)}) · {m.group(2).strip()}"


def build_sidecar(paper_path, scheme_path):
    paper = fitz.open(paper_path)
    scheme = fitz.open(scheme_path)

    p_anchors, p_ordered, err = walk(paper)
    if err:
        return None, f"paper: {err}"
    s_anchors, s_ordered, err = walk(scheme)
    if err:
        return None, f"scheme: {err}"

    # count + topic-name reconcile: both sides must expose the identical keys
    # in the identical order (topic keys embed the normalised topic name).
    if p_ordered != s_ordered:
        return None, (f"reconcile failed (paper {p_ordered} != scheme {s_ordered})")

    # last topic's answer must fit its own page: everything after it is junk
    last_pi = s_anchors[s_ordered[-1]][0]
    for pi in range(last_pi + 1, len(scheme)):
        if not is_junk(scheme[pi]):
            return None, f"scheme: non-junk page p{pi + 1} after last topic page p{last_pi + 1}"

    qout = []
    for i, key in enumerate(s_ordered):
        s_pi, s_y, s_txt = s_anchors[key]
        if i + 1 < len(s_ordered):
            e_pi, e_y = s_anchors[s_ordered[i + 1]][:2]
        else:
            e_pi, e_y = s_pi, 1.0        # last topic: single page (guarded above)
        if e_pi - s_pi > MAX_REGION_PAGES:
            return None, f"scheme: {key} region spans {e_pi - s_pi + 1} pages"
        region = []
        if e_pi == s_pi:
            region.append({"p": s_pi + 1, "r": [0.0, round(s_y, 4), 1.0, round(e_y, 4)]})
        else:
            region.append({"p": s_pi + 1, "r": [0.0, round(s_y, 4), 1.0, 1.0]})
            for mid in range(s_pi + 1, e_pi):
                if not is_junk(scheme[mid]):
                    region.append({"p": mid + 1, "r": [0.0, 0.0, 1.0, 1.0]})
            if e_y > 0.0 and not is_junk(scheme[e_pi]):
                region.append({"p": e_pi + 1, "r": [0.0, 0.0, 1.0, round(e_y, 4)]})

        p_pi, p_y, p_txt = p_anchors[key]
        # next anchor on the same paper page ends the band (never happens on
        # these one-question-per-page papers, but stay correct if it did)
        nxt = 1.0
        if i + 1 < len(p_ordered) and p_anchors[p_ordered[i + 1]][0] == p_pi:
            nxt = p_anchors[p_ordered[i + 1]][1]
        q = {"n": str(i + 1), "pP": p_pi + 1,
             "pY": [round(p_y, 4), round(nxt, 4)],
             "region": region, "mode": "crop", "conf": 1.0}
        if isinstance(key, tuple):
            q["label"] = topic_display(p_txt)   # printed number lives in label
        qout.append(q)

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
        pt = pg.get_text(clip=fitz.Rect(0, q["pY"][0] * H, W, min(q["pY"][0] + 0.09, 1) * H))
        pt = " ".join(pt.split())[:58]
        seg = q["region"][0]
        sg = scheme[seg["p"] - 1]
        W, H = sg.rect.width, sg.rect.height
        x0, y0, x1, y1 = seg["r"]
        st = sg.get_text(clip=fitz.Rect(x0 * W, y0 * H, x1 * W, min(y0 + 0.09, y1) * H))
        st = " ".join(st.split())[:58]
        lab = q.get("label", f"Q{q['n']}")
        print(f"    {lab[:34]:<34} paper: {pt!r}")
        print(f"    {'':<34} crop : {st!r}")


def main():
    wrote = 0
    for year in YEARS:
        ppath = os.path.join(CORPUS, "exampapers", str(year), FILEID)
        spath = os.path.join(CORPUS, "markingschemes", str(year), FILEID)
        if not (os.path.exists(ppath) and os.path.exists(spath)):
            continue
        sidecar, reason = build_sidecar(ppath, spath)
        if sidecar is None:
            print(f"DROP {year}: {reason}")
            continue
        print(f"MAP  {year}: {len(sidecar['q'])} chips")
        qa_echo(ppath, spath, sidecar)
        ydir = os.path.join(ANSWERS_DIR, str(year))
        os.makedirs(ydir, exist_ok=True)
        with open(os.path.join(ydir, f"{FILEID}.json"), "w", encoding="utf-8") as fh:
            json.dump(sidecar, fh, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"))
        wrote += 1
    print(f"done: {wrote} sidecars")
    return 0


if __name__ == "__main__":
    sys.exit(main())
