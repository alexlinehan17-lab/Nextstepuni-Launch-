#!/usr/bin/env python3
"""Economics 2022 Higher Level, deferred sitting, Sections A and B.

The SEC's deferred examination is a paper of its own: the archive files it
under deferredexams/ and deferredmarkingschemes/ with the June file id, Paper
Trail indexes it as "LC034ALP000EV-deferred", its scheme text is
examiner-reports/economics/schemes/2022-hl-deferred.md, and every card says
so twice: its id ("econ-2022-hl-deferred-...") and its citation ("... —
Deferred sitting"). The census of its 70 printed asks is
drafts/economics-2022-hl-deferred-ev.json (census/census-2022-hl-deferred.py).

Question wording and stems are sliced from the deferred question paper; every
marking point is sliced from the deferred scheme (econ_2026_lib.py). The only
prose written here is guidance: tariffs, route labels and what a figure or a
calculation shows. Scheme PDF page = printed page. Every page of both
documents was viewed; where the scheme's marks column leaves a price open,
the reading is the note on the card.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from econ_2026_lib import Deck, Sheet  # noqa: E402
from econ_lib import anyN, as_option, defurnish, emit, heads, point, tidy  # noqa: E402
from econ_legacy_lib import beside_ask  # noqa: E402

H = Sheet(2022, 'higher', 'LC034ALP000EV', deferred=True)
D = Deck(2022, 'higher', deferred=True)
cards, add, pick, heading, ref = D.cards, D.add, D.pick, D.heading, D.ref
A = dict(section='A')
SOL = 'economics-2022-HL-deferred-scheme-'
PAP = 'economics-2022-HL-deferred-paper-'
EITHER = 'Answer (b) or (c).'


def menu(start, end, pages, **kw):
    """The scheme's headed responses between two anchors, split at its bold headings."""
    return H.menu(start, end, pages, **kw)


def at(start, end, firsts, occ=None):
    """Responses split where each named heading begins (headings the scheme
    does not set in bold)."""
    return [as_option(o) for o in heads(H.chunk(start, end, occ), firsts)]


def run(start, end, occ=None):
    """One contiguous run of the scheme."""
    return H.run(start, end, occ)


def labels(start, end):
    """The labels a scheme prices one by one ("S:1 S2:1 D: 1 ..."), each read
    off its own line as the scheme prints it, without its price."""
    return re.findall(r'(\S+?)\s*:\s*\d+\b', tidy(defurnish(H.chunk(start, end))))


def ask_row(rid, card_ask, marks, note):
    """A row restating the card's own ask: the scheme answers it with a drawing
    and prints no words to claim (its print is the hidden solution figure)."""
    return {"id": rid, "kind": "point", "verbatim": card_ask, "marks": marks, "openList": True,
            "contextNote": note, "ask": True}


def steps(rid, label, options, first, second, what):
    """Two responses paid first-then-second (1 x 4, 1 x 3)."""
    return anyN(rid, label, None, 2, first, options,
                f'Two {what}: the first correct one {first} marks and the second {second}.',
                steps=[first, second])


# ═════════════════════════════════ SECTION A ══════════════════════════════════

# Q1 ─ foreign direct investment
q1_stem = H.ask(3, 'The chart below shows the amounts of foreign direct investment', ' FOREIGN DIRECT')
pick('sa-q1-a', '4-1', 'benefits-of-fdi-inflows', ref(1, '(a)', sa=True),
     H.ask(3, 'Using the above data, outline two positive economic consequences', ' 1. 2.'),
     'A positive consequence of FDI inflows — any two',
     menu('Increased Employment - Creation', '4 | P a g e', [4]),
     2, 3, 'Two consequences, 3 marks each. The scheme prints “1 x 6 (3+3)” and “3 x 3 (1+2)” '
     'together beside (a) and nothing beside (b). (a) asks for two consequences, so it takes the '
     '6 (3 + 3) and (b) the 3 × 3, which makes the question’s 15.',
     stem=q1_stem, figure=PAP + 'p03-q1-chart', **A)
pick('sa-q1-b', '4-1', 'why-firms-invest-abroad', ref(1, '(b)', sa=True),
     H.ask(3, 'Outline reasons why a firm may decide to invest in countries', ' Leaving'),
     'A reason to invest abroad — any three',
     menu('Increase efficiency - companies', '2 The shortage of timber', [5]),
     3, 3, 'Three reasons, 3 marks each (1 + 2). The paper does not say how many; the scheme '
     'prints its “3 x 3 (1+2)” beside (a), and (a) asks for two consequences, so the 3 × 3 is '
     'this part’s.', stem=q1_stem, **A)

# Q2 ─ the timber market; scarcity
q2_stem = H.ask(4, 'The shortage of timber is set to deteriorate', ' Adapted from')
c = add('sa-q2-a', '1-0', 'a-fall-in-supply-on-the-market-diagram', ref(2, '(a)', sa=True),
        H.ask(4, 'Explain, with the aid of a fully labelled diagram, the impact', ' Explanation:'),
        '7 + 3 x 1', 10,
        [anyN('r-labels', 'The diagram — one mark for each label', 7, 7, 1,
              labels('S:1', 'Explanation:'),
              'The diagram, 7 marks: the scheme prices each of its seven labels at 1 (S, S2, D, P1, '
              'P2, Q1, Q2). Supply shifts left from S to S2 and the price rises from P1 to P2. The '
              'official diagram is shown in the figure.'),
         point('r-shift', run('The undersupply of logs means', '5 | P a g e'), 1,
               'The explanation, 3 × 1: the supply curve shifts left.'),
         point('r-cause', run('There is a decrease in supply caused', 'The price increases'), 1,
               'The decrease in supply has an unplanned cause.'),
         point('r-price', run('The price increases form', '(b)\nExplain the meaning'), 1,
               'The price rises from P1 to P2 (the scheme prints “form” for “from”).')],
        stem=q2_stem, figure=SOL + 'p05-q2a-diagram', **A)
beside_ask(c, PAP + 'p04-q2a-diagram')
pick('sa-q2-b', '0-1', 'the-meaning-of-scarcity', ref(2, '(b)', sa=True),
     H.ask(4, 'Explain the meaning of the economic concept scarcity.', ' Explanation:'),
     'Scarcity — any wording',
     [run('The supply of resources / factors', 'Quantity of goods and service'),
      run('Quantity of goods and service people', 'Our wants are infinite'),
      run('Our wants are infinite', '3 The table below')],
     1, 5, 'Explain the term, 5 marks; the scheme gives three wordings of the same idea.',
     stem=q2_stem, **A)

# Q3 ─ income elasticity of demand
q3_stem = H.ask(5, 'The table below shows the annual average level of income', ' Year Income')
add('sa-q3-a', '1-4', 'income-elasticity-of-demand-by-formula', ref(3, '(a)', sa=True),
    H.ask(5, 'Using an appropriate formula, calculate the income elasticity', ' Workings:'), '5 x 2', 10,
    [point('r-dq', 'Change in quantity — 125', 2,
           'The scheme prints 5 × 2: one 2 for each of the five figures in its working. The change '
           'in quantity demanded, 275 − 150.'),
     point('r-dy', 'Change in income — 5,000', 2, 'The change in income, 65,000 − 60,000.'),
     point('r-sum-y', '60,000 + 65,000 (125,000)', 2, 'The sum of the two incomes.'),
     point('r-sum-q', '150 + 275 (425)', 2, 'The sum of the two quantities.'),
     point('r-answer', '= + 7.35', 2,
           'The answer: YED = (125 ÷ 5,000) × (125,000 ÷ 425) = +7.35.')],
    stem=q3_stem, figure=PAP + 'p05-q3-table', **A)
add('sa-q3-b', '1-4', 'reading-a-yed-figure', ref(3, '(b)', sa=True),
    H.ask(5, 'Using your knowledge of YED, explain the economic meaning', ' Leaving'), '3 + 2', 5,
    [point('r-sign', run('+ sign:', 'Number: +7.35'), 3,
           'The sign, 3 marks: a positive YED is a normal good. The scheme prints 1 × 3 and 1 × 2 '
           'beside (b) and sets its answer under two headings, “+ sign” and “Number”; read in that '
           'order, the sign earns 3 and the number 2.'),
     point('r-number', run('Number: +7.35', '6 | P a g e'), 2,
           'The number, 2 marks: greater than 1, so the good is income elastic, a luxury.')],
    stem=q3_stem, **A)

# Q4 ─ ticket touting
q4_stem = H.ask(6, 'A new law banning ticket touting', ' (a) Outline')
pick('sa-q4-a', '1-3', 'why-ban-ticket-touting', ref(4, '(a)', sa=True),
     H.ask(6, 'Outline two reasons why the government introduced this legislation.', ' 1. 2.'),
     'A reason for the legislation — any two',
     menu('Prevent consumer exploitation', '(b) The maximum capacity', [7]),
     2, 4, 'Two reasons, 4 marks each (2 + 2).', stem=q4_stem, **A)
q4b_ask = H.ask(6, 'The maximum capacity of the Croke Park stadium', ' Diagram')
add('sa-q4-b', '1-2', 'a-fixed-supply-of-tickets', ref(4, '(b)', sa=True),
    q4b_ask, '3 x 1 + 2 x 2', 7,
    [ask_row('r-diagram', 'Explain your answer with the aid of a fully labelled diagram.', 3,
             'The diagram, 3 × 1: one mark for each label the scheme marks, the vertical supply line '
             'S1, the quantity Q1 and 82,300. Compare yours with the official diagram shown after '
             'you answer.'),
     point('r-fixed', 'No — ' + run('The supply of tickets available for the All-Ireland', 'Regardless of price'), 2,
           'Tick NO. The scheme answers “No, the law will not change this.” and prices the two '
           'sentences that follow 2 × 2: the supply is fixed at 82,300.'),
     point('r-unchanged', run('Regardless of price and the new law', '7 | P a g e'), 2,
           'The supply curve does not move, whatever the price.')],
    stem=q4_stem, figure=SOL + 'p07-q4b-diagram', **A)

# Q5 ─ data centres; rural broadband; regional development
q5_stem = H.ask(7, 'Ireland has one of the fastest growing data centre markets', ' Adapted from')
add('sa-q5-a', '4-2', 'irelands-comparative-advantage-for-data-centres', ref(5, '(a)', sa=True),
    H.ask(7, 'Outline two sources of comparative advantage', ' 1. 2.'), '4 + 3', 7,
    [steps('r-1', 'A source of comparative advantage — any two',
           menu('Climate – Ireland has a cool', 'Answer (b) or (c)', [8]), 4, 3, 'sources')],
    stem=q5_stem, **A)
pick('sa-q5-b', '3-5', 'benefits-of-rural-broadband', ref(5, '(b)', sa=True),
     H.ask(7, 'The €5.7 bn rural broadband scheme', ' Adapted from'),
     'A benefit of the rural broadband scheme — any two',
     at('Improved standard of living:', '8 | P a g e',
        ['Improved standard of living:', 'Option of remote/tele working', 'Equitable service for all',
         'Protection of the environment', 'Education – With improved', 'Viable rural communities']),
     2, 4, 'Two benefits, 4 marks each (2 + 2).', stem=q5_stem, notes=EITHER, **A)
pick('sa-q5-c', '3-5', 'why-support-balanced-regional-development', ref(5, '(c)', sa=True),
     H.ask(8, 'Explain two reasons why government policies should support', ' 1. 2.'),
     'A reason to support balanced regional development — any two',
     menu('To promote employment creation', '6 (a) Explain the term GNP', [9]),
     2, 4, 'Two reasons, 4 marks each (2 + 2).', stem=q5_stem, notes=EITHER, **A)

# Q6 ─ GNP; the national accounts
add('sa-q6-a', '3-0', 'gnp-at-current-market-prices', ref(6, '(a)', sa=True),
    H.ask(9, 'Explain the term GNP at current market prices.', ' Explanation:'), '3 x 3', 9,
    [point('r-output', 'total output / value of goods and services', 3,
           'The scheme prints “Any 3 x 3” beside its one definition and sets three parts of it in '
           'bold: one 3 for each part. The total output, or value, of goods and services.'),
     point('r-irish', 'Irish-owned factors of production / in Ireland and elsewhere', 3,
           'Produced by Irish-owned factors of production, in Ireland and elsewhere.'),
     point('r-prices', 'measured by current market prices', 3, 'Measured at current market prices.')],
    **A)
add('sa-q6-b', '3-0', 'gnp-gni-and-gni-star-from-the-national-accounts', ref(6, '(b)', sa=True),
    H.ask(9, 'The data below has been adapted', ' Description') + ' '
    + H.ask(9, 'Given that Gross Domestic Product (GDP) at Current Market Prices', ' Adjustments/Relationships'),
    '2 x 3', 6,
    [anyN('r-1', 'A measure, its relationship and its working — any two', 6, 2, 3,
          [run('(A) GNP at current market prices', 'OR\n(B)'),
           run('(B) GNI at CMP', 'OR\n(C)'),
           run('(C) Modified GNI at CMP', '7 (a) The Irish government')],
          'Any two of A, B or C, 3 marks each: the relationship stated and the working to its answer. '
          'GNP €281.8 bn, GNI €282.9 bn, GNI* €207.3 bn.')],
    figure=PAP + 'p09-q6b-table', **A)

# Q7 ─ environment; international aid
add('sa-q7-a', '0-2', 'irish-measures-to-protect-the-environment', ref(7, '(a)', sa=True),
    H.ask(10, 'The Irish government is committed to protecting the environment.', ' 1. 2.'), '4 + 3', 7,
    [steps('r-1', 'A measure to protect the environment — any two',
           menu('Increased carbon tax', '(b) During COP 2021', [10]), 4, 3, 'measures')],
    **A)
pick('sa-q7-b', '4-0', 'why-ireland-assists-less-developed-nations', ref(7, '(b)', sa=True),
     H.ask(10, 'During COP 2021, Ireland pledged', ' Adapted from'),
     'A reason Ireland assists less developed nations — any two',
     at('Attain sustainable development goals', '10 | P a g e',
        ['Attain sustainable development goals', 'To promote economic development', 'Humanitarian reasons',
         'Reduce poverty, hunger etc', 'Improve access and quality of education', 'Provide access to clean water',
         'Meet UN target of 0.7%']),
     2, 4, 'Two reasons other than climate change, 4 marks each (2 + 2).', notes=EITHER, **A)
pick('sa-q7-c', '4-0', 'challenges-of-relying-on-international-aid', ref(7, '(c)', sa=True),
     H.ask(11, 'Outline two challenges for less developed nations', ' 1. 2.'),
     'A challenge of relying on international aid — any two',
     menu('Reduced incentive to increase economic growth', '8 (a) As world population', [11]),
     2, 4, 'Two challenges, 4 marks each (2 + 2).', notes=EITHER, **A)

# Q8 ─ population and sustainability; electric cars and market failure
add('sa-q8-a', '0-2', 'is-a-world-of-8-billion-sustainable', ref(8, '(a)', sa=True),
    H.ask(11, 'As world population has increased', ' Explanation:'), '7', 7,
    [point('r-yes', run('Yes as unless human behaviour changes', '(b) 5% of new private cars'), 7,
           'Agree, 7 marks. The paper asks whether you agree; the scheme answers Yes and prints no '
           'case for disagreeing.')],
    **A)
add('sa-q8-b', '2-2', 'electric-cars-as-a-market-failure', ref(8, '(b)', sa=True),
    H.ask(11, '5% of new private cars purchased in 2020', ' Explanation:'), '2 + 6', 8,
    [point('r-true', 'True', 2, 'Tick TRUE, 2 marks: the scheme ticks True.'),
     point('r-explanation', run('Market failure occurs when economic resources', '11 | P a g e'), 6,
           'The explanation, 6 marks: what market failure is, and the high price of electric '
           'vehicles as a partial market failure.')],
    **A)

# Q9 ─ a hairdressing salon's revenue; specialisation
q9_stem = H.ask(12, 'The table below shows the daily revenue for Headhunters', ' Quantity of')
c = add('sa-q9-a', '1-5', 'total-and-marginal-revenue', ref(9, '(a)', sa=True),
        H.ask(12, 'Complete the total revenue column and the marginal revenue column', ' Workings:'),
        '7 x 1', 7,
        [anyN('r-total', 'Total revenue — the four cells', 4, 4, 1,
              [run('15 x 21 = €315', '18 x 19'), run('18 x 19 = €342', '22 x 17'),
               run('22 x 17 = €374', '28 x 15'), run('28 x 15 = €420', '⟨7 x 1⟩')],
              'The scheme prints 7 × 1: one mark for each completed cell. Total revenue is quantity '
              '× average revenue, four cells.'),
         anyN('r-marginal', 'Marginal revenue — the three cells', 3, 3, 1,
              [run('€342 - €315 = €27', '€374 - €342'), run('€374 - €342 = €32', '€420 - €374'),
               run('€420 - €374 = €46', 'Answer (b) or (c)')],
              'Marginal revenue, three cells: the change in total revenue (the scheme also divides '
              'by the change in quantity, in brackets). The completed table is shown in the figure.')],
        stem=q9_stem, figure=SOL + 'p12-q9a-table', **A)
beside_ask(c, PAP + 'p12-q9-table')
pick('sa-q9-b', '1-5', 'specialisation-and-the-consumer', ref(9, '(b)', sa=True),
     H.ask(12, 'Specialisation involved in hairdressing', ' Benefit:'),
     'A benefit of specialisation to the consumer — any one',
     menu('Better quality / service', 'OR\n(c) Outline one possible', [12]),
     1, 8, 'One benefit, 8 marks. The paper asks for one; the scheme prices this part “2 x 4 '
     '(2+2)”, 8 marks in all, and does not say how one benefit earns them, so the one benefit is '
     'assessed against the part’s 8.', stem=q9_stem, notes=EITHER, **A)
pick('sa-q9-c', '1-5', 'specialisation-and-the-salon', ref(9, '(c)', sa=True),
     H.ask(13, 'Outline one possible economic disadvantage of specialisation', ' Leaving'),
     'A disadvantage of specialisation to the salon — any one',
     menu('Increased training costs', '12 | P a g e', [12]),
     1, 8, 'One disadvantage, 8 marks. The paper asks for one; the scheme prices this part “2 x 4 '
     '(2+2)”, 8 marks in all, and does not say how one disadvantage earns them, so the one '
     'disadvantage is assessed against the part’s 8.', stem=q9_stem, notes=EITHER, **A)

# Q10 ─ the benchmark interest rate
q10_stem = H.ask(14, 'The chart below displays the benchmark interest rate', ' Benchmark')
pick('sa-q10-a', '3-3', 'trends-in-the-benchmark-interest-rate', ref(10, '(a)', sa=True),
     H.ask(14, 'Outline two key trends in interest rates', ' (b)'),
     'A trend in interest rates — any two',
     at('2008 - 2019:', '(b) Explain how current interest rates',
        ['2008 - 2019:', '2009 – 2011:', '2011 – 2015:', '2015 on:']),
     2, 4, 'Two trends, 4 marks each (2 + 2), each with its years and rates.',
     stem=q10_stem, figure=PAP + 'p14-q10-chart', **A)
pick('sa-q10-b', '3-3', 'low-interest-rates-and-borrowers', ref(10, '(b)', sa=True),
     H.ask(14, 'Explain how current interest rates may affect borrowers', ' Leaving'),
     'An effect on borrowers — any one',
     menu('Incentive to borrow', '13 | P a g e', [13]),
     1, 7, 'One developed effect, 7 marks (4 + 3). The paper asks for no number; the scheme’s '
     '“7 (4+3)” is one response, as it is beside the asks for one benefit in Q12(c).',
     stem=q10_stem, **A)


# ═════════════════════════════════ SECTION B ══════════════════════════════════

# Q11 ─ the budget; trade with the US and Great Britain; the circular flow
q11_stem = H.ask(15, 'The chart below shows Ireland’s fiscal data', ' Government Revenue')
q11_fig = PAP + 'p15-q11-chart'
add('q11-a-i', '3-1', 'years-of-budget-surplus', ref(11, '(a)(i)'),
    H.ask(15, 'Using the data above name the years in which Ireland had a budget surplus.', ' Year 1:'),
    '4 + 3', 7,
    [point('r-2018', 'Year 1 — 2018', 4, 'The scheme prints 4 beside 2018 and 3 beside 2019.'),
     point('r-2019', 'Year 2 — 2019', 3, 'The second year of surplus.')],
    stem=q11_stem, figure=q11_fig)
add('q11-a-ii', '3-1', 'the-2020-budget-deficit', ref(11, '(a)(ii)'),
    H.ask(15, 'Using the information provided in the diagram above calculate', ' Workings:'),
    '4 x 3', 12,
    [point('r-revenue', 'Income — €84.5 bn', 3,
           'The scheme prints 4 × 3 beside “€84.5 bn – €103.3 bn = - €18.8 bn” and “Deficit”: one 3 '
           'for each of its four figures and words.'),
     point('r-expenditure', 'Expenditure — €103.3 bn', 3, 'Expenditure, subtracted from revenue.'),
     point('r-balance', '= - €18.8 bn', 3, 'The balance.'),
     point('r-outcome', 'Deficit', 3, 'The outcome stated: a deficit.')],
    stem=q11_stem, figure=q11_fig)
add('q11-a-iii', '3-1', 'expansionary-fiscal-policy-in-2020', ref(11, '(a)(iii)'),
    H.ask(15, 'In your opinion, in 2020 which policy was the Irish government pursuing?', ' Explanation:'),
    '1 + 5', 6,
    [point('r-tick', 'Expansionary', 1, 'Tick EXPANSIONARY, 1 mark: the scheme ticks Expansionary.'),
     point('r-explanation', run('The government is spending more money than it is receiving', '⟨25⟩'), 5,
           'The explanation with an example, 5 marks: spending above revenue, with the pandemic '
           'spending on health, education and unemployment benefit.')],
    stem=q11_stem, figure=q11_fig)
add('q11-b-i', '4-2', 'trade-with-the-us-and-great-britain', ref(11, '(b)(i)'),
    H.ask(16, 'The pie charts below display the share of total exports', ' Share of') + ' '
    + H.ask(16, 'Using the above data, outline the effect of the relevant information', ' US:'),
    '4 + 4', 8,
    [point('r-us', run('US – Trade surplus.', 'Irelands exports (29%)'), 2,
           'The scheme prints 4 (2 × 2) beside each country: 2 for the outcome and 2 for the figures '
           'that show it. The US: a trade surplus.'),
     point('r-us-why', run('Irelands exports (29%) exceeds imports', 'GB – Trade deficit.'), 2,
           'Exports to the US (29%) exceed imports from it (20%).'),
     point('r-gb', run('GB – Trade deficit.', 'Irelands imports (18%)'), 2,
           'Great Britain: a trade deficit.'),
     point('r-gb-why', run('Irelands imports (18%) exceeds exports to the UK', '(ii) Outline one possible'), 2,
           'Imports from Great Britain (18%) exceed exports to it. The scheme prints 00% for '
           'exports; the chart shows 10%.')],
    figure=PAP + 'p16-q11b-pies')
add('q11-b-ii', '4-2', 'a-benefit-and-a-challenge-of-imports', ref(11, '(b)(ii)'),
    H.ask(16, 'Outline one possible economic benefit and one possible economic challenge', ' Economic benefit:'),
    '6 + 6', 12,
    [heading('r-benefit', 'An economic benefit of imports — any one',
             menu('Increased choice of goods and services', 'Economic challenge', [15]), 6,
             'One benefit, 6 marks (3 + 3).'),
     heading('r-challenge', 'An economic challenge of imports — any one',
             at('More dependent on other countries', '15 | P a g e',
                ['More dependent on other countries', 'Domestic companies might struggle to compete']), 6,
             'One challenge, 6 marks (3 + 3).')],
    kind='fixed')
add('q11-c-i', '3-0', 'the-circular-flow-of-an-open-economy', ref(11, '(c)(i)'),
    H.ask(17, 'Draw a fully labelled diagram, showing the Circular Flow of Income', ' (ii)'),
    '13 x 1', 13,
    [ask_row('r-diagram', H.ask(17, 'Draw a fully labelled diagram, showing the Circular Flow of Income', ' (ii)'), 13,
             'The diagram, 13 × 1: one mark for each label. The official diagram, shown after you '
             'answer, labels households, firms, government, financial institutions and foreign '
             'markets, and the flows between them: incomes, spending, tax, government expenditure, '
             'savings, investment, imports and exports.')],
    figure=SOL + 'p16-q11ci-diagram')
add('q11-c-ii', '3-0', 'injections-and-leakages', ref(11, '(c)(ii)'),
    H.ask(17, 'Explain the terms injections and leakages using examples', ' Injections:'),
    '2 + 2 x 2 + 2 + 2 x 2', 12,
    [point('r-injections', run('Injections: Injections are variables', 'Examples: Investment'), 2,
           'Injections explained, 2 marks.'),
     anyN('r-injection-examples', 'An example of an injection — any two', 4, 2, 2,
          ['Investment', 'Gov Expenditure', 'Exports'],
          'Two examples, 2 marks each, from the scheme’s “Investment/Gov Expenditure/Exports”.'),
     point('r-leakages', run('Leakages: Leakages are the non-consumption', 'Examples: Savings'), 2,
           'Leakages explained, 2 marks.'),
     anyN('r-leakage-examples', 'An example of a leakage — any two', 4, 2, 2,
          ['Savings', 'Taxes', 'Imports'],
          'Two examples, 2 marks each, from the scheme’s “Savings/Taxes/Imports”.')])
add('q11-c-iii', '3-0', 'a-welfare-bonus-in-the-circular-flow', ref(11, '(c)(iii)'),
    H.ask(18, 'The Irish Government paid all social welfare recipients a Christmas bonus', ' Adapted from')
    + ' ' + H.ask(18, 'Outline how this measure might have affected the Circular Flow', ' 75 marks'),
    '5', 5,
    [point('r-1', run('This is an increase in an injection into the circular', '⟨30⟩'), 5,
           'The effect, 5 marks: an injection that raises aggregate demand by the injection times '
           'the multiplier.')])

# Q12 ─ mortgage market concentration; perfect competition; monopoly
q12_stem = H.ask(19, 'The pie charts below indicate the mortgage market share', ' MARKET SHARE')
add('q12-a-i', '2-0', 'mortgage-market-concentration-2008-to-2021', ref(12, '(a)(i)'),
    H.ask(19, 'Using the data in the pie charts above, comment on the change', ' Answer:'),
    '6 + 6', 12,
    [point('r-2008', '2008 — ' + run('There is a low concentration ratio for the banking', 'There is a high concentration ratio'), 6,
           '2008, 6 marks (3 + 3): a low concentration ratio, many firms.'),
     point('r-2021', '2021 — ' + run('There is a high concentration ratio / oligopoly.', '(ii) Outline two possible'), 6,
           '2021, 6 marks (3 + 3): a high concentration ratio, an oligopoly of three. The scheme '
           'heads this response “2001”; the paper’s chart is 2021.')],
    stem=q12_stem, figure=PAP + 'p19-q12-pies')
add('q12-a-ii', '2-0', 'when-low-concentration-hurts-consumers', ref(12, '(a)(ii)'),
    H.ask(19, 'Outline two possible reasons why a low market concentration', ' Leaving'), '4 + 3', 7,
    [steps('r-1', 'A difficulty for consumers — any two',
           [o.rstrip(' -–') for o in at('Confusing pricing', '17 | P a g e',
                                        ['Confusing pricing', 'Competition may be limited', 'Lower standard of living'])],
           4, 3, 'reasons')])
q12b_stem = H.ask(20, 'Neo‐classical Economists argued', ' (i)')
c = add('q12-b-i', '2-0', 'long-run-equilibrium-in-perfect-competition', ref(12, '(b)(i)'),
        H.ask(20, 'In the space provided below, explain with the aid of a fully labelled diagram', ' f Explanation:'),
        '9 + 8', 17,
        [anyN('r-labels', run('1 mark per label = 9 marks', 'Explanation:'), 9, 9, 1,
              run('1 mark per label = 9 marks', 'Explanation:')[len('1 mark per label = 9 marks '):].split(),
              'The diagram, 1 mark for each of the 9 labels. The official diagram is shown in the figure.'),
         anyN('r-explanation', 'The explanation — one mark for each point', 8, 8, 1,
              ['Equilibrium is at point E (where MC=MR).', 'Firms produce quantity Q2.',
               'They sell the output at price P2.', 'Costs are at the level C2.',
               'Firms earn normal profits', 'as AR is equal to AC.', 'The firm is efficient',
               'as costs are at the minimum point of the AC curve'],
              'The explanation, 8 marks: the scheme marks eight points with a 1, two of them inside '
              'the last two sentences (normal profits, AR equal to AC; efficient, at the minimum of '
              'AC).')],
        stem=q12b_stem, figure=SOL + 'p18-q12bi-diagram')
add('q12-b-ii', '2-0', 'perfect-competition-for-and-against', ref(12, '(b)(ii)'),
    H.ask(21, 'Explain one possible economic advantage and one possible economic disadvantage', ' Economic advantage:'),
    '6 + 4', 10,
    [heading('r-advantage', 'An advantage of perfect competition — any one',
             at('Low prices - The firm sells', '18 | P a g e',
                ['Low prices - The firm sells', 'Efficiency is encouraged', 'Consumers are not exploited',
                 'No advertising – as all']), 6,
             'One advantage, 6 marks (3 + 3). The scheme prints “1 x 6 (3+3)” and “1 x 4 (2+2)”; '
             'read in the order the paper asks and the scheme answers, the advantage earns 6 and '
             'the disadvantage 4.'),
     heading('r-disadvantage', 'A disadvantage of perfect competition — any one',
             menu('Little potential to expand', '(iii) Firms in perfect competition', [19]), 4,
             'One disadvantage, 4 marks (2 + 2).')],
    stem=q12b_stem, kind='fixed')
pick('q12-b-iii', '2-0', 'advertising-in-perfect-competition', ref(12, '(b)(iii)'),
     H.ask(21, 'Firms in perfect competition should not engage in advertising.', ' 1. 2.'),
     'A reason to agree — any two',
     menu('Homogenous goods - since the goods', '⟨35⟩', [19]),
     2, 4, 'Agree. The scheme ticks Agree and gives reasons for agreeing only: two reasons, 4 marks '
     'each (2 + 2).', stem=q12b_stem)
q12c_stem = H.ask(21, 'In 2013 the EU blocked the takeover of Aer Lingus', ' Adapted from')
pick('q12-c-i', '1-3', 'why-regulate-markets-for-consumers', ref(12, '(c)(i)'),
     H.ask(21, 'Explain why it is important for consumers that bodies like the EU', ' Leaving'),
     'A reason regulation matters to consumers — any one',
     menu('Prevents exploitation', '19 | P a g e', [19]),
     1, 7, 'One developed reason, 7 marks (4 + 3). The paper asks for no number; the scheme’s '
     '“7 (4+3)” is one response, as it is beside (ii) and (iii), which ask for one benefit.',
     stem=q12c_stem)
pick('q12-c-ii', '2-0', 'monopoly-power-and-employees', ref(12, '(c)(ii)'),
     H.ask(22, 'Explain one benefit for employees', ' (iii)'),
     'A benefit for employees — any one',
     menu('Secure employment - as there', '(iii) Explain one benefit for consumers', [20]),
     1, 7, 'One benefit, 7 marks (4 + 3).', stem=q12c_stem)
pick('q12-c-iii', '2-0', 'monopoly-power-and-consumers', ref(12, '(c)(iii)'),
     H.ask(22, 'Explain one benefit for consumers', ' 75 marks'),
     'A benefit for consumers — any one',
     at('Guarantee supply of product/service', '⟨21⟩',
        ['Guarantee supply of product/service', 'Economies of scale - production', 'Potential for innovation/R&D']),
     1, 7, 'One benefit, 7 marks (4 + 3).', stem=q12c_stem)

# Q13 ─ unemployment; the living wage; inflation
q13_stem = H.ask(23, 'The diagram below shows the percentage (%) unemployment rate', ' www.centralbank.ie')
add('q13-a-i', '3-2', 'why-unemployment-rose-and-is-forecast-to-fall', ref(13, '(a)(i)'),
    H.ask(23, 'Using the above information outline one possible reason for the changes', ' 2020 – 2021:'),
    '5 + 5', 10,
    [point('r-2020', run('2020-2021 ⟨5⟩', '2022-2023'), 5,
           '2020–2021, 5 marks: unemployment rose from 5.9% to 7.3% as the pandemic closed retail '
           'and hospitality.'),
     point('r-2022', run('2022-2023 ⟨5⟩', '(ii) Discuss why some businesses'), 5,
           '2022–2023, 5 marks: unemployment is forecast to fall from 7.2% to 5.9% as savings fuel '
           'demand and the economy recovers.')],
    stem=q13_stem, figure=PAP + 'p23-q13-chart')
pick('q13-a-ii', '2-1', 'labour-shortages-alongside-unemployment', ref(13, '(a)(ii)'),
     H.ask(23, 'Discuss why some businesses in Ireland are experiencing labour shortages', ' Leaving'),
     'A reason for labour shortages — any one',
     at('Skills shortage – there is', '21 | P a g e',
        ['Skills shortage – there is', 'Wages considered unattractive', 'Exodus of foreign workers',
         'The pandemic unemployment payment (PUP)', 'Reductions in workers due to Covid']),
     1, 5, 'One developed reason, 5 marks (3 + 2).', stem=q13_stem)
pick('q13-a-iii', '3-2', 'effects-of-unemployment-on-the-economy', ref(13, '(a)(iii)'),
     H.ask(24, 'In May 2021, a report in the Social Justice Ireland', ' Adapted from'),
     'An effect of unemployment — any two',
     menu('Increased current expenditure for the government', '(b) The Low Pay Commission', [22]),
     2, 4, 'Two effects, 4 marks each (2 + 2).', stem=q13_stem)
q13b_stem = H.ask(24, 'The Low Pay Commission will examine', ' Adapted from')
add('q13-b-i', '2-1', 'the-living-wage', ref(13, '(b)(i)'),
    H.ask(24, 'Explain the term living wage.', ' Explanation:'), '7', 7,
    [point('r-1', run('It is a wage which makes possible a minimum acceptable', '22 | P a g e'), 7,
           'Explain the term, 7 marks: a wage that affords a minimum, socially acceptable standard '
           'of living, set by social consensus and not by the cost of living.')],
    stem=q13b_stem)
add('q13-b-ii', '2-1', 'effects-of-a-living-wage', ref(13, '(b)(ii)'),
    H.ask(24, 'Outline one possible economic effect on employees, businesses, and the government', ' Employees:'),
    '7 + 7 + 7', 21,
    [heading('r-employees', 'An effect on employees — any one',
             menu('Increased standard of living – if', 'Businesses:', [23]), 7,
             'Employees: one effect, 7 marks (4 + 3).'),
     heading('r-businesses', 'An effect on businesses — any one',
             menu('Increased costs – if the government', 'Government:', [23]), 7,
             'Businesses: one effect, 7 marks (4 + 3). The scheme also accepts “Incentive to work”, '
             'listed under employees, here.'),
     heading('r-government', 'An effect on the government — any one',
             menu('More direct tax revenue', '(c) In budget 2022', [23], drop=('⟨28⟩',)), 7,
             'Government: one effect, 7 marks (4 + 3).')],
    stem=q13b_stem, kind='fixed')
add('q13-c-i', '3-3', 'pensioners-and-inflation', ref(13, '(c)(i)'),
    H.ask(25, 'In budget 2022 the government increased the old age pension', ' Answer:'), '6', 6,
    [point('r-no', 'No — ' + run('Pensioners income has lost its ability', '23 | P a g e'), 6,
           'Answer NO, 6 marks (3 + 3): the scheme answers No. A €5 rise is far less than the '
           'inflation rate, so pensioners can buy less and their standard of living falls.')])
pick('q13-c-ii', '3-1', 'easing-high-inflation-for-citizens', ref(13, '(c)(ii)'),
     H.ask(26, 'Suggest two measures the Irish Government could take', ' 1. 2.'),
     'A measure to ease high inflation — any two',
     menu('Energy credit', '(iii) If inflation continues', [24]),
     2, 6, 'Two measures, 6 marks each (3 + 3).')
pick('q13-c-iii', '3-3', 'an-ecb-measure-against-inflation', ref(13, '(c)(iii)'),
     H.ask(26, 'If inflation continues at a high rate in Europe', ' 75 marks'),
     'An ECB measure — any one',
     menu('Increase interest rates – if', '⟨24⟩', [24]),
     1, 6, 'One measure, 6 marks (3 + 3).')

# Q14 ─ the cost of collecting tax; tax principles; the PPF; costs
q14_stem = H.ask(27, 'In 2020 Revenue Commissioners in Ireland collected', ' Adapted from')
add('q14-a-i', '3-1', 'revenues-cost-of-collection', ref(14, '(a)(i)'),
    H.ask(27, 'From the data above, calculate Revenue’s administration costs', ' Workings'),
    '4 x 2', 8,
    [point('r-cost', '€467m', 2,
           'The scheme prints 4 × 2: one 2 for each of the four parts of its working, €467m over '
           '€82bn, times 100, = 0.6%.'),
     point('r-receipts', '€82bn', 2, 'The gross receipts, beneath the costs.'),
     point('r-times', 'x 100', 2, 'Times 100.'),
     point('r-answer', '= 0.6%', 2, 'The answer.')],
    stem=q14_stem)
pick('q14-a-ii', '3-1', 'principles-of-a-good-tax-system', ref(14, '(a)(ii)'),
     H.ask(27, 'The data above clearly demonstrates that Revenue follows', ' 1. 2. 3.'),
     'A principle of taxation — any three',
     menu('Taxes should be equitable', '25 | P a g e', [25]),
     3, 5, 'Three principles other than economy, 5 marks each (2 + 3). The paper asks for a “fair” '
     'tax system; the scheme writes “modern”.', stem=q14_stem)
add('q14-a-iii', '3-1', 'is-local-property-tax-regressive', ref(14, '(a)(iii)'),
    H.ask(27, 'The Irish government increased the bands in Local Property Tax', ' Answer:'), '7', 7,
    [point('r-regressive', run('LPT is a regressive tax because', '⟨30⟩'), 7,
           'Answer REGRESSIVE, 7 marks: the scheme answers regressive, because LPT does not take '
           'ability to pay into account.')])
q14b_stem = H.ask(28, 'The diagram below shows the Production Possibility Frontier', ' (i)')
c = add('q14-b-i', '0-1', 'opportunity-cost-on-a-ppf', ref(14, '(b)(i)'),
        H.ask(28, 'Explain, and clearly illustrate using the diagram above', ' Explanation:'), '4 + 4', 8,
        [ask_row('r-diagram', 'clearly illustrate using the diagram above', 4,
                 'The diagram, 4 marks: the scheme’s, shown after you answer, marks MP2 and point B '
                 'where Sw2 meets the frontier.'),
         point('r-explanation', run('If the firm increases production of smartwatches to SW2', '26 | P a g e'), 4,
               'The explanation, 4 marks: more smartwatches means fewer mobile phones, MP2 at point '
               'B.')],
        stem=q14b_stem, figure=SOL + 'p26-q14bi-ppf')
beside_ask(c, PAP + 'p28-q14b-ppf')
c = add('q14-b-ii', '0-1', 'a-chip-shortage-and-the-ppf', ref(14, '(b)(ii)'),
        H.ask(29, 'Companies across industries, globally', ' Adapted from') + ' '
        + H.ask(29, 'Explain, and clearly demonstrate on the diagram below', ' Explanation:'),
        '4 + 2 x 2', 8,
        [ask_row('r-diagram', 'clearly demonstrate on the diagram below', 4,
                 'The diagram, 4 marks: the frontier shifts inwards, as in the scheme’s diagram shown '
                 'after you answer.'),
         point('r-shift', run('The PPF will shift to the left (inwards)', 'Less output can be produced.'), 2,
               'The explanation, 2 × 2: the frontier shifts inwards as capacity falls.'),
         point('r-output', 'Less output can be produced.', 2, 'Less can be produced.')],
        stem=q14b_stem, figure=SOL + 'p27-q14bii-ppf')
beside_ask(c, PAP + 'p29-q14bii-ppf')
add('q14-c-i', '1-5', 'drawing-srac-and-mc', ref(14, '(c)(i)'),
    H.ask(30, 'On one diagram, draw and fully label', ' (ii)'), '4 x 3', 12,
    [ask_row('r-diagram', H.ask(30, 'On one diagram, draw and fully label', ' (ii)'), 12,
             'The diagram, 12 marks. The scheme prints 4 × 3 beside its diagram (Cost and output on '
             'the axes, a U-shaped AC, MC rising through its lowest point) and does not name the four '
             'elements; compare your whole drawing with it.')],
    figure=SOL + 'p27-q14ci-curves')
add('q14-c-ii', '1-5', 'the-shape-of-the-srac', ref(14, '(c)(ii)'),
    H.ask(30, 'Explain the reasons for the shape of the SRAC.', ' Downward'), '4 + 4', 8,
    [heading('r-downward', 'Downward sloping part — any one',
             at('Specialisation/division of labour:', 'Upward sloping part:',
                ['Specialisation/division of labour:', 'Greater spread of fixed costs:']), 4,
             'The downward-sloping part, 4 marks (2 + 2).'),
     point('r-upward', run('The law of diminishing marginal returns / AVC', '(iii) Explain the relationship'), 4,
           'The upward-sloping part, 4 marks (2 × 2): diminishing marginal returns.')])
add('q14-c-iii', '1-5', 'how-mc-and-ac-are-related', ref(14, '(c)(iii)'),
    H.ask(30, 'Explain the relationship between Marginal Costs (MC) and Average Costs (AC).', ' Explanation:'),
    '3 x 3', 9,
    [point('r-below', run('When MC is less than AC', '• When MC is greater'), 3, '3 × 3: one 3 for each.'),
     point('r-above', run('When MC is greater than AC', '• When MC is equal'), 3, 'MC above AC.'),
     point('r-equal', run('When MC is equal to AC', '⟨29⟩'), 3, 'MC equal to AC.')])

# Q15 ─ the market for electric vehicles; subsidies; intervention
c = add('q15-a-i', '1-0', 'demand-and-supply-for-electric-vehicles', ref(15, '(a)(i)'),
        H.ask(31, 'Describe by means of a clearly labelled diagram', ' Explanation:'), '8 + 2 x 2 + 2 x 2', 16,
        [anyN('r-labels', 'The diagram — two marks for each label', 8, 4, 2, labels('P:2', 'The demand curve'),
              'The diagram, 8 marks: the scheme prices four labels at 2 (P, Q, D, S). The official '
              'diagram is shown in the figure.'),
         point('r-demand', run('The demand curve for electric vehicles is downward', 'As price rises, quantity demanded'), 2,
               'Demand, 2 × 2: the curve slopes down.'),
         point('r-demand-why', run('As price rises, quantity demanded falls', 'The supply curve'), 2,
               'Quantity demanded falls as price rises.'),
         point('r-supply', run('The supply curve for electric vehicles is upward', 'As price rises, quantity supplied'), 2,
               'Supply, 2 × 2: the curve slopes up.'),
         point('r-supply-why', run('As price rises, quantity supplied will rise', '(ii) Outline two reasons'), 2,
               'Quantity supplied rises as price rises.')],
        figure=SOL + 'p29-q15ai-diagram')
pick('q15-a-ii', '1-2', 'why-electric-vehicles-cost-more-to-make', ref(15, '(a)(ii)'),
     H.ask(31, 'Outline two reasons for the current increase in the cost', ' 1. 2.'),
     'A reason costs are rising — any two',
     at('Shortage of computer chips', '⟨24⟩',
        ['Shortage of computer chips', 'Supply chain issues', 'Price of raw materials', 'Energy/electricity prices',
         'Wages', 'Transport costs']),
     2, 4, 'Two reasons, 4 marks each (2 + 2). Wages and transport costs are bare headings in the '
     'scheme.')
q15b_ask = H.ask(32, 'Demonstrate, with the aid of a fully labelled diagram', ' (i)')
for part, concept, ask_start, ask_end, sol, first, last, shift, last_note in [
        ('i', 'chargers-and-the-demand-for-evs', 'The Government’s decision to invest heavily', ' Diagram',
         'p30-q15bi-diagram', 'D/C shifts to the right', '(ii) Improvements and advances',
         'demand shifts right to D2', 'the new equilibrium quantity Q2'),
        ('ii', 'technology-and-the-supply-of-evs', 'Improvements and advances in the technology', ' Diagram',
         'p30-q15bii-diagram', 'S/C shifts to the right', '⟨28⟩',
         'supply shifts right to S2', 'the new equilibrium quantity Q2')]:
    points = [tidy(x) for x in run(first, last).split('•') if tidy(x)]
    assert len(points) == 4, (part, points)
    add(f'q15-b-{part}', '1-0', concept, ref(15, f'(b)({part})'),
        q15b_ask + ' ' + H.ask(32, ask_start, ask_end), '3 x 2 + 4 x 2', 14,
        [ask_row('r-diagram', 'Demonstrate, with the aid of a fully labelled diagram', 6,
                 f'The diagram, 6 marks: the scheme prints 3 × 2 beside its diagram, shown after you '
                 f'answer ({shift}, with the new price and quantity), and does not name the three '
                 f'elements.')]
        + [point(f'r-{i}', p, 2, note) for i, (p, note) in enumerate(zip(points, [
            f'The explanation, 4 × 2: one 2 for each point. {shift[0].upper()}{shift[1:]}.',
            'Why it shifts.', 'The new equilibrium price P2.', f'And {last_note}.']), 1)],
        figure=SOL + sol)
add('q15-c-i', '1-3', 'what-a-subsidy-is', ref(15, '(c)(i)'), H.ask(33, 'Explain the economic term subsidy.', ' Subsidy:'),
    '5', 5,
    [point('r-1', run('A subsidy is a direct or indirect payment', '(ii) Discuss one economic argument'), 5,
           'Explain the term, 5 marks: a direct or indirect payment, usually from the government, '
           'that reduces a business’s costs; the scheme’s example is the TWSS.')])
add('q15-c-ii', '1-3', 'the-case-for-and-against-a-subsidy', ref(15, '(c)(ii)'),
    H.ask(33, 'Discuss one economic argument in favour and one economic argument against', ' Argument'),
    '5 + 5', 10,
    [heading('r-for', 'An argument in favour — any one',
             menu('Lower prices for consumers - products', 'Against:', [31]), 5, 'In favour: one argument, 5 marks (2 + 3).'),
     heading('r-against', 'An argument against — any one',
             at('Opportunity cost - the money', '31 | P a g e',
                ['Opportunity cost - the money', 'Higher taxes - governments', 'Possible product shortages',
                 'Difficult to measure success']), 5, 'Against: one argument, 5 marks (2 + 3).')],
    kind='fixed')
pick('q15-c-iii', '1-3', 'why-governments-intervene-in-markets', ref(15, '(c)(iii)'),
     H.ask(34, 'Subsidies are one method governments use to intervene', ' 1. 2.'),
     'A reason to intervene, with an example — any two',
     menu('To prevent a market failure', '32 | P a g e', [32], trim='⟨23⟩'),
     2, 4, 'Two reasons, 4 marks each (2 + 2), each with an example other than subsidies.')

# Q16 ─ corporation tax; minimum pricing of alcohol; land
q16_stem = H.ask(35, 'The graph below shows Corporation Tax Receipts', ' Corporation Tax Receipts 2011')
pick('q16-a-i', '3-1', 'trends-in-corporation-tax-receipts', ref(16, '(a)(i)'),
     H.ask(35, 'Outline two key trends in corporation tax receipts', ' (ii)'),
     'A trend in corporation tax receipts — any two',
     at('Between 2011 and 2014', '(ii) Ireland’s Corporation Tax Rate',
        ['Between 2011 and 2014', 'Between 2014 and 2018', 'Between 2018 and 2020']),
     2, 4, 'Two trends, 4 marks each (2 + 2), each with its years and figures. The scheme writes '
     '€4m and €10m where the graph’s scale is € millions (about €4,000m and €10,000m).',
     stem=q16_stem, figure=PAP + 'p35-q16-chart')
add('q16-a-ii', '3-1', 'a-15-percent-corporation-tax', ref(16, '(a)(ii)'),
    H.ask(35, 'Ireland’s Corporation Tax Rate is set to rise to 15%', ' Adapted from') + ' '
    + H.ask(35, 'Outline one possible positive economic effect', ' One positive:'),
    '8 + 4', 12,
    [heading('r-positive', 'A positive effect — any one',
             menu('Effects on government revenue - firms who do remain', 'Negative:', [33, 34]), 8,
             'One positive effect, 8 marks (4 + 4). The scheme prints “1 x 8 (4+4)” and “1 x 4 (2+2)”; '
             'read in the order the paper asks and the scheme answers, the positive effect earns 8 '
             'and the negative 4.'),
     heading('r-negative', 'A negative effect — any one',
             menu('Difficulty in attracting new FDI', '(b) A new law came into effect', [34], drop=('⟨20⟩',)), 4,
             'One negative effect, 4 marks (2 + 2).')],
    kind='fixed')
q16b_stem = H.ask(36, 'A new law came into effect in Ireland in January 2022', ' Adapted from')
add('q16-b-i', '1-3', 'minimum-pricing-of-alcohol', ref(16, '(b)(i)'),
    H.ask(36, 'Explain, with the use of a fully labelled diagram, how the introduction of minimum pricing',
          ' Explanation:'), '9 + 6', 15,
    [ask_row('r-diagram', 'Explain, with the use of a fully labelled diagram', 9,
             'The diagram, 9 marks: the scheme’s, shown after you answer, sets Pmin above the '
             'equilibrium PE, with QD, QE and QS on the quantity axis.'),
     anyN('r-explanation', 'An effect of the minimum price — any two', 6, 2, 3,
          at('Effect on price', '(ii) Per capita alcohol',
             ['Effect on price', 'Effect on demand', 'Effect on market']),
          'The explanation, 6 marks. The scheme prints “6 (2 x 3)” beside three effects: any two, 3 '
          'marks each.')],
    stem=q16b_stem, figure=SOL + 'p34-q16bi-diagram')
pick('q16-b-ii', '1-3', 'cutting-alcohol-consumption-without-price', ref(16, '(b)(ii)'),
     H.ask(37, 'Suggest two strategies, other than minimum pricing and taxation', ' 1. 2.'),
     'A strategy to reduce alcohol consumption — any two',
     menu('Education – the government', '(iii) The per capita consumption', [35]),
     2, 5, 'Two strategies, 5 marks each (2 + 3).',
     stem=H.ask(37, 'Per capita alcohol consumption in Ireland was 10.78 litres', ' Adapted from'))
pick('q16-b-iii', '2-2', 'social-costs-of-alcohol', ref(16, '(b)(iii)'),
     H.ask(37, 'The per capita consumption rate of alcohol in Ireland may involve social costs.', ' 1. 2.'),
     'A social cost — any two',
     at('Health care – a big social cost', '⟨33⟩',
        ['Health care – a big social cost', 'Social problems in society', 'Workplace productivity',
         'Car accidents and deaths']),
     2, 4, 'Two social costs, 4 marks each (2 + 2).')
q16c_stem = H.ask(37, 'The demand for land is referred to as a derived demand.', ' (i)')
add('q16-c-i', '1-1', 'derived-demand-for-land', ref(16, '(c)(i)'),
    H.ask(37, 'Explain the term derived demand with reference to the factor of production land.', ' Derived'),
    '4', 4,
    [point('r-1', run('Derived demand means that a factor of production', '(ii) Explain two unique'), 4,
           'Explain the term, 4 marks: land is demanded for what it helps produce, so its demand rises '
           'with the demand for housing or crops.')],
    stem=q16c_stem)
pick('q16-c-ii', '1-2', 'characteristics-of-land', ref(16, '(c)(ii)'),
     H.ask(38, 'Explain two unique characteristics of land as a factor of production.', ' 1. 2.'),
     'A characteristic of land — any two',
     menu('Land is fixed in supply - an increase', '(iii) Explain, with the use', [36]),
     2, 5, 'Two characteristics, 5 marks each (3 + 2).', stem=q16c_stem)
add('q16-c-iii', '1-0', 'the-market-for-land', ref(16, '(c)(iii)'),
    H.ask(38, 'Explain, with the use of a fully labelled diagram, the demand and supply curve for land.', ' Explanation:'),
    '4 x 1 + 2 + 2', 8,
    [ask_row('r-diagram', 'Explain, with the use of a fully labelled diagram, the demand and supply curve for land.', 4,
             'The diagram, 4 × 1: the scheme’s, shown after you answer, labels Price, Quantity, a '
             'vertical S and a falling D meeting it at P1.'),
     point('r-supply', run('Land is fixed in supply which means', 'The demand for land is a derived'), 2,
           'Supply, 2 marks: fixed, a vertical line.'),
     point('r-demand', run('The demand for land is a derived demand and is downward', '⟨22⟩'), 2,
           'Demand, 2 marks: derived, sloping down.')],
    stem=q16c_stem, figure=SOL + 'p36-q16ciii-diagram')


if __name__ == '__main__':
    emit(cards)
