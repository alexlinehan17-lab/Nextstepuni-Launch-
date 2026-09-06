#!/usr/bin/env python3
"""Restore exact SEC Mathematics question cards required by the StudyClix audit.

The operation is additive.  Existing cards keep every original field; where a
previous final card ran into a newly-restored following question, its original
``region`` is retained and a narrower ``schemeRegion`` correction is added.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path

import fitz


ROOT = Path(__file__).resolve().parents[2]
ANSWERS = ROOT / "scripts" / "paper-trail" / "answers"
CORPUS = ROOT / "paper-trail-corpus"
ANCHOR_MAP = ROOT / "scripts" / "paper-trail" / "anchor-map.py"


def load_mapper():
    spec = importlib.util.spec_from_file_location("paper_trail_anchor_map", ANCHOR_MAP)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load {ANCHOR_MAP}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


MAPPER = load_mapper()


# year, paper file, scheme file, band strategy
GENERATED = (
    (2010, "LC003BLP200EV.pdf", "LC003BLP000EV.pdf", ("divider", 2, "200")),
    (2011, "LC003GLP000EV.pdf", "LC003GLP000EV.pdf", ("divider", 1, "000")),
    (2012, "LC003ALP130EV.pdf", "LC003ALP030EV.pdf", ("divider", 1, "130")),
    (2012, "LC003GLP130EV.pdf", "LC003GLP030EV.pdf", ("divider", 1, "130")),
    (2012, "LC003GLP230EV.pdf", "LC003GLP030EV.pdf", ("divider", 2, "230")),
    (2012, "LC003BLP200EV.pdf", "LC003BLP000EV.pdf", ("divider", 2, "200")),
    (2013, "LC003ALP130EV.pdf", "LC003ALP030EV.pdf", ("divider", 1, "130")),
    (2013, "LC003GLP130EV.pdf", "LC003GLP030EV.pdf", ("divider", 1, "130")),
    (2013, "LC003BLP130IV.pdf", "LC003BLP030IV.pdf", ("divider", 1, "130")),
    (2013, "LC003BLP200EV.pdf", "LC003BLP000EV.pdf", ("divider", 2, "200")),
    (2013, "LC003BLP230EV.pdf", "LC003BLP030EV.pdf", ("divider", 2, "230")),
    (2013, "LC003BLP230IV.pdf", "LC003BLP030IV.pdf", ("divider", 2, "230")),
    (2014, "LC003ALP130EV.pdf", "LC003ALP000EV.pdf", ("divider", 1, "130")),
    (2014, "LC003ALP230EV.pdf", "LC003ALP000EV.pdf", ("divider", 2, "230")),
    (2014, "LC003GLP130EV.pdf", "LC003GLP000EV.pdf", ("divider", 1, "130")),
    (2014, "LC003GLP230EV.pdf", "LC003GLP000EV.pdf", ("divider", 2, "230")),
    (2014, "LC003BLP130EV.pdf", "LC003BLP000EV.pdf", ("divider", 1, "130")),
    (2014, "LC003BLP230EV.pdf", "LC003BLP000EV.pdf", ("divider", 2, "230")),
    (2016, "LC003ALP200EV.pdf", "LC003ALP000EV.pdf", ("divider", 2, "200")),
    (2017, "LC003ALP200EV.pdf", "LC003ALP000EV.pdf", ("divider", 2, "200")),
    (2018, "LC003ALP200EV.pdf", "LC003ALP000EV.pdf", ("divider", 2, "200")),
    (2019, "LC003BLP000EV.pdf", "LC003BLP000EV.pdf", ("whole", "000")),
    (2020, "LC003BLP000EV.pdf", "LC003BLP000EV.pdf", ("whole", "000")),
    (2021, "LC003BLP000EV.pdf", "LC003BLP000EV.pdf", ("whole", "000")),
    (2021, "LC003GLP200EV.pdf", "LC003GLP000EV.pdf", ("divider", 2, "200")),
    (2023, "LC003BLP000IV.pdf", "LC003BLP000IV.pdf", ("whole", "000")),
    (2023, "LC003ALP100IV.pdf", "LC003ALP000IV.pdf", ("divider", 1, "100")),
    (2023, "LC003ALP200IV.pdf", "LC003ALP000IV.pdf", ("divider", 2, "200")),
    (2023, "LC003GLP100EV.pdf", "LC003GLP000EV.pdf", ("divider", 1, "100")),
    (2023, "LC003GLP100IV.pdf", "LC003GLP000IV.pdf", ("divider", 1, "100")),
    (2023, "LC003GLP200EV.pdf", "LC003GLP000EV.pdf", ("divider", 2, "200")),
    (2023, "LC003GLP200IV.pdf", "LC003GLP000IV.pdf", ("divider", 2, "200")),
    (2025, "LC003GLP200IV.pdf", "LC003GLP000IV.pdf", ("divider", 2, "200")),
    (2026, "LC003ALP100EV.pdf", "LC003ALP000EV.pdf", ("divider", 1, "100")),
    (2026, "LC003ALP200EV.pdf", "LC003ALP000EV.pdf", ("divider", 2, "200")),
    (2026, "LC003GLP200EV.pdf", "LC003GLP000EV.pdf", ("divider", 2, "200")),
    (2026, "LC003GLP200IV.pdf", "LC003GLP000IV.pdf", ("divider", 2, "200")),
)


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def merge_preserving_cards(existing: dict, generated: dict) -> dict:
    """Keep every old card value and add only missing/corrective information."""
    for key in ("paperFileid", "schemeFileid"):
        if existing.get(key) != generated.get(key):
            raise RuntimeError(f"Sidecar identity drift for {existing.get('paperFileid')}: {key}")
    if existing.get("component") != generated.get("component") and not (
        existing.get("component") == ""
        and generated.get("component") in {"1", "000"}
    ):
        raise RuntimeError(
            f"Sidecar identity drift for {existing.get('paperFileid')}: component"
        )

    old_by_n = {card["n"]: card for card in existing["q"]}
    for fresh in generated["q"]:
        old = old_by_n.get(fresh["n"])
        if old is None:
            existing["q"].append(fresh)
            old_by_n[fresh["n"]] = fresh
            continue
        for key in ("pP", "pY"):
            if old.get(key) != fresh.get(key):
                raise RuntimeError(
                    f"Paper anchor drift for {existing['paperFileid']} Q{fresh['n']}: {key}"
                )
        if old.get("region") != fresh.get("region"):
            prior = old.get("schemeRegion")
            if prior is not None and prior != fresh["region"]:
                raise RuntimeError(
                    f"Existing scheme correction drift for {existing['paperFileid']} Q{fresh['n']}"
                )
            old["schemeRegion"] = fresh["region"]
    return existing


def generated_sidecar(year: int, paper_file: str, scheme_file: str, band: tuple) -> dict:
    paper = CORPUS / "exampapers" / str(year) / paper_file
    scheme = CORPUS / "markingschemes" / str(year) / scheme_file
    sidecar, stats = MAPPER.map_paper(paper, scheme, band)
    if sidecar is None or stats.get("conf") != 1.0 or stats.get("pagejump") != 0:
        raise RuntimeError(f"Unsafe map for {year} {paper_file}: {stats}")
    return sidecar


def install_generated(year: int, paper_file: str, scheme_file: str, band: tuple) -> dict:
    fresh = generated_sidecar(year, paper_file, scheme_file, band)
    destination = ANSWERS / str(year) / f"{paper_file}.json"
    if destination.exists():
        return merge_preserving_cards(read_json(destination), fresh)
    return fresh


def exact_hit(doc: fitz.Document, phrase: str, page_number: int):
    page = doc[page_number - 1]
    hits = page.search_for(phrase)
    if len(hits) != 1:
        raise RuntimeError(f"Expected one {phrase!r} hit on PDF page {page_number}, got {len(hits)}")
    return round(hits[0].y0 / page.rect.height, 4)


def add_2010_higher_project_choices() -> dict:
    destination = ANSWERS / "2010" / "LC003ALP230EV.pdf.json"
    sidecar = read_json(destination)
    paper = fitz.open(CORPUS / "exampapers" / "2010" / "LC003ALP230EV.pdf")
    scheme = fitz.open(CORPUS / "markingschemes" / "2010" / "LC003ALP030EV.pdf")

    paper_9a = exact_hit(paper, "Question 9A", 14)
    paper_9b = exact_hit(paper, "Question 9B", 16)
    scheme_9a = exact_hit(scheme, "Question 9A", 55)
    scheme_9b = exact_hit(scheme, "Question 9B", 57)

    # Keep the original Q8 region intact for stable stored cards, while the
    # viewer uses the corrected boundary immediately before Question 9A.
    q8 = next(card for card in sidecar["q"] if card["n"] == "8")
    q8_correction = [
        q8["region"][0],
        {"p": 54, "r": [0.0, 0.0, 1.0, 1.0]},
        {"p": 55, "r": [0.0, 0.0, 1.0, scheme_9a]},
    ]
    if q8.get("schemeRegion") not in (None, q8_correction):
        raise RuntimeError("2010 Higher Project Maths Q8 already has a different correction")
    q8["schemeRegion"] = q8_correction

    additions = (
        {
            "conf": 1.0,
            "label": "Question 9A · Probability and Statistics",
            "mode": "crop",
            # Card ids remain numeric; the printed choice identity lives in
            # the student-facing label and exact crosswalk.
            "n": "9",
            "pP": 14,
            "pY": [paper_9a, 1.0],
            "printOrder": 9,
            "region": [
                {"p": 55, "r": [0.0, max(0.0, round(scheme_9a - 0.012, 4)), 1.0, 1.0]},
                {"p": 56, "r": [0.0, 0.0, 1.0, 1.0]},
                {"p": 57, "r": [0.0, 0.0, 1.0, scheme_9b]},
            ],
        },
        {
            "conf": 1.0,
            "label": "Question 9B · Geometry and Trigonometry",
            "mode": "crop",
            "n": "10",
            "pP": 16,
            "pY": [paper_9b, 1.0],
            "printOrder": 10,
            "region": [
                {"p": 57, "r": [0.0, max(0.0, round(scheme_9b - 0.012, 4)), 1.0, 1.0]},
                {"p": 58, "r": [0.0, 0.0, 1.0, 1.0]},
                {"p": 59, "r": [0.0, 0.0, 1.0, 1.0]},
            ],
        },
    )
    by_n = {card["n"]: card for card in sidecar["q"]}
    for addition in additions:
        current = by_n.get(addition["n"])
        legacy_n = "9A" if addition["n"] == "9" else "9B"
        if current is None and legacy_n in by_n:
            # Repair the unreleased additive card ids emitted by the first
            # audit pass; no pre-existing Mark Bank identity used these ids.
            current = by_n.pop(legacy_n)
            current["n"] = addition["n"]
            by_n[addition["n"]] = current
        if current is None:
            sidecar["q"].append(addition)
        elif current != addition:
            raise RuntimeError(f"2010 Higher Project Maths Q{addition['n']} drift")
    sidecar["q"].sort(key=lambda card: int(card["n"]))
    for index, card in enumerate(sidecar["q"]):
        card.setdefault("printOrder", index + 1)
    return sidecar


def expected_outputs() -> dict[Path, dict]:
    outputs = {}
    for args in GENERATED:
        year, paper_file, scheme_file, band = args
        outputs[ANSWERS / str(year) / f"{paper_file}.json"] = install_generated(*args)
    outputs[ANSWERS / "2010" / "LC003ALP230EV.pdf.json"] = add_2010_higher_project_choices()
    return outputs


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    outputs = expected_outputs()
    changed = []
    for destination, expected in outputs.items():
        rendered = json.dumps(expected, indent=2, ensure_ascii=False) + "\n"
        current = destination.read_text(encoding="utf-8") if destination.exists() else None
        if current == rendered:
            continue
        if args.check:
            raise RuntimeError(f"Generated Mathematics sidecar is stale: {destination}")
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(rendered, encoding="utf-8")
        changed.append(destination.relative_to(ROOT))

    mode = "verified" if args.check else "updated"
    print(f"{mode} {len(outputs)} Mathematics sidecars; changed {len(changed)}")
    for path in changed:
        print(f"  {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
