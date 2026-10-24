#!/usr/bin/env python3
"""
Paper Trail — cover audit: does each document say what the index says?

Reads page 1 of every document in an upload manifest (PyMuPDF text layer; for
scanned PDFs, macOS Vision OCR of the top half of page 1 via ocr/ocr.swift,
compiled into out/ on first use) and checks it against the index: level, paper
vs marking scheme, year, and Paper One/Two. Pre-2010 archive labels come from a
subject-blind component table and some Higher/Ordinary documents are swapped,
so run this over any scope extension before shipping; verified corrections go
in archive-row-fixes.json with their cover evidence.

usage: python3 cover_audit.py <upload-manifest subset.jsonl> <out.tsv>
  (run from the repo root's scripts/paper-trail; prints the flagged rows)
"""
import json
import os
import re
import subprocess
import sys
import tempfile

import fitz

HERE = os.path.dirname(os.path.abspath(__file__))
WT = os.path.dirname(os.path.dirname(HERE))
NEW, OUT = sys.argv[1:3]
OCR = os.path.join(HERE, "out", "ocr")
if not os.path.exists(OCR):
    subprocess.run(["swiftc", "-O", os.path.join(HERE, "ocr", "ocr.swift"), "-o", OCR], check=True)

# index metadata by remote path
idx_src = open(os.path.join(WT, "paperTrailData.ts"), encoding="utf-8").read()
meta = {}
cur = None
cycle_of = {}
for m in re.finditer(r'\{"id": "([^"]+)", "name": "[^"]*", "cycle": "(\w+)"', idx_src):
    cycle_of[m.group(1)] = m.group(2)
body = idx_src[idx_src.index("export const PAPER_TRAIL_INDEX"):]
for line in body.splitlines():
    m = re.match(r'^  "([^"]+)": \[$', line)
    if m:
        cur = m.group(1)
        continue
    if line.startswith('    {"year"'):
        e = json.loads(line.strip().rstrip(","))
        for p in e["papers"]:
            for kind, doc in (("paper", p["doc"]), ("scheme", p.get("scheme"))):
                if not doc:
                    continue
                remote = f"papers/{cycle_of[cur]}/{cur}/{e['year']}/{kind}/{doc['f']}"
                meta.setdefault(remote, []).append(
                    dict(subject=cur, year=e["year"], level=e["level"], lang=e["lang"],
                         sitting=e.get("sitting", "main"), label=p["label"], kind=kind))

LEVELS = [
    ("higher", r"higher\s*level|ard-?leibh[eé]al|ardleibh"),
    ("ordinary", r"ordinary\s*level|gn[aá]th-?leibh[eé]al|gnathleibh"),
    ("foundation", r"foundation\s*level|bonn-?leibh[eé]al|bonnleibh"),
    ("common", r"common\s*level|comhleibh[eé]al"),
]
SCHEME = r"marking\s*scheme|sc[eé]im\s*mharc[aá]la|marking\s*scheme"


def cover_text(path):
    if path.lower().endswith(".jpg"):
        return "", "image"
    try:
        d = fitz.open(path)
    except Exception as e:  # noqa: BLE001
        return f"ERR {e}", "err"
    text = d[0].get_text() if d.page_count else ""
    if len(re.sub(r"\s", "", text)) >= 60:
        # first two pages: some covers carry only the crest + year
        if d.page_count > 1 and len(text) < 400:
            text += " " + d[1].get_text()
        return re.sub(r"\s+", " ", text), "text"
    page = d[0]
    r = page.rect
    clip = fitz.Rect(r.x0, r.y0, r.x1, r.y0 + r.height * 0.5)
    tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
    page.get_pixmap(matrix=fitz.Matrix(1.6, 1.6), clip=clip).save(tmp.name)
    return tmp.name, "ocr"


rows = [json.loads(l) for l in open(NEW)]
results = []
pending_ocr = {}
for r in rows:
    path = os.path.join(WT, r["local"])
    text, how = cover_text(path)
    if how == "ocr":
        pending_ocr[text] = r
        results.append([r, None, how])
    else:
        results.append([r, text, how])

if pending_ocr:
    out = subprocess.run([OCR], input="\n".join(pending_ocr) + "\n", capture_output=True, text=True).stdout
    ocr_text = {}
    for line in out.splitlines():
        p, _, t = line.partition("\t")
        ocr_text[p] = t
    for res in results:
        if res[2] == "ocr":
            png = next(k for k, v in pending_ocr.items() if v is res[0])
            res[1] = ocr_text.get(png, "")
            os.unlink(png)

mismatches = []
with open(OUT, "w") as f:
    f.write("remote\thow\tindex_level\tdetected_levels\tindex_kind\tlooks_scheme\tlabel\tcover\n")
    for r, text, how in results:
        ms = meta.get(r["remote"], [])
        low = (text or "").lower()
        detected = [lv for lv, pat in LEVELS if re.search(pat, low)]
        looks_scheme = bool(re.search(SCHEME, low))
        years = set(re.findall(r"\b(19[89]\d|20[0-2]\d)\b", low))
        for m in ms:
            f.write("\t".join([r["remote"], how, m["level"], ",".join(detected), m["kind"],
                               str(looks_scheme), m["label"], (text or "")[:900].replace("\t", " ")]) + "\n")
            problems = []
            if how in ("text", "ocr"):
                if detected and m["level"] not in detected and m["level"] != "common":
                    problems.append(f"level {m['level']} vs cover {detected}")
                if m["kind"] == "paper" and looks_scheme:
                    problems.append("paper whose cover says marking scheme")
                if m["kind"] == "scheme" and not looks_scheme and m["sitting"] != "sample":
                    problems.append("scheme without 'marking scheme' on cover")
                if m["sitting"] != "sample" and years and str(m["year"]) not in years:
                    problems.append(f"year {m['year']} vs cover {sorted(years)}")
                if not low.strip():
                    problems.append("no cover text")
                if m["kind"] == "paper" and m["sitting"] == "main":
                    p1 = re.search(r"\bpaper\s*(1|i|one)\b(?!i)|p[aá]ip[eé]ar\s*(1|i)\b(?!i)", low)
                    p2 = re.search(r"\bpaper\s*(2|ii|two)\b|p[aá]ip[eé]ar\s*(2|ii)\b", low)
                    if re.search(r"\bpaper one\b", m["label"], re.I) and p2 and not p1:
                        problems.append("label Paper One, cover Paper 2")
                    if re.search(r"\bpaper two\b", m["label"], re.I) and p1 and not p2:
                        problems.append("label Paper Two, cover Paper 1")
            if problems:
                mismatches.append((r["remote"], m["label"], how, problems, (text or "")[:160]))
print(f"audited {len(results)} docs; {sum(1 for r in results if r[2]=='ocr')} OCR; {len(mismatches)} flagged")
for mm in mismatches:
    print("\t".join([mm[0], mm[1], mm[2], "; ".join(mm[3]), mm[4]]))
