#!/usr/bin/env python3
# Copyright 2026 Nextstepuni
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
"""Add the Higher Geography option essays (Questions 13-24).

The original Geography import stopped at Question 12 because the option
marking scheme begins with a shared outline rubric.  The published SEC
schemes also repeat every option prompt and give its question-specific mark
breakdown, so each 80-mark essay is still an independently selectable task.

This repair is deliberately additive: Questions 1-12 and all of their saved
coordinates are retained byte-for-byte as JSON values.  A new card is written
only when the paper and marking scheme both expose one unambiguous Question
13-24 run and the prompt text overlaps strongly on both sides.

Usage:
  python3 geography_options.py --dry    # report candidates, do not write
  python3 geography_options.py          # append verified candidates
  python3 geography_options.py --check  # require every available year complete
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

import fitz


HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
CORPUS = REPO / "paper-trail-corpus"
ANSWERS = HERE / "answers"
YEARS = range(2010, 2027)
OPTION_NUMBERS = list(range(13, 25))

HEADER_RE = re.compile(r"^(?:Question\s+)?(1[3-9]|2[0-4])\.(?:\s|$)", re.I)
OPTIONS_RE = re.compile(
    r"(?:SECTION\s+3\s*[–—-]\s*OPTIONS|Questions?\s+13\s*(?:to|[–—-])\s*24)",
    re.I,
)
SCHEME_END_RE = re.compile(r"^(?:Geographical Investigation|Appendix\s+1)\b", re.I)
WORD_RE = re.compile(r"[a-z]{3,}")
STOPWORDS = {
    "and", "are", "for", "from", "have", "into", "one", "that", "the", "their",
    "these", "this", "three", "two", "which", "with", "you", "your",
    "certificate", "examination", "geography", "higher", "leaving", "level", "marks",
    "page", "part",
}


def paper_fileid(year: int) -> str:
    return "LC005ALP043EV.pdf" if year >= 2020 else "LC005ALP000EV.pdf"


def scheme_fileid(_year: int) -> str:
    return "LC005ALP000EV.pdf"


def lines(page: fitz.Page):
    height = page.rect.height
    result = []
    for block in page.get_text("dict")["blocks"]:
        if block.get("type") != 0:
            continue
        for line in block.get("lines", []):
            text = "".join(span["text"] for span in line.get("spans", [])).strip()
            if text:
                result.append((text, line["bbox"][0], line["bbox"][1] / height))
    result.sort(key=lambda item: (item[2], item[1]))
    return result


def options_start(document: fitz.Document) -> int | None:
    matches = []
    for page_index in range(document.page_count):
        if OPTIONS_RE.search(document[page_index].get_text("text")):
            matches.append(page_index)
    # The paper cover can repeat the section title in its contents table.  The
    # final occurrence is the real divider immediately before Question 13.
    return matches[-1] if matches else None


def collect_headers(document: fitz.Document, start_page: int):
    found: dict[int, list[tuple[int, float, str]]] = {number: [] for number in OPTION_NUMBERS}
    for page_index in range(start_page, document.page_count):
        for text, x0, y_fraction in lines(document[page_index]):
            if page_index > start_page and SCHEME_END_RE.match(text):
                return found
            match = HEADER_RE.match(text)
            if match and x0 < 240:
                found[int(match.group(1))].append((page_index, round(y_fraction, 4), text))
    return found


def reconcile(found, side: str):
    problems = []
    positions = {}
    for number in OPTION_NUMBERS:
        candidates = found[number]
        if len(candidates) != 1:
            rendered = ", ".join(f"p{page + 1}@{y:.4f}:{text!r}" for page, y, text in candidates)
            problems.append(f"{side} Q{number}: expected one header, found {len(candidates)} [{rendered}]")
        else:
            positions[number] = candidates[0][:2]
    if problems:
        return None, problems
    ordered = [positions[number] for number in OPTION_NUMBERS]
    if any(ordered[index] >= ordered[index + 1] for index in range(len(ordered) - 1)):
        return None, [f"{side}: option headers are not strictly monotonic"]
    return positions, []


def scheme_end(document: fitz.Document, start: tuple[int, float]):
    start_page, start_y = start
    for page_index in range(start_page, document.page_count):
        for text, _x0, y_fraction in lines(document[page_index]):
            if (page_index, y_fraction) <= (start_page, start_y):
                continue
            if SCHEME_END_RE.match(text):
                return page_index, round(y_fraction, 4)
    return start_page, 1.0


def region_between(start: tuple[int, float], end: tuple[int, float]):
    start_page, start_y = start
    end_page, end_y = end
    segments = []
    for page_index in range(start_page, end_page + 1):
        top = start_y if page_index == start_page else 0.0
        bottom = end_y if page_index == end_page else 1.0
        if bottom > top + 0.001:
            segments.append({
                "p": page_index + 1,
                "r": [0.0, round(top, 4), 1.0, round(bottom, 4)],
            })
    return segments


def region_text(document: fitz.Document, region) -> str:
    chunks = []
    for segment in region:
        page = document[segment["p"] - 1]
        width, height = page.rect.width, page.rect.height
        x0, y0, x1, y1 = segment["r"]
        chunks.append(page.get_text(
            "text",
            clip=fitz.Rect(x0 * width, y0 * height, x1 * width, y1 * height),
        ))
    return "\n".join(chunks)


def words(text: str):
    return {word for word in WORD_RE.findall(text.lower()) if word not in STOPWORDS}


def overlap(left: str, right: str) -> float:
    left_words = words(left)
    right_words = words(right)
    if not left_words or not right_words:
        return 0.0
    return len(left_words & right_words) / min(len(left_words), len(right_words))


def expand_band_to_regions(data):
    """Keep the half-open scheme band large enough for every preserved crop."""
    pages = [
        segment["p"]
        for question in data.get("q", [])
        for key in ("region", "schemeRegion")
        for segment in question.get(key, [])
    ]
    if not pages:
        return False
    required_hi = max(pages) + 1
    if data["band"][1] >= required_hi:
        return False
    data["band"][1] = required_hi
    return True


def build_year(year: int, write: bool):
    paper_id = paper_fileid(year)
    scheme_id = scheme_fileid(year)
    paper_path = CORPUS / "exampapers" / str(year) / paper_id
    scheme_path = CORPUS / "markingschemes" / str(year) / scheme_id
    sidecar_path = ANSWERS / str(year) / f"{paper_id}.json"
    if not paper_path.exists() or not scheme_path.exists() or not sidecar_path.exists():
        return "unavailable", [f"{year}: paper, scheme or base sidecar unavailable"], 0

    paper = fitz.open(paper_path)
    scheme = fitz.open(scheme_path)
    paper_start = options_start(paper)
    scheme_start = options_start(scheme)
    if paper_start is None or scheme_start is None:
        return "failed", [f"{year}: option-section boundary not found"], 0

    paper_positions, paper_problems = reconcile(collect_headers(paper, paper_start), "paper")
    scheme_positions, scheme_problems = reconcile(collect_headers(scheme, scheme_start), "scheme")
    problems = paper_problems + scheme_problems
    if problems:
        return "failed", [f"{year}: {problem}" for problem in problems], 0

    data = json.loads(sidecar_path.read_text())
    # Once any card carries an explicit printOrder the viewer requires a full,
    # unique permutation. These single-booklet papers print Q1-Q24 in numeric
    # order, so adding the missing ranks is non-destructive metadata only.
    print_order_added = False
    for question in data.get("q", []):
        if question.get("printOrder") is None:
            question["printOrder"] = int(question["n"])
            print_order_added = True
    existing_numbers = {str(question["n"]) for question in data.get("q", [])}
    option_existing = existing_numbers & {str(number) for number in OPTION_NUMBERS}
    if option_existing and len(option_existing) != len(OPTION_NUMBERS):
        return "failed", [f"{year}: partial existing option set {sorted(option_existing)}"], 0

    additions = []
    for index, number in enumerate(OPTION_NUMBERS):
        next_number = number + 1
        paper_end = paper_positions[next_number] if next_number in paper_positions else (
            paper_positions[number][0], 1.0
        )
        scheme_stop = scheme_positions[next_number] if next_number in scheme_positions else scheme_end(
            scheme,
            scheme_positions[number],
        )
        paper_region = region_between(paper_positions[number], paper_end)
        answer_region = region_between(scheme_positions[number], scheme_stop)
        score = overlap(region_text(paper, paper_region), region_text(scheme, answer_region))
        if score < 0.62:
            paper_excerpt = " ".join(region_text(paper, paper_region).split())[:180]
            scheme_excerpt = " ".join(region_text(scheme, answer_region).split())[:180]
            problems.append(
                f"{year} Q{number}: paper/scheme prompt overlap only {score:.2f}; "
                f"paper={paper_excerpt!r}; scheme={scheme_excerpt!r}"
            )
            continue
        start_page, start_y = paper_positions[number]
        first_paper_segment = paper_region[0]["r"]
        additions.append({
            "conf": round(score, 2),
            "label": f"Option essay · Q{number}",
            "mode": "crop",
            "n": str(number),
            "pP": start_page + 1,
            "pY": [round(start_y, 4), first_paper_segment[3]],
            "paperRegion": paper_region,
            "printOrder": number,
            "region": answer_region,
            "schemeRegion": answer_region,
        })

    if problems or len(additions) != len(OPTION_NUMBERS):
        return "failed", problems or [f"{year}: incomplete option run"], 0
    if option_existing:
        band_extended = expand_band_to_regions(data)
        if write and (print_order_added or band_extended):
            sidecar_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
        updates = []
        if print_order_added:
            updates.append("completed print-order metadata")
        if band_extended:
            updates.append("extended scheme band")
        qualifier = f"; {', '.join(updates)}" if updates else ""
        return "complete", [f"{year}: already complete (12 option essays){qualifier}"], 0
    if write:
        data["q"].extend(additions)
        expand_band_to_regions(data)
        sidecar_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    scores = [question["conf"] for question in additions]
    verb = "wrote" if write else "would add"
    return "added", [f"{year}: {verb} 12 option essays (overlap {min(scores):.2f}-{max(scores):.2f})"], 12


def main():
    dry = "--dry" in sys.argv
    check = "--check" in sys.argv
    write = not dry and not check
    failures = 0
    unavailable = 0
    added = 0
    for year in YEARS:
        status, messages, count = build_year(year, write)
        for message in messages:
            print(message)
        failures += status == "failed"
        unavailable += status == "unavailable"
        added += count
    print(f"years={len(YEARS)} unavailable={unavailable} failures={failures} additions={added}")
    if failures or (check and unavailable):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
