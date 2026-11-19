"""Apply the current launch choice rule to the historical review declarations.

The original route declarations and their visual review remain reproducible.
Publication consolidates them at the printed mark boundary, before either the
review ledger or authored deck is written. The reviewed manifest records every
old identity, original prompt and alias; it never infers choices from ID names.
"""
import copy
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
POLICY = json.loads((ROOT / 'scripts/markbank/mathematics/choice-policy.json').read_text())
GROUPS = {g['canonicalId']: g for g in POLICY['groups']}
MEMBERS = {cid: g for g in POLICY['groups'] for cid in g['legacyIds']}
RETIRED = {cid for cid, g in MEMBERS.items() if cid != g['canonicalId']}


def consolidate(cards):
    """Fail closed on changed declarations, then publish one free-choice task."""
    present = {c['id'] for c in cards}
    if len(present) != len(cards):
        raise ValueError('duplicate historical task identity')
    for g in POLICY['groups']:
        members = present.intersection(g['legacyIds'])
        if not members:
            continue
        # Re-application to an already consolidated ledger is idempotent.
        if members == {g['canonicalId']} and any(c.get('selectionChoice') for c in cards if c['id'] in members):
            continue
        if members != set(g['legacyIds']):
            raise ValueError(f"{g['canonicalId']}: historical choice declaration lost a route")
        legacy = {c['id']: c for c in g['legacyCards']}
        for c in cards:
            if c['id'] not in members:
                continue
            for key in ('printedParts', 'totalMarks', 'scale', 'components', 'methods', 'topicId', 'examTopicIds', 'sourcePages', 'schemePages', 'selectionVariant'):
                if c.get(key) != legacy[c['id']].get(key):
                    raise ValueError(f"{c['id']}: reviewed choice changed in {key}; re-review its publication policy")
    output = []
    for card in cards:
        if card['id'] in RETIRED:
            continue
        c = copy.deepcopy(card)
        g = GROUPS.get(c['id'])
        if g:
            c.pop('selectionVariant', None)
            c['questionText'] = g['questionText']
            c['selectionChoice'] = copy.deepcopy(g['selectionChoice'])
        output.append(c)
    return output


def publication_overrides(cid):
    g = GROUPS.get(cid)
    return {k: g[k] for k in ('figureKey', 'questionFigureKey')} if g else {}
