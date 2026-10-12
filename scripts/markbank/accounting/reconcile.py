#!/usr/bin/env python3
"""Independently reconcile the visual audit, corpus and shipped Accounting data.

Does not import the deck generator and does not infer completeness from counts.
The reviewed task boundaries remain the visual paper/scheme evidence; this
checks their bidirectional correspondence to every shipped task and source.
"""
import hashlib
import json
from pathlib import Path
import fitz

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent


def read(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def reconcile():
    issues = []
    checks = 0

    def check(condition, message):
        nonlocal checks
        checks += 1
        if not condition:
            issues.append(message)

    papers = {f'{p.parent.name}/{p.name}': p for p in (ROOT / 'paper-trail-corpus/exampapers').glob('*/LC032*.pdf')}
    inventory = read(HERE / 'inventory.json')['papers']
    check(set(papers) == {f'{i["year"]}/{i["fileid"]}' for i in inventory}, 'Inventory/corpus editions differ')
    reviews = [read(p) for p in sorted((HERE / 'reviewed').glob('*.json'))]
    translations = [read(p) for p in sorted((HERE / 'correspondence').glob('*.json'))]
    all_reviews = {f'{r["year"]}/{r["fileid"]}': r for r in reviews + translations}
    check(set(papers) == set(all_reviews), 'Unreviewed source edition or orphan review')
    authored = read(ROOT / 'components/MarkBank/cards/accounting/authored.json')['cards']
    cards = {c['id']: c for c in authored}
    check(len(cards) == len(authored), 'Duplicate card ID')
    runtime = read(ROOT / 'data/examTopics/accounting-task-runtime.json')
    mappings = {(r['year'], r['fileid'], r['n']): r for r in runtime['tasks']}
    check(len(mappings) == len(runtime['tasks']), 'Duplicate Atlas task mapping')
    expected_ids, parent_rows, pools, fallbacks = set(), [], [], []
    page_totals = {'paper': 0, 'scheme': 0}
    selection_totals = {}
    for key, review in all_reviews.items():
        paper = papers[key]
        check(sha(paper) == review['paperSha256'], f'{key}: changed paper')
        with fitz.open(paper) as doc:
            check(review['visualPaperPages'] == list(range(1, len(doc) + 1)), f'{key}: incomplete paper sweep')
            page_totals['paper'] += len(doc)
        scheme = ROOT / 'paper-trail-corpus/markingschemes' / key
        if not scheme.exists():
            fallback = review.get('schemeFallback', {})
            check(bool(fallback.get('reason')) and bool(fallback.get('paperComparison')), f'{key}: unexplained missing scheme')
            check(review['visualSchemePages'] == [], f'{key}: claims inspection of absent scheme')
            scheme = scheme.with_name(fallback.get('fileid', 'missing'))
            fallbacks.append({'edition': key, 'scheme': str(scheme.relative_to(ROOT)), 'reason': fallback.get('reason')})
        if scheme.exists():
            check(sha(scheme) == review['schemeSha256'], f'{key}: changed scheme')
            with fitz.open(scheme) as doc:
                pages = review.get('schemeFallback', review)['visualSchemePages']
                check(pages == list(range(1, len(doc) + 1)), f'{key}: incomplete scheme sweep')
                if 'schemeFallback' not in review:
                    page_totals['scheme'] += len(doc)
        else:
            check(False, f'{key}: missing fallback scheme')
        for directive in review['selectionReview']:
            classification = directive['classification']
            check(classification in {'paper-level-choice', 'open-response', 'not-a-selection', 'finite-pool-one-card', 'closed-pool', 'comparison-required', 'equivalent-units'}, f'{key}: unclassified selection')
            check(bool(directive['reason']), f'{key}: unexplained selection decision')
            selection_totals[classification] = selection_totals.get(classification, 0) + 1
    for review in reviews:
        year, level, fileid = review['year'], review['level'], review['fileid']
        key = f'{year}/{fileid}'
        rows = [c for c in authored if c['year'] == year and c['paperFileid'] == fileid]
        source_tasks = []
        for task in review['tasks']:
            # A printed choice is one task and one card (AGENTS.md, 2026-10-12).
            pool = task.get('printedChoice')
            check('selectionPool' not in task, f'{key}: {task["key"]}: retired route expansion')
            variants = [task['key']]
            if pool:
                pools.append({'edition': key, 'task': task['key'], 'choose': pool['choose'], 'options': len(pool['options']), 'cards': variants, 'marks': task['marks']})
            for variant in variants:
                ident = f'acc-{year}-{"hl" if level == "higher" else "ol"}-q{variant}'
                expected_ids.add(ident)
                card = cards.get(ident)
                check(card is not None, f'{key}: missing task {variant}')
                if card is None:
                    continue
                check(card['totalMarks'] == task['marks'], f'{ident}: tariff mismatch')
                check(card['paperPages'] == task['paperPages'], f'{ident}: source pages mismatch')
                expected_regions = task['schemeRegions'] + [{'p': p, 'r': [0, 0, 1, 1]} for p in review['markingGuidePages']]
                check(card['schemeRegions'] == expected_regions, f'{ident}: scheme mismatch')
                check(card['topicId'] == task['topicId'] and card['examTopicIds'] == task['examTopicIds'], f'{ident}: topic mismatch')
                mapping = mappings.get((year, fileid, variant))
                check(mapping is not None and mapping['topicIds'] == task['examTopicIds'], f'{ident}: missing/mismatched Atlas mapping')
                source_tasks.append(variant)
        check(set(source_tasks) == {c['taskKey'] for c in rows}, f'{key}: task mismatch')
        # Published full-question tariffs, independently of the generated total.
        for number in range(1, 10):
            expected = (240 if year >= 2021 else 120) if number == 1 else 60 if number <= 4 else 100 if number <= 7 else 80
            group = [c for c in rows if c['questionNumber'] == number]
            check(bool(group) and sum(c['totalMarks'] for c in group) == expected, f'{key} Q{number}: unreconciled published tariff')
            parent_rows.append({'edition': key, 'question': number, 'tasks': [c['taskKey'] for c in group], 'allRouteMarks': expected})
        before = read(ROOT / 'scripts/paper-trail/answers' / (key + '.json'))
        after = read(ROOT / 'public/paper-answers' / (key + '.json'))
        after_by_key = {q['n']: q for q in after['q']}
        check(len(after_by_key) == len(after['q']), f'{key}: duplicate answer ID')
        for old in before['q']:
            updated = after_by_key.get(old['n'])
            check(updated is not None, f'{key}: deleted old question {old["n"]}')
            for field in ['n', 'pP', 'pY', 'region', 'mode', 'conf']:
                check(updated is not None and updated.get(field) == old.get(field), f'{key} {old["n"]}: changed original {field}')
        check(set(after_by_key) == {q['n'] for q in before['q']} | set(source_tasks), f'{key}: missing or orphan answer task')
        for card in rows:
            q = after_by_key.get(card['taskKey'], {})
            check(q.get('practiceTask', {}).get('marks') == card['totalMarks'], f'{card["id"]}: answer marks mismatch')
            check(q.get('practiceTask', {}).get('prompt') == card['questionText'], f'{card["id"]}: answer wording mismatch')
            check(q.get('schemeRegion', q.get('region')) == card['schemeRegions'], f'{card["id"]}: answer source mismatch')
    for review in translations:
        english = read(HERE / 'reviewed' / review['englishReview'])
        expected = {c['taskKey']: c for c in authored if c['year'] == review['year'] and c['paperFileid'] == english['fileid']}
        linked = {t['englishTaskKey']: t for t in review['taskCorrespondence']}
        check(set(linked) == set(expected) and len(linked) == len(review['taskCorrespondence']), f'{review["fileid"]}: incomplete translated task correspondence')
        check(review['uniqueAdditionalTasks'] == [], f'{review["fileid"]}: unhandled translated task')
        check({q['questionNumber'] for q in review['questionReview']} == set(range(1, 10)), f'{review["fileid"]}: missing translated question review')
    check(expected_ids == set(cards), 'Uncovered or orphan Mark Bank task')
    check(set(mappings) == {(c['year'], c['paperFileid'], c['taskKey']) for c in authored}, 'Uncovered or orphan Atlas mapping')
    result = {'subjectId': 'accounting', 'scope': 'All local Paper Trail Accounting papers, 2010–2026, Higher and Ordinary, English and Irish',
              'method': 'Independent reconciliation of visually reviewed boundaries against source files, published parent tariffs, preserved sidecars, one-card printed choices and generated artifacts. Runtime Atlas and canonical-topic checks are in markBankAccounting.test.tsx.',
              'sourceReconciliationPassed': not issues, 'checks': checks, 'openIssues': issues,
              'sourceEditions': len(papers), 'visuallyReviewedPages': page_totals,
              'logicalTasks': len(cards), 'selectionClassifications': selection_totals,
              'explicitSchemeFallbacks': fallbacks, 'finitePools': pools, 'parentReconciliation': parent_rows}
    (HERE / 'reconciliation.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    if issues:
        raise AssertionError('\n'.join(issues))
    print(f'PASS: {checks} reconciliation checks; {len(papers)} editions; {len(cards)} tasks; zero open issues or orphan tasks.')
    return result


if __name__ == '__main__':
    reconcile()
