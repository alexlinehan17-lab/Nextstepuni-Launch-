"""Review the 2025 Ordinary English paper (Section 1 and Section 2).

Sixty-four legacy IDs keep their ID and total with correction records. Four
legacy cards become the first printed route of their finite pools; Section 1
Q9, Section 2 Q8(E) and the Q9(E) pool are new.
"""
from bus_lib import Paper, ORIGINAL, comps, points, seq, unequal, single, ten_five, response

T = {(1, q): 4 for q in range(1, 16)}
T.update({(2, 1): 5, (2, 2): 5, (2, 3): 5, (2, 4): 6, (2, 5): 6, (2, 6): 6, (2, 7): 7, (2, 8): 7, (2, 9): 7})
P = Paper(2025, 'ordinary', {1: 'LC033GLP032EV', 2: 'LC033GLP033EV'}, 'LC033GLP000EV', T)
L, S, add, cum = P.lift, P.scheme, P.add, P.cumulative
TWO = 'Two points are required: 10 (7 + 3) and 5 (4 + 1).'
UNTIED = 'The 10-mark allowance is not tied to a particular point.'


def fixed(label, entries):
    """Named entries that are each right or wrong (no partial marks)."""
    r = response(1, label, [(f'entry-{k}', name, m) for k, (name, m) in enumerate(entries, 1)])
    for a in r['allocations']:
        a['permittedMarks'] = [0, a['maxMarks']]
    return r


def legacy_route(cid, selected, page, schemes, note):
    legacy = ORIGINAL[cid]
    return dict(id=cid, selectedOptionIds=selected, correction=dict(
        originalQuestionText=legacy['questionText'], originalTotalMarks=legacy['totalMarks'],
        reason=f"Visually verified paper page {page} and scheme PDF pages {', '.join(map(str, schemes))}: {note} "
               'Retain the existing card ID and total marks for saved progress.'))


def opt_resp(parts):
    return dict(allocations=[dict(id=k, label=l, maxMarks=m, permittedMarks=list(range(m + 1))) for k, l, m in parts])


# ---------------------------------------------------------------- Section 1
add(1, 1, '', 'Q1', L(1, 3, 'What do the following letters stand for? Write each answer in the space provided.', 'EGM', 'LEO', 'GDP'), 10,
    'business-5-15', 'abbreviations-egm-leo-gdp', 3, [8], 'Each term carries its own marks: 4 (2 + 1 + 1), 3 (1 + 1 + 1) and 3 (1 + 1 + 1).',
    [comps('EGM (first term)', (4,), ['Term written in full'], 1), comps('LEO (second term)', (3,), ['Term written in full'], 2),
     comps('GDP (third term)', (3,), ['Term written in full'], 3)],
    ['Answer key: EGM ' + S(8, 'Extraordinary General Meeting') + '; LEO ' + S(8, 'Local Enterprise Offices') + '; GDP '
     + S(8, 'Gross Domestic Product') + '. Each word earns its share of the term’s marks.'],
    extra=['business-2-12', 'business-5-16'])
cum(1, 2, '', 'Q2', L(1, 3, 'Complete the missing factors of production.') + '\n' + L(1, 3, '1. Land', 'Factors of Production', sep='; ')
    + '; 2, 3 and 4 are blank.', (4, 3, 3), 'business-1-5', 'factors-of-production-missing', 3, [8],
    'Answer key: ' + S(8, '2. Labour 3. Capital 4. Enterprise') + ' (scheme page 8).', extra=['business-5-13'])
cum(1, 3, '', 'Q3', L(1, 3, 'Write the word TRUE or FALSE after each of the following statements.',
                      '(i) Safety/security needs relate to the need for food and shelter.',
                      '(ii) Esteem needs relate to being successful and achieving a high status.',
                      '(iii) Maslow believed that when one need is satisfied, the next one becomes the main motivator.',
                      '(iv) McGregor’s Theory Y managers believe that most workers dislike work.'),
    (3, 3, 2, 2), 'business-2-11', 'maslow-mcgregor-true-false', 3, [8], 'Answer key: (i) False; (ii) True; (iii) True; (iv) False (scheme page 8).')
cum(1, 4, '', 'Q4', L(1, 4, 'Complete the break-even chart below by placing the following labels in the correct position on the chart:',
                      'Fixed Costs (FC) Total Revenue (TR) Break-Even Point (BEP) Total Costs (TC)', 'Break-Even Chart for Rodgers Ltd')
    + '\nSales € m (0 to 1.2) against Output in Units (400 to 2,400). Box A marks the point where two lines cross; B is at the end of the steepest '
      'line, which starts at 0; C is at the end of the line that starts at 0.2; D is at the end of the horizontal line at 0.2.',
    (3, 3, 2, 2), 'business-3-19', 'break-even-chart-labels', 4, [8],
    'Answer key: A ' + S(8, 'Break-Even Point (BEP)') + '; B ' + S(8, 'Total Revenue (TR)') + '; C ' + S(8, 'Total Cost (TC)') + '; D '
    + S(8, 'Fixed Cost (FC)') + '.', noun='labels')
add(1, 5, '', 'Q5', L(1, 4, 'Outline two benefits of teamwork to an organisation.'), 10, 'business-3-20', 'teamwork-benefits', 4, [9],
    'Outline two benefits at 5 marks each (3 + 2).', points('Benefit', 2, (3, 2)),
    ['Scheme examples include ' + S(9, 'Improve decision making') + ', ' + S(9, 'Better staff morale') + ' and ' + S(9, 'Workload is shared') + '.'])
cum(1, 6, '', 'Q6', L(1, 5, 'Indicate by placing a tick (✓) in the correct box, the method of production that each statement best describes.')
    + '\nJob / Batch / Mass\n' + L(1, 5, '(i) Produced by robots on an automated assembly line.', '(ii) Each product has a unique design.',
                                   '(iii) Produces a limited quantity of identical products.'),
    (4, 3, 3), 'business-4-15', 'production-methods-ticks', 5, [9], 'Answer key (ticks on scheme page 9): (i) Mass; (ii) Job; (iii) Batch.')
cum(1, 7, '', 'Q7', L(1, 5, 'Match the images with the most relevant term from the list below.', 'Sales Promotion Personal Selling Sponsorship')
    + '\n(i) A Republic of Ireland footballer in a jersey carrying the Sky logo.\n(ii) A Papa John’s “Two for Tuesdays, Buy 1 Get 1 Free” pizza offer.'
      '\n(iii) A handshake outside a “House for Sale – Sold” sign.',
    (4, 3, 3), 'business-4-17', 'promotion-images', 5, [9], 'Answer key: ' + S(9, '(i) Sponsorship (ii) Sales Promotion (iii) Personal Selling') + '.')
add(1, 8, '', 'Q8', L(1, 5, 'Choose the appropriate words to complete the sentence below. (Two words do not apply.)', 'Stakeholders Competitive Consumers Co-operative',
                      'A ________________________ relationship is where a business’s ___________________ work together to achieve the same objectives.'),
    10, 'business-0-12', 'co-operative-relationship-words', 5, [10], 'Each completed blank earns 5 marks.',
    seq(single('First blank', 5, 'Word chosen'), single('Second blank', 5, 'Word chosen')),
    ['Answer key: A ' + S(10, 'Co-operative') + ' relationship ... business’s ' + S(10, 'Stakeholders') + '. Competitive and Consumers are not used.'])
add(1, 9, '', 'Q9', L(1, 6, 'Complete the Matrix Structure for an organisation with two project teams.') + '\n'
    + 'Managing Director. Department row: Finance Department, Marketing Department, two blank boxes. Team A row: Finance Staff, two blank boxes, '
      'Production Staff. Second team row (team name blank): Finance Staff, a blank box, Purchasing Staff, a blank box.',
    10, 'business-2-13', 'matrix-structure-completion', 6, [10],
    'Seven entries: departments 2 + 2, Team A row 1 + 1, second team row 2 + 1 + 1.',
    seq(fixed('Department row', [('Purchasing Department', 2), ('Production Department', 2)]),
        fixed('Team A row', [('Marketing Staff', 1), ('Purchasing Staff', 1)]),
        comps('Team B row', (4,), ['Team B, Marketing Staff and Production Staff'])),
    ['Answer key (diagram on rendered scheme page 10): Purchasing Department and Production Department; Team A Marketing Staff and Purchasing Staff; '
     'Team B, with Marketing Staff and Production Staff.',
     'The second team row is marked 2 + 1 + 1. For 0, 1, 2 or 3 correct entries in that row, record 0, 2, 3 or 4 marks; the 2 is not tied to a particular box.'])
P.created[-1]['rubric']['responses'][2]['allocations'][0]['permittedMarks'] = [0, 2, 3, 4]
assert all(L(1, 6, v) for v in ['Managing Director', 'Finance Department', 'Marketing Department', 'Team A', 'Finance Staff', 'Production Staff', 'Purchasing Staff'])
add(1, 10, '', 'Q10', L(1, 6, 'Below is a copy of the Cashflow Forecast for Smith Ltd., for the first three months of 2025. Fill in the missing figures represented by the letters A, B, C and D.')
    + '\n2025: January / February / March / Total\n' + L(1, 6, 'Total Receipts (A) 115,000 110,000 120,000 345,000', 'Total Payments (B) 90,000 85,000 92,000 267,000',
                                                         'Net Cash (A-B) 25,000 25,000 B. 78,000', 'Opening Cash 20,000 A. 70,000 C.',
                                                         'Closing Cash 45,000 70,000 98,000 D.'),
    10, 'business-3-16', 'cash-flow-missing-figures', 6, [10], 'Net cash B 3; opening cash A and C 3 + 2; closing cash D 2.',
    seq(fixed('B. Net Cash, March', [('B', 3)]), comps('A and C. Opening Cash', (5,), ['A and C']), fixed('D. Closing Cash, Total', [('D', 2)])),
    ['Answer key: A ' + S(10, '45,000') + '; B ' + S(10, '28,000') + '; C ' + S(10, '20,000') + '; D ' + S(10, '98,000') + '.',
     'The opening-cash row (A and C) is marked 3 + 2: for one or two correct figures record 3 or 5 marks; the 3 is not tied to a particular box.'])
P.created[-1]['rubric']['responses'][1]['allocations'][0]['permittedMarks'] = [0, 3, 5]
cum(1, 11, '', 'Q11', L(1, 7, 'Match the explanation with the correct type of plan from the list below. One type of plan is not explained.',
                        'Tactical Plan Contingency Plan Operational Plan Strategic Plan',
                        '(i) A back-up plan to deal with unforeseen circumstances or emergencies.',
                        '(ii) A long-term plan devised by senior management to achieve the overall goal of the business.',
                        '(iii) A short-term plan for the day-to-day running of the business.'),
    (4, 3, 3), 'business-2-13', 'types-of-plan-matching', 7, [11],
    'Answer key: (i) Contingency Plan; (ii) Strategic Plan; (iii) Operational Plan. Tactical Plan is not explained (scheme page 11).')
cum(1, 12, '', 'Q12', L(1, 7, 'Circle the correct option in each of the following statements.',
                        '(i) A credit card is used to pay for goods and services. An example of a credit card would be a Public Services Card / Visa Card.',
                        '(ii) A Bank Overdraft is an example of a short term / long term source of finance.',
                        '(iii) With Hire Purchase, the buyer becomes the legal owner when the first / last instalment is paid.',
                        '(iv) An unpaid debt owed to a business is written off as a bad debt / debenture.'),
    (3, 3, 2, 2), 'business-3-16', 'finance-statements-options', 7, [11],
    'Answer key (circled on scheme page 11): (i) Visa Card; (ii) short term; (iii) last; (iv) bad debt.')
add(1, 13, '', 'Q13', L(1, 7, 'Explain the term franchising and state one example of a franchise.'), 10, 'business-4-18', 'franchising-explained',
    7, [11], 'Explanation 7 (4 + 3) and example 3.', seq(comps('Explanation', (4, 3)), single('Example', 3, 'Franchise example')),
    ['Scheme examples: ' + S(11, "McDonalds, Body Shop, Domino's Pizza, Subway, Starbucks, Spar etc.")])
cum(1, 14, '', 'Q14', L(1, 8, 'Indicate whether each of the following is an example of an Irish Visible or Invisible Export.',
                        '(i) Kerrygold butter sold in France.', '(ii) The Irish band, The Script, playing at a concert in Spain.',
                        '(iii) American fans coming to Croke Park to watch the All-Ireland Hurling Final.', '(iv) Irish beef exported to China.'),
    (3, 3, 2, 2), 'business-6-13', 'visible-invisible-exports', 8, [12], 'Answer key: (i) Visible; (ii) Invisible; (iii) Invisible; (iv) Visible (scheme page 12).')
cum(1, 15, '', 'Q15', '\n'.join([L(1, 8, 'In the following table, Column 1 is a list of business terms and Column 2 is a list of explanations.'),
                                 L(1, 8, '1. Inflation', '2. Unemployment Rate', '3. Exchange Rate', '4. Taxation', '5. Interest Rate'),
                                 L(1, 8, 'A The cost of one currency expressed in terms of another.',
                                   'B Compulsory payments made to the government from individuals and business.',
                                   'C The rise in the average price of goods and services.', 'D The cost of borrowing money.',
                                   'E Money given by the government that does not have to be repaid.',
                                   'F The percentage of the labour force that does not have a job.'),
                                 L(1, 8, 'Match the two lists by placing the letter of the correct explanation under the number of the relevant business term below. One explanation has no match.')]),
    (2, 2, 2, 2, 2), 'business-5-15', 'economic-terms-matching', 8, [12], 'Answer key: 1 C; 2 F; 3 A; 4 B; 5 D. Explanation E is unused (scheme page 12).')

# ---------------------------------------------------------------- Section 2
sogs = L(2, 2, 'Sale of Goods and Supply of Services Act 1980')
P.pool(2, 1, 'a', '1(A)', 2, [5, 13], 2, L(2, 2, 'Explain, using examples, two of the following provisions of the Sale of Goods and Supply of Services Act 1980:'),
       sogs + '\n\nExplain, using examples, the following two provisions of the Sale of Goods and Supply of Services Act 1980:',
       [dict(id='merchantable-quality', label=L(2, 2, '(i) Goods must be of merchantable quality')),
        dict(id='fit-for-purpose', label=L(2, 2, '(ii) Goods must be fit for purpose')),
        dict(id='as-described', label=L(2, 2, '(iii) Goods must be as described')),
        dict(id='conform-to-sample', label=L(2, 2, '(iv) Goods must conform to sample'))],
       15, 'Explain both selected provisions with examples: 10 (7 + 3) and 5 (4 + 1).', ['The 10-mark allowance is not tied to a particular provision.'],
       'business-0-13', 'sale-of-goods-provisions',
       'The paper prints a closed list of four provisions and asks for two. All six pairs are generated at 15 marks with the 10/5 split unattached; the legacy card is the first printed pair.',
       legacy=legacy_route('bus-2025-ol-s2-q1a', ['merchantable-quality', 'fit-for-purpose'], 2, [5, 13],
                           'question text lifted from the printed paper; the card becomes the first printed pair of the expanded choose-two pool.'),
       ordered=ten_five('Provision response'))
add(2, 1, 'b', 'Q1(B)', sogs + '\n\n' + L(2, 2, 'Outline any two forms of redress that consumers are entitled to if any of the provisions of the Sale of Goods and Supply of Services Act 1980 are broken.'),
    15, 'business-0-13', 'consumer-redress-forms', 2, [13], TWO, ten_five('Form of redress'), [UNTIED])
add(2, 1, 'c', 'Q1(C)', sogs + '\n\n' + L(2, 2, 'Describe two advantages to a consumer of taking a case to the Small Claims Court.'), 15, 'business-0-13',
    'small-claims-advantages', 2, [14], TWO, ten_five('Advantage'), [UNTIED])
oasis = L(2, 2, 'Complaints made over high price of Oasis tickets charged by Ticketmaster')
add(2, 1, 'd', 'Q1(D)', oasis + '\n\n' + L(2, 2, 'Many consumers were unhappy with how the overpricing of tickets by Ticketmaster was managed. Outline two steps (non-legislative) a consumer might take to resolve this issue?'),
    15, 'business-0-13', 'non-legislative-consumer-steps', 2, [14], TWO, ten_five('Step'), [UNTIED])
add(2, 1, 'e', 'Q1(E)', oasis + '\n\n' + L(2, 2, 'Outline two functions of the Competition and Consumer Protection Commission (CCPC).'), 15, 'business-0-13',
    'ccpc-functions', 2, [15], TWO, ten_five('Function'), [UNTIED])

wren = L(2, 3, 'Wren Urban Nest, located in central Dublin, is an innovative hotel designed for sustainability. It is powered by 100% renewable energy, eliminating fossil fuel dependency. This makes the hotel a model of eco-friendly hospitality for travellers looking to reduce their carbon footprint.')
add(2, 2, 'a', 'Q2(A)', wren + '\n\n' + L(2, 3, 'Outline one reward and one risk for Wren Urban Nest of being more environmentally friendly.'), 15, 'business-5-17',
    'environmental-reward-and-risk', 3, [16], 'One reward 10 (7 + 3) and one risk 5 (4 + 1).', [comps('Reward', (7, 3), i=1), comps('Risk', (4, 1), i=2)])
add(2, 2, 'b', 'Q2(B)', wren + '\n\n' + L(2, 3, 'Describe two benefits that Wren Urban Nest brings to the local economy.'), 15, 'business-5-16',
    'local-economy-benefits', 3, [17], TWO, ten_five('Benefit'), [UNTIED])
add(2, 2, 'ci', 'Q2(C)(i)', wren + '\n\n' + L(2, 3, '(i) Name and explain the sector of the economy in which Wren Urban Nest operates.'), 7, 'business-5-13',
    'tertiary-sector-named', 3, [17], 'Name and explain the sector: 7 (4 + 3).', [comps('Sector', (4, 3), ['Sector named', 'Sector explained'])],
    ['Answer: ' + S(17, 'Tertiary Sector') + '.'])
add(2, 2, 'cii', 'Q2(C)(ii)', wren + '\n\n' + L(2, 3, '(ii) List the other two sectors, giving an example of an occupation in each sector.'), 8, 'business-5-13',
    'other-sectors-occupations', 3, [17], 'Each sector 2 and its occupation example 2: (2 + 2) + (2 + 2).',
    points('Sector', 2, (2, 2), ['Sector named', 'Occupation example']),
    ['Answer key: ' + S(17, 'Primary Sector') + ' (' + S(17, 'Farming, fishing, forestry, mining') + ') and ' + S(17, 'Secondary Sector') + ' ('
     + S(17, 'Manufacturing and construction') + ').'])
fuel = (L(2, 3, 'Over half of the total cost of petrol and diesel goes to the government') + '\nPETROL / DIESEL\n'
        + '\n'.join(L(2, 3, row) for row in ['31.3% Excise Duty 26.6%', '18.7% VAT 18.7%', '8.5% Carbon Tax 10.2%', '1.1% Nora Levy 1.1%',
                                             '0.7% Better Energy Charge 0.7%', '39.7% Fuel Supply Costs / Other 42.7%']))
P.pool(2, 2, 'd', '2(D)', 3, [5, 18], 2, L(2, 3, 'Excise Duty, VAT and Carbon Tax are mentioned above. Explain two of these taxes.'),
       fuel + '\n\nExcise Duty, VAT and Carbon Tax are mentioned above. Explain the following two taxes.',
       [dict(id='excise-duty', label='Excise Duty'), dict(id='vat', label='VAT'), dict(id='carbon-tax', label='Carbon Tax')],
       15, 'Explain both selected taxes: 10 (7 + 3) and 5 (4 + 1).', ['The 10-mark allowance is not tied to a particular tax.'],
       'business-3-18', 'fuel-taxes-explained',
       'The paper names three taxes and asks for two. All three pairs are generated at 15 marks with the 10/5 split unattached; the legacy card is the first printed pair.',
       legacy=legacy_route('bus-2025-ol-s2-q2d', ['excise-duty', 'vat'], 3, [5, 18],
                           'question text and fuel-cost table lifted from the printed paper; the card becomes the first printed pair of the expanded choose-two pool.'),
       ordered=ten_five('Tax response'))
add(2, 2, 'e', 'Q2(E)', L(2, 3, 'The government uses the revenue from taxation to assist business in Ireland. Outline two ways in which the government helps Irish businesses.'),
    15, 'business-5-15', 'government-helps-business', 3, [18], TWO, ten_five('Way'), [UNTIED])

apple = L(2, 4, 'Multinational company Apple must pay Ireland €13 billion in unpaid corporation tax, EU’s top court rules')
add(2, 3, 'a', 'Q3(A)', apple + '\n\n' + L(2, 4, 'Outline two reasons (other than corporation tax) why a Multinational Company like Apple would locate in Ireland.'),
    15, 'business-6-15', 'mnc-location-reasons', 4, [19], TWO, ten_five('Reason'), [UNTIED])
add(2, 3, 'b', 'Q3(B)', apple + '\n\n' + L(2, 4, 'Outline one positive and one negative impact the EU’s top court ruling could have on the Irish Economy.'),
    15, 'business-6-15', 'court-ruling-impacts', 4, [20], 'One positive 10 (7 + 3) and one negative 5 (4 + 1).',
    [comps('Positive impact', (7, 3), i=1), comps('Negative impact', (4, 1), i=2)], extra=['business-5-15'])
inflation = 'Inflation rate forecast: 2022 8.1%; 2023 5.4%; 2024 3.2%; 2025 2.3%.'
add(2, 3, 'ci', 'Q3(C)(i)', inflation + '\n\n' + L(2, 4, '(i) What is the official measure of inflation in Ireland?'), 1, 'business-5-15',
    'official-inflation-measure', 4, [21], 'Name the measure for 1 mark.', [single('Measure', 1, 'Measure named')], ['Answer: ' + S(21, 'Consumer Price Index') + '.'])
add(2, 3, 'cii', 'Q3(C)(ii)', inflation + '\n\n' + L(2, 4, '(ii) Explain two effects a decrease in inflation would have on the consumer.'), 14, 'business-5-15',
    'lower-inflation-consumer-effects', 4, [21], 'Explain two effects at 7 marks each (5 + 2).', points('Effect', 2, (5, 2)))
eu50 = L(2, 4, '2023 marked the 50') + '-year anniversary of Ireland formally joining the EEC (European Economic Community), which is known today as the European Union'
cum(2, 3, 'di', 'Q3(D)(i)', eu50 + '\n\n' + L(2, 4, '(i) Name three EU countries with which Ireland trades.'), (4, 2, 1), 'business-6-14', 'eu-trading-partners',
    4, [22], 'Scheme examples: ' + S(22, 'Germany') + ', Belgium, Netherlands, France, Italy; any EU member state is accepted.', extra=['business-6-13'], noun='countries')
add(2, 3, 'dii', 'Q3(D)(ii)', eu50 + '\n\n' + L(2, 4, '(ii) Outline two benefits to Ireland of exporting to EU countries.'), 8, 'business-6-14',
    'eu-export-benefits', 4, [22], 'Outline two benefits at 4 marks each (3 + 1).', points('Benefit', 2, (3, 1)), extra=['business-6-13'])
role = opt_resp([('component-1', 'Role point 1', 10), ('component-2', 'Role point 2', 5)])
P.pool(2, 3, 'e', '3(E)', 4, [5, 23], 1, L(2, 4, 'Explain the role of one of the following EU institutions:'),
       eu50 + '\n\nExplain the role of the following EU institution:',
       [dict(id='european-parliament', label='European Parliament', response=role), dict(id='european-commission', label='European Commission', response=role),
        dict(id='council-of-the-eu', label='Council of the European Union', response=role)],
       15, 'Explain the selected institution’s role: 10 + 5.', ['The scheme allocates the explanation 10 + 5 without fixing either amount to a particular role point.'],
       'business-6-14', 'eu-institution-role',
       'The paper prints a closed list of three EU institutions and asks for one. All three routes are generated at 15 marks; the legacy card is the first printed institution.',
       legacy=legacy_route('bus-2025-ol-s2-q3e', ['european-parliament'], 4, [5, 23],
                           'question text lifted from the printed paper; the card becomes the first printed route of the expanded choose-one pool.'))
for v in ['European Parliament', 'European Commission', 'Council of the European Union', '50_year anniversary of Ireland formally', 'joining the EEC (European Economic Community), which is known today as the European Union']:
    L(2, 4, v)

inmo = L(2, 5, 'Health workers represented by the INMO vote in favour of industrial action over staff shortage')
add(2, 4, 'a', 'Q4(A)', inmo + '\n\n' + L(2, 5, 'Outline two types of industrial action available to employees involved in an industrial dispute with their employer.'),
    15, 'business-0-14', 'industrial-action-types', 5, [24], TWO, ten_five('Type'), [UNTIED])
add(2, 4, 'b', 'Q4(B)', inmo + '\n\n' + L(2, 5, 'Outline the effects industrial action would have on any two stakeholders in the health service.'),
    15, 'business-0-14', 'industrial-action-stakeholder-effects', 5, [24], TWO, ten_five('Stakeholder'), [UNTIED])
mcgrath = L(2, 5, 'On 6 January 2025, the McGrath family signed a contract with Buildings AFD Ltd to add a conservatory to their home for an agreed cost. A deposit was paid, and the project was scheduled to be completed by 1 May 2025. This was specified in the contract. However, it is now 1 June 2025, and the project is still not started.')
add(2, 4, 'ci', 'Q4(C)(i)', mcgrath + '\n\n' + L(2, 5, '(i) Explain with reference to the text above one way the McGrath family can terminate the contract.'),
    10, 'business-0-12', 'contract-termination-breach', 5, [25], 'Explain one way for 10 marks (7 + 3).', [comps('Way', (7, 3))],
    ['The scheme answer is termination on grounds of ' + S(25, 'Breach') + ': the conservatory was not completed by 1 May 2025.'])
add(2, 4, 'cii', 'Q4(C)(ii)', mcgrath + '\n\n' + L(2, 5, '(ii) Explain one other way a contract can be terminated.'), 5, 'business-0-12',
    'contract-termination-other-way', 5, [25], 'Explain one other way for 5 marks (4 + 1).', [comps('Way', (4, 1))])
wrc = L(2, 5, 'Race and sexual orientation discrimination complaints up sharply last year – WRC')
add(2, 4, 'd', 'Q4(D)', wrc + '\n\n' + L(2, 5, 'Outline two grounds, other than race or sexual orientation, on which discrimination is outlawed under the Employment Equality Acts.'),
    15, 'business-0-14', 'discrimination-grounds', 5, [25], TWO, ten_five('Ground'), [UNTIED])
add(2, 4, 'e', 'Q4(E)', wrc + '\n\n' + L(2, 5, 'Explain two functions of the Workplace Relations Commission (WRC).'), 15, 'business-0-14',
    'wrc-functions', 5, [26], TWO, ten_five('Function'), [UNTIED])

aimee = L(2, 6, 'Aimee Connolly is honoured as the Emerging Entrepreneur of the Year', 'Aimee Connolly, a makeup artist and beauty entrepreneur, founded Sculpted by Aimee in 2016. At the age of 23, she launched her own brand, driven by her desire to create products she felt were missing, all with a focus on making them more accessible.', sep='\n')
add(2, 5, 'a', 'Q5(A)', aimee + '\n\n' + L(2, 6, 'Outline one risk and one reward for Aimee of setting up her own business.'), 15, 'business-1-5',
    'entrepreneur-risk-and-reward', 6, [27], 'One risk 10 (7 + 3) and one reward 5 (4 + 1).', [comps('Risk', (7, 3), i=1), comps('Reward', (4, 1), i=2)])
add(2, 5, 'b', 'Q5(B)', aimee + '\n\n' + L(2, 6, 'Aimee turned her passion into a business opportunity. Outline two other sources of new product/business ideas.'),
    15, 'business-4-14', 'sources-of-ideas', 6, [28], TWO, ten_five('Source'), [UNTIED])
add(2, 5, 'c', 'Q5(C)', aimee + '\n\n' + L(2, 6, 'Outline three entrepreneurial characteristics/skills associated with entrepreneurs like Aimee.'), 15, 'business-1-5',
    'entrepreneurial-characteristics', 6, [29], 'Outline three at 5 marks each (4 + 1).', points('Characteristic', 3, (4, 1)))
add(2, 5, 'd', 'Q5(D)', aimee + '\n\n' + L(2, 6, 'Outline two benefits for Aimee of using social media to communicate with her customers.'), 15, 'business-2-12',
    'social-media-benefits', 6, [30], TWO, ten_five('Benefit'), [UNTIED])
add(2, 5, 'ei', 'Q5(E)(i)', aimee + '\n\n' + L(2, 6, '(i) Explain the term stock control.'), 3, 'business-2-13', 'stock-control-explained',
    6, [30], 'Explain the term for 3 marks.', [comps('Stock control', (3,), ['Term explained'])])
add(2, 5, 'eii', 'Q5(E)(ii)', aimee + '\n\n' + L(2, 6, '(ii) Outline two reasons why stock control is important to a business like Sculpted.'), 12, 'business-2-13',
    'stock-control-reasons', 6, [30], 'Outline two reasons at 6 marks each (5 + 1).', points('Reason', 2, (5, 1)))

club = L(2, 7, 'United Football Club’s AGM will take place at the Castlemore clubhouse on Friday, 9 January 2026, at 8:00 p.m.',
         'Chairperson Steven Farrell and Secretary Mary Byrne are preparing for the meeting, focusing on improving cash flow and on raising finance to build a gym.', sep='\n')
add(2, 6, 'a', 'Q6(A)', club + '\n\n' + L(2, 7, 'State two advantages of meetings as a method of communication.'), 15, 'business-2-12',
    'meeting-advantages', 7, [31], TWO, ten_five('Advantage'), [UNTIED])
add(2, 6, 'bi', 'Q6(B)(i)', club + '\n\n' + L(2, 7, '(i) Outline one duty of the Chairperson of a club.'), 10, 'business-2-12', 'chairperson-duty',
    7, [32], 'Outline one duty for 10 marks (7 + 3).', [comps('Duty', (7, 3))])
add(2, 6, 'bii', 'Q6(B)(ii)', club + '\n\n' + L(2, 7, '(ii) Outline one duty of the Secretary of a club.'), 5, 'business-2-12', 'secretary-duty',
    7, [32], 'Outline one duty for 5 marks (4 + 1).', [comps('Duty', (4, 1))])
add(2, 6, 'c', 'Q6(C)', club + '\n\n' + L(2, 7, 'Draft the Notice and Agenda of the Annual General Meeting of United Football Club. (The Agenda must contain at least five items.)'),
    15, 'business-2-12', 'agm-notice-and-agenda', 7, [33], 'Notice 4 @ 1 mark, agenda five items @ 2 marks and signature 1.',
    seq(fixed('Notice', [('United Football Club', 1), ('9 January 2026', 1), ('8.00pm', 1), ('Castlemore Clubhouse', 1)]),
        comps('Agenda', (10,), ['Agenda items']), fixed('Signed', [('Signed by the Secretary', 1)])),
    ['Scheme agenda items include ' + S(33, 'Minutes of AGM 2025') + ', Matters Arising, Chairpersons Report, Treasurers Report and ' + S(33, 'Raising finance to build a gym')
     + '. For 0 to 5 acceptable agenda items, record 0, 2, 4, 6, 8 or 10 marks.', 'The scheme signs the notice ' + S(33, 'Mary Byrne') + ', Club Secretary.'])
P.created[-1]['rubric']['responses'][1]['allocations'][0]['permittedMarks'] = [0, 2, 4, 6, 8, 10]
add(2, 6, 'd', 'Q6(D)', club + '\n\n' + L(2, 7, 'Explain two reasons why a club should prepare a Cash Flow Forecast.'), 15, 'business-3-16',
    'club-cash-flow-reasons', 7, [34], TWO, ten_five('Reason'), [UNTIED])
add(2, 6, 'e', 'Q6(E)', club + '\n\n' + L(2, 7, 'Outline two sources that United Football Club could use to finance the building of a gym.'), 15, 'business-3-16',
    'club-gym-finance-sources', 7, [34], TWO, ten_five('Source'), [UNTIED])

dexcom = L(2, 8, "Dexcom's upcoming manufacturing facility in Athenry, Co. Galway, is set to generate 1,000 new jobs. The HR Department in Dexcom provides extensive training opportunities such as induction and on-the-job training. Dexcom also offers a range of reward schemes such as benefit-in-kind, bonuses and remote work options.")
add(2, 7, 'a', 'Q7(A)', dexcom + '\n\n' + L(2, 8, 'Explain the terms induction training and on the job training.'), 15, 'business-3-20',
    'induction-and-on-the-job-training', 8, [35], 'Both required terms: induction training 10 (7 + 3) and on-the-job training 5 (4 + 1).',
    [comps('Induction training', (7, 3), i=1), comps('On-the-job training', (4, 1), i=2)])
add(2, 7, 'b', 'Q7(B)', dexcom + '\n\n' + L(2, 8, 'Explain two benefits for Dexcom of rewarding its employees.'), 15, 'business-3-20',
    'employee-reward-benefits', 8, [35], TWO, ten_five('Benefit'), [UNTIED])
david = (L(2, 8, 'David Mulroy was successful in his application to work as a Staff Industrial Engineer at Dexcom. The following is a breakdown of his earnings:')
         + '\n' + '\n'.join(L(2, 8, row) for row in ['Annual Gross Pay €46,000', 'PAYE 20% on the first €42,000 and 40% on the remainder',
                                                      'Annual Tax Credit €3,750', 'PRSI 4.1%', 'USC 3.0%']))
add(2, 7, 'c', 'Q7(C)', david + '\n\n' + L(2, 8, 'Outline any two steps in the recruitment and selection process that the Human Resource Department would have carried out before employing David Mulroy.'),
    15, 'business-3-20', 'recruitment-selection-steps', 8, [36], TWO, ten_five('Step'), [UNTIED])
add(2, 7, 'd', 'Q7(D)', david + '\n\n' + L(2, 8, 'Outline two differences between a salary and a wage.'), 15, 'business-3-20', 'salary-versus-wage',
    8, [36], TWO, ten_five('Difference'), [UNTIED])
add(2, 7, 'e', 'Q7(E)', david + '\n\n' + L(2, 8, 'Calculate David’s Annual Net Salary. Show your workings.'), 15, 'business-3-18', 'annual-net-salary',
    8, [37], 'Gross pay 1, then 2 marks for each of the seven published figures.',
    [fixed('Net salary', [('Gross Pay: €46,000', 1), ('PAYE 20% @ 42,000: €8,400', 2), ('PAYE 40% @ 4,000: €1,600', 2),
                          ('Net PAYE after the €3,750 tax credit: €6,250', 2), ('PRSI 46,000 @ 4.1%: €1,886', 2), ('USC 46,000 @ 3.0%: €1,380', 2),
                          ('Total Annual Deductions: €9,516', 2), ('Net Annual Salary: €36,484', 2)])],
    ['Scheme working: gross PAYE ' + S(37, '10,000') + ' less tax credit 3,750 = 6,250; deductions 9,516; net annual salary ' + S(37, '36,484') + '.'])

cadbury = L(2, 9, 'Cadbury is constantly coming up with new and innovative ideas and increasing its product portfolio')
add(2, 8, 'a', 'Q8(A)', cadbury + '\n\n' + L(2, 9, 'Outline two benefits to Cadbury of having a good brand name.'), 15, 'business-4-17',
    'brand-name-benefits', 9, [38], TWO, ten_five('Benefit'), [UNTIED])
add(2, 8, 'b', 'Q8(B)', cadbury + '\n\n' + L(2, 9, 'Explain two factors that a business should consider before setting the price of a product or service.'),
    15, 'business-4-17', 'pricing-factors', 9, [38], TWO, ten_five('Factor'), [UNTIED])
add(2, 8, 'ci', 'Q8(C)(i)', cadbury + '\n\n' + L(2, 9, '(i) Explain the term Target Market, with reference to Cadbury.'), 7, 'business-4-16',
    'target-market-explained', 9, [39], 'Explain with reference to Cadbury: 7 (4 + 2 + 1).', [comps('Target market', (4, 2, 1))])
cum(2, 8, 'cii', 'Q8(C)(ii)', cadbury + '\n\n' + L(2, 9, '(ii) List two advertising media that a business could use.'), (6, 2), 'business-4-17',
    'advertising-media-list', 9, [39], 'Scheme examples: ' + S(39, 'Television') + ', radio, newspapers, magazines, social media, websites/blogs, billboards and promotional displays.',
    noun='media')
add(2, 8, 'd', 'Q8(D)', cadbury + '\n\n' + L(2, 9, 'Name and explain two types of market research a business like Cadbury could have used before launching new products.'),
    15, 'business-4-16', 'market-research-types', 9, [39], TWO, ten_five('Type'), [UNTIED],
    extra=['business-4-14'])
add(2, 8, 'e', 'Q8(E)', cadbury + '\n\n' + L(2, 9, 'Using the graph paper on page 10 of the answerbook, draw and label a Product Life Cycle diagram for a product such as Cadbury’s Dairy Milk chocolate.'),
    15, 'business-4-17', 'plc-diagram', 9, [40], 'Title 1, Sales 1, Time 1, curved line 2 and the five stage labels in order at 2 marks each.',
    [fixed('Product life cycle diagram', [('Title', 1), ('Sales axis', 1), ('Time axis', 1), ('Curved line', 2), ('Introduction/Launch', 2),
                                          ('Growth', 2), ('Maturity', 2), ('Saturation', 2), ('Decline', 2)])],
    ['The scheme diagram (rendered page 40) labels the stages Introduction/Launch, Growth, Maturity, Saturation and Decline, in order, with ' + S(40, 'Labels: (in order) 5 x 2m') + '.'], new=True)
P.created[-1]['rubric']['responses'][0]['allocations'][3]['permittedMarks'] = [0, 1, 2]

ikea = L(2, 10, 'IKEA and Tesco have expanded their successful partnership in Ireland', "IKEA launches seven new 'Click and Collect' sites with Tesco, offering more convenient and affordable collection services nationwide.", sep='\n')
add(2, 9, '-a', 'Q9(A)', ikea + '\n\n' + L(2, 10, 'Outline two reasons for a business like IKEA to expand its services.'), 15, 'business-4-18',
    'reasons-to-expand-services', 10, [41], TWO, ten_five('Reason'), [UNTIED])
add(2, 9, '-b', 'Q9(B)', ikea + '\n\n' + L(2, 10, "Outline two benefits to IKEA of completing a SWOT/SCOT analysis before its 'Click and Collect' partnership with Tesco."),
    15, 'business-2-13', 'swot-benefits', 10, [41], TWO, ten_five('Benefit'), [UNTIED])
add(2, 9, '-c', 'Q9(C)', ikea + '\n\n' + L(2, 10, 'Explain two services that Enterprise Ireland provides to businesses.'), 15, 'business-5-15',
    'enterprise-ireland-services', 10, [42], TWO, ten_five('Service'), [UNTIED])
insurance = L(2, 10, 'Businesses still face costly insurance in spite of reform', 'A recent survey revealed that many businesses are struggling with rising insurance premiums. While reforms have brought some stability to motor insurance premiums for consumers, businesses are facing increased costs for public liability insurance along with higher employer PRSI costs.', sep='\n')
insurance_u = insurance + '\n(Underlined: insurance premiums, motor insurance, public liability insurance, employer PRSI.)'
term = opt_resp([('component-1', 'Component 1', 4), ('component-2', 'Component 2', 1)])
P.pool(2, 9, 'd', '9(D)', 10, [7, 42], 3, L(2, 10, 'Explain any three of the insurance terms underlined above.'),
       insurance_u + '\n\nExplain the following three insurance terms underlined above.',
       [dict(id='insurance-premiums', label='Insurance premiums', response=term), dict(id='motor-insurance', label='Motor insurance', response=term),
        dict(id='public-liability-insurance', label='Public liability insurance', response=term), dict(id='employer-prsi', label='Employer PRSI', response=term)],
       15, 'Explain each selected term at 5 marks (4 + 1).', [], 'business-3-17', 'insurance-terms-explained',
       'The extract underlines four insurance terms and asks for any three. All four selections are generated at 15 marks; the legacy card is the first three printed terms.',
       legacy=legacy_route('bus-2025-ol-s2-q9-d', ['insurance-premiums', 'motor-insurance', 'public-liability-insurance'], 10, [7, 42],
                           'question text and extract lifted from the printed paper (the legacy text was scheme residue); the card becomes the first three printed terms of the expanded choose-three pool.'))
P.pool(2, 9, 'e', '9(E)', 10, [7, 43], 2, L(2, 10, 'Explain two of these principles.'),
       insurance + '\n\n' + L(2, 10, 'Businesses must abide by the insurance principles of insurable interest, indemnity and utmost good faith.') + ' Explain the following two principles.',
       [dict(id='insurable-interest', label='Insurable interest'), dict(id='indemnity', label='Indemnity'), dict(id='utmost-good-faith', label='Utmost good faith')],
       15, 'Explain both selected principles: 10 (7 + 3) and 5 (4 + 1).', ['The 10-mark allowance is not tied to a particular principle.'],
       'business-3-17', 'insurance-principles',
       'The paper names three insurance principles and asks for two. All three pairs are generated at 15 marks with the 10/5 split unattached.',
       ordered=ten_five('Principle response'))

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
legacy = {i for i in ORIGINAL if i.startswith('bus-2025-ol-')}
covered = {c['id'] for c in P.created} | {p['legacyRoute']['id'] for p in P.pools if 'legacyRoute' in p}
assert legacy <= covered, sorted(legacy - covered)
new = sorted(c['id'] for c in P.created if c['id'] not in ORIGINAL)
assert new == ['bus-2025-ol-s1-q9', 'bus-2025-ol-s2-q8e'], new

SELECTION = {
    1: 'No finite printed answer menu occurs in Section 1. True/False labels, ticks, matching rows, circled options, the image matching in Q7 and the shared word bank in Q8 are required answer formats. Support-note lists are open examples.',
    2: 'Four finite printed pools are expanded separately: Q1(A) two of four Sale of Goods provisions (six routes), Q2(D) two of three named taxes (three routes), Q3(E) one of three EU institutions (three routes) and Q9(D) any three of four underlined insurance terms (four routes); each keeps its legacy card as the first printed route. Q9(E) two of three insurance principles is a new three-route pool. “Any two” redress forms, stakeholders and recruitment steps are open choices. Sub-parts with their own published marks are separate cards. Support-note lists are open examples.',
}


def classify(fileid, page, m, w):
    if m.lower().startswith('answer') or 'any other two questions' in w or 'any other TWO questions' in w:
        return 'exam-navigation', 'The rubric sets how many whole questions a candidate answers. Every numbered question remains in the practice corpus as separate cards.', None
    if fileid == 'LC033GLP033EV' and 'two of the following provisions' in w:
        return 'finite-pool', 'Section 2 Q1(A) asks for two of four printed provisions; all six pairs are generated at 15 marks.', 'bus-2025-ol-s2-q1a'
    if fileid == 'LC033GLP033EV' and 'two of these taxes' in w:
        return 'finite-pool', 'Section 2 Q2(D) asks for two of the three named taxes; all three pairs are generated at 15 marks.', 'bus-2025-ol-s2-q2d'
    if fileid == 'LC033GLP033EV' and 'one of the following EU institutions' in w:
        return 'finite-pool', 'Section 2 Q3(E) asks for one of three printed EU institutions; all three routes are generated at 15 marks.', 'bus-2025-ol-s2-q3e'
    if fileid == 'LC033GLP033EV' and 'any three of the insurance terms' in w:
        return 'finite-pool', 'Section 2 Q9(D) asks for any three of four underlined insurance terms; all four selections are generated at 15 marks.', 'bus-2025-ol-s2-q9d'
    if fileid == 'LC033GLP033EV' and 'two of these principles' in w:
        return 'finite-pool', 'Section 2 Q9(E) asks for two of three named insurance principles; all three pairs are generated at 15 marks.', 'bus-2025-ol-s2-q9e'
    if 'any two forms of redress' in w or 'any two stakeholders' in w or 'any two steps' in w:
        return 'open-response', 'The forms, stakeholders or steps are not printed as a closed list; the candidate chooses any two and the task stays whole.', None
    if 'TRUE or FALSE' in w or 'True or False' in w:
        return 'required-headings', 'True/False are answer labels for each of the four required statements in Section 1 Q3, not optional tasks.', None
    if 'Visible or Invisible' in w:
        return 'required-headings', 'Visible/Invisible are answer labels for each of the four required exports in Section 1 Q14.', None
    if 'Choose the appropriate words' in w:
        return 'required-headings', 'Section 1 Q8 is a word-bank completion: both blanks are required and the printed words are the answer options, not optional tasks.', None
    if 'circumstances or emergencies' in w:
        return 'case-context', 'Wording inside explanation (i) of Section 1 Q11; all three explanations require a matching plan.', None
    if 'race or sexual orientation' in w:
        return 'case-context', 'Section 2 Q4(D) excludes race and sexual orientation from the grounds asked for; it creates no choice of task.', None
    if 'one of the fastest' in w:
        return 'case-context', 'Section 2 Q5 extract describes Sculpted by Aimee as one of the fastest-growing brands; it is case context.', None
    if 'product or service' in w:
        return 'case-context', 'Section 2 Q8(B) asks about pricing a product or service; the phrase describes what is priced, not a choice of task.', None
    if 'page 10 of the answerbook' in w:
        return 'exam-navigation', 'Section 2 Q8(E) points to the graph paper on page 10 of the answerbook; it creates no choice of task.', None
    assert (fileid, page) in {('LC033GLP032EV', 2), ('LC033GLP032EV', 9), ('LC033GLP032EV', 36), ('LC033GLP033EV', 12)}, (fileid, page, w)
    return 'exam-navigation', 'Cover instructions, pen/pencil instructions, answerbook supplies or copyright boilerplate. They do not create alternative task routes.', None


n = P.write([(1, range(1, 16)), (2, range(1, 10))], SELECTION, classify,
            'Every part of {year} Ordinary Section {section} Question {q} was visually checked against its SEC booklet, allocation summary and support notes. Booklet-specific p1/p2 identities keep the short and long question numbering apart.')
print(f'Reviewed {len(P.created)} 2025 Ordinary base tasks and {len(P.pools)} route pools; classified {n} raw selection matches.')
