#!/usr/bin/env python3
"""2018 Higher Japanese, independently reviewed against all original pages.

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
PAPER = ROOT / 'examiner-reports/japanese/papers/2018-hl-000-paper.pdf'
AURAL = ROOT / 'examiner-reports/japanese/papers/2018-hl-A00-paper.pdf'
SCHEME = ROOT / 'examiner-reports/japanese/schemes/2018-hl.pdf'
PINNED_SOURCES = {
    PAPER: 'c357e069eadb294aaca01c3a7e9968d0e91074e5afa1c34d0946fa38cfacfe26',
    AURAL: '3443cedcdc08f388158250787723b5d91b8d28d4559381fd240a48403be42baf',
    SCHEME: 'b945fb41c6b24288c864e28808ba4f632eaf92ab2f943d200e6717baa6d34c74',
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
    return {'kind': kind, 'label': '2018 Japanese Higher Level', 'title': 'Original examination material',
            'pages': pages, 'attribution': '© State Examinations Commission.',
            **({'presentationNote': FURIGANA_NOTE} if component == 'paper' else {}),
            '_component': component}


def add(section, q, question, rows, topic, paper_pages, scheme_pages, suffix='', rubric=None, total=None, reading=None, figure=None):
    cid = f'ja-2018-hl-{section.lower()}' + (f'-{q}' if q is not None else '') + (f'-{suffix}' if suffix else '')
    ref = f'2018 HL Section {section}' + (f' Q{q}' if q is not None else '')
    if suffix:
        ref += (' Q' if q is None else '') + ''.join(f'({part})' for part in suffix.split('-'))
    listening = section.startswith('L')
    card = {'id': cid, 'source': 'sec', 'subjectId': 'japanese', 'specVersion': 'lc-japanese-syllabus',
            'kind': 'rubric' if rubric else 'question', 'level': 'higher', 'year': 2018,
            'section': section[1:] if listening else section[0] if section[0] in '1234' else 'Q5',
            'topicId': topic, 'conceptId': concept_for(question, cid), 'questionRef': ref,
            'questionText': question, 'totalMarks': total if total is not None else row_total(rows),
            'qa': {'gates': ['verbatim', 'tariff', 'figure'], 'humanReviewedBy': 'agent-verified', 'humanReviewedAt': '2026-11-09'},
            'sourceEvidence': {'component': 'aural' if listening else 'paper', 'paperPages': paper_pages, 'schemePages': scheme_pages},
            'schemeCitation': 'Marking points quoted from the SEC marking scheme, Japanese 2018 Higher Level — © State Examinations Commission.'}
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
    elif section == '1B':
        language = (7, 6, 'Japanese')
    if section == '2A' and q == 1:
        card['extraneousMaterialRule'] = {'multiplier': 0.5, 'sourceText': cell('scheme', 8, 0), 'schemePages': [8]}
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
    topic = 'japanese-5-0' if section.startswith('1') or section == '2A' else 'japanese-5-2'
    text = prompt(page, question_rows)
    if section == '3B' or section == '2A' and q == 1:
        text = ' '.join(p(page, row, len(ROWS['paper'][page - 1][row]) - 1) for row in question_rows)
        text = re.sub(r'^(?:[1-3]\.|\([ivx]+\))\s*', '', text)
    card = add(section, q, text, rows, topic, [page], scheme_pages, suffix or '',
               reading={'1A': [2], '1B': [4], '2A': [6], '3A': [10], '3B': [10]}[section])
    row = (13 if q == 1 else 20) if section == '2A' else {'1A': 0, '1B': 13, '3A': 0, '3B': 18}[section]
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


def complete_pool(count, labels, answers, instruction, guide):
    return {'system': 'language-points', 'count': count, 'taskRequirements': [instruction],
            'groups': [{'id': f'item-{i + 1}', 'label': label, 'rows': [{'id': 'answer', 'text': answer, 'marks': 1}]}
                       for i, (label, answer) in enumerate(zip(labels, answers))], 'markingGuideNote': guide}


def reading():
    instruction = p(3, 2)
    labels = [p(3, row, 0) + ' ' + english(p(3, row, 1)) for row in range(4, 10)]
    add('1A', 1, instruction + '\n' + p(3, 3) + '\n' + '\n'.join(labels), [], 'japanese-5-0', [3], [6], total=6, reading=[2],
        rubric=complete_pool(6, labels, [s(6, row, 1) for row in range(13, 19)], instruction, cell('scheme', 6, 12)))
    for q, roman, qr, rows, sp in [
        (2, None, [10, 11], [point(s(6, 20), 2)], 6),
        (3, 'i', [13, 14], [point(s(6, 22), 2)], 6),
        (3, 'ii', [16], [point(s(6, 24), 2)], 6),
        (4, 'i', [18], [point(s(6, 26), 2)], 6),
        (4, 'ii', [20], [anyn(options(7, [1], '/'), 2)], 7),
        (5, None, [22, 23], [point(s(7, 3), 2)], 7),
        (6, None, [25], [point(s(7, 5), 2)], 7),
    ]:
        comprehension('1A', q, roman, qr, rows, [sp])
    for q, qr, rows in [(1, [14], [point(s(7, 8), 2)]), (2, [16, 17], [anyn(options(7, [10], '/'), 2, 2)]),
                        (3, [20, 21], [point(s(7, 13), 2)]), (4, [23, 24], [anyn(options(7, [15], '/'), 2)])]:
        comprehension('1B', q, None, qr, rows, [7])
    instruction = prompt(7, [0])
    headers = [selected_header for selected_header in [p(7, 4) + ' ' + p(7, 6),
        p(7, 5, 0) + ' ' + p(7, 7, 0), p(7, 5, 1) + ' ' + p(7, 7, 1) + ' ' + p(7, 8), p(7, 2, 3)]]
    names = [p(7, row, 0) for row in [9, 10, 11]]
    table_values = [
        [(1, point(s(7, 21, 2))), (2, point(s(7, 21, 3))),
         (3, anyn(selected(7, [(21, 4), (22, 2), (23, 0)]).split('/'), 1, 2))],
        [(0, point(s(7, 25, 1))), (2, point(s(7, 25, 2))),
         (3, anyn(selected(7, [(25, 3), (26, 3), (27, 0), (28, 0)]).split('/'), 1, 2))],
        [(0, point(s(7, 30, 1))), (1, point(s(7, 30, 2))), (2, point(s(7, 30, 3)))],
    ]
    rows, groups = [], []
    for person, values in enumerate(table_values):
        start = len(rows)
        for column, row in values:
            row['contextNote'] = names[person] + ' — ' + headers[column]
            rows.append(row)
        groups.append((f'person-{person + 1}', names[person], start, len(rows)))
    table = add('2A', None, instruction + '\n' + '\n'.join(headers + names), rows, 'japanese-5-0', [7], [7], reading=[6, 7],
        figure=crop('ja-2018-hl-2a', 7, [.075, .065, .95, .326], instruction))
    group_rows(table, groups)
    for roman, qr, rows in [('i', [14], [point(s(8, 2))]),
                            ('ii', [16], [anyn(s(8, 4).split('・'), 2)]), ('iii', [18], [point(s(8, 7), 2)])]:
        comprehension('2A', 1, roman, qr, rows, [8])
    comprehension('2A', 2, 'i', [21], [anyn(options(8, [10], '/'), 2)], [8])
    comprehension('2A', 2, 'ii', [23, 24], [point(clean_tariff(s(8, 13)), 2)], [8])
    local = selected(8, [(15, 0), (16, 0)])
    choices = local.split('/')
    assert len(choices) == 4
    groups = [{'id': f'location-{i + 1}', 'label': answer.strip(), 'rows': [{'id': 'answer', 'text': answer.strip(), 'marks': 2}]} for i, answer in enumerate(choices[:3])]
    groups.append({'id': 'location-4', 'label': choices[3].strip(), 'rows': [],
                   'criteria': [{'id': 'sea-or-sunrise', 'label': choices[3].strip(), 'maxMarks': 2,
                                 'permittedMarks': [0, 1, 2], 'guidance': [local]}]})
    add('2A', 2, prompt(7, [26, 27]), [], 'japanese-5-0', [7], [8], 'iii', total=4, reading=[6],
        rubric={'system': 'language-points', 'count': 2, 'groups': groups, 'taskRequirements': [prompt(7, [26, 27])], 'markingGuideNote': cell('scheme', 8, 17) + ' — Sea and its sunrise-only partial occupy this one detail slot. Award the printed 1 for sunrise alone or 2 for the full sea detail; do not select both as different details.'})
    comprehension('2A', 2, 'iv', [29, 30], [point(clean_tariff(selected(8, [(19, 0), (20, 0)])), 2)], [8])
    add('2A', 3, prompt(7, [32]) + '\n' + p(7, 33) + ' ' + p(7, 34),
        [point(text) for text in split_marks(selected(8, [(22, 0), (23, 0)]))], 'japanese-5-3', [7], [8], reading=[6])
    instruction = p(8, 3)
    labels = [p(8, row) for row in range(6, 11)]
    pairs = [{'id': f'item-{i + 1}', 'label': label, 'rows': [
        {'id': 'reading', 'text': s(9, i + 1, 2), 'marks': 1}, {'id': 'meaning', 'text': s(9, i + 1, 4), 'marks': 1}]}
        for i, label in enumerate(labels)]
    add('2B', None, instruction + '\n' + p(8, 5) + '\n' + '\n'.join(labels), [], 'japanese-5-4', [8], [9], total=10, reading=[8],
        figure=crop('ja-2018-hl-2b', 8, [.075, .055, .97, .365], instruction),
        rubric={'system': 'language-points', 'count': 5, 'taskRequirements': [instruction], 'groups': pairs, 'markingGuideNote': cell('scheme', 9, 0)})
    instruction = p(8, 14)
    answer_cells = [[(7, 1)], [(8, 1), (8, 2)], [(9, 0)], [(10, 1), (10, 3)], [(11, 1)], [(12, 1), (12, 3)], [(13, 0)]]
    groups = []
    for index, answer_set in enumerate(answer_cells):
        label = p(8, 15 + index)
        for blank, (row, group) in enumerate(answer_set, 1):
            answer = re.sub(r'^\([ivx]+\)\s*', '', clean_tariff(s(9, row, group)))
            groups.append({'id': f'sentence-{index + 1}-blank-{blank}', 'label': label + f' — blank {blank}', 'rows': [{'id': 'answer', 'text': answer, 'marks': 1}]})
    add('2C', None, instruction + '\n' + '\n'.join(p(8, row) for row in range(15, 22)), [], 'japanese-5-5', [8], [9], total=10, reading=[8],
        figure=crop('ja-2018-hl-2c', 8, [.075, .39, .97, .90], instruction),
        rubric={'system': 'language-points', 'count': 10, 'taskRequirements': [instruction], 'groups': groups, 'markingGuideNote': cell('scheme', 9, 6)})
    for roman, qr, sr in [('i', 2, 4), ('ii', 4, 6)]:
        found = comprehension('3A', 1, roman, [qr], [point(s(10, sr), 2)], [10])
        found['questionText'] = prompt(11, [1]) + ' ' + found['questionText']
    comprehension('3A', 2, None, [6], [point(s(10, 8), 2)], [10])
    comprehension('3A', 3, None, [8, 9], [anyn(options(10, [11], '/'), 1), point(s(10, 12))], [10])
    comprehension('3A', 4, None, [12], [anyn(options(10, [14], '/'), 2)], [10])
    preference, reason = s(10, 16).split('(1 mark)')
    comprehension('3A', 5, None, [14], [point(preference.strip()), point(reason.strip('/'), 2)], [10])
    comprehension('3A', 6, None, [16], [point(s(10, 19), 2)], [10])
    for q, qr, sr, marks in [(1, 19, 22, 1), (2, 21, 24, 2), (3, 23, 26, 2)]:
        comprehension('3B', q, None, [qr], [point(s(10, sr), marks)], [10])
    for section, pp, q, instruction_row, label_rows, answer_rows, region in [
        ('3C', 12, 1, 2, range(4, 9), range(2, 7), [.075, .065, .97, .46]),
        ('3C', 12, 2, 10, range(12, 17), range(8, 13), [.075, .47, .97, .90]),
        ('3D', 13, 1, 2, range(4, 9), range(15, 20), [.075, .05, .97, .45]),
        ('3D', 13, 2, 10, range(12, 17), range(21, 26), [.075, .47, .97, .91]),
    ]:
        instruction = p(pp, instruction_row)
        labels = [p(pp, row) for row in label_rows]
        answers = [clean_tariff(s(11, row, 1)) if row != 23 else re.sub(r'^\(iii\)\s*', '', s(11, row)) for row in answer_rows]
        add(section, q, instruction + '\n' + p(pp, instruction_row + 1) + '\n' + '\n'.join(labels), [],
            'japanese-5-4' if section == '3C' else 'japanese-5-5', [pp], [11], total=5, reading=[pp],
            figure=crop(f'ja-2018-hl-{section.lower()}-{q}', pp, region, instruction),
            rubric=complete_pool(5, labels, answers, instruction, cell('scheme', 11, answer_rows.start - 1)))


def steps(maximum):
    return list(range(maximum + 1))


def writing():
    for q, pp, sp, maximum, lower, threshold, length in [(4, 14, 13, 20, 15, 10, 150), (5, 16, 15, 30, 20, 15, 200)]:
        ranges = [(16, 25), (25, 34), (34, 43)] if q == 4 else [(16, 26), (26, 35), (35, 44)]
        guidance = [join_cells('scheme', sp, range(first, last), 140) for first, last in ranges]
        normal_ranges = [(0, 5), (6, 14), (15, 20)] if q == 4 else [(0, 7), (8, 20), (21, 30)]
        lower_ranges = [(0, 3), (4, 10), (11, 15)] if q == 4 else [(0, 4), (5, 12), (13, 20)]
        bands = [{'label': f'{lo}–{hi}', 'marks': list(range(lo, hi + 1)), 'guidance': [text]} for (lo, hi), text in zip(normal_ranges, guidance)]
        reduced = [{'label': f'{lo}–{hi}', 'marks': list(range(lo, hi + 1)), 'guidance': [text]} for (lo, hi), text in zip(lower_ranges, guidance)]
        rule = selected(sp, [(row, None) for row in range(9, 13)])
        if q == 4:
            instruction = p(14, 3) + ' ' + p(14, 4)
            question = instruction + '\n' + '\n'.join(p(14, row) for row in range(5, 14))
            allocation = selected(12, [(row, None) for row in range(5, 12)]) + '\n' + selected(12, [(row, None) for row in range(14, 21)])
            criteria = [{'id': f'point-{i}', 'label': f'({i})', 'maxMarks': 9, 'permittedMarks': steps(9), 'guidance': [allocation]} for i in ['i', 'ii']]
            criteria += [{'id': f'discretionary-{i}', 'label': f'Discretionary ({i})', 'maxMarks': 1, 'permittedMarks': [0, 1], 'guidance': [allocation]} for i in ['i', 'ii']]
            guide = 'Assess the one article option you answered. Its two content points receive up to 9 each, with one discretionary mark for each point. Use the printed 20-mark expression scale and its conditional 15-mark cap.'
        else:
            instruction = ' '.join(p(16, row) for row in range(5, 9))
            question = instruction + '\n' + '\n'.join(p(16, row) for row in range(9, 21))
            allocation = selected(14, [(row, None) for row in range(4, 11)])
            headings = [cell('scheme', 14, row) for row in range(12, 20)]
            criteria = [{'id': f'heading-{i}', 'label': f'Chosen heading {i}', 'maxMarks': 6, 'permittedMarks': steps(6), 'guidance': [allocation] + headings} for i in range(1, 5)]
            criteria += [{'id': 'discretionary', 'label': 'Discretionary content marks', 'maxMarks': 4, 'permittedMarks': steps(4), 'guidance': [allocation]},
                         *[{'id': label.lower(), 'label': label, 'maxMarks': 1, 'permittedMarks': [0, 1], 'guidance': [allocation]} for label in ['Opening', 'Closing']]]
            guide = 'Assess four different headings once each, up to 6 marks each. One discretionary mark under each chosen heading gives up to 4, with opening 1 and closing 1 separately. Use the printed 30-mark expression scale and its conditional 20-mark cap.'
        content_ids = [criterion['id'] for criterion in criteria]
        criteria.append({'id': 'expression', 'label': 'Expression', 'maxMarks': maximum, 'permittedMarks': steps(maximum),
            'guidance': [selected(sp, [(row, None) for row in ([43, 44] if q == 4 else [44, 45])])], 'bands': bands,
            'limits': [{'id': 'lower-e', 'maxMarks': lower, 'when': {'any': [{'criterionIds': content_ids, 'atMost': threshold}, {'length': 'characters', 'below': length}]},
                        'bands': reduced, 'guidance': [rule]}]})
        add(str(q), None, question, [], 'japanese-5-7', [pp], [sp - 1, sp], total=maximum * 2, reading=[pp],
            figure=crop(f'ja-2018-hl-{q}', pp, [.045, .025, .97, .90], question),
            rubric={'system': 'language-writing', 'taskRequirements': [instruction], 'criteria': criteria, 'markingGuideNote': guide})


def listening():
    def listen(part, q, suffix, qr, rows, question=None):
        pp = {'A': 2, 'B': 3, 'C': 4, 'D': 5}[part]
        sp = {'A': 3, 'B': 4, 'C': 5, 'D': 5 if q == 1 else 6}[part]
        text = question or re.sub(r'^\([ivx]+\)\s*', '', join_cells('aural', pp, qr, 300)).strip()
        card = add('L' + part, q, text, rows, {'A': 'japanese-6-0', 'B': 'japanese-6-2', 'C': 'japanese-6-0', 'D': 'japanese-6-0'}[part], [pp], [sp], suffix or '')
        card['sourceMaterial'] = source([pp], 'source-question', 'aural')
        card['stem'] = join_cells('aural', pp, range(1, 6 if part in 'AB' else 5), 290)
        if part == 'A':
            card['stem'] = cell('aural', 2, 1, 1) + ' about' + cell('aural', 2, 2).split('about', 1)[1] + ' ' + join_cells('aural', 2, [3, 4, 5], 290)
        else:
            row = {('B', 1): 6, ('B', 2): 19, ('B', 3): 30, ('C', 1): 5, ('C', 2): 15, ('D', 1): 5, ('D', 2): 17}[(part, q)]
            card['stem'] += '\n' + join_cells('aural', pp, [row], 300)
        return card
    headers = [selected_header for selected_header in [
        joined_selector('aural', 2, [(9, 0), (10, 0), (11, 0)]),
        joined_selector('aural', 2, [(9, 1), (10, 1)]),
        joined_selector('aural', 2, [(9, 2), (10, 2)]),
        joined_selector('aural', 2, [(9, 3), (10, 3), (11, 1)])]]
    names = [cell('aural', 2, row) for row in [12, 13, 14]]
    merged = s(3, 22)
    assert 'using phone' in merged
    photos, using = merged.split('using phone', 1)
    activities = [selected(3, [(7, 3), (8, 2), (9, 0), (10, 0)]),
                  selected(3, [(14, 3), (15, 2), (16, 0)]), selected(3, [(20, 3), (21, 2)]) + ' ' + photos.strip()]
    negatives = [selected(3, [(7, 4), (8, 3), (9, 1)]),
                 selected(3, [(14, 4), (15, 3), (16, 1)]), selected(3, [(20, 4), (21, 3)]) + ' using phone' + using + ' ' + s(3, 23, 1)]
    rows, groups = [], []
    for person, sr in enumerate([7, 14, 20]):
        for column, row in enumerate([point(s(3, sr, 1)), point(s(3, sr, 2)), anyn(activities[person].split('/'), 2), point(negatives[person], 2)]):
            label = names[person] + ' — ' + headers[column]
            row['contextNote'] = label
            start = len(rows)
            rows.append(row)
            groups.append((f'person-{person + 1}-cell-{column + 1}', label, start, len(rows)))
    question = '\n'.join(headers + names)
    table = listen('A', None, None, [], rows, question)
    group_rows(table, groups)
    table['questionFigureKey'] = crop('ja-2018-hl-la', 2, [.075, .18, .97, .72], question, 'aural')
    full = s(4, 3)
    listen('B', 1, 'i', [7], [point(full.split(' (')[0], 2, kind='criterion', permittedMarks=[0, 1, 2], contextNote=full)])
    listen('B', 1, 'ii', [10, 11], [anyn(options(4, [5], '/'), 2, 2)])
    listen('B', 1, 'iii', [14], [point(text) for text in split_marks(s(4, 8))])
    phone = listen('B', 1, 'iv', [16], [point(s(4, 10), 2, contextNote='The published scheme prices the complete phone number at 2 marks; it gives no per-digit allocation.')])
    phone['questionFigureKey'] = crop('ja-2018-hl-lb-1-iv', 3, [.52, .399, .95, .48], phone['questionText'], 'aural')
    listen('B', 2, 'i', [20, 21], [point(s(4, 13), 2, kind='criterion', permittedMarks=[0, 1, 2], contextNote=s(4, 14))])
    details = selected(4, [(16, 0), (17, 0), (18, 0)])
    details = re.sub(r'\s*\(any 2, two marks each\)$', '', details)
    listen('B', 2, 'ii', [23, 24], [anyn(details.split('/'), 2, 2)])
    listen('B', 2, 'iii', [27, 28], [point(s(4, 20), 2)])
    listen('B', 3, 'i', [31], [point(s(4, 24), 2)])
    listen('B', 3, 'ii', [33], [anyn(options(4, [26], '/'), 1, 2)])
    listen('C', 1, 'i', [6], [point(s(5, 3), 2)])
    listen('C', 1, 'ii', [8, 9], [anyn(options(5, [5, 6], '/'), 3, 2)])
    listen('C', 1, 'iii', [13], [point(s(5, 9), 2)])
    listen('C', 2, 'i', [16], [point(s(5, 12), 2)])
    listen('C', 2, 'ii', [18], [point(answer, 2) for answer in options(5, [14], '/')])
    listen('C', 2, 'iii', [22], [anyn(options(5, [17], '/'), 2, 2)])
    listen('D', 1, 'i', [6, 7], [point(s(5, 22), 2)])
    listen('D', 1, 'ii', [9], [anyn(options(5, [24], '/'), 2, 2)])
    listen('D', 1, 'iii', [12, 13], [point(answer, 2) for answer in split_marks(s(5, 27), 2)])
    who, why = selected(6, [(2, 0), (3, 0)]).split('(2 marks)', 1)
    listen('D', 2, 'i', [18], [point(who.strip(), 2), point(clean_tariff(why.strip(', ')), 2)])
    listen('D', 2, 'ii', [22, 23], [anyn(options(6, [5], '/'), 2, 2)])
    listen('D', 2, 'iii', [26], [point(s(6, 8), 2)])


def build():
    reading()
    writing()
    listening()
    census = json.loads((Path(__file__).parent / 'reviews/japanese-2018-hl-census.json').read_text())
    expected = {'ja-2018-hl-' + '-'.join(str(part).lower() for part in task['key'] if part is not None): task for task in census['tasks']}
    assert set(expected) == {card['id'] for card in CARDS}
    for card in CARDS:
        task = expected[card['id']]
        assert card['totalMarks'] == task['marks'], (card['id'], card['totalMarks'], task['marks'])
        assert card['sourceEvidence']['paperPages'] == task['paperPages']
        assert card['sourceEvidence']['schemePages'] == task['schemePages']
    assert len(CARDS) == 61
    assert sum(card['totalMarks'] for card in CARDS) == 300
    assert sum('answerLanguageRule' in card for card in CARDS) == 26
    assert sum('extraneousMaterialRule' in card for card in CARDS) == 3
    return {'subjectId': 'japanese', 'sitting': '2018-hl', 'reviewedAt': '2026-11-09',
            'sources': [{'document': name, 'path': str(path.relative_to(ROOT)), 'sha256': PINNED_SOURCES[path], 'pagesReviewed': list(range(1, len(DOCS[name]) + 1))} for name, path in [('paper', PAPER), ('aural', AURAL), ('scheme', SCHEME)]],
            'cards': CARDS, 'selectors': EVIDENCE, 'status': 'source-reviewed-browser-qa-pending',
            'choiceAnalysis': census['choiceBoundaries'], 'consolidations': []}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    result = build()
    if args.write:
        (ROOT / 'scripts/markbank/authoring/reviews/japanese-2018-hl.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
        manifest = ROOT / 'components/MarkBank/figures-japanese.json'
        previous = json.loads(manifest.read_text())
        previous.update(FIGURES)
        manifest.write_text(json.dumps(previous, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'cards': len(CARDS), 'marks': sum(card['totalMarks'] for card in CARDS), 'figures': len(FIGURES)}, indent=2))
