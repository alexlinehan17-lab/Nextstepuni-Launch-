#!/usr/bin/env python3
"""2024 Ordinary Russian: original-PDF review, 30 written + 20 listening tasks.

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
from ru_review_2026_hl import ROOT, squash, page_text as original_page_text, between, bullets, base as higher_base, as_points, mark_range, save_reviewed

FILES = {
    'paper': ('papers/2024-ol-000-paper.pdf', '7ca7754d00496ebdc9ce022665c6eba8f7378bf7325d02d46ceab168f3761970'),
    'aural': ('papers/2024-ol-A00-paper.pdf', '9384428ab46b24725f66f30afafdfb22048b4507de24e6307eb2df4fe1ea547c'),
    'scheme': ('schemes/2024-ol.pdf', 'ecba77fed2ef00afe4503bb1d4ed4b5ea0c5803a53727338592764406fbee44a'),
}


def page_text(doc, page, box=None):
    # Preserve the entire answer area while excluding the running footer.
    return original_page_text(doc, page, box or (20, 30, 580, 790))


def opened_sources():
    docs = {}
    for key, (relative, digest) in FILES.items():
        path = ROOT / 'examiner-reports/russian' / relative
        assert hashlib.sha256(path.read_bytes()).hexdigest() == digest, path
        docs[key] = fitz.open(path)
    return docs


def base(unit, text, total, pages, scheme_pages, item=None, roman=None):
    card = higher_base(unit, text, total, pages, scheme_pages, item, roman)
    card['id'] = card['id'].replace('2026', '2024').replace('-hl-', '-ol-')
    card['year'] = 2024
    card['level'] = 'ordinary'
    card['questionRef'] = f'2024 OL Section {unit}' + (f' Q{item}' if item is not None else '')
    if roman:
        card['questionRef'] += f'({roman})'
    card['sourceMaterial']['title'] = f'2024 Ordinary Russian — {unit}'
    return card


def question_blocks(text):
    """Read reviewed numbered/roman headings, including continuation romans."""
    pattern = r'^\s*(?:(\d)\s*\.\s*)?\((iv|v|i{1,3})\)\s+|^\s*(\d)\s*\.\s+(?=[A-Z])'
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
    assert 'Do not penalise answers supplied in Russian.' in squash(page_text(S, 2))
    specs = [
        ('IR1', [4, 5], [2, 3, 4], [1, 2, 2, 2, 1, 1, 1, 2], 'LANGUAGE AWARENESS'),
        ('IR2', [5, 6], [6, 7], [1, 2, 3, 2, 1, 1, 2], 'Language awareness'),
        ('CD', [10, 11], [12, 13, 14], [3, 3, 3, 1, 1, 3, 3, 1, 2], None),
    ]
    for unit, scheme_pages, paper_pages, counts, end in specs:
        # PDF drawing order keeps the multiple-column animal/country pools.
        source = '\n'.join(S[p-1].get_text(clip=fitz.Rect(20,30,580,790)) for p in scheme_pages)
        if unit == 'IR2':
            source = source.split('Q.2')[1]
        if end:
            source = source.split(end)[0]
        blocks = question_blocks(source)
        assert len(blocks) == len(counts), (unit, blocks)
        general = re.split(r'\n\s*1\.', source[source.index('Allocate 2 marks for each'):], maxsplit=1)[0].strip()
        if unit == 'IR1':
            general = general.split('24 marks')[0].strip()
        for (item, scheme_roman, block), count in zip(blocks, counts):
            roman = {'iv':'iii','v':'iv'}.get(scheme_roman,scheme_roman) if unit == 'CD' and item == 3 else scheme_roman
            candidates = [b for b in P.blocks if b.unit == unit and b.item == item and b.roman == roman and b.side == 'R']
            assert len(candidates) == 1, (unit, item, roman)
            question = candidates[0].text
            cue, _ = block.split('•', 1)
            cue = squash(unprice(cue).split('Any ')[0])
            assert score(bag(question), bag(cue)) >= .8 or question.startswith(cue), (question, cue)
            answers = bullets(unprice(block))
            partials = {}
            if unit == 'IR1' and (item, roman) == (2, 'i'):
                assert answers[-2:] == ['Cheap enough', 'Cheap']
                partials = {3: [answers.pop()]}
            elif unit == 'IR1' and (item, roman) == (3, 'i'):
                assert answers == ['80 km/h','Fast enough']
                partials = {0: [answers.pop()]}
            card = as_points(base(unit, question, count * 2, paper_pages, scheme_pages, item, roman),
                             answers, count, partials, steps=[0, 1, 2])
            card['rubric']['taskRequirements'] = [squash(general)]
            card['review']['questionPages'] = [candidates[0].page + 1]
            card['rubric']['markingGuideNote'] = 'Answer in English or Irish. Marking scheme page 2: Do not penalise answers supplied in Russian.'
            if roman != scheme_roman:
                card['rubric']['markingGuideNote'] += f' The marking scheme prints {item}({scheme_roman}); the question booklet prints {item}({roman}). This card follows the printed question booklet.'
            cards.append(card)
    assert len(cards) == 24 and sum(c['totalMarks'] for c in cards) == 88
    return cards


def language_and_matching(docs):
    S, Q, cards = docs['scheme'], docs['paper'], []
    # Handwriting is marked with the printed grid; no invented cursive model.
    text = page_text(Q, 5, (300, 30, 580, 775))
    instruction = squash(re.search(r'Write out three.*?script\.', text, re.S).group())
    phrases = re.findall(r'^\s*([А-Яа-яЁё][А-Яа-яЁё ]+?)\s+_{5,}', page_text(Q, 5), re.M)
    assert len(phrases) == 6, phrases
    instruction += '\n\n' + '\n'.join(phrases)
    source = between(page_text(S, 5), '2 marks per phrase.', 'Q.2')
    guidance = [squash(line) for line in source.splitlines() if squash(line)]
    card = base('LA1', instruction, 6, [5], [5])
    card.pop('rows'); card.pop('tariffModel'); card['kind'] = 'rubric'
    card['rubric'] = {'system': 'language-writing', 'taskRequirements': ['Three phrases in handwritten/cursive script.', '2 marks per phrase.'],
        'criteria': [{'id': f'phrase-{n}', 'label': f'Chosen phrase {n}', 'maxMarks': 2,
                      'permittedMarks': [0, 1, 2], 'guidance': guidance} for n in (1, 2, 3)], 'markingGuideNote': ''}
    cards.append(card)
    instruction = squash(page_text(Q, 8, (300, 30, 580, 150)))
    instruction = re.search(r'Put three.*?nominative case\.', instruction).group()
    table = next(t.extract() for t in S[5].find_tables().tables if 'любого города' in str(t.extract()))
    pairs = [(squash(row[0]), squash(row[1])) for row in table if len(row) == 2 and row[0] and row[1] and 'Example' not in row[0]]
    assert len(pairs) == 6, pairs
    card = as_points(base('LA2', instruction + '\n\n' + '\n'.join(left for left, _ in pairs), 6, [8], [5,6]),
                     [left + ' — ' + right for left, right in pairs], 3)
    card['rubric']['taskRequirements'] = ['Put three of the expressions below into the nominative case.']
    cards.append(card)
    table = S[6].find_tables().tables[0].extract()
    assert len(table) == 10
    answers = [squash(row[1]) + ' — ' + squash(row[0]) for row in table]
    question = Q[8].get_text().replace('\u00a0', ' ')
    question = question[question.index('Match the following'):].strip()
    card = as_points(base('MM', question, 40, [9], [7]), answers, 10)
    for group in card['rubric']['groups']:
        group['rows'][0]['marks'] = 4
    cards.append(card)
    raw = Q[9].get_text().replace('\u00a0', ' ')
    question = 'Read through' + between(raw, 'Read through', 'Focail')
    question = squash(question)
    question += '\n\n' + page_text(Q, 10, (20, 180, 580, 775)) + '\n\n' + page_text(Q, 11)
    card = base('SD', question, 20, [10, 11], [8, 9])
    card['kind'] = 'question'
    variants = []
    for page, group in [(8, 'A'), (9, 'B')]:
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
    source = page_text(S, 12)
    content = squash(between(source, 'Content of each answer', 'Textual coherence'))
    coherence = between(source, 'Textual coherence')
    bands = [{'label': n, 'marks': [int(n)], 'guidance': [squash(text)]}
             for n, text in re.findall(r'(\d) marks\s+(.+?)(?=\d marks|\Z)', coherence, re.S)]
    assert len(bands) == 4
    card = base('SA', question, 30, [15], [12])
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
            choices.append('\n• '.join(squash(part) for part in re.split(r'[\uf0b7•]', cell)))
    question = instructions + '\n\n' + '\n\n'.join(choices)
    source = page_text(S, 14)
    instruction_source = squash(between(page_text(S, 13), 'Write 6-10 sentences', '1. Campa'))
    instruction_source = 'Write 6-10 sentences ' + instruction_source
    content = squash(between(source, '2 points for content', 'Accuracy and fluency'))
    content = '2 points for content ' + content
    lower_rule = squash('If the answer' + between(source, 'If the answer', 'Put square box'))
    table = next(t.extract() for t in S[13].find_tables().tables if 'Lower E' in str(t.extract()))
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
    card = base('EW', question, 30, [16], [13, 14])
    card.pop('rows'); card.pop('tariffModel'); card['kind'] = 'rubric'
    card['rubric'] = {'system': 'language-writing', 'taskRequirements': [squash(instruction_source),
        'No marks are awarded for additional information/content.'],
        'criteria': [criterion('content', 'Communication + content', 12, list(range(0, 13, 2)), [content]),
                     expression, criterion('coherence', 'Textual coherence', 6, list(range(7)), [], coherent)],
        'markingGuideNote': ''}
    cards.append(card)
    return cards

def listening(docs, P):
    source = '\n'.join(docs['scheme'][p-1].get_text(clip=fitz.Rect(20,30,580,790)) for p in range(15,19))
    sections = re.split(r'SECTION\s+(?:IV|III|II|I)\b', source)
    assert len(sections) == 5
    general = bullets(sections[0])
    asks = P.aural_asks()
    assert len(asks) == 20
    audio = next(row['source'] for row in json.loads((ROOT / 'data/russianAudio.json').read_text()) if row['year'] == 2024)
    cards = []
    pages = {'L1': [2], 'L2': [3], 'L3': [4,5], 'L4': [6,7]}
    scheme_pages = {'L1': [15], 'L2': [16], 'L3': [17], 'L4': [18]}
    prices = {'L1': [6,3,6,6,4], 'L2': [4,3,6,6,6], 'L3': [4,6,6,6,3], 'L4': [4,6,6,3,6]}
    for index in range(1,5):
        unit = f'L{index}'
        tasks = [ask for ask in asks if ask[0] == unit]
        blocks = question_blocks(sections[index])
        assert len(tasks) == len(blocks) == len(prices[unit]), (unit, blocks)
        for (_,item,roman,question), (scheme_item,scheme_roman,block),total in zip(tasks,blocks,prices[unit]):
            assert (item,roman) == (scheme_item,scheme_roman)
            block = re.sub(r'^\s*Segment\s+\d+\s*$', '', block, flags=re.M)
            cue, _ = block.split('•',1)
            tariff = re.search(r'(\d+)\s*x\s*(\d+)\s*marks|(\d+)\s*marks',cue)
            assert tariff, (unit,item,roman,cue)
            count = int(tariff.group(1)) if tariff.group(1) else 1
            price = int(tariff.group(2) or tariff.group(3))
            assert count*price == total
            cue = squash(unprice(cue))
            assert score(bag(question),bag(cue)) > .8 or squash(question).startswith(cue), (question,cue)
            answers = [squash(unprice(answer)) for answer in bullets(block)]
            card = as_points(base(unit,question,total,pages[unit],scheme_pages[unit],item,roman),answers,count)
            for group in card['rubric']['groups']:
                group['rows'][0]['marks'] = price
            if (unit,item,roman) == ('L2',3,'ii'):
                assert answers[-2:] == ['Hiking / camping with her friends', 'Spending time with her friends']
                # Reviewed against p16: the immediately following, less
                # specific friends detail is the1-mark partial of the same
                # activity. The source does not draw a grouping bracket.
                card['rubric']['groups'].pop()
                card['rubric']['groups'][-1]['rows'].append({'id':'partial','text':answers[-1],'marks':1})
                card['rubric']['markingGuideNote'] = 'For the friends detail, claim either the 3-mark full answer or the 1-mark partial answer. A second distinct summer plan can earn its own marks.'
            if unit == 'L1':
                topic = 'russian-0-1' if item == 2 else 'russian-0-9'
            elif unit == 'L2':
                topic = 'russian-0-6' if item == 3 and roman == 'ii' else 'russian-0-3'
            elif unit == 'L3':
                topic = 'russian-0-9' if item == 3 else 'russian-0-5'
            else:
                topic = 'russian-0-7' if item == 1 else 'russian-2-5'
            card['topicId'] = topic
            card['additionalTopicIds'] = ['russian-1-0']
            card['rubric']['taskRequirements'] = general
            card['sourceMaterial']['kind'] = 'source-question'
            card['sourceMaterial']['presentationNote'] = 'Listen to the official recording and answer the printed question. The transcript is not shown before answering.'
            card['audioMaterial'] = audio
            card['review']['guidancePages'] = [15]
            if unit == 'L3' and item == 2:
                assert '8 lessons cost 80 000roubles' in answers
                assert '8 000 руб за 8 занятий' in squash(page_text(docs['scheme'],22))
                card['rubric']['markingGuideNote'] = 'The answer list on marking scheme page 17 prints “8 lessons cost 80 000roubles”; its transcript on page 22 prints “8 000 руб за 8 занятий” (8,000 roubles for 8 lessons). The answer row retains the published marking scheme. This discrepancy remains unresolved; the recording has not been used to adjudicate it.'
            cards.append(card)
    assert len(cards) == 20 and sum(card['totalMarks'] for card in cards) == 100
    return cards


def build():
    docs = opened_sources()
    P = RuPaper(2024, 'ol')
    cards = reading(docs,P) + language_and_matching(docs) + writing(docs) + listening(docs,P)
    assert len(cards) == 50 and sum(card['totalMarks'] for card in cards) == 320
    old_ids = {c['id'] for c in json.loads((ROOT / 'scripts/markbank/authored/russian.json').read_text())}
    for card in cards:
        if card['id'] in old_ids:
            card['review']['correctsExisting'] = True
    assert sum(card['review'].get('correctsExisting', False) for card in cards) == 24
    return cards


if __name__ == '__main__':
    save_reviewed(build())
