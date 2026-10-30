"""2011 Foundation Phase 2 Paper 1: all 29 tasks and 30 scoring components."""
import hashlib
import json
import sys
from collections import defaultdict
from pathlib import Path
from review_lib import Paper, quotes

BASE = Path(__file__).resolve().parent
SOURCE = json.loads((BASE / '2011-fl-p1-project-source-review.json').read_text())
PRESENTATION = json.loads((BASE / '2011-fl-p1-project-presentation.json').read_text())
PREFIX = 'maths-2011-fl-p1-project-q'
ROWS = {PREFIX + suffix: task['rows'] for suffix, task in PRESENTATION['tasks'].items()}


def build_paper():
    p = Paper(2011, 'fl', 'p1', SOURCE['scales'], SOURCE['paperFileid'], SOURCE['schemeFileid'],
              reviewed_at='2026-10-30', edition='project', full_credit_minus_one=False)
    assert hashlib.sha256(p.P.read_bytes()).hexdigest() == SOURCE['paperSha256']
    assert hashlib.sha256(p.S.read_bytes()).hexdigest() == SOURCE['schemeSha256']
    for task in SOURCE['tasks']:
        view = PRESENTATION['tasks'][task['suffix']]
        writer = p.D if 'methods' in task else p.A
        writer(task['suffix'], ','.join(task['printedParts']), task.get('methods', task.get('scale')),
               task['schemePages'], task['sourcePages'], view['topic'], view['atlas'],
               task['questionText'], stem=task.get('stem'), extra={k: task[k] for k in ('fullCreditMinusOne', 'markingNote') if k in task})
        assert p.cards[-1]['totalMarks'] == task['totalMarks']
    p.check(SOURCE['printedQuestionMarks'], 29)
    assert sum(c['totalMarks'] for c in p.cards) == SOURCE['offeredMarks'] == 300
    return p


def figure_bindings():
    counts = defaultdict(int)
    result = {}
    shared = {}
    for task in SOURCE['tasks']:
        page = task['schemePages'][0]
        digest = PRESENTATION['tasks'][task['suffix']]['inspectedSolutionSha256']
        if digest not in shared:
            shared[digest] = f'maths-2011-FL-scheme-project-p{page:03}-i{counts[page]}'
        result[PREFIX + task['suffix']] = shared[digest]
        counts[page] += 1
    return result


def classify(text):
    if 'Answer all' in text or 'answer all' in text:
        return 'whole-examination-selection', SOURCE['selectionReview'][0]['reason']
    if 'Which one of these three formulae' in text:
        return 'required-answer-identification', SOURCE['selectionReview'][1]['reason']
    raise ValueError('Unclassified selection directive: ' + text)


def write_review(p):
    p.review(SOURCE['printedQuestionMarks'],
        'Independent visual inspection of all 16 original paper pages and scheme PDF pages 1–28, including every model solution, alternative method, diagram, scale, Section C deduction rule, component allocation and detailed credit note. All 29 question and 29 solution crops visually inspected.',
        SOURCE['schemePagesInspected'], SOURCE['generalNotesPages'], SOURCE['notes'], SOURCE['selectionReview'], classify)


def main():
    if len(sys.argv) > 1:
        quotes(ROWS, sys.argv[1]); return
    assert PRESENTATION['status'] == 'visually inspected', 'Inspect every question and solution crop before publication'
    p = build_paper()
    write_review(p)
    p.apply(ROWS, '2011 Foundation Project Maths Phase 2 Paper 1', expect_added=[c['id'] for c in p.cards],
            card_overrides={c['id']: {'figureKey': figure_bindings()[c['id']], 'section': 'A' if int(c['printedParts'][0][1:].split('(')[0]) <= 5 else 'B' if int(c['printedParts'][0][1:].split('(')[0]) <= 7 else 'C'} for c in p.cards}, question_figures=True)


if __name__ == '__main__':
    main()
