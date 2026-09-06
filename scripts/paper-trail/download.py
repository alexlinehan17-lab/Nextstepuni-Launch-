#!/usr/bin/env python3
"""
Paper Trail — Stage 2: download the enumerated corpus (PDFs only, v1 scope).

Reads scripts/paper-trail/out/manifest.jsonl (from enumerate.py) and mirrors
every .pdf into paper-trail-corpus/{view}/{year}/{fileid}, recording actual
size + sha256 per file in scripts/paper-trail/out/downloads.jsonl.

Non-PDF assets (aural .mp3, .mov video, legacy .tif/.jpg inserts) are skipped
per the approved v1 scope.

Politeness: single-threaded, ~1.6s between requests, exponential backoff on
429/5xx, identifying User-Agent. Resume-safe: existing complete files skipped.
"""

import hashlib
import json
import os
import sys
import time
import urllib.parse
import urllib.request

import certifi
import ssl

SSL_CTX = ssl.create_default_context(cafile=certifi.where())

UA = "NextStepUni-PaperTrail/1.0 (one-time archive mirror; contact: nextstepuniinfo@gmail.com)"
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
MANIFEST = os.path.join(HERE, "out", "manifest.jsonl")
DOWNLOADS = os.path.join(HERE, "out", "downloads.jsonl")
CORPUS = os.path.join(REPO, "paper-trail-corpus")
DELAY = 1.6


def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def fetch(url, dest):
    delay = DELAY
    for attempt in range(8):
        req = urllib.request.Request(url)
        req.add_header("User-Agent", UA)
        try:
            with urllib.request.urlopen(req, timeout=120, context=SSL_CTX) as r:
                data = r.read()
            time.sleep(DELAY)
            if not data.startswith(b"%PDF"):
                return None, f"not-a-pdf ({len(data)} bytes, starts {data[:12]!r})"
            with open(dest, "wb") as f:
                f.write(data)
            return data, None
        except urllib.error.HTTPError as e:
            if e.code == 404:
                time.sleep(DELAY)
                return None, "404"
            if e.code in (429, 500, 502, 503, 504):
                wait = delay * (2 ** attempt)
                log(f"  HTTP {e.code} — backing off {wait:.0f}s")
                time.sleep(wait)
                continue
            raise
        except Exception as e:  # noqa: BLE001
            wait = delay * (2 ** attempt)
            log(f"  {type(e).__name__}: {e} — retrying in {wait:.0f}s")
            time.sleep(wait)
    return None, "gave-up"


def main():
    rows = []
    seen = set()
    with open(MANIFEST) as f:
        for line in f:
            r = json.loads(line)
            key = (r["view"], r["year"], r["fileid"])
            if key in seen:
                continue
            seen.add(key)
            rows.append(r)
    pdfs = [r for r in rows if r["fileid"].lower().endswith(".pdf")]
    skipped = len(rows) - len(pdfs)
    log(f"manifest: {len(rows)} files, {len(pdfs)} PDFs in scope, {skipped} non-PDF skipped")

    done = {}
    if os.path.exists(DOWNLOADS):
        with open(DOWNLOADS) as f:
            for line in f:
                try:
                    d = json.loads(line)
                    done[(d["view"], d["year"], d["fileid"])] = d
                except json.JSONDecodeError:
                    pass
        log(f"resume: {len(done)} already recorded")

    out = open(DOWNLOADS, "a")
    n_ok = n_fail = 0
    total_bytes = sum(d.get("bytes", 0) for d in done.values())
    for i, r in enumerate(pdfs):
        key = (r["view"], r["year"], r["fileid"])
        dest_dir = os.path.join(CORPUS, r["view"], r["year"])
        dest = os.path.join(dest_dir, r["fileid"])
        if (key in done and "error" not in done[key]
                and os.path.exists(dest) and os.path.getsize(dest) > 0):
            continue
        os.makedirs(dest_dir, exist_ok=True)
        # A direct official-archive recovery may have restored a file after a
        # previous urllib attempt was recorded as an error. Accept a valid
        # local PDF and append a successful record so Stage 3 no longer drops
        # it; do not refetch or overwrite the recovered bytes.
        if os.path.exists(dest) and os.path.getsize(dest) > 0:
            with open(dest, "rb") as existing_file:
                existing = existing_file.read()
            if existing.startswith(b"%PDF"):
                rec = dict(r)
                rec["bytes"] = len(existing)
                rec["sha256"] = hashlib.sha256(existing).hexdigest()
                rec["recovered"] = True
                out.write(json.dumps(rec) + "\n")
                out.flush()
                done[key] = rec
                total_bytes += len(existing)
                n_ok += 1
                continue
        url = "https://www.examinations.ie/archive/{}/{}/{}".format(
            r["view"], r["year"], urllib.parse.quote(r["fileid"])
        )
        data, err = fetch(url, dest)
        rec = dict(r)
        if data:
            rec["bytes"] = len(data)
            rec["sha256"] = hashlib.sha256(data).hexdigest()
            total_bytes += len(data)
            n_ok += 1
        else:
            rec["error"] = err
            n_fail += 1
            log(f"  FAIL {r['fileid']}: {err}")
        out.write(json.dumps(rec) + "\n")
        out.flush()
        if (i + 1) % 100 == 0:
            log(
                f"progress {i + 1}/{len(pdfs)} — ok {n_ok}, fail {n_fail}, "
                f"{total_bytes / 1e9:.2f} GB"
            )
    out.close()
    log(f"DONE — ok {n_ok}, fail {n_fail}, corpus {total_bytes / 1e9:.2f} GB")


if __name__ == "__main__":
    sys.exit(main())
