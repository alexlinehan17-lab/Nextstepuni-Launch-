#!/usr/bin/env python3
"""Complete the entitled LC Physics Paper Trail corpus through 2026.

This pass preserves every inherited card, restores the omitted Higher Q12
cards from 2011 and 2012, adds the missing 2025 Ordinary English edition, and
adds all four official 2026 editions.  It also fills paper-only crop maps and
the seven marking-scheme maps that were absent after the generic mapper.

No StudyClix question text, images, solutions, notes, mocks, or PDFs are read
or copied.  Reference-site factual headings are reconciled separately.

Run from the repository root:
    python3 scripts/paper-trail/physics.py
"""

from __future__ import annotations

import copy
import importlib.util
import json
import re
from pathlib import Path

import fitz


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
CORPUS_ROOT = ROOT / "paper-trail-corpus"
CORPUS = CORPUS_ROOT / "exampapers"
SCHEMES = CORPUS_ROOT / "markingschemes"
INDEX_PATH = ROOT / "paperTrailData.ts"
TAGS_PATH = HERE / "topic-tags" / "tags" / "physics.json"
BASELINE_PATH = ROOT / "test" / "fixtures" / "physicsTopicQuestionBaseline.json"
HOSTED_ROOT = ROOT / "public" / "paper-anchors"
HOSTED_ANSWERS_ROOT = ROOT / "public" / "paper-answers"
ANSWERS_ROOT = HERE / "answers"
ANCHOR_MAPPER_PATH = HERE / "anchor-map.py"

COPYRIGHT = "© State Examinations Commission"
EXPECTED_VARIANTS = 68
EXPECTED_CARDS = 864


# Independently reviewed from the official SEC 2026 English papers.  These are
# intentionally the two broad outgoing-syllabus nodes used by Paper Trail; the
# separate exam-topic map retains every applicable old/new practice bucket.
MANUAL_2026_TAGS: dict[tuple[str, str], dict[str, str]] = {
    ("higher", "1"): {"primary": "physics-0-5"},
    ("higher", "2"): {"primary": "physics-0-12", "secondary": "physics-0-4"},
    ("higher", "3"): {"primary": "physics-5-5", "secondary": "physics-5-10"},
    ("higher", "4"): {"primary": "physics-2-2", "secondary": "physics-2-6"},
    ("higher", "5"): {"primary": "physics-6-11", "secondary": "physics-6-10"},
    ("higher", "6"): {"primary": "physics-0-6", "secondary": "physics-6-16"},
    ("higher", "7"): {"primary": "physics-0-3", "secondary": "physics-4-4"},
    ("higher", "8"): {"primary": "physics-5-2", "secondary": "physics-5-6"},
    ("higher", "9"): {"primary": "physics-4-3", "secondary": "physics-4-2"},
    ("higher", "10"): {"primary": "physics-6-7", "secondary": "physics-6-6"},
    ("higher", "11"): {"primary": "physics-7-0", "secondary": "physics-6-15"},
    ("higher", "12"): {"primary": "physics-7-6", "secondary": "physics-7-8"},
    ("higher", "13"): {"primary": "physics-6-10", "secondary": "physics-6-17"},
    ("higher", "14"): {"primary": "physics-0-1", "secondary": "physics-7-9"},
    ("ordinary", "1"): {"primary": "physics-0-4", "secondary": "physics-0-13"},
    ("ordinary", "2"): {"primary": "physics-5-1"},
    ("ordinary", "3"): {"primary": "physics-4-3"},
    ("ordinary", "4"): {"primary": "physics-2-2", "secondary": "physics-2-6"},
    ("ordinary", "5"): {"primary": "physics-6-11", "secondary": "physics-1-1"},
    ("ordinary", "6"): {"primary": "physics-0-1", "secondary": "physics-6-10"},
    ("ordinary", "7"): {"primary": "physics-0-2", "secondary": "physics-0-4"},
    ("ordinary", "8"): {"primary": "physics-2-3", "secondary": "physics-1-0"},
    ("ordinary", "9"): {"primary": "physics-5-2", "secondary": "physics-5-3"},
    ("ordinary", "10"): {"primary": "physics-6-8", "secondary": "physics-6-11"},
    ("ordinary", "11"): {"primary": "physics-3-1", "secondary": "physics-3-2"},
    ("ordinary", "12"): {"primary": "physics-7-4", "secondary": "physics-7-0"},
    ("ordinary", "13"): {"primary": "physics-4-0", "secondary": "physics-4-1"},
    ("ordinary", "14"): {"primary": "physics-0-6", "secondary": "physics-6-16"},
}


# The generic scheme detector found every other Physics map.  These seven
# schemes use attached punctuation ("12.(a)" / "14(a)") or, in 2012, a
# different header style.  Page starts and terminal pages were visually
# reviewed in both official-language editions before being pinned here.
MANUAL_SCHEME_PAGES: dict[tuple[int, str], tuple[list[int], int]] = {
    (2012, "LC021ALP000EV.pdf"): (
        [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
        15,
    ),
    (2024, "LC021ALP000EV.pdf"): (
        [6, 7, 8, 9, 10, 11, 13, 14, 15, 16, 17, 18, 20, 21],
        22,
    ),
    (2024, "LC021ALP000IV.pdf"): (
        [6, 7, 8, 9, 10, 11, 13, 14, 15, 16, 17, 18, 20, 21],
        22,
    ),
    (2025, "LC021ALP000EV.pdf"): (
        [6, 7, 8, 9, 10, 11, 13, 14, 15, 16, 17, 18, 20, 22],
        25,
    ),
    (2025, "LC021ALP000IV.pdf"): (
        [6, 7, 8, 9, 10, 11, 13, 14, 15, 16, 17, 18, 20, 22],
        25,
    ),
    (2025, "LC021GLP000EV.pdf"): (
        [6, 7, 8, 9, 10, 11, 13, 14, 15, 16, 17, 18, 19, 20],
        23,
    ),
    (2025, "LC021GLP000IV.pdf"): (
        [6, 7, 8, 9, 10, 11, 13, 14, 15, 16, 17, 18, 19, 20],
        23,
    ),
}


def clean(text: str) -> str:
    return re.sub(r"\s+", " ", text.replace("\u00a0", " ")).strip()


def paper_index() -> list[dict]:
    source = INDEX_PATH.read_text()
    match = re.search(
        r'  "physics": (\[[\s\S]*?\n  \]),\n  "physics-and-chemistry":',
        source,
    )
    if not match:
        raise RuntimeError("Could not locate Physics in paperTrailData.ts")
    return json.loads(re.sub(r",\s*]$", "]", match.group(1)))


def identity(item: dict) -> str:
    return "|".join(
        [
            item["level"],
            item["lang"],
            str(item["year"]),
            item.get("paperKey", "single"),
            item["fileid"],
        ]
    )


def expected_numbers(year: int) -> list[str]:
    final = 12 if year <= 2020 else 14
    return [str(number) for number in range(1, final + 1)]


def load_anchor_mapper():
    spec = importlib.util.spec_from_file_location("paper_trail_anchor_map", ANCHOR_MAPPER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load {ANCHOR_MAPPER_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def is_paper_tail(page: fitz.Page) -> bool:
    text = clean(page.get_text("text")).casefold()
    if not text:
        return True
    return any(
        marker in text
        for marker in (
            "acknowledgements",
            "acknowledgments",
            "admhálacha",
            "blank page",
            "this page is intentionally blank",
            "this page has been left blank",
            "there is no examination material",
            "do not hand this up",
            "ná tabhair suas é seo",
        )
    )


def paper_anchors(
    document: fitz.Document,
    pdf_path: Path,
    wanted: list[str],
    anchor_mapper,
) -> tuple[list[dict], tuple[int, float]]:
    detected = anchor_mapper.detect_paper_headers(document)
    if detected is None:
        raise RuntimeError(f"{pdf_path}: no clean paper question sequence")
    detector, sequence = detected
    anchors = [
        {"n": str(number), "page": page0 + 1, "y": round(y_fraction, 4)}
        for number, page0, _x, y_fraction in sorted(sequence)
    ]
    found = [anchor["n"] for anchor in anchors]
    if found != wanted:
        raise RuntimeError(
            f"{pdf_path}: {detector} expected Questions {wanted}, found {found}"
        )

    last_page = anchors[-1]["page"]
    tail = (len(document), 1.0)
    for page_number in range(last_page + 1, len(document) + 1):
        if is_paper_tail(document[page_number - 1]):
            tail = (max(last_page, page_number - 1), 1.0)
            break
    if tail <= (anchors[-1]["page"], anchors[-1]["y"]):
        raise RuntimeError(f"{pdf_path}: invalid final paper endpoint {tail}")
    return anchors, tail


def hosted_map(
    fileid: str,
    year: int,
    anchors: list[dict],
    tail: tuple[int, float],
) -> tuple[dict, int]:
    questions: list[dict] = []
    max_span = 0
    section_a_last = 4 if year <= 2020 else 5
    for index, anchor in enumerate(anchors):
        end = (
            (anchors[index + 1]["page"], anchors[index + 1]["y"])
            if index + 1 < len(anchors)
            else tail
        )
        start = (anchor["page"], anchor["y"])
        if end <= start:
            raise RuntimeError(f"{fileid} Q{anchor['n']}: invalid crop endpoint")
        span = end[0] - start[0]
        max_span = max(max_span, span)
        number = int(anchor["n"])
        questions.append(
            {
                "n": anchor["n"],
                "pP": anchor["page"],
                "pY": [anchor["y"], 1],
                "region": [{"p": 1}],
                "mode": "pagejump",
                "conf": 0.5,
                "label": (
                    f"Section {'A' if number <= section_a_last else 'B'}"
                    f" · Question {number}"
                ),
                "printOrder": index + 1,
                "endP": end[0],
                "endY": end[1],
            }
        )
    if max_span > 10:
        raise RuntimeError(f"{fileid}: implausible paper question span {max_span}")
    return {
        "v": 1,
        "paperFileid": fileid,
        "schemeFileid": "",
        "component": "000",
        "band": [1, 1],
        "copyright": COPYRIGHT,
        "paperOnly": 1,
        **({"maxCropPages": max_span} if max_span > 3 else {}),
        "q": questions,
    }, max_span


def line_records(page: fitz.Page) -> list[tuple[str, float, float]]:
    records: list[tuple[str, float, float]] = []
    for block in page.get_text("dict")["blocks"]:
        for line in block.get("lines", []):
            text = clean(" ".join(span["text"] for span in line.get("spans", [])))
            if text:
                records.append(
                    (
                        text,
                        line["bbox"][0] / page.rect.width,
                        line["bbox"][1] / page.rect.height,
                    )
                )
    return records


def scheme_marker_y(document: fitz.Document, page_number: int, number: int) -> float:
    patterns = (
        re.compile(rf"^Question\s*{number}\b", re.IGNORECASE),
        re.compile(rf"^{number}\s*(?:\.|\()"),
    )
    candidates = [
        y_fraction
        for text, x_fraction, y_fraction in line_records(document[page_number - 1])
        if x_fraction < 0.24 and any(pattern.match(text) for pattern in patterns)
    ]
    if not candidates:
        raise RuntimeError(
            f"Scheme page {page_number}: no reviewed marker for Question {number}"
        )
    return round(min(candidates), 4)


def manual_scheme_map(year: int, fileid: str, pages: list[int], tail_page: int) -> dict:
    scheme_path = SCHEMES / str(year) / fileid
    paper_anchor_path = HOSTED_ROOT / str(year) / f"{fileid}.json"
    if not scheme_path.exists():
        raise FileNotFoundError(scheme_path)
    if not paper_anchor_path.exists():
        raise FileNotFoundError(paper_anchor_path)

    wanted = expected_numbers(year)
    if len(pages) != len(wanted):
        raise RuntimeError(f"{scheme_path}: manual page count does not match {wanted}")
    paper_map = json.loads(paper_anchor_path.read_text())
    paper_questions = {question["n"]: question for question in paper_map["q"]}
    if list(paper_questions) != wanted:
        raise RuntimeError(f"{paper_anchor_path}: paper identities do not match {wanted}")

    with fitz.open(scheme_path) as document:
        if tail_page > len(document):
            raise RuntimeError(f"{scheme_path}: terminal page {tail_page} is out of range")
        positions = [
            (number, page_number, scheme_marker_y(document, page_number, int(number)))
            for number, page_number in zip(wanted, pages)
        ]
        if any(
            right[1:] <= left[1:]
            for left, right in zip(positions, positions[1:])
        ):
            raise RuntimeError(f"{scheme_path}: manual markers are not monotonic")

        questions: list[dict] = []
        for index, (number, start_page, start_y) in enumerate(positions):
            end_page, end_y = (
                positions[index + 1][1:]
                if index + 1 < len(positions)
                else (tail_page, 1.0)
            )
            if (end_page, end_y) <= (start_page, start_y):
                raise RuntimeError(f"{scheme_path} Q{number}: invalid crop endpoint")
            if start_page == end_page:
                region = [
                    {"p": start_page, "r": [0.0, start_y, 1.0, end_y]},
                ]
            else:
                region = [
                    {"p": start_page, "r": [0.0, start_y, 1.0, 1.0]},
                    *(
                        {"p": page, "r": [0.0, 0.0, 1.0, 1.0]}
                        for page in range(start_page + 1, end_page)
                    ),
                    {"p": end_page, "r": [0.0, 0.0, 1.0, end_y]},
                ]
            paper_question = paper_questions[number]
            questions.append(
                {
                    "n": number,
                    "pP": paper_question["pP"],
                    "pY": paper_question["pY"],
                    "region": region,
                    "mode": "crop",
                    "conf": 1.0,
                }
            )

        return {
            "v": 1,
            "paperFileid": fileid,
            "schemeFileid": fileid,
            "component": "",
            "band": [1, len(document) + 1],
            "copyright": COPYRIGHT,
            "q": questions,
        }


def main() -> None:
    entries = paper_index()
    existing = json.loads(TAGS_PATH.read_text())
    baseline = json.loads(BASELINE_PATH.read_text())
    existing_by_id = {identity(paper): paper for paper in existing}
    if len(existing_by_id) != len(existing):
        raise RuntimeError("Duplicate Physics paper identity in inherited tags")
    if len(entries) != EXPECTED_VARIANTS:
        raise RuntimeError(
            f"Expected {EXPECTED_VARIANTS} Physics index variants, found {len(entries)}"
        )

    anchor_mapper = load_anchor_mapper()
    generated_maps: list[tuple[int, str, dict]] = []
    existing_maps_verified = 0
    max_crop_span = 0
    papers: list[dict] = []

    source_2025_ordinary_iv = next(
        paper
        for paper in existing
        if paper["year"] == 2025
        and paper["level"] == "ordinary"
        and paper["lang"] == "iv"
    )

    for entry in entries:
        if entry["level"] not in {"higher", "ordinary"}:
            raise RuntimeError(f"Unexpected Physics level: {entry}")
        if len(entry["papers"]) != 1:
            raise RuntimeError(f"Unexpected Physics paper count: {entry}")
        item = entry["papers"][0]
        fileid = item["doc"]["f"]
        year = entry["year"]
        wanted = expected_numbers(year)
        paper_id = "|".join(
            [entry["level"], entry["lang"], str(year), "single", fileid]
        )
        old_paper = existing_by_id.get(paper_id)
        if old_paper is not None:
            questions = copy.deepcopy(old_paper["q"])
            numbers = [question["n"] for question in questions]
            if (
                year in {2011, 2012}
                and entry["level"] == "higher"
                and numbers == wanted[:-1]
            ):
                reviewed = {
                    "n": "12",
                    "primary": "physics-0-12" if year == 2011 else "physics-0-11",
                    "secondary": "physics-5-2",
                }
                questions.append(reviewed)
            elif numbers != wanted:
                raise RuntimeError(f"{paper_id}: inherited cards do not match {wanted}")
        elif year == 2025 and entry["level"] == "ordinary" and entry["lang"] == "ev":
            questions = copy.deepcopy(source_2025_ordinary_iv["q"])
        elif year == 2026:
            questions = []
            for number in wanted:
                tags = MANUAL_2026_TAGS.get((entry["level"], number))
                if tags is None:
                    raise RuntimeError(f"Missing reviewed 2026 tag for {paper_id} Q{number}")
                questions.append({"n": number, **copy.deepcopy(tags)})
        else:
            raise RuntimeError(f"Unexpected missing inherited Physics paper: {paper_id}")

        if [question["n"] for question in questions] != wanted:
            raise RuntimeError(f"{paper_id}: generated cards do not match {wanted}")
        papers.append(
            {
                "subjectId": "physics",
                "level": entry["level"],
                "lang": entry["lang"],
                "year": year,
                "fileid": fileid,
                "paperKey": "single",
                "q": questions,
            }
        )

        hosted_path = HOSTED_ROOT / str(year) / f"{fileid}.json"
        current = json.loads(hosted_path.read_text()) if hosted_path.exists() else None
        current_numbers = [question["n"] for question in current.get("q", [])] if current else []
        if current and current.get("paperOnly") == 1 and current_numbers == wanted:
            existing_maps_verified += 1
            continue

        paper_path = CORPUS / str(year) / fileid
        if not paper_path.exists():
            raise FileNotFoundError(paper_path)
        with fitz.open(paper_path) as document:
            anchors, tail = paper_anchors(document, paper_path, wanted, anchor_mapper)
        anchor_map, paper_span = hosted_map(fileid, year, anchors, tail)
        max_crop_span = max(max_crop_span, paper_span)
        generated_maps.append((year, fileid, anchor_map))

    paper_ids = [identity(paper) for paper in papers]
    if len(set(paper_ids)) != len(paper_ids):
        raise RuntimeError("Duplicate generated Physics paper identity")
    card_count = sum(len(paper["q"]) for paper in papers)
    if len(papers) != EXPECTED_VARIANTS or card_count != EXPECTED_CARDS:
        raise RuntimeError(
            f"Expected {EXPECTED_VARIANTS}/{EXPECTED_CARDS}, "
            f"found {len(papers)}/{card_count}"
        )

    preserved_cards = 0
    for expected in baseline:
        paper_id = identity(expected)
        old = existing_by_id.get(paper_id)
        live = next((paper for paper in papers if identity(paper) == paper_id), None)
        if old is None or live is None:
            raise RuntimeError(f"Preservation failure: missing {paper_id}")
        old_questions = {question["n"]: question for question in old["q"]}
        live_questions = {question["n"]: question for question in live["q"]}
        for number in expected["questions"]:
            if live_questions.get(number) != old_questions.get(number):
                raise RuntimeError(f"Preservation failure: changed {paper_id} Q{number}")
            preserved_cards += 1

    TAGS_PATH.write_text(json.dumps(papers, indent=1, ensure_ascii=False) + "\n")
    for year, fileid, anchor_map in generated_maps:
        target_dir = HOSTED_ROOT / str(year)
        target_dir.mkdir(parents=True, exist_ok=True)
        (target_dir / f"{fileid}.json").write_text(
            json.dumps(anchor_map, ensure_ascii=False, separators=(",", ":")) + "\n"
        )

    scheme_maps_written = 0
    scheme_maps_verified = 0
    hosted_scheme_maps_written = 0
    hosted_scheme_maps_verified = 0
    for (year, fileid), (pages, tail_page) in MANUAL_SCHEME_PAGES.items():
        answer_map = manual_scheme_map(year, fileid, pages, tail_page)
        serialized = (
            json.dumps(
                answer_map,
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
            )
            + "\n"
        )
        answer_path = ANSWERS_ROOT / str(year) / f"{fileid}.json"
        if answer_path.exists():
            if json.loads(answer_path.read_text()) != answer_map:
                raise RuntimeError(f"{answer_path}: differs from reviewed Physics map")
            scheme_maps_verified += 1
        else:
            answer_path.parent.mkdir(parents=True, exist_ok=True)
            answer_path.write_text(serialized)
            scheme_maps_written += 1

        hosted_answer_path = HOSTED_ANSWERS_ROOT / str(year) / f"{fileid}.json"
        if hosted_answer_path.exists() and hosted_answer_path.read_text() == serialized:
            hosted_scheme_maps_verified += 1
        else:
            hosted_answer_path.parent.mkdir(parents=True, exist_ok=True)
            hosted_answer_path.write_text(serialized)
            hosted_scheme_maps_written += 1

    print(
        json.dumps(
            {
                "paperVariants": len(papers),
                "physicalCards": card_count,
                "distinctStudentFacingQuestions": sum(
                    len(paper["q"]) for paper in papers if paper["lang"] == "ev"
                ),
                "hostedAnchorMapsWrittenOrRepaired": len(generated_maps),
                "hostedMapsPreservedAndVerified": existing_maps_verified,
                "reviewedSchemeMapsWritten": scheme_maps_written,
                "reviewedSchemeMapsPreservedAndVerified": scheme_maps_verified,
                "hostedReviewedSchemeMapsWritten": hosted_scheme_maps_written,
                "hostedReviewedSchemeMapsPreservedAndVerified": hosted_scheme_maps_verified,
                "preservedBaselineVariants": len(baseline),
                "preservedBaselineTasks": preserved_cards,
                "maximumGeneratedCropSpanPages": max_crop_span,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
