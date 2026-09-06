#!/usr/bin/env python3
"""Build the audited 2024–2026 Japanese written-paper answer maps.

The generic language mapper deliberately stopped at reading questions and the
Japanese papers subsequently had no written-paper sidecars for these years.
This subject-specific map uses anchors checked against the bilingual SEC papers
and the English SEC marking schemes.  Question IDs follow physical order; the
larger composition tasks include their official marking rubric.

Run from the repository root:
    python3 scripts/paper-trail/japanese_written.py

Set PT_JAPANESE_OUT to stage the generated sidecars outside answers/.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

import fitz


HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
CORPUS = REPO / "paper-trail-corpus"
OUT_ROOT = Path(os.environ.get("PT_JAPANESE_OUT", HERE / "answers"))


def R(page: int, start: float, end: float) -> dict:
    return {"p": page, "r": [0.0, start, 1.0, end]}


def C(
    label: str,
    paper_page: int,
    paper_y: float,
    *regions: dict,
    end: tuple[int, float] | None = None,
) -> dict:
    return {
        "label": label,
        "pP": paper_page,
        "pY": [paper_y, end[1] if end and end[0] == paper_page else 1.0],
        "region": list(regions),
        "end": end,
    }


MAPS: dict[tuple[int, str], list[dict]] = {
    (2024, "A"): [
        C("Q1 A · 1", 3, .0633, R(6, .0985, .3367)),
        C("Q1 A · 2", 3, .3062, R(6, .3247, .4932)),
        C("Q1 A · 3", 3, .5091, R(6, .4812, .7479)),
        C("Q1 A · 4", 3, .7754, R(6, .7359, .90), end=(3, .93)),
        C("Q1 B · 1", 4, .5314, R(7, .0408, .1850)),
        C("Q1 B · 2", 4, .7316, R(7, .1730, .3400), end=(4, .93)),
        C("Q2 A · 1", 7, .0366, R(7, .3596, .5864)),
        C("Q2 A · 2", 7, .2343, R(7, .5744, .9113)),
        C("Q2 A · 3", 7, .5678, R(7, .8993, 1.0), R(8, 0.0, .3740), end=(7, .93)),
        C("Q2 B · Kanji 1", 8, .0662, R(8, .3740, .5307)),
        C("Q2 B · Kanji 2", 8, .4945, R(8, .5187, .90), end=(8, .93)),
        C("Q2 C · Grammar 1", 9, .0732, R(9, .0408, .2217)),
        C("Q2 C · Grammar 2", 9, .4742, R(9, .2097, .4151), end=(9, .93)),
        C("Q3 A · 1", 11, .0655, R(9, .4151, .5194)),
        C("Q3 A · 2", 11, .1677, R(9, .5074, .5891)),
        C("Q3 A · 3", 11, .2721, R(9, .5771, .6587)),
        C("Q3 A · 4", 11, .3591, R(9, .6467, .7456)),
        C("Q3 A · 5", 11, .4635, R(9, .7336, .7975)),
        C("Q3 A · 6", 11, .5504, R(9, .7855, .91)),
        C("Q3 B · 1", 11, .6563, R(10, .0408, .1316)),
        C("Q3 B · 2", 11, .7183, R(10, .1196, .1815)),
        C("Q3 B · 3", 11, .7773, R(10, .1695, .2395)),
        C("Q3 B · 4", 11, .8428, R(10, .2275, .2809), end=(11, .93)),
        C("Q3 C · Kanji", 12, .0366, R(10, .2809, .5086)),
        C("Q3 D · Grammar", 12, .4724, R(10, .5086, .84), end=(12, .93)),
        C("Q4 · Written production (choose A, B or C)", 14, .0497,
          R(11, .0408, .92), R(12, .0405, .92), end=(15, .93)),
        C("Q5 · Japanese study scholarship application", 16, .0497,
          R(13, .0408, .92), R(14, .0408, .92), end=(19, .93)),
    ],
    (2024, "G"): [
        C("Q1 · 1", 3, .0671, R(5, .1627, .4411)),
        C("Q1 · 2", 3, .2988, R(5, .4291, .5063)),
        C("Q1 · 3", 3, .4264, R(5, .4943, .5585)),
        C("Q1 · 4", 3, .4844, R(5, .5465, .6107)),
        C("Q1 · 5", 3, .5772, R(5, .5987, .6630)),
        C("Q1 · 6", 3, .6286, R(5, .6510, .8419)),
        C("Q1 · 7", 3, .8428, R(5, .8299, .8941), end=(3, .93)),
        C("Q2 A · 1", 5, .0897, R(6, .1453, .2101)),
        C("Q2 A · 2", 5, .1463, R(6, .1981, .2570)),
        C("Q2 A · 3", 5, .2130, R(6, .2450, .3232)),
        C("Q2 A · 4", 5, .3115, R(6, .3112, .3662)),
        C("Q2 A · 5", 5, .3631, R(6, .3542, .4137)),
        C("Q2 A · 6", 5, .4254, R(6, .4017, .4620)),
        C("Q2 B · True or false", 5, .4805, R(6, .4620, .90), end=(5, .93)),
        C("Q2 C · Kanji", 6, .0702, R(7, .1105, .4411), end=(6, .93)),
        C("Q2 D · Culture and society", 7, .0702, R(7, .4291, .85), end=(7, .93)),
        C("Q3 A · 1", 9, .0992, R(8, .1344, .2199)),
        C("Q3 A · 2", 9, .1630, R(8, .2079, .2687)),
        C("Q3 A · 3", 9, .2616, R(8, .2567, .3514)),
        C("Q3 A · 4", 9, .3311, R(8, .3394, .5689), end=(9, .93)),
        C("Q3 A · 5", 10, .0702, R(8, .5569, .90)),
        C("Q3 B · Grammar 1", 10, .4173, R(9, .1105, .4584)),
        C("Q3 B · Grammar 2", 11, .0702, R(9, .4464, .90), end=(11, .93)),
        C("Q4 · School cloze", 12, .1158, R(10, .1145, .5622), end=(12, .93)),
        C("Q5 · Friends", 13, .0797, R(10, .5502, .92), end=(13, .93)),
    ],
    (2025, "A"): [
        C("Q1 A · 1", 3, .0691, R(7, .0683, .3043)),
        C("Q1 A · 2", 3, .2866, R(7, .2923, .4445)),
        C("Q1 A · 3", 3, .4199, R(7, .4325, .5602)),
        C("Q1 A · 4", 3, .5359, R(7, .5482, .6243)),
        C("Q1 A · 5", 3, .6113, R(7, .6123, .6884)),
        C("Q1 A · 6", 3, .6693, R(7, .6764, .7463)),
        C("Q1 A · 7", 3, .7447, R(7, .7343, .93), end=(3, .93)),
        C("Q1 B · 1", 4, .5488, R(8, .0470, .2411)),
        C("Q1 B · 2", 4, .7146, R(8, .2291, .3710)),
        C("Q1 B · 3", 4, .8617, R(8, .3590, .4525), end=(4, .93)),
        C("Q2 A · 1", 7, .0565, R(8, .4525, .94)),
        C("Q2 A · 2", 7, .3102, R(9, .0433, .5585)),
        C("Q2 A · 3 (translation)", 7, .7625, R(9, .5465, .7571), end=(7, .93)),
        C("Q2 B · Kanji 1", 8, .0662, R(9, .7451, .94)),
        C("Q2 B · Kanji 2", 8, .4967, R(10, .0366, .3518), end=(8, .93)),
        C("Q2 C · Grammar 1", 9, .0732, R(10, .3518, .6780)),
        C("Q2 C · Grammar 2", 9, .4734, R(10, .6660, .94), end=(9, .93)),
        C("Q3 A · 1", 11, .0673, R(11, .0470, .1709)),
        C("Q3 A · 2", 11, .1407, R(11, .1589, .2692)),
        C("Q3 A · 3", 11, .2451, R(11, .2572, .3532)),
        C("Q3 A · 4", 11, .3495, R(11, .3412, .4404)),
        C("Q3 A · 5", 11, .4365, R(11, .4284, .5490)),
        C("Q3 B · 1", 11, .6112, R(11, .5490, .6925)),
        C("Q3 B · 2", 11, .6870, R(11, .6805, .7852)),
        C("Q3 B · 3", 11, .7628, R(11, .7732, .8707)),
        C("Q3 B · 4", 11, .8407, R(11, .8587, .94), end=(11, .93)),
        C("Q3 C · Kanji", 12, .0366, R(12, .0470, .3827)),
        C("Q3 D · Grammar", 12, .4672, R(12, .3707, .90), end=(12, .93)),
        C("Q4 · Written production (choose A, B or C)", 14, .0479,
          R(13, .0461, .94), R(14, .0470, .94), end=(15, .93)),
        C("Q5 · Hosting a Japanese exchange student", 16, .0478,
          R(15, .0470, .94), R(16, .0470, .94), end=(19, .93)),
    ],
    (2025, "G"): [
        C("Q1 · 1", 3, .0718, R(5, .1078, .4036)),
        C("Q1 · 2", 3, .3061, R(5, .3916, .4558)),
        C("Q1 · 3", 3, .4191, R(5, .4438, .5253)),
        C("Q1 · 4", 3, .5293, R(5, .5133, .5944)),
        C("Q1 · 5", 3, .6410, R(5, .5824, .7429)),
        C("Q1 · 6", 3, .8260, R(5, .7309, .82), end=(3, .93)),
        C("Q2 A · 1", 5, .0948, R(6, .0804, .2338)),
        C("Q2 A · 2", 5, .2079, R(6, .2218, .3393)),
        C("Q2 A · 3", 5, .3471, R(6, .3273, .4394)),
        C("Q2 B · 1", 5, .6103, R(6, .5103, .5676)),
        C("Q2 B · 2", 5, .6604, R(6, .5556, .6254)),
        C("Q2 B · 3", 5, .7106, R(6, .6134, .6735)),
        C("Q2 B · 4", 5, .7693, R(6, .6615, .7241)),
        C("Q2 B · 5", 5, .8280, R(6, .7121, .7888)),
        C("Q2 B · 6", 5, .8882, R(6, .7768, .90), end=(5, .93)),
        C("Q2 C · Kanji", 6, .0661, R(7, .0456, .3385), end=(6, .93)),
        C("Q2 D · Culture and society", 7, .0702, R(7, .3265, .4254), end=(7, .93)),
        C("Q3 A · 1", 9, .1050, R(7, .4254, .5458)),
        C("Q3 A · 2", 9, .1949, R(7, .5338, .5928)),
        C("Q3 A · 3", 9, .2848, R(7, .5808, .6398)),
        C("Q3 A · 4", 9, .3631, R(7, .6278, .93), end=(9, .93)),
        C("Q3 A · 5", 10, .0702, R(8, .0510, .3244)),
        C("Q3 B · Grammar 1", 10, .4028, R(8, .3244, .6215)),
        C("Q3 B · Grammar 2", 11, .0702, R(8, .6095, .90), end=(11, .93)),
        C("Q4 · School cloze", 12, .1050, R(9, .0825, .5291), end=(12, .93)),
        C("Q5 · School", 13, .0681, R(9, .5171, .92), end=(13, .93)),
    ],
    (2026, "A"): [
        C("Q1 A · 1", 3, .0633, R(9, .1007, .2996)),
        C("Q1 A · 2", 3, .2778, R(9, .2876, .6302)),
        C("Q1 A · 3", 3, .5040, R(9, .6182, .7868)),
        C("Q1 A · 4", 3, .6316, R(9, .7748, 1.0), R(10, 0.0, .1674)),
        C("Q1 A · 5", 3, .8658, R(10, .1554, .2370), end=(3, .93)),
        C("Q1 B · 1", 4, .4624, R(10, .2370, .6024)),
        C("Q1 B · 2", 4, .7065, R(10, .5904, .88), end=(4, .93)),
        C("Q2 A · 1", 7, .0713, R(11, .0804, .6493)),
        C("Q2 A · 2", 7, .4947, R(11, .6373, 1.0), R(12, 0.0, .1313)),
        C("Q2 A · 3 (translation)", 7, .7824, R(12, .1193, .3071), end=(7, .93)),
        C("Q2 B · Kanji 1", 8, .0636, R(12, .3071, .4991)),
        C("Q2 B · Kanji 2", 8, .4919, R(12, .4871, .6770), end=(8, .93)),
        C("Q2 C · Grammar 1", 9, .0698, R(12, .6770, 1.0)),
        C("Q2 C · Grammar 2", 9, .5186, R(13, .0456, .2150), end=(9, .93)),
        C("Q3 A · 1", 11, .0626, R(13, .2351, 1.0), R(14, 0.0, .3326)),
        C("Q3 A · 2", 11, .6889, R(14, .3206, .6636), end=(11, .93)),
        C("Q3 B · Kanji", 12, .0366, R(14, .6636, .90)),
        C("Q3 C · Grammar", 12, .4714, R(15, .0456, .85), end=(12, .93)),
        C("Q4 · Written production (choose 1, 2 or 3)", 14, .0479,
          R(16, .0461, .94), R(17, .0456, .94), end=(15, .93)),
        C("Q5 · Daily school routine video", 16, .0478,
          R(18, .0456, .94), R(19, .0456, .94), end=(19, .93)),
    ],
    (2026, "G"): [
        C("Q1 · 1", 3, .0702, R(6, .0833, .3095)),
        C("Q1 · 2", 3, .3143, R(6, .2975, .4660)),
        C("Q1 · 3", 3, .3735, R(6, .4540, .5701)),
        C("Q1 · 4", 3, .4528, R(6, .5581, .7604)),
        C("Q1 · 5", 3, .5470, R(6, .7484, .93)),
        C("Q1 · 6", 3, .6062, R(7, .0456, .3371), end=(3, .93)),
        C("Q2 A · 1", 5, .0992, R(7, .3718, .4936)),
        C("Q2 A · 2", 5, .1760, R(7, .4816, .5646)),
        C("Q2 A · 3", 5, .2224, R(7, .5526, .6304)),
        C("Q2 A · 4", 5, .2818, R(7, .6184, .7000)),
        C("Q2 A · 5", 5, .3457, R(7, .6880, .8044)),
        C("Q2 A · 6", 5, .3877, R(7, .7924, .93)),
        C("Q2 B · 1", 5, .5948, R(8, .0456, .1316)),
        C("Q2 B · 2", 5, .6395, R(8, .1196, .1769)),
        C("Q2 B · 3", 5, .6977, R(8, .1649, .2468)),
        C("Q2 B · 4", 5, .7391, R(8, .2348, .2920)),
        C("Q2 B · 5", 5, .7806, R(8, .2800, .3373)),
        C("Q2 B · 6", 5, .8420, R(8, .3253, .3825), end=(5, .93)),
        C("Q2 C · Kanji", 6, .0702, R(8, .3825, .7884), end=(6, .93)),
        C("Q2 D · Culture and society", 7, .0661, R(8, .7764, .92), end=(7, .93)),
        C("Q3 A · 1", 9, .1050, R(9, .0739, .1779)),
        C("Q3 A · 2", 9, .1724, R(9, .1659, .2718)),
        C("Q3 A · 3", 9, .2594, R(9, .2598, .3188)),
        C("Q3 A · 4", 9, .3268, R(9, .3068, .5399), end=(9, .93)),
        C("Q3 A · 5", 10, .0702, R(9, .5279, .78)),
        C("Q3 B · Grammar 1", 10, .4146, R(10, .0456, .3775)),
        C("Q3 B · Grammar 2", 11, .0702, R(10, .3655, .85), end=(11, .93)),
        C("Q4 · School cloze", 12, .0829, R(11, .0814, .5277), end=(12, .93)),
        C("Q5 · Summer holidays", 13, .0797, R(11, .5157, .92), end=(13, .93)),
    ],
}


def write_map(year: int, level_code: str, cards: list[dict]) -> Path:
    paper_fileid = f"LC058{level_code}LP000BV.pdf"
    scheme_fileid = f"LC058{level_code}LP000EV.pdf"
    paper_path = CORPUS / "exampapers" / str(year) / paper_fileid
    scheme_path = CORPUS / "markingschemes" / str(year) / scheme_fileid
    if not paper_path.exists() or not scheme_path.exists():
        raise FileNotFoundError(f"Missing SEC source for {year} {level_code}")

    with fitz.open(paper_path) as paper, fitz.open(scheme_path) as scheme:
        previous = (0, 0.0)
        questions = []
        for index, card in enumerate(cards, start=1):
            anchor = (card["pP"], card["pY"][0])
            if anchor <= previous:
                raise ValueError(f"Non-monotonic paper anchor at {year} {level_code} {card['label']}")
            previous = anchor
            if not 1 <= card["pP"] <= len(paper):
                raise ValueError(f"Paper page out of range: {card['label']}")
            for region in card["region"]:
                if not 1 <= region["p"] <= len(scheme):
                    raise ValueError(f"Scheme page out of range: {card['label']}")
                if not 0 <= region["r"][1] < region["r"][3] <= 1:
                    raise ValueError(f"Invalid scheme crop: {card['label']}")

            question = {
                "conf": 1.0,
                "label": card["label"],
                "mode": "crop",
                "n": str(index),
                "pP": card["pP"],
                "pY": card["pY"],
                "region": card["region"],
            }
            if card["end"]:
                question["endP"], question["endY"] = card["end"]
            questions.append(question)

        sidecar = {
            "band": [1, len(scheme) + 1],
            "component": "000",
            "copyright": "© State Examinations Commission",
            "paperFileid": paper_fileid,
            "q": questions,
            "schemeFileid": scheme_fileid,
            "v": 1,
        }

    out = OUT_ROOT / str(year) / f"{paper_fileid}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(sidecar, ensure_ascii=False, indent=2) + "\n")
    return out


def main() -> None:
    total = 0
    for (year, level_code), cards in sorted(MAPS.items()):
        out = write_map(year, level_code, cards)
        total += len(cards)
        print(f"wrote {out.relative_to(REPO) if out.is_relative_to(REPO) else out} ({len(cards)} cards)")
    print(f"Japanese written total: {total} cards")


if __name__ == "__main__":
    main()
