#!/usr/bin/env python3
"""Economics 2022 Ordinary Level — Section A.

Ordinary Section A is mostly parts with one right answer — complete the table,
calculate the elasticity, tick the substitute goods, say what CSO stands for —
and those are not menu cards. Three parts here ask for a response from a list
the examiner wrote out, and those are carded.

This paper writes its descending tariff as "1st x 9 / 2nd x 6" where others
write "1st @ 8", and prints it beside the question rather than the part, so the
tariffs below are read off the scheme by hand rather than taken from the part.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from econ_auto import Paper  # noqa: E402
from econ_lib import anyN, as_option, block, bullets, card, load, point, tidy  # noqa: E402

P = Paper(2022, 'ordinary', 'A')
SCAFFOLD = ('Possible responses', 'Suggested responses')

P.menu('use the Irish Government would make of the information collected',
       'econ-2022-ol-sa-q2-ii', 'economics-1-3', 'what-the-census-is-used-for',
       'Explain one use the Irish Government would make of the information collected in the '
       'census.',
       'A use for the census — any one',
       'One use, 6 marks.',
       ref='2022 OL Section A Q2(ii)', claim=1, per=6, drop=SCAFFOLD,
       stem='In April 2022 the CSO conducted a census, an official count of Ireland’s population.')

P.menu('Outline one possible reason for this development', 'econ-2022-ol-sa-q3-i',
       'economics-1-1', 'why-consumers-moved-online',
       'More Irish consumers shopped online during 2020 and 2021. Outline one possible reason '
       'for this development.',
       'A reason consumers moved online — any one',
       'One reason, 9 marks: 6 for the reason and 3 for explaining it.',
       ref='2022 OL Section A Q3(i)', claim=1, per=9, drop=SCAFFOLD)

P.menu('advantages for the Irish economy of increasing the minimum wage', 'econ-2022-ol-sa-q5-a',
       'economics-2-1', 'advantages-of-a-higher-minimum-wage',
       'Outline two advantages for the Irish economy of increasing the minimum wage.',
       'An advantage of a higher minimum wage — any two',
       'Two advantages, the first paid 9 and the second 6.',
       ref='2022 OL Section A Q5(a)', steps=[9, 6], drop=SCAFFOLD,
       stem='The government increased the minimum wage by 30c in Budget 2022.')

P.menu('disadvantage of this development for local retailers',
       'econ-2022-ol-sa-q3-ii', 'economics-2-0', 'how-online-shopping-hurts-local-retailers',
       'Outline one possible disadvantage of the growth in online shopping for local retailers.',
       'A disadvantage — any one', 'One disadvantage, 6 for the point and 3 for developing it.',
       ref='2022 OL Section A Q3(ii)', claim=1, per=6, drop=SCAFFOLD)

# ── Second pass: the parts with one printed answer ─────────────────────────
# Definitions and single responses are not menus, so econ_parts has nothing for
# them; each is sliced from the scheme directly. Q5(b) and Q8(i) ARE menus, but
# their tariff cells are printed beside the question number and land in a
# neighbouring segment, so the extractor cannot see the parts at all.
BODY = tidy(load(2022, 'ordinary'))

P.cards.append(card(
    'econ-2022-ol-sa-q1-ii', 2022, 'ordinary', 'economics-3-5', 'what-economic-growth-is',
    '2022 OL Section A Q1(ii)',
    'The diagram shows the forecast growth in the Irish economy for 2020 to 2023. Explain '
    'the term economic growth.',
    'fixed', 6,
    [point('r-1', 'It is the increase in GNP / output (value of goods and services) national '
                  'income per head of population within a country over a period of time / '
                  'increased productive capacity of an economy.', 6,
           'The definition, 6 marks; any of the slash-separated wordings.')],
    'The chart is the Central Bank\u2019s forecast, and the definition has to hold for it: '
    'growth is the RATE of increase, so the four rising columns are growth even where the '
    'column is shorter than the one before it.',
    section='A', tariff_kind='fixed',
    figure_key='economics-2022-OL-paper-p03-i0'))

P.cards.append(card(
    'econ-2022-ol-sa-q2-i', 2022, 'ordinary', 'economics-1-3', 'what-the-cso-is',
    '2022 OL Section A Q2(i)',
    'What do the initials CSO stand for?',
    'fixed', 9,
    [point('r-1', 'Central Statistics Office', 9, 'The name written out in full, 9 marks.')],
    '', stem='In April 2022 the CSO conducted a census, an official count of Ireland’s '
             'population.',
    section='A', tariff_kind='fixed'))

P.cards.append(card(
    'econ-2022-ol-sa-q5-b', 2022, 'ordinary', 'economics-2-1',
    'employee-advantages-of-a-higher-minimum-wage',
    '2022 OL Section A Q5(b)',
    'Outline two advantages for employees of this increase in the minimum wage.',
    '1 @ 9+1 @ 6', 15,
    [anyN('r-1', 'An advantage for employees — any two', None, 2, 9,
          bullets(block(BODY, 'Increased standard of living', '6. The diagram below')),
          'Two advantages, the first paid 9 and the second 6.', steps=[9, 6])],
    'The paper offers Q5 as (a) or (b); the (a) advantages for the Irish economy are carded '
    'as econ-2022-ol-sa-q5-a.',
    stem='The government increased the minimum wage by 30c in Budget 2022.',
    section='A', tariff_kind='fixed'))

P.cards.append(card(
    'econ-2022-ol-sa-q6-ii', 2022, 'ordinary', 'economics-3-2',
    'why-unemployment-rose-in-lockdown',
    '2022 OL Section A Q6(ii)',
    'Outline one reason for the increase in unemployment between Dec 2020 and April 2021.',
    'fixed', 6,
    [point('r-1', 'The imposition of a national lockdown by the government to protect the '
                  'population against the spread of the COVID-19 virus, many businesses were '
                  'forced to let workers go temporarily as they were not able to have their '
                  'businesses open e.g. hairdressers, pubs etc.', 6,
           'The reason, 6 marks.')],
    'Part (i), naming the two peak months, is answered by reading the unemployment graph and '
    'is not carded.',
    stem='Set on a graph of the monthly number of people unemployed from November 2020 to '
         'November 2021.',
    section='A', tariff_kind='fixed'))

P.cards.append(card(
    'econ-2022-ol-sa-q7-a-i', 2022, 'ordinary', 'economics-1-5', 'what-fixed-costs-are',
    '2022 OL Section A Q7(a)(i)',
    'The table shows the costs of production for a bakery for the week: wages €1,000, raw '
    'materials €1,500, light and heat €300, rent of the premises €750. Explain the term '
    'fixed costs.',
    'fixed', 5,
    [point('r-1', 'Costs which do not change as output changes / costs which have to be paid '
                  'even if nothing is produced.', 5, 'The definition, 5 marks.')],
    'The paper offers Q7 as (a) or (b); (a)(ii) is a tick exercise and (b) is the worked '
    'total-cost and net-profit calculation, so neither is carded.',
    section='A', tariff_kind='fixed'))

P.cards.append(card(
    'econ-2022-ol-sa-q8-i', 2022, 'ordinary', 'economics-2-2',
    'positive-externality-of-vaccination',
    '2022 OL Section A Q8(i)',
    'State one example of a positive externality in relation to vaccinations.',
    '1 @ 9', 9,
    [anyN('r-1', 'A positive externality — any one', 9, 1, 9,
          bullets(block(BODY, 'Protection of others from contracting the virus',
                        '(ii) Outline one opportunity cost')),
          'One example, 9 marks: 6 for the point and 3 for developing it.')],
    '', stem='Over half the world population has received at least one dose of a COVID-19 '
             'vaccine — an externality being the external costs or benefits that accrue to '
             'others as a result of production or consumption.',
    section='A'))

P.cards.append(card(
    'econ-2022-ol-sa-q8-ii', 2022, 'ordinary', 'economics-0-1',
    'opportunity-cost-of-the-vaccine',
    '2022 OL Section A Q8(ii)',
    'Outline one opportunity cost for the Irish government of providing the COVID-19 vaccine '
    'for their citizens.',
    'fixed', 6,
    [point('r-1', 'The money the government could have used to provide other services for '
                  'citizens such as childcare subsidy, respite for Carers, improved pensions '
                  'etc.', 6, 'The opportunity cost, 6 marks: 3 for the point and 3 for '
                             'developing it.')],
    '', section='A', tariff_kind='fixed'))

# Carded like econ-2022-ol-q15-a-i-trend: part (i) of Q9 is the worked
# elasticity calculation, the established leave-alone class, but its (ii)
# carries its own printed cell ⟨2⟩ and one printed answer — the same separable
# shape as econ-2025-hl-q14-b-ii-meaning — so the calculation's result is
# folded into the question and the interpretation stands alone.
P.cards.append(card(
    'econ-2022-ol-sa-q9-ii', 2022, 'ordinary', 'economics-1-4', 'interpreting-a-ped-value',
    '2022 OL Section A Q9(ii)',
    'The price of an iPad falls from €750 to €500. As a result, weekly sales of the iPad '
    'increase from 30,000 units to 45,000 units, giving a Price Elasticity of Demand (PED) '
    'of −1. Indicate if the demand is price elastic, price inelastic or unit elastic.',
    'fixed', 2,
    [point('r-1', 'UNIT ELASTIC', 2, 'The one right answer, 2 marks: a PED of exactly −1 is '
                                     'unit elastic.')],
    'Part (i), the worked elasticity calculation, is the established leave-alone class; its '
    'result is folded into the question so this part stands alone.',
    section='A', tariff_kind='fixed'))

# Carded like econ-2022-ol-q15-a-i-trend and -q15-c-i: the scheme prints the
# comparison statement with its figures, so the card holds it rather than
# leaving the part as a chart read.
P.cards.append(card(
    'econ-2022-ol-sa-q10-a', 2022, 'ordinary', 'economics-3-1',
    'comparing-debt-interest-payments',
    '2022 OL Section A Q10(a)',
    'The graph shows the interest paid and forecast to be paid on the general government '
    'debt from 2018 up to 2024. Compare the interest paid on the national debt in 2018 to '
    'the forecasted amount to be paid in 2024, using the data in the graph.',
    'fixed', 15,
    [point('r-1', 'The interest to be paid on the National Debt in 2024 is significantly '
                  'lower (€3.51 bn) than the interest paid on the debt in 2018 of €5.32bn.',
           15, '15 marks (9+3+3): the comparison, and the two supporting figures.')],
    'The paper offers Q10 as (a) or (b); the (b) National Debt definition is carded as '
    'econ-2022-ol-sa-q10-b.',
    stem='Set on a bar chart of the interest paid on the general government debt in '
         '€ billions, 2018 to 2024.',
    section='A', tariff_kind='fixed'))

P.cards.append(card(
    'econ-2022-ol-sa-q10-b', 2022, 'ordinary', 'economics-3-1', 'what-the-national-debt-is',
    '2022 OL Section A Q10(b)',
    'The graph shows the interest paid and forecast to be paid on the general government '
    'debt from 2021 up to 2024. Explain the term National Debt.',
    '1 @ 15', 15,
    [anyN('r-1', 'The definition — either wording', 15, 1, 15,
          ['Refers to the total amount of government borrowing which is outstanding / owed.',
           'Refers to the total amount of money borrowed by the government which is owed.'],
          'One definition, 15 marks (9+3+3).')],
    'The paper offers Q10 as (a) or (b); the (a) comparison is carded as '
    'econ-2022-ol-sa-q10-a.',
    section='A'))

# ── The part whose question IS a chart ─────────────────────────────────────
# Excluded until now as answered by reading the unemployment chart. The crop is
# catalogued with verified alt text, so binding it gives the student what the
# candidate in the hall had, and the scheme names the two months outright.
P.cards.append(card(
    'econ-2022-ol-seca-q6-i', 2022, 'ordinary', 'economics-3-2',
    'peak-months-of-unemployment', '2022 OL Section A Q6(i)',
    'Identify the two months when the number of people unemployed was at its highest.',
    '1 @ 6+1 @ 3', 9,
    [anyN('r-1', 'The two peak months \u2014 both', None, 2, 6,
          [as_option(block(BODY, 'Month 1: March (2021)', '\u27e8')),
           as_option(block(BODY, 'Month 2: April (2021)', '(ii) Outline one reason'))],
          'Both months are wanted and the scheme prices them unevenly: \u27e86+3\u27e9, six for '
          'the first and three for the second. The chart peaks across the spring 2021 lockdown.',
          steps=[6, 3])],
    'The two peaks sit together at the top of the curve, so the pair has to be read off the '
    'chart rather than recalled.',
    section='A', tariff_kind='fixed',
    figure_key='economics-2022-OL-paper-p06-i0'))


# ── Worked calculations the scheme prints in full ──────────────────────────
# "The response is the worked calculation" describes the answer, not a blocker.
# The scheme sets out formula, substitution and result, so every step a student
# is credited for is on the page and traces.

P.cards.append(card(
    'econ-2022-ol-seca-q9-i', 2022, 'ordinary', 'economics-1-1',
    'working-the-ped-formula', '2022 OL Section A Q9(i)',
    'Using the formula above, complete the workings to calculate the Price Elasticity of '
    'Demand (PED) for these iPads.',
    '13', 13,
    [point('r-1', as_option(block(BODY, '\u2206Q 45,000 \u2013 30,000 = 15,000',
                                  'Once the correct figures are inserted')), 13,
           'Each of the four inputs is worked separately before the formula is assembled, and '
           'the scheme is explicit that the answer must carry its minus sign \u2014 a positive '
           '1 is not the same answer.')],
    'The paper prints the formula and the workings frame; the marks are for filling it in the '
    'right order, which is why the scheme works \u2206Q, \u2206P and both sums separately.',
    tariff_kind='fixed', section='A'))

# ── A tick table, answered by the scheme's own completed table ─────────────
# The ✔ is DRAWN, not set in the text layer, so extraction keeps the ticks but
# loses the column each one sits in: the flat run below reads as though all four
# items were ticked in the same column. Nothing in text can fix that, because
# the column IS the answer and the answer is graphical.
#
# So the scheme's completed table is cropped and bound as a SOLUTION figure —
# the same mechanism the Maths deck uses for a printed model solution, hidden
# until reveal and rendered large to be read. The row keeps the scheme's own
# contiguous run so the claim still traces to its document, and the note says
# plainly that the alignment is in the picture, not in the sentence.
P.cards.append(card(
    'econ-2022-ol-seca-q4-ticks', 2022, 'ordinary', 'economics-1-1',
    'substitutes-and-complements-for-the-iphone', '2022 OL Section A Q4',
    'Apple released the iPhone 13 in September 2021. In the table below, identify by placing a '
    'tick (\u2713) which two items are substitute goods and which two items are complementary '
    'goods for the iPhone 13: Samsung S21; iPhone 13 case; iPhone charging plug; Google Pixel '
    '4A smartphone.',
    '15', 15,
    [point('r-1', as_option(block(BODY, 'Substitute Goods Complementary Goods Samsung S21',
                                  '5 | P a g e')), 15,
           'Read the completed table below, not the line above it: the ticks survive extraction '
           'but their COLUMNS do not, so in flat text all four appear to sit together. The '
           'scheme ticks Samsung S21 and the Google Pixel as substitutes \u2014 rival handsets '
           'you would buy INSTEAD of an iPhone \u2014 and the case and the charging plug as '
           'complements, bought ALONGSIDE it. The tariff is \u27e81st x 9\u27e9 then '
           '\u27e83 x 2\u27e9: nine for the first correct categorisation and two for each of '
           'the other three, so the first one right is worth more than the rest together.')],
    'Both substitutes are phones and both complements are accessories, which is the test: a '
    'substitute satisfies the same want, a complement is used with it.',
    section='A', tariff_kind='fixed',
    figure_key='economics-2022-OL-scheme-p06-q4-ticks'))


# ── Tick tables, answered by the scheme's own completed table ──────────────
# See econ_tick_crop.py: the ✔ is drawn, so extraction keeps it and loses the
# column. The completed table is bound as a SOLUTION crop, hidden until reveal.

P.cards.append(card(
    'econ-2022-ol-seca-q7-a-ii-ticks', 2022, 'ordinary', 'economics-1-5',
    'sorting-fixed-and-variable-costs', '2022 OL Section A Q7(a)(ii)',
    'Indicate by means of a tick (\u2713) which of the costs in the table below are fixed costs '
    'and which are variable costs: Wages \u20ac1,000; Raw Materials \u20ac1,500; Light & Heat '
    '\u20ac300; Rent of the premises \u20ac750.',
    '4+4+1+1', 10,
    [point('r-1', as_option(block(BODY, 'Fixed Cost Variable Cost Wages', '(b) OR A bakery')), 10,
           'Read the completed table below. Only the rent is FIXED \u2014 it is owed whether the '
           'bakery bakes or not. Wages, raw materials and light & heat all move with output, so '
           'all three are variable. The tariff is uneven, \u27e84+4+1+1\u27e9: the first two '
           'right are worth four each and the last two one each.')],
    'Three of the four are variable, so a student splitting them evenly gets one wrong before '
    'thinking about any of them.',
    section='A', tariff_kind='fixed',
    figure_key='economics-2022-OL-scheme-p09-q7aii-ticks'))

P.emit()
