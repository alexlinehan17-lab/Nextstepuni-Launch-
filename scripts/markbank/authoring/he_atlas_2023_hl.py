#!/usr/bin/env python3
"""Apply the independently reviewed 2023 English B/C anchor corrections.

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
from he_review_2023_ol import HASHES as OL_HASHES

SUBJECT = 'home-economics-s-and-s'
def physical_question_count():
    # Use the same answers=1 entries as localTargetsFor in the reference
    # builder. Recount actual maps so reruns and two-level overlays are stable.
    index = (ROOT / 'paperTrailData.ts').read_text()
    match = re.search(r'^  "home-economics-s-and-s": \[\n(.*?)^  \]', index, re.M | re.S)
    assert match, 'Generated index format changed'
    entries = [json.loads(line.strip().rstrip(',')) for line in match[1].splitlines() if line.strip()]
    return sum(len(read(f"scripts/paper-trail/answers/{entry['year']}/{paper['doc']['f']}.json")['q'])
               for entry in entries for paper in entry['papers'] if paper.get('answers') == 1)


def read(path):
    return json.loads((ROOT / path).read_text())


def write(path, value, indent=2):
    path = ROOT / path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=indent) + '\n')


def apply(level='higher'):
    higher = level == 'higher'
    code, short = ('h', 'HL') if higher else ('o', 'OL')
    FILE = 'LC098ALP039EV.pdf' if higher else 'LC098GLP039EV.pdf'
    metadata_key = 'reviewedEnglish2023' if higher else 'reviewedEnglish2023Ordinary'
    for path, expected in (HASHES if higher else OL_HASHES).items():
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == expected
    sidecar_path = f'scripts/paper-trail/answers/2023/{FILE}.json'
    sidecar = read(sidecar_path)
    sidecar['band'] = [1, 45 if higher else 39]  # half-open physical scheme band
    for q in sidecar['q'][:5]:
        q['label'] = f"Section B · Q{q['n']}"
        q['printOrder'] = int(q['n'])
    if higher:
        # Preserve the previous stored region, while the reviewed reveal uses
        # only B5 on scheme p17 (not the following Elective 1 pages).
        sidecar['q'][4]['region'] = [
            {'p': 17, 'r': [0, 0.0797, 1, 1]},
            {'p': 18, 'r': [0, 0, 1, 1]}, {'p': 19, 'r': [0, 0, 1, 1]},
        ]
        sidecar['q'][4]['schemeRegion'] = [{'p': 17, 'r': [0, 0.0797, 1, 0.95]}]
    sidecar['q'][4].pop('pEndP', None)
    sidecar['q'][4]['endP'] = 4
    sidecar['q'][4]['endY'] = 0.87
    ranges = ([(1, 5, 18, 20), (2, 6, 21, 22), (3, 7, 23, 25), (4, 8, 26, 28)] if higher else
              [(1, 5, 16, 17), (2, 6, 18, 19), (3, 7, 20, 22), (4, 8, 23, 24)])
    for number, paper_page, scheme_start, scheme_end in ranges:
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
        if f'-{level}-' in topic:
            for node in nodes:
                node_topics.setdefault(node, []).append(topic)
    deck = (ROOT / f'components/MarkBank/cards/home-economics/{level}.ts').read_text()
    canonical = {str(n): set() for n in range(1, 10)}
    reviewed_cards = []
    for chunk in re.split(r'^\s*\.\.\.base,', deck, flags=re.M)[1:]:
        ref = re.search(rf'questionRef: "(2023 {short} Section ([BC]) (?:E\d )?Q(\d+)[^"]*)"', chunk)
        if not ref:
            continue
        if 'Deferred' in ref[1]:
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
    if not higher:
        short_paper = next(p for p in tags if p['year'] == 2023 and p['fileid'] == 'LC098GLP014EV.pdf')
        symbols = next(q for q in short_paper['q'] if q['n'] == '14')
        symbols['primary'] = 'home-economics-1-4'
        symbols.pop('secondary', None)
    write(tags_path, tags, indent=1)

    local_path = f'data/examTopics/{SUBJECT}-local-crosswalk.json'
    local = read(local_path)
    for association in local['associations']:
        if association['level'] != level or not association['heading'].startswith('2023 '):
            continue
        if 'Deferred' in association['heading']:
            continue
        match = re.search(r'Section ([BC]) - Question (\d+)', association['heading'])
        if not match:
            continue
        n = str(int(match[2]) + (5 if match[1] == 'C' else 0))
        targets = association.setdefault('targets', [])
        if not any(t['fileid'] == FILE and t['lang'] == 'ev' for t in targets):
            targets.append(dict(level=level, lang='ev', year=2023,
                                paperKey='single', fileid=FILE, n=n))
        association['resolution'] = 'matched'
        association.pop('reason', None)
        for target in targets:
            if target['fileid'] == FILE and target['lang'] == 'ev':
                target['n'] = n
                target['label'] = f'Section {match[1]} · Q{match[2]}'

    if not higher:
        for association in local['associations']:
            if (association['level'] == 'ordinary' and association['heading'] == '2023 - Section A - Question 14'
                    and association['topicId'] == f'{SUBJECT}-ordinary-household-appliances'):
                # English paper p7 shows fabric-care symbols. Preserve the
                # unreviewed Irish target; record why this English link is wrong.
                association['targets'] = [t for t in association['targets'] if t['lang'] != 'ev']
                association['englishSourceCorrection'] = 'Fabric-care symbols, not household appliances; English target mapped to textiles from the original paper.'

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
        if row[:5] == [code, 'e', 2023, 'single', FILE]:
            if not added:
                updated += [[code, 'e', 2023, 'single', FILE, str(n),
                             sorted(runtime['topicIds'].index(topic) for topic in topics_by_n[str(n)])]
                            for n in range(1, 10)]
                added = True
        else:
            updated.append(row)
    assert added
    if not higher:
        symbols = next(row for row in updated if row[:6] == ['o', 'e', 2023, 'single', 'LC098GLP014EV.pdf', '14'])
        symbols[6] = sorted(runtime['topicIds'].index(t) for t in node_topics['home-economics-1-4'])
    runtime['questionMappings'] = updated
    write(runtime_path, runtime)
    local['summary']['exactRuntimeQuestionMappings'] = len(updated)
    local['summary']['localAnswerAnchoredPhysicalCards'] = physical_question_count()
    matched = [a for a in local['associations'] if a['resolution'] == 'matched']
    blocked = [a for a in local['associations'] if a['resolution'] == 'source-blocked']
    local['summary']['matchedAssociations'] = len(matched)
    local['summary']['sourceBlockedAssociations'] = len(blocked)
    local['summary']['matchedLocalCardLinks'] = sum(len(a['targets']) for a in matched)
    local['summary']['sourceBlockedByReason'] = {reason: sum(a['reason'] == reason for a in blocked)
                                               for reason in sorted({a['reason'] for a in blocked})}
    local[metadata_key] = dict(
        paperFileid=FILE, physicalQuestions=9,
        review=f'scripts/markbank/authoring/home-economics/2023-{short.lower()}-recovery-review.json',
        policy='B1–B5 retain their IDs; C1–C4 use IDs 6–9. English source anchors and headings reviewed; Irish editions deferred.',
        markBankMappings=reviewed_cards)
    write(local_path, local)
    print(f'2023 {short} Home Economics: 9 B/C questions; {len(reviewed_cards)} Mark Bank cards mapped to their own section.')


if __name__ == '__main__':
    apply('higher')
    apply('ordinary')
    from he_atlas_deferred import apply as apply_deferred
    apply_deferred()
    from he_atlas_2022_deferred import apply as apply_deferred_2022
    apply_deferred_2022()
    from he_atlas_2022_ol import apply as apply_ordinary_2022
    apply_ordinary_2022()
    from he_atlas_2022_hl_main import apply as apply_higher_main_2022
    apply_higher_main_2022()
    from he_atlas_2021_hl_main import apply as apply_higher_main_2021
    apply_higher_main_2021()

# Preserve the independently reviewed 2021 Ordinary English overlay on regeneration.
if __name__ == "__main__":
 from he_atlas_2021_ol_main import apply as apply_2021_ol_main
 apply_2021_ol_main()

# Preserve the independently reviewed 2024 Higher English overlay.
if __name__ == "__main__":
 from he_atlas_2024_hl_main import apply as apply_2024_hl_main
 apply_2024_hl_main()
