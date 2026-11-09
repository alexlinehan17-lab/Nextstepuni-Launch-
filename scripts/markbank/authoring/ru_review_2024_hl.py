#!/usr/bin/env python3
"""Original-PDF selectors for the independently counted 2024 Higher sitting."""
import hashlib
import json
import re
from difflib import SequenceMatcher
import fitz
from ru_paper import RuPaper
from ru_scheme import RuScheme
from ru_review_2026_hl import ROOT, squash, between, bullets, as_points, bands, save_reviewed, attach_language_rule
from ru_review_2026_hl import base as base_2026, page_text

FILES = {
    'paper': ('examiner-reports/russian/papers/2024-hl-000-paper.pdf', 'c154f981d7a257665eb0a71e24e2246dc5e0e14431297819ff91017da79fc1c7'),
    'aural': ('examiner-reports/russian/papers/2024-hl-A00-paper.pdf', '98df8494df03f7ff48a5438d5202036813c4d9a7525d102ca75c9201c95a54c9'),
    'scheme': ('examiner-reports/russian/schemes/2024-hl.pdf', '3fd5f06ee6dbc78e1ef53bcaa1e1e6f9a6d822c6ee898a69f16ec34cf0aac999'),
}

def opened_sources():
    docs = {}
    for key, (path, digest) in FILES.items():
        path = ROOT / path
        assert hashlib.sha256(path.read_bytes()).hexdigest() == digest, path
        docs[key] = fitz.open(path)
    return docs

def draw_text(doc, page):
    # Preserve the wrapped two-column lists in the PDF's reading order.
    # Clip only the running footer; retain all printed answer continuations.
    return doc[page-1].get_text('text', clip=fitz.Rect(20,30,580,795), sort=False)

def base(*args, **kwargs):
    card = base_2026(*args, **kwargs)
    for field in ('id', 'questionRef'):
        card[field] = card[field].replace('2026', '2024')
    card['year'] = 2024
    card['sourceMaterial']['title'] = card['sourceMaterial']['title'].replace('2026', '2024')
    return card

def writing(docs):
    S, Q = docs['scheme'], docs['paper']
    # Read the English instructions and the complete bilingual topic pool from
    # the paper's own text order. No example essay is invented.
    paper = squash(Q[11].get_text())
    question = 'Write a short essay' + between(paper, 'Write a short essay', 'Напишите')
    question += '\n\n' + '\n'.join('• ' + part.strip() for part in paper.split('•')[1:]).split('Teideal/Title')[0].strip()
    assert 'Русская музыка' in question and 'Туризм в России' in question
    content_page = page_text(S, 13)
    content = bullets(between(content_page, 'Communication/content (C)', '2.'))
    expression = bullets(between(content_page, 'Expression (E)'))
    assert len(content) == 6 and len(expression) == 7, (content, expression)
    full, lower = bands(S, 14, 'essay')
    c = base('SE', question, 30, [12], [13, 14])
    c.pop('rows'); c.pop('tariffModel'); c['kind'] = 'rubric'
    c['rubric'] = {'system': 'language-writing', 'taskRequirements': [], 'markingGuideNote': '', 'criteria': [
        {'id': 'content', 'label': 'Communication/content (C)', 'maxMarks': 10,
         'permittedMarks': [0, 2, 4, 6, 8, 10], 'guidance': content},
        {'id': 'title-penalty', 'label': 'Essay title penalty', 'kind': 'deduction', 'deductFrom': 'content',
         'maxMarks': 1, 'permittedMarks': [0, 1], 'guidance': [content[-1]]},
        {'id': 'expression', 'label': 'Language + expression (E)', 'maxMarks': 20,
         'permittedMarks': list(range(21)), 'guidance': expression, 'bands': full,
         'limits': [{'id': 'lower-e', 'maxMarks': 14, 'when': {'any': [
                         {'criterionIds': ['content'], 'atMost': 5, 'ignoreDeductions': True},
                         {'length': 'words', 'below': 25}]}, 'bands': lower, 'guidance': [expression[2]]},
                    {'id': 'no-content', 'maxMarks': 0, 'when': {'any': [
                         {'criterionIds': ['content'], 'atMost': 0, 'ignoreDeductions': True}]}, 'guidance': [content[2]]}]},
        {'id': 'soft-sign-penalty', 'label': 'Soft signs penalty', 'kind': 'deduction', 'deductFrom': 'expression',
         'maxMarks': 2, 'permittedMarks': [0, 1, 2], 'guidance': [expression[-1]]},
    ]}
    # All six choices share the40-mark grid. One complete choice pool avoids
    # six copies of the same practice task; all six prompts fit on page13.
    question = '\n'.join(page_text(Q, p, (297, 35, 580, 775)) for p in (13,))
    question = 'Write a piece' + between(question, 'Write a piece')
    assert all(term in question for term in ('1. LETTER', '2. NARRATIVE', '3. DISCUSSION', 'having a pet animal.'))
    g = base('GW', question, 40, [13], [15, 16, 17])
    g.pop('rows'); g.pop('tariffModel'); g['kind'] = 'rubric'
    scheme = page_text(S, 16)
    content = bullets(between(scheme, 'Communication/content (C)', '2.'))
    expression = bullets(between(scheme, 'Expression (E):', 'Lower E'))
    full, lower = bands(S, 16, 'guided')
    coherence, _ = bands(S, 17, 'coherence')
    g['rubric'] = {'system': 'language-writing', 'taskRequirements': [squash(page_text(S, 15))],
                   'markingGuideNote': '', 'criteria': [
        {'id': 'content', 'label': 'Communication + content (C)', 'maxMarks': 15,
         'permittedMarks': list(range(16)), 'guidance': content},
        {'id': 'expression', 'label': 'Language + expression (E)', 'maxMarks': 15,
         'permittedMarks': list(range(16)), 'guidance': expression, 'bands': full,
         'limits': [{'id': 'lower-e', 'maxMarks': 10, 'when': {'any': [
                         {'criterionIds': ['content'], 'atMost': 7}, {'length': 'words', 'below': 60}]},
                     'bands': lower, 'guidance': [expression[1]]}]},
        {'id': 'coherence', 'label': 'Textual coherence (TC)', 'maxMarks': 10,
         'permittedMarks': list(range(11)), 'guidance': [], 'bands': coherence},
        {'id': 'soft-sign-penalty', 'label': 'Soft sign penalty', 'kind': 'deduction', 'deductFrom': 'expression',
         'maxMarks': 2, 'permittedMarks': [0, 2], 'guidance': [expression[-1]]},
    ]}
    return [c, g]

def reading(docs, P):
    S = docs['scheme']
    cards = []
    text = '\n'.join(draw_text(S, p) for p in (4, 5, 6))
    heads = list(re.finditer(r'^\s*([1-4])\.\s*\((i{1,3}|iv)\)\s+(?=[A-Z])', text, re.M))
    general = bullets(text[:heads[0].start()].split('Question 1.1')[0])
    assert len(general) == 4
    keys = [(1, 'i', 2), (1, 'ii', 2), (2, 'i', 1), (2, 'ii', 1),
            (2, 'iii', 1), (2, 'iv', 2), (3, 'i', 2), (3, 'ii', 1),
            (3, 'iii', 2), (3, 'iv', 2), (4, 'i', 2), (4, 'ii', 2)]
    assert len(heads) == len(keys)
    for i, (head, (item, roman, count)) in enumerate(zip(heads, keys)):
        assert (int(head.group(1)), head.group(2)) == (item, roman)
        block = text[head.end():heads[i+1].start() if i+1 < len(heads) else len(text)]
        cue, body = block.split('assign 2 marks:', 1)
        cue = squash(re.sub(r'\d+\s*x\s*2\s*marks', '', cue))
        question, page, source = P.find('C1', item, roman, cue)
        assert question and source.side == 'R', (item, roman, cue)
        partials = {}
        independent_partial = None
        if 'assign 1 mark:' in body:
            body, partial = body.split('assign 1 mark:', 1)
            partial = bullets(partial)
            if (item, roman) == (2, 'i'):
                partials = {0: partial}
            elif (item, roman) == (3, 'ii'):
                partials = {2: partial}
            elif (item, roman) == (3, 'iii'):
                assert partial == ['the cat was put into the shed']
                independent_partial = partial[0]
            else:
                raise AssertionError((item, roman, partial))
        answers = bullets(body)
        c = base('C1', question, count*2, [2, 3, 4], [4, 5, 6], item, roman)
        c['review']['questionPages'] = [page]
        as_points(c, answers, count, partials)
        c['rubric']['taskRequirements'] = general
        if independent_partial:
            c['rubric']['groups'].append({'id': 'partial-shed', 'label': 'Other printed partial answer',
                'answerCount': 1, 'rows': [{'id': 'partial', 'text': independent_partial, 'marks': 1}]})
            c['rubric']['markingGuideNote'] = 'The scheme separately accepts the shed detail for 1 mark under the same two-detail limit.'
        cards.append(c)
    assert sum(c['totalMarks'] for c in cards) == 40

    summary = '\n'.join(draw_text(S, p) for p in (8, 9))
    rule = 'Award 2 marks for each ' + squash(between(summary, 'Award 2 marks for each', 'Part 1.'))
    assert 'of 4 details (up to 8 marks) AND 2 discretionary marks' in rule
    for item, counts in [(1, (7, 4)), (2, (6, 4)), (3, (6, 1)), (4, (6, 3))]:
        block = between(summary, f'Part {item}.', f'Part {item+1}.' if item < 4 else None)
        cue, rest = block.split('Main points:', 1)
        cue = squash(re.sub(r'10\s*marks', '', cue))
        question, page, source = P.find('C2', item, None, cue)
        assert question and source.side == 'R'
        main, secondary = rest.split('Secondary details:', 1)
        main_answers, secondary = bullets(main), bullets(secondary)
        assert (len(main_answers), len(secondary)) == counts, (item, main_answers, secondary)
        c = base('C2', question, 10, [6, 7, 8], [8, 9], item)
        c['review']['questionPages'] = [page]
        as_points(c, main_answers + secondary, 4, steps=[0, 1, 2],
                  labels=['Main point']*len(main_answers) + ['Secondary detail']*len(secondary))
        c['rubric']['taskRequirements'] = [rule]
        c['rubric']['criteria'] = [{'id': 'summary-skills', 'label': 'Discretionary marks',
            'maxMarks': 2, 'permittedMarks': [0, 1, 2], 'guidance': [rule],
            'limits': [{'id': 'incomplete-response', 'maxMarks': 1,
                'when': {'any': [{'flag': 'incomplete-response', 'prompt': squash(rule[rule.index('If a candidate fails'):])}]},
                'guidance': [rule]}]}]
        cards.append(c)
    return cards


def language_and_matching(docs, P):
    S, Q = docs['scheme'], docs['paper']
    scheme = RuScheme(2024, 'hl')
    cards = []
    for unit, page, paper_pages in [('LA1', 7, [2, 3, 4, 5]), ('LA2', 10, [6, 7, 8, 9])]:
        tasks = scheme.tasks(unit)
        assert len(tasks) == 2
        for roman, task in zip(('i', 'ii'), tasks):
            question = P.instruction(unit, roman)
            assert question
            if unit == 'LA2' and roman == 'i':
                pool = between(draw_text(S, 10), 'Cемантическое поле:', 'This list is not exhaustive.')
                answers = [part.strip() for bullet in bullets(pool)
                           for part in re.split(r',\s*(?![^()]*\))', bullet) if part.strip()]
                assert len(answers) > 25 and len(set(answers)) == len(answers)
            else:
                answers = [f'{left} — {right}' for left, right in task.pairs]
                assert len(answers) == 5
            c = base(unit, question, 10, paper_pages, [page], roman=roman)
            as_points(c, answers, 5)
            if unit == 'LA2' and roman == 'i':
                guidance = squash(between(draw_text(S, 10), 'This list is not exhaustive.', 'OR'))
                c['rubric']['taskRequirements'] = ['This list is not exhaustive.', guidance]
            cards.append(c)
    question = squash(page_text(Q, 10, (294, 65, 580, 174)))
    question = question[question.index('Read the following brief news items.'):]
    table = S[10].find_tables().tables[0].extract()
    answers = [squash(row[0]) for row in table if row[0] and re.fullmatch(r'\d+', squash(row[0]))]
    assert answers == ['8', '1', '10', '3', '9', '4', '7', '5', '6', '2'], table
    c = base('SD', question, 20, [10], [11])
    as_points(c, [f'{i} — {a}' for i, a in enumerate(answers, 1)], 10)
    c['rubric']['markingGuideNote'] = 'Rows are numbered from top to bottom in the original table. Award 2 marks for each correct answer.'
    cards.append(c)
    question = squash(page_text(Q, 11, (306, 132, 580, 280)))
    question = question[question.index('Read through the following text.'):]
    passage = between(page_text(S, 12), '15 x 2 marks')
    forms = re.findall(r'\(([^()]+)\)', passage)
    assert len(forms) == 15
    c = base('GR', question, 30, [11], [12])
    as_points(c, forms, 15)
    c['rubric']['taskRequirements'] = bullets(between(page_text(S, 12), 'Note:', 'Award 2 marks'))
    cards.append(c)
    return cards


def listening(docs, P):
    S = docs['scheme']
    audio = next(row['source'] for row in json.loads((ROOT / 'data/russianAudio.json').read_text()) if row['year'] == 2024)
    asks = P.aural_asks()
    assert len(asks) == 24
    cards = []
    sections = [(1, 18, [2], [2, 2, 2, 2, 1, 1]), (2, 19, [3, 4], [2, 1, 1, 2, 2, 2]),
                (3, 20, [5], [2, 1, 2, 2, 2, 1]), (4, 21, [6], [2, 2, 2, 1, 1, 2])]
    general = bullets(between(draw_text(S, 18), 'General:', 'SECTION I'))
    assert any('contradictory answer nullifies the correct answer' in rule for rule in general)
    assert any('no penalty for excess material' in rule for rule in general)
    for section, page, paper_pages, counts in sections:
        unit = f'L{section}'
        source = draw_text(S, page)
        assert 'Award 2 marks for each detail' in squash(source)
        heads = list(re.finditer(r'^\s*(\d)\.\s*\((i{1,3})\)\s*', source, re.M))
        questions = [a for a in asks if a[0] == unit]
        assert len(heads) == len(questions) == len(counts), (unit, heads)
        for index, (head, ask, count) in enumerate(zip(heads, questions, counts)):
            _, item, roman, question = ask
            block = source[head.end():heads[index+1].start() if index+1 < len(heads) else len(source)]
            block = re.sub(r'Segment\s+\d+:?', '', block)
            cue, rest = block.split('•', 1)
            cue = squash(cue)
            assert SequenceMatcher(None, squash(question).lower(), cue.lower()).ratio() > .9, (question, cue)
            assert (int(head.group(1)), head.group(2)) == (item, roman)
            answers = bullets('•' + rest)
            c = base(unit, question, count*2, paper_pages, [page], item, roman)
            as_points(c, answers, count)
            if section == 1:
                topic = 'russian-0-1' if item == 2 else 'russian-0-9'
            elif section == 2:
                topic = 'russian-0-6' if item == 3 and roman == 'ii' else 'russian-0-3'
            elif section == 3:
                topic = 'russian-0-9' if (item == 1 and roman == 'ii') or item == 3 else 'russian-0-5'
            else:
                topic = 'russian-0-7' if item == 1 and roman == 'i' else 'russian-0-3' if item == 1 else 'russian-2-5'
            c['topicId'] = topic
            c['additionalTopicIds'] = ['russian-1-0']
            c['rubric']['taskRequirements'] = general
            c['sourceMaterial']['kind'] = 'source-question'
            c['sourceMaterial']['presentationNote'] = 'Listen to the official recording and answer the printed question. The transcript is not shown before answering.'
            c['audioMaterial'] = audio
            c['review']['guidancePages'] = [18]
            cards.append(c)
    assert len(cards) == 24 and sum(c['totalMarks'] for c in cards) == 80
    return cards


def build():
    docs = opened_sources()
    P = RuPaper(2024, 'hl')
    cards = reading(docs, P) + language_and_matching(docs, P) + writing(docs) + listening(docs, P)
    assert len(cards) == 48 and sum(c['totalMarks'] for c in cards) == 320
    old_ids = {c['id'] for c in json.loads((ROOT / 'scripts/markbank/authored/russian.json').read_text())}
    for c in cards:
        if c['id'] in old_ids:
            c['review']['correctsExisting'] = True
    attach_language_rule(cards, docs['scheme'])
    assert sum(c['review'].get('correctsExisting', False) for c in cards) == 20
    return cards


if __name__ == '__main__':
    save_reviewed(build())
