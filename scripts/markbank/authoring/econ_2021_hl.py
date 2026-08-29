#!/usr/bin/env python3
"""Economics 2021 Higher Level — Section B.

Authored against econ_parts, which reads the tariff and the response headings off
the scheme, so each card states only what a machine cannot decide: the topic, the
question as a student should read it, and whether the part is a menu at all.

`drop` removes the scheme's own scaffolding — "Suggested responses:", the heading
over a list — and, where one part answers two opposite questions, the half a
given card is not about.

The second cell of a pair here — ⟨2 @ 7⟩ ⟨(3 + 4)⟩ — is the split WITHIN one
answer (3 for the point, 4 for developing it), not between the two answers.
Reading it as a descending tariff would halve the marks, so it goes on the row
note instead.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from econ_auto import Paper  # noqa: E402
from econ_lib import anyN, as_option, block, bullets, card, defurnish, load, point, tidy  # noqa: E402

P = Paper(2021, 'higher')
SCAFFOLD = ('Suggested responses', 'Possible responses')

P.menu('positive impacts and two negative', 'econ-2021-hl-q12-a-ii-pos',
       'economics-4-1', 'positive-impacts-of-globalisation',
       'Outline two positive impacts of globalisation.',
       'A positive impact of globalisation — any two',
       'Two impacts, 8 marks each, split 5 for the point and 3 for developing it.',
       ref='2021 HL Q12(a)(ii) — positive impacts',
       drop=SCAFFOLD + ('Positive impacts of globalisation',),
       stop='Negative impacts of globalisation',
       notes='The part asks for two positive AND two negative impacts, and the scheme lists them '
             'under a heading each. Carded one per side, which is the rule for parallel accounts, '
             'so a student is not shown fifteen options to pick two from.')

P.menu('positive impacts and two negative', 'econ-2021-hl-q12-a-ii-neg',
       'economics-4-1', 'negative-impacts-of-globalisation',
       'Outline two negative impacts of globalisation.',
       'A negative impact of globalisation — any two',
       'Two impacts, 5 marks each, split 2 for the point and 3 for developing it.',
       ref='2021 HL Q12(a)(ii) — negative impacts', claim=2, per=5,
       drop=SCAFFOLD + ('Positive impacts of globalisation', 'Trade enhances division',
                        'Improvements in economic growth', 'Reduction in numbers living',
                        'Innovation is encouraged', 'Benefits of economies of scale',
                        'Negative impacts of globalisation'))

P.menu('Evaluate two reasons why the Minister for Finance', 'econ-2021-hl-q12-b-i',
       'economics-3-1', 'reasons-for-the-125-corporation-tax-rate',
       'The Minister for Finance reaffirmed Ireland’s commitment to the 12.5% corporation tax '
       'rate. Evaluate two reasons why the Minister made this decision.',
       'A reason for keeping the 12.5% rate — any two',
       'Two reasons, 7 marks each — split 3 for the reason and 4 for developing it, so a named '
       'reason with nothing after it earns less than half.',
       drop=SCAFFOLD)

P.menu('Discuss two implications of this exit', 'econ-2021-hl-q12-c-i',
       'economics-4-2', 'implications-of-brexit-for-ireland',
       'The United Kingdom left the European Union on January 31, 2020. Discuss two implications '
       'of this exit for the Irish economy.',
       'An implication of Brexit for Ireland — any two',
       'Two implications, 6 marks each, split 3 and 3.',
       drop=SCAFFOLD)

P.menu('advantages to Ireland of remaining a member', 'econ-2021-hl-q12-c-ii',
       'economics-4-1', 'advantages-of-eu-membership',
       'Outline two possible advantages to Ireland of remaining a member of the EU.',
       'An advantage of EU membership — any two',
       'Two advantages, 6 marks each, split 3 and 3.',
       drop=SCAFFOLD)

P.menu('potential advantages to Ireland as a country of maintaining', 'econ-2021-hl-q14-a-ii',
       'economics-3-3', 'advantages-of-low-inflation',
       'Outline the potential advantages to Ireland of maintaining the lowest price inflation '
       'rate relative to the Euro Area and the UK over this period.',
       'An advantage of low inflation — any two',
       'Two advantages, 6 marks each, split 3 and 3.',
       drop=SCAFFOLD,
       stem='Set on a chart of Irish, UK and Euro Area inflation from 2014 to 2019, with Ireland '
            'lowest throughout.')

P.menu('disadvantages to Irish citizens of a low inflation', 'econ-2021-hl-q14-b-i',
       'economics-3-3', 'disadvantages-of-low-inflation',
       'Outline two possible disadvantages to Irish citizens of a low inflation rate in Ireland.',
       'A disadvantage of low inflation — any two',
       'Two disadvantages, 7 marks each, split 3 and 4. The paper asks for the downside of LOW '
       'inflation, which is the harder half of the topic.',
       drop=SCAFFOLD)

P.menu('Continued capital investment in the National Broadband Plan', 'econ-2021-hl-q14-c-ii',
       'economics-4-2', 'broadband-and-competitiveness',
       'Discuss the importance of continued capital investment in the National Broadband Plan '
       'for Ireland’s international competitiveness.',
       'A reason broadband investment matters — any two',
       'Two points, 6 marks each, split 3 and 3.',
       drop=SCAFFOLD + ('Ireland’s international competitiv',))

P.menu('Choose two other areas the Irish Government should focus on', 'econ-2021-hl-q14-c-iii',
       'economics-4-2', 'improving-international-competitiveness',
       'Choose two other areas the Irish Government should focus on to become more '
       'internationally competitive. Justify your choice in each case.',
       'An area to focus on — any two',
       'Two areas, 6 marks each, split 3 for the choice and 3 for the justification.',
       drop=SCAFFOLD)

P.menu('negative implications of this reduction in air passenger', 'econ-2021-hl-q15-b-iii',
       'economics-3-2', 'effects-of-falling-air-passenger-numbers',
       'Outline two negative implications of the reduction in air passenger numbers on the Irish '
       'economy.',
       'A negative implication — any two',
       'Two implications, 5 marks each.',
       drop=SCAFFOLD)

P.menu('reasons for the increase in the number of homeless', 'econ-2021-hl-q16-a-i',
       'economics-2-2', 'causes-of-homelessness',
       'Discuss two reasons for the increase in the number of homeless people in Ireland.',
       'A reason homelessness rose — any two',
       'Two reasons, 6 marks each.',
       drop=SCAFFOLD)

P.menu('economic measures, other than social housing', 'econ-2021-hl-q16-a-ii',
       'economics-1-3', 'measures-to-reduce-homelessness',
       'Outline two economic measures, other than social housing, that could be taken by the '
       'Irish government to help reduce the number of homeless people.',
       'A measure other than social housing — any two',
       'Two measures, 6 marks each. Social housing is excluded by the question.',
       drop=SCAFFOLD + ('Irish government to help reduce',))

# ── Elasticity, which is not a menu ─────────────────────────────────────────
BODY = block(tidy(load(2021, 'higher')), 'Question 12 Possible responses Max Mark', occ=0)
P.cards.append(card(
    'econ-2021-hl-q13-c-ii', 2021, 'higher', 'economics-1-4', 'reading-a-ped-figure',
    '2021 HL Q13(c)(ii)',
    'The Price Elasticity of Demand for Apple Airpods was calculated as −1.63. State whether '
    'demand is elastic or inelastic, and give a reason for your answer.',
    '(4 + 4)', 8,
    [point('r-answer', 'Based upon the above calculation Apple Airpods can be said to be Elastic.',
           4, 'The scheme pays this half for the classification alone.'),
     anyN('r-reason', 'The reason — either one', 4, 1, 4,
          [defurnish(x) for x in block(
              BODY, '• The number is greater than 1',
              '(iii) If the firm selling the above product').split('•') if len(x.strip()) > 12],
          'Either reason earns the second half: the size of the number, or what it means about '
          'the two percentage changes.')],
    'The calculation itself (15 marks) is not carded — it is keyed to figures printed on the '
    'paper. What is carded is reading the answer, which is where marks are lost.',
    tariff_kind='fixed'))

P.cards.append(card(
    'econ-2021-hl-q13-c-iii', 2021, 'higher', 'economics-1-4', 'elasticity-and-revenue',
    '2021 HL Q13(c)(iii)',
    'If the firm selling this product intends to maximise revenue from its sale, should it '
    'increase, decrease, or maintain the same price? Explain your answer.',
    'fixed', 10,
    [point('r-1',
           'As the price elasticity of demand is elastic the firm should decrease price in order '
           'to increase total revenue. A decrease in price will lead to a more than proportionate '
           'increase in quantity demanded than the percentage decrease in price thereby increasing '
           'total revenue.', 10,
           'One point, and the marks are for the mechanism: elastic demand means the quantity '
           'response outweighs the price cut.')],
    '', tariff_kind='fixed'))

# ── Question 11, recovered ──────────────────────────────────────────────────
# Not an oversight in the authoring: the extractor could not see this question.
# Section B used to begin at the first "Question 1x" heading that repeated the
# response-table caption, and on this paper alone that heading is question 12 —
# so question 11's five pages were in neither section's output and could not be
# carded. econ_parts now begins Section B at the first such heading of any kind.
P.menu('Would you consider this market to be competitive', 'econ-2021-hl-q11-a-ii',
       'economics-2-0', 'reading-a-concentration-ratio',
       'Explain why the global aircraft market in 2018 would be considered highly concentrated.',
       'A reason it is highly concentrated — any one',
       'One reason, 5 marks. The part pays 8: 3 for naming the market highly concentrated and 5 '
       'for the explanation, and it is the explanation that is carded.',
       ref='2021 HL Q11(a)(ii)', claim=1, per=5,
       stem='Boeing and Airbus each held 46% of the global aircraft market in 2018, Embraer 5%, '
            'Others 2% and Bombardier 1%.',
       drop=SCAFFOLD + ('Highly concentrated because',))

P.menu('Would you advise the above firm to engage in price competition', 'econ-2021-hl-q11-b-ii',
       'economics-2-0', 'price-competition-in-oligopoly',
       'A firm in oligopoly is at long-run equilibrium. Would you advise it to engage in price '
       'competition? Give two reasons for your answer.',
       'A reason not to compete on price — any two',
       'Two reasons, 4 marks each. Every response the scheme lists argues against price '
       'competition, so the answer the examiner is marking is "no".',
       ref='2021 HL Q11(b)(ii)', drop=SCAFFOLD)

P.menu('small firms such as Embraer and Bombardier', 'econ-2021-hl-q11-b-iii',
       'economics-2-0', 'small-firms-in-an-oligopoly',
       'Outline two reasons why small firms such as Embraer and Bombardier may survive in a '
       'market dominated by two large firms.',
       'A reason a small firm survives — any two',
       'Two reasons, 4 marks each.',
       ref='2021 HL Q11(b)(iii)', drop=SCAFFOLD)

P.menu('Internal Economies of Scale which could arise for Boeing and Embraer',
       'econ-2021-hl-q11-c-ii', 'economics-1-5', 'internal-economies-of-scale',
       'Outline possible internal economies of scale which could arise for Boeing and Embraer if '
       'a merger between them were to occur.',
       'An internal economy of scale — any three',
       'Three economies, 6 marks each.',
       ref='2021 HL Q11(c)(ii)', drop=SCAFFOLD + ('Possible responses',))


# ── A figure card ───────────────────────────────────────────────────────────
# Not cardable until the figure pipeline reached Economics: the answer IS the
# diagram. The four lines cannot be named from the scheme's word list without
# seeing which curve each numeral points at.
P.cards.append(card(
    'econ-2021-hl-q11-b-i', 2021, 'higher', 'economics-2-0', 'labelling-an-oligopoly-diagram',
    '2021 HL Q11(b)(i)',
    'The diagram shows the long-run equilibrium of a firm in oligopoly at point E, producing Q1 '
    'and selling at P1. Write out in full the label for each of the lines numbered 1 to 4.',
    'fixed', 16,
    [point('r-1', 'Marginal Cost', 4, 'Line 1 — the curve rising steeply to the top right.'),
     point('r-2', 'Average (Total) Cost', 4, 'Line 2 — the U-shaped curve above point E.'),
     point('r-3', 'Demand / Average Revenue', 4, 'Line 3 — the kinked line falling to the right.'),
     point('r-4', 'Marginal Revenue', 4, 'Line 4 — the short line dropping steeply below E.')],
    'Abbreviations are not accepted: the part says to write the labels out in full.',
    tariff_kind='fixed',
    figure_key='economics-2021-HL-paper-p16-i0',
    label_key=[{'letter': '1', 'meaning': 'Marginal Cost', 'askedInThisQuestion': True},
               {'letter': '2', 'meaning': 'Average (Total) Cost', 'askedInThisQuestion': True},
               {'letter': '3', 'meaning': 'Demand / Average Revenue', 'askedInThisQuestion': True},
               {'letter': '4', 'meaning': 'Marginal Revenue', 'askedInThisQuestion': True}]))


# ── Section B, second pass ──────────────────────────────────────────────────
P.menu('European Commission want to remove this power', 'econ-2021-hl-q12-b-ii',
       'economics-4-2', 'why-brussels-wants-tax-harmony',
       'Outline one reason why the European Commission wants to remove the power to set '
       'corporation tax from the Irish government.',
       'A reason the Commission wants it — any one', 'One reason, 7 marks.',
       ref='2021 HL Q12(b)(ii)', claim=1, per=7, drop=SCAFFOLD)

P.menu('Government intervention in this market could address', 'econ-2021-hl-q13-b-ii',
       'economics-2-2', 'fixing-information-failure',
       'Misinformation to consumers by technology retailers is a market failure. Evaluate how '
       'Government intervention in this market could address this market failure.',
       'A form of intervention — any one', 'One point, 6 marks.',
       ref='2021 HL Q13(b)(ii)', claim=1, per=6, drop=SCAFFOLD)

P.menu('one advantage of a government regulation', 'econ-2021-hl-q13-b-iii',
       'economics-1-3', 'advantages-of-regulation',
       'Explain, giving an example, one advantage of a government regulation.',
       'An advantage of regulation — any one',
       'One advantage, 6 marks: the marks split between the point and the example.',
       ref='2021 HL Q13(b)(iii)', claim=1, per=6, drop=SCAFFOLD)

P.menu('method the government could use to address rising inflation', 'econ-2021-hl-q14-b-ii',
       'economics-3-3', 'government-tools-against-inflation',
       'Explain one method the government could use to address rising inflation.',
       'A method against inflation — any one', 'One method, 7 marks.',
       ref='2021 HL Q14(b)(ii)', claim=1, per=7, drop=SCAFFOLD)

P.menu('more accurate indicator of Ireland', 'econ-2021-hl-q15-a',
       'economics-3-0', 'gni-or-gdp-for-welfare',
       'Which measure is a more accurate indicator of Ireland’s economic welfare: gross national '
       'income or gross domestic product? Justify your answer.',
       'A case for one measure — either one',
       'One justification, 7 marks. The scheme sets out the case for each measure; gross national '
       'income is the one that counts income actually accruing to Irish residents.',
       ref='2021 HL Q15(a)', claim=1, per=7, drop=SCAFFOLD)

P.menu('negative multiplier effects of large corporations', 'econ-2021-hl-q15-c-iii',
       'economics-3-0', 'the-multiplier-in-reverse',
       'Discuss two possible negative multiplier effects if a large corporation moved its staff to '
       'remote working.',
       'A negative multiplier effect — any two', 'Two effects, 7 marks each.',
       ref='2021 HL Q15(c)(iii)', claim=2, per=7, drop=SCAFFOLD + ('Possible Responses',))

P.menu('one social reason and one economic reason', 'econ-2021-hl-q16-b-ii-social',
       'economics-2-1', 'social-case-for-the-minimum-wage',
       'Explain one SOCIAL reason why the Irish government has increased the national minimum '
       'wage.',
       'A social reason — any one', 'One reason, 5 marks.',
       ref='2021 HL Q16(b)(ii) — social', claim=1, per=5,
       drop=SCAFFOLD + ('Social reasons:',), stop='Economic reasons:',
       notes='The part asks for one of each and the scheme heads the two lists separately, so '
             'each side is its own card.')

P.menu('one social reason and one economic reason', 'econ-2021-hl-q16-b-ii-economic',
       'economics-2-1', 'economic-case-for-the-minimum-wage',
       'Explain one ECONOMIC reason why the Irish government has increased the national minimum '
       'wage.',
       'An economic reason — any one', 'One reason, 5 marks.',
       ref='2021 HL Q16(b)(ii) — economic', claim=1, per=5,
       drop=SCAFFOLD, after='Economic reasons:')

# ── Third pass: the definition-shaped and welded parts ──────────────────────
# Each prints one tariff cell over one stated answer (or a short list of
# alternatives), so these are point/anyN cards sliced with block() — the
# extractor hands them back with the answer welded to the question, or loses
# them to a page boundary, and there is nothing for menu() to claim.
FULL = tidy(load(2021, 'higher'))

# ── Fourth pass: the parts whose question IS a chart ────────────────────────
# These were excluded as "every response reads the chart printed with it", which
# was true and was never a reason: the chart is catalogued, carries verified alt
# text and an md5 the build re-checks, and 159 of this subject's 161 crops
# already name the part they belong to. With the figure bound the student has
# exactly what the candidate in the hall had, and the scheme's responses are
# ordinary prose that quotes the figures off it.
P.cards.append(card(
    'econ-2021-hl-q16-a-i-trend', 2021, 'higher', 'economics-3-2',
    'trend-in-air-passenger-numbers', '2021 HL Q16(a)(i)',
    'Using the data provided above, analyse the trend in the number of passengers handled by '
    'the main Irish airports between 2017 and 2020.',
    '7', 7,
    [point('r-1', as_option(block(FULL, 'Between Q2 2017 and Q2 2019 there is a steady increase',
                                  '(ii) The demand for labour')), 7,
           'One analysis worth 7. The scheme prints the rise and the collapse as a single '
           'response rather than as alternatives, so the trend is not analysed until both '
           'movements are named — and the marks are for quoting the figures, not for the '
           'adjective.')],
    'The id carries a -trend suffix because econ-2021-hl-q16-a-i is taken by a card whose '
    'citation econ_refs.py corrects to Q16(c)(i); an id is never renamed, since it keys a '
    'student\u2019s review history. '
    'The chart is the question. The scheme\u2019s own wording puts the passenger numbers either '
    'side of Q2 2019, which is the shape the graph makes: three years of gentle growth and '
    'then a near-vertical fall.',
    figure_key='economics-2021-HL-paper-p34-art', tariff_kind='fixed'))

P.cards.append(card(
    'econ-2021-hl-q11-c-i', 2021, 'higher', 'economics-1-5',
    'what-internal-economies-of-scale-are', '2021 HL Q11(c)(i)',
    'Boeing and Embraer entered potential merger talks in 2019. If a merger were to occur '
    'between Boeing and Embraer it is likely they would benefit from Internal Economies of '
    'Scale. Define Internal Economies of Scale.',
    '8', 8,
    [point('r-1', as_option(block(FULL, 'Internal economies of scale refer to the decreases',
                                  '(ii) Outline possible Internal Economies')), 8,
           'The definition, 8 marks: falling average total cost as the firm’s own scale of '
           'production grows.')],
    '', tariff_kind='fixed'))

P.cards.append(card(
    'econ-2021-hl-q12-a-i', 2021, 'higher', 'economics-4-1', 'what-globalisation-is',
    '2021 HL Q12(a)(i)',
    'Explain the term globalisation.',
    '1 @ 4', 4,
    [anyN('r-1', 'A definition of globalisation — any one', 4, 1, 4,
          [as_option(block(FULL, 'Globalisation is the process by which the world',
                           'The term globalisation is generally')),
           as_option(block(FULL, 'The term globalisation is generally used to describe',
                           'Globalisation is ability to produce')),
           as_option(block(FULL, 'Globalisation is ability to produce any good or service',
                           '(ii) Outline two positive impacts'))],
          'The scheme prints three alternative definitions; any one earns the 4.')],
    ''))

P.cards.append(card(
    'econ-2021-hl-q13-a-ii', 2021, 'higher', 'economics-1-0', 'how-excess-demand-occurs',
    '2021 HL Q13(a)(ii)',
    'From your diagram above, explain how excess demand occurs.',
    '3 @ 4', 12,
    [anyN('r-1', 'How excess demand occurs — all three steps', 12, 3, 4,
          [as_option(block(FULL, 'At the price of €500 there is more demand',
                           'This indicates that the price charged')),
           as_option(block(FULL, 'This indicates that the price charged in this too low',
                           'By undercharging for the PS5')),
           as_option(block(FULL, 'By undercharging for the PS5 it created additional demand',
                           '(b) Technology retailers mislead'))],
          'Three steps, 4 marks each: demand exceeds the fixed supply at €500, the low price '
          'presses price up towards equilibrium, and the undercharging itself created the '
          'excess demand.')],
    'The diagram completion in (a)(i) carries its own 8 marks and is not this card.',
    stem='The paper’s supply-and-demand diagram shows the PlayStation 5 market with the '
         'retail price fixed at €500, below the equilibrium price P1, so quantity demanded '
         'QX exceeds quantity supplied QE.'))

P.cards.append(card(
    'econ-2021-hl-q13-b-i', 2021, 'higher', 'economics-2-2',
    'information-failure-as-market-failure', '2021 HL Q13(b)(i)',
    'Explain why misinformation to consumers by technology retailers represents a market '
    'failure in this industry.',
    '2 @ 5', 10,
    [anyN('r-1', 'Why it is a market failure — any two', 10, 2, 5,
          bullets(block(FULL, '• Information failure is a form of market failure',
                        'Note Market failure occurs')),
          'Two points, 5 marks each, split 2 and 3.')],
    '',
    stem='Technology retailers mislead shoppers with Black Friday ‘deals’. A survey of '
         '‘before and after’ pricing shows that many products are not discounted as claimed.'))

P.cards.append(card(
    'econ-2021-hl-q14-c-i', 2021, 'higher', 'economics-4-2',
    'the-principle-of-comparative-advantage', '2021 HL Q14(c)(i)',
    'Define the principle of comparative advantage.',
    '3 + 3', 6,
    [point('r-1', as_option(block(FULL, 'Comparative Advantage is the ability of a country',
                                  '(ii) Continued capital investment')), 6,
           'The scheme splits the 6 as 3 + 3: producing at a lower opportunity cost than '
           'another country, and the specialisation that relative opportunity cost drives.')],
    '', tariff_kind='fixed'))

P.cards.append(card(
    'econ-2021-hl-q15-b-i', 2021, 'higher', 'economics-3-0', 'what-a-recession-is',
    '2021 HL Q15(b)(i)',
    'Define the term recession.',
    '4 + 4', 8,
    [point('r-1', as_option(block(FULL, 'A recession refers to a period of negative economic '
                                        'growth',
                                  '(ii) Based upon the graph')), 8,
           'The scheme splits the 8 as 4 + 4: negative economic growth, lasting at least two '
           'quarters.')],
    '', tariff_kind='fixed'))

P.cards.append(card(
    'econ-2021-hl-q15-b-iii-percap', 2021, 'higher', 'economics-3-0',
    'why-per-capita-comparisons-matter', '2021 HL Q15(b)(iii)',
    'With reference to GNI, why is it important to use per capita measures for comparisons '
    'between countries?',
    '1 @ 8', 8,
    [anyN('r-1', 'Why per capita matters — either account', 8, 1, 8,
          [as_option(block(FULL, 'GNI per capita is a more useful measure',
                           ' or If GNI is compared')),
           as_option(block(FULL, 'If GNI is compared on a nominal level',
                           ' or Worked example'))],
          'One answer, 8 marks, split 4 + 4. The scheme also accepts a worked numerical '
          'example making the same point.')],
    ''))

P.cards.append(card(
    'econ-2021-hl-q15-c-i', 2021, 'higher', 'economics-3-0', 'meaning-of-the-multiplier',
    '2021 HL Q15(c)(i)',
    'Explain the term multiplier.',
    '8', 8,
    [point('r-1', as_option(block(FULL, 'The multiplier effect means that any injection',
                                  '(ii) Assume that MPM')), 8,
           'The explanation, 8 marks: an injection raises National Income by more than '
           'itself, and the example shows the scale.')],
    'The multiplier calculation in (c)(ii) is not carded — the response is the worked '
    'formula.', tariff_kind='fixed'))

P.cards.append(card(
    'econ-2021-hl-q16-a-ii-derived', 2021, 'higher', 'economics-2-1',
    'derived-demand-for-labour', '2021 HL Q16(a)(ii)',
    'The demand for labour is said to be a derived demand. Explain this statement in the '
    'context of the aviation data above.',
    '9', 9,
    [point('r-1', as_option(block(FULL, 'The demand for labour in the aviation sector',
                                  '(iii) Outline two negative implications')), 9,
           'One explanation, 9 marks: demand for aviation workers depends on the demand for '
           'flights — labour is demanded for what it produces, not for its own sake.')],
    'The ids econ-2021-hl-q16-a-i and -a-ii are taken by cards whose citation econ_refs.py '
    'corrects to Q16(c); this card is the paper’s actual Q16(a)(ii).',
    tariff_kind='fixed',
    stem='The paper’s chart shows passengers handled by the main Irish airports in Quarter 2 '
         'of each year: a steady rise to just over 10 million in 2019, then a collapse to '
         'virtually zero in Q2 2020.',
    figure_key='economics-2021-HL-paper-p34-art'))


# Q13(a)(i): the completed excess-demand diagram. The scheme itemises eight
# creditable labelled points at 1 mark each; each option below is a verbatim
# contiguous slice of that run, so every one traces. The paper's blank axes
# ride as the card's figure.
_LBL = block(BODY, 'correctly labelled points = 8 marks ', '(ii) From your diagram')
_opts = []
for _cut in ('Price', 'Quantity', 'QE', 'QX', 'D1', 'S1', 'P = €500',
             'Excess Demand from QE to QX'):
    _at = _LBL.index(_cut)
    _opts.append(_LBL[_at:_at + len(_cut)])
P.cards.append(card(
    'econ-2021-hl-q13-a-i', 2021, 'higher', 'economics-1-0',
    'excess-demand-diagram-labels', '2021 HL Q13(a)(i)',
    'Complete the diagram below to indicate how excess demand is occurring in this '
    'market. (*Note: The retail price for a PlayStation 5 Gaming Console was €500)',
    '8 @ 1', 8,
    [anyN('r-1', 'A correctly labelled point on the diagram — all eight', 8, 8, 1,
          _opts,
          'One mark for each correctly labelled point: the axes, the two '
          'quantities, the curves, the price line, and the excess-demand gap.')],
    'The scheme prints the completed diagram and pays 1 mark per labelled point.',
    tariff_kind='fixed',
    figure_key='economics-2021-HL-paper-p22-art'))

# ── Worked calculations the scheme prints in full ──────────────────────────
# Excluded until now as "the response is the worked calculation". That is a
# description of the answer, not a blocker: the scheme sets out the formula, the
# substitution and the result, so every step a student is credited for is on the
# page and traces. Where the figures come off a chart the crop rides with the
# card, because the arithmetic is unanswerable without it.

P.cards.append(card(
    'econ-2021-hl-q15-c-ii', 2021, 'higher', 'economics-3-0',
    'calculating-the-multiplier', '2021 HL Q15(c)(ii)',
    'Assume that MPM is 0.25 and MPC is 0.65 and MPT is 0.10. Calculate the multiplier. Show '
    'all your workings.',
    '8', 8,
    [point('r-1', as_option(block(FULL, 'MPS = 1 \u2013 0.65 = 0.35', '29 |')), 8,
           'MPS has to be derived from MPC before the formula can be used, and the scheme shows '
           'the multiplier written both ways \u2014 over (1-MPC)+MPM+MPT and over MPS+MPM+MPT '
           '\u2014 because they are the same denominator.')],
    'The question gives MPM, MPC and MPT but the formula wants MPS, so the first line of the '
    'answer is a step the question does not ask for.',
    tariff_kind='fixed'))

# ── Worked calculations the scheme prints in full ──────────────────────────
# "The response is the worked calculation" describes the answer, not a blocker.
# The scheme sets out formula, substitution and result, so every step a student
# is credited for is on the page and traces.

P.cards.append(card(
    'econ-2021-hl-q16-b-i', 2021, 'higher', 'economics-2-1',
    'percentage-increase-in-the-minimum-wage', '2021 HL Q16(b)(i)',
    'Calculate the percentage increase in the minimum wage rate between 2016 and 2021.',
    '9', 9,
    [point('r-1', as_option(block(FULL, '10.20 \u22129.15 = 1.05',
                                  '(ii) Explain one social reason')), 9,
           'The scheme prints two routes to the same 11.48%: the rise over the base, or the '
           'ratio of the two rates less 100. Both start from the 2016 rate as the base.')],
    'Both wage rates are read off the chart. The base is 2016, the earlier year, so dividing by '
    'the 2021 rate is the usual error.',
    tariff_kind='fixed',
    figure_key='economics-2021-HL-paper-p35-i0'))

P.emit()
