#!/usr/bin/env python3
"""Economics 2022 Higher Level — Section B.

Authored against econ_parts; see econ_2021_hl.py for what `drop` is for. This
paper writes its tariffs as ⟨1 x 8⟩ rather than ⟨1 @ 8⟩ — the same shape with a
different sign — and one part sets an argument FOR against an argument AGAINST
under a single heading, which is carded a side at a time.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from econ_auto import Paper  # noqa: E402
from econ_lib import anyN, block, bullets, card, load, tidy  # noqa: E402

P = Paper(2022, 'higher')
SCAFFOLD = ('Possible responses', 'Suggested responses', 'Must have a minimum')

P.menu('interventions the Irish government could pursue to support balanced',
       'econ-2022-hl-q11-a-ii', 'economics-3-5', 'balanced-regional-development',
       'Outline two possible interventions the Irish government could pursue to support balanced '
       'regional development in Ireland.',
       'An intervention for balanced regional development — any two',
       'Two interventions, the first paid 8 and the second 4.',
       claim=2, per=8, steps=[8, 4], drop=SCAFFOLD)

P.menu('Other than land being fixed in supply', 'econ-2022-hl-q11-b-ii',
       'economics-1-2', 'characteristics-of-land',
       'Other than land being fixed in supply, outline two characteristics of land in the '
       'economic sense.',
       'A characteristic of land — any two',
       'Two characteristics, 5 marks each. Fixed supply is excluded by the question.',
       drop=SCAFFOLD)

P.menu('should provide more financial support to regional airports', 'econ-2022-hl-q11-c-iii-for',
       'economics-1-3', 'arguments-for-supporting-regional-airports',
       'The Irish government should provide more financial support to regional airports around '
       'Ireland. Discuss the arguments FOR this statement.',
       'An argument for financial support — any two',
       'Two arguments, 6 marks each.',
       ref='2022 HL Q11(c)(iii) — for',
       drop=SCAFFOLD + ('For financial support',), stop='Against financial support',
       notes='The part asks for arguments both for and against and the scheme heads the two '
             'lists separately, so each side is its own card.')

P.menu('should provide more financial support to regional airports', 'econ-2022-hl-q11-c-iii-against',
       'economics-1-3', 'arguments-against-supporting-regional-airports',
       'The Irish government should provide more financial support to regional airports around '
       'Ireland. Discuss the arguments AGAINST this statement.',
       'An argument against financial support — any two',
       'Two arguments, 6 marks each.',
       ref='2022 HL Q11(c)(iii) — against',
       drop=SCAFFOLD + ('For financial support', 'Supports the government', 'Supports employment',
                        'Supports developing rura', 'Against financial suppor'))

P.menu('reasons why a government would decide to deregulate', 'econ-2022-hl-q12-a-ii',
       'economics-2-0', 'reasons-to-deregulate',
       'Explain two reasons why a government would decide to deregulate its electricity supply.',
       'A reason to deregulate — any two',
       'Two reasons, 3 marks each.',
       drop=SCAFFOLD)

P.menu('changes in market conditions (characteristics) which allows a market to move',
       'econ-2022-hl-q12-b-iii', 'economics-2-0', 'monopoly-versus-oligopoly',
       'Explain two changes in market conditions which allow a market to move from a Monopoly to '
       'an Oligopoly.',
       'A change in market conditions — any two',
       'Two changes, 3 marks each.',
       drop=SCAFFOLD)

P.menu('interventions, other than incentives/taxes', 'econ-2022-hl-q13-b-ii',
       'economics-1-3', 'interventions-to-influence-behaviour',
       'Outline two interventions, other than incentives/taxes, that a government could implement '
       'to influence consumer behaviour.',
       'An intervention to influence behaviour — any two',
       'Two interventions, 6 marks each. Incentives and taxes are excluded by the question.',
       drop=SCAFFOLD)

P.menu('possible economic effects of this measure for the Irish economy', 'econ-2022-hl-q13-c-i',
       'economics-3-1', 'effects-of-the-15-percent-minimum-tax',
       'Ireland signed up to the OECD minimum corporation tax rate of 15% for large companies. '
       'Outline the possible economic effects of this measure for the Irish economy.',
       'An economic effect of the 15% rate — any two',
       'Two effects, 8 marks each. The scheme lists gains and costs together — a higher rate is '
       'not simply bad for Ireland.',
       drop=SCAFFOLD)

P.menu('Explain each of the following economic terms in the context of Irish agriculture',
       'econ-2022-hl-q15-a-ii', 'economics-1-3', 'subsidy-and-quota',
       'Explain each of the following economic terms in the context of Irish agriculture: '
       'subsidy; quota.',
       'The two terms — both of them',
       'Both terms, 4 marks each. The question names them, so this is not a choice.',
       drop=SCAFFOLD)

P.menu('Justify why countries which are Net Contributors', 'econ-2022-hl-q15-c-ii',
       'economics-4-1', 'why-net-contributors-stay-in-the-eu',
       'Justify why countries which are Net Contributors to the EU, despite the financial cost '
       'of membership, still decide to remain members.',
       'A reason a net contributor stays — any two',
       'Two reasons, 5 marks each.',
       drop=SCAFFOLD)

P.menu('likely impacts of this government intervention on social sustainability',
       'econ-2022-hl-q16-a-i', 'economics-0-2', 'rent-caps-and-social-sustainability',
       'What are the likely impacts of rent caps on social sustainability?',
       'An impact on social sustainability — any one',
       'One impact, 8 marks; the paper pays a second at 4.',
       claim=1, per=8, drop=SCAFFOLD)

P.menu('Other than rent caps, suggest two other government interventions',
       'econ-2022-hl-q16-a-ii', 'economics-1-3', 'interventions-for-housing-access',
       'Other than rent caps, suggest two other government interventions which could help reduce '
       'inequality in accessing the Irish housing market.',
       'An intervention other than rent caps — any two',
       'Two interventions, the first paid 8 and the second 4.',
       claim=2, per=8, steps=[8, 4], drop=SCAFFOLD)

P.menu('strategies that could be employed by the Irish government and Irish citizens',
       'econ-2022-hl-q16-b-ii', 'economics-0-2', 'transition-to-a-low-carbon-economy',
       'Suggest strategies that could be employed by the Irish government to aid the transition '
       'to a low carbon economy.',
       'A government strategy — any two',
       'The paper pays 7 for the government strategy and 7 for the citizen one; the scheme lists '
       'the government strategies first.',
       claim=2, per=7, drop=SCAFFOLD, cap=8)

P.menu('steps consumers in Ireland can take to reduce the effects of the fast fashion',
       'econ-2022-hl-q16-c-ii', 'economics-0-2', 'consumer-steps-on-fast-fashion',
       'Outline two steps consumers in Ireland can take to reduce the effects of the fast '
       'fashion industry.',
       'A step a consumer can take — any two',
       'Two steps, 5 marks each. The scheme heads this list "The Irish Consumer" and lists the '
       'business steps separately, so the two are not interchangeable.',
       drop=SCAFFOLD + ('The Irish Consumer',))

# The extractor folds this part's first two responses into the question, because
# the mark cell is printed after them rather than before. Sliced by hand instead.
BODY = block(tidy(load(2022, 'higher')), 'Question 11 Possible responses Max Mark', occ=0)
P.cards.append(card(
    'econ-2022-hl-q11-a-i', 2022, 'higher', 'economics-2-1', 'regional-rent-disparity',
    '2022 HL Q11(a)(i)',
    'Outline two possible reasons for the disparity in average rents between Dublin City and '
    'Waterford City in Q2, 2021.',
    '1 x 8 + 1 x 4', 12,
    [anyN('r-1', 'A reason for the rent disparity — any two', None, 2, 8,
          bullets(block(BODY, '• Greater population per sq. km in Dublin',
                        '(ii) Outline two possible interventions')),
          'Two reasons, the first paid 8 and the second 4.', steps=[8, 4])],
    '', tariff_kind='fixed'))

P.emit()
