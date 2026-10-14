#!/usr/bin/env python3
"""Add independently reviewed Agricultural Science tasks without replacing cards.

This is an incremental review, NOT a claim of corpus completeness. Source page
numbers are PDF pages, including the two unnumbered 2022 OL scheme pages.
Every finite response choice below is expanded mechanically. Open answer pools
remain bounded marking menus; identifying the two correct signs is not a choice
of examination route. Run with --write, or --check to verify generated content.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from agricultural_science_2010_hl import reviewed_tasks as reviewed_2010_hl, paper_review
from agricultural_science_2010_ol import reviewed_tasks as reviewed_2010_ol, paper_review as ordinary_2010_review
from agricultural_science_2010_parity import paper_reviews as irish_2010_reviews
from agricultural_science_2010_irish_crops import attach_sources
from agricultural_science_2011_hl import reviewed_tasks as reviewed_2011_hl, paper_review as higher_2011_review
from agricultural_science_2011_irish import paper_review as irish_2011_review, attach_sources as attach_2011_sources
from agricultural_science_2011_ol_irish import paper_review as irish_2011_ordinary_review, attach_sources as attach_2011_ordinary_sources
from agricultural_science_2011_ol import reviewed_tasks as reviewed_2011_ol, paper_review as ordinary_2011_review

from agricultural_science_2012_hl import reviewed_tasks as reviewed_2012_hl, paper_review as higher_2012_review
from agricultural_science_2026_hl import reviewed_tasks as reviewed_2026_hl, paper_review as higher_2026_review
from agricultural_science_2026_ol import reviewed_tasks as reviewed_2026_ol, paper_review as ordinary_2026_review
from agricultural_science_2025_hl import reviewed_tasks as reviewed_2025_hl, paper_review as higher_2025_review, SNAPSHOT, original_hash, RESTORED as RESTORED_2025_HL, WITHDRAWN
from agricultural_science_2025_ol import reviewed_tasks as reviewed_2025_ol, paper_review as ordinary_2025_review
from agricultural_science_2024_hl import reviewed_tasks as reviewed_2024_hl, paper_review as higher_2024_review, RESTORED as RESTORED_2024_HL
from agricultural_science_2024_ol import reviewed_tasks as reviewed_2024_ol, paper_review as ordinary_2024_review
from agricultural_science_2023_hl import reviewed_tasks as reviewed_2023_hl, paper_review as higher_2023_review, RESTORED as RESTORED_2023_HL
from agricultural_science_2023_ol import reviewed_tasks as reviewed_2023_ol, paper_review as ordinary_2023_review, RESTORED as RESTORED_2023_OL
from agricultural_science_2022_hl import reviewed_tasks as reviewed_2022_hl, paper_review as higher_2022_review, RESTORED as RESTORED_2022_HL
from agricultural_science_2022_ol import reviewed_tasks as reviewed_2022_ol, paper_review as ordinary_2022_review, RESTORED as RESTORED_2022_OL, WITHDRAWN as WITHDRAWN_2022_OL
from agricultural_science_2021_hl import reviewed_tasks as reviewed_2021_hl, paper_review as higher_2021_review, RESTORED as RESTORED_2021_HL
from agricultural_science_2021_ol import reviewed_tasks as reviewed_2021_ol, paper_review as ordinary_2021_review, RESTORED as RESTORED_2021_OL
from agricultural_science_2020_hl import reviewed_tasks as reviewed_2020_hl, paper_review as higher_2020_review
from agricultural_science_2020_ol import reviewed_tasks as reviewed_2020_ol, paper_review as ordinary_2020_review
from agricultural_science_2019_hl import reviewed_tasks as reviewed_2019_hl, paper_review as higher_2019_review
from agricultural_science_2019_ol import reviewed_tasks as reviewed_2019_ol, paper_review as ordinary_2019_review
from agricultural_science_2018_hl import reviewed_tasks as reviewed_2018_hl, paper_review as higher_2018_review
from agricultural_science_2018_ol import reviewed_tasks as reviewed_2018_ol, paper_review as ordinary_2018_review
from agricultural_science_2017_hl import reviewed_tasks as reviewed_2017_hl, paper_review as higher_2017_review

ROOT = Path(__file__).resolve().parents[3]
AUTHORED = ROOT / 'scripts/markbank/authored/agricultural-science.json'
REVIEW = ROOT / 'scripts/markbank/authored/agricultural-science-reviewed-tasks.json'


def source(year, level, page, title):
    return {
        'kind': 'source-illustration', 'label': 'OFFICIAL QUESTION PAGE',
        'title': title, 'pages': [page],
        'attribution': f'SEC Agricultural Science {year} {level.title()} Level examination paper — © State Examinations Commission.',
        'presentationNote': 'Open the exact examination page to use its published photograph, diagram or answer space.',
    }


def card(cid, year, level, ref, topic, concept, question, marks, rows, page, title, stem=None):
    result = {
        'id': cid, 'subjectId': 'agricultural-science', 'year': year,
        'level': level, 'section': 'A' if int(ref.split('Q')[1].split('(')[0]) <= 12 else 'B',
        'questionRef': ref, 'topicId': topic, 'conceptId': concept,
        'questionText': question, 'tariffModel': {'kind': 'fixed'},
        'totalMarks': marks, 'rows': rows,
        'sourceMaterial': source(year, level, page, title),
    }
    if stem:
        result['stem'] = stem
    return result


def reviewed_tasks():
    cards, reviews = [], []
    ref = '2022 OL Q2(b)(ii)'
    question = ('Jessica could choose either breed E or F to cross with her Suffolk cross ewes for '
                'replacements in her flock. Advise Jessica with reasons which breed to choose.')
    pools = {
        'E': ['good milk production', 'prolific', 'easy lambing', 'good mothers',
              'hardy or good survival rate', 'good growth rate', 'calm or easy to handle', 'maternal sire'],
        'F': ['hardy or good survival rate', 'prolific', 'good mothers', 'good growth rate', 'excellent conformation'],
    }
    # Item choice (breed E or F) is ONE practice card: one anyN row over both
    # breeds' scheme reasons, claim limit two at 3+1 (coordinator rule, 2026-10-12).
    options = list(dict.fromkeys(pools['E'] + pools['F']))
    cid = 'agsci-2022-ol-q2bii'
    cards.append(card(cid, 2022, 'ordinary', ref, 'agsci-4-3-2',
        'selecting-a-ram-for-replacement-ewes', question, 4, [{
            'id': 'reasons', 'kind': 'anyN', 'verbatim': ' / '.join(options), 'marks': 4,
            'contextNote': 'Two distinct reasons for the breed you choose; synonymous descriptions of the same trait count once. The first correct reason earns 3 marks and the second earns 1. '
                           'Breed E reasons: ' + ', '.join(pools['E']) + '. Breed F reasons: ' + ', '.join(pools['F']) + '.',
            'group': {'claimMax': 2, 'perOption': 3, 'perOptionSteps': [3, 1], 'options': options},
        }], 5, 'Ram photographs E and F', 'Jessica is looking to buy a ram to breed replacements with her Suffolk cross ewes.'))
    reviews.append({
        'questionRef': ref, 'paperPage': 5, 'schemePage': 12,
        'selection': {'kind': 'closed', 'choose': 1, 'options': ['E', 'F'], 'pooled': True},
        'cardIds': [cid], 'marksPerRoute': 4,
        'examTopicIds': ['agricultural-science-ordinary-animal-production'],
        'evidence': 'Paper and scheme visually inspected. The scheme separates E and F reason pools, each with 3+1. All eight E entries and all five F entries are retained on one card. These are accepted answers, not a printed finite pool of reason choices.',
    })

    cid, ref = 'agsci-2022-ol-q13bi', '2022 OL Q13(b)(i)'
    cards.append(card(cid, 2022, 'ordinary', ref, 'agsci-2-3', 'soil-sampling-pattern',
        'Sketch onto the photograph of field A below, the pattern the farmer would use when taking a number of soil samples. (Please use your pen).',
        4, [{'id': 'sampling-pattern', 'kind': 'criterion', 'verbatim': 'W shape on photograph', 'marks': 4}],
        22, 'Field A: soil sampling',
        'The photograph shows a grassland field where a farmer wants to carry out soil analysis. Use the official page for your sketch.'))
    reviews.append({
        'questionRef': ref, 'paperPage': 22, 'schemePage': 21,
        'selection': {'kind': 'none', 'reason': 'One drawing, marked as a single 4-mark criterion.'},
        'cardIds': [cid], 'marksPerRoute': 4,
        'examTopicIds': ['agricultural-science-ordinary-soil-science'],
        'evidence': 'Paper and scheme visually inspected. The field boundary and gate are retained in the source reader. The published answer is W shape on photograph, 4 marks; no invented partial drawing bands.',
    })

    cid, ref = 'agsci-2025-ol-q8b', '2025 OL Q8(b)'
    cards.append(card(cid, 2025, 'ordinary', ref, 'agsci-1-5', 'reading-fertiliser-hazard-symbols',
        'Orla noticed two warning signs on the fertiliser bags which identified it as an eye irritant and a fire risk. Choose the two warning signs by placing a tick (✓) in the correct boxes to identify these signs.',
        5, [{'id': 'warning-signs', 'kind': 'anyN', 'verbatim': 'Symbols 2 and 3', 'marks': 5,
             'contextNote': 'The symbols are numbered from left to right. The scheme awards 3 marks for the first correct symbol and 2 for the second.',
             'group': {'claimMax': 2, 'perOption': 3, 'perOptionSteps': [3, 2], 'options': ['2', '3']}}],
        9, 'Fertiliser warning signs'))
    reviews.append({
        'questionRef': ref, 'paperPage': 9, 'schemePage': 14,
        'selection': {'kind': 'answer-identification', 'reason': 'Select the two correct answers, not any two permitted examination routes. Expanding six pairs would create four knowingly incorrect tasks.'},
        'cardIds': [cid], 'marksPerRoute': 5,
        'examTopicIds': ['agricultural-science-ordinary-health-safety'],
        'evidence': 'Paper and scheme visually inspected. Scheme PDF page 14 explicitly prints Symbols 2 and 3 and 3+2. A two-option marking group represents partial credit without forcing an all-or-nothing five-mark tick.',
    })
    legacy_cards, legacy_reviews = reviewed_2010_hl()
    cards.extend(legacy_cards)
    reviews.extend(legacy_reviews)
    ordinary_cards, ordinary_reviews = reviewed_2010_ol()
    cards.extend(ordinary_cards)
    reviews.extend(ordinary_reviews)
    paper_reviews = [paper_review(), ordinary_2010_review(), *irish_2010_reviews()]
    attach_sources(reviews, paper_reviews)
    higher_2011_cards, higher_2011_tasks = reviewed_2011_hl()
    cards.extend(higher_2011_cards)
    reviews.extend(higher_2011_tasks)
    paper_reviews.append(higher_2011_review())
    translated_2011_review = irish_2011_review()
    attach_2011_sources(reviews, translated_2011_review)
    paper_reviews.append(translated_2011_review)
    ordinary_2011_cards, ordinary_2011_tasks = reviewed_2011_ol()
    cards.extend(ordinary_2011_cards)
    reviews.extend(ordinary_2011_tasks)
    paper_reviews.append(ordinary_2011_review())
    translated_2011_ordinary_review = irish_2011_ordinary_review()
    attach_2011_ordinary_sources(reviews, translated_2011_ordinary_review)
    paper_reviews.append(translated_2011_ordinary_review)
    higher_2012_cards, higher_2012_tasks = reviewed_2012_hl()
    cards.extend(higher_2012_cards)
    reviews.extend(higher_2012_tasks)
    paper_reviews.append(higher_2012_review())
    higher_2026_cards, higher_2026_tasks = reviewed_2026_hl()
    cards.extend(higher_2026_cards)
    reviews.extend(higher_2026_tasks)
    paper_reviews.append(higher_2026_review())
    ordinary_2026_cards, ordinary_2026_tasks = reviewed_2026_ol()
    cards.extend(ordinary_2026_cards)
    reviews.extend(ordinary_2026_tasks)
    paper_reviews.append(ordinary_2026_review())
    # 2025 Higher reviews every original card; only corrected and added cards
    # are (re)written. Untouched originals are bound to Atlas, never rewritten.
    existing = {c['id']: c for c in json.loads(AUTHORED.read_text())}
    higher_2025_cards, higher_2025_tasks, corrections_2025 = reviewed_2025_hl(existing)
    cards.extend(higher_2025_cards)
    reviews.extend(higher_2025_tasks)
    paper_reviews.append(higher_2025_review())
    ordinary_2025_cards, ordinary_2025_tasks, corrections_2025_ol = reviewed_2025_ol(existing)
    cards.extend(ordinary_2025_cards)
    reviews.extend(ordinary_2025_tasks)
    paper_reviews.append(ordinary_2025_review())
    higher_2024_cards, higher_2024_tasks, corrections_2024 = reviewed_2024_hl(existing)
    cards.extend(higher_2024_cards)
    reviews.extend(higher_2024_tasks)
    paper_reviews.append(higher_2024_review())
    ordinary_2024_cards, ordinary_2024_tasks, corrections_2024_ol = reviewed_2024_ol(existing)
    cards.extend(ordinary_2024_cards)
    reviews.extend(ordinary_2024_tasks)
    paper_reviews.append(ordinary_2024_review())
    higher_2023_cards, higher_2023_tasks, corrections_2023 = reviewed_2023_hl(existing)
    cards.extend(higher_2023_cards)
    reviews.extend(higher_2023_tasks)
    paper_reviews.append(higher_2023_review())
    ordinary_2023_cards, ordinary_2023_tasks, corrections_2023_ol = reviewed_2023_ol(existing)
    cards.extend(ordinary_2023_cards)
    reviews.extend(ordinary_2023_tasks)
    paper_reviews.append(ordinary_2023_review())
    higher_2022_cards, higher_2022_tasks, corrections_2022 = reviewed_2022_hl(existing)
    cards.extend(higher_2022_cards)
    reviews.extend(higher_2022_tasks)
    paper_reviews.append(higher_2022_review())
    ordinary_2022_cards, ordinary_2022_tasks, corrections_2022_ol = reviewed_2022_ol(existing)
    cards.extend(ordinary_2022_cards)
    reviews.extend(ordinary_2022_tasks)
    paper_reviews.append(ordinary_2022_review())
    higher_2021_cards, higher_2021_tasks, corrections_2021 = reviewed_2021_hl(existing)
    cards.extend(higher_2021_cards)
    reviews.extend(higher_2021_tasks)
    paper_reviews.append(higher_2021_review())
    ordinary_2021_cards, ordinary_2021_tasks, corrections_2021_ol = reviewed_2021_ol(existing)
    cards.extend(ordinary_2021_cards)
    reviews.extend(ordinary_2021_tasks)
    paper_reviews.append(ordinary_2021_review())
    # Legacy sittings authored from the SEC sources: every card is new, none corrected.
    legacy_cards, legacy_dates = [], {}
    for legacy, legacy_review, reviewed_on in [(reviewed_2020_hl, higher_2020_review, '2026-10-13'),
                                               (reviewed_2020_ol, ordinary_2020_review, '2026-10-14'),
                                               (reviewed_2019_hl, higher_2019_review, '2026-10-14'),
                                               (reviewed_2019_ol, ordinary_2019_review, '2026-10-14'),
                                               (reviewed_2018_hl, higher_2018_review, '2026-10-14'),
                                               (reviewed_2018_ol, ordinary_2018_review, '2026-10-14'),
                                               (reviewed_2017_hl, higher_2017_review, '2026-10-14')]:
        new_cards, new_tasks = legacy()
        legacy_cards += new_cards
        legacy_dates.update({id(card): reviewed_on for card in new_cards})
        cards.extend(new_cards)
        reviews.extend(new_tasks)
        paper_reviews.append(legacy_review())
    corrections_2025 = {**corrections_2021_ol, **corrections_2021, **corrections_2022_ol, **corrections_2025, **corrections_2025_ol, **corrections_2024, **corrections_2024_ol, **corrections_2023, **corrections_2023_ol, **corrections_2022}
    # Batches reviewed after 7 October carry their own review date; earlier
    # reviewed card objects must stay byte-identical.
    batch_dates = {id(card): '2026-10-11' for card in higher_2026_cards + ordinary_2026_cards + higher_2025_cards + ordinary_2025_cards}
    batch_dates.update({id(card): '2026-10-12' for card in higher_2024_cards + ordinary_2024_cards + higher_2023_cards + ordinary_2023_cards + higher_2022_cards + ordinary_2022_cards})
    batch_dates.update({id(card): '2026-10-13' for card in higher_2021_cards + ordinary_2021_cards})
    batch_dates.update(legacy_dates)
    for reviewed in cards:
        reviewed['qa'] = {'gates':['verbatim','tariff','figure','source-crop'],
                          'humanReviewedBy':'agent-source-reviewed','humanReviewedAt':batch_dates.get(id(reviewed),'2026-10-07')}
    corrected = ['agsci-2025-ol-q8b', *sorted(corrections_2025)]
    # Originals an earlier review rewrote and this one restores byte-identical:
    # kept as they were on main, or withdrawn as progress aliases of a pooled card.
    restored = [*RESTORED_2025_HL, *RESTORED_2024_HL, *RESTORED_2023_HL, *RESTORED_2023_OL, *RESTORED_2022_HL, *RESTORED_2022_OL, *RESTORED_2021_HL, *RESTORED_2021_OL]
    assert not {c['id'] for c in restored} & {c['id'] for c in cards}
    return cards, restored, {'status': 'in-progress', 'reviewedAt': '2026-10-07',
                   'addedCardIds': [c['id'] for c in cards if c['id'] not in corrected],
                   'correctedCardIds': corrected,
                   'withdrawnCardIds': dict(sorted({**WITHDRAWN, **WITHDRAWN_2022_OL}.items())),
                   'corrections': {cid: {k: v for k, v in record.items()} for cid, record in sorted(corrections_2025.items())},
                   'tasks': reviews, 'paperReviews': paper_reviews}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true')
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    cards, restored, review = reviewed_tasks()
    existing = json.loads(AUTHORED.read_text())
    by_id = {c['id']: c for c in existing}
    restored_ids = {c['id'] for c in restored}
    if args.check:
        assert all(by_id.get(c['id']) == c for c in cards), 'Reviewed cards missing or stale'
        assert all(by_id.get(c['id']) == c for c in restored), 'Restored originals missing or changed'
        assert json.loads(REVIEW.read_text()) == review, 'Review record stale'
        print(f'OK: {len(cards)} cards for {len(review["tasks"])} reviewed tasks; full corpus review remains open')
    elif args.write:
        # Updates are allowed only for this script's own previously written IDs:
        # its additions and its recorded corrections. Reviewed-but-untouched
        # original cards are never rewritten.
        previous = json.loads(REVIEW.read_text()) if REVIEW.exists() else {}
        managed = set(previous.get('addedCardIds', [])) | set(previous.get('correctedCardIds', []))
        snapshot = json.loads(SNAPSHOT.read_text())
        for cid, record in review.get('corrections', {}).items():
            if cid not in managed:
                assert original_hash(by_id[cid]) == record['originalSha256'] == snapshot[cid]['originalSha256'], f'{cid} changed since its correction was reviewed'
                managed.add(cid)
        if 'agsci-2025-ol-q8b' not in managed:
            old = by_id['agsci-2025-ol-q8b']
            assert old['rows'] == [{'id': 'r-1', 'kind': 'point', 'verbatim': 'Symbols 2 and 3', 'marks': 5}], 'The independently verified correction needs re-review'
            managed.add(old['id'])
        for c in cards:
            assert c['id'] not in by_id or c['id'] in managed, f'Refusing to replace prior card {c["id"]}'
        for c in restored:
            assert c['id'] in managed or by_id.get(c['id']) == c, f'{c["id"]} changed outside a reviewed restore'
        revised = [c for c in existing if c['id'] not in managed and c['id'] not in restored_ids] + cards + restored
        # Only this script's own branch-only combination siblings may go: a
        # printed item choice is one card (coordinator rule, 2026-10-12). Any
        # other disappearance, or any card that existed before this audit, stops.
        removed = set(by_id) - {c['id'] for c in revised}
        assert all('-route-' in cid and cid in previous.get('addedCardIds', []) for cid in removed), f'Refusing to remove an existing card: {sorted(removed)[:5]}'
        AUTHORED.write_text(json.dumps(revised, ensure_ascii=False, indent=1) + '\n')
        REVIEW.write_text(json.dumps(review, ensure_ascii=False, indent=2) + '\n')
        print(f'Wrote {len(cards)} reviewed cards; preserved every existing ID')
    else:
        print(json.dumps(review, ensure_ascii=False, indent=2))
    return cards, restored


if __name__ == '__main__':
    main()
