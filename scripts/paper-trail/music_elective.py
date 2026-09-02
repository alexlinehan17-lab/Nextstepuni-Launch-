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
Paper Trail — Music Listening Elective (LC067 LP007), Higher, both languages.

The elective paper asks about the candidate's own prepared topic, so the
scheme marks it with a single banded-criteria table headed "Listening –
Higher level - Elective" (Irish: "Éisteacht - Ardleibhéal - Roghnach").
One chip per paper (the CS Section C precedent) anchored on the paper's
first prompt, opening that criteria block. The practical electives'
pages all carry an "(one activity)/(Gníomhaíocht)" qualifier and are
excluded by it. The 2021+ broken-font listening pages do not matter
here — the elective header pages kept a clean text layer.

Usage: python3 music_elective.py [--dry-run]
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
COPYRIGHT = "© State Examinations Commission"

POS = re.compile(r"(listening.{0,40}elective|elective.{0,40}listening|"
                 r"éisteacht?.{0,40}roghnach|roghnach.{0,40}éisteacht?)", re.I | re.S)
NEG = re.compile(r"activit|gníomhaíocht", re.I)
# the criteria table always cites syllabus page 12 §2.3.5 — a language-proof
# fingerprint for years whose running header drops the Roghnach tail
FP = re.compile(r"(page|leathanach)\s*12\s*[–—-]\s*2\.3\.5", re.I)


def head_text(page):
    lns = [l.strip() for l in page.get_text().splitlines() if l.strip()]
    return " ".join(lns[:3])[:160]


def elective_pages(doc):
    hits = []
    for pi in range(len(doc)):
        head = head_text(doc[pi])
        if NEG.search(head):
            continue
        if POS.search(head) or FP.search(doc[pi].get_text()):
            hits.append(pi + 1)
    if not hits:
        return None
    # keep the first contiguous block
    block = [hits[0]]
    for p in hits[1:]:
        if p == block[-1] + 1:
            block.append(p)
        else:
            break
    return block


def paper_anchor(doc):
    if len(doc) < 2:
        return None
    page = doc[1]
    H = page.rect.height
    rows = {}
    for w in page.get_text("words"):
        rows.setdefault((w[5], w[6]), []).append(w)
    best = None
    for key in rows:
        ws = sorted(rows[key], key=lambda w: w[0])
        txt = " ".join(w[4] for w in ws).strip()
        y = min(w[1] for w in ws) / H
        if re.match(r"^1\.(\s|$)", txt) and ws[0][0] < 120 and y > 0.05:
            if best is None or y < best:
                best = y
    return (2, best if best is not None else 0.0)


def build(ppath, spath, lang, ev_block=None):
    paper, scheme = fitz.open(ppath), fitz.open(spath)
    block = elective_pages(scheme)
    if not block and ev_block:
        # scanned Irish tail: image-correlate the EV twin's criteria page
        sys.path.insert(0, HERE)
        from twin_align import _thumb, _corr
        ev = fitz.open(spath.replace("IV.pdf", "EV.pdf"))
        ref = _thumb(ev[ev_block[0] - 1])
        best, score = None, 0.0
        for cand in range(max(0, ev_block[0] - 3), min(len(scheme), ev_block[0] + 2)):
            c = _corr(ref, _thumb(scheme[cand]))
            if c > score:
                best, score = cand + 1, c
        if best is not None and score >= 0.35:
            block = [best + i for i in range(len(ev_block)) if best + i <= len(scheme)]
        else:
            return None, f"no elective page (image corr {score:.2f})"
    if not block:
        return None, "no elective criteria page in scheme"
    anchor = paper_anchor(paper)
    if anchor is None:
        return None, "paper too short"
    label = "Listening Elective" if lang == "EV" else "Éisteacht Roghnach"
    region = [{"p": p, "r": [0.0, 0.0, 1.0, 1.0]} for p in block]
    q = [{"n": "1", "conf": 1.0, "mode": "crop", "label": label,
          "pP": anchor[0], "pY": [round(anchor[1], 4), 1.0], "region": region}]
    return {
        "v": 1, "paperFileid": os.path.basename(ppath),
        "schemeFileid": os.path.basename(spath), "component": "007",
        "band": [1, len(scheme) + 1], "copyright": COPYRIGHT, "q": q,
    }, None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    wrote = dropped = 0
    ev_blocks = {}
    for year in range(2010, 2027):
        for lg in ("EV", "IV"):
            pf = f"LC067ALP007{lg}.pdf"
            sf = f"LC067ALP000{lg}.pdf"
            ppath = os.path.join(CORPUS, "exampapers", str(year), pf)
            spath = os.path.join(CORPUS, "markingschemes", str(year), sf)
            if not (os.path.exists(ppath) and os.path.exists(spath)):
                continue
            out = os.path.join(ANSWERS_DIR, str(year), f"{pf}.json")
            if os.path.exists(out):
                continue
            sidecar, why = build(ppath, spath, lg, ev_blocks.get(year))
            tag = f"{year} {lg}"
            if sidecar is None:
                print(f"DROP {tag}: {why}")
                dropped += 1
                continue
            pages = [r["p"] for r in sidecar["q"][0]["region"]]
            if lg == "EV":
                ev_blocks[year] = pages
            print(f"MAP  {tag}: scheme pages {pages}")
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
