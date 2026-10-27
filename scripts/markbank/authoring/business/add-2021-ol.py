"""Review the 2021 Ordinary English paper (Section 1 and Section 2).

2021 is the adjusted paper: answer five of fifteen short questions at 15 marks
and three of nine long questions at 75. Sixty-eight legacy IDs keep their ID
and total with correction records; Section 1 Q7, Section 2 Q9(C)(i) and
Q9(D) are new. The two printed choices (Q6(E) two of three insurance
principles, Q8(A) two of three underlined terms) are marked alike whichever
items are chosen, so each stays ONE card carrying every printed item.
"""
from bus_lib import (Paper, ORIGINAL, comps, points, seq, unequal, single, response, fixed, permit)

T = {(1, q): p for q, p in [(1, 4), (2, 4), (3, 4), (4, 4), (5, 5), (6, 5), (7, 5), (8, 5), (9, 6), (10, 6), (11, 6), (12, 6),
                             (13, 7), (14, 7), (15, 7)]}
T.update({(2, 1): 8, (2, 2): 10, (2, 3): 12, (2, 4): 14, (2, 5): 16, (2, 6): 18, (2, 7): 21, (2, 8): 23, (2, 9): 26})
P = Paper(2021, 'ordinary', {1: 'LC033GLP032EV', 2: 'LC033GLP033EV'}, 'LC033GLP000EV', T)
L, S, add, cum = P.lift, P.scheme, P.add, P.cumulative
EIGHT = 'Two points are required: 8 (4 + 4) and 7 (4 + 3).'
FIVE = 'Two points are required: 8 (5 + 3) and 7 (5 + 2).'
UNTIED = 'The 8-mark allowance is not tied to a particular point.'


def eight_seven(label):
    return unequal(label, [(4, 4), (4, 3)], None)


def five_three(label):
    return unequal(label, [(5, 3), (5, 2)], None)


# ---------------------------------------------------------------- Section 1 (15 marks each)
add(1, 1, '', 'Q1', L(1, 3, 'What do the following letters stand for? Write each answer in the space provided.', 'PIN', 'ATM', 'APR'), 15,
    'business-3-16', 'abbreviations-pin-atm-apr', 3, [], 'Each term earns 5 marks (2 + 2 + 1).',
    [comps('PIN (first term)', (5,), ['Term written in full'], 1), comps('ATM (second term)', (5,), ['Term written in full'], 2),
     comps('APR (third term)', (5,), ['Term written in full'], 3)],
    ['Answer key: PIN ' + S(4, 'PERSONAL IDENTIFICATION NUMBER') + '; ATM ' + S(4, 'AUTOMATED TELLER MACHINE') + '; APR '
     + S(4, 'ANNUAL PERCENTAGE RATE') + '.'])
cum(1, 2, '', 'Q2', L(1, 3, 'Write the word TRUE or FALSE after each of the following statements.',
                      '(i) A chairperson has a casting vote if a vote is tied at a meeting.', '(ii) A chairperson sends out the notice and agenda for all meetings.',
                      '(iii) A secretary takes notes during the meeting and writes up the minutes of the meeting.',
                      '(iv) A quorum is the minimum number of people who must be present for a meeting to take place.'),
    (4, 4, 4, 3), 'business-2-12', 'meetings-true-false', 3, [], 'Answer key (scheme page 4): (i) TRUE; (ii) FALSE; (iii) TRUE; (iv) TRUE.')
cum(1, 3, '', 'Q3', L(1, 3, 'Choose the appropriate words to complete the sentence. (One word does not apply).', 'Strategy Demographics Segmentation')
    + '\nMarket ______ ' + L(1, 3, 'involves dividing up the market using different methods such as') + ' ______'
    + L(1, 3, ', which then provides analysis of consumers based on age, gender etc. This is done to identify the brand’s target market.'),
    (8, 7), 'business-4-16', 'segmentation-word-bank', 3, [],
    'Answer key: Market ' + S(4, 'SEGMENTATION') + ' ... such as ' + S(4, 'DEMOGRAPHICS') + '. Strategy is not used.', noun='words')
cum(1, 4, '', 'Q4', L(1, 4, 'Match the product idea with the correct source of business idea from the list below:', 'Experience Competitors Market trends')
    + '\n' + L(1, 4, 'James Dyson was frustrated with his own vacuum cleaner and took it apart to try to develop his own.',
               'A Microsoft employee saw an opportunity to develop a rival product to the Sony PlayStation and developed the Xbox.',
               'Brian Lee noticed the increasing popularity of healthy food on the go and developed his chain of take-away healthy food restaurants.'),
    (5, 5, 5), 'business-4-14', 'sources-of-business-ideas-matching', 4, [],
    'Answer key (scheme page 4): James Dyson ' + S(4, 'Experience') + '; the Xbox ' + S(4, 'Competitors') + '; Brian Lee ' + S(4, 'Market Trends') + '.',
    noun='matches')
cum(1, 5, '', 'Q5', L(1, 4, 'The following steps are involved in the management activity controlling. Number the steps in the correct order, 1 – 4 (1 being the first step).')
    + '\n' + L(1, 4, 'Measure performance', 'Compare performance with standard', 'Set the standard', 'Take corrective action (if necessary)'),
    (4, 4, 4, 3), 'business-2-13', 'controlling-steps-order', 4, [],
    'Answer key (scheme page 5): Set the standard 1; Measure performance 2; Compare performance with standard 3; Take corrective action 4.', noun='steps')
dismiss = add(1, 6, '', 'Q6', L(1, 4, 'List two reasons for fair dismissal under the Unfair Dismissals Acts, 1977-2015:'), 15, 'business-0-14',
              'fair-dismissal-reasons', 4, [], 'Two reasons: 8 and 7. Examples alone earn 4 each.',
              seq(comps('First reason', (8,), ['Reason for fair dismissal']), comps('Second reason', (7,), ['Reason for fair dismissal'])),
              ['Scheme reasons (page 5): ' + S(5, 'Incapability of employee to carry out assigned duties') + '; '
               + S(5, 'Incompetence of employee – poor work performance') + '; ' + S(5, 'Qualifications – misrepresentation by employee') + '; '
               + S(5, 'Misconduct / improper behaviour by employee') + '; Redundancy.',
               'The scheme prints 8 and 7 for the two reasons and “' + S(5, '(If only examples given, allow 4m each)') + '”.'])
permit(dismiss, 0, [0, 4, 8])
permit(dismiss, 1, [0, 4, 7])
cum(1, 7, '', 'Q7', L(1, 5, 'Insert the correct EU institution below: One institution is not explained.')
    + '\n' + L(1, 5, 'European Commission', 'The Court of Justice of the European Union', 'The European Court of Auditors', 'EU Parliament')
    + '\n' + L(1, 5, 'Members elected every 5 years by EU citizens', 'Each member appointed by the Government of each member state',
               'Responsible for ensuring the EU budget is spent correctly'),
    (5, 5, 5), 'business-6-14', 'eu-institutions-matching', 5, [],
    'Answer key (scheme page 5): members elected every 5 years ' + S(5, 'EU PARLIAMENT') + '; each member appointed by the Government '
    + S(5, 'EUROPEAN COMMISSION') + '; the EU budget ' + S(5, 'THE EUROPEAN COURT OF AUDITORS') + '. The Court of Justice is not explained.',
    noun='institutions')
L(1, 5, 'Net PAYE A', 'Total Deductions: C', 'Net Annual Take-home Pay D', '-Tax Credit 7,000 - 3,300')
pay = add(1, 8, '', 'Q8', L(1, 5, 'Calculate Alison Chamber’s net annual take home pay from the following details. Show your workings.')
          + '\nName: Alison Chambers\n' + L(1, 5, 'Gross Pay 35,000', 'Deductions:') + '\nPAYE: (20% of €35,000) 7,000\n-Tax Credit - 3,300\nNet PAYE A\n'
          + L(1, 5, 'PRSI: (4% of €35,000) 1,400') + '\nUSC: (3% of €35,000) B\nTotal Deductions: C\nNet Annual Take-home Pay D',
          15, 'business-3-18', 'net-take-home-pay', 5, [], 'Boxes A, B and C earn 4 marks each and D earns 3.',
          [fixed('Completed boxes', [('A Net PAYE', 4), ('B USC', 4), ('C Total deductions', 4), ('D Net annual take-home pay', 3)])],
          ['Answer key (scheme page 5): A ' + S(5, '3,700') + '; B ' + S(5, '1,050') + '; C ' + S(5, '6,150') + '; D ' + S(5, '28,850') + '.'])
L(1, 5, 'USC: (3% of €35,000) B')

add(1, 9, '', 'Q9', L(1, 6, 'Outline two benefits of teamwork to an organisation:'), 15, 'business-3-20', 'teamwork-benefits', 6, [],
    'Two benefits: 8 (4 + 4) and 7 (4 + 3).', eight_seven('Benefit'),
    ['Scheme examples include ' + S(6, 'Improved decision-making') + ', better staff morale, a shared workload and improved communication.', UNTIED],
    extra=['business-3-21'])
add(1, 10, '', 'Q10', L(1, 6, 'Tick (✓) the correct box to indicate which organisation provides a mediation service in an industrial relations conflict.')
    + '\n' + L(1, 6, 'Labour Court', 'Workplace Relations Commission (WRC)'), 15, 'business-0-14', 'mediation-service-tick', 6, [],
    'The correct tick earns 15.', [single('Correct box ticked', 15, 'Organisation ticked')],
    ['Answer key (scheme page 6): ' + S(6, 'Workplace Relations Commission') + '.'])
ratios = add(1, 11, '', 'Q11', L(1, 6, 'Hempstead Ltd is examining its profitability. From the information below, calculate the Gross Profit Percentage and Net Profit Percentage for 2020. Show all workings in the spaces provided.',
                                 '2020 Sales €210,000 Gross Profit €42,000 Net Profit €10,500'),
             15, 'business-3-19', 'gross-and-net-profit-percentages', 6, [],
             '(i) Gross profit percentage 8: answer 3 and workings 3 + 2. (ii) Net profit percentage 7: answer 3 and workings 2 + 2.',
             [response(1, 'Gross profit percentage', [('answer', 'Answer: 20%', 3), ('numerator', 'Workings: €42,000 on top', 3), ('denominator', 'Workings: €210,000 below', 2)]),
              response(2, 'Net profit percentage', [('answer', 'Answer: 5%', 3), ('numerator', 'Workings: €10,500 on top', 2), ('denominator', 'Workings: €210,000 below', 2)])],
             ['Scheme (page 6): ' + S(6, '42000 x 100 = 20%') + ' over 210,000, and ' + S(6, '10,500 x 100 = 5%') + ' over 210,000; ' + S(6, '(i) 8m (ii) 7m') + '.'])
for r in ratios['rubric']['responses']:
    for a in r['allocations']:
        a['permittedMarks'] = [0, a['maxMarks']]
cum(1, 12, '', 'Q12', '\n'.join([L(1, 7, 'Column 1 is a list of business terms. Column 2 is a list of explanations for these terms. One explanation has no match.'),
                                 L(1, 7, '1 Database', '2 Cloud Computing', '3 Data Controller', '4 Data Subject', '5 PowerPoint'),
                                 L(1, 7, 'A The person in the business who decides how information is collected and used.',
                                   'B A system of remote servers, hosted by the internet, which stores and manages information.',
                                   'C A software package which allows the user to present information using sound, words and images.',
                                   'D An electronic filing system used to store large amounts of information.',
                                   'E A system which allows business to business communication without human interaction.',
                                   'F The person whose personal information is stored by a business.'),
                                 L(1, 7, 'Match the two lists by placing the letter of the correct explanation under the relevant number below.')]),
    (3, 3, 3, 3, 3), 'business-2-12', 'ict-terms-matching', 7, [], 'Answer key (scheme page 6): 1 D; 2 B; 3 A; 4 F; 5 C. Explanation E is unused.',
    noun='matches')
cum(1, 13, '', 'Q13', L(1, 7, 'Complete the missing factors of production.') + '\nFour hexagons: ' + L(1, 7, 'LABOUR CAPITAL').replace(' ', ' and ')
    + ' are printed; two are blank.', (8, 7), 'business-1-5', 'missing-factors-of-production', 7, [],
    'Answer key (scheme page 7): ' + S(7, 'LAND') + ' and ' + S(7, 'ENTERPRISE') + '.', noun='factors')
cum(1, 14, '', 'Q14', L(1, 8, 'Indicate by means of a tick (✓) whether each of the following is a strength, weakness, opportunity or threat:',
                        'Strength Weakness Opportunity Threat', 'Ryanair customers find it difficult to contact the airline.',
                        'Wetter weather has impacted on the potato crop for Keogh’s crisps.', 'A new housing development has been built near SuperValu, Loughrea.',
                        'Apple have almost $200 billion in cash reserves.'),
    (4, 4, 4, 3), 'business-2-13', 'swot-ticks', 8, [],
    'Answer key (ticks on scheme page 7): Ryanair Weakness; Keogh’s crisps Threat; SuperValu Opportunity; Apple Strength.', noun='ticks')
cum(1, 15, '', 'Q15', L(1, 8, 'Circle the correct option in each of the following statements.', '(i) TQM stands for Total / Team Quality Management.',
                        '(ii) Employee encouragement / empowerment involves employees being actively involved in the running of the business.',
                        '(iii) A Facilitator Manager delegates / dictates tasks to employees.', '(iv) Products can be designed using Computer Assisted / Aided Design.'),
    (4, 4, 4, 3), 'business-3-21', 'quality-and-empowerment-options', 8, [],
    'Answer key (circled on scheme page 7): (i) Total; (ii) empowerment; (iii) delegates; (iv) Aided.', extra=['business-2-11'])

# ---------------------------------------------------------------- Section 2 (75 marks each)
consumer = L(2, 2, 'CONSUMER LAW', 'Consumers in Ireland are protected by a number of different laws. The CCPC is responsible for ensuring all consumer laws’ are implemented by businesses and they protect consumers rights. The Sale of Goods and Supply of Services Act, 1980, outlines consumers rights and retailers’ responsibilities in relation to goods and services.')
add(2, 1, 'ai', 'Q1(A)(i)', consumer + '\n\n' + L(2, 2, '(A) (i) What do the letters CCPC stand for?'), 5, 'business-0-13', 'ccpc-letters',
    2, [], 'The four words: 2 + 1 + 1 + 1.', [comps('CCPC written in full', (5,), ['Words written in full'])],
    ['Answer: ' + S(8, 'Competition and Consumer Protection Commission') + ' (' + S(8, '2+1+1+1') + ').'])
add(2, 1, 'aii', 'Q1(A)(ii)', consumer + '\n\n' + L(2, 2, '(ii) Name the other consumer law which the CCPC enforces.'), 5, 'business-0-13',
    'other-consumer-law', 2, [], 'The Act named: 2 + 2 + 1.', [comps('Consumer law', (5,), ['Act named'])],
    ['Answer: ' + S(8, 'Consumer Protection Act 2007') + ' (' + S(8, '2+2+1') + ').'])
sog = L(2, 2, '(B) Explain, using examples, the following provisions of the Sale of Goods and Supply of Services Act, 1980:')
add(2, 1, 'bi', 'Q1(B)(i)', consumer + '\n\n' + sog + '\n' + L(2, 2, '(i) Goods must be of merchantable quality'), 7, 'business-0-13',
    'merchantable-quality', 2, [], 'Explain it, using an example: 7 marks (4 + 3).', [comps('Merchantable quality', (4, 3))],
    ['Scheme: ' + S(8, 'The goods should be of a reasonable standard, fit to be sold, considering their durability and the price paid.')])
add(2, 1, 'bii', 'Q1(B)(ii)', consumer + '\n\n' + sog + '\n' + L(2, 2, '(ii) Goods must be fit for purpose'), 7, 'business-0-13',
    'fit-for-purpose', 2, [], 'Explain it, using an example: 7 marks (4 + 3).', [comps('Fit for purpose', (4, 3))],
    ['Scheme: ' + S(8, 'Goods must be able to do what they are sold as being capable of doing and what they are designed for.')])
add(2, 1, 'biii', 'Q1(B)(iii)', consumer + '\n\n' + sog + '\n' + L(2, 2, '(iii) If a consumer purchases a faulty product who is responsible?'), 6,
    'business-0-13', 'faulty-product-responsibility', 2, [], 'Explain it, using an example: 6 marks (4 + 2).', [comps('Who is responsible', (4, 2))],
    ['Scheme: ' + S(8, 'The Retailer is responsible.') + ' ' + S(8, 'The contract exists between the retailer and the consumer.')])
add(2, 1, 'c', 'Q1(C)', consumer + '\n\n' + L(2, 2, '(C) Outline two forms of remedy/redress that consumers are entitled to if any provisions of the Sale of Goods and Supply of Services Act, 1980 are broken.'),
    15, 'business-0-13', 'remedies-redress', 2, [9], EIGHT, eight_seven('Remedy'), [UNTIED])
strike = L(2, 2, '‘Unofficial strike causes severe disruption to bus services in Limerick’ Newstalk, Oct 2020')
add(2, 1, 'd', 'Q1(D)', strike + '\n\n' + L(2, 2, '(D) Describe any two functions of a trade union.'), 15, 'business-0-14', 'trade-union-functions',
    2, [9], EIGHT, eight_seven('Function'), [UNTIED])
add(2, 1, 'e', 'Q1(E)', strike + '\n\n' + L(2, 2, '(E) Explain the process employees must engage in to hold an ‘official strike’, as set out in the Industrial Relations Act, 1990.'),
    15, 'business-0-14', 'official-strike-process', 2, [9], EIGHT, eight_seven('Step'),
    ['Scheme steps include ' + S(9, 'A secret ballot of union members must take place.') + ' and one week’s notice to the employer.',
     'The 8-mark allowance is not tied to a particular step.'])

burger = L(2, 3, 'Janet and Michael O’Donnell are considering using a franchise method to expand their business. They operate an artisan burger bar, where all food is made freshly by Michael every day. The business thrived during the last year and they can see potential in franchising the idea.')
add(2, 2, 'a', 'Q2(A)', burger + '\n\n' + L(2, 3, '(A) Explain the term franchise as a form of business ownership.'), 10, 'business-5-14',
    'franchise-explained', 3, [], 'Explanation: 10 marks (4 + 3 + 3).', [comps('Franchise', (4, 3, 3))],
    ['Scheme: ' + S(10, 'A franchise is an agreement between an original company (franchisor) and a new business (franchisee)') + ' ...'])
cum(2, 2, 'b', 'Q2(B)', burger + '\n\n' + L(2, 3, '(B) Name two other businesses in Ireland which operate as franchises.'), (5, 5), 'business-5-14',
    'franchises-named', 3, [], 'Scheme examples: ' + S(10, 'McDonalds Supermacs Burger King KFC Eason Subway') + '. ' + S(10, '(SuperValu etc. are not franchises)') + '.',
    noun='businesses')
add(2, 2, 'c', 'Q2(C)', burger + '\n\n' + L(2, 3, '(C) Outline one advantage and one disadvantage for Janet and Michael if they decide to franchise out their business.'),
    15, 'business-4-18', 'franchising-advantage-disadvantage', 3, [], 'The advantage 8 (4 + 4) and the disadvantage 7 (4 + 3).',
    seq(comps('Advantage', (4, 4)), comps('Disadvantage', (4, 3))),
    ['The scheme prints 8m (4 + 4) beside its advantages and 7m (4 + 3) beside its disadvantages, for example '
     + S(10, 'Quick method of expansion') + ' and ' + S(10, 'Damage to brand if franchise fails.')])
vat = L(2, 3, 'Hospitality industry welcomes the reduction of VAT to 9%', 'Budget 2021 saw a decrease in the VAT rate for the hospitality and tourism industries from 13.5% to 9% until December 2021.')
sector_i = L(2, 3, '(D) (i) Name the sector of the economy in which the hospitality and tourism industries operate.')
add(2, 2, 'di', 'Q2(D)(i)', vat + '\n\n' + sector_i, 5, 'business-5-13', 'tourism-sector-named', 3, [11], 'Name the sector for 5 marks.',
    [single('Sector', 5, 'Sector named')], ['Answer: ' + S(11, 'Tertiary (also known as Services sector)') + '.'])
add(2, 2, 'dii', 'Q2(D)(ii)', vat + '\n\n' + sector_i + '\n' + L(2, 3, '(ii) Explain the other two sectors of the economy and give one example of an industry in each sector.'),
    20, 'business-5-13', 'other-two-sectors', 3, [11], 'Each sector: 4 + 4 for the explanation and 2 for the example.',
    seq(comps('Primary sector', (4, 4, 2), ['Explanation', 'Explanation developed', 'Example']),
        comps('Secondary sector', (4, 4, 2), ['Explanation', 'Explanation developed', 'Example'])),
    ['Scheme: ' + S(11, 'Primary Sector') + ' and ' + S(11, 'Secondary Sector') + ', each 4 + 4 + 2; ' + S(11, '(The 2m is for the example)') + '.'])
add(2, 2, 'e', 'Q2(E)', vat + '\n\n' + L(2, 3, '(E) Outline one impact the reduction in the VAT rate will have on each of the following:', '• Tourism and hospitality industries', '• Government Current Income.'),
    15, 'business-5-15', 'vat-reduction-impacts', 3, [11], 'Tourism and hospitality 8 (5 + 3); Government Current Income 7 (5 + 2).',
    seq(comps('Impact on tourism and hospitality industries', (5, 3)), comps('Impact on Government Current Income', (5, 2))),
    ['The scheme prints 8m (5 + 3) beside ' + S(11, 'Impact on Tourism and Hospitality Industries') + ' and 7m (5 + 2) beside '
     + S(11, 'Impact on Government Current Income') + '.'], extra=['business-3-18'])

L(2, 4, 'Exports €56bn', 'Exports €52bn', 'Imports €23bn', 'Imports €53bn')
accounts = (L(2, 4, 'International Accounts Q2 2020', 'Ireland’s economic interactions with the rest of the world')
            + '\nGoods: Exports €56bn; Imports €23bn\nServices: Exports €52bn; Imports €53bn')
bop_i = L(2, 4, '(A) (i) Using the information above, calculate the Balance of Payments for Q2 2020. Show your workings.')
bop = add(2, 3, 'ai', 'Q3(A)(i)', accounts + '\n\n' + bop_i, 16, 'business-6-13', 'balance-of-payments-calculation', 4, [],
          'Formula 2, total exports 2 + 2 + 1, total imports 2 + 2 + 1 and the balance 4.',
          [response(1, 'Balance of payments', [('formula', 'Formula: Balance of Payments = Total Exports – Total Imports', 2),
                                               ('exports', 'Total exports: €56bn + €52bn = €108bn', 5),
                                               ('imports', 'Total imports: €23bn + €53bn = €76bn', 5), ('answer', 'Answer: €32bn', 4)])],
          ['Scheme (page 12): ' + S(12, 'Balance of Payments = Total Exports – Total Imports') + ' (2); total exports €56bn + €52bn = €108bn (2 + 2 + 1); '
           + 'total imports €23bn + €53bn = €76bn (2 + 2 + 1); ' + S(12, 'Balance of Payments = 108bn – 76bn = €32bn') + ' (4).'])
permit(bop, 0, [0, 2], 0)
permit(bop, 0, [0, 4], 3)
add(2, 3, 'aii', 'Q3(A)(ii)', accounts + '\n\n' + bop_i + '\n' + L(2, 4, '(ii) State whether it is a surplus or a deficit.'), 4, 'business-6-13',
    'payments-surplus-or-deficit', 4, [], 'State it for 4 marks.', [single('Surplus or deficit', 4, 'Answer stated')], ['Answer: ' + S(12, 'Surplus') + '.'])
add(2, 3, 'b', 'Q3(B)', accounts + '\n\n' + L(2, 4, '(B) Explain two reasons why international trade is important for Ireland.'), 15, 'business-6-13',
    'importance-of-international-trade', 4, [], FIVE, five_three('Reason'), [UNTIED])
brexit = L(2, 4, 'Brexit is having a major impact on Irish business. Consumers and business are now faced with tariffs when buying and selling goods. Some multinational companies, however, are relocating to Ireland because of Brexit.')
add(2, 3, 'c', 'Q3(C)', brexit + '\n\n' + L(2, 4, '(C) A tariff is used as a barrier to trade. Explain the term tariff and name one other barrier to trade.'), 15,
    'business-6-13', 'tariff-and-other-barrier', 4, [13], 'Tariff explained 10 (5 + 5) and one other barrier named 5.',
    seq(comps('Tariff', (5, 5)), single('Other barrier to trade', 5, 'Barrier named')),
    ['Scheme: ' + S(13, 'A tariff is a tax on imported goods coming into a country from a specific country.') + ' Other barriers: '
     + S(13, 'Quotas • Subsidies • Embargoes/Ban • Regulations • Import/Export Licences').replace(' •', ',') + '.'])
add(2, 3, 'd', 'Q3(D)', brexit + '\n\n' + L(2, 4, '(D) Explain the term multinational company (MNC).'), 10, 'business-6-15', 'multinational-explained',
    4, [13], 'Explanation: 10 marks (5 + 5).', [comps('Multinational company', (5, 5))],
    ['Scheme: ' + S(13, 'A multinational company is a business with headquarters in one country but company offices/locations in other countries throughout the world.')])
add(2, 3, 'e', 'Q3(E)', brexit + '\n\n' + L(2, 4, '(E) Outline two reasons why multinational companies might relocate to Ireland, following Brexit.'), 15,
    'business-6-15', 'mnc-relocation-after-brexit', 4, [13], FIVE, five_three('Reason'), [UNTIED])

debenhams = L(2, 5, 'Debenhams workers participate in a national strike outside 11 stores in Ireland Adapted from the Irish Examiner')
add(2, 4, 'a', 'Q4(A)', debenhams + '\n\n' + L(2, 5, '(A) Explain two benefits to an employee of being a member of a trade union.'), 15, 'business-0-14',
    'trade-union-membership-benefits', 5, [], EIGHT, eight_seven('Benefit'), [UNTIED])
add(2, 4, 'b', 'Q4(B)', debenhams + '\n\n' + L(2, 5, '(B) State one example of a trade union in Ireland.'), 10, 'business-0-14', 'trade-union-example',
    5, [], 'One example for 10 marks.', [single('Trade union', 10, 'Trade union named')],
    ['Scheme examples: ' + S(14, 'SIPTU, TUI, INMO, ASTI, INTO, Fórsa, NUJ') + '.'])
add(2, 4, 'c', 'Q4(C)', debenhams + '\n\n' + L(2, 5, '(C) Outline two effects of industrial disputes.'), 15, 'business-0-14', 'industrial-dispute-effects',
    5, [], FIVE, five_three('Effect'), [UNTIED])
add(2, 4, 'd', 'Q4(D)', debenhams + '\n\n' + L(2, 5, '(D) Outline two functions of a shop steward.'), 15, 'business-0-14', 'shop-steward-functions',
    5, [15], FIVE, five_three('Function'), [UNTIED])
advert = L(2, 5, 'Child Care Assistant required for busy Crèche. Full time. Female applicants only. Applicants must be Irish and speak fluent English. Email your CV to: info@daisycrèche.ie')
add(2, 4, 'e', 'Q4(E)', L(2, 5, '(E) Explain, giving two reasons, why the advertisement below is unlawful under the Employment Equality Acts, 1998-2015.') + '\n\n' + advert,
    20, 'business-0-14', 'unlawful-advertisement', 5, [15], 'Two reasons at 10 marks each (5 + 5).', points('Reason', 2, (5, 5)),
    ['Scheme: ' + S(15, 'Gender discrimination') + ' (female applicants only) and ' + S(15, 'Racial discrimination') + ' (must be Irish), each 10 (5 + 5).'],
    extra=['business-3-20'])

buymie = L(2, 6, 'Buymie was founded in 2015 by Devan Hughes and Artavazd Soyhikyan as a mobile app for same-day grocery delivery. The app allows customers to shop for groceries in major retailers such as Tesco, Lidl and Dunnes. They hired an additional 200 personal shoppers and drivers due to increased demand.')
add(2, 5, 'a', 'Q5(A)', buymie + '\n\n' + L(2, 6, '(A) Outline three entrepreneurial characteristics/skills associated with entrepreneurs like Devan and Artavazd.'), 15,
    'business-1-5', 'entrepreneurial-characteristics', 6, [], 'Three at 5 marks each (3 + 2).', points('Characteristic', 3, (3, 2)))
add(2, 5, 'b', 'Q5(B)', buymie + '\n\n' + L(2, 6, '(B) Explain two ways in which Information & Communication Technology (ICT) can assist a business.'), 15,
    'business-2-12', 'ict-assists-business', 6, [], EIGHT, eight_seven('Way'), [UNTIED])
tesco = L(2, 6, 'Tesco Ireland Ltd increased their employees pay by 10% as an acknowledgement of their hard work during the difficult times of 2020 and 2021.')
add(2, 5, 'c', 'Q5(C)', tesco + '\n\n' + L(2, 6, '(C) Outline two benefits to a business of motivating employees.'), 15, 'business-2-11', 'motivating-employees-benefits',
    6, [17], EIGHT, eight_seven('Benefit'), [UNTIED])
L(2, 6, '5. 4. Social 2. Physiological')
pyramid = 'Maslow’s Hierarchy of Needs pyramid (printed, top to bottom): 5. ______; 4. ______; Social; 2. ______; Physiological.'
maslow_i = L(2, 6, '(D) (i) Maslow’s Hierarchy of Needs pyramid is presented below. List the missing levels 2, 4 and 5.')
add(2, 5, 'di', 'Q5(D)(i)', tesco + '\n\n' + maslow_i + '\n' + pyramid, 15, 'business-2-11', 'maslow-missing-levels', 6, [17],
    'Each missing level earns 5 marks.', [fixed('Missing levels', [('Level 2', 5), ('Level 4', 5), ('Level 5', 5)])],
    ['Answer key (scheme page 17): 2 ' + S(17, 'Safety/Security') + '; 4 Esteem; 5 ' + S(17, 'Self Actualisation') + '.'])
add(2, 5, 'dii', 'Q5(D)(ii)', tesco + '\n\n' + maslow_i + '\n' + pyramid + '\n' + L(2, 6, '(ii) Explain an initiative Tesco could introduce to try and satisfy their employees social needs at level 3.'),
    5, 'business-2-11', 'social-needs-initiative', 6, [17], 'One initiative: 5 marks (3 + 2).', [comps('Initiative', (3, 2))],
    ['Scheme examples: ' + S(17, 'Social Club/Outings') + '; ' + S(17, 'Matrix Structure') + '.'])
add(2, 5, 'e', 'Q5(E)', tesco + '\n\n' + L(2, 6, '(E) Explain the democratic style of leadership sometimes used by Tesco when making decisions.'), 10,
    'business-2-11', 'democratic-leadership', 6, [17], 'Explanation: 10 marks (5 + 5).', [comps('Democratic leadership', (5, 5))],
    ['Scheme: ' + S(17, 'Democratic leadership is an inclusive style of leadership.') + ' ' + S(17, 'Tesco managers involve staff in decision making.')])

hotel = L(2, 7, 'Dunmackey House Hotel', 'Dunmackey House Hotel has struggled to remain open over the past year. Aideen McNally, the Human Resource Manager, had to make seven staff redundant during this time. Aideen did not like this aspect of manpower planning and hopes they will be able to re-hire staff in the future. All staff were paid redundancy based on six weeks’ pay per year of service.')
add(2, 6, 'a', 'Q6(A)', hotel + '\n\n' + L(2, 7, '(A) Explain three methods, other than wages, of rewarding employees.'), 15, 'business-3-20', 'rewarding-employees',
    7, [], 'Three at 5 marks each (3 + 2).', points('Method', 3, (3, 2)))
add(2, 6, 'b', 'Q6(B)', hotel + '\n\n' + L(2, 7, '(B) Outline two functions, other than manpower planning, which are part of a Human Resource Manager’s job.'), 20,
    'business-3-20', 'hr-manager-functions', 7, [], 'Two functions at 10 marks each (5 + 5).', points('Function', 2, (5, 5)))
tom = L(2, 7, 'Tom Delaney earned €490 per week in the Hotel and worked there for 11 years. He decided to use his redundancy package to purchase a van and provide a delivery service for the local retailers in Dunmackey who were relying on online/phone in sales for survival. He needed to purchase motor insurance for business use on the van and was hoping his premium would not be too high.')
red = add(2, 6, 'c', 'Q6(C)', hotel + '\n\n' + tom + '\n\n' + L(2, 7, '(C) Calculate Tom’s redundancy package from Dunmackey House Hotel.'), 10, 'business-3-20',
          'redundancy-package-calculation', 7, [19], 'The correct package earns 10; if it is incorrect, good workings earn up to 8.',
          [comps('Redundancy package', (10,), ['Package calculated'])],
          ['Scheme: ' + S(19, 'Tom will get a redundancy payment of €32,340') + '; workings €490 × 6 weeks × 11 years = €32,340, marked 2 + 1 + 2 + 1 + 2; '
           + S(19, '(If incorrect, allow up to 8 marks for good workings)') + '.'])
permit(red, 0, list(range(9)) + [10])
add(2, 6, 'di', 'Q6(D)(i)', tom + '\n\n' + L(2, 7, '(D) (i) Name and explain one type of motor insurance Tom could purchase.'), 10, 'business-3-17',
    'motor-insurance-type', 7, [19], 'Name and explain one type: 10 marks (5 + 5).', [comps('Motor insurance', (5, 5), ['Type named', 'Type explained'])],
    ['Scheme types: ' + S(19, 'Comprehensive Insurance') + '; ' + S(19, 'Third Party – minimum requirement by law') + '; Third Party, Fire and Theft.'])
add(2, 6, 'dii', 'Q6(D)(ii)', tom + '\n\n' + L(2, 7, '(ii) Name one factor which might impact on a motor insurance premium.'), 5, 'business-3-17',
    'motor-premium-factor', 7, [19], 'One factor for 5 marks.', [single('Factor', 5, 'Factor named')],
    ['Scheme examples: ' + S(19, 'Type of Driving Licence') + '; driving experience or years of no claims bonus; make, model and value of vehicle; '
     + 'previous accidents or claims; penalty points; age.'])
add(2, 6, 'e', 'Q6(E)', tom + '\n\n' + L(2, 7, '(E) Tom must adhere to the principles of Utmost Good Faith, Indemnity and Insurable Interest. Explain two of these principles.'),
    15, 'business-3-17', 'insurance-principles-choice', 7, [20], 'Explain two of the three printed principles: 8 (4 + 4) and 7 (4 + 3).',
    seq(comps('First principle you chose', (4, 4)), comps('Second principle you chose', (4, 3))),
    ['You choose which two of the three printed principles to explain. Each is marked alike: the first principle you explain earns up to 8 (4 + 4) and the second up to 7 (4 + 3), whichever two you choose.',
     'Utmost Good Faith (scheme PDF page 20): “' + S(20, 'A person taking out insurance must be truthful when completing proposal form – all material facts must be declared.') + '”',
     'Indemnity: “' + S(20, 'A person cannot make a profit from insurance – the purpose of insurance is to leave the person in the same financial position as before the claim.') + '”',
     'Insurable Interest: “' + S(20, 'The person taking out insurance must have a financial interest in the item being insured – must gain from its existence and suffer financially from its loss.') + '”'])

golf = L(2, 8, 'Eden Hills Golf Club', 'Eden Hills Golf Club is a very popular course in the sunny South East of Ireland. It has a top-class course, with a bar that supplies bar food. They want to expand the club house to include a function room, to hold bigger events in the future. The golf club has no money saved and sees this as a long-term investment. The Finance Committee is currently producing a business plan and a Zoom meeting of all club members has been called.')
cash = L(2, 8, 'Cashflow Forecast Eden Hills Golf Club Ltd for the first 3 months of 2022', '2022 January February March Total',
         'Total Receipts (A) 13,000 14,000 25,000 52,000', 'Total Payments (B) 21,000 15,000 13,000 49,000', 'Net Cash (A-B) -8,000 -1,000 12,000 3,000',
         'Opening Cash 2,000 -6,000 -7,000 2,000', 'Closing Cash -6,000 -7,000 5,000 5,000')
items = L(2, 8, '(A) Name one item Eden Hills Golf Club might include in their cashflow forecast under each of the following sections:')
add(2, 7, 'ai', 'Q7(A)(i)', golf + '\n\n' + cash + '\n\n' + items + '\n' + L(2, 8, '(i) Receipts section'), 5, 'business-3-16', 'cashflow-receipt-item',
    8, [21], 'One receipts item for 5 marks.', [single('Receipts item', 5, 'Item named')],
    ['Scheme examples: ' + S(21, 'Membership/Subscriptions Green Fees Bar Sales Food/Restaurant Sales Grant') + '. ' + S(21, 'Accept any other relevant answer.')])
add(2, 7, 'aii', 'Q7(A)(ii)', golf + '\n\n' + cash + '\n\n' + items + '\n' + L(2, 8, '(ii) Payments section.'), 5, 'business-3-16', 'cashflow-payment-item',
    8, [21], 'One payments item for 5 marks.', [single('Payments item', 5, 'Item named')],
    ['Scheme examples: ' + S(21, 'Wages Insurance Light & Heat Maintenance') + '. ' + S(21, 'Accept any other relevant answer.')])
better = L(2, 8, '(B) (i) Does Eden Hills Golf Club have a better cashflow position in January or March?')
add(2, 7, 'bi', 'Q7(B)(i)', golf + '\n\n' + cash + '\n\n' + better, 5, 'business-3-16', 'better-cashflow-month', 8, [21], 'State the month for 5 marks.',
    [single('Better month', 5, 'Month stated')], ['Scheme: ' + S(21, 'Answer: March') + '.'])
add(2, 7, 'bii', 'Q7(B)(ii)', golf + '\n\n' + cash + '\n\n' + better + '\n' + L(2, 8, '(ii) Outline two possible reasons for your answer.'), 15, 'business-3-16',
    'cashflow-month-reasons', 8, [21], EIGHT, eight_seven('Reason'),
    ['Give reasons for the month you chose in (i). The scheme lists reasons for March and, after “OR”, reasons for January, such as '
     + S(21, 'Payments exceeded receipts by €8,000 in January') + '.', UNTIED])
add(2, 7, 'c', 'Q7(C)', golf + '\n\n' + L(2, 8, '(C) Outline two advantages of meetings as a method of communication.'), 15, 'business-2-12', 'meetings-advantages',
    8, [22], FIVE, five_three('Advantage'), [UNTIED])
add(2, 7, 'd', 'Q7(D)', golf + '\n\n' + L(2, 8, '(D) Explain two sources of long term finance Eden Hills Golf Club could use to expand its business.'), 15, 'business-3-16',
    'long-term-finance-sources', 8, [22], FIVE, five_three('Source'),
    ['Scheme sources: ' + S(22, 'Retained Earnings (Reserves)') + '; ' + S(22, 'Long Term loan (Debentures)') + '; ' + S(22, 'Sports Capital Grant') + '. '
     + S(22, 'Do not accept Share Capital/Equity Capital.'), UNTIED])
add(2, 7, 'e', 'Q7(E)', golf + '\n\n' + L(2, 8, '(E) Outline two benefits of preparing a business plan.'), 15, 'business-4-15', 'business-plan-benefits',
    8, [22], FIVE, five_three('Benefit'), [UNTIED], extra=['business-2-13'])

cadbury = L(2, 9, 'Cadbury has launched its latest products.', 'The stages of the new product development process included Idea Generation, Product Screening and Feasibility Study. Cadbury also engaged in test marketing.')
add(2, 8, 'a', 'Q8(A)', cadbury + '\n(Idea Generation, Product Screening and Feasibility Study are underlined.)\n\n' + L(2, 9, '(A) Explain two of the underlined terms above.'),
    15, 'business-4-14', 'new-product-development-terms-choice', 9, [], 'Explain two of the three underlined terms: 8 (5 + 3) and 7 (5 + 2).',
    seq(comps('First term you chose', (5, 3)), comps('Second term you chose', (5, 2))),
    ['You choose which two of the three underlined terms to explain. Each is marked alike: the first term you explain earns up to 8 (5 + 3) and the second up to 7 (5 + 2), whichever two you choose.',
     'Idea Generation (scheme PDF page 23): “' + S(23, 'This is a systematic approach to coming up with ideas for new products.') + '”',
     'Product Screening: “' + S(23, 'This involves assessing all ideas for a new product, discarding the least viable and unworkable ideas and choosing the most suitable idea, the one that has best potential to succeed in the marketplace.') + '”',
     'Feasibility Study: “' + S(23, 'A Feasibility Study is carried out to see if the product can actually be made and brought to the market.') + '”'])
add(2, 8, 'b', 'Q8(B)', cadbury + '\n\n' + L(2, 9, '(B) Outline two methods of field research that Cadbury may have used as part of its test marketing stage.'), 15,
    'business-4-16', 'field-research-methods', 9, [], FIVE, five_three('Method'),
    ['Scheme methods: ' + S(23, 'Survey/ Questionnaire') + '; Interview; Consumer Panel; Observation.', UNTIED])
mass = L(2, 9, 'Cadbury bars are manufactured using mass production. The bars are wrapped using packaging with the distinctive purple Cadbury colour.')
mass_i = L(2, 9, '(C) (i) Explain the term mass production.')
add(2, 8, 'ci', 'Q8(C)(i)', mass + '\n\n' + mass_i, 7, 'business-4-15', 'mass-production-explained', 9, [24], 'Explanation: 7 marks (4 + 3).',
    [comps('Mass production', (4, 3))], ['Scheme: ' + S(24, 'Mass Production involves the manufacture of very large quantities of identical products on a continuous basis.')])
add(2, 8, 'cii', 'Q8(C)(ii)', mass + '\n\n' + mass_i + '\n' + L(2, 9, '(ii) Name and explain two other methods of production.'), 13, 'business-4-15',
    'other-production-methods', 9, [24], 'Job production 7 (4 + 3) and batch production 6 (3 + 3).',
    seq(comps('Job production', (4, 3)), comps('Batch production', (3, 3))),
    ['The scheme prints 7m (4 + 3) beside ' + S(24, 'Job Production:') + ' and 6m (3 + 3) beside ' + S(24, 'Batch Production') + '.'])
chan = add(2, 8, 'd', 'Q8(D)', mass + '\n\n' + L(2, 9, '(D) Illustrate, using a diagram, the channel of distribution Cadbury might use to distribute their chocolate bars.'), 10,
           'business-4-17', 'channel-of-distribution-diagram', 9, [25], 'Four stages at 2 marks each and 2 for the arrows.',
           [fixed('Channel diagram', [('Manufacturer', 2), ('Wholesaler', 2), ('Retailer', 2), ('Consumer', 2), ('Arrows', 2)])],
           ['Scheme: ' + S(25, 'MANUFACTURER WHOLESALER RETAILER CONSUMER') + ', ' + S(25, '4 x 2m + 2m for arrows') + '.'])
add(2, 8, 'e', 'Q8(E)', mass + '\n\n' + L(2, 9, '(E) Outline two functions of product packaging.'), 15, 'business-4-17', 'packaging-functions',
    9, [25], FIVE, five_three('Function'), [UNTIED])

ryan = L(2, 10, 'The Ryan family have operated their hardware and DIY store for over 60 years on the outskirts of Limerick city. They had a high sales turnover in 2020, due to the large amount of people renovating their homes. However, a large DIY chain store has recently opened in the nearby retail park. The Ryan’s are concerned that they may lose some of their customers to this new chain store, despite building a good name over 60 years.')
add(2, 9, '-a', 'Q9(A)', ryan + '\n\n' + L(2, 10, '(A) Outline two reasons why a good brand name is important to a business like the Ryan’s.'), 15, 'business-4-17',
    'brand-name-importance', 10, [], EIGHT, eight_seven('Reason'), [UNTIED])
add(2, 9, '-b', 'Q9(B)', ryan + '\n\n' + L(2, 10, '(B) Outline three factors the Ryan’s must consider before setting prices for their products.'), 20, 'business-4-17',
    'pricing-factors', 10, [], 'Three factors: 7 (4 + 3), 7 (4 + 3) and 6 (4 + 2).', unequal('Factor', [(4, 3), (4, 3), (4, 2)], None),
    ['The 7/7/6 sequence prices the three factors, not particular factors.'])
promo_i = L(2, 10, '(C) (i) Explain the term sales promotion.')
add(2, 9, '-c-i', 'Q9(C)(i)', ryan + '\n\n' + promo_i, 8, 'business-4-17', 'sales-promotion-explained', 10, [], 'Explanation: 8 marks (4 + 4).',
    [comps('Sales promotion', (4, 4))], ['Scheme: ' + S(26, 'Sales Promotion involves using short term incentives/gimmicks to attract extra consumption/boost sales.')], new=True)
cum(2, 9, '-c-ii', 'Q9(C)(ii)', ryan + '\n\n' + promo_i + '\n' + L(2, 10, '(ii) List three methods of sales promotion the Ryan’s could use to compete with the larger chain store.'),
    (4, 4, 4), 'business-4-17', 'sales-promotion-methods', 10, [],
    'Scheme examples: ' + S(26, 'Special offers: buy one, get one free / three for price of two') + '; competitions offering prizes; loyalty cards; money off vouchers; free samples; discounts.',
    noun='methods')
cum(2, 9, '-d', 'Q9(D)', ryan + '\n\n' + L(2, 10, '(D) List two reasons why businesses expand.'), (5, 5), 'business-4-18', 'reasons-businesses-expand', 10, [27],
    'Scheme examples: ' + S(27, 'To increase sales/profits') + '; to protect itself against competitors; to diversify; ambition; economies of scale; '
    + 'to protect source of supplies; to eliminate competition.', noun='reasons')
add(2, 9, '-e', 'Q9(E)', ryan + '\n\n' + L(2, 10, '(E) Explain the difference between a merger and a takeover.'), 10, 'business-4-18', 'merger-versus-takeover',
    10, [27], 'Merger 5 (3 + 2) and takeover 5 (3 + 2).', [comps('Merger', (3, 2), i=1), comps('Takeover', (3, 2), i=2)],
    ['Scheme: ' + S(27, 'A Merger is when two companies voluntarily agree to come together and operate as one.') + ' '
     + S(27, 'A Takeover is when one company buys out another company (with or without its consent) by buying at least 51% of its shares.')])

# ---------------------------------------------------------------- checks and write-out
qn = lambda c: c['questionRef'].split(' Q')[1].split('(')[0]
for section, count, total in [('1', 15, 15), ('2', 9, 75)]:
    for q in range(1, count + 1):
        got = sum(c['totalMarks'] for c in P.created if c['section'] == section and qn(c) == str(q))
        assert got == total, (section, q, got)
legacy = {i for i in ORIGINAL if i.startswith('bus-2021-ol-')}
assert legacy <= {c['id'] for c in P.created}, sorted(legacy - {c['id'] for c in P.created})
new = sorted(c['id'] for c in P.created if c['id'] not in ORIGINAL)
assert new == ['bus-2021-ol-s1-q7', 'bus-2021-ol-s2-q9-c-i', 'bus-2021-ol-s2-q9-d'], new
assert not P.pools

SELECTION = {
    1: 'No finite printed answer menu occurs in Section 1 (answer five of fifteen at 15 marks). TRUE/FALSE labels, the word bank in Q3, the matching rows in Q4, Q7 and Q12, the tick boxes in Q10 and Q14 and the circled options in Q15 are required answer formats. Support-note lists are open examples.',
    2: 'Two printed choices stay one card each: Q6(E) explain two of three printed insurance principles and Q8(A) explain two of three underlined product-development terms. The scheme marks every choice alike (8 then 7), so each card carries all three items and its guidance quotes the scheme for every item. Q1(D) “any two functions of a trade union” is open. Sub-parts with their own published marks are separate cards. Support-note lists are open examples.',
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
    if fileid == 'LC033GLP033EV' and m == 'two of' and own(w, m, 'Explain two of these principles'):
        return 'finite-choice', 'Section 2 Q6(E) asks for two of three printed insurance principles. The scheme marks any two alike (8 then 7), so one card carries all three principles with the scheme wording for each.', 'bus-2021-ol-s2-q6e'
    if fileid == 'LC033GLP033EV' and m == 'two of' and own(w, m, 'Explain two of the underlined terms above'):
        return 'finite-choice', 'Section 2 Q8(A) asks for two of three underlined product-development terms. The scheme marks any two alike (8 then 7), so one card carries all three terms with the scheme wording for each.', 'bus-2021-ol-s2-q8a'
    if m == 'any two' and own(w, m, 'Describe any two functions of a trade union'):
        return 'open-response', 'Section 2 Q1(D) lets the candidate describe any two functions of a trade union; no closed list is printed, so the task stays whole.', None
    if m == 'or' and own(w, m, 'surplus or a deficit'):
        return 'required-headings', 'Section 2 Q3(A)(ii) requires a determination of surplus or deficit; it is one required answer, not a choice of task.', None
    if m == 'or' and own(w, m, 'January or March'):
        return 'required-headings', 'Section 2 Q7(B)(i) requires one determination (January or March); (ii) asks for reasons for that answer and is its own card.', None
    if m == 'or' and (own(w, m, 'TRUE or FALSE') or own(w, m, 'True or False')):
        return 'required-headings', 'TRUE/FALSE are answer labels for each of the four required statements in Section 1 Q2, not optional tasks.', None
    if m == 'or' and own(w, m, 'opportunity or threat'):
        return 'required-headings', 'Strength/weakness/opportunity/threat are the tick-box labels for each of the four required statements in Section 1 Q14, not optional tasks.', None
    if m == 'Choose' and own(w, m, 'Choose the appropriate words'):
        return 'required-headings', 'Section 1 Q3 is a word-bank completion: both blanks are required and the printed words are the answer options, not optional tasks.', None
    assert (fileid, page) in {('LC033GLP032EV', 2), ('LC033GLP032EV', 9), ('LC033GLP032EV', 36), ('LC033GLP033EV', 1), ('LC033GLP033EV', 2)}, (fileid, page, m, w)
    return 'exam-navigation', 'Cover instructions, the question-choice rubric, pen/pencil instructions, answerbook supplies or copyright boilerplate. They do not create alternative task routes.', None


n = P.write([(1, range(1, 16)), (2, range(1, 10))], SELECTION, classify,
            'Every part of {year} Ordinary Section {section} Question {q} was visually checked against its SEC booklet and the expected responses with their marks. Booklet-specific p1/p2 identities keep the short and long question numbering apart.')
print(f'Reviewed {len(P.created)} 2021 Ordinary base tasks; classified {n} raw selection matches.')
