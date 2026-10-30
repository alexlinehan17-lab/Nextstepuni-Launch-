"""2010 Ordinary Paper 2: all 44 tasks and 47 scoring components."""
import hashlib
import json
import sys
from collections import defaultdict
from pathlib import Path
from review_lib import Paper, quotes

BASE = Path(__file__).resolve().parent
SOURCE = json.loads((BASE / '2010-ol-p2-project-source-review.json').read_text())
PRESENTATION = json.loads((BASE / '2010-ol-p2-project-presentation.json').read_text())
PREFIX = 'maths-2010-ol-p2-project-q'
ROWS = {PREFIX + suffix: task['rows'] for suffix, task in PRESENTATION['tasks'].items()}


def build_paper():
    p = Paper(2010, 'ol', 'p2', SOURCE['scales'], SOURCE['paperFileid'], SOURCE['schemeFileid'],
              reviewed_at='2026-10-30', edition='project', full_credit_minus_one=False)
    assert hashlib.sha256(p.P.read_bytes()).hexdigest() == SOURCE['paperSha256']
    assert hashlib.sha256(p.S.read_bytes()).hexdigest() == SOURCE['schemeSha256']
    for task in SOURCE['tasks']:
        view = PRESENTATION['tasks'][task['suffix']]
        writer = p.D if 'methods' in task else p.C if 'components' in task else p.A
        writer(task['suffix'], ','.join(task['printedParts']), task.get('methods', task.get('components', task.get('scale'))),
               task['schemePages'], task['sourcePages'], view['topic'], view['atlas'],
               task['questionText'], stem=task.get('stem'), extra={k: task[k] for k in ('fullCreditMinusOne', 'measurementRequired', 'markingNote', 'generalNotesPages') if k in task})
        assert p.cards[-1]['totalMarks'] == task['totalMarks']
    p.check(SOURCE['printedQuestionMarks'], 44)
    assert sum(c['totalMarks'] for c in p.cards) == SOURCE['offeredMarks'] == 345
    return p


def figure_bindings():
    return {PREFIX + suffix: view['figureKey'] for suffix, view in PRESENTATION['tasks'].items()}


def classify(text):
    if 'either' in text or 'Answer all' in text:
        return 'whole-examination-selection', SOURCE['selectionReview'][0]['reason']
    if 'or otherwise' in text:
        return 'open-method-choice', SOURCE['selectionReview'][1]['reason']
    if 'one particular song' in text or 'selections' in text:
        return 'counting-scenario', SOURCE['selectionReview'][2]['reason']
    if 'Tick the correct' in text:
        return 'single-correct-response', SOURCE['selectionReview'][3]['reason']
    raise ValueError('Unclassified selection directive: ' + text)


def write_review(p):
    p.review(SOURCE['printedQuestionMarks'],
        'Independent visual inspection of all 20 original paper pages and scheme PDF pages 3–4 and 45–78, including every model solution, alternative proof, diagram, scale, component allocation and detailed credit note. All 44 question and 44 solution crops visually inspected.',
        SOURCE['schemePagesInspected'], SOURCE['generalNotesPages'], SOURCE['notes'], SOURCE['selectionReview'], classify)


def main():
    if len(sys.argv) > 1:
        quotes(ROWS, sys.argv[1]); return
    assert PRESENTATION['status'] == 'visually inspected', 'Inspect every question and solution crop before publication'
    p = build_paper()
    write_review(p)
    p.apply(ROWS, '2010 Ordinary Project Maths Paper 2', expect_added=[c['id'] for c in p.cards],
            card_overrides={cid: {'section': 'A' if int(cid.split('-q')[1].split('-')[0].rstrip('ab')) <= 6 else 'B', 'figureKey': key} for cid, key in figure_bindings().items()}, question_figures=True)


if __name__ == '__main__':
    main()
