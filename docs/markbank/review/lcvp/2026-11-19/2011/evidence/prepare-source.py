#!/usr/bin/env python3
"""Review-only LCVP 2011 original selectors, after both 64-page readings."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import re
import sys
import fitz

HERE = Path(__file__).resolve().parent
READING = HERE.parent / '2026-11-19-lcvp-2011-independent'
LANE = Path('/Users/alexlinehan/Documents/Nextstepuni-LCVP-Release-20261119')
sys.path.insert(0, str(LANE / 'scripts/markbank/authoring'))
from lcvp_review_2026 import tidy
from lcvp_review_2024 import split_raw
from lcvp_review_2017 import header_body

manifest = json.loads((READING / 'source-manifest.json').read_text())
sources = {}
for source in manifest['sources']:
    path = Path(source['path'])
    assert hashlib.sha256(path.read_bytes()).hexdigest() == source['sha256']
    sources[source['kind']] = fitz.open(path)
paper, scheme = sources['paper'], sources['scheme']
reading = json.loads((READING / 'first-reading-frozen.json').read_text())
prompts = {}
removed_furniture = {}
removed_scheme_footers = {}
questionnaire_repairs = {}


def page_raw(doc, number):
    page = doc[number - 1]
    found = []
    for block in page.get_text('dict')['blocks']:
        for line in block.get('lines', []):
            value = tidy(''.join(span['text'] for span in line['spans']))
            box = fitz.Rect(line['bbox'])
            if value == str(number - 2) and 745 < box.y0 < 747 and 290 < box.x0 < 296:
                found.append(box)
    assert len(found) == 1, (number, found)
    removed_scheme_footers[str(number)] = {'text': str(number - 2), 'box': list(found[0])}
    text = page.get_text(clip=fitz.Rect(0, 15, page.rect.width, found[0].y0 - 2), sort=True)
    if number == 21:
        # The original PDF's glyph401 visibly prints an empty checkbox.
        # Its text mapping says Ƒ; use only these eleven verified glyphs.
        traces = page.get_texttrace()
        checks = [dict(font=s['font'], glyphId=c[1], origin=list(c[2]), box=list(c[3]))
                  for s in traces for c in s['chars']
                  if s['font'] == 'TimesNewRomanPSMT' and c[1] == 401]
        assert len(checks) == text.count('Ƒ') == 11
        text = text.replace('Ƒ', '□')
        # The PDF paints an opaque white questionnaire box over an obsolete
        # Male/female text fragment before drawing the visible model. Exclude
        # exactly that occluded fragment, not either visible answer option.
        hidden = [s for s in traces if tidy(''.join(chr(c[0]) for c in s['chars'])) == 'Male female']
        covers = [d for d in page.get_drawings() if d.get('seqno') == 1 and d.get('fill') == (1, 1, 1) and d.get('fill_opacity') == 1]
        assert len(hidden) == len(covers) == 1 and hidden[0]['seqno'] == 0
        assert covers[0]['rect'].contains(fitz.Rect(hidden[0]['bbox']))
        text, removed = re.subn(r'^\s*Male\s+female\s*$', '', text, flags=re.M)
        assert removed == 1
        questionnaire_repairs.update(page=21, checkboxGlyphs=checks,
            replacement={'extracted': 'Ƒ', 'visible': '□'}, hiddenText='Male female',
            hiddenTextBox=list(hidden[0]['bbox']), hiddenTextSeqno=0,
            opaqueCoverBox=list(covers[0]['rect']), opaqueCoverSeqno=1,
            originalImageRead='original-pages/scheme-21.png',
            reason='Rendered original shows eleven empty checkboxes and no duplicate Male/female line.')
    return text


def paper_raw(doc, number):
    page = doc[number - 1]
    lines, removed = [], []
    for block in page.get_text('dict')['blocks']:
        for line in block.get('lines', []):
            kept = []
            for span in line['spans']:
                value, box = tidy(span['text']), fitz.Rect(span['bbox'])
                office = value in ['Office Use', 'Only', '1', '2'] and box.x0 > 520 and box.y1 < 130
                footer = re.fullmatch(r'Page \d+ of 32', value) and box.y0 > 800
                if office or footer:
                    removed.append({'text': span['text'], 'box': list(span['bbox'])})
                else:
                    kept.append(span['text'])
            if tidy(''.join(kept)):
                lines.append((line['bbox'][1], line['bbox'][0], tidy(''.join(kept))))
    removed_furniture[str(number)] = removed
    return '\n'.join(value for _, _, value in sorted(lines))


def ref(section, q, letter=None, roman=None):
    return section + str(q) + (f'({letter})' if letter else '') + (f'({roman})' if roman else '')


def clean_prompt(value):
    return tidy(re.sub(r'\b\d+\s+[Mm]arks?\b', '', value))


def scheme_parts():
    text = '\n'.join(page_raw(scheme, n) for n in range(5, 25))
    text = re.sub(r'^\s*Part [123]\s*$', '', text, flags=re.M)
    sections = split_raw(text, r'^\s*Section ([ABC])\s+', list('ABC'))
    out = {}
    for section, text in sections.items():
        if section == 'C':
            # C5's model questionnaire contains Q1–Q6; those are answer
            # content, not new exam questions. Bound the six actual questions
            # by the original pages already read in both independent passes.
            page_groups = {1: [11, 12], 2: [13, 14], 3: [15, 16, 17],
                           4: [18, 19], 5: [20, 21, 22], 6: [23, 24]}
            qs = {}
            for q, numbers in page_groups.items():
                block = '\n'.join(page_raw(scheme, n) for n in numbers)
                qs[str(q)] = re.split(r'^\s*Q\.?\s*' + str(q) + r'\s+', block, maxsplit=1, flags=re.M)[1]
        else:
            qs = split_raw(text, r'^\s*Q\.?\s*(\d+)\s*',
                           [str(n) for n in range(1, {'A': 8, 'B': 3}[section] + 1)])
        for number, block in qs.items():
            q = int(number)
            if section == 'A' or (section == 'B' and q == 1):
                out[ref(section, q)] = block
                prompts[ref(section, q)] = clean_prompt(header_body(block)[0])
            elif section == 'B':
                header, answers = header_body(block)
                wanted = ['i', 'ii'] if q == 2 else ['i', 'ii', 'iii']
                for roman, text in split_raw(header, r'^\s*\((i{1,3})\)\s*', wanted).items():
                    prompts[ref(section, q, roman=roman)] = clean_prompt(text)
                if q == 2:
                    # The first answer pool is not preceded by an (i) label
                    # in the scheme. The paper and scheme heading name it (i).
                    found = list(re.finditer(r'^\s*\(ii\)\s*', answers, re.M))
                    assert len(found) == 1
                    parts = {'i': answers[:found[0].start()], 'ii': answers[found[0].end():]}
                else:
                    parts = split_raw(answers, r'^\s*\((i{1,3})\)\s*', wanted)
                for roman, text in parts.items():
                    out[ref(section, q, roman=roman)] = text
            else:
                for letter, part in split_raw(block, r'^\s*\(([abcd])\)\s*', list('abcd')).items():
                    if (q, letter) == (2, 'd'):
                        header, answers = header_body(part)
                        for roman, text in split_raw(header, r'^\s*\((i{1,2})\)\s*', ['i', 'ii']).items():
                            prompts[ref(section, q, letter, roman)] = clean_prompt(text)
                        for roman, text in split_raw(answers, r'^\s*\((i{1,2})\)\s*', ['i', 'ii']).items():
                            out[ref(section, q, letter, roman)] = text
                    else:
                        out[ref(section, q, letter)] = part
                        prompts[ref(section, q, letter)] = clean_prompt(header_body(part)[0])
    assert len(out) == 39
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
    assert value and not re.search(r'Office|Page \d+|Section [ABC]|\b1 2\b', value), (item['ref'], value)
    return value


raw = scheme_parts()
assert set(raw) == set(prompts) == {i['ref'] for i in reading['items']}
records = []
for item in reading['items']:
    section, q, letter, roman = parse_ref(item['ref'])
    identifier = 'lcvp-2011-cl-' + section.lower() + str(q) + (letter or '') + (roman or '')
    records.append(dict(id=identifier, ref=item['ref'], questionText=question(item),
                        paperPages=item['paperPages'], schemePages=item['schemePhysicalPages'],
                        sourceSchemeBlock=raw[item['ref']], sourceSchemePrompt=prompts[item['ref']],
                        proposedCardMarks=item['cardMarks'], firstReaderHeadings=item['headingIds'],
                        sourceDecision=item['readingNote']))
assert len(records) == 39
assert sum(len(r['proposedCardMarks']) for r in records) == 47
assert sum(sum(r['proposedCardMarks']) for r in records) == 210
stems = {}
for q, number in [(1, 14), (2, 17), (3, 20), (4, 23), (5, 26), (6, 29)]:
    value = re.split(r'^\s*Q\.\s*' + str(q) + r'\s+', paper_raw(paper, number), maxsplit=1, flags=re.M)[1]
    stems[str(q)] = tidy(value.split('(a)', 1)[0])
    assert not re.search(r'Office|\b1 2\b', stems[str(q)])
payload = dict(recordedAt=datetime.now(timezone.utc).isoformat(), status='Source preparation only; no production writes.',
               sourceSha256={s['kind']: s['sha256'] for s in manifest['sources']},
               printedParts=39, proposedAsks=47, offeredMarks=210, candidateMaximum=160,
               pending='Ten ask headings need third reading. C2(d)(ii) generic split consistency and fresh R4 archive recheck remain pending.',
               sectionCStems=stems, records=records)
(HERE / 'removed-page-furniture.json').write_text(json.dumps(removed_furniture, indent=2) + '\n')
(HERE / 'removed-scheme-footers.json').write_text(json.dumps(removed_scheme_footers, indent=2) + '\n')
(HERE / 'questionnaire-glyph-and-paint-proof.json').write_text(json.dumps(questionnaire_repairs, ensure_ascii=False, indent=2) + '\n')
(HERE / 'source-parts.json').write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({k: v for k, v in payload.items() if k != 'records'}, ensure_ascii=False))
for r in records:
    print(r['ref'], r['proposedCardMarks'], r['questionText'])
