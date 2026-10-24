#!/usr/bin/env python3
"""Independently scan every English PDF page for selection language.

This scan starts at the source PDF, not the extracted card list. Each hit
needs a source-bound decision: covered task IDs, an outer examination
instruction, source prose, or an explicitly explained non-selection.
Suggested matches are evidence for review, never automatic exemptions.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import unicodedata

import fitz

from english_complete import ROOT, inventory
from english_choices import DIRECTIVE, expand, fingerprint

LEDGER = ROOT / 'scripts/markbank/authored/english-raw-selection-review.json'


def normalise(value):
    value = unicodedata.normalize('NFKC', value).lower()
    return re.sub(r'[^\w]+', ' ', value).strip()


def raw_lines(page):
    """Use native PDF text lines independently of the card crop parser."""
    rows = []
    for block in page.get_text('dict')['blocks']:
        for line in block.get('lines', []):
            text = ''.join(span['text'] for span in line['spans']).strip()
            if text:
                rows.append({'text': text, 'x': line['bbox'][0] / page.rect.width,
                             'y': line['bbox'][1] / page.rect.height})
    return sorted(rows, key=lambda row: (round(row['y'], 3), row['x']))


def hits_for_rows(paper_id, page, rows, origin='pdf'):
    hits = []
    for index, row in enumerate(rows):
        if not DIRECTIVE.search(row['text']):
            continue
        context = '\n'.join(r['text'] for r in rows[max(0, index - 2):index + 3])
        digest = fingerprint(row['text'])
        hits.append({
            'id': f'{paper_id}-p{page}-{origin}-{index + 1}-{digest[:12]}',
            'paperId': paper_id, 'page': page, 'origin': origin,
            'text': row['text'], 'textSha256': digest,
            'context': context, 'contextSha256': fingerprint(context),
            'x': round(row['x'], 5), 'y': round(row['y'], 5),
        })
    return hits


def scan(records):
    repairs = json.loads((ROOT / 'scripts/markbank/authored/english-paper-text-repairs.json').read_text())
    hits = []
    for record in records:
        source = record['questionPaper']
        if hashlib.sha256((ROOT / source['path']).read_bytes()).hexdigest() != source['sha256']:
            raise ValueError('Source changed during raw scan: ' + record['id'])
        with fitz.open(ROOT / source['path']) as doc:
            for number, page in enumerate(doc, 1):
                hits.extend(hits_for_rows(record['id'], number, raw_lines(page)))
        # Retain the raw scan above even for damaged PDFs. Scan the independently
        # reviewed repair as well so unreadable glyph encoding cannot hide a choice.
        for repair in repairs:
            if repair['source'] != source['path']:
                continue
            if repair['sha256'] != source['sha256']:
                raise ValueError('Raw scan has a stale text repair: ' + record['id'])
            for page, text in repair['pages'].items():
                rows = [{'text': line, 'x': 0, 'y': 0} for line in text.splitlines() if line.strip()]
                hits.extend(hits_for_rows(record['id'], int(page), rows, 'repair'))
    if len({hit['id'] for hit in hits}) != len(hits):
        raise ValueError('Repeated raw source directive identity')
    return hits


def suggested_tasks(hit, tasks):
    text = re.sub(r'^\s*(?:[1-9]\.|\([a-ziv]+\))\s*', '', hit['text'], flags=re.I)
    text = re.sub(r'\(\s*\d+\s*(?:marks?)?\s*\)\s*$', '', text, flags=re.I)
    phrase = normalise(text)
    if len(phrase.split()) < 4:
        return []
    result = []
    for task in tasks:
        if not task['id'].startswith(hit['paperId'] + '-'):
            continue
        if not any(region['p'] == hit['page'] and
                   (hit['origin'] == 'repair' or region['r'][1] - .01 <= hit['y'] < region['r'][3])
                   for region in task.get('paperRegion', [])):
            continue
        if phrase in normalise(task['rawQuestionText']):
            result.append(task['id'])
    return result


def reconcile(hits, records, ledger, tasks, task_decisions):
    sources = {r['id']: r['questionPaper']['sha256'] for r in records}
    for paper_id, sha in ledger.get('sources', {}).items():
        if sources.get(paper_id) != sha:
            raise ValueError('Raw selection ledger has a stale source: ' + paper_id)
    by_id = {hit['id']: hit for hit in hits}
    decisions = ledger.get('decisions', {})
    orphaned = set(decisions) - set(by_id)
    if orphaned:
        raise ValueError('Raw selection decisions no longer match the paper: ' + ', '.join(sorted(orphaned)))
    task_by_id = {task['id']: task for task in tasks}
    unreviewed, pending_tasks = [], set()
    for hit in hits:
        decision = decisions.get(hit['id'])
        if not decision:
            unreviewed.append(hit['id'])
            continue
        if ledger.get('sources', {}).get(hit['paperId']) != sources[hit['paperId']]:
            raise ValueError('Raw decision has no bound paper source: ' + hit['id'])
        if any(decision.get(key) != hit[key] for key in ('textSha256', 'contextSha256')):
            raise ValueError('Raw decision wording/context changed: ' + hit['id'])
        if not decision.get('reason', '').strip():
            raise ValueError('Raw directive has no written reason: ' + hit['id'])
        kind = decision.get('kind')
        if kind == 'tasks':
            if not decision.get('taskIds'):
                raise ValueError('Raw directive has no covered tasks: ' + hit['id'])
            for task_id in decision['taskIds']:
                if task_id not in task_by_id or not task_id.startswith(hit['paperId'] + '-'):
                    raise ValueError('Raw directive points to an absent/wrong-paper task: ' + task_id)
                if decision.get('taskSha256', {}).get(task_id) != fingerprint(task_by_id[task_id]['questionText']):
                    raise ValueError('Raw directive task wording changed: ' + task_id)
                if task_id not in task_decisions:
                    pending_tasks.add(task_id)
                else:
                    expand(task_by_id[task_id], task_decisions[task_id])
        elif kind not in ('exam-instruction', 'source-prose', 'non-selection'):
            raise ValueError('Raw directive has an unknown classification: ' + hit['id'])
    return unreviewed, sorted(pending_tasks)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', action='store_true')
    args = parser.parse_args()
    records = inventory()['papers']
    candidates = json.loads((ROOT / 'tmp/english-audit/all-candidates.json').read_text())
    if candidates['failures']:
        raise SystemExit('Raw reconciliation refused: candidate extraction failures')
    task_decisions = json.loads((ROOT / 'scripts/markbank/authored/english-selection-review.json').read_text())['decisions']
    ledger = json.loads(LEDGER.read_text()) if LEDGER.exists() else {}
    hits = scan(records)
    unreviewed, pending = reconcile(hits, records, ledger, candidates['tasks'], task_decisions)
    tasks_by_paper = {r['id']: [t for t in candidates['tasks'] if t['id'].startswith(r['id'] + '-')] for r in records}
    for hit in hits:
        hit['suggestedTaskIds'] = suggested_tasks(hit, tasks_by_paper[hit['paperId']])
    out = ROOT / 'tmp/english-audit/raw-selection-report.json'
    out.write_text(json.dumps({'hits': hits, 'unreviewed': unreviewed, 'pendingTaskDecisions': pending}, ensure_ascii=False, indent=2) + '\n')
    print(f'{len(hits)} raw directive occurrences; {len(unreviewed)} unclassified; {len(pending)} linked tasks pending.')
    if (unreviewed or pending) and not args.report:
        raise SystemExit('Generation refused: raw paper selection directives are not reconciled')


if __name__ == '__main__':
    main()
