#!/usr/bin/env python3
"""2016 Higher Japanese, independently reviewed against all original pages.

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
PAPER = ROOT / 'examiner-reports/japanese/papers/2016-hl-000-paper.pdf'
AURAL = ROOT / 'examiner-reports/japanese/papers/2016-hl-A00-paper.pdf'
SCHEME = ROOT / 'examiner-reports/japanese/schemes/2016-hl.pdf'
PINNED_SOURCES = {
    PAPER: '18c4e6e4695bc5e2db4ea074e674927cdde6918ba95a3995e6b6227bfa908523',
    AURAL: '37e7f13202e852e6ab0209ad8cf4d1bb02a6c356477333355d770c9e76defb52',
    SCHEME: '9b8fda5225ae55e5dfb9682a76defaab104d836b7e8d10c9cab8ab928bcdab06',
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
    return {'kind': kind, 'label': '2016 Japanese Higher Level', 'title': 'Original examination material',
            'pages': pages, 'attribution': '© State Examinations Commission.',
            **({'presentationNote': FURIGANA_NOTE} if component == 'paper' else {}),
            '_component': component}


def add(section, q, question, rows, topic, paper_pages, scheme_pages, suffix='', rubric=None, total=None, reading=None, figure=None):
    cid = f'ja-2016-hl-{section.lower()}' + (f'-{q}' if q is not None else '') + (f'-{suffix}' if suffix else '')
    ref = f'2016 HL Section {section}' + (f' Q{q}' if q is not None else '')
    if suffix:
        ref += (' Q' if q is None else '') + ''.join(f'({part})' for part in suffix.split('-'))
    listening = section.startswith('L')
    card = {'id': cid, 'source': 'sec', 'subjectId': 'japanese', 'specVersion': 'lc-japanese-syllabus',
            'kind': 'rubric' if rubric else 'question', 'level': 'higher', 'year': 2016,
            'section': section[1:] if listening else section[0] if section[0] in '1234' else 'Q5',
            'topicId': topic, 'conceptId': concept_for(question, cid), 'questionRef': ref,
            'questionText': question, 'totalMarks': total if total is not None else row_total(rows),
            'qa': {'gates': ['verbatim', 'tariff', 'figure'], 'humanReviewedBy': 'agent-verified', 'humanReviewedAt': '2026-11-09'},
            'sourceEvidence': {'component': 'aural' if listening else 'paper', 'paperPages': paper_pages, 'schemePages': scheme_pages},
            'schemeCitation': 'Marking points quoted from the SEC marking scheme, Japanese 2016 Higher Level — © State Examinations Commission.'}
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
        language = (7, 22, 'Japanese')
    if section == '2A' and q == 2:
        page, row = (8, 18)
        card['extraneousMaterialRule'] = {'multiplier': 0.5, 'sourceText': cell('scheme', page, row), 'schemePages': [page]}
        card['sourceEvidence']['generalSchemePages'] = [page]
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
    instruction_row = (8 if q == 2 else 15) if section == '2A' else {'1A': 0, '1B': 26, '3A': 0, '3B': 22}[section]
    card['stem'] = english(p(page, instruction_row))
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
    instruction = prompt(3, [1])
    labels = [english(p(3, row, 1 if row == 3 else 0)) for row in range(3, 9)]
    add('1A', 1, instruction + '\n' + '\n'.join(labels), [], 'japanese-5-0', [3], [7], total=6, reading=[2],
        rubric=complete_pool(6, labels, [s(7, row, 1) for row in range(4, 10)], instruction, cell('scheme', 7, 3)))
    comprehension('1A', 2, None, [9], [point(clean_tariff(s(7, 11, gi))) for gi in [0, 1]], [7])
    full = options(7, [13], '/')
    partial = s(7, 14).removeprefix('(').split(',')[0].split('/')
    assert len(full) == 4 and len(partial) == 3
    groups = [{'id': f'instrument-{i}', 'label': answer, 'answerCount': 1,
               'rows': [{'id': 'full', 'text': answer, 'marks': 2}] +
                       ([{'id': 'partial', 'text': partial[i - 1].strip(), 'marks': 1}] if i else [])}
              for i, answer in enumerate(full)]
    question = prompt(3, [11, 12])
    add('1A', 3, question, [], 'japanese-5-0', [3], [7], 'i', total=4, reading=[2],
        rubric={'system': 'language-points', 'count': 2, 'taskRequirements': [question], 'groups': groups,
                'markingGuideNote': cell('scheme', 7, 13) + '\n' + cell('scheme', 7, 14) + '\nEach full instrument and its named partial occupy one response slot; count at most two instruments.'})
    comprehension('1A', 3, 'ii', [14], [anyn(options(7, [16], '/'), 2, 2)], [7])
    for roman, qr, sr, key in [('i', 17, 18, 'bath'), ('ii', 18, 19, 'electric')]:
        raw = s(7, sr).split(key, 1)
        card = comprehension('1A', 4, roman, [16], [point(answer) for answer in split_marks(key + raw[1])], [7])
        card['questionText'] += '\n' + p(3, qr, 1).split('_', 1)[0].strip()
    card = comprehension('1A', 5, None, [19], [point(answer) for answer in split_marks(s(7, 21))], [7])
    card['rows'][0]['contextNote'] = 'The general paper instruction says questions 1–4, but this question 5 is explicitly printed and separately marked in the scheme.'
    for q, qr, sr in [(1, [27, 28], 24), (2, [30], 26), (3, [32, 33], 28)]:
        rows = [point(answer) for answer in split_marks(s(7, sr))] if q < 3 else [point(s(7, sr), 2)]
        comprehension('1B', q, None, qr, rows, [7])
    comprehension('1B', 4, None, [35, 36], [anyn(s(7, 30).split('/'), 2, contextNote=cell('scheme', 7, 31))], [7])
    instruction = prompt(7, [1])
    headers = [p(7, 3, 0) + ' ' + p(7, 4), p(7, 3, 1), p(7, 3, 2)]
    names = [p(7, row) for row in [5, 6, 7]]
    values = [
        [(1, point(selected(8, [(5, 0), (7, 0)]))),
         (2, anyn(selected(8, [(5, 1), (7, 1), (8, 1)]).split('/'), 2))],
        [(0, point(s(8, 11, 0))), (1, point(s(8, 11, 1))),
         (2, anyn(selected(8, [(11, 2), (12, 2)]).split('/'), 2))],
        [(0, point(selected(8, [(15, 0), (16, 0)]))), (1, point(s(8, 15, 1))),
         (2, anyn(selected(8, [(15, 2), (16, 2)]).split('/'), 2))],
    ]
    rows, task_groups = [], []
    for person, cells in enumerate(values):
        for col, row in cells:
            label = names[person] + ' — ' + headers[col]
            row['contextNote'] = label
            start = len(rows); rows.append(row)
            task_groups.append((f'person-{person+1}-cell-{col+1}', label, start, len(rows)))
    table = add('2A', 1, instruction + '\n' + '\n'.join(headers + names), rows, 'japanese-5-2', [7], [8], reading=[6, 7],
        figure=crop('ja-2016-hl-2a-1', 7, [.06, .035, .97, .28], instruction))
    group_rows(table, task_groups)
    comprehension('2A', 2, 'i', [9], [point(answer) for answer in split_marks(s(8, 20))], [8])
    full, partial = s(8, 22).split(' (', 1)
    comprehension('2A', 2, 'ii', [11], [point(full, 2, kind='criterion', permittedMarks=[0, 1, 2], contextNote='(' + partial)], [8])
    comprehension('2A', 2, 'iii', [13], [point(s(8, 24), 2)], [8])
    comprehension('2A', 3, 'i', [16], [anyn(options(8, [27], '/'), 2)], [8])
    comprehension('2A', 3, 'ii', [18, 19], [anyn(options(8, [29, 30], '/'), 2, 1, [2, 1], contextNote=cell('scheme', 8, 31))], [8])
    comprehension('2A', 3, 'iii', [21, 22, 23], [anyn(options(8, [34, 35, 36, 37], '/'), 1, 2)], [8])
    comprehension('2A', 3, 'iv', [26], [point(answer) for answer in split_marks(s(8, 39))], [8])
    translation_rows = []
    for route, parts in [('A', [(2, 0), (3, 0)]), ('B', [(5, 0), (6, 0)])]:
        for answer in split_marks(selected(9, parts), 2):
            translation_rows.append(point(answer, 2, route=route))
    add('2A', 4, prompt(7, [28]) + '\n' + p(7, 29) + ' ' + p(7, 30), translation_rows, 'japanese-5-3', [7], [9], reading=[6])
    instruction = p(8, 3)
    labels = [p(8, row).split('________')[0].strip() for row in range(5, 10)]
    meanings = [s(9, 8, 3), s(9, 9, 3), clean_tariff(s(9, 10, 3)), s(9, 11, 3), clean_tariff(selected(9, [(12, 3), (13, 0)]))]
    pairs = [{'id': f'item-{i+1}', 'label': label, 'rows': [
        {'id': 'reading', 'text': s(9, i+8, 1), 'marks': 1}, {'id': 'meaning', 'text': meanings[i], 'marks': 1}]}
        for i, label in enumerate(labels)]
    add('2B', None, instruction + '\n' + '\n'.join(labels), [], 'japanese-5-4', [8], [9], total=10, reading=[8],
        figure=crop('ja-2016-hl-2b', 8, [.06, .025, .97, .355], instruction),
        rubric={'system': 'language-points', 'count': 5, 'taskRequirements': [instruction], 'groups': pairs, 'markingGuideNote': cell('scheme', 9, 7)})
    instruction = p(8, 13)
    groups = []
    for index, sr in enumerate(range(15, 22)):
        for blank, gi in enumerate([1, 3] if index < 3 else [1], 1):
            answer = clean_tariff(s(9, sr, gi))
            groups.append({'id': f'sentence-{index+1}-blank-{blank}', 'label': p(8, 14+index) + f' — blank {blank}',
                           'rows': [{'id': 'answer', 'text': answer, 'marks': 1}]})
    add('2C', None, instruction + '\n' + '\n'.join(p(8, row) for row in range(14, 21)), [], 'japanese-5-5', [8], [9], total=10, reading=[8],
        figure=crop('ja-2016-hl-2c', 8, [.06, .36, .97, .92], instruction),
        rubric={'system': 'language-points', 'count': 10, 'taskRequirements': [instruction], 'groups': groups, 'markingGuideNote': cell('scheme', 9, 14)})
    family = []
    for sr in range(25, 30):
        row = s(9, sr)
        name, answers = row.split(':', 1) if ':' in row else ('', row)
        for answer in answers.split('/'):
            text = answer.strip()
            family.append({'id': f'detail-{len(family)+1}', 'label': name + ': ' + text if name else text,
                           'rows': [{'id': 'answer', 'text': text, 'marks': 1}]})
    question = prompt(11, [1, 2])
    add('3A', 1, question, [], 'japanese-5-1', [11], [9], total=3, reading=[10],
        rubric={'system': 'language-points', 'count': 3, 'groups': family, 'taskRequirements': [question],
                'markingGuideNote': selected(9, [(r, None) for r in range(25, 31)])})
    raw = selected(9, [(32, 0), (33, 0), (34, 0)])
    first, second = raw.split('(3 marks)', 1)
    fixed, contexts = second.strip(' /').split('(2 marks)', 1)
    contexts = clean_tariff(contexts).strip()
    rows = [point(first, 3, route='A'), point(fixed.strip(), 2, route='B'), anyn(contexts.split('/'), 1, route='B')]
    comprehension('3A', 2, None, [6, 7], rows, [9])
    comprehension('3A', 3, 'i', [10, 11], [anyn(options(9, [36, 37], '/'), 3)], [9])
    comprehension('3A', 3, 'ii', [14, 15], [anyn(s(9, 39).split('/'), 1, 2, contextNote=cell('scheme', 9, 40))], [9])
    comprehension('3A', 4, None, [17, 18, 19], [anyn(options(10, [2, 3, 4], '/'), 2, 1, [2, 1])], [10])
    comprehension('3B', 1, None, [23], [point(s(10, 7), 2)], [10])
    comprehension('3B', 2, None, [25], [point(answer, 2) for answer in split_marks(s(10, 9), 2)], [10])
    for section, q, pp, instruction_rows, labels_range, answers_range, region in [
        ('3C', 1, 12, [2], range(4, 9), range(12, 17), [.06,.035,.97,.36]),
        ('3C', 2, 12, [10], range(12, 17), range(18, 23), [.06,.375,.97,.70]),
        ('3D', 1, 13, [1, 2], range(5, 10), range(25, 30), [.06,.035,.97,.48]),
        ('3D', 2, 13, [10], range(12, 17), range(31, 36), [.06,.48,.97,.91]),
    ]:
        instruction = prompt(pp, instruction_rows)
        labels = [p(pp, row).strip() for row in labels_range]
        answers = [re.sub(r'^\([ivx]+\)\s*', '', s(10, row)) for row in answers_range]
        add(section, q, instruction + '\n' + '\n'.join(labels), [], 'japanese-5-4' if section == '3C' else 'japanese-5-5', [pp], [10], total=5, reading=[pp],
            figure=crop(f'ja-2016-hl-{section.lower()}-{q}', pp, region, instruction),
            rubric=complete_pool(5, labels, answers, instruction, cell('scheme', 10, answers_range.start-1)))


def steps(maximum):
    return list(range(maximum + 1))


def writing():
    for q, pp, sp, maximum, lower, threshold, length in [(4,14,12,20,15,9,150), (5,16,14,30,20,15,200)]:
        guidance = [join_cells('scheme', sp, range(first,last), 150) for first,last in [(16,23),(23,30),(30,37)]]
        if q == 5:
            # Highest-band first descriptor shares one text group with the printed score.
            guidance[2] = re.sub(r'^21\s*-\s*30\s*', '', cell('scheme', sp, 30, 1)) + ' ' + join_cells('scheme', sp, range(31,37), 167)
        normal = [(0,5),(6,14),(15,20)] if q == 4 else [(0,7),(8,20),(21,30)]
        low = [(0,3),(4,10),(11,15)] if q == 4 else [(0,4),(5,12),(13,20)]
        bands = [{'label':f'{lo}–{hi}','marks':list(range(lo,hi+1)),'guidance':[text]} for (lo,hi),text in zip(normal,guidance)]
        reduced = [{'label':f'{lo}–{hi}','marks':list(range(lo,hi+1)),'guidance':[text]} for (lo,hi),text in zip(low,guidance)]
        allocation = selected(sp-1, [(row,None) for row in (range(9,14) if q == 4 else range(11,16))])
        if q == 4:
            instruction = p(14,2)
            question = instruction + '\n(a) ' + p(14,4) + '\n' + '\n'.join(p(14,r) for r in [5,6]) + '\n' + english(p(14,7)) + '\n(b) ' + p(14,9) + '\n' + '\n'.join(p(14,r) for r in [10,11])
            criteria = [{'id':f'point-{i}','label':f'Point {i}','maxMarks':8,'permittedMarks':steps(8),'guidance':[allocation]} for i in [1,2]]
            criteria += [{'id':f'discretionary-{i}','label':f'Discretionary point {i}','maxMarks':1,'permittedMarks':[0,1],'guidance':[allocation]} for i in [1,2]]
            guide = 'Assess the one diary option you answered. Two content responses earn up to 8 each, with one discretionary mark under each point, opening 1 and closing 1. Lower E applies when content is below 10 (not at 10) or the response is shorter than 150 characters.'
        else:
            instruction = ' '.join(p(16,r) for r in [4,5,6])
            headings = []
            for rows in [[7,8],[9],[10],[11,12],[13],[14,15,16]]:
                first = rows[0]
                jp = p(16,first,0) + ' ' + p(16,first,1)
                en = english(' '.join(p(16,r,2 if r == first else 0) for r in rows))
                headings.append(jp + ' — ' + en)
            question = instruction + '\n' + '\n'.join(headings)
            criteria = [{'id':f'heading-{i}','label':f'Chosen heading {i}','maxMarks':6,'permittedMarks':steps(6),'guidance':[allocation, selected(13, [(r,None) for r in range(4,11)])]} for i in range(1,5)]
            criteria += [{'id':f'discretionary-{i}','label':f'Discretionary heading {i}','maxMarks':1,'permittedMarks':[0,1],'guidance':[allocation]} for i in range(1,5)]
            guide = 'Assess four different headings once each, up to 6 marks each, plus one discretionary mark under each chosen heading, opening 1 and closing 1. Use the printed 30-mark expression scale and conditional 20-mark scale.'
        criteria += [{'id':label.lower(),'label':label,'maxMarks':1,'permittedMarks':[0,1],'guidance':[allocation]} for label in ['Opening','Closing']]
        content_ids = [item['id'] for item in criteria]
        criteria.append({'id':'expression','label':'Expression','maxMarks':maximum,'permittedMarks':steps(maximum),'bands':bands,
                         'guidance':[selected(sp,[(37,None),(38,None)])],
                         'limits':[{'id':'lower-e','maxMarks':lower,'when':{'any':[{'criterionIds':content_ids,'atMost':threshold},{'length':'characters','below':length}]},'bands':reduced,'guidance':[selected(sp,[(r,None) for r in range(9,13)])]}]})
        add(str(q),None,question,[],'japanese-5-7',[pp],[sp-1,sp],total=maximum*2,reading=[pp],
            figure=crop(f'ja-2016-hl-{q}',pp,[.045,.025,.97,.92],question),
            rubric={'system':'language-writing','taskRequirements':[instruction],'criteria':criteria,'markingGuideNote':guide})


def listening():
    def listen(part, q, suffix, qr, rows, question=None, rubric=None, total=None):
        pp = {'A':2,'B':3,'C':4,'D':5}[part]
        sp = {'A':3,'B':4,'C':5,'D':6}[part]
        text = question or re.sub(r'^\([ivx]+\)\s*','',join_cells('aural',pp,qr,300)).strip()
        card = add('L'+part,q,text,rows,{'A':'japanese-6-1','B':'japanese-6-0','C':'japanese-6-2','D':'japanese-6-0'}[part],[pp],[sp],suffix or '',rubric=rubric,total=total)
        card['sourceMaterial'] = source([pp],'source-question','aural')
        card['stem'] = join_cells('aural',pp,range(1,6 if part in 'BD' else 5),300)
        if part in 'BC':
            row = {('B',1):6,('B',2):19,('C',1):6,('C',2):17,('C',3):24}[(part,q)]
            card['stem'] += '\n' + join_cells('aural',pp,[row],300)
        return card
    merged = cell('aural',2,12,0)
    head1, head2 = merged.split('?',1)
    headers = [cell('aural',2,11,0)+' '+head1+'?',cell('aural',2,11,1)+' '+head2.strip(),
               cell('aural',2,11,2)+' '+cell('aural',2,12,1),
               cell('aural',2,11,3)+' '+cell('aural',2,12,2)+' '+cell('aural',2,13)]
    names = [cell('aural',2,r) for r in [14,15,16]]
    mixed = cell('scheme',3,12,0)
    travel, study = mixed.split(' / Study',1)
    action1 = selected(3,[(6,1),(7,0)])
    values = [
        [[point(action1),point(s(3,9,0))],
         [point(clean_tariff(selected(3,[(6,2),(7,1),(8,1)])),2)], [point(s(3,6,3))],
         [point(selected(3,[(6,4),(7,3),(8,2),(9,1)]))]],
        [[point(clean_tariff(travel)),point(s(3,13,0))],
         [anyn(('Study'+study+' '+selected(3,[(13,1),(14,1),(15,0),(16,0)])).split('/'),2)],
         [point(s(3,12,1))], [point(selected(3,[(12,2),(13,3),(14,2),(15,1)]))]],
        [[point(clean_tariff(selected(3,[(20,0),(21,0)])),2)],
         [anyn(selected(3,[(20,1),(21,1),(22,0),(23,0)]).split('/'),2)],
         [point(s(3,20,2))], [point(selected(3,[(20,3),(21,3),(22,1),(23,1)]))]],
    ]
    rows, groups = [], []
    for person,cells in enumerate(values):
        for column,components in enumerate(cells):
            label = names[person]+' — '+headers[column]
            start = len(rows)
            for row in components:
                row['contextNote'] = label
                rows.append(row)
            groups.append((f'person-{person+1}-cell-{column+1}',label,start,len(rows)))
    instruction = cell('aural',2,6,1)
    table = listen('A',None,None,[],rows,instruction+'\n'+'\n'.join(headers+names))
    group_rows(table,groups)
    table['questionFigureKey'] = crop('ja-2016-hl-la',2,[.06,.16,.975,.77],table['questionText'],'aural')
    listen('B',1,'i',[7],[point(answer) for answer in split_marks(s(4,3))])
    listen('B',1,'ii',[10],[point(s(4,5),2)])
    directions = re.split(r'\(\d+ marks?\)',selected(4,[(7,0),(8,0)]))
    listen('B',1,'iii',[12,13],[point(answer.strip(' ,'),marks) for answer,marks in zip(directions,[2,1,1])])
    listen('B',1,'iv',[17],[point(s(4,10))])
    listen('B',2,'i',[20,21],[anyn(options(4,[13],'/'),2,2)])
    choices = re.split(r'\s/\s(?![^()]*\))',s(4,15))
    assert len(choices)==4,choices
    listen('B',2,'ii',[24,25],[anyn(choices,2,1,[2,1],contextNote=cell('scheme',4,16))])
    listen('B',2,'iii',[28],[point(s(4,18),2)])
    opening = re.split(r'\(\d+ marks?\)',s(5,3))
    listen('C',1,'i',[7],[point(answer.strip(),marks) for answer,marks in zip(opening,[1,1,2])])
    listen('C',1,'ii',[10],[point(s(5,5),2)])
    listen('C',1,'iii',[13],[point(answer) for answer in split_marks(s(5,7))])
    phone=listen('C',1,'iv',[15],[point(s(5,9),4,contextNote='The scheme prices the complete number at 4 marks. Six digits are missing in the original grid; no per-digit allocation is printed.')])
    phone['questionFigureKey']=crop('ja-2016-hl-lc-1-iv',4,[.54,.415,.97,.504],phone['questionText'],'aural')
    full = options(5,[12,13],'/')
    assert len(full)==9,full
    groups=[{'id':f'fact-{i+1}','label':answer,'rows':[{'id':'full','text':answer,'marks':2}]} for i,answer in enumerate(full)]
    groups[-1]['answerCount']=1
    partial=cell('scheme',5,14,0).split('(')[1].split('1 mark')[0].strip()
    groups[-1]['rows'].append({'id':'partial','text':partial,'marks':1})
    question=join_cells('aural',4,[18,19],300)
    listen('C',2,None,[],[],question,rubric={'system':'language-points','count':4,'groups':groups,'taskRequirements':[question],
        'markingGuideNote':selected(5,[(12,0),(13,0),(14,0)])+' — The original transcript connects Guinness to the largest-sportswoman fact. On that source-context evidence, its Guinness-only partial and the full fact occupy one detail slot, never 2+1. This association is not an explicit bracket in the printed answer list. Count at most four details.'},total=8)
    selected(17, [(18,0),(19,0)])
    CARDS[-1]['sourceEvidence']['interpretiveSchemePages']=[17]
    weather = []
    for sr in [16,17]:
        weather.append(anyn(options(5,[sr],'/'),2,contextNote=s(5,sr,0)))
        # Options are in the table's second column, not the city-label column.
        weather[-1]['group']['options']=strip_tariff(s(5,sr,1)).split('/')
    card=listen('C',3,None,[],weather,join_cells('aural',4,[24,25,26,27,28],300))
    group_rows(card,[(f'city-{i+1}',s(5,16+i,0),i,i+1) for i in range(2)])
    card['questionFigureKey']=crop('ja-2016-hl-lc-3',4,[.54,.72,.97,.95],card['questionText'],'aural')
    listen('D',None,'i',[6],[point(s(6,2),2)])
    listen('D',None,'ii',[8],[anyn(options(6,[4,5],'/'),2,2)])
    routine = options(6,[7,8],'/')
    assert len(routine)==4,routine
    groups=[{'id':'detail-1','label':routine[0],'rows':[{'id':'full','text':routine[0],'marks':2}]}]
    for i,answer in enumerate(routine[1:],2):
        location,time=answer.rsplit(' in ',1)
        groups.append({'id':f'detail-{i}','label':answer,'rows':[{'id':'location','text':location,'marks':1},{'id':'time','text':time,'marks':1}]})
    question=join_cells('aural',5,[12],300)
    listen('D',None,'iii',[],[],question,rubric={'system':'language-points','count':2,'groups':groups,'taskRequirements':[question],
        'markingGuideNote':selected(6,[(7,0),(8,0)])+' — Choose at most two complete response groups. Location and time are separate one-mark components where both are printed; Studies 10 hours is the separately printed two-mark option.'},total=4)
    listen('D',None,'iv',[15],[point(s(6,11),2)])
    listen('D',None,'v',[18],[point(answer) for answer in split_marks(s(6,13))])
    listen('D',None,'vi',[21],[point(s(6,15),2)])
    groups=[]
    for i,sr in enumerate([17,18,19],1):
        answer=s(6,sr);item,person=answer.split(' for ',1)
        groups.append({'id':f'souvenir-{i}','label':answer,'rows':[{'id':'item','text':item,'marks':1},{'id':'person','text':person,'marks':1}]})
    question=join_cells('aural',5,[25,26],300)
    listen('D',None,'vii',[],[],question,rubric={'system':'language-points','count':2,'groups':groups,'taskRequirements':[question],
        'markingGuideNote':cell('scheme',6,20)+' — Each item/person pair occupies one response slot; choose at most two.'},total=4)


def build():
    reading(); writing(); listening()
    census=json.loads((Path(__file__).parent/'reviews/japanese-2016-hl-census.json').read_text())
    expected={'ja-2016-hl-'+'-'.join(str(part).lower() for part in task['key'] if part is not None):task for task in census['tasks']}
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
    assert len(CARDS)==56
    assert sum(card['totalMarks'] for card in CARDS)==300
    assert sum('answerLanguageRule' in card for card in CARDS)==25
    assert sum('extraneousMaterialRule' in card for card in CARDS)==3
    assert '\ufffd' not in json.dumps([CARDS,EVIDENCE],ensure_ascii=False)
    return {'subjectId':'japanese','sitting':'2016-hl','reviewedAt':'2026-11-09',
        'sources':[{'document':name,'path':str(path.relative_to(ROOT)),'sha256':PINNED_SOURCES[path],'pagesReviewed':list(range(1,len(DOCS[name])+1))} for name,path in [('paper',PAPER),('aural',AURAL),('scheme',SCHEME)]],
        'cards':CARDS,'selectors':EVIDENCE,'status':'source-reviewed-browser-qa-pending','choiceAnalysis':census['choiceBoundaries'],'consolidations':[]}


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--write',action='store_true');args=parser.parse_args()
    result=build()
    if args.write:
        scheme_text=''.join(f'\n## Page {i+1}\n\n'+page.get_text(sort=True) for i,page in enumerate(DOCS['scheme']))
        scheme_text+='\n## Original text with furigana folded at its printed character\n'
        scheme_text+=''.join(f'\n### Physical page {i+1}\n\n'+'\n'.join(' '.join(group[2] for group in row) for row in rows)+'\n' for i,rows in enumerate(ROWS['scheme']))
        for page,x_ranges in [(3,[(78,220),(203,330),(332,410),(414,590)]),(8,[(125,260),(270,375),(375,590)])]:
            scheme_text+=f'\n## Original table columns — physical page {page}\n'
            scheme_text+='\n'.join(DOCS['scheme'][page-1].get_text(clip=fitz.Rect(x0,0,x1,DOCS['scheme'][page-1].rect.height),sort=True) for x0,x1 in x_ranges)
        SCHEME.with_suffix('.md').write_text(scheme_text.rstrip()+'\n')
        (ROOT/'scripts/markbank/authoring/reviews/japanese-2016-hl.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
        manifest=ROOT/'components/MarkBank/figures-japanese.json'; previous=json.loads(manifest.read_text());previous.update(FIGURES)
        manifest.write_text(json.dumps(previous,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'cards':len(CARDS),'marks':sum(card['totalMarks'] for card in CARDS),'figures':len(FIGURES)},indent=2))
