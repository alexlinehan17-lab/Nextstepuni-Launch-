#!/usr/bin/env python3
"""2010 Higher Japanese, independently reviewed against all original pages.

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
PAPER = ROOT / 'examiner-reports/japanese/papers/2010-hl-000-paper.pdf'
AURAL = ROOT / 'examiner-reports/japanese/papers/2010-hl-A00-paper.pdf'
SCHEME = ROOT / 'examiner-reports/japanese/schemes/2010-hl.pdf'
PINNED_SOURCES = {
    PAPER: 'a8431333d349dc9c686ae8bad56a92ea1800e1e0186af3c6850ea4599b28f629',
    AURAL: '57c204e0041bc620f105acf3a6c71549f4c633e0448a10517355f2c9989fdd64',
    SCHEME: '7a71fa81c9f4dcdf00223ec1774c8e8c1fe86ce8ddffa61c04cb207c896d6628',
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
    return {'kind': kind, 'label': '2010 Japanese Higher Level', 'title': 'Original examination material',
            'pages': pages, 'attribution': '© State Examinations Commission.',
            **({'presentationNote': FURIGANA_NOTE} if component == 'paper' else {}),
            '_component': component}


def add(section, q, question, rows, topic, paper_pages, scheme_pages, suffix='', rubric=None, total=None, reading=None, figure=None):
    cid = f'ja-2010-hl-{section.lower()}' + (f'-{q}' if q is not None else '') + (f'-{suffix}' if suffix else '')
    ref = f'2010 HL Section {section}' + (f' Q{q}' if q is not None else '')
    if suffix:
        ref += (' Q' if q is None else '') + ''.join(f'({part})' for part in suffix.split('-'))
    listening = section.startswith('L')
    card = {'id': cid, 'source': 'sec', 'subjectId': 'japanese', 'specVersion': 'lc-japanese-syllabus',
            'kind': 'rubric' if rubric else 'question', 'level': 'higher', 'year': 2010,
            'section': section[1:] if listening else section[0],
            'topicId': topic, 'conceptId': concept_for(question, cid), 'questionRef': ref,
            'questionText': question, 'totalMarks': total if total is not None else row_total(rows),
            'qa': {'gates': ['verbatim', 'tariff', 'figure'], 'humanReviewedBy': 'agent-verified', 'humanReviewedAt': '2026-11-12'},
            'sourceEvidence': {'component': 'aural' if listening else 'paper', 'paperPages': paper_pages, 'schemePages': scheme_pages},
            'schemeCitation': 'Marking points quoted from the SEC marking scheme, Japanese 2010 Higher Level — © State Examinations Commission.'}
    if rubric:
        card['rubric'] = rubric
    else:
        card['tariffModel'] = {'kind': 'fixed'}
        card['rows'] = [dict(row, id=f'r-{i + 1}') for i, row in enumerate(rows)]
    original_ids = set(re.findall(r'    id: "([^"]+)"', (ROOT / 'components/MarkBank/cards/japanese/higher.ts').read_text()))
    if cid in original_ids:
        card['qa']['gates'].append('reviewed-card-correction')
    # Bind each rule from its own original heading; Part A is confidence-only.
    language = None
    if section == 'LB': language = (4, '1/2 marks if answered in Japanese', 'Japanese')
    elif section in ['LC1', 'LC2']: language = (5, '1/2 marks if answered in Japanese', 'Japanese')
    elif section == 'LD' and q != 1: language = (6, '1/2 marks if answered in Japanese', 'Japanese')
    elif section == '1AB': language = (7, 'B:  (14 marks) Half marks if answered in Japanese.', 'Japanese')
    elif section == '1B': language = (7, 'Part B (10 marks) Half marks if answered in Japanese.', 'Japanese')
    elif section == '2A': language = (8, '1/2 marks if answered in English', 'English')
    elif section == '2B': language = (8, '1/2 marks if answered in Japanese', 'Japanese')
    if language:
        page, fragment, named = language
        matches = [i for i, row in enumerate(ROWS['scheme'][page - 1]) if fragment in ' '.join(group[2] for group in row)]
        assert len(matches) == 1, (section, page, fragment, matches)
        card['sourceEvidence']['generalSchemePages'] = [page]
        card['answerLanguageRule'] = {'otherLanguageMultiplier': 0.5,
            'sourceText': joined_selector('scheme', page, [(matches[0], None)]), 'schemePages': [page], 'penalizedLanguage': named}
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
    proof_path = ROOT / 'tmp/japanese-review/2010-hl-crop-rendered.json'
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


def listening_a():
    instruction = join_cells('aural', 2, [7, 8], 300)
    language = cell('scheme', 3, 2)
    note = (language + ' The scheme separately publishes half-credit content alternatives and this language reduction, '
            'but gives no rule for combining them. This complete 18-mark task is therefore a confidence review: '
            'no quarter mark, combined multiplier or calculated score is inferred. Given cells are not additional answers.')
    definitions = [
        ('tom-age', '1. TOM — age', [(8, 0)], '1 mark'),
        ('tom-hobby', '1. TOM — one hobby', [(6, 1), (7, 1)], '1 mark'),
        ('tom-reason', '1. TOM — one reason', [(6, 2), (7, 2), (8, 1)], '1 mark; literal half-credit alternative retained'),
        ('tara-birthday', '2. TARA — birthday', [(12, 1), (13, 2), (15, 0), (16, 0)], 'Month1 + day1'),
        ('tara-current', '2. TARA — current activity, one detail', [(12, 2), (13, 3), (14, 0), (15, 1), (17, 0), (18, 0), (19, 0), (20, 0), (21, 0)], '1 mark; all full/partial alternatives retained'),
        ('tara-reason', '2. TARA — one reason', [(12, 3), (13, 5), (15, 2), (20, 1), (21, 1)], '1 mark'),
        ('mike-age', '3. MIKE — age', [(22, 1)], '1 mark'),
        ('mike-birthday', '3. MIKE — birthday', [(22, 2), (23, 1), (25, 0), (26, 0)], 'Month1 + day1'),
        ('mike-current', '3. MIKE — current activity, one detail', [(22, 3), (23, 2), (24, 0), (25, 1), (28, 0), (29, 0), (30, 0), (31, 1), (32, 1)], '1 mark; all full/partial alternatives retained'),
        ('mike-hobby', '3. MIKE — one hobby', [(22, 4), (23, 3), (26, 1), (27, 0)], '1 mark for one listed alternative'),
        ('mike-reason', '3. MIKE — one reason', [(22, 5), (23, 4), (25, 2), (26, 2), (27, 1), (28, 1)], '1 mark for one listed alternative'),
        ('sophie-birthday', '4. SOPHIE — birthday', [(33, 1), (34, 1), (36, 0), (37, 0)], 'Month1 + day1'),
        ('sophie-current', '4. SOPHIE — current activity, one detail', [], '1 mark; all full/partial alternatives retained'),
        ('sophie-hobby', '4. SOPHIE — one hobby', [], '1 mark for one listed alternative'),
        ('sophie-reason', '4. SOPHIE — one reason', [(33, 3), (34, 4), (36, 3)], '1 mark for one listed alternative'),
    ]
    rows = []
    for identity, label, parts, tariff in definitions:
        if identity == 'sophie-current':
            # The row extractor merges adjacent table columns here. Remove
            # only the inspected next-column word, retaining the bound cell.
            first = cell('scheme', 3, 33, 2)
            assert first.endswith(' Designing')
            answer = first.removesuffix(' Designing') + ' ' + selected(3, [(34, 2), (35, 1), (36, 1), (37, 1), (38, 0), (39, 0), (40, 0), (41, 0)])
        elif identity == 'sophie-hobby':
            merged = cell('scheme', 3, 33, 2)
            assert merged.endswith(' Designing')
            answer = merged.rsplit(' ', 1)[1] + ' ' + selected(3, [(34, 3), (36, 2), (37, 2), (38, 1), (39, 1)])
        else:
            answer = selected(3, parts)
        # This is one complete task: show the shared limitation once, on its
        # first answer row, while keeping each remaining cell's own allocation.
        rows.append(point(answer, None, contextNote=f'{label}. Printed allocation: {tariff}.' + (f' {note}' if not rows else '')))
    card = add('LA', None, instruction, rows, 'japanese-6-1', [2], [3], total=18,
               figure=crop('ja-2010-hl-la', 2, [.07, .035, .98, .77], instruction, 'aural'))
    card['tariffModel'] = {'kind': 'questionTotal'}
    card['sourceEvidence']['generalSchemePages'] = [3]
    card['sourceMaterial'] = source([2], 'source-question', 'aural')
    card['stem'] = join_cells('aural', 2, range(1, 6), 300)
    for row, definition in zip(card['rows'], definitions):
        row['id'] = definition[0]


def listening_b():
    stem = join_cells('aural', 3, range(1, 6), 300)
    questions = [[7], [8, 9], [10], [11], [13, 14], [15, 16], [17]]
    answers = [s(4, 2, 1), s(4, 3).rsplit('?', 1)[1].strip(), s(4, 4, 1),
               s(4, 5, 1), s(4, 6).rsplit('?', 1)[1].strip(), s(4, 7, 1)]
    for q, source_rows in enumerate(questions, 1):
        question = join_cells('aural', 3, source_rows, 300)
        if q == 7:
            pool = selected(4, [(9, 1), (10, 0)]).split(', ')
            assert len(pool) == 3
            rows = [anyn(pool, 2, contextNote=cell('scheme', 4, 11))]
        else:
            rows = [point(answers[q - 1], 1 if q <= 2 else 2)]
        add('LB', q, question, rows, 'japanese-6-0', [3], [4])['stem'] = stem
    for letter, qr, sr in [('a', 20, 13), ('b', 21, 14), ('c', 22, 15)]:
        question = cell('aural', 3, 19, 1) + '\n' + cell('aural', 3, qr, 1)
        add('LB', 8, question, [point(s(4, sr, 1), 2)], 'japanese-6-0', [3], [4], suffix=letter)['stem'] = stem
    for letter, qr, sr in [('a', 24, 17), ('b', 25, 19)]:
        question = cell('aural', 3, 23, 1) + '\n' + cell('aural', 3, qr, 1)
        rows = [criterion(s(4, sr, 1), 2, [0, 1, 2], cell('scheme', 4, 18))] if letter == 'a' else [point(s(4, sr, 1), 2)]
        add('LB', 9, question, rows, 'japanese-6-0', [3], [4], suffix=letter)['stem'] = stem


def listening_c():
    stem = join_cells('aural', 4, range(1, 5), 300)
    section_one = join_cells('aural', 4, [6, 7], 300)
    for q, suffix, qrows, answer_row, count, note_row in [(1, 'a', [8, 9], 5, 2, 4), (2, '', [14, 15], 11, 3, 10)]:
        pool = s(5, answer_row).split('; ')
        assert len(pool) == 5
        card = add('LC1', q, join_cells('aural', 4, qrows, 300),
                   [anyn(pool, count, 2, contextNote=cell('scheme', 5, note_row))],
                   'japanese-6-0', [4], [5], suffix=suffix)
        card['stem'] = stem + '\n' + section_one
        if q == 1:
            answer = s(5, 8)
            rows = [point(text, 1) for text in split_marks(answer)]
            assert len(rows) == 2
            card = add('LC1', 1, join_cells('aural', 4, [12, 13], 300), rows, 'japanese-6-0', [4], [5], suffix='b')
            card['stem'] = stem + '\n' + section_one
    for q, qr, answer in [(1, 20, s(5, 14, 1).removeprefix('(iii) ')), (2, 21, s(5, 15).rsplit('?', 1)[1].strip())]:
        add('LC2', q, cell('aural', 4, qr, 1), [point(answer, 2)], 'japanese-6-0', [4], [5])['stem'] = stem
    instruction = join_cells('aural', 4, [22, 23, 24], 300)
    labels = [cell('aural', 4, 27, 2), cell('aural', 4, 28, 2), cell('aural', 4, 29, 3)]
    rows = [point(s(5, sr, 1), 2, contextNote=label) for sr, label in zip([17, 18, 19], labels)]
    card = add('LC2', 3, instruction + '\n' + '\n'.join(labels), rows, 'japanese-6-0', [4], [5],
               figure=crop('ja-2010-hl-lc2-map', 4, [.07, .58, .98, .955], instruction, 'aural'))
    card['sourceMaterial'] = source([4], 'source-question', 'aural')
    card['stem'] = stem


def listening_d():
    stem = join_cells('aural', 5, range(1, 8), 300)
    greeting = join_cells('aural', 5, [8, 9], 300)
    for suffix, qr in [('a', 11), ('b', 12)]:
        question = greeting + '\n' + cell('aural', 5, qr, 1)
        if suffix == 'a':
            rows = [point(s(6, 3, 1))]
        else:
            full = cell('scheme', 6, 4, 0).split('mother ', 1)[1].strip()
            partial = cell('scheme', 6, 5, 0)
            rows = [criterion(full, 1, [0, 0.5, 1], partial + ' This is the printed content partial; the general Japanese-language reduction explicitly excludes question 1(a) and (b).')]
        card = add('LD', 1, question, rows, 'japanese-6-0', [5], [6], suffix=suffix)
        card['stem'] = stem
    intro = join_cells('aural', 5, [13, 15], 300)
    add('LD', 2, intro + '\n' + cell('aural', 5, 18, 0), [point(s(6, 6, 2))], 'japanese-6-0', [5], [6], suffix='a')['stem'] = stem
    for suffix, qr, parts in [('i', 22, [(8, 0)]), ('ii', 23, [(9, 1), (10, 0)])]:
        answer = clean_tariff(selected(6, parts))
        if suffix == 'i':
            answer = answer.split(':', 1)[1].strip()
        question = intro + '\n' + join_cells('aural', 5, [20, 21], 300) + '\n' + cell('aural', 5, qr, 1)
        add('LD', 2, question, [point(answer, 2)], 'japanese-6-0', [5], [6], suffix='b-' + suffix)['stem'] = stem
    add('LD', 3, cell('aural', 5, 24, 1), [point(cell('scheme', 6, 11, 0).split('?', 1)[1].strip(), 2)], 'japanese-6-0', [5], [6])['stem'] = stem
    rows = [point(clean_tariff(cell('scheme', 6, row, group)), contextNote=label) for row, group, label in [
        (14, 0, 'First day'), (16, 0, 'Second day'), (14, 1, 'Starting time'), (16, 1, 'Finishing time'), (15, 1, 'Location')]]
    instruction = join_cells('aural', 5, [25, 26], 300)
    card = add('LD', 4, instruction + '\n' + cell('aural', 5, 28), rows, 'japanese-6-0', [5], [6],
               figure=crop('ja-2010-hl-ld-table', 5, [.07, .595, .97, .72], instruction, 'aural'))
    card['stem'] = stem
    for suffix, qr, sr in [('a', 32, 18), ('b', 33, 19)]:
        question = join_cells('aural', 5, [29, 30, 31], 300) + '\n' + cell('aural', 5, qr, 1)
        add('LD', 5, question, [point(s(6, sr, 1))], 'japanese-6-0', [5], [6], suffix=suffix)['stem'] = stem
    add('LD', 6, cell('aural', 5, 34, 1), [point(s(6, 21), 2)], 'japanese-6-0', [5], [6])['stem'] = stem


def writing_criterion(identity, label, maximum, permitted, guidance):
    return {'id': identity, 'label': label, 'maxMarks': maximum, 'permittedMarks': permitted, 'guidance': guidance}


def find_source_row(page, fragment, occurrence=0):
    matches = [i for i, row in enumerate(ROWS['scheme'][page - 1]) if fragment in ' '.join(group[2] for group in row)]
    assert len(matches) > occurrence, (page, fragment, matches)
    return cell('scheme', page, matches[occurrence])


def writing_expression(question):
    page = 12 if question == 5 else 14
    maximum, lower, threshold, length = (20, 15, 10, 150) if question == 5 else (30, 20, 15, 200)
    parts = [(9, 1), *[(i, 0) for i in range(10, 13 if question == 5 else 14)]]
    clause = selected(page, parts)
    normal_ranges = [(0, 5), (6, 14), (15, 20)] if question == 5 else [(0, 7), (8, 20), (21, 30)]
    lower_ranges = [(0, 3), (4, 10), (11, 15)] if question == 5 else [(0, 4), (5, 12), (13, 20)]
    tariff_rows = [17, 25, 34] if question == 5 else [18, 26, 35]
    description_rows = [(16, 24), (24, 33), (33, 41)] if question == 5 else [(17, 25), (25, 34), (34, 42)]
    bands, lower_bands = [], []
    for index, (tariff_row, (first, end)) in enumerate(zip(tariff_rows, description_rows)):
        descriptor = join_cells('scheme', page, range(first, end), 180)
        for target, ranges, group in [(bands, normal_ranges, 1), (lower_bands, lower_ranges, 0)]:
            low, high = ranges[index]
            target.append({'label': cell('scheme', page, tariff_row, group),
                           'marks': list(range(low, high + 1)), 'guidance': [descriptor]})
    instructions = selected(page, [(row, None) for row in range(1, 9)])
    global_view = selected(page, [(row, None) for row in ([41, 42] if question == 5 else [42, 43])])
    expression = writing_criterion('expression', 'Expression', maximum, list(range(maximum + 1)), [clause, instructions, global_view])
    expression['bands'] = bands
    expression['limits'] = [{'id': 'lower-expression', 'scaleLabel': 'Lower E', 'maxMarks': lower,
        'when': {'any': [
            {'criterionIds': ['discretionary'] if question == 5 else [], 'atMost': threshold, 'includeSelectedGroupMarks': True},
            {'length': 'characters', 'below': length},
        ]}, 'guidance': [clause], 'bands': lower_bands}]
    return expression


def writing():
    # The four slots record distinct selected questions, not combinations of
    # questions. The specially priced school response has the only split route.
    instruction = join_cells('paper', 12, [1, 2], 260)
    option_a = join_cells('paper', 12, range(3, 9), 300) + '\n' + '\n'.join(p(12, r) for r in range(10, 16))
    option_i = cell('paper', 12, 17, 1) + '\n' + join_cells('paper', 12, range(18, 21), 300) + '\n' + '\n'.join(p(12, r) for r in range(22, 28))
    question = instruction + '\n' + option_a + '\n' + english(p(12, 16)) + '\n' + option_i
    allocation = find_source_row(11, 'Any four points, 4 marks each.')
    discretionary = find_source_row(11, 'Discretionary marks (4 marks)', 0)
    school_rows = [i for i, row in enumerate(ROWS['scheme'][10]) if '2 marks' in ' '.join(group[2] for group in row)]
    assert school_rows
    school_tariff = selected(11, [(row, None) for row in school_rows])
    first = {'id': 'first', 'label': 'First selected response', 'alternativeSet': 'first-response', 'rows': [],
             'criteria': [writing_criterion('first-answer', 'Complete first response', 4, [0, 4], [allocation])]}
    school = {'id': 'school', 'label': 'School location and nearby places (option ア, question 2)',
              'alternativeSet': 'first-response', 'rows': [], 'criteria': [
                  writing_criterion('school-location', 'School location', 2, [0, 2], [school_tariff]),
                  writing_criterion('school-nearby', 'Nearby places', 2, [0, 2], [school_tariff]),
              ]}
    groups = [first, school] + [{'id': f'slot-{i}', 'label': f'Selected response {i}', 'rows': [],
        'criteria': [writing_criterion(f'answer-{i}', f'Complete response {i}', 4, [0, 4], [allocation])]} for i in [2, 3, 4]]
    guide = ('Choose one complete option, ア or イ, and identify four distinct questions from that option. '
             'Do not mix options or count the same question twice. If school question 2 is chosen, put it in the school route of the first slot; '
             'the ordinary first-slot route and school route cannot both count. Only the school question has a printed internal split. '
             'The expression threshold uses actual selected content plus the discretionary marks once.\n'
             + join_cells('scheme', 11, range(len(ROWS['scheme'][10]) - 1)))
    rubric = {'system': 'language-points', 'count': 4, 'groups': groups,
              'alternativeSets': [{'id': 'first-response', 'label': 'First selected response', 'sourceText': school_tariff, 'schemePages': [11]}],
              'allocationCap': {'maxMarks': 16, 'sourceText': allocation, 'schemePages': [11]},
              'criteria': [writing_criterion('discretionary', 'Discretionary content', 4, list(range(5)), [discretionary]), writing_expression(5)],
              'taskRequirements': [instruction], 'markingGuideNote': guide}
    add('5', None, question, [], 'japanese-5-7', [12], [11, 12], rubric=rubric, total=40)

    instruction = join_cells('paper', 16, [1, 2], 300)
    birthday = p(16, 3) + '\n' + p(16, 4) + '\n' + p(16, 5).split('/')[-1] + '\n' + p(16, 7)
    future = '\n'.join(cell('paper', 16, row, 0) for row in [8, 9, 10, 11, 13, 14])
    past = '\n'.join(cell('paper', 16, row, 2 if row == 11 else 1) for row in [8, 9, 10, 11, 13, 14])
    country = p(16, 16) + '\n' + p(16, 17) + '\n' + p(16, 18).split('/')[-1] + '\n' + join_cells('paper', 16, [21, 22]) + '\n' + '\n'.join(p(16, row) for row in range(23, 29))
    question = instruction + '\n' + birthday + '\n' + future + '\n' + p(16, 12) + '\n' + past + '\n' + english(p(16, 15)) + '\n' + country
    allocation = find_source_row(13, '5 marks each for any FOUR', 0)
    country_allocation = find_source_row(13, '5 marks each for any FOUR', 1)
    birthday_mark_rows = [i for i, row in enumerate(ROWS['scheme'][12]) if any(group[2] == '3 marks' for group in row)]
    assert len(birthday_mark_rows) == 1
    birthday_mark = cell('scheme', 13, birthday_mark_rows[0], 0)
    country_mark_rows = [i for i, row in enumerate(ROWS['scheme'][12]) if re.search(r'(?<!\d)5 marks\s*$', ' '.join(group[2] for group in row))]
    assert len(country_mark_rows) == 1
    country_mark = cell('scheme', 13, country_mark_rows[0])
    birthday_discretion = find_source_row(13, 'Discretionary marks (7 marks)')
    country_discretion = find_source_row(13, 'Discretionary marks (5marks)')
    groups = []
    for identity, label, required, mandatory_guide, pool_guide, discretion, discretionary_guide in [
        ('birthday', 'ア — birthday option', 3, birthday_mark, allocation, 7, birthday_discretion),
        ('country', 'イ — country option', 5, country_mark, country_allocation, 5, country_discretion),
    ]:
        groups.append({'id': identity, 'label': label, 'rows': [], 'criteria': [
            writing_criterion(identity + '-required', 'Required part (i)', required, [0, required], [mandatory_guide]),
            writing_criterion(identity + '-selected', 'Four distinct questions in part (ii)', 20, [0, 5, 10, 15, 20], [pool_guide]),
            writing_criterion(identity + '-discretionary', 'Discretionary content', discretion, list(range(discretion + 1)), [discretionary_guide]),
        ]})
    rubric = {'system': 'language-points', 'count': 1, 'groups': groups, 'criteria': [writing_expression(6)],
        'taskRequirements': [instruction], 'markingGuideNote':
        'Select one whole option. Within it, complete part (i) and any four distinct part (ii) questions. '
        'For ア, use one of the printed future/past versions, without mixing or crediting a question twice. '
        'The paper’s future gift prompt literally prints プレセント; it is retained unchanged. '
        'All content and discretionary marks belong to the selected option; expression uses that selected total once. '
        'The scheme’s later numbering reference is retained as printed and does not replace the six actual prompts.\n'
        + join_cells('scheme', 13, range(len(ROWS['scheme'][12]) - 1))}
    add('6', None, question, [], 'japanese-5-7', [16], [13, 14], rubric=rubric, total=60)


def scheme_row(page, fragment):
    matches = [i for i, row in enumerate(ROWS['scheme'][page - 1]) if fragment in ' '.join(group[2] for group in row)]
    assert len(matches) == 1, (page, fragment, matches)
    return matches[0]


def reading_q1():
    instruction = join_cells('paper', 3, [0, 1], 300)
    questions = [join_cells('paper', 3, rows, 300) for rows in [[3, 4], [5], [6], [7], [9, 10], [11], [12]]]
    rows = [point(s(7, 4 + i, 1), contextNote=question) for i, question in enumerate(questions)]
    card = add('1AA', None, instruction + '\n' + '\n'.join(questions), rows, 'japanese-5-0', [3], [7], reading=[2],
               figure=crop('ja-2010-hl-web-buttons', 2, [.045, .015, .965, .98], 'Original webpage with numbered buttons'))
    card['questionFigureIncludesPrompt'] = False
    group_rows(card, [(str(i + 1), question, i, i + 1) for i, question in enumerate(questions)])
    instruction = join_cells('paper', 3, [13, 14], 300)
    for q, qrows in [(1, [15, 16, 17]), (2, [18, 19]), (3, [22, 23]), (4, [25, 26]), (5, [28, 29])]:
        question = join_cells('paper', 3, qrows, 300)
        if q == 1:
            rows = [point(s(7, 12, 1), 2, contextNote=cell('paper', 3, 16, 2)), point(s(7, 13, 1), 2, contextNote=cell('paper', 3, 17, 2))]
        elif q == 2:
            grape = clean_tariff(cell('scheme', 7, 15, 0)).removeprefix('(i) ')
            italian, peach = cell('scheme', 7, 15, 1).removeprefix('(ii) ').split('1 mark', 1)
            rows = [point(grape, 2), point(italian.strip()), point(clean_tariff(peach))]
        elif q == 3:
            rows = [point(selected(7, [(17, 0), (17, 1)]), 2)]
        else:
            rows = [point(s(7, 18 if q == 4 else 19, 1), 2)]
        card = add('1AB', q, question, rows, 'japanese-5-0', [3], [7], reading=[2])
        card['stem'] = instruction
        if q == 2:
            group_rows(card, [('grape', 'First other flavour', 0, 1), ('italian-peach', 'Second other flavour', 1, 3)])
    instruction = cell('paper', 3, 31, 1)
    for q, qr, needle in [(1, 32, 'コカコーラ'), (2, 34, 'ファンタ')]:
        row = scheme_row(7, needle)
        answer = next(group[2] for group in ROWS['scheme'][6][row] if needle in group[2])
        # Record the exact chosen group rather than a typed replacement.
        group = next(i for i, entry in enumerate(ROWS['scheme'][6][row]) if entry[2] == answer)
        card = add('1AC', q, p(3, qr), [point(clean_tariff(cell('scheme', 7, row, group)), 2)], 'japanese-5-0', [3], [7], reading=[2])
        card['stem'] = instruction
    table_start = scheme_row(7, 'drinks Coca Cola Catechin after meals')
    question = join_cells('paper', 4, [22, 23], 300)
    labels = [cell('paper', 4, r, 0) for r in [28, 30, 32]]
    rows = []
    for index, label in enumerate(labels):
        sr = table_start + index * 2
        groups = ROWS['scheme'][6][sr]
        date_group = next(i for i, value in enumerate(groups) if re.fullmatch(r'\d+/\d+/\d+', value[2]))
        rows.extend([point(cell('scheme', 7, sr, date_group), contextNote=label + ' — date (dd/mm/yyyy)'),
                     point(cell('scheme', 7, sr, date_group + 1), contextNote=label + ' — day of the week')])
    card = add('1B', 1, question + '\n' + '\n'.join(labels), rows, 'japanese-5-0', [4], [7], reading=[4])
    group_rows(card, [(str(i + 1), labels[i], i * 2, i * 2 + 2) for i in range(3)])
    for q, qrows, needle in [(2, [33, 34], 'What does Yuka prefer'), (3, [36, 37], 'Who likes Coca Cola Plus Catechin')]:
        sr = scheme_row(7, needle)
        add('1B', q, join_cells('paper', 4, qrows, 300), [point(clean_tariff(cell('scheme', 7, sr, 1)), 2)], 'japanese-5-0', [4], [7], reading=[4])


def reading_q2():
    start = len(CARDS)
    discrepancy = ('The scheme’s section headings give A=5, B=10 and C=6, while its individual task tariffs give A=4, B=8 and C=9. '
                   'Both sets total 29 with D=8. These cards retain the individual printed task tariffs; no missing mark is invented.')
    for q, needle in [(1, '少な'), (2, 'ほうがいいですか')]:
        # The first question's ruby interrupts 少ない in the row extraction;
        # its numbered opening binds the answer cell without normalizing it.
        sr = scheme_row(8, '1. 日本は' if q == 1 else needle) + 1
        card = add('2A', q, p(7, 1 + q, 0).rstrip('_').rstrip(), [point(s(8, sr), 2)], 'japanese-5-0', [7], [8], reading=[6])
        card['stem'] = join_cells('paper', 7, [0, 1], 300)
    for q, qrows, needle in [(1, [6, 7], 'Look up.'), (2, [9], 'Don’t drive.'),
                            (3, [11, 12], 'Water / money'), (4, [14, 15], 'English / Chinese')]:
        sr = scheme_row(8, needle)
        answer = cell('scheme', 8, sr, 0)
        if q <= 2:
            rows = [point(answer, 2)]
        else:
            allocation = cell('scheme', 8, sr + 1, 0)
            rows = [criterion(answer, 2, [0, 1, 2], allocation + ' Assess the complete three-item response once: one correct item earns 0; two earn 1; three earn 2. The items are not separately priced.')]
        card = add('2B', q, join_cells('paper', 7, qrows, 300), rows, 'japanese-5-0', [7], [8], reading=[6])
        card['stem'] = join_cells('paper', 7, [4, 5], 300)
    instruction = join_cells('paper', 7, [17, 18, 19, 20], 300)
    for q, qr, needle in [(1, 21, 'Please get off'), (2, 23, 'Please go to high'), (3, 25, 'Please listen to the news')]:
        card = add('2C', q, p(7, qr), [point(s(8, scheme_row(8, needle)), 3)], 'japanese-5-3', [7], [8], reading=[6])
        card['stem'] = instruction
    meaning_start = scheme_row(8, '1. foreigner')
    rows = [point(re.sub(r'^\d+\.\s*', '', s(8, meaning_start + i)), contextNote=label) for i, label in enumerate(['(i)', '(ii)', '(iii)', '(iv)'])]
    question = join_cells('paper', 7, [28, 29], 300) + '\n' + '\n'.join(p(7, r) for r in [30, 31, 32])
    add('2D', 1, question, rows, 'japanese-5-4', [7], [8], reading=[6],
        figure=crop('ja-2010-hl-2d-meaning', 7, [.045, .67, .965, .835], question))
    rows = []
    for i in range(4):
        literal = s(8, meaning_start + 4 + i)
        match = re.search(r'[（(]([^）)]+)[）)]', literal)
        assert match and len(match.group(1)) == 1, literal
        rows.append(point(match.group(1), contextNote=f'({["i", "ii", "iii", "iv"][i]}) — Fill only the kanji’s reading; the following okurigana is already given. Printed scheme: {literal}'))
    question = cell('paper', 7, 33, 1) + '\n' + '\n'.join(p(7, r) for r in [34, 35, 36])
    add('2D', 2, question, rows, 'japanese-5-4', [7], [8], reading=[6],
        figure=crop('ja-2010-hl-2d-reading', 7, [.045, .837, .965, .963], question))
    for card in CARDS[start:]:
        card['stem'] = card.get('stem', '') + '\n' + discrepancy


def grammar():
    start = scheme_row(10, 'Question 4')
    boundary = scheme_row(10, 'B:  8 marks')
    answer_rows = [i for i in range(start + 1, boundary) if any(group[2] == '2 marks' for group in ROWS['scheme'][9][i])]
    assert len(answer_rows) == 6
    labels = [p(11, row, 0) for row in range(7, 13)]
    rows = [point(re.sub(r'^\d+\.\s*', '', cell('scheme', 10, sr, 0)), 2, contextNote=label) for sr, label in zip(answer_rows, labels)]
    question = join_cells('paper', 11, range(1, 5), 300) + '\n' + p(11, 6) + '\n' + '\n'.join(labels)
    add('4A', None, question, rows, 'japanese-5-5', [11], [10], reading=[8])
    answer_rows = [i for i in range(boundary + 1, len(ROWS['scheme'][9])) if any(group[2] == '1 mark' for group in ROWS['scheme'][9][i])]
    assert len(answer_rows) == 8
    rows = [point(cell('scheme', 10, sr, 1), contextNote=f'Blank ({index + 1})') for index, sr in enumerate(answer_rows)]
    instruction = cell('paper', 11, 13, 1)
    sentences = [p(11, row) for row in range(14, 19)]
    question = instruction + '\n' + '\n'.join(sentences)
    card = add('4B', None, question, rows, 'japanese-5-5', [11], [10])
    group_rows(card, [(str(i + 1), sentences[i], start, end)
                      for i, (start, end) in enumerate([(0, 1), (1, 3), (3, 4), (4, 6), (6, 8)])])


def reading_q3():
    rule = selected(9, [(1, 0), (2, 0), (3, 0)])
    guide = (rule + ' These are manually assessed response marks. Award the full printed amount only for otherwise correct content; '
             'use its half value only when a printed condition applies to that response. Apply that half award once, without recursive or compounded quartering. '
             'Do not reduce another unaffected response, and do not award the half value for arbitrary incorrect content.')
    def assessed(text, maximum, label):
        return criterion(text, maximum, [0, maximum / 2, maximum], label + '. ' + guide)
    start = len(CARDS)
    for q in range(1, 10):
        question = p(9, 2 * q)
        if q == 2:
            components = [text.strip(' ・') for text in split_marks(cell('scheme', 9, 8, 0))]
            assert len(components) == 2
            rows = [assessed(text, 1, f'Content component {index + 1}') for index, text in enumerate(components)]
        elif q == 9:
            pool = selected(9, [(22, 0), (23, 0)])
            allocation = cell('scheme', 9, 24, 0)
            rows = [assessed(pool, 1, f'Distinct action {i} of 2. {allocation}. Record two different actions only; the two printed sentence forms are alternatives for the same actions, not additional facts') for i in [1, 2]]
        else:
            rows = [assessed(s(9, 4 + 2 * q), 2, f'Question {q}')]
        card = add('3A', q, question, rows, 'japanese-5-1', [9], [9], reading=[8])
        card['stem'] = join_cells('paper', 9, [0, 1], 300)
        if q == 4:
            card['rows'][0]['contextNote'] += ' The scheme literally prints full-size イ in デイズニーランド and the question-ending か。; the paper’s passage uses ディズニーランド. Both source forms are retained, without silently rewriting the key.'
    first_question = join_cells('paper', 9, [24, 25], 300)
    second_question = join_cells('paper', 9, [27, 28], 300)
    first = assessed(s(9, 27), 1, first_question)
    second = assessed(selected(9, [(29, 0), (30, 0)]), 2, second_question + '. ' + cell('scheme', 9, 31, 0) + ' earns 2; its 1-mark setting is solely the printed half award, not a separate base partial')
    bonus_text = cell('scheme', 9, 32, 0)
    variants = []
    for under in [1, 2]:
        bonus = assessed(bonus_text, 1, f'The single discretionary mark is assigned under question {under}; apply the same printed response condition to this bonus. It is awarded only once across the joint task')
        variants.append({'id': f'bonus-under-{under}', 'label': f'Discretionary mark under question {under}',
                         'rows': [dict(row, id=f'r-{i + 1}') for i, row in enumerate([first, second, bonus])]})
    card = add('3B', None, first_question + '\n' + second_question, variants[0]['rows'], 'japanese-5-6', [9], [9], reading=[8])
    card['stem'] = join_cells('paper', 9, range(20, 24), 300)
    card['answerVariants'] = variants
    rows = []
    for i in range(1, 8):
        reading = re.sub(r'^\d+\.\s*', '', cell('scheme', 10, i, 0))
        rows.extend([assessed(reading, 1, f'Item {i} — reading'), assessed(cell('scheme', 10, i, 2), 1, f'Item {i} — meaning')])
    question = join_cells('paper', 10, range(4), 300) + '\n' + '\n'.join(p(10, row) for row in range(4, 13))
    card = add('3C', None, question, rows, 'japanese-5-4', [10], [10], reading=[8],
               figure=crop('ja-2010-hl-3c-kanji', 10, [.045, .025, .97, .47], question))
    group_rows(card, [(str(i + 1), f'Item {i + 1}: reading and meaning', i * 2, i * 2 + 2) for i in range(7)])
    for card in CARDS[start:]:
        card['sourceEvidence']['generalSchemePages'] = [9]
        assert 'answerLanguageRule' not in card and 'extraneousMaterialRule' not in card


def build():
    reading_q1(); reading_q2(); reading_q3(); grammar(); writing()
    listening_a(); listening_b(); listening_c(); listening_d()
    census = json.loads((Path(__file__).parent / 'reviews/japanese-2010-hl-census.json').read_text())
    expected = {'ja-2010-hl-' + '-'.join(str(part).lower() for part in task['key'] if part is not None): task for task in census['tasks']}
    assert set(expected) == {card['id'] for card in CARDS}, (set(expected) - {card['id'] for card in CARDS}, {card['id'] for card in CARDS} - set(expected))
    for card in CARDS:
        task = expected[card['id']]
        assert card['totalMarks'] == task['marks'], (card['id'], card['totalMarks'], task['marks'])
        assert card['sourceEvidence']['paperPages'] == task['paperPages'], card['id']
        assert card['sourceEvidence']['schemePages'] == task['schemePages'], card['id']
        assert card['questionRef'] == task.get('paperRef', card['questionRef']), card['id']
        rubric = card.get('rubric', {})
        for item in rubric.get('criteria', []) + [item for group in rubric.get('groups', []) for item in group.get('criteria', [])]:
            guidance = item.get('guidance', []) + [text for band in item.get('bands', []) for text in band['guidance']]
            guidance += [text for limit in item.get('limits', []) for text in limit['guidance']]
            guidance += [text for limit in item.get('limits', []) for band in limit.get('bands', []) for text in band['guidance']]
            assert all(text.strip() for text in guidance), (card['id'], item['id'], 'Empty source guidance')
    assert len(CARDS) == 66
    assert sum(card['totalMarks'] for card in CARDS) == 300
    assert sum('answerLanguageRule' in card for card in CARDS) == 40
    assert not any('extraneousMaterialRule' in card for card in CARDS)
    assert '\ufffd' not in json.dumps([CARDS, EVIDENCE], ensure_ascii=False)
    recovery = ROOT / 'scripts/markbank/authoring/glyphmap-japanese-2010-hl.json'
    return {'subjectId': 'japanese', 'sitting': '2010-hl', 'reviewedAt': '2026-11-12',
            'sources': [{'document': name, 'path': str(path.relative_to(ROOT)), 'sha256': PINNED_SOURCES[path],
                         'pagesReviewed': list(range(1, len(DOCS[name]) + 1))} for name, path in [('paper', PAPER), ('aural', AURAL), ('scheme', SCHEME)]],
            'glyphRecovery': {'path': str(recovery.relative_to(ROOT)), 'sha256': hashlib.sha256(recovery.read_bytes()).hexdigest()},
            'cards': CARDS, 'selectors': EVIDENCE, 'status': 'source-captured', 'choiceAnalysis': census['choiceBoundaries'], 'consolidations': []}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    result = build()
    if args.write:
        assert all(figure['md5'] for figure in FIGURES.values()), 'Render each planned source crop in a separate guarded slot before publication'
        scheme_text = ''.join(f'\n## Page {i + 1}\n\n' + page.get_text(sort=True) for i, page in enumerate(DOCS['scheme']))
        scheme_text += '\n## Original text with source-proven glyph recovery and furigana folded at its printed character\n'
        scheme_text += ''.join(f'\n### Physical page {i + 1}\n\n' + '\n'.join(' '.join(group[2] for group in row) for row in rows) + '\n' for i, rows in enumerate(ROWS['scheme']))
        # The source table's adjacent English columns merge in a few row groups.
        # Retain a second literal column reading for the provenance gate.
        for page, x_ranges in [(3, [(50, 114), (114, 156), (156, 242), (242, 341), (341, 426), (426, 550)])]:
            scheme_text += f'\n## Original table columns — physical page {page}\n'
            scheme_text += '\n'.join(DOCS['scheme'][page - 1].get_text(clip=fitz.Rect(x0, 0, x1, DOCS['scheme'][page - 1].rect.height), sort=True) for x0, x1 in x_ranges)
        SCHEME.with_suffix('.md').write_text(scheme_text.rstrip() + '\n')
        (ROOT / 'scripts/markbank/authoring/reviews/japanese-2010-hl.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
        manifest = ROOT / 'components/MarkBank/figures-japanese.json'
        previous = json.loads(manifest.read_text()); previous.update(FIGURES)
        manifest.write_text(json.dumps(previous, ensure_ascii=False, indent=2) + '\n')
    (ROOT / 'tmp/japanese-review/2010-hl-draft.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    (ROOT / 'tmp/japanese-review/2010-hl-crop-plan.json').write_text(json.dumps(FIGURES, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'cards': len(CARDS), 'marks': sum(card['totalMarks'] for card in CARDS), 'figures': len(FIGURES)}, indent=2))
