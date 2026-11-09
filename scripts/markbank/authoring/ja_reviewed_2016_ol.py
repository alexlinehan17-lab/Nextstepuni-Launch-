#!/usr/bin/env python3
"""Publish the independently censused 2016 Ordinary sitting from PDF selectors.

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
    'paper': ROOT / 'examiner-reports/japanese/papers/2016-ol-000-paper.pdf',
    'aural': ROOT / 'examiner-reports/japanese/papers/2016-ol-A00-paper.pdf',
    'scheme': ROOT / 'examiner-reports/japanese/schemes/2016-ol.pdf',
}
HASHES = {
    'paper': '9377b217ba808b6320baa90d17f5fa0a1a33c65cb520f363a4cdef944067e4b7',
    'aural': 'acacbc404fed69359b1e90797d1263307fc7a2cbbd0c6ea0124c9e6e98d163e1',
    'scheme': 'd9cf9b92a4cebec8e58be494bd8388efddd680651e1271d1a08bfe42dadea3c5',
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
    return text.replace('\xa0', ' ').split(' / ', 1)[-1].strip()


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
    return {'kind': 'source-text', 'label': '2016 Japanese Ordinary Level', 'title': 'Original examination material',
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
    cid = f'ja-2016-ol-{section.lower()}' + (f'-{q}' if q is not None else '') + (f'-{suffix}' if suffix else '')
    ref = f'2016 OL Section {section}' + (f' Q{q}' if q is not None else ' Q' if suffix else '') + ''.join(f'({part})' for part in suffix.split('-') if part)
    listening = section.startswith('L')
    card = {'id': cid, 'source': 'sec', 'subjectId': 'japanese', 'specVersion': 'lc-japanese-syllabus',
            'kind': 'rubric' if rubric else 'question', 'level': 'ordinary', 'year': 2016,
            'section': section[1:] if listening else section[0] if section[0] in '1234' else 'Q5',
            'topicId': topic, 'conceptId': concept_for(question, cid), 'questionRef': ref,
            'questionText': question, 'totalMarks': total if total is not None else sum(map(worth, rows)),
            'qa': {'gates': ['verbatim', 'tariff', 'figure'], 'humanReviewedBy': 'agent-verified', 'humanReviewedAt': '2026-11-09'},
            'sourceEvidence': {'component': 'aural' if listening else 'paper', 'paperPages': pp, 'schemePages': sp},
            'schemeCitation': 'Marking points quoted from the SEC marking scheme, Japanese 2016 Ordinary Level — © State Examinations Commission.'}
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

def clean_label(text):
    return re.sub(r'_+', '', text).strip()


def reading():
    instruction = without_marker(col('paper', 3, [0, 1]))
    labels = [clean_label(col('paper', 3, [row])) for row in range(3, 8)]
    add('1', 1, instruction + '\n' + col('paper', 3, [2]) + '\n' + '\n'.join(labels),
        [point(s(5, row, 2), 2, contextNote=label) for label, row in zip(labels, range(4, 9))],
        'japanese-5-0', [3], [5], reading=[2, 3])
    date = s(5, 10)
    add('1', 2, without_marker(col('paper', 3, [9, 10])),
        [point(part.strip(), 1) for part in date.split('(1 mark)') if part.strip()],
        'japanese-5-0', [3], [5], reading=[2], stem=p(3, 8, 1))
    for q, qr, lr, answers in [
        (3, [12, 13], [14, 15], [s(5, 12, 2), s(5, 13, 2)]),
        (5, [18, 19], [20, 21, 22], [s(5, 17, 2), s(5, 18, 1).removeprefix('November '), s(5, 19, 1).removeprefix('December ')])]:
        labels = [clean_label(col('paper', 3, [row])) for row in lr]
        add('1', q, without_marker(col('paper', 3, qr)) + '\n' + '\n'.join(labels),
            [point(answer, 2, contextNote=label) for answer, label in zip(answers, labels)],
            'japanese-5-0', [3], [5], reading=[2])
    for q, qr, sr in [(4, [16], 15), (6, [23, 24, 25], 22)]:
        add('1', q, without_marker(col('paper', 3, qr)), [anyn(options(5, [sr], separator='/'), 2, 2)],
            'japanese-5-0', [3], [5], reading=[2])
    instruction = without_marker(col('paper', 5, [1]))
    labels = [col('paper', 5, [row]) for row in [3, 4, 5]]
    add('2A', 1, instruction + '\n' + '\n'.join(labels),
        [point(s(6, row, 2), 3, contextNote=s(6, row, 1)) for row in [3, 4, 5]],
        'japanese-5-2', [5], [6], reading=[4, 5],
        figure=crop('ja-2016-ol-2a-1', 5, [.50, .035, .97, .208], instruction))
    add('2A', 2, without_marker(col('paper', 5, [6, 7])), [anyn(options(6, [7], separator='/'), 1, 3)],
        'japanese-5-2', [5], [6], reading=[4], stem=col('paper', 5, [0]))
    for roman, qr, sr in [('i', 11, 9), ('ii', 12, 10)]:
        answer = s(6, sr).split(':', 1)[1].strip()
        question = without_marker(col('paper', 5, [9], 290)) + '\n' + clean_label(col('paper', 5, [qr]))
        add('2A', 3, question, [anyn([part.strip() for part in answer.split('/')], 1, 2)],
            'japanese-5-2', [5], [6], roman, reading=[4], stem=col('paper', 5, [0]))
    instruction = p(5, 15) + ' ' + p(5, 16)
    labels = [english(p(5, 19, 1)) + ' ' + p(5, 20), english(p(5, 22, 1)) + ' ' + p(5, 23),
              english(p(5, 25, 1)), english(p(5, 27, 1)), english(p(5, 29, 1)) + ' ' + p(5, 30)]
    labels = [re.match(r'\([ivx]+\)', p(5, row, 0)).group() + ' ' + label for row, label in zip([19, 22, 25, 27, 29], labels)]
    groups = []
    for i, (sr, quote_row) in enumerate([(12, 14), (15, 17), (18, 20), (21, 22), (23, 25)]):
        groups.append({'id': f'item-{i + 1}', 'label': labels[i], 'rows': [
            {'id': 'true-false', 'text': s(6, sr, 2), 'marks': 1},
            {'id': 'quote', 'text': re.sub(r'\s*2 marks$', '', s(6, quote_row)), 'marks': 2}]})
    add('2A', 4, instruction + '\n' + '\n'.join(labels), [], 'japanese-5-2', [5], [6], total=15, reading=[4, 5],
        rubric={'system': 'language-points', 'count': 5, 'taskRequirements': [instruction], 'groups': groups, 'markingGuideNote': cell('scheme', 6, 11)},
        figure=crop('ja-2016-ol-2a-4', 5, [.075, .46, .97, .956], instruction))
    discrepancy = ('The original scheme prints おもしいです。 for (ii), visibly omitting ろ from the adjective in the paper prompt. '
                   'The published answer is retained literally here; this spelling discrepancy is not a changed question or an additional marking condition.')
    for q, instruction_row, example, lr, answers, region in [
        (1, 2, 3, range(4, 9), [s(7, 2, 1), s(7, 3).split('。 ')[1], s(7, 4).split('。')[1] + '。', s(7, 5, 1), s(7, 6, 1)], [.075, .03, .97, .42]),
        (2, 10, 11, range(12, 17), [s(7, row, 1) + ' ' + s(7, row, 2) if row < 11 else s(7, row, 1) for row in range(8, 13)], [.075, .46, .97, .80])]:
        instruction = p(6, instruction_row)
        labels = [p(6, row) for row in lr]
        rubric = pool(5, labels, answers, 2, instruction, cell('scheme', 7, 1 if q == 1 else 7))
        if q == 1:
            rubric['markingGuideNote'] += ' — ' + discrepancy
        add('2B', q, instruction + '\n' + p(6, example) + '\n' + '\n'.join(labels), [], 'japanese-5-5', [6], [7], total=10, reading=[6],
            rubric=rubric, figure=crop(f'ja-2016-ol-2b-{q}', 6, region, instruction))
    instruction = p(7, 15)
    first_options = re.sub(r'\s+\(b\)', ' ' + p(7, 18) + ' (b)', p(7, 17, 2))
    first_label = p(7, 17, 0) + ' ' + p(7, 17, 1) + ' ' + first_options + ' ' + p(7, 17, 3)
    labels = [first_label] + [p(7, row) for row in range(19, 25)] + [p(7, 26) + ' ' + p(7, 25)] + [p(7, row) for row in [27, 28]]
    answers = [s(7, row, 2 if row in [15, 16] else 1) for row in range(14, 24)]
    add('2C', None, instruction + '\n' + p(7, 16) + '\n' + '\n'.join(labels), [], 'japanese-5-4', [7], [7], total=10, reading=[7],
        rubric=pool(10, labels, answers, 1, instruction, cell('scheme', 7, 13)),
        figure=crop('ja-2016-ol-2c', 7, [.07, .53, .97, .96], instruction))
    add('3A', 1, without_marker(col('paper', 9, [1])), [point(s(8, 2), 2)], 'japanese-5-2', [9], [8], reading=[8], stem=p(9, 0, 1))
    for roman, qr, sr, count, marks in [('i', [3, 4], 4, 2, 2), ('ii', [7, 8], 7, 1, 2)]:
        question = re.sub(r'^(?:2\.\s*)?\([ivx]+\)\s*', '', col('paper', 9, qr))
        add('3A', 2, question, [anyn(options(8, [sr], separator='/'), count, marks)], 'japanese-5-2', [9], [8], roman, reading=[8], stem=p(9, 0, 1))
    for roman, qr, sr in [('i', range(12, 17), 10), ('ii', range(17, 23), 12), ('iii', range(23, 29), 14)]:
        add('3A', 3, without_marker(col('paper', 9, qr)), [point(s(8, sr), 3)], 'japanese-5-2', [9], [8], roman,
            reading=[8], stem=without_marker(col('paper', 9, [10, 11], 290)))
    for roman, qr, sr in [('i', 30, 17), ('ii', 32, 19), ('iii', 34, 21)]:
        card = add('3A', 4, without_marker(p(9, qr)), [point(s(8, sr), 3)], 'japanese-5-2', [9], [8], roman,
                   reading=[8], stem=english(p(9, 29, 1)))
        if roman == 'iii':
            cell('scheme', 8, 20)
            card['rows'][0]['contextNote'] = 'The scheme repeats (ii) for this third Japanese prompt. The paper prints (iii); the complete question wording establishes this binding.'
    instruction = p(10, 6)
    allocation = s(8, 24)
    content, discretionary = allocation.split(', ')
    parts = [{'id': 'point', 'verbatim': content, 'marks': 2, 'permittedMarks': [0, 2]},
             {'id': 'discretionary', 'verbatim': discretionary, 'marks': 1, 'permittedMarks': [0, 1]}]
    add('3B', None, instruction, [{'kind': 'criterion', 'verbatim': UNPRINTED, 'unprinted': True, 'marks': 3,
        'permittedMarks': [0, 1, 2, 3], 'parts': parts, 'contextNote': allocation}],
        'japanese-5-6', [10], [8], stem=p(10, 2) + ' ' + p(10, 3))


def writing():
    instruction = p(11, 4) + ' ' + p(11, 5)
    question = instruction + '\n' + '\n'.join(p(11, row) for row in range(6, 19))
    labels = [re.match(r'\([ivx]+\)', s(9, row)).group() for row in range(2, 12)]
    answers = [s(9, row, 1) if row != 9 else sa(9, row) for row in range(2, 12)]
    add('4', None, question, [], 'japanese-5-7', [11], [9],
        rubric=pool(10, labels, answers, 3, instruction, cell('scheme', 9, 1)), total=30,
        reading=[11], figure=crop('ja-2016-ol-4', 11, [.05, .045, .97, .95], instruction))
    instruction = p(12, 3) + ' ' + p(12, 4)
    labels = [p(12, row) for row in range(5, 12)]
    content_bands = [{'label': s(9, row), 'marks': marks, 'guidance': [s(9, row, 1)]}
                     for row, marks in [(25, [1]), (24, [2, 3]), (23, [4, 5])]]
    expression_bands = [{'label': s(10, first), 'marks': marks,
                         'guidance': [s(10, first, 1) + ' ' + ' '.join(s(10, row) for row in rest)]}
                        for first, rest, marks in [(10, range(11, 17), [1]), (17, range(18, 24), [2, 3]), (24, range(25, 31), [4, 5])]]
    cap = joined_selector('scheme', 9, [(27, 0), (28, 0)])
    groups = []
    for i, label in enumerate(labels, 1):
        criteria = [{'id': f'item-{i}-content', 'label': s(9, 22).removesuffix(':'), 'maxMarks': 5,
                     'permittedMarks': list(range(6)), 'guidance': [s(9, 14)], 'bands': content_bands},
                    {'id': f'item-{i}-expression', 'label': s(9, 26).removesuffix(':'), 'maxMarks': 5,
                     'permittedMarks': list(range(6)), 'guidance': [cap], 'bands': expression_bands,
                     'limits': [{'id': f'item-{i}-low-content', 'maxMarks': 3,
                                 'when': {'any': [{'criterionIds': [f'item-{i}-content'], 'atMost': 3}]}, 'guidance': [cap]}]}]
        groups.append({'id': f'item-{i}', 'label': label, 'rows': [], 'criteria': criteria})
    rubric = {'system': 'language-points', 'count': 5, 'taskRequirements': [instruction], 'groups': groups,
              'markingGuideNote': s(9, 13) + ' ' + s(9, 14) + ' ' + cap + ' ' + s(10, 31) + ' ' + s(10, 32)}
    add('5', None, instruction + '\n' + '\n'.join(labels), [], 'japanese-5-7', [12], [9, 10], rubric=rubric, total=50,
        reading=[12], figure=crop('ja-2016-ol-5', 12, [.05, .035, .97, .977], instruction))


def listening():
    def listen(section, q, roman, qr, answers):
        page = {'A': 2, 'B': 3, 'C': 4, 'D': 5}[section]
        topic = 'japanese-6-1' if section == 'A' else 'japanese-6-2' if section == 'C' else 'japanese-6-0'
        question = re.sub(r'^(?:\d+\.?\s*)?(?:\([ivx]+\)\s*)?', '', col('aural', page, qr, 300)).strip()
        card = add('L' + section, q, question, answers, topic, [page], [3 if section in 'AB' else 4], roman, reading=[page])
        card['stem'] = col('aural', page, range(1, 8 if section in 'BC' else 7))
        if section in 'BC':
            header = {'B': {1: 8, 2: 30}, 'C': {1: 8, 2: 21, 3: 28}}[section][q]
            card['stem'] += '\n' + col('aural', page, [header])
        return card
    car = s(3, 3, 2)
    first, second = car.split('(1 mark)', 1)
    second = second.removesuffix('(1 mark)').strip()
    listen('A', 1, 'i', [7], [point(first.strip(), 1), anyn([part.strip() for part in second.split('/')], 1, 1)])
    for q, roman, qr, sr, sg in [(1, 'ii', range(9, 14), 5, 1), (1, 'iii', range(14, 20), 6, 1),
        (2, 'ii', range(22, 27), 8, 1), (2, 'iii', range(27, 32), 9, 1),
        (3, 'i', range(32, 37), 10, 2), (3, 'ii', range(37, 42), 11, 1)]:
        listen('A', q, roman, qr, [point(s(3, sr, sg), 4)])
    listen('A', 2, 'i', [20], [anyn(options(3, [7], 2, '/'), 1, 2)])
    for q, roman, qr, sr in [(1, 'i', range(9, 15), 14), (1, 'ii', range(15, 20), 15),
        (1, 'iii', range(20, 25), 16), (1, 'iv', range(25, 30), 17), (2, 'i', range(31, 36), 19), (2, 'ii', range(36, 41), 20)]:
        listen('B', q, roman, qr, [point(s(3, sr, 1), 4)])
    listen('C', 1, 'i', range(9, 14), [point(s(4, 2, 1), 4)])
    listen('C', 1, 'ii', range(14, 19), [point(s(4, 3, 1), 4)])
    phone_source = cell('scheme', 4, 4, 1)
    number = re.search(r'\d{4}–\d{3}–\d{3}', phone_source).group()
    digits = number.replace('–', '')
    rows = [point(digits[position - 1], contextNote=f'Missing digit {index + 1} (position {position} in {number}). {phone_source} — Only the four missing digits score; the printed digits are given.')
            for index, position in enumerate([2, 6, 7, 8])]
    phone = listen('C', 1, 'iii', [19], rows)
    phone['questionFigureKey'] = crop('ja-2016-ol-lc-1-iii', 4, [.53, .46, .97, .535], phone['questionText'], 'aural')
    listen('C', 2, '', range(22, 28), [point(s(4, 6, 1), 4)])
    for roman, qr, sr in [('i', 31, 10), ('ii', 33, 12)]:
        card = listen('C', 3, roman, [29, 30, qr], [anyn(options(4, [sr], separator='/'), 1, 4)])
        card['rows'][0]['contextNote'] = 'The scheme gives 4 marks for this weather response and lists these alternatives; no separate per-detail allocation is printed.'
    for q, qr, sr in [(1, range(7, 12), 14), (2, [12], 15), (3, range(14, 20), 16),
                      (4, range(20, 26), 17), (5, range(26, 31), 18), (6, range(31, 37), 19)]:
        listen('D', q, '', qr, [point(re.sub(r'^\d+\.\s*', '', s(4, sr)), 4)])


def build():
    reading()
    writing()
    listening()
    census = json.loads((Path(__file__).parent / 'reviews/japanese-2016-ol-census.json').read_text())
    expected = {'ja-2016-ol-' + '-'.join(str(part).lower() for part in task['key'] if part is not None): task for task in census['tasks']}
    assert set(expected) == {card['id'] for card in CARDS}
    def nonempty_guidance(value):
        if isinstance(value, dict):
            for key, child in value.items():
                if key == 'guidance':
                    assert child and all(isinstance(text, str) and text.strip() for text in child), value
                nonempty_guidance(child)
        elif isinstance(value, list):
            for child in value: nonempty_guidance(child)
    for card in CARDS:
        task = expected[card['id']]
        assert card['questionText'].strip()
        assert card['totalMarks'] == task['marks'], (card['id'], card['totalMarks'], task['marks'])
        assert card['sourceEvidence']['paperPages'] == task['paperPages']
        assert card['sourceEvidence']['schemePages'] == task['schemePages']
        nonempty_guidance(card)
    assert len(CARDS) == 52
    assert sum(card['totalMarks'] for card in CARDS) == 300
    assert sum('answerLanguageRule' in card for card in CARDS) == 50
    assert not any(card['id'] in ORIGINAL_IDS for card in CARDS)
    return {'subjectId': 'japanese', 'sitting': '2016-ol', 'reviewedAt': '2026-11-09',
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
        (ROOT / 'scripts/markbank/authoring/reviews/japanese-2016-ol.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
        manifest = ROOT / 'components/MarkBank/figures-japanese.json'
        previous = json.loads(manifest.read_text())
        previous.update(FIGURES)
        manifest.write_text(json.dumps(previous, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'cards': len(CARDS), 'marks': sum(card['totalMarks'] for card in CARDS), 'figures': len(FIGURES)}, indent=2))
