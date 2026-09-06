#!/usr/bin/env python3
"""Complete and reclassify the entitled Leaving Certificate Business corpus.

The pre-migration tags exposed only short questions on the combined papers and
did not expose the Higher Applied Business Question. This generator preserves
every shipped question object byte-for-byte, fills all official-language paper
variants through 2026, and adds one selectable card for every finite top-level
question. It also emits paper-only anchors for the complete stable numbering.

StudyClix contributes factual headings and counts only. Question text, marking
schemes, mocks, notes, images, videos, and PDFs are never copied from it.
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
TAGS_PATH = HERE / "topic-tags" / "tags" / "business.json"
REFERENCE_PATH = ROOT / "data" / "examTopics" / "business.json"
CROSSWALK_PATH = ROOT / "data" / "examTopics" / "business-curriculum-crosswalk.json"
BASELINE_PATH = ROOT / "test" / "fixtures" / "businessTopicQuestionBaseline.json"
ANSWERS_ROOT = HERE / "answers"
HOSTED_ROOT = ROOT / "public" / "paper-anchors"

COPYRIGHT = "© State Examinations Commission"
EXPECTED_DOCUMENTS = 96
EXPECTED_CARDS = 1442


# Directly reviewed from the official English SEC papers. The six pre-2026
# entries are genuine reference omissions; the 45 entries from 2026 post-date
# the factual reference snapshot. These are Paper Trail's broad outgoing-
# syllabus tags only. The separate exam-topic evidence retains every applicable
# old/new practice bucket for the same top-level question.
MANUAL_TAGS: dict[tuple[str, int, str, str], dict[str, str]] = {
    ("higher", 2011, "single", "8"): {"primary": "business-5-15", "secondary": "business-5-17"},
    ("higher", 2014, "single", "6"): {"primary": "business-5-15", "secondary": "business-3-20"},
    ("higher", 2014, "single", "9"): {"primary": "business-4-18"},
    ("ordinary", 2014, "single", "S2Q3"): {"primary": "business-5-15", "secondary": "business-3-18"},
    ("higher", 2016, "single", "1"): {"primary": "business-5-15", "secondary": "business-2-11"},
    ("higher", 2016, "single", "3"): {"primary": "business-5-15"},
    ("ordinary", 2016, "single", "11"): {"primary": "business-5-15"},

    ("higher", 2026, "p1", "1"): {"primary": "business-4-15"},
    ("higher", 2026, "p1", "2"): {"primary": "business-3-21", "secondary": "business-6-15"},
    ("higher", 2026, "p1", "3"): {"primary": "business-2-12"},
    ("higher", 2026, "p1", "4"): {"primary": "business-5-14"},
    ("higher", 2026, "p1", "5"): {"primary": "business-6-14"},
    ("higher", 2026, "p1", "6"): {"primary": "business-0-12", "secondary": "business-5-15"},
    ("higher", 2026, "p1", "7"): {"primary": "business-5-14"},
    ("higher", 2026, "p1", "8"): {"primary": "business-5-16"},
    ("higher", 2026, "p1", "9"): {"primary": "business-3-17"},
    ("higher", 2026, "p1", "10"): {"primary": "business-3-19"},
    ("higher", 2026, "p1", "11"): {"primary": "business-4-18"},
    ("higher", 2026, "p1", "12"): {"primary": "business-2-11"},
    ("higher", 2026, "p2", "ABQ"): {"primary": "business-4-19"},
    ("higher", 2026, "p2", "1"): {"primary": "business-0-12", "secondary": "business-0-13"},
    ("higher", 2026, "p2", "2"): {"primary": "business-5-17", "secondary": "business-5-15"},
    ("higher", 2026, "p2", "3"): {"primary": "business-6-13", "secondary": "business-6-14"},
    ("higher", 2026, "p2", "4"): {"primary": "business-0-14"},
    ("higher", 2026, "p2", "5"): {"primary": "business-1-5", "secondary": "business-2-11"},
    ("higher", 2026, "p2", "6"): {"primary": "business-3-20", "secondary": "business-3-18"},
    ("higher", 2026, "p2", "7"): {"primary": "business-3-19", "secondary": "business-4-14"},
    ("higher", 2026, "p2", "8"): {"primary": "business-4-17", "secondary": "business-4-18"},

    ("ordinary", 2026, "p1", "1"): {"primary": "business-4-17", "secondary": "business-3-18"},
    ("ordinary", 2026, "p1", "2"): {"primary": "business-2-13"},
    ("ordinary", 2026, "p1", "3"): {"primary": "business-4-17"},
    ("ordinary", 2026, "p1", "4"): {"primary": "business-6-14"},
    ("ordinary", 2026, "p1", "5"): {"primary": "business-6-13"},
    ("ordinary", 2026, "p1", "6"): {"primary": "business-1-5"},
    ("ordinary", 2026, "p1", "7"): {"primary": "business-2-11"},
    ("ordinary", 2026, "p1", "8"): {"primary": "business-3-17"},
    ("ordinary", 2026, "p1", "9"): {"primary": "business-2-13"},
    ("ordinary", 2026, "p1", "10"): {"primary": "business-3-18"},
    ("ordinary", 2026, "p1", "11"): {"primary": "business-0-13"},
    ("ordinary", 2026, "p1", "12"): {"primary": "business-5-15"},
    ("ordinary", 2026, "p1", "13"): {"primary": "business-4-14"},
    ("ordinary", 2026, "p1", "14"): {"primary": "business-3-19"},
    ("ordinary", 2026, "p1", "15"): {"primary": "business-0-12"},
    ("ordinary", 2026, "p2", "1"): {"primary": "business-0-13"},
    ("ordinary", 2026, "p2", "2"): {"primary": "business-5-13", "secondary": "business-5-17"},
    ("ordinary", 2026, "p2", "3"): {"primary": "business-6-13", "secondary": "business-5-15"},
    ("ordinary", 2026, "p2", "4"): {"primary": "business-0-14", "secondary": "business-0-12"},
    ("ordinary", 2026, "p2", "5"): {"primary": "business-1-5", "secondary": "business-2-11"},
    ("ordinary", 2026, "p2", "6"): {"primary": "business-4-16", "secondary": "business-3-16"},
    ("ordinary", 2026, "p2", "7"): {"primary": "business-3-20", "secondary": "business-4-17"},
    ("ordinary", 2026, "p2", "8"): {"primary": "business-4-14", "secondary": "business-4-16"},
    ("ordinary", 2026, "p2", "9"): {"primary": "business-5-16", "secondary": "business-4-18"},
}


def clean(value: str) -> str:
    return re.sub(r"\s+", " ", value.replace("\u00a0", " ")).strip()


def paper_index() -> list[dict]:
    source = INDEX_PATH.read_text()
    match = re.search(
        r'  "business": (\[[\s\S]*?\n  \]),\n  "chemistry":',
        source,
    )
    if not match:
        raise RuntimeError("Could not locate Business in paperTrailData.ts")
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


def expected_numbers(level: str, year: int, paper_key: str) -> list[str]:
    if year <= 2019:
        if level == "higher":
            return (
                [str(n) for n in range(1, 11)]
                + ["ABQ"]
                + [f"S3Q{n}" for n in range(1, 8)]
            )
        return [str(n) for n in range(1, 16)] + [f"S2Q{n}" for n in range(1, 9)]
    if level == "higher":
        if paper_key == "p1":
            return [str(n) for n in range(1, 11 if year == 2020 else 13)]
        return ["ABQ"] + [str(n) for n in range(1, 8 if year == 2020 else 9)]
    if paper_key == "p1":
        return [str(n) for n in range(1, 16)]
    return [str(n) for n in range(1, 9 if year == 2020 else 10)]


def parse_reference_heading(heading: str, level: str) -> dict:
    normalized = clean(heading)
    year_match = re.match(r"^(\d{4})\s*-\s*(.*)$", normalized)
    question_match = re.search(r"Question\s+(ABQ|A-C|[A-C]|\d+)", normalized, re.I)
    if not year_match or not question_match:
        raise RuntimeError(f"Unparseable Business reference heading: {heading}")
    year = int(year_match.group(1))
    rest = year_match.group(2)
    sitting = (
        "deferred"
        if re.search(r"Deferred Exam Paper", rest, re.I)
        else "sample"
        if re.search(r"Sample Paper", rest, re.I)
        else "main"
    )
    token = question_match.group(1).upper()
    sections: list[str] = []
    for match in re.finditer(r"Sections?\s+([123AB])(?:\s*&\s*([123]))?", rest, re.I):
        sections.extend(value.upper() for value in match.groups() if value)

    paper_key = "single"
    if year >= 2020:
        if re.match(r"Paper\s*-\s*Sections?\s+2(?:\s*&\s*3)?", rest, re.I):
            paper_key = "p2"
        elif re.match(r"Paper\s*-\s*Section\s+1", rest, re.I):
            paper_key = "p1"
        else:
            paper_key = "p1" if sections and sections[0] in {"1", "A"} else "p2"

    if level == "higher":
        semantic_section = sections[-1] if sections else ""
        if (
            token in {"ABQ", "A", "B", "C", "A-C"}
            or semantic_section in {"2", "B"}
        ):
            number = "ABQ"
        elif year <= 2019 and semantic_section == "3":
            number = f"S3Q{token}"
        else:
            number = token
    else:
        number = (
            f"S2Q{token}"
            if year <= 2019 and sections and sections[0] in {"2", "B"}
            else token
        )
    return {
        "year": year,
        "sitting": sitting,
        "paperKey": paper_key,
        "number": number,
    }


def reference_nodes(reference: dict, crosswalk: dict) -> dict[tuple[str, int, str, str], list[str]]:
    result: dict[tuple[str, int, str, str], list[str]] = {}
    # The outgoing taxonomy is the closest canonical source for Paper Trail's
    # two broad tags. New-course associations are retained in the runtime join.
    for variant in ("higher-old-course", "ordinary-old-course"):
        level = "higher" if variant.startswith("higher") else "ordinary"
        for topic in reference["variants"][variant]["topics"]:
            for heading in topic["officialQuestionHeadings"]:
                parsed = parse_reference_heading(heading, level)
                if parsed["year"] < 2010 or parsed["sitting"] != "main":
                    continue
                key = (level, parsed["year"], parsed["paperKey"], parsed["number"])
                nodes = result.setdefault(key, [])
                for node in crosswalk[topic["id"]]:
                    if node not in nodes:
                        nodes.append(node)
    return result


def line_records(document: fitz.Document) -> list[tuple[int, float, float, str]]:
    records: list[tuple[int, float, float, str]] = []
    for page_number, page in enumerate(document, start=1):
        for block in page.get_text("dict")["blocks"]:
            for line in block.get("lines", []):
                text = clean(" ".join(span["text"] for span in line.get("spans", [])))
                if text:
                    records.append(
                        (
                            page_number,
                            line["bbox"][0] / page.rect.width,
                            line["bbox"][1] / page.rect.height,
                            text,
                        )
                    )
    return records


def section_position(records: list[tuple[int, float, float, str]], number: int):
    pattern = re.compile(rf"^(?:SECTION|ROINN)\s*{number}$", re.I)
    matches = [(page, round(y, 4)) for page, _x, y, text in records if page > 1 and pattern.match(text)]
    return matches[0] if matches else None


def bare_numbers(
    records: list[tuple[int, float, float, str]],
    lower: tuple[int, float] | None,
    upper: tuple[int, float] | None,
    wanted: list[int],
) -> dict[int, tuple[int, float]]:
    found: dict[int, tuple[int, float]] = {}
    if lower is None:
        return found
    for page, x, y, text in records:
        position = (page, y)
        if position <= lower or (upper is not None and position >= upper) or x >= 0.13:
            continue
        match = re.match(r"^(\d{1,2})\s*[.]\s*(?:$|\D)", text)
        if match and int(match.group(1)) in wanted:
            found.setdefault(int(match.group(1)), (page, round(y, 4)))
    return found


def word_numbers(
    records: list[tuple[int, float, float, str]],
    lower: tuple[int, float] | None,
    wanted: list[int],
) -> dict[int, tuple[int, float]]:
    found: dict[int, tuple[int, float]] = {}
    if lower is None:
        return found
    pattern = re.compile(r"^(?:QUESTION|CEIST)\s*(\d{1,2})$", re.I)
    for page, _x, y, text in records:
        match = pattern.match(text)
        if match and (page, y) > lower and int(match.group(1)) in wanted:
            found.setdefault(int(match.group(1)), (page, round(y, 4)))
    return found


def detected_anchors(
    document: fitz.Document,
    level: str,
    year: int,
    paper_key: str,
) -> dict[str, tuple[int, float]]:
    records = line_records(document)
    section_1 = section_position(records, 1)
    section_2 = section_position(records, 2)
    section_3 = section_position(records, 3)
    result: dict[str, tuple[int, float]] = {}
    if paper_key == "single":
        short_count = 10 if level == "higher" else 15
        for number, position in bare_numbers(
            records, section_1, section_2, list(range(1, short_count + 1)),
        ).items():
            result[str(number)] = position
        if level == "higher":
            if section_2:
                result["ABQ"] = section_2
            for number, position in word_numbers(
                records, section_3, list(range(1, 8)),
            ).items():
                result[f"S3Q{number}"] = position
        else:
            for number, position in word_numbers(
                records, section_2, list(range(1, 9)),
            ).items():
                result[f"S2Q{number}"] = position
    elif paper_key == "p1":
        count = (10 if year == 2020 else 12) if level == "higher" else 15
        for number, position in bare_numbers(
            records, section_1, section_2 or (999, 1.0), list(range(1, count + 1)),
        ).items():
            result[str(number)] = position
    elif level == "higher":
        if section_2:
            result["ABQ"] = section_2
        count = 7 if year == 2020 else 8
        for number, position in word_numbers(
            records, section_3, list(range(1, count + 1)),
        ).items():
            result[str(number)] = position
    else:
        count = 8 if year == 2020 else 9
        for number, position in word_numbers(
            records, section_2, list(range(1, count + 1)),
        ).items():
            result[str(number)] = position
    return result


def classic_anchors(
    level: str,
    year: int,
    paper_key: str,
    fileid: str,
) -> dict[str, tuple[int, float]]:
    path = ANSWERS_ROOT / str(year) / f"{fileid}.json"
    if not path.exists():
        return {}
    answer_map = json.loads(path.read_text())
    by_number = {question["n"]: question for question in answer_map["q"]}

    def position(number: str):
        question = by_number.get(number)
        return (
            (question["pP"], round(question["pY"][0], 4))
            if question and question.get("pP") and question.get("pY")
            else None
        )

    result: dict[str, tuple[int, float]] = {}
    if year <= 2019 and level == "higher":
        translations = {
            **{str(number): str(number) for number in range(1, 11)},
            "ABQ": "11",
            **{f"S3Q{number}": str(number + 11) for number in range(1, 8)},
        }
    elif year <= 2019:
        translations = {
            **{str(number): str(number) for number in range(1, 16)},
            **{f"S2Q{number}": str(number + 15) for number in range(1, 9)},
        }
    else:
        translations = {number: number for number in expected_numbers(level, year, paper_key)}
        # Existing Higher Paper-2 maps address Section 3 Q1… only. ABQ is the
        # separate preceding task and intentionally has no legacy numeric alias.
        translations.pop("ABQ", None)
    for target, source in translations.items():
        value = position(source)
        if value:
            result[target] = value
    return result


def label_for(level: str, year: int, paper_key: str, number: str) -> str:
    if number == "ABQ":
        return "Section 2 · Applied Business Question"
    if number.startswith("S3Q"):
        return f"Section 3 · Question {number[3:]}"
    if number.startswith("S2Q"):
        return f"Section 2 · Question {number[3:]}"
    section = "1" if paper_key == "p1" or year <= 2019 else "3" if level == "higher" else "2"
    return f"Section {section} · Question {number}"


def paper_tail(
    document: fitz.Document,
    last: tuple[int, float],
) -> tuple[int, float]:
    markers = (
        "answerbook for section",
        "freagarleabhar do roinn",
        "there is no examination material",
        "níl aon ábhar scrúdaithe",
        "blank page",
        "leathanach bán",
        "copyright notice",
    )
    for page_number in range(last[0] + 1, len(document) + 1):
        text = clean(document[page_number - 1].get_text("text")).casefold()
        if not text or any(marker in text for marker in markers):
            return max(last[0], page_number - 1), 0.95
    return len(document), 0.95


def hosted_map(
    fileid: str,
    level: str,
    year: int,
    paper_key: str,
    anchors: dict[str, tuple[int, float]],
    tail: tuple[int, float],
) -> tuple[dict, int]:
    wanted = expected_numbers(level, year, paper_key)
    questions: list[dict] = []
    maximum_span = 0
    for index, number in enumerate(wanted):
        start = anchors[number]
        end = anchors[wanted[index + 1]] if index + 1 < len(wanted) else tail
        if end <= start:
            raise RuntimeError(f"{year}/{fileid} {number}: invalid anchor range {start}..{end}")
        span = end[0] - start[0]
        maximum_span = max(maximum_span, span)
        questions.append(
            {
                "n": number,
                "pP": start[0],
                "pY": [start[1], 1],
                "region": [{"p": 1}],
                "mode": "pagejump",
                "conf": 0.5,
                "label": label_for(level, year, paper_key, number),
                "printOrder": index + 1,
                "endP": end[0],
                "endY": end[1],
            }
        )
    if maximum_span > 10:
        raise RuntimeError(f"{year}/{fileid}: implausible crop span {maximum_span}")
    component = re.search(r"LP(\d{3})", fileid)
    return {
        "v": 1,
        "paperFileid": fileid,
        "schemeFileid": "",
        "component": component.group(1) if component else "000",
        "band": [1, 1],
        "copyright": COPYRIGHT,
        "paperOnly": 1,
        **({"maxCropPages": maximum_span} if maximum_span > 3 else {}),
        "q": questions,
    }, maximum_span


def main() -> None:
    entries = paper_index()
    existing = json.loads(TAGS_PATH.read_text())
    baseline = json.loads(BASELINE_PATH.read_text())
    reference = json.loads(REFERENCE_PATH.read_text())
    crosswalk = json.loads(CROSSWALK_PATH.read_text())
    nodes_by_card = reference_nodes(reference, crosswalk)
    canonical_ids = {
        node
        for nodes in crosswalk.values()
        for node in nodes
        if not node.startswith("business-2027-")
    }

    existing_by_id = {identity(paper): paper for paper in existing}
    existing_logical: dict[tuple[str, int, str, str], dict[str, str]] = {}
    for paper in existing:
        for question in paper["q"]:
            key = (paper["level"], paper["year"], paper["paperKey"], question["n"])
            existing_logical.setdefault(
                key,
                {
                    field: question[field]
                    for field in ("primary", "secondary")
                    if question.get(field)
                },
            )

    def tags_for(level: str, year: int, paper_key: str, number: str) -> dict[str, str]:
        key = (level, year, paper_key, number)
        if key in existing_logical:
            return copy.deepcopy(existing_logical[key])
        nodes = nodes_by_card.get(key, [])
        if nodes:
            return {"primary": nodes[0], **({"secondary": nodes[1]} if len(nodes) > 1 else {})}
        if key in MANUAL_TAGS:
            return copy.deepcopy(MANUAL_TAGS[key])
        raise RuntimeError(f"No reviewed Business tag for {key}")

    documents: list[dict] = []
    anchor_inputs: dict[str, dict] = {}
    for entry in entries:
        for item in entry["papers"]:
            label = item["label"].casefold()
            paper_key = "single" if len(entry["papers"]) == 1 else "p1" if "section 1" in label else "p2"
            fileid = item["doc"]["f"]
            paper_path = CORPUS / str(entry["year"]) / fileid
            if not paper_path.exists():
                raise FileNotFoundError(paper_path)
            paper_id = "|".join(
                [entry["level"], entry["lang"], str(entry["year"]), paper_key, fileid]
            )
            old_paper = existing_by_id.get(paper_id)
            old_questions = {question["n"]: question for question in (old_paper or {}).get("q", [])}
            questions = []
            for number in expected_numbers(entry["level"], entry["year"], paper_key):
                question = (
                    copy.deepcopy(old_questions[number])
                    if number in old_questions
                    else {"n": number, **tags_for(entry["level"], entry["year"], paper_key, number)}
                )
                if question["primary"] not in canonical_ids or (
                    question.get("secondary") and question["secondary"] not in canonical_ids
                ):
                    raise RuntimeError(f"{paper_id} {number}: invalid outgoing Business tag")
                questions.append(question)
            documents.append(
                {
                    "subjectId": "business",
                    "level": entry["level"],
                    "lang": entry["lang"],
                    "year": entry["year"],
                    "fileid": fileid,
                    "paperKey": paper_key,
                    "q": questions,
                }
            )
            with fitz.open(paper_path) as document:
                anchors = classic_anchors(
                    entry["level"], entry["year"], paper_key, fileid,
                )
                for number, position in detected_anchors(
                    document, entry["level"], entry["year"], paper_key,
                ).items():
                    anchors.setdefault(number, position)
                anchor_inputs[paper_id] = {
                    "paperPath": paper_path,
                    "fileid": fileid,
                    "level": entry["level"],
                    "lang": entry["lang"],
                    "year": entry["year"],
                    "paperKey": paper_key,
                    "anchors": anchors,
                }

    # A text-layer defect in one language may hide a header. Official-language
    # siblings share pagination/layout, so copy only the missing normalized
    # coordinate from the independently detected or mapped sibling.
    for paper_id, item in anchor_inputs.items():
        wanted = expected_numbers(item["level"], item["year"], item["paperKey"])
        for number in wanted:
            if number in item["anchors"]:
                continue
            siblings = [
                candidate
                for candidate in anchor_inputs.values()
                if candidate["level"] == item["level"]
                and candidate["year"] == item["year"]
                and candidate["paperKey"] == item["paperKey"]
                and candidate["lang"] != item["lang"]
                and number in candidate["anchors"]
            ]
            if len(siblings) != 1:
                raise RuntimeError(f"{paper_id}: missing anchor {number}")
            item["anchors"][number] = siblings[0]["anchors"][number]

    ids = [identity(paper) for paper in documents]
    if len(ids) != len(set(ids)):
        raise RuntimeError("Duplicate Business document identity")
    if len(documents) != EXPECTED_DOCUMENTS:
        raise RuntimeError(f"Expected {EXPECTED_DOCUMENTS} documents, found {len(documents)}")
    card_count = sum(len(paper["q"]) for paper in documents)
    if card_count != EXPECTED_CARDS:
        raise RuntimeError(f"Expected {EXPECTED_CARDS} cards, found {card_count}")

    preserved = 0
    for expected in baseline:
        paper_id = identity(expected)
        live = next((paper for paper in documents if identity(paper) == paper_id), None)
        if live is None:
            raise RuntimeError(f"Preservation failure: missing {paper_id}")
        old = existing_by_id[paper_id]
        live_questions = {question["n"]: question for question in live["q"]}
        old_questions = {question["n"]: question for question in old["q"]}
        for number in expected["questions"]:
            if live_questions.get(number) != old_questions.get(number):
                raise RuntimeError(f"Preservation failure: changed {paper_id} {number}")
            preserved += 1

    maximum_span = 0
    for item in anchor_inputs.values():
        with fitz.open(item["paperPath"]) as document:
            wanted = expected_numbers(item["level"], item["year"], item["paperKey"])
            positions = [item["anchors"][number] for number in wanted]
            if any(right <= left for left, right in zip(positions, positions[1:])):
                raise RuntimeError(f"{item['paperPath']}: non-monotonic complete anchors")
            tail = paper_tail(document, positions[-1])
            anchor_map, span = hosted_map(
                item["fileid"],
                item["level"],
                item["year"],
                item["paperKey"],
                item["anchors"],
                tail,
            )
        maximum_span = max(maximum_span, span)
        target_dir = HOSTED_ROOT / str(item["year"])
        target_dir.mkdir(parents=True, exist_ok=True)
        (target_dir / f"{item['fileid']}.json").write_text(
            json.dumps(anchor_map, ensure_ascii=False, separators=(",", ":")) + "\n"
        )

    TAGS_PATH.write_text(json.dumps(documents, indent=1, ensure_ascii=False) + "\n")
    print(
        json.dumps(
            {
                "paperDocuments": len(documents),
                "physicalCards": card_count,
                "distinctStudentFacingQuestions": sum(
                    len(paper["q"]) for paper in documents if paper["lang"] == "ev"
                ),
                "hostedAnchorMapsWritten": len(anchor_inputs),
                "preservedBaselineVariants": len(baseline),
                "preservedBaselineCards": preserved,
                "maximumHostedCropSpanPages": maximum_span,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
