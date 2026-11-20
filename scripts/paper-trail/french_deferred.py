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
"""Paper-only Atlas anchors and Paper Trail topic tags for French's deferred sittings.

Paper Trail indexes each deferred booklet as its own paper: the written paper
"LC010ALP000BV-deferred.pdf" and the listening booklet "LC010ALPA00BV-deferred.pdf"
(Ordinary: LC010GLP...); a listening booklet is written here once its sitting's
listening is carded (AURAL_CARDED). The Topic Atlas already lists their printed questions as
the StudyClix references of data/examTopics/french-runtime.json whose sitting is
'd': "A1".."A4" for the reading comprehensions, "B1A".."B6" for Section B and "1".."5"
for the listening sections. This writes, for each of those questions:

  * an anchor map entry the question opens from (paper only, mode "pagejump"),
    on the page the booklet prints it: a comprehension's first page, a Section B
    question's page, a listening section's page ("SECTION A" ... "SECTION E");
  * its Paper Trail topic tags (topic-tags/tags/french.json, then build-tags.mjs):
    the Paper Trail topics of the runtime topics those references name, in the
    references' own order, the first as primary and the second, if any, as
    secondary.

The reviewed cards' own task anchors are added beneath these parents by
french-reviewed-anchors.mjs, as June's are.

    python3 scripts/paper-trail/french_deferred.py           # write
    python3 scripts/paper-trail/french_deferred.py --check   # compare
"""
import argparse
import json
import re
import sys
from pathlib import Path

import fitz

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT / 'scripts' / 'markbank' / 'authoring'))
from fr_paper import FrPaper  # noqa: E402

PAPERS = ROOT / 'examiner-reports' / 'french' / 'papers'
OUT = ROOT / 'public' / 'paper-anchors'
TAGS = HERE / 'topic-tags' / 'tags' / 'french.json'
RUNTIME = ROOT / 'data' / 'examTopics' / 'french-runtime.json'
TASKS = ROOT / 'data' / 'examTopics' / 'french-reviewed-tasks.json'

# The carded deferred sittings: those the reviewed reading ledger lists (of paper_census.FR_DEFERRED_SITTINGS).
SITTINGS = tuple((r['year'], r['level']) for r in json.loads(
    (ROOT / 'scripts' / 'markbank' / 'authoring' / 'french-reading-review-deferred.json').read_text())['papers'])
# The listening booklets join the Atlas when their sitting's listening is carded, which waits on the
# deferred recordings (coordinator, 20 November 2026: the audio lane fetches and fingerprints them first).
AURAL_CARDED = set()
LEVEL = {'hl': 'higher', 'ol': 'ordinary'}


def fileid(level, component):
    return f'LC010{"A" if level == "hl" else "G"}LP{component}BV-deferred.pdf'


# The two deferred comprehensions the StudyClix references do not list (2023 Higher A1 and A2), settled
# by the source each prints beneath its passage: an online magazine article is a newspaper/magazine
# comprehension, a novel extract a literary one -- the two Higher reading topics of the runtime.
PRINTED_SOURCES = {
    (2023, 'hl', 's', 'A1'): ('french-higher-newspapermagazine-comprehension',
                              'paper page 4 prints the passage "Adapté de La-Zep.fr 30/11/2021" (an online magazine)'),
    (2023, 'hl', 's', 'A2'): ('french-higher-literarynovel-comprehension',
                              'paper page 6 prints "Dans cet extrait ..." and "Adapté de Un Cirque Passe, Patrick Modiano" (a novel)'),
}


def references(year, level, key):
    """{question: [Paper Trail topic, ...]} from the runtime's deferred StudyClix references
    (and PRINTED_SOURCES where they list none)."""
    runtime = json.loads(RUNTIME.read_text())
    out = {}
    for (y, lv, k, n), (topic_id, _evidence) in PRINTED_SOURCES.items():
        if (y, lv, k) == (year, level, key):
            topic = next(t for t in runtime['topics'] if t[0] == topic_id)
            out[n] = list(topic[5])
    for topic, yy, lv, paper, sitting, n, _heading in runtime['partReferences']:
        if (yy, lv, paper, sitting) != (year - 2000, level[0], key, 'd'):
            continue
        for tag in runtime['topics'][topic][5]:
            if tag not in out.setdefault(n, []):
                out[n].append(tag)
    return out


def runtime_topic_ids(year, level, key, n):
    """The Topic Atlas topics (runtime topic ids) a deferred question is listed under: its StudyClix
    references, or PRINTED_SOURCES where they list none."""
    runtime = json.loads(RUNTIME.read_text())
    ids = [topic_id for (y, lv, k, nn), (topic_id, _evidence) in PRINTED_SOURCES.items()
           if (y, lv, k, nn) == (year, level, key, n)]
    for topic, yy, lv, paper, sitting, nn, _heading in runtime['partReferences']:
        if (yy, lv, paper, sitting, nn) == (year - 2000, level[0], key, 'd', n) and runtime['topics'][topic][0] not in ids:
            ids.append(runtime['topics'][topic][0])
    assert ids, (year, level, key, n)
    return ids


def head_y(pdf, page, pattern):
    """Where on its page a printed head starts (its top, as a fraction), or 0."""
    p = pdf[page - 1]
    for block in p.get_text('dict')['blocks']:
        for line in block.get('lines', []):
            text = ' '.join(''.join(span['text'] for span in line['spans']).split())
            if re.search(pattern, text):
                return round(line['bbox'][1] / p.rect.height, 4)
    return 0.0


def written(year, level):
    """[(n, label, page, y)] for the written paper: the comprehensions, then Section B."""
    paper = FrPaper(year, level, sitting='deferred')
    pdf = fitz.open(paper.path)
    rows = []
    for rc, pages in sorted(paper.rc_pages.items()):
        rows.append((f'A{rc}', f'Reading Comprehension {rc}', pages[0],
                     head_y(pdf, pages[0], rf'^(?:Q|C)\.\s*{rc}\b')))
    for q, letter, _text, page in paper.section_b_asks():
        n = f'B{q}{(letter or "").upper()}'
        label = f'Section B · Q{q}' + (f'({letter})' if letter else '')
        # A lettered alternative opens at its own "(a)"; a question at its "Question N" head.
        rows.append((n, label, page, head_y(pdf, page, rf'^\({letter}\)$' if letter else rf'^Question {q}\b\.?')))
    return rows


def aural(year, level):
    """[(n, label, page, y)] for the listening booklet: one per printed SECTION A-E."""
    path = PAPERS / f'{year}-{level}-deferred-A00-paper.pdf'
    pdf = fitz.open(path)
    rows = []
    for i, page in enumerate(pdf, 1):
        for block in page.get_text('dict')['blocks']:
            for line in block.get('lines', []):
                text = ' '.join(''.join(span['text'] for span in line['spans']).split())
                m = re.search(r'\bSECTION\s+([A-E])$', text)
                if m:
                    rows.append((str(ord(m.group(1)) - 64), f'Listening Section {m.group(1)}', i,
                                 round(line['bbox'][1] / page.rect.height, 4)))
    assert [r[0] for r in rows] == ['1', '2', '3', '4', '5'], (year, level, rows)
    return rows


def anchor_map(fid, component, rows):
    q = [{'n': n, 'label': label, 'printOrder': i, 'pP': page, 'pY': [y, 1],
          'paperRegion': [{'p': page, 'r': [0, 0, 1, 1]}], 'region': [{'p': 1}],
          'mode': 'pagejump', 'conf': 0.5}
         for i, (n, label, page, y) in enumerate(rows, 1)]
    return {'v': 1, 'paperFileid': fid, 'schemeFileid': '', 'component': component, 'band': [1, 1],
            'copyright': '© State Examinations Commission', 'paperOnly': 1, 'q': q}


def maps_and_tags():
    maps, tags = {}, []
    for year, level in SITTINGS:
        components = [('000', 's', written(year, level))]
        if (year, level) in AURAL_CARDED:
            components.append(('A00', 'a', aural(year, level)))
        for component, key, rows in components:
            fid = fileid(level, component)
            refs = references(year, level, key)
            missing = [n for n, *_ in rows if n not in refs]
            assert not missing and set(refs) == {n for n, *_ in rows}, (year, level, component, missing, sorted(refs))
            maps[OUT / str(year) / f'{fid}.json'] = anchor_map(fid, component, rows)
            q = [{'n': n, 'primary': refs[n][0], **({'secondary': refs[n][1]} if len(refs[n]) > 1 else {})}
                 for n, *_ in rows]
            # Each reviewed card's own task beneath its question (A1-Q1-a, B1B-field-1, B1A-gap-3 ...), in the
            # order french-reviewed-anchors.mjs adds them to the anchor map, under its question's topics.
            parents = {row['n']: row for row in q}
            for task in json.loads(TASKS.read_text()):
                if task['year'] == year and task['fileid'] == fid and task['n'] != task['parent']:
                    q.append({**parents[task['parent']], 'n': task['n']})
            tags.append({'subjectId': 'french', 'level': LEVEL[level], 'lang': 'ev', 'year': year, 'fileid': fid,
                         'paperKey': 'single' if key == 's' else 'aural', 'q': q})
    return maps, tags


def tags_text(tags):
    june = [p for p in json.loads(TAGS.read_text()) if not p['fileid'].endswith('-deferred.pdf')]
    return json.dumps(june + tags, indent=2, ensure_ascii=False) + '\n'


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--check', action='store_true')
    args = ap.parse_args()
    maps, tags = maps_and_tags()
    stale = []
    for path, hosted in maps.items():
        if path.exists():
            # french-reviewed-anchors.mjs adds the reviewed cards' task anchors beneath these parents.
            existing = json.loads(path.read_text())
            parents = {q['n'] for q in hosted['q']}
            # A parent that is itself a reviewed task (a Section B question) carries the task's own
            # pages, which french-reviewed-anchors.mjs sets; keep them.
            regions = {q['n']: q['paperRegion'] for q in existing['q'] if q['n'] in parents}
            for q in hosted['q']:
                q['paperRegion'] = regions.get(q['n'], q['paperRegion'])
            hosted['q'] += [q for q in existing['q'] if q['n'] not in parents]
            if 'maxCropPages' in existing:
                hosted['maxCropPages'] = existing['maxCropPages']
        text = json.dumps(hosted, ensure_ascii=False, separators=(',', ':')) + '\n'
        if args.check:
            if not path.exists() or path.read_text() != text:
                stale.append(str(path.relative_to(ROOT)))
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
        print('wrote', path.relative_to(ROOT))
    text = tags_text(tags)
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
