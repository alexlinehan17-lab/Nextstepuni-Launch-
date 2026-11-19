#!/usr/bin/env python3
"""Audit the actual Paper Trail inventory; counts never certify completeness.

Run from any directory. The report names every paper, missing source, unreviewed
page and authored card rejected by the runtime build. A separate visual review
records published mark boundaries, topics, source pages and selection decisions.
"""
import argparse
import hashlib
import json
from itertools import combinations
import re
from collections import Counter
from pathlib import Path

import fitz
from sources import review_source

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
CHOICE_POLICY = json.loads((HERE / 'choice-policy.json').read_text())['groups']
SELECTION_NUMBER = r'(?:one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|\d+)'
SELECTION = re.compile(
    r'\b(?:choos\w*|one of|any (?:one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|\d+)|either|'
    r'or otherwise|answer (?:all|any)|(?:attempt|answer)(?: any)? ' + SELECTION_NUMBER +
    r'(?= (?:questions?\b|of\b)))\b', re.I)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def selection_candidates(path):
    result = []
    with fitz.open(path) as pdf:
        for number, page in enumerate(pdf, 1):
            text = ' '.join(page.get_text().split())
            for match in SELECTION.finditer(text):
                context = text[max(0, match.start() - 40):match.end() + 90]
                key = f'{number}:' + hashlib.sha256(context.encode()).hexdigest()[:16]
                result.append({'id': key, 'page': number, 'context': context})
    return result


def logical_tasks(review):
    """Validate every finite route, then count its published task tariff once."""
    result, groups = [], {}
    ids = [c['id'] for c in review['cards']]
    if len(ids) != len(set(ids)):
        raise ValueError('duplicate reviewed task identity')
    for policy in CHOICE_POLICY:
        if (review.get('year'), review.get('paperFileid')) != (policy['year'], policy['paperFileid']):
            continue
        active = [c for c in review['cards'] if c['id'] in policy['legacyIds']]
        if len(active) != 1 or active[0]['id'] != policy['canonicalId']:
            raise ValueError(f"{policy['canonicalId']}: missing or expanded printed choice")
        card = active[0]
        original = policy['legacyCards'][0]
        if any(card.get(k) != original.get(k) for k in ('printedParts', 'totalMarks', 'scale', 'components', 'methods', 'topicId', 'examTopicIds')):
            raise ValueError(f"{card['id']}: choice tariff or curriculum boundary changed")
        if card.get('selectionChoice') != policy['selectionChoice'] or card.get('questionText') != policy['questionText']:
            raise ValueError(f"{card['id']}: choice directive, options or wording changed")
    for card in review['cards']:
        choice = card.get('selectionChoice')
        if choice:
            pool, choose = choice['pool'], choice['choose']
            if len(pool) != len(set(pool)) or not 0 < choose <= len(pool):
                raise ValueError(f"{card['id']}: invalid printed choice")
            path = review_source(review, 'paper')
            with fitz.open(path) as pdf:
                text = ' '.join(pdf[choice['sourcePage'] - 1].get_text().split())
            if choice['sourceDirective'] not in text:
                raise ValueError(f"{card['id']}: printed choice directive changed")
            if any(other['id'] != card['id'] and other.get('selectionChoice', {}).get('groupId') == choice['groupId'] for other in review['cards']):
                raise ValueError(f"{card['id']}: choice was expanded into sibling cards")
        variant = card.get('selectionVariant')
        if not variant:
            result.append(card)
            continue
        groups.setdefault(variant['groupId'], []).append(card)
    for group, cards in groups.items():
        first = cards[0]
        spec = first['selectionVariant']
        pool, choose = spec['pool'], spec['choose']
        if len(pool) != len(set(pool)) or not 0 < choose <= len(pool):
            raise ValueError(f'{group}: invalid selection pool')
        expected = set(combinations(pool, choose))
        actual = []
        for card in cards:
            variant = card['selectionVariant']
            if not variant.get('practiceInstruction', '').strip():
                raise ValueError(f'{group}: missing visible practice instruction')
            if any(variant[k] != spec[k] for k in ('pool', 'choose', 'sourcePage', 'sourceDirective')):
                raise ValueError(f'{group}: inconsistent selection definition')
            if any(card.get(k) != first.get(k) for k in ('printedParts', 'totalMarks', 'scale', 'permittedMarks', 'sourcePages', 'schemePages')):
                raise ValueError(f'{group}: routes disagree on source task or tariff')
            actual.append(tuple(variant['selected']))
        if len(actual) != len(set(actual)) or set(actual) != expected:
            raise ValueError(f'{group}: missing, duplicate or invalid finite route')
        path = review_source(review, 'paper')
        with fitz.open(path) as pdf:
            text = ' '.join(pdf[spec['sourcePage'] - 1].get_text().split())
        if spec['sourceDirective'] not in text:
            raise ValueError(f'{group}: finite directive no longer matches original paper')
        result.append(first)
    return result


def validate_review_sources(reviews=None):
    """Fail authoring before generation when a source or choice decision drifts."""
    if reviews is None:
        reviews = [json.loads(p.read_text()) for p in sorted((HERE / 'reviews').glob('*.json'))]
    errors = []
    for review in reviews:
        identity = f"{review['year']}/{review['paperFileid']}"
        paper = review_source(review, 'paper')
        scheme = review_source(review, 'scheme')
        if not paper.is_file() or not scheme.is_file():
            errors.append(f'{identity}: missing reviewed primary source')
            continue
        if sha(paper) != review['paperSha256'] or sha(scheme) != review['schemeSha256']:
            errors.append(f'{identity}: source changed after visual review')
        with fitz.open(paper) as pdf:
            if review['paperPagesInspected'] != list(range(1, len(pdf) + 1)):
                errors.append(f'{identity}: incomplete visual paper-page sweep')
        with fitz.open(scheme) as pdf:
            pages = review['schemePagesInspected']
            required = set(review['generalNotesPages'])
            for card in review['cards']:
                required.update(card['schemePages'])
            if not required.issubset(pages) or any(p < 1 or p > len(pdf) for p in pages):
                errors.append(f'{identity}: uninspected or invalid scheme page')
        try:
            logical_tasks(review)
        except (ValueError, KeyError, IndexError) as error:
            errors.append(f'{identity}: {error}')
        decisions = review.get('selectionDecisions', {})
        actual = {item['id'] for item in selection_candidates(paper)}
        if set(decisions) != actual:
            errors.append(f'{identity}: unclassified or stale raw selection directives')
        for key, decision in decisions.items():
            if not decision.get('classification') or not decision.get('reason', '').strip():
                errors.append(f'{identity}: selection decision {key} lacks a written reason')
    return errors


def inventory():
    source = (ROOT / 'paperTrailData.ts').read_text()
    section = source.split('export const PAPER_TRAIL_INDEX')[1]
    section = section.split('  "mathematics": [\n', 1)[1].split('\n  ],', 1)[0]
    return [json.loads(line.strip().rstrip(',')) for line in section.splitlines() if line.strip()]


def runtime_cards():
    result = {}
    for path in sorted((ROOT / 'components/MarkBank/cards/maths').glob('*.ts')):
        for chunk in re.split(r'\.\.\.base,[^\n]*?kind:', path.read_text())[1:]:
            identity = re.search(r'\bid: "([^"]+)"', chunk)
            if not identity:
                continue
            result[identity[1]] = {
                'questionRef': re.search(r'questionRef: "([^"]+)"', chunk)[1],
                'hasSourceReader': 'sourceMaterial:' in chunk,
                'hasQuestionFigure': 'questionFigure:' in chunk,
            }
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, default=HERE / 'audit.json')
    parser.add_argument('--check-reviewed', action='store_true')
    parser.add_argument('--year-from', type=int, default=2010)
    parser.add_argument('--year-to', type=int, default=2026)
    args = parser.parse_args()
    if args.check_reviewed:
        errors = validate_review_sources()
        for error in errors:
            print('ERROR', error)
        if not errors:
            print('Reviewed Mathematics source hashes, page sweeps and raw selection decisions agree.')
        return bool(errors)
    reviews = [json.loads(p.read_text()) for p in sorted((HERE / 'reviews').glob('*.json'))]
    by_paper = {(r['year'], r['paperFileid']): r for r in reviews}
    authored = json.loads((ROOT / 'scripts/markbank/authored/maths.json').read_text())
    runtime = runtime_cards()
    papers, errors = [], []
    all_entries = inventory()
    entries = [e for e in all_entries if args.year_from <= e['year'] <= args.year_to]
    for entry in entries:
        for item in entry['papers']:
            fileid = item['doc']['f']
            year = entry['year']
            sitting = item.get('sitting', entry.get('sitting', 'main'))
            archive = 'deferredexams' if sitting == 'deferred' else 'exampapers'
            disk_file = fileid.replace('-deferred.pdf', '.pdf') if sitting == 'deferred' else fileid
            path = ROOT / 'paper-trail-corpus' / archive / str(year) / disk_file
            scheme_file = item.get('scheme', {}).get('f')
            scheme_archive = 'deferredmarkingschemes' if sitting == 'deferred' else 'markingschemes'
            scheme_disk_file = (scheme_file or '').replace('-deferred.pdf', '.pdf') if sitting == 'deferred' else (scheme_file or '')
            scheme = ROOT / 'paper-trail-corpus' / scheme_archive / str(year) / scheme_disk_file
            review = by_paper.get((year, fileid))
            count = len(fitz.open(path)) if path.is_file() else None
            candidates = selection_candidates(path) if path.is_file() and entry['lang'] == 'ev' else []
            record = {
                'year': year, 'level': entry['level'], 'lang': entry['lang'],
                'fileid': fileid, 'sitting': sitting, 'label': item['label'], 'schemeFileid': scheme_file,
                'paperAvailable': path.is_file(), 'schemeAvailable': scheme.is_file(),
                'paperPages': count,
                'answerSidecarAvailable': (ROOT / 'scripts/paper-trail/answers' / str(year) / (fileid + '.json')).is_file(),
                'reviewed': bool(review), 'reviewedTaskCount': len(review['cards']) if review else 0,
                'selectionCandidates': candidates,
            }
            if not path.is_file():
                errors.append(f'{year}/{fileid}: missing question-paper PDF')
            if not scheme_file:
                errors.append(f'{year}/{fileid}: no scheme association in Paper Trail')
            elif not scheme.is_file():
                errors.append(f'{year}/{fileid}: missing scheme PDF {scheme_file}')
            if review:
                if sha(path) != review['paperSha256'] or sha(scheme) != review['schemeSha256']:
                    errors.append(f'{year}/{fileid}: reviewed source hash changed')
                if review['paperPagesInspected'] != list(range(1, count + 1)):
                    errors.append(f'{year}/{fileid}: paper-page sweep incomplete')
                decisions = review.get('selectionDecisions', {})
                actual = {candidate['id'] for candidate in candidates}
                if set(decisions) != actual:
                    errors.append(f'{year}/{fileid}: unclassified or stale selection directives')
                totals = Counter()
                parts = []
                for card in review['cards']:
                    if card['id'] not in runtime:
                        errors.append(f"{card['id']}: reviewed task absent from runtime")
                    if card['sourcePages'] != sorted(set(card['sourcePages'])) or any(p < 1 or p > count for p in card['sourcePages']):
                        errors.append(f"{card['id']}: invalid source pages")
                try:
                    logical = logical_tasks(review)
                except (ValueError, KeyError, IndexError) as error:
                    errors.append(f'{year}/{fileid}: {error}')
                    logical = review['cards']
                for card in logical:
                    totals[re.match(r'Q(\d+[A-Z]?)', card['printedParts'][0])[1]] += card['totalMarks']
                    parts.extend(card['printedParts'])
                if dict(totals) != review['printedQuestionMarks']:
                    errors.append(f'{year}/{fileid}: scales disagree with printed question totals')
                if len(set(parts)) != len(parts):
                    errors.append(f'{year}/{fileid}: repeated printed part in review')
            papers.append(record)
    dropped = [card['id'] for card in authored if card['id'] not in runtime]
    report = {
        'schemaVersion': 1, 'subjectId': 'mathematics', 'complete': False,
        'scope': f'Mathematics {args.year_from}–{args.year_to}, all indexed levels and editions; translated editions retain separate source provenance. Earlier Paper Trail holdings are outside this requested authoring scope.',
        'yearRange': [args.year_from, args.year_to],
        'outOfScopeIndexedPaperEditions': sum(len(e['papers']) for e in all_entries if e not in entries),
        'summary': {
            'paperEditions': len(papers), 'englishEditionPapers': sum(p['lang'] == 'ev' for p in papers),
            'years': sorted({p['year'] for p in papers}),
            'levels': sorted({p['level'] for p in papers}),
            'runtimeCards': len(runtime), 'authoredCards': len(authored),
            'authoredNotInRuntime': len(dropped), 'reviewedPaperEditions': len(reviews),
            'reviewedMarkedTasks': sum(len(r['cards']) for r in reviews),
        },
        'authoredNotInRuntime': dropped, 'reviewErrors': errors,
        'remainingRequirements': [
            'Visually review every outstanding paper and its marking boundaries.',
            'Include every independently practicable published mark unit in Mark Bank, including Foundation and earlier years.',
            'Reconcile all printed parts and finite prompt choices against an independent reviewed census.',
            'Verify canonical and Atlas placement for every task.',
            'Replace Mathematics credit-band checklists with the actual published scale selection.',
            'Verify source opening, zooming, closing and solution reveal on desktop and mobile.',
            'Run preservation, curriculum, deck, parity and runtime checks for the full corpus.',
        ],
        'papers': papers,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(report['summary'], indent=2))
    for error in errors:
        print('ERROR', error)
    return bool(errors)


if __name__ == '__main__':
    raise SystemExit(main())
