#!/usr/bin/env python3
"""Reviewed specs for the Romanian classic examination (small-languages lane).

One entry per printed ask; see sl_lib.py for the selector language. Line
numbers are lines of examiner-reports/romanian/schemes/<year>-hl.md.
"""
from sl_lib import (R, S, J, L, PL, PC, QP, Run, pre, prerun, PP, SP, PY, RX, PaperP, PARTP,  # noqa: F401
                    one, shown, graded, crit, examples, quote, unprinted, part, NoScheme)

SPECS = {}


def both(*notes):
    """Several printed notes on one row, in order."""
    return lambda doc: ' '.join(n(doc) for n in notes)


def bullets(*spans):
    """Shown rows, one per printed bullet: each a span (a, b) of wrapped lines."""
    return [shown(L(a, b, after='• ')) if isinstance(a, int) else a
            for a, b in ((sp, sp) if isinstance(sp, int) else sp for sp in spans)]


# ================================================================ 2010 HL ===
# Paper p3: Q1 "(5x1 puncte)" over five expressions; the scheme answers them as
# five unlettered bullets in the paper's order (each matches its expression's
# words: docu-, edu-, infotainment, plan de marketing, obiectivitate), priced
# "(5 puncte)" for the question. Q2-Q6 "(5 puncte)" each over points with no
# split: shown, priced as a whole (10a); Q3 is one explanation. Q2's first
# bullet is one sentence the SEC bulleted line by line (rendered p2): joined.
# Parts II (30) and III (40) on the four criteria the scheme prints for both
# (p4), 30/30/30/10 % (10b).
CRIT_2010 = crit((94, 95), (96, 97), (98, 99), 100)
SPECS[2010] = [
    R('I1a', [one(L(20, 21, after='• '), PP())]),
    R('I1b', [one(L(22, 23, after='• '), PP())]),
    R('I1c', [one(L(24, 25, after='• '), PP())]),
    R('I1d', [one(L(26, 27, after='• '), PP())]),
    R('I1e', [one(L(28, 29, after='• '), PP())]),
    R('I2', [shown(J(S(32, after='• '), S(33, after='• '), S(34, after='• '))), shown(L(35, 37, after='• ')),
             shown(L(38, 41, after='• '))], whole=True),
    R('I3', [one(L(44, 47), PP())]),
    R('I4', [shown(S(55, after='• '), lead=S(54)), shown(S(56, after='• '), lead=S(54)),
             shown(L(57, 58, after='• '), lead=S(54)), shown(S(60, after='• '), lead=S(59)),
             shown(S(61, after='• '), lead=S(59)), shown(L(62, 63, after='• '), lead=S(59))], whole=True,
      rownote=quote(S(53, after='4. '), lead='The scheme heads it')),
    R('I5', bullets((67, 69), (70, 72), (73, 74)), whole=True,
      rownote=quote(L(65, 66, after='5. '), lead='The scheme heads it')),
    R('I6', bullets((78, 80), 81, (82, 83), (84, 85), 86), whole=True,
      rownote=quote(L(76, 77, after='6. '), lead='The scheme heads it')),
    R('II1', [graded(L(102, 105), PARTP(), CRIT_2010)],
      rownote=quote(S(93), lead='The scheme prints')),
    R('III1', [graded(L(107, 108), PARTP(), CRIT_2010)],
      rownote=quote(S(93), lead='The scheme prints'),
      question=QP(4, 'Scrieţi un comentariu de aproximativ 300', '1. “Informaţia')),
    R('III2', [graded(L(107, 108), PARTP(), CRIT_2010)],
      rownote=quote(S(93), lead='The scheme prints'),
      question=QP(4, 'Scrieţi un comentariu de aproximativ 300', '2. Nimeni')),
]


def specs(year):
    return SPECS.get(year, [])
