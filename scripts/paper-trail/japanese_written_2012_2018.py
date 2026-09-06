#!/usr/bin/env python3
"""Repair omitted sections in the 2012-2018 Japanese written maps.

All 28 language/level sidecars in this range stopped at Question 3 even
though the official papers contain assessed Questions 4 and 5.  This builder
also exposes assessed Kanji, grammar and culture sections that historic maps
hid inside coarse reading cards.  It is intentionally additive: it verifies a
SHA-256 sentinel for every original question array, keeps every stable ID and
crop unchanged, and gives every recovered section a new stable ID.

Run from the repository root:
    python3 scripts/paper-trail/japanese_written_2012_2018.py

Set PT_JAPANESE_OLDER_OUT to stage the generated sidecars outside answers/.
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
OUT_ROOT = Path(os.environ.get("PT_JAPANESE_OLDER_OUT", SOURCE_ROOT))


def R(page: int, start: float, end: float) -> dict:
    return {"p": page, "r": [0.0, start, 1.0, end]}


def C(
    number: int,
    label: str,
    paper_page: int,
    paper_y: float,
    regions: list[dict],
    end_page: int,
    end_y: float = 0.93,
) -> dict:
    return {
        "conf": 1.0,
        "label": label,
        "mode": "crop",
        "n": str(number),
        "pP": paper_page,
        "pY": [paper_y, 1.0],
        "region": regions,
        "endP": end_page,
        "endY": end_y,
    }


def S(
    after: int,
    label: str,
    paper_page: int,
    paper_y: float,
    end_page: int,
    end_y: float,
    topic: str,
    *regions: dict,
) -> dict:
    """Describe one additive skill card and its physical insertion point."""
    return {
        "after": after,
        "label": label,
        "paper_page": paper_page,
        "paper_y": paper_y,
        "end_page": end_page,
        "end_y": end_y,
        "topic": topic,
        "regions": list(regions),
    }


# Python JSON serialisation sentinels for the untouched, pre-repair q arrays.
# A source map that has drifted is rejected rather than silently rewritten.
BASE_HASHES = {
    (2012, "A", "E"): "8e508595591780a73dc6fc777ccfc86898e7f74b5678297f9a822a045e27fa4b",
    (2012, "A", "I"): "20b5cf24ca19841232b03a23eb32bcf98ec7e657fa5b8cc5e0d6dd33eb6d02e1",
    (2012, "G", "E"): "8e6740376acaaefc1a2e4cd3c2f21ef0d80b805ca78168f7468c47d84f5c0ef5",
    (2012, "G", "I"): "2277a7eb15396a8a68e11cf74ea8dc133a1922cbde88985ea9c03097608f44cb",
    (2013, "A", "E"): "6e555cc399d2ee362f76d33057b6e84f9c8f46d3d2420ccb44f63ef5b88b6e1e",
    (2013, "A", "I"): "567a6048a92e34b9b7d1de873086564e650bd5a3883e8bf2f6e256e80ea3cd55",
    (2013, "G", "E"): "495834ea0973e97a3042a83a4c54507af745b5244e609ee0d664f3335ba5ee6f",
    (2013, "G", "I"): "98ee912d9e6d25c5163fa093e881ea57e346e2f5f58e9afbd1b0bb4559a86937",
    (2014, "A", "E"): "994411c4778ac34b7ef8f57721016aa5548541f415fa1e7352408fe36440339d",
    (2014, "A", "I"): "3ff5cea47986565fb775f73489b0979bf5bf09f15bd7777c81763d6a8ecb260e",
    (2014, "G", "E"): "2aedd94ee704d06c3a02e11c65b3218337183a25bfe7e69edb1627c9c07d1466",
    (2014, "G", "I"): "2f30ccb612267d23c28c34232e0d1147cc1ea13a8075af667c21bd77b0fcdf55",
    (2015, "A", "E"): "468d0df2d1c8a77fe7a5b73aac23f6fe451af5ae8bacf00396429a52ec55d0e8",
    (2015, "A", "I"): "f2e201d4a9c5a9fdf37545563a28ceebc6719f9cd2fa82b4c401dd3e71d77827",
    (2015, "G", "E"): "f9f0980672ba7f22d991620be0dffae272aefa0ea51a9be3b0a2e7a986ac8eca",
    (2015, "G", "I"): "3439ac1a79e62181ced515872a758ff5a529de4290cf0007c14eafb6d5a195cb",
    (2016, "A", "E"): "0cc163ea4037aecffa343600ef93f7c6abc71a18ab845fbf280953048c7f3a93",
    (2016, "A", "I"): "a5d73cbd973694901edb7953aef6d0049637c216f430c6eb515c5417b961d9f3",
    (2016, "G", "E"): "5e6b3f98e833e930c147a98c3f2f5f613e08e7733c69adf9a2b110b127214a56",
    (2016, "G", "I"): "d80f3491ab20239ac33be3b1b2bf5c72d8e7fad2c8c25c87b3e52f92184aa428",
    (2017, "A", "E"): "95077342f1a2cf0931d6800e8b34f1127b3b588043637b7a2a63c5feb2289515",
    (2017, "A", "I"): "09a776bb0935ab2d415e49478e6d1c2d12dd3df48ed75d8b4600e44c22be24a4",
    (2017, "G", "E"): "e174b2eb65a0d2b039975cb6080fe333193ec33affb28c337ebb63a021a28d8d",
    (2017, "G", "I"): "e0b8738272bbe662b86d767bf82681d09770a09e8354835dd7e0b4d9a00d58bf",
    (2018, "A", "E"): "891dda02849a7709e7ef90e957910eebf884896b3ff635bdec4318d72688f7a6",
    (2018, "A", "I"): "9fcde3b9f3969671a428dca7571474770ea09de11f859867ee67e9f4dc59f5a5",
    (2018, "G", "E"): "957be131675b9816040320854e00cc92745fe8992ffd256cf8d362baa0adc61f",
    (2018, "G", "I"): "f72562a18a391dc0602724e8c5a6e19d6353e9cb22bc904b7ec9c2378bc5c772",
}


BASE_COUNTS = {
    (2012, "A", "E"): 21, (2012, "A", "I"): 20,
    (2012, "G", "E"): 14, (2012, "G", "I"): 13,
    (2013, "A", "E"): 3, (2013, "A", "I"): 6,
    (2013, "G", "E"): 3, (2013, "G", "I"): 8,
    (2014, "A", "E"): 5, (2014, "A", "I"): 18,
    (2014, "G", "E"): 13, (2014, "G", "I"): 12,
    (2015, "A", "E"): 17, (2015, "A", "I"): 8,
    (2015, "G", "E"): 16, (2015, "G", "I"): 12,
    (2016, "A", "E"): 22, (2016, "A", "I"): 19,
    (2016, "G", "E"): 14, (2016, "G", "I"): 14,
    (2017, "A", "E"): 14, (2017, "A", "I"): 20,
    (2017, "G", "E"): 17, (2017, "G", "I"): 11,
    (2018, "A", "E"): 23, (2018, "A", "I"): 21,
    (2018, "G", "E"): 3, (2018, "G", "I"): 18,
}


# (paper page, vertical anchor, final paper page).  EV and IV exam papers are
# byte-identical within each year/level, while their marking schemes differ.
PAPER_SPECS = {
    (2012, "A"): ((12, .0313, 14), (15, .0313, 18)),
    (2012, "G"): ((10, .1019, 10), (11, .0343, 11)),
    (2013, "A"): ((12, .0331, 14), (15, .0332, 18)),
    (2013, "G"): ((12, .0698, 12), (13, .0443, 13)),
    (2014, "A"): ((14, .0276, 15), (16, .0263, 19)),
    (2014, "G"): ((12, .0834, 12), (13, .0343, 13)),
    (2015, "A"): ((14, .0519, 15), (16, .0517, 19)),
    (2015, "G"): ((11, .0853, 11), (12, .0519, 12)),
    (2016, "A"): ((14, .0276, 15), (16, .0291, 19)),
    (2016, "G"): ((11, .0915, 11), (12, .0349, 12)),
    (2017, "A"): ((14, .0351, 15), (16, .0351, 19)),
    (2017, "G"): ((11, .0851, 11), (12, .0426, 12)),
    (2018, "A"): ((14, .0687, 15), (16, .0687, 19)),
    (2018, "G"): ((11, .1007, 11), (12, .0654, 12)),
}


SCHEME_REGIONS = {
    (2012, "A", "E"): ([R(12, .1067, .93), R(13, .1216, .85)], [R(14, .0601, .93), R(15, .0759, .85)]),
    (2012, "A", "I"): ([R(13, .0889, .93), R(14, .1062, .85)], [R(15, .0601, .93), R(16, .0600, .85)]),
    (2012, "G", "E"): ([R(9, .0601, .4857)], [R(9, .4857, .93), R(10, .0833, .85)]),
    (2012, "G", "I"): ([R(10, .0599, .4882)], [R(10, .4882, .93), R(11, .0831, .85)]),
    (2013, "A", "E"): ([R(10, .0642, .93), R(11, .0641, .85)], [R(12, .0751, .93), R(13, .0641, .85)]),
    (2013, "A", "I"): ([R(10, .3478, .93), R(11, .0641, .85)], [R(12, .0806, .93), R(13, .0804, .85)]),
    (2013, "G", "E"): ([R(9, .1045, .4999)], [R(9, .4999, .93), R(10, .1250, .85)]),
    (2013, "G", "I"): ([R(10, .0842, .4936)], [R(10, .4936, .93), R(11, .0843, .85)]),
    (2014, "A", "E"): ([R(11, .0570, .93), R(12, .0669, .85)], [R(13, .0670, .93), R(14, .0600, .85)]),
    (2014, "A", "I"): ([R(11, .0816, .93), R(12, .0660, .85)], [R(13, .0497, .93), R(14, .0660, .85)]),
    (2014, "G", "E"): ([R(9, .0775, .4284)], [R(9, .4284, .93), R(10, .0785, .75)]),
    (2014, "G", "I"): ([R(9, .3454, .90)], [R(10, .1087, .93), R(11, .0800, .70)]),
    (2015, "A", "E"): ([R(12, .0478, .93), R(13, .0477, .85)], [R(14, .0478, .93), R(15, .0477, .85)]),
    (2015, "A", "I"): ([R(11, .0478, .93), R(12, .0477, .85)], [R(13, .0806, .93), R(14, .0477, .85)]),
    (2015, "G", "E"): ([R(10, .0797, .5545)], [R(10, .5545, .93), R(11, .0660, .82)]),
    (2015, "G", "I"): ([R(10, .0648, .5435)], [R(10, .5435, .93), R(11, .0661, .90)]),
    (2016, "A", "E"): ([R(11, .0665, .93), R(12, .0509, .85)], [R(13, .0519, .93), R(14, .0673, .87)]),
    (2016, "A", "I"): ([R(12, .0492, .93), R(13, .0818, .90)], [R(14, .0502, .93), R(15, .0490, .90)]),
    (2016, "G", "E"): ([R(9, .0506, .4279)], [R(9, .4279, .93), R(10, .0586, .75)]),
    (2016, "G", "I"): ([R(9, .0567, .4340)], [R(9, .4340, .93), R(10, .0730, .82)]),
    (2017, "A", "E"): ([R(11, .0490, .93), R(12, .0653, .86)], [R(13, .0655, .93), R(14, .0489, .86)]),
    (2017, "A", "I"): ([R(11, .0514, .93), R(12, .0512, .88)], [R(13, .0626, .93), R(14, .0348, .88)]),
    (2017, "G", "E"): ([R(9, .0802, .4756)], [R(9, .4756, .93), R(10, .1663, .75)]),
    (2017, "G", "I"): ([R(9, .0718, .4672)], [R(9, .4672, .93), R(10, .1579, .85)]),
    (2018, "A", "E"): ([R(12, .0661, .93), R(13, .0660, .86)], [R(14, .0661, .93), R(15, .0660, .87)]),
    (2018, "A", "I"): ([R(12, .5049, .93), R(13, .0470, .93), R(14, .0474, .92)], [R(15, .0473, .93), R(16, .0474, .92)]),
    (2018, "G", "E"): ([R(10, .0667, .4621)], [R(10, .4621, .93), R(11, .0679, .78)]),
    (2018, "G", "I"): ([R(10, .0643, .4587)], [R(10, .4587, .93), R(11, .0656, .85)]),
}


# The historic mapper often made one coarse reading card for an entire printed
# question.  That technically displayed the page, but it made the assessed
# Kanji/grammar/culture sub-section impossible to find under its own topic.
# These audited cards deliberately overlap the coarse card and use new IDs.
# ``after`` names the last original stable ID before the recovered section in
# physical paper order; it is used only to calculate display order.
SKILL_SPECS = {
    # Higher — StudyClix's 2013-2018 Kanji/Grammar heading families.
    (2013, "A", "E"): [
        S(2, "Q2 · B · Kanji", 7, .0490, 7, .3953, "japanese-5-4", R(8, .1785, .3383)),
        S(2, "Q2 · C · Grammar", 7, .3953, 8, .93, "japanese-5-5", R(8, .3383, .93)),
        S(3, "Q3 · B · Kanji", 11, .0490, 11, .93, "japanese-5-4", R(9, .6576, .93)),
    ],
    (2013, "A", "I"): [
        S(5, "Ceist 2 · B · Kanji", 7, .0490, 7, .3953, "japanese-5-4", R(8, .3210, .4862)),
        S(5, "Ceist 2 · C · Gramadach", 7, .3953, 8, .93, "japanese-5-5", R(8, .4862, .93), R(9, 0, .2581)),
        S(6, "Ceist 3 · B · Kanji", 11, .0490, 11, .93, "japanese-5-4", R(10, .0642, .3478)),
    ],
    (2014, "A", "E"): [
        S(3, "Q2 · B · Kanji", 8, .0268, 8, .93, "japanese-5-4", R(8, .5715, .93)),
        S(3, "Q2 · C · Grammar", 9, .0267, 9, .93, "japanese-5-5", R(9, .0670, .4672)),
        S(5, "Q3 · C · Kanji", 12, .0268, 12, .3992, "japanese-5-4", R(10, .2619, .4198)),
        S(5, "Q3 · D · Grammar", 12, .3992, 12, .93, "japanese-5-5", R(10, .4198, .93), R(11, 0, .0570)),
    ],
    (2014, "A", "I"): [
        S(13, "Ceist 2 · B · Kanji", 8, .0268, 8, .93, "japanese-5-4", R(8, .4560, .7429)),
        S(13, "Ceist 2 · C · Gramadach", 9, .0267, 9, .93, "japanese-5-5", R(8, .7429, .93), R(9, 0, .2457)),
        S(18, "Ceist 3 · C · Kanji", 12, .0268, 12, .3992, "japanese-5-4", R(10, .2866, .4773)),
        S(18, "Ceist 3 · D · Gramadach", 12, .3992, 12, .93, "japanese-5-5", R(10, .4773, .93), R(11, 0, .0816)),
    ],
    (2015, "A", "E"): [
        S(12, "Q2 · B · Kanji", 8, .0511, 8, .93, "japanese-5-4", R(8, .2397, .5616)),
        S(12, "Q2 · C · Grammar", 9, .0511, 9, .93, "japanese-5-5", R(8, .5616, .93), R(9, 0, .93)),
        S(17, "Q3 · C · Kanji", 12, .0511, 12, .4713, "japanese-5-4", R(10, .6956, .93)),
        S(17, "Q3 · D · Grammar", 12, .4713, 12, .93, "japanese-5-5", R(11, .0478, .93), R(12, 0, .0478)),
    ],
    (2015, "A", "I"): [
        S(6, "Ceist 2 · B · Kanji", 8, .0511, 8, .93, "japanese-5-4", R(7, .7389, .93), R(8, 0, .2058)),
        S(6, "Ceist 2 · C · Gramadach", 9, .0511, 9, .93, "japanese-5-5", R(8, .2058, .93), R(9, 0, .0478)),
        S(8, "Ceist 3 · C · Kanji", 12, .0511, 12, .4713, "japanese-5-4", R(9, .7681, .93), R(10, 0, .0478)),
        S(8, "Ceist 3 · D · Gramadach", 12, .4713, 12, .93, "japanese-5-5", R(10, .0478, .93), R(11, 0, .0478)),
    ],
    (2016, "A", "I"): [
        S(13, "Ceist 2 · B · Kanji", 8, .0268, 8, .3618, "japanese-5-4", R(9, .5219, .7105)),
        S(13, "Ceist 2 · C · Gramadach", 8, .3618, 8, .93, "japanese-5-5", R(9, .7105, .93), R(10, 0, .0656)),
        S(19, "Ceist 3 · C · Kanji", 12, .0469, 13, .0442, "japanese-5-4", R(10, .8016, .93), R(11, 0, .2861)),
        S(19, "Ceist 3 · D · Gramadach", 13, .0442, 13, .93, "japanese-5-5", R(11, .2861, .93), R(12, 0, .0492)),
    ],
    (2017, "A", "E"): [
        S(12, "Q2 · B · Kanji", 8, .0366, 8, .93, "japanese-5-4", R(8, .3947, .7002)),
        S(12, "Q2 · C · Grammar", 9, .0365, 9, .93, "japanese-5-5", R(8, .7002, .93), R(9, 0, .2317)),
        S(14, "Q3 · C · Kanji", 12, .0365, 12, .4619, "japanese-5-4", R(10, .0634, .2450)),
        S(14, "Q3 · D · Grammar", 12, .4619, 12, .93, "japanese-5-5", R(10, .2450, .93), R(11, 0, .0490)),
    ],
    (2017, "A", "I"): [
        S(12, "Ceist 2 · B · Kanji", 8, .0366, 8, .93, "japanese-5-4", R(8, .3916, .93), R(9, 0, .0514)),
        S(12, "Ceist 2 · C · Gramadach", 9, .0365, 9, .93, "japanese-5-5", R(9, .0514, .3838)),
        S(20, "Ceist 3 · C · Kanji", 12, .0365, 12, .4619, "japanese-5-4", R(10, .3679, .5823)),
        S(20, "Ceist 3 · D · Gramadach", 12, .4619, 12, .93, "japanese-5-5", R(10, .5823, .93), R(11, 0, .0514)),
    ],
    (2018, "A", "E"): [
        S(14, "Q2 · B · Kanji", 8, .0702, 8, .3924, "japanese-5-4", R(9, .0621, .2901)),
        S(14, "Q2 · C · Grammar", 8, .3924, 8, .93, "japanese-5-5", R(9, .2901, .93), R(10, 0, .0497)),
        S(23, "Q3 · C · Kanji", 12, .0702, 13, .0702, "japanese-5-4", R(11, .0620, .4628)),
        S(23, "Q3 · D · Grammar", 13, .0702, 13, .93, "japanese-5-5", R(11, .4628, .93), R(12, 0, .0661)),
    ],
    (2018, "A", "I"): [
        S(14, "Ceist 2 · B · Kanji", 8, .0702, 8, .3924, "japanese-5-4", R(9, .6135, .93), R(10, 0, .0637)),
        S(14, "Ceist 2 · C · Gramadach", 8, .3924, 8, .93, "japanese-5-5", R(10, .0637, .3962)),
        S(21, "Ceist 3 · C · Kanji", 12, .0702, 13, .0702, "japanese-5-4", R(11, .4287, .93), R(12, 0, .0719)),
        S(21, "Ceist 3 · D · Gramadach", 13, .0702, 13, .93, "japanese-5-5", R(12, .0719, .5049)),
    ],

    # Ordinary — official assessed sections missing from one or both maps.
    (2012, "G", "E"): [
        S(14, "Q3 · B · Kanji", 8, .0341, 8, .4846, "japanese-5-4", R(7, .6074, .93)),
        S(14, "Q3 · C · Grammar", 8, .4846, 9, .0341, "japanese-5-5", R(8, .0601, .4203)),
        S(14, "Q3 · D · Culture and society", 9, .0341, 9, .93, "japanese-5-6", R(8, .4203, .93), R(9, 0, .0601)),
    ],
    (2012, "G", "I"): [
        S(13, "Ceist 3 · B · Kanji", 8, .0341, 8, .4846, "japanese-5-4", R(8, .5842, .93)),
        S(13, "Ceist 3 · C · Gramadach", 8, .4846, 9, .0341, "japanese-5-5", R(9, .0601, .4203)),
        S(13, "Ceist 3 · D · Cultúr agus sochaí", 9, .0341, 9, .93, "japanese-5-6", R(9, .4203, .93), R(10, 0, .0599)),
    ],
    (2013, "G", "E"): [
        S(2, "Q2 · C · Culture and society", 6, .0438, 6, .93, "japanese-5-6", R(7, .0840, .1900)),
        S(3, "Q3 · B · Kanji", 10, .0437, 10, .5256, "japanese-5-4", R(7, .7214, .93), R(8, 0, .3265)),
        S(3, "Q3 · C · Grammar (present tense)", 10, .5256, 11, .0601, "japanese-5-5", R(8, .3265, .5740)),
        S(3, "Q3 · D · Grammar (particles)", 11, .0601, 11, .93, "japanese-5-5", R(8, .5740, .93), R(9, 0, .1045)),
    ],
    (2013, "G", "I"): [
        S(4, "Ceist 2 · C · Cultúr agus sochaí", 6, .0438, 6, .93, "japanese-5-6", R(7, .5453, .93), R(8, 0, .0842)),
    ],
    (2014, "G", "E"): [
        S(9, "Q2 · D · Culture and society", 8, .0505, 8, .93, "japanese-5-6", R(7, .7128, .93), R(8, 0, .0951)),
    ],
    (2014, "G", "I"): [
        S(8, "Ceist 2 · B · Kanji", 6, .0343, 6, .93, "japanese-5-4", R(7, .0759, .3591)),
        S(8, "Ceist 2 · C · Gramadach", 7, .0506, 7, .93, "japanese-5-5", R(7, .3591, .93), R(8, 0, .0923)),
        S(8, "Ceist 2 · D · Cultúr agus sochaí", 8, .0505, 8, .93, "japanese-5-6", R(8, .0923, .2396)),
    ],
    (2015, "G", "E"): [
        S(10, "Q2 · D · Culture and society", 7, .0510, 7, .93, "japanese-5-6", R(7, .3938, .93), R(8, 0, .0660)),
    ],
    (2015, "G", "I"): [
        S(9, "Ceist 2 · C · Kanji", 6, .0511, 6, .93, "japanese-5-4", R(7, .0661, .3774)),
        S(9, "Ceist 2 · D · Cultúr agus sochaí", 7, .0510, 7, .93, "japanese-5-6", R(7, .3774, .93), R(8, 0, .0661)),
        S(12, "Ceist 3 · B1 · Gramadach (foirmeacha)", 10, .0837, 10, .4193, "japanese-5-5", R(9, .0661, .3407)),
        S(12, "Ceist 3 · B2 · Gramadach (páirteagail)", 10, .4193, 10, .93, "japanese-5-5", R(9, .3407, .93)),
    ],
    (2016, "G", "E"): [
        S(10, "Q2 · B · Grammar", 6, .0343, 6, .93, "japanese-5-5", R(7, .0668, .4157)),
        S(10, "Q2 · C · Kanji", 7, .0343, 7, .93, "japanese-5-4", R(7, .4157, .93), R(8, 0, .0670)),
        S(14, "Q3 · B · Culture and society", 10, .0505, 10, .93, "japanese-5-6", R(8, .7478, .93), R(9, 0, .0506)),
    ],
    (2016, "G", "I"): [
        S(10, "Ceist 2 · B · Gramadach", 6, .0343, 6, .93, "japanese-5-5", R(7, .0566, .4055)),
        S(10, "Ceist 2 · C · Kanji", 7, .0343, 7, .93, "japanese-5-4", R(7, .4055, .93), R(8, 0, .0567)),
        S(14, "Ceist 3 · B · Cultúr agus sochaí", 10, .0505, 10, .93, "japanese-5-6", R(8, .7486, .93), R(9, 0, .0567)),
    ],
    (2017, "G", "E"): [
        S(11, "Q2 · D · Culture and society", 7, .0331, 7, .93, "japanese-5-6", R(7, .0763, .2074)),
    ],
    (2018, "G", "E"): [
        S(2, "Q2 · C · Kanji", 6, .0668, 6, .93, "japanese-5-4", R(7, .0679, .4121)),
        S(2, "Q2 · D · Culture and society", 7, .0668, 7, .93, "japanese-5-6", R(7, .4121, .93), R(8, 0, .0679)),
        S(3, "Q3 · C · Grammar", 10, .0668, 10, .93, "japanese-5-5", R(9, .0680, .93), R(10, 0, .0667)),
    ],
    (2018, "G", "I"): [
        S(11, "Ceist 2 · C · Kanji", 6, .0668, 6, .93, "japanese-5-4", R(7, .0656, .4425)),
        S(11, "Ceist 2 · D · Cultúr agus sochaí", 7, .0668, 7, .93, "japanese-5-6", R(7, .4425, .93), R(8, 0, .0656)),
        S(18, "Ceist 3 · C · Gramadach", 10, .0668, 10, .93, "japanese-5-5", R(9, .0656, .93), R(10, 0, .0643)),
    ],
}


def without_print_order(question: dict) -> dict:
    """Return the preserved card payload, excluding additive display metadata."""
    return {key: value for key, value in question.items() if key != "printOrder"}


def digest(questions: list[dict]) -> str:
    payload = json.dumps(
        [without_print_order(question) for question in questions],
        ensure_ascii=False,
        separators=(",", ":"),
    ).encode()
    return hashlib.sha256(payload).hexdigest()


def additions_for(year: int, level_code: str, language_code: str) -> list[dict]:
    key = (year, level_code, language_code)
    base = BASE_COUNTS[key]
    q4, q5 = PAPER_SPECS[(year, level_code)]
    q4_regions, q5_regions = SCHEME_REGIONS[(year, level_code, language_code)]
    if level_code == "A":
        labels = ("Q4 · Short written production", "Q5 · Extended written production")
    else:
        labels = ("Q4 · Cloze written production", "Q5 · Personal written production")
    additions = [
        C(base + 1, labels[0], q4[0], q4[1], q4_regions, q4[2]),
        C(base + 2, labels[1], q5[0], q5[1], q5_regions, q5[2]),
    ]
    for offset, spec in enumerate(SKILL_SPECS.get(key, []), start=base + 3):
        additions.append(C(
            offset,
            spec["label"],
            spec["paper_page"],
            spec["paper_y"],
            spec["regions"],
            spec["end_page"],
            spec["end_y"],
        ))
    return additions


def print_order_ids(key: tuple[int, str, str], additions: list[dict]) -> list[str]:
    """Keep original identities and insert recovered skills in paper order."""
    base_count = BASE_COUNTS[key]
    skill_cards = additions[2:]
    skill_specs = SKILL_SPECS.get(key, [])
    if len(skill_cards) != len(skill_specs):
        raise ValueError(f"{key}: skill specification/card count mismatch")

    inserted: dict[int, list[str]] = {}
    for spec, card in zip(skill_specs, skill_cards):
        after = spec["after"]
        if not 1 <= after <= base_count:
            raise ValueError(f"{key}: skill insertion point {after} is outside original IDs")
        inserted.setdefault(after, []).append(card["n"])

    ordered: list[str] = []
    for number in range(1, base_count + 1):
        ordered.append(str(number))
        ordered.extend(inserted.get(number, []))
    ordered.extend(question["n"] for question in additions[:2])
    return ordered


def validate_sources(sidecar: dict, additions: list[dict], year: int, key: tuple[int, str, str]) -> None:
    paper_path = CORPUS / "exampapers" / str(year) / sidecar["paperFileid"]
    scheme_path = CORPUS / "markingschemes" / str(year) / sidecar["schemeFileid"]
    with fitz.open(paper_path) as paper, fitz.open(scheme_path) as scheme:
        for question in additions:
            if not 1 <= question["pP"] <= question["endP"] <= len(paper):
                raise ValueError(f"{key}: paper crop outside official source")
            if not 0 <= question["pY"][0] < 1 or not 0 < question["endY"] <= 1:
                raise ValueError(f"{key}: invalid paper crop ordinate")
            if (
                question["pP"] == question["endP"]
                and question["endY"] <= question["pY"][0]
            ):
                raise ValueError(f"{key}: paper crop ends before it starts")
            if question["endP"] - question["pP"] > 3:
                raise ValueError(f"{key}: paper crop exceeds the viewer's four-page bound")
            page_text = paper[question["pP"] - 1].get_text().strip()
            if not page_text:
                raise ValueError(f"{key}: paper anchor page has no extractable text")
            last_scheme_page = 0
            for region in question["region"]:
                if not 1 <= region["p"] <= len(scheme):
                    raise ValueError(f"{key}: scheme crop outside official source")
                if region["p"] < last_scheme_page:
                    raise ValueError(f"{key}: scheme regions are not in page order")
                last_scheme_page = region["p"]
                if not 0 <= region["r"][1] < region["r"][3] <= 1:
                    raise ValueError(f"{key}: invalid scheme crop")

        # Historic original anchors contain known collapsed searches, so they
        # are not used as a global ordering oracle.  Each audited insertion
        # group and the recovered Q4/Q5 pair must still be internally ordered.
        groups: dict[int, list[dict]] = {}
        for spec, card in zip(SKILL_SPECS.get(key, []), additions[2:]):
            groups.setdefault(spec["after"], []).append(card)
        for after, cards in groups.items():
            anchors = [(card["pP"], card["pY"][0]) for card in cards]
            if anchors != sorted(anchors) or len(anchors) != len(set(anchors)):
                raise ValueError(f"{key}: skills after original {after} are not in paper order")
        q4_q5_anchors = [(card["pP"], card["pY"][0]) for card in additions[:2]]
        if q4_q5_anchors != sorted(q4_q5_anchors) or len(set(q4_q5_anchors)) != 2:
            raise ValueError(f"{key}: recovered Q4/Q5 are not in paper order")


def repair(year: int, level_code: str, language_code: str) -> Path:
    key = (year, level_code, language_code)
    fileid = f"LC058{level_code}LP000{language_code}V.pdf"
    source = SOURCE_ROOT / str(year) / f"{fileid}.json"
    sidecar = json.loads(source.read_text())
    if sidecar["paperFileid"] != fileid or sidecar["schemeFileid"] != fileid:
        raise ValueError(f"{key}: unexpected source document IDs")

    base_count = BASE_COUNTS[key]
    base = copy.deepcopy(sidecar["q"][:base_count])
    if [int(q["n"]) for q in base] != list(range(1, base_count + 1)):
        raise ValueError(f"{key}: original stable ID range is incomplete")
    if digest(base) != BASE_HASHES[key]:
        raise ValueError(f"{key}: an original question changed; refusing additive repair")

    additions = additions_for(year, level_code, language_code)
    current_tail = sidecar["q"][base_count:]
    if len(current_tail) > len(additions) or [
        without_print_order(question) for question in current_tail
    ] != [
        without_print_order(question) for question in additions[:len(current_tail)]
    ]:
        raise ValueError(f"{key}: unexpected post-baseline cards; refusing to overwrite")
    validate_sources(sidecar, additions, year, key)

    sidecar["q"] = base + additions
    expected_ids = [str(number) for number in range(1, base_count + len(additions) + 1)]
    if [q["n"] for q in sidecar["q"]] != expected_ids:
        raise ValueError(f"{key}: repaired stable IDs are not contiguous")

    ordered_ids = print_order_ids(key, additions)
    if len(ordered_ids) != len(sidecar["q"]) or len(set(ordered_ids)) != len(ordered_ids):
        raise ValueError(f"{key}: print order is not a complete stable-ID permutation")
    rank_for_id = {stable_id: rank for rank, stable_id in enumerate(ordered_ids, start=1)}
    for question in sidecar["q"]:
        question["printOrder"] = rank_for_id[question["n"]]

    out = OUT_ROOT / str(year) / f"{fileid}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(sidecar, ensure_ascii=False, indent=2) + "\n")
    return out


def main() -> None:
    written = []
    total_additions = 0
    total_skills = 0
    for year in range(2012, 2019):
        for level_code in ("A", "G"):
            for language_code in ("E", "I"):
                key = (year, level_code, language_code)
                out = repair(year, level_code, language_code)
                written.append(out)
                skill_count = len(SKILL_SPECS.get(key, []))
                addition_count = 2 + skill_count
                total_additions += addition_count
                total_skills += skill_count
                shown = out.relative_to(REPO) if out.is_relative_to(REPO) else out
                print(f"wrote {shown} (+{addition_count} cards)")
    if total_skills != 75:
        raise ValueError(f"expected 75 audited skill cards, got {total_skills}")
    print(
        "Japanese 2012-2018 written additions: "
        f"{total_additions} cards (56 Q4/Q5 + {total_skills} granular skills)"
    )


if __name__ == "__main__":
    main()
