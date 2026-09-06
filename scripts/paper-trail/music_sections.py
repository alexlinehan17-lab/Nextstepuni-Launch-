#!/usr/bin/env python3
"""Music (LC067) answer maps — component-banded bespoke.

The single Music scheme bundles COMPOSING (component 006), LISTENING (008) and
elective material, and each component restarts Q1..N — which is why the generic
engine mis-bands or drops these papers (and why 2026's composing chips once
opened listening answers). The reliable structure is the RUNNING PAGE HEADER:
every scheme page names its component ("… Marking Scheme Composing – Higher
level – Core", "Listening - Higher Level – Core", Irish "Cumadóireacht" /
"Éisteacht"). So:

  1. Band the scheme by running-header keyword, EXCLUDING elective pages.
  2. Within the band, find question starts by any of the observed marker styles:
       'Q.N TITLE' headers (composing, 2010s), a leading 'Q N' pair opening a
       per-question marks table (listening), 'C.N' section heads (2018-era),
       or restated 'Question N' blocks (2020s).
  3. Chip regions run marker → next marker / band end. Count-reconcile against
     the paper's detected questions; drop on any mismatch.

Usage: python3 music_sections.py <years...>   (corpus + answers/ layout paths)
Writes sidecars only for (paper, scheme) pairs that fully reconcile.
"""
import json
import os
import re
import sys
import unicodedata
from collections import defaultdict

import fitz

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
CORPUS = os.path.join(REPO, "paper-trail-corpus")
ANSWERS = os.path.join(HERE, "answers")

SIDECAR_V = 1
COPYRIGHT = "© State Examinations Commission"
MAX_REGION_PAGES = 6

COMPONENT_WORDS = {
    "006": ("composing", "cumad"),      # Cumadóireacht
    "008": ("listening", "éisteacht", "eisteacht"),
}
ELECTIVE_WORDS = ("elective", "roghnach")

# These two 2017 Irish schemes are image-only scans.  Their English and Irish
# editions were rendered side by side and have the same page/table geometry.
# The coordinates below are the starts of the six matching Irish table blocks,
# not OCR guesses.
AUDITED_SCANNED_SCHEME_LAYOUTS = {
    (2017, "LC067ALP000IV.pdf", "008"): {
        "band": (9, 17),
        "markers": {
            1: (10, 0.0715),
            2: (11, 0.0664),
            3: (12, 0.0514),
            4: (13, 0.0868),
            5: (14, 0.0914),
            6: (16, 0.0685),
        },
    },
    (2017, "LC067GLP000IV.pdf", "008"): {
        "band": (8, 15),
        "markers": {
            1: (9, 0.0715),
            2: (10, 0.0978),
            3: (11, 0.0514),
            4: (12, 0.0677),
            5: (13, 0.0913),
            6: (14, 0.0915),
        },
    },
}

# The 2010 Higher English composing scheme omits Q3's number from its PDF text
# layer.  A direct render places Q3 at the top border of the page-4 table.
AUDITED_SCHEME_MARKERS = {
    (2010, "LC067ALP000EV.pdf", "006"): {3: (3, 0.0698)},
}

RECOVERED_BOOKLETS = {
    "LC067ALP006EV.pdf": {2010, 2012, 2026},
    "LC067ALP006IV.pdf": {2012, 2026},
    "LC067GLP006EV.pdf": {2012, 2026},
    "LC067GLP006IV.pdf": {2012, 2026},
    "LC067ALP008EV.pdf": {2010, 2012, 2014, 2015, 2016, 2017, 2021, 2022, 2023},
    "LC067ALP008IV.pdf": {2012, 2017, 2021},
    "LC067GLP008EV.pdf": {2011, 2012, 2017, 2023, 2025},
    "LC067GLP008IV.pdf": {2011, 2012, 2017},
}


def page_header_text(page):
    H = page.rect.height
    words = [w[4] for w in page.get_text("words") if w[1] < H * 0.12]
    return " ".join(words).lower()


def normalized_text(value):
    return unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode().lower()


def page_probe_text(page):
    return normalized_text(" ".join(page.get_text().split())[:900])


def effectively_blank(page):
    return len(re.sub(r"\W", "", page.get_text())) < 20


def component_band(scheme, comp):
    keys = COMPONENT_WORDS[comp]
    pages = []
    for pi in range(len(scheme)):
        hdr = normalized_text(page_header_text(scheme[pi]))
        if (any(normalized_text(k) in hdr for k in keys)
                and not any(normalized_text(e) in hdr for e in ELECTIVE_WORDS)):
            pages.append(pi)
    if not pages:
        return None
    lo = min(pages)
    if comp == "006":
        stop_words = (
            "elective", "roghnach", "listening", "eisteacht",
            "general notes to examiners", "notai ginearalta do scrudaitheoiri",
        )
    else:
        stop_words = (
            "elective", "roghnach", "audio acknowledg", "admhala fuaime",
            "marking schemes and assessment criteria",
            "sceimeanna marcala agus crit",
        )
    hi = len(scheme)
    for pi in range(lo + 1, len(scheme)):
        probe = page_probe_text(scheme[pi])
        if any(normalized_text(word) in probe for word in stop_words):
            hi = pi
            break
    while hi > lo and effectively_blank(scheme[hi - 1]):
        hi -= 1
    return lo, hi  # [lo, hi)


def lines_of(page):
    lines = defaultdict(list)
    for w in page.get_text("words"):
        lines[(w[5], w[6])].append(w)
    out = []
    H = page.rect.height
    for k in sorted(lines):
        lw = sorted(lines[k], key=lambda w: w[0])
        out.append((" ".join(w[4] for w in lw), lw[0][0], lw[0][1] / H))
    out.sort(key=lambda t: t[2])
    return out


def scheme_markers(scheme, lo, hi):
    """{n: (page0, yFrac)} across the band, first occurrence, any style."""
    seen = {}
    for pi in range(lo, hi):
        for txt, x0, y in lines_of(scheme[pi]):
            m = re.match(r"^(?:Question|Ceist)\s+(\d{1,2})\b", txt, re.I)
            if m is None:
                if x0 > 150:
                    continue
                m = (re.match(r"^Q\.?\s*(\d{1,2})\b", txt)
                     or re.match(r"^C\.?\s*(\d{1,2})\b", txt))
            if m:
                n = int(m.group(1))
                if 1 <= n <= 20 and n not in seen:
                    seen[n] = (pi, y)
        # 'Q' and its number can extract as ADJACENT one-word lines (the 2015
        # listening tables): pair a lone left-margin 'Q' with the nearest digit
        # word just right/below it.
        # Table style (2015-era listening): the page is one question's marks
        # table; 'Q' heads a column and the question number sits in that column
        # far below. Take the topmost lone digit in the leftmost column as the
        # page's question number.
        H = scheme[pi].rect.height
        words = sorted(scheme[pi].get_text("words"), key=lambda w: w[1])
        hdr_has_q = any(w[4] in ("Q", "C") and w[0] < 80 for w in words[:24])
        if hdr_has_q:
            for w in words:
                if (re.fullmatch(r"\d{1,2}", w[4]) and w[0] < 75
                        and w[1] > H * 0.08):
                    n = int(w[4])
                    if 1 <= n <= 20 and n not in seen:
                        seen[n] = (pi, 0.0)
                    break
        # Some schemes carry the number only in the first merged table cell.
        # A single-question table begins at its outer border even when the PDF
        # vertically centres that number; multi-question tables begin each
        # later question at its own row border.
        for table in scheme[pi].find_tables().tables:
            rows = table.extract()
            header = " ".join(
                str(value or "").replace("\xa0", " ").strip()
                for row in rows[:3] for value in row
            )
            if not re.search(r"(^|\s)(?:Q|C)(?:\s|$)", header, re.I):
                continue
            matches = []
            for row_index, values in enumerate(rows):
                first = ""
                first_column = None
                for column_index, value in enumerate(values):
                    if value is not None and str(value).strip():
                        first = str(value).replace("\xa0", " ").strip()
                        first_column = column_index
                        break
                match = re.fullmatch(
                    r"(?:(?:Q|C)\.?\s*)?(\d{1,2})\s*A?", first, re.I,
                )
                if match and first_column is not None and first_column <= 1:
                    number = int(match.group(1))
                    if 1 <= number <= 20:
                        matches.append((row_index, number))
            distinct = list(dict.fromkeys(number for _, number in matches))
            for row_index, number in matches:
                if number in seen:
                    continue
                y = (table.bbox[1] if len(distinct) == 1
                     else table.rows[row_index].bbox[1])
                seen[number] = (pi, round(y / H, 4))
    return seen


def align_markers_to_table_rows(scheme, markers):
    """Move extracted question-number text to its enclosing table-row start.

    SEC listening tables commonly merge the question-number cell over several
    answer rows. PDF text extraction then places the number near the vertical
    middle of the merged cell, which is not the start of the answer. A table's
    first question starts at the table border; later questions in that table
    start at their own row border. Markers that cannot be tied unambiguously to
    a numeric first cell are left unchanged.
    """
    aligned = dict(markers)
    by_page = defaultdict(list)
    for number, (page_index, _) in markers.items():
        by_page[page_index].append(number)

    for page_index, numbers in by_page.items():
        page = scheme[page_index]
        height = page.rect.height
        for table in page.find_tables().tables:
            matches = []
            for number in numbers:
                for row_index, values in enumerate(table.extract()):
                    first = next(
                        (
                            str(value).replace("\xa0", " ").strip()
                            for value in values
                            if value is not None and str(value).strip()
                        ),
                        "",
                    )
                    matched = re.fullmatch(
                        rf"(?:(?:Q|C)\.?\s*)?{number}\s*A?", first, re.I,
                    )
                    if matched:
                        matches.append((row_index, number))
                        break
            matches.sort()
            distinct = list(dict.fromkeys(number for _, number in matches))
            for match_index, (row_index, number) in enumerate(matches):
                begins_table = len(distinct) == 1 or (match_index == 0 and row_index <= 2)
                y = table.bbox[1] if begins_table else table.rows[row_index].bbox[1]
                aligned[number] = (page_index, round(y / height, 4))
    return aligned


def paper_questions(paper):
    seen = {}
    for pi in range(len(paper)):
        for txt, x0, y in lines_of(paper[pi]):
            m = (re.match(r"^(?:Question|Ceist)\s+(\d{1,2})\b", txt, re.I)
                 or re.match(r"^Q\.?\s*(\d{1,2})\b", txt)
                 or re.match(r"^(\d{1,2})\.\s", txt))
            if m and x0 < 150:
                n = int(m.group(1))
                if 1 <= n <= 20 and n not in seen:
                    seen[n] = (pi, y)
    return seen


def region_between(start, end, hi):
    (sp, sy), e = start, end if end else (hi, 0.0)
    ep, ey = e
    segs = []
    if ep == sp:
        if ey <= sy:
            return None
        return [{"p": sp + 1, "r": [0.0, round(sy, 4), 1.0, round(ey, 4)]}]
    segs.append({"p": sp + 1, "r": [0.0, round(sy, 4), 1.0, 1.0]})
    for p in range(sp + 1, min(ep, sp + MAX_REGION_PAGES - 1)):
        segs.append({"p": p + 1, "r": [0.0, 0.0, 1.0, 1.0]})
    if ep < sp + MAX_REGION_PAGES - 1 and ey > 0.02:
        segs.append({"p": ep + 1, "r": [0.0, 0.0, 1.0, round(ey, 4)]})
    return segs


def build(paper_path, scheme_path, comp, year):
    paper, scheme = fitz.open(paper_path), fitz.open(scheme_path)
    layout_key = (year, os.path.basename(scheme_path), comp)
    audited_layout = AUDITED_SCANNED_SCHEME_LAYOUTS.get(layout_key)
    band = audited_layout["band"] if audited_layout else component_band(scheme, comp)
    if not band:
        return None, "no component band in scheme"
    lo, hi = band
    anchor_path = os.path.join(
        REPO, "public", "paper-anchors", str(year),
        f"{os.path.basename(paper_path)}.json",
    )
    pq = {}
    if os.path.exists(anchor_path):
        anchor = json.load(open(anchor_path))
        for question in anchor.get("q", []):
            if str(question.get("n", "")).isdigit():
                pq[int(question["n"])] = (
                    int(question["pP"]) - 1,
                    float(question["pY"][0]),
                )
    if not pq:
        pq = paper_questions(paper)
    ns = sorted(pq)
    if not ns or ns != list(range(1, len(ns) + 1)):
        return None, f"paper questions not 1..N: {ns}"
    ppts = [pq[n] for n in ns]
    if any(b <= a for a, b in zip(ppts, ppts[1:])):
        return None, "paper anchors not monotonic (decoy numbering)"
    sm = (dict(audited_layout["markers"]) if audited_layout
          else scheme_markers(scheme, lo, hi))
    sm.update(AUDITED_SCHEME_MARKERS.get(layout_key, {}))
    missing = [n for n in ns if n not in sm]
    if missing:
        # Rescue: 2017+ Composing sets its tables with the question number as
        # a LONE DIGIT cell ('5'), which no head pattern matches. A lone digit
        # counts only when it falls in the monotonic SLOT between its
        # neighbours' markers — a page number or marks value cannot.
        for n in list(missing):
            lo_pt = sm.get(n - 1, (lo - 1, 1.0))
            hi_pt = sm.get(n + 1, (hi, 0.0))
            for pi in range(max(lo, lo_pt[0]), min(hi, hi_pt[0] + 1)):
                hit = None
                for txt, x0, y in lines_of(scheme[pi]):
                    if txt.replace("\xa0", " ").strip() == str(n) and x0 < 260:
                        cand = (pi, y)
                        if lo_pt < cand < hi_pt:
                            hit = cand
                            break
                if hit:
                    sm[n] = hit
                    missing.remove(n)
                    break
    if missing:
        return None, f"scheme markers missing {missing} in band {lo}-{hi}"
    sm = align_markers_to_table_rows(scheme, sm)
    pts = [sm[n] for n in ns]
    if any(b <= a for a, b in zip(pts, pts[1:])):
        return None, "scheme markers not monotonic in band"
    qs = []
    for i, n in enumerate(ns):
        nxt = sm[ns[i + 1]] if i + 1 < len(ns) else None
        segs = region_between(sm[n], nxt, hi)
        if not segs:
            return None, f"empty region Q{n}"
        p_pi, p_y = pq[n]
        nxt_p = pq[ns[i + 1]] if i + 1 < len(ns) else (len(paper), 1.0)
        py1 = nxt_p[1] if nxt_p[0] == p_pi else 1.0
        qs.append({"n": str(n), "pP": p_pi + 1,
                   "pY": [round(p_y, 4), round(py1, 4)],
                   "region": segs, "mode": "crop", "conf": 1.0})
    sidecar = {"v": SIDECAR_V, "paperFileid": os.path.basename(paper_path),
               "schemeFileid": os.path.basename(scheme_path),
               "component": comp, "band": [lo + 1, hi + 1],
               "copyright": COPYRIGHT, "q": qs}
    return sidecar, None


def main():
    check_recovered = "--check-recovered" in sys.argv[1:]
    refresh_recovered = "--refresh-recovered" in sys.argv[1:]
    flags = {"--check-recovered", "--refresh-recovered"}
    years = [int(y) for y in sys.argv[1:] if y not in flags] or list(range(2010, 2027))
    ok = drop = 0
    checked = mismatched = 0
    for year in years:
        for lvl in "AG":
            for comp in ("006", "008"):
                for lang in ("EV", "IV"):
                    f = f"LC067{lvl}LP{comp}{lang}.pdf"
                    if ((check_recovered or refresh_recovered)
                            and year not in RECOVERED_BOOKLETS.get(f, set())):
                        continue
                    s = f"LC067{lvl}LP000{lang}.pdf"
                    pp = os.path.join(CORPUS, "exampapers", str(year), f)
                    sp = os.path.join(CORPUS, "markingschemes", str(year), s)
                    if not (os.path.exists(pp) and os.path.exists(sp)):
                        continue
                    dst = os.path.join(ANSWERS, str(year), f"{f}.json")
                    if os.path.exists(dst) and not (check_recovered or refresh_recovered):
                        continue  # committed (earlier verified maps stay)
                    sidecar, err = build(pp, sp, comp, year)
                    if sidecar is None:
                        print(f"DROP {year} {lvl} {comp} {lang}: {err}")
                        drop += 1
                        continue
                    if check_recovered:
                        checked += 1
                        stored = json.load(open(dst)) if os.path.exists(dst) else None
                        if stored != sidecar:
                            print(f"MISMATCH {year} {lvl} {comp} {lang}")
                            mismatched += 1
                        continue
                    os.makedirs(os.path.dirname(dst), exist_ok=True)
                    json.dump(sidecar, open(dst, "w"), sort_keys=True,
                              separators=(",", ":"))
                    print(f"OK   {year} {lvl} {comp} {lang}: {len(sidecar['q'])} q")
                    ok += 1
    if check_recovered:
        print(json.dumps({"checked": checked, "mismatched": mismatched}))
        if checked != 29 or mismatched:
            raise SystemExit(1)
        return
    print(f"\nmapped {ok} · dropped {drop}")


if __name__ == "__main__":
    main()
