#!/usr/bin/env python3
"""Publish the independently censused 2024 Ordinary sitting from PDF selectors.

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
    'paper': ROOT / 'examiner-reports/japanese/papers/2024-ol-000-paper.pdf',
    'aural': ROOT / 'examiner-reports/japanese/papers/2024-ol-A00-paper.pdf',
    'scheme': ROOT / 'examiner-reports/japanese/schemes/2024-ol.pdf',
}
HASHES = {
    'paper': '4b98a657a87bff55e83fe8419ed2d9f0926738f2bab6820c976637a0bde1b14e',
    'aural': '466dda0e3f2d8e38475be8c3fd9d636db7d7490e80f99187ab9659d274750abc',
    'scheme': '998990bd6cfdec27155f064a23766c1797503ac9afa11ccfa273fa2783d1dfea',
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
    return {'kind': 'source-text', 'label': '2024 Japanese Ordinary Level', 'title': 'Original examination material',
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
    cid = f'ja-2024-ol-{section.lower()}' + (f'-{q}' if q is not None else '') + (f'-{suffix}' if suffix else '')
    ref = f'2024 OL Section {section}' + (f' Q{q}' if q is not None else '') + ''.join(f'({part})' for part in suffix.split('-') if part)
    listening = section.startswith('L')
    card = {'id': cid, 'source': 'sec', 'subjectId': 'japanese', 'specVersion': 'lc-japanese-syllabus',
            'kind': 'rubric' if rubric else 'question', 'level': 'ordinary', 'year': 2024,
            'section': section[1:] if listening else section[0] if section[0] in '1234' else 'Q5',
            'topicId': topic, 'conceptId': concept_for(question, cid), 'questionRef': ref,
            'questionText': question, 'totalMarks': total if total is not None else sum(map(worth, rows)),
            'qa': {'gates': ['verbatim', 'tariff', 'figure'], 'humanReviewedBy': 'agent-verified', 'humanReviewedAt': '2026-11-09'},
            'sourceEvidence': {'component': 'aural' if listening else 'paper', 'paperPages': pp, 'schemePages': sp},
            'schemeCitation': 'Marking points quoted from the SEC marking scheme, Japanese 2024 Ordinary Level — © State Examinations Commission.'}
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
    add('1', 1, instruction + '\n' + example + '\n' + '\n'.join(labels),
        [point(s(5, row, 2), 2, contextNote=label) for row, label in zip(range(4, 9), labels)],
        'japanese-5-0', [3], [5], reading=[2, 3])
    for q, qr, answers in [
        (2, [10], [anyn(options(5, [10], separator='/'), 3)]),
        (3, [18], [point(s(5, 13), 2)]),
        (4, [22], [anyn(options(5, [15]), 2, 2, [2, 1])]),
        (5, [28], [anyn(options(5, [17], separator='/'), 2, 2, [2, 1])]),
        (7, [47, 49], [anyn(options(5, [25], separator='/'), 2, 2, [2, 1])]),
    ]:
        add('1', q, without_marker(col('paper', 3, qr)), answers, 'japanese-5-0', [3], [5], reading=[2], stem=p(3, 8))
    question = without_marker(col('paper', 3, [32, 33])) + '\n' + '\n'.join(col('paper', 3, [row]) for row in [35, 36, 38, 40, 42, 44])
    membership = [point(s(5, 20, 2), 2, contextNote=s(5, 19, 2) + ' — ' + s(5, 20, 0)),
                  point(s(5, 22, 1), 2, contextNote=s(5, 19, 1) + ' — ' + s(5, 22, 0)),
                  point(s(5, 22, 2), 2, contextNote=s(5, 19, 2) + ' — ' + s(5, 22, 0))]
    add('1', 6, question, membership, 'japanese-5-0', [3], [5], reading=[2, 3], stem=p(3, 8),
        figure=crop('ja-2024-ol-1-6', 3, [.52, .62, .96, .835], question))
    for q, qr, answers in [
        (1, [1, 2], [point(s(6, 2), 2)]),
        (2, [4, 5], [anyn(options(6, [4], separator='/'), 1, 2)]),
        (3, [7, 8], [anyn(options(6, [6], separator='/'), 2, 2, [2, 1])]),
        (4, [11], [point(s(6, 9), 2)]),
        (5, [15, 17], [point(part.strip().removeprefix('to ')) for part in cell('scheme', 6, 11, 0).split('(1 mark)') if part.strip()]),
        (6, [20], [point(s(6, 13), 2)]),
    ]:
        add('2A', q, without_marker(col('paper', 5, qr)), answers, 'japanese-5-2', [5], [6], reading=[4], stem=without_marker(p(5, 0, 1)))
    instruction = english(' '.join(p(5, row) for row in range(22, 26)))
    labels = [english(p(5, row)) + ' ' + p(5, row + 1) for row in [28, 31, 34, 37, 40, 43]]
    groups = []
    for i, (truth_row, truth_group, quote_row, quote_group) in enumerate([(16, 0, 17, 0), (20, 1, 20, 0), (23, 0, 24, 0), (27, 2, 27, 0), (30, 1, 30, 0), (33, 1, 33, 0)]):
        groups.append({'id': f'item-{i + 1}', 'label': labels[i], 'rows': [
            {'id': 'true-false', 'text': s(6, truth_row, truth_group), 'marks': 1},
            {'id': 'quote', 'text': s(6, quote_row, quote_group).removeprefix('→').strip(), 'marks': 2}]})
    add('2B', None, instruction + '\n' + '\n'.join(labels), [], 'japanese-5-2', [5], [6],
        rubric={'system': 'language-points', 'count': 5, 'taskRequirements': [instruction], 'groups': groups, 'markingGuideNote': cell('scheme', 6, 14)},
        total=15, reading=[4, 5], figure=crop('ja-2024-ol-2b', 5, [.025, .475, .97, .92], instruction))
    instruction = p(6, 17)
    labels = [p(6, row) for row in range(19, 32)]
    answers = [without_marker(s(7, row, None)) for row in range(2, 15)]
    add('2C', None, instruction + '\n' + p(6, 18) + '\n' + '\n'.join(labels), [], 'japanese-5-4', [6], [7],
        rubric=pool(10, labels, answers, 1, instruction, cell('scheme', 7, 1)), total=10, reading=[6],
        figure=crop('ja-2024-ol-2c', 6, [.07, .49, .96, .89], instruction))
    question = english(p(7, 3) + ' ' + p(7, 4))
    allocation = cell('scheme', 7, 17)
    point_label = re.search(r'\bpoints\b', allocation).group()
    parts = [{'id': f'point-{i}', 'verbatim': f'{i}. {point_label}', 'marks': 2, 'permittedMarks': [0, 2]} for i in [1, 2]]
    add('2D', None, question, [{'kind': 'criterion', 'verbatim': UNPRINTED, 'unprinted': True, 'marks': 4,
        'permittedMarks': [0, 2, 4], 'parts': parts, 'contextNote': allocation}], 'japanese-5-6', [7], [7], stem=english(p(7, 1)) + ' ' + p(7, 2))
    for q, qr, answers in [(1, 1, [point(s(8, 3), 2)]), (2, 3, [anyn(options(8, [5], separator='/'), 2, 2)])]:
        add('3A', q, without_marker(col('paper', 9, [qr])), answers, 'japanese-5-1', [9], [8], reading=[8], stem=without_marker(p(9, 0, 1)))
    family_prompt = without_marker(col('paper', 9, [7]))
    for roman, label, sr in [('i', p(9, 9, 1).split('(ii)')[0], 7), ('ii', '(ii)' + p(9, 9, 1).split('(ii)')[1], 8)]:
        question = family_prompt + ' ' + re.sub(r'_+', '', label).strip()
        answer = sa(8, sr).split(':', 1)[1].strip()
        add('3A', 3, question, [anyn([part.strip() for part in answer.split('/')], 1, 2)], 'japanese-5-1', [9], [8], roman, reading=[8], stem=without_marker(p(9, 0, 1)))
    for roman, qr, sr in [('i', range(12, 18), 10), ('ii', [18, 20, 21, 22, 23], 12), ('iii', range(24, 29), 14), ('iv', [30, 32, 33, 34, 35], 16)]:
        add('3A', 4, without_marker(col('paper', 9, qr)), [point(s(8, sr), 3)], 'japanese-5-1', [9], [8], roman, reading=[8], stem=without_marker(col('paper', 9, [10, 11])))
    instruction = english(p(10, 0, 1))
    labels = [p(10, row) for row in [1, 3, 5, 7]]
    add('3A', 5, instruction + '\n' + '\n'.join(labels), [], 'japanese-5-1', [10], [8],
        rubric=pool(3, labels, [s(8, row) for row in [19, 21, 23, 25]], 2, instruction, cell('scheme', 8, 17)), total=6, reading=[8, 10])
    for q, page, instrrows, itemrows, answerrows, region in [(1, 10, [10, 11], range(13, 19), range(2, 8), [.07, .365, .96, .81]), (2, 11, [0, 1], range(3, 9), range(9, 15), [.07, .04, .96, .39])]:
        instruction = english(' '.join(p(page, row) for row in instrrows))
        labels = [p(page, row) for row in itemrows]
        answers = [without_marker(s(9, row, None)) for row in answerrows]
        add('3B', q, instruction + '\n' + '\n'.join(labels), [], 'japanese-5-5', [page], [9],
            rubric=pool(5, labels, answers, 2, instruction, cell('scheme', 9, 1 if q == 1 else 8)), total=10,
            reading=[page], figure=crop(f'ja-2024-ol-3b-{q}', page, region, instruction))


def writing():
    instruction = english(' '.join(p(12, row) for row in [2, 3, 4]))
    question = instruction + '\n' + '\n'.join(p(12, row) for row in range(5, 18))
    labels = [s(10, row, 0) for row in range(2, 14)]
    answers = [s(10, row, 1) for row in range(2, 14)]
    add('4', None, question, [], 'japanese-5-7', [12], [10], rubric=pool(10, labels, answers, 3, instruction, cell('scheme', 10, 1)), total=30,
        reading=[12], figure=crop('ja-2024-ol-4', 12, [.07, .055, .975, .815], instruction))
    instruction = english(' '.join(p(13, row) for row in [1, 2]))
    labels = [p(13, row, 1) for row in range(3, 11)]
    content_bands = [{'label': s(10, row), 'marks': marks, 'guidance': [s(10, row, 1)]} for row, marks in [(28, [1]), (27, [2, 3]), (26, [4, 5])]]
    expression_bands = [{'label': s(11, first), 'marks': marks, 'guidance': [s(11, first, 1) + ' ' + ' '.join(s(11, row) for row in rest)]} for first, rest, marks in [(12, range(13, 19), [1]), (19, range(20, 27), [2, 3]), (27, range(28, 34), [4, 5])]]
    groups = []
    for i, label in enumerate(labels, 1):
        criteria = [{'id': f'item-{i}-content', 'label': s(10, 25).removesuffix(':'), 'maxMarks': 5, 'permittedMarks': list(range(6)), 'guidance': [s(10, 16)], 'bands': content_bands},
                    {'id': f'item-{i}-expression', 'label': s(11, 0).removesuffix(':'), 'maxMarks': 5, 'permittedMarks': list(range(6)), 'guidance': [s(11, 1)], 'bands': expression_bands}]
        groups.append({'id': f'item-{i}', 'label': label, 'rows': [], 'criteria': criteria})
    rubric = {'system': 'language-points', 'count': 5, 'taskRequirements': [instruction], 'groups': groups, 'markingGuideNote': s(10, 15) + ' ' + s(10, 16) + ' ' + s(11, 34) + ' ' + s(11, 35)}
    add('5', None, instruction + '\n' + '\n'.join(p(13, row) for row in range(3, 11)), [], 'japanese-5-7', [13], [10, 11], rubric=rubric, total=50,
        reading=[13], figure=crop('ja-2024-ol-5', 13, [.05, .04, .97, .93], instruction))


def listening():
    def listen(section, q, roman, qr, answers, question=None):
        page = {'A': 2, 'B': 3, 'C': 4, 'D': 5}[section]
        question = question or without_marker(col('aural', page, qr))
        topic = {'A': 'japanese-6-1', 'B': 'japanese-6-1', 'C': 'japanese-6-2', 'D': 'japanese-6-0'}[section]
        card = add('L' + section, q, question, answers, topic, [page], [3 if section in 'AB' else 4], roman or '', reading=[page])
        card['stem'] = col('aural', page, [1, 2])
        if section != 'B':
            context = {'A': {1: 3, 2: 16, 3: 29}, 'C': {1: 3, 2: 24}, 'D': {1: 3, 2: 12, 3: 24}}[section][q]
            card['stem'] += '\n' + col('aural', page, [context])
        return card

    def la(row):
        return re.sub(r'^(?:\d+\.\s*)?\([ivx]+\)\s*', '', s(3, row))

    for q, roman, qr, sr, marks in [(1, 'i', range(4, 9), 3, 4), (1, 'ii', [9, 10, 12, 13, 14, 15], 4, 4),
                                   (2, 'i', [17], 5, 2), (2, 'ii', range(19, 24), 6, 4), (2, 'iii', range(24, 29), 7, 4),
                                   (3, 'i', range(30, 35), 8, 4), (3, 'iii', [37, 39, 41, 43, 45], 10, 4)]:
        listen('A', q, roman, qr, [point(la(sr), marks)])
    listen('A', 3, 'ii', [35], [anyn([part.strip() for part in la(9).split('/')], 1, 2)])
    for q, qr, sr, marks in [(1, range(3, 8), 12, 4), (2, range(8, 13), 13, 4), (4, [15], 15, 2),
                            (5, range(17, 24), 16, 4), (6, range(24, 29), 17, 4), (8, [32, 34, 35, 36, 37], 19, 4)]:
        listen('B', q, None, qr, [point(sa(3, sr), marks)])
    listen('B', 3, None, [13], [anyn([part.strip() for part in sa(3, 14).split('/')], 1, 2)])
    listen('B', 7, None, [29, 30], [anyn([part.strip() for part in sa(3, 18).split('/')], 1, 2)])
    for q, roman, qr, sr in [(1, 'i', range(4, 10), 2), (1, 'iii', range(13, 18), 4), (1, 'iv', range(18, 24), 5), (2, 'iii', range(30, 35), 9)]:
        listen('C', q, roman, qr, [point(sa(4, sr), 4)])
    for q, roman, qr, sr in [(1, 'ii', [10, 11], 3), (2, 'i', [25, 26], 7), (2, 'ii', [28], 8)]:
        listen('C', q, roman, qr, [anyn([part.strip() for part in sa(4, sr).split('/') if part.strip()], 1, 2)])
    listen('D', 1, 'i', [4], [point(sa(4, 12), 2)])
    listen('D', 1, 'ii', [7, 8], [anyn([part.strip() for part in sa(4, 13).split('/')], 1, 2)])
    answer = sa(4, 14)
    number = re.search(r'085-\s*2418139', answer).group()
    digits = re.sub(r'\D', '', number)
    # The source grid gives six digits; the four underlined scheme digits
    # are the independently priced blanks, in printed left-to-right order.
    parts = [{'id': f'blank-{i + 1}', 'verbatim': digits[position], 'marks': 1, 'permittedMarks': [0, 1]} for i, position in enumerate([2, 4, 7, 9])]
    phone = listen('D', 1, 'iii', [10], [{'kind': 'criterion', 'verbatim': answer, 'marks': 4,
        'permittedMarks': [0, 1, 2, 3, 4], 'parts': parts, 'contextNote': 'Missing digits from left to right; one mark for each correct number.'}])
    phone['questionFigureKey'] = crop('ja-2024-ol-ld-1-iii', 5, [.55, .295, .96, .37], phone['questionText'], 'aural')
    for q, roman, qr, sr in [(2, 'i', range(13, 18), 16), (2, 'ii', [18, 20, 21, 22, 23], 17),
                           (3, 'i', [25, 27, 29, 31, 33, 35], 19), (3, 'ii', [36, 38, 40, 42, 44], 20)]:
        listen('D', q, roman, qr, [point(sa(4, sr), 4)])


def consolidations(census):
    records = []
    romans = ['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x', 'xi', 'xii', 'xiii']
    for suffix, count, pp, pr, sp, sr, reason in [
        ('1-1', 5, 3, [0], 5, 3, 'One required five-cell matching task, two marks per cell; keep every printed item together.'),
        ('2b', 6, 5, [22, 23, 24, 25], 6, 14, 'One printed any-five-of-six truth-and-quote pool, truth1 and quote2 independently priced.'),
        ('2c', 13, 6, [17], 7, 1, 'One printed any-ten-of-thirteen meaning pool, one mark per chosen answer.'),
        ('3a-5', 4, 10, [0], 8, 17, 'One printed any-three-of-four Japanese response pool, two marks per chosen response.'),
        ('3b-1', 6, 10, [10, 11], 9, 1, 'One printed any-five-of-six negative-form pool, two marks per chosen response.'),
        ('3b-2', 6, 11, [0, 1], 9, 8, 'One printed any-five-of-six particle pool, two marks per chosen response.'),
    ]:
        canonical = 'ja-2024-ol-' + suffix
        task = next(task for task in census['tasks'] if canonical == 'ja-2024-ol-' + '-'.join(str(part).lower() for part in task['key'] if part is not None))
        records.append({'canonicalId': canonical, 'legacyIds': [canonical + '-' + part for part in romans[:count]], 'taskKey': task['key'], 'marks': task['marks'], 'reason': reason,
                        'paperEvidence': {'page': pp, 'text': joined_selector('paper', pp, [(row, None) for row in pr])}, 'schemeEvidence': {'page': sp, 'text': cell('scheme', sp, sr)}})
    return records


def build():
    reading()
    writing()
    listening()
    census = json.loads((Path(__file__).parent / 'reviews/japanese-2024-ol-census.json').read_text())
    expected = {'ja-2024-ol-' + '-'.join(str(part).lower() for part in task['key'] if part is not None): task for task in census['tasks']}
    assert set(expected) == {card['id'] for card in CARDS}
    for card in CARDS:
        task = expected[card['id']]
        assert card['totalMarks'] == task['marks'], (card['id'], card['totalMarks'], task['marks'])
        assert card['sourceEvidence']['paperPages'] == task['paperPages']
        assert card['sourceEvidence']['schemePages'] == task['schemePages']
    assert len(CARDS) == 59
    assert sum(card['totalMarks'] for card in CARDS) == 300
    return {'subjectId': 'japanese', 'sitting': '2024-ol', 'reviewedAt': '2026-11-09',
            'sources': [{'document': name, 'path': str(path.relative_to(ROOT)), 'sha256': HASHES[name], 'pagesReviewed': list(range(1, len(DOCS[name]) + 1))} for name, path in PATHS.items()],
            'cards': CARDS, 'selectors': EVIDENCE, 'status': 'source-reviewed-browser-qa-pending',
            'choiceAnalysis': census['choiceBoundaries'], 'consolidations': consolidations(census)}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    result = build()
    if args.write:
        (ROOT / 'scripts/markbank/authoring/reviews/japanese-2024-ol.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
        manifest = ROOT / 'components/MarkBank/figures-japanese.json'
        previous = json.loads(manifest.read_text())
        previous.update(FIGURES)
        manifest.write_text(json.dumps(previous, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'cards': len(CARDS), 'marks': sum(card['totalMarks'] for card in CARDS), 'figures': len(FIGURES)}, indent=2))


