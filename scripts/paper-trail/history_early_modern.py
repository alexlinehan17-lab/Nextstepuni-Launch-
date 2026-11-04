#!/usr/bin/env python3
"""Paper-only topic anchors and Topic Atlas tags for LC Early Modern History.

The Early Modern field (SEC subject 096) is a separate paper from Later Modern
(004), indexed in Paper Trail as `history-early-modern`, and printed in the
same shape: a documents-based question on one case study, then Ireland and
Europe topic blocks, each an independently selectable exam task. history.py
builds Later Modern's anchors and tags; this is the same pass for Early
Modern, using history.py's own page readers so the two fields are cut by one
rule.

Tags use the canonical History curriculum (curriculum.ts): Early Modern
Ireland is strand history-0 and Europe history-1, four ids per topic (the
topic, then its three case studies). A topic block files under its topic's
first id, as Later Modern's do; the documents question files under its CASE
STUDY, read off the paper's own "Case study to which the documents relate"
line and matched against the curriculum's case-study names, with the topic as
its secondary tag, as Later Modern's do.

Sittings are added as their Mark Bank cards are carded:

    python3 scripts/paper-trail/history_early_modern.py 2021hl 2021ol ...

Every sitting named is rebuilt from its papers (both language editions);
every other paper already in the tag file is kept exactly as it was.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import fitz

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import history as LM  # noqa: E402  the Later Modern pass and its page readers

ROOT = HERE.parent.parent
CORPUS = ROOT / "paper-trail-corpus" / "exampapers"
INDEX_PATH = ROOT / "paperTrailData.ts"
CURRICULUM_PATH = ROOT / "curriculum.ts"
TAGS_PATH = HERE / "topic-tags" / "tags" / "history-early-modern.json"
HOSTED_ROOT = ROOT / "public" / "paper-anchors"
SUBJECT = "history-early-modern"

TOPIC_MAIN_IDS = {
    "I": {number: f"history-0-{(number - 1) * 4}" for number in range(1, 7)},
    "E": {number: f"history-1-{(number - 1) * 4}" for number in range(1, 7)},
}
STRAND = {"I": 0, "E": 1}
LEVEL = {"hl": "higher", "ol": "ordinary"}


def paper_index() -> list[dict]:
    source = INDEX_PATH.read_text()
    match = re.search(r'  "history-early-modern": (\[[\s\S]*?\n  \]),\n  "', source)
    if not match:
        raise RuntimeError("Could not locate History (Early Modern) in paperTrailData.ts")
    return [entry for entry in json.loads(re.sub(r",\s*]$", "]", match.group(1)))
            if not entry.get("sitting") and entry["year"] >= 2010]


def curriculum_names() -> dict[str, str]:
    text = CURRICULUM_PATH.read_text()
    return {m.group(1): m.group(2)
            for m in re.finditer(r'"id": "(history-[01]-\d+)",\s*"name": "([^"]+)"', text)}


WORD = re.compile(r"[a-z]+")
STOP = {"the", "of", "and", "case", "study", "to", "in", "a", "s", "port", "new", "world",
        "his", "her", "career", "clerical", "mission"}


def case_study_id(family: str, number: int, title: str, names: dict[str, str]) -> str:
    """The curriculum case study a documents question's printed title names.

    Only the topic's three case studies are candidates (the paper names the
    topic too), and exactly one must share a content word with the title.
    """
    words = set(WORD.findall(title.lower().replace("’", "'"))) - STOP
    base = (number - 1) * 4
    candidates = [f"history-{STRAND[family]}-{base + k}" for k in (1, 2, 3)]
    hits = [cid for cid in candidates
            if words & (set(WORD.findall(names[cid].lower())) - STOP)]
    if len(hits) != 1:
        raise RuntimeError(f"case study {title!r}: {family}{number} candidates "
                           f"{[(c, names[c]) for c in candidates]} matched {hits}")
    return hits[0]


def dqb_case_title(document: fitz.Document) -> str:
    """The printed "Case study to which (the) documents relate" title."""
    for page in document:
        lines = [LM.clean(t) for t, _y in LM.line_records(page)]
        for index, line in enumerate(lines):
            if re.match(r"^Case study to which (?:the )?documents? relate", line, re.I):
                rest = re.sub(r"^Case study to which (?:the )?documents? relates?\s*:?\s*", "", line, flags=re.I)
                return rest or lines[index + 1]
    raise RuntimeError("no case-study line")


def dqb_topic(document: fitz.Document, pdf_path: Path) -> tuple[str, int]:
    """The documents question's topic. As history.py reads it, except that the
    2025 Higher Early Modern paper heads it "Europe: Topic 1", the area's
    name abbreviated (hist_paper.py's TOPIC allows the same)."""
    try:
        return LM.dqb_topic(document, pdf_path)
    except RuntimeError:
        page_text = LM.clean(document[1].get_text("text"))
        ireland = re.search(r"(?:Ireland|Éire)\s*:\s*(?:Topic|Topaic)\s*([1-6])", page_text, re.I)
        europe = re.search(r"(?:Europe|An Eoraip)(?: and the wider world| agus an domhan mór)?\s*:\s*(?:Topic|Topaic)\s*([1-6])",
                           page_text, re.I)
        if bool(ireland) == bool(europe):
            raise
        match = ireland or europe
        return ("I" if ireland else "E", int(match.group(1)))


def main(argv: list[str]) -> None:
    sittings = set()
    for token in argv:
        m = re.fullmatch(r"(\d{4})(hl|ol)", token)
        if not m:
            raise SystemExit(f"usage: {Path(__file__).name} 2021hl 2021ol ...  (got {token!r})")
        sittings.add((int(m.group(1)), LEVEL[m.group(2)]))
    names = curriculum_names()
    existing = json.loads(TAGS_PATH.read_text()) if TAGS_PATH.exists() else []
    kept = [paper for paper in existing if (paper["year"], paper["level"]) not in sittings]

    papers: list[dict] = []
    report: list[dict] = []
    for entry in paper_index():
        if (entry["year"], entry["level"]) not in sittings:
            continue
        if len(entry["papers"]) != 1:
            raise RuntimeError(f"{entry['year']} {entry['level']} {entry['lang']}: expected one paper")
        fileid = entry["papers"][0]["doc"]["f"]
        path = CORPUS / str(entry["year"]) / fileid
        if not path.exists():
            raise FileNotFoundError(path)
        with fitz.open(path) as document:
            dqb = dqb_topic(document, path)
            anchors, section_three, _corrections = LM.topic_anchors(document, path, entry, dqb)
            alternative = LM.alternative_anchor(document, path, entry, anchors, dqb)
            title = dqb_case_title(document) if entry["lang"] == "ev" else None

        if entry["lang"] == "ev":
            case_id = case_study_id(dqb[0], dqb[1], title, names)
        else:
            # The Irish edition prints the same case study; its tag is the
            # English edition's, read off that paper.
            twin = next(p for p in papers if p["year"] == entry["year"]
                        and p["level"] == entry["level"] and p["lang"] == "ev")
            case_id = twin["q"][0]["primary"]
        dqb_tag = {"primary": case_id, "secondary": TOPIC_MAIN_IDS[dqb[0]][dqb[1]]}
        questions = [{"n": str(number), **dqb_tag} for number in range(1, 5)]
        questions += [{"n": f"{a['family']}{a['number']}", "primary": TOPIC_MAIN_IDS[a["family"]][a["number"]]}
                      for a in anchors]
        if alternative:
            questions.append({"n": "ALT", **dqb_tag})
        papers.append({"subjectId": SUBJECT, "level": entry["level"], "lang": entry["lang"],
                       "year": entry["year"], "fileid": fileid, "paperKey": "single", "q": questions})

        hosted: list[dict] = []
        card_anchors = anchors + ([alternative] if alternative else [])
        for index, anchor in enumerate(card_anchors):
            if index + 1 < len(card_anchors):
                nxt = card_anchors[index + 1]
                end = (nxt["page"], nxt["y"])
                if anchor["family"] == "I" and nxt["family"] == "E":
                    end = section_three
                if nxt.get("alternative"):
                    end = (anchor["page"], 1.0)
            else:
                end = (anchor["page"], 1.0)
            if end[0] < anchor["page"] or (end[0] == anchor["page"] and end[1] <= anchor["y"] + 0.005):
                raise RuntimeError(f"{path}: invalid crop end for {anchor}")
            if end[0] - anchor["page"] > 3:
                raise RuntimeError(f"{path}: implausible topic span for {anchor}")
            family_label = "Ireland" if anchor["family"] == "I" else "Europe & Wider World"
            section = 2 if anchor["family"] == "I" else 3
            n = "ALT" if anchor.get("alternative") else f"{anchor['family']}{anchor['number']}"
            label = (f"Alternative Part A · {family_label} Topic {anchor['number']}" if anchor.get("alternative")
                     else f"Section {section} · {family_label} Topic {anchor['number']}")
            hosted.append({"n": n, "pP": anchor["page"], "pY": [anchor["y"], 1], "region": [{"p": 1}],
                           "mode": "pagejump", "conf": 0.5, "label": label, "printOrder": index + 1,
                           "endP": end[0], "endY": end[1]})
        target = HOSTED_ROOT / str(entry["year"])
        target.mkdir(parents=True, exist_ok=True)
        (target / f"{fileid}.json").write_text(json.dumps(
            {"v": 1, "paperFileid": fileid, "schemeFileid": "", "component": "000", "band": [1, 1],
             "copyright": LM.COPYRIGHT, "paperOnly": 1, "q": hosted},
            ensure_ascii=False, separators=(",", ":")) + "\n")
        report.append({"paper": f"{entry['year']} {entry['level']} {entry['lang']}", "dqb": f"{dqb[0]}{dqb[1]}",
                       "caseStudy": title, "caseStudyId": case_id, "caseStudyName": names[case_id],
                       "blocks": [q["n"] for q in questions[4:]]})

    found = {(p["year"], p["level"]) for p in papers}
    if found != sittings:
        raise RuntimeError(f"sittings with no Early Modern paper in the index: {sorted(sittings - found)}")
    out = sorted(kept + papers, key=lambda p: (-p["year"], p["level"], p["lang"]))
    TAGS_PATH.write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n")
    print(json.dumps(report, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main(sys.argv[1:])
