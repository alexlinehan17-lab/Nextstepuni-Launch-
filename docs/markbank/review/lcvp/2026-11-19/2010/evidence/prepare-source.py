#!/usr/bin/env python3
"""Review-only 2010 source selectors. No production writes or source requests."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import re
import sys
import fitz

HERE = Path(__file__).resolve().parent
READING = HERE.parent / '2026-11-19-lcvp-2010-independent'
LANE = Path('/Users/alexlinehan/Documents/Nextstepuni-LCVP-Release-20261119')
sys.path.insert(0, str(LANE / 'scripts/markbank/authoring'))
from lcvp_review_2026 import tidy
from lcvp_review_2024 import split_raw
from lcvp_review_2017 import header_body

manifest = json.loads((READING / 'source-manifest.json').read_text())
documents = {}
for record in manifest['sources']:
    path = Path(record['path'])
    assert hashlib.sha256(path.read_bytes()).hexdigest() == record['sha256']
    documents[record['kind']] = fitz.open(path)
paper, scheme = documents['paper'], documents['scheme']
reading = json.loads((READING / 'first-reading-frozen.json').read_text())
paper_furniture, scheme_furniture, prompts = {}, {}, {}


def scheme_raw(number):
    page = scheme[number - 1]
    footers = [line for block in page.get_text('dict')['blocks'] for line in block.get('lines', [])
               if tidy(''.join(s['text'] for s in line['spans'])) == str(number)
               and 756 < line['bbox'][1] < 760 and 297 < line['bbox'][0] < 304]
    assert len(footers) == 1, (number, footers)
    box = fitz.Rect(footers[0]['bbox'])
    scheme_furniture[str(number)] = {'text': str(number), 'box': list(box)}
    return page.get_text(clip=fitz.Rect(0, 15, page.rect.width, box.y0 - 2), sort=True)


def paper_raw(number):
    page = paper[number - 1]
    lines, removed = [], []
    for block in page.get_text('dict')['blocks']:
        for line in block.get('lines', []):
            kept = []
            for span in line['spans']:
                value, box = tidy(span['text']), fitz.Rect(span['bbox'])
                office = value in ['Don Oifig', 'Office Use', 'Only', '1', '2'] and box.x0 > 520 and box.y1 < 100
                footer = re.fullmatch(r'Page \d+ of 32', value) and box.y0 > 800
                if office or footer:
                    removed.append({'text': span['text'], 'box': list(box)})
                else:
                    kept.append(span['text'])
            if tidy(''.join(kept)):
                lines.append((line['bbox'][1], line['bbox'][0], tidy(''.join(kept))))
    paper_furniture[str(number)] = removed
    return '\n'.join(value for _, _, value in sorted(lines))


def ref(section, q, letter=None, roman=None):
    return section + str(q) + (f'({letter})' if letter else '') + (f'({roman})' if roman else '')


def clean_prompt(text):
    return tidy(re.sub(r'\b\d+\s+[Mm]arks?\b', '', text))


def scheme_parts():
    text = '\n'.join(scheme_raw(n) for n in range(4, 18))
    text = re.sub(r'^\s*Part [123]\s*$', '', text, flags=re.M)
    sections = split_raw(text, r'^\s*Section ([ABC])\s+', list('ABC'))
    out = {}
    for section, text in sections.items():
        questions = split_raw(text, r'^\s*Q\.?\s*(\d+)\s*', [str(n) for n in range(1, {'A': 8, 'B': 3, 'C': 6}[section] + 1)])
        for q, block in questions.items():
            if section == 'A':
                out[ref(section, q)] = block
                prompts[ref(section, q)] = clean_prompt(header_body(block)[0])
            elif section == 'B':
                header, answers = header_body(block)
                wanted = ['i', 'ii', 'iii'] if q == '3' else ['i', 'ii']
                for roman, text in split_raw(header, r'^\s*\((i{1,3})\)\s*', wanted).items():
                    prompts[ref(section, q, roman=roman)] = clean_prompt(text)
                if q == '1':
                    marker = list(re.finditer(r'^\s*2\.\s*Reasons:', answers, re.M))
                    assert len(marker) == 1
                    parts = {'i': answers[:marker[0].start()], 'ii': answers[marker[0].end():]}
                else:
                    parts = split_raw(answers, r'^\s*\((i{1,3})\)\s*', wanted)
                for roman, text in parts.items():
                    out[ref(section, q, roman=roman)] = text
            else:
                for letter, part in split_raw(block, r'^\s*\(([abcd])\)\s*', list('abcd')).items():
                    if (q, letter) == ('4', 'd'):
                        header, answers = header_body(part)
                        for roman, text in split_raw(header, r'^\s*\((i{1,2})\)\s*', ['i', 'ii']).items():
                            prompts[ref(section, q, letter, roman)] = clean_prompt(text)
                        for roman, text in split_raw(answers, r'^\s*\((i{1,2})\)\s*', ['i', 'ii']).items():
                            out[ref(section, q, letter, roman)] = text
                    else:
                        out[ref(section, q, letter)] = part
                        prompts[ref(section, q, letter)] = clean_prompt(header_body(part)[0])
    assert len(out) == 40
    return out


def question(item):
    m = re.fullmatch(r'([ABC])(\d+)(?:\(([abcd])\))?(?:\((i{1,3})\))?', item['ref'])
    section, q, letter, roman = m.groups()
    value = paper_raw(item['paperPages'][0])
    if section in ['A', 'B']:
        value = re.split(r'^\s*Q\.?\s*' + q + r'\s*', value, maxsplit=1, flags=re.M)[1]
        value = re.split(r'^\s*Q\.?\s*\d+\s*', value, maxsplit=1, flags=re.M)[0]
    if letter and re.search(r'\(' + letter + r'\)', value):
        value = re.split(r'^\s*\(' + letter + r'\)\s*', value, maxsplit=1, flags=re.M)[1]
        value = re.split(r'^\s*\([abcd]\)\s*', value, maxsplit=1, flags=re.M)[0]
    if roman:
        value = re.split(r'\(' + roman + r'\)\s*', value, maxsplit=1)[1]
        value = re.split(r'\(i{1,3}\)\s*', value, maxsplit=1)[0]
    value = clean_prompt(value)
    assert value and not re.search(r'Office Use|Don Oifig|Page \d+|Section [ABC]|\b1 2\b', value), (item['ref'], value)
    return value


raw = scheme_parts()
assert set(raw) == set(prompts) == {item['ref'] for item in reading['items']}
records = []
for item in reading['items']:
    identifier = 'lcvp-2010-cl-' + re.sub(r'[()]', '', item['ref']).lower()
    records.append(dict(id=identifier, ref=item['ref'], questionText=question(item), paperPages=item['paperPages'],
                        schemePages=item['schemePhysicalPages'], sourceSchemeBlock=raw[item['ref']],
                        sourceSchemePrompt=prompts[item['ref']], proposedCardMarks=item['cardMarks'],
                        proposedHeadingIds=item['headingIds'], perAskHeadingIds=item.get('perAskHeadingIds'),
                        sourceDecision=item['readingNote']))
assert sum(len(r['proposedCardMarks']) for r in records) == 48
assert sum(sum(r['proposedCardMarks']) for r in records) == 210
stems = {}
for q, number in [(1, 14), (2, 17), (3, 20), (4, 23), (5, 26), (6, 29)]:
    text = re.split(r'^\s*Q\.?\s*' + str(q) + r'\.?\s*', paper_raw(number), maxsplit=1, flags=re.M)[1]
    stems[str(q)] = tidy(text.split('(a)', 1)[0])
payload = dict(recordedAt=datetime.now(timezone.utc).isoformat(), status='Review-only source selections; no production writes.',
               sourceSha256={s['kind']: s['sha256'] for s in manifest['sources']}, printedParts=40, proposedAsks=48,
               offeredMarks=210, candidateMaximum=160, sectionCStems=stems, records=records,
               unresolvedAlternatives={'B2(i)': {'combinedMarks': [6], 'splitMarks': [3, 3]},
                                       'C3(a)': {'combinedMarks': [6], 'splitMarks': [2, 2, 2]}},
               pending='Two disputed split groups, generic B2(ii) consistency, five display-heading differences, source/application checks and SEC archive/media follow-up.')
(HERE / 'source-parts.json').write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n')
(HERE / 'removed-paper-furniture.json').write_text(json.dumps(paper_furniture, ensure_ascii=False, indent=2) + '\n')
(HERE / 'removed-scheme-footers.json').write_text(json.dumps(scheme_furniture, ensure_ascii=False, indent=2) + '\n')
print('Selected40 original parts; provisional48 asks/210 marks. Both disputed alternatives remain unresolved.')
