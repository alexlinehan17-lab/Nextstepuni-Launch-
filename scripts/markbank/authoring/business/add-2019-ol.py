"""Review the 2019 Ordinary English paper (one booklet: Section 1 and Section 2).

2019: answer ten of fifteen short questions at 10 marks and four of eight
long questions at 75, all in one booklet (LC033GLP000EV, the same file id as
its scheme). No Ordinary card existed for 2019, so every card is new. The
allocation summary (scheme pages 29-32) sets each boundary; where the
support page prints a different split the card follows the summary and says
so. Two printed choices are one card each: Q2(A) bar chart or line graph
(one grid, one topic) and Q7(C) any three of the five underlined sources of
finance (the scheme marks every choice alike).
"""
from bus_lib import (Paper, ORIGINAL, comps, points, seq, unequal, single, response, fixed, permit)

T = {(1, q): 29 for q in range(1, 16)}
T.update({(2, 1): 30, (2, 2): 30, (2, 3): 31, (2, 4): 31, (2, 5): 31, (2, 6): 32, (2, 7): 32, (2, 8): 32})
P = Paper(2019, 'ordinary', {1: 'LC033GLP000EV', 2: 'LC033GLP000EV'}, 'LC033GLP000EV', T)
L, S, add, cum = P.lift, P.scheme, P.add, P.cumulative
EIGHT = 'Two points are required: 8 (4 + 4) and 7 (4 + 3).'
UNTIED = 'The 8-mark allowance is not tied to a particular point.'


def eight_seven(label):
    return unequal(label, [(4, 4), (4, 3)], None)


def flat(card):
    for r in card['rubric']['responses']:
        for a in r['allocations']:
            a['permittedMarks'] = [0, a['maxMarks']]
    return card


# ---------------------------------------------------------------- Section 1 (10 marks each)
add(1, 1, '', 'Q1', L(1, 2, 'What do the following letters stand for? Write each answer in the space provided.', 'AGM AOB EGM').replace(' AOB', '\nAOB').replace(' EGM', '\nEGM'),
    10, 'business-2-12', 'abbreviations-agm-aob-egm', 2, [4], 'The first correct term earns 4 (2 + 1 + 1); the second and third 3 each (1 + 1 + 1).',
    [comps('First correct term', (4,), ['Words written in full'], 1), comps('Second correct term', (3,), ['Words written in full'], 2),
     comps('Third correct term', (3,), ['Words written in full'], 3)],
    ['Answer key: AGM ' + S(4, 'Annual General Meeting') + '; AOB ' + S(4, 'Any Other Business') + '; EGM ' + S(4, 'Extraordinary General Meeting') + '.'])
cum(1, 2, '', 'Q2', 'Product A: Alcatel 1, prepay from €59.99. Product B: Samsung Galaxy Note 9, prepay from €859.99. (Photographs of the two phones.)\n'
    + L(1, 2, 'Businesses use high price strategies and low price strategies as part of their marketing mix. Identify the product (A or B) where the business is using:',
        '(i) Premium Pricing:', '(ii) Penetration Pricing:'),
    (5, 5), 'business-4-17', 'premium-and-penetration-pricing', 2, [4],
    'Answer key (scheme page 4): ' + S(4, '(i) Premium Pricing: Product B (Samsung Galaxy Note 9) (ii) Penetration Pricing: Product A (Alcatel 1)') + '.')
words = add(1, 3, '', 'Q3', L(1, 2, 'Choose the appropriate word/s to complete the sentence below. (Two words do not apply.)', 'INDEMNITY COSTS UTMOST GOOD FAITH INFORMATION')
            + '\n______ ' + L(1, 2, 'is an insurance principle which states that the insured person must voluntarily disclose, accurately and fully, all')
            + ' ______ ' + L(1, 2, 'relevant to the risk being insured whether requested or not.'),
            10, 'business-3-17', 'utmost-good-faith-word-bank', 2, [4], 'The first blank earns 6 and the second 4.',
            [fixed('Completed blanks', [('First blank', 6), ('Second blank', 4)])],
            ['Answer key (scheme page 4): ' + S(4, 'Utmost Good Faith is an insurance principle') + ' ... all information relevant to the risk. Indemnity and Costs are not used.'])
add(1, 4, '', 'Q4', L(1, 2, 'The euro celebrated its 20th anniversary in January 2019. Outline two advantages for Irish consumers of using the euro currency.'), 10,
    'business-6-14', 'euro-advantages-consumers', 2, [4], 'The allocation summary prices the two advantages 6 + 4.',
    [comps('Advantage 1', (6,), ['Advantage outlined'], 1), comps('Advantage 2', (4,), ['Advantage outlined'], 2)],
    ['The allocation summary (scheme page 29) prints “' + S(29, 'Two advantages: 6m + 4m') + '”; the support page prints 3 + 2 for each. The card follows the summary.',
     'Scheme examples include ' + S(4, 'Common Currency – euro – makes travel easier for Irish consumers.') + ' and reduced transaction costs.'])
memo = add(1, 5, '', 'Q5', L(1, 3, 'Draft the memorandum sent by Stephen Kennedy, ICT Manager, on today’s date to all Sales Managers reminding them that Data Protection Authorities may issue fines for non-compliance with the General Data Protection Regulation (GDPR).')
           + '\nMemorandum: To / From / Date / Re / message / Signed / Title', 10, 'business-2-12', 'gdpr-memorandum', 3, [5],
           'Seven entries: To, Date and the message at 2 each; From, Re, Signed and Title at 1 each.',
           [fixed('Memorandum', [('To', 2), ('From', 1), ('Date', 2), ('Re', 1), ('Message', 2), ('Signed', 1), ('Title', 1)])],
           ['Scheme (page 5): To ' + S(5, 'All Sales Managers') + '; From Stephen Kennedy; Date 13th June 2019; Re ' + S(5, 'GDPR non-compliance')
            + '; Signed Stephen Kennedy; Title ICT Manager. The allocation summary prints “' + S(29, 'Seven entries: 3 @ 2m each plus 4 @ 1m each') + '”.'])
cum(1, 6, '', 'Q6', L(1, 3, 'Circle the correct option in each of the following statements.',
                      '(i) When there is clear, complete and unconditional acceptance of an offer, there is an invitation to treat / a legal agreement.',
                      '(ii) In a contract, each party must give something of value to the other party and this refers to consideration / consent to contract.',
                      '(iii) Some contracts must be in writing if they are to be legally valid. This refers to legality of form / legality of purpose.',
                      '(iv) Persons under the influence of alcohol or drugs do / do not have the capacity to enter a legal contract.'),
    (4, 3, 2, 1), 'business-0-12', 'contract-options', 3, [5], 'Answer key (scheme page 5): ' + S(5, '(i) legal agreement (ii) consideration (iii) legality of form (iv) do not') + '.')
add(1, 7, '', 'Q7', L(1, 3, 'Explain the following types of taxation.', '(i) Corporation Tax:', '(ii) Value Added Tax:'), 10, 'business-3-18', 'corporation-tax-and-vat',
    3, [5], 'Each explanation earns 5 marks (3 + 2).', [comps('Corporation Tax', (3, 2), i=1), comps('Value Added Tax', (3, 2), i=2)],
    ['Scheme: ' + S(5, 'Corporation tax refers to the annual tax on a company’s profits.') + ' ' + S(5, 'Value Added Tax (VAT) is a tax on the sale of goods and services')])
cum(1, 8, '', 'Q8', L(1, 4, 'Indicate by placing a tick (✓) in the correct box, the leadership style that each statement relates to.', 'AUTOCRATIC DEMOCRATIC LAISSEZ-FAIRE',
                      'This leader discusses and consults with staff when making decisions.', 'This leader does not discuss and consult with staff when making decisions.',
                      'The leader gives her / his staff freedom to make their own decisions.'),
    (4, 3, 3), 'business-2-11', 'leadership-style-ticks', 4, [6], 'Answer key (ticks on scheme page 6): discusses and consults Democratic; does not consult Autocratic; gives freedom Laissez-faire.',
    noun='ticks')
cum(1, 9, '', 'Q9', L(1, 4, 'Complete the following Channel of Distribution.') + '\nManufacturer → Wholesaler → ______ → ______', (5, 5), 'business-4-17',
    'channel-of-distribution-complete', 4, [6], 'Answer key (scheme page 6): ' + S(6, 'Manufacturer Wholesaler Retailer Consumer') + '.', noun='entries')
add(1, 10, '', 'Q10', L(1, 4, 'Outline two reasons why an entrepreneur should prepare a business plan.'), 10, 'business-4-15', 'business-plan-reasons',
    4, [6], 'Two reasons at 5 marks each (3 + 2).', points('Reason', 2, (3, 2)))
flat(add(1, 11, '', 'Q11', L(1, 4, 'W. O’Brien Ltd is examining its liquidity. From the information below, calculate the Current Ratio. (Show formula and workings.)')
         + '\nCurrent Assets €150,000\nCurrent Liabilities €75,000', 10, 'business-3-19', 'current-ratio', 4, [6], 'Formula 3, workings 4 and answer 3.',
         [response(1, 'Current ratio', [('formula', 'Formula: Current Assets : Current Liabilities', 3), ('workings', 'Workings: 150,000 : 75,000', 4),
                                        ('answer', 'Answer: 2 : 1', 3)])],
         ['Scheme: ' + S(6, 'Formula: Current Assets : Current Liabilities Workings: 150,000 : 75,000 Answer: 2 : 1') + ' (3, 4, 3).']))
L(1, 4, 'Current Assets €150,000', 'Current Liabilities €75,000')
cum(1, 12, '', 'Q12', L(1, 5, 'Study Table 1 below and use the information to fill in the appropriate product (car) for stages A, B, C, and E of the Product Life Cycle. D has been completed for you.')
    + '\nTable 1: ' + L(1, 5, 'Electric car (EV) 1950s Chevy GM Self-Driving car The VW Golf 2.0 Litre Diesel Jeep')
    + '\nProduct Life Cycle: Launch A=, Growth B=, Maturity C=, Saturation D= 2.0 Litre Diesel Jeep, Decline E=',
    (3, 3, 2, 2), 'business-4-17', 'product-life-cycle-cars', 5, [7],
    'Answer key (scheme page 7): A GM Self-Driving Car; B Electric Car (EV); C The VW Golf; E 1950’s Chevy.', noun='stages')
cum(1, 13, '', 'Q13', L(1, 5, 'Write the word TRUE or FALSE after each of the following statements.', 'Brainstorming is an idea generation technique.',
                        'Product Screening involves developing a sample or ‘mock up’ of a product.',
                        'During the feasibility stage of product development, the product is made available to the market.',
                        'Test Marketing involves releasing a small sample in order to test consumer reaction and gain feedback.'),
    (3, 3, 2, 2), 'business-4-14', 'product-development-true-false', 5, [7], 'Answer key (scheme page 7): TRUE; FALSE; FALSE; TRUE.')
comms = L(1, 6, 'Good communication between managers and employees is key to business success. Choose the most appropriate method of communication in the following situations and explain the reason for your choice in each case.')
add(1, 14, '', 'Q14', comms + '\n' + L(1, 6, '(i) Management communicating about the financial performance of the business.',
                                    '(ii) Management issuing a formal warning to a member of staff about his/her conduct.',
                                    '(iii) Management consulting with a member of staff about an urgent decision.'),
    10, 'business-2-12', 'communication-method-choice', 6, [7], 'Each method 2; the reasons 2, 1 and 1.',
    seq(comps('Situation (i)', (2, 2), ['Method chosen', 'Reason explained']), comps('Situation (ii)', (2, 1), ['Method chosen', 'Reason explained']),
        comps('Situation (iii)', (2, 1), ['Method chosen', 'Reason explained'])),
    ['The allocation summary prints “' + S(29, 'Reasons: 3 @ 2m Explanations: 2m + 1m + 1m') + '”. Scheme: ' + S(7, 'Accept relevant/appropriate answers where students make a decision and support their decision with a valid reason.')])
cum(1, 15, '', 'Q15', '\n'.join([L(1, 6, 'Column 1 is a list of business terms. Column 2 is a list of explanations for these terms. One explanation has no match. Match the two lists by placing the letter of the correct explanation under the relevant number below.'),
                                 L(1, 6, '1. Privatisation', '2. Indigenous Firms', '3. Secondary Sector', '4. Tertiary Sector', '5. Primary Sector'),
                                 L(1, 6, 'A. Construction and manufacturing industries.', 'B. Service providers such as Ryanair and Aer Lingus.',
                                   'C. Businesses that are Irish owned and located in Ireland.', 'D. The sale of a state-owned company such as Bord Gáis.',
                                   'E. The government buying shares in a company such as AIB bank.', 'F. Extractive industries such as fishing, farming and forestry.')]),
    (3, 3, 2, 1, 1), 'business-5-13', 'sectors-and-ownership-matching', 6, [7], 'Answer key (scheme page 7): 1 D; 2 C; 3 A; 4 B; 5 F. Explanation E is unused.',
    extra=['business-5-14'], noun='matches')

# ---------------------------------------------------------------- Section 2 (75 marks each)
debs = L(2, 7, 'Debs Dress Jane Boland purchased her Debs dress from a local retailer. When she tried on the dress at home, Jane noticed a stain on the front of the dress. Jane had studied consumer law in Business class at school and remembered that goods must be of merchantable quality and fit for purpose.')
law_i = L(2, 7, '(A) (i) Name the consumer law/act that protects Jane in this situation.')
law = add(2, 1, 'ai', 'Q1(A)(i)', debs + '\n\n' + law_i, 10, 'business-0-13', 'law-protecting-jane', 7, [8], 'Name the Act: 2 + 2 + 2 + 2 + 2.',
          [comps('Consumer law', (10,), ['Act named'])], ['Answer: ' + S(8, 'The Sale of Goods and Supply of Services Act 1980') + ' (scheme: 2 + 2 + 2 + 2 + 2).'])
permit(law, 0, [0, 2, 4, 6, 8, 10])
add(2, 1, 'aii', 'Q1(A)(ii)', debs + '\n\n' + law_i + '\n' + L(2, 7, '(ii) Explain the terms merchantable quality and fit for purpose.'), 10, 'business-0-13',
    'merchantable-quality-and-fit-for-purpose', 7, [8], 'Each term 5 marks (3 + 2).', [comps('Merchantable quality', (3, 2), i=1), comps('Fit for purpose', (3, 2), i=2)],
    ['Scheme: ' + S(8, 'The goods should be of reasonable standard/quality, fit to be sold, taking into account their durability and the price paid.') + ' '
     + S(8, 'This means that goods must be able to do what they are meant to do and what they are designed for.')])
redress_i = L(2, 7, '(B) (i) Outline two forms of remedy/redress that Jane is entitled to.')
add(2, 1, 'bi', 'Q1(B)(i)', debs + '\n\n' + redress_i, 10, 'business-0-13', 'remedies-for-jane', 7, [8], 'Two forms at 5 marks each (3 + 2).', points('Remedy', 2, (3, 2)))
add(2, 1, 'bii', 'Q1(B)(ii)', debs + '\n\n' + redress_i + '\n' + L(2, 7, '(ii) Explain one method Jane could use as proof of purchase.'), 5, 'business-0-13',
    'proof-of-purchase', 7, [8], 'One method: 5 marks (3 + 2).', [comps('Proof of purchase', (3, 2))],
    ['Scheme: ' + S(8, 'A receipt or a bank statement or credit card statement as they show the cost price and the date of purchase.')])
add(2, 1, 'c', 'Q1(C)', debs + '\n' + L(2, 7, 'If the retailer refuses to offer redress, Jane will take her case to the Small Claims Court.') + '\n\n'
    + L(2, 7, '(C) Outline two advantages for a consumer in taking a case to the Small Claims Court.'), 15, 'business-0-13', 'small-claims-advantages',
    7, [9], EIGHT, eight_seven('Advantage'), [UNTIED])
advert = (L(2, 7, '\'Shocking\' job advert posted by Dublin-based firm highlights employer discrimination') + '\n'
          + L(2, 7, '‘Persons with young children need not apply’ was the sentence in a recent job advert posted by a Dublin-based oil company on the recruitment search engine, Indeed.com.')
          + ' (www.independent.ie/business)')
eq_i = L(2, 7, '(i) Name the law / act that protects an employee in cases of discrimination.')
add(2, 1, 'di', 'Q1(D)(i)', advert + '\n\n' + eq_i, 3, 'business-0-14', 'employment-equality-law', 7, [9], 'Name the law for 3 marks.',
    [single('Law', 3, 'Law named')], ['Answer: ' + S(9, 'Employment Equality Act.')])
add(2, 1, 'dii', 'Q1(D)(ii)', advert + '\n\n' + eq_i + '\n' + L(2, 7, '(ii) Outline three grounds on which discrimination is outlawed.'), 12, 'business-0-14',
    'discrimination-grounds', 7, [9], 'Three grounds at 4 marks each (2 + 2).', points('Ground', 3, (2, 2)))
add(2, 1, 'e', 'Q1(E)', L(2, 7, '(E) Outline two causes of industrial relations disputes between trade unions and employers.'), 10, 'business-0-14',
    'industrial-dispute-causes', 7, [10], 'Two causes at 5 marks each (3 + 2).', points('Cause', 2, (3, 2)))

L(2, 8, 'A sample of Government Expenditure', 'Social Protection Health Education Debt Servicing Transport EU Payments')
spend = ('A sample of Government Expenditure\nSocial Protection €20 billion; Health €15 Billion; Education €10 billion; Debt Servicing / EU Payments €11 billion; Transport €2 billion'
         + '\n(' + L(2, 8, 'Figures have been adapted for the question') + ')')
L(2, 8, '€20 billion €15 Billion €10 billion €11 billion €2 billion')
chart = add(2, 2, 'a', 'Q2(A)', spend + '\n\n' + L(2, 8, '(A) Draw a Bar Chart or Line Graph to represent the above information. (You may use graph paper.)'), 20,
            'business-5-15', 'government-expenditure-chart', 8, [11], 'Choose a bar chart or a line graph: title 2, labelled axes 2 + 1, five bars or points at 2 and five expenditures at 1.',
            [fixed('The chart you chose', [('Title', 2), ('Labelled axis 1', 2), ('Labelled axis 2', 1),
                                           ('Social Protection bar or point', 2), ('Health bar or point', 2), ('Education bar or point', 2),
                                           ('Debt Servicing / EU Payments bar or point', 2), ('Transport bar or point', 2),
                                           ('€20 billion', 1), ('€15 billion', 1), ('€10 billion', 1), ('€11 billion', 1), ('€2 billion', 1)])],
            ['You choose one of the two printed charts to answer. The scheme marks every choice alike and files them under one topic, so this is one card whichever chart you choose.',
             'Bar Chart (scheme PDF page 11): “' + S(11, '5 Bars @ 2m each 5 Exp. @ 1m each') + '”',
             'Line Graph (scheme PDF page 11): “' + S(11, '5 Pts. @ 2m each 5 Exp. @ 1m each') + '”'])
add(2, 2, 'b', 'Q2(B)', spend + '\n\n' + L(2, 8, '(B) Outline two examples of government expenditure on education.'), 10, 'business-5-15', 'education-expenditure-examples',
    8, [11], 'Two examples at 5 marks each (3 + 2).', points('Example', 2, (3, 2)))
add(2, 2, 'c', 'Q2(C)', spend + '\n\n' + L(2, 8, '(C) Outline two benefits for businesses of the Government increasing expenditure in any of the sectors above.'), 15,
    'business-5-15', 'government-expenditure-benefits', 8, [12], 'Two points are required: 8 (5 + 3) and 7 (5 + 2).', unequal('Benefit', [(5, 3), (5, 2)], None), [UNTIED])
amazon = L(2, 8, 'Multinational company Amazon to create 1,000 new jobs in Dublin') + ' (www.rte.ie)'
mnc_i = L(2, 8, '(i) Explain what is meant by the term multinational company.')
add(2, 2, 'di', 'Q2(D)(i)', amazon + '\n\n' + mnc_i, 5, 'business-6-15', 'multinational-meaning', 8, [12], 'Explanation: 5 marks (3 + 2).',
    [comps('Multinational company', (3, 2))], ['Scheme: ' + S(12, 'A Multinational Company (MNC) is a company with a base/headquarters in one country and several branches in other countries throughout the world.')])
add(2, 2, 'dii', 'Q2(D)(ii)', amazon + '\n\n' + mnc_i + '\n' + L(2, 8, '(ii) Explain two reasons why multinational companies choose to locate in Ireland.'), 15,
    'business-6-15', 'why-mncs-locate-in-ireland', 8, [12], EIGHT, eight_seven('Reason'), [UNTIED])
add(2, 2, 'e', 'Q2(E)', amazon + '\n\n' + L(2, 8, '(E) Outline two benefits, other than employment, of multinational companies for the Irish economy.'), 10, 'business-6-15',
    'mnc-benefits-irish-economy', 8, [13], 'Two benefits at 5 marks each (3 + 2).', points('Benefit', 2, (3, 2)))

cum(2, 3, 'a', 'Q3(A)', L(2, 9, '(A) List three examples of goods / services that are imported into Ireland.'), (4, 3, 3), 'business-6-13', 'imports-examples',
    9, [14], 'Scheme examples: ' + S(14, 'Oil, Cars, Fruit, Wines.') + ' Insurance from a UK company; holidays abroad.', noun='examples')
add(2, 3, 'b', 'Q3(B)', L(2, 9, '(B) Outline three reasons why goods or services are imported into Ireland.'), 20, 'business-6-13', 'reasons-for-importing',
    9, [14], 'Three reasons: 7 (4 + 3), 7 (4 + 3) and 6 (4 + 2).', unequal('Reason', [(4, 3), (4, 3), (4, 2)], None),
    ['The 7/7/6 sequence prices the three reasons, not particular reasons.'])
add(2, 3, 'c', 'Q3(C)', L(2, 9, '(C) Explain the term exports and provide one example.'), 15, 'business-6-13', 'exports-explained',
    9, [14], 'Explanation 10 (5 + 5) and example 5.', seq(comps('Exports explained', (5, 5)), single('Example', 5, 'Export example')),
    ['Scheme: ' + S(14, 'Exports are goods and services sold by businesses based in Ireland to customers in other countries')])
trade = L(2, 9, 'Irish Exports and Imports - January 2019', 'In January 2019 Irish Exports were €13,703m whereas Irish Imports were €6,520m.') + ' (www.cso.ie)'
bop_i = L(2, 9, '(D) (i) Using the figures above, calculate the Balance of Payments for the month of January 2019. Show your workings.')
flat(add(2, 3, 'di', 'Q3(D)(i)', trade + '\n\n' + bop_i, 10, 'business-6-13', 'balance-of-payments-january-2019', 9, [14],
         'Formula 2, exports 2, imports 2 and the balance 4.',
         [response(1, 'Balance of payments', [('formula', 'Formula: Balance of Payments = Total Exports minus Total Imports', 2), ('exports', '€13,703 million', 2),
                                              ('imports', '€6,520 million', 2), ('answer', 'Answer: €7,183 million', 4)])],
         ['Scheme: ' + S(14, 'Balance of Payments = Total Exports minus Total Imports = €13,703 million minus €6,520 million = Balance of Payments: €7,183 million') + ' (2 + 2 + 2, 4).']))
add(2, 3, 'dii', 'Q3(D)(ii)', trade + '\n\n' + bop_i + '\n' + L(2, 9, '(ii) State whether it is a surplus or deficit.'), 5, 'business-6-13',
    'payments-surplus-or-deficit-2019', 9, [14], 'State it for 5 marks.', [single('Surplus or deficit', 5, 'Answer stated')], ['Answer: Surplus.'])
eu = L(2, 9, '(E) Ireland trades freely with other European Union countries.')
eu_i = L(2, 9, '(i) Name three European Union countries that Ireland trades with.')
cum(2, 3, 'ei', 'Q3(E)(i)', eu + '\n' + eu_i, (4, 3, 3), 'business-6-14', 'eu-trading-partners', 9, [14],
    'Scheme: ' + S(14, 'France, Spain, Germany etc. Accept relevant answers.'), noun='countries')
add(2, 3, 'eii', 'Q3(E)(ii)', eu + '\n' + eu_i + '\n' + L(2, 9, '(ii) Explain the term tariff.'), 5, 'business-6-13', 'tariff-explained',
    9, [14], 'Explanation: 5 marks (3 + 2).', [comps('Tariff', (3, 2))], ['Scheme: ' + S(14, 'A tariff is a tax placed on foreign products.')])

smyths = L(2, 10, 'Irish Indigenous firm Smyths Toys Superstores is now the largest toy retailer in Europe. Bridie and Paddy Smyth ran a pub and newsagents in Claremorris and also sold toys. This was the origin of their children’s toys and entertainment business. Several of the Smyth family are shareholders in the company and they have over 100 stores throughout Ireland and the UK. They stock a huge range of children’s toys which varies according to the time of year. The directors and senior management help set out the vision for Smyths Toys Superstores. Tony Smyth is the Managing Director of the family-owned business.')
add(2, 4, 'a', 'Q4(A)', smyths + '\n\n' + L(2, 10, '(A) Outline three enterprising skills / characteristics that entrepreneurs display.'), 15, 'business-1-5',
    'enterprising-skills', 10, [15], 'Three at 5 marks each (3 + 2).', points('Characteristic', 3, (3, 2)))
add(2, 4, 'b', 'Q4(B)', smyths + '\n\n' + L(2, 10, '(B) Outline three risks of setting up your own business.'), 15, 'business-1-5', 'risks-of-setting-up',
    10, [15], 'Three risks at 5 marks each (3 + 2).', points('Risk', 3, (3, 2)))
plan_i = L(2, 10, '(C) (i) Name two types of plan used in business.')
cum(2, 4, 'ci', 'Q4(C)(i)', smyths + '\n\n' + plan_i, (4, 4), 'business-2-13', 'types-of-plan', 10, [16],
    'Scheme examples: ' + S(16, '• Strategic plan • Tactical plan • Contingency plan').replace('• ', '').replace(' Tactical', '; Tactical').replace(' Contingency', '; Contingency') + '; business plan; operational plan.',
    noun='types')
add(2, 4, 'cii', 'Q4(C)(ii)', smyths + '\n\n' + plan_i + '\n' + L(2, 10, '(ii) Explain one type of plan that Smyths Toys Superstores might have.'), 7, 'business-2-13',
    'smyths-plan-explained', 10, [16], 'One plan: 7 marks (1 + 3 + 3).', [comps('Plan', (1, 3, 3), ['Plan named', 'Explained', 'Developed'])],
    ['Scheme examples: ' + S(16, 'Strategic plan– long term plan outlining the goals or objective to be achieved over a longer period of time e.g. 5-year plan.')])
stock_i = L(2, 10, '(D) (i) Explain the term stock control.')
add(2, 4, 'di', 'Q4(D)(i)', smyths + '\n\n' + stock_i, 5, 'business-2-13', 'stock-control-explained', 10, [17], 'Explanation: 5 marks (3 + 2).',
    [comps('Stock control', (3, 2))], ['Scheme: ' + S(17, 'Stock control involves ensuring the business always has sufficient/ optimum stock to meet customer requirements.')])
add(2, 4, 'dii', 'Q4(D)(ii)', smyths + '\n\n' + stock_i + '\n' + L(2, 10, '(ii) Explain two reasons why stock control is important for a toy store.'), 10, 'business-2-13',
    'stock-control-importance', 10, [17], 'Two reasons at 5 marks each (3 + 2).', points('Reason', 2, (3, 2)))
flat(add(2, 4, 'e', 'Q4(E)', smyths + '\n\n' + L(2, 10, '(E) Draw a diagram to illustrate a functional organisational structure for a business with four departments.'), 15,
         'business-2-13', 'functional-structure-diagram', 10, [17], 'Shareholders, Board of Directors and Managing Director 1 each; four departments 3 each.',
         [fixed('Organisation chart', [('Shareholders', 1), ('Board of Directors', 1), ('Managing Director', 1),
                                       ('Department 1', 3), ('Department 2', 3), ('Department 3', 3), ('Department 4', 3)])],
         ['Scheme (page 17): Shareholders, Board of Directors, Managing Director; Finance, Production, Marketing, HR. ' + S(17, 'Accept other relevant departments.')]))

job = L(2, 11, 'Job advertisement – Seasonal Sales Staff for SuperClothes retail outlet',
        'Seasonal part-time sales staff required at SuperClothes retail outlet The role: As a Sales Assistant you are the face of the company. See website for full Job Description The person must be motivated and positive. See website for full Person Specification What we offer: A competitive hourly rate of €15.00 per hour, induction training, amazing staff discount (50% online and in store), a generous clothing allowance, because you love to wear our brand. See website for a list of benefits-in-kind.')
add(2, 5, 'a', 'Q5(A)', job + '\n\n' + L(2, 11, '(A) Explain the term induction training.'), 10, 'business-3-20', 'induction-training', 11, [18],
    'Explanation: 10 marks (6 + 4).', [comps('Induction training', (6, 4))],
    ['Scheme: ' + S(18, 'Induction training takes place when a new employee starts in an organisation') + ' ...'])
add(2, 5, 'b', 'Q5(B)', job + '\n\n' + L(2, 11, '(B) Outline two benefits for SuperClothes of training its sales staff.'), 15, 'business-3-20', 'training-benefits',
    11, [18], EIGHT, eight_seven('Benefit'), [UNTIED])
add(2, 5, 'c', 'Q5(C)', job + '\n\n' + L(2, 11, '(C) Explain the term benefit-in-kind.'), 15, 'business-3-20', 'benefit-in-kind-explained', 11, [18],
    'Explanation: 15 marks (6 + 6 + 3).', [comps('Benefit-in-kind', (6, 6, 3))],
    ['Scheme: ' + S(18, 'A benefit in kind is a non-financial form of income. It is also known as a perk.')])
orla = L(2, 11, 'Orla has started working for SuperClothes as a Sales Assistant. Orla will be paid €15.00 per hour. On St. Stephen’s Day staff are paid double time i.e. double the hourly wage.')
gross_i = L(2, 11, '(D) (i) Explain the term Gross Pay.')
add(2, 5, 'di', 'Q5(D)(i)', orla + '\n\n' + gross_i, 5, 'business-3-18', 'gross-pay-explained', 11, [19], 'Explanation: 5 marks (3 + 2).',
    [comps('Gross pay', (3, 2))], ['Scheme: ' + S(19, 'This refers to an employee’s wages before any deductions.')])
flat(add(2, 5, 'dii', 'Q5(D)(ii)', orla + '\n\n' + gross_i + '\n' + L(2, 11, '(ii) If Orla works 10 hours in a regular week, calculate her gross weekly pay.'), 5,
         'business-3-18', 'gross-weekly-pay', 11, [19], 'Workings 3 and answer 2.',
         [response(1, 'Gross weekly pay', [('workings', 'Workings: 10 x 15', 3), ('answer', 'Answer: €150', 2)])],
         ['Scheme: ' + S(19, 'Workings: 10 x 15 = 150 Answer: €150') + '.']))
flat(add(2, 5, 'diii', 'Q5(D)(iii)', orla + '\n\n' + gross_i + '\n' + L(2, 11, '(iii) If Orla works 8 hours on St. Stephen’s Day, calculate her gross pay for that one day.'), 5,
         'business-3-18', 'double-time-pay', 11, [19], 'Workings 3 and answer 2.',
         [response(1, 'Gross pay for the day', [('workings', 'Workings: 8 x 15 x 2', 3), ('answer', 'Answer: €240', 2)])],
         ['Scheme: ' + S(19, 'Workings: 8 x 15 x 2 = 240 Answer: €240') + '.']))
fiona = L(2, 11, 'Fiona is a manager at SuperClothes. She receives an annual Gross Salary of €35,000. Assume that deductions are calculated as follows: Net PAYE= €3,700, PRSI is 7% of Gross Salary and USC is 3% of Gross Salary.')
ded_i = L(2, 11, '(E) (i) Calculate Fiona’s total annual deductions. Show your workings.')
flat(add(2, 5, 'ei', 'Q5(E)(i)', fiona + '\n\n' + ded_i, 10, 'business-3-18', 'total-annual-deductions', 11, [19], 'PAYE 2, PRSI 3, USC 3 and the total 2.',
         [response(1, 'Total annual deductions', [('paye', 'PAYE €3,700', 2), ('prsi', 'PRSI 7% of €35,000 = €2,450', 3), ('usc', 'USC 3% of €35,000 = €1,050', 3),
                                                  ('total', 'Total deductions €7,200', 2)])],
         ['Scheme (page 19): PAYE €3,700; PRSI €2,450; USC €1,050; total deductions €7,200 (2, 3, 3, 2).']))
flat(add(2, 5, 'eii', 'Q5(E)(ii)', fiona + '\n\n' + ded_i + '\n' + L(2, 11, '(ii) Calculate Fiona’s Net Annual Salary. Show your workings.'), 10, 'business-3-18',
         'net-annual-salary', 11, [19], 'Gross salary 3, total deductions 3 and the net salary 4.',
         [response(1, 'Net annual salary', [('gross', 'Gross Salary €35,000', 3), ('deductions', '– Total Deductions €7,200', 3), ('net', 'Net Annual Salary €27,800', 4)])],
         ['Scheme (page 19): ' + S(19, 'Gross Salary €35,000 – Total Deductions €7,200 Net Annual Salary €27,800') + ' (3, 3, 4).']))
L(2, 11, 'Fiona is a manager at SuperClothes.')

joanie = L(2, 12, 'Joanie’s Gelato Ice Cream Bar Joanie got the idea of setting up an ice cream bar while on holiday in Italy. Joanie carried out market research and gathered information about the industry, who her competitors were and what customers’ preferences were. In April 2017, she opened Joanie’s Gelato Ice Cream Bar. The summer heatwave in 2018 resulted in excellent sales of Joanie’s Gelato Ice Cream.')
idea_i = L(2, 12, '(A) (i) Identify where Joanie sourced the idea for her new ice cream business.')
add(2, 6, 'ai', 'Q6(A)(i)', joanie + '\n\n' + idea_i, 5, 'business-4-14', 'joanie-idea-source', 12, [20], 'Identify the source for 5 marks.',
    [single('Source of the idea', 5, 'Source identified')], ['Scheme: ' + S(20, 'Joanie got the idea of setting up an ice cream bar while on holiday in Italy.')])
add(2, 6, 'aii', 'Q6(A)(ii)', joanie + '\n\n' + idea_i + '\n' + L(2, 12, '(ii) Outline two other sources of new product ideas for entrepreneurs.'), 10, 'business-4-14',
    'other-idea-sources', 12, [20], 'Two sources at 5 marks each (3 + 2).', points('Source', 2, (3, 2)))
mr_i = L(2, 12, '(B) (i) Explain the term market research.')
add(2, 6, 'bi', 'Q6(B)(i)', joanie + '\n\n' + mr_i, 4, 'business-4-16', 'market-research-explained', 12, [21], 'Explanation: 4 marks (2 + 2).',
    [comps('Market research', (2, 2))], ['Scheme: ' + S(21, 'Market research consists of systematically gathering, recording and analysing data about people or companies.')])
add(2, 6, 'bii', 'Q6(B)(ii)', joanie + '\n\n' + mr_i + '\n' + L(2, 12, '(ii) Explain, using an example in each case, the difference between primary research and secondary research.'), 16,
    'business-4-16', 'primary-versus-secondary-research', 12, [21], 'Primary research 8 (3 + 3 + 2) and secondary research 8 (3 + 3 + 2).',
    [comps('Primary research', (3, 3, 2), ['Explanation', 'Explanation developed', 'Example'], 1),
     comps('Secondary research', (3, 3, 2), ['Explanation', 'Explanation developed', 'Example'], 2)],
    ['Scheme: ' + S(21, 'Primary research involves going into the marketplace to gather first- hand or new business information.') + ' '
     + S(21, 'Secondary research involves accessing or using information that has already been gathered.')])
add(2, 6, 'c', 'Q6(C)', joanie + '\n\n' + L(2, 12, '(C) Outline three factors Joanie should consider when deciding on the price of her ice cream.'), 15, 'business-4-17',
    'ice-cream-pricing-factors', 12, [21], 'Three factors at 5 marks each (3 + 2).', points('Factor', 3, (3, 2)))
swot = L(2, 12, 'A SWOT analysis carried out identified the following:', '(a) A new competitor has recently opened an ice cream bar in a nearby location.',
         '(b) Joanie is considering opening a second ice cream bar in summer 2020.', '(c) The packaging and cutlery used by the business is not biodegradable.',
         '(d) The ice cream bar has developed a good reputation for high quality ice cream and excellent service.')
cum(2, 6, 'd', 'Q6(D)', joanie + '\n\n' + swot + '\n\n' + L(2, 12, 'Identify the elements of a SWOT analysis (Strength, Weakness, Opportunity and Threat) from the list (a) to (d) above.'),
    (4, 4, 4, 3), 'business-2-13', 'swot-elements', 12, [22], 'Answer key (scheme page 22): ' + S(22, '(a) Threat (b) Opportunity (c) Weakness (d) Strength') + '.',
    noun='elements')
add(2, 6, 'e', 'Q6(E)', joanie + '\n\n' + L(2, 12, '(E) Outline two ways in which Joanie’s Gelato Ice Cream Bar could become more environmentally responsible.'), 10,
    'business-5-17', 'environmental-responsibility-ways', 12, [22], 'Two ways at 5 marks each (3 + 2).', points('Way', 2, (3, 2)))

icare = L(2, 13, 'I-Care Cutlery Having read a newspaper article about France passing a new law requiring that all plastic cups, cutlery and plates be composted, Brian had the idea to set up his own business I-Care Cutlery operating as a sole trader. The business produces eco-friendly catering disposables. It makes cups, cutlery and plates that can be composted and are made of biologically-sourced materials such as plants.')
sole_i = L(2, 13, '(A) (i) Explain the term sole trader.')
add(2, 7, 'ai', 'Q7(A)(i)', icare + '\n\n' + sole_i, 5, 'business-5-14', 'sole-trader-explained', 13, [23], 'Explanation: 5 marks (3 + 2).',
    [comps('Sole trader', (3, 2))], ['Scheme: ' + S(23, 'A Sole Trader business is owned and controlled by one person.')])
add(2, 7, 'aii', 'Q7(A)(ii)', icare + '\n\n' + sole_i + '\n' + L(2, 13, '(ii) Outline two benefits of setting up as a sole trader.'), 10, 'business-5-14',
    'sole-trader-benefits', 13, [23], 'Two benefits at 5 marks each (3 + 2).', points('Benefit', 2, (3, 2)))
batch = L(2, 13, 'I-Care Cutlery makes its products using batch production methods.')
batch_i = L(2, 13, '(B) (i) Explain the term batch production.')
add(2, 7, 'bi', 'Q7(B)(i)', icare + '\n' + batch + '\n\n' + batch_i, 8, 'business-4-15', 'batch-production-explained', 13, [23], 'Explanation: 8 marks (4 + 4).',
    [comps('Batch production', (4, 4))], ['Scheme: ' + S(23, 'A certain amount or limited quantity of identical goods is produced at the same time and then production switches to a different batch or group.')])
add(2, 7, 'bii', 'Q7(B)(ii)', icare + '\n' + batch + '\n\n' + batch_i + '\n' + L(2, 13, '(ii) Outline one other method of production.'), 7, 'business-4-15',
    'other-production-method', 13, [23], 'One method: 7 marks (4 + 3).', [comps('Method', (4, 3))],
    ['Scheme: ' + S(23, 'Job Production involves making one-off products or goods made to order.') + ' ' + S(23, 'Mass Production involves the manufacture of very large quantities of identical products on a continuous basis.')])
finance = L(2, 13, 'I-Care Cutlery has used the following sources of finance: a bank overdraft, trade credit and hire-purchase. I-Care Cutlery is planning on seeking a grant and a long term loan to grow the business.')
add(2, 7, 'c', 'Q7(C)', icare + '\n\n(C) ' + finance + '\n(bank overdraft, trade credit, hire-purchase, grant and long term loan are underlined.)\n'
    + L(2, 13, 'Explain any three sources of finance underlined in the paragraph above.'), 20, 'business-3-16', 'underlined-sources-of-finance-choice', 13, [24],
    'Choose three of the five underlined sources and explain each: 8 (4 + 4), 8 (4 + 4) and 4 (2 + 2).',
    seq(comps('First source you chose', (4, 4)), comps('Second source you chose', (4, 4)), comps('Third source you chose', (2, 2))),
    ['You choose which three of the five underlined sources to answer. The scheme marks every choice alike, so this is one card whichever sources you choose.',
     'The 8/8/4 allowance is not tied to a particular source.',
     'Bank overdraft (scheme PDF page 24): “' + S(24, 'Bank Overdraft is a short-term source of finance.') + '”',
     'Trade credit (scheme PDF page 24): “' + S(24, 'A supplier allowing a business to buy stock now and pay later.') + '”',
     'Hire-purchase (scheme PDF page 24): “' + S(24, 'buying an asset by paying a deposit of a percentage of the total cost and paying the balance in regular instalments.') + '”',
     'Grant (scheme PDF page 24): “' + S(24, 'the firm receives a sum of money that does not have to be repaid provided certain conditions are met.') + '”',
     'Long term loan (scheme PDF page 24): “' + S(24, 'the firm borrows money from a financial institution.') + '”'])
merger = L(2, 13, 'I-Care Cutlery is considering expanding by means of a merger with a similar business based in the UK.')
add(2, 7, 'd', 'Q7(D)', merger + '\n\n' + L(2, 13, 'Outline two reasons why a business might choose to expand.'), 15, 'business-4-18', 'reasons-to-expand',
    13, [25], EIGHT, eight_seven('Reason'), [UNTIED])
add(2, 7, 'e', 'Q7(E)', merger + '\n\n' + L(2, 13, '(E) Explain the term merger.'), 10, 'business-4-18', 'merger-explained', 13, [25], 'Explanation: 10 marks (6 + 4).',
    [comps('Merger', (6, 4))], ['Scheme: ' + S(25, 'A merger is a friendly or voluntary amalgamation of two or more businesses for their mutual benefit.')])

promo = L(2, 14, 'There are various methods of promoting your brand. Lidl and Centra use sponsorship as a method of Public Relations.')
add(2, 8, 'a', 'Q8(A)', promo + '\n\n' + L(2, 14, '(A) Outline two benefits for a business of sponsorship as a method of Public Relations (PR).'), 10, 'business-4-17',
    'sponsorship-benefits', 14, [26], 'Two benefits at 5 marks each (3 + 2).', points('Benefit', 2, (3, 2)))
add(2, 8, 'b', 'Q8(B)', promo + '\n\n' + L(2, 14, '(B) Discuss three sales promotions techniques that retailers such as Lidl and Centra use to increase sales.'), 15, 'business-4-17',
    'sales-promotion-techniques', 14, [26], 'Three techniques at 5 marks each (3 + 2).', points('Technique', 3, (3, 2)))
media = L(2, 14, 'Lidl and Centra advertise using various media.')
adv_i = L(2, 14, '(C) (i) Outline two functions of advertising.')
add(2, 8, 'ci', 'Q8(C)(i)', media + '\n\n' + adv_i, 10, 'business-4-17', 'advertising-functions', 14, [27], 'Two functions at 5 marks each (3 + 2).',
    points('Function', 2, (3, 2)))
add(2, 8, 'cii', 'Q8(C)(ii)', media + '\n\n' + adv_i + '\n' + L(2, 14, '(ii) List two advertising media that could be used by retailers and outline reasons for your choice in each case.'),
    10, 'business-4-17', 'advertising-media-with-reasons', 14, [27], 'Two media at 5 marks each: medium 2 and reason 3.',
    points('Medium and reason', 2, (2, 3), ['Medium listed', 'Reason outlined']))
mike = L(2, 14, 'Mike is considering setting up his own store. He read online that Centra operates as a franchise.')
fr_i = L(2, 14, '(D) (i) Explain the term franchise as a form of business ownership.')
add(2, 8, 'di', 'Q8(D)(i)', mike + '\n\n' + fr_i, 12, 'business-5-14', 'franchise-explained', 14, [27], 'Explanation: 12 marks (4 + 4 + 4).',
    [comps('Franchise', (4, 4, 4))], ['Scheme: ' + S(27, 'This is the granting of a licence by the owner of a business (the franchisor) to another firm (the franchisee)') + ' ...'])
cum(2, 8, 'dii', 'Q8(D)(ii)', mike + '\n\n' + fr_i + '\n' + L(2, 14, '(ii) List two other examples of franchises.'), (4, 4), 'business-5-14', 'franchise-examples',
    14, [27], 'Scheme examples: ' + S(27, 'Supermacs, Costa Coffee, Starbucks, The ZipYard, Circle K, Snap Printing.'), noun='examples')
add(2, 8, 'e', 'Q8(E)', mike + '\n\n' + L(2, 14, '(E) Outline two advantages for Mike of setting up a Centra store under the franchise model rather than operating as an independent retailer.'),
    10, 'business-4-18', 'franchise-advantages-mike', 14, [28], 'Two advantages at 5 marks each (3 + 2).', points('Advantage', 2, (3, 2)), extra=['business-5-14'])

# ---------------------------------------------------------------- checks and write-out
qn = lambda c: c['questionRef'].split(' Q')[1].split('(')[0]
for section, count, total in [('1', 15, 10), ('2', 8, 75)]:
    for q in range(1, count + 1):
        got = sum(c['totalMarks'] for c in P.created if c['section'] == section and qn(c) == str(q))
        assert got == total, (section, q, got)
assert not [i for i in ORIGINAL if i.startswith('bus-2019-ol-')]
assert not P.pools

SELECTION = {
    1: 'No finite printed answer menu occurs in Section 1 (answer ten of fifteen at 10 marks). The word bank in Q3, the ticks in Q8, the circled options in Q6, TRUE/FALSE in Q13 and the matching rows in Q15 are required answer formats. Q14 lets the candidate choose a method for each situation (an open choice, no printed list). Support-note lists are open examples.',
    2: 'Two printed choices, each one card: Q2(A) a bar chart or a line graph (one grid, one topic) and Q7(C) any three of the five underlined sources of finance (the scheme marks every choice alike). Q2(C) “any of the sectors above” is an open choice of context. Sub-parts with their own published marks are separate cards. Support-note lists are open examples.',
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
    if m.lower().startswith('answer'):
        return 'exam-navigation', 'The rubric sets how many whole questions a candidate answers. Every numbered question remains in the practice corpus as separate cards.', None
    if m == 'any three' and own(w, m, 'Explain any three sources of finance underlined'):
        return 'finite-choice', 'Section 2 Q7(C) asks for any three of the five underlined sources of finance. The scheme marks every choice alike, so one card carries all five with the scheme wording for each.', 'bus-2019-ol-s2-q7c'
    if m == 'or' and own(w, m, 'Bar Chart or Line Graph'):
        return 'finite-choice', 'Section 2 Q2(A) offers a bar chart or a line graph. The scheme marks either alike under one topic, so it is one card.', 'bus-2019-ol-s2-q2a'
    if m == 'Choose' and own(w, m, 'Choose the appropriate word/s'):
        return 'required-headings', 'Section 1 Q3 is a word-bank completion: both blanks are required and the printed words are the answer options, not optional tasks.', None
    if m == 'Choose' and own(w, m, 'Choose the most appropriate method of communication'):
        return 'open-response', 'Section 1 Q14 asks the candidate to choose and justify a method for each of three required situations; no closed list is printed.', None
    if m == 'or' and (own(w, m, 'TRUE or FALSE') or own(w, m, 'True or False')):
        return 'required-headings', 'TRUE/FALSE are answer labels for each of the four required statements in Section 1 Q13, not optional tasks.', None
    if m == 'or' and own(w, m, 'surplus or deficit'):
        return 'required-headings', 'Section 2 Q3(D)(ii) requires a determination of surplus or deficit; it is one required answer, not a choice of task.', None
    if m == 'or' and own(w, m, 'A or B'):
        return 'required-headings', 'Section 1 Q2 asks which product (A or B) fits each of two required pricing strategies; both are required.', None
    for phrase in ('requested or not', 'alcohol or drugs', 'a sample or ‘mock up’', 'goods or services are imported',
                   'multinational companies choose to locate', 'might choose to expand'):
        if own(w, m, phrase):
            return 'case-context', f'“{phrase}” is wording inside a printed statement or question, not a choice of task.', None
    assert (fileid, page) in {('LC033GLP000EV', 1), ('LC033GLP000EV', 7)} and m in ('either', 'or'), (fileid, page, m, w)
    return 'exam-navigation', 'The cover and Section 2 rubrics set how many whole questions a candidate answers. Every numbered question remains in the practice corpus as separate cards.', None


n = P.write([(1, range(1, 16)), (2, range(1, 9))], SELECTION, classify,
            'Every part of {year} Ordinary Section {section} Question {q} was visually checked against its SEC paper, allocation summary and expected responses. The single-booklet identity keeps the short (n) and long (S2Q) question numbering apart.')
print(f'Reviewed {len(P.created)} 2019 Ordinary tasks; classified {n} raw selection matches.')
