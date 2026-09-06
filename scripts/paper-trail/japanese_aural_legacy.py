#!/usr/bin/env python3
"""Repair restart-collided Japanese aural maps from 2013-2016.

Five historic year/level layouts number questions from 1 again in each of four
Parts.  The generic aural mapper joined the first run in Part A to the matching
tail of Part D, leaving Parts B/C and the start of D without selectable cards.
This additive builder preserves every shipped ID and crop, appends the 82
missing EV/IV cards, and supplies an explicit physical display order.

Run from the repository root:
    python3 scripts/paper-trail/japanese_aural_legacy.py

Set PT_JAPANESE_AURAL_OUT to stage generated sidecars outside answers/.
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
OUT_ROOT = Path(os.environ.get("PT_JAPANESE_AURAL_OUT", SOURCE_ROOT))

CONVERSATION = "japanese-6-0"
INTERVIEW = "japanese-6-1"
RADIO = "japanese-6-2"


def R(page: int, start: float, end: float) -> dict:
    return {"p": page, "r": [0.0, start, 1.0, end]}


def P(
    part: str,
    number: int,
    page: int,
    start: float,
    end: float,
    topic: str,
) -> dict:
    return {
        "label": f"PART {part} · {number}",
        "paper_page": page,
        "paper_start": start,
        "paper_end": end,
        "topic": topic,
    }


BASE_COUNTS = {
    (2013, "G"): 9,
    (2014, "G"): 6,
    (2015, "A"): 7,
    (2015, "G"): 6,
    (2016, "G"): 6,
}


# Python compact-JSON sentinels for the pre-repair q arrays.  Additive labels
# and printOrder are excluded on later idempotent runs; every shipped crop and
# stable ID remains inside the protected payload.
BASE_HASHES = {
    (2013, "G", "E"): "79d6f3e5cf756da5cecfb7cbc0064953bdd11f02ccc11e5b1c97ced58146edc1",
    (2013, "G", "I"): "b4b4cad9830a1ae6dc29b9cc220988c779471db4e0e1ae9c5dd62a5922d34493",
    (2014, "G", "E"): "db6437f4f6e8c06115004cc013c31fc704d054630fb99e43b52ca411efa02398",
    (2014, "G", "I"): "051b964aadffbafce14a62a52e005fdbb85b06c7ef7f80fea03a9f6979d06e50",
    (2015, "A", "E"): "66c7addc852baabd5b653e3d553842bbaafd5ef98c810aeb9a499da5f5b12629",
    (2015, "A", "I"): "342c1d6a8eb099cb934fbaa2b9f861f622e035af97dbeaffc5d2cbc9a04dd289",
    (2015, "G", "E"): "6792d5c2749cf4e0bd054038526e9fe552ce47150b180ad9bd66daae4ff7075f",
    (2015, "G", "I"): "5c84ede4bfd58435e09840fa0d7ea4f1941202900e59809ede7439bbca33f851",
    (2016, "G", "E"): "aa785718b93e7c03cc37b67d4cefc29f51935a0ac149609ac078c03127941ac9",
    (2016, "G", "I"): "141f6d3ab202b1d473599a7e4601312e188f3ee7270f603d92ab3d13abeadc7d",
}


BASE_LABELS = {
    (2013, "G"): [
        "PART A · 1", "PART A · 2", "PART A · 3", "PART A · 4",
        "PART D · 5", "PART D · 6", "PART D · 7", "PART D · 8", "PART D · 9",
    ],
    (2014, "G"): [
        "PART A · 1", "PART A · 2", "PART A · 3",
        "PART D · 4", "PART D · 5", "PART D · 6",
    ],
    (2015, "A"): [
        "PART A · 1", "PART A · 2", "PART A · 3",
        "PART D · 4", "PART D · 5", "PART D · 6", "PART D · 7",
    ],
    (2015, "G"): [
        "PART A · 1", "PART A · 2", "PART A · 3",
        "PART D · 4", "PART D · 5", "PART D · 6",
    ],
    (2016, "G"): [
        "PART A · 1", "PART A · 2", "PART A · 3",
        "PART D · 4", "PART D · 5", "PART D · 6",
    ],
}


PAPER_ADDITIONS = {
    (2013, "G"): [
        P("B", 1, 3, .2012, .5559, RADIO),
        P("B", 2, 3, .5559, 1.0, RADIO),
        P("C", 1, 4, .1811, .4924, CONVERSATION),
        P("C", 2, 4, .4924, .7710, CONVERSATION),
        P("C", 3, 4, .7710, .94, CONVERSATION),
        P("D", 1, 5, .2274, .2916, INTERVIEW),
        P("D", 2, 5, .2916, .3564, INTERVIEW),
        P("D", 3, 5, .3564, .4377, INTERVIEW),
        P("D", 4, 5, .4377, .5344, INTERVIEW),
    ],
    (2014, "G"): [
        P("B", 1, 3, .1972, .5438, RADIO),
        P("B", 2, 3, .5438, .7808, RADIO),
        P("B", 3, 3, .7808, .94, RADIO),
        P("C", 1, 4, .1846, .7342, CONVERSATION),
        P("C", 2, 4, .7342, .94, CONVERSATION),
        P("D", 1, 5, .2002, .3258, CONVERSATION),
        P("D", 2, 5, .3258, .4514, CONVERSATION),
        P("D", 3, 5, .4514, .5770, CONVERSATION),
    ],
    (2015, "A"): [
        P("B", 1, 3, .1569, .5597, RADIO),
        P("B", 2, 3, .5597, .7892, RADIO),
        P("B", 3, 3, .7892, .94, RADIO),
        P("C", 1, 4, .1432, .6048, CONVERSATION),
        P("C", 2, 4, .6048, .94, CONVERSATION),
        P("D", 1, 5, .1551, .2862, CONVERSATION),
        P("D", 2, 5, .2862, .4173, CONVERSATION),
        P("D", 3, 5, .4173, .5157, CONVERSATION),
    ],
    (2015, "G"): [
        P("B", 1, 3, .1922, .5342, RADIO),
        P("B", 2, 3, .5342, .7885, RADIO),
        P("B", 3, 3, .7885, .94, RADIO),
        P("C", 1, 4, .1817, .5914, CONVERSATION),
        P("C", 2, 4, .5914, .94, CONVERSATION),
        P("D", 1, 5, .1939, .3250, CONVERSATION),
        P("D", 2, 5, .3250, .4397, CONVERSATION),
        P("D", 3, 5, .4397, .5542, CONVERSATION),
    ],
    (2016, "G"): [
        P("B", 1, 3, .1972, .6759, CONVERSATION),
        P("B", 2, 3, .6759, .94, CONVERSATION),
        P("C", 1, 4, .2107, .5348, RADIO),
        P("C", 2, 4, .5348, .6918, RADIO),
        P("C", 3, 4, .6918, .94, RADIO),
        P("D", 1, 5, .2034, .3291, CONVERSATION),
        P("D", 2, 5, .3291, .4077, CONVERSATION),
        P("D", 3, 5, .4077, .5490, CONVERSATION),
    ],
}


SCHEME_REGIONS = {
    (2013, "G", "E"): [
        [R(3, .4955, .6395)], [R(3, .6275, .93)],
        [R(4, .1051, .2484)], [R(4, .2364, .3962)], [R(4, .3842, .5113)],
        [R(4, .5323, .6212)], [R(4, .6092, .6980)],
        [R(4, .6860, .7751)], [R(4, .7631, .8410)],
    ],
    (2013, "G", "I"): [
        [R(3, .4955, .6726)], [R(3, .6606, .93)],
        [R(4, .1051, .2648)], [R(4, .2528, .4126)], [R(4, .4006, .5441)],
        [R(4, .5651, .6595)], [R(4, .6475, .7417)],
        [R(4, .7297, .8243)], [R(4, .8123, .93)],
    ],
    (2014, "G", "E"): [
        [R(3, .4593, .6528)], [R(3, .6408, .8013)], [R(3, .7893, .93)],
        [R(4, .0995, .3084)], [R(4, .2964, .4729)],
        [R(4, .4935, .5546)], [R(4, .5426, .6038)], [R(4, .5918, .6366)],
    ],
    (2014, "G", "I"): [
        [R(3, .4374, .6309)], [R(3, .6189, .7464)], [R(3, .7344, .93)],
        [R(4, .0804, .2894)], [R(4, .2774, .4536)],
        [R(4, .4744, .5353)], [R(4, .5233, .5847)], [R(4, .5727, .6174)],
    ],
    (2015, "A", "E"): [
        [R(3, .5368, .7518)], [R(3, .7398, .93)],
        [R(4, .0443, .2522)], [R(4, .2566, .5408)], [R(4, .5288, .7522)],
        [R(4, .7565, .8328)], [R(4, .8208, .93)],
        [R(5, .0341, .1117)],
    ],
    (2015, "A", "I"): [
        [R(3, .5187, .7189)], [R(3, .7069, .8225)],
        [R(3, .8105, 1.0), R(4, 0, .1035)],
        [R(4, .1243, .3937)], [R(4, .3817, .6067)],
        [R(4, .6274, .7200)], [R(4, .7080, .7804)], [R(4, .7684, .8459)],
    ],
    (2015, "G", "E"): [
        [R(3, .4784, .6555)], [R(3, .6435, .7876)], [R(3, .7756, .93)],
        [R(4, .1199, .2796)], [R(4, .2676, .4604)],
        [R(4, .4812, .5262)], [R(4, .5142, .5593)], [R(4, .5473, .5923)],
    ],
    (2015, "G", "I"): [
        [R(3, .5020, .6790)], [R(3, .6670, .8112)], [R(3, .7992, .93)],
        [R(4, .1200, .3125)], [R(4, .3005, .5262)],
        [R(4, .5471, .5921)], [R(4, .5801, .6252)], [R(4, .6132, .6581)],
    ],
    (2016, "G", "E"): [
        [R(3, .4340, .5894)], [R(3, .5774, .93)],
        [R(4, .0715, .2156)], [R(4, .2036, .2978)], [R(4, .2858, .4784)],
        [R(4, .4992, .5435)], [R(4, .5315, .5763)], [R(4, .5643, .6090)],
    ],
    (2016, "G", "I"): [
        [R(3, .4544, .6098)], [R(3, .5978, .93)],
        [R(4, .0612, .2053)], [R(4, .1933, .2875)], [R(4, .2755, .4846)],
        [R(4, .5057, .5502)], [R(4, .5382, .5830)], [R(4, .5710, .6157)],
    ],
}


# The collision also polluted the stored scheme crop on each run's final Part
# A card.  The 2013 Irish map resolved all four Part A IDs against later Parts.
# Keep those frozen `region` values for stable identity, but give the UI a
# visually audited additive correction through `schemeRegion`.
BASE_SCHEME_OVERRIDES = {
    (2013, "G", "E"): {
        "4": [R(3, .3757, .4696)],
    },
    (2013, "G", "I"): {
        "1": [R(3, .1641, .2466)],
        "2": [R(3, .2346, .3172)],
        "3": [R(3, .3052, .3877)],
        "4": [R(3, .3757, .4696)],
    },
    (2014, "G", "E"): {
        "3": [R(3, .3628, .4335)],
    },
    (2014, "G", "I"): {
        "3": [R(3, .3409, .4115)],
    },
    (2015, "A", "E"): {
        "3": [R(3, .4108, .5143)],
    },
    (2015, "A", "I"): {
        "3": [R(3, .3911, .5110)],
    },
    (2015, "G", "E"): {
        "3": [R(3, .3584, .4525)],
    },
    (2015, "G", "I"): {
        "3": [R(3, .3584, .4760)],
    },
    (2016, "G", "E"): {
        "3": [R(3, .3375, .4081)],
    },
    (2016, "G", "I"): {
        "3": [R(3, .3581, .4284)],
    },
}


# The 2015 Higher Part A cards are separately marked table rows, but each row
# needs the shared instructions and column headings to remain practicable.
BASE_PAPER_OVERRIDES = {
    (2015, "A", "E"): {
        "1": [R(2, .02, .66)],
        "2": [R(2, .02, .66)],
        "3": [R(2, .02, .66)],
    },
    (2015, "A", "I"): {
        "1": [R(2, .02, .66)],
        "2": [R(2, .02, .66)],
        "3": [R(2, .02, .66)],
    },
}


def protected(question: dict) -> dict:
    return {
        key: value
        for key, value in question.items()
        if key not in {
            "label", "printOrder", "schemeRegion", "paperRegion", "endP", "endY",
        }
    }


def digest(questions: list[dict]) -> str:
    payload = json.dumps(
        [protected(question) for question in questions],
        ensure_ascii=False,
        separators=(",", ":"),
    ).encode()
    return hashlib.sha256(payload).hexdigest()


def additions_for(key: tuple[int, str, str]) -> list[dict]:
    year, level, _language = key
    base_count = BASE_COUNTS[(year, level)]
    papers = PAPER_ADDITIONS[(year, level)]
    schemes = SCHEME_REGIONS[key]
    if len(papers) != len(schemes):
        raise ValueError(f"{key}: paper/scheme addition count mismatch")
    return [
        {
            "conf": 1.0,
            "label": spec["label"],
            "mode": "crop",
            "n": str(base_count + index),
            "pP": spec["paper_page"],
            "pY": [spec["paper_start"], spec["paper_end"]],
            "region": regions,
            "endP": spec["paper_page"],
            "endY": spec["paper_end"],
        }
        for index, (spec, regions) in enumerate(zip(papers, schemes), start=1)
    ]


def physical_ids(year: int, level: str, additions: list[dict]) -> list[str]:
    labels = BASE_LABELS[(year, level)]
    first_d = next(index for index, label in enumerate(labels) if label.startswith("PART D"))
    before_d = [str(index) for index in range(1, first_d + 1)]
    d_tail = [str(index) for index in range(first_d + 1, len(labels) + 1)]
    return before_d + [question["n"] for question in additions] + d_tail


def validate_sources(sidecar: dict, additions: list[dict], key: tuple[int, str, str]) -> None:
    year, _level, _language = key
    paper_path = CORPUS / "exampapers" / str(year) / sidecar["paperFileid"]
    scheme_path = CORPUS / "markingschemes" / str(year) / sidecar["schemeFileid"]
    with fitz.open(paper_path) as paper, fitz.open(scheme_path) as scheme:
        for question in additions:
            if not 1 <= question["pP"] <= question["endP"] <= len(paper):
                raise ValueError(f"{key}: paper crop outside official source")
            if not 0 <= question["pY"][0] < question["endY"] <= 1:
                raise ValueError(f"{key}: invalid paper crop")
            if not paper[question["pP"] - 1].get_text().strip():
                raise ValueError(f"{key}: paper anchor page has no text")
            last_page = 0
            for region in question["region"]:
                if not 1 <= region["p"] <= len(scheme) or region["p"] < last_page:
                    raise ValueError(f"{key}: scheme crop outside/order invalid")
                last_page = region["p"]
                if not 0 <= region["r"][1] < region["r"][3] <= 1:
                    raise ValueError(f"{key}: invalid scheme crop")


def repair(year: int, level: str, language: str) -> tuple[Path, int]:
    key = (year, level, language)
    fileid = f"LC058{level}LPA00{language}V.pdf"
    source = SOURCE_ROOT / str(year) / f"{fileid}.json"
    sidecar = json.loads(source.read_text())
    if sidecar["paperFileid"] != fileid:
        raise ValueError(f"{key}: unexpected paper document ID")
    if sidecar["schemeFileid"] != f"LC058{level}LP000{language}V.pdf":
        raise ValueError(f"{key}: unexpected scheme document ID")

    base_count = BASE_COUNTS[(year, level)]
    base = copy.deepcopy(sidecar["q"][:base_count])
    if [question["n"] for question in base] != [
        str(number) for number in range(1, base_count + 1)
    ]:
        raise ValueError(f"{key}: original stable ID range is incomplete")
    if digest(base) != BASE_HASHES[key]:
        raise ValueError(f"{key}: an original card changed; refusing additive repair")
    overrides = BASE_SCHEME_OVERRIDES[key]
    paper_overrides = BASE_PAPER_OVERRIDES.get(key, {})
    for question, label in zip(base, BASE_LABELS[(year, level)]):
        question["label"] = label
        if question["n"] in overrides:
            question["schemeRegion"] = overrides[question["n"]]
        if question["n"] in paper_overrides:
            question["paperRegion"] = paper_overrides[question["n"]]

    # Once recovered Parts B/C exist, the next physical anchor sits on the next
    # page. Cap Part A explicitly so its final card cannot bleed into Part B.
    first_d = next(
        index for index, label in enumerate(BASE_LABELS[(year, level)])
        if label.startswith("PART D")
    )
    last_a = base[first_d - 1]
    last_a["endP"] = last_a["pP"]
    last_a["endY"] = last_a["pY"][1]

    additions = additions_for(key)
    current_tail = sidecar["q"][base_count:]
    if len(current_tail) > len(additions) or [
        {k: v for k, v in question.items() if k != "printOrder"}
        for question in current_tail
    ] != [
        {k: v for k, v in question.items() if k != "printOrder"}
        for question in additions[:len(current_tail)]
    ]:
        raise ValueError(f"{key}: unexpected post-baseline cards; refusing to overwrite")
    validate_sources(sidecar, additions, key)

    sidecar["q"] = base + additions
    expected_ids = [str(number) for number in range(1, len(sidecar["q"]) + 1)]
    if [question["n"] for question in sidecar["q"]] != expected_ids:
        raise ValueError(f"{key}: repaired stable IDs are not contiguous")

    ordered_ids = physical_ids(year, level, additions)
    if len(ordered_ids) != len(sidecar["q"]) or len(set(ordered_ids)) != len(ordered_ids):
        raise ValueError(f"{key}: physical order is not a complete ID permutation")
    rank = {stable_id: index for index, stable_id in enumerate(ordered_ids, start=1)}
    for question in sidecar["q"]:
        question["printOrder"] = rank[question["n"]]
    physical = sorted(sidecar["q"], key=lambda question: question["printOrder"])
    anchors = [(question["pP"], question["pY"][0]) for question in physical]
    if anchors != sorted(anchors) or len(anchors) != len(set(anchors)):
        raise ValueError(f"{key}: physical paper anchors are not strictly increasing")

    out = OUT_ROOT / str(year) / f"{fileid}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(sidecar, ensure_ascii=False, indent=2) + "\n")
    return out, len(additions)


def main() -> None:
    total = 0
    maps = 0
    for year, level in BASE_COUNTS:
        for language in ("E", "I"):
            out, added = repair(year, level, language)
            total += added
            maps += 1
            shown = out.relative_to(REPO) if out.is_relative_to(REPO) else out
            print(f"wrote {shown} (+{added} cards)")
    if maps != 10 or total != 82:
        raise ValueError(f"expected 82 cards across 10 maps, got {total} across {maps}")
    print(f"Japanese legacy aural additions: {total} cards across {maps} maps")


if __name__ == "__main__":
    main()
