#!/usr/bin/env python3
"""Extract review candidates for English's complete Paper Trail corpus.

Candidates stay outside the runtime until their paper boundaries, tariffs,
choices, topics and source pages have been reviewed. No parser-generated
count is treated as independent evidence of completeness.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
from urllib.parse import urlparse
import sys

import fitz
from functools import lru_cache

from english_complete import ROOT, CORPUS, inventory
from english_cards import (
    clean_unicode, compact, comparable, concept_for, requirements_for,
    question_scheme_page, paper_source,
    POET_LABELS,
)

sys.path.insert(0, str(ROOT / 'scripts/paper-trail'))
from english_p2_complete import (  # noqa: E402
    lines_of, collect_single_text_cards, collect_comparative_cards,
    collect_poetry_cards, paper_segments,
)
from english_p2_ol import collect_cards as ordinary_blocks  # noqa: E402

TARIFF = re.compile(r'\(\s*(\d{1,3})\s*(?:marks?)?\s*\)', re.I)
DIRECTIVE = re.compile(
    r'\b(?:choose|choice|select|either|or|any|following|which|'
    r'what (?:one|two|three|four)|one of|answer (?:one|two|three|four|\d+) of)\b', re.I)

TEXT_REPAIRS = json.loads((ROOT / 'scripts/markbank/authored/english-paper-text-repairs.json').read_text())
EXAM_IDENTITIES = json.loads((ROOT / 'scripts/markbank/authored/english-exam-identities.json').read_text())['identities']
SOURCE_ATTACHMENTS = json.loads((ROOT / 'scripts/markbank/authored/english-source-review.json').read_text())['attachments']
TASK_CONTEXT = json.loads((ROOT / 'scripts/markbank/authored/english-task-context.json').read_text())['tasks']
for repair in TEXT_REPAIRS:
    if hashlib.sha256((ROOT / repair['source']).read_bytes()).hexdigest() != repair['sha256']:
        raise ValueError('Source changed under a reviewed text repair: ' + repair['source'])


def exam_identity(record, suffix):
    key = record['id'] + '-' + suffix
    identity = EXAM_IDENTITIES[key]
    if identity['sourceSha256'] != record['questionPaper']['sha256']:
        raise ValueError('Source changed under an exact identity: ' + key)
    return identity


# Comparative mode headings print in capitals; the stem shows the same words in
# their printed wording with the SEC's own case ("General Vision and Viewpoint",
# never a title-cased "Vision And Viewpoint"). An unlisted mode fails closed.
MODE_LABELS = {
    'aspects of story tension or climax or resolution': 'Aspects of Story: Tension or Climax or Resolution',
    'cultural context': 'Cultural Context',
    'the cultural context': 'The Cultural Context',
    'general vision and viewpoint': 'General Vision and Viewpoint',
    'the general vision and viewpoint': 'The General Vision and Viewpoint',
    'hero heroine villain': 'Hero, Heroine, Villain',
    'literary genre': 'Literary Genre',
    'relationships': 'Relationships',
    'social setting': 'Social Setting',
    'theme': 'Theme',
    'theme or issue': 'Theme or Issue',
}


def printed_mode_label(mode, page_text):
    key = comparable(mode)
    if key not in MODE_LABELS:
        raise ValueError('Comparative mode has no printed-case label: ' + mode)
    if key not in comparable(page_text):
        raise ValueError('Comparative mode is not printed on its page: ' + mode)
    return MODE_LABELS[key]


def printed_title(record, doc, identity, key):
    """An identity title must be printed on its paper page (case-insensitively),
    and a title recorded as printed in mixed case must appear exactly so."""
    title = identity['title']
    if 'titleEvidence' not in identity:
        return title
    if comparable(title) not in comparable(doc[identity['paperPage'] - 1].get_text()):
        raise ValueError('Identity title is not printed on its page: ' + key)
    page = identity.get('titlePrintedPage')
    if page:
        text = re.sub(r'\s+', ' ', doc[page - 1].get_text().replace('\xa0', ' '))
        if title not in text:
            raise ValueError('Identity title is not printed in this case: ' + key)
    return title


SYMBOL_MARKERS = str.maketrans({'\uf0b7': '•', '\uf02d': '–'})


def region_text(doc, regions):
    chunks = []
    for region in regions:
        page = doc[region['p'] - 1]
        x0, y0, x1, y1 = region.get('r', [0, 0, 1, 1])
        repair = next((r['pages'].get(str(region['p'])) for r in TEXT_REPAIRS
                       if Path(doc.name).resolve() == (ROOT / r['source']).resolve()), None)
        if repair and y1 == 1:
            chunks.append(repair)
            continue
        rows = []
        for line in lines_of(page):
            if rows and abs(rows[-1][0].y - line.y) < .0045:
                rows[-1].append(line)
            else:
                rows.append([line])
        for row in rows:
            # PDF runs belonging to the same printed baseline can have
            # slightly different font boxes (notably 2025 OL Q1(a)(i)).
            # Keep the complete row at a boundary, in horizontal order.
            if not any(y0 - .0045 <= line.y for line in row) or any(abs(line.y - y1) < .0045 for line in row):
                continue
            if min(line.y for line in row) >= y1:
                continue
            text = ' '.join(line.text for line in sorted(row, key=lambda line: line.x)
                            if x0 * page.rect.width <= line.x < x1 * page.rect.width)
            if not text:
                continue
            if min(line.y for line in row) > .9 and re.fullmatch(
                    r'(?:Higher|Ordinary) Level [–—-] Paper [12]', text, re.I):
                continue
            if re.match(r'^Copyright notice', text, re.I):
                break
            if re.match(r'^(?:Page \d+ of \d+|Leaving Certificate Examination \d{4}|'
                        r'English [–—-] (?:Higher|Ordinary) Level [–—-] Paper [12]|'
                        r'There is no examination material|Copyright notice|©)', text, re.I):
                continue
            if re.fullmatch(r'\d{1,2}', text):
                continue
            if re.match(r'^Question continues on page \d+', text, re.I):
                continue
            if re.fullmatch(r'(?:[A-I]\s*)?\(continued\)', text, re.I):
                continue
            # SymbolMT list markers extract as private-use code points and render as a missing glyph;
            # the paper prints a bullet (U+F0B7) and a dash (U+F02D), as other prompts show them.
            text = text.translate(SYMBOL_MARKERS)
            for repair_record in TEXT_REPAIRS:
                if Path(doc.name).resolve() != (ROOT / repair_record['source']).resolve():
                    continue
                for replacement in repair_record.get('replacements', []):
                    if replacement['page'] == region['p']:
                        text = text.replace(replacement['before'], replacement['after'])
            chunks.append(text)
    # In 2018 OL Poetry A, the separate (a) glyph run starts a fraction
    # above the adjacent 1. marker. They are one printed 1.(a) heading.
    return re.sub(r'(?m)^\(a\)\n1\.\n', '1.\n(a)\n', '\n'.join(chunks))


def question_region(question):
    return question.get('paperRegion') or [
        {'p': question['pP'], 'r': [0, question['pY'][0], 1, question['pY'][1]]}]


def prompt(value):
    value = clean_unicode(value)
    value = re.sub(r'(?mi)^\s*(?:N\.?B\.?\s*)?Candidates may NOT.*$', '', value)
    value = re.sub(r'(?mi)^\s*(?:N\.?B\.?\s*)?Answer only ONE.*$', '', value)
    value = re.sub(r'(?m)^\s*OR\s*$', '', value)
    value = TARIFF.sub('', value)
    value = compact(value)
    value = re.sub(r'(?<=\w)-\s+(?=\w)', '-', value)
    return value.strip()


def numbered(value, pattern):
    matches = list(re.finditer(pattern, value, re.M | re.I))
    return [(m.group(1).lower(), value[m.end():matches[i + 1].start()
            if i + 1 < len(matches) else len(value)]) for i, m in enumerate(matches)]


def source_for_text(doc, number, end_page):
    starts = []
    for index in range(end_page):
        ls = lines_of(doc[index])
        for i, line in enumerate(ls):
            numeral = {1: 'I', 2: 'II', 3: 'III'}[number]
            match = re.match(rf'^TEXT\s*(?:{number}|{numeral})\b\s*[–—-]?\s*(.*)', line.text, re.I)
            if not match or re.search(r'QUESTION|COMPREHENDING', match.group(1), re.I):
                continue
            title = match.group(1).strip()
            if not title:
                title = next((candidate.text for candidate in ls[i + 1:]
                              if candidate.y > line.y and len(candidate.text) > 4), '')
            starts.append((index + 1, title))
    if not starts:
        raise ValueError(f'Text {number}: no source heading before p.{end_page}')
    start, title = starts[-1]
    return paper_source(f'TEXT {number}', title, list(range(start, end_page + 1)),
                        'Source and acknowledgements as printed on the official SEC paper.')


def reference(record, key):
    prefix = f"{record['year']} {'HL' if record['level'] == 'higher' else 'OL'} Paper {record['paper']} "
    if match := re.fullmatch(r't([123])-([ab])(?:-([iv]+)(?:-([ab]))?)?', key):
        number, letter, roman, part = match.groups()
        return prefix + f'Text {number} Q{letter.upper()}' + (f'({roman})' if roman else '') + (f'({part})' if part else '')
    if match := re.fullmatch(r'composing-(\d)', key):
        return prefix + 'Composing ' + match.group(1)
    if match := re.fullmatch(r'single-([a-i])-(i|ii|q[1-4](?:-i{1,3})?)', key):
        letter, part = match.groups()
        suffix = '(' + part + ')' if part in ('i', 'ii') else ' ' + part.upper().split('-')[0] + ''.join('(' + p + ')' for p in part.split('-')[1:])
        return prefix + 'Single Text ' + letter.upper() + suffix
    if match := re.fullmatch(r'comparative-([abc])-q([12])', key):
        return prefix + f'Comparative {match.group(1).upper()} Q{match.group(2)}'
    if match := re.fullmatch(r'unseen-q([123])', key):
        return prefix + 'Unseen Poetry Q' + match.group(1)
    if match := re.fullmatch(r'prescribed-([a-f1-5])(?:-q([12])(?:-(i{1,3}))?)?', key):
        option, number, roman = match.groups()
        if option.isdigit():
            return prefix + 'Prescribed Poetry Q' + option
        return prefix + 'Prescribed Poetry ' + option.upper() + f' Q{number}' + (f'({roman})' if roman else '')
    raise ValueError('Unclassified question reference: ' + key)


@lru_cache(maxsize=None)
def reading_copy_record(paper_id):
    return next(record for record in inventory()['papers'] if record['id'] == paper_id)


def source_from_attachment(attachment, task_id):
    source = paper_source(attachment['label'], attachment['title'],
                          attachment['pages'], attachment['attribution'])
    source['kind'] = attachment['kind']
    if source['kind'] == 'supplementary-text':
        if attachment['pages'] or not attachment.get('texts') or not attachment.get('presentationNote'):
            raise ValueError('Incomplete supplementary reader: ' + task_id)
        source['texts'] = attachment['texts']
    if source['kind'] == 'linked-reading':
        readings = attachment.get('readings', [])
        if attachment['pages'] or not readings or not attachment.get('presentationNote'):
            raise ValueError('Incomplete linked reader: ' + task_id)
        for reading in readings:
            url = urlparse(reading.get('sourceUrl', ''))
            if url.scheme != 'https' or url.hostname not in ('www.examinations.ie', 'ccea.org.uk') or \
                    not all(reading.get(field, '').strip() for field in ('title', 'author', 'edition', 'location')):
                raise ValueError('Unverified linked reading: ' + task_id)
        source['readings'] = readings
    if attachment.get('presentationNote'):
        source['presentationNote'] = attachment['presentationNote']
    if attachment.get('sourcePaperId'):
        record = reading_copy_record(attachment['sourcePaperId'])
        if attachment['sourceSha256'] != record['questionPaper']['sha256'] or \
                not attachment['pages'] or any(p < 1 or p > record['questionPaper']['pages'] for p in attachment['pages']):
            raise ValueError('Stale or invalid reading-copy source: ' + task_id)
        source.update(sourceYear=record['year'], sourceFileid=record['paperFileid'])
    return source


SOURCE_NOT_REQUIRED = 'not-required'


def reviewed_source(task_id, text, default=None):
    attachment = SOURCE_ATTACHMENTS.get(task_id)
    if not attachment:
        return default
    if attachment['questionSha256'] != hashlib.sha256(text.encode('utf-8')).hexdigest():
        raise ValueError('Source attachment has stale question wording: ' + task_id)
    if attachment['kind'] == SOURCE_NOT_REQUIRED:
        # Applied to the leaf task by apply_source_exclusion, which checks
        # the exact default reader it removes.
        return default
    return source_from_attachment(attachment, task_id)


def apply_source_exclusion(task, record):
    """Remove a default comprehension reader only on reviewed, bound evidence.

    The exclusion names the paper hash, the question wording and the exact
    default reader (label, title, pages) it removes, with a written reason.
    Any change to those inputs fails, rather than silently dropping a source.
    """
    attachment = SOURCE_ATTACHMENTS.get(task['id'])
    if not attachment or attachment['kind'] != SOURCE_NOT_REQUIRED:
        return
    default = task.get('sourceMaterial') or {}
    excluded = attachment.get('excludedSource') or {}
    if attachment['questionSha256'] != hashlib.sha256(task['questionText'].encode('utf-8')).hexdigest() or \
            attachment.get('paperSha256') != record['questionPaper']['sha256']:
        raise ValueError('Source exclusion is stale: ' + task['id'])
    if not attachment.get('reason', '').strip() or attachment.get('additionalSources') or \
            any(key in attachment for key in ('pages', 'label', 'title', 'texts', 'readings')):
        raise ValueError('Source exclusion needs only a written reason and the excluded reader: ' + task['id'])
    if not excluded or any(default.get(key) != excluded.get(key) for key in ('label', 'title', 'pages')):
        raise ValueError('Source exclusion does not match the default reader: ' + task['id'])
    del task['sourceMaterial']
    task['taskRequirements'] = requirements_for(task['questionText'], None, [])


def apply_reviewed_context(task, record):
    context = TASK_CONTEXT.get(task['id'])
    if not context:
        return
    if context['questionSha256'] != hashlib.sha256(task['questionText'].encode()).hexdigest() or \
            context['paperSha256'] != record['questionPaper']['sha256']:
        raise ValueError('Reviewed task context changed: ' + task['id'])
    task['contextNotes'] = list(dict.fromkeys(task.get('contextNotes', []) + context['notes']))


def emit(record, key, section, value, marks, scheme_pages, *, source=None,
         topic=None, parent=None, regions=None, stem=None):
    text = prompt(value)
    source = reviewed_source(record['id'] + '-' + key, text, source)
    if len(comparable(text).split()) < 5:
        raise ValueError(f'{key}: empty or truncated prompt: {text!r}')
    page, score = question_scheme_page(text, scheme_pages)
    card = {
        'id': record['id'] + '-' + key,
        'year': record['year'], 'level': record['level'], 'paper': record['paper'],
        'section': section,
        'questionRef': reference(record, key),
        'questionText': text, 'totalMarks': marks, 'printedParts': [],
        'rawQuestionText': clean_unicode(value).strip(),
        'schemePage': page, 'schemeTraceScore': score,
        'topicId': topic, 'conceptId': concept_for(section, text),
        'taskRequirements': requirements_for(text, source, []),
        'paperFileid': record['paperFileid'], 'schemeFileid': record['schemeFileid'],
        'atlasParent': parent, 'paperRegion': regions,
    }
    if source:
        card['sourceMaterial'] = source
    if stem:
        card['stem'] = stem
    if DIRECTIVE.search(value):
        card['selectionReviewRequired'] = True
    return card


def p1_cards(record, doc, sidecar, scheme_pages):
    cards = []
    for question in sorted(sidecar['q'], key=lambda q: q.get('printOrder', int(q['n']))):
        regions = question_region(question)
        text = region_text(doc, regions)
        label = question.get('label', '')
        marker = re.match(r'Comprehending · Text ([123]) · Question ([AB])', label)
        if marker:
            number, letter = int(marker.group(1)), marker.group(2)
            text = re.sub(r'^QUESTION\s+[AB]\.?(?:\s*[–—-]\s*\d+\s*MARKS?)?', '', text, flags=re.I).strip()
            if letter == 'B':
                printed = TARIFF.findall(text)
                heading = region_text(doc, regions).split('\n')[0]
                tariff = re.search(r'(\d+)\s*MARK', heading, re.I)
                marks = int(tariff.group(1)) if tariff else int(printed[-1]) if printed else 50
                cards.append(emit(record, f't{number}-b', 'Comprehending B', text,
                                  marks, scheme_pages, topic='english-10-1',
                                  parent=question['n'], regions=regions))
                continue
            source = source_for_text(doc, number, question['pP'])
            parts = numbered(text, r'^\s*\((i{1,3}|iv)\)\s*')
            if [key for key, _ in parts] != ['i', 'ii', 'iii']:
                raise ValueError(f'Text {number} QA: roman parts not reconciled {parts}')
            for roman, body in parts:
                subparts = numbered(body, r'^\s*\(([ab])\)\s*')
                # A printed marker is a separate task only when each part
                # actually carries its own tariff. Lists of required aspects
                # inside one holistic response do not become separate cards.
                if len(subparts) > 1 and all(TARIFF.search(b) for _, b in subparts):
                    shared = body[:re.search(r'^\s*\([ab]\)', body, re.M | re.I).start()]
                    units = [(roman + '-' + suffix, shared + '\n' + part) for suffix, part in subparts]
                else:
                    units = [(roman, body)]
                for suffix, part in units:
                    tariffs = TARIFF.findall(part)
                    if len(tariffs) != 1:
                        raise ValueError(f'Text {number} QA({suffix}): tariffs {tariffs}: {part}')
                    cards.append(emit(record, f't{number}-a-{suffix}', 'Comprehending A', part,
                                      int(tariffs[0]), scheme_pages, source=source,
                                      topic='english-10-0', parent=question['n'], regions=regions))
        else:
            number = int(question['n'])
            if not 1 <= number <= 7:
                raise ValueError('Unclassified Paper 1 block: ' + str(question))
            text = re.sub(rf'^\s*{number}\.\s*', '', text)
            cards.append(emit(record, f'composing-{number}', 'Composing', text,
                              100, scheme_pages, topic='english-9-1',
                              parent=question['n'], regions=regions))
    return cards


MODE_TOPICS = {
    'theme': 'english-7-0', 'theme or issue': 'english-7-0',
    'literary genre': 'english-7-2', 'cultural context': 'english-7-3',
    'general vision and viewpoint': 'english-7-4',
    'hero heroine villain': 'english-7-5', 'relationships': 'english-7-6',
    'social setting': 'english-7-7',
    'aspects of story tension or climax or resolution': 'english-7-10',
}


def p2_cards(record, doc, sidecar, scheme_pages):
    higher = record['level'] == 'higher'
    blocks = (collect_single_text_cards(doc) + collect_comparative_cards(doc)
              + collect_poetry_cards(doc)) if higher else ordinary_blocks(doc, record['year'])
    cards = []
    for block in blocks:
        regions = paper_segments(block)
        raw = region_text(doc, regions)
        # A block can end at the next task after a section heading. The
        # next section's overall tariff is not part of this response.
        raw = re.split(r'(?m)^\s*SECTION\s+[IVX]+\b', raw)[0]
        legacy = next((q for q in sidecar.get('q', []) if q['pP'] == block.p_page + 1
                       and abs(q['pY'][0] - block.p_y) < .04), None)
        parent = legacy['n'] if legacy else None
        source, stem = None, block.label
        if block.kind == 'single':
            letter = re.search(r'Single Text ([A-I])', block.label).group(1).lower()
            identity = exam_identity(record, f'single-{letter}')
            topic = identity['topicId']
            stem = identity['canonicalLabel']
            section = 'Single Text'
            if higher:
                roman = re.search(r'\((i|ii)\)$', block.label).group(1)
                units = [(f'single-{letter}-{roman}', re.sub(r'^\s*\(ii?\)\s*', '', raw),
                          70 if record['year'] in (2021, 2022) else 60)]
            else:
                parts = numbered(raw, r'^\s*([1-4])\.\s*')
                numbers = [n for n, _ in parts]
                if numbers == ['1', '2', '3', '4']:
                    common_tariff = re.search(r'Each question carries (\d+) marks', raw, re.I)
                    if not common_tariff:
                        raise ValueError(f'{block.label}: missing common question tariff')
                    units = [(f'single-{letter}-q{n}', value, int(common_tariff.group(1)))
                             for n, value in parts]
                elif numbers in (['1', '2', '3'], ['1', '2']):
                    units = []
                    for number, value in parts:
                        choices = numbered(value, r'^\s*\((i{1,3})\)\s*')
                        if choices and re.search(r'Answer ONE', value, re.I):
                            tariff = re.search(r'Each part carries (\d+) marks', value, re.I)
                            if not tariff:
                                raise ValueError(f'{block.label} Q{number}: missing choice tariff')
                            units.extend((f'single-{letter}-q{number}-{n}', choice, int(tariff.group(1)))
                                         for n, choice in choices)
                        else:
                            tariffs = [int(n) for n in TARIFF.findall(value)]
                            if not tariffs:
                                raise ValueError(f'{block.label} Q{number}: missing tariff')
                            units.append((f'single-{letter}-q{number}', value, sum(tariffs)))
                else:
                    raise ValueError(f'{block.label}: unclassified Single Text questions {numbers}')
        elif block.kind == 'comparative':
            section = 'Comparative Study'
            letter = re.search(r'Comparative ([ABC])', block.label).group(1).lower()
            mode = block.label.split(' · ')[1]
            topic = MODE_TOPICS[re.sub(r'^the ', '', comparable(mode))]
            pieces = block.label.split(' · ')
            pieces[1] = printed_mode_label(mode, doc[block.p_page].get_text())
            stem = ' · '.join(pieces)
            if higher:
                number = block.label.rsplit('Q', 1)[1]
                units = [(f'comparative-{letter}-q{number}',
                          re.sub(r'^\s*[12]\.\s*', '', raw), 70)]
            else:
                parts = numbered(raw, r'^\s*([12])\.\s*')
                if [n for n, _ in parts] != ['1', '2']:
                    raise ValueError(f'{block.label}: expected both Comparative questions')
                units = [(f'comparative-{letter}-q{n}', value, 70) for n, value in parts]
        elif block.kind == 'unseen':
            section, topic = 'Unseen Poetry', 'english-8-2'
            source_pages = sorted({r['p'] for r in regions if r['r'][3] > .02})
            source = paper_source('UNSEEN POEM', 'Unseen poem', source_pages,
                                  'Title and poet as printed on the official SEC paper.')
            if higher:
                number = block.label.rsplit('Q', 1)[1]
                units = [(f'unseen-q{number}', re.sub(r'^\s*[12]\.\s*', '', raw), 20)]
            else:
                parts = numbered(raw, r'^\s*([123])\.\s*')
                if [n for n, _ in parts] not in (['1', '2'], ['1', '2', '3']):
                    raise ValueError('Unseen poem: unclassified question sequence')
                units = [(f'unseen-q{n}', value, 10) for n, value in parts]
        else:
            section = 'Prescribed Poetry'
            if higher:
                number = block.label.rsplit('Q', 1)[1]
                value = re.sub(r'^\s*[1-5]\.\s*', '', raw)
                identity = exam_identity(record, f'prescribed-{number}')
                topic, stem = identity['topicId'], identity['canonicalLabel']
                # Some papers put the next poet's name immediately ABOVE
                # their question number. The geometric numbered block must
                # stop before that heading, rather than swallowing it.
                rows = value.splitlines()
                if identity.get('promptHeading'):
                    if not rows or comparable(rows[0]) != comparable(identity['promptHeading']):
                        raise ValueError('Reviewed poet heading changed: ' + record['id'] + '-' + number)
                    rows.pop(0)
                while rows and comparable(rows[-1]) in POET_LABELS:
                    rows.pop()
                value = '\n'.join(rows)
                units = [(f'prescribed-{number}', value, 50)]
            else:
                letter = re.search(r'Poetry ([A-F])', block.label).group(1).lower()
                identity = exam_identity(record, f'prescribed-{letter}')
                poem, poet = printed_title(record, doc, identity, f'prescribed-{letter}'), identity['canonicalLabel']
                stem = f'{poem} — {poet}'
                source_pages = identity.get('sourcePages') or sorted({r['p'] for r in regions if r['r'][3] > .04})
                source = paper_source(f'PRESCRIBED POEM {letter.upper()}', poem,
                                      source_pages, f'{poem} — {poet}.')
                topic = identity['topicId']
                # Line numbers in the poem itself (for example The Collar)
                # must not become question markers. Q1 starts with part (a).
                first_question = re.search(r'^\s*1\.\s*\(a\)', raw, re.M | re.I)
                if not first_question:
                    raise ValueError(f'{block.label}: no Q1(a) boundary')
                parts = numbered(raw[first_question.start():], r'^\s*([12])\.\s*')
                if [n for n, _ in parts] != ['1', '2']:
                    raise ValueError(f'{block.label}: expected Q1 and Q2')
                choices = numbered(parts[1][1], r'^\s*\((i{1,3})\)\s*')
                if [n for n, _ in choices] != ['i', 'ii', 'iii']:
                    raise ValueError(f'{block.label}: expected three Q2 choices')
                units = [(f'prescribed-{letter}-q1', parts[0][1], 30)] + [
                    (f'prescribed-{letter}-q2-{n}', value, 20) for n, value in choices]
        for key, value, total in units:
            tariffs = [int(n) for n in TARIFF.findall(value)]
            # Cut any source poem following a questions-first layout at the
            # final printed tariff. The complete poem remains in the reader.
            if block.kind == 'unseen' and tariffs:
                last = list(TARIFF.finditer(value))[-1]
                value = value[:last.end()]
            result = emit(record, key, section, value, total, scheme_pages,
                          source=source, topic=topic, parent=parent, regions=regions, stem=stem)
            result['printedTariffs'] = tariffs
            result['boundaryReviewRequired'] = len(tariffs) > 1 or (tariffs and sum(tariffs) != total)
            cards.append(result)
    return cards


def split_marked_tasks(card, scheme_pages):
    """Propose leaf tasks at printed tariffs, retaining the whole context.

    These are still review candidates. A printed tariff is evidence to check
    against the scheme, not automatic authorization to publish a boundary.
    """
    raw = card['rawQuestionText']
    tariffs = list(TARIFF.finditer(raw))
    if len(tariffs) < 2:
        return [card]
    if sum(int(match.group(1)) for match in tariffs) != card['totalMarks']:
        raise ValueError(f"{card['id']}: unreconciled part tariffs")
    markers = list(re.finditer(r'(?m)^\s*\(?([a-c]|i{1,3}|iv)\)\s*', raw))
    if not markers:
        raise ValueError(f"{card['id']}: tariffs without part labels")
    shared = raw[:markers[0].start()].strip()
    previous, parent_letter, tasks = 0, '', []
    for tariff_index, tariff in enumerate(tariffs):
        start = markers[0].start() if previous == 0 else previous
        segment = raw[start:tariff.start()].strip()
        first_marker = re.search(r'(?m)^\s*\(?[a-ciIvV]{1,3}\)\s*', segment)
        local_context = segment[:first_marker.start()].strip() if first_marker else ''
        if first_marker:
            segment = segment[first_marker.start():].strip()
        heading = re.match(r'^(?:\(?[a-ciIvV]{1,3}\)\s*)+', segment)
        labels = list(re.finditer(r'\(?([a-c]|i{1,3}|iv)\)\s*', heading.group(0))) if heading else []
        if not labels:
            raise ValueError(f"{card['id']}: marked part has no label")
        for label in labels:
            if label.group(1) in ('a', 'b', 'c'):
                parent_letter = label.group(1)
        leaf = labels[-1]
        suffix = (parent_letter + '-' if leaf.group(1) not in ('a', 'b', 'c') else '') + leaf.group(1)
        value = segment[heading.end():].strip()
        # A shared stem can separate the printed (a) and (i) markers.
        # Recognise it only when a separately tariffed (ii) immediately
        # follows; unmarked roman lists inside a holistic part stay intact.
        if leaf.group(1) in ('a', 'b', 'c') and tariff_index + 1 < len(tariffs):
            following = raw[tariff.end():tariffs[tariff_index + 1].start()].strip()
            delayed_first = re.search(r'(?m)^\s*\(i\)\s*', value)
            if delayed_first and re.match(r'^\(ii\)\s*', following):
                suffix += '-i'
                value = value[:delayed_first.start()].strip() + '\n' + value[delayed_first.end():].strip()
        task = dict(card)
        task.update({
            'id': card['id'] + '-' + suffix,
            'parentTaskId': card['id'],
            'partLabel': '(' + suffix.replace('-', ')(') + ')',
            'questionRef': card['questionRef'] + '(' + suffix.replace('-', ')(') + ')',
            'questionText': prompt((shared + '\n' if shared else '') + value),
            'rawQuestionText': (shared + '\n' if shared else '') + value,
            'totalMarks': int(tariff.group(1)),
            'printedTariffs': [int(tariff.group(1))],
            'boundaryReviewRequired': True,
            'boundaryEvidence': 'Separate printed tariff; scheme confirmation required.',
            'parentQuestionText': card['questionText'],
            'selectionReviewRequired': bool(DIRECTIVE.search(value)),
        })
        task['schemePage'], task['schemeTraceScore'] = question_scheme_page(task['questionText'], scheme_pages)
        task['taskRequirements'] = requirements_for(task['questionText'], task.get('sourceMaterial'), [])
        if local_context:
            task['contextNotes'] = [prompt(local_context)]
        tasks.append(task)
        previous = tariff.end()
    if len(set(task['id'] for task in tasks)) != len(tasks):
        raise ValueError(f"{card['id']}: repeated marked part identity")
    return tasks


def extract_record(record):
    """Extract one complete paper atomically, restricting scheme traces by block."""
    with fitz.open(ROOT / record['questionPaper']['path']) as doc, \
            fitz.open(ROOT / record['markingScheme']['path']) as scheme:
        sidecar_path = ROOT / 'scripts/paper-trail/answers' / str(record['year']) / (record['paperFileid'] + '.json')
        sidecar = json.loads(sidecar_path.read_text()) if sidecar_path.exists() else {}
        pages = {i + 1: page.get_text() for i, page in enumerate(scheme)}
        parsed = (p1_cards if record['paper'] == 1 else p2_cards)(record, doc, sidecar, pages)
        parents = {q['n']: q for q in sidecar['q']}
        scopes, leaf_tasks = {}, []
        for card in parsed:
            parent = parents[card['atlasParent']]
            regions = parent.get('schemeRegion') or parent['region']
            card['schemeParentRegion'] = regions
            if parent['n'] not in scopes:
                scoped = {}
                for region in regions:
                    scoped[region['p']] = scoped.get(region['p'], '') + '\n' + region_text(scheme, [region])
                scopes[parent['n']] = scoped
            scoped = scopes[parent['n']]
            card['schemePage'], card['schemeTraceScore'] = question_scheme_page(card['questionText'], scoped)
            for task in split_marked_tasks(card, scoped):
                source = reviewed_source(task['id'], task['questionText'], task.get('sourceMaterial'))
                if source:
                    task['sourceMaterial'] = source
                    task['taskRequirements'] = requirements_for(task['questionText'], source, [])
                additional = SOURCE_ATTACHMENTS.get(task['id'], {}).get('additionalSources', [])
                if additional:
                    task['additionalSourceMaterials'] = [source_from_attachment(a, task['id']) for a in additional]
                apply_source_exclusion(task, record)
                apply_reviewed_context(task, record)
                leaf_tasks.append(task)
        return parsed, leaf_tasks


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--year', type=int)
    parser.add_argument('--level', choices=['higher', 'ordinary'])
    parser.add_argument('--paper', type=int, choices=[1, 2])
    parser.add_argument('--output', default='tmp/english-audit/all-candidates.json')
    args = parser.parse_args()
    records = [p for p in inventory()['papers'] if (not args.paper or p['paper'] == args.paper)
               and (not args.year or p['year'] == args.year)
               and (not args.level or p['level'] == args.level)]
    cards, tasks, failures = [], [], []
    for record in records:
        try:
            parsed, leaf_tasks = extract_record(record)
            cards.extend(parsed)
            tasks.extend(leaf_tasks)
            print(record['id'], len(parsed), 'candidates')
        except Exception as error:
            failures.append({'paper': record['id'], 'error': str(error)})
            print(record['id'], 'FAILED', str(error)[:200])
    out = ROOT / args.output
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({'cards': cards, 'tasks': tasks, 'failures': failures}, ensure_ascii=False, indent=2) + '\n')
    print(f'{len(cards)} candidates; {len(failures)} papers require parser repair; no runtime data written.')
    return bool(failures)


if __name__ == '__main__':
    raise SystemExit(main())
