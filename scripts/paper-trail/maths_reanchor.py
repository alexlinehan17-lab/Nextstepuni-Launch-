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
Paper Trail — re-anchor 2010-2013 Mathematics sidecars onto the SERVED scheme.

The estate audit found these sidecars were built against the LP000 scheme
edition while the index (and therefore the viewer) serves the LP030 edition —
a differently paginated document — so every region rendered wrong pages live.
The paper side of each chip is untouched; scheme regions are re-derived from
the served document's own "Question N" heads, constrained to the paper's half
of the combined P1+P2 file (the second cover / "Paper 2" heading splits it),
and cross-checked by word overlap with the chip's paper ask where the era
restates questions.

Usage: python3 maths_reanchor.py [--dry-run]
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

HEAD = re.compile(r"^(?:QUESTION|Question|CEIST|Ceist)\s+(\d{1,2})\b")
COVER = re.compile(r"State Examinations Commission|Coimisiún na Scrúduithe")
P2_HEAD = re.compile(r"Paper\s*2|Páipéar\s*2", re.I)


def lines_pos(page):
    W, H = page.rect.width, page.rect.height
    rows = {}
    for w in page.get_text("words"):
        rows.setdefault((w[5], w[6]), []).append(w)
    out = []
    for key in rows:
        ws = sorted(rows[key], key=lambda w: w[0])
        out.append((" ".join(w[4] for w in ws).strip(), ws[0][0] / W,
                    min(1.0, max(0.0, min(w[1] for w in ws) / H))))
    out.sort(key=lambda t: (t[2], t[1]))
    return out


MNUM = re.compile(r"\bM\s?2\d{2}T?\b")


def halves(doc):
    """(p1_range, p2_range), 1-based inclusive. The served files place a
    fresh exam-number cover (2011. M229 / M230) at each paper's scheme; one
    cover means the file's front IS Paper 1 and the cover opens Paper 2."""
    covers = []
    for pi in range(2, len(doc)):
        head = " ".join(doc[pi].get_text().split())[:220]
        if COVER.search(head) and (MNUM.search(head) or P2_HEAD.search(head)):
            covers.append(pi + 1)
    if len(covers) >= 2:
        return (covers[0], covers[1] - 1), (covers[1], len(doc))
    if len(covers) == 1:
        return (1, covers[0] - 1), (covers[0], len(doc))
    q1s = []
    for pi in range(1, len(doc)):
        for t, x, y in lines_pos(doc[pi]):
            m = HEAD.match(t)
            if m and int(m.group(1)) == 1:
                q1s.append(pi + 1)
                break
    b = q1s[1] if len(q1s) > 1 else len(doc) + 1
    return (1, b - 1), (b, len(doc))


def heads_in(doc, lo, hi):
    out = []
    for pi in range(lo - 1, hi):
        for t, x, y in lines_pos(doc[pi]):
            m = HEAD.match(t)
            if m and x < 0.45 and len(t) < 70:
                out.append((int(m.group(1)), pi + 1, y))
    return out


def ask_words(paper, q):
    H = paper[q["pP"] - 1]
    words = set()
    ph = H.rect.height
    for w in H.get_text("words"):
        if q["pY"][0] - 0.002 <= w[1] / ph <= min(1.0, q["pY"][0] + 0.3):
            t = re.sub(r"\W+", "", w[4]).lower()
            if len(t) >= 4:
                words.add(t)
    return words


def region_words(scheme, pg, y, span=0.6):
    words = set()
    page = scheme[pg - 1]
    ph = page.rect.height
    for w in page.get_text("words"):
        if y <= w[1] / ph <= min(1.0, y + span):
            t = re.sub(r"\W+", "", w[4]).lower()
            if len(t) >= 4:
                words.add(t)
    return words


def rebuild(year, fname, served_fid):
    path = os.path.join(ANSWERS_DIR, year, fname)
    sc = json.load(open(path))
    ppath = os.path.join(CORPUS, "exampapers", year, sc["paperFileid"])
    spath = os.path.join(CORPUS, "markingschemes", year, served_fid)
    paper, scheme = fitz.open(ppath), fitz.open(spath)
    p1, p2 = halves(scheme)
    lo, hi = p1 if "LP1" in sc["paperFileid"] else p2
    heads = heads_in(scheme, lo, hi)
    byn = {}
    for n, pg, y in heads:
        byn.setdefault(n, []).append((pg, y))
    q_new = []
    last = (0, -1.0)
    echo_ok = echo_all = 0
    for q in sorted(sc["q"], key=lambda x: int(x["n"])):
        n = int(q["n"])
        cands = [c for c in byn.get(n, []) if c > last]
        if not cands:
            return None, f"no served head for Q{n} in half [{lo},{hi}]"
        pick = cands[0]
        aw = ask_words(paper, q)
        if len(byn.get(n, [])) > 1 and aw:
            pick = max(cands, key=lambda c: len(aw & region_words(scheme, *c)))
        last = pick
        nxt_heads = [c for cs in byn.values() for c in cs if c > pick]
        nxt = min(nxt_heads) if nxt_heads else (hi, 1.0)
        if nxt[0] > hi:
            nxt = (hi, 1.0)
        region = []
        p0, y0 = pick
        p1e, y1e = nxt
        if p1e == p0:
            region.append({"p": p0, "r": [0.0, round(max(0.0, y0 - 0.012), 4), 1.0, round(y1e, 4)]})
        else:
            region.append({"p": p0, "r": [0.0, round(max(0.0, y0 - 0.012), 4), 1.0, 1.0]})
            for mid in range(p0 + 1, p1e):
                region.append({"p": mid, "r": [0.0, 0.0, 1.0, 1.0]})
            if y1e > 0.04:
                region.append({"p": p1e, "r": [0.0, 0.0, 1.0, round(y1e, 4)]})
        if aw:
            ov = len(aw & region_words(scheme, *pick))
            echo_all += 1
            if ov >= 3:
                echo_ok += 1
        q_new.append({**q, "region": region})
    sc["q"] = q_new
    sc["schemeFileid"] = served_fid
    sc["band"] = [lo, hi + 1]
    return (sc, f"echo {echo_ok}/{echo_all}"), None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    sys.path.insert(0, "/private/tmp/claude-501/-Users-alexlinehan/345a28d9-1b6f-47b5-829c-f6fca188a1e9/scratchpad")
    import pt_parse
    by_key = {(str(r["year"]), r["doc"]): r for r in pt_parse.load()}
    wrote = dropped = 0
    for year in sorted(os.listdir(ANSWERS_DIR)):
        ydir = os.path.join(ANSWERS_DIR, year)
        if not os.path.isdir(ydir):
            continue
        for f in sorted(os.listdir(ydir)):
            if not (f.startswith("LC003") and f.endswith(".json")):
                continue
            sc = json.load(open(os.path.join(ydir, f)))
            row = by_key.get((year, sc["paperFileid"]))
            if not row or not row["scheme"] or row["scheme"] == sc["schemeFileid"]:
                continue
            served = row["scheme"]
            if not os.path.exists(os.path.join(CORPUS, "markingschemes", year, served)):
                print(f"SKIP {year}/{f}: served {served} not local")
                continue
            out, why = rebuild(year, f, served)
            if out is None:
                print(f"DROP {year}/{f}: {why}")
                dropped += 1
                continue
            sc_new, note = out
            print(f"MAP  {year}/{f}: {len(sc_new['q'])} chips -> {served} band={sc_new['band']} ({note})")
            if not args.dry_run:
                with open(os.path.join(ydir, f), "w", encoding="utf-8") as fh:
                    json.dump(sc_new, fh, ensure_ascii=False, sort_keys=True,
                              separators=(",", ":"))
                wrote += 1
    print(f"done: {wrote} rewritten, {dropped} dropped")


if __name__ == "__main__":
    main()
