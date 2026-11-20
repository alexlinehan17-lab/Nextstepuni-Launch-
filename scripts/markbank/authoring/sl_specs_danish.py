#!/usr/bin/env python3
"""Reviewed specs for the Danish classic examination (small-languages lane).

One entry per printed ask with no live card; see sl_lib.py for the selector
language. Line numbers are lines of examiner-reports/danish/schemes/<year>-hl.md.
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
# The SEC published no marking scheme for 2010 (SOURCES.md item 5: not in the
# archive listing; no scheme on disk). Every ask is carded with the paper's own
# price and the fixed line NO_SCHEME_PUBLISHED, unscored (R4), by the lead.
# Paper (rendered pp2-4): the text runs pp2-3 (paragraphs 1-8, to y380 on p3);
# Opgave I "(maksimum 30 point)": Q1 prints five unlettered expressions under
# "(5 x 1 point)" (one ask in the census), Q2-Q6 "(5 point)" each; Opgave II
# "(maksimum 30 point)" (p4), the commentary; Opgave III "(maksimum 40 point)",
# one essay task with its two titles as dashes (one ask in the census).
SPECS[2010] = [
    NoScheme('I1', pages=(2, 3)),
    NoScheme('I2', pages=(2, 3)),
    NoScheme('I3', pages=(2, 3)),
    NoScheme('I4', pages=(2, 3)),
    NoScheme('I5', pages=(2, 3)),
    NoScheme('I6', pages=(2, 3)),
    NoScheme('II1', total=PARTP(), pages=(2, 3)),
    NoScheme('III1', total=PARTP()),
]


def specs(year):
    return SPECS.get(year, [])
