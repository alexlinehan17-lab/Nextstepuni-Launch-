#!/usr/bin/env python3
"""Economics 2021 Higher Level — Section B.

Same rules as econ_2024_hl.py. This paper runs its responses together under bold
headings with no bullet, so it splits with `heads()`, and it writes the split of
each answer's own marks as a second cell — `⟨2 @ 7⟩ ⟨(3 + 4)⟩` means two answers
at 7, each of which is 3 for the point and 4 for developing it. That inner split
is between parts of ONE answer, not between the two answers, so it does not make
a descending tariff.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from econ_lib import anyN, block, card, defurnish, emit, heads, load, tidy  # noqa: E402

YEAR, LEVEL = 2021, 'higher'
T = tidy(load(YEAR, LEVEL))
BODY = block(T, 'Question 12 Possible responses Max Mark', occ=0)


def menu(cid, topic, concept, ref, qtext, notation, total, verbatim, claim, per,
         start, end, headings, note, notes='', steps=None, stem=''):
    chunk = block(BODY, start, end)
    return card(cid, YEAR, LEVEL, topic, concept, ref, qtext, notation, total,
                [anyN('r-1', verbatim, None if steps else total, claim, per,
                      [defurnish(h) for h in heads(chunk, headings)], note, steps=steps)],
                notes, stem=stem,
                tariff_kind='fixed' if steps else 'bestNofParts')


cards = [
    menu('econ-2021-hl-q12-b-i', 'economics-3-1', 'reasons-for-the-125-corporation-tax-rate',
         '2021 HL Q12(b)(i)',
         'The Minister for Finance reaffirmed Ireland’s commitment to the 12.5% corporation tax '
         'rate. Evaluate two reasons why the Minister for Finance made this decision.',
         '2 @ 7', 14, 'A reason for keeping the 12.5% rate — any two', 2, 7,
         'Incentivise FDI / discourage any exodus of MNCs',
         '(b) The Irish government has repeatedly rejected calls',
         ['Incentivise FDI / discourage any exodus of MNCs', 'Maintain employment levels',
          'Government revenue', 'Maintain economic growth', 'Loss of fiscal sovereignty'],
         'Two reasons, 7 marks each — the scheme splits each into 3 for the reason and 4 for '
         'developing it, so a named reason with nothing after it earns less than half.'),

    menu('econ-2021-hl-q12-c-i', 'economics-4-2', 'implications-of-brexit-for-ireland',
         '2021 HL Q12(c)(i)',
         'The United Kingdom left the European Union on January 31, 2020. Discuss two '
         'implications of this exit for the Irish economy.',
         '2 @ 6', 12, 'An implication of Brexit for Ireland — any two', 2, 6,
         'Possible negative effect on Irish exports',
         '(ii) Outline two possible advantages to Ireland of remaining a member of the EU',
         ['Possible negative effect on Irish exports',
          'Effects on agricultural sector / agri-food sectors', 'Labour market effects',
          'Imports from the UK'],
         'Two implications, 6 marks each, split 3 for the point and 3 for developing it.'),

    menu('econ-2021-hl-q12-c-ii', 'economics-4-1', 'advantages-of-eu-membership',
         '2021 HL Q12(c)(ii)',
         'Outline two possible advantages to Ireland of remaining a member of the EU.',
         '2 @ 6', 12, 'An advantage of EU membership — any two', 2, 6,
         'Free Trade Area / larger market / trade expansion', 'Question 13',
         ['Free Trade Area / larger market / trade expansion',
          'Access to capital / research funding', 'Freedom movement of capital / labour',
          'Foreign Direct Investment / job creation'],
         'Two advantages, 6 marks each, split 3 for the point and 3 for developing it.'),
]

emit(cards)
