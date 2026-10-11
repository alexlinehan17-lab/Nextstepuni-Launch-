#!/usr/bin/env python3
"""Generate only the reading papers independently reviewed in the source ledger.

Keep every scheme line, including all partial-credit rungs and examiner notes.
Printed matching subparts are distinct tasks; required details and open textual
evidence remain one response. MCQ distractors are never alternative tasks.
"""
from pathlib import Path
import hashlib
import json
import re
import fitz
from fr_scheme import FrScheme, PAGE, SOLIDUS_LIST
from fr_paper import FrPaper
from fr_all import ORDINAL_ANSWER
from fr_selection import verify_paper
from fr_reviewed_tasks import write_tasks

ROOT = Path(__file__).resolve().parents[3]
DATA = ROOT / 'examiner-reports/french'
LEDGER = Path(__file__).with_name('french-reading-review.json')


def pdf_text(path):
    with fitz.open(path) as doc:
        return '\n'.join(f'## Page {i}\n' + '\n'.join(' '.join(line.split())
                         for line in page.get_text(sort=True).splitlines())
                         for i, page in enumerate(doc, 1))


def guide_lines(scheme, ask, headings=()):
    stops = scheme._stops() | {h[0] for h in scheme._heads()}
    end = min(i for i in stops if i > ask.line)
    lines = [line.strip() for line in scheme.lines[ask.line + 1:end]
             if line.strip() and not PAGE.match(line.strip())]
    start = re.compile(r'^[•●▪■\uf0b7\uf02d−–—\-]|^(?:Appropriate|Correct manipulation|Direct quotation|One of|Two of|Any two|Either|Candidates|Accept|Note|Mon/Ma/Mes)\b')
    while lines and not (lines[0] in headings or start.search(lines[0]) or SOLIDUS_LIST.match(lines[0])):
        lines.pop(0)  # repeated question wording, never scheme instructions
    paragraphs = []
    for line in lines:
        # PDF Symbol-font markers have no portable text glyph in the app font.
        line = line.replace('\uf0d8', '–').replace('\uf02d', '–').replace('\uf0b7', '•')
        line = re.sub(r'[. …]{3,}', ' — ', line)
        if not paragraphs or line in headings or start.search(line) or re.match(r'^(?:Agree|Disagree|Etc|An indication)', line) or (scheme.legacy_ordinary and re.match(r'^(?:Yes:|No:|Award)', line)):
            paragraphs.append(line)
        else:
            paragraphs[-1] += ' ' + line
    assert paragraphs, scheme.ref(ask)
    pages = []
    page = None
    for i, line in enumerate(scheme.lines[:end]):
        match = re.match(r'## Page (\d+)', line)
        if match:
            page = int(match[1])
        if i >= ask.line and line.strip() and not PAGE.match(line) and page not in pages:
            pages.append(page)
    return paragraphs, pages


HL_RULES = [
    'Answer French questions in French. Answer the final comprehension question in English or Irish.',
    'Use the separate answer spaces where provided. Two or more answers on one line count as one answer. An extra subdivision is rewarded only if an earlier answer is cancelled.',
    'Excess material: deduct 1 or 2 marks. All other errors together: deduct at most 1 mark per question or segment (inappropriate quotation, unnecessary manipulation, grammar in manipulation, required manipulation not attempted, or wrong answer language). The excess-material penalty may also apply.',
]
OL_RULES = [
    'Equivalent meaning earns full marks in Comprehensions 1 and 2 and in Q8 of Comprehensions 3 and 4; exact scheme wording is not required.',
]
OL_FRENCH_RULES = [
    'Penalise extraneous material by at most 2 marks. In questions 1–7, answers in English or Irish earn half marks only. Where manipulation is required, do not penalise grammar mistakes; if a quotation is given instead of required manipulation, deduct 1 mark.',
]


def build():
    review = json.loads(LEDGER.read_text())
    index = (ROOT / 'paperTrailData.ts').read_text().split('  "french": [', 1)[1].split('\n  ],', 1)[0]
    entries = [json.loads(line.strip().rstrip(',')) for line in index.splitlines() if line.strip()]
    tags = json.loads((ROOT / 'scripts/paper-trail/topic-tags/tags/french.json').read_text())
    runtime = json.loads((ROOT / 'data/examTopics/french-runtime.json').read_text())
    original = {card['id']: card for card in json.loads((ROOT / 'scripts/markbank/authored/french.json').read_text())}
    cards, tasks = [], []
    for record in review['papers']:
        year, level = record['year'], record['level']
        for source in record['sources']:
            assert hashlib.sha256((ROOT / source['path']).read_bytes()).hexdigest() == source['sha256'], source['path']
        paper = FrPaper(year, level)
        verify_paper(Path(paper.path), pages=record.get('selectionPages'))
        scheme = FrScheme(year, level, raw_text=pdf_text(DATA / f'schemes/{year}-{level}.pdf'))
        actual = [f'{a.rc}:{a.item}{a.letter or ""}{"-" + a.letter_to if a.letter_to else ""}:{a.total}' for a in scheme.reading()]
        assert actual == record['pricedBoundaries'], (level, actual)
        level_name = {'hl': 'higher', 'ol': 'ordinary'}[level]
        entry = next(e for e in entries if e['year'] == year and e['level'] == level_name and e['lang'] == 'ev')
        doc = next(p for p in entry['papers'] if p['label'] == 'Exam Paper')
        paper_tags = next(p for p in tags if p['year'] == year and p['level'] == level_name and p['fileid'] == doc['doc']['f'])
        for ask in scheme.reading():
            address = f'A{ask.rc}-Q{ask.item}' + (f'-{ask.letter}' if ask.letter else '')
            scoring = record.get('scoringDecisions', {}).get(address)
            if scoring:
                assert (ask.total, ask.per, ask.count, ask.fault) == (
                    scoring['printedHeadMarks'], scoring['perPointMarks'], 1, scoring['parserFault']), address
                assert scoring['reason'] and scoring['sourceNote'], address
                ask.per, ask.count = scoring['perPointMarks'], scoring['requiredPoints']
                ask.total, ask.fault = ask.per * ask.count, None
            assert not ask.fault, scheme.ref(ask)
            mcq = address in record.get('multipleChoice', {}) or any(ORDINAL_ANSWER.search(answer['text']) for answer in ask.answers)
            hit = paper.find(ask.rc, ask.item, None if ask.letter_to else ask.letter, ask.cue, whole=mcq)
            assert hit, scheme.ref(ask)
            question, question_page, _ = hit
            context = record.get('paperContextLines', {}).get(address)
            if context:
                assert context['reason'] and context['page'] == question_page, address
                with fitz.open(paper.path) as source_pdf:
                    lines = [' '.join(line.split()) for line in source_pdf[question_page - 1].get_text(sort=True).splitlines()]
                assert context['sourceLine'] in lines, address
                question += '\n\n' + re.sub(r'_+', '', context['sourceLine']).strip()
            shared_tariff = record.get('sevenPlusOne', {}).get(address)
            question_group = record.get('paperQuestionGroups', {}).get(address)
            if question_group:
                assert question_group['questions'][0] == ask.item and question_group['reason'], address
                prompts = []
                for item in question_group['questions']:
                    found = paper.find(ask.rc, item, None, record['paperCues'][f'A{ask.rc}-Q{item}'])
                    assert found, (address, item)
                    prompts.append(f'Question {item}: {found[0]}')
                question = '\n\n'.join(prompts)
            choice_review = record.get('multipleChoice', {}).get(address, {})
            if choice_review.get('letteredOptions'):
                options = []
                for option_letter in 'abcd':
                    candidates = [b for b in paper.candidates(ask.rc, ask.item, option_letter)
                                  if b.page + 1 == question_page]
                    assert len(candidates) == 1, (address, option_letter)
                    options.append(candidates[0].text)
                question = question + '\n' + '\n'.join(options)
            split = record.get('schemePartSplits', {}).get(f'A{ask.rc}-Q{ask.item}')
            if split and not split.get('standaloneQuestions'):
                stem = paper.find(ask.rc, ask.item, None, record['paperCues'][f'A{ask.rc}-Q{ask.item}'])
                assert stem, address
                if split.get('stemPrefix'):
                    assert stem[0].startswith(split['stemPrefix']), address
                    label = next(part['paperLabel'] for part in split['parts'] if part['letter'] == ask.letter)
                    assert label in question, address
                    if split.get('labelSuffix'):
                        # A category label can be printed separately from the
                        # shared noun and passage reference. Verify that source
                        # continuation before carrying it into each split card.
                        assert any(b.text == split['paperContextCue'] for b in paper.candidates(ask.rc, ask.item, split.get('paperContextPart', 'i'))), address
                        assert split['labelSuffix'] in split['paperContextCue'], address
                        label += split['labelSuffix']
                    if split.get('subjectName'):
                        assert split['subjectName'] in stem[0] and label.startswith('His '), address
                        label = split['subjectName'] + '’s ' + label.removeprefix('His ')
                    question = split['stemPrefix'] + '\n\n' + label
                else:
                    question = stem[0] + '\n\n' + question
            if year <= 2019:
                question = re.sub(r'_+', '', question).strip()
                if mcq:
                    # The older Higher paper's drawn checkboxes expose Symbol
                    # font glyphs as separate text lines, not answer wording.
                    question = '\n'.join(line for line in question.split('\n')
                                         if not re.fullmatch(r'[\uf0a3\uf020\s]+', line))
                    question = question.replace('\uf0fc', '✓')
                    question = re.sub(r'\n(?=\[Cochez\b)', ' ', question)
            guidance, scheme_pages = guide_lines(scheme, ask, record.get('guideHeadings', []))
            offset = record.get('archiveParentOffsets', {}).get(str(ask.rc))
            if offset is None:
                offset = (ask.rc - 1) * 6 if level == 'hl' else [0, 0, 6, 14, 22][ask.rc]
            parent = record.get('archiveParents', {}).get(address, str(offset + ask.item))
            tag = next(q for q in paper_tags['q'] if q['n'] == parent)
            topic_indexes = next(m[5] for m in runtime['questionMappings'] if m[:5] == [level_name[0], 'e', year - 2000, 's', parent])
            topic_ids = [runtime['topics'][i][0] for i in topic_indexes]
            topic_id = tag['primary']
            topic_correction = record.get('topicCorrections', {}).get(str(ask.rc))
            if topic_correction:
                assert topic_correction['reason'] and topic_correction['topicIds'], ask.rc
                topic_id, topic_ids = topic_correction['topicId'], topic_correction['topicIds']
            letters = [chr(i) for i in range(ord(ask.letter), ord(ask.letter_to) + 1)] if ask.letter_to else [ask.letter]
            for index, letter in enumerate(letters):
                prompt, guide, maximum = question, guidance, ask.total
                if ask.letter_to:
                    part = max(paper.candidates(ask.rc, ask.item, letter), key=lambda block: (block.side == 'R', len(block.text)))
                    prompt = question.rstrip(':.') + ':\n\n' + part.text
                    answer = ask.answers[index]
                    assert answer['marks'] == ask.per
                    guide = [f'{answer["text"]} — {answer["marks"]} marks.']
                    maximum = ask.per
                suffix = f'{ask.item}' + (f'({letter})' if letter else '')
                if question_group:
                    suffix = ' and Q'.join(map(str, question_group['questions']))
                n = f'A{ask.rc}-Q{ask.item}' + (f'-{letter}' if letter else '')
                cid = f'fr-{year}-{level}-reading-{n.lower()}'
                preserved_id = record.get('preservedCardIds', {}).get(n)
                if preserved_id:
                    previous = original[preserved_id]
                    assert record.get('correctionReason'), preserved_id
                    assert (previous['year'], previous['level'], previous['section']) == (year, level_name, 'A'), preserved_id
                    assert previous['questionRef'] == f'{year} {level.upper()} Section A{ask.rc} Q{suffix}' + ('–(d)' if ask.letter_to else ''), preserved_id
                    assert previous['totalMarks'] == (ask.total if ask.letter_to else maximum), preserved_id
                    cid = preserved_id
                correction = record.get('promptCorrections', {}).get(n)
                if correction:
                    assert prompt == correction['from'] and correction['to'] in prompt and correction['reason'], n
                    prompt = correction['to']
                opinion_question = record.get('ordinaryOpinionQuestions', {}).get(str(ask.rc), 8)
                english = (level == 'hl' and ask.item == 6) or (level == 'ol' and (ask.rc < 3 or ask.item == opinion_question))
                language = 'English or Irish' if english else 'French'
                ordinary_rules = record.get('ordinaryRules')
                if ordinary_rules:
                    assert ordinary_rules['reason'] and ordinary_rules['rules'], address
                requirements = [f'Answer in {language}.'] + (HL_RULES[1:] if level == 'hl' else ordinary_rules['rules'] if ordinary_rules else OL_RULES)
                if level == 'ol' and ask.rc >= 3:
                    rules = record.get('ordinaryFrenchRules', {}).get(str(ask.rc))
                    if rules:
                        assert rules['reason'] and rules['rules'], address
                    requirements += rules['rules'] if rules else OL_FRENCH_RULES
                if mcq:
                    requirements += ['Select one answer. The other printed options are distractors.']
                if shared_tariff:
                    assert maximum == 8 and shared_tariff['reason'], address
                    requirements += ['Give both required answers. Award 7 marks for one correct answer and 1 additional mark for the second correct answer (8 marks total).']
                elif ask.count > 1 and not ask.letter_to:
                    requirements += [f'Give {ask.count} distinct points. Each earns at most {ask.per} marks; do not score the same point twice.']
                if shared_tariff:
                    allowed = [0, 7, 8] if ask.rc < 3 else list(range(9))
                elif mcq:
                    allowed = [0, maximum]
                elif level == 'hl' or (level == 'ol' and ask.rc >= 3):
                    allowed = list(range(maximum + 1))  # published deductions can reduce the ladder score
                else:
                    per_marks = {0, *[a['marks'] for a in ask.answers if a['marks'] is not None]}
                    if ask.open_list:
                        per_marks |= {0, 2, 4}
                    allowed = {0}
                    for _ in range(1 if ask.letter_to else ask.count):
                        allowed = {a + b for a in allowed for b in per_marks}
                    allowed = sorted(allowed)
                assert allowed[-1] == maximum, cid
                explicit_marks = record.get('permittedMarks', {}).get(address)
                if explicit_marks:
                    assert explicit_marks['reason'] and explicit_marks['marks'][0] == 0
                    assert explicit_marks['marks'][-1] == maximum
                    allowed = explicit_marks['marks']
                pages = paper.rc_pages[ask.rc]
                source = dict(kind='source-text', label=f'Reading Comprehension {ask.rc}', title=f'Reading Comprehension {ask.rc} — answer in {language}',
                              pages=pages, attribution=f'SEC French {year} {level_name.title()} Level examination paper — © State Examinations Commission.',
                              presentationNote=f'Read the original passage and return to this task. Answer in {language}.')
                card = dict(id=cid, subjectId='french', level=level_name, source='sec', kind='rubric', year=year,
                            paperFileid=doc['doc']['f'].removesuffix('.pdf'), section='A',
                            questionRef=f'{year} {level.upper()} Section A{ask.rc} Q{suffix}', questionText=prompt,
                            totalMarks=maximum, topicId=topic_id, conceptId=f'french-reading-{topic_id}',
                            sourceMaterial=source, specVersion='lc-french-syllabus',
                            schemeCitation=f'SEC French {year} {level_name.title()} Level marking scheme, pp.{", ".join(map(str, scheme_pages))}; general rules p.{record.get("generalRulesPage", 4 if level == "hl" else 3)} — © State Examinations Commission.',
                            schemeRegion=dict(schemeFileid=doc['scheme']['f'], p=scheme_pages[0], r=[0, 0, 1, 1]),
                            rubric=dict(system='french', taskRequirements=requirements, answerGuide=guide,
                                        criteria=[dict(id='response', label='Response', maxMarks=maximum, permittedMarks=allowed,
                                                       guidance=['Use the accepted answers and partial-credit rules above, then apply any stated deductions.'])],
                                        markingGuideNote='Round brackets in the scheme identify extraneous material that is not penalised. The published examples are not necessarily exhaustive; other valid responses may be accepted.'),
                            qa=dict(gates=['visual-paper-scheme-review', 'published-tariff-boundary', 'complete-partial-credit', 'selection-review'], humanReviewedBy='agent-verified', humanReviewedAt=review['reviewedAt']))
                cards.append(card)
                if preserved_id:
                    card['conceptId'] = previous['conceptId']
                if scoring:
                    card['rubric']['taskRequirements'].insert(1, scoring['sourceNote'])
                if split and split.get('taskInstruction'):
                    card['rubric']['taskRequirements'].append(split['taskInstruction'])
                if address in record.get('sourceNotes', {}):
                    card['rubric']['taskRequirements'].insert(1, record['sourceNotes'][address])
                if mcq:
                    choices = prompt.split('\n')[1:]
                    assert len(choices) == 4 and all(choices), cid
                    card['questionChoices'] = choices
                    if choice_review.get('letteredOptions'):
                        correct = choice_review['correctOption']
                        key = f'({chr(97 + correct)})'
                        assert len(ask.answers) == 1 and ask.answers[0]['text'] == key, cid
                        assert guide[0].startswith(f'• {key}'), cid
                        card['rubric']['answerGuide'] = [f'• {key} {choices[correct]} — {maximum} marks.', *guide[1:]]
                tasks.append(dict(cardId=cid, category='reading', subjectId='french', level=level_name, year=year, sitting='main', paperKey='single', lang='ev',
                                  fileid=doc['doc']['f'], n=n, parent=parent, topicIds=topic_ids,
                                  topicId=topic_id, pages=pages, label=f'Reading Comprehension {ask.rc} · Q{suffix}'))
    assert len(cards) == review['expectedCards']
    (ROOT / 'components/MarkBank/cards/french/reading.json').write_text(json.dumps(cards, ensure_ascii=False, indent=2) + '\n')
    write_tasks('reading', tasks)
    print(f'Wrote {len(cards)} reviewed French reading cards and exact Atlas tasks.')


if __name__ == '__main__':
    build()
