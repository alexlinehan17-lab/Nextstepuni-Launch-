"""2011 HL Phase 2 P1: 36 marking units, 74 complete practice routes."""
import copy
import hashlib
import itertools
import json
import math
import sys
from collections import defaultdict
from pathlib import Path
from review_lib import Paper, quotes

BASE = Path(__file__).resolve().parent
SOURCE = json.loads((BASE / '2011-hl-p1-project-source-review.json').read_text())
PRESENTATION = json.loads((BASE / '2011-hl-p1-project-presentation.json').read_text())
POOL = ['0', '1', '2', '3', '4']
VALUES = [2.920, 2.642, 2.391, 2.163, 1.957]
PAIRS = list(itertools.combinations(POOL, 2))
CHECKS = [(a, b, k) for a, b in PAIRS for k in POOL if k not in (a, b)]
A_DIRECTIVE = 'Use any two of the observations from the table'
B_DIRECTIVE = 'Use a different observation from the table to verify your values for A and b.'
PREFIX = 'maths-2011-hl-p1-project-q'


def base_suffix(suffix):
    return '4-a' if suffix.startswith('4-a-times-') else '4-b' if suffix.startswith('4-b-times-') else suffix


def fit_pair(a, b):
    i, j = int(a), int(b)
    rate = math.log(VALUES[i] / VALUES[j]) / (j - i)
    return VALUES[i] * math.exp(rate * i), rate


def tasks():
    for task in SOURCE['tasks']:
        if task['suffix'] not in ('4-a', '4-b'):
            yield task
            continue
        is_a = task['suffix'] == '4-a'
        routes = PAIRS if is_a else CHECKS
        for route in routes:
            a, b = route[:2]
            item = copy.deepcopy(task)
            item['suffix'] += f'-times-{a}-{b}' + ('' if is_a else '-check-' + route[2])
            if is_a:
                instruction = f'For this practice, use the observations at t = {a} and t = {b} seconds to find A and b to three decimal places.'
                pool, choose, selected = POOL, 2, [a, b]
            else:
                A, rate = fit_pair(a, b)
                instruction = f'For this practice, part (a) used t = {a} and t = {b} seconds and gave A = {A:.3f}, b = {rate:.3f}. Verify using the unused observation at t = {route[2]} seconds. The printed observations are rounded, so report any small rounding difference honestly.'
                pool = [f'{i}-{j}-check-{k}' for i, j, k in CHECKS]
                choose, selected = 1, [f'{a}-{b}-check-{route[2]}']
            item['questionText'] += ' ' + instruction
            item['selectionVariant'] = dict(groupId='q' + task['suffix'] + '-observations', pool=pool,
                choose=choose, selected=selected, practiceInstruction=instruction, sourcePage=6,
                sourceDirective=A_DIRECTIVE if is_a else B_DIRECTIVE)
            yield item


ROWS = {PREFIX + task['suffix']: PRESENTATION['tasks'][base_suffix(task['suffix'])]['rows'] for task in tasks()}


def build_paper():
    p = Paper(2011, 'hl', 'p1', SOURCE['scales'], SOURCE['paperFileid'], SOURCE['schemeFileid'],
              reviewed_at='2026-10-30', edition='project', full_credit_minus_one=False)
    assert hashlib.sha256(p.P.read_bytes()).hexdigest() == SOURCE['paperSha256']
    assert hashlib.sha256(p.S.read_bytes()).hexdigest() == SOURCE['schemeSha256']
    for task in tasks():
        view = PRESENTATION['tasks'][base_suffix(task['suffix'])]
        extra = {k: task[k] for k in ('selectionVariant', 'markingNote') if k in task}
        writer = p.D if 'methods' in task else p.A
        writer(task['suffix'], ','.join(task['printedParts']), task.get('methods', task.get('scale')),
               task['schemePages'], task['sourcePages'], view['topic'], view['atlas'],
               task['questionText'], stem=task.get('stem'), extra=extra)
        assert p.cards[-1]['totalMarks'] == task['totalMarks']
    p.check({**SOURCE['printedQuestionMarks'], '4': 305}, 74)
    assert sum(t['totalMarks'] for t in SOURCE['tasks']) == SOURCE['offeredMarks'] == 350
    return p


def figure_bindings():
    counts = defaultdict(int)
    result = {}
    for task in tasks():
        page = task['schemePages'][0]
        result[PREFIX + task['suffix']] = f'maths-2011-HL-scheme-project-p{page:03}-i{counts[page]}'
        counts[page] += 1
    return result


def classify(text):
    if 'Answer all' in text or 'answer all' in text or 'any two of the three questions' in text:
        return 'whole-examination-selection', SOURCE['selectionReview'][0]['reason']
    if 'One of them lies' in text:
        return 'given-diagram-state', SOURCE['selectionReview'][1]['reason']
    if 'or otherwise' in text:
        return 'alternative-method', SOURCE['selectionReview'][2]['reason']
    if A_DIRECTIVE in text:
        return 'expanded-alternatives', SOURCE['selectionReview'][3]['reason']
    if 'choose between two' in text or 'chooses the cash' in text:
        return 'contextual-choice', SOURCE['selectionReview'][4]['reason']
    if 'One of the three diagrams' in text:
        return 'answer-identification', SOURCE['selectionReview'][5]['reason']
    raise ValueError('Unclassified selection directive: ' + text)


def write_review(p):
    p.review(SOURCE['printedQuestionMarks'],
        'Independent visual inspection of all 20 original paper pages and scheme pages 1–42, including every model solution, allocation, detailed credit note and Section C deduction rule. All 36 base question/solution presentations and all 40 observation-route supplements visually inspected. All ten fitting pairs and thirty dependent verification routes retained.',
        SOURCE['schemePagesInspected'], SOURCE['generalNotesPages'], SOURCE['notes'], SOURCE['selectionReview'], classify)


def main():
    if len(sys.argv) > 1:
        quotes(ROWS, sys.argv[1]); return
    assert PRESENTATION['status'] == 'visually inspected', 'Inspect every crop before publication'
    p = build_paper(); write_review(p)
    overrides = {c['id']: {'section': 'A' if int(c['printedParts'][0][1:].split('(')[0]) <= 4 else 'B' if int(c['printedParts'][0][1:].split('(')[0]) <= 6 else 'C', 'figureKey': figure_bindings()[c['id']]} for c in p.cards}
    p.apply(ROWS, '2011 Higher Project Maths Phase 2 Paper 1', expect_added=[c['id'] for c in p.cards],
            card_overrides=overrides, question_figures=True)


if __name__ == '__main__':
    main()
