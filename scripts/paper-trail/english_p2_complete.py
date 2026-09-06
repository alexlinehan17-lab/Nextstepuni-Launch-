#!/usr/bin/env python3
"""Complete English Higher Paper 2 answer cards without changing shipped IDs.

The original Higher Paper 2 mapper retained only the first Comparative mode's
two choices and Prescribed Poetry options 3 onward.  This additive repair
discovers every independently selectable official task in the same papers:

* both choices for every Single Text;
* questions 1 and 2 for every Comparative mode;
* both Unseen Poetry choices; and
* every Prescribed Poetry choice.

Existing card numbers, paper anchors and scheme regions are preserved.  A
complete ``printOrder`` permutation records the real order on the paper, while
new cards receive numbers after the existing maximum.  Question text is never
stored; only coordinates and short structural labels are written.

The scheme locator is content-gated: each paper task must have one monotonic,
high-overlap match in the Paper 2 portion of the official marking scheme or the
whole year is refused.

Usage:
    python3 english_p2_complete.py --check
    python3 english_p2_complete.py
"""

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass

import fitz

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
CORPUS = os.path.join(REPO, "paper-trail-corpus")
ANSWERS = os.path.join(HERE, "answers")

PAPER_FILEID = "LC002ALP200EV.pdf"
SCHEME_FILEID = "LC002ALP000EV.pdf"
YEARS = list(range(2010, 2027))
MIN_PAGE_OVERLAP = 0.25
MIN_ANCHOR_OVERLAP = 0.45
MIN_REGION_OVERLAP = 0.52
STOPWORDS = frozenset(
    "the and that this with your you for from are can our their his her its have has "
    "been each one two three texts text course answer answers reference support discuss "
    "compare extent which what how why either both least other more than may must in on "
    "of to a an or is it not do does at by as be we statement response developing marks "
    "english higher level paper section question candidates".split()
)


@dataclass(frozen=True)
class Line:
    text: str
    x: float
    y: float
    y1: float


@dataclass
class Card:
    kind: str
    label: str
    p_page: int
    p_y: float
    prompt: str = ""
    p_end_page: int = 0
    p_end_y: float = 1.0
    s_page: int = -1
    s_y: float = 0.0
    score: float = 0.0


def norm(value):
    return " ".join(value.replace("\xa0", " ").split())


def lines_of(page):
    groups = {}
    for word in page.get_text("words"):
        groups.setdefault((word[5], word[6]), []).append(word)
    height = page.rect.height
    out = []
    for words in groups.values():
        words.sort(key=lambda word: word[0])
        out.append(Line(
            norm(" ".join(word[4] for word in words)),
            min(word[0] for word in words),
            min(word[1] for word in words) / height,
            max(word[3] for word in words) / height,
        ))
    return sorted(out, key=lambda line: (line.y, line.x))


def tokens(value):
    words = re.findall(r"[a-záéíóúà-ÿ’']+", norm(value).lower())
    return {word for word in words if len(word) >= 4 and word not in STOPWORDS}


def crop_text(doc, start_page, start_y, end_page, end_y):
    parts = []
    for page_index in range(start_page, end_page + 1):
        page = doc[page_index]
        top = start_y if page_index == start_page else 0.0
        bottom = end_y if page_index == end_page else 1.0
        if bottom <= top:
            continue
        parts.append(page.get_text("text", clip=fitz.Rect(
            0,
            top * page.rect.height,
            page.rect.width,
            bottom * page.rect.height,
        )))
    return norm(" ".join(parts))


def title_case(value):
    value = norm(re.split(r"\s+[‐‑–—-]\s+", value, maxsplit=1)[0]).strip(" ‐‑–—-")
    return value.title()


def header_candidates(page, letters):
    """Return structural letter headings, pairing separately positioned letters/titles."""
    lines = lines_of(page)
    found = []
    direct = re.compile(
        rf"^([{letters}])\s+([A-Za-z][\w’'&.,:()?!‐‑–—\- ]{{2,}}(?:\s+[‐‑–—-]\s+.*)?)$")
    for index, line in enumerate(lines):
        match = direct.match(line.text)
        if match and line.x < 150:
            found.append((match.group(1), title_case(match.group(2)), line.y))
            continue
        if not re.fullmatch(rf"[{letters}]", line.text) or line.x > 120:
            continue
        neighbours = [candidate for candidate in lines
                      if candidate.x > line.x + 8 and abs(candidate.y - line.y) < 0.018]
        if not neighbours:
            neighbours = [candidate for candidate in lines[index + 1:index + 4]
                          if candidate.x > line.x and 0 <= candidate.y - line.y < 0.025]
        if not neighbours:
            continue
        title = min(neighbours, key=lambda candidate: (abs(candidate.y - line.y), candidate.x)).text
        if len(tokens(title)):
            found.append((line.text, title_case(title), line.y))
    deduped = {}
    for letter, title, y in found:
        deduped.setdefault(letter, (letter, title, y))
    return sorted(deduped.values(), key=lambda row: row[2])


def collect_single_text_cards(paper):
    headers = []
    for page_index in (1, 2):
        for letter, title, y in header_candidates(paper[page_index], "ABCDEFGHI"):
            headers.append((letter, title, page_index, y))
    headers.sort(key=lambda row: (row[2], row[3]))
    by_letter = {}
    for header in headers:
        by_letter.setdefault(header[0], header)
    headers = sorted(by_letter.values(), key=lambda row: (row[2], row[3]))
    if len(headers) < 4 or [row[0] for row in headers] != list("ABCDE")[:len(headers)]:
        raise ValueError(f"Single Text headings not reconciled: {[row[0] for row in headers]}")

    cards = []
    for header_index, (letter, title, page_index, y) in enumerate(headers):
        next_point = (headers[header_index + 1][2], headers[header_index + 1][3]) \
            if header_index + 1 < len(headers) else (3, 0.0)
        romans = []
        for candidate_page in range(page_index, min(next_point[0], 2) + 1):
            for line in lines_of(paper[candidate_page]):
                if candidate_page == page_index and line.y <= y:
                    continue
                if candidate_page == next_point[0] and line.y >= next_point[1]:
                    continue
                match = re.match(r"^\((i|ii)\)(?:\s|$)", line.text, re.I)
                if match and line.x < 125:
                    roman = match.group(1).lower()
                    if roman not in {row[0] for row in romans}:
                        romans.append((roman, candidate_page, line.y))
        if [row[0] for row in romans] != ["i", "ii"]:
            raise ValueError(f"Single Text {letter} roman choices not reconciled: {romans}")
        for roman_index, (roman, card_page, card_y) in enumerate(romans):
            end = (romans[roman_index + 1][1], romans[roman_index + 1][2]) \
                if roman_index + 1 < len(romans) else next_point
            cards.append(Card(
                "single",
                f"Single Text {letter} · {title} · ({roman})",
                card_page,
                card_y,
                p_end_page=end[0],
                p_end_y=end[1] if end[0] < len(paper) else 1.0,
            ))
    return cards


def collect_comparative_cards(paper):
    headers = []
    for page_index in (3, 4):
        for letter, title, y in header_candidates(paper[page_index], "ABC"):
            # Mode titles are short uppercase structural headings, never prose.
            if len(title) <= 48 and not title.startswith(("In ", "The Case", "With Reference")):
                headers.append((letter, title, page_index, y))
    headers.sort(key=lambda row: (row[2], row[3]))
    by_letter = {}
    for header in headers:
        by_letter.setdefault(header[0], header)
    headers = sorted(by_letter.values(), key=lambda row: (row[2], row[3]))
    if len(headers) < 2 or [row[0] for row in headers] != list("ABC")[:len(headers)]:
        raise ValueError(f"Comparative headings not reconciled: {headers}")

    cards = []
    for header_index, (letter, title, page_index, y) in enumerate(headers):
        next_point = (headers[header_index + 1][2], headers[header_index + 1][3]) \
            if header_index + 1 < len(headers) else (5, 0.0)
        questions = []
        for candidate_page in range(page_index, min(next_point[0], 4) + 1):
            for line in lines_of(paper[candidate_page]):
                if candidate_page == page_index and line.y <= y:
                    continue
                if candidate_page == next_point[0] and line.y >= next_point[1]:
                    continue
                match = re.match(r"^([12])\.(?:\s|$)", line.text)
                if match and line.x < 100:
                    number = match.group(1)
                    if number not in {row[0] for row in questions}:
                        questions.append((number, candidate_page, line.y))
        if [row[0] for row in questions] != ["1", "2"]:
            raise ValueError(f"Comparative {letter} choices not reconciled: {questions}")
        for question_index, (number, card_page, card_y) in enumerate(questions):
            end = (questions[question_index + 1][1], questions[question_index + 1][2]) \
                if question_index + 1 < len(questions) else next_point
            cards.append(Card(
                "comparative",
                f"Comparative {letter} · {title} · Q{number}",
                card_page,
                card_y,
                p_end_page=end[0],
                p_end_y=end[1] if end[0] < len(paper) else 1.0,
            ))
    return cards


def numbered_cards_on_page(paper, page_index, kind, label_prefix, start_after):
    found = []
    for line in lines_of(paper[page_index]):
        if line.y <= start_after:
            continue
        match = re.match(r"^([1-6])\.(?:\s|$)", line.text)
        if match and line.x < 105:
            number = int(match.group(1))
            if number not in {row[0] for row in found}:
                found.append((number, line.y, line.text))
    found.sort(key=lambda row: row[1])
    cards = []
    for index, (number, y, line_text) in enumerate(found):
        end_y = found[index + 1][1] if index + 1 < len(found) else 1.0
        suffix = f"Q{number}"
        if kind == "prescribed":
            poet = norm(re.sub(r"^[1-6]\.\s*", "", line_text))
            if not poet:
                following = [line for line in lines_of(paper[page_index]) if line.y > y and line.y - y < 0.045]
                poet = following[0].text if following else "Prescribed option"
            suffix = f"{title_case(poet)} · Q{number}"
        cards.append(Card(
            kind,
            f"{label_prefix} · {suffix}",
            page_index,
            y,
            p_end_page=page_index,
            p_end_y=end_y,
        ))
    return cards


def collect_poetry_cards(paper):
    page_index = 5
    unseen_heading = next((line.y for line in lines_of(paper[page_index])
                          if "UNSEEN POEM" in line.text.upper()), None)
    if unseen_heading is None:
        raise ValueError("Unseen Poetry heading missing")
    unseen = numbered_cards_on_page(paper, page_index, "unseen", "Unseen Poetry", unseen_heading)
    if [card.label.rsplit("Q", 1)[-1] for card in unseen] != ["1", "2"]:
        raise ValueError(f"Unseen choices not reconciled: {[card.label for card in unseen]}")

    page_index = 6
    prescribed_heading = next((line.y for line in lines_of(paper[page_index])
                               if "PRESCRIBED POETRY" in line.text.upper()), None)
    if prescribed_heading is None:
        raise ValueError("Prescribed Poetry heading missing")
    prescribed = numbered_cards_on_page(
        paper, page_index, "prescribed", "Prescribed Poetry", prescribed_heading)
    numbers = [int(card.label.rsplit("Q", 1)[-1]) for card in prescribed]
    if numbers not in ([1, 2, 3, 4], [1, 2, 3, 4, 5]):
        raise ValueError(f"Prescribed choices not reconciled: {numbers}")
    return unseen + prescribed


def paper2_start(scheme):
    for page_index, page in enumerate(scheme):
        head = norm(page.get_text())[:350].upper()
        if "PAPER 2" in head and "SINGLE TEXT" in norm(page.get_text()).upper():
            return page_index
    raise ValueError("Paper 2 scheme divider missing")


def line_window_score(anchor_tokens, lines, start_index):
    text = " ".join(line.text for line in lines[start_index:start_index + 5])
    return len(anchor_tokens & tokens(text)) / max(1, len(anchor_tokens))


def line_has_card_marker(card, line):
    if card.kind == "single":
        roman = card.label.rsplit("(", 1)[-1].rstrip(")")
        return bool(re.match(rf"^\({re.escape(roman)}\)(?:\s|$)", line.text, re.I)
                    and line.x < 150)
    number = card.label.rsplit("Q", 1)[-1]
    return bool(re.match(rf"^{re.escape(number)}\.(?:\s|$)", line.text)
                and line.x < 150)


def structural_marker_score(card, page):
    return 1 if any(line_has_card_marker(card, line) for line in lines_of(page)) else 0


def locate_scheme_cards(cards, paper, scheme):
    start_page = paper2_start(scheme)
    scheme_page_tokens = [tokens(page.get_text()) for page in scheme]
    prior = (start_page, 0.0)
    for card in cards:
        card.prompt = crop_text(
            paper, card.p_page, card.p_y, card.p_end_page, card.p_end_y)
        prompt_tokens = tokens(card.prompt)
        if len(prompt_tokens) < 5:
            raise ValueError(f"{card.label}: paper prompt has too few content tokens")

        paper_lines = lines_of(paper[card.p_page])
        anchor_lines = [line.text for line in paper_lines
                        if line.y >= card.p_y - 0.002][:5]
        anchor_tokens = tokens(" ".join(anchor_lines))

        page_scores = []
        for page_index in range(start_page, len(scheme)):
            prompt_score = len(prompt_tokens & scheme_page_tokens[page_index]) / len(prompt_tokens)
            anchor_score = len(anchor_tokens & scheme_page_tokens[page_index]) / max(1, len(anchor_tokens))
            marker_score = structural_marker_score(card, scheme[page_index])
            continuation_penalty = 3 if (
                card.kind == "comparative"
                and card.label.endswith("Q1")
                and "CONTD" in norm(scheme[page_index].get_text()).upper()
            ) else 0
            page_scores.append((4 * marker_score + 2 * anchor_score + prompt_score - continuation_penalty,
                                prompt_score, anchor_score, page_index))
        _, best_page_score, best_anchor_score, best_page = max(page_scores)
        if best_page_score < MIN_PAGE_OVERLAP or best_anchor_score < MIN_ANCHOR_OVERLAP:
            raise ValueError(
                f"{card.label}: scheme start overlap prompt={best_page_score:.2f}, "
                f"anchor={best_anchor_score:.2f}")

        scheme_lines = lines_of(scheme[best_page])
        line_scores = [(line_window_score(anchor_tokens, scheme_lines, index), index)
                       for index in range(len(scheme_lines))]
        best_line_score = max(score for score, _ in line_scores)
        marker_line_indexes = [index for index, line in enumerate(scheme_lines)
                               if line_has_card_marker(card, line)]
        if marker_line_indexes:
            marker_best = max(line_scores[index][0] for index in marker_line_indexes)
            eligible_line_indexes = [index for index in marker_line_indexes
                                     if line_scores[index][0] >= max(0.30, marker_best * 0.78)]
        else:
            eligible_line_indexes = [index for score, index in line_scores
                                     if score >= max(0.30, best_line_score * 0.78)]
        best_line_index = min(eligible_line_indexes)
        best_y = max(0.0, scheme_lines[best_line_index].y - 0.004)
        point = (best_page, best_y)
        if point <= prior:
            # Page-level matching is decisive, but a repeated generic first line can
            # select the wrong point.  Restrict to later pages/lines and retry.
            later = []
            for combined, prompt_score, anchor_score, page_index in page_scores:
                if (page_index < prior[0] or prompt_score < MIN_PAGE_OVERLAP
                        or anchor_score < MIN_ANCHOR_OVERLAP):
                    continue
                candidate_lines = lines_of(scheme[page_index])
                local_scores = [line_window_score(anchor_tokens, candidate_lines, index)
                                for index in range(len(candidate_lines))]
                local_best = max(local_scores)
                for line_index, line in enumerate(candidate_lines):
                    candidate = (page_index, max(0.0, line.y - 0.004))
                    if candidate <= prior:
                        continue
                    local_score = local_scores[line_index]
                    if local_score < max(0.30, local_best * 0.78):
                        continue
                    later.append((combined + local_score, prompt_score, anchor_score, candidate))
            if not later:
                raise ValueError(f"{card.label}: no monotonic scheme match after {prior}")
            best_rank = max(row[0] for row in later)
            eligible = [row for row in later if row[0] >= best_rank - 0.02]
            _, best_page_score, best_anchor_score, point = min(eligible, key=lambda row: row[3])
        card.s_page, card.s_y = point
        card.score = best_page_score
        prior = point


def region_segments(scheme, start, end):
    start_page, start_y = start
    end_page, end_y = end
    segments = []
    for page_index in range(start_page, end_page + 1):
        top = start_y if page_index == start_page else 0.0
        bottom = end_y if page_index == end_page else 1.0
        if bottom <= top or not scheme[page_index].get_text().strip():
            continue
        segments.append({"p": page_index + 1, "r": [0.0, round(top, 4), 1.0, round(bottom, 4)]})
    return segments


def paper_segments(card):
    segments = []
    for page_index in range(card.p_page, card.p_end_page + 1):
        top = card.p_y if page_index == card.p_page else 0.0
        bottom = card.p_end_y if page_index == card.p_end_page else 1.0
        if bottom > top:
            segments.append({"p": page_index + 1, "r": [0.0, round(top, 4), 1.0, round(bottom, 4)]})
    return segments


def scheme_region_text(scheme, region):
    return norm(" ".join(
        scheme[segment["p"] - 1].get_text("text", clip=fitz.Rect(
            0,
            segment["r"][1] * scheme[segment["p"] - 1].rect.height,
            scheme[segment["p"] - 1].rect.width,
            segment["r"][3] * scheme[segment["p"] - 1].rect.height,
        )) for segment in region
    ))


def require_region_overlap(card, scheme, region):
    overlap = len(tokens(card.prompt) & tokens(scheme_region_text(scheme, region))) \
        / max(1, len(tokens(card.prompt)))
    if overlap < MIN_REGION_OVERLAP:
        raise ValueError(
            f"{card.label}: scheme-region overlap {overlap:.2f} < {MIN_REGION_OVERLAP}")


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
            if delta < 0.035:
                candidates.append((delta, index))
        if not candidates:
            raise ValueError(
                f"existing Q{question['n']} does not match a discovered task at "
                f"paper p{question['pP']} y{question['pY'][0]}")
        _, index = min(candidates)
        matches[question["n"]] = index
        available.remove(index)
    return matches


def build_year(year):
    paper_path = os.path.join(CORPUS, "exampapers", str(year), PAPER_FILEID)
    scheme_path = os.path.join(CORPUS, "markingschemes", str(year), SCHEME_FILEID)
    sidecar_path = os.path.join(ANSWERS, str(year), f"{PAPER_FILEID}.json")
    if not all(os.path.exists(path) for path in (paper_path, scheme_path, sidecar_path)):
        return None, "official paper, scheme or shipped sidecar missing"

    paper = fitz.open(paper_path)
    scheme = fitz.open(scheme_path)
    with open(sidecar_path, encoding="utf-8") as handle:
        sidecar = json.load(handle)

    cards = collect_single_text_cards(paper) + collect_comparative_cards(paper) + collect_poetry_cards(paper)
    locate_scheme_cards(cards, paper, scheme)
    matches = match_existing(cards, sidecar["q"])
    matched_indexes = set(matches.values())
    next_number = max(int(question["n"]) for question in sidecar["q"]) + 1

    output_questions = []
    for question in sidecar["q"]:
        index = matches[question["n"]]
        card = cards[index]
        augmented = dict(question)
        augmented["label"] = card.label
        augmented["printOrder"] = index + 1
        augmented.pop("schemeRegion", None)
        end = (cards[index + 1].s_page, cards[index + 1].s_y) if index + 1 < len(cards) \
            else (min(card.s_page + 1, len(scheme) - 1), 1.0)
        audited_region = region_segments(scheme, (card.s_page, card.s_y), end)
        require_region_overlap(card, scheme, audited_region)
        if audited_region != question["region"]:
            augmented["schemeRegion"] = audited_region
        if card.p_end_page != card.p_page:
            augmented["paperRegion"] = paper_segments(card)
        output_questions.append(augmented)

    for index, card in enumerate(cards):
        if index in matched_indexes:
            continue
        end = (cards[index + 1].s_page, cards[index + 1].s_y) if index + 1 < len(cards) \
            else (min(card.s_page + 1, len(scheme) - 1), 1.0)
        region = region_segments(scheme, (card.s_page, card.s_y), end)
        if not region:
            raise ValueError(f"{card.label}: empty scheme region")
        require_region_overlap(card, scheme, region)
        question = {
            "n": str(next_number),
            "pP": card.p_page + 1,
            "pY": [round(card.p_y, 4), round(card.p_end_y if card.p_end_page == card.p_page else 1.0, 4)],
            "region": region,
            "mode": "crop",
            "conf": 1.0,
            "label": card.label,
            "printOrder": index + 1,
        }
        if card.p_end_page != card.p_page:
            question["paperRegion"] = paper_segments(card)
        output_questions.append(question)
        next_number += 1

    output_questions.sort(key=lambda question: int(question["n"]))
    if sorted(question["printOrder"] for question in output_questions) != list(range(1, len(cards) + 1)):
        raise ValueError("printOrder is not a complete permutation")
    sidecar["q"] = output_questions
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
    for year in years:
        try:
            sidecar, summary = build_year(year)
            if sidecar is None:
                print(f"SKIP {year}: {summary}")
                continue
            if not args.check:
                destination = os.path.join(ANSWERS, str(year), f"{PAPER_FILEID}.json")
                with open(destination, "w", encoding="utf-8") as handle:
                    json.dump(sidecar, handle, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
            action = "CHECK" if args.check else "WROTE"
            print(
                f"{action} {year}: {summary['cards']} cards; preserved {summary['preserved']}; "
                f"added {summary['added']}; min page overlap {summary['minPageOverlap']:.2f}")
        except Exception as error:
            failed += 1
            print(f"DROP {year}: {error}")
    print(f"done: {len(years) - failed} passed; {failed} dropped")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
