#!/usr/bin/env python3
"""Independent census of every printed Art task, read from the paper itself.

This shares no code with art_cards.py. It reads a current-format (2023 on)
question paper's own text, finds every printed "Question N" and its lettered
parts, and records any selection directive the paper prints. The deck is then
checked against it (tests/test_art_sec_wording.py): a printed task with no
card, or a card for no printed task, fails.

    python3 scripts/markbank/authoring/art_paper_census.py 2026 higher
"""
from __future__ import annotations

import json
import os
import re
import sys

import fitz

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))
PAPERS = os.path.join(ROOT, 'examiner-reports', 'art', 'papers')
SHORT = {'higher': 'hl', 'ordinary': 'ol'}
FURNITURE = re.compile(
    r'Leaving Certificate Examination \d{4}|Art\s*[–-]\s*(?:Visual Studies|History and Appreciation of Art)\s*[–-]\s*'
    r'(?:Higher|Ordinary) Level|Optional (?:Planning|Answer) Space.*|Additional Answer Space.*|'
    r'Answer for Question|Label all work clearly with the question number and part\.?')
DIRECTIVE = re.compile(
    r'\b(?:choose|select|either|(?:one|any) of the following|any (?:one|two|three|four|five))\b', re.I)


def paper_text(year: int, level: str) -> list[tuple[int, str]]:
    doc = fitz.open(os.path.join(PAPERS, f'{year}-{SHORT[level]}-paper.pdf'))
    pages = []
    for number, page in enumerate(doc, start=1):
        text = page.get_text(sort=True)
        if re.search(r'Acknowledgements|Copyright notice', text):
            continue
        pages.append((number, text))
    return pages


def census(year: int, level: str) -> dict:
    pages = paper_text(year, level)
    text = '\n'.join(f'\n@@PAGE {number}\n{FURNITURE.sub(" ", body)}' for number, body in pages)
    heads = list(re.finditer(r'(?m)^\s*Question\s+(\d{1,2})\b', text))
    questions = {}
    for index, head in enumerate(heads):
        number = int(head.group(1))
        end = heads[index + 1].start() if index + 1 < len(heads) else len(text)
        body = text[head.end():end]
        page = int(re.findall(r'@@PAGE (\d+)', text[:head.start()])[-1])
        if number in questions:
            continue  # the instructions page names questions it does not print
        parts = sorted(set(re.findall(r'(?m)^\s*\(([a-d])\)\s', body)))
        linked = bool(re.search(r'(?mi)^\s*and\s*$|^\s*and\s+(?=[A-Z])', body)) and year <= 2022
        tasks = [f'({p})' for p in parts] if parts else (['task 1', 'task 2'] if linked else ['response'])
        directives = sorted({m.group(0).lower() for m in DIRECTIVE.finditer(' '.join(body.split()))})
        questions[number] = {'page': page, 'tasks': tasks, 'directives': directives}
    return {'year': year, 'level': level, 'questions': questions}


def main() -> int:
    year, level = int(sys.argv[1]), sys.argv[2]
    print(json.dumps(census(year, level), indent=1))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
