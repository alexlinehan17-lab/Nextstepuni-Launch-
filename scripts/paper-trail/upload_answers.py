#!/usr/bin/env python3
"""Upload answer sidecars to Firebase Storage. Reads a TSV of `localPath\\tremotePath`
(one per line) and uploads each to gs://nextstepuni-app.firebasestorage.app/<remote>
with JSON content-type + 1-day cache. Parallel, idempotent (overwrites with the
current verified version). Prints a final present/total check.

Usage: python3 upload_answers.py <tsv_file>
"""
import os, sys, subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed

GCLOUD = os.path.expanduser("~/google-cloud-sdk/bin/gcloud")
BUCKET = "gs://nextstepuni-app.firebasestorage.app"


def upload(loc, rem):
    r = subprocess.run(
        [GCLOUD, "storage", "cp", "--quiet",
         "--cache-control", "public, max-age=86400",
         "--content-type", "application/json",
         loc, f"{BUCKET}/{rem}"],
        capture_output=True, text=True)
    return rem, r.returncode, (r.stderr or "").strip()


def main():
    rows = []
    for line in open(sys.argv[1]):
        line = line.rstrip("\n")
        if not line:
            continue
        loc, rem = line.split("\t")
        rows.append((loc, rem))
    ok = err = 0
    errors = []
    with ThreadPoolExecutor(max_workers=12) as ex:
        futs = [ex.submit(upload, loc, rem) for loc, rem in rows]
        for f in as_completed(futs):
            rem, rc, msg = f.result()
            if rc == 0:
                ok += 1
            else:
                err += 1
                errors.append(f"{rem}: {msg[:120]}")
    print(f"uploaded ok={ok} err={err} / {len(rows)}")
    for e in errors[:15]:
        print("  ERR", e)


if __name__ == "__main__":
    main()
