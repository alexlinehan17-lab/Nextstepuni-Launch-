#!/usr/bin/env python3
"""Review-only selections from hash-verified 2023 deferred originals."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import re
import sys
import fitz

HERE = Path(__file__).resolve().parent
READING = HERE.parent / '2026-11-19-lcvp-2023-deferred-independent'
LANE = Path('/Users/alexlinehan/Documents/Nextstepuni-LCVP-Release-20261119')
sys.path.insert(0, str(LANE / 'scripts/markbank/authoring'))
from lcvp_review_2026 import tidy
from lcvp_review_2024 import split_raw

manifest = json.loads((READING / 'source-manifest.json').read_text())
docs = {}
for item in manifest['sources']:
    assert hashlib.sha256(Path(item['path']).read_bytes()).hexdigest() == item['sha256']
    docs[item['kind']] = fitz.open(item['path'])
paper, scheme = docs['paper'], docs['scheme']
reading = json.loads((READING / 'first-reading-frozen.json').read_text())
furniture = []


def page_raw(doc, number, kind):
    page = doc[number - 1]
    cut = page.rect.height - 15
    for block in page.get_text('dict')['blocks']:
        for line in block.get('lines', []):
            value = tidy(''.join(s['text'] for s in line['spans']))
            if line['bbox'][1] > page.rect.height * .82 and (
                re.fullmatch(r'\d{1,2}', value)
                or value.startswith('Leaving Certificate Vocational Programme')
                or value == 'Link Modules Examination'
            ):
                cut = min(cut, line['bbox'][1] - 2)
                record = dict(kind=kind, page=number, text=value, box=list(line['bbox']))
                if record not in furniture:
                    furniture.append(record)
    return page.get_text(clip=fitz.Rect(0, 15, page.rect.width, cut), sort=True)


def ref(section, q, letter='', roman=''):
    return section + str(q) + (f'({letter})' if letter else '') + (f'({roman})' if roman else '')


def scheme_parts():
    text = '\n'.join(page_raw(scheme, n, 'scheme') for n in range(4, 20))
    sections = split_raw(text, r'^\s*Section ([ABC])\s+', list('ABC'))
    result = {}
    for section, value in sections.items():
        questions = split_raw(value, r'^\s*Q\.?\s*(\d+)\.?\s*',
                              [str(n) for n in range(1, {'A': 8, 'B': 3, 'C': 7}[section] + 1)])
        for q, block in questions.items():
            if section == 'A' or (section == 'B' and q == '1'):
                result[ref(section, q)] = block
            elif section == 'B':
                for roman, part in split_raw(block, r'^\s*\((i{1,3})\)\s*',
                                             ['i', 'ii'] if q == '2' else ['i', 'ii', 'iii']).items():
                    result[ref(section, q, roman=roman)] = part
            else:
                for letter, part in split_raw(block, r'^\s*\(([abcd])\)\s*', list('abcd')).items():
                    if q == '1' and letter == 'd':
                        for roman, sub in split_raw(part, r'^\s*\((i{1,2})\)\s*', ['i', 'ii']).items():
                            result[ref(section, q, letter, roman)] = sub
                    else:
                        result[ref(section, q, letter)] = part
    assert len(result) == 43
    return result


def question(item):
    section, q, letter, roman = re.fullmatch(r'([ABC])(\d+)(?:\(([abcd])\))?(?:\((i{1,3})\))?', item['ref']).groups()
    text = page_raw(paper, item['paperPages'][0], 'paper')
    if section in ['A', 'B']:
        text = re.split(r'^\s*Q\.\s*' + q + r'\s+', text, maxsplit=1, flags=re.M)[1]
        text = re.split(r'^\s*Q\.\s*\d+\s+', text, maxsplit=1, flags=re.M)[0]
    if letter:
        text = re.split(r'^\s*\(' + letter + r'\)\s*', text, maxsplit=1, flags=re.M)[1]
        text = re.split(r'^\s*\([abcd]\)\s*', text, maxsplit=1, flags=re.M)[0]
    if roman:
        text = re.split(r'\(' + roman + r'\)\s*', text, maxsplit=1)[1]
        text = re.split(r'\(i{1,3}\)\s*', text, maxsplit=1)[0]
    text = tidy(re.sub(r'\(?\s*\d+\s+marks?\s*\)?', '', text, flags=re.I))
    assert text and not re.search(r'Leaving Certificate|Office Use|Section [ABC]', text), (item['ref'], text)
    return text


raw = scheme_parts()
assert set(raw) == {i['ref'] for i in reading['items']}
records = []
for item in reading['items']:
    block = raw[item['ref']]
    mark = re.search(r'\b\d+\s+(?:marks?\b|x\s*\d+\s*m\b)', block, re.I)
    assert mark, (item['ref'], block)
    label = tidy(block[:mark.start()])
    if item['ref'] == 'C2(b)':
        assert label.startswith('(i)'); label = label[3:].strip()
    suffix = re.sub(r'[()]', '', item['ref']).lower()
    records.append(dict(id='lcvp-2023-cl-deferred-' + suffix, ref=item['ref'],
                        questionText=question(item), sourceSchemePrompt=label,
                        sourceSchemeBlock=block, paperPages=item['paperPages'],
                        schemePages=item['schemePhysicalPages'], proposedCardMarks=item['cardMarks'],
                        firstReaderHeadings=item['headingIds'], sourceDecision=item['readingNote']))
stems = {}
for q in range(1, 8):
    text = page_raw(paper, 16 + (q - 1) * 3, 'paper')
    text = re.split(r'^\s*Q\.\s*' + str(q) + r'\s+', text, maxsplit=1, flags=re.M)[1]
    text = text.split('(a)', 1)[0]
    stems[str(q)] = tidy(re.sub(r'\d+\s+marks?', '', text, flags=re.I))
case = page_raw(paper, 9, 'paper').split('Ballyfert', 1)[1]
assert 'Ballyfert is a small' in case and 'sustainable in the long term.' in case
result = dict(recordedAt=datetime.now(timezone.utc).isoformat(), status='Review-only; no lane writes.',
              sourceSha256={s['kind']: s['sha256'] for s in manifest['sources']},
              printedParts=43, numberedLeafLabels=42, proposedAsks=50, offeredMarks=235,
              examMaximum=160, sectionCStems=stems, caseStudy='Ballyfert\n\n' + tidy(case),
              pending='Six headings and two informed splits require a third reading; fresh R4 archive checks and video hosting remain outstanding.',
              records=records)
assert sum(len(r['proposedCardMarks']) for r in records) == 50
assert sum(sum(r['proposedCardMarks']) for r in records) == 235
(HERE / 'source-parts.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
(HERE / 'removed-source-furniture.json').write_text(json.dumps(furniture, ensure_ascii=False, indent=2) + '\n')
(HERE / 'source-preview.txt').write_text('\n\n'.join(r['ref'] + '\n' + r['questionText'] + '\nSCHEME\n' + r['sourceSchemeBlock'] for r in records))
print(json.dumps({k: v for k, v in result.items() if k not in ['records', 'caseStudy', 'sectionCStems']}, indent=2))
