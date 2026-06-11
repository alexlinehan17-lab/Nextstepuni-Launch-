#!/usr/bin/env python3
"""
Paper Trail — Stage 4: upload the corpus to Firebase Storage.

Reads scripts/paper-trail/out/upload-manifest.jsonl (emitted by build-index.py
— the single source of truth for the storage layout, including the load-bearing
{paper|scheme} path segment) and:

 1. Stages the corpus as HARDLINKS into out/stage/{immutable|current}/...
    mirroring the remote layout (no extra disk).
 2. Runs two parallel `gcloud storage cp -r` batches:
      - past years:   Cache-Control: public, max-age=31536000, immutable
      - current year: Cache-Control: public, max-age=86400
    (SEC occasionally re-issues current-year schemes; immutable caching would
    pin a bad copy for a year.)
 3. Verifies the remote object count matches the manifest.

Prereqs: Firebase Storage activated; `gcloud auth login` done;
downloads complete (run build-index.py after download.py so sizes are real).
"""

import json
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
MANIFEST = os.path.join(HERE, "out", "upload-manifest.jsonl")
STAGE = os.path.join(HERE, "out", "stage")
BUCKET = "gs://nextstepuni-app.firebasestorage.app"
GCLOUD = os.path.expanduser("~/google-cloud-sdk/bin/gcloud")
CURRENT_YEAR = 2025  # most recent published exam year


def main():
    rows = [json.loads(l) for l in open(MANIFEST)]
    print(f"manifest: {len(rows)} objects")

    missing = [r for r in rows if not os.path.exists(os.path.join(REPO, r["local"]))]
    if missing:
        print(f"ABORT: {len(missing)} local files missing (downloads incomplete?)")
        for r in missing[:5]:
            print("  e.g.", r["local"])
        return 1

    if os.path.exists(STAGE):
        shutil.rmtree(STAGE)
    staged = {"immutable": 0, "current": 0}
    for r in rows:
        bucket_kind = "current" if r["year"] >= CURRENT_YEAR else "immutable"
        dest = os.path.join(STAGE, bucket_kind, r["remote"])
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        os.link(os.path.join(REPO, r["local"]), dest)
        staged[bucket_kind] += 1
    print(f"staged: {staged['immutable']} immutable, {staged['current']} current-year")

    for bucket_kind, cache in [
        ("immutable", "public, max-age=31536000, immutable"),
        ("current", "public, max-age=86400"),
    ]:
        src = os.path.join(STAGE, bucket_kind, "papers")
        if not os.path.isdir(src):
            continue
        print(f"uploading {bucket_kind} batch…")
        rc = subprocess.run(
            [GCLOUD, "storage", "cp", "-r", "--cache-control", cache,
             "--content-type", "application/pdf", src, f"{BUCKET}/"],
            cwd=REPO,
        ).returncode
        if rc != 0:
            print(f"ABORT: gcloud cp failed for {bucket_kind} batch (rc={rc})")
            return rc

    print("verifying remote object count…")
    out = subprocess.run(
        [GCLOUD, "storage", "ls", "-r", f"{BUCKET}/papers/**"],
        capture_output=True, text=True,
    )
    remote = len([l for l in out.stdout.splitlines() if l.endswith(".pdf")])
    print(f"remote PDFs: {remote} / expected {len(rows)}")
    if remote < len(rows):
        print("WARNING: counts differ — re-run to fill gaps (cp is resumable).")
        return 2
    shutil.rmtree(STAGE)
    print("DONE — corpus live.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
