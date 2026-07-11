#!/usr/bin/env python3
"""
Paper Trail — hosted paper-anchors derived from scheme-verified CLASSIC
sidecars, cross-validated against the paper's text layer (TV-14, arabic).

WHY NOT THE DETECTOR PIPELINE. arabic (LC059) is an RTL paper whose question
markers are right-margin Arabic-Indic numerals — new detector capability
(paper_anchors.rtl_marker_rows). But its vault tags are SUBPART-numbered: the
printed paper numbers questions 1..14 (+15 composition), while the tags and
the answers-wave classics give each literature subpart its own sequential n
('Literature · Q7 (أ)' = n7, '(ب)' = n8, …), era-dependent (17 n pre-2021,
20 n after). A printed-number detector therefore CANNOT reproduce the tag
numbering (the dual-numbering trap, PAPER-ANCHORS.md) — but the repo already
carries scheme-verified classic sidecars for every tagged arabic sitting
(scripts/paper-trail/answers/<year>/<fileid>.json, built by lang_reading.py
from hand-authored specs; NOT live on Storage while task #94 is blocked, so
the vault currently serves NOTHING for arabic).

WHAT THIS SCRIPT DOES. For each index paper of the subject:
  1. loads the local classic sidecar (no classic → DROP);
  2. mirrors the CI contract on it (test/vaultAnchors.test.ts: dense
     sequential n from 1, strictly monotonic anchors, a non-null
     paperRegionFor crop for every question);
  3. CROSS-VALIDATES every classic paper anchor against the actual text
     layer using paper_anchors.rtl_marker_rows — each anchor must claim its
     own printed marker row (right number, right page, anchor at-or-above the
     row within a 0.10 window), assigned monotonically within each printed-
     number group so subpart order is proven, with no other marker row hiding
     between the crop start and the claimed row (a marker there would mean
     the crop shows the WRONG question) and no unclaimed same-number row
     inside the group's span (a skipped subpart would mean the classic is
     shifted — this catches real off-by-one-row classic bugs);
  4. papers whose text layer yields no usable markers (scanned 2010, damaged
     font cmaps 2011 / 2022 OL / 2023 HL) are DROPPED, not trusted blind;
  5. emits the verified anchors as a hosted paper-only sidecar
     (public/paper-anchors/<year>/<fileid>.json): same pP/pY/label, but
     schemeFileid "", mode pagejump, conf 0.5, paperOnly 1 — exactly the
     paper_anchors.py artifact shape, so test/vaultAnchors.test.ts covers it;
  6. checks the vault topic tags (topic-tags/tags/<subject>.json): every
     tagged n for the sitting must exist in the emitted sidecar.

When task #94 unblocks Storage uploads, the classics go live as answers/
sidecars (richer: crop + reveal) and these hosted copies retire — they carry
IDENTICAL anchors by construction, so the swap is invisible to users.

A wrong crop is worse than none: any verification failure drops the PAPER.

Usage:
  python3 anchors_from_answers.py <subjectId>
      [--years 2010-2025] [--qa-render N] [--seed N] [--dry-run]

Outputs (deterministic, sorted, idempotent):
  public/paper-anchors/<year>/<paperFileid>.json     (committed, hosted)
  scripts/paper-trail/out/anchors-from-answers-<subject>-report.md
  scripts/paper-trail/out/qa-render/<subject>/*.png  (--qa-render only)
"""

import argparse
import json
import os
import random
import re
import sys
from collections import defaultdict

import fitz  # pymupdf

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paper_anchors as pa  # noqa: E402

ANSWERS_DIR = os.path.join(pa.HERE, "answers")
TAGS_DIR = os.path.join(pa.HERE, "topic-tags", "tags")

# Verification windows (fractions of page height).
ABOVE_WINDOW = 0.10   # anchor may start up to this above its marker row
BELOW_TOL = 0.010     # ... or this far below the row top (hand-rounded specs;
                      # the viewer's TOP_PAD 0.008 still shows the full row)
GENEROUS_NOTE = 0.04  # report (not fail) anchors starting this far above

LABEL_K_RE = re.compile(r"Q(\d+)")

# Per-question crop-END clamps (TV-9 endP/endY, applied to the HOSTED artifact
# only). The printed paper is an island layout: each literature question
# (printed Q7/Q8/Q9) opens with its own poem/Quran passage, and Part Two /
# grammar part headers separate the sections — so the LAST question before
# each such boundary would otherwise bleed across a full passage page to the
# next anchor (render-verified: 2025 HL n9's derived crop swallowed Q8's
# entire poem). Clamping those questions at the end of their OWN page is
# complete by construction here: the next printed marker was independently
# verified on a LATER page, so everything below the anchor on its own page is
# the question's own content (or blank). Keys are the printed group numbers
# AFTER which a passage/section boundary follows; only their group-last
# question is clamped, and only when the next anchor sits on a later page.
CLAMP_AFTER_GROUP = {
    "arabic": {6, 7, 8, 9},  # reading→Part Two; Q7/Q8/Q9 passages; →grammar
}


def parse_k(label):
    """Printed question number from a classic label ('Literature · Q7 (أ)'
    → 7). None when the label carries no printed number."""
    m = LABEL_K_RE.search(label or "")
    return int(m.group(1)) if m else None


def shape_check(classic, fileid):
    """Mirror of the committed-sidecar CI contract (test/vaultAnchors.test.ts)
    plus label parseability. Returns a list of failure reasons."""
    fails = []
    qs = classic.get("q") or []
    if classic.get("paperFileid") != fileid:
        fails.append(f"classic paperFileid {classic.get('paperFileid')!r} != {fileid!r}")
    if not qs:
        return fails + ["classic has no questions"]
    for i, q in enumerate(qs):
        if q.get("n") != str(i + 1):
            fails.append(f"q[{i}].n = {q.get('n')!r}, expected {i + 1} (dense sequential)")
        if parse_k(q.get("label")) is None:
            fails.append(f"n{q.get('n')}: label {q.get('label')!r} has no printed Q-number")
    for a, b in zip(qs, qs[1:]):
        if not (b["pP"] > a["pP"] or (b["pP"] == a["pP"] and b["pY"][0] > a["pY"][0])):
            fails.append(f"n{b['n']} not after n{a['n']} in print order")
    for q in qs:
        if pa.paper_region_for(qs, q["n"]) is None:
            fails.append(f"n{q['n']}: paperRegionFor yields no crop (span/order)")
    return fails


def cross_validate(qs, rows):
    """Verify every classic anchor against the printed marker rows.
    Returns (fails, notes, n_verified). Groups anchors by printed number k
    (subparts of one printed question share k) and greedily assigns each
    anchor, in print order, the earliest unclaimed row with k among its
    numeric readings, on the anchor's page, within
    [anchor - BELOW_TOL, anchor + ABOVE_WINDOW] of the row top."""
    fails, notes = [], []
    n_verified = 0
    groups = defaultdict(list)
    for q in qs:
        groups[parse_k(q.get("label"))].append((q["pP"] - 1, q["pY"][0], q["n"]))
    used = set()
    for k in sorted(groups):
        assigned = []
        for cp, cy, n in sorted(groups[k]):
            cand = [i for i, r in enumerate(rows)
                    if i not in used and r[0] == cp and k in r[2]
                    and cy - BELOW_TOL <= r[1] <= cy + ABOVE_WINDOW
                    and (not assigned or (r[0], r[1]) > assigned[-1])]
            if not cand:
                fails.append(f"n{n} (Q{k}): no printed marker row claims this anchor "
                             f"(page {cp + 1}, y={cy})")
                continue
            i = cand[0]
            used.add(i)
            r = rows[i]
            assigned.append((r[0], r[1]))
            # A DIFFERENT marker row between the crop start and the claimed
            # row would put another question's start inside this crop's lead.
            between = [x for x in rows
                       if x[0] == cp and cy + 0.002 <= x[1] < r[1] - 0.002]
            if between:
                fails.append(f"n{n} (Q{k}): marker row(s) between the anchor and its "
                             f"own marker at {[(round(x[1], 3), sorted(x[2])) for x in between]}")
                continue
            n_verified += 1
            if cy < r[1] - GENEROUS_NOTE:
                notes.append(f"n{n} (Q{k}): generous crop start "
                             f"(anchor {cy}, marker row {r[1]:.4f})")
        # An unclaimed same-number row INSIDE the group's assigned span means
        # a subpart row was skipped — the classic anchors are shifted.
        if len(assigned) > 1:
            lo, hi = assigned[0], assigned[-1]
            stray = [r for i, r in enumerate(rows)
                     if i not in used and k in r[2] and lo < (r[0], r[1]) < hi]
            if stray:
                fails.append(f"group Q{k}: unclaimed Q{k} marker row(s) inside the "
                             f"anchored span at {[(r[0] + 1, round(r[1], 3)) for r in stray]} "
                             f"— classic anchors shifted?")
    return fails, notes, n_verified


def make_paper_only(classic):
    """Strip the scheme mapping: same anchors/labels, pagejump-only artifact
    (the paper_anchors.py sidecar shape — CI-checked by vaultAnchors.test.ts)."""
    qout = []
    for q in classic["q"]:
        o = {
            "n": q["n"],
            "pP": q["pP"],
            "pY": [q["pY"][0], q["pY"][1]],
            "region": [{"p": 1}],
            "mode": "pagejump",
            "conf": pa.PAGEJUMP_CONF,
        }
        if q.get("label"):
            o["label"] = q["label"]
        qout.append(o)
    return {
        "v": pa.SIDECAR_V,
        "paperFileid": classic["paperFileid"],
        "schemeFileid": "",
        "component": classic.get("component") or pa.component_of(classic["paperFileid"]),
        "band": [1, 1],
        "copyright": pa.COPYRIGHT,
        "paperOnly": 1,
        "q": qout,
    }


def add_crop_end_clamps(subject, qs, rows):
    """Clamp each boundary group's LAST question at the end of its own page
    (see CLAMP_AFTER_GROUP). Skipped when the next anchor shares the page
    (the derived crop is already tight) or when a marker row for the NEXT
    printed number sits below the anchor on its own page (contradiction —
    leave the derived crop rather than guess). Returns the clamped n's."""
    bset = CLAMP_AFTER_GROUP.get(subject)
    if not bset:
        return []
    by_k = defaultdict(list)
    for i, q in enumerate(qs):
        by_k[parse_k(q.get("label"))].append(i)
    clamped = []
    for k in sorted(by_k):
        if k not in bset:
            continue
        i = by_k[k][-1]
        q = qs[i]
        nxt = qs[i + 1] if i + 1 < len(qs) else None
        if nxt is None or nxt["pP"] <= q["pP"]:
            continue
        page0 = q["pP"] - 1
        if any(r[0] == page0 and r[1] > q["pY"][0] + 0.012 and (k + 1) in r[2]
               for r in rows):
            continue
        q["endP"] = q["pP"]
        q["endY"] = 1.0
        clamped.append(q["n"])
    return clamped


def load_tag_ns(subject):
    """{(year, fileid): [tagged n, ...]} from the vault topic tags."""
    path = os.path.join(TAGS_DIR, f"{subject}.json")
    if not os.path.exists(path):
        return {}
    out = {}
    with open(path, encoding="utf-8") as f:
        for e in json.load(f):
            out[(e["year"], e["fileid"])] = [q["n"] for q in e["q"]]
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    ap.add_argument("subject")
    ap.add_argument("--years", default="2010-2025")
    ap.add_argument("--qa-render", type=int, default=0, metavar="N")
    ap.add_argument("--seed", type=int, default=562)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    y0, y1 = (int(x) for x in args.years.split("-"))
    years = set(range(y0, y1 + 1))
    cycle, rows_idx = pa.load_subject_index(args.subject)
    rows_idx = [r for r in rows_idx if r["year"] in years]
    tag_ns = load_tag_ns(args.subject)
    rng = random.Random(args.seed)

    pa.log(f"anchors-from-answers: {args.subject} ({cycle}) — {len(rows_idx)} papers")
    report, shipped, dropped, skipped = [], 0, 0, 0
    for r in sorted(rows_idx, key=lambda r: (-r["year"], r["level"], r["lang"], r["fileid"])):
        tag = f"{r['year']} {r['level']}/{r['lang']} {r['label']} {r['fileid']}"
        if r["hasAnswers"]:
            skipped += 1
            report.append((tag, "SKIP", "already has a verified Storage sidecar"))
            continue
        classic_path = os.path.join(ANSWERS_DIR, str(r["year"]), f"{r['fileid']}.json")
        if not os.path.exists(classic_path):
            dropped += 1
            report.append((tag, "DROP", "no classic sidecar in answers/"))
            continue
        with open(classic_path, encoding="utf-8") as f:
            classic = json.load(f)

        fails = shape_check(classic, r["fileid"])
        if fails:
            dropped += 1
            report.append((tag, "DROP", "classic fails the CI contract: " + "; ".join(fails)))
            continue

        pdf_path = pa.fetch_paper(cycle, args.subject, r["year"], r["fileid"])
        if not pdf_path:
            dropped += 1
            report.append((tag, "DROP", "download failed"))
            continue
        doc = fitz.open(pdf_path)
        marker_rows = pa.rtl_marker_rows(doc)
        fails, notes, n_verified = cross_validate(classic["q"], marker_rows)
        if n_verified == 0:
            dropped += 1
            report.append((tag, "DROP", "text layer unverifiable (no printed marker "
                          "rows match — scanned or damaged font cmap); refusing to "
                          "ship unverified anchors"))
            continue
        if fails:
            dropped += 1
            report.append((tag, "DROP", f"{n_verified}/{len(classic['q'])} verified; "
                          + "; ".join(fails)))
            continue

        # Vault tags must reference n values the sidecar actually carries.
        tagged = tag_ns.get((r["year"], r["fileid"]))
        have = {q["n"] for q in classic["q"]}
        if tagged and not set(tagged) <= have:
            dropped += 1
            report.append((tag, "DROP", f"topic tags reference n outside the sidecar: "
                          f"{sorted(set(tagged) - have, key=int)}"))
            continue

        sidecar = make_paper_only(classic)
        clamped = add_crop_end_clamps(args.subject, sidecar["q"], marker_rows)
        # Post-clamp CI mirror: every question must still yield a crop.
        broken = [q["n"] for q in sidecar["q"]
                  if pa.paper_region_for(sidecar["q"], q["n"]) is None]
        if broken:
            dropped += 1
            report.append((tag, "DROP", f"clamped sidecar loses crops for n {broken}"))
            continue
        if not args.dry_run:
            ydir = os.path.join(pa.PUBLIC_OUT, str(r["year"]))
            os.makedirs(ydir, exist_ok=True)
            with open(os.path.join(ydir, f"{r['fileid']}.json"), "w", encoding="utf-8") as fh:
                json.dump(sidecar, fh, ensure_ascii=False, sort_keys=True,
                          separators=(",", ":"))
        rendered = []
        if args.qa_render:
            rdir = os.path.join(pa.OUT_DIR, "qa-render", args.subject)
            rendered = pa.qa_render(pdf_path, sidecar, rdir, args.qa_render, rng, r["year"])
        detail = (f"{len(sidecar['q'])}q, all {n_verified} anchors marker-verified"
                  + (f" · tags n⊆sidecar ({len(tagged)} tagged)" if tagged else " · no tags")
                  + (f" · crop-end clamped n {','.join(clamped)}" if clamped else ""))
        for note in notes:
            detail += f" · {note}"
        if rendered:
            detail += f" · {len(rendered)} QA crops"
        shipped += 1
        report.append((tag, "ANCHORED", detail))

    os.makedirs(pa.OUT_DIR, exist_ok=True)
    rep_path = os.path.join(pa.OUT_DIR, f"anchors-from-answers-{args.subject}-report.md")
    with open(rep_path, "w", encoding="utf-8") as f:
        f.write(f"# Hosted anchors from classic sidecars — {args.subject}\n\n")
        f.write(f"**{shipped} anchored · {dropped} dropped · {skipped} skipped** "
                f"of {len(rows_idx)} papers\n\n")
        f.write("| paper | status | detail |\n|---|---|---|\n")
        for t, status, detail in report:
            f.write(f"| {t} | {status} | {detail} |\n")
    pa.log(f"  {shipped} anchored · {dropped} dropped · {skipped} skipped")
    pa.log(f"  → {os.path.relpath(rep_path, pa.REPO)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
