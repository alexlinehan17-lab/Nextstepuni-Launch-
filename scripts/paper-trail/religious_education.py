#!/usr/bin/env python3
"""Build complete paper-only section anchors for LC Religious Education.

The generic Paper Trail detector can see only the numbered questions in
Section A. Sections B-J are headed by a letter and would otherwise disappear
from Topic Atlas. This subject-specific pass detects the official section
headers in the entitled local SEC papers, emits one stable card per printed
section, and stages matching hosted paper-only anchors.

No StudyClix question text, image, solution, mock paper, or PDF is read here.
The committed StudyClix audit contributes factual year/topic coverage only;
all crop coordinates are independently derived from local SEC PDFs.

Run from the repository root:
    python3 scripts/paper-trail/religious_education.py
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import fitz


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
CORPUS = ROOT / "paper-trail-corpus" / "exampapers"
INDEX_PATH = ROOT / "paperTrailData.ts"
TAGS_PATH = HERE / "topic-tags" / "tags" / "religious-education.json"
BASELINE_PATH = ROOT / "test" / "fixtures" / "religiousEducationTopicQuestionBaseline.json"
HOSTED_ROOT = ROOT / "public" / "paper-anchors"

COPYRIGHT = "© State Examinations Commission"
SECTION_PATTERN = re.compile(r"^(?:SECTION|CTION|ROINN|OINN|INN)([A-J])")


def paper_index() -> list[dict]:
    source = INDEX_PATH.read_text()
    match = re.search(
        r'  "religious-education": (\[[\s\S]*?\n  \]),\n  "romanian":',
        source,
    )
    if not match:
        raise RuntimeError("Could not locate Religious Education in paperTrailData.ts")
    # The generated TypeScript array has a legal trailing comma; remove it for
    # Python's strict JSON parser.
    return json.loads(re.sub(r",\s*]$", "]", match.group(1)))


def expected_page(letter: str, page_number: int) -> bool:
    if letter == "A":
        return page_number == 2
    if letter in "BCD":
        return page_number == 3
    return page_number in (4, 5)


def section_anchors(pdf_path: Path) -> dict[str, tuple[int, float]]:
    """Return independently verified (one-based page, y-fraction) headers."""
    anchors: dict[str, tuple[int, float]] = {}
    with fitz.open(pdf_path) as document:
        for page_number, page in enumerate(document, start=1):
            for block in page.get_text("dict")["blocks"]:
                for line in block.get("lines", []):
                    x0, y0, *_ = line["bbox"]
                    if x0 > 140:
                        continue
                    text = "".join(span["text"] for span in line.get("spans", []))
                    compact = re.sub(r"[^A-Za-z]", "", text).upper()
                    match = SECTION_PATTERN.match(compact)
                    if not match:
                        continue
                    letter = match.group(1)
                    if not expected_page(letter, page_number):
                        continue
                    anchors.setdefault(letter, (page_number, round(y0 / page.rect.height, 4)))

    if set("ABCD") - anchors.keys():
        raise RuntimeError(f"{pdf_path}: missing compulsory section headers")
    optional = sorted(set(anchors) & set("EFGHIJ"))
    if len(optional) != 4:
        raise RuntimeError(
            f"{pdf_path}: expected four printed optional sections, found {optional}"
        )

    ordered = [anchors[letter] for letter in sorted(anchors)]
    if ordered != sorted(ordered):
        raise RuntimeError(f"{pdf_path}: non-monotonic section anchors")
    return anchors


def identity(item: dict) -> str:
    return "|".join(
        [
            item["level"],
            item["lang"],
            str(item["year"]),
            item["paperKey"],
            item["fileid"],
        ]
    )


def main() -> None:
    entries = paper_index()
    papers: list[dict] = []
    hosted_maps: list[tuple[int, str, dict]] = []
    section_sets_by_year: dict[int, set[str]] = {}

    for entry in entries:
        if len(entry["papers"]) != 1:
            raise RuntimeError(
                f"{entry['year']} {entry['level']} {entry['lang']}: expected one paper"
            )
        item = entry["papers"][0]
        fileid = item["doc"]["f"]
        paper_path = CORPUS / str(entry["year"]) / fileid
        if not paper_path.exists():
            raise FileNotFoundError(paper_path)
        anchors = section_anchors(paper_path)
        letters = sorted(anchors)

        prior = section_sets_by_year.setdefault(entry["year"], set(letters))
        if prior != set(letters):
            raise RuntimeError(
                f"{entry['year']}: translated/level editions disagree on sections "
                f"{sorted(prior)} != {letters}"
            )

        questions = [
            {
                "n": str(number),
                "primary": f"religious-education-{ord(letter) - ord('A')}-0",
            }
            for number, letter in enumerate(letters, start=1)
        ]
        paper = {
            "subjectId": "religious-education",
            "level": entry["level"],
            "lang": entry["lang"],
            "year": entry["year"],
            "fileid": fileid,
            "paperKey": "single",
            "q": questions,
        }
        papers.append(paper)

        hosted_questions = []
        for number, letter in enumerate(letters, start=1):
            page_number, y_fraction = anchors[letter]
            question = {
                "n": str(number),
                "pP": page_number,
                "pY": [y_fraction, 1],
                "region": [{"p": 1}],
                "mode": "pagejump",
                "conf": 0.5,
                "label": f"Section {letter}",
                "printOrder": number,
            }
            if number < len(letters):
                next_page, _ = anchors[letters[number]]
                # Every printed section ends on its own page before the next
                # page's section header. Without this explicit boundary the
                # generic next-anchor derivation would append the next page's
                # instructions/header to the preceding card.
                if next_page > page_number:
                    question["endP"] = page_number
                    question["endY"] = 1
            hosted_questions.append(question)
        hosted_maps.append(
            (
                entry["year"],
                fileid,
                {
                    "v": 1,
                    "paperFileid": fileid,
                    "schemeFileid": "",
                    "component": "000",
                    "band": [1, 1],
                    "copyright": COPYRIGHT,
                    "paperOnly": 1,
                    "q": hosted_questions,
                },
            )
        )

    paper_ids = [identity(paper) for paper in papers]
    duplicates = sorted({item for item in paper_ids if paper_ids.count(item) > 1})
    if duplicates:
        raise RuntimeError(f"Duplicate Religious Education variants: {duplicates}")

    baseline = json.loads(BASELINE_PATH.read_text())
    baseline_cards = 0
    for expected in baseline:
        live = next((paper for paper in papers if identity(paper) == identity(expected)), None)
        if live is None:
            raise RuntimeError(f"Preservation failure: missing {identity(expected)}")
        live_numbers = {question["n"] for question in live["q"]}
        missing = set(expected["questions"]) - live_numbers
        if missing:
            raise RuntimeError(
                f"Preservation failure: {identity(expected)} missing {sorted(missing)}"
            )
        baseline_cards += len(expected["questions"])

    TAGS_PATH.write_text(json.dumps(papers, indent=1, ensure_ascii=False) + "\n")
    for year, fileid, anchor_map in hosted_maps:
        target_dir = HOSTED_ROOT / str(year)
        target_dir.mkdir(parents=True, exist_ok=True)
        (target_dir / f"{fileid}.json").write_text(
            json.dumps(anchor_map, ensure_ascii=False, separators=(",", ":")) + "\n"
        )

    print(
        json.dumps(
            {
                "paperVariants": len(papers),
                "cards": sum(len(paper["q"]) for paper in papers),
                "hostedAnchorMaps": len(hosted_maps),
                "preservedBaselineVariants": len(baseline),
                "preservedBaselineCards": baseline_cards,
                "sectionRotations": {
                    str(year): "".join(sorted(letters))
                    for year, letters in sorted(section_sets_by_year.items())
                },
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
