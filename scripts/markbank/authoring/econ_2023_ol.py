#!/usr/bin/env python3
"""Economics 2023 Ordinary Level, Sections A and B.

Re-authored from the independent census in drafts/economics-2023-ol-ev.json,
made from a visual sweep of all 32 paper pages and 32 scheme pages. Every card
ID the earlier extractors shipped is kept (student progress follows the ID), and
the 61 routes are the ones the 2023 Ordinary Irish review mirrors task for task,
so the Irish attachment is unchanged.

Question wording and stems are sliced from the question paper; every marking
point is sliced from the scheme (econ_2026_lib.py). Ordinary Level sets its
responses as a bullet list, so menus are split at the bullets. The only prose
written here is guidance: tariffs, route labels and what a figure or a
calculation shows. Scheme PDF page = printed page + 2.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from econ_2026_lib import Deck, Sheet, show_before_reveal  # noqa: E402
from econ_lib import anyN, as_option, block, bullets, defurnish, emit, heads, point  # noqa: E402

O = Sheet(2023, 'ordinary', 'LC034GLP000EV')
D = Deck(2023, 'ordinary')
cards, add, pick, heading, ref = D.cards, D.add, D.pick, D.heading, D.ref
A = dict(section='A')
SOL = 'economics-2023-OL-scheme-'
PAP = 'economics-2023-OL-paper-'
EITHER = 'Answer either (a) or (b).'


def bl(start, end, occ=None):
    """The scheme's bullet-listed responses between two anchors."""
    return bullets(O.chunk(start, end, occ))


def items(start, end):
    """A bullet list of one- or two-word answers, which bullets() sets aside as
    too short to be a response ("Transport.", "Social.")."""
    return [as_option(x) for x in re.split(r'\s*•\s*', defurnish(O.chunk(start, end))) if x.strip()]


def at(start, end, firsts, occ=None):
    """Responses printed as plain sentences, split where each one begins."""
    return [as_option(o) for o in heads(O.chunk(start, end, occ), firsts)]


def cell(start, end, occ=None):
    """One cell of a scheme table, from the recovered table-cell block."""
    return as_option(defurnish(block(O.full_md, start, end, occ)))


def paras(options):
    """A list of the scheme's examples printed as one marking point."""
    return '\n\n'.join(options)


def shared(rid, label, options, note):
    """A required answer inside a jointly priced response (1st @ n, 2nd @ m).

    One unpriced point carrying its examples: a per-option price here would
    print "n marks each" for a share the scheme never fixes.
    """
    return point(rid, paras(options), None, f'{label}. {note}')


def steps(rid, label, options, first, second, what):
    """Two responses paid first-then-second (1st @ 8, 2nd @ 4)."""
    return anyN(rid, label, None, 2, first, options,
                f'Two {what}: the first correct one {first} marks and the second {second}.',
                steps=[first, second])


# ═════════════════════════════════ SECTION A ══════════════════════════════════

# Q1 ─ unemployment rate
q1_stem = O.ask(3, 'The graph below shows the unemployment rate for Ireland', ' Seasonally')
add('sa-q1-i', '3-2', 'reading-the-lowest-month-off-an-unemployment-chart', ref(1, '(i)', sa=True),
    O.ask(3, 'Identify the month when unemployment was at its lowest.', ' (ii)'), '8', 8,
    [point('r-1', O.run('July 2022 ⟨8⟩', '(ii) Comment on the unemployment rate'), 8,
           'July 2022, the first month on the chart, at 4.3%, 8 marks. Give the month, not the rate: '
           'the line later falls from 4.5% back to 4.4% but never below July’s figure.')],
    stem=q1_stem, figure=PAP + 'p03-i0', **A)
pick('seca-q1-ii', '3-2', 'commenting-on-the-unemployment-rate', ref(1, '(ii)', sa=True),
     O.ask(3, 'Comment on the unemployment rate between July 2022', ' Comment:'),
     'A comment using the chart’s figures — either approach',
     at('Overall trend', '3 | P a g e', ['Overall trend', 'Monthly trends']),
     1, 4, 'One comment with figures, 4 marks: the overall move from 4.3% to 4.4% (a rise of 0.1 '
     'percentage point), or the month-by-month path, which rises, holds, peaks at 4.5% and dips back.',
     stem=q1_stem, figure=PAP + 'p03-i0', **A)

# Q2 ─ banks leaving the market; the Central Bank
q2_stem = O.ask(4, 'In 2021, KBC Bank and Ulster Bank announced', ' Adapted from')
add('sa-q2-a', '3-4', 'effects-of-banks-exiting-the-market', ref(2, '(a)', sa=True),
    O.ask(4, 'Outline two effects on the Irish consumer of KBC Bank', ' 1. 2.'), '8 + 4', 12,
    [steps('r-1', 'An effect on the Irish consumer — any two',
           bl('• Less choice for the consumer', 'OR\n(b) Outline two functions'), 8, 4, 'effects')],
    stem=q2_stem, notes=EITHER, **A)
add('sa-q2-b', '3-4', 'functions-of-the-central-bank-ol', ref(2, '(b)', sa=True),
    O.ask(4, 'Outline two functions of the Central Bank of Ireland.', ' 1. 2.'), '8 + 4', 12,
    [steps('r-1', 'A function of the Central Bank — any two',
           bl('• Acts as the Government’s Bank.', '4 | P a g e'), 8, 4, 'functions')],
    stem=q2_stem, notes=EITHER, **A)

# Q3 ─ the skills shortage
q3_stem = O.ask(5, 'There are loads of job vacancies in Ireland', ' Adapted from')
pick('sa-q3-a-i', '2-1', 'areas-of-skills-shortage', ref(3, '(a)(i)', sa=True),
     O.ask(5, 'Identify one area where the Irish economy is experiencing', ' (ii)'),
     'An area short of skills — any one',
     items('• Hospitality sector.', '(ii) Outline one economic effect'),
     1, 8, 'One area, 8 marks. These are the scheme’s examples, not a closed list.',
     stem=q3_stem, notes=EITHER, **A)
pick('sa-q3-a-ii', '2-1', 'effects-of-a-skills-shortage', ref(3, '(a)(ii)', sa=True),
     O.ask(5, 'Outline one economic effect of a skilled labour shortage', ' One area:'),
     'An economic effect of the shortage — any one',
     bl('• Wages could increase to attract workers', 'OR\n(b) Outline two measures'),
     1, 4, 'One developed effect, 4 marks.', stem=q3_stem, notes=EITHER, **A)
add('sa-q3-b', '2-1', 'measures-to-address-a-labour-shortage', ref(3, '(b)', sa=True),
    O.ask(5, 'Outline two measures the Irish government could take', ' 1. 2.'), '8 + 4', 12,
    [steps('r-1', 'A measure to address the shortage — any two',
           bl('• Increase in the minimum wage', '5 | P a g e'), 8, 4, 'measures')],
    stem=q3_stem, notes=EITHER, **A)

# Q4 ─ monopoly
add('seca-q4-a-i', '2-0', 'which-irish-firm-is-a-monopoly', ref(4, '(a)(i)', sa=True),
    O.ask(6, 'Identify, with a tick (✓), which one of the following firms', ' Name of Organisation'), '8', 8,
    [point('r-1', 'Iarnród Eireann (Irish Rail)', 8,
           'Tick IARNRÓD ÉIREANN (IRISH RAIL), 8 marks: the sole provider of rail services in the '
           'State. Aer Lingus competes with other airlines and VHI with other health insurers.')],
    figure=PAP + 'p06-i0', notes=EITHER, **A)
add('sa-q4-a-ii', '2-0', 'what-a-monopoly-is', ref(4, '(a)(ii)', sa=True),
    O.ask(6, 'Explain the term monopoly in economics.', ' OR'), '4', 4,
    [point('r-1', O.run('A monopoly exists when there is only one firm', 'OR\n(b) Outline two characteristics'), 4,
           'Explain the term, 4 marks: one firm is the whole industry, the sole supplier, and it can set '
           'the price or the quantity but not both.')],
    notes=EITHER, **A)
add('sa-q4-b', '2-0', 'characteristics-of-a-monopoly', ref(4, '(b)', sa=True),
    O.ask(6, 'Outline two characteristics of a monopoly market.', ' 1. 2.'), '8 + 4', 12,
    [steps('r-1', 'A characteristic of a monopoly — any two',
           bl('• One seller – the firm is the industry.', '6 | P a g e'), 8, 4, 'characteristics')],
    notes=EITHER, **A)

# Q5 ─ Rugby World Cup tickets
add('sa-q5', '1-2', 'fixed-supply-of-tickets', ref(5, sa=True),
    O.ask(7, 'The diagram below represents the supply of tickets', ' Explanation:'), '12', 12,
    [point('r-1', O.run('The supply of tickets for the Rugby World Cup is fixed', '6. Ireland’s GDP'), 12,
           'Explain the relationship, 12 marks: the vertical S1 means the number of tickets is fixed, '
           'so the quantity supplied does not respond to price at all (perfectly inelastic supply).')],
    figure=PAP + 'p07-q5-diagram', **A)

# Q6 ─ GDP
q6_stem = O.ask(7, 'Ireland’s GDP is predicted to increase by 2.7% in 2023.', ' Adapted from')
add('sa-q6-i', '3-0', 'what-gdp-stands-for', ref(6, '(i)', sa=True),
    O.ask(7, 'What do the initials GDP stand for?', ' Gross D P'), '2 @ 4', 8,
    [point('r-d', 'DOMESTIC', 4, 'D___: Domestic, 4 marks. Gross is printed.'),
     point('r-p', 'PRODUCT', 4, 'P___: Product, 4 marks.')],
    stem=q6_stem, **A)
pick('sa-q6-ii', '3-5', 'advantages-of-rising-gdp', ref(6, '(ii)', sa=True),
     O.ask(7, 'Outline one advantage of an increasing GDP', ' Leaving'),
     'An advantage of a rising GDP — any one',
     bl('• Increased demand for goods and services in Ireland.', '7 | P a g e'),
     1, 4, 'One developed advantage, 4 marks.', stem=q6_stem, **A)

# Q7 ─ why the government collects tax
add('sa-q7', '3-1', 'why-a-government-collects-tax', ref(7, sa=True),
    O.ask(8, 'Explain two reasons why the government in Ireland collects tax.', ' 1. 2.'), '8 + 4', 12,
    [steps('r-1', 'A reason the government collects tax — any two',
           bl('• To fund / help improve / pay for state services', '8. Ireland ranks second'), 8, 4,
           'reasons')],
    stem=O.ask(8, 'Corporation tax receipts in Ireland rose', ' Adapted from'), **A)

# Q8 ─ the Human Development Index
q8_stem = O.ask(8, 'Ireland ranks eighth highest in the world', ' (i)')
add('sa-q8-i', '4-0', 'elements-of-the-hdi', ref(8, '(i)', sa=True),
    O.ask(8, 'Name two of the three areas (elements)', ' 1. Gross National Income'), '6', 6,
    [point('r-1', 'EDUCATION', None, 'Education. Gross National Income is completed on the paper.'),
     point('r-2', 'LIFE EXPECTANCY', None,
           'Life expectancy. Both are needed: the scheme prices the two together as one 6, the first '
           'correct answer 4 marks and the second 2.')],
    kind='questionTotal', stem=q8_stem, **A)
add('sa-q8-ii', '4-0', 'expenditure-behind-irelands-hdi', ref(8, '(ii)', sa=True),
    O.ask(8, 'In your opinion, what area of government expenditure', ' Area of expenditure:'), '6', 6,
    [point('r-area', 'Education', None,
           'Area of expenditure: the scheme names education. The question asks for your opinion, so '
           'another area argued on its merits can earn the marks.'),
     point('r-explanation', O.run('An educated workforce is able to gain employment.', '8 | P a g e'), None,
           'Explain how that spending lifted Ireland’s HDI. The scheme prices the area and the '
           'explanation together as one 6: the first correct element 4 marks and the second 2. The '
           'scheme writes “second” where the paper says eighth.')],
    kind='questionTotal', stem=q8_stem, **A)

# Q9 ─ opportunity cost
add('sa-q9', '0-1', 'opportunity-cost-and-housing-spend', ref(9, sa=True),
    O.ask(9, 'Explain the term opportunity cost.', ' Explanation:') + ' '
    + O.ask(9, 'Capital funding of €2.3bn has been allocated', ' Outline:'), '12', 12,
    [shared('r-definition', 'Explain opportunity cost',
            bl('• The cost of the foregone alternatives', '(ii) Capital funding'),
            'Complete BOTH parts. The scheme prices (i) and (ii) together as one 12: the first correct '
            'answer 8 marks and the second 4, with no fixed share for either part.'),
     shared('r-application', 'One opportunity cost of the housing spend',
            [O.run('The Irish government could have spent the money', '10. The government')],
            'Name the next-best use of the €2.3bn forgone.')],
    kind='questionTotal', **A)

# Q10 ─ vaping
add('sa-q10-private', '0-1', 'private-and-social-benefits-of-reducing-vaping', ref(10, sa=True),
    O.ask(9, 'The government is currently looking to reduce the vaping', ' Private benefit:'), '12', 12,
    [shared('r-private', 'One private benefit',
            bl('• Teenagers will have more disposable income.', 'Social benefit:'),
            'Give one private benefit AND one social benefit. The scheme prices the two together as one '
            '12: the first correct benefit 8 marks and the second 4, with no fixed share for either.'),
     shared('r-social', 'One social benefit', bl('• Healthier young population.', '9 | P a g e'),
            'A benefit to society as a whole.')],
    kind='questionTotal', **A)


# ═════════════════════════════════ SECTION B ══════════════════════════════════

# Q11 ─ hair and beauty: monopolistic competition; the hidden economy
q11_stem = O.ask(10, 'The hair and beauty industries in Ireland are an example', ' Adapted from')
add('q11-a-i', '2-0', 'monopolistic-competition-identified', ref(11, '(a)(i)'),
    O.ask(10, 'Outline two reasons why, in your opinion the hair and beauty', ' 1. 2.'), '6 + 4', 10,
    [steps('r-1', 'A reason it is monopolistic competition — any two',
           bl('• There are many firms in the industry', '(ii) Outline two advantages'), 6, 4, 'reasons')],
    stem=q11_stem, figure=PAP + 'p10-i0')
add('q11-a-ii', '2-0', 'monopolistic-competition-consumer-advantages', ref(11, '(a)(ii)'),
    O.ask(10, 'Outline two advantages for consumers of monopolistic competition.', ' 1. 2.'), '6 + 4', 10,
    [steps('r-1', 'An advantage for consumers — any two',
           bl('• Consumers benefit from increased choice.', '10 | P a g e'), 6, 4, 'advantages')],
    stem=q11_stem)
q11b_stem = O.ask(11, 'The diagram below represents the long run equilibrium', ' (i)')
q11b_fig = PAP + 'p11-q11b-diagram'
c = add('q11-b-i', '2-0', 'labelling-monopolistic-competition', ref(11, '(b)(i)'),
        O.ask(11, 'Write out in full what each of the three numbered items', ' 1. 2. 3.'), '3 @ 8', 24,
        [point('r-1', 'AVERAGE COST', 8, 'Item 1, the U-shaped curve with W at its lowest point, 8 marks.'),
         point('r-2', 'AVERAGE REVENUE / DEMAND', 8, 'Item 2, the downward-sloping line, 8 marks.'),
         point('r-3', 'QUANTITY', 8,
               'Item 3, the horizontal axis, 8 marks. Write each in full: the paper rules out '
               'abbreviations.')],
        stem=q11b_stem, figure=q11b_fig)
c['labelKey'] = [{'letter': '1', 'meaning': 'Average cost', 'askedInThisQuestion': True},
                 {'letter': '2', 'meaning': 'Average revenue / demand', 'askedInThisQuestion': True},
                 {'letter': '3', 'meaning': 'Quantity', 'askedInThisQuestion': True},
                 {'letter': 'MC', 'meaning': 'Marginal cost', 'askedInThisQuestion': False},
                 {'letter': 'MR', 'meaning': 'Marginal revenue', 'askedInThisQuestion': False}]
add('q11-b-ii', '2-0', 'marking-output-price-and-cost-at-long-run-equilibrium', ref(11, '(b)(ii)'),
    O.ask(11, 'Equilibrium occurs at point E on the diagram above.', ' (iii)'), '9', 9,
    [point('r-q1', 'Q1', None, 'Q1: drop a line from E, where MC cuts MR, to the quantity axis.'),
     point('r-p1', 'P1', None,
           'P1: from Q1 go up to the average revenue / demand curve, then across to the price axis.'),
     point('r-c1', 'C1', None,
           'C1: in long-run equilibrium the average cost curve just touches the demand curve above Q1, '
           'so C1 is the same point as P1 (normal profit only). The scheme gives 9 for the three '
           'labels, the first correct 4, the second 4 and the third 1; the official diagram is shown '
           'in the figure.')],
    kind='questionTotal', stem=q11b_stem, figure=SOL + 'p13-q11bii-equilibrium')
add('q11-b-iii', '2-0', 'efficiency-in-monopolistic-competition', ref(11, '(b)(iii)'),
    O.ask(11, 'Is the above firm producing efficiently?', ' Reason:'), '1 + 1', 2,
    [point('r-choice', 'No.', 1, 'Tick NO, 1 mark: the scheme credits no Yes answer.'),
     point('r-reason', O.run('The firm is not producing at the minimum point', '(c) The hidden economy'), 1,
           'The reason, 1 mark: equilibrium output is to the left of W, the lowest point of average '
           'cost.')],
    stem=q11b_stem, figure=q11b_fig)
q11c_stem = (O.ask(12, 'The hidden economy in the hair & beauty market', ' Adapted from') + ' '
             + O.ask(12, 'The Irish government is concerned about the size', ' (i)'))
add('q11-c-i', '3-0', 'what-the-hidden-economy-is-ol', ref(11, '(c)(i)'),
    O.ask(12, 'Explain the term hidden economy.', ' Explanation:'), '6 + 4', 10,
    [heading('r-definition', 'The hidden economy — any wording',
             bl('• The hidden economy refers to all economic activity', 'Give one other example'), 6,
             'Explain the term, 6 marks.'),
     point('r-example', O.run('Sale of cigarettes on the black market.', '(ii) Outline one effect'), 4,
           'One OTHER activity in the Irish hidden economy, 4 marks; the scheme gives these two.')],
    stem=q11c_stem)
add('q11-c-ii', '3-0', 'effects-of-the-hidden-economy-ol', ref(11, '(c)(ii)'),
    O.ask(12, 'Outline one effect the hidden economy in the hair and beauty industry', ' Businesses in'),
    '10', 10,
    [shared('r-business', 'One effect on businesses in this industry',
            bl('• Loss of income to the firms that are in the legitimate', 'Effect of hidden economy on the Irish government:'),
            'Complete BOTH headings. The scheme prices the two together as one 10: the first correct '
            'effect 6 marks and the second 4, with no fixed share for either.'),
     shared('r-government', 'One effect on the Irish government',
            bl('• Loss of revenue to the state in unpaid taxes.', '12 | P a g e'),
            'An effect on the state.')],
    kind='questionTotal', stem=q11c_stem)

# Q12 ─ government revenue; tax principles; the electricity credit
q12a_stem = O.ask(13, 'The government planned revenue for 2023', ' Budget Planned')
add('q12-a-i', '3-1', 'total-planned-government-revenue', ref(12, '(a)(i)'),
    O.ask(13, 'Using the figures in the pie chart above, calculate', ' Workings:'), '6 @ 2 + 4', 16,
    [point('r-total', O.run('€27.5m + €14m + €17m', 'Deduct 1 mark each'), 16,
           'Add all six slices, including the €2m and €7m ones: €27.5m + €14m + €17m + €27.5m + €2m + '
           '€7m = €95 million. Six figures at 2 marks and the answer 4. Deduct 1 each for omission '
           'of € and million.')],
    stem=q12a_stem, figure=PAP + 'p13-i0')
add('q12-a-ii', '3-1', 'income-tax-as-a-share-of-revenue', ref(12, '(a)(ii)'),
    O.ask(13, 'Using your answer from (i) above calculate', ' Workings:'), '4 @ 3', 12,
    [point('r-share', O.run('€27.5m / €95m x 100', 'Deduct 1 mark for omission'), 12,
           'Income tax share = 27.5 ÷ 95 × 100 = 28.94%, or 29% rounded, using the €95m total from '
           '(i). Four steps at 3 marks; deduct 1 if % is omitted.')],
    stem=q12a_stem, figure=PAP + 'p13-i0')
add('q12-b-i', '3-1', 'equity-in-taxation', ref(12, '(b)(i)'),
    O.ask(14, 'Equity is one of the principles of a good tax system.', ' Explanation:'), '8', 8,
    [point('r-1', O.run('This means the more income you earn', '(ii) Explain two other principles'), 8,
           'Explain the term, 8 marks: tax is charged according to ability to pay.')])
add('q12-b-ii', '3-1', 'principles-of-a-good-tax-system', ref(12, '(b)(ii)'),
    O.ask(14, 'Explain two other principles of a good tax system', ' 1. 2.'), '8 + 4', 12,
    [steps('r-1', 'Another principle of a good tax system — any two',
           bl('• A good tax system should not be a disincentive', '(c) As part of Budget'), 8, 4,
           'principles other than equity')])
q12c_stem = O.ask(14, 'As part of Budget 2023 the government have announced', ' Adapted from')
pick('q12-c-i', '1-3', 'benefit-of-the-electricity-credit', ref(12, '(c)(i)'),
     O.ask(14, 'Outline one benefit of this electricity credit', ' Benefit:'),
     'A benefit to the household — any one',
     bl('• It helps Irish households to maintain their standard', '(ii) Describe two actions'),
     1, 10, 'One developed benefit, 10 marks.', stem=q12c_stem)
add('q12-c-ii', '0-2', 'household-actions-to-cut-electricity-use', ref(12, '(c)(ii)'),
    O.ask(15, 'Describe two actions an Irish household could take', ' 1. 2.'), '10 + 4', 14,
    [steps('r-1', 'An action the household could take — any two',
           bl('• The Irish household could reduce their consumption', '(iii) Name the three pillars'),
           10, 4, 'actions')],
    stem=q12c_stem)
add('q12-c-iii', '0-2', 'three-pillars-of-sustainability', ref(12, '(c)(iii)'),
    O.ask(15, 'Name the three pillars of sustainability.', ' 1. 2. 3.'), '3', 3,
    [point(f'r-{i}', name, None, note) for i, (name, note) in enumerate(zip(
        items('• Economic.', '14 | P a g e'),
        ['The economic pillar.', 'The environmental pillar.',
         'The social pillar. The scheme gives 3 for the three names, with no published split.']), 1)],
    kind='questionTotal')

# Q13 ─ food and drink exports; national income; interest rates
add('q13-a-i', '4-2', 'highest-and-lowest-years-for-food-and-drink-exports', ref(13, '(a)(i)'),
    O.ask(16, 'Using the bar chart above, answer the following questions.', ' (ii)'), '12', 12,
    [point('r-highest', O.run('2019 1st@ 8', 'State the year with the lowest'), None,
           'Highest: 2019, at €13.85bn.'),
     point('r-lowest', '2016', None,
           'Lowest: 2016, at €10.6bn. The scheme prices the two together as one 12: the first correct '
           'answer 8 marks and the second 4.')],
    kind='questionTotal',
    stem=O.ask(16, 'The bar chart below shows the expected value', ' Value of food'), figure=PAP + 'p16-art')
add('q13-a-ii', '4-2', 'advantages-of-exports', ref(13, '(a)(ii)'),
    O.ask(16, 'Describe two advantages of exports for the Irish economy.', ' 1. 2.'), '8 + 2', 10,
    [steps('r-1', 'An advantage of exports — any two',
           bl('• Increased national income:', '15 | P a g e'), 8, 2, 'advantages')])
q13b_stem = O.ask(17, 'National Income is calculated using the following formula:', ' (i)')
q13b_ask = O.ask(17, 'Using the formula in (i) above and the figures below calculate:', ' •')
q13b_work = O.ask(17, 'Show your workings', ' Year')
add('q13-b-i', '3-0', 'letters-in-the-national-income-formula', ref(13, '(b)(i)'),
    O.ask(17, 'State what each of the letters C and G represent.', ' C G'), '2 @ 4', 8,
    [point('r-c', 'Consumption expenditure.', 4, 'C: consumption, spending by households, 4 marks.'),
     point('r-g', 'Government expenditure.', 4, 'G: government spending, 4 marks.')],
    stem=q13b_stem)
add('q13-b-ii', '3-0', 'calculate-national-income', ref(13, '(b)(ii)', 'national income'),
    q13b_ask + ' ' + O.ask(17, 'The level of National Income in 2023', ' and •') + ' ' + q13b_work, '6 @ 3', 18,
    [point('r-income', O.run('Y = C + I + G + (X-M)', 'Deduct 1 mark each for omission', occ=0), 18,
           'Y = C + I + G + (X − M) = €700m + €200m + €400m + €300m − €200m = €1,400m. Imports are '
           'subtracted. Six steps at 3 marks; deduct 1 each for omission of € and million.')],
    stem=q13b_stem, figure=PAP + 'p17-i1')
add('q13-b-ii-trade', '4-2', 'calculate-balance-of-trade', ref(13, '(b)(ii)', 'balance of trade'),
    q13b_ask + ' ' + O.ask(17, 'The Balance of Trade', ' Show') + ' ' + q13b_work, '3 @ 3', 9,
    [point('r-trade', O.run('Balance of Trade: ⟨9⟩', 'Deduct 1 mark each for omission', occ=0), 9,
           'Balance of trade = exports − imports = €300m − €200m = €100m. Consumption, investment and '
           'government spending play no part. Three steps at 3 marks; deduct 1 each for omission of € '
           'and million.')],
    stem=q13b_stem, figure=PAP + 'p17-i1')
q13c_stem = O.ask(18, 'When the European Central Bank (ECB) implemented', ' Adapted from')
pick('q13-c-i', '3-3', 'interest-rates-and-mortgage-holders', ref(13, '(c)(i)'),
     O.ask(18, 'Explain how this increase in interest rates would affect consumers', ' Explanation:'),
     'An effect on mortgage holders — any one',
     bl('• Increased monthly repayments on mortgages:', '(ii) Outline how the increase'),
     1, 8, 'One developed effect, 8 marks.', stem=q13c_stem)
pick('q13-c-ii', '3-3', 'interest-rates-and-saving', ref(13, '(c)(ii)'),
     O.ask(18, 'Outline how the increase in interest rates could affect savings', ' Outline:'),
     'An effect on savings — any one',
     bl('• Savings could increase if people spend less', '(iii) Outline one reason why consumers'),
     1, 8, 'One developed effect, 8 marks. The scheme accepts savings rising, falling or not changing; '
     'the reasoning earns the marks.', stem=q13c_stem)
pick('q13-c-iii', '3-4', 'why-consumers-switch-bank', ref(13, '(c)(iii)'),
     O.ask(18, 'Outline one reason why consumers are switching', ' Outline:'),
     'A reason consumers are switching — any one',
     bl('• The consumer has one place to deal with all money', '17 | P a g e'),
     1, 2, 'One reason, 2 marks.', stem=q13c_stem)

# Q14 ─ petrol prices; revenue and profit; costs
q14_stem = O.ask(19, 'The line graph below shows changes in the price of petrol', ' Petrol Prices')
q14_fig = PAP + 'p19-q14-chart'
pick('q14-a-i', '3-3', 'trend-in-petrol-prices', ref(14, '(a)(i)'),
     O.ask(19, 'Comment on one key trend in the price of petrol', ' Comment:'),
     'One key trend, with figures from the graph — either one',
     at('From April to June 2022, petrol prices', '(ii) Outline one reason why the price',
        ['From April to June 2022', 'From June 2022 to September 2022']),
     1, 10, 'One trend with figures, 10 marks: the scheme writes it (6+4), the trend and the figures '
     'that support it. The graph is in cent, so 180 is €1.80 and 210 is €2.10.',
     stem=q14_stem, figure=q14_fig)
add('q14-a-ii-reason', '3-3', 'petrol-price-rise-cause-and-consumer-effect', ref(14, '(a)(ii)'),
    O.ask(19, 'Outline one reason why the price of petrol changed', ' One reason:'), '12', 12,
    [shared('r-reason', 'One reason the price changed',
            at('The easing of restrictions following lockdowns', 'Effect:',
               ['The easing of restrictions', 'However, the sharp increase']),
            'Give a reason AND an effect. The scheme prices the two together as one 12: the first '
            'correct answer 8 marks and the second 4, with no fixed share for either.'),
     shared('r-effect', 'One effect on Irish consumers',
            [O.run('The increase in petrol prices leads to consumers', '18 | P a g e')],
            'Explain the effect on consumers.')],
    kind='questionTotal', stem=q14_stem, figure=q14_fig)
q14b_stem = O.ask(20, 'The table below shows the output, total cost', ' Output (Units)')
add('q14-b-i', '1-5', 'total-revenue-from-price-and-quantity', ref(14, '(b)(i)'),
    O.ask(20, 'Calculate the total revenue if the firm sells 400 units.', ' Workings:'), '3 @ 6', 18,
    [point('r-revenue', O.run('Total revenue = Price x Quantity', 'Deduct 1 for omission', occ=0), 18,
           'Total revenue = price × quantity = €15 × 400 = €6,000. Three steps at 6 marks; deduct 1 if '
           'the € is omitted.')],
    stem=q14b_stem, figure=PAP + 'p20-i0')
add('q14-b-ii', '1-5', 'profit-from-total-revenue-and-total-cost', ref(14, '(b)(ii)'),
    O.ask(20, 'Calculate the profit earned when the firm sells 400 units.', ' Workings:'), '3 @ 3', 9,
    [point('r-profit', O.run('Profit = Total revenue – Total cost', 'Deduct 1 for omission', occ=0), 9,
           'Profit = total revenue − total cost = €6,000 − €4,500 = €1,500, the revenue carried from (i) '
           'and the cost read from the table. Three steps at 3 marks; deduct 1 if the € is omitted.')],
    stem=q14b_stem, figure=PAP + 'p20-i0')
pick('q14-b-iii', '1-2', 'why-a-global-parts-shortage', ref(14, '(b)(iii)'),
     O.ask(20, 'A shortage of parts for making electronic devices', ' Explanation:'),
     'A reason for the shortage — any one',
     bl('• Interruption to the supply chain', '19 | P a g e'),
     1, 3, 'One reason, 3 marks.')
add('q14-c-i', '1-5', 'fixed-and-variable-costs', ref(14, '(c)(i)'),
    O.ask(21, 'Explain the terms fixed costs and variable costs', ' Fixed Costs:'), '6 + 3 + 6 + 3', 18,
    [point('r-fixed', O.run('Fixed costs: costs which remain the same', 'Examples: rent'), 6,
           'Explain fixed costs, 6 marks: they do not change with output and are paid even at zero '
           'output.'),
     point('r-fixed-example', O.run('Examples: rent of premises', 'Variable costs:'), 3,
           'One example of a fixed cost, 3 marks.'),
     point('r-variable', O.run('Variable costs: costs which vary with output', 'Examples: raw'), 6,
           'Explain variable costs, 6 marks: they rise as output rises.'),
     point('r-variable-example', O.run('Examples: raw materials', '(ii) Outline one reason why it is'), 3,
           'One example of a variable cost, 3 marks.')])
pick('q14-c-ii', '1-5', 'why-profit-matters', ref(14, '(c)(ii)'),
     O.ask(21, 'Outline one reason why it is important for a business', ' 75 marks'),
     'A reason profit matters in the long run — any one',
     bl('• Continue production:', '20 | P a g e'),
     1, 5, 'One developed reason, 5 marks.')

# Q15 ─ vehicle licensing; demand for electric cars; EV incentives
add('q15-a-i-percentage', '1-1', 'private-cars-as-a-share-of-vehicles-licensed', ref(15, '(a)(i)'),
    O.ask(22, 'Using the information in the table above, calculate', ' Workings:'), '5 @ 4', 20,
    [point('r-answer', '81.32%', 20,
           'Add both private-car rows before dividing: (101,853 + 68,042) ÷ 208,913 × 100 = 81.32%. '
           'Five steps at 4 marks; deduct 1 if % is omitted.')],
    stem=O.ask(22, 'The infographic below details the number of vehicles', ' TOTAL'), figure=PAP + 'p22-i0')
add('q15-a-ii', '1-3', 'subsidising-public-transport', ref(15, '(a)(ii)'),
    O.ask(22, 'The Irish government are currently subsiding the users', ' Subsidy:'), '5', 5,
    [point('r-1', O.run('The Irish government is paying part of the cost', '21 | P a g e'), 5,
           'Explain the term, 5 marks: the government pays part of the cost of each journey, so the '
           'fare the user pays is lower.')])
q15b_sol = SOL + 'p24-q15b-diagram'
add('q15-b-i', '1-1', 'drawing-a-labelled-market-demand-curve', ref(15, '(b)(i)'),
    O.ask(23, 'Draw and label (include the axes) the market demand curve', ' (ii)'), '4 @ 4', 16,
    [point('r-price', 'Price', None, 'Label the vertical axis Price.'),
     point('r-quantity', 'Quantity', None, 'Label the horizontal axis Quantity.'),
     point('r-curve', 'D', None,
           'Draw the demand curve sloping down from left to right and label it D. The scheme gives '
           '4 @ 4 for the diagram without naming the four elements; its official diagram, which also '
           'shows the D2 asked in (ii), is shown in the figure.')],
    kind='questionTotal', figure=q15b_sol)
add('q15-b-ii', '1-1', 'shifting-demand-when-incomes-rise', ref(15, '(b)(ii)'),
    O.ask(23, 'If consumers income increases, show how this would affect', ' Explanation:'), '6 + 3', 9,
    [point('r-shift', 'The demand curve shifts to the right.', 6,
           'Show it, 6 marks: draw D2 to the right of D. Income is not the car’s own price, so the '
           'whole curve shifts rather than a movement along it.'),
     point('r-explanation', 'Consumers can afford to buy more.', 3,
           'Explain, 3 marks: with more income consumers demand more at every price.')],
    figure=q15b_sol)
pick('q15-b-iii', '1-1', 'what-shifts-demand-for-electric-cars', ref(15, '(b)(iii)'),
     O.ask(23, 'Explain one factor, other than an increase in income', ' Explanation:'),
     'A factor affecting demand — any one',
     bl('• Change in consumer tastes or preference', '22 | P a g e'),
     1, 5, 'One developed factor, 5 marks.')
q15c_stem = O.ask(24, 'Meeting the government target to have almost a million', ' Adapted from')
add('q15-a-i', '1-3', 'encouraging-electric-vehicles', ref(15, '(c)(i)'),
    O.ask(24, 'Outline two ways the Irish government may influence', ' 1. 2.'), '8 + 4', 12,
    [steps('r-1', 'A way to influence consumers to switch — any two',
           bl('• Provide a grant to consumers', '(ii) Describe one social benefit'), 8, 4, 'ways')],
    stem=q15c_stem)
pick('q15-c-ii', '0-2', 'social-benefits-of-electric-cars', ref(15, '(c)(ii)'),
     O.ask(24, 'Describe one social benefit for Ireland', ' 75 marks'),
     'A social benefit — any one',
     bl('• Less air pollution due to reduced carbon emissions.', '23 | P a g e'),
     1, 8, 'One developed benefit, 8 marks.', stem=q15c_stem)

# Q16 ─ Keogh's Crisps: factors of production; economic goods; food waste
q16_stem = O.ask(25, 'Established in 2011 by Tom Keogh', ' Adapted from')
add('q16-a-i-factors', '0-1', 'factors-of-production', ref(16, '(a)(i)'),
    O.ask(25, 'Complete the table below to show your understanding', ' Factor of'), '6 @ 4', 24,
    [point('r-land', cell('POTATOES SALT OIL', '\nTHE HUMAN EFFORT', occ=0), 4,
           'Row 1 (Land): an example, 4 marks; the scheme accepts potatoes, salt or oil.'),
     point('r-labour', 'LABOUR — ' + cell('THE HUMAN EFFORT INVOLVED IN THE PRODUCTION', '\nWorkers', occ=0),
           8, 'Row 2: name the factor, Labour, and explain it, 4 marks each.'),
     point('r-capital', cell('ANYTHING MADE BY HUMANS WHICH IS USED', '\nMachinery', occ=0), 4,
           'Row 3 (Capital): explain it, 4 marks.'),
     point('r-enterprise', 'ENTERPRISE — TOM KEOGH', 8,
           'Row 4: name the factor, Enterprise, and give an example, the entrepreneur Tom Keogh, 4 marks '
           'each. The scheme prices the six blank cells at 4 marks each; the completed table is shown in '
           'the figure.')],
    stem=q16_stem, figure=SOL + 'p26-q16ai-table')
add('q16-a-ii', '0-1', 'why-entrepreneurs-matter', ref(16, '(a)(ii)'),
    O.ask(26, 'In your opinion are entrepreneurs important', ' Explanation:'), '2 + 4', 6,
    [point('r-choice', 'Yes.', 2, 'Tick YES, 2 marks: the scheme credits no No answer.'),
     heading('r-explanation', 'Why entrepreneurs matter — any one',
             bl('• Entrepreneurs create employment', '(b) Keogh’s Crisps are economic goods'), 4,
             'Explain, 4 marks.')],
    stem=q16_stem)
pick('q16-a-i', '0-1', 'properties-of-an-economic-good', ref(16, '(b)(i)'),
     O.ask(26, 'Explain any two of the above terms.', ' 1. 2.'),
     'One of the three terms — any two',
     at('Scarce:', '(ii) Keogh’s Crisps are due', ['Scarce:', 'Transferable:', 'Utility:']),
     2, 7, 'Any two of scarce, transferable and utility, explained for Keogh’s Crisps, 7 marks each.',
     stem=O.ask(26, 'Keogh’s Crisps are economic goods which means', ' (i)'))
add('q16-b-ii', '1-5', 'economies-of-scale-ol', ref(16, '(b)(ii)'),
    O.ask(26, 'This expansion will allow Keogh’s Crisps to benefit', ' Economies of scale:'), '7', 7,
    [point('r-1', O.run('Economies of scale arise as the firm increases', '25 | P a g e'), 7,
           'Explain the term, 7 marks: as Keogh’s grows, its average cost per unit falls.')],
    stem=O.ask(26, 'Keogh’s Crisps are due to increase production capacity', ' Adapted from'))
q16c_stem = O.ask(27, 'In Ireland, we generate nearly 800,000 tons', ' Adapted from')
pick('q16-c-i', '0-2', 'the-social-cost-of-food-waste', ref(16, '(c)(i)'),
     O.ask(27, 'Outline one cost to society of wasting food.', ' Cost to society:'),
     'A cost to society — any one',
     bl('• Inequitable:', '(ii) Describe one action consumers'),
     1, 8, 'One developed cost, 8 marks.', stem=q16c_stem)
pick('q16-c-ii', '0-2', 'how-consumers-can-cut-food-waste', ref(16, '(c)(ii)'),
     O.ask(27, 'Describe one action consumers could take', ' Consumers:'),
     'An action consumers could take — any one',
     bl('• Reduce consumption: buy only what is necessary.', '(iii) Describe one action producers'),
     1, 8, 'One developed action, 8 marks.', stem=q16c_stem)
pick('q16-c-iii', '0-2', 'how-producers-can-cut-food-waste', ref(16, '(c)(iii)'),
     O.ask(27, 'Describe one action producers could take', ' Producers:'),
     'An action producers could take — any one',
     bl('• Invest in efficient production systems', '26 | P a g e'),
     1, 8, 'One developed action, 8 marks.', stem=q16c_stem)

# A card whose figure slot holds its solution carries the whole printed question.
for cid, fig in [('q11-b-ii', 'p11-q11bii-question'), ('q16-a-i-factors', 'p25-q16ai-question')]:
    show_before_reveal(next(c for c in cards if c['id'] == D.prefix + cid), None, PAP + fig)


# ── Withdrawn halves ──────────────────────────────────────────────────────────
# The earlier extractors split two jointly priced answers into one card per
# part. Each half is still emitted, lifted from its own part, so that
# card-corrections.json can withdraw it by ID and name the combined card that
# now carries its saved progress (cardAliases.ts). Neither ships.
WITHDRAWN = [
    ('sa-q10-social', 'sa-q10-private', 'Social benefit', bl('• Healthier young population.', '9 | P a g e'), 4),
    ('q14-a-ii-effect', 'q14-a-ii-reason', 'One effect on Irish consumers',
     [O.run('The increase in petrol prices leads to consumers', '18 | P a g e')], 4),
]
for old, canonical, label, options, per in WITHDRAWN:
    base = next(c for c in cards if c['id'] == D.prefix + canonical)
    pick(old, base['topicId'].removeprefix('economics-'), base['conceptId'] + '-withdrawn-half',
         base['questionRef'], f"{base['questionText']} Withdrawn half: {label}.", label, options, 1, per,
         f'Withdrawn: this part is answered within {D.prefix + canonical}.', stem=base.get('stem', ''),
         section=base['section'])

if __name__ == '__main__':
    emit(cards)
