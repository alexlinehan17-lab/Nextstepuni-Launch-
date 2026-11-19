#!/usr/bin/env python3
# Copyright 2026 Nextstepuni
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Paper Trail — English's deferred sittings (2022-2025): answer maps.

The SEC's deferred English sittings are papers of their own, filed as
"LC002<A|G>LP<100|200>EV-deferred.pdf" (paperTrailData.ts), set to June's
layout: Paper 1 prints three texts, each with Question A and B, then seven
compositions; Paper 2 prints the Single Text, Comparative Study, Unseen Poem
and Prescribed Poetry options. The PAPER side of each map is read by June's
own readers (english_p1, english_p1_comprehending, english_p2_complete,
english_p2_ol), so a deferred task is bounded exactly as June's is.

The SCHEME side differs. A deferred scheme says (its page 2) that it "will
only have been finalised for the questions attempted by the candidates", and
it omits whole tasks: 2024 Higher prints COMPOSING 1, 4, 5, 6 and 7 and no 2
or 3. So a task is mapped to its own scheme block only when that block is
found by the task's printed marker or title on a page whose words agree with
the prompt; a task the scheme does not set out is mapped `pagejump` to the
scheme's section heading for that part of the paper (whose general criteria
and grids still apply), and is listed as `schemeAbsent` in the report.

Usage:
  python3 scripts/paper-trail/english_deferred.py            # write the maps
  python3 scripts/paper-trail/english_deferred.py --check    # compare, write nothing
  python3 scripts/paper-trail/english_deferred.py --report out.json
"""
import argparse
import json
import os
import re
import sys

import fitz  # pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import english_p1  # noqa: E402
import english_p1_comprehending as comprehending  # noqa: E402
import english_p2_complete as p2  # noqa: E402
import english_p2_ol as p2ol  # noqa: E402

REPO = os.path.dirname(os.path.dirname(HERE))
CORPUS = os.path.join(REPO, "paper-trail-corpus")
ANSWERS = os.path.join(HERE, "answers")
COPYRIGHT = "© State Examinations Commission"

# Every English deferred sitting the SEC archive holds (paperTrailData.ts).
SITTINGS = ((2025, "A"), (2024, "A"), (2024, "G"), (2023, "A"), (2022, "A"), (2022, "G"))


def paths(year, level, component):
    paper = os.path.join(CORPUS, "deferredexams", str(year), f"LC002{level}LP{component}EV.pdf")
    scheme = os.path.join(CORPUS, "deferredmarkingschemes", str(year), f"LC002{level}LP000EV.pdf")
    return paper, scheme


def fileid(level, component, kind="paper"):
    return f"LC002{level}LP{component if kind == 'paper' else '000'}EV-deferred.pdf"


def words(text):
    return {w.lower() for w in re.findall(r"[A-Za-z’']{5,}", text)}


def clip_text(doc, region):
    out = []
    for seg in region:
        page = doc[seg["p"] - 1]
        r = seg.get("r", [0, 0, 1, 1])
        out.append(page.get_text("text", clip=fitz.Rect(
            r[0] * page.rect.width, r[1] * page.rect.height,
            r[2] * page.rect.width, r[3] * page.rect.height)))
    return " ".join(out)


def segments(doc, start, end):
    """Scheme region from (page0, y) to (page0, y), skipping blank leaves."""
    out = []
    for page_index in range(start[0], end[0] + 1):
        top = start[1] if page_index == start[0] else 0.0
        bottom = end[1] if page_index == end[0] else 1.0
        if bottom <= top or not doc[page_index].get_text().strip():
            continue
        out.append({"p": page_index + 1, "r": [0.0, round(max(0.0, top), 4), 1.0, round(bottom, 4)]})
    return out


# ------------------------------------------------------------------ Paper 1

def composing_heads(scheme, start_page0):
    """[(n, page0, y)] for every line that could open composition n, in page order."""
    heads = []
    for page_index in range(start_page0, len(scheme)):
        text = scheme[page_index].get_text()
        if page_index > start_page0 and re.search(r"^\s*PAPER\s+2\b", text, re.M):
            break
        for txt, x, y in english_p1.lines_with_pos(scheme[page_index]):
            m = english_p1.COMPOSING_HEAD.match(txt) or (english_p1.HEAD.match(txt) if x <= 0.25 else None)
            if m and 1 <= int(m.group(1)) <= 7:
                heads.append((int(m.group(1)), page_index, y))
    return heads


def paper2_divider(scheme, after_page0):
    for page_index in range(after_page0 + 1, len(scheme)):
        head = " ".join(scheme[page_index].get_text().split())[:200].upper()
        if "PAPER 2" in head:
            return page_index
    return len(scheme) - 1


def build_p1(year, level):
    paper_path, scheme_path = paths(year, level, "100")
    paper, scheme = fitz.open(paper_path), fitz.open(scheme_path)
    cp = english_p1.find_composing_page(paper)
    prompts = english_p1.composing_run(paper, cp)
    if sorted(prompts) != list(range(1, 8)):
        raise ValueError(f"{year} {level} P1: composing run {sorted(prompts)}")
    sp = english_p1.find_composing_page(scheme)
    stop = paper2_divider(scheme, sp)
    candidates = composing_heads(scheme, sp)

    def prompt_words(n):
        pg, y = prompts[n]
        nxt = prompts.get(n + 1)
        y_end = nxt[1] if nxt and nxt[0] == pg else 1.0
        page = paper[pg - 1]
        return words(page.get_text(clip=fitz.Rect(0, y * page.rect.height, page.rect.width, y_end * page.rect.height)))

    # A composition's block opens where the scheme restates its prompt: the
    # first candidate head for n whose following lines echo the paper's words.
    heads = {}
    for n in range(1, 8):
        for i, (m, page_index, y) in enumerate(candidates):
            if m != n or n in heads:
                continue
            probe = segments(scheme, (page_index, y - 0.005), (page_index, min(1.0, y + 0.12)))
            echo = len(prompt_words(n) & words(clip_text(scheme, probe))) / max(1, len(prompt_words(n)))
            if echo >= 0.5:
                heads[n] = (page_index, y)
    ordered_heads = sorted(heads.items(), key=lambda kv: kv[1])
    q, absent = [], []
    for i, n in enumerate(sorted(prompts)):
        pg, y = prompts[n]
        nxt = prompts.get(n + 1)
        y_end = nxt[1] if nxt and nxt[0] == pg else 1.0
        entry = {"n": str(n), "pP": pg, "pY": [round(y, 4), round(y_end, 4)], "printOrder": 7 + i}
        if n in heads:
            position = [k for k, _ in ordered_heads].index(n)
            end = ordered_heads[position + 1][1] if position + 1 < len(ordered_heads) else (stop, 0.0)
            region = segments(scheme, (heads[n][0], heads[n][1] - 0.012), end)
            echo = len(prompt_words(n) & words(clip_text(scheme, region))) / max(1, len(prompt_words(n)))
            if echo < 0.5:
                raise ValueError(f"{year} {level} P1 composing {n}: scheme block echo {echo:.2f}")
            entry.update({"region": region, "mode": "crop", "conf": 1.0})
        else:
            entry.update({"region": [{"p": sp + 1}], "mode": "pagejump", "conf": 0.5})
            absent.append(f"Composing {n}")
        q.append(entry)
    cards, error, qa = comprehending.build_cards(paper_path, scheme_path)
    if error:
        raise ValueError(f"{year} {level} P1 comprehending: {error}")
    q.extend(cards)
    q.sort(key=lambda e: int(e["n"]))
    sidecar = {"v": 1, "paperFileid": fileid(level, "100"), "schemeFileid": fileid(level, "000", "scheme"),
               "component": "100", "band": [1, len(scheme) + 1], "copyright": COPYRIGHT, "q": q}
    return sidecar, absent


# ------------------------------------------------------------------ Paper 2

SECTION_PHRASES = (("single", "SINGLE TEXT"), ("comparative", "COMPARATIVE STUDY"),
                   ("unseen", "UNSEEN POEM"), ("prescribed", "PRESCRIBED POETRY"))


def scheme_markers(scheme, start):
    """Every structural marker of the scheme's Paper 2, in reading order.

    section  a section heading ("SECTION II – THE COMPARATIVE STUDY", "UNSEEN POEM (20 marks)")
    option   a lettered option heading ("C  THE CRUCIBLE – Arthur Miller", "B  THEME")
    roman    a "(i)"/"(ii)" opening a line at the left margin
    number   a "1."-"7." opening a line at the left margin
    end      the criteria appendix, after which nothing is a task
    """
    out = []
    for page_index in range(start, len(scheme)):
        page = scheme[page_index]
        lines = p2.lines_of(page)
        if page_index > start and any(re.match(r"^(?:LEAVING CERTIFICATE ENGLISH\s+)?(?:CRITERIA FOR ASSESSMENT|"
                                               r"REASONABLE ACCOMMODATIONS?)\.?$", line.text.strip())
                                      for line in lines):
            out.append({"kind": "end", "page": page_index, "y": 0.0})
            break
        for line in lines:
            upper = line.text.upper()
            for kind, phrase in SECTION_PHRASES:
                if phrase in upper and len(line.text) <= 64 and not upper.startswith("CANDIDATES"):
                    out.append({"kind": "section", "section": kind, "page": page_index, "y": line.y})
            m = re.match(r"^\((i{1,3})\)(?:\s|$)", line.text, re.I)
            if m and line.x < 150:
                out.append({"kind": "roman", "value": m.group(1).lower(), "page": page_index, "y": line.y})
            m = re.match(r"^([1-7])\.(?:\s|$)", line.text)
            if m and line.x < 150:
                out.append({"kind": "number", "value": m.group(1), "page": page_index, "y": line.y})
            # A comparative mode named only in the running head ("GENERAL VISION AND VIEWPOINT (1)").
            m = re.match(r"^(?:([A-C])[.\s]+)?(%s)\s*(?:\(\d\))?$" % "|".join(MODES), upper.strip())
            if m and not m.group(1):
                # "A" printed apart from its centred mode title on the same baseline.
                beside = [o for o in lines if re.fullmatch(r"[A-C]\.?", o.text.strip())
                          and abs(o.y - line.y) < 0.01 and o.x < line.x]
                if beside and line.x > 150:
                    out.append({"kind": "option", "value": beside[0].text.strip(".").strip(),
                                "title": p2.tokens(m.group(2)), "page": page_index, "y": line.y,
                                "running": False})
                    continue
            if m and line.x > 150 and (m.group(1) or line.y < 0.1):
                # A centred "A RELATIONSHIPS" heading, or the mode alone in a running head.
                out.append({"kind": "option", "value": m.group(1), "title": p2.tokens(m.group(2)),
                            "page": page_index, "y": line.y, "running": not m.group(1)})
        for letter, title, y in p2.header_candidates(page, "ABCDEFGHI"):
            # A heading names a text, a poem or a mode; a prose line opening with a capital
            # letter ("I ... insights gained into Macbeth's various ...") is not one.
            if any(phrase in title.upper() for _, phrase in SECTION_PHRASES) or len(p2.tokens(title)) > 6:
                continue
            out.append({"kind": "option", "value": letter, "title": p2.tokens(title), "page": page_index, "y": y})
    order = {"section": 0, "option": 1, "number": 2, "roman": 3, "end": 4}
    out.sort(key=lambda m: (m["page"], round(m["y"], 3), order[m["kind"]]))
    # A list of the paper's sections ("Section I – The Single Text / Section II – The Comparative
    # Study ...") is not a heading: drop section lines with another section's line close by.
    out = [m for m in out if m["kind"] != "section" or not any(
        o["kind"] == "section" and o["section"] != m["section"] and o["page"] == m["page"]
        and abs(o["y"] - m["y"]) < 0.12 for o in out)]
    # Sections follow the paper's order; "... included in SECTION 1 – The Single Text" inside
    # the Comparative Study's notes is a cross-reference, not a heading.
    rank = {kind: i for i, (kind, _) in enumerate(SECTION_PHRASES)}
    ordered, reached = [], -1
    for m in out:
        if m["kind"] == "section":
            if rank[m["section"]] < reached:
                continue
            reached = rank[m["section"]]
        ordered.append(m)
    out = ordered
    # Lettered options ascend within a section; a prose line opening "A ..." after B is not one.
    # A running head repeats on every page of its mode; only its first appearance opens it.
    out = [m for m in out if not m.get("running") or not any(
        o["kind"] == "option" and o["value"] and o["page"] == m["page"] and o["title"] == m["title"]
        for o in out)]
    kept, last_letter, seen_running, last_title = [], None, set(), None
    for m in out:
        if m["kind"] in ("section", "end"):
            last_letter, seen_running, last_title = None, set(), None
        if m["kind"] == "option" and m.get("running"):
            key = frozenset(m["title"])
            if key in seen_running or key == last_title:
                continue
            seen_running.add(key)
            last_title = key
        elif m["kind"] == "option":
            if last_letter is not None and m["value"] <= last_letter:
                continue
            last_letter, last_title = m["value"], frozenset(m["title"])
        kept.append(m)
    return kept


MODES = ("THEME OR ISSUE", "THEME", "CULTURAL CONTEXT", "GENERAL VISION AND VIEWPOINT", "LITERARY GENRE",
         "RELATIONSHIPS", "SOCIAL SETTING", "HERO, HEROINE, VILLAIN", "ASPECTS OF STORY")


def point(marker):
    return (marker["page"], marker["y"])


def next_point(markers, after, stop_kinds):
    for m in markers:
        if point(m) > after and m["kind"] in stop_kinds:
            return point(m)
    return None


def section_range(markers, kind):
    begin = next((point(m) for m in markers if m["kind"] == "section" and m["section"] == kind), None)
    if begin is None:
        return None
    end = next((point(m) for m in markers if point(m) > begin and
                ((m["kind"] == "section" and m["section"] != kind) or m["kind"] == "end")), (10 ** 6, 0.0))
    return begin, end


def option_marker(markers, rng, letter, title):
    inside = [m for m in markers if m["kind"] == "option" and rng[0] <= point(m) < rng[1]]
    for m in inside:
        agrees = bool(title) and bool(m["title"]) and len(title & m["title"]) / max(1, len(title)) >= 0.5
        if (m["value"] == letter and (not title or not m["title"] or agrees)) or (m["value"] is None and agrees):
            return m
    return None


def locate(card, markers):
    """(start, end) of the card's own block in the scheme, or None."""
    kind = card.kind
    rng = section_range(markers, kind)
    if rng is None:
        return None
    label = card.label.split(" · ")
    letter_match = re.search(r"(?:Single Text|Comparative|Poetry) ([A-I])\b", card.label)
    letter = letter_match.group(1) if letter_match else None
    title = p2.tokens(label[1]) if len(label) > 1 and kind in ("single", "comparative") else \
        (p2.tokens(label[1]) if len(label) > 1 and kind == "prescribed" and letter else set())
    in_range = [m for m in markers if rng[0] <= point(m) < rng[1]]
    if kind == "unseen" and "Q" not in label[-1]:
        return rng                                   # Ordinary: the whole Unseen Poem
    if kind in ("single", "comparative", "prescribed") and letter:
        option = option_marker(markers, rng, letter, title)
        if option is None:
            return None
        opt_end = next_point(in_range, point(option), {"option", "section", "end"}) or rng[1]
        inner = [m for m in in_range if point(option) < point(m) < opt_end]
        roman = re.search(r"\((i|ii)\)$", card.label)
        number = re.search(r"Q(\d)$", card.label)
        if roman:                                    # Higher Single Text (i)/(ii)
            hit = next((m for m in inner if m["kind"] == "roman" and m["value"] == roman.group(1)), None)
            if hit is None:
                return None
            start = point(option) if roman.group(1) == "i" else point(hit)
            end = next((point(m) for m in inner if point(m) > point(hit) and m["kind"] == "roman"), opt_end)
            return start, end
        if number:                                   # Higher Comparative Q1/Q2
            hit = next((m for m in inner if m["kind"] == "number" and m["value"] == number.group(1)), None)
            if hit is None:
                return None
            start = point(option) if number.group(1) == "1" else point(hit)
            end = next((point(m) for m in inner if point(m) > point(hit) and m["kind"] == "number"
                        and m["value"] != number.group(1)), opt_end)
            return start, end
        return point(option), opt_end                # Ordinary: the whole option
    number = re.search(r"Q(\d)$", card.label)
    if not number:
        return None
    hits = [m for m in in_range if m["kind"] == "number" and m["value"] == number.group(1)]
    if not hits:
        return None
    hit = hits[0]
    end = next((point(m) for m in in_range if point(m) > point(hit) and m["kind"] == "number"
                and m["value"] != number.group(1)), rng[1])
    return point(hit), end


def build_p2(year, level):
    paper_path, scheme_path = paths(year, level, "200")
    paper, scheme = fitz.open(paper_path), fitz.open(scheme_path)
    ordinary = level == "G"
    if ordinary:
        cards = p2ol.collect_cards(paper, year)
    else:
        cards = (p2.collect_single_text_cards(paper) + p2.collect_comparative_cards(paper)
                 + p2.collect_poetry_cards(paper))
    start = next(i for i, page in enumerate(scheme)
                 if re.search(r"PAPER (?:2|TWO)\b", " ".join(page.get_text().split())[:350].upper()) and i > 2)
    markers = scheme_markers(scheme, start)
    q, absent = [], []
    for index, card in enumerate(cards):
        mp, my = card.match_point if ordinary else (card.p_page, card.p_y)
        card.prompt = p2.crop_text(paper, mp, my, card.p_end_page, card.p_end_y)
        entry = {"n": str(index + 1), "label": card.label, "printOrder": index + 1,
                 "pP": card.p_page + 1,
                 "pY": [round(card.p_y, 4), round(card.p_end_y if card.p_end_page == card.p_page else 1.0, 4)]}
        if card.p_end_page != card.p_page:
            entry["paperRegion"] = p2.paper_segments(card)
        block = locate(card, markers)
        region = None
        if block is not None:
            (sp, sy), (ep, ey) = block
            if ep >= len(scheme):
                ep, ey = len(scheme) - 1, 1.0
            region = segments(scheme, (sp, sy - 0.004), (ep, ey))
            prompt_tokens = p2.tokens(card.prompt)
            overlap = len(prompt_tokens & p2.tokens(clip_text(scheme, region))) / max(1, len(prompt_tokens))
            if overlap < 0.33:
                raise ValueError(f"{year} {level} P2 {card.label}: scheme-region overlap {overlap:.2f}")
        if region:
            entry.update({"region": region, "mode": "crop", "conf": 1.0})
        else:
            rng = section_range(markers, card.kind)
            entry.update({"region": [{"p": (rng[0][0] if rng else start) + 1}], "mode": "pagejump", "conf": 0.5})
            absent.append(card.label)
        q.append(entry)
    sidecar = {"v": 1, "paperFileid": fileid(level, "200"), "schemeFileid": fileid(level, "000", "scheme"),
               "component": "200", "band": [start + 1, len(scheme) + 1], "copyright": COPYRIGHT, "q": q}
    return sidecar, absent


def dump(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--report")
    args = ap.parse_args()
    report, stale = [], []
    for year, level in SITTINGS:
        for builder in (build_p1, build_p2):
            sidecar, absent = builder(year, level)
            tag = f"{year} {'HL' if level == 'A' else 'OL'} {sidecar['component']}"
            report.append({"year": year, "level": level, "component": sidecar["component"],
                           "tasks": len(sidecar["q"]), "schemeAbsent": absent})
            print(f"{tag}: {len(sidecar['q'])} blocks; scheme sets out no block for {absent or 'none'}")
            # June's English papers are served by these reviewed maps hosted byte-identically in
            # public/paper-answers once a paper is published (english_publish.py), never by paper-anchors.
            for directory, value in ((ANSWERS, sidecar),):
                path = os.path.join(directory, str(year), sidecar["paperFileid"] + ".json")
                text = dump(value)
                if args.check:
                    if not os.path.exists(path) or open(path, encoding="utf-8").read() != text:
                        stale.append(path)
                else:
                    os.makedirs(os.path.dirname(path), exist_ok=True)
                    with open(path, "w", encoding="utf-8") as fh:
                        fh.write(text)
    if args.report:
        with open(args.report, "w", encoding="utf-8") as fh:
            json.dump(report, fh, ensure_ascii=False, indent=1)
    if stale:
        print("stale: " + ", ".join(stale))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
