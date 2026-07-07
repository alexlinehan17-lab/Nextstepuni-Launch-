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
Paper Trail — Engineering (LC027) dropped-year re-probe:
HIGHER EV {2010–2014, 2016–2020} and ORDINARY EV {2012, 2017, 2022}.

Why bespoke: wave 7's generic engine drops these years at COUNT RECONCILE
(typically 5/8 HL, 6/7 OL) because of two scheme-side quirks the shipped
2015/2021+ schemes don't trip on:

  * the scheme's "Page 2" is a MARK-ALLOCATION GRID ("Question 3 – 50 marks" …
    "Question 1 Section A – 50 marks") whose left-margin 'Question N' tokens
    hand _marker_map a poisoned monotonic start (1→3→6→7→8 in 2017 HL), and
  * the REAL per-question headers are unreachable to _marker_map's one-x-bucket
    scan: HL prints the Question 1 answer-page header as the FUSED token
    'Question1' (no space — invisible to _det_question_word; 2015 prints
    'Question 1' and passes), and the OL headers' x positions jitter 31–99 pt
    within one scheme (beyond HEADER_X_TOL's single-bucket reach: 2022 OL has
    Q1 at x=31 and Q2–Q7 at x=72–85).

Deterministic fix (scheme side only; the papers already parse cleanly):

  1. Anchor the marker band at the 'Sample Answers and Marking Scheme' page —
     everything before it (cover, note-to-teachers, MARKING SCHEME title, the
     marks grid) is blacklisted. Every target year prints this title verbatim.
  2. Scan that band for HEADERISH question markers: a line whose FIRST word is
     'Question'/'QUESTION' + integer, or the fused 'QuestionN', at the left
     margin, on a short (≤6-word) line. First occurrence per number; no
     x-bucket restriction.

Everything else — COUNT RECONCILE (every paper question must land a marker),
the monotonic gate, paper/scheme spread guards, the practical-marking-scheme
tail boundary, blank/rotation checks and crop assembly — is anchor-map.py's
map_paper, imported via importlib with ONLY detect_scheme_markers overridden
in memory (anchor-map.py itself is untouched). Papers that don't fully
reconcile still drop.

This script NEVER writes into scripts/paper-trail/answers/ — it stages
sidecars into --out, prints a QA echo (scheme marker line + first crop lines
per question), and the staged sidecars are copied into answers/ by hand only
after per-question content QA.

Usage: python3 engineering_years.py --out /path/to/staging
"""
import argparse
import importlib.util
import json
import os
import re
import sys

import fitz  # pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
CORPUS = os.path.join(REPO, "paper-trail-corpus")

# Load the frozen wave-7 engine without touching it.
_spec = importlib.util.spec_from_file_location("anchor_map", os.path.join(HERE, "anchor-map.py"))
am = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(am)

SAMPLE_ANSWERS_TITLE = "sample answers and marking scheme"
QHEAD_MAX_WORDS = 6      # 'Question 2 (45 Marks)' etc. — real headers are short lines
QHEAD_FUSED = re.compile(r"(?:Question|QUESTION)(\d{1,2})[.:]?")
QHEAD_NUM = re.compile(r"(\d{1,2})[.:]?")

TARGETS = {
    "LC027ALP000EV.pdf": [2010, 2011, 2012, 2013, 2014, 2016, 2017, 2018, 2019, 2020],
    "LC027GLP000EV.pdf": [2012, 2017, 2022],
}


def sample_answers_page(scheme, band_start, band_end):
    """0-based page of the 'Sample Answers and Marking Scheme' title, else None."""
    for pi in range(band_start, band_end):
        if SAMPLE_ANSWERS_TITLE in am._norm_match(scheme[pi].get_text("text")):
            return pi
    return None


def lc027_scheme_markers(doc, band_start, band_end, want_ns, paper_det=None):
    """detect_scheme_markers override: headerish 'Question N' / fused 'QuestionN'
    lines in [sample-answers page, band_end), first occurrence per number, no
    x-bucket restriction. Returns {} (→ engine drop) when the anchor title is
    missing. map_paper's count-reconcile + monotonic + spread gates still apply."""
    if paper_det is not None and paper_det != "question":
        return {}  # same grammar guard as the engine: schemes here are Question-headed
    sa = sample_answers_page(doc, band_start, band_end)
    if sa is None:
        return {}
    found = {}
    for pi in range(sa, band_end):
        page = doc[pi]
        if page.rotation:
            continue
        H = page.rect.height
        for lw in am.line_groups(page):
            if not lw or len(lw) > QHEAD_MAX_WORDS:
                continue
            w0 = lw[0]
            if w0[0] >= am.LEFT_MARGIN_X:
                continue
            word = am._deligature(w0[4])
            n = None
            m = QHEAD_FUSED.fullmatch(word)
            if m:
                n = int(m.group(1))
            elif word in ("Question", "QUESTION") and len(lw) >= 2:
                m2 = QHEAD_NUM.fullmatch(lw[1][4])
                if m2:
                    n = int(m2.group(1))
            if n is not None and n not in found:
                found[n] = (pi, w0[1] / H)
    return found


am.detect_scheme_markers = lc027_scheme_markers  # in-memory override only


def qa_echo(scheme, sidecar, year):
    """Print the first lines of every question's first crop segment."""
    for q in sidecar["q"]:
        seg = q["region"][0]
        if "r" not in seg:
            print(f"  {year} Q{q['n']} p{seg['p']} PAGEJUMP")
            continue
        pg = scheme[seg["p"] - 1]
        W, H = pg.rect.width, pg.rect.height
        x0, y0, x1, y1 = seg["r"]
        t = pg.get_text("text", clip=fitz.Rect(x0 * W, y0 * H, x1 * W, y1 * H))
        lines = [l.strip() for l in t.splitlines() if l.strip()]
        span = sum(1 for s in q["region"])
        print(f"  {year} Q{q['n']} scheme p{seg['p']} ({span} seg) starts: "
              f"{' | '.join(lines[:3])[:90]!r}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True,
                    help="staging dir for sidecars (copied to answers/ only after QA)")
    args = ap.parse_args()

    wrote = dropped = 0
    for fid in sorted(TARGETS):
        for year in TARGETS[fid]:
            ppath = os.path.join(CORPUS, "exampapers", str(year), fid)
            spath = os.path.join(CORPUS, "markingschemes", str(year), fid)
            if not (os.path.exists(ppath) and os.path.exists(spath)):
                print(f"MISS {year} {fid}: paper/scheme not in corpus")
                continue
            sidecar, st = am.map_paper(ppath, spath, ("whole", "000"))
            if sidecar is None:
                dropped += 1
                print(f"DROP {year} {fid}: {st['reason']} (detector {st['detector']})")
                continue
            bs, be = sidecar["band"]
            for q in sidecar["q"]:
                for seg in q["region"]:
                    assert bs <= seg["p"] < be, \
                        f"{fid} Q{q['n']} page {seg['p']} escapes band [{bs},{be})"
            print(f"MAP  {year} {fid}: {len(sidecar['q'])}q "
                  f"crop={st['crop']} pagejump={st['pagejump']} conf={st['conf']}")
            qa_echo(fitz.open(spath), sidecar, year)
            ydir = os.path.join(args.out, str(year))
            os.makedirs(ydir, exist_ok=True)
            with open(os.path.join(ydir, f"{fid}.json"), "w", encoding="utf-8") as fh:
                json.dump(sidecar, fh, ensure_ascii=False, sort_keys=True,
                          separators=(",", ":"))
            wrote += 1
    print(f"done: {wrote} staged, {dropped} dropped")
    return 0


if __name__ == "__main__":
    sys.exit(main())
