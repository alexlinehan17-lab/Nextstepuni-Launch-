#!/usr/bin/env python3
"""2023 Higher Japanese, independently reviewed against all original pages.

Selectors below are coordinates in ja_text.page_rows, not transcribed answers.
Every question comes from the paper; every answer and tariff wording from the
scheme. Choice pools are kept whole. Run with --write to publish the manifest.
"""
import argparse
import hashlib
import json
import re
from pathlib import Path

import fitz
from ja_text import page_rows
from ja_topics import FURIGANA_NOTE, concept_for

ROOT = Path(__file__).resolve().parents[3]
PAPER = ROOT / 'examiner-reports/japanese/papers/2023-hl-000-paper.pdf'
AURAL = ROOT / 'examiner-reports/japanese/papers/2023-hl-A00-paper.pdf'
SCHEME = ROOT / 'examiner-reports/japanese/schemes/2023-hl.pdf'
PINNED_SOURCES = {
    PAPER: 'c67da4e231677defa459f6e4989a291d9d68ca8375dbdc59edd159c2392c9aab',
    AURAL: 'd7b4c83a1a8140baea8f11a586f3b8921002bac161c8850ff369f2cba0832ce2',
    SCHEME: 'be69f009c1fda57635c653bc07ccff23c88fa8be5fc3816da8ad7383f782a5ce',
}
for path, expected in PINNED_SOURCES.items():
    assert hashlib.sha256(path.read_bytes()).hexdigest() == expected, f'Source changed; review again: {path}'
DOCS = {name: fitz.open(path) for name, path in [('paper', PAPER), ('aural', AURAL), ('scheme', SCHEME)]}
ROWS = {name: [page_rows(page) for page in doc] for name, doc in DOCS.items()}
CARDS = []
FIGURES = {}
EVIDENCE = []


def cell(doc, page, row, group=None):
    groups = ROWS[doc][page - 1][row]
    text = ' '.join(group[2] for group in groups) if group is None else groups[group][2]
    EVIDENCE.append({'document': doc, 'page': page, 'row': row, 'group': group, 'text': text})
    return text


def s(page, row, group=0):
    """Answer cell, preserving scheme alternatives; remove only bullet/tariff."""
    text = cell('scheme', page, row, group)
    return re.sub(r'\s*\(\d+ marks?\)\s*$', '', text).strip().removeprefix('- ').strip()


def p(page, row, group=None):
    return cell('paper', page, row, group)


def join_cells(doc, page, rows, x_min=0):
    return ' '.join(' '.join(cell(doc, page, row, gi) for gi, group in enumerate(ROWS[doc][page - 1][row]) if group[0] >= x_min) for row in rows)


def english(text):
    return re.split(r'\s*/\s*', text.replace('\xa0', ' '), maxsplit=1)[-1].strip()


def point(text, marks=1, **extra):
    return {'kind': 'point', 'verbatim': text, 'marks': marks, **extra}


def anyn(options, count, marks=1, steps=None, **extra):
    group = {'claimMax': count, 'perOption': marks, 'options': options}
    if steps:
        group['perOptionSteps'] = steps
    return {'kind': 'anyN', 'verbatim': 'Accepted answers', 'marks': None, 'group': group, **extra}


def worth(row):
    if row['kind'] != 'anyN':
        return row['marks']
    group = row['group']
    return sum(group['perOptionSteps']) if 'perOptionSteps' in group else group['claimMax'] * group['perOption']


def source(pages, kind='source-text', component='paper'):
    return {'kind': kind, 'label': '2023 Japanese Higher Level', 'title': 'Original examination material',
            'pages': pages, 'attribution': '© State Examinations Commission.',
            **({'presentationNote': FURIGANA_NOTE} if component == 'paper' else {}),
            '_component': component}


def add(section, q, question, rows, topic, paper_pages, scheme_pages, suffix='', rubric=None, total=None, reading=None, figure=None):
    cid = f'ja-2023-hl-{section.lower()}' + (f'-{q}' if q is not None else '') + (f'-{suffix}' if suffix else '')
    ref = f'2023 HL Section {section}' + (f' Q{q}' if q is not None else '')
    if suffix:
        ref += ''.join(f'({part})' for part in suffix.split('-'))
    listening = section.startswith('L')
    card = {'id': cid, 'source': 'sec', 'subjectId': 'japanese', 'specVersion': 'lc-japanese-syllabus',
            'kind': 'rubric' if rubric else 'question', 'level': 'higher', 'year': 2023,
            'section': section[1:] if listening else section[0] if section[0] in '1234' else 'Q5',
            'topicId': topic, 'conceptId': concept_for(question, cid), 'questionRef': ref,
            'questionText': question, 'totalMarks': total if total is not None else sum(map(worth, rows)),
            'qa': {'gates': ['verbatim', 'tariff', 'figure'], 'humanReviewedBy': 'agent-verified', 'humanReviewedAt': '2026-11-09'},
            'sourceEvidence': {'component': 'aural' if listening else 'paper', 'paperPages': paper_pages, 'schemePages': scheme_pages},
            'schemeCitation': 'Marking points quoted from the SEC marking scheme, Japanese 2023 Higher Level — © State Examinations Commission.'}
    if rubric:
        card['rubric'] = rubric
    else:
        card['tariffModel'] = {'kind': 'fixed'}
        card['rows'] = [dict(row, id=f'r-{i + 1}') for i, row in enumerate(rows)]
    original_ids = set(re.findall(r'    id: "([^"]+)"', (ROOT / 'components/MarkBank/cards/japanese/higher.ts').read_text()))
    if cid in original_ids:
        card['qa']['gates'].append('reviewed-card-correction')
    # Every condition is local to its printed heading. In 2023 the
    # extraneous-material clauses do not also name an answer language.
    if listening or section == '1B':
        page, row = (3, 1) if listening else (8, 0)
        card['sourceEvidence']['generalSchemePages'] = [page]
        card['answerLanguageRule'] = {'otherLanguageMultiplier': 0.5, 'penalizedLanguage': 'Japanese',
                                      'sourceText': cell('scheme', page, row), 'schemePages': [page]}
    if section == '2A' and q == 2:
        page, row = 9, 0
        card['sourceEvidence']['generalSchemePages'] = [page]
        card['extraneousMaterialRule'] = {'multiplier': 0.5, 'sourceText': cell('scheme', page, row), 'schemePages': [page]}
    if reading:
        card['sourceMaterial'] = source(reading)
    if figure:
        card['questionFigureKey'] = figure
    CARDS.append(card)
    return card



def joined_selector(document, page, parts):
    text = ' '.join(cell(document, page, row, group) for row, group in parts)
    EVIDENCE.append({'document': document, 'page': page, 'parts': [{'row': row, 'group': group} for row, group in parts], 'text': text})
    return text


def prompt(page, rows):
    return english(' '.join(p(page, row) for row in rows))


def strip_tariff(text):
    return re.sub(r'\s*\(any.*$', '', text).strip()


def options(page, rows, separator=', '):
    return [part.strip() for part in strip_tariff(' '.join(s(page, row) for row in rows)).split(separator)]


def comprehension(section, q, suffix, question_rows, rows, scheme_pages, total=None):
    page = 3 if section == '1A' else 4 if section == '1B' else 7 if section == '2A' else 11
    topic = {'1': 'japanese-5-0', '2': 'japanese-5-2', '3': 'japanese-5-1'}[section[0]]
    text = prompt(page, question_rows)
    if section == '3B':
        text = p(page, question_rows[0], 1)
    if section == '2A' and q == 2:
        text = re.sub(r'^\([ivx]+\)\s*', '', ' '.join(p(page, row, 1) if len(ROWS['paper'][page - 1][row]) > 1 else p(page, row) for row in question_rows))
    card = add(section, q, text, rows, topic, [page], scheme_pages, suffix or '', total=total,
               reading={'1A': [2], '1B': [4], '2A': [6], '3A': [10], '3B': [10]}[section])
    if section == '2A':
        card['stem'] = english(p(7, 5 if q == 2 else 12, 1))
    else:
        row = {'1A': 0, '1B': 17, '3A': 0, '3B': 15}[section]
        card['stem'] = english(p(page, row))
    return card

def crop(key, page, region, alt, component='paper'):
    doc = DOCS[component]
    sheet = doc[page - 1]
    rect = fitz.Rect(region[0] * sheet.rect.width, region[1] * sheet.rect.height, region[2] * sheet.rect.width, region[3] * sheet.rect.height)
    rel = f'/exam-figures/japanese/{key}.png'
    path = ROOT / 'public' / rel.lstrip('/')
    path.parent.mkdir(parents=True, exist_ok=True)
    sheet.get_pixmap(matrix=fitz.Matrix(2, 2), clip=rect).save(path)
    FIGURES[key] = {'src': rel, 'md5': hashlib.md5(path.read_bytes()).hexdigest(), 'alt': alt,
                    'attribution': '© State Examinations Commission.',
                    'source': {'document': component, 'page': page, 'region': region}}
    return key


def reading():
    instruction = prompt(3, [1, 2])
    labels = [p(3, row, 0) + ' ' + english(p(3, row, 1)) for row in range(4, 10)]
    add('1A', 1, instruction + '\n' + english(p(3, 3, 0)) + ' ' + p(3, 3, 1) + '\n' + '\n'.join(labels),
        [point(s(7, row, 1), contextNote=label) for row, label in zip(range(5, 11), labels)],
        'japanese-5-0', [3], [7], reading=[2])
    comprehension('1A', 2, None, [10], [anyn(options(7, [12], '/'), 2)], [7])
    discount = ' '.join(cell('scheme', 7, row, 0) for row in [15, 16])
    first, second = re.split(r'\(1 mark\s*\)', discount)[:2]
    comprehension('1A', 3, None, [12], [point(first.strip()), anyn([part.strip() for part in second.strip(' ,').split('/')], 1)], [7])
    comprehension('1A', 4, None, [14, 15], [anyn(options(7, [18], '/'), 1)], [7])
    comprehension('1A', 5, None, [17, 18], [anyn(options(7, [20], '/'), 2)], [7])
    comprehension('1A', 6, None, [20], [anyn(options(7, [22], '/'), 2)], [7])
    comprehension('1A', 7, None, [22, 23], [point(re.sub(r'\s+1 mark$', '', cell('scheme', 7, 24)))], [7])
    rows = []
    for first_row, detail_rows in [(28, [28, 29, 30]), (32, [32, 33])]:
        branch = s(7, first_row, 0)
        detail = ' '.join(s(7, row, 2 if row == first_row else 0) for row in detail_rows)
        rows += [point(s(7, first_row, 1), contextNote=branch + ' — ' + s(7, 26, 1)),
                 anyn([part.strip() for part in detail.split('/')], 2, contextNote=branch + ' — ' + s(7, 26, 2))]
    add('1A', 8, prompt(3, [25]) + '\n' + '\n'.join(p(3, row) for row in range(26, 33)), rows, 'japanese-5-0', [3], [7], reading=[2, 3],
        figure=crop('ja-2023-hl-1a-8', 3, [.065, .725, .95, .938], prompt(3, [25])))
    for q, qr, sr, steps in [(1, [18, 19], [2, 3], [2, 1]), (2, [22, 23], [6, 7], [2, 1]), (3, [26, 27], [10, 11], None)]:
        comprehension('1B', q, None, qr, [anyn(options(8, sr, '/'), 2, 2 if steps else 1, steps)], [8])
    # Required six-cell profile table: each descriptive cell has its own
    # printed any-two quota, rather than becoming unrelated fragment cards.
    rows = []
    for origin, desc, hobbies in [(20, [(19, 0), (21, 0), (24, 0)], [(20, 2), (22, 0)]),
                                  (28, [(27, 0), (29, 0), (32, 0), (34, 0)], [(28, 2), (30, 0), (33, 0)])]:
        name = s(8, origin, 0)
        detail = strip_tariff(joined_selector('scheme', 8, desc))
        hobby = strip_tariff(joined_selector('scheme', 8, hobbies))
        rows += [point(s(8, origin, 1), contextNote=name + ' — ' + s(8, 17, 0) + ' ' + s(8, 18, 0)),
                 anyn([part.strip() for part in detail.split('/')], 2, contextNote=name + ' — ' + s(8, 17, 1) + ' ' + s(8, 18, 1)),
                 anyn([part.strip() for part in hobby.split('/')], 2, contextNote=name + ' — ' + s(8, 17, 2))]
    add('2A', 1, prompt(7, [0]) + '\n' + '\n'.join(p(7, row) for row in range(1, 5)), rows, 'japanese-5-2', [7], [8], reading=[6, 7],
        figure=crop('ja-2023-hl-2a-1', 7, [.065, .03, .95, .205], prompt(7, [0])))
    for roman, qr, sr in [('i', 6, 2), ('ii', 8, 4)]:
        comprehension('2A', 2, roman, [qr], [point(s(9, sr), 2)], [9])
    third = joined_selector('scheme', 9, [(6, 0), (7, 0)])
    comprehension('2A', 2, 'iii', [10], [point(part.strip()) for part in third.split('(1 mark)')], [9])
    for roman, qr, sr in [('i', [13, 14], 11), ('iii', [18], 15), ('iv', [20, 21], 17)]:
        pieces = [part.strip() for part in cell('scheme', 9, sr, 0).split('(1 mark)') if part.strip()]
        comprehension('2A', 3, roman, qr, [point(part) for part in pieces], [9])
    comprehension('2A', 3, 'ii', [16], [{'kind': 'criterion', 'verbatim': cell('scheme', 9, 13, 0), 'marks': 2, 'permittedMarks': [0, 1, 2]}], [9])
    comprehension('2A', 3, 'v', [23, 24], [anyn(options(9, [19], '/'), 1, 2)], [9])
    translation = joined_selector('scheme', 9, [(row, 0) for row in [24, 25, 26]])
    pieces = [part.strip(' ,') for part in re.split(r'\(1\s+mark\)', translation) if part.strip(' ,')]
    add('2A', 4, prompt(7, [26]) + '\n' + p(7, 27) + ' ' + p(7, 28), [point(part) for part in pieces], 'japanese-5-2', [7], [9], reading=[6])
    for section, page, q, sp, sr in [('2B', 8, 1, 10, 2), ('2B', 8, 2, 10, 9), ('2C', 9, 1, 10, 17), ('2C', 9, 2, 11, 1)]:
        instruction = prompt(page, [1, 2] if q == 1 else [10, 11])
        labels = [p(page, row, 0) + ' ' + p(page, row, 1) for row in (range(4, 10) if q == 1 else range(13, 19))]
        answers = []
        for row in range(sr, sr + 6):
            if section == '2C' and (q == 2 or row == 17):
                answer = re.sub(r'^\([ivx]+\)\s*', '', cell('scheme', sp, row, 0))
            else:
                answer = s(sp, row, 1)
            answers.append(answer)
        groups = [{'id': f'item-{i}', 'label': label, 'rows': [{'id': 'answer', 'text': answer, 'marks': 1}]} for i, (label, answer) in enumerate(zip(labels, answers), 1)]
        guide = cell('scheme', sp, sr - 1)
        if section == '2B' and q == 1:
            guide += ' The paper repeats (vi) on the fourth and sixth items; the kanji distinguish them. Keep the six printed items in their original order.'
        add(section, q, instruction + '\n' + p(page, 3 if q == 1 else 12) + '\n' + '\n'.join(labels), [],
            'japanese-5-4' if section == '2B' else 'japanese-5-5', [page], [sp], total=5,
            rubric={'system': 'language-points', 'count': 5, 'taskRequirements': [instruction], 'groups': groups, 'markingGuideNote': guide}, reading=[6, page],
            figure=crop(f'ja-2023-hl-{section.lower()}-{q}', page,
                        {('2B', 1): [.055, .025, .97, .49], ('2B', 2): [.055, .505, .97, .935],
                         ('2C', 1): [.055, .025, .97, .46], ('2C', 2): [.055, .46, .97, .905]}[(section, q)], instruction))
    comprehension('3A', 1, None, [1], [anyn(options(11, [10], '/'), 3)], [11])
    friday = joined_selector('scheme', 11, [(13, 0), (14, 0)])
    parts = [part.strip(' ,/') for part in re.split(r'\([12] marks?\)', friday) if part.strip(' ,/')]
    comprehension('3A', 2, None, [4], [point(text, marks) for text, marks in zip(parts, [2, 1, 1])], [11])
    comprehension('3A', 3, None, [7], [anyn(options(11, [17], '/'), 1)], [11])
    comprehension('3A', 4, None, [9], [anyn(options(11, [19], '/'), 2)], [11])
    comprehension('3A', 5, None, [11, 12], [anyn(options(11, [22, 23], '/'), 2)], [11])
    for q, qr, sr in [(1, 16, 2), (3, 20, 6), (4, 22, 8)]:
        comprehension('3B', q, None, [qr], [point(s(12, sr), 2)], [12])
    weather = re.split('[、,]', strip_tariff(s(12, 4)))
    comprehension('3B', 2, None, [18], [anyn([part.strip() for part in weather], 2)], [12])
    instruction = prompt(12, [1, 2, 3])
    groups = [{'id': f'item-{i + 1}', 'label': re.sub(r'_+', '', p(12, i + 6)).strip(), 'rows': [
        {'id': 'reading', 'text': s(12, i + 10, 1) + ' ' + s(12, i + 10, 2), 'marks': 1},
        {'id': 'meaning', 'text': s(12, i + 10, 4), 'marks': 1}]} for i in range(6)]
    add('3C', None, instruction + '\n' + '\n'.join(group['label'] for group in groups), [], 'japanese-5-4', [12], [12], total=10,
        rubric={'system': 'language-points', 'count': 5, 'taskRequirements': [instruction], 'groups': groups, 'markingGuideNote': cell('scheme', 12, 9)},
        reading=[12], figure=crop('ja-2023-hl-3c', 12, [.045, .035, .98, .47], instruction))
    instruction = prompt(12, [13, 14, 15])
    groups = []
    for row in range(18, 25):
        count = 1 if row in [19, 22] else 2
        for blank, group in enumerate([1, 3][:count], 1):
            groups.append({'id': f'item-{len(groups) + 1}', 'label': p(12, row - 2) + (f' [{blank}]' if count > 1 else ''),
                           'rows': [{'id': 'particle', 'text': s(12, row, group), 'marks': 1}]})
    assert len(groups) == 12
    add('3D', None, instruction + '\n' + '\n'.join(p(12, row) for row in range(16, 23)), [], 'japanese-5-5', [12], [12], total=10,
        rubric={'system': 'language-points', 'count': 10, 'taskRequirements': [instruction], 'groups': groups, 'markingGuideNote': cell('scheme', 12, 17)},
        reading=[12], figure=crop('ja-2023-hl-3d', 12, [.045, .48, .98, .91], instruction))


def steps(maximum):
    return list(range(maximum + 1))


def writing():
    for q, pp, sp, maximum, threshold, length, lower, normal, reduced in [
        (4, 14, 14, 20, 10, 150, 15, [(0, 5), (6, 14), (15, 20)], [(0, 3), (4, 10), (11, 15)]),
        (5, 16, 17, 30, 15, 200, 20, [(0, 7), (8, 20), (21, 30)], [(0, 4), (5, 12), (13, 20)]),
    ]:
        # Both expression grids span two pages. Keep the middle band's
        # continuation before the final band starts on the next page.
        guidance = [join_cells('scheme', sp, range(16, 25), 180),
                    join_cells('scheme', sp, range(25, 30 if q == 4 else 33), 180) + ' ' + join_cells('scheme', sp + 1, range(4 if q == 4 else 2), 180),
                    join_cells('scheme', sp + 1, range(4, 12) if q == 4 else range(2, 11), 180)]
        bands = [{'label': f'{lo}–{hi}', 'marks': list(range(lo, hi + 1)), 'guidance': [text]} for (lo, hi), text in zip(normal, guidance)]
        lower_bands = [{'label': f'{lo}–{hi}', 'marks': list(range(lo, hi + 1)), 'guidance': [text]} for (lo, hi), text in zip(reduced, guidance)]
        rule = joined_selector('scheme', sp, [(row, None) for row in range(9, 13)])
        if q == 4:
            instruction = prompt(14, [1, 2])
            question = instruction + '\n' + '\n'.join([
                '(a) ' + prompt(14, [3, 4, 5]), p(14, 6), p(14, 7), english(p(14, 8)),
                '(b) ' + prompt(14, [9, 10, 11]), p(14, 12), p(14, 13), english(p(14, 14)),
                '(c) ' + prompt(14, [15, 16, 17]), p(14, 18), p(14, 19)])
            criteria = [
                {'id': 'opening', 'label': 'Opening', 'maxMarks': 1, 'permittedMarks': [0, 1], 'guidance': [s(13, 19)]},
                *[{'id': f'point-{i}', 'label': f'({i})', 'maxMarks': 9, 'permittedMarks': steps(9), 'guidance': [s(13, 18)]} for i in ['i', 'ii']],
                {'id': 'closing', 'label': 'Closing', 'maxMarks': 1, 'permittedMarks': [0, 1], 'guidance': [s(13, 20)]},
            ]
        else:
            instruction = prompt(16, range(1, 6))
            question = instruction + '\n' + '\n'.join(p(16, row) for row in range(6, 16))
            source_headings = [cell('scheme', 16, row) for row in range(9, 17)]
            criteria = [{'id': f'heading-{i}', 'label': f'Heading {i} you chose', 'maxMarks': 7, 'permittedMarks': steps(7), 'guidance': [s(16, 5)] + source_headings} for i in range(1, 5)]
            criteria.append({'id': 'discretionary', 'label': 'Discretionary marks', 'maxMarks': 2, 'permittedMarks': steps(2), 'guidance': [s(16, 6)]})
        content_ids = [criterion['id'] for criterion in criteria]
        criteria.append({'id': 'expression', 'label': s(13, 21) if q == 4 else s(16, 7), 'maxMarks': maximum,
                         'permittedMarks': steps(maximum), 'guidance': [join_cells('scheme', sp + 1, [12, 13] if q == 4 else [11, 12])], 'bands': bands,
                         'limits': [{'id': 'lower-e', 'maxMarks': lower,
                                     'when': {'any': [{'criterionIds': content_ids, 'atMost': threshold}, {'length': 'characters', 'below': length}]},
                                     'bands': lower_bands, 'guidance': [rule]}]})
        add(str(q), None, question, [], 'japanese-5-7', [pp], [sp - 1, sp, sp + 1], total=maximum * 2,
            figure=crop(f'ja-2023-hl-{q}', pp, [.045, .015, .97, .92], question),
            rubric={'system': 'language-writing', 'taskRequirements': [instruction], 'criteria': criteria,
                    'markingGuideNote': 'Assess four different selected headings once each, using the printed content and expression grid.' if q == 5 else 'Assess the one option you answered. The same printed content and expression grid applies to all three options.'})


def listening():
    def aq(page, rows):
        text = join_cells('aural', page, rows, 290)
        return re.sub(r'^(?:\d+\.\s*)?(?:\([ivx]+\)\s*)?(?:\([a-f]\)\s*)?', '', text).strip().replace('self- introduction', 'self-introduction')

    def listen(part, q, suffix, question_rows, rows, question=None):
        pp, sp = {'A': (2, 3), 'B': (3, 4), 'C': (4, 5), 'D': (5, 6)}[part]
        card = add('L' + part, q, question or aq(pp, question_rows), rows,
                   {'A': 'japanese-6-2', 'B': 'japanese-6-0', 'C': 'japanese-6-2', 'D': 'japanese-6-1'}[part], [pp], [sp], suffix or '')
        card['sourceMaterial'] = source([pp], 'source-question', 'aural')
        card['stem'] = join_cells('aural', pp, [1, 2], 290)
        if part == 'B':
            card['stem'] += '\n' + join_cells('aural', pp, [3 if q == 1 else 27], 290)
        if part == 'C':
            card['stem'] += '\n' + join_cells('aural', pp, [{1: 3, 2: 16, 3: 26}[q]], 290)
        if suffix and re.fullmatch(r'[a-b]-[ivx]+', suffix):
            letter, roman = suffix.split('-')
            card['questionRef'] = f'2023 HL Section L{part}' + (f' Q{q}' if q is not None else '') + f'({roman})({letter})'
        return card

    headers = [joined_selector('aural', 2, [(row, 0) for row in range(7, 11)]),
               joined_selector('aural', 2, [(6, 1), (7, 1)]),
               english(joined_selector('aural', 2, [(5, 2), (6, 2)])),
               english(joined_selector('aural', 2, [(5, 3), (6, 3)]))]
    def selected(parts):
        return joined_selector('scheme', 3, parts)
    claire = [point(s(3, 11, 1)), anyn([part.strip() for part in selected([(11, 2), (12, 0), (14, 0)]).split('/')], 1),
              anyn([part.strip() for part in selected([(11, 3), (12, 1), (14, 1)]).split('/')], 2),
              anyn([part.strip() for part in selected([(11, 4), (12, 2), (14, 2), (15, 0), (17, 0)]).split('/')], 2)]
    merged_ben = cell('scheme', 3, 21, 1)
    positive_tail, negative_middle = merged_ben.split(' (who speak', 1)
    positive = s(3, 20, 3) + ' ' + positive_tail + ' ' + s(3, 23, 0)
    negative = s(3, 20, 4) + ' (who speak' + negative_middle + ' ' + selected([(23, 1), (25, 0), (27, 0), (28, 0)])
    ben = [point(s(3, 20, 1)), anyn([part.strip() for part in selected([(20, 2), (21, 0)]).split('/')], 1),
           anyn([part.strip() for part in positive.split('/')], 2), anyn([part.strip() for part in negative.split('/')], 2)]
    place, positive_start = cell('scheme', 3, 30, 2).split(' Food is', 1)
    place += ' ' + selected([(31, 0), (33, 0)])
    positive = 'Food is' + positive_start + ' ' + selected([(31, 1), (33, 1)])
    negative = selected([(30, 3), (31, 2), (33, 2), (34, 0), (36, 0), (37, 0)])
    pam = [point(s(3, 30, 1)), anyn([part.strip() for part in place.split('/')], 1),
           anyn([part.strip() for part in positive.split('/')], 2), anyn([part.strip() for part in negative.split('/')], 2)]
    for q, rows in enumerate([claire, ben, pam], 1):
        for row, header in zip(rows, headers):
            row['contextNote'] = header
        question = cell('aural', 2, 3, 1) + '\n' + cell('aural', 2, q + 10) + '\n' + '\n'.join(headers)
        listen('A', q, None, [], rows, question)
    listen('B', 1, 'i', [4], [point(s(4, 3))])
    listen('B', 1, 'ii', [6], [anyn(options(4, [5], '/'), 3)])
    listen('B', 1, 'a-iii', [9, 10], [point(s(4, 7))])
    listen('B', 1, 'b-iii', [13, 15], [anyn(options(4, [9], '/'), 2, 2, [2, 1])])
    listen('B', 1, 'a-iv', [18], [point(s(4, 12))])
    listen('B', 1, 'b-iv', [22], [point(s(4, 14))])
    phone = listen('B', 1, 'v', [25], [point(s(4, 16), 3)])
    phone['questionFigureKey'] = crop('ja-2023-hl-lb-1-v', 3, [.51, .525, .95, .592], phone['questionText'], 'aural')
    listen('B', 2, 'i', [28], [anyn([part for part in options(4, [19], '/') if part], 2, 2, [2, 1])])
    gifts = [point(s(4, 23, 0), contextNote=s(4, 23, 1)), point(s(4, 24, 1), contextNote=s(4, 24, 0)), point(s(4, 25, 0), contextNote=s(4, 25, 1))]
    gift = listen('B', 2, 'ii', [31, 32, 33, 34, 35], gifts)
    gift['questionFigureKey'] = crop('ja-2023-hl-lb-2-ii', 3, [.51, .69, .95, .86], gift['questionText'], 'aural')
    ranking = [point(s(5, row, group), contextNote=s(5, row, 0) + ' — ' + (s(5, 3, 1) + ' ' + s(5, 4, 1) if group == 2 else s(5, 3, 0).removeprefix('Rank ') + ' ' + s(5, 4, 0))) for row, group in [(5, 2), (6, 1), (7, 1), (7, 2)]]
    rank = listen('C', 1, 'i', [4, 5, 6, 7, 8, 9, 10], ranking)
    rank['questionFigureKey'] = crop('ja-2023-hl-lc-1-i', 4, [.5, .14, .97, .342], rank['questionText'], 'aural')
    listen('C', 1, 'ii', [12, 13], [anyn(options(5, [10], '/'), 2, 2, [2, 1])])
    listen('C', 2, 'i', [18], [point(s(5, 14), 2)])
    listen('C', 2, 'ii', [20], [anyn(options(5, [16]), 2, 2)])
    listen('C', 2, 'iii', [23], [point(s(5, 19), 2)])
    listen('C', 3, 'i', [28, 30, 32], [anyn([part.strip() for part in strip_tariff(s(5, 22, 1)).split('/')], 2, contextNote=s(5, 22, 0)), point(s(5, 23, 1), contextNote=s(5, 23, 0))])
    listen('C', 3, 'ii', [34], [anyn(options(5, [25], '/'), 2, 2, [2, 1])])
    listen('D', None, 'i', [3, 4], [anyn(options(6, [2, 3]), 3)])
    listen('D', None, 'ii', [7], [anyn(options(6, [5, 6], '/'), 1, 2)])
    listen('D', None, 'iii', [13], [anyn(options(6, [8, 9], '/'), 3)])
    for letter, qr, sr in [('a', 20, 11), ('b', 25, 13)]:
        answers = [part.strip() for part in s(6, sr).split('?', 1)[1].split('/')]
        listen('D', None, letter + '-iv', [18, qr], [anyn(answers, 2)])
    listen('D', None, 'v', [31], [anyn(options(6, [16], '/'), 2)])
    date = [part.strip() for part in cell('scheme', 6, 18, 0).split('(1 mark)') if part.strip()]
    listen('D', None, 'vi', [35], [point(part) for part in date])
    listen('D', None, 'vii', [39], [point(s(6, 20), 2)])
    uniform = joined_selector('scheme', 6, [(22, 0), (23, 0)])
    listen('D', None, 'viii', [42], [{'kind': 'criterion', 'verbatim': uniform, 'marks': 3, 'permittedMarks': [0, 1, 2, 3],
            'contextNote': 'Use the published subtotal: two accepted uniform details earn 2 + 1. Three correct colours alone earn 1 instead; do not add that alternative to the full answer.'}])
    listen('D', None, 'ix', [49], [point(s(6, 25))])


def consolidations(census):
    records = []
    romans = ['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii']
    for suffix, count, pp, pr, sp, sr, reason in [
        ('1a-1', 6, 3, [1, 2], 7, 4, 'One required six-cell matching table, priced one mark per cell; all six original items remain on one task.'),
        ('2b-1', 6, 8, [1, 2], 10, 1, 'One printed any-five-of-six meaning pool; all six items and five claim slots remain together.'),
        ('2b-2', 6, 8, [10, 11], 10, 8, 'One printed any-five-of-six reading pool; all six items and five claim slots remain together.'),
        ('2c-1', 6, 9, [1, 2], 10, 16, 'One printed any-five-of-six grammar pool; all six items and five claim slots remain together.'),
        ('2c-2', 6, 9, [10, 11], 11, 0, 'One printed any-five-of-six grammar pool; all six items and five claim slots remain together.'),
        ('3c', 6, 12, [1, 2, 3], 12, 9, 'One printed any-five-of-six paired reading-and-meaning pool, one mark for each component.'),
        ('3d', 7, 12, [13, 14, 15], 12, 17, 'One printed any-ten-of-twelve-blank pool across seven numbered sentences, one mark per blank.'),
    ]:
        canonical = 'ja-2023-hl-' + suffix
        paper_text = joined_selector('paper', pp, [(row, None) for row in pr])
        scheme_text = cell('scheme', sp, sr)
        task = next(task for task in census['tasks'] if canonical == 'ja-2023-hl-' + '-'.join(str(part).lower() for part in task['key'] if part is not None))
        records.append({'canonicalId': canonical, 'legacyIds': [canonical + '-' + part for part in romans[:count]],
                        'taskKey': task['key'], 'marks': task['marks'], 'reason': reason,
                        'paperEvidence': {'page': pp, 'text': paper_text}, 'schemeEvidence': {'page': sp, 'text': scheme_text}})
    return records


def build():
    reading()
    writing()
    listening()
    census = json.loads((Path(__file__).parent / 'reviews/japanese-2023-hl-census.json').read_text())
    expected = {'ja-2023-hl-' + '-'.join(str(part).lower() for part in task['key'] if part is not None): task for task in census['tasks']}
    assert set(expected) == {card['id'] for card in CARDS}
    for card in CARDS:
        task = expected[card['id']]
        assert card['totalMarks'] == task['marks'], (card['id'], card['totalMarks'], task['marks'])
        assert card['sourceEvidence']['paperPages'] == task['paperPages']
        assert card['sourceEvidence']['schemePages'] == task['schemePages']
        if 'paperRef' in task:
            assert card['questionRef'] == task['paperRef']
    assert len(CARDS) == 67, len(CARDS)
    assert sum(card['totalMarks'] for card in CARDS) == 300
    return {'subjectId': 'japanese', 'sitting': '2023-hl', 'reviewedAt': '2026-11-09',
            'sources': [{'document': name, 'path': str(path.relative_to(ROOT)), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'pagesReviewed': list(range(1, len(DOCS[name]) + 1))} for name, path in [('paper', PAPER), ('aural', AURAL), ('scheme', SCHEME)]],
            'cards': CARDS, 'selectors': EVIDENCE, 'status': 'source-reviewed-browser-qa-pending',
            'choiceAnalysis': census['choiceBoundaries'], 'consolidations': consolidations(census)}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    result = build()
    if args.write:
        (ROOT / 'scripts/markbank/authoring/reviews/japanese-2023-hl.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
        manifest = ROOT / 'components/MarkBank/figures-japanese.json'
        previous = json.loads(manifest.read_text())
        previous.update(FIGURES)
        manifest.write_text(json.dumps(previous, ensure_ascii=False, indent=2) + '\n')
        scheme_md = SCHEME.with_suffix('.md')
        marker = '\n## Audited original table columns — 2023 HL pages 3 and 8\n'
        original = scheme_md.read_text().split(marker)[0]
        columns = []
        for page, bounds in [(3, [(96, 172), (173, 259), (260, 404), (404, 550)]),
                             (8, [(266, 373), (373, 550)])]:
            for x0, x1 in bounds:
                columns.append(DOCS['scheme'][page - 1].get_text(clip=fitz.Rect(x0, 0, x1, 780), sort=True))
        scheme_md.write_text(original + marker + '\n'.join(columns))
    print(json.dumps({'cards': len(CARDS), 'marks': sum(card['totalMarks'] for card in CARDS), 'figures': len(FIGURES)}, indent=2))
