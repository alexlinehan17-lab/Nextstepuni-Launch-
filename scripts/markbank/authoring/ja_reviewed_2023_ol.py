#!/usr/bin/env python3
"""Publish the independently censused 2023 Ordinary sitting from PDF selectors.

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
    'paper': ROOT / 'examiner-reports/japanese/papers/2023-ol-000-paper.pdf',
    'aural': ROOT / 'examiner-reports/japanese/papers/2023-ol-A00-paper.pdf',
    'scheme': ROOT / 'examiner-reports/japanese/schemes/2023-ol.pdf',
}
HASHES = {
    'paper': '2307421a7a512bf54cee23213875bc1545b5616ffd7cc877aa28034232a27e3b',
    'aural': 'bc4052eb76ca8ca4f0e552c4e79a1475f73ac5d223207abfb199efd32e89f9eb',
    'scheme': '360f0300ec60d4920a5831f01f53f9dce2ed9169eb2f569c3f0a6760a4932425',
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
    return re.split(r'\s*/\s*', text.replace('\xa0', ' '), maxsplit=1)[-1].strip()


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
    return {'kind': 'source-text', 'label': '2023 Japanese Ordinary Level', 'title': 'Original examination material',
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
    cid = f'ja-2023-ol-{section.lower()}' + (f'-{q}' if q is not None else '') + (f'-{suffix}' if suffix else '')
    ref = f'2023 OL Section {section}' + (f' Q{q}' if q is not None else '') + ''.join(f'({part})' for part in suffix.split('-') if part)
    listening = section.startswith('L')
    card = {'id': cid, 'source': 'sec', 'subjectId': 'japanese', 'specVersion': 'lc-japanese-syllabus',
            'kind': 'rubric' if rubric else 'question', 'level': 'ordinary', 'year': 2023,
            'section': section[1:] if listening else section[0] if section[0] in '1234' else 'Q5',
            'topicId': topic, 'conceptId': concept_for(question, cid), 'questionRef': ref,
            'questionText': question, 'totalMarks': total if total is not None else sum(map(worth, rows)),
            'qa': {'gates': ['verbatim', 'tariff', 'figure'], 'humanReviewedBy': 'agent-verified', 'humanReviewedAt': '2026-11-09'},
            'sourceEvidence': {'component': 'aural' if listening else 'paper', 'paperPages': pp, 'schemePages': sp},
            'schemeCitation': 'Marking points quoted from the SEC marking scheme, Japanese 2023 Ordinary Level — © State Examinations Commission.'}
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
    instruction = without_marker(p(3, 0, 1))
    labels = [re.sub(r'_+', '', col('paper', 3, [row])).strip() for row in range(2, 7)]
    example = p(3, 1, 2) + ' ' + p(3, 1, 3)
    answers = [s(5, row, 2) if row != 7 else re.search(r'\d+$', s(5, row, 1)).group() for row in range(4, 9)]
    add('1', 1, instruction + '\n' + example + '\n' + '\n'.join(labels),
        [point(answer, 2, contextNote=label) for label, answer in zip(labels, answers)],
        'japanese-5-0', [3], [5], reading=[2, 3])
    for q, qr, answers in [
        (2, [8], [anyn(options(5, [10], separator='/'), 2, 2)]),
        (3, [12], [anyn(options(5, [12], separator='/'), 1, 2)]),
        (4, [15], [point(s(5, 14), 2)]),
        (5, [18], [anyn(options(5, [16], separator='/'), 2, 2)]),
        (6, [23], [point(s(5, 18), 2)]),
        (8, [28, 30], [point(s(5, 23), 2)]),
    ]:
        add('1', q, without_marker(col('paper', 3, qr)), answers, 'japanese-5-0', [3], [5], reading=[2], stem=p(3, 7, 1))
    question = without_marker(col('paper', 3, [26])) + '\n' + col('paper', 3, [27])
    add('1', 7, question, [anyn(options(5, [20], separator='/'), 2, 2, contextNote=cell('scheme', 5, 21, 0))],
        'japanese-5-0', [3], [5], reading=[2, 3], stem=p(3, 7, 1),
        figure=crop('ja-2023-ol-1-7', 3, [.52, .677, .96, .79], question))
    question = english(p(5, 1)) + '\n' + '\n'.join(p(5, row) for row in [3, 4, 5])
    profile = [point(s(6, row, group), contextNote=s(6, row, 0) + ' — ' + s(6, 3, header)) for row, group, header in [(5, 1, 0), (5, 2, 1), (7, 1, 0), (7, 3, 2)]]
    profile[-1]['contextNote'] += ' ' + s(6, 4)
    add('2A', 1, question, profile, 'japanese-5-2', [5], [6], reading=[4, 5], stem=without_marker(p(5, 0, 1)),
        figure=crop('ja-2023-ol-2a-1', 5, [.075, .064, .94, .22], question))
    for q, qr, answers in [
        (2, [6, 7], [anyn(options(6, [10], separator='/'), 1, 2)]),
        (3, [9, 10], [anyn(options(6, [12], separator='/'), 1, 2)]),
        (4, [12], [point(s(6, 14), 2)]),
        (5, [14], [anyn(options(6, [16], separator='/'), 3)]),
    ]:
        add('2A', q, without_marker(col('paper', 5, qr)), answers, 'japanese-5-2', [5], [6], reading=[4], stem=without_marker(p(5, 0, 1)))
    instruction = english(' '.join(p(5, row) for row in range(17, 21)))
    labels = []
    for rows in [[24], [26, 27], [29, 30], [32, 33], [35, 36], [38, 39]]:
        text = ' '.join(p(5, row) for row in rows)
        labels.append(re.match(r'\([ivx]+\)', text).group() + ' ' + english(text))
    groups = []
    for i, (truth_row, truth_group, quote_row) in enumerate([(19, 3, 20), (21, 2, 22), (23, 1, 24), (25, 1, 26), (27, 2, 28), (29, 1, 30)]):
        groups.append({'id': f'item-{i + 1}', 'label': labels[i], 'rows': [
            {'id': 'true-false', 'text': s(6, truth_row, truth_group), 'marks': 1},
            {'id': 'quote', 'text': s(6, quote_row).removeprefix('→').strip(), 'marks': 2}]})
    add('2B', None, instruction + '\n' + '\n'.join(labels), [], 'japanese-5-2', [5], [6],
        rubric={'system': 'language-points', 'count': 5, 'taskRequirements': [instruction], 'groups': groups, 'markingGuideNote': cell('scheme', 6, 18)},
        total=15, reading=[4, 5], figure=crop('ja-2023-ol-2b', 5, [.075, .425, .94, .9], instruction))
    instruction = p(6, 17)
    labels = [p(6, row) for row in range(19, 32)]
    answers = [without_marker(s(7, row, None)) for row in range(1, 14)]
    add('2C', None, instruction + '\n' + p(6, 18) + '\n' + '\n'.join(labels), [], 'japanese-5-4', [6], [7],
        rubric=pool(10, labels, answers, 1, instruction, cell('scheme', 7, 0)), total=10, reading=[6],
        figure=crop('ja-2023-ol-2c', 6, [.075, .48, .96, .9], instruction))
    instruction = english(p(7, 1) + ' ' + p(7, 2))
    labels = [p(7, row) for row in range(4, 10)]
    answers = [sa(7, row, 0 if row == 19 else 1) for row in range(15, 21)]
    add('2D', None, instruction + '\n' + p(7, 3) + '\n' + '\n'.join(labels), [], 'japanese-5-5', [7], [7],
        rubric=pool(5, labels, answers, 2, instruction, cell('scheme', 7, 14)), total=10, reading=[7],
        figure=crop('ja-2023-ol-2d', 7, [.075, .06, .96, .49], instruction))
    teacher = joined_selector('scheme', 8, [(3, 0), (4, 0)])
    teacher = re.sub(r'\s*\(any.*$', '', teacher)
    for q, qr, answers in [(1, [1, 2], [anyn([part.strip() for part in teacher.split('/')], 2, 2)]),
                           (2, [5], [point(s(8, 6), 2)]),
                           (3, [7], [anyn(options(8, [8], separator='/'), 2, 2)])]:
        add('3A', q, without_marker(col('paper', 9, qr)), answers, 'japanese-5-1', [9], [8], reading=[8], stem=without_marker(p(9, 0, 1)))
    for roman, qr, sr in [('i', [11, 13, 14, 15, 16], 10), ('ii', range(18, 24), 11),
                          ('iii', [24, 26, 27, 28, 29], 12), ('iv', [31, 34, 36, 38, 40], 13)]:
        answer = s(8, sr, 1) if sr == 10 else re.search(r'\([a-d]\).*', s(8, sr)).group()
        add('3A', 4, without_marker(col('paper', 9, qr)), [point(answer, 3)], 'japanese-5-1', [9], [8], roman,
            reading=[8], stem=without_marker(col('paper', 9, [9, 10])))
    instruction = english(p(10, 0, 1))
    labels = [p(10, row) for row in [1, 3, 5, 7]]
    add('3A', 5, instruction + '\n' + '\n'.join(labels), [], 'japanese-5-1', [10], [8],
        rubric=pool(3, labels, [s(8, row) for row in [16, 18, 20, 22]], 2, instruction, cell('scheme', 8, 14)), total=6, reading=[8, 10])
    question = p(10, 13)
    allocation = joined_selector('scheme', 8, [(24, 0), (25, 0)])
    point_label = re.search(r'\bpoints\b', allocation).group()
    parts = [{'id': f'point-{i}', 'verbatim': f'{i}. {point_label}', 'marks': 2, 'permittedMarks': [0, 2]} for i in [1, 2]]
    add('3B', None, question, [{'kind': 'criterion', 'verbatim': UNPRINTED, 'unprinted': True, 'marks': 4,
        'permittedMarks': [0, 2, 4], 'parts': parts, 'contextNote': allocation}], 'japanese-5-6', [10], [8], stem=english(p(10, 10)) + ' ' + p(10, 11))
    instruction = english(p(10, 21) + ' ' + p(10, 22))
    labels = [p(10, row) for row in range(24, 30)]
    add('3C', None, instruction + '\n' + p(10, 23) + '\n' + '\n'.join(labels), [], 'japanese-5-5', [10], [9],
        rubric=pool(5, labels, [s(9, row, 1) for row in range(1, 7)], 2, instruction, cell('scheme', 9, 0)), total=10,
        reading=[10], figure=crop('ja-2023-ol-3c', 10, [.075, .61, .96, .915], instruction))


def writing():
    instruction = english(' '.join(p(11, row) for row in [2, 3, 4]))
    question = instruction + '\n' + '\n'.join(p(11, row) for row in range(5, 18))
    labels = [s(9, row, 0) for row in range(9, 21)]
    answers = [s(9, row, 1) for row in range(9, 21)]
    discrepancy = 'Published-source discrepancy for (ix): the scheme prints ' + answers[8] + ', which is absent from the paper’s word bank. The printed bank contains トレーニング. Compare the original paper and scheme when assessing this item; the scheme answer is retained here as published.'
    guide = cell('scheme', 9, 8) + ' ' + discrepancy
    add('4', None, question, [], 'japanese-5-7', [11], [9], rubric=pool(10, labels, answers, 3, instruction, guide), total=30,
        reading=[11], figure=crop('ja-2023-ol-4', 11, [.075, .055, .97, .93], instruction))
    instruction = english(' '.join(p(12, row) for row in [1, 2, 3]))
    labels = [p(12, row) for row in range(4, 12)]
    content_bands = [{'label': s(11, row), 'marks': marks, 'guidance': [s(11, row, 1)]} for row, marks in [(3, [1]), (2, [2, 3]), (1, [4, 5])]]
    expression_bands = [{'label': s(11, first), 'marks': marks, 'guidance': [s(11, first, 1) + ' ' + ' '.join(s(11, row) for row in rest)]} for first, rest, marks in [(16, range(17, 23), [1]), (23, range(24, 31), [2, 3]), (31, range(32, 38), [4, 5])]]
    groups = []
    for i, label in enumerate(labels, 1):
        criteria = [{'id': f'item-{i}-content', 'label': s(11, 0).removesuffix(':'), 'maxMarks': 5, 'permittedMarks': list(range(6)), 'guidance': [s(10, 2)], 'bands': content_bands},
                    {'id': f'item-{i}-expression', 'label': s(11, 4).removesuffix(':'), 'maxMarks': 5, 'permittedMarks': list(range(6)), 'guidance': [s(11, 5)], 'bands': expression_bands}]
        groups.append({'id': f'item-{i}', 'label': label, 'rows': [], 'criteria': criteria})
    scheme_last_prompts = joined_selector('scheme', 10, [(9, None), (10, None)])
    discrepancy = 'The paper’s eight prompts are retained. The scheme instead prints ' + scheme_last_prompts + ' for its last two prompts. Apply the published content and expression grid separately to each paper prompt answered.'
    rubric = {'system': 'language-points', 'count': 5, 'taskRequirements': [instruction], 'groups': groups,
              'markingGuideNote': cell('scheme', 10, 1) + ' ' + s(10, 2) + ' ' + s(11, 38) + ' ' + s(11, 39) + ' ' + discrepancy}
    add('5', None, instruction + '\n' + '\n'.join(labels), [], 'japanese-5-7', [12], [10, 11], rubric=rubric, total=50,
        reading=[12], figure=crop('ja-2023-ol-5', 12, [.05, .04, .97, .944], instruction))


def listening():
    def aq(page, rows):
        return re.sub(r'^(?:\d+\.\s*)?(?:\([ivx]+\)\s*)?', '', col('aural', page, rows, 290)).strip()

    def listen(section, q, roman, qr, answers, question=None):
        page = {'A': 2, 'B': 3, 'C': 4, 'D': 5}[section]
        topic = {'A': 'japanese-6-2', 'B': 'japanese-6-0', 'C': 'japanese-6-2', 'D': 'japanese-6-1'}[section]
        card = add('L' + section, q, question or aq(page, qr), answers, topic, [page], [3 if section in 'AB' else 4], roman, reading=[page])
        card['stem'] = col('aural', page, [1, 3] if section == 'A' else [1, 2], 290)
        if section in 'BC':
            context = {1: 3, 2: 20}[q] if section == 'B' else {1: 3, 2: 26, 3: 33}[q]
            card['stem'] += '\n' + col('aural', page, [context], 290)
        return card

    for q, roman, qr, sr, group, marks in [
        (1, 'i', [5], 3, 2, 2), (1, 'ii', [7, 8, 10, 12, 14, 16], 4, 1, 4),
        (1, 'iii', [18, 20, 22, 24, 26, 28], 5, 1, 4), (2, 'i', [29], 6, 2, 2),
        (2, 'ii', range(31, 37), 7, 1, 4), (3, 'i', range(40, 45), 9, 2, 4),
        (3, 'ii', [45, 47, 50, 52, 54, 56, 58, 59], 10, 1, 4),
    ]:
        listen('A', q, roman, qr, [point(s(3, sr, group), marks)])
    listen('A', 2, 'iii', [37, 38], [anyn(options(3, [8], 1, '/'), 1, 2)])
    for q, roman, qr, sr, marks in [
        (1, 'i', [4], 13, 2), (1, 'ii', range(6, 11), 14, 4), (1, 'iii', [11], 15, 2),
        (1, 'iv', range(13, 18), 16, 4), (2, 'i', range(21, 27), 19, 4),
        (2, 'iii', [31, 33, 35, 37, 39], 21, 4),
    ]:
        listen('B', q, roman, qr, [point(s(3, sr, 1), marks)])
    phone = listen('B', 1, 'v', [18], [point(s(3, 17, 1), 4,
        contextNote='Complete the four blank digits in the printed grid. The scheme awards 4 marks for the number and publishes no separate per-digit tariff.')])
    phone['questionFigureKey'] = crop('ja-2023-ol-lb-1-v', 3, [.49, .47, .91, .53], phone['questionText'], 'aural')
    listen('B', 2, 'ii', [27], [anyn([part.strip() for part in sa(3, 20).split('/')], 1, 2)])
    first = cell('aural', 4, 4, 1).rsplit('(i)', 1)[1].strip() + ' ' + col('aural', 4, [5, 6, 8, 10, 12])
    listen('C', 1, 'i', [], [point(s(4, 2, 1), 4)], first)
    listen('C', 1, 'ii', [14, 16], [anyn(options(4, [3], 1, '/'), 1, 3)])
    third = cell('aural', 4, 20).rsplit('(iii)', 1)[1].strip() + ' ' + col('aural', 4, [21, 22, 23, 24, 25])
    listen('C', 1, 'iii', [], [point(s(4, 4, 1), 4)], third)
    listen('C', 2, 'i', [27, 28, 29, 31, 32], [point(s(4, 6), 4)])
    listen('C', 3, 'i', [34], [anyn(options(4, [8], 1, '/'), 1, 3)])
    listen('C', 3, 'ii', [39, 41, 43, 45, 47], [point(s(4, 9, 1), 4)])
    for roman, qr, sr in [('i', range(3, 8), 11), ('ii', range(9, 15), 12),
                           ('iv', [20, 23, 25, 27, 29], 15), ('vi', range(34, 39), 17),
                           ('vii', range(39, 44), 18)]:
        listen('D', None, roman, qr, [point(s(4, sr, 1), 4)])
    listen('D', None, 'iii', [15, 17], [anyn(options(4, [13], 1, '/'), 1, 2)])
    listen('D', None, 'v', [31], [anyn(options(4, [16], 1, '/'), 1, 2)])
    listen('D', None, 'viii', [44], [anyn([part.strip() for part in sa(4, 19).split('/')], 1, 2)])




def consolidations(census):
    records = []
    romans = ['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x', 'xi', 'xii', 'xiii']
    for suffix, count, pp, pr, sp, sr, reason in [
        ('1-1', 5, 3, [0], 5, 3, 'One required five-cell matching task, two marks per cell; keep every printed item together.'),
        ('2c', 13, 6, [17], 7, 0, 'One printed any-ten-of-thirteen meaning pool, one mark per chosen answer.'),
        ('2d', 6, 7, [1, 2], 7, 14, 'One printed any-five-of-six particle pool, two marks per chosen answer.'),
        ('3a-5', 4, 10, [0], 8, 14, 'One printed any-three-of-four Japanese response pool, two marks per chosen response.'),
        ('3c', 6, 10, [21, 22], 9, 0, 'One printed any-five-of-six past-form pool, two marks per chosen response.'),
    ]:
        canonical = 'ja-2023-ol-' + suffix
        task = next(task for task in census['tasks'] if canonical == 'ja-2023-ol-' + '-'.join(str(part).lower() for part in task['key'] if part is not None))
        records.append({'canonicalId': canonical, 'legacyIds': [canonical + '-' + part for part in romans[:count]], 'taskKey': task['key'], 'marks': task['marks'], 'reason': reason,
                        'paperEvidence': {'page': pp, 'text': joined_selector('paper', pp, [(row, None) for row in pr])}, 'schemeEvidence': {'page': sp, 'text': cell('scheme', sp, sr)}})
    return records


def build():
    reading()
    writing()
    listening()
    census = json.loads((Path(__file__).parent / 'reviews/japanese-2023-ol-census.json').read_text())
    expected = {'ja-2023-ol-' + '-'.join(str(part).lower() for part in task['key'] if part is not None): task for task in census['tasks']}
    assert set(expected) == {card['id'] for card in CARDS}
    for card in CARDS:
        task = expected[card['id']]
        assert card['totalMarks'] == task['marks'], (card['id'], card['totalMarks'], task['marks'])
        assert card['sourceEvidence']['paperPages'] == task['paperPages']
        assert card['sourceEvidence']['schemePages'] == task['schemePages']
    assert len(CARDS) == 58
    assert sum(card['totalMarks'] for card in CARDS) == 300
    return {'subjectId': 'japanese', 'sitting': '2023-ol', 'reviewedAt': '2026-11-09',
            'sources': [{'document': name, 'path': str(path.relative_to(ROOT)), 'sha256': HASHES[name], 'pagesReviewed': list(range(1, len(DOCS[name]) + 1))} for name, path in PATHS.items()],
            'cards': CARDS, 'selectors': EVIDENCE, 'status': 'source-reviewed-browser-qa-pending',
            'choiceAnalysis': census['choiceBoundaries'], 'consolidations': consolidations(census)}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    result = build()
    if args.write:
        (ROOT / 'scripts/markbank/authoring/reviews/japanese-2023-ol.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
        manifest = ROOT / 'components/MarkBank/figures-japanese.json'
        previous = json.loads(manifest.read_text())
        previous.update(FIGURES)
        manifest.write_text(json.dumps(previous, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'cards': len(CARDS), 'marks': sum(card['totalMarks'] for card in CARDS), 'figures': len(FIGURES)}, indent=2))


