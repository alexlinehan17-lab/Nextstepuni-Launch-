"""2011 Ordinary legacy Paper 2: all 74 tasks under the original deduction rules."""
import hashlib
import json
import sys
from collections import defaultdict
from pathlib import Path
from review_lib import Paper, quotes

BASE = Path(__file__).resolve().parent
SOURCE = json.loads((BASE / '2011-ol-p2-source-review.json').read_text())
PRESENTATION = json.loads((BASE / '2011-ol-p2-presentation.json').read_text())
ROWS = {'maths-2011-ol-p2-q' + suffix: view['rows'] for suffix, view in PRESENTATION['tasks'].items()}
MARKS = {str(n): 50 for n in range(1, 12)}


def build_paper():
    p = Paper(2011, 'ol', 'p2', {}, SOURCE['paperFileid'], SOURCE['schemeFileid'],
              reviewed_at='2026-10-30', full_credit_minus_one=False)
    assert hashlib.sha256(p.P.read_bytes()).hexdigest() == SOURCE['paperSha256']
    assert hashlib.sha256(p.S.read_bytes()).hexdigest() == SOURCE['schemeSha256']
    for task in SOURCE['tasks']:
        view = PRESENTATION['tasks'][task['suffix']]
        extra = {'markingNote': task['markingNote']} if task.get('markingNote') else None
        p.D(task['suffix'], ','.join(task['printedParts']), task['methods'], task['schemePages'],
            task['sourcePages'], view['topic'], view['atlas'], task['questionText'], task.get('stem'), extra)
        assert p.cards[-1]['totalMarks'] == task['totalMarks']
    p.check(MARKS, 74)
    return p


def figure_bindings():
    counts = defaultdict(int)
    result = {}
    for task in SOURCE['tasks']:
        page = task['schemePages'][0]
        result['maths-2011-ol-p2-q' + task['suffix']] = f'maths-2011-OL-scheme-p{page:03}-i{counts[page]}'
        counts[page] += 1
    return result


def classify(text):
    if 'Attempt FIVE' in text or 'Attempt ONE' in text:
        return 'whole-examination-selection', SOURCE['selectionReview'][0]
    if 'any two sides' in text:
        return 'universal-theorem', SOURCE['selectionReview'][2]
    raise ValueError('Unclassified selection directive: ' + text)


def write_review(p):
    p.review(MARKS,
        'Independent visual inspection of all twelve original paper pages and scheme pages 45–104, all eleven questions, every published marking allocation, restricted award list, alternative solution and relevant note. All 74 question and 74 solution presentations inspected.',
        SOURCE['schemePagesInspected'], SOURCE['generalNotesPages'],
        SOURCE['selectionReview'] + SOURCE['markingRules'] + SOURCE['taskBoundaryReview'], [
            {'pages': [1, 2, 8], 'wording': 'Attempt FIVE questions from Section A and ONE question from Section B.', 'classification': 'whole-examination-selection', 'reason': SOURCE['selectionReview'][0]},
            {'pages': [4], 'wording': 'Prove that the sum of the lengths of any two sides of a triangle is greater than that of the third side.', 'classification': 'universal-theorem', 'reason': SOURCE['selectionReview'][2]},
        ], classify)


def main():
    if len(sys.argv) > 1:
        quotes(ROWS, sys.argv[1])
        return
    assert PRESENTATION['status'] == 'visually inspected', 'Inspect every crop before publication'
    p = build_paper()
    write_review(p)
    overrides = {cid: {'section': 'A' if int(cid.split('-q')[1].split('-')[0]) <= 7 else 'B', 'figureKey': key} for cid, key in figure_bindings().items()}
    p.apply(ROWS, '2011 Ordinary Paper 2', expect_added=[c['id'] for c in p.cards],
            card_overrides=overrides, question_figures=True)


if __name__ == '__main__':
    main()
