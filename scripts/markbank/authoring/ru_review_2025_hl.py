#!/usr/bin/env python3
"""Original-PDF selectors for the independently counted 2025 Higher sitting."""
import hashlib
import json
import re
from difflib import SequenceMatcher
import fitz
from ru_paper import RuPaper, bag, score
from ru_scheme import RuScheme
from ru_review_2026_hl import ROOT, squash, between, bullets, as_points, bands, save_reviewed, attach_language_rule
from ru_review_2026_hl import base as base_2026, page_text

FILES = {
    'paper': ('examiner-reports/russian/papers/2025-hl-000-paper.pdf', '671650c672d92ab191f615700de4dfd7077835d86223a2e976a8818809c8d97f'),
    'aural': ('examiner-reports/russian/papers/2025-hl-A00-paper.pdf', 'edcc2149eddeababbeb62a5e471c22de654b4fb74bbf671b2e12c0e5abb921fe'),
    'scheme': ('examiner-reports/russian/schemes/2025-hl.pdf', '3c74de1d1d5d35a4e0e9ada2b5e7754446722444003f480a2bd876c90c27a52b'),
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
    # p20's final accepted answer ends at y784; the footer begins at y808.
    return doc[page-1].get_text('text', clip=fitz.Rect(20,30,580,795), sort=False)

def base(*args, **kwargs):
    card = base_2026(*args, **kwargs)
    for field in ('id', 'questionRef'):
        card[field] = card[field].replace('2026', '2025')
    card['year'] = 2025
    card['sourceMaterial']['title'] = card['sourceMaterial']['title'].replace('2026', '2025')
    return card

def writing(docs):
    S, Q = docs['scheme'], docs['paper']
    # Read the English instructions and the complete bilingual topic pool from
    # the paper's own text order. No example essay is invented.
    paper = squash(Q[11].get_text())
    question = 'Write a short essay' + between(paper, 'Write a short essay', 'Напишите')
    question += '\n\n' + '\n'.join('• ' + part.strip() for part in paper.split('•')[1:]).split('Teideal/Title')[0].strip()
    assert 'Русская национальная кухня' in question and 'Города России' in question
    content_page = page_text(S, 12)
    content = bullets(between(content_page, 'Communication/content (C)', '2.'))
    expression = bullets(between(content_page, 'Expression (E)'))
    assert len(content) == 7 and len(expression) == 7, (content, expression)
    full, lower = bands(S, 13, 'essay')
    c = base('SE', question, 30, [12], [12, 13])
    c.pop('rows'); c.pop('tariffModel'); c['kind'] = 'rubric'
    c['rubric'] = {'system': 'language-writing', 'taskRequirements': [], 'markingGuideNote': '', 'criteria': [
        {'id': 'content', 'label': 'Communication/content (C)', 'maxMarks': 10,
         'permittedMarks': [0, 2, 4, 6, 8, 10], 'guidance': content,
         'limits': [{'id': 'one-subject', 'maxMarks': 8,
                     'when': {'any': [{'flag': 'one-subject', 'prompt': content[-1]}]}, 'guidance': [content[-1]]}]},
        {'id': 'title-penalty', 'label': 'Essay title penalty', 'kind': 'deduction', 'deductFrom': 'content',
         'maxMarks': 1, 'permittedMarks': [0, 1], 'guidance': [content[-2]]},
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
    # six copies of the same practice task and includes3(b) on the next page.
    question = '\n'.join(page_text(Q, p, (297, 35, 580, 775)) for p in (13,))
    question = 'Write a piece' + between(question, 'Write a piece')
    assert all(term in question for term in ('1. LETTER', '2. NARRATIVE', '3. DISCUSSION', 'professional tour guide.'))
    g = base('GW', question, 40, [13], [14, 15, 16])
    g.pop('rows'); g.pop('tariffModel'); g['kind'] = 'rubric'
    scheme = page_text(S, 15)
    content = bullets(between(scheme, 'Communication/content (C)', '2.'))
    expression = bullets(between(scheme, 'Expression (E):', 'Lower E'))
    full, lower = bands(S, 15, 'guided')
    coherence, _ = bands(S, 16, 'coherence')
    g['rubric'] = {'system': 'language-writing', 'taskRequirements': [squash(page_text(S, 14))],
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
    text = '\n'.join(draw_text(S, p) for p in (4, 5))
    heads = list(re.finditer(r'^\s*([1-4])\.\s*(?:\((i{1,3})\))?\s+(?=[A-Z])', text, re.M))
    keys = [(1, 'i', 3), (1, 'ii', 1), (1, 'iii', 1), (2, 'i', 3), (2, 'ii', 2),
            (3, 'i', 3), (3, 'ii', 3), (3, 'iii', 1), (4, None, 3)]
    assert len(heads) == len(keys)
    for i, (head, (item, roman, count)) in enumerate(zip(heads, keys)):
        assert (int(head.group(1)), head.group(2)) == (item, roman)
        block = text[head.end():heads[i+1].start() if i+1 < len(heads) else len(text)]
        cue, body = block.split('assign 2 marks:', 1)
        cue = squash(re.sub(r'\d+\s*x\s*2\s*marks', '', cue))
        question, page, source = P.find('C1', item, roman, cue)
        assert question and source.side == 'R', (item, roman, cue)
        partials = {}
        if 'assign 1 mark:' in body:
            body, partial = body.split('assign 1 mark:', 1)
            partials = {0: bullets(partial)}
        answers = bullets(body)
        c = base('C1', question, count*2, [2, 3, 4], [4, 5], item, roman)
        c['review']['questionPages'] = [page]
        as_points(c, answers, count, partials)
        cards.append(c)
    assert sum(c['totalMarks'] for c in cards) == 40

    summary = '\n'.join(draw_text(S, p) for p in (7, 8, 9))
    summary = re.split(r'Question\s+2\.2', summary)[0]
    rule = 'Award 2 marks for each ' + squash(between(summary, 'Award 2 marks for each', 'Part 1.'))
    assert 'of 4 details (up to 8 marks) AND 2 discretionary marks' in rule
    for item, counts in [(1, (11, 4)), (2, (8, 1)), (3, (9, 3)), (4, (10, 2))]:
        block = between(summary, f'Part {item}.', f'Part {item+1}.' if item < 4 else None)
        cue, rest = block.split('Main points:', 1)
        cue = squash(re.sub(r'10\s*marks', '', cue))
        question, page, source = P.find('C2', item, None, cue)
        assert question and source.side == 'R'
        main, secondary = rest.split('Secondary details:', 1)
        if item == 2:
            advantages, disadvantages = main.split('Disadvantages (at least 2 should be mentioned):')
            advantages, disadvantages = bullets(advantages), bullets(disadvantages)
            assert len(advantages) == len(disadvantages) == 4
            main_answers = advantages + disadvantages
        else:
            main_answers = bullets(main)
        secondary = bullets(secondary)
        assert (len(main_answers), len(secondary)) == counts, (item, main_answers, secondary)
        c = base('C2', question, 10, [6, 7, 8], [7, 8, 9], item)
        c['review']['questionPages'] = [page]
        as_points(c, main_answers + secondary, 4, steps=[0, 1, 2],
                  labels=['Main point']*len(main_answers) + ['Secondary detail']*len(secondary))
        if item == 2:
            # Printed quotas apply independently. The secondary biographical
            # detail is retained as additional-detail evidence for the scheme's
            # discretionary component, not a replacement for a required side.
            c['rubric']['groups'] = [
                {'id': side.lower(), 'label': side, 'answerCount': 2,
                 'rows': [{'id': f'detail-{i+1}', 'text': answer, 'marks': 2,
                           'steps': [0, 1, 2]} for i, answer in enumerate(answers)]}
                for side, answers in [('Advantages', advantages), ('Disadvantages', disadvantages)]]
            c['rubric']['count'] = 2
        c['rubric']['taskRequirements'] = [rule]
        c['rubric']['criteria'] = [{'id': 'summary-skills', 'label': 'Discretionary marks',
            'maxMarks': 2, 'permittedMarks': [0, 1, 2],
            'guidance': [rule] + (secondary if item == 2 else []),
            'limits': [{'id': 'incomplete-response', 'maxMarks': 1,
                'when': {'any': [{'flag': 'incomplete-response', 'prompt': squash(rule[rule.index('If a candidate fails'):])}]},
                'guidance': [rule]}]}]
        cards.append(c)
    return cards


def language_and_matching(docs, P):
    S, Q = docs['scheme'], docs['paper']
    scheme = RuScheme(2025, 'hl')
    cards = []
    for unit, page, paper_pages in [('LA1', 6, [2, 5]), ('LA2', 9, [6, 7, 8, 9])]:
        tasks = scheme.tasks(unit)
        assert len(tasks) == 2
        for roman, task in zip(('i', 'ii'), tasks):
            question = P.instruction(unit, roman)
            assert question
            if unit == 'LA1' and roman == 'i':
                pool = between(draw_text(S, 6), 'Cемантическое поле:', 'Etc.')
                # Commas inside a parenthesized alternative do not create a
                # new option; retain the complete source phrase there.
                answers = [part.strip() for bullet in bullets(pool)
                           for part in re.split(r',\s*(?![^()]*\))', bullet)]
                assert len(answers) > 25 and len(set(answers)) == len(answers)
            else:
                answers = [f'{left} — {right}' for left, right in task.pairs]
                assert len(answers) == 5
            c = base(unit, question, 10, paper_pages, [page], roman=roman)
            as_points(c, answers, 5)
            cards.append(c)
    question = squash(page_text(Q, 10, (294, 65, 580, 174)))
    question = question[question.index('Read the following brief news items.'):]
    table = S[9].find_tables().tables[0].extract()
    # The actual two-column answer table contains the printed row's answer.
    answers = [squash(row[0]) for row in table if row[0] and re.fullmatch(r'\d+', squash(row[0]))]
    assert answers == ['4', '9', '7', '5', '6', '3', '2', '10', '1', '8'], table
    c = base('SD', question, 20, [10], [10])
    as_points(c, [f'{i} — {a}' for i, a in enumerate(answers, 1)], 10)
    c['rubric']['markingGuideNote'] = 'Rows are numbered from top to bottom in the original table. Award 2 marks for each correct answer.'
    cards.append(c)
    question = squash(page_text(Q, 11, (306, 132, 580, 280)))
    question = question[question.index('Read through the following text.'):]
    passage = between(page_text(S, 11), '15 x 2 marks')
    forms = re.findall(r'\(([^()]+)\)', passage)
    assert len(forms) == 15
    c = base('GR', question, 30, [11], [11])
    as_points(c, forms, 15)
    c['rubric']['taskRequirements'] = bullets(between(page_text(S, 11), 'Note:', 'Award 2 marks'))
    cards.append(c)
    return cards


def listening(docs, P):
    S = docs['scheme']
    audio = next(row['source'] for row in json.loads((ROOT / 'data/russianAudio.json').read_text()) if row['year'] == 2025)
    asks = P.aural_asks()
    assert len(asks) == 22
    cards = []
    sections = [(1, 17, [2, 3], [2, 2, 2, 1, 2, 1]), (2, 18, [4], [2]*5),
                (3, 19, [5], [3, 1, 2, 1, 2, 1]), (4, 20, [6, 7], [2]*5)]
    general = bullets(between(draw_text(S, 17), 'General:', 'SECTION I'))
    for section, page, paper_pages, counts in sections:
        unit = f'L{section}'
        source = draw_text(S, page)
        heads = list(re.finditer(r'^\s*(\d)\.\s*\((i{1,3})\)\s*', source, re.M))
        questions = [a for a in asks if a[0] == unit]
        assert len(heads) == len(questions) == len(counts), (unit, heads)
        for index, (head, ask, count) in enumerate(zip(heads, questions, counts)):
            _, item, roman, question = ask
            block = source[head.end():heads[index+1].start() if index+1 < len(heads) else len(source)]
            block = re.sub(r'Segment\s+\d+', '', block)
            cue, rest = block.split('•', 1)
            cue = squash(cue)
            pronoun_cue = (section == 4 and 'Anton Chekhov’s' in question
                           and squash(question).replace('Anton Chekhov’s', 'his') == cue)
            assert SequenceMatcher(None, squash(question).lower(), cue.lower()).ratio() > .9 or pronoun_cue, (question, cue)
            source_key = (int(head.group(1)), head.group(2))
            mismatch = {(1, 3, 'ii'): (4, 'ii'), (2, 1, None): (1, 'i'), (4, 3, None): (3, 'i')}
            assert source_key == mismatch.get((section, item, roman), (item, roman))
            rest = '•' + rest
            partials = {}
            restaurant = None
            if '1 mark Gym' in rest:
                rest, partial = rest.split('1 mark ', 1)
                parts = [s.strip() for s in squash(partial).split('/')]
                assert parts == ['Gym', 'Wi-Fi', 'restaurant']
                partials = {0: [parts[1]], 2: [parts[0]]}
                restaurant = parts[2]
            answers = bullets(rest)
            c = base(unit, question, count*2, paper_pages, [page], item, roman)
            as_points(c, answers, count, partials)
            if restaurant:
                c['rubric']['groups'].append({'id': 'partial-restaurant', 'label': 'Other printed partial answer',
                    'answerCount': 1, 'rows': [{'id': 'partial', 'text': restaurant, 'marks': 1}]})
                c['rubric']['markingGuideNote'] = 'The scheme lists “restaurant” separately as a 1-mark partial answer and does not assign it to a particular full answer. Claim only distinct details under the printed two-detail limit.'
            if source_key != (item, roman):
                c['rubric']['markingGuideNote'] += f' The scheme prints {source_key[0]}({source_key[1]}); the booklet prints {item}' + (f'({roman})' if roman else '') + '. This card follows the question booklet.'
            c['rubric']['taskRequirements'] = general
            c['sourceMaterial']['kind'] = 'source-question'
            c['sourceMaterial']['presentationNote'] = 'Listen to the official recording and answer the printed question. The transcript is not shown before answering.'
            c['audioMaterial'] = audio
            c['review']['guidancePages'] = [17]
            # Filing is based on each source's communicative domain.
            if section == 1:
                topic = 'russian-0-8' if item == 3 else 'russian-0-9'
            elif section == 2:
                topic = 'russian-0-3' if item == 1 else 'russian-0-5'
            elif section == 3:
                topic = 'russian-0-8' if item == 1 else 'russian-0-2' if item == 2 and roman == 'ii' else 'russian-0-9'
            else:
                topic = ('russian-0-1' if roman == 'i' else 'russian-0-3') if item == 1 else 'russian-0-4' if item == 2 and roman == 'i' else 'russian-2-5'
            c['topicId'] = topic
            c['additionalTopicIds'] = ['russian-1-0']
            cards.append(c)
    assert len(cards) == 22 and sum(c['totalMarks'] for c in cards) == 80
    return cards


def build():
    docs = opened_sources()
    P = RuPaper(2025, 'hl')
    cards = reading(docs, P) + language_and_matching(docs, P) + writing(docs) + listening(docs, P)
    assert len(cards) == 43 and sum(c['totalMarks'] for c in cards) == 320
    old_ids = {c['id'] for c in json.loads((ROOT / 'scripts/markbank/authored/russian.json').read_text())}
    for c in cards:
        if c['id'] in old_ids:
            c['review']['correctsExisting'] = True
    attach_language_rule(cards, docs['scheme'])
    assert sum(c['review'].get('correctsExisting', False) for c in cards) == 16
    from ru_summary_language_rules import attach_reviewed_summary_language_exceptions
    return attach_reviewed_summary_language_exceptions(cards)


if __name__ == '__main__':
    save_reviewed(build())
