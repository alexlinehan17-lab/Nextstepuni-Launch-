#!/usr/bin/env python3
"""Reconcile the full Business source inventory without claiming task coverage.

Paper Trail's document list is the scope authority. Its top-level question
anchors are useful navigation, not proof of the independently marked tasks.
The visual paper/scheme review remains explicit and separate from this scan.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import re
import subprocess
from pathlib import Path

import fitz
from business_selection import page_directives, apply_reviews, require_reviewed
from strip_pages import page_text

ROOT = Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location(
    "business_paper_inventory", ROOT / "scripts/paper-trail/business.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else None


def prepare_census_sources():
    """Expose all English Paper Trail PDFs to the existing candidate parser.

    These ignored relative symlinks are a local cache, never independent proof
    of task coverage. Do not silently replace an existing source document.
    """
    destination = ROOT / 'examiner-reports/business/papers'
    destination.mkdir(parents=True, exist_ok=True)
    for entry in module.paper_index():
        if entry['lang'] != 'ev':
            continue
        for paper in entry['papers']:
            filename = paper['doc']['f']
            source = ROOT / 'paper-trail-corpus/exampapers' / str(entry['year']) / filename
            if not source.exists():
                raise FileNotFoundError(source)
            component = re.search(r'P(\d{3})', filename).group(1)
            level = 'hl' if entry['level'] == 'higher' else 'ol'
            target = destination / f"{entry['year']}-{level}-{component}-paper.pdf"
            if target.exists() or target.is_symlink():
                if not target.exists() or digest(target) != digest(source):
                    raise ValueError(f'Different source already exists: {target}')
            else:
                target.symlink_to(os.path.relpath(source, destination))


def paper_for(card, papers):
    if len(papers) == 1:
        return papers[0]
    matches = [paper for paper in papers if re.search(
        rf"\b{re.escape(card['section'])}\b", paper["label"])]
    if len(matches) != 1:
        raise ValueError(f"Ambiguous paper for {card['id']}")
    return matches[0]


def inventory():
    cards = json.loads((ROOT / "scripts/markbank/authored/business.json").read_text())
    supplement = ROOT / 'components/MarkBank/cards/business/rubric-authored.json'
    reviews = []
    if supplement.exists():
        payload = json.loads(supplement.read_text())
        reviewed = payload['cards']
        reviews = payload['reviews']
        cards = list({card['id']: card for card in cards + reviewed}.values())
    route_path = ROOT / 'components/MarkBank/cards/business/route-pools.json'
    if route_path.exists():
        routes = json.loads(subprocess.check_output(
            ['node', str(ROOT / 'scripts/markbank/authoring/business_routes.mjs')], text=True))
        # A legacy card kept as one expanded route is the same card, once.
        cards = list({card['id']: card for card in cards + routes}.values())
        reviews.extend(pool['review'] for pool in json.loads(route_path.read_text())['pools'])
    documents = []
    assigned = set()
    for entry in module.paper_index():
        matching = [card for card in cards
                    if card['year'] == entry['year'] and card['level'] == entry['level']]
        for paper in entry['papers']:
            filename = paper['doc']['f']
            paper_path = ROOT / 'paper-trail-corpus/exampapers' / str(entry['year']) / filename
            scheme = paper.get('scheme', {}).get('f')
            scheme_path = (ROOT / 'paper-trail-corpus/markingschemes' / str(entry['year']) / scheme
                           if scheme else None)
            # Published paper anchors use the same ABQ/S3Q identities as Topic
            # Atlas. Legacy answer maps can use sequential numbers 11–18 for
            # these same questions, so they are not the identity authority.
            anchor_path = ROOT / 'public/paper-anchors' / str(entry['year']) / f'{filename}.json'
            anchor = json.loads(anchor_path.read_text()) if anchor_path.exists() else None
            # The existing cards quote the English paper. Irish source variants
            # remain in scope; an English match never asserts Irish card coverage.
            bound = [card['id'] for card in matching
                     if entry['lang'] == 'ev' and paper_for(card, entry['papers']) == paper]
            assigned.update(bound)
            directives = []
            page_count = None
            paper_hash = digest(paper_path)
            if paper_path.exists():
                with fitz.open(paper_path) as pdf:
                    page_count = len(pdf)
                    # A strip-cut page (2011 OL p11) is scanned as its rebuilt
                    # lines, so its directives read as printed.
                    for index, page in enumerate(pdf):
                        directives.extend(page_directives(entry['year'], filename,
                            index + 1, page_text(page), paper_hash))
            documents.append({
                'year': entry['year'], 'level': entry['level'], 'language': entry['lang'],
                'paperFileid': filename, 'paperLabel': paper['label'], 'schemeFileid': scheme,
                'paperSha256': paper_hash,
                'schemeSha256': digest(scheme_path) if scheme_path else None,
                'paperPages': page_count,
                'paperTrailQuestionIds': [q['n'] for q in anchor['q']] if anchor else [],
                'authoredCardIds': sorted(bound),
                'selectionDirectives': directives,
                'taskBoundaryReview': 'not-yet-complete',
                'reviewedSections': [
                    {'section': review['section'], 'question': review['question'],
                     'boundaries': review['boundaries'],
                     'paperPages': review['paperPagesReviewed'],
                     'schemePages': review['schemePagesReviewed']}
                    for review in reviews
                    if entry['lang'] == 'ev' and review['year'] == entry['year']
                    and review['level'] == entry['level']
                    and review['sources']['exampapers']['fileid'] == filename
                ],
            })
    all_directives = [item for doc in documents for item in doc['selectionDirectives']]
    selection_path = ROOT / 'scripts/markbank/authored/business-selection-reviews.json'
    selection_reviews = json.loads(selection_path.read_text())['reviews'] if selection_path.exists() else {}
    apply_reviews(all_directives, selection_reviews)
    pools = json.loads(route_path.read_text())['pools'] if route_path.exists() else []
    pool_ids = {pool['id'] for pool in pools}
    card_ids = {card['id'] for card in cards}
    for item in all_directives:
        if item.get('poolId') and item['poolId'] not in pool_ids:
            raise ValueError(f"Business selection references a missing pool: {item['poolId']}")
        if item.get('cardId') and item['cardId'] not in card_ids:
            raise ValueError(f"Business selection references a missing card: {item['cardId']}")
    for pool in pools:
        if not any(item.get('poolId') == pool['id'] for item in all_directives):
            raise ValueError(f"Business route pool has no reviewed source directive: {pool['id']}")
        template = pool['template']
        path = ROOT / 'paper-trail-corpus/exampapers' / str(template['year']) / (template['paperFileid'] + '.pdf')
        with fitz.open(path) as pdf:
            wording = re.sub(r'\s+', ' ', ' '.join(pdf[p-1].get_text() for p in template['paperPages']))
        if pool['sourceWording'] not in wording:
            raise ValueError(f"Business route wording no longer matches its paper: {pool['id']}")
    paper_review_path = ROOT / 'scripts/markbank/authored/business-paper-reviews.json'
    paper_reviews = json.loads(paper_review_path.read_text())['reviews'] if paper_review_path.exists() else []
    for review in paper_reviews:
        matches = [doc for doc in documents if all(doc[field] == review[field]
                   for field in ['year', 'level', 'language', 'paperFileid'])]
        if len(matches) != 1:
            raise ValueError('Stale Business full-paper review identity')
        doc = matches[0]
        if any(doc[field] != review[field] for field in
               ['paperSha256', 'schemeSha256', 'schemeFileid']):
            raise ValueError(f"Business full-paper review source changed: {doc['paperFileid']}")
        if (set(doc['authoredCardIds']) != set(review['authoredCardIds'])
                or set(doc['paperTrailQuestionIds']) != set(review['questionIdsReviewed'])
                or review['paperPagesReviewed'] != list(range(1, doc['paperPages'] + 1))):
            raise ValueError(f"Business full-paper review coverage changed: {doc['paperFileid']}")
        if any(pool_id not in pool_ids for pool_id in review['finiteRoutePoolIds']):
            raise ValueError('Business full-paper review references a missing route pool')
        if any(card_id not in doc['authoredCardIds'] for card_id in review.get('finiteChoiceCardIds', [])):
            raise ValueError('Business full-paper review references a choice card outside its paper')
        require_reviewed(doc['selectionDirectives'])
        # This status comes only from the explicit visual/source review. The
        # equality checks above detect stale evidence; they do not prove that
        # a parser or card count has found every independently marked task.
        doc['taskBoundaryReview'] = review['status']
    orphaned = sorted(card['id'] for card in cards if card['id'] not in assigned)
    return {
        'schemaVersion': 2,
        'subjectId': 'business',
        'scope': 'Every Business document in the current Paper Trail index, 2010–2026, both levels and published languages.',
        'status': 'in-progress',
        'evidenceLimit': 'Document and card reconciliation only. Neither parser counts nor Paper Trail question anchors prove separately marked task completeness.',
        'summary': {
            'documents': len(documents),
            'englishDocuments': sum(d['language'] == 'ev' for d in documents),
            'fullyReviewedDocuments': len(paper_reviews),
            'authoredCards': len(cards),
            'documentsWithAuthoredCards': sum(bool(d['authoredCardIds']) for d in documents),
            'documentsWithoutAuthoredCards': sum(not d['authoredCardIds'] for d in documents),
            'missingPaperFiles': sum(d['paperSha256'] is None for d in documents),
            'missingSchemeBindings': sum(d['schemeFileid'] is None for d in documents),
            'missingSchemeFiles': sum(d['schemeFileid'] is not None and d['schemeSha256'] is None for d in documents),
            'selectionDirectives': len(all_directives),
            'reviewedSelectionDirectives': sum(item['reviewStatus'] == 'reviewed' for item in all_directives),
            'unclassifiedSelectionDirectives': sum(item['reviewStatus'] != 'reviewed' for item in all_directives),
        },
        'orphanedAuthoredCardIds': orphaned,
        'documents': documents,
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--prepare-census', action='store_true',
                        help='Create ignored relative PDF links for the candidate parser')
    parser.add_argument('--check-selections', action='store_true',
                        help='Exit 3 when any raw-paper selection directive is unclassified')
    args = parser.parse_args()
    if args.prepare_census:
        prepare_census_sources()
    result = inventory()
    destination = ROOT / 'scripts/markbank/authored/business-corpus-inventory.json'
    destination.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(result['summary'], indent=2))
    if result['orphanedAuthoredCardIds']:
        raise SystemExit(f"Unresolved authored cards: {result['orphanedAuthoredCardIds']}")
    if args.check_selections:
        try:
            require_reviewed([item for doc in result['documents'] for item in doc['selectionDirectives']])
        except ValueError as error:
            print(str(error))
            raise SystemExit(3)
