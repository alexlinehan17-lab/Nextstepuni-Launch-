#!/usr/bin/env python3
"""Compile reviewed Politics tasks. Production fails until the entire index is reviewed.

Paper and scheme groups are aligned by order and wording, using align.py's
scorer. Printed keys are retained as evidence, never used to choose the match.
All generated material can be checked against the original PDF in the UI.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
import hashlib
from itertools import combinations
import json
from pathlib import Path
import re

import fitz

from align import bag, score
from politics_corpus import ROOT, OUT, clean
from politics_reviewed import REVIEWED


def readable(text, question=False):
    rows = []
    for line in text.splitlines():
        line = clean(line).replace('\uf0d8', '•').replace('\uf0b7', '•').replace('\uf0a7', '•').replace('\uf050', '✓').replace('Ō', 'ft')
        if not line or re.fullmatch(r'\(?\d+\s*marks?\)?|\d+|[_.\s]+', line, re.I):
            continue
        if question and re.fullmatch(r'or|Optional space to help you prepare your answer\.?', line, re.I):
            continue
        if question and (line.startswith(('http://', 'https://', 'www.')) or re.fullmatch(r'[^\s]+/[^\s]*', line) or re.fullmatch(r'[A-Za-z ]+(?:\d+)?:?\s*_{3,}', line)):
            continue
        if question and (re.match(r'^Source:\s*(?:https?://|www\.)', line) or re.fullmatch(r'\d+\.\s*_{3,}', line)):
            continue
        if question and re.fullmatch(r'(?:First|Second|Third) (?:piece|description|point|reason|challenge|cause|impact|function|way|action|initiative|department):?|(?:Cause|Reason|Process) \d+:|Key piece of (?:data|information):|Argument (?:for|against):|Name:|Explanation:|Description:|Example:|Theorist:|Theory:|Work:|Role:|Answer', line, re.I):
            continue
        line = re.sub(r'_{3,}', '_____', line)
        rows.append(line)
    return '\n'.join(rows)


def groups(units):
    result = []
    for unit in units:
        key = re.sub(r'\([ivx]+\)$', '', unit['key']) if unit['roman'] else unit['key']
        # A bare question letter (i) is not a roman numeral.
        if result and result[-1]['key'] == key:
            result[-1]['units'].append(unit)
        else:
            result.append({'key': key, 'section': unit['section'], 'units': [unit]})
    for group in result:
        group['text'] = '\n'.join(unit['text'] for unit in group['units'])
        group['pages'] = sorted({p for unit in group['units'] for p in unit['pages']})
    return result


def ordered_pairs(papers, schemes):
    """Needleman–Wunsch with the same content-word scorer as align_ordered.

    No question key or page position participates in the score.
    """
    n, m = len(papers), len(schemes)
    gap = -.1
    matrix = [[0.] * (m + 1) for _ in range(n + 1)]
    back = {}
    for i in range(1, n + 1):
        matrix[i][0] = i * gap
    for j in range(1, m + 1):
        matrix[0][j] = j * gap
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            overlap = score(bag(papers[i-1]['text']), bag(schemes[j-1]['text']))
            options = [(matrix[i-1][j-1] + overlap, 'pair'),
                       (matrix[i-1][j] + gap, 'paper'), (matrix[i][j-1] + gap, 'scheme')]
            matrix[i][j], back[i, j] = max(options, key=lambda item: item[0])
    i, j, pairs, open_paper, open_scheme = n, m, [], [], []
    while i or j:
        step = back.get((i, j), 'paper' if i else 'scheme')
        if step == 'pair':
            p, s = papers[i-1], schemes[j-1]
            pairs.append((p, s, round(score(bag(p['text']), bag(s['text'])), 4)))
            i, j = i - 1, j - 1
        elif step == 'paper':
            open_paper.append(papers[i-1]['key'])
            i -= 1
        else:
            open_scheme.append(schemes[j-1]['key'])
            j -= 1
    return list(reversed(pairs)), open_paper, open_scheme


def group_pairs(draft, review):
    papers = [g for g in groups(draft['paper']['units']) if g['section'] != 'C']
    schemes = groups(draft['scheme']['units'])
    pairs, unmatched_papers, unmatched_schemes = ordered_pairs(papers, schemes)
    assert not unmatched_papers and not unmatched_schemes, (draft['source']['year'], unmatched_papers, unmatched_schemes)
    result, evidence = {}, []
    for paper, scheme, confidence in pairs:
        manual = review.get('alignmentReviews', {}).get(paper['key'])
        if confidence < .3 and not manual:
            print('READ alignment:', draft['source']['year'], draft['source']['level'], paper['key'], scheme['key'], confidence)
        # A reviewed physical-page match must contain a real cue from each PDF.
        if manual:
            assert clean(manual['paper']) in clean(paper['text']), (paper['key'], 'stale paper cue')
            assert clean(manual['scheme']) in clean(scheme['text']), (paper['key'], 'stale scheme cue')
        result[paper['key']] = scheme
        evidence.append({'paper': paper['key'], 'scheme': scheme['key'], 'score': confidence,
                         'paperPages': paper['pages'], 'schemePages': scheme['pages'],
                         'review': manual, 'status': 'paired' if confidence >= .3 or manual else 'READ'})
    return result, evidence


def build_tasks(draft, review, matches):
    """Expand the reviewed boundary map, retaining a link to its paper parent."""
    units = draft['paper']['units']
    paper_groups = {g['key']: g for g in groups(units)}
    merged = set(review.get('mergeParts', []))
    tasks = []
    for unit in units:
        parent_key = re.sub(r'\([ivx]+\)$', '', unit['key']) if unit['roman'] else unit['key']
        if unit.get('contextOnly') and parent_key not in merged:
            continue
        if unit['roman'] and parent_key in merged:
            continue
        task = deepcopy(unit)
        if parent_key in merged:
            task['text'] = paper_groups[parent_key]['text']
            task['pages'] = paper_groups[parent_key]['pages']
        task['parentKey'] = parent_key
        task['prompt'] = review.get('promptOverrides', {}).get(unit['key'], readable(task['text'], True))
        task['stem'] = review.get('stemOverrides', {}).get(unit['key'], review.get('stemOverrides', {}).get(parent_key, readable(unit.get('stem', ''), True)))
        if task['section'] == 'C':
            task['marks'] = sum(c['maxMarks'] for c in draft['essay']['criteria'])
            task['topic'] = review['essayTopics'][unit['key']]
        elif task['section'] == 'A':
            task['marks'] = review.get('partMarks', {}).get(unit['key'], review['shortMarks'])
            task['topic'] = review['shortTopics'][ord(unit['part']) - ord('a')]
            assert not unit['roman'] or unit['key'] in review.get('partMarks', {}), ('Unpriced child', unit['key'])
        else:
            task['marks'] = review.get('partMarks', {}).get(unit['key'], review['dataMarks'][str(unit['q'])][ord(unit['part'])-ord('a')])
            task['topic'] = review['dataTopics'][str(unit['q'])]
        task['topic'] = review.get('topicOverrides', {}).get(unit['key'], task['topic'])
        task['allocation'] = review.get('criterionAllocations', {}).get(unit['key'], [('Complete response', task['marks'])])
        assert sum(m for _, m in task['allocation']) == task['marks'], unit['key']
        # Each split has its exact task wording and explicit selection of the
        # already reviewed scheme components; it cannot silently drop marks.
        splits = review.get('splits', {}).get(unit['key'])
        if splits:
            assert sorted(i for split in splits for i in split['criteria']) == list(range(len(task['allocation']))), unit['key']
            for split in splits:
                child = deepcopy(task)
                child['suffix'] = split['id']
                child['focus'] = split['label']
                child['prompt'] = split['prompt']
                child['allocation'] = [task['allocation'][i] for i in split['criteria']]
                child['marks'] = sum(m for _, m in child['allocation'])
                tasks.append(child)
        else:
            tasks.append(task)
    expanded = []
    used_rules = set()
    for task in tasks:
        key = task['key'] + ('#' + task['suffix'] if task.get('suffix') else '')
        rule = review.get('finiteRoutes', {}).get(key)
        if not rule:
            expanded.append(task)
            continue
        assert clean(rule['cue']) in clean(task['text']), ('Stale route cue', key)
        if rule.get('sourceEvidence'):
            evidence = rule['sourceEvidence']
            page = fitz.open(ROOT / draft['source']['papers']['path'])[evidence['page'] - 1]
            assert clean(evidence['text']) in clean(page.get_text()), ('Stale source route pool', key)
        assert 0 < rule['choose'] <= len(rule['pool'])
        used_rules.add(key)
        for chosen in combinations(rule['pool'], rule['choose']):
            route = deepcopy(task)
            route['suffix'] = '-'.join(filter(None, [task.get('suffix'), *[item[0] for item in chosen]]))
            route['focus'] = ' / '.join(item[1] for item in chosen)
            route['prompt'] = rule['prompt'].replace('{selection}', ' and '.join(item[1] for item in chosen))
            route['route'] = {'key': key, 'options': [item[0] for item in chosen], 'choose': rule['choose'], 'poolSize': len(rule['pool'])}
            expanded.append(route)
    assert used_rules == set(review.get('finiteRoutes', {})), ('Stale route rule', used_rules)
    for task in expanded:
        key = task['key'] + ('#' + task['suffix'] if task.get('suffix') else '')
        task['topic'] = review.get('topicOverrides', {}).get(key, task['topic'])
    return expanded


def card_for(task, draft, review, matches):
    src = draft['source']
    year, level = src['year'], src['level']
    code = 'hl' if level == 'higher' else 'ol'
    ref = f'{year} {code.upper()} Q{task["key"]}'
    if task.get('suffix'):
        ref += ' — ' + task['focus']
    identity = re.sub(r'[^a-z0-9-]', '-', task['key']).strip('-')
    identity = re.sub('-+', '-', identity)
    card_id = f'politics-{year}-{code}-q{identity}' + ('-' + task['suffix'] if task.get('suffix') else '')
    if task['section'] == 'C':
        criteria = deepcopy(draft['essay']['criteria'])
        scheme_pages = [draft['essay']['page'], draft['essay']['page'] + 1]
        guidance = []
    else:
        scheme = matches[task['parentKey']]
        scheme_pages = scheme['pages']
        guidance = [readable(scheme['text'])]
        criteria = [{'id': f'criterion-{i+1}', 'label': name, 'maxMarks': marks,
                     'permittedMarks': review.get('permittedMarks', {}).get(task['key'], {}).get(name, list(range(marks+1))), 'guidance': []}
                    for i, (name, marks) in enumerate(task['allocation'])]
    pages = sorted(set(task['pages'] + task.get('contextPages', [])))
    if task['section'] == 'B':
        pages = sorted(set(review['sourcePages'] + pages))
    note = 'The published suggestions and examples are not exhaustive. Compare your response with the scheme and apply its stated allocations and quality descriptors. Other valid responses remain creditable.'
    if task['section'] == 'A' and review.get('shortMarkNote'):
        note += ' ' + review['shortMarkNote']
    if task['key'] in review.get('markNotes', {}):
        note += ' ' + review['markNotes'][task['key']]
    return {
        'id': card_id, 'subjectId': 'politics-and-society', 'source': 'sec', 'kind': 'rubric',
        'year': year, 'level': level, 'section': task['section'], 'questionRef': ref,
        'topicId': 'politics-and-society-' + task['topic'],
        'conceptId': 'politics-and-society-' + task['topic'],
        'paperFileid': src['paperFileid'], 'questionText': task['prompt'], 'stem': task['stem'],
        'totalMarks': task['marks'], 'specVersion': 'politics-and-society:current',
        'schemeCitation': f'SEC Politics and Society {year}, {level.title()} Level marking scheme, pp. {", ".join(map(str, scheme_pages))}. © State Examinations Commission.',
        'sourceMaterial': {
            'kind': 'source-data', 'label': 'Documents and original question' if task['section'] == 'B' else 'Original question and graphics',
            'title': ref, 'pages': pages,
            'attribution': '© State Examinations Commission',
            'presentationNote': 'Read the original examination pages, including any documents, charts, quotations and illustrations used by this question.',
        },
        'qa': {'gates': ['paper-scheme-visual-review', 'wording-order-alignment', 'published-tariff'],
               'humanReviewedBy': 'Codex source review; no human sign-off claimed', 'humanReviewedAt': '2026-10-07'},
        'rubric': {'system': 'politics', 'taskRequirements': [task['focus']] if task.get('focus') else [],
                   'criteria': criteria, 'schemeGuidance': guidance, 'markingGuideNote': note,
                   'schemePages': scheme_pages, 'schemeFileid': src['schemes']['fileid']},
        '_audit': {'paperKey': task['key'], 'parentKey': task['parentKey'], 'paperPages': pages,
                   'paperTextSha256': hashlib.sha256(task['text'].encode()).hexdigest(),
                   'split': task.get('suffix'), 'route': task.get('route')},
    }


def main():
    args = argparse.ArgumentParser()
    args.add_argument('--draft', action='store_true')
    options = args.parse_args()
    drafts = json.loads((OUT / 'draft-extraction.json').read_text())
    cards, ledger, pending = [], [], []
    for draft in drafts:
        src = draft['source']
        review = REVIEWED.get((src['year'], src['level']))
        if not review:
            pending.append([src['year'], src['level']])
            continue
        for doc in ['paper', 'scheme']:
            assert review[doc+'PagesReviewed'] == list(range(1, draft[doc]['pages']+1)), (src['year'], doc, 'Incomplete visual review')
        matches, alignment = group_pairs(draft, review)
        tasks = build_tasks(draft, review, matches)
        assert {section: sum(t['section'] == section for t in tasks) for section in 'ABC'} == review['reviewedTaskCounts'], (src['year'], src['level'], 'Visual task census differs from generated tasks')
        new_cards = [card_for(t, draft, review, matches) for t in tasks]
        cards += new_cards
        ledger.append({'year': src['year'], 'level': src['level'], 'alignment': alignment,
                       'cardIds': [c['id'] for c in new_cards], 'decisions': review['boundaryNotes']})
    assert len({c['id'] for c in cards}) == len(cards), 'Duplicate card IDs'
    result = {'v': 1, 'subjectId': 'politics-and-society', 'pendingPapers': pending, 'ledger': ledger, 'cards': cards}
    (OUT / 'authored-draft.json').write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
    print('Reviewed drafts:', len(ledger), 'Pending indexed papers:', len(pending), 'Draft tasks:', len(cards))
    if not options.draft:
        assert not pending, 'Cannot publish an incomplete paper review'
        assert all(p['status'] == 'paired' for entry in ledger for p in entry['alignment']), 'Unreviewed alignments'
        from politics_audit import verify
        page_count, signal_count = verify(drafts)
        destination = ROOT / 'components/MarkBank/cards/politics-and-society'
        destination.mkdir(parents=True, exist_ok=True)
        shipped = [{k:v for k,v in c.items() if k != '_audit'} for c in cards]
        (destination / 'authored.json').write_text(json.dumps({'v':1, 'cardCount':len(cards), 'cards':shipped}, ensure_ascii=False, indent=2)+'\n')
        audit = ROOT / 'scripts/markbank/authored'
        (audit / 'politics-reconciliation.json').write_text(json.dumps({'sources':[d['source'] for d in drafts], 'rawSelectionPages':page_count, 'rawSelectionSignals':signal_count, 'papers':ledger, 'tasks':[{'id':c['id'], **c['_audit']} for c in cards]}, ensure_ascii=False, indent=2)+'\n')
        runtime = [{'id':c['id'], 'year':c['year'], 'level':c['level'], 'n':re.match(r'\d+',c['_audit']['paperKey']).group(), 'questionRef':c['questionRef'], 'topicId':c['topicId'], 'section':c['section'], 'fileid':c['paperFileid'], 'thinker':bool(re.search(r'thinker|theorist|Hobbes|Locke|Freire|Nussbaum|Lynch|Walby|Chomsky|Anderson|Eriksen|Said|Shiva|McDonagh|Gunder',c['questionText'],re.I))} for c in cards]
        (ROOT / 'data/examTopics/politics-tasks.json').write_text(json.dumps(runtime, ensure_ascii=False, separators=(',',':'))+'\n')
        print('Published reviewed corpus; raw choice scan:',page_count,'pages,',signal_count,'signals')


if __name__ == '__main__':
    main()
