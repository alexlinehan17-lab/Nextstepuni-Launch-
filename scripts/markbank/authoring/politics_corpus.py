#!/usr/bin/env python3
"""Paper-first Politics and Society audit. Draft extraction is NOT a completion gate.

The inventory is taken from Paper Trail, not from a year window. Every source is
hashed. Coordinates retain the original PDF boundaries for visual review; the
paper and scheme are scanned independently. No draft is shipped automatically.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import unicodedata

import fitz

ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / 'examiner-reports/politics-society'
OUT = ROOT / 'tmp/politics-audit'
sys.path.insert(0, str(ROOT / 'scripts/markbank'))
from markbank_text import unligature


def clean(text):
    # Embedded Calibri encodings in the papers use these glyphs for ligatures.
    return re.sub(r'\s+', ' ', unicodedata.normalize('NFKC', unligature(text))).strip()


def lines(page, number, paper):
    result = []
    for block in page.get_text('dict')['blocks']:
        for line in block.get('lines', []):
            spans = [s for s in line['spans'] if s['text'].strip()]
            if not spans:
                continue
            text = clean(''.join(s['text'] for s in line['spans']))
            x0, y0, x1, y1 = line['bbox']
            if y0 > page.rect.height * .92:
                continue
            # White-on-white remnants are present in the actual 2026 HL PDF
            # (an unrelated energy-tax chart behind Q1(g)). They are invisible
            # in the rendered paper and must not become question wording.
            if all(s.get('color') == 0xffffff for s in spans):
                continue
            if re.match(r'^(Leaving Certificate|Politics and Society|Higher Level|Ordinary Level)', text):
                continue
            if re.fullmatch(r'\d+', text) and (y0 < 40 or y0 > page.rect.height * .88):
                continue
            result.append({'p': number, 'x': round(x0, 2), 'y': round(y0, 2),
                           'bottom': round(y1, 2), 'baseline': round(max(s['origin'][1] for s in spans), 2), 'text': text})
    # Glyph bounding boxes vary within one printed row (notably the tick glyph
    # on 2018 OL Q1(t)). Order by the text baseline, then left-to-right, so the
    # label precedes its ask even when a symbol extends slightly above it.
    rows = []
    for line in sorted(result, key=lambda item: (item['baseline'], item['x'])):
        if rows and abs(line['baseline'] - rows[-1][0]['baseline']) <= 1.5:
            rows[-1].append(line)
        else:
            rows.append([line])
    return [line for row in rows for line in sorted(row, key=lambda item: item['x'])]


def scan(path, paper):
    doc = fitz.open(path)
    entries = [line for n, page in enumerate(doc, 1)
               if (n >= 3 if paper else n >= 4)
               for line in lines(page, n, paper)]
    units, sources, active = [], [], None
    section, question, letter = 'A', 1, None
    source_start = None

    def end():
        nonlocal active
        if active:
            active['text'] = '\n'.join(row['text'] for row in active['lines']).strip()
            active['pages'] = sorted({row['p'] for row in active['lines']} | {active['p']})
            units.append(active)
            active = None

    def start(line, q, part='', roman=''):
        nonlocal active
        end()
        active = {'key': f'{q}{"(" + part + ")" if part else ""}{"(" + roman + ")" if roman else ""}',
                  'section': section, 'q': q, 'part': part, 'roman': roman,
                  'p': line['p'], 'y': line['y'], 'lines': []}

    for line in entries:
        t, x = line['text'], line['x']
        section_match = re.match(r'^Section\s+([ABC])\b', t, re.I)
        if section_match:
            next_section = section_match[1].upper()
            if paper and next_section == 'C' and re.search(r'Answer to Question', t):
                end()
                break
            if not paper and next_section == 'C':
                end()
                break  # Essay criteria are reviewed independently, not Q1 letters.
            if next_section != section:
                end()
                section = next_section
                if section == 'B':
                    question, letter = 2, None
                    source_start = line['p']
                elif section == 'C':
                    source_start = None
            continue
        if paper and section == 'B' and active is None and re.match(r'^Document\s+[AB]\b', t):
            end()
            sources.append({'p': line['p'], 'label': t})
            continue
        qmatch = re.match(r'^Question\s*(\d+)(?:\s*\(\s*([ab])\s*\))?', t, re.I)
        if qmatch:
            end()
            question, letter = int(qmatch[1]), None
            source_start = None
            if section == 'C':
                start(line, question, qmatch[2] or '')
            continue
        # Top-level paper parts share the left margin. Scheme romans sometimes
        # share that margin too, so (i) is a roman only immediately before (ii).
        marker = re.match(r'^\(\s*([a-z]+)\s*\)\s*(?:\(\s*([ivx]+)\s*\))?', t)
        if marker and section != 'C':
            token = marker[1]
            is_roman = len(token) > 1 or (paper and x > 75)
            if not paper and token == 'i' and letter and not marker[2]:
                # Explicitly repeated parent, e.g. (b)(i), is handled below;
                # a bare (i) followed by (ii) within a group is a nested ask.
                pos = entries.index(line)
                nxt = next((re.match(r'^\(\s*([a-z]+)\s*\)', other['text'])
                            for other in entries[pos+1:]
                            if re.match(r'^\(\s*([a-z]+)\s*\)', other['text'])), None)
                is_roman = bool(nxt and nxt[1] == 'ii')
            if is_roman:
                if letter:
                    start(line, question, letter, token)
            elif x < (90 if paper else 110):
                letter = token
                start(line, question, token, marker[2] or '')
            if active:
                remainder = t[marker.end():].strip()
                if remainder:
                    active['lines'].append({**line, 'text': remainder})
                continue
        if active:
            if t != 'OR':
                active['lines'].append(line)
    end()
    # Parent stems are context, not separately marked tasks when subparts exist.
    for unit in units:
        children = [u for u in units if u['q'] == unit['q'] and u['part'] == unit['part'] and u['roman']]
        if not unit['roman'] and children:
            for child in children:
                child['stem'] = unit['text']
                child['contextPages'] = unit['pages']
            unit['contextOnly'] = True
        if unit['section'] == 'C' and not unit['part'] and any(
                other['q'] == unit['q'] and other['part'] for other in units):
            unit['contextOnly'] = True
    return {'pages': len(doc), 'units': units, 'sources': sources}


def inventory():
    data = subprocess.check_output([
        'node', '--input-type=module', '-e',
        "import {paperIndex} from './scripts/markbank/paperIndex.mjs';"
        "console.log(JSON.stringify(paperIndex['politics-and-society']))",
    ], cwd=ROOT, text=True)
    manifest = []
    for entry in json.loads(data):
        if entry['lang'] != 'ev':
            continue
        level = 'hl' if entry['level'] == 'higher' else 'ol'
        for paper in entry['papers']:
            item = {'year': entry['year'], 'level': entry['level'], 'lang': entry['lang'],
                    'label': paper['label'], 'paperFileid': paper['doc']['f']}
            for kind, key in [('papers', 'doc'), ('schemes', 'scheme')]:
                path = SOURCE / kind / f'{entry["year"]}-{level}{"-paper" if kind == "papers" else ""}.pdf'
                assert path.exists(), f'Missing indexed {kind}: {path}'
                raw = path.read_bytes()
                assert raw.startswith(b'%PDF'), path
                assert len(raw) == paper[key]['b'], f'Index byte-size mismatch: {path}'
                item[kind] = {'path': str(path.relative_to(ROOT)), 'sha256': hashlib.sha256(raw).hexdigest(),
                              'bytes': len(raw), 'pages': len(fitz.open(path)), 'fileid': paper[key]['f']}
            manifest.append(item)
    return sorted(manifest, key=lambda x: (x['year'], x['level']))


def essay_criteria(path):
    """Read the six-column/five-column SEC grid by cell coordinates.

    Flat text interleaves adjacent grades. Keep each printed column separate,
    and reject a grid unless its marks cover every permitted score once.
    """
    doc = fitz.open(path)
    pages = [(i + 1, page) for i, page in enumerate(doc)
             if all(word in page.get_text() for word in ['Introduction', 'Knowledge', 'Cohesion'])]
    assert len(pages) == 1, f'{path}: missing or ambiguous essay grid'
    number, page = pages[0]
    raw_lines = []
    for block in page.get_text('dict')['blocks']:
        for line in block.get('lines', []):
            # Some older files rotate an already-landscape page; others encode
            # vertical text and rotate the page back. Normalise reading direction.
            matrix = page.rotation_matrix if abs(line['dir'][0]) < .5 else fitz.Matrix(1, 1)
            box = fitz.Rect(line['bbox']) * matrix
            baseline = (fitz.Point(line['spans'][0]['origin']) * matrix).y
            raw_lines.append((clean(''.join(s['text'] for s in line['spans'])), box, baseline))
    headings = sorted([(text, box, baseline) for text, box, baseline in raw_lines
                       if text in ['Excellent', 'Very good', 'Good', 'Fair', 'Weak'] and box.y0 < 100],
                      key=lambda pair: pair[1].x0)
    assert len(headings) in [4, 5], f'{path}: unexpected grade columns'
    marks = sorted([(int(re.match(r'\d+', text)[0]), box, baseline) for text, box, baseline in raw_lines
                    if re.fullmatch(r'\d+ marks', text) and box.x0 < headings[0][1].x0],
                   key=lambda pair: pair[1].y0)
    assert len(marks) == 6, f'{path}: unexpected essay components'
    centres = [(box.x0 + box.x1) / 2 for _, box, _ in headings]
    # The printed cells are equal-width grade columns.
    spacing = centres[1] - centres[0]
    boundaries = [centres[0] - spacing / 2] + [(a + b) / 2 for a, b in zip(centres, centres[1:])] + [centres[-1] + spacing / 2]
    names = ['Introduction', 'Knowledge', 'Evidence', 'Analysis and Synthesis', 'Evaluation', 'Cohesion']
    ids = ['introduction', 'knowledge', 'evidence', 'analysis', 'evaluation', 'cohesion']
    result = []
    top = max(baseline for _, _, baseline in headings)
    for index, (maximum, mark_box, mark_baseline) in enumerate(marks):
        bands = []
        for col, (label, _, _) in enumerate(headings):
            x0, x1 = boundaries[col:col+2]
            cell = sorted([(baseline, box.x0, text) for text, box, baseline in raw_lines
                           if x0 <= (box.x0 + box.x1)/2 < x1 and top < baseline <= mark_baseline + 2])
            wording = clean(' '.join(text for baseline, _, text in cell if baseline < mark_baseline - 2))
            notation = clean(' '.join(text for baseline, _, text in cell if abs(baseline - mark_baseline) <= 2))
            match = re.fullmatch(r'(\d+)\s*(?:[-–]\s*(\d+))?', notation)
            assert match, f'{path}: bad {names[index]}/{label} mark range {notation!r}'
            low, high = int(match[1]), int(match[2] or match[1])
            assert wording, f'{path}: empty essay descriptor'
            bands.append({'label': label, 'marks': list(range(low, high+1)), 'guidance': wording})
        assert sorted(mark for band in bands for mark in band['marks']) == list(range(maximum+1)), path
        result.append({'id': ids[index], 'label': names[index], 'maxMarks': maximum,
                       'permittedMarks': list(range(maximum+1)), 'guidance': [], 'bands': bands})
        top = mark_baseline + 2
    return {'page': number, 'criteria': result}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    manifest = inventory()
    (OUT / 'source-inventory.json').write_text(json.dumps(manifest, indent=2) + '\n')
    drafts = []
    for source in manifest:
        paper = scan(ROOT / source['papers']['path'], True)
        scheme = scan(ROOT / source['schemes']['path'], False)
        essay = essay_criteria(ROOT / source['schemes']['path'])
        assert sum(c['maxMarks'] for c in essay['criteria']) == (100 if source['level'] == 'higher' else 50)
        drafts.append({'source': source, 'paper': paper, 'scheme': scheme, 'essay': essay})
        print(source['year'], source['level'], 'paper tasks', len([u for u in paper['units'] if not u.get('contextOnly')]),
              'scheme blocks', len([u for u in scheme['units'] if not u.get('contextOnly')]))
    (OUT / 'draft-extraction.json').write_text(json.dumps(drafts, ensure_ascii=False, indent=2) + '\n')
    # Every finite-looking directive remains visible for human classification.
    directives = []
    for draft in drafts:
        for unit in draft['paper']['units']:
            if re.search(r'\b(choose|any|either|one of|two of|three of|and/or)\b', unit['text'], re.I):
                directives.append({'year': draft['source']['year'], 'level': draft['source']['level'],
                                   'key': unit['key'], 'text': unit['text']})
    (OUT / 'selection-directives.json').write_text(json.dumps(directives, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    main()
