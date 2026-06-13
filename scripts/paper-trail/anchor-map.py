#!/usr/bin/env python3
"""
Paper Trail — Stage 2.5: build per-paper question→answer ANCHOR MAPS.

Runs AFTER download.py, BEFORE build-index.py. For each in-scope exam paper that
has a marking scheme, it precomputes — by reading the REAL corpus PDFs with
pymupdf (fitz), deterministically — a coordinates-only sidecar that lets the
viewer drop a CROP of the scheme's own pixels beside each question. It ships NO
answer text and NO image bytes: only page numbers + fractional rectangles.

Why the engine is shaped the way it is (every choice verified against the real
Maths Higher Level corpus; see scripts/paper-trail/ANSWERS_PLAN.md):

  • WORD-BOUNDARY token location, never page.search_for(). Verified:
    search_for("Question 1") on the real Maths HL P1 returns BOTH page 3 and
    page 27 (page 27 is "Question 10" — a substring hit), which would silently
    mis-map the founder's flagship Q1. We instead scan get_text("words") for a
    'Question' token at the left margin immediately followed by an EXACT-match
    integer token.

  • COMPONENT-BAND SPLIT. Paper 1 (LC003ALP100EV) and Paper 2 (LC003ALP200EV)
    SHARE ONE scheme file (LC003ALP000EV), in which "Q1" legitimately appears in
    BOTH the Paper-1 band (pages ~6-8) and the Paper-2 band (pages ~34-36). The
    scheme carries hard 'Paper 1' / 'Paper 2' dividers (whose pages MOVE year to
    year: 30/35/28/37) so we detect them dynamically and scope every marker
    search to the paper's own band. A region that escapes the band fails the gate.

  • OMIT-ON-DOUBT. Any paper whose headers aren't a clean monotonic 1..N, any
    question whose scheme marker is missing/non-monotonic, any rotated page, any
    fraction outside [0,1], or any region longer than MAX_REGION_PAGES degrades
    to a reliable page-jump (mode='pagejump') or is dropped entirely. Better a
    missing chip than a wrong crop — the product's whole trust model.

Output (deterministic, sorted, idempotent — safe to re-run):
  scripts/paper-trail/out/answers/<year>/<paperFileid>.json   (one sidecar/paper)
  scripts/paper-trail/out/answers-manifest.jsonl              (build-index input)
  scripts/paper-trail/out/answers-report.md                  (coverage report)

All emitted page numbers are 1-BASED (matching pdf.js getPage + the viewer's
data-page attribute). All rects are fractions of the (unrotated) page box.

Scope is the per-subject GRAMMAR table below — a new subject is one table row
plus a contact-sheet review, never a code change.
"""

import json
import os
import re
import sys
from collections import defaultdict

import fitz  # pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
OUT_DIR = os.path.join(HERE, "out")
CORPUS = os.path.join(REPO, "paper-trail-corpus")
MANIFEST = os.path.join(OUT_DIR, "manifest.jsonl")
# Sidecars are COMMITTED generated artifacts (like paperTrailData.ts) — CI and
# deploy need them without the gitignored 10GB corpus — so they live OUTSIDE
# out/. The manifest + report stay in the ephemeral out/.
ANSWERS_DIR = os.path.join(HERE, "answers")
ANSWERS_MANIFEST = os.path.join(OUT_DIR, "answers-manifest.jsonl")
ANSWERS_REPORT = os.path.join(OUT_DIR, "answers-report.md")

SIDECAR_V = 1
COPYRIGHT = "© State Examinations Commission"
LEFT_MARGIN_X = 140      # a header/marker token must start left of this (points)
MAX_REGION_PAGES = 6     # a single question's scheme region longer than this → pagejump
DIVIDER_TOP_FRAC = 0.5   # a band divider title sits in the top half of its page

# fileid grammar (mirrors build-index.py): {LC|JC|LB}{SSS}{LVL}L?P{CCC}{LANG}.pdf
FILEID_RE = re.compile(r"^(LC|JC|LB)(\d{3})([A-Z])L?P([A-Z0-9]{3})(EV|IV|BV)\.pdf$", re.I)


# ─── per-subject MARKER GRAMMAR (one row per (subjectCode, language) profile) ──
# A grammar row is verified on a contact sheet before its `answers` flag ships
# (Phase 5). Adding a subject = adding a row + a review pass, never code.
GRAMMAR = {
    # Leaving Cert Mathematics (English version). Pilot.
    ("LC003", "EV"): {
        "name": "Mathematics",
        # paper question header: the word 'Question' + an integer, left margin
        "paper_header": "question_int",
        # scheme per-question body marker: a standalone 'Q1'/'Q.1' token, left margin
        "scheme_marker": re.compile(r"^Q\.?(\d{1,2})$"),
        # component code → band divider title within the shared scheme
        "bands": {"100": "Paper 1", "200": "Paper 2"},
        # only these components are mapped for this subject
        "components": {"100", "200"},
        # only these level codes (A=higher) are in pilot scope
        "levels": {"A"},
    },
}

# Pilot scope filter: (subjectCode, years). Everything else is skipped cleanly.
SCOPE_YEARS = set(range(2022, 2026))


def log(msg):
    print(msg, flush=True)


def decode_fileid(fileid):
    m = FILEID_RE.match(fileid)
    if not m:
        return None
    return {
        "exam": m.group(1).upper(),
        "code": (m.group(1) + m.group(2)).upper(),   # e.g. LC003
        "levelCode": m.group(3).upper(),
        "component": m.group(4).upper(),
        "lang": m.group(5).upper(),
    }


def corpus_path(view, year, fileid):
    return os.path.join(CORPUS, view, str(year), fileid)


# ─── PDF reading primitives ──────────────────────────────────────────────────

def line_groups(page):
    """get_text('words') grouped into lines, each sorted left→right.
    word tuple = (x0, y0, x1, y1, text, block_no, line_no, word_no)."""
    lines = defaultdict(list)
    for w in page.get_text("words"):
        lines[(w[5], w[6])].append(w)
    for lw in lines.values():
        lw.sort(key=lambda w: w[0])
    return list(lines.values())


def find_paper_headers(doc):
    """Locate 'Question N' headers by word-boundary tokens (NOT search_for).
    Returns [(n, page0, x0, y0, page_h)] in document order, or None on rotation."""
    hits = []
    for pi, page in enumerate(doc):
        if page.rotation:
            return None  # rotated paper page → omit whole paper (degrade)
        H = page.rect.height
        for lw in line_groups(page):
            for i, w in enumerate(lw):
                if (
                    w[4] == "Question"
                    and w[0] < LEFT_MARGIN_X
                    and i + 1 < len(lw)
                    and re.fullmatch(r"\d+", lw[i + 1][4])
                ):
                    hits.append((int(lw[i + 1][4]), pi, w[0], w[1], H))
    return hits


def find_band(scheme, divider_title):
    """0-based page index of the FIRST top-of-page occurrence of the band divider
    title (e.g. 'Paper 1'). The SEC prints this either as a standalone title
    (2022/24/25, page 2) or only inside 'Marking Scheme – Paper 1, Section A…'
    (2023, no standalone line) — so we take the first top-half hit, which is the
    true band start in every observed year. The band ORDER (Paper 1 band precedes
    Paper 2 band) plus the in-band assert in main() are the real safety net; a
    later running-header copy of the title can't move the start earlier.
    Returns None if not found."""
    for pi, page in enumerate(scheme):
        if page.rotation:
            continue
        H = page.rect.height
        for r in page.search_for(divider_title):
            if r.y0 < H * DIVIDER_TOP_FRAC:
                return pi
    return None


# A filler page may still carry a footer rule / margin border (1-3 vector ops);
# a real vector-drawn answer page has dozens. This threshold separates them.
BLANK_MAX_DRAWINGS = 3


def is_blank(page):
    """A scheme page carrying no answer content (trailing filler/blank) — no
    text, no images, and at most a footer-rule's worth of vector drawings."""
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
    """Last non-blank 0-based page in [start, band_end) — trims trailing blanks
    so the last question's region doesn't run into filler (which would inflate
    its span into a needless page-jump, or pad a crop with an empty page)."""
    e = band_end - 1
    while e > start and is_blank(doc[e]):
        e -= 1
    return e


def find_scheme_markers(scheme, marker_re, band_start, band_end):
    """First occurrence of each 'QN' marker within [band_start, band_end).
    Returns {n: (page0, yFrac)} using the FIRST page each marker appears on."""
    first = {}
    for pi in range(band_start, band_end):
        page = scheme[pi]
        if page.rotation:
            continue  # skip rotated scheme pages; bounding logic will degrade
        H = page.rect.height
        for lw in line_groups(page):
            for w in lw:
                if w[0] >= LEFT_MARGIN_X:
                    continue
                m = marker_re.match(w[4])
                if m:
                    n = int(m.group(1))
                    if n not in first:
                        first[n] = (pi, w[1] / H)
    return first


# ─── per-paper mapping ───────────────────────────────────────────────────────

def map_paper(paper_path, scheme_path, profile, component):
    """Returns (sidecar_dict_or_None, stats_dict)."""
    stats = {"crop": 0, "pagejump": 0, "omit": 0, "reason": None}

    paper = fitz.open(paper_path)
    scheme = fitz.open(scheme_path)

    headers = find_paper_headers(paper)
    if headers is None:
        stats["reason"] = "rotated paper page"
        return None, stats
    headers.sort(key=lambda h: (h[1], h[3]))  # by (page, y)
    ns = [h[0] for h in headers]
    if ns != list(range(1, len(ns) + 1)) or len(ns) == 0:
        stats["reason"] = f"paper headers not clean 1..N (got {ns})"
        return None, stats

    # Band for this paper's component.
    divider_title = profile["bands"][component]
    band_start = find_band(scheme, divider_title)
    if band_start is None:
        stats["reason"] = f"band divider {divider_title!r} not found"
        return None, stats
    # Band end = the next divider after band_start, else end of scheme.
    other_starts = [
        find_band(scheme, t)
        for c, t in profile["bands"].items()
        if t != divider_title
    ]
    later = [p for p in other_starts if p is not None and p > band_start]
    band_end = min(later) if later else len(scheme)

    markers = find_scheme_markers(scheme, profile["scheme_marker"], band_start, band_end)
    # Marker monotonicity within band (page,y strictly increasing by n).
    seq = [markers[n] for n in sorted(markers) if n in markers]
    mono = all(seq[i] < seq[i + 1] for i in range(len(seq) - 1))

    qout = []
    # paper header y-end per page: next header on same page, else page bottom.
    by_page = defaultdict(list)
    for n, pi, x0, y0, H in headers:
        by_page[pi].append((y0 / H, n))
    for pi in by_page:
        by_page[pi].sort()

    for idx, (n, p_pi, p_x0, p_y0, p_H) in enumerate(headers):
        p_yfrac = p_y0 / p_H
        # paper question y-band end
        same = by_page[p_pi]
        nxt_same = next((yf for yf, nn in same if yf > p_yfrac + 1e-6), 1.0)
        p_yband = [round(p_yfrac, 4), round(nxt_same, 4)]

        if n not in markers or not mono:
            stats["omit"] += 1
            continue
        s_pi, s_yfrac = markers[n]
        maxn = max(markers)
        # region end = start of the NEXT question's marker (n+1) within band.
        end = markers.get(n + 1)
        degrade = False
        if end is not None and end > (s_pi, s_yfrac):
            e_pi, e_yfrac = end
        elif n == maxn:
            # genuinely the last mapped question: run to the last NON-BLANK page
            # in the band (trailing blanks excluded so the span stays honest).
            e_pi, e_yfrac = last_nonblank_page(scheme, s_pi, band_end), 1.0
        else:
            # an intermediate marker (n+1) is missing/out of order — do NOT
            # swallow the following question(s); degrade this one to a page-jump.
            degrade = True
            e_pi, e_yfrac = s_pi, 1.0

        span = e_pi - s_pi
        # region rects (fractions of each page; full width)
        region = []
        ok = not degrade
        if not ok:
            pass  # forced page-jump below
        elif span == 0:
            region.append({"p": s_pi + 1, "r": [0.0, round(s_yfrac, 4), 1.0, round(e_yfrac, 4)]})
        elif 0 < span <= MAX_REGION_PAGES:
            region.append({"p": s_pi + 1, "r": [0.0, round(s_yfrac, 4), 1.0, 1.0]})
            for mid in range(s_pi + 1, e_pi):
                region.append({"p": mid + 1, "r": [0.0, 0.0, 1.0, 1.0]})
            region.append({"p": e_pi + 1, "r": [0.0, 0.0, 1.0, round(e_yfrac, 4)]})
        else:
            ok = False  # region too long → degrade to page-jump

        # validate all fractions ∈ [0,1] and rotation-free region pages
        if ok:
            for seg in region:
                if any(not (0.0 <= v <= 1.0) for v in seg["r"]):
                    ok = False
                    break
                if scheme[seg["p"] - 1].rotation:
                    ok = False
                    break

        if ok:
            qout.append({
                "n": str(n), "pP": p_pi + 1, "pY": p_yband,
                "region": region, "mode": "crop", "conf": 1.0,
            })
            stats["crop"] += 1
        else:
            qout.append({
                "n": str(n), "pP": p_pi + 1, "pY": p_yband,
                "region": [{"p": s_pi + 1}], "mode": "pagejump", "conf": 0.6,
            })
            stats["pagejump"] += 1

    if not qout:
        stats["reason"] = "no questions mapped"
        return None, stats

    sidecar = {
        "v": SIDECAR_V,
        "paperFileid": os.path.basename(paper_path),
        "schemeFileid": os.path.basename(scheme_path),
        "component": component,
        # 1-based half-open [lo, hi): band_start..band_end-1 (0-based) → +1 each.
        "band": [band_start + 1, band_end + 1],
        "copyright": COPYRIGHT,
        "q": qout,
    }
    return sidecar, stats


# ─── pairing (mirror build-index: same component, then 000 fallback) ──────────

def build_pairs(rows):
    """Return [(paperRow, schemeRow, profile, component)] for in-scope papers."""
    papers = defaultdict(list)   # (code, year, levelCode, lang) -> [rows]
    schemes = defaultdict(list)
    for r in rows:
        d = decode_fileid(r["fileid"])
        if not d:
            continue
        key = (d["code"], int(r["year"]), d["levelCode"], d["lang"])
        (papers if r["view"] == "exampapers" else schemes)[key].append((r, d))

    pairs = []
    for key, plist in sorted(papers.items()):
        code, year, levelCode, lang = key
        profile = GRAMMAR.get((code, lang))
        if not profile:
            continue
        if year not in SCOPE_YEARS or levelCode not in profile["levels"]:
            continue
        cands = schemes.get(key, [])
        for prow, pd in sorted(plist, key=lambda x: x[0]["fileid"]):
            if pd["component"] not in profile["components"]:
                continue
            # scheme: same-component, else the whole-level 000 scheme
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
            if scheme is None:
                continue
            pairs.append((prow, scheme, profile, pd["component"]))
    return pairs


def main():
    log("Paper Trail — Stage 2.5: anchor maps")
    if not os.path.exists(MANIFEST):
        log(f"FATAL: {MANIFEST} missing — run enumerate.py first")
        return 1
    rows = []
    seen = set()
    with open(MANIFEST, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            k = (r["view"], r["year"], r["fileid"])
            if k in seen:
                continue
            seen.add(k)
            if r["fileid"].lower().endswith(".pdf"):
                rows.append(r)

    pairs = build_pairs(rows)
    log(f"  in-scope papers: {len(pairs)}")

    os.makedirs(ANSWERS_DIR, exist_ok=True)
    manifest_lines = []
    report = ["# Paper Trail — Stage 2.5 anchor-map report (answers-report.md)", ""]
    report.append("Deterministic; re-run after download.py. Scope = GRAMMAR table × SCOPE_YEARS.")
    report.append("")
    report.append("| paper | scheme | comp | band | crop | pagejump | omit | status |")
    report.append("|---|---|---|---|---|---|---|---|")

    fully = degraded = failed = 0
    for prow, srow, profile, component in pairs:
        year = int(prow["year"])
        pfile = prow["fileid"]
        sfile = srow["fileid"]
        ppath = corpus_path("exampapers", year, pfile)
        spath = corpus_path("markingschemes", year, sfile)
        if not (os.path.exists(ppath) and os.path.exists(spath)):
            report.append(f"| {pfile} | {sfile} | {component} | — | — | — | — | MISSING file |")
            failed += 1
            continue

        sidecar, st = map_paper(ppath, spath, profile, component)
        if sidecar is None:
            report.append(f"| {pfile} | {sfile} | {component} | — | 0 | 0 | {st['omit']} | DROP: {st['reason']} |")
            failed += 1
            manifest_lines.append({"year": year, "paperFileid": pfile, "schemeFileid": sfile,
                                   "mapped": False, "reason": st["reason"]})
            continue

        # IN-BAND ASSERTION (the P1/P2 fix): every region page inside the band.
        bs, be = sidecar["band"]
        for q in sidecar["q"]:
            for seg in q["region"]:
                assert bs <= seg["p"] < be, (
                    f"{pfile} Q{q['n']} region page {seg['p']} escapes band [{bs},{be})")
        # write sidecar (sorted keys for determinism)
        ydir = os.path.join(ANSWERS_DIR, str(year))
        os.makedirs(ydir, exist_ok=True)
        with open(os.path.join(ydir, f"{pfile}.json"), "w", encoding="utf-8") as fh:
            json.dump(sidecar, fh, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        status = "FULL" if st["pagejump"] == 0 and st["omit"] == 0 else "PARTIAL"
        if status == "FULL":
            fully += 1
        else:
            degraded += 1
        report.append(f"| {pfile} | {sfile} | {component} | {bs}-{be} | "
                      f"{st['crop']} | {st['pagejump']} | {st['omit']} | {status} |")
        manifest_lines.append({"year": year, "paperFileid": pfile, "schemeFileid": sfile,
                               "mapped": True, "nCrop": st["crop"], "nPagejump": st["pagejump"],
                               "nOmit": st["omit"]})

    with open(ANSWERS_MANIFEST, "w", encoding="utf-8") as f:
        for row in sorted(manifest_lines, key=lambda r: (r["year"], r["paperFileid"])):
            f.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
    report += ["", f"**{fully} fully-mapped · {degraded} partial · {failed} dropped/missing**", ""]
    with open(ANSWERS_REPORT, "w", encoding="utf-8") as f:
        f.write("\n".join(report) + "\n")

    log(f"  wrote {fully} full + {degraded} partial sidecars ({failed} dropped)")
    log(f"  → {os.path.relpath(ANSWERS_MANIFEST, REPO)}")
    log(f"  → {os.path.relpath(ANSWERS_REPORT, REPO)}")
    log("DONE")
    return 0


if __name__ == "__main__":
    sys.exit(main())
