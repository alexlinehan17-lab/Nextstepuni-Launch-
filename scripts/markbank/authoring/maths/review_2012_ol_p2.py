"""2012 Ordinary Phase 1 Paper 2: all 43 tasks and both geometry alternatives."""
import json
import sys
from collections import defaultdict
from pathlib import Path
from review_lib import Paper, quotes

BASE = Path(__file__).resolve().parent
SOURCE = json.loads((BASE / '2012-ol-p2-source-review.json').read_text())
PRESENTATION = json.loads((BASE / '2012-ol-p2-presentation.json').read_text())
ROWS = {'maths-2012-ol-p2-q' + suffix: task['rows'] for suffix, task in PRESENTATION['tasks'].items()}
MARKS = {**{str(n): 25 for n in range(1, 5)}, '5A': 25, '5B': 25, '6': 75, '7': 50, '8': 50}


def build_paper():
    p = Paper(2012, 'ol', 'p2', SOURCE['scales'], SOURCE['paperFileid'], SOURCE['schemeFileid'],
              reviewed_at='2026-10-29', full_credit_minus_one=False)
    for task in SOURCE['tasks']:
        view = PRESENTATION['tasks'][task['suffix']]
        extra = {k: task[k] for k in ('fullCreditMinusOne', 'measurementRequired') if k in task}
        writer = p.C if 'components' in task else p.A
        writer(task['suffix'], ','.join(task['printedParts']), task.get('components', task.get('scale')),
               task['schemePages'], task['sourcePages'], view['topic'], view['atlas'],
               task['questionText'], stem=task.get('stem'), extra=extra)
    p.check(MARKS, 43)
    return p


def figure_bindings():
    counts = defaultdict(int); result = {}
    for task in SOURCE['tasks']:
        page = task['schemePages'][0]
        result['maths-2012-ol-p2-q' + task['suffix']] = f'maths-2012-OL-scheme-p{page:03}-i{counts[page]}'
        counts[page] += 1
    return result


def classify(text):
    if 'either Question 5' in text or 'either 5A' in text:
        return 'expanded-alternatives', SOURCE['selectionReview'][0]['reason']
    if 'Answer all' in text:
        return 'all-required', 'All required tasks retained, including both complete Q5 alternatives.'
    if 'one of the ways' in text:
        return 'open-method-choice', SOURCE['selectionReview'][1]['reason']
    if 'either three boys' in text:
        return 'scenario-definition', 'Both predictions must be compared; this is probability data, not a selection of questions.'
    raise ValueError('Unclassified selection directive: ' + text)


def main():
    if len(sys.argv) > 1:
        quotes(ROWS, sys.argv[1]); return
    assert PRESENTATION['status'] == 'visually inspected', 'Inspect every question and solution crop before publication'
    p = build_paper()
    p.review(MARKS,
        'Independent visual inspection of all 20 original paper pages and scheme PDF pages 37–72, including every model, alternative proof, diagram, scale, component allocation and detailed credit note. All 43 question and 43 solution crops inspected.',
        SOURCE['schemePagesInspected'], SOURCE['generalNotesPages'], SOURCE['notes'], SOURCE['selectionReview'], classify)
    p.apply(ROWS, '2012 Ordinary Project Maths Phase 1 Paper 2', expect_added=[c['id'] for c in p.cards],
            card_overrides={c['id']: {'figureKey': figure_bindings()[c['id']], 'section': 'A' if int(c['printedParts'][0][1]) <= 5 else 'B' if int(c['printedParts'][0][1]) <= 7 else 'C'} for c in p.cards}, question_figures=True)


if __name__ == '__main__':
    main()
