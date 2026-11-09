#!/usr/bin/env python3
"""Publish the independently censused 2018 Ordinary sitting from PDF selectors.

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
    'paper': ROOT / 'examiner-reports/japanese/papers/2018-ol-000-paper.pdf',
    'aural': ROOT / 'examiner-reports/japanese/papers/2018-ol-A00-paper.pdf',
    'scheme': ROOT / 'examiner-reports/japanese/schemes/2018-ol.pdf',
}
HASHES = {
    'paper': 'd4350996bef8795c53d2fb0f1e68f763a27bcdb6a4980e30a4ce83127208cef0',
    'aural': '6f7464db7f617ae9c35aea8f4891b4ec0d7518c2ab5d9e893910b2b4d86c455b',
    'scheme': '8140e430a7c93568637fba566e37a27e6928a56eddb2272264b0d93fe195f8a5',
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
    return {'kind': 'source-text', 'label': '2018 Japanese Ordinary Level', 'title': 'Original examination material',
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
    cid = f'ja-2018-ol-{section.lower()}' + (f'-{q}' if q is not None else '') + (f'-{suffix}' if suffix else '')
    ref = f'2018 OL Section {section}' + (f' Q{q}' if q is not None else ' Q' if suffix else '') + ''.join(f'({part})' for part in suffix.split('-') if part)
    listening = section.startswith('L')
    card = {'id': cid, 'source': 'sec', 'subjectId': 'japanese', 'specVersion': 'lc-japanese-syllabus',
            'kind': 'rubric' if rubric else 'question', 'level': 'ordinary', 'year': 2018,
            'section': section[1:] if listening else section[0] if section[0] in '1234' else 'Q5',
            'topicId': topic, 'conceptId': concept_for(question, cid), 'questionRef': ref,
            'questionText': question, 'totalMarks': total if total is not None else sum(map(worth, rows)),
            'qa': {'gates': ['verbatim', 'tariff', 'figure'], 'humanReviewedBy': 'agent-verified', 'humanReviewedAt': '2026-11-09'},
            'sourceEvidence': {'component': 'aural' if listening else 'paper', 'paperPages': pp, 'schemePages': sp},
            'schemeCitation': 'Marking points quoted from the SEC marking scheme, Japanese 2018 Ordinary Level — © State Examinations Commission.'}
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
    instruction = without_marker(col('paper', 3, [0, 1]))
    labels = [re.sub(r'_+', '', col('paper', 3, [row])).strip() for row in range(3, 9)]
    add('1', 1, instruction + '\n' + col('paper', 3, [2]) + '\n' + '\n'.join(labels),
        [point(s(5, row, 2), 2, contextNote=label) for label, row in zip(labels, range(4, 10))],
        'japanese-5-0', [3], [5], reading=[2, 3])
    add('1', 2, without_marker(col('paper', 3, [10, 11])), [point(s(5, 11), 2)],
        'japanese-5-0', [3], [5], reading=[2], stem=p(3, 9, 1))
    instruction = without_marker(col('paper', 3, [13]))
    headers = [p(3, 14, group) for group in [3, 4, 5]]
    events = [col('paper', 3, [16, 18]), col('paper', 3, [20, 22, 24])]
    first_date = s(5, 14, 1).split('(1 mark)')
    rows = []
    for event, answers in zip(events, [[(first_date[0].strip(), 1), (first_date[1].strip(), 1), (s(5, 14, 2), 2)],
                                      [(s(5, 16, 1), 1), (s(5, 18), 1), (s(5, 16, 2), 2)]]):
        rows.extend(point(answer, marks, contextNote=event + ' — ' + headers[1 if i < 2 else 2]) for i, (answer, marks) in enumerate(answers))
    table = add('1', 3, instruction + '\n' + '\n'.join(headers + events), rows, 'japanese-5-0', [3], [5], reading=[2, 3],
                figure=crop('ja-2018-ol-1-3', 3, [.51, .43, .97, .59], instruction))
    table['taskGroups'] = [{'sourceCardId': table['id'] + f'-event-{i + 1}', 'label': event, 'marks': 4,
                            'rowIds': [row['id'] for row in table['rows'][i * 3:i * 3 + 3]]} for i, event in enumerate(events)]
    split = s(5, 21).split('(1 mark)')
    add('1', 4, without_marker(col('paper', 3, [26, 28])), [point(split[0].strip()), point(split[1].strip())],
        'japanese-5-0', [3], [5], reading=[2])
    for q, qr, sr in [(5, 30, [23]), (6, 34, [26, 27])]:
        add('1', q, without_marker(col('paper', 3, [qr])), [anyn(options(5, sr, separator='/'), 3, 2)],
            'japanese-5-0', [3], [5], reading=[2])
    instruction = without_marker(col('paper', 5, [1]))
    labels = [re.sub(r'_+', '', col('paper', 5, [row])).strip() for row in [2, 3, 4]]
    names = [s(6, 3, 1), re.search(r'Hiroshi', s(6, 4)).group(), re.search(r'Michiko', s(6, 5, 1)).group()]
    add('2A', 1, instruction + '\n' + '\n'.join(labels), [], 'japanese-5-2', [5], [6], reading=[4], total=3,
        rubric=pool(3, labels, names, 1, instruction, cell('scheme', 6, 1)), stem=col('paper', 5, [0]))
    for q, qr, rows in [(2, [6, 7], [point(s(6, 7), 2)]), (3, [9], [point(s(6, 9), 2)]),
                        (4, [11, 12], [anyn(options(6, [11], separator='/'), 2, 2, [2, 1])]),
                        (5, [15, 16], [point(s(6, 14), 2)])]:
        add('2A', q, without_marker(col('paper', 5, qr)), rows, 'japanese-5-2', [5], [6], reading=[4], stem=col('paper', 5, [0]))
    instruction = ' '.join(p(5, row) for row in [20, 21])
    labels = [p(5, row, 0) + ' ' + english(p(5, row, 1) + (' ' + p(5, row + 1) if row in [29, 32, 35] else '')) for row in [25, 27, 29, 32, 35]]
    groups = []
    for i, row in enumerate([16, 19, 22, 25, 28]):
        groups.append({'id': f'item-{i + 1}', 'label': labels[i], 'rows': [
            {'id': 'true-false', 'text': s(6, row, 2), 'marks': 1},
            {'id': 'quote', 'text': re.sub(r'\s*2 marks$', '', s(6, row + 2)), 'marks': 2}]})
    add('2B', None, instruction + '\n' + '\n'.join(labels), [], 'japanese-5-2', [5], [6], total=15, reading=[4, 5],
        rubric={'system': 'language-points', 'count': 5, 'taskRequirements': [instruction], 'groups': groups, 'markingGuideNote': cell('scheme', 6, 15)},
        figure=crop('ja-2018-ol-2b', 5, [.075, .505, .97, .92], instruction))
    instruction = p(6, 15)
    labels = [p(6, row) + (' ' + p(6, 24) if row == 23 else '') for row in [17, 18, 19, 20, 21, 22, 23, 25, 26, 27]]
    answers = [s(7, 1, 1)] + [sa(7, row) for row in range(2, 11)]
    add('2C', None, instruction + '\n' + p(6, 16) + '\n' + '\n'.join(labels), [], 'japanese-5-4', [6], [7], total=10, reading=[6],
        rubric=pool(10, labels, answers, 1, instruction, cell('scheme', 7, 0)),
        figure=crop('ja-2018-ol-2c', 6, [.075, .495, .97, .93], instruction))
    question = ' '.join(p(7, row) for row in [6, 7])
    allocation = cell('scheme', 7, 14)
    parts = [{'id': f'point-{i}', 'verbatim': f'{i}. ' + re.search(r'points', allocation).group(), 'marks': 2, 'permittedMarks': [0, 2]} for i in [1, 2]]
    add('2D', None, question, [{'kind': 'criterion', 'verbatim': UNPRINTED, 'unprinted': True, 'marks': 4,
        'permittedMarks': [0, 2, 4], 'parts': parts, 'contextNote': allocation}], 'japanese-5-6', [7], [7],
        stem=' '.join(p(7, row) for row in [2, 3]))
    for q, qr, answer in [(1, [1], re.search(r'Golden week$', s(8, 2)).group()), (2, [4], re.search(r'English$', s(8, 3)).group())]:
        add('3A', q, without_marker(col('paper', 9, qr)), [point(answer, 2)], 'japanese-5-1', [9], [8], reading=[8], stem=p(9, 0, 1))
    for roman, qr, sr, answer in [('i', 8, 5, 'Japanese'), ('ii', 9, 6, 'Irish')]:
        selected = re.search(answer, s(8, sr)).group()
        question = without_marker(col('paper', 9, [7])) + ' ' + re.sub(r'_+', '', without_marker(col('paper', 9, [qr]))).strip()
        add('3A', 3, question, [point(selected, 2)], 'japanese-5-1', [9], [8], roman, reading=[8])
    for roman, qr, answer in [('i', range(12, 17), re.sub(r'\s*2 marks$', '', s(8, 9, 1))),
                              ('ii', range(17, 22), re.sub(r'\s*2 marks$', '', s(8, 10, 1))),
                              ('iii', range(22, 28), re.search(r'a\. his birthday$', s(8, 11)).group())]:
        add('3A', 4, without_marker(col('paper', 9, qr)), [point(answer, 2)], 'japanese-5-1', [9], [8], roman,
            reading=[8], stem=without_marker(col('paper', 9, [10, 11])))
    for q, qr, sr in [(1, 29, 14), (2, 31, 16), (3, 33, 18)]:
        add('3B', q, without_marker(p(9, qr)), [point(s(8, sr), 3)], 'japanese-5-1', [9], [8], reading=[8], stem=english(p(9, 28, 1)))
    for q, instruction_row, example, lr, rr, region in [(1, 2, 3, range(4, 9), range(2, 7), [.075, .065, .97, .405]),
                                                      (2, 10, 11, range(12, 17), range(8, 13), [.075, .405, .97, .76])]:
        instruction = p(10, instruction_row)
        labels = [p(10, row) for row in lr]
        answers = []
        for row in rr:
            group = 1 if row in ([2, 3] if q == 1 else [8, 11]) else 0
            answers.append(re.sub(r'\s*2 marks$', '', without_marker(s(9, row, group))))
        add('3C', q, instruction + '\n' + p(10, example) + '\n' + '\n'.join(labels), [], 'japanese-5-5', [10], [9], total=10, reading=[10],
            rubric=pool(5, labels, answers, 2, instruction, cell('scheme', 9, 1 if q == 1 else 7)),
            figure=crop(f'ja-2018-ol-3c-{q}', 10, region, instruction))


def writing():
    instruction = ' '.join(p(11, row) for row in [4, 5])
    question = instruction + '\n' + '\n'.join(p(11, row) for row in range(6, 21))
    labels = [re.match(r'\([ivx]+\)', s(10, row)).group() for row in range(2, 12)]
    answers = [s(10, row, 1) if row != 9 else sa(10, row) for row in range(2, 12)]
    add('4', None, question, [], 'japanese-5-7', [11], [10],
        rubric=pool(10, labels, answers, 3, instruction, cell('scheme', 10, 1)), total=30,
        reading=[11], figure=crop('ja-2018-ol-4', 11, [.075, .065, .97, .925], instruction))
    instruction = p(12, 2)
    labels = [p(12, row) for row in range(3, 10)]
    content_bands = [{'label': s(10, row), 'marks': marks, 'guidance': [s(10, row, 1)]}
                     for row, marks in [(26, [1]), (25, [2, 3]), (24, [4, 5])]]
    expression_bands = [{'label': s(11, first), 'marks': marks,
                         'guidance': [s(11, first, 1) + ' ' + ' '.join(s(11, row) for row in rest)]}
                        for first, rest, marks in [(13, range(14, 20), [1]), (20, range(21, 27), [2, 3]), (27, range(28, 34), [4, 5])]]
    cap = joined_selector('scheme', 11, [(1, 0), (2, 0)])
    first = s(10, 15, 1)
    first_parts = first.split('(2 marks)')
    groups = []
    for i, label in enumerate(labels, 1):
        if i == 1:
            criteria = [{'id': f'item-1-{name}', 'label': first_parts[index].strip(), 'maxMarks': 2,
                         'permittedMarks': [0, 2], 'guidance': [first]}
                        for index, name in enumerate(['name', 'age'])]
            criteria.append({'id': 'item-1-discretionary', 'label': s(10, 16), 'maxMarks': 1,
                             'permittedMarks': [0, 1], 'guidance': [s(10, 16)]})
        else:
            criteria = [{'id': f'item-{i}-content', 'label': s(10, 23).removesuffix(':'), 'maxMarks': 5,
                         'permittedMarks': list(range(6)), 'guidance': [s(10, 14)], 'bands': content_bands}]
        content_ids = [criterion['id'] for criterion in criteria]
        criteria.append({'id': f'item-{i}-expression', 'label': s(11, 0).removesuffix(':'), 'maxMarks': 5,
                         'permittedMarks': list(range(6)), 'guidance': [cap], 'bands': expression_bands,
                         'limits': [{'id': f'item-{i}-low-content', 'maxMarks': 3, 'when': {'any': [{'criterionIds': content_ids, 'atMost': 3}]}, 'guidance': [cap]}]})
        groups.append({'id': f'item-{i}', 'label': label, 'rows': [], 'criteria': criteria})
    discrepancy = ('The original paper asks what you do together at(iii) and what your friend likes at(iv). '
                   'The scheme restates likes at(iii), then repeats age at(iv), already asked in(i), and omits do-together from its prompt restatement. '
                   'Keep the seven original paper prompts and apply the printed common content/expression rubric; the repeated scheme age prompt is not an extra or replacement question.')
    for row in [17, 18, 19, 20, 21, 22]:
        cell('scheme', 10, row)
    rubric = {'system': 'language-points', 'count': 5, 'taskRequirements': [instruction], 'groups': groups,
              'markingGuideNote': s(10, 13) + ' ' + s(10, 14) + ' ' + cap + ' ' + s(11, 34) + ' ' + s(11, 35) + ' — ' + discrepancy}
    add('5', None, instruction + '\n' + '\n'.join(labels), [], 'japanese-5-7', [12], [10, 11], rubric=rubric, total=50,
        reading=[12], figure=crop('ja-2018-ol-5', 12, [.05, .04, .97, .935], instruction))


def listening():
    def listen(section, q, roman, qr, answers):
        page = {'A': 2, 'B': 3, 'C': 4, 'D': 5}[section]
        topic = 'japanese-6-2' if section == 'B' else 'japanese-6-0'
        question = re.sub(r'^(?:\d+\.?\s*)?(?:\([ivx]+\)\s*)?', '', col('aural', page, qr, 290)).strip()
        card = add('L' + section, q, question, answers, topic, [page], [3 if section in 'AB' else 4], roman, reading=[page])
        if section == 'B':
            card['stem'] = col('aural', page, [1, 2])
            for row, marker in [(3, 'item will'), (4, 'then in')]:
                text = cell('aural', page, row).replace('\xa0', ' ')
                card['stem'] += ' ' + marker + text.split(marker, 1)[1]
            card['stem'] += ' ' + col('aural', page, [5]) + '\n' + col('aural', page, [{1: 6, 2: 18, 3: 30}[q]])
        else:
            card['stem'] = col('aural', page, range(1, 5))
            if section in 'CD':
                card['stem'] += '\n' + col('aural', page, [5 if q == 1 else 23 if section == 'C' else 20])
        return card
    full = s(3, 3, 2)
    parts = full.split('(1 mark)')
    listen('A', 1, 'i', [6], [point(parts[0].strip()), point(parts[1].strip())])
    for q, roman, qr, sr, sg, marks in [(1, 'ii', range(8, 13), 4, 1, 4), (1, 'iii', range(13, 19), 5, 1, 4),
        (2, 'i', [19, 20], 6, 2, 2), (2, 'ii', range(22, 27), 7, 1, 4), (2, 'iii', range(27, 32), 8, 1, 4),
        (3, 'i', [32, 33], 9, 2, 2), (3, 'ii', range(35, 41), 10, 1, 4)]:
        listen('A', q, roman, qr, [point(s(3, sr, sg), marks)])
    listen('B', 1, 'i', [7], [point(s(3, 13, 1), 2)])
    listen('B', 1, 'ii', range(10, 15), [point(s(3, 14, 1), 4)])
    phone_source = cell('scheme', 3, 15)
    number = re.search(r'\d{2}-\d{4}-\d{4}', phone_source).group()
    digits = number.replace('-', '')
    rows = [point(digits[position - 1], contextNote=f'Missing digit {index + 1} (position {position} in {number}). {phone_source} — Only the four missing digits score; the printed digits are given.')
            for index, position in enumerate([4, 5, 7, 8])]
    phone = listen('B', 1, 'iii', [15], rows)
    phone['questionFigureKey'] = crop('ja-2018-ol-lb-1-iii', 3, [.50, .37, .95, .46], phone['questionText'], 'aural')
    listen('B', 2, 'i', [19, 20], [point(s(3, 17, 1), 2)])
    listen('B', 2, 'ii', range(22, 27), [point(sa(3, 18), 4)])
    listen('B', 2, 'iii', [27], [anyn(sa(3, 19).split('/'), 1, 2)])
    full = s(3, 22, 1)
    listen('B', 3, 'i', [31], [point(full.split(' (')[0], 4, kind='criterion', permittedMarks=[0, 2, 4], contextNote=full)])
    listen('B', 3, 'ii', range(33, 38), [point(sa(3, 23), 4)])
    for q, roman, qr, sr, marks in [(1, 'i', [6], 2, 2), (1, 'ii', range(8, 13), 3, 4),
                                  (1, 'iii', range(13, 18), 4, 4), (1, 'iv', range(18, 23), 5, 4),
                                  (2, 'i', range(24, 29), 7, 4), (2, 'ii', range(29, 34), 8, 4), (2, 'iii', [34], 9, 2)]:
        listen('C', q, roman, qr, [point(s(4, sr, 1), marks)])
    for q, roman, qr, sr in [(1, 'i', range(6, 11), 12), (1, 'ii', [11], 13), (1, 'iii', range(14, 19), 14),
                            (2, 'i', [21], 16), (2, 'ii', range(23, 29), 17), (2, 'iii', range(30, 35), 18)]:
        listen('D', q, roman, qr, [point(s(4, sr, 1), 4)])


def build():
    reading()
    writing()
    listening()
    census = json.loads((Path(__file__).parent / 'reviews/japanese-2018-ol-census.json').read_text())
    expected = {'ja-2018-ol-' + '-'.join(str(part).lower() for part in task['key'] if part is not None): task for task in census['tasks']}
    assert set(expected) == {card['id'] for card in CARDS}
    for card in CARDS:
        task = expected[card['id']]
        assert card['totalMarks'] == task['marks'], (card['id'], card['totalMarks'], task['marks'])
        assert card['sourceEvidence']['paperPages'] == task['paperPages']
        assert card['sourceEvidence']['schemePages'] == task['schemePages']
    assert len(CARDS) == 57
    assert sum(card['totalMarks'] for card in CARDS) == 300
    assert sum('answerLanguageRule' in card for card in CARDS) == 55
    assert not any(card['id'] in ORIGINAL_IDS for card in CARDS)
    return {'subjectId': 'japanese', 'sitting': '2018-ol', 'reviewedAt': '2026-11-09',
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
        (ROOT / 'scripts/markbank/authoring/reviews/japanese-2018-ol.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
        manifest = ROOT / 'components/MarkBank/figures-japanese.json'
        previous = json.loads(manifest.read_text())
        previous.update(FIGURES)
        manifest.write_text(json.dumps(previous, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'cards': len(CARDS), 'marks': sum(card['totalMarks'] for card in CARDS), 'figures': len(FIGURES)}, indent=2))
