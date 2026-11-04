#!/usr/bin/env python3
"""Economics 2014 Ordinary Level, Sections A and B (old syllabus, first cards).

Authored from the independent census in drafts/economics-2014-ol-ev.json, made
from a visual sweep of all 12 paper pages and 36 scheme pages before any 2014
Ordinary card existed. Section B restarts at Question 1, so every citation
names its section and every id carries it (-sa-, -sb-). Question wording and
stems are sliced from the question paper; every marking point is sliced from
the scheme (econ_legacy_lib.py). The Ordinary scheme reprints each question
above its answer, so a slice always starts after the reprinted wording. A stem
stops before any printed table: the table is the crop beside the typed ask,
and printed items a student must read to answer are typed from the text layer.
The only prose written here is guidance: tariffs, route labels and what a
figure or a calculation shows.

As in the 2014 Higher scheme, the bullets are drawn in SymbolMT and the text
layer reports each as the letter "x"; no slice crosses one (`xb`, `xcell`).
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from econ_legacy_lib import TAIL, Old, OldDeck, beside_ask  # noqa: E402
from econ_lib import anyN, as_option, emit, point, tidy  # noqa: E402

H = Old(2014, 'ordinary', 'LC034GLP000EV')
D = OldDeck(2014, 'ordinary')
cards, add, pick, heading, ref = D.cards, D.add, D.pick, D.heading, D.ref
A = dict(section='A')
B = dict(section='B')
SOL = 'economics-2014-OL-scheme-'
PAP = 'economics-2014-OL-paper-'
XB = re.compile(r'(?:^|\n)x ')
cc = lambda text, **kw: H.cell(text, cells_only=True, **kw)   # a whole table cell
# The paper's ruled answer lines are set as an ellipsis, so a statement still reads as one to complete.
blanks = lambda t: ' '.join(re.sub(r'\s*_{2,}\s*', ' … ', t).split())


def xb(start, end, occ=None):
    """The scheme's SymbolMT bullet list between two anchors, cut at each bullet."""
    out = []
    for piece in XB.split(H.chunk(start, end, occ)):
        piece = TAIL.sub('', as_option(tidy(piece))).strip()
        if piece:
            out.append(H.traced(piece))
    return out


def xcell(start, **kw):
    """A table cell that opens with a SymbolMT bullet (or several), read without the bullet letters."""
    text = cc(start, **kw)
    return H.traced(' '.join(p.strip() for p in re.split(r'(?:^|\s)x\s', text) if p.strip()))


def cut(text, firsts):
    """One cell holding several responses, cut where each begins."""
    return [H.traced(o) for o in H._cut(text, firsts, firsts[0])]


def side(label, options):
    """Options listed under one of the scheme's own headings, each named by it."""
    lab = H.traced(label)
    return [f'{lab} — {o}' for o in options]


def pair(head, body):
    return f'{H.traced(head)} — {H.traced(body)}'


# ═════════════════════════════════ SECTION A ══════════════════════════════════

# Q1 ─ economics as a social science
add('sa-q1', '0-1', 'what-economics-studies', ref('A', 1),
    blanks(H.ask(2, 'Complete the following statement:', ' (16 marks)')), '8 + 4 + 4', 16,
    [anyN('r-1', 'Each word placed', 16, 3, 8,
          [H.traced('SOCIAL'), H.traced('RESOURCES / FACTORS OF PRODUCTION / INPUTS'), H.traced('WANTS')],
          'The three words, as the scheme completes the statement: ' + H.traced('Economics is a SOCIAL science.') + ' '
          + H.traced('It examines how scarce RESOURCES / FACTORS OF PRODUCTION / INPUTS are used to satisfy our infinite WANTS.')
          + ' The first correct response 8 marks, the 2nd and 3rd 4 each.', steps=[8, 4, 4])],
    kind='fixed', **A)

# Q2 ─ visible and invisible trade
ticks = (('Visible exports', 'Irish farmers selling beef in the UK'), ('Invisible imports', 'Irish rugby supporters travelling to France'),
         ('Invisible exports', 'Americans using Aer Lingus to travel to Ireland'),
         ('Visible imports', 'Irish consumers buying Abercrombie hoodies from USA on-line'))
add('sa-q2', '4-2', 'visible-and-invisible-trade', ref('A', 2),
    f"{H.q(2, 'Indicate by means of a tick', ' Visible Invisible')} {H.q(2, 'Irish farmers selling beef in the UK.', ' (16 marks)')}",
    '10 + 2 + 2 + 2', 16,
    [anyN('r-1', 'Each statement ticked', 16, 4, 10, [f'{cc(cat, whole=True)} — {cc(st, whole=True)}' for cat, st in ticks],
          'All four: the first correct response 10 marks, the 2nd, 3rd and 4th 2 each.', steps=[10, 2, 2, 2])],
    kind='fixed', **A)

# Q3 ─ diminishing marginal utility
add('sa-q3', '1-1', 'diminishing-marginal-utility', ref('A', 3),
    blanks(H.ask(2, 'Choose the correct word from the bracketed words', ' (16 marks)')), '12 + 4', 16,
    [anyN('r-1', 'Each word chosen', 16, 2, 12, [H.traced('INCREASING'), H.traced('FALL')],
          'Both words, as the scheme completes the statement: '
          + H.traced('As INCREASING (increasing / decreasing) quantities of a good are consumed, the marginal utility gained '
                     'from consuming each extra unit of the good will eventually FALL (rise / fall).')
          + ' The first correct response 12 marks, the 2nd 4.', steps=[12, 4])],
    kind='fixed', **A)

# Q4 ─ lower public sector pay
add('sa-q4', '3-1', 'lower-public-sector-pay', ref('A', 4),
    H.q(3, 'Outline one economic effect which a decrease in public sector pay', ' Retailers'), '10 + 6', 16,
    [anyN('r-1', 'One effect for each — retailers and the government’s finances', 16, 2, 10,
          side('Retailers in Ireland', H.split('Reduced demand / fewer sales / lower profits', 'Government Finances\nReduced',
                                               ['Reduced demand / fewer sales / lower profits', 'Reduction in employment',
                                                'Closure of some retailers:']))
          + side('Government Finances', H.split('Reduced current expenditure / government borrowing', '1st correct response: 10',
                                                ['Reduced current expenditure / government borrowing', 'Reduced tax revenue.',
                                                 'Increased social welfare payments'])),
          'One effect for retailers and one for the government’s finances: the 1st correct response 10 marks, the 2nd 6.',
          steps=[10, 6])],
    kind='fixed', **A)

# Q5 ─ national income
add('sa-q5', '3-0', 'national-income-from-its-parts', ref('A', 5),
    H.q(3, 'Suppose C + I + G = €3,200m', ' Workings'), '15 + 1', 16,
    [point('r-working', f"{H.traced('Y = C + I + G + X – M')}; {H.traced('Y = €3,200m + €500m - €400m')}", 15,
           H.traced('5 correct components: 3 marks each') + '. The figure shows the working as printed.'),
     point('r-answer', H.traced('€ 3,300m'), 1, 'The answer, 1 mark.')],
    figure=SOL + 'p06-q5-working', **A)

# Q6 ─ a union's minimum wage
q6_fig = PAP + 'p03-q6-diagram'
statements6 = (('TRUE', 'W1 is the minimum wage rate in the above diagram'), ('FALSE', 'Trade Union members will work below wage rate W1.'),
               ('FALSE', 'Above W1, as the wage rate increases, the supply of labour decreases.'))
add('sa-q6', '2-1', 'a-unions-minimum-wage', ref('A', 6),
    f"{H.q(3, 'Tick (✓) True or False after each of the following statements:', ' Statement')} "
    f"{H.q(3, 'W1 is the minimum wage rate in the above diagram.', ' (17 marks)')}", '7 + 7 + 3', 17,
    [anyN('r-1', 'Each statement marked', 17, 3, 7, [f'{H.traced(a)} — {H.traced(s)}' for a, s in statements6],
          'All three: the 1st and 2nd correct responses 7 marks each, the 3rd 3. The scheme prints the third statement '
          'as “Above W1, as the wage rate increases, …”.', steps=[7, 7, 3])],
    kind='fixed', stem=H.q(3, 'The diagram below represents the supply curve of labour', ' Wage Rate'), figure=q6_fig, **A)

# Q7 ─ the home renovation incentive
add('sa-q7', '3-1', 'the-home-renovation-incentive', ref('A', 7),
    H.q(4, 'State one economic effect which this scheme may have for each of the following:', ' Irish businesses'), '11 + 6', 17,
    [anyN('r-1', 'One effect for each — Irish businesses and homeowners', 17, 2, 11,
          side('Irish businesses', H.split('Demand for products\nIncreased', 'Homeowners\nImproved',
                                           ['Demand for products', 'Employment / Reduction in unemployment rates',
                                            'Opportunities for expansion.', '‘Legitimate’ businesses may develop.']))
          + side('Homeowners', H.split('Improved standard of living / increased disposable incomes', '1st correct response: 11',
                                       ['Improved standard of living / increased disposable incomes', 'Value of property may increase',
                                        'More affordable / net cost of home improvement falls', 'Speedier repayment of borrowings',
                                        'Future energy bills reduced'])),
          'One effect for businesses and one for homeowners: the 1st correct response 11 marks, the 2nd 6.', steps=[11, 6])],
    kind='fixed', stem=H.q(4, 'The Home Renovation Incentive Scheme introduced in Budget 2014', ' State one'), **A)

# Q8 ─ economists and their ideas
matches = (('A. Canons of Taxation', '3. Adam Smith'), ('B. Liquidity Preference Theory', '1. John Maynard Keynes'),
           ('C. Theory of Population and Food Supply', '4. Thomas Malthus'), ('D. Worker exploitation in a capitalist system', '2. Karl Marx'))
add('sa-q8', '0-0', 'economists-and-their-ideas', ref('A', 8),
    # The two printed lists follow the ask, column by column (the text layer interleaves them line by line).
    ' '.join([H.q(4, 'Match the economic ideas listed below with the associated economist:', ' Economic Idea'),
              'Economic Idea:', ' '.join(H.traced(i) for i, _ in matches), 'Economist:',
              ' '.join(H.traced(x) for x in ('1. John Maynard Keynes', '2. Karl Marx', '3. Adam Smith', '4. Thomas Malthus'))]),
    '8 + 3 + 3 + 3', 17,
    [anyN('r-1', 'Each idea matched', 17, 4, 8, [f'{H.traced(i)} — {H.traced(e)}' for i, e in matches],
          'All four: the 1st correct response 8 marks, the 2nd, 3rd and 4th 3 each.', steps=[8, 3, 3, 3])],
    kind='fixed', **A)

# Q9 ─ the PED formula's symbols
q9_fig = PAP + 'p04-q9-table'
add('sa-q9', '1-4', 'the-symbols-of-ped', ref('A', 9),
    H.q(4, 'Complete the following table to indicate what each of the above symbols stands for:', ' ∆Q'), '8 + 3 + 3 + 3', 17,
    [anyN('r-1', 'Each blank symbol', 17, 4, 8,
          [H.traced(x) for x in ('Change in the quantity demanded of the good', 'Original price of the good.',
                                 'New / current price of the good', 'New / current quantity demanded of the good')],
          'The four symbols the table leaves blank, in its order: ΔQ, P1, P2 and Q2 (ΔP and Q1 are printed). The 1st '
          'correct response 8 marks, the 2nd, 3rd and 4th 3 each.', steps=[8, 3, 3, 3])],
    kind='fixed', stem=H.q(4, 'A formula for measuring Price Elasticity of Demand (PED) is as follows:', ' ∆Q'), figure=q9_fig, **A)

# ═════════════════════════════════ SECTION B ══════════════════════════════════

# Q1 ─ monopoly; barriers; Dublin Bus
q1 = ' '.join([H.q(5, 'The diagram below represents a Monopoly firm in equilibrium.', ' P MC'),
               H.q(5, 'Copy the diagram into your answer book.', ' (i)')])
q1_fig = PAP + 'p05-q1-diagram'
add('sb-q1-a-i', '2-0', 'labels-of-monopoly', ref('B', 1, '(a)(i)'),
    H.q(5, 'State what each of the five labels circled above represents.', ' (ii)'), '5 @ 4', 20,
    [point(f'r-{lab.lower()}', f'{lab} — {H.traced(full)}', 4, f'{lab}, 4 marks.')
     for lab, full in (('P', 'Price'), ('AC', 'Average Cost'), ('MC', 'Marginal Cost'), ('AR', 'Average Revenue'), ('MR', 'Marginal Revenue'))],
    stem=q1, figure=q1_fig, **B)
add('sb-q1-a-ii', '2-0', 'equilibrium-of-the-monopolist', ref('B', 1, '(a)(ii)'),
    H.q(5, 'The firm is in equilibrium at point E and produces output Q1.', ' (30 marks)'), '6 + 4', 10,
    [anyN('r-1', 'Each label shown', 10, 2, 6, [H.traced('C1 the average cost of producing this output'), H.traced('P1 the price charged for this output')],
          'C1 and P1: the 1st correct response 6 marks, the 2nd 4. The completed diagram is shown with the answer.', steps=[6, 4])],
    kind='fixed', stem=q1, figure=SOL + 'p09-q1a-diagram', **B)
beside_ask(cards[-1], q1_fig)
q1b = H.q(5, 'A legal/statutory monopoly is a barrier to entry.', ' (i)')
add('sb-q1-b-i', '2-0', 'a-statutory-monopoly', ref('B', 1, '(b)(i)'), H.q(5, 'Explain the underlined term.', ' (ii)'), '7', 7,
    [point('r-1', H.opt('The government may grant a company the sole right to supply', '\n7 marks'), 7, 'The explanation, 7 marks.')],
    stem=q1b, **B)
pick('sb-q1-b-ii', '2-0', 'other-barriers-to-entry', ref('B', 1, '(b)(ii)–(iii)'),
     ' '.join([H.q(5, 'State two other barriers to entry facing firms', ' (iii)'), H.q(5, 'Write brief notes on each of these.', ' (21 marks)')]),
     'A barrier, with its note — any two',
     H.split('Ownership of a Patent / Copyright', '2 x 7 marks each',
             ['Ownership of a Patent / Copyright', 'Trade Agreements & Collusion.', 'Ownership of raw materials',
              'Industry requires a large investment in capital', 'Mergers / Takeovers', 'Monopolies based on fear, force or threats']),
     2, 7, 'Two barriers, 7 marks each: the scheme prices (ii) and (iii) together.', stem=q1b, **B)
q1c = H.q(5, 'Dublin Bus has a monopoly on bus services', ' (i)')
pick('sb-q1-c-i', '2-0', 'advantages-of-the-bus-monopoly', ref('B', 1, '(c)(i)'),
     H.q(5, 'State and explain two advantages of this statutory monopoly for consumers.', ' (ii)'), 'An advantage — any two',
     H.split('Convenient and reliable service', '2 points: 6 marks', ['Convenient and reliable service', 'Provision of public services']),
     2, 6, 'Two advantages, 6 marks each.', stem=q1c, **B)
pick('sb-q1-c-ii', '2-0', 'benefits-of-bus-competition', ref('B', 1, '(c)(ii)'),
     H.q(5, 'State and explain two reasons why increased competition may benefit consumers.', ' (24 marks)'), 'A reason — any two',
     H.split('Improved quality of service', '2 points: 6 marks', ['Improved quality of service', 'Lower prices', 'Increased availability of service']),
     2, 6, 'Two reasons, 6 marks each.', stem=q1c, **B)

# Q2 ─ economic goods; demand for cars; alcohol
q2a = H.q(6, 'An economic good is scarce and transferable', ' (i)')
pick('sb-q2-a-i', '0-1', 'what-makes-an-economic-good', ref('B', 2, '(a)(i)'), H.q(6, 'Explain any two of the underlined terms.', ' (ii)'),
     'A term — any two', H.split('Scarce\nThere must be', 'Explanations: 2 points', ['Scarce', 'Transferable', 'Utility']),
     2, 7, 'Two terms, 7 marks each.', stem=q2a, **B)
add('sb-q2-a-ii', '0-1', 'is-good-health-an-economic-good', ref('B', 2, '(a)(ii)'),
    H.q(6, 'Is good health an economic good? Explain your answer.', ' (21 marks)'), '7', 7,
    [point('r-1', H.traced('No. It is not transferable from one person to another.'), 7, 'The answer with its reason, 7 marks.')], stem=q2a, **B)
q2b = H.q(6, 'The diagram below represents a shift in the demand curve for new cars in Ireland.', ' P D1')
q2b_fig = PAP + 'p06-q2b-diagram'
add('sb-q2-b-i', '1-1', 'the-law-of-demand', ref('B', 2, '(b)(i)'), H.q(6, 'Explain the Law of Demand.', ' (ii)'), '6', 6,
    [point('r-1', H.opt('This states that as price increases / quantity demanded', '\n6 marks'), 6, 'The explanation, 6 marks.')], stem=q2b, **B)
reasons = (('Availability of offers from motor dealers', 'Some companies are offering loans at low or zero interest rates.'),
           ('Preference for lower annual car tax rates', 'People who can afford to do so are changing their cars'),
           ('Preference for better fuel efficiency', 'People are changing cars so as to get a more fuel efficient car'),
           ('Increased confidence in economy', 'Increased employment; increased incomes for some employees'))
pick('sb-q2-b-ii', '1-1', 'why-demand-for-new-cars-rose', ref('B', 2, '(b)(ii)'),
     H.q(6, 'State and explain two reasons why the demand curve for new cars might shift to the right.', ' (iii)'), 'A reason — any two',
     [f'{cc(s, whole=True)} — {cc(e)}' for s, e in reasons], 2, 6, 'Two reasons, 6 marks each.', stem=q2b, figure=q2b_fig, **B)
pick('sb-q2-b-iii', '0-2', 'electric-cars-for-society', ref('B', 2, '(b)(iii)'),
     H.q(6, 'Outline one economic advantage to society of increased use of electric cars.', ' (24 marks)'), 'An advantage — any one',
     H.split('Reduced emissions / cleaner environment', '1 advantage: 6 marks',
             ['Reduced emissions / cleaner environment', 'Newer vehicles on roads (Safety)', 'Less waste of scarce resources / reduced reliance on oil/gas']),
     1, 6, 'One advantage, 6 marks.', stem=q2b, **B)
q2c = H.q(6, '“The government is considering the introduction of a minimum price for alcohol', ' (i)')
pick('sb-q2-c-i', '1-3', 'curbing-alcohol-consumption', ref('B', 2, '(c)(i)'),
     H.q(6, 'State and explain one other measure the government could take to reduce alcohol consumption.', ' (ii)'), 'A measure — any one',
     H.split('Taxes: increase taxes', '\n6 marks', ['Taxes:', 'Opening hours:', 'Introduce limits to the amount', 'Age restrictions:',
                                                  'Sales points:', 'Sponsorship:', 'Consumer Awareness:', 'Increased penalties:']),
     1, 6, 'One measure, 6 marks.', stem=q2c, **B)
pick('sb-q2-c-ii', '1-3', 'drinking-less-for-individuals', ref('B', 2, '(c)(ii)'),
     H.q(6, 'Discuss two possible benefits to individuals if they reduce their alcohol consumption.', ' (iii)'), 'A benefit — any two',
     H.split('Greater disposable income:', '2 x 6 marks', ['Greater disposable income:', 'Healthier lifestyle:', 'Reduced spending on healthcare:',
                                                         'Reduced healthcare insurance premiums:', 'Increased productivity:']),
     2, 6, 'Two benefits, 6 marks each.', stem=q2c, **B)
pick('sb-q2-c-iii', '2-2', 'drinking-less-for-society', ref('B', 2, '(c)(iii)'),
     H.q(6, 'Discuss two possible benefits to society if the consumption of alcohol falls.', ' (30 marks)'), 'A benefit — any two',
     H.split('Reduction in absenteeism:', '2 x 6 marks', ['Reduction in absenteeism:', 'Reduced pressure on hospitals:',
                                                        'Reduction in alcohol related deaths', 'Population healthier:']),
     2, 6, 'Two benefits, 6 marks each.', stem=q2c, **B)

# Q3 ─ economic systems; LDCs; growth
q3a = H.q(7, 'The economy in China is changing from a centrally planned economic system', ' (i)')
# The paper asks "Explain ... the underlined term(s)." five times, so each card's question carries its own stem.
add('sb-q3-a-i', '1-0', 'planned-and-mixed-economies', ref('B', 3, '(a)(i)'),
    f"{q3a} {H.q(7, 'Explain each of the underlined terms.', ' (ii)')}", '4 + 4', 8,
    [point('r-planned', f"{cc('Centrally planned economic system', whole=True)} — {xcell('x Resources are allocated by the state', whole=False)}", 4,
           'The centrally planned economic system, 4 marks.'),
     point('r-mixed', f"{cc('Mixed economic system', whole=True)} — {xcell('x An economy that incorporates elements')}", 4,
           'The mixed economic system, 4 marks.')], **B)
add('sb-q3-a-ii', '1-0', 'examples-of-the-two-systems', ref('B', 3, '(a)(ii)'),
    H.q(7, 'State one other example of a centrally planned economic system', ' (iii)'), '4 + 4', 8,
    [heading('r-planned', 'A centrally planned economic system — any one', [H.traced('North Korea'), H.traced('Cuba')], 4,
             'A centrally planned economy, 4 marks.'),
     point('r-mixed', 'Mixed economic system — ' + H.traced('Ireland.'), 4, 'A mixed economy, 4 marks.')],
    kind='fixed', stem=q3a, **B)
pick('sb-q3-a-iii', '1-0', 'gains-from-a-mixed-economy', ref('B', 3, '(a)(iii)'),
     H.q(7, 'Outline one possible economic advantage for Chinese citizens', ' (20 marks)'), 'An advantage — any one',
     H.split('Increased individual choice / reduced government interference', '\n4 marks',
             ['Increased individual choice / reduced government interference', 'More competitive prices / improved efficiency',
              'Individuals can set up their own businesses', 'Greater incentive to work', 'Higher standard of living']),
     1, 4, 'One advantage, 4 marks.', stem=q3a, **B)
q3b = H.q(7, 'Some Less Developed Countries (LDCs) experience difficulties', ' (i)')
add('sb-q3-b-i', '4-0', 'economic-growth-defined', ref('B', 3, '(b)(i)'), f"{q3b} {H.q(7, 'Explain the underlined term.', ' (ii)')}", '5', 5,
    [point('r-1', H.traced('Economic growth: an increase in the rate of growth of GNP /GDP / national income /output'), 5, 'The explanation, 5 marks.')],
    **B)
pick('sb-q3-b-ii', '4-0', 'other-difficulties-of-ldcs', ref('B', 3, '(b)(ii)'),
     H.q(7, 'Outline two other economic difficulties which LDCs may experience.', ' (iii)'), 'A difficulty — any two',
     H.split('High population growth rates in LDCs', '2 points: 5 marks',
             ['High population growth rates in LDCs', 'Famine in LDCs / low life expectancy', 'Over-dependence on one crop in LDCs',
              'Poor infrastructure in LDCs', 'Low per capita incomes in LDCs', 'Poor levels of education/literacy in LDCs',
              'Exploitation by multinationals', 'Political corruption / less stable political institutions']),
     2, 5, 'Two difficulties, 5 marks each.', stem=q3b, **B)
pick('sb-q3-b-iii', '4-0', 'how-irish-citizens-can-help', ref('B', 3, '(b)(iii)'),
     H.q(7, 'Outline two measures which Irish citizens could take', ' (25 marks)'), 'A measure — any two',
     H.split('Buy goods produced in LDCs / buy Fair Trade products', '2 points: 5 marks',
             ['Buy goods produced in LDCs / buy Fair Trade products', 'Campaigns: for debt reduction', 'Volunteer to work in a LDC',
              'Donations / Financial aid']),
     2, 5, 'Two measures, 5 marks each.', stem=q3b, **B)
q3c = H.q(7, 'In recent years Ireland has been in recession', ' (i)')
add('sb-q3-c-i', '3-0', 'measuring-the-economy', ref('B', 3, '(c)(i)'),
    H.q(7, 'What is the name of the official measurement of the size of the economy?', ' (ii)'), '9', 9,
    [heading('r-1', 'A measure — any one', [H.traced('Gross National Product / GNP'), H.traced('Gross Domestic Product / GDP')], 9,
             'The measurement, 9 marks.')], kind='fixed', stem=q3c, **B)
growth = (('citizens', 'Irish citizens', 'Employment opportunities Increased standard of living Improved state services Less need to emigrate',
           ['Employment opportunities', 'Increased standard of living', 'Improved state services', 'Less need to emigrate'],
           'x If sales increase more workers'),
          ('retailers', 'Retailers', 'Increased sales / profits Expansion / less risk of closure',
           ['Increased sales / profits', 'Expansion / less risk of closure'], 'x Sales increase and so too will profits.'),
          ('government', 'Government finances', 'Tax revenues Social welfare spending Reduced borrowing',
           ['Tax revenues', 'Social welfare spending', 'Reduced borrowing'], 'x Increased employment will result in increased tax revenues.'))
rows = []
for rid, area, line, heads, expl in growth:
    bodies = [H.traced(p.strip()) for p in re.split(r'(?:^|\s)x\s', cc(expl)) if p.strip()]
    rows.append(heading(f'r-{rid}', H.traced(area) + ' — any one', [pair(h, b) for h, b in zip(cut(cc(line, whole=True), heads), bodies)], 7,
                        f'One benefit for {area if area.startswith("Irish") else area.lower()}, 7 marks.'))
add('sb-q3-c-ii', '3-5', 'who-gains-from-growth', ref('B', 3, '(c)(ii)'),
    H.q(7, 'Outline one benefit of economic growth to each of the following', ' (30 marks)'), '3 x 7', 21, rows, kind='fixed', stem=q3c, **B)

# Q4 ─ VAT and the airport tax; austerity; the Budget 2014 measures
q4a = H.q(7, 'In Budget 2014 The Minister for Finance decided to retain the reduced 9% VAT rate', ' (i)')
add('sb-q4-a-i', '3-1', 'value-added-tax', ref('B', 4, '(a)(i)'), H.q(7, 'Explain the term ‘Value Added Tax’.', ' (ii)'), '6', 6,
    [point('r-1', xb('This is a tax on goods and services.', '\n6 marks')[0], 6,
           'The explanation, 6 marks. The scheme also accepts its second statement.',
           accepts=[xb('This is a tax on goods and services.', '\n6 marks')[1]])], stem=q4a, **B)
add('sb-q4-a-ii', '3-1', 'both-taxes-are-indirect', ref('B', 4, '(a)(ii)'),
    H.q(7, 'Are the taxes underlined above direct taxes or indirect taxes?', ' (iii)'), '2 x 6', 12,
    [point('r-vat', f"{cc('VAT', whole=True)} — {H.traced('Indirect')}. {cc('It is a tax on goods and services', whole=True)}", 6,
           'VAT, indirect, with its explanation, 6 marks.'),
     point('r-airport', f"{cc('Airport Travel Tax', whole=True)} — {H.traced('Indirect')}. {cc('It is a tax on using this service', whole=True)}", 6,
           'The airport travel tax, indirect, with its explanation, 6 marks.')],
    stem=q4a, **B)
pick('sb-q4-a-iii', '3-1', 'why-the-minister-kept-the-measures', ref('B', 4, '(a)(iii)'),
     H.q(7, 'Discuss two possible economic reasons why the Minister for Finance decided', ' (30 marks)'), 'A reason — any two',
     H.split('Encourage tourism\nBy making', '2 reasons: 6 marks',
             ['Encourage tourism', 'Protect / create jobs', 'Encourage spending / economic growth', 'Increase tax revenues']),
     2, 6, 'Two reasons, 6 marks each.', stem=q4a, **B)
q4b = ' '.join([H.q(7, 'The Budget 2014 is considered to be an ‘austerity’ budget.', ' (i)')])
add('sb-q4-b-i', '3-1', 'austerity-measures', ref('B', 4, '(b)(i)'),
    H.q(7, 'State two examples of austerity measures introduced by the Irish government', ' (ii)'), '5 + 4', 9,
    [anyN('r-1', 'An example — any two', 9, 2, 5, xb('Reduction in public sector pay.', '1st example: 5 marks'),
          'Two examples: the 1st 5 marks, the 2nd 4.', steps=[5, 4])],
    kind='fixed', stem=q4b, **B)
pick('sb-q4-b-ii', '3-1', 'austerity-and-citizens', ref('B', 4, '(b)(ii)'),
     H.q(7, 'Outline two economic effects which austerity measures may have on Irish citizens.', ' (21 marks)'), 'An effect — any two',
     H.split('Increased unemployment / emigration\nReduced', '2 effects: 6 marks',
             ['Increased unemployment / emigration', 'Loss of business confidence / lack of investment',
              'Reduction in aggregate demand / spending / lack of economic growth', 'Fall in living standards', 'Increased indebtedness',
              'Loss of some state services']),
     2, 6, 'Two effects, 6 marks each.', stem=q4b, **B)
q4c = H.q(7, 'Outline one economic argument in favour of and one economic argument against', ' •')
measures = (
    ('jobseekers', ('A reduction in Jobseekers Allowance', ' • Increase in rate'),
     ['Decreased expenditure / borrowing The', 'Opportunity cost Money saved', 'Incentive to education / training The'],
     ['Inequitable The lower', 'Emigration Younger', 'Burden on families Families']),
    ('dirt', ('Increase in rate of Deposit Interest Retention Tax', ' • Increase in excise'),
     ['Government revenue This increase may raise', 'Less need to raise direct taxes', 'Economic The cost of collection', 'Progressive Only those',
      'Encourage spending People'],
     ['Discourage savings The', 'Reduced availability of loans Financial']),
    ('tobacco', ('Increase in excise duty on tobacco', ' (24 marks)'),
     ['Government revenue This increase will help', 'Reduce consumption / personal health', 'Reduced healthcare costs As', 'Opportunity cost The money saved'],
     ['Standard of living Disposable', 'Inflation Prices', 'Smuggling/black economy may increase', 'Tax revenue If consumption']))
for key, label, pro, con in measures:
    add(f'sb-q4-c-{key}', '3-1', 'arguing-the-budget-2014-measures', ref('B', 4, '(c)', key),
        f"{q4c} Answer for: {H.q(7, *label).rstrip(';.')}.", '8 + 4', 12,
        [anyN('r-1', 'One argument in favour and one against', 12, 2, 8,
              side('Economic argument in favour', [cc(x) for x in pro]) + side('Economic argument against', [cc(x) for x in con]),
              'One argument in favour of this measure and one against: the 1st correct response 8 marks, the 2nd 4 ('
              + H.traced('Two measures: 1st correct response: 8 marks / 2nd correct response: 4 marks') + '). Any two of '
              'the three measures are answered.', steps=[8, 4])],
        kind='fixed', **B)

# Q5 ─ costs; entrepreneurship; factors and location
q5a = H.q(8, 'Irish businesses face many challenges in attempting to control their costs.', ' (i)')
add('sb-q5-a-i', '1-5', 'fixed-and-variable-costs', ref('B', 5, '(a)(i)'),
    H.q(8, 'Define fixed cost and variable cost and state one example of each.', ' (ii)'), '5 + 4 + 2 + 2', 13,
    [point('r-fixed', f"{cc('Fixed Costs', whole=True)} — {cc('Costs which do not change/remain fixed when output changes', whole=True)}", 5,
           'Fixed costs, 5 marks.'),
     point('r-variable', f"{cc('Variable Costs', whole=True)} — {cc('Costs which change as output changes', whole=True)}", 4,
           'Variable costs, 4 marks.'),
     point('r-fixed-example', f"{cc('Fixed Costs', whole=True)} — {cc('One correct example:', whole=True)}", 2,
           'An example of a fixed cost, 2 marks: the scheme prints no example.'),
     point('r-variable-example', f"{cc('Variable Costs', whole=True)} — {cc('One correct example:', whole=True)}", 2,
           'An example of a variable cost, 2 marks.')],
    stem=q5a, **B)
add('sb-q5-a-ii', '1-5', 'why-control-costs', ref('B', 5, '(a)(ii)'),
    H.q(8, 'State and explain two reasons why it is important for a business to control its costs.', ' (25 marks)'), '8 + 4', 12,
    [anyN('r-1', 'A reason — any two', 12, 2, 8,
          H.split('Lower prices / increased demand / profits increase', '1st correct response: 8',
                  ['Lower prices / increased demand / profits increase', 'Increased employment', 'Increased competitiveness',
                   'Better use of scarce resources / reduced waste', 'Survival of business']),
          'Two reasons: the 1st correct response 8 marks, the 2nd 4.', steps=[8, 4])],
    kind='fixed', stem=q5a, **B)
q5b = H.q(8, 'Patrick Joy was named Entrepreneur of the Year in 2013.', ' (i)')
ent = xb('An entrepreneur undertakes the risk in setting up a business.', '\n5 marks')
# Page 8 prints "Explain the underlined term." twice, so each is read with the ask that follows it.
add('sb-q5-b-i', '0-1', 'the-entrepreneur', ref('B', 5, '(b)(i)'),
    f"{q5b} {H.q(8, 'Explain the underlined term. (ii) Outline two reasons why entrepreneurs', ' are').split(' (ii)')[0]}", '5', 5,
    [point('r-1', ent[0], 5, 'The explanation, 5 marks. The scheme also accepts its second statement.', accepts=ent[1:])], **B)
for part, concept, ask, nxt, start, end, firsts, word in (
        ('ii', 'why-entrepreneurs-matter', 'Outline two reasons why entrepreneurs are essential for the Irish economy.', ' (iii)',
         'Help create jobs/employment', '1st correct response: 6', ['Help create jobs/employment', 'Improve the Balance of Payments',
                                                                   'Encourage further investment / help create wealth', 'Innovation: new products'],
         'reason'),
        ('iii', 'encouraging-entrepreneurs', 'Outline two actions which the government could take to encourage entrepreneurship', ' (25 marks)',
         'Encourage Enterprise education', '1st correct response: 6', ['Encourage Enterprise education', 'Government policies',
                                                                      'Labour market skills', 'Develop the country’s infrastructure',
                                                                      'Stability in the banking sector'], 'action')):
    add(f'sb-q5-b-{part}', '0-1', concept, ref('B', 5, f'(b)({part})'), H.q(8, ask, nxt), '6 + 4', 10,
        [anyN('r-1', f'A{"n" if word[0] in "aeiou" else ""} {word} — any two', 10, 2, 6, H.split(start, end, firsts),
              f'Two {word}s: the 1st correct response 6 marks, the 2nd 4.', steps=[6, 4])],
        kind='fixed', stem=q5b, **B)
q5c = H.q(8, 'Businesses need factors of production to produce output or provide a service.', ' (i)')
add('sb-q5-c-i', '0-1', 'the-other-factors-of-production', ref('B', 5, '(c)(i)'),
    H.q(8, 'State and explain the three factors of production, other than enterprise.', ' (ii)'), '3 x 5', 15,
    [point(f'r-{f.lower()}', f"{cc(f, whole=True)} — {cc(d, whole=True)}", 5, f'{f}, 5 marks.')
     for f, d in (('Land', 'Anything supplied by nature which helps in the production of output.'),
                  ('Labour', 'The human effort involved in the production of output.'),
                  ('Capital', 'Man-made wealth / machinery used in the production of output.'))],
    stem=q5c, **B)
add('sb-q5-c-ii', '1-2', 'choosing-a-location', ref('B', 5, '(c)(ii)'),
    H.q(8, 'Outline two economic factors which an entrepreneur should consider', ' (25 marks)'), '6 + 4', 10,
    [anyN('r-1', 'A factor — any two', 10, 2, 6,
          H.split('Availability of services\nA business', '1st correct response: 6',
                  ['Availability of services', 'Land for expansion / cost of land / rent of commercial property', 'Regulations: environmental / planning',
                   'Workforce availability', 'Government incentives', 'Proximity to the market / raw materials', 'Social infrastructure']),
          'Two factors: the 1st correct response 6 marks, the 2nd 4.', steps=[6, 4])],
    kind='fixed', stem=q5c, **B)

# Q6 ─ barter, money, inflation; interest rates; banks and credit unions
q6a = H.q(8, 'Explain the following terms:', ' (i)')
for part, concept, term, start, ask, nxt in (('i', 'barter', 'Barter', 'x Swapping/the direct exchange', 'Barter;', ' (ii)'),
                                             ('ii', 'money', 'Money', 'x Anything which is acceptable in payment', 'Money;', ' (iii)'),
                                             ('iii', 'price-inflation', 'Price Inflation', 'x An increase in prices of goods',
                                              'Price Inflation.', ' (21 marks)')):
    add(f'sb-q6-a-{part}', '3-4' if part != 'iii' else '3-3', concept, ref('B', 6, f'(a)({part})'),
        f"{q6a} {H.q(8, ask, nxt).rstrip(';')}", '7', 7,
        [point('r-1', xcell(start), 7, f'{term}, 7 marks: ' + H.traced('3 correct answers: 7 marks each') + '.')], **B)
q6b = H.q(8, 'In November 2013 the ECB reduced interest rates.', ' (i)')
add('sb-q6-b-i', '3-3', 'the-ecb', ref('B', 6, '(b)(i)'), H.q(8, 'What do the initials ECB represent?', ' (ii)'), '9', 9,
    [point('r-1', H.traced('European Central Bank'), 9, 'The name, 9 marks.')], stem=q6b, **B)
add('sb-q6-b-ii', '3-3', 'the-interest-rate', ref('B', 6, '(b)(ii)'),
    f"{q6b} {H.q(8, 'Explain the underlined term. (iii) Discuss three possible', ' economic').split(' (iii)')[0]}", '6', 6,
    [point('r-1', H.traced('Interest rate: the price of money / the cost of borrowing / the return on savings:').rstrip(':'), 6,
           'The explanation, 6 marks.')], **B)
pick('sb-q6-b-iii', '3-3', 'effects-of-lower-interest-rates', ref('B', 6, '(b)(iii)'),
     H.q(8, 'Discuss three possible economic effects of a reduction in interest rates', ' (30 marks)'), 'An effect — any three',
     H.split('Borrowing encouraged / reduced mortgage repayments', '3 points: 5 marks',
             ['Borrowing encouraged / reduced mortgage repayments', 'Savings discouraged / spending encouraged', 'Cost of Servicing the National Debt',
              'Costs of Production / increased competitiveness', 'Economic Growth encouraged', 'Taxation revenues']),
     3, 5, 'Three effects, 5 marks each.', stem=q6b, **B)
q6c = H.q(8, 'A number of retail banks have shut down operations in Ireland', ' (i)')
for part, concept, ask, nxt, start, firsts, word in (
        ('i', 'functions-of-commercial-banks', 'Outline two functions of commercial/retail banks.', ' (ii)', 'Savings Facilities',
         ['Savings Facilities', 'Lending', 'Operate cheque system/current accounts', '24 Hour Banking', 'Foreign Exchange'], 'function'),
        ('ii', 'fewer-banks', 'Outline two economic effects of the reduction in the number of banks', ' (iii)',
         'Inconvenience/ loss of service to customers',
         ['Inconvenience/ loss of service to customers', 'Loss of jobs / re-location of employees', 'Reduced economic activity in rural areas',
          'Increased pressure on Post Office', 'Reduced profits / Reduction in share price', 'Increase in on line banking'], 'effect')):
    add(f'sb-q6-c-{part}', '3-4', concept, ref('B', 6, f'(c)({part})'), H.q(8, ask, nxt), '6 + 4', 10,
        [anyN('r-1', f'A{"n" if word[0] in "ae" else ""} {word} — any two', 10, 2, 6, H.split(start, '1st correct response: 6', firsts),
              f'Two {word}s: the 1st correct response 6 marks, the 2nd 4.', steps=[6, 4])],
        kind='fixed', stem=q6c, **B)
pick('sb-q6-c-iii', '3-4', 'credit-unions-in-difficulty', ref('B', 6, '(c)(iii)'),
     H.q(8, 'Outline one reason why some credit unions are in financial difficulty.', ' (24 marks)'), 'A reason — any one',
     H.split('High Bad debts', '1 reason: 4 marks', ['High Bad debts', 'Too many loans extended', 'Poor governance of CU']),
     1, 4, 'One reason, 4 marks.', stem=q6c, **B)

# Q7 ─ the WTO and barriers; exports; the EU
q7a = H.q(9, 'In December 2013 the WTO reached agreement', ' (i)')
add('sb-q7-a-i', '4-2', 'the-wto', ref('B', 7, '(a)(i)'), H.q(9, 'What do the initials WTO stand for?', ' (ii)'), '7', 7,
    [point('r-1', H.traced('World Trade Organisation'), 7, 'The name, 7 marks.')], stem=q7a, **B)
add('sb-q7-a-ii', '4-2', 'tariffs-and-quotas', ref('B', 7, '(a)(ii)'),
    H.q(9, 'Define each of the following barriers to free trade: tariffs and quotas.', ' (iii)'), '2 x 4', 8,
    [point('r-tariffs', f"{cc('Tariffs', whole=True)} — {cc('This is a tax on imported goods', whole=True)}", 4, 'Tariffs, 4 marks.'),
     point('r-quotas', f"{cc('Quotas', whole=True)} — {cc('This is a limit on the quantity of goods which can be imported', whole=True)}", 4,
           'Quotas, 4 marks.')], stem=q7a, **B)
pick('sb-q7-a-iii', '4-2', 'why-countries-protect', ref('B', 7, '(a)(iii)'),
     H.q(9, 'Discuss two reasons why some countries impose barriers to free trade.', ' (25 marks)'), 'A reason — any two',
     H.split('Protect domestic industries', '2 reasons: 5 marks',
             ['Protect domestic industries', 'Protect domestic employment', 'Protect against ‘Cheap Labour’ economies', 'National Security',
              'To protect human rights / Political motives', 'Production of strategic goods']),
     2, 5, 'Two reasons, 5 marks each.', stem=q7a, **B)
add('sb-q7-b-i', '4-2', 'an-open-economy', ref('B', 7, '(b)(i)'),
    ' '.join([H.q(9, 'Ireland is an example of an "open economy".', ' (ii)')]), '6', 6,
    [point('r-1', H.traced('Open economy: one that engages in trade (importing and exporting).'), 6, 'The explanation, 6 marks.')], **B)
pick('sb-q7-b-ii', '4-2', 'benefits-of-more-exports', ref('B', 7, '(b)(ii)'),
     H.q(9, 'Outline two benefits for the Irish economy of increased exports.', ' (iii)'), 'A benefit — any two',
     H.split('Employment creation\nExports', '2 benefits: 8 marks',
             ['Employment creation', 'Increased GNP / Economic growth', 'Increased sales / profits', 'Earn foreign currencies', 'Attract investment',
              'Government finances']),
     2, 8, 'Two benefits, 8 marks each.', **B)
pick('sb-q7-b-iii', '4-2', 'making-exports-competitive', ref('B', 7, '(b)(iii)'),
     H.q(9, 'State and explain two factors which could make Irish exports more competitive.', ' (30 marks)'), 'A factor — any two',
     H.split('Value of the Euro v. that of other currencies', '2 points: 4 marks',
             ['Value of the Euro v. that of other currencies', 'Irish inflation rates v. that of competitors', 'Costs of production', 'Wage Costs']),
     2, 4, 'Two factors, 4 marks each.', **B)
q7c = H.q(9, 'Croatia is the newest member of the EU', ' (i)')
add('sb-q7-c-i', '4-1', 'the-eu', ref('B', 7, '(c)(i)'), H.q(9, 'What do the initials EU stand for?', ' (ii)'), '5', 5,
    [point('r-1', H.traced('European Union'), 5, 'The name, 5 marks.')], stem=q7c, **B)
pos = ['Larger market / Expansion of Trade', 'Profitable Investment opportunities', 'Source of Labour / New Skills', 'Wage demands moderate']
neg = ['Lower costs of production Firms', 'Decline in funds for investment in Ireland', 'Increase in immigration', 'EU funds As']
pick('sb-q7-c-ii', '4-1', 'effects-of-eu-enlargement', ref('B', 7, '(c)(ii)'),
     H.q(9, 'Discuss three economic effects for the Irish economy of more countries joining the EU.', ' (20 marks)'), 'An effect — any three',
     side('Positive economic effects', [cc(x) for x in pos]) + side('Negative economic effects', [cc(x) for x in neg]),
     3, 5, 'Three effects, 5 marks each, positive or negative.', stem=q7c, **B)

# Q8 ─ emigration; unemployment; economic aims
q8a = H.q(9, '“Ireland has gone from having the highest net immigration levels', ' (i)')
add('sb-q8-a-i', '3-2', 'emigration-and-immigration', ref('B', 8, '(a)(i)'),
    f"{q8a} {H.q(9, 'Explain each of the underlined terms.', ' (ii)')}", '2 x 5', 10,
    [point('r-emigration', H.traced('Emigration: Movement of Irish nationals to reside elsewhere.'), 5, 'Emigration, 5 marks.'),
     point('r-immigration', H.traced('Immigration: Movement of foreign nationals to reside in Ireland'), 5, 'Immigration, 5 marks.')],
    **B)
add('sb-q8-a-ii', '3-2', 'why-emigration-rose', ref('B', 8, '(a)(ii)'),
    H.q(9, 'Discuss two reasons why emigration levels have increased.', ' (iii)'), '6 + 4', 10,
    [anyN('r-1', 'A reason — any two', 10, 2, 6,
          H.split('Economic recession in Ireland / Job opportunities abroad', '1st correct response: 6',
                  ['Economic recession in Ireland / Job opportunities abroad', 'Wage rates in Ireland', 'Rising levels of taxation in Ireland',
                   'Develop skills abroad', 'More optimistic outlook abroad']),
          'Two reasons: the 1st correct response 6 marks, the 2nd 4.', steps=[6, 4])],
    kind='fixed', stem=q8a, **B)
add('sb-q8-a-iii', '3-2', 'effects-of-emigration', ref('B', 8, '(a)(iii)'),
    H.q(9, 'Outline one positive economic effect and one negative economic effect', ' (30 marks)'), '5 + 5', 10,
    [heading('r-positive', H.traced('Positive effects') + ' — any one',
             [cc(x) for x in ('Unemployment reduced Those', 'Emigrants remittances to Ireland', 'Contacts / Export opportunities',
                              'Less demand for state services')], 5, 'One positive effect, 5 marks.'),
     heading('r-negative', H.traced('Negative effects') + ' — any one',
             [cc(x) for x in ('Possible higher dependency ratio', 'Opportunity cost The state', 'Loss of skills within the economy',
                              'Smaller domestic market As', 'Upward pressure on Irish wage levels')], 5, 'One negative effect, 5 marks.')],
    kind='fixed', stem=q8a, **B)
q8b = H.q(9, '“Unemployment is at its lowest level since 2009', ' (i)')
add('sb-q8-b-i', '3-2', 'the-cso', ref('B', 8, '(b)(i)'), H.q(9, 'What do the initials CSO stand for?', ' (ii)'), '10', 10,
    [point('r-1', H.traced('Central Statistics Office'), 10, 'The name, 10 marks.')], stem=q8b, **B)
effects = (('Increased Profits Expansion', ['Increased Profits', 'Expansion'],
            'More employment leading to increased spending power.', ['More employment leading', 'Retailers may be able']),
           ('Tax revenues Social welfare spending Reduced state borrowing Less social problems',
            ['Tax revenues', 'Social welfare spending', 'Reduced state borrowing', 'Less social problems'],
            'Increased employment will result in increased income tax revenues.',
            ['Increased employment will result', 'Expenditure on social welfare', 'The improvement in the state', 'Fewer resources required']),
           ('Increased imports Imports of raw materials Increased exports', ['Increased imports', 'Imports of raw materials', 'Increased exports'],
            'Spending power increases and thus imports', ['Spending power increases', 'Businesses may expand', 'If unemployment is falling']))
opts = []
for heads_line, heads, expl_line, expl_firsts in effects:
    opts += [pair(h, b) for h, b in zip(cut(cc(heads_line, whole=True), heads), cut(cc(expl_line), expl_firsts))]
add('sb-q8-b-ii', '3-2', 'effects-of-falling-unemployment', ref('B', 8, '(b)(ii)'),
    H.q(9, 'Discuss one economic effect which a fall in unemployment may have on each of the following:', ' (25 marks)'), '7 + 4 + 4', 15,
    [anyN('r-1', 'One effect on each — retailers, the government’s finances and the Balance of Trade', 15, 3, 7, opts,
          'One effect for each area: the 1st correct response 7 marks, the 2nd and 3rd 4 each. The scheme’s effects by area: '
          'retailers, increased profits or expansion; the government’s finances, tax revenues, social welfare spending, reduced '
          'state borrowing or fewer social problems; the Balance of Trade, increased imports, imports of raw materials or '
          'increased exports.', steps=[7, 4, 4])],
    kind='fixed', stem=q8b, **B)
q8c = H.q(9, 'Increasing employment is one of the economic aims of the Irish government.', ' (i)')
add('sb-q8-c-i', '3-1', 'other-economic-aims', ref('B', 8, '(c)(i)'),
    H.q(9, 'State and explain two other economic aims of the government.', ' (ii)'), '8 + 4', 12,
    [anyN('r-1', 'An aim — any two', 12, 2, 8,
          H.split('Sustainable government finances / reduce borrowing', '1st correct response: 8',
                  ['Sustainable government finances / reduce borrowing', 'Achieve economic growth', 'Provide efficient state services',
                   'Infrastructural development / broadband access', 'Promote balanced regional development', 'Boost exports / improve competitiveness']),
          'Two aims: the 1st correct response 8 marks, the 2nd 4.', steps=[8, 4])],
    kind='fixed', stem=q8c, **B)
pick('sb-q8-c-ii', '3-1', 'measures-for-the-aims', ref('B', 8, '(c)(ii)'),
     H.q(9, 'Explain one measure the government could take to achieve each economic aim', ' (20 marks)'), 'A measure — one for each aim',
     H.split('Provide efficient state services\nThe government could', '2 correct measures: 4 marks',
             ['Provide efficient state services', 'Infrastructural development', 'Broader tax base', 'Sustainable government finances']),
     2, 4, 'Two measures, 4 marks each: ' + H.traced('Possible responses:').rstrip(':').lower() + '.', stem=q8c, **B)

if __name__ == '__main__':
    emit(cards)
