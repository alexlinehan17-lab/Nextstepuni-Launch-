"""Shared wording for the English deferred review files (english-deferred-review/<year>-<hl|ol>.json).

Only the review files are data; this module builds the parts of them that are the
same sentence for every sitting of a level, so each sitting's file states only
what differs: its pages, its readers, what its scheme omits and the decisions.
    python3 scripts/markbank/authoring/english_deferred_review_common.py   (prints nothing; imported)
"""
from __future__ import annotations


def disc(p, c, l, m):
    return {'P': p, 'C': c, 'L': l, 'M': m}


def higher_criteria(year, grid_page, criteria_page=3):
    combined = ('One global mark ex {marks} from the H1–H8 band printed with the task (combined criteria grid '
                f'PDF{grid_page}); no P/C/L/M submarks.')
    combined_absent = ('One global mark ex {marks} on the combined H1–H8 grid printed in Appendix 2 '
                       f'(PDF{grid_page}); no P/C/L/M submarks.')
    discrete = (f'{year} HL deferred PDF{criteria_page}: marks for Coherence of Delivery or Efficiency of Language '
                'Use cannot exceed the marks awarded for Clarity of Purpose. Discrete H1–H8 grid printed with the '
                f'task and on PDF{grid_page}.')
    discrete_absent = (f'PDF{criteria_page} gives Clarity of Purpose, Coherence of Delivery and Efficiency of Language '
                       'Use 30% each and Accuracy of Mechanics 10% of the marks for every task, and C or L cannot '
                       'exceed P; the discrete H1–H8 grid for {marks} marks is printed on PDF'
                       f'{grid_page} (Appendix 2).')
    return {
        'qa': {'mode': 'holistic', 'notes': combined, 'absentNotes': combined_absent},
        'qb': {'mode': 'discrete', 'allocation': disc(15, 15, 15, 5), 'notes': discrete, 'absentNotes': discrete_absent},
        'composing': {'mode': 'discrete', 'allocation': disc(30, 30, 30, 10), 'notes': discrete,
                      'absentNotes': discrete_absent},
        'single': {'mode': 'discrete', 'allocation': disc(18, 18, 18, 6), 'notes': discrete,
                   'absentNotes': discrete_absent},
        'comparative-q1': {'mode': 'holistic', 'notes': combined, 'absentNotes': combined_absent},
        'comparative-q2': {'mode': 'discrete', 'allocation': disc(21, 21, 21, 7), 'notes': discrete,
                           'absentNotes': discrete_absent},
        'unseen': {'mode': 'holistic', 'notes': combined, 'absentNotes': combined_absent},
        'prescribed': {'mode': 'discrete', 'allocation': disc(15, 15, 15, 5), 'notes': discrete,
                       'absentNotes': discrete_absent},
    }


def higher_present_reasons(p1_pages, p2_pages, grid_page):
    view1, view2 = f'All {p1_pages} paper pages viewed.', f'All {p2_pages} paper pages viewed.'
    return {
        'qa': view1 + ' Exact task and award verified on scheme PDF{page}: “Mark ex {marks} by reference to the '
              f'criteria for assessment” with the H1–H8 band printed with the task (combined grid PDF{grid_page}). '
              'No invented splits or submarks.',
        'qb': view1 + ' Exact task and award verified on scheme PDF{page}: “Mark ex 50 by reference to the criteria '
              f'for assessment”, P 15 / C 15 / L 15 / M 5 printed with the task (discrete grid PDF{grid_page}).',
        'composing': view1 + ' Exact task and award verified on scheme PDF{page}: “Mark ex 100 by reference to the '
                     'criteria for assessment”, P 30 / C 30 / L 30 / M 10 printed with the composition (discrete '
                     f'grid PDF{grid_page}).',
        'single': view2 + ' Exact task and award verified on scheme PDF{page}: “Mark ex 60 … using the breakdown of '
                  f'marks below”, P 18 / C 18 / L 18 / M 6 printed with the task (discrete grid PDF{grid_page}).',
        'comparative-q1': view2 + ' Exact task and award verified on scheme PDF{page}: “Mark ex {marks} by reference '
                          'to the criteria for assessment”, one H1–H8 row printed with the part (combined grid '
                          f'PDF{grid_page}); the P/C/L/M lines describe the criteria and carry no marks.',
        'comparative-q2': view2 + ' Exact task and award verified on scheme PDF{page}: “Mark ex 70 … using the '
                          'breakdown of marks below”, P 21 / C 21 / L 21 / M 7 printed with the task (discrete grid '
                          f'PDF{grid_page}).',
        'unseen': view2 + ' Exact task and award verified on scheme PDF{page}: “Mark ex {marks} by reference to the '
                  f'criteria for assessment” (combined grid PDF{grid_page}). No invented splits or submarks.',
        'prescribed': view2 + ' Exact task and award verified on scheme PDF{page}: “Mark ex 50 … using the breakdown '
                      f'of marks below”, P 15 / C 15 / L 15 / M 5 printed with the task (discrete grid PDF{grid_page}).',
    }


def higher_absent_reasons(p1_pages, p2_pages, grid_page, criteria_page=3):
    rule = f'PDF{criteria_page}’s criteria (P, C, L 30%, M 10%; C/L ≤ P)'
    return {
        'composing': f'All {p1_pages} paper pages viewed; the prompt and its 100-mark tariff are the paper’s (“Each '
                     f'composition carries 100 marks”). Marked as every composition on this scheme: {rule} and the '
                     f'discrete 100-mark grid of Appendix 2, PDF{grid_page}. No task-specific guidance exists to quote.',
        'single': f'All {p2_pages} paper pages viewed; the prompt and its 60-mark tariff are the paper’s (SECTION I THE '
                  f'SINGLE TEXT (60 marks)). Marked as every Single Text task on this scheme: {rule} and the discrete '
                  f'60-mark grid of Appendix 2, PDF{grid_page}. No task-specific guidance exists to quote.',
        'comparative-q1': f'All {p2_pages} paper pages viewed; the prompt and its {{marks}}-mark tariff are the paper’s. '
                          'Marked as every two-part Comparative part on this scheme: one combined mark on the '
                          f'{{marks}}-mark H1–H8 row of Appendix 2, PDF{grid_page}. No task-specific guidance exists to '
                          'quote.',
        'comparative-q2': f'All {p2_pages} paper pages viewed; the prompt and its 70-mark tariff are the paper’s. Marked '
                          f'as every 70-mark Comparative question on this scheme: {rule} and the discrete 70-mark grid '
                          f'of Appendix 2, PDF{grid_page}. No task-specific guidance exists to quote.',
        'prescribed': f'All {p2_pages} paper pages viewed; the prompt and its 50-mark tariff are the paper’s. Marked as '
                      f'every Prescribed Poetry question on this scheme: {rule} and the discrete 50-mark grid of '
                      f'Appendix 2, PDF{grid_page}. No task-specific guidance exists to quote.',
        'qb': f'All {p1_pages} paper pages viewed; the prompt and its 50-mark tariff are the paper’s. Marked as every '
              f'Question B on this scheme: {rule} and the discrete 50-mark grid of Appendix 2, PDF{grid_page}.',
        'qa': f'All {p1_pages} paper pages viewed; the prompt and its {{marks}}-mark tariff are the paper’s. One combined '
              f'mark on the {{marks}}-mark H1–H8 row of Appendix 2, PDF{grid_page}.',
        'unseen': f'All {p2_pages} paper pages viewed; the prompt and its {{marks}}-mark tariff are the paper’s. One '
                  f'combined mark on the {{marks}}-mark H1–H8 row of Appendix 2, PDF{grid_page}.',
    }


SOURCE_REASON = ('All {pages} paper pages viewed: printed heading (in capitals), introduction, both columns and the '
                 'image checked. Scheme PDF{integral}: introductions and accompanying illustrations are integral parts '
                 'of the texts, so the whole text is retained.')


def ordinary_criteria(year, grid_pages, criteria_page=3):
    grid = 'PDF' + '–'.join(str(p) for p in (grid_pages[0], grid_pages[-1])) if len(grid_pages) > 1 else f'PDF{grid_pages[0]}'
    combined = (f'One global mark ex {{marks}} from the {year} OL deferred combined grid ({grid}, O1–O8), P+C and '
                'L+M read together.')
    discrete = (f'{year} OL deferred PDF{criteria_page}: marks for Coherence of Delivery or Efficiency of Language Use '
                f'cannot exceed the marks awarded for Clarity of Purpose. Discrete grid {grid} (O1–O8).')

    def comb(pc, lm):
        return {'mode': 'combined', 'allocation': {'P+C': pc, 'L+M': lm}, 'notes': combined, 'absentNotes': combined}

    def dis(p, c, l, m):
        return {'mode': 'discrete', 'allocation': disc(p, c, l, m), 'notes': discrete, 'absentNotes': discrete}
    return {
        'qa15': comb(9, 6), 'qa10': comb(6, 4), 'qb': dis(15, 15, 15, 5), 'composing': dis(30, 30, 30, 10),
        'single-q1': comb(6, 4), 'single-q': dis(9, 9, 9, 3), 'comparative-a': comb(9, 6),
        'comparative-b': dis(12, 12, 12, 4), 'unseen': comb(6, 4), 'prescribed-q1': comb(9, 6),
        'prescribed-q2': comb(12, 8),
    }


ORDINARY_AWARD = {
    'qa15': 'Combined Criteria ex 15, P + C = 9, L + M = 6', 'qa10': 'Combined Criteria ex 10, P + C = 6, L + M = 4',
    'qb': 'Discrete Criteria ex 50, P = 15, C = 15, L = 15, M = 5', 'composing': 'Discrete Criteria ex 100, 30/30/30/10',
    'single-q1': 'Combined Criteria ex 10, P + C = 6, L + M = 4', 'single-q': 'Discrete Criteria ex 30, 9/9/9/3',
    'comparative-a': 'Combined Criteria ex 15, P + C = 9, L + M = 6',
    'comparative-b': 'Discrete Criteria ex 40, P = 12, C = 12, L = 12, M = 4',
    'unseen': 'Combined Criteria ex 10, P + C = 6, L + M = 4', 'prescribed-q1': 'Combined Criteria ex 15, P + C = 9, L + M = 6',
    'prescribed-q2': 'Combined Criteria ex 20, P + C = 12, L + M = 8',
}


def ordinary_present_reasons(p1_pages, p2_pages, grid):
    out = {}
    for kind, award in ORDINARY_AWARD.items():
        pages = p1_pages if kind in ('qa15', 'qa10', 'qb', 'composing') else p2_pages
        out[kind] = (f'All {pages} paper pages viewed. Exact task and award verified on scheme PDF{{page}}: the part’s own '
                     f'line “{award}” printed with it (grid {grid}). No invented splits or submarks.')
    return out


def ordinary_absent_reasons(p1_pages, p2_pages, grid, criteria_page=3):
    out = {}
    for kind, award in ORDINARY_AWARD.items():
        pages = p1_pages if kind in ('qa15', 'qa10', 'qb', 'composing') else p2_pages
        out[kind] = (f'All {pages} paper pages viewed; the prompt and its {{marks}}-mark tariff are the paper’s. Marked as '
                     f'every part of its kind that this scheme does set out (“{award}”), on PDF{criteria_page}’s criteria '
                     f'(C/L ≤ P) and the grid {grid}. No task-specific guidance exists to quote.')
    return out
