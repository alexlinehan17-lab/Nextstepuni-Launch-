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
SCOPE_EXAMS = {"LC"}
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
    # wave 10 (section-anchored essay subjects — bespoke wave10_sections.py, NOT
    # this generic engine; frozen so a re-run never clears their committed maps)
    "LC568", "LC008",
}
# Aural / unprepared-listening / non-level components never carry page questions.
SKIP_COMPONENTS = {"A00", "U00"}

# New-spec multi-booklet subjects (Biology 2026: Sections A&B = Q1-15, Section C
# = Q11-17 continuation) — their booklets may start numbering past 1, and their
# lead-int papers legitimately reconcile against 'Question N' scheme blocks
# (the scheme restates each question; there is no competing short-answer key).
CONTINUATION_CODES = {"LC025", "LC034", "LC022", "LC032", "LC020", "LC029",
                      "LC021", "LC023", "LC225"}


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
        page_words = page.get_text("words")
        for lw in line_groups(page):
            for i, w in enumerate(lw):
                word = _deligature(w[4])
                # 'Ceist'/'CEIST' = Irish for 'Question' (Irish-medium IV papers).
                # "Cesit" = the SEC's own transposition typo (2021 LC034 IV scheme)
                if word not in ("Question", "QUESTION", "Ceist", "CEIST", "Cesit", "CESIT") or i + 1 >= len(lw):
                    continue
                m = re.fullmatch(r"(\d+)[.:]?", lw[i + 1][4])  # 'Question 1' / '1.' / '1:'
                if not m:
                    continue
                # One damaged SEC text layer (2013 Foundation Maths P2 Q10)
                # overlays both ``1`` and ``10`` at exactly the same visual
                # coordinate but assigns them to different text blocks.  Use
                # the longest overlaid digit token so the visible Q10 is not
                # silently reduced to Q1.
                number_word = lw[i + 1]
                overlays = [
                    other[4].rstrip('.:')
                    for other in page_words
                    if re.fullmatch(r"\d+[.:]?", other[4])
                    and abs(other[0] - number_word[0]) < 1
                    and abs(other[1] - number_word[1]) < 1
                ]
                number = max(overlays, key=len) if overlays else m.group(1)
                # Left-margin header (the common case) OR a CENTERED standalone
                # 'QUESTION N' header line — some schemes (Business 'Possible
                # Responses') centre the real solution headers while a left-margin
                # numbered SUMMARY table sits earlier; spread-max then prefers the
                # real, page-spread solutions over the clustered summary.
                standalone = len(lw) <= 3
                # table-scheme variant: "Question N Possible Responses Marks"
                # headers (2026 Economics Section B), any x
                table_hdr = (i + 2 < len(lw)
                             and lw[i + 2][4] in ("Possible", "Freagraí"))
                if w[0] < LEFT_MARGIN_X or table_hdr or (word in ("QUESTION", "CEIST", "Question", "Ceist", "Cesit", "CESIT") and standalone):
                    hits.append((int(number), pi, w[0], w[1] / H))
    return hits


def _det_lead_int(doc):
    hits = []
    for pi, page in enumerate(doc):
        if page.rotation:
            continue
        H = page.rect.height
        groups = line_groups(page)
        blocks_with = Counter(lw[0][5] for lw in groups if lw)
        for lw in groups:
            if not lw:
                continue
            w = lw[0]
            m = re.fullmatch(r"(\d{1,2})\.", w[4])
            # Dotless variant: the SEC sometimes drops the dot on a lone
            # question marker (2022 Physics OL IV prints a bare '4' on its own
            # line beside the text block). Accepted only when the line is a
            # margin-left number whose BLOCK carries more lines (page numbers
            # sit in single-line blocks or outside LEAD_INT_X) and it is not
            # in the footer zone.
            if m is None:
                bare = re.fullmatch(r"(\d{1,2})", w[4])
                if bare and (len(lw) >= 3
                             or (len(lw) == 1 and blocks_with[w[5]] > 1)) \
                        and w[1] / H < 0.9:
                    m = bare
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


def _det_model_solution(doc):
    """Question labels beside a literal ``Model Solutions`` heading.

    Foundation Maths schemes usually print ``Q1 Model Solutions`` but two
    archive PDFs encode the final label as either a bare ``10`` or a stacked
    ``Q`` / ``10``.  Treating the nearby heading as part of the grammar keeps
    this detector specific while recovering the complete 1..10 sequence.
    """
    hits = []
    for pi, page in enumerate(doc):
        if page.rotation:
            continue
        H = page.rect.height
        words = page.get_text("words")
        has_model_heading = any(
            word[4] == "Model" and word[0] < 180 and word[1] < H * 0.2
            for word in words
        ) and any(
            word[4].startswith("Solution") and word[0] < 220 and word[1] < H * 0.2
            for word in words
        )
        if not has_model_heading:
            continue
        candidates = []
        for word in words:
            if word[0] >= LEFT_MARGIN_X or word[1] >= H * 0.2:
                continue
            match = re.fullmatch(r"Q\.?\s*(\d{1,2})", word[4], re.I)
            if match is None:
                match = re.fullmatch(r"(\d{1,2})", word[4])
            if match:
                candidates.append((int(match.group(1)), word))
        if candidates:
            n, word = min(candidates, key=lambda item: item[1][1])
            hits.append((n, pi, word[0], word[1] / H))
    return hits


def _det_c_token(doc):
    """Irish-medium schemes abbreviate 'Ceist N' to a left-margin 'C1'/'C2'
    marker (e.g. Ag Science IV: 'C1 (6 chuid ar bith) 6 × 10 marc'). Same shape
    as the Q-token detector. False C-hits (part labels, chemistry formulae)
    don't form clean monotonic 1..N runs and lose at sequence/count-reconcile."""
    hits = []
    for pi, page in enumerate(doc):
        if page.rotation:
            continue
        H = page.rect.height
        page_hit = False
        for lw in line_groups(page):
            for wi, w in enumerate(lw):
                m = re.fullmatch(r"C\.?(\d{1,2})", w[4])
                # Some translated Maths schemes drop the ``C`` from the final
                # question and print a bare ``10`` immediately beside
                # ``Réiteach Samplach``.  The adjacent solution heading makes
                # this safe and prevents a numbered instruction from matching.
                if (m is None and re.fullmatch(r"\d{1,2}", w[4])
                        and any(v[4].startswith("Réiteach") for v in lw[wi + 1:])):
                    m = re.fullmatch(r"(\d{1,2})", w[4])
                if m and w[0] < LEFT_MARGIN_X:
                    hits.append((int(m.group(1)), pi, w[0], w[1] / H))
                    page_hit = True
                    break
        if not page_hit:
            # Column grouping can separate the left marker from the solution
            # heading even though both sit on the same visual baseline.
            words = page.get_text("words")
            for w in words:
                if not (w[0] < LEFT_MARGIN_X and re.fullmatch(r"\d{1,2}", w[4])):
                    continue
                if any(v[0] > w[2] and abs(v[1] - w[1]) < 3
                       and v[4].startswith("Réiteach") for v in words):
                    hits.append((int(w[4]), pi, w[0], w[1] / H))
                    break
    return hits


def _det_topic_word(doc):
    """'Topic N.' headers (old-spec Classical Studies papers and schemes mirror
    each other topic-for-topic; 'Topaic' on the Irish side)."""
    hits = []
    for pi, page in enumerate(doc):
        if page.rotation:
            continue
        H = page.rect.height
        for lw in line_groups(page):
            for i, w in enumerate(lw):
                if w[4] not in ("Topic", "TOPIC", "Topaic", "TOPAIC") or i + 1 >= len(lw):
                    continue
                m = re.fullmatch(r"(\d{1,2})[.:]?", lw[i + 1][4])
                if m and w[0] < 200:
                    hits.append((int(m.group(1)), pi, w[0], w[1] / H))
    return hits


def _det_q_column(doc):
    """Schemes laid out as a marks TABLE with a 'Q' column: the question number
    is a lone digit in that left column (2026 Economics, the Music listening
    tables). Detected per page: a 'Q' header word left of x=80, then digit
    words in the same column."""
    hits = []
    has_qcol = any(
        any(w[4] == "Q" and w[0] < 80 and w[1] < pg.rect.height * 0.25
            for w in pg.get_text("words")[:40])
        for pg in doc)
    if not has_qcol:
        return hits
    for pi, page in enumerate(doc):
        if page.rotation:
            continue
        H = page.rect.height
        words = sorted(page.get_text("words"), key=lambda w: (w[1], w[0]))
        for i, w in enumerate(words):
            if not (re.fullmatch(r"\d{1,2}", w[4]) and w[0] < 80):
                continue
            n = int(w[4])
            nxt = next((v for v in words[i + 1:] if abs(v[1] - w[1]) < 14), None)
            # exclude "N | Page" page numbers; the run-selection in _marker_map
            # prunes annotation-table clusters (they fail the page-spread
            # preference) and the reconcile gates do the rest
            if n > 20 or (nxt is not None and nxt[4] == "|"):
                continue
            hits.append((n, pi, w[0], w[1] / H))
    return hits


DETECTORS = [("question", _det_question_word), ("lead_int", _det_lead_int), ("qtoken", _det_q_token),
             ("model_solution", _det_model_solution),
             ("ctoken", _det_c_token), ("topic", _det_topic_word), ("qcol", _det_q_column)]


def best_sequence(hits, allow_k_start=False):
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
        ok_run = ns == list(range(1, len(ns) + 1))
        if not ok_run and allow_k_start and ns and len(ns) >= 3:
            # continuation booklets (Biology Section C numbers 11..17): accept a
            # contiguous run starting past 1
            ok_run = ns == list(range(ns[0], ns[0] + len(ns)))
        if ok_run and len(ns) >= MIN_QUESTIONS:
            seq = [first[n] for n in ns]
            if best is None or len(seq) > len(best):
                best = seq
    return best


def detect_paper_headers(doc, allow_k_start=False):
    """Best (detector_name, [(n,page0,x0,yFrac)]) across detectors, or None."""
    best = None
    for name, fn in DETECTORS:
        seq = best_sequence(fn(doc), allow_k_start)
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
    # Neighbour-consistent fill: some schemes indent a lone question's marker
    # off the modal column (2018 Physics IV prints Q5 at x57 amid an x28 run),
    # so the x-cluster filter discards a real marker. Re-admit an off-column
    # hit ONLY where it slots strictly between its numeric neighbours' page/y
    # positions — a front-matter or summary duplicate cannot satisfy that.
    if best:
        for n, pi, x, y in sorted(inb, key=lambda h: (h[1], h[3])):
            if n in best:
                continue
            lower = max((m for m in best if m < n), default=None)
            upper = min((m for m in best if m > n), default=None)
            if lower is None or upper is None:
                # tail/head extension: a run continuing past the modal-column
                # run (Technology IV prints Q12-15 at a second indent) — accept
                # only strictly beyond the run's edge, keeping monotonic order
                if lower is not None and (pi, y) > best[lower]:
                    best[n] = (pi, y)
                elif upper is not None and (pi, y) < best[upper]:
                    best[n] = (pi, y)
                continue
            if best[lower] < (pi, y) < best[upper]:
                best[n] = (pi, y)
    return best


def detect_scheme_markers(doc, band_start, band_end, want_ns, paper_det=None,
                          divider_band=False):
    """The detector whose in-band number-set best covers the paper's questions.

    Grammar guard: a 'Question N' scheme marker always heads a major structured
    answer. A short-answer paper (numbered with a bare 'N.' or 'Q.N') must NOT
    reconcile against those — its answers live in a compact short-answer key, not
    the essay solutions. So when the paper is not 'question'-headed we exclude the
    'question' scheme detector (else e.g. a Geography Part One short-answer book
    would map onto the Part Two essay scheme and ship a confidently-wrong chip).

    Divider-band exception: inside a P1/P2 divider band (shared Maths-style
    scheme) both siblings are full papers with structured per-question solutions
    inside their OWN bands — there is no competing short-answer key for the
    guard to protect. 2012-era Maths numbers the paper '1.' but heads scheme
    solutions 'CEIST 1'; the guard blocked that legitimate pairing."""
    best, best_score = {}, -1
    maps = {}
    for name, fn in DETECTORS:
        if (paper_det is not None and paper_det != "question" and name == "question"
                and not divider_band):
            continue
        m = _marker_map(fn(doc), band_start, band_end)
        maps[name] = m
        score = len(set(m) & want_ns)
        if score > best_score:
            best, best_score = m, score
    if best_score < len(want_ns):
        # hybrid schemes split marker styles by section (2026 Economics:
        # Section A is a Q-column table, Section B uses 'Question N' headers).
        # Union two detectors when the merged positions stay monotonic in n.
        for na, ma in maps.items():
            for nb, mb in maps.items():
                if na == nb:
                    continue
                merged = dict(ma)
                for k, v in mb.items():
                    merged.setdefault(k, v)
                got = sorted(set(merged) & want_ns)
                if len(got) <= best_score:
                    continue
                pts = [merged[n] for n in got]
                if all(b > a for a, b in zip(pts, pts[1:])):
                    best, best_score = merged, len(got)
    return best


def find_band_pages(scheme, divider_title):
    """All 0-based page indices with a top-of-page occurrence of the divider
    title (e.g. 'Paper 1' / 'Páipéar 1'), in order."""
    out = []
    for pi, page in enumerate(scheme):
        if page.rotation:
            continue
        H = page.rect.height
        for r in page.search_for(divider_title):
            if r.y0 < H * DIVIDER_TOP_FRAC:
                out.append(pi)
                break
        else:
            # Some SEC Maths PDFs visually print "Paper 2" on the divider but
            # encode the title as separately positioned glyph runs, so
            # PyMuPDF's phrase search cannot see it.  Fall back to the already
            # line-grouped words while retaining the same top-half guard.
            wanted = re.sub(r"\s+", " ", divider_title).casefold()
            for words in line_groups(page):
                # SEC divider covers are vertically centred (the 2018 Paper 2
                # title sits about two-thirds down the page), so the glyph-run
                # fallback deliberately scans farther than phrase search.
                if not words or words[0][1] >= H * 0.8:
                    continue
                line = " ".join(_deligature(word[4]) for word in words)
                if wanted in re.sub(r"\s+", " ", line).casefold():
                    out.append(pi)
                    break
    return out


def find_paper_band(scheme, k):
    """[start, end) 0-based page band for 'Paper k' in a shared P1+P2 scheme,
    or None. Contents-aware: a cover/contents page names BOTH papers at the top
    (the Maths schemes do, EN and GA alike), so single-occurrence logic banded
    Paper 2 at the contents page and its chips fell through to Paper 1's
    questions — a cross-paper mis-map that count-reconcile cannot see. The
    robust reading: discard pages naming both papers, then the Paper-2 divider
    is the first of its pages past EVERY Paper-1 page (running per-page
    headers make 'last occurrence' equally wrong in the other direction)."""
    def occ(n):
        pages = set()
        for t in (f"Paper {n}", f"Páipéar {n}", f"PÁIPÉAR {n}"):
            pages |= set(find_band_pages(scheme, t))
        return pages
    p1, p2 = occ(1), occ(2)
    shared = p1 & p2
    p1, p2 = sorted(p1 - shared), sorted(p2 - shared)
    if not p2:
        # No Paper-2 divider at all: Paper 1 runs to the end (or the scheme is
        # genuinely single-paper); Paper 2 cannot be banded.
        return (min(p1), len(scheme)) if k == 1 and p1 else None
    # Prefer an actual sparse divider cover over a dense page whose running
    # header happens to say ``Paper 2``.  The 2023 Irish Higher scheme has a
    # misleading Paper-2 label on a Paper-1 instruction page; taking the first
    # occurrence shifted every Paper-1 answer into unrelated material.
    sparse_p2 = [
        p for p in p2
        if len(re.sub(r"\s+", " ", scheme[p].get_text("text")).strip()) < 500
    ]
    if sparse_p2:
        p2 = sparse_p2
    # The boundary is the first Paper-2 page with the FEWEST Paper-1 pages
    # after it — ideally zero, but the SEC's own 2016-era schemes repeat the
    # "Marking Scheme – Paper 1 …" boilerplate header inside the Paper-2 half,
    # so a single stray must not sink the whole band.
    def strays(b):
        return sum(1 for p in p1 if p >= b)
    best = min(strays(b) for b in p2)
    boundary = next(b for b in p2 if strays(b) == best)
    if p1 and boundary <= min(p1):
        return None  # every Paper-2 mention precedes Paper 1 — not a real split
    if k == 1:
        return (p1[0], boundary) if p1 else None
    return (boundary, len(scheme))


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
    # Irish-medium (IV) scheme boilerplate — the same general-guideline pages,
    # numbered 1..N, that decoy the detectors when not skipped (2012-era Maths
    # IV anchored every chip on the penalties list before these were added).
    "treoirlínte ginearálta do scrúdaitheoirí",
    "na treoirlínte a chur i bhfeidhm",
    "cuirtear trí chineál pionóis",
    "nótaí ginearálta maidir leis an marcáil",
    "marcanna breise as ucht freagairt trí ghaeilge",
    "scéim mharcála a úsáid",
    "ní foláir d'iarrthóirí",
    "ba chóir na pointí seo a leanas",
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
        # Some IV schemes extract with every space glued away ("bachóirnapointí…"),
        # so match phrases with spaces stripped from BOTH sides.
        t_glued = t.replace(" ", "")
        if any(p in t or p.replace(" ", "") in t_glued for p in FRONT_MATTER_PHRASES):
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
    real per-question headers + a scheme.

    DO NOT SHIP THIS OUTPUT (2026-08 audit). Proportional placement mis-navigates
    wherever per-question page counts vary or the scheme's structure differs from
    the paper's numbering — which is exactly where the precise path drops. All 64
    fallback sidecars produced for 2026 were render-audited and deleted; see
    README.md §Annual refresh item 6. build-index.py flags fallback sidecars
    UNGATED, so anything left in answers/ goes live."""
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

    _code = (decode_fileid(os.path.basename(paper_path)) or {}).get("code")
    _continuation = _code in CONTINUATION_CODES
    ph = detect_paper_headers(paper, allow_k_start=_continuation)
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

    # Band for this paper within (possibly shared) scheme (EN + GA titles,
    # contents-page aware — see find_paper_band).
    if band_strategy[0] == "divider":
        k = band_strategy[1]
        band = find_paper_band(scheme, k)
        if band is None:
            return drop(f"band 'Paper {k}' not found")
        band_start, band_end = band
    else:
        band_start, band_end = 0, len(scheme)

    fm_start = front_matter_end(scheme, band_start, band_end)
    markers = detect_scheme_markers(scheme, fm_start, band_end, want_ns, detector,
                                    divider_band=(band_strategy[0] == "divider"
                                                  or _continuation))
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
                if not is_blank(scheme[mid]):  # never crop a blank scheme page
                    region.append({"p": mid + 1, "r": [0.0, 0.0, 1.0, 1.0]})
            if not is_blank(scheme[e_pi]):
                region.append({"p": e_pi + 1, "r": [0.0, 0.0, 1.0, round(e_yfrac, 4)]})
        else:
            ok = False

        if ok:
            for seg in region:
                if any(not (0.0 <= v <= 1.0) for v in seg["r"]) or scheme[seg["p"] - 1].rotation:
                    ok = False
                    break

        if ok:
            q_out = {"n": str(n), "pP": p_pi + 1, "pY": p_yband,
                     "region": region, "mode": "crop", "conf": 1.0}
            if detector == "topic":
                # topic-organised papers (old-spec Classical Studies): the chip
                # heads 'Topic N', so name it that way in the reveal panel
                q_out["label"] = ("Topaic" if "IV.pdf" in os.path.basename(paper_path)
                                  else "Topic") + f" {n}"
            qout.append(q_out)
            stats["crop"] += 1
        else:
            qout.append({"n": str(n), "pP": p_pi + 1, "pY": p_yband,
                         "region": [{"p": s_pi + 1}], "mode": "pagejump", "conf": 0.6})
            stats["pagejump"] += 1

    if not qout:
        stats["reason"] = "no questions mapped"
        return None, stats

    # Chip order must follow the paper's print order (the viewer derives crop
    # bands from consecutive anchors). A non-monotonic n sequence means the
    # paper-side headers captured a section restart — drop, never ship (PE 2023
    # wrote 9..13,1..8 before this gate; vitest caught it post-hoc).
    ns = [int(q["n"]) for q in qout]
    if any(b <= a for a, b in zip(ns, ns[1:])):
        stats["reason"] = "paper chip order not monotonic (section restart)"
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

# Content-verified NO-GO list: (code, component, levelCode-or-None, lang-or-None,
# year-or-None). These pairs produce maps that pass every structural gate but are
# WRONG at the content level (render-verified) — the engine must never emit them,
# or each sweep resurrects a deleted defect. None = wildcard.
NEVER_MAP = (
    # Art practical components (Design/Craftwork/Coursework): the shared scheme's
    # criteria grids decoy-anchor 'Q.N' from the wrong component (2016 Design Q6
    # opened the H&A 'Berry Dress' rows). All levels, both languages.
    ("LC014", "010", None, None, None),
    ("LC014", "011", None, None, None),
    ("LC014", "027", None, None, None),
    # Accounting HL IV: the scheme numbers its working LINES (Q9 chip opened
    # arithmetic item 9 of another solution). EV heads real 'Question N' blocks.
    ("LC032", "000", "A", "IV", None),
    # Geography OL IV 2025 Part Two: anchors the Part One short-answer key.
    ("LC005", "043", "G", "IV", None),
    # History OL: the scheme's numbered RSR criteria list ("3. Criticism
    # (20 marks)") reconciles against the paper's document questions — the
    # documented mainstream-History-OL blocker, confirmed again by render.
    ("LC004", "000", "G", None, None),
    # Biology Sections A&B (038) EV transition years: the chip crops the
    # Q-marks grid, not the answers. The IV twins map correctly.
    ("LC025", "038", "A", "EV", 2020),
    ("LC025", "038", "A", "EV", 2022),
    ("LC025", "038", "A", "EV", 2023),
)


def never_map(d, year):
    for code, comp, lvl, lang, yr in NEVER_MAP:
        if (d["code"] == code and d["component"] == comp
                and lvl in (None, d["levelCode"])
                and lang in (None, d["lang"].upper())
                and yr in (None, year)):
            return True
    return False


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
        if not d or d["exam"] not in SCOPE_EXAMS:
            continue
        if d["code"] in DONE_CODES and not include_done:
            continue  # frozen — lit in an earlier wave, never re-mapped
        if SCOPE_CODES is not None and d["code"] not in SCOPE_CODES:
            continue  # --codes filters unconditionally (targeted re-runs)
        if d["levelCode"] not in SCOPE_LEVELS or d["lang"] not in langs:
            continue
        if r["view"] == "exampapers" and never_map(d, int(r["year"])):
            continue  # content-verified wrong (NEVER_MAP) — never emit
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
    # Annual-refresh knobs (README "Annual refresh"): --years 2026 scopes the
    # run to the new year; --include-done also ATTEMPTS the frozen DONE_CODES
    # subjects for those years (their committed sidecars for other years are
    # protected by the SCOPE_YEARS guard on the clearing loop above). Codes
    # owned by the bespoke generators are still excluded via --skip-codes.
    global SCOPE_YEARS, DONE_CODES, SCOPE_CODES
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--years", help="comma-separated years to (re)map, e.g. 2026")
    ap.add_argument("--include-done", action="store_true",
                    help="attempt frozen DONE_CODES subjects too (new-year refresh)")
    ap.add_argument("--codes", default="",
                    help="comma-separated SEC codes to attempt EXCLUSIVELY "
                         "(e.g. LC024) — targeted re-runs after an engine fix")
    ap.add_argument("--skip-codes", default="",
                    help="comma-separated SEC codes to leave alone (bespoke-owned)")
    ap.add_argument("--langs", default="",
                    help="comma-separated language codes to attempt (default EV; "
                         "the IV-audit profiles need EV,IV)")
    ap.add_argument("--levels", default="",
                    help="comma-separated level codes to attempt (default A,G,C; "
                         "Foundation maths needs A,G,C,B)")
    ap.add_argument("--exams", default="",
                    help="comma-separated exam prefixes to attempt "
                         "(default LC; the JC/LCA profiles need LC,JC,LB)")
    ap.add_argument("--fallback", action="store_true",
                    help="also run the universal navigation-fallback pass "
                         "(conf-0.3 page-jump chips for papers the precise "
                         "engine drops; ships ungated by design)")
    args = ap.parse_args()
    global SCOPE_LANGS, SCOPE_LEVELS, UNIVERSAL_FALLBACK, SCOPE_EXAMS, SCOPE_CODES
    if args.years:
        SCOPE_YEARS = {int(y) for y in args.years.split(",")}
    if args.codes:
        SCOPE_CODES = {c.strip().upper() for c in args.codes.split(",") if c.strip()}
    if args.langs:
        SCOPE_LANGS = {x.strip().upper() for x in args.langs.split(",") if x.strip()}
    if args.levels:
        SCOPE_LEVELS = {x.strip().upper() for x in args.levels.split(",") if x.strip()}
    if args.exams:
        SCOPE_EXAMS = {x.strip().upper() for x in args.exams.split(",") if x.strip()}
    if args.fallback:
        UNIVERSAL_FALLBACK = True
    skip = {c.strip().upper() for c in args.skip_codes.split(",") if c.strip()}
    if args.include_done:
        DONE_CODES = set(skip)
    elif skip:
        DONE_CODES = DONE_CODES | skip
    log("Paper Trail — Stage 2.5: anchor maps (auto-grammar)")
    log(f"  scope: years {sorted(SCOPE_YEARS)} | frozen codes: {len(DONE_CODES)}")
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

    # Clear only the sidecars this run will regenerate (in-scope, not frozen,
    # AND within SCOPE_YEARS) so earlier waves' committed sidecars survive —
    # each wave is additive. The year guard matters on an annual refresh: a run
    # scoped to the new year can only regenerate that year's files, so it must
    # only clear that year's files — without it, extending a frozen subject to
    # the new year (DONE_CODES emptied, SCOPE_YEARS={new}) would delete every
    # committed sidecar of every attempted code whose corpus PDF is not on the
    # machine, silently de-flagging shipped papers.
    def in_scope_code(code):
        return (code[:2].upper() in SCOPE_EXAMS
                and code not in DONE_CODES
                and (SCOPE_CODES is None or code in SCOPE_CODES))

    # Lang/level guard: a run scoped to --langs IV must clear ONLY the IV
    # sidecars of an in-scope code — the code prefix alone is lang-blind, and
    # clearing by code would delete committed EV sidecars this run cannot
    # regenerate (the bespoke-authored ones most of all). Same for levels.
    _sidecar_re = re.compile(r"^(LC|JC|LB)\d{3}([A-Z])L?P[A-Z0-9]{3}(EV|IV|BV)\.pdf\.json$", re.I)

    # Committed sidecars the generic engine cannot regenerate (special-cased
    # years authored via FILEID_FIXES or hand-verified one-offs). Clearing one
    # of these silently unships it on every sweep — preserve by exact name.
    CLEARING_PRESERVE = {
        (2011, "LC014ALP013IV.pdf.json"),  # Art H&A IV 2011 (FILEID_FIXES year)
        (2011, "LC003ALP100IV.pdf.json"),  # Maths HL P1 IV 2011 (FILEID_FIXES year)
    }

    def in_scope_sidecar(fn, year):
        if (year, fn) in CLEARING_PRESERVE:
            return False
        m = _sidecar_re.match(fn)
        if not m:
            return False  # unrecognised name — never delete what we can't parse
        return (in_scope_code(fn[:5])
                and m.group(2).upper() in SCOPE_LEVELS
                and m.group(3).upper() in SCOPE_LANGS)
    if os.path.isdir(ANSWERS_DIR):
        for yd in os.listdir(ANSWERS_DIR):
            ydp = os.path.join(ANSWERS_DIR, yd)
            if not (yd.isdigit() and int(yd) in SCOPE_YEARS):
                continue
            if os.path.isdir(ydp):
                for fn in os.listdir(ydp):
                    if in_scope_sidecar(fn, int(yd)):
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
    rep.append(f"Scope: {'/'.join(sorted(SCOPE_EXAMS))} levels {sorted(SCOPE_LEVELS)} langs {sorted(SCOPE_LANGS)} "
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
