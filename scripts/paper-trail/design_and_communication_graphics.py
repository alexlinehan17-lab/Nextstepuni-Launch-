#!/usr/bin/env python3
"""Complete the entitled DCG question corpus without mutating shipped cards.

The existing 62 Section-B/C tag records are frozen.  This generator adds the
four 2026 B/C records and every separately published Section-A sheet, then
emits paper-only maps.  Topic choices come from the factual reference-heading
snapshot plus a small, reviewed list of questions the reference omits.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from pypdf import PdfReader


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
SUBJECT_ID = "design-and-communication-graphics"
TAGS_PATH = HERE / "topic-tags" / "tags" / f"{SUBJECT_ID}.json"
REFERENCE_PATH = ROOT / "data" / "examTopics" / f"{SUBJECT_ID}.json"
CROSSWALK_PATH = ROOT / "data" / "examTopics" / f"{SUBJECT_ID}-curriculum-crosswalk.json"
BASELINE_PATH = ROOT / "test" / "fixtures" / "designAndCommunicationGraphicsTopicQuestionBaseline.json"
CORPUS_ROOT = ROOT / "paper-trail-corpus" / "exampapers"
DEFERRED_ROOT = ROOT / "paper-trail-corpus" / "deferredexams"
HOSTED_ROOT = ROOT / "public" / "paper-anchors"

LEVEL_CODE = {"higher": "A", "ordinary": "G"}
EXPECTED_YEARS = {
    "higher": list(range(2010, 2027)),
    "ordinary": [year for year in range(2010, 2027) if year != 2020],
}
LANGUAGES = ("ev", "iv")

H = "design-and-communication-graphics-higher-"
O = "design-and-communication-graphics-ordinary-"

# Directly reviewed against the entitled SEC sheets.  These 49 valid tasks do
# not appear in the factual reference headings; retaining them is deliberate.
REVIEWED_OMISSIONS: dict[str, list[str]] = {
    "higher|2010|single|5": [H + "structural-forms"],
    **{
        f"higher|{year}|single|8": [H + "assemblies"]
        for year in range(2010, 2027)
    },
    "higher|2012|section-a|3": [H + "orthographic-auxiliary-projection-plus"],
    "higher|2025|single|7": [H + "dynamic-mechanisms"],

    "ordinary|2010|section-a|1": [O + "conic-sections"],
    "ordinary|2010|section-a|2": [O + "solids-in-contact"],
    "ordinary|2010|section-a|3": [O + "orthographic-auxillary-projection"],
    "ordinary|2010|section-a|4": [O + "axonometric-projection"],
    "ordinary|2010|single|4": [O + "geological-geometry"],
    "ordinary|2011|section-a|1": [O + "axonometric-projection"],
    "ordinary|2011|section-a|3": [O + "conic-sections"],
    "ordinary|2011|single|5": [O + "structural-forms-developments"],
    "ordinary|2012|section-a|1": [O + "conic-sections"],
    "ordinary|2012|section-a|3": [O + "axonometric-projection"],
    "ordinary|2013|section-a|4": [O + "conic-sections"],
    "ordinary|2014|section-a|1": [O + "conic-sections"],
    "ordinary|2015|section-a|2": [O + "conic-sections"],
    "ordinary|2016|section-a|1": [O + "conic-sections"],
    "ordinary|2017|section-a|2": [O + "conic-sections"],
    "ordinary|2017|single|2": [O + "axonometric-projection"],
    "ordinary|2017|single|5": [O + "structural-forms-developments"],
    "ordinary|2018|section-a|1": [O + "conic-sections"],
    "ordinary|2018|single|3": [O + "axonometric-projection"],
    "ordinary|2019|section-a|3": [O + "conic-sections"],
    "ordinary|2019|section-a|4": [O + "orthographic-auxillary-projection"],
    "ordinary|2021|section-a|1": [O + "conic-sections"],
    "ordinary|2021|section-a|2": [O + "orthographic-auxillary-projection"],
    "ordinary|2022|section-a|2": [O + "conic-sections"],
    "ordinary|2023|section-a|1": [O + "conic-sections"],
    "ordinary|2024|section-a|1": [O + "conic-sections"],
    "ordinary|2024|single|3": [O + "interpenetration"],
    "ordinary|2025|section-a|2": [O + "conic-sections"],
    "ordinary|2026|section-a|1": [O + "conic-sections"],
}

# The SEC's deferred sittings in the archive: 2022 and 2023 Higher, each a
# Section A sheet and a Sections B and C booklet (deferredexams/<year>/
# LC562ALP014EV.pdf and LC562ALP039EV.pdf); no Ordinary, nothing for 2024 or
# 2025. Each booklet is its own Atlas paper, its file id the index's
# "LC562ALP014EV-deferred.pdf", numbered as June's, so its questions never
# replace or merge with June's question of the same number. English only: the
# 2023 Irish edition is deferred with every Irish-version paper. A sitting
# joins the Atlas with its Mark Bank cards (test/paperTrailSyllabus.test.ts,
# ADMITTED_DEFERRED), so this lists the deferred sittings carded.
DEFERRED_SITTINGS: tuple[tuple[int, str], ...] = ((2022, "higher"),)

# The reference heads every deferred question but Section C's assembly, C-5,
# in both years; each was read on its own booklet ("Details of a beam balance
# weighing scales", 2022; "a pipe vice for holding round bars", 2023, both a
# sectional elevation of an assembly), as REVIEWED_OMISSIONS reads June's.
DEFERRED_REVIEWED_OMISSIONS: dict[str, list[str]] = {
    f"higher|{year}|deferred|single|8": [H + "assemblies"] for year in (2022, 2023)
}

# A-sheet rectangles are stable quadrants on the rotated A3 page as rendered
# by pdf.js: left questions 1/2, right questions 3/4.
A_RECTS = {
    "1": [0.02, 0.07, 0.50, 0.505],
    "2": [0.02, 0.495, 0.50, 0.94],
    "3": [0.50, 0.07, 0.98, 0.505],
    "4": [0.50, 0.495, 0.98, 0.94],
}


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def paper_identity(paper: dict) -> str:
    return "|".join(
        [paper["level"], paper["lang"], str(paper["year"]), paper["paperKey"], paper["fileid"]]
    )


def logical_key(level: str, year: int, paper_key: str, number: str) -> str:
    return f"{level}|{year}|{paper_key}|{number}"


def parse_heading(heading: str) -> tuple[int, str, str, str]:
    normalized = re.sub(r"\s+", " ", heading).strip()
    year_match = re.match(r"(\d{4})", normalized)
    sections = re.findall(r"Section\s*([ABC])", normalized, flags=re.I)
    if not year_match or not sections:
        raise ValueError(f"Unparseable DCG heading: {heading}")
    section = sections[-1].upper()
    question_match = re.search(r"Question\s*(?:[ABC]\s*-?\s*)?(\d+)", normalized, flags=re.I)
    if not question_match and section == "B":
        question_match = re.search(r"Part\s*(\d+)\b", normalized, flags=re.I)
    if not question_match:
        raise ValueError(f"Unparseable DCG question number: {heading}")
    sitting = "deferred" if re.search(r"Deferred Exam", normalized, flags=re.I) else "main"
    return int(year_match.group(1)), sitting, section, question_match.group(1)


def local_slot(section: str, printed_number: str) -> tuple[str, str]:
    number = int(printed_number)
    if section == "A":
        return "section-a", str(number)
    if section == "B":
        return "single", str(number)
    if section == "C":
        return "single", str(number + 3)
    raise ValueError(f"Unexpected DCG section {section}")


def exact_topics(reference: dict) -> dict[str, list[str]]:
    result: dict[str, list[str]] = {}
    for level, level_data in reference["levels"].items():
        for topic in level_data["topics"]:
            for heading in topic["officialQuestionHeadings"]:
                year, sitting, section, printed = parse_heading(heading)
                if sitting != "main" or year not in EXPECTED_YEARS[level]:
                    continue
                paper_key, number = local_slot(section, printed)
                key = logical_key(level, year, paper_key, number)
                result.setdefault(key, [])
                if topic["id"] not in result[key]:
                    result[key].append(topic["id"])
    return result


def deferred_topics(reference: dict) -> dict[str, list[str]]:
    """exact_topics for the deferred headings, keyed level|year|deferred|paperKey|n."""
    result: dict[str, list[str]] = {}
    for level, level_data in reference["levels"].items():
        for topic in level_data["topics"]:
            for heading in topic["officialQuestionHeadings"]:
                year, sitting, section, printed = parse_heading(heading)
                if sitting != "deferred":
                    continue
                paper_key, number = local_slot(section, printed)
                key = f"{level}|{year}|deferred|{paper_key}|{number}"
                result.setdefault(key, [])
                if topic["id"] not in result[key]:
                    result[key].append(topic["id"])
    return result


def deferred_files(level: str, year: int) -> tuple[Path, Path]:
    code = LEVEL_CODE[level]
    candidates = sorted((DEFERRED_ROOT / str(year)).glob(f"LC562{code}LP*EV.pdf"))
    section_a = [path for path in candidates if len(PdfReader(path).pages) <= 3]
    section_bc = [path for path in candidates if len(PdfReader(path).pages) > 3]
    if len(section_a) != 1 or len(section_bc) != 1:
        raise ValueError(f"{level}|{year} deferred: expected one Section-A and one B/C PDF, found {candidates}")
    return section_a[0], section_bc[0]


def corpus_files(level: str, lang: str, year: int) -> tuple[Path, Path | None]:
    code = LEVEL_CODE[level]
    candidates = sorted((CORPUS_ROOT / str(year)).glob(f"LC562{code}LP*{lang.upper()}.pdf"))
    section_a = []
    section_bc = []
    for path in candidates:
        pages = len(PdfReader(path).pages)
        (section_a if pages <= 3 else section_bc).append(path)
    if len(section_a) != 1:
        raise ValueError(f"{level}|{lang}|{year}: expected one Section-A PDF, found {section_a}")
    if len(section_bc) > 1:
        raise ValueError(f"{level}|{lang}|{year}: ambiguous Section-B/C PDFs {section_bc}")
    return section_a[0], section_bc[0] if section_bc else None


def question_card(number: str, topic_ids: list[str], crosswalk: dict[str, list[str]]) -> dict:
    canonical = []
    for topic_id in topic_ids:
        for node_id in crosswalk[topic_id]:
            if node_id not in canonical:
                canonical.append(node_id)
    if not canonical:
        raise ValueError(f"Q{number}: no canonical curriculum node for {topic_ids}")
    card = {"n": number, "primary": canonical[0]}
    if len(canonical) > 1:
        card["secondary"] = canonical[1]
    return card


def component(fileid: str) -> str:
    match = re.search(r"LP([A-Z0-9]{3})(?:EV|IV)(?:-deferred)?\.pdf$", fileid, flags=re.I)
    if not match:
        raise ValueError(f"Unparseable DCG fileid {fileid}")
    return match.group(1)


def write_map(year: int, fileid: str, section_a: bool) -> None:
    out = HOSTED_ROOT / str(year) / f"{fileid}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    questions = []
    if section_a:
        for index in range(1, 5):
            n = str(index)
            rect = A_RECTS[n]
            questions.append(
                {
                    "n": n,
                    "label": f"A-{n}",
                    "printOrder": index,
                    "pP": 2,
                    "pY": [rect[1], rect[3]],
                    "paperRegion": [{"p": 2, "r": rect}],
                    "region": [{"p": 1}],
                    "mode": "pagejump",
                    "conf": 0.5,
                }
            )
    else:
        labels = ["B-1", "B-2", "B-3", "C-1", "C-2", "C-3", "C-4", "C-5"]
        for index, label in enumerate(labels, start=1):
            page = index + 1
            questions.append(
                {
                    "n": str(index),
                    "label": label,
                    "printOrder": index,
                    "pP": page,
                    "pY": [0.06, 1.0],
                    "paperRegion": [{"p": page, "r": [0.0, 0.0, 1.0, 1.0]}],
                    "region": [{"p": 1}],
                    "mode": "pagejump",
                    "conf": 0.5,
                }
            )
    payload = {
        "v": 1,
        "paperFileid": fileid,
        "schemeFileid": "",
        "component": component(fileid),
        "band": [1, 1],
        "copyright": "© State Examinations Commission",
        "paperOnly": 1,
        "q": questions,
    }
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    reference = read_json(REFERENCE_PATH)
    crosswalk = read_json(CROSSWALK_PATH)
    baseline = read_json(BASELINE_PATH)
    papers = read_json(TAGS_PATH)
    topics_by_card = exact_topics(reference)

    if len(REVIEWED_OMISSIONS) != 49:
        raise ValueError(f"Expected 49 reviewed omissions, found {len(REVIEWED_OMISSIONS)}")
    overlap = set(topics_by_card).intersection(REVIEWED_OMISSIONS)
    if overlap:
        raise ValueError(f"Reviewed omissions now present in the reference: {sorted(overlap)}")
    topics_by_card.update(REVIEWED_OMISSIONS)

    existing = {paper_identity(paper): paper for paper in papers}
    if len(existing) != len(papers):
        raise ValueError("Duplicate DCG paper identities before generation")

    for frozen in baseline:
        identity = paper_identity(frozen)
        live = existing.get(identity)
        if live is None:
            raise ValueError(f"Preservation failure: missing {identity}")
        actual = [question["n"] for question in live["q"]]
        if actual != frozen["questions"]:
            raise ValueError(f"Preservation failure: changed card run for {identity}")

    for year in range(2026, 2009, -1):
        for level in ("higher", "ordinary"):
            if year not in EXPECTED_YEARS[level]:
                continue
            for lang in LANGUAGES:
                a_path, bc_path = corpus_files(level, lang, year)

                if bc_path is not None:
                    identity = "|".join([level, lang, str(year), "single", bc_path.name])
                    if identity not in existing:
                        q = []
                        for number in map(str, range(1, 9)):
                            key = logical_key(level, year, "single", number)
                            q.append(question_card(number, topics_by_card[key], crosswalk))
                        paper = {
                            "subjectId": SUBJECT_ID,
                            "level": level,
                            "lang": lang,
                            "year": year,
                            "fileid": bc_path.name,
                            "paperKey": "single",
                            "q": q,
                        }
                        papers.append(paper)
                        existing[identity] = paper
                    if year == 2026:
                        write_map(year, bc_path.name, section_a=False)

                identity = "|".join([level, lang, str(year), "section-a", a_path.name])
                if identity not in existing:
                    q = []
                    for number in map(str, range(1, 5)):
                        key = logical_key(level, year, "section-a", number)
                        q.append(question_card(number, topics_by_card[key], crosswalk))
                    paper = {
                        "subjectId": SUBJECT_ID,
                        "level": level,
                        "lang": lang,
                        "year": year,
                        "fileid": a_path.name,
                        "paperKey": "section-a",
                        "q": q,
                    }
                    papers.append(paper)
                    existing[identity] = paper
                write_map(year, a_path.name, section_a=True)

    june = [paper for paper in papers if not paper["fileid"].endswith("-deferred.pdf")]
    if len(june) != 132:
        raise ValueError(f"Expected 132 DCG physical variants, found {len(june)}")
    if sum(len(paper["q"]) for paper in june) != 792:
        raise ValueError("Expected 792 DCG physical question mappings")

    # The deferred sittings, after every June paper, so a June record never
    # moves. Their topics come from the reference's deferred headings alone.
    deferred_by_card = deferred_topics(reference)
    overlap = set(deferred_by_card).intersection(DEFERRED_REVIEWED_OMISSIONS)
    if overlap:
        raise ValueError(f"Reviewed deferred omissions now present in the reference: {sorted(overlap)}")
    deferred_by_card.update(DEFERRED_REVIEWED_OMISSIONS)
    for year, level in DEFERRED_SITTINGS:
        a_path, bc_path = deferred_files(level, year)
        for path, paper_key, numbers in (
            (bc_path, "single", range(1, 9)),
            (a_path, "section-a", range(1, 5)),
        ):
            fileid = f"{path.stem}-deferred.pdf"
            identity = "|".join([level, "ev", str(year), paper_key, fileid])
            if identity not in existing:
                q = [
                    question_card(
                        str(number),
                        deferred_by_card[f"{level}|{year}|deferred|{paper_key}|{number}"],
                        crosswalk,
                    )
                    for number in numbers
                ]
                paper = {
                    "subjectId": SUBJECT_ID,
                    "level": level,
                    "lang": "ev",
                    "year": year,
                    "fileid": fileid,
                    "paperKey": paper_key,
                    "q": q,
                }
                papers.append(paper)
                existing[identity] = paper
            write_map(year, fileid, section_a=paper_key == "section-a")
    deferred = [paper for paper in papers if paper["fileid"].endswith("-deferred.pdf")]
    if len(deferred) != 2 * len(DEFERRED_SITTINGS):
        raise ValueError(f"Expected {2 * len(DEFERRED_SITTINGS)} deferred DCG variants, found {len(deferred)}")

    for paper in papers:
        expected = 4 if paper["paperKey"] == "section-a" else 8
        if len(paper["q"]) != expected:
            raise ValueError(f"{paper_identity(paper)}: expected {expected} cards")
        for question in paper["q"]:
            if paper["fileid"].endswith("-deferred.pdf"):
                key = f"{paper['level']}|{paper['year']}|deferred|{paper['paperKey']}|{question['n']}"
                known = deferred_by_card
            else:
                key = logical_key(paper["level"], paper["year"], paper["paperKey"], question["n"])
                known = topics_by_card
            if key not in known:
                raise ValueError(f"Unclassified DCG card {key}")

    TAGS_PATH.write_text(json.dumps(papers, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print("DCG: preserved 62 variants / 496 cards; emitted 132 variants / 792 cards and 70 new maps")


if __name__ == "__main__":
    main()
