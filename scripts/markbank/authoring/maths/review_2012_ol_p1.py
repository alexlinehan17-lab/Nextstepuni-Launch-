"""2012 Ordinary Paper 1: 48 tasks under the SEC step/deduction rules."""
import json
import sys
from collections import defaultdict
from pathlib import Path
from review_lib import Paper, quotes

BASE = Path(__file__).resolve().parent
SOURCE = json.loads((BASE / '2012-ol-p1-source-review.json').read_text())
PRESENTATION = json.loads((BASE / '2012-ol-p1-presentation.json').read_text())
ROWS = {'maths-2012-ol-p1-q' + suffix: task['rows'] for suffix, task in PRESENTATION['tasks'].items()}


def build_paper():
    p = Paper(2012, 'ol', 'p1', {}, SOURCE['paperFileid'], SOURCE['schemeFileid'],
              reviewed_at='2026-10-29', full_credit_minus_one=False)
    for task in SOURCE['tasks']:
        view = PRESENTATION['tasks'][task['suffix']]
        extra = {'markingNote': task['markingNote']} if task.get('markingNote') else None
        p.D(task['suffix'], ','.join(task['printedParts']), task['methods'], task['schemePages'],
            task['sourcePages'], view['topic'], view['atlas'], task['questionText'], task.get('stem'), extra)
    p.check({str(n): 50 for n in range(1, 9)}, 48)
    return p


def figure_bindings():
    counts = defaultdict(int); result = {}
    for task in SOURCE['tasks']:
        page = task['schemePages'][0]
        result['maths-2012-ol-p1-q' + task['suffix']] = f'maths-2012-OL-scheme-p{page:03}-i{counts[page]}'
        counts[page] += 1
    return result


def classify(text):
    if 'Attempt SIX QUESTIONS' in text:
        return 'whole-examination-selection', SOURCE['selectionReview'][0]
    if 'Hence, or otherwise' in text:
        return 'open-method-choice', 'Use the earlier division or another valid method to find all remaining factors; no finite option pool.'
    raise ValueError('Unclassified selection directive: ' + text)


def main():
    if len(sys.argv) > 1:
        quotes(ROWS, sys.argv[1]); return
    assert PRESENTATION['status'] == 'visually inspected', 'Inspect all question and solution crops before publication'
    p = build_paper()
    p.review({str(n): 50 for n in range(1, 9)},
        'Independent visual inspection of all eight original paper pages and scheme pages 1–36, including every task, alternative model, step allocation, attempt floor and task-specific deduction. All 48 question and 48 complete solution images inspected.',
        list(range(1, 37)), [4, 5], SOURCE['selectionReview'] + SOURCE['markingRules'] + [
            'Q2(c)(ii) and Q4(c) use their explicit award lists, not all intermediate deduction scores.',
            'Typeset fractions, powers, complex numbers, graph read-offs and every printed solution method remain visible.',
            'Shared marking-note blocks are retained with a labelled note; only deductions relevant to the named task apply.'
        ], [
            {'pages': [1], 'wording': 'Attempt SIX QUESTIONS (50 marks each).', 'classification': 'whole-examination-selection', 'reason': SOURCE['selectionReview'][0]},
            {'pages': [2, 3, 4, 5], 'wording': 'values; other factors; solutions; terms; graph estimates; proofs', 'classification': 'all-required', 'reason': SOURCE['selectionReview'][1]},
        ], classify)
    overrides = {cid: {'section': 'A', 'figureKey': key} for cid, key in figure_bindings().items()}
    p.apply(ROWS, '2012 Ordinary Paper 1', expect_added=[c['id'] for c in p.cards],
            card_overrides=overrides, question_figures=True)


if __name__ == '__main__':
    main()
