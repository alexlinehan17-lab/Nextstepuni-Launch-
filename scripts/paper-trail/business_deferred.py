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
"""Paper-only Atlas anchors and Paper Trail topic tags for Business's carded deferred sittings.

Paper Trail indexes each deferred booklet as its own paper ("LC033ALP032EV-deferred.pdf", Section 1 and
Answerbook; "LC033ALP041EV-deferred.pdf", Sections 2 and 3; at Ordinary "LC033GLP032EV-deferred.pdf" and
"LC033GLP033EV-deferred.pdf"), numbered as June's. The Topic Atlas lists a carded deferred sitting's printed
questions under those file ids (data/examTopics/business-deferred-question-topics.json, written with the cards
by scripts/markbank/authoring/business/add-<year>-<level>-deferred.py). This writes the anchor maps those
questions open from with the June reader's own geometry (business.py detected_anchors, paper_tail and
hosted_map): paper only, mode "pagejump", one entry per printed question.

The same booklets are written into the Paper Trail topic tags (topic-tags/tags/business.json, then
build-tags.mjs): each printed question is tagged with the curriculum nodes ("business-x-y") of the cards it
holds, ranked by the marks they carry (an additional topic at half its card's marks), the first as primary and
the second, if any, as secondary.

    python3 scripts/paper-trail/business_deferred.py           # write
    python3 scripts/paper-trail/business_deferred.py --check   # compare
"""
import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

import fitz

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import business as BUS  # noqa: E402

ROOT = HERE.parent.parent
CORPUS = ROOT / 'paper-trail-corpus' / 'deferredexams'
OUT = ROOT / 'public' / 'paper-anchors'
TAGS = HERE / 'topic-tags' / 'tags' / 'business.json'
QUESTIONS = ROOT / 'data' / 'examTopics' / 'business-deferred-question-topics.json'
CARDS = ROOT / 'components' / 'MarkBank' / 'cards' / 'business' / 'deferred-authored.json'


def booklets():
    """(year, level, paper key, SEC file id) of every carded deferred booklet, in year, level, booklet order."""
    seen = {}
    for q in json.loads(QUESTIONS.read_text())['questions']:
        seen[(q['year'], q['level'], q['paperKey'])] = q['fileid'].removesuffix('-deferred.pdf')
    return [(y, lv, key, fid) for (y, lv, key), fid in sorted(seen.items())]


def maps():
    out = {}
    for year, level, key, raw in booklets():
        pdf = fitz.open(CORPUS / str(year) / f'{raw}.pdf')
        anchors = BUS.detected_anchors(pdf, level, year, key)
        wanted = BUS.expected_numbers(level, year, key)
        if key == 'p1' and not anchors:
            # The deferred Section 1 booklet heads its short questions "Section A" where June's prints
            # "Section 1"; the numbers are read below that heading as June's are below its own.
            records = BUS.line_records(pdf)
            heads = [(page, round(y, 4)) for page, _x, y, text in records if page > 1 and text == 'Section A']
            assert len(heads) == 1, (year, level, raw, heads)
            anchors = {str(n): at for n, at in BUS.bare_numbers(
                records, (heads[0][0], heads[0][1] - 0.0001), BUS.section_position(records, 2) or (999, 1.0),
                [int(n) for n in wanted]).items()}
        missing = [n for n in wanted if n not in anchors]
        if missing:
            raise SystemExit(f'{year} {level} {raw}: no printed heading found for {missing}')
        last = max(anchors[n] for n in wanted)
        tail = BUS.paper_tail(pdf, last)
        fileid = f'{raw}-deferred.pdf'
        hosted, _ = BUS.hosted_map(fileid, level, year, key, anchors, tail)
        out[OUT / str(year) / f'{fileid}.json'] = hosted
    return out


def tag_papers():
    cards = json.loads(CARDS.read_text())['cards']
    pools = json.loads(CARDS.read_text())['pools']
    weights = defaultdict(lambda: defaultdict(float))
    for card in cards + [dict(p['template'], topicId=p['options'][0]['topicId']) for p in pools]:
        q = question_of(card['questionRef'])
        key = (card['year'], card['level'], f"{card['paperFileid']}.pdf", q)
        weights[key][card['topicId']] += card['totalMarks']
        for extra in card.get('additionalTopicIds', []):
            weights[key][extra] += card['totalMarks'] / 2
    papers = []
    for year, level, key, raw in booklets():
        fileid = f'{raw}-deferred.pdf'
        entries = []
        for n in BUS.expected_numbers(level, year, key):
            topics = weights[(year, level, fileid, n)]
            if not topics:
                raise SystemExit(f'{year} {level} {fileid} Q{n}: no carded topic to tag')
            ranked = sorted(topics, key=lambda t: (-topics[t], t))
            entries.append({'n': n, 'primary': ranked[0], **({'secondary': ranked[1]} if len(ranked) > 1 else {})})
        papers.append({'subjectId': 'business', 'level': level, 'lang': 'ev', 'year': year, 'fileid': fileid,
                       'paperKey': key, 'q': entries})
    return papers


def question_of(ref):
    """The printed question a card's reference names: "ABQ", or the number after Q."""
    m = re.search(r' (?:Q(\d+)|(ABQ))', ref)
    return m.group(1) or m.group(2)


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
