#!/usr/bin/env python3
"""Publish the independently censused 2021 Ordinary sitting from PDF selectors.

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
    'paper': ROOT / 'examiner-reports/japanese/papers/2021-ol-000-paper.pdf',
    'aural': ROOT / 'examiner-reports/japanese/papers/2021-ol-A00-paper.pdf',
    'scheme': ROOT / 'examiner-reports/japanese/schemes/2021-ol.pdf',
}
HASHES = {
    'paper': '9e08378aa046efa6aa546be9a143a6ed4c42037cccc146c1638a65b91af75063',
    'aural': 'cd02fd8088e72e5f54b8eb89d238be0eec8e8252fc48ce2b5be7cfdbb2f44110',
    'scheme': 'ddc4b5bd8045f44a4a86664c7fc4c4981ed659cb1f14b83c4801cb5a4fb0b30b',
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
    return {'kind': 'source-text', 'label': '2021 Japanese Ordinary Level', 'title': 'Original examination material',
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


def continued_crop(key, clips, alt):
    """Render two original PDF regions in reading order, without rewriting them."""
    rectangles = [fitz.Rect(r[0] * DOCS['paper'][page - 1].rect.width,
                            r[1] * DOCS['paper'][page - 1].rect.height,
                            r[2] * DOCS['paper'][page - 1].rect.width,
                            r[3] * DOCS['paper'][page - 1].rect.height) for page, r in clips]
    combined = fitz.open()
    output = combined.new_page(width=max(r.width for r in rectangles), height=sum(r.height for r in rectangles) + 10)
    top = 0
    for (page, _), rect in zip(clips, rectangles):
        output.show_pdf_page(fitz.Rect(0, top, rect.width, top + rect.height), DOCS['paper'], page - 1, clip=rect)
        top += rect.height + 10
    rel = f'/exam-figures/japanese/{key}.png'
    path = ROOT / 'public' / rel.lstrip('/')
    output.get_pixmap(matrix=fitz.Matrix(2, 2)).save(path)
    FIGURES[key] = {'src': rel, 'md5': hashlib.md5(path.read_bytes()).hexdigest(), 'alt': alt,
                    'attribution': '© State Examinations Commission.',
                    'source': {'document': 'paper', 'page': clips[0][0], 'region': clips[0][1],
                               'continuations': [{'page': page, 'region': region} for page, region in clips[1:]]}}
    combined.close()
    return key


def add(section, q, question, rows, topic, pp, sp, suffix='', rubric=None, total=None, reading=None, figure=None, stem=None):
    cid = f'ja-2021-ol-{section.lower()}' + (f'-{q}' if q is not None else '') + (f'-{suffix}' if suffix else '')
    ref = f'2021 OL Section {section}' + (f' Q{q}' if q is not None else ' Q' if suffix else '') + ''.join(f'({part})' for part in suffix.split('-') if part)
    listening = section.startswith('L')
    card = {'id': cid, 'source': 'sec', 'subjectId': 'japanese', 'specVersion': 'lc-japanese-syllabus',
            'kind': 'rubric' if rubric else 'question', 'level': 'ordinary', 'year': 2021,
            'section': section[1:] if listening else section[0] if section[0] in '1234' else 'Q5',
            'topicId': topic, 'conceptId': concept_for(question, cid), 'questionRef': ref,
            'questionText': question, 'totalMarks': total if total is not None else sum(map(worth, rows)),
            'qa': {'gates': ['verbatim', 'tariff', 'figure'], 'humanReviewedBy': 'agent-verified', 'humanReviewedAt': '2026-11-09'},
            'sourceEvidence': {'component': 'aural' if listening else 'paper', 'paperPages': pp, 'schemePages': sp},
            'schemeCitation': 'Marking points quoted from the SEC marking scheme, Japanese 2021 Ordinary Level — © State Examinations Commission.'}
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
    labels = [re.sub(r'_+', '', col('paper', 3, [row])).strip() for row in range(3, 8)]
    answers = [s(5, row, 2) for row in range(4, 9)]
    add('1', 1, instruction + '\n' + p(3, 2, 2) + ' ' + p(3, 2, 3) + '\n' + '\n'.join(labels),
        [point(answer, 2, contextNote=label) for label, answer in zip(labels, answers)],
        'japanese-5-0', [3], [5], reading=[2, 3])
    for q, qr, sr, count, marks, steps in [
        (2, [9], 10, 1, 3, None), (3, [12], 12, 1, 3, None),
        (4, [14], 14, 1, 3, None), (5, [17], 16, 2, 2, [2, 1]), (6, [20], 18, 2, 2, [2, 1])]:
        add('1', q, without_marker(col('paper', 3, qr)), [anyn(options(5, [sr], separator='/'), count, marks, steps)],
            'japanese-5-0', [3], [5], reading=[2], stem=p(3, 8, 1))
    age = s(5, 20)
    lower, upper = age.split('(1 mark) to ')
    upper = upper.removesuffix('(1 mark)').strip()
    add('1', 7, without_marker(col('paper', 3, [23])), [point(lower.strip()), point(upper)],
        'japanese-5-0', [3], [5], 'i', reading=[2], stem=p(3, 8, 1))
    add('1', 7, without_marker(col('paper', 3, [27, 28])), [point(s(5, 22), 3)],
        'japanese-5-0', [3], [5], 'ii', reading=[2], stem=p(3, 8, 1))
    for q, qr, sp, rows in [
        (1, [1], 5, [point(s(5, 26), 2)]),
        (2, [3], 5, [anyn(options(5, [28], separator='/'), 2, 2, [2, 1])]),
        (3, [6], 6, [point(s(6, 1), 2)]),
        (4, [9], 6, [anyn(options(6, [3], separator='/'), 1, 2)]),
        (5, [13], 6, [anyn(options(6, [5], separator='/'), 2, 2)]),
    ]:
        add('2A', q, without_marker(col('paper', 5, qr)), rows, 'japanese-5-2', [5], [sp],
            reading=[4], stem=without_marker(col('paper', 5, [0])))
    instruction = english(' '.join(p(5, row) for row in range(15, 19)))
    labels = []
    for rows in [[23, 24], [26, 27], [29, 30], [32, 33], [35, 36], [38, 39]]:
        text = ' '.join(p(5, row) for row in rows)
        labels.append(re.match(r'\([ivx]+\)', text).group() + ' ' + english(text))
    groups = []
    for i, (tr, qr) in enumerate([(8, 10), (11, 13), (14, 16), (18, 19), (21, 23), (24, 25)], 1):
        groups.append({'id': f'item-{i}', 'label': labels[i - 1], 'rows': [
            {'id': 'true-false', 'text': s(6, tr, 2), 'marks': 1},
            {'id': 'quote', 'text': s(6, qr), 'marks': 2}]})
    add('2B', None, instruction + '\n' + '\n'.join(labels), [], 'japanese-5-2', [5], [6],
        rubric={'system': 'language-points', 'count': 5, 'taskRequirements': [instruction], 'groups': groups,
                'markingGuideNote': cell('scheme', 6, 7)}, total=15, reading=[4, 5],
        figure=crop('ja-2021-ol-2b', 5, [.075, .425, .97, .92], instruction))
    instruction = p(6, 17)
    labels = [p(6, row) for row in range(19, 27)] + [p(7, row) for row in range(5)]
    answers = [s(7, row, 1) + ' (' + s(7, row, 2) + ')' for row in range(1, 13)]
    answers.append(without_marker(s(7, 13)) + ' (' + s(7, 13, 1) + ')')
    add('2C', None, instruction + '\n' + p(6, 18) + '\n' + '\n'.join(labels), [], 'japanese-5-4', [6, 7], [7],
        rubric=pool(10, labels, answers, 1, instruction, cell('scheme', 7, 0)), total=10, reading=[6, 7],
        figure=continued_crop('ja-2021-ol-2c', [(6, [.075, .58, .97, .90]), (7, [.075, .06, .97, .22])], instruction))
    question = english(' '.join(p(7, row) for row in [8, 9, 10, 11]))
    allocation = cell('scheme', 7, 17)
    point_label = re.search(r'\bpoints\b', allocation).group()
    parts = [{'id': f'point-{i}', 'verbatim': f'{i}. {point_label}', 'marks': 2, 'permittedMarks': [0, 2]} for i in [1, 2]]
    add('2D', None, question, [{'kind': 'criterion', 'verbatim': UNPRINTED, 'unprinted': True, 'marks': 4,
        'permittedMarks': [0, 2, 4], 'parts': parts, 'contextNote': allocation}],
        'japanese-5-6', [7], [7], stem=english(' '.join(p(7, row) for row in [5, 6, 7])))
    year = s(7, 21)
    third, school = year.split('(2 marks)')
    school = school.removesuffix('(1 mark)').strip()
    for q, qr, sp, rows in [
        (1, [1], 7, [point(third.strip(), 2), point(school)]),
        (2, [3], 7, [point(s(7, 23), 3)]),
        (3, [5], 8, [anyn(options(8, [1, 2], separator='/'), 2, 2)]),
    ]:
        add('3A', q, without_marker(col('paper', 9, qr)), rows, 'japanese-5-1', [9], [sp],
            reading=[8], stem=p(9, 0, 1))
    for roman, qr, sr in [('i', range(10, 15), 5), ('ii', range(15, 20), 6),
                           ('iii', range(20, 25), 7), ('iv', range(25, 31), 8)]:
        add('3A', 4, without_marker(col('paper', 9, qr)), [point(s(8, sr, 1), 3)], 'japanese-5-1', [9], [8], roman,
            reading=[8], stem=without_marker(col('paper', 9, [8, 9])))
    instruction = english(p(10, 0, 1))
    labels = [p(10, row) for row in [1, 3, 5, 7]]
    add('3A', 5, instruction + '\n' + '\n'.join(labels), [], 'japanese-5-1', [10], [8],
        rubric=pool(3, labels, [s(8, row) for row in [12, 14, 16, 18]], 2, instruction, cell('scheme', 8, 10)),
        total=6, reading=[8, 10])
    for q, qr, lr, example, sp, sr, rr, region in [
        (1, [10, 11], range(13, 19), 12, 8, 20, range(21, 27), [.075, .345, .97, .618]),
        (2, [19, 20], range(22, 28), 21, 9, 0, range(1, 7), [.075, .619, .97, .92]),
    ]:
        instruction = english(' '.join(p(10, row) for row in qr))
        labels = [p(10, row) for row in lr]
        answers = [sa(sp, row, 0 if sp == 9 and row == 5 else 1) for row in rr]
        add('3B', q, instruction + '\n' + p(10, example) + '\n' + '\n'.join(labels), [], 'japanese-5-5', [10], [sp],
            rubric=pool(5, labels, answers, 2, instruction, cell('scheme', sp, sr)), total=10, reading=[10],
            figure=crop(f'ja-2021-ol-3b-{q}', 10, region, instruction))


def writing():
    choice = english(p(11, 1))
    instruction = english(' '.join(p(11, row) for row in [3, 4, 5]))
    question = choice + '\n' + instruction + '\n' + '\n'.join(p(11, row) for row in range(6, 21))
    labels = [s(9, row, 0) for row in range(9, 21)]
    answers = [s(9, row, 1) for row in range(9, 21)]
    add('4', None, question, [], 'japanese-5-7', [11], [9],
        rubric=pool(10, labels, answers, 4, instruction, cell('scheme', 9, 8) + ' ' + choice
                    + ' Preserve both printed scheme alternatives in(v) and(xi); the paper says to use each word once.'), total=40,
        reading=[11], figure=crop('ja-2021-ol-4', 11, [.075, .04, .97, .91], instruction))
    instruction = english(' '.join(p(12, row) for row in [1, 2, 3]))
    labels = [p(12, row) for row in range(4, 12)]
    content_bands = [{'label': s(10, row), 'marks': marks, 'guidance': [s(10, row, 1)]}
                     for row, marks in [(14, [1]), (13, [2, 3]), (12, [4])]]
    expression_bands = [{'label': s(11, first), 'marks': marks,
                         'guidance': [s(11, first, 1) + ' ' + ' '.join(s(11, row) for row in rest)]}
                        for first, rest, marks in [(1, range(2, 8), [1]), (8, range(9, 16), [2, 3]), (16, range(17, 23), [4])]]
    cap_guidance = s(10, 16) + ' ' + s(10, 17)
    groups = []
    for i, label in enumerate(labels, 1):
        criteria = [
            {'id': f'item-{i}-content', 'label': s(10, 11).removesuffix(':'), 'maxMarks': 4,
             'permittedMarks': list(range(5)), 'guidance': [s(10, 2)], 'bands': content_bands},
            {'id': f'item-{i}-expression', 'label': s(10, 15).removesuffix(':'), 'maxMarks': 4,
             'permittedMarks': list(range(5)), 'guidance': [cap_guidance], 'bands': expression_bands,
             'limits': [{'id': f'content-cap-{cap}', 'maxMarks': cap, 'guidance': [cap_guidance],
                         'when': {'any': [{'criterionIds': [f'item-{i}-content'], 'atMost': cap}]}} for cap in range(4)]},
        ]
        groups.append({'id': f'item-{i}', 'label': label, 'rows': [], 'criteria': criteria})
    rubric = {'system': 'language-points', 'count': 5, 'taskRequirements': [choice, instruction], 'groups': groups,
              'markingGuideNote': cell('scheme', 10, 1) + ' ' + s(10, 2) + ' ' + cap_guidance + ' ' + s(11, 23) + ' ' + s(11, 24)}
    add('5', None, choice + '\n' + instruction + '\n' + '\n'.join(labels), [], 'japanese-5-7', [12], [10, 11],
        rubric=rubric, total=40, reading=[12], figure=crop('ja-2021-ol-5', 12, [.05, .04, .97, .943], instruction))


def listening():
    def listen(section, q, roman, qr, answers):
        page = {'A': 2, 'B': 3, 'C': 4, 'D': 5}[section]
        topic = {'A': 'japanese-6-1', 'B': 'japanese-6-2', 'C': 'japanese-6-1', 'D': 'japanese-6-0'}[section]
        question = re.sub(r'^(?:\d+\.?\s*)?(?:\([ivx]+\)\s*)?', '', col('aural', page, qr, 300)).strip()
        card = add('L' + section, q, question, answers, topic, [page], [3 if section in 'AB' else 4], roman, reading=[page])
        if section == 'C':
            card['stem'] = 'You' + cell('aural', page, 1).split('You', 1)[1] + ' ' + col('aural', page, [2, 3, 4, 5])
        else:
            card['stem'] = col('aural', page, range(1, 5) if section == 'A' else range(1, 6) if section == 'B' else range(1, 9))
        if section == 'B':
            card['stem'] += '\n' + col('aural', page, [6 if q == 1 else 34])
        return card

    for q, roman, qr, sr, sg, marks in [
        (1, 'i', [6], 3, 2, 2), (1, 'ii', range(8, 13), 4, 1, 4),
        (1, 'iii', range(13, 18), 5, 1, 4), (2, 'i', [20], 6, 2, 2),
        (2, 'ii', range(22, 27), 7, 1, 4), (3, 'i', range(27, 32), 8, 2, 4),
        (3, 'ii', range(32, 37), 9, 1, 4),
    ]:
        listen('A', q, roman, qr, [point(s(3, sr, sg), marks)])
    listen('A', 3, 'iii', [37, 38], [anyn(options(3, [10], group=1, separator='/'), 1, 2)])
    for q, roman, qr, sr, sg in [
        (1, 'i', [7, 9, 11, 12, 13], 13, 1),
        (1, 'iii', range(18, 24), 15, 1), (1, 'v', [27, 29, 30, 31, 32], 17, 1),
        (2, 'i', range(35, 40), 19, 1), (2, 'ii', [40, 42, 43, 44, 46], 20, 0),
    ]:
        answer = s(3, sr, sg)
        if sr == 20:
            answer = without_marker(answer)
        listen('B', q, roman, qr, [point(answer, 4)])
    listen('B', 1, 'ii', [15], [anyn(options(3, [14], group=1, separator='/'), 1, 2)])
    listen('B', 1, 'iv', [24, 25], [anyn(options(3, [16], group=1, separator='/'), 1, 2)])
    for roman, qr, sr in [('i', range(6, 12), 1), ('iii', range(15, 20), 3),
                           ('iv', [20, 22, 23, 24, 26], 4), ('vi', range(30, 35), 6), ('vii', range(35, 40), 7)]:
        listen('C', None, roman, qr, [point(s(4, sr, 1), 4)])
    listen('C', None, 'ii', [12, 13], [anyn(options(4, [2], group=1, separator='/'), 1, 2)])
    phone_source = s(4, 5, 1)
    number = phone_source.split(' (')[0]
    digits = number.replace('-', '')
    rows = [point(digits[position - 1], contextNote=f'Missing digit {index + 1} (position {position} in {number}). {phone_source}')
            for index, position in enumerate([3, 5, 7, 9])]
    phone = listen('C', None, 'v', [27], rows)
    phone['questionFigureKey'] = crop('ja-2021-ol-lc-v', 4, [.52, .575, .97, .672], phone['questionText'], 'aural')
    for roman, qr, sr, sg, marks in [
        ('i', [9, 10, 12, 13, 15], 9, 1, 4), ('ii', [17], 10, 1, 2),
        ('iii', [19, 21, 22, 23, 25], 11, 1, 4), ('iv', range(27, 32), 12, 1, 4),
        ('v', range(32, 37), 13, 0, 4), ('vii', range(39, 44), 15, 1, 4),
    ]:
        answer = s(4, sr, sg)
        if sr == 13:
            answer = without_marker(answer)
        rows = [point(answer, marks)]
        if roman == 'iv':
            rows[0]['contextNote'] = 'This response is paper(iv), misprinted(vi) in the scheme; the Maths answer is bound by the exact question wording.'
        listen('D', None, roman, qr, rows)
    listen('D', None, 'vi', [37], [anyn(options(4, [14], group=1, separator='/'), 1, 2)])


def consolidations(census):
    records = []
    romans = ['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x', 'xi', 'xii', 'xiii']
    for suffix, count, pp, pr, sp, sr, reason in [
        ('1-1', 5, 3, [0, 1], 5, 3, 'One required five-link task, two marks per cell, with complete original ten-link stimulus.'),
        ('2b', 6, 5, [15, 16, 17, 18], 6, 7, 'One any-five-of-six truth1/evidence2 pool. Original(ii) was unshipped: include it from verified source but never invent an original alias key.'),
        ('2c', 13, 6, [17], 7, 0, 'One complete any-ten-of-thirteen kanji pool across paper6–7, one mark per answer.'),
        ('3a-5', 4, 10, [0], 8, 10, 'One any-three-of-four Japanese-response pool, two marks per chosen answer.'),
        ('3b-1', 6, 10, [10, 11], 8, 20, 'One any-five-of-six negative-form pool, two marks per answer; preserve all printed alternatives.'),
        ('3b-2', 6, 10, [19, 20], 9, 0, 'One any-five-of-six particle pool, two marks per answer.'),
    ]:
        canonical = 'ja-2021-ol-' + suffix
        task = next(task for task in census['tasks'] if canonical == 'ja-2021-ol-' + '-'.join(str(part).lower() for part in task['key'] if part is not None))
        records.append({'canonicalId': canonical, 'legacyIds': [canonical + '-' + part for part in romans[:count] if canonical + '-' + part in ORIGINAL_IDS],
                        'taskKey': task['key'], 'marks': task['marks'], 'reason': reason,
                        'paperEvidence': {'page': pp, 'text': joined_selector('paper', pp, [(row, None) for row in pr])},
                        'schemeEvidence': {'page': sp, 'text': cell('scheme', sp, sr)}})
    return records


def build():
    reading()
    writing()
    listening()
    census = json.loads((Path(__file__).parent / 'reviews/japanese-2021-ol-census.json').read_text())
    expected = {'ja-2021-ol-' + '-'.join(str(part).lower() for part in task['key'] if part is not None): task for task in census['tasks']}
    assert set(expected) == {card['id'] for card in CARDS}
    for card in CARDS:
        task = expected[card['id']]
        assert card['totalMarks'] == task['marks'], (card['id'], card['totalMarks'], task['marks'])
        assert card['sourceEvidence']['paperPages'] == task['paperPages']
        assert card['sourceEvidence']['schemePages'] == task['schemePages']
    assert len(CARDS) == 57
    assert sum(card['totalMarks'] for card in CARDS) == 300
    return {'subjectId': 'japanese', 'sitting': '2021-ol', 'reviewedAt': '2026-11-09',
            'sources': [{'document': name, 'path': str(path.relative_to(ROOT)), 'sha256': HASHES[name],
                         'pagesReviewed': list(range(1, len(DOCS[name]) + 1))} for name, path in PATHS.items()],
            'cards': CARDS, 'selectors': EVIDENCE, 'status': 'source-reviewed-browser-qa-pending',
            'choiceAnalysis': census['choiceBoundaries'], 'consolidations': consolidations(census)}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    result = build()
    if args.write:
        (ROOT / 'scripts/markbank/authoring/reviews/japanese-2021-ol.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
        manifest = ROOT / 'components/MarkBank/figures-japanese.json'
        previous = json.loads(manifest.read_text())
        previous.update(FIGURES)
        manifest.write_text(json.dumps(previous, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'cards': len(CARDS), 'marks': sum(card['totalMarks'] for card in CARDS), 'figures': len(FIGURES)}, indent=2))
