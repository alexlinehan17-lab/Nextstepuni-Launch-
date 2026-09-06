#!/usr/bin/env python3
"""Build complete paper-only topic anchors for LC Later Modern History.

The generic Paper Trail pass currently exposes only the four parts of the
documents-based question.  The same official booklet also prints eleven
Ireland / Europe topic blocks, each of which is an independently selectable
exam task.  This subject-specific pass preserves every shipped DQB card and
adds one stable card for every printed topic block in all entitled local SEC
editions.

No StudyClix question text, image, solution, mock paper, or PDF is read here.
All topic identities and crop coordinates are independently derived from the
local SEC papers.

Run from the repository root:
    python3 scripts/paper-trail/history.py
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
TAGS_PATH = HERE / "topic-tags" / "tags" / "history.json"
BASELINE_PATH = ROOT / "test" / "fixtures" / "historyTopicQuestionBaseline.json"
HOSTED_ROOT = ROOT / "public" / "paper-anchors"

COPYRIGHT = "© State Examinations Commission"

TOPIC_MAIN_IDS = {
    "I": {number: f"history-2-{(number - 1) * 4}" for number in range(1, 7)},
    "E": {number: f"history-3-{(number - 1) * 4}" for number in range(1, 7)},
}

# 2026 was added to the entitled corpus after the legacy four-card tag file
# was generated.  Its official DQB is Ireland Topic 2, case study: GAA to 1891.
NEW_DQB_TAGS = {
    2026: {"primary": "history-2-7", "secondary": "history-2-4"},
}

IRELAND_HEADING = re.compile(
    r"^(?:Ireland|Éire)\s*:?\s*(?:Topic|Topaic)\s*([1-6])",
    re.IGNORECASE,
)
EUROPE_HEADING = re.compile(
    r"^(?:Europe and the wider world|An Eoraip agus an domhan mór)"
    r"\s*:?\s*(?:Topic|Topaic)\s*([1-6])",
    re.IGNORECASE,
)


def clean(text: str) -> str:
    return re.sub(r"\s+", " ", text.replace("\u00a0", " ")).strip()


def paper_index() -> list[dict]:
    source = INDEX_PATH.read_text()
    match = re.search(
        r'  "history": (\[[\s\S]*?\n  \]),\n  "history-early-modern":',
        source,
    )
    if not match:
        raise RuntimeError("Could not locate History in paperTrailData.ts")
    return json.loads(re.sub(r",\s*]$", "]", match.group(1)))


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


def dqb_topic(document: fitz.Document, pdf_path: Path) -> tuple[str, int]:
    if len(document) < 2:
        raise RuntimeError(f"{pdf_path}: no DQB page")
    page_text = clean(document[1].get_text("text"))
    ireland = re.search(
        r"(?:Later Modern )?(?:Ireland|Éire)\s*:\s*(?:Topic|Topaic)\s*([1-6])",
        page_text,
        re.IGNORECASE,
    )
    europe = re.search(
        r"(?:Europe and the wider world|An Eoraip agus an domhan mór)"
        r"\s*:\s*(?:Topic|Topaic)\s*([1-6])",
        page_text,
        re.IGNORECASE,
    )
    if bool(ireland) == bool(europe):
        raise RuntimeError(
            f"{pdf_path}: expected exactly one Ireland/Europe DQB topic, "
            f"found Ireland={ireland and ireland.group(1)}, "
            f"Europe={europe and europe.group(1)}"
        )
    match = ireland or europe
    return ("I" if ireland else "E", int(match.group(1)))


def line_records(page: fitz.Page) -> list[tuple[str, float]]:
    records: list[tuple[str, float]] = []
    for block in page.get_text("dict")["blocks"]:
        for line in block.get("lines", []):
            text = clean("".join(span["text"] for span in line.get("spans", [])))
            if text:
                records.append((text, line["bbox"][1] / page.rect.height))
    return records


def topic_anchors(
    document: fitz.Document,
    pdf_path: Path,
    entry: dict,
    dqb: tuple[str, int],
) -> tuple[list[dict], tuple[int, float], list[dict]]:
    by_family: dict[str, list[dict]] = {"I": [], "E": []}
    section_three: tuple[int, float] | None = None

    # Pages 1-3 contain instructions and DQB source material.  The independently
    # selectable essay / structured topic blocks always begin on page 4.
    for page_number, page in enumerate(document, start=1):
        if page_number < 4:
            continue
        for text, y_fraction in line_records(page):
            compact = clean(text)
            if re.match(r"^(?:SECTION|ROINN)\s*3\b", compact, re.IGNORECASE):
                section_three = section_three or (
                    page_number,
                    round(y_fraction, 4),
                )
            ireland = IRELAND_HEADING.match(compact)
            europe = EUROPE_HEADING.match(compact)
            if ireland:
                by_family["I"].append(
                    {
                        "observed": int(ireland.group(1)),
                        "page": page_number,
                        "y": round(y_fraction, 4),
                    }
                )
            elif europe:
                by_family["E"].append(
                    {
                        "observed": int(europe.group(1)),
                        "page": page_number,
                        "y": round(y_fraction, 4),
                    }
                )

    if section_three is None:
        raise RuntimeError(f"{pdf_path}: missing Section 3 header")

    corrections: list[dict] = []
    mapped: list[dict] = []
    for family in ("I", "E"):
        expected = [
            number
            for number in range(1, 7)
            if dqb != (family, number)
        ]
        anchors = by_family[family]
        observed = [anchor["observed"] for anchor in anchors]
        if len(anchors) != len(expected):
            raise RuntimeError(
                f"{pdf_path}: expected {family} topics {expected}, found {observed}"
            )
        if observed != expected:
            known_2010_ol_typo = (
                entry["year"] == 2010
                and entry["level"] == "ordinary"
                and entry["lang"] == "ev"
                and family == "I"
                and observed == [1, 2, 3, 4, 5]
                and expected == [1, 2, 3, 4, 6]
            )
            if not known_2010_ol_typo:
                raise RuntimeError(
                    f"{pdf_path}: unexpected {family} topic sequence "
                    f"{observed}; expected {expected}"
                )
            corrections.append(
                {
                    "year": 2010,
                    "level": "ordinary",
                    "lang": "ev",
                    "printedHeading": "Ireland: Topic 5",
                    "resolvedTopic": "Ireland: Topic 6",
                    "evidence": (
                        "The block title and content are Government, economy and "
                        "society in the Republic of Ireland, 1949-1989; Topic 5 is "
                        "already the documents-based question and is excluded from "
                        "Section 2 by the paper instructions."
                    ),
                }
            )

        # Physical syllabus order is authoritative here.  Assigning the
        # expected sequence also corrects the one verified 2010 OL header typo.
        for anchor, number in zip(anchors, expected):
            mapped.append({**anchor, "family": family, "number": number})

    mapped.sort(key=lambda anchor: (anchor["page"], anchor["y"]))
    if [anchor["family"] for anchor in mapped] != (
        ["I"] * len(by_family["I"]) + ["E"] * len(by_family["E"])
    ):
        raise RuntimeError(f"{pdf_path}: non-monotonic Ireland/Europe topic blocks")
    return mapped, section_three, corrections


def alternative_anchor(
    document: fitz.Document,
    pdf_path: Path,
    entry: dict,
    anchors: list[dict],
    dqb: tuple[str, int],
) -> dict | None:
    """Locate the extra OL Part-A task printed after the normal topic blocks."""
    candidates: list[tuple[int, float]] = []
    last_topic_page = max(anchor["page"] for anchor in anchors)
    for page_number, page in enumerate(document, start=1):
        if page_number <= last_topic_page:
            continue
        for text, y_fraction in line_records(page):
            if re.match(r"^A\s*\(\s*30\s+(?:marks|marc)\s*\)", text, re.IGNORECASE):
                candidates.append((page_number, round(y_fraction, 4)))

    expected = entry["level"] == "ordinary" and entry["year"] in {2023, 2024, 2025, 2026}
    if expected and len(candidates) != 1:
        raise RuntimeError(
            f"{pdf_path}: expected one alternative Part-A anchor, found {candidates}"
        )
    if not expected and candidates:
        raise RuntimeError(f"{pdf_path}: unexpected alternative Part-A anchor {candidates}")
    if not candidates:
        return None
    page_number, y_fraction = candidates[0]
    return {
        "family": dqb[0],
        "number": dqb[1],
        "page": page_number,
        "y": y_fraction,
        "alternative": True,
    }


def dqb_templates(existing: list[dict]) -> dict[int, dict]:
    templates: dict[int, dict] = {}
    for paper in existing:
        questions = [
            question
            for question in paper.get("q", [])
            if question.get("n") in {"1", "2", "3", "4"}
        ]
        if len(questions) != 4:
            continue
        tags = {
            (
                question.get("primary"),
                question.get("secondary"),
            )
            for question in questions
        }
        if len(tags) != 1:
            raise RuntimeError(
                f"{identity(paper)}: DQB questions do not share one topic tag"
            )
        primary, secondary = tags.pop()
        template = {
            "primary": primary,
            **({"secondary": secondary} if secondary else {}),
        }
        prior = templates.setdefault(paper["year"], template)
        if prior != template:
            raise RuntimeError(
                f"{paper['year']}: inconsistent DQB tags {prior} != {template}"
            )
    templates.update(NEW_DQB_TAGS)
    return templates


def main() -> None:
    entries = paper_index()
    existing = json.loads(TAGS_PATH.read_text())
    existing_by_id = {identity(paper): paper for paper in existing}
    year_dqb_tags = dqb_templates(existing)
    baseline = json.loads(BASELINE_PATH.read_text())

    papers: list[dict] = []
    hosted_maps: list[tuple[int, str, dict]] = []
    corrections: list[dict] = []
    dqb_topics_by_year: dict[int, str] = {}

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
            dqb = dqb_topic(document, paper_path)
            anchors, section_three, paper_corrections = topic_anchors(
                document,
                paper_path,
                entry,
                dqb,
            )
            alternative = alternative_anchor(
                document,
                paper_path,
                entry,
                anchors,
                dqb,
            )

        dqb_key = f"{dqb[0]}{dqb[1]}"
        prior_dqb = dqb_topics_by_year.setdefault(entry["year"], dqb_key)
        if prior_dqb != dqb_key:
            raise RuntimeError(
                f"{entry['year']}: level/language editions disagree on DQB "
                f"{prior_dqb} != {dqb_key}"
            )

        dqb_tag = year_dqb_tags.get(entry["year"])
        if not dqb_tag:
            raise RuntimeError(f"{entry['year']}: no canonical DQB tag")
        dqb_main = TOPIC_MAIN_IDS[dqb[0]][dqb[1]]
        if dqb_main not in {dqb_tag.get("primary"), dqb_tag.get("secondary")}:
            raise RuntimeError(
                f"{paper_path}: DQB {dqb_key} conflicts with canonical tags {dqb_tag}"
            )

        old_paper = existing_by_id.get(
            "|".join(
                [
                    entry["level"],
                    entry["lang"],
                    str(entry["year"]),
                    "single",
                    fileid,
                ]
            )
        )
        old_dqb = {
            question["n"]: question
            for question in (old_paper or {}).get("q", [])
            if question.get("n") in {"1", "2", "3", "4"}
        }
        questions = [
            copy.deepcopy(old_dqb.get(str(number)))
            if old_dqb.get(str(number))
            else {"n": str(number), **dqb_tag}
            for number in range(1, 5)
        ]

        for anchor in anchors:
            questions.append(
                {
                    "n": f"{anchor['family']}{anchor['number']}",
                    "primary": TOPIC_MAIN_IDS[anchor["family"]][anchor["number"]],
                }
            )
        if alternative:
            questions.append({"n": "ALT", **dqb_tag})

        paper = {
            "subjectId": "history",
            "level": entry["level"],
            "lang": entry["lang"],
            "year": entry["year"],
            "fileid": fileid,
            "paperKey": "single",
            "q": questions,
        }
        papers.append(paper)
        corrections.extend(paper_corrections)

        hosted_questions: list[dict] = []
        card_anchors = anchors + ([alternative] if alternative else [])
        for index, anchor in enumerate(card_anchors):
            if index + 1 < len(card_anchors):
                next_anchor = card_anchors[index + 1]
                end = (next_anchor["page"], next_anchor["y"])
                if anchor["family"] == "I" and next_anchor["family"] == "E":
                    end = section_three
                if next_anchor.get("alternative"):
                    end = (anchor["page"], 1.0)
            else:
                end = (anchor["page"], 1.0)
            if end[0] < anchor["page"] or (
                end[0] == anchor["page"] and end[1] <= anchor["y"] + 0.005
            ):
                raise RuntimeError(f"{paper_path}: invalid crop end for {anchor}")
            if end[0] - anchor["page"] > 3:
                raise RuntimeError(f"{paper_path}: implausible topic span for {anchor}")

            family_label = "Ireland" if anchor["family"] == "I" else "Europe & Wider World"
            section = 2 if anchor["family"] == "I" else 3
            number = "ALT" if anchor.get("alternative") else f"{anchor['family']}{anchor['number']}"
            label = (
                f"Alternative Part A · {family_label} Topic {anchor['number']}"
                if anchor.get("alternative")
                else f"Section {section} · {family_label} Topic {anchor['number']}"
            )
            hosted_questions.append(
                {
                    "n": number,
                    "pP": anchor["page"],
                    "pY": [anchor["y"], 1],
                    "region": [{"p": 1}],
                    "mode": "pagejump",
                    "conf": 0.5,
                    "label": label,
                    "printOrder": index + 1,
                    "endP": end[0],
                    "endY": end[1],
                }
            )
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
        raise RuntimeError(f"Duplicate History variants: {duplicates}")

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
                "dqbTopicsByYear": {
                    str(year): topic
                    for year, topic in sorted(dqb_topics_by_year.items())
                },
                "officialPaperCorrections": corrections,
            },
            indent=2,
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
