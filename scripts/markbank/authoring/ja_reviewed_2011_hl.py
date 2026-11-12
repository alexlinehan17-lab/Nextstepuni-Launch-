#!/usr/bin/env python3
"""2011 Higher Japanese, independently reviewed against all original pages.

Selectors below are coordinates in ja_text.page_rows, not transcribed answers.
Every question comes from the paper; every answer and tariff wording from the
scheme. Choice pools are kept whole. All original-source selectors and final crops are verified.
"""
import argparse
import hashlib
import json
import os
import re
from pathlib import Path

import fitz
from ja_text import page_rows
from ja_topics import FURIGANA_NOTE, concept_for

ROOT = Path(__file__).resolve().parents[3]
PAPER = ROOT / 'examiner-reports/japanese/papers/2011-hl-000-paper.pdf'
AURAL = ROOT / 'examiner-reports/japanese/papers/2011-hl-A00-paper.pdf'
SCHEME = ROOT / 'examiner-reports/japanese/schemes/2011-hl.pdf'
PINNED_SOURCES = {
    PAPER: 'fea3c8874340bd32e29af2fa5a3ea6900c82d4245be0df89fed00441957877cb',
    AURAL: '791f4689903af58657a32cdef4020201a3c012bc3725f3a20bd3a4996350373d',
    SCHEME: 'b074b5846c2f41ce7a4476795922fd4570334c44536924c8484a4aed02238f81',
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
    return {'kind': kind, 'label': '2011 Japanese Higher Level', 'title': 'Original examination material',
            'pages': pages, 'attribution': '© State Examinations Commission.',
            **({'presentationNote': FURIGANA_NOTE} if component == 'paper' else {}),
            '_component': component}


def add(section, q, question, rows, topic, paper_pages, scheme_pages, suffix='', rubric=None, total=None, reading=None, figure=None):
    cid = f'ja-2011-hl-{section.lower()}' + (f'-{q}' if q is not None else '') + (f'-{suffix}' if suffix else '')
    ref = f'2011 HL Section {section}' + (f' Q{q}' if q is not None else '')
    if suffix:
        ref += (' Q' if q is None else '') + ''.join(f'({part})' for part in suffix.split('-'))
    listening = section.startswith('L')
    card = {'id': cid, 'source': 'sec', 'subjectId': 'japanese', 'specVersion': 'lc-japanese-syllabus',
            'kind': 'rubric' if rubric else 'question', 'level': 'higher', 'year': 2011,
            'section': section[1:] if listening else section[0] if section[0] in '1234' else 'Q5',
            'topicId': topic, 'conceptId': concept_for(question, cid), 'questionRef': ref,
            'questionText': question, 'totalMarks': total if total is not None else row_total(rows),
            'qa': {'gates': ['verbatim', 'tariff', 'figure'], 'humanReviewedBy': 'agent-verified', 'humanReviewedAt': '2026-11-11'},
            'sourceEvidence': {'component': 'aural' if listening else 'paper', 'paperPages': paper_pages, 'schemePages': scheme_pages},
            'schemeCitation': 'Marking points quoted from the SEC marking scheme, Japanese 2011 Higher Level — © State Examinations Commission.'}
    if rubric:
        card['rubric'] = rubric
    else:
        card['tariffModel'] = {'kind': 'fixed'}
        card['rows'] = [dict(row, id=f'r-{i + 1}') for i, row in enumerate(rows)]
    original_ids = set(re.findall(r'    id: "([^"]+)"', (ROOT / 'components/MarkBank/cards/japanese/higher.ts').read_text()))
    if cid in original_ids:
        card['qa']['gates'].append('reviewed-card-correction')
    language = None
    if section == 'LA': language = (3, [(2, 0)], 'Japanese')
    elif section == '1B': language = (7, [(11, 1)], 'Japanese')
    elif section == '2A': language = (9, [(2, 0)], 'Japanese')
    if section in ['1C', '2B', '3B']:
        page, start = {'1C': (8, 0), '2B': (10, 1), '3B': (11, 30)}[section]
        condition = joined_selector('scheme', page, [(r, 0) for r in range(start, start + 3)])
        card['extraneousMaterialRule'] = {
            'multiplier': 0.5,
            'conditionLabel': 'quotation without manipulation where manipulation required or containing extraneous material',
            'sourceText': condition, 'schemePages': [page]}
        language = (page, [(2, 0)], 'English') if section == '1C' else (page, [(start + 1, 0), (start + 2, 0)], None)
    if language:
        page, parts, named = language
        card['sourceEvidence']['generalSchemePages'] = [page]
        card['answerLanguageRule'] = {'otherLanguageMultiplier': 0.5,
            'sourceText': joined_selector('scheme', page, parts), 'schemePages': [page]}
        if named: card['answerLanguageRule']['penalizedLanguage'] = named
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
    metadata = {'src': rel, 'alt': alt, 'attribution': '© State Examinations Commission.',
                'source': {'document': component, 'page': page, 'region': region}}
    previous_path = ROOT / 'components/MarkBank/figures-japanese.json'
    previous = json.loads(previous_path.read_text()).get(key, {})
    current = path.exists() and all(previous.get(field) == value for field, value in metadata.items()) and previous.get('md5') == hashlib.md5(path.read_bytes()).hexdigest()
    proof_path = ROOT / 'tmp/japanese-review/2011-hl-crop-rendered.json'
    proofs = json.loads(proof_path.read_text()) if proof_path.exists() else {}
    if os.environ.get('JA_RENDER_ONLY') == key:
        sheet.get_pixmap(matrix=fitz.Matrix(2, 2), clip=rect).save(path)
        proofs[key] = {**metadata, 'md5': hashlib.md5(path.read_bytes()).hexdigest()}
        proof_path.write_text(json.dumps(proofs, ensure_ascii=False, indent=2) + '\n')
    elif path.exists() and not current:
        proof = proofs.get(key, {})
        valid = all(proof.get(field) == value for field, value in metadata.items()) and proof.get('md5') == hashlib.md5(path.read_bytes()).hexdigest()
        if not valid:
            assert os.environ.get('JA_RENDER_ONLY'), f'Crop metadata changed; rerender explicitly: {key}'
            FIGURES[key] = {**metadata, 'md5': None}
            return key
    FIGURES[key] = {**metadata, 'md5': hashlib.md5(path.read_bytes()).hexdigest() if path.exists() else None}
    return key


def clean_tariff(text):
    return re.sub(r'\s*\(?\d+\s*marks?\)?\s*$', '', text).strip()


def selected(page, parts):
    return joined_selector('scheme', page, parts)


def split_marks(text, marks=1):
    return [part.strip(' ,-/.;' ) for part in re.split(rf'\({marks}\s+marks?\)', text) if part.strip(' ,-/.' )]


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
    instruction = join_cells('paper', 3, [0, 1], 300)
    labels = [p(3, 2, 3)] + [p(3, r, 2) for r in range(3, 10)]
    rows = [point(s(7, r, 1), contextNote=label) for r, label in zip(range(3, 11), labels)]
    card = add('1A', None, instruction + '\n' + '\n'.join(labels), rows, 'japanese-5-0', [3], [7], reading=[2],
               figure=crop('ja-2011-hl-1a', 3, [.04, .025, .97, .375], instruction))
    group_rows(card, [(f'item-{i + 1}', label, i, i + 1) for i, label in enumerate(labels)])
    for q, qr in enumerate([[11, 12], [14, 15], [17, 18], [20, 21], [23, 24], [26, 27]], 1):
        question = join_cells('paper', 3, qr, 300)
        if q == 1: rows = [point(value) for value in split_marks(s(7, 13))]
        elif q == 2: rows = [point(s(7, 16), 2)]
        elif q == 3: rows = [anyn([value.strip() for value in s(7, 18).split(' (1 mark', 1)[0].split('/')], 2, contextNote=cell('scheme', 7, 18, 0))]
        elif q == 4:
            answer = selected(7, [(20, 0), (21, 0)])
            rows = [anyn([value.strip() for value in answer.split(' ( any', 1)[0].split('/')], 2, contextNote=answer + ' Count distinct details once.')]
        elif q == 5: rows = [point(s(7, 23), 2)]
        else: rows = [anyn([value.strip() for value in s(7, 25).split('/')], 2, contextNote=cell('scheme', 7, 26, 0))]
        c = add('1B', q, question, rows, 'japanese-5-0', [3], [7], reading=[2])
        c['stem'] = p(3, 10, 1)
    for q, qr, sr in [(1, 1, 4), (2, 3, 7), (3, 5, 9)]:
        rows = [point(value) for value in split_marks(s(8, sr))] if q == 3 else [point(s(8, sr), 2)]
        c = add('1C', q, p(4, qr), rows, 'japanese-5-0', [4], [8], reading=[2]);c['stem'] = english(p(4, 0))
    for q, instruction_row, question_rows, answer_rows, region in [(1, 9, range(10, 13), range(12, 16), [.055, .345, .97, .535]),
        (2, 14, range(15, 19), range(17, 21), [.055, .535, .97, .72])]:
        rows = [point(s(8, r, 1) if q == 1 else unnumber(s(8, r)), contextNote=f'({["i", "ii", "iii", "iv"][i]})') for i, r in enumerate(answer_rows)]
        instruction = p(4, instruction_row)
        add('1D', q, instruction + '\n' + '\n'.join(p(4, r) for r in question_rows), rows, 'japanese-5-4', [4], [8], reading=[2],
            figure=crop(f'ja-2011-hl-1d-{q}', 4, region, instruction))


def reading_q2():
    rows = [point(s(9, 5, 2), contextNote='Niamh — lucky numbers'), point(s(9, 5, 3), contextNote='Mike — lucky numbers'),
            point(s(9, 7, 1), contextNote='Niamh — lucky colour')]
    brown, green = s(9, 7, 2).split('&')
    rows += [point(brown.strip(), contextNote='Mike — lucky colours'), point(green.strip(), contextNote='Mike — lucky colours')]
    instruction = english(p(7, 2))
    c = add('2A', 1, instruction + '\n' + p(7, 3) + '\n' + english(p(7, 4)) + '\n' + english(p(7, 5)) + ' ' + p(7, 6),
            rows, 'japanese-5-0', [7], [9], reading=[6], figure=crop('ja-2011-hl-2a-1', 7, [.065, .025, .97, .205], instruction))
    group_rows(c, [('niamh-numbers', 'Niamh — lucky numbers', 0, 1), ('mike-numbers', 'Mike — lucky numbers', 1, 2), ('niamh-colour', 'Niamh — lucky colour', 2, 3), ('mike-colours', 'Mike — lucky colours', 3, 5)])
    add('2A', 2, p(7, 8).split('  ___', 1)[0], [point(s(9, 11), 2)], 'japanese-5-0', [7], [9], 'i', reading=[6])
    add('2A', 2, p(7, 10), [anyn([text.strip() for text in s(9, 13).split('/')], 2, contextNote=cell('scheme', 9, 13, 1))], 'japanese-5-0', [7], [9], 'ii', reading=[6])
    scenario = [point(s(9, 16, 0)), point(s(9, 16, 1)), point(s(9, 18).split('(1 mark)', 1)[0].strip()), point(s(9, 18).split('(1 mark)', 1)[1].strip())]
    for i, row in enumerate(scenario): row['contextNote'] = 'If he has a date' if i < 2 else 'If he does not have a date'
    question = english(p(7, 12)) + '\n' + english(p(7, 13)).split(' ___', 1)[0] + '\n' + english(p(7, 14))
    c = add('2A', 2, question, scenario, 'japanese-5-0', [7], [9], 'iii', reading=[6])
    group_rows(c, [('with-date', 'If he has a date', 0, 2), ('without-date', 'If he does not have a date', 2, 4)])
    money = selected(9, [(29, 0), (30, 0), (31, 0)])
    buy, parents = money.removeprefix('(').removesuffix(')').split(';')
    rows = [point(selected(9, [(21, 1), (22, 0), (23, 0)]), 2, contextNote='Niamh — advice regarding work'),
            point(selected(9, [(21, 2), (22, 1)]), 2, contextNote='Niamh — advice regarding money'),
            point(s(9, 25, 1), 2, contextNote='Mike — advice regarding work'),
            point(clean_tariff(buy).rstrip(','), contextNote='Mike — advice regarding money'),
            point(clean_tariff(parents).rstrip(','), contextNote='Mike — advice regarding money')]
    instruction = p(7, 16).split('Complete', 1)[1];instruction = 'Complete' + instruction
    c = add('2A', 3, instruction + '\n' + p(7, 18) + '\n' + p(7, 19) + '\n' + p(7, 20), rows, 'japanese-5-0', [7], [9], reading=[6],
            figure=crop('ja-2011-hl-2a-3', 7, [.065, .445, .97, .625], instruction))
    group_rows(c, [('niamh-work', 'Niamh — work', 0, 1), ('niamh-money', 'Niamh — money', 1, 2), ('mike-work', 'Mike — work', 2, 3), ('mike-money', 'Mike — money', 3, 5)])
    for q, qr, sr in [(1, [23, 24], 6), (2, [26], 8), (3, [28], 10)]:
        c = add('2B', q, join_cells('paper', 7, qr), [point(s(10, sr), 2)], 'japanese-5-0', [7], [10], reading=[6])
        c['stem'] = join_cells('paper', 7, [21, 22], 300)
        if q == 2: c['rows'][0]['contextNote'] = 'Source discrepancy: the printed scheme literally says はじめまた. This published typo is retained; it has not been silently replaced with はじめた.'
    instruction = join_cells('paper', 8, range(3), 290)
    rows = [point(re.sub(r'^\d+[.．]\s*', '', s(10, r)), contextNote=str(i + 1)) for i, r in enumerate(range(12, 22))]
    c = add('2C', None, instruction + '\n' + '\n'.join(p(8, r) for r in range(3, 14)), rows, 'japanese-5-5', [8], [10], reading=[6],
            figure=crop('ja-2011-hl-2c', 8, [.035, .025, .98, .86], instruction))
    group_rows(c, [(f'verb-{i + 1}', str(i + 1), i, i + 1) for i in range(10)])


def reading_q3():
    pool = selected(11, [(3, 0), (4, 0)])
    add('3A', 1, p(10, 2), [anyn([text.strip() for text in pool.split('(any', 1)[0].split('/')], 2, contextNote=pool)], 'japanese-5-1', [10], [11], reading=[9])
    rows, groups = [], []
    labels = [p(10, 7), p(10, 8), p(10, 9), p(10, 10), p(10, 12), p(10, 13)]
    values = [
        [point(value) for value in split_marks(selected(11, [(8, 2), (9, 0)]))],
        [point(value) for value in split_marks(selected(11, [(11, 1), (12, 0)]))],
        [anyn([text.strip() for text in selected(11, [(14, 1), (15, 0)]).split(' ( any', 1)[0].split('/')], 2)],
        [point(s(11, 17, 1), 2, contextNote='Source discrepancy: the paper names ウェザー・ニュース・タッチ; the scheme table names ウェザー・ニュース・リポート. The original paper label and published weather-vocabulary answer are retained.')],
        [criterion(selected(11, [(21, 1), (23, 0)]), 2, [0, 1, 2], 'Japanese geography earns 2; the printed Interesting partial earns 1 within the same app response.')],
        [anyn([text.strip().rstrip(')') for text in selected(11, [(25, 1), (26, 0)]).split(';')], 2, contextNote=cell('scheme', 11, 27, 0))],
    ]
    for i, components in enumerate(values):
        start = len(rows);rows.extend(components)
        for row in components: row['contextNote'] = labels[i] + '. ' + row.get('contextNote', '')
        groups.append((f'app-{i + 1}', labels[i], start, len(rows)))
    question = english(p(10, 4, 1)) + '\n' + p(10, 6) + '\n' + '\n'.join(labels)
    c = add('3A', 2, question, rows, 'japanese-5-1', [10], [11], reading=[9], figure=crop('ja-2011-hl-3a-2', 10, [.035, .15, .98, .59], question))
    group_rows(c, groups)
    for q, qr, sp, sr in [(1, 15, 11, 34), (2, 17, 12, 1), (3, 19, 12, 4), (4, 21, 12, 6)]:
        c = add('3B', q, p(10, qr), [point(s(sp, sr), 2)], 'japanese-5-1', [10], [11] if q == 1 else [11, 12], reading=[9]);c['stem'] = english(p(10, 14, 1))
    rows, groups = [], []
    for i, r in enumerate(range(8, 14)):
        label = p(11, 6 + i, 1);start = len(rows)
        rows += [point(s(12, r, 1), contextNote=label + ' — reading letter'), point(s(12, r, 3), contextNote=label + ' — English meaning')]
        groups.append((f'kanji-{i + 1}', label, start, len(rows)))
    instruction = join_cells('paper', 11, range(4), 290)
    c = add('3C', None, instruction + '\n' + '\n'.join(p(11, r) for r in range(4, 12)), rows, 'japanese-5-4', [11], [12], reading=[9],
            figure=crop('ja-2011-hl-3c', 11, [.035, .025, .98, .365], instruction))
    group_rows(c, groups)
    rows = [point(unnumber(s(12, r, 0)) if r == 22 else s(12, r, 1), contextNote=f'({i + 1})') for i, r in enumerate(range(15, 25))]
    instruction = join_cells('paper', 11, [12, 13], 290)
    c = add('3D', None, instruction + '\n' + '\n'.join(p(11, r) for r in range(15, 21)), rows, 'japanese-5-5', [11], [12], reading=[9],
            figure=crop('ja-2011-hl-3d', 11, [.035, .355, .98, .63], instruction))
    group_rows(c, [(f'particle-{i + 1}', str(i + 1), i, i + 1) for i in range(10)])
    instruction = english(p(11, 22)) + ' ' + p(11, 23)
    allocation = cell('scheme', 12, 28)
    criteria = [{'id': f'point-{i}', 'label': f'Distinct point {i}', 'maxMarks': 2, 'permittedMarks': [0, 2], 'guidance': [allocation]} for i in [1, 2]]
    criteria.append({'id': 'discretionary', 'label': 'Discretionary mark', 'maxMarks': 1, 'permittedMarks': [0, 1], 'guidance': [allocation]})
    add('3E', None, instruction + '\n' + p(11, 27) + ' ' + p(11, 28), [], 'japanese-5-6', [11], [12], total=5,
        rubric={'system': 'language-writing', 'taskRequirements': [instruction], 'criteria': criteria,
        'markingGuideNote': 'Assess two distinct points at 2 marks each plus one discretionary mark. The scheme supplies no model answer or discretionary descriptor; do not invent either. Include Japanese technology company names as the original question requires.'})
def steps(maximum):
    return list(range(maximum + 1))


def writing():
    for q, sp, maximum, lower, threshold, length in [(4, 14, 20, 15, 10, 150), (5, 16, 30, 20, 15, 200)]:
        ranges = [(16, 24), (24, 32), (32, 39)] if q == 4 else [(16, 24), (24, 33), (33, 41)]
        guidance = [join_cells('scheme', sp, range(a, b), 180) for a, b in ranges]
        normal = [(0, 5), (6, 14), (15, 20)] if q == 4 else [(0, 7), (8, 20), (21, 30)]
        low = [(0, 3), (4, 10), (11, 15)] if q == 4 else [(0, 4), (5, 12), (13, 20)]
        bands = [{'label': f'{lo}–{hi}', 'marks': list(range(lo, hi + 1)), 'guidance': [text]} for (lo, hi), text in zip(normal, guidance)]
        reduced = [{'label': f'{lo}–{hi}', 'marks': list(range(lo, hi + 1)), 'guidance': [text]} for (lo, hi), text in zip(low, guidance)]
        if q == 4:
            instruction = join_cells('paper', 12, [1, 2], 280)
            question = instruction + '\n' + join_cells('paper', 12, [3, 4, 6, 8, 9, 10, 11, 13, 14, 15, 16, 18, 20, 22, 24, 26, 29, 31, 33, 35], 300)
            criteria = [{'id': f'heading-{i}', 'label': label, 'maxMarks': 5, 'permittedMarks': steps(5),
                         'guidance': [selected(13, [(3, 0), (r, 1), (r + 6, 1)])]}
                        for i, label, r in [(1, 'Where you went', 4), (2, 'What you did', 5), (3, 'Why the day was great or terrible', 6)]]
            discretionary = selected(13, [(7, 0), (13, 0)])
            guide = 'Choose one complete diary entry: a great day OR a terrible day. Assess all three required headings at up to 5 marks each, plus up to 5 discretionary marks for extra information. Do not mix the alternatives. The printed expression guidance refers to numbering (1–6), although each actual option has three headings; no extra headings are invented. Lower E applies when total content is 10 or less, or fewer than 150 characters.'
            pp = [12]
        else:
            instruction = p(15, 1)
            question = instruction + '\n(a) ' + p(15, 4) + ' ' + p(15, 5) + '\n' + '\n'.join(p(15, r) for r in range(17, 27))
            question += '\nOR\n(b) ' + p(16, 2) + ' ' + p(16, 3) + '\n' + '\n'.join(p(16, r) for r in range(13, 21))
            criteria = [{'id': f'heading-{i}', 'label': label, 'maxMarks': marks, 'permittedMarks': steps(marks),
                         'guidance': [selected(15, [(r, 1), (r, 2), (r + 6, 1), (r + 6, 2)])]}
                        for i, label, marks, r in [(1, 'Brief personal background', 5, 4), (2, 'Reasons for the chosen option', 10, 5), (3, 'Return-to-Ireland plans OR how you find Japanese', 10, 6)]]
            discretionary = selected(15, [(r, 0) for r in [2, 3, 8, 9]])
            guide = 'Choose one complete option and cover its three required headings. Both original flyers are retained in full: scholarship essay OR speech-contest entry. Background earns up to 5, each other required heading up to 10, and discretionary content up to 5 across the task. Do not mix option-specific headings. The expression guidance has stale (i)a–f/(ii)a–d numbering; it does not add headings. Lower E applies when total content is 15 or less, or fewer than 200 characters.'
            pp = [15, 16]
        criteria.append({'id': 'discretionary', 'label': 'Discretionary content', 'maxMarks': 5, 'permittedMarks': steps(5), 'guidance': [discretionary]})
        content_ids = [criterion['id'] for criterion in criteria]
        criteria.append({'id': 'expression', 'label': 'Expression', 'maxMarks': maximum, 'permittedMarks': steps(maximum),
            'bands': bands, 'guidance': [selected(sp, [(r, None) for r in ([39, 40] if q == 4 else [41, 42])]), selected(sp, [(r, None) for r in range(1, 9)])],
            'limits': [{'id': 'lower-e', 'maxMarks': lower, 'when': {'any': [{'criterionIds': content_ids, 'atMost': threshold}, {'length': 'characters', 'below': length}]},
                        'bands': reduced, 'guidance': [selected(sp, [(r, None) for r in range(9, 13)])]}]})
        c = add(str(q), None, question, [], 'japanese-5-7', pp, [sp - 1, sp], total=maximum * 2, reading=pp,
            rubric={'system': 'language-writing', 'taskRequirements': [instruction], 'criteria': criteria, 'markingGuideNote': guide})
        if q == 4: c['questionFigureKey'] = crop('ja-2011-hl-4', 12, [.04, .025, .97, .905], question)
        # Q5 spans two paper pages. Its full literal English flyers are displayed
        # as text, with both original source pages; no one-page crop hides (b).


def listening():
    def listen(part, q, suffix, qr, rows, question=None, rubric=None, total=None):
        pp = {'A': 2, 'B': 3, 'C': 4, 'D': 5}[part];sp = pp + 1
        text = question or re.sub(r'^(?:\d+\.\s*)?(?:\([ivx]+\)\s*)?', '', join_cells('aural', pp, qr, 300)).strip()
        c = add('L' + part, q, text, rows, 'japanese-6-2' if part == 'C' else 'japanese-6-0',
                [pp], [sp], suffix or '', rubric=rubric, total=total)
        c['sourceMaterial'] = source([pp], 'source-question', 'aural')
        c['stem'] = join_cells('aural', pp, range(1, 5 if part in 'AB' else 6), 300)
        if part == 'A': c['stem'] += ' ' + cell('aural', 2, 6, 1)
        if part in 'BC': c['stem'] += '\n' + join_cells('aural', pp, [{'B': {1: 5, 2: 15, 3: 25}, 'C': {1: 6, 2: 20, 3: 29}}[part][q]], 300)
        return c

    # Row extraction merges portions of adjacent table columns. These exact
    # substring boundaries are independently visible in original physical p3.
    merged = cell('scheme', 3, 15, 2)
    first_reason = merged.split(' A double class', 1)[0]
    assert first_reason == 'Caught a cold/ has a'
    class_answer = merged.split(' A double class', 1)[1].split(' Tomorrow morning', 1)[0]
    class_answer = 'A double class' + class_answer + ' ' + cell('scheme', 3, 16, 2)
    cancelled = cell('scheme', 3, 27, 0).split(' Bad weather', 1)[0]
    values = [
        [('reason', point(selected(3, [(7, 2), (8, 1)]), 2)),
         ('alternative', criterion(selected(3, [(7, 3), (8, 2), (9, 0)]), 2, [0, 1, 2], 'Have lunch earns 2; next Tuesday alone earns 1.')),
         ('callback', point(selected(3, [(7, 4), (8, 3), (9, 1)]), contextNote=selected(3, [(10, 0), (11, 0), (12, 1)])))],
        [('cancelled', point(selected(3, [(15, 1), (16, 0)]), 2)),
         ('reason', criterion(first_reason + ' ' + selected(3, [(16, 1), (17, 0), (18, 0), (19, 0)]), 2, [0, 1, 2], 'Any complete printed reason earns 2; sick alone earns 1.')),
         ('alternative', criterion(class_answer + ' ' + cell('scheme', 3, 18, 1), 2, [0, 1, 2], 'A double class earns 2; double alone earns 1.'))],
        [('cancelled', point(selected(3, [(23, 0), (24, 0)]), 2)), ('reason', point(s(3, 23, 1), 2)), ('callback', point(s(3, 23, 3)))],
        [('cancelled', criterion(cancelled + ' ' + cell('scheme', 3, 28, 0), 2, [0, 1, 2], 'Barbeque party earns 2; party alone earns 1.')),
         ('alternative', point(s(3, 27, 1), 2)), ('callback', point(selected(3, [(27, 2), (28, 1)])))],
    ]
    rows, groups = [], []
    for caller, entries in zip(['Yuriko', 'Yamada', 'Mami', 'Kazuyo'], values):
        for column, row in entries:
            start = len(rows);row['contextNote'] = caller + ' — ' + column + '. ' + row.get('contextNote', '');rows.append(row)
            groups.append((caller.lower() + '-' + column, caller + ' — ' + column, start, len(rows)))
    table = listen('A', None, None, [], rows, cell('aural', 2, 6, 1))
    group_rows(table, groups)
    table['stem'] += '\nFour cells are already given and carry no marks: David’s Thursday farewell, Yamada’s tomorrow-morning callback, Mami’s Friday meeting, and Kazuyo’s bad-weather reason. Complete all twelve remaining cells.'
    table['questionFigureKey'] = crop('ja-2011-hl-la', 2, [.055, .025, .975, .92], table['questionText'], 'aural')
    assert len(rows) == 12 and row_total(rows) == 21

    location = s(4, 3)
    components, alternative = location.split('/ ', 1)
    variants = [{'id': 'components', 'label': 'Mori and department store', 'rows': [dict(point(text), id=f'r-{i + 1}') for i, text in enumerate(split_marks(components))]},
                {'id': 'depato', 'label': 'Mori depato', 'rows': [dict(point(alternative, 2), id='r-1')]}]
    c = listen('B', 1, 'i', [6, 7], variants[0]['rows']);c['answerVariants'] = variants
    directions = s(4, 5).split('2 marks,', 1)
    rows = [point(directions[0].strip(), 2), criterion(clean_tariff(directions[1]), 2, [0, 1, 2], cell('scheme', 4, 5, 1))]
    listen('B', 1, 'ii', [9], rows)
    listen('B', 1, 'iii', [12, 13], [point(s(4, r)) for r in [7, 8]])
    listen('B', 2, 'i', [16], [anyn([text.strip() for text in s(4, 11).split(' (any', 1)[0].split('/')], 2, contextNote=cell('scheme', 4, 11, 0))])
    listen('B', 2, 'ii', [18, 19], [point(s(4, 13), 2)])
    donut, coffee = s(4, 15).split('1 mark and')
    listen('B', 2, 'iii', [21], [point(donut.strip()), point(clean_tariff(coffee))])
    listen('B', 2, 'iv', [23], [point(s(4, 17), 2)])
    listen('B', 3, None, [26, 27], [anyn([text.strip() for text in s(4, 21).split(';')], 3, contextNote=cell('scheme', 4, 20, 0))])
    listen('C', 1, 'i', [7, 8], [point(s(5, 2).split('? ', 1)[1])])
    c = listen('C', 1, 'ii', [10, 11], [point(s(5, 3).split('? ', 1)[1], 2)])
    c['rows'][0]['contextNote'] = 'The scheme labels this answer (iii); the original paper identifies the duration question as (ii).'
    listen('C', 1, 'iii', [13], [criterion(selected(5, [(5, 0), (6, 0)]), 2, [0, 1, 2], 'One complete garden detail earns 2. Beautiful alone or has cherry blossoms alone earns 1; these partials do not combine into a new 2-mark answer.')])
    months = s(5, 8).split('(', 1)[0].removeprefix('From ').split(' to ')
    listen('C', 1, 'iv', [15], [point(text) for text in months])
    listen('C', 1, 'v', [17], [point(s(5, 10), 3)])
    listen('C', 2, 'i', [21], [point(s(5, 12).split('? ', 1)[1], 2)])
    pool = selected(5, [(14, 0), (15, 0), (16, 0), (16, 1)])
    guide = 'Two distinct responses, maximum 4. Record any manga-only 1-mark partial in the FIRST slot regardless of answer order. That partial may be used ONCE across the whole task and may never also score alongside an overlapping full detail. The scheme lists manga-only after the whole pool and does not tie it to a particular full answer.'
    listen('C', 2, 'ii', [23, 24], [criterion(pool, 2, [0, 1, 2], 'First response: full detail or the sole manga-only partial. ' + guide),
                                   criterion(pool, 2, [0, 2], 'Second response: another distinct full detail. ' + guide)])
    phone = listen('C', 2, 'iii', [27], [point(s(5, 18), 2, contextNote='The complete phone number earns 2. No per-digit allocation is published; do not invent one.')])
    phone['questionFigureKey'] = crop('ja-2011-hl-lc-2-iii', 4, [.505, .72, .965, .795], phone['questionText'], 'aural')
    weather = selected(5, [(21, 0), (22, 0)])
    full, partial = weather.split(' (2 marks', 1)
    groups = [
        {'id': 'morning', 'label': 'Morning', 'rows': [], 'criteria': [{'id': 'morning-answer', 'label': 'Morning detail', 'maxMarks': 2, 'permittedMarks': [0, 1, 2], 'guidance': [full.split(' P.m.', 1)[0], weather]}]},
        {'id': 'afternoon', 'label': 'Afternoon', 'rows': [], 'criteria': [{'id': 'afternoon-answer', 'label': 'Afternoon detail', 'maxMarks': 2, 'permittedMarks': [0, 1, 2], 'guidance': ['P.m.' + full.split(' P.m.', 1)[1].split(' Temperature', 1)[0], weather]}]},
        {'id': 'temperature', 'label': 'Temperature', 'rows': [{'id': 'answer', 'text': 'Temperature' + full.split('Temperature', 1)[1], 'marks': 2}]},
    ]
    listen('C', 3, None, [30, 31], [], rubric={'system': 'language-points', 'count': 2, 'groups': groups,
        'taskRequirements': [join_cells('aural', 4, [30, 31], 300)], 'markingGuideNote': weather + ' Count each full/partial concept once; only two distinct details count. Fine alone earns1 within morning; rain alone earns1 within afternoon.'}, total=4)
    listen('D', 1, 'i', [6], [criterion(s(6, 2), 2, [0, 1, 2], 'Cafe earns 2; gym/fitness centre alone earns 1.')])
    listen('D', 1, 'ii', [8, 9], [anyn([text.strip() for text in s(6, 4).split(';')], 2, 2, contextNote=cell('scheme', 6, 5, 0))])
    listen('D', 1, 'iii', [12, 13], [point(s(6, 7), 2, contextNote=cell('scheme', 6, 8, 0))])
    listen('D', 2, 'i', [16], [criterion(s(6, 10), 2, [0, 1, 2], 'Library earns 2; in the university alone earns 1.')])
    listen('D', 2, 'ii', [19, 20], [anyn([text.strip() for text in s(6, 12).split(';')], 2, 2, contextNote=cell('scheme', 6, 13, 0))])
    details = s(6, 15).split(';')
    groups = [{'id': f'detail-{i + 1}', 'label': text.strip(), 'rows': [{'id': 'answer', 'text': text.strip(), 'marks': 2}]} for i, text in enumerate(details[:2])]
    groups.append({'id': 'friends', 'label': 'Cannot hang out with friends', 'rows': [], 'criteria': [{'id': 'friends-answer', 'label': 'Friends detail', 'maxMarks': 2, 'permittedMarks': [0, 1, 2], 'guidance': [details[2].strip(), cell('scheme', 6, 16, 0)]}]})
    listen('D', 2, 'iii', [23, 24], [], rubric={'system': 'language-points', 'count': 2, 'groups': groups,
        'taskRequirements': [join_cells('aural', 5, [23, 24], 300)], 'markingGuideNote': cell('scheme', 6, 16, 0) + ' Friends alone earns1 within the cannot-hang-out concept, never as another independent detail. The scheme labels this answer(iv), while the original paper identifies Q2(iii).'}, total=4)


def build():
    reading_q1(); reading_q2(); reading_q3(); writing(); listening()
    census = json.loads((Path(__file__).parent / 'reviews/japanese-2011-hl-census.json').read_text())
    expected = {'ja-2011-hl-' + '-'.join(str(part).lower() for part in task['key'] if part is not None): task for task in census['tasks']}
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
    assert len(CARDS) == 56
    assert sum(card['totalMarks'] for card in CARDS) == 300
    assert sum('answerLanguageRule' in card for card in CARDS) == 22
    assert sum('extraneousMaterialRule' in card for card in CARDS) == 10
    assert '\ufffd' not in json.dumps([CARDS, EVIDENCE], ensure_ascii=False)
    return {'subjectId': 'japanese', 'sitting': '2011-hl', 'reviewedAt': '2026-11-11',
            'sources': [{'document': name, 'path': str(path.relative_to(ROOT)), 'sha256': PINNED_SOURCES[path],
                         'pagesReviewed': list(range(1, len(DOCS[name]) + 1))} for name, path in [('paper', PAPER), ('aural', AURAL), ('scheme', SCHEME)]],
            'cards': CARDS, 'selectors': EVIDENCE, 'status': 'source-captured', 'choiceAnalysis': census['choiceBoundaries'], 'consolidations': []}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    result = build()
    if args.write:
        assert all(figure['md5'] for figure in FIGURES.values()), 'Render each planned source crop in a separate guarded slot before publication'
        scheme_text = ''.join(f'\n## Page {i + 1}\n\n' + page.get_text(sort=True) for i, page in enumerate(DOCS['scheme']))
        scheme_text += '\n## Original text with furigana folded at its printed character\n'
        scheme_text += ''.join(f'\n### Physical page {i + 1}\n\n' + '\n'.join(' '.join(group[2] for group in row) for row in rows) + '\n' for i, rows in enumerate(ROWS['scheme']))
        for page, x_ranges in [(3, [(155, 245), (245, 355), (355, 452), (452, 590)]), (9, [(153, 325), (326, 550)]), (11, [(258, 550)])]:
            scheme_text += f'\n## Original table columns — physical page {page}\n'
            scheme_text += '\n'.join(DOCS['scheme'][page - 1].get_text(clip=fitz.Rect(x0, 0, x1, DOCS['scheme'][page - 1].rect.height), sort=True) for x0, x1 in x_ranges)
        SCHEME.with_suffix('.md').write_text(scheme_text.rstrip() + '\n')
        (ROOT / 'scripts/markbank/authoring/reviews/japanese-2011-hl.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
        manifest = ROOT / 'components/MarkBank/figures-japanese.json'
        previous = json.loads(manifest.read_text()); previous.update(FIGURES)
        manifest.write_text(json.dumps(previous, ensure_ascii=False, indent=2) + '\n')
    (ROOT / 'tmp/japanese-review/2011-hl-draft.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    (ROOT / 'tmp/japanese-review/2011-hl-crop-plan.json').write_text(json.dumps(FIGURES, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'cards': len(CARDS), 'marks': sum(card['totalMarks'] for card in CARDS), 'figures': len(FIGURES)}, indent=2))
