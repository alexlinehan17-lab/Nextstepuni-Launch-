#!/usr/bin/env python3
"""Expose every selectable question in the entitled LC Computer Science corpus.

The existing topic file covered only 23 of the 52 separately published
official-language booklets. This pass preserves every shipped card verbatim,
adds the missing Section A/B and Section C variants through 2026, and emits a
finite paper-only crop map for every booklet.

Topic tags are reconciled from factual reference headings only. No StudyClix
question text, images, solutions, notes, mocks, or PDFs are read or copied.

Run from the repository root:
    python3 scripts/paper-trail/computer_science.py
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
TAGS_PATH = HERE / "topic-tags" / "tags" / "computer-science.json"
REFERENCE_PATH = ROOT / "data" / "examTopics" / "computer-science.json"
CROSSWALK_PATH = (
    ROOT / "data" / "examTopics" / "computer-science-curriculum-crosswalk.json"
)
BASELINE_PATH = (
    ROOT / "test" / "fixtures" / "computerScienceTopicQuestionBaseline.json"
)
HOSTED_ROOT = ROOT / "public" / "paper-anchors"

COPYRIGHT = "© State Examinations Commission"
EXPECTED_VARIANTS = 52
EXPECTED_CARDS = 416


def clean(text: str) -> str:
    return re.sub(r"\s+", " ", text.replace("\u00a0", " ")).strip()


def paper_index() -> list[dict]:
    source = INDEX_PATH.read_text()
    match = re.search(
        r'  "computer-science": (\[[\s\S]*?\n  \]),\n  "construction-studies":',
        source,
    )
    if not match:
        raise RuntimeError("Could not locate Computer Science in paperTrailData.ts")
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


def exact_question_number(text: str) -> int | None:
    match = re.fullmatch(r"(?:Question|Ceist)\s+(\d{1,2})", text, re.IGNORECASE)
    return int(match.group(1)) if match else None


def optional_page(text: str) -> bool:
    lowered = text.lower()
    return (
        "optional additional page" in lowered
        or ("leathanach breise" in lowered and "rogha" in lowered)
        or "space for rough work" in lowered
        or "sracoibre" in lowered
    )


def question_anchors(
    document: fitz.Document,
    pdf_path: Path,
    expected: list[int],
) -> tuple[list[dict], tuple[int, float], tuple[int, float] | None]:
    first: dict[int, tuple[int, float]] = {}
    section_b_candidates: list[tuple[int, float]] = []
    for page_number, page in enumerate(document, start=1):
        for text, _x_fraction, y_fraction in line_records(page):
            if re.fullmatch(r"(?:Section|Roinn)\s+B", text, re.IGNORECASE):
                section_b_candidates.append((page_number, round(y_fraction, 4)))
            number = exact_question_number(text)
            if number in expected:
                first.setdefault(number, (page_number, round(y_fraction, 4)))

    if set(first) != set(expected):
        raise RuntimeError(
            f"{pdf_path}: expected Question {expected}, found {sorted(first)}"
        )
    positions = [first[number] for number in expected]
    if any(right <= left for left, right in zip(positions, positions[1:])):
        raise RuntimeError(f"{pdf_path}: non-monotonic question anchors")

    tail = (len(document), 0.9)
    last_page = positions[-1][0]
    for page_number in range(last_page + 1, len(document) + 1):
        if optional_page(clean(document[page_number - 1].get_text("text"))):
            tail = (page_number - 1, 0.9)
            break
    if tail <= positions[-1]:
        raise RuntimeError(f"{pdf_path}: invalid last-question tail {tail}")

    section_b = None
    if expected == list(range(1, 16)):
        between = [
            position
            for position in section_b_candidates
            if first[12] < position < first[13]
        ]
        if not between:
            raise RuntimeError(f"{pdf_path}: missing operative Section B divider")
        section_b = min(between)

    anchors = [
        {
            "n": str(number),
            "section": "A" if number <= 12 else "B" if number <= 15 else "C",
            "page": first[number][0],
            "y": first[number][1],
        }
        for number in expected
    ]
    return anchors, tail, section_b


def parse_reference_heading(heading: str) -> dict:
    normalized = clean(heading)
    year_match = re.match(r"^(\d{4})\b", normalized)
    section_matches = list(re.finditer(r"Section\s*([ABC])\b", normalized, re.I))
    question_match = re.search(r"Question\s*(\d{1,2})\b", normalized, re.I)
    if not year_match or not section_matches or not question_match:
        raise RuntimeError(f"Unparseable Computer Science reference heading: {heading}")
    return {
        "year": int(year_match.group(1)),
        "section": section_matches[-1].group(1).upper(),
        "question": int(question_match.group(1)),
        "sample": "sample" in normalized.lower(),
    }


def reference_topics(reference: dict) -> dict[tuple[str, int, str], list[str]]:
    result: dict[tuple[str, int, str], list[str]] = {}
    for level, level_data in reference["levels"].items():
        for topic in level_data["topics"]:
            for heading in topic["officialQuestionHeadings"]:
                parsed = parse_reference_heading(heading)
                if parsed["sample"]:
                    continue
                key = (level, parsed["year"], str(parsed["question"]))
                topics = result.setdefault(key, [])
                if topic["id"] not in topics:
                    topics.append(topic["id"])
    return result


def component(fileid: str) -> str:
    match = re.search(r"P(\d{3})", fileid)
    if not match or match.group(1) not in {"038", "040"}:
        raise RuntimeError(f"Unexpected Computer Science component: {fileid}")
    return match.group(1)


def main() -> None:
    entries = paper_index()
    existing = json.loads(TAGS_PATH.read_text())
    baseline = json.loads(BASELINE_PATH.read_text())
    reference = json.loads(REFERENCE_PATH.read_text())
    crosswalk = json.loads(CROSSWALK_PATH.read_text())
    canonical_ids = {node for nodes in crosswalk.values() for node in nodes}
    reference_by_card = reference_topics(reference)

    existing_by_id = {identity(paper): paper for paper in existing}
    if len(existing_by_id) != len(existing):
        raise RuntimeError("Duplicate Computer Science paper identity in baseline tags")
    existing_logical: dict[tuple[str, int, str], dict[str, str]] = {}
    for paper in existing:
        for question in paper["q"]:
            key = (paper["level"], paper["year"], question["n"])
            tags = {
                field: question[field]
                for field in ("primary", "secondary")
                if question.get(field)
            }
            existing_logical.setdefault(key, tags)

    def tags_for(level: str, year: int, number: str) -> dict[str, str]:
        key = (level, year, number)
        nodes: list[str] = []
        for topic_id in reference_by_card.get(key, []):
            for node in crosswalk[topic_id]:
                if node not in nodes:
                    nodes.append(node)
        if not nodes:
            preserved = existing_logical.get(key)
            if preserved is None:
                raise RuntimeError(f"No reviewed Computer Science tag for {key}")
            return copy.deepcopy(preserved)
        return {
            "primary": nodes[0],
            **({"secondary": nodes[1]} if len(nodes) > 1 else {}),
        }

    papers: list[dict] = []
    hosted_maps: list[tuple[int, str, dict]] = []
    max_crop_span = 0

    for entry in entries:
        if entry["level"] not in {"higher", "ordinary"}:
            raise RuntimeError(f"Unexpected level in Computer Science index: {entry}")
        if len(entry["papers"]) != 2:
            raise RuntimeError(
                f"{entry['year']} {entry['level']} {entry['lang']}: expected A/B and C"
            )
        seen_components: set[str] = set()
        for item in entry["papers"]:
            fileid = item["doc"]["f"]
            paper_component = component(fileid)
            seen_components.add(paper_component)
            expected = list(range(1, 16)) if paper_component == "038" else [16]
            paper_path = CORPUS / str(entry["year"]) / fileid
            if not paper_path.exists():
                raise FileNotFoundError(paper_path)

            with fitz.open(paper_path) as document:
                anchors, tail, section_b = question_anchors(
                    document, paper_path, expected
                )

            paper_id = "|".join(
                [entry["level"], entry["lang"], str(entry["year"]), "single", fileid]
            )
            old_paper = existing_by_id.get(paper_id)
            old_questions = {
                question["n"]: question for question in (old_paper or {}).get("q", [])
            }
            questions: list[dict] = []
            for anchor in anchors:
                old_question = old_questions.get(anchor["n"])
                question = (
                    copy.deepcopy(old_question)
                    if old_question is not None
                    else {
                        "n": anchor["n"],
                        **tags_for(entry["level"], entry["year"], anchor["n"]),
                    }
                )
                for field in ("primary", "secondary"):
                    if question.get(field) and question[field] not in canonical_ids:
                        raise RuntimeError(
                            f"{paper_id} Q{anchor['n']}: invalid canonical tag {question[field]}"
                        )
                questions.append(question)

            papers.append(
                {
                    "subjectId": "computer-science",
                    "level": entry["level"],
                    "lang": entry["lang"],
                    "year": entry["year"],
                    "fileid": fileid,
                    "paperKey": "single",
                    "q": questions,
                }
            )

            hosted_questions: list[dict] = []
            paper_max_span = 0
            for index, anchor in enumerate(anchors):
                if index + 1 < len(anchors):
                    following = anchors[index + 1]
                    end = (following["page"], following["y"])
                    if anchor["n"] == "12" and following["n"] == "13":
                        if section_b is None:
                            raise RuntimeError(f"{paper_path}: missing Section B crop boundary")
                        end = section_b
                else:
                    end = tail
                start = (anchor["page"], anchor["y"])
                if end <= start:
                    raise RuntimeError(f"{paper_path}: invalid crop end for Q{anchor['n']}")
                span = end[0] - start[0]
                paper_max_span = max(paper_max_span, span)
                max_crop_span = max(max_crop_span, span)
                hosted_questions.append(
                    {
                        "n": anchor["n"],
                        "pP": anchor["page"],
                        "pY": [anchor["y"], 1],
                        "region": [{"p": 1}],
                        "mode": "pagejump",
                        "conf": 0.5,
                        "label": f"Section {anchor['section']} · Question {anchor['n']}",
                        "printOrder": index + 1,
                        "endP": end[0],
                        "endY": end[1],
                    }
                )
            if paper_max_span > 12:
                raise RuntimeError(f"{paper_path}: implausible question span {paper_max_span}")
            anchor_map = {
                "v": 1,
                "paperFileid": fileid,
                "schemeFileid": "",
                "component": paper_component,
                "band": [1, 1],
                "copyright": COPYRIGHT,
                "paperOnly": 1,
                **({"maxCropPages": paper_max_span} if paper_max_span > 3 else {}),
                "q": hosted_questions,
            }
            hosted_maps.append((entry["year"], fileid, anchor_map))

        if seen_components != {"038", "040"}:
            raise RuntimeError(
                f"{entry['year']} {entry['level']} {entry['lang']}: components {seen_components}"
            )

    paper_ids = [identity(paper) for paper in papers]
    if len(set(paper_ids)) != len(paper_ids):
        raise RuntimeError("Duplicate generated Computer Science paper identity")
    card_count = sum(len(paper["q"]) for paper in papers)
    if len(papers) != EXPECTED_VARIANTS or card_count != EXPECTED_CARDS:
        raise RuntimeError(
            f"Expected {EXPECTED_VARIANTS}/{EXPECTED_CARDS}, found {len(papers)}/{card_count}"
        )

    preserved_cards = 0
    for expected in baseline:
        live = next((paper for paper in papers if identity(paper) == identity(expected)), None)
        if live is None:
            raise RuntimeError(f"Preservation failure: missing {identity(expected)}")
        old = existing_by_id[identity(expected)]
        live_by_number = {question["n"]: question for question in live["q"]}
        old_by_number = {question["n"]: question for question in old["q"]}
        for number in expected["questions"]:
            if live_by_number.get(number) != old_by_number.get(number):
                raise RuntimeError(
                    f"Preservation failure: changed {identity(expected)} Q{number}"
                )
            preserved_cards += 1

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
                "physicalCards": card_count,
                "distinctStudentFacingQuestions": sum(
                    len(paper["q"]) for paper in papers if paper["lang"] == "ev"
                ),
                "hostedAnchorMapsWritten": len(hosted_maps),
                "preservedBaselineVariants": len(baseline),
                "preservedBaselineCards": preserved_cards,
                "maximumHostedCropSpanPages": max_crop_span,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
