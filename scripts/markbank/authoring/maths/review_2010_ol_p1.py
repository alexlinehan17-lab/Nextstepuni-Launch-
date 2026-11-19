"""2010 Ordinary legacy Paper 1: all 40 tasks under the original deduction rules."""
import hashlib
import json
import sys
from collections import defaultdict
from pathlib import Path
from review_lib import Paper, quotes

BASE = Path(__file__).resolve().parent
SOURCE = json.loads((BASE / '2010-ol-p1-source-review.json').read_text())
PRESENTATION = json.loads((BASE / '2010-ol-p1-presentation.json').read_text())
ROWS = {'maths-2010-ol-p1-q' + suffix: view['rows'] for suffix, view in PRESENTATION['tasks'].items()}
MARKS = {str(n): 50 for n in range(1, 9)}


def build_paper():
    p = Paper(2010, 'ol', 'p1', {}, SOURCE['paperFileid'], SOURCE['schemeFileid'],
              reviewed_at='2026-10-30', full_credit_minus_one=False)
    assert hashlib.sha256(p.P.read_bytes()).hexdigest() == SOURCE['paperSha256']
    assert hashlib.sha256(p.S.read_bytes()).hexdigest() == SOURCE['schemeSha256']
    for task in SOURCE['tasks']:
        view = PRESENTATION['tasks'][task['suffix']]
        extra = {'markingNote': task['markingNote']} if task.get('markingNote') else None
        p.D(task['suffix'], ','.join(task['printedParts']), task['methods'], task['schemePages'],
            task['sourcePages'], view['topic'], view['atlas'], task['questionText'], task.get('stem'), extra)
        assert p.cards[-1]['totalMarks'] == task['totalMarks']
    p.check(MARKS, 40)
    return p


def figure_bindings():
    counts = defaultdict(int)
    result = {}
    for task in SOURCE['tasks']:
        page = task['schemePages'][0]
        result['maths-2010-ol-p1-q' + task['suffix']] = f'maths-2010-OL-scheme-p{page:03}-i{counts[page]}'
        counts[page] += 1
    return result


def classify(text):
    if 'Attempt SIX QUESTIONS' in text:
        return 'whole-examination-selection', SOURCE['selectionReview'][0]['reason']
    if 'Hence, or otherwise' in text:
        return 'open-method-choice', SOURCE['selectionReview'][1]['reason']
    raise ValueError('Unclassified selection directive: ' + text)


def write_review(p):
    p.review(MARKS,
        'Independent visual inspection of all eight original paper pages and scheme PDF pages 1–43, including every task, original typeset working, graph, allocation, attempt floor and alternative method. Card crops are certified separately in the presentation ledger.',
        SOURCE['schemePagesInspected'], SOURCE['generalNotesPages'], SOURCE['notes'], SOURCE['selectionReview'], classify)


def main():
    if len(sys.argv) > 1:
        quotes(ROWS, sys.argv[1])
        return
    assert PRESENTATION['status'] == 'visually inspected', 'Inspect every crop before publication'
    p = build_paper()
    write_review(p)
    overrides = {cid: {'section': 'A', 'figureKey': key} for cid, key in figure_bindings().items()}
    p.apply(ROWS, '2010 Ordinary Paper 1', expect_added=[c['id'] for c in p.cards],
            card_overrides=overrides, question_figures=True)


if __name__ == '__main__':
    main()
