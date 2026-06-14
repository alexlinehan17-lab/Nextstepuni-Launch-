#!/usr/bin/env python3
"""Coverage wave — attempt EVERY paper-with-scheme profile not already mapped,
across all exams (LC/JC/LB) and EV+IV, levels A/G/C. Precise engine only
(UNIVERSAL_FALLBACK stays False — we never ship an approximate crop). Writes to a
STAGING dir, never to the committed answers/ (so the verified 684 are untouched and
nothing is overwritten). Ships only profiles the engine's reconcile/monotonic/spread
gates accept. Screen + agent-verify staging, then merge the verified subset.

Usage: python3 coverage_wave.py            # all exams, EV+IV
       python3 coverage_wave.py LC EV      # restrict exam / lang
"""
import importlib.util, json, os, sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("am", os.path.join(HERE, "anchor-map.py"))
am = importlib.util.module_from_spec(spec); spec.loader.exec_module(am)
am.UNIVERSAL_FALLBACK = False

STAGING = os.path.join(HERE, "answers_staging")
COMMITTED = am.ANSWERS_DIR

EXAMS = [sys.argv[1]] if len(sys.argv) > 1 else ["LC", "JC", "LB"]
LANGS = {sys.argv[2]} if len(sys.argv) > 2 else {"EV", "IV"}
LEVELS = {"A", "G", "C"}

# every paperFileid already committed — never re-create or overwrite these
committed = set()
for yd in (os.listdir(COMMITTED) if os.path.isdir(COMMITTED) else []):
    d = os.path.join(COMMITTED, yd)
    if os.path.isdir(d):
        for fn in os.listdir(d):
            committed.add(fn[:-5])  # strip .json -> paperFileid.pdf

rows, seen = [], set()
for line in open(am.MANIFEST, encoding="utf-8"):
    line = line.strip()
    if not line:
        continue
    r = json.loads(line); k = (r["view"], r["year"], r["fileid"])
    if k in seen or not r["fileid"].lower().endswith(".pdf"):
        continue
    seen.add(k); rows.append(r)
names = {r["fileid"][:6]: r.get("subjectName", "?") for r in rows}

am.SCOPE_LEVELS = LEVELS
mapped = dropped = skipped = 0
by_map = Counter(); by_drop = Counter()
for exam in EXAMS:
    am.SCOPE_EXAM = exam
    pairs = am.build_pairs(rows, include_done=True, langs=LANGS, levels=LEVELS)
    for prow, srow, strat, level in pairs:
        year = int(prow["year"]); pfile, sfile = prow["fileid"], srow["fileid"]
        if pfile in committed:
            skipped += 1
            continue
        pp = am.corpus_path("exampapers", year, pfile)
        sp = am.corpus_path("markingschemes", year, sfile)
        if not (os.path.exists(pp) and os.path.exists(sp)):
            continue
        try:
            sc, st = am.map_paper(pp, sp, strat)
        except Exception as e:
            dropped += 1; by_drop[f"{names.get(pfile[:6], pfile[:5])} ERR"] += 1
            continue
        crops = sum(1 for q in sc["q"] if q.get("mode") == "crop") if sc else 0
        if sc is None or crops < am.MIN_QUESTIONS or crops < len(sc["q"]) * 0.6:
            dropped += 1; by_drop[names.get(pfile[:6], pfile[:5])] += 1
            continue
        ydir = os.path.join(STAGING, str(year)); os.makedirs(ydir, exist_ok=True)
        json.dump(sc, open(os.path.join(ydir, f"{pfile}.json"), "w"),
                  ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        mapped += 1; by_map[names.get(pfile[:6], pfile[:5])] += 1

print(f"COVERAGE WAVE  exams={EXAMS} langs={sorted(LANGS)}")
print(f"  staged(new)={mapped}  dropped={dropped}  skipped(already committed)={skipped}")
print("  --- newly staged by subject ---")
for s, c in by_map.most_common(60):
    print(f"    +{c:3d}  {s}")
print("  --- dropped by subject (top 30) ---")
for s, c in by_drop.most_common(30):
    print(f"    -{c:3d}  {s}")
