"""2010 Higher legacy Paper 2: every core and optional task, with exact deductions."""
import hashlib
import json
import sys
from collections import defaultdict
from pathlib import Path
from review_lib import Paper, quotes

BASE = Path(__file__).resolve().parent
SOURCE = json.loads((BASE / '2010-hl-p2-source-review.json').read_text())
PRESENTATION = json.loads((BASE / '2010-hl-p2-presentation.json').read_text())
ROWS = {'maths-2010-hl-p2-q' + suffix: view['rows'] for suffix, view in PRESENTATION['tasks'].items()}
MARKS = {str(n): 50 for n in range(1, 12)}


def build_paper():
    p = Paper(2010, 'hl', 'p2', {}, SOURCE['paperFileid'], SOURCE['schemeFileid'],
              reviewed_at='2026-10-30', full_credit_minus_one=False)
    assert hashlib.sha256(p.P.read_bytes()).hexdigest() == SOURCE['paperSha256']
    assert hashlib.sha256(p.S.read_bytes()).hexdigest() == SOURCE['schemeSha256']
    for task in SOURCE['tasks']:
        view = PRESENTATION['tasks'][task['suffix']]
        extra = {'markingNote': task['markingNote']} if task.get('markingNote') else None
        p.D(task['suffix'], ','.join(task['printedParts']), task['methods'], task['schemePages'],
            task['sourcePages'], view['topic'], view['atlas'], task['questionText'], task.get('stem'), extra)
        assert p.cards[-1]['totalMarks'] == task['totalMarks']
    p.check(MARKS, 57)
    return p


def figure_bindings():
    counts = defaultdict(int)
    result = {}
    for task in SOURCE['tasks']:
        page = task['schemePages'][0]
        result['maths-2010-hl-p2-q' + task['suffix']] = f'maths-2010-HL-scheme-p{page:03}-i{counts[page]}'
        counts[page] += 1
    return result


def classify(text):
    for phrases, category, n in [
        (('Attempt FIVE questions', 'Answer FIVE questions', 'Answer one question'), 'whole-examination-selection', 0),
        (('one of the novels', 'one of the plays', 'one of the poems'), 'scenario-definition', 1),
        (('only one of which is correct',), 'scenario-definition', 2),
        (('unit circle, or otherwise',), 'alternative-proof-method', 3),
    ]:
        if any(phrase in text for phrase in phrases):
            return category, SOURCE['selectionReview'][n]
    raise ValueError('Unclassified selection directive: ' + text)


def write_review(p):
    p.review(MARKS,
        'Independent visual inspection of all eight original paper pages and scheme pages 39–82, including every optional question, published allocation, restricted award, original diagram and alternative method. All 57 question and 57 complete solution presentations inspected.',
        SOURCE['schemePagesInspected'], SOURCE['generalNotesPages'],
        SOURCE['selectionReview'] + SOURCE['markingRules'] + SOURCE['taskBoundaryReview'] +
        [v['sourceNote'] for v in PRESENTATION['tasks'].values() if v.get('sourceNote')], [
            {'pages': [1, 2, 6], 'wording': 'Attempt FIVE questions from Section A and ONE question from Section B.', 'classification': 'whole-examination-selection', 'reason': SOURCE['selectionReview'][0]},
            {'pages': [5], 'wording': 'one of the novels; one of the plays; one of the poems', 'classification': 'scenario-definition', 'reason': SOURCE['selectionReview'][1]},
            {'pages': [6], 'wording': 'four possible answers, only one of which is correct', 'classification': 'scenario-definition', 'reason': SOURCE['selectionReview'][2]},
            {'pages': [7], 'wording': 'to or from the unit circle, or otherwise', 'classification': 'alternative-proof-method', 'reason': SOURCE['selectionReview'][3]},
            {'pages': [7], 'wording': 'Give an isomorphism', 'classification': 'open-example-construction', 'reason': SOURCE['selectionReview'][4]},
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
    p.apply(ROWS, '2010 Higher Paper 2', expect_added=[c['id'] for c in p.cards],
            card_overrides=overrides, question_figures=True)


if __name__ == '__main__':
    main()
