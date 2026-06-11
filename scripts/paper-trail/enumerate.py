#!/usr/bin/env python3
"""
Paper Trail — Stage 1: enumerate the SEC Exam Material Archive.

Politely walks the archive's browse form (single stateful POST endpoint) to
produce an authoritative manifest of every exam paper / marking scheme in
scope, with the archive's own human-readable labels.

Scope (per approved plan):
  - exampapers + markingschemes (no deferred materials)
  - LC  2010-2025
  - LCA 2010-2025
  - JC  2017-2025 minus 2020/2021 (cancelled); new-spec filtering happens at
    decode time, not here — the manifest stays complete for audit.

Politeness: single-threaded, ~1.6s between requests, exponential backoff on
HTTP 429/5xx, identifying User-Agent with contact address. One-time run.

Output: scripts/paper-trail/out/manifest.jsonl  (one JSON object per file)
        scripts/paper-trail/out/subjects.json   (per year x exam subject lists)

Resume-safe: combos already present in manifest.jsonl are skipped on re-run.
"""

import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

import certifi
import ssl

SSL_CTX = ssl.create_default_context(cafile=certifi.where())

BASE = "https://www.examinations.ie/exammaterialarchive/index.php"
UA = "NextStepUni-PaperTrail/1.0 (one-time archive mirror; contact: nextstepuniinfo@gmail.com)"
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
MANIFEST = os.path.join(OUT_DIR, "manifest.jsonl")
SUBJECTS = os.path.join(OUT_DIR, "subjects.json")
DELAY = 1.6

VIEWS = ["exampapers", "markingschemes"]
YEARS = {
    "lc": [str(y) for y in range(2010, 2026)],
    "lb": [str(y) for y in range(2010, 2026)],
    "jc": ["2017", "2018", "2019", "2022", "2023", "2024", "2025"],
}

F = "MaterialArchive__noTable__"


def fields(view=None, year=None, exam=None, subject=None):
    d = {F + "cbv__AgreeCheck": "Y", F + "cbh__AgreeCheck": "N"}
    if view:
        d[F + "sbv__ViewType"] = view
        d[F + "sbh__ViewType"] = "id"
    if year:
        d[F + "sbv__YearSelect"] = year
        d[F + "sbh__YearSelect"] = "id"
    if exam:
        d[F + "sbv__ExaminationSelect"] = exam
        d[F + "sbh__ExaminationSelect"] = "id"
    if subject:
        d[F + "sbv__SubjectSelect"] = subject
        d[F + "sbh__SubjectSelect"] = "id"
    return d


_cookie = {"v": ""}


def post(data):
    body = urllib.parse.urlencode(data).encode()
    delay = DELAY
    for attempt in range(8):
        req = urllib.request.Request(BASE, data=body, method="POST")
        req.add_header("User-Agent", UA)
        req.add_header("Content-Type", "application/x-www-form-urlencoded")
        if _cookie["v"]:
            req.add_header("Cookie", _cookie["v"])
        try:
            with urllib.request.urlopen(req, timeout=60, context=SSL_CTX) as r:
                setc = r.headers.get("Set-Cookie")
                if setc:
                    _cookie["v"] = setc.split(";")[0]
                html = r.read().decode("utf-8", "replace")
            time.sleep(DELAY)
            return html
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504):
                wait = delay * (2 ** attempt)
                log(f"  HTTP {e.code} — backing off {wait:.0f}s")
                time.sleep(wait)
                continue
            raise
        except Exception as e:  # noqa: BLE001 — network blips: retry
            wait = delay * (2 ** attempt)
            log(f"  {type(e).__name__}: {e} — retrying in {wait:.0f}s")
            time.sleep(wait)
    raise RuntimeError("giving up after 8 attempts")


def parse_subjects(html):
    m = re.search(r'<select name="%ssbv__SubjectSelect".*?</select>' % F, html, re.S)
    if not m:
        return []
    return [
        (sid, name.strip())
        for sid, name in re.findall(r'<option[^>]*value="(\d+)"[^>]*>([^<]*)', m.group(0))
    ]


def parse_files(html):
    """Return [(fileid, label, size_hint)] from the listing tables."""
    rows = []
    for m in re.finditer(
        r"name='fileid' value='([^']+)'>.*?<TD class='materialbody'>([^<]*)</TD>.*?"
        r"(?:\[([0-9.]+\s*[KM]B)\])?",
        html,
        re.S,
    ):
        rows.append((m.group(1).strip(), m.group(2).strip(), (m.group(3) or "").strip()))
    return rows


def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    done = set()
    if os.path.exists(MANIFEST):
        with open(MANIFEST) as f:
            for line in f:
                try:
                    r = json.loads(line)
                    done.add((r["view"], r["year"], r["exam"], r["subjectId"]))
                except json.JSONDecodeError:
                    pass
        log(f"resume: {len(done)} subject-combos already enumerated")

    subjects_index = {}
    if os.path.exists(SUBJECTS):
        with open(SUBJECTS) as f:
            subjects_index = json.load(f)

    out = open(MANIFEST, "a")
    total_files = 0
    for view in VIEWS:
        for exam, years in YEARS.items():
            for year in years:
                key = f"{view}|{exam}|{year}"
                if key in subjects_index:
                    subs = subjects_index[key]
                else:
                    html = post(fields(view, year, exam))
                    subs = parse_subjects(html)
                    subjects_index[key] = subs
                    with open(SUBJECTS, "w") as f:
                        json.dump(subjects_index, f, indent=1)
                log(f"{view} {exam} {year}: {len(subs)} subjects")
                for sid, sname in subs:
                    if (view, year, exam, sid) in done:
                        continue
                    html = post(fields(view, year, exam, sid))
                    files = parse_files(html)
                    for fileid, label, size_hint in files:
                        out.write(
                            json.dumps(
                                {
                                    "view": view,
                                    "exam": exam,
                                    "year": year,
                                    "subjectId": sid,
                                    "subjectName": sname,
                                    "fileid": fileid,
                                    "label": label,
                                    "sizeHint": size_hint,
                                }
                            )
                            + "\n"
                        )
                    out.flush()
                    total_files += len(files)
                    log(f"  {sname}: {len(files)} files (running total {total_files})")
    out.close()
    log(f"DONE — {total_files} new file rows")


if __name__ == "__main__":
    sys.exit(main())
