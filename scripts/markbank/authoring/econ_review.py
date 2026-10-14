#!/usr/bin/env python3
"""Validate independent Economics paper reviews against the physical sources.

Default refuses an incomplete corpus. --allow-pending is for work in progress;
it still refuses source changes, stale reviews and unclassified directives in
any reviewed paper. The task census is authored by visual paper/scheme review,
not generated from the existing cards or the old extraction parser.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re

import fitz

from econ_inventory import ROOT, indexed_papers

DIRECTIVE = re.compile(
    r"\b(?:choose|choices?|select|either|or|agree|disagree|yes|no)\b|"
    r"\b(?:\d+|one|two|three|four|five|six|seven|eight|nine|ten) of\b|"
    r"\bany \w+\b|\banswer (?:\d+|one|two|three|four|five|six|seven|eight|nine|ten)\b|"
    r"\bfor and against\b|"
    r"\b(?:freagair|nó|aon|rogha|roghanna|roghnaigh|roghnaítear|cibé|"
    r"aontaím|aontaíonn|aontaigh|easaontaím|easaontaíonn)\b|"
    r"\bcé acu\b|\b(?:ceann|cinn|amháin) de\b|\bar bith\b|"
    r"\b(?:ar|ba|níor|ní|nár) (?:chóir|cheart)\b|"
    r"\b(?:ceapaim|gceapann|gceapfá|cheapann|ceapann|cheapaim|cheapfá)\b|"
    r"\b(?:an|is|ní) dóigh\b|\ban léiríonn\b|"
    r"\ban bhfuil\b|\btá:\s*níl:", re.I)
CLASSIFICATIONS = {
    'exam-question-selection', 'finite-route', 'answer-classification',
    'required-headings', 'scenario-choice', 'not-a-task-selection',
}
REVIEW_DIR = Path(__file__).with_name('reviews')


def paper_key(paper):
    return (paper['year'], paper['level'], paper['lang'],
            paper['fileid'].removesuffix('.pdf'))


def directives(path):
    with fitz.open(path) as document:
        return Counter(
            (page_number, text)
            for page_number, page in enumerate(document, 1)
            for line in page.get_text(sort=True).splitlines()
            if DIRECTIVE.search(text := ' '.join(line.split()))
        )


def validate_review(review, indexed):
    source_paths = {}
    for kind, folder, fileid in [
        ('paper', 'exampapers', indexed['fileid']),
        ('scheme', 'markingschemes', indexed['schemeFileid']),
    ]:
        path = ROOT / 'paper-trail-corpus' / folder / str(indexed['year']) / fileid
        if hashlib.sha256(path.read_bytes()).hexdigest() != review[kind + 'Sha256']:
            raise ValueError(f"Changed {kind} source: {paper_key(indexed)}")
        source_paths[kind] = path
    reviewed = Counter((item['page'], item['text']) for item in review['selections'])
    actual = directives(source_paths['paper'])
    if actual != reviewed:
        raise ValueError(f"Directive review mismatch: {paper_key(indexed)}; "
                         f"unclassified={list((actual - reviewed).elements())}; "
                         f"stale={list((reviewed - actual).elements())}")
    for item in review['selections']:
        if item['classification'] not in CLASSIFICATIONS or not item['reason'].strip():
            raise ValueError(f'Unexplained selection: {item}')
    tasks = [task for q in review['questions'] for task in q['tasks']]
    if len({task['cardId'] for task in tasks}) != len(tasks):
        raise ValueError('Repeated card in independent task census')
    for kind in source_paths:
        with fitz.open(source_paths[kind]) as document:
            for question in review['questions']:
                pages = question[kind + 'Pages']
                if not pages or any(page < 1 or page > len(document) for page in pages):
                    raise ValueError(f"Invalid {kind} evidence pages: {question['n']}")
    # Targeted evidence can resolve a displaced tariff without pretending that
    # the complete second language edition has been reviewed. Bind it to its
    # own physical PDFs, rather than accepting an unchecked footnote.
    targeted = review.get('targetedIrishEvidence')
    if targeted:
        if (targeted.get('lang') != 'iv' or not targeted.get('notFullEditionReview')
                or not targeted.get('reason', '').strip()):
            raise ValueError('Invalid targeted Irish evidence scope')
        for kind, folder in [('paper', 'exampapers'), ('scheme', 'markingschemes')]:
            path = (ROOT / 'paper-trail-corpus' / folder / str(review['year'])
                    / (targeted['fileid'].removesuffix('.pdf') + '.pdf'))
            if hashlib.sha256(path.read_bytes()).hexdigest() != targeted[kind + 'Sha256']:
                raise ValueError(f'Changed targeted Irish {kind} source')
            with fitz.open(path) as document:
                pages = targeted.get(kind + 'Pages')
                if not pages or any(p < 1 or p > len(document) for p in pages):
                    raise ValueError(f'Invalid targeted Irish {kind} pages')


def validate_equivalences(reviews):
    for key, review in reviews.items():
        equivalent = review.get('equivalentTo')
        if not equivalent:
            continue
        primary_key = (review['year'], review['level'], equivalent['lang'],
                       equivalent['fileid'])
        primary = reviews.get(primary_key)
        if not primary or primary.get('equivalentTo') or primary_key == key:
            raise ValueError(f'Unreviewed or circular equivalent edition: {key}')
        primary_questions = {q['n']: q for q in primary['questions']}
        if set(primary_questions) != {q['n'] for q in review['questions']}:
            raise ValueError(f'Equivalent edition omits a question: {key}')
        for question in review['questions']:
            if not question.get('equivalenceReason', '').strip():
                raise ValueError(f"Unexplained edition equivalence: {key} Q{question['n']}")
            allocation = question.get('allocationEvidence')
            if allocation:
                primary_question = primary_questions[question['n']]
                if (allocation.get('lang') != primary['lang']
                        or allocation.get('fileid') != primary['fileid']
                        or not allocation.get('reason', '').strip()
                        or not allocation.get('schemePages')
                        or not set(allocation['schemePages']).issubset(primary_question['schemePages'])):
                    raise ValueError(f"Invalid cross-edition allocation evidence: {key} Q{question['n']}")
            def routes(q):
                return {(t['key'], t['cardId'], t['marks'], t['topicId']) for t in q['tasks']}
            if routes(question) != routes(primary_questions[question['n']]):
                raise ValueError(f"Equivalent edition has different tasks: {key} Q{question['n']}")


def reviewed_papers():
    indexed = {paper_key(p): p for p in indexed_papers()}
    result = {}
    for path in sorted(REVIEW_DIR.glob('economics-*.json')):
        review = json.loads(path.read_text())
        key = paper_key(review)
        if key not in indexed or key in result:
            raise ValueError(f'Stale or duplicate reviewed paper: {key}')
        validate_review(review, indexed[key])
        result[key] = review
    validate_equivalences(result)
    return indexed, result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--allow-pending', action='store_true')
    args = parser.parse_args()
    indexed, reviewed = reviewed_papers()
    pending = len(indexed) - len(reviewed)
    print(f'Economics source review: {len(reviewed)}/{len(indexed)} paper variants; '
          f'{pending} pending; reviewed source/directive checks passed.')
    if pending and not args.allow_pending:
        raise SystemExit('Economics is incomplete: the remaining physical papers require review.')


if __name__ == '__main__':
    main()
