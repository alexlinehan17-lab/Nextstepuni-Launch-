#!/usr/bin/env python3
# Copyright 2026 Nextstepuni
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Paper-only Atlas anchors and Paper Trail topic tags for Geography's carded deferred sittings.

Paper Trail indexes each deferred booklet as its own paper ("LC005ALP042EV-deferred.pdf", Part One and
Answerbook; "LC005ALP043EV-deferred.pdf", Part Two), numbered as June's. The Topic Atlas lists a carded
deferred sitting's printed questions under those file ids (geography_cards.py writes their rows into
data/examTopics/geography-reviewed-question-runtime.json from the sitting's review ledger). This writes
the anchor maps those questions open from: paper only, mode "pagejump", one entry per printed question
(Part One Questions 1-12; Part Two Questions 1-12 and the option essays 13-24), each at its printed
heading and running to the next.

The same booklets are written into the Paper Trail topic tags (topic-tags/tags/geography.json, then
build-tags.mjs): each printed question is tagged with the outgoing-curriculum nodes ("geography-x-y")
its reviewed cards are filed under, ordered by the marks they carry (a routed task's marks shared
between its routes), the first as primary and the second, if any, as secondary.

A sitting is written once geography_cards.py carries it (REVIEWED_DEFERRED).

    python3 scripts/paper-trail/geography_deferred.py           # write
    python3 scripts/paper-trail/geography_deferred.py --check   # compare
"""
import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

import fitz

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
CORPUS = ROOT / 'paper-trail-corpus' / 'deferredexams'
OUT = ROOT / 'public' / 'paper-anchors'
TAGS = HERE / 'topic-tags' / 'tags' / 'geography.json'
CARDS = ROOT / 'components' / 'MarkBank' / 'cards' / 'geography' / 'authored.json'
COPYRIGHT = '© State Examinations Commission'


def deferred_cards():
    cards = json.loads(CARDS.read_text())['cards']
    return [card for card in cards if card['paperFileid'].endswith('-deferred')]


def sittings():
    return sorted({(card['year'], card['level']) for card in deferred_cards()})


def is_bold(line):
    return any('Bold' in span.get('font', '') for span in line['spans'][:1])


def heading_lines(doc, pattern, first_page, last_page):
    """(number, page, y) of every bold printed heading matching ``pattern`` (group 1 = number)."""
    found = []
    for index in range(first_page - 1, last_page):
        page = doc[index]
        for block in page.get_text('dict')['blocks']:
            for line in block.get('lines', ()):
                text = ''.join(span['text'] for span in line['spans']).strip()
                match = re.match(pattern, text)
                if match and is_bold(line):
                    found.append((int(match.group(1)), index + 1,
                                  round(line['bbox'][1] / page.rect.height, 4)))
    return found


def anchors(doc, numbers, labels):
    """One pagejump anchor per printed question, in print order, each ending at the next."""
    starts = {}
    for number, page, y in numbers:
        starts.setdefault(number, (page, y))
    expected = list(labels)
    if sorted(starts) != expected:
        raise SystemExit(f'{doc.name}: printed questions {sorted(starts)} != {expected}')
    order = sorted(expected, key=lambda n: starts[n])
    out = []
    for index, number in enumerate(order):
        page, y = starts[number]
        entry = {'n': str(number), 'pP': page, 'pY': [y, 1], 'region': [{'p': 1}], 'mode': 'pagejump',
                 'conf': 0.5, 'label': labels[number], 'printOrder': index + 1}
        if index + 1 < len(order):
            end_page, end_y = starts[order[index + 1]]
            entry.update({'endP': end_page, 'endY': end_y})
        out.append(entry)
    return out


def maps():
    out = {}
    for year, level in sittings():
        letter = 'A' if level == 'higher' else 'G'
        part_one = fitz.open(CORPUS / str(year) / f'LC005{letter}LP042EV.pdf')
        part_two = fitz.open(CORPUS / str(year) / f'LC005{letter}LP043EV.pdf')
        # Part One's questions run from page 3 to page 12 or 13 (2023 prints Q12 on p13); the answerbook follows.
        one = anchors(part_one, heading_lines(part_one, r'^(1[0-2]|[1-9])\.(?:\s|$)', 3, 14),
                      {n: f'Part One · Question {n}' for n in range(1, 13)})
        two_numbers = heading_lines(part_two, r'^Question\s+(1[0-2]|[1-9])$', 3, len(part_two))
        two_numbers += [hit for hit in heading_lines(part_two, r'^(1[3-9]|2[0-4])\.(?:\s|$)', 3, len(part_two))]
        two = anchors(part_two, two_numbers,
                      {n: (f'Question {n}' if n <= 12 else f'Option essay · Q{n}') for n in range(1, 25)})
        for component, raw, entries in (('042', f'LC005{letter}LP042EV', one), ('043', f'LC005{letter}LP043EV', two)):
            fileid = f'{raw}-deferred.pdf'
            out[OUT / str(year) / f'{fileid}.json'] = {
                'v': 1, 'paperFileid': fileid, 'schemeFileid': '', 'component': component, 'band': [1, 1],
                'copyright': COPYRIGHT, 'paperOnly': 1, 'q': entries}
    return out


def tag_papers():
    """The carded deferred booklets as topic-tag papers, in year, level, booklet order."""
    cards = deferred_cards()
    shares = Counter(card['questionRef'].split(' · ')[0].replace(' — Deferred sitting', '') for card in cards)
    weights = defaultdict(lambda: defaultdict(float))
    for card in cards:
        base = card['questionRef'].split(' · ')[0].replace(' — Deferred sitting', '')
        number = re.search(r' Q(\d+)', base).group(1)
        weights[(card['year'], card['level'], card['paperFileid'], number)][card['topicId']] += (
            card['totalMarks'] / shares[base])
    papers = []
    for year, level in sittings():
        letter = 'A' if level == 'higher' else 'G'
        for part, key in (('042', 'p1'), ('043', 'p2')):
            fileid = f'LC005{letter}LP{part}EV-deferred'
            entries = []
            for number in range(1, 13 if part == '042' else 25):
                topics = weights[(year, level, fileid, str(number))]
                if not topics:
                    raise SystemExit(f'{year} {level} {fileid} Q{number}: no carded topic to tag')
                ranked = sorted(topics, key=lambda topic: (-topics[topic], topic))
                entries.append({'n': str(number), 'primary': ranked[0],
                                **({'secondary': ranked[1]} if len(ranked) > 1 else {})})
            papers.append({'subjectId': 'geography', 'level': level, 'lang': 'ev', 'year': year,
                           'fileid': f'{fileid}.pdf', 'paperKey': key, 'q': entries})
    return papers


def tags_text():
    june = [p for p in json.loads(TAGS.read_text()) if not p['fileid'].endswith('-deferred.pdf')]
    return json.dumps(june + tag_papers(), indent=1, ensure_ascii=False) + '\n'


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--check', action='store_true')
    args = ap.parse_args()
    stale = []
    for path, hosted in maps().items():
        text = json.dumps(hosted, ensure_ascii=False, separators=(',', ':')) + '\n'
        if args.check:
            if not path.exists() or path.read_text() != text:
                stale.append(str(path.relative_to(ROOT)))
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
        print('wrote', path.relative_to(ROOT))
    text = tags_text()
    if args.check:
        if TAGS.read_text() != text:
            stale.append(str(TAGS.relative_to(ROOT)))
    elif TAGS.read_text() != text:
        TAGS.write_text(text)
        print('wrote', TAGS.relative_to(ROOT))
    if stale:
        print('stale: ' + ', '.join(stale), file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
