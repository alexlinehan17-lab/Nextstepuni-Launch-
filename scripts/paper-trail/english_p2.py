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
Paper Trail — English (LC002) HIGHER Paper 2: wave-8-shape literature maps.

Why bespoke: wave 8 shipped HL P2 for 2010 + 2012-2016 through the generic
engine, whose deduped greedy lead-int grammar lands on exactly four chips per
paper — Comparative Study option A questions 1-2 (the paper's first '1.'/'2.'
page) and Prescribed Poetry questions 3..N (poetry '1.'/'2.' dedupe away
against the comparative pair). 2011 and 2017-2025 were never mapped simply
because the corpus was never populated for those years (no scheme PDF ever
present); the schemes themselves kept the same shape throughout: the combined
P1+P2 scheme file echoes every P2 essay question verbatim, followed by an
indicative-material list and the grade-band criteria appendix.

This generator reproduces that wave-8 grammar EXPLICITLY (and is validated by
reproducing the five committed golden sidecars byte-for-byte before it is
allowed to write anything new):

  * PAPER: greedy monotonic '1.' .. 'N.' at the left margin across pages;
    markers 1-2 must sit on the COMPARATIVE STUDY page, markers 3..N on the
    PRESCRIBED POETRY page (N=4, or 5 in the 2021-2025 five-poet years).
  * SCHEME: the same greedy grammar restricted to the PAPER 2 half (first page
    whose head carries the uppercase 'PAPER 2' divider). The comparative pair
    resolves to option A's two blocks; poetry 3..N resolve to poets 3..N
    (poetry 1-2 dedupe away exactly as on the paper). 2023's scheme prints
    poetry Q5 as '5 "…' (no period) — a narrow number-then-quote fallback
    accepts it; content QA still gates it.
  * REGIONS mirror the engine: crop from marker to next marker; >6-page spans
    (always comparative Q2, whose block is followed by options B/C + the
    unseen poem) degrade to a conf-0.6 pagejump; the LAST question's crop runs
    one page past its marker page onto the CRITERIA FOR ASSESSMENT appendix
    (grade bands are part of an essay answer), guarded by requiring that
    appendix header on the trailing page.

Safety posture identical to anchor-map.py / hem_history.py: COUNT RECONCILE —
every paper question must land a monotonic in-band scheme block AND pass a
content QA gate (the scheme echoes each question verbatim, so the paper
question's own words must appear in its crop: token containment >= 0.6, plus
the verify_all first-marker invariant) or the whole paper drops. Coordinates
only, sidecar schema v1.

Usage: python3 english_p2.py            # golden parity check, then maps
                                        # 2011 + 2017-2025, writes answers/<year>/
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
COMPONENT = "200"
PAPER_FILEID = "LC002ALP200EV.pdf"
SCHEME_FILEID = "LC002ALP000EV.pdf"
LEAD_X = 95              # a 'N.' marker starts left of this (points)
MAX_REGION_PAGES = 6     # engine parity: longer crop spans degrade to pagejump
GOLDEN_YEARS = [2010, 2012, 2013, 2014, 2015, 2016]   # committed by wave 8 — compare only
TARGET_YEARS = [2011] + list(range(2017, 2027))        # this re-probe's scope
QA_MIN_OVERLAP = 0.6     # paper-question tokens that must reappear in the crop

# NOTE: 2023's scheme prints prescribed-poetry Q5 as '5        “A powerful …'
# (no period). page_leadints accepts number-then-quote ONLY as a fallback; the
# greedy expectation plus content QA keeps it from ever grabbing stray digits.
PAPER2_HEAD_RE = re.compile(r"PAPER\s*2\b")            # uppercase divider only
CRITERIA_RE = re.compile(r"CRITERIA\s+FOR\s+ASSESSMENT", re.I)
STOPWORDS = frozenset(
    "the and that this with your you for from are can our their his her its "
    "have has been each one two three texts text course comparative answer "
    "answers reference support discuss compare extent which what how why "
    "either both least other more than may must in on of to a an or is it "
    "not do does at by as be we".split())


def norm(s):
    return " ".join(s.replace("\xa0", " ").split())


def line_groups(page):
    """Words grouped into visual lines (engine parity: get_text('words')
    keyed by block/line number, sorted left-to-right)."""
    lines = {}
    for w in page.get_text("words"):
        lines.setdefault((w[5], w[6]), []).append(w)
    for lw in lines.values():
        lw.sort(key=lambda w: w[0])
    return list(lines.values())


def page_leadints(page):
    """[(n, x0, yFrac)] 'N.' lead-int markers on one page, y-sorted — the
    engine's _det_lead_int word grammar (y is the marker WORD's own bbox top,
    which is what the committed goldens carry), plus the narrow number-then-
    quote fallback for 2023's dotless poetry Q5."""
    H = page.rect.height
    out = []
    for lw in line_groups(page):
        w = lw[0]
        if w[0] >= LEAD_X:
            continue
        m = re.fullmatch(r"(\d{1,2})\.", w[4])
        if not m and len(lw) > 1 and lw[1][4][:1] in ("“", '"'):
            m = re.fullmatch(r"(\d{1,2})", w[4])
        if m:
            out.append((int(m.group(1)), w[0], w[1] / H))
    out.sort(key=lambda t: t[2])
    return out


def greedy_leadints(doc, start_pi=0, cap=None):
    """[(n, page0, yFrac)] greedy monotonic 1..N left-margin lead-int markers
    (the wave-8 dedupe grammar: only the FIRST occurrence of the next expected
    number counts; section-restart 1./2. runs dedupe away)."""
    seq, want = [], 1
    for pi in range(start_pi, len(doc)):
        for n, x, y in page_leadints(doc[pi]):
            if cap is not None and want > cap:
                return seq
            if n == want:
                seq.append((want, pi, y))
                want += 1
    return seq


def paper_headers(paper):
    """Wave-8 paper chips, validated against the P2 section grammar:
    markers 1-2 on the COMPARATIVE STUDY page, 3..N on the PRESCRIBED POETRY
    page. Returns (seq, reason)."""
    seq = greedy_leadints(paper)
    if len(seq) < 4:
        return None, f"paper greedy lead-int run too short ({len(seq)})"
    comp_pi = seq[0][1]
    if seq[1][1] != comp_pi:
        return None, "paper markers 1-2 not on one page"
    if "COMPARATIVE STUDY" not in norm(paper[comp_pi].get_text()).upper():
        return None, f"paper p{comp_pi + 1} (markers 1-2) is not the Comparative Study page"
    poet_pi = seq[2][1]
    if any(h[1] != poet_pi for h in seq[2:]):
        return None, "paper markers 3..N not on one page"
    if "PRESCRIBED POETRY" not in norm(paper[poet_pi].get_text()).upper():
        return None, f"paper p{poet_pi + 1} (markers 3..N) is not the Prescribed Poetry page"
    return seq, None


def scheme_p2_start(scheme):
    """0-based page of the uppercase 'PAPER 2' divider head (the scheme file
    covers P1 then P2)."""
    for pi in range(len(scheme)):
        head = norm(scheme[pi].get_text())[:150]
        if PAPER2_HEAD_RE.search(head):
            return pi
    return None


def engine_band(scheme):
    """Engine-parity sidecar band: first top-of-page search hit for 'Paper 2'
    (case-insensitive, like find_band) — on English this lands on the CRITERIA
    page's 'Paper 1 and Paper 2' sentence, so the committed goldens carry
    [3, len+1]. Reproduced verbatim for consistency."""
    for pi, page in enumerate(scheme):
        if page.rotation:
            continue
        H = page.rect.height
        for r in page.search_for("Paper 2"):
            if r.y0 < H * 0.5:
                return [pi + 1, len(scheme) + 1]
    return None


def crop_text(page, r):
    W, H = page.rect.width, page.rect.height
    return page.get_text("text", clip=fitz.Rect(r[0] * W, r[1] * H, r[2] * W, min(1.0, r[3]) * H))


def qa_tokens(txt):
    words = re.findall(r"[a-záéíóúà-ÿ’']+", norm(txt).lower())
    return {w for w in words if len(w) >= 4 and w not in STOPWORDS}


def first_marker(txt):
    """verify_all.py invariant: first lead-int/Question/Q-token marker in the
    crop, reading top to bottom."""
    for raw in txt.splitlines():
        ln = norm(raw)
        if not ln:
            continue
        m = re.search(r"\b(?:Question|QUESTION)\s+(\d{1,2})\b", ln)
        if m:
            return int(m.group(1))
        m = re.match(r"^(\d{1,2})[.:]", ln)
        if m:
            return int(m.group(1))
        m = re.search(r"\bQ\.?(\d{1,2})\b", ln)
        if m:
            return int(m.group(1))
    return None


def build_sidecar(paper_path, scheme_path):
    paper = fitz.open(paper_path)
    scheme = fitz.open(scheme_path)

    headers, reason = paper_headers(paper)
    if headers is None:
        return None, reason, []
    n_qs = len(headers)

    p2_pi = scheme_p2_start(scheme)
    if p2_pi is None:
        return None, "no uppercase 'PAPER 2' divider head in scheme", []
    markers = greedy_leadints(scheme, p2_pi, cap=n_qs)
    if [m[0] for m in markers] != list(range(1, n_qs + 1)):
        return None, (f"scheme markers do not reconcile 1..{n_qs} in the P2 half "
                      f"(got {[m[0] for m in markers]})"), []

    # last question's crop runs one page past its marker page onto the
    # criteria appendix (engine parity) — guard that the trailing page IS it
    last_pi = markers[-1][1]
    if last_pi + 1 >= len(scheme) or not CRITERIA_RE.search(scheme[last_pi + 1].get_text()):
        return None, "page after the last poetry block is not the criteria appendix", []

    qout, qa_log = [], []
    for i, (n, s_pi, s_y) in enumerate(markers):
        # paper chip band: marker to next marker on the same paper page
        _, p_pi, p_y = headers[i]
        nxt_same = [h for h in headers[i + 1:] if h[1] == p_pi]
        p_y1 = nxt_same[0][2] if nxt_same else 1.0
        base = {"n": str(n), "pP": p_pi + 1, "pY": [round(p_y, 4), round(p_y1, 4)]}

        # scheme region: marker to next marker; last runs onto the appendix page
        if i + 1 < len(markers):
            e_pi, e_y = markers[i + 1][1], markers[i + 1][2]
        else:
            e_pi, e_y = s_pi + 1, 1.0
        if e_pi - s_pi + 1 > MAX_REGION_PAGES:
            q = dict(base, conf=0.6, mode="pagejump", region=[{"p": s_pi + 1}])
        else:
            region = [{"p": s_pi + 1, "r": [0.0, round(s_y, 4), 1.0, 1.0]}]
            for mid in range(s_pi + 1, e_pi):
                if scheme[mid].get_text().strip():
                    region.append({"p": mid + 1, "r": [0.0, 0.0, 1.0, 1.0]})
            if e_y > 0.0 and scheme[e_pi].get_text().strip():
                region.append({"p": e_pi + 1, "r": [0.0, 0.0, 1.0, round(e_y, 4)]})
            q = dict(base, conf=1.0, mode="crop", region=region)
        qout.append(q)

        # CONTENT QA — the scheme echoes the question verbatim, so the paper
        # question's own tokens must reappear in the crop (pagejump: its page)
        p_txt = crop_text(paper[p_pi], [0.0, p_y, 1.0, p_y1])
        if q["mode"] == "pagejump":
            s_txt = scheme[s_pi].get_text()
        else:
            s_txt = "".join(crop_text(scheme[seg["p"] - 1], seg["r"]) for seg in q["region"])
        ptok, stok = qa_tokens(p_txt), qa_tokens(s_txt)
        ov = len(ptok & stok) / max(1, len(ptok))
        fm = first_marker(s_txt)
        qa_log.append((n, ov, fm, norm(p_txt)[:72], norm(s_txt)[:72]))
        if ov < QA_MIN_OVERLAP:
            return None, f"content QA fail Q{n}: crop overlap {ov:.2f} < {QA_MIN_OVERLAP}", qa_log
        if q["mode"] == "crop" and fm not in (n, None):
            return None, f"content QA fail Q{n}: first marker in crop is {fm}", qa_log

    band = engine_band(scheme)
    if band is None:
        return None, "no engine-parity band anchor", qa_log
    return {
        "v": SIDECAR_V,
        "paperFileid": os.path.basename(paper_path),
        "schemeFileid": os.path.basename(scheme_path),
        "component": COMPONENT,
        "band": band,
        "copyright": COPYRIGHT,
        "q": qout,
    }, None, qa_log


def dumps(sidecar):
    return json.dumps(sidecar, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def run_year(year, write):
    ppath = os.path.join(CORPUS, "exampapers", str(year), PAPER_FILEID)
    spath = os.path.join(CORPUS, "markingschemes", str(year), SCHEME_FILEID)
    if not (os.path.exists(ppath) and os.path.exists(spath)):
        print(f"SKIP {year}: paper/scheme not in corpus")
        return None
    sidecar, reason, qa_log = build_sidecar(ppath, spath)
    for n, ov, fm, ptxt, stxt in qa_log:
        print(f"  {year} Q{n} overlap={ov:.2f} firstMarker={fm}")
        print(f"       paper: {ptxt!r}")
        print(f"       crop : {stxt!r}")
    if sidecar is None:
        print(f"DROP {year}: {reason}")
        return None
    if write:
        ydir = os.path.join(ANSWERS_DIR, str(year))
        os.makedirs(ydir, exist_ok=True)
        out = os.path.join(ydir, f"{PAPER_FILEID}.json")
        with open(out, "w", encoding="utf-8") as fh:
            fh.write(dumps(sidecar))
        print(f"WROTE {out}")
    return sidecar


def main():
    # 1. GOLDEN PARITY — must reproduce every committed wave-8 sidecar
    #    byte-for-byte before anything new is written.
    ok = True
    for year in GOLDEN_YEARS:
        committed_path = os.path.join(ANSWERS_DIR, str(year), f"{PAPER_FILEID}.json")
        if not os.path.exists(committed_path):
            continue
        # Parity needs the golden year's corpus PDFs; on a machine holding only
        # the refresh year's corpus (annual refresh), absence is not a drop.
        if not (os.path.exists(os.path.join(CORPUS, "exampapers", str(year), PAPER_FILEID))
                and os.path.exists(os.path.join(CORPUS, "markingschemes", str(year), SCHEME_FILEID))):
            print(f"PARITY SKIP {year}: corpus not on this machine")
            continue
        committed = open(committed_path, encoding="utf-8").read().strip()
        sidecar = run_year(year, write=False)
        if sidecar is None:
            print(f"PARITY FAIL {year}: generator dropped a shipped year")
            ok = False
        elif dumps(sidecar) != committed:
            print(f"PARITY FAIL {year}: generated sidecar differs from committed")
            ok = False
        else:
            print(f"PARITY OK {year}")
    if not ok:
        print("golden parity failed — refusing to write new sidecars")
        return 1

    # 2. TARGET YEARS
    wrote = 0
    for year in TARGET_YEARS:
        if run_year(year, write=True) is not None:
            wrote += 1
    print(f"done: {wrote} sidecars")
    return 0


if __name__ == "__main__":
    sys.exit(main())
