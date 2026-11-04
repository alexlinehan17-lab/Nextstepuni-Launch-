#!/usr/bin/env python3
"""Reconcile independent English paper, scheme and selection review gates."""
from __future__ import annotations

import argparse
import json

from english_complete import ROOT, inventory
from english_choices import review
from english_raw_selection import scan, reconcile as reconcile_raw
from english_task_review import reconcile as reconcile_schemes


AUTHORED = ROOT / 'scripts/markbank/authored'


def read(name):
    return json.loads((AUTHORED / name).read_text())


def check_visual(records, tasks, routes, ledger):
    by_id = {entry['paperId']: entry for entry in ledger['papers']}
    if set(by_id) != {record['id'] for record in records} or len(by_id) != len(ledger['papers']):
        raise ValueError('Visual ledger must cover every paper exactly once')
    pending = []
    for record in records:
        key = record['id']
        entry = by_id[key]
        if entry['paperSha256'] != record['questionPaper']['sha256'] or \
                entry['schemeSha256'] != record['markingScheme']['sha256']:
            raise ValueError('Visual review has stale sources: ' + key)
        pending.extend(key + ': ' + finding for finding in entry.get('openFindings', []))
        if not entry['visualSweepComplete']:
            pending.append(key + ': visual sweep')
            continue
        pages = entry['paperPagesInspected']
        if pages != list(range(1, record['questionPaper']['pages'] + 1)):
            raise ValueError('Claimed visual sweep omits/repeats pages: ' + key)
        tally = entry.get('independentPaperTally', {})
        if not tally.get('basis', '').strip():
            pending.append(key + ': independent paper tally')
        for name, values in ([('baseTasks', tasks), ('finiteRoutes', routes)] if tally else []):
            actual = sum(value['id'].startswith(key + '-') for value in values)
            if tally.get(name) != actual:
                raise ValueError(f'{key}: independent {name} tally differs ({tally.get(name)} vs {actual})')
        for flag in ('allTaskBoundariesSchemeChecked', 'allFiniteRoutesReconciled'):
            if not entry[flag]:
                pending.append(key + ': ' + flag)
    return pending


def check(tasks, *, strict=True):
    records = inventory()['papers']
    orphaned_context = set(read('english-task-context.json')['tasks']) - {task['id'] for task in tasks}
    if orphaned_context:
        raise ValueError('Orphaned reviewed task context: ' + ', '.join(sorted(orphaned_context)))
    decisions = read('english-selection-review.json')['decisions']
    routes, selection_pending = review(tasks, decisions)
    raw_pending, raw_tasks_pending = reconcile_raw(
        scan(records), records, read('english-raw-selection-review.json'), tasks, decisions)
    scheme_pending = reconcile_schemes(tasks, records, read('english-task-review.json'))
    visual_pending = check_visual(records, tasks, routes, read('english-visual-review.json'))
    report = {'papers': len(records), 'baseTasks': len(tasks), 'routes': len(routes),
              'pending': {'taskSelections': selection_pending, 'rawDirectives': raw_pending,
                          'rawLinkedTasks': raw_tasks_pending, 'schemeTasks': scheme_pending,
                          'paperReviews': visual_pending}}
    if strict and any(report['pending'].values()):
        raise ValueError('English publication refused: incomplete independent review gates')
    return report


def check_paper(record, tasks, *, strict=True):
    """Strict gate for ONE paper, independent of every other paper.

    Paper-by-paper shipping is approved, so a reviewed paper may publish while
    the corpus-wide gate still refuses because of other years. Every input is
    restricted to this paper: its freshly extracted tasks, its selection
    decisions, its raw directive hits and their ledger rows, its scheme
    reviews, its visual ledger entry and any reviewed context for its tasks.
    Nothing outside the paper can make it pass, and nothing inside can be
    skipped.
    """
    key = record['id']
    if any(not task['id'].startswith(key + '-') for task in tasks):
        raise ValueError('Paper gate received a task from another paper: ' + key)
    task_ids = {task['id'] for task in tasks}
    all_context = read('english-task-context.json')['tasks']
    orphaned = sorted(tid for tid in all_context if tid.startswith(key + '-') and tid not in task_ids)
    if orphaned:
        raise ValueError('Orphaned reviewed task context: ' + ', '.join(orphaned))

    all_decisions = read('english-selection-review.json')['decisions']
    decisions = {tid: decision for tid, decision in all_decisions.items() if tid.startswith(key + '-')}
    routes, selection_pending = review(tasks, decisions)

    raw_ledger = read('english-raw-selection-review.json')
    raw_subset = {
        'sources': {key: raw_ledger.get('sources', {}).get(key)} if key in raw_ledger.get('sources', {}) else {},
        'decisions': {hid: d for hid, d in raw_ledger.get('decisions', {}).items() if hid.startswith(key + '-p')},
    }
    hits = scan([record])
    raw_pending, raw_tasks_pending = reconcile_raw(hits, [record], raw_subset, tasks, decisions)
    if hits and raw_subset['sources'].get(key) != record['questionPaper']['sha256']:
        raw_pending = sorted(set(raw_pending) | {key + ': raw ledger not bound to this paper'})

    scheme_ledger = read('english-task-review.json')
    scheme_subset = {'tasks': {tid: d for tid, d in scheme_ledger['tasks'].items() if tid.startswith(key + '-')}}
    scheme_pending = reconcile_schemes(tasks, [record], scheme_subset)

    visual = read('english-visual-review.json')
    entries = [entry for entry in visual['papers'] if entry['paperId'] == key]
    if len(entries) != 1:
        raise ValueError('Visual ledger must hold this paper exactly once: ' + key)
    visual_pending = check_visual([record], tasks, routes, {'papers': entries})

    report = {'paperId': key, 'baseTasks': len(tasks), 'routes': len(routes),
              'pending': {'taskSelections': selection_pending, 'rawDirectives': raw_pending,
                          'rawLinkedTasks': raw_tasks_pending, 'schemeTasks': scheme_pending,
                          'paperReviews': visual_pending}}
    if strict and any(report['pending'].values()):
        raise ValueError('English paper refused by its own gate: ' + key)
    return report, routes


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', action='store_true')
    args = parser.parse_args()
    candidates = json.loads((ROOT / 'tmp/english-audit/all-candidates.json').read_text())
    if candidates['failures']:
        raise ValueError('Cannot review an incomplete candidate extraction')
    report = check(candidates['tasks'], strict=not args.report)
    (ROOT / 'tmp/english-audit/review-gate-report.json').write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({**{k: v for k, v in report.items() if k != 'pending'},
                      'pending': {k: len(v) for k, v in report['pending'].items()}}))


if __name__ == '__main__':
    main()
