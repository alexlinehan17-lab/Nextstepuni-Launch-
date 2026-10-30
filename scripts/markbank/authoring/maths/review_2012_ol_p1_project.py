"""2012 Ordinary Phase 3 Paper 1: all 35 published mark units."""
import json
import sys
from collections import defaultdict
from pathlib import Path
from review_lib import Paper, quotes

BASE = Path(__file__).resolve().parent
SOURCE = json.loads((BASE / '2012-ol-p1-project-source-review.json').read_text())
PRESENTATION = json.loads((BASE / '2012-ol-p1-project-presentation.json').read_text())
ROWS = {'maths-2012-ol-p1-project-q' + suffix: task['rows'] for suffix, task in PRESENTATION['tasks'].items()}
MARKS = {**{str(n): 25 for n in range(1, 7)}, **{str(n): 50 for n in range(7, 10)}}


def build_paper():
    p = Paper(2012, 'ol', 'p1', SOURCE['scales'], SOURCE['paperFileid'], SOURCE['schemeFileid'],
              reviewed_at='2026-10-30', edition='project', full_credit_minus_one=False)
    for task in SOURCE['tasks']:
        view = PRESENTATION['tasks'][task['suffix']]
        extra = {k: task[k] for k in ('fullCreditMinusOne', 'measurementRequired') if k in task}
        writer = p.C if 'components' in task else p.A
        writer(task['suffix'], ','.join(task['printedParts']), task.get('components', task.get('scale')),
               task['schemePages'], task['sourcePages'], view['topic'], view['atlas'],
               task['questionText'], stem=task.get('stem'), extra=extra)
    p.check(MARKS, 35)
    return p


def figure_bindings():
    counts = defaultdict(int); result = {}
    for task in SOURCE['tasks']:
        page = task['schemePages'][0]
        result['maths-2012-ol-p1-project-q' + task['suffix']] = f'maths-2012-OL-scheme-project-p{page:03}-i{counts[page]}'
        counts[page] += 1
    return result


def classify(text):
    if 'Answer all' in text:
        return 'all-required', 'All nine questions and every published mark unit are retained.'
    if 'One rule' in text:
        return 'given-model', 'Introduces Clark’s rule, not a choice of questions.'
    raise ValueError('Unclassified selection directive: ' + text)


def write_review(p):
    p.review(MARKS,
        'Independent visual inspection of all 20 original paper pages and scheme PDF pages 1–36, including every model, alternative, diagram, scale, component allocation and detailed credit note. All 35 question and 35 solution crops inspected.',
        SOURCE['schemePagesInspected'], SOURCE['generalNotesPages'], SOURCE['notes'], SOURCE['selectionReview'], classify)


def main():
    if len(sys.argv) > 1:
        quotes(ROWS, sys.argv[1]); return
    assert PRESENTATION['status'] == 'visually inspected', 'Inspect every question and solution crop before publication'
    p = build_paper()
    write_review(p)
    p.apply(ROWS, '2012 Ordinary Project Maths Phase 3 Paper 1', expect_added=[c['id'] for c in p.cards],
            card_overrides={cid: {'figureKey': key} for cid, key in figure_bindings().items()}, question_figures=True)


if __name__ == '__main__':
    main()
