"""Review the 2012 Higher English paper outside its ABQ (Sections 1 and 3).

2012 Higher: answer eight of ten short questions at 10 marks (Section 1),
the compulsory Applied Business Question (Section 2, carded by
add-2012-abq.py and left untouched here) and four of seven long questions
at 60 (Section 3: one from Part 1, two from Part 2 and one other), all in
one twelve-page booklet (LC033ALP000EV, the same file id as its scheme).
No card existed for Sections 1 and 3, so every card is new. The allocation
summary (scheme pages 5 and 8-12) sets each boundary; printed sub-parts with
their own published marks are separate cards. No printed choice of task
occurs.
"""
from bus_lib import (Paper, ORIGINAL, comps, points, seq, unequal, single, response, fixed, permit)

T = {(1, q): 5 for q in range(1, 11)}
T.update({(3, 1): 8, (3, 2): 8, (3, 3): 9, (3, 4): 9, (3, 5): 10, (3, 6): 11, (3, 7): 12})
P = Paper(2012, 'higher', {1: 'LC033ALP000EV', 3: 'LC033ALP000EV'}, 'LC033ALP000EV', T)
L, S, add, cum = P.lift, P.scheme, P.add, P.cumulative


def flat(card):
    for r in card['rubric']['responses']:
        for a in r['allocations']:
            a['permittedMarks'] = [0, a['maxMarks']]
    return card


def bullets(text, sep='; '):
    return sep.join(x.strip() for x in text.split('•') if x.strip())


# ---------------------------------------------------------------- Section 1 (10 marks each)
add(1, 1, '', 'Q1', L(1, 2, 'Illustrate your understanding of the term enterprise.'), 10, 'business-1-5', 'enterprise-illustrated-2012', 2, [13],
    'Illustration: 10 marks (4 + 4 + 2).', [comps('Enterprise', (4, 4, 2))],
    ['Scheme: ' + S(13, 'Enterprise is being innovative and creative while taking personal/financial risk to achieve ones goal.') + ' Examples include '
     + S(13, 'Business Enterprise – Diversification into new markets/new products/ Facebook-Mark Zuckerberg/Xbox-Microsoft /iPad-Apple') + '.'])
cum(1, 2, '', 'Q2', '\n'.join([L(1, 2, 'Column 1 is a list of business terms. Column 2 is a list of explanations for these terms. (One explanation does not refer to any of the terms)'),
                               L(1, 2, '1. Stakeholder', '2. Ultra Vires', '3. Lobbying', '4. Legality of Form', '5. Labour Court'),
                               L(1, 2, 'A. A party acting beyond its legal powers.', 'B. A quick, inexpensive way for dealing with consumer complaints.',
                                 'C. The manner in which a contract is drawn up.', 'D. A party that can affect or be affected by business decisions.',
                                 'E. Using an organised campaign to influence a decision maker.', 'F. Establishes Joint Labour Committees.'),
                               L(1, 2, 'Match the two lists by placing the letter of the correct explanation under the relevant number below:')]),
    (2, 2, 2, 2, 2), 'business-0-12', 'business-terms-matching-2012-hl', 2, [13], 'Answer key (scheme page 13): 1 D; 2 A; 3 E; 4 C; 5 F. Explanation B is unused.',
    extra=['business-5-14', 'business-0-14'], noun='matches')
S(13, '1. 2. 3. 4. 5. D A E C F')
add(1, 3, '', 'Q3', L(1, 2, 'Explain the difference between the terms tax rates and tax credits.'), 10, 'business-3-18', 'tax-rates-and-tax-credits',
    2, [13, 14], 'Both terms: 6 (3 + 3) and 4 (2 + 2).', unequal('Term explained', [(3, 3), (2, 2)], None),
    ['The 6-mark allowance is not tied to either term. Scheme: ' + S(13, 'Tax rates: Income is taxed at two different rates.') + ' '
     + S(13, 'Tax credits: Gross Tax less Tax Credits = Tax Payable.')])
add(1, 4, 'a', 'Q4(a)', L(1, 3, '(a) Define the term delegation.'), 4, 'business-2-11', 'delegation-defined-2012', 3, [14], 'Definition: 4 marks (2 + 2).',
    [comps('Delegation', (2, 2))], ['Scheme: ' + S(14, 'Delegation involves the assignment of authority/power to another person.')])
add(1, 4, 'b', 'Q4(b)', L(1, 3, '(a) Define the term delegation.') + '\n' + L(1, 3, '(b) Outline two benefits of delegation within a business:'), 6, 'business-2-11',
    'delegation-benefits-2012', 3, [14], 'Two benefits at 3 marks each.', points('Benefit', 2, (3,)),
    ['Scheme examples: ' + S(14, 'Manager is not required to do all the work and has more time for strategic planning.') + ' '
     + S(14, 'Increased employee motivation from job enrichment/ improved staff morale/more challenging work.')])
add(1, 5, '', 'Q5', L(1, 3, 'Outline two features of a matrix organisation structure:'), 10, 'business-2-13', 'matrix-structure-features',
    3, [14], 'Two features: 6 (3 + 3) and 4 (2 + 2).', unequal('Feature', [(3, 3), (2, 2)], None),
    ['The 6-mark allowance is not tied to a particular feature. Scheme examples: ' + S(14, 'It is a team based structure with expertise drawn from different departments e.g. marketing, finance, information technology, production etc.')])
cum(1, 6, '', 'Q6', L(1, 3, 'In the context of business, what do the following letters stand for? Write your answers in the spaces provided.') + '\nR&D\nPLC\nIBEC\nEGM\nDIRT',
    (3, 3, 2, 1, 1), 'business-5-14', 'abbreviations-2012-hl', 3, [14],
    'Answer key (scheme page 14): ' + S(14, 'R&D Research and Development PLC Public Limited Company IBEC Irish Business and Employers’ Confederation EGM Extraordinary General Meeting DIRT Deposit Interest Retention Tax') + '.',
    extra=['business-4-14', 'business-0-12', 'business-2-12', 'business-3-18'], noun='abbreviations')
L(1, 3, 'R&D PLC IBEC EGM DIRT')
add(1, 7, '', 'Q7', L(1, 3, 'Distinguish between a merger and a franchise as methods of business expansion.'), 10, 'business-4-18', 'merger-and-franchise',
    3, [15], 'Both methods: 6 (3 + 3) and 4 (2 + 2).', unequal('Method explained', [(3, 3), (2, 2)], None),
    ['The 6-mark allowance is not tied to either method. Scheme: ' + S(15, 'A merger is a friendly or voluntary amalgamation/joining together of two or more firms for their mutual benefit.') + ' '
     + S(15, 'A Franchise is a business arrangement whereby the franchisor (the existing business with the proven business model) grants a contractual licence/permission to the franchisee (person setting up the business) to use its name, logo and business idea in return for a fee or a percentage of profits or sales.')],
    extra=['business-5-14'])
add(1, 8, 'a', 'Q8(a)', L(1, 4, '(a) Define the term primary sector.'), 4, 'business-5-13', 'primary-sector-defined', 4, [15], 'Definition: 4 marks (2 + 2).',
    [comps('Primary sector', (2, 2))], ['Scheme: ' + S(15, 'The primary sector (extractive) is a category of industry based on the natural resources of a country such as agriculture, forestry, fishing, mining, energy.')])
add(1, 8, 'b', 'Q8(b)', L(1, 4, '(a) Define the term primary sector.') + '\n' + L(1, 4, '(b) Outline two current trends affecting this sector in Ireland:'), 6, 'business-5-13',
    'primary-sector-trends-2012', 4, [15], 'Two trends at 3 marks each.', points('Trend', 2, (3,)),
    ['Scheme examples: ' + S(15, 'As a result of overfishing the EU has introduced fish quotas in an attempt to conserve fish stocks.') + ' '
     + S(15, 'Continued growth in organic food production capitalising on Ireland’s green image worldwide.')])
add(1, 9, '', 'Q9', L(1, 4, 'Illustrate your understanding of the term Trading Bloc.'), 10, 'business-6-13', 'trading-bloc-2012', 4, [16],
    'Illustration: 6 (3 + 3) and 4.', unequal('Point', [(3, 3), (4,)], None),
    ['Scheme: ' + S(16, 'A trading bloc is a group of countries who agree to form a free trade area or common market or customs union.') + ' Examples: '
     + S(16, 'The European Union (EU) • The North American Free Trade Agreement (NAFTA).').replace(' •', ';')], extra=['business-6-14'])
chart = (L(1, 4, 'Break-even chart') + '\n(Chart: ' + L(1, 4, 'TR TC € ’000s 700 600 500 400 300 200 100 Costs & Revenues FC 5 10 15 Output in units ’000s')
         + '; the TR, TC and FC lines are drawn on the printed grid.)\n' + L(1, 4, 'Answer the following questions in the Answer Box below.'))
key = ('Scheme answer box (page 16): BEP ' + S(16, 'Units: 10,000') + ' and ' + S(16, '€ 450,000') + '; ' + S(16, 'Profit at Forecast € 125,000') + '.')
flat(add(1, 10, 'i', 'Q10(i)', chart + '\n' + L(1, 4, '(i) Break-even point (BEP) in units and in euros'), 6, 'business-3-19', 'bep-units-and-euros-2012',
         4, [16], 'Units 3 and euros 3.', [comps('Break-even point', (3, 3), ['In units', 'In euros'])], [key]))
flat(add(1, 10, 'ii', 'Q10(ii)', chart + '\n' + L(1, 4, '(ii) The Profit at Forecast Sales (15,000 units) in euros.'), 2, 'business-3-19', 'profit-at-forecast-2012',
         4, [16], 'Profit: 2 marks.', [comps('Profit at forecast sales', (2,))], [key]))
add(1, 10, 'iii', 'Q10(iii)', chart + '\n' + L(1, 4, '(iii) Explain the term Margin of Safety.'), 2, 'business-3-19', 'margin-of-safety-2012',
    4, [16], 'Explanation: 2 marks.', [comps('Margin of Safety', (2,))],
    ['Scheme: ' + S(16, 'Margin of Safety shows the amount by which sales can fall before reaching the Break-Even point where no profits are made.')])
S(5, '10. (i) 6 marks (3+3) (ii) 2 marks (iii) 2 marks')

# ---------------------------------------------------------------- Section 3 (60 marks each)
add(3, 1, 'a', 'Q1(A)', L(3, 6, '(A) Outline the procedures an employer should follow under the Unfair Dismissals Acts of 1977-2007, before dismissing an employee.'), 20,
    'business-0-14', 'dismissal-procedures-2012', 6, [22, 23], 'Three procedures: 7 (4 + 3), 7 (4 + 3) and 6 (3 + 3).', unequal('Procedure', [(4, 3), (4, 3), (3, 3)], None),
    ['The 7-mark allowances are not tied to particular procedures. Scheme examples: ' + S(22, 'Formal verbal warning: The employer has to inform the employee of the reasons for the possible dismissal.') + ' '
     + S(22, 'First Written warning: If there is no change to the situation, a formal written warning follows the oral warning.')])
add(3, 1, 'b', 'Q1(B)', L(3, 6, '(B) A legal contract can be terminated by breach, frustration or agreement. Illustrate your understanding of the underlined terms.') + '\n(breach, frustration and agreement are underlined.)',
    20, 'business-0-12', 'contract-termination-2012', 6, [23], 'All three terms, each explained with an example: 7 (4 + 3), 7 (4 + 3) and 6 (3 + 3).',
    unequal('Term', [(4, 3), (4, 3), (3, 3)], None),
    ['The 7-mark allowances are not tied to particular terms. Scheme: ' + S(23, 'By Frustration An unforeseen event prevents the contract from being completed.') + ' '
     + S(23, 'By Agreement The parties to the contract may agree to end/cancel a contract by mutual consent whether or not the purpose of the contract has been achieved.')])
cpa = L(3, 6, 'The Consumer Protection Act 2007 came into effect in Ireland on 1st May, 2007. The Act provided for the establishment of the National Consumer Agency, which replaced the Office of the Director of Consumer Affairs.')
add(3, 1, 'c', 'Q1(C)', cpa + '\n\n' + L(3, 6, '(C) Evaluate the role and functions of the National Consumer Agency (NCA) in protecting consumers.'), 20, 'business-0-13', 'nca-evaluated-2012',
    6, [24, 25], 'Three points at 6 marks each (3 + 3) and an evaluation 2.', seq(points('Role or function', 3, (3, 3)), comps('Evaluation', (2,))),
    ['Scheme examples: ' + S(24, 'To promote and protect the interests and welfare of consumers.') + ' Evaluation: '
     + S(25, 'The NCA is very effective because it is a statutory body, is an advocate for the consumer and has enforcement powers')])

structure = L(3, 6, '“Choosing an appropriate business structure is a key element of a business plan.”')
add(3, 2, 'a', 'Q2(A)', structure + '\n\n' + L(3, 6, '(A) Discuss Co-operatives and Private Limited Companies as forms of business ownership, using the following headings: Formation; Liability; Finance; Control'),
    25, 'business-5-14', 'coop-and-private-company', 6, [26, 27], 'Formation 7 ((2 + 3) + 2); liability, finance and control 6 each ((2 + 2) + 2).',
    [comps('Formation', (2, 3, 2), None, 1), comps('Liability', (2, 2, 2), None, 2), comps('Finance', (2, 2, 2), None, 3), comps('Control', (2, 2, 2), None, 4)],
    ['The allocation summary prints “' + S(8, 'Formation ((2+3)+2) Liability ((2+2)+2) Finance ((2+2)+2) Control ((2+2)+2)') + '”.',
     'Scheme (control): ' + S(27, 'A private limited company is controlled by the shareholders based on the rule “one share one vote”.') + ' '
     + S(27, 'Co-operatives have a democratic structure, where each member has one vote, “one member one vote”')])
add(3, 2, 'b', 'Q2(B)', structure + '\n\n' + L(3, 6, '(B) Outline how the Irish Government’s policy of increased taxation and decreased public expenditure is impacting on business.'), 20,
    'business-5-15', 'taxation-and-spending-impact', 6, [27, 28, 29], 'Taxation: two points at 5 (2 + 3). Expenditure: two points at 5 (2 + 3).',
    seq(points('Taxation impact', 2, (2, 3)), points('Expenditure impact', 2, (2, 3))),
    ['Scheme examples: ' + S(28, 'VAT increases lead to more expensive goods and services for the consumer which in turn causes demand to fall, thereby affecting business.') + ' '
     + S(29, 'Under-investment in infrastructure can undermine economic growth and competitiveness.')], extra=['business-3-18'])
ethics_i = L(3, 6, '(C) (i) Define the term ‘Business Ethics’.')
add(3, 2, 'c-i', 'Q2(C)(i)', structure + '\n\n' + ethics_i, 5, 'business-5-17', 'business-ethics-defined-2012', 6, [29], 'Definition: 5 marks (2 + 3).',
    [comps('Business Ethics', (2, 3))], ['Scheme: ' + S(29, 'It is a set of moral rules and standards that provide guidelines for right and truthful behaviour in business situations with its various stakeholders')])
add(3, 2, 'c-ii', 'Q2(C)(ii)', structure + '\n\n' + ethics_i + '\n' + L(3, 6, '(ii) Outline how ethical behavior in business can be encouraged.'), 10, 'business-5-17',
    'encouraging-ethics-2012', 6, [29], 'Two ways at 5 marks each (2 + 3).', points('Way', 2, (2, 3)),
    ['Scheme examples: ' + S(29, 'Establishing a code of ethics.') + ' ' + S(29, 'Encouraging ‘whistle blowing’.') + ' ' + S(29, 'Modelling ethical behaviour.')])

glob = L(3, 7, '“Globalisation refers to the increasing interdependence of the world’s economies.”')
add(3, 3, 'a', 'Q3(A)', glob + '\n\n' + L(3, 7, '(A) Outline four developments in technology that have facilitated the growth in globalisation.'), 20, 'business-6-15',
    'technology-and-globalisation', 7, [30], 'Four developments at 5 marks each (2 + 3).', points('Development', 4, (2, 3)),
    ['Scheme examples: ' + S(30, 'Communication/mobile technology/EDI') + '; ' + S(30, 'Marketing/Internet/social networking/www') + '; ' + S(30, 'Distribution/ JIT') + '.'], extra=['business-2-12'])
add(3, 3, 'b', 'Q3(B)', glob + '\n\n' + L(3, 7, '(B) “Protectionism is a Government policy of placing barriers on free trade.” Describe, using examples, barriers to free trade between countries.'), 20,
    'business-6-13', 'free-trade-barriers-2012', 7, [31], 'Three barriers, each named, explained and exemplified: 7 (2 + 3 + 2), 7 (2 + 3 + 2) and 6 (2 + 3 + 1).',
    unequal('Barrier', [(2, 3, 2), (2, 3, 2), (2, 3, 1)], ['Name', 'Explanation', 'Example']),
    ['The 7-mark allowances are not tied to particular barriers. Scheme: ' + S(31, 'Quota: is a physical restriction/limit on the number of units of a good that may be imported/exported.') + ' '
     + S(31, 'Tariff: this is a tax on the value/price of goods imported.')])
add(3, 3, 'c', 'Q3(C)', glob + '\n\n' + L(3, 7, '(C) Discuss the role of the Council of the European Union (Council of Ministers) and the European Commission in the European Union (EU) decision making process.'), 20,
    'business-6-14', 'council-and-commission-2012', 7, [31, 32], 'Each institution 10 marks (4 + 3 + 3).',
    [comps('Council of the European Union', (4, 3, 3), None, 1), comps('European Commission', (4, 3, 3), None, 2)],
    ['Scheme: ' + S(31, 'Main decision making body of the EU.') + ' ' + S(32, 'The European Commission is the executive body of the European Union.')])

comms = L(3, 8, '“How you communicate is as important as what you communicate.”')
add(3, 4, 'a', 'Q4(A)', comms + '\n\n' + L(3, 8, '(A) Illustrate the factors that a business needs to consider when communicating with its various stakeholders.'), 20, 'business-2-12',
    'stakeholder-communication-factors', 8, [33], 'Four factors at 5 marks each (2 + 2 + 1).', points('Factor', 4, (2, 2, 1)),
    ['Scheme factors: ' + S(33, 'Appropriate Language/Clarity') + '; ' + S(33, 'Confidentiality/Safety') + '; ' + S(33, 'Cost') + '; ' + S(33, 'Urgency/Speed/Destination') + '; ' + S(33, 'Feedback/Accuracy/Record') + '.'])
add(3, 4, 'b', 'Q4(B)', comms + '\n\n' + L(3, 8, '(B) Distinguish between the duties of a chairperson and a secretary in the organising and running of an Annual General Meeting.'), 20, 'business-2-12',
    'agm-chair-and-secretary', 8, [34], 'Chairperson 10 (4 + 3 + 3) and secretary 10 (4 + 3 + 3).',
    [comps('Chairperson', (4, 3, 3), None, 1), comps('Secretary', (4, 3, 3), None, 2)],
    ['Scheme examples: ' + S(34, 'The chairperson opens the meeting only after ensuring the quorum is present.') + ' '
     + S(34, 'The secretary sends out the notice and agenda to all those who are entitled to attend.')])
add(3, 4, 'c', 'Q4(C)', comms + '\n\n' + L(3, 8, '(C) Outline two styles of leadership and illustrate how each of these styles may be appropriate in different business situations.'), 20, 'business-2-11',
    'leadership-styles-situations', 8, [34, 35], 'Two styles at 10 marks each (2 + 3 + 3 + 2).', points('Leadership style', 2, (2, 3, 3, 2)),
    ['Scheme illustration (autocratic): ' + S(35, 'This style of leadership may be appropriate in a crisis or emergency situation where tough decisions may be needed quickly')])

bianua = L(3, 9, 'Bianua Ltd, a medium size company, operating in the agrifood sector, supplies quality prepared food products in Ireland and in the UK market.')
add(3, 5, 'a', 'Q5(A)', bianua + '\n\n' + L(3, 9, '(A) Draft a business letter from EXON Insurance PLC to Bianua Ltd, using today’s date, identifying the possible business risks and the appropriate types of insurance for Bianua Ltd. Use fictitious names and addresses.'),
    20, 'business-3-17', 'insurance-letter-bianua', 9, [36], 'Layout 8, four risks at 2 each and four types of insurance at 1 each.',
    seq(fixed('Letter layout', [('Letterhead', 1), ('Date', 2), ('RE', 1), ('Inside name and address', 1), ('Salutation', 1), ('Complimentary close', 1), ("Author's signature", 1)]),
        fixed('Business risks', [('Risk 1', 2), ('Risk 2', 2), ('Risk 3', 2), ('Risk 4', 2)]),
        fixed('Types of insurance', [('Insurance 1', 1), ('Insurance 2', 1), ('Insurance 3', 1), ('Insurance 4', 1)])),
    ['The allocation summary prints “' + S(10, 'Layout: 8 marks Letterhead 1m Date 2m, RE 1m Inside Name & Address 1m Salutation 1m, Complimentary Close 1m, Author’s Signature 1m 8 marks :4 risks @ 2 marks 4 marks: 4 types of insurance @ 1 marks') + '”.',
     'Scheme example: ' + S(36, 'The risk of a customer injuring themselves while on premises. Public Liability Insurance – protects the business against claims made by the public as a result of accidents while on site.')],
    extra=['business-2-12'])
figures = (L(3, 9, '(B) The average performance of companies in the same industry as Bianua Ltd for 2011 is detailed in the table as follows:')
           + '\nIndustry Average Results 2011\nROI | 11%\nCurrent Ratio | 2:1\nAcid Test Ratio | 1.2 :1\nDebt/Equity Ratio | 0.3:1\n'
           + L(3, 9, 'The following figures are taken from the final accounts of Bianua Ltd for 2011.')
           + '\nBianua Ltd figures for 2011 | €\nNet Profit | 50,000\nSales | 975,000\nCurrent Assets (including closing stock) | 155,000\nLong Term Loan | 300,000\nOrdinary Share Capital | 500,000\nCurrent Liabilities | 85,000\nRetained Earnings | 100,000\nClosing Stock | 80,000')
L(3, 9, 'Industry Average Results 2011 ROI 11% Current Ratio 2:1 Acid Test Ratio 1.2 :1 Debt/Equity Ratio 0.3:1')
L(3, 9, 'Bianua Ltd figures for 2011 € Net Profit 50,000 Sales 975,000 Current Assets (including closing stock) 155,000 Long Term Loan 300,000 Ordinary Share Capital 500,000 Current Liabilities 85,000 Retained Earnings 100,000 Closing Stock 80,000')
ratios_i = L(3, 9, '(i) Calculate the following for 2011 for Bianua Ltd: • Return On Investment (ROI) • Current Ratio • Acid Test Ratio • Debt/Equity Ratio.').replace(' •', '\n•')
ratios = add(3, 5, 'b-i', 'Q5(B)(i)', bianua + '\n\n' + figures + '\n' + ratios_i, 20, 'business-3-19', 'bianua-four-ratios', 9, [37],
             'Each formula 1; calculations ROI 5, current ratio 3, acid test ratio 4 and debt/equity ratio 4.',
             [response(i, name, [('formula', 'Formula', 1), ('calculation', 'Calculation: ' + answer, m)]) for i, (name, answer, m) in
              enumerate([('Return On Investment', '5.56%', 5), ('Current Ratio', '1.82:1', 3), ('Acid Test Ratio', '0.88:1', 4), ('Debt/Equity Ratio', '0.5:1', 4)], 1)],
             ['The allocation summary prints “' + S(10, 'Ratio formulas 1 m each Calculation (5+3+4+4)') + '”.',
              'Scheme (page 37): ' + S(37, 'Return on Investment = Net Profit x100 / Cap. Employed (Ordinary share capital + Retained Earnings + Long Term Loan) 50,000/(500,000 + 100,000 + 300,000) 50,000/900,000 5.56%') + '; '
              + S(37, 'Current Ratio = Current Assets: Current Liabilities 155,000: 85,000 1.82:1') + '; '
              + S(37, 'Acid Test Ratio = Current Assets – Closing Stock: Current Liabilities (155,000 – 80,000): 85,000 75,000:85,000 0.88:1') + '; '
              + S(37, 'Debt Equity Ratio = Debt: Equity/ (Ordinary share capital + Retained Earnings) 300,000: (500,000 + 100,000) 300,000:600,000 0.5:1') + '.'])
for i in range(4):
    permit(ratios, i, [0, 1], 0)
add(3, 5, 'b-ii', 'Q5(B)(ii)', bianua + '\n\n' + figures + '\n' + L(3, 9, '(ii) Analyse the profitability and liquidity of Bianua Ltd for 2011, with reference to the industry average results shown in the box above, and make recommendations for Bianua Ltd.'),
    20, 'business-3-19', 'bianua-profitability-liquidity', 9, [37, 38], 'Profitability 10 (2 + 3 + 3 + 2) and liquidity 10 (2 + 3 + 3 + 2).',
    [comps('Profitability', (2, 3, 3, 2), None, 1), comps('Liquidity', (2, 3, 3, 2), None, 2)],
    ['Scheme: ' + S(37, 'The ROI for Bianua Ltd is 5.6%, which measures the return on capital for investors in a business. This is half the average performance of companies in the same industry.') + ' '
     + S(38, 'Bianua Ltd has €1.82 available to pay for every €1 owed, a little below the ideal of 2:1.')])

add(3, 6, 'a', 'Q6(A)', L(3, 10, '(A) Discuss the benefits and risks of empowering employees within a business.'), 20, 'business-3-21', 'empowerment-benefits-and-risks',
    10, [39], 'Four points at 5 marks each (2 + 3), at least one benefit and one risk.', points('Benefit or risk', 4, (2, 3)),
    ['The allocation summary adds “' + S(11, '(At least one benefit and one risk required)') + '”. Scheme examples: '
     + S(39, 'Employees more motivated/job satisfaction/valued/improved morale/loyal.') + ' ' + S(39, 'If empowerment is introduced without adequate training for employees then mistakes can be made.')],
    extra=['business-2-11'])
npd = L(3, 10, '“The process of introducing new products on a consistent basis is important to the future success of businesses.”')
add(3, 6, 'b', 'Q6(B)', npd + '\n\n' + L(3, 10, '(B) Idea Generation and Feasibility Study are important stages before a new product or service is launched onto the market. Discuss the stages underlined above, referring to a product or service of your choice.')
    + '\n(Idea Generation and Feasibility Study are underlined.)', 20, 'business-4-14', 'idea-generation-and-feasibility', 10, [39, 40],
    'Each stage 10 marks (3 + 4 + 3), with reference to a product or service of your choice.',
    [comps('Idea Generation', (3, 4, 3), None, 1), comps('Feasibility Study', (3, 4, 3), None, 2)],
    ['Scheme: ' + S(39, 'This is an efficient, methodical way of finding ideas for new products and services and can come from internal or external sources.') + ' '
     + S(40, 'A feasibility study is an investigative report into the potential and profitability of a business idea.') + ' The support notes add “' + S(40, 'PRODUCT/SERVICE REQUIRED WITH REFERENCE TO IDEA GENERATION.') + '”'])
zac = L(3, 10, '(C) Read the information supplied below and answer the questions which follow.') + '\n' + L(3, 10, 'Zac Computing Ltd, an innovative new technology business, considers its business plan to be an essential document in the context of a business start-up and future growth.')
plan_i = L(3, 10, '(i) Explain the term “business plan”.')
add(3, 6, 'c-i', 'Q6(C)(i)', zac + '\n\n' + plan_i, 6, 'business-4-15', 'business-plan-explained-2012', 10, [41], 'Explanation: 6 marks (3 + 3).', [comps('Business plan', (3, 3))],
    ['Scheme: ' + S(41, 'A business plan is a written statement/proposal about the business and its objectives (where it wants to go) and strategies in areas such as marketing, ownership, production, finance and the identifying of opportunities.')])
add(3, 6, 'c-ii', 'Q6(C)(ii)', zac + '\n\n' + plan_i + '\n' + L(3, 10, '(ii) Evaluate the importance of a business plan to an innovative new technology business.'), 14, 'business-4-15',
    'business-plan-importance-2012', 10, [41], 'Two points at 6 marks each (3 + 2 + 1) and an evaluation 2.', seq(points('Point', 2, (3, 2, 1)), comps('Evaluation', (2,))),
    ['Scheme evaluation: ' + S(41, 'A business plan will enable the business to determine if it can be commercially viable.')])

add(3, 7, 'a', 'Q7(A)', L(3, 10, '(A) Outline the factors a business should consider when choosing a suitable Channel of Distribution. Provide examples to illustrate your answer.'), 20, 'business-4-17',
    'distribution-channel-factors-2012', 10, [42], 'Three factors with examples: 7 (3 + 3 + 1), 7 (3 + 3 + 1) and 6 (3 + 2 + 1).', unequal('Factor', [(3, 3, 1), (3, 3, 1), (3, 2, 1)], None),
    ['The 7-mark allowances are not tied to particular factors. Scheme factors include ' + S(42, 'Cost: Cost is a factor in choice of channel of distribution.') + ' ' + S(42, 'Market size:')])
add(3, 7, 'b', 'Q7(B)', L(3, 10, '(B) Within the product element of the marketing mix, evaluate “product design” and “product packaging.”'), 20, 'business-4-17', 'design-and-packaging-2012',
    10, [42, 43], 'Product design 10 (5 + 5), product packaging 8 (4 + 4) and an evaluation 2.',
    [comps('Product design', (5, 5), None, 1), comps('Product packaging', (4, 4), None, 2), comps('Evaluation', (2,), None, 3)],
    ['The allocation summary prints “' + S(12, 'Product design Product packaging Evaluation. 10 (5+5)+ 8 (4+4)+2 marks') + '”.',
     'Scheme: ' + S(43, 'Protection: Packaging safeguards the product during transit, storage and handling.')])
toys = L(3, 10, '(C) Read the information supplied below and answer the question which follows.') + '\n' + L(3, 10, 'SuperToys Ltd, a large retail chain with 45 shops throughout Ireland, had sales of €100 million in 2011. It has just commissioned a firm to design and manufacture a new range of soft toys for babies. These will be available for sale in its shops from Summer 2013. SuperToys Ltd plans to open its first shop in the UK in 2014.')
add(3, 7, 'c', 'Q7(C)', toys + '\n\n' + L(3, 10, 'Discuss the possible reasons for business expansion and growth at SuperToys Ltd.'), 20, 'business-4-18', 'supertoys-expansion-reasons',
    10, [43], 'Three reasons: 7 (3 + 3 + 1), 7 (3 + 3 + 1) and 6 (3 + 2 + 1).', unequal('Reason', [(3, 3, 1), (3, 3, 1), (3, 2, 1)], None),
    ['The 7-mark allowances are not tied to particular reasons. Scheme examples: ' + S(43, 'Diversification. Spreading the risk by moving away from a company’s core area of business is facilitated by business expansion.')])

# ---------------------------------------------------------------- checks and write-out
qn = lambda c: c['questionRef'].split(' Q')[1].split('(')[0]
for section, count, total in [('1', 10, 10), ('3', 7, 60)]:
    for q in range(1, count + 1):
        got = sum(c['totalMarks'] for c in P.created if c['section'] == section and qn(c) == str(q))
        assert got == total, (section, q, got)
assert not [i for i in ORIGINAL if i.startswith('bus-2012-hl-')]
assert not P.pools

SELECTION = {
    1: 'No finite printed answer menu occurs in Section 1 (answer eight of ten at 10 marks). The matching rows in Q2 are a required answer format. Support-note lists are open examples.',
    3: 'No printed choice of task occurs in Section 3. Q1(B) and Q6(B) underline terms that are all required; Q2(A) prints required headings; Q6(B) asks for a product or service of the candidate’s own. Sub-parts with their own published marks are separate cards. Support-note lists are open examples.',
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
    if m == 'or' and own(w, m, 'affect or be affected'):
        return 'case-context', 'Wording inside explanation D of the Section 1 Q2 matching table, not a choice of task.', None
    if m == 'or' and own(w, m, 'breach, frustration or agreement'):
        return 'required-headings', 'Section 3 Q1(B) underlines breach, frustration and agreement and asks for an understanding of the underlined terms; all three are required.', None
    if m == 'or' and own(w, m, 'new product or service is launched'):
        return 'case-context', 'Wording inside the Section 3 Q6(B) statement, not a choice of task.', None
    if m == 'or' and own(w, m, 'a product or service of your choice'):
        return 'open-response', 'Section 3 Q6(B) asks the candidate to refer to a product or service of their own choice; no list is printed, so it is one card.', None
    assert (fileid, page) in {('LC033ALP000EV', 1), ('LC033ALP000EV', 6)} and m in ('either', 'or'), (fileid, page, m, w)
    return 'exam-navigation', 'The cover and Section 3 rubrics set how many whole questions a candidate answers (one from Part 1, two from Part 2 and one other from either part). Every numbered question remains in the practice corpus as separate cards.', None


n = P.write([(1, range(1, 11)), (3, range(1, 8))], SELECTION, classify,
            'Every part of {year} Higher Section {section} Question {q} was visually checked against its SEC paper, allocation summary and support notes. The single-booklet identity keeps the short (n) and long (S3Q) question numbering apart.')
print(f'Reviewed {len(P.created)} 2012 Higher tasks; classified {n} raw selection matches.')
