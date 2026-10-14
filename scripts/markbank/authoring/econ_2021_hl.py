#!/usr/bin/env python3
"""Economics 2021 Higher Level, Sections A and B.

Authored from the independent census in drafts/economics-2021-hl-ev.json, made
from a visual sweep of all 40 paper pages and 40 scheme pages. Every card ID the
earlier extractors shipped is kept (student progress follows the ID). The census
differs from the shipped deck in two consolidations: Q12(a)(ii) prints
2 @ 8 (5 + 3) and 2 @ 5 (2 + 3) beside the one ask for two positive AND two
negative impacts, and Q16(b)(ii) prints one 10 (2 @ 5) cell for one social AND
one economic reason, so each is one card and the second card resolves by alias.
Q11(a)(ii), Q11(b)(ii) and Q15(a) now carry the marks printed for the answer as
well as the explanation, and every menu carries the scheme's full list.

Question wording and stems are sliced from the question paper; every marking
point is sliced from the scheme (econ_2026_lib.py). This scheme sets most
responses as bold headings over a paragraph, so menus are split where each
heading begins; its bullet lists are split at the bullets. The only prose written
here is guidance: tariffs, route labels and what a figure or a calculation shows.
Scheme PDF page = printed page + 1.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from econ_2026_lib import Deck, Sheet, show_before_reveal  # noqa: E402
from econ_lib import anyN, as_option, bullets, defurnish, emit, heads, point  # noqa: E402

H = Sheet(2021, 'higher', 'LC034ALP000EV')
D = Deck(2021, 'higher')
cards, add, pick, heading, ref = D.cards, D.add, D.pick, D.heading, D.ref
A = dict(section='A')
SOL = 'economics-2021-HL-scheme-'
PAP = 'economics-2021-HL-paper-'
EITHER = 'Answer either (b) or (c).'
# A separator the scheme prints between alternatives, or the number of the next
# list item, left at the end of an option when the list is split.
TAIL = re.compile(r'(?:\s+(?:OR|or|\d\.)|\s*•)\s*$')


def clean(options):
    return [TAIL.sub('', o).strip() for o in options]


def bl(start, end, occ=None):
    """The scheme's bullet-listed responses between two anchors."""
    return clean(bullets(H.chunk(start, end, occ)))


def at(start, end, firsts, occ=None):
    """Responses printed as headed paragraphs, split where each one begins."""
    return clean([as_option(o) for o in heads(H.chunk(start, end, occ), firsts)])


def cell(start, upto=None):
    """One line of the scheme file that opens with `start`, its tick removed. With
    `upto`, the first line that runs as far as `upto`, cut there (the recovered
    table cells keep a cell on one line where the primary extraction splits it)."""
    hits = [ln.strip() for ln in H.full_md.splitlines() if ln.strip().startswith(start)]
    if upto:
        hits = [h[:h.index(upto) + len(upto)] for h in hits if upto in h]
    if not hits:
        raise ValueError(f'no scheme line opens with {start!r}')
    return defurnish(hits[0].replace('✔', ''))


def lifted(text):
    """A rendering the provenance gate reads from the scheme file's appended
    blocks (a fraction set on one line), checked here so a typo cannot ship."""
    if text not in H.full_md:
        raise ValueError(f'not in the scheme file: {text!r}')
    return text


def paras(options):
    """A list of the scheme's examples printed as one marking point."""
    return '\n\n'.join(options)


# ═════════════════════════════════ SECTION A ══════════════════════════════════

# Q1 ─ the balance of trade
q1_fig = PAP + 'p03-i0'
add('seca-q1-a', '4-2', 'calculating-the-balance-of-trade', ref(1, '(a)', sa=True),
    H.ask(3, 'Calculate the balance of trade for the period', ' Ireland'), '7', 7,
    [point('r-1', H.run('Total Exports: 112+119+123+141+152=647', '(b) Outline two reasons'), 7,
           'Add each line across the five years, then subtract: exports €647m less imports €410m is a '
           'surplus of €237m. The calculation and the surplus are worth 7 marks together.')],
    figure=q1_fig, **A)
pick('sa-q1-b', '4-2', 'why-a-trade-surplus-is-an-aim', ref(1, '(b)', sa=True),
     H.ask(3, 'Outline two reasons why achieving a trade surplus', ' 1. 2.'),
     'A reason a trade surplus is an aim — any two',
     at('Increased employment\nIf there is an increase', '2. Select, using a tick',
        ['Increased employment', 'Injection into Circular Flow', 'Imports are a leakage']),
     2, 4, 'Two reasons, 4 marks each.', **A)

# Q2 ─ positive and normative statements
add('sa-q2', '0-0', 'sorting-positive-from-normative-statements', ref(2, sa=True),
    H.ask(4, 'Select, using a tick', ' Statement Positive'), '4 + 4, 4 + 3', 15,
    [point('r-jobseeker', 'Positive — ' + cell('If the Irish government increase jobseeker', 'by 2023.'), None,
           'POSITIVE: a prediction that evidence could test, whether or not it comes true.'),
     point('r-less-well-off', 'Normative — ' + cell('We have to do more for the less well off', 'in society.'), None,
           'NORMATIVE: “have to” says what ought to happen.'),
     point('r-benefit', 'Normative — ' + cell('The government should have increased unemployment', 'this year.'), None,
           'NORMATIVE: “should” is a value judgement.'),
     point('r-cars', 'Positive — ' + cell('Sales of new cars in Ireland decreased during 2020.'), None,
           'POSITIVE: a statement of fact that the figures can check. The scheme prices the four ticks '
           'together as 4 + 4, 4 + 3 without naming which row earns which; the completed table is shown '
           'in the figure.')],
    kind='questionTotal', figure=SOL + 'p04-q2-ticks', **A)

# Q3 ─ Netflix and price discrimination
q3_stem = H.ask(4, 'The table below shows the subscription price', ' Netlfix')
q3_fig = PAP + 'p04-q3-chart'
pick('sa-q3-a', '2-0', 'why-consumers-accept-different-prices', ref(3, '(a)', sa=True),
     H.ask(4, 'Outline one reason why consumers are willing to pay', ' Answer:'),
     'A reason consumers accept price discrimination — any one',
     at('Consumer ignorance:', '(b) Other than your answer',
        ['Consumer ignorance:', 'Consumer indifference:', 'Consumer attitudes:']),
     1, 5, 'One reason, 5 marks (2 + 3).', stem=q3_stem, figure=q3_fig, **A)
pick('sa-q3-b', '2-0', 'conditions-for-price-discrimination-hl', ref(3, '(b)', sa=True),
     H.ask(5, 'Other than your answer given in part (a)', ' 1. 2.'),
     'A condition for price discrimination — any two',
     at('Monopoly power\nThe firm must have', '4 | P a g e',
        ['Monopoly power', 'Different price elasticities', 'Market separation']),
     2, 5, 'Two conditions, 5 marks each (2 + 3).', stem=q3_stem, figure=q3_fig, **A)

# Q4 ─ demerit goods
q4_stem = H.ask(5, 'In budget 2021, the price of a 20 pack', ' (a)')
add('sa-q4-a', '2-2', 'demerit-goods', ref(4, '(a)', sa=True),
    H.ask(5, 'Explain your understanding of the economic term', ' Leaving'), '4 + 3', 7,
    [point('r-1', H.run('Demerit goods are goods whose positive effect', 'Answer part (b) or (c)'), 7,
           'Explain the term, 7 marks (4 + 3): a good whose benefit consumers overestimate and whose '
           'harm they underestimate, and which usually carries negative externalities.')],
    stem=q4_stem, **A)
add('sa-q4-b', '2-2', 'cigarettes-and-market-failure', ref(4, '(b)', sa=True),
    H.ask(6, 'Explain why the purchase of demerit goods', ' OR'), '4 + 4', 8,
    [point('r-1', H.run('The purchase of demerit goods is seen as a market failure', 'OR\n(c) Explain'), 8,
           'Explain, 8 marks (4 + 4): the free market over-produces and over-consumes the good, and its '
           'price fails to reflect the true private and social cost.')],
    stem=q4_stem, notes=EITHER, **A)
add('sa-q4-c', '2-2', 'taxing-demerit-goods', ref(4, '(c)', sa=True),
    H.ask(6, 'Explain why the Irish Government intervenes', ' Leaving'), '4 + 4', 8,
    [point('r-1', H.run('The government intervenes in order to increase the price', '5 | P a g e'), 8,
           'Explain, 8 marks (4 + 4): the tax raises the price to deter consumption and funds the cost of '
           'the externalities; left to the market, the price would be too low.')],
    stem=q4_stem, notes=EITHER, **A)

# Q5 ─ the Central Bank of Ireland
add('sa-q5-a', '3-4', 'why-bank-regulation-protects-consumers', ref(5, '(a)', sa=True),
    H.ask(7, 'Based upon the above statement outline why', ' (b)'), '7', 7,
    [point('r-1', H.run('Protection of consumer of financial services', '(b) Other than regulation'), 7,
           'One reason, 7 marks: banks that are not properly regulated may operate outside the guidelines '
           'and exploit consumers.')],
    stem=H.ask(7, 'KBC Bank Ireland was fined', ' Adapted from'), **A)
pick('sa-q5-b', '3-4', 'duties-of-the-central-bank', ref(5, '(b)', sa=True),
     H.ask(7, 'Other than the regulation of commercial banks', ' 1. 2.'),
     'A duty of the Central Bank — any two',
     at('Eurosystem effectiveness and price stability', '6 | P a g e',
        ['Eurosystem effectiveness', 'Stability of the financial', 'Efficient and effective payment',
         'Independent economics advice', 'Recovery and resolution', 'Banker to the Government']),
     2, 4, 'Two duties, 4 marks each. Regulating the commercial banks is excluded by the question.', **A)

# Q6 ─ the Human Development Index
add('sa-q6-a', '4-0', 'hdi-versus-gdp', ref(6, '(a)', sa=True),
    H.ask(8, 'Explain why the Human Development Index', ' Answer (b)'), '4 + 3', 7,
    [point('r-1', H.run('The HDI is a more accurate indicator of human welfare', 'Answer question (b) or (c)'), 7,
           'Explain, 7 marks (4 + 3): the HDI combines income per person, education and life expectancy, '
           'where GDP reflects the level of economic activity alone.')],
    **A)
q6_stem = H.ask(8, 'The data below has been extracted from the HDI 2020.', ' Rank')
q6_fig = PAP + 'p08-i0'
pick('sa-q6-b', '4-0', 'policies-to-raise-a-countrys-hdi', ref(6, '(b)', sa=True),
     H.ask(8, 'Using the data provided above, advise the governments', ' Leaving'),
     'A policy to improve the HDI ranking — any one',
     at('Improve education in the country', 'OR\n7 | P a g e',
        ['Improve education', 'Improve national healthcare', 'Improve distribution of income',
         'Reduce corruption']),
     1, 8, 'One policy, 8 marks (4 + 4).', stem=q6_stem, figure=q6_fig, notes=EITHER, **A)
pick('sa-q6-c', '4-0', 'how-a-rich-country-can-assist-ldcs', ref(6, '(c)', sa=True),
     H.ask(9, 'Advise the Irish government on how it could assist', ' Leaving'),
     'A way the Irish government could assist — any one',
     at('Direct financial aid by the government', '7. (a) Compare the level',
        ['Direct financial aid', 'Assist with skills', 'Help restructuring', 'Help improve the terms']),
     1, 8, 'One way, 8 marks (4 + 4).', stem=q6_stem, figure=q6_fig, notes=EITHER, **A)

# Q7 ─ government finance
add('seca-q7-a', '3-1', 'gross-debt-per-person-2007-to-2019', ref(7, '(a)', sa=True),
    H.ask(10, 'Compare the level of Gross Debt per Person', ' Answer (b)'), '5 + 4', 9,
    [heading('r-comparison', 'A comparison of gross debt per person — any one',
             [cell('Between 2007 and 2019 the gross debt'), cell('Between 2007 and 2013 the gross debt'),
              cell('Between 2013 and 2019 the gross debt')], 5,
             'The comparison, 5 marks: any one of the scheme’s three comparisons, with its figures.'),
     point('r-reason', H.run('Between 2007 and 2013 the Irish economy fell into recession', '8 | P a g e'), 4,
           'The reason for the increase, 4 marks: the recession, the housing bubble and the bank bail-outs.')],
    stem=H.ask(10, 'The diagram below shows Government Finance Statistics', ' Adapted from'),
    figure=PAP + 'p10-art', **A)
pick('sa-q7-b', '3-1', 'disadvantages-of-a-budget-surplus', ref(7, '(b)', sa=True),
     H.ask(10, 'Explain the economic disadvantages for a government', ' Leaving'),
     'A disadvantage of a budget surplus — any two',
     at('Rise in conflicting expectations', 'OR\n(c) Servicing the national debt',
        ['Rise in conflicting expectations', 'Public Sector Workers', 'Tax burden',
         'Government financial planning', 'Opportunity costs of a surplus', 'Difficulties in the Social']),
     2, 3, 'Two disadvantages, 3 marks each.', notes=EITHER, **A)
add('sa-q7-c', '3-1', 'national-debt-and-opportunity-cost', ref(7, '(c)', sa=True),
    H.ask(11, 'Servicing the national debt creates opportunity costs', ' Leaving'), '6', 6,
    [point('r-1', H.run('Servicing the national debt involves using up scarce resources', '9 | P a g e'), 6,
           'Explain, 6 marks: the resources used to service the debt could have gone to other uses, such '
           'as the health services.')],
    notes=EITHER, **A)

# Q8 ─ the equi-marginal principle
q8_stem = H.ask(12, 'John always spends his income', ': ', include_end=True)
q8_fig = PAP + 'p12-q8-ratios'
add('seca-q8-a', '1-1', 'price-from-the-equi-marginal-principle', ref(8, '(a)', sa=True),
    H.ask(12, 'Calculate the price John would be willing to pay', ' Workings:'), '7', 7,
    [point('r-1', H.run('2500 ÷ 200 = 12.5', '(b) Explain why John'), 7,
           'Find the common ratio first: 2500 ÷ 200 = 12.5 (or 1250 ÷ 100 = 12.5). Good Z must give the '
           'same marginal utility per euro, so its price is 75 ÷ 12.5 = €6. The calculation is worth 7 '
           'marks.')],
    stem=q8_stem, figure=q8_fig, **A)
add('seca-q8-b', '1-1', 'why-the-equi-marginal-price-is-paid', ref(8, '(b)', sa=True),
    H.ask(12, 'Explain why John would pay this price.', ' Leaving'), '2 @ 4', 8,
    [point('r-1', H.run('He would pay this price in order to maximise his utility', '9. (a) What is'), 8,
           'Explain, 8 marks (2 @ 4): he maximises his utility by spending in line with the equi-marginal '
           'principle, the ratio of marginal utility to price being the same for every good.')],
    stem=q8_stem, figure=q8_fig, **A)

# Q9 ─ market structures
q9_fig = PAP + 'p13-i0'
add('seca-q9-a', '2-0', 'naming-the-market-structure', ref(9, '(a)', sa=True),
    H.ask(13, 'Identify the corresponding market structure', ' Product / Firm'), '3 @ 3', 9,
    [point('r-banking', cell('A The Irish banking sector'), 3, 'A, the banking sector: OLIGOPOLY.'),
     point('r-water', cell('B Irish Water (the company)'), 3, 'B, Irish Water: MONOPOLY.'),
     point('r-takeaway', cell('C A takeaway food outlet'), 3, 'C, a takeaway: MONOPOLISTIC COMPETITION.')],
    figure=q9_fig, **A)
add('seca-q9-b', '2-0', 'reasons-for-each-market-structure', ref(9, '(b)', sa=True),
    H.ask(13, 'Give one reason for each of your chosen', ' A. B. C.'), '6', 6,
    [point(f'r-{k}', o, None, n) for k, o, n in zip(
        ['banking', 'water', 'takeaway'],
        bl('• The Irish banking sector is dominated', '10 | P a g e'),
        ['The banking sector: a few large firms dominate.', 'Irish Water: one firm supplies the market.',
         'A takeaway: many firms selling close substitutes, each setting its own price. The scheme gives 6 '
         'for the three reasons, with no published split.'])],
    kind='questionTotal', figure=q9_fig, **A)

# Q10 ─ the ECB rate
q10_stem = H.ask(14, 'The graph below shows the fluctuation', ' European Central Bank Fixed Rate May')
q10_fig = PAP + 'p14-art'
add('sa-q10-a', '3-3', 'why-ecb-rates-fell-to-zero', ref(10, '(a)', sa=True),
    H.ask(14, 'Explain the historical reason for this trend', ' (b)'), '8', 8,
    [point('r-1', H.run('In the wake of the great recession in 2008', '(b) Outline whether you would'), 8,
           'One explanation, 8 marks: the post-2008 credit crunch, and the cuts made to cheapen borrowing '
           'and encourage investment and growth.')],
    stem=q10_stem, figure=q10_fig, **A)
pick('sa-q10-b', '3-3', 'what-you-would-advise-the-ecb-to-do-with-a-zero-rate', ref(10, '(b)', sa=True),
     H.ask(14, 'Outline whether you would advise the European Central Bank', ' Answer:'),
     'A recommendation for the ECB with its justification — either one',
     bl('• During these economically volatile times', '11 | P a g e'),
     1, 7, 'One justified recommendation, 7 marks. The scheme credits MAINTAIN or DECREASE (including a '
           'negative rate); it prints no case for an increase.',
     stem=q10_stem, figure=q10_fig, **A)


# ═════════════════════════════════ SECTION B ══════════════════════════════════

# Q11 ─ the global aircraft market
q11a_stem = H.ask(15, 'The pie chart below shows the market share', ' Global Aircraft Market 2018')
q11a_fig = PAP + 'p15-i0'
add('q11-a-i', '2-0', 'calculating-the-hhi-for-the-aircraft-market', ref(11, '(a)(i)'),
    H.ask(15, 'Using the data provided above, calculate the Herfindahl', ' Workings:'), '7', 7,
    [point('r-1', '4262', 7,
           'Square each market share and add: 46² + 46² + 5² + 2² + 1² = 4,262. Squaring is what turns '
           'shares into concentration. The calculation is worth 7 marks.')],
    stem=q11a_stem, figure=q11a_fig)
add('q11-a-ii', '2-0', 'reading-a-concentration-ratio', ref(11, '(a)(ii)'),
    H.ask(16, 'Would you consider this market to be competitive', ' Answer:'), '3 + 5', 8,
    [point('r-answer', 'Highly concentrated', 3, 'The answer, 3 marks: the HHI of 4,262 is above 2,500.'),
     heading('r-explanation', 'Why it is highly concentrated — any one',
             bl('• The HHI is greater than 2500.', '(b) (i) Write in full'), 5, 'The explanation, 5 marks.')],
    stem=q11a_stem, figure=q11a_fig)
q11b_stem = H.ask(16, 'The diagram below represents the long', ' 1 P')
q11b_fig = PAP + 'p16-i0'
add('q11-b-i', '2-0', 'labelling-an-oligopoly-diagram', ref(11, '(b)(i)'),
    H.ask(16, 'Write in full the label', ' Number'), '16', 16,
    [point(f'r-{i}', cell(f'{i}. {label}'), None, note) for i, label, note in [
        (1, 'Marginal Cost', 'Line 1.'), (2, 'Average (Total) Cost', 'Line 2.'),
        (3, 'Demand / Average Revenue', 'Line 3.'),
        (4, 'Marginal Revenue', 'Line 4. The scheme gives 16 for the four labels, with no published split; '
                                'abbreviations are not accepted.')]],
    kind='questionTotal', stem=q11b_stem, figure=q11b_fig)
add('q11-b-ii', '2-0', 'price-competition-in-oligopoly', ref(11, '(b)(ii)'),
    H.ask(17, 'Would you advise the above firm to engage in price competition?', ' 1. 2.'), '2 + 2 @ 4', 10,
    [point('r-answer', 'No', 2, 'The answer, 2 marks: every reason the scheme lists argues against price '
                                'competition.'),
     anyN('r-reasons', 'A reason not to engage in price competition — any two', 8, 2, 4,
          bl('• Fear of a price wars by their rivals', '12 | P a g e'), 'Two reasons, 4 marks each.')],
    stem=q11b_stem, figure=q11b_fig)
pick('q11-b-iii', '2-0', 'small-firms-in-an-oligopoly', ref(11, '(b)(iii)'),
     H.ask(17, 'Outline two reasons why small firms such as Embraer', ' 1. 2.'),
     'A reason a small firm may survive — any two',
     at('Personalised / exclusive nature', '13 | P a g e',
        ['Personalised / exclusive', 'Consumer loyalty', 'A niche market', 'Small size of market']),
     2, 4, 'Two reasons, 4 marks each.', stem=q11a_stem, figure=q11a_fig)
q11c_stem = H.ask(18, 'Boeing and Embraer entered potential merger talks', ' (i)')
add('q11-c-i', '1-5', 'what-internal-economies-of-scale-are', ref(11, '(c)(i)'),
    H.ask(18, 'Define Internal Economies of Scale.', ' (ii)'), '8', 8,
    [point('r-1', H.run('Internal economies of scale refer to the decreases', '(ii) Outline possible'), 8,
           'Define the term, 8 marks: average total cost falls as the firm’s own scale of production grows.')],
    stem=q11c_stem)
pick('q11-c-ii', '1-5', 'internal-economies-of-scale', ref(11, '(c)(ii)'),
     H.ask(18, 'Outline possible Internal Economies of Scale', ' 75 marks'),
     'An internal economy of scale from the merger — any three',
     at('Labour economies:', '14 | P a g e',
        ['Labour economies:', 'Managerial economies:', 'Purchasing economies', 'Technical economies',
         'Economies in use of raw materials', 'Economies in distribution', 'Marketing economies',
         'Financial economies']),
     3, 6, 'Three economies, 6 marks each (2 + 4).', stem=q11c_stem)

# Q12 ─ globalisation; corporation tax; Brexit
pick('q12-a-i', '4-1', 'what-globalisation-is', ref(12, '(a)(i)'),
     H.ask(19, 'Explain the term globalisation.', ' (ii)'),
     'What globalisation means — any one wording',
     at('Globalisation is the process by which', '(ii) Outline two positive',
        ['Globalisation is the process', 'The term globalisation is', 'Globalisation is ability']),
     1, 4, 'Explain the term, 4 marks; the scheme prints three alternative wordings.')
q12_positive = at('Trade enhances division of labour', 'Negative impacts of globalisation\nInequality',
                  ['Trade enhances division', 'Improvements in economic growth', 'Reduction in numbers',
                   'Innovation is encouraged', 'Benefits of economies of scale'])
q12_negative = at('Inequality\nGlobalisation has been linked', '16 | P a g e',
                  ['Inequality', 'Re-location of jobs', 'Increases in world food prices', 'Dominant Global Brands',
                   'Threat to the environment', 'Trade Imbalances', 'Macroeconomic Instability',
                   'Standardisation of commodities'])
add('q12-a-ii-pos', '4-1', 'positive-and-negative-impacts-of-globalisation', ref(12, '(a)(ii)'),
    H.ask(19, 'Outline two positive impacts and two negative impacts', ' Positive:'), '2 @ 8, 2 @ 5', 26,
    [anyN('r-1', 'An impact of globalisation — two positive and two negative', None, 4, 8,
          q12_positive + q12_negative,
          'Four impacts, two of each kind. The scheme prints 2 @ 8 (5 + 3) and 2 @ 5 (2 + 3) beside the one '
          'ask without tying either price to a side, so the best two impacts take 8 each and the other two '
          '5. The first five are the scheme’s positive impacts and the last eight its negative.',
          steps=[8, 8, 5, 5])])
q12b_stem = H.ask(20, 'In Budget 2020, the Minister for Finance reaffirmed', ' (i)')
pick('q12-b-i', '3-1', 'reasons-for-the-125-corporation-tax-rate', ref(12, '(b)(i)'),
     H.ask(20, 'Evaluate two reasons why the Minister for Finance', ' 1. 2.'),
     'A reason for keeping the 12.5% rate — any two',
     at('Incentivise FDI / discourage', '17 | P a g e',
        ['Incentivise FDI', 'Maintain employment levels', 'Government revenue', 'Maintain economic growth',
         'Loss of fiscal sovereignty']),
     2, 7, 'Two reasons, 7 marks each (3 + 4).', stem=q12b_stem)
pick('q12-b-ii', '4-2', 'why-brussels-wants-tax-harmony', ref(12, '(b)(ii)'),
     H.ask(20, 'The Irish government has repeatedly rejected', ' Leaving'),
     'A reason the European Commission wants this power removed — any one',
     at('Streamlining of all European policies', '18 | P a g e',
        ['Streamlining of all European', 'Greater transparency', 'Seen as anti-competitive']),
     1, 7, 'One reason, 7 marks (3 + 4).', stem=q12b_stem)
q12c_stem = H.ask(21, 'The United Kingdom exited the European Union', ' (i)')
pick('q12-c-i', '4-2', 'implications-of-brexit-for-ireland', ref(12, '(c)(i)'),
     H.ask(21, 'Discuss two implications of this exit', ' 1. 2.'),
     'An implication of Brexit for the Irish economy — any two',
     at('Possible negative effect on Irish exports', '19 | P a g e',
        ['Possible negative effect', 'Effects on agricultural sector', 'Labour market effects',
         'Imports from the UK']),
     2, 6, 'Two implications, 6 marks each (3 + 3).', stem=q12c_stem)
pick('q12-c-ii', '4-1', 'advantages-of-eu-membership', ref(12, '(c)(ii)'),
     H.ask(21, 'Outline two possible advantages to Ireland of remaining', ' 1. 2.'),
     'An advantage of remaining in the EU — any two',
     at('Free Trade Area / larger market', '20 | P a g e',
        ['Free Trade Area', 'Access to capital', 'Freedom movement', 'Foreign Direct Investment',
         'EU legislation and policies', 'Supports the Peace Process']),
     2, 6, 'Two advantages, 6 marks each (3 + 3).', stem=q12c_stem)

# Q13 ─ the PS5 shortage; misinformation; elasticity
q13a_stem = H.ask(22, 'Shortages of the PlayStation 5', ' Adapted from')
q13a_sol = SOL + 'p22-q13ai-diagram'
add('q13-a-i', '1-0', 'excess-demand-diagram-labels', ref(13, '(a)(i)'),
    H.ask(22, 'Complete the diagram below to indicate how excess demand', ' (ii)'), '8 @ 1', 8,
    [anyN('r-1', 'A correctly labelled point on the diagram — all eight', 8, 8, 1,
          ['Price', 'Quantity', 'QE', 'QX', 'D1', 'S1', 'P = €500', 'Excess Demand from QE to QX'],
          'One mark for each correctly labelled point: the two axes, the two quantities, the two curves, '
          'the price of €500 and the excess demand from QE to QX. The completed diagram is shown in the '
          'figure.')],
    stem=q13a_stem, figure=q13a_sol)
add('q13-a-ii', '1-0', 'how-excess-demand-occurs', ref(13, '(a)(ii)'),
    H.ask(22, 'From your diagram above, explain how excess demand occurs.', ' Leaving'), '3 @ 4', 12,
    [point('r-shortage', H.run('At the price of €500 there is more demand', 'This indicates that the price'), 4,
           'At €500, quantity demanded (QX) exceeds the fixed supply (QE), 4 marks.'),
     point('r-pressure', H.run('This indicates that the price charged', 'By undercharging for the PS5'), 4,
           'The price is too low: the excess demand pushes it up towards the equilibrium P1, 4 marks.'),
     point('r-undercharging', H.run('By undercharging for the PS5', '21 | P a g e'), 4,
           'Undercharging created the extra demand, which a higher price would ration, 4 marks.')],
    stem=q13a_stem, figure=q13a_sol)
q13b_stem = H.ask(23, 'Technology retailers mislead shoppers', ' Adapted from')
pick('q13-b-i', '2-2', 'information-failure-as-market-failure', ref(13, '(b)(i)'),
     H.ask(23, 'Explain why misinformation to consumers', ' (ii)'),
     'Why the misinformation is a market failure — any two',
     bl('• Information failure is a form of market failure', 'Note\nMarket failure occurs'),
     2, 5, 'Two points, 5 marks each (2 + 3). The scheme adds a note: “'
           + H.run('Market failure occurs when the price mechanism', '(ii) Evaluate how Government') + '”',
     stem=q13b_stem)
pick('q13-b-ii', '2-2', 'fixing-information-failure', ref(13, '(b)(ii)'),
     H.ask(23, 'Evaluate how Government intervention in this market', ' (iii)'),
     'A form of government intervention — any one',
     at('Increased public awareness', '22 | P a g e',
        ['Increased public awareness', 'Government legislation', 'Increased penalties',
         'Increased accuracy of information']),
     1, 6, 'One developed intervention, 6 marks (3 + 3).', stem=q13b_stem)
pick('q13-b-iii', '1-3', 'advantages-of-regulation', ref(13, '(b)(iii)'),
     H.ask(23, 'Explain, giving an example, one advantage', ' Leaving'),
     'An advantage of government regulation — any one',
     at('Health and safety regulations', '(c) (i) Apple Airpods',
        ['Health and safety regulations', 'Protects consumers from exploitation', 'Prevent anti-competitive',
         'Increases competition', 'Environmental protection', 'Employment Laws']),
     1, 6, 'One advantage with an example, 6 marks (2 @ 3).')
q13c_ask = H.ask(24, 'Apple AirPods (earphones) price fell', ' Calculate')
add('q13-c-i', '1-4', 'ped-of-apple-airpods', ref(13, '(c)(i)'),
    q13c_ask + ' ' + H.ask(24, 'Calculate the Price Elasticity of Demand', ' Workings:'), '15', 15,
    [point('r-1', lifted('+5000/−35 × 160 + 125 (285)/10,000 + 15,000 (25,000) = −1.63'), 15,
           'PED = (ΔQ ÷ ΔP) × ((P1 + P2) ÷ (Q1 + Q2)) = (+5,000 ÷ −35) × (285 ÷ 25,000) = −1.63. Keep the '
           'minus sign: price and quantity moved in opposite directions. The calculation is worth 15 marks; '
           'the official working is shown in the figure.')],
    figure=SOL + 'p24-q13ci-working')
add('q13-c-ii', '1-4', 'reading-a-ped-figure', ref(13, '(c)(ii)'),
    H.ask(24, 'Based on the figure you have calculated', ' Answer:'), '4 + 4', 8,
    [point('r-answer', H.run('Based upon the above calculation Apple Airpods', '• The number is greater'), 4,
           'ELASTIC, 4 marks: the PED from (i) is −1.63.'),
     heading('r-reason', 'The reason — either one', bl('• The number is greater than 1', '(iii) If the firm'), 4,
             'The reason, 4 marks: the size of the number, or what it says about the two percentage '
             'changes.')],
    stem=q13c_ask)
add('q13-c-iii', '1-4', 'elasticity-and-revenue', ref(13, '(c)(iii)'),
    H.ask(25, 'If a firm selling the above product intends', ' Answer:'), '10', 10,
    [point('r-answer', H.run('As the price elasticity of demand is elastic the firm', 'A decrease in price will lead'),
           None, 'DECREASE the price: demand is elastic.'),
     point('r-explanation', H.run('A decrease in price will lead to a more than proportionate', '23 | P a g e'),
           None, 'Explain: the quantity demanded rises by proportionately more than the price falls, so '
                 'total revenue rises. The scheme gives one 10 for the answer and its explanation, with no '
                 'published split.')],
    kind='questionTotal', stem=q13c_ask)

# Q14 ─ inflation; competitiveness
q14_stem = H.ask(26, 'The graph below shows the Harmonised Indices', ' HICP average')
q14_fig = PAP + 'p26-art'
add('q14-a-i', '3-3', 'irelands-inflation-against-the-uk-and-euro-area', ref(14, '(a)(i)'),
    H.ask(26, 'Analyse the trend of Ireland’s inflation rate', ' Leaving'), '1 @ 6, 2 @ 3', 12,
    [anyN('r-1', 'A trend read off the chart — any three', None, 3, 6,
          bl('• Across the entire time Ireland’s inflation rate', '(ii) Outline the potential'),
          'Three trends: the first correct one 6 marks and the next two 3 each. Analyse Ireland IN RELATION '
          'to the UK and the Euro Area.', steps=[6, 3, 3])],
    stem=q14_stem, figure=q14_fig)
pick('q14-a-ii', '3-3', 'advantages-of-low-inflation', ref(14, '(a)(ii)'),
     H.ask(27, 'Outline the potential advantages to Ireland', ' (b)'),
     'An advantage of the lowest inflation rate — any two',
     at('More competitive exports', '24 | P a g e',
        ['More competitive exports', 'Competitive costs', 'Domestic spending', 'Government finances']),
     2, 6, 'Two advantages, 6 marks each (3 + 3).', stem=q14_stem, figure=q14_fig)
pick('q14-b-i', '3-3', 'disadvantages-of-low-inflation', ref(14, '(b)(i)'),
     H.ask(27, 'Outline two possible disadvantages to Irish citizens', ' 1. 2.'),
     'A disadvantage of low inflation for Irish citizens — any two',
     at('Consumers may postpone spending', '(ii) Explain one method',
        ['Consumers may postpone', 'No / low wage increases', 'Debt burden effect', 'Asset appreciation']),
     2, 7, 'Two disadvantages, 7 marks each (3 + 4).')
pick('q14-b-ii', '3-3', 'government-tools-against-inflation', ref(14, '(b)(ii)'),
     H.ask(28, 'Explain one method the government could use', ' (c)'),
     'A method to address rising inflation — any one',
     at('Increase direct taxation', '25 | P a g e',
        ['Increase direct taxation', 'Decrease government current', 'Reduce cost of government']),
     1, 7, 'One method, 7 marks (3 + 4).')
add('q14-c-i', '4-2', 'the-principle-of-comparative-advantage', ref(14, '(c)(i)'),
    H.ask(28, 'Define the principle of comparative advantage.', ' (ii)'), '3 + 3', 6,
    [point('r-1', H.run('Comparative Advantage is the ability of a country', '(ii) Continued capital'), 6,
           'Define the principle, 6 marks (3 + 3): producing at a lower opportunity cost than another '
           'country, which drives specialisation.')])
pick('q14-c-ii', '4-2', 'broadband-and-competitiveness', ref(14, '(c)(ii)'),
     H.ask(28, 'Continued capital investment in the National Broadband Plan', ' Adapted from') + ' '
     + H.ask(28, 'Discuss the importance of this recommendation', ' Continued on'),
     'Why the broadband recommendation matters — any two',
     at('Ability to attract FDI', '26 | P a g e',
        ['Ability to attract FDI', 'More flexible working', 'Allow state provide', 'Reduce costs of running']),
     2, 6, 'Two points, 6 marks each (3 + 3).')
pick('q14-c-iii', '4-2', 'improving-international-competitiveness', ref(14, '(c)(iii)'),
     H.ask(29, 'Choose two other areas the Irish Government', ' 1. 2.'),
     'An area to focus on, with its justification — any two',
     at('Fund skills, education and training', '27 | P a g e',
        ['Fund skills', 'Improve the infrastructure', 'Manage the current housing', 'Supporting Enterprise',
         'Reduce utility charges', 'Encourage competition', 'Reduce taxation', 'Address climate action']),
     2, 6, 'Two areas, 6 marks each (3 + 3): the choice and its justification.')

# Q15 ─ GDP and GNI; recession; the multiplier
add('q15-a', '3-0', 'gni-or-gdp-for-welfare', ref(15, '(a)'),
    H.ask(30, 'Which measure is a more accurate indicator', ' Answer:'), '7 + 7 + 7', 21,
    [point('r-gni', H.run('Gross national income is a more accurate measure', 'Gross domestic product is a'), None,
           'GNI is the more accurate measure: it is the income received by Ireland’s permanent residents.'),
     point('r-gdp', H.run('Gross domestic product is a measure of the total', 'GNI:'), None,
           'Why GDP overstates Irish living standards: much of the income from production here accrues to '
           'foreign owners of capital.'),
     point('r-key', H.run('GNI:\nincome to permanent domestic residents', '(b) (i) Define the term'), None,
           'The scheme’s summary of the GNI case. It prices the answer 7 + 7 + 7 without naming which '
           'element earns which.')],
    kind='questionTotal')
add('q15-b-i', '3-0', 'what-a-recession-is', ref(15, '(b)(i)'),
    H.ask(31, 'Define the term recession.', ' (ii)'), '4 + 4', 8,
    [point('r-1', H.run('A recession refers to a period of negative economic growth', '(ii) Based upon the graph'),
           8, 'Define the term, 8 marks (4 + 4): negative economic growth, for at least two quarters.')])
add('q15-b-ii', '3-5', 'reading-a-recession-off-a-gni-chart', ref(15, '(b)(ii)'),
    H.ask(31, 'Based upon the graph below, identify the years', ' GNI Per'), '4 + 4', 8,
    [point('r-years', H.run('The period from 2007 to 2009 sees both', 'During this period, it can be seen'), 4,
           'The years, 4 marks: 2007 to 2009.'),
     point('r-explanation', H.run('During this period, it can be seen that the GNI', '28 | P a g e'), 4,
           'The explanation, 4 marks: GNI per capita falls for both countries, so both economies were '
           'shrinking.')],
    figure=PAP + 'p31-art')
pick('q15-b-iii-percap', '3-0', 'why-per-capita-comparisons-matter', ref(15, '(b)(iii)'),
     H.ask(32, 'With reference to GNI, why is it important', ' (c)'),
     'Why per capita measures matter — any one account',
     at('GNI per capita is a more useful measure', '(c) (i) Explain the term Multiplier',
        ['GNI per capita is a more useful', 'If GNI is compared on a nominal', 'Worked example:']),
     1, 8, 'One account, 8 marks (4 + 4); the scheme prints these three as alternatives.')
add('q15-c-i', '3-0', 'meaning-of-the-multiplier', ref(15, '(c)(i)'),
    H.ask(32, 'Explain the term multiplier.', ' (ii)'), '8', 8,
    [point('r-1', H.run('The multiplier effect means that any injection', '(ii) Assume that MPM'), 8,
           'Explain the term, 8 marks: an injection raises national income by more than itself.')])
add('q15-c-ii', '3-0', 'calculating-the-multiplier', ref(15, '(c)(ii)'),
    H.ask(32, 'Assume that MPM is 0.25', ' Workings:'), '8', 8,
    [point('r-1', 'Multiplier = 1.43', 8,
           'MPS = 1 − MPC = 1 − 0.65 = 0.35, then multiplier = 1 ÷ (MPS + MPM + MPT) = 1 ÷ (0.35 + 0.25 + '
           '0.10) = 1 ÷ 0.70 = 1.43. The calculation is worth 8 marks; the official working, written both '
           'ways, is shown in the figure.')],
    figure=SOL + 'p30-q15cii-working')
pick('q15-c-iii', '3-0', 'the-multiplier-in-reverse', ref(15, '(c)(iii)'),
     H.ask(33, 'Discuss two possible negative multiplier effects', ' 1. 2.'),
     'A negative multiplier effect — any two',
     at('Lost rents\nThe owners of the property', '30 | P a g e',
        ['Lost rents', 'Reduced demand for goods', 'Reduced demand for public transport',
         'Effect on government finances']),
     2, 7, 'Two effects, 7 marks each (3 + 4).')

# Q16 ─ air passengers; the minimum wage; homelessness
q16a_stem = H.ask(34, 'The diagram below shows the number of passengers', ' Number of')
q16a_fig = PAP + 'p34-art'
add('q16-a-i-trend', '3-2', 'trend-in-air-passenger-numbers', ref(16, '(a)(i)'),
    H.ask(34, 'Using the data provided above, analyse the trend', ' Analysis of'), '7', 7,
    [point('r-1', paras(bl('• Between Q2 2017 and Q2 2019', '(ii) The demand for labour')), 7,
           'One analysis, 7 marks: the steady rise to just over 10 million in Q2 2019, then the sharp '
           'decline to virtually zero in Q2 2020, with the figures.')],
    stem=q16a_stem, figure=q16a_fig)
add('q16-a-ii-derived', '2-1', 'derived-demand-for-labour', ref(16, '(a)(ii)'),
    H.ask(34, 'The demand for labour is said to be a derived demand.', ' Leaving'), '9', 9,
    [point('r-1', H.run('The demand for labour in the aviation sector', '(iii) Outline two negative'), 9,
           'Explain, 9 marks: the demand for aviation workers depends on the demand for flights; labour is '
           'demanded for what it produces.')],
    stem=q16a_stem, figure=q16a_fig)
pick('q15-b-iii', '3-2', 'effects-of-falling-air-passenger-numbers', ref(16, '(a)(iii)'),
     H.ask(35, 'Outline two negative implications of this reduction', ' 1. 2.'),
     'A negative implication for employment — any two',
     at('Decreased direct employment', '31 | P a g e',
        ['Decreased direct employment', 'Suppliers to the aviation', 'Reduction in aggregate demand']),
     2, 5, 'Two implications, 5 marks each (2 + 3).', stem=q16a_stem, figure=q16a_fig)
q16b_stem = H.ask(35, 'The graph below shows the national minimum wage', ' National Minimum')
q16b_fig = PAP + 'p35-i0'
add('q16-b-i', '2-1', 'percentage-increase-in-the-minimum-wage', ref(16, '(b)(i)'),
    H.ask(35, 'Calculate the percentage increase in the minimum wage', ' Workings:'), '9', 9,
    [heading('r-1', 'The percentage increase — either route',
             [lifted('10.20 −9.15 = 1.05/9.15 × 100 = 11.48%'), lifted('10.20/9.15 × 100 = 111.48 −100 = 11.48%')],
             9, 'The calculation, 9 marks: the rise of €1.05 over the 2016 rate of €9.15, or the ratio of the '
                'two rates less 100. Both routes divide by the 2016 rate.')],
    stem=q16b_stem, figure=q16b_fig)
add('q16-b-ii-social', '2-1', 'social-and-economic-case-for-the-minimum-wage', ref(16, '(b)(ii)'),
    H.ask(36, 'Explain one social reason and one economic reason', ' Social reason:'), '2 @ 5', 10,
    [heading('r-social', 'A social reason — any one',
             at('Introduce a more equitable distribution', 'Economic reasons:',
                ['Introduce a more equitable', 'Protection of the most vulnerable', 'Reduce problem of poverty']),
             5, 'One social reason, 5 marks (2 + 3).'),
     heading('r-economic', 'An economic reason — any one',
             at('Increase worker’s standard of living', '32 | P a g e',
                ['Increase worker’s standard', 'Increase the incentive to work', 'Boost economic growth']),
             5, 'One economic reason, 5 marks (2 + 3). The scheme prices the pair as one 10 (2 @ 5).')],
    stem=q16b_stem, figure=q16b_fig)
q16c_stem = H.ask(36, 'The number of homeless families', ' Adapted from')
pick('q16-a-i', '2-2', 'causes-of-homelessness', ref(16, '(c)(i)'),
     H.ask(36, 'Discuss two reasons for the increase in the number of homeless', ' 1. 2.'),
     'A reason homelessness increased — any two',
     at('lack of affordable public housing', '(ii) Outline two economic measures',
        ['lack of affordable public housing', 'Reduced availability of rental', 'Rising rents',
         'Reduced profit margins', 'Personal factors']),
     2, 6, 'Two reasons, 6 marks each (3 + 3).', stem=q16c_stem)
pick('q16-a-ii', '1-3', 'measures-to-reduce-homelessness', ref(16, '(c)(ii)'),
     H.ask(37, 'Outline two economic measures, other than social housing', ' 1. 2.'),
     'An economic measure other than social housing — any two',
     at('Modular housing:', '33 | P a g e',
        ['Modular housing:', 'Build up, not out:', 'Rezone land:', 'Reduce tax / charges',
         'Increase the levy', 'Increased provision of emergency', 'Rent freeze']),
     2, 6, 'Two measures, 6 marks each (3 + 3). Social housing is excluded by the question.', stem=q16c_stem)
add('q16-c-iii', '3-1', 'why-use-a-cost-benefit-analysis-before-spending', ref(16, '(c)(iii)'),
    H.ask(37, 'In budget 2020 the Minister for Public Expenditure', ' Adapted from') + ' '
    + H.ask(37, 'Explain why the Department for Public Expenditure', ' 75 marks'), '2 @ 3', 6,
    [point('r-1', H.run('To ensure that the benefits of this expenditure', '34 | P a g e'), 6,
           'Explain, 6 marks (2 @ 3): to ensure the economic and social benefits at least equal the costs, '
           'so the best possible benefits accrue to taxpayers.')])

# A card whose figure slot holds its solution carries the whole printed question.
for cid, fig in [('sa-q2', 'p04-q2-question'), ('q13-a-i', 'p22-q13a-question'),
                 ('q13-a-ii', 'p22-q13a-question')]:
    show_before_reveal(next(c for c in cards if c['id'] == D.prefix + cid), None, PAP + fig)


# ── Withdrawn halves ──────────────────────────────────────────────────────────
# The earlier extractors split two jointly priced answers into one card per
# side. Each half is still emitted, lifted from its own list, so that
# card-corrections.json can withdraw it by ID and name the combined card that
# now carries its saved progress (cardAliases.ts). None of these ships.
WITHDRAWN = [
    ('q12-a-ii-neg', 'q12-a-ii-pos', 'Two negative impacts of globalisation', q12_negative, 2, 5),
    ('q16-b-ii-economic', 'q16-b-ii-social', 'An economic reason',
     at('Increase worker’s standard of living', '32 | P a g e',
        ['Increase worker’s standard', 'Increase the incentive to work', 'Boost economic growth']), 1, 5),
]
for old, canonical, label, options, claim, per in WITHDRAWN:
    base = next(c for c in cards if c['id'] == D.prefix + canonical)
    pick(old, base['topicId'].removeprefix('economics-'), base['conceptId'] + '-withdrawn-half',
         base['questionRef'], f"{base['questionText']} Withdrawn half: {label}.", label, options, claim, per,
         f'Withdrawn: this part is answered within {D.prefix + canonical}.', stem=base.get('stem', ''),
         figure=base.get('figureKey', ''), section=base['section'])

if __name__ == '__main__':
    emit(cards)
