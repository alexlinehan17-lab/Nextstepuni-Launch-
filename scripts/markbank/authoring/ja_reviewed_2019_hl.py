#!/usr/bin/env python3
"""2019 Higher Japanese, independently reviewed against all original pages.

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
PAPER = ROOT / 'examiner-reports/japanese/papers/2019-hl-000-paper.pdf'
AURAL = ROOT / 'examiner-reports/japanese/papers/2019-hl-A00-paper.pdf'
SCHEME = ROOT / 'examiner-reports/japanese/schemes/2019-hl.pdf'
PINNED_SOURCES = {
    PAPER: 'c1127796075df825e5e7e676529d14e9ab3d9db3b9dae7a909e9e91abd6653c1',
    AURAL: '6b36a5c5ab891adf5c9ed0634f559d19cc08ef9699f6a658dbb6d44023cc95e4',
    SCHEME: '272b8bc5bc9e6fd7adcb43a02abed17768cc0c35e02fce8b6271e00da3fc525c',
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
    return text.replace('\xa0', ' ').rsplit('/', 1)[-1].strip()


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
    return {'kind': kind, 'label': '2019 Japanese Higher Level', 'title': 'Original examination material',
            'pages': pages, 'attribution': '© State Examinations Commission.',
            **({'presentationNote': FURIGANA_NOTE} if component == 'paper' else {}),
            '_component': component}


def add(section, q, question, rows, topic, paper_pages, scheme_pages, suffix='', rubric=None, total=None, reading=None, figure=None):
    cid = f'ja-2019-hl-{section.lower()}' + (f'-{q}' if q is not None else '') + (f'-{suffix}' if suffix else '')
    ref = f'2019 HL Section {section}' + (f' Q{q}' if q is not None else '')
    if suffix:
        ref += (' Q' if q is None else '') + ''.join(f'({part})' for part in suffix.split('-'))
    listening = section.startswith('L')
    card = {'id': cid, 'source': 'sec', 'subjectId': 'japanese', 'specVersion': 'lc-japanese-syllabus',
            'kind': 'rubric' if rubric else 'question', 'level': 'higher', 'year': 2019,
            'section': section[1:] if listening else section[0] if section[0] in '1234' else 'Q5',
            'topicId': topic, 'conceptId': concept_for(question, cid), 'questionRef': ref,
            'questionText': question, 'totalMarks': total if total is not None else row_total(rows),
            'qa': {'gates': ['verbatim', 'tariff', 'figure'], 'humanReviewedBy': 'agent-verified', 'humanReviewedAt': '2026-11-09'},
            'sourceEvidence': {'component': 'aural' if listening else 'paper', 'paperPages': paper_pages, 'schemePages': scheme_pages},
            'schemeCitation': 'Marking points quoted from the SEC marking scheme, Japanese 2019 Higher Level — © State Examinations Commission.'}
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
        language = (4, 1, 'Japanese')
    elif section == '1B':
        language = (8, 0, 'Japanese')
    if section == '2A' and q == 2:
        card['extraneousMaterialRule'] = {'multiplier': 0.5, 'sourceText': cell('scheme', 8, 32), 'schemePages': [8]}
        card['sourceEvidence']['generalSchemePages'] = [8]
    if language:
        page, row, named = language
        card['sourceEvidence']['generalSchemePages'] = [page]
        card['answerLanguageRule'] = {'otherLanguageMultiplier': 0.5, 'penalizedLanguage': named,
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
    topic = 'japanese-5-0' if section.startswith('1') else 'japanese-5-2' if section == '2A' else 'japanese-5-1'
    text = prompt(page, question_rows)
    if section == '3B' or section == '2A' and q == 2:
        text = ' '.join(p(page, row, len(ROWS['paper'][page - 1][row]) - 1) for row in question_rows)
        text = re.sub(r'^(?:[1-3]\.|\([ivx]+\))\s*', '', text)
    card = add(section, q, text, rows, topic, [page], scheme_pages, suffix or '',
               reading={'1A': [2], '1B': [4], '2A': [6], '3A': [10], '3B': [10]}[section])
    row = (10 if q == 2 else 17) if section == '2A' else {'1A': 0, '1B': 21, '3A': 0, '3B': 20}[section]
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
    return [part.strip(' ,-/.' ) for part in re.split(rf'\({marks}\s+marks?\)', text) if part.strip(' ,-/.' )]


def group_rows(card, groups):
    card['taskGroups'] = [
        {'sourceCardId': card['id'] + '-' + name, 'label': label,
         'marks': row_total(card['rows'][start:end]),
         'rowIds': [row['id'] for row in card['rows'][start:end]]}
        for name, label, start, end in groups]


def reading():
    instruction = prompt(3, [1, 2])
    labels = [p(3, row, 0) + ' ' + english(p(3, row, 1)) for row in range(4, 10)]
    add('1A', 1, instruction + '\n' + p(3, 3) + '\n' + '\n'.join(labels), [], 'japanese-5-0', [3], [7], total=6, reading=[2],
        rubric={'system': 'language-points', 'count': 6,
                'groups': [{'id': f'item-{i}', 'label': label, 'rows': [{'id': 'answer', 'text': s(7, i + 4, 1), 'marks': 1}]} for i, label in enumerate(labels, 1)],
                'taskRequirements': [instruction], 'markingGuideNote': cell('scheme', 7, 4)})
    comprehension('1A', 2, 'i', [10, 11], [point(s(7, 12))], [7])
    comprehension('1A', 2, 'ii', [13, 14], [anyn(options(7, [14], '/'), 2)], [7])
    comprehension('1A', 3, 'i', [16, 17], [point(s(7, 17))], [7])
    comprehension('1A', 3, 'ii', [19], [point(s(7, 19))], [7])
    comprehension('1A', 4, None, [21, 22], [point(s(7, 21))], [7])
    comprehension('1A', 5, 'i', [24, 25], [point(text, 2) for text in split_marks(s(7, 23), 2)], [7])
    comprehension('1A', 5, 'ii', [27, 28], [point(s(7, 25))], [7])
    comprehension('1A', 5, 'iii', [30], [point(s(7, 27))], [7])
    comprehension('1B', 1, 'i', [22, 23], [point(text) for text in split_marks(s(8, 2))], [8])
    comprehension('1B', 1, 'ii', [25, 26], [anyn(options(8, [4], '/'), 2)], [8])
    comprehension('1B', 2, 'i', [28, 29], [{'kind': 'criterion', 'verbatim': s(8, 7), 'marks': 2,
        'permittedMarks': [0, 1, 2], 'contextNote': cell('scheme', 8, 8)}], [8])
    comprehension('1B', 2, 'ii', [31], [point(text) for text in split_marks(s(8, 10))], [8])
    comprehension('1B', 3, 'i', [33, 34], [anyn(options(8, [12], '/'), 2)], [8])
    comprehension('1B', 3, 'ii', [36], [point(s(8, 14), 2)], [8])

    headers = [english(joined_selector('paper', 7, [(3, 0), (4, 0)])), p(7, 3, 1),
               joined_selector('paper', 7, [(4, 1), (5, 0)]), p(7, 3, 3)]
    labels = [p(7, row, 0) for row in [7, 8]]
    rows = [point(s(8, 21, 1), contextNote=labels[0] + ' — ' + headers[0]),
            point(s(8, 21, 2), contextNote=labels[0] + ' — ' + headers[2]),
            anyn([text.strip() for text in selected(8, [(20, 1), (22, 0)]).split('/')], 2, contextNote=labels[0] + ' — ' + headers[3]),
            point(selected(8, [(26, 1), (28, 0), (29, 0)]), contextNote=labels[1] + ' — ' + headers[0]),
            point(s(8, 25), contextNote=labels[1] + ' — ' + headers[1]),
            anyn([text.strip() for text in selected(8, [(25, 1), (27, 0)]).split('/')], 2, contextNote=labels[1] + ' — ' + headers[3])]
    instruction = prompt(7, [1])
    example = p(7, 6) + ' — ' + joined_selector('paper', 7, [(8, 1), (9, 0)])
    table = add('2A', 1, instruction + '\n' + '\n'.join(headers) + '\nPrinted examples: ' + example, rows,
                'japanese-5-2', [7], [8], reading=[6, 7], figure=crop('ja-2019-hl-2a-1', 7, [.06, .035, .96, .27], instruction))
    group_rows(table, [('uniform-1', labels[0], 0, 3), ('uniform-2', labels[1], 3, 6)])
    for roman, qr, sr in [('i', 11, 34), ('ii', 13, 36)]:
        comprehension('2A', 2, roman, [qr], [point(s(8, sr), 2)], [8])
    comprehension('2A', 2, 'iii', [15], [point(text) for text in split_marks(s(8, 38))], [8])
    comprehension('2A', 3, 'i', [18], [point(text) for text in split_marks(selected(9, [(2, 0), (3, 0)]))], [9])
    comprehension('2A', 3, 'ii', [20, 21], [anyn(options(9, [5], '/'), 2, 2, [2, 1])], [9])
    comprehension('2A', 3, 'iii', [23, 24], [point(s(9, 8), 2)], [9])
    comprehension('2A', 3, 'iv', [26, 27], [point(selected(9, [(10, 0), (11, 0)]), 2)], [9])
    add('2A', 4, prompt(7, [29]) + '\n' + p(7, 30) + ' ' + p(7, 31),
        [point(text) for text in split_marks(selected(9, [(15, 0), (16, 0), (17, 0)]))],
        'japanese-5-3', [7], [9], reading=[6])
    for section, q, pp, qr, prange, sp, sr, answer_parts, region in [
        ('2B', 1, 8, [1], range(3, 8), 9, 19, [(i, 1) for i in range(20, 25)], [.06, .055, .96, .44]),
        ('2B', 2, 8, [8, 9], range(11, 16), 9, 25, [(i, 1) for i in range(26, 31)], [.06, .46, .96, .87]),
        ('2C', 1, 9, [1, 2], range(4, 9), 10, 1, [(i, 0) for i in range(2, 7)], [.06, .055, .96, .44]),
        ('2C', 2, 9, [9], range(11, 16), 10, 7, [(i, 0) for i in range(8, 13)], [.06, .44, .96, .89]),
    ]:
        instruction = prompt(pp, qr)
        labels = [re.sub(r'\s+_+\s*$', '', p(pp, row)).strip() for row in prange]
        answers = [re.sub(r'^\([ivx]+\)\s*', '', s(sp, row, group)) for row, group in answer_parts]
        groups = [{'id': f'item-{i}', 'label': label, 'rows': [{'id': 'answer', 'text': answer, 'marks': 1}]} for i, (label, answer) in enumerate(zip(labels, answers), 1)]
        add(section, q, instruction + '\n' + p(pp, qr[-1] + 1) + '\n' + '\n'.join(labels), [],
            'japanese-5-4' if section == '2B' else 'japanese-5-5', [pp], [sp], total=5, reading=[pp],
            figure=crop(f'ja-2019-hl-{section.lower()}-{q}', pp, region, instruction),
            rubric={'system': 'language-points', 'count': 5, 'groups': groups, 'taskRequirements': [instruction], 'markingGuideNote': cell('scheme', sp, sr)})
    comprehension('3A', 1, 'i', [1], [anyn(options(10, [16, 17], '/'), 2)], [10])
    comprehension('3A', 1, 'ii', [3], [point(text) for text in split_marks(clean_tariff(s(10, 20)))], [10])
    comprehension('3A', 2, 'i', [5], [point(text) for text in split_marks(s(10, 22))], [10])
    comprehension('3A', 2, 'ii', [7, 8], [anyn(options(10, [24], '/'), 2)], [10])
    comprehension('3A', 3, 'i', [10, 11], [anyn(options(10, [27], '/'), 2)], [10])
    comprehension('3A', 3, 'ii', [13], [point(s(10, 29), 2)], [10])
    comprehension('3A', 4, 'i', [15], [point(text) for text in split_marks(s(11, 1))], [11])
    comprehension('3A', 4, 'ii', [17, 18], [point(selected(11, [(3, 0), (4, 0)]), 2)], [11])
    for q, qr, sr in [(1, 21, 7), (2, 23, 9), (3, 25, 11), (4, 27, 13)]:
        comprehension('3B', q, None, [qr], [point(s(11, sr))], [11])
    instruction = prompt(12, [1, 2])
    labels = [re.sub(r'_+', '', p(12, row)).strip() for row in range(5, 10)]
    groups = [{'id': f'item-{i}', 'label': label,
               'rows': [{'id': 'reading', 'text': s(11, i + 14, 2), 'marks': 1},
                        {'id': 'meaning', 'text': s(11, i + 14, 4), 'marks': 1}]} for i, label in enumerate(labels, 1)]
    add('3C', None, instruction + '\n' + p(12, 4) + '\n' + '\n'.join(labels), [], 'japanese-5-4', [12], [11], total=10, reading=[12],
        figure=crop('ja-2019-hl-3c', 12, [.02, .025, .98, .42], instruction),
        rubric={'system': 'language-points', 'count': 5, 'groups': groups, 'taskRequirements': [instruction], 'markingGuideNote': cell('scheme', 11, 14)})
    instruction = prompt(12, [11, 12, 13])
    groups = []
    for index, sr in enumerate(range(21, 28)):
        label = p(12, 14 + index)
        text = re.sub(r'^\([ivx]+\)\s*', '', cell('scheme', 11, sr))
        answers = [text.strip() for text in text.split('1 mark') if text.strip()]
        for blank, answer in enumerate(answers, 1):
            groups.append({'id': f'sentence-{index + 1}-blank-{blank}', 'label': label + f' — blank {blank}', 'rows': [{'id': 'answer', 'text': answer, 'marks': 1}]})
    assert len(groups) == 10
    add('3D', None, instruction + '\n' + '\n'.join(p(12, row) for row in range(14, 21)), [], 'japanese-5-5', [12], [11], total=10, reading=[12],
        figure=crop('ja-2019-hl-3d', 12, [.06, .427, .98, .91], instruction),
        rubric={'system': 'language-points', 'count': 10, 'groups': groups, 'taskRequirements': [instruction],
                'markingGuideNote': cell('scheme', 11, 20) + ' — All ten printed blanks are required. The original paper labels this D and its final sentence (vii); the scheme repeats C and (vi). The first blank accepts either printed particle, not both for two marks.'})


def steps(maximum):
    return list(range(maximum + 1))


def writing():
    for q, pp, sp, maximum, lower, threshold, length in [(4, 14, 13, 20, 15, 10, 150), (5, 16, 15, 30, 20, 15, 200)]:
        ranges = [(16, 24), (24, 31), (31, 38)] if q == 4 else [(16, 24), (24, 32), (32, 39)]
        guidance = [join_cells('scheme', sp, range(first, last), 150) for first, last in ranges]
        normal_ranges = [(0, 5), (6, 14), (15, 20)] if q == 4 else [(0, 7), (8, 20), (21, 30)]
        lower_ranges = [(0, 3), (4, 10), (11, 15)] if q == 4 else [(0, 4), (5, 12), (13, 20)]
        bands = [{'label': f'{lo}–{hi}', 'marks': list(range(lo, hi + 1)), 'guidance': [text]} for (lo, hi), text in zip(normal_ranges, guidance)]
        reduced = [{'label': f'{lo}–{hi}', 'marks': list(range(lo, hi + 1)), 'guidance': [text]} for (lo, hi), text in zip(lower_ranges, guidance)]
        rule = selected(sp, [(row, None) for row in range(9, 13)])
        if q == 4:
            instruction = prompt(14, [1, 2])
            question = instruction + '\n(a) ' + ' '.join(p(14, row) for row in range(5, 9)) + '\nOR\n(b) ' + ' '.join(p(14, row) for row in range(12, 16))
            allocation = selected(12, [(row, None) for row in range(4, 11)]) + '\n' + selected(12, [(row, None) for row in range(15, 22)])
            criteria = [{'id': f'point-{i}', 'label': f'({i})', 'maxMarks': 9, 'permittedMarks': steps(9), 'guidance': [allocation]} for i in ['i', 'ii']]
            criteria += [{'id': label.lower(), 'label': label, 'maxMarks': 1, 'permittedMarks': [0, 1], 'guidance': [allocation]} for label in ['Opening', 'Closing']]
            guide = 'Assess the one presentation option you answered. Its two content points receive up to 9 each, with opening 1 and closing 1. Use the printed 20-mark expression scale and its conditional 15-mark cap.'
        else:
            instruction = prompt(16, [1, 2, 3, 4, 5, 6])
            question = instruction + '\n' + '\n'.join(p(16, row) for row in range(7, 19))
            allocation = selected(14, [(row, None) for row in range(4, 11)])
            headings = [cell('scheme', 14, row) for row in range(12, 18)]
            criteria = [{'id': f'heading-{i}', 'label': f'Chosen heading {i}', 'maxMarks': 6, 'permittedMarks': steps(6), 'guidance': [allocation] + headings} for i in range(1, 5)]
            criteria += [{'id': 'discretionary', 'label': 'Discretionary content marks', 'maxMarks': 4, 'permittedMarks': steps(4), 'guidance': [allocation]},
                         *[{'id': label.lower(), 'label': label, 'maxMarks': 1, 'permittedMarks': [0, 1], 'guidance': [allocation]} for label in ['Opening', 'Closing']]]
            guide = 'Assess four different headings once each, up to 6 marks each. One discretionary mark under each chosen heading gives up to 4, with opening 1 and closing 1 separately. Use the printed 30-mark expression scale and its conditional 20-mark cap.'
        content_ids = [criterion['id'] for criterion in criteria]
        criteria.append({'id': 'expression', 'label': 'Expression', 'maxMarks': maximum, 'permittedMarks': steps(maximum),
            'guidance': [selected(sp, [(row, None) for row in ([38, 39] if q == 4 else [39, 40])])], 'bands': bands,
            'limits': [{'id': 'lower-e', 'maxMarks': lower, 'when': {'any': [{'criterionIds': content_ids, 'atMost': threshold}, {'length': 'characters', 'below': length}]},
                        'bands': reduced, 'guidance': [rule]}]})
        add(str(q), None, question, [], 'japanese-5-7', [pp], [sp - 1, sp], total=maximum * 2, reading=[pp],
            figure=crop(f'ja-2019-hl-{q}', pp, [.045, .025, .97, .88], question),
            rubric={'system': 'language-writing', 'taskRequirements': [instruction], 'criteria': criteria, 'markingGuideNote': guide})


def listening():
    def aq(page, rows):
        return re.sub(r'^(?:\d+\.\s*)?(?:\([ivx]+\)\s*)?(?:\([ab]\)\s*)?', '', join_cells('aural', page, rows, 300)).strip()

    def listen(part, q, suffix, qr, rows, question=None, scheme_page=None):
        pp, sp = {'A': (2, 4), 'B': (3, 4), 'C': (4, 5), 'D': (5, 6)}[part]
        card = add('L' + part, q, question or aq(pp, qr), rows,
                   {'A': 'japanese-6-1', 'B': 'japanese-6-2', 'C': 'japanese-6-0', 'D': 'japanese-6-0'}[part], [pp], [scheme_page or sp], suffix or '')
        card['sourceMaterial'] = source([pp], 'source-question', 'aural')
        card['stem'] = join_cells('aural', pp, range(1, 6 if part == 'B' else 5), 300)
        if part == 'B':
            card['stem'] += '\n' + cell('aural', 3, 6 if q == 1 else 23, 1)
        if part == 'C':
            card['stem'] += '\n' + cell('aural', 4, 5 if q == 1 else 18, 2 if q == 1 else 1)
        return card

    headers = [joined_selector('aural', 2, [(8, column), (9, column)]) for column in range(4)]
    names = [cell('aural', 2, row) for row in [10, 11, 12]]
    cells = [
        [[point(s(4, 6, 1))], [point(clean_tariff(s(4, 6, 2).rstrip(' &'))), point(s(4, 7, 1))],
         [point(cell('scheme', 4, 6, 3).split('Coach')[0].strip())],
         [point('Coach' + cell('scheme', 4, 6, 3).split('Coach')[1] + ' ' + s(4, 7, 3), 2)]],
        [[point(s(4, 9, 1))], [point(clean_tariff(s(4, 9, 2))), point(clean_tariff(s(4, 10, 1)))],
         [point(selected(4, [(9, 3), (10, 2)]))], [point(selected(4, [(9, 4), (10, 3), (11, 1)]), 2)]],
        [[point(s(4, 13, 1))],
         [point(selected(4, [(13, 2), (14, 1), (16, 0), (17, 0)]), 2,
                permittedMarks=[0, 0.5, 1, 1.5, 2])],
         [point(s(4, 13, 3))], [point(selected(4, [(13, 4), (14, 3), (15, 0)]), 2)]],
    ]
    rows, groups = [], []
    for person, values in enumerate(cells):
        for column, cell_rows in enumerate(values):
            start = len(rows)
            label = names[person] + ' — ' + headers[column]
            for row in cell_rows:
                row['contextNote'] = label
                row['kind'] = 'criterion'
                row.setdefault('permittedMarks', [0, row['marks'] / 2, row['marks']])
                row['contextNote'] += ' — ' + cell('scheme', 4, 1) + ' — Enter the final credit, including any printed Japanese-language half credit. Do not halve it again.'
                if person == 2 and column == 1:
                    row['contextNote'] += ' Use the two named-day components at 1 each, or the generic three-times-a-week partial at 1, never both. A Japanese component earns 0.5. Two named days with mixed languages earn 1.5; both in Japanese earn 1; the generic partial in Japanese earns 0.5.'
            rows.extend(cell_rows)
            groups.append((f'club-{person + 1}-cell-{column + 1}', label, start, len(rows)))
    question = cell('aural', 2, 5, 1) + '\n' + '\n'.join(headers + names)
    table = listen('A', None, None, [], rows, question)
    table['sourceEvidence']['manualLanguageCalculation'] = table.pop('answerLanguageRule')
    group_rows(table, groups)
    table['questionFigureKey'] = crop('ja-2019-hl-la', 2, [.075, .17, .97, .83], question, 'aural')
    listen('B', 1, 'i', [7], [point(s(4, 21), 2)])
    listen('B', 1, 'ii', [9], [anyn([text for text in options(4, [23], '/') if text], 3)])
    listen('B', 1, 'iii', [12], [point(text) for text in split_marks(selected(4, [(26, 0), (27, 0)]))])
    listen('B', 1, 'iv', [17], [anyn(options(4, [29], ', '), 2, 2)])
    phone = listen('B', 1, 'v', [21], [point(s(4, 31).split(':', 1)[1].strip(), 3,
        contextNote='The published scheme prices the complete phone number at 3 marks; it gives no per-digit allocation.')])
    phone['questionFigureKey'] = crop('ja-2019-hl-lb-1-v', 3, [.51, .598, .98, .69], phone['questionText'], 'aural')
    listen('B', 2, 'i', [24], [anyn(options(5, [2], '/'), 2, 2, [2, 1])], scheme_page=5)
    listen('B', 2, 'ii', [27], [point(clean_tariff(s(5, 4)), 2)], scheme_page=5)
    listen('B', 2, 'iii', [31], [anyn(options(5, [6], '/'), 2, 2, [2, 1])], scheme_page=5)
    listen('C', 1, 'i', [6], [anyn(options(5, [10], '/'), 2, 2, contextNote=cell('scheme', 5, 11))])
    partial = s(5, 13)
    partial_options = [text.strip(' ()') for text in re.split(r'\(?1 mark\)', partial) if text.strip(' ()')]
    listen('C', 1, 'ii', [9], [anyn(partial_options, 2,
        contextNote=partial + ' — These are the printed one-mark details. The response total is 2; do not add a third mark.')])
    listen('C', 1, 'iii', [11], [anyn(options(5, [15, 16], '/'), 2, 2)])
    listen('C', 1, 'iv', [14], [anyn(options(5, [18], '/'), 2, 2)])
    listen('C', 2, 'i', [19], [point(s(5, 22), 2)])
    listen('C', 2, 'ii', [21], [anyn(options(5, [24], '/'), 2, 2, [2, 1])])
    listen('C', 2, 'iii', [24], [point(s(5, 26), 2)])
    language_rows = [{'kind': 'criterion', 'verbatim': s(6, 2), 'marks': 2,
        'permittedMarks': [0, 0.5, 1, 1.5, 2],
        'contextNote': cell('scheme', 6, 3) + ' — Use English 1 plus Chinese 1, or the generic Languages partial 1, never both. '
            + cell('scheme', 4, 1) + ' — Enter final credit after that rule: a named-language component in Japanese earns 0.5; mixed-language named answers earn 1.5, both in Japanese earn 1; Languages alone in Japanese earns 0.5. Do not halve the final credit again.'}]
    languages = listen('D', None, 'i', [5, 6], language_rows)
    languages['sourceEvidence']['manualLanguageCalculation'] = languages.pop('answerLanguageRule')
    for suffix, qr, sr in [('a-ii', [8], 5), ('b-ii', [11, 12], 7), ('iii', [14], 9), ('iv', [17], 11),
                           ('a-v', [20, 21], 14), ('b-v', [23], 16), ('vi', [25], 18)]:
        listen('D', None, suffix, qr, [point(s(6, sr), 2)])
    listen('D', None, 'vii', [27, 28], [point(text) for text in split_marks(s(6, 20))])


def build():
    reading()
    writing()
    listening()
    census = json.loads((Path(__file__).parent / 'reviews/japanese-2019-hl-census.json').read_text())
    expected = {'ja-2019-hl-' + '-'.join(str(part).lower() for part in task['key'] if part is not None): task for task in census['tasks']}
    assert set(expected) == {card['id'] for card in CARDS}
    for card in CARDS:
        task = expected[card['id']]
        if task.get('paperRef'):
            card['questionRef'] = task['paperRef']
        assert card['totalMarks'] == task['marks'], (card['id'], card['totalMarks'], task['marks'])
        assert card['sourceEvidence']['paperPages'] == task['paperPages']
        assert card['sourceEvidence']['schemePages'] == task['schemePages']
    assert len(CARDS) == 69
    assert sum(card['totalMarks'] for card in CARDS) == 300
    assert sum('answerLanguageRule' in card for card in CARDS) == 29
    assert sum('manualLanguageCalculation' in card['sourceEvidence'] for card in CARDS) == 2
    return {'subjectId': 'japanese', 'sitting': '2019-hl', 'reviewedAt': '2026-11-09',
            'sources': [{'document': name, 'path': str(path.relative_to(ROOT)), 'sha256': PINNED_SOURCES[path], 'pagesReviewed': list(range(1, len(DOCS[name]) + 1))} for name, path in [('paper', PAPER), ('aural', AURAL), ('scheme', SCHEME)]],
            'cards': CARDS, 'selectors': EVIDENCE, 'status': 'source-reviewed-browser-qa-pending',
            'choiceAnalysis': census['choiceBoundaries'], 'consolidations': []}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    result = build()
    if args.write:
        (ROOT / 'scripts/markbank/authoring/reviews/japanese-2019-hl.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
        manifest = ROOT / 'components/MarkBank/figures-japanese.json'
        previous = json.loads(manifest.read_text())
        previous.update(FIGURES)
        manifest.write_text(json.dumps(previous, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'cards': len(CARDS), 'marks': sum(card['totalMarks'] for card in CARDS), 'figures': len(FIGURES)}, indent=2))


