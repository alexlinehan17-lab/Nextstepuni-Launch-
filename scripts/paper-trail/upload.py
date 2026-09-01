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
ANSWERS_MANIFEST = os.path.join(HERE, "out", "answers-upload-manifest.jsonl")
STAGE = os.path.join(HERE, "out", "stage")
BUCKET = "gs://nextstepuni-app.firebasestorage.app"
GCLOUD = os.path.expanduser("~/google-cloud-sdk/bin/gcloud")
CURRENT_YEAR = 2026  # most recent published exam year


def main():
    # Annual refresh: `--year 2026` uploads only that year's objects, so the
    # (gitignored, absent) corpus for other years can't abort the run. The
    # remote-count verification is scoped the same way.
    only_year = None
    if len(sys.argv) == 3 and sys.argv[1] == "--year":
        only_year = int(sys.argv[2])
    rows = [json.loads(l) for l in open(MANIFEST)]
    if only_year is not None:
        rows = [r for r in rows if r["year"] == only_year]
    print(f"manifest: {len(rows)} objects" + (f" (year {only_year})" if only_year else ""))

    missing = [r for r in rows if not os.path.exists(os.path.join(REPO, r["local"]))]
    if missing:
        print(f"ABORT: {len(missing)} local files missing (downloads incomplete?)")
        for r in missing[:5]:
            print("  e.g.", r["local"])
        return 1

    if os.path.exists(STAGE):
        shutil.rmtree(STAGE)
    staged = {"immutable": 0, "current": 0, "immutable-img": 0, "current-img": 0}
    corrupt = []
    for r in rows:
        src = os.path.join(REPO, r["local"])
        is_img = r["remote"].lower().endswith(".jpg")
        with open(src, "rb") as fh:
            head = fh.read(5)
            fh.seek(-64, os.SEEK_END if os.path.getsize(src) > 64 else os.SEEK_SET)
            tail = fh.read()
        # Integrity by format: PDFs carry %PDF-…%%EOF; JPEGs SOI…EOI markers.
        ok = (head[:2] == b"\xff\xd8" and b"\xff\xd9" in tail) if is_img \
            else (head == b"%PDF-" and b"%%EOF" in tail)
        if not ok:
            corrupt.append(r["local"])
            continue
        bucket_kind = "current" if r["year"] >= CURRENT_YEAR else "immutable"
        if is_img:
            bucket_kind += "-img"
        dest = os.path.join(STAGE, bucket_kind, r["remote"])
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        os.link(src, dest)
        staged[bucket_kind] += 1
    if corrupt:
        print(f"ABORT: {len(corrupt)} corrupt/truncated files — re-download before uploading:")
        for c in corrupt[:10]:
            print("  ", c)
        return 1
    print(f"staged: {staged['immutable']} immutable, {staged['current']} current-year, "
          f"{staged['immutable-img']}+{staged['current-img']} images")

    for bucket_kind, cache, ctype in [
        ("immutable", "public, max-age=31536000, immutable", "application/pdf"),
        ("current", "public, max-age=86400", "application/pdf"),
        ("immutable-img", "public, max-age=31536000, immutable", "image/jpeg"),
        ("current-img", "public, max-age=86400", "image/jpeg"),
    ]:
        src = os.path.join(STAGE, bucket_kind, "papers")
        if not os.path.isdir(src):
            continue
        print(f"uploading {bucket_kind} batch…")
        rc = subprocess.run(
            [GCLOUD, "storage", "cp", "-r", "--cache-control", cache,
             "--content-type", ctype, src, f"{BUCKET}/"],
            cwd=REPO,
        ).returncode
        if rc != 0:
            print(f"ABORT: gcloud cp failed for {bucket_kind} batch (rc={rc})")
            return rc

    # Answer-map sidecars (Stage 2.5) — uploaded as application/json, NOT pdf.
    # Coordinates-only JSON; tiny; may be re-generated, so a 1-day cache. Empty
    # manifest (no QA-passed profiles yet) is a clean no-op.
    answer_rows = [json.loads(l) for l in open(ANSWERS_MANIFEST)] if os.path.exists(ANSWERS_MANIFEST) else []
    if only_year is not None:
        answer_rows = [r for r in answer_rows if f"/{only_year}/" in r["remote"]]
    if answer_rows:
        a_missing = [r for r in answer_rows if not os.path.exists(os.path.join(REPO, r["local"]))]
        if a_missing:
            print(f"ABORT: {len(a_missing)} answer sidecars missing (run anchor-map.py + build-index.py)")
            return 1
        a_stage = os.path.join(STAGE, "answers")
        for r in answer_rows:
            dest = os.path.join(a_stage, r["remote"])
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            os.link(os.path.join(REPO, r["local"]), dest)
        print(f"uploading {len(answer_rows)} answer sidecars…")
        rc = subprocess.run(
            [GCLOUD, "storage", "cp", "-r", "--cache-control", "public, max-age=86400",
             "--content-type", "application/json", os.path.join(a_stage, "papers"), f"{BUCKET}/"],
            cwd=REPO,
        ).returncode
        if rc != 0:
            print(f"ABORT: gcloud cp failed for answer sidecars (rc={rc})")
            return rc

    print("verifying remote object count…")
    out = subprocess.run(
        [GCLOUD, "storage", "ls", "-r", f"{BUCKET}/papers/**"],
        capture_output=True, text=True,
    )
    listed = [l for l in out.stdout.splitlines() if l.endswith((".pdf", ".jpg"))]
    if only_year is not None:
        listed = [l for l in listed if f"/{only_year}/" in l]
    remote = len(listed)
    print(f"remote docs: {remote} / expected {len(rows)}")
    if remote < len(rows):
        print("WARNING: counts differ — re-run to fill gaps (cp is resumable).")
        return 2
    shutil.rmtree(STAGE)
    print("DONE — corpus live.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
