#!/usr/bin/env python3
"""Publish the independently censused 2019 Ordinary sitting from PDF selectors.

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
    'paper': ROOT / 'examiner-reports/japanese/papers/2019-ol-000-paper.pdf',
    'aural': ROOT / 'examiner-reports/japanese/papers/2019-ol-A00-paper.pdf',
    'scheme': ROOT / 'examiner-reports/japanese/schemes/2019-ol.pdf',
}
HASHES = {
    'paper': '00e95d69d8ba77dcdb1e9650678e2120708bbba9fdf9cd1c395845ad11cd38e0',
    'aural': 'da32fc28efe1458022116587a0b9cf72cff589496459bfdab41457458e752639',
    'scheme': 'be1782b438ce07304d7c624fde74c23d533b6f4a3ba0522613b38571d6c4b0f8',
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
    return {'kind': 'source-text', 'label': '2019 Japanese Ordinary Level', 'title': 'Original examination material',
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
    cid = f'ja-2019-ol-{section.lower()}' + (f'-{q}' if q is not None else '') + (f'-{suffix}' if suffix else '')
    ref = f'2019 OL Section {section}' + (f' Q{q}' if q is not None else ' Q' if suffix else '') + ''.join(f'({part})' for part in suffix.split('-') if part)
    listening = section.startswith('L')
    card = {'id': cid, 'source': 'sec', 'subjectId': 'japanese', 'specVersion': 'lc-japanese-syllabus',
            'kind': 'rubric' if rubric else 'question', 'level': 'ordinary', 'year': 2019,
            'section': section[1:] if listening else section[0] if section[0] in '1234' else 'Q5',
            'topicId': topic, 'conceptId': concept_for(question, cid), 'questionRef': ref,
            'questionText': question, 'totalMarks': total if total is not None else sum(map(worth, rows)),
            'qa': {'gates': ['verbatim', 'tariff', 'figure'], 'humanReviewedBy': 'agent-verified', 'humanReviewedAt': '2026-11-09'},
            'sourceEvidence': {'component': 'aural' if listening else 'paper', 'paperPages': pp, 'schemePages': sp},
            'schemeCitation': 'Marking points quoted from the SEC marking scheme, Japanese 2019 Ordinary Level — © State Examinations Commission.'}
    if cid in ORIGINAL_IDS:
        card['qa']['gates'].append('reviewed-card-correction')
    if listening or section[0] in '123':
        rule_page = 10 if listening else 4
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
    labels = [re.sub(r'_+', '', col('paper', 3, [row])).strip() for row in range(2, 7)]
    add('1', 1, instruction + '\n' + col('paper', 3, [1]) + '\n' + '\n'.join(labels),
        [point(s(4, row, 2), 2, contextNote=label) for label, row in zip(labels, range(4, 9))],
        'japanese-5-0', [3], [4], reading=[2, 3])
    for q, qr, rows in [(2, [8, 9], [anyn(options(4, [10], separator='/'), 2, 2, [2, 1])]),
                        (3, [12, 13], [point(s(4, 12), 2)]),
                        (4, [15], [anyn(options(4, [14], separator='/'), 2, 2, [2, 1])])]:
        add('1', q, without_marker(col('paper', 3, qr)), rows, 'japanese-5-0', [3], [4], reading=[2], stem=p(3, 7, 1))
    instruction = without_marker(col('paper', 3, [18]))
    headers = [p(3, 19, group) for group in [3, 4, 5]]
    events = [p(3, row) for row in [21, 23]]
    rows = []
    for event, parts in zip(events, [[(17, 1), (18, 0), (17, 2)], [(19, 1), (21, 0), (19, 2)]]):
        rows.extend(point(s(4, row, group), contextNote=event + ' — ' + headers[1 if i < 2 else 2]) for i, (row, group) in enumerate(parts))
    table = add('1', 5, instruction + '\n' + '\n'.join(headers + events), rows, 'japanese-5-0', [3], [4], reading=[2, 3],
                figure=crop('ja-2019-ol-1-5', 3, [.52, .56, .97, .75], instruction))
    table['taskGroups'] = [{'sourceCardId': table['id'] + f'-event-{i + 1}', 'label': event, 'marks': 3,
                            'rowIds': [row['id'] for row in table['rows'][i * 3:i * 3 + 3]]} for i, event in enumerate(events)]
    for roman, qr, answer in [('i', 25, s(4, 23)), ('ii', 27, s(4, 25))]:
        question = re.sub(r'^(?:6\.\s*)?\([ivx]+\)\s*', '', col('paper', 3, [qr]))
        add('1', 6, question, [point(answer, 2)], 'japanese-5-0', [3], [4], roman, reading=[2])
    start = re.search(r'6$', s(4, 26)).group()
    finish = re.search(r'8', s(4, 27)).group()
    add('1', 6, without_marker(col('paper', 3, [29])), [point(start), point(finish)], 'japanese-5-0', [3], [4], 'iii', reading=[2])
    for q, qr, rows in [(1, [1], [point(s(5, 3), 2)]), (2, [5], [point(s(5, 5), 3)]),
                        (3, [8], [point(s(5, 7), 2)]), (4, [11, 13], [anyn(options(5, [9], separator='/'), 2, 2)]),
                        (5, [19], [anyn(options(5, [11], separator=','), 2, 2)])]:
        add('2A', q, without_marker(col('paper', 5, qr)), rows, 'japanese-5-2', [5], [5], reading=[4], stem=col('paper', 5, [0]))
    instruction = english(' '.join(p(5, row) for row in range(24, 28)))
    labels = [re.match(r'\([ivx]+\)', p(5, row)).group() + ' ' + p(5, row + 1) for row in [32, 35, 38, 41, 44]]
    groups = []
    for i, row in enumerate([13, 15, 17, 19, 21]):
        quote = re.sub(r'\s*2 marks$', '', s(5, row + 1))
        groups.append({'id': f'item-{i + 1}', 'label': labels[i], 'rows': [
            {'id': 'true-false', 'text': s(5, row, 1), 'marks': 1}, {'id': 'quote', 'text': quote, 'marks': 2}]})
    add('2B', None, instruction + '\n' + '\n'.join(labels), [], 'japanese-5-2', [5], [5], total=15, reading=[4, 5],
        rubric={'system': 'language-points', 'count': 5, 'taskRequirements': [instruction], 'groups': groups, 'markingGuideNote': cell('scheme', 5, 12)},
        figure=crop('ja-2019-ol-2b', 5, [.075, .43, .97, .91], instruction))
    instruction = p(6, 13)
    labels = [p(6, row) for row in range(15, 25)]
    answers = [s(5, row, 1) + ' (' + s(5, row, 2) + ')' if row not in [30, 31]
               else without_marker(s(5, row)) + ' (' + s(5, row, 1) + ')' for row in range(24, 34)]
    add('2C', None, instruction + '\n' + p(6, 14) + '\n' + '\n'.join(labels), [], 'japanese-5-4', [6], [5], total=10, reading=[6],
        rubric=pool(10, labels, answers, 1, instruction, cell('scheme', 5, 23)),
        figure=crop('ja-2019-ol-2c', 6, [.075, .50, .97, .94], instruction))
    question = english(' '.join(p(7, row) for row in [3, 4]))
    allocation = cell('scheme', 6, 2)
    point_label = re.search(r'\bpoints\b', allocation).group()
    parts = [{'id': f'point-{i}', 'verbatim': f'{i}. {point_label}', 'marks': 2, 'permittedMarks': [0, 2]} for i in [1, 2]]
    parts.append({'id': 'discretionary', 'verbatim': re.search(r'discretionary mark', allocation).group(), 'marks': 1, 'permittedMarks': [0, 1]})
    add('2D', None, question, [{'kind': 'criterion', 'verbatim': UNPRINTED, 'unprinted': True, 'marks': 5,
        'permittedMarks': list(range(6)), 'parts': parts, 'contextNote': allocation}], 'japanese-5-6', [7], [6],
        stem=english(' '.join(p(7, row) for row in [0, 1, 2])))
    dad, car = s(6, 8).split('(1 mark)')
    for q, qr, rows in [(1, [1], [point(s(6, 6), 2)]), (2, [3], [point(dad.strip()), point(car.strip(), 2)]),
                        (3, [5], [point(s(6, 10), 3)])]:
        add('3A', q, without_marker(col('paper', 9, qr)), rows, 'japanese-5-1', [9], [6], reading=[8], stem=p(9, 0, 1))
    for roman, qr, sr, sg in [('i', range(10, 17), 12, 1), ('ii', range(17, 26), 13, 1),
                              ('iii', range(26, 34), 14, 0), ('iv', range(34, 43), 15, 1)]:
        answer = s(6, sr, sg)
        if roman == 'iii':
            answer = answer[answer.index('(d)'):]
        add('3A', 4, without_marker(col('paper', 9, qr)), [point(answer, 2)], 'japanese-5-1', [9], [6], roman,
            reading=[8], stem=without_marker(col('paper', 9, [7, 8])))
    instruction = english(p(10, 0, 1))
    labels = [p(10, row) for row in [1, 3, 5]]
    add('3A', 5, instruction + '\n' + '\n'.join(labels), [], 'japanese-5-1', [10], [6], total=9, reading=[8, 10],
        rubric=pool(3, labels, [s(6, row) for row in [18, 20, 22]], 3, instruction, cell('scheme', 6, 16)))
    for q, qr, lr, example, sr, rr, region in [
        (1, [8, 9], range(11, 16), 10, 1, range(2, 7), [.075, .325, .97, .63]),
        (2, [16, 17], range(19, 24), 18, 7, range(8, 13), [.075, .63, .97, .94]),
    ]:
        instruction = english(' '.join(p(10, row) for row in qr))
        labels = [p(10, row) for row in lr]
        add('3B', q, instruction + '\n' + p(10, example) + '\n' + '\n'.join(labels), [], 'japanese-5-5', [10], [7],
            rubric=pool(5, labels, [s(7, row, 1) for row in rr], 2, instruction, cell('scheme', 7, sr)), total=10, reading=[10],
            figure=crop(f'ja-2019-ol-3b-{q}', 10, region, instruction))


def writing():
    instruction = english(' '.join(p(11, row) for row in [2, 3, 4]))
    question = instruction + '\n' + '\n'.join(p(11, row) for row in range(5, 20))
    labels = [s(8, row, 0) for row in range(2, 12)]
    answers = [s(8, row, 1) for row in range(2, 12)]
    add('4', None, question, [], 'japanese-5-7', [11], [8],
        rubric=pool(10, labels, answers, 3, instruction, cell('scheme', 8, 1)
                    + ' — Preserve both published answers for(viii). The paper says each word may be used only once: do not award the same パーティー token twice in(viii) and(ix).'), total=30,
        reading=[11], figure=crop('ja-2019-ol-4', 11, [.075, .06, .97, .94], instruction))
    instruction = english(' '.join(p(12, row) for row in [1, 2, 3]))
    labels = [p(12, row) for row in range(4, 11)]
    content_bands = [{'label': s(8, row), 'marks': marks, 'guidance': [s(8, row, 1)]}
                     for row, marks in [(25, [1]), (24, [2, 3]), (23, [4, 5])]]
    expression_bands = [{'label': s(9, first), 'marks': marks,
                         'guidance': [s(9, first, 1) + ' ' + ' '.join(s(9, row) for row in rest)]}
                        for first, rest, marks in [(12, range(13, 19), [1]), (19, range(20, 27), [2, 3]), (27, range(28, 34), [4, 5])]]
    groups = []
    for i, label in enumerate(labels, 1):
        groups.append({'id': f'item-{i}', 'label': label, 'rows': [], 'criteria': [
            {'id': f'item-{i}-content', 'label': s(8, 22).removesuffix(':'), 'maxMarks': 5,
             'permittedMarks': list(range(6)), 'guidance': [s(8, 14)], 'bands': content_bands},
            {'id': f'item-{i}-expression', 'label': s(9, 0).removesuffix(':'), 'maxMarks': 5,
             'permittedMarks': list(range(6)), 'guidance': [s(9, 1)], 'bands': expression_bands},
        ]})
    rubric = {'system': 'language-points', 'count': 5, 'taskRequirements': [instruction], 'groups': groups,
              'markingGuideNote': s(8, 13) + ' ' + s(8, 14) + ' ' + s(9, 34) + ' ' + s(9, 35)}
    add('5', None, instruction + '\n' + '\n'.join(labels), [], 'japanese-5-7', [12], [8, 9], rubric=rubric, total=50,
        reading=[12], figure=crop('ja-2019-ol-5', 12, [.05, .04, .97, .945], instruction))


def listening():
    conflict = cell('scheme', 10, 11) + ' — ' + cell('scheme', 10, 12) + ' — The scheme gives each of the five Hotel Okura responses 4 marks (20), although its subtotal says 18; Part B therefore adds to 28 rather than its heading 26. Local listening tariffs add to 102 rather than the printed 100. These controls retain the explicit per-answer awards.'

    def listen(section, q, roman, qr, answers):
        page = {'A': 2, 'B': 3, 'C': 4, 'D': 5}[section]
        topic = {'A': 'japanese-6-1', 'B': 'japanese-6-2', 'C': 'japanese-6-0', 'D': 'japanese-6-0'}[section]
        question = re.sub(r'^(?:\d+\.?\s*)?(?:\([ivx]+\)\s*)?', '', col('aural', page, qr, 290)).strip()
        card = add('L' + section, q, question, answers, topic, [page], [10 if section in 'AB' else 11], roman, reading=[page])
        if section == 'C':
            card['stem'] = 'You' + cell('aural', page, 1).split('You', 1)[1] + ' and' + cell('aural', page, 2).split('and', 1)[1] + ' ' + col('aural', page, [3, 4, 5], 290)
            card['stem'] += '\n' + col('aural', page, [6 if q == 1 else 28], 290)
        else:
            card['stem'] = col('aural', page, range(1, 5) if section == 'A' else range(1, 6) if section == 'B' else range(1, 9))
        if section == 'B':
            card['stem'] += '\n' + col('aural', page, [6 if q == 1 else 24])
            for row in card['rows']:
                row['contextNote'] = row.get('contextNote', '') + ' — ' + conflict
        return card

    for q, roman, qr, sr, sg, marks in [
        (1, 'i', [5], 3, 2, 2), (1, 'ii', range(7, 12), 4, 1, 4), (1, 'iii', range(12, 18), 5, 1, 4),
        (2, 'i', [18], 6, 2, 2), (2, 'ii', range(21, 28), 7, 1, 4), (2, 'iii', range(28, 33), 8, 1, 4),
        (3, 'i', [34], 9, 2, 2), (3, 'ii', range(36, 41), 10, 1, 4),
    ]:
        listen('A', q, roman, qr, [point(s(10, sr, sg), marks)])
    listen('B', 1, 'i', range(7, 12), [point(s(10, 13, 1), 4)])
    facilities = joined_selector('scheme', 10, [(14, 1), (15, 0)])
    facilities = re.sub(r'\s*\(any.*$', '', facilities)
    listen('B', 1, 'ii', [12], [anyn([text.strip() for text in facilities.split('/')], 2, 2)])
    listen('B', 1, 'iii', range(14, 19), [point(s(10, 16, 1), 4)])
    listen('B', 1, 'iv', [19, 20], [point(s(10, 17, 1), 4)])
    phone_source = s(10, 18, 1)
    number = phone_source.split(' (')[0]
    digits = number.replace('-', '')
    rows = [point(digits[position - 1], contextNote=f'Missing digit {index + 1} (position {position} in {number}). {phone_source} — The original paper calls this(v), misprinted(vi) in the scheme. Only the four missing digits score.')
            for index, position in enumerate([4, 5, 7, 8])]
    phone = listen('B', 1, 'v', [22], rows)
    phone['questionFigureKey'] = crop('ja-2019-ol-lb-1-v', 3, [.50, .53, .93, .612], phone['questionText'], 'aural')
    listen('B', 2, 'i', range(25, 35), [point(s(10, 20, 1), 4)])
    listen('B', 2, 'ii', range(35, 42), [point(joined_selector('scheme', 10, [(21, 1), (22, 0)]), 4)])
    for q, roman, qr, sr in [(1, 'i', range(7, 12), 2), (1, 'ii', range(12, 17), 3),
                            (1, 'iii', range(17, 22), 4), (1, 'iv', range(22, 28), 5),
                            (2, 'i', range(29, 34), 7), (2, 'ii', range(34, 39), 8)]:
        listen('C', q, roman, qr, [point(s(11, sr, 1), 4)])
    for roman, qr, sr, marks in [('i', range(9, 16), 10, 4), ('ii', [16], 11, 2),
                                ('iii', range(19, 24), 12, 4), ('iv', range(24, 29), 14, 4),
                                ('v', range(29, 35), 15, 4), ('vi', [35], 16, 2), ('vii', range(37, 42), 17, 4)]:
        listen('D', None, roman, qr, [point(s(11, sr, 1), marks)])


def build():
    reading()
    writing()
    listening()
    census = json.loads((Path(__file__).parent / 'reviews/japanese-2019-ol-census.json').read_text())
    expected = {'ja-2019-ol-' + '-'.join(str(part).lower() for part in task['key'] if part is not None): task for task in census['tasks']}
    assert set(expected) == {card['id'] for card in CARDS}
    for card in CARDS:
        task = expected[card['id']]
        assert card['totalMarks'] == task['marks'], (card['id'], card['totalMarks'], task['marks'])
        assert card['sourceEvidence']['paperPages'] == task['paperPages']
        assert card['sourceEvidence']['schemePages'] == task['schemePages']
    assert len(CARDS) == 56
    assert sum(card['totalMarks'] for card in CARDS) == 302
    assert sum('answerLanguageRule' in card for card in CARDS) == 54
    assert not any(card['id'] in ORIGINAL_IDS for card in CARDS)
    return {'subjectId': 'japanese', 'sitting': '2019-ol', 'reviewedAt': '2026-11-09',
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
        (ROOT / 'scripts/markbank/authoring/reviews/japanese-2019-ol.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
        manifest = ROOT / 'components/MarkBank/figures-japanese.json'
        previous = json.loads(manifest.read_text())
        previous.update(FIGURES)
        manifest.write_text(json.dumps(previous, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'cards': len(CARDS), 'marks': sum(card['totalMarks'] for card in CARDS), 'figures': len(FIGURES)}, indent=2))
