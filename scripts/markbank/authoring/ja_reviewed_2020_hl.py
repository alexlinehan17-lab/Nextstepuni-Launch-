#!/usr/bin/env python3
"""2020 Higher Japanese, independently reviewed against all original pages.

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
PAPER = ROOT / 'examiner-reports/japanese/papers/2020-hl-000-paper.pdf'
AURAL = ROOT / 'examiner-reports/japanese/papers/2020-hl-A00-paper.pdf'
SCHEME = ROOT / 'examiner-reports/japanese/schemes/2020-hl.pdf'
PINNED_SOURCES = {
    PAPER: 'c41d53e7ce61e3e1423578dc19d969c157961a36291dabd817062bf91d06c35a',
    AURAL: '801f709a01d0f50873eb68b7d8c8dd47630c61922dc114e2eae061d3a149db52',
    SCHEME: 'a30e9c6ccc490940127d6052a15c4642f685d20df7e5a269ac88619886c217db',
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
    return re.split(r'\s+/\s+', text.replace('\xa0', ' ').lstrip('/').strip(), maxsplit=1)[-1].strip()


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
    return {'kind': kind, 'label': '2020 Japanese Higher Level', 'title': 'Original examination material',
            'pages': pages, 'attribution': '© State Examinations Commission.',
            **({'presentationNote': FURIGANA_NOTE} if component == 'paper' else {}),
            '_component': component}


def add(section, q, question, rows, topic, paper_pages, scheme_pages, suffix='', rubric=None, total=None, reading=None, figure=None):
    cid = f'ja-2020-hl-{section.lower()}' + (f'-{q}' if q is not None else '') + (f'-{suffix}' if suffix else '')
    ref = f'2020 HL Section {section}' + (f' Q{q}' if q is not None else '')
    if suffix:
        ref += (' Q' if q is None else '') + ''.join(f'({part})' for part in suffix.split('-'))
    listening = section.startswith('L')
    card = {'id': cid, 'source': 'sec', 'subjectId': 'japanese', 'specVersion': 'lc-japanese-syllabus',
            'kind': 'rubric' if rubric else 'question', 'level': 'higher', 'year': 2020,
            'section': section[1:] if listening else section[0] if section[0] in '1234' else 'Q5',
            'topicId': topic, 'conceptId': concept_for(question, cid), 'questionRef': ref,
            'questionText': question, 'totalMarks': total if total is not None else sum(map(worth, rows)),
            'qa': {'gates': ['verbatim', 'tariff', 'figure'], 'humanReviewedBy': 'agent-verified', 'humanReviewedAt': '2026-11-09'},
            'sourceEvidence': {'component': 'aural' if listening else 'paper', 'paperPages': paper_pages, 'schemePages': scheme_pages},
            'schemeCitation': 'Marking points quoted from the SEC marking scheme, Japanese 2020 Higher Level — © State Examinations Commission.'}
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
    elif section == '2A' and q == 2:
        language = (8, 21, 'English')
        card['extraneousMaterialRule'] = {'multiplier': 0.5, 'sourceText': cell('scheme', 8, 20), 'schemePages': [8]}
    elif section == '2A' and q in [3, 4]:
        language = (9, 0, 'Japanese')
    elif section == '3A':
        language = (10, 6, 'Japanese')
    elif section == '3B':
        language = (10, 24, 'English')
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
    topic = 'japanese-5-0' if section.startswith('1') else 'japanese-5-1' if section == '2A' else 'japanese-5-2'
    text = prompt(page, question_rows)
    if section == '3B' or section == '2A' and q == 2:
        text = ' '.join(p(page, row, len(ROWS['paper'][page - 1][row]) - 1) for row in question_rows)
        text = re.sub(r'^(?:[1-3]\.|\([ivx]+\))\s*', '', text)
    card = add(section, q, text, rows, topic, [page], scheme_pages, suffix or '',
               reading={'1A': [2], '1B': [4], '2A': [6], '3A': [10], '3B': [10]}[section])
    row = (10 if q == 2 else 17) if section == '2A' else {'1A': 0, '1B': 22, '3A': 0, '3B': 19}[section]
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
    instruction = p(3, 2)
    labels = [p(3, row, 0) + ' ' + english(p(3, row, 1)) for row in range(4, 10)]
    add('1A', 1, instruction + '\n' + p(3, 3) + '\n' + '\n'.join(labels), [], 'japanese-5-0', [3], [7], total=6, reading=[2],
        rubric={'system': 'language-points', 'count': 6,
                'groups': [{'id': f'item-{i}', 'label': label, 'rows': [{'id': 'answer', 'text': s(7, i + 4, 1), 'marks': 1}]} for i, label in enumerate(labels, 1)],
                'taskRequirements': [instruction], 'markingGuideNote': cell('scheme', 7, 4)})
    comprehension('1A', 2, 'i', [10, 11], [anyn(options(7, [13], '/'), 2, 2, [2, 1])], [7])
    comprehension('1A', 2, 'ii', [13], [point(text) for text in split_marks(s(7, 15))], [7])
    comprehension('1A', 2, 'iii', [15], [point(s(7, 17), 2)], [7])
    comprehension('1A', 3, 'i', [17, 18], [anyn(options(7, [19], '/'), 2)], [7])
    comprehension('1A', 3, 'ii', [20], [anyn(options(7, [21, 22], '/'), 2, 2, [2, 1])], [7])
    comprehension('1A', 3, 'iii', [22], [point(text) for text in split_marks(s(7, 24))], [7])
    comprehension('1A', 4, None, [24, 25], [point(s(7, 26))], [7])
    comprehension('1B', 1, None, [23], [point(s(8, 2), 2)], [8])
    gift = comprehension('1B', 2, None, [25, 26], [
        {'kind': 'criterion', 'verbatim': selected(8, [(4, 0), (5, 0)]), 'marks': 3, 'permittedMarks': [0, 1, 1.5, 2, 2.5, 3],
         'contextNote': cell('scheme', 8, 6) + ' — ' + cell('scheme', 8, 0)
             + ' — Choose one product. Do not combine reasons across box and bag. Enter the final total after applying the printed language rule to each accepted reason: one reason earns 2 (or 1 in Japanese); two reasons earn 2+1 before any reduction. Two Japanese reasons earn 1+0.5=1.5; mixed answers can earn 2+0.5=2.5 or 1+1=2. These controls already include the language adjustment; do not halve the final total again.'}], [8])
    # A single whole-response language checkbox cannot represent mixed reasons
    # inside this mutually exclusive product choice. Keep its source selector
    # and use the exact arithmetic totals above, without applying it twice.
    gift['sourceEvidence']['manualLanguageCalculation'] = gift.pop('answerLanguageRule')
    comprehension('1B', 3, 'i', [28, 29], [point(s(8, 8), 2)], [8])
    comprehension('1B', 3, 'ii', [31, 32], [point(s(8, 10), 2)], [8])
    headers = [p(7, 3, 0), english(joined_selector('paper', 7, [(2, 2), (3, 1), (4, 0), (5, 0)])), p(7, 3, 2)]
    dates = [english(p(7, row)) for row in [7, 9]]
    rows = []
    groups = []
    for i, (date, sr) in enumerate(zip(dates, [16, 18])):
        start = len(rows)
        rows.extend([point(s(8, sr + 1, 1), contextNote=date + ' — ' + headers[0]),
                     point(s(8, sr), 2, contextNote=date + ' — ' + headers[1]),
                     point(s(8, sr, 1), contextNote=date + ' — ' + headers[2])])
        groups.append((f'day-{i + 1}', date, start, len(rows)))
    instruction = prompt(7, [1])
    table = add('2A', 1, instruction + '\n' + '\n'.join(headers + dates), rows, 'japanese-5-1', [7], [8], reading=[6, 7],
                figure=crop('ja-2020-hl-2a-1', 7, [.06, .045, .96, .26], instruction))
    group_rows(table, groups)
    for roman, qr, sr in [('i', 11, 23), ('ii', 13, 25), ('iii', 15, 27)]:
        comprehension('2A', 2, roman, [qr], [point(s(8, sr), 2)], [8])
    comprehension('2A', 3, 'i', [18, 19], [point(s(9, 2), 2)], [9])
    comprehension('2A', 3, 'ii', [21], [anyn(options(9, [4], '/'), 2, 2)], [9])
    comprehension('2A', 3, 'iii', [23, 24], [point(s(9, 7), 2)], [9])
    comprehension('2A', 3, 'iv', [26, 27], [anyn(options(9, [10], '/'), 2, 2)], [9])
    translation = split_marks(selected(9, [(14, 0), (15, 0)]))
    add('2A', 4, prompt(7, [29]) + '\n' + p(7, 30) + ' ' + p(7, 31), [point(text) for text in translation],
        'japanese-5-3', [7], [9], reading=[6])
    for section, q, pp, qr, prange, sp, sr, answer_parts, region in [
        ('2B', 1, 8, [1], range(3, 8), 9, 17, [(i, 1) for i in range(19, 24)], [.06, .055, .96, .37]),
        ('2B', 2, 8, [8, 9], range(11, 16), 9, 24, [(i, 1) for i in range(25, 30)], [.06, .37, .96, .75]),
        ('2C', 1, 9, [1, 2], range(4, 9), 9, 30, [(32, 1), (33, 1), (34, 0), (35, 1), (36, 1)], [.06, .055, .96, .44]),
        ('2C', 2, 9, [9, 10], range(12, 17), 10, 0, [(0, 1), (1, 1), (2, 0), (3, 1), (4, 1)], [.06, .44, .96, .88]),
    ]:
        instruction = prompt(pp, qr)
        labels = [re.sub(r'\s+_+\s*$', '', p(pp, row)).strip() for row in prange]
        answers = [re.sub(r'^\([ivx]+\)\s*', '', s(sp, row, group)) for row, group in answer_parts]
        groups = [{'id': f'item-{i}', 'label': label, 'rows': [{'id': 'answer', 'text': answer, 'marks': 1}]} for i, (label, answer) in enumerate(zip(labels, answers), 1)]
        note = cell('scheme', sp, sr)
        if section == '2C':
            note += ' — All five printed forms are required. The original paper labels grammar C; the scheme prints D.'
        add(section, q, instruction + '\n' + p(pp, qr[-1] + 1) + '\n' + '\n'.join(labels), [],
            'japanese-5-4' if section == '2B' else 'japanese-5-5', [pp], [sp], total=5, reading=[pp],
            figure=crop(f'ja-2020-hl-{section.lower()}-{q}', pp, region, instruction),
            rubric={'system': 'language-points', 'count': 5, 'groups': groups, 'taskRequirements': [instruction], 'markingGuideNote': note})
    comprehension('3A', 1, None, [1, 2], [anyn(options(10, [8, 9], '/'), 3)], [10])
    comprehension('3A', 2, None, [5], [point(s(10, 12), 2)], [10])
    comprehension('3A', 3, None, [7, 8], [anyn(options(10, [14], ', '), 2)], [10])
    comprehension('3A', 4, None, [10, 11], [point(s(10, 16), 2)], [10])
    comprehension('3A', 5, None, [13, 14], [anyn(options(10, [18, 19], '/'), 2, 2, [2, 1])], [10])
    comprehension('3A', 6, None, [16, 17], [point(s(10, 22), 2)], [10])
    for q, qr, rows in [(1, 20, [point(s(10, 26), 2)]), (2, 22, [anyn(options(10, [28], '/'), 2)]), (3, 24, [point(s(10, 30), 2)])]:
        comprehension('3B', q, None, [qr], rows, [10])
    instruction = prompt(12, [1, 2])
    labels = [re.sub(r'_+', '', p(12, row)).strip() for row in range(5, 10)]
    groups = [{'id': f'item-{i}', 'label': label,
               'rows': [{'id': 'reading', 'text': s(11, i, 1), 'marks': 1},
                        {'id': 'meaning', 'text': s(11, i, 3 if i == 5 else 2), 'marks': 1}]} for i, label in enumerate(labels, 1)]
    add('3C', None, instruction + '\n' + p(12, 4) + '\n' + '\n'.join(labels), [], 'japanese-5-4', [12], [11], total=10, reading=[12],
        figure=crop('ja-2020-hl-3c', 12, [.06, .045, .98, .42], instruction),
        rubric={'system': 'language-points', 'count': 5, 'groups': groups, 'taskRequirements': [instruction], 'markingGuideNote': cell('scheme', 11, 0)})
    instruction = prompt(12, [11, 12, 13])
    groups = []
    for index, sr in enumerate(range(7, 14)):
        label = p(12, 14 + index)
        text = re.sub(r'^\([ivx]+\)\s*', '', cell('scheme', 11, sr))
        answers = [text.strip() for text in text.split('1 mark') if text.strip()]
        for blank, answer in enumerate(answers, 1):
            groups.append({'id': f'sentence-{index + 1}-blank-{blank}', 'label': label + f' — blank {blank}', 'rows': [{'id': 'answer', 'text': answer, 'marks': 1}]})
    assert len(groups) == 10
    add('3D', None, instruction + '\n' + '\n'.join(p(12, row) for row in range(14, 21)), [], 'japanese-5-5', [12], [11], total=10, reading=[12],
        figure=crop('ja-2020-hl-3d', 12, [.06, .427, .98, .91], instruction),
        rubric={'system': 'language-points', 'count': 10, 'groups': groups, 'taskRequirements': [instruction],
                'markingGuideNote': cell('scheme', 11, 6) + ' — All ten printed blanks are required. The final sentence is (vii) in the paper; its scheme label repeats (vi).'})


def steps(maximum):
    return list(range(maximum + 1))


def writing():
    for q, pp, sp, maximum, lower, threshold, length in [(4, 14, 13, 20, 15, 10, 150), (5, 16, 15, 30, 20, 15, 200)]:
        ranges = [(16, 25), (25, 33), (33, 41)] if q == 4 else [(16, 24), (24, 32), (32, 39)]
        guidance = [join_cells('scheme', sp, range(first, last), 150) for first, last in ranges]
        normal_ranges = [(0, 5), (6, 14), (15, 20)] if q == 4 else [(0, 7), (8, 20), (21, 30)]
        lower_ranges = [(0, 3), (4, 10), (11, 15)] if q == 4 else [(0, 4), (5, 12), (13, 20)]
        bands = [{'label': f'{lo}–{hi}', 'marks': list(range(lo, hi + 1)), 'guidance': [text]} for (lo, hi), text in zip(normal_ranges, guidance)]
        reduced = [{'label': f'{lo}–{hi}', 'marks': list(range(lo, hi + 1)), 'guidance': [text]} for (lo, hi), text in zip(lower_ranges, guidance)]
        rule = selected(sp, [(row, None) for row in range(9, 13)])
        if q == 4:
            instruction = prompt(14, [1, 2])
            question = instruction + '\n' + '\n'.join(p(14, row) for row in range(3, 13))
            allocation = selected(12, [(row, None) for row in range(3, 10)])
            criteria = [{'id': f'point-{i}', 'label': f'({i})', 'maxMarks': 9, 'permittedMarks': steps(9), 'guidance': [allocation]} for i in ['i', 'ii']]
            criteria += [{'id': label.lower(), 'label': label, 'maxMarks': 1, 'permittedMarks': [0, 1], 'guidance': [allocation]} for label in ['Opening', 'Closing']]
            guide = 'Assess the one email option you answered. Its two content points receive up to 9 each, with opening 1 and closing 1. Use the printed 20-mark expression scale and its conditional 15-mark cap.'
        else:
            instruction = prompt(16, [1, 2, 3, 4, 5, 6])
            question = instruction + '\n' + '\n'.join(p(16, row) for row in range(7, 16))
            allocation = selected(14, [(row, None) for row in range(4, 10)])
            headings = [cell('scheme', 14, row) for row in range(11, 17)]
            criteria = [{'id': f'heading-{i}', 'label': f'Chosen heading {i}', 'maxMarks': 6, 'permittedMarks': steps(6), 'guidance': [allocation] + headings} for i in range(1, 5)]
            criteria += [
                {'id': 'discretionary', 'label': 'Discretionary content marks', 'maxMarks': 4, 'permittedMarks': steps(4), 'guidance': [allocation]},
                {'id': 'opening-closing', 'label': 'Opening and closing', 'maxMarks': 2, 'permittedMarks': steps(2), 'guidance': [allocation]},
            ]
            guide = 'Assess four different headings once each, up to 6 marks each, with 4 discretionary content marks and a combined 2 for opening and closing. Use the printed 30-mark expression scale and its conditional 20-mark cap.'
        content_ids = [criterion['id'] for criterion in criteria]
        criteria.append({'id': 'expression', 'label': 'Expression', 'maxMarks': maximum, 'permittedMarks': steps(maximum),
            'guidance': [selected(sp, [(row, None) for row in ([41, 42] if q == 4 else [39, 40])])], 'bands': bands,
            'limits': [{'id': 'lower-e', 'maxMarks': lower, 'when': {'any': [{'criterionIds': content_ids, 'atMost': threshold}, {'length': 'characters', 'below': length}]},
                        'bands': reduced, 'guidance': [rule]}]})
        add(str(q), None, question, [], 'japanese-5-7', [pp], [sp - 1, sp], total=maximum * 2, reading=[pp],
            figure=crop(f'ja-2020-hl-{q}', pp, [.045, .025, .97, .88], question),
            rubric={'system': 'language-writing', 'taskRequirements': [instruction], 'criteria': criteria, 'markingGuideNote': guide})


def listening():
    def aq(page, rows):
        return re.sub(r'^(?:\d+\.\s*)?(?:\([ivx]+\)\s*)?', '', join_cells('aural', page, rows, 300)).strip()

    def listen(part, q, roman, qr, rows, question=None, scheme_page=None):
        pp, sp = {'A': (2, 4), 'B': (3, 4), 'C': (4, 5), 'D': (5, 6)}[part]
        card = add('L' + part, q, question or aq(pp, qr), rows,
                   {'A': 'japanese-6-1', 'B': 'japanese-6-1', 'C': 'japanese-6-2', 'D': 'japanese-6-0'}[part], [pp], [scheme_page or sp], roman or '')
        card['sourceMaterial'] = source([pp], 'source-question', 'aural')
        if part == 'A':
            card['stem'] = joined_selector('aural', 2, [(1, 1), (2, 1), (3, 1)]) + ' ' + 'segments' + cell('aural', 2, 4).split('segments', 1)[-1] + ' ' + cell('aural', 2, 5, 1)
        else:
            card['stem'] = join_cells('aural', pp, range(1, 5), 300)
        if part == 'C':
            card['stem'] += '\n' + cell('aural', 4, {1: 5, 2: 15, 3: 25}[q], 0 if q == 3 else 1)
        return card

    headers = [joined_selector('aural', 2, [(10, 0), (11, 0)]),
               joined_selector('aural', 2, [(11, 1), (12, 0), (13, 0)]),
               english(joined_selector('aural', 2, [(10, 2), (11, 2), (12, 1)])),
               english(joined_selector('aural', 2, [(10, 3), (11, 3), (12, 2)]))]
    names = [cell('aural', 2, row) for row in [14, 15, 16]]
    first_best = strip_tariff(selected(4, [(6, 3), (7, 2)]))
    first_worst = strip_tariff(selected(4, [(6, 4), (7, 3), (8, 1), (9, 1)]))
    second_best = strip_tariff(selected(4, [(11, 3), (12, 2), (13, 0)]))
    second_worst = selected(4, [(11, 4), (12, 3)])
    passport = split_marks(selected(4, [(16, 4), (17, 3), (18, 0)]))
    passport = [text.strip(' /') for text in passport if text.strip(' /') and text.strip() != '(2 marks)']
    people = [
        [[point(s(4, 6, 1))], [point(s(4, 6, 2), 2)],
         [anyn([text.strip() for text in first_best.split(',')], 2)],
         [anyn([text.strip() for text in first_worst.split(',')], 2)]],
        [[point(s(4, 11, 1))], [point(s(4, 11, 2), 2)],
         [anyn([text.strip() for text in re.split(r',|/ (?=snow is)', second_best)], 2)],
         [anyn([text.strip() for text in second_worst.split(',')], 2)]],
        [[point(s(4, 16, 1))], [point(s(4, 16, 2), 2)], [point(s(4, 16, 3), 2)], [point(text) for text in passport]],
    ]
    rows, display_groups = [], []
    for person, cells in enumerate(people):
        for column, cell_rows in enumerate(cells):
            start = len(rows)
            label = names[person] + ' — ' + headers[column]
            for row in cell_rows:
                row['contextNote'] = label
            rows.extend(cell_rows)
            display_groups.append((f'person-{person + 1}-cell-{column + 1}', label, start, len(rows)))
    question = cell('aural', 2, 6, 1) + '\n' + '\n'.join(headers + names)
    table = listen('A', None, None, [], rows, question)
    table['questionFigureKey'] = crop('ja-2020-hl-la', 2, [.075, .162, .97, .76], question, 'aural')
    group_rows(table, display_groups)
    listen('B', None, 'i', [6, 7], [point(s(4, 21), 3)])
    listen('B', None, 'ii', [9], [point(s(4, 23), 2)])
    listen('B', None, 'iii', [11], [point(s(4, 25), 2)])
    listen('B', None, 'iv', [15, 16], [anyn(options(4, [28], '/'), 2, 2, [2, 1])])
    listen('B', None, 'v', [19, 20], [point(s(4, 31), 2)])
    listen('B', None, 'vi', [23, 24], [point(s(4, 33), 2)])
    listen('B', None, 'vii', [26], [anyn(options(5, [1], '/'), 2, 2, [2, 1])], scheme_page=5)
    listen('B', None, 'viii', [29], [anyn(options(5, [4], '/'), 2, 2, [2, 1])], scheme_page=5)
    listen('C', 1, 'i', [6, 7], [point(text) for text in split_marks(s(5, 9))])
    listen('C', 1, 'ii', [9, 10], [point(s(5, 11), 2)])
    listen('C', 1, 'iii', [12, 13], [anyn(options(5, [13], ', '), 3)])
    listen('C', 2, 'i', [16], [anyn(options(5, [17, 18], '/'), 2, 2, [2, 1])])
    listen('C', 2, 'ii', [18, 19], [point(s(5, 20)), anyn(options(5, [21], '/'), 2)])
    phone = listen('C', 2, 'iii', [23], [point(s(5, 23), 2, contextNote='The published scheme prices the complete phone number at 2 marks; it gives no per-digit allocation.')])
    phone['questionFigureKey'] = crop('ja-2020-hl-lc-2-iii', 4, [.51, .61, .98, .674], phone['questionText'], 'aural')
    listen('C', 3, 'i', [27], [anyn(options(5, [26], ', '), 2)])
    listen('C', 3, 'ii', [30], [anyn(options(5, [28], ', '), 2)])
    listen('C', 3, 'iii', [32], [point(s(5, 30), 2)])
    for roman, qr, sr in [('i', [5, 6], 2), ('ii', [10], 5), ('iii', [13], 8), ('iv', [16], 11), ('v', [19, 20], 14)]:
        rows = [anyn(options(6, [sr], '/'), 3)]
        if roman == 'v':
            rows[0]['contextNote'] = cell('scheme', 6, 15) + ' — The paper and scheme question both ask for two negative comments, but the published answer tariff explicitly says any three details, 1 mark each (3 total). This control follows that printed tariff; the conflicting request remains visible above.'
        listen('D', None, roman, qr, rows)
    listen('D', None, 'vi', [23, 24], [anyn(options(6, [17], '/'), 2, 2, [2, 1])])


def build():
    reading()
    writing()
    listening()
    census = json.loads((Path(__file__).parent / 'reviews/japanese-2020-hl-census.json').read_text())
    expected = {'ja-2020-hl-' + '-'.join(str(part).lower() for part in task['key'] if part is not None): task for task in census['tasks']}
    assert set(expected) == {card['id'] for card in CARDS}
    for card in CARDS:
        task = expected[card['id']]
        assert card['totalMarks'] == task['marks'], (card['id'], card['totalMarks'], task['marks'])
        assert card['sourceEvidence']['paperPages'] == task['paperPages']
        assert card['sourceEvidence']['schemePages'] == task['schemePages']
    assert len(CARDS) == 62
    assert sum(card['totalMarks'] for card in CARDS) == 300
    assert sum('answerLanguageRule' in card for card in CARDS) == 44
    return {'subjectId': 'japanese', 'sitting': '2020-hl', 'reviewedAt': '2026-11-09',
            'sources': [{'document': name, 'path': str(path.relative_to(ROOT)), 'sha256': PINNED_SOURCES[path], 'pagesReviewed': list(range(1, len(DOCS[name]) + 1))} for name, path in [('paper', PAPER), ('aural', AURAL), ('scheme', SCHEME)]],
            'cards': CARDS, 'selectors': EVIDENCE, 'status': 'source-reviewed-browser-qa-pending',
            'choiceAnalysis': census['choiceBoundaries'], 'consolidations': []}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    result = build()
    if args.write:
        (ROOT / 'scripts/markbank/authoring/reviews/japanese-2020-hl.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
        manifest = ROOT / 'components/MarkBank/figures-japanese.json'
        previous = json.loads(manifest.read_text())
        previous.update(FIGURES)
        manifest.write_text(json.dumps(previous, ensure_ascii=False, indent=2) + '\n')
        # Whole-page extraction interleaves the listening table's columns.
        # Append original physical columns, independently inspected above.
        scheme_md = SCHEME.with_suffix('.md')
        marker = '\n## Audited original table columns — 2020 HL page 4\n'
        original = scheme_md.read_text().split(marker)[0]
        columns = [DOCS['scheme'][3].get_text(clip=fitz.Rect(x0, 100, x1, 435), sort=True)
                   for x0, x1 in [(74, 154), (155, 249), (250, 397), (398, 595)]]
        scheme_md.write_text(original + marker + '\n'.join(columns))
    print(json.dumps({'cards': len(CARDS), 'marks': sum(card['totalMarks'] for card in CARDS), 'figures': len(FIGURES)}, indent=2))


