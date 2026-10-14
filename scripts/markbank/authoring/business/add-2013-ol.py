"""Review the 2013 Ordinary English paper (one booklet: Section 1 and Section 2).

2013: answer ten of fifteen short questions at 10 marks and four of eight
long questions at 75 (one from Part 1, two from Part 2 and one other), all in
one twelve-page booklet (LC033GLP000EV, the same file id as its scheme). No
Ordinary card existed for 2013, so every card is new. The allocation summary
(scheme pages 4-8) sets each boundary; the support notes (pages 9-25) print
totals only, so the summary's splits are the card's. One printed choice is
one card: Section 2 Q8(C) any two of three product-development stages
(8 and 7, not tied to a stage).
"""
from bus_lib import (Paper, ORIGINAL, comps, points, seq, unequal, single, response, fixed, permit)

T = {(1, q): 4 for q in range(1, 16)}
T.update({(2, 1): 5, (2, 2): 5, (2, 3): 6, (2, 4): 6, (2, 5): 7, (2, 6): 7, (2, 7): 8, (2, 8): 8})
P = Paper(2013, 'ordinary', {1: 'LC033GLP000EV', 2: 'LC033GLP000EV'}, 'LC033GLP000EV', T)
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


def bullets(text, sep='; '):
    return sep.join(x.strip() for x in text.split('•') if x.strip())


# ---------------------------------------------------------------- Section 1 (10 marks each)
add(1, 1, '', 'Q1', L(1, 2, 'What do the following letters stand for? (Write each answer in the space provided.)', 'PAYE PRSI USC').replace(' PRSI', '\nPRSI').replace(' USC', '\nUSC'),
    10, 'business-3-18', 'abbreviations-paye-prsi-usc', 2, [9], 'The first and third correct terms earn 3 each (1 + 1 + 1); the second 4 (1 + 1 + 1 + 1).',
    [comps('First correct term', (3,), ['Words written in full'], 1), comps('Second correct term', (4,), ['Words written in full'], 2),
     comps('Third correct term', (3,), ['Words written in full'], 3)],
    ['Answer key (scheme page 9): ' + S(9, 'PAYE – Pay As You Earn PRSI – Pay Related Social Insurance USC – Universal Social Charge') + '.'])
cum(1, 2, '', 'Q2', L(1, 2, 'Name levels 3, 4, and 5 in Maslow’s Hierarchy of Needs.') + '\n(Pyramid: ' + L(1, 2, '2. Safety & Security 1. Physiological Needs')
    + ' printed at the base; levels 3, 4 and 5 blank.)\nLevel 5:\nLevel 4:\nLevel 3:', (4, 3, 3), 'business-2-11', 'maslow-levels-three-to-five', 2, [9],
    'Answer key (scheme page 9): ' + S(9, '5. Self-Actualisation Needs 4. Esteem Needs 3. Social Needs') + '.', noun='levels')
L(1, 2, 'Level 5:', 'Level 4:', 'Level 3:')
cum(1, 3, '', 'Q3', L(1, 2, 'Outline three reasons why a person would consider becoming an entrepreneur:'), (4, 3, 3), 'business-1-5', 'reasons-to-become-entrepreneur', 2, [9],
    'Scheme examples (page 9): ' + bullets(S(9, '• Own boss / self-employed / independent / own decisions • To make money/profit • To be successful/have power')) + '.', noun='reasons')
cum(1, 4, '', 'Q4', L(1, 2, 'Complete the three missing elements of the Marketing Mix:') + '\n(i) PRODUCT | (ii) ______ | (iii) ______ | (iv) ______', (4, 3, 3), 'business-4-17',
    'missing-marketing-mix-2013', 2, [9], 'Answer key (scheme page 9): ' + S(9, 'PRODUCT PRICE PLACE PROMOTION') + ' (Product is printed).', noun='elements')
L(1, 2, '(i) PRODUCT (ii) (iii) (iv)')
add(1, 5, '', 'Q5', L(1, 3, 'Explain what is meant by a ‘Multinational Company’ and state one example.') + '\nExample:', 10, 'business-6-15', 'multinational-explained-2013',
    3, [9], 'Explanation 6 (3 + 3) and an example 4.', seq(comps('Multinational company', (3, 3)), single('Example', 4, 'Example named')),
    ['Scheme: ' + S(9, 'A Multinational company is a business with headquarters in one country and many bases/branches in other countries') + '; examples ' + S(9, 'Glanbia, Kerry Group, Hewlett Packard') + '.'])
add(1, 6, '', 'Q6', L(1, 3, 'The following information is available from the final accounts of Daly Ltd on 31/12/2012: (Show your workings)')
    + '\nCurrent Liabilities €140,000\nCurrent Assets €280,000 (includes Closing Stock € 70,000)\n' + L(1, 3, 'Calculate: (a) Working Capital Ratio Answer:') + '\n(b) Acid Test Ratio Answer:',
    10, 'business-3-19', 'working-capital-and-acid-test-daly', 3, [9], 'Working capital ratio 4 and acid test ratio 6.',
    [comps('Working Capital Ratio', (4,), ['Ratio calculated'], 1), comps('Acid Test Ratio', (6,), ['Ratio calculated'], 2)],
    ['Scheme (page 9): ' + S(9, '(i)Working Capital Ratio: Current Assets : Current Liabilities 280,000 : 140,000 2 : 1') + '; ' + S(9, '(ii) Acid Test Ratio Current Assets – Closing Stock : Current Liabilities 280,000 – 70,000 : 140,000') + ' = 1.5 : 1.'])
L(1, 3, 'Current Liabilities €140,000 Current Assets €280,000 (includes Closing Stock € 70,000)')
cum(1, 7, '', 'Q7', L(1, 3, 'Indicate by means of a tick (✓), the category to which each good or service belongs:', 'Visible Export Invisible Export Visible Import Invisible Import',
                      'Australian tourists in Ireland for ‘The Gathering 2013’', 'Greek cheese sold in Ireland', 'Irish Lamb sold in France', 'Justin Timberlake plays a concert in the O2 Dublin'),
    (3, 3, 2, 2), 'business-6-13', 'trade-category-ticks', 3, [10],
    'Answer key (ticks on scheme page 10): Australian tourists Invisible Export; Greek cheese Visible Import; Irish lamb in France Visible Export; Justin Timberlake in Dublin Invisible Import.',
    noun='ticks')
cum(1, 8, '', 'Q8', L(1, 3, 'List two elements of a valid contract:'), (5, 5), 'business-0-12', 'valid-contract-elements-2013', 3, [10],
    'Scheme elements (page 10): offer and acceptance (agreement), consideration, consent to contract, capacity to contract, legality of form, legality of purpose.', noun='elements')
S(10, '• Consideration • Consent to Contract • Capacity to Contract • Legality of Form • Legality of Purpose')
cum(1, 9, '', 'Q9', L(1, 4, 'State whether the following market research techniques are DESK or FIELD research.', '1. Questionnaire', '2. Central Statistics Office Statistics',
                      '3. Government Publications', '4. Focus Group', '5. Observation'),
    (2, 2, 2, 2, 2), 'business-4-16', 'desk-or-field-techniques', 4, [10], 'Answer key (scheme page 10): FIELD; DESK; DESK; FIELD; FIELD.')
S(10, '1. Questionnaire FIELD 2. Central Statistics Office Statistics DESK 3. Government Publications DESK 4. Focus Group FIELD 5. Observation FIELD')
add(1, 10, '', 'Q10', L(1, 4, 'Outline two advantages of leasing as a medium term source of finance:'), 10, 'business-3-16', 'leasing-advantages', 4, [10],
    'Two advantages at 5 marks each.', points('Advantage', 2, (5,)),
    ['Scheme examples: ' + bullets(S(10, '• No capital/lump sum required to purchase asset • Business will not lose money when asset depreciates • No security required')) + '.'])
cum(1, 11, '', 'Q11', L(1, 4, 'List three benefits to a business of investing in new technology:'), (4, 3, 3), 'business-2-12', 'new-technology-benefits', 4, [10],
    'Scheme examples (page 10): ' + bullets(S(10, '• Production becomes more efficient/ time saving • Less errors made • Production costs are lowered')) + '.', noun='benefits')
cum(1, 12, '', 'Q12', L(1, 4, 'Complete the functional organisation structure of a business with four departments:') + '\n(Chart: ' + L(1, 4, 'MANAGING DIRECTOR')
    + ' at the top; four department boxes below: (i) FINANCE printed, (ii), (iii) and (iv) blank.)', (4, 3, 3), 'business-2-13', 'functional-structure-three-departments', 4, [10],
    'Scheme departments (page 10): ' + bullets(S(10, '• HUMAN RESOURCES • PRODUCTION • SALES • R & D • MARKETING • IT • QUALITY CONTROL'), ', ') + '.', noun='departments')
L(1, 4, 'MANAGING DIRECTOR (i) FINANCE (ii) (iv) (iii)')
cum(1, 13, '', 'Q13', '\n'.join([L(1, 5, 'Column 1 is a list of business terms. Column 2 is a list of explanations for these terms. (One explanation has no match.)'),
                                 L(1, 5, '1. Certificate of Incorporation', '2. Articles of Association', '3. Private Limited Company', '4. Sole Trader', '5. Memorandum of Association'),
                                 L(1, 5, 'A. Has eight or more members with a common bond.', 'B. Has unlimited liability.', 'C. It states the main objectives of the company.',
                                   'D. Document proving the company legally exists.', 'E. Has the abbreviation LTD after its name.', 'F. Internal rules governing how a company operates.'),
                                 L(1, 5, 'Match the two lists by placing the letter of the correct explanation under the relevant number below.')]),
    (2, 2, 2, 2, 2), 'business-5-14', 'company-terms-matching', 5, [11], 'Answer key (scheme page 11): 1 D; 2 F; 3 E; 4 B; 5 C. Explanation A is unused.', noun='matches')
S(11, '1 2 3 4 5 D F E B C')
cum(1, 14, '', 'Q14', L(1, 5, 'Write TRUE or FALSE after the following statements:', '1. The balance sheet is a statement of assets and liabilities.',
                        '2. Quality Control involves monitoring how much money is owed to the business by its customers.', '3. A Tactical Plan is a long term plan set out by the business.',
                        '4. A Mission Statement outlines what a business sets out to do.', '5. A cash flow is an example of a financial plan.'),
    (2, 2, 2, 2, 2), 'business-2-13', 'management-true-false-2013', 5, [11], 'Answer key (scheme page 11): TRUE; FALSE; FALSE; TRUE; TRUE.', extra=['business-3-16'])
S(11, '1. The balance sheet is a statement of assets and liabilities. TRUE')
add(1, 15, '', 'Q15', L(1, 5, 'Outline two methods for rewarding employees:'), 10, 'business-3-20', 'methods-of-rewarding-employees', 5, [11],
    'Two methods at 5 marks each (3 + 2).', points('Method', 2, (3, 2)),
    ['Scheme examples: ' + bullets(S(11, '• Basic Salary – payment based on contract • Piece Rate – payment based on the amount of items produced')) + '; commission, benefit in kind, share options.'])

# ---------------------------------------------------------------- Section 2 (75 marks each)
sunhols = L(2, 6, 'Sunhols') + '\n' + L(2, 6, 'Jim & Cliona McCarthy booked a two-week family holiday to Portugal with Sunhols costing €1,800. On arrival they discovered that the apartment, which was advertised on the website as overlooking the beach, was actually three kilometres inland. They had been informed by the sales assistant that there was a restaurant on site but this was not the case. They were very disappointed when they realised that the ‘Kids Club’ which they read about in the company\'s brochure as being open from June to August, did not open until July. Cliona complained to Sunhols when she returned home, but they said it was not their responsibility. Cliona then contacted the National Consumer Agency (NCA) about her rights, and they advised her to take her case to the Small Claims Court.')
add(2, 1, 'a', 'Q1(A)', sunhols + '\n\n' + L(2, 6, '(A) Explain how Sunhols has broken the terms of the Consumer Protection Act, 2007.'), 15, 'business-0-13', 'sunhols-breaches',
    6, [12], 'The term broken (false or misleading advertising) 7, and two examples from the case at 4 each.',
    seq(comps('Term of the Act broken', (7,), ['False or misleading advertising explained']), single('Example from the case 1', 4, 'Example given'),
        single('Example from the case 2', 4, 'Example given')),
    ['Scheme (page 12): ' + S(12, 'False/misleading advertising – apartment advertised overlooking beach but was 3km inland') + '; '
     + S(12, 'False/misleading sales practice – there was no restaurant on site which sales assistant told them there would be') + '.'])
add(2, 1, 'b', 'Q1(B)', sunhols + '\n\n' + L(2, 6, '(B) Outline two functions of the National Consumer Agency (NCA).'), 15, 'business-0-13', 'nca-functions',
    6, [12], EIGHT, eight_seven('Function'), [UNTIED])
add(2, 1, 'c', 'Q1(C)', sunhols + '\n\n' + L(2, 6, '(C) Outline three advantages for Cliona of bringing her case to the Small Claims Court.'), 20, 'business-0-13', 'cliona-small-claims-advantages',
    6, [12], 'Three advantages: 7 (4 + 3), 7 (4 + 3) and 6 (3 + 3).', unequal('Advantage', [(4, 3), (4, 3), (3, 3)], None),
    ['The 7/7/6 sequence prices the three advantages, not particular advantages.'])
pavel = L(2, 6, 'Employment Equality Act, 1998') + '\n' + L(2, 6, 'Pavel Zachwieja applied for a promotion in Reddon Ltd. He worked for the company for four years and was qualified in Production Management. The promotion was given to John Clancy, who had only worked in the company for six months and had no management qualification. Pavel believed he was not given the job because he is not Irish.')
cum(2, 1, 'd', 'Q1(D)', pavel + '\n\n' + L(2, 6, '(D) List three grounds on which discrimination is outlawed under the Employment Equality Act, 1998.'), (5, 5, 5), 'business-0-14',
    'discrimination-grounds-2013', 6, [12], 'Scheme grounds (page 12): gender, marital status, family status, religion, age, race, disability, sexual orientation, membership of the Travelling Community.',
    noun='grounds')
S(12, '• Age • Race – originate from another country/colour of skin')
add(2, 1, 'e', 'Q1(E)', pavel + '\n\n' + L(2, 6, '(E) Outline the role of the Equality Tribunal in assisting Pavel with his discrimination case.'), 10, 'business-0-14', 'equality-tribunal-role',
    6, [13], 'One outline: 10 marks (5 + 5).', [comps('Equality Tribunal', (5, 5))],
    ['Scheme: ' + S(13, 'The Equality Tribunal is an independent body set up up to investigate or mediate employee discrimination cases/complaints')])

glen = L(2, 7, 'GLENTRONIC PHARMACEUTICALS') + '\n' + L(2, 7, 'John Tuohy set up Glentronic Pharmaceuticals in 2003 in his home town of Abbeyglen. The company develops and produces medical drugs. Glentronic Pharmaceuticals employs over 600 employees and exports its products to many countries. John is thinking about expanding into the Asian market and setting up a base there. He is considering changing Glentronic Pharmaceuticals from a Private Limited Company to a PLC so that it can access more finance to support the expansion.')
add(2, 2, 'a', 'Q2(A)', glen + '\n\n' + L(2, 7, '(A) What do the letters PLC stand for?'), 5, 'business-5-14', 'plc-letters', 7, [14], 'PLC in full: 5 marks (3 + 1 + 1).',
    [comps('PLC', (5,), ['Words written in full'])], ['Answer: ' + S(14, 'PLC: Public Limited Company') + '.'])
cum(2, 2, 'b', 'Q2(B)', glen + '\n\n' + L(2, 7, '(B) List two sources of finance Glentronic Pharmaceuticals can use for expansion.'), (5, 5), 'business-3-16', 'expansion-finance-sources',
    7, [14], 'Scheme examples (page 14): ' + bullets(S(14, '• Issuing shares • Long term Loan/Debenture • Retained Earnings/Reserves/Profit ploughed back in • Government/EU Grants')) + '.', noun='sources')
add(2, 2, 'c', 'Q2(C)', glen + '\n\n' + L(2, 7, '(C) Explain two possible benefits of Glentronic Pharmaceuticals for the town of Abbeyglen.'), 20, 'business-5-16', 'glentronic-town-benefits',
    7, [14], 'Two benefits at 10 marks each (5 + 5).', points('Benefit', 2, (5, 5)))
add(2, 2, 'd', 'Q2(D)', glen + '\n\n' + L(2, 7, '(D) Outline two possible benefits for Glentronic Pharmaceuticals of expanding into the Asian market.'), 20, 'business-6-15', 'asian-market-benefits',
    7, [14], 'Two benefits at 10 marks each (5 + 5).', points('Benefit', 2, (5, 5)), extra=['business-4-18'])
add(2, 2, 'e', 'Q2(E)', glen + '\n\n' + L(2, 7, '(E) Outline two environmental responsibilities of Glentronic Pharmaceuticals.'), 20, 'business-5-17', 'environmental-responsibilities',
    7, [14], 'Two responsibilities at 10 marks each (5 + 5).', points('Responsibility', 2, (5, 5)))

taxes = L(2, 7, 'The following information relates to the main sources of taxation received by the Irish Government in 2012:') + '\nIncome Tax €15 billion; VAT €10 billion; Corporation Tax € 4 billion; Excise Duties € 5 billion'
L(2, 7, 'Income Tax €15 billion VAT €10 billion Corporation Tax € 4 billion Excise Duties € 5 billion')
chart = add(2, 3, 'a', 'Q3(A)', taxes + '\n\n' + L(2, 7, '(A) Draft a Bar Chart to represent the above information.'), 15, 'business-2-12', 'tax-sources-bar-chart', 7, [15],
            'Title 2, labels 5 and four bars at 2 each.', [response(1, 'Bar chart', [('title', 'Title', 2), ('labels', 'Labels', 5), ('income-tax', 'Income Tax: €15 billion', 2),
                                                                                  ('vat', 'VAT: €10 billion', 2), ('corporation-tax', 'Corporation Tax: €4 billion', 2),
                                                                                  ('excise', 'Excise Duties: €5 billion', 2)])],
            ['The allocation summary prints “' + S(6, 'Bar Chart: Title 2 marks Labels 5 marks Bars 8 marks (4 @ 2m)') + '”; the scheme’s chart is titled “' + S(15, 'Taxation recieved by Irish Government in 2012 €bn.') + '”.'],
            extra=['business-3-18'])
for a in chart['rubric']['responses'][0]['allocations']:
    if a['id'] != 'labels':
        a['permittedMarks'] = [0, a['maxMarks']]
add(2, 3, 'b', 'Q3(B)', taxes + '\n\n' + L(2, 7, '(B) Outline three reasons why the Government collects tax.'), 15, 'business-5-15', 'why-government-collects-tax',
    7, [15], 'Three reasons at 5 marks each.', points('Reason', 3, (5,)))
add(2, 3, 'c', 'Q3(C)', taxes + '\n\n' + L(2, 7, '(C) Outline two effects on Irish business of increases in taxation.'), 10, 'business-3-18', 'tax-increase-effects',
    7, [15], 'Two effects at 5 marks each (3 + 2).', points('Effect', 2, (3, 2)))
add(2, 3, 'd', 'Q3(D)', taxes + '\n\n' + L(2, 7, '(D) Outline two advantages to Ireland of membership of the European Union (EU).'), 15, 'business-6-14', 'eu-membership-advantages-2013',
    7, [15], EIGHT, eight_seven('Advantage'), [UNTIED])
add(2, 3, 'e', 'Q3(E)', taxes + '\n\n' + L(2, 7, '(E) Name two EU institutions and explain the role of one of them.'), 20, 'business-6-14', 'eu-institutions-one-role',
    7, [16, 17], 'Two institutions named at 5 each, and the role of one of them 10 (5 + 5).',
    seq(single('Institution 1', 5, 'Institution named'), single('Institution 2', 5, 'Institution named'), comps('Role of one of them', (5, 5))),
    ['You explain the role of one of the two institutions you named; the scheme marks any institution alike. Example: '
     + S(16, 'The main body responsible for running the EU – looks after day-to-day management of EU') + ' (European Commission).'])

snap = L(2, 8, 'SNAPAPPY') + '\n' + L(2, 8, 'While completing a degree in Computer Science, Shane Whelan designed and developed an ‘app’ for smartphones, allowing users to change their photographs into cartoons. Shane worked long hours to develop the ‘app’. Once it was launched it became very popular, achieving more than 20,000 downloads in the first few days, and so began his business ‘Snapappy’. He intends employing three of his college friends to develop more ideas for ‘apps’, and plans to adopt a democratic leadership style. He contacted his local County Enterprise Board for assistance.')
add(2, 4, 'a', 'Q4(A)', snap + '\n\n' + L(2, 8, '(A) Outline three enterprising characteristics/skills displayed by Shane.'), 15, 'business-1-5', 'shane-enterprising-skills',
    8, [18], 'Three at 5 marks each (3 + 2).', points('Characteristic', 3, (3, 2)))
add(2, 4, 'b', 'Q4(B)', snap + '\n\n' + L(2, 8, '(B) Outline two risks and two rewards for Shane setting up his own business.'), 20, 'business-1-5', 'shane-risks-and-rewards',
    8, [18], 'Two risks and two rewards at 5 marks each (3 + 2).', seq(points('Risk', 2, (3, 2)), points('Reward', 2, (3, 2))))
add(2, 4, 'c', 'Q4(C)', snap + '\n\n' + L(2, 8, '(C) Explain two features of a democratic leadership style.'), 15, 'business-2-11', 'democratic-leadership-2013',
    8, [18], EIGHT, eight_seven('Feature'), [UNTIED])
add(2, 4, 'd', 'Q4(D)', snap + '\n\n' + L(2, 8, '(D) Explain two benefits of teamwork in ‘Snapappy’.'), 15, 'business-3-20', 'snapappy-teamwork',
    8, [18], EIGHT, eight_seven('Benefit'), [UNTIED])
add(2, 4, 'e', 'Q4(E)', snap + '\n\n' + L(2, 8, '(E) Outline two services provided by County/City Enterprise Boards.'), 10, 'business-5-16', 'enterprise-board-services',
    8, [18], 'Two services at 5 marks each (3 + 2).', points('Service', 2, (3, 2)), extra=['business-1-5'])

flaxco = (L(2, 8, 'FLAXCO LTD') + '\n' + L(2, 8, 'Frank Mahon is the Managing Director of Flaxco Ltd. The AGM of the company is to be held in The Marriot Hotel, Rathmines on Friday 19th July 2013 at 3.00 p.m. Flaxco Ltd needs to reduce its costs and will not be able to pay a dividend this year. At the AGM Frank needs to make the shareholders aware of this and knows the importance of delivering this message clearly.')
          + '\n(dividend and shareholders are underlined.)')
add(2, 5, 'a', 'Q5(A)', flaxco + '\n\n' + L(2, 8, '(A) What do the letters AGM stand for?'), 5, 'business-2-12', 'agm-letters', 8, [19], 'AGM in full: 5 marks (2 + 2 + 1).',
    [comps('AGM', (5,), ['Words written in full'])], ['Answer: ' + S(19, 'AGM: Annual General Meeting') + '.'])
add(2, 5, 'b', 'Q5(B)', flaxco + '\n\n' + L(2, 8, '(B) Explain the terms underlined above.'), 15, 'business-5-14', 'dividend-and-shareholders',
    8, [19], 'Dividend 8 (4 + 4) and shareholders 7 (4 + 3).', [comps('Dividend', (4, 4), i=1), comps('Shareholders', (4, 3), i=2)],
    ['Scheme: ' + S(19, 'Dividend – this is the share of the profits given to owners (shareholders) after tax has been paid.') + ' '
     + S(19, 'Shareholders – owners of a business who invest their own money with the hope of making a profit.')])
flat(add(2, 5, 'c', 'Q5(C)', flaxco + '\n\n' + L(2, 8, '(C) Draft the Notice and Agenda of the AGM of Flaxco Ltd sent by the company secretary, Miriam Hannon. (The Agenda must contain at least five items.)'), 25,
         'business-2-12', 'flaxco-notice-and-agenda', 8, [19], 'Notice five items at 2 each, the heading Agenda 1, five agenda items at 2 each, signature 2 and title 2.',
         seq(comps('Notice', (2, 2, 2, 2, 2), ['Notice item 1', 'Notice item 2', 'Notice item 3', 'Notice item 4', 'Notice item 5']),
             comps('Agenda heading', (1,), ['Agenda']),
             comps('Agenda items', (2, 2, 2, 2, 2), ['Agenda item 1', 'Agenda item 2', 'Agenda item 3', 'Agenda item 4', 'Agenda item 5']),
             comps('Signature', (2, 2), ['Signed (Miriam Hannon)', 'Title (Company Secretary)'])),
         ['Scheme (page 19): ' + S(19, 'The AGM of Flaxco Ltd. will be held in The Marriot Hotel, Rathmines, on Friday 19th July 2013 at 3.00 pm.') + ' Agenda: '
          + S(19, '1. Minutes of AGM 2012 2. Matters arising from minutes 3. Chairperson’s Report 4. Auditor’s Report 5. Declaration of Dividend') + ' ...',
          'The allocation summary prints “' + S(7, 'Notice: 5 items @ 2m each ‘Agenda’ 1 mark Agenda contents: 5 items @ 2m each Signature: 2 marks Title: 2 marks') + '”.']))
add(2, 5, 'd', 'Q5(D)', flaxco + '\n\n' + L(2, 8, '(D) Outline two functions of the Managing Director of a company.'), 15, 'business-2-13', 'managing-director-functions',
    8, [19], EIGHT, eight_seven('Function'), [UNTIED])
add(2, 5, 'e', 'Q5(E)', flaxco + '\n\n' + L(2, 8, '(E) Name and explain two barriers to effective communication.'), 15, 'business-2-12', 'communication-barriers',
    8, [20], EIGHT, eight_seven('Barrier'), [UNTIED])

liscarrig = L(2, 9, 'Liscarrig Equestrian Centre The Liscarrig Equestrian Centre provides individual and group horse riding lessons. It has a café and an activity centre for children. There are 12 full-time staff and 10 seasonal staff employed. Susanne Carey is the Office Manager and she looks after all the finances in the business. Liscarrig Equestrian Centre wants to purchase eight acres of land to expand the Centre and Susanne is currently preparing a Business Plan and a Cash Flow Forecast to assist its application for a bank loan.').replace('Liscarrig Equestrian Centre The', 'Liscarrig Equestrian Centre\nThe', 1)
L(2, 9, '2013 July August September')
cash = '\n'.join([L(2, 9, 'Liscarrig Equestrian Centre CASH FLOW FORECAST JULY-SEPT 2013'), 'Columns: July, August, September',
                  L(2, 9, 'Total Receipts (A) 42,000 40,000 26,000'), L(2, 9, 'Total Payments (B) 35,000 34,000 20,000'), L(2, 9, 'Net Cash (A-B) 7,000 6,000 6,000'),
                  L(2, 9, 'Opening Cash 2,000 9,000 15,000'), L(2, 9, 'Closing Cash 9,000 15,000 21,000')])
add(2, 6, 'a', 'Q6(A)', liscarrig + '\n\n' + L(2, 9, '(A) Outline four types of insurance you would expect Liscarrig Equestrian Centre to have.'), 20, 'business-3-17', 'equestrian-insurance-types',
    9, [21], 'Four types at 5 marks each (3 + 2).', points('Type of insurance', 4, (3, 2)))
add(2, 6, 'b', 'Q6(B)', liscarrig + '\n\n' + L(2, 9, '(B) Outline two responsibilities Liscarrig Equestrian Centre has towards its employees.'), 10, 'business-5-17', 'responsibilities-to-employees',
    9, [21], 'Two responsibilities at 5 marks each (3 + 2).', points('Responsibility', 2, (3, 2)), extra=['business-0-12'])
cum(2, 6, 'c', 'Q6(C)', liscarrig + '\n\n' + cash + '\n\n' + L(2, 9, '(C) List two items that would be included in the payments section of the above Cash Flow forecast.'), (5, 5), 'business-3-16',
    'cash-flow-payment-items', 9, [21], 'Scheme examples (page 21): ' + bullets(S(21, '• Insurance • Electricity • Wages • Raw Materials/Supplies • Fuel • Horse feed/tack.')), noun='items')
add(2, 6, 'd', 'Q6(D)', liscarrig + '\n\n' + L(2, 9, '(D) Explain two factors a bank should consider before giving Liscarrig Equestrian Centre a bank loan.'), 15, 'business-3-16', 'bank-loan-factors-2013',
    9, [21], EIGHT, eight_seven('Factor'), [UNTIED])
add(2, 6, 'e', 'Q6(E)', liscarrig + '\n\n' + cash + '\n\n' + L(2, 9, '(E) Based on the Cash Flow forecast above, would you advise the bank to give Liscarrig Equestrian Centre the loan? Outline two reasons for your answer.'), 20,
    'business-3-16', 'advise-on-the-loan', 9, [21], 'Yes or No 2, and two reasons at 9 marks each (5 + 4).', seq(single('Advice', 2, 'Yes or No stated'), points('Reason', 2, (5, 4))),
    ['Either answer can earn full marks with reasons. Scheme reasons for Yes: ' + S(21, '• Positive cash flow for 3 months') + ' ...; for No: ' + S(21, '• Sales peak in Summer') + ' ...'])

ace = L(2, 10, 'SPRAOI') + '\n' + L(2, 10, 'ACE Toys Ltd is a successful Irish toy manufacturer. It uses a ‘Batch Production’ process. Each year it develops new products for the Christmas period, selling to the Irish and international markets. This year ACE Toys Ltd has produced ‘SPRAOI’ an interactive games console which uses basic Irish language, aimed at children aged 7-11. ACE Toys Ltd have set up a website called www. acetoys.com.')
add(2, 7, 'a', 'Q7(A)', ace + '\n\n' + L(2, 10, '(A) Explain what is meant by the term ‘Batch Production’.'), 10, 'business-4-15', 'batch-production-explained-2013', 10, [22],
    'Explanation: 10 marks (5 + 5).', [comps('Batch production', (5, 5))],
    ['Scheme: ' + S(22, 'A certain amount or limited quantity of a product is produced at the same time and then production switches to a different batch or group.')])
add(2, 7, 'b', 'Q7(B)', ace + '\n\n' + L(2, 10, '(B) Describe two internal and two external sources of new product ideas for ACE Toys Ltd.'), 20, 'business-4-14', 'internal-and-external-idea-sources',
    10, [22], 'Two internal and two external sources at 5 marks each.', seq(points('Internal source', 2, (5,)), points('External source', 2, (5,))),
    ['Scheme examples: internal ' + bullets(S(22, '• R & D Department • Brainstorming • Sales team feedback'), ', ') + '; external copying competitors’ ideas, new trends, customer feedback, import substitution.'])
flat(add(2, 7, 'c', 'Q7(C)', ace + '\n\n' + L(2, 10, '(C) Draft and label the Product Life Cycle for ‘SPRAOI’.'), 15, 'business-4-17', 'spraoi-product-life-cycle', 10, [22],
         'Five ordered stages at 2 each, the two labelled axes 1 each and a correct diagram 3.',
         [fixed('Product life cycle diagram', [('Sales axis', 1), ('Time axis', 1), ('Correct diagram', 3), ('Introduction', 2), ('Growth', 2), ('Maturity', 2), ('Saturation', 2), ('Decline', 2)])],
         ['Scheme (page 22): ' + S(22, 'SALES INTRODUCTION GROWTH MATURITY SATURATION DECLINE TIME') + '; the summary prints “' + S(8, 'Product Life Cycle: 5 ordered stages @ 2 marks each 2 labelled axes @ 1 mark each Correct diagram: 3 marks') + '”.']))
add(2, 7, 'd', 'Q7(D)', ace + '\n\n' + L(2, 10, '(D) Outline two benefits for ACE Toys Ltd of having its own website.'), 10, 'business-2-12', 'own-website-benefits',
    10, [23], 'Two benefits at 5 marks each (3 + 2).', points('Benefit', 2, (3, 2)), extra=['business-4-17'])
add(2, 7, 'e', 'Q7(E)', ace + '\n\n' + L(2, 10, '(E) Choose a suitable advertising medium to bring ‘SPRAOI’ to the attention of consumers, and outline two reasons for your choice.'), 20, 'business-4-17',
    'spraoi-advertising-medium', 10, [23], 'The medium 6, and two reasons at 7 each (4 + 3).', seq(single('Advertising medium', 6, 'Medium chosen'), points('Reason', 2, (4, 3))),
    ['Scheme media (page 23): TV, radio, magazines/newspapers, internet, billboards, direct mail; ' + S(23, 'Reasons specific to the medium chosen:') + ' suitable for the product, wide audience, specific target market, cost.'])

juices = L(2, 11, 'IRISH NATURAL JUICES LTD') + '\n' + L(2, 11, 'Thomas McCann, of Irish Natural Juices Ltd, identified a gap in the market for an Irish brand of organic fruit juice. Thomas is working on the concept development stage of the Product Development process. He is working on the design of a brand name and developing a Unique Selling Point (USP) for the fruit juice.')
add(2, 8, 'a', 'Q8(A)', juices + '\n\n' + L(2, 11, '(A) Explain three advantages of giving the organic fruit juice a brand name.'), 20, 'business-4-17', 'brand-name-advantages-2013',
    11, [24], 'Three advantages: 7 (4 + 3), 7 (4 + 3) and 6 (3 + 3).', unequal('Advantage', [(4, 3), (4, 3), (3, 3)], None),
    ['The 7/7/6 sequence prices the three advantages, not particular advantages.'])
add(2, 8, 'b', 'Q8(B)', juices + '\n\n' + L(2, 11, '(B) Explain what is meant by the term ‘Unique Selling Point’ (USP).'), 10, 'business-4-17', 'usp-explained',
    11, [24], 'Explanation: 10 marks (5 + 5).', [comps('Unique Selling Point', (5, 5))],
    ['Scheme: ' + S(24, 'The USP or Unique Selling Point of a product is the feature or characteristic that differentiates that product from its competitors.')])
add(2, 8, 'c', 'Q8(C)', juices + '\n\n' + L(2, 11, '(C) Explain two of the following stages in the Product Development Process: (i) Idea Generation; (ii) Prototype Development; (iii) Test Marketing.'), 15,
    'business-4-14', 'development-stages-choice-2013', 11, [24], 'Choose two of the three stages and explain each: 8 (4 + 4) and 7 (4 + 3).',
    seq(comps('First stage you chose', (4, 4)), comps('Second stage you chose', (4, 3))),
    ['You choose which two of the three printed stages to answer. The scheme marks every choice alike, so this is one card whichever stages you choose.',
     'The 8-mark allowance is not tied to a particular stage.',
     'Idea Generation (scheme PDF page 24): “' + S(24, 'this involves coming up with new ideas for a new or improved product.') + '”',
     'Prototype Development (scheme PDF page 24): “' + S(24, 'this involves making a first model of a new product.') + '”',
     'Test Marketing (scheme PDF page 24): “' + S(24, 'this involves testing a new product on a small number of potential customers to gauge their reaction and get feedback.') + '”'])
advert = L(2, 11, 'IRISH NATURAL JUICES LTD FINANCE MANAGER REQUIRED The ideal candidate: Will have a Business Degree, excellent leadership, communication and analytical skills. Two years experience in a similar role is essential. The position: Involves managing the Finance Department. Responsibilities include: Preparation of monthly and annual accounts. Apply by 1st August 2013 with a letter of application, including a CV to: Marion Pender, HR Manager, Irish Natural Juices Ltd, Newtown Industrial Park, Newtown, Co. Tipperary. Irish Natural Juices Ltd is an Equal Opportunities Employer')
letter = add(2, 8, 'd', 'Q8(D)', advert + '\n\n' + L(2, 11, '(D) Deirdre Keegan, 37 Oaklands, Athlone, Co. Westmeath applied for the position advertised. Using today’s date, draft Deirdre’s letter of application.'), 20,
             'business-2-12', 'letter-of-application', 11, [25],
             'Sender’s and receiver’s addresses and the date 2 each; reference, opening and closing salutations and signature 1 each; ten points of content at 1 each.',
             [response(1, 'Letter of application', [('sender', 'Sender’s address', 2), ('receiver', 'Receiver’s address', 2), ('date', 'Date', 2), ('reference', 'Reference', 1),
                                                     ('opening', 'Opening salutation', 1), ('closing', 'Closing salutation', 1), ('signature', 'Signature', 1),
                                                     ('contents', 'Contents: ten points at 1 each', 10)])],
             ['The allocation summary prints “' + S(8, 'Letter of application: Sender’s Address 2m Receiver’s Address 2m Date 2m Reference 1m Opening Salutation 1m Closing Salutation 1m Signature 1m Contents: 10 points @ 1m each') + '”.',
              'Scheme sample (page 25): ' + S(25, 'Re: Finance Manager Position') + '; ' + S(25, 'I refer to your advertisement for the position of Finance Manager at Irish Natural Juices Ltd.') + ' ...'],
             extra=['business-3-20'])
for a in letter['rubric']['responses'][0]['allocations']:
    if a['id'] != 'contents':
        a['permittedMarks'] = [0, a['maxMarks']]
add(2, 8, 'e', 'Q8(E)', advert + '\n\n' + L(2, 11, '(E) Explain the term ‘Equal Opportunities Employer’.'), 10, 'business-0-14', 'equal-opportunities-employer',
    11, [25], 'Explanation: 10 marks (5 + 5).', [comps('Equal Opportunities Employer', (5, 5))],
    ['Scheme: ' + S(25, 'An Equal Opportunities Employer is a company that will hire people without discriminating against gender, marital status, family status, religion, age, race, disability, sexual orientation or membership of the travelling community.')], extra=['business-3-20'])

# ---------------------------------------------------------------- checks and write-out
qn = lambda c: c['questionRef'].split(' Q')[1].split('(')[0]
for section, count, total in [('1', 15, 10), ('2', 8, 75)]:
    for q in range(1, count + 1):
        got = sum(c['totalMarks'] for c in P.created if c['section'] == section and qn(c) == str(q))
        assert got == total, (section, q, got)
assert not [i for i in ORIGINAL if i.startswith('bus-2013-ol-')]
assert not P.pools

SELECTION = {
    1: 'No finite printed answer menu occurs in Section 1 (answer ten of fifteen at 10 marks). The ticks in Q7, DESK/FIELD in Q9, the matching rows in Q13 and TRUE/FALSE in Q14 are required answer formats. Support-note lists are open examples.',
    2: 'One printed choice is one card: Q8(C) any two of the three product-development stages (8 and 7, marked alike). Q3(E) asks for the role of one of the two institutions the candidate names and Q7(E) for a medium of their choice; both are open. Q4(B) requires two risks and two rewards. Support-note lists are open examples.',
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
    if m == 'two of' and own(w, m, 'Explain two of the following stages'):
        return 'finite-choice', 'Section 2 Q8(C) asks for any two of the three printed product-development stages. The scheme marks every choice alike (8 and 7), so one card carries all three with the scheme wording for each.', 'bus-2013-ol-s2-q8c'
    if m == 'one of' and own(w, m, 'explain the role of one of them'):
        return 'open-response', 'Section 2 Q3(E) asks for the role of one of the two institutions the candidate names; the list is their own and the scheme marks any institution alike, so it is one card.', None
    if m == 'Choose' and own(w, m, 'Choose a suitable advertising medium'):
        return 'open-response', 'Section 2 Q7(E) asks the candidate to choose a medium and justify it; no list is printed, so it is one card.', None
    if m == 'three of' and own(w, m, 'employing three of his college friends'):
        return 'case-context', '“three of his college friends” is wording inside the Section 2 Q4 extract, not a choice of task.', None
    if m == 'or' and own(w, m, 'DESK or FIELD'):
        return 'required-headings', 'DESK/FIELD are answer labels for each of the five required techniques in Section 1 Q9, not optional tasks.', None
    if m == 'or' and own(w, m, 'TRUE or FALSE'):
        return 'required-headings', 'TRUE/FALSE are answer labels for each of the five required statements in Section 1 Q14, not optional tasks.', None
    if m == 'or' and (own(w, m, 'good or service belongs') or own(w, m, 'eight or more members')):
        return 'case-context', 'Wording inside a printed instruction or explanation (Section 1 Q7, Q13), not a choice of task.', None
    assert (fileid, page) in {('LC033GLP000EV', 1), ('LC033GLP000EV', 6)} and m in ('either', 'or'), (fileid, page, m, w)
    return 'exam-navigation', 'The cover and Section 2 rubrics set how many whole questions a candidate answers (one from Part 1, two from Part 2 and one other from either part). Every numbered question remains in the practice corpus as separate cards.', None


n = P.write([(1, range(1, 16)), (2, range(1, 9))], SELECTION, classify,
            'Every part of {year} Ordinary Section {section} Question {q} was visually checked against its SEC paper, allocation summary and support notes. The single-booklet identity keeps the short (n) and long (S2Q) question numbering apart.')
print(f'Reviewed {len(P.created)} 2013 Ordinary tasks; classified {n} raw selection matches.')
