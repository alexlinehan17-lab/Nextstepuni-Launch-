"""2012 Higher Phase 3 P1: all 32 tasks, including five altitude routes."""
import copy
import itertools
import json
import sys
import fitz
from collections import defaultdict
from pathlib import Path
from review_lib import Paper, quotes

BASE = Path(__file__).resolve().parent
SOURCE = json.loads((BASE / '2012-hl-p1-project-source-review.json').read_text())
PRESENTATION = json.loads((BASE / '2012-hl-p1-project-presentation.json').read_text())
MARKS = {str(i): 25 if i <= 6 else 50 for i in range(1, 10)}
ALTITUDES = ['1', '2', '3', '4', '5']
DIRECTIVE = 'Taking any one value other than 0 for the altitude'


def base_suffix(suffix):
    return '9-b-i' if suffix.startswith('9-b-i-altitude-') else suffix


def tasks():
    for task in SOURCE['tasks']:
        if task['suffix'] != '9-b-i':
            yield task
            continue
        for (altitude,) in itertools.combinations(ALTITUDES, 1):
            route = copy.deepcopy(task)
            route['suffix'] = f'9-b-i-altitude-{altitude}'
            instruction = f'For this practice, use altitude {altitude} km. The original question allows any nonzero altitude from the supplied table.'
            route['questionText'] += f' For this practice, use altitude {altitude} km.'
            route['selectionVariant'] = dict(groupId='q9-b-i-altitude', pool=ALTITUDES, choose=1,
                selected=[altitude], practiceInstruction=instruction, sourcePage=16, sourceDirective=DIRECTIVE)
            yield route


ROWS = {'maths-2012-hl-p1-project-q' + t['suffix']: PRESENTATION['tasks'][base_suffix(t['suffix'])]['rows'] for t in tasks()}


def build_paper():
    p = Paper(2012, 'hl', 'p1', SOURCE['scales'], SOURCE['paperFileid'], SOURCE['schemeFileid'],
              reviewed_at='2026-10-30', edition='project', full_credit_minus_one=False)
    with fitz.open(p.P) as original:
        assert DIRECTIVE in ' '.join(original[15].get_text().split())
    for task in tasks():
        view = PRESENTATION['tasks'][base_suffix(task['suffix'])]
        extra = {k: task[k] for k in ('fullCreditMinusOne', 'selectionVariant') if k in task}
        writer = p.C if 'components' in task else p.A
        writer(task['suffix'], ','.join(task['printedParts']), task.get('components', task.get('scale')),
               task['schemePages'], task['sourcePages'], view['topic'], view['atlas'],
               task['questionText'], stem=task.get('stem'), extra=extra)
    p.check({**MARKS, '9': 70}, 36)
    assert sum(c['totalMarks'] for c in p.cards if not c.get('selectionVariant')) + 5 == SOURCE['offeredMarks']
    return p


def figure_bindings():
    counts = defaultdict(int); hashes = {}; result = {}
    for task in tasks():
        view = PRESENTATION['tasks'][base_suffix(task['suffix'])]
        digest = view['inspectedSolutionSha256']
        if digest not in hashes:
            page = task['schemePages'][0]
            hashes[digest] = f'maths-2012-HL-scheme-project-p{page:03}-i{counts[page]}'
            counts[page] += 1
        result['maths-2012-hl-p1-project-q' + task['suffix']] = hashes[digest]
    return result


def classify(text):
    if 'Answer all' in text:
        return 'all-required', 'Every task is retained.'
    if 'One of these is shaded' in text:
        return 'given-diagram-state', 'Both remaining empty regions are required.'
    if 'One of these values is an integer' in text:
        return 'given-property', 'Both positive heights are required.'
    if 'one of the three cups' in text:
        return 'single-best-answer', 'The task evaluates the most reasonable cup; all three options remain in the card.'
    if 'Taking any one value other than 0' in text:
        return 'expanded-alternatives', 'All five nonzero altitudes in the supplied table are mechanically expanded at 5B each.'
    raise ValueError('Unclassified selection directive: ' + text)


def write_review(p):
    p.review(MARKS,
        'Independent visual reading of all 20 original paper pages and scheme PDF pages 1–36, including all model solutions, allocation tables and detailed credit notes. All 32 distinct question and solution presentations visually inspected. The five nonzero table altitudes yield 36 practice cards.',
        SOURCE['schemePagesInspected'], SOURCE['generalNotesPages'], SOURCE['notes'], SOURCE['selectionReview'], classify)


def main():
    if len(sys.argv) > 1:
        quotes(ROWS, sys.argv[1]); return
    assert PRESENTATION['status'] == 'visually inspected', 'Inspect every question and solution crop before publication'
    p = build_paper()
    write_review(p)
    p.apply(ROWS, '2012 Higher Project Maths Phase 3 Paper 1', expect_added=[c['id'] for c in p.cards],
            card_overrides={c['id']: {'figureKey': figure_bindings()[c['id']]} for c in p.cards}, question_figures=True)


if __name__ == '__main__':
    main()
