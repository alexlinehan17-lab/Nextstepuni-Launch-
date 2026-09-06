#!/usr/bin/env python3
"""Repair the audited 2019-2022 Japanese written-paper answer maps.

The existing language mapper exposed the reading-comprehension cards but
omitted whole Kanji, grammar, culture and written-production sections.  This
builder is deliberately additive: stable existing question IDs and all their
crop data are retained byte-for-byte at the object level (apart from the new
``printOrder`` field), while newly recovered sections receive IDs after the
existing range.  ``printOrder`` restores the order in which those stable IDs
appear on the physical paper.

Run from the repository root:
    python3 scripts/paper-trail/japanese_written_legacy.py

Set PT_JAPANESE_LEGACY_OUT to stage the generated sidecars outside answers/.
"""

from __future__ import annotations

import copy
import hashlib
import json
import os
from pathlib import Path

import fitz


HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
CORPUS = REPO / "paper-trail-corpus"
SOURCE_ROOT = HERE / "answers"
OUT_ROOT = Path(os.environ.get("PT_JAPANESE_LEGACY_OUT", SOURCE_ROOT))


def R(page: int, start: float, end: float) -> dict:
    return {"p": page, "r": [0.0, start, 1.0, end]}


def C(
    number: int,
    label: str,
    paper_page: int,
    paper_y: float,
    *regions: dict,
    end: tuple[int, float],
) -> dict:
    return {
        "conf": 1.0,
        "label": label,
        "mode": "crop",
        "n": str(number),
        "pP": paper_page,
        "pY": [paper_y, 1.0],
        "region": list(regions),
        "endP": end[0],
        "endY": end[1],
    }


# SHA-256 of each pre-repair question array after removing printOrder.  These
# sentinels make the additive guarantee executable: the builder refuses to
# rewrite a paper if any pre-existing card has drifted.
BASE_HASHES = {
    (2019, "A"): "2ec3c328254b27142b54c4acd2a875a95e22ceb5fe9db5fb001dc5d2c79d30c2",
    (2019, "G"): "74ac002a6a2b3e09733916efda00b7018f603df43033c5dbeb066d5b15b56199",
    (2020, "A"): "de7a019cae918623fc7a054b10f5e09f526d23e774d7337e6a70a777f850fdf4",
    (2021, "A"): "a7c27fb2416715acb1636f102e71a74164d4b0f370761fba332e51e0dd9995f7",
    (2021, "G"): "f89565985962b97a40233e2ac21351d09e5dcaea9d64a287d412caad64a88925",
    (2022, "A"): "4445ffc44a1593c0369a57c0121b0707708d6684c62e310c2a355117371c5f04",
    (2022, "G"): "f5ccc81d250d852c318a50c73e256794ab9143242e72860e1f015e3ebd893398",
}


SPECS: dict[tuple[int, str], dict] = {
    (2019, "A"): {
        "base": 26,
        "order": [*range(1, 29)],
        "cards": [
            C(27, "Q4 · Written production (choose A or B)", 14, .0351,
              R(12, .0348, .90), R(13, .0348, .84), end=(15, .93)),
            C(28, "Q5 · Email to a visiting Japanese friend", 16, .0351,
              R(14, .0512, .90), R(15, .0348, .82), end=(19, .93)),
        ],
    },
    (2019, "G"): {
        "base": 20,
        "order": [*range(1, 14), 21, *range(14, 21), 22, 23],
        "cards": [
            C(21, "Q2 D · Culture and society", 7, .0331,
              R(6, .0884, .2101), end=(7, .93)),
            C(22, "Q4 · Birthday cloze", 11, .0341,
              R(8, .1029, .4750), end=(11, .93)),
            C(23, "Q5 · Japanese study", 12, .0625,
              R(8, .4986, .91), R(9, .0884, .80), end=(12, .93)),
        ],
    },
    (2020, "A"): {
        "base": 20,
        "order": [*range(1, 12), 21, 22, *range(12, 21), 23, 24, 25, 26],
        "cards": [
            C(21, "Q2 B · Kanji", 8, .0366,
              R(9, .4742, .7724), end=(8, .93)),
            C(22, "Q2 C · Grammar", 9, .0366,
              R(9, .7724, .91), R(10, .0734, .1880), end=(9, .93)),
            C(23, "Q3 C · Kanji", 12, .0365,
              R(11, .0727, .3357), end=(12, .4279)),
            C(24, "Q3 D · Grammar", 12, .4279,
              R(11, .3357, .64), end=(12, .93)),
            C(25, "Q4 · Written production (choose A or B)", 14, .0542,
              R(12, .0727, .64), R(13, .0727, .88), end=(15, .93)),
            C(26, "Q5 · Speech about Ireland", 16, .0351,
              R(14, .0727, .84), R(15, .0727, .83), end=(19, .93)),
        ],
    },
    (2021, "A"): {
        "base": 23,
        "order": [*range(1, 15), 24, 25, *range(15, 24), 26, 27, 28, 29],
        "cards": [
            C(24, "Q2 B · Kanji", 8, .0366,
              R(9, .5699, .91), R(10, .0843, .3452), end=(8, .93)),
            C(25, "Q2 C · Grammar", 9, .0365,
              R(10, .3452, .88), end=(9, .93)),
            C(26, "Q3 C · Kanji", 12, .0365,
              R(12, .0843, .2858), end=(12, .4962)),
            C(27, "Q3 D · Grammar", 12, .4962,
              R(12, .2858, .59), end=(12, .93)),
            C(28, "Q4 · Written production (choose A, B or C)", 14, .0365,
              R(13, .0843, .90), R(15, .0843, .90), end=(15, .93)),
            C(29, "Q5 · Blog about your locality", 16, .0351,
              R(14, .0843, .90), R(15, .0843, .90), end=(19, .93)),
        ],
    },
    (2021, "G"): {
        "base": 21,
        "order": [*range(1, 15), 22, *range(15, 22), 23, 24],
        "cards": [
            C(22, "Q2 D · Culture and society", 7, .2438,
              R(7, .5428, .6941), end=(7, .93)),
            C(23, "Q4 · Personal introduction cloze", 11, .0742,
              R(9, .2904, .69), end=(11, .93)),
            C(24, "Q5 · Summer holidays", 12, .0687,
              R(10, .0669, .90), end=(12, .93)),
        ],
    },
    (2022, "A"): {
        "base": 22,
        "order": [*range(1, 14), 23, 24, *range(14, 23), 25, 26, 27, 28],
        "cards": [
            C(23, "Q2 B · Kanji", 8, .0366,
              R(9, .5204, .90), end=(8, .93)),
            C(24, "Q2 C · Grammar", 9, .0365,
              R(10, .0884, .4494), end=(9, .93)),
            C(25, "Q3 C · Kanji", 12, .0365,
              R(11, .4215, .6250), end=(12, .4260)),
            C(26, "Q3 D · Grammar", 12, .4260,
              R(11, .6250, .90), end=(12, .93)),
            C(27, "Q4 · Written production (choose A, B or C)", 14, .0365,
              R(12, .0884, .92), R(14, .0884, .90), end=(15, .93)),
            C(28, "Q5 · Blog about your locality", 16, .0351,
              R(13, .0884, .92), R(14, .0884, .90), end=(19, .93)),
        ],
    },
    (2022, "G"): {
        "base": 21,
        "order": [*range(1, 15), 22, *range(15, 22), 23, 24],
        "cards": [
            C(22, "Q2 D · Culture and society", 7, .0702,
              R(7, .3889, .4865), end=(7, .93)),
            C(23, "Q4 · Summer job cloze", 12, .0774,
              R(9, .0815, .54), end=(12, .93)),
            C(24, "Q5 · Weekend", 13, .0685,
              R(9, .5573, .92), R(10, .0777, .73), end=(13, .93)),
        ],
    },
}


def without_print_order(question: dict) -> dict:
    return {key: value for key, value in question.items() if key != "printOrder"}


def digest(questions: list[dict]) -> str:
    payload = json.dumps(
        [without_print_order(question) for question in questions],
        ensure_ascii=False,
        separators=(",", ":"),
    ).encode()
    return hashlib.sha256(payload).hexdigest()


def repair(year: int, level_code: str, spec: dict) -> Path:
    paper_fileid = f"LC058{level_code}LP000BV.pdf"
    source = SOURCE_ROOT / str(year) / f"{paper_fileid}.json"
    sidecar = json.loads(source.read_text())
    base_count = spec["base"]
    base = [copy.deepcopy(q) for q in sidecar["q"] if int(q["n"]) <= base_count]
    if [int(q["n"]) for q in base] != list(range(1, base_count + 1)):
        raise ValueError(f"{year} {level_code}: existing stable ID range is incomplete")
    if digest(base) != BASE_HASHES[(year, level_code)]:
        raise ValueError(f"{year} {level_code}: a pre-existing question changed; refusing additive repair")

    additions = copy.deepcopy(spec["cards"])
    expected_tail = {int(q["n"]): without_print_order(q) for q in additions}
    current_tail = [q for q in sidecar["q"] if int(q["n"]) > base_count]
    if current_tail:
        actual_tail = {int(q["n"]): without_print_order(q) for q in current_tail}
        if actual_tail != expected_tail:
            raise ValueError(f"{year} {level_code}: unexpected post-baseline cards; refusing to overwrite")

    questions = base + additions
    stable_ids = [int(q["n"]) for q in questions]
    if stable_ids != list(range(1, len(questions) + 1)):
        raise ValueError(f"{year} {level_code}: stable IDs are not contiguous")

    order = spec["order"]
    if sorted(order) != stable_ids:
        raise ValueError(f"{year} {level_code}: print-order permutation is invalid")
    rank = {number: index for index, number in enumerate(order, start=1)}
    for question in questions:
        question["printOrder"] = rank[int(question["n"])]

    paper_path = CORPUS / "exampapers" / str(year) / sidecar["paperFileid"]
    scheme_path = CORPUS / "markingschemes" / str(year) / sidecar["schemeFileid"]
    with fitz.open(paper_path) as paper, fitz.open(scheme_path) as scheme:
        physically_ordered = sorted(questions, key=lambda q: q["printOrder"])
        previous = (0, 0.0)
        for question in physically_ordered:
            anchor = (question["pP"], question["pY"][0])
            if anchor <= previous:
                raise ValueError(f"{year} {level_code}: non-monotonic anchor at {question['label']}")
            previous = anchor
            if not 1 <= question["pP"] <= len(paper):
                raise ValueError(f"{year} {level_code}: paper page outside source")
            if question.get("endP", question["pP"]) > len(paper):
                raise ValueError(f"{year} {level_code}: paper crop end outside source")
            for region in question["region"]:
                if not 1 <= region["p"] <= len(scheme):
                    raise ValueError(f"{year} {level_code}: scheme page outside source")
                if not 0 <= region["r"][1] < region["r"][3] <= 1:
                    raise ValueError(f"{year} {level_code}: invalid scheme crop")

    sidecar["q"] = questions
    out = OUT_ROOT / str(year) / f"{paper_fileid}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(sidecar, ensure_ascii=False, indent=2) + "\n")
    return out


def main() -> None:
    total_added = 0
    for (year, level_code), spec in sorted(SPECS.items()):
        out = repair(year, level_code, spec)
        added = len(spec["cards"])
        total_added += added
        shown = out.relative_to(REPO) if out.is_relative_to(REPO) else out
        print(f"wrote {shown} (+{added} cards)")
    print(f"Japanese 2019-2022 written additions: {total_added} cards")


if __name__ == "__main__":
    main()
