#!/usr/bin/env python3
"""Publish the independently censused 2015 Ordinary sitting from PDF selectors.

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
    'paper': ROOT / 'examiner-reports/japanese/papers/2015-ol-000-paper.pdf',
    'aural': ROOT / 'examiner-reports/japanese/papers/2015-ol-A00-paper.pdf',
    'scheme': ROOT / 'examiner-reports/japanese/schemes/2015-ol.pdf',
}
HASHES = {
    'paper': 'f879d2104da262a0d71d0b35fe4e8b96663005919a79de7e985437311ddbaae4',
    'aural': '4182135287021fe369c51c80cdb12a9c1d87b8bcbdf6b859995a005c6d72ca91',
    'scheme': 'a61a77888865f54df92faadfbde180cf052ab549a5f17a255856961808da22e8',
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
    text = ' '.join(' '.join(cell(doc, page, row, i) for i, group in enumerate(ROWS[doc][page - 1][row]) if group[0] >= xmin) for row in rows).strip()
    assert text, (doc, page, rows, xmin)
    return text


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
    return {'kind': 'source-text', 'label': '2015 Japanese Ordinary Level', 'title': 'Original examination material',
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
    cid = f'ja-2015-ol-{section.lower()}' + (f'-{q}' if q is not None else '') + (f'-{suffix}' if suffix else '')
    ref = f'2015 OL Section {section}' + (f' Q{q}' if q is not None else ' Q' if suffix else '') + ''.join(f'({part})' for part in suffix.split('-') if part)
    listening = section.startswith('L')
    card = {'id': cid, 'source': 'sec', 'subjectId': 'japanese', 'specVersion': 'lc-japanese-syllabus',
            'kind': 'rubric' if rubric else 'question', 'level': 'ordinary', 'year': 2015,
            'section': section[1:] if listening else section[0] if section[0] in '1234' else 'Q5',
            'topicId': topic, 'conceptId': concept_for(question, cid), 'questionRef': ref,
            'questionText': question, 'totalMarks': total if total is not None else sum(map(worth, rows)),
            'qa': {'gates': ['verbatim', 'tariff', 'figure'], 'humanReviewedBy': 'agent-verified', 'humanReviewedAt': '2026-11-09'},
            'sourceEvidence': {'component': 'aural' if listening else 'paper', 'paperPages': pp, 'schemePages': sp},
            'schemeCitation': 'Marking points quoted from the SEC marking scheme, Japanese 2015 Ordinary Level — © State Examinations Commission.'}
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
    instruction = without_marker(col('paper', 3, [0]))
    labels = [clean_label(col('paper', 3, [row])) for row in range(2, 7)]
    answers = [s(5, 4, 2), s(5, 5, 1).split()[-1], s(5, 6, 2), s(5, 7, 1).split()[-1], s(5, 8, 2)]
    add('1', 1, instruction + '\n' + col('paper', 3, [1]) + '\n' + '\n'.join(labels),
        [point(answer, 2, contextNote=label) for label, answer in zip(labels, answers)],
        'japanese-5-0', [3], [5], reading=[2, 3])
    labels = [clean_label(col('paper', 3, [row])) for row in range(10, 15)]
    name = s(5, 10, 2).split('(1 mark)')
    rows = [anyn([part.strip() for part in name[0].split('/')], 1, 1, contextNote=labels[0]),
            point(name[1].strip(' /'), 1, contextNote=labels[0])]
    rows += [point(s(5, row, 2), 2, contextNote=label) for row, label in zip([12, 13], labels[1:3])]
    rows += [anyn(options(5, [14], 2, '/'), 1, 2, contextNote=labels[3]), point(s(5, 15, 2), 2, contextNote=labels[4])]
    add('1', 2, without_marker(col('paper', 3, [8])) + '\n' + '\n'.join(labels), rows,
        'japanese-5-0', [3], [5], reading=[2], stem=p(3, 7, 1))
    add('1', 3, without_marker(col('paper', 3, [15])), [anyn(options(5, [17], separator='/'), 2, 2)],
        'japanese-5-0', [3], [5], reading=[2], stem=p(3, 7, 1))
    for roman, row in [('i', 20), ('ii', 21)]:
        add('1', 4, without_marker(col('paper', 3, [19])) + '\n' + clean_label(col('paper', 3, [row])),
            [point(s(5, row, 2), 2)], 'japanese-5-0', [3], [5], roman, reading=[2], stem=p(3, 7, 1))
    add('1', 5, without_marker(col('paper', 3, [22])), [point(s(5, 23), 2)], 'japanese-5-0', [3], [5], reading=[2], stem=p(3, 7, 1))
    instruction = without_marker(col('paper', 5, [1]))
    labels = [clean_label(col('paper', 5, [row])) for row in [3, 4, 5]]
    answers = [s(6, 3, 1), s(6, 4, 1), sa(6, 5).removeprefix('Kyari Pamyu Pamyu ').strip()]
    add('2A', 1, instruction + '\n' + '\n'.join(labels),
        [point(answer, 2, contextNote=label) for label, answer in zip(labels, answers)],
        'japanese-5-2', [5], [6], reading=[4], stem=p(5, 0, 1))
    instruction = without_marker(col('paper', 5, [6, 7]))
    countries = options(6, [7], separator='/')
    partial = re.sub(r'^\(|\s+1 mark\)$', '', s(6, 8))
    rubric = pool(2, countries + [partial], countries + [partial], 2, instruction, cell('scheme', 6, 7) + ' ' + cell('scheme', 6, 8))
    rubric['groups'][-1]['rows'][0]['marks'] = 1
    add('2A', 2, instruction, [], 'japanese-5-2', [5], [6], reading=[4], stem=p(5, 0, 1), rubric=rubric, total=4)
    add('2A', 3, without_marker(col('paper', 5, [9, 10])), [anyn(options(6, [10], separator='/'), 1, 2)],
        'japanese-5-2', [5], [6], reading=[4], stem=p(5, 0, 1))
    instruction = p(5, 14) + ' ' + p(5, 15)
    labels = [p(5, 20, 0) + ' ' + english(p(5, 20, 1)) + ' ' + p(5, 21),
              p(5, 23, 0) + ' ' + english(p(5, 23, 1)),
              p(5, 25, 0) + ' ' + english(p(5, 25, 1)) + ' ' + p(5, 26),
              p(5, 28, 0) + ' ' + english(p(5, 28, 1)) + ' ' + p(5, 29),
              p(5, 31, 0) + ' ' + p(5, 32)]
    quotes = [s(6, row) for row in [14, 16, 19, 21]] + [s(6, 25) + s(6, 26)]
    groups = [{'id': f'item-{i + 1}', 'label': label, 'rows': [
        {'id': 'true-false', 'text': s(6, row, 2), 'marks': 1},
        {'id': 'quote', 'text': quote, 'marks': 2}]} for i, (label, row, quote) in enumerate(zip(labels, [13, 15, 18, 20, 23], quotes))]
    add('2B', None, instruction + '\n' + '\n'.join(labels), [], 'japanese-5-2', [5], [6], total=15, reading=[4, 5],
        rubric={'system': 'language-points', 'count': 5, 'taskRequirements': [instruction], 'groups': groups, 'markingGuideNote': cell('scheme', 6, 12)},
        figure=crop('ja-2015-ol-2b', 5, [.07, .42, .97, .953], instruction))
    instruction = p(6, 13)
    labels = [p(6, row) for row in range(15, 25)]
    answers = [s(7, row, 2 if row == 1 else 1) for row in range(1, 11)]
    add('2C', None, instruction + '\n' + p(6, 14) + '\n' + '\n'.join(labels), [], 'japanese-5-4', [6], [7], total=10, reading=[6],
        rubric=pool(10, labels, answers, 1, instruction, cell('scheme', 7, 0)),
        figure=crop('ja-2015-ol-2c', 6, [.07, .51, .97, .95], instruction))
    allocation = s(7, 13)
    add('2D', None, p(7, 5), [{'kind': 'criterion', 'verbatim': UNPRINTED, 'unprinted': True, 'marks': 4,
        'permittedMarks': [0, 2, 4], 'parts': [{'id': f'point-{i}', 'verbatim': allocation, 'marks': 2, 'permittedMarks': [0, 2]} for i in [1, 2]],
        'contextNote': allocation}], 'japanese-5-6', [7], [7], stem=p(7, 2) + ' ' + p(7, 3))
    dara = s(8, 3).split('(i)', 1)[1].strip()
    hina = s(8, 6, 1)
    first, second = hina.split('(ii)', 1)
    first = re.sub(r'\s*\(2 marks\)', '', first).removeprefix('(i)').strip()
    add('3A', 1, without_marker(col('paper', 9, [1])), [point(dara, 2), anyn([part.strip() for part in sa(8, 3, 1).split('/')], 1, 2)],
        'japanese-5-2', [9], [8], reading=[8], stem=p(9, 0, 1))
    add('3A', 2, without_marker(col('paper', 9, [3])), [point(first, 2), anyn([text.strip() for text in second.split('/')], 1, 2)],
        'japanese-5-2', [9], [8], reading=[8], stem=p(9, 0, 1))
    for roman, qr, sr in [('i', range(7, 12), 9), ('ii', range(12, 17), 10), ('iii', range(17, 22), 11), ('iv', range(22, 27), 12)]:
        answer = s(8, sr, 1) if sr != 10 else '(a)' + s(8, 10).split('(a)', 1)[1]
        add('3A', 3, without_marker(col('paper', 9, qr)), [point(answer, 3)], 'japanese-5-2', [9], [8], roman, reading=[8],
            stem=without_marker(col('paper', 9, [5, 6])))
    for roman, qr, sr in [('i', 28, 15), ('ii', 30, 17), ('iii', 32, 19)]:
        card = add('3A', 4, without_marker(p(9, qr)), [point(s(8, sr), 3)], 'japanese-5-2', [9], [8], roman, reading=[8], stem=english(p(9, 27, 1)))
        if roman == 'i':
            p(8, 9)
            card['rows'][0]['contextNote'] = 'The scheme prints むじかしいです。; the original email prints むずかしいですね。 The published answer is retained literally; this spelling discrepancy does not add a marking condition.'
    for q, instruction_row, example, lr, answers, region in [
        (1, 2, 3, range(4, 9), [s(9, row, 1) for row in [2, 3, 4]] + [sa(9, row) for row in [5, 6]], [.07, .04, .97, .405]),
        (2, 10, 11, range(12, 17), [s(9, 8, 1)] + [sa(9, row) for row in range(9, 13)], [.07, .405, .97, .79])]:
        instruction = p(10, instruction_row)
        labels = [p(10, row) for row in lr]
        add('3B', q, instruction + '\n' + p(10, example) + '\n' + '\n'.join(labels), [], 'japanese-5-5', [10], [9], total=10, reading=[10],
            rubric=pool(5, labels, answers, 2, instruction, cell('scheme', 9, 1 if q == 1 else 7)),
            figure=crop(f'ja-2015-ol-3b-{q}', 10, region, instruction))


def writing():
    instruction = p(11, 4)
    question = instruction + '\n' + '\n'.join(p(11, row) for row in range(5, 19))
    canonical = p(11, 17, 1)
    primary = s(10, 2, 1)
    conditions = {1: cell('scheme', 10, 3, 0), 4: cell('scheme', 10, 7, 0), 8: cell('scheme', 10, 12, 0)}
    primary_rows = [2, 4, 5, 6, 8, 9, 10, 11, 13, 14]
    answers = [[s(10, row, 1) if row != 11 else sa(10, row)] for row in primary_rows]
    answers[0] = [canonical, re.search(r'学校', conditions[1]).group()]
    answers[3] += [re.search(r'大好き', conditions[4]).group(), canonical]
    answers[7] += [re.search(r'バスで', conditions[8]).group()]
    rows = []
    for i, opts in enumerate(answers, 1):
        label = re.match(r'\([ivx]+\)', cell('scheme', 10, primary_rows[i - 1], 0)).group()
        note = label + ' — ' + instruction
        if i in conditions: note += ' — ' + conditions[i]
        if i in [1, 4]:
            note += f' — Original bank: {canonical}; scheme (i): {primary}; scheme (iv) alternative: 日本料理. These source-local spellings identify the same bank entry, which can be used only once.'
        rows.append(anyn(opts, 1, 3, contextNote=note))
    cloze = add('4', None, question, rows, 'japanese-5-7', [11], [10], reading=[11],
        figure=crop('ja-2015-ol-4', 11, [.05, .045, .97, .95], instruction))
    cloze['taskGroups'] = [{'sourceCardId': cloze['id'] + f'-blank-{i + 1}',
        'label': re.match(r'\([ivx]+\)', row['contextNote']).group(), 'marks': 3, 'rowIds': [row['id']]}
        for i, row in enumerate(cloze['rows'])]
    instruction = p(12, 3)
    labels = [p(12, row) for row in range(4, 11)]
    content_bands = [{'label': s(10, row), 'marks': marks, 'guidance': [s(10, row, 1)]}
                     for row, marks in [(28, [1]), (27, [2, 3]), (26, [4, 5])]]
    expression_bands = [{'label': s(11, first), 'marks': marks,
                         'guidance': [s(11, first, 1) + ' ' + ' '.join(s(11, row) for row in rest)]}
                        for first, rest, marks in [(14, range(15, 21), [1]), (21, range(22, 28), [2, 3]), (28, range(29, 35), [4, 5])]]
    cap = joined_selector('scheme', 11, [(2, 0), (3, 0)])
    groups = []
    for i, label in enumerate(labels, 1):
        criteria = [{'id': f'item-{i}-content', 'label': s(10, 25).removesuffix(':'), 'maxMarks': 5,
                     'permittedMarks': list(range(6)), 'guidance': [s(10, 17)], 'bands': content_bands},
                    {'id': f'item-{i}-expression', 'label': s(11, 0).removesuffix(':'), 'maxMarks': 5,
                     'permittedMarks': list(range(6)), 'guidance': [cap], 'bands': expression_bands,
                     'limits': [{'id': f'item-{i}-low-content', 'maxMarks': 3,
                                 'when': {'any': [{'criterionIds': [f'item-{i}-content'], 'atMost': 3}]}, 'guidance': [cap]}]}]
        groups.append({'id': f'item-{i}', 'label': label, 'rows': [], 'criteria': criteria})
    source_prompt = s(10, 22, 1)
    note = f'The original scheme repeats (v) as {source_prompt} The original paper prints どうやって; that paper question is retained. The common content/expression grid still applies.'
    rubric = {'system': 'language-points', 'count': 5, 'taskRequirements': [instruction], 'groups': groups,
              'markingGuideNote': s(10, 16) + ' ' + s(10, 17) + ' ' + cap + ' ' + s(11, 35) + ' ' + s(11, 36) + ' — ' + note}
    add('5', None, instruction + '\n' + '\n'.join(labels), [], 'japanese-5-7', [12], [10, 11], rubric=rubric, total=50,
        reading=[12], figure=crop('ja-2015-ol-5', 12, [.05, .035, .97, .977], instruction))


def listening():
    def listen(section, q, roman, qr, answers):
        page = {'A': 2, 'B': 3, 'C': 4, 'D': 5}[section]
        topic = 'japanese-6-1' if section == 'A' else 'japanese-6-2' if section == 'B' else 'japanese-6-0'
        question = re.sub(r'^(?:\d+\.?\s*)?(?:\([ivx]+\)\s*)?', '', col('aural', page, qr, 290)).strip()
        card = add('L' + section, q, question, answers, topic, [page], [3 if section in 'AB' else 4], roman, reading=[page])
        card['stem'] = col('aural', page, range(1, 7 if section == 'C' else 8), 290)
        if section in 'BC':
            header = {'B': {1: 8, 2: 32, 3: 50}, 'C': {1: 7, 2: 24}}[section][q]
            card['stem'] += '\n' + col('aural', page, [header], 290)
        return card
    for q, roman, qr, sr, sg, marks in [
        (1, 'i', [8], 3, 2, 2), (1, 'ii', range(10, 15), 4, 1, 4), (1, 'iii', range(15, 21), 5, 1, 4),
        (2, 'i', [23], 6, 2, 2), (2, 'ii', range(25, 30), 7, 1, 4), (2, 'iii', range(30, 36), 8, 1, 4),
        (3, 'i', range(36, 41), 9, 2, 4), (3, 'ii', range(41, 46), 10, 1, 4)]:
        listen('A', q, roman, qr, [point(s(3, sr, sg), marks)])
    for q, roman, qr, sr in [(1, 'i', range(9, 17), 13), (1, 'ii', range(18, 27), 14),
        (2, 'i', range(33, 38), 17), (2, 'ii', range(39, 48), 18), (3, 'i', range(52, 61), 20)]:
        listen('B', q, roman, qr, [point(s(3, sr, 1), 4)])
    phone = listen('B', 1, 'iii', [28], [point(sa(3, 15), 4)])
    phone['rows'][0]['contextNote'] = 'The scheme assigns 4 marks to this complete telephone response. The paper has four missing digits; no per-digit tariff is printed.'
    phone['questionFigureKey'] = crop('ja-2015-ol-lb-1-iii', 3, [.54, .425, .96, .52], phone['questionText'], 'aural')
    for q, roman, qr, sr in [(1, 'i', [9, 10], 2), (1, 'ii', range(12, 17), 3), (1, 'iii', range(19, 24), 4),
        (2, 'ii', range(27, 32), 9), (2, 'iii', range(32, 37), 10)]:
        listen('C', q, roman, qr, [point(s(4, sr, 1), 4)])
    full = s(4, 6, 1) + ' ' + s(4, 7)
    partial = s(4, 8)
    listen('C', 2, 'i', [25], [{'kind': 'criterion', 'verbatim': full, 'marks': 4, 'permittedMarks': [0, 2, 4],
        'contextNote': cell('scheme', 4, 6) + ' ' + cell('scheme', 4, 7) + ' ' + partial}])
    for q, qr, sr in [(1, range(8, 14), 12), (2, range(14, 19), 13), (3, range(19, 24), 14),
                      (4, range(24, 29), 15), (5, [29, 30], 16), (6, range(32, 38), 17)]:
        listen('D', q, '', qr, [point(s(4, sr, 1), 4)])


def build():
    reading()
    writing()
    listening()
    census = json.loads((Path(__file__).parent / 'reviews/japanese-2015-ol-census.json').read_text())
    expected = {'ja-2015-ol-' + '-'.join(str(part).lower() for part in task['key'] if part is not None): task for task in census['tasks']}
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
    assert len(CARDS) == 51
    assert sum(card['totalMarks'] for card in CARDS) == 300
    assert sum('answerLanguageRule' in card for card in CARDS) == 49
    assert not any(card['id'] in ORIGINAL_IDS for card in CARDS)
    return {'subjectId': 'japanese', 'sitting': '2015-ol', 'reviewedAt': '2026-11-09',
            'sources': [{'document': name, 'path': str(path.relative_to(ROOT)), 'sha256': HASHES[name],
                         'pagesReviewed': list(range(1, len(DOCS[name]) + 1))} for name, path in PATHS.items()],
            'cards': CARDS, 'selectors': EVIDENCE, 'status': 'source-reviewed-browser-qa-pending',
            'choiceAnalysis': census['choiceBoundaries'], 'consolidations': [],
            'sourceAnswerBindings': [{
                'cardId': 'ja-2015-ol-4', 'answer': '日本りょうり', 'rowIds': ['r-1', 'r-4'],
                'paperSelector': {'document': 'paper', 'page': 11, 'row': 17, 'group': 1, 'text': '日本りょうり'},
                'schemeSelectors': [
                    {'document': 'scheme', 'page': 10, 'row': 2, 'group': 1, 'text': '日本りようり'},
                    {'document': 'scheme', 'page': 10, 'row': 7, 'group': 0, 'text': '（大好き/日本料理  accepted if not used elsewhere）'},
                ],
            }]}


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
        (ROOT / 'scripts/markbank/authoring/reviews/japanese-2015-ol.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
        manifest = ROOT / 'components/MarkBank/figures-japanese.json'
        previous = json.loads(manifest.read_text())
        previous.update(FIGURES)
        manifest.write_text(json.dumps(previous, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'cards': len(CARDS), 'marks': sum(card['totalMarks'] for card in CARDS), 'figures': len(FIGURES)}, indent=2))
