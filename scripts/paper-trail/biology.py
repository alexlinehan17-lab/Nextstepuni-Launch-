#!/usr/bin/env python3
"""Complete and correct the entitled LC Biology Paper Trail corpus.

The inherited topic wave omitted eleven official paper editions. It also
numbered every 2019-2020 Section C card one higher than the number printed on
the SEC paper (11-16 instead of 10-15). This pass:

* preserves every real baseline task while applying that verified bijective
  numbering correction;
* adds all missing English/Irish editions through 2026;
* assigns reviewed canonical tags to the 34 reference-omitted 2026 questions;
* fills missing paper-only crop maps without replacing correct verified maps.

No StudyClix question text, images, solutions, notes, mocks, or PDFs are read or
copied. Reference-site data is reconciled separately from factual headings.

Run from the repository root:
    python3 scripts/paper-trail/biology.py
"""

from __future__ import annotations

import copy
import json
import re
from pathlib import Path

import fitz


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
CORPUS = ROOT / "paper-trail-corpus" / "exampapers"
INDEX_PATH = ROOT / "paperTrailData.ts"
TAGS_PATH = HERE / "topic-tags" / "tags" / "biology.json"
BASELINE_PATH = ROOT / "test" / "fixtures" / "biologyTopicQuestionBaseline.json"
HOSTED_ROOT = ROOT / "public" / "paper-anchors"

COPYRIGHT = "© State Examinations Commission"
EXPECTED_VARIANTS = 100
EXPECTED_CARDS = 1068

# Independently reviewed from the four official SEC 2026 English paper
# booklets. The compact Paper Trail format permits two canonical curriculum
# nodes; the richer exam-topic runtime retains every relevant browse topic.
MANUAL_2026_TAGS: dict[tuple[str, str], dict[str, str]] = {
    # Higher level, Sections A and B.
    ("higher", "1"): {"primary": "biology-0-2"},
    ("higher", "2"): {"primary": "biology-1-0", "secondary": "biology-1-3"},
    ("higher", "3"): {"primary": "biology-2-3"},
    ("higher", "4"): {"primary": "biology-2-1"},
    ("higher", "5"): {"primary": "biology-1-4"},
    ("higher", "6"): {"primary": "biology-0-3", "secondary": "biology-2-0"},
    ("higher", "7"): {"primary": "biology-2-4", "secondary": "biology-2-8"},
    ("higher", "8"): {"primary": "biology-0-0", "secondary": "biology-1-0"},
    ("higher", "9"): {"primary": "biology-1-1"},
    ("higher", "10"): {"primary": "biology-2-11"},
    # Higher level, Section C.
    ("higher", "11"): {"primary": "biology-1-6", "secondary": "biology-1-5"},
    ("higher", "12"): {"primary": "biology-0-3", "secondary": "biology-0-4"},
    ("higher", "13"): {"primary": "biology-1-4"},
    ("higher", "14"): {"primary": "biology-2-13", "secondary": "biology-2-1"},
    ("higher", "15"): {"primary": "biology-2-12"},
    ("higher", "16"): {"primary": "biology-1-2", "secondary": "biology-2-0"},
    ("higher", "17"): {"primary": "biology-2-6", "secondary": "biology-2-7"},
    # Ordinary level, Sections A and B.
    ("ordinary", "1"): {"primary": "biology-0-2"},
    ("ordinary", "2"): {"primary": "biology-0-0"},
    ("ordinary", "3"): {"primary": "biology-1-0", "secondary": "biology-1-7"},
    ("ordinary", "4"): {"primary": "biology-1-4"},
    ("ordinary", "5"): {"primary": "biology-0-3"},
    ("ordinary", "6"): {"primary": "biology-2-0"},
    ("ordinary", "7"): {"primary": "biology-2-3"},
    ("ordinary", "8"): {"primary": "biology-0-0", "secondary": "biology-1-0"},
    ("ordinary", "9"): {"primary": "biology-1-1"},
    ("ordinary", "10"): {"primary": "biology-2-6", "secondary": "biology-2-1"},
    # Ordinary level, Section C.
    ("ordinary", "11"): {"primary": "biology-0-3"},
    ("ordinary", "12"): {"primary": "biology-1-4"},
    ("ordinary", "13"): {"primary": "biology-1-5", "secondary": "biology-1-6"},
    ("ordinary", "14"): {"primary": "biology-2-2"},
    ("ordinary", "15"): {"primary": "biology-2-12"},
    ("ordinary", "16"): {"primary": "biology-2-10", "secondary": "biology-2-6"},
    ("ordinary", "17"): {"primary": "biology-2-9", "secondary": "biology-2-8"},
}

# Both 2022 Ordinary Section C language editions were missing from the inherited
# wave, so there is no same-sitting local twin to copy. These seven top-level
# tags were reviewed directly against LC025GLP040EV.pdf.
MANUAL_2022_ORDINARY_C_TAGS: dict[str, dict[str, str]] = {
    "11": {"primary": "biology-0-3", "secondary": "biology-2-0"},
    "12": {"primary": "biology-1-4", "secondary": "biology-1-2"},
    "13": {"primary": "biology-2-3"},
    "14": {"primary": "biology-1-1", "secondary": "biology-1-5"},
    "15": {"primary": "biology-2-11", "secondary": "biology-2-1"},
    "16": {"primary": "biology-2-12", "secondary": "biology-2-0"},
    "17": {"primary": "biology-2-4", "secondary": "biology-1-4"},
}


def clean(text: str) -> str:
    return re.sub(r"\s+", " ", text.replace("\u00a0", " ")).strip()


def paper_index() -> list[dict]:
    source = INDEX_PATH.read_text()
    match = re.search(
        r'  "biology": (\[[\s\S]*?\n  \]),\n  "bulgarian":',
        source,
    )
    if not match:
        raise RuntimeError("Could not locate Biology in paperTrailData.ts")
    return json.loads(re.sub(r",\s*]$", "]", match.group(1)))


def component(fileid: str) -> str:
    match = re.search(r"P(\d{3})", fileid, re.IGNORECASE)
    if not match or match.group(1) not in {"000", "038", "040"}:
        raise RuntimeError(f"Unexpected Biology component: {fileid}")
    return match.group(1)


def expected_numbers(year: int, fileid: str) -> list[int]:
    paper_component = component(fileid)
    if paper_component == "000":
        return list(range(1, 16))
    if paper_component == "038":
        return list(range(1, 10 if year <= 2020 else 11))
    if year <= 2020:
        return list(range(10, 16))
    return list(range(11, 18))


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


def corrected_number(year: int, fileid: str, number: str) -> str:
    """Map the inherited 2019-2020 Section C off-by-one ID to printed truth."""
    if year in {2019, 2020} and component(fileid) == "040":
        return str(int(number) - 1)
    return number


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
            "answerbook for section c",
            "freagarleabhar do roinn c",
            "start each question on a new page",
            "tosaigh gach ceist ar leathanach nua",
            "this page is intentionally blank",
            "this page has been left blank",
            "do not write on this page",
            "ná scríobh ar an leathanach seo",
        )
    )


def anchors_for(
    document: fitz.Document,
    pdf_path: Path,
    expected: list[int],
) -> tuple[list[dict], tuple[int, float]]:
    first: dict[int, tuple[int, float]] = {}
    wanted = set(expected)
    for page_number, page in enumerate(document, start=1):
        for text, x_fraction, y_fraction in line_records(page):
            # A few source PDFs drop the printed full stop from their text
            # layer (for example 2026 HL Q12), while retaining the same
            # left-margin header geometry.
            match = re.match(r"^(\d{1,2})(?:\s*\.(?:\s|$)|$)", text)
            if not match or x_fraction > 0.22 or y_fraction > 0.93:
                continue
            number = int(match.group(1))
            if number in wanted:
                first.setdefault(number, (page_number, round(y_fraction, 4)))

    if set(first) != wanted:
        raise RuntimeError(
            f"{pdf_path}: expected Question {expected}, found {sorted(first)}"
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

    anchors = [
        {
            "n": str(number),
            "page": first[number][0],
            "y": first[number][1],
        }
        for number in expected
    ]
    return anchors, tail


def section_for(year: int, number: int) -> str:
    if year <= 2020:
        return "A" if number <= 6 else "B" if number <= 9 else "C"
    return "A" if number <= 7 else "B" if number <= 10 else "C"


def hosted_map(
    year: int,
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
            raise RuntimeError(f"{year}/{fileid} Q{anchor['n']}: invalid crop endpoint")
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
                "label": f"Section {section_for(year, number)} · Question {number}",
                "printOrder": index + 1,
                "endP": end[0],
                "endY": end[1],
            }
        )
    if max_span > 10:
        raise RuntimeError(f"{year}/{fileid}: implausible question span {max_span}")
    result = {
        "v": 1,
        "paperFileid": fileid,
        "schemeFileid": "",
        "component": component(fileid),
        "band": [1, 1],
        "copyright": COPYRIGHT,
        "paperOnly": 1,
        **({"maxCropPages": max_span} if max_span > 3 else {}),
        "q": questions,
    }
    return result, max_span


def main() -> None:
    entries = paper_index()
    existing = json.loads(TAGS_PATH.read_text())
    baseline = json.loads(BASELINE_PATH.read_text())
    existing_by_id = {identity(paper): paper for paper in existing}
    if len(existing_by_id) != len(existing):
        raise RuntimeError("Duplicate Biology paper identity in baseline tags")

    logical_tags: dict[tuple[str, int, str], dict[str, str]] = {}
    conflicting_language_tags: set[tuple[str, int, str]] = set()
    for paper in existing:
        for question in paper["q"]:
            number = corrected_number(paper["year"], paper["fileid"], question["n"])
            key = (paper["level"], paper["year"], number)
            tags = {
                field: question[field]
                for field in ("primary", "secondary")
                if question.get(field)
            }
            previous = logical_tags.get(key)
            if previous is not None and previous != tags:
                conflicting_language_tags.add(key)
            # English is the review source when translated editions disagree;
            # all existing edition-specific records themselves remain intact.
            if previous is None or paper["lang"] == "ev":
                logical_tags[key] = tags

    papers: list[dict] = []
    generated_maps: list[tuple[int, str, dict]] = []
    corrected_maps = 0
    existing_maps_verified = 0
    max_crop_span = 0

    for entry in entries:
        if entry["level"] not in {"higher", "ordinary"}:
            raise RuntimeError(f"Unexpected Biology level: {entry}")
        for item in entry["papers"]:
            fileid = item["doc"]["f"]
            expected = expected_numbers(entry["year"], fileid)
            paper_path = CORPUS / str(entry["year"]) / fileid
            if not paper_path.exists():
                raise FileNotFoundError(paper_path)
            with fitz.open(paper_path) as document:
                anchors, tail = anchors_for(document, paper_path, expected)
            anchor_map, paper_span = hosted_map(entry["year"], fileid, anchors, tail)
            max_crop_span = max(max_crop_span, paper_span)

            paper_id = "|".join(
                [entry["level"], entry["lang"], str(entry["year"]), "single", fileid]
            )
            old_paper = existing_by_id.get(paper_id)
            old_by_corrected_number = {
                corrected_number(entry["year"], fileid, question["n"]): question
                for question in (old_paper or {}).get("q", [])
            }

            questions: list[dict] = []
            for number in map(str, expected):
                old_question = old_by_corrected_number.get(number)
                if old_question is not None:
                    question = copy.deepcopy(old_question)
                    question["n"] = number
                else:
                    if entry["year"] == 2026:
                        tags = MANUAL_2026_TAGS.get((entry["level"], number))
                    elif (
                        entry["year"] == 2022
                        and entry["level"] == "ordinary"
                        and component(fileid) == "040"
                    ):
                        tags = MANUAL_2022_ORDINARY_C_TAGS.get(number)
                    else:
                        tags = logical_tags.get(
                            (entry["level"], entry["year"], number)
                        )
                    if tags is None:
                        raise RuntimeError(
                            f"No reviewed Biology tag for "
                            f"{entry['level']} {entry['year']} Q{number}"
                        )
                    question = {"n": number, **copy.deepcopy(tags)}
                questions.append(question)

            papers.append(
                {
                    "subjectId": "biology",
                    "level": entry["level"],
                    "lang": entry["lang"],
                    "year": entry["year"],
                    "fileid": fileid,
                    "paperKey": "single",
                    "q": questions,
                }
            )

            hosted_path = HOSTED_ROOT / str(entry["year"]) / f"{fileid}.json"
            replace_for_numbering_fix = (
                entry["year"] in {2019, 2020} and component(fileid) == "040"
            )
            if hosted_path.exists() and not replace_for_numbering_fix:
                current = json.loads(hosted_path.read_text())
                current_numbers = [question["n"] for question in current.get("q", [])]
                wanted_numbers = list(map(str, expected))
                if current.get("paperOnly") != 1 or current_numbers != wanted_numbers:
                    raise RuntimeError(
                        f"{hosted_path}: existing verified map does not match "
                        f"{wanted_numbers}"
                    )
                existing_maps_verified += 1
            else:
                generated_maps.append((entry["year"], fileid, anchor_map))
                if replace_for_numbering_fix and hosted_path.exists():
                    corrected_maps += 1

    paper_ids = [identity(paper) for paper in papers]
    if len(set(paper_ids)) != len(paper_ids):
        raise RuntimeError("Duplicate generated Biology paper identity")
    card_count = sum(len(paper["q"]) for paper in papers)
    if len(papers) != EXPECTED_VARIANTS or card_count != EXPECTED_CARDS:
        raise RuntimeError(
            f"Expected {EXPECTED_VARIANTS}/{EXPECTED_CARDS}, "
            f"found {len(papers)}/{card_count}"
        )

    preserved_cards = 0
    corrected_card_ids = 0
    for expected in baseline:
        live = next((paper for paper in papers if identity(paper) == identity(expected)), None)
        if live is None:
            raise RuntimeError(f"Preservation failure: missing {identity(expected)}")
        old = existing_by_id[identity(expected)]
        live_by_number = {question["n"]: question for question in live["q"]}
        old_by_number = {question["n"]: question for question in old["q"]}
        for old_number in expected["questions"]:
            live_number = corrected_number(expected["year"], expected["fileid"], old_number)
            old_question = copy.deepcopy(old_by_number[old_number])
            old_question["n"] = live_number
            if live_by_number.get(live_number) != old_question:
                raise RuntimeError(
                    f"Preservation failure: changed {identity(expected)} "
                    f"Q{old_number} -> Q{live_number}"
                )
            preserved_cards += 1
            corrected_card_ids += int(live_number != old_number)

    TAGS_PATH.write_text(json.dumps(papers, indent=1, ensure_ascii=False) + "\n")
    for year, fileid, anchor_map in generated_maps:
        target_dir = HOSTED_ROOT / str(year)
        target_dir.mkdir(parents=True, exist_ok=True)
        (target_dir / f"{fileid}.json").write_text(
            json.dumps(anchor_map, ensure_ascii=False, separators=(",", ":")) + "\n"
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
                "corrected2019To2020SectionCMaps": corrected_maps,
                "preservedBaselineVariants": len(baseline),
                "preservedBaselineTasks": preserved_cards,
                "correctedBaselineCardIds": corrected_card_ids,
                "retainedEditionSpecificTagDisagreements": len(
                    conflicting_language_tags
                ),
                "maximumGeneratedCropSpanPages": max_crop_span,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
