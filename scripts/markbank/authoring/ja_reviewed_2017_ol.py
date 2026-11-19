#!/usr/bin/env python3
"""Publish the independently censused 2017 Ordinary sitting from PDF selectors.

Question/answer/guidance strings below are selected from the original PDFs.
Finite choices remain single tasks, including the seven independent C/E
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
    'paper': ROOT / 'examiner-reports/japanese/papers/2017-ol-000-paper.pdf',
    'aural': ROOT / 'examiner-reports/japanese/papers/2017-ol-A00-paper.pdf',
    'scheme': ROOT / 'examiner-reports/japanese/schemes/2017-ol.pdf',
}
HASHES = {
    'paper': '9922a1801afe3fb3647800e0d09bac6c079a59f3f7fb5a40e6aed4bf8b738bf2',
    'aural': '3918ea5765a059289b06f22201c958a6a876369edb66b62eec976018288864ce',
    'scheme': 'bd72510e1ac85538e0c4fca9c479ec95ce3edec7255e00421e65243420b662af',
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
    return {'kind': 'source-text', 'label': '2017 Japanese Ordinary Level', 'title': 'Original examination material',
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
    cid = f'ja-2017-ol-{section.lower()}' + (f'-{q}' if q is not None else '') + (f'-{suffix}' if suffix else '')
    ref = f'2017 OL Section {section}' + (f' Q{q}' if q is not None else ' Q' if suffix else '') + ''.join(f'({part})' for part in suffix.split('-') if part)
    listening = section.startswith('L')
    card = {'id': cid, 'source': 'sec', 'subjectId': 'japanese', 'specVersion': 'lc-japanese-syllabus',
            'kind': 'rubric' if rubric else 'question', 'level': 'ordinary', 'year': 2017,
            'section': section[1:] if listening else section[0] if section[0] in '1234' else 'Q5',
            'topicId': topic, 'conceptId': concept_for(question, cid), 'questionRef': ref,
            'questionText': question, 'totalMarks': total if total is not None else sum(map(worth, rows)),
            'qa': {'gates': ['verbatim', 'tariff', 'figure'], 'humanReviewedBy': 'agent-verified', 'humanReviewedAt': '2026-11-09'},
            'sourceEvidence': {'component': 'aural' if listening else 'paper', 'paperPages': pp, 'schemePages': sp},
            'schemeCitation': 'Marking points quoted from the SEC marking scheme, Japanese 2017 Ordinary Level — © State Examinations Commission.'}
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
    text = re.sub(r'\s*\(any .*?\)', '', text, flags=re.I)
    return [part.strip() for part in text.split(separator)]


def joined_selector(doc, page, rows):
    text = ' '.join(cell(doc, page, row, group) for row, group in rows)
    EVIDENCE.append({'document': doc, 'page': page, 'parts': [{'row': row, 'group': group} for row, group in rows], 'text': text})
    return text

def reading():
    instruction = without_marker(col('paper', 3, [0]))
    labels = [re.sub(r'_+', '', col('paper', 3, [row])).strip() for row in [2, 4, 6, 8, 10]]
    add('1', 1, instruction + '\n' + col('paper', 3, [1]) + '\n' + '\n'.join(labels),
        [point(s(5, row, 2), 2, contextNote=label) for label, row in zip(labels, range(4, 9))],
        'japanese-5-0', [3], [5], reading=[2, 3])
    add('1', 2, without_marker(col('paper', 3, [13, 14])), [anyn(options(5, [10], separator='/'), 3, 2)],
        'japanese-5-0', [3], [5], reading=[2], stem=p(3, 12, 1))
    add('1', 3, without_marker(col('paper', 3, [18, 20])) + '\n' + col('paper', 3, [21, 23]),
        [point(s(5, 12), 2), point(s(5, 13), 2)], 'japanese-5-0', [3], [5], reading=[2])
    add('1', 4, without_marker(col('paper', 3, [25])), [anyn(options(5, [15], separator='/'), 2, 2)],
        'japanese-5-0', [3], [5], reading=[2])
    instruction = re.sub(r'^5\.\s*\(i\)\s*', '', col('paper', 3, [30])).strip()
    headers = [p(3, 32, group) for group in [3, 4, 5]]
    events = [col('paper', 3, [33, 34]), col('paper', 3, [35])]
    discrepancy = ('The scheme table heading prints 8 marks, but its six explicit day/month/weekday components are 1 mark each, totalling 6. '
                   'The other Question 1 tasks total 26, so these six components agree with the printed Question 1 total of 32. No extra two marks are allocated.')
    cell('scheme', 5, 17);cell('scheme', 5, 2)
    rows = []
    for event, row in zip(events, [19, 21]):
        answers = [s(5, row, 1), s(5, row + 1), s(5, row, 2)]
        rows.extend(point(answer, contextNote=event + ' — ' + headers[1 if i < 2 else 2]) for i, answer in enumerate(answers))
    rows[0]['contextNote'] += ' — ' + discrepancy
    table = add('1', 5, instruction + '\n' + '\n'.join(headers + events), rows, 'japanese-5-0', [3], [5], 'i', reading=[2, 3],
                figure=crop('ja-2017-ol-1-5-i', 3, [.51, .68, .97, .868], instruction))
    table['taskGroups'] = [{'sourceCardId': table['id'] + f'-event-{i + 1}', 'label': event, 'marks': 3,
                            'rowIds': [row['id'] for row in table['rows'][i * 3:i * 3 + 3]]} for i, event in enumerate(events)]
    add('1', 5, without_marker(col('paper', 3, [36])), [point(s(5, 24), 2)], 'japanese-5-0', [3], [5], 'ii', reading=[2])
    for q, qr, answers in [(1, [1], [point(s(6, 3), 3)]), (2, [3], [anyn(options(6, [5], separator='/'), 2, 2)]),
                           (3, [6], [anyn(options(6, [7], separator='/'), 1, 3)])]:
        add('2A', q, without_marker(col('paper', 5, qr)), answers, 'japanese-5-2', [5], [6], reading=[4], stem=col('paper', 5, [0]))
    for roman, qr, answers in [('i', [8], [point(s(6, 9), 3)]), ('ii', [11, 12], [anyn(options(6, [11]), 1, 3)])]:
        question = re.sub(r'^(?:4\.\s*)?\([ivx]+\)\s*', '', col('paper', 5, qr))
        add('2A', 4, question, answers, 'japanese-5-2', [5], [6], roman, reading=[4], stem=col('paper', 5, [0]))
    for card in CARDS:
        if card['id'].startswith('ja-2017-ol-2a-'):
            card['rows'][0]['contextNote'] = cell('scheme', 6, 1)
    instruction = ' '.join(p(5, row) for row in [16, 17])
    labels = [re.match(r'\([ivx]+\)', p(5, row)).group() + ' ' + p(5, row + 1) for row in [22, 25, 28, 31, 34]]
    groups = []
    for i, row in enumerate([13, 16, 19, 22, 25]):
        groups.append({'id': f'item-{i + 1}', 'label': labels[i], 'rows': [
            {'id': 'true-false', 'text': s(6, row, 2), 'marks': 1},
            {'id': 'quote', 'text': re.sub(r'\s*2 marks$', '', s(6, row + 2)), 'marks': 2}]})
    add('2B', None, instruction + '\n' + '\n'.join(labels), [], 'japanese-5-2', [5], [6], total=15, reading=[4, 5],
        rubric={'system': 'language-points', 'count': 5, 'taskRequirements': [instruction], 'groups': groups, 'markingGuideNote': cell('scheme', 6, 12)},
        figure=crop('ja-2017-ol-2b', 5, [.075, .44, .97, .945], instruction))
    instruction = p(6, 13)
    labels = [p(6, row) for row in range(15, 25)]
    answers = [s(6, 29, 1)] + [sa(6, row) for row in range(30, 39)]
    add('2C', None, instruction + '\n' + p(6, 14) + '\n' + '\n'.join(labels), [], 'japanese-5-4', [6], [6], total=10, reading=[6],
        rubric=pool(10, labels, answers, 1, instruction, cell('scheme', 6, 28)),
        figure=crop('ja-2017-ol-2c', 6, [.075, .49, .97, .925], instruction))
    question = ' '.join(p(7, row) for row in [6, 7])
    allocation = cell('scheme', 7, 3)
    parts = [{'id': f'point-{i}', 'verbatim': f'{i}. ' + re.search(r'points', allocation).group(), 'marks': 2, 'permittedMarks': [0, 2]} for i in [1, 2]]
    add('2D', None, question, [{'kind': 'criterion', 'verbatim': UNPRINTED, 'unprinted': True, 'marks': 4,
        'permittedMarks': [0, 2, 4], 'parts': parts, 'contextNote': allocation}], 'japanese-5-6', [7], [7], stem=' '.join(p(7, row) for row in [2, 3]))
    add('3A', 1, without_marker(col('paper', 9, [1])), [point(s(7, 7), 2)], 'japanese-5-1', [9], [7], reading=[8], stem=p(9, 0, 1))
    add('3A', 2, without_marker(col('paper', 9, [3, 4])), [anyn(options(7, [9], separator='/'), 1, 2)], 'japanese-5-1', [9], [7], reading=[8], stem=p(9, 0, 1))
    for roman, qr, sr, answer in [('i', range(8, 13), 11, s(7, 11, 1)), ('ii', range(13, 18), 12, re.search(r'c\. English$', s(7, 12)).group()),
                                  ('iii', range(18, 23), 13, s(7, 13, 1)), ('iv', range(23, 29), 14, s(7, 14, 1))]:
        add('3A', 3, without_marker(col('paper', 9, qr)), [point(answer, 3)], 'japanese-5-1', [9], [7], roman,
            reading=[8], stem=without_marker(col('paper', 9, [6, 7])))
    for roman, qr, sr in [('i', 32, 17), ('ii', 34, 19), ('iii', 36, 21)]:
        answer = s(7, sr)
        rows = [point(part.strip(), 1) for part in re.split(r'\(1 mark\)', answer) if part.strip()] if roman != 'ii' else [point(answer, 3)]
        add('3A', 4, without_marker(p(9, qr)), rows, 'japanese-5-1', [9], [7], roman, reading=[8], stem=english(p(9, 31, 1)))
    for q, instruction_row, example, lr, rr, region in [(1, 2, 3, range(4, 9), range(2, 7), [.075, .065, .97, .405]),
                                                      (2, 10, 11, range(12, 17), range(8, 13), [.075, .405, .97, .76])]:
        instruction = p(10, instruction_row)
        labels = [p(10, row) for row in lr]
        answers = []
        for row in rr:
            group = 1 if row in ([2, 3] if q == 1 else [8, 9]) else 0
            answers.append(re.sub(r'\s*2 marks$', '', without_marker(s(8, row, group))))
        add('3B', q, instruction + '\n' + p(10, example) + '\n' + '\n'.join(labels), [], 'japanese-5-5', [10], [8], total=10, reading=[10],
            rubric=pool(5, labels, answers, 2, instruction, cell('scheme', 8, 1 if q == 1 else 7)),
            figure=crop(f'ja-2017-ol-3b-{q}', 10, region, instruction))


def writing():
    instruction = p(11, 4)
    question = instruction + '\n' + '\n'.join(p(11, row) for row in range(5, 20))
    labels = [re.match(r'\([ivx]+\)', s(9, row)).group() for row in range(2, 12)]
    answers = [s(9, row, 1) if row != 9 else sa(9, row) for row in range(2, 12)]
    add('4', None, question, [], 'japanese-5-7', [11], [9],
        rubric=pool(10, labels, answers, 3, instruction, cell('scheme', 9, 1)), total=30,
        reading=[11], figure=crop('ja-2017-ol-4', 11, [.075, .045, .97, .95], instruction))
    instruction = p(12, 3) + ' ' + p(12, 4)
    labels = [p(12, row) for row in range(5, 12)]
    content_bands = [{'label': s(9, row), 'marks': marks, 'guidance': [s(9, row, 1)]}
                     for row, marks in [(25, [1]), (24, [2, 3]), (23, [4, 5])]]
    expression_bands = [{'label': s(10, first), 'marks': marks,
                         'guidance': [s(10, first, 1) + ' ' + ' '.join(s(10, row) for row in rest)]}
                        for first, rest, marks in [(13, range(14, 19), [1]), (19, range(20, 26), [2, 3]), (26, range(27, 33), [4, 5])]]
    cap = cell('scheme', 10, 1)
    groups = []
    for i, label in enumerate(labels, 1):
        criteria = [{'id': f'item-{i}-content', 'label': s(9, 22).removesuffix(':'), 'maxMarks': 5,
                     'permittedMarks': list(range(6)), 'guidance': [s(9, 14)], 'bands': content_bands},
                    {'id': f'item-{i}-expression', 'label': s(10, 0).removesuffix(':'), 'maxMarks': 5,
                     'permittedMarks': list(range(6)), 'guidance': [cap], 'bands': expression_bands,
                     'limits': [{'id': f'item-{i}-low-content', 'maxMarks': 3,
                                 'when': {'any': [{'criterionIds': [f'item-{i}-content'], 'atMost': 3}]}, 'guidance': [cap]}]}]
        groups.append({'id': f'item-{i}', 'label': label, 'rows': [], 'criteria': criteria})
    restated = s(9, 21, 1)
    discrepancy = ('The original paper asks about your other hobby in(vii). The scheme restates a different prompt: ' + restated +
                   ' Keep the actual paper prompt and apply the printed common content/expression rubric; the restated prompt is not an extra or replacement question.')
    rubric = {'system': 'language-points', 'count': 5, 'taskRequirements': [instruction], 'groups': groups,
              'markingGuideNote': s(9, 13) + ' ' + s(9, 14) + ' ' + cap + ' ' + s(10, 33) + ' ' + s(10, 34) + ' — ' + discrepancy}
    add('5', None, instruction + '\n' + '\n'.join(labels), [], 'japanese-5-7', [12], [9, 10], rubric=rubric, total=50,
        reading=[12], figure=crop('ja-2017-ol-5', 12, [.05, .035, .97, .95], instruction))


def listening():
    def listen(section, q, roman, qr, answers):
        page = {'A': 2, 'B': 3, 'C': 4, 'D': 5}[section]
        topic = 'japanese-6-1' if section == 'A' else 'japanese-6-2' if section == 'B' else 'japanese-6-0'
        question = re.sub(r'^(?:\d+\.?\s*)?(?:\([ivx]+\)\s*)?', '', col('aural', page, qr, 290)).strip()
        card = add('L' + section, q, question, answers, topic, [page], [3 if section in 'AB' else 4], roman, reading=[page])
        card['stem'] = col('aural', page, range(1, 6 if section == 'C' else 5))
        if section in 'BCD':
            header = {'B': {1: 6, 2: 28}, 'C': {1: 6, 2: 17, 3: 25}, 'D': {1: 5, 2: 22}}[section][q]
            card['stem'] += '\n' + col('aural', page, [header])
        if section == 'D' and q == 2:
            cell('aural', 5, 22, 0);cell('scheme', 4, 15)
            card['rows'][0]['contextNote'] = ('The English paper misnumbers the At the restaurant heading(iv); its facing Irish heading and the marking scheme number it2. '
                                               'These three prompts match by their full wording and order; the question reference retains the paired printed Question2 identity.')
        return card
    for q, roman, qr, sr, sg, marks in [(1, 'i', [6], 3, 2, 3), (1, 'ii', range(8, 13), 4, 1, 4), (1, 'iii', range(13, 18), 5, 1, 4),
        (2, 'i', [18], 6, 2, 2), (2, 'ii', range(20, 25), 7, 1, 4), (2, 'iii', range(25, 30), 8, 1, 4),
        (3, 'i', [30], 9, 2, 3), (3, 'ii', range(32, 37), 10, 1, 4)]:
        listen('A', q, roman, qr, [point(s(3, sr, sg), marks)])
    listen('B', 1, 'i', range(7, 12), [point(sa(3, 13), 4)])
    listen('B', 1, 'ii', [12], [point(s(3, 14, 1), 4)])
    listen('B', 1, 'iii', range(15, 20), [point(s(3, 15, 1), 4)])
    phone_source = cell('scheme', 3, 16, 1)
    number = re.search(r'\d{3}-\d{3}-\d{4}', phone_source).group()
    digits = number.replace('-', '')
    rows = [point(digits[position - 1], contextNote=f'Missing digit {index + 1} (position {position} in {number}). {phone_source} — Only the four missing digits score; the printed digits are given.')
            for index, position in enumerate([4, 6, 8, 9])]
    phone = listen('B', 1, 'iv', [20], rows)
    phone['questionFigureKey'] = crop('ja-2017-ol-lb-1-iv', 3, [.54, .485, .97, .58], phone['questionText'], 'aural')
    listen('B', 1, 'v', range(23, 28), [point(s(3, 17, 1), 4)])
    listen('B', 2, 'i', range(29, 34), [point(s(3, 19, 1), 4)])
    listen('B', 2, 'ii', range(34, 39), [point(sa(3, 20), 4)])
    for q, roman, qr, sr in [(1, 'i', range(7, 12), 2), (1, 'ii', range(12, 17), 3),
                            (2, 'i', range(18, 23), 5), (2, 'ii', [23], 6),
                            (3, 'i', range(26, 31), 8), (3, 'ii', range(31, 36), 9)]:
        listen('C', q, roman, qr, [point(s(4, sr, 1), 4)])
    for roman, qr, sr in [('i', range(6, 12), 12), ('ii', range(12, 17), 13), ('iii', range(17, 22), 14)]:
        listen('D', 1, roman, qr, [point(s(4, sr, 1), 4)])
    listen('D', 2, 'i', [23], [anyn(s(4, 16, 1).split('/'), 1, 2)])
    listen('D', 2, 'ii', [25], [anyn(s(4, 17, 1).split('/'), 1, 2)])
    listen('D', 2, 'iii', range(27, 33), [point(s(4, 19, 1), 4)])


def build():
    reading()
    writing()
    listening()
    census = json.loads((Path(__file__).parent / 'reviews/japanese-2017-ol-census.json').read_text())
    expected = {'ja-2017-ol-' + '-'.join(str(part).lower() for part in task['key'] if part is not None): task for task in census['tasks']}
    assert set(expected) == {card['id'] for card in CARDS}
    for card in CARDS:
        task = expected[card['id']]
        assert card['totalMarks'] == task['marks'], (card['id'], card['totalMarks'], task['marks'])
        assert card['sourceEvidence']['paperPages'] == task['paperPages']
        assert card['sourceEvidence']['schemePages'] == task['schemePages']
    assert len(CARDS) == 54
    assert sum(card['totalMarks'] for card in CARDS) == 300
    assert sum('answerLanguageRule' in card for card in CARDS) == 52
    assert not any(card['id'] in ORIGINAL_IDS for card in CARDS)
    return {'subjectId': 'japanese', 'sitting': '2017-ol', 'reviewedAt': '2026-11-09',
            'sources': [{'document': name, 'path': str(path.relative_to(ROOT)), 'sha256': HASHES[name],
                         'pagesReviewed': list(range(1, len(DOCS[name]) + 1))} for name, path in PATHS.items()],
            'cards': CARDS, 'selectors': EVIDENCE, 'status': 'source-reviewed-browser-qa-pending',
            'choiceAnalysis': census['choiceBoundaries'], 'consolidations': []}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    result = build()
    if args.write:
        text = ''.join(f'\n## Page {i + 1}\n\n' + page.get_text(sort=True) for i, page in enumerate(DOCS['scheme']))
        text += '\n## Original text with furigana folded at its printed character\n'
        text += ''.join(f'\n### Physical page {i + 1}\n\n' + '\n'.join(' '.join(g[2] for g in row) for row in page_rows(page)) + '\n' for i, page in enumerate(DOCS['scheme']))
        PATHS['scheme'].with_suffix('.md').write_text(text.rstrip() + '\n')
        (ROOT / 'scripts/markbank/authoring/reviews/japanese-2017-ol.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
        manifest = ROOT / 'components/MarkBank/figures-japanese.json'
        previous = json.loads(manifest.read_text())
        previous.update(FIGURES)
        manifest.write_text(json.dumps(previous, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'cards': len(CARDS), 'marks': sum(card['totalMarks'] for card in CARDS), 'figures': len(FIGURES)}, indent=2))
