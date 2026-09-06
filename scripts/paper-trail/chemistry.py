#!/usr/bin/env python3
"""Complete the entitled LC Chemistry Paper Trail corpus through 2026.

This pass preserves every inherited 2010-2025 task byte-for-byte, adds the
four official 2026 editions with tags reviewed from the SEC English papers,
and fills missing hosted paper-only crop maps. Existing valid hosted maps are
verified and left untouched.

No StudyClix question text, images, solutions, notes, mocks, or PDFs are read
or copied. Reference-site factual headings are reconciled separately.

Run from the repository root:
    python3 scripts/paper-trail/chemistry.py
"""

from __future__ import annotations

import copy
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
TAGS_PATH = HERE / "topic-tags" / "tags" / "chemistry.json"
BASELINE_PATH = ROOT / "test" / "fixtures" / "chemistryTopicQuestionBaseline.json"
HOSTED_ROOT = ROOT / "public" / "paper-anchors"
ANSWERS_ROOT = HERE / "answers"

COPYRIGHT = "© State Examinations Commission"
EXPECTED_VARIANTS = 68
EXPECTED_CARDS = 748

# Two English marking schemes have complete Q1-Q11 answer runs but defeat the
# generic detector: the 2012 OL scheme labels Q4 as "SECTION B", while the 2014
# HL scheme misspells Q2 and Q4 as "QUSESTION". These exact official headings
# were visually reviewed. The final endpoints exclude the trailing blank pages.
MANUAL_SCHEME_SPECS: dict[tuple[int, str], dict] = {
    (2012, "LC022GLP000EV.pdf"): {
        "markers": [
            (1, 5, "QUESTION 1"),
            (2, 6, "QUESTION 2"),
            (3, 7, "QUESTION 3"),
            (4, 8, "SECTION B"),
            (5, 9, "QUESTION 5"),
            (6, 10, "QUESTION 6"),
            (7, 11, "QUESTION 7"),
            (8, 12, "QUESTION 8"),
            (9, 13, "QUESTION 9"),
            (10, 14, "QUESTION 10"),
            (11, 16, "QUESTION 11"),
        ],
        "tail": (17, 1.0),
    },
    (2014, "LC022ALP000EV.pdf"): {
        "markers": [
            (1, 5, "QUESTION 1"),
            (2, 7, "QUSESTION 2"),
            (3, 8, "QUESTION 3"),
            (4, 10, "QUSESTION 4"),
            (5, 12, "QUESTION 5"),
            (6, 14, "QUESTION 6"),
            (7, 16, "QUESTION 7"),
            (8, 17, "QUESTION 8"),
            (9, 19, "QUESTION 9"),
            (10, 21, "QUESTION 10"),
            (11, 23, "QUESTION 11"),
        ],
        "tail": (24, 1.0),
    },
}

# Independently reviewed from the official SEC 2026 English papers. Paper
# Trail stores two canonical outgoing-syllabus nodes; the richer exam-topic
# map retains every applicable old/new browse bucket.
MANUAL_2026_TAGS: dict[tuple[str, str], dict[str, str]] = {
    ("higher", "1"): {"primary": "chemistry-3-2", "secondary": "chemistry-2-2"},
    ("higher", "2"): {"primary": "chemistry-6-3", "secondary": "chemistry-6-2"},
    ("higher", "3"): {"primary": "chemistry-8-3", "secondary": "chemistry-8-2"},
    ("higher", "4"): {"primary": "chemistry-0-1", "secondary": "chemistry-0-4"},
    ("higher", "5"): {"primary": "chemistry-0-0", "secondary": "chemistry-1-3"},
    ("higher", "6"): {"primary": "chemistry-4-4", "secondary": "chemistry-4-3"},
    ("higher", "7"): {"primary": "chemistry-7-0", "secondary": "chemistry-7-2"},
    ("higher", "8"): {"primary": "chemistry-6-2", "secondary": "chemistry-6-1"},
    ("higher", "9"): {"primary": "chemistry-5-0", "secondary": "chemistry-5-1"},
    ("higher", "10"): {"primary": "chemistry-0-1", "secondary": "chemistry-2-2"},
    ("higher", "11"): {"primary": "chemistry-6-2", "secondary": "chemistry-0-4"},
    ("ordinary", "1"): {"primary": "chemistry-4-1", "secondary": "chemistry-6-2"},
    ("ordinary", "2"): {"primary": "chemistry-3-2", "secondary": "chemistry-3-0"},
    ("ordinary", "3"): {"primary": "chemistry-5-0", "secondary": "chemistry-5-1"},
    ("ordinary", "4"): {"primary": "chemistry-0-1", "secondary": "chemistry-0-0"},
    ("ordinary", "5"): {"primary": "chemistry-1-3", "secondary": "chemistry-1-4"},
    ("ordinary", "6"): {"primary": "chemistry-4-1", "secondary": "chemistry-6-1"},
    ("ordinary", "7"): {"primary": "chemistry-8-1", "secondary": "chemistry-8-0"},
    ("ordinary", "8"): {"primary": "chemistry-6-2", "secondary": "chemistry-6-1"},
    ("ordinary", "9"): {"primary": "chemistry-7-0", "secondary": "chemistry-2-1"},
    ("ordinary", "10"): {"primary": "chemistry-0-4", "secondary": "chemistry-0-2"},
    ("ordinary", "11"): {"primary": "chemistry-9-0", "secondary": "chemistry-11-1"},
}


def clean(text: str) -> str:
    return re.sub(r"\s+", " ", text.replace("\u00a0", " ")).strip()


def paper_index() -> list[dict]:
    source = INDEX_PATH.read_text()
    match = re.search(
        r'  "chemistry": (\[[\s\S]*?\n  \]),\n  "classical-studies":',
        source,
    )
    if not match:
        raise RuntimeError("Could not locate Chemistry in paperTrailData.ts")
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


def is_tail_boundary(text: str) -> bool:
    lowered = clean(text).lower()
    if not lowered:
        return True
    return any(
        marker in lowered
        for marker in (
            "acknowledg",
            "admhál",
            "copyright notice",
            "there is no examination material",
            "this page is intentionally blank",
            "this page has been left blank",
            "do not write on this page",
            "ná scríobh ar an leathanach seo",
        )
    )


def anchors_for(
    document: fitz.Document,
    pdf_path: Path,
) -> tuple[list[dict], tuple[int, float]]:
    expected = list(range(1, 12))
    first: dict[int, tuple[int, float]] = {}
    for page_number, page in enumerate(document, start=1):
        for text, x_fraction, y_fraction in line_records(page):
            # Chemistry's top-level headers retain a printed full stop. Requiring
            # it avoids chart/table values (for example a bare "11" in the 2024
            # Ordinary electronegativity diagram) shadowing the later Q11 header.
            match = re.match(r"^(\d{1,2})\s*\.(?:\s|$)", text)
            if match is None and x_fraction < 0.06:
                # A small number of SEC text layers drop the printed stop from
                # a standalone left-margin header (2026 Higher Q8).
                match = re.fullmatch(r"(\d{1,2})", text)
            if not match or x_fraction > 0.22 or y_fraction > 0.93:
                continue
            number = int(match.group(1))
            if number in expected:
                first.setdefault(number, (page_number, round(y_fraction, 4)))

    if set(first) != set(expected):
        raise RuntimeError(
            f"{pdf_path}: expected Questions {expected}, found {sorted(first)}"
        )
    positions = [first[number] for number in expected]
    if any(right <= left for left, right in zip(positions, positions[1:])):
        raise RuntimeError(f"{pdf_path}: non-monotonic question anchors")

    last_page = positions[-1][0]
    tail = (len(document), 0.92)
    for page_number in range(last_page + 1, len(document) + 1):
        if is_tail_boundary(document[page_number - 1].get_text("text")):
            tail = (page_number - 1, 0.92)
            break
    if tail <= positions[-1]:
        tail = (positions[-1][0], 0.95)
    if tail <= positions[-1]:
        raise RuntimeError(f"{pdf_path}: invalid final crop endpoint {tail}")

    return [
        {"n": str(number), "page": first[number][0], "y": first[number][1]}
        for number in expected
    ], tail


def hosted_map(
    fileid: str,
    anchors: list[dict],
    tail: tuple[int, float],
) -> tuple[dict, int]:
    questions: list[dict] = []
    max_span = 0
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
                "label": f"Section {'A' if number <= 3 else 'B'} · Question {number}",
                "printOrder": index + 1,
                "endP": end[0],
                "endY": end[1],
            }
        )
    if max_span > 10:
        raise RuntimeError(f"{fileid}: implausible question span {max_span}")
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


def exact_line_y(document: fitz.Document, page_number: int, marker: str) -> float:
    matches = [
        y_fraction
        for text, _x_fraction, y_fraction in line_records(document[page_number - 1])
        if clean(text).casefold() == marker.casefold()
    ]
    if len(matches) != 1:
        raise RuntimeError(
            f"Expected one {marker!r} marker on scheme page {page_number}, "
            f"found {len(matches)}"
        )
    return matches[0]


def manual_scheme_map(
    year: int,
    fileid: str,
    spec: dict,
) -> dict:
    scheme_path = SCHEMES / str(year) / fileid
    paper_anchor_path = HOSTED_ROOT / str(year) / f"{fileid}.json"
    if not scheme_path.exists():
        raise FileNotFoundError(scheme_path)
    if not paper_anchor_path.exists():
        raise FileNotFoundError(paper_anchor_path)

    paper_map = json.loads(paper_anchor_path.read_text())
    paper_questions = {int(question["n"]): question for question in paper_map["q"]}
    if sorted(paper_questions) != list(range(1, 12)):
        raise RuntimeError(f"{paper_anchor_path}: expected paper Questions 1-11")

    with fitz.open(scheme_path) as document:
        positions = [
            (number, page_number, exact_line_y(document, page_number, marker))
            for number, page_number, marker in spec["markers"]
        ]
        if [number for number, _page, _y in positions] != list(range(1, 12)):
            raise RuntimeError(f"{scheme_path}: manual markers are not Questions 1-11")
        if any(
            right[1:] <= left[1:]
            for left, right in zip(positions, positions[1:])
        ):
            raise RuntimeError(f"{scheme_path}: manual markers are not monotonic")

        questions: list[dict] = []
        for index, (number, start_page, start_y) in enumerate(positions):
            if index + 1 < len(positions):
                _next_number, end_page, end_y = positions[index + 1]
            else:
                end_page, end_y = spec["tail"]
            if (end_page, end_y) <= (start_page, start_y):
                raise RuntimeError(f"{scheme_path} Q{number}: invalid crop endpoint")

            region = [
                {"p": start_page, "r": [0.0, start_y, 1.0, 1.0]},
                *(
                    {"p": page, "r": [0.0, 0.0, 1.0, 1.0]}
                    for page in range(start_page + 1, end_page)
                ),
                {"p": end_page, "r": [0.0, 0.0, 1.0, end_y]},
            ]
            if start_page == end_page:
                region = [
                    {"p": start_page, "r": [0.0, start_y, 1.0, end_y]},
                ]
            paper_question = paper_questions[number]
            questions.append(
                {
                    "n": str(number),
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
            "component": "000",
            "band": [1, len(document) + 1],
            "copyright": COPYRIGHT,
            "q": questions,
        }


def missing_scheme_maps() -> tuple[list[tuple[int, str, dict]], int]:
    generated: list[tuple[int, str, dict]] = []
    verified = 0
    for (year, fileid), spec in MANUAL_SCHEME_SPECS.items():
        answer_map = manual_scheme_map(year, fileid, spec)
        answer_path = ANSWERS_ROOT / str(year) / f"{fileid}.json"
        if answer_path.exists():
            if json.loads(answer_path.read_text()) != answer_map:
                raise RuntimeError(f"{answer_path}: differs from reviewed Chemistry map")
            verified += 1
        else:
            generated.append((year, fileid, answer_map))
    return generated, verified


def main() -> None:
    entries = paper_index()
    existing = json.loads(TAGS_PATH.read_text())
    baseline = json.loads(BASELINE_PATH.read_text())
    existing_by_id = {identity(paper): paper for paper in existing}
    if len(existing_by_id) != len(existing):
        raise RuntimeError("Duplicate Chemistry paper identity in baseline tags")

    papers: list[dict] = []
    generated_maps: list[tuple[int, str, dict]] = []
    existing_maps_verified = 0
    max_crop_span = 0
    expected_numbers = [str(number) for number in range(1, 12)]
    generated_scheme_maps, reviewed_scheme_maps_verified = missing_scheme_maps()

    for entry in entries:
        if entry["level"] not in {"higher", "ordinary"}:
            raise RuntimeError(f"Unexpected Chemistry level: {entry}")
        if len(entry["papers"]) != 1:
            raise RuntimeError(f"Unexpected Chemistry paper count: {entry}")
        item = entry["papers"][0]
        fileid = item["doc"]["f"]
        paper_path = CORPUS / str(entry["year"]) / fileid
        if not paper_path.exists():
            raise FileNotFoundError(paper_path)
        with fitz.open(paper_path) as document:
            anchors, tail = anchors_for(document, paper_path)
        anchor_map, paper_span = hosted_map(fileid, anchors, tail)
        max_crop_span = max(max_crop_span, paper_span)

        paper_id = "|".join(
            [entry["level"], entry["lang"], str(entry["year"]), "single", fileid]
        )
        old_paper = existing_by_id.get(paper_id)
        if old_paper is not None:
            if [question["n"] for question in old_paper["q"]] != expected_numbers:
                raise RuntimeError(f"{paper_id}: inherited cards are not Q1-Q11")
            questions = copy.deepcopy(old_paper["q"])
        elif entry["year"] == 2026:
            questions = []
            for number in expected_numbers:
                tags = MANUAL_2026_TAGS.get((entry["level"], number))
                if tags is None:
                    raise RuntimeError(
                        f"No reviewed 2026 Chemistry tag for {entry['level']} Q{number}"
                    )
                questions.append({"n": number, **copy.deepcopy(tags)})
        else:
            raise RuntimeError(f"Unexpected missing inherited Chemistry paper: {paper_id}")

        papers.append(
            {
                "subjectId": "chemistry",
                "level": entry["level"],
                "lang": entry["lang"],
                "year": entry["year"],
                "fileid": fileid,
                "paperKey": "single",
                "q": questions,
            }
        )

        hosted_path = HOSTED_ROOT / str(entry["year"]) / f"{fileid}.json"
        if hosted_path.exists():
            current = json.loads(hosted_path.read_text())
            current_numbers = [question["n"] for question in current.get("q", [])]
            if current.get("paperOnly") != 1 or current_numbers != expected_numbers:
                raise RuntimeError(f"{hosted_path}: existing map is not Chemistry Q1-Q11")
            existing_maps_verified += 1
        else:
            generated_maps.append((entry["year"], fileid, anchor_map))

    paper_ids = [identity(paper) for paper in papers]
    if len(set(paper_ids)) != len(paper_ids):
        raise RuntimeError("Duplicate generated Chemistry paper identity")
    card_count = sum(len(paper["q"]) for paper in papers)
    if len(papers) != EXPECTED_VARIANTS or card_count != EXPECTED_CARDS:
        raise RuntimeError(
            f"Expected {EXPECTED_VARIANTS}/{EXPECTED_CARDS}, "
            f"found {len(papers)}/{card_count}"
        )

    preserved_cards = 0
    for expected in baseline:
        live = next((paper for paper in papers if identity(paper) == identity(expected)), None)
        if live is None:
            raise RuntimeError(f"Preservation failure: missing {identity(expected)}")
        old = existing_by_id[identity(expected)]
        if live != old:
            raise RuntimeError(f"Preservation failure: changed {identity(expected)}")
        preserved_cards += len(expected["questions"])

    TAGS_PATH.write_text(json.dumps(papers, indent=1, ensure_ascii=False) + "\n")
    for year, fileid, anchor_map in generated_maps:
        target_dir = HOSTED_ROOT / str(year)
        target_dir.mkdir(parents=True, exist_ok=True)
        (target_dir / f"{fileid}.json").write_text(
            json.dumps(anchor_map, ensure_ascii=False, separators=(",", ":")) + "\n"
        )
    for year, fileid, answer_map in generated_scheme_maps:
        target_dir = ANSWERS_ROOT / str(year)
        target_dir.mkdir(parents=True, exist_ok=True)
        (target_dir / f"{fileid}.json").write_text(
            json.dumps(answer_map, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
            + "\n"
        )

    print(
        json.dumps(
            {
                "paperVariants": len(papers),
                "physicalCards": card_count,
                "distinctStudentFacingQuestions": sum(
                    len(paper["q"]) for paper in papers if paper["lang"] == "ev"
                ),
                "hostedAnchorMapsWritten": len(generated_maps),
                "hostedMapsPreservedAndVerified": existing_maps_verified,
                "reviewedSchemeMapsWritten": len(generated_scheme_maps),
                "reviewedSchemeMapsPreservedAndVerified": reviewed_scheme_maps_verified,
                "preservedBaselineVariants": len(baseline),
                "preservedBaselineTasks": preserved_cards,
                "maximumGeneratedCropSpanPages": max_crop_span,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
