#!/usr/bin/env python3
"""
Paper Trail — Wave 10: SECTION-ANCHORED maps (Politics & Society, Classical Studies).

Bespoke grammar for two subjects the generic engine drops:

  • Politics and Society (LC568, 2018–2025): the scheme carries per-question
    blocks for the Section A/B questions ("Question N" headers) and ONE common
    marking-criteria block (Section C) shared by every discursive-essay option.
    The paper's essay-menu questions all map to that block — that is genuinely
    the scheme's whole treatment of them, framed honestly via `label`.

  • Classical Studies (LC008, 2023–2025 new spec): Section A answers are keyed
    by bare "N." lead markers in the scheme; Section B essays (Q11(b)–Q16) share
    a common essay rubric block ("Question 11 (b) – Question 16" header).

Same safety posture as anchor-map.py: COUNT RECONCILE — every question on the
paper must land a region or the whole paper is dropped. Coordinates only.
Output sidecars are schema-identical (SIDECAR_V=1) and land in answers/<year>/.

Usage: python3 wave10_sections.py <corpusDir> <outDir>
  corpusDir contains {subjectId}_{year}_{level}_{paper|scheme}.pdf
  (downloaded from Firebase Storage — scripts/paper-trail/README.md).
"""
import json
import os
import re
import sys
from collections import defaultdict

import fitz  # pymupdf

SIDECAR_V = 1
COPYRIGHT = "© State Examinations Commission"
MAX_REGION_PAGES = 6

LIG = {"Ɵ": "ti", "ƫ": "tt", "ﬁ": "fi", "ﬂ": "fl", " ": " "}


def delig(s: str) -> str:
    for k, v in LIG.items():
        s = s.replace(k, v)
    return s


def lines_with_pos(page):
    """[(text, x0, yFrac)] for each text line on the page (sorted by y)."""
    H = page.rect.height
    out = []
    for blk in page.get_text("dict")["blocks"]:
        if blk.get("type") != 0:
            continue
        for ln in blk.get("lines", []):
            txt = delig("".join(sp["text"] for sp in ln.get("spans", []))).strip()
            if not txt:
                continue
            x0 = ln["bbox"][0]
            y = ln["bbox"][1] / H
            out.append((txt, x0, y))
    out.sort(key=lambda t: t[2])
    return out


Q_RE = re.compile(r"^(?:Question|Ceist)\s+(\d+)\b", re.I)
# 'N. text', 'N. 30 marks' or a standalone 'N.' line (CS schemes number answers
# with a bare marker line and put the body beside/below it).
LEAD_RE = re.compile(r"^(\d{1,2})\s?\.(\s|$)")


def paper_questions(doc):
    """First occurrence of each 'Question N' header: {n: (page1, yFrac)}."""
    seen = {}
    for pi in range(len(doc)):
        for txt, x0, y in lines_with_pos(doc[pi]):
            m = Q_RE.match(txt)
            if m:
                n = int(m.group(1))
                if n not in seen:
                    seen[n] = (pi + 1, y)
    return seen


def scheme_question_blocks(doc):
    """Per-question scheme blocks: {n: (page1, yFrac)}, headers 'Question N'."""
    seen = {}
    for pi in range(len(doc)):
        for txt, x0, y in lines_with_pos(doc[pi]):
            m = Q_RE.match(txt)
            if m:
                n = int(m.group(1))
                # ignore essay-range headers like 'Question 11 (b) – Question 16'
                if re.search(r"[–-]\s*(?:Question|Ceist)", txt, re.I):
                    continue
                if n not in seen:
                    seen[n] = (pi + 1, y)
    return seen


def scheme_lead_markers(doc, lo_page1, hi_page1):
    """Bare 'N.' markers inside [lo,hi): {n: (page1, yFrac)} (first hit)."""
    seen = {}
    for pi in range(lo_page1 - 1, min(hi_page1 - 1, len(doc))):
        for txt, x0, y in lines_with_pos(doc[pi]):
            if x0 > 120:
                continue
            m = LEAD_RE.match(txt)
            if m:
                n = int(m.group(1))
                if n not in seen:
                    seen[n] = (pi + 1, y)
    return seen


def find_header(doc, pattern, after=None):
    """First (page1, yFrac) whose line matches `pattern`, strictly after the
    (page1, yFrac) position `after` when given (skips front-matter look-alikes)."""
    rx = re.compile(pattern, re.I)
    for pi in range(len(doc)):
        for txt, x0, y in lines_with_pos(doc[pi]):
            if after and (pi + 1, y) <= after:
                continue
            if rx.search(txt):
                return (pi + 1, y)
    return None


def region_between(start, end, scheme_len):
    """Crop segs from (page1,yFrac) start to end (or doc end). Ends exclusive."""
    sp, sy = start
    ep, ey = end if end else (scheme_len, 1.0)
    if end and (ep, ey) <= (sp, sy):
        return None
    segs = []
    if ep == sp:
        segs.append({"p": sp, "r": [0.0, round(sy, 4), 1.0, round(ey, 4)]})
    else:
        segs.append({"p": sp, "r": [0.0, round(sy, 4), 1.0, 1.0]})
        for p in range(sp + 1, min(ep, sp + MAX_REGION_PAGES)):
            segs.append({"p": p, "r": [0.0, 0.0, 1.0, 1.0]})
        if ep - sp < MAX_REGION_PAGES and ey > 0.02:
            segs.append({"p": ep, "r": [0.0, 0.0, 1.0, round(ey, 4)]})
    return segs[:MAX_REGION_PAGES]


def paper_yband(qmap, n, doc_len):
    """Paper band for question n: header y to next header on same page else 1.0."""
    p, y = qmap[n]
    same = sorted(yy for (pp, yy) in qmap.values() if pp == p and yy > y + 1e-6)
    return [round(y, 4), round(same[0], 4) if same else 1.0]


def build_map(paper_path, scheme_path, subject, lang="ev"):
    iv = lang == "iv"
    paper = fitz.open(paper_path)
    scheme = fitz.open(scheme_path)
    S = len(scheme)
    pq = paper_questions(paper)
    if not pq:
        return None, "no paper questions detected"
    ns = sorted(pq)
    if ns != list(range(1, len(ns) + 1)):
        return None, f"paper question sequence not 1..N: {ns}"

    sq = scheme_question_blocks(scheme)
    qs = []

    if subject == "politics-and-society":
        rubric = find_header(scheme, r"^(?:Section|Roinn)\s+C\b")
        if not rubric:
            return None, "no Section C rubric block in scheme"
        # per-question blocks, ordered; regions run block→next block / rubric
        block_ns = sorted(n for n in sq if n in pq)
        for i, n in enumerate(block_ns):
            nxt = sq[block_ns[i + 1]] if i + 1 < len(block_ns) else rubric
            segs = region_between(sq[n], nxt, S)
            if not segs:
                return None, f"empty scheme block for Q{n}"
            qs.append((n, segs, None))
        menu_ns = [n for n in ns if n not in sq]
        # essay menu: every remaining question maps to the common §C criteria
        rsegs = region_between(rubric, None, S)
        for n in menu_ns:
            if n <= max(block_ns, default=0):
                return None, f"unmatched non-essay question Q{n}"
            qs.append((n, rsegs,
                       (f"Ceist {n} · Roinn C — critéir choiteanna mharcála" if iv
                        else f"Question {n} · Section C — common marking criteria")))
    elif subject == "classical-studies":
        ESSAY_PAT = (r"(Question\s+11\s*\(b\)\s*[–-]\s*Question\s+16"
                     r"|Questions?\s+12\s*[–-]\s*16"
                     r"|Each of these questions has the same marking scheme"
                     # Irish-medium (IV) twins of the same headers
                     r"|Ceist\s+11\s*\(b\)\s*[–-]\s*Ceist\s+16"
                     r"|Ceisteanna\s+12\s*[–-]\s*16:"
                     r"|^12\.?\s*[–-]\s*16\b"
                     r"|úsáidtear an scéim mharcála ch?éanna"
                     r"|^Le haghaidh gach ceann de na ceisteanna)")
        # Q11's own block starts at 'Question 11' or the '11a …' descriptor grid.
        q11 = sq.get(11) or find_header(scheme, r"^11a\b")
        # Common essay block: positioned AFTER Q11's block start when Q11 has one
        # (skips the front-matter 'Questions 11b-16' general-info look-alikes).
        essay_hdr = find_header(scheme, ESSAY_PAT, after=q11)
        if not essay_hdr:
            return None, "no common essay header in scheme"
        q11_own = q11 is not None and (q11[0], q11[1]) < (essay_hdr[0], essay_hdr[1])
        a_end = q11 if q11_own else essay_hdr
        # Section A (Q1–10): lead 'N.' markers before the Q11/common block
        lead = scheme_lead_markers(scheme, 1, a_end[0] + 1)
        marks = {n: lead[n] for n in range(1, 11)
                 if n in lead and (lead[n][0], lead[n][1]) < (a_end[0], a_end[1])}
        if sorted(marks) != list(range(1, 11)):
            # 2026 restyle: Section A blocks are headed 'Question N.  20 marks'
            # (no bare lead-ints). Same semantics, different marker — reuse the
            # 'Question N' block positions already collected in sq.
            marks = {n: sq[n] for n in range(1, 11)
                     if n in sq and (sq[n][0], sq[n][1]) < (a_end[0], a_end[1])}
        if sorted(marks) != list(range(1, 11)):
            return None, f"section A markers incomplete: {sorted(marks)}"
        for n in range(1, 11):
            nxt = marks.get(n + 1) or a_end
            segs = region_between(marks[n], nxt, S)
            if not segs:
                return None, f"empty region Q{n}"
            qs.append((n, segs, None))
        start = 11
        if q11_own:
            segs = region_between(q11, essay_hdr, S)
            if segs:
                qs.append((11, segs, None))
                start = 12
        rsegs = region_between(essay_hdr, None, S)
        for n in range(start, max(ns) + 1):
            qs.append((n, rsegs,
                       (f"Ceist {n} · scéim mharcála choiteann na n-aistí" if iv
                        else f"Question {n} · common essay marking scheme")))
    else:
        return None, f"unknown subject grammar {subject}"

    # COUNT RECONCILE: every paper question covered, monotonic, in-band
    covered = sorted(n for n, _, _ in qs)
    if covered != ns:
        return None, f"reconcile failed: paper {ns} vs mapped {covered}"

    out_qs = []
    for n, segs, label in sorted(qs):
        q = {
            "n": str(n),
            "pP": pq[n][0],
            "pY": paper_yband(pq, n, len(paper)),
            "region": segs,
            "mode": "crop",
            "conf": 1.0,
        }
        if label:
            q["label"] = label
        out_qs.append(q)

    sidecar = {
        "v": SIDECAR_V,
        "paperFileid": os.path.basename(paper_path),
        "schemeFileid": os.path.basename(scheme_path),
        "component": "000",
        "band": [1, S + 1],
        "copyright": COPYRIGHT,
        "q": out_qs,
    }
    return sidecar, None


def main():
    corpus, outdir = sys.argv[1], sys.argv[2]
    targets = json.load(open(os.path.join(corpus, "..", "targets.json")))
    ok = drop = 0
    for t in targets:
        pp = os.path.join(corpus, f"{t['sid']}_{t['year']}_{t['level']}_paper.pdf")
        sp = os.path.join(corpus, f"{t['sid']}_{t['year']}_{t['level']}_scheme.pdf")
        if not (os.path.exists(pp) and os.path.exists(sp)):
            continue
        sidecar, err = build_map(pp, sp, t["sid"], t.get("lang", "ev"))
        if sidecar is None:
            print(f"DROP {t['sid']} {t['year']} {t['level']}: {err}")
            drop += 1
            continue
        sidecar["paperFileid"] = t["f"]
        sidecar["schemeFileid"] = t["s"]
        os.makedirs(os.path.join(outdir, str(t["year"])), exist_ok=True)
        with open(os.path.join(outdir, str(t["year"]), f"{t['f']}.json"), "w") as fh:
            json.dump(sidecar, fh, sort_keys=True, separators=(",", ":"))
        print(f"OK   {t['sid']} {t['year']} {t['level']}: {len(sidecar['q'])} questions")
        ok += 1
    print(f"\nmapped {ok} · dropped {drop}")


if __name__ == "__main__":
    main()
