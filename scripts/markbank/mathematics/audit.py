#!/usr/bin/env python3
"""Audit the actual Paper Trail inventory; counts never certify completeness.

Run from any directory. The report names every paper, missing source, unreviewed
page and authored card rejected by the runtime build. A separate visual review
records published mark boundaries, topics, source pages and selection decisions.
"""
import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

import fitz

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
SELECTION = re.compile(
    r'\b(?:choos\w*|one of|any (?:one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|\d+)|either|'
    r'or otherwise|answer (?:all|any))\b', re.I)


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


def validate_review_sources(reviews=None):
    """Fail authoring before generation when a source or choice decision drifts."""
    if reviews is None:
        reviews = [json.loads(p.read_text()) for p in sorted((HERE / 'reviews').glob('*.json'))]
    errors = []
    for review in reviews:
        identity = f"{review['year']}/{review['paperFileid']}"
        paper = ROOT / 'paper-trail-corpus/exampapers' / str(review['year']) / review['paperFileid']
        scheme = ROOT / 'paper-trail-corpus/markingschemes' / str(review['year']) / review['schemeFileid']
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
        for chunk in re.split(r'\.\.\.base,\s*kind:', path.read_text())[1:]:
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
    for entry in inventory():
        for item in entry['papers']:
            fileid = item['doc']['f']
            year = entry['year']
            path = ROOT / 'paper-trail-corpus/exampapers' / str(year) / fileid
            scheme_file = item.get('scheme', {}).get('f')
            scheme = ROOT / 'paper-trail-corpus/markingschemes' / str(year) / (scheme_file or '')
            review = by_paper.get((year, fileid))
            count = len(fitz.open(path)) if path.is_file() else None
            candidates = selection_candidates(path) if path.is_file() and entry['lang'] == 'ev' else []
            record = {
                'year': year, 'level': entry['level'], 'lang': entry['lang'],
                'fileid': fileid, 'label': item['label'], 'schemeFileid': scheme_file,
                'paperAvailable': path.is_file(), 'schemeAvailable': scheme.is_file(),
                'paperPages': count,
                'answerSidecarAvailable': (ROOT / 'scripts/paper-trail/answers' / str(year) / (fileid + '.json')).is_file(),
                'reviewed': bool(review), 'reviewedTaskCount': len(review['cards']) if review else 0,
                'selectionCandidates': candidates,
            }
            if not path.is_file() or not scheme.is_file():
                errors.append(f'{year}/{fileid}: missing primary source')
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
                    totals[re.match(r'Q(\d+[A-Z]?)', card['printedParts'][0])[1]] += card['totalMarks']
                    parts.extend(card['printedParts'])
                    if card['id'] not in runtime:
                        errors.append(f"{card['id']}: reviewed task absent from runtime")
                    if card['sourcePages'] != sorted(set(card['sourcePages'])) or any(p < 1 or p > count for p in card['sourcePages']):
                        errors.append(f"{card['id']}: invalid source pages")
                if dict(totals) != review['printedQuestionMarks']:
                    errors.append(f'{year}/{fileid}: scales disagree with printed question totals')
                if len(set(parts)) != len(parts):
                    errors.append(f'{year}/{fileid}: repeated printed part in review')
            papers.append(record)
    dropped = [card['id'] for card in authored if card['id'] not in runtime]
    report = {
        'schemaVersion': 1, 'subjectId': 'mathematics', 'complete': False,
        'scope': 'Every Mathematics paper in the current Paper Trail index, all years and levels; translated editions retain separate source provenance.',
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
