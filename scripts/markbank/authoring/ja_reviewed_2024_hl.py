#!/usr/bin/env python3
"""2024 Higher Japanese, independently reviewed against all original pages.

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
PAPER = ROOT / 'examiner-reports/japanese/papers/2024-hl-000-paper.pdf'
AURAL = ROOT / 'examiner-reports/japanese/papers/2024-hl-A00-paper.pdf'
SCHEME = ROOT / 'examiner-reports/japanese/schemes/2024-hl.pdf'
PINNED_SOURCES = {
    PAPER: '4e0c6178a0f00657cfefee31b38456b21ed6acdff8e249d7a143ea06d858a0c6',
    AURAL: '84e83ebc5b2f4fdfdc2de0b05b31b43c581694211e053d7cf92279005845b3b5',
    SCHEME: 'c3eeadd3fca460b978cb366815b07b3cb303626626714481a1163247550a56b2',
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
    return {'kind': kind, 'label': '2024 Japanese Higher Level', 'title': 'Original examination material',
            'pages': pages, 'attribution': '© State Examinations Commission.',
            **({'presentationNote': FURIGANA_NOTE} if component == 'paper' else {}),
            '_component': component}


def add(section, q, question, rows, topic, paper_pages, scheme_pages, suffix='', rubric=None, total=None, reading=None, figure=None):
    cid = f'ja-2024-hl-{section.lower()}' + (f'-{q}' if q is not None else '') + (f'-{suffix}' if suffix else '')
    ref = f'2024 HL Section {section}' + (f' Q{q}' if q is not None else '')
    if suffix:
        ref += ''.join(f'({part})' for part in suffix.split('-'))
    listening = section.startswith('L')
    card = {'id': cid, 'source': 'sec', 'subjectId': 'japanese', 'specVersion': 'lc-japanese-syllabus',
            'kind': 'rubric' if rubric else 'question', 'level': 'higher', 'year': 2024,
            'section': section[1:] if listening else section[0] if section[0] in '1234' else 'Q5',
            'topicId': topic, 'conceptId': concept_for(question, cid), 'questionRef': ref,
            'questionText': question, 'totalMarks': total if total is not None else sum(map(worth, rows)),
            'qa': {'gates': ['verbatim', 'tariff', 'figure'], 'humanReviewedBy': 'agent-verified', 'humanReviewedAt': '2026-11-09'},
            'sourceEvidence': {'component': 'aural' if listening else 'paper', 'paperPages': paper_pages, 'schemePages': scheme_pages},
            'schemeCitation': 'Marking points quoted from the SEC marking scheme, Japanese 2024 Higher Level — © State Examinations Commission.'}
    if rubric:
        card['rubric'] = rubric
    else:
        card['tariffModel'] = {'kind': 'fixed'}
        card['rows'] = [dict(row, id=f'r-{i + 1}') for i, row in enumerate(rows)]
    original_ids = set(re.findall(r'    id: "([^"]+)"', (ROOT / 'components/MarkBank/cards/japanese/higher.ts').read_text()))
    if cid in original_ids:
        card['qa']['gates'].append('reviewed-card-correction')
    # Every condition is local to its printed heading. In 2024 the
    # extraneous-material clauses do not also name an answer language.
    if listening or section == '1B':
        page, row = (3, 1) if listening else (7, 0)
        card['sourceEvidence']['generalSchemePages'] = [page]
        card['answerLanguageRule'] = {'otherLanguageMultiplier': 0.5, 'penalizedLanguage': 'Japanese',
                                      'sourceText': cell('scheme', page, row), 'schemePages': [page]}
    if (section == '2A' and q == 3) or section == '3B':
        page, row = (7, 39) if section == '2A' else (10, 0)
        card['sourceEvidence']['generalSchemePages'] = [page]
        card['extraneousMaterialRule'] = {'multiplier': 0.5, 'sourceText': cell('scheme', page, row), 'schemePages': [page]}
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
    topic = {'1': 'japanese-5-0', '2': 'japanese-5-0', '3': 'japanese-5-1'}[section[0]]
    text = prompt(page, question_rows)
    if section == '3B':
        text = p(page, question_rows[0], 1)
    if section == '2A' and q == 3:
        text = re.sub(r'^\([ivx]+\)\s*', '', ' '.join(p(page, row, 1) if len(ROWS['paper'][page - 1][row]) > 1 else p(page, row) for row in question_rows))
    card = add(section, q, text, rows, topic, [page], scheme_pages, suffix or '', total=total,
               reading={'1A': [2], '1B': [4], '2A': [6], '3A': [10], '3B': [10]}[section])
    if section == '2A':
        card['stem'] = english(p(7, 24 if q == 3 else 10, 1))
    else:
        row = {'1A': 0, '1B': 16, '3A': 0, '3B': 21}[section]
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
    labels = [p(3, row, 0) + ' ' + english(p(3, row, 1)) for row in range(4, 10)]
    rows = [point(s(6, row, 1 if row == 6 else 2), contextNote=label) for row, label in zip(range(4, 10), labels)]
    add('1A', 1, instruction + '\n' + p(3, 3, 0) + ' ' + p(3, 3, 1) + '\n' + '\n'.join(labels), rows, 'japanese-5-0', [3], [6], reading=[2, 3])
    comprehension('1A', 2, 'i', [10, 11], [point(s(6, 12), 2)], [6])
    comprehension('1A', 2, 'ii', [13, 14], [point(s(6, 14))], [6])
    comprehension('1A', 2, 'iii', [16], [anyn(options(6, [16], '/'), 1)], [6])
    who = [part.strip(' ,') for part in cell('scheme', 6, 18, 0).split('(1 mark)') if part.strip(' ,')]
    comprehension('1A', 3, 'i', [18, 19], [point(part) for part in who], [6])
    table = comprehension('1A', 3, 'ii', [21], [point(s(6, row, group), contextNote=s(6, labelrow)) for row, group, labelrow in [(22, 0, 21), (24, 0, 23), (25, 1, 25), (26, 0, 27)]], [6])
    table['questionText'] += '\n' + english(p(3, 22, 0)) + ' / ' + english(p(3, 22, 1)) + '\n' + '\n'.join(p(3, row) for row in range(23, 27))
    table['questionFigureKey'] = crop('ja-2024-hl-1a-3-ii', 3, [.07, .575, .83, .76], table['questionText'])
    comprehension('1A', 4, 'i', [27, 28], [point(s(6, 29), 2)], [6])
    comprehension('1A', 4, 'ii', [30, 31], [anyn(options(6, [31, 32]), 2)], [6])
    comprehension('1B', 1, 'i', [17], [anyn(options(7, [2, 3]), 3)], [7])
    tired, cause = cell('scheme', 7, 5, 0).split(' (1 mark) ', 1)
    comprehension('1B', 1, 'ii', [21, 22], [point(tired), point(re.sub(r'\s*\(1 mark\)$', '', cause))], [7])
    comprehension('1B', 2, 'i', [24, 25], [anyn(options(7, [7], '/'), 1, 2)], [7])
    comprehension('1B', 2, 'ii', [27], [point(s(7, 9))], [7])
    no, reason = s(7, 11).split(' (1 mark), ')
    comprehension('1B', 2, 'iii', [29, 30], [point(no), point(reason)], [7])

    office_heading = p(7, 2, 0).split('/')[1].split('chosnaíonn')[0].strip() + ' ' + p(7, 3, 0)
    cost_heading = p(7, 2, 0).rsplit('/', 1)[1].strip() + ' ' + p(7, 3, 1)
    intended_heading = p(7, 2, 1)
    tokyo, kimono = p(7, 4), english(p(7, 8) + ' ' + p(7, 9))
    question = english(p(7, 0, 1)) + '\n' + ' / '.join([office_heading, cost_heading, intended_heading]) + '\n' + tokyo + ' — ' + p(7, 5) + '\n' + kimono
    who_tokyo = ' '.join([s(7, 17, 2), s(7, 18, 1), s(7, 19, 1), s(7, 20)])
    who_kimono = ' '.join([s(7, 21, 1), s(7, 22, 3), s(7, 23, 2)])
    # The two printed slash-separated routes are alternatives for the same
    # two-mark cell, unlike Tokyo Kart's explicit any-two detail allocation.
    rows = [point(s(7, 17, 1), contextNote=tokyo + ' — ' + cost_heading),
            anyn(strip_tariff(who_tokyo).split(', '), 2, contextNote=tokyo + ' — ' + intended_heading),
            point(s(7, 22, 1), contextNote=kimono + ' — ' + office_heading),
            point(s(7, 22, 2), contextNote=kimono + ' — ' + cost_heading),
            anyn([part.strip() for part in who_kimono.split('/')], 1, 2, contextNote=kimono + ' — ' + intended_heading)]
    add('2A', 1, question, rows, 'japanese-5-0', [7], [7], reading=[6, 7],
        figure=crop('ja-2024-hl-2a-1', 7, [.06, .03, .99, .23], question))
    route, other = s(7, 26).split('(any 2 landmarks), ', 1)
    tour = [route.strip() + ' (any 2 landmarks)', other.rstrip(','), *options(7, [27])]
    comprehension('2A', 2, 'i', [11, 12], [anyn(tour, 2, 2, [2, 1], contextNote=cell('scheme', 7, 28, 0))], [7])
    restrictions = strip_tariff(s(7, 30)).split(', ')
    smoke, footwear = restrictions.pop().split(' wear ', 1)
    restrictions += [smoke, 'wear ' + footwear]
    comprehension('2A', 2, 'ii', [14, 15], [anyn(restrictions, 2, 2, [2, 1])], [7])
    comprehension('2A', 2, 'iii', [17], [anyn(options(7, [33]), 2)], [7])
    rental = strip_tariff(' '.join(s(7, row) for row in [35, 36]))
    sizes, rest = rental.split('; ', 1)
    colours, rest = rest.split(' etc kimonos, ', 1)
    hair, deadline = rest.split(', return', 1)
    comprehension('2A', 2, 'iv', [19], [anyn([sizes, colours + ' etc kimonos', hair, 'return' + deadline], 2, 2, [2, 1])], [7])
    comprehension('2A', 2, 'v', [21, 22], [anyn(options(7, [38], '/'), 1, 2)], [7])
    for roman, qr, sr in [('i', 25, 1), ('ii', 27, 3), ('iii', 29, 5)]:
        comprehension('2A', 3, roman, [qr], [point(s(8, sr), 2)], [8])
    translation = ' '.join(cell('scheme', 8, row, 0) for row in [8, 9])
    translation_parts = [part.strip(' ,') for part in translation.split('(1 mark)') if part.strip(' ,')]
    add('2A', 4, prompt(7, [31]) + '\n' + p(7, 32) + ' ' + p(7, 33), [point(part.removeprefix('and ')) for part in translation_parts], 'japanese-5-0', [7], [8], reading=[6])
    for section, page, scheme_page in [('2B', 8, 8), ('2C', 9, 9)]:
        for q, instrrows, itemrows, answerrows in [(1, [1, 2], range(4, 10), range(13, 19) if section == '2B' else range(2, 8)), (2, [10, 11], range(13, 19), range(20, 26) if section == '2B' else range(9, 15))]:
            instruction = prompt(page, instrrows)
            labels = [p(page, row, 0) + ' ' + p(page, row, 1) for row in itemrows]
            # For finite word pools the question carries every original item;
            # marking options preserve the scheme's numbered answer wording.
            options_with_markers = [cell('scheme', scheme_page, row, 0) + ' ' + s(scheme_page, row, 1) for row in answerrows]
            add(section, q, instruction + '\n' + '\n'.join(labels), [anyn(options_with_markers, 5)],
                'japanese-5-4' if section == '2B' else 'japanese-5-5', [page], [scheme_page], reading=[page],
                figure=crop(f'ja-2024-hl-{section.lower()}-{q}', page, [.06, .05 if q == 1 else (.485 if section == '2B' else .465), .96, (.485 if section == '2B' else .46) if q == 1 else .91], instruction))

    for q, qr, answers, quota, marks in [(1, [1, 2], options(9, [18]), 3, 1), (2, [5, 6], options(9, [21]), 2, 1), (3, [9], options(9, [24], '/'), 1, 2), (4, [12, 13], options(9, [27, 28]), 3, 1), (5, [16], options(9, [31]), 2, 1), (6, [19], options(9, [33]), 2, 1)]:
        comprehension('3A', q, None, qr, [anyn(answers, quota, marks)], [9])
    for q, qr, sr, marks in [(1, 22, 2, 1), (2, 24, 4, 1), (3, 26, 6, 2)]:
        comprehension('3B', q, None, [qr], [point(s(10, sr), marks)], [10])
    room, reason = cell('scheme', 10, 8, 0).split(' (1 mark)   ')
    reason = re.sub(r'\s*\(1 mark\)\s*\(2 marks\)$', '', reason)
    comprehension('3B', 4, None, [28], [point(room), anyn([part.strip() for part in reason.split('/')], 1)], [10])
    instruction = prompt(12, [1, 2, 3])
    groups = []
    for i, row in enumerate(range(6, 12), 1):
        # The original PDF merges table columns inconsistently; select the
        # complete source row and split at its printed first one-mark tariff.
        original = re.sub(r'^\([ivx]+\)\s*', '', cell('scheme', 10, i + 9))
        reading_answer, meaning = original.split('(1 mark)', 1)
        meaning = re.sub(r'\s*\(1 mark\)\s*$', '', meaning).strip()
        groups.append({'id': f'item-{i}', 'label': re.sub(r'_+', '', p(12, row)).strip(), 'rows': [
            {'id': 'reading', 'text': re.sub(r'\s+', ' ', reading_answer).strip(), 'marks': 1},
            {'id': 'meaning', 'text': meaning, 'marks': 1}]})
    add('3C', None, instruction + '\n' + '\n'.join(group['label'] for group in groups), [], 'japanese-5-4', [12], [10],
        rubric={'system': 'language-points', 'count': 5, 'taskRequirements': [instruction], 'groups': groups, 'markingGuideNote': cell('scheme', 10, 9)}, total=10,
        reading=[12], figure=crop('ja-2024-hl-3c', 12, [.06, .03, .97, .455], instruction))
    instruction = prompt(12, [13, 14, 15])
    groups = []
    for row in range(17, 25):
        label = p(12, row - 1)
        original = re.sub(r'^\([ivx]+\)\s*', '', cell('scheme', 10, row))
        answers = [part.strip() for part in re.split(r'\(1 mark\)|(?<=\)) 1 mark$', original) if part.strip()]
        for blank, answer in enumerate(answers, 1):
            groups.append({'id': f'item-{len(groups) + 1}', 'label': label + (f' [{blank}]' if len(answers) > 1 else ''),
                           'rows': [{'id': 'particle', 'text': re.sub(r'\s+', ' ', answer), 'marks': 1}]})
    assert len(groups) == 12
    add('3D', None, instruction + '\n' + '\n'.join(p(12, row) for row in range(16, 24)), [], 'japanese-5-5', [12], [10],
        rubric={'system': 'language-points', 'count': 10, 'taskRequirements': [instruction], 'groups': groups,
                'markingGuideNote': cell('scheme', 10, 16)}, total=10,
        reading=[12], figure=crop('ja-2024-hl-3d', 12, [.06, .47, .97, .89], instruction))


def steps(maximum):
    return list(range(maximum + 1))


def writing():
    for q, pp, sp, maximum, threshold, length, lower, normal, reduced in [
        (4, 14, 12, 20, 10, 150, 15, [(0, 5), (6, 14), (15, 20)], [(0, 3), (4, 10), (11, 15)]),
        (5, 16, 14, 30, 15, 200, 20, [(0, 7), (8, 20), (21, 30)], [(0, 4), (5, 12), (13, 20)]),
    ]:
        bands, lower_bands = [], []
        ranges = [range(17, 25), range(25, 32), range(32, 39)] if q == 4 else [range(16, 24), range(24, 32), range(32, 39)]
        for i, rows in enumerate(ranges):
            guidance = [join_cells('scheme', sp, rows, 150)]
            for target, marks in [(bands, normal), (lower_bands, reduced)]:
                lo, hi = marks[i]
                target.append({'label': f'{lo}–{hi}', 'marks': list(range(lo, hi + 1)), 'guidance': guidance})
        rule = join_cells('scheme', sp, range(10, 14) if q == 4 else range(9, 13))
        if q == 4:
            instruction = prompt(14, [1, 2])
            question = instruction + '\n' + '\n'.join([
                '(a) ' + prompt(14, [3, 4, 5]), p(14, 6), p(14, 7), english(p(14, 8)),
                '(b) ' + prompt(14, [9, 10, 11]), p(14, 12), p(14, 13), english(p(14, 14)),
                '(c) ' + prompt(14, [15, 16, 17]), p(14, 18), p(14, 19)])
            criteria = [
                {'id': 'opening', 'label': 'Opening', 'maxMarks': 1, 'permittedMarks': [0, 1], 'guidance': [s(11, 17, 1)]},
                *[{'id': f'point-{i}', 'label': f'({i})', 'maxMarks': 9, 'permittedMarks': steps(9), 'guidance': [s(11, 16)]} for i in ['i', 'ii']],
                {'id': 'closing', 'label': 'Closing', 'maxMarks': 1, 'permittedMarks': [0, 1], 'guidance': [s(11, 18)]},
            ]
        else:
            instruction = prompt(16, range(1, 5))
            headings = [prompt(16, rows) for rows in [[5], [6, 7], [8, 9], [10, 11], [12, 13, 14], [15, 16], [17, 18], [19, 20]]]
            question = instruction + '\n' + '\n'.join(f'{i}. {heading}' for i, heading in enumerate(headings, 1))
            source_headings = [cell('scheme', 13, row) for row in range(9, 17)]
            criteria = [{'id': f'heading-{i}', 'label': f'Heading {i} you chose', 'maxMarks': 7, 'permittedMarks': steps(7), 'guidance': [s(13, 4)] + source_headings} for i in range(1, 5)]
            criteria.extend([
                {'id': 'opening', 'label': 'Opening', 'maxMarks': 1, 'permittedMarks': [0, 1], 'guidance': [s(13, 5, 1)]},
                {'id': 'closing', 'label': 'Closing', 'maxMarks': 1, 'permittedMarks': [0, 1], 'guidance': [s(13, 6)]},
            ])
        content_ids = [criterion['id'] for criterion in criteria]
        criteria.append({'id': 'expression', 'label': s(11, 19) if q == 4 else s(13, 7), 'maxMarks': maximum,
                         'permittedMarks': steps(maximum), 'guidance': [join_cells('scheme', sp, [39, 40])], 'bands': bands,
                         'limits': [{'id': 'lower-e', 'maxMarks': lower,
                                     'when': {'any': [{'criterionIds': content_ids, 'atMost': threshold}, {'length': 'characters', 'below': length}]},
                                     'bands': lower_bands, 'guidance': [rule]}]})
        add(str(q), None, question, [], 'japanese-5-7', [pp], [sp - 1, sp], total=maximum * 2,
            figure=crop(f'ja-2024-hl-{q}', pp, [.045, .015, .96, .92], question),
            rubric={'system': 'language-writing', 'taskRequirements': [instruction], 'criteria': criteria,
                    'markingGuideNote': 'Assess four different selected headings once each, using the printed content and expression grid.' if q == 5 else 'Assess the one option you answered. The same printed content and expression grid applies to all three options.'})


def listening():
    def aq(page, rows):
        return re.sub(r'^(?:\d+\.\s*)?(?:\([ivx]+\)\s*)?(?:\([a-f]\)\s*)?', '', join_cells('aural', page, rows, 300)).strip()

    def listen(part, q, suffix, question_rows, rows, total=None, question=None, scheme_pages=None):
        pp, sp = {'A': (2, 3), 'B': (3, 4), 'C': (4, 4), 'D': (5, 5)}[part]
        card = add('L' + part, q, question or aq(pp, question_rows), rows,
                   {'A': 'japanese-6-1', 'B': 'japanese-6-1', 'C': 'japanese-6-2', 'D': 'japanese-6-0'}[part],
                   [pp], scheme_pages or [sp], suffix or '', total=total)
        card['sourceMaterial'] = source([pp], 'source-question', 'aural')
        card['stem'] = join_cells('aural', pp, [1, 2], 300)
        if part in 'CD':
            context_row = (3 if q == 1 else 29) if part == 'C' else {1: 3, 2: 11, 3: 19}[q]
            card['stem'] += '\n' + join_cells('aural', pp, [context_row], 300)
        if suffix and re.fullmatch(r'[a-b]-[ivx]+', suffix):
            letter, roman = suffix.split('-')
            card['questionRef'] = f'2024 HL Section L{part} Q{q}({roman})({letter})'
        return card

    def column(rows, x0, x1):
        return ' '.join(cell('scheme', 3, row, gi) for row in rows for gi, group in enumerate(ROWS['scheme'][2][row]) if x0 <= group[0] < x1)

    headers = [
        english(joined_selector('aural', 2, [(8, 0), (9, 0), (10, 0)])).replace('gcaitheamh ', ''),
        joined_selector('aural', 2, [(10, 1), (11, 0), (12, 0)]),
        english(joined_selector('aural', 2, [(5, 2), (6, 2), (7, 1)])),
        joined_selector('aural', 2, [(7, 2), (8, 1)]),
    ]
    # Separate printed answer columns, retain whole facts and slash routes.
    brian_details = strip_tariff(column(range(6, 12), 250, 420)).split(', ')
    brian_now = re.split(r'\(Any', column(range(6, 14), 420, 550))[0].strip().split(', ')
    brian = [point(s(3, 6, 1)), point(s(3, 6, 2), 2), anyn(brian_details, 3), anyn(brian_now, 2)]
    maeve_start = column(range(14, 18), 150, 250)
    maeve_start = [part.strip(' ,') for part in maeve_start.split('(1 mark)') if part.strip(' ,')]
    maeve_details = strip_tariff(column(range(14, 20), 250, 420))
    lesson, saturday, hours, rest = [part.strip() for part in maeve_details.split('/', 3)]
    maeve_details = [lesson, saturday, hours, *rest.split(', ')]
    maeve_now = re.split(r'\(Any', column(range(14, 23), 420, 550))[0].strip().split(', ')
    maeve = [point(s(3, 14, 1)), *[point(part) for part in maeve_start], anyn(maeve_details, 3), anyn(maeve_now, 2)]
    chloe_details = strip_tariff(column(range(23, 31), 250, 420)).split(', ')
    chloe = [point(s(3, 23, 1) + ' ' + s(3, 24, 1)), point(s(3, 23, 2)), anyn(chloe_details, 3), point(column(range(23, 26), 420, 550), 2)]
    for n, rows in enumerate([brian, maeve, chloe], 1):
        question = cell('aural', 2, 4, 1) + '\n' + cell('aural', 2, 12 + n) + '\n' + '\n'.join(headers)
        listen('A', n, None, [], rows, question=question)

    listen('B', 1, None, [3, 4], [point(s(4, 2))])
    listen('B', 2, None, [6], [anyn(options(4, [4, 5]), 2)])
    listen('B', 3, None, [10], [anyn(options(4, [8], '/'), 1)])
    listen('B', 4, None, [12], [point(s(4, 10))])
    listen('B', 5, None, [14], [anyn(options(4, [12]), 2, 2, [2, 1])])
    listen('B', 6, None, [17], [anyn(options(4, [15], '/'), 1, 2)])
    schooling, other = cell('scheme', 4, 17, 0).split(' (2 marks), ')
    listen('B', 7, None, [19], [anyn([part.strip() for part in schooling.split('/')], 1, 2), anyn([part.strip() for part in other.split('/')], 1)])
    listen('B', 8, None, [23], [anyn(options(4, [20]), 2)])
    listen('B', 9, None, [27, 28], [anyn(options(4, [23], '/'), 1, 2)])
    listen('C', 1, 'i', [4, 5], [anyn(options(4, [27]), 2, 2, [2, 1])])
    listen('C', 1, 'ii', [8, 9], [anyn(options(4, [30]), 3,
           contextNote='The question asks for two activities. The published marking scheme states: ' + cell('scheme', 4, 31))])
    transport = [part.strip() for part in cell('scheme', 4, 33, 0).split('(1 mark)') if part.strip()]
    listen('C', 1, 'iii', [12], [point(part) for part in transport])
    listen('C', 1, 'a-iv', [15, 16], [point(s(4, 35))])
    listen('C', 1, 'b-iv', [19, 20], [anyn(options(5, [0]), 2)], scheme_pages=[4, 5])
    listen('C', 1, 'v', [23], [anyn(options(5, [3], '/'), 1, 2)], scheme_pages=[5])
    listen('C', 1, 'vi', [26, 27], [point(s(5, 6))], scheme_pages=[5])
    for letter, qr, sr in [('a', 31, 9), ('b', 33, 11)]:
        text = s(5, sr).split(': ', 1)[1]
        listen('C', 2, letter + '-i', [30, qr], [anyn(text.split(', '), 2)], scheme_pages=[5])
    listen('C', 2, 'ii', [35, 36], [anyn(options(5, [14]), 3)], scheme_pages=[5])
    time = [part.strip() for part in cell('scheme', 5, 19, 0).split('(1 mark)') if part.strip()]
    listen('D', 1, 'i', [4], [point(part) for part in time])
    listen('D', 1, 'ii', [6], [anyn(options(5, [21]), 2, 2, [2, 1])])
    phone = listen('D', 1, 'iii', [9], [point(s(5, 23), 2)])
    phone['questionFigureKey'] = crop('ja-2024-hl-ld-1-iii', 5, [.53, .298, .96, .36], phone['questionText'], 'aural')
    listen('D', 2, 'i', [12], [anyn(options(5, [26], '/'), 1, 2)])
    listen('D', 2, 'ii', [15, 16], [anyn(options(5, [28], '/'), 1, 2)])
    listen('D', 3, 'i', [20], [anyn(options(5, [31], '/'), 1, 2)])
    listen('D', 3, 'a-ii', [23], [anyn(options(5, [33], '/'), 1)])
    listen('D', 3, 'b-ii', [25], [anyn(options(5, [35]), 3)])
    gifts = strip_tariff(s(5, 38)).replace('(for mum) macha', '(for mum), macha').split(', ')
    listen('D', 3, 'iii', [28], [anyn(gifts, 2)])


def consolidations(census):
    records = []
    romans = ['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii']
    for suffix, count, pp, pr, sp, sr, reason in [
        ('1a-1', 6, 3, [1, 2], 6, 3, 'One required six-cell matching table, priced one mark per cell; all six original items remain on one task.'),
        ('2b-1', 6, 8, [1, 2], 8, 12, 'One printed any-five-of-six meaning pool; all six items and five claim slots remain together.'),
        ('2b-2', 6, 8, [10, 11], 8, 19, 'One printed any-five-of-six reading pool; all six items and five claim slots remain together.'),
        ('2c-1', 6, 9, [1, 2], 9, 1, 'One printed any-five-of-six grammar pool; all six items and five claim slots remain together.'),
        ('2c-2', 6, 9, [10, 11], 9, 8, 'One printed any-five-of-six grammar pool; all six items and five claim slots remain together.'),
        ('3c', 6, 12, [1, 2, 3], 10, 9, 'One printed any-five-of-six paired reading-and-meaning pool, one mark for each component.'),
        ('3d', 8, 12, [13, 14, 15], 10, 16, 'One printed any-ten-of-twelve-blank pool across eight numbered sentences, one mark per blank. Preserve the published conditional alternative for sentence(ii).'),
    ]:
        canonical = 'ja-2024-hl-' + suffix
        paper_text = joined_selector('paper', pp, [(row, None) for row in pr])
        scheme_text = cell('scheme', sp, sr)
        task = next(task for task in census['tasks'] if canonical == 'ja-2024-hl-' + '-'.join(str(part).lower() for part in task['key'] if part is not None))
        records.append({'canonicalId': canonical, 'legacyIds': [canonical + '-' + part for part in romans[:count]],
                        'taskKey': task['key'], 'marks': task['marks'], 'reason': reason,
                        'paperEvidence': {'page': pp, 'text': paper_text}, 'schemeEvidence': {'page': sp, 'text': scheme_text}})
    return records


def build():
    reading()
    writing()
    listening()
    census = json.loads((Path(__file__).parent / 'reviews/japanese-2024-hl-census.json').read_text())
    expected = {'ja-2024-hl-' + '-'.join(str(part).lower() for part in task['key'] if part is not None): task for task in census['tasks']}
    assert set(expected) == {card['id'] for card in CARDS}
    for card in CARDS:
        task = expected[card['id']]
        assert card['totalMarks'] == task['marks'], (card['id'], card['totalMarks'], task['marks'])
        assert card['sourceEvidence']['paperPages'] == task['paperPages']
        assert card['sourceEvidence']['schemePages'] == task['schemePages']
        if 'paperRef' in task:
            assert card['questionRef'] == task['paperRef']
    assert len(CARDS) == 72, len(CARDS)
    assert sum(card['totalMarks'] for card in CARDS) == 300
    return {'subjectId': 'japanese', 'sitting': '2024-hl', 'reviewedAt': '2026-11-09',
            'sources': [{'document': name, 'path': str(path.relative_to(ROOT)), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'pagesReviewed': list(range(1, len(DOCS[name]) + 1))} for name, path in [('paper', PAPER), ('aural', AURAL), ('scheme', SCHEME)]],
            'cards': CARDS, 'selectors': EVIDENCE, 'status': 'source-reviewed-browser-qa-pending',
            'choiceAnalysis': census['choiceBoundaries'], 'consolidations': consolidations(census)}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    result = build()
    if args.write:
        (ROOT / 'scripts/markbank/authoring/reviews/japanese-2024-hl.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
        manifest = ROOT / 'components/MarkBank/figures-japanese.json'
        previous = json.loads(manifest.read_text())
        previous.update(FIGURES)
        manifest.write_text(json.dumps(previous, ensure_ascii=False, indent=2) + '\n')
        scheme_md = SCHEME.with_suffix('.md')
        marker = '\n## Audited original table columns — 2024 HL pages 3 and 7\n'
        original = scheme_md.read_text().split(marker)[0]
        columns = []
        for page, bounds in [(3, [(76, 150), (152, 250), (252, 420), (422, 560)]), (7, [(150, 323), (325, 555)])]:
            for x0, x1 in bounds:
                columns.append(DOCS['scheme'][page - 1].get_text(clip=fitz.Rect(x0, 0, x1, 780), sort=True))
        scheme_md.write_text(original + marker + '\n'.join(columns))
    print(json.dumps({'cards': len(CARDS), 'marks': sum(card['totalMarks'] for card in CARDS), 'figures': len(FIGURES)}, indent=2))
