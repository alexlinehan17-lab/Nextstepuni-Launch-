#!/usr/bin/env python3
"""
Paper Trail — official SEC sample papers for new specifications.

The Exam Material Archive only holds papers that have been sat. Sample papers
for a specification not yet examined (2025 Tranche 1: Climate Action and
Sustainable Development; Drama, Film and Theatre Studies; and the revised
Biology, Chemistry, Physics, Business, Arabic, Latin and Ancient Greek —
first examined in 2027) live on the SEC's Senior Cycle Redevelopment pages
(https://www.examinations.ie/scr/, one fragment per subject code, e.g.
scr/571.php). sample-papers.json is the curated, committed list (one row per
subject/level/language/document, with the source page); this script mirrors
each unique file into paper-trail-corpus/samplepapers/<year>/<fileid> and
records bytes + sha256 in out/sample-downloads.jsonl for build-index.py.

Same politeness as download.py (single thread, ~1.6 s delay, backoff,
identifying User-Agent); resume-safe.
"""

import hashlib
import importlib.util
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
# download.py's fetch (politeness, backoff, PDF check) is reused as-is.
_spec = importlib.util.spec_from_file_location("pt_download", os.path.join(HERE, "download.py"))
dl = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(dl)

SAMPLES = os.path.join(HERE, "sample-papers.json")
OUT = os.path.join(HERE, "out", "sample-downloads.jsonl")
VIEW = "samplepapers"


def main():
    rows = json.load(open(SAMPLES, encoding="utf-8"))
    done = {}
    if os.path.exists(OUT):
        for line in open(OUT):
            d = json.loads(line)
            done[(d["year"], d["fileid"])] = d
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    out = open(OUT, "a")
    seen = set()
    ok = fail = 0
    for r in rows:
        key = (str(r["year"]), r["fileid"])
        if key in seen:
            continue
        seen.add(key)
        dest_dir = os.path.join(dl.CORPUS, VIEW, str(r["year"]))
        dest = os.path.join(dest_dir, r["fileid"])
        if key in done and "error" not in done[key] and os.path.exists(dest):
            continue
        os.makedirs(dest_dir, exist_ok=True)
        data, err = dl.fetch(r["url"], dest)
        rec = {"view": VIEW, "year": str(r["year"]), "fileid": r["fileid"], "url": r["url"]}
        if data:
            rec.update(bytes=len(data), sha256=hashlib.sha256(data).hexdigest())
            ok += 1
        else:
            rec["error"] = err
            fail += 1
            dl.log(f"  FAIL {r['fileid']}: {err}")
        out.write(json.dumps(rec) + "\n")
        out.flush()
    dl.log(f"DONE — ok {ok}, fail {fail}")
    return 1 if fail else 0


if __name__ == "__main__":
    sys.exit(main())
