"""Review the 2024 Ordinary English paper (Section 1 and Section 2).

Sixty-nine legacy IDs keep their ID and total with correction records. Five
legacy cards become the first printed route of their finite pools; Section 2
Q9(A)(ii) and the Q9(E) pool are new.
"""
from bus_lib import (Paper, ORIGINAL, comps, points, seq, unequal, single, ten_five, response,
                     fixed, legacy_route, opt_resp, permit)

T = {(1, q): 3 for q in range(1, 16)}
T.update({(2, 1): 4, (2, 2): 4, (2, 3): 4, (2, 4): 5, (2, 5): 5, (2, 6): 5, (2, 7): 6, (2, 8): 6, (2, 9): 6})
P = Paper(2024, 'ordinary', {1: 'LC033GLP032EV', 2: 'LC033GLP033EV'}, 'LC033GLP000EV', T)
L, S, add, cum = P.lift, P.scheme, P.add, P.cumulative
TWO = 'Two points are required: 10 (7 + 3) and 5 (4 + 1).'
UNTIED = 'The 10-mark allowance is not tied to a particular point.'
EIGHT_SEVEN = unequal('Point', [(4, 4), (4, 3)], None)

# ---------------------------------------------------------------- Section 1
add(1, 1, '', 'Q1', L(1, 3, 'What do the following letters stand for? Write each answer in the space provided.', 'ATM', 'DIRT', 'APR'), 10,
    'business-3-16', 'abbreviations-atm-dirt-apr', 3, [7], 'Each term carries its own marks: 3 (1 + 1 + 1), 4 (1 + 1 + 1 + 1) and 3 (1 + 1 + 1).',
    [comps('ATM (first term)', (3,), ['Term written in full'], 1), comps('DIRT (second term)', (4,), ['Term written in full'], 2),
     comps('APR (third term)', (3,), ['Term written in full'], 3)],
    ['Answer key: ATM ' + S(7, 'Automated Teller Machine') + '; DIRT ' + S(7, 'Deposit Interest Retention Tax') + '; APR '
     + S(7, 'Annual Percentage Rate') + '. Each word earns one mark of its term.'], extra=['business-3-18'])
add(1, 2, '', 'Q2', L(1, 3, 'Choose the appropriate terms to complete the sentence below. (One term does not apply.)', 'Court of Auditors Parliament Court of Justice',
                      'Members of the European ____________________________ are directly elected by citizens of the European Union. The European ____________________________ ensures that the EU budget is spent correctly.'),
    10, 'business-6-14', 'eu-institutions-word-bank', 3, [7], 'Each completed blank earns 5 marks.',
    seq(single('First blank', 5, 'Term chosen'), single('Second blank', 5, 'Term chosen')),
    ['Answer key: Members of the European ' + S(7, 'Parliament') + '; the European ' + S(7, 'Court of Auditors') + '. Court of Justice is not used.'])
cum(1, 3, '', 'Q3', L(1, 3, 'Circle the correct option in each of the following statements.',
                      '(i) A functional structure divides the business into departments / geographic locations.',
                      '(ii) A team based organisation structure is referred to as a matrix / product structure.',
                      '(iii) A narrow / wide span of control means there are a large number of employees reporting to one manager.',
                      '(iv) Delayering involves adding / removing layers of employees in the business.'),
    (3, 3, 2, 2), 'business-2-13', 'organisation-structure-options', 3, [7],
    'Answer key (circled on scheme page 7): (i) departments; (ii) matrix; (iii) wide; (iv) removing.')
cum(1, 4, '', 'Q4', L(1, 4, 'Indicate by placing a tick (✓) in the correct box, the method of expansion to which each statement relates.')
    + '\nMerger / Franchise / Takeover / Strategic Alliance\n'
    + S(8, 'Subway allows other business owners to use their business model and logo in return for a fee and a percentage of profits.') + '\n'
    + S(8, 'Apple temporarily joined forces with Mastercard when they released Apple Pay.') + '\n'
    + S(8, 'Disney and Pixar joined their businesses together permanently to form a new company.') + '\n'
    + S(8, 'Coca Cola purchased over 51% of the shares of Costa Coffee to become its new owner.'),
    (3, 3, 2, 2), 'business-4-18', 'expansion-methods-ticks', 4, [8],
    'Answer key (ticks on scheme page 8): Subway Franchise; Apple and Mastercard Strategic Alliance; Disney and Pixar Merger; Coca Cola and Costa Takeover.',
    fix='the company names printed as logos on the paper are read from the scheme’s own statement text')
add(1, 5, '', 'Q5', L(1, 4, 'Outline two ways in which a business could be more environmentally friendly.'), 10, 'business-5-17',
    'environmentally-friendly-ways', 4, [8], 'Outline two ways at 5 marks each (3 + 2).', points('Way', 2, (3, 2)),
    ['Scheme examples include ' + S(8, 'Minimise waste/safe disposal of waste') + ' and ' + S(8, 'Use eco-friendly vehicles, such as electric or hybrid cars') + '.'])
plc = (L(1, 5, 'The diagram below illustrates the product life cycle. Answer the questions which follow.')
       + '\nProduct Life Cycle (sales against time): Launch, Growth, Stage 3, Saturation, Decline.')
add(1, 6, 'i', 'Q6(i)', plc + '\n\n' + L(1, 5, '(i) Identify the stage above, labelled stage 3.'), 5, 'business-4-17', 'plc-stage-3', 5, [9],
    'Identify the stage for 5 marks.', [single('Stage 3', 5, 'Stage identified')], ['Answer: ' + S(9, 'Maturity') + '.'])
add(1, 6, 'ii', 'Q6(ii)', plc + '\n\n' + L(1, 5, '(ii) Identify a stage of the product life cycle where sales decrease.'), 5, 'business-4-17',
    'plc-sales-decrease-stage', 5, [9], 'Identify one stage for 5 marks.', [single('Stage where sales decrease', 5, 'Stage identified')],
    ['Scheme: ' + S(9, 'Saturation / Decline') + '.'])
cum(1, 7, '', 'Q7', L(1, 5, 'Write the word TRUE or FALSE after each of the following statements.',
                      'Variable costs remain the same regardless of how many units of a product are produced.',
                      'The Breakeven point is the point at which revenue and costs are equal.', 'Rent is an example of a fixed cost.',
                      'The margin of safety is forecast sales minus the breakeven point.'),
    (3, 3, 2, 2), 'business-3-19', 'breakeven-true-false', 5, [9], 'Answer key: False; True; True; True (scheme page 9).')
pay = add(1, 8, '', 'Q8', L(1, 6, 'Calculate Ian Kenny’s net annual take home pay from the following details.')
          + '\nName: Ian Kenny\nGross Pay 38,000\nDeductions:\nPAYE: (20% of €38,000) 7,600\n-Tax Credit 3,550\nNet PAYE A\nPRSI: (4% of €38,000) B\n'
            'USC: (3% of €38,000) C 1,140\nTotal Deductions: D\nNet Annual Take-home Pay E',
          10, 'business-3-18', 'net-take-home-pay', 6, [9], 'A 3, B 3, D 2 and E 2; one mark per figure or method for workings if required.',
          [response(1, 'Missing figures', [('a', 'A. Net PAYE: €4,050', 3), ('b', 'B. PRSI: €1,520', 3), ('d', 'D. Total Deductions: €6,710', 2),
                                           ('e', 'E. Net Annual Take-home Pay: €31,290', 2)])],
          ['Answer key: A ' + S(9, '€4,050') + '; B ' + S(9, '€1,520') + '; D ' + S(9, '€6,710') + '; E ' + S(9, '€31,290') + '. C (1,140) is printed.',
           'Scheme: “' + S(9, 'If required, allow one mark per figure/method for workings.') + '”'])
for v in ['Gross Pay 38,000', 'PAYE: (20% of €38,000)', '-Tax Credit 7,600 - 3,550', 'Net PAYE A', 'PRSI: (4% of €38,000) B', 'USC: (3% of €38,000) C 1,140',
          'Total Deductions: D', 'Net Annual Take-home Pay E']:
    L(1, 6, v)
cum(1, 9, '', 'Q9', L(1, 6, 'Match the explanation with the relevant State agency/organisation from the list below.',
                      'Local Enterprise Office (LEO) IDA Ireland Enterprise Ireland',
                      'Assists existing Irish business in expanding into foreign markets',
                      'Provides training, mentoring and grant aid to entrepreneurs setting up their business',
                      'Attracts Multinational companies and global firms to set up in Ireland.'),
    (4, 3, 3), 'business-5-15', 'state-agencies-matching', 6, [9],
    'Answer key: foreign markets Enterprise Ireland; training, mentoring and grant aid Local Enterprise Office; multinationals IDA Ireland (scheme page 9).')
cum(1, 10, '', 'Q10', L(1, 7, 'Identify the three other elements of a SWOT/SCOT analysis.') + '\n2. Weakness/Challenge is printed; 1, 3 and 4 are blank.',
    (4, 3, 3), 'business-2-13', 'swot-elements', 7, [10], 'Answer key (scheme page 10): 1. Strengths; 3. Opportunities; 4. Threats.')
add(1, 11, '', 'Q11', L(1, 7, 'Outline two methods a business could use to encourage intrapreneurship.'), 10, 'business-1-5',
    'encouraging-intrapreneurship', 7, [10], 'Outline two methods at 5 marks each (3 + 2).', points('Method', 2, (3, 2)),
    ['Scheme examples include ' + S(10, 'Employee of the month award encourages employees') + ' and ' + S(10, 'Suggestion box') + '.'])
cum(1, 12, '', 'Q12', L(1, 7, 'Complete the table below by matching the correct remedy for breach of contract with the corresponding explanation.',
                        'Rescind the contract Compensation Specific Performance', 'The Judge orders the contract to be completed', 'The contract is cancelled',
                        'A sum of money is paid to the other party'),
    (4, 3, 3), 'business-0-12', 'breach-of-contract-remedies', 7, [10],
    'Answer key (scheme page 10): Judge orders completion Specific Performance; contract cancelled Rescind the Contract; sum of money Compensation.')
cum(1, 13, '', 'Q13', L(1, 7, 'Complete the stages in the formation of a team:') + '\n1. ______ 2. ______ 3. Norming 4. ______',
    (4, 3, 3), 'business-3-20', 'team-formation-stages', 7, [10], 'Answer key (scheme page 10): 1. Forming; 2. Storming; 4. Performing.')
cum(1, 14, '', 'Q14', L(1, 8, 'Indicate whether each of the following statements refers to a Public Limited Company or a Private Limited Company by writing public or private after each statement.',
                        '(i) The company can raise capital by selling shares to the public on the stock market.',
                        '(ii) This company can have a maximum of 149 shareholders.', '(iii) PLC must be written after the company name.'),
    (4, 3, 3), 'business-5-14', 'public-private-company', 8, [11], 'Answer key: (i) Public; (ii) Private; (iii) Public (scheme page 11).')
cum(1, 15, '', 'Q15', '\n'.join([L(1, 8, 'In the following table, Column 1 is a list of business terms and Column 2 is a list of explanations.'),
                                 L(1, 8, '1. Tactical Plan', '2. Operational Plan', '3. Contingency Plan', '4. Strategic Plan', '5. Mission Statement'),
                                 L(1, 8, 'A Plan that covers the day-to-day running of the business.', 'B A long-term plan for the business.',
                                   'C Setting out the number and type of staff required in order to achieve the organisation’s goal.',
                                   'D A plan which sets out the overall vision/goal of the organisation.', 'E Short-term plan for a business.',
                                   'F Back-up plan to cope with unforeseen events or emergencies.'),
                                 L(1, 8, 'Match the two lists by placing the letter of the correct explanation under the number of the relevant business term below. One explanation has no match.')]),
    (2, 2, 2, 2, 2), 'business-2-13', 'planning-terms-matching', 8, [11], 'Answer key: 1 E; 2 A; 3 F; 4 B; 5 D. Explanation C is unused (scheme page 11).')

# ---------------------------------------------------------------- Section 2
lily = L(2, 2, "Lily purchased a new smartwatch for €195. After two weeks, the touchscreen on the watch stopped working, and the device failed to charge properly. When she returned to the shop, the manager gave Lily the manufacturer's address and said she should contact the manufacturer of the watch.")
add(2, 1, 'a', 'Q1(A)', lily + '\n\n' + L(2, 2, '(A) Name the consumer law that protects Lily in this situation.'), 10, 'business-0-13',
    'consumer-law-named', 2, [12], 'Name the Act: five words at 2 marks each.', [comps('Consumer law', (10,), ['Act named'])],
    ['Answer: ' + S(12, 'The Sale of Goods and Supply of Services Act 1980') + '. For 0 to 5 correct words, record 0, 2, 4, 6, 8 or 10 marks.'])
permit(P.created[-1], 0, [0, 2, 4, 6, 8, 10])
add(2, 1, 'bi', 'Q1(B)(i)', lily + '\n\n' + L(2, 2, '(i) Outline two provisions of the law named above that are relevant to Lily’s situation.'), 10, 'business-0-13',
    'relevant-provisions', 2, [12], 'Outline two provisions at 5 marks each (4 + 1).', points('Provision', 2, (4, 1)))
add(2, 1, 'bii', 'Q1(B)(ii)', lily + '\n\n' + L(2, 2, '(ii) Outline two forms of redress that Lily is entitled to in the above case.'), 10, 'business-0-13',
    'forms-of-redress', 2, [12], 'Outline two forms at 5 marks each (4 + 1).', points('Form of redress', 2, (4, 1)))
pilots = L(2, 2, 'Aer Lingus regional pilots plan work-to-rule', 'Pilots at Emerald Airlines, which operates the Aer Lingus regional network, recently voted for industrial action.', sep='\n')
add(2, 1, 'ci', 'Q1(C)(i)', pilots + '\n\n' + L(2, 2, '(i) Explain the term work-to-rule.'), 5, 'business-0-14', 'work-to-rule',
    2, [13], 'Explain the term for 5 marks (4 + 1).', [comps('Work-to-rule', (4, 1))])
add(2, 1, 'cii', 'Q1(C)(ii)', pilots + '\n\n' + L(2, 2, '(ii) Other than a work to rule, outline one other type of industrial action.'), 10, 'business-0-14',
    'other-industrial-action', 2, [13], 'Outline one type for 10 marks (7 + 3).', [comps('Type of industrial action', (7, 3))])
add(2, 1, 'd', 'Q1(D)', pilots + '\n\n' + L(2, 2, '(D) Outline two benefits of good industrial relations in the workplace.'), 15, 'business-0-14',
    'good-industrial-relations-benefits', 2, [13], TWO, ten_five('Benefit'), [UNTIED])
add(2, 1, 'e', 'Q1(E)', pilots + '\n\n' + L(2, 2, '(E) Describe two functions of a trade union.'), 15, 'business-0-14',
    'trade-union-functions', 2, [14], TWO, ten_five('Function'), [UNTIED])

butter = L(2, 3, 'Ór-Real Irish Butter was launched in October 2021. It is made in Kanturk, Co. Cork, by North Cork Creameries, which is a farmer-owned co-operative.')
add(2, 2, 'ai', 'Q2(A)(i)', butter + '\n\n' + L(2, 3, '(i) Ór-Real Irish Butter operates in the secondary sector of the Irish economy. Explain what is meant by the secondary sector.'),
    5, 'business-5-13', 'secondary-sector-explained', 3, [15], 'Explain for 5 marks (3 + 2).', [comps('Secondary sector', (3, 2))])
cum(2, 2, 'aii', 'Q2(A)(ii)', butter + '\n\n' + L(2, 3, '(ii) Name the two other sectors of the economy.'), (5, 5), 'business-5-13',
    'other-sectors-named', 3, [15], 'Answer key: ' + S(15, 'Primary Sector') + ' and ' + S(15, 'Tertiary Sector') + '.', noun='sectors')
add(2, 2, 'b', 'Q2(B)', butter + '\n\n' + L(2, 3, '(B) Outline two challenges facing the secondary sector in Ireland.'), 15, 'business-5-13',
    'secondary-sector-challenges', 3, [15], TWO, ten_five('Challenge'), [UNTIED])
add(2, 2, 'c', 'Q2(C)', butter + '\n\n' + L(2, 3, '(C) Explain the term co-operative as mentioned in the text above.'), 10, 'business-5-14',
    'co-operative-explained', 3, [16], 'One explanation: 10 marks (5 + 5).', [comps('Co-operative', (5, 5))])
revenue = L(2, 3, 'Three firms pay a third of all corporation tax', 'According to revenue data, Ireland’s corporation tax takings are heavily concentrated in a small number of large foreign-owned multinationals.', sep='\n')
cum(2, 2, 'di', 'Q2(D)(i)', revenue + '\n\n' + L(2, 3, '(i) List three taxes, other than corporation tax, collected by the Irish Government.'), (5, 5, 5),
    'business-3-18', 'three-other-taxes', 3, [16], 'Scheme examples include VAT, PAYE, Capital Gains Tax, DIRT, USC and ' + S(16, 'Local Property Tax') + '.', noun='taxes')
add(2, 2, 'dii', 'Q2(D)(ii)', revenue + '\n\n' + L(2, 3, '(ii) Outline one impact of the reliance on corporation tax by the Irish Government.'), 5, 'business-5-15',
    'corporation-tax-reliance-impact', 3, [16], 'Outline one impact for 5 marks (4 + 1).', [comps('Impact', (4, 1))], extra=['business-3-18'])
add(2, 2, 'e', 'Q2(E)', L(2, 3, '(E) Describe two benefits of a low unemployment rate for the Irish economy.'), 15, 'business-5-15',
    'low-unemployment-benefits', 3, [17], TWO, ten_five('Benefit'), [UNTIED])

bop = L(2, 4, 'Balance of Payments, Q1 2023') + '\nGoods: Exports €89bn, Imports €33bn. Services: Exports €83bn, Imports €85bn. (Central Statistics Office)'
add(2, 3, 'ai', 'Q3(A)(i)', bop + '\n\n' + L(2, 4, '(i) Using the figures above, calculate the Balance of Payments for Q1 2023. Show your workings.'), 10,
    'business-6-13', 'balance-of-payments-calculation', 4, [18], 'Six figures at 1 mark each and the balance at 4 (2 + 2).',
    [response(1, 'Balance of payments', [('exports', 'Total exports: €89bn + €83bn = €172bn', 3), ('imports', 'Total imports: €33bn + €85bn = €118bn', 3),
                                         ('balance', 'Balance: €172bn – €118bn = €54bn', 4)])],
    ['Scheme working: ' + S(18, 'Total Exports = €89bn + €83bn = €172bn') + '; ' + S(18, 'Total Imports = €33bn + €85bn = €118bn') + '; balance €54bn.',
     'The goods-and-services route (€56bn – €2bn = €54bn) earns the same marks.'])
permit(P.created[-1], 0, [0, 2, 4], 2)
add(2, 3, 'aii', 'Q3(A)(ii)', bop + '\n\n' + L(2, 4, '(ii) State whether it is a surplus or a deficit.'), 5, 'business-6-13', 'surplus-or-deficit',
    4, [18], 'State it for 5 marks.', [single('Surplus or deficit', 5, 'Answer stated')], ['Answer: ' + S(18, 'Surplus') + '.'])
add(2, 3, 'b', 'Q3(B)', bop + '\n\n' + L(2, 4, '(B) Outline two benefits of international trade for consumers in Ireland.'), 15, 'business-6-13',
    'trade-benefits-consumers', 4, [18], TWO, ten_five('Benefit'), [UNTIED])
barrier = opt_resp([('component-1', 'Component 1', 4), ('component-2', 'Component 2', 3)])
P.pool(2, 3, 'c', '3(C)', 4, [4, 18], 3, L(2, 4, '(C) Explain any three of the following barriers to international trade:'),
       bop + '\n\nExplain the following three barriers to international trade:',
       [dict(id='quota', label='Quota'), dict(id='tariff', label='Tariff'), dict(id='embargo', label='Embargo'), dict(id='subsidies', label='Subsidies')],
       20, 'Explain all three selected barriers: 7 (4 + 3), 7 (4 + 3) and 6 (4 + 2).', ['The 7/7/6 sequence prices the three explanations, not particular barriers.'],
       'business-6-13', 'trade-barriers',
       'The paper prints a closed list of four barriers and asks for any three. All four selections are generated at 20 marks with the 7/7/6 sequence unattached; the legacy card is the first three printed barriers.',
       legacy=legacy_route('bus-2024-ol-s2-q3c', ['quota', 'tariff', 'embargo'], 4, [4, 18],
                           'question text lifted from the printed paper; the card becomes the first three printed barriers of the expanded choose-three pool.'),
       ordered=unequal('Barrier response', [(4, 3), (4, 3), (4, 2)], None))
for v in ['(i) Quota', '(ii) Tariff', '(iii) Embargo', '(iv) Subsidies']:
    L(2, 4, v)
glob = L(2, 4, 'A global business sees the world as one market and aims to sell the same product worldwide.')
cum(2, 3, 'd', 'Q3(D)', glob + '\n\n' + L(2, 4, '(D) List two examples of global businesses.'), (7, 3), 'business-6-15', 'global-business-examples',
    4, [19], 'Scheme examples: ' + S(19, 'Apple, Coca-Cola, Amazon, Dell, Nike, Toyota, Microsoft, Intel, HP, Google, Facebook (Meta), VW etc.'), noun='examples')
add(2, 3, 'e', 'Q3(E)', glob + '\n\n' + L(2, 4, '(E) Outline two challenges for global businesses when operating in international markets.'), 15, 'business-6-15',
    'global-business-challenges', 4, [19], TWO, ten_five('Challenge'), [UNTIED])

wrc = L(2, 5, 'A worker with 51 years’ service has been awarded €30,000 at the Workplace Relations Commission for unfair dismissal.')
add(2, 4, 'a', 'Q4(A)', wrc + '\n\n' + L(2, 5, '(A) Outline three reasons, other than age, for unfair dismissal.'), 20, 'business-0-14',
    'unfair-dismissal-reasons', 5, [20], 'Three reasons: 7 (5 + 2), 7 (5 + 2) and 6 (5 + 1).', unequal('Reason', [(5, 2), (5, 2), (5, 1)], None),
    ['The 7/7/6 sequence prices the three reasons, not particular grounds.'])
add(2, 4, 'b', 'Q4(B)', wrc + '\n\n' + L(2, 5, '(B) Outline one non-legislative method of solving an industrial relations dispute.'), 10, 'business-0-14',
    'non-legislative-dispute-method', 5, [21], 'One method: 7 + 3.', [comps('Method', (7, 3))])
cpa = L(2, 5, 'The Consumer Protection Act 2007 protects consumers from unfair commercial practices.')
P.pool(2, 4, 'c', '4(C)', 5, [5, 22], 2, L(2, 5, '(C) Explain two of the following practices prohibited by the Consumer Protection Act 2007:'),
       cpa + '\n\nExplain the following two practices prohibited by the Consumer Protection Act 2007:',
       [dict(id='misleading-advertising', label=L(2, 5, '(i) False or misleading advertising')),
        dict(id='false-descriptions', label=L(2, 5, '(ii) False product descriptions')), dict(id='false-pricing', label=L(2, 5, '(iii) False pricing'))],
       15, 'Explain both selected practices: 10 (7 + 3) and 5 (4 + 1).', ['The 10-mark allowance is not tied to a particular practice.'],
       'business-0-13', 'prohibited-practices',
       'The paper prints a closed list of three practices and asks for two. All three pairs are generated at 15 marks with the 10/5 split unattached; the legacy card is the first printed pair.',
       legacy=legacy_route('bus-2024-ol-s2-q4c', ['misleading-advertising', 'false-descriptions'], 5, [5, 22],
                           'question text lifted from the printed paper; the card becomes the first printed pair of the expanded choose-two pool.'),
       ordered=ten_five('Practice response'))
cum(2, 4, 'd', 'Q4(D)', cpa + '\n\n' + L(2, 5, '(D) Name the organisation responsible for enforcing the Consumer Protection Act 2007.'), (3, 3, 2, 2),
    'business-0-13', 'ccpc-named', 5, [22], 'Answer: ' + S(22, 'Competition and Consumer Protection Commission (CCPC)') + '; the four words carry 3 + 3 + 2 + 2.',
    noun='words of the name')
element = opt_resp([('component-1', 'Component 1', 4), ('component-2', 'Component 2', 3)])
P.pool(2, 4, 'e', '4(E)', 5, [5, 23], 3, L(2, 5, '(E) Explain three of the following elements of a legal contract:'),
       'Explain the following three elements of a legal contract:',
       [dict(id='consideration', label=L(2, 5, '(i) Consideration')), dict(id='capacity', label=L(2, 5, '(ii) Capacity to Contract')),
        dict(id='consent', label=L(2, 5, '(iii) Consent to Contract')), dict(id='legality', label=L(2, 5, '(iv) Legality of Purpose'))],
       20, 'Explain all three selected elements: 7 (4 + 3), 7 (4 + 3) and 6 (4 + 2).', ['The 7/7/6 sequence prices the three explanations, not particular elements.'],
       'business-0-12', 'contract-elements',
       'The paper prints a closed list of four elements and asks for three. All four selections are generated at 20 marks with the 7/7/6 sequence unattached; the legacy card is the first three printed elements.',
       legacy=legacy_route('bus-2024-ol-s2-q4e', ['consideration', 'capacity', 'consent'], 5, [5, 23],
                           'question text lifted from the printed paper; the card becomes the first three printed elements of the expanded choose-three pool.'),
       ordered=unequal('Element response', [(4, 3), (4, 3), (4, 2)], None))

blizzard = L(2, 6, 'Blizzard Entertainment is a leading American developer of video games with an office in Cork city. The company offers its employees a comprehensive healthcare and insurance package and employees engage in company-wide team events.')
add(2, 5, 'a', 'Q5(A)', blizzard + '\n\n' + L(2, 6, '(A) Explain one risk and one reward for entrepreneurs who set up their own business.'), 15, 'business-1-5',
    'entrepreneur-risk-and-reward', 6, [24], 'One risk 8 (4 + 4) and one reward 7 (4 + 3).', [comps('Risk', (4, 4), i=1), comps('Reward', (4, 3), i=2)])
maslow = 'Maslow’s Hierarchy of Needs (printed): 5. Self Actualisation; 4. ______; 3. Social needs; 2. Safety needs; 1. ______'
add(2, 5, 'bi', 'Q5(B)(i)', blizzard + '\n\n' + maslow + '\n\n' + L(2, 6, '(i) Below is an image of Maslow’s Hierarchy of Needs. Identify the missing stages labelled 1 and 4.'),
    10, 'business-2-11', 'maslow-missing-stages', 6, [25], 'Stage 1 earns 7 and stage 4 earns 3.',
    seq(single('Stage 1', 7, 'Stage 1 named'), single('Stage 4', 3, 'Stage 4 named')),
    ['Answer key: 1. ' + S(25, 'Physiological/Basic human needs') + '; 4. ' + S(25, 'Esteem needs') + '.'])
add(2, 5, 'bii', 'Q5(B)(ii)', blizzard + '\n\n' + L(2, 6, '(ii) Using the information from the text above identify how Blizzard Entertainment satisfies their employees safety needs and social needs.'),
    10, 'business-2-11', 'blizzard-safety-social-needs', 6, [25], 'Safety needs 5 and social needs 5.',
    seq(single('Safety needs', 5, 'Identified from the text'), single('Social needs', 5, 'Identified from the text')),
    ['Scheme: safety, the ' + S(25, 'comprehensive healthcare and insurance package') + '; social, ' + S(25, 'company-wide team events') + '.'])
for v in ['5. Self Actualisation', '3. Social needs', '2. Safety needs']:
    L(2, 6, v)
add(2, 5, 'c', 'Q5(C)', blizzard + '\n\n' + L(2, 6, '(C) Outline two benefits for a business of managers using a democratic leadership style.'), 15, 'business-2-11',
    'democratic-leadership-benefits', 6, [25], TWO, ten_five('Benefit'), [UNTIED])
add(2, 5, 'd', 'Q5(D)', blizzard + '\n\n' + L(2, 6, '(D) Blizzard employees work successfully in teams to achieve many of the targets in the business. Outline two disadvantages of working in teams.'),
    15, 'business-3-20', 'teamwork-disadvantages', 6, [26], TWO, ten_five('Disadvantage'), [UNTIED])
add(2, 5, 'e', 'Q5(E)', blizzard + '\n\n' + L(2, 6, '(E) Outline one duty Blizzard have as a data controller in relation to their customers’ data under General Data Protection Regulation (GDPR).'),
    10, 'business-2-12', 'gdpr-data-controller-duty', 6, [26], 'One duty: 10 marks (7 + 3).', [comps('Duty', (7, 3))], extra=['business-0-13'])

revolut = L(2, 7, 'Banking and payments app Revolut is launching car insurance in Ireland in partnership with insurer AIG.')
mortgage = L(2, 7, 'Revolut has also announced plans to offer mortgage products to its 30 million customers around the world for the first time.')
add(2, 6, 'a', 'Q6(A)', revolut + '\n\n' + L(2, 7, '(A) Outline two benefits to customers of using apps for banking services.'), 15, 'business-3-16',
    'banking-app-benefits', 7, [27], TWO, ten_five('Benefit'), [UNTIED])
add(2, 6, 'b', 'Q6(B)', revolut + '\n\n' + L(2, 7, '(B) Name and explain two insurances that a household could have, other than motor insurance.'), 15, 'business-3-17',
    'household-insurances', 7, [27], TWO, ten_five('Insurance'), [UNTIED])
principle = opt_resp([('explanation', 'Explanation', 6), ('example', 'Example', 4)])
P.pool(2, 6, 'c', '6(C)', 7, [5, 28], 2, L(2, 7, '(C) Explain two of the following principles of insurance and give one example in each case:'),
       revolut + '\n\nExplain the following two principles of insurance and give one example in each case:',
       [dict(id='utmost-good-faith', label='Utmost good faith', response=principle), dict(id='insurable-interest', label='Insurable interest', response=principle),
        dict(id='indemnity', label='Indemnity', response=principle)],
       20, 'Explain each selected principle with an example: 10 marks each (explanation 6 + example 4).', [],
       'business-3-17', 'insurance-principles-examples',
       'The paper prints three principles and asks for two. All three pairs are generated at 20 marks; each principle carries its own explanation 6 and example 4; the legacy card is the first printed pair.',
       legacy=legacy_route('bus-2024-ol-s2-q6c', ['utmost-good-faith', 'insurable-interest'], 7, [5, 28],
                           'question text lifted from the printed paper; the card becomes the first printed pair of the expanded choose-two pool.'))
for v in ['(i) Utmost good faith', '(ii) Insurable interest', '(iii) Indemnity.']:
    L(2, 7, v)
add(2, 6, 'd', 'Q6(D)', mortgage + '\n\n' + L(2, 7, '(D) Explain how a mortgage works.'), 10, 'business-3-16', 'how-a-mortgage-works',
    7, [28], 'One explanation: 10 marks (5 + 5).', [comps('Mortgage', (5, 5))])
cum(2, 6, 'e', 'Q6(E)', mortgage + '\n\n' + L(2, 7, '(E) List three factors a financial institution/fintech company will assess before granting a mortgage to a customer.'),
    (5, 5, 5), 'business-3-16', 'mortgage-assessment-factors', 7, [28],
    'Scheme examples: ' + S(28, 'Credit history') + ', capacity to repay, collateral, employment, deposit, spending habits.', noun='factors')

hr = L(2, 8, '76% would turn down jobs that do not meet flexible working needs, according to a study.',
       'Employees are demanding more than just a good wage when seeking employment. Research suggests that Human Resource Managers are looking at other ways of retaining and attracting staff.', sep='\n')
add(2, 7, 'a', 'Q7(A)', hr + '\n\n' + L(2, 8, '(A) Explain two different types of rewards (financial or non-financial), other than wages, that employers can offer employees.'),
    15, 'business-3-20', 'employee-rewards', 8, [29], TWO, ten_five('Reward'), [UNTIED])
P.pool(2, 7, 'b', '7(B)', 8, [6, 30], 2, L(2, 8, '(B) Explain any two of the following functions of a Human Resource Manager:'),
       hr + '\n\nExplain the following two functions of a Human Resource Manager:',
       [dict(id='manpower-planning', label=L(2, 8, '(i) Manpower Planning')), dict(id='training-development', label=L(2, 8, '(ii) Training and Development')),
        dict(id='performance-appraisal', label=L(2, 8, '(iii) Performance Appraisal'))],
       15, 'Explain both selected functions: 10 (7 + 3) and 5 (4 + 1).', ['The 10-mark allowance is not tied to a particular function.'],
       'business-3-20', 'hrm-functions',
       'The paper prints a closed list of three functions and asks for any two. All three pairs are generated at 15 marks with the 10/5 split unattached; the legacy card is the first printed pair.',
       legacy=legacy_route('bus-2024-ol-s2-q7b', ['manpower-planning', 'training-development'], 8, [6, 30],
                           'question text lifted from the printed paper; the card becomes the first printed pair of the expanded choose-two pool.'),
       ordered=ten_five('Function response'))
jd = L(2, 8, '(C) The Human Resource Manager must prepare a job description and a person specification before recruiting new staff.')
cum(2, 7, 'ci', 'Q7(C)(i)', hr + '\n\n' + jd + '\n' + L(2, 8, '(i) List two items in a job description.'), (5, 5), 'business-3-20', 'job-description-items',
    8, [31], 'Scheme examples: ' + S(31, 'Job Title') + ', details of the work, place of work, duties and responsibilities, salary and conditions, working hours.', noun='items')
cum(2, 7, 'cii', 'Q7(C)(ii)', hr + '\n\n' + jd + '\n' + L(2, 8, '(ii) List two items in a person specification.'), (5, 5), 'business-3-20', 'person-specification-items',
    8, [31], 'Scheme examples: ' + S(31, 'Skills') + ', qualities/characteristics, work experience, qualifications.', noun='items')
add(2, 7, 'd', 'Q7(D)', hr + '\n\n' + L(2, 8, '(D) Outline two negative impacts that technology has on employees.'), 15, 'business-3-21',
    'technology-impact-employees', 8, [31], TWO, ten_five('Impact'), [UNTIED])
add(2, 7, 'e', 'Q7(E)', hr + '\n\n' + L(2, 8, '(E) Explain the term Employee Empowerment.'), 10, 'business-2-11', 'employee-empowerment',
    8, [31], 'Explanation: 10 marks (7 + 3).', [comps('Employee empowerment', (7, 3))])

add(2, 8, 'ai', 'Q8(A)(i)', L(2, 9, '(A) Many of the products sold at Supervalu are mass-produced.', '(i) Explain the term mass production. Use an example to illustrate your answer.'),
    10, 'business-4-15', 'mass-production-explained', 9, [32], 'Explanation 6 and example 4.', [comps('Mass production', (6, 4), ['Explanation', 'Example'])])
add(2, 8, 'aii', 'Q8(A)(ii)', L(2, 9, '(A) Many of the products sold at Supervalu are mass-produced.', '(ii) Name one other production method.'),
    5, 'business-4-15', 'other-production-method', 9, [32], 'Name one method for 5 marks.', [single('Production method', 5, 'Method named')],
    ['Scheme: ' + S(32, 'Job Production') + ' or ' + S(32, 'Batch Production') + '.'])
add(2, 8, 'bi', 'Q8(B)(i)', L(2, 9, '(B) Supervalu is part of the Musgrave Group, which is an Irish food wholesaler.', '(i) Explain the term wholesaler.'),
    10, 'business-4-17', 'wholesaler-explained', 9, [32], 'Explanation: 10 marks (6 + 4).', [comps('Wholesaler', (6, 4))])
chan = add(2, 8, 'bii', 'Q8(B)(ii)', L(2, 9, '(B) Supervalu is part of the Musgrave Group, which is an Irish food wholesaler.', '(ii) Illustrate, using a diagram, a channel of distribution that includes a wholesaler.'),
           10, 'business-4-17', 'wholesaler-channel-diagram', 9, [32],
           'Manufacturer 3, wholesaler 3, then retailer 2 and consumer 2 (or a single retailer/consumer stage 4).',
           [response(1, 'Channel diagram', [('manufacturer', 'Manufacturer', 3), ('wholesaler', 'Wholesaler', 3),
                                            ('end', 'Retailer and consumer (2 + 2), or one retailer/consumer stage (4)', 4)])],
           ['The scheme draws ' + S(32, 'MANUFACTURER WHOLESALER RETAILER CONSUMER 3 3 2 2') + ', or ' + S(32, 'MANUFACTURER WHOLESALER RETAILER / CONSUMER 3 3 4') + '.'])
permit(chan, 0, [0, 3], 0)
permit(chan, 0, [0, 3], 1)
permit(chan, 0, [0, 2, 4], 2)
add(2, 8, 'c', 'Q8(C)', L(2, 9, '(C) SuperValu stocks a range of own-brand products. Explain, including an example, the term own-brand products.'), 10, 'business-4-17',
    'own-brand-products', 9, [32], 'Explanation 6 and example 4.', [comps('Own-brand products', (6, 4), ['Explanation', 'Example'])])
add(2, 8, 'd', 'Q8(D)', L(2, 9, '(D) Outline two sales promotion techniques that retailers such as SuperValu could use to increase sales.'), 15, 'business-4-17',
    'sales-promotion-techniques', 9, [33], TWO, ten_five('Technique'), [UNTIED])
add(2, 8, 'e', 'Q8(E)', L(2, 9, '(E) Outline two benefits for SuperValu of sponsoring the All-Ireland Football Championship.'), 15, 'business-4-17',
    'sponsorship-benefits', 9, [33], 'Two benefits: 8 (4 + 4) and 7 (4 + 3).', unequal('Benefit', [(4, 4), (4, 3)], None),
    ['The 8-mark allowance is not tied to a particular benefit.'])

crisp = L(2, 10, 'In 2023 Keogh’s launched a new Smoked Barbecue & Teeling Whiskey flavoured crisp.')
plant = L(2, 10, 'Crisp maker Keogh’s has announced the company will be constructing a new production facility worth €10 million in 2024 as the business continues to grow.')
add(2, 9, '-a-i', 'Q9(A)(i)', crisp + '\n\n' + L(2, 10, '(i) Outline one method of idea generation that a business like Keogh’s may use.'), 10, 'business-4-14',
    'idea-generation-method', 10, [34], 'One method: 10 marks (7 + 3).', [comps('Method', (7, 3))])
add(2, 9, '-a-ii', 'Q9(A)(ii)', crisp + '\n\n' + L(2, 10, '(ii) Explain the term prototype development.'), 5, 'business-4-14',
    'prototype-development', 10, [34], 'Explanation: 5 marks (4 + 1).', [comps('Prototype development', (4, 1))])
add(2, 9, '-b', 'Q9(B)', crisp + '\n\n' + L(2, 10, '(B) Outline two reasons why a business would conduct market research before launching a new product.'), 15, 'business-4-16',
    'market-research-reasons', 10, [35], TWO, ten_five('Reason'), [UNTIED])
add(2, 9, '-c', 'Q9(C)', crisp + '\n\n' + L(2, 10, '(C) Explain two functions of product packaging for a business like Keogh’s.'), 15, 'business-4-17',
    'packaging-functions', 10, [35], TWO, ten_five('Function'), [UNTIED])
add(2, 9, '-d', 'Q9(D)', plant + '\n\n' + L(2, 10, '(D) Outline two reasons why a business may choose to expand.'), 15, 'business-4-18',
    'reasons-to-expand', 10, [36], TWO, ten_five('Reason'), [UNTIED])
P.pool(2, 9, 'e', '9(E)', 10, [6, 36], 2, L(2, 10, '(E) Explain any two long-term sources of finance from the list below that Keogh’s may use to fund the expansion.').replace('long-term', 'long\u2010term'),  # the paper prints U+2010
       plant + '\n\nExplain the following two long-term sources of finance that Keogh’s may use to fund the expansion.',
       [dict(id='grant', label=L(2, 10, '(i) Grant')), dict(id='long-term-loan', label=L(2, 10, '(ii) Long-term Loan')),
        dict(id='share-capital', label=L(2, 10, '(iii) Share Capital'))],
       15, 'Explain both selected sources: 8 (4 + 4) and 7 (4 + 3).', ['The 8-mark allowance is not tied to a particular source.'],
       'business-3-16', 'long-term-finance-sources-list',
       'The paper prints a closed list of three sources and asks for any two. All three pairs are generated at 15 marks with the 8/7 split unattached; no earlier card existed.',
       ordered=unequal('Source response', [(4, 4), (4, 3)], None))

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
legacy = {i for i in ORIGINAL if i.startswith('bus-2024-ol-')}
covered = {c['id'] for c in P.created} | {p['legacyRoute']['id'] for p in P.pools if 'legacyRoute' in p}
assert legacy <= covered, sorted(legacy - covered)
new = sorted(c['id'] for c in P.created if c['id'] not in ORIGINAL)
assert new == ['bus-2024-ol-s2-q9-a-ii'], new

SELECTION = {
    1: 'No finite printed answer menu occurs in Section 1. True/False and public/private labels, ticks, matching rows, circled options and the word banks in Q2, Q9 and Q12 are required answer formats. Q6 splits at its two separately marked sub-parts. Support-note lists are open examples.',
    2: 'Five finite printed pools are expanded separately: Q3(C) any three of four barriers (four routes), Q4(C) two of three prohibited practices (three), Q4(E) three of four contract elements (four), Q6(C) two of three insurance principles (three) and Q7(B) any two of three HRM functions (three), each with its legacy card as the first printed route; Q9(E) any two of three long-term sources is a new three-route pool. “Surplus or a deficit” is one required determination. Sub-parts with their own published marks are separate cards. Support-note lists are open examples.',
}


def classify(fileid, page, m, w):
    if m.lower().startswith('answer') or 'any other TWO questions' in w or 'any other two questions' in w or 'any two other question' in w:
        return 'exam-navigation', 'The rubric sets how many whole questions a candidate answers. Every numbered question remains in the practice corpus as separate cards.', None
    # A raw-scan window spans neighbouring parts, so settle the matched word's own phrase first.
    if m == 'or' and 'surplus or a deficit' in w:
        return 'required-headings', 'Section 2 Q3(A)(ii) requires a determination of surplus or deficit; it is one required answer, not a choice of task.', None
    if m == 'or' and 'financial or non' in w:
        return 'open-response', 'Section 2 Q7(A) rewards may be financial or non-financial; the candidate chooses any two and the task stays whole.', None
    if m.lower() == 'choose' and 'choose to expand' in w:
        return 'case-context', 'Section 2 Q9(D) asks why a business may choose to expand; the word describes the business, not a candidate choice of task.', None
    if m == 'or' and 'False or misleading' in w:
        return 'case-context', 'Wording inside printed option (i) of Section 2 Q4(C); the pool itself is classified separately.', None
    if fileid == 'LC033GLP033EV' and 'any three of the following barriers' in w:
        return 'finite-pool', 'Section 2 Q3(C) asks for any three of four printed barriers; all four selections are generated at 20 marks.', 'bus-2024-ol-s2-q3c'
    if fileid == 'LC033GLP033EV' and 'two of the following practices' in w:
        return 'finite-pool', 'Section 2 Q4(C) asks for two of three printed practices; all three pairs are generated at 15 marks.', 'bus-2024-ol-s2-q4c'
    if fileid == 'LC033GLP033EV' and 'three of the following elements' in w:
        return 'finite-pool', 'Section 2 Q4(E) asks for three of four printed contract elements; all four selections are generated at 20 marks.', 'bus-2024-ol-s2-q4e'
    if fileid == 'LC033GLP033EV' and 'two of the following principles' in w:
        return 'finite-pool', 'Section 2 Q6(C) asks for two of three printed insurance principles; all three pairs are generated at 20 marks.', 'bus-2024-ol-s2-q6c'
    if fileid == 'LC033GLP033EV' and 'any two of the following functions' in w:
        return 'finite-pool', 'Section 2 Q7(B) asks for any two of three printed HRM functions; all three pairs are generated at 15 marks.', 'bus-2024-ol-s2-q7b'
    if fileid == 'LC033GLP033EV' and 'any two long' in w:
        return 'finite-pool', 'Section 2 Q9(E) asks for any two of three printed long-term sources; all three pairs are generated at 15 marks.', 'bus-2024-ol-s2-q9e'
    if 'surplus or a deficit' in w:
        return 'required-headings', 'Section 2 Q3(A)(ii) requires a determination of surplus or deficit; it is one required answer, not a choice of task.', None
    if 'False or misleading' in w:
        return 'case-context', 'Wording inside printed option (i) of Section 2 Q4(C); the pool itself is classified separately.', None
    if 'financial or non' in w:
        return 'open-response', 'Section 2 Q7(A) rewards may be financial or non-financial; the candidate chooses any two and the task stays whole.', None
    if 'choose to expand' in w:
        return 'case-context', 'Section 2 Q9(D) asks why a business may choose to expand; the word describes the business, not a candidate choice of task.', None
    if 'TRUE or FALSE' in w or 'True or False' in w:
        return 'required-headings', 'True/False are answer labels for each of the four required statements in Section 1 Q7, not optional tasks.', None
    if 'Public Limited Company or a Private' in w or 'public or private' in w or 'Public or Private' in w:
        return 'required-headings', 'Public/private are answer labels for each of the three required statements in Section 1 Q14.', None
    if 'events or emergencies' in w:
        return 'case-context', 'Wording inside explanation F of Section 1 Q15; all five terms require a match.', None
    if 'Choose the appropriate terms' in w:
        return 'required-headings', 'Section 1 Q2 is a word-bank completion: both blanks are required and the printed terms are the answer options, not optional tasks.', None
    assert (fileid, page) in {('LC033GLP032EV', 2), ('LC033GLP032EV', 9), ('LC033GLP032EV', 36), ('LC033GLP033EV', 1), ('LC033GLP033EV', 2), ('LC033GLP033EV', 12)}, (fileid, page, w)
    return 'exam-navigation', 'Cover instructions, pen/pencil instructions, answerbook supplies, the question-choice rubric or copyright boilerplate. They do not create alternative task routes.', None


n = P.write([(1, range(1, 16)), (2, range(1, 10))], SELECTION, classify,
            'Every part of {year} Ordinary Section {section} Question {q} was visually checked against its SEC booklet, allocation summary and support notes. Booklet-specific p1/p2 identities keep the short and long question numbering apart.')
print(f'Reviewed {len(P.created)} 2024 Ordinary base tasks and {len(P.pools)} route pools; classified {n} raw selection matches.')
