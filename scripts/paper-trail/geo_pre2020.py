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
Paper Trail — Geography LC005 PRE-2020 single-booklet years: Part Two maps.

Why bespoke: pre-2020 Geography is ONE booklet (LC005ALP000EV / LC005GLP000EV)
whose COVER carries a contents table listing "Question 1"…"Question 12" — the
generic engine's 'question' detector latches onto that table (a perfect
monotonic 1..12 run on a single page) and the wave-7 chip-on-cover spread
guard correctly rejects it. The booklet itself is:

  Part One  — short-answer Q1–12 ("1."…"12." lead-ints). Its scheme collapses
              onto a 1–2 page key — the SAME shape wave 7 deliberately dropped
              for the modern split-format short-answer answerbook. NOT mapped.
  Part Two  — structured/essay "Question 1"…"Question 12", each starting a
              fresh page on BOTH the paper and the scheme. Mapped here —
              mirroring exactly the Q1–12 coverage the shipped 2020+ P043
              sidecars have.
  Section 3 — HL Options essays Q13–24 ("13."…"24." lead-ints), marked by a
              generic Outline-Marking-Scheme/OC rubric, 2–3 per scheme page.
              NOT mapped (no per-question scheme block worth cropping).

This generator anchors on the paper's PART TWO divider (skipping the cover
and Part One entirely), collects bare "Question N" headers on both sides,
and enforces COUNT RECONCILE: every one of Q1–12 must have exactly one
page-top scheme header, strictly monotonic, or the paper DROPS. The last
question is bounded at the first Section-3 / Appendix / Marcanna-Breise /
blank boundary page. Built-in per-question CONTENT QA (sub-part labels
"nA./nB./nC." inside the crop must carry the right question number, and a
paper sub-part title must reappear in the crop text) must pass for EVERY
question or the paper drops — no sidecar is written partially verified.

Note: pre-2020 paper and scheme share ONE fileid (LC005ALP000EV.pdf); they
differ only by corpus dir (exampapers/ vs markingschemes/), so paperFileid
== schemeFileid in these sidecars — the folder disambiguates.

Safety posture identical to anchor-map.py / hem_history.py: coordinates only,
sidecar schema v1, better no chip than a wrong one.

Usage: python3 geo_pre2020.py            # maps corpus years, writes answers/<year>/
       python3 geo_pre2020.py --dry      # report only, write nothing
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
YEARS = range(2010, 2020)                 # pre-2020 single-booklet era only
FILEIDS = ["LC005ALP000EV.pdf", "LC005GLP000EV.pdf"]
HEADER_X_MAX = 140      # a "Question N" header starts left of this (points)
MAX_LAST_SPAN = 8       # last question's boundary scan gives up after this many pages
EXPECT_NS = list(range(1, 13))            # Part Two is always Questions 1–12

PART_TWO_RE = re.compile(r"PART\s+TWO\s*[–-]\s*STRUCTURED", re.I)
HEADER_RE = re.compile(r"^Question\s+(\d{1,2})\s*$", re.I)
SUBPART_RE = re.compile(r"^(\d{1,2})\s*([A-C])\s*\.")
# pages that terminate the last question's scheme region
BOUNDARY_RES = [
    re.compile(r"SECTION\s+3\s*[–-]\s*OPTIONS", re.I),
    re.compile(r"^\s*Appendix\s+\d", re.I | re.M),
    re.compile(r"Marcanna\s+Breise", re.I),
    re.compile(r"Outline\s+Marking\s+Scheme", re.I),
]


def lines_with_pos(page):
    """[(text, x0, y_frac)] in reading order."""
    H = page.rect.height
    out = []
    for blk in page.get_text("dict")["blocks"]:
        if blk.get("type") != 0:
            continue
        for ln in blk.get("lines", []):
            txt = "".join(sp["text"] for sp in ln.get("spans", [])).strip()
            if txt:
                out.append((txt, ln["bbox"][0], ln["bbox"][1] / H))
    out.sort(key=lambda t: (t[2], t[1]))
    return out


def find_part_two(doc):
    """0-based index of the PART TWO divider page, or None."""
    for pi in range(doc.page_count):
        if PART_TWO_RE.search(doc[pi].get_text("text")):
            return pi
    return None


def is_boundary(page):
    t = page.get_text("text")
    if not t.strip():
        return True                       # blank / scanned-empty trailing page
    return any(rx.search(t) for rx in BOUNDARY_RES)


def collect_headers(doc, start_pi):
    """[(n, page_index, y_frac)] for bare 'Question N' lines after start_pi."""
    out = []
    for pi in range(start_pi + 1, doc.page_count):
        for txt, x0, yf in lines_with_pos(doc[pi]):
            m = HEADER_RE.match(txt)
            if m and x0 < HEADER_X_MAX:
                out.append((int(m.group(1)), pi, round(yf, 4)))
    return out


def reconcile(headers, want_ns, side, problems):
    """Exactly one header per wanted n, strictly monotonic. Returns {n:(pi,yf)}."""
    got = {}
    for n, pi, yf in headers:
        if n not in want_ns:
            problems.append(f"{side}: stray header Question {n} on p{pi + 1}")
            return None
        if n in got:
            problems.append(f"{side}: duplicate header Question {n} (p{got[n][0] + 1} and p{pi + 1})")
            return None
        got[n] = (pi, yf)
    missing = [n for n in want_ns if n not in got]
    if missing:
        problems.append(f"{side}: missing Question headers {missing}")
        return None
    seq = [got[n] for n in want_ns]
    if any(seq[i] >= seq[i + 1] for i in range(len(seq) - 1)):
        problems.append(f"{side}: headers not monotonic")
        return None
    return got


def region_text(doc, region):
    out = []
    for seg in region:
        pg = doc[seg["p"] - 1]
        W, H = pg.rect.width, pg.rect.height
        x0, y0, x1, y1 = seg["r"]
        out.append(pg.get_text("text", clip=fitz.Rect(x0 * W, y0 * H, x1 * W, y1 * H)))
    return "\n".join(out)


def norm(s):
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


def paper_question_text(doc, pmarks, n):
    """Paper text of question n: from its header up to (not into) the next header."""
    pi, yf = pmarks[n]
    if n + 1 in pmarks:
        end_pi, end_yf = pmarks[n + 1]
    else:
        end_pi, end_yf = min(pi + 2, doc.page_count - 1), 1.0
    chunks = []
    for p in range(pi, end_pi + 1):
        pg = doc[p]
        W, H = pg.rect.width, pg.rect.height
        y0 = (yf if p == pi else 0.0) * H
        y1 = (end_yf if (p == end_pi and n + 1 in pmarks) else 1.0) * H
        if y1 > y0:
            chunks.append(pg.get_text("text", clip=fitz.Rect(0, y0, W, y1)))
    return "\n".join(chunks)


UNNUM_SUBPART_RE = re.compile(r"^([A-C])\s*\.")


def subpart_titles(txt):
    """Titles of a question's lettered sub-parts ('2A. Earthquakes' → 'earthquakes').

    Handles both numbered ('5A.') and unnumbered ('A.') labels, and the layout
    where the label and its title land on separate extracted lines."""
    lines = [ln.strip() for ln in txt.splitlines() if ln.strip()]
    titles = []
    for i, ln in enumerate(lines):
        m = SUBPART_RE.match(ln) or UNNUM_SUBPART_RE.match(ln)
        if not m:
            continue
        t = norm(ln[m.end():])
        if len(t) < 5 and i + 1 < len(lines):
            t = norm(lines[i + 1])
        if len(t) >= 5:
            titles.append(t)
    return titles


def qa_question(n, paper_txt, crop_txt, problems):
    """Content QA: crop must belong to question n and echo its sub-part titles."""
    if len(crop_txt.strip()) < 40:
        problems.append(f"Q{n}: crop text too thin ({len(crop_txt.strip())} chars) — needs render check")
        return False, None
    # 1) every numbered sub-part label in the crop must carry n
    for ln in crop_txt.splitlines():
        m = SUBPART_RE.match(ln.strip())
        if m and int(m.group(1)) != n:
            problems.append(f"Q{n}: crop contains foreign sub-part label '{ln.strip()[:30]}'")
            return False, None
    # 2) the crop's first 'Question N' token must be n
    mm = re.search(r"Question\s+(\d{1,2})", crop_txt)
    if not mm or int(mm.group(1)) != n:
        problems.append(f"Q{n}: crop's first Question token is "
                        f"{mm.group(1) if mm else 'absent'}")
        return False, None
    # 3) at least one paper sub-part TITLE must reappear in the crop — and a
    #    question with no extractable titles is NOT auto-trusted
    ncrop = norm(crop_txt)
    titles = subpart_titles(paper_txt)
    if not titles:
        problems.append(f"Q{n}: no sub-part titles extractable from the paper — cannot content-match")
        return False, None
    hit = next((t for t in titles if t in ncrop), None)
    if not hit:
        problems.append(f"Q{n}: no paper sub-part title found in crop (looked for {titles[:3]})")
        return False, None
    return True, hit


def map_paper(paper_path, scheme_path):
    """Returns (sidecar_or_None, evidence, problems)."""
    problems, evidence = [], []
    paper, scheme = fitz.open(paper_path), fitz.open(scheme_path)
    try:
        p_div, s_div = find_part_two(paper), find_part_two(scheme)
        if p_div is None or s_div is None:
            problems.append(f"PART TWO divider not found (paper={p_div}, scheme={s_div})")
            return None, evidence, problems

        pmarks = reconcile(collect_headers(paper, p_div), EXPECT_NS, "paper", problems)
        smarks = reconcile(collect_headers(scheme, s_div), EXPECT_NS, "scheme", problems)
        if not pmarks or not smarks:
            return None, evidence, problems

        # bound the last question at the first boundary page
        last_pi = smarks[EXPECT_NS[-1]][0]
        end_pi = None
        for p in range(last_pi + 1, min(last_pi + 1 + MAX_LAST_SPAN, scheme.page_count)):
            if is_boundary(scheme[p]):
                end_pi = p - 1
                break
        if end_pi is None:
            if last_pi + 1 + MAX_LAST_SPAN >= scheme.page_count:
                end_pi = scheme.page_count - 1
            else:
                problems.append(f"no boundary after last question within {MAX_LAST_SPAN} pages")
                return None, evidence, problems

        qout = []
        for n in EXPECT_NS:
            s_pi, s_yf = smarks[n]
            e_pi = (smarks[n + 1][0] - 1) if n + 1 in smarks else end_pi
            # trim trailing blank/divider pages between this Q and the next header
            while e_pi > s_pi and is_divider_or_blank(scheme[e_pi]):
                e_pi -= 1
            region = [{"p": s_pi + 1, "r": [0.0, s_yf, 1.0, 1.0]}]
            for mid in range(s_pi + 1, e_pi + 1):
                if scheme[mid].get_text("text").strip():
                    region.append({"p": mid + 1, "r": [0.0, 0.0, 1.0, 1.0]})
            # engine-style top strip: when the NEXT question's header sits below
            # real continuation content (not just a section divider / page number),
            # that content belongs to THIS question — include it
            if n + 1 in smarks:
                nx_pi, nx_yf = smarks[n + 1]
                if nx_yf > 0.02 and content_above(scheme[nx_pi], nx_yf):
                    region.append({"p": nx_pi + 1, "r": [0.0, 0.0, 1.0, nx_yf]})
            p_pi, p_yf = pmarks[n]
            qout.append({"n": str(n), "pP": p_pi + 1, "pY": [p_yf, 1.0],
                         "region": region, "mode": "crop", "conf": 1.0})

        # ── mandatory content QA: every question or nothing ────────────────
        for q in qout:
            n = int(q["n"])
            ptxt = paper_question_text(paper, pmarks, n)
            ctxt = region_text(scheme, q["region"])
            ok, hit = qa_question(n, ptxt, ctxt, problems)
            if not ok:
                return None, evidence, problems
            evidence.append((n, hit or "(no numbered sub-part titles on paper)",
                             " ".join(ctxt.split())[:70]))

        sidecar = {"v": SIDECAR_V,
                   "paperFileid": os.path.basename(paper_path),
                   "schemeFileid": os.path.basename(scheme_path),
                   "component": "",
                   "band": [s_div + 1, end_pi + 1],
                   "copyright": COPYRIGHT,
                   "q": qout}
        return sidecar, evidence, problems
    finally:
        paper.close()
        scheme.close()


DIVIDER_RE = re.compile(
    r"(SECTION\s+\d\s*[–-]\s*(CORE|ELECTIVES|OPTIONS))|"
    r"(PATTERNS\s+AND\s+PROCESSES)|(REGIONAL\s+GEOGRAPHY)", re.I)


def is_divider_or_blank(page):
    """A section-divider or blank page carrying no per-question marking."""
    t = page.get_text("text")
    if not t.strip():
        return True
    lines = [ln for ln in t.splitlines() if ln.strip()]
    return len(lines) <= 14 and bool(DIVIDER_RE.search(t)) and "[" not in t


PAGE_NUM_RE = re.compile(r"^(Page\s+\d+\s+of\s+\d+|\d{1,3})$", re.I)
DIVIDERISH_RE = re.compile(
    r"(SECTION\s+\d)|(PATTERNS\s+AND\s+PROCESSES)|(REGIONAL\s+GEOGRAPHY)|"
    r"(Questions?\s+\d+\s+to\s+\d+)|(Attempt\s+ONE)|(You\s+MUST\s+attempt)|"
    r"(^OR$)|(carry\s+\d+\s+marks)|(From\s+EITHER)", re.I)


def content_above(page, yf):
    """True if real (non-divider, non-page-number) text sits above y-frac yf."""
    for txt, _x0, y in lines_with_pos(page):
        if y >= yf - 1e-6:
            break
        s = txt.strip()
        if PAGE_NUM_RE.match(s) or DIVIDERISH_RE.search(s):
            continue
        return True
    return False


def main():
    dry = "--dry" in sys.argv
    written, dropped = [], []
    for year in YEARS:
        for fid in FILEIDS:
            paper_path = os.path.join(CORPUS, "exampapers", str(year), fid)
            scheme_path = os.path.join(CORPUS, "markingschemes", str(year), fid)
            tag = f"{year} {fid}"
            if not (os.path.exists(paper_path) and os.path.exists(scheme_path)):
                dropped.append((tag, "paper or scheme missing from corpus"))
                continue
            sidecar, evidence, problems = map_paper(paper_path, scheme_path)
            if sidecar is None:
                dropped.append((tag, "; ".join(problems) or "unknown"))
                continue
            out_dir = os.path.join(ANSWERS_DIR, str(year))
            out_path = os.path.join(out_dir, fid + ".json")
            if not dry:
                os.makedirs(out_dir, exist_ok=True)
                with open(out_path, "w") as f:
                    json.dump(sidecar, f, sort_keys=True, separators=(",", ":"))
            written.append((tag, out_path, len(sidecar["q"]), evidence))
            print(f"MAPPED  {tag}: {len(sidecar['q'])} questions -> {out_path}")
            for n, title, snippet in evidence:
                print(f"    Q{n:<2} title-hit: {title[:40]!r:44} crop: {snippet}")
    print()
    for tag, why in dropped:
        print(f"DROPPED {tag}: {why}")
    print(f"\n{len(written)} mapped, {len(dropped)} dropped"
          + (" (dry run — nothing written)" if dry else ""))


if __name__ == "__main__":
    main()
