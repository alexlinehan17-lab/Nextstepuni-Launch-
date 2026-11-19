#!/usr/bin/env python3
"""Review-only original selectors; never writes the production lane."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import re
import sys
import fitz

HERE = Path(__file__).resolve().parent
READING = HERE.parent / '2026-11-19-lcvp-2012-independent'
LANE = Path('/Users/alexlinehan/Documents/Nextstepuni-LCVP-Release-20261119')
sys.path.insert(0, str(LANE / 'scripts/markbank/authoring'))
from lcvp_review_2026 import tidy
from lcvp_review_2024 import split_raw
from lcvp_review_2017 import paper_raw, header_body

manifest = json.loads((READING / 'source-manifest.json').read_text())
sources = {}
for source in manifest['sources']:
    path = Path(source['path'])
    assert hashlib.sha256(path.read_bytes()).hexdigest() == source['sha256']
    sources[source['kind']] = fitz.open(path)
paper, scheme = sources['paper'], sources['scheme']
reading = json.loads((READING / 'first-reading-frozen.json').read_text())
scheme_prompts = {}
scheme_furniture = {}


def page_raw(doc, number):
    page = doc[number - 1]
    footers = []
    for block in page.get_text('dict')['blocks']:
        for line in block.get('lines', []):
            value = tidy(''.join(span['text'] for span in line['spans']))
            box = fitz.Rect(line['bbox'])
            if value == str(number - 2) and 740 < box.y0 < 745 and 295 < box.x0 < 302:
                footers.append(box)
    assert len(footers) == 1, (number, footers)
    scheme_furniture[str(number)] = {'footer': str(number - 2), 'box': list(footers[0])}
    return page.get_text(clip=fitz.Rect(0, 15, page.rect.width, footers[0].y0 - 2), sort=True)


def prompt(value):
    return tidy(re.sub(r'\b\d+\s+[Mm]arks?\b', '', value))


def ref(section, q, letter=None, roman=None):
    return section + str(q) + (f'({letter})' if letter else '') + (f'({roman})' if roman else '')


def scheme_parts():
    source_text = '\n'.join(page_raw(scheme, n) for n in range(5, 19))
    source_text = re.sub(r'^\s*Part [123]\s*$', '', source_text, flags=re.M)
    sections = split_raw(source_text,
                         r'^\s*Section ([ABC])\s+', list('ABC'))
    out = {}
    for section, text in sections.items():
        qs = split_raw(text, r'^\s*Q\.?\s*(\d+)\s*',
                       [str(n) for n in range(1, {'A': 8, 'B': 3, 'C': 6}[section] + 1)])
        for number, body in qs.items():
            q = int(number)
            if section == 'A' or (section == 'B' and q == 1):
                out[ref(section, q)] = body
                scheme_prompts[ref(section, q)] = prompt(header_body(body)[0])
            elif section == 'B':
                header, answers = header_body(body)
                wanted = ['i', 'ii', 'iii'] if q == 2 else ['i', 'ii']
                for roman, text in split_raw(header, r'^\s*\((i{1,3})\)\s*', wanted).items():
                    scheme_prompts[ref(section, q, roman=roman)] = prompt(text)
                for roman, part in split_raw(answers, r'^\s*\((i{1,3})\)\s*',
                                             ['i', 'ii', 'iii'] if q == 2 else ['i', 'ii']).items():
                    out[ref(section, q, roman=roman)] = part
            else:
                for letter, part in split_raw(body, r'^\s*\(([abcd])\)\s*', list('abcd')).items():
                    if (q, letter) in [(1, 'b'), (5, 'd')]:
                        header, answers = header_body(part)
                        for roman, text in split_raw(header, r'^\s*\((i{1,2})\)\s*', ['i', 'ii']).items():
                            scheme_prompts[ref(section, q, letter, roman)] = prompt(text)
                        for roman, answer in split_raw(answers, r'^\s*\((i{1,2})\)\s*', ['i', 'ii']).items():
                            out[ref(section, q, letter, roman)] = answer
                    elif (q, letter) in [(3, 'd'), (4, 'd')]:
                        # Both printed question parts share one pool; preserve it
                        # on both source records, without claiming double credit.
                        header, _ = header_body(part)
                        for roman, text in split_raw(header, r'^\s*\((i{1,2})\)\s*', ['i', 'ii']).items():
                            scheme_prompts[ref(section, q, letter, roman)] = prompt(text)
                        for roman in ['i', 'ii']:
                            out[ref(section, q, letter, roman)] = part
                    else:
                        out[ref(section, q, letter)] = part
                        scheme_prompts[ref(section, q, letter)] = prompt(header_body(part)[0])
    assert len(out) == 42
    return out


def parse_ref(value):
    m = re.fullmatch(r'([ABC])(\d+)(?:\(([abcd])\))?(?:\((i{1,3})\))?', value)
    assert m, value
    return m[1], int(m[2]), m[3], m[4]


def question(item):
    section, q, letter, roman = parse_ref(item['ref'])
    value = paper_raw(paper, item['paperPages'][0])
    if section in ['A', 'B']:
        value = re.split(r'^\s*Q\.\s*' + str(q) + r'\s+', value, maxsplit=1, flags=re.M)[1]
        value = re.split(r'^\s*Q\.\s*\d+\s+', value, maxsplit=1, flags=re.M)[0]
    if letter:
        value = re.split(r'^\s*\(' + letter + r'\)\s*', value, maxsplit=1, flags=re.M)[1]
        if letter != 'd':
            following = 'abcd'['abcd'.index(letter) + 1]
            value = re.split(r'^\s*\(' + following + r'\)\s*', value, maxsplit=1, flags=re.M)[0]
    if roman:
        value = re.split(r'\(' + roman + r'\)\s*', value, maxsplit=1)[1]
        value = re.split(r'\(i{1,3}\)\s*', value, maxsplit=1)[0]
    value = tidy(re.sub(r'\b\d+\s+marks?\b', '', value, flags=re.I))
    assert value and not re.search(r'Office|Page \d+|Section [ABC]', value), (item['ref'], value)
    return value


raw = scheme_parts()
assert set(raw) == {i['ref'] for i in reading['items']}
records = []
for item in reading['items']:
    section, q, letter, roman = parse_ref(item['ref'])
    identifier = 'lcvp-2012-cl-' + section.lower() + str(q) + (letter or '') + (roman or '')
    records.append(dict(id=identifier, ref=item['ref'], questionText=question(item),
                        paperPages=item['paperPages'], schemePages=item['schemePhysicalPages'],
                        sourceSchemeBlock=raw[item['ref']], proposedCardMarks=item['proposedCardMarks'],
                        sourceSchemePrompt=scheme_prompts[item['ref']],
                        firstReaderHeading=item['headingId'], sourceDecision=item['readingNote']))
assert len(records) == 42
assert sum(len(r['proposedCardMarks']) for r in records) == 47
assert sum(sum(r['proposedCardMarks']) for r in records) == 210
payload = dict(recordedAt=datetime.now(timezone.utc).isoformat(), status='Source preparation only; no production writes.',
               sourceSha256={s['kind']: s['sha256'] for s in manifest['sources']},
               printedParts=42, proposedAsks=47, offeredMarks=210, candidateMaximum=160,
               pending='Five headings need third reading. Generic split consistency and fresh R4 archive recheck remain pending.',
               records=records)
(HERE / 'source-parts.json').write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n')
(HERE / 'removed-scheme-furniture.json').write_text(json.dumps(scheme_furniture, indent=2) + '\n')
print(json.dumps({k: v for k, v in payload.items() if k != 'records'}, ensure_ascii=False))
for r in records:
    print(r['ref'], r['proposedCardMarks'], r['questionText'])
