#!/usr/bin/env python3
"""Publish the independently censused 2014 Ordinary sitting from PDF selectors.

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
    'paper': ROOT / 'examiner-reports/japanese/papers/2014-ol-000-paper.pdf',
    'aural': ROOT / 'examiner-reports/japanese/papers/2014-ol-A00-paper.pdf',
    'scheme': ROOT / 'examiner-reports/japanese/schemes/2014-ol.pdf',
}
HASHES = {
    'paper': '64eb767e0866b2605ea1cc2eaeb9cb1979e9ed5c2c7e5a4bb565e5306bde67c4',
    'aural': 'f6e50ff8e32cbd3081f71533d63bb266dc04ea97d18a1997d470ccf6ff6cad9f',
    'scheme': '69355ed48177aeaec82eb22b281381acfe9cea433c3a39a8791b88c662472f9f',
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
    return {'kind': 'source-text', 'label': '2014 Japanese Ordinary Level', 'title': 'Original examination material',
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
    cid = f'ja-2014-ol-{section.lower()}' + (f'-{q}' if q is not None else '') + (f'-{suffix}' if suffix else '')
    ref = f'2014 OL Section {section}' + (f' Q{q}' if q is not None else ' Q' if suffix else '') + ''.join(f'({part})' for part in suffix.split('-') if part)
    listening = section.startswith('L')
    card = {'id': cid, 'source': 'sec', 'subjectId': 'japanese', 'specVersion': 'lc-japanese-syllabus',
            'kind': 'rubric' if rubric else 'question', 'level': 'ordinary', 'year': 2014,
            'section': section[1:] if listening else section[0] if section[0] in '1234' else 'Q5',
            'topicId': topic, 'conceptId': concept_for(question, cid), 'questionRef': ref,
            'questionText': question, 'totalMarks': total if total is not None else sum(map(worth, rows)),
            'qa': {'gates': ['verbatim', 'tariff', 'figure'], 'humanReviewedBy': 'agent-verified', 'humanReviewedAt': '2026-11-10'},
            'sourceEvidence': {'component': 'aural' if listening else 'paper', 'paperPages': pp, 'schemePages': sp},
            'schemeCitation': 'Marking points quoted from the SEC marking scheme, Japanese 2014 Ordinary Level — © State Examinations Commission.'}
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


def find_row(doc, page, phrase):
    found = [i for i, row in enumerate(ROWS[doc][page - 1]) if phrase in ' '.join(group[2] for group in row)]
    assert len(found) == 1, (doc, page, phrase, found)
    return found[0]



def reading_q1():
    stem = p(3, 1)
    instruction = without_marker(col('paper', 3, [2]))
    labels = [clean_label(col('paper', 3, [row])) for row in range(4, 9)]
    add('1', 1, instruction + '\n' + col('paper', 3, [3]) + '\n' + '\n'.join(labels),
        [point(s(5, row, 2), 2, contextNote=label) for row, label in zip(range(4, 9), labels)],
        'japanese-5-0', [3], [5], reading=[2], stem=stem)
    labels = [clean_label(col('paper', 3, [row])) for row in range(12, 17)]
    add('1', 2, without_marker(col('paper', 3, [9])) + '\n' + col('paper', 3, [11]) + '\n' + '\n'.join(labels),
        [point(s(5, row, 2), 2, contextNote=label) for row, label in zip(range(10, 15), labels)],
        'japanese-5-0', [3], [5], reading=[2], stem=stem)
    colours = re.findall(r'(\w+)\s*\(2 marks\)', cell('scheme', 5, 16, 0))
    assert len(colours) == 2
    add('1', 3, without_marker(col('paper', 3, [17, 18])), [anyn(colours, 2, 2)],
        'japanese-5-0', [3], [5], 'i', reading=[2], stem=stem)
    labels = [clean_label(col('paper', 3, [row])) for row in [24, 25]]
    add('1', 3, without_marker(col('paper', 3, [21, 22])) + '\n' + col('paper', 3, [23]) + '\n' + '\n'.join(labels),
        [point(s(5, row, 1), 2, contextNote=label) for row, label in zip([18, 19], labels)],
        'japanese-5-0', [3], [5], 'ii', reading=[2], stem=stem)
    add('1', 4, without_marker(col('paper', 3, [26])), [point(s(5, 21), 2)],
        'japanese-5-0', [3], [5], reading=[2], stem=stem)


def reading_q2_profiles():
    instruction = without_marker(col('paper', 5, [2]))
    for roman, pr, sr in [('i', 3, 3), ('ii', 4, 4)]:
        add('2A', 1, instruction + '\n' + clean_label(col('paper', 5, [pr])), [point(s(6, sr, 2), 3)],
            'japanese-5-2', [5], [6], roman, reading=[4], stem=p(5, 1, 1))
    add('2A', 2, without_marker(col('paper', 5, [5])) + '\n' + col('paper', 5, [6, 7]), [point(s(6, 5, 1), 2)],
        'japanese-5-2', [5], [6], reading=[4], stem=p(5, 1, 1))
    instruction = without_marker(col('paper', 5, [8, 9]))
    groups = []
    for i, row in enumerate(range(8, 12), 1):
        names = sa(6, row).split()
        assert len(names) == 2
        groups.append({'id': f'person-{i}', 'label': ' '.join(names), 'rows': [
            {'id': 'surname', 'text': names[0], 'marks': 1}, {'id': 'first-name', 'text': names[1], 'marks': 1},
            {'id': 'date', 'text': s(6, row, 1), 'marks': 1}, {'id': 'place', 'text': s(6, row, 2), 'marks': 2}]})
    guide = joined_selector('scheme', 6, [(12, 0), (13, 0)])
    rubric = {'system': 'language-points', 'count': 2, 'taskRequirements': [instruction], 'groups': groups,
              'markingGuideNote': guide + ' — Choose two complete people profiles. Okawa Misao is the given example and carries no marks.'}
    add('2A', 3, instruction + '\n' + p(5, 11) + ' ' + p(5, 12) + '\n' + p(5, 13), [],
        'japanese-5-2', [5], [6], reading=[4, 5], stem=p(5, 1, 1), rubric=rubric, total=10,
        figure=crop('ja-2014-ol-2a-3', 5, [.07, .30, .96, .54], instruction))


def reading_q2_remaining():
    instruction = p(5, 18) + ' ' + p(5, 19)
    labels = [p(5, 23, 0) + ' ' + english(p(5, 23, 1)), p(5, 25, 0) + ' ' + english(p(5, 25, 1)),
              english(p(5, 27)), english(p(5, 29)) + ' ' + p(5, 30), p(5, 32, 0) + ' ' + english(p(5, 32, 1))]
    groups = []
    for i, (label, phrase) in enumerate(zip(labels, ['She was born in Tokyo.', 'Her family had a Kimono shop.',
            'She has three children.', 'Her hobby is knitting.', 'She likes to eat meat.']), 1):
        row = find_row('scheme', 6, phrase)
        truth = cell('scheme', 6, row, len(ROWS['scheme'][5][row]) - 1)
        quote_row = row + (1 if i == 4 else 2)
        quote = re.sub(r'\s*1 mark$', '', s(6, quote_row)).strip()
        assert quote and not any(ord(ch) < 32 for ch in quote)
        groups.append({'id': f'item-{i}', 'label': label, 'rows': [
            {'id': 'true-false', 'text': truth, 'marks': 1}, {'id': 'quote', 'text': quote, 'marks': 1}]})
    add('2A', 4, instruction + '\n' + '\n'.join(labels), [], 'japanese-5-2', [5], [6], reading=[4, 5],
        total=10, rubric={'system': 'language-points', 'count': 5, 'taskRequirements': [instruction], 'groups': groups,
                         'markingGuideNote': cell('scheme', 6, 14) + ' — Each required decision and its supporting quotation have one printed mark each. The given Okawa age example is unpriced.'},
        figure=crop('ja-2014-ol-2a-4', 5, [.07, .555, .97, .961], instruction))
    labels = [p(6, row) for row in range(19, 29)]
    answers = [s(7, row, 1 if row == 8 else 2) for row in range(1, 11)]
    instruction = without_marker(p(6, 16))
    add('2B', None, instruction + '\n' + p(6, 17) + ' ' + p(6, 18) + '\n' + '\n'.join(labels), [],
        'japanese-5-4', [6], [7], total=10, reading=[6], rubric=pool(10, labels, answers, 1, instruction, cell('scheme', 7, 0)),
        figure=crop('ja-2014-ol-2b', 6, [.06, .51, .96, .95], instruction))
    instruction = p(7, 2)
    labels = [clean_label(p(7, row)) for row in range(4, 9)]
    answers = [s(7, 13, 2), s(7, 14, 2) + s(7, 15), s(7, 16, 2), s(7, 17, 2), s(7, 18, 2)]
    add('2C', 1, instruction + '\n' + p(7, 3) + '\n' + '\n'.join(labels), [], 'japanese-5-5', [7], [7],
        reading=[7], total=10, rubric=pool(5, labels, answers, 2, instruction, cell('scheme', 7, 12)),
        figure=crop('ja-2014-ol-2c-1', 7, [.07, .04, .96, .37], instruction))
    instruction = p(7, 10)
    labels = [p(7, row) for row in range(12, 17)]
    answers = [sa(7, row) for row in range(20, 25)]
    add('2C', 2, instruction + '\n' + p(7, 11) + '\n' + '\n'.join(labels), [], 'japanese-5-5', [7], [7],
        reading=[7], total=10, rubric=pool(5, labels, answers, 2, instruction, cell('scheme', 7, 19)),
        figure=crop('ja-2014-ol-2c-2', 7, [.07, .39, .97, .70], instruction))
    guide = cell('scheme', 7, 28)
    content, discretionary = guide.split(' + ')
    parts = [{'id': 'point', 'verbatim': content, 'marks': 2, 'permittedMarks': [0, 2]},
             {'id': 'discretionary', 'verbatim': discretionary, 'marks': 1, 'permittedMarks': [0, 1]}]
    add('2D', None, p(8, 5), [{'kind': 'criterion', 'verbatim': UNPRINTED, 'unprinted': True, 'marks': 3, 'permittedMarks': list(range(4)),
                             'parts': parts, 'contextNote': guide}], 'japanese-5-6', [8], [7], reading=[8], stem=p(8, 2) + ' ' + p(8, 3))


def reading_q3():
    instruction = without_marker(col('paper', 11, [0, 1]))
    labels = [col('paper', 11, [row]) for row in [2, 4, 6, 8]]
    add('3', 1, instruction + '\n' + '\n'.join(labels),
        [point(s(8, row, 1), 2, contextNote=s(8, row)) for row in range(2, 6)],
        'japanese-5-2', [11], [8], reading=[10],
        figure=crop('ja-2014-ol-3-1', 11, [.51, .03, .96, .21], instruction))
    add('3', 2, without_marker(col('paper', 11, [10, 11])), [point(s(8, 8), 3)],
        'japanese-5-2', [11], [8], 'i', reading=[10])
    add('3', 2, without_marker(col('paper', 11, [13, 14])), [anyn(options(8, [10], separator='/'), 2, 3)],
        'japanese-5-2', [11], [8], 'ii', reading=[10])
    for roman, qr, sr in [('i', range(19, 24), 14), ('ii', range(24, 29), 16), ('iii', range(29, 35), 18)]:
        add('3', 3, without_marker(col('paper', 11, qr)), [point(s(8, sr), 2)],
            'japanese-5-2', [11], [8], roman, reading=[10], stem=without_marker(col('paper', 11, [17, 18])))
    header = find_row('scheme', 8, '4.  (6 marks)')
    answers = [i for i, row in enumerate(ROWS['scheme'][7]) if i > header and any(group[2].strip() == '(2 marks)' for group in row)]
    assert len(answers) == 3
    for roman, qr, sr in zip(['i', 'ii', 'iii'], [36, 38, 40], answers):
        found = add('3', 4, without_marker(p(11, qr)), [point(s(8, sr), 2)],
            'japanese-5-2', [11], [8], roman, reading=[10], stem=english(p(11, 35, 1)))
        if roman == 'ii':
            restatement = cell('scheme', 8, sr - 1)
            assert 'すねいます' in restatement
            found['rows'][0]['contextNote'] = f'The original scheme restates the question as {restatement} It prints すねいます; the original paper prompt with すんでいます is retained. The source answer and its 2-mark tariff are unchanged.'


def writing():
    instruction = col('paper', 12, [2, 3])
    question = instruction + '\n' + '\n'.join(p(12, row) for row in range(4, 20))
    labels = [cell('scheme', 9, row, 0) if row != 9 else re.match(r'\([ivx]+\)', cell('scheme', 9, row)).group() for row in range(2, 12)]
    answers = [s(9, row, 1) if row != 9 else sa(9, row) for row in range(2, 12)]
    add('4', None, question, [], 'japanese-5-7', [12], [9], reading=[12], total=30,
        rubric=pool(10, labels, answers, 3, instruction, cell('scheme', 9, 1)),
        figure=crop('ja-2014-ol-4', 12, [.065, .055, .97, .94], instruction))
    instruction = p(13, 4)
    labels = [p(13, row) for row in range(5, 12)]
    content_row = find_row('scheme', 9, 'Content marks:')
    content_bands = [{'label': s(9, content_row + offset), 'marks': marks, 'guidance': [s(9, content_row + offset, 1)]}
                     for offset, marks in [(4, [1]), (3, [2]), (2, [3, 4]), (1, [5])]]
    expression_bands = [{'label': s(10, first), 'marks': marks,
                         'guidance': [s(10, first, 1) + ' ' + ' '.join(s(10, row) for row in rest)]}
                        for first, rest, marks in [(9, range(10, 16), [1]), (16, range(17, 24), [2, 3]), (24, range(25, 31), [4, 5])]]
    expression_row = find_row('scheme', 9, 'Expression marks:')
    cap = joined_selector('scheme', 9, [(expression_row + 1, 0), (expression_row + 2, 0)])
    split_rows = [i for i, row in enumerate(ROWS['scheme'][8]) if '(3 marks)' in ' '.join(group[2] for group in row)]
    assert len(split_rows) == 2
    splits = {4: cell('scheme', 9, split_rows[0]), 5: cell('scheme', 9, split_rows[1])}
    groups = []
    for i, label in enumerate(labels, 1):
        guide = [s(9, 14)]
        if i in splits:
            guide += [splits[i]]
        criteria = [{'id': f'item-{i}-content', 'label': s(9, content_row).removesuffix(':'), 'maxMarks': 5,
                     'permittedMarks': list(range(6)), 'guidance': guide, 'bands': content_bands},
                    {'id': f'item-{i}-expression', 'label': s(9, expression_row).removesuffix(':'), 'maxMarks': 5,
                     'permittedMarks': list(range(6)), 'guidance': [cap], 'bands': expression_bands,
                     'limits': [{'id': f'item-{i}-low-content', 'maxMarks': 3,
                                 'when': {'any': [{'criterionIds': [f'item-{i}-content'], 'atMost': 3}]}, 'guidance': [cap]}]}]
        groups.append({'id': f'item-{i}', 'label': label, 'rows': [], 'criteria': criteria})
    rubric = {'system': 'language-points', 'count': 5, 'taskRequirements': [instruction], 'groups': groups,
              'markingGuideNote': s(9, 13) + ' ' + s(9, 14) + ' ' + cap + ' ' + s(10, 31) + ' ' + s(10, 32)
              + ' — For (iv) and (v), the source gives component maxima of 3 and 2 and also a general content scale of 1, 2, 3–4 and 5. Assess the complete response on that printed scale; no per-component partial allocation is published.'}
    add('5', None, instruction + '\n' + '\n'.join(labels), [], 'japanese-5-7', [13], [9, 10], rubric=rubric, total=50,
        reading=[13], figure=crop('ja-2014-ol-5', 13, [.065, .03, .97, .96], instruction))


def listening():
    def listen(section, q, roman, qr, answers, rubric=None, total=None):
        page = {'A': 2, 'B': 3, 'C': 4, 'D': 5}[section]
        question = re.sub(r'^(?:\d+\.?\s*)?(?:\([ivx]+\)\s*)?', '', col('aural', page, qr, 300)).strip()
        card = add('L' + section, q, question, answers, 'japanese-6-2' if section == 'B' else 'japanese-6-0',
                   [page], [3 if section in 'AB' else 4], roman, reading=[page], rubric=rubric, total=total)
        card['stem'] = col('aural', page, range(1, 7 if section in 'ACD' else 8), 300)
        if section in 'BC':
            header = {'B': {1: 9, 2: 24, 3: 35}, 'C': {1: 8, 2: 31}}[section][q]
            card['stem'] += '\n' + col('aural', page, [header], 300)
        return card
    for q, roman, qr, sr, sg, marks in [
        (1, 'i', [7], 3, 2, 2), (1, 'ii', range(9, 14), 4, 1, 4), (1, 'iii', range(14, 20), 5, 0, 4),
        (2, 'i', [20], 6, 2, 2), (2, 'ii', range(22, 27), 7, 1, 4), (2, 'iii', range(27, 32), 8, 0, 4),
        (3, 'i', range(32, 37), 9, 2, 4), (3, 'ii', range(37, 42), 10, 1, 4)]:
        listen('A', q, roman, qr, [point(without_marker(s(3, sr, sg)), marks)])
    for q, roman, qr, sr, sg in [(1, 'i', range(10, 15), 13, 1), (1, 'ii', range(15, 20), 14, 0),
        (2, 'i', range(25, 30), 17, 1), (2, 'ii', range(30, 35), 18, 1), (3, '', range(36, 42), 20, 1)]:
        card = listen('B', q, roman, qr, [point(s(3, sr, sg), 4)])
        if q == 3:
            card['rows'][0]['contextNote'] = 'The scheme labels the weather response (i); the original paper prints Q3 without a subsidiary number. The original paper identity is retained.'
    phone_source = cell('scheme', 3, 15)
    number = re.search(r'03-5822\)\s*–\s*\(6405', phone_source).group().replace(')', '').replace('(', '').replace(' ', '')
    digits = re.sub(r'\D', '', number)
    rows = [point(digits[position - 1], contextNote=f'Missing digit {index + 1} (position {position} in {number}). {phone_source} — Only the four missing digits score; the printed digits are given.')
            for index, position in enumerate([4, 8, 9, 10])]
    phone = listen('B', 1, 'iii', [21], rows)
    phone['questionFigureKey'] = crop('ja-2014-ol-lb-1-iii', 3, [.51, .43, .97, .525], phone['questionText'], 'aural')
    for roman, qr, sr, sg, marks in [('i', [9], 2, 1, 2), ('ii', range(11, 16), 3, 1, 4),
            ('iii', range(16, 21), 4, 1, 4), ('iv', range(21, 26), 5, 1, 4), ('v', range(26, 31), 6, 1, 4)]:
        answer = s(4, sr, sg) + (' ' + s(4, sr, 2) if sr > 2 else '')
        listen('C', 1, roman, qr, [point(answer, marks)])
    listen('C', 2, 'i', [32], [anyn(options(4, [8], 1, ','), 1, 2)])
    dishes = s(4, 9, 1).split('/')
    compound = [re.findall(r'(\w+)\s*\(1 mark\)', text) for text in dishes[1:3]]
    assert len(compound) == 2 and all(len(pair) == 2 for pair in compound)
    groups = [{'id': 'tempura', 'label': dishes[0].strip(), 'rows': [{'id': 'answer', 'text': dishes[0].strip(), 'marks': 2}]}]
    for index, pair in enumerate(compound, 1):
        groups.append({'id': f'dish-{index}', 'label': ' '.join(pair), 'rows': [
            {'id': f'part-{part + 1}', 'text': answer, 'marks': 1} for part, answer in enumerate(pair)]})
    groups.append({'id': 'sashimi', 'label': s(4, 10), 'rows': [{'id': 'answer', 'text': s(4, 10), 'marks': 2}]})
    rubric = {'system': 'language-points', 'count': 2, 'taskRequirements': [without_marker(col('aural', 4, [34]))],
              'groups': groups, 'markingGuideNote': cell('scheme', 4, 9) + ' ' + cell('scheme', 4, 10) + ' ' + cell('scheme', 4, 11)
              + ' — Select at most two dishes. Each compound dish is one group; its two printed one-mark components remain separate. Sashimi and raw fish name one accepted dish.'}
    listen('C', 2, 'ii', [34], [], rubric=rubric, total=4)
    for q, qr, sr in [(1, range(8, 13), 13), (2, range(13, 18), 14), (3, range(18, 23), 15),
                     (4, range(23, 28), 16), (6, range(31, 36), 19)]:
        listen('D', q, '', qr, [point(sa(4, sr), 4)])
    listen('D', 5, '', [28], [{'kind': 'criterion', 'verbatim': sa(4, 17), 'marks': 4, 'permittedMarks': [0, 2, 4],
                              'contextNote': cell('scheme', 4, 17) + ' ' + cell('scheme', 4, 18)}])


def build():
    reading_q1()
    reading_q2_profiles()
    reading_q2_remaining()
    reading_q3()
    writing()
    listening()
    census = json.loads((Path(__file__).parent / 'reviews/japanese-2014-ol-census.json').read_text())
    expected = {'ja-2014-ol-' + '-'.join(str(part).lower() for part in task['key'] if part is not None): task for task in census['tasks']}
    assert set(expected) == {card['id'] for card in CARDS}
    def nonempty_guidance(value):
        if isinstance(value, dict):
            for key, child in value.items():
                if key == 'guidance':
                    assert child and all(isinstance(text, str) and text.strip() for text in child), value
                nonempty_guidance(child)
        elif isinstance(value, list):
            for child in value: nonempty_guidance(child)
        elif isinstance(value, str):
            assert not any(ord(char) < 32 and char not in '\n\r\t' or char == '\ufffd' for char in value), value
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
    assert not any(ord(char) < 32 and char not in '\n\r\t' or char == '\ufffd'
                   for char in json.dumps([CARDS, EVIDENCE], ensure_ascii=False))
    recovery = ROOT / 'scripts/markbank/authoring/glyphmap-japanese-2014-ol.json'
    return {'subjectId': 'japanese', 'sitting': '2014-ol', 'reviewedAt': '2026-11-10',
            'sources': [{'document': name, 'path': str(path.relative_to(ROOT)), 'sha256': HASHES[name],
                         'pagesReviewed': list(range(1, len(DOCS[name]) + 1))} for name, path in PATHS.items()],
            'glyphRecovery': {'path': str(recovery.relative_to(ROOT)), 'sha256': hashlib.sha256(recovery.read_bytes()).hexdigest()},
            'cards': CARDS, 'selectors': EVIDENCE, 'status': 'source-reviewed-browser-qa-pending',
            'choiceAnalysis': census['choiceBoundaries'], 'consolidations': []}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    result = build()
    if args.write:
        text = '# Original text with source-proven glyph recovery and furigana folded at its printed character\n'
        for i, page in enumerate(DOCS['scheme']):
            body = '\n'.join(' '.join(g[2] for g in row) for row in page_rows(page))
            if '\ufffd' in body:
                assert i + 1 >= 11
                body = 'The complete original listening transcript is retained in the source PDF image. No transcription of unresolved glyphs is published.'
            text += f'\n## Physical page {i + 1}\n\n{body}\n'
        PATHS['scheme'].with_suffix('.md').write_text(text.rstrip() + '\n')
        (ROOT / 'scripts/markbank/authoring/reviews/japanese-2014-ol.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
        manifest = ROOT / 'components/MarkBank/figures-japanese.json'
        previous = json.loads(manifest.read_text())
        previous.update(FIGURES)
        manifest.write_text(json.dumps(previous, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'cards': len(CARDS), 'marks': sum(card['totalMarks'] for card in CARDS), 'figures': len(FIGURES)}, indent=2))
