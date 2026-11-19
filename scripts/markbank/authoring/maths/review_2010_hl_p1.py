"""2010 Higher Paper 1: 40 mark units, all 43 finite practice routes."""
import copy
import hashlib
import json
import sys
from collections import defaultdict
from pathlib import Path
from review_lib import Paper, quotes

BASE = Path(__file__).resolve().parent
SOURCE = json.loads((BASE / '2010-hl-p1-source-review.json').read_text())
PRESENTATION = json.loads((BASE / '2010-hl-p1-presentation.json').read_text())
PREFIX = 'maths-2010-hl-p1-q'
ROOTS = ['1', '2', '3', '4']
DIRECTIVE = 'Choose one of the roots w, where .1 ≠ w'


def base_suffix(suffix):
    return '3-c-ii' if suffix.startswith('3-c-ii-root-') else suffix


def tasks():
    for task in SOURCE['tasks']:
        if task['suffix'] != '3-c-ii':
            yield task
            continue
        for root in ROOTS:
            item = copy.deepcopy(task)
            item['suffix'] += '-root-' + root
            angle = str(2 * int(root)) + 'π/5'
            instruction = f'For this practice, use w = cos({angle}) + i sin({angle}). Show explicitly that the imaginary part of w² + w³ is zero.'
            item['questionText'] += ' ' + instruction
            item['selectionVariant'] = dict(groupId='q3-c-ii-fifth-roots', pool=ROOTS, choose=1,
                selected=[root], practiceInstruction=instruction, sourcePage=3, sourceDirective=DIRECTIVE)
            yield item


ROWS = {PREFIX + t['suffix']: PRESENTATION['tasks'][base_suffix(t['suffix'])]['rows'] for t in tasks()}


def build_paper():
    p = Paper(2010, 'hl', 'p1', {}, SOURCE['paperFileid'], SOURCE['schemeFileid'],
              reviewed_at='2026-10-30', full_credit_minus_one=False)
    assert hashlib.sha256(p.P.read_bytes()).hexdigest() == SOURCE['paperSha256']
    assert hashlib.sha256(p.S.read_bytes()).hexdigest() == SOURCE['schemeSha256']
    for t in tasks():
        view = PRESENTATION['tasks'][base_suffix(t['suffix'])]
        extra = {k: t[k] for k in ('selectionVariant', 'markingNote') if k in t}
        p.D(t['suffix'], ','.join(t['printedParts']), t['methods'], t['schemePages'], t['sourcePages'],
            view['topic'], view['atlas'], t['questionText'], t.get('stem'), extra)
        assert p.cards[-1]['totalMarks'] == t['totalMarks']
    p.check({**SOURCE['printedQuestionMarks'], '3': 80}, 43)
    assert sum(t['totalMarks'] for t in SOURCE['tasks']) == 400
    return p


def figure_bindings():
    counts = defaultdict(int)
    result = {}
    for t in tasks():
        page = t['schemePages'][0]
        result[PREFIX + t['suffix']] = f'maths-2010-HL-scheme-p{page:03}-i{counts[page]}'
        counts[page] += 1
    result[PREFIX + '1-c-ii'] = result[PREFIX + '1-c-i']
    return result


def classify(text):
    if 'Attempt SIX QUESTIONS' in text:
        return 'whole-examination-selection', SOURCE['selectionReview'][0]['reason']
    if 'Choose one of the roots' in text:
        return 'expanded-alternatives', SOURCE['selectionReview'][1]['reason']
    if 'or otherwise' in text:
        return 'alternative-method', SOURCE['selectionReview'][2]['reason']
    raise ValueError('Unclassified selection directive: ' + text)


def write_review(p):
    p.review(SOURCE['printedQuestionMarks'],
        'Independent visual inspection of all six paper pages and scheme pages 1–40. All 40 original question and complete solution presentations plus the four exact fifth-root practice supplements inspected. All 43 practice routes retain original mark boundaries, alternative methods and full relevant deduction notes.',
        SOURCE['schemePagesInspected'], SOURCE['generalNotesPages'], SOURCE['notes'] + SOURCE['markingRules'],
        SOURCE['selectionReview'], classify)


def main():
    if len(sys.argv) > 1:
        quotes(ROWS, sys.argv[1]); return
    assert PRESENTATION['status'] == 'visually inspected', 'Inspect every crop before publication'
    p = build_paper(); write_review(p)
    overrides = {cid: {'section': 'A', 'figureKey': key} for cid, key in figure_bindings().items()}
    p.apply(ROWS, '2010 Higher Paper 1', expect_added=[c['id'] for c in p.cards],
            card_overrides=overrides, question_figures=True)


if __name__ == '__main__':
    main()
