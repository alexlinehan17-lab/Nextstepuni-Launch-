#!/usr/bin/env python3
"""Fail closed when a published English task lacks current scheme evidence."""
from __future__ import annotations

import hashlib
import json


def task_fingerprint(task):
    fields = ('id', 'questionText', 'questionRef', 'totalMarks', 'topicId',
              'parentQuestionText', 'contextNotes', 'sourceMaterial', 'additionalSourceMaterials')
    value = {key: task[key] for key in fields if key in task}
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                     separators=(',', ':')).encode()).hexdigest()


def reconcile(tasks, records, ledger):
    task_by_id = {task['id']: task for task in tasks}
    record_by_id = {record['id']: record for record in records}
    decisions = ledger.get('tasks', {})
    orphaned = set(decisions) - set(task_by_id)
    if orphaned:
        raise ValueError('Orphaned scheme task review: ' + ', '.join(sorted(orphaned)))
    for task_id, decision in decisions.items():
        task = task_by_id[task_id]
        paper_id = task_id.split('-p')[0] + '-p' + str(task['paper'])
        record = record_by_id[paper_id]
        if decision['taskSha256'] != task_fingerprint(task):
            raise ValueError('Stale scheme task review: ' + task_id)
        if decision['paperSha256'] != record['questionPaper']['sha256'] or \
                decision['schemeSha256'] != record['markingScheme']['sha256']:
            raise ValueError('Stale scheme source: ' + task_id)
        if decision['totalMarks'] != task['totalMarks']:
            raise ValueError('Scheme tariff differs from task: ' + task_id)
        if not decision.get('schemePages') or not decision.get('reason', '').strip():
            raise ValueError('Incomplete scheme evidence: ' + task_id)
        criteria = decision['criteria']
        if criteria['mode'] == 'holistic':
            if criteria.get('allocation'):
                raise ValueError('Holistic criteria cannot invent submarks: ' + task_id)
        elif criteria['mode'] in ('combined', 'discrete'):
            if sum(criteria['allocation'].values()) != task['totalMarks']:
                raise ValueError('Criteria allocation does not sum to tariff: ' + task_id)
        else:
            raise ValueError('Unknown criteria mode: ' + task_id)
    return sorted(set(task_by_id) - set(decisions))
