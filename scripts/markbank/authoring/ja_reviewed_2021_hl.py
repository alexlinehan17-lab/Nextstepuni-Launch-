#!/usr/bin/env python3
"""2021 Higher Japanese, independently reviewed against all original pages.

Selectors below are coordinates in ja_text.page_rows, not transcribed answers.
Every question comes from the paper; every answer and tariff wording from the
scheme. Choice pools are kept whole. Run with --write to publish the manifest.
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
PAPER = ROOT / 'examiner-reports/japanese/papers/2021-hl-000-paper.pdf'
AURAL = ROOT / 'examiner-reports/japanese/papers/2021-hl-A00-paper.pdf'
SCHEME = ROOT / 'examiner-reports/japanese/schemes/2021-hl.pdf'
PINNED_SOURCES = {
    PAPER: '906c9dc00db6e0b4f0ad0b7f63403046bad7533a09aa57a0f51767b9124e96fd',
    AURAL: '760082f066675ec3cf2f60c9839dce035c2d0229eadf25450704ba79794efc7c',
    SCHEME: 'e9fb692a2c1046ef9c23e0a93a2334536885dc67ab5bb10298923cd51d462b7e',
}
for path, expected in PINNED_SOURCES.items():
    assert hashlib.sha256(path.read_bytes()).hexdigest() == expected, f'Source changed; review again: {path}'
DOCS = {name: fitz.open(path) for name, path in [('paper', PAPER), ('aural', AURAL), ('scheme', SCHEME)]}
ROWS = {name: [page_rows(page) for page in doc] for name, doc in DOCS.items()}
CARDS = []
FIGURES = {}
EVIDENCE = []


def cell(doc, page, row, group=None):
    groups = ROWS[doc][page - 1][row]
    text = ' '.join(group[2] for group in groups) if group is None else groups[group][2]
    EVIDENCE.append({'document': doc, 'page': page, 'row': row, 'group': group, 'text': text})
    return text


def s(page, row, group=0):
    """Answer cell, preserving scheme alternatives; remove only bullet/tariff."""
    text = cell('scheme', page, row, group)
    return re.sub(r'\s*\(\d+ marks?\)\s*$', '', text).strip().removeprefix('- ').strip()


def p(page, row, group=None):
    return cell('paper', page, row, group)


def join_cells(doc, page, rows, x_min=0):
    return ' '.join(' '.join(cell(doc, page, row, gi) for gi, group in enumerate(ROWS[doc][page - 1][row]) if group[0] >= x_min) for row in rows)


def english(text):
    return re.split(r'\s*/\s*', text.replace('\xa0', ' '), maxsplit=1)[-1].strip()


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


def source(pages, kind='source-text', component='paper'):
    return {'kind': kind, 'label': '2021 Japanese Higher Level', 'title': 'Original examination material',
            'pages': pages, 'attribution': '© State Examinations Commission.',
            **({'presentationNote': FURIGANA_NOTE} if component == 'paper' else {}),
            '_component': component}


def add(section, q, question, rows, topic, paper_pages, scheme_pages, suffix='', rubric=None, total=None, reading=None, figure=None):
    cid = f'ja-2021-hl-{section.lower()}' + (f'-{q}' if q is not None else '') + (f'-{suffix}' if suffix else '')
    ref = f'2021 HL Section {section}' + (f' Q{q}' if q is not None else '')
    if suffix:
        ref += (' Q' if q is None else '') + ''.join(f'({part})' for part in suffix.split('-'))
    listening = section.startswith('L')
    card = {'id': cid, 'source': 'sec', 'subjectId': 'japanese', 'specVersion': 'lc-japanese-syllabus',
            'kind': 'rubric' if rubric else 'question', 'level': 'higher', 'year': 2021,
            'section': section[1:] if listening else section[0] if section[0] in '1234' else 'Q5',
            'topicId': topic, 'conceptId': concept_for(question, cid), 'questionRef': ref,
            'questionText': question, 'totalMarks': total if total is not None else sum(map(worth, rows)),
            'qa': {'gates': ['verbatim', 'tariff', 'figure'], 'humanReviewedBy': 'agent-verified', 'humanReviewedAt': '2026-11-09'},
            'sourceEvidence': {'component': 'aural' if listening else 'paper', 'paperPages': paper_pages, 'schemePages': scheme_pages},
            'schemeCitation': 'Marking points quoted from the SEC marking scheme, Japanese 2021 Higher Level — © State Examinations Commission.'}
    if rubric:
        card['rubric'] = rubric
    else:
        card['tariffModel'] = {'kind': 'fixed'}
        card['rows'] = [dict(row, id=f'r-{i + 1}') for i, row in enumerate(rows)]
    original_ids = set(re.findall(r'    id: "([^"]+)"', (ROOT / 'components/MarkBank/cards/japanese/higher.ts').read_text()))
    if cid in original_ids:
        card['qa']['gates'].append('reviewed-card-correction')
    if listening or section[0] in '123':
        page, row = (3, 1) if listening else (7, 1) if section.startswith('1') else (8, 10) if section.startswith('2') else (11, 0)
        card['sourceEvidence']['generalSchemePages'] = [page]
        card['answerLanguageRule'] = {'otherLanguageMultiplier': 0.5, 'sourceText': cell('scheme', page, row), 'schemePages': [page]}
        if listening:
            card['answerLanguageRule']['penalizedLanguage'] = 'Japanese'
        if section == '1B':
            # Q1's incorrect-language rule governs both A and B. The local B
            # Japanese note is additional guidance, not an exemption for other
            # incorrect languages; preserve it visibly without narrowing Q1.
            card['sourceEvidence']['generalSchemePages'].append(8)
            card['rows'][0]['contextNote'] = cell('scheme', 8, 0)
        if section == '2A' and q == 2:
            card['extraneousMaterialRule'] = {'multiplier': 0.5, 'sourceText': cell('scheme', 8, 27), 'schemePages': [8]}
    if reading:
        card['sourceMaterial'] = source(reading)
    if figure:
        card['questionFigureKey'] = figure
    CARDS.append(card)
    return card



def joined_selector(document, page, parts):
    text = ' '.join(cell(document, page, row, group) for row, group in parts)
    EVIDENCE.append({'document': document, 'page': page, 'parts': [{'row': row, 'group': group} for row, group in parts], 'text': text})
    return text


def prompt(page, rows):
    return english(' '.join(p(page, row) for row in rows))


def strip_tariff(text):
    return re.sub(r'\s*\(any.*$', '', text).strip()


def options(page, rows, separator=', '):
    return [part.strip() for part in strip_tariff(' '.join(s(page, row) for row in rows)).split(separator)]


def comprehension(section, q, suffix, question_rows, rows, scheme_pages):
    page = 3 if section == '1A' else 4 if section == '1B' else 7 if section == '2A' else 11
    topic = 'japanese-5-0' if section.startswith('1') else 'japanese-5-2'
    text = prompt(page, question_rows)
    if section == '3B' or section == '2A' and q == 2:
        text = ' '.join(p(page, row, 1) for row in question_rows)
    card = add(section, q, text, rows, topic, [page], scheme_pages, suffix or '',
               reading={'1A': [2], '1B': [4], '2A': [6], '3A': [10], '3B': [10]}[section])
    row = (7 if q == 2 else 14) if section == '2A' else {'1A': 0, '1B': 17, '3A': 0, '3B': 17}[section]
    card['stem'] = english(p(page, row))
    return card


def crop(key, page, region, alt, component='paper'):
    doc = DOCS[component]
    sheet = doc[page - 1]
    rect = fitz.Rect(region[0] * sheet.rect.width, region[1] * sheet.rect.height, region[2] * sheet.rect.width, region[3] * sheet.rect.height)
    rel = f'/exam-figures/japanese/{key}.png'
    path = ROOT / 'public' / rel.lstrip('/')
    path.parent.mkdir(parents=True, exist_ok=True)
    sheet.get_pixmap(matrix=fitz.Matrix(2, 2), clip=rect).save(path)
    FIGURES[key] = {'src': rel, 'md5': hashlib.md5(path.read_bytes()).hexdigest(), 'alt': alt,
                    'attribution': '© State Examinations Commission.',
                    'source': {'document': component, 'page': page, 'region': region}}
    return key


def clean_tariff(text):
    return re.sub(r'\s*\(?\d+\s*marks?\)?\s*$', '', text).strip()


def selected(page, parts):
    return joined_selector('scheme', page, parts)


def split_marks(text, marks=1):
    return [part.strip(' ,-') for part in re.split(rf'\({marks}\s+marks?\)', text) if part.strip(' ,-')]


def group_rows(card, groups):
    card['taskGroups'] = [
        {'sourceCardId': card['id'] + '-' + name, 'label': label,
         'marks': sum(worth(row) for row in card['rows'][start:end]),
         'rowIds': [row['id'] for row in card['rows'][start:end]]}
        for name, label, start, end in groups]


def reading():
    instruction = prompt(3, [1, 2])
    labels = [p(3, row, 0) + ' ' + english(p(3, row, 1)) for row in range(4, 10)]
    answers = [s(7, row, 1 if row == 7 else 2) for row in range(5, 11)]
    question = instruction + '\n' + english(p(3, 3, 0)) + ' ' + p(3, 3, 1) + '\n' + '\n'.join(labels)
    add('1A', 1, question, [], 'japanese-5-0', [3], [7], total=5, reading=[2],
        rubric={'system': 'language-points', 'count': 5,
                'groups': [{'id': f'item-{i}', 'label': label, 'rows': [{'id': 'answer', 'text': answer, 'marks': 1}]} for i, (label, answer) in enumerate(zip(labels, answers), 1)],
                'taskRequirements': [instruction], 'markingGuideNote': cell('scheme', 7, 4) + ' — The paper presents six links; the adjusted scheme explicitly credits any five. All six remain available.'})
    headers = [p(3, 12, i) for i in [0, 1]]
    question = prompt(3, [10]) + '\n' + '\n'.join(headers + [p(3, 14), p(3, 16)])
    men_name = selected(7, [(13, 1), (14, 0)])
    men_description = strip_tariff(selected(7, [(13, 2), (14, 1), (15, 0)]))
    women_name = s(7, 17, 0).removeprefix('For women ')
    table_rows = [*[point(text, contextNote=p(3, 14) + ' — ' + headers[0]) for text in split_marks(men_name)],
                  anyn([text.strip() for text in men_description.split('/')], 2, contextNote=p(3, 14) + ' — ' + headers[1]),
                  *[point(text, contextNote=p(3, 16) + ' — ' + headers[0]) for text in split_marks(women_name)],
                  anyn(options(7, [17], '/'), 2)]
    # The last cell is the second physical column, not the combined name cell.
    table_rows[-1]['group']['options'] = [text.strip() for text in s(7, 17, 1).split('/')]
    table_rows[-1]['contextNote'] = p(3, 16) + ' — ' + headers[1]
    table = add('1A', 2, question, table_rows, 'japanese-5-0', [3], [7], reading=[2, 3],
                figure=crop('ja-2021-hl-1a-2', 3, [.07, .29, .94, .495], question))
    group_rows(table, [('men', p(3, 14), 0, 3), ('women', p(3, 16), 3, 6)])
    comprehension('1A', 3, None, [17], [point(text) for text in split_marks(selected(7, [(20, 0), (20, 1)]))], [7])
    for q, qr, sr in [(4, 19, 22), (5, 21, 24)]:
        comprehension('1A', q, None, [qr], [point(s(7, sr), 2)], [7])
    for roman, qr, sr in [('i', 23, 26), ('ii', 25, 29)]:
        comprehension('1A', 6, roman, [qr], [anyn(options(7, [sr], '/'), 2)], [7])
    comprehension('1B', 1, None, [18, 19], [point(text) for text in split_marks(s(8, 2))], [8])
    comprehension('1B', 2, None, [21], [anyn(options(8, [4, 5], '/'), 2, 2, [2, 1])], [8])
    comprehension('1B', 3, None, [23, 24], [anyn(options(8, [7], '/'), 2)], [8])
    comprehension('1B', 4, None, [26, 27], [point(s(8, 9), 2)], [8])
    question = prompt(7, [1]) + '\n' + '\n'.join(p(7, row) for row in [3, 4, 5, 6])
    rachel, jun = p(7, 5), p(7, 6)
    headers = [p(7, 3, 0), p(7, 3, 1).split('/', 1)[-1] + ' ' + p(7, 4), p(7, 3, 2)]
    hometown = re.sub(r'\s*\(2 marks\)', '', selected(8, [(16, 1), (17, 0)]))
    physical_rachel = strip_tariff(selected(8, [(16, 2), (17, 1), (18, 0)]))
    physical_jun = strip_tariff(selected(8, [(21, 2), (23, 0), (25, 0), (26, 0)]))
    table_rows = [point(hometown, contextNote=rachel + ' — ' + headers[0]),
                  point(s(8, 15), 2, contextNote=rachel + ' — ' + headers[1]),
                  anyn([text.strip() for text in physical_rachel.split('/')], 2, contextNote=rachel + ' — ' + headers[2]),
                  point(s(8, 21, 1), contextNote=jun + ' — ' + headers[0]),
                  *[point(text, contextNote=jun + ' — ' + headers[1]) for text in split_marks(selected(8, [(20, 0), (22, 0)]))],
                  anyn([text.strip() for text in physical_jun.split('/') if text.strip()], 2, contextNote=jun + ' — ' + headers[2])]
    table = add('2A', 1, question, table_rows, 'japanese-5-2', [7], [8], reading=[6, 7],
                figure=crop('ja-2021-hl-2a-1', 7, [.06, .048, .95, .249], question))
    group_rows(table, [('rachel', rachel, 0, 3), ('jun', jun, 3, 7)])
    for roman, qr, sr in [('i', 8, 29), ('ii', 10, 31), ('iii', 12, 33)]:
        comprehension('2A', 2, roman, [qr], [point(s(8, sr), 2)], [8])
    communication = split_marks(selected(9, [(2, 0), (3, 0)]))
    comprehension('2A', 3, 'i', [15, 16], [point(text) for text in communication], [9])
    comprehension('2A', 3, 'ii', [18], [point(s(9, 5))], [9])
    comprehension('2A', 3, 'iii', [20, 21], [anyn(options(9, [7, 8], '/'), 2, 2, [2, 1])], [9])
    comprehension('2A', 3, 'iv', [23, 24], [anyn(options(9, [10], '/'), 2, 2, [2, 1])], [9])
    translation = split_marks(selected(9, [(15, 0), (16, 0)]))
    add('2A', 4, prompt(7, [26]) + '\n' + p(7, 27) + ' ' + p(7, 28), [point(text) for text in translation],
        'japanese-5-3', [7], [9], reading=[6])
    for section, q, pp, qr, prange, sp, sr, answer_rows, region in [
        ('2B', 1, 8, [1, 2], range(4, 10), 9, 18, range(19, 25), [.06, .06, .96, .47]),
        ('2B', 2, 8, [10, 11], range(13, 19), 10, 0, range(1, 7), [.06, .474, .96, .92]),
        ('2C', 1, 9, [1, 2], range(4, 10), 10, 8, [9, 10, 11, 14, 15, 16], [.06, .06, .96, .44]),
        ('2C', 2, 9, [10, 11], range(13, 19), 10, 17, range(18, 24), [.06, .437, .96, .88]),
    ]:
        instruction = prompt(pp, qr)
        labels = [p(pp, row, 0) + ' ' + p(pp, row, 1) for row in prange]
        answers = [re.sub(r'^\([ivx]+\)\s*', '', s(sp, row, 0 if section == '2C' and q == 1 and row == 9 else 1)) for row in answer_rows]
        if section == '2C' and q == 1:
            answers[2] += ' ' + s(10, 12) + ' ' + s(10, 13)
        groups = [{'id': f'item-{i}', 'label': label, 'rows': [{'id': 'answer', 'text': answer, 'marks': 1}]} for i, (label, answer) in enumerate(zip(labels, answers), 1)]
        question = instruction + '\n' + p(pp, qr[-1] + 1) + '\n' + '\n'.join(labels)
        add(section, q, question, [], 'japanese-5-4' if section == '2B' else 'japanese-5-5', [pp], [sp], total=5, reading=[pp],
            figure=crop(f'ja-2021-hl-{section.lower()}-{q}', pp, region, instruction),
            rubric={'system': 'language-points', 'count': 5, 'groups': groups, 'taskRequirements': [instruction], 'markingGuideNote': cell('scheme', sp, sr)})
    comprehension('3A', 1, None, [1], [anyn(options(11, [3, 4], '/'), 2)], [11])
    location = options(11, [7, 8], '/')
    partial_location = re.sub(r'\s*1 mark\)$', '', s(11, 9).removeprefix('('))
    location += [text.strip() for text in partial_location.split('/')]
    comprehension('3A', 2, None, [4], [anyn(location, 2)], [11])
    comprehension('3A', 3, None, [7], [anyn(options(11, [11, 12], '/'), 3)], [11])
    comprehension('3A', 4, None, [10, 11], [anyn(options(11, [14, 15, 16], '/'), 2, 2, [2, 1])], [11])
    comprehension('3A', 5, None, [14, 15], [anyn(options(11, [19], '/'), 2)], [11])
    for q, qr, answers in [(1, 18, [point(s(11, 23))]), (2, 20, [anyn(options(11, [25], '/'), 2)]),
                           (3, 22, [point(s(11, 28))]), (4, 24, [point(s(11, 30, 1), 2)])]:
        comprehension('3B', q, None, [qr], answers, [11])
    instruction = prompt(12, [1, 2, 3])
    labels = [p(12, row) for row in range(6, 12)]
    groups = [{'id': f'item-{i}', 'label': label,
               'rows': [{'id': 'reading', 'text': s(12, i, 1) + ' ' + s(12, i, 2), 'marks': 1},
                        {'id': 'meaning', 'text': s(12, i, 4), 'marks': 1}]} for i, label in enumerate(labels, 1)]
    add('3C', None, instruction + '\n' + p(12, 5) + '\n' + '\n'.join(labels), [], 'japanese-5-4', [12], [12], total=10, reading=[12],
        figure=crop('ja-2021-hl-3c', 12, [.06, .06, .98, .475], instruction),
        rubric={'system': 'language-points', 'count': 5, 'groups': groups, 'taskRequirements': [instruction], 'markingGuideNote': cell('scheme', 12, 0) + ' — The paper calls this pool C; the scheme prints B.'})
    instruction = prompt(12, [13, 14, 15])
    groups = []
    for index, sr in enumerate(range(9, 16)):
        label = p(12, 16 + index)
        text = re.sub(r'^\([ivx]+\)\s*', '', cell('scheme', 12, sr))
        answers = [text.strip() for text in text.split('1 mark') if text.strip()]
        for blank, answer in enumerate(answers, 1):
            groups.append({'id': f'sentence-{index + 1}-blank-{blank}', 'label': label + f' — blank {blank}', 'rows': [{'id': 'answer', 'text': answer, 'marks': 1}]})
    assert len(groups) == 12
    add('3D', None, instruction + '\n' + '\n'.join(p(12, row) for row in range(16, 23)), [], 'japanese-5-5', [12], [12], total=10, reading=[12],
        figure=crop('ja-2021-hl-3d', 12, [.06, .478, .98, .91], instruction),
        rubric={'system': 'language-points', 'count': 10, 'groups': groups, 'taskRequirements': [instruction], 'markingGuideNote': cell('scheme', 12, 8) + ' — The paper calls this pool D; the scheme prints C.'})


def steps(maximum):
    return list(range(maximum + 1))


def writing():
    guidance = [join_cells('scheme', 15, range(first, last), 155) for first, last in [(16, 25), (25, 33), (33, 41)]]
    bands = [{'label': f'{lo}–{hi}', 'marks': list(range(lo, hi + 1)), 'guidance': [text]} for (lo, hi), text in zip([(0, 6), (7, 17), (18, 25)], guidance)]
    reduced = [{'label': f'{lo}–{hi}', 'marks': list(range(lo, hi + 1)), 'guidance': [text]} for (lo, hi), text in zip([(0, 4), (5, 13), (14, 19)], guidance)]
    rule = selected(15, [(row, None) for row in range(9, 13)])
    exam_choice = english(p(14, 0))
    for q, pp, sp in [(4, 14, 13), (5, 16, 14)]:
        if q == 4:
            instruction = prompt(14, [2, 3])
            question = exam_choice + '\n' + instruction + '\n' + '\n'.join([
                '(a) ' + prompt(14, [4, 5, 6]), p(14, 7), p(14, 8), p(14, 9), english(p(14, 10)),
                '(b) ' + prompt(14, [11, 12, 13]), p(14, 14), p(14, 15), p(14, 16), english(p(14, 17)),
                '(c) ' + prompt(14, [18, 19, 20]), p(14, 21), p(14, 22), p(14, 23)])
            allocation = selected(13, [(row, None) for row in range(19, 25)])
            criteria = [{'id': f'point-{i}', 'label': f'({i})', 'maxMarks': 7, 'permittedMarks': steps(7), 'guidance': [s(13, 20)]} for i in ['i', 'ii', 'iii']]
            guide = 'Assess the one option you answered: three required content points at 7 each, opening 1, closing 1 and two further discretionary marks. Use one common expression score. The examination requires either Q4 or Q5.'
        else:
            instruction = prompt(16, [1, 2, 3, 4, 5])
            question = exam_choice + '\n' + instruction + '\n' + '\n'.join(p(16, row) for row in range(6, 22))
            allocation = selected(14, [(row, None) for row in range(4, 10)])
            headings = [cell('scheme', 14, row) for row in range(12, 20)]
            criteria = [{'id': f'heading-{i}', 'label': f'Chosen heading {i}', 'maxMarks': 5, 'permittedMarks': steps(5),
                         'guidance': [cell('scheme', 14, 5)] + headings} for i in range(1, 5)]
            guide = 'Assess four different headings once each, at 5 marks each, plus opening 1, closing 1 and three further discretionary marks. Use one common expression score. The examination requires either Q4 or Q5.'
        criteria += [
            {'id': 'opening', 'label': 'Opening', 'maxMarks': 1, 'permittedMarks': [0, 1], 'guidance': [allocation]},
            {'id': 'closing', 'label': 'Closing', 'maxMarks': 1, 'permittedMarks': [0, 1], 'guidance': [allocation]},
            {'id': 'discretionary', 'label': 'Further discretionary marks', 'maxMarks': q - 2, 'permittedMarks': steps(q - 2), 'guidance': [allocation]},
        ]
        content_ids = [criterion['id'] for criterion in criteria]
        criteria.append({'id': 'expression', 'label': s(sp, 25 if q == 4 else 10), 'maxMarks': 25, 'permittedMarks': steps(25),
            'guidance': [selected(15, [(41, None), (42, None)])], 'bands': bands,
            'limits': [{'id': 'lower-e', 'maxMarks': 19, 'when': {'any': [{'criterionIds': content_ids, 'atMost': 13}, {'length': 'characters', 'below': 150}]},
                        'bands': reduced, 'guidance': [rule]}]})
        add(str(q), None, question, [], 'japanese-5-7', [pp], [sp, 15], total=50, reading=[pp],
            figure=crop(f'ja-2021-hl-{q}', pp, [.045, .015, .97, .92], question),
            rubric={'system': 'language-writing', 'taskRequirements': [exam_choice, instruction], 'criteria': criteria, 'markingGuideNote': guide})


def listening():
    def aq(page, rows):
        return re.sub(r'^(?:\d+\.\s*)?(?:\([ivx]+\)\s*)?', '', join_cells('aural', page, rows, 300)).strip()

    def listen(part, q, roman, qr, rows, question=None):
        pp, sp = {'A': (2, 3), 'B': (3, 4), 'C': (4, 5), 'D': (5, 6)}[part]
        card = add('L' + part, q, question or aq(pp, qr), rows,
                   {'A': 'japanese-6-1', 'B': 'japanese-6-2', 'C': 'japanese-6-1', 'D': 'japanese-6-0'}[part], [pp], [sp], roman or '')
        card['sourceMaterial'] = source([pp], 'source-question', 'aural')
        card['stem'] = join_cells('aural', pp, range(1, 5 if part == 'A' else 7 if part == 'D' else 6), 300)
        if part == 'B':
            card['stem'] += '\n' + cell('aural', 3, 6 if q == 1 else 26, 1)
        return card

    headers = [cell('aural', 2, 9, 0), cell('aural', 2, 9, 1),
               joined_selector('aural', 2, [(10, 0), (11, 0)]), joined_selector('aural', 2, [(10, 1), (11, 1)])]
    names = [cell('aural', 2, row) for row in [13, 15, 17]]
    maria = [
        [point(s(3, 7, 1))],
        [point(text) for text in split_marks(selected(3, [(7, 2), (8, 0), (10, 0)]))],
        [point(selected(3, [(7, 3), (8, 1), (10, 1)]), 2)],
        [point(text) for text in split_marks(selected(3, [(7, 4), (8, 2), (10, 2)]))],
    ]
    max_reason = selected(3, [(12, 3), (13, 1), (15, 1), (16, 1)]).replace('(1 mark)', '')
    # The final 1-mark phrase belongs to the adjacent method column; the
    # original visual table prices this whole reason cell at two marks.
    max_reason = re.sub(r'\s+', ' ', max_reason).strip()
    max_method = [point(s(3, 12, 4).split('(1 mark)')[0].strip()), point(s(3, 13, 2))]
    max_rows = [
        [point(s(3, 12, 1))],
        [point(text) for text in split_marks(selected(3, [(12, 2), (13, 0), (15, 0), (16, 0)]))],
        [point(max_reason, 2)], max_method,
    ]
    sophie_reason = selected(3, [(18, 3), (19, 1), (21, 0), (23, 0), (24, 0), (26, 0), (27, 0), (28, 0), (29, 0)])
    sophie = [
        [point(s(3, 18, 1))],
        [point(text) for text in split_marks(selected(3, [(18, 2), (19, 0)]))],
        [{'kind': 'criterion', 'verbatim': sophie_reason, 'marks': 2, 'permittedMarks': [0, 1, 2],
          'contextNote': 'Use the exact reason and partial-credit distinctions printed here. The final parenthesised brother alternative earns only 1 mark; this cell has a 2-mark maximum.'}],
        [point(text) for text in split_marks(selected(3, [(18, 4), (19, 2), (21, 1), (23, 1)]))],
    ]
    rows, display_groups = [], []
    for person, cells in enumerate([maria, max_rows, sophie]):
        for column, cell_rows in enumerate(cells):
            start = len(rows)
            label = names[person] + ' — ' + headers[column]
            for row in cell_rows:
                row['contextNote'] = label + (' — ' + row['contextNote'] if row.get('contextNote') else '')
            rows.extend(cell_rows)
            display_groups.append((f'person-{person + 1}-cell-{column + 1}', label, start, len(rows)))
    question = cell('aural', 2, 6, 1) + '\n' + '\n'.join(headers + names)
    table = listen('A', None, None, [], rows, question)
    table['questionFigureKey'] = crop('ja-2021-hl-la', 2, [.075, .151, .97, .71], question, 'aural')
    group_rows(table, display_groups)
    listen('B', 1, 'i', [7, 8], [anyn(options(4, [3], '/'), 2)])
    listen('B', 1, 'ii', [11], [anyn(options(4, [6, 7], '/'), 2, 2, [2, 1])])
    listen('B', 1, 'iii', [15], [point(text) for text in split_marks(s(4, 10))])
    listen('B', 1, 'iv', [18, 19], [anyn(options(4, [12], '/'), 2, 2, [2, 1])])
    listen('B', 1, 'v', [22, 23], [point(s(4, 15), 2)])
    weather = [
        anyn([text.strip() for text in selected(4, [(19, 1), (20, 0)]).split('/')], 2, contextNote=cell('aural', 3, 29) + ' — ' + cell('aural', 3, 27, 2)),
        point(selected(4, [(19, 2), (20, 1)]), 2, contextNote=cell('aural', 3, 29) + ' — ' + cell('aural', 3, 27, 3)),
        anyn([text.strip() for text in selected(4, [(22, 1), (23, 0), (24, 0)]).split('/')], 2, contextNote=cell('aural', 3, 32) + ' — ' + cell('aural', 3, 27, 2)),
        point(selected(4, [(22, 2), (23, 1)]), 2, contextNote=cell('aural', 3, 32) + ' — ' + cell('aural', 3, 27, 3)),
    ]
    question = aq(3, [26]) + '\n' + cell('aural', 3, 27, 2) + ' / ' + cell('aural', 3, 27, 3) + '\n' + cell('aural', 3, 29) + '\n' + cell('aural', 3, 32)
    table = listen('B', 2, None, [], weather, question)
    table['questionFigureKey'] = crop('ja-2021-hl-lb-2', 3, [.52, .69, .96, .925], question, 'aural')
    listen('C', None, 'i', [6], [point(s(5, 2), 2)])
    listen('C', None, 'ii', [8, 9], [anyn(options(5, [4, 5], '/'), 3, 2, [2, 1, 1])])
    listen('C', None, 'iii', [13, 14], [point(s(5, 8), 2)])
    listen('C', None, 'iv', [17, 18], [point(text) for text in split_marks(s(5, 11))])
    listen('C', None, 'v', [20], [point(s(5, 13), 2)])
    phone = listen('C', None, 'vi', [23], [point(s(5, 15), 3, contextNote='The published scheme prices the full phone number at 3 marks and supplies no per-digit split.')])
    phone['questionFigureKey'] = crop('ja-2021-hl-lc-vi', 4, [.54, .675, .98, .75], phone['questionText'], 'aural')
    route = options(5, [17], '/')
    east = route.pop(1)
    listen('C', None, 'vii', [25], [point(east, contextNote=s(5, 18)), anyn(route, 2, 2, [2, 1], contextNote=s(5, 18))])
    listen('D', None, 'i', [7], [point(s(6, 2), 2)])
    listen('D', None, 'ii', [9], [point(s(6, 4), 2)])
    listen('D', None, 'iii', [11, 12], [point(text, 2) for text in split_marks(s(6, 6), 2)])
    listen('D', None, 'iv', [15], [point(text, 2) for text in split_marks(s(6, 8), 2)])
    listen('D', None, 'v', [18], [point(s(6, 11), 2)])
    listen('D', None, 'vi', [22], [anyn(options(6, [13], '/'), 2, 2, [2, 1])])
    cat, description = s(6, 16).split('(1 mark)', 1)
    listen('D', None, 'vii', [25], [point(cat.strip()), anyn([text.strip() for text in description.strip(' ,').split('/')], 2, contextNote=s(6, 17))])


def consolidations(census):
    records = []
    romans = ['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii']
    for suffix, count, pp, pr, sp, sr, reason in [
        ('1a-1', 6, 3, [1, 2], 7, 4, 'The adjusted scheme prices one complete any-five-of-six link pool at one mark per chosen answer.'),
        ('2b-1', 6, 8, [1, 2], 9, 18, 'One complete any-five-of-six kanji meaning pool, one mark per chosen answer.'),
        ('2b-2', 6, 8, [10, 11], 10, 0, 'One complete any-five-of-six kanji reading pool, one mark per chosen answer.'),
        ('2c-1', 6, 9, [1, 2], 10, 8, 'One complete any-five-of-six negative-form pool, one mark per chosen answer.'),
        ('2c-2', 6, 9, [10, 11], 10, 17, 'One complete any-five-of-six verb-form pool, one mark per chosen answer.'),
        ('3c', 6, 12, [1, 2, 3], 12, 0, 'One complete any-five-of-six paired reading1/meaning1 pool.'),
        ('3d', 7, 12, [13, 14, 15], 12, 8, 'One complete any-ten-of-twelve-blank particle pool across seven sentences, one mark per chosen blank.'),
    ]:
        canonical = 'ja-2021-hl-' + suffix
        task = next(task for task in census['tasks'] if canonical == 'ja-2021-hl-' + '-'.join(str(part).lower() for part in task['key'] if part is not None))
        records.append({'canonicalId': canonical, 'legacyIds': [canonical + '-' + roman for roman in romans[:count]],
                        'taskKey': task['key'], 'marks': task['marks'], 'reason': reason,
                        'paperEvidence': {'page': pp, 'text': joined_selector('paper', pp, [(row, None) for row in pr])},
                        'schemeEvidence': {'page': sp, 'text': cell('scheme', sp, sr)}})
    return records


def build():
    reading()
    writing()
    listening()
    census = json.loads((Path(__file__).parent / 'reviews/japanese-2021-hl-census.json').read_text())
    expected = {'ja-2021-hl-' + '-'.join(str(part).lower() for part in task['key'] if part is not None): task for task in census['tasks']}
    assert set(expected) == {card['id'] for card in CARDS}
    for card in CARDS:
        task = expected[card['id']]
        assert card['totalMarks'] == task['marks'], (card['id'], card['totalMarks'], task['marks'])
        assert card['sourceEvidence']['paperPages'] == task['paperPages']
        assert card['sourceEvidence']['schemePages'] == task['schemePages']
    assert len(CARDS) == 58
    assert sum(card['totalMarks'] for card in CARDS) == 300
    return {'subjectId': 'japanese', 'sitting': '2021-hl', 'reviewedAt': '2026-11-09',
            'sources': [{'document': name, 'path': str(path.relative_to(ROOT)), 'sha256': PINNED_SOURCES[path], 'pagesReviewed': list(range(1, len(DOCS[name]) + 1))} for name, path in [('paper', PAPER), ('aural', AURAL), ('scheme', SCHEME)]],
            'cards': CARDS, 'selectors': EVIDENCE, 'status': 'source-reviewed-browser-qa-pending',
            'choiceAnalysis': census['choiceBoundaries'], 'consolidations': consolidations(census)}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    result = build()
    if args.write:
        (ROOT / 'scripts/markbank/authoring/reviews/japanese-2021-hl.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
        manifest = ROOT / 'components/MarkBank/figures-japanese.json'
        previous = json.loads(manifest.read_text())
        previous.update(FIGURES)
        manifest.write_text(json.dumps(previous, ensure_ascii=False, indent=2) + '\n')
        # Whole-page PDF extraction interleaves adjacent table cells. Preserve
        # the independently inspected physical column order for provenance.
        scheme_md = SCHEME.with_suffix('.md')
        prefix = '\n## Audited original table columns — 2021 HL pages'
        marker = prefix + ' 3, 4 and 8\n'
        original = scheme_md.read_text().split(prefix)[0]
        columns = []
        for page, y0, y1, bounds in [(3, 160, 650, [(82, 156), (160, 264), (266, 410), (411, 595)]),
                                     (4, 429, 600, [(203, 366), (369, 595)]),
                                     (8, 375, 560, [(145, 218), (219, 352), (353, 595)])]:
            for x0, x1 in bounds:
                columns.append(DOCS['scheme'][page - 1].get_text(clip=fitz.Rect(x0, y0, x1, y1), sort=True))
        scheme_md.write_text(original + marker + '\n'.join(columns))
    print(json.dumps({'cards': len(CARDS), 'marks': sum(card['totalMarks'] for card in CARDS), 'figures': len(FIGURES)}, indent=2))
