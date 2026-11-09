#!/usr/bin/env python3
"""Source-reviewed 2026 Higher Russian. No legacy deck is reauthored here.

Every answer is extracted from a pinned original PDF, with reviewed page
boundaries. The existing reader supplies wording-aligned question candidates;
its answer output is deliberately not used (it conflates page furniture,
question continuations and partial-credit instructions with answers).
"""
import hashlib
import json
import re
from difflib import SequenceMatcher
from pathlib import Path

import fitz
from ru_paper import RuPaper, bag, score
from ru_topics import concept_for, topic_for

ROOT = Path(__file__).resolve().parents[3]
FILES = {
    'paper': ('examiner-reports/russian/papers/2026-hl-000-paper.pdf',
              'e9fd3cede429b88a1f530fe18a494af3e2cdeb98ba218c932c3d4a72fe147992'),
    'aural': ('examiner-reports/russian/papers/2026-hl-A00-paper.pdf',
              'c0c4ed2e47c5476de8d68179f90acf383c79d2648e77b7bc34589d32caeccb6d'),
    'scheme': ('examiner-reports/russian/schemes/2026-hl.pdf',
               'e56810faf2cb2b34e30216c07b4ff771d1cc6f99b91fb6fcf1d47d045d8265be'),
}


def squash(text):
    return ' '.join(text.split())


def opened_sources():
    result = {}
    for key, (relative, digest) in FILES.items():
        path = ROOT / relative
        assert hashlib.sha256(path.read_bytes()).hexdigest() == digest, path
        result[key] = fitz.open(path)
    return result


def page_text(doc, page, box=None):
    # The scheme's final answer on p4 reaches y769. Its running footer starts
    # at y779, so clipping at760 silently loses a real priced answer.
    return '\n'.join(line.rstrip() for line in doc[page - 1].get_text(
        'text', clip=fitz.Rect(box or (20, 30, 580, 775)), sort=True).splitlines())


def between(text, start, end=None):
    assert text.count(start) == 1, (start, text.count(start))
    result = text.split(start, 1)[1]
    if end:
        assert end in result, end
        result = result.split(end, 1)[0]
    return result


def bullets(text):
    # Source selectors delimit each list first. This only rejoins line wraps;
    # it never supplies a missing answer or translates the Russian words.
    return [squash(part) for part in re.split(r'\s*•\s*', text)[1:] if squash(part)]


def menu(options, count, price, note=''):
    return {'id': 'answers', 'kind': 'anyN', 'verbatim': 'The answers the scheme accepts',
            'marks': None, 'contextNote': note,
            'group': {'claimMax': count, 'perOption': price, 'options': options}}


def base(unit, text, total, pages, scheme_pages, item=None, roman=None):
    suffix = f'-{item}' if item is not None else ''
    suffix += f'-{roman}' if roman else ''
    printed_question = item if item is not None else {'SD': 3, 'GR': 1, 'SE': 2, 'GW': 3}.get(unit)
    ref = f'2026 HL Section {unit} Q' + (str(printed_question) if printed_question is not None else '')
    ref += f'({roman})' if roman else ''
    return {
        'id': f'ru-2026-hl-{unit.lower()}{suffix}', 'subjectId': 'russian',
        'level': 'higher', 'year': 2026, 'section': unit,
        'topicId': ('russian-1-0' if unit.startswith('L') and unit[1:].isdigit() else topic_for(unit)), 'conceptId': concept_for(text),
        'questionRef': ref, 'questionText': text, 'tariffModel': {'kind': 'fixed'},
        'totalMarks': total, 'rows': [],
        'sourceMaterial': {'kind': 'source-text', 'label': 'Official question and source',
                           'title': f'2026 Higher Russian — {unit}', 'pages': pages,
                           'attribution': '© State Examinations Commission.',
                           'presentationNote': 'Read the complete printed source and instructions before answering.'},
        'notes': f'Source reviewed against the original paper and marking scheme, pages {", ".join(map(str, scheme_pages))}.',
        'review': {'paperPages': pages, 'schemePages': scheme_pages, 'component': 'A00' if unit in ('L1', 'L2', 'L3', 'L4') else '000'},
    }


def as_points(card, answers, count, partials=None, steps=None, labels=None):
    card.pop('rows', None)
    card.pop('tariffModel', None)
    card['kind'] = 'rubric'
    groups = []
    for i, answer in enumerate(answers):
        rows = [{'id': 'full', 'text': answer, 'marks': 2}]
        if steps:
            rows[0]['steps'] = steps
        for j, partial in enumerate((partials or {}).get(i, [])):
            rows.append({'id': f'partial-{j+1}', 'text': partial, 'marks': 1})
        groups.append({'id': f'answer-{i+1}', 'label': (labels or [])[i] if labels else f'Answer {i+1}',
                       'answerCount': 1, 'rows': rows})
    card['rubric'] = {'system': 'language-points', 'taskRequirements': [], 'count': count,
                      'groups': groups, 'markingGuideNote': ''}
    return card


def listening(docs, P):
    source = '\n'.join(page_text(docs['scheme'], p) for p in range(18, 23))
    general = bullets(between(source, 'General:', 'SECTION I'))
    asks = P.aural_asks()
    assert len(asks) == 24, asks
    audio = next(row['source'] for row in json.loads((ROOT / 'data/russianAudio.json').read_text()) if row['year'] == 2026)
    cards = []
    section_names = ['I', 'II', 'III', 'IV']
    sections = re.split(r'SECTION\s+(?:IV|III|II|I)\b', source)
    assert len(sections) == 5
    pages = {'L1': [2, 3], 'L2': [4], 'L3': [5], 'L4': [6, 7]}
    scheme_pages = {'L1': [18, 19], 'L2': [19, 20], 'L3': [20, 21], 'L4': [21, 22]}
    for n, roman_section in enumerate(section_names, 1):
        unit = f'L{n}'
        text = sections[n]
        # p21 prints "3 (i)."; preserve the paper address while recognizing
        # this source layout explicitly. Tariffs can sit before their header.
        heads = list(re.finditer(r'^\s*(\d)\s*\.?\s*(?:\((i{1,3})\)\s*\.?)?\s+(?=[A-Z])', text, re.M))
        assert len(heads) == 6, (unit, [(h.group(),h.start()) for h in heads])
        for i, head in enumerate(heads):
            item, roman = int(head.group(1)), head.group(2)
            block = text[head.end():heads[i+1].start() if i+1 < len(heads) else len(text)]
            block = re.sub(r'^\s*Segment\s+\d+\s*$', '', block, flags=re.M)
            # Prices are checked against each question's printed number of
            # details and the section's explicit2marks-per-detail direction.
            prices = re.findall(r'\((\d)x2 marks\)', block)
            block = re.sub(r'\(\d+x2 marks\)', '', block)
            cue, rest = block.split('•', 1)
            cue = squash(cue)
            candidates = [a for a in asks if a[:3] == (unit, item, roman)]
            assert len(candidates) == 1, (unit, item, roman)
            question = candidates[0][3]
            reworded = (unit, item, roman) == ('L2', 3, None) and (
                squash(question) == 'Give two details about Peter’s future plans.'
                and cue == 'What are Peter’s future plans? Give two details.')
            reworded |= ((unit, item, roman) == ('L4', 2, 'i')
                        and cue == squash(question) + ' Give one detail.')
            assert (SequenceMatcher(None, squash(question).lower(), cue.lower()).ratio() > .93
                    or score(bag(question), bag(cue)) > .9 or reworded), (question, cue)
            count = 3 if 'three details' in question else 2 if 'two details' in question else 1
            assert str(count) in prices or (unit, item, roman) in [('L2', 2, 'i'), ('L3', 1, 'ii')], (unit,item,roman,prices)
            rest = '•' + rest
            partials = {}
            if '1 mark for' in rest:
                rest, partial_text = rest.split('1 mark for', 1)
                partial_text = squash(partial_text)
            else:
                partial_text = None
            if 'study at university 1 mark' in rest:
                rest = rest.split('study at university 1 mark')[0]
                partial_text = 'study at university'
            answers = bullets(rest)
            alternative_degree = None
            if partial_text:
                if unit == 'L3' and item == 2 and roman == 'ii':
                    partials = {1: [partial_text.split(',')[0].strip()],
                                3: [part.strip() for part in partial_text.split(',')[1:3]],
                                5: [partial_text.split(',')[3].strip()]}
                elif unit == 'L2' and item == 3:
                    # Both degree descriptions refine the same lesser answer.
                    # One full/partial group prevents claiming the generic
                    # university detail alongside either full degree detail.
                    assert answers[:2] == ['study International Relations', 'study Linguistics at university']
                    alternative_degree = answers.pop(1)
                    partials = {0: [partial_text]}
                else:
                    partials = {len(answers)-1: [partial_text]}
            card = base(unit, question, count*2, pages[unit], scheme_pages[unit], item, roman)
            # Russian has no separate canonical aural strand. File each ask
            # under its actual communicative domain, with the target-language
            # material strand as the additional listening-skill connection.
            if unit == 'L1':
                topic = ('russian-0-3' if roman == 'ii' else 'russian-0-4') if item == 1 else 'russian-0-9' if item == 2 else 'russian-0-14'
            elif unit == 'L2':
                topic = 'russian-0-1' if item == 1 and roman == 'i' else 'russian-0-6' if item == 3 else 'russian-0-3'
            elif unit == 'L3':
                topic = 'russian-0-9' if item == 1 and roman == 'ii' else 'russian-0-3' if item == 3 else 'russian-0-5'
            else:
                topic = 'russian-0-7' if item == 1 else 'russian-0-4' if item == 2 else 'russian-2-5'
            card['topicId'] = topic
            card['additionalTopicIds'] = ['russian-1-0']
            card = as_points(card, answers, count, partials)
            if alternative_degree:
                card['rubric']['groups'][0]['rows'].insert(1, {
                    'id': 'alternative', 'text': alternative_degree, 'marks': 2})
            card['rubric']['taskRequirements'] = general
            card['sourceMaterial']['kind'] = 'source-question'
            card['sourceMaterial']['presentationNote'] = 'Listen to the official recording and answer the printed question. The transcript is not shown before answering.'
            card['audioMaterial'] = audio
            card['review']['guidancePages'] = [18]
            if unit == 'L4' and item == 1 and roman == 'i':
                card['rubric']['markingGuideNote'] = 'The answer list prints “7th July 1939”; the transcript on scheme page 27 prints “1 июля 1939 года”. This source discrepancy remains under review; the answer row preserves the published marking scheme.'
            cards.append(card)
    assert len(cards) == 24 and sum(c['totalMarks'] for c in cards) == 80
    return cards


def mark_range(label):
    nums = list(map(int, re.findall(r'\d+', label)))
    return list(range(nums[0], nums[-1]+1))


def bands(S, page, kind):
    table = S[page-1].find_tables().tables[0].extract()
    normal, lower = [], []
    for row in table:
        cells = [squash(cell) for cell in row if cell and squash(cell)]
        if not cells or not re.match(r'^\d', cells[0]):
            continue
        if kind == 'essay':
            prices = cells[0].split('lower E')
            full, low, description = prices[0].strip(), prices[-1].strip(), cells[-1]
        elif kind == 'guided':
            low, full, description = cells
        else:
            full, description = cells
            low = full
        normal.append({'label': full, 'marks': mark_range(full), 'guidance': [description]})
        lower.append({'label': low, 'marks': mark_range(low), 'guidance': [description]})
    return normal, lower


def writing(docs):
    S, Q = docs['scheme'], docs['paper']
    # Read the English instructions and the complete bilingual topic pool from
    # the paper's own text order. No example essay is invented.
    paper = squash(Q[11].get_text())
    question = 'Write a short essay' + between(paper, 'Write a short essay', 'Напишите')
    question += '\n\n' + '\n'.join('• ' + part.strip() for part in paper.split('')[1:]).split('Teideal/Title')[0].strip()
    assert question.count(' / ') >= 10 and 'Русские сказки' in question
    content_page = page_text(S, 13)
    content = bullets(between(content_page, 'Communication/content (C)', '2.'))
    expression = bullets(between(content_page, 'Expression (E)'))
    assert len(content) == 7 and len(expression) == 7, (content, expression)
    full, lower = bands(S, 14, 'essay')
    c = base('SE', question, 30, [12], [13, 14])
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
    question = '\n'.join(page_text(Q, p, (297, 35, 580, 775)) for p in (13, 14))
    question = 'Write a piece' + between(question, 'Write a piece')
    assert all(term in question for term in ('1. LETTER', '2. NARRATIVE', '3. DISCUSSION', 'to college.'))
    g = base('GW', question, 40, [13, 14], [15, 16, 17])
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


def build():
    docs = opened_sources()
    S, P = docs['scheme'], RuPaper(2026, 'hl')
    cards = []
    # Visually counted ten asks, 40 marks. The last one prints a1-mark rung.
    c1 = '\n'.join(page_text(S, p) for p in (4, 5))
    keys = [(1, 'i', 2), (1, 'ii', 1), (1, 'iii', 2), (2, 'i', 3), (2, 'ii', 2),
            (3, 'i', 3), (3, 'ii', 2), (4, 'i', 1), (4, 'ii', 3), (4, 'iii', 1)]
    for index, (item, roman, count) in enumerate(keys):
        marker = f'{item}.({roman})'
        next_marker = f'{keys[index+1][0]}.({keys[index+1][1]})' if index+1 < len(keys) else None
        block = between(c1, marker, next_marker)
        cue, body = block.split('assign 2 marks:', 1)
        cue = squash(re.sub(r'\d+\s*x\s*\d+\s*marks', '', cue))
        question, question_page, source_block = P.find('C1', item, roman, cue)
        assert question and source_block.side == 'R', (item, roman, cue)
        # The next question's tariff is printed slightly ABOVE its heading.
        body = re.sub(r'\d+\s*x\s*\d+\s*marks', '', body)
        partial = None
        if '1 mark for' in body:
            body, partial = body.split('1 mark for', 1)
        answers = bullets(body)
        card = base('C1', question, count*2, [2, 3, 4], [4, 5], item, roman)
        card['review']['questionPages'] = [question_page]
        if partial:
            assert len(answers) == count == 1
            card['rows'] = [{'id': 'answer', 'kind': 'criterion', 'verbatim': answers[0],
                             'marks': 2, 'permittedMarks': [0, 1, 2],
                             'contextNote': '1 mark for ' + squash(partial)}]
        else:
            card['rows'] = [menu(answers, count, 2)]
        card['notes'] += ' Answer in English or Irish.'
        cards.append(card)
    assert sum(c['totalMarks'] for c in cards) == 40

    # Language awareness: the task structures differ, so each original
    # alternative remains practicable. All five required cells stay together.
    from ru_scheme import RuScheme
    scheme = RuScheme(2026, 'hl')
    for unit, page, source_pages in [('LA1', 6, [2, 5]), ('LA2', 10, [6, 7, 8, 9])]:
        tasks = scheme.tasks(unit)
        assert len(tasks) == 2
        for roman, task in zip(('i', 'ii'), tasks):
            # The exact alternative heading begins its whole instruction;
            # a wording-best single line can start halfway through a task.
            text = P.instruction(unit, roman)
            assert text and len(text.split()) > 8
            options = [f'{left} — {right}' for left, right in task.pairs] if task.pairs else task.options
            assert len(options) == (19 if unit == 'LA1' and roman == 'ii' else 5), options
            card = base(unit, text, 10, source_pages, [page], roman=roman)
            card['rows'] = [menu(options, 5, 2)]
            if unit == 'LA2' and roman == 'ii':
                assert 'Irish, English or Russian' in text, text
            cards.append(card)

    summary = '\n'.join(page_text(S, p) for p in (7, 8, 9))
    rule = squash(between(summary, 'Award 2 marks for each', 'Part 1.'))
    assert rule.startswith('of 4 details (up to 8 marks) AND 2 discretionary marks')
    summary_rule = 'Award 2 marks for each ' + rule
    for item, expected in [(1, 14), (2, 15), (3, 9), (4, 13)]:
        block = between(summary, f'Part {item}.', f'Part {item+1}.' if item < 4 else None)
        cue, rest = block.split('Main points:', 1)
        cue = squash(re.sub(r'10\s*marks', '', cue))
        text, _, source_block = P.find('C2', item, None, cue)
        assert text and source_block.side == 'R'
        main, secondary = rest.split('Secondary details:', 1)
        main, secondary = bullets(main), bullets(secondary)
        assert len(main) + len(secondary) == expected, (item, main, secondary)
        card = base('C2', text, 10, [6, 7, 8], [7, 8, 9], item)
        row = menu(main + secondary, 4, 2,
                   f'The first {len(main)} answers are the scheme’s main points; the remaining {len(secondary)} are its secondary details. ' + summary_rule)
        # An exact source sentence, followed by the complete published rules.
        card['rows'] = [row, {'id': 'summary-skills', 'kind': 'criterion',
                              'verbatim': 'Express / develop their ideas clearly.',
                              'marks': 2, 'permittedMarks': [0, 1, 2], 'contextNote': summary_rule}]
        cards.append(card)

    # Complete ten-item matching table. Its10 separately priced cells are a
    # single required task; using an anyN with count=all keeps the table whole.
    text = page_text(docs['paper'], 10, (294, 65, 580, 174))
    text = squash(text)
    text = text[text.index('Read the following brief news items.'):]
    assert text.startswith('Read the following brief news items.'), text
    source = page_text(S, 11)
    answers = re.findall(r'^\s*(\d{1,2})\s+(?=[А-Я«])', source, re.M)
    assert answers == ['9', '8', '1', '10', '2', '6', '4', '3', '5', '7'], answers
    card = base('SD', text, 20, [10], [11])
    card['rows'] = [menu([f'{i} — {answer}' for i, answer in enumerate(answers, 1)], 10, 2,
                         'Rows are numbered from top to bottom in the original table. Award 2 marks for each correct answer.')]
    cards.append(card)

    # Thirty marks are printed for the whole passage; no per-form rate is
    # printed. Fourteen brackets include one two-word form. Never invent2each.
    text = squash(page_text(docs['paper'], 11, (306, 132, 580, 280)))
    text = text[text.index('Read through the following text.'):]
    passage = between(page_text(S, 12), 'История блинов')
    forms = re.findall(r'\(([^()]+)\)', passage)
    assert len(forms) == 14
    card = base('GR', text, 30, [11], [12])
    card['tariffModel'] = {'kind': 'questionTotal'}
    card['rows'] = [{'id': f'form-{i}', 'kind': 'point', 'verbatim': form, 'marks': None}
                    for i, form in enumerate(forms, 1)]
    card['notes'] += ' The scheme gives 30 marks for the complete exercise and does not print a per-form tariff. Answers are either right or wrong; misspelled/transcribed forms and wrong verb tenses receive no marks.'
    cards.append(card)
    assert len(cards) == 20
    for card in cards:
        if card['section'] == 'C2':
            row, criterion = card['rows']
            note = row['contextNote']
            main_count = int(re.search(r'first (\d+)', note).group(1))
            answers = row['group']['options']
            as_points(card, answers, 4, steps=[0, 1, 2],
                      labels=['Main point' if i < main_count else 'Secondary detail' for i in range(len(answers))])
            card['rubric']['taskRequirements'] = [summary_rule]
            card['rubric']['criteria'] = [{'id': 'summary-skills', 'label': 'Discretionary marks',
                'maxMarks': 2, 'permittedMarks': [0, 1, 2], 'guidance': [summary_rule],
                'limits': [{'id': 'incomplete-response', 'maxMarks': 1,
                    'when': {'any': [{'flag': 'incomplete-response', 'prompt': squash(summary_rule[summary_rule.index('If a candidate fails'):])}]},
                    'guidance': [summary_rule]}]}]
        elif card['section'] == 'SD':
            as_points(card, card['rows'][0]['group']['options'], 10)
        else:
            card['kind'] = 'question'
    cards.extend(writing(docs))
    cards.extend(listening(docs, P))
    attach_language_rule(cards, docs['scheme'])
    assert len(cards) == 46
    return cards


def attach_language_rule(cards, scheme):
    """Apply the original Higher rule only to language-mandated responses.

    The bilingual written comprehension permits Irish as well as English.
    Number-matching, explicit three-language case naming and listening are
    exempt. The 2026 whole-question grammar tariff currently has note-only
    support; never manufacture a per-form price to enable the shared control.
    """
    source = 'Language of answer: ' + squash(between(page_text(scheme, 3), 'Language of answer:', 'Quality of English:'))
    assert 'award NO marks' in source and 'listening comprehension' in source
    for card in cards:
        unit = card['section']
        language_task = (unit in ('C1', 'C2', 'SE', 'GW') or
                         (unit == 'LA1' and (card['year'] == 2026 or card['id'].endswith('-i'))) or
                         (unit == 'LA2' and card['year'] in (2022, 2024, 2025) and card['id'].endswith('-i')) or
                         (unit == 'LA2' and card['year'] == 2023 and card['id'].endswith('-ii')) or
                         (unit == 'GR' and card['year'] in (2022, 2023, 2024, 2025)))
        if language_task:
            card['answerLanguageRule'] = {'otherLanguageMultiplier': 0, 'sourceText': source, 'schemePages': [3]}
            if unit in ('C1', 'C2'):
                card['notes'] += ' The original bilingual paper permits English or Irish; either is an accepted response language. Mark only answers in a language not permitted for this task as wrong-language.'
                direction = 'Answer in English or Irish. Both languages are permitted by the original bilingual paper.'
                if card['kind'] == 'question':
                    card['rows'][0]['contextNote'] = (card['rows'][0].get('contextNote', '') + ' ' + direction).strip()
                else:
                    card['rubric']['markingGuideNote'] = (card['rubric']['markingGuideNote'] + ' ' + direction).strip()
        elif unit == 'GR':
            card['notes'] += ' ' + source + ' This whole-question tariff currently has no numeric wrong-language control; apply the published rule when assessing the complete exercise.'
            card['rows'][0]['contextNote'] = 'The complete exercise is marked out of 30. The scheme does not print separate marks for individual forms. ' + source + ' Assess the complete exercise using this rule.'


def save_reviewed(cards):
    """Replace this reviewed batch by stable ID and preserve other sittings."""
    output = ROOT / 'scripts/markbank/authored/russian-reviewed.json'
    output.parent.mkdir(parents=True, exist_ok=True)
    previous = json.loads(output.read_text()) if output.exists() else []
    incoming = {card['id']: card for card in cards}
    assert len(incoming) == len(cards)
    existing = {card['id'] for card in previous}
    merged = [incoming.get(card['id'], card) for card in previous]
    merged.extend(card for card in cards if card['id'] not in existing)
    output.write_text(json.dumps(merged, ensure_ascii=False, indent=2) + '\n')
    print(output)


if __name__ == '__main__':
    save_reviewed(build())
