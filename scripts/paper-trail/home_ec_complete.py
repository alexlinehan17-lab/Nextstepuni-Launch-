#!/usr/bin/env python3
"""Additively complete the older Home Economics Section A/B/C sidecars.

The first importer left several 2011 and 2016 files with only the twelve
Section A cards.  It also missed Ordinary 2012 Section B Questions 4 and 5.
This repair reuses the strict section parser in ``home_ec_old.py``, preserves
every existing card and coordinate, labels the original Section A cards, and
appends only section/question keys that are absent.

Usage:
  python3 home_ec_complete.py --dry
  python3 home_ec_complete.py
  python3 home_ec_complete.py --check
"""

from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

import home_ec_old


HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
CORPUS = REPO / "paper-trail-corpus"
ANSWERS = HERE / "answers"
CONFIGS = [(year, level) for year in (2011, 2012, 2016) for level in "AG"]


def expected_sidecar(year: int, level: str):
    fileid = f"LC098{level}LP000EV.pdf"
    generated, error = home_ec_old.build(
        str(CORPUS / "exampapers" / str(year) / fileid),
        str(CORPUS / "markingschemes" / str(year) / fileid),
        False,
    )
    if error or generated is None:
        raise RuntimeError(f"{year} {level}: {error or 'could not build expected sidecar'}")
    labels = [question["label"] for question in generated["q"]]
    wanted = [
        *(f"Section A · Q{number}" for number in range(1, 13)),
        *(f"Section B · Q{number}" for number in range(1, 6)),
        *(f"Section C · Q{number}" for number in range(1, 4)),
    ]
    if labels != wanted:
        raise RuntimeError(f"{year} {level}: incomplete generated labels: {labels}")
    return fileid, generated


def merge(year: int, level: str, write: bool):
    fileid, generated = expected_sidecar(year, level)
    path = ANSWERS / str(year) / f"{fileid}.json"
    existing = json.loads(path.read_text())
    original_cards = copy.deepcopy(existing["q"])

    by_label = {
        question.get("label"): question
        for question in existing["q"]
        if question.get("label")
    }
    expected_by_label = {question["label"]: question for question in generated["q"]}

    # The old generic files contain precisely the twelve Section A cards in
    # printed order.  Label them in place without touching their coordinates.
    unlabeled = [question for question in existing["q"] if not question.get("label")]
    if unlabeled:
        if len(existing["q"]) != 12 or len(unlabeled) != 12:
            raise RuntimeError(f"{year} {level}: unexpected partial unlabeled sidecar")
        for number, question in enumerate(existing["q"], start=1):
            question["label"] = f"Section A · Q{number}"
            question["printOrder"] = number
        by_label = {question["label"]: question for question in existing["q"]}

    # Give preserved labelled cards an explicit physical order.  This matters
    # for 2012 Ordinary, whose newly appended B4/B5 IDs cannot reuse the old
    # C1/C2 IDs.
    order_by_label = {
        question["label"]: index
        for index, question in enumerate(generated["q"], start=1)
    }
    for label, question in by_label.items():
        if label in order_by_label:
            question.setdefault("printOrder", order_by_label[label])

    used_ids = {str(question["n"]) for question in existing["q"]}
    next_id = max(int(value) for value in used_ids if value.isdigit()) + 1
    added = []
    for label, candidate in expected_by_label.items():
        if label in by_label:
            continue
        card = copy.deepcopy(candidate)
        desired_id = str(card["n"])
        if desired_id in used_ids:
            desired_id = str(next_id)
            next_id += 1
        card["n"] = desired_id
        card["printOrder"] = order_by_label[label]
        used_ids.add(desired_id)
        existing["q"].append(card)
        added.append(label)

    if len(existing["q"]) != 20 or len({q["n"] for q in existing["q"]}) != 20:
        raise RuntimeError(f"{year} {level}: merged sidecar is not 20 unique cards")
    final_labels = {question.get("label") for question in existing["q"]}
    missing = set(expected_by_label) - final_labels
    if missing:
        raise RuntimeError(f"{year} {level}: missing labels after merge: {sorted(missing)}")

    # Existing cards may gain label/printOrder metadata, but their original
    # values must remain unchanged.
    for before, after in zip(original_cards, existing["q"][:len(original_cards)]):
        for key, value in before.items():
            if after.get(key) != value:
                raise RuntimeError(f"{year} {level}: existing card {before['n']} field {key} changed")

    changed = existing != json.loads(path.read_text())
    if write and changed:
        path.write_text(json.dumps(existing, ensure_ascii=False, indent=2) + "\n")
    return fileid, added, changed


def main():
    dry = "--dry" in sys.argv
    check = "--check" in sys.argv
    write = not dry and not check
    total_added = 0
    changed_files = 0
    for year, level in CONFIGS:
        fileid, added, changed = merge(year, level, write)
        total_added += len(added)
        changed_files += changed
        verb = "would add" if dry else "added" if write else "still missing"
        if added:
            print(f"{year} {fileid}: {verb} {len(added)} cards: {', '.join(added)}")
        else:
            print(f"{year} {fileid}: complete (20 cards)")
    print(f"files={len(CONFIGS)} changed={changed_files} additions={total_added}")
    if check and (changed_files or total_added):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
