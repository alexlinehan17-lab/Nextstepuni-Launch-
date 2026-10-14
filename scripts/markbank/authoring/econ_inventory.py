#!/usr/bin/env python3
"""Inventory the Economics corpus against Paper Trail, without claiming completion.

Unlike the older Mark Bank census (2021–2025 English papers only), this starts
from every indexed Economics paper, including both official language editions.
PDF presence, hashes and whole-question tags are evidence of source availability,
not evidence that every separately marked task has been authored or reviewed.

Run from any directory: python3 scripts/markbank/authoring/econ_inventory.py
"""

from __future__ import annotations

import collections
import hashlib
import json
import re
from pathlib import Path

import fitz

ROOT = Path(__file__).resolve().parents[3]
OUTPUT = Path(__file__).with_name("economics-source-inventory.json")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def indexed_papers() -> list[dict]:
    source = (ROOT / "paperTrailData.ts").read_text()
    match = re.search(r'  "economics": (\[[\s\S]*?\n  \]),\n  "engineering":', source)
    if not match:
        raise ValueError("Economics Paper Trail index was not found")
    entries = json.loads(re.sub(r",\s*]$", "]", match.group(1)))
    return [
        {"year": entry["year"], "level": entry["level"], "lang": entry["lang"],
         "fileid": paper["doc"]["f"], "label": paper["label"],
         "schemeFileid": paper.get("scheme", {}).get("f")}
        for entry in entries for paper in entry["papers"]
    ]


def shipped_cards() -> list[dict]:
    result = []
    for level in ("higher", "ordinary"):
        text = (ROOT / "components/MarkBank/cards/economics" / f"{level}.ts").read_text()
        for chunk in re.split(r"\.\.\.base,\s*kind:", text)[1:]:
            def field(name: str) -> str:
                match = re.search(rf'\b{name}: ("(?:[^"\\]|\\.)*")', chunk)
                if not match:
                    raise ValueError(f"Missing {name} in shipped Economics card")
                return json.loads(match.group(1))
            def json_field(name, fallback):
                match = re.search(rf'\b{name}: ', chunk)
                return json.JSONDecoder().raw_decode(chunk[match.end():])[0] if match else fallback
            sources = [json_field('sourceMaterial', None),
                       *json_field('additionalSourceMaterials', [])]
            result.append({"id": field("id"), "questionRef": field("questionRef"),
                           "topicId": field("topicId"),
                           "paperFileid": field("paperFileid") + ".pdf",
                           "year": int(re.search(r"\byear: (\d{4})", chunk).group(1)),
                           "level": level,
                           "sources": [
                               {'fileid': source.get('sourceFileid', field('paperFileid')).removesuffix('.pdf') + '.pdf',
                                'pages': source['pages']}
                               for source in sources if source]})
    ids = [card["id"] for card in result]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate shipped Economics card IDs")
    return result


def pdf_record(folder: str, year: int, fileid: str) -> dict:
    path = ROOT / "paper-trail-corpus" / folder / str(year) / fileid
    if not path.is_file():
        raise FileNotFoundError(path)
    with fitz.open(path) as document:
        return {"path": str(path.relative_to(ROOT)), "sha256": digest(path),
                "pages": len(document),
                "coverText": " ".join(document[0].get_text().split())}


def build_inventory() -> dict:
    from econ_review import reviewed_papers, paper_key
    _, reviews = reviewed_papers()
    cards = shipped_cards()
    papers = indexed_papers()
    tags = json.loads((ROOT / "scripts/paper-trail/topic-tags/tags/economics.json").read_text())
    def key(item: dict) -> tuple:
        return tuple(item[k] for k in ("year", "level", "lang", "fileid"))
    tag_index = {key(paper): paper for paper in tags}
    if len(tag_index) != len(tags) or set(map(key, papers)) != set(tag_index):
        raise ValueError("Paper Trail and Economics topic-tag paper identities differ")
    records = []
    assigned = []
    for paper in sorted(papers, key=key):
        matching = [card for card in cards
                    if (card["year"], card["level"], card["paperFileid"]) ==
                    (paper["year"], paper["level"], paper["fileid"])]
        assigned.extend(card["id"] for card in matching)
        review = reviews.get(paper_key(paper))
        equivalent = []
        if review and review.get('equivalentTo'):
            expected_ids = {t['cardId'] for q in review['questions'] for t in q['tasks']}
            equivalent = [card for card in cards if card['id'] in expected_ids
                          and card['year'] == paper['year'] and card['level'] == paper['level']
                          and any(source['fileid'] == paper['fileid'] for source in card['sources'])]
        associated = matching + equivalent
        if not paper["schemeFileid"]:
            raise ValueError(f"Missing indexed scheme for {key(paper)}")
        record = {k: paper[k] for k in ("year", "level", "lang", "fileid", "label")}
        record.update({
            "paper": pdf_record("exampapers", paper["year"], paper["fileid"]),
            "scheme": pdf_record("markingschemes", paper["year"], paper["schemeFileid"]),
            "atlasTopLevelQuestions": [q["n"] for q in tag_index[key(paper)]["q"]],
            "primaryMarkBankCardIds": [card["id"] for card in matching],
            "equivalentEditionCardIds": [card["id"] for card in equivalent],
            "markBankCardIds": [card["id"] for card in associated],
            "taskBoundaryReview": "pending",
            "selectionRouteReview": "pending",
            "topicAndSourceReview": "pending",
        })
        if review:
            by_id = {card['id']: card for card in associated}
            for question in review['questions']:
                for task in question['tasks']:
                    card = by_id.get(task['cardId'])
                    if (not card or card['topicId'] not in question['canonicalNodeIds'] or
                            ('topicId' in task and card['topicId'] != task['topicId']) or
                            not any(source['fileid'] == paper['fileid'] and
                                    source['pages'] == question['paperPages']
                                    for source in card['sources'])):
                        raise ValueError(f"Reviewed task lacks its shipped source/topic: {paper_key(paper)} {task['cardId']}")
            record.update({
                "taskBoundaryReview": "reviewed",
                "selectionRouteReview": "reviewed",
                "topicAndSourceReview": "reviewed",
                "reviewedTaskRoutes": sum(len(q["tasks"]) for q in
                                          reviews[paper_key(paper)]["questions"]),
            })
        records.append(record)
    if collections.Counter(assigned) != collections.Counter(card["id"] for card in cards):
        raise ValueError("Every shipped card must resolve to exactly one indexed paper")
    return {
        "subjectId": "economics", "complete": False,
        "scope": "Every question and finite answer route in the indexed Paper Trail Economics corpus",
        "evidenceLimit": "Source availability and card presence only. Pending reviews are not coverage.",
        "summary": {
            "paperVariants": len(records),
            "years": sorted({paper["year"] for paper in records}),
            "logicalPapers": len({(p["year"], p["level"]) for p in records}),
            "atlasTopLevelQuestionVariants": sum(len(p["atlasTopLevelQuestions"]) for p in records),
            "shippedMarkBankCards": len(cards),
            "paperVariantsWithoutMarkBankCards": sum(not p["markBankCardIds"] for p in records),
            "paperVariantsWithoutPrimaryMarkBankCards": sum(not p["primaryMarkBankCardIds"] for p in records),
            "paperVariantsWithValidatedVisualReview": len(reviews),
        },
        "papers": records,
    }


if __name__ == "__main__":
    inventory = build_inventory()
    OUTPUT.write_text(json.dumps(inventory, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(inventory["summary"], indent=2))
    print(f"Wrote {OUTPUT.relative_to(ROOT)}; completion remains unverified.")
