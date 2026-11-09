#!/usr/bin/env python3
"""Publish the independently censused 2026 Ordinary sitting from PDF selectors.

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
    'paper': ROOT / 'examiner-reports/japanese/papers/2026-ol-000-paper.pdf',
    'aural': ROOT / 'examiner-reports/japanese/papers/2026-ol-A00-paper.pdf',
    'scheme': ROOT / 'examiner-reports/japanese/schemes/2026-ol.pdf',
}
HASHES = {
    'paper': '3e426ef7ef17020d89b812e13eabaf47efb18d3b0b97e6dd4810d966551634b7',
    'aural': '19c7f71b7308c47f20207f7f90845456ea9c445e5e64e6ba1e72f56a878181d1',
    'scheme': '1781dbc10f0f34043655b1ee9a093f368726a8caa5203dad214d0c63051321cc',
}
for name, path in PATHS.items():
    assert hashlib.sha256(path.read_bytes()).hexdigest() == HASHES[name], path
DOCS = {name: fitz.open(path) for name, path in PATHS.items()}
ROWS = {name: [page_rows(page) for page in doc] for name, doc in DOCS.items()}
CARDS, EVIDENCE, FIGURES = [], [], {}
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
    return {'kind': 'source-text', 'label': '2026 Japanese Ordinary Level', 'title': 'Original examination material',
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
    cid = f'ja-2026-ol-{section.lower()}' + (f'-{q}' if q is not None else '') + (f'-{suffix}' if suffix else '')
    ref = f'2026 OL Section {section}' + (f' Q{q}' if q is not None else '') + ''.join(f'({part})' for part in suffix.split('-') if part)
    listening = section.startswith('L')
    convention = cell('scheme', 3, 12, 1)
    card = {'id': cid, 'source': 'sec', 'subjectId': 'japanese', 'specVersion': 'lc-japanese-syllabus',
            'kind': 'rubric' if rubric else 'question', 'level': 'ordinary', 'year': 2026,
            'section': section[1:] if listening else section[0] if section[0] in '1234' else 'Q5',
            'topicId': topic, 'conceptId': concept_for(question, cid), 'questionRef': ref,
            'questionText': question, 'totalMarks': total if total is not None else sum(map(worth, rows)),
            'qa': {'gates': ['verbatim', 'tariff', 'figure'], 'humanReviewedBy': 'agent-verified', 'humanReviewedAt': '2026-11-06'},
            'sourceEvidence': {'component': 'aural' if listening else 'paper', 'paperPages': pp, 'schemePages': sp, 'generalSchemePages': [3]},
            'answerLanguageRule': {'otherLanguageMultiplier': 0.5, 'sourceText': convention, 'schemePages': [3]},
            'schemeCitation': 'Marking points quoted from the SEC marking scheme, Japanese 2026 Ordinary Level — © State Examinations Commission.'}
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


def reading():
    instruction = p(3, 0, 3) + ' ' + p(3, 1, 1)
    items = [p(3, r, 3) + ' ' + p(3, r, 4) for r in range(3, 8)]
    matching = [point(s(6, row, group), 2, contextNote=item) for (row, group), item in zip([(3, 2), (4, 1), (5, 2), (6, 2), (7, 2)], items)]
    add('1', 1, instruction + '\n' + '\n'.join(items), matching, 'japanese-5-0', [3], [6], reading=[2, 3])
    add('1', 2, p(3, 9, 3), [anyn([s(6, r) for r in range(9, 15)], 3)], 'japanese-5-0', [3], [6], reading=[2])
    add('1', 3, p(3, 11, 3), [anyn([s(6, r) for r in range(17, 20)], 2, 2, [2, 1])], 'japanese-5-0', [3], [6], reading=[2])
    for suffix, row, answers in [('a', 15, [s(6, 22, 2), s(6, 23), s(6, 24)]), ('b', 16, [s(6, 26, 1).split(': - ', 1)[1], s(6, 27), s(6, 28)])]:
        question = p(3, 14, 3) + ' ' + re.sub(r'_+', '', p(3, row, 3)).strip()
        add('1', 4, question, [anyn(answers, 1)], 'japanese-5-0', [3], [6], suffix, reading=[2])
    add('1', 5, p(3, 17, 3), [anyn([s(6, r) for r in range(31, 35)], 2)], 'japanese-5-0', [3], [6], reading=[2])
    add('1', 6, p(3, 19, 4) + ' ' + p(3, 20, 1), [point(s(7, 1), 2)], 'japanese-5-0', [3], [7], 'a', reading=[2])
    add('1', 6, without_marker(p(3, 22, 2)) + ' ' + p(3, 23, 1), [anyn([s(7, r) for r in range(3, 6)], 2, 2, [2, 1])], 'japanese-5-0', [3], [7], 'b', reading=[2])
    question = p(3, 25, 4)
    table = [point(s(7, 11, 1), 2, contextNote=s(7, 8, 1)), anyn([s(7, 8, 2), s(7, 9)], 1, contextNote=s(7, 11, 2)), point(s(7, 11, 3), 2, contextNote=s(7, 8, 3))]
    add('1', 6, question, table, 'japanese-5-0', [3], [7], 'c', reading=[2, 3], figure=crop('ja-2026-ol-1-6-c', 3, [.07, .72, .94, .90], question))

    questions = [p(5, 1, 3) + ' ' + p(5, 2, 1), without_marker(p(5, 5, 2)), p(5, 7, 3), p(5, 10, 3) + ' ' + p(5, 11, 1), without_marker(p(5, 13, 2)), p(5, 15, 3) + ' ' + p(5, 16, 1)]
    for q, rows in [(1, [point(s(7, 15), 2)]), (2, [point(s(7, 17)), point(s(7, 18))]), (3, [point(s(7, 20)), point(s(7, 21))]), (4, [point(s(7, 23)), point(s(7, 24))]), (6, [anyn([s(7, r) for r in range(31, 34)], 2, 2)])]:
        add('2A', q, questions[q - 1], rows, 'japanese-5-2', [5], [7], reading=[4], stem=p(5, 0, 3))
    contents, interesting = s(7, 26).removeprefix('-').split(' (1 mark) ', 1)
    interesting = re.sub(r'\s*\(2 marks\)$', '', interesting)
    groups = [{'id': 'contents', 'label': contents, 'rows': [{'id': 'contents', 'text': contents, 'marks': 1}, {'id': 'interesting', 'text': interesting, 'marks': 2}]}]
    for i, row in enumerate([27, 28]):
        groups.append({'id': f'alternative-{i + 1}', 'label': s(7, row), 'rows': [{'id': 'answer', 'text': s(7, row), 'marks': 3}]})
    rubric = {'system': 'language-points', 'count': 1, 'taskRequirements': [questions[4]], 'groups': groups, 'markingGuideNote': cell('scheme', 7, 29)}
    add('2A', 5, questions[4], [], 'japanese-5-2', [5], [7], rubric=rubric, total=3, reading=[4], stem=p(5, 0, 3))

    instruction = p(5, 20) + ' ' + p(5, 21)
    labels = [english(p(5, row, group)) for row, group in [(24, 1), (27, 0), (29, 1), (31, 1), (34, 0), (37, 0)]]
    groups = []
    for i, (truth, quote) in enumerate([(1, [2]), (3, [4]), (5, [6, 7]), (8, [9]), (10, [11]), (12, [13])]):
        quoted = re.sub(r'\s*\(2\s*marks\)\s*$', '', ' '.join(cell('scheme', 8, row, 0) for row in quote)).removeprefix('→').strip()
        groups.append({'id': f'item-{i + 1}', 'label': labels[i], 'rows': [{'id': 'true-false', 'text': s(8, truth, 2), 'marks': 1}, {'id': 'quote', 'text': quoted, 'marks': 2}]})
    add('2B', None, instruction + '\n' + '\n'.join(labels), [], 'japanese-5-2', [5], [8], rubric={'system': 'language-points', 'count': 5, 'taskRequirements': [instruction], 'groups': groups, 'markingGuideNote': cell('scheme', 8, 0)}, total=15, reading=[4, 5], figure=crop('ja-2026-ol-2b', 5, [.07, .46, .94, .94], instruction))
    instruction = p(6, 17)
    labels = [p(6, row) for row in range(19, 32)]
    add('2C', None, instruction + '\n' + '\n'.join(labels), [], 'japanese-5-4', [6], [8], rubric=pool(10, labels, [s(8, row, 1) for row in range(15, 28)], 1, instruction, cell('scheme', 8, 14)), total=10, reading=[6], figure=crop('ja-2026-ol-2c', 6, [.06, .518, .95, .93], instruction))
    question = p(7, 6) + ' ' + p(7, 7)
    allocation = cell('scheme', 8, 30)
    point_label = re.search(r'\bpoints\b', allocation).group()
    parts = [{'id': f'point-{i}', 'verbatim': f'{i}. {point_label}', 'marks': 2, 'permittedMarks': [0, 2]} for i in [1, 2]]
    add('2D', None, question, [{'kind': 'criterion', 'verbatim': UNPRINTED, 'unprinted': True, 'marks': 4, 'permittedMarks': [0, 2, 4], 'parts': parts, 'contextNote': allocation}], 'japanese-5-6', [7], [8], stem=p(7, 2) + ' ' + p(7, 3))

    for q, question, rows in [(1, without_marker(p(9, 1, 1)), [point(s(9, 4), 2)]), (2, without_marker(p(9, 3, 1)) + ' ' + p(9, 4, 1), [anyn([s(9, r) for r in range(6, 9)], 2, 2)]), (3, without_marker(p(9, 6, 1)), [point(s(9, 11), 2)])]:
        add('3A', q, question, rows, 'japanese-5-2', [9], [9], reading=[8], stem=without_marker(p(9, 0, 2)).removeprefix('A. '))
    for letter, qr, sr in [('a', [10, 11, 12, 14, 16, 17], 13), ('b', range(18, 23), 15), ('c', range(23, 28), 17), ('d', range(28, 33), 19)]:
        add('3A', 4, without_marker(col('paper', 9, qr)), [point(s(9, sr), 3)], 'japanese-5-2', [9], [9], letter, reading=[8], stem=without_marker(p(9, 8, 1)) + ' ' + p(9, 9, 1))
    instruction = english(p(10, 0, 1))
    labels = [p(10, row) for row in [1, 3, 5, 7]]
    add('3A', 5, instruction + '\n' + '\n'.join(labels), [], 'japanese-5-2', [10], [9], rubric=pool(3, labels, [s(9, row) for row in [22, 24, 26, 28]], 2, instruction, cell('scheme', 9, 20)), total=6, reading=[8])
    for q, page, instr, items, answerrows, region in [(1, 10, 11, range(13, 19), range(2, 8), [.07, .40, .95, .83]), (2, 11, 1, range(3, 9), range(9, 15), [.07, .04, .95, .48])]:
        instruction = english(p(page, instr))
        labels = [p(page, row) for row in items]
        add('3B', q, instruction + '\n' + '\n'.join(labels), [], 'japanese-5-5', [page], [10], rubric=pool(5, labels, [s(10, row, 1) for row in answerrows], 2, instruction, cell('scheme', 10, 1 if q == 1 else 8)), total=10, reading=[page], figure=crop(f'ja-2026-ol-3b-{q}', page, region, instruction))


def writing():
    instruction = p(12, 3) + ' ' + p(12, 4)
    question = instruction + '\n' + '\n'.join(p(12, row) for row in range(5, 20))
    labels = [s(11, row, 0) for row in range(2, 14)]
    add('4', None, question, [], 'japanese-5-7', [12], [11], rubric=pool(10, labels, [s(11, row, 1) for row in range(2, 14)], 3, instruction, cell('scheme', 11, 1)), total=30, reading=[12], figure=crop('ja-2026-ol-4', 12, [.07, .055, .95, .94], instruction))
    instruction = english(p(13, 2)) + ' ' + p(13, 3)
    labels = [p(13, row, 1) for row in range(4, 12)]
    content_bands = [{'label': s(11, row), 'marks': marks, 'guidance': [s(11, row, 1)]} for row, marks in [(28, [1]), (27, [2, 3]), (26, [4, 5])]]
    expression_bands = [{'label': s(12, first), 'marks': marks, 'guidance': [s(12, first, 1) + ' ' + ' '.join(s(12, row) for row in rest)]} for first, rest, marks in [(10, range(11, 17), [1]), (17, range(18, 25), [2, 3]), (25, range(26, 31), [4, 5])]]
    groups = []
    for i, label in enumerate(labels, 1):
        criteria = [{'id': f'item-{i}-content', 'label': s(11, 25).removesuffix(':'), 'maxMarks': 5, 'permittedMarks': list(range(6)), 'guidance': [s(11, 16)], 'bands': content_bands},
                    {'id': f'item-{i}-expression', 'label': s(12, 0).removesuffix(':'), 'maxMarks': 5, 'permittedMarks': list(range(6)), 'guidance': [s(12, 1)], 'bands': expression_bands}]
        groups.append({'id': f'item-{i}', 'label': label, 'rows': [], 'criteria': criteria})
    rubric = {'system': 'language-points', 'count': 5, 'taskRequirements': [instruction], 'groups': groups, 'markingGuideNote': s(11, 15) + ' ' + s(11, 16) + ' ' + s(12, 31) + ' ' + s(12, 32)}
    add('5', None, instruction + '\n' + '\n'.join(f'{i}. {label}' for i, label in enumerate(labels, 1)), [], 'japanese-5-7', [13], [11, 12], rubric=rubric, total=50, reading=[13], figure=crop('ja-2026-ol-5', 13, [.06, .04, .96, .92], instruction))


def listening():
    def listen(section, q, roman, rows, answers, *, figure=None):
        page = {'A': 2, 'B': 3, 'C': 4, 'D': 5}[section]
        question = without_marker(col('aural', page, rows, 290))
        topic = {'A': 'japanese-6-1', 'B': 'japanese-6-0', 'C': 'japanese-6-2', 'D': 'japanese-6-1'}[section]
        card = add('L' + section, q, question, answers, topic, [page], [4 if section in 'AB' else 5], roman or '', reading=[page], figure=figure)
        scene = {'A': {1: (5, 3), 2: (16, 3), 3: (28, 3)}, 'B': {1: (4, 3), 2: (15, 3), 3: (24, 3)}, 'C': {1: (5, 2), 2: (30, 3)}}
        if section in scene:
            r, g = scene[section][q]
            card['stem'] = cell('aural', page, r, g)
        else:
            card['stem'] = col('aural', page, [1, 2])
        return card

    listen('A', 1, 'i', range(6, 11), [point(s(4, 3, 2), 4)])
    listen('A', 1, 'ii', range(11, 16), [point(sa(4, 4), 4)])
    listen('A', 2, 'i', [17], [point(s(4, 5, 2), 2)])
    listen('A', 2, 'ii', [19, 21, 22, 23, 24], [point(sa(4, 6), 4)])
    listen('A', 2, 'iii', [25, 26], [anyn([sa(4, 7), *[s(4, r) for r in range(8, 11)]], 1, 2)])
    listen('A', 3, 'i', [29], [point(s(4, 12, 2), 2)])
    listen('A', 3, 'ii', range(31, 36), [point(sa(4, 13), 4)])
    listen('A', 3, 'iii', range(36, 41), [point(sa(4, 14), 4)])
    listen('B', 1, 'i', range(5, 10), [point(sa(4, 17), 4)])
    listen('B', 1, 'ii', range(10, 15), [point(sa(4, 18), 4)])
    listen('B', 2, 'i', range(16, 21), [point(sa(4, 20), 4)])
    listen('B', 2, 'ii', [21, 22], [anyn([sa(4, 21), *[s(4, r) for r in range(22, 25)]], 1, 2)])
    phone_question = col('aural', 3, [25])
    listen('B', 3, 'i', [25], [point(s(4, 27, 1), 4)], figure=crop('ja-2026-ol-lb-3-i', 3, [.07, .608, .94, .68], phone_question, 'aural'))
    listen('B', 3, 'ii', [27, 29, 30, 31, 32], [point(sa(4, 28), 4)])
    listen('B', 3, 'iii', range(33, 38), [point(sa(4, 29), 4)])
    listen('C', 1, 'i', [7, 8], [point(sa(5, 2), 2)])
    listen('C', 1, 'ii', [10, 11, 13, 14, 15, 16], [point(sa(5, 3), 4)])
    listen('C', 1, 'iii', range(17, 23), [point(sa(5, 4), 4)])
    listen('C', 1, 'iv', [23], [point(sa(5, 5), 2)])
    listen('C', 1, 'v', range(25, 30), [point(sa(5, 6), 4)])
    weather = []
    for first, rest in [(8, range(9, 12)), (13, range(14, 16))]:
        label, answer = sa(5, first).split(':', 1)
        weather.append(anyn([answer.strip().removeprefix('-').strip(), *[s(5, r) for r in rest]], 1, 2, contextNote=label))
    card = listen('C', 2, 'i', [31, 32], weather)
    card['questionText'] += '\n' + '\n'.join(re.sub(r'_+', '', cell('aural', 4, row)).strip() for row in [33, 34])
    listen('C', 2, 'ii', range(35, 41), [point(sa(5, 17), 4)])
    for q, qr, answers in [(1, [5, 7, 8, 9, 10], [point(s(5, 19, 1), 4)]), (2, [11, 13, 14, 15, 16], [point(s(5, 20, 1), 4)]), (3, [17], [anyn([s(5, 21, 1), s(5, 22), s(5, 23)], 1, 2)]), (4, [20], [anyn([s(5, 25, 1), *[s(5, r) for r in range(26, 31)]], 1, 2)]), (5, range(22, 27), [point(s(5, 32, 1), 4)]), (6, [27, 29, 30, 31, 32], [point(s(5, 33, 1), 4)]), (7, range(33, 38), [point(s(5, 34, 1), 4)])]:
        listen('D', q, None, qr, answers)


def build():
    reading()
    writing()
    listening()
    assert len(CARDS) == 59, len(CARDS)
    assert sum(card['totalMarks'] for card in CARDS) == 300
    assert all(card['questionText'].strip() for card in CARDS)
    return {'subjectId': 'japanese', 'sitting': '2026-ol', 'reviewedAt': '2026-11-06',
            'sources': [{'document': name, 'path': str(path.relative_to(ROOT)), 'sha256': HASHES[name], 'pagesReviewed': list(range(1, len(DOCS[name]) + 1))} for name, path in PATHS.items()],
            'cards': CARDS, 'selectors': EVIDENCE, 'status': 'source-reviewed-browser-qa-pending',
            'choiceAnalysis': {'2B': 'any5of6-truth-and-quote-onecard', '2C': 'any10of13-kanji-onecard', '3A5': 'any3of4-onecard', '3B1': 'any5of6-onecard', '3B2': 'any5of6-onecard', '4': 'any10of12-cloze-onecard', '5': 'any5of8-independent-content5-expression5-onecard'}}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    result = build()
    if args.write:
        (ROOT / 'scripts/markbank/authoring/reviews/japanese-2026-ol.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
        PATHS['scheme'].with_suffix('.md').write_text(''.join(f'\n## Page {page}\n\n' + '\n'.join(' '.join(group[2] for group in row) for row in rows) + '\n' for page, rows in enumerate(ROWS['scheme'], 1)))
        path = ROOT / 'components/MarkBank/figures-japanese.json'
        previous = json.loads(path.read_text())
        previous.update(FIGURES)
        path.write_text(json.dumps(previous, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'cards': len(CARDS), 'marks': sum(card['totalMarks'] for card in CARDS), 'figures': len(FIGURES)}, indent=2))
