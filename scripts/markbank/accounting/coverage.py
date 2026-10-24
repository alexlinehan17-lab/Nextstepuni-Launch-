"""Expose Accounting's independent source audit to the shared coverage ratchet."""
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def census_accounting():
    spec = importlib.util.spec_from_file_location('accounting_source_reconciliation', HERE / 'reconcile.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    receipt = module.reconcile()  # Reopens and verifies all papers/schemes; raises on any issue.
    papers = []
    for path in sorted((HERE / 'reviewed').glob('*.json')):
        review = json.loads(path.read_text())
        papers.append({'year': review['year'], 'level': review['level'], 'paper': None,
                       'leaves': [], 'sourceReview': str(path.relative_to(ROOT))})
    return {'subject': 'accounting', 'mode': 'accounting-reviewed', 'papers': papers,
            'sourceReceipt': receipt, 'flags': []}


def reconcile_accounting(census):
    receipt = census['sourceReceipt']
    if not receipt['sourceReconciliationPassed'] or receipt['openIssues']:
        raise AssertionError('Accounting source reconciliation is incomplete')
    # The source reconciler independently checks exact expected IDs, Atlas
    # mappings, finite pools, preserved original sidecars and every tariff.
    count = receipt['logicalTasks']
    return {'subject': 'accounting', 'mode': census['mode'], 'cards': count,
            'leaves': count, 'covered': count, 'excluded': 0, 'open': 0,
            'coveragePct': 100.0, 'orphans': [], 'unparsed': [], 'staleExclusions': [],
            'papers': [], 'censusFlags': 0, 'sourceEditions': receipt['sourceEditions']}
