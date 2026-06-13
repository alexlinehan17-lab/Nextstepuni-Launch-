#!/usr/bin/env python3
"""
Paper Trail — Stage 2.5: build per-paper question→answer ANCHOR MAPS.

Runs AFTER download.py, BEFORE build-index.py. For each in-scope exam paper that
has a marking scheme, it precomputes — by reading the REAL corpus PDFs with
pymupdf (fitz), deterministically — a coordinates-only sidecar that lets the
viewer drop a CROP of the scheme's own pixels beside each question. It ships NO
answer text and NO image bytes: only page numbers + fractional rectangles.

GENERALISED ENGINE (auto-grammar). Rather than a hand-authored grammar per
subject, the engine TRIES several question-numbering patterns and self-validates:

  • PAPER question headers — detectors tried in turn, best clean run wins:
      'question'  word 'Question'/'QUESTION' + integer at the left margin
                  (Maths, Ag Science, Computer Science, PE, Mandarin…)
      'lead_int'  a bare 'N.' starting a line at the left margin
                  (Biology, Physics, Geography and most sciences)
      'qtoken'    a 'Q1'/'Q.1' token at the left margin
    The winner is the detector giving the longest CLEAN monotonic 1..N sequence
    at a consistent left-margin x (deduped per number).

  • SCHEME markers — the same three detectors, restricted to the paper's band;
    the one whose number-set best covers the paper's questions wins.

  • COUNT RECONCILE is the safety gate: a paper is mapped only when EVERY one of
    its questions has a matching, monotonic scheme marker (confidence 1.0).
    Anything short of that is reported and DROPPED (better no chip than a wrong
    one). Rotation, over-long spans and uncertain boundaries degrade to a
    reliable page-jump exactly as before.

  • COMPONENT-BAND SPLIT still applies when sibling papers SHARE one scheme file
    (e.g. Maths P1+P2 → LC003ALP000EV, split on 'Paper 1'/'Paper 2' dividers).
    Subjects whose papers each have their own scheme use the whole scheme.

Scope (wave 1): Leaving Cert, Higher + Ordinary level, English version, 2022–2025.
Aural/listening and Irish-medium are out (they fail detection and drop cleanly).
The `answers:1` flag that lights a profile is STILL gated by
QA_PASSED_ANSWER_PROFILES in build-index.py — nothing ships unverified.

Output (deterministic, sorted, idempotent — safe to re-run):
  scripts/paper-trail/answers/<year>/<paperFileid>.json   (committed sidecars)
  scripts/paper-trail/out/answers-manifest.jsonl          (build-index input)
  scripts/paper-trail/out/answers-report.md               (coverage + confidence)

All emitted page numbers are 1-BASED (pdf.js getPage / viewer data-page).
All rects are fractions of the (unrotated) page box.
"""

import json
import os
import re
import sys
from collections import Counter, defaultdict

import fitz  # pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
OUT_DIR = os.path.join(HERE, "out")
CORPUS = os.path.join(REPO, "paper-trail-corpus")
MANIFEST = os.path.join(OUT_DIR, "manifest.jsonl")
ANSWERS_DIR = os.path.join(HERE, "answers")          # committed sidecars
ANSWERS_MANIFEST = os.path.join(OUT_DIR, "answers-manifest.jsonl")
ANSWERS_REPORT = os.path.join(OUT_DIR, "answers-report.md")

SIDECAR_V = 1
COPYRIGHT = "© State Examinations Commission"
LEFT_MARGIN_X = 140      # a header/marker token must start left of this (points)
LEAD_INT_X = 95          # a 'N.' lead number sits within this of the left edge
MAX_REGION_PAGES = 6     # a question's scheme region longer than this → pagejump
DIVIDER_TOP_FRAC = 0.5   # a band divider title sits in the top half of its page
BLANK_MAX_DRAWINGS = 3   # a filler page may carry a footer rule; a real page many
MIN_QUESTIONS = 3        # a paper needs ≥3 clean questions to be worth mapping

# fileid grammar (mirrors build-index.py): {LC|JC|LB}{SSS}{LVL}L?P{CCC}{LANG}.pdf
FILEID_RE = re.compile(r"^(LC|JC|LB)(\d{3})([A-Z])L?P([A-Z0-9]{3})(EV|IV|BV)\.pdf$", re.I)

# Scope. SCOPE_CODES None = all subjects; a set = only those SEC codes (used to
# extend already-verified subjects to more years without re-mapping the rest).
SCOPE_EXAM = "LC"
SCOPE_LEVELS = {"A", "G"}           # higher, ordinary
SCOPE_LANGS = {"EV"}
SCOPE_YEARS = set(range(2010, 2026))
SCOPE_CODES = None  # which codes to ATTEMPT this run; None = all not in DONE_CODES
# Subjects already verified + lit in earlier waves. The engine never re-maps or
# clears these (their committed sidecars are final), so each new wave is additive.
DONE_CODES = {
    "LC003", "LC022", "LC023", "LC024", "LC225", "LC029", "LC014", "LC007",
    "LC559", "LC038", "LC017", "LC049", "LC557", "LC019", "LC553", "LC558",
}
# Aural / unprepared-listening / non-level components never carry page questions.
SKIP_COMPONENTS = {"A00", "U00"}


def log(msg):
    print(msg, flush=True)


def decode_fileid(fileid):
    m = FILEID_RE.match(fileid)
    if not m:
        return None
    return {
        "exam": m.group(1).upper(),
        "code": (m.group(1) + m.group(2)).upper(),
        "levelCode": m.group(3).upper(),
        "component": m.group(4).upper(),
        "lang": m.group(5).upper(),
    }


def corpus_path(view, year, fileid):
    return os.path.join(CORPUS, view, str(year), fileid)


# ─── PDF reading primitives ──────────────────────────────────────────────────

def line_groups(page):
    """get_text('words') grouped into lines, each sorted left→right.
    word = (x0, y0, x1, y1, text, block_no, line_no, word_no)."""
    lines = defaultdict(list)
    for w in page.get_text("words"):
        lines[(w[5], w[6])].append(w)
    for lw in lines.values():
        lw.sort(key=lambda w: w[0])
    return list(lines.values())


# ─── question-number detectors (return raw [(n, page0, x0, yFrac)]) ──────────

def _det_question_word(doc):
    hits = []
    for pi, page in enumerate(doc):
        if page.rotation:
            continue
        H = page.rect.height
        for lw in line_groups(page):
            for i, w in enumerate(lw):
                if (w[4] in ("Question", "QUESTION") and w[0] < LEFT_MARGIN_X
                        and i + 1 < len(lw) and re.fullmatch(r"\d+", lw[i + 1][4])):
                    hits.append((int(lw[i + 1][4]), pi, w[0], w[1] / H))
    return hits


def _det_lead_int(doc):
    hits = []
    for pi, page in enumerate(doc):
        if page.rotation:
            continue
        H = page.rect.height
        for lw in line_groups(page):
            if not lw:
                continue
            w = lw[0]
            m = re.fullmatch(r"(\d{1,2})\.", w[4])
            if m and w[0] < LEAD_INT_X:
                hits.append((int(m.group(1)), pi, w[0], w[1] / H))
    return hits


def _det_q_token(doc):
    hits = []
    for pi, page in enumerate(doc):
        if page.rotation:
            continue
        H = page.rect.height
        for lw in line_groups(page):
            for w in lw:
                m = re.fullmatch(r"Q\.?(\d{1,2})", w[4])
                if m and w[0] < LEFT_MARGIN_X:
                    hits.append((int(m.group(1)), pi, w[0], w[1] / H))
                    break
    return hits


DETECTORS = [("question", _det_question_word), ("lead_int", _det_lead_int), ("qtoken", _det_q_token)]


def best_sequence(hits):
    """Clean a detector's hits to the longest contiguous 1..N at a consistent
    left-margin x (deduped per number). Returns sorted [(n,page0,x0,yFrac)] or None."""
    if not hits:
        return None
    xs = Counter(round(h[2] / 5) * 5 for h in hits)
    best = None
    for xb, _ in xs.most_common(5):
        f = [h for h in hits if abs(h[2] - xb) <= 7]
        f.sort(key=lambda h: (h[1], h[3]))
        first = {}
        for n, pi, x, y in f:
            if n not in first:
                first[n] = (n, pi, x, y)
        ns = sorted(first)
        if ns == list(range(1, len(ns) + 1)) and len(ns) >= MIN_QUESTIONS:
            seq = [first[n] for n in ns]
            if best is None or len(seq) > len(best):
                best = seq
    return best


def detect_paper_headers(doc):
    """Best (detector_name, [(n,page0,x0,yFrac)]) across detectors, or None."""
    best = None
    for name, fn in DETECTORS:
        seq = best_sequence(fn(doc))
        if seq and (best is None or len(seq) > len(best[1])):
            best = (name, seq)
    return best


def _marker_map(hits, band_start, band_end):
    """First in-band occurrence of each number at the modal left-margin x →
    {n: (page0, yFrac)}."""
    inb = [h for h in hits if band_start <= h[1] < band_end]
    if not inb:
        return {}
    xs = Counter(round(h[2] / 5) * 5 for h in inb)
    best = {}
    for xb, _ in xs.most_common(5):
        f = [h for h in inb if abs(h[2] - xb) <= 7]
        f.sort(key=lambda h: (h[1], h[3]))
        m = {}
        for n, pi, x, y in f:
            if n not in m:
                m[n] = (pi, y)
        if len(m) > len(best):
            best = m
    return best


def detect_scheme_markers(doc, band_start, band_end, want_ns):
    """The detector whose in-band number-set best covers the paper's questions."""
    best, best_score = {}, -1
    for _, fn in DETECTORS:
        m = _marker_map(fn(doc), band_start, band_end)
        score = len(set(m) & want_ns)
        if score > best_score:
            best, best_score = m, score
    return best


def find_band(scheme, divider_title):
    """0-based page index of the FIRST top-of-page occurrence of the band divider
    title (e.g. 'Paper 1'). Returns None if not found."""
    for pi, page in enumerate(scheme):
        if page.rotation:
            continue
        H = page.rect.height
        for r in page.search_for(divider_title):
            if r.y0 < H * DIVIDER_TOP_FRAC:
                return pi
    return None


def is_blank(page):
    """A scheme page carrying no answer content (trailing filler/blank)."""
    if page.get_text("text").strip():
        return False
    if page.get_images():
        return False
    try:
        if len(page.get_drawings()) > BLANK_MAX_DRAWINGS:
            return False
    except Exception:
        pass
    return True


def last_nonblank_page(doc, start, band_end):
    e = band_end - 1
    while e > start and is_blank(doc[e]):
        e -= 1
    return e


# ─── per-paper mapping ───────────────────────────────────────────────────────

def map_paper(paper_path, scheme_path, band_strategy):
    """Returns (sidecar_or_None, stats)."""
    stats = {"crop": 0, "pagejump": 0, "omit": 0, "reason": None,
             "detector": None, "conf": 0.0}

    paper = fitz.open(paper_path)
    scheme = fitz.open(scheme_path)

    ph = detect_paper_headers(paper)
    if not ph:
        stats["reason"] = "no clean paper question sequence"
        return None, stats
    detector, seq = ph
    stats["detector"] = detector
    headers = sorted(seq, key=lambda h: (h[1], h[3]))  # (n, page0, x0, yFrac)
    want_ns = {h[0] for h in headers}
    N = len(headers)

    # Band for this paper within (possibly shared) scheme.
    if band_strategy[0] == "divider":
        k = band_strategy[1]
        band_start = find_band(scheme, f"Paper {k}")
        if band_start is None:
            stats["reason"] = f"band 'Paper {k}' not found"
            return None, stats
        nxt = find_band(scheme, f"Paper {k + 1}")
        band_end = nxt if (nxt is not None and nxt > band_start) else len(scheme)
    else:
        band_start, band_end = 0, len(scheme)

    markers = detect_scheme_markers(scheme, band_start, band_end, want_ns)
    matched = sum(1 for n in want_ns if n in markers)
    stats["conf"] = round(matched / N, 3)
    # Strict gate: every paper question must have a scheme marker.
    if matched < N:
        stats["reason"] = f"count reconcile {matched}/{N} (detector {detector})"
        return None, stats
    seq_pts = [markers[n] for n in sorted(markers) if n in want_ns]
    mono = all(seq_pts[i] < seq_pts[i + 1] for i in range(len(seq_pts) - 1))
    if not mono:
        stats["reason"] = "scheme markers not monotonic"
        return None, stats

    # paper question y-band end (next header on same page, else page bottom)
    by_page = defaultdict(list)
    for n, pi, x0, y in headers:
        by_page[pi].append((y, n))
    for pi in by_page:
        by_page[pi].sort()

    qout = []
    maxn = max(markers)
    for n, p_pi, p_x0, p_y in headers:
        same = by_page[p_pi]
        nxt_same = next((yf for yf, nn in same if yf > p_y + 1e-6), 1.0)
        p_yband = [round(p_y, 4), round(nxt_same, 4)]

        s_pi, s_yfrac = markers[n]
        end = markers.get(n + 1)
        degrade = False
        if end is not None and end > (s_pi, s_yfrac):
            e_pi, e_yfrac = end
        elif n == maxn:
            e_pi, e_yfrac = last_nonblank_page(scheme, s_pi, band_end), 1.0
        else:
            degrade = True
            e_pi, e_yfrac = s_pi, 1.0

        span = e_pi - s_pi
        region = []
        ok = not degrade
        if not ok:
            pass
        elif span == 0:
            region.append({"p": s_pi + 1, "r": [0.0, round(s_yfrac, 4), 1.0, round(e_yfrac, 4)]})
        elif 0 < span <= MAX_REGION_PAGES:
            region.append({"p": s_pi + 1, "r": [0.0, round(s_yfrac, 4), 1.0, 1.0]})
            for mid in range(s_pi + 1, e_pi):
                region.append({"p": mid + 1, "r": [0.0, 0.0, 1.0, 1.0]})
            region.append({"p": e_pi + 1, "r": [0.0, 0.0, 1.0, round(e_yfrac, 4)]})
        else:
            ok = False

        if ok:
            for seg in region:
                if any(not (0.0 <= v <= 1.0) for v in seg["r"]) or scheme[seg["p"] - 1].rotation:
                    ok = False
                    break

        if ok:
            qout.append({"n": str(n), "pP": p_pi + 1, "pY": p_yband,
                         "region": region, "mode": "crop", "conf": 1.0})
            stats["crop"] += 1
        else:
            qout.append({"n": str(n), "pP": p_pi + 1, "pY": p_yband,
                         "region": [{"p": s_pi + 1}], "mode": "pagejump", "conf": 0.6})
            stats["pagejump"] += 1

    if not qout:
        stats["reason"] = "no questions mapped"
        return None, stats

    sidecar = {
        "v": SIDECAR_V,
        "paperFileid": os.path.basename(paper_path),
        "schemeFileid": os.path.basename(scheme_path),
        "component": band_strategy[2] if len(band_strategy) > 2 else "",
        "band": [band_start + 1, band_end + 1],
        "copyright": COPYRIGHT,
        "q": qout,
    }
    return sidecar, stats


# ─── pairing + band strategy ─────────────────────────────────────────────────

def build_pairs(rows):
    """[(paperRow, schemeRow, band_strategy, levelCode)] for in-scope papers.
    band_strategy = ('whole', component) or ('divider', k, component)."""
    papers = defaultdict(list)   # (code, year, level, lang) -> [(row, decoded)]
    schemes = defaultdict(list)
    for r in rows:
        d = decode_fileid(r["fileid"])
        if not d or d["exam"] != SCOPE_EXAM:
            continue
        if d["code"] in DONE_CODES:
            continue  # frozen — lit in an earlier wave, never re-mapped
        if SCOPE_CODES is not None and d["code"] not in SCOPE_CODES:
            continue
        if d["levelCode"] not in SCOPE_LEVELS or d["lang"] not in SCOPE_LANGS:
            continue
        if int(r["year"]) not in SCOPE_YEARS or d["component"] in SKIP_COMPONENTS:
            continue
        key = (d["code"], int(r["year"]), d["levelCode"], d["lang"])
        (papers if r["view"] == "exampapers" else schemes)[key].append((r, d))

    pairs = []
    for key in sorted(papers):
        plist = sorted(papers[key], key=lambda x: x[0]["fileid"])
        cands = schemes.get(key, [])
        # pair each paper to a scheme: same component, else the 000 whole-level scheme
        paired = []
        for prow, pd in plist:
            scheme = None
            for srow, sd in cands:
                if sd["component"] == pd["component"]:
                    scheme = srow
                    break
            if scheme is None:
                for srow, sd in cands:
                    if sd["component"] == "000":
                        scheme = srow
                        break
            if scheme is not None:
                paired.append((prow, pd, scheme))
        # detect shared scheme files within this profile-year
        scheme_users = defaultdict(list)
        for prow, pd, scheme in paired:
            scheme_users[scheme["fileid"]].append(pd["component"])
        for prow, pd, scheme in paired:
            comps = sorted(set(scheme_users[scheme["fileid"]]))
            if len(comps) > 1:
                k = comps.index(pd["component"]) + 1  # 1-based rank → "Paper k"
                strat = ("divider", k, pd["component"])
            else:
                strat = ("whole", pd["component"])
            pairs.append((prow, scheme, strat, pd["levelCode"]))
    return pairs


def main():
    log("Paper Trail — Stage 2.5: anchor maps (auto-grammar)")
    if not os.path.exists(MANIFEST):
        log(f"FATAL: {MANIFEST} missing — run enumerate.py first")
        return 1
    rows, seen = [], set()
    with open(MANIFEST, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            k = (r["view"], r["year"], r["fileid"])
            if k in seen or not r["fileid"].lower().endswith(".pdf"):
                continue
            seen.add(k)
            rows.append(r)

    pairs = build_pairs(rows)
    log(f"  in-scope papers: {len(pairs)}")

    # Clear only the sidecars this run will regenerate (in-scope, not frozen) so
    # earlier waves' committed sidecars survive — each wave is additive.
    def in_scope_code(code):
        return code not in DONE_CODES and (SCOPE_CODES is None or code in SCOPE_CODES)
    if os.path.isdir(ANSWERS_DIR):
        for yd in os.listdir(ANSWERS_DIR):
            ydp = os.path.join(ANSWERS_DIR, yd)
            if os.path.isdir(ydp):
                for fn in os.listdir(ydp):
                    if in_scope_code(fn[:5]):
                        os.remove(os.path.join(ydp, fn))

    manifest_lines, report_rows = [], []
    fully = degraded = dropped = 0
    by_subject = defaultdict(lambda: {"mapped": 0, "dropped": 0, "detector": set()})

    for prow, srow, strat, level in sorted(pairs, key=lambda p: (int(p[0]["year"]), p[0]["fileid"])):
        year = int(prow["year"])
        pfile, sfile = prow["fileid"], srow["fileid"]
        subj = prow["subjectName"].strip()
        ppath = corpus_path("exampapers", year, pfile)
        spath = corpus_path("markingschemes", year, sfile)
        if not (os.path.exists(ppath) and os.path.exists(spath)):
            continue

        sidecar, st = map_paper(ppath, spath, strat)
        if sidecar is None:
            dropped += 1
            by_subject[subj]["dropped"] += 1
            report_rows.append((subj, year, level, pfile, "DROP", st))
            manifest_lines.append({"year": year, "paperFileid": pfile, "schemeFileid": sfile,
                                   "mapped": False, "reason": st["reason"]})
            continue

        bs, be = sidecar["band"]
        for q in sidecar["q"]:
            for seg in q["region"]:
                assert bs <= seg["p"] < be, f"{pfile} Q{q['n']} page {seg['p']} escapes band [{bs},{be})"
        ydir = os.path.join(ANSWERS_DIR, str(year))
        os.makedirs(ydir, exist_ok=True)
        with open(os.path.join(ydir, f"{pfile}.json"), "w", encoding="utf-8") as fh:
            json.dump(sidecar, fh, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        status = "FULL" if st["pagejump"] == 0 and st["omit"] == 0 else "PARTIAL"
        fully += status == "FULL"
        degraded += status == "PARTIAL"
        by_subject[subj]["mapped"] += 1
        by_subject[subj]["detector"].add(st["detector"])
        report_rows.append((subj, year, level, pfile, status, st))
        manifest_lines.append({"year": year, "paperFileid": pfile, "schemeFileid": sfile,
                               "mapped": True, "nCrop": st["crop"], "nPagejump": st["pagejump"],
                               "detector": st["detector"]})

    with open(ANSWERS_MANIFEST, "w", encoding="utf-8") as f:
        for row in sorted(manifest_lines, key=lambda r: (r["year"], r["paperFileid"])):
            f.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")

    # report
    rep = ["# Paper Trail — Stage 2.5 anchor-map report (auto-grammar)", ""]
    rep.append(f"Scope: {SCOPE_EXAM} levels {sorted(SCOPE_LEVELS)} langs {sorted(SCOPE_LANGS)} "
               f"years {min(SCOPE_YEARS)}–{max(SCOPE_YEARS)}.")
    rep.append(f"\n**{fully} full · {degraded} partial · {dropped} dropped** "
               f"({fully + degraded}/{fully + degraded + dropped} papers mapped)\n")
    rep.append("## Per-subject coverage (mapped / total, detector)")
    rep.append("")
    rep.append("| subject | mapped | dropped | detector |")
    rep.append("|---|---|---|---|")
    for subj in sorted(by_subject):
        d = by_subject[subj]
        det = ",".join(sorted(x for x in d["detector"] if x)) or "—"
        rep.append(f"| {subj} | {d['mapped']} | {d['dropped']} | {det} |")
    rep.append("\n## Per-paper detail\n")
    rep.append("| subject | year | lvl | paper | status | detail |")
    rep.append("|---|---|---|---|---|---|")
    for subj, year, level, pfile, status, st in report_rows:
        detail = (f"{st['crop']}crop/{st['pagejump']}pj · {st['detector']}"
                  if status != "DROP" else st["reason"])
        rep.append(f"| {subj} | {year} | {level} | {pfile} | {status} | {detail} |")
    with open(ANSWERS_REPORT, "w", encoding="utf-8") as f:
        f.write("\n".join(rep) + "\n")

    log(f"  {fully} full + {degraded} partial sidecars ({dropped} dropped)")
    log(f"  → {os.path.relpath(ANSWERS_REPORT, REPO)}")
    log("DONE")
    return 0


if __name__ == "__main__":
    sys.exit(main())
