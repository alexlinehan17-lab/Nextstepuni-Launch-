#!/usr/bin/env python3
"""Reviewed specs for the Hungarian classic examination (small-languages lane).

One entry per printed ask with no live card; see sl_lib.py for the selector
language. Line numbers are lines of examiner-reports/hungarian/schemes/<year>-hl.md.
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


# ================================================================ 2010 HL ===
# Carded by the lead (20 Nov). Live: Part I. Paper p4: II. RÉSZ "(30 pont / 100
# pont)" (y70), the commentary on one sentence; III. RÉSZ "(40 pont / 100 pont)"
# (y217), two titles ("1. lehetőség" / "vagy" / "2. lehetőség"). Scheme p3-4:
# "A II. és III. részben elérhető pontok az alábbi szempontok szerint oszlanak
# meg:" (103) and the four criteria at 30/30/30/10 % (104-110): both parts
# graded (10b). Part II's head is its requirement line (77), its "Lehetséges
# irányok:" (78) quoted as examples; Part III's head is its own line (94), each
# title's "Egyéni válasz körülbelül 300 szóban." left to the head. The labels
# "1. lehetőség" / "2. lehetőség" are not part of the titles.
CRIT_2010 = crit((104, 105), (106, 107), (108, 109), 110)
LEAD_2010 = quote(S(103), lead='The scheme prints')
SPECS[2010] = [
    R('II1', [graded(S(77), PARTP(), CRIT_2010)],
      rownote=both(LEAD_2010, examples(S(78), L(79, 80, after='• '), L(81, 82, after='• '), L(83, 84, after='• '),
                                       S(85, after='• '), S(86, after='• '), S(87, after='• '))),
      question=QP(4, 'A szöveg alapján kommentáld', 'Pénzt kell költeni'), pages=(2, 3)),
    R('III1', [graded(S(94), PARTP(), CRIT_2010)], rownote=LEAD_2010,
      question=QP(4, 'A két téma közül', 'Reklámok: hiszünk')),
    R('III2', [graded(S(94), PARTP(), CRIT_2010)], rownote=LEAD_2010,
      question=QP(4, 'A két téma közül', Run('„Senki sem', '(J. Donne'))),
]


def specs(year):
    return SPECS.get(year, [])
