#!/usr/bin/env python3
"""
Paper Trail — PAPER-SIDE-ONLY question anchors for the Topic Vault.

~2,000 index papers have no answer-map sidecar (scheme unmappable or not yet
attempted), so the vault cannot crop their questions. This generator produces a
paper-anchors artifact for those papers: the SAME PaperAnswerMap sidecar schema
(types/paperTrail.ts) with real per-question paper anchors (pP/pY) but NO scheme
mapping claimed — every question is mode:'pagejump' with a placeholder region
[{p:1}], schemeFileid "" and a `paperOnly:1` marker. The vault only needs pP/pY
(components/PaperTrail/paperRegion.ts derives the paper crop from anchor N to
anchor N+1); mode:'crop' is required only for the answer-reveal toggle, so these
maps light up the question crop while the card keeps its honest "Open beside its
marking scheme" fallback.

HOSTING (Storage uploads are credential-blocked, task #94): outputs are staged
into public/paper-anchors/<year>/<paperFileid>.json and deploy with the app via
Firebase Hosting on push to main — no Storage objects. The vault tries the
Storage sidecar first and falls back to this hosted path (vaultResolve.ts).

HONESTY GATES — a wrong crop is worse than none:
  • detectors only accept a question token that STARTS a line at the left
    margin of an unrotated page;
  • per-question QA: after building the map, each anchor is independently
    re-verified — the expected marker text must be re-found at (pP, pY[0]);
  • sequence gates: anchors must be monotonic in print order and contiguous
    (1..max per section) — any gap, duplicate-in-doubt or rotated-page anchor
    drops the QUESTION;
  • hole gate: a content page BETWEEN two anchors that carries no anchor means
    a question was missed — its neighbour's derived crop would swallow it, so
    the whole PAPER is dropped;
  • tail gate: pages after the last anchor must be blank / "no examination
    material" / a short back cover — otherwise the last question's extent is
    uncertain and the PAPER is dropped;
  • coverage gate: a paper ships only when ≥ MIN_QUESTIONS anchor and
    anchored/expected ≥ MIN_COVERAGE (expected = contiguous 1..max per section).

Usage:
  python3 paper_anchors.py <subjectId> [--grammar auto|section_token|question|lead_int]
                           [--years 2010-2025] [--qa-render N] [--dry-run]

Outputs (deterministic, sorted, idempotent):
  public/paper-anchors/<year>/<paperFileid>.json     (committed, hosted)
  scripts/paper-trail/out/paper-anchors-<subject>-report.md
  scripts/paper-trail/out/qa-render/<subject>/*.png  (--qa-render only)

All emitted page numbers are 1-BASED; all bands are fractions of the unrotated
page box — exactly the conventions of anchor-map.py and the viewer.
"""

import argparse
import json
import os
import random
import re
import sys
import urllib.request
from collections import defaultdict

import fitz  # pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
INDEX_TS = os.path.join(REPO, "paperTrailData.ts")
CORPUS = os.path.join(REPO, "paper-trail-corpus")          # gitignored cache
PUBLIC_OUT = os.path.join(REPO, "public", "paper-anchors")  # committed, hosted
OUT_DIR = os.path.join(HERE, "out")

BUCKET = "nextstepuni-app.firebasestorage.app"
SIDECAR_V = 1
COPYRIGHT = "© State Examinations Commission"

LEFT_MARGIN_X = 140   # a header token must start left of this (points)
LEAD_INT_X = 95       # a bare 'N.' lead number sits within this of the left edge
MIN_QUESTIONS = 3     # a paper needs ≥3 anchored questions to be worth shipping
MIN_COVERAGE = 0.6    # anchored/expected below this → drop the paper
PAGEJUMP_CONF = 0.5   # below anchor-map's 0.6 "right scheme page" tier: no scheme claim
MAX_TAIL_CHARS = 400  # a post-questions page longer than this is unexplained content

# Pages that carry no question content (fillers, back covers).
BLANK_PAGE_TEXTS = {
    "", "blank page", "this page is intentionally blank",
    "this page has been left blank intentionally",
    "this page has been intentionally left blank",
    "there is no examination material on this page",
}

# Per-subject grammar pins. Everything else runs 'auto' (best detector wins),
# but a pinned grammar removes one degree of freedom — prefer pinning when
# rolling a subject out. See PAPER-ANCHORS.md for the rollout recipe.
SUBJECT_GRAMMAR = {
    "design-and-communication-graphics": "section_token",
    # Sciences wave: LC biology/chemistry/physics print questions as a bare
    # left-margin 'N.' in every era (pre- and post-2020 formats verified).
    "biology": "lead_int",
    "chemistry": "lead_int",
    "physics": "lead_int",
    # agricultural-science is era-split (old spec ≤2020: 'N.' lead ints; new
    # spec 2021+: 'Question N') — run it with explicit --years + --grammar
    # per era rather than a single pin.
    # mathematics is era-split too, so it runs UNPINNED (auto): compact
    # pre-Project-Maths papers (2010–2012 P100/P200/P000) print bare 'N.'
    # lead ints; every Project-Maths-format paper (P130/P230 pilots and all
    # papers 2013+) prints 'Question N' / 'Ceist N'. The PM-format papers are
    # answer booklets whose questions span multiple pages (continuation parts
    # and answer space between headers), so they drop at the hole gate
    # regardless of grammar; only the lead_int era passes the gates
    # (2026-07 maths wave — see out/paper-anchors-mathematics-report.md).
}

_LIGATURES = {
    "Ɵ": "ti", "Ʃ": "tt", "ϐ": "fi",
    "ﬀ": "ff", "ﬁ": "fi", "ﬂ": "fl",
    "ﬃ": "ffi", "ﬄ": "ffl", "ﬅ": "ft", "ﬆ": "st",
}


def deligature(s):
    if s.isascii():
        return s
    for k, v in _LIGATURES.items():
        if k in s:
            s = s.replace(k, v)
    return s


def norm_text(s):
    return re.sub(r"[^a-z0-9]+", " ", deligature(s).lower()).strip()


def log(msg):
    print(msg, flush=True)


# ─── index parsing (paperTrailData.ts is line-per-entry JSON) ─────────────────

def load_subject_index(subject_id):
    """(cycle, [(year, level, lang, label, fileid), ...]) for one subject."""
    with open(INDEX_TS, encoding="utf-8") as f:
        src = f.read()
    m = re.search(r'\{"id":\s*"%s".*?\}' % re.escape(subject_id), src)
    if not m:
        raise SystemExit(f"subject {subject_id!r} not in PAPER_TRAIL_SUBJECTS")
    cycle = json.loads(m.group(0))["cycle"]

    block_m = re.search(r'"%s":\s*\[\n(.*?)\n  \],' % re.escape(subject_id), src, re.S)
    if not block_m:
        raise SystemExit(f"subject {subject_id!r} has no PAPER_TRAIL_INDEX block")
    rows = []
    for line in block_m.group(1).splitlines():
        line = line.strip().rstrip(",")
        if not line.startswith('{"year"'):
            continue
        e = json.loads(line)
        for p in e["papers"]:
            rows.append({
                "year": e["year"], "level": e["level"], "lang": e["lang"],
                "label": p["label"], "fileid": p["doc"]["f"],
                "hasAnswers": p.get("answers") == 1,
            })
    return cycle, rows


# ─── download (public Storage REST, same layout as download.py) ──────────────

def fetch_paper(cycle, subject_id, year, fileid):
    dst = os.path.join(CORPUS, "exampapers", str(year), fileid)
    if os.path.exists(dst) and os.path.getsize(dst) > 0:
        return dst
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    path = f"papers/{cycle}/{subject_id}/{year}/paper/{fileid}"
    url = (f"https://firebasestorage.googleapis.com/v0/b/{BUCKET}/o/"
           + urllib.parse.quote(path, safe="") + "?alt=media")
    try:
        with urllib.request.urlopen(url, timeout=120) as r, open(dst + ".part", "wb") as fh:
            while True:
                chunk = r.read(1 << 16)
                if not chunk:
                    break
                fh.write(chunk)
        os.replace(dst + ".part", dst)
        return dst
    except Exception as e:  # noqa: BLE001 — report + drop, never guess
        if os.path.exists(dst + ".part"):
            os.remove(dst + ".part")
        log(f"    download FAILED {fileid}: {e}")
        return None


# ─── PDF primitives ───────────────────────────────────────────────────────────

def line_groups(page):
    """get_text('words') grouped into lines, each sorted left→right."""
    lines = defaultdict(list)
    for w in page.get_text("words"):
        lines[(w[5], w[6])].append(w)
    for lw in lines.values():
        lw.sort(key=lambda w: w[0])
    return list(lines.values())


def is_blank(page):
    if re.sub(r"\d+", "", norm_text(page.get_text("text"))).strip() in BLANK_PAGE_TEXTS:
        return True
    if page.get_text("text").strip():
        return False
    if page.get_images():
        return False
    try:
        return len(page.get_drawings()) <= 3
    except Exception:  # noqa: BLE001
        return True


# ─── detectors: hits are (sort_key, printed_label, page0, x0, yFrac) ─────────
# sort_key orders questions across the doc: (section_index, number).

SECTION_TOKEN_RE = re.compile(r"([A-C])-(\d{1,2})\.?")


def det_section_token(doc):
    """'A-1.' / 'B-2' / 'C-3.' as the FIRST word of a left-margin line (DCG,
    Engineering-style sectioned papers)."""
    hits = []
    for pi, page in enumerate(doc):
        if page.rotation:
            continue
        H = page.rect.height
        for lw in line_groups(page):
            w = lw[0]
            m = SECTION_TOKEN_RE.fullmatch(deligature(w[4]))
            if m and w[0] < LEFT_MARGIN_X:
                sec, num = m.group(1), int(m.group(2))
                hits.append(((ord(sec) - ord("A"), num), f"{sec}-{num}", pi, w[0], w[1] / H))
    return hits


def det_question_word(doc):
    hits = []
    for pi, page in enumerate(doc):
        if page.rotation:
            continue
        H = page.rect.height
        for lw in line_groups(page):
            for i, w in enumerate(lw):
                word = deligature(w[4])
                if word not in ("Question", "QUESTION", "Ceist", "CEIST") or i + 1 >= len(lw):
                    continue
                m = re.fullmatch(r"(\d+)[.:]?", lw[i + 1][4])
                if m and w[0] < LEFT_MARGIN_X:
                    n = int(m.group(1))
                    hits.append(((0, n), str(n), pi, w[0], w[1] / H))
    return hits


def det_lead_int(doc):
    hits = []
    for pi, page in enumerate(doc):
        if page.rotation:
            continue
        H = page.rect.height
        for lw in line_groups(page):
            w = lw[0]
            m = re.fullmatch(r"(\d{1,2})\.", w[4])
            if m and w[0] < LEAD_INT_X:
                n = int(m.group(1))
                hits.append(((0, n), str(n), pi, w[0], w[1] / H))
    return hits


DETECTORS = {
    "section_token": det_section_token,
    "question": det_question_word,
    "lead_int": det_lead_int,
}


# ─── anchor building + gates ──────────────────────────────────────────────────

def build_anchors(doc, hits):
    """hits → (anchors, expected, reasons). anchors = [(sort_key, label, page0,
    x0, yFrac)] deduped/ordered; expected counts contiguous 1..max per section.
    Question-level drops are recorded in reasons; paper-level gates run later."""
    reasons = []
    first = {}
    for h in sorted(hits, key=lambda h: (h[2], h[4])):  # print order
        first.setdefault(h[0], h)                        # first occurrence wins

    by_sec = defaultdict(list)
    for key in sorted(first):
        by_sec[key[0]].append(key[1])

    anchors, expected = [], 0
    for sec in sorted(by_sec):
        nums = by_sec[sec]
        top = max(nums)
        expected += top
        missing = sorted(set(range(1, top + 1)) - set(nums))
        if missing:
            reasons.append(f"section {sec}: missing question number(s) {missing}")
        for n in range(1, top + 1):
            if n in nums:
                anchors.append(first[(sec, n)])

    anchors.sort(key=lambda a: a[0])
    # print order must match question order — else the layout defeats the
    # anchor→next-anchor crop derivation and every question is in doubt.
    pos = [(a[2], a[4]) for a in anchors]
    if any(pos[i] >= pos[i + 1] for i in range(len(pos) - 1)):
        return [], expected, reasons + ["anchors not monotonic in print order"]
    return anchors, expected, reasons


def paper_gates(doc, anchors, expected, reasons):
    """Paper-level honesty gates. Returns None when the paper passes, else the
    drop reason."""
    if len(anchors) < MIN_QUESTIONS:
        return f"only {len(anchors)} anchored questions (<{MIN_QUESTIONS}): " + "; ".join(reasons)
    if expected and len(anchors) / expected < MIN_COVERAGE:
        return (f"coverage {len(anchors)}/{expected} < {MIN_COVERAGE:.0%}: "
                + "; ".join(reasons))

    pages_with = {a[2] for a in anchors}
    first_p, last_p = min(pages_with), max(pages_with)

    # Hole gate: an anchor-less content page between anchors = a missed question
    # whose neighbour's derived crop would swallow it.
    for pi in range(first_p, last_p + 1):
        if pi in pages_with:
            continue
        if not is_blank(doc[pi]) and not doc[pi].rotation:
            return f"content page {pi + 1} between anchors carries no anchor (missed question?)"
        if doc[pi].rotation:
            return f"rotated page {pi + 1} between anchors (unrepresentable question?)"

    # Tail gate: after the last anchor only fillers / a short back cover.
    for pi in range(last_p + 1, len(doc)):
        page = doc[pi]
        if is_blank(page):
            continue
        t = norm_text(page.get_text("text"))
        if len(t) > MAX_TAIL_CHARS or SECTION_TOKEN_RE.search(page.get_text("text")):
            return f"page {pi + 1} after the last anchor still carries content"
    return None


def qa_verify(pdf_path, sidecar, grammar):
    """Independent per-question re-verification: re-open the PDF and require the
    printed marker text to be re-found at each anchor position. Any mismatch
    fails the WHOLE paper (the generator and verifier disagreeing = doubt)."""
    doc = fitz.open(pdf_path)
    det = DETECTORS[grammar]
    hits = det(doc)
    by_pos = {}
    for _, label, pi, _x, y in hits:
        by_pos.setdefault((pi, round(y, 3)), set()).add(label)
    for q in sidecar["q"]:
        want = q.get("label") or f"{q['n']}"
        found = by_pos.get((q["pP"] - 1, round(q["pY"][0], 3)), set())
        # tolerate rounding: scan nearby y keys on the same page
        if want not in found:
            near = {lab for (pi, y), labs in by_pos.items()
                    if pi == q["pP"] - 1 and abs(y - q["pY"][0]) < 0.004 for lab in labs}
            if want not in near:
                return f"Q{q['n']} ({want}): marker not re-found at page {q['pP']} y={q['pY'][0]}"
    return None


# ─── sidecar emit ─────────────────────────────────────────────────────────────

def component_of(fileid):
    m = re.match(r"^(LC|JC|LB)(\d{3})([A-Z])L?P([A-Z0-9]{3})(EV|IV|BV)\.pdf$", fileid, re.I)
    return m.group(4).upper() if m else ""


def make_sidecar(fileid, anchors, doc):
    by_page = defaultdict(list)
    for a in anchors:
        by_page[a[2]].append(a[4])
    for pi in by_page:
        by_page[pi].sort()

    qout = []
    for i, (_key, label, pi, _x, y) in enumerate(anchors, start=1):
        nxt = next((yf for yf in by_page[pi] if yf > y + 1e-6), 1.0)
        q = {
            "n": str(i),
            "pP": pi + 1,
            "pY": [round(y, 4), round(nxt, 4)],
            "region": [{"p": 1}],
            "mode": "pagejump",
            "conf": PAGEJUMP_CONF,
        }
        if label != str(i):
            q["label"] = label
        qout.append(q)
    return {
        "v": SIDECAR_V,
        "paperFileid": fileid,
        "schemeFileid": "",     # paper-only: NO scheme mapping claimed
        "component": component_of(fileid),
        "band": [1, 1],         # empty band — nothing indexes into a scheme
        "copyright": COPYRIGHT,
        "paperOnly": 1,
        "q": qout,
    }


# ─── QA render (ports components/PaperTrail/paperRegion.ts) ──────────────────

TOP_PAD = 0.008
MAX_PAGES = 3
MIN_TAIL = 0.03


def paper_region_for(qs, n):
    """Mirror of paperRegionFor in components/PaperTrail/paperRegion.ts."""
    ordered = sorted(qs, key=lambda q: (q["pP"], q["pY"][0]))
    idx = next((i for i, q in enumerate(ordered) if q["n"] == n), -1)
    if idx == -1:
        return None
    q = ordered[idx]
    y0 = max(0.0, min(1.0, q["pY"][0]) - TOP_PAD)
    nxt = ordered[idx + 1] if idx + 1 < len(ordered) else None
    if nxt is None:
        y1 = q["pY"][1] if q["pY"][1] > y0 + 0.01 else 1.0
        return [{"p": q["pP"], "r": [0, y0, 1, min(1.0, y1)]}]
    if nxt["pP"] < q["pP"] or (nxt["pP"] == q["pP"] and nxt["pY"][0] <= q["pY"][0] + 0.005):
        return None
    span = nxt["pP"] - q["pP"]
    if span > MAX_PAGES:
        return None
    if span == 0:
        return [{"p": q["pP"], "r": [0, y0, 1, min(1.0, nxt["pY"][0])]}]
    segs = [{"p": q["pP"], "r": [0, y0, 1, 1]}]
    for p in range(q["pP"] + 1, nxt["pP"]):
        segs.append({"p": p, "r": [0, 0, 1, 1]})
    tail = min(1.0, nxt["pY"][0])
    if tail > MIN_TAIL:
        segs.append({"p": nxt["pP"], "r": [0, 0, 1, tail]})
    return segs


def qa_render(pdf_path, sidecar, out_dir, n_samples, rng, year):
    """Render N random derived question crops to PNG for visual QA."""
    doc = fitz.open(pdf_path)
    qs = sidecar["q"]
    os.makedirs(out_dir, exist_ok=True)
    sample = rng.sample(qs, min(n_samples, len(qs)))
    rendered = []
    for q in sample:
        region = paper_region_for(qs, q["n"])
        if not region:
            continue
        pixmaps = []
        for seg in region:
            page = doc[seg["p"] - 1]
            r = seg["r"]
            clip = fitz.Rect(r[0] * page.rect.width, r[1] * page.rect.height,
                             r[2] * page.rect.width, r[3] * page.rect.height)
            pixmaps.append(page.get_pixmap(clip=clip, dpi=100))
        w = max(p.width for p in pixmaps)
        h = sum(p.height for p in pixmaps)
        combo = fitz.Pixmap(fitz.csRGB, fitz.IRect(0, 0, w, h))
        combo.clear_with(255)
        y = 0
        for p in pixmaps:
            combo.copy(p, fitz.IRect(0, y, p.width, y + p.height))
            y += p.height
        label = q.get("label", q["n"]).replace("/", "_")
        fn = os.path.join(out_dir, f"{year}-{sidecar['paperFileid']}-Q{q['n']}-{label}.png")
        combo.save(fn)
        rendered.append(fn)
    return rendered


# ─── main ─────────────────────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    ap.add_argument("subject")
    ap.add_argument("--grammar", default=None,
                    help="pin a detector (default: SUBJECT_GRAMMAR pin, else auto)")
    ap.add_argument("--years", default="2010-2025")
    ap.add_argument("--qa-render", type=int, default=0, metavar="N",
                    help="render N random derived crops per anchored paper")
    ap.add_argument("--seed", type=int, default=562)
    ap.add_argument("--dry-run", action="store_true", help="no files written")
    args = ap.parse_args()

    y0, y1 = (int(x) for x in args.years.split("-"))
    years = set(range(y0, y1 + 1))
    cycle, rows = load_subject_index(args.subject)
    rows = [r for r in rows if r["year"] in years]
    grammar_pin = args.grammar or SUBJECT_GRAMMAR.get(args.subject)
    rng = random.Random(args.seed)

    log(f"paper-anchors: {args.subject} ({cycle}) — {len(rows)} papers, "
        f"grammar {grammar_pin or 'auto'}")

    report, shipped, dropped, skipped = [], 0, 0, 0
    for r in sorted(rows, key=lambda r: (-r["year"], r["level"], r["lang"], r["fileid"])):
        tag = f"{r['year']} {r['level']}/{r['lang']} {r['label']} {r['fileid']}"
        if r["hasAnswers"]:
            skipped += 1
            report.append((tag, "SKIP", "already has a verified Storage sidecar"))
            continue
        pdf_path = fetch_paper(cycle, args.subject, r["year"], r["fileid"])
        if not pdf_path:
            dropped += 1
            report.append((tag, "DROP", "download failed"))
            continue

        doc = fitz.open(pdf_path)
        cands = [grammar_pin] if grammar_pin else list(DETECTORS)
        best = None  # (grammar, anchors, expected, reasons)
        for g in cands:
            anchors, expected, reasons = build_anchors(doc, DETECTORS[g](doc))
            if best is None or len(anchors) > len(best[1]):
                best = (g, anchors, expected, reasons)
        g, anchors, expected, reasons = best
        drop = paper_gates(doc, anchors, expected, reasons)
        if drop:
            dropped += 1
            report.append((tag, "DROP", drop))
            continue

        sidecar = make_sidecar(r["fileid"], anchors, doc)
        qa_fail = qa_verify(pdf_path, sidecar, g)
        if qa_fail:
            dropped += 1
            report.append((tag, "DROP", f"QA re-verify failed: {qa_fail}"))
            continue

        if not args.dry_run:
            ydir = os.path.join(PUBLIC_OUT, str(r["year"]))
            os.makedirs(ydir, exist_ok=True)
            with open(os.path.join(ydir, f"{r['fileid']}.json"), "w", encoding="utf-8") as fh:
                json.dump(sidecar, fh, ensure_ascii=False, sort_keys=True,
                          separators=(",", ":"))
        rendered = []
        if args.qa_render:
            rdir = os.path.join(OUT_DIR, "qa-render", args.subject)
            rendered = qa_render(pdf_path, sidecar, rdir, args.qa_render, rng, r["year"])
        labels = ",".join(q.get("label", q["n"]) for q in sidecar["q"])
        detail = f"{len(sidecar['q'])}q [{labels}] via {g}"
        if rendered:
            detail += f" · {len(rendered)} QA crops"
        shipped += 1
        report.append((tag, "ANCHORED", detail))

    os.makedirs(OUT_DIR, exist_ok=True)
    rep_path = os.path.join(OUT_DIR, f"paper-anchors-{args.subject}-report.md")
    with open(rep_path, "w", encoding="utf-8") as f:
        f.write(f"# Paper anchors — {args.subject}\n\n")
        f.write(f"**{shipped} anchored · {dropped} dropped · {skipped} skipped "
                f"(already sidecar'd)** of {len(rows)} papers\n\n")
        f.write("| paper | status | detail |\n|---|---|---|\n")
        for tag, status, detail in report:
            f.write(f"| {tag} | {status} | {detail} |\n")
    log(f"  {shipped} anchored · {dropped} dropped · {skipped} skipped")
    log(f"  → {os.path.relpath(rep_path, REPO)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
