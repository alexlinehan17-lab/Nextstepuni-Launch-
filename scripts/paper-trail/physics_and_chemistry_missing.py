#!/usr/bin/env python3
"""Add the one missing 2015 Higher Physics & Chemistry English card.

The committed English sidecar stops at Q11 even though the official paper,
scheme, Irish sidecar and topic evidence all contain Q12. This additive repair
keeps every existing card byte-for-byte equivalent and appends only Q12.
"""

from __future__ import annotations

import argparse
import json
import os
import re

import fitz


HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
FILEID = "LC023ALP000EV.pdf"
SIDECAR = os.path.join(HERE, "answers", "2015", f"{FILEID}.json")
PAPER = os.path.join(REPO, "paper-trail-corpus", "exampapers", "2015", FILEID)
SCHEME = os.path.join(REPO, "paper-trail-corpus", "markingschemes", "2015", FILEID)


def first_line(document: fitz.Document, pattern: re.Pattern, start_page: int):
    for page_index in range(start_page, len(document)):
        page = document[page_index]
        height = page.rect.height
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            for line in block.get("lines", []):
                text = " ".join(
                    span["text"].strip() for span in line.get("spans", []) if span["text"].strip()
                )
                if pattern.match(text):
                    return page_index, line["bbox"][1] / height
    raise RuntimeError(f"Marker not found: {pattern.pattern}")


def expected_card():
    paper = fitz.open(PAPER)
    scheme = fitz.open(SCHEME)
    paper_page, paper_y = first_line(paper, re.compile(r"^12\.$"), 8)
    scheme_page, scheme_y = first_line(scheme, re.compile(r"^Question 12\b"), 24)
    if paper_page != 9 or scheme_page != 27:
        raise RuntimeError(
            f"Unexpected official Q12 anchors: paper={paper_page + 1}, scheme={scheme_page + 1}"
        )
    return {
        "conf": 1.0,
        "mode": "crop",
        "n": "12",
        "pP": paper_page + 1,
        "pY": [round(paper_y, 4), 1.0],
        "region": [
            {"p": scheme_page + 1, "r": [0.0, round(scheme_y, 4), 1.0, 1.0]},
            {"p": scheme_page + 2, "r": [0.0, 0.0, 1.0, 1.0]},
            {"p": scheme_page + 3, "r": [0.0, 0.0, 1.0, 1.0]},
        ],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    sidecar = json.load(open(SIDECAR, encoding="utf-8"))
    card = expected_card()
    matches = [question for question in sidecar["q"] if question["n"] == "12"]

    if args.check:
        if matches != [card]:
            raise SystemExit(f"STALE {SIDECAR} Q12")
        if len(sidecar["q"]) != 12:
            raise SystemExit(f"Unexpected card count in {SIDECAR}: {len(sidecar['q'])}")
        print(f"OK {os.path.basename(SIDECAR)}: Q12 restored")
        return

    if matches:
        if matches != [card]:
            raise SystemExit(f"REFUSE overwrite of existing Q12 in {SIDECAR}")
        print(f"UNCHANGED {os.path.basename(SIDECAR)}")
        return
    sidecar["q"].append(card)
    with open(SIDECAR, "w", encoding="utf-8") as handle:
        json.dump(sidecar, handle, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        handle.write("\n")
    print(f"ADDED {os.path.basename(SIDECAR)} Q12")


if __name__ == "__main__":
    main()
