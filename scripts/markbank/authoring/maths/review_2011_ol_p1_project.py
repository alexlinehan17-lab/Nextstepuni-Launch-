"""2011 Ordinary Phase 2 Paper 1: all 43 tasks and 44 scoring components."""
import hashlib
import json
import sys
from collections import defaultdict
from pathlib import Path
from review_lib import Paper, quotes

BASE = Path(__file__).resolve().parent
SOURCE = json.loads((BASE / '2011-ol-p1-project-source-review.json').read_text())
PRESENTATION = json.loads((BASE / '2011-ol-p1-project-presentation.json').read_text())
PREFIX = 'maths-2011-ol-p1-project-q'
ROWS = {PREFIX + suffix: task['rows'] for suffix, task in PRESENTATION['tasks'].items()}


def build_paper():
    p = Paper(2011, 'ol', 'p1', SOURCE['scales'], SOURCE['paperFileid'], SOURCE['schemeFileid'],
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
    p.check(SOURCE['printedQuestionMarks'], 43)
    assert sum(c['totalMarks'] for c in p.cards) == SOURCE['offeredMarks'] == 350
    return p


def figure_bindings():
    counts = defaultdict(int)
    result = {}
    for task in SOURCE['tasks']:
        page = task['schemePages'][0]
        result[PREFIX + task['suffix']] = f'maths-2011-OL-scheme-project-p{page:03}-i{counts[page]}'
        counts[page] += 1
    return result


def classify(text):
    if 'Answer all' in text or 'answer all' in text or 'any two of the three questions' in text:
        return 'whole-examination-selection', SOURCE['selectionReview'][0]['reason']
    if 'or otherwise' in text:
        return 'open-method-choice', SOURCE['selectionReview'][1]['reason']
    raise ValueError('Unclassified selection directive: ' + text)


def write_review(p):
    p.review(SOURCE['printedQuestionMarks'],
        'Independent visual inspection of all 20 original paper pages and scheme PDF pages 1–42, including every model solution, alternative method, diagram, scale, Section C deduction rule, component allocation and detailed credit note. All 43 question and 43 solution crops visually inspected.',
        SOURCE['schemePagesInspected'], SOURCE['generalNotesPages'], SOURCE['notes'], SOURCE['selectionReview'], classify)


def main():
    if len(sys.argv) > 1:
        quotes(ROWS, sys.argv[1]); return
    assert PRESENTATION['status'] == 'visually inspected', 'Inspect every question and solution crop before publication'
    p = build_paper()
    write_review(p)
    p.apply(ROWS, '2011 Ordinary Project Maths Phase 2 Paper 1', expect_added=[c['id'] for c in p.cards],
            card_overrides={c['id']: {'figureKey': figure_bindings()[c['id']], 'section': 'A' if int(c['printedParts'][0][1:].split('(')[0]) <= 4 else 'B' if int(c['printedParts'][0][1:].split('(')[0]) <= 6 else 'C'} for c in p.cards}, question_figures=True)


if __name__ == '__main__':
    main()
