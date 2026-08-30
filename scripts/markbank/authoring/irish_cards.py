#!/usr/bin/env python3
"""Build the complete 2021–2025 Irish Mark Bank corpus.

The question paper is the source of every prompt.  The marking scheme supplies
the published Eolas/Ábhar, Gaeilge, task/style and deduction grammar.  Printed
passages and poems remain PDF pages from Paper Trail; listening cards carry the
real SEC recording, never a transcript that would reveal the answers.

    python3 scripts/markbank/authoring/irish_cards.py
    python3 scripts/markbank/authoring/irish_cards.py --check

One card is one independently selectable response opportunity.  Linked parts
which the candidate must answer together stay together.  This produces exactly
400 cards across twenty papers:

  * 215 Higher Level (17 Paper 1 + 26 Paper 2 per year)
  * 185 Ordinary Level (15 Paper 1 + 22 Paper 2 per year)

The generated runtime JSON and the census ledger are committed because the
authoring PDFs are deliberately gitignored.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import unicodedata
from dataclasses import dataclass
from difflib import SequenceMatcher
from typing import Iterable, Sequence

import fitz


ROOT = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))
PAPER_ROOT = os.path.join(ROOT, 'examiner-reports', 'irish', 'papers')
OUT = os.path.join(ROOT, 'components', 'MarkBank', 'cards', 'irish', 'authored.json')
CENSUS_OUT = os.path.join(ROOT, 'scripts', 'markbank', 'authored', 'irish-census.json')
SCHEME_TEXT_ROOT = os.path.join(ROOT, 'examiner-reports', 'irish', 'schemes')
YEARS = tuple(range(2021, 2026))

SPACE_CHARS = ('\xa0', '\u2007', '\u202f')
LIGATURES = {
    '\u00ad': '', '\ufb00': 'ff', '\ufb01': 'fi', '\ufb02': 'fl',
    '\ufb03': 'ffi', '\ufb04': 'ffl',
}

LEVEL_SHORT = {'higher': 'hl', 'ordinary': 'ol'}
LEVEL_IRISH = {'higher': 'Ardleibhéal', 'ordinary': 'Gnáthleibhéal'}

PROSE_TOPICS = {
    'oisín i dtír na nóg': 'irish-4-1',
    'an gnáthrud': 'irish-4-2',
    'seal i neipeal': 'irish-4-3',
    'dís': 'irish-4-4',
    'hurlamaboc': 'irish-4-5',
    'cáca milis': 'irish-4-6',
    'an lasair choille': 'irish-4-8',
}
POETRY_TOPICS = {
    'an spailpín fánach': 'irish-5-1',
    'géibheann': 'irish-5-2',
    'an tearrach thiar': 'irish-5-3',
    'mo ghrá-sa': 'irish-5-4',
    'colscaradh': 'irish-5-5',
}
ADDITIONAL_TOPICS = {
    'an triail': 'irish-6-0',
    'a thig ná tit orm': 'irish-6-1',
    'tóraíocht dhiarmada': 'irish-6-2',
    'gafa': 'irish-6-3',
    'canary wharf': 'irish-6-4',
    'caoineadh airt uí laoghaire': 'irish-6-6',
    'fill arís': 'irish-6-7',
    'a chlann': 'irish-6-8',
    'colmáin': 'irish-6-9',
    'éiceolaí': 'irish-6-10',
}

AUDIO = {
    2025: 'https://educateplus.ie/sites/default/files/2025_6.mp3',
    2024: 'https://educateplus.ie/sites/default/files/2024_6.mp3',
    2023: 'https://educateplus.ie/sites/default/files/2023_4.mp3',
    2022: 'https://educateplus.ie/sites/default/files/2022_5.mp3',
}
AUDIO_2021 = {
    'A': 'https://educateplus.ie/sites/default/files/2021%20LC%20Irish%20Cuid%20A.mp3',
    'B': 'https://educateplus.ie/sites/default/files/2021%20LC%20Irish%20Cuid%20B.mp3',
    'C': 'https://educateplus.ie/sites/default/files/2021%20LC%20Irish%20Cuid%20C.mp3',
}


def clean_unicode(value: str) -> str:
    for char in SPACE_CHARS:
        value = value.replace(char, ' ')
    for bad, good in LIGATURES.items():
        value = value.replace(bad, good)
    return value.replace('‐', '-').replace('‑', '-').replace('‒', '-').replace('−', '-')


def compact(value: str) -> str:
    return re.sub(r'\s+', ' ', clean_unicode(value)).strip()


def comparable(value: str) -> str:
    value = unicodedata.normalize('NFKC', clean_unicode(value)).lower()
    value = value.replace('’', "'").replace('‘', "'").replace('ʼ', "'")
    value = value.replace('“', '"').replace('”', '"').replace('–', '-').replace('—', '-')
    return re.sub(r'[^\w]+', ' ', value, flags=re.UNICODE).strip()


def slug(value: str) -> str:
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z0-9]+', '-', value).strip('-')


def clean_lines(value: str, *, drop_answer_slots: bool = True) -> str:
    """Remove page furniture while preserving the paper's wording and labels."""
    lines: list[str] = []
    for raw in clean_unicode(value).splitlines():
        line = compact(raw)
        if not line:
            lines.append('')
            continue
        if re.match(r'^Scrúdú na hArdteistiméireachta,?\s*20\d{2}\b', line, re.I):
            continue
        if re.match(r'^Gaeilge(?:,|\s)[^\n]*(?:Ardleibhéal|Gnáthleibhéal)\s*$', line, re.I):
            continue
        if re.match(r'^\d{1,2}\s*$', line):
            continue
        if re.match(r'^(?:Leathanach Bán|Níl (?:aon |ábhar ).*leathanach seo)$', line, re.I):
            continue
        if re.fullmatch(r'[_\-–—\s]+', line):
            continue
        if drop_answer_slots and re.fullmatch(r'\((?:i|ii|iii|iv)\)', line, re.I):
            continue
        if re.match(r'^Cuid I\s+An Chluastuiscint\s+60 marc', line, re.I):
            continue
        if re.match(r'^Cuid II\s+An Cheapadóireacht\s+100 marc', line, re.I):
            continue
        lines.append(line)
    value = '\n'.join(lines)
    value = re.sub(r'\n{3,}', '\n\n', value)
    return value.strip()


def prompt_text(value: str) -> str:
    value = clean_lines(value)
    value = re.sub(r'(?m)^nó\s*$', '', value, flags=re.I)
    value = re.sub(r'\s+([?.!,;:])', r'\1', value)
    value = re.sub(r'\n{2,}', '\n', value)
    return compact(value)


def page_texts(path: str) -> list[str]:
    document = fitz.open(path)
    return [clean_unicode(page.get_text()) for page in document]


@dataclass
class PagedText:
    pages: list[str]

    def __post_init__(self) -> None:
        chunks: list[str] = []
        self.offsets: list[int] = []
        cursor = 0
        for page in self.pages:
            self.offsets.append(cursor)
            chunks.append(page)
            cursor += len(page) + 2
        self.text = '\n\n'.join(chunks)

    def page_for_offset(self, offset: int) -> int:
        page = 1
        for index, start in enumerate(self.offsets):
            if start > offset:
                break
            page = index + 1
        return page


def paper_path(year: int, level: str, paper: int) -> str:
    return os.path.join(PAPER_ROOT, f'{year}-{LEVEL_SHORT[level]}-{paper}00-paper.pdf')


def scheme_path(year: int, level: str) -> str:
    return os.path.join(PAPER_ROOT, f'{year}-{LEVEL_SHORT[level]}-scheme.pdf')


def find_matches(text: str, pattern: str, start: int = 0) -> list[re.Match[str]]:
    return list(re.finditer(pattern, text[start:], flags=re.I | re.M))


def slice_section(
    text: str,
    start_pattern: str,
    end_patterns: Sequence[str],
    *,
    last: bool = False,
    include_heading: bool = False,
) -> tuple[str, int]:
    matches = find_matches(text, start_pattern)
    if not matches:
        raise AssertionError(f'missing section marker {start_pattern!r}')
    match = matches[-1] if last else matches[0]
    absolute_start = match.start() if include_heading else match.end()
    end = len(text)
    for pattern in end_patterns:
        candidate = re.search(pattern, text[match.end():], flags=re.I | re.M)
        if candidate:
            end = min(end, match.end() + candidate.start())
    return text[absolute_start:end], absolute_start


def split_options(value: str, labels: Sequence[str]) -> list[tuple[str, str, int]]:
    wanted = set(labels)
    matches = [match for match in re.finditer(
        r'(?m)^\s*\(([a-ziv]+)\)\s*', value, re.I)
        if match.group(1).lower() in wanted]
    # Retain the first ordered run.  A nested (a) inside an (i) question must not
    # become a new selectable response.
    ordered: list[re.Match[str]] = []
    cursor = 0
    for label in labels:
        candidate = next((match for match in matches[cursor:]
                          if match.group(1).lower() == label), None)
        if candidate is None:
            raise AssertionError(f'missing option ({label}) in {compact(value)[:500]}')
        ordered.append(candidate)
        cursor = matches.index(candidate) + 1
    out: list[tuple[str, str, int]] = []
    for index, match in enumerate(ordered):
        end = ordered[index + 1].start() if index + 1 < len(ordered) else len(value)
        out.append((match.group(1).lower(), value[match.end():end], match.start()))
    return out


def numbered_questions(value: str, count: int) -> list[tuple[int, str, int]]:
    matches = list(re.finditer(r'(?m)^\s*(\d+)\.\s*\(a\)\s*', value, re.I))
    ordered: list[re.Match[str]] = []
    next_number = 1
    for match in matches:
        if int(match.group(1)) == next_number:
            ordered.append(match)
            next_number += 1
            if next_number > count:
                break
    if len(ordered) != count:
        raise AssertionError(
            f'expected {count} numbered questions, found {len(ordered)} in {compact(value)[:700]}')
    out = []
    for index, match in enumerate(ordered):
        end = ordered[index + 1].start() if index + 1 < len(ordered) else len(value)
        out.append((int(match.group(1)), '(a) ' + value[match.end():end], match.start()))
    return out


def mark_tokens(value: str) -> list[re.Match[str]]:
    return list(re.finditer(r'\(\s*\d+\s+mh?arc(?:anna)?\s*\)', value, re.I))


def cut_after_n_marks(value: str, count: int) -> str:
    marks = mark_tokens(value)
    if len(marks) < count:
        return value
    return value[:marks[count - 1].end()]


def range_marks(maximum: int, *, even: bool = False) -> list[int]:
    step = 2 if even else 1
    return [0, *range(step, maximum + 1, step)]


def normalised_with_map(value: str) -> tuple[str, list[int]]:
    out: list[str] = []
    positions: list[int] = []
    in_space = True
    for index, char in enumerate(clean_unicode(value)):
        char = unicodedata.normalize('NFKC', char).lower()
        for unit in char:
            if unit.isalnum() or unit == '_':
                out.append(unit)
                positions.append(index)
                in_space = False
            elif not in_space:
                out.append(' ')
                positions.append(index)
                in_space = True
    if out and out[-1] == ' ':
        out.pop()
        positions.pop()
    return ''.join(out), positions


def best_scheme_page(prompt: str, pages: Sequence[str]) -> tuple[int, int, str]:
    words = comparable(prompt).split()
    if len(words) < 4:
        raise AssertionError(f'prompt too short for scheme trace: {prompt!r}')
    width = min(8, len(words))
    grams = [' '.join(words[index:index + width])
             for index in range(max(1, len(words) - width + 1))]
    scored: list[tuple[int, int, int]] = []
    comparable_pages = [comparable(page) for page in pages]
    for index, page in enumerate(comparable_pages):
        shared = sum(gram in page for gram in grams)
        longest = SequenceMatcher(None, comparable(prompt), page, autojunk=False) \
            .find_longest_match().size
        scored.append((shared, longest, -index))
    shared, longest, negative_index = max(scored)
    page_index = -negative_index
    if shared == 0 and longest < min(26, max(15, len(comparable(prompt)) // 8)):
        raise AssertionError(
            f'no scheme trace (best p.{page_index + 1}, shared={shared}, longest={longest}): {prompt}')
    return page_index + 1, shared * 1000 + longest, pages[page_index]


def excerpt_from_prompt(page: str, prompt: str, maximum: int = 2600) -> str:
    normalised, positions = normalised_with_map(page)
    words = comparable(prompt).split()
    width = min(8, len(words))
    hit = -1
    for index in range(max(1, len(words) - width + 1)):
        gram = ' '.join(words[index:index + width])
        candidate = normalised.find(gram)
        if candidate >= 0:
            hit = candidate
            break
    if hit < 0:
        return clean_lines(page, drop_answer_slots=False)[:maximum]
    raw = positions[hit]
    start = page.rfind('\n', 0, raw) + 1
    return clean_lines(page[start:start + maximum], drop_answer_slots=False)


def chunk_guide(value: str, *, indicative: bool = False) -> list[str]:
    value = clean_lines(value, drop_answer_slots=False)
    value = re.sub(r'(?m)^\s*(?:nó|Nó)\s*$', '', value)
    value = compact(value)
    if not value:
        return []
    if indicative:
        marker = re.search(r'\b(?:Nótaí tacaíochta|Pointí eolais (?:féideartha|samplacha))\b', value, re.I)
        if marker:
            value = value[:min(len(value), marker.start() + 1550)]
        else:
            value = value[:1700]
    else:
        value = value[:2200]

    # Keep complete phrases together but stop one scheme excerpt becoming an
    # unreadable wall.  The source remains cited page-for-page beneath the card.
    sentences = re.split(r'(?<=[.;!?])\s+(?=[A-ZÁÉÍÓÚÀÈÌÒÙÂÊÎÔÛ(a-z0-9•])', value)
    chunks: list[str] = []
    current = ''
    for sentence in sentences:
        sentence = compact(sentence)
        if not sentence:
            continue
        if current and len(current) + len(sentence) + 1 > 430:
            chunks.append(current)
            current = sentence
        else:
            current = compact(current + ' ' + sentence)
    if current:
        chunks.append(current)
    return chunks[:8]


def trace_prompt_on_pages(prompt: str, pages: Sequence[str], candidates: Iterable[int]) -> tuple[int, int]:
    words = comparable(prompt).split()
    width = min(7, len(words))
    grams = [' '.join(words[index:index + width])
             for index in range(max(1, len(words) - width + 1))]
    scored = []
    for page_no in candidates:
        page = comparable(pages[page_no - 1])
        shared = sum(gram in page for gram in grams)
        longest = SequenceMatcher(None, comparable(prompt), page, autojunk=False) \
            .find_longest_match().size
        scored.append((shared, longest, -page_no))
    shared, longest, neg_page = max(scored)
    if shared == 0 and longest < 16:
        raise AssertionError(f'no question-paper trace: {prompt}')
    return -neg_page, shared * 1000 + longest


def title_topic(question: str, mapping: dict[str, str], fallback: str) -> str:
    normal = comparable(question)
    for title, topic in mapping.items():
        if comparable(title) in normal:
            return topic
    return fallback


def source_material(label: str, title: str, pages: list[int]) -> dict:
    return {
        'kind': 'source-text',
        'label': label,
        'title': title,
        'pages': pages,
        'attribution': 'Official source as printed in the State Examinations Commission question paper.',
        'presentationNote': 'Shown page-for-page from the official examination paper; swipe to move between pages.',
    }


def audio_material(year: int, section: str, label: str) -> dict:
    playback = AUDIO_2021[section] if year == 2021 else AUDIO[year]
    fileid = 'LC001ZLP017IV.mp3'
    return {
        'kind': 'source-audio',
        'label': label,
        'title': f'Triail Chluastuisceana {year}',
        'playbackUrl': playback,
        'secFileid': fileid,
        'canonicalUrl': f'https://www.examinations.ie/archive/exampapers/{year}/{fileid}',
        'attribution': '© State Examinations Commission. Verified playback mirror: Educateplus.',
        'presentationNote': 'Play the official recording and use the section heading on this card to follow the correct part.',
    }


def criterion(
    identifier: str,
    label: str,
    maximum: int,
    guidance: list[str],
    *,
    guidance_kind: str,
    kind: str = 'award',
    permitted: list[int] | None = None,
) -> dict:
    return {
        'id': identifier,
        'label': label,
        'kind': kind,
        'maxMarks': maximum,
        'permittedMarks': permitted if permitted is not None else range_marks(maximum),
        'guidanceKind': guidance_kind,
        'guidance': guidance,
    }


def base_card(
    *, year: int, level: str, paper: int, section: str, key: str,
    ref: str, question: str, total: int, topic: str, concept: str,
    paper_pages: Sequence[str], candidate_pages: Iterable[int], scheme_page: int,
    scheme_trace: int, criteria: list[dict], requirements: list[str],
    guide_note: str, source: dict | None = None, audio: dict | None = None,
) -> dict:
    page, paper_trace = trace_prompt_on_pages(question, paper_pages, candidate_pages)
    card = {
        'id': f'irish-{year}-{LEVEL_SHORT[level]}-p{paper}-{key}',
        'year': year,
        'level': level,
        'paper': paper,
        'section': section,
        'questionRef': ref,
        'questionText': question,
        'totalMarks': total,
        'topicId': topic,
        'conceptId': concept,
        'paperPage': page,
        'paperTraceScore': paper_trace,
        'schemePage': scheme_page,
        'schemeTraceScore': scheme_trace,
        'taskRequirements': list(dict.fromkeys(requirements)),
        'criteria': criteria,
        'markingGuideNote': guide_note,
    }
    if source:
        card['sourceMaterial'] = source
    if audio:
        card['audioMaterial'] = audio
    return card


def find_last_section(document: PagedText, heading: str, end_headings: Sequence[str]) -> tuple[str, int]:
    body, offset = slice_section(
        document.text, heading, end_headings, last=True, include_heading=True)
    return body, document.page_for_offset(offset)


def listening_total(segment: str, fallback: int | None = None) -> int:
    match = re.search(r'\(\s*(\d+)\s+mh?arc(?:anna)?\s*\)', segment, re.I)
    if match:
        return int(match.group(1))
    if fallback is not None:
        return fallback
    raise AssertionError(f'no listening total in scheme segment: {compact(segment)[:300]}')


def answer_slots(prompt: str) -> int:
    """Count HL two-mark information slots in one conversation half."""
    numbered = len(re.findall(r'(?m)^\s*\d+\.', clean_lines(prompt)))
    extras = len(re.findall(
        r'\b(?:scríobh síos|luaigh|tabhair|cén)\s+(?:an\s+)?d(?:á|há)\b',
        comparable(prompt), re.I))
    return numbered + extras


def listening_cards(year: int, level: str, paper_pages: list[str], scheme_pages: list[str]) -> list[dict]:
    # 2021 prints Cuid A on page 2; later booklets place it on page 3.
    paper_doc = PagedText(paper_pages[1:6])
    scheme_doc = PagedText(scheme_pages)
    cards: list[dict] = []
    level_ref = 'HL' if level == 'higher' else 'OL'

    def bounded_scheme(value: str) -> str:
        """Stop at annotation keys or the following composition rubric."""
        boundaries = [
            r'(?mi)^\s*(?:Na\s+)?Siombailí\s+Anótála',
            r'(?mi)^\s*Stíl\s+chuí\s+scríbhneoireachta',
            r'(?mi)^\s*An\s+Cumas\s+Gaeilge\s*\(\s*(?:40|80)\s+marc',
            r'(?mi)^\s*Cumas\s+agus\s+Cruinneas\s+Gaeilge',
        ]
        cuts = [match.start() for pattern in boundaries
                if (match := re.search(pattern, value))]
        return value[:min(cuts)] if cuts else value

    # The 2021 OL scheme prints the Fógra a hAon grid answers after the Fógra
    # a Dó answers.  Preserve that official layout while assigning each answer
    # only to the card it belongs to.
    f1_grid_answers = ''
    f2_grid_cut: int | None = None
    if year == 2021 and level == 'ordinary':
        f2_whole, _ = find_last_section(
            scheme_doc, r'FÓGRA\s+A\s+DÓ', [r'Cuid\s+B', r'COMHRÁ\s+A\s+hAON'])
        marker = re.search(r'Cén\s+ollscoil\s+a\s+chuir\s+amach\s+an\s+fógra\s+seo', f2_whole, re.I)
        if not marker:
            raise AssertionError('2021 OL: Fógra a hAon grid answers missing')
        f2_grid_cut = marker.start()
        f1_grid_answers = f2_whole[marker.start():]

    groups = [
        ('a-f1', 'A', r'FÓGRA\s+A\s+hAON', [r'FÓGRA\s+A\s+DÓ'], 'Fógra a hAon', 'irish-1-0'),
        ('a-f2', 'A', r'FÓGRA\s+A\s+DÓ', [r'Cuid\s+B', r'COMHRÁ\s+A\s+hAON'], 'Fógra a Dó', 'irish-1-0'),
        ('c-p1', 'C', r'PÍOSA\s+A\s+hAON', [r'PÍOSA\s+A\s+DÓ'], 'Píosa a hAon', 'irish-1-2'),
        ('c-p2', 'C', r'PÍOSA\s+A\s+DÓ', [r'Cuid\s+II', r'An Cheapadóireacht'], 'Píosa a Dó', 'irish-1-2'),
    ]
    for key, section, start, ends, title, topic in groups:
        paper_body, _ = slice_section(paper_doc.text, start, ends)
        question = prompt_text(paper_body)
        scheme_body, scheme_page = find_last_section(scheme_doc, start, ends)
        if key == 'a-f1' and f1_grid_answers:
            scheme_body += '\n' + f1_grid_answers
        if key == 'a-f2' and f2_grid_cut is not None:
            scheme_body = scheme_body[:f2_grid_cut]
        scheme_body = bounded_scheme(scheme_body)
        fallback = 12 if level == 'ordinary' and section == 'A' else \
            6 if level == 'ordinary' and section == 'C' else None
        total = listening_total(scheme_body, fallback)
        guide = chunk_guide(scheme_body)
        cards.append(base_card(
            year=year, level=level, paper=1, section='1', key=f'listening-{key}',
            ref=f'{year} {level_ref} Paper 1 Cluastuiscint Cuid {section} · {title}',
            question=question, total=total, topic=topic,
            concept=f'irish-listening-{key}', paper_pages=paper_pages,
            candidate_pages=range(2, 7), scheme_page=scheme_page,
            scheme_trace=len(comparable(scheme_body)),
            criteria=[criterion('eolas', 'Tuiscint / Eolas', total, guide, guidance_kind='exact')],
            requirements=['Éist leis an taifeadadh oifigiúil.', 'Freagair gach mír atá priontáilte ar an gcárta.'],
            guide_note='The listed responses and tariffs come from the same year’s SEC marking scheme. Equivalent wording is accepted where the scheme permits it.',
            audio=audio_material(year, section, f'Cuid {section} · {title}'),
        ))

    conversation_specs = [
        ('b-c1', r'COMHRÁ\s+A\s+hAON', [r'COMHRÁ\s+A\s+DÓ'], 'Comhrá a hAon'),
        ('b-c2', r'COMHRÁ\s+A\s+DÓ', [r'Cuid\s+C', r'PÍOSA\s+A\s+hAON'], 'Comhrá a Dó'),
    ]
    for key, start, ends, title in conversation_specs:
        paper_conversation, _ = slice_section(paper_doc.text, start, ends)
        scheme_conversation, scheme_offset = slice_section(
            scheme_doc.text, start, ends, last=True, include_heading=True)
        scheme_conversation = bounded_scheme(scheme_conversation)
        if level == 'higher':
            paper_first, _ = slice_section(
                paper_conversation, r'An\s+Chéad\s+Mhír', [r'An\s+Dara\s+Mír'])
            paper_second, _ = slice_section(
                paper_conversation, r'An\s+Dara\s+Mír', [])
            scheme_first, first_local = slice_section(
                scheme_conversation, r'An\s+Chéad\s+Mhír', [r'An\s+Dara\s+Mír'])
            scheme_second, second_local = slice_section(
                scheme_conversation, r'An\s+Dara\s+Mír', [])
            halves = [
                ('first', 'An Chéad Mhír', paper_first, scheme_first, first_local),
                ('second', 'An Dara Mír', paper_second, scheme_second, second_local),
            ]
            totals: list[int] = []
            for suffix, half_title, paper_half, scheme_half, local_offset in halves:
                question = prompt_text(paper_half)
                total = answer_slots(paper_half) * 2
                totals.append(total)
                scheme_page = scheme_doc.page_for_offset(scheme_offset + local_offset)
                cards.append(base_card(
                    year=year, level=level, paper=1, section='1',
                    key=f'listening-{key}-{suffix}',
                    ref=f'{year} {level_ref} Paper 1 Cluastuiscint Cuid B · {title} · {half_title}',
                    question=question, total=total, topic='irish-1-1',
                    concept=f'irish-listening-{key}-{suffix}', paper_pages=paper_pages,
                    candidate_pages=range(2, 7), scheme_page=scheme_page,
                    scheme_trace=len(comparable(scheme_half)),
                    criteria=[criterion(
                        'eolas', 'Tuiscint / Eolas', total, chunk_guide(scheme_half),
                        guidance_kind='exact')],
                    requirements=['Éist leis an taifeadadh oifigiúil.', 'Freagair gach mír atá priontáilte ar an gcárta.'],
                    guide_note='The listed responses and tariffs come from the same year’s SEC marking scheme. Equivalent wording is accepted where the scheme permits it.',
                    audio=audio_material(year, 'B', f'Cuid B · {title} · {half_title}'),
                ))
            if sum(totals) != 14:
                raise AssertionError(f'{year} HL {title}: conversation halves total {totals}, expected 14')
        else:
            question = prompt_text(paper_conversation)
            scheme_page = scheme_doc.page_for_offset(scheme_offset)
            total = listening_total(scheme_conversation, 12)
            cards.append(base_card(
                year=year, level=level, paper=1, section='1', key=f'listening-{key}',
                ref=f'{year} {level_ref} Paper 1 Cluastuiscint Cuid B · {title}',
                question=question, total=total, topic='irish-1-1',
                concept=f'irish-listening-{key}', paper_pages=paper_pages,
                candidate_pages=range(2, 7), scheme_page=scheme_page,
                scheme_trace=len(comparable(scheme_conversation)),
                criteria=[criterion(
                    'eolas', 'Tuiscint / Eolas', total, chunk_guide(scheme_conversation),
                    guidance_kind='exact')],
                requirements=['Éist leis an taifeadadh oifigiúil.', 'Freagair gach mír atá priontáilte ar an gcárta.'],
                guide_note='The listed responses and tariffs come from the same year’s SEC marking scheme. Equivalent wording is accepted where the scheme permits it.',
                audio=audio_material(year, 'B', f'Cuid B · {title}'),
            ))

    expected = 8 if level == 'higher' else 6
    if len(cards) != expected:
        raise AssertionError(f'{year} {level}: {len(cards)} listening cards, expected {expected}')
    return cards


def composition_scheme(year: int, level: str, scheme_pages: list[str]) -> tuple[int, list[dict]]:
    if level == 'higher':
        page = next((index + 1 for index, text in enumerate(scheme_pages)
                     if 'Stíl chuí scríbhneoireachta' in text), None)
        if page is None:
            raise AssertionError(f'{year} HL: composition rubric page missing')
        criteria = [
            criterion('stil', 'Stíl chuí scríbhneoireachta', 5,
                      ['5 marks where the required writing style is used; 0 where a different form is substituted.'],
                      guidance_kind='quality', permitted=[0, 5]),
            criterion('abhar', 'Ábhar', 15,
                      ['Valid, worthwhile content based on the chosen title, with a definite continuous connection between title and response.'],
                      guidance_kind='indicative'),
            criterion('gaeilge', 'Cumas Gaeilge', 80,
                      ['Fairsinge agus saibhreas stór Gaeilge; beachtas agus cruinneas in grammar, syntax, structure and word formation.'],
                      guidance_kind='quality'),
        ]
        return page, criteria

    page = next((index + 1 for index, text in enumerate(scheme_pages)
                 if re.search(r'An\s+Cumas\s+Gaeilge\s*\(\s*40\s+marc', text, re.I)
                 and re.search(r'Tasc', text, re.I)
                 and re.search(r'Ábhar', text, re.I)), None)
    if page is None:
        raise AssertionError(f'{year} OL: composition rubric page missing')
    criteria = [
        criterion('tasc', 'Tasc', 2,
                  ['2 marks when the printed task is fulfilled.'], guidance_kind='exact', permitted=[0, 2]),
        criterion('abhar', 'Ábhar', 8,
                  ['Relevant content which stays connected to the selected task.'], guidance_kind='indicative'),
        criterion('gaeilge', 'Cumas agus Cruinneas Gaeilge', 40,
                  ['Use the published 40-mark quality grid for command of Irish and accuracy.'],
                  guidance_kind='quality', permitted=range_marks(40, even=True)),
    ]
    return page, criteria


def composition_cards(year: int, level: str, paper_pages: list[str], scheme_pages: list[str]) -> list[dict]:
    # Roman numerals are the option labels on Ordinary Level Paper 1, not
    # answer-writing furniture, so retain them while splitting this page.
    raw = clean_lines(paper_pages[6], drop_answer_slots=False)
    level_ref = 'HL' if level == 'higher' else 'OL'
    scheme_page, shared_criteria = composition_scheme(year, level, scheme_pages)
    cards: list[dict] = []

    def without_next_section_or_footer(value: str) -> str:
        """Remove column headings/tariff tables that follow a final option."""
        patterns = [
            r'(?mi)^\s*[BCD]\s*[–—\-\uf02d]\s*(?:SCÉAL|DÍOSPÓIREACHT|ÓRÁID|LITIR|RÍOMHPHOST|COMHRÁ)\b',
            r'(?mi)^\s*Cuid\s+II\b',
            r'(?mi)^\s*A\s+(?:AISTE|Giota\s+Leanúnach)\b',
            r'(?mi)^\s*A\s*$\s*\n\s*(?:AISTE|Giota\s+Leanúnach)\b',
        ]
        cuts = [match.start() for pattern in patterns
                if (match := re.search(pattern, value))]
        return value[:min(cuts)] if cuts else value

    def add(section: str, label: str, body: str, instruction: str, topic: str, total: int) -> None:
        body = without_next_section_or_footer(body)
        question = prompt_text(f'{instruction}\n({label}) {body}')
        key = f'composition-{section.lower()}-{label}'
        requirements = [
            'Lean an fhoirm scríbhneoireachta a iarrtar sa cheist.',
            'Coinnigh ceangal cinnte leanúnach idir an teideal agus an t-ábhar.',
            'Bain úsáid as Gaeilge chruinn, shaibhir atá oiriúnach don tasc.',
        ]
        cards.append(base_card(
            year=year, level=level, paper=1, section='1', key=key,
            ref=f'{year} {level_ref} Paper 1 Ceapadóireacht {section}({label})',
            question=question, total=total, topic=topic,
            concept=f'irish-composition-{section.lower()}', paper_pages=paper_pages,
            candidate_pages=[7], scheme_page=scheme_page, scheme_trace=1000 + scheme_page,
            criteria=json.loads(json.dumps(shared_criteria, ensure_ascii=False)),
            requirements=requirements,
            guide_note='Composition is marked through the SEC’s published task/style, content and Irish-language criteria. The scheme does not prescribe one model answer.',
        ))

    if level == 'higher':
        a_start = re.search(r'Scríobh\s+AISTE', raw, re.I)
        b_start = re.search(r'Ceap\s+SCÉAL', raw, re.I)
        c_matches = list(re.finditer(r'Freagair\s+do\s+rogha\s+ceann\s+amháin\s+díobh\s+seo', raw, re.I))
        if not a_start or not b_start or not c_matches:
            raise AssertionError(f'{year} HL: composition sections missing')
        c_start = c_matches[-1]
        a_zone = raw[a_start.start():b_start.start()]
        b_zone = raw[b_start.start():c_start.start()]
        c_zone = raw[c_start.start():]
        a_first = re.search(r'(?m)^\s*\(a\)', a_zone, re.I)
        b_first = re.search(r'(?m)^\s*\(a\)', b_zone, re.I)
        c_first = re.search(r'(?m)^\s*\(a\)', c_zone, re.I)
        assert a_first and b_first and c_first
        a_instruction = prompt_text(a_zone[:a_first.start()])
        b_instruction = prompt_text(b_zone[:b_first.start()])
        c_instruction = prompt_text(c_zone[:c_first.start()])
        for label, body, _ in split_options(a_zone, tuple('abcde')):
            add('A', label, body, a_instruction, 'irish-2-0', 100)
        for label, body, _ in split_options(b_zone, ('a', 'b')):
            add('B', label, body, b_instruction, 'irish-2-3', 100)
        for label, body, _ in split_options(c_zone, ('a', 'b')):
            topic = 'irish-2-4' if label == 'a' else 'irish-2-5'
            add('C', label, body, c_instruction, topic, 100)
    else:
        start = re.search(r'Scríobh\s+giota\s+leanúnach', raw, re.I)
        if not start:
            raise AssertionError(f'{year} OL: composition start missing')
        zone = raw[start.start():]
        markers = list(re.finditer(r'(?m)^\s*\((i|ii|iii)\)\s*', zone, re.I))
        if len(markers) < 9:
            raise AssertionError(f'{year} OL: {len(markers)} composition options, expected 9')
        markers = markers[:9]
        bodies: list[str] = []
        for index, marker in enumerate(markers):
            end = markers[index + 1].start() if index + 1 < len(markers) else len(zone)
            bodies.append(zone[marker.end():end])
        story = re.search(r'Ceap\s+scéal', bodies[2], re.I)
        if not story:
            raise AssertionError(f'{year} OL: story instruction missing')
        a_instruction = prompt_text(zone[:markers[0].start()])
        story_instruction = prompt_text(bodies[2][story.start():])
        bodies[2] = bodies[2][:story.start()]
        specs = [
            ('A', ('i', 'ii', 'iii'), bodies[0:3], a_instruction, 'irish-2-6'),
            ('B', ('i', 'ii'), bodies[3:5], story_instruction, 'irish-2-3'),
            ('C', ('i', 'ii'), bodies[5:7], '', 'irish-2-8'),
            ('D', ('i', 'ii'), bodies[7:9], '', 'irish-2-9'),
        ]
        for section, labels, option_bodies, instruction, topic in specs:
            for label, body in zip(labels, option_bodies):
                add(section, label, body, instruction, topic, 50)

    if len(cards) != 9:
        raise AssertionError(f'{year} {level}: {len(cards)} composition cards, expected 9')
    return cards


def passage_title(page: str) -> str:
    clean = clean_lines(page)
    instruction = re.search(r'Léigh\s+an\s+sliocht[^.]*\.', clean, re.I | re.S)
    if not instruction:
        return 'Léamhthuiscint'
    tail = clean[instruction.end():]
    paragraph = re.search(r'(?m)^\s*1\.\s*', tail)
    title = prompt_text(tail[:paragraph.start()] if paragraph else tail[:180])
    return title[:160] or 'Léamhthuiscint'


def reading_scheme_excerpt(question: str, number: int, scheme_pages: list[str]) -> tuple[int, int, list[str]]:
    page_no, trace, page = best_scheme_page(question, scheme_pages)
    cleaned = clean_lines(page, drop_answer_slots=False)
    start_match = re.search(rf'(?m)^\s*{number}\.\s*\(a\)', cleaned, re.I)
    if start_match:
        start = start_match.start()
        next_match = re.search(rf'(?m)^\s*{number + 1}\.\s*\(a\)', cleaned[start_match.end():], re.I)
        end = start_match.end() + next_match.start() if next_match else len(cleaned)
        excerpt = cleaned[start:end]
    else:
        excerpt = excerpt_from_prompt(page, question)
    return page_no, trace, chunk_guide(excerpt)


def reading_cards(year: int, level: str, paper_pages: list[str], scheme_pages: list[str]) -> list[dict]:
    cards: list[dict] = []
    level_ref = 'HL' if level == 'higher' else 'OL'
    count = 6 if level == 'higher' else 5
    for passage, question_page in [('A', 5), ('B', 7)]:
        raw = clean_lines(paper_pages[question_page - 1])
        questions = numbered_questions(raw, count)
        for number, body, _ in questions:
            # Several two-column PDFs expose the question column before the
            # final paragraph of the passage in extraction order.  The printed
            # total is the authoritative end of each question.
            body = cut_after_n_marks(body, 1)
            question = prompt_text(f'{number}. {body}')
            total = (15 if number == 6 else 7) if level == 'higher' else 10
            scheme_page, trace, guide = reading_scheme_excerpt(
                question, number, scheme_pages)
            source_pages = [question_page - 1, question_page]
            cards.append(base_card(
                year=year, level=level, paper=2, section='2',
                key=f'reading-{passage.lower()}-q{number}',
                ref=f'{year} {level_ref} Paper 2 Léamhthuiscint {passage} · Ceist {number}',
                question=question, total=total,
                topic='irish-3-0' if passage == 'A' else 'irish-3-1',
                concept=f'irish-reading-{passage.lower()}-q{number}',
                paper_pages=paper_pages, candidate_pages=[question_page],
                scheme_page=scheme_page, scheme_trace=trace,
                criteria=[criterion('eolas', 'Eolas', total, guide, guidance_kind='exact')],
                requirements=[
                    'Léigh an sliocht oifigiúil a ghabhann leis an gceist.',
                    'Freagair gach fochuid agus cloígh leis an alt a luaitear.',
                    'Bain úsáid as do chuid focal féin nuair a iarrtar ort é.',
                ],
                guide_note='These are the question-specific answers and tariffs printed by the SEC. Equivalent answers remain valid where the scheme says they are acceptable.',
                source=source_material(
                    f'Léamhthuiscint {passage}',
                    passage_title(paper_pages[question_page - 2]),
                    source_pages,
                ),
            ))
    expected = 12 if level == 'higher' else 10
    if len(cards) != expected:
        raise AssertionError(f'{year} {level}: {len(cards)} reading cards, expected {expected}')
    return cards


def section_from_pages(pages: Sequence[str], start_page: int = 8, end_page: int = 15) -> PagedText:
    return PagedText([clean_lines(page, drop_answer_slots=False)
                      for page in pages[start_page - 1:end_page]])


def locate_prompt_page(prompt: str, paper_pages: Sequence[str], candidates: Iterable[int]) -> int:
    return trace_prompt_on_pages(prompt, paper_pages, candidates)[0]


def literature_scheme(prompt: str, scheme_pages: list[str]) -> tuple[int, int, list[str]]:
    page, trace, scheme_page = best_scheme_page(prompt, scheme_pages)
    excerpt = excerpt_from_prompt(scheme_page, prompt, maximum=3200)
    return page, trace, chunk_guide(excerpt, indicative=True)


def option_source_pages(
    prompt: str,
    paper_pages: Sequence[str],
    *,
    extend_to_end: bool = False,
) -> list[int]:
    start = locate_prompt_page(prompt, paper_pages, range(8, min(16, len(paper_pages) + 1)))
    if not extend_to_end:
        return [start]
    pages = [start]
    for page_no in range(start + 1, min(15, len(paper_pages)) + 1):
        text = comparable(paper_pages[page_no - 1])
        blank_key = slug(text)
        if (not text or 'leathanach-ban' in blank_key
                or re.search(r'nil-(?:aon-)?abhar-scrudaithe', blank_key)
                or 'admhalacha' in blank_key):
            break
        pages.append(page_no)
    return pages


def prose_poetry_zones(document: PagedText, level: str) -> dict[str, tuple[str, int]]:
    if level == 'ordinary':
        # In 2021–2022 page 8 is a literature contents page and the four real
        # answer zones start on pages 9, 10, 11–13 and 14.  From 2023 onward
        # those zones moved one page earlier.  Page-based extraction is more
        # trustworthy here than following the repeated contents headings.
        contents_first = 'ar leathanach' in comparable(document.pages[0])
        shift = 1 if contents_first else 0
        return {
            '2a': (document.pages[shift], document.offsets[shift]),
            '2b': (document.pages[shift + 1], document.offsets[shift + 1]),
            '3a': ('\n\n'.join(document.pages[shift + 2:shift + 5]),
                   document.offsets[shift + 2]),
            '3b': (document.pages[shift + 5], document.offsets[shift + 5]),
        }

    text = document.text
    patterns = {
        '2a': (r'2A\.\s*Prós\s+Ainmnithe', [r'2B\.\s*Prós\s+Roghnach']),
        '2b': (r'2B\.\s*Prós\s+Roghnach', [r'Ceist\s+3', r'3A\.\s*Filíocht']),
        '3a': (r'3A\.\s*Filíocht\s+Ainmnithe', [r'3B\.\s*Filíocht\s+Roghnach']),
        '3b': (r'3B\.\s*Filíocht\s+Roghnach', [r'Ceist\s+4', r'4A\.']),
    }
    out: dict[str, tuple[str, int]] = {}
    for key, (start, ends) in patterns.items():
        # The candidate-instructions page repeats the section names before the
        # actual questions.  Always select the final occurrence.
        body, offset = slice_section(text, start, ends, last=True)
        out[key] = (body, offset)
    return out


def literature_cards(year: int, level: str, paper_pages: list[str], scheme_pages: list[str]) -> list[dict]:
    cards: list[dict] = []
    level_ref = 'HL' if level == 'higher' else 'OL'
    document = section_from_pages(paper_pages)
    zones = prose_poetry_zones(document, level)

    def without_literature_footer(value: str) -> str:
        footer = re.search(
            r'(?mi)^\s*(?:(?:2A|2B|3A|3B)\s*(?:[–—-]\s*)?'
            r'(?:PRÓS|FILÍOCHT)\b|Ceist\s+[23]\s+(?:Prós|Filíocht)\b)', value)
        return value[:footer.start()] if footer else value

    def add_literature(
        *, family: str, section_key: str, option: str, body: str, topic: str,
        total: int, source: dict | None = None,
    ) -> None:
        body = without_literature_footer(body)
        question = prompt_text(f'({option}) {body}')
        scheme_page, trace, guide = literature_scheme(question, scheme_pages)
        knowledge = total - 5 if level == 'higher' else total
        criteria = [criterion(
            'eolas', 'Eolas', knowledge, guide, guidance_kind='indicative')]
        if level == 'higher':
            criteria.append(criterion(
                'gaeilge', 'Gaeilge', 5,
                ['5 sárchumas; 4 cumas an-mhaith; 3 cumas maith; 2 cumas sásúil; 1 cumas lag; 0 gan fiúntas.'],
                guidance_kind='quality'))
        else:
            criteria.append(criterion(
                'gaeilge-deduction', 'Gaeilge lochtach', 4,
                ['Apply only the 0–4 language deduction printed by the scheme; this is subtracted from Eolas.'],
                guidance_kind='quality', kind='deduction'))
        restrictions = []
        if section_key.endswith('b'):
            restrictions.append('Ná húsáid ábhar ainmnithe i bhfreagra ar an ábhar roghnach.')
        requirements = [
            'Freagair gach fochuid atá priontáilte sa rogha seo.',
            'Úsáid eolas cruinn agus samplaí ábhartha ón téacs.',
            *restrictions,
        ]
        cards.append(base_card(
            year=year, level=level, paper=2, section='2',
            key=f'{family}-{section_key}-{option}',
            ref=f'{year} {level_ref} Paper 2 {family.title()} {section_key.upper()}({option})',
            question=question, total=total, topic=topic,
            concept=f'irish-{family}-{section_key}-{topic}', paper_pages=paper_pages,
            candidate_pages=range(8, min(16, len(paper_pages) + 1)),
            scheme_page=scheme_page, scheme_trace=trace, criteria=criteria,
            requirements=requirements,
            guide_note='SEC supporting points for literature are indicative rather than exhaustive. Relevant alternatives must be judged on their merits; the language criterion or deduction is applied separately exactly as printed.',
            source=source,
        ))

    prose_labels = ('a', 'b') if level == 'higher' else ('a', 'b', 'c')
    poetry_labels = prose_labels
    for section_key in ('2a', '2b'):
        zone, _ = zones[section_key]
        for option, body, _ in split_options(zone, prose_labels):
            if level == 'higher':
                body = cut_after_n_marks(body, 1)
            topic = title_topic(
                body, PROSE_TOPICS,
                'irish-4-0' if section_key == '2a' else 'irish-4-7')
            add_literature(
                family='prose', section_key=section_key, option=option,
                body=body, topic=topic, total=30 if level == 'higher' else 25)

    for section_key in ('3a', '3b'):
        zone, _ = zones[section_key]
        for option, body, _ in split_options(zone, poetry_labels):
            # Prescribed poems are printed after the three linked subparts.  The
            # poem is source material, not part of the question text.
            if section_key == '3a':
                body = cut_after_n_marks(body, 3)
            topic = title_topic(
                body, POETRY_TOPICS,
                'irish-5-0' if section_key == '3a' else 'irish-5-6')
            question = prompt_text(f'({option}) {body}')
            source = None
            if section_key == '3a':
                source_pages = option_source_pages(question, paper_pages)
                title = next((key.title() for key in POETRY_TOPICS
                              if comparable(key) in comparable(question)), 'Dán Ainmnithe')
                source = source_material('Filíocht Ainmnithe', title, source_pages)
            add_literature(
                family='poetry', section_key=section_key, option=option,
                body=body, topic=topic, total=30 if level == 'higher' else 25,
                source=source)

    if level == 'higher':
        q4_body, _ = slice_section(document.text, r'4A\.', [])
        q4_text = '4A. ' + q4_body
        option_matches = list(re.finditer(r'(?m)^\s*4([A-F])\.\s*', q4_text, re.I))
        if len(option_matches) != 6:
            raise AssertionError(f'{year} HL: {len(option_matches)} additional-literature options, expected 6')
        for index, match in enumerate(option_matches):
            letter = match.group(1).lower()
            end = option_matches[index + 1].start() if index + 1 < len(option_matches) else len(q4_text)
            body = cut_after_n_marks(q4_text[match.end():end], 1)
            question = prompt_text(f'4{letter.upper()}. {body}')
            topic = title_topic(question, ADDITIONAL_TOPICS, 'irish-6-5')
            source = None
            if 'thíos' in comparable(question) or topic.startswith('irish-6-') and topic not in {
                'irish-6-0', 'irish-6-1', 'irish-6-2', 'irish-6-3', 'irish-6-4'
            }:
                pages = option_source_pages(question, paper_pages, extend_to_end=index == 5)
                # Additional-literature option F prints the selected poem on
                # the following page(s); the start page is the question card
                # itself, not source material the student needs to swipe past.
                if index == 5 and len(pages) > 1:
                    pages = pages[1:]
                printed = prompt_text(body)
                title_match = re.search(
                    r'Dánta\s+Breise\s*[–—-]\s*(.+?)\s+Freagair\b', printed, re.I)
                title = title_match.group(1).strip() if title_match else printed.split('‘', 1)[0][:110]
                source = source_material('Litríocht Bhreise', title or 'Téacs Clóite', pages)
            add_literature(
                family='literature', section_key='4', option=letter,
                body='4' + letter.upper() + '. ' + body, topic=topic, total=40,
                source=source)

    expected = 14 if level == 'higher' else 12
    if len(cards) != expected:
        raise AssertionError(f'{year} {level}: {len(cards)} literature cards, expected {expected}')
    return cards


def paper_fileid(year: int, level: str, paper: int) -> str:
    code = 'A' if level == 'higher' else 'G'
    if year == 2022 and level == 'ordinary' and paper == 1:
        return 'LC001GLP000IV'
    return f'LC001{code}LP{paper}00IV'


def build_corpus() -> list[dict]:
    cards: list[dict] = []
    for year in YEARS:
        for level in ('higher', 'ordinary'):
            p1_pages = page_texts(paper_path(year, level, 1))
            p2_pages = page_texts(paper_path(year, level, 2))
            scheme_pages = page_texts(scheme_path(year, level))
            year_cards = [
                *listening_cards(year, level, p1_pages, scheme_pages),
                *composition_cards(year, level, p1_pages, scheme_pages),
                *reading_cards(year, level, p2_pages, scheme_pages),
                *literature_cards(year, level, p2_pages, scheme_pages),
            ]
            expected = 43 if level == 'higher' else 37
            if len(year_cards) != expected:
                raise AssertionError(f'{year} {level}: {len(year_cards)} total cards, expected {expected}')
            for card in year_cards:
                card['paperFileid'] = paper_fileid(year, level, card['paper'])
            cards.extend(year_cards)

    if len(cards) != 400:
        raise AssertionError(f'Irish corpus has {len(cards)} cards, expected 400')
    ids = [card['id'] for card in cards]
    if len(set(ids)) != len(ids):
        duplicates = sorted({identifier for identifier in ids if ids.count(identifier) > 1})
        raise AssertionError(f'duplicate card ids: {duplicates}')
    if any(len(card['questionText']) < 18 for card in cards):
        raise AssertionError('one or more Irish prompts are implausibly short')
    composition_furniture = re.compile(
        r'\b(?:Cuid\s+II\s+An\s+Cheapadóireacht|[BCD]\s*[–—\-\uf02d]\s*'
        r'(?:SCÉAL|DÍOSPÓIREACHT|LITIR|COMHRÁ))\b', re.I)
    if any(composition_furniture.search(card['questionText'])
           for card in cards if '-composition-' in card['id']):
        raise AssertionError('a composition option contains the next section or footer')
    literature_furniture = re.compile(
        r'\b(?:(?:2A|2B|3A|3B)\s*(?:[–—-]\s*)?(?:PRÓS|FILÍOCHT)'
        r'|Ceist\s+[23]\s+(?:Prós|Filíocht))\b', re.I)
    if any(literature_furniture.search(card['questionText'])
           for card in cards if card['paper'] == 2 and '-reading-' not in card['id']):
        raise AssertionError('a literature option contains a page footer')
    if any(len(card['questionText']) > 900
           for card in cards if '-reading-' in card['id']):
        raise AssertionError('a reading question contains passage text after its printed total')
    listening_leakage = re.compile(
        r'\b(?:Siombailí\s+Anótála|Stíl\s+chuí\s+scríbhneoireachta|'
        r'An\s+Cumas\s+Gaeilge\s*\(\s*(?:40|80)\s+marc)\b', re.I)
    if any(listening_leakage.search(' '.join(card['criteria'][0]['guidance']))
           for card in cards if '-listening-' in card['id']):
        raise AssertionError('a listening guide contains annotation or composition material')
    if any(not card['criteria'] for card in cards):
        raise AssertionError('one or more Irish cards have no published marking criteria')
    return cards


def census(cards: Sequence[dict]) -> dict:
    asks = [{
        'id': card['id'],
        'year': card['year'],
        'level': LEVEL_SHORT[card['level']],
        'paper': card['paper'],
        'questionRef': card['questionRef'],
        'status': 'authored',
    } for card in cards]
    papers = []
    for year in YEARS:
        for level in ('higher', 'ordinary'):
            for paper in (1, 2):
                subset = [card for card in cards
                          if card['year'] == year and card['level'] == level and card['paper'] == paper]
                papers.append({
                    'year': year,
                    'level': LEVEL_SHORT[level],
                    'paper': paper,
                    'cardUnits': len(subset),
                    'authored': len(subset),
                    'queued': 0,
                })
    return {
        'subject': 'irish',
        'scope': 'Leaving Certificate Higher and Ordinary Level, 2021–2025',
        'definition': 'One independently selectable response; compulsory linked parts remain together.',
        'paperCount': len(papers),
        'cardUnitCount': len(asks),
        'authoredCount': len(asks),
        'queuedCount': 0,
        'papers': papers,
        'asks': asks,
    }


def serialise(cards: Sequence[dict]) -> str:
    return json.dumps({
        'subject': 'irish',
        'scope': '2021–2025 Higher and Ordinary Level',
        'cardCount': len(cards),
        'cards': cards,
    }, ensure_ascii=False, indent=2) + '\n'


def scheme_text_exports() -> dict[str, str]:
    """Commit searchable page-separated scheme text; source PDFs stay ignored."""
    exports: dict[str, str] = {}
    for year in YEARS:
        for level in ('higher', 'ordinary'):
            pages = page_texts(scheme_path(year, level))
            chunks = [
                f'# SEC Gaeilge {LEVEL_IRISH[level]} marking scheme {year}',
                '',
                'Extracted page text used for Mark Bank provenance checks.',
                '',
            ]
            for page_no, page in enumerate(pages, 1):
                chunks.extend([
                    f'## Page {page_no}', '',
                    clean_lines(page, drop_answer_slots=False), '',
                ])
            path = os.path.join(
                SCHEME_TEXT_ROOT, f'{year}-{LEVEL_SHORT[level]}.md')
            exports[path] = '\n'.join(chunks).rstrip() + '\n'
    return exports


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    cards = build_corpus()
    manifest = serialise(cards)
    ledger = json.dumps(census(cards), ensure_ascii=False, indent=2) + '\n'
    schemes = scheme_text_exports()
    if args.check:
        existing_manifest = open(OUT, encoding='utf-8').read() if os.path.exists(OUT) else ''
        existing_census = open(CENSUS_OUT, encoding='utf-8').read() if os.path.exists(CENSUS_OUT) else ''
        stale_schemes = [path for path, content in schemes.items()
                         if not os.path.exists(path)
                         or open(path, encoding='utf-8').read() != content]
        if existing_manifest != manifest or existing_census != ledger or stale_schemes:
            print('Irish generated files are stale; run irish_cards.py', file=sys.stderr)
            return 1
        print(f'Irish corpus verified: {len(cards)} cards across 20 papers')
        return 0

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    os.makedirs(os.path.dirname(CENSUS_OUT), exist_ok=True)
    with open(OUT, 'w', encoding='utf-8') as handle:
        handle.write(manifest)
    with open(CENSUS_OUT, 'w', encoding='utf-8') as handle:
        handle.write(ledger)
    os.makedirs(SCHEME_TEXT_ROOT, exist_ok=True)
    for path, content in schemes.items():
        with open(path, 'w', encoding='utf-8') as handle:
            handle.write(content)
    higher = sum(card['level'] == 'higher' for card in cards)
    ordinary = sum(card['level'] == 'ordinary' for card in cards)
    print(f'wrote {len(cards)} Irish cards ({higher} Higher, {ordinary} Ordinary)')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
