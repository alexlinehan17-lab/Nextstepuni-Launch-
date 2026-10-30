"""2011 Higher Paper 1: all 41 printed tasks, including every required component."""
import hashlib
import json
import sys
from collections import defaultdict
from pathlib import Path
from review_lib import Paper, quotes

BASE = Path(__file__).resolve().parent
SOURCE = json.loads((BASE / '2011-hl-p1-source-review.json').read_text())
PRESENTATION = json.loads((BASE / '2011-hl-p1-presentation.json').read_text())
ROWS = {'maths-2011-hl-p1-q' + suffix: view['rows'] for suffix, view in PRESENTATION['tasks'].items()}


def build_paper():
    p = Paper(2011, 'hl', 'p1', {}, SOURCE['paperFileid'], SOURCE['schemeFileid'],
              reviewed_at='2026-10-30', full_credit_minus_one=False)
    assert hashlib.sha256(p.P.read_bytes()).hexdigest() == SOURCE['paperSha256']
    assert hashlib.sha256(p.S.read_bytes()).hexdigest() == SOURCE['schemeSha256']
    for task in SOURCE['tasks']:
        view = PRESENTATION['tasks'][task['suffix']]
        extra = {'markingNote': task['markingNote']} if task.get('markingNote') else None
        p.D(task['suffix'], ','.join(task['printedParts']), task['methods'], task['schemePages'],
            task['sourcePages'], view['topic'], view['atlas'], task['questionText'], task.get('stem'), extra)
        assert p.cards[-1]['totalMarks'] == task['totalMarks']
    p.check({str(n): 50 for n in range(1, 9)}, 41)
    return p


def figure_bindings():
    counts = defaultdict(int)
    result = {}
    for task in SOURCE['tasks']:
        page = task['schemePages'][0]
        result['maths-2011-hl-p1-q' + task['suffix']] = f'maths-2011-HL-scheme-p{page:03}-i{counts[page]}'
        counts[page] += 1
    return result


def classify(text):
    for phrase, kind, index in [
        ('Attempt SIX QUESTIONS', 'whole-examination-selection', 0),
        ('One of the three diagrams', 'answer-identification', 1),
        ('one of the roots is four times the other', 'given-condition', 2),
        ('Hence, or otherwise', 'alternative-method', 3),
    ]:
        if phrase in text:
            return kind, SOURCE['selectionReview'][index]
    raise ValueError('Unclassified selection directive: ' + text)


def write_review(p):
    p.review({str(n): 50 for n in range(1, 9)},
        'Independent visual inspection of all eight original paper pages and scheme pages 1–32, including all printed tasks, allocation steps, attempt floors and alternative methods. All 41 question and 41 complete solution presentations inspected.',
        list(range(1, 33)), [4], SOURCE['selectionReview'] + SOURCE['markingRules'] + SOURCE['taskBoundaryReview'] + [
            'Q6(c)(ii) is 5 marks, attempt 2 in both the summary and detailed allocation. A later note refers to “2nd 5 marks”; this discrepancy is explained without creating extra marks.',
            'Historical matrices are retained in algebra; original matrix notation, proofs, integrals, graphs and alternative solutions remain visible.',
            'Shared marking-note blocks are labelled; only deductions relevant to the named task apply.'
        ], [
            {'pages': [1], 'wording': 'Attempt SIX QUESTIONS (50 marks each).', 'classification': 'whole-examination-selection', 'reason': SOURCE['selectionReview'][0]},
            {'pages': [5], 'wording': 'One of the three diagrams A, B, or C', 'classification': 'answer-identification', 'reason': SOURCE['selectionReview'][1]},
            {'pages': [2], 'wording': 'If one of the roots is four times the other', 'classification': 'given-condition', 'reason': SOURCE['selectionReview'][2]},
            {'pages': [3], 'wording': 'Hence, or otherwise', 'classification': 'alternative-method', 'reason': SOURCE['selectionReview'][3]},
        ], classify)


def main():
    if len(sys.argv) > 1:
        quotes(ROWS, sys.argv[1])
        return
    assert PRESENTATION['status'] == 'visually inspected', 'Inspect every crop before publication'
    p = build_paper()
    write_review(p)
    overrides = {cid: {'section': 'A', 'figureKey': key} for cid, key in figure_bindings().items()}
    p.apply(ROWS, '2011 Higher Paper 1', expect_added=[c['id'] for c in p.cards],
            card_overrides=overrides, question_figures=True)


if __name__ == '__main__':
    main()
