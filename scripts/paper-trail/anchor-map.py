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
HEADER_X_TOL = 22        # header x-jitter within one sequence (SEC indents Q1 under a page title)
MIN_SPREAD_FRAC = 0.5    # paper chips AND scheme regions must each span ≥ this·N distinct pages

# fileid grammar (mirrors build-index.py): {LC|JC|LB}{SSS}{LVL}L?P{CCC}{LANG}.pdf
FILEID_RE = re.compile(r"^(LC|JC|LB)(\d{3})([A-Z])L?P([A-Z0-9]{3})(EV|IV|BV)\.pdf$", re.I)

# Scope. SCOPE_CODES None = all subjects; a set = only those SEC codes (used to
# extend already-verified subjects to more years without re-mapping the rest).
SCOPE_EXAM = "LC"
SCOPE_LEVELS = {"A", "G", "C"}      # higher, ordinary, common
SCOPE_LANGS = {"EV"}
SCOPE_YEARS = set(range(2010, 2026))
SCOPE_CODES = None  # which codes to ATTEMPT this run; None = all not in DONE_CODES
# Short-answer crop tier. When a paper reconciles fully + monotonically but its
# scheme answers cluster (≈3 per page → fails the scheme-spread crop guard), allow
# the crop loop to emit a TIGHT per-question Y-band crop within the shared page
# (Q5 = [y5, y6]) instead of dropping — "click to see what the scheme says" for
# short-answer subjects (Technology, Ag Economics, Swedish reading…). The monotonic
# gate already rejects 2-column interleaved keys. Gated by adversarial verification
# + QA_PASSED before anything ships.
SHORT_ANSWER_TIER = True
# Universal navigation fallback. Goal: EVERY paper that has detectable questions
# AND a marking scheme gets a per-question chip — even when precise crop/page-jump
# mapping fails (essays with mixed scheme grammar, languages with aural sections…).
# It never claims an exact answer (that would be confidently wrong); each chip is a
# conf=0.3 page-jump to the scheme region PROPORTIONALLY near that question, and the
# viewer frames it "opens the scheme near Q N — scroll to find it". Precise maps
# always win; this only fires where the precise path would otherwise drop, and is
# written to a SEPARATE manifest so build-index flags it distinctly.
UNIVERSAL_FALLBACK = False
# Subjects already verified + lit in earlier waves. The engine never re-maps or
# clears these (their committed sidecars are final), so each new wave is additive.
DONE_CODES = {
    # wave 1-2
    "LC003", "LC022", "LC023", "LC024", "LC225", "LC029", "LC014", "LC007",
    "LC559", "LC038", "LC017", "LC049", "LC557", "LC019", "LC553", "LC558",
    # wave 3
    "LC004", "LC006", "LC018", "LC021", "LC025", "LC034", "LC223",
    "LC547", "LC549", "LC550", "LC551", "LC554", "LC567",
    # wave 4 (Junior Cycle)
    "JC003", "JC002", "JC057", "JC042", "JC052", "JC223", "JC046", "JC126", "JC565",
    # wave 6 (Computer Science, JC Geography, LCA)
    "LC219", "JC005",
    "LB832", "LB846", "LB810", "LB833", "LB013", "LB847", "LB849", "LB816", "LB835", "LB010", "LB011", "LB850",
    # wave 7 (Geography Part Two + Engineering, HL+OL — ligature-norm + spread guards)
    "LC005", "LC027",
    # wave 8 (Applied Maths, Home Ec, English P2, Accounting, Business Section 1 —
    # colon/centered-header detection; per-paper agent-verified subsets only)
    "LC020", "LC098", "LC002", "LC032", "LC033",
    # wave 9 (short-answer crop tier — Technology, Swedish, Agri Economics)
    "LC065", "LC039", "LC026",
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


# SEC PDFs frequently extract typographic ligatures as stray glyphs, so the word
# 'Question' comes out as 'QuesƟon' (ti-ligature) and 'Certificate' as 'Certiϐicate'.
# Normalise the common ones before matching question-header words — clean PDFs
# contain none of these so this is a no-op for them.
_LIGATURES = {
    "Ɵ": "ti", "Ʃ": "tt", "ϐ": "fi",
    "ﬀ": "ff", "ﬁ": "fi", "ﬂ": "fl",
    "ﬃ": "ffi", "ﬄ": "ffl", "ﬅ": "ft", "ﬆ": "st",
}


def _deligature(s):
    if s.isascii():
        return s
    for k, v in _LIGATURES.items():
        if k in s:
            s = s.replace(k, v)
    return s


# ─── question-number detectors (return raw [(n, page0, x0, yFrac)]) ──────────

def _det_question_word(doc):
    hits = []
    for pi, page in enumerate(doc):
        if page.rotation:
            continue
        H = page.rect.height
        for lw in line_groups(page):
            for i, w in enumerate(lw):
                word = _deligature(w[4])
                # 'Ceist'/'CEIST' = Irish for 'Question' (Irish-medium IV papers).
                if word not in ("Question", "QUESTION", "Ceist", "CEIST") or i + 1 >= len(lw):
                    continue
                m = re.fullmatch(r"(\d+)[.:]?", lw[i + 1][4])  # 'Question 1' / '1.' / '1:'
                if not m:
                    continue
                # Left-margin header (the common case) OR a CENTERED standalone
                # 'QUESTION N' header line — some schemes (Business 'Possible
                # Responses') centre the real solution headers while a left-margin
                # numbered SUMMARY table sits earlier; spread-max then prefers the
                # real, page-spread solutions over the clustered summary.
                standalone = len(lw) <= 3
                if w[0] < LEFT_MARGIN_X or (word in ("QUESTION", "CEIST") and standalone):
                    hits.append((int(m.group(1)), pi, w[0], w[1] / H))
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
        f = [h for h in hits if abs(h[2] - xb) <= HEADER_X_TOL]
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
    """In-band scheme markers at the modal left-margin x → {n: (page0, yFrac)}.

    Many schemes carry a numbered SUMMARY / marks-allocation table (all of 1..N
    clustered on 1-3 pages) IN ADDITION to the real per-question solutions
    (1..N spread across many pages). First-occurrence-per-number grabs the
    summary. Instead, for each candidate '1' start we build the monotonic
    increasing-number/increasing-position run and keep the one that SPREADS
    across the most scheme pages — the real solutions, not the summary. With a
    single occurrence per number (the common case) this is just first-occurrence."""
    inb = [h for h in hits if band_start <= h[1] < band_end]
    if not inb:
        return {}
    xs = Counter(round(h[2] / 5) * 5 for h in inb)
    best, best_key = {}, (-1, -1)
    for xb, _ in xs.most_common(5):
        f = [h for h in inb if abs(h[2] - xb) <= HEADER_X_TOL]
        f.sort(key=lambda h: (h[1], h[3]))
        starts = [i for i, h in enumerate(f) if h[0] == 1] or [0]
        for si in starts:
            m, prev, last_n = {}, (-1, -1.0), 0
            for n, pi, x, y in f[si:]:
                if n > last_n and (pi, y) > prev and n not in m:
                    m[n] = (pi, y)
                    prev, last_n = (pi, y), n
            # prefer the most page-spread run (real solutions), then the longest
            key = (len({p for p, _ in m.values()}), len(m))
            if key > best_key:
                best, best_key = m, key
    return best


def detect_scheme_markers(doc, band_start, band_end, want_ns, paper_det=None):
    """The detector whose in-band number-set best covers the paper's questions.

    Grammar guard: a 'Question N' scheme marker always heads a major structured
    answer. A short-answer paper (numbered with a bare 'N.' or 'Q.N') must NOT
    reconcile against those — its answers live in a compact short-answer key, not
    the essay solutions. So when the paper is not 'question'-headed we exclude the
    'question' scheme detector (else e.g. a Geography Part One short-answer book
    would map onto the Part Two essay scheme and ship a confidently-wrong chip)."""
    best, best_score = {}, -1
    for name, fn in DETECTORS:
        if paper_det is not None and paper_det != "question" and name == "question":
            continue
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


# SEC marking-scheme front-matter boilerplate. Schemes that prefix a numbered
# general-instructions / outline / summary / contents block reuse 1., 2., 3.…
# before the real per-question solutions restart — so we skip past it before
# detecting scheme markers. Clean schemes contain none of these → no change.
FRONT_MATTER_PHRASES = (
    "in considering this marking scheme",
    "only key words are given",
    "only key phrases are given",
    "the following points should be noted",
    "summary of marking scheme",
    "summary of marks",
    "outline marking scheme",
    "general guidelines",
    "table of contents",
    # LCA / answer-book instruction pages
    "candidates must attempt",
    "candidates should answer",
    "write your examination number",
    "write all answers",
    "general directions",
)


def front_matter_end(scheme, band_start, band_end):
    """First 0-based page of real solutions: skip past any numbered front-matter
    block (instructions/outline/summary/contents) in the band's first pages.
    Returns band_start when there is no front matter — unchanged for clean schemes."""
    last_fm = -1
    for pi in range(band_start, min(band_start + 8, band_end)):
        t = scheme[pi].get_text("text").lower()
        if any(p in t for p in FRONT_MATTER_PHRASES):
            last_fm = pi
    return last_fm + 1 if last_fm >= band_start else band_start


# Tail appendix that follows the WRITTEN questions in subjects with a coursework /
# practical component (Engineering, DCG…). These pages are non-blank and portrait,
# so the last question's continuation must stop before them rather than swallow a
# practical-marking grid as if it were the written answer.
# Phrases are matched against punctuation-normalised text, so "Practical, Marking
# Scheme" / "Practical - Marking Scheme" / "Engineering Practical" all reduce to a
# clean space-separated form before the substring test.
TAIL_BOUNDARY_PHRASES = (
    "practical marking scheme",
    "coursework marking scheme",
    "practical coursework",
    "project marking scheme",
    "subjective marking",
)
# A "Blank Page" filler carries the literal words rather than empty text, so the
# empty-text blank test misses it — match the normalised page text exactly.
BLANK_PAGE_TEXTS = {
    "", "blank page", "this page is intentionally blank",
    "this page has been left blank intentionally",
    "this page has been intentionally left blank",
    "there is no examination material on this page",
}


def _norm_match(s):
    """Lowercase + collapse every non-alphanumeric run to a single space."""
    return re.sub(r"[^a-z0-9]+", " ", _deligature(s).lower()).strip()


def is_tail_boundary(page):
    t = _norm_match(page.get_text("text"))
    return any(p in t for p in TAIL_BOUNDARY_PHRASES)


def is_blank(page):
    """A scheme page carrying no answer content (trailing filler/blank)."""
    # 'Blank Page' / 'no examination material' notices read as text but are filler.
    if re.sub(r"\d+", "", _norm_match(page.get_text("text"))).strip() in BLANK_PAGE_TEXTS:
        return True
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


def fallback_chips(headers, yband, scheme, band_start, band_end,
                   paper_path, scheme_path, band_strategy, stats):
    """Universal navigation fallback: a per-question chip for every detected paper
    question, page-jumping PROPORTIONALLY into the scheme's answer region. Never a
    crop and never an exact-answer claim (conf 0.3) — the viewer frames it as "opens
    the scheme near Q N". Used only where the precise path drops but the paper has
    real per-question headers + a scheme."""
    if not UNIVERSAL_FALLBACK:
        return None
    # SEC schemes always open with a cover + a "Note to teachers" page before any
    # answers, so never let the proportional region start before page 3 (index 2).
    lo = max(front_matter_end(scheme, band_start, band_end), min(band_start + 2, band_end - 1))
    hi = last_nonblank_page(scheme, lo, band_end)
    apages = max(1, hi - lo + 1)
    hs = sorted(headers, key=lambda h: h[0])
    N = len(hs)
    qout = []
    for idx, (n, p_pi, p_x0, p_y) in enumerate(hs):
        sp = lo + min(apages - 1, idx * apages // N)
        if scheme[sp].rotation:
            sp = next((p for p in range(sp, hi + 1) if not scheme[p].rotation), sp)
        qout.append({"n": str(n), "pP": p_pi + 1, "pY": yband(p_pi, p_y),
                     "region": [{"p": sp + 1}], "mode": "pagejump", "conf": 0.3})
    if not qout:
        return None
    stats["pagejump"] = len(qout)
    stats["fallback"] = True
    return {"v": SIDECAR_V, "paperFileid": os.path.basename(paper_path),
            "schemeFileid": os.path.basename(scheme_path),
            "component": band_strategy[2] if len(band_strategy) > 2 else "",
            "band": [band_start + 1, band_end + 1], "copyright": COPYRIGHT,
            "fallback": 1, "q": qout}


# ─── per-paper mapping ───────────────────────────────────────────────────────

def map_paper(paper_path, scheme_path, band_strategy, fallback_only=False):
    """Returns (sidecar_or_None, stats). fallback_only skips the precise attempt and
    emits navigation chips straight away (used to cover already-shipped subjects'
    dropped years + any paper with no committed map)."""
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

    # Guard 1 — paper-side spread. If most chips collapse onto one/two pages the
    # paper has no real per-question headers (the detector matched a contents/
    # instructions list on the cover). Dropping avoids stacking every chip on the
    # cover page (old single-booklet Geography, instruction-page papers). Short-
    # answer papers legitimately pack many questions per page, so there we only
    # reject a true single-page collapse (a cover contents list).
    paper_pages = len({h[1] for h in headers})
    paper_floor = 2 if SHORT_ANSWER_TIER else max(2, MIN_SPREAD_FRAC * N)
    if paper_pages < paper_floor:
        stats["reason"] = f"paper headers collapse onto {paper_pages} pages (chip-on-cover)"
        return None, stats

    # paper question y-band end (next header on same page, else page bottom)
    by_page = defaultdict(list)
    for n, pi, x0, y in headers:
        by_page[pi].append((y, n))
    for pi in by_page:
        by_page[pi].sort()

    def paper_yband(p_pi, p_y):
        nxt = next((yf for yf, nn in by_page[p_pi] if yf > p_y + 1e-6), 1.0)
        return [round(p_y, 4), round(nxt, 4)]

    def drop(reason):
        """Drop to the universal navigation fallback (or None if disabled)."""
        stats["reason"] = reason
        fb = fallback_chips(headers, paper_yband, scheme, 0, len(scheme),
                            paper_path, scheme_path, band_strategy, stats)
        return (fb, stats)

    if fallback_only:
        return drop("fallback-only pass")

    # Band for this paper within (possibly shared) scheme.
    if band_strategy[0] == "divider":
        k = band_strategy[1]
        band_start = find_band(scheme, f"Paper {k}")
        if band_start is None:
            return drop(f"band 'Paper {k}' not found")
        nxt = find_band(scheme, f"Paper {k + 1}")
        band_end = nxt if (nxt is not None and nxt > band_start) else len(scheme)
    else:
        band_start, band_end = 0, len(scheme)

    fm_start = front_matter_end(scheme, band_start, band_end)
    markers = detect_scheme_markers(scheme, fm_start, band_end, want_ns, detector)
    matched = sum(1 for n in want_ns if n in markers)
    stats["conf"] = round(matched / N, 3)
    # Strict gate: every paper question must have a scheme marker.
    if matched < N:
        return drop(f"count reconcile {matched}/{N} (detector {detector})")
    seq_pts = [markers[n] for n in sorted(markers) if n in want_ns]
    mono = all(seq_pts[i] < seq_pts[i + 1] for i in range(len(seq_pts) - 1))
    if not mono:
        return drop("scheme markers not monotonic")

    # Guard 2 — scheme-side spread. If many questions resolve to the same scheme
    # page the markers collapsed onto a compact short-answer key / summary table.
    # The monotonic gate above already rejects 2-column interleaved keys, so a
    # collapse here with monotonic markers is a single-column SHORT-ANSWER key
    # whose per-question Y positions are distinct — the crop loop below yields a
    # tight Y-band crop per question (Q5 = [y5, y6] on the shared page). By default
    # we still drop (conservative); SHORT_ANSWER_TIER lets it crop, gated by
    # adversarial verification.
    scheme_spread = len({markers[n][0] for n in want_ns})
    short_answer = scheme_spread < max(2, MIN_SPREAD_FRAC * N)
    if short_answer and not SHORT_ANSWER_TIER:
        stats["reason"] = f"scheme markers collapse onto {scheme_spread} pages (short-answer key)"
        return None, stats

    qout = []
    maxn = max(want_ns)  # the PAPER's last question (scheme may carry stray markers beyond it)
    # The last question has no following marker to bound it. Using the scheme's
    # last non-blank page over-reaches across appendix/filler pages → the span
    # blows past MAX_REGION_PAGES and the question degrades to a whole-page jump
    # that opens at the page TOP (i.e. on the PREVIOUS question's answer when this
    # question's header sits mid-page). Bound it to the typical per-question span
    # (median gap between consecutive markers) so it stays a header-anchored crop.
    sm = sorted(markers)
    gaps = [markers[sm[i + 1]][0] - markers[sm[i]][0] for i in range(len(sm) - 1)]
    gaps = [g for g in gaps if g >= 0]
    typ_span = max(1, min(sorted(gaps)[len(gaps) // 2] if gaps else 1, MAX_REGION_PAGES))
    for n, p_pi, p_x0, p_y in headers:
        same = by_page[p_pi]
        nxt_same = next((yf for yf, nn in same if yf > p_y + 1e-6), 1.0)
        p_yband = [round(p_y, 4), round(nxt_same, 4)]

        s_pi, s_yfrac = markers[n]
        end = markers.get(n + 1) if n + 1 <= maxn else None  # ignore stray > last-paper-Q markers
        degrade = False
        if end is not None and end > (s_pi, s_yfrac):
            e_pi, e_yfrac = end
        elif n == maxn and short_answer:
            # A short answer never spans pages — crop to the bottom of its own page
            # (extending into the next Section would over-run → needless pagejump).
            e_pi, e_yfrac = s_pi, 1.0
        elif n == maxn:
            # Extend only across clean consecutive continuation pages, stopping at
            # the first blank or rotated page (schemes append landscape marks-total
            # / filler pages after the last answer — including them forces pagejump).
            e_pi = s_pi
            while (e_pi + 1 < band_end and e_pi - s_pi < typ_span
                   and not is_blank(scheme[e_pi + 1]) and not scheme[e_pi + 1].rotation
                   and not is_tail_boundary(scheme[e_pi + 1])):
                e_pi += 1
            e_yfrac = 1.0
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

def build_pairs(rows, include_done=False, langs=None, levels=None):
    """[(paperRow, schemeRow, band_strategy, levelCode)] for in-scope papers.
    band_strategy = ('whole', component) or ('divider', k, component).
    include_done=True keeps frozen codes too (the navigation-fallback pass covers
    their unmapped dropped years). langs/levels override SCOPE_LANGS/SCOPE_LEVELS
    (the fallback pass adds IV/BV + Foundation papers for navigation chips)."""
    langs = langs or SCOPE_LANGS
    levels = levels or SCOPE_LEVELS
    papers = defaultdict(list)   # (code, year, level, lang) -> [(row, decoded)]
    schemes = defaultdict(list)
    for r in rows:
        d = decode_fileid(r["fileid"])
        if not d or d["exam"] != SCOPE_EXAM:
            continue
        if d["code"] in DONE_CODES and not include_done:
            continue  # frozen — lit in an earlier wave, never re-mapped
        if SCOPE_CODES is not None and not include_done and d["code"] not in SCOPE_CODES:
            continue
        if d["levelCode"] not in SCOPE_LEVELS or d["lang"] not in langs:
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
            # Only split into Paper 1 / Paper 2 bands when the shared components are
            # actually Paper-N components (1xx / 2xx, like Maths 100/200). Other
            # subjects share one scheme across unrelated components (e.g. Computer
            # Science 038/040, Technology 014/039) with NO 'Paper N' dividers — they
            # use the whole scheme. Without this, those papers wrongly drop.
            paper_like = len(comps) > 1 and all(c[:1] in ("1", "2") for c in comps)
            if paper_like:
                k = 1 if pd["component"][:1] == "1" else 2  # Paper-1 vs Paper-2 family
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

    # ── Pass 2: universal navigation fallback for EVERY remaining paper that has a
    # scheme but no committed map — including already-shipped subjects' dropped
    # years (frozen codes). Never overwrites an existing sidecar (precise stays
    # frozen); only fills the gaps so the Answers feature reaches every paper.
    if UNIVERSAL_FALLBACK:
        have = set()
        for yd in (os.listdir(ANSWERS_DIR) if os.path.isdir(ANSWERS_DIR) else []):
            ydp = os.path.join(ANSWERS_DIR, yd)
            if yd.isdigit() and os.path.isdir(ydp):
                for fn in os.listdir(ydp):
                    if fn.endswith(".json"):
                        have.add((int(yd), fn[:-5]))
        fb_added = 0
        fb_langs = set(SCOPE_LANGS) | {"IV", "BV"}  # + Irish-medium + bilingual papers
        for prow, srow, strat, level in sorted(build_pairs(rows, include_done=True, langs=fb_langs),
                                               key=lambda p: (int(p[0]["year"]), p[0]["fileid"])):
            year, pfile, sfile = int(prow["year"]), prow["fileid"], srow["fileid"]
            if (year, pfile) in have:
                continue  # already has a precise or fallback map — leave it
            ppath = corpus_path("exampapers", year, pfile)
            spath = corpus_path("markingschemes", year, sfile)
            if not (os.path.exists(ppath) and os.path.exists(spath)):
                continue
            sidecar, st = map_paper(ppath, spath, strat, fallback_only=True)
            if sidecar is None:
                continue
            bs, be = sidecar["band"]
            for q in sidecar["q"]:
                for seg in q["region"]:
                    assert bs <= seg["p"] < be, f"{pfile} Q{q['n']} page {seg['p']} escapes band"
            ydir = os.path.join(ANSWERS_DIR, str(year))
            os.makedirs(ydir, exist_ok=True)
            with open(os.path.join(ydir, f"{pfile}.json"), "w", encoding="utf-8") as fh:
                json.dump(sidecar, fh, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
            have.add((year, pfile))
            fb_added += 1
        log(f"  navigation fallback added for {fb_added} dropped-year/unmapped papers")

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
