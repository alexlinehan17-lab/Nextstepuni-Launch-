#!/usr/bin/env python3
"""Restore the missing 2012 Ordinary Agricultural Science answer cards.

The SEC archive contains both language editions of the paper and marking
scheme, but the generic anchor mapper cannot reconcile the schemes' written
number words (``Question One`` / ``Ceist a hAon``) with the papers' numeric
headers.  This additive generator creates Q1-Q13 only when the sidecar is
absent.  It never replaces an existing Mark Bank sidecar.

Usage:
  python3 scripts/paper-trail/agricultural_science_missing.py
  python3 scripts/paper-trail/agricultural_science_missing.py --check
"""

from __future__ import annotations

import argparse
import json
import os
import re
from collections import defaultdict

import fitz


HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
CORPUS = os.path.join(REPO, "paper-trail-corpus")
ANSWERS = os.path.join(HERE, "answers", "2012")
COPYRIGHT = "© State Examinations Commission"

ENGLISH_NUMBERS = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10,
    "eleven": 11,
    "twelve": 12,
    "thirteen": 13,
}

IRISH_NUMBERS = {
    "a haon": 1,
    "a dó": 2,
    "a trí": 3,
    "a ceathair": 4,
    "a cúig": 5,
    "a sé": 6,
    "a seacht": 7,
    "a hocht": 8,
    "a naoi": 9,
    "a deich": 10,
    "a haon déag": 11,
    "a dó dhéag": 12,
    "a trí déag": 13,
}


def lines_of(page: fitz.Page):
    grouped = defaultdict(list)
    for word in page.get_text("words"):
        grouped[(word[5], word[6])].append(word)
    height = page.rect.height
    lines = []
    for words in grouped.values():
        words.sort(key=lambda word: word[0])
        lines.append((" ".join(word[4] for word in words), words[0][1] / height))
    return sorted(lines, key=lambda line: line[1])


def clean_number_words(value: str) -> str:
    return re.sub(r"\s+", " ", value.casefold().strip().rstrip(". :"))


def paper_markers(document: fitz.Document, lang: str):
    word = "Question" if lang == "EV" else "Ceist"
    pattern = re.compile(rf"^{word}\s+(\d+)\.\s*$", re.I)
    found = {}
    for page_index in range(1, len(document)):
        for text, y in lines_of(document[page_index]):
            match = pattern.match(text)
            if match:
                number = int(match.group(1))
                if 1 <= number <= 13:
                    found.setdefault(number, (page_index, y))
    return found


def scheme_markers(document: fitz.Document, lang: str):
    if lang == "EV":
        pattern = re.compile(r"^Question\s+([A-Za-z]+)\b", re.I)
        number_words = ENGLISH_NUMBERS
    else:
        pattern = re.compile(r"^Ceist\s+(.+?)(?:\.|$)", re.I)
        number_words = IRISH_NUMBERS

    found = {}
    for page_index in range(2, len(document)):
        for text, y in lines_of(document[page_index]):
            match = pattern.match(text)
            if not match:
                continue
            words = clean_number_words(match.group(1))
            number = number_words.get(words)
            if number is not None:
                found.setdefault(number, (page_index, y))
    return found


def last_content_page(document: fitz.Document, start: int) -> int:
    answer_pages = [
        index for index in range(start, len(document))
        if len(" ".join(document[index].get_text("text").split())) > 80
    ]
    return answer_pages[-1] if answer_pages else start


def region_between(start, end):
    start_page, start_y = start
    end_page, end_y = end
    if start_page == end_page:
        return [{"p": start_page + 1, "r": [0.0, round(start_y, 4), 1.0, round(end_y, 4)]}]

    regions = [{"p": start_page + 1, "r": [0.0, round(start_y, 4), 1.0, 1.0]}]
    for page_index in range(start_page + 1, end_page):
        regions.append({"p": page_index + 1, "r": [0.0, 0.0, 1.0, 1.0]})
    if end_y > 0.02:
        regions.append({"p": end_page + 1, "r": [0.0, 0.0, 1.0, round(end_y, 4)]})
    return regions


def build(lang: str):
    fileid = f"LC024GLP000{lang}.pdf"
    paper_path = os.path.join(CORPUS, "exampapers", "2012", fileid)
    scheme_path = os.path.join(CORPUS, "markingschemes", "2012", fileid)
    paper = fitz.open(paper_path)
    scheme = fitz.open(scheme_path)
    paper_points = paper_markers(paper, lang)
    scheme_points = scheme_markers(scheme, lang)

    expected = set(range(1, 14))
    if set(paper_points) != expected:
        raise RuntimeError(f"{fileid}: paper markers {sorted(paper_points)}")
    if set(scheme_points) != expected:
        raise RuntimeError(f"{fileid}: scheme markers {sorted(scheme_points)}")

    final_scheme_page = last_content_page(scheme, scheme_points[13][0])
    questions = []
    for number in range(1, 14):
        paper_page, paper_y = paper_points[number]
        if number < 13:
            next_paper_page, next_paper_y = paper_points[number + 1]
            paper_end = next_paper_y if next_paper_page == paper_page else 1.0
            scheme_end = scheme_points[number + 1]
        else:
            paper_end = 1.0
            scheme_end = (final_scheme_page + 1, 0.0)
        questions.append({
            "conf": 1.0,
            "label": f"Question {number}",
            "mode": "crop",
            "n": str(number),
            "pP": paper_page + 1,
            "pY": [round(paper_y, 4), round(paper_end, 4)],
            "region": region_between(scheme_points[number], scheme_end),
        })

    return {
        "band": [1, len(scheme) + 1],
        "component": "",
        "copyright": COPYRIGHT,
        "paperFileid": fileid,
        "q": questions,
        "schemeFileid": fileid,
        "v": 1,
    }


def canonical(value) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    os.makedirs(ANSWERS, exist_ok=True)
    for lang in ("EV", "IV"):
        sidecar = build(lang)
        path = os.path.join(ANSWERS, f"{sidecar['paperFileid']}.json")
        expected = canonical(sidecar)
        if args.check:
            if not os.path.exists(path) or canonical(json.load(open(path, encoding="utf-8"))) != expected:
                raise SystemExit(f"STALE {path}")
            print(f"OK {os.path.basename(path)}: 13 cards")
            continue
        if os.path.exists(path):
            existing = canonical(json.load(open(path, encoding="utf-8")))
            if existing != expected:
                raise SystemExit(f"REFUSE overwrite of existing sidecar: {path}")
            print(f"UNCHANGED {os.path.basename(path)}")
            continue
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(expected + "\n")
        print(f"ADDED {os.path.basename(path)}: 13 cards")


if __name__ == "__main__":
    main()
