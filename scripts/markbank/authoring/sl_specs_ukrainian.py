#!/usr/bin/env python3
"""Reviewed specs for the Ukrainian classic examination (small-languages lane).

One entry per printed ask with no live card; see sl_lib.py for the selector
language. Line numbers are lines of examiner-reports/ukrainian/schemes/<year>-hl.md.
Drafted by Opus helpers on the Bulgarian, Romanian, Dutch and Maltese models, integrated
and gated by the lane lead.
"""
from sl_lib import (R, S, SR, J, L, PL, PC, QP, QL, Run, pre, prerun, PP, SP, PY, RX, PaperP, PARTP, REM,  # noqa: F401
                    one, shown, graded, crit, examples, quote, unprinted, part, NoScheme)
from pl_listen_lib import Join  # noqa: F401

SPECS = {}


def both(*notes):
    """Several printed notes on one row, in order."""
    return lambda doc: ' '.join(n(doc) for n in notes)


# ================================================================ 2025 HL ===
# Carded by the lead (20 Nov). Live: Part I (I1a-e, I2-I6). Paper p4: ЧАСТИНА II
# "(30 балів)" (y534), the commentary; ЧАСТИНА III "(40 балів)" (y651), two
# titles joined by "Або". Reading text pp2-3 (the article to its source line,
# p3 y698; the census reads [4], the questions page).
# Scheme pp6-7: under the reprinted Part II task, "Наприклад:" (171) and seven
# bulleted points, the fifth running over the page break (184-185, 190-192;
# the page number 186 and the page head left out): shown rows on the paper's
# 30 (10a), the heading quoted. Part III: the instruction and both titles
# reprinted, nothing under them: R4 at the paper's 40 (ruling 4). The scheme's
# "(100–150 слів)" against the paper's "(100-150 слів)": punctuation, not quoted.
UNPRINTED_2025 = 'The scheme reprints the instruction and the two titles and prints nothing under them.'
SPECS[2025] = [
    R('II1', [shown(L(172, 175, after='• ')), shown(L(176, 178, after='• ')), shown(L(179, 181, after='• ')),
              shown(L(182, 183, after='• ')), shown(J(L(184, 185, after='• '), L(190, 192))),
              shown(L(193, 196, after='• ')), shown(L(197, 198, after='• '))],
      whole=True, total=PY(4, 534), rownote=quote(S(171), lead='The scheme heads its points'),
      question=QP(4, 'Напишіть коментар', '«Вишита сорочка'), pages=(2, 3)),
    R('III1', [unprinted(UNPRINTED_2025)], total=PY(4, 651),
      question=QP(4, 'Напишіть есе', '1. «Бережи')),
    R('III2', [unprinted(UNPRINTED_2025)], total=PY(4, 651),
      question=QP(4, 'Напишіть есе', '2. «Там, де')),
]


# ================================================================ 2026 HL ===
# Carded by the lead (20 Nov). Live: Part I. Paper p4: ЧАСТИНА II "(30 балів)"
# (y507), ЧАСТИНА III "(40 балів)" (y610), two titles joined by "Або", title
# 2 ending on its own attribution line. Reading text pp2-3 (to the source line,
# p3 y662). Scheme p7: under the reprinted task, the lead "У відповіді можна
# розглянути ... аспектів:" (159-160) and nine bulleted aspects: shown rows on
# the paper's 30 (10a), the lead quoted. Part III: instruction and titles
# reprinted, nothing under them: R4 at 40.
SPECS[2026] = [
    R('II1', [shown(S(n, after='• ')) for n in range(161, 170)],
      whole=True, total=PY(4, 507), rownote=quote(L(159, 160), lead='The scheme heads its points'),
      question=QP(4, 'Напишіть коментар', '«І жодна машина'), pages=(2, 3)),
    R('III1', [unprinted(UNPRINTED_2025)], total=PY(4, 610),
      question=QP(4, 'Напишіть есе', '1. Технології')),
    R('III2', [unprinted(UNPRINTED_2025)], total=PY(4, 610),
      question=QP(4, 'Напишіть есе', Run('2. «Людина без вади', '(Андрій Любка).'))),
]


def specs(year):
    return SPECS.get(year, [])
