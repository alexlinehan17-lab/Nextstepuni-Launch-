#!/usr/bin/env python3
"""Expose every selectable question in the entitled LC Economics corpus.

The legacy pipeline indexed only Section A on pre-2021 papers.  This pass
preserves every shipped card, adds the eight independently selectable Section
B questions, fills missing paper variants, and emits paper-only anchors where
the classic answer map cannot address the resulting stable ID.

Topic tags are reconciled from factual reference headings only.  No StudyClix
question text, images, solutions, notes, mocks, or PDFs are read or copied.

Run from the repository root:
    python3 scripts/paper-trail/economics.py
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
TAGS_PATH = HERE / "topic-tags" / "tags" / "economics.json"
REFERENCE_PATH = ROOT / "data" / "examTopics" / "economics.json"
CROSSWALK_PATH = (
    ROOT / "data" / "examTopics" / "economics-curriculum-crosswalk.json"
)
BASELINE_PATH = (
    ROOT / "test" / "fixtures" / "economicsTopicQuestionBaseline.json"
)
HOSTED_ROOT = ROOT / "public" / "paper-anchors"
ANSWERS_ROOT = HERE / "answers"

COPYRIGHT = "© State Examinations Commission"
EXPECTED_VARIANTS = 66
EXPECTED_CARDS = 1098

# The factual reference omits 32 entitled old-format cards.  Eleven already
# carry reviewed canonical tags in the frozen local corpus; these 21 are the
# remaining independently reviewed SEC questions.  The values point only into
# the canonical NCCA Economics tree.
MANUAL_TAGS: dict[tuple[str, int, str], dict[str, str]] = {
    ("higher", 2010, "1"): {"primary": "economics-1-0", "secondary": "economics-1-2"},
    ("higher", 2010, "5"): {"primary": "economics-1-2", "secondary": "economics-3-5"},
    ("ordinary", 2010, "9"): {"primary": "economics-4-2", "secondary": "economics-4-1"},
    ("ordinary", 2010, "B6"): {"primary": "economics-3-4", "secondary": "economics-3-3"},
    ("higher", 2011, "4"): {"primary": "economics-3-1", "secondary": "economics-3-4"},
    ("higher", 2011, "8"): {"primary": "economics-1-4", "secondary": "economics-1-1"},
    ("higher", 2011, "B3"): {"primary": "economics-2-1", "secondary": "economics-3-5"},
    ("ordinary", 2011, "2"): {"primary": "economics-0-0", "secondary": "economics-1-0"},
    ("ordinary", 2011, "B7"): {"primary": "economics-3-4", "secondary": "economics-0-0"},
    ("ordinary", 2012, "1"): {"primary": "economics-3-1", "secondary": "economics-1-3"},
    ("higher", 2013, "2"): {"primary": "economics-1-2", "secondary": "economics-3-5"},
    ("higher", 2013, "6"): {"primary": "economics-0-0", "secondary": "economics-3-0"},
    ("higher", 2013, "7"): {"primary": "economics-0-0"},
    ("higher", 2014, "B4"): {"primary": "economics-1-2", "secondary": "economics-3-4"},
    ("higher", 2015, "B4"): {"primary": "economics-1-2", "secondary": "economics-3-4"},
    ("ordinary", 2017, "B4"): {"primary": "economics-3-4", "secondary": "economics-3-3"},
    ("higher", 2018, "2"): {"primary": "economics-3-3", "secondary": "economics-3-4"},
    ("ordinary", 2018, "4"): {"primary": "economics-0-0"},
    ("ordinary", 2018, "7"): {"primary": "economics-3-3"},
    ("ordinary", 2019, "4"): {"primary": "economics-0-0"},
    ("ordinary", 2019, "B8"): {"primary": "economics-3-5", "secondary": "economics-3-2"},
}


def clean(text: str) -> str:
    return re.sub(r"\s+", " ", text.replace("\u00a0", " ")).strip()


def paper_index() -> list[dict]:
    source = INDEX_PATH.read_text()
    match = re.search(
        r'  "economics": (\[[\s\S]*?\n  \]),\n  "engineering":',
        source,
    )
    if not match:
        raise RuntimeError("Could not locate Economics in paperTrailData.ts")
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


def lead_number(text: str) -> int | None:
    words = text.split()
    if not words:
        return None
    token = words[0]
    if len(words) > 1 and words[1] == "." and token.isdigit():
        token += "."
    match = re.fullmatch(r"(\d{1,2})\.", token)
    return int(match.group(1)) if match else None


def old_format_anchors(
    document: fitz.Document,
    pdf_path: Path,
) -> tuple[list[dict], tuple[int, float]]:
    sections: dict[str, tuple[int, float]] = {}
    hits: list[tuple[int, int, float]] = []

    for page_number, page in enumerate(document, start=1):
        for text, x_fraction, y_fraction in line_records(page):
            section = re.match(r"^(?:SECTION|ROINN)\s+([AB])\b", text, re.IGNORECASE)
            # The cover repeats both section names.  The actual paper begins on
            # page 2, and the first later occurrence is the operative divider.
            if section and page_number > 1:
                sections.setdefault(section.group(1).upper(), (page_number, y_fraction))

            number = lead_number(text)
            if number is not None and x_fraction < 0.18 and y_fraction < 0.9:
                hits.append((number, page_number, round(y_fraction, 4)))

    if set(sections) != {"A", "B"} or not sections["A"] < sections["B"]:
        raise RuntimeError(f"{pdf_path}: invalid Section A/B dividers {sections}")

    anchors: list[dict] = []
    for section, expected in (("A", range(1, 10)), ("B", range(1, 9))):
        lower = sections[section]
        upper = sections.get("B") if section == "A" else None
        section_hits = [
            hit
            for hit in hits
            if hit[1:] > lower and (upper is None or hit[1:] < upper)
        ]
        first: dict[int, tuple[int, float]] = {}
        for number, page_number, y_fraction in section_hits:
            if number in expected:
                first.setdefault(number, (page_number, y_fraction))
        if set(first) != set(expected):
            raise RuntimeError(
                f"{pdf_path}: {section} expected {list(expected)}, found {sorted(first)}"
            )
        positions = [first[number] for number in expected]
        if any(right <= left for left, right in zip(positions, positions[1:])):
            raise RuntimeError(f"{pdf_path}: non-monotonic Section {section} anchors")
        anchors.extend(
            {
                "n": str(number) if section == "A" else f"B{number}",
                "section": section,
                "printed": number,
                "page": first[number][0],
                "y": first[number][1],
            }
            for number in expected
        )

    if any(
        (right["page"], right["y"]) <= (left["page"], left["y"])
        for left, right in zip(anchors, anchors[1:])
    ):
        raise RuntimeError(f"{pdf_path}: non-monotonic complete question sequence")
    return anchors, sections["B"]


def question_word_number(text: str) -> int | None:
    words = text.split()
    if len(words) < 2 or words[0].lower() not in {"question", "ceist"}:
        return None
    if not words[1].isdigit():
        return None
    digits = words[1]
    # A handful of English PDFs encode a two-digit header as adjacent glyphs
    # ("Question 1 2").  No prose follows a genuine one-digit header with a
    # second bare digit on that same header line.
    if (
        len(digits) == 1
        and len(words) > 2
        and len(words[2]) == 1
        and words[2].isdigit()
    ):
        digits += words[2]
    number = int(digits)
    return number if 1 <= number <= 16 else None


def optional_page(text: str) -> bool:
    lowered = text.lower()
    return (
        "optional additional page" in lowered
        or ("leathanach breise" in lowered and "rogha" in lowered)
    )


def new_format_anchors(
    document: fitz.Document,
    pdf_path: Path,
) -> tuple[list[dict], tuple[int, float], tuple[int, float]]:
    first: dict[int, tuple[int, float]] = {}
    section_b_candidates: list[tuple[int, float]] = []
    for page_number, page in enumerate(document, start=1):
        for text, x_fraction, y_fraction in line_records(page):
            if re.match(r"^(?:SECTION|ROINN)\s+B\b", text, re.IGNORECASE):
                section_b_candidates.append((page_number, round(y_fraction, 4)))
            number = question_word_number(text)
            if number is not None and x_fraction < 0.2 and y_fraction < 0.9:
                first.setdefault(number, (page_number, round(y_fraction, 4)))

    if set(first) != set(range(1, 17)):
        raise RuntimeError(
            f"{pdf_path}: expected Question 1-16, found {sorted(first)}"
        )
    positions = [first[number] for number in range(1, 17)]
    if any(right <= left for left, right in zip(positions, positions[1:])):
        raise RuntimeError(f"{pdf_path}: non-monotonic Question 1-16 anchors")

    section_b_options = [position for position in section_b_candidates if position < first[11]]
    if not section_b_options:
        raise RuntimeError(f"{pdf_path}: missing operative Section B divider")
    section_b = max(section_b_options)
    if section_b <= first[10]:
        raise RuntimeError(f"{pdf_path}: Section B divider does not follow Question 10")

    last_page = positions[-1][0]
    tail = (len(document), 0.9)
    for page_number in range(last_page + 1, len(document) + 1):
        if optional_page(clean(document[page_number - 1].get_text("text"))):
            tail = (page_number - 1, 0.9)
            break
    if tail <= positions[-1]:
        raise RuntimeError(f"{pdf_path}: invalid last-question tail {tail}")

    anchors = [
        {
            "n": str(number),
            "section": "A" if number <= 10 else "B",
            "printed": number,
            "page": first[number][0],
            "y": first[number][1],
        }
        for number in range(1, 17)
    ]
    return anchors, section_b, tail


def parse_reference_heading(heading: str) -> dict:
    normalized = clean(heading)
    match = re.match(
        r"^(\d{4})\s*-\s*"
        r"(?:(Paper|Sample Paper|Deferred Exam Paper)\s*-\s*)?"
        r"Section\s*([AB12])\s*-\s*Question\s*(\d{1,2})\b",
        normalized,
        re.IGNORECASE,
    )
    if not match:
        raise RuntimeError(f"Unparseable Economics reference heading: {heading}")
    section = {"1": "A", "2": "B"}.get(match.group(3).upper(), match.group(3).upper())
    return {
        "year": int(match.group(1)),
        "edition": (match.group(2) or "main").lower(),
        "section": section,
        "question": int(match.group(4)),
    }


def local_number(parsed: dict) -> str:
    if parsed["year"] <= 2020:
        return (
            str(parsed["question"])
            if parsed["section"] == "A"
            else f"B{parsed['question']}"
        )
    return str(parsed["question"])


def reference_topics(reference: dict) -> dict[tuple[str, int, str], list[str]]:
    result: dict[tuple[str, int, str], list[str]] = {}
    for level, level_data in reference["levels"].items():
        for topic in level_data["topics"]:
            for heading in topic["officialQuestionHeadings"]:
                parsed = parse_reference_heading(heading)
                if parsed["year"] < 2010:
                    continue
                if "sample" in parsed["edition"] or "deferred" in parsed["edition"]:
                    continue
                key = (level, parsed["year"], local_number(parsed))
                topics = result.setdefault(key, [])
                if topic["id"] not in topics:
                    topics.append(topic["id"])
    return result


def main() -> None:
    entries = paper_index()
    existing = json.loads(TAGS_PATH.read_text())
    baseline = json.loads(BASELINE_PATH.read_text())
    reference = json.loads(REFERENCE_PATH.read_text())
    crosswalk = json.loads(CROSSWALK_PATH.read_text())
    canonical_ids = {node for nodes in crosswalk.values() for node in nodes}
    reference_by_card = reference_topics(reference)

    existing_by_id = {identity(paper): paper for paper in existing}
    existing_logical: dict[tuple[str, int, str], dict[str, str]] = {}
    for paper in existing:
        for question in paper["q"]:
            key = (paper["level"], paper["year"], question["n"])
            tags = {
                field: question[field]
                for field in ("primary", "secondary")
                if question.get(field)
            }
            # A few legacy Irish/English siblings differ only in whether a
            # secondary tag was present.  Their exact shipped objects are
            # preserved below; a newly filled sibling uses the independently
            # reconciled reference mapping where one exists, otherwise the
            # first reviewed legacy tag is a safe preservation fallback.
            existing_logical.setdefault(key, tags)

    def tags_for(level: str, year: int, number: str) -> dict[str, str]:
        key = (level, year, number)
        topics = reference_by_card.get(key, [])
        nodes: list[str] = []
        for topic_id in topics:
            if topic_id not in crosswalk:
                raise RuntimeError(f"Missing curriculum crosswalk for {topic_id}")
            for node in crosswalk[topic_id]:
                if node not in nodes:
                    nodes.append(node)
        if not nodes:
            if key in existing_logical:
                return copy.deepcopy(existing_logical[key])
            manual = MANUAL_TAGS.get(key)
            if manual is None:
                raise RuntimeError(f"No reviewed Economics tag for {key}")
            return copy.deepcopy(manual)
        return {
            "primary": nodes[0],
            **({"secondary": nodes[1]} if len(nodes) > 1 else {}),
        }

    papers: list[dict] = []
    hosted_maps: list[tuple[int, str, dict]] = []
    max_crop_span = 0

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

        with fitz.open(paper_path) as document:
            if entry["year"] <= 2020:
                anchors, section_b = old_format_anchors(document, paper_path)
                tail = (anchors[-1]["page"], 0.9)
            else:
                anchors, section_b, tail = new_format_anchors(document, paper_path)

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
            if question["primary"] not in canonical_ids or (
                question.get("secondary")
                and question["secondary"] not in canonical_ids
            ):
                raise RuntimeError(f"{paper_id} Q{anchor['n']}: invalid canonical tag")
            questions.append(question)

        papers.append(
            {
                "subjectId": "economics",
                "level": entry["level"],
                "lang": entry["lang"],
                "year": entry["year"],
                "fileid": fileid,
                "paperKey": "single",
                "q": questions,
            }
        )

        classic_map = ANSWERS_ROOT / str(entry["year"]) / f"{fileid}.json"
        needs_hosted = entry["year"] <= 2020 or not classic_map.exists()
        if not needs_hosted:
            continue

        hosted_questions: list[dict] = []
        paper_max_span = 0
        for index, anchor in enumerate(anchors):
            if index + 1 < len(anchors):
                following = anchors[index + 1]
                end = (following["page"], following["y"])
                if anchor["section"] == "A" and following["section"] == "B":
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
                    "label": f"Section {anchor['section']} · Question {anchor['printed']}",
                    "printOrder": index + 1,
                    "endP": end[0],
                    "endY": end[1],
                }
            )
        if paper_max_span > 8:
            raise RuntimeError(f"{paper_path}: implausible question span {paper_max_span}")
        anchor_map = {
            "v": 1,
            "paperFileid": fileid,
            "schemeFileid": "",
            "component": "000",
            "band": [1, 1],
            "copyright": COPYRIGHT,
            "paperOnly": 1,
            **({"maxCropPages": paper_max_span} if paper_max_span > 3 else {}),
            "q": hosted_questions,
        }
        hosted_maps.append((entry["year"], fileid, anchor_map))

    paper_ids = [identity(paper) for paper in papers]
    duplicate_ids = sorted(
        {paper_id for paper_id in paper_ids if paper_ids.count(paper_id) > 1}
    )
    if duplicate_ids:
        raise RuntimeError(f"Duplicate Economics variants: {duplicate_ids}")
    if len(papers) != EXPECTED_VARIANTS:
        raise RuntimeError(f"Expected {EXPECTED_VARIANTS} variants, found {len(papers)}")
    card_count = sum(len(paper["q"]) for paper in papers)
    if card_count != EXPECTED_CARDS:
        raise RuntimeError(f"Expected {EXPECTED_CARDS} cards, found {card_count}")

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
