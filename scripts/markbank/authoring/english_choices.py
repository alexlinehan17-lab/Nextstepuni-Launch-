#!/usr/bin/env python3
"""Expand reviewed finite English pools, refusing unreviewed or stale wording.

This stage writes review candidates only. Paper/scheme boundaries, topic
parity and visual/source review remain separate publication gates.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
import hashlib
from itertools import combinations, product
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[3]
DIRECTIVE = re.compile(
    r'\b(?:choose|choice|select|either|or|any|following|which|'
    r'what (?:one|two|three|four)|'
    r'(?:one|two|three|four|five|six|seven|eight|nine|ten|\d+)\s+of|'
    r'answer (?:one|two|three|four|\d+) of)\b', re.I)


def fingerprint(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def expand(task, decision):
    if decision['questionSha256'] != fingerprint(task['questionText']):
        raise ValueError(task['id'] + ': reviewed question wording changed')
    if not decision.get('reason', '').strip():
        raise ValueError(task['id'] + ': missing written selection decision')
    if decision['kind'] != 'finite':
        if decision['kind'] not in ('open', 'flexible', 'required', 'context'):
            raise ValueError(task['id'] + ': unclassified selection directive')
        return [task]
    groups = []
    for pool in decision['pools']:
        options = pool['options']
        if len({option['id'] for option in options}) != len(options):
            raise ValueError(task['id'] + ': repeated pool option')
        if not 0 < pool['take'] <= len(options):
            raise ValueError(task['id'] + ': impossible selection size')
        groups.append(list(combinations(options, pool['take'])))
    routes = []
    for selection in product(*groups):
        keys = [option['id'] for group in selection for option in group]
        if decision.get('distinctAcrossPools') and len(set(keys)) < len(keys):
            continue
        route = deepcopy(task)
        components = [pool['id'] + '-' + '-'.join(option['id'] for option in choices)
                      for pool, choices in zip(decision['pools'], selection)]
        descriptions = [pool['label'] + ': ' + '; '.join(option['text'] for option in choices)
                        for pool, choices in zip(decision['pools'], selection)]
        route['id'] += '-route-' + '--'.join(components)
        route['choiceParentId'] = task['id']
        route['choiceRoute'] = {
            'label': ' · '.join(descriptions),
            'selections': {pool['id']: [option['id'] for option in choices]
                           for pool, choices in zip(decision['pools'], selection)},
        }
        route['questionText'] += '\n\nFor this practice response — ' + '. '.join(descriptions) + '.'
        route['questionRef'] += ' · ' + ' · '.join(descriptions)
        # The route retains the original published tariff and source/context.
        # Never multiply marks by the number of alternative routes.
        routes.append(route)
    if len(routes) != decision['expectedRoutes']:
        raise ValueError(f"{task['id']}: {len(routes)} routes, expected {decision['expectedRoutes']}")
    if len({route['id'] for route in routes}) != len(routes):
        raise ValueError(task['id'] + ': repeated route identity')
    return routes


def review(tasks, decisions):
    by_id = {task['id']: task for task in tasks}
    orphaned = sorted(set(decisions) - set(by_id))
    if orphaned:
        raise ValueError('Selection decisions no longer have a task: ' + ', '.join(orphaned))
    expanded, unreviewed = [], []
    for task in tasks:
        decision = decisions.get(task['id'])
        if decision:
            expanded.extend(expand(task, decision))
        elif DIRECTIVE.search(task['rawQuestionText']):
            unreviewed.append(task['id'])
        else:
            expanded.append(task)
    return expanded, unreviewed


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', action='store_true', help='Report open decisions without publishing anything.')
    args = parser.parse_args()
    candidates = json.loads((ROOT / 'tmp/english-audit/all-candidates.json').read_text())
    if candidates['failures']:
        raise SystemExit('Candidate extraction has unresolved papers')
    decisions = json.loads((ROOT / 'scripts/markbank/authored/english-selection-review.json').read_text())['decisions']
    routes, unreviewed = review(candidates['tasks'], decisions)
    print(f'{len(routes)} resolved candidate routes; {len(unreviewed)} unreviewed selection tasks.')
    out = ROOT / 'tmp/english-audit/selection-report.json'
    out.write_text(json.dumps({'routes': routes, 'unreviewed': unreviewed}, ensure_ascii=False, indent=2) + '\n')
    if unreviewed and not args.report:
        raise SystemExit('Generation refused: unclassified selection directives remain')


if __name__ == '__main__':
    main()
