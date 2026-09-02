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
Paper Trail — Computer Science Section C (LC219 LP040): the programming booklet.

The booklet prints ONE question (Question 16 / Ceist 16, with parts) and the
shared scheme answers it in a "Section C / Programming" block near the end —
full model solutions, code listings included. One precise chip per booklet is
the right shape here (a question's sub-parts share one scheme block), and it
replaces the two imprecise whole-tail band chips an early wave shipped.

The block is found from the BACK: the last page headed Section C / Roinn C
before the Coursework appendix, falling back to the last "Question/Ceist 16"
heading in the scheme's second half (two Irish schemes translate the section
banner away). The region runs to the Coursework page or the last page that
carries real text.

Usage: python3 cs_section_c.py [--dry-run]
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

Q16 = re.compile(r"^(?:Question|Ceist)\s+16\b")
SEC_C = re.compile(r"\b(?:Section|Roinn|ROINN)\s+C\b")
COURSEWORK = re.compile(r"Coursework|Obair\s+Ch[úu]rsa", re.I)


def q16_anchor(doc):
    for pi in range(len(doc)):
        H = doc[pi].rect.height
        rows = {}
        for w in doc[pi].get_text("words"):
            rows.setdefault((w[5], w[6]), []).append(w)
        for k, ws in rows.items():
            ws = sorted(ws, key=lambda w: w[0])
            t = " ".join(w[4] for w in ws).replace("\xa0", " ").strip()
            if Q16.match(t):
                return pi + 1, min(w[1] for w in ws) / H
    return None, None


def section_c_block(doc):
    """(start_page1, end_page1) of the Section C answer block."""
    cw = None
    for pi in range(len(doc)):
        if COURSEWORK.search(doc[pi].get_text()):
            cw = pi + 1
    limit = cw - 1 if cw else len(doc)
    start = None
    for pi in range(limit):
        t = doc[pi].get_text()
        # The front of the scheme carries a "structure of the marking scheme
        # for Section C" NOTE page; the real block also names Question 16 or
        # sits in the second half.
        if SEC_C.search(t) and re.search(r"(?:Question|Ceist)\s*16", t) \
                and pi + 1 > len(doc) // 3:
            start = pi + 1
    if start is None:
        for pi in range(len(doc) // 2, limit):
            if re.search(r"(?:Question|Ceist)\s*16", doc[pi].get_text()):
                start = pi + 1
                break
    if start is None:
        return None, None
    end = limit
    while end > start and len(doc[end - 1].get_text().strip()) < 40:
        end -= 1
    return start, end


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    wrote = dropped = 0
    for year in range(2020, 2027):
        for lv in ("A", "G"):
            for lg in ("EV", "IV"):
                pf = f"LC219{lv}LP040{lg}.pdf"
                sf = f"LC219{lv}LP000{lg}.pdf"
                ppath = os.path.join(CORPUS, "exampapers", str(year), pf)
                spath = os.path.join(CORPUS, "markingschemes", str(year), sf)
                if not (os.path.exists(ppath) and os.path.exists(spath)):
                    continue
                paper, scheme = fitz.open(ppath), fitz.open(spath)
                pg, y = q16_anchor(paper)
                s0, s1 = section_c_block(scheme)
                tag = f"{year} {lv}{lg}"
                if pg is None or s0 is None:
                    print(f"DROP {tag}: {'no Q16 head' if pg is None else 'no Section C block'}")
                    dropped += 1
                    continue
                region = [{"p": p, "r": [0.0, 0.0, 1.0, 1.0]} for p in range(s0, s1 + 1)]
                region[0]["r"] = [0.0, 0.0, 1.0, 1.0]
                sidecar = {
                    "v": 1, "paperFileid": pf, "schemeFileid": sf,
                    "component": "", "band": [1, len(scheme) + 1],
                    "copyright": COPYRIGHT,
                    "q": [{"n": "16", "conf": 1.0, "mode": "crop",
                           "label": "Section C · Question 16",
                           "pP": pg, "pY": [round(y, 4), 1.0],
                           "region": region}],
                }
                print(f"MAP  {tag}: Q16@p{pg} -> scheme p{s0}-{s1}")
                if args.dry_run:
                    continue
                out = os.path.join(ANSWERS_DIR, str(year), f"{pf}.json")
                os.makedirs(os.path.dirname(out), exist_ok=True)
                with open(out, "w", encoding="utf-8") as fh:
                    json.dump(sidecar, fh, ensure_ascii=False, sort_keys=True,
                              separators=(",", ":"))
                wrote += 1
    print(f"done: {wrote} written, {dropped} dropped")
    return 0


if __name__ == "__main__":
    sys.exit(main())
