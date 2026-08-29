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
from econ_lib import anyN, as_option, block, bullets, card, load, point, tidy  # noqa: E402

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

P.menu('one step businesses in Ireland can take', 'econ-2022-hl-q16-c-iii',
       'economics-0-2', 'how-business-can-curb-fast-fashion',
       'Outline one step businesses in Ireland can take to reduce the effects of the fast '
       'fashion industry.',
       'A step a business can take — any one', 'One step, 2 for the point and 3 for '
       'developing it. The scheme lists five.',
       ref='2022 HL Q16(c)(iii)', claim=1, per=2,
       drop=SCAFFOLD + ('Deduct 1m', 'The Research Process', 'Data: 5 quantitative'))

# Q15(b)(ii). The scheme runs its six impacts together as headed paragraphs
# rather than bullets, so the extractor read them as two welded runs and the
# audit flagged both. Split at the scheme's own headings instead — and claim
# what the printed tariff says, ⟨2 x 7⟩⟨(4 + 3)⟩: two impacts at 7, not one at 4.
BREXIT = [as_option(block(BODY, a, b)) for a, b in (
    ('Possible negative effect on Irish exports', 'Effects on agricultural sector'),
    ('Effects on agricultural sector', 'Labour market effects'),
    ('Labour market effects', 'Imports from the UK.'),
    ('Imports from the UK.', 'Relocation of U.K. based firms'),
    ('Relocation of U.K. based firms', 'Instability in Northern Ireland'),
    ('Instability in Northern Ireland', '(iii) Explain how a knowledge of price elasticity'),
)]
P.cards.append(card(
    'econ-2022-hl-q15-b-ii', 2022, 'higher', 'economics-4-2', 'brexit-and-irish-uk-trade',
    '2022 HL Q15(b)(ii)',
    'Apart from the change in exchange rates between the two currencies, outline two other '
    'impacts Brexit has had on the trade relationship between the UK and Ireland.',
    '2 x 7', 14,
    [anyN('r-1', 'An impact — any two', 14, 2, 7, BREXIT,
          'Two impacts, 7 marks each: 4 for the point and 3 for developing it.')],
    ''))

# ── The term definitions, built from the scheme directly ────────────────────
# Each of these prints one answer as a single block — a definition, not a menu
# — so the card is a point row sliced by hand. Scheme typos ride along
# uncorrected, because retyping is how corruption enters.

P.cards.append(card(
    'econ-2022-hl-q11-c-i', 2022, 'higher', 'economics-0-1', 'what-opportunity-cost-is',
    '2022 HL Q11(c)(i)',
    # The paper's own question is five words — too short for the citation gate
    # to place — so the paper's lead-in about the project rides in front of it.
    'The North Runway Project at Dublin airport is estimated to cost €250m - €500m. Explain '
    'the term opportunity cost.',
    '8', 8,
    [point('r-1', as_option(block(BODY, 'Opportunity cost refers to the cost of foregone '
                                        'alternatives')), 8,
           'One definition, 8 marks: the cost of the next best alternative forgone.')],
    'The applied opportunity cost on this question, Q11(c)(ii), is carded separately.',
    tariff_kind='fixed'))

P.cards.append(card(
    'econ-2022-hl-q12-a-iii', 2022, 'higher', 'economics-1-3', 'what-privatisation-is',
    '2022 HL Q12(a)(iii)',
    # Four words on the paper — too short for the citation gate to place — so
    # the paper's next sentence, the (iv) lead-in, rides in front of it.
    'A government could choose privatisation of a semi-state body over deregulation. Explain '
    'the term privatisation.',
    '4', 4,
    [point('r-1', as_option(block(BODY, 'This is the sale of a state-owned company')), 4,
           'One definition, 4 marks. Whole or partial sale both count.')],
    'The reason to privatise rather than deregulate, Q12(a)(iv), is carded separately.',
    tariff_kind='fixed'))

P.cards.append(card(
    'econ-2022-hl-q14-a-i', 2022, 'higher', 'economics-3-3', 'what-cost-push-inflation-is',
    '2022 HL Q14(a)(i)',
    'Explain the term cost push inflation with reference to the statement above.',
    '3 + 3', 6,
    [point('r-1', as_option(block(BODY, 'Cost push inflation refers to increases in the '
                                        'average price')), 6,
           '3 for the definition and 3 for relating it to the statement: dearer cement and '
           'timber pushing up house prices.')],
    '', tariff_kind='fixed',
    stem='The cost of building a house has risen by 30% in 2021. Everything has gone up by a '
         'staggering rate, from the price of a bag of cement, to the timber on the roof, to '
         'the steel. The cost of building a house in late 2021 was €70,000 more than was '
         'originally budgeted.'))

# Q13(a)(ii). Two definitions with their examples, priced ⟨6 + 2⟩ each — the
# question names both taxes, so this is not a choice.
P.cards.append(card(
    'econ-2022-hl-q13-a-ii', 2022, 'higher', 'economics-3-1', 'direct-and-indirect-taxes',
    '2022 HL Q13(a)(ii)',
    'The Irish government uses both direct and indirect tax to raise government revenue. '
    'Distinguish between these two types of taxes. Use examples of each to support your answer.',
    '(6 + 2) + (6 + 2)', 16,
    [point('r-direct', as_option(block(BODY, 'Direct taxes are taxes placed upon income and '
                                             'wealth',
                                       'Indirect taxes are taxes placed')), 8,
           'Direct tax: 6 for the distinction and 2 for an example.'),
     point('r-indirect', as_option(block(BODY, 'Indirect taxes are taxes placed on spending')), 8,
           'Indirect tax: 6 for the distinction and 2 for an example.')],
    '', tariff_kind='fixed'))

# Q12(c)(i). A menu the extractor drops: the ⟨2 x 4⟩ cell is printed beside the
# (c) lead-in, so the (i) segment that holds the bullets arrives with no cells
# and is skipped. Sliced by hand instead.
P.cards.append(card(
    'econ-2022-hl-q12-c-i', 2022, 'higher', 'economics-0-2',
    'challenges-of-a-carbon-neutral-motor-industry', '2022 HL Q12(c)(i)',
    'Outline two challenges which the Irish economy faces in transforming the Irish motor '
    'industry into a carbon neutral industry.',
    '2 x 4', 8,
    [anyN('r-1', 'A challenge — any two', 8, 2, 4,
          bullets(block(BODY, 'Prohibitive cost of electric cars',
                        'Discuss one reason why the Irish government should grant')),
          'Two challenges, 4 marks each, split 2 for the challenge and 2 for developing it.')],
    '',
    stem='By 2030, there will be an estimated 500,000 electric vehicles on Irish roads with '
         'proposals already in place to ban the sale of non-zero emission vehicles.'))

# Q11(b)(iii). The ⟨5⟩ cell is printed a line into the response, so the head of
# the answer is welded to the extractor's question. Sliced whole instead.
P.cards.append(card(
    'econ-2022-hl-q11-b-iii', 2022, 'higher', 'economics-1-2', 'derived-demand-and-land',
    '2022 HL Q11(b)(iii)',
    'Explain how the concept of derived demand relates to the factor of production land.',
    '5', 5,
    [point('r-1', as_option(block(BODY, 'Derived demand states that a factor of production')), 5,
           'The concept, then its application: land is wanted for what it lets you produce, '
           'not for itself.')],
    '', tariff_kind='fixed'))

# Q14(b)(iii). The cost table is in the figure manifest whole; row 4 prints the
# marginal cost of €55,000 the part turns on. The calculations for A, B and C
# in (b)(i) are worked figures and are not carded.
P.cards.append(card(
    'econ-2022-hl-q14-b-iii', 2022, 'higher', 'economics-1-5', 'profit-maximising-output',
    '2022 HL Q14(b)(iii)',
    'If the firm earns €55,000 for an additional unit of output produced, how many houses '
    'should it produce? Explain your answer.',
    '5', 5,
    [point('r-1', as_option(block(BODY, 'The firm should produce 4 houses')), 5,
           'The answer and the rule it follows: produce where marginal cost equals marginal '
           'revenue.')],
    '', tariff_kind='fixed',
    stem='The figures below represent the costs of building an average 3-bedroom '
         'semi-detached house in rural Ireland.',
    figure_key='economics-2022-HL-paper-p27-i0',
    label_key=[{'letter': 'A', 'meaning': 'total cost at one unit — 360,000',
                'askedInThisQuestion': False},
               {'letter': 'B', 'meaning': 'average total cost at two units — 200,000',
                'askedInThisQuestion': False},
               {'letter': 'C', 'meaning': 'marginal cost of the third unit — 50,000',
                'askedInThisQuestion': False}]))

# ── Tick tables, answered by the scheme's own completed table ──────────────
# See econ_tick_crop.py: the ✔ is drawn, so extraction keeps the tick and loses
# the column. The completed table is bound as a SOLUTION crop.

P.cards.append(card(
    'econ-2022-hl-q14-a-ii-ticks', 2022, 'higher', 'economics-1-5',
    'fixed-and-variable-building-costs', '2022 HL Q14(a)(ii)',
    'Choose by means of a tick (\u2713) which type of cost best describes each of the '
    'following. Explain your choice: bags of cement; carpenters (labour); purchase price of a '
    'construction site.',
    '(2+4)+(2+4)+(2+4)', 18,
    [point('r-1', as_option(block(BODY, 'Building Expense Fixed', '26 | P a g e')), 18,
           'Read the completed table below. Cement and carpenters are VARIABLE \u2014 build more '
           'houses and you need more of both. The site is FIXED: it costs the same whether it '
           'holds one house or a hundred. Each row is priced \u27e82+4\u27e9, two for the tick '
           'and four for the explanation, so the reasoning carries twice the marks of the choice. '
           'Note the scheme itself allows labour as a FIXED cost if it is on a fixed-price '
           'contract.')],
    'The carpenters row is the interesting one: the scheme concedes that labour can be fixed if '
    'contracted at a set price, so the classification follows the contract, not the input.',
    tariff_kind='fixed',
    figure_key='economics-2022-HL-scheme-p27-q14aii-ticks'))

# ── Backfill: asks the scheme answers in full ──────────────────────────────
# Excluded under labels describing the ANSWER rather than any blocker. Tariff
# and response are printed for each; catalogued crops ride where the figures
# come off printed artwork.

P.cards.append(card(
    'econ-2022-hl-q12-a-i', 2022, 'higher', 'economics-2-0',
    'what-a-falling-hhi-shows', '2022 HL Q12(a)(i)',
    'Comment on what the Herfindahl-Hirschman Index (HHI) results outlined above indicate about '
    'the market concentration in this industry over this time period.',
    '9', 9,
    [point('r-1', as_option(block(BODY, 'By 2019 the concentration has decreased to 3,328',
                                  '(ii)')), 9,
           'Two moves at once, and the scheme wants both: concentration FELL as firms entered, '
           'AND it is still above 2,500, so the market remains highly concentrated. A comment '
           'that reports only the fall has described the direction and missed the level.')],
    'A falling HHI is not the same as a competitive market. At 3,328 the top three firms still '
    'hold over 80%, so the industry has become less concentrated while staying concentrated.',
    tariff_kind='fixed',
    figure_key='economics-2022-HL-paper-p18-art'))

P.cards.append(card(
    'econ-2022-hl-q15-c-i', 2022, 'higher', 'economics-4-2',
    'the-eus-largest-contributor-and-beneficiary', '2022 HL Q15(c)(i)',
    'Using the data in the graph above, name the country which is the EU\u2019s largest '
    'contributor and which country is the EU\u2019s largest beneficiary.',
    '1 @ 4+1 @ 3', 7,
    [anyN('r-1', 'The two countries \u2014 both', None, 2, 4,
          [as_option(block(BODY, 'Largest EU Contributor: GERMANY', 'Largest EU Beneficiary')),
           as_option(block(BODY, 'Largest EU Beneficiary: POLAND', '(ii) Justify why countries'))],
          'Both are read straight off the net-benefit bars, and the scheme prices them unevenly '
          '\u2014 4 for the first and 3 for the second.',
          steps=[4, 3])],
    'The chart plots NET position, so the largest contributor is the deepest negative bar and '
    'the largest beneficiary the tallest positive one. Reading it as gross payments reverses the '
    'answer. The crop was catalogued under Q16(c)(i), which the paper shows is the fast-fashion '
    'minimum-pricing question; the manifest ref has been corrected to this part.',
    tariff_kind='fixed',
    figure_key='economics-2022-HL-paper-p33-art'))

P.emit()
