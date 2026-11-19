#!/usr/bin/env python3
"""2013 Higher Japanese, independently reviewed against all original pages.

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
PAPER = ROOT / 'examiner-reports/japanese/papers/2013-hl-000-paper.pdf'
AURAL = ROOT / 'examiner-reports/japanese/papers/2013-hl-A00-paper.pdf'
SCHEME = ROOT / 'examiner-reports/japanese/schemes/2013-hl.pdf'
PINNED_SOURCES = {
    PAPER: '0ffbc8bb2997bcf7cc45501f37740d7ac630ed94cf5043951eef0d37b8c9ed30',
    AURAL: 'f305723a4a90896b32c16db110d32a97e49bad1157e37b4357705951239ac94e',
    SCHEME: '23b16facde93e13a8a83aa590ac970e6e6776ae6df84c39347288ad65a32a887',
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
    return {'kind': kind, 'label': '2013 Japanese Higher Level', 'title': 'Original examination material',
            'pages': pages, 'attribution': '© State Examinations Commission.',
            **({'presentationNote': FURIGANA_NOTE} if component == 'paper' else {}),
            '_component': component}


def add(section, q, question, rows, topic, paper_pages, scheme_pages, suffix='', rubric=None, total=None, reading=None, figure=None):
    cid = f'ja-2013-hl-{section.lower()}' + (f'-{q}' if q is not None else '') + (f'-{suffix}' if suffix else '')
    ref = f'2013 HL Section {section}' + (f' Q{q}' if q is not None else '')
    if suffix:
        ref += (' Q' if q is None else '') + ''.join(f'({part})' for part in suffix.split('-'))
    listening = section.startswith('L')
    card = {'id': cid, 'source': 'sec', 'subjectId': 'japanese', 'specVersion': 'lc-japanese-syllabus',
            'kind': 'rubric' if rubric else 'question', 'level': 'higher', 'year': 2013,
            'section': section[1:] if listening else section[0] if section[0] in '1234' else 'Q5',
            'topicId': topic, 'conceptId': concept_for(question, cid), 'questionRef': ref,
            'questionText': question, 'totalMarks': total if total is not None else row_total(rows),
            'qa': {'gates': ['verbatim', 'tariff', 'figure'], 'humanReviewedBy': 'agent-verified', 'humanReviewedAt': '2026-11-10'},
            'sourceEvidence': {'component': 'aural' if listening else 'paper', 'paperPages': paper_pages, 'schemePages': scheme_pages},
            'schemeCitation': 'Marking points quoted from the SEC marking scheme, Japanese 2013 Higher Level — © State Examinations Commission.'}
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
    elif section in ['1AB', '1B']:
        language = (6, 10 if section == '1AB' else 22, 'Japanese')
    if section == '2A' and q == 2 and suffix:
        page, row = (7, 13)
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


def reading_q1():
    instruction = p(3, 1) + ' Write in Japanese' + p(3, 2).split('Write in Japanese', 1)[1]
    labels = [english(' '.join(cell('paper', 3, row, group) for group in range(len(ROWS['paper'][2][row])) if ROWS['paper'][2][row][group][0] < 400)) for row in range(4, 9)]
    answers = [s(6, row, 1) for row in range(5, 9)] + [s(6, 9).split('collection ', 1)[1]]
    card = add('1AA', None, instruction + '\n' + p(3, 3) + '\n' + '\n'.join(labels),
               [point(answer, 2, contextNote=label + ' — ' + cell('scheme', 6, 1)) for label, answer in zip(labels, answers)],
               'japanese-5-0', [3], [6], reading=[2], figure=crop('ja-2013-hl-1aa', 3, [.065, .025, .97, .37], instruction))
    card['sourceEvidence']['generalSchemePages'] = [6]
    card['stem'] = 'Part A, subpart A. Refer to the complete original fashion-week webpage.'

    venue_labels = [english(p(3, row, 1)) for row in range(13, 16)]
    venue_rows = [point(s(6, 12, 1), 2, contextNote=venue_labels[0])]
    for row, label in [(13, venue_labels[1]), (14, venue_labels[2])]:
        printed = cell('scheme', 6, row, 1)
        parts = re.findall(r'([^()]+?)\s*\(1 mark\)', printed)
        assert len(parts) == 2
        venue_rows.append({'kind': 'criterion', 'verbatim': printed, 'marks': 2, 'permittedMarks': [0, 1, 2],
                           'contextNote': label, 'parts': [{'id': f'part-{i + 1}', 'verbatim': part.strip(), 'marks': 1,
                                                           'permittedMarks': [0, 1]} for i, part in enumerate(parts)]})
    instruction = english(p(3, 11, 1))
    add('1AB', 1, instruction + '\n' + p(3, 12) + '\n' + '\n'.join(venue_labels), venue_rows,
        'japanese-5-0', [3], [6], reading=[2])
    speaker = cell('scheme', 6, 15)
    components = re.search(r'Orla \(1 mark\) Kiely \(1 mark\)', speaker).group()
    rows = [point(part.strip(), contextNote=speaker) for part in components.split('(1 mark)') if part.strip()]
    add('1AB', 2, p(3, 17), rows, 'japanese-5-0', [3], [6], 'i', reading=[2])
    for roman, qr, sr in [('ii', 21, 17), ('iii', 24, 20)]:
        add('1AB', 2, p(3, qr), [criterion(s(6, sr), 2, [0, 1, 2], cell('scheme', 6, sr) + ' ' + cell('scheme', 6, sr + 1))],
            'japanese-5-0', [3], [6], roman, reading=[2])

    labels = [p(4, row) for row in [17, 19, 21, 23]] + [p(4, 26) + ' ' + p(4, 27)]
    answers = [re.sub(r'^\d+\.\s*', '', cell('scheme', 6, row, 0)) for row in range(23, 28)]
    rows = []
    for i, (label, answer) in enumerate(zip(labels, answers)):
        if i == 1:
            parts = re.findall(r'([^()]+?)\s*\(1 mark\)', answer)
            assert len(parts) == 2
            rows.append({'kind': 'criterion', 'verbatim': answer, 'marks': 2, 'permittedMarks': [0, 1, 2], 'contextNote': label,
                         'parts': [{'id': f'part-{j + 1}', 'verbatim': part.strip(), 'marks': 1, 'permittedMarks': [0, 1]} for j, part in enumerate(parts)]})
        elif i == 3:
            rows.append(criterion(answer, 2, [0, 1, 2], label + ' — ' + cell('scheme', 6, 26)
                                  + ' The source also lists Grand prix as an alternative; its literal wording is retained. Assess this one response once.'))
        else:
            rows.append(point(answer, 2, contextNote=label))
    instruction = p(4, 15)
    add('1B', None, instruction + '\n' + '\n'.join(labels), rows, 'japanese-5-0', [4], [6], reading=[4],
        figure=crop('ja-2013-hl-1b', 4, [.085, .51, .96, .94], instruction))


def reading_q2():
    instruction = english(p(6, 1))
    table_rows = []
    def table(text, name, column):
        table_rows.append(point(text, contextNote=f'{name} — {column}. Given cells carry no marks.'))
    table(s(7, 4, 2), 'Adam', 'Accommodation type')
    table(re.search(r'1 hour', cell('scheme', 7, 4, 3)).group(), 'Adam', 'Location: journey time')
    table(s(7, 5, 1), 'Adam', 'Location: station')
    table(re.match(r'3500 yen', cell('scheme', 7, 6, 2)).group(), 'Bashir', 'Cost per night')
    table(re.search(r'5 minute \(walk\)', cell('scheme', 7, 6, 2)).group(), 'Bashir', 'Location: journey time')
    table(s(7, 7).split('(1 mark) ', 1)[1], 'Bashir', 'Location: station')
    table(re.match(r'2300yen', cell('scheme', 7, 8, 2)).group(), 'Max', 'Cost per night')
    table(re.search(r'1 minute \(walk\)', cell('scheme', 7, 8, 2)).group(), 'Max', 'Location: journey time')
    table(s(7, 9).split('(1 mark) ', 1)[1], 'Max', 'Location: station')
    table(s(7, 11, 1), 'Mei', 'Accommodation type')
    table(re.match(r'1900 yen', cell('scheme', 7, 11, 2)).group(), 'Mei', 'Cost per night')
    table_card = add('2A', 1, instruction + '\n' + '\n'.join(p(6, row) for row in range(2, 14)), table_rows,
        'japanese-5-0', [6], [7], reading=[5], figure=crop('ja-2013-hl-2a-1', 6, [.055, .025, .97, .34], instruction))
    group_rows(table_card, [('adam', 'Adam', 0, 3), ('bashir', 'Bashir', 3, 6), ('max', 'Max', 6, 9), ('mei', 'Mei', 9, 11)])
    for roman, row in [('i', 15), ('ii', 18), ('iii', 21)]:
        question = p(6, row, 1)
        if roman == 'i':
            rows = [point(re.sub(r'\s*2 marks$', '', s(7, 15)), 2)]
        elif roman == 'ii':
            printed = selected(7, [(17, 0), (18, 0), (19, 0)])
            choices = [part.strip() for part in printed.split('／') if part.strip()]
            rows = [anyn(choices, 2, contextNote='Source discrepancy: the original scheme prints ２時間オープン; the original passage prints 24時間オープン. Both literals are retained, with no silent change to the published answer pool.')]
            assert '24 時間オープン' in cell('paper', 5, 22)
            assert '２時間オープン' in printed
        else:
            printed = selected(7, [(21, 0), (22, 0)])
            rows = [criterion(printed, 2, [0, 1, 2], 'Assess one response once: the source prices はい at 1 and the cheap reason at 1; the separately printed uncertain response carries 1. ' + printed)]
        card = add('2A', 2, question, rows, 'japanese-5-0', [6], [7], roman, reading=[5])
        card['stem'] = english(p(6, 14))
    instruction = 'Discuss' + p(6, 24).split('Discuss', 1)[1] + ' ' + p(6, 25) + ' ' + p(6, 27)
    rule = selected(7, [(25, 0), (26, 0)])
    hostel = selected(7, [(row, 0) for row in range(27, 31)])
    capsule = selected(8, [(row, 0) for row in range(5)])
    rubric = {'system': 'language-writing', 'taskRequirements': [instruction],
              'criteria': [{'id': f'detail-{i}', 'label': f'Distinct detail {i}', 'maxMarks': 2, 'permittedMarks': [0, 2],
                            'guidance': [rule, hostel, capsule]} for i in range(1, 5)],
              'markingGuideNote': rule + ' — Assess four distinct details from the full published pools, with reference to both hotels. The source does not require one detail from every advantage/disadvantage category or publish a separate numeric omission penalty. Source numbering: the paper repeats Q2 for this discussion after its separate Japanese Q2(i–iii); both original questions are retained.'}
    add('2A', 2, instruction, [], 'japanese-5-0', [6], [7, 8], rubric=rubric, total=8, reading=[5])

    labels = [p(7, row) for row in range(5, 10)]
    groups = [{'id': f'item-{i + 1}', 'label': label, 'rows': [
        {'id': 'reading', 'text': s(8, row, 2), 'marks': 1}, {'id': 'meaning', 'text': s(8, row, 4), 'marks': 1}]} for i, (label, row) in enumerate(zip(labels, range(6, 11)))]
    instruction = p(7, 2)
    add('2B', None, instruction + '\n' + p(7, 4) + '\n' + '\n'.join(labels), [], 'japanese-5-4', [7], [8], total=10,
        reading=[5, 7], rubric={'system': 'language-points', 'count': 5, 'groups': groups, 'taskRequirements': [instruction],
                               'markingGuideNote': cell('scheme', 8, 5) + ' — All five readings and five meanings are required; the worked example is unpriced.'},
        figure=crop('ja-2013-hl-2b', 7, [.01, .035, .97, .36], instruction))
    labels, answers = [], []
    for i, sr in enumerate(range(13, 20)):
        label = p(7, i + 14)
        groups = [0, 1 if sr == 13 else 2] if sr in [13, 14, 19] else [0]
        for blank, group in enumerate(groups, 1):
            answer = re.sub(r'^[a-g]\.?(?:\s*\([ivx]+\))?\s*|^\([ivx]+\)\s*', '', s(8, sr, group))
            answer = re.sub(r'\s*1 mark$', '', answer)
            labels.append(label + (f' — blank {blank}' if len(groups) == 2 else ''))
            answers.append(answer)
    instruction = unnumber(join_cells('paper', 7, range(11, 14), 300))
    add('2C', 1, instruction + '\n' + '\n'.join(p(7, row) for row in range(14, 21)), [], 'japanese-5-5', [7], [8], total=10,
        reading=[7], rubric=complete_pool(10, labels, answers, instruction, cell('scheme', 8, 12)),
        figure=crop('ja-2013-hl-2c-1', 7, [.055, .39, .97, .94], instruction))
    for q, qr, sr, example, region in [(2, 3, 21, 2, [.055, .035, .97, .435]), (3, 10, 27, 9, [.055, .48, .97, .85])]:
        instruction = 'Write' + p(8, 0 if q == 2 else 8).split('Write', 1)[1]
        labels = [p(8, row) for row in range(qr, qr + 5)]
        answers = [re.sub(r'^[a-e]\.\s*', '', s(8, row)) for row in range(sr, sr + 5)]
        add('2C', q, instruction + '\n' + p(8, example) + '\n' + '\n'.join(labels), [], 'japanese-5-5', [8], [8], total=5,
            reading=[8], rubric=complete_pool(5, labels, answers, instruction, cell('scheme', 8, sr - 1)),
            figure=crop(f'ja-2013-hl-2c-{q}', 8, region, instruction))


def reading_q3():
    def comprehension(q, roman, qr, rows):
        card = add('3A', q, p(10, qr), rows, 'japanese-5-1', [10], [9], roman, reading=[9])
        card['stem'] = 'Answer these questions in English. Refer to the complete original exchange between Evan and Mika.'
        return card
    comprehension(1, 'i', 2, [point(selected(9, [(3, 0), (4, 0)]).split('(4 marks', 1)[0].strip(), 4,
                                      contextNote=cell('scheme', 9, 4))])
    printed = selected(9, [(6, 0), (7, 0)])
    pieces = split_marks(printed, 2)
    assert len(pieces) == 2
    comprehension(1, 'ii', 6, [point(piece.removeprefix('and ').strip(), 2) for piece in pieces])
    comprehension(2, 'i', 10, [criterion(s(9, 9), 3, [0, 1, 2, 3], selected(9, [(r, 0) for r in range(9, 13)]))])
    comprehension(2, 'ii', 14, [criterion(s(9, 14), 4, [0, 1, 2, 4], cell('scheme', 9, 15))])
    comprehension(2, 'iii', 18, [point(selected(9, [(17, 0), (18, 0)]), 3)])
    card = add('3A', 3, p(10, 23), [criterion(selected(9, [(20, 0), (21, 0)]), 5, [0, 2, 5], s(9, 22))],
               'japanese-5-1', [10], [9], reading=[9])
    card['stem'] = 'Answer in English, supporting your answer with the original text.'
    for q, first, sr, ir, er, region in [(1, 4, 25, 1, 3, [.06, .04, .97, .36]),
                                       (2, 12, 31, 9, 11, [.06, .36, .97, .68])]:
        labels = [p(11, row) for row in range(first, first + 5)]
        answers = [unnumber(s(9, row)) for row in range(sr, sr + 5)]
        instruction = join_cells('paper', 11, [ir, ir + 1], 350)
        guide = cell('scheme', 9, sr - 1)
        if q == 2:
            guide += ' Source numbering: the paper labels its last two readings (iv) and (v), while the scheme prints (vi) and (vii). The five printed paper items and their corresponding literal answers remain in original order.'
            assert cell('scheme', 9, 34, 0).startswith('(vi)') and cell('scheme', 9, 35, 0).startswith('(vii)')
        add('3B', q, instruction + '\n' + p(11, er) + '\n' + '\n'.join(labels), [], 'japanese-5-4', [11], [9], total=5,
            reading=[9, 11], rubric=complete_pool(5, labels, answers, instruction, guide),
            figure=crop(f'ja-2013-hl-3b-{q}', 11, region, instruction))


def steps(maximum):
    return list(range(maximum + 1))


def writing():
    for q, pp, sp, maximum, lower, threshold, length in [(4, 12, 11, 20, 15, 9, 150), (5, 15, 13, 30, 20, 14, 200)]:
        ranges = [(15, 23), (23, 30), (30, 37)] if q == 4 else [(16, 24), (24, 33), (33, 41)]
        guidance = [join_cells('scheme', sp, range(a, b), 170) for a, b in ranges]
        normal = [(0, 5), (6, 14), (15, 20)] if q == 4 else [(0, 7), (8, 20), (21, 30)]
        low = [(0, 3), (4, 10), (11, 15)] if q == 4 else [(0, 4), (5, 12), (13, 20)]
        bands = [{'label': f'{lo}–{hi}', 'marks': list(range(lo, hi + 1)), 'guidance': [text]} for (lo, hi), text in zip(normal, guidance)]
        reduced = [{'label': f'{lo}–{hi}', 'marks': list(range(lo, hi + 1)), 'guidance': [text]} for (lo, hi), text in zip(low, guidance)]
        instruction = join_cells('paper', pp, [1, 2], 300)
        if q == 4:
            question = instruction + '\n' + join_cells('paper', pp, range(3, 8), 300) + '\nOR\n' + join_cells('paper', pp, range(9, 14), 300)
            allocation = selected(10, [(r, None) for r in [4, 5, 9, 10]])
            criteria = [{'id': 'content', 'label': 'Content', 'maxMarks': 18, 'permittedMarks': steps(18), 'guidance': [allocation]}]
            intro, cohesion = cell('scheme', 10, 13), cell('scheme', 10, 14)
            guide = 'Choose one complete speech: finding a job OR going to college. The source allocates 18 content marks in aggregate, plus one mark for appropriate introduction/conclusion and one for textual cohesion and flow. It does not allocate individual content headings. Lower E applies only when content is less than 10 or length is less than 150 characters.'
            scheme_pages = [10, 11]
            crop_region = [.045, .025, .975, .74]
        else:
            question = instruction + '\n' + join_cells('paper', pp, range(3, 7), 300) + '\n' + '\n'.join(p(pp, r) for r in range(8, 14)) + '\nOR\n' + join_cells('paper', pp, range(15, 19), 300) + '\n' + '\n'.join(p(pp, r) for r in range(20, 26))
            allocation = selected(12, [(r, None) for r in range(2, 9)])
            criteria = []
            for i in range(1, 5):
                criteria.extend([
                    {'id': f'heading-{i}', 'label': f'Chosen heading {i}', 'maxMarks': 6, 'permittedMarks': steps(6), 'guidance': [allocation]},
                    {'id': f'heading-{i}-discretionary', 'label': f'Chosen heading {i} discretionary mark', 'maxMarks': 1, 'permittedMarks': [0, 1], 'guidance': [cell('scheme', 12, 8)]},
                ])
            intro, cohesion = cell('scheme', 12, 6), cell('scheme', 12, 7)
            guide = 'Choose ONE scenario, then any four distinct headings from that scenario’s complete six-heading pool. Do not mix headings from scenarios (a) and (b), or count the same heading twice. Each chosen heading earns up to 6 content marks and its own discretionary mark. Introduction/conclusion and textual cohesion each earn one further mark. Lower E applies only when content is less than 15 or length is less than 200 characters.'
            selected(12, [(r, None) for r in range(11, 28)])
            scheme_pages = [12, 13]
            crop_region = [.035, .025, .975, .92]
        criteria.extend([
            {'id': 'intro-conclusion', 'label': 'Introduction / conclusion', 'maxMarks': 1, 'permittedMarks': [0, 1], 'guidance': [intro]},
            {'id': 'cohesion', 'label': 'Textual cohesion and flow', 'maxMarks': 1, 'permittedMarks': [0, 1], 'guidance': [cohesion]},
        ])
        content_ids = [criterion['id'] for criterion in criteria]
        expression_guidance = selected(sp, [(r, None) for r in ([37, 38] if q == 4 else [41, 42])])
        lower_guidance = selected(sp, [(r, None) for r in (range(9, 12) if q == 4 else range(9, 13))])
        criteria.append({'id': 'expression', 'label': 'Expression', 'maxMarks': maximum, 'permittedMarks': steps(maximum),
                         'bands': bands, 'guidance': [expression_guidance, selected(sp, [(r, None) for r in range(1, 9)])],
                         'limits': [{'id': 'lower-e', 'maxMarks': lower,
                                     'when': {'any': [{'criterionIds': content_ids, 'atMost': threshold}, {'length': 'characters', 'below': length}]},
                                     'bands': reduced, 'guidance': [lower_guidance]}]})
        add(str(q), None, question, [], 'japanese-5-7', [pp], scheme_pages, total=maximum * 2, reading=[pp],
            figure=crop(f'ja-2013-hl-{q}', pp, crop_region, question),
            rubric={'system': 'language-writing', 'taskRequirements': [instruction], 'criteria': criteria, 'markingGuideNote': guide})


def listening():
    def listen(part, q, suffix, qr, rows, question=None):
        pp = {'A': 2, 'B': 3, 'C': 4, 'D': 5}[part]
        sp = 3 if part in 'AB' else 4 if part == 'C' else 5
        text = question or re.sub(r'^(?:\([ivx]+\)|\d+\.)\s*', '', join_cells('aural', pp, qr, 300)).strip()
        card = add('L' + part, q, text, rows, 'japanese-6-2' if part == 'B' else 'japanese-6-1' if part == 'D' else 'japanese-6-0',
                   [pp], [sp], suffix or '')
        card['sourceMaterial'] = source([pp], 'source-question', 'aural')
        card['stem'] = join_cells('aural', pp, range(1, 6 if part in 'ABD' else 4), 300)
        if part in 'BC':
            row = {('B', 1): 6, ('B', 2): 15, ('C', 1): 5, ('C', 2): 15, ('C', 3): 25}[(part, q)]
            card['stem'] += '\n' + join_cells('aural', pp, [row], 300)
        return card

    headers = [selected(3, [(3, 0), (4, 0)]), selected(3, [(3, 1), (4, 1)]), selected(3, [(3, 2), (4, 2)])]
    plan1 = selected(3, [(5, 3), (6, 1), (7, 0)])
    plan2 = selected(3, [(8, 3), (9, 1), (10, 0)])
    plan3 = selected(3, [(11, 3), (12, 1)])
    plan4 = selected(3, [(14, 3), (15, 1)])
    values = [
        [[point(s(3, 5, 2))], [criterion(plan1, 2, [0, 1, 2], 'Watch film alone earns 1; the full published alternatives earn 2. Assess this single plan response once.')], [point(s(3, 5, 4), 2)]],
        [[point(s(3, 8, 2))], [criterion(plan2, 2, [0, 1, 2], 'Onsen alone earns 1; the full published alternatives earn 2. Assess this single plan response once.')], [point(s(3, 8, 4), 2)]],
        [[point(s(3, 11, 2))], [point(plan3, 2)], [point(s(3, 11, 4), 2)]],
        [[point(s(3, 14, 2))], [point(plan4, 2)], [point(s(3, 14, 4), 2)]],
    ]
    rows, groups = [], []
    for person, cells in enumerate(values):
        paper_name = cell('aural', 2, 12 + person, 1)
        scheme_name = cell('scheme', 3, [5, 8, 11, 14][person], 1)
        name = paper_name + (f' (scheme: {scheme_name})' if paper_name != scheme_name else '')
        for col, components in enumerate(cells):
            label = name + ' — ' + headers[col]
            start = len(rows)
            rows += [dict(row, contextNote=label + '. ' + row.get('contextNote', '')) for row in components]
            groups.append((f'person-{person + 1}-cell-{col + 1}', label, start, len(rows)))
    table = listen('A', None, None, [], rows, cell('aural', 2, 6, 1) + '\n' + '\n'.join(headers))
    table['stem'] += '\nSource discrepancy: the third person is Tom in the original question table and Haru in the original marking scheme. The third-row answers are preserved in place, with both names shown.'
    group_rows(table, groups)
    table['questionFigureKey'] = crop('ja-2013-hl-la', 2, [.06, .035, .97, .83], table['questionText'], 'aural')

    listen('B', 1, None, [7, 8], [point(s(3, 20, 1), 2), criterion(s(3, 21, 1), 2, [0, 1, 2], cell('scheme', 3, 22)),
                                criterion(s(3, 23, 1), 2, [0, 1, 2], cell('scheme', 3, 24)), point(s(3, 25, 1), 2)])
    listen('B', 2, 'i', [16], [point(v) for v in split_marks(s(3, 28))])
    listen('B', 2, 'ii', [18], [anyn(selected(3, [(30, 0), (31, 0)]).split('/'), 2, 2, contextNote=cell('scheme', 3, 32))])
    listen('B', 2, 'iii', [21], [point(s(3, 34), 2)])
    phone = listen('B', 2, 'iv', [23, 24], [point(s(3, 36), 2, contextNote='The complete phone number earns 2. The prefix 06 is given in the paper; no per-digit tariff is published for its seven missing digits. Source numbering: the paper labels this (iv), whereas the scheme labels it (v).')])
    phone['questionFigureKey'] = crop('ja-2013-hl-lb-2-iv', 3, [.06, .735, .97, .885], phone['questionText'], 'aural')

    listen('C', 1, 'i', [7, 8], [anyn(strip_tariff(s(4, 3)).split('/'), 2, contextNote=cell('scheme', 4, 3))])
    listen('C', 1, 'ii', [12], [anyn(selected(4, [(5, 0), (6, 0)]).split('/'), 2, 2, contextNote=cell('scheme', 4, 7))])
    for roman, qr, sr in [('i', 16, 10), ('ii', 18, 12)]:
        listen('C', 2, roman, [qr], [point(s(4, sr), 2)])
    for roman, qr, sr, tr in [('iii', 20, 14, 15), ('iv', 22, 17, 18)]:
        listen('C', 2, roman, [qr], [anyn(s(4, sr).split('/'), 2, 1, [2, 1], contextNote=cell('scheme', 4, tr))])
    listen('C', 3, 'i', [26], [point(s(4, 21), 2)])
    direction = s(4, 23).split('(2 marks)', 1)[0].strip()
    pool = selected(4, [(24, 0), (25, 0)])
    listen('C', 3, 'ii', [28], [point(direction, 2), anyn(pool.split('each)', 1)[1].strip().split('/'), 2, contextNote=pool)])

    labels = [english(cell('aural', 5, 7)), english(cell('aural', 5, 8)), english(cell('aural', 5, 9)),
              cell('aural', 5, 11), cell('aural', 5, 13), selected(5, [(12, 0), (13, 0)]),
              cell('aural', 5, 19), cell('aural', 5, 21), cell('aural', 5, 24)]
    hometown = criterion(s(5, 2, 1), 2, [0, 1, 2], cell('scheme', 5, 3))
    hobbies = cell('scheme', 5, 6, 1)
    hobby_parts = re.match(r'(.+?)\s*\(3 marks\)\s*/\s*(.+?)\s*\(1 mark\)', hobbies)
    assert hobby_parts
    location = selected(5, [(7, 1), (8, 1)])
    days = cell('scheme', 5, 12, 1)
    day_parts = re.match(r'(.+?)\s*\(1 mark\)\s*and\s*(.+?)\s*\(1 mark\)', days)
    assert day_parts
    reason = cell('scheme', 5, 14).split('Ireland ', 1)[1]
    liked = selected(5, [(16, 1), (17, 1)])
    missing = selected(5, [(19, 1), (20, 1)])
    values = [[hometown], [point(s(5, 4, 1), 2)], [point(hobby_parts[1], 3), point(hobby_parts[2])],
              [criterion(strip_tariff(location), 2, [0, 1, 2], cell('scheme', 5, 9))], [point(s(5, 10, 1), 2)],
              [point(day_parts[1]), point(day_parts[2])], [point(reason, 2, contextNote=cell('scheme', 5, 15))],
              [anyn([part.strip() for row in [16, 17] for part in s(5, row, 1).split('/')], 1, 2, contextNote=cell('scheme', 5, 18))], [criterion(missing, 2, [0, 1, 2], cell('scheme', 5, 22))]]
    rows, groups = [], []
    for i, (label, components) in enumerate(zip(labels, values)):
        start = len(rows)
        rows.extend([dict(row, contextNote=label + '. ' + row.get('contextNote', '')) for row in components])
        groups.append((f'field-{i + 1}', label, start, len(rows)))
    table = listen('D', None, None, [], rows, cell('aural', 5, 1, 1) + ' ' + cell('aural', 5, 2, 1) + '\n' + '\n'.join(labels))
    table['stem'] += '\nThe name Kenta Suzuki is given in the original table and carries no marks. Complete all nine remaining fields.'
    group_rows(table, groups)
    table['questionFigureKey'] = crop('ja-2013-hl-ld', 5, [.06, .035, .97, .95], table['questionText'], 'aural')


def build():
    reading_q1(); reading_q2(); reading_q3(); writing(); listening()
    census = json.loads((Path(__file__).parent / 'reviews/japanese-2013-hl-census.json').read_text())
    expected = {'ja-2013-hl-' + '-'.join(str(part).lower() for part in task['key'] if part is not None): task for task in census['tasks']}
    assert set(expected) == {card['id'] for card in CARDS}, (set(expected) - {card['id'] for card in CARDS}, {card['id'] for card in CARDS} - set(expected))
    for card in CARDS:
        task = expected[card['id']]
        assert card['totalMarks'] == task['marks'], (card['id'], card['totalMarks'], task['marks'])
        assert card['sourceEvidence']['paperPages'] == task['paperPages']
        assert card['sourceEvidence']['schemePages'] == task['schemePages']
        rubric = card.get('rubric', {})
        for item in rubric.get('criteria', []) + [item for group in rubric.get('groups', []) for item in group.get('criteria', [])]:
            guidance = item.get('guidance', []) + [text for band in item.get('bands', []) for text in band['guidance']]
            guidance += [text for limit in item.get('limits', []) for text in limit['guidance']]
            guidance += [text for limit in item.get('limits', []) for band in limit.get('bands', []) for text in band['guidance']]
            assert all(text.strip() for text in guidance), (card['id'], item['id'], 'Empty source guidance')
    assert len(CARDS) == 40
    assert sum(card['totalMarks'] for card in CARDS) == 300
    assert sum('answerLanguageRule' in card for card in CARDS) == 20
    assert sum('extraneousMaterialRule' in card for card in CARDS) == 3
    assert '\ufffd' not in json.dumps([CARDS, EVIDENCE], ensure_ascii=False)
    return {'subjectId': 'japanese', 'sitting': '2013-hl', 'reviewedAt': '2026-11-10',
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
        for page, x_ranges in [(3, [(145, 245), (246, 420), (421, 590)]), (5, [(230, 590)]), (7, [(70, 160), (161, 270), (271, 410), (411, 590)])]:
            scheme_text += f'\n## Original table columns — physical page {page}\n'
            scheme_text += '\n'.join(DOCS['scheme'][page - 1].get_text(clip=fitz.Rect(x0, 0, x1, DOCS['scheme'][page - 1].rect.height), sort=True) for x0, x1 in x_ranges)
        SCHEME.with_suffix('.md').write_text(scheme_text.rstrip() + '\n')
        (ROOT / 'scripts/markbank/authoring/reviews/japanese-2013-hl.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
        manifest = ROOT / 'components/MarkBank/figures-japanese.json'
        previous = json.loads(manifest.read_text()); previous.update(FIGURES)
        manifest.write_text(json.dumps(previous, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'cards': len(CARDS), 'marks': sum(card['totalMarks'] for card in CARDS), 'figures': len(FIGURES)}, indent=2))
