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
"""Paper-only Atlas anchors and topic tags for Chemistry's carded deferred sittings.

Paper Trail indexes each deferred paper as its own file ("LC022ALP000EV-deferred.pdf"), numbered Q1-Q11 as
June's. A sitting is written here once Mark Bank holds its cards (chem_<year>_<lvl>_deferred.py, ids
chem-<year>-<lvl>-deferred-...), and then:

  * its anchor map, public/paper-anchors/<year>/<fileid>.json, with the June reader's own geometry
    (chemistry.py anchors_for and hosted_map): paper only, mode "pagejump", one entry per printed question;
  * its topic-tag paper in topic-tags/tags/chemistry.json, after June's (then build-tags.mjs), each printed
    question tagged with the first two outgoing-curriculum nodes ("chemistry-x-y") of the outgoing-course
    topics the factual reference (data/examTopics/chemistry.json) lists that deferred question under, in the
    reference's order, through the curriculum crosswalk: the June wave's own form. The reference's format
    headings (the experiment questions, Q4's short items: isFormatTopic in build-chemistry-exam-topic-
    crosswalk.mjs) name a question's place on the paper, not its chemistry, and are not read; a question the
    reference lists under no other topic carries the reviewed tags in REVIEWED, each with its evidence.

Chemistry is a single-model subject: the Topic Atlas files each deferred question's parts by the cards'
own filings (scripts/atlas-model/filings/chemistry.json), not by these tags.

    python3 scripts/paper-trail/chemistry_deferred.py           # write
    python3 scripts/paper-trail/chemistry_deferred.py --check   # compare
"""
import argparse
import json
import re
import sys
from pathlib import Path

import fitz

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import chemistry as CH  # noqa: E402

ROOT = HERE.parent.parent
CORPUS = ROOT / 'paper-trail-corpus' / 'deferredexams'
OUT = ROOT / 'public' / 'paper-anchors'
TAGS = HERE / 'topic-tags' / 'tags' / 'chemistry.json'
REFERENCE = ROOT / 'data' / 'examTopics' / 'chemistry.json'
CROSSWALK = ROOT / 'data' / 'examTopics' / 'chemistry-curriculum-crosswalk.json'
DECK = ROOT / 'scripts' / 'markbank' / 'authored' / 'chemistry.json'
# The SEC's deferred Chemistry sittings: 2022 at both levels and 2023 Higher (deferredexams/<year>/).
SITTINGS = ((2022, 'higher', 'LC022ALP000EV'), (2022, 'ordinary', 'LC022GLP000EV'), (2023, 'higher', 'LC022ALP000EV'))
NUMBERS = [str(n) for n in range(1, 12)]

# Deferred questions the factual reference lists under no content topic, tagged by review of the paper, each as
# June tags the same experiment.
REVIEWED = {
    # 2022 Higher Q1 (listed only as "experiment Q1 titration"): the iron(II) content of ammonium iron(II) sulfate
    # by manganate(VII) titration, tagged as June 2021, 2023 and 2024 Higher Q1's titrations are: 4.3 Volumetric
    # Analysis, then 4.1 Concentration of Solutions.
    (2022, 'higher', '1'): ['chemistry-3-2', 'chemistry-3-0'],
    # 2022 Higher Q2 (not listed): the steam distillation of clove oil and its liquid-liquid extraction, the
    # experiment June 2011 and 2018 Higher Q2 set, both tagged 7.4 Organic Natural Products, then 7.3 Organic
    # Reaction Types.
    (2022, 'higher', '2'): ['chemistry-6-3', 'chemistry-6-2'],
    # 2022 Higher Q3 (listed only as "experiment Q3 other"): the rate of decomposition of hydrogen peroxide, tagged
    # as June 2022 Higher Q3's rate experiment is: 6.1 Reaction Rates, then 6.2 Factors Affecting Rates.
    (2022, 'higher', '3'): ['chemistry-5-0', 'chemistry-5-1'],
    # 2022 Ordinary Q1 (not listed): the recrystallisation of benzoic acid and its melting point, tagged as June 2024
    # Higher Q2's recrystallisation is: 7.3 Organic Reaction Types, then 7.4 Organic Natural Products.
    (2022, 'ordinary', '1'): ['chemistry-6-2', 'chemistry-6-3'],
    # 2022 Ordinary Q2 (not listed): an acid-base titration with a standard solution, tagged as every June Ordinary Q2
    # titration from 2014 to 2026 (bar 2017's one tag, 2022's and 2024's) is: 4.3 Volumetric Analysis, then 4.1
    # Concentration of Solutions.
    (2022, 'ordinary', '2'): ['chemistry-3-2', 'chemistry-3-0'],
    # 2022 Ordinary Q3 (listed only as an experiment question): the dissolved solids in seawater, tagged as June 2023
    # Ordinary Q3's is: 9.4 Water Analysis, then 4.1 Concentration of Solutions.
    (2022, 'ordinary', '3'): ['chemistry-8-3', 'chemistry-3-0'],
    # 2023 Higher Q2 (listed only as "experiment Q2 organic"): tests on organic compounds and the recrystallisation
    # of benzoic acid, tagged as June 2022 and 2023 Higher Q2's organic experiments are: chemistry-4-1, then
    # chemistry-6-2 (7.3 Organic Reaction Types).
    (2023, 'higher', '2'): ['chemistry-4-1', 'chemistry-6-2'],
}


def format_topic(topic_id):
    # isFormatTopic in build-chemistry-exam-topic-crosswalk.mjs: the experiment questions and Q4's short items.
    return '-experiment-' in topic_id or topic_id.endswith('-q4')


def carded(year, level):
    prefix = f"chem-{year}-{'hl' if level == 'higher' else 'ol'}-deferred-"
    return any(c['id'].startswith(prefix) for c in json.loads(DECK.read_text()))


def maps():
    out = {}
    for year, level, raw in SITTINGS:
        if not carded(year, level):
            continue
        pdf = CORPUS / str(year) / f'{raw}.pdf'
        fileid = f'{raw}-deferred.pdf'
        with fitz.open(pdf) as document:
            anchors, tail = CH.anchors_for(document, pdf)
        hosted, _ = CH.hosted_map(fileid, anchors, tail)
        out[OUT / str(year) / f'{fileid}.json'] = hosted
    return out


def listed_nodes(year, level):
    """Question number -> the outgoing-curriculum nodes of the topics the reference lists it under."""
    reference = json.loads(REFERENCE.read_text())
    crosswalk = json.loads(CROSSWALK.read_text())
    out = {}
    for topic in reference['variants'][f'{level}-old-course']['topics']:
        if format_topic(topic['id']):
            continue
        for heading in topic['officialQuestionHeadings']:
            m = re.match(rf'^{year} - Deferred Exam Paper\s+- .*?Question\s+(\d+)\b', heading)
            if not m:
                continue
            nodes = out.setdefault(m.group(1), [])
            for node in crosswalk[topic['id']]:
                if node.startswith('chemistry-') and node not in nodes:
                    nodes.append(node)
    return out


def tag_papers():
    """The carded deferred papers as topic-tag papers, in year then level order."""
    papers = []
    for year, level, raw in SITTINGS:
        if not carded(year, level):
            continue
        listed = listed_nodes(year, level)
        entries = []
        for n in NUMBERS:
            nodes = listed.get(n) or REVIEWED.get((year, level, n))
            if listed.get(n) and (year, level, n) in REVIEWED:
                raise SystemExit(f'{year} {level} deferred Q{n}: the reference now lists it; drop it from REVIEWED')
            if not nodes:
                raise SystemExit(f'{year} {level} deferred Q{n}: no outgoing-curriculum node to tag')
            entries.append({'n': n, 'primary': nodes[0], **({'secondary': nodes[1]} if len(nodes) > 1 else {})})
        papers.append({'subjectId': 'chemistry', 'level': level, 'lang': 'ev', 'year': year,
                       'fileid': f'{raw}-deferred.pdf', 'paperKey': 'single', 'q': entries})
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
