"""2010 Ordinary legacy Paper 2: all 74 tasks under the original deduction rules."""
import hashlib
import json
import sys
from collections import defaultdict
from pathlib import Path
from review_lib import Paper, quotes

BASE = Path(__file__).resolve().parent
SOURCE = json.loads((BASE / '2010-ol-p2-source-review.json').read_text())
PRESENTATION = json.loads((BASE / '2010-ol-p2-presentation.json').read_text())
ROWS = {'maths-2010-ol-p2-q' + suffix: view['rows'] for suffix, view in PRESENTATION['tasks'].items()}
MARKS = {str(n): 50 for n in range(1, 12)}


def build_paper():
    p = Paper(2010, 'ol', 'p2', {}, SOURCE['paperFileid'], SOURCE['schemeFileid'],
              reviewed_at='2026-10-30', full_credit_minus_one=False)
    assert hashlib.sha256(p.P.read_bytes()).hexdigest() == SOURCE['paperSha256']
    assert hashlib.sha256(p.S.read_bytes()).hexdigest() == SOURCE['schemeSha256']
    for task in SOURCE['tasks']:
        view = PRESENTATION['tasks'][task['suffix']]
        extra = {k: task[k] for k in ('markingNote', 'measurementRequired') if k in task}
        p.D(task['suffix'], ','.join(task['printedParts']), task['methods'], task['schemePages'],
            task['sourcePages'], view['topic'], view['atlas'], task['questionText'], task.get('stem'), extra)
        assert p.cards[-1]['totalMarks'] == task['totalMarks']
    p.check(MARKS, 74)
    return p


def figure_bindings():
    counts = defaultdict(int)
    result = {}
    inspected = {}
    for task in SOURCE['tasks']:
        page = task['schemePages'][0]
        digest = PRESENTATION['tasks'][task['suffix']]['inspectedSolutionSha256']
        key = inspected.setdefault(digest, f'maths-2010-OL-scheme-p{page:03}-i{counts[page]}')
        result['maths-2010-ol-p2-q' + task['suffix']] = key
        counts[page] += 1
    return result


def classify(text):
    if any(s in text for s in ('Attempt FIVE questions', 'Attempt ONE question')):
        return 'whole-examination-selection', SOURCE['selectionReview'][0]['reason']
    if 'any other transversal' in text:
        return 'universal-proof-statement', SOURCE['selectionReview'][1]['reason']
    if 'one particular person' in text or 'selected from ten people' in text:
        return 'counting-scenario', SOURCE['selectionReview'][2]['reason']
    raise ValueError('Unclassified selection directive: ' + text)


def write_review(p):
    p.review(MARKS,
        'Independent visual inspection of all twelve original paper pages (including two blank pages) and scheme PDF pages 42–96, including every optional question, allocation, attempt floor, original diagram, full solution and alternative method. Card crops are certified separately in the presentation ledger.',
        SOURCE['schemePagesInspected'], SOURCE['generalNotesPages'], SOURCE['notes'], SOURCE['selectionReview'], classify)


def main():
    if len(sys.argv) > 1:
        quotes(ROWS, sys.argv[1])
        return
    assert PRESENTATION['status'] == 'visually inspected', 'Inspect every crop before publication'
    p = build_paper()
    write_review(p)
    overrides = {cid: {'section': 'A' if int(cid.split('-q')[1].split('-')[0]) <= 7 else 'B', 'figureKey': key} for cid, key in figure_bindings().items()}
    p.apply(ROWS, '2010 Ordinary Paper 2', expect_added=[c['id'] for c in p.cards],
            card_overrides=overrides, question_figures=True)


if __name__ == '__main__':
    main()
