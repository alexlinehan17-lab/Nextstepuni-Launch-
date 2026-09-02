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
Paper Trail — History (LC004): DBQ-part chips for the unchipped sittings.

The shipped Higher EV maps chip the documents-based question's numbered
parts (the one compulsory question) and nothing else; twin_align's Irish
borrows were REFUSED after a render showed a DBQ part opening a Thatcher
essay. This builds the same DBQ chips directly from each sitting's own
documents — Higher IV (2010/2018/2020/2022) and the never-chipped
Ordinary level, both languages, 2010-2026.

Ordinary papers also get one labelled chip per essay section ("Section 2
· Ireland", "Section 3 · Europe and the Wider World") onto the scheme's
per-topic answer blocks, following the irish_sections.py precedent.

The Ordinary scheme file carries the EARLY MODERN field of study as its
second half (its own DBQ + sections); the LATER MODERN chips end at that
boundary and the sidecar band hides it from the viewer. A marking-outline
page lists the section names in mixed case before the real all-caps
answer headings, so section heads are matched case-sensitively.

Usage: python3 hist_dbq.py [--dry-run]
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

SEC_ANY = [re.compile(rf"^(?:Section|SECTION|Roinn|ROINN)\s*{n}\s*[:.\s]") for n in (0, 1, 2, 3)]
SEC_CAPS = [re.compile(rf"^(?:SECTION|ROINN)\s*{n}\s*[:.\s]") for n in (0, 1, 2, 3)]
PART = re.compile(r"^(\d{1,2})\.(?:\s|$)")


def lines_pos(page):
    W, H = page.rect.width, page.rect.height
    rows = {}
    for w in page.get_text("words"):
        rows.setdefault((w[5], w[6]), []).append(w)
    out = []
    for key in rows:
        ws = sorted(rows[key], key=lambda w: w[0])
        out.append((" ".join(w[4] for w in ws).replace("\xa0", " ").strip(),
                    ws[0][0] / W,
                    min(1.0, max(0.0, min(w[1] for w in ws) / H))))
    out.sort(key=lambda t: (t[2], t[1]))
    return out


def find_heads(doc, rx_list):
    """[(secno, page1, y, text)] for every matching row, doc order."""
    out = []
    for pi in range(len(doc)):
        for txt, x, y in lines_pos(doc[pi]):
            if len(txt) > 80:
                continue
            for secno in (1, 2, 3):
                if rx_list[secno].match(txt):
                    out.append((secno, pi + 1, y, txt))
                    break
    return out


def paper_parts(doc):
    heads = find_heads(doc, SEC_CAPS)
    sec = {}
    for secno, pg, y, txt in heads:
        if secno not in sec:
            sec[secno] = (pg, y, txt)
    if 1 not in sec or 2 not in sec:
        return None, None, "paper: section heads not found"
    p1, p2 = sec[1][0], sec[2][0]
    parts = {}
    # the questions sit on the Section 1 page; the facing documents pages
    # carry numbered source text, so widen only while parts are missing
    for pi in range(p1 - 1, p2):
        before = len(parts)
        for txt, x, y in lines_pos(doc[pi]):
            m = PART.match(txt)
            if m and x < 0.17 and y > 0.05 and (pi + 1, y) != sec[1][:2]:
                n = int(m.group(1))
                if n == len(parts) + 1 and n <= 6:
                    parts[n] = (pi + 1, y)
        if before >= 3 and len(parts) == before:
            break
        if len(parts) >= 3 and pi >= p1 - 1:
            break
    if len(parts) < 3:
        return None, None, f"paper: DBQ parts 1..{len(parts)} only"
    return parts, sec, None


def scheme_layout(doc, K, em_half=False):
    """DBQ part blocks + section answer heads + field-of-study boundary.
    em_half: map the EARLY MODERN half (the combined file's second Section 1
    onward) instead of the Later Modern first half."""
    any_heads = find_heads(doc, SEC_ANY)
    caps_heads = find_heads(doc, SEC_CAPS)
    sec1s = [h for h in any_heads if h[0] == 1]
    if not sec1s:
        return None, "scheme: no Section 1 head"
    if em_half:
        if len(sec1s) < 2:
            return None, "scheme: no early-modern Section 1 head"
        dbq = sec1s[-1]
        em = len(doc) + 1
    else:
        dbq = sec1s[0]
        em = sec1s[1][1] if len(sec1s) > 1 else len(doc) + 1
    stop2 = next((h for h in any_heads if h[0] == 2 and (h[1], h[2]) > (dbq[1], dbq[2])), None)
    # collect loose candidates (a lone dotless digit heads some blocks), then
    # take the LAST complete 1..K ascending run — the compact mark-outline
    # list prints the same numbers before the real answer blocks
    cands = []
    for pi in range(dbq[1] - 1, (stop2[1] if stop2 else len(doc))):
        for txt, x, y in lines_pos(doc[pi]):
            if (pi + 1, y) <= (dbq[1], dbq[2]):
                continue
            if stop2 and (pi + 1, y) >= (stop2[1], stop2[2]):
                continue
            m = PART.match(txt) or re.match(r"^(\d{1,2})$", txt)
            if m and x < 0.3 and int(m.group(1)) <= K:
                cands.append((int(m.group(1)), pi + 1, y))
    runs, cur = [], {}
    for n, pg, y in cands:
        if n == len(cur) + 1:
            cur[n] = (pg, y)
        elif n == 1:
            runs.append(cur)
            cur = {1: (pg, y)}
        if len(cur) == K:
            runs.append(cur)
            cur = {}
    runs.append(cur)
    full = [r for r in runs if len(r) == K]
    if not full:
        best = max(runs, key=len) if runs else {}
        return None, f"scheme: DBQ blocks 1..{len(best)} vs paper 1..{K}"
    parts = full[-1]
    s2 = next((h for h in caps_heads if h[0] == 2 and h[1] >= dbq[1] and h[1] < em), None)
    s3 = next((h for h in caps_heads if h[0] == 3 and s2 and (h[1], h[2]) > (s2[1], s2[2]) and h[1] < em), None)
    return {"parts": parts, "stop2": stop2, "s2": s2, "s3": s3, "em": em,
            "band_lo": dbq[1] if em_half else 1}, None


def region_span(p0, y0, p1, y1, doc_len):
    region = [{"p": p0, "r": [0.0, round(max(0.0, y0 - 0.012), 4), 1.0, 1.0]}]
    if p1 == p0:
        region[0]["r"][3] = round(y1, 4) if y1 > y0 else 1.0
        return region
    for mid in range(p0 + 1, min(p1, doc_len + 1)):
        region.append({"p": mid, "r": [0.0, 0.0, 1.0, 1.0]})
    if y1 > 0.04 and p1 <= doc_len:
        region.append({"p": p1, "r": [0.0, 0.0, 1.0, round(y1, 4)]})
    return region


def humanize(txt):
    body = txt.split(":", 1)
    tail = body[1].strip().title() if len(body) > 1 else ""
    tail = re.sub(r"\s*\(\d+\s*mh?arc[s]?\)\s*$", "", tail, flags=re.I)
    head = body[0].strip().title()
    return f"{head} · {tail}" if tail else head


def build(ppath, spath, level, em_half=False):
    paper, scheme = fitz.open(ppath), fitz.open(spath)
    parts, psec, err = paper_parts(paper)
    if err:
        return None, err
    K = len(parts)
    lay, err = scheme_layout(scheme, K, em_half)
    if err:
        return None, err
    sp = lay["parts"]
    q = []
    for n in range(1, K + 1):
        pg, y = parts[n]
        y_end = parts[n + 1][1] if n + 1 in parts and parts[n + 1][0] == pg else 1.0
        p0, y0 = sp[n]
        if n + 1 in sp:
            p1, y1 = sp[n + 1]
        elif lay["stop2"]:
            p1, y1 = lay["stop2"][1], 0.0
        else:
            p1, y1 = p0, 1.0
        q.append({"n": str(n), "conf": 1.0, "mode": "crop",
                  "pP": pg, "pY": [round(y, 4), round(y_end, 4)],
                  "region": region_span(p0, y0, p1, y1, len(scheme))})
    band_hi = min(lay["em"], len(scheme) + 1)
    if level == "G" and lay["s2"] and lay["s3"]:
        for secno, head, nxt in ((2, lay["s2"], lay["s3"]), (3, lay["s3"], None)):
            pane = psec.get(secno)
            if not pane:
                continue
            end_pg, end_y = (nxt[1], nxt[2]) if nxt else (band_hi - 1, 1.0)
            if end_pg - head[1] > 9:
                end_pg, end_y = head[1] + 9, 1.0
            q.append({"n": str(len(q) + 1), "conf": 1.0, "mode": "crop",
                      "label": humanize(pane[2]),
                      "pP": pane[0], "pY": [round(pane[1], 4), 1.0],
                      "region": region_span(head[1], head[2], end_pg, end_y, len(scheme))})
    return {
        "v": 1, "paperFileid": os.path.basename(ppath),
        "schemeFileid": os.path.basename(spath), "component": "",
        "band": [lay["band_lo"], band_hi], "copyright": COPYRIGHT, "q": q,
    }, None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    targets = [("LC004", y, "A", lg) for y in (2010, 2018, 2020, 2022) for lg in ("IV",)] + \
              [("LC004", y, "G", lg) for y in range(2010, 2027) for lg in ("EV", "IV")] + \
              [("LC096", 2021, "G", "EV"), ("LC096", 2021, "G", "IV"),
               ("LC096", 2022, "G", "EV"), ("LC096", 2022, "G", "IV"),
               ("LC096", 2022, "A", "IV")]
    wrote = dropped = 0
    for code, year, lv, lg in targets:
        fid = f"{code}{lv}LP000{lg}.pdf"
        ppath = os.path.join(CORPUS, "exampapers", str(year), fid)
        spath = os.path.join(CORPUS, "markingschemes", str(year), fid)
        if not (os.path.exists(ppath) and os.path.exists(spath)):
            continue
        out = os.path.join(ANSWERS_DIR, str(year), f"{fid}.json")
        if os.path.exists(out):
            continue
        sidecar, why = build(ppath, spath, lv, em_half=(code == "LC096"))
        tag = f"{code[-2:]}-{year}{lv}{lg}"
        if sidecar is None:
            print(f"DROP {tag}: {why}")
            dropped += 1
            continue
        labels = [x.get("label", "") for x in sidecar["q"]]
        print(f"MAP  {tag}: {len(sidecar['q'])} chips  {[l for l in labels if l]}")
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
