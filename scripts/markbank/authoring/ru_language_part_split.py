"""R7: split separately answered language-awareness prompts at SEC mark boundaries."""
import copy
from ru_topics import concept_for
import re

REVIEW = 'scripts/markbank/authoring/reviews/russian-language-splits-20261119'

def split_language_parts(cards, source, year):
    original = next(c for c in cards if c['id'] == f'ru-{year}-hl-la1')
    record = next(r for r in source['tasks'] if r['unit'] == 'LA1')
    prompts = record['printedPrompts']
    criteria = original['rubric']['criteria']
    count = 3 if year == 2012 else 6
    assert len(prompts) == len(criteria) == count
    assert original['totalMarks'] == 2 * count
    assert all(c['maxMarks'] == 2 for c in criteria)
    if year == 2012:
        suffixes = ['i', 'ii', 'iii']
        refs = [f'2012 HL Section LA1 Q({s})' for s in suffixes]
        texts = [record['question'].removesuffix(' (6 marks)').strip() + '\n\n' + p for p in prompts]
    else:
        suffixes = ['1-i', '1-ii', '2-i', '2-ii', '3', '4']
        refs = ['2010 HL Section LA1 Q' + x for x in ['1(i)', '1(ii)', '2(i)', '2(ii)', '3', '4']]
        sections = [1, 1, 2, 2, 3, 4]
        texts = [f'Section {s}\n\n{p}' for s, p in zip(sections, prompts)]
    replacements = []
    for index, (suffix, ref, text, criterion) in enumerate(zip(suffixes, refs, texts, criteria)):
        c = copy.deepcopy(original)
        c['id'] = original['id'] if index == 0 else f'ru-{year}-hl-la1-{suffix}'
        c['conceptId'] = original['conceptId'] if index == 0 else concept_for(prompts[index])
        c['questionRef'] = ref
        c['questionText'] = text
        c['totalMarks'] = 2
        c['rubric']['criteria'] = [copy.deepcopy(criterion)]
        if year == 2012:
            body = record['publishedSourceBlock']
            general = body[:body.index('i. Give an example')].strip()
            prompts_in_scheme = [part.strip() for part in re.split(r'\b(?:iii|ii|i)\.? Give an example', body)[1:]]
            assert len(prompts_in_scheme) == 3
            own_guidance = 'Give an example ' + prompts_in_scheme[index]
            c['rubric']['criteria'][0]['guidance'] = [general, own_guidance]
            c['rubric']['taskRequirements'] = [general]
            c['rubric']['markingGuideNote'] = 'Use the shared paragraph on the original question page. This separately numbered part is marked out of two; all three parts together are marked out of six. The scheme permits the nominative form or the requested case.'
            if suffix == 'iii':
                c['rubric']['markingGuideNote'] += ' The scheme gives one mark for одним, but prints no full-credit example. Preserve that partial answer when assessing the response.'
        else:
            c['rubric']['markingGuideNote'] = 'Use the named section of the original story. This printed prompt is marked out of two; the six prompts together are marked out of twelve. The scheme accepts the requested form, an appropriate English translation or the base/dictionary form.'
            if suffix == '2-ii':
                c['rubric']['markingGuideNote'] += ' The scheme gives two marks to every candidate for this impossible request, including a blank response.'
            else:
                c['rubric']['taskRequirements'] = [r for r in c['rubric']['taskRequirements'] if 'award 2 marks to all' not in r]
        c['review']['reviewedAt'] = '2026-11-19'
        c['review']['splitEvidence'] = f'{REVIEW}/{year}-hl.json'
        replacements.append(c)
    assert sum(c['totalMarks'] for c in replacements) == original['totalMarks']
    assert replacements[0]['id'] == original['id'] and replacements[0]['conceptId'] == original['conceptId']
    result = []
    for card in cards:
        result.extend(replacements if card is original else [card])
    assert len(result) == len(cards) + count - 1
    return result
