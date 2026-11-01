#!/usr/bin/env python3
"""Apply the independently reviewed 2023 HL English B/C anchor correction.

Keep B1..B5 identities; append C1..C4 as 6..9. Irish editions are deferred.
This overlay also runs after the general reference-crosswalk builder, so a
rebuild cannot send reviewed Section C headings back to Section B.
"""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import re
import sys

from he_review_2023_hl import ROOT, HASHES

SUBJECT = 'home-economics-s-and-s'
FILE = 'LC098ALP039EV.pdf'


def read(path):
    return json.loads((ROOT / path).read_text())


def write(path, value, indent=2):
    path = ROOT / path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=indent) + '\n')


def apply():
    for path, expected in HASHES.items():
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == expected
    sidecar_path = f'scripts/paper-trail/answers/2023/{FILE}.json'
    sidecar = read(sidecar_path)
    sidecar['band'] = [1, 45]  # half-open: all 44 physical scheme pages
    for q in sidecar['q'][:5]:
        q['label'] = f"Section B · Q{q['n']}"
        q['printOrder'] = int(q['n'])
    # B5 finishes on scheme p17. The old region incorrectly continued through
    # the first two pages of Elective 1, making its apparent reveal unrelated.
    sidecar['q'][4]['region'] = [
        {'p': 17, 'r': [0, 0.0797, 1, 1]},
        {'p': 18, 'r': [0, 0, 1, 1]}, {'p': 19, 'r': [0, 0, 1, 1]},
    ]
    sidecar['q'][4]['schemeRegion'] = [{'p': 17, 'r': [0, 0.0797, 1, 0.95]}]
    sidecar['q'][4].pop('pEndP', None)
    sidecar['q'][4]['endP'] = 4
    sidecar['q'][4]['endY'] = 0.87
    for number, paper_page, scheme_start, scheme_end in [
        (1, 5, 18, 20), (2, 6, 21, 22), (3, 7, 23, 25), (4, 8, 26, 28),
    ]:
        q = dict(n=str(number + 5), label=f'Section C · Q{number}', printOrder=number + 5,
                 pP=paper_page, pY=[0.06, 0.885], endP=paper_page, endY=0.885,
                 conf=1.0, mode='crop',
                 region=[dict(p=p, r=[0, 0.035, 1, 0.96]) for p in range(scheme_start, scheme_end + 1)])
        if len(sidecar['q']) < number + 5:
            sidecar['q'].append(q)
        else:
            sidecar['q'][number + 4] = q
    assert len(sidecar['q']) == 9
    write(sidecar_path, sidecar)
    write(f'public/paper-answers/2023/{FILE}.json', sidecar)
    hosted = dict(v=1, paperOnly=1, paperFileid=FILE, schemeFileid='', component='039', band=[1, 1],
                  copyright='© State Examinations Commission',
                  q=[{**{k: v for k, v in q.items() if k not in ('region', 'schemeRegion', 'mode', 'conf')},
                      'region': [{'p': 1}], 'mode': 'pagejump', 'conf': 0.5} for q in sidecar['q']])
    write(f'public/paper-anchors/2023/{FILE}.json', hosted)

    # Build the reviewed question/topic map from the actual emitted cards,
    # preserving all canonical topic placements, including the new career.
    crosswalk = read(f'data/examTopics/{SUBJECT}-curriculum-crosswalk.json')
    node_topics = {}
    for topic, nodes in crosswalk.items():
        if '-higher-' in topic:
            for node in nodes:
                node_topics.setdefault(node, []).append(topic)
    deck = (ROOT / 'components/MarkBank/cards/home-economics/higher.ts').read_text()
    canonical = {str(n): set() for n in range(1, 10)}
    reviewed_cards = []
    for chunk in re.split(r'^\s*\.\.\.base,', deck, flags=re.M)[1:]:
        ref = re.search(r'questionRef: "(2023 HL Section ([BC]) (?:E\d )?Q(\d+)[^"]*)"', chunk)
        if not ref:
            continue
        cid = re.search(r'\bid: "([^"]+)"', chunk).group(1)
        node = re.search(r'topicId: "([^"]+)"', chunk).group(1)
        n = str(int(ref[3]) + (5 if ref[2] == 'C' else 0))
        assert node in node_topics, (cid, node)
        canonical[n].add(node)
        reviewed_cards.append(dict(id=cid, questionRef=ref[1], n=n, topicId=node,
                                   atlasTopicIds=node_topics[node]))
    assert all(canonical.values())
    tags_path = f'scripts/paper-trail/topic-tags/tags/{SUBJECT}.json'
    tags = read(tags_path)
    paper = next(p for p in tags if p['year'] == 2023 and p['fileid'] == FILE)
    for number in range(6, 10):
        nodes = sorted(canonical[str(number)])
        tag = dict(n=str(number), primary=nodes[0])
        if len(nodes) > 1:
            tag['secondary'] = nodes[1]
        existing = next((q for q in paper['q'] if q['n'] == str(number)), None)
        if existing:
            existing.update(tag)
        else:
            paper['q'].append(tag)
    write(tags_path, tags, indent=1)

    local_path = f'data/examTopics/{SUBJECT}-local-crosswalk.json'
    local = read(local_path)
    before = (local['summary']['localAnswerAnchoredPhysicalCards'] - 4
              if '--after-reference-build' in sys.argv else
              local.get('reviewedEnglish2023', {}).get('priorPhysicalQuestionCount',
                  local['summary']['localAnswerAnchoredPhysicalCards']))
    for association in local['associations']:
        if association['level'] != 'higher' or not association['heading'].startswith('2023 '):
            continue
        if 'Deferred' in association['heading']:
            continue
        match = re.search(r'Section ([BC]) - Question (\d+)', association['heading'])
        if not match:
            continue
        n = str(int(match[2]) + (5 if match[1] == 'C' else 0))
        targets = association.setdefault('targets', [])
        if not any(t['fileid'] == FILE and t['lang'] == 'ev' for t in targets):
            targets.append(dict(level='higher', lang='ev', year=2023,
                                paperKey='single', fileid=FILE, n=n))
        association['resolution'] = 'matched'
        association.pop('reason', None)
        for target in targets:
            if target['fileid'] == FILE and target['lang'] == 'ev':
                target['n'] = n
                target['label'] = f'Section {match[1]} · Q{match[2]}'

    runtime_path = f'data/examTopics/{SUBJECT}-question-runtime.json'
    runtime = read(runtime_path)
    mappings = runtime['questionMappings']
    topics_by_n = {n: {topic for node in nodes for topic in node_topics[node]} for n, nodes in canonical.items()}
    for association in local['associations']:
        for target in association.get('targets', []):
            if target['year'] == 2023 and target['fileid'] == FILE and target['lang'] == 'ev':
                topics_by_n[target['n']].add(association['topicId'])
    updated = []
    added = False
    for row in mappings:
        if row[:5] == ['h', 'e', 2023, 'single', FILE]:
            if not added:
                updated += [['h', 'e', 2023, 'single', FILE, str(n),
                             sorted(runtime['topicIds'].index(topic) for topic in topics_by_n[str(n)])]
                            for n in range(1, 10)]
                added = True
        else:
            updated.append(row)
    assert added
    runtime['questionMappings'] = updated
    write(runtime_path, runtime)
    local['summary']['exactRuntimeQuestionMappings'] = len(updated)
    local['summary']['localAnswerAnchoredPhysicalCards'] = before + 4
    matched = [a for a in local['associations'] if a['resolution'] == 'matched']
    blocked = [a for a in local['associations'] if a['resolution'] == 'source-blocked']
    local['summary']['matchedAssociations'] = len(matched)
    local['summary']['sourceBlockedAssociations'] = len(blocked)
    local['summary']['matchedLocalCardLinks'] = sum(len(a['targets']) for a in matched)
    local['summary']['sourceBlockedByReason'] = {reason: sum(a['reason'] == reason for a in blocked)
                                               for reason in sorted({a['reason'] for a in blocked})}
    local['reviewedEnglish2023'] = dict(
        priorPhysicalQuestionCount=before, paperFileid=FILE, physicalQuestions=9,
        review='scripts/markbank/authoring/home-economics/2023-hl-recovery-review.json',
        policy='B1–B5 retain their IDs; C1–C4 use IDs 6–9. English source anchors and headings reviewed; Irish editions deferred.',
        markBankMappings=reviewed_cards)
    write(local_path, local)
    print(f'2023 HL Home Economics: 9 B/C questions; {len(reviewed_cards)} Mark Bank cards mapped to their own section.')


if __name__ == '__main__':
    apply()
