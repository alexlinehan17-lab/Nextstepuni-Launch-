#!/usr/bin/env python3
"""Publish reviewed deferred anchors and the emitted cards' canonical topics."""
import json
import re
from he_review_2023_hl import ROOT
from he_review_2023_hl_deferred import documents, a_regions
from he_atlas_2023_hl import read, write, physical_question_count

SUBJECT = 'home-economics-s-and-s'
FILE = 'LC098ALP014EV-deferred.pdf'


def apply():
    docs = documents()
    paper = a_regions(docs['a'], range(3, 8), body_bottom=730); scheme = a_regions(docs['scheme'], range(4, 8))
    def normalized(region, doc):
        page = doc[region['page'] - 1]
        x0, y0, x1, y1 = region['rect']
        return [round(x0 / page.rect.width, 6), round(y0 / page.rect.height, 6),
                round(x1 / page.rect.width, 6), round(y1 / page.rect.height, 6)]
    questions = []
    for n in range(1, 15):
        p, s = paper[n], scheme[n]
        pr = normalized(p, docs['a']); sr = normalized(s, docs['scheme'])
        questions.append(dict(n=str(n), label=f'Section A · Q{n}', printOrder=n, pP=p['page'], pY=[pr[1], pr[3]],
            endP=p['page'], endY=pr[3], region=[dict(p=s['page'], r=sr)], conf=1.0, mode='crop'))
    sidecar = dict(v=1, paperFileid=FILE, schemeFileid='LC098ALP000EV-deferred.pdf',
                   component='014', band=[1, 33], copyright='© State Examinations Commission', q=questions)
    for folder in ['scripts/paper-trail/answers', 'public/paper-answers']:
        write(f'{folder}/2023/{FILE}.json', sidecar)
    write(f'public/paper-anchors/2023/{FILE}.json', dict(v=1, paperOnly=1, paperFileid=FILE, schemeFileid='',
        component='014', band=[1, 1], copyright='© State Examinations Commission',
        q=[{**{k: v for k, v in q.items() if k not in ('region', 'mode', 'conf')},
            'region': [dict(p=1)], 'mode': 'pagejump', 'conf': 0.5} for q in questions]))

    index_path = ROOT / 'paperTrailData.ts'; index = index_path.read_text()
    pattern = r'^  "home-economics-s-and-s": \[\n(.*?)^  \]'
    match = re.search(pattern, index, re.M | re.S); assert match
    lines = match[1].splitlines(keepends=True); found = 0
    for i, line in enumerate(lines):
        entry = json.loads(line.strip().rstrip(','))
        if entry['year'] != 2023 or entry['level'] != 'higher' or entry['lang'] != 'ev': continue
        for p in entry['papers']:
            if p['doc']['f'] == FILE:
                p['answers'] = 1; found += 1
        if found:
            lines[i] = '    ' + json.dumps(entry, ensure_ascii=False, separators=(',', ':')) + ',\n'
    assert found == 1
    index_path.write_text(index[:match.start(1)] + ''.join(lines) + index[match.end(1):])

    crosswalk = read(f'data/examTopics/{SUBJECT}-curriculum-crosswalk.json')
    node_topics = {}
    for topic, nodes in crosswalk.items():
        if '-higher-' in topic:
            for node in nodes: node_topics.setdefault(node, []).append(topic)
    deck = (ROOT / 'components/MarkBank/cards/home-economics/higher.ts').read_text()
    mappings = []
    canonical = {str(n): set() for n in range(1, 15)}
    for chunk in re.split(r'^\s*\.\.\.base,', deck, flags=re.M)[1:]:
        cid = re.search(r'\bid: "([^"]+)"', chunk).group(1)
        if not cid.startswith('he-2023-hl-deferred-sa-'): continue
        ref = re.search(r'questionRef: "([^"]+)"', chunk).group(1)
        n = re.search(r'Q(\d+)', ref).group(1)
        node = re.search(r'topicId: "([^"]+)"', chunk).group(1)
        assert node in node_topics
        canonical[n].add(node)
        mappings.append(dict(id=cid, n=n, topicId=node, atlasTopicIds=node_topics[node]))
    assert len(mappings) == 15 and all(canonical.values())
    tags_path = f'scripts/paper-trail/topic-tags/tags/{SUBJECT}.json'; tags = read(tags_path)
    tags = [p for p in tags if not (p['year'] == 2023 and p['fileid'] == FILE)]
    tags.append(dict(subjectId=SUBJECT, paperKey='single', year=2023, level='higher', lang='ev', fileid=FILE,
        q=[dict(n=str(n), primary=sorted(canonical[str(n)])[0]) for n in range(1, 15)]))
    write(tags_path, tags, indent=1)
    local_path = f'data/examTopics/{SUBJECT}-local-crosswalk.json'; local = read(local_path)
    topics_by_n = {n: {topic for node in nodes for topic in node_topics[node]} for n, nodes in canonical.items()}
    matched_deferred = 0
    for association in local['associations']:
        match = re.fullmatch(r'2023 - Deferred Exam Paper - Section A - Question (\d+)', association['heading'])
        if association['level'] != 'higher' or not match: continue
        n = match[1]; assert n in canonical
        association['targets'] = [dict(level='higher', lang='ev', year=2023, paperKey='single', fileid=FILE, n=n, label=f'Section A · Q{n}')]
        association['resolution'] = 'matched'; association.pop('reason', None)
        topics_by_n[n].add(association['topicId']); matched_deferred += 1
    assert matched_deferred == 14
    runtime_path = f'data/examTopics/{SUBJECT}-question-runtime.json'; runtime = read(runtime_path)
    runtime['questionMappings'] = [r for r in runtime['questionMappings'] if r[:5] != ['h', 'e', 2023, 'single', FILE]]
    runtime['questionMappings'] += [['h', 'e', 2023, 'single', FILE, str(n),
        sorted(runtime['topicIds'].index(topic) for topic in topics_by_n[str(n)]), 'deferred'] for n in range(1, 15)]
    write(runtime_path, runtime)
    local['summary']['exactRuntimeQuestionMappings'] = len(runtime['questionMappings'])
    local['summary']['localAnswerAnchoredPhysicalCards'] = physical_question_count()
    entries = [json.loads(line.strip().rstrip(',')) for line in lines]
    local['summary']['localAnswerAnchoredPaperVariants'] = sum(p.get('answers') == 1 for e in entries for p in e['papers'])
    matched = [a for a in local['associations'] if a['resolution'] == 'matched']
    blocked = [a for a in local['associations'] if a['resolution'] == 'source-blocked']
    local['summary'].update(matchedAssociations=len(matched), sourceBlockedAssociations=len(blocked),
        matchedLocalCardLinks=sum(len(a['targets']) for a in matched),
        sourceBlockedByReason={reason: sum(a['reason'] == reason for a in blocked) for reason in sorted({a['reason'] for a in blocked})})
    local['reviewedEnglish2023DeferredA'] = dict(paperFileid=FILE, physicalQuestions=14,
        review='scripts/markbank/authoring/home-economics/2023-hl-deferred-review.json',
        policy='15 practice tasks map to 14 printed Section A questions. Deferred identities are separate from main. B/C still open.', markBankMappings=mappings)
    write(local_path, local)
    print('2023 HL deferred: 14 Section A anchors; all 15 Mark Bank tasks mapped to canonical Atlas topics.')
    apply_b(docs, node_topics)


def b_heads(doc, pages):
    heads = {}
    for page in pages:
        for block in doc[page - 1].get_text('dict')['blocks']:
            for line in block.get('lines', []):
                text = ''.join(span['text'] for span in line['spans']).strip()
                match = re.fullmatch(r'Question\s+([1-5])', text)
                if match: heads[int(match[1])] = (page, line['bbox'][1] - 3)
    assert list(heads) == [1, 2, 3, 4, 5]
    return heads


def apply_b(docs, node_topics):
    file = 'LC098ALP039EV-deferred.pdf'
    ph = b_heads(docs['bc'], range(2, 5)); sh = b_heads(docs['scheme'], range(8, 18))
    questions = []
    for number in range(1, 6):
        paper_page, top = ph[number]; p = docs['bc'][paper_page - 1]
        bound = ph[number + 1][1] if number < 5 and ph[number + 1][0] == paper_page else 770
        bottom = min(bound, max(w[3] for w in p.get_text('words') if top <= w[1] and w[3] < bound) + 8)
        scheme_start, scheme_top = sh[number]
        scheme_end = sh[number + 1][0] - 1 if number < 5 else 17
        regions = []
        for page in range(scheme_start, scheme_end + 1):
            s = docs['scheme'][page - 1]
            start = scheme_top if page == scheme_start else 35
            end = max(w[3] for w in s.get_text('words') if w[3] < 775) + 8
            regions.append(dict(p=page, r=[0, round(start / s.rect.height, 6), 1, round(end / s.rect.height, 6)]))
        questions.append(dict(n=str(number), label=f'Section B · Q{number}', printOrder=number, pP=paper_page,
            pY=[round(top / p.rect.height, 6), round(bottom / p.rect.height, 6)], endP=paper_page,
            endY=round(bottom / p.rect.height, 6), region=regions, conf=1.0, mode='crop'))
    sidecar = dict(v=1, paperFileid=file, schemeFileid='LC098ALP000EV-deferred.pdf', component='039', band=[1, 33],
                   copyright='© State Examinations Commission', q=questions)
    for folder in ['scripts/paper-trail/answers', 'public/paper-answers']: write(f'{folder}/2023/{file}.json', sidecar)
    write(f'public/paper-anchors/2023/{file}.json', dict(v=1, paperOnly=1, paperFileid=file, schemeFileid='', component='039', band=[1, 1],
        copyright='© State Examinations Commission', q=[{**{k: v for k, v in q.items() if k not in ('region', 'mode', 'conf')},
        'region': [dict(p=1)], 'mode': 'pagejump', 'conf': 0.5} for q in questions]))
    index_path = ROOT / 'paperTrailData.ts'; index = index_path.read_text()
    match = re.search(r'^  "home-economics-s-and-s": \[\n(.*?)^  \]', index, re.M | re.S); assert match
    lines = match[1].splitlines(keepends=True)
    entries = [json.loads(line.strip().rstrip(',')) for line in lines]
    found = 0
    for i, entry in enumerate(entries):
        if entry['year'] != 2023 or entry['level'] != 'higher' or entry['lang'] != 'ev': continue
        for paper in entry['papers']:
            if paper['doc']['f'] == file:
                paper['answers'] = 1; found += 1
                lines[i] = '    ' + json.dumps(entry, ensure_ascii=False, separators=(',', ':')) + ',\n'
    assert found == 1
    index_path.write_text(index[:match.start(1)] + ''.join(lines) + index[match.end(1):])
    mappings = []; topics = {str(n): set() for n in range(1, 6)}
    canonical = {str(n): set() for n in range(1, 6)}
    deck = (ROOT / 'components/MarkBank/cards/home-economics/higher.ts').read_text()
    for chunk in re.split(r'^\s*\.\.\.base,', deck, flags=re.M)[1:]:
        cid = re.search(r'\bid: "([^"]+)"', chunk).group(1)
        match = re.fullmatch(r'he-2023-hl-deferred-sb-q([1-5])[a-e]', cid)
        if not match: continue
        n = match[1]
        node = re.search(r'topicId: "([^"]+)"', chunk).group(1)
        canonical[n].add(node); topics[n].update(node_topics[node]); mappings.append(dict(id=cid, n=n, topicId=node, atlasTopicIds=node_topics[node]))
    assert len(mappings) == 17 and all(canonical.values())
    tags_path = f'scripts/paper-trail/topic-tags/tags/{SUBJECT}.json'; tags = read(tags_path)
    tags = [p for p in tags if not (p['year'] == 2023 and p['fileid'] == file)]
    tagged = []
    for n, primary in [('1', '0-6'), ('2', '0-1'), ('3', '0-4'), ('4', '1-3'), ('5', '2-0')]:
        primary = 'home-economics-' + primary; assert primary in canonical[n]
        tag = dict(n=n, primary=primary); other = sorted(canonical[n] - {primary})
        if other: tag['secondary'] = other[0]
        tagged.append(tag)
    tags.append(dict(subjectId=SUBJECT, paperKey='single', year=2023, level='higher', lang='ev', fileid=file, q=tagged))
    write(tags_path, tags, indent=1)
    local_path = f'data/examTopics/{SUBJECT}-local-crosswalk.json'; local = read(local_path)
    matched_b = 0
    for association in local['associations']:
        match = re.fullmatch(r'2023 - Deferred Exam Paper - Section B - Question ([1-5]) - Part [A-E]', association['heading'])
        if association['level'] != 'higher' or not match: continue
        n = match[1]
        association['targets'] = [dict(level='higher', lang='ev', year=2023, paperKey='single', fileid=file, n=n, label=f'Section B · Q{n}')]
        association['resolution'] = 'matched'; association.pop('reason', None)
        topics[n].add(association['topicId']); matched_b += 1
    assert matched_b == 20
    runtime_path = f'data/examTopics/{SUBJECT}-question-runtime.json'; runtime = read(runtime_path)
    runtime['questionMappings'] = [r for r in runtime['questionMappings'] if r[:5] != ['h', 'e', 2023, 'single', file]]
    runtime['questionMappings'] += [['h', 'e', 2023, 'single', file, str(n), sorted(runtime['topicIds'].index(t) for t in topics[str(n)]), 'deferred'] for n in range(1, 6)]
    write(runtime_path, runtime)
    local['summary']['exactRuntimeQuestionMappings'] = len(runtime['questionMappings'])
    local['summary']['localAnswerAnchoredPhysicalCards'] = physical_question_count()
    local['summary']['localAnswerAnchoredPaperVariants'] = sum(p.get('answers') == 1 for e in entries for p in e['papers'])
    matched = [a for a in local['associations'] if a['resolution'] == 'matched']; blocked = [a for a in local['associations'] if a['resolution'] == 'source-blocked']
    local['summary'].update(matchedAssociations=len(matched), sourceBlockedAssociations=len(blocked),
        matchedLocalCardLinks=sum(len(a['targets']) for a in matched),
        sourceBlockedByReason={reason: sum(a['reason'] == reason for a in blocked) for reason in sorted({a['reason'] for a in blocked})})
    local.pop('reviewedEnglish2023DeferredB1', None)
    local['reviewedEnglish2023DeferredB'] = dict(paperFileid=file, physicalQuestions=5, review='scripts/markbank/authoring/home-economics/2023-hl-deferred-review.json',
        policy='All 17 Section B tasks across five printed questions. Section C still open.', markBankMappings=mappings)
    write(local_path, local)
    print('2023 HL deferred B: five original questions, full scheme anchors; all 17 tasks mapped.')


if __name__ == '__main__': apply()
