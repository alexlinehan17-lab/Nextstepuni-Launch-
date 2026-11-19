#!/usr/bin/env python3
"""2014 Higher Japanese, independently reviewed against all original pages.

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
PAPER = ROOT / 'examiner-reports/japanese/papers/2014-hl-000-paper.pdf'
AURAL = ROOT / 'examiner-reports/japanese/papers/2014-hl-A00-paper.pdf'
SCHEME = ROOT / 'examiner-reports/japanese/schemes/2014-hl.pdf'
PINNED_SOURCES = {
    PAPER: '59b71fcb93297410cf035d781222996745dd4b602cd8923f6af8728e825e53cf',
    AURAL: 'e0c704274e1029a9e29c263027e4dd5b48a1708f3fd25cc1b6bd0c34c1e6dd3d',
    SCHEME: '5035dd9f744ba5e6fb9e19b75589787a53eb9035950d0480d1168dfe0e0654d0',
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
    return {'kind': kind, 'label': '2014 Japanese Higher Level', 'title': 'Original examination material',
            'pages': pages, 'attribution': '© State Examinations Commission.',
            **({'presentationNote': FURIGANA_NOTE} if component == 'paper' else {}),
            '_component': component}


def add(section, q, question, rows, topic, paper_pages, scheme_pages, suffix='', rubric=None, total=None, reading=None, figure=None):
    cid = f'ja-2014-hl-{section.lower()}' + (f'-{q}' if q is not None else '') + (f'-{suffix}' if suffix else '')
    ref = f'2014 HL Section {section}' + (f' Q{q}' if q is not None else '')
    if suffix:
        ref += (' Q' if q is None else '') + ''.join(f'({part})' for part in suffix.split('-'))
    listening = section.startswith('L')
    card = {'id': cid, 'source': 'sec', 'subjectId': 'japanese', 'specVersion': 'lc-japanese-syllabus',
            'kind': 'rubric' if rubric else 'question', 'level': 'higher', 'year': 2014,
            'section': section[1:] if listening else section[0] if section[0] in '1234' else 'Q5',
            'topicId': topic, 'conceptId': concept_for(question, cid), 'questionRef': ref,
            'questionText': question, 'totalMarks': total if total is not None else row_total(rows),
            'qa': {'gates': ['verbatim', 'tariff', 'figure'], 'humanReviewedBy': 'agent-verified', 'humanReviewedAt': '2026-11-10'},
            'sourceEvidence': {'component': 'aural' if listening else 'paper', 'paperPages': paper_pages, 'schemePages': scheme_pages},
            'schemeCitation': 'Marking points quoted from the SEC marking scheme, Japanese 2014 Higher Level — © State Examinations Commission.'}
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
        language = (7, 0, 'Japanese')
    if section == '2A' and q == 2:
        page, row = (7, 29)
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
    topic = 'japanese-5-0' if section.startswith('1') else 'japanese-5-2'
    text = prompt(page, question_rows)
    if section == '3B' or section == '2A' and q == 2:
        text = ' '.join(p(page, row, 1) for row in question_rows)
    card = add(section, q, text, rows, topic, [page], scheme_pages, suffix or '',
               reading={'1A': [2], '1B': [4], '2A': [6], '3A': [10], '3B': [10]}[section])
    instruction_row = (13 if q == 2 else 24) if section == '2A' else {'1A': 1, '1B': 16, '3A': 0, '3B': 23}[section]
    card['stem'] = english(p(page, instruction_row)) if section != '1A' else 'Refer to the original television webpage.'
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


def criterion(answer, maximum, permitted, note):
    return {'kind': 'criterion', 'verbatim': answer, 'marks': maximum, 'permittedMarks': permitted, 'contextNote': note}


def unnumber(text):
    return re.sub(r'^\([ivx]+\)\s*', '', text).strip()


def reading():
    instruction = p(3, 1)
    labels = [english(p(3, row, 0)) for row in range(3, 9)]
    add('1A', 1, instruction + '\n' + '\n'.join(labels), [], 'japanese-5-0', [3], [6], total=6, reading=[2],
        rubric=complete_pool(6, labels, [s(6, row, 1) for row in range(4, 10)], instruction, selected(6, [(row, None) for row in range(4, 10)])))
    for roman, qr, sr in [('i', 11, 11), ('ii', 12, 12)]:
        c = comprehension('1A', 2, roman, [qr], [point(s(6, sr, 1), 2)], [6])
        c['questionText'] = p(3, 10) + ' ' + english(p(3, qr, 0))
    for roman, qr, sr in [('i', 14, 13), ('ii', 17, 14)]:
        comprehension('1A', 3, roman, [qr], [point(clean_tariff(s(6, sr).split('NHK.', 1)[1]), 2)], [6])
    for roman, qr, answer in [('i', 21, s(6, 16).split('10:00', 1)[1].strip()), ('ii', 22, s(6, 17, 1))]:
        c = comprehension('1A', 4, roman, [20], [point(answer, 2)], [6])
        c['questionText'] += ' ' + p(3, qr, 1)
    comprehension('1A', 5, 'i', [24], [point(s(6, 19), 2)], [6])
    comprehension('1A', 5, 'ii', [27], [point(clean_tariff(s(6, 21))), point(s(6, 21, 1))], [6])
    comprehension('1B', 1, None, [18], [point(v) for v in split_marks(s(7, 2))], [7])
    comprehension('1B', 2, None, [21], [criterion(s(7, 4).split('  (')[0], 2, [0, 1, 2], cell('scheme', 7, 4))], [7])
    comprehension('1B', 3, None, [24], [point(s(7, 6), 2)], [7])
    comprehension('1B', 4, None, [27], [point(s(7, 8), 2)], [7])

    headers = [p(7, 3, 0), p(7, 4), p(7, 6) + ' ' + p(7, 7)]
    names = [p(7, row, 0) for row in [8, 10, 12]]
    values = [
        [[], [criterion(selected(7, [(14, 2), (15, 0), (16, 0)]), 2, [0, 1, 2], selected(7, [(18, 0), (19, 0), (20, 0)]))], [point(s(7, 14, 3)), point(s(7, 15, 1))]],
        [[point(s(7, 21, 1))], [point(s(7, 21, 2), 2)], []],
        [[point(clean_tariff(selected(7, [(23, 1), (24, 0)])), contextNote=cell('scheme', 7, 27))], [criterion(clean_tariff(selected(7, [(23, 2), (24, 1), (26, 0)])), 2, [0, 1, 2], cell('scheme', 7, 28))], [point(s(7, 23, 3)), point(s(7, 25))]],
    ]
    rows, groups = [], []
    discrepancy = 'The scheme table labels Makoto Takashi, but the original profile, paper table and subsequent scheme answer identify Makoto Hayashi. This card retains the original identity.'
    cell('scheme', 7, 23, 0); cell('scheme', 8, 8)
    for person, cells in enumerate(values):
        for col, components in enumerate(cells):
            if not components: continue
            label = names[person] + ' — ' + headers[col]
            start = len(rows)
            rows += [dict(row, contextNote=label + '. ' + row.get('contextNote', '') + (' ' + discrepancy if person == 2 else '')) for row in components]
            groups.append((f'person-{person + 1}-cell-{col + 1}', label, start, len(rows)))
    table = add('2A', 1, english(p(7, 1)) + '\n' + '\n'.join(headers + names), rows, 'japanese-5-2', [7], [7], reading=[6])
    table['sourceEvidence']['interpretiveSchemePages'] = [8]
    group_rows(table, groups)
    table['questionFigureKey'] = crop('ja-2014-hl-2a-1', 7, [.065, .04, .95, .335], table['questionText'])
    comprehension('2A', 2, 'i', [14], [criterion(s(7, 31), 2, [0, 1, 2], cell('scheme', 7, 32))], [7])
    comprehension('2A', 2, 'ii', [16], [point(s(7, 34), 2)], [7])
    # Retain the complete Japanese sentence while exposing its two printed components.
    components = split_marks(s(8, 1))
    comprehension('2A', 2, 'iii', [18], [point(components[0]), point(components[1], contextNote=cell('scheme', 8, 1))], [8])
    comprehension('2A', 2, 'iv', [20], [point(s(8, 3), 2)], [8])
    for roman, qr, answer in [('i', 25, s(8, 5, 1).split('Miyu Kawasaki', 1)[1].strip()), ('ii', 26, selected(8, [(6, 0), (7, 0)]).split('Hidemi Mori', 1)[1].strip())]:
        c = comprehension('2A', 3, roman, [24], [point(answer, 2)], [8])
        c['questionText'] += '\n' + p(7, qr, 1).split('_', 1)[0].strip()
    culture = s(8, 8).split('Makoto Hayashi', 1)[1].strip()
    culture_parts = split_marks(culture)
    rows = [point(culture_parts[0]), point(culture_parts[1].removeprefix('and ').strip())]
    # Ignore only the separate printed total following the answer-alternative slash.
    c = comprehension('2A', 3, 'iii', [24], rows, [8])
    c['questionText'] += '\n' + p(7, 27, 1).split('_', 1)[0].strip()
    c['answerVariants'] = [
        {'id': 'teaching', 'label': 'Teaching culture and origami', 'rows': c['rows']},
        {'id': 'voluntary', 'label': 'Voluntary work', 'rows': [dict(point(s(8, 9), 2), id='r-1')]},
    ]
    translation = add('2A', 4, english(p(7, 28)) + '\n' + p(7, 29), [point(v, 2) for v in split_marks(s(8, 12), 2)], 'japanese-5-3', [7], [8], reading=[6])
    translation['stem'] = p(7, 29)
    for section, q, page, qr, sp, sr, instruction_row in [('2B', 1, 8, 4, 8, 16, 2), ('2B', 2, 8, 12, 8, 22, 10), ('2C', 1, 9, 4, 9, 2, 2), ('2C', 2, 9, 12, 9, 8, 10)]:
        labels = [p(page, row).split('_', 1)[0].strip() if section == '2B' else p(page, row).rstrip('_ ') for row in range(qr, qr + 5)]
        instruction = p(page, instruction_row)
        answers = [unnumber(s(sp, row)) for row in range(sr, sr + 5)]
        card = add(section, q, instruction + '\n' + '\n'.join(labels), [], 'japanese-5-4' if section == '2B' else 'japanese-5-5', [page], [sp], total=5, reading=[6],
                   rubric=complete_pool(5, labels, answers, instruction, cell('scheme', sp, sr - 1)))
        card['questionFigureKey'] = crop(f'ja-2014-hl-{section.lower()}-{q}', page, [.04, .025 if q == 1 else .345, .975, .34 if q == 1 else .68], card['questionText'])
    comprehension('3A', 1, 'i', [2], [anyn(selected(9, [(16, 0), (17, 0)]).split('/'), 2, 1, [2, 1], contextNote=cell('scheme', 9, 17, 1))], [9])
    comprehension('3A', 1, 'ii', [6], [point(s(9, 19), 2)], [9])
    comprehension('3A', 2, 'i', [10], [point(s(9, 21), 2)], [9])
    comprehension('3A', 2, 'ii', [13], [criterion(s(9, 23), 2, [0, 1, 2], cell('scheme', 9, 24))], [9])
    comprehension('3A', 3, 'i', [16], [criterion(selected(9, [(26, 0), (27, 0), (28, 0)]), 3, [0, 1, 3], cell('scheme', 9, 29))], [9])
    comprehension('3A', 3, 'ii', [20], [point(s(9, 31), 2)], [9])
    comprehension('3B', 1, None, [24], [point(s(10, 2), 3)], [10])
    comprehension('3B', 2, None, [26], [point(selected(10, [(4, 0), (5, 0)]), 3)], [10])
    instruction, groups, labels = p(12, 3), [], []
    for i, sr, gi in [(0, 7, 1), (1, 8, 0), (2, 9, 0), (3, 10, 0), (4, 11, 0)]:
        label = p(12, 5 + i).split('_', 1)[0].strip(); labels.append(label)
        reading_answer = re.sub(r'^[a-d]\.\s*', '', unnumber(clean_tariff(s(10, sr, gi))))
        meaning = clean_tariff(s(10, sr, 2 if i in [0, 1, 3] else 1))
        groups.append({'id': f'item-{i + 1}', 'label': label, 'rows': [{'id': 'reading', 'text': reading_answer, 'marks': 1}, {'id': 'meaning', 'text': meaning, 'marks': 1}]})
    guide = 'Each of the five readings earns 1 and each meaning earns 1. Source letter discrepancies: (iv) the paper prints a. にんき while the scheme prints b. にんき; (v) the paper prints b. でんしゃ while the scheme prints a. でんしゃ. The hiragana readings agree and are retained exactly; no additional penalty is invented.'
    c = add('3C', None, instruction + '\n' + '\n'.join(labels), [], 'japanese-5-4', [12], [10], total=10, reading=[10],
            rubric={'system': 'language-points', 'count': 5, 'groups': groups, 'taskRequirements': [instruction], 'markingGuideNote': guide})
    c['questionFigureKey'] = crop('ja-2014-hl-3c', 12, [.04, .025, .975, .375], c['questionText'])
    labels, answers = [], []
    for i, sr in enumerate(range(13, 19)):
        label = p(12, 14 + i)
        gis = [1] if i in [0, 5] else [1, 3]
        for blank, gi in enumerate(gis, 1):
            labels.append(label + (f' — blank {blank}' if len(gis) > 1 else ''))
            answers.append(clean_tariff(s(10, sr, gi)))
    instruction = p(12, 13)
    c = add('3D', None, instruction + '\n' + '\n'.join(p(12, row) for row in range(14, 20)), [], 'japanese-5-5', [12], [10], total=10, reading=[10],
            rubric=complete_pool(10, labels, answers, instruction, cell('scheme', 10, 12)))
    c['questionFigureKey'] = crop('ja-2014-hl-3d', 12, [.04, .40, .975, .84], c['questionText'])


def steps(maximum):
    return list(range(maximum + 1))


def writing():
    for q, pp, sp, maximum, lower, threshold, length in [(4, 14, 12, 20, 15, 9, 150), (5, 16, 14, 30, 20, 14, 200)]:
        ranges = [(16, 24), (24, 31), (31, 38)] if q == 4 else [(7, 15), (15, 24), (24, 32)]
        guidance = [join_cells('scheme', sp, range(a, b), 150 if q == 4 else 168) for a, b in ranges]
        normal = [(0, 5), (6, 14), (15, 20)] if q == 4 else [(0, 7), (8, 20), (21, 30)]
        low = [(0, 3), (4, 10), (11, 15)] if q == 4 else [(0, 4), (5, 12), (13, 20)]
        bands = [{'label': f'{lo}–{hi}', 'marks': list(range(lo, hi + 1)), 'guidance': [text]} for (lo, hi), text in zip(normal, guidance)]
        reduced = [{'label': f'{lo}–{hi}', 'marks': list(range(lo, hi + 1)), 'guidance': [text]} for (lo, hi), text in zip(low, guidance)]
        allocation = selected(sp - 1, [(r, None) for r in (range(4, 11) if q == 4 else range(5, 11))])
        if q == 4:
            instruction = p(14, 2)
            question = instruction + '\n' + '\n'.join(p(14, r) for r in [3, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15, 16])
            criteria = [{'id': f'point-{i}', 'label': f'Content point {i}', 'maxMarks': 6, 'permittedMarks': steps(6), 'guidance': [allocation]} for i in [1, 2, 3]]
            guide = 'Assess one complete diary option: Christmas OR birthday. Each of the three required content responses earns up to 6. The two discretionary marks are assessed together for appropriate introduction and ending; the scheme does not prescribe one mark each. Lower E applies only when content is less than 10 or length is less than 150 characters.'
        else:
            instruction = ' '.join(p(16, r) for r in [4, 5, 6])
            question = instruction + '\n' + '\n'.join(p(16, r) for r in range(7, 15))
            criteria = []
            for i in range(1, 5):
                criteria += [
                    {'id': f'heading-{i}', 'label': f'Chosen heading {i}', 'maxMarks': 6, 'permittedMarks': steps(6), 'guidance': [allocation]},
                    {'id': f'heading-{i}-discretionary', 'label': f'Chosen heading {i} discretionary mark', 'maxMarks': 1, 'permittedMarks': [0, 1], 'guidance': [cell('scheme', 13, 10)]},
                ]
            guide = 'Choose four distinct headings from all eight printed in both the paper and scheme. Each chosen heading earns up to 6 content marks and its own discretionary mark. The remaining two discretionary marks assess introduction/conclusion together; no one-mark-per-part split is published. Source discrepancy: the content line says “6 marks for any 4 headings 1-6”, although both sources list eight headings and the next expression page explicitly uses numbering 1–8. All eight remain available. Lower E applies only when content is less than 15 or length is less than 200 characters.'
            selected(13, [(r, None) for r in range(13, 21)])
        criteria.append({'id': 'intro-ending', 'label': 'Introduction and ending', 'maxMarks': 2, 'permittedMarks': [0, 1, 2], 'guidance': [allocation]})
        content_ids = [c['id'] for c in criteria]
        criteria.append({'id': 'expression', 'label': 'Expression', 'maxMarks': maximum, 'permittedMarks': steps(maximum), 'bands': bands,
                         'guidance': [selected(sp, [(38, None), (39, None)] if q == 4 else [(32, None), (33, None)])],
                         'limits': [{'id': 'lower-e', 'maxMarks': lower, 'when': {'any': [{'criterionIds': content_ids, 'atMost': threshold}, {'length': 'characters', 'below': length}]}, 'bands': reduced, 'guidance': [selected(sp, [(r, None) for r in (range(9, 13) if q == 4 else range(0, 4))])]}]})
        add(str(q), None, question, [], 'japanese-5-7', [pp], [sp - 1, sp], total=maximum * 2, reading=[pp],
            figure=crop(f'ja-2014-hl-{q}', pp, [.045, .025, .975, .92], question),
            rubric={'system': 'language-writing', 'taskRequirements': [instruction], 'criteria': criteria, 'markingGuideNote': guide})


def listening():
    def listen(part, q, suffix, qr, rows, question=None, rubric=None, total=None):
        pp = {'A': 2, 'B': 3, 'C': 4, 'D': 5}[part]
        sp = 3 if part == 'A' or part == 'B' and q == 1 and suffix != 'iv' else 5 if part == 'D' else 4
        text = question or re.sub(r'^(?:\([ivx]+\)|\d+\.)\s*', '', join_cells('aural', pp, qr, 300)).strip()
        card = add('L' + part, q, text, rows, 'japanese-6-2' if part == 'B' else 'japanese-6-0', [pp], [sp], suffix or '', rubric=rubric, total=total)
        card['sourceMaterial'] = source([pp], 'source-question', 'aural')
        card['stem'] = join_cells('aural', pp, range(1, 7 if part == 'A' else 6 if part == 'B' else 5), 300)
        if part in 'BC':
            row = {('B', 1): 6, ('B', 2): 20, ('B', 3): 26, ('C', 1): 5, ('C', 2): 21}[(part, q)]
            card['stem'] += '\n' + join_cells('aural', pp, [row], 300)
        return card
    headers = [selected(3, [(3, 0), (4, 0)]), cell('scheme', 3, 3, 1), selected(3, [(3, 2), (4, 1)]), cell('scheme', 3, 3, 3)]
    trip1 = selected(3, [(5, 3), (6, 1), (7, 0), (8, 0), (9, 0)])
    trip2 = selected(3, [(13, 3), (14, 1), (15, 0), (16, 0), (17, 0), (18, 0)])
    trip3 = selected(3, [(22, 3), (23, 2), (24, 0), (25, 0)])
    trip3guide = selected(3, [(26, 0), (27, 0), (29, 0)]) + ' Assess two distinct responses against this complete pool. Put the higher-value response first: a full detail earns 2 first and 1 second; cycled alone earns 1. Count each cycling concept once and never count a partial and full version of the same detail twice.'
    values = [
        [[point(s(3, 5, 1))], [point(s(3, 5, 2))], [anyn([v.strip() for v in re.split(r'/|,', trip1)], 2, 1, [2, 1], contextNote=selected(3, [(10, 0), (11, 0)]))], [anyn(s(3, 5, 4).split('/'), 1)]],
        [[point(s(3, 13, 1))], [point(s(3, 13, 2))], [anyn(trip2.split('/'), 2, 1, [2, 1], contextNote=selected(3, [(19, 0), (20, 0)]))], [anyn(s(3, 13, 4).split('/'), 1)]],
        [[point(s(3, 22, 1))], [point(s(3, 22, 2))], [criterion(trip3, 2, [0, 1, 2], 'First distinct trip detail. ' + trip3guide), criterion(trip3, 1, [0, 1], 'Second distinct trip detail. ' + trip3guide)], [point(s(3, 22, 4))]],
    ]
    rows, groups = [], []
    for person, cells in enumerate(values):
        for col, components in enumerate(cells):
            label = f'{person + 1}. — ' + headers[col]
            start = len(rows)
            rows += [dict(row, contextNote=label + '. ' + row.get('contextNote', '')) for row in components]
            groups.append((f'person-{person + 1}-cell-{col + 1}', label, start, len(rows)))
    table = listen('A', None, None, [], rows, cell('aural', 2, 7, 1) + '\n' + '\n'.join(headers))
    group_rows(table, groups)
    table['questionFigureKey'] = crop('ja-2014-hl-la', 2, [.05, .025, .975, .68], table['questionText'], 'aural')
    listen('B', 1, 'i', [7], [point(v) for v in split_marks(s(3, 33))])
    sky = selected(3, [(35, 0), (36, 0)])
    parts = [v.strip().rstrip('.') for v in sky.split('/')]
    groups = [
        {'id': 'record', 'label': 'Tallest tower / Guinness record', 'rows': [{'id': 'answer', 'text': ' / '.join(parts[:2]), 'marks': 2}]},
        {'id': 'height', 'label': 'Height', 'rows': [{'id': 'answer', 'text': parts[2], 'marks': 2}]},
        {'id': 'amenities', 'label': 'At least two amenities', 'rows': [], 'criteria': [{'id': 'amenities', 'label': 'Two amenities given', 'maxMarks': 2, 'permittedMarks': [0, 2], 'guidance': [parts[3]]}]},
    ]
    listen('B', 1, 'ii', [9], [], rubric={'system': 'language-points', 'count': 2, 'groups': groups,
        'taskRequirements': [join_cells('aural', 3, [9], 300)], 'markingGuideNote': cell('scheme', 3, 37, 0) + ' The tallest-tower/Guinness wording is one record concept. The literal scheme height is 630 meters. Manually award the amenities concept 2 only when at least two of restaurants, shops and cafes are supplied; one amenity earns 0, with no invented 1-mark partial. Amenities count as one concept within the overall two-concept limit.'}, total=4)
    listen('B', 1, 'iii', [13, 14], [point(v.lstrip('/ ').strip(), m) for v, m in zip(split_marks(s(3, 39), 2), [2, 1])])
    # The first and second direction components have different printed tariffs.
    c = CARDS[-1]
    c['rows'][1]['verbatim'] = re.sub(r'\s*\(1 mark\)\s*$', '', c['rows'][1]['verbatim']).strip()
    phone = listen('B', 1, 'iv', [17], [point(s(4, 1), 3, contextNote='The scheme prices the complete number at 3 marks. The eight missing digits have no separate published tariff.')])
    phone['questionFigureKey'] = crop('ja-2014-hl-lb-1-iv', 3, [.515, .49, .97, .575], phone['questionText'], 'aural')
    pool = selected(4, [(4, 0), (5, 0), (6, 0)])
    groups = [{'id': f'response-{i}', 'label': f'Distinct response {i}', 'rows': [], 'criteria': [{'id': f'response-{i}', 'label': f'Distinct response {i}', 'maxMarks': 2, 'permittedMarks': [0, 1, 2], 'guidance': [pool]}]} for i in [1, 2, 3]]
    listen('B', 2, None, [21], [], rubric={'system': 'language-points', 'count': 3, 'groups': groups, 'taskRequirements': [join_cells('aural', 3, [21], 300)], 'markingGuideNote': 'Assess three distinct responses against the complete printed pool. A full printed detail earns 2; the printed show-only answer earns 1. Count each concept once: a partial and full version of the same detail cannot be counted twice, and synonymous dancer wording is not an extra fact.'}, total=6)
    for roman, qr, sr in [('i', 28, 9), ('ii', 30, 11)]:
        text = s(4, sr)
        answer = re.sub(r'\s*\((?:any 2 details, )?2 marks and (?:one|1) mark\)\s*$', '', text)
        listen('B', 3, roman, [qr], [anyn(answer.split('/'), 2, 1, [2, 1], contextNote=cell('scheme', 4, sr))])
    listen('C', 1, 'i', [6, 7], [point(s(4, 15), 2)])
    experience = selected(4, [(17, 0), (18, 0)])
    exp_parts = split_marks(experience, 2)
    listen('C', 1, 'ii', [9, 10], [criterion(exp_parts[0], 2, [0, 1, 2], cell('scheme', 4, 19)), point(re.sub(r'\s*\(1 mark\)\s*$', '', exp_parts[1]))])
    listen('C', 1, 'iii', [13], [anyn(s(4, 21).split('/'), 2, 2, contextNote=cell('scheme', 4, 22, 0))])
    listen('C', 1, 'iv', [18], [anyn(s(4, 24).split('/'), 2, 2, contextNote=cell('scheme', 4, 25))])
    for roman, qr, sr, tr in [('i', 22, 28, 29), ('ii', 25, 31, 32)]:
        listen('C', 2, roman, [qr], [anyn(s(4, sr).split('/'), 2, 1, [2, 1], contextNote=cell('scheme', 4, tr, 0))])
    listen('D', None, 'i', [5], [point(s(5, 2), 2)])
    listen('D', None, 'ii', [7, 8], [point(s(5, 4), 2)])
    listen('D', None, 'iii', [11, 12], [anyn(selected(5, [(6, 0), (7, 0)]).split('/'), 2, 3, contextNote=cell('scheme', 5, 7, 1))])
    listen('D', None, 'iv', [15, 16], [anyn(s(5, 9).split('/'), 2, 3, contextNote=cell('scheme', 5, 10, 0))])
    listen('D', None, 'v', [20, 21], [point(s(5, 12, 0)), point(s(5, 12, 1))])


def build():
    reading(); writing(); listening()
    census=json.loads((Path(__file__).parent/'reviews/japanese-2014-hl-census.json').read_text())
    expected={'ja-2014-hl-'+'-'.join(str(part).lower() for part in task['key'] if part is not None):task for task in census['tasks']}
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
    assert len(CARDS)==57
    assert sum(card['totalMarks'] for card in CARDS)==300
    assert sum('answerLanguageRule' in card for card in CARDS)==23
    assert sum('extraneousMaterialRule' in card for card in CARDS)==4
    assert '\ufffd' not in json.dumps([CARDS,EVIDENCE],ensure_ascii=False)
    return {'subjectId':'japanese','sitting':'2014-hl','reviewedAt':'2026-11-10',
        'sources':[{'document':name,'path':str(path.relative_to(ROOT)),'sha256':PINNED_SOURCES[path],'pagesReviewed':list(range(1,len(DOCS[name])+1))} for name,path in [('paper',PAPER),('aural',AURAL),('scheme',SCHEME)]],
        'cards':CARDS,'selectors':EVIDENCE,'status':'source-captured','choiceAnalysis':census['choiceBoundaries'],'consolidations':[]}


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--write',action='store_true');args=parser.parse_args()
    result=build()
    if args.write:
        scheme_text=''.join(f'\n## Page {i+1}\n\n'+page.get_text(sort=True) for i,page in enumerate(DOCS['scheme']))
        scheme_text+='\n## Original text with furigana folded at its printed character\n'
        scheme_text+=''.join(f'\n### Physical page {i+1}\n\n'+'\n'.join(' '.join(group[2] for group in row) for row in rows)+'\n' for i,rows in enumerate(ROWS['scheme']))
        for page,x_ranges in [(3,[(90,208),(209,307),(308,421),(422,590)]),(7,[(165,300),(301,435),(436,590)])]:
            scheme_text+=f'\n## Original table columns — physical page {page}\n'
            scheme_text+='\n'.join(DOCS['scheme'][page-1].get_text(clip=fitz.Rect(x0,0,x1,DOCS['scheme'][page-1].rect.height),sort=True) for x0,x1 in x_ranges)
        SCHEME.with_suffix('.md').write_text(scheme_text.rstrip()+'\n')
        (ROOT/'scripts/markbank/authoring/reviews/japanese-2014-hl.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
        manifest=ROOT/'components/MarkBank/figures-japanese.json'; previous=json.loads(manifest.read_text());previous.update(FIGURES)
        manifest.write_text(json.dumps(previous,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'cards':len(CARDS),'marks':sum(card['totalMarks'] for card in CARDS),'figures':len(FIGURES)},indent=2))
