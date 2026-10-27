"""Review the 2018 Ordinary English paper (one booklet: Section 1 and Section 2).

2018: answer ten of fifteen short questions at 10 marks and four of eight
long questions at 75 (one from Part 1, two from Part 2 and one other), all in
one booklet (LC033GLP000EV, the same file id as its scheme). No Ordinary card
existed for 2018, so every card is new. The allocation summary (scheme pages
4-7) sets each boundary. Where it and the expected-responses page disagree the
card says so: Section 1 Q4 follows the summary (5 + 5, not 6 + 4); Section 2
Q1(C) follows the expected responses (3, 6 and 6), because the summary's
"two explanations @ 6" would exceed the 15 printed for (C). Three printed
choices are one card each: Q5(A) any four of five underlined insurance terms,
Q5(D) any three of four underlined recruitment terms and Q8(C) any three of
four sources of finance (the scheme marks every choice alike).
"""
from bus_lib import (Paper, ORIGINAL, comps, points, seq, unequal, single, response, fixed, permit)

T = {(1, q): 4 for q in range(1, 16)}
T.update({(2, 1): 5, (2, 2): 5, (2, 3): 6, (2, 4): 6, (2, 5): 6, (2, 6): 7, (2, 7): 7, (2, 8): 7})
P = Paper(2018, 'ordinary', {1: 'LC033GLP000EV', 2: 'LC033GLP000EV'}, 'LC033GLP000EV', T)
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


def bullets(text):
    return text.replace('• ', '').strip()


# ---------------------------------------------------------------- Section 1 (10 marks each)
add(1, 1, '', 'Q1', L(1, 2, 'What do the following letters stand for? Write each answer in the space provided.', 'DIRT PIN PAYE').replace(' PIN', '\nPIN').replace(' PAYE', '\nPAYE'),
    10, 'business-3-18', 'abbreviations-dirt-pin-paye', 2, [8], 'The first correct term earns 4 (1 + 1 + 1 + 1); the second and third 3 each (1 + 1 + 1).',
    [comps('First correct term', (4,), ['Words written in full'], 1), comps('Second correct term', (3,), ['Words written in full'], 2),
     comps('Third correct term', (3,), ['Words written in full'], 3)],
    ['Answer key: DIRT ' + S(8, 'Deposit Interest Retention Tax') + '; PIN ' + S(8, 'Personal Identification Number') + '; PAYE ' + S(8, 'Pay As You Earn') + '.'])
cum(1, 2, '', 'Q2', L(1, 2, 'Indicate whether each of the following is an example of intrapreneurship or entrepreneurship by writing INTRAPRENEUR or ENTREPRENEUR after each of the following statements.',
                      'An employee at Sony coming up with the idea for the Sony Playstation.',
                      'Two Stanford University graduates set up a photo sharing app business known as Snapchat.',
                      'An employee at Facebook coming up with the idea of the like button as a method of communicating that you like a post or photograph.',
                      'An employee at Google coming up with the idea for an email service, which became known as Gmail.',
                      'Irish fashion and beauty blogger, Pippa O’Connor, launching her own range of jeans.'),
    (2, 2, 2, 2, 2), 'business-1-5', 'intrapreneur-or-entrepreneur', 2, [8],
    'Answer key (scheme page 8): Sony Intrapreneur; Snapchat (the Stanford graduates) Entrepreneur; Facebook Intrapreneur; Google Intrapreneur; Pippa O’Connor Entrepreneur ('
    + S(8, 'Sony Intrapreneur Stanford Univ. Entrepreneur Facebook Intrapreneur Google Intrapreneur O’Connor Entrepreneur') + ').', noun='statements')
add(1, 3, '', 'Q3', L(1, 2, 'The Irish government privatised Bord Gáis in 2014. Explain the term privatisation.'), 10, 'business-5-14', 'privatisation-explained',
    2, [8], 'Explanation: 10 marks (4 + 3 + 3).', [comps('Privatisation', (4, 3, 3))],
    ['Scheme: ' + S(8, 'Privatisation refers to the sale of a state-owned company by the government to a privately-owned firm.') + ' '
     + S(8, 'It involves the transfer of ownership of a public enterprise to private owners.')])
add(1, 4, '', 'Q4', L(1, 3, 'Choose the appropriate words to complete the sentence below. (Two words do not apply.)', 'MERGER; FRANCHISE; STRATEGIC ALLIANCE; TAKEOVER.')
    + '\nA ______ ' + L(1, 3, 'involves two businesses voluntarily joining together to form a single business, while a')
    + ' ______ ' + L(1, 3, 'involves two businesses working together on a specific project without any change of ownership.'),
    10, 'business-4-18', 'merger-and-strategic-alliance-word-bank', 3, [8], 'Each blank earns 5 marks.',
    [fixed('Completed blanks', [('First blank', 5), ('Second blank', 5)])],
    ['Answer key (scheme page 8): ' + S(8, 'A MERGER involves two businesses voluntarily joining together to form a single business, while a STRATEGIC ALLIANCE involves')
     + ' ... Franchise and Takeover are not used.',
     'The allocation summary (scheme page 4) prints “' + S(4, 'Two words: @ 5m each') + '”; the expected-responses page prints 6 + 4. The card follows the summary.'])
cum(1, 5, '', 'Q5', L(1, 3, 'Fill in the missing elements of a SWOT analysis in the spaces 2, 3 and 4 in the table below.') + '\n' + L(1, 3, '1. Strengths') + '\n2. ______\n3. ______\n4. ______',
    (4, 3, 3), 'business-2-13', 'swot-missing-elements', 3, [8], 'Answer key (scheme page 8): ' + S(8, '1. Strengths 2. Weaknesses 3. Opportunities 4. Threats') + '.', noun='elements')
L(1, 3, 'Name: Joanne Heffernan', 'Gross Pay 70,000', 'PAYE (20% of €34,550) (40% of €35,450) - Tax Credits 6910 14180 21090 21090 -4200 Net PAYE 16890',
  'PRSI (4% of €70,000) (i) USC (3% of €70,000) (ii) Total Deductions (iii) Net Annual Take Home Pay (iv)')
flat(add(1, 6, '', 'Q6', L(1, 3, 'Calculate Joanne Heffernan’s net annual take home pay from the following details.', 'Show your workings in the spaces provided.')
         + '\nName: Joanne Heffernan\nGross Pay €70,000\nDeductions\nPAYE (20% of €34,550) 6910; (40% of €35,450) 14180; 21090\n- Tax Credits -4200\nNet PAYE 16890'
         + '\nPRSI (4% of €70,000) (i)\nUSC (3% of €70,000) (ii)\nTotal Deductions (iii)\nNet Annual Take Home Pay (iv)',
         10, 'business-3-18', 'net-annual-take-home-pay', 3, [8], 'PRSI 3 (2 + 1 for the workings), USC 3 (2 + 1), total deductions 2 and take home pay 2.',
         [response(1, 'Net annual take home pay', [('prsi', '(i) PRSI €2,800', 2), ('prsi-workings', 'PRSI workings: 70,000 x 4 / 100', 1),
                                                   ('usc', '(ii) USC €2,100', 2), ('usc-workings', 'USC workings: 70,000 x 3 / 100', 1),
                                                   ('total', '(iii) Total Deductions €21,790', 2), ('net', '(iv) Take Home Pay €48,210', 2)])],
         ['Scheme (page 8): ' + S(8, '(i) PRSI €2,800 (70,000 x 4 / 100) (ii) USC €2,100 (70,000 x 3 / 100) (iii) Total Deductions €21,790 (iv) Take Home Pay €48, 210')
          + ' (2 + 1, 2 + 1, 2, 2). The allocation summary prints “' + S(4, 'Four calculations: 3m + 3m + 2m + 2m') + '”.']))
cum(1, 7, '', 'Q7', L(1, 4, 'Write TRUE or FALSE after each of the following statements.', 'Tax paid on company profits is known as capital gains tax.',
                      '‘Span of control’ refers to the number of employees who report to a superior.', 'Interest groups lobby governments on behalf of their members.',
                      'A Trade Union represents consumers who have a dispute with a retailer.'),
    (3, 3, 2, 2), 'business-0-12', 'mixed-true-false-2018', 4, [9],
    'Answer key (scheme page 9): FALSE; TRUE; TRUE; FALSE (' + S(9, 'Tax on company profits FALSE Span of control TRUE Interest groups TRUE Trade Union FALSE') + ').',
    extra=['business-3-18', 'business-2-13', 'business-0-14'])
add(1, 8, '', 'Q8', L(1, 4, 'Outline two types of official industrial action a trade union can take as part of an industrial relations dispute.'), 10, 'business-0-14',
    'official-industrial-action-types', 4, [9], 'Two types at 5 marks each (3 + 2).', points('Type', 2, (3, 2)),
    ['Scheme examples: ' + S(9, 'Official Strike – employees do not enter their workplace and refuse to perform their work duties.') + ' '
     + S(9, 'Work-to-rule – where employees only undertake the exact jobs written in their job description/contract of employment.') + ' Overtime ban / go slow; token stoppage.'])
add(1, 9, '', 'Q9', L(1, 4, 'Draft, using today’s date, a Memorandum (Memo) from Mary Moore, IT manager, to all department managers reminding them to inform all staff of the importance of protecting sensitive data from cyber security threats.')
    + '\n' + L(1, 4, 'MEMORANDUM To: From: Date: Re: Signed: Title:').replace(' To:', '\nTo:').replace(' From:', ' / From:').replace(' Date:', ' / Date:').replace(' Re:', ' / Re:').replace(' Signed:', ' / Signed:').replace(' Title:', ' / Title:'),
    10, 'business-2-12', 'cyber-security-memorandum', 4, [9], 'Seven entries: To, Date and the message at 2 each; From, Re, Signed and Title at 1 each.',
    [fixed('Memorandum', [('To', 2), ('From', 1), ('Date', 2), ('Re', 1), ('Message', 2), ('Signed', 1), ('Title', 1)])],
    ['Scheme (page 9): To ' + S(9, 'All Department Managers') + '; From Mary Moore; Date 14th June 2018; Re ' + S(9, 'Data Security')
     + '; Signed Mary Moore; Title IT Manager. The allocation summary prints “' + S(4, 'Seven entries: 3 @ 2m each plus 4 @ 1m each') + '”.'])
add(1, 10, '', 'Q10', L(1, 5, 'Describe, using an example, what is meant by a multinational company.'), 10, 'business-6-15', 'multinational-described-with-example',
    5, [10], 'Explanation 7 (4 + 3) and an example 3.', [comps('Multinational company', (4, 3, 3), ['Explanation', 'Explanation developed', 'Example'])],
    ['Scheme: ' + S(10, 'A multinational company is a business with headquarters in one country but company offices/locations in other countries throughout the world.')])
add(1, 11, '', 'Q11', L(1, 5, 'In the context of a meeting explain the terms agenda and minutes.') + '\nAgenda:\nMinutes:', 10, 'business-2-12', 'agenda-and-minutes',
    5, [10], 'Each term 5 marks (3 + 2).', [comps('Agenda', (3, 2), i=1), comps('Minutes', (3, 2), i=2)],
    ['Scheme: ' + S(10, 'An agenda is a list of the items to be discussed at a meeting.') + ' ' + S(10, 'The minutes of a meeting are a written record of what happened at a meeting.')])
cum(1, 12, '', 'Q12', L(1, 5, 'List the three other factors of production:') + '\n______ | ' + L(1, 5, 'LABOUR') + ' | ______ | ______', (4, 3, 3), 'business-1-5',
    'other-factors-of-production', 5, [10], 'Answer key (scheme page 10): Land, Capital and Enterprise (' + S(10, 'LAND Labour CAPITAL ENTERPRISE') + '; Labour is printed).',
    noun='factors')
cum(1, 13, '', 'Q13', L(1, 5, 'The aim of Public Relations (PR) is to maintain the good image of a business. In the spaces provided below, indicate which of the following PR methods is being used in each case: Celebrity Endorsement, Sponsorship, Press Release.')
    + '\n' + L(1, 5, 'Vodafone and the Irish Rugby team is an example of') + ' ______.\n' + L(1, 5, 'David Beckham and H&M Store is an example of') + ' ______.\n'
    + L(1, 5, 'Apple used a') + ' ______ ' + L(1, 5, 'to announce the launch of the iPhone X.'),
    (4, 3, 3), 'business-4-17', 'public-relations-methods', 5, [10],
    'Answer key (scheme page 10): ' + S(10, 'Vodafone and Irish Rugby Team: Sponsorship David Beckham and H&M Store: Celebrity Endorsement Apple announcement: Press Release') + '.', noun='methods')
cum(1, 14, '', 'Q14', L(1, 6, 'Indicate by placing a tick (✓) in the correct box, the type of plan to which each statement for Ben and Jerry’s ice cream relates.',
                        'Strategic Plan Tactical Plan Mission Statement Contingency Plan',
                        'Ben & Jerry’s aim is to create linked prosperity for everyone connected to their business: suppliers, farmers, franchisees, customers and neighbours.',
                        'Ben & Jerry’s aim is to continue expanding its product range and its locations over the next 10 years.',
                        'Ben & Jerry’s will switch to non-dairy sources for their ice-creams in the event of a milk shortage.',
                        'Ben & Jerry’s will expand its vegan range of ice-cream in the next 6 months.'),
    (3, 3, 2, 2), 'business-2-13', 'plan-type-ticks', 6, [10],
    'Answer key (ticks on scheme page 10): linked prosperity Mission Statement; expanding over the next 10 years Strategic Plan; non-dairy sources in a milk shortage Contingency Plan; vegan range in the next 6 months Tactical Plan.',
    noun='ticks')
cum(1, 15, '', 'Q15', '\n'.join([L(1, 6, 'Column 1 is a list of terms used in international trade. Column 2 is a list of explanations for these terms. Match the two lists by placing the letter of the correct explanation under the relevant number below. One explanation has no match.'),
                                 L(1, 6, '1. Trading Bloc', '2. Regulation', '3. Embargo', '4. Quota', '5. Tariff'),
                                 L(1, 6, 'A. A European Union law which must be implemented in each EU country immediately.',
                                   'B. A limit to the amount of a particular product which can be imported into a country.',
                                   'C. The treatment of the world as one single market by global firms.', 'D. A tax on imported goods and services.',
                                   'E. A group of countries that trade freely with each other – there are no barriers to trade between these countries.',
                                   'F. A ban on a particular product being imported into a country.')]),
    (3, 3, 2, 1, 1), 'business-6-13', 'international-trade-terms-matching', 6, [10], 'Answer key (scheme page 10): 1 E; 2 A; 3 F; 4 B; 5 D. Explanation C is unused.',
    extra=['business-6-14'], noun='matches')
S(10, '1. 2. 3. 4. 5. E A F B D')

# ---------------------------------------------------------------- Section 2 (75 marks each)
stake = L(2, 7, 'Stakeholders and Relationships', 'Stakeholders refer to different groups of people who are directly affected by the decisions that a business makes. A stakeholder has an interest in the success of a business.')
add(2, 1, 'a', 'Q1(A)', stake + '\n\n' + L(2, 7, '(A) In relation to the following stakeholders of a business:', '(i) explain the term employee', '(ii) explain the term manager.'),
    15, 'business-0-12', 'employee-and-manager-explained', 7, [11], 'Two explanations: 8 (4 + 4) and 7 (4 + 3).', unequal('Explanation', [(4, 4), (4, 3)], None),
    ['The 8-mark allowance is not tied to either term.',
     'Scheme: ' + S(11, 'An employee is an individual who works for an employer in the production of goods or services in return for a fee called wages or salary.') + ' '
     + S(11, 'A manager is a person who is responsible for controlling or running or administering an organisation or group of staff.')])
add(2, 1, 'b', 'Q1(B)', stake + '\n\n' + L(2, 7, '(B) Describe the relationship that the following stakeholders may have with a business: (i) an investor and (ii) a supplier.'),
    15, 'business-0-12', 'investor-and-supplier-relationships', 7, [11], 'Two explanations: 8 (4 + 4) and 7 (4 + 3).', unequal('Relationship', [(4, 4), (4, 3)], None),
    ['The 8-mark allowance is not tied to either stakeholder.',
     'Scheme: ' + S(11, 'An investor provides the finance/capital required by the business/entrepreneur.') + ' '
     + S(11, 'A supplier provides raw materials, components and finished goods to the business.')])
add(2, 1, 'c', 'Q1(C)', stake + '\n\n' + L(2, 7, '(C) If a consumer purchases a faulty product, who is responsible – the retailer or the producer? Explain your answer and name the law that protects the consumer in this case.'),
    15, 'business-0-13', 'faulty-product-responsibility', 7, [12], 'Who is responsible 3, the explanation 6 (3 + 3) and the consumer law 6.',
    seq(single('Who is responsible', 3, 'Responsibility stated'), comps('Explanation', (3, 3)), comps('Consumer law', (6,), ['Law named'])),
    ['Scheme (page 12): ' + S(12, 'The Retailer is responsible.') + ' ' + S(12, 'When you, the consumer, purchase products from a retailer, you make a contract with the retailer (not the producer).')
     + ' ' + S(12, 'Relevant Consumer Law – Sale of Goods & Supply of Services Act 1980.'),
     'The allocation summary (scheme page 5) prints “' + S(5, 'Two explanations: @ 6 marks each (3m + 3m)') + '”, which would exceed the 15 printed for (C); the expected-responses page prints 3, 6 (3 + 3) and 6, and the card follows it.'])
add(2, 1, 'd', 'Q1(D)', L(2, 7, 'The Small Claims Court procedure can be used to resolve consumer complaints.') + '\n\n' + L(2, 7, '(D) Outline two advantages for a consumer of taking a case to the Small Claims Court.'),
    15, 'business-0-13', 'small-claims-court-advantages', 7, [12], EIGHT, eight_seven('Advantage'), [UNTIED])
cum(2, 1, 'e', 'Q1(E)', L(2, 7, 'When employees believe they have been treated unfairly in the workplace, they can make a complaint through the Workplace Relations Commission. Laws such as the Employment Equality Act and the Unfair Dismissals Act exist to protect employee rights.')
    + '\n\n' + L(2, 7, '(E) List four grounds on which discrimination in the workplace is outlawed.'), (4, 4, 4, 3), 'business-0-14', 'discrimination-grounds-listed', 7, [12],
    'Scheme grounds (page 12): ' + bullets(S(12, '• Gender • Age • Religious beliefs • Sexual Orientation • Disability • Marital Status • Family Status • Race • Membership of Travelling Community.')).replace(' Age', ', Age').replace(' Religious', ', Religious').replace(' Sexual', ', Sexual').replace(' Disability', ', Disability').replace(' Marital', ', Marital').replace(' Family', ', Family').replace(' Race', ', Race').replace(' Membership', ', Membership'),
    noun='grounds')

jsk = L(2, 8, 'JSK Construction Ltd') + '\n' + L(2, 8, 'JSK Construction Ltd is an Irish construction business currently building a new housing estate in Kildare. Market research identified that a large number of people in the local area are employed by multinationals. Over 60 people will be employed during the construction of the new homes. JSK Construction Ltd promote themselves as an ethical business that “does the right thing for customers, employees and the environment”.')
sector_i = L(2, 8, '(A) (i) Name the sector of the economy that JSK Construction Ltd operates in.')
add(2, 2, 'ai', 'Q2(A)(i)', jsk + '\n\n' + sector_i, 5, 'business-5-13', 'jsk-sector', 8, [13], 'Name the sector for 5 marks.',
    [single('Sector', 5, 'Sector named')], ['Answer: ' + S(13, 'Secondary Sector.')])
add(2, 2, 'aii', 'Q2(A)(ii)', jsk + '\n\n' + sector_i + '\n' + L(2, 8, '(ii) Explain one other sector of the economy and provide one example of an occupation in that sector.'), 10,
    'business-5-13', 'other-sector-and-occupation', 8, [13], 'Name the other sector 2, explain it 4 (2 + 2) and give an occupation 4.',
    [comps('Other sector', (2, 2, 2, 4), ['Sector named', 'Explained', 'Explanation developed', 'Occupation example'])],
    ['Scheme: ' + S(13, 'Primary Sector: Also known as the Extractive industries, it involves extracting raw materials from natural resources.') + ' '
     + S(13, 'Tertiary Sector: This is the services sector, which provides all other industries with a wide range of services.') + ' Occupations: '
     + S(13, 'Farmer/Farming/Agriculture, Fishermen/Fishing, Forestry, Mining.') + ' ' + S(13, 'Hairdresser, taxi driver, financial services, retailing, telecommunications.')])
add(2, 2, 'b', 'Q2(B)', jsk + '\n\n' + L(2, 8, '(B) Outline two benefits of JSK Construction Ltd to the local economy.'), 15, 'business-5-16', 'construction-benefits-local-economy',
    8, [13], EIGHT, eight_seven('Benefit'), [UNTIED])
add(2, 2, 'c', 'Q2(C)', jsk + '\n\n' + L(2, 8, '(C) Outline three reasons why multinational companies decide to locate in Ireland.'), 20, 'business-6-15', 'why-mncs-locate-in-ireland-2018',
    8, [14], 'Three reasons: 7 (5 + 2), 7 (5 + 2) and 6 (5 + 1).', unequal('Reason', [(5, 2), (5, 2), (5, 1)], None),
    ['The 7/7/6 sequence prices the three reasons, not particular reasons.'])
add(2, 2, 'd', 'Q2(D)', jsk + '\n\n' + L(2, 8, '(D) Outline two examples of ethical behaviour by a business.'), 15, 'business-5-17', 'ethical-behaviour-examples',
    8, [14], EIGHT, eight_seven('Example'), [UNTIED])
add(2, 2, 'e', 'Q2(E)', jsk + '\n\n' + L(2, 8, '(E) Explain the term limited liability.'), 10, 'business-5-14', 'limited-liability-explained', 8, [14],
    'Explanation: 10 marks (5 + 5).', [comps('Limited liability', (5, 5))],
    ['Scheme: ' + S(14, 'Limited Liability means that if a company goes bankrupt the owners of the company are not personally responsible for all the debts of the company')])

trade = L(2, 8, 'Irish International trade', 'The value of total exports for the month of March 2017 rose to €11 billion. At the same time, the value of total imports for the month of March fell to €5.8 billion.') + ' (' + L(2, 8, 'Source 1 – www.irishtimes.com') + ')'
exporters = (L(2, 8, 'The Worlds Biggest Exporters (% Share of Global Exports)') + ' (bar chart, 0 to 18): ' + L(2, 8, 'China EU USA Japan S Korea Canada Mexico')
             + ' — read the bars on the printed page. (' + L(2, 8, 'Source 2 – www.independent.ie') + ')')
L(2, 8, '0 2 4 6 8 10 12 14 16 18 China')
bop_i = L(2, 8, '(A) (i) From the information provided in Source 1 calculate the Balance of Payments for March.')
flat(add(2, 3, 'ai', 'Q3(A)(i)', trade + '\n\n' + bop_i, 10, 'business-6-13', 'balance-of-payments-march-2017', 8, [15],
         'Show your workings (the paper prints this at the end of (A)): method 2, exports 2, imports 2 and the balance 4.',
         [response(1, 'Balance of payments', [('method', 'Total Exports minus Total Imports', 2), ('exports', 'Total Exports €11.0 billion', 2),
                                              ('imports', 'Total Imports €5.8 billion', 2), ('answer', 'Balance of Payments: €5.2 billion', 4)])],
         ['Scheme (page 15): ' + S(15, 'Total Exports €11.0 billion minus Total Imports €5.8 billion = Balance of Payments: €5.2 billion') + ' (2 + 2 + 2, 4).']))
add(2, 3, 'aii', 'Q3(A)(ii)', trade + '\n\n' + bop_i + '\n' + L(2, 8, '(ii) State whether it is a surplus or a deficit. Show your workings.'), 5, 'business-6-13',
    'payments-surplus-or-deficit-2018', 8, [15], 'State it for 5 marks.', [single('Surplus or deficit', 5, 'Answer stated')], ['Answer: ' + S(15, 'Surplus or Deficit: Surplus') + '.'])
add(2, 3, 'b', 'Q3(B)', L(2, 8, '(B) Explain, using an example in each case, the difference between visible exports and visible imports.'), 15, 'business-6-13',
    'visible-exports-versus-imports', 8, [15], 'Explanations 5 (3 + 2) and 4 (2 + 2), and an example for each at 3.',
    unequal('Explanation and example', [(3, 2, 3), (2, 2, 3)], ['Explanation', 'Explanation developed', 'Example']),
    ['The 5-mark explanation is not tied to exports or imports.',
     'Scheme: ' + S(15, 'Visible Exports are physical goods sold by businesses based in Ireland to customers in other countries') + '. '
     + S(15, 'Visible Imports are physical goods that are purchased by Irish customers from businesses based in foreign countries.')])
c_intro = L(2, 8, '(C) From the information provided in Source 2,')
c_i = L(2, 8, '(i) Identify the country that has the largest percentage share of global exports.')
add(2, 3, 'ci', 'Q3(C)(i)', exporters + '\n\n' + c_intro + '\n' + c_i, 8, 'business-6-13', 'largest-global-exporter', 8, [15], 'Identify the country for 8 marks.',
    [single('Country', 8, 'Country identified')], ['Answer: ' + S(15, 'global exports. China').replace('global exports. ', '') + '.'])
add(2, 3, 'cii', 'Q3(C)(ii)', exporters + '\n\n' + c_intro + '\n' + c_i + '\n' + L(2, 8, '(ii) Identify what percentage share of global exports the EU accounts for.'), 7,
    'business-6-13', 'eu-share-of-global-exports', 8, [15], 'Identify the percentage for 7 marks.', [single('Percentage', 7, 'Percentage identified')],
    ['Answer: ' + S(15, '16%') + '.'], extra=['business-6-14'])
add(2, 3, 'd', 'Q3(D)', L(2, 8, '(D) Outline two benefits for Irish businesses of exporting within the European Union.'), 15, 'business-6-14', 'exporting-within-eu-benefits',
    8, [15], EIGHT, eight_seven('Benefit'), [UNTIED])
add(2, 3, 'e', 'Q3(E)', L(2, 8, '(E) Outline two challenges for Irish businesses exporting to China.'), 15, 'business-6-13', 'exporting-to-china-challenges',
    8, [16], EIGHT, eight_seven('Challenge'), [UNTIED])

michelle = L(2, 9, 'Superfoods by SuperDudes') + '\n' + L(2, 9, 'Michelle, a ‘gym goer’, found it very difficult to source healthy ‘food on the go’ in Ireland. She gave up her job and invested her savings in “Superfoods by Superdudes” a ‘pop-up’ restaurant, serving healthy fast food in Dublin city centre, near many local gyms. The business employs seven staff. Their customers include athletes, fitness enthusiasts, office workers, families, students, etc. She holds weekly meetings with her staff and recently announced plans to offer a delivery service to customers who sign up for a weekly meal plan. The business will order more stock every week from suppliers to fulfil orders for its delivery service.')
add(2, 4, 'a', 'Q4(A)', michelle + '\n\n' + L(2, 9, '(A) Outline three entrepreneurial characteristics/skills displayed by Michelle. (Refer to the text in your answer.)'), 15,
    'business-1-5', 'michelle-entrepreneurial-characteristics', 9, [17], 'Three at 5 marks each (3 + 2).', points('Characteristic', 3, (3, 2)),
    ['Scheme examples: ' + S(17, 'Risk Taker – She gave up her job and invested her savings in “Superfoods by Superdudes”.')])
add(2, 4, 'b', 'Q4(B)', michelle + '\n\n' + L(2, 9, '(B) Outline two methods of communication, other than meetings, that Michelle could use to communicate with her staff.'), 15,
    'business-2-12', 'staff-communication-methods', 9, [17], EIGHT, eight_seven('Method'), [UNTIED])
add(2, 4, 'c', 'Q4(C)', michelle + '\n\n' + L(2, 9, '(C) Outline two features of a democratic leadership approach.'), 15, 'business-2-11', 'democratic-leadership-features',
    9, [17], EIGHT, eight_seven('Feature'), [UNTIED])
maslow = (L(2, 9, 'Maslow’s Hierarchy of Needs') + ' (a pyramid of five levels numbered 1 at the base to 5 at the top). ' + L(2, 9, 'Maslow arranged human needs in a hierarchy.'))
needs_i = '(D) ' + L(2, 9, '(i) In your answer book, Identify the needs numbered 1 to 5 from the following list: Social needs; Basic/Physical needs; Self-Actualisation needs; Esteem needs; Security/Safety needs.',
                     'Write your answers in your answer book as follows: 1 = 2 = etc.')
cum(2, 4, 'di', 'Q4(D)(i)', maslow + '\n\n' + needs_i, (2, 2, 2, 2, 2), 'business-2-11', 'maslow-needs-numbered', 9, [18],
    'Answer key (scheme page 18): ' + S(18, '1 = Basic/Physical Needs 2 = Security/Safety Needs 3 = Social Needs. 4 = Esteem Needs 5 = Self-Actualisation Needs') + '.', noun='needs')
add(2, 4, 'dii', 'Q4(D)(ii)', maslow + '\n\n' + needs_i + '\n' + L(2, 9, '(ii) Outline using examples how a manager can satisfy the social needs of his/her employees.'), 10,
    'business-2-11', 'satisfying-social-needs', 9, [18], 'Two ways with examples at 5 marks each (3 + 2).', points('Way', 2, (3, 2)),
    ['Scheme examples: ' + bullets(S(18, 'Organising staff outings • Organise staff team events – “bonding days”')).replace(' Organise', '; organise') + '.'])
add(2, 4, 'e', 'Q4(E)', michelle + '\n\n' + L(2, 9, '(E) Explain two reasons why stock control is very important for a food business.'), 10, 'business-2-13',
    'stock-control-food-business', 9, [18], 'Two reasons at 5 marks each (3 + 2).', points('Reason', 2, (3, 2)))

report = (L(2, 10, 'A report on motor insurance in Ireland', 'Motor insurance premiums in Ireland have increased in recent years. Many motor insurance customers experienced substantial increases in their premium, despite having a no claims bonus. Young motorists are faced with loadings which make their insurance premiums very expensive. Many drivers do not read their insurance policy carefully to identify important issues such as their policy excess.')
          + '\n(premium, no claims bonus, loadings, insurance policy and policy excess are underlined.)')
add(2, 5, 'a', 'Q5(A)', report + '\n\n' + L(2, 10, '(A) Explain any four of the insurance terms underlined above.'), 20, 'business-3-17', 'underlined-insurance-terms-choice',
    10, [19], 'Choose four of the five underlined terms and explain each at 5 marks (3 + 2).',
    seq(comps('First term you chose', (3, 2)), comps('Second term you chose', (3, 2)), comps('Third term you chose', (3, 2)), comps('Fourth term you chose', (3, 2))),
    ['You choose which four of the five underlined terms to answer. The scheme marks every choice alike (5 marks each, 3 + 2), so this is one card whichever terms you choose.',
     'Premium (scheme PDF page 19): “' + S(19, 'Premium – fee paid for insurance (to cover the risk) by the policy holder to the insurance company.') + '”',
     'No claims bonus (scheme PDF page 19): “' + S(19, 'No claims bonus – a reduction/discount in a premium for a policy holder who has not looked for any compensation') + '”',
     'Loadings (scheme PDF page 19): “' + S(19, 'Loading – an extra charge/fee/cost added to the basic premium of an insurance policy to cover higher risks') + '”',
     'Insurance policy (scheme PDF page 19): “' + S(19, 'Insurance Policy – this is the contract for insurance between the insurer and the insured.') + '”',
     'Policy excess (scheme PDF page 19): “' + S(19, 'Policy Excess – refers to the amount of money the insured person (policyholder) must pay towards the damages/claim before receiving the compensation for the damage from the insurance company.') + '”'])
types_i = L(2, 10, '(B) (i) Outline two types of insurance, other than motor insurance.')
add(2, 5, 'bi', 'Q5(B)(i)', report + '\n\n' + types_i, 10, 'business-3-17', 'insurance-types-other-than-motor', 10, [19], 'Two types at 5 marks each (3 + 2).',
    points('Type', 2, (3, 2)), ['Scheme examples: ' + S(19, 'Buildings & Contents Insurance – to cover financial loss to the buildings and contents in the event of burglary or damage.')
                                + ' Public liability, employer’s liability, goods in transit, plate glass, product liability and fidelity guarantee insurance.'])
add(2, 5, 'bii', 'Q5(B)(ii)', report + '\n\n' + types_i + '\n' + L(2, 10, '(ii) Explain the insurance principle utmost good faith.'), 5, 'business-3-17',
    'utmost-good-faith-explained', 10, [19], 'Explanation: 5 marks (3 + 2).', [comps('Utmost good faith', (3, 2))],
    ['Scheme: ' + S(19, 'Utmost Good Faith is a principle of insurance that states the person/business applying for insurance must answer all questions truthfully and disclose all material facts when completing the proposal form.')])
proposal = (L(2, 10, 'Sample questions on a motor insurance proposal form. The applicant has circled a response in each case.',
              '1. Does the car/vehicle have an alarm/immobiliser? YES / NO', '2. Do you have any penalty points on your licence? YES / NO')
            + '\n(YES is circled for both questions.)')
add(2, 5, 'c', 'Q5(C)', proposal + '\n\n(C) ' + L(2, 10, 'Explain whether the response to each of the questions on the motor insurance proposal form above should result in a premium loading or a premium reduction (discount).'),
    10, 'business-3-17', 'proposal-form-loading-or-discount', 10, [20], 'Each response 5 marks (3 + 2).',
    [comps('Question 1 (alarm/immobiliser)', (3, 2), i=1), comps('Question 2 (penalty points)', (3, 2), i=2)],
    ['Scheme (page 20): ' + S(20, 'Question one will result in a premium discount because an alarm/immobiliser will lead to a reduction in the risk of theft.') + ' '
     + S(20, 'Question two will lead to loading/increase on the premium.')])
lucia = (L(2, 10, 'Lucia noticed a job advertisement for a Team Leader at Aztec Insurance. The advertisement includes details such as; salary, benefit in kind, person specification and details about the training the successful candidate will receive.')
         + '\n(salary, benefit in kind, person specification and training are underlined.)')
add(2, 5, 'd', 'Q5(D)', lucia + '\n\n' + L(2, 10, '(D) Explain any three of the terms underlined above.'), 15, 'business-3-20', 'underlined-recruitment-terms-choice',
    10, [20], 'Choose three of the four underlined terms and explain each at 5 marks (3 + 2).',
    seq(comps('First term you chose', (3, 2)), comps('Second term you chose', (3, 2)), comps('Third term you chose', (3, 2))),
    ['You choose which three of the four underlined terms to answer. The scheme marks every choice alike (5 marks each, 3 + 2), so this is one card whichever terms you choose.',
     'Salary (scheme PDF page 20): “' + S(20, 'A type of remuneration that involves the employee receiving a fixed amount of money each fortnight/month/year irrespective of extra hours fulfilled.') + '”',
     'Benefit in kind (scheme PDF page 20): “' + S(20, 'A non-financial form of income. It is also known as a ‘perk’.') + '”',
     'Person specification (scheme PDF page 20): “' + S(20, 'This describes the qualities that the successful candidate for the job should have.') + '”',
     'Training (scheme PDF page 20): “' + S(20, 'This is an organised activity aimed at imparting the information and skills required for a particular job.') + '”'],
    extra=['business-3-18'])
add(2, 5, 'e', 'Q5(E)', lucia + '\n\n' + L(2, 10, '(E) Outline two benefits of teamwork in a business.'), 15, 'business-3-20', 'teamwork-benefits',
    10, [20], EIGHT, eight_seven('Benefit'), [UNTIED])

niamh = L(2, 11, 'Social Media Advertising Ireland Ltd') + '\n' + L(2, 11, 'Niamh O’Byrne is a Business Studies student from the University of Limerick. She conducted market research to determine how many local businesses use a website to sell their products. Niamh saw an opportunity to provide a digital marketing service for Irish businesses who do not have a marketing department. The service she offers involves managing the business’ social media pages and social media posts. Feedback from her clients has helped Niamh come up with ideas for new services she could offer local businesses.')
add(2, 6, 'a', 'Q6(A)', niamh + '\n\n' + L(2, 11, '(A) Outline two functions of advertising.'), 10, 'business-4-17', 'advertising-functions-2018',
    11, [21], 'Two functions at 5 marks each (3 + 2).', points('Function', 2, (3, 2)))
add(2, 6, 'b', 'Q6(B)', niamh + '\n\n' + L(2, 11, '(B) Explain the two market research methods and give one example of each method.'), 20, 'business-4-16', 'desk-and-field-research-with-examples',
    11, [21], 'Each method 10: named 3, explained 5 (3 + 2) and an example 2.',
    [comps('Desk research', (3, 3, 2, 2), ['Method named', 'Explained', 'Explanation developed', 'Example'], 1),
     comps('Field research', (3, 3, 2, 2), ['Method named', 'Explained', 'Explanation developed', 'Example'], 2)],
    ['Scheme: ' + S(21, 'Desk research involves accessing or using information that has already been gathered.') + ' '
     + S(21, 'Field research involves going into the marketplace to gather first-hand or new business information.'),
     'Examples: ' + S(21, 'Examples of desk research: the internet, internal sales reports, trade reports, Central Statistics Office publications, newspapers.') + ' '
     + S(21, 'Examples of field research: surveys, observation, questionnaires, and customer panels.')])
genoa = L(2, 11, 'Genoa Italian Restaurant is examining its ability to pay its bills as they fall due.')
ratios = (genoa + '\n\n' + L(2, 11, '(C) Calculate the Working Capital Ratio and the Acid Test Ratio of Genoa Italian Restaurant from the data below.', 'Show your workings in your answer book.')
          + '\n2017: Current Assets €84,000; Current Liabilities €42,000; Closing Stock €14,000; Opening Stock €18,000')
L(2, 11, '2017 Current Assets €84,000 Current Liabilities €42,000 Closing Stock €14,000 Opening Stock €18,000')
flat(add(2, 6, 'c', 'Q6(C)', ratios, 20, 'business-3-19', 'working-capital-and-acid-test-genoa', 11, [22],
         'Working Capital Ratio 9 (formula 3, workings 4, answer 2) and Acid Test Ratio 11 (formula 3, workings 6, answer 2).',
         seq(response(1, 'Working Capital Ratio', [('formula', 'Formula: Current Assets : Current Liabilities', 3), ('workings', 'Workings: 84,000 : 42,000', 4),
                                                   ('answer', 'Answer: 2 : 1', 2)]),
             response(2, 'Acid Test Ratio', [('formula', 'Formula: (Current Assets – Closing Stock) : Current Liabilities', 3),
                                             ('workings', 'Workings: (84,000 – 14,000) : 42,000', 6), ('answer', 'Answer: 1.66 : 1', 2)])),
         ['The allocation summary prints “' + S(7, 'Working Capital Ratio: 9m (3m + 4m + 2m) Acid Test Ratio: 11m (3m + 6m + 2m)') + '”.',
          'Scheme (page 22): ' + S(22, 'Working Capital Ratio Current Assets : Current Liabilities 3 = 84,000 : 42,000 4 = 2 : 1 2') + '; '
          + S(22, 'Acid Test Ratio (Current Assets – Closing Stock) : Current Liabilities 3 = (84,000 – 14,000) : 42,000 6 [= 70,000 : 42,000] = 1.66 : 1 2') + '.',
          'The scheme’s working uses closing stock (€14,000); opening stock does not enter either ratio.']))
add(2, 6, 'd', 'Q6(D)', genoa + '\n\n' + L(2, 11, '(D) Name two expenses that a business such as Genoa Italian Restaurant would incur.'), 10, 'business-3-16',
    'restaurant-expenses', 11, [22], 'Two expenses at 5 marks each.', seq(single('Expense 1', 5, 'Expense named'), single('Expense 2', 5, 'Expense named')),
    ['Scheme examples: ' + S(22, 'Wages, Electricity, Insurance, Advertising, Rent, Delivery Costs.') + ' ' + S(22, 'Accept other appropriate correct answers.')])
add(2, 6, 'e', 'Q6(E)', genoa + '\n\n' + L(2, 11, '(E) Discuss two sales promotions techniques a restaurant could use to increase its sales.'), 15, 'business-4-17',
    'restaurant-sales-promotions', 11, [22], EIGHT, eight_seven('Technique'), [UNTIED])

plc = (L(2, 12, 'Product Life Cycle') + ' (diagram): a sales curve plotted against time, divided into five stages labelled Launch, Growth, Maturity, Saturation and Decline — read the curve on the printed page.')
L(2, 12, 'Product Life Cycle TIME')
stages_i = L(2, 12, '(A) (i) Name two stages in the product life cycle above, where sales are increasing.')
cum(2, 7, 'ai', 'Q7(A)(i)', plc + '\n\n' + stages_i, (3, 2), 'business-4-17', 'plc-stages-sales-increasing', 12, [23],
    'Scheme (page 23): any two of ' + S(23, 'Launch Growth Maturity').replace(' ', ', ', 1).replace(' Maturity', ' and Maturity') + '.', noun='stages')
add(2, 7, 'aii', 'Q7(A)(ii)', plc + '\n\n' + stages_i + '\n' + L(2, 12, '(ii) Name one example of a product in the launch/introductory stage and one example of a product in the decline stage.'), 10,
    'business-4-17', 'plc-launch-and-decline-examples', 12, [23], 'Each example 5 marks.',
    seq(single('Launch-stage product', 5, 'Example named'), single('Decline-stage product', 5, 'Example named')),
    ['Scheme: ' + S(23, 'Launch: Any relevant example of a recently introduced product e.g. the new Kia Sportage, The iPhone X') + '. '
     + S(23, 'Decline: Any relevant example of a long established now out-of-date or obsolete product e.g. DVD players, The iPhone 4.')])
add(2, 7, 'b', 'Q7(B)', L(2, 12, '(B) The product life cycle, product packaging and product design relate to the product element of the marketing mix. Explain two functions of product packaging.'),
    15, 'business-4-17', 'packaging-functions-2018', 12, [23], EIGHT, eight_seven('Function'), [UNTIED])
target_i = L(2, 12, '(C) (i) Explain the term target market.')
add(2, 7, 'ci', 'Q7(C)(i)', target_i, 12, 'business-4-16', 'target-market-explained', 12, [23], 'Explanation: 12 marks (6 + 6).', [comps('Target market', (6, 6))],
    ['Scheme: ' + S(23, 'A target market is the group of people at whom a particular product or service is aimed.')])
add(2, 7, 'cii', 'Q7(C)(ii)', target_i + '\n' + L(2, 12, '(ii) Name a target market for electric cars.'), 8, 'business-4-16', 'electric-car-target-market',
    12, [23], 'Name a target market for 8 marks.', [single('Target market', 8, 'Target market named')],
    ['Scheme examples: ' + S(23, 'Environmentally conscious motorists/ eco-friendly customers/ “green” consumers.')])
chan = add(2, 7, 'd', 'Q7(D)', L(2, 12, '(D) Illustrate, using a diagram, one channel of distribution a baker could use for freshly baked cakes.'), 10, 'business-4-17',
           'baker-channel-of-distribution', 12, [24],
           'Draw one channel: 10 marks, either 4 + 2 + 4 (manufacturer, arrow, consumer) or 5 @ 2 (manufacturer, arrow, retailer, arrow, consumer).',
           [comps('Channel diagram', (10,), ['Diagram marked on the scheme’s template'])],
           ['The scheme (page 24) prints two channels: ' + S(24, 'MANUFACTURER CONSUMER 4 2 4 or MANUFACTURER RETAILER CONSUMER 2 2 2 2 2')
            + '. Manufacturer to consumer: manufacturer 4, the arrow 2, consumer 4. Manufacturer to retailer to consumer: each stage and each arrow 2.',
            'The allocation summary prints “' + S(7, 'Illustration: 10 marks (4m + 2m +4m) or (5 @ 2m)') + '”. Whichever channel you draw, record the marks in steps of 2.'])
permit(chan, 0, [0, 2, 4, 6, 8, 10])
test_i = L(2, 12, '(E) (i) Explain the term test marketing.')
add(2, 7, 'ei', 'Q7(E)(i)', test_i, 7, 'business-4-14', 'test-marketing-explained', 12, [24], 'Explanation: 7 marks (4 + 3).', [comps('Test marketing', (4, 3))],
    ['Scheme: ' + S(24, 'The product is tested on a sample of potential consumers before going into full production.')])
add(2, 7, 'eii', 'Q7(E)(ii)', test_i + '\n' + L(2, 12, '(ii) Outline two others stages in the development process of a new product.'), 8, 'business-4-14',
    'other-development-stages', 12, [24], 'Two stages at 4 marks each (2 + 2).', points('Stage', 2, (2, 2)),
    ['Scheme stages: Idea Generation, Product Screening, Concept Development, Feasibility Study, Prototype Development. '
     + S(24, 'Idea Generation: Initial concepts for the new product are thought up systematically.')])

leo = L(2, 13, 'Local Enterprise Offices (LEOs) across Ireland, provide advice and assistance to potential start-up businesses. This includes help in setting up the business, drawing up a business plan, accessing finance, marketing, and the day-to-day running of the business. Mentors are provided for the new business owner, to offer independent advice in order to aid decision making.')
add(2, 8, 'a', 'Q8(A)', leo + '\n\n' + L(2, 13, '(A) Explain two differences between a Sole Trader and a Partnership as forms of business ownership.'), 15, 'business-5-14',
    'sole-trader-versus-partnership', 13, [25], EIGHT, eight_seven('Difference'), [UNTIED])
plan_i = L(2, 13, '(B) (i) List two headings included in a business plan.')
cum(2, 8, 'bi', 'Q8(B)(i)', leo + '\n\n' + plan_i, (4, 4), 'business-4-15', 'business-plan-headings', 13, [25],
    'Scheme headings: ' + bullets(S(25, '• Description of Business & Owners • Management & Organisation Structure • Production Details • Marketing Plan • Market Research & Analysis • Financial Plan.')).replace(' Management', '; Management').replace(' Production', '; Production').replace(' Marketing Plan', '; Marketing Plan').replace(' Market Research', '; Market Research').replace(' Financial', '; Financial'),
    noun='headings')
add(2, 8, 'bii', 'Q8(B)(ii)', leo + '\n\n' + plan_i + '\n' + L(2, 13, '(ii) Explain two benefits of preparing a business plan.'), 12, 'business-4-15', 'business-plan-benefits-2018',
    13, [25], 'Two benefits at 6 marks each.', points('Benefit', 2, (6,)),
    ['Scheme examples: ' + S(25, 'To set out clearly the objectives and targets of the business') + '; ' + S(25, 'To obtain finance from lenders, who must be convinced that the plan has a good chance of success') + '.'])
add(2, 8, 'c', 'Q8(C)', leo + '\n\n' + L(2, 13, '(C) Explain any three of the following sources of finance:', '(i) Share Capital/Equity Capital', '(ii) Bank Overdraft', '(iii) Leasing', '(iv) Medium Term Loan.'),
    15, 'business-3-16', 'sources-of-finance-choice-2018', 13, [26], 'Choose three of the four sources and explain each at 5 marks (3 + 2).',
    seq(comps('First source you chose', (3, 2)), comps('Second source you chose', (3, 2)), comps('Third source you chose', (3, 2))),
    ['You choose which three of the four printed sources to answer. The scheme marks every choice alike (5 marks each, 3 + 2), so this is one card whichever sources you choose.',
     'Share Capital/Equity Capital (scheme PDF page 26): “' + S(26, 'Share Capital/Equity Capital is a long-term source of finance, provided by investors known as shareholders.') + '”',
     'Bank Overdraft (scheme PDF page 26): “' + S(26, 'Bank Overdraft is a short-term source of finance. It involves permission from the bank to withdraw more money than is in the current account.') + '”',
     'Leasing (scheme PDF page 26): “' + S(26, 'Leasing is the use of a fixed asset in return for an agreed payment over a period of 1-5 years.') + '”',
     'Medium Term Loan (scheme PDF page 26): “' + S(26, 'Medium term loan is money borrowed from a financial institution for a period of 1 – 5 years.') + '”'])
add(2, 8, 'd', 'Q8(D)', leo + '\n\n' + L(2, 13, '(D) Explain two features of Job Production.'), 15, 'business-4-15', 'job-production-features',
    13, [26], EIGHT, eight_seven('Feature'), [UNTIED])
add(2, 8, 'e', 'Q8(E)', leo + '\n\n' + L(2, 13, '(E) Outline two challenges for start-up businesses in Ireland.'), 10, 'business-4-15', 'start-up-challenges',
    13, [26], 'Two challenges at 5 marks each (3 + 2).', points('Challenge', 2, (3, 2)))

# ---------------------------------------------------------------- checks and write-out
qn = lambda c: c['questionRef'].split(' Q')[1].split('(')[0]
for section, count, total in [('1', 15, 10), ('2', 8, 75)]:
    for q in range(1, count + 1):
        got = sum(c['totalMarks'] for c in P.created if c['section'] == section and qn(c) == str(q))
        assert got == total, (section, q, got)
assert not [i for i in ORIGINAL if i.startswith('bus-2018-ol-')]
assert not P.pools

SELECTION = {
    1: 'No finite printed answer menu occurs in Section 1 (answer ten of fifteen at 10 marks). The labels in Q2, the word bank in Q4, TRUE/FALSE in Q7, the PR methods in Q13, the ticks in Q14 and the matching rows in Q15 are required answer formats. Support-note lists are open examples.',
    2: 'Three printed choices, each one card: Q5(A) any four of the five underlined insurance terms, Q5(D) any three of the four underlined recruitment terms and Q8(C) any three of the four printed sources of finance (the scheme marks every choice alike). Q7(D) “one channel” is an open choice the scheme marks on two templates (4 + 2 + 4 or 5 @ 2), so it is one card. Q6(C) asks for both ratios in one printed part, so it is one card with the summary’s 9 and 11 as two responses. Sub-parts with their own published marks are separate cards. Support-note lists are open examples.',
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
    if m == 'any four' and own(w, m, 'Explain any four of the insurance terms underlined'):
        return 'finite-choice', 'Section 2 Q5(A) asks for any four of the five underlined insurance terms. The scheme marks every choice alike, so one card carries all five with the scheme wording for each.', 'bus-2018-ol-s2-q5a'
    if m == 'any three' and own(w, m, 'Explain any three of the terms underlined'):
        return 'finite-choice', 'Section 2 Q5(D) asks for any three of the four underlined recruitment terms. The scheme marks every choice alike, so one card carries all four with the scheme wording for each.', 'bus-2018-ol-s2-q5d'
    if m == 'any three' and own(w, m, 'Explain any three of the following sources of finance'):
        return 'finite-choice', 'Section 2 Q8(C) asks for any three of the four printed sources of finance. The scheme marks every choice alike, so one card carries all four with the scheme wording for each.', 'bus-2018-ol-s2-q8c'
    if m == 'Choose' and own(w, m, 'Choose the appropriate words'):
        return 'required-headings', 'Section 1 Q4 is a word-bank completion: both blanks are required and the printed words are the answer options, not optional tasks.', None
    if m == 'or' and own(w, m, 'TRUE or FALSE'):
        return 'required-headings', 'TRUE/FALSE are answer labels for each of the four required statements in Section 1 Q7, not optional tasks.', None
    if m == 'or' and (own(w, m, 'intrapreneurship or entrepreneurship') or own(w, m, 'INTRAPRENEUR or ENTREPRENEUR')):
        return 'required-headings', 'Section 1 Q2 asks for one label (intrapreneur or entrepreneur) after each of five required statements; the labels are answers, not optional tasks.', None
    if m == 'or' and own(w, m, 'the retailer or the producer'):
        return 'required-headings', 'Section 2 Q1(C) asks who is responsible; it is one required determination, explained and supported by the law, not a choice of task.', None
    if m == 'or' and own(w, m, 'surplus or a deficit'):
        return 'required-headings', 'Section 2 Q3(A)(ii) requires a determination of surplus or deficit; it is one required answer, not a choice of task.', None
    if m == 'or' and own(w, m, 'premium loading or a premium reduction'):
        return 'required-headings', 'Section 2 Q5(C) asks whether each of the two required responses leads to a loading or a discount; it is one determination per response, not a choice of task.', None
    if m == 'or' and own(w, m, 'a post or photograph'):
        return 'case-context', '“a post or photograph” is wording inside a printed statement in Section 1 Q2, not a choice of task.', None
    assert (fileid, page) in {('LC033GLP000EV', 1), ('LC033GLP000EV', 7)} and m in ('either', 'or'), (fileid, page, m, w)
    return 'exam-navigation', 'The cover and Section 2 rubrics set how many whole questions a candidate answers (one from Part 1, two from Part 2 and one other from either part). Every numbered question remains in the practice corpus as separate cards.', None


n = P.write([(1, range(1, 16)), (2, range(1, 9))], SELECTION, classify,
            'Every part of {year} Ordinary Section {section} Question {q} was visually checked against its SEC paper, allocation summary and expected responses. The single-booklet identity keeps the short (n) and long (S2Q) question numbering apart.')
print(f'Reviewed {len(P.created)} 2018 Ordinary tasks; classified {n} raw selection matches.')
