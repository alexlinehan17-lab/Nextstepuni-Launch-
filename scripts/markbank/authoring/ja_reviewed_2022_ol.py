#!/usr/bin/env python3
"""Publish the independently censused 2022 Ordinary sitting from PDF selectors.

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
    'paper': ROOT / 'examiner-reports/japanese/papers/2022-ol-000-paper.pdf',
    'aural': ROOT / 'examiner-reports/japanese/papers/2022-ol-A00-paper.pdf',
    'scheme': ROOT / 'examiner-reports/japanese/schemes/2022-ol.pdf',
}
HASHES = {
    'paper': 'f74fee39f437d293d101cb9f8ee3743eb1c268f7bc01950fa3016f59baaa32f1',
    'aural': '0967cbf965a69d1d695174b6104824c174b13ff582c7cb379a39e8c209de5ad8',
    'scheme': 'e348bdf1ac02f46c9c73350d1b7fbde4505a8d4f0dc0ff406ed4ac2d4e11093d',
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
    return {'kind': 'source-text', 'label': '2022 Japanese Ordinary Level', 'title': 'Original examination material',
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
    cid = f'ja-2022-ol-{section.lower()}' + (f'-{q}' if q is not None else '') + (f'-{suffix}' if suffix else '')
    ref = f'2022 OL Section {section}' + (f' Q{q}' if q is not None else '') + ''.join(f'({part})' for part in suffix.split('-') if part)
    listening = section.startswith('L')
    card = {'id': cid, 'source': 'sec', 'subjectId': 'japanese', 'specVersion': 'lc-japanese-syllabus',
            'kind': 'rubric' if rubric else 'question', 'level': 'ordinary', 'year': 2022,
            'section': section[1:] if listening else section[0] if section[0] in '1234' else 'Q5',
            'topicId': topic, 'conceptId': concept_for(question, cid), 'questionRef': ref,
            'questionText': question, 'totalMarks': total if total is not None else sum(map(worth, rows)),
            'qa': {'gates': ['verbatim', 'tariff', 'figure'], 'humanReviewedBy': 'agent-verified', 'humanReviewedAt': '2026-11-09'},
            'sourceEvidence': {'component': 'aural' if listening else 'paper', 'paperPages': pp, 'schemePages': sp},
            'schemeCitation': 'Marking points quoted from the SEC marking scheme, Japanese 2022 Ordinary Level — © State Examinations Commission.'}
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


Q2_DISCREPANCY = 'The published Q2 heading says 42 marks, but its explicit local allocations are A14 + B15 + C10 + D4 = 43. These cards retain the local tariffs. The reading tasks therefore sum to 121 rather than the printed section total of 120.'


def reading():
    instruction = without_marker(col('paper', 3, [0, 1]))
    labels = [re.sub(r'_+', '', col('paper', 3, [row])).strip() for row in range(3, 9)]
    answers = [s(5, row, 2 if row < 9 else 1) for row in range(4, 10)]
    add('1', 1, instruction + '\n' + p(3, 2, 2) + ' ' + p(3, 2, 3) + '\n' + '\n'.join(labels),
        [point(answer, 2, contextNote=label) for label, answer in zip(labels, answers)],
        'japanese-5-0', [3], [5], reading=[2, 3])
    for q, qr, sr, count, marks, separator in [
        (2, [10], 11, 1, 2, '/'), (3, [13], 13, 1, 2, '/'), (4, [16, 17], 15, 3, 1, ',')]:
        add('1', q, without_marker(col('paper', 3, qr)), [anyn(options(5, [sr], separator=separator), count, marks)],
            'japanese-5-0', [3], [5], reading=[2], stem=p(3, 9, 1))
    for roman, qr, sr in [('i', 23, 17), ('ii', 24, 18)]:
        add('1', 5, without_marker(col('paper', 3, [qr])), [point(s(5, sr, 2), 2)], 'japanese-5-0', [3], [5], roman,
            reading=[2], stem=without_marker(col('paper', 3, [21, 22])))
    table_text = without_marker(p(3, 26)) + '\n' + '\n'.join(p(3, row, 1) for row in range(27, 32))
    date = [text.strip() for text in s(5, 20, 1).split('(1 mark)') if text.strip()]
    time = [re.sub(r'\s*\(\s*1 mark\)\s*$', '', s(5, row)).strip() for row in [21, 23]]
    login = re.sub(r'\s*\(1 mark\)\s*$', '', s(5, 24)).strip()
    rows = [*[point(text, contextNote=s(5, 20, 0)) for text in date],
            *[point(text, contextNote=s(5, 22)) for text in time], point(login, contextNote=s(5, 25)),
            anyn(options(5, [26], separator='/'), 1, 2, contextNote=s(5, 27) + ' ' + s(5, 28))]
    add('1', 6, table_text, rows, 'japanese-5-0', [3], [5], reading=[2, 3], stem=p(3, 9, 1),
        figure=crop('ja-2022-ol-1-6', 3, [.51, .738, .96, .92], table_text))
    for q, qr, rows in [
        (1, [1, 2], [point(s(6, 3), 2)]),
        (2, [4], [anyn(options(6, [5], separator='/'), 2, 2)]),
        (3, [6], [point(s(6, 8), 2)]),
        (4, [8, 9], [anyn(options(6, [10]), 1, 2)]),
        (5, [11], [point(s(6, 12), 2)]),
        (6, [14, 15], [point(s(6, 14), 2)]),
    ]:
        rows[0]['contextNote'] = Q2_DISCREPANCY
        add('2A', q, without_marker(col('paper', 5, qr)), rows, 'japanese-5-2', [5], [6], reading=[4],
            stem=without_marker(col('paper', 5, [0])))
    instruction = english(' '.join(p(5, row) for row in range(18, 22)))
    labels = []
    for rows in [[24, 25], [27, 28], [30], [32, 33], [35, 36], [38, 39]]:
        text = ' '.join(p(5, row) for row in rows)
        labels.append(re.match(r'\([ivx]+\)', text).group() + ' ' + english(text))
    groups = []
    for i, (tr, tg, qr) in enumerate([(19, 0, 20), (22, 1, 22), (25, 0, 26), (29, 0, 30), (33, 1, 33), (36, 1, 36)], 1):
        groups.append({'id': f'item-{i}', 'label': labels[i - 1], 'rows': [
            {'id': 'true-false', 'text': s(6, tr, tg), 'marks': 1},
            {'id': 'quote', 'text': s(6, qr), 'marks': 2}]})
    add('2B', None, instruction + '\n' + '\n'.join(labels), [], 'japanese-5-2', [5], [6],
        rubric={'system': 'language-points', 'count': 5, 'taskRequirements': [instruction], 'groups': groups,
                'markingGuideNote': cell('scheme', 6, 15) + ' ' + Q2_DISCREPANCY}, total=15, reading=[4, 5],
        figure=crop('ja-2022-ol-2b', 5, [.075, .475, .97, .905], instruction))
    instruction = p(6, 17)
    labels = [p(6, row) for row in range(19, 32)]
    answers = [sa(7, row, 1 if row in [2, 3, 6, 11] else 0) for row in range(2, 15)]
    add('2C', None, instruction + '\n' + p(6, 18) + '\n' + '\n'.join(labels), [], 'japanese-5-4', [6], [7],
        rubric=pool(10, labels, answers, 1, instruction, cell('scheme', 7, 1) + ' ' + Q2_DISCREPANCY), total=10, reading=[6],
        figure=crop('ja-2022-ol-2c', 6, [.075, .49, .97, .91], instruction))
    question = english(' '.join(p(7, row) for row in [3, 4, 5]))
    allocation = cell('scheme', 7, 17)
    point_label = re.search(r'\bpoints\b', allocation).group()
    parts = [{'id': f'point-{i}', 'verbatim': f'{i}. {point_label}', 'marks': 2, 'permittedMarks': [0, 2]} for i in [1, 2]]
    add('2D', None, question, [{'kind': 'criterion', 'verbatim': UNPRINTED, 'unprinted': True, 'marks': 4,
        'permittedMarks': [0, 2, 4], 'parts': parts, 'contextNote': allocation + ' ' + Q2_DISCREPANCY}],
        'japanese-5-6', [7], [7], stem=english(' '.join(p(7, row) for row in [0, 1, 2])))
    for q, qr, rows in [(1, [1], [point(s(7, 21), 2)]),
                       (2, [3], [anyn(options(7, [23], separator='/'), 2, 2, [2, 1])]),
                       (3, [6], [point(s(7, 26), 2)])]:
        add('3A', q, without_marker(col('paper', 9, qr)), rows, 'japanese-5-2', [9], [7], reading=[8], stem=p(9, 0, 1))
    for roman, qr, sr in [('i', range(10, 15), 28), ('ii', range(15, 20), 30),
                           ('iii', range(20, 26), 32), ('iv', [26, 27, 29, 31, 33, 35], 34)]:
        add('3A', 4, without_marker(col('paper', 9, qr)), [point(s(7, sr), 3)], 'japanese-5-2', [9], [7], roman,
            reading=[8], stem=without_marker(col('paper', 9, [8, 9])))
    instruction = english(p(10, 0, 1))
    labels = [p(10, row) for row in [1, 3, 5, 7]]
    add('3A', 5, instruction + '\n' + '\n'.join(labels), [], 'japanese-5-2', [10], [8],
        rubric=pool(3, labels, [s(8, row) for row in [2, 4, 6, 8]], 3, instruction,
                    cell('scheme', 8, 0) + ' The paper labels this pool Q3A5; the scheme calls it B.'), total=9, reading=[8, 10])
    for q, pp, qr, lr, example, sr, rr, region in [
        (1, 10, [10, 11], range(13, 19), 12, 10, range(11, 17), [.075, .35, .97, .79]),
        (2, 11, [0, 1], range(3, 9), 2, 17, range(18, 24), [.075, .06, .97, .50]),
    ]:
        instruction = english(' '.join(p(pp, row) for row in qr))
        labels = [p(pp, row) for row in lr]
        answers = [sa(8, row, 0 if row in [16, 22, 23] else 1) for row in rr]
        add('3B', q, instruction + '\n' + p(pp, example) + '\n' + '\n'.join(labels), [], 'japanese-5-5', [pp], [8],
            rubric=pool(5, labels, answers, 2, instruction, cell('scheme', 8, sr) + ' The paper labels this grammar section B; the scheme calls it C.'),
            total=10, reading=[pp], figure=crop(f'ja-2022-ol-3b-{q}', pp, region, instruction))


def writing():
    choice = english(p(12, 1))
    instruction = english(' '.join(p(12, row) for row in [3, 4, 5]))
    question = choice + '\n' + instruction + '\n' + '\n'.join(p(12, row) for row in range(6, 20))
    labels = [s(9, row, 0) for row in range(2, 14)]
    answers = [s(9, row, 1) for row in range(2, 14)]
    add('4', None, question, [], 'japanese-5-7', [12], [9],
        rubric=pool(10, labels, answers, 4, instruction, cell('scheme', 9, 1) + ' ' + choice), total=40,
        reading=[12], figure=crop('ja-2022-ol-4', 12, [.075, .04, .97, .88], instruction))
    instruction = english(' '.join(p(13, row) for row in [1, 2, 3]))
    labels = [p(13, row) for row in range(4, 12)]
    content_bands = [{'label': s(9, row), 'marks': marks, 'guidance': [s(9, row, 1)]}
                     for row, marks in [(28, [1]), (27, [2, 3]), (26, [4])]]
    expression_bands = [{'label': s(10, first), 'marks': marks,
                         'guidance': [s(10, first, 1) + ' ' + ' '.join(s(10, row) for row in rest)]}
                        for first, rest, marks in [(10, range(11, 17), [1]), (17, range(18, 25), [2, 3]), (25, range(26, 32), [4])]]
    groups = []
    for i, label in enumerate(labels, 1):
        criteria = [
            {'id': f'item-{i}-content', 'label': s(9, 25).removesuffix(':'), 'maxMarks': 4,
             'permittedMarks': list(range(5)), 'guidance': [s(9, 16)], 'bands': content_bands},
            {'id': f'item-{i}-expression', 'label': s(10, 0).removesuffix(':'), 'maxMarks': 4,
             'permittedMarks': list(range(5)), 'guidance': [s(10, 0, 1)], 'bands': expression_bands},
        ]
        groups.append({'id': f'item-{i}', 'label': label, 'rows': [], 'criteria': criteria})
    rubric = {'system': 'language-points', 'count': 5, 'taskRequirements': [choice, instruction], 'groups': groups,
              'markingGuideNote': cell('scheme', 9, 15) + ' ' + s(9, 16) + ' ' + s(10, 32) + ' ' + s(10, 33)}
    add('5', None, choice + '\n' + instruction + '\n' + '\n'.join(labels), [], 'japanese-5-7', [13], [9, 10],
        rubric=rubric, total=40, reading=[13], figure=crop('ja-2022-ol-5', 13, [.05, .04, .97, .943], instruction))


def listening():
    def aq(page, rows):
        return re.sub(r'^(?:\d+\.\s*)?(?:\([ivx]+\)\s*)?', '', col('aural', page, rows, 290)).strip()

    def listen(section, q, roman, qr, answers, question=None):
        page = {'A': 2, 'B': 3, 'C': 4, 'D': 5}[section]
        topic = {'A': 'japanese-6-1', 'B': 'japanese-6-2', 'C': 'japanese-6-0', 'D': 'japanese-6-0'}[section]
        card = add('L' + section, q, question or aq(page, qr), answers, topic,
                   [page], [3 if section in 'AB' else 4], roman, reading=[page])
        card['stem'] = col('aural', page, [1] if section == 'D' else [1, 2], 290)
        context = {'A': {1: 4, 2: 22, 3: 39}, 'B': {1: 3, 2: 28},
                   'C': {1: 3, 2: 12, 3: 21}, 'D': {1: 2, 2: 27}}[section][q]
        card['stem'] += '\n' + col('aural', page, [context], 290)
        return card

    for q, roman, qr, sr, marks in [
        (1, 'i', range(5, 11), 4, 4), (1, 'ii', range(12, 17), 5, 4),
        (1, 'iii', [18], 6, 2), (2, 'i', [24, 26, 28, 30, 32, 34], 8, 4),
        (2, 'ii', [36], 9, 2), (3, 'ii', [51], 12, 2), (3, 'iii', range(53, 58), 13, 4),
    ]:
        listen('A', q, roman, qr, [point(sa(3, sr), marks)])
    andrea = cell('aural', 2, 40).rsplit('(i)', 1)[1].strip() + ' ' + col('aural', 2, [42, 44, 46, 48])
    listen('A', 3, 'i', [], [point(sa(3, 11), 4)], andrea)
    listen('B', 1, 'i', [4, 5, 6, 8, 9], [point(sa(3, 16), 4)])
    listen('B', 1, 'ii', [11], [point(sa(3, 17), 2)])
    types = re.sub(r'\s*\(any.*$', '', sa(3, 18))
    listen('B', 1, 'iii', [13], [anyn([text.strip() for text in types.split('/')], 2, 2)])
    listen('B', 1, 'iv', [15, 17, 19, 21, 23, 25], [point(sa(3, 19), 4)])
    phone_rule = cell('scheme', 3, 20)
    phone = listen('B', 1, 'v', [26], [point(sa(3, 20), 4)])
    # The question total is explicit, but no consistent partial allocation is.
    # Keep this as unpriced answer review, never an invented set of score steps.
    phone['tariffModel'] = {'kind': 'questionTotal'}
    phone['rows'][0]['marks'] = None
    phone['rows'][0]['contextNote'] = (
        'Unresolved source scoring conflict: the scheme prints a 4-mark total and also '
        '“any two digits, 1 mark each”. The original paper has eight missing digits. '
        'These published statements are inconsistent. The full answer and question total '
        'are reproduced; no per-digit allocation or partial-credit scale is inferred. '
        'Use this card for answer review and consult examiner guidance for an exact award. '
        + phone['answerLanguageRule']['sourceText'])
    # This task asks for digits only. Preserve the general language instruction
    # visibly above; do not attach an unsupported scoring control to questionTotal.
    del phone['answerLanguageRule']
    phone['qa']['gates'].remove('tariff')
    phone['qa']['gates'].append('source-tariff-unresolved')
    phone['questionFigureKey'] = crop('ja-2022-ol-lb-1-v', 3, [.51, .552, .94, .639], phone['questionText'], 'aural')
    phone['sourceEvidence']['scoringClarification'] = {'status': 'unresolved-published-conflict', 'sourceText': phone_rule,
        'issue': 'Four-mark published total conflicts with any-two-digits one-mark partial clause and eight paper blanks. Independently confirmed from both originals; no partial allocation adjudicated.'}
    weather = re.sub(r'\s*\(any.*$', '', sa(3, 22))
    listen('B', 2, 'i', [29, 30], [anyn([text.strip() for text in weather.split(',')], 1, 2)])
    listen('B', 2, 'ii', [32, 34, 35, 36, 37], [point(sa(3, 23), 4)])
    listen('C', 1, 'i', range(4, 9), [point(sa(4, 2), 4)])
    stranger = re.sub(r'\s*\(any.*$', '', sa(4, 3))
    listen('C', 1, 'ii', [9], [anyn([text.strip() for text in stranger.split(',')], 2, 2)])
    listen('C', 2, 'i', range(13, 18), [point(sa(4, 6), 4)])
    listen('C', 2, 'ii', [18, 19], [point(sa(4, 7), 2)])
    listen('C', 3, 'i', [22, 23, 25, 26, 28], [point(sa(4, 9), 4)])
    listen('C', 3, 'ii', [29, 30, 32, 33, 34], [point(sa(4, 10), 4)])
    listen('C', 3, 'iii', [35, 36, 38, 39, 40], [point(sa(4, 11), 4,
        contextNote='This response is paper (iii), printed (vii) in the scheme. The question wording and answer match.')])
    for q, roman, qr, sr, marks in [
        (1, 'i', [3], 14, 2), (1, 'ii', [5, 7, 9, 11, 13, 15], 15, 4),
        (1, 'iii', [17, 18, 19, 20, 21], 16, 2), (1, 'iv', [23], 17, 2),
        (2, 'iii', range(32, 37), 21, 4), (2, 'iv', range(37, 42), 22, 4),
    ]:
        listen('D', q, roman, qr, [point(sa(4, sr), marks)])
    for roman, qr, sr in [('i', 28, 19), ('ii', 30, 20)]:
        listen('D', 2, roman, [qr], [anyn([text.strip() for text in sa(4, sr).split('/')], 1, 3)])


def consolidations(census):
    records = []
    romans = ['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x', 'xi', 'xii', 'xiii']
    for suffix, count, pp, pr, sp, sr, reason in [
        ('1-1', 6, 3, [0, 1], 5, 3, 'One required six-link matching task, two marks per cell; keep all printed links and items.'),
        ('2b', 6, 5, [18, 19, 20, 21], 6, 15, 'One any-five-of-six pool; each chosen response retains truth1 and supporting Japanese evidence2.'),
        ('2c', 13, 6, [17], 7, 1, 'One any-ten-of-thirteen kanji meaning pool, one mark per chosen answer.'),
        ('3a-5', 4, 10, [0], 8, 0, 'One any-three-of-four Japanese-response pool, three marks per chosen answer.'),
        ('3b-1', 6, 10, [10, 11], 8, 10, 'One any-five-of-six past-tense pool, two marks per chosen answer.'),
        ('3b-2', 6, 11, [0, 1], 8, 17, 'One any-five-of-six particle pool, two marks per chosen answer.'),
    ]:
        canonical = 'ja-2022-ol-' + suffix
        task = next(task for task in census['tasks'] if canonical == 'ja-2022-ol-' + '-'.join(str(part).lower() for part in task['key'] if part is not None))
        records.append({'canonicalId': canonical, 'legacyIds': [canonical + '-' + part for part in romans[:count]],
                        'taskKey': task['key'], 'marks': task['marks'], 'reason': reason,
                        'paperEvidence': {'page': pp, 'text': joined_selector('paper', pp, [(row, None) for row in pr])},
                        'schemeEvidence': {'page': sp, 'text': cell('scheme', sp, sr)}})
    return records


def build():
    reading()
    writing()
    listening()
    census = json.loads((Path(__file__).parent / 'reviews/japanese-2022-ol-census.json').read_text())
    expected = {'ja-2022-ol-' + '-'.join(str(part).lower() for part in task['key'] if part is not None): task for task in census['tasks']}
    assert set(expected) == {card['id'] for card in CARDS}
    for card in CARDS:
        task = expected[card['id']]
        assert card['totalMarks'] == task['marks'], (card['id'], card['totalMarks'], task['marks'])
        assert card['sourceEvidence']['paperPages'] == task['paperPages']
        assert card['sourceEvidence']['schemePages'] == task['schemePages']
    assert len(CARDS) == 58
    assert sum(card['totalMarks'] for card in CARDS) == 301
    return {'subjectId': 'japanese', 'sitting': '2022-ol', 'reviewedAt': '2026-11-09',
            'sources': [{'document': name, 'path': str(path.relative_to(ROOT)), 'sha256': HASHES[name],
                         'pagesReviewed': list(range(1, len(DOCS[name]) + 1))} for name, path in PATHS.items()],
            'cards': CARDS, 'selectors': EVIDENCE, 'status': 'source-captured-with-unresolved-tariff',
            'unresolvedSourceIssues': [{'cardId': 'ja-2022-ol-lb-1-v', 'kind': 'partial-credit-conflict',
                                       'paperPages': [3], 'schemePages': [3],
                                       'resolution': None, 'runtimeTreatment': 'Unpriced answer review with printed question total and visible original conflict; not an adjudicated partial-credit scale.'}],
            'choiceAnalysis': census['choiceBoundaries'], 'consolidations': consolidations(census)}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    result = build()
    if args.write:
        (ROOT / 'scripts/markbank/authoring/reviews/japanese-2022-ol.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
        manifest = ROOT / 'components/MarkBank/figures-japanese.json'
        previous = json.loads(manifest.read_text())
        previous.update(FIGURES)
        manifest.write_text(json.dumps(previous, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'cards': len(CARDS), 'marks': sum(card['totalMarks'] for card in CARDS), 'figures': len(FIGURES)}, indent=2))
