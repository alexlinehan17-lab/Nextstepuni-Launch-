"""2011 Higher legacy Paper 2: all 60 tasks, including all Section B options."""
import hashlib
import json
import sys
from collections import defaultdict
from pathlib import Path
from review_lib import Paper, quotes

BASE = Path(__file__).resolve().parent
SOURCE = json.loads((BASE / '2011-hl-p2-source-review.json').read_text())
PRESENTATION = json.loads((BASE / '2011-hl-p2-presentation.json').read_text())
ROWS = {'maths-2011-hl-p2-q' + suffix: view['rows'] for suffix, view in PRESENTATION['tasks'].items()}
MARKS = {str(n): 50 for n in range(1, 12)}


def build_paper():
    p = Paper(2011, 'hl', 'p2', {}, SOURCE['paperFileid'], SOURCE['schemeFileid'],
              reviewed_at='2026-10-30', full_credit_minus_one=False)
    assert hashlib.sha256(p.P.read_bytes()).hexdigest() == SOURCE['paperSha256']
    assert hashlib.sha256(p.S.read_bytes()).hexdigest() == SOURCE['schemeSha256']
    for task in SOURCE['tasks']:
        view = PRESENTATION['tasks'][task['suffix']]
        extra = {'markingNote': task['markingNote']} if task.get('markingNote') else None
        p.D(task['suffix'], ','.join(task['printedParts']), task['methods'], task['schemePages'],
            task['sourcePages'], view['topic'], view['atlas'], task['questionText'], task.get('stem'), extra)
        assert p.cards[-1]['totalMarks'] == task['totalMarks']
    p.check(MARKS, 60)
    return p


def figure_bindings():
    counts = defaultdict(int)
    result = {}
    for task in SOURCE['tasks']:
        page = task['schemePages'][0]
        result['maths-2011-hl-p2-q' + task['suffix']] = f'maths-2011-HL-scheme-p{page:03}-i{counts[page]}'
        counts[page] += 1
    return result


def classify(text):
    if any(phrase in text for phrase in ('Attempt FIVE questions', 'Answer FIVE questions', 'Answer one question')):
        return 'whole-examination-selection', SOURCE['selectionReview'][0]
    if 'one of the paths' in text.lower():
        return 'scenario-definition', SOURCE['selectionReview'][1]
    raise ValueError('Unclassified selection directive: ' + text)


def write_review(p):
    p.review(MARKS,
        'Independent visual inspection of all eight original paper pages and scheme pages 33–76, including every optional question, published allocation, attempt floor, original diagram and alternative method. All 60 question and 60 complete solution presentations inspected.',
        SOURCE['schemePagesInspected'], SOURCE['generalNotesPages'],
        SOURCE['selectionReview'] + SOURCE['markingRules'] + SOURCE['taskBoundaryReview'] + [
            'Q3(a) retains the explicit exception to the usual best-of-attempts rule.',
            'Q5(c)(ii), Q8(b)(ii) and Q8(c)(ii) retain their task-specific restrictions from earlier work.',
            'Q8(a) omitting the integration constant is a one-mark slip, as this paper specifies.',
            'Q9(c)(i), Q10(b)(v) and Q11(b)(ii) retain original printing errors with explanatory source notes; no invented marks or criteria.',
        ], [
            {'pages': [1, 2, 6], 'wording': 'Attempt FIVE questions from Section A and ONE question from Section B.', 'classification': 'whole-examination-selection', 'reason': SOURCE['selectionReview'][0]},
            {'pages': [5], 'wording': 'must follow one of the paths; List the other two possible paths', 'classification': 'scenario-definition', 'reason': SOURCE['selectionReview'][1]},
            {'pages': [7], 'wording': 'one element x of order 3; one element y of order 2', 'classification': 'open-example-choice', 'reason': SOURCE['selectionReview'][2]},
        ], classify)


def main():
    if len(sys.argv) > 1:
        quotes(ROWS, sys.argv[1])
        return
    assert PRESENTATION['status'] == 'visually inspected', 'Inspect every crop before publication'
    p = build_paper()
    write_review(p)
    overrides = {cid: {'section': 'A' if int(cid.split('-q')[1].split('-')[0]) <= 7 else 'B', 'figureKey': key}
                 for cid, key in figure_bindings().items()}
    p.apply(ROWS, '2011 Higher Paper 2', expect_added=[c['id'] for c in p.cards],
            card_overrides=overrides, question_figures=True)


if __name__ == '__main__':
    main()
