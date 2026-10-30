"""2012 Higher Paper 1: 45 tasks under the SEC step/deduction rules."""
import json
import sys
from collections import defaultdict
from pathlib import Path
from review_lib import Paper, quotes

BASE = Path(__file__).resolve().parent
SOURCE = json.loads((BASE / '2012-hl-p1-source-review.json').read_text())
PRESENTATION = json.loads((BASE / '2012-hl-p1-presentation.json').read_text())
ROWS = {'maths-2012-hl-p1-q' + suffix: task['rows'] for suffix, task in PRESENTATION['tasks'].items()}


def build_paper():
    p = Paper(2012, 'hl', 'p1', {}, SOURCE['paperFileid'], SOURCE['schemeFileid'],
              reviewed_at='2026-10-29', full_credit_minus_one=False)
    for task in SOURCE['tasks']:
        view = PRESENTATION['tasks'][task['suffix']]
        extra = {'markingNote': task['markingNote']} if task.get('markingNote') else None
        p.D(task['suffix'], ','.join(task['printedParts']), task['methods'], task['schemePages'],
            task['sourcePages'], view['topic'], view['atlas'], task['questionText'], task.get('stem'), extra)
    p.check({str(n): 50 for n in range(1, 9)}, 45)
    return p


def figure_bindings():
    counts = defaultdict(int); result = {}
    for task in SOURCE['tasks']:
        page = task['schemePages'][0]
        result['maths-2012-hl-p1-q' + task['suffix']] = f'maths-2012-HL-scheme-p{page:03}-i{counts[page]}'
        counts[page] += 1
    return result


def classify(text):
    if 'Attempt SIX QUESTIONS' in text:
        return 'whole-examination-selection', SOURCE['selectionReview'][0]
    raise ValueError('Unclassified selection directive: ' + text)


def main():
    if len(sys.argv) > 1:
        quotes(ROWS, sys.argv[1]); return
    assert PRESENTATION['status'] == 'visually inspected', 'Inspect all question and solution crops before publication'
    p = build_paper()
    p.review({str(n): 50 for n in range(1, 9)},
        'Independent visual inspection of all eight original paper pages and scheme pages 1–43, including every task, alternative model, step allocation, attempt floor and task-specific deduction. All 45 question and 45 complete solution images inspected.',
        list(range(1, 44)), [4, 5], SOURCE['selectionReview'] + SOURCE['markingRules'] + [
            'Q7(c)(iii) is explicitly Hit or Miss (0 or 5), overriding the question summary’s generic attempt marks.',
            'Historical matrix tasks are retained in algebra. Typeset original matrices, integrals, proofs and diagrams remain visible.',
            'Shared marking-note blocks are retained with a labelled note; only deductions relevant to the named task apply.'
        ], [
            {'pages': [1], 'wording': 'Attempt SIX QUESTIONS (50 marks each).', 'classification': 'whole-examination-selection', 'reason': SOURCE['selectionReview'][0]},
            {'pages': [2, 3, 4, 5], 'wording': 'all values; three roots; two possible values; all natural numbers; all further approximations', 'classification': 'all-required', 'reason': SOURCE['selectionReview'][1]},
            {'pages': [2], 'wording': 'Given any value of k ≠ 0', 'classification': 'open-parameter', 'reason': SOURCE['selectionReview'][2]},
        ], classify)
    overrides = {cid: {'section': 'A', 'figureKey': key} for cid, key in figure_bindings().items()}
    p.apply(ROWS, '2012 Higher Paper 1', expect_added=[c['id'] for c in p.cards],
            card_overrides=overrides, question_figures=True)


if __name__ == '__main__':
    main()
