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
import itertools
import json
from pathlib import Path

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
    route_ids = []
    for route, options in pools.items():
        cid = f'agsci-2022-ol-q2bii-route-{route.lower()}'
        route_ids.append(cid)
        cards.append(card(cid, 2022, 'ordinary', f'{ref} — breed {route}', 'agsci-4-3-2',
            'selecting-a-ram-for-replacement-ewes', question, 4, [{
                'id': 'reasons', 'kind': 'anyN', 'verbatim': ' / '.join(options), 'marks': 4,
                'contextNote': f'Use the scheme’s reasons for breed {route}. Credit two distinct reasons; synonymous descriptions of the same trait count once. The first correct reason earns 3 marks and the second earns 1.',
                'group': {'claimMax': 2, 'perOption': 3, 'perOptionSteps': [3, 1], 'options': options},
            }], 5, 'Ram photographs E and F',
            f'Practice choice: breed {route}. Jessica is looking to buy a ram to breed replacements with her Suffolk cross ewes.'))
    reviews.append({
        'questionRef': ref, 'paperPage': 5, 'schemePage': 12,
        'selection': {'kind': 'closed', 'choose': 1, 'options': ['E', 'F']},
        'cardIds': route_ids, 'marksPerRoute': 4,
        'examTopicIds': ['agricultural-science-ordinary-animal-production'],
        'evidence': 'Paper and scheme visually inspected. The scheme separates E and F reason pools, each with 3+1. All eight E entries and all five F entries are retained. These are accepted answers, not a printed finite pool of reason choices.',
    })

    ref = '2023 HL Q18(a)(i)'
    answers = {'A': 'Teat', 'B': 'Median suspensory ligament',
               'C': 'Connective tissue / fine membrane', 'D': 'Epidermis / hind quarter / outer wall'}
    route_ids = []
    for letters in itertools.combinations(answers, 3):
        cid = f'agsci-2023-hl-q18ai-route-{"".join(letters).lower()}'
        route_ids.append(cid)
        cards.append(card(cid, 2023, 'higher', f'{ref} — {", ".join(letters)}', 'agsci-4-1',
            'udder-structure', 'Label any three parts of the structure of the udder.', 3,
            [{'id': f'label-{letter.lower()}', 'kind': 'point', 'verbatim': answers[letter],
              'marks': 1, 'contextNote': f'Label {letter}.'} for letter in letters],
            37, 'Udder structure', f'Practice choice: label {", ".join(letters)} on the official udder diagram.'))
    reviews.append({
        'questionRef': ref, 'paperPage': 37, 'schemePage': 27,
        'selection': {'kind': 'closed', 'choose': 3, 'options': list(answers)},
        'cardIds': route_ids, 'marksPerRoute': 3,
        'examTopicIds': ['agricultural-science-higher-dairy-cattle'],
        'evidence': 'Paper and scheme visually inspected. Four labelled structures, any three at 1 mark each: all four combinations. B is the complete phrase Median suspensory ligament, present in the scheme’s block-order extraction.',
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
    return cards, {'status': 'in-progress', 'reviewedAt': '2026-10-07',
                   'addedCardIds': [c['id'] for c in cards if c['id'] != 'agsci-2025-ol-q8b'],
                   'correctedCardIds': ['agsci-2025-ol-q8b'], 'tasks': reviews}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true')
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    cards, review = reviewed_tasks()
    existing = json.loads(AUTHORED.read_text())
    by_id = {c['id']: c for c in existing}
    if args.check:
        assert all(by_id.get(c['id']) == c for c in cards), 'Reviewed cards missing or stale'
        assert json.loads(REVIEW.read_text()) == review, 'Review record stale'
        print(f'OK: {len(cards)} cards for {len(review["tasks"])} reviewed tasks; full corpus review remains open')
    elif args.write:
        # Updates are allowed only for this script's own previously recorded IDs.
        managed = {cid for task in json.loads(REVIEW.read_text())['tasks'] for cid in task['cardIds']} if REVIEW.exists() else set()
        if 'agsci-2025-ol-q8b' not in managed:
            old = by_id['agsci-2025-ol-q8b']
            assert old['rows'] == [{'id': 'r-1', 'kind': 'point', 'verbatim': 'Symbols 2 and 3', 'marks': 5}], 'The independently verified correction needs re-review'
            managed.add(old['id'])
        for c in cards:
            assert c['id'] not in by_id or c['id'] in managed, f'Refusing to replace prior card {c["id"]}'
        revised = [c for c in existing if c['id'] not in managed] + cards
        assert set(by_id) <= {c['id'] for c in revised}, 'Refusing to remove an existing card'
        AUTHORED.write_text(json.dumps(revised, ensure_ascii=False, indent=1) + '\n')
        REVIEW.write_text(json.dumps(review, ensure_ascii=False, indent=2) + '\n')
        print(f'Wrote {len(cards)} reviewed cards; preserved every existing ID')
    else:
        print(json.dumps(review, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
