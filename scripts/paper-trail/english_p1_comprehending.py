#!/usr/bin/env python3
# Copyright 2026 Nextstepuni
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
"""Append answer-anchored English Paper 1 COMPREHENDING cards.

The established English Paper 1 sidecars contain Section II's numbered
composition choices. Section I reuses those numbers for its three reading
texts, so its recovered tasks receive the next unused stable numeric ids and
descriptive labels. ``printOrder`` records that they appear before the
already-shipped composition cards; no existing ``n`` identity is changed.

Every candidate card must reconcile on both the paper and marking scheme and
pass a question-text overlap check. A paper is all-or-nothing: no partial
sidecar is written.

Usage:
  python3 english_p1_comprehending.py --dry-run
  python3 english_p1_comprehending.py
"""
import argparse
import glob
import json
import os
import re

import fitz

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
CORPUS = os.path.join(REPO, "paper-trail-corpus")
ANSWERS = os.path.join(HERE, "answers")

TEXT_RE = re.compile(r"^TEXT\s+([123])\b", re.I)
QUESTION_RE = re.compile(r"^QUESTION\s+([AB])\b", re.I)
TEXT_QUESTION_RE = re.compile(r"^TEXT\s+([123])\s+QUESTION\s+([AB])\b", re.I)
COMPOSING_RE = re.compile(r"SECTION\s+(?:II|2)\b.*COMPOS", re.I)
PAPER_TWO_RE = re.compile(r"^PAPER\s+(?:2|TWO)\b", re.I)
WORD_RE = re.compile(r"[a-záéíóúà-ÿ’']{4,}", re.I)
STOPWORDS = frozenset(
    "the and that this with your you for from are can our their his her its "
    "have has been each one two three text question answer responses response "
    "support reference marks candidates should expect allow points point".split()
)


def lines(page):
    """[(text, y-fraction)] in visual reading order."""
    grouped = {}
    for word in page.get_text("words"):
        grouped.setdefault((word[5], word[6]), []).append(word)
    out = []
    height = page.rect.height
    for words in grouped.values():
        words.sort(key=lambda word: word[0])
        out.append((" ".join(word[4] for word in words).strip(),
                    min(word[1] for word in words) / height))
    out.sort(key=lambda row: row[1])
    return out


def task_markers(doc, stop_re):
    """Return one ordered marker for each Text 1–3, Question A/B."""
    found = {}
    current_text = None
    start_page = next((
        page_index for page_index in range(1, len(doc))
        if any("COMPREHENDING" in text.upper() and "100" in text
               for text, _ in lines(doc[page_index]))
    ), None)
    if start_page is None:
        start_page = next((
            page_index for page_index in range(1, len(doc))
            if any(re.match(r"^PAPER\s+(?:1|ONE)\b", text.strip(), re.I)
                   for text, _ in lines(doc[page_index]))
        ), 1)
    for page_index in range(start_page, len(doc)):
        page = doc[page_index]
        page_lines = lines(page)
        if found and any(stop_re.match(text.strip()) for text, _ in page_lines):
            break
        for text, y in page_lines:
            clean = " ".join(text.split())
            combined_match = TEXT_QUESTION_RE.match(clean)
            if combined_match:
                current_text = int(combined_match.group(1))
                key = (current_text, combined_match.group(2).upper())
                found.setdefault(key, (page_index, round(y, 4)))
                continue
            text_match = TEXT_RE.match(clean)
            if text_match:
                current_text = int(text_match.group(1))
            question_match = QUESTION_RE.match(clean)
            # Older schemes begin directly with "Question A" and do not
            # repeat their first paper's "TEXT 1" heading.
            if question_match and current_text is None and not found:
                current_text = 1
            if question_match and current_text:
                key = (current_text, question_match.group(1).upper())
                found.setdefault(key, (page_index, round(y, 4)))
    wanted = [(number, letter) for number in range(1, 4) for letter in ("A", "B")]
    if any(key not in found for key in wanted):
        missing = [key for key in wanted if key not in found]
        return None, f"missing task markers {missing}"
    ordered = [(*key, *found[key]) for key in wanted]
    points = [(row[2], row[3]) for row in ordered]
    if any(right <= left for left, right in zip(points, points[1:])):
        return None, "task markers are not strictly monotonic"
    return ordered, None


def clip_text(doc, segments):
    chunks = []
    for segment in segments:
        page = doc[segment["p"] - 1]
        x0, y0, x1, y1 = segment["r"]
        chunks.append(page.get_text(
            "text",
            clip=fitz.Rect(x0 * page.rect.width, y0 * page.rect.height,
                           x1 * page.rect.width, y1 * page.rect.height),
        ))
    return "\n".join(chunks)


def region_between(doc, start, end):
    start_page, start_y = start
    end_page, end_y = end
    region = [{"p": start_page + 1, "r": [0.0, start_y, 1.0,
                                             end_y if start_page == end_page else 1.0]}]
    for page_index in range(start_page + 1, end_page):
        if doc[page_index].get_text("text").strip():
            region.append({"p": page_index + 1, "r": [0.0, 0.0, 1.0, 1.0]})
    if end_page > start_page and end_y > 0.02:
        region.append({"p": end_page + 1, "r": [0.0, 0.0, 1.0, end_y]})
    return region


def tokens(text):
    return {word.lower() for word in WORD_RE.findall(text)
            if word.lower() not in STOPWORDS}


def build_cards(paper_path, scheme_path):
    paper = fitz.open(paper_path)
    scheme = fitz.open(scheme_path)
    try:
        paper_markers, error = task_markers(paper, COMPOSING_RE)
        if error:
            return None, f"paper: {error}", []
        scheme_markers, error = task_markers(scheme, PAPER_TWO_RE)
        if error:
            return None, f"scheme: {error}", []

        paper_points = [(row[2], row[3]) for row in paper_markers]
        scheme_points = [(row[2], row[3]) for row in scheme_markers]
        # Stop the last B response at Section II/Paper 2, never at EOF.
        paper_last_page = paper_points[-1][0]
        scheme_last_page = scheme_points[-1][0]
        paper_stop = next(
            ((pi, y) for pi, page in enumerate(paper) for text, y in lines(page)
             if pi >= paper_last_page and COMPOSING_RE.match(text.strip())),
            (len(paper) - 1, 1.0),
        )
        scheme_stop = next(
            ((pi, y) for pi, page in enumerate(scheme) for text, y in lines(page)
             if pi >= scheme_last_page and PAPER_TWO_RE.match(text.strip())),
            (len(scheme) - 1, 1.0),
        )
        cards = []
        qa = []
        for index, (number, letter, page_index, y) in enumerate(paper_markers):
            paper_end = paper_points[index + 1] if index + 1 < len(paper_points) else paper_stop
            if paper_end[0] != page_index:
                paper_end = (page_index, 1.0)
            scheme_page, scheme_y = scheme_points[index]
            scheme_end = scheme_points[index + 1] if index + 1 < len(scheme_points) else scheme_stop
            paper_region = region_between(paper, (page_index, y), paper_end)
            scheme_region = region_between(scheme, (scheme_page, scheme_y), scheme_end)
            paper_words = tokens(clip_text(paper, paper_region))
            scheme_words = tokens(clip_text(scheme, scheme_region))
            overlap = len(paper_words & scheme_words) / max(1, len(paper_words))
            card_id = str(8 + index)
            qa.append((card_id, overlap, len(paper_words)))
            if overlap < 0.42 or len(paper_words) < 8:
                return None, f"Text {number} Question {letter}: content overlap {overlap:.2f}", qa
            p_end_page, p_end_y = paper_end
            cards.append({
                "n": card_id,
                "label": f"Comprehending · Text {number} · Question {letter}",
                "printOrder": index + 1,
                "pP": page_index + 1,
                "pY": [y, p_end_y if p_end_page == page_index else 1.0],
                "region": scheme_region,
                "mode": "crop",
                "conf": 1.0,
            })
        return cards, None, qa
    finally:
        paper.close()
        scheme.close()


def scheme_for(year, level_code):
    candidates = sorted(glob.glob(os.path.join(
        CORPUS, "markingschemes", str(year), f"LC002{level_code}LP*EV.pdf")))
    preferred = [path for path in candidates if "LP000" in os.path.basename(path)]
    return (preferred or candidates or [None])[0]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    mapped = dropped = unchanged = 0
    for year in range(2010, 2027):
        for level_code in ("A", "G"):
            paper_file = f"LC002{level_code}LP100EV.pdf"
            paper_path = os.path.join(CORPUS, "exampapers", str(year), paper_file)
            sidecar_path = os.path.join(ANSWERS, str(year), f"{paper_file}.json")
            scheme_path = scheme_for(year, level_code)
            if not (os.path.exists(paper_path) and scheme_path):
                continue
            if os.path.exists(sidecar_path):
                sidecar = json.load(open(sidecar_path, encoding="utf-8"))
            else:
                from english_p1 import build as build_composing
                sidecar, base_error = build_composing(paper_path, scheme_path)
                if base_error:
                    tag = f"{year} {'HL' if level_code == 'A' else 'OL'}"
                    print(f"DROP {tag}: base composition map: {base_error}")
                    dropped += 1
                    continue
            # Clean up section-qualified ids emitted by the first local draft;
            # they were never part of the shipped contract.
            sidecar["q"] = [question for question in sidecar["q"]
                            if not str(question["n"]).startswith("R")]
            if all(any(question["n"] == str(number) for question in sidecar["q"])
                   for number in range(8, 14)):
                unchanged += 1
                continue
            cards, error, qa = build_cards(paper_path, scheme_path)
            tag = f"{year} {'HL' if level_code == 'A' else 'OL'}"
            if error:
                print(f"DROP {tag}: {error}; QA={qa}")
                dropped += 1
                continue
            print(f"MAP  {tag}: " + ", ".join(f"{card}={score:.2f}" for card, score, _ in qa))
            if not args.dry_run:
                for index, question in enumerate(sidecar["q"]):
                    question["printOrder"] = 7 + index
                existing = {question["n"] for question in sidecar["q"]}
                sidecar["q"].extend(card for card in cards if card["n"] not in existing)
                with open(sidecar_path, "w", encoding="utf-8") as handle:
                    json.dump(sidecar, handle, ensure_ascii=False, sort_keys=True,
                              separators=(",", ":"))
            mapped += 1
    print(f"done: {mapped} mapped, {unchanged} already complete, {dropped} dropped"
          + (" (dry run)" if args.dry_run else ""))


if __name__ == "__main__":
    main()
