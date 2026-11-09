#!/usr/bin/env python3
"""2017 Higher Japanese, independently reviewed against all original pages.

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
PAPER = ROOT / 'examiner-reports/japanese/papers/2017-hl-000-paper.pdf'
AURAL = ROOT / 'examiner-reports/japanese/papers/2017-hl-A00-paper.pdf'
SCHEME = ROOT / 'examiner-reports/japanese/schemes/2017-hl.pdf'
PINNED_SOURCES = {
    PAPER: 'e96083ac6d83286da7ad5e1172a3094819339d01cfe1acda36e4abeed1762a0e',
    AURAL: 'e41a80ce4085d666477710f6b43d95d6be317c11949c1ca0e98c52a29d53d0ab',
    SCHEME: '601de9e56949ad7147ce4a6ffcb2ed009d4656898b15b84a269e9d9ca82535d1',
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
    return text.replace('\xa0', ' ').rsplit('/', 1)[-1].strip()


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


def row_total(rows):
    routes = {}
    common = 0
    for row in rows:
        if row.get('route'):
            routes[row['route']] = routes.get(row['route'], 0) + worth(row)
        else:
            common += worth(row)
    return common + max([0, *routes.values()])


def source(pages, kind='source-text', component='paper'):
    return {'kind': kind, 'label': '2017 Japanese Higher Level', 'title': 'Original examination material',
            'pages': pages, 'attribution': '© State Examinations Commission.',
            **({'presentationNote': FURIGANA_NOTE} if component == 'paper' else {}),
            '_component': component}


def add(section, q, question, rows, topic, paper_pages, scheme_pages, suffix='', rubric=None, total=None, reading=None, figure=None):
    cid = f'ja-2017-hl-{section.lower()}' + (f'-{q}' if q is not None else '') + (f'-{suffix}' if suffix else '')
    ref = f'2017 HL Section {section}' + (f' Q{q}' if q is not None else '')
    if suffix:
        ref += (' Q' if q is None else '') + ''.join(f'({part})' for part in suffix.split('-'))
    listening = section.startswith('L')
    card = {'id': cid, 'source': 'sec', 'subjectId': 'japanese', 'specVersion': 'lc-japanese-syllabus',
            'kind': 'rubric' if rubric else 'question', 'level': 'higher', 'year': 2017,
            'section': section[1:] if listening else section[0] if section[0] in '1234' else 'Q5',
            'topicId': topic, 'conceptId': concept_for(question, cid), 'questionRef': ref,
            'questionText': question, 'totalMarks': total if total is not None else row_total(rows),
            'qa': {'gates': ['verbatim', 'tariff', 'figure'], 'humanReviewedBy': 'agent-verified', 'humanReviewedAt': '2026-11-09'},
            'sourceEvidence': {'component': 'aural' if listening else 'paper', 'paperPages': paper_pages, 'schemePages': scheme_pages},
            'schemeCitation': 'Marking points quoted from the SEC marking scheme, Japanese 2017 Higher Level — © State Examinations Commission.'}
    if rubric:
        card['rubric'] = rubric
    else:
        card['tariffModel'] = {'kind': 'fixed'}
        card['rows'] = [dict(row, id=f'r-{i + 1}') for i, row in enumerate(rows)]
    original_ids = set(re.findall(r'    id: "([^"]+)"', (ROOT / 'components/MarkBank/cards/japanese/higher.ts').read_text()))
    if cid in original_ids:
        card['qa']['gates'].append('reviewed-card-correction')
    language = None
    if listening:
        language = (3, 1, 'Japanese')
    elif section == '1B':
        language = (7, 0, 'Japanese')
    if section == '2A' and q == 2 or section == '3B':
        page, row = (7, 28) if section == '2A' else (9, 24)
        card['extraneousMaterialRule'] = {'multiplier': 0.5, 'sourceText': cell('scheme', page, row), 'schemePages': [page]}
        card['sourceEvidence']['generalSchemePages'] = [page]
    if language:
        page, row, named = language
        card['sourceEvidence']['generalSchemePages'] = [page]
        card['answerLanguageRule'] = {'otherLanguageMultiplier': 0.5, 'penalizedLanguage': named,
                                      'sourceText': cell('scheme', page, row), 'schemePages': [page]}
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
    return re.sub(r'\s*\(any.*$', '', text, flags=re.I).strip()


def options(page, rows, separator=', '):
    return [part.strip() for part in strip_tariff(' '.join(s(page, row) for row in rows)).split(separator)]


def comprehension(section, q, suffix, question_rows, rows, scheme_pages):
    page = 3 if section == '1A' else 4 if section == '1B' else 7 if section == '2A' else 11
    topic = 'japanese-5-0' if section.startswith('1') else 'japanese-5-2' if section == '2A' else 'japanese-5-1'
    text = prompt(page, question_rows)
    if section == '3B' or section == '2A' and q == 2:
        text = ' '.join(p(page, row, len(ROWS['paper'][page - 1][row]) - 1) for row in question_rows)
        text = re.sub(r'^(?:[1-3]\.|\([ivx]+\))\s*', '', text)
    card = add(section, q, text, rows, topic, [page], scheme_pages, suffix or '',
               reading={'1A': [2], '1B': [4], '2A': [6], '3A': [10], '3B': [10]}[section])
    instruction_row = (11 if q == 2 else 18) if section == '2A' else {'1A': 0, '1B': 19, '3A': 0, '3B': 21}[section]
    card['stem'] = english(p(page, instruction_row))
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


def clean_tariff(text):
    return re.sub(r'\s*\(?\d+\s*marks?\)?\s*$', '', text).strip()


def selected(page, parts):
    return joined_selector('scheme', page, parts)


def split_marks(text, marks=1):
    return [part.strip(' ,-/.' ) for part in re.split(rf'\({marks}\s+marks?\)', text) if part.strip(' ,-/.' )]


def group_rows(card, groups):
    card['taskGroups'] = [
        {'sourceCardId': card['id'] + '-' + name, 'label': label,
         'marks': row_total(card['rows'][start:end]),
         'rowIds': [row['id'] for row in card['rows'][start:end]]}
        for name, label, start, end in groups]


def complete_pool(count, labels, answers, instruction, guide):
    return {'system': 'language-points', 'count': count, 'taskRequirements': [instruction],
            'groups': [{'id': f'item-{i + 1}', 'label': label, 'rows': [{'id': 'answer', 'text': answer, 'marks': 1}]}
                       for i, (label, answer) in enumerate(zip(labels, answers))], 'markingGuideNote': guide}


def listening():
    def listen(part, q, suffix, qr, rows, question=None):
        pp = {'A': 2, 'B': 3, 'C': 4, 'D': 5}[part]
        sp = 3 if part == 'A' or part == 'B' and q == 1 else 5 if part == 'D' else 4
        text = question or re.sub(r'^\([ivx]+\)\s*', '', join_cells('aural', pp, qr, 300)).strip()
        card = add('L' + part, q, text, rows, {'A': 'japanese-6-1', 'B': 'japanese-6-2', 'C': 'japanese-6-0', 'D': 'japanese-6-0'}[part], [pp], [sp], suffix or '')
        card['sourceMaterial'] = source([pp], 'source-question', 'aural')
        card['stem'] = join_cells('aural', pp, range(1, 5 if part in 'AD' else 6), 300)
        if part != 'A':
            row = {('B', 1): 6, ('B', 2): 24, ('C', 1): 6, ('C', 2): 14, ('C', 3): 21, ('D', 1): 5, ('D', 2): 21}[(part, q)]
            card['stem'] += '\n' + join_cells('aural', pp, [row], 300)
        return card
    first_headers = cell('aural', 2, 9, 0).split('How')
    last_headers = cell('aural', 2, 9, 1).split('What')
    headers = [first_headers[0].strip(), 'How' + first_headers[1] + ' ' + cell('aural', 2, 10, 0),
               last_headers[0].strip(), 'What' + last_headers[1] + ' ' + cell('aural', 2, 10, 1)]
    names = [cell('aural', 2, row) for row in [11, 12, 13]]
    third = selected(3, [(13, 4), (14, 3), (15, 0)]).split('/')
    assert len(third) == 5
    third_options = [value.strip() for value in third[:3]] + [' / '.join(value.strip() for value in third[3:])]
    values = [
        [[point(s(3, 7, 1))], [point(s(3, 7, 2))], [point(s(3, 7, 3))], [anyn(s(3, 7, 4).split('/'), 2)]],
        [[point(s(3, 9, 1), 2)], [point(s(3, 9, 2))], [point(s(3, 9, 3)), point(s(3, 11, 0))],
         [anyn(selected(3, [(9, 4), (10, 3), (11, 1)]).split('/'), 2)]],
        [[point(s(3, 13, 1), 2)], [point(s(3, 13, 2))], [point(s(3, 13, 3))],
         [anyn(third_options, 2, contextNote='The single 美術館 in the original transcript identifies art gallery/museum as alternative renderings of one place; count it once. This grouping is a source-context interpretation. The separately printed bus tour and sightseeing options remain independent within the two-detail quota.')]],
    ]
    rows, groups = [], []
    for person, cells in enumerate(values):
        for column, components in enumerate(cells):
            label = names[person] + ' — ' + headers[column]
            start = len(rows)
            for row in components:
                row['contextNote'] = label + (' — ' + row['contextNote'] if row.get('contextNote') else '')
                rows.append(row)
            groups.append((f'person-{person + 1}-cell-{column + 1}', label, start, len(rows)))
    question = '\n'.join(headers + names)
    table = listen('A', None, None, [], rows, question)
    cell('scheme', 15, 34)  # Exact transcript proof for the one 美術館 concept.
    table['sourceEvidence']['interpretiveSchemePages'] = [15]
    group_rows(table, groups)
    table['questionFigureKey'] = crop('ja-2017-hl-la', 2, [.075, .18, .97, .74], question, 'aural')
    listen('B', 1, 'i', [8], [point(s(3, 20), 2)])
    listen('B', 1, 'ii', [11], [anyn(s(3, 22).split('/'), 2, 1, [2, 1], contextNote=cell('scheme', 3, 23))])
    directions = s(3, 25)
    components = re.split(r'\(\d+ marks?\)', directions)
    listen('B', 1, 'iii', [15, 16], [point(text.strip(' /'), marks) for text, marks in zip(components[:3], [2, 1, 1])])
    listen('B', 1, 'iv', [19], [point(s(3, 27), 2)])
    phone = listen('B', 1, 'v', [21], [point(s(3, 29), 4, contextNote='The scheme prices the complete number at 4 marks. The original grid has seven missing digits; no per-digit tariff is printed.')])
    cell('scheme', 3, 30)
    phone['questionFigureKey'] = crop('ja-2017-hl-lb-1-v', 3, [.53, .53, .965, .616], phone['questionText'], 'aural')
    listen('B', 2, 'i', [25], [anyn(s(4, 2).split('/'), 2, 2)])
    listen('B', 2, 'ii', [29], [anyn(s(4, 5).split('/'), 2, 2)])
    listen('B', 2, 'iii', [33, 34], [point(s(4, 8), 2)])
    listen('C', 1, 'i', [7], [anyn(s(4, 12).split('/'), 2, 2)])
    listen('C', 1, 'ii', [11, 12], [point(s(4, 15), 2)])
    listen('C', 2, 'i', [15, 16], [point(s(4, 18), 2), anyn(s(4, 19).split('/'), 1, 2)])
    listen('C', 2, 'ii', [19], [point(s(4, 21), 2)])
    listen('C', 3, 'i', [22], [point(s(4, 24), 2), anyn(s(4, 25).split('/'), 1)])
    listen('C', 3, 'ii', [25], [point(answer) for answer in split_marks(s(4, 27))])
    full = s(4, 29).split(',')
    partial = s(4, 31).split(',')
    listen('C', 3, 'iii', [28], [point(full[0].strip(), 2, kind='criterion', permittedMarks=[0, 1, 2], contextNote=partial[0].strip()),
        point(full[1].strip(), 1, contextNote=partial[1].strip())])
    listen('D', 1, 'i', [6, 7], [anyn(options(5, [3], '/'), 2, 2)])
    listen('D', 1, 'ii', [10, 11], [point(s(5, 6), 3)])
    listen('D', 1, 'iii', [14, 15], [anyn(options(5, [9], '/'), 2)])
    listen('D', 1, 'iv', [18, 19], [point(s(5, 11), 2, kind='criterion', permittedMarks=[0, 1, 2], contextNote=s(5, 12))])
    listen('D', 2, 'i', [22], [anyn(options(5, [15], '/'), 2)])
    listen('D', 2, 'ii', [25, 26], [*[point(answer) for answer in split_marks(s(5, 17))], anyn(s(5, 18).split('/'), 1, 2)])

def reading():
    instruction = p(3, 2)
    labels = [p(3, row, 0) + ' ' + english(p(3, row, 1)) for row in range(4, 10)]
    add('1A', 1, instruction + '\n' + '\n'.join(labels), [], 'japanese-5-0', [3], [6], total=6, reading=[2],
        rubric=complete_pool(6, labels, [s(6, row, 1) for row in range(4, 10)], instruction, cell('scheme', 6, 3)))
    comprehension('1A', 2, 'i', [10], [point(s(6, 11), 2)], [6])
    for letter, qr, sr, place in [('a', 13, 13, 'Tokyo'), ('b', 14, 14, 'Hiroshima')]:
        question = english(p(3, 12, 1)) + ' ' + english(p(3, qr, 0)).removeprefix(f'({letter})').strip()
        found = add('1A', 2, question, [point(s(6, sr).split('in ' + place, 1)[1].strip(), 2)], 'japanese-5-0', [3], [6], letter + '-ii', reading=[2])
        found['questionRef'] = f'2017 HL Section 1A Q2(ii)({letter})'
        found['stem'] = english(p(3, 0))
    comprehension('1A', 3, 'i', [15, 16], [point(answer) for answer in split_marks(s(6, 16))], [6])
    comprehension('1A', 3, 'ii', [18], [point(answer) for answer in split_marks(s(6, 18))], [6])
    comprehension('1A', 4, 'i', [20, 21], [anyn(options(6, [20], ','), 2)], [6])
    comprehension('1A', 4, 'ii', [23], [point(s(6, 22), 2)], [6])
    comprehension('1A', 4, 'iii', [25], [point(answer) for answer in split_marks(s(6, 24))], [6])
    comprehension('1B', 1, None, [20], [point(answer) for answer in split_marks(s(7, 2))], [7])
    comprehension('1B', 2, None, [22], [anyn(options(7, [4], '/'), 2)], [7])
    comprehension('1B', 3, None, [25], [point(s(7, 6))], [7])
    comprehension('1B', 4, None, [27], [anyn(options(7, [8, 9], '/'), 2, 1, [2, 1])], [7])
    instruction = prompt(7, [1])
    headers = [p(7, 3, 1), english(p(7, 2, 2)) + ' ' + p(7, 3, 2), p(7, 3, 3)]
    names = [p(7, row, 1) for row in [4, 6, 8, 9, 10]]
    values = [
        [(0, point(s(7, 16, 2))), (2, point(selected(7, [(16, 4), (17, 1)]), 2))],
        [(0, point(s(7, 19, 2))), (1, point(s(7, 19, 3)))],
        [(1, point(s(7, 21, 3))), (2, point(s(7, 21, 4), 2))],
        [(1, point(selected(7, [(23, 3), (24, 0)]))), (2, point(clean_tariff(selected(7, [(23, 4), (24, 1), (25, 1)])), 2))],
        [(0, point(s(7, 26, 2))), (2, point(s(7, 26, 4), 2))],
    ]
    rows, groups = [], []
    for person, cells in enumerate(values):
        start = len(rows)
        for column, row in cells:
            row['contextNote'] = names[person] + ' — ' + headers[column]
            rows.append(row)
        groups.append((f'person-{person + 1}', names[person], start, len(rows)))
    table = add('2A', 1, instruction + '\n' + '\n'.join(headers + names), rows, 'japanese-5-2', [7], [7], reading=[6, 7],
        figure=crop('ja-2017-hl-2a-1', 7, [.06, .045, .96, .343], instruction))
    group_rows(table, groups)
    for roman, qr, sr in [('i', 12, 30), ('ii', 14, 32), ('iii', 16, 34)]:
        comprehension('2A', 2, roman, [qr], [point(s(7, sr), 2)], [7])
    comprehension('2A', 3, 'i', [19], [point(s(8, 2), 2)], [8])
    comprehension('2A', 3, 'ii', [21, 22], [anyn(s(8, 4).split('/'), 3)], [8])
    comprehension('2A', 3, 'iii', [24, 25], [anyn(options(8, [7], '/'), 1)], [8])
    translation = selected(8, [(11, 0), (12, 0)])
    add('2A', 4, prompt(7, [27]) + '\n' + p(7, 28) + ' ' + p(7, 29),
        [point(answer, 2) for answer in split_marks(translation, 2)], 'japanese-5-3', [7], [8], reading=[6])
    for q, instruction_row, label_rows, answer_rows, region in [
        (1, 2, range(4, 9), range(15, 20), [.06, .05, .96, .45]),
        (2, 10, range(12, 17), range(21, 26), [.06, .46, .96, .88]),
    ]:
        instruction = p(8, instruction_row)
        labels = [p(8, row, 0) + ' ' + p(8, row, 1) for row in label_rows]
        answers = [re.sub(r'^\([ivx]+\)\s*', '', s(8, row, 0 if row == 21 else 1)) for row in answer_rows]
        add('2B', q, instruction + '\n' + '\n'.join(labels), [], 'japanese-5-4', [8], [8], total=5, reading=[8],
            figure=crop(f'ja-2017-hl-2b-{q}', 8, region, instruction),
            rubric=complete_pool(5, labels, answers, instruction, cell('scheme', 8, answer_rows.start - 1)))
    for q, instruction_row, label_rows, sp, answer_rows, region in [
        (1, 2, range(4, 9), 8, range(28, 33), [.06, .03, .97, .48]),
        (2, 10, range(12, 17), 9, range(1, 6), [.06, .48, .97, .89]),
    ]:
        instruction = p(9, instruction_row)
        labels = [p(9, row, 0) + ' ' + p(9, row, 1) for row in label_rows]
        answers = [re.sub(r'^\([ivx]+\)\s*', '', s(sp, row, 0 if (sp, row) in [(8, 28), (8, 32), (9, 3), (9, 4), (9, 5)] else 1)) for row in answer_rows]
        add('2C', q, instruction + '\n' + '\n'.join(labels), [], 'japanese-5-5', [9], [sp], total=5, reading=[9],
            figure=crop(f'ja-2017-hl-2c-{q}', 9, region, instruction),
            rubric=complete_pool(5, labels, answers, instruction, cell('scheme', sp, answer_rows.start - 1)))
    first, second = s(9, 9).split('(1 mark)', 1)
    comprehension('3A', 1, None, [1, 2], [point(first.strip()), point(second.strip(' /'))], [9])
    comprehension('3A', 2, None, [4, 5], [point(s(9, 12))], [9])
    comprehension('3A', 3, None, [7], [point(answer) for answer in split_marks(s(9, 14))], [9])
    comprehension('3A', 4, None, [9], [point(answer) for answer in split_marks(s(9, 16))], [9])
    comprehension('3A', 5, None, [11, 12], [anyn(options(9, [18], '/'), 2)], [9])
    comprehension('3A', 6, None, [14, 15], [anyn(options(9, [20], '/'), 2)], [9])
    when, why = selected(9, [(22, 0), (23, 0)]).split('(1 mark)', 1)
    comprehension('3A', 7, None, [18], [point(when.strip()), point(clean_tariff(why.strip(' /')), 2)], [9])
    for q, qr, sr in [(1, 22, 26), (2, 24, 28), (3, 26, 30)]:
        comprehension('3B', q, None, [qr], [point(s(9, sr), 2)], [9])
    instruction = p(12, 2)
    labels = [p(12, row) for row in range(5, 10)]
    pairs = [{'id': f'item-{i + 1}', 'label': label, 'rows': [
        {'id': 'reading', 'text': s(10, i + 1, 2), 'marks': 1}, {'id': 'meaning', 'text': s(10, i + 1, 4), 'marks': 1}]}
        for i, label in enumerate(labels)]
    add('3C', None, instruction + '\n' + '\n'.join(labels), [], 'japanese-5-4', [12], [10], total=10, reading=[12],
        figure=crop('ja-2017-hl-3c', 12, [.06, .035, .97, .455], instruction),
        rubric={'system': 'language-points', 'count': 5, 'taskRequirements': [instruction], 'groups': pairs, 'markingGuideNote': cell('scheme', 10, 0)})
    instruction = p(12, 13)
    answer_cells = [[(7, 0)], [(8, 0), (8, 2)], [(9, 0)], [(10, 0)], [(11, 0), (11, 2)], [(12, 0)], [(13, 0), (13, 2)]]
    groups = []
    for index, answers in enumerate(answer_cells):
        label = p(12, 14 + index)
        for blank, (row, group) in enumerate(answers, 1):
            answer = re.sub(r'^\([ivx]+\)\s*', '', s(10, row, group))
            groups.append({'id': f'sentence-{index + 1}-blank-{blank}', 'label': label + f' — blank {blank}', 'rows': [{'id': 'answer', 'text': answer, 'marks': 1}]})
    add('3D', None, instruction + '\n' + '\n'.join(p(12, row) for row in range(14, 21)), [], 'japanese-5-5', [12], [10], total=10, reading=[12],
        figure=crop('ja-2017-hl-3d', 12, [.06, .465, .97, .91], instruction),
        rubric={'system': 'language-points', 'count': 10, 'taskRequirements': [instruction], 'groups': groups, 'markingGuideNote': cell('scheme', 10, 6)})


def steps(maximum):
    return list(range(maximum + 1))


def writing():
    for q, pp, sp, maximum, lower, threshold, length in [(4, 14, 12, 20, 15, 10, 150), (5, 16, 14, 30, 20, 15, 200)]:
        ranges = [(16, 25), (25, 34), (34, 43)] if q == 4 else [(16, 25), (25, 35), (35, 43)]
        guidance = [join_cells('scheme', sp, range(first, last), 140) for first, last in ranges]
        normal_ranges = [(0, 5), (6, 14), (15, 20)] if q == 4 else [(0, 7), (8, 20), (21, 30)]
        lower_ranges = [(0, 3), (4, 10), (11, 15)] if q == 4 else [(0, 4), (5, 12), (13, 20)]
        bands = [{'label': f'{lo}–{hi}', 'marks': list(range(lo, hi + 1)), 'guidance': [text]} for (lo, hi), text in zip(normal_ranges, guidance)]
        reduced = [{'label': f'{lo}–{hi}', 'marks': list(range(lo, hi + 1)), 'guidance': [text]} for (lo, hi), text in zip(lower_ranges, guidance)]
        rule = selected(sp, [(row, None) for row in range(9, 13)])
        if q == 4:
            instruction = p(14, 2)
            question = instruction + '\n(a) ' + ' '.join(p(14, row) for row in range(6, 9)) + '\n' + '\n'.join(p(14, row) for row in [9, 10])
            question += '\n' + english(p(14, 11)) + '\n(b) ' + ' '.join(p(14, row) for row in range(15, 18)) + '\n' + '\n'.join(p(14, row) for row in [18, 19])
            allocation = selected(11, [(row, None) for row in range(6, 11)]) + '\n' + selected(11, [(row, None) for row in range(17, 22)])
            criteria = [{'id': f'point-{i}', 'label': f'({i})', 'maxMarks': 9, 'permittedMarks': steps(9), 'guidance': [allocation]} for i in ['i', 'ii']]
            guide = 'Assess the one speech option you answered. Its two content points receive up to 9 each, with opening 1 and closing 1. Use the printed 20-mark expression scale and its conditional 15-mark scale. No discretionary content marks are printed.'
        else:
            instruction = p(16, 3) + ' ' + p(16, 4)
            question = instruction + '\n' + '\n'.join(p(16, row) for row in range(5, 17))
            allocation = selected(13, [(row, None) for row in range(3, 7)])
            headings = [cell('scheme', 13, row) for row in range(9, 15)]
            criteria = [{'id': f'heading-{i}', 'label': f'Chosen heading {i}', 'maxMarks': 7, 'permittedMarks': steps(7), 'guidance': [allocation] + headings} for i in range(1, 5)]
            guide = 'Assess four different headings once each, up to 7 marks each, with opening 1 and ending 1. Use the printed 30-mark expression scale and its conditional 20-mark scale. No discretionary content marks are printed.'
        criteria += [{'id': label.lower(), 'label': label, 'maxMarks': 1, 'permittedMarks': [0, 1], 'guidance': [allocation]} for label in ['Opening', 'Closing' if q == 4 else 'Ending']]
        content_ids = [criterion['id'] for criterion in criteria]
        criteria.append({'id': 'expression', 'label': 'Expression', 'maxMarks': maximum, 'permittedMarks': steps(maximum),
            'guidance': [selected(sp, [(43, None), (44, None)])], 'bands': bands,
            'limits': [{'id': 'lower-e', 'maxMarks': lower, 'when': {'any': [{'criterionIds': content_ids, 'atMost': threshold}, {'length': 'characters', 'below': length}]},
                        'bands': reduced, 'guidance': [rule]}]})
        add(str(q), None, question, [], 'japanese-5-7', [pp], [sp - 1, sp], total=maximum * 2, reading=[pp],
            figure=crop(f'ja-2017-hl-{q}', pp, [.045, .025, .97, .90], question),
            rubric={'system': 'language-writing', 'taskRequirements': [instruction], 'criteria': criteria, 'markingGuideNote': guide})


def build():
    reading()
    writing()
    listening()
    census = json.loads((Path(__file__).parent / 'reviews/japanese-2017-hl-census.json').read_text())
    expected = {'ja-2017-hl-' + '-'.join(str(part).lower() for part in task['key'] if part is not None): task for task in census['tasks']}
    assert set(expected) == {card['id'] for card in CARDS}
    for card in CARDS:
        task = expected[card['id']]
        assert card['totalMarks'] == task['marks'], (card['id'], card['totalMarks'], task['marks'])
        assert card['sourceEvidence']['paperPages'] == task['paperPages']
        assert card['sourceEvidence']['schemePages'] == task['schemePages']
        if task.get('paperRef'):
            assert card['questionRef'] == task['paperRef']
    assert len(CARDS) == 61
    assert sum(card['totalMarks'] for card in CARDS) == 300
    assert sum('answerLanguageRule' in card for card in CARDS) == 26
    assert sum('extraneousMaterialRule' in card for card in CARDS) == 6
    assert '\ufffd' not in json.dumps([CARDS, EVIDENCE], ensure_ascii=False), 'An unresolved font glyph entered published text'
    assert not any(ord(char) < 32 and char not in '\n\r\t' for card in CARDS for char in json.dumps(card, ensure_ascii=False))
    recovery = ROOT / 'scripts/markbank/authoring/glyphmap-japanese-2017.json'
    return {'subjectId': 'japanese', 'sitting': '2017-hl', 'reviewedAt': '2026-11-09',
            'sources': [{'document': name, 'path': str(path.relative_to(ROOT)), 'sha256': PINNED_SOURCES[path], 'pagesReviewed': list(range(1, len(DOCS[name]) + 1))} for name, path in [('paper', PAPER), ('aural', AURAL), ('scheme', SCHEME)]],
            'glyphRecovery': {'path': str(recovery.relative_to(ROOT)), 'sha256': hashlib.sha256(recovery.read_bytes()).hexdigest(), 'unresolvedPresentation': 'Original passage/cover PDF images only; no unresolved glyph is accepted in card or selector text.'},
            'cards': CARDS, 'selectors': EVIDENCE, 'status': 'source-reviewed-browser-qa-pending',
            'choiceAnalysis': census['choiceBoundaries'], 'consolidations': []}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    result = build()
    if args.write:
        scheme_text = ''.join(f'\n## Page {i + 1}\n\n' + page.get_text(sort=True) for i, page in enumerate(DOCS['scheme']))
        scheme_text += '\n## Original text with furigana folded at its printed character\n'
        scheme_text += ''.join(f'\n### Physical page {i + 1}\n\n' + '\n'.join(' '.join(group[2] for group in row) for row in rows) + '\n' for i, rows in enumerate(ROWS['scheme']))
        scheme_text += '\n## Original listening table columns — physical page 3\n'
        scheme_text += '\n'.join(DOCS['scheme'][2].get_text(clip=fitz.Rect(x0, 180, x1, 420), sort=True) for x0, x1 in [(78, 190), (190, 285), (290, 375), (375, 590)])
        scheme_text += '\n## Original member table columns — physical page 7\n'
        scheme_text += '\n'.join(DOCS['scheme'][6].get_text(clip=fitz.Rect(x0, 335, x1, 620), sort=True) for x0, x1 in [(145, 254), (255, 365), (365, 590)])
        SCHEME.with_suffix('.md').write_text(scheme_text.rstrip() + '\n')
        (ROOT / 'scripts/markbank/authoring/reviews/japanese-2017-hl.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
        manifest = ROOT / 'components/MarkBank/figures-japanese.json'
        previous = json.loads(manifest.read_text())
        previous.update(FIGURES)
        manifest.write_text(json.dumps(previous, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'cards': len(CARDS), 'marks': sum(card['totalMarks'] for card in CARDS), 'figures': len(FIGURES)}, indent=2))
