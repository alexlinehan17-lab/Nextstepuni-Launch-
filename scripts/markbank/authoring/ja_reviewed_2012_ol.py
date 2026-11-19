#!/usr/bin/env python3
"""Publish the independently censused 2012 Ordinary sitting from PDF selectors.

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
    'paper': ROOT / 'examiner-reports/japanese/papers/2012-ol-000-paper.pdf',
    'aural': ROOT / 'examiner-reports/japanese/papers/2012-ol-A00-paper.pdf',
    'scheme': ROOT / 'examiner-reports/japanese/schemes/2012-ol.pdf',
}
HASHES = {
    'paper': '321fb05912052148a0b71c99deb4a825dc00f0dc39b8005379e3229dbc4bc5e3',
    'aural': 'ae87cf36ebb7962067bfc06fca86abbb185ca34b683a443341d6d8e82db3e875',
    'scheme': '28a98e6d51c20e2bb207594d9d2c1c03058b2637d09c0bfd9ac43f8cd4465eaf',
}
for name, path in PATHS.items():
    assert hashlib.sha256(path.read_bytes()).hexdigest() == HASHES[name], path
DOCS = {name: fitz.open(path) for name, path in PATHS.items()}
ROWS = {name: [page_rows(page) for page in doc] for name, doc in DOCS.items()}
CARDS, EVIDENCE, FIGURES, BINDINGS = [], [], {}, []
EXISTING_FIGURES = json.loads((ROOT / 'components/MarkBank/figures-japanese.json').read_text())
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
    text = ' '.join(' '.join(cell(doc, page, row, i) for i, group in enumerate(ROWS[doc][page - 1][row]) if group[0] >= xmin) for row in rows).strip()
    assert text, (doc, page, rows, xmin)
    return text


def s(page, row, group=0):
    return re.sub(r'\s*\(?\s*\d+\s*marks?\)?\s*$', '', cell('scheme', page, row, group)).strip().removeprefix('- ').strip()


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
    return {'kind': 'source-text', 'label': '2012 Japanese Ordinary Level', 'title': 'Original examination material',
            'pages': pages, 'attribution': '© State Examinations Commission.',
            **({'presentationNote': FURIGANA_NOTE} if component == 'paper' else {}), '_component': component}


def crop(key, page, region, alt, component='paper'):
    sheet = DOCS[component][page - 1]
    rect = fitz.Rect(region[0] * sheet.rect.width, region[1] * sheet.rect.height, region[2] * sheet.rect.width, region[3] * sheet.rect.height)
    rel = f'/exam-figures/japanese/{key}.png'
    path = ROOT / 'public' / rel.lstrip('/')
    path.parent.mkdir(parents=True, exist_ok=True)
    metadata = {'src': rel, 'alt': alt, 'attribution': '© State Examinations Commission.',
                'source': {'document': component, 'page': page, 'region': region}}
    previous = EXISTING_FIGURES.get(key, {})
    # Source PDFs are hash-pinned above. Reuse an unchanged source crop only
    # when its exact region/metadata and existing image digest still agree.
    reusable = path.is_file() and all(previous.get(name) == value for name, value in metadata.items())
    if not reusable or hashlib.md5(path.read_bytes()).hexdigest() != previous.get('md5'):
        sheet.get_pixmap(matrix=fitz.Matrix(2, 2), clip=rect).save(path)
        print(f'Rendered changed original crop: {key}')
    FIGURES[key] = {**metadata, 'md5': hashlib.md5(path.read_bytes()).hexdigest()}
    return key


def add(section, q, question, rows, topic, pp, sp, suffix='', rubric=None, total=None, reading=None, figure=None, stem=None):
    cid = f'ja-2012-ol-{section.lower()}' + (f'-{q}' if q is not None else '') + (f'-{suffix}' if suffix else '')
    ref = f'2012 OL Section {section}' + (f' Q{q}' if q is not None else ' Q' if suffix else '') + ''.join(f'({part})' for part in suffix.split('-') if part)
    listening = section.startswith('L')
    card = {'id': cid, 'source': 'sec', 'subjectId': 'japanese', 'specVersion': 'lc-japanese-syllabus',
            'kind': 'rubric' if rubric else 'question', 'level': 'ordinary', 'year': 2012,
            'section': section[1:] if listening else section[0] if section[0] in '1234' else 'Q5',
            'topicId': topic, 'conceptId': concept_for(question, cid), 'questionRef': ref,
            'questionText': question, 'totalMarks': total if total is not None else sum(map(worth, rows)),
            'qa': {'gates': ['verbatim', 'tariff', 'figure'], 'humanReviewedBy': 'agent-verified', 'humanReviewedAt': '2026-11-10'},
            'sourceEvidence': {'component': 'aural' if listening else 'paper', 'paperPages': pp, 'schemePages': sp},
            'schemeCitation': 'Marking points quoted from the SEC marking scheme, Japanese 2012 Ordinary Level — © State Examinations Commission.'}
    if cid in ORIGINAL_IDS:
        card['qa']['gates'].append('reviewed-card-correction')
    if listening or section[0] in '123':
        rule_page = 3 if listening else 5
        card['sourceEvidence']['generalSchemePages'] = [rule_page]
        card['answerLanguageRule'] = {'otherLanguageMultiplier': 0.5, 'sourceText': cell('scheme', rule_page, 1 if listening else 10), 'schemePages': [rule_page]}
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


def find_row(doc, page, phrase):
    found = [i for i, row in enumerate(ROWS[doc][page - 1]) if phrase in ' '.join(group[2] for group in row)]
    assert len(found) == 1, (doc, page, phrase, found)
    return found[0]



def group_rows(card, groups):
    card['taskGroups'] = [{'sourceCardId': card['id'] + '-' + name, 'label': label,
        'marks': sum(worth(row) for row in card['rows'][start:end]), 'rowIds': [row['id'] for row in card['rows'][start:end]]}
        for name, label, start, end in groups]


def criterion(text, maximum, allowed, note):
    return {'kind': 'criterion', 'verbatim': text, 'marks': maximum, 'permittedMarks': allowed, 'contextNote': note}


def reading_q1():
    instruction = p(3, 3)
    labels = [english(p(3, r, 1 if r != 11 else 0)) for r in range(4, 12)]
    rows = [point(s(5, r, 2 if r != 20 else 1), 2, contextNote=label) for r, label in zip(range(13, 21), labels)]
    c = add('1', 1, instruction + '\n' + '\n'.join(labels), rows, 'japanese-5-0', [3], [5], reading=[2],
        figure=crop('ja-2012-ol-1-1', 3, [.065, .025, .97, .345], instruction))
    group_rows(c, [(f'price-{i + 1}', label, i, i + 1) for i, label in enumerate(labels)])
    add('1', 2, p(3, 13, 0), [point(s(5, 23), 2)], 'japanese-5-0', [3], [5], 'i', reading=[2])
    add('1', 2, p(3, 15, 0), [anyn(s(5, 25).split('/'), 1, 2)], 'japanese-5-0', [3], [5], 'ii', reading=[2])
    add('1', 3, p(3, 17), [point(s(5, r, 1), 2) for r in [27, 28]], 'japanese-5-0', [3], [5], reading=[2])
    instruction = p(3, 21)
    add('1', 4, instruction + '\n' + p(3, 22) + '\n' + '\n'.join(p(3, r) for r in [23, 24]),
        [point(sa(5, r), 2, contextNote=english(p(3, pr, 1))) for r, pr in [(30, 23), (31, 24)]], 'japanese-5-0', [3], [5], reading=[2],
        figure=crop('ja-2012-ol-1-4', 3, [.065, .595, .97, .745], instruction))
    add('1', 5, p(3, 26, 0), [criterion(s(5, 33), 3, [0, 1, 3], cell('scheme', 5, 33, 1) + ' — The printed whole-response total is 3. Retain cake-only 1 and drink-only 3 exactly; do not add them to 4 or infer an unprinted 2-mark allocation.')], 'japanese-5-0', [3], [5], reading=[2])
    hours = cell('scheme', 5, 36)
    parts = [text.strip().removeprefix('to ').strip() for text in hours.split('(1 mark)') if text.strip()]
    assert len(parts) == 2
    add('1', 6, p(3, 28), [point(text) for text in parts], 'japanese-5-0', [3], [5], 'i', reading=[2])
    add('1', 6, clean_label(p(3, 30)), [point(s(5, 38), 2)], 'japanese-5-0', [3], [5], 'ii', reading=[2])


def reading_q2():
    instruction = english(p(5, 0))
    names = [p(5, 2, i) for i in range(4)]
    field_labels = [joined_selector('paper', 5, [(r, 0) for r in rr]) for rr in [[6, 7], [12, 13, 14], [18, 19]]]
    rows, groups = [], []
    for i, name in enumerate(names):
        start = len(rows)
        if i != 0: rows.append(point(s(6, 3, i + 1), contextNote=name + ' — ' + field_labels[0]))
        if i != 3: rows.append(point(s(6, 5, i + 1), contextNote=name + ' — ' + field_labels[1]))
        if i != 2:
            answer = s(6, 8, i) if i else cell('scheme', 6, 8, 0).rsplit(' ', 1)[1]
            rows.append(point(answer, contextNote=name + ' — ' + field_labels[2]))
        groups.append((f'person-{i + 1}', name, start, len(rows)))
    c = add('2A', None, instruction + '\n' + '\n'.join(names + field_labels), rows, 'japanese-5-0', [5], [6], reading=[4],
        figure=crop('ja-2012-ol-2a', 5, [.065, .025, .97, .35], instruction), stem='Tanaka, Ginza and Labrador are already supplied in the original table; all nine remaining cells are required.')
    group_rows(c, groups)
    instruction = p(5, 22) + ' ' + p(5, 23)
    prompt_rows = [29, 31, 34, 37, 40, 43, 45, 48]
    sr_truth = [11, 14, 17, 20, 23, 26, 29, 32]
    quote_rows = [[12], [15], [18, 19], [21], [25], [28], [31], [33]]
    rows, groups, labels = [], [], []
    for i, (pr, tr, qr) in enumerate(zip(prompt_rows, sr_truth, quote_rows)):
        label = english(p(5, pr, 1 if pr in [31, 45] else 0)).removeprefix('/ ')
        labels.append(label)
        quote = joined_selector('scheme', 6, [(r, 0) for r in qr]).removeprefix('→').strip()
        quote = re.sub(r'\s*1 mark\s*$', '', quote).strip()
        start = len(rows)
        rows.extend([point(s(6, tr, 2), contextNote=label + ' — decision'), point(quote, contextNote=label + ' — exact evidence')])
        groups.append((f'statement-{i + 1}', label, start, len(rows)))
    c = add('2B', None, instruction + '\n' + '\n'.join(labels), rows, 'japanese-5-0', [5], [6], reading=[4],
        figure=crop('ja-2012-ol-2b', 5, [.065, .37, .97, .975], instruction))
    group_rows(c, groups)


def reading_q3():
    def read(q, roman, question, rows):
        return add('3A', q, question, rows, 'japanese-5-2', [7], [7], roman, reading=[6])
    read(1, 'i', english(p(7, 1, 2)), [point(s(7, 2, 2), 2)])
    read(1, 'ii', p(7, 3, 0), [point(s(7, 3, 1), 2)])
    countries = re.sub(r'\s*\(any.*$', '', s(7, 6))
    read(2, '', p(7, 5), [anyn([answer.strip() for answer in countries.split(',')], 2, 2, contextNote=cell('scheme', 7, 6))])
    read(3, 'i', p(7, 8, 0), [point(s(7, 8), 2)])
    read(3, 'ii', english(p(7, 10)) + ' ' + p(7, 11, 0), [point(s(7, 10, g), 2) for g in [0, 1]])
    read(3, 'iii', p(7, 13, 0), [point(s(7, 12), 2)])
    for q, roman, pr, choices, sr in [(4, '', 14, range(15, 19), 14), (5, 'i', 19, range(20, 24), 16),
        (5, 'ii', 24, range(25, 29), 18), (6, '', 29, range(30, 34), 20)]:
        head = english(p(7, pr, 1 if pr in [14, 19, 29] else 0))
        question = head + '\n' + '\n'.join(p(7, r, 0) + ' ' + english(p(7, r, 1)) for r in choices)
        read(q, roman, question, [point(s(7, sr), 2)])
    instruction = p(8, 1)
    labels = [p(8, r, 0) + (' ' + p(8, r, 1) if r != 18 else '') for r in range(4, 24, 2)]
    c = add('3B', None, instruction + '\n' + '\n'.join(p(8, r) for r in range(2, 24)),
        [point(s(7, r, 1), contextNote=label) for r, label in zip(range(22, 32), labels)], 'japanese-5-4', [8], [7], reading=[6],
        figure=crop('ja-2012-ol-3b', 8, [.065, .025, .97, .48], instruction))
    group_rows(c, [(f'kanji-{i + 1}', label, i, i + 1) for i, label in enumerate(labels)])
    for q, pr, prompt_rows, sr, region in [(1, 26, range(27, 33), range(2, 7), [.065, .48, .97, .70]),
        (2, 34, range(35, 41), range(8, 13), [.065, .70, .97, .95])]:
        instruction = p(8, pr)
        add('3C', q, instruction + '\n' + '\n'.join(p(8, r) for r in prompt_rows),
            [point(sa(8, r), 2, contextNote=p(8, qr, 0)) for r, qr in zip(sr, list(prompt_rows)[1:])],
            'japanese-5-5', [8], [8], reading=[6], figure=crop(f'ja-2012-ol-3c-{q}', 8, region, instruction))
    question = p(9, 4)
    guide = cell('scheme', 8, 17)
    add('3D', None, question, [], 'japanese-5-6', [9], [8], total=6,
        stem=p(9, 0).split('D. ', 2)[2] + ' ' + col('paper', 9, [1, 2]),
        rubric={'system': 'language-writing', 'taskRequirements': [question],
            'criteria': [{'id': f'point-{i}', 'label': f'Distinct comparison {i}', 'maxMarks': 2, 'permittedMarks': [0, 2], 'guidance': [guide]} for i in [1, 2]]
                + [{'id': 'discretionary', 'label': 'Discretionary', 'maxMarks': 2, 'permittedMarks': [0, 1, 2], 'guidance': [guide]}],
            'markingGuideNote': guide + ' — ' + UNPRINTED + ' Assess two distinct comparisons against the original task; do not invent a published model answer.'})


def writing():
    instruction = col('paper', 10, [2, 3])
    rows = []
    for i, r in enumerate(range(2, 12), 1):
        label = re.match(r'\([ivx]+\)', cell('scheme', 9, r, 0)).group()
        note = label
        if i == 3: note += ' — Original word bank: ' + p(10, 13, 1) + '; scheme: ' + sa(9, r) + '. Both original spellings are retained.'
        rows.append(point(sa(9, r), 3, contextNote=note))
    c = add('4', None, instruction + '\n' + '\n'.join(p(10, r) for r in range(4, 18)), rows, 'japanese-5-7', [10], [9], reading=[10],
        figure=crop('ja-2012-ol-4', 10, [.065, .025, .97, .93], instruction))
    group_rows(c, [(f'blank-{i + 1}', re.match(r'\([ivx]+\)', row['contextNote']).group(), i, i + 1) for i, row in enumerate(rows)])
    instruction = col('paper', 11, [1, 2, 3])
    labels = [p(11, r) for r in range(4, 11)]
    content_bands = [{'label': s(10, row), 'marks': marks, 'guidance': [s(10, row, 1)]} for row, marks in [(4, [1]), (3, [2, 3]), (2, [4]), (1, [5])]]
    expression_bands = [{'label': s(10, first), 'marks': marks,
        'guidance': [joined_selector('scheme', 10, [(first, 1)] + [(r, 0) for r in rest])]} for first, rest, marks in [(17, range(18, 24), [1]), (24, range(25, 31), [2, 3]), (31, range(32, 38), [4, 5])]]
    allocation = cell('scheme', 9, 14)
    groups = []
    for i, label in enumerate(labels, 1):
        groups.append({'id': f'item-{i}', 'label': label, 'rows': [], 'criteria': [
            {'id': f'item-{i}-content', 'label': 'Content', 'maxMarks': 5, 'permittedMarks': list(range(6)), 'guidance': [allocation], 'bands': content_bands},
            {'id': f'item-{i}-expression', 'label': 'Expression', 'maxMarks': 5, 'permittedMarks': list(range(6)), 'guidance': [cell('scheme', 10, 6)], 'bands': expression_bands}]})
    guide = cell('scheme', 9, 13) + ' ' + allocation + ' ' + joined_selector('scheme', 10, [(r, None) for r in list(range(9, 16)) + [38, 39]])
    guide += ' — Source discrepancy: the paper prints seven prompts, including (v) favourite teacher. The scheme lists six, omitting that prompt and labelling the paper’s (vi) after-school and (vii) school-liking prompts as 5 and 6. All seven original prompts remain under the common any-five C5/E5 rubric. No lower-expression cap is printed in this sitting.'
    joined_selector('scheme', 9, [(r, None) for r in range(15, 21)])
    add('5', None, instruction + '\n' + '\n'.join(labels), [], 'japanese-5-7', [11], [9, 10], total=50, reading=[11],
        rubric={'system': 'language-points', 'count': 5, 'taskRequirements': [instruction], 'groups': groups, 'markingGuideNote': guide},
        figure=crop('ja-2012-ol-5', 11, [.055, .025, .97, .95], instruction))


def listening():
    def listen(section, q, roman, qr, rows, sp=None):
        page = {'A': 2, 'B': 3, 'C': 4, 'D': 5}[section]
        question = re.sub(r'^(?:\d+\.?\s*)?(?:\([ivx]+\)\s*)?', '', col('aural', page, qr)).strip()
        card = add('L' + section, q, question, rows, 'japanese-6-2' if section == 'C' else 'japanese-6-1' if section == 'D' else 'japanese-6-0',
            [page], [sp or (3 if section in 'AB' else 4)], roman, reading=[page])
        card['stem'] = col('aural', page, range(1, 6 if section == 'C' else 5))
        if section == 'B': card['stem'] += '\n' + col('aural', page, [{1: 5, 2: 13, 3: 25}[q]])
        if section == 'C': card['stem'] += '\n' + col('aural', page, [{1: 6, 2: 28, 3: 40}[q]])
        if section == 'D': card['stem'] += '\n' + col('aural', page, [6 if q == 1 else 24])
        return card
    for q, roman, qr, sr, marks in [
        (1, 'i', range(6, 11), 3, 3), (1, 'ii', [11, 12], 4, 2),
        (2, 'i', range(13, 18), 5, 3), (2, 'ii', [18, 19], 6, 2),
        (3, 'i', range(20, 26), 7, 3), (3, 'ii', [26, 27], 8, 2),
        (4, 'i', range(28, 33), 9, 3), (4, 'ii', [33, 34], 10, 2),
        (5, 'i', range(35, 42), 11, 3), (5, 'ii', [42, 43], 12, 2)]:
        listen('A', q, roman, qr, [point(s(3, sr, 1), marks)])
    listen('B', 1, 'i', range(6, 11), [point(s(3, 15, 1), 3)])
    directions = joined_selector('scheme', 3, [(16, 1), (17, 0)])
    listen('B', 1, 'ii', [11], [anyn([part.strip().rstrip('.') for part in directions.split('/')], 1, 3, contextNote=cell('scheme', 3, 18))])
    for q, roman, qr, sr in [(2, 'i', range(14, 20), 20), (2, 'ii', range(20, 25), 21),
        (3, 'i', [26, 27], 23), (3, 'ii', range(29, 34), 24), (3, 'iii', [34], 25)]:
        listen('B', q, roman, qr, [point(s(3, sr, 1), 3)])
    for roman, qr, sr in [('i', range(7, 13), 2), ('ii', range(13, 19), 3), ('iii', range(19, 25), 4)]:
        listen('C', 1, roman, qr, [point(s(4, sr, 1), 3)])
    listen('C', 1, 'iv', [25, 26], [point(s(4, 6), 2)])
    listen('C', 2, 'i', range(29, 34), [point(s(4, 8, 1), 3)])
    job = joined_selector('scheme', 4, [(10, 0), (11, 0)])
    listen('C', 2, 'ii', [34, 35], [point(job, 4, contextNote=cell('scheme', 4, 9, 1) + ' — One accepted detail earns 4. The complete original pool is retained, including its printed age wording; do not count separate age endpoints.')])
    number = re.sub(r'\s+', '', s(4, 14))
    assert number == '03-8353-4969'
    digits = re.sub(r'\D', '', number)
    guide = cell('scheme', 4, 15)
    rows = [point(digits[position - 1], 1, contextNote=f'Missing digit {i + 1} (position {position} in {number}). {guide} — The printed 03, 4 and final 9 are given; only the six original blanks score.') for i, position in enumerate([3, 4, 5, 6, 8, 9])]
    phone = listen('C', 2, 'iii', [37], rows)
    phone['questionFigureKey'] = crop('ja-2012-ol-lc-2-iii', 4, [.055, .66, .97, .73], phone['questionText'], 'aural')
    for roman, qr, sr in [('i', range(41, 47), 17), ('ii', range(47, 55), 18)]:
        listen('C', 3, roman, qr, [point(s(4, sr, 1), 3)])
    listen('D', 1, 'i', range(7, 12), [point(s(4, 22), 3)])
    for roman, qr, first, last, allowed in [('ii', [12], 24, 26, [0, 2, 4]), ('iii', [15], 28, 30, [0, 1, 4])]:
        answer = joined_selector('scheme', 4, [(r, None) for r in range(first, last + 1)])
        listen('D', 1, roman, qr, [criterion(answer, 4, allowed, 'One complete response: apply only the printed full or partial tariff; do not add a partial answer to its full version.')])
    listen('D', 1, 'iv', range(17, 23), [point(s(4, 32), 3)])
    listen('D', 2, 'i', range(25, 30), [point(s(5, 2), 3)], 5)
    answer = joined_selector('scheme', 5, [(r, None) for r in range(4, 7)])
    listen('D', 2, 'ii', [30], [criterion(answer, 4, [0, 1, 4], 'One complete response: Tokyo alone earns the printed 1 mark; do not add it to the full 4-mark answer.')], 5)
    listen('D', 2, 'iii', range(33, 38), [point(s(5, 8), 3)], 5)


def build():
    reading_q1(); reading_q2(); reading_q3(); writing(); listening()
    census = json.loads((Path(__file__).parent / 'reviews/japanese-2012-ol-census.json').read_text())
    expected = {'ja-2012-ol-' + '-'.join(str(part).lower() for part in task['key'] if part is not None): task for task in census['tasks']}
    assert set(expected) == {card['id'] for card in CARDS}, (set(expected) - {c['id'] for c in CARDS}, {c['id'] for c in CARDS} - set(expected))
    def inspect(value):
        if isinstance(value, dict):
            for key, child in value.items():
                if key == 'guidance': assert child and all(isinstance(text, str) and text.strip() for text in child)
                inspect(child)
        elif isinstance(value, list):
            for child in value: inspect(child)
        elif isinstance(value, str): assert not any(ord(ch) < 32 and ch not in '\n\r\t' or ch == '\ufffd' for ch in value), value
    for card in CARDS:
        task = expected[card['id']]
        assert card['questionText'].strip()
        assert card['totalMarks'] == task['marks'], (card['id'], card['totalMarks'], task['marks'])
        assert card['sourceEvidence']['paperPages'] == task['paperPages']
        assert card['sourceEvidence']['schemePages'] == task['schemePages'], (card['id'], card['sourceEvidence'], task)
        inspect(card)
    assert len(CARDS) == 59 and sum(card['totalMarks'] for card in CARDS) == 300
    assert sum('answerLanguageRule' in card for card in CARDS) == 57
    assert not any(card['id'] in ORIGINAL_IDS for card in CARDS)
    return {'subjectId': 'japanese', 'sitting': '2012-ol', 'reviewedAt': '2026-11-10',
        'sources': [{'document': name, 'path': str(path.relative_to(ROOT)), 'sha256': HASHES[name], 'pagesReviewed': list(range(1, len(DOCS[name]) + 1))} for name, path in PATHS.items()],
        'cards': CARDS, 'selectors': EVIDENCE, 'status': 'source-reviewed-browser-qa-pending', 'choiceAnalysis': census['choiceBoundaries'], 'consolidations': [], 'sourceAnswerBindings': BINDINGS}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('--write', action='store_true'); args = parser.parse_args()
    result = build()
    if args.write:
        text = '# Original PDF text and furigana folded at its printed character\n'
        for i, page in enumerate(DOCS['scheme']):
            text += f'\n## Physical page {i + 1}\n\n' + page.get_text() + '\n### Printed rows\n\n' + '\n'.join(' '.join(g[2] for g in row) for row in page_rows(page)) + '\n'
        PATHS['scheme'].with_suffix('.md').write_text(text.rstrip() + '\n')
        (ROOT / 'scripts/markbank/authoring/reviews/japanese-2012-ol.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
        manifest = ROOT / 'components/MarkBank/figures-japanese.json'; previous = json.loads(manifest.read_text()); previous.update(FIGURES)
        manifest.write_text(json.dumps(previous, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'cards': len(CARDS), 'marks': sum(c['totalMarks'] for c in CARDS), 'figures': len(FIGURES)}, indent=2))
