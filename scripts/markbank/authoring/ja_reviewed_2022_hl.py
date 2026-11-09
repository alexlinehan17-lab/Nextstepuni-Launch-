#!/usr/bin/env python3
"""2022 Higher Japanese, independently reviewed against all original pages.

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
PAPER = ROOT / 'examiner-reports/japanese/papers/2022-hl-000-paper.pdf'
AURAL = ROOT / 'examiner-reports/japanese/papers/2022-hl-A00-paper.pdf'
SCHEME = ROOT / 'examiner-reports/japanese/schemes/2022-hl.pdf'
PINNED_SOURCES = {
    PAPER: '39206c2a7866abe770cd11ab26e442750b77d9846b67c25749f5525f2d212120',
    AURAL: 'bf2cf1aa89ac7b0a2df950367a91db0b0af0a0c71fa174380ccd7a22644fa970',
    SCHEME: '99f3a19d2594fb1d0832877f21f018d07f6947900f20003cada3c34ca25083a0',
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
    return {'kind': kind, 'label': '2022 Japanese Higher Level', 'title': 'Original examination material',
            'pages': pages, 'attribution': '© State Examinations Commission.',
            **({'presentationNote': FURIGANA_NOTE} if component == 'paper' else {}),
            '_component': component}


def add(section, q, question, rows, topic, paper_pages, scheme_pages, suffix='', rubric=None, total=None, reading=None, figure=None):
    cid = f'ja-2022-hl-{section.lower()}' + (f'-{q}' if q is not None else '') + (f'-{suffix}' if suffix else '')
    ref = f'2022 HL Section {section}' + (f' Q{q}' if q is not None else '')
    if suffix:
        ref += ''.join(f'({part})' for part in suffix.split('-'))
    listening = section.startswith('L')
    card = {'id': cid, 'source': 'sec', 'subjectId': 'japanese', 'specVersion': 'lc-japanese-syllabus',
            'kind': 'rubric' if rubric else 'question', 'level': 'higher', 'year': 2022,
            'section': section[1:] if listening else section[0] if section[0] in '1234' else 'Q5',
            'topicId': topic, 'conceptId': concept_for(question, cid), 'questionRef': ref,
            'questionText': question, 'totalMarks': total if total is not None else sum(map(worth, rows)),
            'qa': {'gates': ['verbatim', 'tariff', 'figure'], 'humanReviewedBy': 'agent-verified', 'humanReviewedAt': '2026-11-09'},
            'sourceEvidence': {'component': 'aural' if listening else 'paper', 'paperPages': paper_pages, 'schemePages': scheme_pages},
            'schemeCitation': 'Marking points quoted from the SEC marking scheme, Japanese 2022 Higher Level — © State Examinations Commission.'}
    if rubric:
        card['rubric'] = rubric
    else:
        card['tariffModel'] = {'kind': 'fixed'}
        card['rows'] = [dict(row, id=f'r-{i + 1}') for i, row in enumerate(rows)]
    original_ids = set(re.findall(r'    id: "([^"]+)"', (ROOT / 'components/MarkBank/cards/japanese/higher.ts').read_text()))
    if cid in original_ids:
        card['qa']['gates'].append('reviewed-card-correction')
    language = (3, 1, 'Japanese') if listening else {
        '1A': (7, 2, 'Japanese'), '1B': (8, 0, 'Japanese'),
        '3A': (10, 16, 'Japanese'), '3B': (11, 0, 'English'),
    }.get(section)
    if section == '2A':
        language = (8, 14, 'Japanese') if q == 1 else (8, 22, 'English') if q == 2 else (9, 0, 'Japanese')
    if language:
        page, row, name = language
        text = joined_selector('scheme', 8, [(22, None), (23, None)]) if section == '2A' and q == 2 else cell('scheme', page, row)
        card['sourceEvidence']['generalSchemePages'] = [page]
        card['answerLanguageRule'] = {'otherLanguageMultiplier': 0.5, 'penalizedLanguage': name, 'sourceText': text, 'schemePages': [page]}
        if section == '2A' and q == 2:
            card['extraneousMaterialRule'] = {'multiplier': 0.5, 'sourceText': text, 'schemePages': [page]}
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


def comprehension(section, q, suffix, question_rows, rows, scheme_pages, total=None):
    page = 3 if section == '1A' else 4 if section == '1B' else 7 if section == '2A' else 11
    topic = {'1': 'japanese-5-0', '2': 'japanese-5-2', '3': 'japanese-5-2'}[section[0]]
    text = prompt(page, question_rows)
    if section == '3B':
        text = p(page, question_rows[0], 1)
    if section == '2A' and q == 2:
        text = re.sub(r'^\([ivx]+\)\s*', '', ' '.join(p(page, row, 1) if len(ROWS['paper'][page - 1][row]) > 1 else p(page, row) for row in question_rows))
    card = add(section, q, text, rows, topic, [page], scheme_pages, suffix or '', total=total,
               reading={'1A': [2], '1B': [4], '2A': [6], '3A': [10], '3B': [10]}[section])
    if section == '2A':
        card['stem'] = english(p(7, 8 if q == 2 else 17, 1))
    else:
        row = {'1A': 0, '1B': 19, '3A': 0, '3B': 19}[section]
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


def reading():
    instruction = prompt(3, [1, 2])
    labels = [p(3, row, 0) + ' ' + english(p(3, row, 1)) for row in range(4, 10)]
    card = add('1A', 1, instruction + '\n' + english(p(3, 3, 0)) + ' ' + p(3, 3, 1) + '\n' + '\n'.join(labels),
        [point(s(7, row, 2), contextNote=label) for row, label in zip(range(4, 10), labels)],
        'japanese-5-0', [3], [7], reading=[2])
    card['rows'][0]['contextNote'] += ' — The paper says links 1–6, but the original website prints 1–10; the published answers include 7 and 8. Use the complete source website.'
    comprehension('1A', 2, None, [10], [anyn(options(7, [12], '/'), 3)], [7])
    comprehension('1A', 3, None, [12], [anyn(options(7, [15], '/'), 2)], [7])
    comprehension('1A', 4, None, [14, 15], [point(s(7, 18))], [7])
    comprehension('1A', 5, 'i', [17, 18], [point(clean_tariff(s(7, 20)))], [7])
    comprehension('1A', 5, 'ii', [20, 21], [anyn(options(7, [22], '/'), 2)], [7])
    table_text = prompt(3, [23]) + '\n' + '\n'.join([p(3, 25), english(p(3, 26)), p(3, 28), p(3, 30), english(p(3, 31))])
    date = [part.strip() for part in s(7, 25, 1).split('(1 mark)') if part.strip()]
    send = [part.strip(' ,') for part in s(7, 28, 1).split('(1 mark)') if part.strip(' ,')]
    prize = joined_selector('scheme', 7, [(30, 1), (31, 0)])
    prize = [part.strip(' ,') for part in prize.split('(1 mark)') if part.strip(' ,')]
    table_rows = [*[point(value, contextNote=s(7, 25, 0)) for value in date],
                  anyn([x.strip() for x in s(7, 26, 1).split('/')], 1, 2, contextNote=s(7, 26, 0) + ' ' + s(7, 27)),
                  *[point(value, contextNote=s(7, 28, 0) + ' ' + s(7, 29)) for value in send],
                  *[point(value, contextNote=s(7, 30, 0)) for value in prize]]
    table = add('1A', 6, table_text, table_rows, 'japanese-5-0', [3], [7], reading=[2, 3],
        figure=crop('ja-2022-hl-1a-6', 3, [.075, .68, .96, .925], table_text))
    # Preserve the four separately priced printed headings within the single
    # required table, with every scoring row in exactly one display group.
    table['taskGroups'] = [
        {'sourceCardId': table['id'] + '-' + name, 'label': table_rows[start]['contextNote'],
         'marks': 2, 'rowIds': [row['id'] for row in table['rows'][start:end]]}
        for name, start, end in [('date', 0, 2), ('photo', 2, 3), ('send', 3, 5), ('prize', 5, 7)]
    ]
    bought, purpose = cell('scheme', 8, 2, 0).split('(1 mark)', 1)
    purpose = re.sub(r'\(any.*$', '', purpose).strip(' /')
    comprehension('1B', 1, None, [20, 21], [point(bought.strip()), anyn([x.strip() for x in purpose.split('/')], 1)], [8])
    comprehension('1B', 2, 'i', [23], [anyn(options(8, [4, 5], '/'), 3)], [8])
    comprehension('1B', 2, 'ii', [25], [point(s(8, 8), 2)], [8])
    comprehension('1B', 3, None, [27, 28], [anyn(options(8, [10], '/'), 1, 2)], [8])
    question = prompt(7, [1]) + '\n' + '\n'.join(p(7, row) for row in [3, 5, 7])
    description = joined_selector('scheme', 8, [(17, 1), (18, 1)])
    famous = strip_tariff(joined_selector('scheme', 8, [(20, 1), (21, 1)]))
    add('2A', 1, question, [point(s(8, 16), 2, contextNote=s(8, 15)),
        anyn([x.strip() for x in description.split('/')], 2, 2, contextNote=s(8, 17, 0) + ' ' + s(8, 18, 0)),
        anyn([x.strip() for x in famous.split('/')], 2, 2, [2, 1], contextNote=s(8, 20, 0) + ' ' + s(8, 21, 0))],
        'japanese-5-2', [7], [8], reading=[6, 7], figure=crop('ja-2022-hl-2a-1', 7, [.09, .05, .9, .234], question))
    for roman, qr, answer in [('i', 9, [point(s(8, 25), 2)]), ('ii', 11, [anyn(options(8, [27], '/'), 2)]),
                              ('iii', 13, [point(s(8, 30), 2)]), ('iv', 15, [point(s(8, 32), 2)])]:
        comprehension('2A', 2, roman, [qr], answer, [8])
    comprehension('2A', 3, 'i', [18, 19], [anyn(options(9, [2], '/'), 3)], [9])
    times = cell('scheme', 9, 4, 0).split(' to ')
    comprehension('2A', 3, 'ii', [21, 22], [anyn(times, 2, 2, [2, 1], contextNote=cell('scheme', 9, 4, 1))], [9])
    comprehension('2A', 3, 'iii', [24, 25], [anyn(options(9, [6, 7], '/'), 3)], [9])
    translation = joined_selector('scheme', 9, [(12, 0), (13, 0)])
    halves = [part.strip() for part in translation.split('(2 marks)') if part.strip()]
    add('2A', 4, prompt(7, [27]) + '\n' + ' '.join(p(7, row) for row in [28, 29]), [point(value, 2) for value in halves],
        'japanese-5-3', [7], [9], reading=[6])
    for section, q, pp, qr, prange, sp, sr, arange, region in [
        ('2B', 1, 8, [1, 2], range(4, 10), 9, 15, range(16, 22), [.06, .06, .96, .47]),
        ('2B', 2, 8, [10, 11], range(13, 19), 9, 22, range(23, 29), [.06, .474, .96, .92]),
        ('2C', 1, 9, [1, 2], range(4, 10), 10, 1, range(2, 8), [.06, .06, .96, .44]),
        ('2C', 2, 9, [10, 11], range(13, 19), 10, 8, range(9, 15), [.06, .45, .96, .88]),
    ]:
        instruction = prompt(pp, qr)
        labels = [' '.join(p(pp, row, gi) for gi in range(len(ROWS['paper'][pp - 1][row])) if not re.fullmatch(r'_+', p(pp, row, gi))) for row in prange]
        answers = []
        for row in arange:
            answer = s(sp, row, 0 if sp == 10 and row in [4, 9, 11, 13] else 1)
            answers.append(re.sub(r'^\([ivx]+\)\s*', '', answer))
        groups = [{'id': f'item-{i}', 'label': label, 'rows': [{'id': 'answer', 'text': answer, 'marks': 1}]} for i, (label, answer) in enumerate(zip(labels, answers), 1)]
        question = instruction + '\n' + p(pp, qr[-1] + 1) + '\n' + '\n'.join(labels)
        add(section, q, question, [], 'japanese-5-4' if section == '2B' else 'japanese-5-5', [pp], [sp], total=5, reading=[pp],
            figure=crop(f'ja-2022-hl-{section.lower()}-{q}', pp, region, instruction),
            rubric={'system': 'language-points', 'count': 5, 'groups': groups, 'taskRequirements': [instruction], 'markingGuideNote': cell('scheme', sp, sr)})
    comprehension('3A', 1, None, [1, 2], [anyn(options(10, [18, 19], '/'), 3)], [10])
    comprehension('3A', 2, None, [5], [anyn(options(10, [22, 23], '/'), 2)], [10])
    comprehension('3A', 3, None, [8, 9], [anyn(options(10, [25, 26, 27], '/'), 2)], [10])
    bath, reasons = cell('scheme', 10, 30).split('(1 mark)', 1)
    comprehension('3A', 4, None, [12, 13], [point(bath.strip()), anyn([x.strip() for x in strip_tariff(reasons.strip(' .')).split('/')], 2)], [10])
    maths, reasons = cell('scheme', 10, 33).split('(1 mark)', 1)
    comprehension('3A', 5, None, [16], [point(maths.strip()), anyn([x.strip() for x in reasons.split('/')], 1)], [10])
    for q, qr, answer in [
        (1, 20, [point(s(11, 2))]), (2, 22, [point(s(11, 4))]),
        (3, 24, [point(x.strip(' 、')) for x in joined_selector('scheme', 11, [(6, 0), (7, 0)]).split('(1 mark)') if x.strip(' 、')]),
        (4, 26, [point(x.strip()) for x in re.split(r'\(1\s+mark\)', joined_selector('scheme', 11, [(9, 0), (10, 0)])) if x.strip()]),
    ]:
        card = comprehension('3B', q, None, [qr], answer, [11])
        card['rows'][0]['contextNote'] = 'The scheme heading says 8 marks, while its explicit row tariffs are 1 + 1 + 2 + 2 = 6. Those local tariffs reconcile the printed Q3 total 38 and reading total 120; this task retains its published row allocation.'
    instruction = prompt(12, [1, 2, 3])
    labels = [p(12, row) for row in range(6, 12)]
    answers = []
    for row in range(12, 18):
        text = cell('scheme', 11, row)
        text = re.sub(r'^\([ivx]+\)\s*', '', text)
        reading, meaning = text.split('1 mark', 1)
        answers.append((reading.strip(), meaning.removesuffix('1 mark').strip()))
    groups = [{'id': f'item-{i}', 'label': label, 'rows': [{'id': 'reading', 'text': a, 'marks': 1}, {'id': 'meaning', 'text': b, 'marks': 1}]} for i, (label, (a, b)) in enumerate(zip(labels, answers), 1)]
    question = instruction + '\n' + p(12, 5) + '\n' + '\n'.join(labels)
    add('3C', None, question, [], 'japanese-5-4', [12], [11], total=10, reading=[12],
        figure=crop('ja-2022-hl-3c', 12, [.06, .06, .98, .417], instruction),
        rubric={'system': 'language-points', 'count': 5, 'groups': groups, 'taskRequirements': [instruction], 'markingGuideNote': cell('scheme', 11, 11)})
    instruction = prompt(12, [13, 14, 15])
    groups = []
    for index, sr in enumerate(range(19, 26)):
        label = p(12, 16 + index)
        text = re.sub(r'^\([ivx]+\)\s*', '', cell('scheme', 11, sr))
        answers = [x.strip() for x in text.split('1 mark') if x.strip()]
        for blank, answer in enumerate(answers, 1):
            groups.append({'id': f'sentence-{index + 1}-blank-{blank}', 'label': label + f' — blank {blank}', 'rows': [{'id': 'answer', 'text': answer, 'marks': 1}]})
    assert len(groups) == 12
    question = instruction + '\n' + '\n'.join(p(12, row) for row in range(16, 23))
    add('3D', None, question, [], 'japanese-5-5', [12], [11], total=10, reading=[12],
        figure=crop('ja-2022-hl-3d', 12, [.06, .42, .98, .91], instruction),
        rubric={'system': 'language-points', 'count': 10, 'groups': groups, 'taskRequirements': [instruction], 'markingGuideNote': cell('scheme', 11, 18)})

def steps(maximum):
    return list(range(maximum + 1))


def writing():
    guidance = [join_cells('scheme', 14, range(first, last), 170) for first, last in [(16, 24), (24, 31), (31, 38)]]
    bands = [{'label': f'{lo}–{hi}', 'marks': list(range(lo, hi + 1)), 'guidance': [text]} for (lo, hi), text in zip([(0, 6), (7, 17), (18, 25)], guidance)]
    reduced = [{'label': f'{lo}–{hi}', 'marks': list(range(lo, hi + 1)), 'guidance': [text]} for (lo, hi), text in zip([(0, 4), (5, 13), (14, 19)], guidance)]
    rule = joined_selector('scheme', 14, [(row, None) for row in range(9, 13)])
    exam_choice = english(p(14, 0))
    for q, pp, sp in [(4, 14, 12), (5, 16, 13)]:
        if q == 4:
            instruction = prompt(14, [2, 3])
            question = exam_choice + '\n' + instruction + '\n' + '\n'.join([
                '(a) ' + prompt(14, [4, 5, 6, 7]), p(14, 8), p(14, 9), english(p(14, 10)),
                '(b) ' + prompt(14, [11, 12, 13]), p(14, 14), p(14, 15), english(p(14, 16)),
                '(c) ' + prompt(14, [17, 18, 19, 20]), p(14, 21), p(14, 22)])
            allocation = joined_selector('scheme', 12, [(row, None) for row in range(17, 21)])
            criteria = [{'id': f'point-{i}', 'label': f'({i})', 'maxMarks': 11, 'permittedMarks': steps(11), 'guidance': [s(12, 17)]} for i in ['i', 'ii']]
            criteria += [{'id': name, 'label': label, 'maxMarks': 1, 'permittedMarks': [0, 1], 'guidance': [allocation]} for name, label in [('opening', 'Opening'), ('closing', 'Closing'), ('discretionary', 'Discretionary mark in (i) or (ii)')]]
            guide = 'Assess the one option you answered. The same C25 / E25 grid applies to all three prompts. The examination requires either Q4 or Q5, not both.'
        else:
            instruction = prompt(16, [1, 2, 3, 4])
            question = exam_choice + '\n' + instruction + '\n' + '\n'.join(p(16, row) for row in range(5, 15))
            headings = [cell('scheme', 13, row) for row in range(10, 18)]
            allocation = joined_selector('scheme', 13, [(row, None) for row in range(4, 8)])
            criteria = []
            for i in range(1, 5):
                criteria += [
                    {'id': f'heading-{i}', 'label': f'Chosen heading {i}', 'maxMarks': 5, 'permittedMarks': steps(5), 'guidance': [s(13, 4)] + headings},
                    {'id': f'heading-{i}-discretionary', 'label': f'Discretionary mark for chosen heading {i}', 'maxMarks': 1, 'permittedMarks': [0, 1], 'guidance': [allocation]},
                ]
            criteria.append({'id': 'opening-or-closing', 'label': 'Suitable opening or closing', 'maxMarks': 1, 'permittedMarks': [0, 1], 'guidance': [allocation]})
            guide = 'Assess four different paper headings once each: content 5 and discretionary 1 per selected heading, plus 1 for a suitable opening or closing. The scheme lists the same headings in a different order (weather last); keep the paper numbering. The examination requires either Q4 or Q5, not both.'
        content_ids = [criterion['id'] for criterion in criteria]
        criteria.append({'id': 'expression', 'label': s(sp, 21 if q == 4 else 8), 'maxMarks': 25, 'permittedMarks': steps(25),
            'guidance': [s(14, 38)], 'bands': bands,
            'limits': [{'id': 'lower-e', 'maxMarks': 19, 'when': {'any': [{'criterionIds': content_ids, 'atMost': 13}, {'length': 'characters', 'below': 150}]},
                        'bands': reduced, 'guidance': [rule]}]})
        add(str(q), None, question, [], 'japanese-5-7', [pp], [sp, 14], total=50, reading=[pp],
            figure=crop(f'ja-2022-hl-{q}', pp, [.045, .015, .97, .92], question),
            rubric={'system': 'language-writing', 'taskRequirements': [exam_choice, instruction], 'criteria': criteria, 'markingGuideNote': guide})


def listening():
    def aq(page, rows):
        text = join_cells('aural', page, rows, 290)
        return re.sub(r'^(?:\d+\.\s*)?(?:\([ivx]+\)\s*)?(?:[a-b]\.\s*)?', '', text).strip()

    def listen(part, q, suffix, question_rows, rows, question=None):
        pp, sp = {'A': (2, 3), 'B': (3, 4), 'C': (4, 5), 'D': (5, 5 if q == 1 and suffix in ['i', 'ii'] else 6)}[part]
        card = add('L' + part, q, question or aq(pp, question_rows), rows,
                   {'A': 'japanese-6-1', 'B': 'japanese-6-2', 'C': 'japanese-6-0', 'D': 'japanese-6-0'}[part], [pp], [sp], suffix or '')
        card['sourceMaterial'] = source([pp], 'source-question', 'aural')
        card['stem'] = join_cells('aural', pp, [1, 2], 290)
        if part in 'BCD':
            context = {'B': {1: 3, 2: 28}, 'C': {1: 3, 2: 10, 3: 21}, 'D': {1: 3, 2: 20}}[part][q]
            card['stem'] += '\n' + join_cells('aural', pp, [context], 290)
        if suffix and re.fullmatch(r'[a-b]-[ivx]+', suffix):
            letter, roman = suffix.split('-')
            card['questionRef'] = f'2022 HL Section L{part} Q{q}({roman})({letter})'
        return card

    headers = [english(joined_selector('aural', 2, [(11, 0), (12, 0), (13, 0)])),
               english(cell('aural', 2, 11, 1).split('  /')[0]) + ' ' + joined_selector('aural', 2, [(12, 1), (13, 1)]),
               joined_selector('aural', 2, [(12, 2), (13, 2)]),
               english(joined_selector('aural', 2, [(11, 2), (12, 3), (13, 3)]))]
    # The two middle column headings share one extracted row. Both fragments
    # are lifted from that source selector, never retyped.
    middle = cell('aural', 2, 11, 1)
    first, second = middle.split('/', 2)[1:]
    headers[1] = first.strip() + ' ' + joined_selector('aural', 2, [(12, 1), (13, 1)])
    headers[2] = second.strip() + ' ' + joined_selector('aural', 2, [(12, 2), (13, 2)])
    def colparts(parts): return joined_selector('scheme', 3, parts)
    memory1 = colparts([(6, 1), (7, 1), (8, 0), (9, 0), (10, 0)])
    plans1 = colparts([(6, 2), (7, 2), (8, 1), (9, 1), (10, 1)])
    home1 = colparts([(6, 3), (7, 3), (8, 2)])
    split_marks = lambda text: [x.strip(' ,') for x in re.split(r'\(1\s+mark\)', text) if x.strip(' ,')]
    sinead = [anyn([x.strip() for x in memory1.split(',')], 2),
              *[point(x, contextNote=headers[1]) for x in split_marks(plans1)],
              *[point(x, contextNote=headers[2]) for x in split_marks(home1)], point(s(3, 6, 4), contextNote=headers[3])]
    sinead[0]['contextNote'] = headers[0]
    memory2 = [s(3, 14, 1), s(3, 15, 1).removesuffix('/'), s(3, 16, 0)]
    plans2 = colparts([(14, 2), (15, 2), (16, 1), (17, 1), (18, 1), (19, 0)])
    home2 = colparts([(14, 3), (15, 3)])
    career2 = colparts([(14, 4), (15, 4)])
    joe = [anyn(memory2, 2, contextNote=headers[0]),
           anyn([x.strip() for x in plans2.split('/')], 2, contextNote=headers[1]),
           *[point(x, contextNote=headers[2]) for x in split_marks(home2)],
           anyn([x.strip() for x in career2.split('/')], 1, contextNote=headers[3])]
    memory3 = cell('scheme', 3, 24, 1) + ' ' + cell('scheme', 3, 25, 0).removeprefix('Andrea ') + ' ' + colparts([(26, 0), (27, 0), (28, 0), (29, 0)])
    plans3 = colparts([(24, 2), (25, 1), (26, 1), (27, 1)])
    career3 = colparts([(24, 4), (25, 2), (26, 2)])
    andrea = [anyn([x.strip() for x in memory3.split(',')], 2, contextNote=headers[0]),
              *[point(x, contextNote=headers[1]) for x in split_marks(plans3)], point(s(3, 24, 3), contextNote=headers[2]),
              *[point(x, contextNote=headers[3]) for x in split_marks(career3)]]
    table_figure = crop('ja-2022-hl-la-table', 2, [.075, .17, .96, .79], cell('aural', 2, 5), 'aural')
    for q, rows in enumerate([sinead, joe, andrea], 1):
        question = cell('aural', 2, 5) + '\n' + cell('aural', 2, 13 + 2 * q) + '\n' + '\n'.join(headers)
        card = listen('A', q, None, [], rows, question)
        card['questionFigureKey'] = table_figure
    listen('B', 1, 'i', [5], [anyn(options(4, [3, 4], ', '), 3)])
    listen('B', 1, 'ii', [11], [point(s(4, 7))])
    listen('B', 1, 'iii', [14, 15], [anyn(options(4, [9], '/'), 3)])
    listen('B', 1, 'iv', [21], [anyn(options(4, [11], '/'), 2, 2, [2, 1])])
    phone = listen('B', 1, 'v', [25], [point(s(4, 14), 2, contextNote='The complete phone number earns 2 marks. No separate per-digit tariff is published.')])
    phone['questionFigureKey'] = crop('ja-2022-hl-lb-1-v', 3, [.55, .56, .96, .621], phone['questionText'], 'aural')
    days = []
    for row in [16, 18]:
        text = strip_tariff(re.sub(r'^\(i\)\s*', '', cell('scheme', 4, row, 0)))
        day, details = text.split(':', 1)
        days.append(anyn([x.strip() for x in details.split(',')], 2, contextNote=day))
    listen('B', 2, 'i', [29, 31, 32], days)
    listen('B', 2, 'ii', [34, 35], [anyn(options(4, [20], '/'), 1, 2)])
    listen('B', 2, 'iii', [37], [anyn(options(4, [22], '/'), 1, 2)])
    for q, roman, qr, sr in [(1, 'i', [4], 3), (2, 'i', [11], 9), (2, 'iv', [17, 18], 15), (3, 'iii', [32], 22)]:
        answers = split_marks(cell('scheme', 5, sr, 0))
        listen('C', q, roman, qr, [point(value) for value in answers])
    listen('C', 1, 'ii', [6], [anyn(options(5, [5], '/'), 3)])
    listen('C', 2, 'ii', [13], [point(s(5, 11), 2)])
    listen('C', 2, 'iii', [15], [point(s(5, 13), 2)])
    teacher = cell('scheme', 5, 18, 0)
    listen('C', 3, 'i', [23, 25], [{'kind': 'criterion', 'verbatim': teacher, 'marks': 2, 'permittedMarks': [0, 1, 2],
                                 'contextNote': 'Teacher alone earns 1 mark; the named teacher earns 2. These are alternative totals for one response.'}])
    listen('C', 3, 'ii', [28], [anyn(options(5, [20], '/'), 1, 2)])
    birthday = [x.strip() for x in cell('scheme', 5, 26, 0).split('(1 mark)') if x.strip()]
    listen('D', 1, 'i', [4], [point(x) for x in birthday])
    ingredients = joined_selector('scheme', 5, [(28, 0), (29, 0)])
    listen('D', 1, 'ii', [6, 7], [{'kind': 'criterion', 'verbatim': ingredients, 'marks': 3, 'permittedMarks': [0, 1, 2, 3],
        'contextNote': 'Award 1 for each accepted detail, up to 3. At most two of meat, vegetables and butter count; three ingredient examples alone therefore earn at most 2.'}])
    listen('D', 1, 'a-iii', [11, 12], [point(s(6, 2))])
    listen('D', 1, 'b-iii', [14, 15], [anyn(options(6, [4], '/'), 2, 2, [2, 1])])
    listen('D', 1, 'iv', [18], [point(s(6, 7), 2)])
    food = [point(s(6, 9, 1)), point(s(6, 10).removesuffix(')'))]
    listen('D', 2, 'i', [21], food)
    dessert = [point(s(6, 12, 1)), point(clean_tariff(s(6, 13, 1)))]
    listen('D', 2, 'ii', [22], dessert)
    listen('D', 2, 'iii', [23], [anyn([x.strip() for x in s(6, 14).split(',')], 2, 2, [2, 1])])
    listen('D', 2, 'iv', [24], [point(s(6, 16, 1), 2)])


def consolidations(census):
    records = []
    romans = ['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii']
    for suffix, count, pp, pr, sp, sr, reason in [
        ('1a-1', 6, 3, [1, 2], 7, 3, 'One required six-cell matching task at1mark each; keep all original links and questions together.'),
        ('2b-1', 6, 8, [1, 2], 9, 15, 'One complete printed any-five-of-six meaning pool,1mark per chosen answer.'),
        ('2b-2', 6, 8, [10, 11], 9, 22, 'One complete printed any-five-of-six reading pool,1mark per chosen answer.'),
        ('2c-1', 6, 9, [1, 2], 10, 1, 'One complete printed any-five-of-six plain-form pool,1mark per chosen answer.'),
        ('2c-2', 6, 9, [10, 11], 10, 8, 'One complete printed any-five-of-six conjugation pool,1mark per chosen answer.'),
        ('3c', 6, 12, [1, 2, 3], 11, 11, 'One complete any-five-of-six paired reading1/meaning1 pool.'),
        ('3d', 7, 12, [13, 14, 15], 11, 18, 'One any-ten-of-twelve-blank pool across seven numbered sentences;1mark per chosen blank.'),
    ]:
        canonical = 'ja-2022-hl-' + suffix
        task = next(task for task in census['tasks'] if canonical == 'ja-2022-hl-' + '-'.join(str(part).lower() for part in task['key'] if part is not None))
        records.append({'canonicalId': canonical, 'legacyIds': [canonical + '-' + roman for roman in romans[:count]],
                        'taskKey': task['key'], 'marks': task['marks'], 'reason': reason,
                        'paperEvidence': {'page': pp, 'text': joined_selector('paper', pp, [(row, None) for row in pr])},
                        'schemeEvidence': {'page': sp, 'text': cell('scheme', sp, sr)}})
    return records


def build():
    reading()
    writing()
    listening()
    census = json.loads((Path(__file__).parent / 'reviews/japanese-2022-hl-census.json').read_text())
    expected = {'ja-2022-hl-' + '-'.join(str(part).lower() for part in task['key'] if part is not None): task for task in census['tasks']}
    assert set(expected) == {card['id'] for card in CARDS}
    for card in CARDS:
        task = expected[card['id']]
        assert card['totalMarks'] == task['marks'], (card['id'], card['totalMarks'], task['marks'])
        assert card['sourceEvidence']['paperPages'] == task['paperPages']
        assert card['sourceEvidence']['schemePages'] == task['schemePages']
        if 'paperRef' in task:
            assert card['questionRef'] == task['paperRef']
    assert len(CARDS) == 66
    assert sum(card['totalMarks'] for card in CARDS) == 300
    return {'subjectId': 'japanese', 'sitting': '2022-hl', 'reviewedAt': '2026-11-09',
            'sources': [{'document': name, 'path': str(path.relative_to(ROOT)), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'pagesReviewed': list(range(1, len(DOCS[name]) + 1))} for name, path in [('paper', PAPER), ('aural', AURAL), ('scheme', SCHEME)]],
            'cards': CARDS, 'selectors': EVIDENCE, 'status': 'source-reviewed-browser-qa-pending',
            'choiceAnalysis': census['choiceBoundaries'], 'consolidations': consolidations(census)}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    result = build()
    if args.write:
        (ROOT / 'scripts/markbank/authoring/reviews/japanese-2022-hl.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
        manifest = ROOT / 'components/MarkBank/figures-japanese.json'
        previous = json.loads(manifest.read_text())
        previous.update(FIGURES)
        manifest.write_text(json.dumps(previous, ensure_ascii=False, indent=2) + '\n')
        scheme_md = SCHEME.with_suffix('.md')
        marker = '\n## Audited original table columns — 2022 HL pages 3 and 8\n'
        original = scheme_md.read_text().split(marker)[0]
        columns = []
        for page, bounds in [(3, [(120, 224), (225, 329), (330, 456), (456, 595)]), (8, [(185, 595)])]:
            for x0, x1 in bounds:
                columns.append(DOCS['scheme'][page - 1].get_text(clip=fitz.Rect(x0, 0, x1, 780), sort=True))
        scheme_md.write_text(original + marker + '\n'.join(columns))
    print(json.dumps({'cards': len(CARDS), 'marks': sum(card['totalMarks'] for card in CARDS), 'figures': len(FIGURES)}, indent=2))
