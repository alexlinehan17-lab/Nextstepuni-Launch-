#!/usr/bin/env python3
"""Paper Trail — full-estate chip audit (coverage + correctness triage).

For every committed sidecar:

COVERAGE — detect top-level question headers printed on the paper (strict,
multi-pattern, ascending-gated) and report any that no chip's paper band
covers. Sub-parts under a covered header are fine by design.

CORRECTNESS — for each chip, compare content words near the paper anchor
against the opening of the scheme region it points to. High overlap means the
scheme restates the question (proof of correct pairing); low overlap is only a
TRIAGE signal (numeric/indicative schemes legitimately score low) — the output
ranks papers for render inspection, it never edits anything.

Output: out/audit-report.tsv (one row per paper) + out/audit-flags.tsv (one
row per finding), sorted worst-first.

Usage: python3 audit_chips.py [--codes LC003,LC025] [--years 2024,2025]
"""
import json
import os
import re
import sys
from collections import defaultdict

import fitz

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
CORPUS = os.path.join(REPO, "paper-trail-corpus")
ANSWERS = os.path.join(HERE, "answers")
OUT = os.path.join(HERE, "out")

Q_WORD = re.compile(
    r"^(?:Question|QUESTION|Ceist|CEIST|Cuestión|Pytanie|Tehtävä|Qu\.?)\s+(\d{1,2})\b")
Q_NUM = re.compile(r"^(\d{1,2})\s*\.(?:\s|$)")
STOP = {"the", "and", "that", "with", "this", "from", "have", "your",
        "each", "agus", "leis", "seo", "sin", "for", "are", "was"}


def lines_of(page):
    lines = defaultdict(list)
    for w in page.get_text("words"):
        lines[(w[5], w[6])].append(w)
    out = []
    H = page.rect.height
    for k in sorted(lines):
        lw = sorted(lines[k], key=lambda w: w[0])
        out.append((" ".join(w[4] for w in lw), lw[0][0], lw[0][1] / H))
    out.sort(key=lambda t: t[2])
    return out


def detect_questions(paper):
    """[(n, page1, y)] — worded headers anywhere; bare 'N.' only in an
    ascending run (start at 1) at the left margin, the campaign's calibrated
    compromise between recall and passage-paragraph noise."""
    worded, bare = {}, {}
    num = 0
    for pi in range(1, len(paper)):
        for txt, x0, y in lines_of(paper[pi]):
            t = txt.strip()
            m = Q_WORD.match(t)
            if m and x0 < 150:
                n = int(m.group(1))
                if 0 < n <= 25 and n not in worded:
                    worded[n] = (pi + 1, y)
                continue
            m = Q_NUM.match(t)
            if m and x0 < 80:
                n = int(m.group(1))
                if n == num + 1:
                    num = n
                    bare[n] = (pi + 1, y)
    # worded headers win; bare fills only if it found a longer clean run
    if len(worded) >= 3 or (worded and len(bare) < 3):
        return worded
    if len(bare) > len(worded):
        return bare
    return worded or bare


def words_of_clip(page, y0, y1, cap=60):
    H = page.rect.height
    out = []
    for w in page.get_text("words"):
        if y0 <= w[1] / H <= y1:
            t = re.sub(r"\W+", "", w[4]).lower()
            if len(t) >= 4 and t not in STOP:
                out.append(t)
            if len(out) >= cap:
                return out
    return out


def audit_paper(year, fname, sc):
    ppath = os.path.join(CORPUS, "exampapers", year, sc["paperFileid"])
    spath = os.path.join(CORPUS, "markingschemes", year, sc["schemeFileid"])
    if not (os.path.exists(ppath) and os.path.exists(spath)):
        return None, ["missing-pdf"]
    paper, scheme = fitz.open(ppath), fitz.open(spath)
    flags = []
    qs = sc["q"]

    # --- structural sanity
    for q in qs:
        if not (1 <= q["pP"] <= len(paper)):
            flags.append(f"chip{q['n']}:paper-page-out-of-range")
        for seg in q["region"]:
            seg.setdefault("r", [0.0, 0.0, 1.0, 1.0])
            if not (1 <= seg["p"] <= len(scheme)):
                flags.append(f"chip{q['n']}:scheme-page-out-of-range")

    # --- coverage
    detected = detect_questions(paper)
    # chip numbers: explicit n, or the FIRST QN token in the label
    chip_ns = set()
    numbered = 0
    for q in qs:
        n = None
        if str(q.get("n", "")).isdigit():
            n = int(q["n"])
        lab = q.get("label") or ""
        m = re.search(r"[QC](?:eist|uestion|uid)?\.?\s*(\d{1,2})\b", lab)
        if m:
            n = int(m.group(1))
        if n is not None:
            chip_ns.add(n)
            numbered += 1
    question_style = (numbered >= 0.6 * len(qs)
                      and len(qs) >= 0.5 * max(1, len(detected)))
    if question_style and detected:
        missing = sorted(set(detected) - chip_ns)
    else:
        # band-style: chips partition the paper from the first anchor on —
        # only questions printed BEFORE the first chip's anchor are uncovered
        first = min((q["pP"], q["pY"][0]) for q in qs) if qs else (1, 0.0)
        missing = sorted(n for n, (pg, y) in detected.items()
                         if (pg, y) < (first[0], first[1] - 0.03))

    # --- correctness overlap
    lows = 0
    scores = []
    for q in qs:
        pw = set(words_of_clip(paper[q["pP"] - 1], q["pY"][0],
                               min(1.0, q["pY"][0] + 0.25)))
        seg = q["region"][0]
        sw = set(words_of_clip(scheme[seg["p"] - 1], seg["r"][1],
                               min(1.0, seg["r"][1] + 0.5), cap=120))
        if seg["r"][3] - seg["r"][1] > 0.9 and len(q["region"]) > 1:
            nxt = q["region"][1]
            sw |= set(words_of_clip(scheme[nxt["p"] - 1], 0.0, 0.5, cap=120))
        inter = len(pw & sw)
        score = inter / max(1, min(len(pw), 25))
        scores.append(round(score, 2))
        if score < 0.08 and len(pw) >= 5:
            lows += 1
    mean = round(sum(scores) / len(scores), 3) if scores else 0.0
    row = {
        "year": year, "file": fname, "chips": len(qs),
        "detected": len(detected), "missing": missing,
        "mean_overlap": mean, "low_chips": lows,
    }
    if missing:
        flags.append(f"uncovered:{missing}")
    if scores and lows == len(scores):
        flags.append("all-chips-zero-overlap")
    return row, flags


def main():
    codes = years = None
    for i, a in enumerate(sys.argv):
        if a == "--codes":
            codes = set(sys.argv[i + 1].split(","))
        if a == "--years":
            years = set(sys.argv[i + 1].split(","))
    rows, flagged = [], []
    for year in sorted(os.listdir(ANSWERS)):
        ydir = os.path.join(ANSWERS, year)
        if not os.path.isdir(ydir) or (years and year not in years):
            continue
        for f in sorted(os.listdir(ydir)):
            if not f.endswith(".json"):
                continue
            if codes and f[:5] not in codes:
                continue
            try:
                sc = json.load(open(os.path.join(ydir, f)))
                row, flags = audit_paper(year, f, sc)
            except Exception as e:
                row, flags = None, [f"error:{e}"]
            if row:
                rows.append(row)
            for fl in flags:
                flagged.append((year, f, fl))
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "audit-report.tsv"), "w") as fh:
        fh.write("year\tfile\tchips\tdetected\tmissing\tmean_overlap\tlow_chips\n")
        for r in rows:
            fh.write(f"{r['year']}\t{r['file']}\t{r['chips']}\t{r['detected']}"
                     f"\t{r['missing']}\t{r['mean_overlap']}\t{r['low_chips']}\n")
    with open(os.path.join(OUT, "audit-flags.tsv"), "w") as fh:
        for y, f, fl in flagged:
            fh.write(f"{y}\t{f}\t{fl}\n")
    n_gap = sum(1 for r in rows if r["missing"])
    n_zero = sum(1 for _, _, fl in flagged if fl == "all-chips-zero-overlap")
    print(f"audited {len(rows)} papers · {n_gap} with uncovered questions · "
          f"{n_zero} all-zero-overlap · {len(flagged)} flags total")
    print("→ out/audit-report.tsv, out/audit-flags.tsv")


if __name__ == "__main__":
    main()
