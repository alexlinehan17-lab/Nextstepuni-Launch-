#!/usr/bin/env python3
"""Complete English Ordinary Paper 2 cards without changing shipped IDs.

StudyClix shelves Ordinary Paper 2 by the selectable Single Text, Comparative
mode, Unseen Poetry block and Prescribed Poetry option. The former mapper
mistook inline references to ``SECTION I`` for real section headings, so it
dropped every Comparative block and most complete paper variants.

This repair discovers those structural blocks from the official SEC paper,
locates the same question wording in the official marking scheme, and adds
only missing cards. Existing card numbers, paper anchors and scheme regions
remain untouched; corrected audited crops live in ``schemeRegion``. Question
text is never stored.

Usage:
    python3 english_p2_ol.py --check
    python3 english_p2_ol.py
"""

import argparse
import json
import os
import re
import sys

import fitz

from english_p2_complete import (
    Card,
    crop_text,
    header_candidates,
    lines_of,
    norm,
    paper_segments,
    region_segments,
    scheme_region_text,
    tokens,
)

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
CORPUS = os.path.join(REPO, "paper-trail-corpus")
ANSWERS = os.path.join(HERE, "answers")

PAPER_FILEID = "LC002GLP200EV.pdf"
SCHEME_FILEID = "LC002GLP000EV.pdf"
YEARS = list(range(2010, 2026))
COPYRIGHT = "© State Examinations Commission"


def point_in_range(point, start, end):
    return point >= start and point < end


def find_marker(doc, phrase, start_page=1):
    """Find an actual structural heading, never an inline cross-reference."""
    phrase = phrase.upper()
    matches = []
    for page_index in range(start_page, len(doc)):
        for line in lines_of(doc[page_index]):
            upper = norm(line.text).upper()
            if phrase not in upper:
                continue
            if phrase in {"THE SINGLE TEXT", "THE COMPARATIVE STUDY"}:
                if line.y > 0.16 or len(upper) > 75:
                    continue
            elif phrase in {"UNSEEN POEM", "PRESCRIBED POETRY"}:
                if not re.search(rf"\b{re.escape(phrase)}\s*\(", upper):
                    continue
            matches.append((page_index, line.y))
    return min(matches) if matches else None


def range_headers(doc, start, end, letters):
    candidates = []
    for page_index in range(start[0], min(end[0], len(doc) - 1) + 1):
        for letter, title, y in header_candidates(doc[page_index], letters):
            if point_in_range((page_index, y), start, end):
                candidates.append((letter, title, page_index, y))
    candidates.sort(key=lambda row: (row[2], row[3], row[0]))

    # A real option series is A, B, C... in physical order. Greedy sequence
    # selection discards uppercase prose artefacts without relying on titles.
    selected = []
    expected = ord("A")
    for candidate in candidates:
        if candidate[0] == chr(expected):
            selected.append(candidate)
            expected += 1
    return selected


def first_numbered_point(doc, start, end, require_part_a=False):
    for page_index in range(start[0], end[0] + 1):
        for line in lines_of(doc[page_index]):
            point = (page_index, line.y)
            if not point_in_range(point, start, end):
                continue
            if line.x < 115 and re.match(r"^1\.(?:\s|$)", line.text):
                if require_part_a:
                    same_row = [
                        candidate for candidate in lines_of(doc[page_index])
                        if abs(candidate.y - line.y) < 0.006
                    ]
                    if not any(re.match(r"^\(a\)", candidate.text, re.I)
                               for candidate in same_row):
                        continue
                return point
    return start


def cards_from_headers(doc, kind, label_prefix, headers, final_end):
    cards = []
    for index, (letter, title, page_index, y) in enumerate(headers):
        end = (headers[index + 1][2], headers[index + 1][3]) \
            if index + 1 < len(headers) else final_end
        card = Card(
            kind,
            f"{label_prefix} {letter} · {title}",
            page_index,
            y,
            p_end_page=end[0],
            p_end_y=end[1],
        )
        card.match_point = first_numbered_point(
            doc, (page_index, y), end, require_part_a=kind == "prescribed")
        cards.append(card)
    return cards


def collect_cards(paper, year):
    single_start = find_marker(paper, "THE SINGLE TEXT")
    comparative_start = find_marker(paper, "THE COMPARATIVE STUDY")
    unseen_start = find_marker(paper, "UNSEEN POEM")
    prescribed_start = find_marker(paper, "PRESCRIBED POETRY")
    if not single_start or not comparative_start:
        raise ValueError("Single Text or Comparative structural heading missing")

    single_headers = range_headers(paper, single_start, comparative_start, "ABCDEFGHI")
    if len(single_headers) not in {8, 9}:
        raise ValueError(f"Single Text headings not reconciled: {[row[0] for row in single_headers]}")

    # One 2011 PDF has damaged text coordinates for the whole poetry page. Its
    # physical section still follows the stable SEC page order.
    if not unseen_start:
        unseen_start = (comparative_start[0] + 2, 0.0)
    if not prescribed_start:
        prescribed_start = (unseen_start[0] + 1, 0.0)

    comparative_headers = range_headers(paper, comparative_start, unseen_start, "ABC")
    if len(comparative_headers) not in {2, 3}:
        raise ValueError(
            f"Comparative headings not reconciled: {[row[0] for row in comparative_headers]}")

    poetry_headers = range_headers(
        paper, prescribed_start, (len(paper), 0.0), "ABCDEF")
    if year == 2011:
        poetry_headers = [
            ("A", "Lines 17-52 From A Christmas Childhood", 10, 0.0897),
            ("B", "All Day Long", 12, 0.0275),
            ("C", "The Net", 14, 0.0250),
            ("D", "Spring", 15, 0.0250),
        ]
    if len(poetry_headers) not in {4, 6}:
        raise ValueError(
            f"Prescribed Poetry headings not reconciled: {[row[0] for row in poetry_headers]}")

    cards = []
    cards.extend(cards_from_headers(
        paper, "single", "Single Text", single_headers, comparative_start))
    cards.extend(cards_from_headers(
        paper, "comparative", "Comparative", comparative_headers, unseen_start))

    unseen = Card(
        "unseen",
        "Unseen Poetry",
        unseen_start[0],
        unseen_start[1],
        p_end_page=prescribed_start[0],
        p_end_y=prescribed_start[1],
    )
    unseen.match_point = first_numbered_point(paper, unseen_start, prescribed_start)
    unseen.min_region_overlap = 0.15 if year == 2011 else 0.33
    cards.append(unseen)

    last_poetry_end = (poetry_headers[-1][2], 1.0)
    prescribed_cards = cards_from_headers(
        paper, "prescribed", "Poetry", poetry_headers, last_poetry_end)
    if year == 2011:
        for card in prescribed_cards:
            card.min_region_overlap = 0.20
    cards.extend(prescribed_cards)
    return cards


def page_line_score(anchor_tokens, page_lines, start_index):
    window = " ".join(line.text for line in page_lines[start_index:start_index + 8])
    return len(anchor_tokens & tokens(window)) / max(1, len(anchor_tokens))


def meaningful_label_tokens(card):
    return tokens(card.label) - {
        "single", "comparative", "poetry", "unseen", "prescribed", "option",
    }


def scheme_section_page(scheme, section, phrase):
    for page_index, page in enumerate(scheme):
        upper = norm(page.get_text()).upper()
        if phrase in upper and section in upper:
            return page_index
    raise ValueError(f"scheme section not found: {section} {phrase}")


def locate_scheme_cards(cards, paper, scheme, year):
    scheme_page_tokens = [tokens(page.get_text()) for page in scheme]
    comparative_page = scheme_section_page(scheme, "SECTION II", "COMPARATIVE STUDY")
    unseen_marker = find_marker(scheme, "UNSEEN POEM")
    prescribed_marker = find_marker(scheme, "PRESCRIBED POETRY")
    if not unseen_marker or not prescribed_marker:
        raise ValueError("scheme poetry structural headings missing")
    page_ranges = {
        "single": (0, comparative_page),
        "comparative": (comparative_page, unseen_marker[0] + 1),
        "unseen": (unseen_marker[0], prescribed_marker[0] + 1),
        "prescribed": (prescribed_marker[0], len(scheme)),
    }
    prior = (0, 0.0)
    manual_points = {
        2011: {
            "Poetry A": (29, 0.5111),
            "Poetry B": (31, 0.0277),
            "Poetry C": (32, 0.5501),
            "Poetry D": (34, 0.0416),
        },
        2023: {
            "Poetry A": (49, 0.5204),
            "Poetry B": (51, 0.5771),
            "Poetry C": (53, 0.6839),
        },
    }.get(year, {})
    prescribed_cards = [card for card in cards if card.kind == "prescribed"]
    structural_poetry = range_headers(
        scheme, prescribed_marker, (len(scheme), 0.0), "ABCDEF")
    if len(structural_poetry) == len(prescribed_cards):
        manual_points = {
            **manual_points,
            **{
                f"Poetry {letter}": (page_index, y)
                for letter, _, page_index, y in structural_poetry
            },
        }
    for card in cards:
        match_page, match_y = card.match_point
        card.prompt = crop_text(
            paper, match_page, match_y, card.p_end_page, card.p_end_y)
        prompt_tokens = tokens(card.prompt)
        paper_lines = lines_of(paper[match_page])
        anchor_text = " ".join(
            line.text for line in paper_lines if line.y >= match_y - 0.002
        )[:900]
        anchor_tokens = tokens(anchor_text) | tokens(card.label)
        if len(prompt_tokens) < 5 or len(anchor_tokens) < 3:
            raise ValueError(f"{card.label}: insufficient paper matching evidence")

        manual = next((point for prefix, point in manual_points.items()
                       if card.label.startswith(prefix)), None)
        if manual:
            card.s_page, card.s_y = manual
            card.score = len(prompt_tokens & scheme_page_tokens[card.s_page]) / len(prompt_tokens)
            prior = manual
            continue

        candidates = []
        meaningful = meaningful_label_tokens(card)
        first_page, stop_page = page_ranges[card.kind]
        for page_index, page_tokens in enumerate(scheme_page_tokens):
            if not first_page <= page_index < stop_page:
                continue
            if (page_index, 1.0) <= prior:
                continue
            prompt_score = len(prompt_tokens & page_tokens) / len(prompt_tokens)
            anchor_score = len(anchor_tokens & page_tokens) / len(anchor_tokens)
            label_tokens = tokens(card.label)
            label_score = len(label_tokens & page_tokens) / max(1, len(label_tokens))
            combined = prompt_score + 2.2 * anchor_score + 0.8 * label_score
            meaningful_score = len(meaningful & page_tokens) / max(1, len(meaningful))
            candidates.append((
                combined, prompt_score, anchor_score, label_score,
                meaningful_score, page_index,
            ))
        if not candidates:
            raise ValueError(f"{card.label}: no later scheme page")
        if card.kind == "unseen":
            forced = [row for row in candidates if row[5] == unseen_marker[0]]
            if not forced:
                raise ValueError(f"{card.label}: scheme Unseen Poetry page unavailable")
            _, prompt_score, anchor_score, _, _, best_page = max(forced)
            min_prompt, min_anchor = 0.08, 0.03
        elif meaningful and card.kind != "comparative":
            max_meaningful = max(row[4] for row in candidates)
            titled = [
                row for row in candidates
                if row[4] >= max(0.60, max_meaningful - 0.01)
                and row[1] >= 0.08
            ]
        else:
            titled = []
        if titled:
            selected = min(titled, key=lambda row: row[5]) \
                if card.kind == "single" else max(titled)
            _, prompt_score, anchor_score, _, _, best_page = selected
            min_prompt, min_anchor = 0.08, 0.03
        else:
            _, prompt_score, anchor_score, _, _, best_page = max(candidates)
            min_prompt = 0.10 if card.kind == "unseen" else 0.12
            min_anchor = 0.10 if card.kind == "unseen" else 0.25
        if prompt_score < min_prompt or anchor_score < min_anchor:
            raise ValueError(
                f"{card.label}: weak scheme evidence prompt={prompt_score:.2f}, "
                f"anchor={anchor_score:.2f}")

        scheme_lines = lines_of(scheme[best_page])
        line_scores = [page_line_score(anchor_tokens, scheme_lines, index)
                       for index in range(len(scheme_lines))]
        if not line_scores:
            raise ValueError(f"{card.label}: scheme page contains no text lines")
        title_indexes = []
        if meaningful and card.kind != "comparative":
            title_indexes = [
                index for index, line in enumerate(scheme_lines)
                if len(meaningful & tokens(line.text)) / len(meaningful) >= 0.60
                and (best_page, line.y) > prior
            ]
        if card.kind == "unseen":
            best_y = unseen_marker[1]
            eligible = []
        elif title_indexes:
            eligible = title_indexes
        else:
            best_line_score = max(line_scores)
            eligible = [
                index for index, score in enumerate(line_scores)
                if score >= max(0.18, best_line_score * 0.72)
                and (best_page, scheme_lines[index].y) > prior
            ]
        if card.kind != "unseen" and not eligible:
            raise ValueError(f"{card.label}: no monotonic scheme line after {prior}")
        if card.kind != "unseen":
            best_y = max(0.0, scheme_lines[min(eligible)].y - 0.004)

        card.s_page = best_page
        card.s_y = best_y
        card.score = prompt_score
        prior = (best_page, best_y)


def require_region_overlap(card, scheme, region):
    prompt_tokens = tokens(card.prompt)
    overlap = len(prompt_tokens & tokens(scheme_region_text(scheme, region))) \
        / max(1, len(prompt_tokens))
    minimum = getattr(card, "min_region_overlap", 0.33)
    if overlap < minimum:
        raise ValueError(
            f"{card.label}: scheme-region overlap {overlap:.2f} < {minimum:.2f}")


def match_existing(cards, existing):
    available = set(range(len(cards)))
    matches = {}
    for question in existing:
        candidates = []
        for index in available:
            card = cards[index]
            if card.p_page + 1 != question["pP"]:
                continue
            delta = abs(card.p_y - question["pY"][0])
            if delta < 0.045:
                candidates.append((delta, index))
        if not candidates:
            raise ValueError(
                f"existing Q{question['n']} does not match a discovered block at "
                f"paper p{question['pP']} y{question['pY'][0]}")
        _, index = min(candidates)
        matches[question["n"]] = index
        available.remove(index)
    return matches


def audited_region(cards, index, scheme):
    card = cards[index]
    if index + 1 < len(cards):
        end = (cards[index + 1].s_page, cards[index + 1].s_y)
    else:
        end = (min(card.s_page + 2, len(scheme) - 1), 1.0)
    region = region_segments(scheme, (card.s_page, card.s_y), end)
    if not region:
        raise ValueError(f"{card.label}: empty scheme region")
    require_region_overlap(card, scheme, region)
    return region


def build_year(year):
    paper_path = os.path.join(CORPUS, "exampapers", str(year), PAPER_FILEID)
    scheme_path = os.path.join(CORPUS, "markingschemes", str(year), SCHEME_FILEID)
    sidecar_path = os.path.join(ANSWERS, str(year), f"{PAPER_FILEID}.json")
    if not os.path.exists(paper_path) or not os.path.exists(scheme_path):
        return None, "official paper or scheme missing"

    paper = fitz.open(paper_path)
    scheme = fitz.open(scheme_path)
    cards = collect_cards(paper, year)
    locate_scheme_cards(cards, paper, scheme, year)

    if os.path.exists(sidecar_path):
        with open(sidecar_path, encoding="utf-8") as handle:
            sidecar = json.load(handle)
    else:
        sidecar = {
            "v": 1,
            "paperFileid": PAPER_FILEID,
            "schemeFileid": SCHEME_FILEID,
            "component": "200",
            "copyright": COPYRIGHT,
            "q": [],
        }

    matches = match_existing(cards, sidecar["q"])
    matched_indexes = set(matches.values())
    next_number = max([int(question["n"]) for question in sidecar["q"]] + [0]) + 1
    output = []

    for question in sidecar["q"]:
        index = matches[question["n"]]
        card = cards[index]
        augmented = dict(question)
        augmented["label"] = card.label
        augmented["printOrder"] = index + 1
        augmented.pop("schemeRegion", None)
        region = audited_region(cards, index, scheme)
        if region != question["region"]:
            augmented["schemeRegion"] = region
        if card.p_end_page != card.p_page:
            augmented["paperRegion"] = paper_segments(card)
        output.append(augmented)

    for index, card in enumerate(cards):
        if index in matched_indexes:
            continue
        region = audited_region(cards, index, scheme)
        question = {
            "n": str(next_number),
            "pP": card.p_page + 1,
            "pY": [
                round(card.p_y, 4),
                round(card.p_end_y if card.p_end_page == card.p_page else 1.0, 4),
            ],
            "region": region,
            "mode": "crop",
            "conf": 1.0,
            "label": card.label,
            "printOrder": index + 1,
        }
        if card.p_end_page != card.p_page:
            question["paperRegion"] = paper_segments(card)
        output.append(question)
        next_number += 1

    output.sort(key=lambda question: int(question["n"]))
    if sorted(question["printOrder"] for question in output) != list(range(1, len(cards) + 1)):
        raise ValueError("printOrder is not a complete permutation")
    sidecar["q"] = output
    # The immutable legacy regions for a handful of final poetry options run
    # farther than the newly audited correction crop. The paper band is an
    # envelope, so it must contain both the preserved region and any additive
    # schemeRegion correction rather than stopping at the latter.
    region_pages = [
        segment["p"]
        for question in output
        for key in ("region", "schemeRegion")
        for segment in question.get(key, [])
    ]
    sidecar["band"] = [
        cards[0].s_page + 1,
        max(min(cards[-1].s_page + 3, len(scheme)) + 1, max(region_pages) + 1),
    ]
    return sidecar, {
        "cards": len(cards),
        "preserved": len(matches),
        "added": len(cards) - len(matches),
        "minPageOverlap": min(card.score for card in cards),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="validate without writing")
    parser.add_argument("years", nargs="*", type=int)
    args = parser.parse_args()
    years = args.years or YEARS
    failed = 0
    passed = 0
    for year in years:
        try:
            sidecar, summary = build_year(year)
            if sidecar is None:
                print(f"SKIP {year}: {summary}")
                continue
            if not args.check:
                destination = os.path.join(ANSWERS, str(year), f"{PAPER_FILEID}.json")
                os.makedirs(os.path.dirname(destination), exist_ok=True)
                with open(destination, "w", encoding="utf-8") as handle:
                    json.dump(sidecar, handle, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
            action = "CHECK" if args.check else "WROTE"
            print(
                f"{action} {year}: {summary['cards']} cards; preserved {summary['preserved']}; "
                f"added {summary['added']}; min page overlap {summary['minPageOverlap']:.2f}")
            passed += 1
        except Exception as error:
            failed += 1
            print(f"DROP {year}: {error}")
    print(f"done: {passed} passed; {failed} dropped")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
