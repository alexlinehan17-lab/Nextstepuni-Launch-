"""2011 Foundation Paper 2: all 49 tasks and 50 marking components."""
import hashlib
import json
import sys
import re
from collections import defaultdict
from pathlib import Path
from review_lib import Paper, quotes

BASE = Path(__file__).resolve().parent
SOURCE = json.loads((BASE / '2011-fl-p2-source-review.json').read_text())
PRESENTATION = json.loads((BASE / '2011-fl-p2-presentation.json').read_text())
PREFIX = 'maths-2011-fl-p2-q'
ROWS = {PREFIX + suffix: task['rows'] for suffix, task in PRESENTATION['tasks'].items()}


def build_paper():
    p = Paper(2011, 'fl', 'p2', {}, SOURCE['paperFileid'], SOURCE['schemeFileid'],
              reviewed_at='2026-10-30', full_credit_minus_one=False)
    assert hashlib.sha256(p.P.read_bytes()).hexdigest() == SOURCE['paperSha256']
    assert hashlib.sha256(p.S.read_bytes()).hexdigest() == SOURCE['schemeSha256']
    for task in SOURCE['tasks']:
        view = PRESENTATION['tasks'][task['suffix']]
        writer = p.D if 'methods' in task else p.A
        writer(task['suffix'], ','.join(task['printedParts']), task.get('methods', task.get('scale')),
               task['schemePages'], task['sourcePages'], view['topic'], view['atlas'],
               task['questionText'], stem=task.get('stem'), extra={k: task[k] for k in ('fullCreditMinusOne', 'markingNote', 'measurementRequired') if k in task})
        assert p.cards[-1]['totalMarks'] == task['totalMarks']
    p.check(SOURCE['printedQuestionMarks'], 49)
    assert sum(c['totalMarks'] for c in p.cards) == SOURCE['offeredMarks'] == 400
    return p


def figure_bindings():
    counts = defaultdict(int)
    result = {}
    shared = {}
    for task in SOURCE['tasks']:
        page = task['schemePages'][0]
        digest = PRESENTATION['tasks'][task['suffix']]['inspectedSolutionSha256']
        if digest not in shared:
            shared[digest] = f'maths-2011-FL-scheme-p{page:03}-i{counts[page]}'
        result[PREFIX + task['suffix']] = shared[digest]
        counts[page] += 1
    return result


def classify(text):
    if 'Attempt SIX QUESTIONS' in text:
        return 'whole-examination-selection', SOURCE['selectionReview'][0]['reason']
    raise ValueError('Unclassified selection directive: ' + text)


def write_review(p):
    p.review(SOURCE['printedQuestionMarks'],
        'Independent visual inspection of all eight original paper pages and scheme PDF pages 37–60, including every task, alternative method, graph, 50 marking components, attempt floor and special deduction. All 49 question and 49 complete solution crops visually inspected.',
        SOURCE['schemePagesInspected'], SOURCE['generalNotesPages'], SOURCE['notes'], SOURCE['selectionReview'], classify)


def main():
    if len(sys.argv) > 1:
        quotes(ROWS, sys.argv[1]); return
    assert PRESENTATION['status'] == 'visually inspected', 'Inspect every question and solution crop before publication'
    p = build_paper()
    write_review(p)
    p.apply(ROWS, '2011 Foundation Paper 2', expect_added=[c['id'] for c in p.cards],
            card_overrides={cid: {'figureKey': key, 'section': 'A'} for cid, key in figure_bindings().items()}, question_figures=True)


if __name__ == '__main__':
    main()
