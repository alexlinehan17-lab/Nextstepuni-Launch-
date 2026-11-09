#!/usr/bin/env python3
"""Publish the independently censused 2025 Ordinary sitting from PDF selectors.

Question/answer/guidance strings below are selected from the original PDFs.
Finite choices remain single tasks, including the eight independent C/E
responses in Q5. The census does not import this file or its output.
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
PATHS = {
    'paper': ROOT / 'examiner-reports/japanese/papers/2025-ol-000-paper.pdf',
    'aural': ROOT / 'examiner-reports/japanese/papers/2025-ol-A00-paper.pdf',
    'scheme': ROOT / 'examiner-reports/japanese/schemes/2025-ol.pdf',
}
HASHES = {
    'paper': 'f0c17ece1c7896e680f84903d780fa51bceec23638ad249f37953e61e39c0f3e',
    'aural': '272e54c3ce42b5689fdd94b090713bd248d43e4ae71579d4c31a638354b81df6',
    'scheme': 'a11b7c790c76827cbd049d0ccea42c9f6c33f109c027db0a566e84ddb954cabc',
}
for name, path in PATHS.items():
    assert hashlib.sha256(path.read_bytes()).hexdigest() == HASHES[name], path
DOCS = {name: fitz.open(path) for name, path in PATHS.items()}
ROWS = {name: [page_rows(page) for page in doc] for name, doc in DOCS.items()}
CARDS, EVIDENCE, FIGURES = [], [], {}
ORIGINAL_IDS = set(re.findall(r'^    id: "([^\"]+)"', (ROOT / "components/MarkBank/cards/japanese/ordinary.ts").read_text(), re.M))
UNPRINTED = re.search(r"export const UNPRINTED_ANSWER = '([^']+)'", (ROOT / 'types/markBank.ts').read_text()).group(1)


def cell(doc, page, row, group=None):
    groups = ROWS[doc][page - 1][row]
    text = ' '.join(group[2] for group in groups) if group is None else groups[group][2]
    EVIDENCE.append({'document': doc, 'page': page, 'row': row, 'group': group, 'text': text})
    return text


def p(page, row, group=None):
    return cell('paper', page, row, group)


def without_marker(text):
    return re.sub(r'^(?:\d+\.|\([a-z]+\))\s*', '', text).strip()


def english(text):
    return text.split(' / ', 1)[-1].strip()


def col(doc, page, rows, xmin=300):
    return ' '.join(' '.join(cell(doc, page, row, i) for i, group in enumerate(ROWS[doc][page - 1][row]) if group[0] >= xmin) for row in rows).strip()


def s(page, row, group=0):
    return re.sub(r'\s*\(\d+\s*marks?\)\s*$', '', cell('scheme', page, row, group)).strip().removeprefix('- ').strip()


def sa(page, row, group=0):
    return without_marker(s(page, row, group)).removeprefix('- ').strip()


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


def source(pages, component='paper'):
    return {'kind': 'source-text', 'label': '2025 Japanese Ordinary Level', 'title': 'Original examination material',
            'pages': pages, 'attribution': '© State Examinations Commission.',
            **({'presentationNote': FURIGANA_NOTE} if component == 'paper' else {}), '_component': component}


def crop(key, page, region, alt, component='paper'):
    sheet = DOCS[component][page - 1]
    rect = fitz.Rect(region[0] * sheet.rect.width, region[1] * sheet.rect.height, region[2] * sheet.rect.width, region[3] * sheet.rect.height)
    rel = f'/exam-figures/japanese/{key}.png'
    path = ROOT / 'public' / rel.lstrip('/')
    path.parent.mkdir(parents=True, exist_ok=True)
    sheet.get_pixmap(matrix=fitz.Matrix(2, 2), clip=rect).save(path)
    FIGURES[key] = {'src': rel, 'md5': hashlib.md5(path.read_bytes()).hexdigest(), 'alt': alt,
                    'attribution': '© State Examinations Commission.', 'source': {'document': component, 'page': page, 'region': region}}
    return key


def add(section, q, question, rows, topic, pp, sp, suffix='', rubric=None, total=None, reading=None, figure=None, stem=None):
    cid = f'ja-2025-ol-{section.lower()}' + (f'-{q}' if q is not None else '') + (f'-{suffix}' if suffix else '')
    ref = f'2025 OL Section {section}' + (f' Q{q}' if q is not None else '') + ''.join(f'({part})' for part in suffix.split('-') if part)
    listening = section.startswith('L')
    card = {'id': cid, 'source': 'sec', 'subjectId': 'japanese', 'specVersion': 'lc-japanese-syllabus',
            'kind': 'rubric' if rubric else 'question', 'level': 'ordinary', 'year': 2025,
            'section': section[1:] if listening else section[0] if section[0] in '1234' else 'Q5',
            'topicId': topic, 'conceptId': concept_for(question, cid), 'questionRef': ref,
            'questionText': question, 'totalMarks': total if total is not None else sum(map(worth, rows)),
            'qa': {'gates': ['verbatim', 'tariff', 'figure'], 'humanReviewedBy': 'agent-verified', 'humanReviewedAt': '2026-11-09'},
            'sourceEvidence': {'component': 'aural' if listening else 'paper', 'paperPages': pp, 'schemePages': sp},
            'schemeCitation': 'Marking points quoted from the SEC marking scheme, Japanese 2025 Ordinary Level — © State Examinations Commission.'}
    if cid in ORIGINAL_IDS:
        card['qa']['gates'].append('reviewed-card-correction')
    if listening or section[0] in '123':
        rule_page = 3 if listening else 5
        card['sourceEvidence']['generalSchemePages'] = [rule_page]
        card['answerLanguageRule'] = {'otherLanguageMultiplier': 0.5, 'sourceText': cell('scheme', rule_page, 1), 'schemePages': [rule_page]}
        if listening:
            card['answerLanguageRule']['penalizedLanguage'] = 'Japanese'
    if rubric:
        card['rubric'] = rubric
    else:
        card['tariffModel'] = {'kind': 'fixed'}
        card['rows'] = [dict(row, id=f'r-{i + 1}') for i, row in enumerate(rows)]
    if reading:
        card['sourceMaterial'] = source(reading, 'aural' if listening else 'paper')
    if figure:
        card['questionFigureKey'] = figure
    if stem:
        card['stem'] = stem
    CARDS.append(card)
    return card


def pool(count, labels, answers, marks, instruction, guide):
    return {'system': 'language-points', 'count': count, 'taskRequirements': [instruction],
            'groups': [{'id': f'item-{i + 1}', 'label': label, 'rows': [{'id': 'answer', 'text': answer, 'marks': marks}]} for i, (label, answer) in enumerate(zip(labels, answers))],
            'markingGuideNote': guide}


def options(page, rows, group=0, separator=','):
    text = ' '.join(s(page, row, group) for row in rows)
    text = re.sub(r'\s*\(any .*?\)', '', text)
    return [part.strip() for part in text.split(separator)]


def joined_selector(doc, page, rows):
    text = ' '.join(cell(doc, page, row, group) for row, group in rows)
    EVIDENCE.append({'document': doc, 'page': page, 'parts': [{'row': row, 'group': group} for row, group in rows], 'text': text})
    return text


def reading():
    instruction = p(3, 0, 1) + ' ' + p(3, 1, 1)
    labels = [p(3, row, group) for row, group in [(3, 3), (4, 2), (5, 2), (6, 2), (7, 3)]]
    example = p(3, 2, 2) + ' ' + p(3, 2, 3)
    add('1', 1, instruction + '\n' + example + '\n' + '\n'.join(labels),
        [point(s(5, row, 2), 2, contextNote=label) for row, label in zip(range(4, 9), labels)],
        'japanese-5-0', [3], [5], reading=[2, 3])
    for q, qr, answers in [(2, [10, 11], options(5, [11])), (3, [14, 15], options(5, [13]))]:
        add('1', q, without_marker(col('paper', 3, qr)), [anyn(answers, 2, 2)], 'japanese-5-0', [3], [5], reading=[2], stem=p(3, 9, 1))
    question = without_marker(col('paper', 3, [18, 19])) + '\n' + '\n'.join(re.sub(r'_+', '', p(3, row, 1)).strip() for row in [20, 21])
    add('1', 4, question, [point(s(5, row, 1), 2, contextNote=s(5, row, 0)) for row in [16, 17]],
        'japanese-5-0', [3], [5], reading=[2, 3], stem=p(3, 9, 1))
    question = without_marker(col('paper', 3, [22, 23])) + '\n' + '\n'.join(col('paper', 3, [row]) for row in range(24, 28))
    membership = [point(sa(5, row), 2, contextNote=p(3, 26, 3) if row == 21 else p(3, 27, 2)) for row in [21, 22]]
    price, duration = sa(5, 22, 1).split(' (1 mark) for ')
    membership += [point(price, contextNote=p(3, 27, 3)), point(duration, contextNote=p(3, 27, 3))]
    add('1', 5, question, membership, 'japanese-5-0', [3], [5], reading=[2, 3],
        figure=crop('ja-2025-ol-1-5', 3, [.53, .63, .95, .817], question), stem=p(3, 9, 1))
    add('1', 6, without_marker(p(3, 28, 1)), [point(s(5, 25), 2)], 'japanese-5-0', [3], [5], reading=[2], stem=p(3, 9, 1))
    for q, suffix, qr, answer in [(1, 'a', [(1, 3)], [point(s(6, 3), 2)]),
                                  (1, 'b', [(3, 1)], [anyn(options(6, [5]), 2, 2)]),
                                  (2, 'a', [(6, 3)], [point(s(6, 8), 2)]),
                                  (2, 'b', [(9, 1)], [anyn(options(6, [10]), 2, 2, [2, 1])]),
                                  (3, 'a', [(12, 3)], [point(s(6, 12), 2)]),
                                  (3, 'b', [(14, 1), (15, 1)], [point(s(6, 14), 2)])]:
        add('2A', q, without_marker(' '.join(p(5, row, group) for row, group in qr)), answer, 'japanese-5-2', [5], [6], suffix, reading=[4], stem=p(5, 0, 3))
    instruction = english(' '.join(p(5, row) for row in range(17, 21)))
    labels = [english(p(5, first)) + (' ' + without_marker(p(5, second)) if second else '') for first, second in [(26, 27), (29, None), (32, 33), (35, 36), (38, 39), (41, 42)]]
    groups = []
    for i, (truth, quote) in enumerate([(18, 19), (20, 22), (23, 25), (26, 28), (29, 31), (32, 34)]):
        groups.append({'id': f'item-{i + 1}', 'label': labels[i], 'rows': [
            {'id': 'true-false', 'text': s(6, truth, 2), 'marks': 1},
            {'id': 'quote', 'text': s(6, quote).removeprefix('→').strip(), 'marks': 2}]})
    add('2B', None, instruction + '\n' + '\n'.join(labels), [], 'japanese-5-2', [5], [6],
        rubric={'system': 'language-points', 'count': 5, 'taskRequirements': [instruction], 'groups': groups,
                'markingGuideNote': cell('scheme', 6, 15)}, total=15, reading=[4, 5],
        figure=crop('ja-2025-ol-2b', 5, [.07, .46, .94, .93], instruction))
    instruction = p(6, 17) + ' ' + p(6, 18)
    labels = [p(6, row) for row in range(20, 33)]
    add('2C', None, instruction + '\n' + '\n'.join(labels), [], 'japanese-5-4', [6], [7],
        rubric=pool(10, labels, [s(7, row, 1) for row in range(2, 15)], 1, instruction, cell('scheme', 7, 0)),
        total=10, reading=[6], figure=crop('ja-2025-ol-2c', 6, [.06, .49, .95, .87], instruction))
    question = english(p(7, 3)) + ' ' + p(7, 4)
    allocation = cell('scheme', 7, 17)
    point_label = re.search(r'\bpoints\b', allocation).group()
    parts = [{'id': f'point-{i}', 'verbatim': f'{i}. {point_label}', 'marks': 2, 'permittedMarks': [0, 2]} for i in [1, 2]]
    add('2D', None, question, [{'kind': 'criterion', 'verbatim': UNPRINTED, 'unprinted': True, 'marks': 4,
        'permittedMarks': [0, 2, 4], 'parts': parts, 'contextNote': allocation}], 'japanese-5-6', [7], [7], stem=english(p(7, 1)) + ' ' + p(7, 2))
    for q, qr, answers, quota, steps in [(1, (1, 2), options(7, [21, 22]), 2, [2, 1]), (2, (4, 1), options(7, [24]), 2, [2, 1]), (3, (7, 2), options(7, [26]), 1, None)]:
        add('3A', q, without_marker(p(9, *qr)), [anyn(answers, quota, 2, steps)], 'japanese-5-1', [9], [7], reading=[8], stem=p(9, 0, 1).removeprefix('A. '))
    for roman, qr, sr in [('i', [12, 14, 16, 18, 20], 28), ('ii', range(22, 28), 30), ('iii', [28, 30, 32, 34, 36], 32), ('iv', range(39, 45), 34)]:
        add('3A', 4, without_marker(col('paper', 9, qr)), [point(s(7, sr), 3)], 'japanese-5-1', [9], [7], roman, reading=[8], stem=without_marker(col('paper', 9, [10, 11])))
    instruction = english(p(10, 0, 1))
    labels = [p(10, row) for row in [1, 3, 5, 7]]
    add('3A', 5, instruction + '\n' + '\n'.join(labels), [], 'japanese-5-1', [10], [8],
        rubric=pool(3, labels, [s(8, row) for row in [2, 4, 6, 8]], 2, instruction, cell('scheme', 8, 0)), total=6, reading=[8, 10])
    for q, page, instrrows, itemrows, answerrows, region in [(1, 10, [10, 11], range(13, 19), range(11, 17), [.07, .39, .95, .86]), (2, 11, [0, 1, 2], range(4, 10), range(18, 24), [.07, .04, .95, .55])]:
        instruction = english(' '.join(p(page, row) for row in instrrows))
        labels = [p(page, row) for row in itemrows]
        answers = [s(8, row, 1) + (' ' + s(8, row, 2) if q == 2 and row > 18 else '') for row in answerrows]
        add('3B', q, instruction + '\n' + '\n'.join(labels), [], 'japanese-5-5', [page], [8],
            rubric=pool(5, labels, answers, 2, instruction, cell('scheme', 8, 10 if q == 1 else 17)), total=10,
            reading=[page], figure=crop(f'ja-2025-ol-3b-{q}', page, region, instruction))


def writing():
    instruction = english(' '.join(p(12, row) for row in [2, 3, 4]))
    question = instruction + '\n' + '\n'.join(p(12, row) for row in range(5, 20))
    labels = [s(9, row, 0) if row < 11 else re.match(r'\(\d+\)', s(9, row)).group() for row in range(2, 14)]
    answers = [s(9, row, 1) if row < 11 else re.sub(r'^\(\d+\)\s*', '', s(9, row)) for row in range(2, 14)]
    add('4', None, question, [], 'japanese-5-7', [12], [9], rubric=pool(10, labels, answers, 3, instruction, cell('scheme', 9, 1)), total=30,
        reading=[12], figure=crop('ja-2025-ol-4', 12, [.07, .055, .95, .91], instruction))
    instruction = english(' '.join(p(13, row) for row in [1, 2, 3]))
    labels = [p(13, row, 1) for row in range(4, 12)]
    content_bands = [{'label': s(9, row), 'marks': marks, 'guidance': [s(9, row, 1)]} for row, marks in [(28, [1]), (27, [2, 3]), (26, [4, 5])]]
    expression_bands = [{'label': s(10, first), 'marks': marks, 'guidance': [s(10, first, 1) + ' ' + ' '.join(s(10, row) for row in rest)]} for first, rest, marks in [(13, range(14, 20), [1]), (20, range(21, 28), [2, 3]), (28, range(29, 34), [4, 5])]]
    groups = []
    for i, label in enumerate(labels, 1):
        criteria = [{'id': f'item-{i}-content', 'label': s(9, 25).removesuffix(':'), 'maxMarks': 5, 'permittedMarks': list(range(6)), 'guidance': [s(9, 16)], 'bands': content_bands},
                    {'id': f'item-{i}-expression', 'label': s(10, 0).removesuffix(':'), 'maxMarks': 5, 'permittedMarks': list(range(6)), 'guidance': [s(10, 1)], 'bands': expression_bands}]
        groups.append({'id': f'item-{i}', 'label': label, 'rows': [], 'criteria': criteria})
    rubric = {'system': 'language-points', 'count': 5, 'taskRequirements': [instruction], 'groups': groups, 'markingGuideNote': s(9, 15) + ' ' + s(9, 16) + ' ' + s(10, 34) + ' ' + s(10, 35)}
    add('5', None, instruction + '\n' + '\n'.join(f'{i}. {label}' for i, label in enumerate(labels, 1)), [], 'japanese-5-7', [13], [9, 10], rubric=rubric, total=50,
        reading=[13], figure=crop('ja-2025-ol-5', 13, [.05, .04, .96, .93], instruction))


def listening():
    def listen(section, q, roman, qr, answers, question=None):
        page = {'A': 2, 'B': 3, 'C': 4, 'D': 5}[section]
        question = question or without_marker(col('aural', page, qr))
        topic = {'A': 'japanese-6-1', 'B': 'japanese-6-2', 'C': 'japanese-6-1', 'D': 'japanese-6-0'}[section]
        card = add('L' + section, q, question, answers, topic, [page], [3 if section in 'AB' else 4], roman or '', reading=[page])
        if section == 'D':
            card['stem'] = cell('aural', 5, 1, 1) + ' ' + 'Akemi and Chris.' + cell('aural', 5, 2).split('Akemi and Chris.', 1)[1] + ' ' + cell('aural', 5, 3, 1)
            card['stem'] += ' ' + cell('aural', 5, {1: 4, 2: 16, 3: 29}[q], 1)
        else:
            card['stem'] = col('aural', page, [1, 2])
            if section == 'A':
                r, g = {1: (5, 3), 2: (18, 2), 3: (32, 2)}[q]
                card['stem'] += ' ' + cell('aural', page, r, g)
            if section == 'B':
                card['stem'] += ' ' + cell('aural', page, 5 if q == 1 else 26, 1)
        return card

    listen('A', 1, 'i', [6], [point(s(3, 3, 2), 2)])
    listen('A', 1, 'ii', range(8, 13), [point(s(3, 4, 1), 4)])
    listen('A', 1, 'iii', range(13, 18), [point(sa(3, 5), 4)])
    listen('A', 2, 'i', range(19, 24), [point(s(3, 6, 2), 4)])
    listen('A', 2, 'ii', [25, 27, 28, 29, 30], [point(s(3, 7, 1), 4)])
    question = cell('aural', 2, 33).rsplit('(i)', 1)[1].strip()
    listen('A', 3, 'i', [], [anyn(options(3, [8], 2, '/'), 2, 2)], question)
    listen('A', 3, 'ii', [36, 37, 38, 40, 42], [point(s(3, 9, 1), 4)])
    listen('B', 1, 'i', range(6, 11), [point(s(3, 12, 1), 4)])
    question = cell('aural', 3, 11).rsplit('(ii)', 1)[1].strip() + ' ' + cell('aural', 3, 12, 1)
    listen('B', 1, 'ii', [], [anyn(options(3, [13], 1, '/'), 1, 2)], question)
    listen('B', 1, 'iii', range(14, 19), [point(s(3, 14, 1), 4)])
    listen('B', 1, 'iv', [19], [point(sa(3, 15), 2)])
    listen('B', 1, 'v', [21, 22], [anyn(options(3, [16], 1, '/'), 1, 2)])
    phone = listen('B', 1, 'vi', [24], [point(sa(3, 17), 4)])
    phone['questionFigureKey'] = crop('ja-2025-ol-lb-1-vi', 3, [.51, .61, .94, .67], phone['questionText'], 'aural')
    listen('B', 2, 'i', [27, 30, 32, 34, 36], [point(sa(3, 19), 4)])
    question = cell('aural', 3, 38).rsplit('(ii)', 1)[1].strip()
    listen('B', 2, 'ii', [], [anyn([part.strip() for part in sa(3, 20).split('/')], 1, 2)], question)
    for q, qr in [(1, range(5, 11)), (2, range(11, 16)), (3, range(16, 22))]:
        listen('C', q, None, qr, [point(s(4, q, 1), 4)])
    ingredients = [point(sa(4, row, group), 2, contextNote=context) for row, group, context in [(6, 1, cell('aural', 4, 24, 2)), (8, 0, cell('aural', 4, 25, 3)), (10, 0, cell('aural', 4, 26, 3))]]
    table = listen('C', 4, None, [22], ingredients)
    table['questionFigureKey'] = crop('ja-2025-ol-lc-4', 4, [.51, .52, .94, .68], table['questionText'], 'aural')
    listen('C', 5, None, [27], [anyn(options(4, [12], 1, '/'), 1, 2)])
    listen('C', 6, None, [29], [point(s(4, 13, 1), 2)])
    listen('C', 7, None, range(31, 36), [point(s(4, 14, 1), 4)])
    for q, roman, qr, sr in [(1, 'i', range(5, 11), 17), (1, 'ii', range(11, 16), 18), (2, 'i', range(17, 22), 20), (2, 'ii', range(22, 28), 21), (3, 'i', [30, 31, 32, 33, 35, 36], 23)]:
        listen('D', q, roman, qr, [point(s(4, sr, 1), 4)])
    # PDF superscripts are separate rows: restore their printed visual order
    # using only the original selected text, retaining all four choices.
    question = without_marker(col('aural', 5, [38, 39])) + ' ' + cell('aural', 5, 41) + cell('aural', 5, 40, 1)
    question += ' ' + col('aural', 5, [42, 43]) + ' ' + cell('aural', 5, 45).removesuffix(' .') + cell('aural', 5, 44, 1) + '.'
    listen('D', 3, 'ii', [], [point(s(4, 24, 1), 4)], question)


def consolidations(census):
    records = []
    for suffix, fragments, pp, pr, sp, sr, reason in [
        ('2b', ['1', '3', '4', '5', '6'], 5, [18, 19, 20], 6, 15, 'One printed any-five-of-six truth-and-quote pool, with independently priced truth1 and quote2. Only five fragment IDs shipped; the second item is included in the complete six-item source task without inventing a legacy alias.'),
        ('2c', list(map(str, range(1, 14))), 6, [17, 18], 7, 0, 'One printed any-ten-of-thirteen meaning pool, one mark per chosen answer. All thirteen printed options remain together.'),
        ('3a-5', list('abcd'), 10, [0], 8, 0, 'One printed any-three-of-four Japanese comprehension pool, two marks per chosen response.'),
    ]:
        canonical = 'ja-2025-ol-' + suffix
        task = next(task for task in census['tasks'] if canonical == 'ja-2025-ol-' + '-'.join(str(part).lower() for part in task['key'] if part is not None))
        records.append({'canonicalId': canonical, 'legacyIds': [canonical + '-' + part for part in fragments], 'taskKey': task['key'], 'marks': task['marks'], 'reason': reason,
                        'paperEvidence': {'page': pp, 'text': joined_selector('paper', pp, [(row, None) for row in pr])}, 'schemeEvidence': {'page': sp, 'text': cell('scheme', sp, sr)}})
    return records


def build():
    reading()
    writing()
    listening()
    census = json.loads((Path(__file__).parent / 'reviews/japanese-2025-ol-census.json').read_text())
    expected = {'ja-2025-ol-' + '-'.join(str(part).lower() for part in task['key'] if part is not None): task for task in census['tasks']}
    assert set(expected) == {card['id'] for card in CARDS}
    for card in CARDS:
        task = expected[card['id']]
        assert card['totalMarks'] == task['marks'], (card['id'], card['totalMarks'], task['marks'])
        assert card['sourceEvidence']['paperPages'] == task['paperPages']
        assert card['sourceEvidence']['schemePages'] == task['schemePages']
    assert len(CARDS) == 55
    assert sum(card['totalMarks'] for card in CARDS) == 300
    return {'subjectId': 'japanese', 'sitting': '2025-ol', 'reviewedAt': '2026-11-09',
            'sources': [{'document': name, 'path': str(path.relative_to(ROOT)), 'sha256': HASHES[name], 'pagesReviewed': list(range(1, len(DOCS[name]) + 1))} for name, path in PATHS.items()],
            'cards': CARDS, 'selectors': EVIDENCE, 'status': 'source-reviewed-browser-qa-pending',
            'choiceAnalysis': census['choiceBoundaries'], 'consolidations': consolidations(census)}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    result = build()
    if args.write:
        (ROOT / 'scripts/markbank/authoring/reviews/japanese-2025-ol.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
        PATHS['scheme'].with_suffix('.md').write_text(''.join(f'\n## Page {page}\n\n' + '\n'.join(' '.join(group[2] for group in row) for row in rows) + '\n' for page, rows in enumerate(ROWS['scheme'], 1)).rstrip() + '\n')
        path = ROOT / 'components/MarkBank/figures-japanese.json'
        previous = json.loads(path.read_text())
        previous.update(FIGURES)
        path.write_text(json.dumps(previous, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'cards': len(CARDS), 'marks': sum(card['totalMarks'] for card in CARDS), 'figures': len(FIGURES)}, indent=2))

