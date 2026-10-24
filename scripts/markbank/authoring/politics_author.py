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


def lifted_question(task, rule):
    """The printed question, line for line.

    Only three things may happen to the extracted paper lines: lines that
    belong to a graphic beside the question (named in the reviewed rule, or
    outside its kept line ranges) are dropped, a printed bullet glyph is
    normalised, and the PDF's line wraps are re-flowed so the question reads as
    the paper prints it on a phone. No word is added or reordered; the final
    assertion proves it against the extracted text.
    """
    return lift_lines(task['stem'] if rule.get('fromStem') else task['text'], rule, task['key'])


def lift_lines(source, rule, key):
    """Printed lines, with graphic labels dropped and line wraps re-flowed."""
    lines = readable(source, True).splitlines()
    if rule.get('keep'):
        lines = [line for start, end in rule['keep'] for line in lines[start:end]]
    for line in rule.get('dropLines', []):
        assert line in lines, ('Stale dropped graphic line', key, line)
    lines = [line for line in lines if line not in rule.get('dropLines', [])]
    lines = [re.sub(r'^o (?=[A-Z])', '• ', line) if rule.get('bulletO') else line for line in lines]
    flowed = []
    for line in lines:
        if flowed and flowed[-1] in ('•', '∗'):
            flowed[-1] += ' ' + line            # a bullet glyph extracted onto its own line
        elif (flowed and (len(flowed[-1]) >= 40 or line[:1].islower()) and not re.search(r'[.?!:]$', flowed[-1])
              and not line.startswith(('•', '∗'))):
            # A wrapped sentence, not a printed list item; a word hyphenated
            # across the line break ("socio-" / "economic") rejoins unspaced.
            flowed[-1] += ('' if flowed[-1].endswith(('-', '‐')) else ' ') + line
        else:
            flowed.append(line)
    text = '\n'.join(flowed)
    assert re.sub(r'\s+', '', text) == re.sub(r'\s+', '', ''.join(lines)), ('Question wording changed', key)
    return text


def tokens(text):
    return re.findall(r'[a-z0-9]+', clean(text).casefold().replace('’', "'"))


def unprinted(text, page_text):
    """Lines, list items or clauses of a question whose words are not printed, in order."""
    hay = ' ' + ' '.join(tokens(page_text)) + ' '
    segments = [segment for segment in re.split(r'\n|;|:\s|•', text) if tokens(segment)]
    return [segment.strip() for segment in segments if ' ' + ' '.join(tokens(segment)) + ' ' not in hay]


def scheme_labels(text):
    """Re-join a scheme label printed in its own column ("EU:") with its wording."""
    lines = text.splitlines()
    result = []
    for line in lines:
        if result and re.fullmatch(r'[A-Z]{2,6}:', result[-1]):
            result[-1] += ' ' + line
        else:
            result.append(line)
    return '\n'.join(result)


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
        lift = review.get('liftedPrompts', {}).get(unit['key'])
        if lift is not None:
            assert unit['key'] not in review.get('promptOverrides', {}), ('Lifted and overridden', unit['key'])
        if lift is not None:
            task['stem'] = unit.get('stem', '')
            task['prompt'] = lifted_question(task, lift)
            if lift.get('focus'):
                assert lift['focus'] in task['text'], ('Unprinted focus label', unit['key'])
                task['practiceFocus'] = lift['focus']
        task['stem'] = review.get('stemOverrides', {}).get(unit['key'], review.get('stemOverrides', {}).get(parent_key, readable(unit.get('stem', ''), True)))
        stem_rule = review.get('liftedStems', {}).get(unit['key'], review.get('liftedStems', {}).get(parent_key))
        if stem_rule is not None:
            assert unit['key'] not in review.get('stemOverrides', {}) and parent_key not in review.get('stemOverrides', {}), unit['key']
            source = next(u['text'] for u in units if u['key'] == stem_rule['from']) if stem_rule.get('from') else unit.get('stem', '')
            task['stem'] = lift_lines(source, stem_rule, unit['key'])
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
                child['splitFamily'] = unit['key']
                child['allocation'] = [task['allocation'][i] for i in split['criteria']]
                child['marks'] = sum(m for _, m in child['allocation'])
                tasks.append(child)
        else:
            tasks.append(task)
    # Choice is not a route. When the candidate chooses which N of M printed
    # items to answer, every Politics scheme marks the choice with one shared
    # grid, so the task stays ONE card: the printed question with its whole
    # list, and N slot criteria at the scheme's per-slot tariff. Writing a card
    # per option or per combination rewrote the SEC wording and put the same
    # question in a session up to 286 times (2023 OL Q2(d)). Split routes only
    # where a scheme marks them differently; none in this corpus does.
    assert 'finiteRoutes' not in review, 'Retired: route expansion; declare choices instead'
    expanded = []
    used_rules = set()
    for task in tasks:
        key = task['key'] + ('#' + task['suffix'] if task.get('suffix') else '')
        rule = review.get('choices', {}).get(key)
        if rule:
            assert clean(rule['cue']) in clean(task['text']), ('Stale choice cue', key)
            evidence_text = clean(task['text'])
            if task['parentKey'] in matches:
                evidence_text += ' ' + clean(matches[task['parentKey']]['text'])
            if rule.get('sourceEvidence'):
                evidence = rule['sourceEvidence']
                page = clean(fitz.open(ROOT / draft['source']['papers']['path'])[evidence['page'] - 1].get_text())
                assert clean(evidence['text']) in page, ('Stale source choice pool', key)
                evidence_text += ' ' + page
            # Every pool item is printed on the paper or named by the scheme.
            for _, label in rule['pool']:
                assert clean(label).lower() in evidence_text.lower(), ('Unprinted pool item', key, label)
            assert 0 < rule['choose'] < len(rule['pool']), key
            assert rule['choose'] == 1 or len(task['allocation']) == rule['choose'], ('One slot per chosen item', key)
            if rule.get('instruction'):
                assert clean(rule['instruction']) in clean(task['text']), ('Unprinted choice instruction', key)
            if not task.get('suffix'):
                assert task['key'] not in review.get('promptOverrides', {}), ('Choice question must be lifted', key)
                task['prompt'] = lifted_question(task, rule)
            task['choice'] = {'key': key, 'choose': rule['choose'], 'poolSize': len(rule['pool']),
                              'pool': [label for _, label in rule['pool']], 'instruction': rule.get('instruction')}
            used_rules.add(key)
            if rule.get('topicGroups'):
                # Options under different syllabus topics file under their own
                # Atlas headings (AGENTS.md): one card per topic, never per option
                # within one topic. The question text stays the printed one.
                assert rule['choose'] == 1 and not task.get('suffix'), key
                labels = [label for _, label in rule['pool']]
                assert sorted(o for g in rule['topicGroups'] for o in g['options']) == sorted(labels), key
                assert len({g['topic'] for g in rule['topicGroups']}) == len(rule['topicGroups']) > 1, key
                for group in rule['topicGroups']:
                    card = deepcopy(task)
                    card['suffix'], card['focus'], card['topic'] = group['id'], ' or '.join(group['options']), group['topic']
                    card['choice'] = {**task['choice'], 'topicGroup': group['options']}
                    expanded.append(card)
                continue
        expanded.append(task)
    assert used_rules == set(review.get('choices', {})), ('Stale choice rule', set(review.get('choices', {})) - used_rules)
    for task in expanded:
        key = task['key'] + ('#' + task['suffix'] if task.get('suffix') else '')
        task['topic'] = review.get('topicOverrides', {}).get(key, task['topic'])
    # Lift never write: every question is the paper's own wording. A split
    # whose printed boundary has no sentence of its own shows the printed
    # question with the separately priced part named as its practice focus.
    with fitz.open(ROOT / draft['source']['papers']['path']) as doc:
        page_text = {task['key']: ' '.join(doc[p - 1].get_text() for p in task['pages']) for task in expanded}
    families = {}
    for task in expanded:
        if task.get('splitFamily'):
            families.setdefault(task['splitFamily'], []).append(task)
    for family, children in families.items():
        if any(unprinted(child['prompt'], page_text[child['key']]) for child in children):
            for child in children:
                child['prompt'] = lifted_question(child, review.get('liftedPrompts', {}).get(family, {}))
                child['practiceFocus'] = child['focus']
    for task in expanded:
        allowed = review.get('visualTranscriptions', {}).get(task['key'], [])
        for line in allowed:
            assert line in task['prompt'], ('Stale visual transcription', task['key'])
        missing = [segment for segment in unprinted(task['prompt'], page_text[task['key']]) if segment not in allowed]
        assert not missing, ('Question not as printed', draft['source']['year'], draft['source']['level'], task['key'], missing)
        # The lead-in shown above the question is printed wording as well.
        missing = unprinted(task['stem'], page_text[task['key']])
        assert not missing, ('Stem not as printed', draft['source']['year'], draft['source']['level'], task['key'], missing)
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
        if task.get('choice'):
            guidance = [scheme_labels(guidance[0])]
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
        **({'practiceFocus': task['practiceFocus']} if task.get('practiceFocus') else {}),
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
        'rubric': {'system': 'politics', 'taskRequirements': ([task['focus']] if task.get('focus') else []) + ([task['choice']['instruction']] if task.get('choice', {}).get('instruction') else []),
                   'criteria': criteria, 'schemeGuidance': guidance, 'markingGuideNote': note,
                   'schemePages': scheme_pages, 'schemeFileid': src['schemes']['fileid']},
        '_audit': {'paperKey': task['key'], 'parentKey': task['parentKey'], 'paperPages': pages,
                   'paperTextSha256': hashlib.sha256(task['text'].encode()).hexdigest(),
                   'split': task.get('suffix'), 'choice': task.get('choice')},
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
