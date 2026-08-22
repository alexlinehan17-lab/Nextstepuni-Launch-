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


# ── Section B, second pass ──────────────────────────────────────────────────
SIDES3 = ('The part asks for one of each and the scheme heads the two lists separately, so each '
          'side is its own card.')

P.menu('opportunity cost involved in the above government expenditure',
       'econ-2022-hl-q11-c-ii', 'economics-0-1', 'opportunity-cost-of-transport-spending',
       'Outline one opportunity cost involved in government expenditure on transport, using an '
       'example to illustrate your answer.',
       'The opportunity cost, with an example',
       'One point, 5 marks. The spending is capital, so the example must be capital spending '
       'forgone — a hospital or a school, not a wage bill.',
       ref='2022 HL Q11(c)(ii)', claim=1, per=5,
       drop=SCAFFOLD + ('transport, using an example',))

P.menu('privatise a semi-state body instead of deregulation', 'econ-2022-hl-q12-a-iv',
       'economics-1-3', 'why-privatise-rather-than-deregulate',
       'Outline one reason why a government may choose to privatise a semi-state body instead of '
       'deregulation.',
       'A reason to privatise — any one',
       'One reason, 5 marks.',
       ref='2022 HL Q12(a)(iv)', claim=1, per=5,
       drop=SCAFFOLD + ('Outline one reason why a government may choose',))

P.menu('best described as a State Monopoly', 'econ-2022-hl-q12-b-i-monopoly',
       'economics-2-0', 'advantages-of-a-state-monopoly',
       'The 2005 electricity market is best described as a State Monopoly. Outline one advantage '
       'of that market structure.',
       'An advantage of monopoly — any one',
       'One advantage, 5 marks.',
       ref='2022 HL Q12(b)(i) — monopoly', claim=1, per=5,
       drop=SCAFFOLD, stop='Stability in prices', notes=SIDES3)

P.menu('best described as a State Monopoly', 'econ-2022-hl-q12-b-i-oligopoly',
       'economics-2-0', 'advantages-of-an-oligopoly',
       'The 2019 electricity market is best described as an Oligopoly. Outline one advantage of '
       'that market structure.',
       'An advantage of oligopoly — any one',
       'One advantage, 5 marks.',
       ref='2022 HL Q12(b)(i) — oligopoly', claim=1, per=5,
       drop=SCAFFOLD, after='Stability in prices')

P.menu('additional data centres in Ireland', 'econ-2022-hl-q12-c-ii-for',
       'economics-1-3', 'the-case-for-more-data-centres',
       'Discuss one reason why the Irish government SHOULD grant planning permission to '
       'additional data centres in Ireland.',
       'A reason to grant permission — any one',
       'One reason, 4 marks.',
       ref='2022 HL Q12(c)(ii) — for', claim=1, per=4,
       drop=SCAFFOLD + ('Reasons for granting planning permission',),
       stop='Reasons against granting planning permission', notes=SIDES3)

P.menu('additional data centres in Ireland', 'econ-2022-hl-q12-c-ii-against',
       'economics-1-3', 'the-case-against-more-data-centres',
       'Discuss one reason why the Irish government should NOT grant planning permission to '
       'additional data centres in Ireland.',
       'A reason to refuse permission — any one',
       'One reason, 4 marks.',
       ref='2022 HL Q12(c)(ii) — against', claim=1, per=4,
       drop=SCAFFOLD + ('Possible responses',), after='Reasons against granting planning permission')

P.menu('social benefits represent such a high proportion', 'econ-2022-hl-q13-a-i',
       'economics-3-1', 'why-social-benefits-dominate-spending',
       'Using the infographic, explain why social benefits represent such a high proportion of '
       'government expenditure. Use an example of a social benefit to support your answer.',
       'A reason social benefits are so large — any one',
       'One explanation, 5 marks.',
       ref='2022 HL Q13(a)(i)', claim=1, per=5, drop=SCAFFOLD)

P.menu('incentive the government uses to encourage', 'econ-2022-hl-q13-b-i-incentive',
       'economics-1-3', 'incentives-that-change-behaviour',
       'Outline one possible incentive the government uses to encourage certain human behaviour, '
       'with an example.',
       'An incentive — any one',
       'One incentive, 7 marks.',
       ref='2022 HL Q13(b)(i) — incentive', claim=1, per=7,
       drop=SCAFFOLD, stop='Plastic bag tax', notes=SIDES3)

P.menu('incentive the government uses to encourage', 'econ-2022-hl-q13-b-i-tax',
       'economics-1-3', 'taxes-that-change-behaviour',
       'Outline one possible tax measure to discourage certain human behaviour. Give an '
       'example to support your answer.',
       'A tax measure — any one',
       'One measure, 7 marks.',
       ref='2022 HL Q13(b)(i) — tax measure', claim=1, per=7,
       drop=SCAFFOLD, after='Plastic bag tax')

P.menu('impose the new 15% corporation tax rate on all firms', 'econ-2022-hl-q13-c-ii-yes',
       'economics-3-1', 'taxing-all-firms-at-15-percent-for',
       'Should the Irish Government impose the new 15% corporation tax rate on ALL firms in '
       'Ireland, regardless of turnover? Justify a YES answer.',
       'A reason to impose it on all firms — any one',
       'One justification, 8 marks.',
       ref='2022 HL Q13(c)(ii) — yes', claim=1, per=8,
       drop=SCAFFOLD + ('For implementation',), stop='Against implementation',
       notes='The part is answered either way and the scheme heads the two lists separately, so '
             'each side is its own card.')

P.menu('impose the new 15% corporation tax rate on all firms', 'econ-2022-hl-q13-c-ii-no',
       'economics-3-1', 'taxing-all-firms-at-15-percent-against',
       'Should the Irish Government impose the new 15% corporation tax rate on ALL firms in '
       'Ireland, regardless of turnover? Justify a NO answer.',
       'A reason not to impose it on all firms — any one',
       'One justification, 8 marks.',
       ref='2022 HL Q13(c)(ii) — no', claim=1, per=8,
       drop=SCAFFOLD, after='Against implementation')

# ── further Section B parts ────────────────────────────────────────────────
P.menu('reason why a gender pay gap persists in many European countries',
       'econ-2022-hl-q14-c-ii', 'economics-3-5', 'why-a-gender-pay-gap-persists',
       'Explain one reason why a gender pay gap persists in many European countries.',
       'A reason the gap persists — any one',
       'One reason, 5 marks: 2 for naming it and 3 for explaining it. The scheme lists seven.',
       ref='2022 HL Q14(c)(ii)', claim=1, per=5, drop=SCAFFOLD)

# The question runs on into what the scheme prints as its first response, so
# that line is dropped and the full wording is given here.
P.menu('knowledge of price elasticity of demand (PED) might be helpful',
       'econ-2022-hl-q15-b-iii', 'economics-1-2', 'using-ped-to-set-an-export-price',
       'Explain how a knowledge of price elasticity of demand (PED) might be helpful to Irish '
       'exporters who wish to maximise their total revenue in the UK market.',
       'A use of PED to an exporter — any one', 'One explanation, 6 marks.',
       ref='2022 HL Q15(b)(iii)', claim=1, per=6,
       drop=SCAFFOLD + ('exporters who wish to maximise their total revenue',))

P.menu('importance of environmental sustainability for the future of our economy',
       'econ-2022-hl-q16-b-i', 'economics-0-2', 'why-environmental-sustainability-matters',
       'Outline the importance of environmental sustainability for the future of our economy.',
       'A reason it matters — any one', 'One reason, 7 marks: 4 for the point and 3 for '
       'developing it. The scheme lists four.',
       ref='2022 HL Q16(b)(i)', claim=1, per=7, drop=SCAFFOLD)

P.menu('Rapid increase in milk production', 'econ-2022-hl-q15-a-i',
       'economics-1-4', 'reading-trends-in-irish-milk-production',
       'Analyse two key trends in Irish milk production across the time period in the chart.',
       'A trend — any two', 'Two trends, 4 marks each.',
       ref='2022 HL Q15(a)(i)', claim=2, per=4, drop=SCAFFOLD)

# Q15(a)(iii) is not carded: the scheme's tariff reads 9/5 across a part whose
# marks are mostly for a labelled diagram, and it does not say how much of that
# belongs to the written steps. I had it at 4 x 1, which was my arithmetic.

P.emit()
