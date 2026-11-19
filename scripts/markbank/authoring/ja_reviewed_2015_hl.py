#!/usr/bin/env python3
"""2015 Higher Japanese, independently reviewed against all original pages.

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
PAPER = ROOT / 'examiner-reports/japanese/papers/2015-hl-000-paper.pdf'
AURAL = ROOT / 'examiner-reports/japanese/papers/2015-hl-A00-paper.pdf'
SCHEME = ROOT / 'examiner-reports/japanese/schemes/2015-hl.pdf'
PINNED_SOURCES = {
    PAPER: '91e2718a0447eca580669607a334026aff6299d0d4523e86937a43bff1b16145',
    AURAL: 'd66a1b1135ce90d812f908f6ce0db96693b679bf8cedf1eb7c85ecd640102d7f',
    SCHEME: 'eebf8e3aacf9c162bf075915785491f93d1d633d2dab3278536e6d7eea48e2e1',
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
    text = ' '.join(' '.join(cell(doc, page, row, gi) for gi, group in enumerate(ROWS[doc][page - 1][row]) if group[0] >= x_min) for row in rows)
    assert text.strip(), (doc, page, rows, x_min, 'Empty source selection')
    return text


def english(text):
    text = text.replace('\xa0', ' ')
    return (text.split(' / ', 1)[1] if ' / ' in text else text.removeprefix('NÓ/')).strip()


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


def row_total(rows):
    routes = {}
    common = 0
    for row in rows:
        if row.get('route'):
            routes[row['route']] = routes.get(row['route'], 0) + worth(row)
        else:
            common += worth(row)
    return common + max([0, *routes.values()])


def source(pages, kind='source-text', component='paper'):
    return {'kind': kind, 'label': '2015 Japanese Higher Level', 'title': 'Original examination material',
            'pages': pages, 'attribution': '© State Examinations Commission.',
            **({'presentationNote': FURIGANA_NOTE} if component == 'paper' else {}),
            '_component': component}


def add(section, q, question, rows, topic, paper_pages, scheme_pages, suffix='', rubric=None, total=None, reading=None, figure=None):
    cid = f'ja-2015-hl-{section.lower()}' + (f'-{q}' if q is not None else '') + (f'-{suffix}' if suffix else '')
    ref = f'2015 HL Section {section}' + (f' Q{q}' if q is not None else '')
    if suffix:
        ref += (' Q' if q is None else '') + ''.join(f'({part})' for part in suffix.split('-'))
    listening = section.startswith('L')
    card = {'id': cid, 'source': 'sec', 'subjectId': 'japanese', 'specVersion': 'lc-japanese-syllabus',
            'kind': 'rubric' if rubric else 'question', 'level': 'higher', 'year': 2015,
            'section': section[1:] if listening else section[0] if section[0] in '1234' else 'Q5',
            'topicId': topic, 'conceptId': concept_for(question, cid), 'questionRef': ref,
            'questionText': question, 'totalMarks': total if total is not None else row_total(rows),
            'qa': {'gates': ['verbatim', 'tariff', 'figure'], 'humanReviewedBy': 'agent-verified', 'humanReviewedAt': '2026-11-09'},
            'sourceEvidence': {'component': 'aural' if listening else 'paper', 'paperPages': paper_pages, 'schemePages': scheme_pages},
            'schemeCitation': 'Marking points quoted from the SEC marking scheme, Japanese 2015 Higher Level — © State Examinations Commission.'}
    if rubric:
        card['rubric'] = rubric
    else:
        card['tariffModel'] = {'kind': 'fixed'}
        card['rows'] = [dict(row, id=f'r-{i + 1}') for i, row in enumerate(rows)]
    original_ids = set(re.findall(r'    id: "([^"]+)"', (ROOT / 'components/MarkBank/cards/japanese/higher.ts').read_text()))
    if cid in original_ids:
        card['qa']['gates'].append('reviewed-card-correction')
    language = None
    if listening:
        language = (3, 1, 'Japanese')
    elif section in ['1A', '1B']:
        language = (5, 12, None)
    if section == '2A' and q == 2:
        page, row = (7, 18)
        card['extraneousMaterialRule'] = {'multiplier': 0.5, 'sourceText': cell('scheme', page, row), 'schemePages': [page]}
        card['sourceEvidence']['generalSchemePages'] = [page]
    if language:
        page, row, named = language
        card['sourceEvidence']['generalSchemePages'] = [page]
        card['answerLanguageRule'] = {'otherLanguageMultiplier': 0.5, **({'penalizedLanguage': named} if named else {}),
                                      'sourceText': cell('scheme', page, row), 'schemePages': [page]}
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
    return re.sub(r'\s*\(any.*$', '', text, flags=re.I).strip()


def options(page, rows, separator=', '):
    return [part.strip() for part in strip_tariff(' '.join(s(page, row) for row in rows)).split(separator)]


def comprehension(section, q, suffix, question_rows, rows, scheme_pages):
    page = 3 if section == '1A' else 4 if section == '1B' else 7 if section == '2A' else 11
    topic = 'japanese-5-0' if section.startswith('1') else 'japanese-5-0' if section == '2A' else 'japanese-5-1'
    text = prompt(page, question_rows)
    if section == '3B' or section == '2A' and q == 2:
        text = ' '.join(p(page, row, len(ROWS['paper'][page - 1][row]) - 1) for row in question_rows)
        text = re.sub(r'^(?:[1-3]\.|\([ivx]+\))\s*', '', text)
    card = add(section, q, text, rows, topic, [page], scheme_pages, suffix or '',
               reading={'1A': [2], '1B': [4], '2A': [6], '3A': [10], '3B': [10]}[section])
    instruction_row = (12 if q == 2 else 21) if section == '2A' else {'1A': 1, '1B': 16, '3A': 0, '3B': 23}[section]
    card['stem'] = english(p(page, instruction_row)) if section != '1A' else 'Refer to the original Kellogg’s webpage.'
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
    return [part.strip(' ,-/.' ) for part in re.split(rf'\({marks}\s+marks?\)', text) if part.strip(' ,-/.' )]


def group_rows(card, groups):
    card['taskGroups'] = [
        {'sourceCardId': card['id'] + '-' + name, 'label': label,
         'marks': row_total(card['rows'][start:end]),
         'rowIds': [row['id'] for row in card['rows'][start:end]]}
        for name, label, start, end in groups]


def complete_pool(count, labels, answers, instruction, guide):
    return {'system': 'language-points', 'count': count, 'taskRequirements': [instruction],
            'groups': [{'id': f'item-{i + 1}', 'label': label, 'rows': [{'id': 'answer', 'text': answer, 'marks': 1}]}
                       for i, (label, answer) in enumerate(zip(labels, answers))], 'markingGuideNote': guide}


def reading():
    instruction = p(3, 1)
    labels = [english(p(3, r, 1 if r in [3, 4, 7] else 0)) for r in range(3, 9)]
    add('1A', 1, instruction + '\n' + '\n'.join(labels), [], 'japanese-5-0', [3], [5], total=6, reading=[2],
        rubric=complete_pool(6, labels, [s(5, r, 1) for r in range(15, 21)], instruction, cell('scheme', 5, 14)))
    for roman, qr, sr in [('i', 10, 22), ('ii', 13, 25)]:
        comprehension('1A', 2, roman, [qr], [anyn(options(5, [sr], '/'), 2)], [5])
    for roman, qr, sr in [('i', 17, 1), ('ii', 18, 2), ('iii', 19, 3)]:
        answer = s(6, sr, 1).split('? ', 1)[1] if sr == 1 else s(6, sr, 2)
        question = p(3, 16) + ' ' + english(p(3, qr, 1 if qr < 19 else 0)).split('_', 1)[0].strip()
        comprehension('1A', 3, roman, [qr], [point(answer, 2)], [6])['questionText'] = question
    comprehension('1A', 4, 'i', [21], [point(s(6, 5), 2)], [6])
    recipe = selected(6, [(7, 0), (8, 0)]).split('/')
    comprehension('1A', 4, 'ii', [24], [anyn([v.strip() for v in recipe], 2, 2)], [6])
    comprehension('1B', 1, None, [17], [point(s(6, 11), 2)], [6])
    comprehension('1B', 2, None, [19], [anyn(options(6, [13], '/'), 2)], [6])
    comprehension('1B', 3, None, [21], [point(s(6, 15), 2)], [6])
    comprehension('1B', 4, None, [23, 24], [point(answer) for answer in split_marks(s(6, 18))], [6])

    headers = [p(7, 4, 0) + ' ' + p(7, 5, 0), p(7, 4, 1), p(7, 3, 3), p(7, 4, 2) + ' ' + p(7, 5, 1)]
    names = [p(7, r, 0) for r in [7, 9, 11]]
    values = [
        [[point(clean_tariff(s(7, 6, 2)))], [point(clean_tariff(s(7, 6, 3)).rstrip(' &')), point(clean_tariff(s(7, 8)))], [point(s(7, 5, 0))], [point(s(7, 5, 1))]],
        [[point(clean_tariff(s(7, 11, 0)))], [point(clean_tariff(s(7, 11, 1)).rstrip(' &')), point(clean_tariff(s(7, 13)))], [point(s(7, 9))], []],
        [[point(clean_tariff(s(7, 14, 0)))], [], [point(s(7, 14, 1))], [point(s(7, 14, 2))]],
    ]
    rows, groups = [], []
    for person, cells in enumerate(values):
        for col, components in enumerate(cells):
            if not components:
                continue
            label = names[person] + ' — ' + headers[col]
            start = len(rows)
            rows += [dict(row, contextNote=label) for row in components]
            groups.append((f'course-{person + 1}-cell-{col + 1}', label, start, len(rows)))
    # Both days are individually priced; remove the ampersand after the tariff first.
    for row in rows:
        row['verbatim'] = re.sub(r'\s*\(1 mark\)\s*&?$', '', row['verbatim'])
    table = add('2A', 1, english(p(7, 1)) + '\n' + '\n'.join(headers + names), rows, 'japanese-5-0', [7], [7], reading=[6])
    group_rows(table, groups)
    table['questionFigureKey'] = crop('ja-2015-hl-2a-1', 7, [.06, .06, .95, .318], table['questionText'])
    for roman, qr, sr in [('i', 13, 20), ('ii', 15, 22), ('iii', 17, 24), ('iv', 19, 27)]:
        answer = selected(7, [(24, 0), (25, 0)]) if sr == 24 else s(7, sr)
        comprehension('2A', 2, roman, [qr], [point(answer, 2)], [7])
    for roman, qr, sp, sr in [('i', 23, 7, 30), ('ii', 25, 7, 32), ('iii', 27, 8, 1)]:
        comprehension('2A', 3, roman, [qr], [anyn(options(sp, [sr], '/'), 1, 2)], [sp])
    translation = add('2A', 4, prompt(7, [29]) + '\n' + p(7, 30), [point(answer, 2) for answer in split_marks(s(8, 4), 2)], 'japanese-5-3', [7], [8], reading=[6])
    translation['stem'] = p(7, 30)
    for q, qr, sr in [(1, 4, 7), (2, 12, 13)]:
        labels = [p(8, r, 1) for r in range(qr, qr + 5)]
        instruction = p(8, 2 if q == 1 else 10)
        card = add('2B', q, instruction + '\n' + '\n'.join(labels), [], 'japanese-5-4', [8], [8], total=5, reading=[6],
                   rubric=complete_pool(5, labels, [s(8, r, 1) for r in range(sr, sr + 5)], instruction, cell('scheme', 8, 6 if q == 1 else 12)))
        card['questionFigureKey'] = crop(f'ja-2015-hl-2b-{q}', 8, [.06, .03 if q == 1 else .44, .94, .435 if q == 1 else .82], card['questionText'])
    for q, qr, sp, sr in [(1, 4, 8, 20), (2, 12, 9, 1)]:
        labels = [p(9, r, 1) for r in range(qr, qr + 5)]
        instruction = p(9, 2 if q == 1 else 10)
        answers = [re.sub(r'^[a-e]\.\s*', '', s(sp, r)) for r in range(sr, sr + 5)]
        card = add('2C', q, instruction + '\n' + '\n'.join(labels), [], 'japanese-5-5', [9], [sp], total=5, reading=[6],
                   rubric=complete_pool(5, labels, answers, instruction, cell('scheme', sp, 19 if q == 1 else 0)))
        card['questionFigureKey'] = crop(f'ja-2015-hl-2c-{q}', 9, [.06, .03 if q == 1 else .43, .97, .40 if q == 1 else .77], card['questionText'])

    comprehension('3A', 1, 'i', [1, 2], [anyn(options(10, [3], '/'), 2, 1, [2, 1], contextNote=cell('scheme', 10, 4))], [10])
    comprehension('3A', 1, 'ii', [5, 6], [{'kind': 'criterion', 'verbatim': s(10, 6), 'marks': 2, 'permittedMarks': [0, 1, 2], 'contextNote': cell('scheme', 10, 7)}], [10])
    comprehension('3A', 2, 'i', [9], [anyn(clean_tariff(s(10, 9)).split('/'), 1, 2)], [10])
    comprehension('3A', 2, 'ii', [12], [anyn(options(10, [11], '/'), 2)], [10])
    variants = [{'id': name.lower(), 'label': name, 'rows': [dict(anyn(options(10, [sr], '/'), 2, 1, [2, 1], contextNote=cell('scheme', 10, 16)), id='r-1')]}
                for name, sr in [('Nicole', 14), ('Michael', 15)]]
    person = comprehension('3A', 3, 'i', [15, 16], variants[0]['rows'], [10])
    person['answerVariants'] = variants
    comprehension('3A', 3, 'ii', [19, 20], [anyn(options(10, [18], '/'), 1, 2)], [10])
    comprehension('3B', 1, None, [24], [anyn(s(10, 22).split('／'), 2, 1, [2, 1], contextNote=cell('scheme', 10, 23))], [10])
    comprehension('3B', 2, None, [26], [{'kind': 'criterion', 'verbatim': s(10, 25), 'marks': 3, 'permittedMarks': [0, 2, 3], 'contextNote': cell('scheme', 10, 26)}], [10])
    instruction = p(12, 3)
    groups = []
    labels = []
    for i, sr in enumerate(range(28, 33)):
        label = p(12, i + 6).split('_', 1)[0].strip()
        labels.append(label)
        groups.append({'id': f'item-{i + 1}', 'label': label, 'rows': [{'id': 'reading', 'text': s(10, sr, 2), 'marks': 1}, {'id': 'meaning', 'text': s(10, sr, 4), 'marks': 1}]})
    card = add('3C', None, instruction + '\n' + '\n'.join(labels), [], 'japanese-5-4', [12], [10], total=10, reading=[10],
               rubric={'system': 'language-points', 'count': 5, 'groups': groups, 'taskRequirements': [instruction], 'markingGuideNote': cell('scheme', 10, 27)})
    card['questionFigureKey'] = crop('ja-2015-hl-3c', 12, [.015, .025, .975, .455], card['questionText'])
    labels, answers = [], []
    for i, sr in enumerate(range(1, 8)):
        label = p(12, 15 + i)
        for blank, gi in enumerate([0, 2] if i < 3 else [0], 1):
            labels.append(label + (f' — blank {blank}' if i < 3 else ''))
            answers.append(re.sub(r'^\([ivx]+\)\s*', '', s(11, sr, gi)))
    instruction = p(12, 14)
    card = add('3D', None, instruction + '\n' + '\n'.join(p(12, r) for r in range(15, 22)), [], 'japanese-5-5', [12], [11], total=10, reading=[10],
               rubric=complete_pool(10, labels, answers, instruction, cell('scheme', 11, 0)))
    card['questionFigureKey'] = crop('ja-2015-hl-3d', 12, [.06, .46, .975, .94], card['questionText'])


def steps(maximum):
    return list(range(maximum + 1))


def writing():
    for q, pp, sp, maximum, lower, threshold, length in [(4, 14, 13, 20, 15, 10, 150), (5, 16, 15, 30, 20, 15, 200)]:
        guidance = [join_cells('scheme', sp, range(first, last), 150) for first, last in [(16, 23), (23, 30), (30, 37)]]
        if q == 5:
            guidance[2] = re.sub(r'^21\s*-\s*30\s*', '', cell('scheme', sp, 30, 1)) + ' ' + join_cells('scheme', sp, range(31, 37), 167)
        normal = [(0, 5), (6, 14), (15, 20)] if q == 4 else [(0, 7), (8, 20), (21, 30)]
        low = [(0, 3), (4, 10), (11, 15)] if q == 4 else [(0, 4), (5, 12), (13, 20)]
        bands = [{'label': f'{lo}–{hi}', 'marks': list(range(lo, hi + 1)), 'guidance': [text]} for (lo, hi), text in zip(normal, guidance)]
        reduced = [{'label': f'{lo}–{hi}', 'marks': list(range(lo, hi + 1)), 'guidance': [text]} for (lo, hi), text in zip(low, guidance)]
        allocation = selected(sp - 1, [(r, None) for r in (range(14, 19) if q == 4 else range(11, 16))])
        if q == 4:
            instruction = p(14, 2)
            question = instruction + '\n' + '\n'.join(p(14, r) for r in [3, 4, 7, 8, 9, 10, 11, 12, 13, 16, 17, 18, 19])
            criteria = [{'id': f'point-{i}', 'label': f'Content point {i}', 'maxMarks': 8, 'permittedMarks': steps(8), 'guidance': [allocation]} for i in [1, 2]]
            discretionary = 2
            guide = 'Assess one complete e-mail option. Two content responses earn up to 8 each. The four discretionary content marks include opening 1 and closing 1; the other two remain global, with no invented one-per-point restriction. Lower E applies at content 10 or less, or below 150 characters.'
        else:
            instruction = p(16, 4) + ' ' + p(16, 5)
            headings = []
            for rows in [[6, 7], [8, 9], [10, 11], [12, 13, 14], [15, 16, 17], [18, 19]]:
                first = rows[0]
                jp = p(16, first, 0) + ' ' + p(16, first, 1)
                en = english(' '.join(p(16, r, 2 if r == first else 0) for r in rows))
                headings.append(jp + ' — ' + en)
            question = instruction + '\n' + '\n'.join(headings)
            criteria = [{'id': f'heading-{i}', 'label': f'Chosen heading {i}', 'maxMarks': 6, 'permittedMarks': steps(6), 'guidance': [allocation, selected(14, [(r, None) for r in range(3, 11)])]} for i in range(1, 5)]
            discretionary = 4
            guide = 'Assess four different headings once each, up to 6 marks each. Six discretionary content marks include opening 1 and closing 1; the remaining four stay global, without an invented one-per-heading limit. Lower E applies at content 15 or less, or below 200 characters.'
        criteria.append({'id': 'discretionary', 'label': 'Other discretionary content marks', 'maxMarks': discretionary, 'permittedMarks': steps(discretionary), 'guidance': [allocation]})
        criteria += [{'id': label.lower(), 'label': label, 'maxMarks': 1, 'permittedMarks': [0, 1], 'guidance': [allocation]} for label in ['Opening', 'Closing']]
        content_ids = [criterion['id'] for criterion in criteria]
        criteria.append({'id': 'expression', 'label': 'Expression', 'maxMarks': maximum, 'permittedMarks': steps(maximum), 'bands': bands,
                         'guidance': [selected(sp, [(37, None), (38, None)])],
                         'limits': [{'id': 'lower-e', 'maxMarks': lower, 'when': {'any': [{'criterionIds': content_ids, 'atMost': threshold}, {'length': 'characters', 'below': length}]}, 'bands': reduced, 'guidance': [selected(sp, [(r, None) for r in range(9, 13)])]}]})
        add(str(q), None, question, [], 'japanese-5-7', [pp], [sp - 1, sp], total=maximum * 2, reading=[pp],
            figure=crop(f'ja-2015-hl-{q}', pp, [.045, .025, .97, .92], question),
            rubric={'system': 'language-writing', 'taskRequirements': [instruction], 'criteria': criteria, 'markingGuideNote': guide})


def listening():
    def listen(part, q, suffix, qr, rows, question=None, rubric=None, total=None):
        pp = {'A': 2, 'B': 3, 'C': 4, 'D': 5}[part]
        sp = 3 if part in 'AB' and q != 3 else 5 if part == 'D' and q >= 3 else 4
        text = question or re.sub(r'^(?:\([ivx]+\)|\d+\.)\s*', '', join_cells('aural', pp, qr, 300)).strip()
        card = add('L' + part, q, text, rows, {'A': 'japanese-6-1', 'B': 'japanese-6-2', 'C': 'japanese-6-0', 'D': 'japanese-6-0'}[part], [pp], [sp], suffix or '', rubric=rubric, total=total)
        card['sourceMaterial'] = source([pp], 'source-question', 'aural')
        card['stem'] = join_cells('aural', pp, range(1, 6 if part == 'B' else 5), 300)
        if part in 'BC':
            row = {('B', 1): 6, ('B', 2): 18, ('B', 3): 25, ('C', 1): 5, ('C', 2): 21}[(part, q)]
            card['stem'] += '\n' + join_cells('aural', pp, [row], 300)
        return card

    headers = [cell('aural', 2, 8, col) + ' ' + cell('aural', 2, 9, col) + (' ' + cell('aural', 2, 10, 0) if col == 1 else '') for col in range(4)]
    names = [cell('aural', 2, r, 0) for r in [11, 12, 13]]
    values = [
        [[point(clean_tariff(s(3, 6, 1))), point(s(3, 7, 0))], [anyn(s(3, 6, 2).split('/'), 2)], [point(s(3, 6, 3))], [point(selected(3, [(6, 4), (7, 3), (8, 2)]))]],
        [[point(clean_tariff(s(3, 10, 1))), point(clean_tariff(s(3, 11, 0)))], [anyn(s(3, 10, 2).split('/'), 2)], [point(s(3, 10, 3))], [point(selected(3, [(10, 4), (11, 3), (12, 1)]))]],
        [[point(selected(3, [(14, 1), (15, 0)]), 2)], [anyn(selected(3, [(14, 2), (15, 1)]).split('/'), 2)], [point(s(3, 14, 3))], [point(selected(3, [(14, 4), (15, 3)]))]],
    ]
    rows, groups = [], []
    for person, cells in enumerate(values):
        for col, components in enumerate(cells):
            label = names[person] + ' — ' + headers[col]
            start = len(rows)
            rows += [dict(row, contextNote=label) for row in components]
            groups.append((f'person-{person + 1}-cell-{col + 1}', label, start, len(rows)))
    table = listen('A', None, None, [], rows, cell('aural', 2, 5, 1) + '\n' + '\n'.join(headers + names))
    group_rows(table, groups)
    table['questionFigureKey'] = crop('ja-2015-hl-la', 2, [.06, .025, .975, .64], table['questionText'], 'aural')
    listen('B', 1, 'i', [7], [point(s(3, 20, 1), 2)])
    listen('B', 1, 'ii', [9], [point(answer) for answer in split_marks(s(3, 21, 1))])
    listen('B', 1, 'iii', [11], [point(s(3, 22, 1), 2)])
    unpriced = listen('B', 1, 'iv', [13], [point(s(3, 24), 3)])
    unpriced['tariffModel'] = {'kind': 'questionTotal'}
    unpriced['rows'][0]['marks'] = None
    unpriced['rows'][0]['contextNote'] = ('The paper requests three items and the scheme prints a 3-mark total, but no per-item allocation. All six accepted options are retained. Marks are not calculated because the response split is unpublished; use confidence review and consult examiner guidance for an exact award. ' + unpriced['answerLanguageRule']['sourceText'])
    del unpriced['answerLanguageRule']
    unpriced['qa']['gates'].remove('tariff')
    unpriced['qa']['gates'].append('source-tariff-unresolved')
    unpriced['sourceEvidence']['scoringClarification'] = {'status': 'unpublished-response-allocation', 'sourceText': cell('scheme', 3, 24), 'issue': 'Three requested items and total 3 without a published per-item split. Confidence review only; no inferred partial allocation.', 'resolution': None}
    phone = listen('B', 1, 'v', [15], [point(s(3, 25, 1), 3, contextNote='The scheme prices the complete telephone number at 3 marks. The paper has eight missing digits; no per-digit allocation is published.')])
    phone['questionFigureKey'] = crop('ja-2015-hl-lb-1-v', 3, [.51, .45, .96, .55], phone['questionText'], 'aural')

    pool = selected(3, [(28, 0), (29, 0), (30, 0)])
    question = join_cells('aural', 3, [19, 20], 300)
    groups = [{'id': f'response-{i}', 'label': f'Distinct response {i}', 'rows': [], 'criteria': [{'id': f'response-{i}', 'label': f'Distinct response {i}', 'maxMarks': 2, 'permittedMarks': [0, 1, 2], 'guidance': [pool]}]} for i in [1, 2, 3]]
    frankl = listen('B', 2, None, [], [], question, rubric={'system': 'language-points', 'count': 3, 'groups': groups, 'taskRequirements': [question],
        'markingGuideNote': 'Assess three distinct responses against the complete printed pool above. Award 2 for a full printed detail or 1 for the printed popular partial; do not count a partial and full version of the same answer twice. The scheme does not attach popular to one specific full detail, so no exclusive association is inferred. Many languages and twelve languages refer to one fact in the transcript: count that language concept once. Street performer and juggler remain distinct printed details. All other response slots remain independently assessable.'}, total=6)
    selected(16, [(r, None) for r in range(25, 32)])
    frankl['sourceEvidence']['interpretiveSchemePages'] = [16]
    for roman, qr, sr in [('i', 26, 2), ('ii', 28, 5)]:
        listen('B', 3, roman, [qr], [anyn(options(4, [sr], '/'), 2, 1, [2, 1], contextNote=cell('scheme', 4, 3 if sr == 2 else 6))])
    listen('C', 1, 'i', [7], [{'kind': 'criterion', 'verbatim': s(4, 11), 'marks': 2, 'permittedMarks': [0, 1, 2], 'contextNote': cell('scheme', 4, 12)}])
    listen('C', 1, 'ii', [10, 11], [point(answer) for answer in split_marks(s(4, 14))])
    listen('C', 1, 'iii', [13], [anyn(options(4, [16], '/'), 2, 1, [2, 1], contextNote=cell('scheme', 4, 17))])
    listen('C', 1, 'iv', [16, 17], [anyn(options(4, [19], '/'), 2, 2)])
    listen('C', 2, 'i', [22, 23], [anyn(options(4, [23], '/'), 2, 1, [2, 1], contextNote=cell('scheme', 4, 24))])
    listen('C', 2, 'ii', [26], [anyn(options(4, [26], '/'), 1, 2)])
    listen('C', 2, 'iii', [28, 29], [anyn(options(4, [28], '/'), 2, 2)])
    listen('D', 1, None, [5], [anyn(options(4, [32], '/'), 2, 2)])
    listen('D', 2, None, [9], [anyn(options(4, [35], '/'), 2, 1, [2, 1], contextNote=cell('scheme', 4, 36))])
    listen('D', 3, None, [13, 14], [anyn(options(5, [1], '/'), 2, 1, [2, 1], contextNote=cell('scheme', 5, 2))])
    for q, qr, sr in [(4, [16], 4), (5, [18, 19], 6), (6, [21], 8), (7, [24, 25], 10)]:
        listen('D', q, None, qr, [point(s(5, sr), 2)])




def build():
    reading(); writing(); listening()
    census=json.loads((Path(__file__).parent/'reviews/japanese-2015-hl-census.json').read_text())
    expected={'ja-2015-hl-'+'-'.join(str(part).lower() for part in task['key'] if part is not None):task for task in census['tasks']}
    assert set(expected)=={card['id'] for card in CARDS},(set(expected)-{card['id'] for card in CARDS},{card['id'] for card in CARDS}-set(expected))
    for card in CARDS:
        task=expected[card['id']]
        assert card['totalMarks']==task['marks'],(card['id'],card['totalMarks'],task['marks'])
        assert card['sourceEvidence']['paperPages']==task['paperPages']
        assert card['sourceEvidence']['schemePages']==task['schemePages']
    for card in CARDS:
        rubric = card.get('rubric', {})
        for criterion in rubric.get('criteria', []) + [criterion for group in rubric.get('groups', []) for criterion in group.get('criteria', [])]:
            guidance = criterion.get('guidance', []) + [text for band in criterion.get('bands', []) for text in band['guidance']]
            guidance += [text for limit in criterion.get('limits', []) for text in limit['guidance']]
            guidance += [text for limit in criterion.get('limits', []) for band in limit.get('bands', []) for text in band['guidance']]
            assert all(text.strip() for text in guidance), (card['id'], criterion['id'], 'Empty source guidance')
    assert len(CARDS)==60
    assert sum(card['totalMarks'] for card in CARDS)==300
    assert sum('answerLanguageRule' in card for card in CARDS)==34
    assert sum('extraneousMaterialRule' in card for card in CARDS)==4
    assert '\ufffd' not in json.dumps([CARDS,EVIDENCE],ensure_ascii=False)
    return {'subjectId':'japanese','sitting':'2015-hl','reviewedAt':'2026-11-09',
        'sources':[{'document':name,'path':str(path.relative_to(ROOT)),'sha256':PINNED_SOURCES[path],'pagesReviewed':list(range(1,len(DOCS[name])+1))} for name,path in [('paper',PAPER),('aural',AURAL),('scheme',SCHEME)]],
        'cards':CARDS,'selectors':EVIDENCE,'status':'source-captured-with-unresolved-tariff', 'unresolvedSourceIssues':[{'cardId':'ja-2015-hl-lb-1-iv','kind':'unpublished-response-allocation','paperPages':[3],'schemePages':[3],'resolution':None,'runtimeTreatment':'Unpriced confidence review with all six accepted options and the printed question total; general listening language directive visible, no numeric partial model.'}],'choiceAnalysis':census['choiceBoundaries'],'consolidations':[]}


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--write',action='store_true');args=parser.parse_args()
    result=build()
    if args.write:
        scheme_text=''.join(f'\n## Page {i+1}\n\n'+page.get_text(sort=True) for i,page in enumerate(DOCS['scheme']))
        scheme_text+='\n## Original text with furigana folded at its printed character\n'
        scheme_text+=''.join(f'\n### Physical page {i+1}\n\n'+'\n'.join(' '.join(group[2] for group in row) for row in rows)+'\n' for i,rows in enumerate(ROWS['scheme']))
        for page,x_ranges in [(3,[(78,188),(188,331),(331,415),(415,590)]),(7,[(135,230),(231,350),(350,430),(430,590)])]:
            scheme_text+=f'\n## Original table columns — physical page {page}\n'
            scheme_text+='\n'.join(DOCS['scheme'][page-1].get_text(clip=fitz.Rect(x0,0,x1,DOCS['scheme'][page-1].rect.height),sort=True) for x0,x1 in x_ranges)
        SCHEME.with_suffix('.md').write_text(scheme_text.rstrip()+'\n')
        (ROOT/'scripts/markbank/authoring/reviews/japanese-2015-hl.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
        manifest=ROOT/'components/MarkBank/figures-japanese.json'; previous=json.loads(manifest.read_text());previous.update(FIGURES)
        manifest.write_text(json.dumps(previous,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'cards':len(CARDS),'marks':sum(card['totalMarks'] for card in CARDS),'figures':len(FIGURES)},indent=2))
