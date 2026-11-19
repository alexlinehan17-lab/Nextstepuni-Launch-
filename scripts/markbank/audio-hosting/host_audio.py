#!/usr/bin/env python3
"""
Host verified copies of the SEC's listening recordings in the app's own
Firebase Storage bucket, so listening cards can play them.

Why: the SEC lets its mp3s play on its own pages but blocks them when another
site embeds them, and scripted requests get a Cloudflare 403. Alex approved
(19 Nov 2026) keeping a verified copy of each recording in Storage, credited to
the SEC, and playing it from there. The card keeps the SEC's own address
(`canonicalUrl`) and file id (`secFileid`); `components/MarkBank/audioStorage.ts`
maps that address to the hosted copy.

The recordings are fetched in a real Chrome tab on www.examinations.ie (one
request every ten seconds, stopping at the first non-200). The tab hashes each
response, saves it to ~/Downloads as `audiohost-[deferred-]<year>-<fileid>`,
and finally saves its own log of what the server sent (status, headers, bytes,
sha256) as `audiohost-log-<batch>.json`. This script then:

  adopt --map <map.json>    takes a copy already on this Mac from another lane's
                            earlier SEC fetch, only when its sha256 equals the
                            fingerprint that lane recorded (never deletes it).
  verify --log <log.json>   checks every saved file against that log (bytes,
                            sha256), against an earlier independent verification
                            where one exists, and that it decodes as MPEG audio
                            (macOS afinfo: file type, duration, bit rate); then
                            records it in audio-manifest.json.
  upload                    uploads each verified file with the Paper Trail
                            conventions (scripts/paper-trail/upload.py): one
                            year's cache for past years, a day for the current
                            year; audio/mpeg; reads the object back from the
                            bucket (size and MD5 must match) and only then
                            deletes the local copy.

Storage layout mirrors Paper Trail: `audio/<year>/<secFileid>` for June
sittings. The SEC reuses the June file id for a deferred sitting's recording in
the same year (e.g. 2022 LC001ZLP017IV.mp3), so a deferred recording is stored
as `audio/<year>/<stem>-deferred.mp3`, the same rule build-index.py uses for
deferred papers.
"""

import base64
import hashlib
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
MANIFEST = os.path.join(HERE, "audio-manifest.json")
DOWNLOADS = os.path.expanduser("~/Downloads")
BUCKET = "gs://nextstepuni-app.firebasestorage.app"
GCLOUD = os.path.expanduser("~/google-cloud-sdk/bin/gcloud")
CURRENT_YEAR = 2026  # as scripts/paper-trail/upload.py
LANES = "/Users/alexlinehan/Documents/NextStepUni-MarkBank-Lanes-20261104"
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
# Fingerprints recorded when each recording was first fetched from the SEC by
# another lane: every one that exists for a recording must agree with the copy.
PRIOR_BY_YEAR = [  # {year: {url, sha256}}
    os.path.join(LANES, "languages/audio/audio-verify.json"),
    os.path.join(LANES, "languages/audio/german-audio-verify.json"),
]
PRIOR_SOURCES = [  # [{source: {canonicalUrl}, verification: {sha256}}]
    os.path.join(REPO, "data/frenchAudio.json"),
    os.path.join(REPO, "data/germanAudio.json"),
    os.path.join(REPO, "data/spanishAudio.json"),
    "/Users/alexlinehan/Documents/Nextstepuni-Classics-Lane-20261118/data/italianAudio.json",
]
PRIOR_RECORDS = [  # [{canonicalUrl, sha256}]
    os.path.join(LANES, "codex-continuation-20261106/audio-discovery/japanese-recordings.json"),
    os.path.join(LANES, "codex-continuation-20261106/audio-discovery/russian-recordings.json"),
]
SEC_AUDIO = re.compile(
    r"^https://www\.examinations\.ie/archive/(exampapers|deferredexams)/(\d{4})/([A-Za-z0-9]+\.mp3)$")


def storage_path(url):
    """The Storage object path for an SEC recording address (mirrors audioStorage.ts)."""
    m = SEC_AUDIO.match(url)
    if not m:
        raise ValueError(f"not an SEC archive recording: {url}")
    view, year, fileid = m.groups()
    name = re.sub(r"\.mp3$", "-deferred.mp3", fileid, flags=re.I) if view == "deferredexams" else fileid
    return f"audio/{year}/{name}"


def download_name(url):
    view, year, fileid = SEC_AUDIO.match(url).groups()
    return f"audiohost-{'deferred-' if view == 'deferredexams' else ''}{year}-{fileid}"


def load_manifest():
    return json.load(open(MANIFEST)) if os.path.exists(MANIFEST) else {}


def save_manifest(m):
    with open(MANIFEST, "w") as fh:
        json.dump(dict(sorted(m.items())), fh, indent=1, sort_keys=True, ensure_ascii=False)
        fh.write("\n")


def gcloud(*args, capture=True):
    env = dict(os.environ, CLOUDSDK_PYTHON=os.path.expanduser("~/py312/bin/python3"))
    return subprocess.run([GCLOUD, *args], capture_output=capture, text=True, env=env)


def afinfo(path):
    out = subprocess.run(["afinfo", path], capture_output=True, text=True).stdout
    get = lambda pat: (re.search(pat, out, re.M) or [None, None])[1]
    return {
        "fileType": get(r"^File type ID:\s+(\S+)"),
        "durationSeconds": float(get(r"^estimated duration:\s+([\d.]+) sec") or 0),
        "bitRate": int(get(r"^bit rate:\s+(\d+) bits per second") or 0),
        "format": (get(r"^Data format:\s+(.+)$") or "").strip(),
    }


def digest(path):
    sha, md5, n = hashlib.sha256(), hashlib.md5(), 0
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            sha.update(chunk); md5.update(chunk); n += len(chunk)
    return n, sha.hexdigest(), base64.b64encode(md5.digest()).decode()


def prior_refs():
    """{url: [(where, sha256)]} from every earlier fingerprint on this Mac."""
    refs = {}
    def add(url, sha, f):
        if url and sha:
            where = os.path.relpath(f, REPO) if f.startswith(REPO) else f.replace(os.path.expanduser("~/"), "~/")
            refs.setdefault(url, []).append((where, sha))
    for f in PRIOR_BY_YEAR:
        if os.path.exists(f):
            for v in json.load(open(f)).values():
                add(v["url"], v["sha256"], f)
    for f in PRIOR_SOURCES:
        if os.path.exists(f):
            for v in json.load(open(f)):
                add(v["source"]["canonicalUrl"], (v.get("verification") or {}).get("sha256"), f)
    for f in PRIOR_RECORDS:
        if os.path.exists(f):
            for v in json.load(open(f)):
                add(v.get("canonicalUrl"), v.get("sha256"), f)
    return refs


def check_file(local, url, target):
    """Problems with a local copy of an SEC recording (empty when it is good)."""
    problems = []
    n, sha, md5 = digest(local)
    info = afinfo(local)
    with open(local, "rb") as fh:
        head = fh.read(3)
    fileid = SEC_AUDIO.match(url).group(3)
    if fileid != target["fileid"]:
        problems.append(f"file id {fileid} != card file id {target['fileid']}")
    if not (head == b"ID3" or (head[0] == 0xFF and head[1] & 0xE0 == 0xE0)):
        problems.append(f"not an MPEG audio header: {head!r}")
    if info["fileType"] != "MPG3" or info["durationSeconds"] < 60:
        problems.append(f"afinfo: {info}")
    return problems, n, sha, md5, info


def entry(url, target, n, sha, md5, info, source, priors, local):
    view, year, fileid = SEC_AUDIO.match(url).groups()
    return {
        "path": storage_path(url),
        "secFileid": fileid,
        "canonicalUrl": url,
        "year": int(year),
        "sitting": "deferred" if view == "deferredexams" else "june",
        "subjects": target["subjects"],
        "bytes": n,
        "sha256": sha,
        "md5": md5,
        **info,
        "source": source,
        **({"priorVerification": sorted({w for w, _ in priors})} if priors else {}),
        "local": local,
    }


def report(failures):
    if failures:
        print(f"\nFAILED {len(failures)}:")
        for f in failures:
            print("  " + f)
        return 1
    return 0


def verify(log_path, targets_path):
    """Files fetched now in the Chrome tab, checked against the tab's own log."""
    log = json.load(open(log_path))
    targets = {t["url"]: t for t in json.load(open(targets_path))}
    refs = prior_refs()
    man = load_manifest()
    failures = []
    for rec in log:
        url = rec["url"]
        if rec.get("status") != 200:
            failures.append(f"{url}: browser status {rec.get('status')}")
            continue
        t = targets.get(url)
        if not t:
            failures.append(f"{url}: not in the target list")
            continue
        path = storage_path(url)
        if man.get(path, {}).get("storage"):
            print(f"skip (already uploaded) {path}")
            continue
        local = os.path.join(DOWNLOADS, download_name(url))
        if not os.path.exists(local):
            failures.append(f"{url}: saved file missing ({local})")
            continue
        problems, n, sha, md5, info = check_file(local, url, t)
        if n != rec["bytes"]:
            problems.append(f"bytes on disk {n} != bytes received {rec['bytes']}")
        if rec.get("contentLength") and int(rec["contentLength"]) != n:
            problems.append(f"bytes {n} != Content-Length {rec['contentLength']}")
        if sha != rec["sha256"]:
            problems.append("sha256 on disk != sha256 of the bytes received")
        if (rec.get("contentType") or "").split(";")[0].strip() != "audio/mpeg":
            problems.append(f"SEC content type {rec.get('contentType')}")
        priors = refs.get(url, [])
        problems += [f"sha256 differs from the earlier fingerprint in {w}" for w, h in priors if h != sha]
        if problems:
            failures.append(f"{url}: " + "; ".join(problems))
            continue
        source = {
            "fetchedAt": rec["fetchedAt"],
            "via": "Chrome tab on www.examinations.ie",
            "status": rec["status"],
            "contentType": rec.get("contentType"),
            "contentLength": int(rec["contentLength"]) if rec.get("contentLength") else None,
            "lastModified": rec.get("lastModified"),
            "etag": rec.get("etag"),
            **({"note": rec["note"]} if rec.get("note") else {}),
        }
        man[path] = entry(url, t, n, sha, md5, info, source, priors, local)
        print(f"verified {path}  {n} bytes  {info['durationSeconds']:.1f} s"
              + (f"  (matches {len(priors)} earlier fingerprint(s))" if priors else ""))
    save_manifest(man)
    return report(failures)


def adopt(map_path, targets_path):
    """Copies already on this Mac from an earlier SEC fetch by another lane.

    Accepted only when the copy's sha256 equals the fingerprint that lane
    recorded from the SEC at the time, and every other fingerprint agrees. The
    file stays where it is (it is that lane's); upload never deletes it."""
    mapping = json.load(open(map_path))  # {url: local path}
    targets = {t["url"]: t for t in json.load(open(targets_path))}
    refs = prior_refs()
    man = load_manifest()
    failures = []
    for url, local in sorted(mapping.items()):
        t = targets.get(url)
        if not t:
            continue  # not in this target list
        path = storage_path(url)
        if man.get(path, {}).get("storage"):
            print(f"skip (already uploaded) {path}")
            continue
        problems, n, sha, md5, info = check_file(local, url, t)
        priors = refs.get(url, [])
        if not priors:
            problems.append("no earlier SEC fingerprint to match")
        problems += [f"sha256 differs from the earlier fingerprint in {w}" for w, h in priors if h != sha]
        if problems:
            failures.append(f"{url}: " + "; ".join(problems))
            continue
        source = {
            "via": "copy already on this Mac from an earlier fetch of the SEC archive; sha256 matched that fetch's fingerprint",
            "localCopy": local.replace(os.path.expanduser("~/"), "~/"),
        }
        man[path] = entry(url, t, n, sha, md5, info, source, priors, local)
        print(f"adopted {path}  {n} bytes  {info['durationSeconds']:.1f} s  (matches {len(priors)} fingerprint(s))")
    save_manifest(man)
    return report(failures)


def upload():
    man = load_manifest()
    todo = [e for e in man.values() if not e.get("storage") and e.get("local")]
    print(f"to upload: {len(todo)}")
    failures = []
    for e in todo:
        local = e["local"]
        if not os.path.exists(local):
            failures.append(f"{e['path']}: local file missing")
            continue
        n, sha, md5 = digest(local)
        if (n, sha) != (e["bytes"], e["sha256"]):
            failures.append(f"{e['path']}: local file changed since verify")
            continue
        cache = ("public, max-age=86400" if e["year"] >= CURRENT_YEAR
                 else "public, max-age=31536000, immutable")
        dest = f"{BUCKET}/{e['path']}"
        meta = ",".join([
            "source=State Examinations Commission",
            f"secUrl={e['canonicalUrl']}",
            f"secFileid={e['secFileid']}",
            f"sha256={e['sha256']}",
        ])
        r = gcloud("storage", "cp", "--content-type", "audio/mpeg", "--cache-control", cache,
                   f"--custom-metadata={meta}", local, dest)
        if r.returncode != 0:
            failures.append(f"{e['path']}: gcloud cp failed: {r.stderr.strip()[-300:]}")
            continue
        d = gcloud("storage", "objects", "describe", dest, "--format=json")
        if d.returncode != 0:
            failures.append(f"{e['path']}: describe failed: {d.stderr.strip()[-300:]}")
            continue
        o = json.loads(d.stdout)
        got = {
            "object": dest,
            "size": int(o.get("size")),
            "md5Hash": o.get("md5_hash"),
            "crc32c": o.get("crc32c_hash"),
            "contentType": o.get("content_type"),
            "cacheControl": o.get("cache_control"),
            "generation": str(o.get("generation")),
            "sha256Metadata": (o.get("custom_fields") or {}).get("sha256"),
            "uploadedAt": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        }
        bad = []
        if got["size"] != e["bytes"]:
            bad.append(f"size {got['size']} != {e['bytes']}")
        if got["md5Hash"] != e["md5"]:
            bad.append(f"md5 {got['md5Hash']} != {e['md5']}")
        if got["contentType"] != "audio/mpeg":
            bad.append(f"content type {got['contentType']}")
        if got["cacheControl"] != cache:
            bad.append(f"cache control {got['cacheControl']}")
        if got["sha256Metadata"] != e["sha256"]:
            bad.append("sha256 metadata missing or different")
        if bad:
            failures.append(f"{e['path']}: " + "; ".join(bad))
            continue
        e["storage"] = got
        del e["local"]
        ours = (os.path.dirname(local) == DOWNLOADS
                and os.path.basename(local).startswith("audiohost-"))
        if ours:
            os.remove(local)  # another lane's copy is never ours to delete
        save_manifest(man)
        print(f"uploaded {e['path']}  {got['size']} bytes  md5 ok"
              + ("  (local copy deleted)" if ours else "  (another lane's copy left in place)"))
    save_manifest(man)
    return report(failures)


def main(argv):
    if len(argv) >= 2 and argv[1] == "verify":
        return verify(argv[argv.index("--log") + 1], argv[argv.index("--targets") + 1])
    if len(argv) >= 2 and argv[1] == "adopt":
        return adopt(argv[argv.index("--map") + 1], argv[argv.index("--targets") + 1])
    if len(argv) >= 2 and argv[1] == "upload":
        return upload()
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
