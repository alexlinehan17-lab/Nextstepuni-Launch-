#!/usr/bin/env python3
"""English Mark Bank's paper-only denominator.

    python3 scripts/markbank/authoring/english_census.py
    python3 scripts/markbank/authoring/english_census.py --check

English defeats the generic leaf parser because its question numbers restart for
each text, work, comparative mode and poet, while choice questions often contain
compulsory subparts governed by one holistic rubric. This census names every
independently selectable scored response and also records the printed subparts
that must live inside that card.

The question papers are the only denominator. Marking schemes are never opened
here. Structural assertions are run against all twenty local 2021-2025 PDFs
before the ledger is emitted, so a missing paper, text, composing choice, work,
mode or poet stops the build instead of quietly lowering the denominator.
"""

from __future__ import annotations

import argparse
import glob
import json
import os
import re
import sys

import fitz

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))
PAPER_ROOT = os.path.join(ROOT, 'examiner-reports', 'english', 'papers')
OUT = os.path.join(ROOT, 'scripts', 'markbank', 'authored', 'english-census.json')

PAPER_RE = re.compile(r'(?P<year>\d{4})-(?P<level>hl|ol)-(?P<component>100|200)-paper\.pdf$')
ROMANS = ('i', 'ii', 'iii')
LETTERS_5 = tuple('abcde')
LETTERS_6 = tuple('abcdef')
LETTERS_9 = tuple('abcdefghi')


def compact(value: str) -> str:
    return re.sub(r'\s+', ' ', value.replace('\xa0', ' ')).strip()


def paper_text(path: str) -> tuple[fitz.Document, str]:
    doc = fitz.open(path)
    return doc, '\n'.join(page.get_text('text').replace('\xa0', ' ') for page in doc)


def record(*, year: int, level: str, paper: int, key: str, ref: str,
           section: str, marks: int, parts: list[str] | None = None) -> dict:
    card_id = f'english-{year}-{level}-p{paper}-{key}'
    # The first batch is one complete paper. Every other row is explicit queue,
    # never an omission disguised as "not applicable".
    status = 'authored' if year == 2025 and level == 'hl' and paper == 1 else 'queued'
    return {
        'id': card_id,
        'year': year,
        'level': level,
        'paper': paper,
        'section': section,
        'questionRef': ref,
        'marks': marks,
        'printedParts': parts or [],
        'status': status,
    }


def assert_paper_1(doc: fitz.Document, text: str, path: str) -> None:
    qas = re.findall(r'QUESTION\s+A\s*[–-]\s*\d+\s+MARKS', text, re.I)
    qbs = re.findall(r'QUESTION\s+B\s*[–-]\s*\d+\s+MARKS', text, re.I)
    if len(qas) != 3 or len(qbs) != 3:
        raise AssertionError(f'{path}: expected 3 Question A and 3 Question B blocks; got {len(qas)}/{len(qbs)}')
    if len(doc) < 8:
        raise AssertionError(f'{path}: composing page 8 is missing')
    composing = re.findall(r'^\s*([1-7])\.\s+', doc[7].get_text('text').replace('\xa0', ' '), re.M)
    if composing != list('1234567'):
        raise AssertionError(f'{path}: composing choices are {composing}, expected 1..7')


def paper_1(year: int, level: str, doc: fitz.Document, text: str, path: str) -> list[dict]:
    assert_paper_1(doc, text, path)
    out = []
    for text_no in range(1, 4):
        if level == 'hl':
            qa_marks = (10, 10, 20) if year <= 2022 else (15, 15, 20)
            for roman, marks in zip(ROMANS, qa_marks):
                out.append(record(
                    year=year, level=level, paper=1,
                    key=f't{text_no}-a-{roman}', ref=f'{year} {level.upper()} Paper 1 Text {text_no} QA({roman})',
                    section='Comprehending A', marks=marks,
                ))
        else:
            qa_marks = (10, 10, 10, 10) if year <= 2022 else (15, 15, 10, 10)
            for suffix, marks in zip(('i', 'ii', 'iii-a', 'iii-b'), qa_marks):
                printed = suffix.replace('-', ')(')
                out.append(record(
                    year=year, level=level, paper=1,
                    key=f't{text_no}-a-{suffix}', ref=f'{year} OL Paper 1 Text {text_no} QA({printed})',
                    section='Comprehending A', marks=marks,
                ))
        out.append(record(
            year=year, level=level, paper=1,
            key=f't{text_no}-b', ref=f'{year} {level.upper()} Paper 1 Text {text_no} QB',
            section='Comprehending B', marks=40 if year <= 2022 else 50,
        ))
    for number in range(1, 8):
        out.append(record(
            year=year, level=level, paper=1,
            key=f'composing-{number}', ref=f'{year} {level.upper()} Paper 1 Composing {number}',
            section='Composing', marks=100,
        ))
    return out


def assert_hl_paper_2(doc: fitz.Document, text: str, path: str) -> None:
    if len(doc) < 7:
        raise AssertionError(f'{path}: expected at least seven pages')
    # Pages 2-3 contain the five Single Text work choices. Use uppercase OR:
    # lowercase "or" is ordinary prose and not a choice boundary.
    single = '\n'.join(doc[index].get_text('text') for index in (1, 2))
    if len(re.findall(r'\bOR\b', single)) != 5:
        raise AssertionError(f'{path}: Single Text must print five OR choices')
    comparative = '\n'.join(doc[index].get_text('text') for index in (3, 4))
    if len(re.findall(r'^\s*2\.\s+', comparative, re.M)) != 3:
        raise AssertionError(f'{path}: Comparative must print Q2 in each of three modes')
    unseen = doc[5].get_text('text')
    if not re.search(r'Answer either Question 1 or Question 2', compact(unseen), re.I):
        raise AssertionError(f'{path}: Unseen Poetry Q1/Q2 choice is missing')
    prescribed = doc[6].get_text('text')
    if not re.search(r'one of the following questions\s*\(1\s*[–-]\s*5\)', compact(prescribed), re.I):
        raise AssertionError(f'{path}: five Prescribed Poetry choices are missing')


def hl_paper_2(year: int, doc: fitz.Document, text: str, path: str) -> list[dict]:
    assert_hl_paper_2(doc, text, path)
    out = []
    single_marks = 70 if year <= 2022 else 60
    for work in LETTERS_5:
        for roman in ('i', 'ii'):
            out.append(record(
                year=year, level='hl', paper=2,
                key=f'single-{work}-{roman}', ref=f'{year} HL Paper 2 Single Text {work.upper()}({roman})',
                section='Single Text', marks=single_marks,
            ))
    for mode in LETTERS_5[:3]:
        out.append(record(
            year=year, level='hl', paper=2,
            key=f'comparative-{mode}-q1', ref=f'{year} HL Paper 2 Comparative {mode.upper()} Q1',
            section='Comparative Study', marks=70, parts=['(a) 30 marks', '(b) 40 marks'],
        ))
        out.append(record(
            year=year, level='hl', paper=2,
            key=f'comparative-{mode}-q2', ref=f'{year} HL Paper 2 Comparative {mode.upper()} Q2',
            section='Comparative Study', marks=70,
        ))
    out.extend([
        record(year=year, level='hl', paper=2, key='unseen-q1',
               ref=f'{year} HL Paper 2 Unseen Poetry Q1', section='Unseen Poetry', marks=20,
               parts=['(a) 10 marks', '(b) 10 marks']),
        record(year=year, level='hl', paper=2, key='unseen-q2',
               ref=f'{year} HL Paper 2 Unseen Poetry Q2', section='Unseen Poetry', marks=20),
    ])
    for number in range(1, 6):
        out.append(record(
            year=year, level='hl', paper=2,
            key=f'prescribed-{number}', ref=f'{year} HL Paper 2 Prescribed Poetry {number}',
            section='Prescribed Poetry', marks=50,
        ))
    return out


def assert_ol_paper_2(doc: fitz.Document, text: str, path: str) -> None:
    if len(doc) < 20:
        raise AssertionError(f'{path}: expected the nine works and six prescribed-poem pages')
    for page_no in range(2, 11):
        page = compact(doc[page_no - 1].get_text('text'))
        if not re.search(r'Answer any two of the following four questions', page, re.I):
            raise AssertionError(f'{path}: Single Text work page {page_no} lacks its four-question instruction')
        for number in range(1, 5):
            if not re.search(rf'(?:^|\s){number}\.\s', page):
                raise AssertionError(f'{path}: Single Text work page {page_no} lacks Q{number}')
    for page_no in range(11, 14):
        page = compact(doc[page_no - 1].get_text('text'))
        if len(re.findall(r'\bOR\b', page)) != 1:
            raise AssertionError(f'{path}: Comparative page {page_no} must contain one OR')
    unseen = compact(doc[13].get_text('text'))
    if not re.search(r'1\.\s', unseen) or not re.search(r'2\.\s', unseen):
        raise AssertionError(f'{path}: both compulsory Unseen Poetry questions are required')
    for page_no in range(15, 21):
        page = doc[page_no - 1].get_text('text')
        for roman in ROMANS:
            if not re.search(rf'\({roman}\)', page, re.I):
                raise AssertionError(f'{path}: Prescribed Poetry page {page_no} lacks ({roman})')


def ol_paper_2(year: int, doc: fitz.Document, text: str, path: str) -> list[dict]:
    assert_ol_paper_2(doc, text, path)
    out = []
    for work in LETTERS_9:
        for number in range(1, 5):
            out.append(record(
                year=year, level='ol', paper=2,
                key=f'single-{work}-q{number}', ref=f'{year} OL Paper 2 Single Text {work.upper()} Q{number}',
                section='Single Text', marks=30,
                parts=['(a) 10 marks', '(b) 10 marks', '(c) 10 marks'] if number == 1 else [],
            ))
    for mode in LETTERS_5[:3]:
        for number in (1, 2):
            out.append(record(
                year=year, level='ol', paper=2,
                key=f'comparative-{mode}-q{number}', ref=f'{year} OL Paper 2 Comparative {mode.upper()} Q{number}',
                section='Comparative Study', marks=70,
                parts=['(a)(i) 15 marks', '(a)(ii) 15 marks', '(b) 40 marks'],
            ))
    for number in (1, 2):
        out.append(record(
            year=year, level='ol', paper=2,
            key=f'unseen-q{number}', ref=f'{year} OL Paper 2 Unseen Poetry Q{number}',
            section='Unseen Poetry', marks=10,
        ))
    for poet in LETTERS_6:
        for roman, marks in zip(ROMANS, (15, 15, 20)):
            out.append(record(
                year=year, level='ol', paper=2,
                key=f'prescribed-{poet}-{roman}', ref=f'{year} OL Paper 2 Prescribed Poetry {poet.upper()}({roman})',
                section='Prescribed Poetry', marks=marks,
            ))
    return out


def build() -> dict:
    files = sorted(glob.glob(os.path.join(PAPER_ROOT, '*-paper.pdf')))
    expected_names = {
        f'{year}-{level}-{component}-paper.pdf'
        for year in range(2021, 2026)
        for level in ('hl', 'ol')
        for component in ('100', '200')
    }
    names = {os.path.basename(path) for path in files}
    if names != expected_names:
        raise AssertionError(
            f'English corpus mismatch; missing={sorted(expected_names - names)}, extra={sorted(names - expected_names)}')

    asks = []
    paper_counts = []
    for path in files:
        match = PAPER_RE.search(path)
        if not match:
            continue
        year = int(match.group('year'))
        level = match.group('level')
        component = match.group('component')
        doc, text = paper_text(path)
        try:
            rows = (paper_1(year, level, doc, text, path) if component == '100'
                    else hl_paper_2(year, doc, text, path) if level == 'hl'
                    else ol_paper_2(year, doc, text, path))
        finally:
            doc.close()
        asks.extend(rows)
        paper_counts.append({
            'paper': os.path.relpath(path, ROOT),
            'year': year,
            'level': level,
            'component': component,
            'cardUnits': len(rows),
            'authored': sum(row['status'] == 'authored' for row in rows),
            'queued': sum(row['status'] == 'queued' for row in rows),
        })

    ids = [ask['id'] for ask in asks]
    if len(ids) != len(set(ids)):
        raise AssertionError('duplicate English census ids')
    if len(asks) != 630:
        raise AssertionError(f'expected 630 independently selectable card units, found {len(asks)}')
    return {
        'subject': 'english',
        'sourceRule': 'Question papers only; marking schemes never contribute to the denominator.',
        'cardUnitRule': (
            'One card per independently selectable scored response. Compulsory subparts governed by one holistic '
            'rubric stay together and are enumerated in printedParts; separately scored subquestions are separate cards.'
        ),
        'paperCount': len(paper_counts),
        'cardUnitCount': len(asks),
        'authoredCount': sum(ask['status'] == 'authored' for ask in asks),
        'queuedCount': sum(ask['status'] == 'queued' for ask in asks),
        'papers': paper_counts,
        'asks': asks,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true', help='fail if the committed ledger is stale')
    args = parser.parse_args()
    payload = build()
    rendered = json.dumps(payload, ensure_ascii=False, indent=2) + '\n'
    if args.check:
        try:
            with open(OUT, encoding='utf-8') as handle:
                current = handle.read()
        except FileNotFoundError:
            print(f'missing {OUT}', file=sys.stderr)
            return 1
        if current != rendered:
            print(f'stale {OUT}; run english_census.py', file=sys.stderr)
            return 1
    else:
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        with open(OUT, 'w', encoding='utf-8') as handle:
            handle.write(rendered)
    print(
        f"English census: {payload['paperCount']} papers, {payload['cardUnitCount']} card units, "
        f"{payload['authoredCount']} authored, {payload['queuedCount']} queued"
    )
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
