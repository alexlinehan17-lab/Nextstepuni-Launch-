#!/usr/bin/env python3
"""2026 Higher Japanese, independently reviewed against all original pages.

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
PAPER = ROOT / 'examiner-reports/japanese/papers/2026-hl-000-paper.pdf'
AURAL = ROOT / 'examiner-reports/japanese/papers/2026-hl-A00-paper.pdf'
SCHEME = ROOT / 'examiner-reports/japanese/schemes/2026-hl.pdf'
PINNED_SOURCES = {
    PAPER: '97bb6e6f693d6255bdf2ebd18b4049b6491bd4fee88dbcde46a2cbfb42906073',
    AURAL: '8ee26b38edb3865ab3b2c837d6d7dc9b9c88869bc4b8eed5a9f674aafbc7ee43',
    SCHEME: '19aedad37177724f53d0a5ecf5bf3097df26355b38acea8fff264add1684b5ec',
}
for path, expected in PINNED_SOURCES.items():
    assert hashlib.sha256(path.read_bytes()).hexdigest() == expected, f'Source changed; review again: {path}'
DOCS = {name: fitz.open(path) for name, path in [('paper', PAPER), ('aural', AURAL), ('scheme', SCHEME)]}
ROWS = {name: [page_rows(page) for page in doc] for name, doc in DOCS.items()}
ASKS = {ask.key: ask for ask in JaPaper(2026, 'hl').asks()}
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


def ask(section, q, letter=None, roman=None):
    # The legacy paper reader stops some bilingual prompts at the first
    # physical line. These audited paper selectors include the continuation;
    # they deliberately do not substitute the scheme's reprinted question.
    continued = {
        ('1A', 2, 'b'): (3, [12]), ('1A', 2, 'c'): (3, [15]),
        ('1A', 4, 'a'): (3, [22]), ('1A', 4, 'b'): (3, [25]),
        ('1B', 1, 'a'): (4, [14]), ('1B', 1, 'b'): (4, [17]),
        ('1B', 2, 'b'): (4, [24]), ('1B', 2, 'c'): (4, [27]),
        ('2A', 1, 'a'): (7, [3]), ('2A', 1, 'b'): (7, [6]),
        ('2A', 1, 'c'): (7, [10]), ('2A', 1, 'd'): (7, [14]),
        ('2A', 3, None): (7, [26, 27, 28]),
    }
    if (section, q, letter) in continued:
        page, rows = continued[(section, q, letter)]
        return english(' '.join(p(page, row) for row in rows))
    a = ASKS[(section, q, letter, roman)]
    EVIDENCE.append({'document': 'paper', 'page': a.page + 1, 'ask': list(a.key), 'text': a.text})
    return english(a.text)


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
    return {'kind': kind, 'label': '2026 Japanese Higher Level', 'title': 'Original examination material',
            'pages': pages, 'attribution': '© State Examinations Commission.',
            **({'presentationNote': FURIGANA_NOTE} if component == 'paper' else {}),
            '_component': component}


def add(section, q, question, rows, topic, paper_pages, scheme_pages, suffix='', rubric=None, total=None, reading=None, figure=None):
    cid = f'ja-2026-hl-{section.lower()}' + (f'-{q}' if q is not None else '') + (f'-{suffix}' if suffix else '')
    ref = f'2026 HL Section {section}' + (f' Q{q}' if q is not None else '')
    if suffix:
        ref += ''.join(f'({part})' for part in suffix.split('-'))
    listening = section.startswith('L')
    card = {'id': cid, 'source': 'sec', 'subjectId': 'japanese', 'specVersion': 'lc-japanese-syllabus',
            'kind': 'rubric' if rubric else 'question', 'level': 'higher', 'year': 2026,
            'section': section[1:] if listening else section[0] if section[0] in '1234' else 'Q5',
            'topicId': topic, 'conceptId': concept_for(question, cid), 'questionRef': ref,
            'questionText': question, 'totalMarks': total if total is not None else sum(map(worth, rows)),
            'qa': {'gates': ['verbatim', 'tariff', 'figure'], 'humanReviewedBy': 'agent-verified', 'humanReviewedAt': '2026-11-06'},
            'sourceEvidence': {'component': 'aural' if listening else 'paper', 'paperPages': paper_pages, 'schemePages': scheme_pages},
            'schemeCitation': 'Marking points quoted from the SEC marking scheme, Japanese 2026 Higher Level — © State Examinations Commission.'}
    language_convention = cell('scheme', 3, 11, 1)
    card['sourceEvidence']['generalSchemePages'] = [3]
    card['answerLanguageRule'] = {'otherLanguageMultiplier': 0.5, 'sourceText': language_convention, 'schemePages': [3]}
    if rubric:
        rubric['markingGuideNote'] += ' ' + language_convention
        card['rubric'] = rubric
    else:
        card['tariffModel'] = {'kind': 'fixed'}
        card['rows'] = [dict(row, id=f'r-{i + 1}') for i, row in enumerate(rows)]
        card['rows'][0]['contextNote'] = language_convention
    if reading:
        card['sourceMaterial'] = source(reading)
    if figure:
        card['questionFigureKey'] = figure
    CARDS.append(card)
    return card


def comprehension(section, q, letter, rows, pages, scheme_pages, roman=None, question=None):
    topic = {'1': 'japanese-5-0', '2': 'japanese-5-2', '3': 'japanese-5-1'}[section[0]]
    suffix = '-'.join(part for part in [letter, roman] if part)
    card = add(section, q, question or ask(section, q, letter, roman), rows, topic, pages, scheme_pages, suffix,
               reading={'1A': [2], '1B': [4], '2A': [6], '3A': [10]}[section])
    page, row, group = {'1A': (3, 0, 0), '1B': (4, 12, 0), '2A': (7, 17 if q == 2 else 1, 1), '3A': (11, 24 if q == 2 else 1, 1)}[section]
    card['stem'] = english(p(page, row, group))
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
    # Q1A link table is one required matching task with five priced cells.
    question = english(p(3, 2))  # pinned to the paper's own instruction
    items = [ask('1A', 1, letter) for letter in 'abcde']
    add('1A', 1, question + '\n' + '\n'.join(f'({letter}) {item}' for letter, item in zip('abcde', items)),
        [point(s(9, row, 1) + ' — ' + s(9, row, 2)) for row in range(4, 9)], 'japanese-5-0', [3], [9], reading=[2])
    configs = [
        (2, 'a', [anyn([s(9, i) for i in range(10, 15)], 2, 2, [2, 1])], [9]),
        (2, 'b', [anyn([s(9, i) for i in range(17, 20)], 2)], [9]),
        (2, 'c', [anyn([s(9, i) for i in [22, 23]], 1, 2)], [9]),
        (3, 'a', [point(s(9, 26), 2)], [9]),
        (3, 'b', [anyn([s(9, i) for i in range(28, 31)], 2)], [9]),
        (4, 'a', [point(s(9, 33))], [9]),
        (4, 'b', [point(s(9, 35)), point(s(9, 36))], [9]),
        (4, 'c', [anyn([s(10, i) for i in range(1, 5)], 2)], [10]),
        (5, None, [point(s(10, 7))], [10]),
    ]
    for q, letter, rows, sp in configs:
        comprehension('1A', q, letter, rows, [3], sp)
    for q, letter, indices, count, marks in [(1, 'a', range(10, 13), 2, 1), (1, 'b', range(15, 19), 2, 1), (1, 'c', range(21, 24), 2, 1), (2, 'a', range(26, 28), 1, 1), (2, 'b', range(30, 33), 2, 1), (2, 'c', range(35, 37), 1, 2)]:
        comprehension('1B', q, letter, [anyn([s(10, i) for i in indices], count, marks)], [4], [10])

    for letter, indices, steps in [('a', range(4, 7), None), ('b', range(9, 13), [2, 1]), ('c', range(15, 18), [2, 1]), ('d', range(20, 23), [2, 1])]:
        comprehension('2A', 1, letter, [anyn([s(11, i) for i in indices], 2, 2 if steps else 1, steps)], [7], [11])
    for letter, row, marks in [('a', 26, 1), ('b', 28, 2), ('c', 30, 2)]:
        comprehension('2A', 2, letter, [point(s(11, row), marks)], [7], [11])
    comprehension('2A', 2, 'd', [anyn([s(11, 32), s(12, 0), s(12, 1)], 2)], [7], [11, 12])
    translation = add('2A', 3, ask('2A', 3), [point(s(12, i)) for i in range(6, 10)], 'japanese-5-3', [7], [12], reading=[6])
    translation['sourceMaterial']['pages'].append(7)

    # Four printed any-five pools: all six choices, one card and five slots.
    for section, q, page, instruction_row, item_rows, scheme_page, answer_rows, region in [
        ('2B', 1, 8, 2, range(4, 10), 12, range(12, 18), [.06, .04, .95, .49]),
        ('2B', 2, 8, 11, range(13, 19), 12, range(19, 25), [.06, .49, .95, .91]),
        ('2C', 1, 9, 3, range(5, 11), 12, range(27, 33), [.06, .035, .95, .507]),
        ('2C', 2, 9, 12, range(14, 20), 13, range(1, 7), [.06, .511, .95, .927]),
    ]:
        instruction = p(page, instruction_row)
        question = instruction + '\n' + '\n'.join(p(page, row) for row in item_rows)
        options = [s(scheme_page, row, 0) + ' — ' + s(scheme_page, row, 1) for row in answer_rows]
        key = crop(f'ja-2026-hl-{section.lower()}-{q}', page, region, question)
        add(section, q, question, [anyn(options, 5)], 'japanese-5-4' if section == '2B' else 'japanese-5-5', [page], [scheme_page], figure=key)

    q3 = [
        ('a', 'i', english(p(11, 2, 2)), [anyn([s(13, i) for i in range(11, 16)], 3)], [13]),
        ('a', 'ii', p(11, 7), [anyn([s(13, 18), s(13, 19), s(13, 20, 1)], 2)], [13]),
        ('b', 'i', p(11, 10), [anyn([s(13, i) for i in range(23, 26)], 2)], [13]),
        ('b', 'ii', p(11, 13), [point(s(13, 28), 2)], [13]),
        ('c', 'i', english(p(11, 15, 2)), [anyn([s(13, i) for i in range(30, 34)], 2)], [13]),
        ('c', 'ii', english(p(11, 17)), [anyn([s(14, i) for i in range(1, 4)], 2)], [14]),
    ]
    for letter, roman, question, rows, sp in q3:
        comprehension('3A', 1, letter, rows, [11], sp, roman, question)
    gift_groups = []
    for row in [7, 8, 9]:
        person = s(14, row, 1) if row != 9 else s(14, row, 0).split('  ')[-1].removeprefix('(a) or (b) ').strip()
        item = s(14, row, 2 if row != 9 else 1)
        gift_groups.append({'id': f'pair-{row}', 'label': person, 'rows': [{'id': 'person', 'text': person, 'marks': 1}, {'id': 'gift', 'text': item, 'marks': 1}]})
    add('3A', 1, p(11, 21), [], 'japanese-5-1', [11], [14], 'c-iii', total=4, reading=[10, 11],
        rubric={'system': 'language-points', 'count': 2, 'groups': gift_groups, 'taskRequirements': [s(14, 10)], 'markingGuideNote': 'The item must correspond with the person, as the scheme states. Claim a gift only if it matches the person you wrote beside it.'})
    for letter, row in zip('abcd', [13, 15, 17, 19]):
        comprehension('3A', 2, letter, [point(s(14, row), 2)], [11], [14])
    instruction = english(p(12, 2)) + ' ' + p(12, 3)
    question = instruction + '\n' + '\n'.join(p(12, row) for row in range(5, 12))
    groups = [{'id': f'item-{i + 1}', 'label': s(14, row, 0), 'rows': [{'id': 'reading', 'text': s(14, row, 1), 'marks': 1}, {'id': 'meaning', 'text': s(14, row, 3), 'marks': 1}]} for i, row in enumerate(range(21, 27))]
    key = crop('ja-2026-hl-3b', 12, [.06, .025, .95, .45], question)
    add('3B', None, question, [], 'japanese-5-4', [12], [14], total=10, figure=key,
        rubric={'system': 'language-points', 'count': 5, 'groups': groups, 'taskRequirements': [instruction], 'markingGuideNote': 'The scheme awards one mark for the correct reading and one for the meaning, for each of five chosen items.'})
    instruction = english(p(12, 14)) + ' ' + p(12, 15)
    # The blank rules are PDF vector lines, not characters in the text layer.
    # Their inspected positions separate the post-marker gap groups here.
    sentences = [p(12, row, 0) + ' ' + ' ____ '.join(p(12, row, gi) for gi in range(1, len(ROWS['paper'][11][row]))) for row in range(16, 23)]
    question = instruction + '\n' + '\n'.join(sentences)
    groups = []
    for row in range(1, 8):
        first = s(15, row, 0)
        groups.append({'id': f'{row}-first', 'label': f'{row}. First blank', 'rows': [{'id': 'particle', 'text': first.split('. ', 1)[1], 'marks': 1}]})
        if row not in [4, 7]:
            groups.append({'id': f'{row}-second', 'label': f'{row}. Second blank', 'rows': [{'id': 'particle', 'text': s(15, row, 2), 'marks': 1}]})
    key = crop('ja-2026-hl-3c', 12, [.06, .46, .95, .92], question)
    add('3C', None, question, [], 'japanese-5-5', [12], [15], total=10, figure=key,
        rubric={'system': 'language-points', 'count': 10, 'groups': groups, 'taskRequirements': [instruction], 'markingGuideNote': 'Select ten blanks. Each correct particle earns the one mark printed in the scheme; slash-separated particles are alternatives for the same blank.'})


def steps(maximum):
    return list(range(maximum + 1))


def writing():
    for q, paper_page, scheme_page, maximum, threshold, length, lower, normal_ranges, lower_ranges in [
        (4, 14, 17, 20, 10, 150, 15, [(0, 5), (6, 14), (15, 20)], [(0, 3), (4, 10), (11, 15)]),
        (5, 16, 19, 30, 15, 200, 20, [(0, 7), (8, 20), (21, 30)], [(0, 4), (5, 12), (13, 20)]),
    ]:
        bands = []
        lower_bands = []
        for n, rows in enumerate([range(16, 23), range(23, 30), range(30, 36)]):
            guidance = [join_cells('scheme', scheme_page, rows, 160)]
            label = f'{normal_ranges[n][0]}–{normal_ranges[n][1]}'
            bands.append({'label': label, 'marks': list(range(normal_ranges[n][0], normal_ranges[n][1] + 1)), 'guidance': guidance})
            lower_bands.append({'label': f'{lower_ranges[n][0]}–{lower_ranges[n][1]}', 'marks': list(range(lower_ranges[n][0], lower_ranges[n][1] + 1)), 'guidance': guidance})
        expression_rule = join_cells('scheme', scheme_page, range(10, 14))
        if q == 4:
            question = p(14, 2) + '\n' + '\n'.join(p(14, row) for row in [5, 6, 7, 8, 9, 12, 13, 14, 15, 16, 19, 20, 21])
            criteria = [
                {'id': 'opening', 'label': 'Appropriate opening', 'maxMarks': 1, 'permittedMarks': [0, 1], 'guidance': [s(16, 16)]},
                *[{'id': f'part-{letter}', 'label': f'({letter})', 'maxMarks': 9, 'permittedMarks': steps(9), 'guidance': [cell('scheme', 16, row), expression_rule]} for letter, row in [('a', 17), ('b', 18)]],
                {'id': 'closing', 'label': 'Appropriate closing', 'maxMarks': 1, 'permittedMarks': [0, 1], 'guidance': [s(16, 19, 1)]},
            ]
        else:
            question = ' '.join(p(16, row) for row in range(4, 7)) + '\n' + '\n'.join(p(16, row) for row in range(7, 15))
            headings = [cell('scheme', 18, row) for row in range(4, 12)]
            criteria = [{'id': f'heading-{i}', 'label': f'Heading {i} you chose', 'maxMarks': 7, 'permittedMarks': steps(7), 'guidance': [s(18, 13)] + headings} for i in range(1, 5)]
            criteria.append({'id': 'discretionary', 'label': 'Discretionary marks', 'maxMarks': 2, 'permittedMarks': [0, 1, 2], 'guidance': [s(18, 14)]})
        content_ids = [criterion['id'] for criterion in criteria]
        criteria.append({'id': 'expression', 'label': s(scheme_page - 1, 20 if q == 4 else 15), 'maxMarks': maximum,
                         'permittedMarks': steps(maximum), 'guidance': [join_cells('scheme', scheme_page, [36, 37])], 'bands': bands,
                         'limits': [{'id': 'lower-e', 'maxMarks': lower, 'when': {'any': [{'criterionIds': content_ids, 'atMost': threshold}, {'length': 'characters', 'below': length}]}, 'bands': lower_bands, 'guidance': [expression_rule]}]})
        key = crop(f'ja-2026-hl-{q}', paper_page, [.045, .015, .96, .92], question)
        add(str(q), None, question, [], 'japanese-5-7', [paper_page], [scheme_page - 1, scheme_page], total=maximum * 2, figure=key,
            rubric={'system': 'language-writing', 'taskRequirements': [p(14, 2)] if q == 4 else [p(16, 6)], 'criteria': criteria,
                    'markingGuideNote': 'Assess the response using the published content allocations and expression descriptors. The scheme gives criteria rather than a model composition. For Question 5, assess four different headings once each.' if q == 5 else 'Assess the one option you answered. The same published content and expression grid applies to all three options; the scheme gives criteria rather than a model composition.'})


def listening():
    def ac(page, row, group=None):
        return ' '.join(cell('aural', page, row, group).split())

    def aq(page, rows):
        text = ' '.join(join_cells('aural', page, rows, 300).split())
        return re.sub(r'^(?:\d+\.\s*)?(?:\([a-f]\)\s*)?', '', text)

    def listen(part, q, letter, question, rows, pages, sp, rubric=None, total=None):
        card = add('L' + part, q, question, rows, {'A': 'japanese-6-1', 'B': 'japanese-6-0', 'C': 'japanese-6-2', 'D': 'japanese-6-1'}[part], pages, sp, letter or '', rubric=rubric, total=total)
        card['sourceMaterial'] = source(pages, 'source-question', 'aural')
        return card

    # Required profile headings stay together. Each row is one separately
    # priced seven-mark response, not four independently scheduled fragments.
    headers = [ac(2, 9, i) + ' ' + ac(2, 10, i) for i in range(4)]
    instruction = ac(2, 4)
    maya = [point(s(4, 6).removeprefix('Maya ')), point(s(4, 6, 1)), point(s(4, 8, 0)),
            anyn([s(4, 6, 2) + ' ' + s(4, 7, 2), s(4, 8, 1) + ' ' + s(4, 9, 1), s(4, 10)], 2),
            point(s(4, 6, 3) + s(4, 7, 3)), point(re.sub(r'\s*\(1\s+mark\)$', '', cell('scheme', 4, 8, 2) + ' ' + cell('scheme', 4, 9, 2)))]
    kenji_date, kenji_city = s(4, 14, 1).split(' - ', 1)
    kenji = [point(kenji_date + ' ' + s(4, 15)),
             anyn([kenji_city, s(4, 15, 1), s(4, 16, 1) + ' ' + s(4, 17) + ' ' + s(4, 18)], 2),
             anyn([s(4, 14, 2), s(4, 15, 2), s(4, 16, 2)], 2), point(s(4, 14, 3)),
             anyn([s(4, 16, 3), s(4, 17, 2), s(4, 18, 1), s(4, 19, 1)], 1)]
    abbie = [point(s(4, 23).removeprefix('Abbie ')), point(s(4, 23, 1)), point(s(4, 25)),
             anyn([s(4, 23, 2), s(4, 24, 2), s(4, 25, 1) + ' ' + s(4, 26, 1)], 2),
             anyn([s(4, 23, 3) + ' ' + s(4, 24, 3), s(4, 25, 2) + ' ' + s(4, 26, 2), s(4, 27, 1)], 2)]
    for n, rows in enumerate([maya, kenji, abbie], 1):
        question = instruction + '\n' + ac(2, 10 + n) + '\n' + '\n'.join(headers)
        card = listen('A', n, None, question, rows, [2], [4])
        card['stem'] = ac(2, 1) + ' ' + ac(2, 3, 1)
        assert card['totalMarks'] == 7

    def alternatives(question, answers):
        return {'system': 'language-points', 'count': 1, 'taskRequirements': [],
                'groups': [{'id': 'answer', 'label': question, 'answerCount': 1,
                            'rows': [{'id': f'answer-{i + 1}', 'text': text, 'marks': mark} for i, (text, mark) in enumerate(answers)]}],
                'markingGuideNote': 'Claim the complete or partial answer you gave at its printed mark. Alternative wordings for the same answer cannot be added together.'}
    question = aq(3, [3])
    partial = s(5, 4).removeprefix('(').removesuffix(' 1 mark)')
    listen('B', 1, 'a', question, [], [3], [5], alternatives(question, [(s(5, 3), 2), (partial, 1)]), 2)
    for q, letter, qr, sr, count in [(1, 'b', [5], range(6, 9), 2), (2, 'a', [9, 10], range(12, 15), 2), (2, 'b', [12, 13], range(17, 21), 2)]:
        listen('B', q, letter, aq(3, qr), [anyn([s(5, row) for row in sr], count, 2)], [3], [5])
    listen('B', 3, 'a', aq(3, [17]), [point(s(5, 24), 2)], [3], [5])
    frequency1, after = s(5, 26).split(' (1 mark) ', 1)
    frequency2 = s(5, 27).split(' (1 mark) ', 1)[0]
    listen('B', 3, 'b', aq(3, [19]), [anyn([frequency1, frequency2], 1), point(after)], [3], [5])
    listen('B', 3, 'c', aq(3, [22]), [point(s(5, 30), 2)], [3], [5])

    listen('C', 1, 'a', aq(4, [5, 6]), [point(s(6, 3), 2)], [4], [6])
    question = ac(4, 8).split('(b)')[-1].strip() + ' ' + ac(4, 9, 1)
    listen('C', 1, 'b', question, [point(s(6, 5), 2)], [4], [6])
    listen('C', 1, 'c', aq(4, [12]), [anyn([s(6, 7), s(6, 8)], 1, 2)], [4], [6])
    listen('C', 1, 'd', aq(4, [15]), [anyn([s(6, row) for row in range(11, 15)], 2, 2)], [4], [6])
    birthday = s(6, 17).split(' (1 mark) ')
    listen('C', 1, 'e', aq(4, [19]), [point(text) for text in birthday], [4], [6])
    listen('C', 1, 'f', aq(4, [21]), [point(s(6, 19), 2)], [4], [6])
    question = aq(4, [24, 25]) + '\n' + english(ac(4, 26)) + '\n' + english(ac(4, 27))
    weather = [anyn([s(6, 23), s(6, 24)], 1), anyn([s(6, 23, 1), s(6, 24, 1)], 1), anyn([s(6, 26).split('- ', 1)[1], s(6, 27), s(6, 28)], 2)]
    for row, label in zip(weather, [s(6, 22, 0), s(6, 22, 1), s(6, 26).split(':', 1)[0]]):
        row['contextNote'] = label
    listen('C', 2, 'a', question, weather, [4], [6])
    listen('C', 2, 'b', aq(4, [28, 29]), [anyn([s(6, row) for row in range(31, 34)], 2)], [4], [6])

    listen('D', 1, None, aq(5, [3, 4]), [point(s(7, 2))], [5], [7])
    question = aq(5, [6])
    partial = s(7, 6).removeprefix('(').removesuffix(' 1 mark)')
    listen('D', 2, None, question, [], [5], [7], alternatives(question, [(s(7, 4), 2), (s(7, 5), 2), (partial, 1)]), 2)
    listen('D', 3, 'a', aq(5, [10, 11]), [point(s(7, 9)), point(s(7, 10))], [5], [7])
    listen('D', 3, 'b', aq(5, [13, 14]), [anyn([s(7, row) for row in range(12, 15)], 2)], [5], [7])
    listen('D', 4, None, aq(5, [17]), [anyn([s(7, row) for row in range(17, 23)], 3)], [5], [7])
    listen('D', 5, None, aq(5, [20, 21]), [point(s(7, 25)), anyn([s(7, row) for row in range(26, 29)], 2)], [5], [7])
    listen('D', 6, None, aq(5, [23]), [anyn([s(7, row) for row in range(31, 34)], 2)], [5], [7])
    listen('D', 7, None, aq(5, [25]), [anyn([s(7, row) for row in range(36, 40)], 2)], [5], [7])
    listen('D', 8, None, aq(5, [28]), [anyn([s(8, row) for row in range(1, 5)], 2)], [5], [8])


def build():
    reading()
    writing()
    listening()
    assert len(CARDS) == 71, len(CARDS)
    assert sum(card['totalMarks'] for card in CARDS) == 300
    return {'subjectId': 'japanese', 'sitting': '2026-hl', 'reviewedAt': '2026-11-06',
            'sources': [{'document': name, 'path': str(path.relative_to(ROOT)), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'pagesReviewed': list(range(1, len(DOCS[name]) + 1))} for name, path in [('paper', PAPER), ('aural', AURAL), ('scheme', SCHEME)]],
            'cards': CARDS, 'selectors': EVIDENCE,
            'status': 'source-reviewed-browser-qa-pending',
            'choiceAnalysis': {'2B1': 'any5of6-onecard', '2B2': 'any5of6-onecard', '2C1': 'any5of6-onecard', '2C2': 'any5of6-onecard', '3A1cIII': 'any2of3-pairs-onecard', '3B': 'any5of6-reading-and-meaning-onecard', '3C': 'any10of12-blanks-onecard', '4': 'choose1of3-same-grid-onecard', '5': 'choose4of8-headings-onecard'}}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    result = build()
    if args.write:
        target = ROOT / 'scripts/markbank/authoring/reviews/japanese-2026-hl.json'
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
        manifest = ROOT / 'components/MarkBank/figures-japanese.json'
        previous = json.loads(manifest.read_text()) if manifest.exists() else {}
        previous.update(FIGURES)
        manifest.write_text(json.dumps(previous, ensure_ascii=False, indent=2) + '\n')
        # Scheme p4 is a five-column table. The whole-page extraction reads
        # across columns and splits a student's answer with another column's
        # text. Append the inspected columns directly from the original PDF,
        # retaining the whole-page extraction above for comparison.
        scheme_md = SCHEME.with_suffix('.md')
        marker = '\n## Audited original table columns — 2026 HL page 4\n'
        text = scheme_md.read_text().split(marker)[0]
        columns = [DOCS['scheme'][3].get_text(clip=fitz.Rect(x0, 0, x1, 780), sort=True) for x0, x1 in [(80, 149), (150, 245), (245, 390), (390, 555)]]
        scheme_md.write_text(text + marker + '\n'.join(columns))
    print(json.dumps({'cards': len(CARDS), 'marks': sum(card['totalMarks'] for card in CARDS), 'figures': len(FIGURES)}, indent=2))
