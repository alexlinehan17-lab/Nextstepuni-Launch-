#!/usr/bin/env python3
"""Build complete paper-only anchors for LC Technology Section B/C booklets.

The generic Paper Trail pass currently anchors only the separate Section A
booklet. This subject-specific pass exposes the two core long questions and all
five option questions from the independently held SEC Section B/C PDFs.

No StudyClix question text, image, solution, mock paper, or PDF is read here.
The factual reference audit is reconciled separately; these crop boundaries
come solely from NextStepUni's entitled local SEC corpus.

Run from the repository root:
    python3 scripts/paper-trail/technology.py
"""

from __future__ import annotations

import json
from pathlib import Path

import fitz


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
CORPUS = ROOT / "paper-trail-corpus" / "exampapers"
HOSTED_ROOT = ROOT / "public" / "paper-anchors"
ANSWER_ROOT = HERE / "answers"
COPYRIGHT = "© State Examinations Commission"


def expected_documents() -> list[tuple[int, str, str, Path]]:
    documents: list[tuple[int, str, str, Path]] = []
    for year in range(2010, 2027):
        component = "015" if year <= 2018 else "039"
        for level, level_code in (("higher", "A"), ("ordinary", "G")):
            if year == 2020 and level == "ordinary":
                # There was no Ordinary-level November 2020 sitting in the SEC
                # corpus or the factual reference.
                continue
            for lang in ("ev", "iv"):
                fileid = f"LC065{level_code}LP{component}{lang.upper()}.pdf"
                documents.append((year, level, lang, CORPUS / str(year) / fileid))
    return documents


def question_pages(level: str) -> dict[str, list[int]]:
    # The official booklet layout is stable throughout 2010–2026. Higher C4
    # spans two pages; the other printed questions occupy one complete page.
    common = {
        "B2": [2],
        "B3": [3],
        "C1": [4],
        "C2": [5],
        "C3": [6],
        "C4": [7],
        "C5": [8],
    }
    if level == "higher":
        common["C4"] = [7, 8]
        common["C5"] = [9]
    return common


def validate_layout(pdf_path: Path, level: str) -> None:
    with fitz.open(pdf_path) as document:
        if len(document) != 12:
            raise RuntimeError(f"{pdf_path}: expected 12 pages, found {len(document)}")
        pages = question_pages(level)
        if pages["B2"][0] != 2 or pages["B3"][0] != 3 or pages["C1"][0] != 4:
            raise RuntimeError(f"{pdf_path}: invalid core/option page boundary")
        if max(page for span in pages.values() for page in span) >= len(document):
            raise RuntimeError(f"{pdf_path}: question page exceeds document")


def anchor_map(fileid: str, level: str) -> dict:
    cards = []
    for print_order, (number, pages) in enumerate(question_pages(level).items(), start=1):
        cards.append(
            {
                "n": number,
                "pP": pages[0],
                "pY": [0, 1],
                "region": [{"p": 1}],
                "mode": "pagejump",
                "conf": 0.5,
                "label": (
                    f"Section B · Question {number[1:]}"
                    if number.startswith("B")
                    else f"Section C · Option {number[1:]}"
                ),
                "printOrder": print_order,
                "paperRegion": [
                    {"p": page, "r": [0, 0, 1, 1]}
                    for page in pages
                ],
            }
        )
    return {
        "v": 1,
        "paperFileid": fileid,
        "schemeFileid": "",
        "component": "015" if "LP015" in fileid else "039",
        "band": [1, 1],
        "copyright": COPYRIGHT,
        "paperOnly": 1,
        "maxCropPages": 2,
        "q": cards,
    }


def mirrored_section_a_map() -> tuple[int, str, dict]:
    """Supply the one indexed Section-A edition without its own sidecar.

    The 2022 Higher English and Irish booklets have the same verified layout;
    the Irish answer map therefore supplies paper anchors only. No marking-
    scheme coordinates are copied into this honest paper-only fallback.
    """
    source = ANSWER_ROOT / "2022" / "LC065ALP014IV.pdf.json"
    data = json.loads(source.read_text())
    fileid = "LC065ALP014EV.pdf"
    questions = [
        {
            "n": question["n"],
            "pP": question["pP"],
            "pY": question["pY"],
            "region": [{"p": 1}],
            "mode": "pagejump",
            "conf": 0.5,
            "label": f"Section A · Question {question['n']}",
            "printOrder": index,
        }
        for index, question in enumerate(data["q"], start=1)
    ]
    if [question["n"] for question in questions] != [str(n) for n in range(1, 16)]:
        raise RuntimeError(f"{source}: incomplete Section A anchor source")
    return (
        2022,
        fileid,
        {
            "v": 1,
            "paperFileid": fileid,
            "schemeFileid": "",
            "component": "014",
            "band": [1, 1],
            "copyright": COPYRIGHT,
            "paperOnly": 1,
            "q": questions,
        },
    )


def main() -> None:
    documents = expected_documents()
    if len(documents) != 66:
        raise RuntimeError(f"Expected 66 Technology B/C editions, found {len(documents)}")

    maps = []
    for year, level, lang, pdf_path in documents:
        if not pdf_path.exists():
            raise FileNotFoundError(pdf_path)
        validate_layout(pdf_path, level)
        maps.append((year, level, lang, pdf_path.name, anchor_map(pdf_path.name, level)))

    identities = [(year, level, lang, fileid) for year, level, lang, fileid, _ in maps]
    if len(identities) != len(set(identities)):
        raise RuntimeError("Duplicate Technology B/C document identity")

    for year, _level, _lang, fileid, data in maps:
        target_dir = HOSTED_ROOT / str(year)
        target_dir.mkdir(parents=True, exist_ok=True)
        (target_dir / f"{fileid}.json").write_text(
            json.dumps(data, ensure_ascii=False, separators=(",", ":")) + "\n"
        )

    section_a_year, section_a_fileid, section_a_data = mirrored_section_a_map()
    section_a_dir = HOSTED_ROOT / str(section_a_year)
    section_a_dir.mkdir(parents=True, exist_ok=True)
    (section_a_dir / f"{section_a_fileid}.json").write_text(
        json.dumps(section_a_data, ensure_ascii=False, separators=(",", ":")) + "\n"
    )

    print(
        json.dumps(
            {
                "paperVariants": len(maps),
                "cards": sum(len(data["q"]) for *_, data in maps),
                "higherVariants": sum(level == "higher" for _, level, *_ in maps),
                "ordinaryVariants": sum(level == "ordinary" for _, level, *_ in maps),
                "hostedAnchorMaps": len(maps),
                "mirroredSectionAAnchors": 1,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
