#!/usr/bin/env python3
"""Reviewed LCVP 2017 anchors; keep the existing 1–17 physical identities."""
import json
import re
from copy import deepcopy
from lcvp_review_2017 import ROOT, REVIEW, documents, tidy

FILE = 'LC462CLPO00EV.pdf'


def read(path):
    return json.loads((ROOT / path).read_text())


def write(path, value, indent=2):
    path = ROOT / path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=indent) + '\n')


def head(doc, page, q):
    found = []
    for block in doc[page - 1].get_text('dict')['blocks']:
        for line in block.get('lines', []):
            value = tidy(''.join(s['text'] for s in line['spans']))
            if re.match(r'^Q\.?\s*' + str(q) + r'(?:\s|$)', value):
                found.append(line['bbox'][1] - 3)
    assert len(found) in [1, 2], (page, q, found)
    # The scheme repeats the same question head before roman(ii).
    return max(0, min(found) / doc[page - 1].rect.height)


def bottom(doc, page):
    p = doc[page - 1]
    bounds = [line['bbox'][1] - 2 for block in p.get_text('dict')['blocks']
              for line in block.get('lines', [])
              if line['bbox'][1] > p.rect.height * .82 and (
                  (re.fullmatch(r'\d{1,2}', tidy(''.join(s['text'] for s in line['spans'])))
                   and line['bbox'][1] > p.rect.height * .90
                   and .4 * p.rect.width < (line['bbox'][0] + line['bbox'][2]) / 2 < .6 * p.rect.width)
                  or re.fullmatch(r'Page \d+ of 32', tidy(''.join(s['text'] for s in line['spans']))))]
    return min(bounds) / p.rect.height if bounds else .96


def anchors():
    paper, scheme = documents()
    paper_pages = [3, 3, 3, 4, 4, 5, 6, 7, 9, 10, 11, 14, 17, 20, 23, 26, 29]
    scheme_pages = [4, 4, 4, 4, 4, 4, 5, 5, 6, 6, 8, 9, 10, 11, 12, 13, 14]
    scheme_end = [4, 4, 4, 4, 4, 4, 5, 5, 6, 7, 8, 9, 10, 12, 13, 14, 14]
    identities = [('A', q) for q in range(1, 9)] + [('B', q) for q in range(1, 4)] + [('C', q) for q in range(1, 7)]
    result = []
    for i, (section, q) in enumerate(identities):
        pp, sp, se = paper_pages[i], scheme_pages[i], scheme_end[i]
        py, sy = head(paper, pp, q), head(scheme, sp, q)
        pe = pp + 2 if section == 'C' else pp + 1 if (section, q) in [('A', 5), ('B', 2), ('B', 3)] else pp
        pb = head(paper, pe, identities[i + 1][1]) if i < 16 and paper_pages[i + 1] == pe else bottom(paper, pe)
        regions = []
        for pn in range(sp, se + 1):
            lower = head(scheme, pn, identities[i + 1][1]) if i < 16 and scheme_pages[i + 1] == pn else bottom(scheme, pn)
            regions.append(dict(p=pn, r=[0, round(sy if pn == sp else .025, 6), 1, round(lower, 6)]))
        result.append(dict(n=str(i + 1), label=f'Section {section} · Q{q}', printOrder=i + 1,
                           pP=pp, pY=[round(py, 6), round(pb if pe == pp else bottom(paper, pp), 6)],
                           endP=pe, endY=round(pb, 6), region=regions, conf=1.0, mode='crop'))
    return result


def apply():
    review = read(str(REVIEW.relative_to(ROOT)))
    assert review['manualPricedTasks'] == 38
    questions = anchors()
    old = read(f'scripts/paper-trail/answers/2017/{FILE}.json')
    assert [q['n'] for q in old['q']] == [q['n'] for q in questions] == [str(n) for n in range(1, 18)]
    sidecar = {**old, 'band': [1, 16], 'q': questions}
    for folder in ['scripts/paper-trail/answers', 'public/paper-answers']:
        write(f'{folder}/2017/{FILE}.json', sidecar)
    write(f'public/paper-anchors/2017/{FILE}.json', dict(v=1, paperOnly=1, paperFileid=FILE,
        schemeFileid='', component='', band=[1, 1], copyright=sidecar['copyright'],
        q=[{**{k: v for k, v in q.items() if k not in ['region', 'mode', 'conf']},
            'region': [dict(p=1)], 'mode': 'pagejump', 'conf': .5} for q in questions]))

    # Resolve the existing registry mapping; do not create a feature-local taxonomy.
    registry = (ROOT / 'data/examTopics/registry.ts').read_text()
    block = registry.split('const LINK_MODULES_CURRICULUM_CROSSWALK:', 1)[1].split('// These are assessment-format', 1)[0]
    crosswalk = {topic: re.findall(r"'([^']+)'", values) for topic, values in
                 re.findall(r"'([^']+)': \[([^\]]+)\]", block)}
    assert len(crosswalk) == 8
    inverse = {}
    for topic, nodes in crosswalk.items():
        for node in nodes:
            inverse.setdefault(node, []).append(topic)
    cards = [c for c in read('scripts/markbank/authored/lcvp.json') if c['year'] == 2017]
    canonical = {str(n): set() for n in range(1, 18)}
    topics = {str(n): set() for n in range(1, 18)}
    mappings = []
    for card in cards:
        match = re.search(r'Section ([ABC]) Q(\d+)', card['questionRef'])
        section, q = match.groups()
        n = str(int(q) + {'A': 0, 'B': 8, 'C': 11}[section])
        canonical[n].add(card['topicId'])
        targets = ([f'link-modules-common-{"audio-visual" if section == "A" else "case-study"}']
                   if section in ['A', 'B'] else inverse[card['topicId']])
        topics[n].update(targets)
        mappings.append(dict(id=card['id'], fileid=FILE, n=n, topicId=card['topicId'], atlasTopicIds=targets))
    assert len(mappings) == 38 and all(canonical.values())
    path = 'scripts/paper-trail/topic-tags/tags/link-modules.json'
    tags = read(path)
    prior = [p for p in tags if p['year'] == 2017 and p['fileid'] == FILE]
    assert len(prior) <= 1
    tagged = dict(subjectId='link-modules', level='common', lang='ev', year=2017, fileid=FILE, paperKey='single', q=[])
    for n, nodes in canonical.items():
        # Select representatives for the legacy two-field format without
        # changing card topics to fit it. Direct runtime retains all buckets.
        ordered = []
        represented = set()
        original_wave = review['originalAtlasMemberships']['canonicalWaveTopics'][n]
        for node in [v for v in original_wave if v in nodes] + sorted(nodes - set(original_wave)):
            targets = set(inverse[node])
            if not targets <= represented:
                ordered.append(node)
                represented.update(targets)
        # The legacy wave has only two fields. Full canonical membership is
        # retained below and every browse bucket is present in direct runtime.
        ordered = ordered[:2]
        tag = dict(n=n, primary=ordered[0])
        if len(ordered) > 1:
            tag['secondary'] = ordered[1]
        tagged['q'].append(tag)
    write(path, [tagged] + [p for p in tags if p not in prior], indent=1)

    runtime_path = 'data/examTopics/direct-question-runtime.json'
    runtime = read(runtime_path)
    other_subjects = deepcopy([r for r in runtime['subjects'] if r['subjectId'] != 'link-modules'])
    lane = next(r for r in runtime['subjects'] if r['subjectId'] == 'link-modules')
    existing = {r[5]: r for r in lane['questionMappings'] if r[:5] == ['common', 'ev', 2017, 'single', FILE]}
    assert set(existing) == set(review['originalAtlasMemberships']['existingRuntimeIds']) or set(existing) == set(topics)
    original_topics = read(str(REVIEW.relative_to(ROOT)))['originalAtlasMemberships']['questionTopicIds']
    assert set(original_topics) <= set(topics)
    for n in sorted(set(topics) - set(existing), key=int):
        row = ['common', 'ev', 2017, 'single', FILE, n, []]
        lane['questionMappings'].append(row)
        existing[n] = row
    for n, target_topics in topics.items():
        # Retain pre-lane memberships, not superseded uncommitted draft tags.
        existing[n][6] = sorted({lane['topicIds'].index(t)
                                 for t in set(original_topics.get(n, [])) | target_topics})
    assert other_subjects == [r for r in runtime['subjects'] if r['subjectId'] != 'link-modules']
    write(runtime_path, runtime)
    local_path = 'data/examTopics/link-modules-local-crosswalk.json'
    local = read(local_path)
    local['reviewedEnglish2017'] = dict(review=str(REVIEW.relative_to(ROOT)), paperFileid=FILE,
        sourceLeaves=38, rawReaderLeaves=38, practiceTasks=38, physicalQuestions=17, markBankMappings=mappings,
        originalAtlasTopicIds=original_topics,
        canonicalTopicIdsByQuestion={n: sorted(v) for n, v in canonical.items()},
        canonicalWavePolicy='Two representative legacy wave fields; full canonical nodes and actual Atlas browse memberships are retained in this crosswalk/direct runtime.',
        policy='All original 1–17 identities retained. Complete paper ranges and matching scheme regions reviewed; canonical content topics and original assessment-format Atlas buckets retained. Numeric scoring holds and native playback QA are separate from source/task coverage.')
    write(local_path, local)
    print('LCVP 2017: all 17 original sidecar/runtime identities retained; 38 complete tasks mapped; non-LCVP records unchanged.')


if __name__ == '__main__':
    import sys
    if '--preview' in sys.argv:
        print(json.dumps(anchors(), ensure_ascii=False, indent=2))
    else:
        apply()
