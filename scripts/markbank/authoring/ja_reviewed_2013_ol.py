#!/usr/bin/env python3
"""Publish the independently censused 2013 Ordinary sitting from PDF selectors.

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
    'paper': ROOT / 'examiner-reports/japanese/papers/2013-ol-000-paper.pdf',
    'aural': ROOT / 'examiner-reports/japanese/papers/2013-ol-A00-paper.pdf',
    'scheme': ROOT / 'examiner-reports/japanese/schemes/2013-ol.pdf',
}
HASHES = {
    'paper': '60e7746677773e02248892c88d25ef79416fff3627afcab2fbf61e94756dd3e4',
    'aural': '3e7d66bbb89fdf43d90374851501c743140d1b01a4538902b41c10a3e4ca892e',
    'scheme': '52d26642f93c8f6e01c84e3eda961db01a643ba645848692770fc9c764887e08',
}
for name, path in PATHS.items():
    assert hashlib.sha256(path.read_bytes()).hexdigest() == HASHES[name], path
DOCS = {name: fitz.open(path) for name, path in PATHS.items()}
ROWS = {name: [page_rows(page) for page in doc] for name, doc in DOCS.items()}
CARDS, EVIDENCE, FIGURES, BINDINGS = [], [], {}, []
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
    return {'kind': 'source-text', 'label': '2013 Japanese Ordinary Level', 'title': 'Original examination material',
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
    cid = f'ja-2013-ol-{section.lower()}' + (f'-{q}' if q is not None else '') + (f'-{suffix}' if suffix else '')
    ref = f'2013 OL Section {section}' + (f' Q{q}' if q is not None else ' Q' if suffix else '') + ''.join(f'({part})' for part in suffix.split('-') if part)
    listening = section.startswith('L')
    card = {'id': cid, 'source': 'sec', 'subjectId': 'japanese', 'specVersion': 'lc-japanese-syllabus',
            'kind': 'rubric' if rubric else 'question', 'level': 'ordinary', 'year': 2013,
            'section': section[1:] if listening else section[0] if section[0] in '1234' else 'Q5',
            'topicId': topic, 'conceptId': concept_for(question, cid), 'questionRef': ref,
            'questionText': question, 'totalMarks': total if total is not None else sum(map(worth, rows)),
            'qa': {'gates': ['verbatim', 'tariff', 'figure'], 'humanReviewedBy': 'agent-verified', 'humanReviewedAt': '2026-11-10'},
            'sourceEvidence': {'component': 'aural' if listening else 'paper', 'paperPages': pp, 'schemePages': sp},
            'schemeCitation': 'Marking points quoted from the SEC marking scheme, Japanese 2013 Ordinary Level — © State Examinations Commission.'}
    if cid in ORIGINAL_IDS:
        card['qa']['gates'].append('reviewed-card-correction')
    if listening or section[0] in '123':
        rule_page = 3 if listening else 5
        card['sourceEvidence']['generalSchemePages'] = [rule_page]
        card['answerLanguageRule'] = {'otherLanguageMultiplier': 0.5, 'sourceText': cell('scheme', rule_page, 1 if listening else 11), 'schemePages': [rule_page]}
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



def reading_q1():
    instruction = col('paper', 2, [21, 22])
    labels = [clean_label(col('paper', 2, [row])) for row in range(24, 29)]
    add('1A', None, instruction + '\n' + col('paper', 2, [23]) + '\n' + '\n'.join(labels),
        [point(s(5, row, 2 if row == 14 else 1), 3, contextNote=label) for row, label in zip(range(14, 19), labels)],
        'japanese-5-0', [2], [5], reading=[2], figure=crop('ja-2013-ol-1a', 2, [.065, .025, .95, .957], instruction))
    instruction = col('paper', 3, [15, 16])
    labels = [clean_label(col('paper', 3, [row])) for row in range(20, 25)]
    groups = []
    for i, (label, row) in enumerate(zip(labels, range(21, 26)), 1):
        full = cell('scheme', 5, row)
        building = re.search(r'\b(main|annex)\s*\(\s*2 marks\)', full).group(1)
        floor = s(5, row, 1 if row == 23 else 2)
        groups.append({'id': f'item-{i}', 'label': label, 'rows': [
            {'id': 'building', 'text': building, 'marks': 2}, {'id': 'floor', 'text': floor, 'marks': 2}]})
    add('1B', None, instruction + '\n' + p(3, 18) + '\n' + '\n'.join(labels), [], 'japanese-5-0', [3], [5], total=20,
        reading=[3], rubric={'system': 'language-points', 'count': 5, 'taskRequirements': [instruction], 'groups': groups,
        'markingGuideNote': cell('scheme', 5, 20) + ' — Each required building and floor has 2 printed marks. Restaurants 9 / B1 are alternatives for the same floor response. Sakura Hall is the given example and unpriced.'},
        figure=crop('ja-2013-ol-1b', 3, [.075, .04, .95, .94], instruction))


def reading_q2():
    instruction = without_marker(col('paper', 5, [1, 2]))
    labels = [s(6, 2, 1).split()[1]] + [sa(6, row).split()[0] for row in [3, 4, 5]]
    answers = [without_marker(s(6, 2, 1)).split(' ', 1)[1]] + [sa(6, row).split(' ', 1)[1] for row in [3, 4, 5]]
    add('2A', 1, instruction + '\n' + '\n'.join(p(5, row) for row in range(3, 7)),
        [point(answer, 2, contextNote=label) for answer, label in zip(answers, labels)], 'japanese-5-2', [5], [6], reading=[4],
        figure=crop('ja-2013-ol-2a-1', 5, [.065, .035, .95, .235], instruction))
    instruction = without_marker(col('paper', 5, [7]))
    prompts = [col('paper', 5, [8, 9]), col('paper', 5, [11, 12, 13])]
    # Both names in each bilingual row are distinct required response fields.
    question = instruction + '\n' + prompts[0] + '\n' + clean_label(p(5, 10)) + '\n' + prompts[1] + '\n' + clean_label(p(5, 14))
    raw = [without_marker(cell('scheme', 6, row)) for row in [7, 8, 9, 10]]
    groups = []
    for i, text in enumerate(raw, 1):
        name, answer = text.split(' ', 1)
        if i == 1:
            answer = answer.split(' (', 1)[0]
            groups.append({'id': f'item-{i}', 'label': name, 'rows': [], 'criteria': [{'id': 'answer', 'label': name,
                'maxMarks': 2, 'permittedMarks': [0, 1, 2], 'guidance': [text]}]})
        else:
            groups.append({'id': f'item-{i}', 'label': name, 'rows': [{'id': 'answer', 'text': answer.strip(), 'marks': 2}]})
    guide = cell('scheme', 6, 6) + ' — Choose any two of the four printed named responses. Sarah and Tom ask about merchandise; Susan and Harry ask about places. Guitar alone earns 1 for Sarah; electric guitar earns 2 for that same response.'
    add('2A', 2, question, [], 'japanese-5-2', [5], [6], total=4, reading=[4], rubric={
        'system': 'language-points', 'count': 2, 'taskRequirements': [instruction, *prompts], 'groups': groups, 'markingGuideNote': guide},
        figure=crop('ja-2013-ol-2a-2', 5, [.065, .238, .95, .455], instruction))
    instruction = p(5, 17) + ' ' + p(5, 18)
    labels = [english(p(5, 22, 1)), english(p(5, 24, 1)) + ' ' + p(5, 25), english(p(5, 27, 1)) + ' ' + p(5, 28),
              english(p(5, 30, 1)) + ' ' + p(5, 31), english(p(5, 33, 1)) + ' ' + p(5, 34)]
    groups = []
    for i, (label, tr, qr) in enumerate(zip(labels, [12, 14, 18, 21, 24], [13, 16, 20, 23, 25]), 1):
        quote = re.sub(r'\s*1 mark$', '', cell('scheme', 6, qr, 0)).strip()
        groups.append({'id': f'item-{i}', 'label': label, 'rows': [
            {'id': 'truth', 'text': cell('scheme', 6, tr, 2), 'marks': 2}, {'id': 'quote', 'text': quote, 'marks': 1}]})
    passage = p(4, 10)
    guide = cell('scheme', 6, 11) + ' — Each required True/False decision earns 2 and its supporting quotation earns 1. The given example is unpriced. The scheme last quotation literally prints あかとくる, whereas the passage prints ' + passage + ' Preserve that source discrepancy; no additional marking condition is inferred.'
    add('2B', None, instruction + '\n' + '\n'.join(labels), [], 'japanese-5-2', [5], [6], total=15, reading=[4, 5],
        rubric={'system': 'language-points', 'count': 5, 'taskRequirements': [instruction], 'groups': groups, 'markingGuideNote': guide},
        figure=crop('ja-2013-ol-2b', 5, [.055, .455, .95, .947], instruction))
    guide = cell('scheme', 7, 3)
    content, discretionary = guide.split(' + ')
    parts = [{'id': f'point-{i}', 'verbatim': content, 'marks': 2, 'permittedMarks': [0, 2]} for i in [1, 2]] + [
        {'id': 'discretionary', 'verbatim': discretionary, 'marks': 1, 'permittedMarks': [0, 1]}]
    add('2C', None, p(6, 5), [{'kind': 'criterion', 'verbatim': UNPRINTED, 'unprinted': True, 'marks': 5,
        'permittedMarks': list(range(6)), 'parts': parts, 'contextNote': guide}], 'japanese-5-6', [6], [7], reading=[6], stem=col('paper', 6, range(4)))


def reading_q3():
    instruction = p(9, 2)
    labels = [english(p(9, row)) for row in range(4, 8)]
    add('3A', 1, instruction + '\n' + p(9, 3) + '\n' + '\n'.join(labels),
        [point(s(7, row, 1), 2, contextNote=label) for row, label in zip(range(7, 11), labels)],
        'japanese-5-1', [9], [7], reading=[8], figure=crop('ja-2013-ol-3a-1', 9, [.065, .025, .9, .26], instruction))
    for roman, qr, sr in [('i', 9, 13), ('ii', 11, 15), ('iii', 13, 17)]:
        answer = s(7, sr)
        if roman == 'ii':
            row = {'kind': 'criterion', 'verbatim': answer, 'marks': 3, 'permittedMarks': [0, 2, 3], 'contextNote': cell('scheme', 7, sr)}
        else: row = point(answer, 3)
        add('3A', 2, without_marker(p(9, qr)), [row], 'japanese-5-1', [9], [7], roman, reading=[8], stem=english(p(9, 8, 1)))
    for roman, qr, sr in [('i', 16, 19), ('ii', 19, 20), ('iii', 22, 21)]:
        # The original bilingual MCQ alternatives retain all four letters.
        prompt = p(9, qr) + '\n' + p(9, qr + 1) + '\n' + p(9, qr + 2)
        add('3A', 3, prompt, [point(s(7, sr, 1), 2)], 'japanese-5-1', [9], [7], roman, reading=[8], stem=english(p(9, 15, 1)))
    instruction = p(10, 2)
    labels = [p(10, row) for row in range(4, 14)]
    answers = [s(7, row, 1) for row in range(23, 27)] + [s(8, row, 2 if row in [2, 3] else 1) for row in range(6)]
    add('3B', None, instruction + '\n' + p(10, 3) + '\n' + '\n'.join(labels), [], 'japanese-5-4', [10], [7, 8], total=10,
        rubric=pool(10, labels, answers, 1, instruction, cell('scheme', 7, 22)), reading=[10],
        figure=crop('ja-2013-ol-3b', 10, [.065, .035, .95, .52], instruction))
    instruction = p(10, 16)
    labels = [p(10, row, 0) for row in range(18, 23)]
    answers = [s(8, row, 1) for row in range(7, 10)] + [sa(8, row) for row in [10, 11]]
    add('3C', 1, instruction + '\n' + p(10, 17) + '\n' + '\n'.join(labels), [], 'japanese-5-5', [10], [8], total=10,
        rubric=pool(5, labels, answers, 2, instruction, cell('scheme', 8, 6)), reading=[10],
        figure=crop('ja-2013-ol-3c-1', 10, [.065, .52, .95, .85], instruction))
    instruction = p(11, 1)
    labels = [p(11, row) for row in range(3, 8)]
    answers = [s(8, 13, 1), sa(8, 14), s(8, 15, 1), s(8, 16, 1), sa(8, 17)]
    guide = cell('scheme', 8, 12) + ' — The scheme labels these particles D; the original paper labels this pool C2. All five original prompts and answers remain together.'
    add('3C', 2, instruction + '\n' + p(11, 2) + '\n' + '\n'.join(labels), [], 'japanese-5-5', [11], [8], total=10,
        rubric=pool(5, labels, answers, 2, instruction, guide), reading=[11],
        figure=crop('ja-2013-ol-3c-2', 11, [.065, .04, .97, .35], instruction))


def writing():
    instruction = col('paper', 12, [2, 3], 290)
    question = instruction + '\n' + '\n'.join(p(12, row) for row in range(4, 21))
    no_reuse = cell('scheme', 9, 1)
    raw = [s(9, row, 1) if row != 9 else sa(9, row) for row in range(2, 12)]
    teacher, year_two = p(12, 20, 0), p(12, 15, 1)
    rows = []
    for i, answer in enumerate(raw, 1):
        label = re.match(r'\([ivx]+\)', cell('scheme', 9, i + 1, 0)).group()
        options = [text.strip() for text in answer.split('/')]
        if i == 9:
            assert options == ['ともだち', 'せんせい', '２年生', 'クラス']
            options = [options[0], teacher, year_two, options[3]]
        note = label + ' — ' + no_reuse
        if i in [2, 5, 9]:
            note += f' — Original bank: {teacher}, {year_two}; scheme (ix): {raw[8]}. The local spellings せんせい/先生 and ２年生/二年生 identify the same respective bank entries; each may be used only once.'
        rows.append(anyn(options, 1, 3, contextNote=note))
    found = add('4', None, question, rows, 'japanese-5-7', [12], [9], reading=[12],
        figure=crop('ja-2013-ol-4', 12, [.065, .025, .95, .957], instruction))
    found['taskGroups'] = [{'sourceCardId': found['id'] + f'-blank-{i+1}', 'label': re.match(r'\([ivx]+\)', row['contextNote']).group(),
        'marks': 3, 'rowIds': [row['id']]} for i, row in enumerate(found['rows'])]
    for answer, row_ids, pr, pg in [(teacher, ['r-5', 'r-9'], 20, 0), (year_two, ['r-2', 'r-9'], 15, 1)]:
        BINDINGS.append({'cardId': found['id'], 'answer': answer, 'rowIds': row_ids,
            'paperSelector': {'document': 'paper', 'page': 12, 'row': pr, 'group': pg, 'text': answer},
            'schemeSelectors': [{'document': 'scheme', 'page': 9, 'row': 10, 'group': 1, 'text': cell('scheme', 9, 10, 1)},
                                {'document': 'scheme', 'page': 9, 'row': 1, 'group': None, 'text': no_reuse}]})
    instruction = p(13, 3)
    labels = [p(13, row) for row in range(4, 11)]
    content_bands = [{'label': s(9, row), 'marks': marks, 'guidance': [s(9, row, 1)]}
        for row, marks in [(26, [1]), (25, [2]), (24, [3, 4]), (23, [5])]]
    expression_bands = [{'label': s(10, first), 'marks': marks, 'guidance': [joined_selector('scheme', 10, [(first, 1)] + [(row, 0) for row in rest])]}
        for first, rest, marks in [(11, range(12, 18), [1]), (18, range(19, 25), [2, 3]), (25, range(26, 32), [4, 5])]]
    cap = cell('scheme', 9, 28) + ' ' + cell('scheme', 10, 0)
    groups = []
    for i, label in enumerate(labels, 1):
        guidance = [s(9, 14)] + ([cell('scheme', 9, 20)] if i == 6 else [])
        criteria = [{'id': f'item-{i}-content', 'label': s(9, 22).removesuffix(':'), 'maxMarks': 5, 'permittedMarks': list(range(6)), 'guidance': guidance, 'bands': content_bands},
            {'id': f'item-{i}-expression', 'label': s(9, 27).removesuffix(':'), 'maxMarks': 5, 'permittedMarks': list(range(6)), 'guidance': [cap], 'bands': expression_bands,
             'limits': [{'id': f'item-{i}-low-content', 'maxMarks': 3, 'when': {'any': [{'criterionIds': [f'item-{i}-content'], 'atMost': 3}]}, 'guidance': [cap]}]}]
        groups.append({'id': f'item-{i}', 'label': label, 'rows': [], 'criteria': criteria})
    guide = cell('scheme', 9, 13) + ' ' + cell('scheme', 9, 14) + ' ' + cap + ' ' + joined_selector('scheme', 10, [(row, 0) for row in range(2, 10)]) + ' ' + joined_selector('scheme', 10, [(32, 0), (33, 0)])
    guide += ' — For (vi), the source gives content maxima of 2 and 3 and also the common whole-response content scale 1, 2, 3–4 and 5. Use that complete-response scale; no per-component partial allocation is published. Each expression cap depends only on that response’s content.'
    add('5', None, instruction + '\n' + '\n'.join(labels), [], 'japanese-5-7', [13], [9, 10], total=50, reading=[13],
        rubric={'system': 'language-points', 'count': 5, 'taskRequirements': [instruction], 'groups': groups, 'markingGuideNote': guide},
        figure=crop('ja-2013-ol-5', 13, [.055, .03, .97, .94], instruction))


def listening():
    def listen(section, q, roman, qr, rows, sp=None):
        page = {'A': 2, 'B': 3, 'C': 4, 'D': 5}[section]
        question = re.sub(r'^(?:\d+\.?\s*)?(?:\([ivx]+\)\s*)?', '', col('aural', page, qr)).strip()
        card = add('L' + section, q, question, rows, 'japanese-6-2' if section == 'B' else 'japanese-6-1' if section == 'D' else 'japanese-6-0',
            [page], [sp or (3 if section in 'AB' else 4)], roman, reading=[page])
        card['stem'] = col('aural', page, range(1, {'A': 8, 'B': 9, 'C': 8, 'D': 9}[section]))
        if section == 'B': card['stem'] += '\n' + col('aural', page, [9, 10] if q == 1 else [27])
        if section == 'C': card['stem'] += '\n' + col('aural', page, {1: [8, 9], 2: [23], 3: [36]}[q])
        return card
    for q, roman, qr, sr, sg in [(1, 'i', [8], 3, 2), (1, 'ii', range(10, 15), 4, 1),
        (2, 'i', range(15, 20), 5, 2), (2, 'ii', range(20, 25), 6, 1),
        (3, 'i', range(25, 30), 7, 2), (3, 'ii', [30], 8, 1),
        (4, 'i', range(32, 37), 9, 2), (4, 'ii', [37], 10, 1)]:
        listen('A', q, roman, qr, [point(s(3, sr, sg), 3)])
    for roman, qr, sr, sg in [('i', range(11, 16), 13, 1), ('ii', range(16, 22), 14, 1), ('iii', range(22, 27), 15, 0)]:
        listen('B', 1, roman, qr, [point(without_marker(s(3, sr, sg)), 3)])
    listen('B', 2, 'i', [28], [point(s(3, 17, 1), 1)])
    listen('B', 2, 'ii', [30], [anyn(sa(3, 18).split(' / '), 1, 4, contextNote=cell('scheme', 3, 19))])
    for roman, qr, sr in [('iii', range(32, 37), 20), ('iv', range(37, 42), 21)]: listen('B', 2, roman, qr, [point(sa(3, sr), 4)])
    guide = cell('scheme', 3, 22, 1)
    number = re.search(r'\(06-81\s+0\) – \(4\s+545\)', guide).group().translate(str.maketrans('', '', '() '))
    digits = re.sub(r'\D', '', number)
    rows = [point(digits[position - 1], 1, contextNote=f'Missing digit {i+1} (position {position} in {number}). {guide} — Only the four blank digits score; the printed 06-81 and 4 are given.') for i, position in enumerate([5, 7, 8, 9])]
    phone = listen('B', 2, 'v', [42, 43], rows)
    phone['questionFigureKey'] = crop('ja-2013-ol-lb-2-v', 3, [.035, .887, .97, .972], phone['questionText'], 'aural')
    for q, roman, qr, sr in [(1, 'i', range(10, 15), 2), (1, 'ii', range(15, 21), 3),
        (2, 'i', range(24, 29), 8), (2, 'ii', range(29, 34), 9), (3, 'i', range(37, 42), 14)]:
        listen('C', q, roman, qr, [point(s(4, sr, 1), 3)])
    listen('C', 1, 'iii', [21], [anyn(re.sub(r'\s*\(any one\)$', '', s(4, 5)).split('/'), 1, 4)])
    listen('C', 2, 'iii', [34], [anyn((s(4, 10, 1) + ' ' + s(4, 11)).split('/'), 1, 3, contextNote=cell('scheme', 4, 12))])
    listen('C', 3, 'ii', [42], [anyn((s(4, 15, 1) + ' ' + s(4, 16)).split('/'), 1, 4, contextNote=cell('scheme', 4, 17))])
    for q, qr, sr, marks in [(1, [9], 20, 1), (2, [11], 22, 3), (3, [15], 24, 3), (4, range(18, 23), 26, 3), (5, [23, 24], 28, 3)]:
        listen('D', q, '', qr, [point(s(4, sr), marks)])
    listen('D', 6, '', range(26, 31), [point(s(5, 1), 3)], 5)
    listen('D', 7, '', [31], [anyn((s(5, 3) + ' ' + s(5, 4)).split('/'), 1, 3)], 5)
    listen('D', 8, '', [34, 35], [{'kind': 'criterion', 'verbatim': s(5, 6), 'marks': 3, 'permittedMarks': [0, 1, 3], 'contextNote': cell('scheme', 5, 6) + ' ' + cell('scheme', 5, 7)}], 5)
    listen('D', 9, '', [37], [point(s(5, 9), 2)], 5)


def build():
    reading_q1(); reading_q2(); reading_q3(); writing(); listening()
    census = json.loads((Path(__file__).parent / 'reviews/japanese-2013-ol-census.json').read_text())
    expected = {'ja-2013-ol-' + '-'.join(str(part).lower() for part in task['key'] if part is not None): task for task in census['tasks']}
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
    assert len(CARDS) == 51 and sum(card['totalMarks'] for card in CARDS) == 300
    assert sum('answerLanguageRule' in card for card in CARDS) == 49
    assert not any(card['id'] in ORIGINAL_IDS for card in CARDS)
    return {'subjectId': 'japanese', 'sitting': '2013-ol', 'reviewedAt': '2026-11-10',
        'sources': [{'document': name, 'path': str(path.relative_to(ROOT)), 'sha256': HASHES[name], 'pagesReviewed': list(range(1, len(DOCS[name]) + 1))} for name, path in PATHS.items()],
        'cards': CARDS, 'selectors': EVIDENCE, 'status': 'source-reviewed-browser-qa-pending', 'choiceAnalysis': census['choiceBoundaries'], 'consolidations': [], 'sourceAnswerBindings': BINDINGS}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('--write', action='store_true'); args = parser.parse_args()
    result = build()
    if args.write:
        text = '# Original text with furigana folded at its printed character\n'
        for i, page in enumerate(DOCS['scheme']): text += f'\n## Physical page {i+1}\n\n' + '\n'.join(' '.join(g[2] for g in row) for row in page_rows(page)) + '\n'
        PATHS['scheme'].with_suffix('.md').write_text(text.rstrip() + '\n')
        (ROOT / 'scripts/markbank/authoring/reviews/japanese-2013-ol.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
        manifest = ROOT / 'components/MarkBank/figures-japanese.json'; previous = json.loads(manifest.read_text()); previous.update(FIGURES)
        manifest.write_text(json.dumps(previous, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'cards': len(CARDS), 'marks': sum(c['totalMarks'] for c in CARDS), 'figures': len(FIGURES)}, indent=2))
