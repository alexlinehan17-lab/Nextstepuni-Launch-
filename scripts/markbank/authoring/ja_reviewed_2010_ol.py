#!/usr/bin/env python3
"""Publish the independently censused 2010 Ordinary sitting from PDF selectors.

Question/answer/guidance strings below are selected from the original PDFs.
Finite choices and required response pools remain single tasks. The census does not import this file or its output.
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
PATHS = {
    'paper': ROOT / 'examiner-reports/japanese/papers/2010-ol-000-paper.pdf',
    'aural': ROOT / 'examiner-reports/japanese/papers/2010-ol-A00-paper.pdf',
    'scheme': ROOT / 'examiner-reports/japanese/schemes/2010-ol.pdf',
}
HASHES = {
    'paper': 'd82e39c9a0e6745f641ca6eab9b6750722a605f878c28750bdd674c15e3d20bc',
    'aural': '0d18de5948b5363719459b06092b4b26424aa35abdd509513a696186581f7d20',
    'scheme': '096c546ef66b119647c04d4e401ad0845819859fba602e9e2ca8d237a14ac080',
}
for name, path in PATHS.items():
    assert hashlib.sha256(path.read_bytes()).hexdigest() == HASHES[name], path
DOCS = {name: fitz.open(path) for name, path in PATHS.items()}
ROWS = {name: [page_rows(page) for page in doc] for name, doc in DOCS.items()}
CARDS, EVIDENCE, FIGURES, BINDINGS, CORRECTIONS = [], [], {}, [], []
EXISTING_FIGURES = json.loads((ROOT / 'components/MarkBank/figures-japanese.json').read_text())
ORIGINAL_IDS = set(re.findall(r'^    id: "([^\"]+)"', (ROOT / "components/MarkBank/cards/japanese/ordinary.ts").read_text(), re.M))
UNPRINTED = re.search(r"export const UNPRINTED_ANSWER = '([^']+)'", (ROOT / 'types/markBank.ts').read_text()).group(1)


def cell(doc, page, row, group=None):
    groups = ROWS[doc][page - 1][row]
    text = ' '.join(group[2] for group in groups) if group is None else groups[group][2]
    EVIDENCE.append({'document': doc, 'page': page, 'row': row, 'group': group, 'text': text})
    return text


def p(page, row, group=None):
    return cell('paper', page, row, group)


def without_marker(text):
    return re.sub(r'^(?:\d+\.|\([a-z]+\))\s*', '', text).strip()


def english(text):
    return text.replace('\xa0', ' ').split('/', 1)[-1].strip()


def col(doc, page, rows, xmin=300):
    text = ' '.join(' '.join(cell(doc, page, row, i) for i, group in enumerate(ROWS[doc][page - 1][row]) if group[0] >= xmin) for row in rows).strip()
    assert text, (doc, page, rows, xmin)
    return text


def s(page, row, group=0):
    return re.sub(r'\s*\(?\s*\d+\s*marks?\)?\s*$', '', cell('scheme', page, row, group)).strip().removeprefix('- ').strip()


def sa(page, row, group=0):
    return without_marker(s(page, row, group)).removeprefix('- ').strip()


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


def source(pages, component='paper'):
    return {'kind': 'source-text', 'label': '2010 Japanese Ordinary Level', 'title': 'Original examination material',
            'pages': pages, 'attribution': '© State Examinations Commission.',
            **({'presentationNote': FURIGANA_NOTE} if component == 'paper' else {}), '_component': component}


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
    proof_path = ROOT / 'tmp/japanese-review/2010-ol-crop-rendered.json'
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



def add(section, q, question, rows, topic, pp, sp, suffix='', rubric=None, total=None, reading=None, figure=None, stem=None):
    cid = f'ja-2010-ol-{section.lower()}' + (f'-{q}' if q is not None else '') + (f'-{suffix}' if suffix else '')
    ref = f'2010 OL Section {section}' + (f' Q{q}' if q is not None else ' Q' if suffix else '') + ''.join(f'({part})' for part in suffix.split('-') if part)
    listening = section.startswith('L')
    card = {'id': cid, 'source': 'sec', 'subjectId': 'japanese', 'specVersion': 'lc-japanese-syllabus',
            'kind': 'rubric' if rubric else 'question', 'level': 'ordinary', 'year': 2010,
            'section': section[1:] if listening else section[0] if section[0] in '1234' else 'Q5',
            'topicId': topic, 'conceptId': concept_for(question, cid), 'questionRef': ref,
            'questionText': question, 'totalMarks': total if total is not None else sum(map(worth, rows)),
            'qa': {'gates': ['verbatim', 'tariff', 'figure'], 'humanReviewedBy': 'agent-verified', 'humanReviewedAt': '2026-11-13'},
            'sourceEvidence': {'component': 'aural' if listening else 'paper', 'paperPages': pp, 'schemePages': sp},
            'schemeCitation': 'Marking points quoted from the SEC marking scheme, Japanese 2010 Ordinary Level — © State Examinations Commission.'}
    if cid in ORIGINAL_IDS:
        card['qa']['gates'].append('reviewed-card-correction')
    if section == '2' and cid != 'ja-2010-ol-2-3-iii':
        card['sourceEvidence']['generalSchemePages'] = [6]
        card['answerLanguageRule'] = {'otherLanguageMultiplier': 0.5, 'sourceText': cell('scheme', 6, 1), 'schemePages': [6]}
    if section == 'LD' and q >= 3:
        card['sourceEvidence']['generalSchemePages'] = [4]
        card['answerLanguageRule'] = {'otherLanguageMultiplier': 0.5, 'penalizedLanguage': 'Japanese', 'sourceText': cell('scheme', 4, 12), 'schemePages': [4]}
    if rubric:
        card['rubric'] = rubric
    else:
        card['tariffModel'] = {'kind': 'fixed'}
        card['rows'] = [dict(row, id=f'r-{i + 1}') for i, row in enumerate(rows)]
    if reading:
        card['sourceMaterial'] = source(reading, 'aural' if listening else 'paper')
    if figure:
        card['questionFigureKey'] = figure
    if stem:
        card['stem'] = stem
    CARDS.append(card)
    return card


def pool(count, labels, answers, marks, instruction, guide):
    return {'system': 'language-points', 'count': count, 'taskRequirements': [instruction],
            'groups': [{'id': f'item-{i + 1}', 'label': label, 'rows': [{'id': 'answer', 'text': answer, 'marks': marks}]} for i, (label, answer) in enumerate(zip(labels, answers))],
            'markingGuideNote': guide}


def options(page, rows, group=0, separator=','):
    text = ' '.join(s(page, row, group) for row in rows)
    text = re.sub(r'\s*\(any .*?\)', '', text, flags=re.I)
    return [part.strip() for part in text.split(separator)]


def joined_selector(doc, page, rows):
    text = ' '.join(cell(doc, page, row, group) for row, group in rows)
    EVIDENCE.append({'document': doc, 'page': page, 'parts': [{'row': row, 'group': group} for row, group in rows], 'text': text})
    return text

def clean_label(text):
    return re.sub(r'_+', '', text).strip()


def find_row(doc, page, phrase):
    found = [i for i, row in enumerate(ROWS[doc][page - 1]) if phrase in ' '.join(group[2] for group in row)]
    assert len(found) == 1, (doc, page, phrase, found)
    return found[0]



def group_rows(card, groups):
    card['taskGroups'] = [{'sourceCardId': card['id'] + '-' + name, 'label': label,
        'marks': sum(worth(row) for row in card['rows'][start:end]), 'rowIds': [row['id'] for row in card['rows'][start:end]]}
        for name, label, start, end in groups]


def criterion(text, maximum, allowed, note):
    return {'kind': 'criterion', 'verbatim': text, 'marks': maximum, 'permittedMarks': allowed, 'contextNote': note}


def reading_q1():
    labels = [english(p(3, r, 0)) for r in range(2, 7)]
    c = add('1', 1, p(3, 1) + '\n' + '\n'.join(labels),
            [point(s(5, r, 1)) for r in range(3, 8)], 'japanese-5-0', [3], [5], reading=[2],
            figure=crop('ja-2010-ol-web', 2, [.055, .025, .97, .985], 'Original shopping webpage, all five buttons and product prices'))
    c['questionFigureIncludesPrompt'] = False
    group_rows(c, [(str(i + 1), label, i, i + 1) for i, label in enumerate(labels)])
    labels = [english(p(3, r, 0)) for r in range(8, 14)]
    c = add('1', 2, english(p(3, 7)) + '\n' + '\n'.join(labels),
            [point(s(5, r, 1)) for r in range(9, 15)], 'japanese-5-0', [3], [5], reading=[2])
    group_rows(c, [(str(i + 1), label, i, i + 1) for i, label in enumerate(labels)])
    for suffix, qr, opt, sr, sg in [
        ('i', [16], [17, 18, 19], 16, 1), ('ii', [20], [21], 17, 0),
        ('iii', [22], [23], 18, 0), ('iv', [24], [25, 26], 19, 0),
        ('v', [27], [28, 29], 20, 1), ('vi', [30, 31], [32, 33], 21, 0),
        ('vii', [34], [35], 22, 0),
    ]:
        question = ' '.join(english(p(3, r)) for r in qr) + '\n' + '\n'.join(p(3, r) for r in opt)
        answer = s(5, sr, sg)
        if sg == 0: answer = without_marker(answer)
        note = None
        if suffix == 'iii':
            literal = cell('scheme', 5, 18, 0)
            bank = p(3, 23, 2)
            case = p(2, 9)
            answer = bank
            note = f'Source discrepancy: scheme “{literal}”; original paper option “{bank}”, while (d) is 24. The webpage says “{case}”. Use only the original paper option (c) 10: the paper case quantity and scheme numeric 10 agree. This is a source-local correction, not a general letter conversion.'
            BINDINGS.append({'cardId': 'ja-2010-ol-1-3-iii', 'answer': answer, 'rowIds': ['r-1'],
                'paperSelector': {'document': 'paper', 'page': 3, 'row': 23, 'group': 2, 'text': bank},
                'corroboratingPaperSelector': {'document': 'paper', 'page': 2, 'row': 9, 'group': None, 'text': case},
                'schemeSelectors': [{'document': 'scheme', 'page': 5, 'row': 18, 'group': 0, 'text': literal}]})
        add('1', 3, question, [point(answer, 2, **({'contextNote': note} if note else {}))],
            'japanese-5-0', [3], [5], suffix, reading=[2], stem=p(3, 15))


def reading_q2():
    labels = [p(5, 3, 0), p(5, 3, 2), p(5, 5, 0), clean_label(p(5, 5, 2))]
    answers = [s(6, 3, 0).split()[-1], s(6, 3, 3), s(6, 4, 0).split()[-1], s(6, 4, 2).split()[-1]]
    c = add('2', 1, p(5, 1) + '\n' + '\n'.join(labels), [point(v, 2) for v in answers],
            'japanese-5-0', [5], [6], reading=[4])
    group_rows(c, [(str(i + 1), label, i, i + 1) for i, label in enumerate(labels)])
    for q, suffix, pr, sr, mark in [(2, 'i', 7, 7, 3), (2, 'ii', 9, 9, 3),
                                  (3, 'i', 19, 19, 3), (3, 'ii', 21, 21, 3)]:
        add('2', q, clean_label(p(5, pr)), [point(s(6, sr), mark)], 'japanese-5-0', [5], [6], suffix,
            reading=[4], stem=english(p(5, 6 if q == 2 else 18)))
    sports = [part.strip() for part in (s(6, 13) + ' ' + s(6, 14)).split(',')]
    assert len(sports) == 6
    add('2', 2, p(5, 13), [anyn(sports, 2, 2, contextNote=cell('scheme', 6, 12))], 'japanese-5-0', [5], [6], 'iii', reading=[4], stem=english(p(5, 11)))
    add('2', 2, p(5, 16), [point(s(6, 16), 2)], 'japanese-5-0', [5], [6], 'iv', reading=[4], stem=english(p(5, 11)))
    full = [part.strip() for part in (s(6, 25) + ' ' + s(6, 26)).split(',')]
    partial = cell('scheme', 6, 27)
    quota = cell('scheme', 6, 24)
    language = cell('scheme', 6, 1)
    assert len(full) == 5
    note = f'{quota}. {partial}. {language}. The full alternatives carry 2 each and the generic chicken/fish/salad alternatives carry half (1 each), under the two-answer total4. The source does not state how generic partial credit and the independent language reduction combine. This complete task is confidence review only; marks are not calculated. Do not infer a cumulative or once-only combined reduction.'
    c = add('2', 3, english(p(5, 24)), [point(v, None, contextNote=note) for v in full]
            + [point(partial, None, contextNote=note)], 'japanese-5-0', [5], [6], 'iii', total=4, reading=[4], stem=english(p(5, 23)))
    c['tariffModel'] = {'kind': 'questionTotal'}
    c['sourceEvidence']['generalSchemePages'] = [6]
    for suffix, qr, sr, mark in [('i', [27], 2, 3), ('ii', [28], 4, 2), ('iii', [30, 31, 32, 33], 7, 2), ('iv', [34, 35, 36], 9, 2)]:
        question = '\n'.join(clean_label(english(p(5, r)) if r in [30, 34] else p(5, r)) for r in qr)
        add('2', 4, question, [point(s(7, sr), mark)], 'japanese-5-0', [5], [7], suffix, reading=[4],
            stem=english(p(5, 26 if suffix in ['i', 'ii'] else 29)))
    name = cell('scheme', 7, 12, 0)
    names = [part.strip() for part in re.split(r'\(1 mark\),?\s*', name) if part.strip()]
    assert len(names) == 2
    add('2', 5, p(5, 38), [point(v, 1, contextNote=name) for v in names], 'japanese-5-0', [5], [7], 'i', reading=[4], stem=english(p(5, 37)))
    add('2', 5, p(5, 40), [point(s(7, 15), 3)], 'japanese-5-0', [5], [7], 'ii', reading=[4], stem=english(p(5, 37)))
    add('2', 5, p(5, 42), [point(s(7, 17), 2)], 'japanese-5-0', [5], [7], 'iii', reading=[4], stem=english(p(5, 37)))


def reading_q3():
    instruction = p(7, 2)
    labels = [p(7, 4), p(7, 5), p(7, 6), p(7, 7, 0) + ' — ' + p(7, 8), p(7, 7, 0) + ' — ' + p(7, 10)]
    weather = ' '.join([s(8, 7, 0), s(8, 8, 0)])
    rows = [point(s(8, r, 1), 2) for r in [3, 4, 5]]
    rows += [anyn([part.strip() for part in weather.split('/')], 1, 2), point(s(8, 10), 2)]
    c = add('3A', 1, instruction + '\n' + '\n'.join(labels), rows, 'japanese-5-0', [7], [8], reading=[6],
            figure=crop('ja-2010-ol-3a-1', 7, [.055, .025, .97, .377], instruction))
    group_rows(c, [(str(i + 1), label, i, i + 1) for i, label in enumerate(labels)])
    instruction = col('paper', 7, range(11, 15))
    labels = [p(7, r) for r in [20, 23, 26, 29, 32, 35]]
    rows = []
    for sr in range(12, 18):
        text = s(8, sr)
        match = re.fullmatch(r'\d+\.\s*(True|False)\s+1 mark\s*(.+?)\s*', text)
        assert match, (sr, text)
        rows += [point(match[1]), point(match[2])]
    c = add('3A', 2, instruction + '\n' + '\n'.join(labels), rows, 'japanese-5-0', [7], [8], reading=[6],
            figure=crop('ja-2010-ol-3a-2', 7, [.055, .375, .97, .89], instruction),
            stem=p(7, 16, 1) + ' — ' + p(7, 17))
    group_rows(c, [(str(i + 1), label, i * 2, i * 2 + 2) for i, label in enumerate(labels)])
    instruction = col('paper', 8, [0, 1])
    labels = [p(8, r) for r in range(3, 8)]
    rows = [point(without_marker(s(8, r))) for r in range(19, 24)]
    c = add('3B', None, instruction + '\n' + '\n'.join(labels), rows, 'japanese-5-5', [8], [8], reading=[6],
            figure=crop('ja-2010-ol-3b', 8, [.055, .025, .985, .34], instruction), stem=p(8, 2))
    group_rows(c, [(str(i + 1), label, i, i + 1) for i, label in enumerate(labels)])
    instruction = col('paper', 8, [8, 9])
    labels = [p(8, r) for r in [12, 14, 16]]
    c = add('3C', None, instruction + '\n' + '\n'.join(labels), [point(s(8, r, 1), 2) for r in [25, 26, 27]],
            'japanese-5-5', [8], [8], reading=[6],
            figure=crop('ja-2010-ol-3c', 8, [.055, .345, .985, .68], instruction), stem=p(8, 10) + '\n' + p(8, 11))
    group_rows(c, [(str(i + 1), label, i, i + 1) for i, label in enumerate(labels)])
    instruction = col('paper', 9, [0, 1], 290)
    labels = [p(9, r) for r in range(2, 12)]
    c = add('3D', None, instruction + '\n' + '\n'.join(labels), [point(without_marker(s(9, r))) for r in range(1, 11)],
            'japanese-5-4', [9], [9], reading=[6], figure=crop('ja-2010-ol-3d', 9, [.055, .025, .975, .44], instruction))
    group_rows(c, [(str(i + 1), label, i, i + 1) for i, label in enumerate(labels)])
    question = p(9, 17) + ' ' + p(9, 18)
    rubric = {'system': 'language-writing', 'taskRequirements': [question], 'criteria': [
        {'id': 'difference-1', 'label': 'First distinct difference', 'maxMarks': 2, 'permittedMarks': [0, 2], 'guidance': [cell('scheme', 9, 14)]},
        {'id': 'difference-2', 'label': 'Second distinct difference', 'maxMarks': 2, 'permittedMarks': [0, 2], 'guidance': [cell('scheme', 9, 14)]},
        {'id': 'discretionary-1', 'label': 'First discretionary mark', 'maxMarks': 1, 'permittedMarks': [0, 1], 'guidance': [cell('scheme', 9, 15)]},
        {'id': 'discretionary-2', 'label': 'Second discretionary mark', 'maxMarks': 1, 'permittedMarks': [0, 1], 'guidance': [cell('scheme', 9, 15)]}],
        'markingGuideNote': 'The scheme gives two differences at 2 marks each and two discretionary marks at 1 each. It supplies no model comparisons. Assess two distinct responses against the original question; no model answer or per-difference partial allocation is invented.'}
    add('3E', None, question, [], 'japanese-5-6', [9], [9], total=6, rubric=rubric,
        stem=col('paper', 9, [12, 13, 14]))


def writing():
    instruction = col('paper', 10, [1, 2])
    question = instruction + '\n' + '\n'.join(p(10, r) for r in range(7, 28)) + '\n' + '\n'.join(p(11, r) for r in range(3, 26))
    criteria = [{'id': f'question-{i}', 'label': f'Selected question {i}', 'maxMarks': 7,
                 'permittedMarks': list(range(8)), 'guidance': [cell('scheme', 10, 5)]} for i in range(1, 6)]
    criteria.append({'id': 'discretionary', 'label': 'Discretionary content', 'maxMarks': 5, 'permittedMarks': list(range(6)),
                     'guidance': [cell('scheme', 10, 6), joined_selector('scheme', 10, [(26, None), (27, None)])]})
    descriptions = [col('scheme', 11, range(a, b), 190) for a, b in [(16, 23), (23, 30), (30, 37)]]
    bands = lambda spans: [{'label': f'{lo}–{hi}', 'marks': list(range(lo, hi + 1)), 'guidance': [text]} for (lo, hi), text in zip(spans, descriptions)]
    criteria.append({'id': 'expression', 'label': 'Expression', 'maxMarks': 40, 'permittedMarks': list(range(41)),
        'guidance': [joined_selector('scheme', 11, [(r, None) for r in range(1, 8)]), joined_selector('scheme', 11, [(37, None), (38, None)])],
        'bands': bands([(0, 9), (10, 27), (28, 40)]),
        'limits': [{'id': 'lower-e', 'maxMarks': 26,
                    'when': {'any': [{'criterionIds': [c['id'] for c in criteria], 'atMost': 20}, {'length': 'characters', 'below': 150}]},
                    'guidance': [joined_selector('scheme', 11, [(r, None) for r in range(8, 13)])],
                    'bands': bands([(0, 6), (7, 16), (17, 26)])}]})
    add('4', None, question, [], 'japanese-5-7', [10, 11], [10, 11], total=80, reading=[10, 11],
        rubric={'system': 'language-writing', 'taskRequirements': [instruction], 'criteria': criteria,
        'markingGuideNote': 'Choose one complete option: school OR hobbies. Both original sets of eight questions are retained. Record five distinct selected questions, each up to 7 marks, and up to 5 discretionary content marks; never mix options or score a question twice. Multi-ask questions keep the whole 7-mark maximum because no internal split is published. Expression40 lowers to26 when total content including discretionary marks is20 or less OR the response has fewer150characters. This source threshold is separate from the paper’s requested approximately200characters.'})


def from_marker(doc, page, row, group, marker):
    text = cell(doc, page, row, group)
    assert text.count(marker) == 1, (doc, page, row, marker)
    return text[text.index(marker):]


def listening():
    instruction = col('aural', 2, range(1, 9))
    questions = [(2, range(10, 15), 3), (2, range(15, 20), 4), (2, range(20, 27), 5),
                 (2, range(29, 36), 7), (2, range(36, 46), 8), (2, range(46, 56), 9),
                 (3, range(1, 6), 11), (3, range(6, 11), 12), (3, range(12, 17), 13),
                 (3, range(18, 23), 15), (3, range(23, 29), 16), (3, range(29, 38), 17)]
    for q, (page, qr, sr) in enumerate(questions, 1):
        intro_page, intro_row = (2, 9) if q <= 3 else (2, 27) if q <= 6 else (3, 0) if q <= 9 else (3, 17)
        add('LA', q, col('aural', page, qr), [point(s(3, sr, 1), 2)], 'japanese-6-1', [page], [3], reading=[page],
            stem=instruction + '\n' + col('aural', intro_page, [intro_row]))
    instruction = col('aural', 4, [5, 6, 7])
    labels = [clean_label(col('aural', 4, rows)) for rows in [[10, 12], [13, 14], [15, 16], [18], [20, 22], [23, 25], [27], [29, 31], [32], [33]]]
    c = add('LB', None, instruction + '\n' + '\n'.join(labels), [point(s(3, r, 1), 3) for r in range(19, 29)],
            'japanese-6-0', [4], [3], reading=[4], stem=col('aural', 4, range(1, 5)) + '\n' + cell('aural', 4, 9, 2) + ' — ' + cell('aural', 4, 8))
    group_rows(c, [(str(i + 1), label, i, i + 1) for i, label in enumerate(labels)])
    instruction = from_marker('aural', 5, 1, 0, 'This part') + ' ' + col('aural', 5, [2, 3, 4, 5])
    for section, q, qr, sr in [(1, 1, [8, 10, 11], 2), (1, 2, [12, 13, 14], 3), (1, 3, [15, 16], 4),
                                (1, 4, [17, 18, 19], 5), (1, 5, [20, 21], 6),
                                (2, 1, [23, 24], 8), (2, 2, [25, 26], 9), (2, 3, [28, 29, 31, 32, 33, 34, 35], 10)]:
        question = col('aural', 5, qr) if (section, q) != (1, 4) else from_marker('aural', 5, 17, 1, '4.  The') + '\n' + col('aural', 5, [18, 19])
        answer = s(4, sr, 1) + (' ' + s(4, sr, 2) if sr == 2 else '')
        note = None
        if (section, q) == (2, 3):
            note = 'Source discrepancy: the general direction says “' + col('aural', 5, [5]) + '” but this question prints four alternatives, including “' + cell('aural', 5, 35, 1) + '”. All four original options are retained.'
        add('LC', section, question, [point(answer, 3, **({'contextNote': note} if note else {}))],
            'japanese-6-0', [5], [4], str(q), reading=[5], stem=instruction + '\n' + col('aural', 5, [7 if section == 1 else 22]))
    instruction = col('aural', 6, range(1, 8))
    language = cell('scheme', 4, 12)
    for q, qr, sr in [(1, range(9, 14), 13), (2, range(14, 19), 14)]:
        add('LD', q, col('aural', 6, qr), [point(s(4, sr, 1), 2,
            contextNote=language + ' — This question asks the candidate to circle a printed Japanese/romaji expression. Selecting the correct original option earns its published 2 marks; the accepted expression itself is not evidence of an inappropriate-language response. No automatic language reduction is attached to this multiple-choice task.')],
            'japanese-6-0', [6], [4], reading=[6], stem=instruction)
    add('LD', 3, col('aural', 6, [19, 20]), [point(s(4, 15, 1), 2)], 'japanese-6-0', [6], [4], reading=[6], stem=instruction)
    labels = [clean_label(col('aural', 6, [22])), clean_label(col('aural', 6, [23]))]
    answers = [s(4, 16, 1).split('Girls ')[-1].strip(), s(4, 17).split('Boys ')[-1].strip()]
    c = add('LD', 4, col('aural', 6, [21]) + '\n' + '\n'.join(labels), [point(v, 2) for v in answers],
            'japanese-6-0', [6], [4], reading=[6], stem=instruction)
    group_rows(c, [('girls', labels[0], 0, 1), ('boys', labels[1], 1, 2)])
    add('LD', 5, col('aural', 6, [24]), [point(without_marker(s(4, 18)), 2)], 'japanese-6-0', [6], [4], reading=[6], stem=instruction)
    add('LD', 6, col('aural', 6, [27, 28]), [point(s(4, 19, 1), 2)], 'japanese-6-0', [6], [4], reading=[6], stem=instruction)
    add('LD', 7, col('aural', 6, [30, 31]), [point(s(4, 21), 2)], 'japanese-6-0', [6], [4], reading=[6], stem=instruction)
    labels = [col('aural', 6, [34]), col('aural', 6, [35])]
    note = 'The paper labels the two required descriptions (a) and (b); the scheme repeats (a) beside Shinai. Preserve both original paper prompts and the separately printed 2-mark allocations.'
    c = add('LD', 8, col('aural', 6, [33]) + '\n' + '\n'.join(labels),
            [point(s(4, 22, 2), 2, contextNote=note), point(s(4, 23, 1), 2, contextNote=note)], 'japanese-6-0', [6], [4], reading=[6], stem=instruction)
    group_rows(c, [('men', labels[0], 0, 1), ('shinai', labels[1], 1, 2)])
    note = 'Source name discrepancy: the original paper asks “' + col('aural', 6, [36]) + '”; the scheme prints “' + cell('scheme', 4, 24, 1) + '”. Retain the original John prompt and the scheme’s No answer; no extra task or different answer is inferred.'
    add('LD', 9, col('aural', 6, [36]), [point(s(4, 24, 2), 2, contextNote=note)], 'japanese-6-0', [6], [4], reading=[6], stem=instruction)


def build():
    reading_q1(); reading_q2(); reading_q3(); writing(); listening()
    census = json.loads((Path(__file__).parent / 'reviews/japanese-2010-ol-census.json').read_text())
    expected = {'ja-2010-ol-' + '-'.join(str(v).lower() for v in task['key'] if v is not None): task for task in census['tasks']}
    assert set(expected) == {c['id'] for c in CARDS}
    for card in CARDS:
        task = expected[card['id']]
        assert card['questionText'].strip()
        assert card['totalMarks'] == task['marks'], (card['id'], card['totalMarks'], task['marks'])
        assert card['sourceEvidence']['paperPages'] == task['paperPages']
        assert card['sourceEvidence']['schemePages'] == task['schemePages']
        assert not any(ord(ch) < 32 and ch not in '\n\r\t' or ch == '\ufffd' for ch in json.dumps(card, ensure_ascii=False))
    assert len(CARDS) == 61 and sum(c['totalMarks'] for c in CARDS) == 300
    assert sum('answerLanguageRule' in c for c in CARDS) == 21
    assert not any(c['id'] in ORIGINAL_IDS for c in CARDS)
    glyph = Path(__file__).with_name('glyphmap-japanese-2010-ol.json')
    return {'subjectId': 'japanese', 'sitting': '2010-ol', 'reviewedAt': '2026-11-13',
        'sources': [{'document': name, 'path': str(path.relative_to(ROOT)), 'sha256': HASHES[name], 'pagesReviewed': list(range(1, len(DOCS[name]) + 1))} for name, path in PATHS.items()],
        'cards': CARDS, 'selectors': EVIDENCE, 'status': 'source-reviewed-browser-qa-pending', 'choiceAnalysis': census['choiceBoundaries'],
        'consolidations': [], 'sourceAnswerBindings': BINDINGS,
        'glyphRecovery': {'path': str(glyph.relative_to(ROOT)), 'sha256': hashlib.sha256(glyph.read_bytes()).hexdigest()}}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('--write', action='store_true'); args = parser.parse_args()
    result = build()
    (ROOT / 'tmp/japanese-review/2010-ol-source-draft.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    (ROOT / 'tmp/japanese-review/2010-ol-crop-plan.json').write_text(json.dumps(FIGURES, ensure_ascii=False, indent=2) + '\n')
    if args.write:
        assert all(v['md5'] for v in FIGURES.values()), 'Render every planned crop before publication'
        text = '# Original PDF extraction and source-verified printed rows\n\nRaw text below is preserved unvalidated: this scheme has missing ToUnicode mappings. Use the independently image-verified, hash-bound glyph recovery in the printed rows; zero replacement characters alone does not validate Japanese decoding.\n'
        for i, page in enumerate(DOCS['scheme']):
            text += f'\n## Physical page {i + 1}\n\n### Raw extraction (unvalidated)\n\n' + page.get_text() + '\n### Source-verified printed rows\n\n' + '\n'.join(' '.join(g[2] for g in row) for row in page_rows(page)) + '\n'
        PATHS['scheme'].with_suffix('.md').write_text(text.rstrip() + '\n')
        (ROOT / 'scripts/markbank/authoring/reviews/japanese-2010-ol.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
        manifest = ROOT / 'components/MarkBank/figures-japanese.json'; previous = json.loads(manifest.read_text()); previous.update(FIGURES)
        manifest.write_text(json.dumps(previous, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'cards': len(CARDS), 'marks': sum(c['totalMarks'] for c in CARDS), 'figures': len(FIGURES)}, indent=2))
