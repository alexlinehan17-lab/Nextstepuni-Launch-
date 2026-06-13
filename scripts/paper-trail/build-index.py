#!/usr/bin/env python3
"""
Paper Trail — Stage 3: build the typed index from the harvest outputs.

Consumes:
  scripts/paper-trail/out/manifest.jsonl   (Stage 1 — enumerate.py)
  scripts/paper-trail/out/downloads.jsonl  (Stage 2 — download.py; optional/partial)
  scripts/paper-trail/out/subjects.json    (Stage 1 — per year x exam subject lists)
  curriculum.ts                            (CURRICULUM — for curriculumId linking)

Produces:
  paperTrailData.ts                        (repo root — typed registry + index + gaps)
  scripts/paper-trail/out/index-report.md  (human-readable build report)

Deterministic (sorted keys/arrays, no timestamps), stdlib only, idempotent.
Safe to run mid-crawl: it indexes whatever rows exist and the report flags the
partial coverage; re-run on the full data for the final artefacts.
"""

import html
import json
import os
import re
import sys
import unicodedata
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
OUT_DIR = os.path.join(HERE, "out")
MANIFEST = os.path.join(OUT_DIR, "manifest.jsonl")
DOWNLOADS = os.path.join(OUT_DIR, "downloads.jsonl")
SUBJECTS_JSON = os.path.join(OUT_DIR, "subjects.json")
CURRICULUM_TS = os.path.join(REPO, "curriculum.ts")
TYPES_TS = os.path.join(REPO, "types", "paperTrail.ts")  # generator<->UI contract
DATA_TS = os.path.join(REPO, "paperTrailData.ts")
REPORT_MD = os.path.join(OUT_DIR, "index-report.md")

# ─── Scope / decode constants ────────────────────────────────────────────────

CYCLE_OF_EXAM = {"lc": "lc", "jc": "jc", "lb": "lca"}
CYCLE_RANK = {"lc": 0, "jc": 1, "lca": 2}
CYCLE_PREFIX = {"lc": "", "jc": "jc-", "lca": "lca-"}

LC_YEAR_MIN, LC_YEAR_MAX = 2010, 2025  # also LCA
JC_YEAR_MAX = 2025
JC_CANCELLED_YEARS = (2020, 2021)
JC_CANCELLED_REASON = "Junior Cycle exams were cancelled in 2020 and 2021"
LCA_CANCELLED_REASON = ("No 2020 LCA written examinations — COVID-19 calculated grades "
                        "replaced them; nothing in the SEC archive")

# SEC renamed subjects mid-archive; merge so one subject spans its full run.
NAME_MERGES = {
    ("lb", "Intro. to Information & Comm. Technology"): "Information & Communication Tech.",
}

# SEC misfiled these exam papers/answer books in the markingschemes view —
# never offer them as scheme candidates (content-audited 2026-06-11).
MISFILED_SCHEMES = {
    (2011, "LC003ALP100IV.pdf"),  # maths 2011 HL IV P1: exam paper, not scheme
    (2011, "LC001ALP200IV.pdf"),  # irish 2011 HL IV P2: exam paper
    (2011, "LC067ALP008IV.pdf"),  # music 2011 HL IV listening: answer booklet
    (2011, "LC014ALP013EV.pdf"),  # art 2011 HL EV H&A: question paper
    (2011, "LC014ALP013IV.pdf"),  # art 2011 HL IV H&A: question paper
    (2011, "LB847CLP000EV.pdf"),  # LCA office admin 2011: written answer book
}

# Audited pairing corrections: (exam, year, paper fileid) -> scheme fileid.
PAIR_OVERRIDES = {
    ("lc", 2011, "LC003ALP100IV.pdf"): "LC003ALP000IV.pdf",
    ("lc", 2011, "LC001ALP200IV.pdf"): "LC001ALP000IV.pdf",
    ("lc", 2011, "LC067ALP008IV.pdf"): "LC067ALP000IV.pdf",
    ("lc", 2011, "LC014ALP013EV.pdf"): "LC014ALP000EV.pdf",
    ("lc", 2011, "LC014ALP013IV.pdf"): "LC014ALP000IV.pdf",
    ("lb", 2010, "LB847CLP000EV.pdf"): "LB847CLP016EV.pdf",  # WRITTEN scheme, not TASKS
    ("lb", 2011, "LB847CLP000EV.pdf"): "LB847CLP016EV.pdf",
}

# Known archive typos, normalised before decoding (verified by adversarial audit).
FILEID_FIXES = {
    "LC462CCLP000EV.pdf": "LC462CLP000EV.pdf",  # 2010 LCVP EV scheme: doubled 'C'
}
# Archive artifacts that are deliberate skips, not decode failures.
ARTIFACT_RE = re.compile(r"\s(\(2\)|hold)\.pdf$", re.I)

# JC new-spec windows (approved scope), keyed by slug of the SEC subject name.
JC_WINDOW_START = {"english": 2017, "science": 2019, "business-studies": 2019}
JC_DEFAULT_START = 2022

# fileid grammar: {LC|JC|LB}{SSS}{LVL}LP{CCC}{LANG}.pdf
# ("L?P" — at least one archive file, LC038AP000EV.pdf, drops the L)
FILEID_RE = re.compile(r"^(LC|JC|LB)(\d{3})([A-Z])L?P([A-Z0-9]{3})(EV|IV|BV)\.pdf$", re.I)
LEVEL_BY_CODE = {"A": "higher", "G": "ordinary", "B": "foundation", "C": "common"}
# Z = aural/other (no level) — only ever seen on non-PDF assets so far.

LEVEL_LABEL_RE = re.compile(r"^(Higher|Ordinary|Foundation|Common)\s+Level$", re.I)
LANG_LABEL_RE = re.compile(r"\s*\((EV|IV|BV)\)\s*$", re.I)
MODIFIED_RE = re.compile(r"\s*[-–—:(]?\s*\bModified\b\s*[)]?", re.I)

LEVEL_RANK = {"higher": 0, "ordinary": 1, "foundation": 2, "common": 3}
LANG_RANK = {"ev": 0, "iv": 1}

# Within-entry paper ordering by fileid component code (label is tie-break).
COMPONENT_ORDER = {
    "000": 0,                                  # single/whole paper
    "100": 10, "130": 11, "117": 15,           # Paper One (+ Project Maths / sound)
    "200": 20, "230": 21, "217": 25,           # Paper Two (+ Project Maths / sound)
    "A00": 40,                                 # Aural Paper
    "C00": 45,                                 # Source / Case paper
    "U00": 50,                                 # Unprepared Tests
}

# Per-entry notes for COVID-era LC sittings (exact strings per approved scope).
ENTRY_NOTES = {
    ("lc", 2020): "November 2020 deferred-sitting papers",
    ("lc", 2021): "adjusted format — COVID years",
}

# Answer-map (Stage 2.5 / anchor-map.py) QA gate. A (subjectId, level, lang)
# profile appears here ONLY after its contact-sheet human review passes (Phase 5).
# Empty = the answer machinery is wired but no `answers` flags ship yet, so the
# viewer toggle stays absent everywhere. Phase 5 adds e.g. ("mathematics","higher","ev").
# Wave-1 (2026-06-13): 16 subjects verified by per-subject adversarial agents +
# region-rect spot-checks against the real PDFs. Sciences/structured + EU
# languages with clean question↔scheme alignment. Essays (English, History),
# accounting-style workings, and passage-numbered languages (Croatian, Hungarian,
# Spanish…) are DEFERRED — they fail semantic alignment and need dedicated grammar.
QA_PASSED_ANSWER_PROFILES = {
    ('agricultural-science', 'higher', 'ev'),
    ('agricultural-science', 'ordinary', 'ev'),
    ('ancient-greek', 'higher', 'ev'),
    ('ancient-greek', 'ordinary', 'ev'),
    ('art', 'higher', 'ev'),
    ('art', 'ordinary', 'ev'),
    ('biology', 'higher', 'ev'),
    ('biology', 'ordinary', 'ev'),
    ('bulgarian', 'higher', 'ev'),
    ('chemistry', 'higher', 'ev'),
    ('chemistry', 'ordinary', 'ev'),
    ('computer-science', 'higher', 'ev'),
    ('computer-science', 'ordinary', 'ev'),
    ('construction-studies', 'higher', 'ev'),
    ('construction-studies', 'ordinary', 'ev'),
    ('croatian', 'higher', 'ev'),
    ('czech', 'higher', 'ev'),
    ('danish', 'higher', 'ev'),
    ('dutch', 'higher', 'ev'),
    ('economics', 'higher', 'ev'),
    ('economics', 'ordinary', 'ev'),
    ('finnish', 'higher', 'ev'),
    ('history', 'higher', 'ev'),
    ('hungarian', 'higher', 'ev'),
    ('jc-business-studies', 'common', 'ev'),
    ('jc-english', 'higher', 'ev'),
    ('jc-english', 'ordinary', 'ev'),
    ('jc-geography', 'common', 'ev'),
    ('jc-home-economics', 'common', 'ev'),
    ('jc-jewish-studies', 'common', 'ev'),
    ('jc-mathematics', 'higher', 'ev'),
    ('jc-mathematics', 'ordinary', 'ev'),
    ('jc-music', 'common', 'ev'),
    ('jc-religious-education', 'common', 'ev'),
    ('jc-science', 'common', 'ev'),
    ('jc-wood-technology', 'common', 'ev'),
    ('latin', 'ordinary', 'ev'),
    ('latvian', 'higher', 'ev'),
    ('lca-agriculture-horticulture', 'common', 'ev'),
    ('lca-childcare-community-care', 'common', 'ev'),
    ('lca-crafts-and-design', 'common', 'ev'),
    ('lca-english-and-communications', 'common', 'ev'),
    ('lca-french', 'common', 'ev'),
    ('lca-german', 'common', 'ev'),
    ('lca-hair-and-beauty', 'common', 'ev'),
    ('lca-hotel-catering-and-tourism', 'common', 'ev'),
    ('lca-information-and-communication-tech', 'common', 'ev'),
    ('lca-italian', 'common', 'ev'),
    ('lca-office-admin-and-customer', 'common', 'ev'),
    ('lca-sign-language', 'common', 'ev'),
    ('lithuanian', 'higher', 'ev'),
    ('maltese', 'higher', 'ev'),
    ('mathematics', 'higher', 'ev'),
    ('mathematics', 'ordinary', 'ev'),
    ('modern-greek', 'higher', 'ev'),
    ('physical-education', 'higher', 'ev'),
    ('physical-education', 'ordinary', 'ev'),
    ('physics', 'higher', 'ev'),
    ('physics', 'ordinary', 'ev'),
    ('physics-and-chemistry', 'higher', 'ev'),
    ('physics-and-chemistry', 'ordinary', 'ev'),
    ('portuguese', 'higher', 'ev'),
    ('religious-education', 'ordinary', 'ev'),
    ('romanian', 'higher', 'ev'),
    ('slovakian', 'higher', 'ev'),
    ('slovenian', 'higher', 'ev'),
}

# ─── Hand-written subject knowledge ──────────────────────────────────────────

# Profile-picker aliases (components/subjectData.ts LC_SUBJECTS / JC_SUBJECTS)
# keyed by registry id. The SEC display name is always prepended at emit time.
ALIAS_MAP = {
    # LC picker names that differ from the SEC archive name
    "agricultural-science": ["Ag Science"],
    "applied-mathematics": ["Applied Maths"],
    "design-and-communication-graphics": ["DCG"],
    "home-economics-s-and-s": ["Home Economics", "Home Ec"],
    "politics-and-society": ["Politics & Society"],
    "physics-and-chemistry": ["Physics and Chemistry"],
    "link-modules": ["LCVP Link Modules", "LCVP"],
    "irish": ["Gaeilge"],
    # JC picker names (SEC JC names may differ — mapped when rows appear)
    "jc-business-studies": ["Business Studies"],
    "jc-science": ["Science"],
    "jc-civic-social-and-political-education": ["CSPE"],
    "jc-social-personal-and-health-education": ["SPHE"],
    "jc-materials-technology-wood": ["Materials Technology (Wood)"],
    "jc-graphics": ["Graphics"],
    "jc-metalwork": ["Metalwork"],
    "jc-irish": ["Gaeilge"],
    "jc-irish-t1": ["Gaeilge T1", "Irish"],
    "jc-irish-t2": ["Gaeilge T2", "Irish"],
}

# Explicit curriculum links where name-matching can't get there on its own,
# keyed by (cycle, normalised SEC name) → CURRICULUM id (see curriculum.ts).
CURRICULUM_OVERRIDES = {
    ("lc", "home economics s and s"): "home-economics",
    ("lc", "home economics scientific and social"): "home-economics",
    ("lc", "link modules"): "lcvp-link-modules",
    ("jc", "irish t1"): None,        # T1 spec has no curriculum subject
    ("jc", "irish t2"): "jc-irish",  # curriculum jc-irish is 'Gaeilge T2'
    ("jc", "gaeilge t1"): None,
    ("jc", "gaeilge t2"): "jc-irish",
}


def log(msg):
    print(msg, flush=True)


def slugify(name):
    # NFKD-fold diacritics so e.g. 'Gaeilge Chumarsáideach' slugs cleanly
    s = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode()
    s = s.lower().replace("&", " and ")
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def norm_name(name, strip_parens=False):
    if strip_parens:
        name = re.sub(r"\([^)]*\)", " ", name)
    s = name.lower().replace("&", " and ")
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9]+", " ", s)).strip()


def load_jsonl(path):
    rows = []
    if not os.path.exists(path):
        return rows
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                pass  # tolerate a truncated trailing line mid-crawl
    return rows


def parse_curriculum():
    """[(id, name, levels)] for the 48 CURRICULUM subjects."""
    src = open(CURRICULUM_TS, encoding="utf-8").read()
    pat = re.compile(
        r'"id":\s*"([a-z0-9-]+)",\s*"name":\s*"([^"]+)",\s*"category":\s*"[^"]+",'
        r'\s*"levels":\s*\[([^\]]*)\]',
        re.S,
    )
    subs = []
    for m in pat.finditer(src):
        subs.append((m.group(1), m.group(2), re.findall(r'"(\w+)"', m.group(3))))
    if not subs:
        raise RuntimeError("could not parse CURRICULUM out of curriculum.ts")
    return subs


# ─── Row decoding ────────────────────────────────────────────────────────────

class Issues:
    """Report buckets."""

    def __init__(self):
        self.non_pdf = Counter()                 # ext -> count
        self.non_pdf_rows = defaultdict(int)     # (exam, name, year) -> count
        self.undecodable = []                    # rows we had to drop
        self.artifacts = []                      # deliberate skips: "(2)"/"hold" uploads
        self.fileid_fallback = []                # decoded from label only (e.g. LCA)
        self.level_disagree = []                 # label vs fileid level
        self.lang_disagree = []                  # label vs fileid lang
        self.component_disagree = []             # label vs fileid component
        self.bv_lang = []                        # BV rows folded into 'ev'
        self.jc_filtered = Counter()             # (name, year) -> count (old-spec)
        self.jc_irish_unmarked = []              # split applied but label has no T1/T2
        self.download_errors = []                # rows excluded: Stage 2 error
        self.bytes_pending = 0                   # docs emitted with b: 0
        self.scheme_extras = []                  # >1 scheme candidate for a key
        self.scheme_odd_component = []           # scheme component != 000
        self.sec_id_renames = []                 # one SEC id, several names
        self.unpaired_papers = []                # (subjectId, year, level, lang, n)
        self.unpaired_schemes = []               # (exam, name, year, level, lang, n)


def decode_row(row, issues):
    """Decode one PDF manifest row. Returns dict or None (dropped + reported)."""
    fileid = FILEID_FIXES.get(row["fileid"].strip(), row["fileid"].strip())
    label = html.unescape(row["label"]).strip()
    name = html.unescape(row["subjectName"]).strip()
    exam = row["exam"]
    name = NAME_MERGES.get((exam, name), name)
    if ARTIFACT_RE.search(fileid):
        issues.artifacts.append(f"{exam} {row['year']} {name} {fileid} (duplicate/held upload)")
        return None
    year = int(row["year"])
    where = f"{exam} {year} {name} {fileid}"

    m = FILEID_RE.match(fileid)
    code_level = code_lang = component = None
    if m:
        code_level = LEVEL_BY_CODE.get(m.group(3).upper())
        component = m.group(4).upper()
        code_lang = m.group(5).lower()
    else:
        issues.fileid_fallback.append(f"{where} | {label}")

    # Language: label '(EV)' suffix wins; fileid is the fallback.
    lm = LANG_LABEL_RE.search(label)
    label_lang = lm.group(1).lower() if lm else None
    lang = label_lang or code_lang
    if label_lang and code_lang and label_lang != code_lang:
        issues.lang_disagree.append(f"{where}: label ({label_lang}) vs fileid ({code_lang})")
    bilingual = lang == "bv"
    if bilingual:
        # From 2019 the SEC publishes a single bilingual document for some
        # subjects instead of separate EV/IV — surface it on the 'ev' side
        # and note it on the entry.
        issues.bv_lang.append(where)
        lang = "ev"
    if lang not in ("ev", "iv"):
        issues.undecodable.append(f"{where}: no language | {label}")
        return None

    # Split label into ' / ' parts; pull out level + Modified flag.
    body = LANG_LABEL_RE.sub("", label).strip()
    modified = False
    label_level = None
    parts_out = []
    # strip(' /') tolerates stray leading/trailing slashes in archive labels
    # (e.g. '/ Ordinary Level (BV)') without touching internal ones
    # ('Picture/Illustration').
    for part in (p.strip(" /") for p in body.split(" / ")):
        if MODIFIED_RE.search(part):
            modified = True
            part = re.sub(r"\s+", " ", MODIFIED_RE.sub(" ", part)).strip(" -–—:")
        if not part:
            continue
        pl = LEVEL_LABEL_RE.match(part)
        if pl:
            label_level = pl.group(1).lower()
        else:
            parts_out.append(part)

    level = label_level or code_level
    if label_level and code_level and label_level != code_level:
        issues.level_disagree.append(f"{where}: label ({label_level}) vs fileid ({code_level})")
    if level is None and exam == "lb":
        level = "common"  # LCA is a common-level programme
        issues.fileid_fallback.append(f"{where}: no level anywhere — defaulted to common (LCA)")
    if level is None:
        issues.undecodable.append(f"{where}: no level | {label}")
        return None

    kind = "scheme" if row["view"] == "markingschemes" else "paper"
    paper_label = " / ".join(parts_out)
    if kind == "scheme":
        if component and component != "000":
            issues.scheme_odd_component.append(f"{where} | {label}")
    else:
        if not paper_label:
            paper_label = "Exam Paper"
        # Component vs label sanity (label wins; recorded only).
        if component:
            if re.match(r"Paper One\b", paper_label) and component not in ("100", "130", "117"):
                issues.component_disagree.append(f"{where}: '{paper_label}' vs component {component}")
            if re.match(r"Paper Two\b", paper_label) and component not in ("200", "230", "217"):
                issues.component_disagree.append(f"{where}: '{paper_label}' vs component {component}")

    return {
        "view": row["view"],
        "exam": exam,
        "cycle": CYCLE_OF_EXAM[exam],
        "year": year,
        "secId": str(row["subjectId"]),
        "secName": name,
        "effName": name,  # may be rewritten by the JC Irish T1/T2 split
        "kind": kind,
        "level": level,
        "lang": lang,
        "modified": modified,
        "bilingual": bilingual,
        "paperLabel": paper_label,
        "component": component,
        "fileid": fileid,
    }


def jc_window_start(name):
    base = slugify(re.sub(r"\(T[12]\)", "", name))
    return JC_WINDOW_START.get(base, JC_DEFAULT_START)


def main():
    log("Paper Trail — Stage 3: build index")
    issues = Issues()

    manifest = load_jsonl(MANIFEST)
    if not manifest:
        log(f"FATAL: no rows in {MANIFEST}")
        return 1
    # Dedupe (resume-safe Stage 1 can in principle repeat rows).
    seen, rows = set(), []
    for r in manifest:
        key = (r["view"], r["exam"], r["year"], r["subjectId"], r["fileid"])
        if key not in seen:
            seen.add(key)
            rows.append(r)

    downloads_present = os.path.exists(DOWNLOADS)
    dl = {}
    for d in load_jsonl(DOWNLOADS):
        dl[(d["view"], d["year"], d["fileid"])] = d

    # Stage 2.5 answer maps: every COMMITTED per-paper sidecar (cumulative across
    # waves), keyed (year, paperFileid). Scanning the files (not a per-run
    # manifest) means pruning a drifted year's sidecar de-flags it, and each wave
    # only adds files — no manifest bookkeeping.
    answer_mapped = set()  # (year, paperFileid)
    answers_root = os.path.join(HERE, "answers")
    if os.path.isdir(answers_root):
        for yd in os.listdir(answers_root):
            ydp = os.path.join(answers_root, yd)
            if yd.isdigit() and os.path.isdir(ydp):
                for fn in os.listdir(ydp):
                    if fn.endswith(".json"):
                        answer_mapped.add((int(yd), fn[:-5]))  # strip .json → paperFileid

    subjects_json = {}
    if os.path.exists(SUBJECTS_JSON):
        subjects_json = json.load(open(SUBJECTS_JSON, encoding="utf-8"))
    listing = defaultdict(set)         # (exam, year) -> SEC names (exampapers view)
    schemes_listing = defaultdict(set)  # (exam, year) -> SEC names (markingschemes view)
    for key, subs in subjects_json.items():
        view, exam, year = key.split("|")
        target = listing if view == "exampapers" else schemes_listing
        for _, n in subs:
            nm = html.unescape(n).strip()
            target[(exam, int(year))].add(NAME_MERGES.get((exam, nm), nm))

    crawl_views = sorted({r["view"] for r in rows})
    crawl_span = sorted({(r["exam"], int(r["year"])) for r in rows})
    log(f"  manifest: {len(rows)} unique rows | views: {', '.join(crawl_views)}")
    log(f"  downloads.jsonl: {'%d records' % len(dl) if downloads_present else 'MISSING (Stage 2 not run yet)'}")

    # ── Decode ───────────────────────────────────────────────────────────────
    decoded = []
    for r in rows:
        if not r["fileid"].lower().endswith(".pdf"):
            ext = r["fileid"].rsplit(".", 1)[-1].lower()
            issues.non_pdf[ext] += 1
            issues.non_pdf_rows[(r["exam"], html.unescape(r["subjectName"]).strip(), int(r["year"]))] += 1
            continue
        d = decode_row(r, issues)
        if d:
            decoded.append(d)
    log(f"  decoded: {len(decoded)} PDF rows | non-PDF skipped: {sum(issues.non_pdf.values())}"
        f" | undecodable: {len(issues.undecodable)}")

    # ── JC Irish T1/T2 split ─────────────────────────────────────────────────
    jc_irish = [d for d in decoded if d["exam"] == "jc"
                and norm_name(d["secName"]) in ("irish", "gaeilge")]
    sec_distinguishes = any(re.search(r"\bT[12]\b", d["secName"]) for d in decoded if d["exam"] == "jc")
    if jc_irish and not sec_distinguishes:
        if any(re.search(r"\bT[12]\b", d["paperLabel"]) for d in jc_irish):
            for d in jc_irish:
                tm = re.search(r"\bT([12])\b", d["paperLabel"])
                if tm:
                    d["effName"] = f"{d['secName']} (T{tm.group(1)})"
                    d["paperLabel"] = re.sub(r"\s+", " ", re.sub(r"\s*\(?\bT[12]\b\)?", " ", d["paperLabel"])).strip() or "Exam Paper"
                else:
                    d["effName"] = f"{d['secName']} (T2)"  # unmarked → mainstream T2
                    issues.jc_irish_unmarked.append(f"jc {d['year']} {d['fileid']} | {d['paperLabel']}")
    elif sec_distinguishes:
        for d in decoded:
            if d["exam"] != "jc":
                continue
            tm = re.search(r"\bT([12])\b", d["secName"])
            if tm and norm_name(re.sub(r"\bT[12]\b", "", d["secName"])) in ("irish", "gaeilge"):
                d["effName"] = f"Irish (T{tm.group(1)})"

    # ── JC new-spec filter ───────────────────────────────────────────────────
    kept = []
    for d in decoded:
        if d["exam"] == "jc" and d["year"] < jc_window_start(d["effName"]):
            issues.jc_filtered[(d["effName"], d["year"])] += 1
            continue
        kept.append(d)
    n_filtered = len(decoded) - len(kept)
    if n_filtered:
        log(f"  JC old-spec filtered: {n_filtered} rows")
    decoded = kept

    # ── SEC id ↔ name consistency check (report only) ────────────────────────
    names_by_id = defaultdict(set)
    for d in decoded:
        names_by_id[(d["exam"], d["secId"])].add(d["secName"])
    for (exam, sid), names in sorted(names_by_id.items()):
        if len(names) > 1:
            issues.sec_id_renames.append(f"{exam} SEC id {sid}: {sorted(names)}")

    # ── Attach byte counts / drop failed downloads ───────────────────────────
    RAW_FILEIDS = {v: k for k, v in FILEID_FIXES.items()}

    def doc_for(d):
        rec = (dl.get((d["view"], str(d["year"]), d["fileid"]))
               or dl.get((d["view"], str(d["year"]), RAW_FILEIDS.get(d["fileid"], ""))))
        if rec is None:
            issues.bytes_pending += 1
            return {"f": d["fileid"], "b": 0}
        if "error" in rec:
            issues.download_errors.append(
                f"{d['exam']} {d['year']} {d['effName']} {d['fileid']}: {rec['error']}")
            return None
        return {"f": d["fileid"], "b": int(rec.get("bytes", 0))}

    # ── Registry from paper rows ─────────────────────────────────────────────
    papers = [d for d in decoded if d["kind"] == "paper"]
    schemes = [d for d in decoded if d["kind"] == "scheme"]

    curriculum = parse_curriculum()
    cur_by_norm = {"lc": {}, "jc": {}}
    for cid, cname, _levels in curriculum:
        pool = "jc" if cid.startswith("jc-") else "lc"
        cur_by_norm[pool][norm_name(cname, strip_parens=True)] = cid

    def curriculum_id_for(cycle, sec_name):
        key = (("jc" if cycle == "jc" else "lc"), norm_name(sec_name))
        if key in CURRICULUM_OVERRIDES:
            return CURRICULUM_OVERRIDES[key]
        if cycle == "lca":
            return None  # LCA programme — no curriculum.ts subjects
        return cur_by_norm["jc" if cycle == "jc" else "lc"].get(norm_name(sec_name))

    registry = {}  # (exam, effName) -> subject dict
    for d in papers:
        key = (d["exam"], d["effName"])
        if key in registry:
            continue
        cycle = d["cycle"]
        sid = CYCLE_PREFIX[cycle] + slugify(d["effName"])
        aliases = [d["effName"]] + ALIAS_MAP.get(sid, [])
        aliases = sorted(set(aliases), key=lambda a: (a != d["effName"], a))  # SEC name first
        registry[key] = {
            "id": sid,
            "name": d["effName"],
            "cycle": cycle,
            "exam": d["exam"],
            "levels": set(),
            "curriculumId": curriculum_id_for(cycle, d["effName"]),
            "aliases": aliases if len(aliases) > 1 else None,
            "origNames": {d["secName"]},
        }
    for d in papers:
        registry[(d["exam"], d["effName"])]["origNames"].add(d["secName"])

    dup_ids = [i for i, c in Counter(s["id"] for s in registry.values()).items() if c > 1]
    if dup_ids:
        raise RuntimeError(f"registry id collision: {dup_ids}")

    # ── Pairing ──────────────────────────────────────────────────────────────
    def pairkey(d):
        return (d["exam"], d["effName"], d["year"], d["level"], d["lang"])

    schemes_by_key = defaultdict(list)
    for s in schemes:
        if (s["year"], s["fileid"]) in MISFILED_SCHEMES:
            issues.scheme_extras.append(
                f"{s['exam']} {s['year']} {s['effName']}: MISFILED in archive scheme view "
                f"(actually a paper/answer book) — excluded: {s['fileid']}")
            continue
        schemes_by_key[pairkey(s)].append(s)

    def scheme_for_paper(p, cands):
        """Pick the scheme whose component family matches THIS paper.

        The SEC publishes distinct examinations under one subject-year-level
        key (e.g. 2010-13 'Project Maths' pilot components 130/230 with their
        own 030 scheme alongside the standard 100/200 papers with the 000
        scheme). Component-blind pairing attached the WRONG examination's
        scheme — caught by adversarial audit. Tiers: exact component match,
        then same component family (last two digits), then the whole-level 000
        scheme — and a 'Project Maths' label may never cross the boundary.
        Better unpaired than wrong."""
        forced = PAIR_OVERRIDES.get((p["exam"], p["year"], p["fileid"]))
        if forced:
            for sc in cands:
                if sc["fileid"] == forced:
                    return sc
            return None  # forced target absent: better unpaired than wrong
        pm_p = "project maths" in p["paperLabel"].lower()
        p_comp = p["component"] or ""
        best, best_rank = None, (9, True, "")
        for sc in cands:
            sc_comp = sc["component"] or ""
            if sc_comp == p_comp:
                tier = 0
            elif sc_comp[-2:] == p_comp[-2:] and sc_comp and p_comp:
                tier = 1
            elif sc_comp == "000":
                tier = 2
            else:
                continue
            if ("project maths" in sc["paperLabel"].lower()) != pm_p:
                continue
            rank = (tier, sc["modified"], sc["fileid"])
            if rank < best_rank:
                best, best_rank = sc, rank
        return best

    papers_by_key = defaultdict(list)
    for p in papers:
        papers_by_key[pairkey(p)].append(p)

    # entries[subject id][(year, level, lang)] = [paper objects]
    entries = defaultdict(lambda: defaultdict(list))
    bilingual_counts = defaultdict(lambda: [0, 0])  # (sid,y,lvl,lang) -> [bv, total]
    paired_keys = set()
    pair_counts = defaultdict(lambda: [0, 0])  # (sid, year, level) -> [papers, with-scheme]
    upload_rows = {}  # remote path -> local path (deduped; single source of truth for upload layout)
    answer_upload_rows = {}  # remote sidecar path -> local sidecar path (QA-passed only)

    for key in sorted(papers_by_key):
        exam, eff_name, year, level, lang = key
        sid = registry[(exam, eff_name)]["id"]
        cands = schemes_by_key.get(key, [])
        if cands:
            paired_keys.add(key)
        used_scheme_ids = set()
        unscheduled = 0
        group = sorted(papers_by_key[key],
                       key=lambda p: (COMPONENT_ORDER.get(p["component"], 60)
                                      if p["component"] in COMPONENT_ORDER or not (p["component"] or "").isdigit()
                                      else 60 + int(p["component"]),
                                      p["paperLabel"], p["fileid"]))
        for p in group:
            doc = doc_for(p)
            if doc is None:
                continue
            item = {"label": p["paperLabel"], "doc": doc}
            _cy = registry[(exam, eff_name)]["cycle"]
            upload_rows[f"papers/{_cy}/{sid}/{year}/paper/{p['fileid']}"] = \
                f"paper-trail-corpus/{p['view']}/{p['year']}/{p['fileid']}"
            prim = scheme_for_paper(p, cands)
            scheme_doc = doc_for(prim) if prim else None
            if prim and scheme_doc:
                used_scheme_ids.add(id(prim))
                upload_rows[f"papers/{_cy}/{sid}/{year}/scheme/{prim['fileid']}"] = \
                    f"paper-trail-corpus/{prim['view']}/{prim['year']}/{prim['fileid']}"
                item["scheme"] = scheme_doc
            else:
                unscheduled += 1
            if p["modified"]:
                item["modified"] = True
            # Answer-map flag (Stage 2.5) — only for QA-passed grammar profiles,
            # and only when anchor-map.py actually mapped this paper.
            _sidecar_local = os.path.join("scripts", "paper-trail", "answers", str(year), f"{p['fileid']}.json")
            if ((year, p["fileid"]) in answer_mapped
                    and (sid, level, lang) in QA_PASSED_ANSWER_PROFILES
                    and os.path.exists(os.path.join(REPO, _sidecar_local))):
                # File-existence gate: deleting a drifted year's sidecar cleanly
                # de-flags it even while its profile stays QA-passed.
                item["answers"] = 1
                answer_upload_rows[f"papers/{_cy}/{sid}/{year}/answers/{p['fileid']}.json"] = _sidecar_local
            entries[sid][(year, level, lang)].append(item)
            bc = bilingual_counts[(sid, year, level, lang)]
            bc[0] += 1 if p["bilingual"] else 0
            bc[1] += 1
            pc = pair_counts[(sid, year, level)]
            pc[0] += 1
            pc[1] += 1 if scheme_doc else 0
        for sc in cands:
            if id(sc) not in used_scheme_ids:
                issues.scheme_extras.append(
                    f"{exam} {year} {eff_name} {level}/{lang}: unmatched scheme candidate "
                    f"{sc['fileid']} ({sc['paperLabel']})")
        if unscheduled and entries[sid].get((year, level, lang)):
            issues.unpaired_papers.append((sid, year, level, lang, unscheduled))

    for key in sorted(schemes_by_key):
        if key not in paired_keys:
            exam, eff_name, year, level, lang = key
            issues.unpaired_schemes.append((exam, eff_name, year, level, lang, len(schemes_by_key[key])))

    # Subject levels = union over surviving entries; drop empty groups.
    index = {}
    for sid in sorted(entries):
        subj = next(s for s in registry.values() if s["id"] == sid)
        out = []
        for (year, level, lang), items in entries[sid].items():
            if not items:
                continue
            subj["levels"].add(level)
            entry = {"year": year, "level": level, "lang": lang, "papers": items}
            notes = []
            if ENTRY_NOTES.get((subj["cycle"], year)):
                notes.append(ENTRY_NOTES[(subj["cycle"], year)])
            bv, total = bilingual_counts[(sid, year, level, lang)]
            if total and bv == total:  # only when EVERY doc is bilingual
                notes.append("bilingual English/Irish document")
            if notes:
                entry["note"] = " · ".join(notes)
            out.append(entry)
        out.sort(key=lambda e: (-e["year"], LEVEL_RANK[e["level"]], LANG_RANK[e["lang"]]))
        if out:
            index[sid] = out

    subjects = sorted((s for s in registry.values() if s["id"] in index),
                      key=lambda s: (CYCLE_RANK[s["cycle"]], s["id"]))

    # ── Gaps ─────────────────────────────────────────────────────────────────
    decoded_paper_years = defaultdict(set)   # (exam, origName) -> years with decoded papers
    for p in papers:
        decoded_paper_years[(p["exam"], p["secName"])].add(p["year"])

    gaps = []
    for s in subjects:
        exam, cycle = s["exam"], s["cycle"]
        years_with_entries = {e["year"] for e in index.get(s["id"], [])}
        listed_years = sorted(y for (ex, y), names in listing.items()
                              if ex == exam and (names & s["origNames"]))
        if cycle == "jc":
            start = jc_window_start(s["name"])
            expected = range(start, JC_YEAR_MAX + 1)
        else:
            expected = range(LC_YEAR_MIN, LC_YEAR_MAX + 1)
        for y in expected:
            if y in years_with_entries:
                continue
            if cycle == "jc" and y in JC_CANCELLED_YEARS:
                gaps.append({"subjectId": s["id"], "year": y, "reason": JC_CANCELLED_REASON})
                continue
            if cycle == "lca" and y == 2020:
                gaps.append({"subjectId": s["id"], "year": y, "reason": LCA_CANCELLED_REASON})
                continue
            if (exam, y) not in listing:
                continue  # year not crawled (partial run) — not a verified gap
            if any(y in decoded_paper_years[(exam, n)] for n in s["origNames"]):
                gaps.append({"subjectId": s["id"], "year": y,
                             "reason": "all archived PDFs for this year failed to download"})
            elif listing[(exam, y)] & s["origNames"]:
                if any(issues.non_pdf_rows.get((exam, n, y)) for n in s["origNames"]):
                    gaps.append({"subjectId": s["id"], "year": y,
                                 "reason": "only non-PDF materials (audio/video) in the archive for this year"})
                else:
                    gaps.append({"subjectId": s["id"], "year": y,
                                 "reason": "listed in the SEC archive but no PDF materials were found"})
            elif schemes_listing.get((exam, y), set()) & s["origNames"]:
                gaps.append({"subjectId": s["id"], "year": y,
                             "reason": "no exam paper in the SEC archive for this year — marking scheme only"})
            elif listed_years and listed_years[0] < y < listed_years[-1]:
                gaps.append({"subjectId": s["id"], "year": y,
                             "reason": "not in the SEC archive subject list for this year"})
            # years outside the subject's own listed span are not holes — skip
    gaps.sort(key=lambda g: (g["subjectId"], g["year"]))

    # ── Emit paperTrailData.ts ───────────────────────────────────────────────
    def ts(obj):
        return json.dumps(obj, ensure_ascii=False)

    lines = [
        "/**",
        " * @license",
        " * SPDX-License-Identifier: Apache-2.0",
        " *",
        " * GENERATED FILE — do not edit by hand.",
        " * Built by scripts/paper-trail/build-index.py from the SEC Exam Material",
        " * Archive harvest (scripts/paper-trail/out/). Re-run the script to refresh;",
        " * see scripts/paper-trail/out/index-report.md for the build report.",
        " *",
        " * Source: State Examinations Commission Exam Material Archive",
        " * (examinations.ie). Import this module only inside the lazy Paper Trail",
        " * tool chunk — it is data-heavy.",
        " */",
        "",
    ]
    contract = os.path.exists(TYPES_TS)
    if contract:
        # types/paperTrail.ts is the generator<->UI contract: import + re-export
        # so there is exactly one declaration of these types in the repo.
        lines += [
            "import { type PaperEntry, type PaperTrailGap, type PaperTrailSubject } from './types/paperTrail';",
            "",
            "export {",
            "  type PaperCycle,",
            "  type PaperDoc,",
            "  type PaperEntry,",
            "  type PaperItem,",
            "  type PaperLang,",
            "  type PaperLevel,",
            "  type PaperTrailGap,",
            "  type PaperTrailSubject,",
            "} from './types/paperTrail';",
            "",
        ]
    else:
        # Standalone fallback — keep the generated file self-contained.
        lines += [
            "export type PaperCycle = 'lc' | 'jc' | 'lca';",
            "export type PaperLevel = 'higher' | 'ordinary' | 'foundation' | 'common';",
            "export type PaperLang = 'ev' | 'iv';",
            "",
            "export interface PaperTrailSubject {",
            "  id: string;",
            "  name: string;",
            "  cycle: PaperCycle;",
            "  levels: PaperLevel[];",
            "  /** Matching subject id in curriculum.ts, where one exists. */",
            "  curriculumId?: string;",
            "  /** SEC display name + profile-picker names that refer to this subject. */",
            "  aliases?: string[];",
            "}",
            "",
            "/** One archived PDF: f = SEC fileid, b = size in bytes (0 = size pending). */",
            "export interface PaperDoc { f: string; b: number }",
            "",
            "export interface PaperEntry {",
            "  year: number;",
            "  level: PaperLevel;",
            "  lang: PaperLang;",
            "  papers: { label: string; doc: PaperDoc; scheme?: PaperDoc; modified?: boolean }[];",
            "  note?: string;",
            "}",
            "",
            "export interface PaperTrailGap { subjectId: string; year: number; reason: string }",
            "",
        ]
    lines.append("export const PAPER_TRAIL_SUBJECTS: PaperTrailSubject[] = [")
    for s in subjects:
        obj = {"id": s["id"], "name": s["name"], "cycle": s["cycle"],
               "levels": sorted(s["levels"], key=LEVEL_RANK.get)}
        if s["curriculumId"]:
            obj["curriculumId"] = s["curriculumId"]
        if s["aliases"]:
            obj["aliases"] = s["aliases"]
        lines.append(f"  {ts(obj)},")
    lines += ["];", "", "export const PAPER_TRAIL_INDEX: Record<string, PaperEntry[]> = {"]
    for s in subjects:
        lines.append(f"  {ts(s['id'])}: [")
        for e in index[s["id"]]:
            lines.append(f"    {ts(e)},")
        lines.append("  ],")
    lines += ["};", "", "export const PAPER_TRAIL_GAPS: PaperTrailGap[] = ["]
    for g in gaps:
        lines.append(f"  {ts(g)},")
    lines += ["];", ""]
    with open(DATA_TS, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    n_papers = sum(len(e["papers"]) for es in index.values() for e in es)
    n_paired = sum(1 for es in index.values() for e in es for p in e["papers"] if "scheme" in p)
    log(f"  wrote {os.path.relpath(DATA_TS, REPO)} — {len(subjects)} subjects, "
        f"{sum(len(v) for v in index.values())} entries, {n_papers} papers "
        f"({n_paired} with schemes), {len(gaps)} gaps "
        f"[{os.path.getsize(DATA_TS) / 1024:.0f} KB]")

    # ── Report ───────────────────────────────────────────────────────────────
    rep = []
    w = rep.append
    w("# Paper Trail — Stage 3 build report (index-report.md)")
    w("")
    w("Generated by `scripts/paper-trail/build-index.py`. Deterministic for a given")
    w("set of harvest files; re-run after the crawl/downloads complete.")
    w("")
    w("## Inputs")
    w("")
    w(f"- manifest.jsonl: **{len(rows)}** unique rows; views seen: {', '.join(crawl_views)}")
    exams_seen = ", ".join(sorted({f'{e} {min(y for x, y in crawl_span if x == e)}-{max(y for x, y in crawl_span if x == e)}' for e, _ in crawl_span}))
    w(f"- exam/year coverage in manifest so far: {exams_seen}")
    if not downloads_present:
        w("- downloads.jsonl: **missing** — Stage 2 has not run; all byte counts emitted as 0 (pending)")
    else:
        w(f"- downloads.jsonl: {len(dl)} records ({len(issues.download_errors)} errors, "
          f"{issues.bytes_pending} docs still pending)")
    missing_views = [v for v in ("exampapers", "markingschemes") if v not in crawl_views]
    if missing_views:
        w(f"- **PARTIAL CRAWL**: no `{'`, `'.join(missing_views)}` rows yet — pairing/gap "
          f"results below will change on the full data")
    w("")
    w("## Registry")
    w("")
    w(f"- {len(subjects)} subjects "
      f"(lc {sum(1 for s in subjects if s['cycle'] == 'lc')}, "
      f"jc {sum(1 for s in subjects if s['cycle'] == 'jc')}, "
      f"lca {sum(1 for s in subjects if s['cycle'] == 'lca')}); "
      f"{sum(1 for s in subjects if s['curriculumId'])} linked to curriculum.ts")
    w("")
    w("| id | SEC name | cycle | levels | curriculumId | aliases |")
    w("|---|---|---|---|---|---|")
    for s in subjects:
        w(f"| {s['id']} | {s['name']} | {s['cycle']} | "
          f"{', '.join(sorted(s['levels'], key=LEVEL_RANK.get))} | "
          f"{s['curriculumId'] or '—'} | {', '.join(s['aliases'] or []) or '—'} |")
    unmapped = [s for s in subjects if not s["curriculumId"]]
    w("")
    w(f"### Unmapped SEC subjects ({len(unmapped)}) — no curriculum.ts counterpart (expected "
      f"for EU languages, LCA, legacy subjects)")
    w("")
    for s in unmapped:
        w(f"- {s['id']} ({s['name']}, {s['cycle']})")
    w("")
    w("## Coverage (years × levels — `papers/with-scheme` per cell)")
    w("")
    all_levels = ["higher", "ordinary", "foundation", "common"]
    for s in subjects:
        w(f"### {s['name']} ({s['id']})")
        w("")
        w("| year | " + " | ".join(lv.capitalize() for lv in all_levels) + " |")
        w("|---|" + "---|" * len(all_levels))
        years = sorted({e["year"] for e in index[s["id"]]}, reverse=True)
        for y in years:
            cells = []
            for lv in all_levels:
                pc = pair_counts.get((s["id"], y, lv))
                cells.append(f"{pc[0]}/{pc[1]}" if pc else "—")
            w(f"| {y} | " + " | ".join(cells) + " |")
        w("")
    w("## Unpaired")
    w("")
    w(f"### Papers without a marking scheme ({sum(n for *_k, n in issues.unpaired_papers)} "
      f"papers in {len(issues.unpaired_papers)} subject-year-level-lang groups)")
    w("")
    if missing_views:
        w("(_expected right now — the markingschemes view has not been crawled yet_)")
        w("")
    for sid, year, level, lang, n in sorted(issues.unpaired_papers):
        w(f"- {sid} {year} {level}/{lang}: {n} paper(s)")
    w("")
    w(f"### Schemes without papers ({len(issues.unpaired_schemes)} groups)")
    w("")
    for exam, name, year, level, lang, n in sorted(issues.unpaired_schemes):
        w(f"- {exam} {name} {year} {level}/{lang}: {n} scheme(s)")
    w("")
    w("## Gaps emitted (PAPER_TRAIL_GAPS)")
    w("")
    reason_counts = Counter(g["reason"] for g in gaps)
    for reason, c in sorted(reason_counts.items()):
        w(f"- {c} × \"{reason}\"")
    w("")
    for g in gaps:
        w(f"- {g['subjectId']} {g['year']}: {g['reason']}")
    w("")
    w("## Skipped & filtered")
    w("")
    w(f"### Non-PDF assets skipped ({sum(issues.non_pdf.values())}) — v1 scope is PDFs only")
    w("")
    for ext, c in sorted(issues.non_pdf.items()):
        w(f"- .{ext}: {c}")
    w("")
    w(f"### JC old-spec rows filtered ({sum(issues.jc_filtered.values())}) — pre-window years, "
      f"not gaps")
    w("")
    for (name, year), c in sorted(issues.jc_filtered.items()):
        w(f"- {name} {year}: {c} rows")
    w("")
    w(f"### Download errors — rows excluded from the index ({len(issues.download_errors)})")
    w("")
    for line in sorted(issues.download_errors):
        w(f"- {line}")
    w("")
    w("## Decode notes")
    w("")

    def section(title, items):
        w(f"### {title} ({len(items)})")
        w("")
        for it in sorted(items):
            w(f"- {it}")
        w("")

    section("Rows dropped as undecodable", issues.undecodable)
    section("Archive artifacts skipped deliberately ('(2)'/'hold' uploads)", issues.artifacts)
    w("")
    w("## Modified (vision-impaired) documents")
    n_mod = sum(1 for sid in index for e in index[sid] for it in e["papers"] if it.get("modified"))
    if n_mod:
        w(f"{n_mod} modified documents indexed.")
    else:
        w("None found in the crawled archive views — the `modified` flag is live but unused; "
          "if the SEC exposes vision-impaired versions elsewhere, they were not enumerated.")
    w("")
    w("## Fileid-vs-subject cross-check")
    code_map = defaultdict(set)
    for d in decoded:
        m2 = FILEID_RE.match(d["fileid"])
        if m2:
            code_map[(d["exam"], m2.group(2))].add(d["effName"])
    conflicts = {k: v for k, v in code_map.items() if len(v) > 1}
    if conflicts:
        w("CONFLICTS — one SEC subject code decoding to multiple subjects (check for typo'd fileids):")
        for (exam, code), names in sorted(conflicts.items()):
            w(f"- {exam} code {code}: {sorted(names)}")
    else:
        w("Clean: every SEC subject code maps to exactly one subject per exam.")
    section("Label vs fileid LEVEL disagreements (label wins)", issues.level_disagree)
    section("Label vs fileid LANG disagreements (label wins)", issues.lang_disagree)
    section("Label vs fileid COMPONENT disagreements (label wins)", issues.component_disagree)
    section("Fileid grammar fallbacks (decoded from label only)", issues.fileid_fallback)
    section("Bilingual (BV) docs folded into 'ev'", issues.bv_lang)
    section("JC Irish rows without a T1/T2 marker (assigned to T2)", issues.jc_irish_unmarked)
    section("Extra scheme candidates (first kept)", issues.scheme_extras)
    section("Schemes with component != 000", issues.scheme_odd_component)
    section("SEC subject ids with multiple display names", issues.sec_id_renames)
    if issues.bytes_pending:
        w(f"### Byte counts pending: {issues.bytes_pending} docs emitted with `b: 0` "
          f"(Stage 2 incomplete)")
        w("")

    with open(REPORT_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(rep) + "\n")
    log(f"  wrote {os.path.relpath(REPORT_MD, REPO)} ({len(rep)} lines)")
    with open(os.path.join(OUT_DIR, "upload-manifest.jsonl"), "w") as f:
        for remote in sorted(upload_rows):
            f.write(json.dumps({"remote": remote, "local": upload_rows[remote], "year": int(remote.split("/")[3])}) + "\n")
    log(f"  wrote upload-manifest.jsonl ({len(upload_rows)} objects)")
    # Answer sidecars upload separately (content-type application/json, not PDF).
    with open(os.path.join(OUT_DIR, "answers-upload-manifest.jsonl"), "w") as f:
        for remote in sorted(answer_upload_rows):
            f.write(json.dumps({"remote": remote, "local": answer_upload_rows[remote], "year": int(remote.split("/")[3])}) + "\n")
    n_flagged = sum(1 for es in index.values() for e in es for p in e["papers"] if p.get("answers"))
    log(f"  wrote answers-upload-manifest.jsonl ({len(answer_upload_rows)} sidecars; "
        f"{n_flagged} papers flagged answers:1)")
    log("DONE")
    return 0


if __name__ == "__main__":
    sys.exit(main())
