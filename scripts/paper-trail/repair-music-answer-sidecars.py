#!/usr/bin/env python3
"""Repair audited LC Music answer sidecars without inventing answer content.

Music's paper components restart question numbering while their marking scheme
is bundled. Older generic maps occasionally joined a component to a similarly
numbered block in the elective/practical tail. This script contains only the
scheme starts confirmed from the official rendered pages during the StudyClix
taxonomy migration. It also replaces stale paper-page coordinates with the
separately verified hosted paper anchor when the page itself changed.

Run with ``--check`` in CI and ``--write`` after deliberately updating the
audited layouts below.
"""

from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ANSWERS = ROOT / "scripts/paper-trail/answers"
HOSTED = ROOT / "public/paper-anchors"
INVENTORY = ROOT / "data/examTopics/music-audit-reconciliation.json"
FULL = [0.0, 0.0, 1.0, 1.0]

# Each entry is (question starts, exclusive section end), in one-based PDF
# coordinates. Same-page starts retain the exact visually checked table split.
REPAIR_LAYOUTS: dict[tuple[int, str], tuple[list[tuple[int, float]], tuple[int, float]]] = {
    (2010, "LC067GLP006EV.pdf"): (
        [(3, 0.0), (3, 0.3907), (3, 0.6641), (4, 0.0), (4, 0.2906), (4, 0.5890)],
        (5, 0.0),
    ),
    (2010, "LC067GLP006IV.pdf"): (
        [(2, 0.0), (2, 0.3787), (2, 0.6520), (3, 0.0), (3, 0.2896), (3, 0.5880)],
        (4, 0.0),
    ),
    (2010, "LC067GLP008EV.pdf"): (
        [(5, 0.0), (6, 0.0), (6, 0.3316), (6, 0.5888), (7, 0.0), (8, 0.0)],
        (9, 0.0),
    ),
    (2011, "LC067ALP006EV.pdf"): (
        [(3, 0.0), (3, 0.5471), (4, 0.0), (5, 0.0), (5, 0.6443), (6, 0.0)],
        (7, 0.0),
    ),
    (2011, "LC067ALP006IV.pdf"): (
        [(3, 0.0), (3, 0.5527), (4, 0.0), (5, 0.0), (5, 0.6445), (6, 0.0)],
        (7, 0.0),
    ),
    (2011, "LC067ALP008EV.pdf"): (
        [(8, 0.0), (8, 0.6443), (9, 0.0), (9, 0.5431), (10, 0.0), (11, 0.0)],
        (12, 0.0),
    ),
    (2011, "LC067ALP008IV.pdf"): (
        [(8, 0.0), (8, 0.6496)],
        (9, 0.0),
    ),
    (2011, "LC067GLP006EV.pdf"): (
        [(3, 0.0), (3, 0.4001), (3, 0.6439), (4, 0.0), (4, 0.3011), (4, 0.5197)],
        (5, 0.0),
    ),
    (2011, "LC067GLP006IV.pdf"): (
        [(3, 0.0), (3, 0.4001), (3, 0.6453), (4, 0.0), (4, 0.3011), (4, 0.5197)],
        (5, 0.0),
    ),
    (2013, "LC067ALP006EV.pdf"): (
        [(3, 0.0), (3, 0.5473), (4, 0.0), (5, 0.0), (5, 0.6445), (6, 0.0)],
        (7, 0.0),
    ),
    (2013, "LC067ALP006IV.pdf"): (
        [(3, 0.0), (3, 0.5527), (4, 0.0), (5, 0.0), (5, 0.6445), (6, 0.0)],
        (7, 0.0),
    ),
    (2013, "LC067ALP008EV.pdf"): (
        [(8, 0.0), (9, 0.0), (9, 0.3864), (9, 0.6224), (10, 0.0), (11, 0.0)],
        (12, 0.0),
    ),
    (2013, "LC067ALP008IV.pdf"): (
        [(8, 0.0), (9, 0.0), (9, 0.3973), (9, 0.6341), (10, 0.0), (11, 0.0)],
        (12, 0.0),
    ),
    (2013, "LC067GLP008EV.pdf"): (
        [(5, 0.0), (6, 0.0), (6, 0.3386), (6, 0.6219), (7, 0.0), (8, 0.0)],
        (9, 0.0),
    ),
    (2013, "LC067GLP006EV.pdf"): (
        [(3, 0.0), (3, 0.4001), (3, 0.6439), (4, 0.0), (4, 0.3011), (4, 0.5197)],
        (5, 0.0),
    ),
    (2013, "LC067GLP006IV.pdf"): (
        [(3, 0.0), (3, 0.4001), (3, 0.6453), (4, 0.0), (4, 0.3011), (4, 0.5197)],
        (5, 0.0),
    ),
    (2014, "LC067ALP006EV.pdf"): (
        [(3, 0.0), (4, 0.0), (5, 0.0), (6, 0.0), (7, 0.0), (8, 0.0)],
        (9, 0.0),
    ),
    (2014, "LC067ALP006IV.pdf"): (
        [(3, 0.0), (4, 0.0), (5, 0.0), (6, 0.0), (7, 0.0), (8, 0.0)],
        (9, 0.0),
    ),
    (2014, "LC067ALP008IV.pdf"): (
        [(11, 0.0), (12, 0.3740), (13, 0.0)],
        (14, 0.0),
    ),
    (2014, "LC067GLP008EV.pdf"): (
        [(7, 0.0), (8, 0.0), (9, 0.0), (10, 0.0), (11, 0.0), (12, 0.0)],
        (13, 0.0),
    ),
    (2014, "LC067GLP008IV.pdf"): (
        [(7, 0.0), (8, 0.0)],
        (9, 0.0),
    ),
    (2014, "LC067GLP006EV.pdf"): (
        [(3, 0.0), (4, 0.0), (5, 0.0), (6, 0.0), (6, 0.3741), (6, 0.6476)],
        (7, 0.0),
    ),
    (2014, "LC067GLP006IV.pdf"): (
        [(3, 0.0), (4, 0.0), (5, 0.0), (6, 0.0), (6, 0.3641), (6, 0.6377)],
        (7, 0.0),
    ),
    (2015, "LC067ALP006EV.pdf"): (
        [(3, 0.0), (4, 0.0), (5, 0.0), (6, 0.0), (7, 0.0), (8, 0.0)],
        (9, 0.0),
    ),
    (2016, "LC067ALP006EV.pdf"): (
        [(3, 0.0), (4, 0.0), (5, 0.0), (6, 0.0), (7, 0.0), (8, 0.0)],
        (9, 0.0),
    ),
    (2017, "LC067ALP006EV.pdf"): (
        [(3, 0.0), (4, 0.0), (5, 0.0), (6, 0.0), (7, 0.0), (8, 0.0)],
        (9, 0.0),
    ),
    (2017, "LC067ALP006IV.pdf"): (
        [(3, 0.0), (4, 0.0), (5, 0.0), (6, 0.0), (7, 0.0), (8, 0.0)],
        (9, 0.0),
    ),
    (2017, "LC067GLP006IV.pdf"): (
        [(3, 0.0), (4, 0.0), (5, 0.0670), (6, 0.0833), (7, 0.0670), (8, 0.0834)],
        (9, 0.0),
    ),
    (2018, "LC067ALP006EV.pdf"): (
        [(3, 0.0825), (4, 0.0867), (5, 0.0667), (6, 0.1075), (7, 0.1134), (8, 0.1065)],
        (9, 0.0),
    ),
    (2018, "LC067ALP006IV.pdf"): (
        [(3, 0.0875), (4, 0.0834), (5, 0.0636), (6, 0.1050), (7, 0.0607), (8, 0.1033)],
        (9, 0.0),
    ),
    (2018, "LC067GLP008IV.pdf"): (
        [(12, 0.0748), (14, 0.0721), (15, 0.0682), (16, 0.0721), (17, 0.0860), (18, 0.0993)],
        (19, 0.0),
    ),
    (2019, "LC067ALP006EV.pdf"): (
        [(3, 0.0), (4, 0.0), (5, 0.0), (6, 0.0), (7, 0.0), (8, 0.0)],
        (9, 0.0),
    ),
    (2019, "LC067ALP006IV.pdf"): (
        [(3, 0.0), (4, 0.0), (5, 0.0), (6, 0.0), (7, 0.0), (8, 0.0)],
        (9, 0.0),
    ),
    (2019, "LC067GLP006IV.pdf"): (
        [(3, 0.0), (4, 0.0), (5, 0.0611), (7, 0.1047), (8, 0.0611), (9, 0.0775)],
        (10, 0.0),
    ),
    (2020, "LC067ALP006IV.pdf"): (
        [(3, 0.0), (4, 0.0), (5, 0.0), (6, 0.0), (7, 0.0), (8, 0.0)],
        (9, 0.0),
    ),
    (2022, "LC067ALP006EV.pdf"): (
        [(3, 0.0), (4, 0.0), (5, 0.0), (6, 0.0), (7, 0.0), (8, 0.0)],
        (9, 0.0),
    ),
    (2022, "LC067ALP006IV.pdf"): (
        [(3, 0.0), (4, 0.0), (5, 0.0), (6, 0.0), (7, 0.0), (8, 0.0)],
        (9, 0.0),
    ),
    (2022, "LC067ALP008IV.pdf"): (
        [(11, 0.0712), (13, 0.0994), (14, 0.0888), (15, 0.0920), (16, 0.1376), (18, 0.1209)],
        (20, 0.0),
    ),
    (2023, "LC067ALP006IV.pdf"): (
        [(3, 0.0), (4, 0.0), (5, 0.0), (6, 0.0), (7, 0.0), (8, 0.0)],
        (9, 0.0),
    ),
    (2024, "LC067ALP006EV.pdf"): (
        [(3, 0.0), (4, 0.0), (5, 0.0), (6, 0.0), (7, 0.0), (9, 0.0)],
        (10, 0.0),
    ),
    (2024, "LC067ALP006IV.pdf"): (
        [(3, 0.0), (4, 0.0), (5, 0.0), (6, 0.0), (7, 0.0), (9, 0.0)],
        (10, 0.0),
    ),
    (2024, "LC067ALP008IV.pdf"): (
        [(14, 0.0888), (16, 0.1307), (17, 0.0897), (18, 0.0940), (19, 0.1037), (21, 0.0760)],
        (23, 0.0),
    ),
    (2025, "LC067ALP006EV.pdf"): (
        [(3, 0.0), (4, 0.0), (5, 0.0), (6, 0.0), (7, 0.0), (8, 0.0)],
        (9, 0.0),
    ),
}

# These deliberately incomplete Irish listening maps retain only their existing
# reviewed questions. Their legacy final crop nevertheless ran to the end of the
# listening band, swallowing later, unmapped questions. Each value is
# (final mapped question, exclusive next-question start), visually read from the
# official scheme; no new answer question is created.
PARTIAL_ENDS: dict[tuple[int, str], tuple[str, tuple[int, float]]] = {
    (2010, "LC067GLP008IV.pdf"): ("2", (5, 0.3305)),
    (2011, "LC067ALP008IV.pdf"): ("2", (9, 0.0)),
    (2013, "LC067GLP008IV.pdf"): ("2", (6, 0.3369)),
    (2014, "LC067ALP008IV.pdf"): ("3", (14, 0.0)),
    (2014, "LC067GLP008IV.pdf"): ("2", (9, 0.0)),
    (2015, "LC067ALP008IV.pdf"): ("2", (13, 0.0)),
    (2015, "LC067GLP008IV.pdf"): ("1", (11, 0.0)),
    (2016, "LC067ALP008IV.pdf"): ("2", (13, 0.0)),
    (2016, "LC067GLP008IV.pdf"): ("2", (12, 0.0)),
}


def region_between(start: tuple[int, float], end: tuple[int, float]) -> list[dict]:
    start_page, start_y = start
    end_page, end_y = end
    if (end_page, end_y) <= (start_page, start_y):
        raise RuntimeError(f"Invalid Music scheme interval {start} -> {end}")
    if start_page == end_page:
        return [{"p": start_page, "r": [0.0, start_y, 1.0, end_y]}]
    segments = [{"p": start_page, "r": [0.0, start_y, 1.0, 1.0]}]
    segments.extend({"p": page, "r": copy.copy(FULL)} for page in range(start_page + 1, end_page))
    if end_y > 0:
        segments.append({"p": end_page, "r": [0.0, 0.0, 1.0, end_y]})
    return segments


def repaired_regions(starts: list[tuple[int, float]], end: tuple[int, float]) -> dict[str, list[dict]]:
    ends = starts[1:] + [end]
    return {
        str(index + 1): region_between(start, stop)
        for index, (start, stop) in enumerate(zip(starts, ends))
    }


def desired_sidecar(year: int, fileid: str, sidecar: dict, hosted: dict) -> tuple[dict, int]:
    desired = copy.deepcopy(sidecar)
    hosted_by_number = {question["n"]: question for question in hosted["q"]}
    existing_by_number = {question["n"]: question for question in sidecar["q"]}
    layout = REPAIR_LAYOUTS.get((year, fileid))
    partial_end = PARTIAL_ENDS.get((year, fileid))
    regions = repaired_regions(*layout) if layout else None
    numbers = list(regions) if regions else [question["n"] for question in sidecar["q"]]
    questions = []
    corrected_paper_pages = 0
    for number in numbers:
        paper = hosted_by_number.get(number)
        if paper is None:
            raise RuntimeError(f"{year}/{fileid}: hosted paper anchor is missing Q{number}")
        existing = existing_by_number.get(number)
        question = copy.deepcopy(existing or {"n": number})
        if question.get("pP") != paper["pP"]:
            question["pP"] = paper["pP"]
            question["pY"] = copy.deepcopy(paper["pY"])
            corrected_paper_pages += 1
        if regions:
            question["mode"] = "crop"
            question["conf"] = 1
            question["region"] = regions[number]
        elif partial_end and number == partial_end[0]:
            first_segment = question["region"][0]
            first_rect = first_segment.get("r", FULL)
            question["region"] = region_between(
                (first_segment["p"], first_rect[1]), partial_end[1]
            )
        elif existing is None:
            question["mode"] = "crop"
            question["conf"] = 1
        if existing is None and paper.get("label"):
            question["label"] = paper["label"]
        questions.append(question)
    desired["q"] = questions
    if regions:
        desired["band"] = [layout[0][0][0], layout[1][0]]
    return desired, corrected_paper_pages


def validate(year: int, fileid: str, sidecar: dict, hosted: dict) -> None:
    expected = {question["n"] for question in hosted["q"]}
    seen: set[str] = set()
    for question in sidecar["q"]:
        number = question["n"]
        if number not in expected or number in seen:
            raise RuntimeError(f"{year}/{fileid}: invalid or duplicate Q{number}")
        seen.add(number)
        if question.get("mode") != "crop" or question.get("conf") != 1:
            raise RuntimeError(f"{year}/{fileid} Q{number}: answer is not a verified crop")
        total_area = 0.0
        previous: tuple[int, float] | None = None
        for segment in question.get("region", []):
            rect = segment.get("r", FULL)
            if (
                len(rect) != 4
                or any(not isinstance(value, (int, float)) or value < 0 or value > 1 for value in rect)
                or rect[2] <= rect[0]
                or rect[3] <= rect[1]
            ):
                raise RuntimeError(f"{year}/{fileid} Q{number}: invalid scheme rectangle {rect}")
            point = (segment["p"], rect[1])
            if previous is not None and point < previous:
                raise RuntimeError(f"{year}/{fileid} Q{number}: scheme segments run backwards")
            previous = (segment["p"], rect[3])
            total_area += (rect[2] - rect[0]) * (rect[3] - rect[1])
        if total_area < 0.12:
            raise RuntimeError(f"{year}/{fileid} Q{number}: implausibly small answer crop ({total_area:.4f})")


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--write", action="store_true")
    args = parser.parse_args()

    inventory = json.loads(INVENTORY.read_text())["inventory"]
    changed_files = repaired_files = corrected_pages = 0
    for paper in inventory:
        year = paper["year"]
        fileid = paper["fileid"]
        sidecar_path = ANSWERS / str(year) / f"{fileid}.json"
        if not sidecar_path.exists():
            continue
        hosted_path = HOSTED / str(year) / f"{fileid}.json"
        sidecar = json.loads(sidecar_path.read_text())
        hosted = json.loads(hosted_path.read_text())
        desired, page_changes = desired_sidecar(year, fileid, sidecar, hosted)
        validate(year, fileid, desired, hosted)
        changed = desired != sidecar
        if changed:
            changed_files += 1
            corrected_pages += page_changes
            if (year, fileid) in REPAIR_LAYOUTS or (year, fileid) in PARTIAL_ENDS:
                repaired_files += 1
            if args.write:
                sidecar_path.write_text(
                    json.dumps(desired, ensure_ascii=True, sort_keys=True, separators=(",", ":")) + "\n"
                )

    summary = {
        "answerMaps": sum(
            (ANSWERS / str(paper["year"]) / f'{paper["fileid"]}.json').exists()
            for paper in inventory
        ),
        "auditedSchemeRepairs": len(REPAIR_LAYOUTS) + len(PARTIAL_ENDS),
        "changedFiles": changed_files,
        "repairedFiles": repaired_files,
        "correctedPaperPages": corrected_pages,
        "mode": "write" if args.write else "check",
    }
    print(json.dumps(summary, indent=2))
    if args.check and changed_files:
        raise SystemExit("Music answer sidecars are not reconciled; run with --write")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
