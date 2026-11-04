"""Review the 2016 Ordinary English paper (one booklet: Section 1 and Section 2).

2016: answer ten of fifteen short questions at 10 marks and four of eight
long questions at 75 (one from Part 1, two from Part 2 and one other), all in
one twelve-page booklet (LC033GLP000EV, the same file id as its scheme). No
Ordinary card existed for 2016, so every card is new. The allocation summary
(scheme pages 5-9) sets each boundary; printed sub-parts with their own
published marks are separate cards. No printed choice of task occurs.
The scheme's text layer mangles some words ("Wz" for PAYE, "h^" for USC);
quotations are taken only from clean runs, read against the rendered pages.
"""
from bus_lib import (Paper, ORIGINAL, comps, points, seq, unequal, single, response, fixed, permit)

T = {(1, q): 5 for q in range(1, 16)}
T.update({(2, 1): 6, (2, 2): 6, (2, 3): 7, (2, 4): 7, (2, 5): 8, (2, 6): 8, (2, 7): 9, (2, 8): 9})
P = Paper(2016, 'ordinary', {1: 'LC033GLP000EV', 2: 'LC033GLP000EV'}, 'LC033GLP000EV', T)
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


def evens(card):
    return permit(card, 0, list(range(0, card['totalMarks'] + 1, 2)))


# ---------------------------------------------------------------- Section 1 (10 marks each)
add(1, 1, '', 'Q1', L(1, 2, 'What do the following letters stand for? Write each answer in the space provided.') + '\nVAT\nWWW\nAGM', 10, 'business-3-18',
    'abbreviations-vat-www-agm', 2, [10], 'The first correct term earns 4 (2 + 1 + 1); the second and third 3 each (1 + 1 + 1).',
    [comps('First correct term', (4,), ['Words written in full'], 1), comps('Second correct term', (3,), ['Words written in full'], 2),
     comps('Third correct term', (3,), ['Words written in full'], 3)],
    ['Answer key: VAT ' + S(10, 'Value Added Tax') + '; WWW ' + S(10, 'World Wide Web') + '; AGM ' + S(10, 'Annual General Meeting') + '.'],
    extra=['business-2-12'])
L(1, 2, 'LAND CAPITAL VAT WWW AGM')
cum(1, 2, '', 'Q2', L(1, 2, 'List three methods of written communication a business might use.'), (4, 3, 3), 'business-2-12', 'written-communication-methods',
    2, [10], 'Scheme examples (page 10): email, letter, memo, business documents (invoice, statement, credit note), report, agenda, minutes, notice, texting, social media.',
    noun='methods')
S(10, 'Email • Letter • Memo/Memorandum • Business Document; Invoice, Statement, Credit Note etc. • Report • Agenda • Minutes • Notice • Texting')
L(1, 2, 'Name: Ken McGrath € € Gross Pay 30,000 Deductions PAYE (20% of €30,000) - Tax Credit 6000 3200 Net PAYE 2800 PRSI (4% of €30,000) (i) USC (3% of €30,000) (ii) Total Deductions (iii) Net Annual Take Home Pay (iv)')
flat(add(1, 3, '', 'Q3', L(1, 2, 'Calculate Ken McGrath’s net annual take home pay from the following details. Show your workings.')
         + '\nName: Ken McGrath\nGross Pay €30,000\nDeductions\nPAYE (20% of €30,000) 6000\n- Tax Credit 3200\nNet PAYE 2800'
         + '\nPRSI (4% of €30,000) (i)\nUSC (3% of €30,000) (ii)\nTotal Deductions (iii)\nNet Annual Take Home Pay (iv)', 10, 'business-3-18',
         'net-annual-take-home-pay-2016', 2, [10], 'PRSI 3, USC 3, total deductions 2 and take home pay 2.',
         [response(1, 'Net annual take home pay', [('prsi', '(i) PRSI €1,200 (30,000 x 4 / 100)', 3), ('usc', '(ii) USC €900 (30,000 x 3 / 100)', 3),
                                                   ('total', '(iii) Total Deductions €4,900', 2), ('net', '(iv) Net Annual Take Home Pay €25,100', 2)])],
         ['Scheme (page 10): ' + S(10, 'Total Deductions (iii) 4,900 Net Annual Take Home Pay (iv) 25,100') + '; workings '
          + S(10, 'Show Workings PRSI 30,000 x 4 / 100 = 1,200 Show Workings USC 30,000 x 3 / 100 = 900') + ' (3, 3, 2, 2).']))
cum(1, 4, '', 'Q4', L(1, 2, 'Complete the missing Factors of Production in the spaces provided.') + '\nLAND | ______ | CAPITAL | ______', (5, 5), 'business-1-5',
    'missing-factors-of-production', 2, [10], 'Answer key (scheme page 10): Labour and Enterprise (' + S(10, 'LAND LABOUR CAPITAL ENTERPRISE') + '; Land and Capital are printed).',
    noun='factors')
flat(add(1, 5, '', 'Q5', L(1, 3, 'The chart below illustrates the projected sales of new cars for Maher Motors Ltd for the six month period January to June 2017.')
         + '\n(Bar chart: projected new car sales for Maher Motors Ltd, January to June 2017, number of car sales in units on a scale of 0 to 350 — read the bars on the printed page.)\n'
         + L(1, 3, '(a) Name the method of visual communication presented above.', '(b) (i) Identify the month with the highest projected sales.',
             '(ii) Identify the projected number of cars that will be sold in that month.', '(c) Name one other method of visual communication.'),
         10, 'business-2-12', 'car-sales-bar-chart', 3, [11], '(a) 3, (b) 2 x 2 and (c) 3.',
         [response(1, 'Bar chart', [('a', '(a) Bar chart', 3), ('b-i', '(b)(i) January', 2), ('b-ii', '(b)(ii) 300', 2), ('c', '(c) Another method, e.g. pie chart', 3)])],
         ['Scheme (page 11): (a) ' + S(11, 'Bar Chart (3)') + '; (b) ' + S(11, 'January (2)') + ', ' + S(11, '300 (2)') + '; (c) '
          + S(11, 'Pie Chart, Pictogram, Line graph, Breakeven chart, Map. (3)')]))
cum(1, 6, '', 'Q6', L(1, 3, 'Name the three management activities.'), (4, 3, 3), 'business-2-13', 'three-management-activities', 3, [11],
    'Answer key (scheme page 11): ' + S(11, '(i) Planning (ii) Organising (iii) Controlling') + '.', noun='activities')
add(1, 7, '', 'Q7', L(1, 3, 'Choose the appropriate words to complete the sentence below. (One word does not apply).', 'POWER DECISIONS TARGETS')
    + '\nEmployee empowerment provides staff with more ______ ' + L(1, 3, 'to make their own') + ' ______ ' + L(1, 3, 'about how to do their jobs.'), 10, 'business-2-11',
    'empowerment-word-bank', 3, [11], 'Each blank earns 5 marks.', [fixed('Completed blanks', [('First blank', 5), ('Second blank', 5)])],
    ['Answer key (scheme page 11): ' + S(11, 'Employee Empowerment provides staff with more POWER to make their own DECISIONS about how to do their jobs.') + ' Targets is not used.'])
L(1, 3, 'Employee empowerment provides staff with more')
cum(1, 8, '', 'Q8', L(1, 3, 'List two reasons for unfair dismissal, under the Unfair Dismissals Act 1977/2007.'), (5, 5), 'business-0-14', 'unfair-dismissal-reasons',
    3, [11], 'Scheme examples (page 11): ' + S(11, 'Member of a trade union/engaging in trade union activities.') + ' ' + S(11, 'Pregnancy or matters connected with pregnancy or birth.')
    + ' ' + S(11, 'Race or colour.'), noun='reasons')
add(1, 9, '', 'Q9', L(1, 4, 'Outline two ways in which a business could become more environmentally friendly.'), 10, 'business-5-17', 'environmentally-friendly-ways',
    4, [12], 'Two ways at 5 marks each (3 + 2).', points('Way', 2, (3, 2)),
    ['Scheme examples: ' + S(12, 'Minimise waste/safe disposal of waste.') + ' ' + S(12, 'Pollution prevention – minimise emissions.')])
cum(1, 10, '', 'Q10', L(1, 4, 'Write TRUE or FALSE after each of the following statements.', 'Inflation refers to an increase in general prices from one year to the next.',
                        'A recession leads to increased spending by consumers.', 'Lower interest rates mean the cost of borrowing money is cheaper.',
                        'Exchanges rates refer to the price of one currency expressed in terms of another currency.',
                        'High unemployment leads to an increase in government spending on social welfare.'),
    (2, 2, 2, 2, 2), 'business-5-15', 'economy-true-false', 4, [12], 'Answer key (scheme page 12): TRUE; FALSE; TRUE; TRUE; TRUE.')
S(12, 'Inflation refers to an increase in general prices from one year to the next. True A recession leads to increased spending by consumers. False')
add(1, 11, '', 'Q11', L(1, 4, 'Indicate which government body is responsible for further education and training. Place a (✓) in the correct box.',
                        'Solas (Formerly known as FÁS) IDA (Industrial Development Authority)').replace(' IDA', '\nIDA'),
    10, 'business-5-15', 'further-education-body-tick', 4, [12], 'The correct box earns 10 marks.', [single('Correct box', 10, 'Body ticked')],
    ['Answer key (tick on scheme page 12): Solas (formerly known as FÁS).'])
cum(1, 12, '', 'Q12', L(1, 4, 'Name two European Union (EU) policies.'), (5, 5), 'business-6-14', 'eu-policies-named', 4, [13],
    'Scheme policies (page 13): Common Agricultural Policy, Common Fisheries Policy, Social Policy/EU Social Charter, Economic and Monetary Policy, European Competition Policy.',
    noun='policies')
S(13, 'Common Agricultural policy • Common Fisheries Policy • Social Policy/EU Social Charter • Economic and Monetary Policy/European Monetary Policy • European Competition Policy')
add(1, 13, '', 'Q13', L(1, 4, 'Insomnia coffee company is an example of an Irish franchise.', '(i) Explain the term franchising.', '(ii) Give one other example of a franchise.'), 10,
    'business-5-14', 'franchising-explained-with-example', 4, [13], 'Explanation 8 (4 + 4) and an example 2.',
    seq(comps('Franchising', (4, 4)), single('Another franchise', 2, 'Example named')),
    ['Scheme: ' + S(13, 'This is the granting of a licence by the franchisor to the franchisee allowing the right to supply and sell its product or service.')
     + ' Examples: Costa Coffee, Starbucks, KFC.'])
S(13, 'Costa Coffee, Starbucks, KFC.')
cum(1, 14, '', 'Q14', L(1, 5, 'The diagram of the Product Life Cycle below is incomplete. The Saturation stage has been filled in and the names of the other stages are missing. Fill in the missing stages below.')
    + '\n(Diagram: a sales curve against time with five stage boxes: ' + L(1, 5, 'Stage 1 Stage 2 Stage 3 Saturation Stage 5') + '.)\nStage 1 ______\nStage 2 ______\nStage 3 ______\nStage 4 Saturation\nStage 5 ______',
    (3, 3, 2, 2), 'business-4-17', 'plc-missing-stages', 5, [13],
    'Answer key (scheme page 13): ' + S(13, 'Stage 1 Launch/Introduction Stage 2 Growth Stage 3 Maturity Stage 4 Saturation Stage 5 Decline') + '.', noun='stages')
cum(1, 15, '', 'Q15', '\n'.join([L(1, 5, 'Column 1 is a list of business terms relating to contract law. Column 2 is a list of possible explanations for these terms. One explanation has no match. Match the two lists by placing the letter of the correct explanation under the relevant number below.'),
                                 L(1, 5, '1. Capacity', '2. Contract', '3. Consideration', '4. Consent', '5. Frustration'),
                                 L(1, 5, 'A. An unforeseen event makes it impossible for a contract to be fulfilled', 'B. Person must be legally able to enter into a contract.',
                                   'C. The parties entering the contract must do so of their own free will.', 'D. The legally binding agreement made between two or more parties.',
                                   'E. Some contracts must be drawn up in a certain way if they are to be legal contracts.',
                                   'F. Something of value exchanged between the parties to the contract.')]),
    (2, 2, 2, 2, 2), 'business-0-12', 'contract-terms-matching', 5, [13], 'Answer key (scheme page 13): 1 B; 2 D; 3 F; 4 C; 5 A. Explanation E is unused.', noun='matches')
S(13, '1 2 3 4 5 B D F C A')

# ---------------------------------------------------------------- Section 2 (75 marks each)
ciara = L(2, 6, 'Black Friday Disaster!') + '\n' + L(2, 6, 'Ciara purchased all of her Christmas gifts in November at the “Black Friday” sales. She got a great discount on a new laptop for her husband. On Christmas Day, when he opened the present, he realised the laptop screen was damaged. Ciara wasn’t sure whether she was entitled to a remedy because she had purchased the laptop in a sale. Ciara contacted the Consumers Association of Ireland and she was informed that she had exactly the same rights and protections as a person who had purchased the product at full price.')
law = add(2, 1, 'a', 'Q1(A)', ciara + '\n\n' + L(2, 6, '(A) Name the law that protects Ciara in this situation.'), 10, 'business-0-13', 'law-protecting-ciara', 6, [14],
          'Name the Act: 5 @ 2 marks.', [comps('Consumer law', (10,), ['Act named'])],
          ['Scheme: ' + S(14, 'Sale (2) of Goods (2) and Supply (2) of Services (2) Act 1980 (2)') + '.'])
evens(law)
add(2, 1, 'b', 'Q1(B)', ciara + '\n\n' + L(2, 6, '(B) Explain two legal rights of the consumer under this law.'), 15, 'business-0-13', 'consumer-legal-rights',
    6, [14], EIGHT, eight_seven('Right'), [UNTIED])
add(2, 1, 'c', 'Q1(C)', ciara + '\n\n' + L(2, 6, '(C) Outline two forms of remedy/redress that Ciara is entitled to in the above case.'), 15, 'business-0-13', 'ciara-remedies',
    6, [14], EIGHT, eight_seven('Remedy'), [UNTIED])
train = L(2, 6, 'Train Drivers Industrial Action') + '\n' + L(2, 6, 'Train drivers at Irish Rail were involved in an industrial relations dispute with their employer. The train drivers were represented by their Trade Unions, the NBRU (National Bus and Rail Workers Union) and SIPTU (Services, Industrial, Professional and Technical Union).')
add(2, 1, 'd', 'Q1(D)', train + '\n\n' + L(2, 6, '(D) Outline three causes of industrial relations disputes.'), 15, 'business-0-14', 'industrial-dispute-causes-2016',
    6, [15], 'Three causes at 5 marks each (3 + 2).', points('Cause', 3, (3, 2)))
add(2, 1, 'e', 'Q1(E)', train + '\n\n' + L(2, 6, '(E) Outline two types of official industrial action a trade union can take as part of an industrial relations dispute.'), 20,
    'business-0-14', 'official-industrial-action-2016', 6, [15], 'Two types at 10 marks each (5 + 5).', points('Type', 2, (5, 5)),
    ['Scheme examples: official strike, work-to-rule, overtime ban, token stoppage. ' + S(15, 'Overtime ban – where workers refuse to do overtime.')])

apple = L(2, 7, 'Apple Chief Executive Tim Cook announced plans to create 1,000 new jobs at Apple’s campus in Cork.') + ' (' + L(2, 7, 'www.irishexaminer.com') + ')'
sec_i = L(2, 7, '(A) (i) Explain the term secondary sector.')
add(2, 2, 'ai', 'Q2(A)(i)', apple + '\n\n' + sec_i, 12, 'business-5-13', 'secondary-sector-explained', 7, [16], 'Explanation: 12 marks (4 + 4 + 4).',
    [comps('Secondary sector', (4, 4, 4))], ['Scheme: ' + S(16, 'The secondary sector includes the manufacturing and construction industries.')])
add(2, 2, 'aii', 'Q2(A)(ii)', apple + '\n\n' + sec_i + '\n' + L(2, 7, '(ii) Name one other sector of the economy.'), 3, 'business-5-13', 'other-sector-named',
    7, [16], 'Name the sector for 3 marks.', [single('Sector', 3, 'Sector named')], ['Answer: ' + S(16, 'Primary sector or Tertiary/Services sector.')])
mnc_i = L(2, 7, '(B) (i) Apple is a multinational company. Explain the term multinational company.')
add(2, 2, 'bi', 'Q2(B)(i)', apple + '\n\n' + mnc_i, 12, 'business-6-15', 'multinational-explained-2016', 7, [16], 'Explanation: 12 marks (7 + 5).',
    [comps('Multinational company', (7, 5))], ['Scheme: ' + S(16, 'A company with its head office in one country and branches in a number of other countries throughout the world.')])
add(2, 2, 'bii', 'Q2(B)(ii)', apple + '\n\n' + mnc_i + '\n' + L(2, 7, '(ii) Name one other multinational company.'), 3, 'business-6-15', 'other-multinational-named',
    7, [16], 'Name the company for 3 marks.', [single('Multinational company', 3, 'Company named')], ['Scheme examples: ' + S(16, 'Intel, Pfizer, Google, Glanbia.')])
add(2, 2, 'c', 'Q2(C)', apple + '\n\n' + L(2, 7, '(C) Outline two possible reasons why Apple decided to locate in Ireland.'), 20, 'business-6-15', 'why-apple-located-in-ireland',
    7, [16], 'Two reasons at 10 marks each (5 + 5).', points('Reason', 2, (5, 5)),
    ['Scheme examples: ' + S(16, 'Low corporation tax, 12.5 % – Companies are attracted by the low tax on profits.')])
add(2, 2, 'd', 'Q2(D)', apple + '\n\n' + L(2, 7, '(D) Apple is a Public Limited Company (plc). Explain two benefits of operating as a plc.'), 15, 'business-5-14', 'plc-benefits',
    7, [17], EIGHT, eight_seven('Benefit'), [UNTIED])
add(2, 2, 'e', 'Q2(E)', L(2, 7, 'The Irish economy experienced economic growth in 2015.') + '\n\n' + L(2, 7, '(E) Outline two benefits of economic growth for the Irish economy.'), 10,
    'business-5-15', 'economic-growth-benefits', 7, [17], 'Two benefits at 5 marks each (3 + 2).', points('Benefit', 2, (3, 2)))

figures = L(2, 7, 'Visible Imports €3,700m Visible Exports €4,800m').replace(' Visible Exports', '\nVisible Exports')
bot_i = L(2, 7, '(A) (i) Using the above information, calculate the Balance of Trade. Show your workings.')
flat(add(2, 3, 'ai', 'Q3(A)(i)', figures + '\n\n' + bot_i, 12, 'business-6-13', 'balance-of-trade-2016', 7, [18], 'Formula 3 and the workings 3 + 3 + 3.',
         [response(1, 'Balance of trade', [('formula', 'Formula: Visible Exports minus Visible Imports = Balance of Trade', 3), ('exports', '€4,800m', 3),
                                           ('imports', '€3,700m', 3), ('answer', '€1,100m', 3)])],
         ['Scheme (page 18): ' + S(18, 'Formula: Visible Exports minus Visible Imports = Balance of Trade') + '; workings €4,800m – €3,700m = €1,100m (3 + 3 + 3). The allocation summary prints “'
          + S(7, 'Formula 3m Figures 9m (3 x 3m)') + '”.']))
add(2, 3, 'aii', 'Q3(A)(ii)', figures + '\n\n' + bot_i + '\n' + L(2, 7, '(ii) State whether it is a surplus or a deficit.'), 3, 'business-6-13',
    'trade-surplus-or-deficit-2016', 7, [18], 'State it for 3 marks.', [single('Surplus or deficit', 3, 'Answer stated')], ['Answer: Surplus (scheme page 18).'])
imp_i = L(2, 7, '(B) (i) List two examples of goods imported into Ireland.')
cum(2, 3, 'bi', 'Q3(B)(i)', figures + '\n\n' + imp_i, (3, 3), 'business-6-13', 'imported-goods-examples', 7, [18],
    'Scheme examples (page 18): ' + S(18, 'Cars, Lemons, Oil, Wine.'), noun='examples')
add(2, 3, 'bii', 'Q3(B)(ii)', figures + '\n\n' + imp_i + '\n' + L(2, 7, '(ii) Outline two reasons why goods are imported into Ireland.'), 14, 'business-6-13',
    'reasons-for-importing-2016', 7, [18], 'Two reasons at 7 marks each (5 + 2).', points('Reason', 2, (5, 2)))
open_economy = L(2, 7, 'Ireland is a small open economy which is heavily dependent on international trade.')
add(2, 3, 'c', 'Q3(C)', open_economy + '\n\n' + L(2, 7, '(C) Outline two challenges for Irish businesses involved in international trade.'), 15, 'business-6-13',
    'international-trade-challenges-2016', 7, [18], 'Two challenges: 8 (5 + 3) and 7 (5 + 2).', unequal('Challenge', [(5, 3), (5, 2)], None), [UNTIED])
add(2, 3, 'd', 'Q3(D)', open_economy + '\n\n' + L(2, 7, '(D) Outline two uses of Information and Communications Technology (ICT) in international trade.'), 15, 'business-6-13',
    'ict-uses-international-trade', 7, [19], 'Two uses: 8 (5 + 3) and 7 (5 + 2).', unequal('Use', [(5, 3), (5, 2)], None), [UNTIED], extra=['business-2-12'])
add(2, 3, 'e', 'Q3(E)', open_economy + '\n\n' + L(2, 7, '(E) Outline two advantages to Ireland of being a member of the European Union.'), 10, 'business-6-14',
    'eu-membership-advantages-2016', 7, [19], 'Two advantages at 5 marks each (3 + 2).', points('Advantage', 2, (3, 2)))

sean = L(2, 8, 'Fitness Fanatics') + '\n' + L(2, 8, 'Sean spotted a gap in the market for a Personal Training business in his hometown. Sean used his personal savings to open a fitness studio. Within one year he had over 150 clients in training. Sean hired five full-time personal trainers to help him with the workload. He regularly consults with his staff and values their opinions.')
add(2, 4, 'a', 'Q4(A)', sean + '\n\n' + L(2, 8, '(A) Outline three characteristics/skills of an entrepreneur.'), 15, 'business-1-5', 'entrepreneur-characteristics-2016',
    8, [20], 'Three at 5 marks each (3 + 2).', points('Characteristic', 3, (3, 2)))
add(2, 4, 'b', 'Q4(B)', sean + '\n\n' + L(2, 8, '(B) Outline two risks for Sean of setting up his own business.'), 15, 'business-1-5', 'sean-business-risks',
    8, [20], EIGHT, eight_seven('Risk'), [UNTIED])
add(2, 4, 'c', 'Q4(C)', sean + '\n\n' + L(2, 8, '(C) Explain two features of a democratic leadership style.'), 15, 'business-2-11', 'democratic-leadership-2016',
    8, [20], EIGHT, eight_seven('Feature'), [UNTIED])
add(2, 4, 'd', 'Q4(D)', sean + '\n\n' + L(2, 8, '(D) Outline two benefits of having highly motivated employees.'), 15, 'business-2-11', 'motivated-employees-benefits',
    8, [21], EIGHT, eight_seven('Benefit'), [UNTIED])
add(2, 4, 'e', 'Q4(E)', sean + '\n\n' + L(2, 8, '(E) Outline two advantages of meetings as a method of communication.'), 15, 'business-2-12', 'meetings-advantages',
    8, [21], EIGHT, eight_seven('Advantage'), [UNTIED])

kevin = L(2, 8, 'Kevin’s Garage') + '\n' + L(2, 8, 'Kevin owns a garage and has a recovery truck. He employs seven people. Kevin received his annual insurance bill for the garage. He was disappointed to discover that his insurance premium had increased by 50%. He decided to ‘shop around’, getting online quotes for insurance from several companies. Kevin’s annual motor tax bill for the business was also due for payment. He identified that he would need to arrange a bank overdraft to help with the current financial demands of his business.')
add(2, 5, 'a', 'Q5(A)', kevin + '\n\n' + L(2, 8, '(A) Outline three types of insurance you would expect a business to have.'), 20, 'business-3-17', 'business-insurance-types-2016',
    8, [22], 'Three types: 7 (4 + 3), 7 (4 + 3) and 6 (4 + 2).', unequal('Type of insurance', [(4, 3), (4, 3), (4, 2)], None),
    ['The 7/7/6 sequence prices the three types, not particular types.'])
add(2, 5, 'b', 'Q5(B)', kevin + '\n\n' + L(2, 8, '(B) Outline two actions Kevin could take to reduce his insurance premium.'), 10, 'business-3-17', 'reduce-insurance-premium',
    8, [22], 'Two actions at 5 marks each.', points('Action', 2, (5,)), ['Scheme examples: ' + S(22, 'Install Cameras/CCTV.') + ' ' + S(22, 'Switch insurance provider.')])
add(2, 5, 'c', 'Q5(C)', kevin + '\n\n' + L(2, 8, '(C) List two taxes, other than motor tax, that a business might pay.'), 15, 'business-3-18', 'business-taxes-listed',
    8, [22], 'Two taxes: 8 and 7.', unequal('Tax', [(8,), (7,)], None),
    ['The 8-mark allowance is not tied to a particular tax. Scheme examples: Value Added Tax, Corporation Tax, commercial rates, customs duties, excise duties.'])
S(22, 'Value Added Tax • Corporation Tax • Commercial Rates, Water Rates • Custom Duties')
add(2, 5, 'd', 'Q5(D)', kevin + '\n\n' + L(2, 8, '(D) Explain the term bank overdraft.'), 10, 'business-3-16', 'bank-overdraft-explained', 8, [23],
    'Explanation: 10 marks (5 + 5).', [comps('Bank overdraft', (5, 5))], ['Scheme: ' + S(23, 'A bank overdraft is a short term source of finance.')])
add(2, 5, 'e', 'Q5(E)', kevin + '\n\n' + L(2, 8, '(E) Explain three factors that a bank would consider before giving a loan to a business.'), 20, 'business-3-16', 'bank-loan-factors',
    8, [23], 'Three factors: 7 (4 + 3), 7 (4 + 3) and 6 (4 + 2).', unequal('Factor', [(4, 3), (4, 3), (4, 2)], None),
    ['The 7/7/6 sequence prices the three factors, not particular factors.'])

advert = '\n'.join([L(2, 9, 'Tech Tastic Digital Marketing Agency Seeks Digital Marketing Consultant'),
                    L(2, 9, 'Tech Tastic Digital Marketing Agency is a Digital Marketing and IT business, involved in the promotion of products or brands through one or more forms of electronic media. We have a current staff of nine. We are looking for a Digital Marketing Consultant to join our team in Dublin.'),
                    L(2, 9, 'The position: involves meeting with clients to identify and understand their needs. Responsibilities include listening to the clients and then creating digital marketing campaigns to promote the clients’ products and services.'),
                    L(2, 9, 'The ideal candidate: must have a relevant degree in Business, three years’ experience in digital marketing, excellent interpersonal and communication skills and the ability to work as part of a team. Rewards are negotiable.'),
                    L(2, 9, 'Apply online: www.techtasticdigitalmarketingagency.com before 24th June 2016.')])
add(2, 6, 'a', 'Q6(A)', advert + '\n\n' + L(2, 9, '(A) Explain the difference between internal recruitment and external recruitment.'), 20, 'business-3-20',
    'internal-versus-external-recruitment', 9, [24], 'Each type 10 marks (4 + 3 + 3).',
    [comps('Internal recruitment', (4, 3, 3), i=1), comps('External recruitment', (4, 3, 3), i=2)],
    ['Scheme: ' + S(24, 'Internal recruitment means finding someone from among those who already work in the business.') + ' '
     + S(24, 'External recruitment means finding someone who does not already work in the business.')])
terms = L(2, 9, '(B) Explain the following terms with reference to the above advertisement:')
add(2, 6, 'bi', 'Q6(B)(i)', advert + '\n\n' + terms + '\n' + L(2, 9, '(i) Job description'), 10, 'business-3-20', 'job-description-with-reference',
    9, [24], 'Explanation: 10 marks (4 + 3 + 3).', [comps('Job description', (4, 3, 3))],
    ['Scheme: ' + S(24, 'This document shows details of the position/vacancy to be filled, including the job title, work details, duties and responsibilities of the job, conditions of employment and place of work.')])
add(2, 6, 'bii', 'Q6(B)(ii)', advert + '\n\n' + terms + '\n' + L(2, 9, '(ii) Person specification.'), 10, 'business-3-20', 'person-specification-with-reference',
    9, [24], 'Explanation: 10 marks (4 + 3 + 3).', [comps('Person specification', (4, 3, 3))],
    ['Scheme: ' + S(24, 'This describes the qualities that the successful candidate for the job should have.')])
add(2, 6, 'c', 'Q6(C)', advert + '\n\n' + L(2, 9, '(C) Explain the difference between ‘on the job training’ and ‘off the job training’.'), 10, 'business-3-20',
    'on-versus-off-the-job-training', 9, [24], 'Each type 5 marks (3 + 2).', [comps('On the job training', (3, 2), i=1), comps('Off the job training', (3, 2), i=2)],
    ['Scheme: ' + S(24, 'Off-the-job training: This means training that takes place outside the work place, usually with specialist trainers.')])
add(2, 6, 'd', 'Q6(D)', advert + '\n\n' + L(2, 9, '(D) Outline three types of rewards for employees.'), 15, 'business-3-20', 'employee-reward-types',
    9, [25], 'Three types at 5 marks each (3 + 2).', points('Reward', 3, (3, 2)), extra=['business-2-11'])
cum(2, 6, 'e', 'Q6(E)', advert + '\n\n' + L(2, 9, '(E) List two methods of advertising job vacancies.'), (5, 5), 'business-3-20', 'job-vacancy-advertising-methods',
    9, [25], 'Scheme examples (page 25): company website, newspapers, trade magazines, recruitment agencies and websites, LinkedIn, social media, word of mouth, head-hunting, shop window.',
    noun='methods')
S(25, 'Website – on the company website • Newspapers • Trade Magazines')

theo = L(2, 10, 'Theo’s Mexican Street Food') + '\n' + L(2, 10, 'Theo had many years of experience working as a chef in Mexican food restaurants. He noticed how popular food trailers had become when attending various music festivals. Theo conducted market research and decided to open his own food trailer selling authentic Mexican food. He purchased a jeep and a food trailer. The brand name, Theo’s Mexican Street Food, now has an excellent reputation for high quality affordable food. Theo communicates his sales promotions through social media such as Facebook and Twitter.')
add(2, 7, 'a', 'Q7(A)', theo + '\n\n' + L(2, 10, '(A) Explain three sources of new product/service ideas for a business.'), 15, 'business-4-14', 'new-idea-sources-2016',
    10, [26], 'Three sources at 5 marks each (3 + 2).', points('Source', 3, (3, 2)))
add(2, 7, 'b', 'Q7(B)', theo + '\n\n' + L(2, 10, '(B) Outline two reasons why a business would carry out market research.'), 15, 'business-4-16', 'market-research-reasons',
    10, [26], EIGHT, eight_seven('Reason'), [UNTIED])
add(2, 7, 'c', 'Q7(C)', theo + '\n\n' + L(2, 10, '(C) Outline two medium term sources of finance that Theo could have used to purchase the jeep and food trailer.'), 10, 'business-3-16',
    'medium-term-sources-theo', 10, [26], 'Two sources at 5 marks each (3 + 2).', points('Source', 2, (3, 2)),
    ['Scheme: ' + S(26, 'Medium Term Loan: borrowing money from the bank and paying it back in regular instalments over a period up to 5 years.') + ' '
     + S(26, 'Hire Purchase: buying an asset and paying for it instalments.')])
brand_i = L(2, 10, '(D) (i) List two examples of well-known brand names.')
cum(2, 7, 'di', 'Q7(D)(i)', theo + '\n\n' + brand_i, (4, 4), 'business-4-17', 'well-known-brand-names', 10, [27],
    'Scheme examples (page 27): ' + S(27, 'Apple, Nike, Tayto, Costa.'), noun='brand names')
add(2, 7, 'dii', 'Q7(D)(ii)', theo + '\n\n' + brand_i + '\n' + L(2, 10, '(ii) Outline two benefits of a brand name for a business.'), 12, 'business-4-17',
    'brand-name-benefits', 10, [27], 'Two benefits at 6 marks each.', points('Benefit', 2, (6,)),
    ['Scheme examples: ' + S(27, 'Product is more recognisable.') + ' ' + S(27, 'Creates brand loyalty.')])
add(2, 7, 'e', 'Q7(E)', theo + '\n\n' + L(2, 10, '(E) Describe two sales promotions that Theo’s Mexican Street Food could offer consumers to increase sales.'), 15, 'business-4-17',
    'theo-sales-promotions', 10, [27], EIGHT, eight_seven('Sales promotion'), [UNTIED])

dolly = L(2, 11, 'Dolly’s Delicious Delights') + '\n' + L(2, 11, 'Baking was always a hobby for Dolly O’Brien until she won the Great Irish Bake Off in 2015. She decided to operate as a sole trader. Dolly uses a batch production system to produce cakes and buns. She sells her products direct to her consumers at farmers’ markets. Dolly decided to make customised wedding cakes as a new product. She introduced her wedding cakes to her target market at wedding fairs.')
sole_i = L(2, 11, '(A) (i) Explain the term sole trader.')
add(2, 8, 'ai', 'Q8(A)(i)', dolly + '\n\n' + sole_i, 5, 'business-5-14', 'sole-trader-explained-2016', 11, [28], 'Explanation: 5 marks (3 + 2).',
    [comps('Sole trader', (3, 2))], ['Scheme: ' + S(28, 'A person who owns and runs his/her own business.')])
add(2, 8, 'aii', 'Q8(A)(ii)', dolly + '\n\n' + sole_i + '\n' + L(2, 11, '(ii) Outline two benefits for Dolly of being a sole trader.'), 10, 'business-5-14',
    'dolly-sole-trader-benefits', 11, [28], 'Two benefits at 5 marks each.', points('Benefit', 2, (5,)))
batch_i = L(2, 11, '(B) (i) Outline two features of batch production.')
add(2, 8, 'bi', 'Q8(B)(i)', dolly + '\n\n' + batch_i, 10, 'business-4-15', 'batch-production-features', 11, [28], 'Two features at 5 marks each (3 + 2).',
    points('Feature', 2, (3, 2)), ['Scheme examples: ' + S(28, 'A limited amount of identical goods is manufactured at the same time.')])
cum(2, 8, 'bii', 'Q8(B)(ii)', dolly + '\n\n' + batch_i + '\n' + L(2, 11, '(ii) List the two other types of production used in business.'), (5, 5), 'business-4-15',
    'other-production-types-listed', 11, [28], 'Answer key (scheme page 28): ' + S(28, 'Job Production Mass Production').replace(' Mass', ' and Mass') + '.', noun='types')
add(2, 8, 'c', 'Q8(C)', dolly + '\n\n' + L(2, 11, '(C) Outline three factors that Dolly should consider when setting the price of her products.'), 20, 'business-4-17',
    'dolly-pricing-factors', 11, [29], 'Three factors: 7 (4 + 3), 7 (4 + 3) and 6 (4 + 2).', unequal('Factor', [(4, 3), (4, 3), (4, 2)], None),
    ['The 7/7/6 sequence prices the three factors, not particular factors.'])
add(2, 8, 'd', 'Q8(D)', dolly + '\n\n' + L(2, 11, '(D) Explain the term target market.'), 10, 'business-4-16', 'target-market-explained-2016', 11, [29],
    'Explanation: 10 marks (5 + 5).', [comps('Target market', (5, 5))], ['Scheme: ' + S(29, 'A target market is the group of people at whom a particular product or service is aimed.')])
add(2, 8, 'e', 'Q8(E)', dolly + '\n\n' + L(2, 11, '(E) Explain the term channels of distribution.'), 10, 'business-4-17', 'channels-of-distribution-explained', 11, [29],
    'Explanation: 10 marks (5 + 5).', [comps('Channels of distribution', (5, 5))],
    ['Scheme: ' + S(29, 'Channels of Distribution refer to the method by which a product gets from the producer/manufacturer to the consumer.')])

# ---------------------------------------------------------------- checks and write-out
qn = lambda c: c['questionRef'].split(' Q')[1].split('(')[0]
for section, count, total in [('1', 15, 10), ('2', 8, 75)]:
    for q in range(1, count + 1):
        got = sum(c['totalMarks'] for c in P.created if c['section'] == section and qn(c) == str(q))
        assert got == total, (section, q, got)
assert not [i for i in ORIGINAL if i.startswith('bus-2016-ol-')]
assert not P.pools

SELECTION = {
    1: 'No finite printed answer menu occurs in Section 1 (answer ten of fifteen at 10 marks). The word bank in Q7, TRUE/FALSE in Q10, the tick in Q11, the missing stages in Q14 and the matching rows in Q15 are required answer formats. Support-note lists are open examples.',
    2: 'No printed choice of task occurs in Section 2. Sub-parts with their own published marks are separate cards. Support-note lists are open examples.',
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
    if m == 'Choose' and own(w, m, 'Choose the appropriate words'):
        return 'required-headings', 'Section 1 Q7 is a word-bank completion: both blanks are required and the printed words are the answer options, not optional tasks.', None
    if m == 'or' and own(w, m, 'TRUE or FALSE'):
        return 'required-headings', 'TRUE/FALSE are answer labels for each of the five required statements in Section 1 Q10, not optional tasks.', None
    if m == 'or' and own(w, m, 'surplus or a deficit'):
        return 'required-headings', 'Section 2 Q3(A)(ii) requires a determination of surplus or deficit; it is one required answer, not a choice of task.', None
    if m == 'or' and own(w, m, 'two or more parties'):
        return 'case-context', '“two or more parties” is wording inside explanation D of the Section 1 Q15 matching table, not a choice of task.', None
    if m == 'or' and (own(w, m, 'products or brands') or own(w, m, 'one or more forms')):
        return 'case-context', 'Wording inside the Section 2 Q6 advertisement, not a choice of task.', None
    assert (fileid, page) in {('LC033GLP000EV', 1), ('LC033GLP000EV', 6)} and m in ('either', 'or'), (fileid, page, m, w)
    return 'exam-navigation', 'The cover and Section 2 rubrics set how many whole questions a candidate answers (one from Part 1, two from Part 2 and one other from either part). Every numbered question remains in the practice corpus as separate cards.', None


n = P.write([(1, range(1, 16)), (2, range(1, 9))], SELECTION, classify,
            'Every part of {year} Ordinary Section {section} Question {q} was visually checked against its SEC paper, allocation summary and support notes. The single-booklet identity keeps the short (n) and long (S2Q) question numbering apart.')
print(f'Reviewed {len(P.created)} 2016 Ordinary tasks; classified {n} raw selection matches.')
