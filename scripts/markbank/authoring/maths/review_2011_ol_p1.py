"""2011 Ordinary legacy Paper 1: all 49 tasks under the original deduction rules."""
import hashlib
import json
import sys
from collections import defaultdict
from pathlib import Path
from review_lib import Paper, quotes

BASE = Path(__file__).resolve().parent
SOURCE = json.loads((BASE / '2011-ol-p1-source-review.json').read_text())
PRESENTATION = json.loads((BASE / '2011-ol-p1-presentation.json').read_text())
ROWS = {'maths-2011-ol-p1-q' + suffix: view['rows'] for suffix, view in PRESENTATION['tasks'].items()}
MARKS = {str(n): 50 for n in range(1, 9)}


def build_paper():
    p = Paper(2011, 'ol', 'p1', {}, SOURCE['paperFileid'], SOURCE['schemeFileid'],
              reviewed_at='2026-10-30', full_credit_minus_one=False)
    assert hashlib.sha256(p.P.read_bytes()).hexdigest() == SOURCE['paperSha256']
    assert hashlib.sha256(p.S.read_bytes()).hexdigest() == SOURCE['schemeSha256']
    for task in SOURCE['tasks']:
        view = PRESENTATION['tasks'][task['suffix']]
        extra = {'markingNote': task['markingNote']} if task.get('markingNote') else None
        p.D(task['suffix'], ','.join(task['printedParts']), task['methods'], task['schemePages'],
            task['sourcePages'], view['topic'], view['atlas'], task['questionText'], task.get('stem'), extra)
        assert p.cards[-1]['totalMarks'] == task['totalMarks']
    p.check(MARKS, 49)
    return p


def figure_bindings():
    counts = defaultdict(int)
    result = {}
    for task in SOURCE['tasks']:
        page = task['schemePages'][0]
        result['maths-2011-ol-p1-q' + task['suffix']] = f'maths-2011-OL-scheme-p{page:03}-i{counts[page]}'
        counts[page] += 1
    return result


def classify(text):
    if 'Attempt SIX QUESTIONS' in text:
        return 'whole-examination-selection', SOURCE['selectionReview'][0]
    if 'Verify one of your solutions' in text:
        return 'derived-answer-verification', SOURCE['selectionReview'][1]
    if 'Hence, or otherwise' in text:
        return 'open-method-choice', SOURCE['selectionReview'][2]
    raise ValueError('Unclassified selection directive: ' + text)


def write_review(p):
    p.review(MARKS,
        'Independent visual inspection of all eight original paper pages and scheme pages 1–44, including all eight questions, published allocations, attempt floors and every alternative solution. All 49 question and 49 complete solution presentations inspected.',
        SOURCE['schemePagesInspected'], SOURCE['generalNotesPages'],
        SOURCE['selectionReview'] + SOURCE['markingRules'] + SOURCE['taskBoundaryReview'] + [
            'Q6(b)(ii) explains the omitted x = 0 domain restriction and preserves x ≠ 3 in the answer.',
            'Q7(b)(ii) explains the extra power in the original substitution definition.',
            'Q8(iv) explains the difference between the printed unbounded interval and the requested plotted domain.',
        ], [
            {'pages': [1], 'wording': 'Attempt SIX QUESTIONS (50 marks each).', 'classification': 'whole-examination-selection', 'reason': SOURCE['selectionReview'][0]},
            {'pages': [3], 'wording': 'Verify one of your solutions.', 'classification': 'derived-answer-verification', 'reason': SOURCE['selectionReview'][1]},
            {'pages': [3], 'wording': 'Hence, or otherwise, find the real numbers k and t', 'classification': 'open-method-choice', 'reason': SOURCE['selectionReview'][2]},
        ], classify)


def main():
    if len(sys.argv) > 1:
        quotes(ROWS, sys.argv[1])
        return
    assert PRESENTATION['status'] == 'visually inspected', 'Inspect every crop before publication'
    p = build_paper()
    write_review(p)
    overrides = {cid: {'section': 'A', 'figureKey': key} for cid, key in figure_bindings().items()}
    p.apply(ROWS, '2011 Ordinary Paper 1', expect_added=[c['id'] for c in p.cards],
            card_overrides=overrides, question_figures=True)


if __name__ == '__main__':
    main()
