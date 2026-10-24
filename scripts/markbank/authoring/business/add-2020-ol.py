"""Review the 2020 Ordinary English paper (Section 1 and Section 2).

2020: answer ten of fifteen short questions at 10 marks and four of eight
long questions at 75. No Ordinary card existed for 2020, so every card is new.
The one printed choice, Section 2 Q5(A)(ii) (explain one of two named
insurance principles), is marked alike under one topic and is ONE card.
"""
from bus_lib import (Paper, ORIGINAL, comps, points, seq, unequal, single, response, fixed, permit)

T = {(1, q): 4 for q in range(1, 16)}
T.update({(2, 1): 5, (2, 2): 5, (2, 3): 5, (2, 4): 6, (2, 5): 6, (2, 6): 6, (2, 7): 7, (2, 8): 7})
P = Paper(2020, 'ordinary', {1: 'LC033GLP032EV', 2: 'LC033GLP033EV'}, 'LC033GLP000EV', T)
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
ab = add(1, 1, '', 'Q1', L(1, 3, 'What do the following letters stand for? Write each answer in the space provided.', 'SWOT', 'CEO', 'PLC'), 10,
         'business-2-13', 'abbreviations-swot-ceo-plc', 3, [8], 'The first term earns 4 (1 + 1 + 1 + 1); the second and third 3 each (1 + 1 + 1).',
         [comps('SWOT (first term)', (4,), ['Words written in full'], 1), comps('CEO (second term)', (3,), ['Words written in full'], 2),
          comps('PLC (third term)', (3,), ['Words written in full'], 3)],
         ['Answer key: SWOT ' + S(8, 'Strengths Weaknesses Opportunities Threats') + '; CEO ' + S(8, 'Chief Executive Officer') + '; PLC '
          + S(8, 'Public Limited Company') + '.'], extra=['business-5-14'])
cum(1, 2, '', 'Q2', L(1, 3, 'Identify the production option most appropriate to each of the products shown below.')
    + '\n(Photographs: (i) a tray of cupcakes; (ii) a suit advertised as custom-made; (iii) bottles on a production line.)',
    (4, 3, 3), 'business-4-15', 'production-options-images', 3, [8], 'Answer key (scheme page 8): ' + S(8, '(i) Batch (ii) Job (iii) Mass') + '.',
    noun='products')
add(1, 3, '', 'Q3', L(1, 3, 'Explain the difference between an Entrepreneur and an Intrapreneur.', 'An Entrepreneur is', 'An Intrapreneur is'), 10,
    'business-1-5', 'entrepreneur-versus-intrapreneur', 3, [8], 'Each explanation earns 5 marks (3 + 2).',
    [comps('Entrepreneur', (3, 2), i=1), comps('Intrapreneur', (3, 2), i=2)],
    ['Scheme: ' + S(8, 'An Entrepreneur uses initiative, spots a gap/opportunity, and takes a risk by setting up a new business.') + ' '
     + S(8, 'An Intrapreneur is an employee within a business who sees an opportunity to create new products/services in the business') + ' ...'])
cum(1, 4, '', 'Q4', L(1, 4, 'Complete the table below, linking the European Union institutions listed with their function.',
                      'EUROPEAN PARLIAMENT EUROPEAN COMMISSION EUROPEAN COURT OF AUDITORS')
    + '\nFunction: ' + L(1, 4, 'Drafts all European laws', 'Ensures the EU Budget is spent correctly', 'Represents all EU citizens and debates all EU laws', sep=' | '),
    (4, 3, 3), 'business-6-14', 'eu-institution-functions', 4, [9],
    'Answer key (scheme page 9): drafts all laws ' + S(9, 'European Commission') + '; the budget ' + S(9, 'European Court of Auditors')
    + '; represents citizens ' + S(9, 'European Parliament') + '.', noun='institutions')
cum(1, 5, '', 'Q5', L(1, 4, 'Indicate whether each of the following is an example of Desk Research or Field Research by writing Desk or Field after each of the following statements.',
                      'Conducting a focus group where a group of consumers is brought together to discuss a product.', 'Observing consumer behaviour in a marketplace.',
                      'Researching magazines and newspapers.', 'Conducting a survey where a business interviews a consumer directly.',
                      'Collecting information from Government publications such as those prepared by the Central Statistics Office (CSO).'),
    (2, 2, 2, 2, 2), 'business-4-16', 'desk-or-field-research', 4, [9], 'Answer key (scheme page 9): Field; Field; Desk; Field; Desk.')
cum(1, 6, '', 'Q6', L(1, 4, 'Circle the correct option in each of the following statements.',
                      '(i) Inflation refers to an increase / a decrease in the general level of prices from one year to the next.',
                      '(ii) A rise in the employment rate results in an increase / a decrease in income tax received by the government.',
                      '(iii) Lower interest rates mean the cost of borrowing is cheaper / more expensive.',
                      '(iv) If the euro (€) increases in value relative to the US Dollar ($), Irish products become cheaper / more expensive in the USA.'),
    (3, 3, 2, 2), 'business-5-15', 'economic-variables-options', 4, [9],
    'Answer key (circled on scheme page 9): (i) an increase; (ii) an increase; (iii) cheaper; (iv) more expensive.')
cum(1, 7, '', 'Q7', L(1, 5, 'Indicate by placing a tick (✓) in the correct box, the pricing strategy to which each statement relates.')
    + '\nPremium Pricing / Price Skimming / Discriminatory Pricing / Loss Leader\n'
    + L(1, 5, 'Rolex charges a high price for its watches to portray an image of high quality.',
        'Lidl sells a litre of milk to consumers for €0.60 but purchased it from its suppliers for €0.65.',
        'Spotify offers students 50% off its premium package.',
        'Apple charges a high price at the launch stage of new iPhones and reduces the price over time.'),
    (3, 3, 2, 2), 'business-4-17', 'pricing-strategy-ticks', 5, [10],
    'Answer key (ticks on scheme page 10): Rolex Premium Pricing; Lidl Loss Leader; Spotify Discriminatory Pricing; Apple Price Skimming.')
cum(1, 8, '', 'Q8', L(1, 5, 'Choose the appropriate terms to complete the sentence below. (Two terms do not apply.)', 'Strategic Alliance Merger Co-operative Takeover')
    + '\nA ______ ' + L(1, 5, 'is when one company takes control of another by buying more than 50% of its shares, while a') + ' ______ '
    + L(1, 5, 'is when two separate businesses voluntarily agree to join together permanently to form a new business.'),
    (5, 5), 'business-4-18', 'takeover-merger-word-bank', 5, [10],
    'Answer key (scheme page 10): A takeover ... a merger. Strategic Alliance and Co-operative are not used.', noun='terms')
add(1, 9, '', 'Q9', L(1, 5, 'Explain the following barriers to trade.', '(i) Tariff:', '(ii) Quota:'), 10, 'business-6-13', 'tariff-and-quota',
    5, [10], 'Each explanation earns 5 marks (3 + 2).', [comps('Tariff', (3, 2), i=1), comps('Quota', (3, 2), i=2)],
    ['Scheme: Tariff: ' + S(10, 'A tax on goods imported into a country from another country.') + ' Quota: '
     + S(10, 'A Quota is a limit to the quantity of particular goods coming into a country') + '.'])
cum(1, 10, '', 'Q10', L(1, 6, 'Complete the stages in the formation of a Team:') + '\n1. ______\n2. Storming\n3. ______\n4. ______',
    (4, 3, 3), 'business-3-20', 'team-formation-stages', 6, [10], 'Answer key (scheme page 10): ' + S(10, '1. FORMING 2. Storming 3. NORMING 4. PERFORMING') + '.',
    noun='stages')
L(1, 6, '2. Storming')
L(1, 6, 'Gross Pay 60,000', 'PAYE: (20% of €35,300) 7,060', '(40% of €24,700) 9,880', 'Tax Credits – 3,300', 'Net PAYE 13,640', 'PRSI (4% of Gross Pay) A',
  'USC (3% of Gross Pay) B', 'Total Deductions C', 'Net Annual Take Home Pay D')
pay = add(1, 11, '', 'Q11', L(1, 6, 'Fill in the four missing values labelled A, B, C, and D in the table below to calculate Paul Costigan’s net annual take home pay. Show your workings in the space provided.')
          + '\nName: Paul Costigan\nGross Pay 60,000\nDeductions\nPAYE: (20% of €35,300) 7,060\n(40% of €24,700) 9,880\n16,940\nTax Credits – 3,300\nNet PAYE 13,640\n'
          + 'PRSI (4% of Gross Pay) A\nUSC (3% of Gross Pay) B\nTotal Deductions C\nNet Annual Take Home Pay D',
          10, 'business-3-18', 'net-take-home-pay', 6, [11], 'Boxes A and B earn 3 marks each, C and D 2 each.',
          [fixed('Missing values', [('A PRSI', 3), ('B USC', 3), ('C Total deductions', 2), ('D Net annual take home pay', 2)])],
          ['Answer key (scheme page 11): ' + S(11, 'A €2,400 B €1,800 C €17,840 D €42,160') + '.'])
cum(1, 12, '', 'Q12', L(1, 7, 'Write the word TRUE or FALSE after each of the following statements.', 'A strategic plan is a long-term plan for a business.',
                        'A mission statement sets out the overall purpose of the business.',
                        'A functional structure divides a business into different geographic locations.', 'A matrix structure is a team-based structure.'),
    (3, 3, 2, 2), 'business-2-13', 'planning-and-structure-true-false', 7, [11], 'Answer key (scheme page 11): True; True; False; True.')
cum(1, 13, '', 'Q13', L(1, 7, 'Name a state agency involved in each of the following sectors.') + '\nSectors: ' + L(1, 7, 'Transport Communications Industrial Relations'),
    (4, 3, 3), 'business-5-14', 'state-agencies-by-sector', 7, [11],
    'Scheme examples (page 11): Transport ' + S(11, 'CIE Iarnród Eireann Bus Eireann Dublin Bus') + '; Communications ' + S(11, 'RTE An Post')
    + '; Industrial Relations ' + S(11, 'Workplace Relations Commission (WRC)') + '.', extra=['business-0-14'], noun='agencies')
cum(1, 14, '', 'Q14', L(1, 7, 'The development of a new product/service normally involves seven stages.',
                        'Three of these stages have been entered in the table below. The remaining stages are:',
                        'Prototype Development Idea Generation Launch Concept Development',
                        'Enter the four stages above in the correct order in the table below.')
    + '\n1. ______\n2. Product/service Screening\n3. ______\n4. Feasibility Study\n5. ______\n6. Test Marketing\n7. ______',
    (3, 3, 2, 2), 'business-4-14', 'new-product-development-order', 7, [11],
    'Answer key (scheme page 11): ' + S(11, '1. Idea Generation 2. Product/service Screening 3. Concept Development 4. Feasibility Study 5. Prototype Development 6. Test Marketing 7. Launch') + '.',
    noun='stages')
L(1, 7, '2. Product/service Screening', '4. Feasibility Study', '6. Test Marketing')
cum(1, 15, '', 'Q15', '\n'.join([L(1, 8, 'In the following table, Column 1 is a list of business terms and Column 2 is a list of explanations.'),
                                 L(1, 8, '1. Capacity to contract', '2. Consent to contract', '3. Consideration', '4. Agreement', '5. Legality of form'),
                                 L(1, 8, 'A Each party in a contract must give something of value to the other party.',
                                   'B There is clear and unconditional acceptance of an offer.',
                                   'C Both parties enter into the contract of their own free will.',
                                   'D Some contracts must be in writing in order to be legally valid.',
                                   'E Both parties intend to enter into the contract and complete it.',
                                   'F Both parties can legally enter into a contract.'),
                                 L(1, 8, 'Match the two lists by placing the letter of the correct explanation under the number of the relevant business term below. One explanation has no match.')]),
    (2, 2, 2, 2, 2), 'business-0-12', 'contract-terms-matching', 8, [12], 'Answer key (scheme page 12): 1 F; 2 C; 3 A; 4 B; 5 D. Explanation E is unused.',
    noun='matches')

# ---------------------------------------------------------------- Section 2 (75 marks each)
sofas = (L(2, 2, 'Super Sofas Free delivery on all sofas ordered in March.') + '\n'
         + L(2, 2, 'Liam saw an advertisement in his local newspaper, offering free delivery on any sofa ordered in March. He purchased a sofa from Super Sofas on 25 March 2020. However, upon delivery, Liam was charged a €70 delivery fee. He paid the fee but was not happy, so he contacted the Competition and Consumer Protection Commission (CCPC).'))
law = add(2, 1, 'a', 'Q1(A)', sofas + '\n\n' + L(2, 2, '(A) Name the law that protects Liam in this situation.'), 10, 'business-0-13', 'law-protecting-liam',
          2, [13], 'Name the law: 4 + 3 + 3.', [comps('Consumer law', (10,), ['Law named'])],
          ['Answer: ' + S(13, 'Consumer Protection Act 2007') + ' (scheme: 4 + 3 + 3).'])
permit(law, 0, [0, 4, 7, 10])
add(2, 1, 'b', 'Q1(B)', sofas + '\n\n' + L(2, 2, '(B) Outline how Super Sofas have breached Liam’s consumer rights.'), 15, 'business-0-13', 'breach-of-consumer-rights',
    2, [13], 'One reason 8 (4 + 4) and its link to the text 7 (4 + 3).',
    seq(comps('Reason: the right breached', (4, 4)), comps('Link to Liam’s case', (4, 3))),
    ['Scheme: ' + S(13, 'The provisions of the Consumer Protection Act 2007 state that false/misleading advertising, information and withholding material information is prohibited.')
     + ' ' + S(13, 'Super Sofas advertisement stated that delivery was free on any sofa ordered in March, but Liam was charged a €70 delivery fee.')])
ccpc = L(2, 2, '(C) (i) Outline one function of the Competition and Consumer Protection Commission.')
add(2, 1, 'ci', 'Q1(C)(i)', sofas + '\n\n' + ccpc, 5, 'business-0-13', 'ccpc-function', 2, [13], 'One function: 5 marks (3 + 2).',
    [comps('Function', (3, 2))], ['Scheme examples include ' + S(13, 'Enforces consumer law') + ' and promoting and protecting consumers’ interests.'])
add(2, 1, 'cii', 'Q1(C)(ii)', sofas + '\n\n' + ccpc + '\n' + L(2, 2, '(ii) List and explain one other consumer agency that assists consumers.'), 10, 'business-0-13',
    'other-consumer-agency', 2, [13], 'List and explain one agency: 10 marks (4 + 3 + 3).',
    [comps('Consumer agency', (4, 3, 3), ['Agency listed', 'Explained', 'Explained further'])],
    ['Scheme examples: ' + S(13, 'Consumers Association of Ireland') + '; Ombudsman; Small Claims Court/Procedure.'])
angela = L(2, 2, 'Angela has been employed as an engineer in a large pharmaceutical plant for three years. Recently she told her manager that she had joined a trade union. Her manager informed her that this was not acceptable to the business and terminated (ended) her contract immediately.')
add(2, 1, 'd', 'Q1(D)', 'UNFAIR DISMISSAL\n' + angela + '\n\n' + L(2, 2, '(D) Outline three reasons (other than trade union membership) for unfair dismissal.'), 15,
    'business-0-14', 'unfair-dismissal-reasons', 2, [14], 'Three reasons at 5 marks each (3 + 2).', points('Reason', 3, (3, 2)))
union_i = L(2, 2, '(E) (i) Describe two functions of a trade union.')
add(2, 1, 'ei', 'Q1(E)(i)', 'UNFAIR DISMISSAL\n' + angela + '\n\n' + union_i, 15, 'business-0-14', 'trade-union-functions', 2, [14], EIGHT,
    eight_seven('Function'), [UNTIED])
add(2, 1, 'eii', 'Q1(E)(ii)', 'UNFAIR DISMISSAL\n' + angela + '\n\n' + union_i + '\n' + L(2, 2, '(ii) Name one trade union in Ireland.'), 5, 'business-0-14',
    'trade-union-named', 2, [14], 'Name one trade union for 5 marks.', [single('Trade union', 5, 'Trade union named')],
    ['Scheme examples: ' + S(14, 'SIPTU, TUI, INMO, ASTI, INTO, Fórsa') + '.'])

farmers = (L(2, 3, 'Farmers threaten to blockade supermarket distribution centres') + '\n'
           + L(2, 3, 'Farmers protesting in Dublin have said they will blockade supermarket distribution centres in the run-up to Christmas if progress is not made on beef prices and other issues.',
               '“There will be no turkeys for Christmas”, said one farmer, as tractors began to leave the capital on Wednesday afternoon after two days of disruption near Leinster House.', sep=' ')
           + ' (irishtimes.com, November 2019)')
add(2, 2, 'a', 'Q2(A)', farmers + '\n\n' + L(2, 3, '(A) Farmers operate in the primary sector of the economy. Outline two challenges facing the primary sector in Ireland.'),
    15, 'business-5-13', 'primary-sector-challenges', 3, [15], EIGHT, eight_seven('Challenge'), [UNTIED])
add(2, 2, 'b', 'Q2(B)', farmers + '\n\n' + L(2, 3, '(B) Name and explain the two other sectors of the Irish economy.'), 15, 'business-5-13',
    'secondary-and-tertiary-sectors', 3, [15], 'Two sectors: 8 (3 + 3 + 2) and 7 (3 + 3 + 1).', unequal('Sector', [(3, 3, 2), (3, 3, 1)], ['Named', 'Explained', 'Developed']),
    ['Scheme: ' + S(15, 'Secondary Sector.') + ' and ' + S(15, 'Tertiary Sector:') + ' The 8-mark allowance is not tied to a particular sector.'])
add(2, 2, 'c', 'Q2(C)', farmers + '\n\n' + L(2, 3, '(C) (i) List and explain the four factors of production. (ii) Give one example of each factor.'), 20, 'business-1-5',
    'factors-of-production-explained', 3, [16], 'Four factors at 5 marks each: listed 2, explained 2, example 1.',
    seq(*[comps(f, (2, 2, 1), ['Listed', 'Explained', 'Example']) for f in ('Land', 'Labour', 'Capital', 'Enterprise')]),
    ['Scheme: ' + S(16, 'Land: This refers to all the natural resources used in the production process.') + ' Labour, Capital and Enterprise follow (page 16).'],
    extra=['business-5-13'])
repak = L(2, 3, '‘Plastic is the biggest environmental problem of our time’, Repak chief warns.')
add(2, 2, 'd', 'Q2(D)', repak + '\n\n' + L(2, 3, '(D) Outline two environmental responsibilities of a business.'), 15, 'business-5-17',
    'environmental-responsibilities', 3, [16], EIGHT, eight_seven('Responsibility'), [UNTIED])
add(2, 2, 'e', 'Q2(E)', repak + '\n\n' + L(2, 3, '(E) Explain one benefit to a business of meeting its social, environmental and ethical responsibilities.'), 10,
    'business-5-17', 'benefit-of-social-responsibility', 3, [16, 17], 'One benefit: 10 marks (5 + 5).', [comps('Benefit', (5, 5))])

L(2, 4, 'United Kingdom €16 bn', 'United Kingdom €20 bn', 'United States €47 bn', 'United States €14 bn', 'Rest of World €90 bn', 'Rest of World €55 bn')
trade = (L(2, 4, 'Ireland’s Trade in Goods 2019') + '\nExports: United Kingdom €16 bn; United States €47 bn; Rest of World €90 bn'
         + '\nImports: United Kingdom €20 bn; United States €14 bn; Rest of World €55 bn')
add(2, 3, 'a', 'Q3(A)', trade + '\n\n' + L(2, 4, '(A) Outline two reasons why Ireland exports goods and services.'), 15, 'business-6-13', 'reasons-ireland-exports',
    4, [17], EIGHT, eight_seven('Reason'), [UNTIED])
ex = flat(add(2, 3, 'bi', 'Q3(B)(i)', trade + '\n\n' + L(2, 4, '(B) (i) Calculate the total visible exports for Ireland in 2019. Show your workings.'), 5,
              'business-6-13', 'total-visible-exports', 4, [17], 'Each figure 1 and the total 2.',
              [response(1, 'Total visible exports', [('uk', 'UK €16bn', 1), ('us', 'US €47bn', 1), ('row', 'Rest of World €90bn', 1), ('total', 'Total €153bn', 2)])],
              ['Scheme: ' + S(17, '16bn + 47bn + 90bn = €153bn') + ' (1 + 1 + 1 + 2).']))
im = flat(add(2, 3, 'bii', 'Q3(B)(ii)', trade + '\n\n' + L(2, 4, '(ii) Calculate the total visible imports for Ireland in 2019. Show your workings.'), 5,
              'business-6-13', 'total-visible-imports', 4, [17], 'Each figure 1 and the total 2.',
              [response(1, 'Total visible imports', [('uk', 'UK €20bn', 1), ('us', 'US €14bn', 1), ('row', 'Rest of World €55bn', 1), ('total', 'Total €89bn', 2)])],
              ['Scheme: ' + S(17, '20bn + 14bn + 55bn = €89bn') + ' (1 + 1 + 1 + 2).']))
bot_i = L(2, 4, '(C) (i) Calculate the Balance of Trade for Ireland in 2019. Show your workings.')
flat(add(2, 3, 'ci', 'Q3(C)(i)', trade + '\n\n' + bot_i, 10, 'business-6-13', 'balance-of-trade-2019', 4, [17],
         'Formula 3, the two totals 2 + 2 and the balance 3.',
         [response(1, 'Balance of trade', [('formula', 'Formula: Balance of Trade = Visible Exports – Visible Imports', 3), ('exports', '€153bn', 2),
                                           ('imports', '€89bn', 2), ('answer', 'Answer: €64 billion', 3)])],
         ['Scheme: ' + S(17, 'Balance of Trade = Visible Exports – Visible Imports = €153bn – €89bn = €64 billion') + ' (3, 2 + 2, 3).']))
add(2, 3, 'cii', 'Q3(C)(ii)', trade + '\n\n' + bot_i + '\n' + L(2, 4, '(ii) State whether it is a surplus or deficit.'), 5, 'business-6-13',
    'trade-surplus-or-deficit-2019', 4, [17], 'State it for 5 marks.', [single('Surplus or deficit', 5, 'Answer stated')], ['Answer: ' + S(17, 'Surplus') + '.'])
add(2, 3, 'd', 'Q3(D)', trade + '\n\n' + L(2, 4, '(D) Explain two benefits that Irish consumers receive from international trade.'), 15, 'business-6-13',
    'consumer-benefits-of-trade', 4, [17], EIGHT, eight_seven('Benefit'), [UNTIED])
export_i = L(2, 4, '(E) (i) Outline two challenges for Irish businesses exporting outside the European Union.')
add(2, 3, 'ei', 'Q3(E)(i)', trade + '\n\n' + export_i, 15, 'business-6-13', 'challenges-exporting-outside-eu', 4, [18], EIGHT, eight_seven('Challenge'), [UNTIED])
add(2, 3, 'eii', 'Q3(E)(ii)', trade + '\n\n' + export_i + '\n' + L(2, 4, '(ii) Explain how the Irish Government benefits from Irish businesses engaging in international trade.'),
    5, 'business-6-13', 'government-benefit-from-trade', 4, [18], 'One benefit: 5 marks (3 + 2).', [comps('Benefit', (3, 2))],
    ['Scheme examples: ' + S(18, 'Increased revenue') + '; ' + S(18, 'Promotes economic growth') + '.'])

vega = (L(2, 5, 'Vegalicious') + '\n'
        + L(2, 5, 'Ciara Brady noticed an increased demand for healthy treats and in particular vegan products. She decided to give up her job in marketing and invest her savings into setting up a new business called “Vegalicious” which produces a range of vegan treats using natural ingredients.',
            'Ciara now employs a staff of eight. She pays her staff well and praises them for their efforts. She holds weekly meetings with her staff where they discuss new ideas and she consults them on her plans for the business. Ciara continuously stresses the importance of good quality control to her staff.', sep=' '))
add(2, 4, 'a', 'Q4(A)', vega + '\n\n' + L(2, 5, '(A) Outline three enterprising characteristics/skills displayed by Ciara.'), 15, 'business-1-5',
    'enterprising-characteristics-ciara', 5, [19], 'Three at 5 marks each (3 + 2).', points('Characteristic', 3, (3, 2)))
add(2, 4, 'b', 'Q4(B)', vega + '\n\n' + L(2, 5, '(B) Outline two rewards for Ciara of setting up her own business.'), 10, 'business-1-5', 'rewards-of-enterprise',
    5, [19], 'Two rewards at 5 marks each (3 + 2).', points('Reward', 2, (3, 2)))
add(2, 4, 'c', 'Q4(C)', vega + '\n\n' + L(2, 5, '(C) Outline two advantages of meetings as a method of communication.'), 15, 'business-2-12', 'meetings-advantages',
    5, [20], EIGHT, eight_seven('Advantage'), [UNTIED])
lead_i = L(2, 5, '(D) (i) Outline two benefits to Ciara of using a democratic leadership style.')
add(2, 4, 'di', 'Q4(D)(i)', vega + '\n\n' + lead_i, 12, 'business-2-11', 'democratic-leadership-benefits', 5, [20], 'Two benefits at 6 marks each (3 + 3).',
    points('Benefit', 2, (3, 3)))
cum(2, 4, 'dii', 'Q4(D)(ii)', vega + '\n\n' + lead_i + '\n' + L(2, 5, '(ii) List two other leadership styles.'), (4, 4), 'business-2-11', 'other-leadership-styles',
    5, [20], 'Scheme: ' + S(20, '• Autocratic • Laissez Faire/Free Rein').replace('• ', '').replace(' Laissez', '; Laissez') + '.', noun='styles')
add(2, 4, 'e', 'Q4(E)', vega + '\n\n' + L(2, 5, '(E) Discuss two reasons why quality control is important for Ciara’s business.'), 15, 'business-2-13',
    'quality-control-importance', 5, [20], EIGHT, eight_seven('Reason'), [UNTIED])

marco = L(2, 6, 'Marco Aliotta owns and runs a busy Italian restaurant in Cork City. Marco employs ten full-time and six part-time staff. The restaurant offers a delivery service to the local area. Marco owns the restaurant premises and two delivery vans. Recently, he has experienced some cashflow difficulties due to an increase in insurance premiums and the cost of installing a new oven in the kitchen. Marco has contacted his bank about these difficulties.')
ins_i = L(2, 6, '(A) (i) List two types of insurance you would expect Marco’s business to have.')
cum(2, 5, 'ai', 'Q5(A)(i)', marco + '\n\n' + ins_i, (5, 5), 'business-3-17', 'business-insurance-types-listed', 6, [21],
    'Scheme examples: ' + S(21, 'Buildings & Contents Insurance') + '; public liability; employers liability; motor insurance.', noun='types')
add(2, 5, 'aii', 'Q5(A)(ii)', marco + '\n\n' + ins_i + '\n' + L(2, 6, '(ii) Marco must abide by the insurance principles of Indemnity and Utmost Good Faith Explain one of these principles.'),
    10, 'business-3-17', 'insurance-principle-choice', 6, [21], 'Choose one of the two printed principles and explain it: 10 marks (5 + 5).',
    [comps('The principle you chose', (5, 5))],
    ['You choose one of the two printed principles to answer. The scheme marks every choice alike and files them under one topic, so this is one card whichever principle you choose.',
     'Indemnity (scheme PDF page 21): “' + S(21, 'A person cannot make a profit from an insurance claim.') + '”',
     'Utmost Good Faith (scheme PDF page 21): “' + S(21, 'A person must be truthful when dealing with an insurance company – they must declare all material facts when seeking insurance cover.') + '”'])
add(2, 5, 'b', 'Q5(B)', marco + '\n\n' + L(2, 6, '(B) Outline two actions Marco could take to try to reduce his insurance premium.'), 15, 'business-3-17',
    'reduce-insurance-premium', 6, [21], EIGHT, eight_seven('Action'), [UNTIED])
add(2, 5, 'c', 'Q5(C)', marco + '\n\n' + L(2, 6, '(C) Outline two benefits to Marco of preparing a cash flow forecast (cash budget).'), 15, 'business-3-16',
    'cash-flow-forecast-benefits', 6, [21], EIGHT, eight_seven('Benefit'), [UNTIED])
cum(2, 5, 'd', 'Q5(D)', marco + '\n\n' + L(2, 6, '(D) List two taxes that Marco’s business must pay.'), (5, 5), 'business-3-18', 'business-taxes-listed', 6, [22],
    'Scheme examples: ' + S(22, 'Corporation Tax/Self-assessment tax') + '; Value Added Tax; motor tax; commercial rates.', noun='taxes')
add(2, 5, 'e', 'Q5(E)', marco + '\n\n' + L(2, 6, '(E) Explain two factors that a bank would consider before giving a loan to a business.'), 15, 'business-3-16',
    'bank-loan-factors', 6, [22], EIGHT, eight_seven('Factor'), [UNTIED])

L(2, 7, 'seeks ASSISTANT RETAIL MANAGER', 'The Wardrobe is an equal opportunities employer.')
advert = ('The Wardrobe seeks ASSISTANT RETAIL MANAGER\nRole:\n'
          + L(2, 7, '• Assisting the store manager with the day-to-day running of the store', '• Motivating and leading a team and providing excellent customer service',
              '• Increasing sales and controlling stock') + '\nRequirements:\n'
          + L(2, 7, '• Minimum of five years fashion retail experience', '• Excellent interpersonal and communication skills with a keen interest in fashion',
              '• Good leadership skills and the ability to work as part of a team', 'Salary negotiable, based on experience Benefit-in-Kind')
          + '\nApply online: www.thewardrobe.com before 30th November 2020\nThe Wardrobe is an equal opportunities employer.')
L(2, 7, 'Apply online: www.thewardrobe.com before 30th November 2020')
terms = L(2, 7, '(A) Explain the following terms with reference to the above advertisement:')
add(2, 6, 'ai', 'Q6(A)(i)', advert + '\n\n' + terms + '\n' + L(2, 7, '(i) Job description'), 10, 'business-3-20', 'job-description-explained', 7, [23],
    'Explanation and reference: 10 marks (4 + 3 + 3).', [comps('Job description', (4, 3, 3), ['Explanation', 'Explanation developed', 'Reference to the advertisement'])],
    ['Scheme: ' + S(23, 'This document shows details of the position/vacancy to be filled') + ' ...'])
add(2, 6, 'aii', 'Q6(A)(ii)', advert + '\n\n' + terms + '\n' + L(2, 7, '(ii) Person specification.'), 10, 'business-3-20', 'person-specification-explained', 7, [23],
    'Explanation and reference: 10 marks (4 + 3 + 3).', [comps('Person specification', (4, 3, 3), ['Explanation', 'Explanation developed', 'Reference to the advertisement'])],
    ['Scheme: ' + S(23, 'This describes the qualities that the successful candidate for the job should have.')])
add(2, 6, 'b', 'Q6(B)', advert + '\n\n' + L(2, 7, '(B) Outline two benefits of teamwork to a business such as The Wardrobe.'), 15, 'business-3-20',
    'teamwork-benefits', 7, [23], EIGHT, eight_seven('Benefit'), [UNTIED])
add(2, 6, 'c', 'Q6(C)', advert + '\n\n' + L(2, 7, '(C) Explain the term equal opportunities employer.'), 10, 'business-3-20', 'equal-opportunities-employer',
    7, [24], 'Explanation: 10 marks (4 + 3 + 3).', [comps('Equal opportunities employer', (4, 3, 3))],
    ['Scheme: ' + S(24, 'This is an employer who does not discriminate against any employee or job applicant') + ' ...'])
pay_i = L(2, 7, '(D) (i) Outline the difference between a Salary and a Wage.')
add(2, 6, 'di', 'Q6(D)(i)', advert + '\n\n' + pay_i, 10, 'business-3-20', 'salary-versus-wage', 7, [24], 'Salary 5 (3 + 2) and wage 5 (3 + 2).',
    [comps('Salary', (3, 2), i=1), comps('Wage', (3, 2), i=2)],
    ['Scheme: ' + S(24, 'A salary is a fixed regular payment made to an employee from their employer, usually expressed in the form of an annual sum.')])
add(2, 6, 'dii', 'Q6(D)(ii)', advert + '\n\n' + pay_i + '\n' + L(2, 7, '(ii) Explain, using two examples, what is meant by Benefit-in-Kind.'), 10, 'business-3-20',
    'benefit-in-kind', 7, [24], 'Explanation 6 (3 + 3) and two examples 4 (2 + 2).',
    seq(comps('Benefit-in-Kind explained', (3, 3)), comps('Examples', (2, 2), ['Example 1', 'Example 2'])),
    ['Scheme: ' + S(24, 'A Benefit in Kind (also known as a ‘perk’) is a non-financial reward given to an employee by their employer.')])
add(2, 6, 'e', 'Q6(E)', advert + '\n\n' + L(2, 7, '(E) Outline one method of selection that The Wardrobe could use to find a suitable candidate for the position of Assistant Retail Manager.'),
    10, 'business-3-20', 'selection-method', 7, [24], 'One method: 10 marks (4 + 3 + 3).', [comps('Selection method', (4, 3, 3))],
    ['Scheme examples: Interview; Aptitude/Personality Tests; Observation; Trial (page 24).'])

brands = (L(2, 8, 'Ireland’s Top Selling Brands') + '\n'
          + L(2, 8, 'While Coca-Cola continues to lead the Top 100, occupying the number one position for the 15th year in a row, Irish brands Brennan’s Bread (3rd) and Avonmore (4th) make the top five, indicating the level of loyalty that consumers have to Ireland’s biggest household names.')
          + ' (checkout.ie)\n'
          + L(2, 8, 'Businesses spend a lot of money promoting their brand to their target market, using methods such as Advertising, Sales Promotion, Public Relations and Direct Selling.'))
add(2, 7, 'a', 'Q7(A)', brands + '\n\n' + L(2, 8, '(A) Outline three advantages of branding for a business.'), 20, 'business-4-17', 'branding-advantages',
    8, [25], 'Three advantages: 7 (4 + 3), 7 (4 + 3) and 6 (3 + 3).', unequal('Advantage', [(4, 3), (4, 3), (3, 3)], None),
    ['The 7/7/6 sequence prices the three advantages, not particular advantages.'])
add(2, 7, 'b', 'Q7(B)', brands + '\n\n' + L(2, 8, '(B) Explain, using an example, the term target market.'), 10, 'business-4-16', 'target-market-example',
    8, [25], 'Explanation and example: 10 marks (4 + 3 + 3).', [comps('Target market', (4, 3, 3), ['Explanation', 'Explanation developed', 'Example'])],
    ['Scheme: ' + S(25, 'A target market is the group of people at whom a particular product or service is aimed.')])
media_i = L(2, 8, '(C) (i) List two advertising media that a business could use.')
cum(2, 7, 'ci', 'Q7(C)(i)', brands + '\n\n' + media_i, (5, 5), 'business-4-17', 'advertising-media-listed', 8, [25],
    'Scheme examples: TV; Radio; Newspapers/magazines; Internet/Social media; Billboards; Direct mail (page 25).', noun='media')
add(2, 7, 'cii', 'Q7(C)(ii)', brands + '\n\n' + media_i + '\n' + L(2, 8, '(ii) Outline two factors a business would consider before deciding which advertising media to use.'),
    10, 'business-4-17', 'advertising-media-factors', 8, [25], 'Two factors at 5 marks each (3 + 2).', points('Factor', 2, (3, 2)))
pr_i = L(2, 8, '(D) (i) Explain what is meant by Public Relations (PR).')
add(2, 7, 'di', 'Q7(D)(i)', brands + '\n\n' + pr_i, 8, 'business-4-17', 'public-relations-meaning', 8, [26], 'Explanation: 8 marks (4 + 4).',
    [comps('Public Relations', (4, 4))], ['Scheme: ' + S(26, 'Public Relations (PR) is a method used by business/people/ organisations to create goodwill towards the organisation')])
add(2, 7, 'dii', 'Q7(D)(ii)', brands + '\n\n' + pr_i + '\n' + L(2, 8, '(ii) Outline one benefit to a business of using Public Relations (PR) as a method of promotion.'),
    7, 'business-4-17', 'public-relations-benefit', 8, [26], 'One benefit: 7 marks (4 + 3).', [comps('Benefit', (4, 3))])
cum(2, 7, 'e', 'Q7(E)', brands + '\n\n' + L(2, 8, '(E) Name two suitable types of Sales Promotion a business could use to boost sales.'), (5, 5), 'business-4-17',
    'sales-promotion-types', 8, [26], 'Scheme examples: Buy one, get one free; Competitions; Loyalty cards; Free samples; Discounts; Point of sale displays (page 26).',
    noun='types')

green = (L(2, 9, 'LOCAL BUSINESS EXPANDING TO EUROPE') + '\n'
         + L(2, 9, 'Simply Green, an eco-friendly hygiene product manufacturer based in Oakfield, has announced its intention to expand into the European market in September 2020.',
             'Simply Green has received grant aid from the Local Enterprise Office (LEO) as a result of its impressive business plan submitted to Meath LEO.',
             'Simply Green intends to invest heavily in new technology and hopes to access the vast European market.', sep=' '))
add(2, 8, 'a', 'Q8(A)', green + '\n\n' + L(2, 9, '(A) Outline two benefits of preparing a business plan.'), 15, 'business-4-15', 'business-plan-benefits',
    9, [27], EIGHT, eight_seven('Benefit'), [UNTIED], extra=['business-2-13'])
add(2, 8, 'b', 'Q8(B)', green + '\n\n' + L(2, 9, '(B) Outline two reasons for business expansion.'), 15, 'business-4-18', 'reasons-for-expansion',
    9, [27], EIGHT, eight_seven('Reason'), [UNTIED])
add(2, 8, 'c', 'Q8(C)', green + '\n\n' + L(2, 9, '(C) Apart from grants, outline two sources of finance to fund business expansion.'), 15, 'business-3-16',
    'expansion-finance-sources', 9, [27], EIGHT, eight_seven('Source'),
    ['Scheme sources: ' + S(27, 'Share Capital/Equity Capital') + '; Retained Earnings (Reserves); Long Term loan (Debentures).', UNTIED], extra=['business-4-18'])
add(2, 8, 'd', 'Q8(D)', green + '\n\n' + L(2, 9, '(D) Outline two advantages of information technology to a growing business.'), 10, 'business-2-12',
    'information-technology-advantages', 9, [28], 'Two advantages at 5 marks each (3 + 2).', points('Advantage', 2, (3, 2)))
research_i = L(2, 9, '(E) (i) Outline two reasons why a business would carry out market research.')
add(2, 8, 'ei', 'Q8(E)(i)', green + '\n\n' + research_i, 12, 'business-4-16', 'market-research-reasons', 9, [28], 'Two reasons at 6 marks each (3 + 3).',
    points('Reason', 2, (3, 3)))
add(2, 8, 'eii', 'Q8(E)(ii)', green + '\n\n' + research_i + '\n' + L(2, 9, '(ii) Explain one method of Market Research.'), 8, 'business-4-16',
    'market-research-method', 9, [28], 'One method: 8 marks (4 + 4).', [comps('Method', (4, 4))],
    ['Scheme: ' + S(28, 'Primary Research (Field Research)') + '; ' + S(28, 'Secondary Research (Desk Research)') + '.'])

# ---------------------------------------------------------------- checks and write-out
qn = lambda c: c['questionRef'].split(' Q')[1].split('(')[0]
for section, count, total in [('1', 15, 10), ('2', 8, 75)]:
    for q in range(1, count + 1):
        got = sum(c['totalMarks'] for c in P.created if c['section'] == section and qn(c) == str(q))
        assert got == total, (section, q, got)
assert not [i for i in ORIGINAL if i.startswith('bus-2020-ol-')]
assert not P.pools

SELECTION = {
    1: 'No finite printed answer menu occurs in Section 1 (answer ten of fifteen at 10 marks). Desk/Field and TRUE/FALSE labels, the word bank in Q8, the matching rows in Q4 and Q15, the ticks in Q7, the circled options in Q6 and the stage table in Q14 are required answer formats. Support-note lists are open examples.',
    2: 'One printed choice: Q5(A)(ii) explain one of the two named insurance principles (Indemnity, Utmost Good Faith). The scheme marks either alike under one topic, so it is one card printing both, with the scheme’s wording for each. Sub-parts with their own published marks are separate cards. Support-note lists are open examples.',
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
    if fileid == 'LC033GLP033EV' and m == 'one of' and own(w, m, 'Explain one of these principles'):
        return 'finite-choice', 'Section 2 Q5(A)(ii) asks for one of two named insurance principles. The scheme marks either alike under one topic, so one card carries both with the scheme wording for each.', 'bus-2020-ol-s2-q5aii'
    if m == 'or' and (own(w, m, 'Desk Research or Field Research') or own(w, m, 'Desk or Field')):
        return 'required-headings', 'Desk/Field are the answer labels for each of the five required statements in Section 1 Q5, not optional tasks.', None
    if m == 'or' and (own(w, m, 'TRUE or FALSE') or own(w, m, 'True or False')):
        return 'required-headings', 'TRUE/FALSE are answer labels for each of the four required statements in Section 1 Q12, not optional tasks.', None
    if m == 'Three of' and own(w, m, 'Three of these stages have been entered'):
        return 'case-context', 'Section 1 Q14 prints three of the seven stages in its table; the four remaining stages are all required.', None
    if m == 'Choose' and own(w, m, 'Choose the appropriate terms'):
        return 'required-headings', 'Section 1 Q8 is a word-bank completion: both blanks are required and the printed terms are the answer options, not optional tasks.', None
    if m == 'or' and own(w, m, 'surplus or deficit'):
        return 'required-headings', 'Section 2 Q3(C)(ii) requires a determination of surplus or deficit; it is one required answer, not a choice of task.', None
    assert (fileid, page) in {('LC033GLP032EV', 2), ('LC033GLP032EV', 9), ('LC033GLP032EV', 36), ('LC033GLP033EV', 1), ('LC033GLP033EV', 2),
                              ('LC033GLP033EV', 12)}, (fileid, page, m, w)
    return 'exam-navigation', 'Cover instructions, the question-choice rubric, pen/pencil instructions, answerbook supplies or copyright boilerplate. They do not create alternative task routes.', None


n = P.write([(1, range(1, 16)), (2, range(1, 9))], SELECTION, classify,
            'Every part of {year} Ordinary Section {section} Question {q} was visually checked against its SEC booklet, allocation summary and support notes. Booklet-specific p1/p2 identities keep the short and long question numbering apart.')
print(f'Reviewed {len(P.created)} 2020 Ordinary tasks; classified {n} raw selection matches.')
