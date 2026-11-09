#!/usr/bin/env python3
"""2026 Ordinary Russian: original-PDF review, 31 written + 25 listening tasks.

This sitting has 220 written and 100 listening marks. Published alternatives
which share a grid remain one task; the two discourse routes use the existing
answerVariants contract so a student cannot mix the two dialogues.
"""
import hashlib
import json
import re
from pathlib import Path

import fitz
from ru_paper import RuPaper, bag, score
from ru_review_2026_hl import ROOT, squash, page_text, between, bullets, base as higher_base, as_points, mark_range, save_reviewed

FILES = {
    'paper': ('papers/2026-ol-000-paper.pdf', '118ab2d6814246c2a9f071945a888fd1ec7be42a46d2d9cf996a25703103f070'),
    'aural': ('papers/2026-ol-A00-paper.pdf', 'd6a8bb9334a155937d15c2287001e5e5e9bd0606993df7f449185cb3837df966'),
    'scheme': ('schemes/2026-ol.pdf', '7fb47439b0e1322e592da32dc160f2f164a84c8ac4810d02b18e7a17d3d89047'),
}


def opened_sources():
    docs = {}
    for key, (relative, digest) in FILES.items():
        path = ROOT / 'examiner-reports/russian' / relative
        assert hashlib.sha256(path.read_bytes()).hexdigest() == digest, path
        docs[key] = fitz.open(path)
    return docs


def base(unit, text, total, pages, scheme_pages, item=None, roman=None):
    card = higher_base(unit, text, total, pages, scheme_pages, item, roman)
    card['id'] = card['id'].replace('-hl-', '-ol-')
    card['level'] = 'ordinary'
    card['questionRef'] = f'2026 OL Section {unit}' + (f' Q{item}' if item is not None else '')
    if roman:
        card['questionRef'] += f'({roman})'
    card['sourceMaterial']['title'] = f'2026 Ordinary Russian — {unit}'
    return card


def question_blocks(text):
    """Read reviewed numbered/roman headings, including continuation romans."""
    pattern = r'^\s*(?:(\d)\s*\.\s*)?\((i{1,3})\)\s+|^\s*(\d)\s*\.\s+(?=[A-Z])'
    heads = list(re.finditer(pattern, text, re.M))
    output, item = [], None
    for index, head in enumerate(heads):
        item = int(head.group(1) or head.group(3)) if head.group(1) or head.group(3) else item
        roman = head.group(2)
        block = text[head.end():heads[index + 1].start() if index + 1 < len(heads) else len(text)]
        output.append((item, roman, block))
    return output


def unprice(text):
    return re.sub(r'\b\d+\s*(?:x\s*\d+\s*)?marks?\b', '', text)


def reading(docs, P):
    S, cards = docs['scheme'], []
    assert 'Do not penalise answers supplied in Russian.' in squash(page_text(S, 3))
    specs = [
        ('IR1', [4, 5], [2, 3, 4], [2, 1, 2, 1, 1, 2, 1, 2], 'LANGUAGE AWARENESS'),
        ('IR2', [6, 7], [6, 7, 8], [4, 1, 1, 2, 2, 2, 2], 'Language awareness'),
        ('CD', [11, 12], [12, 13, 14], [2, 1, 3, 2, 3, 2, 2, 3, 1, 1], None),
    ]
    for unit, scheme_pages, paper_pages, counts, end in specs:
        source = '\n'.join(page_text(S, p) for p in scheme_pages)
        if end:
            source = source.split(end)[0]
        blocks = question_blocks(source)
        assert len(blocks) == len(counts), (unit, blocks)
        general = re.split(r'\n\s*1\.', source[source.index('Allocate 2 marks for each'):], maxsplit=1)[0].strip()
        if unit == 'IR1':
            general = general.split('24 marks')[0].strip()
        for (item, roman, block), count in zip(blocks, counts):
            candidates = [b for b in P.blocks if b.unit == unit and b.item == item and b.roman == roman and b.side == 'R']
            assert len(candidates) == 1, (unit, item, roman)
            question = candidates[0].text
            if unit == 'IR2' and item == 1:
                # Four compulsory headings are one printed task.
                table = next(t.extract() for t in S[5].find_tables().tables if 'Day of the week' in str(t.extract()))
                assert len(table) == 4
                labels = [squash(row[0]).split(' / ')[-1] for row in table]
                answers = [squash(row[1]) for row in table]
                question += '\n\n' + '\n'.join(labels)
                card = base(unit, question, 4, paper_pages, scheme_pages, item, roman)
                card['kind'] = 'question'
                card['rows'] = [{'id': f'cell-{i}', 'kind': 'point', 'verbatim': answer, 'contextNote': labels[i - 1], 'marks': 1}
                                for i, answer in enumerate(answers, 1)]
            else:
                cue, _ = block.split('•', 1)
                cue = squash(unprice(cue).split('Any ')[0])
                assert score(bag(question), bag(cue)) >= .8 or question.startswith(cue), (question, cue)
                answers = bullets(unprice(block))
                partials = {}
                if unit == 'CD' and (item, roman) == (1, 'ii'):
                    assert len(answers) == 2
                    partials = {0: [answers.pop()]}
                elif unit == 'CD' and (item, roman) == (2, 'i'):
                    assert len(answers) == 7
                    partials = {2: [answers.pop()]}
                elif unit == 'CD' and (item, roman) == (3, 'iii'):
                    assert len(answers) == 4
                    parts = answers.pop().split(' / ')
                    assert len(parts) == 4
                    partials = {0: [parts[0]], 1: [parts[1]], 2: [parts[2]]}
                    answers.append(parts[3])
                card = as_points(base(unit, question, count * 2, paper_pages, scheme_pages, item, roman),
                                 answers, count, partials, steps=[0, 1, 2])
                if unit == 'CD' and (item, roman) == (3, 'iii'):
                    card['rubric']['groups'][-1]['rows'][0].update(marks=1, steps=[0, 1])
                card['rubric']['taskRequirements'] = [squash(general)]
            card['review']['questionPages'] = [candidates[0].page + 1]
            card['notes'] += ' The paper asks for English; the general marking directions also accept answers supplied in Russian.'
            direction = 'Answer in English or Irish. Marking scheme page 3: Do not penalise answers supplied in Russian.'
            if card['kind'] == 'question':
                card['rows'][0]['contextNote'] = (card['rows'][0].get('contextNote', '') + '\n' + direction).strip()
            else:
                card['rubric']['markingGuideNote'] = direction
            cards.append(card)
    assert len(cards) == 25 and sum(c['totalMarks'] for c in cards) == 88
    return cards


def language_and_matching(docs):
    S, Q, cards = docs['scheme'], docs['paper'], []
    text = page_text(Q, 5, (300, 30, 580, 775))
    instruction = squash(re.search(r'The following.*?neuter\.', text, re.S).group())
    table = next(t.extract() for t in S[4].find_tables().tables if 'семейный парк' in str(t.extract()))
    pairs = [(squash(row[0]), squash(row[1])) for row in table if len(row) == 2 and row[0] and row[1] and 'Example' not in row[0] and 'мягкое' not in row[0]]
    assert len(pairs) == 6, pairs
    card = as_points(base('LA1', instruction + '\n\n' + '\n'.join(left for left, _ in pairs), 6, [5], [5]),
                     [left + ' — ' + right for left, right in pairs], 3)
    card['rubric']['taskRequirements'] = ['Choose three phrases and indicate the gender of the noun: masculine, feminine or neuter.']
    cards.append(card)

    # The source supplies a handwriting grid, not invented cursive model text.
    text = page_text(Q, 8, (300, 30, 580, 775))
    instruction = squash(re.search(r'Write out three.*?script\.', text, re.S).group())
    phrases = re.findall(r'^\s*([А-Яа-яЁё][А-Яа-яЁё ]+?)\s+_{5,}', page_text(Q, 8), re.M)
    assert len(phrases) == 6, phrases
    instruction += '\n\n' + '\n'.join(phrases)
    source = page_text(S, 7)
    guidance = [squash(line) for line in between(source, '2 marks per phrase.').splitlines() if squash(line)]
    card = base('LA2', instruction, 6, [8], [7])
    card.pop('rows'); card.pop('tariffModel'); card['kind'] = 'rubric'
    card['rubric'] = {'system': 'language-writing', 'taskRequirements': ['Three phrases in handwritten/cursive script.', '2 marks per phrase.'],
        'criteria': [{'id': f'phrase-{n}', 'label': f'Chosen phrase {n}', 'maxMarks': 2,
                      'permittedMarks': [0, 1, 2], 'guidance': guidance} for n in (1, 2, 3)], 'markingGuideNote': ''}
    cards.append(card)

    table = S[7].find_tables().tables[0].extract()
    assert len(table) == 10
    answers = [squash(row[1]) + ' — ' + squash(row[0]) for row in table]
    question = Q[8].get_text().replace('\u00a0', ' ')
    question = question[question.index('Match the following'):].strip()
    card = as_points(base('MM', question, 40, [9], [8]), answers, 10)
    for group in card['rubric']['groups']:
        group['rows'][0]['marks'] = 4
    cards.append(card)

    raw = Q[9].get_text().replace('\u00a0', ' ')
    question = 'Read through' + between(raw, 'Read through', 'Focail')
    question = squash(question)
    question += '\n\n' + page_text(Q, 10, (20, 180, 580, 775)) + '\n\n' + page_text(Q, 11)
    card = base('SD', question, 20, [10, 11], [9, 10])
    card['kind'] = 'question'
    variants = []
    for page, group in [(9, 'A'), (10, 'B')]:
        # Answers are the original bold/underlined completed gap spans.
        spans = [span for line in S[page - 1].get_text('dict')['blocks'] if 'lines' in line
                 for part in line['lines'] for span in part['spans']
                 if span['flags'] & 16 and span['bbox'][1] > 180 and re.search(r'[А-Яа-яЁё]', span['text'])]
        answers = [squash(span['text']) for span in spans if squash(span['text'])]
        assert len(answers) == 5, (page, answers)
        variants.append({'id': f'group-{group.lower()}', 'label': f'Group {group}',
                         'rows': [{'id': f'gap-{i}', 'kind': 'point', 'verbatim': answer, 'marks': 4}
                                  for i, answer in enumerate(answers, 1)]})
    card['rows'] = variants[0]['rows']
    card['answerVariants'] = variants
    cards.append(card)
    return cards


def criterion(cid, label, maximum, allowed, guidance, bands=None):
    return {'id': cid, 'label': label, 'maxMarks': maximum, 'permittedMarks': allowed,
            'guidance': guidance, **({'bands': bands} if bands else {})}


def writing(docs):
    S, Q, cards = docs['scheme'], docs['paper'], []
    raw = Q[14].get_text().replace('\u00a0', ' ')
    instructions = squash('Write 3' + between(raw, 'Write 3', '1.'))
    table = Q[14].find_tables().tables[0].extract()
    assert len(table) == 5
    question = instructions + '\n\n' + '\n'.join(squash(row[1]) + ' / ' + squash(row[2]) for row in table)
    source = page_text(S, 13)
    content = squash(between(source, 'Content of each answer', 'Textual coherence'))
    coherence = between(source, 'Textual coherence')
    bands = [{'label': n, 'marks': [int(n)], 'guidance': [squash(text)]}
             for n, text in re.findall(r'(\d) marks\s+(.+?)(?=\d marks|\Z)', coherence, re.S)]
    assert len(bands) == 4
    card = base('SA', question, 30, [15], [13])
    card.pop('rows'); card.pop('tariffModel'); card['kind'] = 'rubric'
    card['rubric'] = {'system': 'language-writing', 'taskRequirements': [
        'Write 3-5 sentences on ONE of the following topics in Russian or English. Each answer should contain three factual details. Marks are awarded for relevant content and textual coherence.',
        'The quality of the English/Russian will only be an assessment factor insofar as it impedes communication.'],
        'criteria': [criterion('content', 'Content', 24, list(range(0, 25, 4)), [content]),
                     criterion('coherence', 'Textual coherence', 6, [0, 2, 4, 6], [], bands)],
        'markingGuideNote': ''}
    cards.append(card)

    raw = Q[15].get_text().replace('\u00a0', ' ')
    instructions = squash('Write 6' + between(raw, 'Write 6', '1.'))
    table = Q[15].find_tables().tables[0].extract()
    assert len(table) == 3
    choices = []
    for row in table:
        for cell in row[1:]:
            choices.append('\n• '.join(squash(part) for part in cell.split('\uf0b7')))
    question = instructions + '\n\n' + '\n\n'.join(choices)
    source = page_text(S, 15)
    instruction_source = squash(between(page_text(S, 14), 'Write 6-10 sentences', '1. Cathair'))
    instruction_source = 'Write 6-10 sentences ' + instruction_source
    content = squash(between(source, '2 points for content', 'If the answer'))
    content = '2 points for content ' + content
    lower_rule = squash('If the answer' + between(source, 'If the answer', 'Accuracy and fluency'))
    table = next(t.extract() for t in S[14].find_tables().tables if 'Lower E' in str(t.extract()))
    full, lower = [], []
    for row in table[1:]:
        normal, low, description = map(squash, row)
        full.append({'label': normal, 'marks': mark_range(normal), 'guidance': [description]})
        lower.append({'label': low, 'marks': mark_range(low), 'guidance': [description]})
    coherence = between(source, 'Allocate 6 marks for textual coherence:')
    coherent = [{'label': n, 'marks': mark_range(n), 'guidance': [squash(text)]}
                for n, text in re.findall(r'^\s*(\d(?:-\d)?)\s+(.+?)(?=^\s*\d(?:-\d)?\s|\Z)', coherence, re.S | re.M)]
    assert len(coherent) == 5, coherent
    expression = criterion('expression', 'Language + expression', 12, list(range(13)), [], full)
    expression['limits'] = [{'id': 'lower-expression', 'maxMarks': 9,
        'when': {'any': [{'criterionIds': ['content'], 'atMost': 6},
                         {'flag': 'fewer-six-sentences', 'prompt': lower_rule}]},
        'guidance': [lower_rule], 'bands': lower}]
    card = base('EW', question, 30, [16], [14, 15])
    card.pop('rows'); card.pop('tariffModel'); card['kind'] = 'rubric'
    card['rubric'] = {'system': 'language-writing', 'taskRequirements': [squash(instruction_source),
        'No marks are awarded for additional information/content.'],
        'criteria': [criterion('content', 'Communication + content', 12, list(range(0, 13, 2)), [content]),
                     expression, criterion('coherence', 'Textual coherence', 6, list(range(7)), [], coherent)],
        'markingGuideNote': ''}
    cards.append(card)
    return cards


def listening(docs, P):
    # PDF drawing order preserves a wrapped bullet before the next column.
    # Global visual row sorting interleaves "family ... culture" on p17.
    source = '\n'.join(docs['scheme'][p - 1].get_text(clip=fitz.Rect(20, 30, 580, 775))
                       for p in range(16, 22))
    sections = re.split(r'SECTION\s+(?:IV|III|II|I)\b', source)
    assert len(sections) == 5
    general = bullets(sections[0])
    asks = P.aural_asks()
    assert len(asks) == 25
    audio = next(row['source'] for row in json.loads((ROOT / 'data/russianAudio.json').read_text()) if row['year'] == 2026)
    cards = []
    pages = {'L1': [2, 3], 'L2': [4], 'L3': [5, 6], 'L4': [7]}
    scheme_pages = {'L1': [16, 17], 'L2': [17, 18], 'L3': [19], 'L4': [20, 21]}
    prices = {'L1': [3, 6, 3, 3, 3, 3, 4], 'L2': [6, 6, 6, 4, 3],
              'L3': [4, 4, 3, 4, 3, 4, 3], 'L4': [6, 6, 4, 3, 3, 3]}
    for index in range(1, 5):
        unit = f'L{index}'
        tasks = [ask for ask in asks if ask[0] == unit]
        blocks = question_blocks(sections[index])
        assert len(tasks) == len(blocks) == len(prices[unit]), (unit, blocks)
        for (_, item, roman, question), (scheme_item, scheme_roman, block), total in zip(tasks, blocks, prices[unit]):
            source_typo = unit == 'L4' and item == 3 and roman == 'ii'
            assert (item, roman) == (scheme_item, scheme_roman) or (source_typo and (scheme_item, scheme_roman) == (2, 'ii'))
            block = re.sub(r'^\s*Segment\s+\d+\s*$', '', block, flags=re.M)
            cue, _ = block.split('•', 1)
            tariff = re.search(r'(\d+)\s*x\s*(\d+)\s*marks|(\d+)\s*marks', cue)
            assert tariff, (unit, item, roman, cue)
            count = int(tariff.group(1)) if tariff.group(1) else 1
            price = int(tariff.group(2) or tariff.group(3))
            assert count * price == total
            cue = squash(unprice(cue).split('Any ')[0])
            assert score(bag(question), bag(cue)) > .8 or squash(question).startswith(cue), (question, cue)
            answers = bullets(block)
            partials = {}
            partial_target = {('L1', 2, 'ii'): 1, ('L2', 1, 'ii'): 2, ('L4', 2, 'i'): 2}.get((unit, item, roman))
            if partial_target is not None:
                assert re.search(r'1\s*mark\b', answers[-1]), answers[-1]
                partials[partial_target] = [squash(unprice(answers.pop()))]
            answers = [squash(unprice(answer)) for answer in answers]
            card = as_points(base(unit, question, total, pages[unit], scheme_pages[unit], item, roman),
                             answers, count, partials)
            for group in card['rubric']['groups']:
                group['rows'][0]['marks'] = price
            if unit == 'L4' and item == 1 and roman == 'i':
                # Equivalent age statements are one semantic detail.
                assert answers[-2:] == ['Started singing when she was 9', 'She sang when she was 9']
                duplicate = card['rubric']['groups'].pop()['rows'][0]
                duplicate['id'] = 'alternative'
                card['rubric']['groups'][-1]['rows'].append(duplicate)
            if unit == 'L1':
                topic = ('russian-0-3' if roman == 'ii' else 'russian-0-4') if item == 1 else 'russian-0-9' if item == 2 else 'russian-0-14'
            elif unit == 'L2':
                topic = 'russian-0-1' if item == 1 and roman == 'i' else 'russian-0-6' if item == 3 else 'russian-0-3'
            elif unit == 'L3':
                topic = 'russian-0-3' if item == 3 else 'russian-0-5'
            else:
                topic = 'russian-0-7' if item == 1 and roman == 'i' else 'russian-0-4' if item in (1, 2) else 'russian-2-5'
            card['topicId'] = topic
            card['additionalTopicIds'] = ['russian-1-0']
            card['rubric']['taskRequirements'] = general
            card['sourceMaterial']['kind'] = 'source-question'
            card['sourceMaterial']['presentationNote'] = 'Listen to the official recording and answer the printed question. The transcript is not shown before answering.'
            card['audioMaterial'] = audio
            card['review']['guidancePages'] = [16]
            if source_typo:
                card['rubric']['markingGuideNote'] = 'The marking scheme prints 2(ii) for the final question; the question booklet prints 3(ii). This card follows the printed question booklet.'
            cards.append(card)
    assert len(cards) == 25 and sum(card['totalMarks'] for card in cards) == 100
    return cards


def build():
    docs = opened_sources()
    P = RuPaper(2026, 'ol')
    cards = reading(docs, P) + language_and_matching(docs) + writing(docs) + listening(docs, P)
    assert len(cards) == 56 and sum(card['totalMarks'] for card in cards) == 320
    return cards


if __name__ == '__main__':
    save_reviewed(build())
