"""2012 Foundation Phase 1 P2: 38 tasks, all six finite triangle-pair routes."""
import copy
import itertools
import json
import sys
import fitz
from collections import defaultdict
from pathlib import Path
from review_lib import Paper, quotes

BASE = Path(__file__).resolve().parent
SOURCE = json.loads((BASE / '2012-fl-p2-source-review.json').read_text())
PRESENTATION = json.loads((BASE / '2012-fl-p2-presentation.json').read_text())
MARKS = {'1': 25, '2': 25, '3': 25, '4A': 25, '4B': 25, '5': 50, '6': 50, '7': 50, '8': 50}
TRIANGLES = ['OAB', 'OBC', 'OCD', 'ODA']
PAIRS = list(itertools.combinations(TRIANGLES, 2))


def base_suffix(suffix):
    return '4b-c' if suffix.startswith('4b-c-pair-') else suffix


def tasks():
    for task in SOURCE['tasks']:
        if task['suffix'] != '4b-c':
            yield task
            continue
        for index, pair in enumerate(PAIRS, 1):
            route = copy.deepcopy(task)
            route['suffix'] = f'4b-c-pair-{index:02}'
            edges = ' and '.join(triangle[1:] for triangle in pair)
            instruction = f'For this practice, name the two isosceles triangles whose outer sides are {edges}. The original question allows any two isosceles triangles in the diagram.'
            route['questionText'] += f' For this practice, use the triangles with outer sides {edges}.'
            route['selectionVariant'] = dict(groupId='q4b-c-triangle-pair', pool=TRIANGLES, choose=2,
                selected=list(pair), practiceInstruction=instruction, sourcePage=7,
                sourceDirective='Name two isosceles triangles in the diagram.')
            yield route


ROWS = {'maths-2012-fl-p2-q' + task['suffix']: PRESENTATION['tasks'][base_suffix(task['suffix'])]['rows'] for task in tasks()}


def build_paper():
    p = Paper(2012, 'fl', 'p2', SOURCE['scales'], SOURCE['paperFileid'], SOURCE['schemeFileid'],
              reviewed_at='2026-10-29', full_credit_minus_one=False)
    with fitz.open(p.P) as original:
        assert 'Name two isosceles triangles in the diagram.' in ' '.join(original[6].get_text().split())
    for task in tasks():
        view = PRESENTATION['tasks'][base_suffix(task['suffix'])]
        extra = {k: task[k] for k in ('fullCreditMinusOne', 'measurementRequired', 'selectionVariant', 'markingNote') if k in task}
        writer = p.C if 'components' in task else p.A
        writer(task['suffix'], ','.join(task['printedParts']), task.get('components', task.get('scale')),
               task['schemePages'], task['sourcePages'], view['topic'], view['atlas'],
               task['questionText'], stem=task.get('stem'), extra=extra)
    p.check({**MARKS, '4B': 50}, 43)
    assert sum(c['totalMarks'] for c in p.cards if not c.get('selectionVariant')) + 5 == SOURCE['offeredMarks']
    return p


def figure_bindings():
    counts = defaultdict(int); hashes = {}; result = {}
    for task in tasks():
        view = PRESENTATION['tasks'][base_suffix(task['suffix'])]
        digest = view['inspectedSolutionSha256']
        if digest not in hashes:
            page = task['schemePages'][0]
            hashes[digest] = f'maths-2012-FL-scheme-p{page:03}-i{counts[page]}'
            counts[page] += 1
        result['maths-2012-fl-p2-q' + task['suffix']] = hashes[digest]
    return result


def classify(text):
    if 'either Question 4' in text or 'either 4A' in text:
        return 'expanded-alternatives', SOURCE['selectionReview'][0]['reason']
    if 'Answer all' in text:
        return 'all-required', 'All tasks retained, including both complete geometry alternatives.'
    if 'at least one of the numbers' in text:
        return 'scenario-definition', 'The probability event is specified, not a selection of questions.'
    raise ValueError('Unclassified selection directive: ' + text)


def main():
    if len(sys.argv) > 1:
        quotes(ROWS, sys.argv[1]); return
    assert PRESENTATION['status'] == 'visually inspected', 'Inspect every question and solution crop before publication'
    p = build_paper()
    p.review(MARKS,
        'Independent visual inspection of all 16 original paper pages and scheme PDF pages 41–68, including every model, diagram, scale, component allocation and detailed credit note. All 38 distinct question and 38 distinct solution presentations inspected. Six mechanically expanded triangle pairs yield 43 cards.',
        SOURCE['schemePagesInspected'], SOURCE['generalNotesPages'], SOURCE['notes'], SOURCE['selectionReview'], classify)
    p.apply(ROWS, '2012 Foundation Project Maths Phase 1 Paper 2', expect_added=[c['id'] for c in p.cards],
            card_overrides={c['id']: {'figureKey': figure_bindings()[c['id']], 'section': 'A' if int(c['printedParts'][0][1]) <= 4 else 'B' if int(c['printedParts'][0][1]) <= 6 else 'C'} for c in p.cards}, question_figures=True)


if __name__ == '__main__':
    main()
