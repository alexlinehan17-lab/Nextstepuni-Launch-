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
"""Paper-only Atlas anchors and topic tags for Art's carded deferred sittings.

Paper Trail indexes each deferred History and Appreciation paper as its own file ("LC014ALP000EV-deferred.pdf"),
numbered as June's. A sitting is written here once Mark Bank holds its cards (art_cards.py DEFERRED_SITTINGS; the
cards carry "sitting": "deferred"), and then:

  * its anchor map, public/paper-anchors/<year>/<fileid>.json: paper only, mode "pagejump", one entry per printed
    question, from each question's printed head ("N." on the 2021-2022 papers, "Question N" from 2023) to the next
    on the same or the following page, else (a section's last question, its answer pages after it) to the foot of
    its own page;
  * its topic-tag paper in topic-tags/tags/art.json, after June's (then build-tags.mjs), each printed question tagged
    with the topics its cards are filed under (reviewed in art_cards.py), first two in card order.

The Topic Atlas reads the question's exam topics from the runtime's deferredQuestionMappings
(build-art-exam-topic-crosswalk.mjs), keyed by this file id, never June's question of the same number.

    python3 scripts/paper-trail/art_deferred.py           # write
    python3 scripts/paper-trail/art_deferred.py --check   # compare
"""
import argparse
import json
import re
import sys
from pathlib import Path

import fitz

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
OUT = ROOT / 'public' / 'paper-anchors'
TAGS = HERE / 'topic-tags' / 'tags' / 'art.json'
AUTHORED = ROOT / 'components' / 'MarkBank' / 'cards' / 'art' / 'authored.json'
PAPERS = ROOT / 'examiner-reports' / 'art' / 'papers'
SHORT = {'higher': 'hl', 'ordinary': 'ol'}
COPYRIGHT = '© State Examinations Commission'
# The running header and footer each page prints (matched by text, never by position), and blank lines.
FURNITURE = re.compile(r'|\d{1,2}|Leaving Certificate Examination(?: \d{4})?(?: \d{1,2})?'
                       r'|Art\s*[–-]\s*(?:History and Appreciation|Visual Studies)\s*[–-]\s*(?:Higher|Ordinary) Level')


def deferred_papers():
    """(year, level, fileid, {question number: [topic ids in card order]}) for each carded deferred sitting."""
    cards = [c for c in json.loads(AUTHORED.read_text())['cards'] if c.get('sitting') == 'deferred']
    out = {}
    for card in cards:
        number = int(re.search(r'Q(\d+)', card['questionRef']).group(1))
        entry = out.setdefault((card['year'], card['level']), {'fileid': card['paperFileid'] + '.pdf', 'q': {}})
        assert entry['fileid'] == card['paperFileid'] + '.pdf', card['id']
        topics = entry['q'].setdefault(number, [])
        if card['topicId'] not in topics:
            topics.append(card['topicId'])
    return [(year, level, entry['fileid'], entry['q']) for (year, level), entry in sorted(out.items())]


def heads(year, level):
    """Each printed question's head: {number: (page, y fraction)} -- the margin's "N." on the 2021-2022 papers, the
    word "Question" followed by N from 2023."""
    doc = fitz.open(PAPERS / f'{year}-{SHORT[level]}-deferred-paper.pdf')
    found = {}
    for page_number, page in enumerate(doc, start=1):
        words = page.get_text('words')
        for index, word in enumerate(words):
            if word[0] / page.rect.width >= 0.2:
                continue
            if year <= 2022:
                m = re.fullmatch(r'(\d{1,2})\.', word[4])
            else:
                following = words[index + 1][4] if index + 1 < len(words) else ''
                m = re.fullmatch(r'(\d{1,2})', following) if word[4] == 'Question' else None
            if m:
                found.setdefault(int(m.group(1)), (page_number, round(word[1] / page.rect.height, 4)))
    return found, doc


def foot(doc, page_number):
    """The foot of the last printed line on a page, its running header and footer aside (matched by text)."""
    page = doc[page_number - 1]
    lines = [line for block in page.get_text('dict')['blocks'] for line in block.get('lines', [])
             if not FURNITURE.fullmatch(' '.join(span['text'] for span in line['spans']).replace('\xa0', ' ').strip())]
    bottom = max((line['bbox'][3] for line in lines), default=0.92 * page.rect.height)
    return page_number, round(min(1, bottom / page.rect.height + 0.01), 4)


def anchor_map(year, level, fileid, numbers):
    found, doc = heads(year, level)
    if sorted(found) != numbers:
        raise SystemExit(f'{year} {level} deferred: heads {sorted(found)}, cards {numbers}')
    positions = [found[n] for n in numbers]
    if any(b <= a for a, b in zip(positions, positions[1:])):
        raise SystemExit(f'{year} {level} deferred: heads out of order')
    questions = []
    for index, n in enumerate(numbers):
        # To the next question's head when it is on this page or the next; otherwise (the last question of a
        # section, whose answer pages follow, and the paper's last question) to the foot of its own page.
        following = positions[index + 1] if index + 1 < len(numbers) else None
        end = following if following and following[0] <= positions[index][0] + 1 \
            else foot(doc, positions[index][0])
        questions.append({'n': str(n), 'pP': positions[index][0], 'pY': [positions[index][1], 1],
                          'region': [{'p': 1}], 'mode': 'pagejump', 'conf': 0.5, 'label': f'Question {n}',
                          'printOrder': index + 1, 'endP': end[0], 'endY': end[1]})
    span = max(q['endP'] - q['pP'] for q in questions)
    return {'v': 1, 'paperFileid': fileid, 'schemeFileid': '', 'component': '000', 'band': [1, 1],
            'copyright': COPYRIGHT, 'paperOnly': 1, **({'maxCropPages': span} if span > 3 else {}), 'q': questions}


def tag_papers():
    papers = []
    for year, level, fileid, questions in deferred_papers():
        entries = [{'n': str(n), 'primary': topics[0], **({'secondary': topics[1]} if len(topics) > 1 else {})}
                   for n, topics in sorted(questions.items())]
        papers.append({'subjectId': 'art', 'level': level, 'lang': 'ev', 'year': year, 'fileid': fileid,
                       'paperKey': 'single', 'q': entries})
    return papers


def tags_text():
    june = [p for p in json.loads(TAGS.read_text()) if not p['fileid'].endswith('-deferred.pdf')]
    return json.dumps(june + tag_papers(), indent=1, ensure_ascii=False) + '\n'


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--check', action='store_true')
    args = ap.parse_args()
    stale = []
    for year, level, fileid, questions in deferred_papers():
        path = OUT / str(year) / f'{fileid}.json'
        text = json.dumps(anchor_map(year, level, fileid, sorted(questions)), ensure_ascii=False,
                          separators=(',', ':')) + '\n'
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
