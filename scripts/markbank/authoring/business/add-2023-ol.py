"""Review the 2023 Ordinary English paper (Section 1 and Section 2).

Sixty-eight legacy IDs keep their ID and total with correction records. Two
legacy cards become the first printed route of their finite pools; Section 1
Q7 and Q11, Section 2 Q3(A)(i), Q9(C)(i), Q9(C)(ii) and the Q9(D) pool are new.
"""
from bus_lib import (Paper, ORIGINAL, comps, points, seq, unequal, single, ten_five, response,
                     fixed, legacy_route, opt_resp, permit)

T = {(1, q): 4 for q in range(1, 16)}
T.update({(2, 1): 5, (2, 2): 5, (2, 3): 6, (2, 4): 6, (2, 5): 7, (2, 6): 7, (2, 7): 7, (2, 8): 8, (2, 9): 8})
P = Paper(2023, 'ordinary', {1: 'LC033GLP032EV', 2: 'LC033GLP033EV'}, 'LC033GLP000EV', T)
L, S, add, cum = P.lift, P.scheme, P.add, P.cumulative
TWO = 'Two points are required: 10 (7 + 3) and 5 (4 + 1).'
UNTIED = 'The 10-mark allowance is not tied to a particular point.'
EIGHT = 'Two points are required: 8 (4 + 4) and 7 (4 + 3).'
UNTIED8 = 'The 8-mark allowance is not tied to a particular point.'


def eight_seven(label):
    return unequal(label, [(4, 4), (4, 3)], None)


# ---------------------------------------------------------------- Section 1
add(1, 1, '', 'Q1', L(1, 3, 'What do the following letters stand for? Write each answer in the space provided.', 'VAT', 'ECB', 'DIRT'), 10,
    'business-3-18', 'abbreviations-vat-ecb-dirt', 3, [9], 'Each term carries its own marks: 3 (1 + 1 + 1), 3 (1 + 1 + 1) and 4 (1 + 1 + 1 + 1).',
    [comps('VAT (first term)', (3,), ['Term written in full'], 1), comps('ECB (second term)', (3,), ['Term written in full'], 2),
     comps('DIRT (third term)', (4,), ['Term written in full'], 3)],
    ['Answer key: VAT ' + S(9, 'Value Added Tax') + '; ECB ' + S(9, 'European Central Bank') + '; DIRT ' + S(9, 'Deposit Interest Retention Tax')
     + '. Each word earns one mark of its term.'], extra=['business-6-14'])
cum(1, 2, '', 'Q2', L(1, 3, 'Indicate whether each of the following actions is an example of a Controller or Facilitator manager by writing Controller or Facilitator after each of the following statements.',
                      '(i) The manager gives orders and expects them to be followed without question.', '(ii) The manager encourages employee empowerment.',
                      '(iii) Employees are trusted to carry out their duties without constant supervision.',
                      '(iv) The manager makes all the decisions and does not consult with employees.'),
    (3, 3, 2, 2), 'business-2-11', 'controller-facilitator', 3, [9], 'Answer key: (i) Controller; (ii) Facilitator; (iii) Facilitator; (iv) Controller (scheme page 9).')
add(1, 3, '', 'Q3', L(1, 3, 'Outline two reasons for business expansion.'), 10, 'business-4-18', 'reasons-for-expansion', 3, [9],
    'Outline two reasons at 5 marks each (3 + 2).', points('Reason', 2, (3, 2)))
cum(1, 4, '', 'Q4', L(1, 4, 'Write the word TRUE or FALSE after each of the following statements.', '(i) A sole trader has unlimited liability.',
                      '(ii) A public limited company can have a maximum of 149 shareholders.', '(iii) A co-operative is owned and controlled by the government.',
                      '(iv) A partnership business can have 2 - 20 partners.'),
    (3, 3, 2, 2), 'business-5-14', 'ownership-true-false', 4, [10], 'Answer key: (i) True; (ii) False; (iii) False; (iv) True (scheme page 10).')
add(1, 5, '', 'Q5', L(1, 4, 'Complete levels 3 and 4 of Maslow’s Hierarchy of Needs.') + '\n' + L(1, 4, '5. Self-actualisation', '4.', '3.', '2. Safety', '1. Physiological'), 10,
    'business-2-11', 'maslow-levels-3-and-4', 4, [10], 'Each missing level earns 5 marks.',
    seq(single('Level 3', 5, 'Level 3 named'), single('Level 4', 5, 'Level 4 named')),
    ['Answer key: level 4 ' + S(10, '4. Esteem') + '; level 3 ' + S(10, '3. Acceptance / Social') + '.'])
add(1, 6, 'i', 'Q6(i)', L(1, 4, '6. (i) Explain the term USP.'), 6, 'business-4-17', 'usp-explained', 4, [10],
    'Explain the term for 6 marks (3 + 3).', [comps('USP', (3, 3))], ['USP: ' + S(10, 'Unique Selling Point') + '.'])
add(1, 6, 'ii', 'Q6(ii)', L(1, 4, '(ii) Name a product and its USP.'), 4, 'business-4-17', 'product-and-usp', 4, [10],
    'Name a product 2 and its USP 2.', seq(single('Product', 2, 'Product named'), single('USP', 2, 'Its USP')),
    ['Scheme examples: ' + S(10, 'Toblerone – triangular chocolate') + '; ' + S(10, 'Volvo – safety') + '.'])
rec = add(1, 7, '', 'Q7', L(1, 5, 'Complete the recruitment and selection process of the Human Resource Manager in the correct order by filling in the missing tasks:',
                            'Check references Screen applicants Person specification Interview candidates')
          + '\n1. Job Description → 2. ______ → 3. Advertise job → 4. ______ → 5. Selection Tests → 6. ______ → 7. ______ → 8. Offer job',
          10, 'business-3-20', 'recruitment-selection-order', 5, [11], 'Four entries: 3, then 3 + 2 on the second row, then 2.',
          seq(fixed('Step 2', [('Person specification', 3)]), comps('Steps 4 and 6', (5,), ['Screen applicants and Interview candidates']),
              fixed('Step 7', [('Check references', 2)])),
          ['Answer key (scheme page 11): 2. ' + S(11, 'Person specification') + '; 4. ' + S(11, 'Screen applicants') + '; 6. '
           + S(11, 'Interview candidates') + '; 7. ' + S(11, 'Check references') + '.',
           'The second row (steps 4 and 6) is marked 3 + 2: for one or two correct entries record 3 or 5 marks; the 3 is not tied to a particular box.'])
permit(rec, 1, [0, 3, 5])
for v in ['1. Job Description', '3. Advertise job', '5. Selection Tests', '8. Offer job']:
    L(1, 5, v)
cum(1, 8, '', 'Q8', L(1, 5, 'Circle the correct option in each of the following statements.',
                      '(i) Employees must give seven / ten days’ notice of industrial action to their employer.',
                      '(ii) When employees ask for a pay rise because inflation has increased it is known as a productivity / cost of living claim.',
                      '(iii) IBEC represents businesses / employees.', '(iv) The Irish Farmers’ Association (IFA) is an interest group / trade union.'),
    (3, 3, 2, 2), 'business-0-14', 'industrial-relations-options', 5, [11],
    'Answer key (circled on scheme page 11): (i) seven; (ii) cost of living; (iii) businesses; (iv) interest group.')
add(1, 9, '', 'Q9', L(1, 6, 'Match the images with the correct pricing strategy from the list below. (One pricing strategy is not shown.)',
                      'Premium Pricing Price Discrimination Penetration Pricing')
    + '\n(i) A fare table with different one-way, return and ten-trip prices for adults, seniors and children.\n(ii) '
    + L(1, 6, 'iPhone 13 6.1-inch display from €929'),
    10, 'business-4-17', 'pricing-strategy-images', 6, [11], 'Each image earns 5 marks.',
    seq(single('Image (i)', 5, 'Strategy named'), single('Image (ii)', 5, 'Strategy named')),
    ['Answer key: (i) ' + S(11, 'Price Discrimination') + '; (ii) ' + S(11, 'Premium Pricing') + '. Penetration Pricing is not shown.'])
add(1, 10, '', 'Q10', L(1, 6, 'Draft the memorandum sent by Tina Duggan, IT Manager, on today’s date to all employees reminding them that system log-in passwords must be changed by Friday 23rd June 2023.')
    + '\nMemorandum: To / From / Date / Re / Signed / Title', 10, 'business-2-12', 'memorandum-draft', 6, [12],
    'Six entries: To 2, From 2, Date 1, Re 3, Signed 1, Title 1.',
    [response(1, 'Memorandum', [('to', 'To: All staff', 2), ('from', 'From: Tina Duggan (IT Manager)', 2), ('date', 'Date: today’s date', 1),
                                ('re', 'Re: reminder that system log-in passwords must be changed by Friday 23rd June 2023', 3),
                                ('signed', 'Signed: Tina Duggan', 1), ('title', 'Title: IT Manager', 1)])],
    ['Scheme model: To ' + S(12, 'All staff') + '; From Tina Duggan (IT Manager); Date ' + S(12, '15/06/23') + '; Re '
     + S(12, 'I wish to remind all staff that system log-in passwords must be updated/changed by Friday 23rd June 2023.') + '; Signed Tina Duggan; Title IT Manager.'])
cum(1, 11, '', 'Q11', L(1, 7, 'Indicate by placing a tick (✓) in the correct box, the European Union policy that each statement describes.')
    + '\nCommon Agricultural Policy (CAP) / Common Fisheries Policy (CFP) / EU Social Charter / Competition Policy\n'
    + L(1, 7, 'EU citizens have the right to live and work in any EU country.', 'Farmers receive Single Farm Payments to help supplement their income.',
        'All business mergers and takeovers are monitored.', 'The aim is to preserve fish stocks in EU waters.'),
    (3, 3, 2, 2), 'business-6-14', 'eu-policies-ticks', 7, [12],
    'Answer key (ticks on scheme page 12): live and work Social Charter; Single Farm Payments CAP; mergers and takeovers Competition Policy; fish stocks CFP.')
for v in ['Common Agricultural Policy (CAP)', 'Common Fisheries Policy (CFP)', 'EU Social Charter', 'Competition Policy']:
    L(1, 7, v)
cum(1, 12, '', 'Q12', L(1, 7, 'Match the explanation with the correct State Agency from the list below.', 'Local Enterprise Office (LEO) Fáilte Ireland IDA Ireland',
                        'Promotes Irish tourism industry around the world.', 'Attracts multinational companies to set up in Ireland through various incentives.',
                        'Assists entrepreneurs in setting up their business through advice, grant aid etc.'),
    (4, 3, 3), 'business-5-15', 'state-agencies-matching', 7, [12],
    'Answer key (scheme page 12): tourism Fáilte Ireland; multinationals IDA Ireland; entrepreneurs Local Enterprise Office (LEO).')
add(1, 13, '', 'Q13', L(1, 8, 'Complete the missing factors of production.') + '\n1. Land; 2. ______; 3. ______; 4. Enterprise', 10, 'business-1-5',
    'factors-of-production-missing', 8, [13], 'Each missing factor earns 5 marks.',
    seq(single('Factor 2', 5, 'Factor named'), single('Factor 3', 5, 'Factor named')),
    ['Answer key: 2. Labour; 3. Capital (scheme page 13).'], extra=['business-5-13'])
for v in ['1. Land', '4. Enterprise']:
    L(1, 8, v)
cash = (L(1, 8, 'Below is a copy of the Cashflow Forecast for Dwyer’s Guesthouse for the first three months of 2023.')
        + '\nJanuary / February / March\n' + L(1, 8, 'Total Receipts 15,500 26,000 28,000', 'Total Payments 16,700 23,000 24,000', 'Net Cash (1,200) (i) 4,000',
                                              'Opening Cash (1,500) (2,700) 300', 'Closing Cash (2,700) 300 4,300'))
add(1, 14, 'i', 'Q14(i)', cash + '\n\n' + L(1, 8, '(i) Calculate the Net Cash figure for February. Show your workings.'), 4, 'business-3-16',
    'net-cash-february', 8, [13], 'Calculation 4 marks (1 + 1 + 2).', [comps('Net cash, February', (1, 1, 2), ['Receipts figure', 'Payments figure', 'Answer'])],
    ['Answer: ' + S(13, '€3,000') + '; workings ' + S(13, '26,000 – 23,000 = 3,000') + ' (or from the closing and opening cash).'])
add(1, 14, 'ii', 'Q14(ii)', cash + '\n\n' + L(1, 8, '(ii) Identify a month where the guesthouse has a deficit.'), 3, 'business-3-16', 'deficit-month',
    8, [13], 'Identify the month for 3 marks.', [single('Deficit month', 3, 'Month identified')], ['Answer: ' + S(13, '(ii) January') + '.'])
add(1, 14, 'iii', 'Q14(iii)', cash + '\n\n' + L(1, 8, '(iii) Identify a month where the guesthouse has a surplus.'), 3, 'business-3-16', 'surplus-month',
    8, [13], 'Identify the month for 3 marks.', [single('Surplus month', 3, 'Month identified')], ['Answer: ' + S(13, '(iii) March/February') + '.'])
cum(1, 15, '', 'Q15', '\n'.join([L(1, 9, 'In the following table, Column 1 is a list of business terms and Column 2 is a list of explanations.'),
                                 L(1, 9, '1. Leasing', '2. Bank Overdraft', '3. Trade Credit', '4. Debenture', '5. Share Capital'),
                                 L(1, 9, 'A Long-term fixed interest loan.', 'B Business profits re-invested in the firm.', 'C Renting an asset over a one to five-year period.',
                                   'D Allows the account holder to withdraw more money than is in the account.',
                                   'E Money provided by investors in return for part ownership/share of profits.', 'F Buying stock now and paying at a later date.'),
                                 L(1, 9, 'Match the two lists by placing the letter of the correct explanation under the number of the relevant business term below. One explanation has no match.')]),
    (2, 2, 2, 2, 2), 'business-3-16', 'finance-terms-matching', 9, [13], 'Answer key: 1 C; 2 D; 3 F; 4 A; 5 E. Explanation B is unused (scheme page 13).')

# ---------------------------------------------------------------- Section 2
dental = L(2, 2, 'Dental implant firm ordered to pay manager €55,000', 'A UK dental implants company has been ordered to pay €55,000 to a former Irish sales manager who was unfairly dismissed.', sep='\n')
add(2, 1, 'a', 'Q1(A)', dental + '\n\n' + L(2, 2, '(A) Outline two reasons for fair dismissal.'), 15, 'business-0-14', 'fair-dismissal-reasons',
    2, [14], EIGHT, eight_seven('Reason'), [UNTIED8])
add(2, 1, 'b', 'Q1(B)', dental + '\n\n' + L(2, 2, '(B) Outline one function of the Workplace Relations Commission.'), 10, 'business-0-14', 'wrc-function',
    2, [14], 'One function: 10 marks (5 + 5).', [comps('Function', (5, 5))])
cum(2, 1, 'c', 'Q1(C)', L(2, 2, '(C) List five stakeholders in business.'), (3, 3, 3, 3, 3), 'business-0-12', 'five-stakeholders', 2, [14],
    'Scheme examples include ' + S(14, 'Owner/Entrepreneur/Employer') + ', investors, employees, consumers, government, local community and suppliers.', noun='stakeholders')
add(2, 1, 'd', 'Q1(D)', L(2, 2, '(D) Explain the term co-operative relationship and outline one example of a co-operative relationship between two stakeholders.'), 15,
    'business-0-12', 'co-operative-relationship', 2, [15], 'Explanation 8 (4 + 4) and one example 7 (4 + 3).',
    [comps('Explanation', (4, 4), i=1), comps('Example', (4, 3), i=2)])
method = opt_resp([('component-1', 'Component 1', 4), ('component-2', 'Component 2', 3)])
P.pool(2, 1, 'e', '1(E)', 2, [5, 15], 3, L(2, 2, 'Explain, using examples, three of these methods.'),
       L(2, 2, '(E) A legal contract may be terminated by the following methods:') + '\nExplain, using examples, the following three methods.',
       [dict(id='frustration', label='Frustration'), dict(id='breach', label='Breach'), dict(id='agreement', label='Agreement'),
        dict(id='performance', label='Performance')],
       20, 'Explain all three selected methods with examples: 7 (4 + 3), 7 (4 + 3) and 6 (4 + 2).', ['The 7/7/6 sequence prices the three explanations, not particular methods.'],
       'business-0-12', 'contract-termination-methods',
       'The paper prints four methods of terminating a contract and asks for three. All four selections are generated at 20 marks with the 7/7/6 sequence unattached; the legacy card is the first three printed methods.',
       legacy=legacy_route('bus-2023-ol-s2-q1e', ['frustration', 'breach', 'agreement'], 2, [5, 15],
                           'question text lifted from the printed paper; the card becomes the first three printed methods of the expanded choose-three pool.'),
       ordered=unequal('Method response', [(4, 3), (4, 3), (4, 2)], None))
for v in ['• Frustration', '• Breach', '• Agreement', '• Performance']:
    L(2, 2, v)

tiktok = L(2, 3, 'Video-sharing platform TikTok is to create 1,000 new jobs in Ireland as part of its future expansion plans. IDA Ireland has welcomed the news. The new employees will bring TikTok’s total headcount here to about 3,000.')
add(2, 2, 'a', 'Q2(A)', tiktok + '\n\n' + L(2, 3, '(A) Explain the term multinational company (MNC).'), 10, 'business-6-15', 'mnc-explained',
    3, [16], 'Explanation: 10 marks (7 + 3).', [comps('Multinational company', (7, 3))])
add(2, 2, 'b', 'Q2(B)', tiktok + '\n\n' + L(2, 3, '(B) Outline two incentives the Government uses to attract multinational companies (MNCs) to Ireland.'), 15, 'business-6-15',
    'mnc-incentives', 3, [16], TWO, ten_five('Incentive'), [UNTIED])
add(2, 2, 'c', 'Q2(C)', tiktok + '\n\n' + L(2, 3, '(C) Describe two benefits of an increase in employment for the Irish economy.'), 15, 'business-5-15',
    'employment-benefits', 3, [16], TWO, ten_five('Benefit'), [UNTIED])
inflation = L(2, 3, 'High inflation may persist for years.')
add(2, 2, 'di', 'Q2(D)(i)', inflation + '\n\n' + L(2, 3, '(i) Explain the term inflation.'), 5, 'business-5-15', 'inflation-explained',
    3, [17], 'Explanation: 5 marks (3 + 2).', [comps('Inflation', (3, 2))])
add(2, 2, 'dii', 'Q2(D)(ii)', inflation + '\n\n' + L(2, 3, '(ii) Outline two effects of a high inflation rate on Irish business.'), 15, 'business-5-15',
    'high-inflation-effects', 3, [17], TWO, ten_five('Effect'), [UNTIED])
starbucks = L(2, 3, 'Starbucks is listed as one of the world’s most ethical companies.')
add(2, 2, 'e', 'Q2(E)', starbucks + '\n\n' + L(2, 3, '(E) Outline two benefits for a business of behaving ethically.'), 15, 'business-5-17',
    'ethical-behaviour-benefits', 3, [17], TWO, ten_five('Benefit'), [UNTIED])

exports = (L(2, 4, "Share of Ireland's Total Exports by Region") + ' (bar chart, 0% to 40%): '
           + L(2, 4, 'Rest of World Northern Ireland European Union Great Britian United States') + ' — read the bars on the printed page.')
add(2, 3, 'ai', 'Q3(A)(i)', exports + '\n\n' + L(2, 4, '(i) Using the information above, identify the region to which Ireland exports the most.'), 5,
    'business-6-13', 'largest-export-region', 4, [18], 'Name the region for 5 marks.', [single('Region', 5, 'Region identified')],
    ['Answer: ' + S(18, 'European Union') + '.'], new=True)
cum(2, 3, 'aii', 'Q3(A)(ii)', exports + '\n\n' + L(2, 4, '(ii) List three examples of goods/services that Ireland exports.'), (4, 3, 3), 'business-6-13',
    'irish-export-examples', 4, [18], 'Scheme examples: ' + S(18, 'Computer parts, Pharmaceutical products, Beef, Dairy products') + ', a French tourist staying in an Irish hotel.',
    noun='examples')
barriers = add(2, 3, 'b', 'Q3(B)', L(2, 4, '(B) Name two barriers to trade and explain one of them.'), 15, 'business-6-13', 'barriers-named-and-explained',
               4, [18], 'Two barriers named at 4 each, and one explained for 7 (4 + 3).',
               seq(single('Barrier named 1', 4, 'Barrier named'), single('Barrier named 2', 4, 'Barrier named'), comps('Barrier explained', (4, 3))),
               ['Scheme barriers: ' + S(18, 'Tariff • Embargo • Subsidy • Quota') + '.'])
bop = L(2, 4, "(C) Ireland’s Balance of Payments was €15.8 billion from October – December 2022.")
add(2, 3, 'ci', 'Q3(C)(i)', bop + '\n' + L(2, 4, '(i) Explain the term Balance of Payments.'), 8, 'business-6-13', 'balance-of-payments-explained',
    4, [18], 'Explanation: 8 marks (4 + 4).', [comps('Balance of Payments', (4, 4))])
add(2, 3, 'cii', 'Q3(C)(ii)', bop + '\n' + L(2, 4, '(ii) Outline one impact of an increase in exports on the Balance of Payments.'), 7, 'business-6-13',
    'exports-impact-bop', 4, [18], 'One impact: 7 marks (4 + 3).', [comps('Impact', (4, 3))])
eu50 = L(2, 4, 'In 2023 Ireland marks the 50th anniversary since joining the European Union.')
add(2, 3, 'di', 'Q3(D)(i)', eu50 + '\n\n' + L(2, 4, '(i) Outline two benefits to Ireland of being a member of the European Union.'), 12, 'business-6-14',
    'eu-membership-benefits', 4, [19], 'Two benefits at 6 marks each (4 + 2).', points('Benefit', 2, (4, 2)))
add(2, 3, 'dii', 'Q3(D)(ii)', eu50 + '\n\n' + L(2, 4, '(ii) Describe one challenge of European Union membership to Ireland.'), 8, 'business-6-14',
    'eu-membership-challenge', 4, [19], 'One challenge: 8 marks (4 + 4).', [comps('Challenge', (4, 4))])
cum(2, 3, 'e', 'Q3(E)', eu50 + '\n\n' + L(2, 4, '(E) Name two institutions of the European Union.'), (5, 5), 'business-6-14', 'eu-institutions-named',
    4, [19], 'Scheme examples: ' + S(19, 'European Parliament') + ', European Commission, the Council of the EU, European Council, Court of Auditors, Court of Justice, European Central Bank.',
    noun='institutions')

jack = L(2, 5, 'Jack McCarthy purchased a pair of hiking boots from Outdoor Life in Gateway Shopping Centre. After he tried them on again at home, he found the boots to be slightly uncomfortable and went back to the store to return them. The sales assistant told him he would have to accept a Credit Note if he wanted to return the boots.')
add(2, 4, 'ai', 'Q4(A)(i)', jack + '\n\n' + L(2, 5, '(i) Does Jack have to accept the Credit Note? Explain your answer.'), 10, 'business-0-13', 'credit-note',
    5, [20], 'Answer (Yes) 4 and explanation 6 (3 + 3).', seq(single('Answer', 4, 'Yes, he does'), comps('Explanation', (3, 3))),
    ['Scheme: ' + S(20, 'Yes, he does. As there is no fault with the product, the retailer is not obliged to provide a refund/replacement.')])
add(2, 4, 'aii', 'Q4(A)(ii)', jack + '\n\n' + L(2, 5, '(ii) Name the consumer law that applies.'), 10, 'business-0-13', 'consumer-law-named',
    5, [20], 'Name the law: five words at 2 marks each.', [comps('Consumer law', (10,), ['Act named'])],
    ['Answer: ' + S(20, 'Sale of Goods & Supply of Services Act 1980') + '. For 0 to 5 correct words, record 0, 2, 4, 6, 8 or 10 marks.'])
permit(P.created[-1], 0, [0, 2, 4, 6, 8, 10])
add(2, 4, 'b', 'Q4(B)', jack + '\n\n' + L(2, 5, '(B) Name and explain one consumer agency that helps Jack to be more aware of his consumer rights.'), 15, 'business-0-13',
    'consumer-agency', 5, [20], 'Agency named 5 and explained 10 (5 + 5).', seq(single('Agency', 5, 'Agency named'), comps('Explanation', (5, 5))),
    ['Scheme agencies: ' + S(20, 'Competition & Consumer Protection Commission (CCPC)') + ' or ' + S(20, 'Consumers Association of Ireland (CAI)') + '.'])
siptu = L(2, 5, 'SIPTU threatens industrial action', 'SIPTU members at Dublin Airport are threatening industrial action in a dispute over the payment of wages.', sep='\n')
add(2, 4, 'c', 'Q4(C)', siptu + '\n\n' + L(2, 5, '(C) Outline two causes of industrial disputes, other than pay, between trade unions and employers.'), 10, 'business-0-14',
    'dispute-causes', 5, [21], 'Two causes at 5 marks each (3 + 2).', points('Cause', 2, (3, 2)))
add(2, 4, 'di', 'Q4(D)(i)', siptu + '\n\n' + L(2, 5, '(i) Outline two benefits of being a member of a trade union.'), 10, 'business-0-14', 'trade-union-benefits',
    5, [21], 'Two benefits at 5 marks each (3 + 2).', points('Benefit', 2, (3, 2)))
add(2, 4, 'dii', 'Q4(D)(ii)', siptu + '\n\n' + L(2, 5, '(ii) Apart from SIPTU, name one other trade union in Ireland.'), 5, 'business-0-14', 'other-trade-union',
    5, [21], 'Name a trade union for 5 marks.', [single('Trade union', 5, 'Union named')], ['Scheme: ' + S(21, 'ASTI, TUI, INTO, INMO, Mandate, Forsa.')])
add(2, 4, 'e', 'Q4(E)', siptu + '\n\n' + L(2, 5, '(E) Explain the following industrial relations terms:', '• Secret Ballot', '• Minimum Notice', '• Picketing'), 15,
    'business-0-14', 'industrial-relations-terms', 5, [22], 'Each required term at 5 marks (3 + 2).',
    [comps('Secret Ballot', (3, 2), i=1), comps('Minimum Notice', (3, 2), i=2), comps('Picketing', (3, 2), i=3)])

sweet = L(2, 6, 'SweetKing is an online pick ‘n’ mix store which was founded by Nathan Adams in June 2020. Nathan saw a gap in the market for an online pick ‘n’ mix store with speedy delivery to your door. Nathan sources his stock from Ireland, Belgium, Spain, and the UK. He has since expanded his business into retail.')
add(2, 5, 'a', 'Q5(A)', sweet + '\n\n' + L(2, 6, '(A) Outline three enterprising characteristics/skills that entrepreneurs like Nathan display.'), 15, 'business-1-5',
    'enterprising-characteristics', 6, [23], 'Three at 5 marks each (3 + 2).', points('Characteristic', 3, (3, 2)))
add(2, 5, 'bi', 'Q5(B)(i)', sweet + '\n\n' + L(2, 6, '(i) Explain the term stock control.'), 5, 'business-2-13', 'stock-control-explained',
    6, [23], 'Explanation: 5 marks (3 + 2).', [comps('Stock control', (3, 2))])
add(2, 5, 'bii', 'Q5(B)(ii)', sweet + '\n\n' + L(2, 6, '(ii) Outline two reasons why stock control would be important to a business like SweetKing.'), 10, 'business-2-13',
    'stock-control-reasons', 6, [23], 'Two reasons at 5 marks each (3 + 2).', points('Reason', 2, (3, 2)))
add(2, 5, 'c', 'Q5(C)', sweet + '\n\n' + L(2, 6, '(C) Leadership styles include Autocratic, Democratic and Laissez-faire. Outline two features of any one leadership style that Nathan could use in his business.'),
    15, 'business-2-11', 'leadership-style-features', 6, [24], EIGHT, eight_seven('Feature'),
    [UNTIED8, 'Both features describe the one leadership style the candidate chooses; the scheme gives features of all three.'])
add(2, 5, 'di', 'Q5(D)(i)', sweet + '\n\n' + L(2, 6, '(i) Explain the term delegation.'), 5, 'business-2-13', 'delegation-explained',
    6, [25], 'Explanation: 5 marks (3 + 2).', [comps('Delegation', (3, 2))])
add(2, 5, 'dii', 'Q5(D)(ii)', sweet + '\n\n' + L(2, 6, '(ii) Describe two benefits of delegation for a manager.'), 10, 'business-2-13', 'delegation-benefits',
    6, [25], 'Two benefits at 5 marks each (3 + 2).', points('Benefit', 2, (3, 2)))
add(2, 5, 'e', 'Q5(E)', sweet + '\n\n' + L(2, 6, '(E) Outline two benefits of Information and Communication Technology (ICT) for SweetKing.'), 15, 'business-2-12',
    'ict-benefits', 6, [25], EIGHT, eight_seven('Benefit'), [UNTIED8])

golf = (L(2, 7, 'Greenlawn Golf Club Notice and Agenda', 'The AGM of Greenlawn Golf Club and Restaurant will take place on 21st November 2023 at 8.00pm in the Clubhouse.', sep='\n')
        + '\nAgenda: ' + L(2, 7, '• Minutes of the 2022 AGM • Any matters arising • Club Chairperson’s Report • Club Treasurer’s Report • Expansion of Clubhouse • Membership fees • Election of club officers • AOB')
        + '\nSigned Paul Cahill, Secretary. (AGM, Minutes and AOB are underlined.)')
add(2, 6, 'a', 'Q6(A)', golf + '\n\n' + L(2, 7, '(A) Explain the three underlined terms above.'), 15, 'business-2-12', 'meeting-terms',
    7, [26], 'Each required term at 5 marks (3 + 2).', [comps('AGM', (3, 2), i=1), comps('Minutes', (3, 2), i=2), comps('AOB', (3, 2), i=3)])
add(2, 6, 'bi', 'Q6(B)(i)', golf + '\n\n' + L(2, 7, '(i) Outline two duties of a secretary for a club meeting.'), 10, 'business-2-12', 'secretary-duties',
    7, [26], 'Two duties at 5 marks each (3 + 2).', points('Duty', 2, (3, 2)))
add(2, 6, 'bii', 'Q6(B)(ii)', golf + '\n\n' + L(2, 7, '(ii) Outline two duties of a chairperson at a meeting.'), 10, 'business-2-12', 'chairperson-duties',
    7, [26], 'Two duties at 5 marks each (3 + 2).', points('Duty', 2, (3, 2)))
add(2, 6, 'c', 'Q6(C)', golf + '\n\n' + L(2, 7, '(C) Outline three factors a bank will consider before issuing the club a loan to fund their expansion.'), 15, 'business-3-16',
    'loan-factors', 7, [27], 'Three factors at 5 marks each (3 + 2).', points('Factor', 3, (3, 2)))
add(2, 6, 'd', 'Q6(D)', golf + '\n\n' + L(2, 7, '(D) Name and explain two types of insurance Greenlawn Golf Club should have.'), 15, 'business-3-17',
    'club-insurance-types', 7, [27], EIGHT, eight_seven('Insurance'), [UNTIED8])
role = opt_resp([('component-1', 'Component 1', 5), ('component-2', 'Component 2', 5)])
P.pool(2, 6, 'e', '6(E)', 7, [7, 27], 1, L(2, 7, 'Explain the role of one of them.'),
       L(2, 7, '(E) Assessors and Actuaries are both involved in insurance.') + ' Explain the role of the following.',
       [dict(id='assessors', label='Assessors', response=role), dict(id='actuaries', label='Actuaries', response=role)],
       10, 'Explain the selected role: 10 marks (5 + 5).', [], 'business-3-17', 'assessor-or-actuary',
       'The paper names two insurance roles and asks for one. Both routes are generated at 10 marks; the legacy card is the first printed role.',
       legacy=legacy_route('bus-2023-ol-s2-q6e', ['assessors'], 7, [7, 27],
                           'question text lifted from the printed paper; the card becomes the first printed route of the expanded choose-one pool.'))

lucy = L(2, 8, 'Lucy Kavanagh has just started a new job as a payroll administrator with FastParts Ltd. She earns a gross salary of €40,000 per annum. Her annual tax credits are €3,400. She pays PAYE at a standard rate of 20%. PRSI is 4% of Gross Pay. USC is 3% of Gross Pay.')
pay = add(2, 7, 'a', 'Q7(A)', lucy + '\n\n' + L(2, 8, '(A) Calculate Lucy’s net annual salary. Show all workings.'), 20, 'business-3-18', 'net-annual-salary',
          8, [28], 'PAYE 3 (1 + 1 + 1), tax credit 3, PAYE payable 2, PRSI 3 (1 + 1 + 1), USC 3 (1 + 1 + 1), gross pay 2, deductions 2, net pay 2.',
          [response(1, 'Net annual salary', [('paye', 'PAYE: €40,000 × 0.2 = €8,000', 3), ('credit', 'Less tax credit €3,400', 3), ('payable', 'PAYE payable €4,600', 2),
                                             ('prsi', 'PRSI: €40,000 × 0.04 = €1,600', 3), ('usc', 'USC: €40,000 × 0.03 = €1,200', 3), ('gross', 'Gross Pay €40,000', 2),
                                             ('deductions', 'Less Deductions €7,400', 2), ('net', 'Net Annual Pay €32,600', 2)])],
          ['Scheme working on page 28: total deductions €7,400; net annual pay €32,600.'])
for k, steps in [(1, [0, 3]), (2, [0, 2]), (5, [0, 2]), (6, [0, 2]), (7, [0, 2])]:
    permit(pay, 0, steps, k)
add(2, 7, 'b', 'Q7(B)', lucy + '\n\n' + L(2, 8, '(B) Explain the term PAYE.'), 10, 'business-3-18', 'paye-explained',
    8, [28], 'Explanation: 10 marks (6 + 3 + 1).', [comps('PAYE', (6, 3, 1), ['Pay As You Earn', 'Component 2', 'Component 3'])],
    ['Scheme: ' + S(28, 'PAYE – Pay As You Earn') + ', income tax deducted at source by the employer.'])
fast = L(2, 8, 'FastParts Ltd offer several different rewards schemes as part of its package for attracting new employees. Sales Representatives at FastParts Ltd earn commission and receive benefit-in-kind as part of their package.')
add(2, 7, 'c', 'Q7(C)', fast + '\n\n' + L(2, 8, '(C) Outline two methods of recruiting new employees.'), 15, 'business-3-20', 'recruitment-methods',
    8, [28], TWO, ten_five('Method'), [UNTIED])
add(2, 7, 'd', 'Q7(D)', fast + '\n\n' + L(2, 8, '(D) Explain, using examples, commission and benefit-in-kind.'), 15, 'business-3-20', 'commission-and-bik',
    8, [29], 'Commission 8 (3 + 3 explanation, 2 example) and benefit-in-kind 7 (3 + 2 explanation, 2 example).',
    [response(1, 'Commission', [('explain', 'Explanation', 6), ('example', 'Example', 2)]),
     response(2, 'Benefit-in-kind', [('explain', 'Explanation', 5), ('example', 'Example', 2)])])
add(2, 7, 'e', 'Q7(E)', fast + '\n\n' + L(2, 8, '(E) Outline two benefits for FastParts Ltd of rewarding their employees.'), 15, 'business-3-20',
    'reward-benefits', 8, [29], TWO, ten_five('Benefit'), [UNTIED])

insomnia = L(2, 9, 'Irish coffee chain, Insomnia, provides a loyalty programme called Insomnia Treats that allows customers to build and redeem credits on every Insomnia item they purchase. Customers can keep track of their offers on the Insomnia Treats app. Insomnia advertises extensively using social media.')
franchise = L(2, 9, 'Insomnia operates as a franchise. Glenn McCarthy is considering opening a coffee shop in his hometown but is unsure if he should operate independently or under a franchise.')
add(2, 8, 'ai', 'Q8(A)(i)', insomnia + '\n\n' + L(2, 9, '(i) Outline one benefit of a loyalty programme as a method of sales promotion.'), 8, 'business-4-17',
    'loyalty-programme-benefit', 9, [30], 'One benefit: 8 marks (6 + 2).', [comps('Benefit', (6, 2))])
add(2, 8, 'aii', 'Q8(A)(ii)', insomnia + '\n\n' + L(2, 9, '(ii) Apart from a loyalty programme, outline one other sales promotion technique that a coffee shop could use to increase sales.'), 7,
    'business-4-17', 'other-sales-promotion', 9, [30], 'One technique: 7 marks (5 + 2).', [comps('Technique', (5, 2))])
add(2, 8, 'b', 'Q8(B)', insomnia + '\n\n' + L(2, 9, '(B) Outline two benefits of using social media advertising for Insomnia.'), 15, 'business-4-17',
    'social-media-advertising', 9, [30], TWO, ten_five('Benefit'), [UNTIED])
cum(2, 8, 'c', 'Q8(C)', insomnia + '\n\n' + L(2, 9, '(C) List three factors a business such as Insomnia should consider before setting prices for its products.'), (8, 4, 3),
    'business-4-17', 'pricing-factors-list', 9, [31], 'Scheme examples: ' + S(31, 'Cost of production/supply') + ', competitors’ prices, income levels of target market, demand, taxes, branding.',
    noun='factors')
add(2, 8, 'd', 'Q8(D)', franchise + '\n\n' + L(2, 9, '(D) Outline two advantages to Glenn McCarthy of setting up a business through an existing franchise model.'), 15, 'business-4-15',
    'franchise-advantages', 9, [31], TWO, ten_five('Advantage'), [UNTIED], extra=['business-4-18'])
add(2, 8, 'e', 'Q8(E)', franchise + '\n\n' + L(2, 9, '(E) Explain two reasons why preparing a Business Plan is essential for Glenn.'), 15, 'business-4-15',
    'business-plan-reasons', 9, [31], TWO, ten_five('Reason'), [UNTIED])

ispy = L(2, 10, 'I-SPY is an online sportwear business based in Ireland which sells a range of yoga and fitness wear. The business was set up by Louise Egan along with her mother Paulette. They joined their passions for fitness, lifestyle and yoga to create the idea for their business.')
cum(2, 9, '-a', 'Q9(A)', ispy + '\n\n' + L(2, 10, '(A) Paulette and Louise turned their interests into a business opportunity. List two other sources of business ideas for entrepreneurs.'), (5, 5),
    'business-4-14', 'sources-of-ideas-list', 10, [32], 'Scheme examples: ' + S(32, 'Suggestions from family/friends') + ', media/internet, brainstorming, competitors, intrapreneurship, customer feedback.',
    noun='sources')
add(2, 9, '-b', 'Q9(B)', ispy + '\n\n' + L(2, 10, '(B) Name and explain the two types of market research a business like I-SPY could have used before launching its products.'), 15,
    'business-4-16', 'market-research-types', 10, [32], 'Two types: 8 (3 + 3 + 2) and 7 (3 + 2 + 2).', unequal('Type', [(3, 3, 2), (3, 2, 2)], None),
    ['The scheme’s two types are desk (secondary) and field (primary) research; the 8-mark allowance is not tied to either.'])
batch = L(2, 10, '(C) Clothing companies such as I-SPY often make their products using batch production.')
add(2, 9, '-c-i', 'Q9(C)(i)', ispy + '\n\n' + batch + '\n' + L(2, 10, '(i) Explain the term batch production.'), 7, 'business-4-15', 'batch-production-explained',
    10, [33], 'Explanation: 7 marks (4 + 3).', [comps('Batch production', (4, 3))], new=True)
add(2, 9, '-c-ii', 'Q9(C)(ii)', ispy + '\n\n' + batch + '\n' + L(2, 10, '(ii) List two other methods of production and include an example of a product that uses each type of production.'),
    13, 'business-4-15', 'other-production-methods', 10, [33], 'Two methods with examples: 7 (4 + 3) and 6 (4 + 2).',
    unequal('Method', [(4, 3), (4, 2)], None), ['Scheme: ' + S(33, 'Job Production') + ' and ' + S(33, 'Mass Production') + ', each with a product example.'], new=True)
stage = None
P.pool(2, 9, 'd', '9(D)', 10, [8, 33], 2, L(2, 10, '(D) Explain any two of the following stages of the new product development process.'),
       ispy + '\n\nExplain the following two stages of the new product development process.',
       [dict(id='feasibility-study', label=L(2, 10, '(i) Feasibility Study')), dict(id='prototype-development', label=L(2, 10, '(ii) Prototype Development')),
        dict(id='test-marketing', label=L(2, 10, '(iii) Test Marketing'))],
       15, 'Explain both selected stages: 8 (4 + 4) and 7 (4 + 3).', ['The 8-mark allowance is not tied to a particular stage.'],
       'business-4-14', 'new-product-development-stages',
       'The paper prints a closed list of three development stages and asks for any two. All three pairs are generated at 15 marks with the 8/7 split unattached; no earlier card existed.',
       ordered=eight_seven('Stage response'))
add(2, 9, '-e', 'Q9(E)', ispy + '\n\n' + L(2, 10, '(E) Outline two challenges when starting a new business.'), 15, 'business-4-15', 'start-up-challenges',
    10, [34], EIGHT, eight_seven('Challenge'), [UNTIED8])

# ---------------------------------------------------------------- checks and write-out
qn = lambda c: c['questionRef'].split(' Q')[1].split('(')[0]
s1 = [c for c in P.created if c['section'] == '1']
for q in range(1, 16):
    assert sum(c['totalMarks'] for c in s1 if qn(c) == str(q)) == 10, q
pool_q = {}
for p in P.pools:
    k = p['template']['questionRef'].split(' Q')[1].split('(')[0]
    pool_q[k] = pool_q.get(k, 0) + p['template']['totalMarks']
for q in range(1, 10):
    tot = sum(c['totalMarks'] for c in P.created if c['section'] == '2' and qn(c) == str(q)) + pool_q.get(str(q), 0)
    assert tot == 75, (q, tot)
legacy = {i for i in ORIGINAL if i.startswith('bus-2023-ol-')}
covered = {c['id'] for c in P.created} | {p['legacyRoute']['id'] for p in P.pools if 'legacyRoute' in p}
assert legacy <= covered, sorted(legacy - covered)
new = sorted(c['id'] for c in P.created if c['id'] not in ORIGINAL)
assert new == ['bus-2023-ol-s1-q11', 'bus-2023-ol-s1-q7', 'bus-2023-ol-s2-q3ai', 'bus-2023-ol-s2-q9-c-i', 'bus-2023-ol-s2-q9-c-ii'], new

SELECTION = {
    1: 'No finite printed answer menu occurs in Section 1. Controller/Facilitator and True/False labels, ticks, matching rows, circled options, the image matching in Q9 and the word bank of missing recruitment tasks in Q7 are required answer formats. Q6 and Q14 split at their separately marked sub-parts. Support-note lists are open examples.',
    2: 'Three finite printed pools are expanded separately: Q1(E) three of four contract-termination methods (four routes, 7/7/6), Q6(E) one of two insurance roles (two routes), each with its legacy card as the first printed route, and Q9(D) any two of three development stages (three routes, new). Q5(C) says leadership styles “include” the three named, so the style is an open choice; Q3(B) barriers, Q3(E) institutions and the Q6(A) underlined terms are open or required. Sub-parts with their own published marks are separate cards. Support-note lists are open examples.',
}


def classify(fileid, page, m, w):
    if m.lower().startswith('answer'):
        return 'exam-navigation', 'The rubric sets how many whole questions a candidate answers. Every numbered question remains in the practice corpus as separate cards.', None
    if fileid == 'LC033GLP033EV' and m == 'three of' and 'three of these methods' in w:
        return 'finite-pool', 'Section 2 Q1(E) asks for three of four printed methods of terminating a contract; all four selections are generated at 20 marks.', 'bus-2023-ol-s2-q1e'
    if fileid == 'LC033GLP033EV' and m == 'one of' and 'role of one of them' in w:
        return 'finite-pool', 'Section 2 Q6(E) asks for the role of one of the two named insurance roles; both routes are generated at 10 marks.', 'bus-2023-ol-s2-q6e'
    if fileid == 'LC033GLP033EV' and m == 'any two' and 'any two of the following stages' in w:
        return 'finite-pool', 'Section 2 Q9(D) asks for any two of three printed development stages; all three pairs are generated at 15 marks.', 'bus-2023-ol-s2-q9d'
    if m == 'any one' and 'any one leadership style' in w:
        return 'open-response', 'Section 2 Q5(C) says leadership styles “include” the three named; the style is an open choice and the task stays whole.', None
    if m == 'one of' and 'explain one of them' in w:
        return 'open-response', 'Section 2 Q3(B) asks the candidate to name two barriers of their own and explain one of them; no closed list is printed, so the task stays whole.', None
    if m == 'one of' and 'most ethical companies' in w:
        return 'case-context', 'The Section 2 Q2 extract describes Starbucks as one of the world’s most ethical companies; it is case context.', None
    if m == 'or' and 'independently or under a franchise' in w:
        return 'case-context', 'The Section 2 Q8 extract describes Glenn’s choice between operating independently or under a franchise; it creates no choice of task.', None
    if m == 'or' and 'Controller or Facilitator' in w:
        return 'required-headings', 'Controller/Facilitator are answer labels for each of the four required statements in Section 1 Q2, not optional tasks.', None
    if m == 'or' and ('TRUE or FALSE' in w or 'True or False' in w):
        return 'required-headings', 'True/False are answer labels for each of the four required statements in Section 1 Q4, not optional tasks.', None
    if m == '4 of' and 'levels 3 and 4 of' in w:
        return 'required-headings', 'Section 1 Q5 requires both named levels (3 and 4) of the pyramid; they are not alternatives.', None
    assert (fileid, page) in {('LC033GLP032EV', 2), ('LC033GLP032EV', 10), ('LC033GLP032EV', 36), ('LC033GLP033EV', 12)}, (fileid, page, m, w)
    return 'exam-navigation', 'Cover instructions, pen/pencil instructions, answerbook supplies or copyright boilerplate. They do not create alternative task routes.', None


n = P.write([(1, range(1, 16)), (2, range(1, 10))], SELECTION, classify,
            'Every part of {year} Ordinary Section {section} Question {q} was visually checked against its SEC booklet, allocation summary and support notes. Booklet-specific p1/p2 identities keep the short and long question numbering apart.')
print(f'Reviewed {len(P.created)} 2023 Ordinary base tasks and {len(P.pools)} route pools; classified {n} raw selection matches.')
