#!/usr/bin/env python3
"""Build the complete English Mark Bank card manifest from the SEC papers.

The question paper remains the source of every prompt.  The marking scheme is
used only to locate the page containing the corresponding PCLM guidance.  No
indicative answer is promoted to a required marking point.

    python3 scripts/markbank/authoring/english_cards.py
    python3 scripts/markbank/authoring/english_cards.py --check

The generated JSON is committed because the local PDF corpus is deliberately
gitignored.  Structural and textual assertions make a parser miss loud: all 660
census ids must be emitted once, every prompt must be substantial, and every
prompt must have a matching passage in its own year's marking scheme.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import re
import sys
import unicodedata
from difflib import SequenceMatcher
from typing import Iterable

import fitz


ROOT = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))
PAPER_ROOT = os.path.join(ROOT, 'examiner-reports', 'english', 'papers')
SCHEME_ROOT = os.path.join(ROOT, 'examiner-reports', 'english', 'schemes')
CENSUS_PATH = os.path.join(ROOT, 'scripts', 'markbank', 'authored', 'english-census.json')
OUT = os.path.join(ROOT, 'components', 'MarkBank', 'cards', 'english', 'authored.json')
CURRICULUM_PATH = os.path.join(ROOT, 'curriculum.ts')

ROMANS = ('i', 'ii', 'iii')
LETTERS_5 = tuple('abcde')
LETTERS_6 = tuple('abcdef')
LETTERS_9 = tuple('abcdefghi')


def clean_unicode(value: str) -> str:
    return (value.replace('\xa0', ' ').replace('\u00ad', '')
            .replace('\ufb01', 'fi').replace('\ufb02', 'fl'))


def compact(value: str) -> str:
    return re.sub(r'\s+', ' ', clean_unicode(value)).strip()


def comparable(value: str) -> str:
    value = unicodedata.normalize('NFKC', clean_unicode(value)).lower()
    value = value.replace('’', "'").replace('‘', "'")
    value = value.replace('“', '"').replace('”', '"')
    value = value.replace('–', '-').replace('—', '-')
    return re.sub(r'[^a-z0-9]+', ' ', value).strip()


def clean_prompt(value: str) -> str:
    value = clean_unicode(value)
    value = re.sub(r'(?m)^\s*(?:OR|or)\s*$', ' ', value)
    value = re.sub(r'[⟨<]?\(\s*(?:10|15|20|30|40|50|60|70|100)\s*\)[⟩>]?', ' ', value)
    value = re.sub(r'(?m)^\s*\d+\s*$', ' ', value)
    value = compact(value)
    # One 2022 SEC PDF stores the poet's name in several independently placed
    # glyph runs.  The visible print is "Emily Dickinson"; this repairs only
    # that known extraction artefact, not the wording of the question.
    value = re.sub(r'Emi\s+D\s+ly\s+ickinson', 'Emily Dickinson', value)
    # A printed compound split across PDF lines extracts as "wide- ranging".
    # Preserve the real hyphen while removing only the artificial line space.
    value = re.sub(r'(?<=\w)-\s+(?=\w)', '-', value)
    # In the 2022 OL Paper 1 extraction the repeated section instruction is
    # removed after the QA block, leaving only its leading "N.B." attached to
    # part (iii)(b). It is page furniture, not part of the ask.
    value = re.sub(r'\s+N\.?\s*B\.?\s*$', '', value, flags=re.I)
    return value.strip(' -–—')


def strip_furniture_lines(value: str) -> str:
    lines = []
    for line in clean_unicode(value).splitlines():
        text = compact(line)
        if re.match(r'^Leaving Certificate Examination\s+\d{4}$', text, re.I):
            continue
        if re.match(r'^English\s+[–—-]\s+(?:Higher|Ordinary) Level\s+[–—-]\s+Paper\s+[12]$', text, re.I):
            continue
        if re.fullmatch(r'\d{1,2}', text):
            continue
        lines.append(line)
    return '\n'.join(lines)


def before_mark(value: str, marks: int) -> str:
    match = re.search(rf'[⟨<]?\(\s*{marks}\s*\)[⟩>]?', value)
    return value[:match.start()] if match else value


def split_page_markdown(path: str) -> dict[int, str]:
    with open(path, encoding='utf-8') as handle:
        text = handle.read()
    bits = re.split(r'^## Page (\d+)\s*$', text, flags=re.M)
    return {int(bits[index]): bits[index + 1] for index in range(1, len(bits), 2)}


def question_scheme_page(question: str, pages: dict[int, str]) -> tuple[int, int]:
    """Return (page, evidence score) using shared eight-word sequences.

    Full substring matching fails for composite questions whose separately
    marked parts cross a scheme page.  N-grams still tie the exact paper wording
    to the correct question-specific page without confusing it with Appendix 2.
    """
    words = comparable(question).split()
    width = min(8, max(4, len(words)))
    grams = [' '.join(words[index:index + width])
             for index in range(max(1, len(words) - width + 1))]
    normalised_pages = {page_no: comparable(page_text) for page_no, page_text in pages.items()}
    shared_scores: list[tuple[int, int]] = []
    for page_no, page in normalised_pages.items():
        shared_scores.append((sum(gram in page for gram in grams), -page_no))
    shared, neg_page = max(shared_scores)
    if shared:
        return -neg_page, shared * 1000 + len(comparable(question))

    scored: list[tuple[int, int]] = []
    for page_no, page in normalised_pages.items():
        longest = SequenceMatcher(None, comparable(question), page, autojunk=False) \
            .find_longest_match().size
        scored.append((longest, -page_no))
    longest, neg_page = max(scored)
    page_no = -neg_page
    minimum = min(28, max(16, math.floor(len(comparable(question)) * .16)))
    if longest < minimum:
        raise AssertionError(
            f'no marking-scheme trace for prompt (best p.{page_no}, match {longest}): {question}')
    return page_no, longest


def block_text(block: tuple) -> str:
    return clean_unicode(block[4])


def first_meaningful_line(value: str) -> str:
    return next((compact(line) for line in value.splitlines() if compact(line)), '')


def remove_footer(value: str) -> str:
    # Footer/header blocks are often extracted last because these PDFs are
    # internally rotated.  They are never part of a question.
    for marker in (
        'Leaving Certificate Examination',
        'Leaving Certificate – Higher Level',
        'Leaving Certificate – Ordinary Level',
        'Copyright notice',
        'There is no examination material on this page',
    ):
        position = value.find(marker)
        if position >= 0:
            value = value[:position]
    return value


def p1_question_zone(page: fitz.Page) -> str:
    blocks = page.get_text('blocks')
    hits = [block for block in blocks if re.search(r'QUESTION\s+A', block_text(block), re.I)]
    if not hits:
        raise AssertionError(f'page {page.number + 1}: no Question A block')
    start_y = min(block[1] for block in hits) - 2
    selected = [block_text(block) for block in blocks
                if block[1] >= start_y
                and block[1] < page.rect.height - 35
                and not re.match(r'^\s*Leaving Certificate Examination', block_text(block), re.I)]
    zone = remove_footer('\n'.join(selected))
    if not re.search(r'QUESTION\s+B', zone, re.I):
        raise AssertionError(f'page {page.number + 1}: no Question B block')
    return zone


def split_roman_parts(value: str, expected: int = 3) -> dict[str, str]:
    matches = list(re.finditer(r'(?m)^\s*\((i|ii|iii)\)\s*', value, re.I))
    # Keep the first ordered i/ii/iii set; quoted references to a previous part
    # may occur later in a prompt.
    ordered: list[re.Match[str]] = []
    next_index = 0
    for match in matches:
        if match.group(1).lower() == ROMANS[next_index]:
            ordered.append(match)
            next_index += 1
            if next_index == expected:
                break
    if len(ordered) != expected:
        raise AssertionError(f'expected {expected} roman parts, found {len(ordered)} in {compact(value)[:300]}')
    out = {}
    for index, match in enumerate(ordered):
        end = ordered[index + 1].start() if index + 1 < len(ordered) else len(value)
        out[match.group(1).lower()] = value[match.end():end]
    return out


def split_numbered(value: str, numbers: Iterable[int]) -> dict[int, str]:
    wanted = list(numbers)
    positions: list[tuple[int, int, int]] = []
    cursor = 0
    for number in wanted:
        match = re.search(rf'(?m)^\s*{number}\.\s+', value[cursor:])
        if not match:
            raise AssertionError(f'missing Q{number} in {compact(value)[:400]}')
        start, body = cursor + match.start(), cursor + match.end()
        positions.append((number, start, body))
        cursor = body
    out: dict[int, str] = {}
    for index, (number, _, body) in enumerate(positions):
        end = positions[index + 1][1] if index + 1 < len(positions) else len(value)
        out[number] = value[body:end]
    return out


def source_heading(page: fitz.Page, text_no: int) -> tuple[str, str]:
    blocks = page.get_text('blocks')
    heading_block = next((block for block in blocks
                          if re.search(rf'\bTEXT\s*{text_no}\s*[–—-]',
                                       block_text(block), re.I)), None)
    if heading_block is None:
        raise AssertionError(f'page {page.number + 1}: missing TEXT {text_no} heading')
    raw_heading = clean_unicode(block_text(heading_block))
    heading_match = re.search(
        rf'(?mi)^\s*(TEXT\s*{text_no}\s*[–—-][^\n]+)', raw_heading)
    if not heading_match:
        raise AssertionError(f'page {page.number + 1}: malformed TEXT {text_no} heading')
    heading = compact(heading_match.group(1))
    title = re.split(r'[–—-]', heading, maxsplit=1)[1].strip()

    def first_editorial_paragraph(raw: str) -> str:
        raw = re.split(r'(?m)^\s*1\.\s*(?:\n|$)', clean_unicode(raw), maxsplit=1)[0]
        paragraphs = [compact(part) for part in re.split(r'\n\s*\n', raw)
                      if compact(part)]
        return paragraphs[0] if paragraphs else ''

    attribution = first_editorial_paragraph(raw_heading[heading_match.end():])

    # Some papers draw the heading, editorial introduction and passage as
    # separate blocks even though their plain-text extraction interleaves all
    # three. The nearest block visually below the heading is the introduction.
    if not attribution:
        candidates = sorted(
            (block for block in blocks if block != heading_block
             and block[1] >= heading_block[1] + 1
             and block[1] < page.rect.height - 35),
            key=lambda block: (block[1], block[0]),
        )
        if candidates:
            attribution = first_editorial_paragraph(block_text(candidates[0]))
    if not attribution:
        attribution = 'Source acknowledgement printed on the official State Examinations Commission paper.'
    if len(attribution) > 700:
        raise AssertionError(
            f'page {page.number + 1}: source attribution absorbed passage text ({len(attribution)} chars)')
    return title, attribution


def source_needed(question: str) -> bool:
    value = comparable(question)
    triggers = (
        'based on your reading', 'reference to the text', 'reference to text',
        'referring to the article', 'referring to the memoir', 'in the passage',
        'above text', 'above article', 'above passage', 'above memoir',
        'image 1', 'image 2', 'image 3', 'image 4', 'text 1', 'text 2', 'text 3',
        'what does', 'what do you think the writer means',
    )
    return any(trigger in value for trigger in triggers)


def requirements_for(question: str, source: dict | None, printed_parts: list[str]) -> list[str]:
    lower = comparable(question)
    requirements = ['Address every instruction in the printed task.']
    if printed_parts:
        labels = ', '.join(part.rsplit(' ', 2)[0] for part in printed_parts)
        requirements.append(f'Complete every linked part of the question: {labels}.')
    if source:
        requirements.append('Read and use the official source material supplied with the card.')
    if 'support' in lower and ('reference' in lower or 'evidence' in lower):
        requirements.append('Support the response with relevant evidence from the named text or source.')
    if 'compare' in lower:
        requirements.append('Make the comparison explicit across the number of texts requested.')
    count_match = re.search(r'\b(two|three|four)\s+(?:clear\s+|compelling\s+|interesting\s+)?(?:points|reasons|insights|features|elements|examples|moments)', lower)
    if count_match:
        requirements.append(f'Develop the required {count_match.group(1)} points fully.')
    genre_match = re.search(
        r'\b(?:write|prepare|deliver)\s+(?:the\s+text\s+of\s+)?(?:an?\s+)?'
        r'(personal essay|discursive essay|short story|speech|talk|article|letter|review|podcast|'
        r'debate contribution|presentation|pamphlet|diary entr(?:y|ies)|interview|open letter|feature article)',
        lower,
    )
    if genre_match:
        requirements.append(f'Use the conventions and register of the requested {genre_match.group(1)}.')
    requirements.append('Sustain a clear, purposeful response in an appropriate register.')
    return list(dict.fromkeys(requirements))


def concept_for(section: str, question: str) -> str:
    lower = comparable(question)
    if section == 'Comprehending A':
        if any(word in lower for word in ('language', 'style', 'imagery', 'visual image')):
            return 'english-comprehending-style'
        if any(word in lower for word in ('agree', 'personal response', 'your view', 'your opinion')):
            return 'english-comprehending-viewpoint'
        return 'english-comprehending-insights'
    if section == 'Comprehending B':
        return 'english-functional-writing'
    if section == 'Composing':
        for slug, phrase in (
            ('personal-essay', 'personal essay'), ('discursive', 'discursive essay'),
            ('short-story', 'short story'), ('speech', 'speech'), ('article', 'article'),
        ):
            if phrase in lower:
                return f'english-composing-{slug}'
        return 'english-composing'
    if section == 'Single Text':
        return 'english-single-text-response'
    if section == 'Comparative Study':
        return 'english-comparative-response'
    if section == 'Unseen Poetry':
        return 'english-unseen-poetry-response'
    return 'english-prescribed-poetry-response'


def curriculum_topics() -> tuple[
        dict[str, str], dict[str, str], dict[str, str], dict[str, str]]:
    with open(CURRICULUM_PATH, encoding='utf-8') as handle:
        text = handle.read()
    matches = re.findall(
        r'"id": "(english-(?:11|12)-\d+)",\s*\n\s*"name": "([^"]+)"', text)
    poets: dict[str, str] = {}
    works: dict[str, str] = {}
    poet_labels: dict[str, str] = {}
    work_labels: dict[str, str] = {}
    for topic_id, name in matches:
        target = poets if topic_id.startswith('english-11-') else works
        target[comparable(name)] = topic_id
        if topic_id.startswith('english-11-'):
            poet_labels[comparable(name)] = name
        if '(' in name:
            target[comparable(name.split('(')[0])] = topic_id
            target[comparable(name[name.find('(') + 1:name.rfind(')')])] = topic_id
            if topic_id.startswith('english-11-'):
                poet_labels[comparable(name.split('(')[0])] = name.split('(')[0].strip()
                poet_labels[comparable(name[name.find('(') + 1:name.rfind(')')])] = name
        if topic_id.startswith('english-12-'):
            if '(' in name:
                title = name[:name.find('(')].strip()
                author = name[name.find('(') + 1:name.rfind(')')].strip()
                work_labels[topic_id] = f'{title} — {author}'
            else:
                work_labels[topic_id] = name
    return poets, works, poet_labels, work_labels


POET_TOPICS, WORK_TOPICS, POET_LABELS, WORK_LABELS = curriculum_topics()

PRESCRIBED_AUTHORS = {
    comparable('The Glass Hammer'): 'Andrew Hudgins',
    comparable('Oranges'): 'Gary Soto',
    comparable('Hawk Roosting'): 'Ted Hughes',
    comparable("My Father’s Kites"): 'Allison Joseph',
    comparable('Night Drive'): 'Tom French',
    # Preserve the names exactly as these examination pages print them. The
    # curriculum catalogue keeps the poets' canonical spellings and fuzzy
    # topic matching links the two identities.
    comparable('In Praise of My Sister'): 'Wislawa Szymborska',
    comparable('Revelation'): 'Liz Lockhead',
}


def prescribed_source_identity(page: fitz.Page, letter: str, question_zone: str) -> tuple[str, str, str]:
    raw = clean_unicode(page.get_text('text'))
    before_q1 = raw[:re.search(r'(?m)^\s*1\.\s*', raw).start()]
    lines = [compact(line) for line in before_q1.splitlines() if compact(line)]
    title = ''
    for index, line in enumerate(lines):
        match = re.match(rf'^{letter.upper()}(?:\s+(.+))?$', line)
        if not match:
            continue
        title = compact(match.group(1) or '')
        if not title:
            title = next((candidate for candidate in lines[index + 1:]
                          if not re.match(r'^(PRESCRIBED|You must|Leaving|English)', candidate, re.I)), '')
        break
    if not title:
        title = f'Poem {letter.upper()}'

    page_normalised = comparable(raw)
    poet_matches = [(len(key), POET_LABELS[key], POET_TOPICS[key])
                    for key in POET_LABELS if len(key) > 4 and key in page_normalised]
    if poet_matches:
        _, poet, topic = max(poet_matches)
    else:
        byline = re.search(
            r"\bby\s+([A-Z][A-Za-zÀ-ž.'-]+(?:\s+[A-Z][A-Za-zÀ-ž.'-]+){0,3})",
            clean_unicode(question_zone))
        mapped = next((author for poem, author in PRESCRIBED_AUTHORS.items()
                       if poem in comparable(title)), None)
        poet = mapped or (compact(byline.group(1)) if byline
                          else 'author named on the official SEC paper')
        topic = closest_topic(poet, POET_TOPICS, 'english-8-1')
    return title, poet, topic


def closest_topic(value: str, catalogue: dict[str, str], fallback: str) -> str:
    query = comparable(value)
    exact = catalogue.get(query)
    if exact:
        return exact
    candidates = [(SequenceMatcher(None, query, name).ratio(), topic_id)
                  for name, topic_id in catalogue.items()
                  if len(name) > 2]
    score, topic_id = max(candidates, default=(0.0, fallback))
    return topic_id if score >= .58 else fallback


def paper_source(label: str, title: str, pages: list[int], attribution: str) -> dict:
    return {
        'kind': 'source-text',
        'label': label,
        'title': title,
        'pages': pages,
        'attribution': attribution,
        'presentationNote': 'Official State Examinations Commission examination layout.',
    }


def work_groups(doc: fitz.Document) -> dict[str, str]:
    groups: dict[str, list[str]] = {}
    active: str | None = None
    for page_index in (1, 2):
        for block in doc[page_index].get_text('blocks'):
            text = block_text(block)
            line = first_meaningful_line(text)
            match = re.match(r'^([A-E])(?:\s+\S.*)?$', line)
            if match:
                active = match.group(1).lower()
                groups[active] = [text]
            elif active and not re.match(r'^Leaving Certificate', line, re.I):
                groups[active].append(text)
    if set(groups) != set(LETTERS_5):
        raise AssertionError(f'HL Single Text work groups are {sorted(groups)}, expected A-E')
    return {letter: '\n'.join(blocks) for letter, blocks in groups.items()}


def title_before_marker(value: str, marker: str) -> str:
    head = value[:value.find(marker)]
    lines = [compact(line) for line in head.splitlines() if compact(line)]
    if lines and re.fullmatch(r'[A-I]', lines[0]):
        lines = lines[1:]
    elif lines:
        lines[0] = re.sub(r'^[A-I]\s+', '', lines[0])
    return compact(' '.join(lines))


def split_or_number_two(value: str) -> tuple[str, str]:
    match = re.search(r'(?mi)^\s*OR\s*\n?\s*2\.\s+', value)
    if not match:
        match = re.search(r'(?i)\bOR\s+2\.\s+', value)
    if not match:
        raise AssertionError(f'missing OR Q2 boundary in {compact(value)[:400]}')
    return value[:match.start()], value[match.end():]


def add_p1(year: int, level: str, doc: fitz.Document, put) -> None:
    for text_no, page_index in enumerate((2, 4, 6), 1):
        zone = p1_question_zone(doc[page_index])
        qa_match = re.search(r'QUESTION\s+A\s*[–—-]\s*\d+\s+Marks?', zone, re.I)
        qb_match = re.search(r'QUESTION\s+B\s*[–—-]\s*\d+\s+Marks?', zone, re.I)
        if not qa_match or not qb_match or qb_match.start() <= qa_match.end():
            raise AssertionError(f'{year} {level} P1 Text {text_no}: bad A/B boundary')
        qa = zone[qa_match.end():qb_match.start()]
        qa = re.sub(r'(?is)Candidates\s+may\s+NOT.*$', '', qa)
        qa = re.sub(r'(?is)Answer\s+only\s+ONE.*$', '', qa)
        qb = remove_footer(zone[qb_match.end():])
        title, attribution = source_heading(doc[page_index - 1], text_no)
        source = paper_source(f'TEXT {text_no}', title, [page_index, page_index + 1], attribution)
        roman = split_roman_parts(qa)
        if level == 'hl':
            for suffix in ROMANS:
                question = clean_prompt(roman[suffix])
                put(f't{text_no}-a-{suffix}', question,
                    source=source if source_needed(question) else None,
                    topic='english-10-0')
        else:
            for suffix in ('i', 'ii'):
                question = clean_prompt(roman[suffix])
                put(f't{text_no}-a-{suffix}', question,
                    source=source if source_needed(question) else None,
                    topic='english-10-0')
            third = roman['iii']
            part_a = re.search(r'\(a\)\s*', third, re.I)
            part_b = re.search(r'\(b\)\s*', third, re.I)
            if not part_a or not part_b or part_b.start() <= part_a.end():
                raise AssertionError(f'{year} OL P1 Text {text_no}: missing QA(iii)(a)/(b)')
            for suffix, body in (
                ('iii-a', third[part_a.end():part_b.start()]),
                ('iii-b', third[part_b.end():]),
            ):
                question = clean_prompt(body)
                put(f't{text_no}-a-{suffix}', question,
                    source=source if source_needed(question) else None,
                    topic='english-10-0')
        put(f't{text_no}-b', clean_prompt(qb), topic='english-10-1')

    page = clean_unicode(doc[7].get_text('text'))
    options = split_numbered(page, range(1, 8))
    for number, body in options.items():
        put(f'composing-{number}', clean_prompt(remove_footer(body)), topic='english-9-1')


def unseen_poet(raw: str) -> str:
    """Extract a poet's printed name without swallowing the prose after it."""
    person = r"([A-Z][A-Za-zÀ-ž.'-]+(?:\s+[A-Z][A-Za-zÀ-ž.'-]+){1,3})"
    for pattern in (
        rf'\bpoet,\s+{person}\s*,',
        rf'[”"]\s*,?\s*{person}\s+considers\b',
        rf'\bby\s+{person}(?=\s*(?:,|and\b|carefully\b|below\b|\.))',
        rf'\bpoem,\s+{person}\s+fondly\b',
    ):
        match = re.search(pattern, raw)
        if match:
            return compact(match.group(1))
    standalone = re.findall(rf'(?m)^\s*{person}\s*$', raw)
    if standalone:
        return compact(standalone[-1])
    raise AssertionError('could not identify unseen-poem author')


def add_hl_p2(year: int, doc: fitz.Document, put) -> None:
    for letter, group in work_groups(doc).items():
        parts = split_roman_parts(group, expected=2)
        title = title_before_marker(group, re.search(r'(?m)^\s*\(i\)', group).group(0))
        topic = closest_topic(title.split('–')[0].split('-')[0], WORK_TOPICS, 'english-6-0')
        stem = WORK_LABELS.get(topic, title)
        for roman in ('i', 'ii'):
            put(f'single-{letter}-{roman}', clean_prompt(parts[roman]), stem=stem, topic=topic)

    combined = '\n'.join(strip_furniture_lines(doc[index].get_text('text')) for index in (3, 4))
    mode_matches = list(re.finditer(
        r'(?mi)^\s*([ABC])\s+(THEME(?:\s+OR\s+ISSUE)?|LITERARY\s+GENRE|CULTURAL\s+CONTEXT|GENERAL\s+VISION\s+AND\s+VIEWPOINT)\s*$',
        combined))
    if len(mode_matches) != 3:
        raise AssertionError(f'{year} HL P2: found {len(mode_matches)} comparative modes')
    mode_topics = {
        'theme or issue': 'english-7-0', 'theme': 'english-7-0',
        'literary genre': 'english-7-2',
        'cultural context': 'english-7-3',
        'general vision and viewpoint': 'english-7-4',
    }
    for index, match in enumerate(mode_matches):
        end = mode_matches[index + 1].start() if index + 1 < len(mode_matches) else len(combined)
        chunk = combined[match.end():end]
        q1_match = re.search(r'(?m)^\s*1\.\s+', chunk)
        if not q1_match:
            raise AssertionError(f'{year} HL P2 mode {match.group(1)}: missing Q1')
        q1, q2 = split_or_number_two(chunk[q1_match.end():])
        topic = mode_topics[comparable(match.group(2))]
        stem = compact(match.group(2).title())
        letter = match.group(1).lower()
        put(f'comparative-{letter}-q1', clean_prompt(q1), stem=stem, topic=topic)
        put(f'comparative-{letter}-q2', clean_prompt(q2), stem=stem, topic=topic)

    unseen = clean_unicode(doc[5].get_text('text'))
    q1_match = re.search(r'(?m)^\s*1\.\s+', unseen)
    if not q1_match:
        raise AssertionError(f'{year} HL P2: missing unseen Q1')
    q1, q2_tail = split_or_number_two(unseen[q1_match.end():])
    mark = re.search(r'\(\s*20\s*\)', q2_tail)
    q2 = q2_tail[:mark.end()] if mark else q2_tail
    author = unseen_poet(unseen)
    title_match = re.search(r'[‘\'"]([^’\'"]+)[’\'"]', unseen[:q1_match.start()])
    if title_match:
        poem_title = compact(title_match.group(1))
    else:
        after_questions = q2_tail[mark.end():] if mark else ''
        poem_title = first_meaningful_line(after_questions) or 'Unseen poem'
    source = paper_source('UNSEEN POEM', poem_title, [6], f'{poem_title} — {author}.')
    put('unseen-q1', clean_prompt(q1), source=source, topic='english-8-2')
    put('unseen-q2', clean_prompt(q2), source=source, topic='english-8-2')

    prescribed = clean_unicode(doc[6].get_text('text'))
    start = re.search(r'Candidates\s+must\s+answer\s+one.*?\(1\s*[–—-]\s*5\)\.', prescribed, re.I | re.S)
    body = prescribed[start.end():] if start else prescribed
    questions = split_numbered(body, range(1, 6))
    for number, raw in questions.items():
        lines = [compact(line) for line in raw.splitlines() if compact(line)]
        poet = lines[0]
        question = clean_prompt('\n'.join(lines[1:]))
        put(f'prescribed-{number}', question, stem=poet,
            topic=closest_topic(poet, POET_TOPICS, 'english-8-0'))


def page_after_instruction(page: fitz.Page, pattern: str) -> tuple[str, str]:
    raw = clean_unicode(page.get_text('text'))
    match = re.search(pattern, raw, re.I | re.S)
    if not match:
        raise AssertionError(f'page {page.number + 1}: instruction not found')
    return raw[:match.start()], remove_footer(raw[match.end():])


def ordinary_unseen_identity(raw: str) -> tuple[str, str]:
    """Read the poem identity across both OL page layouts used since 2021."""
    quoted = re.search(
        r"Read\s+the\s+poem\s+[‘'\"]([^’'\"]+)[’'\"]\s+by\s+([^\n]+?)\s+below",
        raw, re.I)
    if quoted:
        return compact(quoted.group(1)), compact(quoted.group(2))

    author = unseen_poet(raw)

    # In the questions-first layout, the title is the first standalone line
    # after the second printed 10-mark tariff.
    after_tariff = list(re.finditer(r'\(\s*10\s*\)\s*\n+\s*([^\n]+)', raw))
    title = compact(after_tariff[-1].group(1)) if after_tariff else ''
    if not title or not author:
        raise AssertionError(
            f'could not identify OL unseen poem title/author: {title!r} / {author!r}')
    return title, author


def add_ol_p2(year: int, doc: fitz.Document, put) -> None:
    for index, letter in enumerate(LETTERS_9, 1):
        head, body = page_after_instruction(
            doc[index], r'Answer\s+any\s+two\s+of\s+the\s+following\s+four\s+questions\.[^\n]*')
        questions = split_numbered(body, range(1, 5))
        head_lines = [compact(line) for line in head.splitlines() if compact(line)]
        identity = compact(' '.join(
            line for line in head_lines
            if not re.match(
                r'^(Leaving|English|SECTION|THE SINGLE TEXT|Candidates|\(?\d+\s+MARKS)',
                line, re.I)
            and not re.fullmatch(r'[A-I]|\d+', line)))
        identity = re.sub(r'^[A-I]\s+', '', identity)
        topic = closest_topic(identity, WORK_TOPICS, 'english-6-0')
        stem = WORK_LABELS.get(topic, identity)
        for number, question in questions.items():
            put(f'single-{letter}-q{number}', clean_prompt(question),
                stem=stem, topic=topic)

    mode_topics = {
        'theme': 'english-7-0', 'theme or issue': 'english-7-0',
        'hero heroine villain': 'english-7-5',
        'relationships': 'english-7-6', 'social setting': 'english-7-7',
        'cultural context': 'english-7-3',
        'general vision and viewpoint': 'english-7-4',
    }
    for offset, letter in enumerate('abc', 10):
        raw = clean_unicode(doc[offset].get_text('text'))
        q1_match = re.search(r'(?m)^\s*1\.\s+', raw)
        if not q1_match:
            raise AssertionError(f'{year} OL P2 comparative {letter}: missing Q1')
        prefix = raw[:q1_match.start()]
        title_match = re.search(
            rf'(?mi)^\s*{letter.upper()}\s+(THEME(?:\s+OR\s+ISSUE)?|HERO,?\s+HEROINE,?\s+VILLAIN|SOCIAL\s+SETTING|RELATIONSHIPS|CULTURAL\s+CONTEXT|GENERAL\s+VISION\s+AND\s+VIEWPOINT)\s*$',
            prefix)
        if not title_match:
            raise AssertionError(f'{year} OL P2 comparative {letter}: missing mode heading')
        stem = compact(title_match.group(1).title())
        topic = mode_topics[comparable(title_match.group(1))]
        q1, q2 = split_or_number_two(remove_footer(raw[q1_match.end():]))
        put(f'comparative-{letter}-q1', clean_prompt(q1), stem=stem, topic=topic)
        put(f'comparative-{letter}-q2', clean_prompt(q2), stem=stem, topic=topic)

    unseen = clean_unicode(doc[13].get_text('text'))
    poem_title, author = ordinary_unseen_identity(unseen)
    q1_match = list(re.finditer(r'(?m)^\s*1\.\s+', unseen))[-1]
    questions = split_numbered(unseen[q1_match.start():], (1, 2))
    source = paper_source('UNSEEN POEM', poem_title, [14], f'{poem_title} — {author}.')
    for number, question in questions.items():
        put(f'unseen-q{number}', clean_prompt(before_mark(question, 10)),
            source=source, topic='english-8-2')

    for page_index, letter in zip(range(14, 20), LETTERS_6):
        page = doc[page_index]
        blocks = page.get_text('blocks')
        start = next((index for index, block in enumerate(blocks)
                      if re.search(r'(?m)^\s*1\.\s*$', block_text(block))
                      or (re.search(r'(?m)^\s*1\.\s*', block_text(block))
                          and re.search(r'\(a\)', block_text(block), re.I))), None)
        if start is None:
            raise AssertionError(f'{year} OL P2 page {page_index + 1}: no prescribed Q1')
        selected: list[str] = []
        for block in blocks[start:]:
            selected.append(block_text(block))
            if re.search(r'(?m)^\s*\(iii\)', block_text(block), re.I):
                break
        question_zone = '\n'.join(selected)
        q2_marker = re.search(r'(?m)^\s*2\.\s*Answer\s+ONE.*$', question_zone, re.I)
        if not q2_marker:
            raise AssertionError(f'{year} OL P2 page {page_index + 1}: no prescribed Q2')
        q1_start = re.search(r'(?m)^\s*1\.\s*', question_zone)
        q1 = question_zone[q1_start.end():q2_marker.start()]
        q2 = question_zone[q2_marker.end():]
        choices = split_roman_parts(q2)
        poem_title, poet, topic = prescribed_source_identity(page, letter, question_zone)
        source = paper_source(
            f'PRESCRIBED POEM {letter.upper()}', poem_title, [page_index + 1],
            f'{poem_title} — {poet}.')
        put(f'prescribed-{letter}-q1', clean_prompt(q1),
            stem=f'{poem_title} — {poet}', source=source, topic=topic)
        for roman, question in choices.items():
            put(f'prescribed-{letter}-q2-{roman}', clean_prompt(question),
                stem=f'{poem_title} — {poet}', source=source, topic=topic)


def build() -> dict:
    with open(CENSUS_PATH, encoding='utf-8') as handle:
        census = json.load(handle)
    asks = {row['id']: row for row in census['asks']}
    cards: dict[str, dict] = {}

    for year in range(2021, 2026):
        for level in ('hl', 'ol'):
            scheme_pages = split_page_markdown(os.path.join(SCHEME_ROOT, f'{year}-{level}.md'))
            for paper in (1, 2):
                component = 100 if paper == 1 else 200
                path = os.path.join(PAPER_ROOT, f'{year}-{level}-{component}-paper.pdf')
                doc = fitz.open(path)

                def put(key: str, question: str, *, stem: str | None = None,
                        source: dict | None = None, topic: str) -> None:
                    card_id = f'english-{year}-{level}-p{paper}-{key}'
                    if card_id not in asks:
                        raise AssertionError(f'parser emitted a non-census id: {card_id}')
                    if card_id in cards:
                        raise AssertionError(f'parser emitted {card_id} twice')
                    question = clean_prompt(question)
                    if len(comparable(question).split()) < 5:
                        raise AssertionError(f'{card_id}: prompt is too short: {question!r}')
                    page_no, trace_score = question_scheme_page(question, scheme_pages)
                    ask = asks[card_id]
                    card = {
                        'id': card_id,
                        'year': year,
                        'level': 'higher' if level == 'hl' else 'ordinary',
                        'paper': paper,
                        'section': ask['section'],
                        'questionRef': ask['questionRef'],
                        'questionText': question,
                        'totalMarks': ask['marks'],
                        'printedParts': ask['printedParts'],
                        'schemePage': page_no,
                        'schemeTraceScore': trace_score,
                        'topicId': topic,
                        'conceptId': concept_for(ask['section'], question),
                        'taskRequirements': requirements_for(question, source, ask['printedParts']),
                    }
                    if stem:
                        card['stem'] = compact(stem)
                    if source:
                        card['sourceMaterial'] = source
                    cards[card_id] = card

                try:
                    if paper == 1:
                        add_p1(year, level, doc, put)
                    elif level == 'hl':
                        add_hl_p2(year, doc, put)
                    else:
                        add_ol_p2(year, doc, put)
                finally:
                    doc.close()

    missing = sorted(set(asks) - set(cards))
    extra = sorted(set(cards) - set(asks))
    if missing or extra:
        raise AssertionError(f'English card manifest mismatch; missing={missing[:20]}, extra={extra[:20]}')
    if len(cards) != 660:
        raise AssertionError(f'expected 660 English cards, built {len(cards)}')
    weak = [card['id'] for card in cards.values() if card['schemeTraceScore'] < 20]
    if weak:
        raise AssertionError(f'weak marking-scheme traces: {weak[:20]}')
    return {
        'subject': 'english',
        'sourceRule': 'Every questionText is extracted from its official SEC question paper PDF.',
        'rubricRule': 'PCLM only; indicative material is never converted to required answer rows.',
        'cardCount': len(cards),
        'cards': [cards[row['id']] for row in census['asks']],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true', help='fail if the committed manifest is stale')
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
            print(f'stale {OUT}; run english_cards.py', file=sys.stderr)
            return 1
    else:
        with open(OUT, 'w', encoding='utf-8') as handle:
            handle.write(rendered)
    print(f"English cards: {payload['cardCount']} exact prompts traced to their schemes")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
