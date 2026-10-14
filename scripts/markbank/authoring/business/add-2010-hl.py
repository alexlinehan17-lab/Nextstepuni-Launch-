"""Review the 2010 Higher English paper outside its ABQ (Sections 1 and 3).

2010 Higher: answer eight of ten short questions at 10 marks (Section 1),
the compulsory Applied Business Question (Section 2, carded by
add-2010-abq.py and left untouched here) and four of seven long questions
at 60 (Section 3), all in one twelve-page booklet (LC033ALP000EV, the same
file id as its scheme). No card existed for Sections 1 and 3, so every card
is new. The allocation summary (scheme pages 4 and 6-9) sets each boundary;
printed sub-parts with their own published marks are separate cards.

Section 3 Q1(B) prints (i) the Small Claims Court and (ii) the Ombudsman,
but the summary publishes 7 + 7 + 6 with an evaluation "in each case", not
a mark per sub-part, so it is one card. One printed choice is one card:
Q3(C) any two of three EU policies, marked alike (10 each).

The text layer of paper page 10 also carries an unprinted copy of Q6(B)
("Outline two benefits to 'Marie's Pizzas'...") above Q6(A); nothing is
printed there on the rendered page, so it is not lifted.
"""
from bus_lib import (Paper, ORIGINAL, comps, points, seq, unequal, single, response, fixed, permit)

T = {(1, q): 4 for q in range(1, 11)}
T.update({(3, 1): 6, (3, 2): 6, (3, 3): 7, (3, 4): 8, (3, 5): 8, (3, 6): 9, (3, 7): 9})
P = Paper(2010, 'higher', {1: 'LC033ALP000EV', 3: 'LC033ALP000EV'}, 'LC033ALP000EV', T)
L, S, add, cum = P.lift, P.scheme, P.add, P.cumulative


def flat(card):
    for r in card['rubric']['responses']:
        for a in r['allocations']:
            a['permittedMarks'] = [0, a['maxMarks']]
    return card


# ---------------------------------------------------------------- Section 1 (10 marks each)
ind_a = L(1, 2, '(a) Illustrate your understanding of the term ‘Indigenous firm’.')
add(1, 1, 'a', 'Q1(a)', ind_a, 4, 'business-5-15', 'indigenous-firm-2010', 2, [10], 'Illustration with an example: 4 marks (2 + 2).', [comps('Indigenous firm', (2, 2))],
    ['The allocation summary adds “' + S(4, 'Example required') + '”. Scheme: '
     + S(10, 'An indigenous firm is an Irish/ native/ locally based business that has been established and is owned/managed by Irish people/residents.')])
add(1, 1, 'b', 'Q1(b)', ind_a + '\n' + L(1, 2, '(b) State two benefits of promoting the development of ‘Indigenous firms’ for the Irish economy.'), 6, 'business-5-15',
    'indigenous-firm-benefits-2010', 2, [10], 'Two benefits at 3 marks each (1 + 2).', points('Benefit', 2, (1, 2)),
    ['Scheme examples: ' + S(10, 'Profit Distribution: They re-invest their profits in Ireland, and spend within the economy.') + ' '
     + S(10, 'Taxation: Source of revenue for the Government through VAT, Corporation Tax etc')])
add(1, 2, '', 'Q2', L(1, 2, 'Distinguish between ‘Prototype Development’ and ‘Test Marketing’ as stages in the development process of a new product.'), 10, 'business-4-14',
    'prototype-and-test-marketing', 2, [10], 'Each stage 5 marks (3 + 2).', [comps('Prototype Development', (3, 2), None, 1), comps('Test Marketing', (3, 2), None, 2)],
    ['Scheme: ' + S(10, 'Prototype development is the creation of the first working model/mock-up/sample of a new product')])
fx_a = L(1, 2, '(a) Explain what is meant by the term ‘Exchange rate’.')
add(1, 3, 'a', 'Q3(a)', fx_a, 6, 'business-6-13', 'exchange-rate-2010', 2, [11], 'Explanation: 6 marks (3 + 3).', [comps('Exchange rate', (3, 3))],
    ['Scheme: ' + S(11, 'Exchange rate is the price at which a currency can be exchanged for another')])
add(1, 3, 'b', 'Q3(b)', fx_a + '\n' + L(1, 2, '(b) Outline two impacts on Irish Exporters to the UK market, if the euro (€) increases in value relative to the UK pound sterling (£).'), 4,
    'business-6-13', 'stronger-euro-exporters', 2, [11], 'Two impacts at 2 marks each.', points('Impact', 2, (2,)),
    ['Scheme examples: ' + S(11, 'Irish exports to the UK become more expensive/less competitive/lower profit margins if the euro increases in value relative to the Pound Sterling.') + ' '
     + S(11, 'Exporters may have to change markets/export to other EU countries')])
cum(1, 4, '', 'Q4', '\n'.join([L(1, 3, 'Column 1 is a list of EU Institutions. Column 2 is a list of possible explanations of these institutions. (One explanation does not relate to any of the institutions)'),
                               L(1, 3, '1. European Parliament', '2. European Commission', '3. European Court of Justice', '4. Court of Auditors',
                                 '5. Council of the European Union (Council of Ministers)'),
                               L(1, 3, 'A. Draws up proposals for new EU law.', 'B. Most important decision-making body in the EU.', 'C. Ensures the EU budget is spent efficiently.',
                                 'D. Is responsible for ensuring the correct interpretation and application of EU laws by member states.',
                                 'E. Is responsible for managing the euro currency and the EUs monetary policy.', 'F. Directly elected by EU citizens.'),
                               L(1, 3, 'Match the two lists by placing the letter of the correct explanation under the relevant number below.')]),
    (2, 2, 2, 2, 2), 'business-6-14', 'eu-institutions-matching-2010', 3, [11], 'Answer key (scheme page 11): 1 F; 2 A; 3 D; 4 C; 5 B. Explanation E is unused.', noun='matches')
S(11, '4. 1 2 3 4 5 F A D C B')
arts_a = L(1, 3, '(a) Outline the purpose of a company’s ‘Articles of Association’.')
add(1, 5, 'a', 'Q5(a)', arts_a, 4, 'business-5-14', 'articles-purpose-2010', 3, [11], 'Purpose: 4 marks.', [comps('Articles of Association', (4,))],
    ['Scheme: ' + S(11, 'The Articles of Association is the internal \'rule book\' /internal rules/regulations that every incorporated firm must have and work by.')])
cum(1, 5, 'b', 'Q5(b)', arts_a + '\n' + L(1, 3, '(b) List three items of information included in the ‘Articles of Association’.'), (2, 2, 2), 'business-5-14', 'articles-items-2010', 3, [11],
    'Scheme items (page 11): ' + S(11, '(i) Capital: The amount of share capital/The different classes of shares. (ii) Regulations re Meetings:') + ' ...', noun='items')
chart = (L(1, 4, 'Study the break-even chart below and answer the following questions in the Answer Box provided:')
         + '\n(Break-even chart, printed as an image: Revenue/Costs in ' + L(1, 4, '€ ’000s') + ' against Units ’000s, with TR, TC and FC lines.)')
key = 'Scheme (page 12): ' + S(12, '(i) Break even point in units- 4,000 units Break even point in euro-€40,000 (ii) Profit at forecast sales- €30,000 (iii) Margin of safety- 6,000 units') + '.'
flat(add(1, 6, 'i', 'Q6(i)', chart + '\n' + L(1, 4, '(i) Break-even point (BEP) in units and in euros'), 4, 'business-3-19', 'bep-units-and-euros-2010', 4, [12],
         'Units 2 and euros 2.', [comps('Break-even point', (2, 2), ['In units', 'In euros'])], [key]))
flat(add(1, 6, 'ii', 'Q6(ii)', chart + '\n' + L(1, 4, '(ii) The Profit at Forecast Sales (10,000units) in euros.'), 3, 'business-3-19', 'profit-at-forecast-2010', 4, [12],
         'Profit: 3 marks.', [comps('Profit at forecast sales', (3,))], [key]))
flat(add(1, 6, 'iii', 'Q6(iii)', chart + '\n' + L(1, 4, '(iii) Margin of safety (MOS) in units.'), 3, 'business-3-19', 'margin-of-safety-2010', 4, [12],
     'Margin of safety: 3 marks.', [comps('Margin of safety', (3,))], [key]))
ins = L(1, 4, 'Illustrate the difference between the insurance principles ‘Insurable Interest’ and ‘Indemnity’.')
add(1, 7, 'a', 'Q7(a)', ins + '\n' + L(1, 4, '(a) Insurable interest is:'), 5, 'business-3-17', 'insurable-interest-2010', 4, [12], 'Illustration with an example: 5 marks (3 + 2).',
    [comps('Insurable interest', (3, 2))], ['Scheme: ' + S(12, 'The policy holder must benefit by the continued existence of the object and suffer by its loss.')])
add(1, 7, 'b', 'Q7(b)', ins + '\n' + L(1, 4, '(b) Indemnity is:'), 5, 'business-3-17', 'indemnity-2010', 4, [12], 'Illustration with an example: 5 marks (3 + 2).',
    [comps('Indemnity', (3, 2))], ['Scheme: ' + S(12, 'There can be no profit from insurance, only recovery of the actual loss.')])
add(1, 8, '', 'Q8', L(1, 4, 'Distinguish between a Quota and a Tariff as barriers to free trade between countries.'), 10, 'business-6-13', 'quota-and-tariff-2010',
    4, [12], 'Each barrier 5 marks.', [comps('Quota', (5,), None, 1), comps('Tariff', (5,), None, 2)],
    ['Scheme: ' + S(12, 'Quota: is a physical restriction/limit on the number of units of a good that may be imported/exported.') + ' '
     + S(12, 'Tariff: this is a tax on the value/price of goods imported.')])
add(1, 9, '', 'Q9', L(1, 5, 'Outline three grounds for fair dismissal under the terms of Unfair Dismissals Act 1977/93.'), 10, 'business-0-14', 'fair-dismissal-grounds-2010',
    5, [12], 'Three grounds: 4 (2 + 2), 3 (1 + 2) and 3 (1 + 2).', unequal('Ground', [(2, 2), (1, 2), (1, 2)], None),
    ['The 4-mark allowance is not tied to a particular ground. Scheme examples: ' + S(12, '(i) Incompetence on the part of the employee.') + ' ' + S(12, '(iii) Misconduct by the employee.')])
pay_a = L(1, 5, '(a) From the following figures calculate the net pay of Hazel Dunne.') + '\nGross Pay €50,000, Tax Credits €6,000\nStandard Tax Rate 20%\nHigher Tax Rate 41%\nCut-off Point €36,400\nWorkings:'
L(1, 5, 'Gross Pay €50,000, Tax Credits €6,000 Standard Tax Rate 20% Higher Tax Rate 41% Cut-off Point €36,400')
flat(add(1, 10, 'a', 'Q10(a)', pay_a, 7, 'business-3-18', 'net-pay-hazel-dunne', 5, [13], 'Calculation: seven figures at 1 mark each.',
         [fixed('Net pay', [('€36,400 taxed at 20%: €7,280', 1), ('Balance €13,600', 1), ('€13,600 taxed at 41%: €5,576', 1), ('Gross tax €12,856', 1),
                            ('Less credits €6,000', 1), ('Tax payable €6,856', 1), ('Net pay €43,144', 1)])],
         ['Scheme (page 13): ' + S(13, 'Gross Pay 50,000 36,400 Taxed at 20% 7280 (1) (1)13,600 Taxed at 41% 5576 (1) Gross Tax 12856 (1) Less Credits 6000 (1) Tax Payable 6,856 (1) Net Pay 43,144 (1)') + '.']))
add(1, 10, 'b', 'Q10(b)', L(1, 5, '(b) State two tax credits a person may be entitled to.'), 3, 'business-3-18', 'tax-credits-named-2010', 5, [13],
    'Two tax credits: 2 and 1.', unequal('Tax credit', [(2,), (1,)], None),
    ['Scheme examples: ' + S(13, 'Personal Tax credit (single, married, widowed) PAYE Tax credit Age Tax credit') + '.'])

# ---------------------------------------------------------------- Section 3 (60 marks each)
ir = L(3, 7, 'The purpose of the Industrial Relations Act, 1990 is to put in place an improved framework for the conduct of industrial relations and for the resolution of trade disputes.')
ir_i = L(3, 7, '(A) (i) Outline the impact on trade unions of the main provisions of the Industrial Relations Act 1990.')
add(3, 1, 'a-i', 'Q1(A)(i)', ir + '\n\n' + ir_i, 18, 'business-0-14', 'ira-1990-impact', 7, [20, 21], 'Three provisions at 6 marks each (3 + 3).', points('Provision', 3, (3, 3)),
    ['Scheme examples: ' + S(20, 'Secret Ballots Under the provisions of the Industrial Relations Act 1990 no strike or other industrial action can take place without a secret ballot.') + ' '
     + S(21, 'Immunity The Industrial Relations Act 1990 states the trade unions and workers are immune from legal action/prosecution for damages or losses suffered by the employer as a result of a trade dispute.')])
add(3, 1, 'a-ii', 'Q1(A)(ii)', ir + '\n\n' + ir_i + '\n' + L(3, 7, '(ii) Describe two types of official industrial action a trade union can undertake as part of a trade dispute.'), 12, 'business-0-14',
    'official-industrial-action-2010', 7, [21], 'Two types at 6 marks each (3 + 3).', points('Type of industrial action', 2, (3, 3)),
    ['Scheme examples: ' + S(21, '1. Work to Rule/ Overtime Ban:') + ' ' + S(21, '2. ‘Go Slow’')])
add(3, 1, 'b', 'Q1(B)', ir + '\n\n' + L(3, 7, '(B) Evaluate the role of each of the following in protecting consumers: (i) The Small Claims Court; (ii) The Office of the Ombudsman for Public Services.'), 20,
    'business-0-13', 'small-claims-and-ombudsman', 7, [21, 22], 'Two distinct points for each body, 7 (4 + 3) each, and an evaluation of each, 6 (3 + 3).',
    [comps('The Small Claims Court', (4, 3), None, 1), comps('The Office of the Ombudsman for Public Services', (4, 3), None, 2),
     comps('Evaluation of each', (3, 3), ['The Small Claims Court', 'The Office of the Ombudsman for Public Services'], 3)],
    ['The allocation summary prints “' + S(6, '(2 distinct points in each case) Evaluation/judgement required in each case 7 marks (4+3) 7 marks (4+3) 6 marks (3+3)') + '”, not a mark per sub-part, so this is one card.',
     'Scheme: ' + S(22, 'It is a fast/informal and easy way for consumers to resolve disputes.') + ' '
     + S(22, 'The Office of the Ombudsman investigates complaints about the activities of Government Departments, the Health Service Executive, local authorities and An Post.')])
add(3, 1, 'c', 'Q1(C)', ir + '\n\n' + L(3, 7, '(C) In relation to the Law of Contract, illustrate your understanding of Capacity to Contract.'), 10, 'business-0-12', 'capacity-to-contract-2010',
    7, [23], 'Illustration with an example: 5 + 5.', [comps('Capacity to contract', (5, 5))],
    ['The allocation summary adds “' + S(6, 'Example required') + '”. Scheme: '
     + S(23, 'Capacity to contract means that all natural persons (human beings) and legal/corporate persons, such as companies, have the legal right to enter into a contract.')])

green = L(3, 7, 'Customers expect businesses to show regard for the natural environment.')
add(3, 2, 'a', 'Q2(A)', green + '\n\n' + L(3, 7, '(A) Illustrate the characteristics of an environmentally conscious business.'), 20, 'business-5-17', 'environmentally-conscious-business',
    7, [23, 24], 'Four characteristics, each stated, explained and exemplified: 5 marks each (1 + 2 + 2).', points('Characteristic', 4, (1, 2, 2), ['State', 'Explain', 'Example']),
    ['Scheme examples: ' + S(23, 'Honesty/Openness The company tells the truth and is above board in all matters affecting the environment.') + ' '
     + S(24, 'Compliant with the law Conducts business with integrity and complies with the environmental laws and regulations.')])
add(3, 2, 'b', 'Q2(B)', green + '\n\n' + L(3, 7, '(B) Outline the reasons why a business may change its organisational structure from a ‘Sole Trader’ to a ‘Private Limited Company’.'), 20,
    'business-5-14', 'sole-trader-to-company', 7, [24, 25], 'Four reasons at 5 marks each (2 + 3).', points('Reason', 4, (2, 3)),
    ['Scheme examples: ' + S(25, 'Finance/Borrowing May be easier to raise finance from financial institutions.') + ' '
     + S(25, 'Continuity of existence It is easier to pass a company on from one generation to another')])
add(3, 2, 'c', 'Q2(C)', green + '\n\n' + L(3, 7, '(C) Discuss the different ways in which the Irish Government affects the labour force in Ireland.'), 20, 'business-5-15',
    'government-and-labour-force', 7, [25, 26], 'Four ways at 5 marks each (2 + 3).', points('Way', 4, (2, 3)),
    ['Scheme examples: ' + S(25, 'As an Employer: The Irish government is the single largest employer') + '; ' + S(25, 'Taxation policies/Fiscal Policies:') + '.'])

glob = L(3, 8, 'Ireland is ranked the third most globalised nation behind Singapore and Hong Kong.')
open_i = L(3, 8, '(A) (i) Explain what is meant by the term ‘Open Economy’.')
add(3, 3, 'a-i', 'Q3(A)(i)', glob + '\n\n' + open_i, 6, 'business-6-13', 'open-economy-2010', 8, [26], 'Explanation: 6 marks (3 + 3).', [comps('Open Economy', (3, 3))],
    ['Scheme: ' + S(26, 'Open Economy is one in which people including businesses can trade goods and services (i.e. importing and exporting) and borrow and lend in world financial markets.')])
add(3, 3, 'a-ii', 'Q3(A)(ii)', glob + '\n\n' + open_i + '\n' + L(3, 8, '(ii) Illustrate your understanding of the terms, ‘Balance of Trade’ and ‘Balance of Payments’.'), 14,
    'business-6-13', 'bot-and-bop-explained-2010', 8, [26, 27], 'Each term 7 marks (3 + 2 + 2), with examples.',
    [comps('Balance of Trade', (3, 2, 2), None, 1), comps('Balance of Payments', (3, 2, 2), None, 2)],
    ['The allocation summary adds “' + S(7, 'Examples required') + '”. Scheme: ' + S(26, 'Balance of Trade = Visible Exports - Visible Imports') + '; '
     + S(27, 'Balance of Payments = Total Exports (Visible & Invisible) - Total Imports (Visible & Invisible)') + '.'])
add(3, 3, 'b', 'Q3(B)', glob + '\n\n' + L(3, 8, '(B) Analyse how the changing trends in the international economy have impacted on Irish businesses.'), 20, 'business-6-15',
    'international-trends-2010', 8, [27, 28], 'Four trends at 5 marks each (2 + 3).', points('Trend', 4, (2, 3)),
    ['Scheme examples: ' + S(27, 'Currency fluctuations: Irish exporters are being hit by the international recession and the collapse in the value of sterling.') + ' '
     + S(28, 'Deregulation: has increased competition in the marketplace and reduced protectionism i.e. removal of trade barriers.')], extra=['business-6-13'])
add(3, 3, 'c', 'Q3(C)', glob + '\n\n' + L(3, 8, '(C) Discuss the importance for Ireland of any two of the following EU policies: (i) Competition Policy; (ii) Common Fisheries Policy (CFP); (iii) Common Agricultural Policy (CAP).'),
    20, 'business-6-14', 'eu-policies-choice-2010', 8, [29], 'Choose two of the three policies: each 10 marks, two distinct points at 5 (2 + 3).',
    seq(points('First policy you chose: point', 2, (2, 3)), points('Second policy you chose: point', 2, (2, 3))),
    ['You choose which two of the three printed policies to discuss. The scheme marks every choice alike (10 each, two points at 5), so this is one card whichever policies you choose.',
     'Competition Policy (scheme PDF page 29): “' + S(29, 'It ensures that Irish businesses operate on a fair basis and that customers benefit.') + '”',
     'Common Fisheries Policy (CFP) (scheme PDF page 29): “' + S(29, 'Conservation of Irish Fish Stocks: This policy is designed to protect fish stocks over-fishing.') + '”',
     'Common Agricultural Policy (CAP) (scheme PDF page 29): “' + S(29, 'Promotes a fair standard of living for farmers who have always seen their average incomes lag behind average industrial earnings.') + '”'])

swot_i = L(3, 9, '(A) (i) What is meant by the term SWOT analysis?')
add(3, 4, 'a-i', 'Q4(A)(i)', swot_i, 6, 'business-2-13', 'swot-meaning-2010', 9, [30], 'Explanation: 6 marks (4 + 2).', [comps('SWOT analysis', (4, 2))],
    ['Scheme: ' + S(30, 'It is used to assess/evaluate a business in terms of strengths, weaknesses, opportunities and threats.')])
add(3, 4, 'a-ii', 'Q4(A)(ii)', swot_i + '\n' + L(3, 9, '(ii) Conduct a SWOT analysis on a business of your choice. (Include two points under each heading)'), 14, 'business-2-13', 'swot-analysis-conducted-2010',
    9, [30], 'Name the business 2, then two appropriate points under each of the four headings at 3 each (2 + 1).',
    seq(single('Business named', 2, 'A real business named'), comps('Strengths', (2, 1)), comps('Weaknesses', (2, 1)), comps('Opportunities', (2, 1)), comps('Threats', (2, 1))),
    ['The allocation summary prints “' + S(8, 'Name of a Business 4 Headings: 2 appropriate points under each heading') + '”. Scheme example (Ryanair): '
     + S(30, 'Internet site (94% bookings) www.ryanair.com: Lowers the cost of bookings.')])
add(3, 4, 'b', 'Q4(B)', L(3, 9, '(B) Analyse the contributions that strategic and tactical planning can make to the successful management of a business. Use examples in your answer.'), 20,
    'business-2-13', 'strategic-and-tactical-planning-2010', 9, [31], 'Strategic planning 10 (4 + 4 + 2) and tactical planning 10 (4 + 4 + 2), one example of each.',
    [comps('Strategic planning', (4, 4, 2), None, 1), comps('Tactical planning', (4, 4, 2), None, 2)],
    ['Scheme: ' + S(31, 'Strategic planning is long term, made by top management.') + ' ' + S(31, 'Tactical planning is short term')])
add(3, 4, 'c', 'Q4(C)', L(3, 9, '(C) Discuss the benefits of a functional organisational structure in a business. Refer to the Chain of Command and Span of Control in your answer.'), 20,
    'business-2-13', 'functional-structure-2010', 9, [31, 32], 'Two benefits at 5 (2 + 3), the chain of command 5 (2 + 3) and the span of control 5 (2 + 3).',
    seq(points('Benefit', 2, (2, 3)), comps('Chain of Command', (2, 3)), comps('Span of Control', (2, 3))),
    ['Scheme: ' + S(32, 'The chain of command is the line/path on which orders/instructions and decisions are passed down from top to bottom of the hierarchy and feedback is passed back up.') + ' '
     + S(32, 'A span of control is the number of people who report directly to one manager in a hierarchy.')])

appraisal = L(3, 9, 'Performance appraisals are a valuable way to communicate with employees and may boost business productivity in difficult times.')
pa_i = L(3, 9, '(A) (i) Explain what is meant the term performance appraisal.')
add(3, 5, 'a-i', 'Q5(A)(i)', appraisal + '\n\n' + pa_i, 5, 'business-3-20', 'performance-appraisal-2010', 9, [33], 'Explanation: 5 marks (2 + 3).', [comps('Performance appraisal', (2, 3))],
    ['Scheme: ' + S(33, 'Performance appraisal is reviewing the performance of the employees in business.')])
add(3, 5, 'a-ii', 'Q5(A)(ii)', appraisal + '\n\n' + pa_i + '\n' + L(3, 9, '(ii) Outline the benefits of performance appraisal for a business.'), 15, 'business-3-20',
    'performance-appraisal-benefits-2010', 9, [33], 'Three benefits at 5 marks each (2 + 3).', points('Benefit', 3, (2, 3)),
    ['Scheme examples: ' + S(33, 'Opportunity to review rewards (benefits structures):') + ' ' + S(33, 'Increased productivity:')])
ces = (L(3, 9, '(B) From the figures given below for 2009 calculate the following for CES Ltd.:')
       + '\nInformation for 2009\nSales | €135,000\nNet profit | €33,750\nCurrent Assets ( including closing stock) | €84,500\nCurrent Liabilities | €65,000\n'
       + 'Closing Stock | €39,000\nOrdinary Share Capital | €300,000\nLong Term Debt | €192,000\nRetained Earnings | €20,000')
L(3, 9, 'Information for 2009 Sales €135,000 Net profit €33,750 Current Assets ( including closing stock) €84,500 Current Liabilities €65,000 Closing Stock €39,000 Ordinary Share Capital €300,000 Long Term Debt €192,000 Retained Earnings €20,000')
ratio_scheme = 'The allocation summary prints “' + S(8, '4 Ratios 4 @ 5 marks Ratio formula 4@2 marks Calculation 4@(1+1+1)') + '”.'
for suffix, item, name, working in [
        ('b-i', '(i) Net profit margin;', 'Net profit margin', S(34, '(i) Net Profit Margin = Net Profit x 100 Sales 1 33,750 x 100 135,000 1 = 25%')),
        ('b-ii', '(ii) Current ratio;', 'Current ratio', S(34, '(ii) Current Ratio = Current Assets: Current Liabilities 84,500: 65,000 1.3:1')),
        ('b-iii', '(iii) Acid Test ratio;', 'Acid Test ratio', S(34, '(iii) Acid Test Ratio = Current Assets – Closing Stock: Current Liabilities 84,500 – 39,000: 65,000 45,500:65,000 0.7:1')),
        ('b-iv', '(iv) Debt Equity ratio.', 'Debt Equity ratio', S(34, '(iv) Debt Equity ratio = Debt: Equity/ (Ordinary share capital + Retained Earnings) 192,000:300,000 + 20,000 192,000:320,000 0.6 :1'))]:
    flat(add(3, 5, suffix, f'Q5(B)({suffix[2:]})', appraisal + '\n\n' + ces + '\n' + L(3, 9, item), 5, 'business-3-19', f'ces-{name.lower().replace(" ", "-")}-2010',
             9, [34], 'Formula 2 and the calculation 3 (1 + 1 + 1).',
             [response(1, name, [('formula', 'Formula', 2), ('figure-1', 'Figure', 1), ('figure-2', 'Figure', 1), ('answer', 'Answer', 1)])],
             [ratio_scheme, 'Scheme (page 34): ' + working + '.']))
results = L(3, 9, 'RESULTS 2008') + '\nNet profit margin | 32%\nCurrent ratio | 2:1\nAcid test ratio | 1.1:1\nDebt Equity Ratio | 0.4:1'
L(3, 9, 'RESULTS 2008 Net profit margin 32% Current ratio 2:1 Acid test ratio 1.1:1 Debt Equity Ratio 0.4:1')
trends = L(3, 9, '(C) Analyse the significance of the trends over the two years (2008/2009) for the following stakeholders:')
note = L(3, 9, 'NOTE: Results for 2008 are already calculated above.')
for suffix, item, name, marks, example in [
        ('c-i', '(i) Investors/shareholders;', 'Investors/shareholders', (1, 2, 3),
         S(35, 'In this situation Investors/Shareholders may not be satisfied as there was a drop of 7% from 2008(32%) to 2009(25%).')),
        ('c-ii', '(ii) Suppliers;', 'Suppliers', (1, 2, 5),
         S(35, 'In 2008 the business had €1.10 available immediately to pay for every €1 it owed. The situation deteriorated in 2009 with the business only having 70c available to pay for every €1 it owes.')),
        ('c-iii', '(iii) Employees.', 'Employees', (1, 2, 3),
         S(35, 'The drop in the NPM% diminishes their chances of obtaining a pay increase.'))]:
    add(3, 5, suffix, f'Q5(C)({suffix[2:]})', appraisal + '\n\n' + ces + '\n\n' + results + '\n\n' + trends + '\n' + L(3, 9, item) + '\n' + note, sum(marks), 'business-3-19',
        f'ces-trends-{name.split("/")[0].lower()}-2010', 9, [35], f'{name}: {sum(marks)} marks ({" + ".join(map(str, marks))}).', [comps(name, marks)],
        ['The allocation summary prints “' + S(8, '6 marks (1+2+3) 8 marks (1+2+5) 6 marks (1+2+3)') + '” for investors, suppliers and employees.',
         'Scheme example: ' + example],
        extra=['business-0-12'])

marie = (L(3, 10, 'Read the information supplied below and answer the questions which follow.') + '\n'
         + L(3, 10, 'Marie Nolan is the owner of ‘Marie’s Pizzas’ a successful pizza restaurant with a home- delivery service. Demand for take-aways has increased, as more people are eating at home due to the economic downturn. Marie is planning to expand her business through franchising and her accountant recommends that a business plan should be prepared before going ahead.'))
add(3, 6, 'a', 'Q6(A)', marie + '\n\n' + L(3, 10, '(A) Evaluate franchising (benefits and risks) as a method of expansion for the Pizza business.'), 20, 'business-4-18', 'franchising-evaluated-2010',
    10, [36], 'Three points at 5 (2 + 3), at least one benefit and one risk, and an evaluation 5 (2 + 3).', seq(points('Benefit or risk', 3, (2, 3)), comps('Evaluation', (2, 3))),
    ['Scheme example: ' + S(36, 'Franchising permits a more rapid expansion.')], extra=['business-5-14'])
add(3, 6, 'b', 'Q6(B)', marie + '\n\n' + L(3, 10, '(B) Outline two benefits to ‘Marie’s Pizzas’ of preparing a business plan.'), 10, 'business-4-15', 'marie-business-plan-benefits',
    10, [37], 'Two benefits at 4 marks each (2 + 2) and a reference to Marie’s Pizzas 2.', seq(points('Benefit', 2, (2, 2)), comps('Reference to Marie’s Pizzas', (2,))),
    ['Scheme examples: ' + S(37, 'Finance/Grants: a business plan will be required when or from government agencies.') + ' ' + S(37, 'Performance Measurement:')])
fin_i = L(3, 10, '(C) (i) Discuss the factors that should be considered when choosing between different sources of finance.')
add(3, 6, 'c-i', 'Q6(C)(i)', marie + '\n\n' + fin_i, 15, 'business-3-16', 'finance-choice-factors-2010', 10, [37, 38], 'Three factors at 5 marks each (2 + 3).', points('Factor', 3, (2, 3)),
    ['Scheme examples: ' + S(38, 'Status of the business:') + ' ' + S(38, 'Availability/Credit crunch:')])
add(3, 6, 'c-ii', 'Q6(C)(ii)', marie + '\n\n' + fin_i + '\n' + L(3, 10, '(ii) Analyse two appropriate sources of finance for acquiring an additional delivery van at ‘Marie’s Pizzas’.'), 15,
    'business-3-16', 'delivery-van-finance-2010', 10, [38], 'Two medium-term sources, each stated and explained: 8 (2 + 3 + 3) and 7 (2 + 3 + 2).', unequal('Source', [(2, 3, 3), (2, 3, 2)], None),
    ['The allocation summary prints “' + S(9, '2 medium sources of finance (State, explain, explain)') + '”. Scheme: '
     + S(38, 'Medium Term Loan • A medium term loan is obtained for a period of one to five years.').replace(' •', ':') + ' ' + S(38, 'Leasing • This involves renting rather than purchasing the asset.').replace(' •', ':')])

downtimes = L(3, 10, 'Companies which invest in marketing in downtimes benefit more when market conditions begin to pick up.')
add(3, 7, 'a', 'Q7(A)', downtimes + '\n\n' + L(3, 10, '(A) Discuss the reasons why businesses carry out market research.'), 15, 'business-4-16', 'market-research-reasons-2010-hl',
    10, [39], 'Three reasons at 5 marks each (2 + 3).', points('Reason', 3, (2, 3)),
    ['Scheme examples: ' + S(39, 'Competitors: it reveals information about competition in the market, their products, market share and their strengths and weaknesses.')])
add(3, 7, 'b', 'Q7(B)', downtimes + '\n\n' + L(3, 10, '(B) Evaluate ‘Sales Promotion’ and ‘Public Relations’ as forms of promotion.'), 20, 'business-4-17', 'sales-promotion-and-pr-2010',
    10, [39, 40], 'Two distinct points for each, 7 (4 + 3) each, and an evaluation of both 6 (3 + 3).',
    [comps('Sales Promotion', (4, 3), None, 1), comps('Public Relations', (4, 3), None, 2), comps('Evaluation of both', (3, 3), ['Sales Promotion', 'Public Relations'], 3)],
    ['Scheme: ' + S(40, 'Public Relations: can take the form of press releases where the media are given information about the company.')])
add(3, 7, 'c', 'Q7(C)', downtimes + '\n\n' + L(3, 10, '(C) ‘Many businesses spend large sums of money developing a brand name’. Illustrate the benefits of branding for the business and the consumer.'), 25,
    'business-4-17', 'branding-benefits-2010', 10, [40], 'Five benefits at 5 marks each (2 + 3), at least one for the business and one for the consumer, with an example.',
    points('Benefit', 5, (2, 3)),
    ['The allocation summary prints “' + S(9, '(At least 1 benefit from each required) Example required 4 @ 5 marks (2 + 3) 5 marks (2+3)') + '”.',
     'Scheme example: ' + S(40, 'Pricing: A well-known brand name can command a premium price.')])

# ---------------------------------------------------------------- checks and write-out
qn = lambda c: c['questionRef'].split(' Q')[1].split('(')[0]
for section, count, total in [('1', 10, 10), ('3', 7, 60)]:
    for q in range(1, count + 1):
        got = sum(c['totalMarks'] for c in P.created if c['section'] == section and qn(c) == str(q))
        assert got == total, (section, q, got)
assert not [i for i in ORIGINAL if i.startswith('bus-2010-hl-')]
assert not P.pools

SELECTION = {
    1: 'No finite printed answer menu occurs in Section 1 (answer eight of ten at 10 marks). The matching rows in Q4 are a required answer format. Support-note lists are open examples.',
    3: 'One printed choice is one card: Q3(C) any two of three EU policies, marked alike (10 each). Q4(A)(ii) asks for a business of the candidate’s own. Sub-parts with their own published marks are separate cards; Q1(B) is one card because its 7 + 7 + 6 is not split by sub-part. Support-note lists are open examples.',
}


def own(w, m, phrase):
    """Is the matched word inside this phrase? Scan windows span parts, so the phrase must cover the match itself."""
    at = 70 if w[70:70 + len(m)] == m else w.find(m)
    start = w.find(phrase)
    while start != -1:
        if start <= at < start + len(phrase):
            return True
        start = w.find(phrase, start + 1)
    return False


def classify(fileid, page, m, w):
    if m == f'{page} of' and own(w, m, f'Page {page} of 12'):
        return 'exam-navigation', 'This is the printed page counter (Page N of 12), visually checked on the source page. It is pagination, not a candidate answer choice.', None
    if m.lower().startswith('answer'):
        return 'exam-navigation', 'The rubric sets how many whole questions a candidate answers. Every numbered question remains in the practice corpus as separate cards.', None
    if m == 'any two' and own(w, m, 'any two of the following EU policies'):
        return 'finite-choice', 'Section 3 Q3(C) asks for any two of the three printed EU policies. The scheme marks every choice alike (10 each), so one card carries all three with the scheme wording for each.', 'bus-2010-hl-s3-q3c'
    assert (fileid, page) in {('LC033ALP000EV', 1), ('LC033ALP000EV', 7)} and m in ('either', 'or'), (fileid, page, m, w)
    return 'exam-navigation', 'The cover and Section 3 rubrics set how many whole questions a candidate answers (one from Part 1, two from Part 2 and one other from either part). Every numbered question remains in the practice corpus as separate cards.', None


n = P.write([(1, range(1, 11)), (3, range(1, 8))], SELECTION, classify,
            'Every part of {year} Higher Section {section} Question {q} was visually checked against its SEC paper, allocation summary and support notes. The single-booklet identity keeps the short (n) and long (S3Q) question numbering apart.')
print(f'Reviewed {len(P.created)} 2010 Higher tasks; classified {n} raw selection matches.')
