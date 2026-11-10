#!/usr/bin/env python3
"""2012 Higher Japanese, independently reviewed against all original pages.

Selectors below are coordinates in ja_text.page_rows, not transcribed answers.
Every question comes from the paper; every answer and tariff wording from the
scheme. Choice pools are kept whole. All original-source selectors and final crops are verified.
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
PAPER = ROOT / 'examiner-reports/japanese/papers/2012-hl-000-paper.pdf'
AURAL = ROOT / 'examiner-reports/japanese/papers/2012-hl-A00-paper.pdf'
SCHEME = ROOT / 'examiner-reports/japanese/schemes/2012-hl.pdf'
PINNED_SOURCES = {
    PAPER: '7fd8f6abeb2e7a8ca2b953fd94a0570d3449f40ad58cbd8d478a24b3b9963130',
    AURAL: '2e741b464b4af7f55b555a54db4000c1f784c3a727e38865f7390a6bae81958f',
    SCHEME: 'f976e52a9df6dfb58cd5887e5d003fe5fe2307907d71d0cf515f083fd184e6d5',
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
    return {'kind': kind, 'label': '2012 Japanese Higher Level', 'title': 'Original examination material',
            'pages': pages, 'attribution': '© State Examinations Commission.',
            **({'presentationNote': FURIGANA_NOTE} if component == 'paper' else {}),
            '_component': component}


def add(section, q, question, rows, topic, paper_pages, scheme_pages, suffix='', rubric=None, total=None, reading=None, figure=None):
    cid = f'ja-2012-hl-{section.lower()}' + (f'-{q}' if q is not None else '') + (f'-{suffix}' if suffix else '')
    ref = f'2012 HL Section {section}' + (f' Q{q}' if q is not None else '')
    if suffix:
        ref += (' Q' if q is None else '') + ''.join(f'({part})' for part in suffix.split('-'))
    listening = section.startswith('L')
    card = {'id': cid, 'source': 'sec', 'subjectId': 'japanese', 'specVersion': 'lc-japanese-syllabus',
            'kind': 'rubric' if rubric else 'question', 'level': 'higher', 'year': 2012,
            'section': section[1:] if listening else section[0] if section[0] in '1234' else 'Q5',
            'topicId': topic, 'conceptId': concept_for(question, cid), 'questionRef': ref,
            'questionText': question, 'totalMarks': total if total is not None else row_total(rows),
            'qa': {'gates': ['verbatim', 'tariff', 'figure'], 'humanReviewedBy': 'agent-verified', 'humanReviewedAt': '2026-11-10'},
            'sourceEvidence': {'component': 'aural' if listening else 'paper', 'paperPages': paper_pages, 'schemePages': scheme_pages},
            'schemeCitation': 'Marking points quoted from the SEC marking scheme, Japanese 2012 Higher Level — © State Examinations Commission.'}
    if rubric:
        card['rubric'] = rubric
    else:
        card['tariffModel'] = {'kind': 'fixed'}
        card['rows'] = [dict(row, id=f'r-{i + 1}') for i, row in enumerate(rows)]
    original_ids = set(re.findall(r'    id: "([^"]+)"', (ROOT / 'components/MarkBank/cards/japanese/higher.ts').read_text()))
    if cid in original_ids:
        card['qa']['gates'].append('reviewed-card-correction')
    language = None
    if section in ['LA', 'LB']:
        language = (3, 2, 'Japanese') if section == 'LA' else (4, 1, 'Japanese')
    elif section == '3B':
        language = (11, 16, 'English')
        condition = joined_selector('scheme', 11, [(14, 1), (15, 0)])
        label = condition.split('; ', 1)[1].split(': half marks.', 1)[0]
        assert label == 'quotation without manipulation where manipulation required or containing extraneous material'
        card['extraneousMaterialRule'] = {'multiplier': 0.5, 'conditionLabel': label,
                                          'sourceText': condition, 'schemePages': [11]}
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


def criterion(answer, maximum, permitted, note):
    return {'kind': 'criterion', 'verbatim': answer, 'marks': maximum, 'permittedMarks': permitted, 'contextNote': note}


def unnumber(text):
    return re.sub(r'^\([ivx]+\)\s*', '', text).strip()


def response_pool(text, count, marks, instruction):
    """Printed pool with manual response slots; no invented semantic equivalences."""
    return [criterion(text, marks, [0, marks], f'Response {i + 1} of {count}. {instruction} Count distinct answers only; do not award the same fact twice.') for i in range(count)]


def reading_q1():
    instruction = join_cells('paper', 3, range(3), 300)
    labels = [p(3, 4, 1).split('a. ', 1)[1], p(3, 5, 1), p(3, 7, 1), p(3, 9, 1),
              p(3, 11, 1).split('e. ', 1)[1], p(3, 13, 1), p(3, 15, 1).split('g. ', 1)[1], p(3, 16, 1)]
    answers = [s(7, r, 1) for r in [3, 4, 5, 6, 7, 8, 9, 11]]
    rows = [point(a, contextNote=l + ('. ' + cell('scheme', 7, 10) if i == 6 else '')) for i, (l, a) in enumerate(zip(labels, answers))]
    c = add('1A', None, instruction + '\n' + '\n'.join(labels), rows, 'japanese-5-0', [3], [7], reading=[2],
            figure=crop('ja-2012-hl-1a', 3, [.065, .025, .97, .495], instruction))
    group_rows(c, [(f'link-{i + 1}', labels[i], i, i + 1) for i in range(8)])
    rows, groups = [], []
    for dog, sr, pr in [(1, 15, 22), (2, 17, 24), (3, 19, 26)]:
        start = len(rows)
        for col in range(3):
            answer = s(7, sr, col + 2)
            if dog == 3 and col == 2: answer = clean_tariff(selected(7, [(19, 4), (20, 2)]))
            rows.append(point(answer, contextNote=p(3, pr, 0) + ' — ' + english(p(3, 20, col + 1))))
            cell('scheme', 7, sr + 1, col)
        groups.append((f'dog-{dog}', p(3, pr, 0), start, len(rows)))
    c = add('1B', 1, english(p(3, 19, 1)) + '\n' + p(3, 20), rows, 'japanese-5-0', [3], [7], reading=[2],
            figure=crop('ja-2012-hl-1b-1', 3, [.07, .505, .97, .70], p(3, 19, 1)))
    group_rows(c, groups)
    c['stem'] = 'All nine name, sex and colour cells are required. Breed labels and the homepage example are already given and carry no marks.'
    ability = strip_tariff(s(7, 22))
    add('1B', 2, join_cells('paper', 3, [27, 28], 300), [anyn([a.strip() for a in ability.split(',')], 2, contextNote=cell('scheme', 7, 22))], 'japanese-5-0', [3], [7], reading=[2])
    add('1B', 3, join_cells('paper', 3, [30, 31], 300), [point(s(7, 24))], 'japanese-5-0', [3], [7], 'i', reading=[2])
    add('1B', 3, p(3, 33, 1), [point(clean_tariff(cell('scheme', 7, r, 0))) for r in [26, 27]], 'japanese-5-0', [3], [7], 'ii', reading=[2])
    rows = [point(clean_tariff(cell('scheme', 7, r, g)), contextNote=p(4, pr, 0) + ' — ' + p(4, 2, g - 1)) for r, pr in [(30, 4), (31, 6)] for g in [1, 2]]
    add('1B', 4, p(4, 0, 1), rows, 'japanese-5-0', [4], [7], 'i', reading=[2],
        figure=crop('ja-2012-hl-1b-4-i', 4, [.11, .025, .97, .255], p(4, 0, 1)))
    add('1B', 4, join_cells('paper', 4, [7, 8], 300), [point(s(8, 1, g)) for g in [0, 1]], 'japanese-5-0', [4], [8], 'ii', reading=[2])
    add('1B', 5, join_cells('paper', 4, [10, 11], 300), [point(s(8, 3), 2)], 'japanese-5-0', [4], [8], reading=[2])
    add('1B', 6, join_cells('paper', 4, [13, 14], 300), [point(s(8, 5), 2)], 'japanese-5-0', [4], [8], reading=[2])


def reading_q2():
    prompts = [[1, 2], [6, 7], [10, 11], [14, 15], [17, 18], [20, 21, 22]]
    pools = [selected(9, [(r, None) for r in range(3, 7)]), selected(9, [(r, None) for r in range(10, 13)]),
             selected(9, [(r, None) for r in range(16, 20)]), selected(9, [(22, None), (23, None), (24, None)]),
             cell('scheme', 9, 26), selected(9, [(r, 0) for r in range(29, 34)])]
    for q, qr in enumerate(prompts, 1):
        question = join_cells('paper', 7, qr, 300)
        if q in [1, 2, 3, 6]:
            count = 3 if q in [1, 6] else 2
            guide = cell('scheme', 9, {1: 7, 2: 13, 3: 20, 6: 34}[q])
            if q in [1, 2]: guide += ' ' + cell('scheme', 9, 8 if q == 1 else 14)
            rows = response_pool(pools[q - 1], count, 1, guide)
        elif q == 4:
            rows = [criterion(pools[3], 2, [0, 1, 2], 'Assess one response: exact full answers earn 2; the printed Sea / Mountain / Park partial earns 1. Do not combine overlapping forms of the same response.')]
        else:
            rows = [point(value) for value in split_marks(pools[4])]
            assert len(rows) == 2
        add('2A', q, question, rows, 'japanese-5-2', [7], [9], reading=[6])
    b1 = split_marks(selected(9, [(37, 0), (38, 0)]))
    assert len(b1) == 2
    add('2B', 1, p(7, 27), [point(text) for text in b1], 'japanese-5-2', [7], [9], reading=[6])
    add('2B', 2, p(7, 29), [point(selected(9, [(40, 0), (41, 0)]), 2)], 'japanese-5-2', [7], [9], reading=[6])
    variants = [{'id': f'form-{i + 1}', 'label': f'Published wording {i + 1}',
                 'rows': [dict(point(s(10, r).split('(1 mark)', 1)[0].rstrip('、')), id=f'r-{j + 1}') for j, r in enumerate(pair)]}
                for i, pair in enumerate([[0, 1], [2, 3]])]
    b3 = add('2B', 3, p(7, 31), variants[0]['rows'], 'japanese-5-2', [7], [9, 10], reading=[6])
    b3['answerVariants'] = variants
    translated = split_marks(selected(10, [(7, 0), (8, 0)]))
    assert len(translated) == 4
    add('2C', None, p(8, 0, 2) + '\n' + p(8, 1) + ' ' + p(8, 2), [point(v) for v in translated], 'japanese-5-3', [8], [10], reading=[6])
    for q, sr, qr, region in [(1, range(11, 16), range(6, 11), [.07, .235, .97, .378]), (2, range(17, 22), range(11, 16), [.07, .375, .97, .56])]:
        instruction = join_cells('paper', 8, [qr.start, qr.start + 1], 300)
        add('2D', q, instruction + '\n' + '\n'.join(p(8, r) for r in list(qr)[2:]),
            [point(s(10, r, 1), contextNote=cell('scheme', 10, r, 0)) for r in sr], 'japanese-5-4', [8], [10], reading=[6],
            figure=crop(f'ja-2012-hl-2d-{q}', 8, region, instruction))
    labels = ['a', 'b', 'c(i)', 'c(ii)', 'd', 'e', 'f(i)', 'f(ii)', 'g', 'h']
    entries = [(24, 0), (25, 0), (26, 0), (26, 2), (27, 0), (28, 0), (29, 0), (29, 2), (30, 0), (31, 0)]
    rows = []
    for label, (r, g) in zip(labels, entries):
        answer = clean_tariff(cell('scheme', 10, r, g))
        answer = re.sub(r'^[a-h]\.\s*', '', answer)
        answer = re.sub(r'^\([ivx]+\)\s*', '', answer)
        rows.append(point(answer, contextNote=label))
    instruction = join_cells('paper', 8, [17, 18, 19], 300)
    c = add('2E', 1, instruction + '\n' + '\n'.join(p(8, r) for r in range(20, 28)), rows, 'japanese-5-5', [8], [10], reading=[6],
            figure=crop('ja-2012-hl-2e-1', 8, [.065, .565, .97, .92], instruction))
    group_rows(c, [(f'blank-{i + 1}', label, i, i + 1) for i, label in enumerate(labels)])
    instruction = p(9, 0, 1)
    rows = [point(re.sub(r'^[a-j]\.\s*', '', s(10, r)), contextNote=chr(97 + i)) for i, r in enumerate(range(33, 43))]
    c = add('2E', 2, instruction + '\n' + '\n'.join(p(9, r) for r in range(2, 13)), rows, 'japanese-5-5', [9], [10], reading=[6],
            figure=crop('ja-2012-hl-2e-2', 9, [.065, .025, .97, .51], instruction))
    group_rows(c, [(f'form-{i + 1}', chr(97 + i), i, i + 1) for i in range(10)])


def reading_q3():
    parts = re.split(r'\s*1 mark\s*', cell('scheme', 11, 3))
    assert len(parts) == 3 and not parts[-1]
    add('3A', 1, p(11, 1, 1), [point(part) for part in parts[:-1]], 'japanese-5-2', [11], [11], 'a', reading=[10])
    add('3A', 1, p(11, 3, 1), [criterion(s(11, 6), 2, [0, 1, 2], 'Frankfurt earns 2; Germany alone earns 1.')], 'japanese-5-2', [11], [11], 'b', reading=[10])
    add('3A', 1, p(11, 5, 1), [point(s(11, 8), 2)], 'japanese-5-2', [11], [11], 'c', reading=[10])
    nickname = selected(11, [(r, 0) for r in range(9, 13)])
    add('3A', 2, join_cells('paper', 11, [7, 8], 300), response_pool(nickname, 2, 2, cell('scheme', 11, 13)), 'japanese-5-2', [11], [11], reading=[10])
    for q, qr, sr in [(1, 12, 18), (2, 14, 20), (3, 16, 22), (4, 18, 24)]:
        if q == 4:
            pool = s(11, sr)
            # The original answer's five named countries are separated by や and final など.
            answers = pool.split('など', 1)[0].split('や')
            assert len(answers) == 5
            rows = [anyn(answers, 2, contextNote=cell('scheme', 11, 25))]
        else: rows = [point(s(11, sr), 2)]
        add('3B', q, p(11, qr), rows, 'japanese-5-2', [11], [11], reading=[10])
    instruction = p(11, 20, 1)
    add('3B', 5, instruction + '\n' + p(11, 21, 1) + '\n' + p(11, 22, 1),
        [point(s(11, r, 1), 2, contextNote=cell('scheme', 11, r, 0)) for r in [27, 28]], 'japanese-5-2', [11], [11], reading=[10])
    rows, groups = [], []
    for i, r in enumerate(range(30, 36)):
        reading = clean_tariff(cell('scheme', 11, r, 0))
        reading = re.sub(r'^\d+\.\s*', '', reading)
        gi = 1 if r in [31, 33] else 2
        meaning = s(11, r, gi)
        label = p(11, 27 + i, 0)
        start = len(rows)
        rows.extend([point(reading, contextNote=label + ' — reading'), point(meaning, contextNote=label + ' — meaning')])
        groups.append((f'kanji-{i + 1}', label, start, len(rows)))
    instruction = p(11, 24)
    c = add('3C', None, instruction + '\n' + '\n'.join(p(11, r) for r in range(25, 33)), rows, 'japanese-5-4', [11], [11], reading=[10],
            figure=crop('ja-2012-hl-3c', 11, [.06, .632, .98, .955], instruction))
    group_rows(c, groups)


def steps(maximum):
    return list(range(maximum + 1))


def writing():
    for q, pp, sp, maximum, lower, threshold, length in [(4, 12, 13, 20, 15, 10, 150), (5, 15, 15, 30, 20, 15, 200)]:
        ranges = [(16, 24), (24, 31), (31, 38)] if q == 4 else [(16, 24), (24, 33), (33, 41)]
        guidance = [join_cells('scheme', sp, range(a, b), 180) for a, b in ranges]
        normal = [(0, 5), (6, 14), (15, 20)] if q == 4 else [(0, 7), (8, 20), (21, 30)]
        low = [(0, 3), (4, 10), (11, 15)] if q == 4 else [(0, 4), (5, 12), (13, 20)]
        bands = [{'label': f'{lo}–{hi}', 'marks': list(range(lo, hi + 1)), 'guidance': [text]} for (lo, hi), text in zip(normal, guidance)]
        reduced = [{'label': f'{lo}–{hi}', 'marks': list(range(lo, hi + 1)), 'guidance': [text]} for (lo, hi), text in zip(low, guidance)]
        instruction = join_cells('paper', pp, [1, 2], 300)
        if q == 4:
            # The two English lead-ins share an extraction group with Irish text;
            # the literal English boundary is retained, with all Japanese headings.
            lead_a = p(pp, 3, 1).split('(a) ', 1)[1]
            lead_b = p(pp, 10).split('(b) ', 2)[2]
            question = instruction + '\n(a) ' + lead_a + ' ' + join_cells('paper', pp, [4, 5], 300) + '\n' + '\n'.join(p(pp, r) for r in [6, 7, 8])
            question += '\nOR\n(b) ' + lead_b + ' ' + join_cells('paper', pp, [11, 12], 300) + '\n' + '\n'.join(p(pp, r) for r in [13, 14, 15])
            allocation = selected(12, [(3, None), (9, None)])
            criteria = [{'id': 'content', 'label': 'Content', 'maxMarks': 15, 'permittedMarks': steps(15), 'guidance': [allocation]},
                        {'id': 'discretionary', 'label': 'Discretionary content', 'maxMarks': 5, 'permittedMarks': steps(5), 'guidance': [allocation]}]
            guide = 'Choose one complete diary entry, best day OR worst day. The source allocates 15 content marks in aggregate plus 5 discretionary content marks. It does not publish individual prompt tariffs or later-year introduction/cohesion marks. Lower E applies when total content is 10 or less, or the response has fewer than 150 characters.'
            selected(12, [(r, None) for r in range(2, 15)])
            region = [.055, .025, .97, .59]
        else:
            question = instruction + '\n' + join_cells('paper', pp, range(3, 10), 300) + '\n' + '\n'.join(p(pp, r) for r in range(10, 16))
            question += '\nOR\n' + join_cells('paper', pp, list(range(17, 22)) + [23, 24], 300) + '\n' + '\n'.join(p(pp, r) for r in range(25, 31))
            allocation = selected(14, [(3, None), (17, None)])
            discretionary = selected(14, [(r, None) for r in [4, 5, 6, 18, 19, 20]])
            criteria = [{'id': f'heading-{i}', 'label': f'Chosen heading {i}', 'maxMarks': 6, 'permittedMarks': steps(6), 'guidance': [allocation]} for i in range(1, 5)]
            criteria.append({'id': 'discretionary', 'label': 'Discretionary content', 'maxMarks': 6, 'permittedMarks': steps(6), 'guidance': [discretionary]})
            guide = 'Choose ONE scenario, then any FOUR distinct headings from its complete six-heading pool. Do not mix the two scenarios or count a heading twice. Each chosen heading earns up to 6 content marks; 6 discretionary marks are global across headings or extra relevant information. Lower E applies when total content is 15 or less, or the response has fewer than 200 characters.'
            selected(14, [(r, None) for r in list(range(9, 15)) + list(range(23, 29))])
            region = [.055, .025, .97, .945]
        content_ids = [c['id'] for c in criteria]
        criteria.append({'id': 'expression', 'label': 'Expression', 'maxMarks': maximum, 'permittedMarks': steps(maximum),
                         'bands': bands, 'guidance': [selected(sp, [(r, None) for r in ([38, 39] if q == 4 else [41, 42])]), selected(sp, [(r, None) for r in range(1, 9)])],
                         'limits': [{'id': 'lower-e', 'maxMarks': lower,
                                     'when': {'any': [{'criterionIds': content_ids, 'atMost': threshold}, {'length': 'characters', 'below': length}]},
                                     'bands': reduced, 'guidance': [selected(sp, [(r, None) for r in range(9, 13)])]}]})
        add(str(q), None, question, [], 'japanese-5-7', [pp], [sp - 1, sp], total=maximum * 2, reading=[pp],
            figure=crop(f'ja-2012-hl-{q}', pp, region, question),
            rubric={'system': 'language-writing', 'taskRequirements': [instruction], 'criteria': criteria, 'markingGuideNote': guide})
def listening():
    def listen(part, q, suffix, qr, rows, question=None, rubric=None, total=None):
        pp = {'A': 2, 'B': 3, 'C': 4, 'D': 5}[part]
        sp = {'A': 3, 'B': 4, 'C': 5, 'D': 6}[part]
        text = question or re.sub(r'^(?:\([ivx]+\)|\d+\.)\s*', '', join_cells('aural', pp, qr, 285)).strip()
        card = add('L' + part, q, text, rows, 'japanese-6-2' if part == 'C' else 'japanese-6-1' if part == 'D' else 'japanese-6-0',
                   [pp], [sp], suffix or '', rubric=rubric, total=total)
        card['sourceMaterial'] = source([pp], 'source-question', 'aural')
        card['stem'] = join_cells('aural', pp, range(1, 7 if part == 'C' else 5), 285)
        if part in 'BD': card['stem'] += '\n' + join_cells('aural', pp, [{'B': {1: 5, 2: 9, 3: 14}, 'D': {1: 6, 2: 16}}[part][q]], 285)
        return card

    labels = [cell('aural', 2, 7, 0), selected(3, [(3, 1), (4, 0), (5, 0), (6, 0)]), cell('aural', 2, 7, 2)]
    reasons1 = split_marks(selected(3, [(8, 2), (9, 2)]))
    assert len(reasons1) == 2
    values = [
        [[point(selected(3, [(7, 1), (8, 0)]), contextNote=cell('scheme', 3, 10))], [point(s(3, 8, 1))], [point(v) for v in reasons1]],
        [[point(s(3, 12, 0))], [point(s(3, 12, 1))], [criterion(selected(3, [(12, 2), (13, 2)]), 2, [0, 1, 2], cell('scheme', 3, 14))]],
        [[point(s(3, 16, 0))], [point(s(3, 16, 1))], [point(selected(3, [(16, 2), (17, 2)]), 2)]],
        [[point(s(3, 20, 0))], [point(s(3, 20, 1))], [criterion(selected(3, [(20, 2), (21, 2)]), 2, [0, 1, 2], cell('scheme', 3, 22))]],
        [[], [point(s(3, 24, 1))], [point(s(3, 24, 2), 2)]],
    ]
    rows, groups = [], []
    for i, cells in enumerate(values):
        for col, components in enumerate(cells):
            if not components: continue
            label = f'{i + 1}. {labels[col]}'
            start = len(rows)
            rows.extend(dict(row, contextNote=label + '. ' + row.get('contextNote', '')) for row in components)
            groups.append((f'request-{i + 1}-cell-{col + 1}', label, start, len(rows)))
    table = listen('A', None, None, [], rows, cell('aural', 2, 4, 1) + '\n' + '\n'.join(labels))
    group_rows(table, groups)
    table['stem'] += '\nThe fifth request, Leave the mobile phone switched on, is already printed. It carries no marks; its acceptance and reason are still required.'
    table['questionFigureKey'] = crop('ja-2012-hl-la', 2, [.07, .025, .99, .68], table['questionText'], 'aural')
    assert len(groups) == 14 and row_total(rows) == 19

    listen('B', 1, 'i', [6], [point(s(4, 3), 2)])
    directions = s(4, 5).split('/')
    groups = []
    for i, text in enumerate(directions):
        group = {'id': f'direction-{i + 1}', 'label': text.strip(), 'rows': []}
        if i == 1:
            group['criteria'] = [{'id': 'elevator', 'label': 'Elevator direction', 'maxMarks': 2, 'permittedMarks': [0, 1, 2], 'guidance': [text.strip(), cell('scheme', 4, 7)]}]
        else: group['rows'] = [{'id': 'answer', 'text': text.strip(), 'marks': 2}]
        groups.append(group)
    listen('B', 1, 'ii', [8], [], rubric={'system': 'language-points', 'count': 2, 'groups': groups,
        'taskRequirements': [cell('aural', 3, 8, 1)], 'markingGuideNote': cell('scheme', 4, 6) + ' Elevator alone earns 1 within the same direction concept; it cannot also earn the full Take the elevator credit.'}, total=4)
    listen('B', 2, 'i', [10], [point(s(4, 9), 2)])
    listen('B', 2, 'ii', [11], [point(s(4, 11), 2)])
    listen('B', 2, 'iii', [12], [anyn(s(4, 13).split('/'), 2, contextNote=cell('scheme', 4, 14))])
    listen('B', 3, 'i', [15], [criterion(s(4, 16), 2, [0, 1, 2], cell('scheme', 4, 17))])
    listen('B', 3, 'ii', [17], [point(s(4, 19), 2)])
    listen('B', 3, 'iii', [18], [point(s(4, 21), 2)])

    for letter, qr, sr, tariff in [('a', 11, [3, 4, 5], 6), ('b', 13, [8, 9], 10)]:
        question = join_cells('aural', 4, [9, 10, qr], 285)
        pool = selected(5, [(r, None) for r in sr])
        c = listen('C', 1, f'{letter}-i', [], response_pool(pool, 2, 2, cell('scheme', 5, tariff)), question)
        c['questionRef'] = f'2012 HL Section LC Q1(i)({letter})'
        for row in c['rows']:
            row['contextNote'] += ' The printed summary of film genres is retained in the pool; do not count it again alongside the same genre facts.'
    listen('C', 1, 'ii', [14, 15], [point(s(5, 12))])
    listen('C', 2, 'i', [18], [criterion(s(5, 14), 2, [0, 1, 2], cell('scheme', 5, 15))])
    jobs = selected(5, [(17, 0), (18, 0)]).replace('(4 marks)', '')
    listen('C', 2, 'ii', [20], [anyn([t.strip() for t in jobs.split('/') if t.strip()], 2, 2, contextNote=cell('scheme', 5, 19))])
    phone = listen('C', 2, 'iii', [23, 24], [point(s(5, 21), 3, contextNote='The scheme allocates 3 marks to the complete phone number. The original question gives 03 and eight missing digits; no per-digit tariff is published.')])
    phone['questionFigureKey'] = crop('ja-2012-hl-lc-2-iii', 4, [.49, .61, .97, .765], phone['questionText'], 'aural')
    weather = split_marks(selected(5, [(23, 0), (24, 0)]))
    assert len(weather) == 3
    listen('C', 3, 'i', [27, 28], [point(v) for v in weather])
    listen('C', 3, 'ii', [30, 32], [point(s(5, 26), 2)])

    listen('D', 1, 'i', [7], [point(s(6, 2))])
    listen('D', 1, 'ii', [8], [point(s(6, 4), 2)])
    pool = selected(6, [(6, 0), (7, 0), (8, 0), (9, 0)])
    # Three printed concepts, with the source's 1-mark partials scoped to
    # their corresponding full responses; only the best two concepts count.
    main = s(6, 6)
    mountain, people = main.split('/', 1)
    people = people.rstrip('/').strip()
    spring = strip_tariff(s(6, 7))
    groups = [
        {'id': 'mountains', 'label': 'Mountains', 'rows': [{'id': 'answer', 'text': mountain.strip(), 'marks': 2}]},
        {'id': 'people', 'label': 'People at the inn', 'rows': [], 'criteria': [{'id': 'people-answer', 'label': 'People response', 'maxMarks': 2, 'permittedMarks': [0, 1, 2], 'guidance': [people, cell('scheme', 6, 8, 0)]}]},
        {'id': 'spring', 'label': 'Hot spring', 'rows': [], 'criteria': [{'id': 'spring-answer', 'label': 'Hot spring response', 'maxMarks': 2, 'permittedMarks': [0, 1, 2], 'guidance': [spring, cell('scheme', 6, 9)]}]},
    ]
    listen('D', 1, 'iii', [9, 10], [], rubric={'system': 'language-points', 'count': 2, 'groups': groups,
        'taskRequirements': [join_cells('aural', 5, [9, 10], 285)], 'markingGuideNote': pool + ' Count each full/partial concept once; only two distinct details can score.'}, total=4)
    internet = point(s(6, 11).rstrip('/'), 2)
    skype = cell('scheme', 6, 12, 0)
    pieces = re.split(r'\s*1 mark\.?\s*', skype)
    assert len(pieces) == 3 and not pieces[-1]
    variants = [{'id': 'internet', 'label': 'Internet at the inn', 'rows': [dict(internet, id='r-1')]},
                {'id': 'skype', 'label': 'Skype with her family', 'rows': [dict(point(v.strip()), id=f'r-{i + 1}') for i, v in enumerate(pieces[:-1])]}]
    c = listen('D', 1, 'iv', [12], variants[0]['rows'])
    c['answerVariants'] = variants
    c['rows'][0]['contextNote'] = cell('scheme', 6, 13) + ' Choose one answer route; do not combine the full internet answer with the two Skype components.'
    work = split_marks(cell('scheme', 6, 15, 0))
    assert len(work) == 2
    listen('D', 1, 'v', [14, 15], [point(work[0]), point(work[1], contextNote=cell('scheme', 6, 16) + '. Tokyo is the same one-mark location component, not an extra point.')])
    listen('D', 2, 'i', [17], [point(s(6, 18))])
    listen('D', 2, 'ii', [18], [point(s(6, 20), 2, contextNote=cell('scheme', 6, 21))])
    listen('D', 2, 'iii', [21], response_pool(s(6, 23), 2, 1, cell('scheme', 6, 24) + ' ' + cell('scheme', 6, 25)))
    listen('D', 2, 'iv', [22], [point(s(6, 27), 2)])
    study = cell('scheme', 6, 29, 0).split('(1 mark)')
    assert len(study) == 2
    listen('D', 2, 'v', [23, 24], [point(v.strip().rstrip('.')) for v in study])


def build():
    reading_q1(); reading_q2(); reading_q3(); writing(); listening()
    census = json.loads((Path(__file__).parent / 'reviews/japanese-2012-hl-census.json').read_text())
    expected = {'ja-2012-hl-' + '-'.join(str(part).lower() for part in task['key'] if part is not None): task for task in census['tasks']}
    assert set(expected) == {card['id'] for card in CARDS}, (set(expected) - {card['id'] for card in CARDS}, {card['id'] for card in CARDS} - set(expected))
    for card in CARDS:
        task = expected[card['id']]
        assert card['totalMarks'] == task['marks'], (card['id'], card['totalMarks'], task['marks'])
        assert card['sourceEvidence']['paperPages'] == task['paperPages']
        assert card['sourceEvidence']['schemePages'] == task['schemePages']
        assert card['questionRef'] == task.get('paperRef', card['questionRef'])
        rubric = card.get('rubric', {})
        for item in rubric.get('criteria', []) + [item for group in rubric.get('groups', []) for item in group.get('criteria', [])]:
            guidance = item.get('guidance', []) + [text for band in item.get('bands', []) for text in band['guidance']]
            guidance += [text for limit in item.get('limits', []) for text in limit['guidance']]
            guidance += [text for limit in item.get('limits', []) for band in limit.get('bands', []) for text in band['guidance']]
            assert all(text.strip() for text in guidance), (card['id'], item['id'], 'Empty source guidance')
    assert len(CARDS) == 62
    assert sum(card['totalMarks'] for card in CARDS) == 300
    assert sum('answerLanguageRule' in card for card in CARDS) == 14
    assert sum('extraneousMaterialRule' in card for card in CARDS) == 5
    assert '\ufffd' not in json.dumps([CARDS, EVIDENCE], ensure_ascii=False)
    return {'subjectId': 'japanese', 'sitting': '2012-hl', 'reviewedAt': '2026-11-10',
            'sources': [{'document': name, 'path': str(path.relative_to(ROOT)), 'sha256': PINNED_SOURCES[path],
                         'pagesReviewed': list(range(1, len(DOCS[name]) + 1))} for name, path in [('paper', PAPER), ('aural', AURAL), ('scheme', SCHEME)]],
            'cards': CARDS, 'selectors': EVIDENCE, 'status': 'source-captured', 'choiceAnalysis': census['choiceBoundaries'], 'consolidations': []}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    result = build()
    if args.write:
        scheme_text = ''.join(f'\n## Page {i + 1}\n\n' + page.get_text(sort=True) for i, page in enumerate(DOCS['scheme']))
        scheme_text += '\n## Original text with furigana folded at its printed character\n'
        scheme_text += ''.join(f'\n### Physical page {i + 1}\n\n' + '\n'.join(' '.join(group[2] for group in row) for row in rows) + '\n' for i, rows in enumerate(ROWS['scheme']))
        for page, x_ranges in [(3, [(90, 240), (241, 301), (302, 590)]), (7, [(185, 228), (229, 335), (336, 436), (437, 590)])]:
            scheme_text += f'\n## Original table columns — physical page {page}\n'
            scheme_text += '\n'.join(DOCS['scheme'][page - 1].get_text(clip=fitz.Rect(x0, 0, x1, DOCS['scheme'][page - 1].rect.height), sort=True) for x0, x1 in x_ranges)
        SCHEME.with_suffix('.md').write_text(scheme_text.rstrip() + '\n')
        (ROOT / 'scripts/markbank/authoring/reviews/japanese-2012-hl.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
        manifest = ROOT / 'components/MarkBank/figures-japanese.json'
        previous = json.loads(manifest.read_text()); previous.update(FIGURES)
        manifest.write_text(json.dumps(previous, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'cards': len(CARDS), 'marks': sum(card['totalMarks'] for card in CARDS), 'figures': len(FIGURES)}, indent=2))
