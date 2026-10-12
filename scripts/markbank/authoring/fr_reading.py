#!/usr/bin/env python3
"""Generate only the reading papers independently reviewed in the source ledger.

Keep every scheme line, including all partial-credit rungs and examiner notes.
Printed matching subparts are distinct tasks; required details and open textual
evidence remain one response. MCQ distractors are never alternative tasks.

Every string a card shows as the SEC's is lifted from the paper or scheme page
(fr_printed, fr_printed_rules): the parsed scheme lines only locate the printed
ones, so markers, punctuation and wording are the page's own. NextStepUni's own
guidance goes to practiceNotes, never to an SEC-attributed field.
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
from fr_printed import lift, try_lift, doc_texts, skeleton, MARKER
import fr_printed_rules as printed_rules

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


def synthesized(record):
    """Lines the reviewed block rewrites add so the parser can price older
    Ordinary tasks ("Question 2:", "Corinne:"). The scheme never prints them."""
    out = set()
    for block in record.get('schemeBlocks', []):
        source = {' '.join(line.split()) for line in block['sourceLines']}
        for line in block['replacementLines']:
            line = ' '.join(line.split())
            if line not in source:
                out.add(re.sub(r'^\d+\.\s*(?:-\s*)?', '', line))
    return out


def corrected(record):
    """Reviewed line corrections that add what the scheme does not print (a
    marker, an item number, a tariff): the printed line each one replaces."""
    bare = lambda line: re.sub(r'^\d+\.\s*(?:-\s*)?', '', ' '.join(line.split()))
    return {bare(c['to']): bare(c['from']) for c in record.get('schemeLineCorrections', [])}


def printed_guide(guide, path, pages, aliases, added, what, corrections=None):
    """Each guide paragraph as the scheme prints it, and any page it was found
    on beyond the cited ones. A paragraph the parser's rewrites added is left
    out; every other paragraph must lift."""
    groups = doc_texts(path, pages, aliases)
    count = len(fitz.open(path))
    near = [p for p in (pages[0] - 1, pages[-1] + 1) if 1 <= p <= count]
    shown, extra = [], []
    for para in guide:
        if not skeleton(para)[0]:
            continue  # a stray marker with no wording
        bare = ' '.join(re.sub(rf'^{MARKER}\s*', '', para).split())
        if corrections and bare in corrections and corrections[bare] != bare:
            marker = re.match(rf'^({MARKER})\s*', para)
            para = (marker[1] + ' ' if marker else '') + corrections[bare]
            bare = corrections[bare]
        if bare in added:
            got = try_lift(groups, para)
            if got is None or (bare.endswith(':') and re.sub(rf'^{MARKER}\s*', '', got) != bare):
                continue
            shown.append(got)
            continue
        got = try_lift(groups, para)
        if got is None:
            for page in near:
                got = try_lift(doc_texts(path, [page], aliases), para)
                if got is not None:
                    extra.append(page)
                    break
        assert got is not None, (what, para, 'not printed on or beside the cited pages')
        shown.append(got)
    return shown, sorted(set(extra))


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
            paper_groups = doc_texts(paper.path, paper.rc_pages[ask.rc])
            context = record.get('paperContextLines', {}).get(address)
            if context:
                assert context['reason'] and context['page'] == question_page, address
                with fitz.open(paper.path) as source_pdf:
                    lines = [' '.join(line.split()) for line in source_pdf[question_page - 1].get_text(sort=True).splitlines()]
                assert context['sourceLine'] in lines, address
                question += '\n\n' + ' '.join(re.sub(r'_+', '', context['sourceLine']).split())
            shared_tariff = record.get('sevenPlusOne', {}).get(address)
            question_group = record.get('paperQuestionGroups', {}).get(address)
            if question_group:
                assert question_group['questions'][0] == ask.item and question_group['reason'], address
                prompts = []
                for item in question_group['questions']:
                    found = paper.find(ask.rc, item, None, record['paperCues'][f'A{ask.rc}-Q{item}'])
                    assert found, (address, item)
                    # The paper's own numbering, not a "Question N:" label.
                    prompts.append(lift(paper_groups, f'{item}. {found[0]}', marks='', what=address))
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
                    # The whole printed question, then this part's printed label.
                    question = (lift(paper_groups, split['printedQuestion'], marks='', what=address) + '\n\n'
                                + lift(paper_groups, split['printedLabels'][ask.letter], marks='', what=address))
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
                    prompt = question + '\n\n' + part.text
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
                # Each line as the paper prints it (hyphens, apostrophes, spacing).
                prompt = '\n'.join(lift(paper_groups, line, marks='', what=n) if line.strip() else line
                                    for line in prompt.split('\n'))
                opinion_question = record.get('ordinaryOpinionQuestions', {}).get(str(ask.rc), 8)
                english = (level == 'hl' and ask.item == 6) or (level == 'ol' and (ask.rc < 3 or ask.item == opinion_question))
                # The SEC's own rules: the paper's instruction, then the scheme's.
                practice = []
                requirements = []
                if level == 'hl':
                    kind = 'mcq' if mcq else 'english' if english else 'french'
                    requirements.append(printed_rules.reading_language(year, level, kind)[0])
                    requirements += printed_rules.reading_general_points(year, record.get('generalRulesPage', 4))
                    note = record.get('sourceNotes', {}).get(address, '')
                    if ask.item == 6 and note.startswith('Special'):
                        requirements.append(printed_rules.special_segment_rule(year))
                else:
                    if english:
                        requirements.append(printed_rules.reading_language(year, level, 'english')[0])
                    mcq_instruction = printed_rules.reading_mcq_instruction(year, level, paper.rc_pages[ask.rc]) if mcq else None
                    if mcq_instruction:
                        requirements.append(mcq_instruction[0])
                    elif mcq:
                        practice.append('Select one answer. The other printed options are distractors.')
                    if english:
                        requirements += printed_rules.ordinary_equivalence(year)
                    else:
                        practice.append('Answer in French.')
                    if ask.rc >= 3:
                        requirements += printed_rules.ordinary_question_rules(year, ask.rc)[0]
                if shared_tariff:
                    assert maximum == 8 and shared_tariff['reason'], address
                    requirements.append(lift(doc_texts(DATA / f'schemes/{year}-{level}.pdf', scheme_pages), shared_tariff['printedRule'], marks='', what=address))
                    practice.append('Give both required answers. Award 7 marks for one correct answer and 1 additional mark for the second correct answer (8 marks total).')
                elif ask.count > 1 and not ask.letter_to:
                    practice.append(f'Give {ask.count} distinct points. Each earns at most {ask.per} marks; do not score the same point twice.')
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
                source = dict(kind='source-text', label=f'Reading Comprehension {ask.rc}', title=f'Reading Comprehension {ask.rc}',
                              pages=pages, attribution=f'SEC French {year} {level_name.title()} Level examination paper — © State Examinations Commission.',
                              presentationNote='Read the original passage and return to this task.')
                aliases = tuple(alias['glyph'] for alias in record.get('schemeBulletAliases', []))
                scheme_path = DATA / f'schemes/{year}-{level}.pdf'
                if choice_review.get('letteredOptions'):
                    # The scheme prints the letter; the option it names is quoted
                    # as our note, never joined to the scheme's line.
                    choices = prompt.split('\n')[1:]
                    practice.append(f'The scheme’s answer ({chr(97 + choice_review["correctOption"])}) is this option on the paper: “{choices[choice_review["correctOption"]]}”')
                guide, extra_pages = printed_guide(guide, scheme_path, scheme_pages, aliases, synthesized(record), cid, corrected(record))
                cited = sorted(set(scheme_pages) | set(extra_pages))
                card = dict(id=cid, subjectId='french', level=level_name, source='sec', kind='rubric', year=year,
                            paperFileid=doc['doc']['f'].removesuffix('.pdf'), section='A',
                            questionRef=f'{year} {level.upper()} Section A{ask.rc} Q{suffix}', questionText=prompt,
                            totalMarks=maximum, topicId=topic_id, conceptId=f'french-reading-{topic_id}',
                            sourceMaterial=source, specVersion='lc-french-syllabus',
                            schemeCitation=f'SEC French {year} {level_name.title()} Level marking scheme, pp.{", ".join(map(str, cited))}; general rules p.{record.get("generalRulesPage", 4 if level == "hl" else 3)} — © State Examinations Commission.',
                            schemeRegion=dict(schemeFileid=doc['scheme']['f'], p=cited[0], r=[0, 0, 1, 1]),
                            rubric=dict(system='french', taskRequirements=requirements, answerGuide=guide,
                                        criteria=[dict(id='response', label='Response', maxMarks=maximum, permittedMarks=allowed, guidance=[])],
                                        markingGuideNote='\n'.join(printed_rules.scheme_notes(year, level)), practiceNotes=practice),
                            qa=dict(gates=['visual-paper-scheme-review', 'published-tariff-boundary', 'complete-partial-credit', 'selection-review'], humanReviewedBy='agent-verified', humanReviewedAt=review['reviewedAt']))
                cards.append(card)
                if preserved_id:
                    card['conceptId'] = previous['conceptId']
                if scoring:
                    practice.append(scoring['sourceNote'])
                if split and split.get('taskInstruction'):
                    practice.append(split['taskInstruction'])
                if address in record.get('sourceNotes', {}):
                    practice.append(record['sourceNotes'][address])
                practice.append('Use the accepted answers and partial-credit rules above, then apply any stated deductions.')
                if mcq:
                    choices = prompt.split('\n')[1:]
                    assert len(choices) == 4 and all(choices), cid
                    card['questionChoices'] = choices
                    if choice_review.get('letteredOptions'):
                        key = f'({chr(97 + choice_review["correctOption"])})'
                        assert len(ask.answers) == 1 and ask.answers[0]['text'] == key, cid
                        assert re.match(rf'(?:{MARKER}\s*)?{re.escape(key)}', card['rubric']['answerGuide'][0]), cid
                tasks.append(dict(cardId=cid, category='reading', subjectId='french', level=level_name, year=year, sitting='main', paperKey='single', lang='ev',
                                  fileid=doc['doc']['f'], n=n, parent=parent, topicIds=topic_ids,
                                  topicId=topic_id, pages=pages, label=f'Reading Comprehension {ask.rc} · Q{suffix}'))
    assert len(cards) == review['expectedCards']
    (ROOT / 'components/MarkBank/cards/french/reading.json').write_text(json.dumps(cards, ensure_ascii=False, indent=2) + '\n')
    write_tasks('reading', tasks)
    print(f'Wrote {len(cards)} reviewed French reading cards and exact Atlas tasks.')


if __name__ == '__main__':
    build()
