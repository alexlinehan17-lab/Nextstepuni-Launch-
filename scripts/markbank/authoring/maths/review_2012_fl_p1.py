"""2012 Foundation Paper 1: 45 tasks under the SEC step/deduction rules."""
import json
import sys
from collections import defaultdict
from pathlib import Path
from review_lib import Paper, quotes

BASE = Path(__file__).resolve().parent
SOURCE = json.loads((BASE / '2012-fl-p1-source-review.json').read_text())
PRESENTATION = json.loads((BASE / '2012-fl-p1-presentation.json').read_text())
ROWS = {'maths-2012-fl-p1-q' + suffix: task['rows'] for suffix, task in PRESENTATION['tasks'].items()}
MARKS = {'1': 100, **{str(n): 50 for n in range(2, 8)}}


def build_paper():
    p = Paper(2012, 'fl', 'p1', {}, SOURCE['paperFileid'], SOURCE['schemeFileid'],
              reviewed_at='2026-10-29', full_credit_minus_one=False)
    for task in SOURCE['tasks']:
        view = PRESENTATION['tasks'][task['suffix']]
        extra = {'markingNote': task['markingNote']} if task.get('markingNote') else None
        p.D(task['suffix'], ','.join(task['printedParts']), task['methods'], task['schemePages'],
            task['sourcePages'], view['topic'], view['atlas'], task['questionText'], task.get('stem'), extra)
    p.check(MARKS, 45)
    return p


def figure_bindings():
    counts = defaultdict(int); result = {}; shared = {}
    for task in SOURCE['tasks']:
        page = task['schemePages'][0]
        digest = PRESENTATION['tasks'][task['suffix']]['inspectedSolutionSha256']
        if digest not in shared:
            shared[digest] = f'maths-2012-FL-scheme-p{page:03}-i{counts[page]}'
            counts[page] += 1
        result['maths-2012-fl-p1-q' + task['suffix']] = shared[digest]
    result['maths-2012-fl-p1-q5-b-i'] = 'maths-2012-FL-scheme-p029-i2'
    return result


def classify(text):
    if 'FOUR' in text:
        return 'whole-examination-selection', SOURCE['selectionReview'][0]
    if 'Hence, or otherwise' in text:
        return 'open-method-choice', SOURCE['selectionReview'][2]
    raise ValueError('Unclassified selection directive: ' + text)


def main():
    if len(sys.argv) > 1:
        quotes(ROWS, sys.argv[1]); return
    assert PRESENTATION['status'] == 'visually inspected', 'Inspect all question and solution crops before publication'
    p = build_paper()
    p.review(MARKS,
        'Independent visual inspection of all eight original paper pages and scheme pages 1–40, including all 45 task groups, alternative methods, 47 marking steps, attempt floors and task-specific deductions. All 45 question and 45 complete solution images inspected.',
        list(range(1, 41)), [4], SOURCE['selectionReview'] + SOURCE['markingRules'] + [
            'Typeset fractions, powers, graph read-offs and every published solution method remain visible.',
            'Shared marking-note panels are labelled; only the named task earns marks on its card.',
        ], [
            {'pages': [1], 'wording': 'Answer QUESTION 1 and FOUR other questions.', 'classification': 'whole-examination-selection', 'reason': SOURCE['selectionReview'][0]},
            {'pages': [2, 3, 4, 5], 'wording': 'first five multiples; solutions; two years; all values; graph estimates', 'classification': 'all-required', 'reason': SOURCE['selectionReview'][1]},
            {'pages': [4], 'wording': 'Hence, or otherwise', 'classification': 'open-method-choice', 'reason': SOURCE['selectionReview'][2]},
        ], classify)
    overrides = {cid: {'section': 'A', 'figureKey': key} for cid, key in figure_bindings().items()}
    p.apply(ROWS, '2012 Foundation Paper 1', expect_added=[c['id'] for c in p.cards],
            card_overrides=overrides, question_figures=True)


if __name__ == '__main__':
    main()
