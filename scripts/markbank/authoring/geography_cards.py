#!/usr/bin/env python3
"""Build the 2021–2026 Geography Mark Bank corpus.

The two official question-paper PDFs and the shared marking scheme are the
authorities for every sitting.  Part One remains one card per short question;
Part Two remains one card per independently selectable A/B/C task (and per
Higher-Level option essay).  A printed finite route is expanded: (i)/(ii), a
choose-one list, and every choose-N combination each become real practice
cards.  Open choices such as "any city" remain open.

Geography's marking grammar is not a model-answer checklist.  The generated
cards retain the published allocation and Significant Relevant Point (SRP)
directions, with one holistic placement control.  This lets exact short answers
stay exact while ensuring the scheme's explicitly non-exhaustive examples do
not become invented binary marking points.

Question pages that contain maps, charts, photographs or source text are kept
as official PDF source material. Tasks that require a *separate* Ordnance
Survey map, legend or aerial photograph ship only when those exact official
companions are in Paper Trail; otherwise they remain census-held.

Run:

    python3 scripts/markbank/authoring/geography_cards.py
    python3 scripts/markbank/authoring/geography_cards.py --check
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
import os
import re
import subprocess
import sys
import unicodedata
from dataclasses import dataclass
from typing import Any, Iterable

import fitz

import geography_review as GR
import geography_review_2026_hl as REVIEW_2026_HL
import geography_review_2026_ol as REVIEW_2026_OL
import geography_review_2025_hl as REVIEW_2025_HL
import geography_review_2025_ol as REVIEW_2025_OL
import geography_review_2024_hl as REVIEW_2024_HL
import geography_review_2024_ol as REVIEW_2024_OL
import geography_review_2023_hl as REVIEW_2023_HL
import geography_review_2023_ol as REVIEW_2023_OL
import geography_review_2022_hl as REVIEW_2022_HL
import geography_review_2022_ol as REVIEW_2022_OL
import geography_review_2021_hl as REVIEW_2021_HL
import geography_review_2021_ol as REVIEW_2021_OL
import geography_review_2020_hl as REVIEW_2020_HL
import geography_review_2020_ol as REVIEW_2020_OL
import geography_review_2019_hl as REVIEW_2019_HL
import geography_review_2019_ol as REVIEW_2019_OL
import geography_review_2018_hl as REVIEW_2018_HL
import geography_review_2018_ol as REVIEW_2018_OL
import geography_review_2017_hl as REVIEW_2017_HL
import geography_review_2017_ol as REVIEW_2017_OL
import geography_review_2016_hl as REVIEW_2016_HL
import geography_review_2016_ol as REVIEW_2016_OL
import geography_review_2015_hl as REVIEW_2015_HL
import geography_review_2015_ol as REVIEW_2015_OL
import geography_review_2014_hl as REVIEW_2014_HL
import geography_review_2014_ol as REVIEW_2014_OL


ROOT = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))
PAPER_ROOT = os.path.join(ROOT, 'examiner-reports', 'geography', 'papers')
SCHEME_ROOT = os.path.join(ROOT, 'examiner-reports', 'geography', 'schemes')
OUT = os.path.join(ROOT, 'components', 'MarkBank', 'cards', 'geography', 'authored.json')
CENSUS_OUT = os.path.join(
    ROOT, 'scripts', 'markbank', 'authored', 'geography-census.json')
REVIEW_AUDIT_OUT = os.path.join(
    ROOT, 'scripts', 'markbank', 'authored', 'geography-reviewed-audit.json')
SIZES = os.path.join(ROOT, 'components', 'MarkBank', 'cards', 'sizes.json')
ATLAS_OUT = os.path.join(
    ROOT, 'data', 'examTopics', 'geography-reviewed-question-runtime.json')
CROSSWALK = os.path.join(
    ROOT, 'data', 'examTopics', 'geography-curriculum-crosswalk.json')
# The exact-question join the Atlas already ships. A reviewed question's row
# replaces this one at runtime, so the reviewed row must carry every topic the
# shipped join gave it: a review adds the topics its tasks prove and never
# takes a question out of a topic a student already browses it under.
REFERENCE_ATLAS = os.path.join(
    ROOT, 'data', 'examTopics', 'geography-question-runtime.json')

# Sittings whose every page and scheme allocation was independently reviewed.
# Their cards come from the review ledger, not from the generic reader below.
REVIEWED = {
    (2026, 'higher'): REVIEW_2026_HL,
    (2026, 'ordinary'): REVIEW_2026_OL,
    (2025, 'higher'): REVIEW_2025_HL,
    (2025, 'ordinary'): REVIEW_2025_OL,
    (2024, 'higher'): REVIEW_2024_HL,
    (2024, 'ordinary'): REVIEW_2024_OL,
    (2023, 'higher'): REVIEW_2023_HL,
    (2023, 'ordinary'): REVIEW_2023_OL,
    (2022, 'higher'): REVIEW_2022_HL,
    (2022, 'ordinary'): REVIEW_2022_OL,
    (2021, 'higher'): REVIEW_2021_HL,
    (2021, 'ordinary'): REVIEW_2021_OL,
    (2020, 'higher'): REVIEW_2020_HL,
    (2020, 'ordinary'): REVIEW_2020_OL,
    (2019, 'higher'): REVIEW_2019_HL,
    (2019, 'ordinary'): REVIEW_2019_OL,
    (2018, 'higher'): REVIEW_2018_HL,
    (2018, 'ordinary'): REVIEW_2018_OL,
    (2017, 'higher'): REVIEW_2017_HL,
    (2017, 'ordinary'): REVIEW_2017_OL,
    (2016, 'higher'): REVIEW_2016_HL,
    (2016, 'ordinary'): REVIEW_2016_OL,
    (2015, 'higher'): REVIEW_2015_HL,
    (2015, 'ordinary'): REVIEW_2015_OL,
    (2014, 'higher'): REVIEW_2014_HL,
    (2014, 'ordinary'): REVIEW_2014_OL,
}

# 2021-2026 are carded in full. An earlier sitting joins the corpus only once
# its own review ledger is in REVIEWED; the generic reader never reads it.
CORE_YEARS = tuple(range(2021, 2027))
YEARS = tuple(sorted({*CORE_YEARS, *(year for year, _level in REVIEWED)}))
ID_PREFIX = 'geography-{year}-{short}-'
LEVELS = ('higher', 'ordinary')
LEVEL_SHORT = {'higher': 'hl', 'ordinary': 'ol'}
LEVEL_REF = {'higher': 'HL', 'ordinary': 'OL'}
PART_TWO_BASE = {'higher': 48, 'ordinary': 36}
PART_TWO_MARKS = {
    'higher': {'A': 20, 'B': 30, 'C': 30, 'option': 80},
    'ordinary': {'A': 30, 'B': 40, 'C': 30},
}

# The map extract, its legend and the aerial photograph are separate official
# documents, so cards retain them separately instead of fabricating one
# combined page. Their identities per year are in COMPANIONS below (CLP003 is
# the 1:50 000 extract and CLPC00 the legend; they were once attached the wrong
# way round). Older sittings without a reviewed ledger still hold their
# companion tasks.
COMPANION_SOURCE_YEARS = frozenset({2026})

# U+F020 is the Symbol-font space some schemes and papers set after a bullet.
SPACE_CHARS = ('\xa0', '\u2007', '\u202f', '\uf020')
LIGATURES = {
    '\u00ad': '', '\ufb00': 'ff', '\ufb01': 'fi', '\ufb02': 'fl',
    '\ufb03': 'ffi', '\ufb04': 'ffl',
}

# Geography's OS map and aerial photograph are separate examination materials,
# not pages in the Part One/Part Two booklet. The location name may sit between
# the source noun and "accompanying this paper" ("map of Clonmel accompanying
# this paper"), and one 2024 task names both sources without repeating that
# boilerplate. Match the dependency, not one exact sentence shape.
EXTERNAL_SOURCE = re.compile(
    r'\baccompan(?:y|ying|ies)\s+(?:this|the)\s+paper\b|'
    r'\busing evidence from the aerial photograph\s+OR\s+from the\s+'
    r'1:50\s*000 Ordnance Survey map\b',
    re.I,
)

GEOGRAPHY_SOURCE_REFERENCE = re.compile(
    r'\bOrdnance Survey map\b|\baerial photograph\b', re.I)
EMBEDDED_OS_EXTRACT = re.compile(
    r'\bOrdnance Survey map extract above\b', re.I)

# A small number of B/C tasks print their evidence on the question page rather
# than in the usual A position. Keep the official layout for those too. This is
# intentionally about evidence the student must READ, not a prompt asking the
# student to draw a diagram of their own.
EMBEDDED_SOURCE = re.compile(
    r'\btable above\b|'
    r'\bphotographs?\s+(?:[A-Z](?:\s*,?\s*(?:and\s+)?[A-Z])+|of\s+different)\b|'
    r'\b(?:map extract|diagram|graph|chart|figure|images?)\s+(?:above|below)\b|'
    r'\bshown above\b',
    re.I,
)

# These closed inline routes are printed without a bullet pool.  The phrase is
# replaced with the selected route while every other word of the task remains.
INLINE_CHOICES: tuple[tuple[re.Pattern[str], tuple[tuple[str, str], ...]], ...] = (
    (
        re.compile(
            r'one fluvial landform\s+or\s+one coastal landform\s+or\s+'
            r'one glacial landform', re.I),
        (
            ('fluvial-landform', 'one fluvial landform'),
            ('coastal-landform', 'one coastal landform'),
            ('glacial-landform', 'one glacial landform'),
        ),
    ),
    (
        re.compile(r'climate\s+or\s+geomorphology', re.I),
        (('climate', 'climate'), ('geomorphology', 'geomorphology')),
    ),
    (
        re.compile(
            r'footloose industries\s+or\s+financial services\s+or\s+mass tourism',
            re.I,
        ),
        (
            ('footloose-industries', 'footloose industries'),
            ('financial-services', 'financial services'),
            ('mass-tourism', 'mass tourism'),
        ),
    ),
)


CHOICE_IS_NOT_A_ROUTE = (
    'Choice is not a route: the student chooses which N of the M printed items '
    'to answer and the scheme marks each chosen item with the same allocation, '
    'so the printed question, with every item, is one card. Saved progress '
    'moves to the card kept on the first printed combination.')


def clean_unicode(value: str) -> str:
    for char in SPACE_CHARS:
        value = value.replace(char, ' ')
    for bad, good in LIGATURES.items():
        value = value.replace(bad, good)
    return (value.replace('‐', '-').replace('‑', '-').replace('‒', '-')
            .replace('−', '-'))


def compact(value: str) -> str:
    return re.sub(r'\s+', ' ', clean_unicode(value)).strip()


def comparable(value: str) -> str:
    value = unicodedata.normalize('NFKC', clean_unicode(value)).lower()
    value = value.replace('’', "'").replace('‘', "'")
    return re.sub(r'[^\w]+', ' ', value, flags=re.UNICODE).strip()


def slug(value: str, limit: int = 72) -> str:
    value = unicodedata.normalize('NFKD', value)
    value = ''.join(char for char in value if not unicodedata.combining(char))
    value = value.lower().replace('’', '').replace("'", '')
    value = re.sub(r'[^a-z0-9]+', '-', value).strip('-')
    return value[:limit].rstrip('-') or 'route'


def paper_path(year: int, level: str, part: int) -> str:
    return os.path.join(
        PAPER_ROOT, f'{year}-{LEVEL_SHORT[level]}-04{part + 1}-paper.pdf')


def scheme_path(year: int, level: str) -> str:
    return os.path.join(SCHEME_ROOT, f'{year}-{LEVEL_SHORT[level]}.pdf')


def scheme_markdown_path(year: int, level: str) -> str:
    return os.path.join(SCHEME_ROOT, f'{year}-{LEVEL_SHORT[level]}.md')


def clean_pdf_text(value: str) -> str:
    value = clean_unicode(value)
    value = value.replace('', '•').replace('', '•').replace('', '✓')
    value = re.sub(r'(?mi)^\s*Leaving Certificate Examination.*$', '', value)
    value = re.sub(r'(?mi)^\s*Geography\s*[-–].*$', '', value)
    value = re.sub(r'(?mi)^\s*Copyright notice.*$', '', value)
    value = re.sub(r'(?m)^\s*\d+\s*$', '', value)
    value = re.sub(r'[ \t]+', ' ', value)
    value = re.sub(r' *\n *', '\n', value)
    value = re.sub(r'\n{2,}', '\n', value)
    return value.strip()


def readable_prompt(value: str) -> str:
    """Unwrap visual PDF lines while retaining lists and numbered subparts."""
    value = clean_pdf_text(value)
    value = re.sub(r'\s*\[(?:8|10|20|30|40|80|100)m\]\s*', '', value)
    value = re.sub(
        r'Answer\s+\(i\)\s+or\s+\(ii\)\.?', '@@ANSWER_ROUTE@@',
        value, flags=re.I)
    value = re.sub(r'(?m)^\s*([•])\s*', r'\n\1 ', value)
    value = re.sub(r'(?m)^\s*(\((?:i|ii|iii|iv|v|vi|vii)\))\s*', r'\n\1 ', value)
    value = re.sub(r'(?mi)^\s*Or\s*$', '\nOr\n', value)
    value = re.sub(r'[ \t]+', ' ', value)
    value = re.sub(r'\s*\n\s*', ' ', value)
    value = re.sub(r'\s*(• |\((?:i|ii|iii|iv|v|vi|vii)\) |Or\s)', r'\n\1', value)
    value = re.sub(r'\n{2,}', '\n', value)
    value = re.sub(r'\s+([?.!,;:])', r'\1', value)
    value = value.replace('@@ANSWER_ROUTE@@', 'Answer (i) or (ii).')
    return value.strip()


def question_only_text(value: str) -> str:
    """Remove flattened source evidence when the official page is attached.

    PDF extraction serialises map labels, prose, axes and image credits ahead
    of the ask. Repeating that noisy serialization above the official page is
    both less legible and less faithful than showing the printed source once.
    Roman subquestions are the cleanest boundary; source tasks without them
    begin at their first examination command.
    """
    first_part = re.search(r'(?m)^\(i\)\s+', value)
    if first_part:
        value = value[first_part.start():]
    else:
        command = re.search(
            r'\b(?:Answer|Calculate|Complete|Describe|Discuss|Draw|Examine|Explain|'
            r'Identify|List|Match|Name|Outline|State|Study|Suggest|Using|Use)\b',
            value,
        )
        value = value[command.start():] if command else value
    # Image/source credits are valuable on the attached official page but are
    # OCR litter in the plain prompt. Attribution remains explicit in the
    # source reader; remove only URL-shaped credit tokens here.
    value = re.sub(
        r'\b(?:Amended from|Source:)\s+(?:https?://)?\S+', '', value,
        flags=re.I)
    value = re.sub(r'\b(?:https?://|www\.)\S+', '', value, flags=re.I)
    # Location tables can be flattened after the instruction as a run of
    # headings, feature names and the example answer ("Feature on Satellite
    # Image Location on Aerial Photograph A Bridge ...").  The exact table is
    # already visible on the attached official page, so stop at the paper's
    # own final instruction instead of printing an unreadable second copy.
    value = re.sub(
        r'(One has been completed for you\.)\s+.*$', r'\1', value,
        flags=re.I | re.S)
    value = re.sub(r'[ \t]{2,}', ' ', value)
    return value.strip()


def question_title_and_text(ref: str, raw: str) -> tuple[str, str]:
    raw = clean_pdf_text(raw)
    raw = re.sub(r'\s*\[(?:8|10|20|30|40|80|100)m\]\s*', '', raw)
    # First printed line contains the number/ref and title.  On some PDFs the
    # title is a second block at the same y-coordinate; the text layer still
    # places it immediately after the ref.
    if ref.isdigit() and int(ref) >= 13:
        match = re.match(rf'^\s*{re.escape(ref)}\.\s*', raw, re.I)
        if not match:
            raise AssertionError(f'{ref}: cannot find printed option heading in {raw[:120]!r}')
        number = int(ref)
        title = (
            'Global Interdependence' if number <= 15
            else 'Geoecology' if number <= 18
            else 'Culture and Identity' if number <= 21
            else 'The Atmosphere–Ocean Environment')
        body = readable_prompt(raw[match.end():])
        if len(body) < 8:
            raise AssertionError(f'{ref}: implausibly short question text {body!r}')
        return title, body

    match = re.match(rf'^\s*{re.escape(ref)}\.\s*([^\n]*)\n?', raw, re.I)
    if not match:
        raise AssertionError(f'{ref}: cannot find printed heading in {raw[:120]!r}')
    title = compact(match.group(1)) or f'Question {ref}'
    body = readable_prompt(raw[match.end():])
    if len(body) < 8:
        raise AssertionError(f'{ref}: implausibly short question text {body!r}')
    return title, body


@dataclass(frozen=True)
class PaperQuestion:
    ref: str
    title: str
    question_text: str
    marks: int
    page: int
    part: int


def line_text(line: dict[str, Any]) -> str:
    return ''.join(span['text'] for span in line.get('spans', ())).strip()


def part_one_questions(year: int, level: str) -> list[PaperQuestion]:
    document = fitz.open(paper_path(year, level, 1))
    starts: dict[int, tuple[int, float]] = {}
    for page_index, page in enumerate(document):
        if page_index < 2 or page_index > 14:
            continue
        for block in page.get_text('dict')['blocks']:
            for line in block.get('lines', ()):  # image blocks have no lines
                text = line_text(line)
                # Require whitespace (or line end) after the dot: graph labels
                # such as 11.5 are bold numbers too, not Question 11 headings.
                match = re.match(r'^(1[0-2]|[1-9])\.(?:\s+|$)', text)
                if not match or not line.get('spans'):
                    continue
                first = line['spans'][0]
                if 'Bold' not in first.get('font', ''):
                    continue
                number = int(match.group(1))
                starts.setdefault(number, (page_index, float(line['bbox'][1])))

    if sorted(starts) != list(range(1, 13)):
        raise AssertionError(
            f'{year} {level} Part One headings {sorted(starts)}, expected 1-12')

    out: list[PaperQuestion] = []
    marks = 8 if level == 'higher' else 10
    for number in range(1, 13):
        page_index, top = starts[number]
        next_page, next_top = starts[number + 1] if number < 12 else (-1, 0.0)
        bottom = next_top - 2 if next_page == page_index else document[page_index].rect.height - 44
        raw = document[page_index].get_text(
            'text', sort=True,
            clip=fitz.Rect(0, max(0, top - 2), document[page_index].rect.width, bottom),
        )
        title, question_text = question_title_and_text(str(number), raw)
        out.append(PaperQuestion(
            ref=str(number), title=title, question_text=question_text,
            marks=marks, page=page_index + 1, part=1,
        ))
    return out


def part_two_questions(year: int, level: str) -> list[PaperQuestion]:
    document = fitz.open(paper_path(year, level, 2))
    chunks: list[str] = []
    page_starts: list[tuple[int, int]] = []
    cursor = 0
    for page_number, page in enumerate(document, start=1):
        text = clean_unicode(page.get_text('text', sort=True))
        page_starts.append((cursor, page_number))
        chunks.append(text)
        cursor += len(text) + 2
    joined = '\n\n'.join(chunks)
    marker = re.compile(
        r'(?m)^\s*((?:[1-9]|1[0-2])[ABC]|1[3-9]|2[0-4])\.\s+')
    raw_matches = list(marker.finditer(joined))
    matches: list[re.Match[str]] = []
    seen: set[str] = set()
    for match in raw_matches:
        if match.group(1) in seen:
            continue
        seen.add(match.group(1))
        matches.append(match)
    expected = PART_TWO_BASE[level]
    if len(matches) != expected:
        raise AssertionError(
            f'{year} {level} Part Two found {len(matches)} tasks, expected {expected}: '
            f'{[match.group(1) for match in matches]}')

    def page_for(offset: int) -> int:
        answer = 1
        for start, number in page_starts:
            if start > offset:
                break
            answer = number
        return answer

    out: list[PaperQuestion] = []
    for index, match in enumerate(matches):
        ref = match.group(1)
        end = matches[index + 1].start() if index + 1 < len(matches) else len(joined)
        block = joined[match.start():end]
        tariff = re.search(r'\[(\d{2,3})m\]', block)
        if tariff is None:
            raise AssertionError(f'{year} {level} {ref}: printed mark tariff not found')
        raw = block[:tariff.start()]
        title, question_text = question_title_and_text(ref, raw)
        printed_marks = int(tariff.group(1))
        expected_marks = (
            PART_TWO_MARKS[level]['option'] if ref.isdigit()
            else PART_TWO_MARKS[level][ref[-1]])
        # The 2021/2022 Ordinary papers occasionally place the 40-mark task at
        # C rather than B. The printed tariff, not the letter, is authoritative;
        # later papers use the now-familiar 30/40/30 order.
        valid_ordinary = (
            level == 'ordinary' and not ref.isdigit()
            and ((ref.endswith('A') and printed_marks == 30)
                 or (not ref.endswith('A') and printed_marks in (30, 40))))
        if printed_marks != expected_marks and not valid_ordinary:
            raise AssertionError(
                f'{year} {level} {ref}: {printed_marks}m, expected {expected_marks}m')
        out.append(PaperQuestion(
            ref=ref, title=title, question_text=question_text,
            marks=printed_marks, page=page_for(match.end()), part=2,
        ))
    if level == 'ordinary':
        for number in range(1, 13):
            total = sum(item.marks for item in out
                        if (not item.ref.isdigit()
                            and int(re.match(r'\d+', item.ref).group()) == number))
            if total != 100:
                raise AssertionError(
                    f'{year} ordinary Q{number}: A/B/C total {total}, expected 100')
    return out


def first_part_one_scheme_page(document: fitz.Document) -> int:
    for page_index, page in enumerate(document):
        text = page.get_text('text', sort=True)
        if 'PART ONE' in text and 'SHORT' in text:
            return page_index
    raise AssertionError('Part One scheme table not found')


def numbered_scheme_chunks(text: str) -> dict[int, str]:
    text = compact(text)
    matches = list(re.finditer(
        r'\bQ\.?\s*(1[0-2]|[1-9])\.?(?=\s|\()', text, re.I))
    first: list[re.Match[str]] = []
    seen: set[int] = set()
    for match in matches:
        number = int(match.group(1))
        if number in seen:
            continue
        seen.add(number)
        first.append(match)
    out: dict[int, str] = {}
    for index, match in enumerate(first):
        end = first[index + 1].start() if index + 1 < len(first) else len(text)
        chunk = compact(text[match.start():end])
        chunk = re.split(
            r'\s+(?:Leaving Certificate Examination|Page\s+\d+|\d+\s+of\s+\d+)\b',
            chunk, maxsplit=1, flags=re.I)[0]
        out[int(match.group(1))] = chunk
    return out


def part_one_scheme(year: int, level: str) -> dict[int, dict[str, Any]]:
    document = fitz.open(scheme_path(year, level))
    page_index = first_part_one_scheme_page(document)
    found: dict[int, str] = {}
    if level == 'higher':
        page = document[page_index]
        mid = page.rect.width / 2
        clips = (fitz.Rect(0, 0, mid + 5, page.rect.height),
                 fitz.Rect(mid - 5, 0, page.rect.width, page.rect.height))
        for clip in clips:
            found.update(numbered_scheme_chunks(
                page.get_text('text', sort=True, clip=clip)))
    else:
        for offset in (0, 1):
            found.update(numbered_scheme_chunks(
                document[page_index + offset].get_text('text', sort=True)))
    if sorted(found) != list(range(1, 13)):
        raise AssertionError(
            f'{year} {level}: Part One scheme questions {sorted(found)}, expected 1-12')
    return {
        number: {'page': page_index + 1 + (1 if level == 'ordinary' and number >= 7 else 0),
                 'guidance': [text]}
        for number, text in found.items()
    }


@dataclass(frozen=True)
class SchemeBlock:
    page: int
    guidance: list[str]


def paragraph_lines(value: str) -> list[str]:
    """Turn PDF-wrapped scheme lines into legible allocation paragraphs."""
    furniture = (
        r'^## Page ', r'^Question \d+$', r'^SECTION \d+$',
        r'^PATTERNS AND PROCESSES', r'^REGIONAL GEOGRAPHY$',
        r'^ELECTIVE ', r'^OPTIONS$', r'^Questions \d+ to \d+$',
        r'^All questions carry ', r'^Leaving Certificate Examination',
        r'^Geography\s*[-–]', r'^Page \d+ of \d+$', r'^\d+$',
    )
    raw = []
    for source in clean_unicode(value).splitlines():
        line = compact(source.replace('', '•').replace('', '•'))
        if not line or any(re.search(pattern, line, re.I) for pattern in furniture):
            continue
        raw.append(line)
    paragraphs: list[str] = []
    current = ''
    starts = re.compile(
        r'^(?:[•]|\((?:i|ii|iii|iv|v|vi|vii)\)|Or$|Total\b|Annotation\b|'
        r'(?:Sketch|Map) Outline\b|For each\b|Allow\b|Credit\b|Max\b|'
        r'At least\b|Relevant information\b|Description\b|Explanation\b|'
        r'Examination\b|Discussion\b|Coherence\b|Valid\b|Named\b|'
        r'Factor\b|Feature\b|Process\b|Landform\b|Rock\b|Showing\b|Label)', re.I)
    for line in raw:
        new = bool(starts.search(line)) or (current and current.endswith(('.', ':', 'm', 'marks')))
        if current and new:
            paragraphs.append(current)
            current = line
        elif current:
            current = f'{current} {line}'
        else:
            current = line
    if current:
        paragraphs.append(current)
    return paragraphs


def part_two_scheme(year: int, level: str) -> dict[str, SchemeBlock]:
    with open(scheme_markdown_path(year, level), encoding='utf-8') as handle:
        text = handle.read().split('<!-- markbank:table-cells -->', 1)[0]
    page_markers = list(re.finditer(r'(?m)^## Page (\d+)\s*$', text))

    def page_for(offset: int) -> int:
        answer = 1
        for marker in page_markers:
            if marker.start() > offset:
                break
            answer = int(marker.group(1))
        return answer

    marker = re.compile(
        r'(?m)^((?:[1-9]|1[0-2])[ABC]|1[3-9]|2[0-4])\.\s+([^\n]+)')
    matches: list[re.Match[str]] = []
    seen: set[str] = set()
    for match in marker.finditer(text):
        ref = match.group(1)
        if ref in seen:
            continue
        seen.add(ref)
        matches.append(match)
    if len(matches) != PART_TWO_BASE[level]:
        raise AssertionError(
            f'{year} {level}: scheme found {len(matches)} task blocks, '
            f'expected {PART_TWO_BASE[level]}')

    out: dict[str, SchemeBlock] = {}
    for index, match in enumerate(matches):
        ref = match.group(1)
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        block = text[match.start():end]
        lines = paragraph_lines(block)
        # Drop the heading, retained separately as the card stem.
        if lines and re.match(rf'^{re.escape(ref)}\.\s+', lines[0]):
            lines[0] = re.sub(rf'^{re.escape(ref)}\.\s+[^.?!]+\.?\s*', '', lines[0], count=1)
            if not lines[0]:
                lines.pop(0)
        # Exact A answers follow the first printed sub-question.  Removing the
        # preceding article/table text keeps reveal concise without discarding
        # any answer/allocation pair. Map-sketch tasks have no (i), so retain
        # their published outline allocation in full.
        if ref.endswith('A'):
            first_part = next((i for i, line in enumerate(lines)
                               if re.match(r'^\(i\)', line, re.I)), None)
            if first_part is not None:
                lines = lines[first_part:]
        if not lines:
            raise AssertionError(f'{year} {level} {ref}: empty scheme guidance')
        out[ref] = SchemeBlock(page=page_for(match.start()), guidance=lines)
    return out


def paper_fileids() -> dict[tuple[int, str, int], str]:
    """Resolve from Paper Trail's index; no SEC filename is typed here."""
    source = """
import { resolvePaperFileid } from './scripts/markbank/paperIndex.mjs';
const out = {};
for (const year of YEARS_JSON) {
  for (const level of ['higher', 'ordinary']) {
    for (const part of [1, 2]) {
      out[`${year}:${level}:${part}`] = resolvePaperFileid(
        'geography', year, level, String(part));
    }
  }
}
process.stdout.write(JSON.stringify(out));
"""
    result = subprocess.run(
        ['node', '--input-type=module', '-e', source.replace('YEARS_JSON', json.dumps(list(YEARS)))],
        cwd=ROOT,
        check=True, capture_output=True, text=True)
    raw = json.loads(result.stdout)
    out: dict[tuple[int, str, int], str] = {}
    for year in YEARS:
        for level in LEVELS:
            for part in (1, 2):
                value = raw.get(f'{year}:{level}:{part}')
                if not value:
                    raise AssertionError(
                        f'Paper Trail has no Geography {year} {level} Part {part} file id')
                out[(year, level, part)] = value
    return out


def bullet_pool(question_text: str) -> tuple[int, list[str], tuple[int, int]] | None:
    lines = question_text.splitlines()
    bullets = [index for index, line in enumerate(lines) if line.startswith('• ')]
    if not bullets:
        return None
    # Only a contiguous final task pool is selectable. Earlier bullets in an A
    # source question are matching options or compulsory asks and are retained.
    groups: list[list[int]] = []
    for index in bullets:
        if not groups or index != groups[-1][-1] + 1:
            groups.append([index])
        else:
            groups[-1].append(index)
    for group in reversed(groups):
        lead = compact(' '.join(lines[max(0, group[0] - 4):group[0]]))
        match = re.search(
            r'(?:(any|the)\s+)?(one|two|three|four|1|2|3|4)\s+of\s+the\s+following',
            lead, re.I)
        if not match:
            continue
        word = match.group(2).lower()
        choose = {'one': 1, 'two': 2, 'three': 3, 'four': 4,
                  '1': 1, '2': 2, '3': 3, '4': 4}[word]
        items = [compact(lines[index][2:]) for index in group]
        if choose > len(items):
            raise AssertionError(f'choose {choose} from {items!r}')
        return choose, items, (group[0], group[-1])
    return None


@dataclass(frozen=True)
class Variant:
    slug: str
    label: str
    question_text: str
    requirements: list[str]
    selection_kind: str
    # Slugs of the combination cards this one card absorbs (choose-N pools).
    absorbs: tuple[str, ...] = ()


def split_i_ii(question_text: str) -> list[Variant] | None:
    if not re.search(r'Answer\s+\(i\)\s+or\s+\(ii\)', question_text, re.I):
        return None
    match_i = re.search(r'(?m)^\(i\)\s+', question_text)
    match_ii = re.search(r'(?mi)^Or\s*\n\(ii\)\s+|^\(ii\)\s+', question_text)
    if not match_i or not match_ii or match_ii.start() <= match_i.start():
        raise AssertionError(f'cannot split printed (i)/(ii): {question_text!r}')
    preamble = re.sub(
        r'Answer\s+\(i\)\s+or\s+\(ii\)\.?', '',
        question_text[:match_i.start()], flags=re.I).strip()
    first = question_text[match_i.start():match_ii.start()].strip()
    first = re.sub(r'(?mi)\s*\n?Or\s*$', '', first).strip()
    second = question_text[match_ii.start():].strip()
    second = re.sub(r'(?i)^Or\s*\n?', '', second).strip()
    return [
        Variant('route-i', 'Route (i)', '\n'.join(filter(None, (preamble, first))),
                ['Complete printed route (i).'], 'answer-i-or-ii'),
        Variant('route-ii', 'Route (ii)', '\n'.join(filter(None, (preamble, second))),
                ['Complete printed route (ii).'], 'answer-i-or-ii'),
    ]


def apply_inline_choices(variant: Variant) -> list[Variant]:
    variants = [variant]
    for pattern, choices in INLINE_CHOICES:
        next_variants: list[Variant] = []
        for current in variants:
            if not pattern.search(current.question_text):
                next_variants.append(current)
                continue
            for choice_slug, label in choices:
                next_variants.append(Variant(
                    slug='-'.join(filter(None, (current.slug, choice_slug))),
                    label=' · '.join(filter(None, (current.label, label))),
                    # The printed question stays verbatim; the option rides in
                    # questionRef and the task requirement.
                    question_text=current.question_text,
                    requirements=[*current.requirements, f'Use the printed route: {label}.'],
                    selection_kind=(current.selection_kind + '+inline-choice').strip('+'),
                ))
        variants = next_variants
    return variants


def apply_bullet_choices(variant: Variant) -> list[Variant]:
    pool = bullet_pool(variant.question_text)
    if pool is None:
        return [variant]
    choose, items, (first, last) = pool
    lines = variant.question_text.splitlines()
    out: list[Variant] = []
    if choose >= 2:
        # Choice is not a route: one card, the printed question verbatim with
        # every item. It keeps the first printed combination's id.
        combos = ['-'.join(slug(item, 34) for item in selected)
                  for selected in itertools.combinations(items, choose)]
        return [Variant(
            slug='-'.join(filter(None, (variant.slug, combos[0]))),
            label=variant.label,
            question_text=variant.question_text,
            requirements=list(variant.requirements),
            selection_kind=(variant.selection_kind
                            + f'+choose-{choose}-of-{len(items)}-one-card').strip('+'),
            absorbs=tuple('-'.join(filter(None, (variant.slug, combo))) for combo in combos[1:]),
        )]
    for selected in itertools.combinations(items, choose):
        labels = ' + '.join(selected)
        question_text = variant.question_text
        out.append(Variant(
            slug='-'.join(filter(None, (variant.slug, *[slug(item, 34) for item in selected]))),
            label=' · '.join(filter(None, (variant.label, labels))),
            question_text=question_text,
            requirements=[*variant.requirements,
                          f'Use the selected printed route: {labels}.'],
            selection_kind=(variant.selection_kind + f'+choose-{choose}-of-{len(items)}').strip('+'),
        ))
    return out


def apply_table_choices(variant: Variant) -> list[Variant]:
    """Expand the one closed choose-two pool printed as a table, not bullets."""
    phrase = re.compile(
        r'^Population dynamics Language Religion Urban development Rural development\s+'
        r'Examine the impact of any two of the factors listed in the table above',
        re.I,
    )
    if not phrase.search(variant.question_text):
        return [variant]
    items = (
        'Population dynamics', 'Language', 'Religion',
        'Urban development', 'Rural development',
    )
    # Choice is not a route: one card with the printed question verbatim,
    # the table's five printed cells on their own line above the ask.
    combos = ['-'.join(slug(item, 34) for item in selected)
              for selected in itertools.combinations(items, 2)]
    table = ' '.join(items)
    if not variant.question_text.startswith(table + ' '):
        raise AssertionError(f'table pool not printed as {table!r}')
    return [Variant(
        slug='-'.join(filter(None, (variant.slug, combos[0]))),
        label=variant.label,
        question_text=' · '.join(items) + '\n' + variant.question_text[len(table) + 1:],
        requirements=list(variant.requirements),
        selection_kind=(variant.selection_kind + '+choose-2-of-5-table-one-card').strip('+'),
        absorbs=tuple('-'.join(filter(None, (variant.slug, combo))) for combo in combos[1:]),
    )]


def variants_for(question_text: str) -> list[Variant]:
    initial = split_i_ii(question_text) or [Variant('', '', question_text, [], 'none')]
    expanded: list[Variant] = []
    for variant in initial:
        for inline in apply_inline_choices(variant):
            for tabular in apply_table_choices(inline):
                expanded.extend(apply_bullet_choices(tabular))
    # Stable uniqueness guards against overlapping patterns producing the same
    # card twice — the exact defect that previously duplicated Irish listening.
    unique: dict[tuple[str, str], Variant] = {}
    for variant in expanded:
        key = (variant.slug, comparable(variant.question_text))
        if key in unique:
            raise AssertionError(f'duplicate finite route {key!r}')
        unique[key] = variant
    return list(unique.values())


def topic_for(question: PaperQuestion) -> str:
    text = comparable(f'{question.title} {question.question_text}')
    if question.part == 2:
        if question.ref.isdigit():
            number = int(question.ref)
            if 13 <= number <= 15:
                return {'13': 'geography-5-1', '14': 'geography-5-2',
                        '15': 'geography-5-3'}.get(question.ref, 'geography-5-0')
            if 16 <= number <= 18:
                return 'geography-6-3' if number == 18 else (
                    'geography-6-2' if 'biome' in text else 'geography-6-1')
            if 19 <= number <= 21:
                return 'geography-7-1' if 'nation' in text else (
                    'geography-7-2' if 'identity' in text else 'geography-7-0')
            if 22 <= number <= 24:
                if 'climat' in text:
                    return 'geography-8-4'
                if 'economic' in text:
                    return 'geography-8-5'
                return 'geography-8-3'
        number = int(re.match(r'\d+', question.ref).group())
        if 1 <= number <= 3:
            strand = '0'
        elif 4 <= number <= 6:
            strand = '1'
        elif 7 <= number <= 9:
            strand = '3'
        else:
            strand = '4'
        if strand == '1':
            if 'irish region' in text:
                return 'geography-1-4'
            if 'european region' in text or 'european union' in text:
                return 'geography-1-5'
            if 'continental' in text:
                return 'geography-1-6'
            if 'culture' in text or 'urban region' in text:
                return 'geography-1-3'
            return 'geography-1-0'
        if strand == '3':
            if 'renewable' in text or 'energy' in text or 'fossil fuel' in text:
                return 'geography-3-5'
            if 'environment' in text or 'pollution' in text:
                return 'geography-3-4'
            if 'european union' in text or 'ireland and the eu' in text:
                return 'geography-3-3'
            if 'multinational' in text or 'global' in text or 'trade' in text:
                return 'geography-3-2'
            if 'developing' in text or 'colonial' in text:
                return 'geography-3-1'
            return 'geography-3-0'
        if strand == '4':
            if 'migration' in text or 'population movement' in text:
                return 'geography-4-2'
            if 'urban land' in text:
                return 'geography-4-4'
            if any(word in text for word in ('urban problem', 'urban sprawl', 'traffic congestion')):
                return 'geography-4-5'
            if any(word in text for word in ('settlement', 'urban function', 'site')):
                return 'geography-4-3'
            if 'development' in text or 'overpopulation' in text:
                return 'geography-4-1'
            return 'geography-4-0'

    if any(word in text for word in ('ordnance survey', 'map skills', 'grid reference')):
        return 'geography-2-6'
    if any(word in text for word in ('aerial photograph', 'satellite')):
        return 'geography-2-8'
    if any(word in text for word in ('weather chart', 'synoptic', 'isobar')):
        return 'geography-2-7'
    if any(word in text for word in ('graph', 'statistic', 'table', 'chart', 'data')):
        return 'geography-2-0'
    if 'tectonic' in text or 'plate boundary' in text or 'structure of the earth' in text:
        return 'geography-0-0'
    if 'rock' in text:
        return 'geography-0-1'
    if 'fold' in text or 'fault' in text:
        return 'geography-0-2'
    if 'karst' in text:
        return 'geography-0-3'
    if 'earthquake' in text or 'volcano' in text or 'volcanic' in text:
        return 'geography-0-7'
    if 'weathering' in text or 'mass movement' in text:
        return 'geography-0-8'
    if 'river' in text or 'fluvial' in text:
        return 'geography-0-9'
    if 'coast' in text or 'sea ' in text:
        return 'geography-0-10'
    if 'glacial' in text or 'glaciation' in text:
        return 'geography-0-11'
    if 'region' in text:
        return 'geography-1-0'
    return 'geography-0-4'


def question_page_source(
        question: PaperQuestion, year: int, level: str) -> dict[str, Any]:
    return {
        'kind': 'source-illustration',
        'label': f'PART {question.part} · Q{question.ref}',
        'title': 'Official question page',
        'pages': [question.page],
        'attribution': (
            f'State Examinations Commission Geography {LEVEL_REF[level]} '
            f'question paper {year} — © State Examinations Commission.'),
        'presentationNote': (
            'Official examination layout, reproduced page-for-page so every '
            'printed map, chart, photograph and source remains in context.'),
    }


# The separate official companions of each sitting (map extract, OS legend,
# aerial photograph), keyed by year. Identities come from Paper Trail's index;
# each was rendered and checked by eye before it was listed here.
COMPANIONS: dict[int, dict[str, str]] = {
    2026: {'place': 'Dundalk', 'map': 'LC005CLP003EV', 'legend': 'LC005CLPC00EV',
           'aerial': 'LC005CLP004EV'},
    # 2025's aerial photograph is published only as a JPEG image.
    2025: {'place': 'Oughterard', 'map': 'LC005CLP003EV', 'legend': 'LC005CLPC00EV',
           'aerial': 'LC005CLP004EV.jpg'},
    2024: {'place': 'Bantry', 'map': 'LC005CLP003EV', 'legend': 'LC005CLPC00EV',
           'aerial': 'LC005CLP004EV.jpg'},
    2023: {'place': 'Cavan', 'map': 'LC005CLP003EV', 'legend': 'LC005CLPC00EV',
           'aerial': 'LC005CLP004EV.jpg'},
    # 2022's legend and aerial photograph are both published only as JPEGs.
    2022: {'place': 'Clonmel', 'map': 'LC005CLP003EV', 'legend': 'LC005CLPC00EV.jpg',
           'aerial': 'LC005CLP004EV.jpg'},
    2021: {'place': 'Foxford', 'map': 'LC005CLP003EV', 'legend': 'LC005CLPC00EV',
           'aerial': 'LC005CLP004EV.jpg'},
    2020: {'place': 'Arklow', 'map': 'LC005CLP003EV', 'legend': 'LC005CLPC00EV',
           'aerial': 'LC005CLP004EV.jpg'},
    # 2019's map extract, like its aerial photograph, is published only as a JPEG.
    2019: {'place': 'Templemore', 'map': 'LC005CLP003EV.jpg', 'legend': 'LC005CLPC00EV',
           'aerial': 'LC005CLP004EV.jpg'},
    # 2018's map and legend are published only as JPEGs; Paper Trail files its
    # aerial photograph as the one-page PDF.
    2018: {'place': 'Sligo', 'map': 'LC005CLP003EV.jpg', 'legend': 'LC005CLPC00EV.jpg',
           'aerial': 'LC005CLP004EV'},
    # 2017's map extract is a one-page PDF holding a 1136 x 784 pixel image.
    2017: {'place': 'Macroom', 'map': 'LC005CLP003EV', 'legend': 'LC005CLPC00EV',
           'aerial': 'LC005CLP004EV'},
    # 2016's map extract is a one-page PDF holding a 1135 x 783 pixel image.
    2016: {'place': 'Westport', 'map': 'LC005CLP003EV', 'legend': 'LC005CLPC00EV',
           'aerial': 'LC005CLP004EV'},
    # 2015's legend and aerial photograph are stacked image strips in one-page PDFs.
    2015: {'place': 'Kenmare', 'map': 'LC005CLP003EV', 'legend': 'LC005CLPC00EV',
           'aerial': 'LC005CLP004EV'},
    # 2014's map extract is eight stacked image strips in a one-page PDF.
    2014: {'place': 'Dungarvan', 'map': 'LC005CLP003EV', 'legend': 'LC005CLPC00EV',
           'aerial': 'LC005CLP004EV'},
}


COMPANION_CACHE = os.path.join(ROOT, 'tmp', 'geography-audit', 'companions')
STORAGE = ('https://firebasestorage.googleapis.com/v0/b/nextstepuni-app.firebasestorage.app/o/'
           'papers%2Flc%2Fgeography%2F{year}%2Fpaper%2F{name}?alt=media')


def companion_path(year: int, fileid: str, fetch: bool = False) -> str:
    """The local copy of a companion: the harvested corpus, else a copy of the
    same Paper Trail storage object kept in a git-ignored cache. Its bytes are
    checked against the review ledger by the caller."""
    name = fileid if '.' in fileid else f'{fileid}.pdf'
    cached = os.path.join(COMPANION_CACHE, f'{year}-{name}')
    for path in (os.path.join(GR.CORPUS_ROOT, str(year), name), cached):
        if os.path.exists(path):
            return path
    if fetch:
        import urllib.request
        os.makedirs(COMPANION_CACHE, exist_ok=True)
        urllib.request.urlretrieve(STORAGE.format(year=year, name=name), cached)
        return cached
    raise AssertionError(
        f'{year} companion {name} is not available locally; run '
        'geography_cards.py --fetch-companions')


def companion_material(kind: str, year: int = 2026) -> dict[str, Any]:
    """One separate official companion document, shown as its own source."""
    files = COMPANIONS[year]
    if kind == 'map':
        return {
            'kind': 'source-illustration',
            'label': 'OS MAP',
            'title': 'Official 1:50 000 map extract',
            'pages': [1],
            'sourceFileid': files['map'],
            'attribution': (
                f'State Examinations Commission Geography {year} Ordnance '
                'Survey map — © State Examinations Commission.'),
            'presentationNote': (
                'The exact official map extract supplied with the '
                'examination, reproduced without retyping or alteration.'),
        }
    if kind == 'legend':
        return {
            'kind': 'source-illustration',
            'label': 'MAP LEGEND',
            'title': 'Official Ordnance Survey legend',
            'pages': [1],
            'sourceFileid': files['legend'],
            'attribution': (
                f'State Examinations Commission Geography {year} Ordnance '
                'Survey legend — © State Examinations Commission.'),
            'presentationNote': (
                'The exact official legend supplied with the examination, '
                'reproduced without retyping or alteration.'),
        }
    if kind == 'aerial':
        return {
            'kind': 'source-illustration',
            'label': 'AERIAL PHOTOGRAPH',
            'title': f"Official {files['place']} aerial photograph",
            'pages': [1],
            'sourceFileid': files['aerial'],
            'attribution': (
                f'State Examinations Commission Geography {year} aerial '
                'photograph — © State Examinations Commission.'),
            'presentationNote': (
                'The exact official examination photograph, preserved at its '
                'published resolution in a single-page reader document.'),
        }
    raise AssertionError(f'unknown companion {kind}')


def companion_sources(
        question: PaperQuestion, year: int) -> list[dict[str, Any]]:
    if year not in COMPANION_SOURCE_YEARS:
        return []
    text = question.question_text
    out: list[dict[str, Any]] = []
    if re.search(r'\bOrdnance Survey map\b', text, re.I):
        out.extend((companion_material('map'), companion_material('legend')))
    if re.search(r'\baerial photograph\b', text, re.I):
        out.append(companion_material('aerial'))
    return out


def source_materials(
        question: PaperQuestion, year: int, level: str) -> list[dict[str, Any]]:
    # The page is most useful for the visual/data short questions and structured
    # A tasks. A few B/C tasks also embed a table or photograph; detect those
    # from the printed wording so their evidence cannot disappear merely
    # because it sits outside the paper's usual position.
    sources: list[dict[str, Any]] = []
    if (question.part != 2 or question.ref.endswith('A')
            or EMBEDDED_SOURCE.search(question.question_text)):
        sources.append(question_page_source(question, year, level))
    companions = companion_sources(question, year)
    if EXTERNAL_SOURCE.search(question.question_text) and not companions:
        return []
    sources.extend(companions)
    return sources


def selection_directive(question_text: str) -> bool:
    return bool(re.search(
        r'Answer\s+\(i\)\s+or\s+\(ii\)|'
        r'(?:one|two|three|four)\s+of\s+the\s+following|'
        r'any\s+(?:one|two|three|four)\s+of\s+the\s+following|'
        r'one fluvial landform\s+or\s+one coastal landform|'
        r'impact of any two of the factors listed in the table above|'
        r'climate\s+or\s+geomorphology|'
        r'footloose industries\s+or\s+financial services\s+or\s+mass tourism',
        question_text, re.I))


def scheme_guidance_for_variant(guidance: list[str], variant: Variant) -> list[str]:
    """Keep only the marking branch belonging to an (i)/(ii) route card."""
    if 'answer-i-or-ii' not in variant.selection_kind:
        return list(guidance)
    first = next((index for index, line in enumerate(guidance)
                  if re.match(r'^\(i\)\s+', line, re.I)), None)
    divider = next((index for index, line in enumerate(guidance)
                    if first is not None and index > first
                    and re.match(r'^Or\b', line, re.I)), None)
    if first is None or divider is None:
        # Some scheme layouts omit a standalone Or but still print the second
        # branch. Find that second top-level marker after the first allocation.
        divider = next((index for index, line in enumerate(guidance)
                        if first is not None and index > first
                        and re.match(r'^\(ii\)\s+', line, re.I)), None)
    if first is None or divider is None:
        raise AssertionError(
            f'cannot split scheme guidance for {variant.label}: {guidance[:6]!r}')
    if re.match(r'^route-i(?:-|$)', variant.slug):
        return guidance[first:divider]
    second = divider + 1 if re.match(r'^Or\b', guidance[divider], re.I) else divider
    return guidance[second:]


def canonical_topic_ids() -> set[str]:
    """Outgoing-syllabus Geography node ids, read from curriculum.ts."""
    text = open(os.path.join(ROOT, 'curriculum.ts'), encoding='utf-8').read()
    start = text.rfind('{', 0, text.index('"id": "geography"'))
    depth = 0
    for index in range(start, len(text)):
        depth += {'{': 1, '}': -1}.get(text[index], 0)
        if depth == 0:
            subject = json.loads(text[start:index + 1])
            return {topic['id'] for strand in subject['strands']
                    for topic in strand['subtopics']}
    raise AssertionError('Geography curriculum not found')


def reviewed_sitting(year: int, level: str, review: Any,
                     fileids: dict[tuple[int, str, int], str],
                     topic_ids: set[str], crosswalk: dict[str, list[str]]) -> dict[str, Any]:
    """Cards, census rows, audit and Atlas rows for one independently reviewed sitting."""
    sitting = GR.Sitting.open(year, level)
    short = LEVEL_SHORT[level]
    for part, document in sitting.papers.items():
        if len(document) != review.PAPER_PAGES[part]:
            raise AssertionError(f'{year} {level} Part {part}: {len(document)} pages, '
                                 f'review covers {review.PAPER_PAGES[part]}')
        if sorted(review.PAGE_REVIEW[f'paper{part}']) != list(range(1, len(document) + 1)):
            raise AssertionError(f'{year} {level} Part {part}: unreviewed paper page')
    if len(sitting.scheme) != review.SCHEME_PAGES or sorted(
            review.PAGE_REVIEW['scheme']) != list(range(1, review.SCHEME_PAGES + 1)):
        raise AssertionError(f'{year} {level}: scheme page review incomplete')
    sources = {}
    for key, document in (('paper1', sitting.papers[1]), ('paper2', sitting.papers[2]),
                          ('scheme', sitting.scheme)):
        name, size = review.EXPECTED_SOURCES[key]
        if os.path.getsize(document.path) != size:
            raise AssertionError(f'{year} {level} {key}: bytes changed from {size}')
        sources[key] = {'fileid': name, 'bytes': size, 'sha256': GR.sha256(document.path),
                        'pages': len(document)}
    for part in (1, 2):
        if fileids[(year, level, part)] + '.pdf' != review.EXPECTED_SOURCES[f'paper{part}'][0]:
            raise AssertionError(f'{year} {level} Part {part}: Paper Trail file id changed')
    # A companion the SEC never published for a sitting is None in COMPANIONS
    # (2011 has no legend sheet); a task that names it then fails loudly below,
    # so the ledger must hold, not card, any task that depends on it.
    published = tuple(kind for kind in ('map', 'legend', 'aerial') if COMPANIONS[year][kind])
    for kind in published:
        path = companion_path(year, COMPANIONS[year][kind])
        sources[kind] = {'fileid': os.path.basename(path).split(f'{year}-')[-1],
                         'bytes': os.path.getsize(path),
                         'sha256': GR.sha256(path), 'pages': len(fitz.open(path))}
        expected = review.EXPECTED_SOURCES.get(kind)
        if expected and (sources[kind]['fileid'], sources[kind]['bytes']) != expected:
            raise AssertionError(f'{year} {level} {kind}: {sources[kind]} != {expected}')
    scan = GR.selection_scan(sitting)
    if scan != review.EXPECTED_SELECTION_SCAN:
        raise AssertionError(f'{year} {level}: unclassified or stale selection directives '
                             f'{scan!r}')
    classified = [item for entry in review.SELECTION_REVIEW for item in entry['scan']]
    if sorted(map(tuple, classified)) != sorted(map(tuple, scan)):
        raise AssertionError(f'{year} {level}: selection review does not classify the scan')

    companions = {kind: companion_material(kind, year) for kind in published}
    cards: list[dict[str, Any]] = []
    tasks_out, base_tasks, selection_rows = [], [], []
    absorbed_pairs: list[tuple[str, str]] = []
    totals: dict[tuple[int, str], int] = {}
    # Per printed question, each Atlas topic's share of the marks its reviewed
    # cards carry (alternative routes split their task's marks). Paper Trail
    # takes a question's primary and secondary syllabus nodes from the row's
    # order, so a question the shipped join already filed keeps its shipped
    # order and a question it omitted lists what it mostly examines first.
    atlas: dict[tuple[int, str], dict[str, float]] = {}
    for task in review.TASKS:
        task_cards = GR.build_task_cards(
            sitting, task, fileids[(year, level, task.part)], companions, topic_ids)
        for card in task_cards:
            card_topic = card['topicId']
            for atlas_id in card['atlasTopicIds']:
                if not atlas_id.startswith(f'geography-{level}-') or atlas_id not in crosswalk:
                    raise AssertionError(f"{card['id']}: {atlas_id} is not a {level} Atlas topic")
            if not any(card_topic in crosswalk[atlas_id] for atlas_id in card['atlasTopicIds']):
                raise AssertionError(f"{card['id']}: no Atlas topic covers {card_topic}")
        cards.extend(task_cards)
        totals[(task.part, task.question)] = totals.get((task.part, task.question), 0) + task.marks
        number = re.match(r'\d+', task.question).group()
        weights = atlas.setdefault((task.part, number), {})
        for card in task_cards:
            for atlas_id in card['atlasTopicIds']:
                weights[atlas_id] = weights.get(atlas_id, 0) + card['totalMarks'] / len(task_cards)
        ref = GR.ref_label(year, level, task)
        base_tasks.append({'id': task.card_id, 'year': year, 'level': level,
                           'part': task.part, 'questionRef': ref,
                           'title': task_cards[0]['stem'].split(' — ')[0],
                           'status': 'authored'})
        if task.routes:
            selection_rows.append({'questionRef': ref, 'classification': 'finite-expanded',
                                   'variants': len(task_cards),
                                   'kinds': ['reviewed-printed-route']})
        absorbed = [(old, task.card_id) for old in task.absorbs] + [
            (old, route.card_id) for route in task.routes for old in route.absorbs]
        if absorbed:
            selection_rows.append({'questionRef': ref, 'classification': 'single-card-choice',
                                   'variants': len(task_cards),
                                   'kinds': ['reviewed-choose-n-of-m'],
                                   'combinationsAbsorbed': len(absorbed)})
        absorbed_pairs.extend(absorbed)
        tasks_out.append({
            'key': task.key, 'questionRef': ref, 'marks': task.marks,
            'paperPage': task.page,
            'schemePages': sorted({piece.page for piece in task.scheme}
                                  | {piece.page for route in task.routes
                                     for piece in (route.scheme or ())}),
            'criteria': [{'label': c['label'], 'maxMarks': c['maxMarks']}
                         for c in task_cards[0]['criteria']],
            'topicIds': sorted({card['topicId'] for card in task_cards}),
            'atlasTopicIds': sorted({a for card in task_cards for a in card['atlasTopicIds']}),
            'sources': list(task.sources),
            **({'routeSources': {route.card_id: list(route.sources) for route in task.routes
                                 if route.sources is not None}}
               if any(route.sources is not None for route in task.routes) else {}),
            'cards': [card['id'] for card in task_cards],
            'routes': [route.label for route in task.routes],
        })
    # A printed part the ledger cannot card honestly (its published allocation
    # does not add up to its printed tariff) is held, never guessed at: it
    # stays in the census as excluded, with the ledger's reason.
    held = list(getattr(review, 'HELD', ()))
    excluded_rows = []
    for row in held:
        totals[(row['part'], row['question'])] = (
            totals.get((row['part'], row['question']), 0) + row['marks'])
        # A held row may name one separately priced part ('sub', e.g. '(iii)').
        sub = row.get('sub', '')
        key = sub.strip('()').replace(')(', '-')
        ref = f"{year} {LEVEL_REF[level]} Part {row['part']} Q{row['question']}{sub}"
        base_tasks.append({'id': ID_PREFIX.format(year=year, short=LEVEL_SHORT[level])
                           + f"p{row['part']}-q{row['question'].lower()}" + (f'-{key}' if key else ''),
                           'year': year, 'level': level, 'part': row['part'], 'questionRef': ref,
                           'title': row['title'], 'status': 'excluded'})
        excluded_rows.append({'year': year, 'level': level, 'part': row['part'],
                              'questionRef': row['question'] + sub, 'title': row['title'],
                              'reason': row['reason']})
    expected_totals = {(part, q): marks for part, row in review.QUESTION_TARIFFS.items()
                       for q, marks in row.items()}
    if totals != expected_totals:
        raise AssertionError(f'{year} {level}: task tariffs {totals} != printed {expected_totals}')
    ids = [card['id'] for card in cards]
    if len(ids) != len(set(ids)):
        raise AssertionError(f'{year} {level}: duplicate reviewed card id')
    legacy = set(review.LEGACY_IDS)
    # A shipped combination card that its choose-N question now absorbs keeps
    # its identity through a progress alias; a branch-only one simply goes.
    for old, _canonical in absorbed_pairs:
        if old in ids:
            raise AssertionError(f'{old}: absorbed by its choose-N card yet still emitted')
    aliases = {old: canonical for old, canonical in absorbed_pairs if old in legacy}
    if not legacy <= set(ids) | set(aliases):
        raise AssertionError(
            f'{year} {level}: lost legacy ids {sorted(legacy - set(ids) - set(aliases))}')
    flagged = {t.card_id for t in review.TASKS if t.legacy and not t.routes} | {
        r.card_id for t in review.TASKS for r in t.routes if r.legacy} | set(aliases)
    if flagged != legacy:
        raise AssertionError(f'{year} {level}: legacy flags disagree with LEGACY_IDS: '
                             f'{sorted(flagged ^ legacy)}')
    # A shipped id now held by one printed sub-part: the task's own id, and
    # every shipped route id of a routed sub-part (each is re-scoped alike).
    corrections = [{'id': card_id, 'nowQuestionRef': GR.ref_label(year, level, t),
                    'reason': review.ID_CORRECTION_REASON}
                   for t in review.TASKS if t.legacy and t.sub
                   for card_id in dict.fromkeys(
                       [t.card_id, *(r.card_id for r in t.routes if r.legacy)])]
    # Before 2020 one booklet printed both parts. Paper Trail and the shipped
    # join know that booklet's questions only as its Part Two numbers under
    # the paper key "single"; a Part One question has no question identity
    # there to file under (its cards still carry their own Atlas topics).
    single = fileids[(year, level, 1)] == fileids[(year, level, 2)]
    atlas_rows = [
        {'level': level, 'year': year, 'paperKey': 'single' if single else f'p{part}',
         'fileid': fileids[(year, level, part)] + '.pdf', 'n': n,
         'topicIds': sorted(weights, key=lambda topic: (-weights[topic], topic))}
        for (part, n), weights in sorted(atlas.items(), key=lambda kv: (kv[0][0], int(kv[0][1])))
        if not (single and part == 1)]
    audit = {
        'year': year, 'level': level, 'lang': 'ev', 'status': 'reviewed',
        'reviewedAt': '2026-10-11', 'sources': sources,
        'pageReview': review.PAGE_REVIEW, 'selectionScan': scan,
        'selectionReview': review.SELECTION_REVIEW,
        'questionTotals': {f'Part {p} Q{q}': m for (p, q), m in sorted(totals.items())},
        'taskCount': len(review.TASKS), 'cardCount': len(cards),
        'legacyIds': sorted(legacy), 'addedIds': sorted(set(ids) - legacy),
        'idCorrections': corrections,
        'aliases': [{'id': old, 'canonicalId': new} for old, new in sorted(aliases.items())],
        'tasks': tasks_out,
        **({'held': excluded_rows} if excluded_rows else {}),
        'rule': (review.__doc__ or '').strip(),
    }
    sitting_row = {'year': year, 'level': level, 'paperBaseTasks': len(review.TASKS) + len(held),
                   'includedBaseTasks': len(review.TASKS), 'excludedBaseTasks': len(held),
                   'authoredCardsAfterFiniteExpansion': len(cards), 'reviewed': True}
    return {'cards': cards, 'baseTasks': base_tasks, 'sitting': sitting_row,
            'selection': selection_rows, 'audit': audit, 'atlas': atlas_rows,
            'aliases': aliases, 'excluded': excluded_rows}


def make_corpus() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    fileids = paper_fileids()
    cards: list[dict[str, Any]] = []
    base_tasks: list[dict[str, Any]] = []
    sittings: list[dict[str, Any]] = []
    excluded: list[dict[str, Any]] = []
    selection_audit: list[dict[str, Any]] = []

    reviewed_audits: list[dict[str, Any]] = []
    atlas_rows: list[dict[str, Any]] = []
    aliases: dict[str, str] = {}
    topic_ids = canonical_topic_ids()
    with open(CROSSWALK, encoding='utf-8') as handle:
        crosswalk = json.load(handle)
    for year in YEARS:
        for level in LEVELS:
            if (year, level) in REVIEWED:
                built = reviewed_sitting(year, level, REVIEWED[(year, level)],
                                         fileids, topic_ids, crosswalk)
                cards.extend(built['cards'])
                base_tasks.extend(built['baseTasks'])
                sittings.append(built['sitting'])
                selection_audit.extend(built['selection'])
                aliases.update(built['aliases'])
                reviewed_audits.append(built['audit'])
                atlas_rows.extend(built['atlas'])
                excluded.extend(built['excluded'])
                continue
            if year not in CORE_YEARS:
                continue
            short_scheme = part_one_scheme(year, level)
            long_scheme = part_two_scheme(year, level)
            questions = [*part_one_questions(year, level),
                         *part_two_questions(year, level)]
            base_expected = 12 + PART_TWO_BASE[level]
            if len(questions) != base_expected:
                raise AssertionError(
                    f'{year} {level}: {len(questions)} base tasks, expected {base_expected}')
            before = len(cards)
            excluded_before = len(excluded)
            base_included = 0
            for question in questions:
                ref_label = (
                    f'{year} {LEVEL_REF[level]} Part {question.part} Q{question.ref}')
                base_task = {
                    'id': (
                        f'geography-{year}-{LEVEL_SHORT[level]}-p{question.part}-'
                        f'q{question.ref.lower()}'
                    ),
                    'year': year,
                    'level': level,
                    'part': question.part,
                    'questionRef': ref_label,
                    'title': question.title,
                }
                external_source = bool(EXTERNAL_SOURCE.search(question.question_text))
                if external_source and year not in COMPANION_SOURCE_YEARS:
                    base_tasks.append({**base_task, 'status': 'excluded'})
                    excluded.append({
                        'year': year, 'level': level, 'part': question.part,
                        'questionRef': question.ref, 'title': question.title,
                        'reason': (
                            'The printed task requires a separate Ordnance Survey '
                            'map or aerial photograph that is not present in the '
                            'official question-paper PDF held by Paper Trail.'),
                    })
                    continue
                if (GEOGRAPHY_SOURCE_REFERENCE.search(question.question_text)
                        and not external_source
                        and not EMBEDDED_OS_EXTRACT.search(question.question_text)):
                    raise AssertionError(
                        f'{ref_label}: map/aerial source reference is neither '
                        'classified as a separate companion nor as an embedded '
                        'question-page extract')
                base_included += 1
                base_tasks.append({**base_task, 'status': 'authored'})
                scheme = (short_scheme[int(question.ref)] if question.part == 1
                          else {'page': long_scheme[question.ref].page,
                                'guidance': long_scheme[question.ref].guidance})
                selectable_task = question.part == 2 and not question.ref.endswith('A')
                variants = (variants_for(question.question_text) if selectable_task
                            else [Variant('', '', question.question_text, [], 'none')])
                if (selectable_task and selection_directive(question.question_text)
                        and len(variants) == 1 and not variants[0].absorbs):
                    raise AssertionError(
                        f'{ref_label}: finite selection directive was not expanded')
                if len(variants) > 1:
                    selection_audit.append({
                        'questionRef': ref_label,
                        'classification': 'finite-expanded',
                        'variants': len(variants),
                        'kinds': sorted({variant.selection_kind for variant in variants}),
                    })
                absorbed = sum(len(variant.absorbs) for variant in variants)
                if absorbed:
                    selection_audit.append({
                        'questionRef': ref_label,
                        'classification': 'single-card-choice',
                        'variants': len(variants),
                        'kinds': sorted({variant.selection_kind for variant in variants}),
                        'combinationsAbsorbed': absorbed,
                    })
                for variant_index, variant in enumerate(variants, start=1):
                    # Q6C originally shipped as one unsplit card. Keep that
                    # stable id on its first now-explicit route so students'
                    # saved progress survives the finite-route correction.
                    preserve_legacy_id = (
                        year == 2021 and level == 'higher'
                        and question.part == 2 and question.ref == '6C'
                        and variant_index == 1
                    )
                    route_suffix = (
                        '' if preserve_legacy_id
                        else f'-{variant.slug}' if variant.slug else '')
                    card_id = (
                        f'geography-{year}-{LEVEL_SHORT[level]}-p{question.part}-'
                        f'q{question.ref.lower()}{route_suffix}')
                    for absorbed_slug in variant.absorbs:
                        aliases[(f'geography-{year}-{LEVEL_SHORT[level]}-p{question.part}-'
                                 f'q{question.ref.lower()}-{absorbed_slug}')] = card_id
                    topic_id = topic_for(question)
                    kind = ('exact' if question.part == 1 or question.ref.endswith('A')
                            else 'srp')
                    guidance = scheme_guidance_for_variant(
                        list(scheme['guidance']), variant)
                    if len(variants) > 1:
                        guidance = [
                            f'This card practises {variant.label or f"route {variant_index}"}.',
                            *guidance,
                        ]
                    sources = source_materials(question, year, level)
                    if external_source and not sources:
                        raise AssertionError(
                            f'{ref_label}: published companion source set is incomplete')
                    # A choose-N card keeps every printed item in its text.
                    display_question = (question_only_text(variant.question_text)
                                        if sources and not variant.absorbs
                                        else variant.question_text)
                    card: dict[str, Any] = {
                        'id': card_id,
                        'year': year,
                        'level': level,
                        'part': question.part,
                        'questionRef': (
                            ref_label if not variant.label
                            else f'{ref_label} · {variant.label}'),
                        'stem': question.title,
                        'questionText': display_question,
                        'paperPage': question.page,
                        'paperFileid': fileids[(year, level, question.part)],
                        'totalMarks': question.marks,
                        'schemePage': scheme['page'],
                        'topicId': topic_id,
                        'conceptId': (
                            f'geography-{topic_id.replace("geography-", "")}-'
                            f'{slug(question.title, 40)}'
                            f'{("-" + variant.slug) if variant.slug else ""}'),
                        'taskRequirements': variant.requirements,
                        'guidanceKind': kind,
                        'schemeGuidance': guidance,
                    }
                    if sources:
                        card['sourceMaterial'] = sources[0]
                    if len(sources) > 1:
                        card['additionalSourceMaterials'] = sources[1:]
                    cards.append(card)

            sitting_cards = len(cards) - before
            sittings.append({
                'year': year,
                'level': level,
                'paperBaseTasks': base_expected,
                'includedBaseTasks': base_included,
                'excludedBaseTasks': len(excluded) - excluded_before,
                'authoredCardsAfterFiniteExpansion': sitting_cards,
            })

    ids = [card['id'] for card in cards]
    if len(ids) != len(set(ids)):
        duplicate = next(card_id for card_id in ids if ids.count(card_id) > 1)
        raise AssertionError(f'duplicate Geography card id {duplicate}')
    if not cards:
        raise AssertionError('Geography corpus is empty')
    census = {
        'subjectId': 'geography',
        'years': list(YEARS),
        'levels': list(LEVELS),
        'paperBaseTasks': sum(row['paperBaseTasks'] for row in sittings),
        'includedBaseTasks': sum(row['includedBaseTasks'] for row in sittings),
        'excludedBaseTasks': len(excluded),
        'authoredCards': len(cards),
        'baseTasks': base_tasks,
        'sittings': sittings,
        'selectionAudit': selection_audit,
        'exclusions': excluded,
        'aliases': [{'id': old, 'canonicalId': new, 'reason': CHOICE_IS_NOT_A_ROUTE}
                    for old, new in sorted(aliases.items())],
        'rule': (
            'One Part One short question, one separately selectable Part Two '
            'A/B/C task, or one Higher-Level option is a base task. Every finite '
            'printed route is expanded; a choose-N-of-M pool (N >= 2) is one card '
            'with the printed question verbatim (choice is not a route). Tasks needing '
            'a missing separate OS map/aerial source are census-held, never '
            'presented as answerable. Independently reviewed sittings '
            '(geography-reviewed-audit.json) instead take one base task per '
            'separately priced printed part, from their review ledgers.'),
    }
    with open(REFERENCE_ATLAS, encoding='utf-8') as handle:
        reference = json.load(handle)
    shipped: dict[tuple[str, int, str, str, str], list[str]] = {}
    for level_code, lang_code, year, paper_key, fileid, n, indexes in reference['questionMappings']:
        if lang_code != 'e':
            continue
        key = ('higher' if level_code == 'h' else 'ordinary', year, paper_key, fileid, str(n))
        shipped.setdefault(key, []).extend(reference['topicIds'][i] for i in indexes)
    for row in atlas_rows:
        key = (row['level'], row['year'], row['paperKey'], row['fileid'], row['n'])
        # The shipped topics first, in the shipped order, then each topic the
        # review adds by weight: a review adds, never removes or reorders.
        row['topicIds'] = list(dict.fromkeys([*shipped.get(key, []), *row['topicIds']]))
    topic_list = sorted({topic for row in atlas_rows for topic in row['topicIds']})
    atlas = {
        'schemaVersion': 1,
        'subjectId': 'geography',
        'topicIds': topic_list,
        'questionMappings': [
            ['h' if row['level'] == 'higher' else 'o', 'e', row['year'], row['paperKey'],
             row['fileid'], row['n'], [topic_list.index(t) for t in row['topicIds']]]
            for row in atlas_rows],
    }
    audit = {
        'schemaVersion': 1, 'subjectId': 'geography',
        'scope': 'English (EV) editions; Irish editions are deferred.',
        'reviewedSittings': reviewed_audits,
    }
    return cards, census, audit, atlas


def serialised() -> tuple[str, str, str, str]:
    cards, census, audit, atlas = make_corpus()
    payload = {
        'meta': {
            'subjectId': 'geography',
            'years': list(YEARS),
            'levels': list(LEVELS),
            'cardCount': len(cards),
            'source': (
                'Official SEC Geography question papers and final marking '
                'schemes, 2021-2026.'),
            'authoredAt': '2026-08-31',
        },
        'cards': cards,
    }
    return (json.dumps(payload, ensure_ascii=False, indent=2) + '\n',
            json.dumps(census, ensure_ascii=False, indent=2) + '\n',
            json.dumps(audit, ensure_ascii=False, indent=2) + '\n',
            json.dumps(atlas, ensure_ascii=False, separators=(',', ':')) + '\n')


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--fetch-companions', action='store_true',
                        help='download reviewed sittings\' missing companions from Paper Trail storage')
    args = parser.parse_args()
    if args.fetch_companions:
        for year in sorted({year for year, _level in REVIEWED}):
            for kind in ('map', 'legend', 'aerial'):
                if COMPANIONS[year][kind]:
                    companion_path(year, COMPANIONS[year][kind], fetch=True)
    authored, census, audit, atlas = serialised()
    # The deck-size manifest is shared by every subject; only the Geography
    # entry is ours to restate.
    with open(SIZES, encoding='utf-8') as handle:
        sizes = json.load(handle)
    deck = json.loads(authored)['cards']
    sizes['geography'] = {level: sum(card['level'] == level for card in deck)
                          for level in LEVELS}
    outputs = ((OUT, authored), (CENSUS_OUT, census),
               (REVIEW_AUDIT_OUT, audit), (ATLAS_OUT, atlas),
               (SIZES, json.dumps(sizes, indent=1) + '\n'))
    if args.check:
        failures = []
        for path, expected in outputs:
            actual = ''
            if os.path.exists(path):
                with open(path, encoding='utf-8') as handle:
                    actual = handle.read()
            if actual != expected:
                failures.append(os.path.relpath(path, ROOT))
        if failures:
            print('Geography generated files are stale: ' + ', '.join(failures), file=sys.stderr)
            return 1
        print('Geography authored corpus is current.')
        return 0

    for path, text in outputs:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding='utf-8') as handle:
            handle.write(text)
    payload = json.loads(authored)
    summary = json.loads(census)
    reviewed = json.loads(audit)['reviewedSittings']
    print(
        f"Wrote {len(payload['cards'])} Geography cards from "
        f"{summary['includedBaseTasks']} answerable base tasks; "
        f"held {summary['excludedBaseTasks']} tasks (see census exclusions); "
        f"{len(reviewed)} independently reviewed sitting(s): "
        + ', '.join(f"{r['year']} {r['level']} {r['taskCount']} tasks/{r['cardCount']} cards"
                    for r in reviewed) + '.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
