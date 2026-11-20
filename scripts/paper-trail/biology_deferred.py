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
"""Paper-only Atlas anchors for Biology's carded deferred sittings.

Paper Trail indexes each deferred booklet as its own paper ("LC025ALP038EV-deferred.pdf", Sections A and
B; "LC025ALP040EV-deferred.pdf", Section C), numbered as June's. The Topic Atlas lists a carded deferred
sitting's printed questions under those file ids (build-biology-exam-topic-crosswalk.mjs, from the
sitting's reviewed map data/examTopics/biology-<year>-deferred-exam-topic-map.json). This writes the anchor
maps those questions open from, with the June reader's own geometry (biology.py anchors_for and
hosted_map): paper only, mode "pagejump", one entry per printed question, Questions 1-10 in 038 and 11-17
in 040.

A sitting is written once its reviewed map exists (bio_review_<year>_<level>_deferred.py carded it). Its two
booklets are also written into the Paper Trail topic tags (topic-tags/tags/biology.json, then build-tags.mjs),
each printed question tagged with the first two outgoing-curriculum nodes ("biology-x-y") of the topics its
reviewed map gives it, in the map's order: the June wave's own form.

    python3 scripts/paper-trail/biology_deferred.py           # write
    python3 scripts/paper-trail/biology_deferred.py --check   # compare
"""
import argparse
import json
import sys
from pathlib import Path

import fitz

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import biology as BIO  # noqa: E402

ROOT = HERE.parent.parent
CORPUS = ROOT / 'paper-trail-corpus' / 'deferredexams'
OUT = ROOT / 'public' / 'paper-anchors'
TOPIC_MAPS = ROOT / 'data' / 'examTopics'
TAGS = HERE / 'topic-tags' / 'tags' / 'biology.json'
CROSSWALK = TOPIC_MAPS / 'biology-curriculum-crosswalk.json'
SITTINGS = ((2022, 'higher'), (2022, 'ordinary'), (2023, 'higher'), (2023, 'ordinary'), (2024, 'higher'),
            (2025, 'higher'))


def carded(year, level):
    path = TOPIC_MAPS / f'biology-{year}-deferred-exam-topic-map.json'
    if not path.exists():
        return False
    return any(key.startswith(f'{level}|') for key in json.loads(path.read_text())['questions'])


def maps():
    out = {}
    for year, level in SITTINGS:
        if not carded(year, level):
            continue
        letter = 'A' if level == 'higher' else 'G'
        for part in ('038', '040'):
            raw = f'LC025{letter}LP{part}EV'
            pdf = CORPUS / str(year) / f'{raw}.pdf'
            fileid = f'{raw}-deferred.pdf'
            anchors, tail = BIO.anchors_for(fitz.open(pdf), pdf, BIO.expected_numbers(year, fileid))
            hosted, _ = BIO.hosted_map(year, fileid, anchors, tail)
            out[OUT / str(year) / f'{fileid}.json'] = hosted
    return out


def tag_papers():
    """The carded deferred booklets as topic-tag papers, in year, level, booklet order."""
    crosswalk = json.loads(CROSSWALK.read_text())
    papers = []
    for year, level in SITTINGS:
        if not carded(year, level):
            continue
        questions = json.loads((TOPIC_MAPS / f'biology-{year}-deferred-exam-topic-map.json').read_text())['questions']
        letter = 'A' if level == 'higher' else 'G'
        for part in ('038', '040'):
            fileid = f'LC025{letter}LP{part}EV-deferred.pdf'
            entries = []
            for n in BIO.expected_numbers(year, fileid):
                nodes = []
                for topic in questions[f'{level}|{n}']:
                    for node in crosswalk[topic]:
                        if node.startswith('biology-') and node not in nodes:
                            nodes.append(node)
                if not nodes:
                    raise SystemExit(f'{year} {level} deferred Q{n}: no outgoing-curriculum node to tag')
                entries.append({'n': str(n), 'primary': nodes[0], **({'secondary': nodes[1]} if len(nodes) > 1 else {})})
            papers.append({'subjectId': 'biology', 'level': level, 'lang': 'ev', 'year': year, 'fileid': fileid,
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
