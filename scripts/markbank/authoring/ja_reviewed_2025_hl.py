#!/usr/bin/env python3
"""2025 Higher Japanese, independently reviewed against all original pages.

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
from ja_paper import JaPaper, plain
from ja_text import page_rows
from ja_topics import FURIGANA_NOTE, concept_for

ROOT = Path(__file__).resolve().parents[3]
PAPER = ROOT / 'examiner-reports/japanese/papers/2025-hl-000-paper.pdf'
AURAL = ROOT / 'examiner-reports/japanese/papers/2025-hl-A00-paper.pdf'
SCHEME = ROOT / 'examiner-reports/japanese/schemes/2025-hl.pdf'
PINNED_SOURCES = {
    PAPER: 'ee65b1a62840d44091078fcfa7838c93ebe561dc70bc5729d2fd64cd829f1ac2',
    AURAL: '978fe00bd2976087f3e0ddede26c9c346b94af6a6fe430b466e6075d18dc16c8',
    SCHEME: 'da1b0a337677d064eae660437ef2f6cf6ac9da574b03426de0d63f75cddf5454',
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
    return text.split(' / ', 1)[-1].strip()


def point(text, marks=1, **extra):
    return {'kind': 'point', 'verbatim': text, 'marks': marks, **extra}


def anyn(options, count, marks=1, steps=None):
    group = {'claimMax': count, 'perOption': marks, 'options': options}
    if steps:
        group['perOptionSteps'] = steps
    return {'kind': 'anyN', 'verbatim': 'Accepted answers', 'marks': None, 'group': group}


def worth(row):
    if row['kind'] != 'anyN':
        return row['marks']
    group = row['group']
    return sum(group['perOptionSteps']) if 'perOptionSteps' in group else group['claimMax'] * group['perOption']


def source(pages, kind='source-text', component='paper'):
    return {'kind': kind, 'label': '2025 Japanese Higher Level', 'title': 'Original examination material',
            'pages': pages, 'attribution': '© State Examinations Commission.',
            **({'presentationNote': FURIGANA_NOTE} if component == 'paper' else {}),
            '_component': component}


def add(section, q, question, rows, topic, paper_pages, scheme_pages, suffix='', rubric=None, total=None, reading=None, figure=None):
    cid = f'ja-2025-hl-{section.lower()}' + (f'-{q}' if q is not None else '') + (f'-{suffix}' if suffix else '')
    ref = f'2025 HL Section {section}' + (f' Q{q}' if q is not None else '')
    if suffix:
        ref += ''.join(f'({part})' for part in suffix.split('-'))
    listening = section.startswith('L')
    card = {'id': cid, 'source': 'sec', 'subjectId': 'japanese', 'specVersion': 'lc-japanese-syllabus',
            'kind': 'rubric' if rubric else 'question', 'level': 'higher', 'year': 2025,
            'section': section[1:] if listening else section[0] if section[0] in '1234' else 'Q5',
            'topicId': topic, 'conceptId': concept_for(question, cid), 'questionRef': ref,
            'questionText': question, 'totalMarks': total if total is not None else sum(map(worth, rows)),
            'qa': {'gates': ['verbatim', 'tariff', 'figure'], 'humanReviewedBy': 'agent-verified', 'humanReviewedAt': '2026-11-09'},
            'sourceEvidence': {'component': 'aural' if listening else 'paper', 'paperPages': paper_pages, 'schemePages': scheme_pages},
            'schemeCitation': 'Marking points quoted from the SEC marking scheme, Japanese 2025 Higher Level — © State Examinations Commission.'}
    if rubric:
        card['rubric'] = rubric
    else:
        card['tariffModel'] = {'kind': 'fixed'}
        card['rows'] = [dict(row, id=f'r-{i + 1}') for i, row in enumerate(rows)]
    original_ids = set(re.findall(r'    id: "([^"]+)"', (ROOT / 'components/MarkBank/cards/japanese/higher.ts').read_text()))
    if cid in original_ids:
        card['qa']['gates'].append('reviewed-card-correction')
    # 2025 has scoped rules, not a general all-paper language convention.
    convention = None
    if listening:
        convention = (3, cell('scheme', 3, 1))
    elif section in ['1A', '1B']:
        convention = (7, cell('scheme', 7, 1, 1))
    elif section == '2A' and q == 2:
        convention = (9, cell('scheme', 9, 0, 1))
    elif section == '3A':
        convention = (11, cell('scheme', 11, 1, 1))
    elif (section == '2A' and q == 1) or section == '3B':
        page, first, last = (8, 14, 15) if section == '2A' else (11, 17, 18)
        text = joined_selector('scheme', page, [(first, 1), (last, 0)])
        convention = (page, text)
        card['extraneousMaterialRule'] = {'multiplier': 0.5, 'sourceText': text, 'schemePages': [page]}
    if convention:
        page, text = convention
        card['sourceEvidence']['generalSchemePages'] = [page]
        card['answerLanguageRule'] = {'otherLanguageMultiplier': 0.5, 'penalizedLanguage': 'English' if 'extraneousMaterialRule' in card else 'Japanese', 'sourceText': text, 'schemePages': [page]}
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
    return strip_tariff(' '.join(s(page, row) for row in rows)).split(separator)


def comprehension(section, q, suffix, question_rows, rows, scheme_pages, total=None):
    page = 3 if section == '1A' else 4 if section == '1B' else 7 if section == '2A' else 11
    topic = {'1': 'japanese-5-0', '2': 'japanese-5-2', '3': 'japanese-5-1'}[section[0]]
    text = prompt(page, question_rows)
    if section == '3B':
        text = p(page, question_rows[0], 1)
    if section == '2A' and q == 1:
        text = p(page, question_rows[0], 1)
    card = add(section, q, text, rows, topic, [page], scheme_pages, suffix or '', total=total,
               reading={'1A': [2], '1B': [4], '2A': [6], '3A': [10], '3B': [10]}[section])
    if section == '2A':
        card['stem'] = english(p(7, 1 if q == 1 else 10, 1))
    else:
        row = {'1A': 0, '1B': 14, '3A': 0, '3B': 19}[section]
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



def reading():
    instruction = prompt(3, [1, 2])
    items = [english(p(3, row)).rstrip('_ ').strip() for row in range(4, 9)]
    add('1A', 1, instruction + '\n' + 'e.g. ' + english(p(3, 3)) + '\n' + '\n'.join(f'({letter}) {text}' for letter, text in zip('abcde', items)),
        [point(s(7, row, 0) + ' — ' + s(7, row, 1)) for row in range(4, 9)], 'japanese-5-0', [3], [7], reading=[2])
    first = cell('scheme', 7, 10, 0)
    comprehension('1A', 2, 'a', [9], [point(text.strip()) for text in first.replace(' (1 mark)', '').split(', ')], [7])
    comprehension('1A', 2, 'b', [11, 12], [anyn(options(7, [12]), 2)], [7])
    comprehension('1A', 3, 'a', [14], [point(s(7, 15), 2)], [7])
    comprehension('1A', 3, 'b', [16], [point(text) for text in cell('scheme', 7, 17, 0).replace(' (1 mark)', '').split(', ')], [7])
    comprehension('1A', 4, None, [18, 19], [anyn(options(7, [19]), 2)], [7])
    comprehension('1A', 5, None, [21], [point(s(7, 21), 2)], [7])
    comprehension('1A', 6, None, [23, 24], [anyn(options(7, [23]), 2)], [7])
    question = prompt(3, [26]) + '\n' + p(3, 27) + '\n' + ' '.join(p(3, row) for row in range(28, 35))
    donpen = cell('scheme', 7, 26, 1).removeprefix('(a) ') + ' ' + cell('scheme', 7, 27, 0).removeprefix('description:  ') + ' ' + cell('scheme', 7, 28, 0)
    donko = cell('scheme', 7, 26, 2).removeprefix('(c) ') + ' ' + cell('scheme', 7, 27, 1)
    personality = cell('scheme', 7, 30, 0).split('(b) ')[1]
    figure = crop('ja-2025-hl-1a-7', 3, [.06, .738, .95, .934], question)
    rows = [anyn(strip_tariff(donpen).split(', '), 2), point(personality), anyn(donko.split(', '), 2)]
    for row, label in zip(rows, ['(a) Donpen — Physical description', '(b) Donpen — Personality', '(c) Donko — Physical description']):
        row['contextNote'] = label
    add('1A', 7, question, rows, 'japanese-5-0', [3], [7], reading=[2], figure=figure)
    comprehension('1B', 1, 'a', [15, 16], [point(s(8, 2), 2)], [8])
    first, second = cell('scheme', 8, 4, 0).split(' (1 mark) and ')
    comprehension('1B', 1, 'b', [18, 19], [point(first), point(second)], [8])
    comprehension('1B', 2, 'a', [21, 22], [point(s(8, 7), 2)], [8])
    comprehension('1B', 2, 'b', [24], [anyn(options(8, [9]), 2)], [8])
    comprehension('1B', 3, None, [26, 27], [point(text) for text in cell('scheme', 8, 11, 0).replace(' (1 mark)', '').split(', ')], [8])

    comprehension('2A', 1, 'a', [2], [point(s(8, 17), 2)], [8])
    # A separately priced partial answer, independent of either source reduction.
    full, partial = s(8, 19), cell('scheme', 8, 19, 1)
    comprehension('2A', 1, 'b', [4], [{'kind': 'criterion', 'verbatim': full + ' ' + partial, 'marks': 2, 'permittedMarks': [0, 1, 2]}], [8])
    pieces = cell('scheme', 8, 21, 0).split('(1 mark)')
    comprehension('2A', 1, 'c', [6], [point(text.strip().lstrip('、')) for text in pieces if text.strip()], [8])
    pieces = cell('scheme', 8, 24, 0).split(' (1 mark)')
    comprehension('2A', 1, 'd', [8], [point(text.strip()) for text in pieces if text.strip()], [8])
    history = s(9, 2).removesuffix('.')
    history_options = [history.split(', held')[0], 'held' + history.split(', held')[1].split(', 3rd')[0], '3rd' + history.split(', 3rd')[1]]
    comprehension('2A', 2, 'a', [11], [anyn(history_options, 2, 2, [2, 1])], [9])
    comprehension('2A', 2, 'b', [14, 15], [point(s(9, 5), 2)], [9])
    pavilion = ' '.join(s(9, row) for row in [7, 8])
    # The commas within "Ireland, Japan and creativity" do not split that fact.
    pavilion_options = [pavilion.split(', design')[0], 'design' + pavilion.split(', design')[1].split(', three circles')[0],
                        'three circles' + pavilion.split(', three circles')[1].split(', the wood')[0],
                        'the wood' + pavilion.split(', the wood')[1].split(', sustainable')[0], pavilion.rsplit(', ', 1)[1]]
    comprehension('2A', 2, 'c-i', [17, 18], [anyn(pavilion_options, 2, 2, [2, 1])], [9])
    comprehension('2A', 2, 'c-ii', [21, 22], [anyn(options(9, [11]), 2, 2, [2, 1])], [9])
    comprehension('2A', 2, 'd', [25, 26], [anyn(options(9, [14, 15]), 3)], [9])
    translation = cell('scheme', 9, 19, 0) + ' ' + cell('scheme', 9, 20, 0)
    a, remainder = translation.split(' (1 mark). ', 1)
    b, remainder = remainder.split(' (2 marks) ', 1)
    c = remainder.split(' (1 mark)')[0]
    add('2A', 3, prompt(7, [29]) + '\n' + ' '.join(p(7, row) for row in [30, 31]),
        [point(a), point(b, 2), point(c)], 'japanese-5-3', [7], [9], reading=[6, 7])

    for section, q, page, instruction_rows, item_rows, sp, sr, region in [
        ('2B', 1, 8, [1, 2], range(3, 10), 9, range(23, 29), [.06, .055, .95, .485]),
        ('2B', 2, 8, [10, 11], range(12, 19), 10, range(1, 7), [.06, .49, .95, .92]),
        ('2C', 1, 9, [1, 2], range(3, 10), 10, range(9, 15), [.06, .055, .95, .465]),
        ('2C', 2, 9, [10, 11], range(12, 19), 10, range(16, 22), [.06, .466, .95, .92]),
    ]:
        question = prompt(page, instruction_rows) + '\n' + '\n'.join(p(page, row) for row in item_rows)
        key = crop(f'ja-2025-hl-{section.lower()}-{q}', page, region, question)
        add(section, q, question, [anyn([s(sp, row, 0) + ' — ' + s(sp, row, 1) for row in sr], 5)],
            'japanese-5-4' if section == '2B' else 'japanese-5-5', [page], [sp], figure=key)

    for q, qr, sr, count, descending in [(1, [1, 2], [3], 2, False), (2, [4, 5], [5, 6], 3, False),
                                        (3, [8, 9], [8, 9], 2, True), (4, [12], [11], 3, False), (5, [15], [14, 15], 3, False)]:
        answers = options(11, sr)
        if q == 3:
            answers[-1] = answers[-1].removesuffix('.')
        comprehension('3A', q, None, qr, [anyn(answers, count, 2 if descending else 1, [2, 1] if descending else None)], [11])
    for q, qr, sr, marks in [(1, 20, 20, 1), (2, 22, 22, 2), (3, 24, 24, 2), (4, 26, 26, 1)]:
        text = cell('scheme', 11, sr, 0)
        answers = [part.strip(' ,') for part in text.split(' (1 mark)') if part.strip(' ,')]
        comprehension('3B', q, None, [qr], [point(text) for text in answers], [11], total=marks)

    instruction = prompt(12, [1, 2, 3])
    question = instruction + '\n' + '\n'.join(p(12, row) for row in range(5, 12))
    groups = [{'id': f'item-{row}', 'label': s(12, row, 1), 'rows': [{'id': 'reading', 'text': s(12, row, 2), 'marks': 1},
               {'id': 'meaning', 'text': s(12, row, 4), 'marks': 1}]} for row in range(1, 7)]
    key = crop('ja-2025-hl-3c', 12, [.06, .025, .97, .46], question)
    add('3C', None, question, [], 'japanese-5-4', [12], [12], figure=key, total=10,
        rubric={'system': 'language-points', 'count': 5, 'groups': groups, 'taskRequirements': [instruction],
                'markingGuideNote': 'The scheme awards one mark for the correct reading and one for the meaning for each of five selected kanji.'})
    instruction = prompt(12, [13, 14, 15])
    question = instruction + '\n' + '\n'.join(p(12, row) for row in range(16, 23))
    groups = []
    for n, columns in enumerate([[1], [1, 3], [1, 3], [1, 3, 4], [1, 3], [1], [1]], 1):
        for blank, column in enumerate(columns, 1):
            groups.append({'id': f'{n}-{blank}', 'label': f'{n}. Blank {blank}', 'rows': [{'id': 'particle', 'text': s(12, n + 7, column), 'marks': 1}]})
    key = crop('ja-2025-hl-3d', 12, [.06, .46, .97, .92], question)
    add('3D', None, question, [], 'japanese-5-5', [12], [12], figure=key, total=10,
        rubric={'system': 'language-points', 'count': 10, 'groups': groups, 'taskRequirements': [instruction],
                'markingGuideNote': 'Select ten of the twelve blanks. Each correct particle earns one mark; slash-separated forms are alternatives for the same blank.'})


def steps(maximum):
    return list(range(maximum + 1))


def writing():
    for q, pp, sp, maximum, threshold, length, lower, normal, reduced, shift in [
        (4, 14, 14, 20, 10, 150, 15, [(0, 5), (6, 14), (15, 20)], [(0, 3), (4, 10), (11, 15)], 0),
        (5, 16, 16, 30, 15, 200, 20, [(0, 7), (8, 20), (21, 30)], [(0, 4), (5, 12), (13, 20)], 1),
    ]:
        bands, lower_bands = [], []
        for i, rows in enumerate([range(16 + shift, 23 + shift), range(23 + shift, 30 + shift), range(30 + shift, 36 + shift)]):
            guidance = [join_cells('scheme', sp, rows, 170)]
            for target, ranges in [(bands, normal), (lower_bands, reduced)]:
                lo, hi = ranges[i]
                target.append({'label': f'{lo}–{hi}', 'marks': list(range(lo, hi + 1)), 'guidance': guidance})
        rule = join_cells('scheme', sp, range(10 + shift, 14 + shift))
        if q == 4:
            instruction = prompt(14, [1, 2])
            question = instruction + '\n' + '\n'.join([
                '(a) ' + prompt(14, [3, 4, 5]), p(14, 6), p(14, 7), english(p(14, 8)),
                '(b) ' + prompt(14, [9, 10, 11, 12]), p(14, 13), p(14, 14), english(p(14, 15)),
                '(c) ' + prompt(14, [16, 17, 18]), p(14, 19), p(14, 20)])
            criteria = [
                {'id': 'opening', 'label': 'Opening', 'maxMarks': 1, 'permittedMarks': [0, 1], 'guidance': [s(13, 18)]},
                *[{'id': f'point-{i}', 'label': f'({i})', 'maxMarks': 9, 'permittedMarks': steps(9), 'guidance': [s(13, 17)]} for i in ['i', 'ii']],
                {'id': 'closing', 'label': 'Closing', 'maxMarks': 1, 'permittedMarks': [0, 1], 'guidance': [s(13, 19, 1)]},
            ]
        else:
            instruction = prompt(16, range(1, 5))
            question = instruction + '\n' + '\n'.join(p(16, row, 0) + ' ' + english(p(16, row, 1)) + (' ' + p(16, 13) if row == 12 else '') for row in range(5, 13))
            headings = [cell('scheme', 15, row) for row in range(3, 11)]
            criteria = [{'id': f'heading-{i}', 'label': f'Heading {i} you chose', 'maxMarks': 7, 'permittedMarks': steps(7), 'guidance': [s(15, 12)] + headings} for i in range(1, 5)]
            criteria.extend([
                {'id': 'opening', 'label': 'Opening', 'maxMarks': 1, 'permittedMarks': [0, 1], 'guidance': [s(15, 13)]},
                {'id': 'closing', 'label': 'Closing', 'maxMarks': 1, 'permittedMarks': [0, 1], 'guidance': [s(15, 14, 1)]},
            ])
        content_ids = [criterion['id'] for criterion in criteria]
        criteria.append({'id': 'expression', 'label': s(sp - 1, 20 if q == 4 else 15), 'maxMarks': maximum,
                         'permittedMarks': steps(maximum), 'guidance': [join_cells('scheme', sp, [36 + shift, 37 + shift])], 'bands': bands,
                         'limits': [{'id': 'lower-e', 'maxMarks': lower, 'when': {'any': [{'criterionIds': content_ids, 'atMost': threshold}, {'length': 'characters', 'below': length}]}, 'bands': lower_bands, 'guidance': [rule]}]})
        key = crop(f'ja-2025-hl-{q}', pp, [.045, .015, .96, .92], question)
        add(str(q), None, question, [], 'japanese-5-7', [pp], [sp - 1, sp], total=maximum * 2, figure=key,
            rubric={'system': 'language-writing', 'taskRequirements': [instruction], 'criteria': criteria,
                    'markingGuideNote': 'Assess four different selected headings once each, using the printed content and expression grid.' if q == 5 else 'Assess the one option you answered. The same printed content and expression grid applies to all three options.'})


def listening():
    def aq(page, rows):
        return re.sub(r'^(?:\d+\.\s*)?(?:\([a-f]\)\s*)?(?:\(i{1,2}\)\s*)?', '', join_cells('aural', page, rows, 300)).strip()

    def listen(part, q, suffix, question_rows, rows, rubric=None, total=None, question=None):
        pp, sp = {'A': (2, 3), 'B': (3, 4), 'C': (4, 5), 'D': (5, 6)}[part]
        card = add('L' + part, q, question or aq(pp, question_rows), rows,
                   {'A': 'japanese-6-1', 'B': 'japanese-6-2', 'C': 'japanese-6-1', 'D': 'japanese-6-0'}[part],
                   [pp], [sp], suffix or '', rubric=rubric, total=total)
        card['sourceMaterial'] = source([pp], 'source-question', 'aural')
        card['stem'] = join_cells('aural', pp, [1, 2], 300)
        return card

    # Column extraction remains source-pinned when the PDF row merges adjacent
    # cells. These boundaries are the inspected printed table columns.
    def column(rows, x0, x1):
        result = []
        for row in rows:
            for gi, group in enumerate(ROWS['scheme'][2][row]):
                if x0 <= group[0] < x1:
                    result.append(cell('scheme', 3, row, gi))
        return ' '.join(result)

    headers = [' '.join(cell('aural', 2, r, g) for r, g in parts) for parts in [
        [(6, 0), (7, 0)], [(5, 0), (6, 1)], [(6, 2), (7, 1)], [(6, 3), (7, 2)]]]
    headers[0] = english(headers[0]).lstrip('/ ')
    headers[1] = english(headers[1])
    emi_positive = strip_tariff(column(range(7, 12), 300, 420)).split(', ')
    emi_negative = column(range(7, 11), 420, 550)
    emi_parts = [part.strip() for part in re.split(r'\(1\s+mark\)', emi_negative) if part.strip()]
    emi = [point(s(3, 7, 1)), point(s(3, 7, 2).replace('(1mark)', '').strip()), point(s(3, 8, 0)), anyn(emi_positive, 2), *[point(part) for part in emi_parts]]
    # Row 15 merges time and positive columns; split at the original first
    # word in the positive column, keeping both sides as pinned substrings.
    merged = cell('scheme', 3, 15, 1)
    time_continuation, positive_continuation = merged.split(' cleaning ', 1)
    andy_time = s(3, 14, 2) + ' ' + time_continuation + ' ' + s(3, 16, 1)
    positive = s(3, 14, 3) + ' cleaning ' + positive_continuation + ' ' + s(3, 16, 2) + ' ' + s(3, 17, 0)
    negative = column(range(14, 20), 420, 550)
    andy_parts = [part.strip(' ,') for part in negative.split('(1 mark)') if part.strip(' ,')]
    andy = [point(column(range(14, 17), 100, 180)), point(andy_time, 2), anyn(positive.split(', '), 2), *[point(part) for part in andy_parts]]
    naomi_time = column(range(22, 25), 190, 300)
    naomi_time_parts = [part.strip() for part in re.split(r'\(1\s+marks?\)', naomi_time) if part.strip()]
    naomi = [point(s(3, 22, 1)), *[point(part) for part in naomi_time_parts], point(column(range(22, 24), 300, 420), 2),
             anyn(strip_tariff(column(range(22, 27), 420, 550)).split(', '), 2)]
    for n, rows in enumerate([emi, andy, naomi], 1):
        question = cell('aural', 2, 3, 1) + '\n' + cell('aural', 2, 7 + n * 2) + '\n' + '\n'.join(headers)
        card = listen('A', n, None, [], rows, question=question)
        assert card['totalMarks'] == 7, card

    listen('B', 1, 'a', [4], [point(s(4, 3))])
    listen('B', 1, 'b', [7, 8], [anyn(options(4, [5]), 2)])
    listen('B', 1, 'c', [10], [point(text) for text in options(4, [7])])
    hotel_views = s(4, 10).split('/Tokyo Tower /')
    # The two night-view descriptions are synonyms for one fact. Preserve
    # both wordings without allowing the same fact to earn credit twice.
    listen('B', 1, 'd', [14, 15], [anyn([hotel_views[0].strip(), s(4, 10).split('/')[2].strip(), hotel_views[1].strip()], 2)])
    directions = options(4, [13, 14])
    exit_text = directions.pop(0).replace(' (1 mark)', '')
    listen('B', 1, 'e', [18, 19], [point(exit_text), anyn(directions, 2, 2, [2, 1])])
    phone = listen('B', 1, 'f', [23], [point(s(4, 16), 2)])
    phone['questionFigureKey'] = crop('ja-2025-hl-lb-1-f', 3, [.53, .642, .96, .700], phone['questionText'], 'aural')
    listen('B', 2, 'a', [26], [anyn(options(4, [19]), 2)])
    listen('B', 2, 'b', [29], [point(text.strip()) for text in cell('scheme', 4, 22, 0).split(' (1 mark)') if text.strip()])
    listen('B', 2, 'c', [31], [anyn(options(4, [24]), 2)])
    listen('C', 1, None, [3, 4], [anyn(options(5, [2, 3]), 2, 2, [2, 1])])
    listen('C', 2, None, [7, 8], [point(s(5, 5), 2)])
    listen('C', 3, None, [10], [point(' '.join(s(5, row) for row in [7, 8]), 2)])
    listen('C', 4, None, [13], [anyn(options(5, [10]), 2, 2, [2, 1])])
    ingredients = []
    for row in [14, 15, 16]:
        ingredients.append(point(re.sub(r'^\([a-c]\) ', '', s(5, row, 1)), contextNote=s(5, row, 0)))
    table = listen('C', 5, None, [19], ingredients)
    table['questionFigureKey'] = crop('ja-2025-hl-lc-5', 4, [.53, .505, .97, .655], table['questionText'], 'aural')
    listen('C', 6, None, [29], [anyn(options(5, [18]), 2, 2, [2, 1])])
    listen('C', 7, None, [34, 35], [anyn(options(5, [21, 22]), 2, 2, [2, 1])])
    for suffix, qr, sr in [('a', [4, 5], 3), ('b', [7], 5)]:
        listen('D', 1, suffix, qr, [point(text.strip()) for text in cell('scheme', 6, sr, 0).split(' (1 mark)') if text.strip()])
    buy = cell('scheme', 6, 8, 0).split(' (1 mark)')
    listen('D', 2, 'a-i', [10], [point(text.strip().removeprefix('and ')) for text in buy if text.strip()])
    listen('D', 2, 'a-ii', [12], [point(s(6, 10), 2)])
    first, second = cell('scheme', 6, 12, 0).split(' (1 mark) because ')
    listen('D', 2, 'b-i', [14, 15], [point(first), point(re.sub(r'\s*\(2 marks\)$', '', second), 2)])
    listen('D', 2, 'b-ii', [18, 19], [point(s(6, 15), 2)])
    # The scheme gives a 2+1 full-answer pool and a separate 1-mark partial
    # route. A single criterion exposes exactly 0/1/2/3, retaining both routes
    # without adding the partial alternative as a fourth bonus point.
    guidance = ' '.join(cell('scheme', 6, row, 0) for row in [19, 20, 21])
    listen('D', 3, 'a', [23, 24], [{'kind': 'criterion', 'verbatim': guidance, 'marks': 3, 'permittedMarks': [0, 1, 2, 3]}])
    listen('D', 3, 'b', [27, 28], [point(s(6, 23), 2)])
    listen('D', 3, 'c', [30], [point(text.strip()) for text in cell('scheme', 6, 25, 0).split(' (1 mark)') if text.strip()])



def consolidations(census):
    records = []
    for suffix, fragments, pp, pr, sp, sr, reason in [
        ('1a-1', list('abcde'), 3, [1, 2], 7, 3, 'One required five-cell matching table, priced one mark per cell; all five printed items remain on one task.'),
        ('2b-1', list('abcdef'), 8, [1, 2], 9, 22, 'One printed any-five-of-six meaning pool; all six items and five claim slots remain together.'),
        ('2b-2', list('abcdef'), 8, [10, 11], 10, 0, 'One printed any-five-of-six reading pool; all six items and five claim slots remain together.'),
        ('2c-1', list('abcdef'), 9, [1, 2], 10, 8, 'One printed any-five-of-six past-form pool; all six items and five claim slots remain together.'),
        ('2c-2', list('abcdef'), 9, [10, 11], 10, 15, 'One printed any-five-of-six verb-form pool; all six items and five claim slots remain together.'),
        ('3c', list(map(str, range(1, 7))), 12, [1, 2, 3], 12, 0, 'One printed any-five-of-six paired reading-and-meaning pool, one mark for each component.'),
        ('3d', list(map(str, range(1, 8))), 12, [13, 14, 15], 12, 7, 'One printed any-ten-of-twelve-blank pool across seven numbered sentences, one mark per blank.'),
    ]:
        canonical = 'ja-2025-hl-' + suffix
        paper_text = joined_selector('paper', pp, [(row, None) for row in pr])
        scheme_text = cell('scheme', sp, sr)
        task = next(task for task in census['tasks'] if canonical == 'ja-2025-hl-' + '-'.join(str(part).lower() for part in task['key'] if part is not None))
        records.append({'canonicalId': canonical, 'legacyIds': [canonical + '-' + part for part in fragments],
                        'taskKey': task['key'], 'marks': task['marks'], 'reason': reason,
                        'paperEvidence': {'page': pp, 'text': paper_text}, 'schemeEvidence': {'page': sp, 'text': scheme_text}})
    return records


def build():
    reading()
    writing()
    listening()
    census = json.loads((Path(__file__).parent / 'reviews/japanese-2025-hl-census.json').read_text())
    expected = {'ja-2025-hl-' + '-'.join(str(part).lower() for part in task['key'] if part is not None): task for task in census['tasks']}
    assert set(expected) == {card['id'] for card in CARDS}
    for card in CARDS:
        task = expected[card['id']]
        assert card['totalMarks'] == task['marks'], (card['id'], card['totalMarks'], task['marks'])
        assert card['sourceEvidence']['paperPages'] == task['paperPages']
        assert card['sourceEvidence']['schemePages'] == task['schemePages']
    assert len(CARDS) == 69, len(CARDS)
    assert sum(card['totalMarks'] for card in CARDS) == 300
    return {'subjectId': 'japanese', 'sitting': '2025-hl', 'reviewedAt': '2026-11-09',
            'sources': [{'document': name, 'path': str(path.relative_to(ROOT)), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'pagesReviewed': list(range(1, len(DOCS[name]) + 1))} for name, path in [('paper', PAPER), ('aural', AURAL), ('scheme', SCHEME)]],
            'cards': CARDS, 'selectors': EVIDENCE, 'status': 'source-reviewed-browser-qa-pending',
            'choiceAnalysis': census['choiceBoundaries'], 'consolidations': consolidations(census)}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    result = build()
    if args.write:
        (ROOT / 'scripts/markbank/authoring/reviews/japanese-2025-hl.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
        manifest = ROOT / 'components/MarkBank/figures-japanese.json'
        previous = json.loads(manifest.read_text())
        previous.update(FIGURES)
        manifest.write_text(json.dumps(previous, ensure_ascii=False, indent=2) + '\n')
        # Retain whole-page extraction; append original table columns where
        # reading across columns interleaves adjacent answers.
        scheme_md = SCHEME.with_suffix('.md')
        marker = '\n## Audited original table columns — 2025 HL pages 3 and 7\n'
        original = scheme_md.read_text().split(marker)[0]
        columns = []
        for page, bounds in [(3, [(100, 190), (192, 313), (314, 423), (425, 560)]), (7, [(150, 323), (325, 555)])]:
            for x0, x1 in bounds:
                columns.append(DOCS['scheme'][page - 1].get_text(clip=fitz.Rect(x0, 0, x1, 780), sort=True))
        scheme_md.write_text(original + marker + '\n'.join(columns))
    print(json.dumps({'cards': len(CARDS), 'marks': sum(card['totalMarks'] for card in CARDS), 'figures': len(FIGURES)}, indent=2))
