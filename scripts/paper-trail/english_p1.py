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
Paper Trail — English Paper One (LC002 LP100): the COMPOSING prompts.

Paper 1's Section II prints seven numbered composition prompts, and the scheme
answers each with a per-prompt assessment block (focus, register, the P/C/L/M
grid). Both sides are ascending 1..7 runs, so the map is mechanical — with one
sharp edge this file exists to enforce: the reading texts in Section I number
their PARAGRAPHS 1..N, so a paper-side run may only begin ON OR AFTER the
"SECTION II COMPOSING" page. The committed 2022 OL map was built without that
fence and anchored every chip on a reading passage's paragraphs; this
generator regenerates it correctly (--check reproduces the hand-built 2014 HL
map before any open year is generated).

Usage:
  python3 english_p1.py --check     # regression against committed 2014 HL map
  python3 english_p1.py             # map every corpus year (fixes 2022 OL)
  python3 english_p1.py --dry-run
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

# The real section divider prints its tariff on the heading line; the cover
# mentions COMPOSING three times without one. Line-level, and the LAST match
# wins, because 2022 OL's cover also prints a bare "SECTION II – COMPOSING".
COMPOSING_LINE = re.compile(r"COMPOSING\s*\(100|SECTION\s+II\s{3,}COMPOSING")
HEAD = re.compile(r"^(\d)\.(?:\s|$)")


def lines_with_pos(page):
    W, H = page.rect.width, page.rect.height
    rows = {}
    for w in page.get_text("words"):
        rows.setdefault((w[5], w[6]), []).append(w)
    out = []
    for key in rows:
        ws = sorted(rows[key], key=lambda w: w[0])
        out.append((" ".join(w[4] for w in ws).strip(),
                    ws[0][0] / W, min(w[1] for w in ws) / H))
    out.sort(key=lambda t: (t[2], t[1]))
    return out


def composing_run(doc, start_page0, stop_page0=None, xmax=0.2):
    """{n: (page1, y)} — ascending 1..N run from the given page on."""
    found, want = {}, 1
    stop = stop_page0 if stop_page0 is not None else len(doc)
    for pi in range(start_page0, stop):
        for txt, x, y in lines_with_pos(doc[pi]):
            m = HEAD.match(txt)
            if m and x <= xmax and int(m.group(1)) == want:
                found[want] = (pi + 1, y)
                want += 1
    return found


def find_composing_page(doc):
    last = None
    for pi in range(len(doc)):
        for ln in doc[pi].get_text().split("\n"):
            if COMPOSING_LINE.search(ln):
                last = pi
    return last


def build(paper_path, scheme_path):
    paper, scheme = fitz.open(paper_path), fitz.open(scheme_path)
    cp = find_composing_page(paper)
    if cp is None:
        return None, "paper prints no SECTION II COMPOSING heading"
    pq = composing_run(paper, cp)
    if not (5 <= len(pq) <= 8):
        return None, f"composing run is {len(pq)} prompts — expected ~7"

    sp = find_composing_page(scheme)
    # The scheme restates the prompts in its own composing section; where the
    # heading is absent (older schemes), the LAST full run of the paper's
    # length is the composing block — comprehension answers sit earlier.
    best = None
    starts = [sp] if sp is not None else list(range(len(scheme)))
    for st in starts if sp is not None else [0]:
        run = composing_run(scheme, st if sp is not None else 0, xmax=0.25)
        if len(run) >= len(pq):
            best = {n: run[n] for n in range(1, len(pq) + 1)}
    if sp is None:
        # scan for the last complete ascending run
        marks = []  # noqa: shadowed below
        for pi in range(len(scheme)):
            for txt, x, y in lines_with_pos(scheme[pi]):
                m = HEAD.match(txt)
                if m and x <= 0.25:
                    marks.append((int(m.group(1)), pi + 1, y))
        runs, cur = [], {}
        for n, pg, y in marks:
            if n == 1:
                cur = {1: (pg, y)}
            elif cur and n == max(cur) + 1:
                cur[n] = (pg, y)
            if len(cur) == len(pq):
                runs.append(dict(cur))
        best = runs[-1] if runs else None
    if not best or len(best) < len(pq):
        return None, "scheme has no composing run matching the paper's prompts"

    q = []
    ordered = sorted(pq)
    for i, n in enumerate(ordered):
        pg, y = pq[n]
        y_end = 1.0
        if i + 1 < len(ordered) and pq[ordered[i + 1]][0] == pg:
            y_end = pq[ordered[i + 1]][1]
        spg, sy = best[n]
        if i + 1 < len(ordered):
            npg, ny = best[ordered[i + 1]]
        else:
            npg, ny = spg, 1.0
        region = []
        if npg == spg:
            region.append({"p": spg, "r": [0.0, round(max(0.0, sy - 0.012), 4),
                                           1.0, round(ny if ny > sy else 1.0, 4)]})
        else:
            region.append({"p": spg, "r": [0.0, round(max(0.0, sy - 0.012), 4), 1.0, 1.0]})
            for mid in range(spg + 1, npg):
                region.append({"p": mid, "r": [0.0, 0.0, 1.0, 1.0]})
            if ny > 0.04:
                region.append({"p": npg, "r": [0.0, 0.0, 1.0, round(ny, 4)]})
        q.append({"n": str(n), "conf": 1.0, "mode": "crop",
                  "pP": pg, "pY": [round(y, 4), round(y_end, 4)],
                  "region": region})
    # Echo self-check: the scheme restates each prompt, so the paper ask and
    # the scheme block must share real words. This is what caught both
    # committed maps anchoring chip 1 on a reading text.
    echo = 0
    for c in q:
        pg = paper[c["pP"] - 1]
        H = pg.rect.height
        a = set(w.lower() for w in re.findall(r"[A-Za-z]{5,}", pg.get_text(
            clip=fitz.Rect(0, c["pY"][0] * H, pg.rect.width,
                           min(c["pY"][0] + 0.12, 1.0) * H))))
        seg = c["region"][0]
        sg = scheme[seg["p"] - 1]
        SH = sg.rect.height
        b = set(w.lower() for w in re.findall(r"[A-Za-z]{5,}", sg.get_text(
            clip=fitz.Rect(0, seg["r"][1] * SH, sg.rect.width,
                           min(seg["r"][1] + 0.12, 1.0) * SH))))
        if len(a & b) >= 3:
            echo += 1
    if echo < len(q) - 1:
        return None, f"echo check failed — only {echo}/{len(q)} chips restate their prompt"
    return {
        "v": 1, "paperFileid": os.path.basename(paper_path),
        "schemeFileid": os.path.basename(scheme_path),
        "component": "100", "band": [1, len(scheme) + 1],
        "copyright": COPYRIGHT, "q": q,
    }, None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    if args.check:
        gold = json.load(open(os.path.join(ANSWERS_DIR, "2014", "LC002ALP100EV.pdf.json")))
        built, why = build(os.path.join(CORPUS, "exampapers", "2014", "LC002ALP100EV.pdf"),
                           os.path.join(CORPUS, "markingschemes", "2014", "LC002ALP000EV.pdf"))
        assert built, why
        g = [(c["n"], c["pP"], c["region"][0]["p"]) for c in gold["q"]]
        b = [(c["n"], c["pP"], c["region"][0]["p"]) for c in built["q"]]
        print("gold :", g)
        print("built:", b)
        assert g == b, "regression FAILED against the committed 2014 map"
        print("check OK — reproduces the committed 2014 HL map")
        return 0

    wrote = dropped = 0
    for year in range(2010, 2027):
        for lv in ("A", "G"):
            pf = f"LC002{lv}LP100EV.pdf"
            sf = f"LC002{lv}LP000EV.pdf"
            ppath = os.path.join(CORPUS, "exampapers", str(year), pf)
            spath = os.path.join(CORPUS, "markingschemes", str(year), sf)
            if not (os.path.exists(ppath) and os.path.exists(spath)):
                continue
            out = os.path.join(ANSWERS_DIR, str(year), f"{pf}.json")
            # Regenerate the two committed maps too: 2022 OL anchored on a
            # reading text's paragraphs, and 2014 HL's first chip on a text
            # intro — the echo self-check above is the regression now.
            sidecar, why = build(ppath, spath)
            tag = f"{year} {'HL' if lv == 'A' else 'OL'}"
            if sidecar is None:
                print(f"DROP {tag}: {why}")
                dropped += 1
                continue
            print(f"MAP  {tag}: {len(sidecar['q'])} prompts")
            if args.dry_run:
                continue
            os.makedirs(os.path.dirname(out), exist_ok=True)
            with open(out, "w", encoding="utf-8") as fh:
                json.dump(sidecar, fh, ensure_ascii=False, sort_keys=True,
                          separators=(",", ":"))
            wrote += 1
    print(f"done: {wrote} written, {dropped} dropped")
    return 0


if __name__ == "__main__":
    sys.exit(main())
