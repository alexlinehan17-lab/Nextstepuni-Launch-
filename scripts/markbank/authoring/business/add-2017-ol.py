"""Review the 2017 Ordinary English paper (one booklet: Section 1 and Section 2).

2017: answer ten of fifteen short questions at 10 marks and four of eight
long questions at 75 (one from Part 1, two from Part 2 and one other), all in
one twelve-page booklet (LC033GLP000EV, the same file id as its scheme). No
Ordinary card existed for 2017, so every card is new. The allocation summary
(scheme pages 4-7) sets each boundary. Two printed choices are one card each:
Section 2 Q1(A) any two of three Consumer Protection Act provisions and Q6(A)
any three of four underlined terms (the scheme marks every choice alike).
Printed sub-parts with their own published marks are separate cards, Q7(C)'s
inline (i) the Business and (ii) the Consumer (10 each) among them.
Page 10's text layer also carries "(C) Explain the difference between 'on the
job training' and 'off the job training'. (10 marks)" under the white box of
the Q6(C) extract. The printed page does not show it and the scheme does not
mark it (Q6 is 75 without it), so it has no card.
"""
from bus_lib import (Paper, ORIGINAL, comps, points, seq, unequal, single, response, fixed, permit)

T = {(1, q): 4 for q in range(1, 16)}
T.update({(2, 1): 5, (2, 2): 5, (2, 3): 5, (2, 4): 6, (2, 5): 6, (2, 6): 7, (2, 7): 7, (2, 8): 7})
P = Paper(2017, 'ordinary', {1: 'LC033GLP000EV', 2: 'LC033GLP000EV'}, 'LC033GLP000EV', T)
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


def evens(card):
    return permit(card, 0, list(range(0, card['totalMarks'] + 1, 2)))


# ---------------------------------------------------------------- Section 1 (10 marks each)
add(1, 1, '', 'Q1', L(1, 2, 'What do the following letters stand for? Write each answer in the space provided.') + '\nUSC\nCEO\nSWOT', 10, 'business-3-18',
    'abbreviations-usc-ceo-swot', 2, [8], 'The first and second correct terms earn 3 each (1 + 1 + 1); the third 4 (1 + 1 + 1 + 1).',
    [comps('First correct term', (3,), ['Words written in full'], 1), comps('Second correct term', (3,), ['Words written in full'], 2),
     comps('Third correct term', (4,), ['Words written in full'], 3)],
    ['Answer key: USC ' + S(8, 'Universal Social Charge') + '; CEO ' + S(8, 'Chief Executive Officer') + '; SWOT ' + S(8, 'Strengths Weaknesses Opportunities Threats') + '.'],
    extra=['business-2-13'])
L(1, 2, 'Topshop Asos Boohoo (A) USC CEO SWOT')
cum(1, 2, '', 'Q2', L(1, 2, 'List three elements of a valid contract.'), (4, 3, 3), 'business-0-12', 'valid-contract-elements', 2, [8],
    'Scheme elements (page 8): ' + bullets(S(8, '• Agreement/Offer/Acceptance • Consideration • Intention to contract • Consent to contract • Capacity to contract • Legality of form • Legality of purpose')) + '.',
    noun='elements')
chart = (L(1, 2, 'Most popular online clothes retailer amongst a sample of third level students.') + ' (bar chart: ' + L(1, 2, 'No of students')
         + ', 0 to 30, for 2015, 2016 and 2017, with bars for Topshop, Asos and Boohoo — read the bars on the printed page.)')
L(1, 2, '0 10 20 30 2015 2016 2017 No of students')
memo = (L(1, 2, 'To: All Staff From: Sales Manager Date: 15th July 2016 Re: Commission Scheme Commission will increase to 8% of sales for the month of August. Signed: Michael Barron Michael Barron Sales Manager')
        .replace(' From:', '\nFrom:').replace(' Date:', '\nDate:').replace(' Re:', '\nRe:').replace(' Commission will', '\nCommission will').replace(' Signed:', '\nSigned:'))
flat(add(1, 3, '', 'Q3', L(1, 2, '(i) Identify the methods of communication used to convey the information in (A) and (B) and (ii) answer the question relating to each method of communication.')
         + '\n\n(A) ' + chart + '\n' + L(1, 2, '(i) A =') + '\n' + L(1, 2, '(ii) From the data, identify which website was the most popular online clothes retailer amongst the sample of students in 2015.')
         + '\n\n(B) ' + memo + '\n' + L(1, 2, '(i) B =') + '\n' + L(1, 2, '(ii) From the data, identify the sender and receiver of this information.') + '\nSender =\nReceiver =',
         10, 'business-2-12', 'communication-methods-chart-and-memo', 2, [8], 'A: the method 3 and the answer 2. B: the method 3, the sender 1 and the receiver 1.',
         [response(1, '(A) The bar chart', [('method', '(i) Method: bar chart / visual communication', 3), ('answer', '(ii) Topshop', 2)]),
          response(2, '(B) The memo', [('method', '(i) Method: memorandum / written communication', 3), ('sender', 'Sender: Michael Barron / Sales Manager', 1),
                                       ('receiver', 'Receiver: All Staff', 1)])],
         ['Scheme (page 8): ' + S(8, 'A. (i) Bar Chart/Visual communication. (ii) Most popular online clothes retailer: Topshop B. (i) Memorandum (Memo)/Written communication. (ii) Sender: Michael Barron/Sales Manager Receiver All Staff') + '.']))
cum(1, 4, '', 'Q4', L(1, 2, 'List the three other elements of the Marketing Mix.') + '\n______ | ' + L(1, 2, 'PRICE') + ' | ______ | ______', (4, 3, 3), 'business-4-17',
    'other-marketing-mix-elements', 2, [8], 'Answer key (scheme page 8): Product, Promotion and Place (' + S(8, 'PRODUCT PRICE PROMOTION PLACE') + '; Price is printed).', noun='elements')
add(1, 5, '', 'Q5', L(1, 3, 'Explain one use of each of the following computer software programs for a business.', '(i) Microsoft Word', '(ii) Microsoft Excel'), 10,
    'business-2-12', 'word-and-excel-uses', 3, [9], 'Each use 5 marks.', [comps('Microsoft Word', (5,), ['Use explained'], 1), comps('Microsoft Excel', (5,), ['Use explained'], 2)],
    ['Scheme: ' + S(9, '(i) Microsoft Word – To prepare reports, the agenda/minutes of a meeting, letters, business documents, invoices.') + ' '
     + S(9, '(ii) Microsoft Excel – To prepare financial accounts, budgets, customer databases, bar charts, spreadsheets, cash flow, sales records.')])
L(1, 3, '2016 Sales €220,000 Gross Profit €99,000 Net Profit €55,000')
flat(add(1, 6, '', 'Q6', L(1, 3, 'Healthy Foods Ltd is examining the profits made by the business. From the information below, calculate the Gross Profit percentage and Net Profit percentage for 2016. Show all workings in the spaces provided.')
         + '\n2016: Sales €220,000; Gross Profit €99,000; Net Profit €55,000\nGross Profit Percentage (i)\nNet Profit Percentage (ii)', 10, 'business-3-19',
         'gross-and-net-profit-percentage', 3, [9], 'Each percentage 5: workings 4 and the answer 1.',
         [response(1, 'Gross Profit Percentage', [('workings', 'Workings: 99,000 / 220,000 x 100', 4), ('answer', 'Answer: 45%', 1)]),
          response(2, 'Net Profit Percentage', [('workings', 'Workings: 55,000 / 220,000 x 100', 4), ('answer', 'Answer: 25%', 1)])],
         ['Scheme (page 9): ' + S(9, 'Gross Profit Percentage (i) 99,000 x 100 = 45% 220,000') + '; ' + S(9, 'Net Profit Percentage (ii) 55,000 x 100 = 25% 220,000')
          + '; ' + S(9, '1m for correct answer. 4m for workings.')]))
add(1, 7, '', 'Q7', L(1, 3, 'Choose the appropriate words to complete the sentence below. (Two words do not apply.)', 'SUPPLIERS EMPLOYEES IDEAS SALARIES')
    + '\nIntrapreneurship involves ______ ' + L(1, 3, 'in a business coming up with new') + ' ______ ' + L(1, 3, 'to help improve the business.'), 10, 'business-1-5',
    'intrapreneurship-word-bank', 3, [9], 'Each blank earns 5 marks.', [fixed('Completed blanks', [('First blank', 5), ('Second blank', 5)])],
    ['Answer key (scheme page 9): ' + S(9, 'Intrapreneurship involves EMPLOYEES in a business coming up with new IDEAS to help improve the business.') + ' Suppliers and Salaries are not used.'])
L(1, 3, 'Intrapreneurship involves')
cum(1, 8, '', 'Q8', L(1, 3, 'List three grounds on which discrimination is outlawed under the Employment Equality Act 1998.'), (4, 3, 3), 'business-0-14',
    'employment-equality-grounds', 3, [9], 'Scheme grounds (page 9): ' + bullets(S(9, '• Gender – male/female • Marital Status – single/married/separated/divorced • Family Status – family/pregnancy • Religious belief (or none) • Age • Race – originate from another country/colour of skin • Disability – physical/ mental disability • Sexual Orientation – sexual preference • Membership of Travelling Community.')),
    noun='grounds')
add(1, 9, '', 'Q9', L(1, 4, 'Outline two benefits of quality control for a business.'), 10, 'business-2-13', 'quality-control-benefits', 4, [9],
    'Two benefits at 5 marks each (3 + 2).', points('Benefit', 2, (3, 2)),
    ['Scheme examples: ' + S(9, 'Consistent standard of products: The business develops a reputation for producing quality products / offering services of a very high standard.')
     + ' ' + S(9, 'Reduced Costs: Less faulty products, less waste.')])
cum(1, 10, '', 'Q10', L(1, 4, 'Indicate by means of a tick (✓) in the correct box, the method of expansion to which each statement below relates:',
                        'Statement Merger Takeover Franchise Strategic Alliance', 'Apple buys Beats by Dr Dre for $3bn.',
                        'Avonmore Foods plc and Waterford Foods plc joined forces to form Glanbia plc.',
                        'Irish grocery retailer SuperValu has announced a new partnership with Bank of Ireland as part of its ‘Real Rewards’ loyalty programme.',
                        'The Zip Yard have expanded by allowing other parties to use the business model and trademark in exchange for a fee and a percentage of profits.'),
    (4, 3, 2, 1), 'business-4-18', 'expansion-method-ticks', 4, [10],
    'Answer key (ticks on scheme page 10): Apple and Beats Takeover; Avonmore and Waterford (Glanbia) Merger; SuperValu and Bank of Ireland Strategic Alliance; The Zip Yard Franchise.',
    extra=['business-5-14'], noun='ticks')
add(1, 11, '', 'Q11', L(1, 4, 'Indicate the term below that refers to trade union members voting on industrial action. Tick (✓) the correct box.', 'Picketing Secret Ballot Work to rule'),
    10, 'business-0-14', 'secret-ballot-tick', 4, [10], 'The correct box earns 10 marks.', [single('Correct box', 10, 'Term ticked')],
    ['Answer key (tick on scheme page 10): Secret Ballot.'])
cum(1, 12, '', 'Q12', L(1, 4, 'Name two European Union institutions.'), (5, 5), 'business-6-14', 'eu-institutions-named', 4, [10],
    'Scheme institutions (page 10): ' + bullets(S(10, '• European Commission • European Parliament • EU Council • European Central Bank • European Court of Justice • European Court of Auditors')) + '.',
    noun='institutions')
add(1, 13, '', 'Q13', L(1, 5, '(i) Explain the term Visible Imports.', '(ii) Explain the term Invisible Exports.'), 10, 'business-6-13', 'visible-imports-invisible-exports',
    5, [10], 'Each explanation 5 marks (3 + 2).', [comps('Visible Imports', (3, 2), i=1), comps('Invisible Exports', (3, 2), i=2)],
    ['Scheme: ' + S(10, 'Businesses and people buying physical products from foreign countries.') + ' '
     + S(10, 'Businesses selling services from one country to other foreign countries/to customers in other countries.')])
cum(1, 14, '', 'Q14', L(1, 5, 'Write TRUE or FALSE after each of the following statements.',
                        'A loading is a reduction on the basic insurance premium charge because the customer insuring has a lower risk of claiming.',
                        'Corporation Tax is a tax paid on the profits made by a company.', 'Commercial rates are a tax paid by businesses to their local council.',
                        'Indemnity is a principle of insurance that states you must reveal all relevant information when applying for insurance.',
                        'Utmost good faith is a principle of taxation.'),
    (2, 2, 2, 2, 2), 'business-3-17', 'insurance-and-tax-true-false', 5, [11], 'Answer key (scheme page 11): FALSE; TRUE; TRUE; FALSE; FALSE.', extra=['business-3-18'])
cum(1, 15, '', 'Q15', '\n'.join([L(1, 5, 'Column 1 is a list of stakeholders in a business. Column 2 is a list of explanations for these stakeholders. One explanation has no match. Match the two lists by placing the letter of the correct explanation under the relevant number below.'),
                                 L(1, 5, '1. Government', '2. Consumer', '3. Investor', '4. Manager', '5. Supplier'),
                                 L(1, 5, 'A. Has the idea and the initiative to take the risk of setting up a business.',
                                   'B. Engages in the activities of planning, organising and controlling the business on a daily basis in return for a salary.',
                                   'C. Provides raw materials that are used in production.', 'D. Provides capital in the hope of a financial return/gain.',
                                   'E. Provides essential services for the citizens in a country using the money collected in taxation to fund public spending.',
                                   'F. Buys goods and services for his/her own use.')]),
    (2, 2, 2, 2, 2), 'business-0-12', 'stakeholder-matching', 5, [11], 'Answer key (scheme page 11): 1 E; 2 F; 3 D; 4 B; 5 C. Explanation A is unused.', noun='matches')
S(11, '1. 2. 3. 4. 5. E F D B C')

# ---------------------------------------------------------------- Section 2 (75 marks each)
seamus = L(2, 6, 'The Savvy (Informed) Consumer', 'Seamus is a Leaving Certificate Business student who did a classroom presentation based on Consumer law. Seamus discussed the Consumer Protection Act 2007 and informed the class that the law prohibits (bans) false or misleading claims about goods, services and prices. Seamus presented various examples of false and misleading advertising and examples of false prices. Seamus encouraged his classmates to visit the website www.consumerhelp.ie for important consumer information.')
add(2, 1, 'a', 'Q1(A)', seamus + '\n\n' + L(2, 6, '(A) Explain by means of examples any two of the following provisions of the Consumer Protection Act 2007:',
                                             '(i) “Prohibits false or misleading advertising”', '(ii) “Prohibits false prices”', '(iii) “Prohibits false product descriptions”.'),
    20, 'business-0-13', 'consumer-protection-provisions-choice', 6, [12], 'Choose two of the three provisions and explain each with an example: 15 (10 + 5) and 5 (4 + 1).',
    seq(comps('First provision you chose', (10, 5)), comps('Second provision you chose', (4, 1))),
    ['You choose which two of the three printed provisions to answer. The scheme marks every choice alike, so this is one card whichever provisions you choose.',
     'The 15-mark allowance is not tied to a particular provision. The scheme notes: ' + S(12, '[Accept a relevant explanation or a relevant example.]'),
     'False or misleading advertising (scheme PDF page 12): “' + S(12, 'It gives consumers wrong information about goods or services they intend to buy.') + '”',
     'False prices (scheme PDF page 12): “' + S(12, 'It is illegal for a business to make false/misleading claims about prices.') + '”',
     'False product descriptions (scheme PDF page 12): “' + S(12, 'It is illegal for a business to give false product descriptions to its goods.') + '”'])
law = add(2, 1, 'b', 'Q1(B)', L(2, 6, 'Consumers in Ireland are also protected in relation to the sale of goods, hire purchase agreements and contracts for the supply of services. www.consumerhelp.ie')
          + '\n\n' + L(2, 6, '(B) Name a consumer law, other than the Consumer Protection Act 2007, that protects consumers in Ireland.'), 10, 'business-0-13', 'other-consumer-law',
          6, [12], 'Name the law: 5 @ 2 marks.', [comps('Consumer law', (10,), ['Act named'])], ['Answer: ' + S(12, 'The Sale of Goods and Supply of Services Act 1980') + ' (scheme: 2 + 2 + 2 + 2 + 2).'])
evens(law)
asti = L(2, 6, 'The ASTI, a trade union representing second-level teachers, voted in October 2016 to take industrial action up to and including strike action.')
add(2, 1, 'c', 'Q1(C)', asti + '\n\n' + L(2, 6, '(C) Outline three benefits of being a member of a trade union.'), 20, 'business-0-14', 'trade-union-membership-benefits',
    6, [13], 'Three benefits: 8 (6 + 2), 8 (6 + 2) and 4 (2 + 2).', unequal('Benefit', [(6, 2), (6, 2), (2, 2)], None),
    ['The 8/8/4 sequence prices the three benefits, not particular benefits.'])
add(2, 1, 'd', 'Q1(D)', asti + '\n\n' + L(2, 6, '(D) Outline two effects of industrial disputes.'), 10, 'business-0-14', 'industrial-dispute-effects',
    6, [13], 'Two effects: 6 and 4.', unequal('Effect', [(6,), (4,)], None), ['The 6-mark allowance is not tied to a particular effect.'])
add(2, 1, 'e', 'Q1(E)', asti + '\n\n' + L(2, 6, '(E) Outline two functions of a shop steward.'), 15, 'business-0-14', 'shop-steward-functions',
    6, [13], 'Two functions: 8 and 7.', unequal('Function', [(8,), (7,)], None), ['The 8-mark allowance is not tied to a particular function.'])

tourism = L(2, 7, 'Tourism initiatives such as the “Wild Atlantic Way”, “The Ancient East” and “The Gathering” have helped to boost business sales in Ireland. The Wild Atlantic Way has boosted the reputation of Ireland as a holiday destination. Communities throughout the West of Ireland have experienced increased visitor numbers. Local construction firms have been busy as new businesses such as hostels, restaurants and cafes have been established. Farmers and fishermen have experienced an increase in demand for their raw materials from local restaurants, cafes and bars.')
add(2, 2, 'a', 'Q2(A)', tourism + '\n\n' + L(2, 7, '(A) From the information provided above, name the sector of the economy that tourism operates in. State one example of a business in the tourism industry.'),
    10, 'business-5-13', 'tourism-sector-and-example', 7, [14], 'Name the sector 6 and give an example 4.',
    seq(single('Sector', 6, 'Sector named'), single('Tourism business', 4, 'Example stated')),
    ['Scheme (page 14): ' + S(14, 'Sector: Tertiary Sector/Services Sector Example: Restaurant, hotel, tour operator.')])
add(2, 2, 'b', 'Q2(B)', tourism + '\n\n' + L(2, 7, '(B) Explain the two other sectors of the economy and provide one example of a business in each sector from the information provided above.'),
    20, 'business-5-13', 'primary-and-secondary-sectors-explained', 7, [14], 'Each sector 10 marks (3 + 4 + 3).',
    [comps('Primary sector', (3, 4, 3), i=1), comps('Secondary sector', (3, 4, 3), i=2)],
    ['Scheme: ' + S(14, 'Primary Sector: The Primary Sector is made up of the extractive industries.') + ' '
     + S(14, 'Example: Local farmers and fishermen have experienced an increase in demand for their raw materials from local restaurants, cafes, and bars.') + ' '
     + S(14, 'Secondary Sector: The secondary sector includes the manufacturing and construction industries.') + ' '
     + S(14, 'Example: Local construction firms building hostels, restaurants, and cafes.')])
add(2, 2, 'c', 'Q2(C)', tourism + '\n\n' + L(2, 7, '(C) Outline three benefits to a local community of a new business setting up in an area.'), 20, 'business-5-16',
    'new-business-local-community-benefits', 7, [14], 'Three benefits: 7 (4 + 3), 7 (4 + 3) and 6 (4 + 2).', unequal('Benefit', [(4, 3), (4, 3), (4, 2)], None),
    ['The 7/7/6 sequence prices the three benefits, not particular benefits.'])
vat = L(2, 7, 'The Finance Minister announced in Budget 2017 that the 9% VAT rate for businesses involved in tourism would remain. The VAT rate was reduced in 2011 from 13.5%.')
vat_i = L(2, 7, '(D) (i) What do the letters VAT stand for?')
add(2, 2, 'di', 'Q2(D)(i)', vat + '\n\n' + vat_i, 5, 'business-3-18', 'vat-letters', 7, [15], 'VAT written in full: 5 marks (2 + 2 + 1).',
    [comps('VAT', (5,), ['Words written in full'])], ['Answer: ' + S(15, 'Value Added Tax') + '.'])
add(2, 2, 'dii', 'Q2(D)(ii)', vat + '\n\n' + vat_i + '\n' + L(2, 7, '(ii) Explain two taxes, other than VAT and USC, which the government collects.'), 10, 'business-3-18',
    'other-taxes-explained', 7, [15], 'Two taxes at 5 marks each (3 + 2).', points('Tax', 2, (3, 2)),
    ['Scheme examples: PAYE, Capital Gains Tax, DIRT, Corporation Tax. ' + S(15, 'Capital Gains Tax is a tax on gains or profits made on the sale of assets.')])
add(2, 2, 'e', 'Q2(E)', vat + '\n\n' + L(2, 7, '(E) Outline two effects of the lower VAT rate on businesses involved in tourism in Ireland.'), 10, 'business-5-15',
    'lower-vat-tourism-effects', 7, [15], 'Two effects at 5 marks each (3 + 2).', points('Effect', 2, (3, 2)), extra=['business-3-18'])

brexit = L(2, 7, 'In June 2016, the UK voted to leave the European Union (EU). This became widely known as ‘Brexit’. More than €1.2 billion of goods and services are traded between the UK and Ireland every week. Brexit could result in trade barriers such as tariffs being imposed.')
cum(2, 3, 'a', 'Q3(A)', brexit + '\n\n' + L(2, 7, '(A) Apart from Ireland and the UK, name three member states in the EU.'), (4, 3, 3), 'business-6-14', 'eu-member-states',
    7, [16], 'Scheme: any EU member state other than Ireland and the UK, e.g. ' + S(16, 'Austria, Belgium, Bulgaria, Croatia') + '.', noun='member states')
tariff_i = L(2, 7, '(B) (i) Explain the term tariff.')
add(2, 3, 'bi', 'Q3(B)(i)', brexit + '\n\n' + tariff_i, 7, 'business-6-13', 'tariff-explained-2017', 7, [16], 'Explanation: 7 marks (3 + 2 + 2).',
    [comps('Tariff', (3, 2, 2))], ['Scheme: ' + S(16, 'A tariff is a tax placed on imports.')])
cum(2, 3, 'bii', 'Q3(B)(ii)', brexit + '\n\n' + tariff_i + '\n' + L(2, 7, '(ii) Name two other trade barriers.'), (4, 4), 'business-6-13', 'other-trade-barriers',
    7, [16], 'Scheme barriers (page 16): ' + S(16, 'Quota, Embargo, Subsidy, Regulations, Import/Export Licences.'), noun='barriers')
eu_i = L(2, 7, '(C) (i) Outline two advantages for Ireland of membership of the EU.')
add(2, 3, 'ci', 'Q3(C)(i)', brexit + '\n\n' + eu_i, 14, 'business-6-14', 'eu-membership-advantages', 7, [16], 'Two advantages at 7 marks each (4 + 3).',
    points('Advantage', 2, (4, 3)))
add(2, 3, 'cii', 'Q3(C)(ii)', brexit + '\n\n' + eu_i + '\n' + L(2, 7, '(ii) Outline one disadvantage for Ireland of membership of the EU.'), 6, 'business-6-14',
    'eu-membership-disadvantage', 7, [16], 'One disadvantage: 6 marks (3 + 3).', [comps('Disadvantage', (3, 3))],
    ['Scheme examples: ' + S(16, 'No control over interest rates- Interest rates are set by the ECB.')])
global_i = L(2, 7, '(D) (i) Explain the term Global Business.')
add(2, 3, 'di', 'Q3(D)(i)', brexit + '\n\n' + global_i, 10, 'business-6-15', 'global-business-explained', 7, [17], 'Explanation: 10 marks (4 + 4 + 2).',
    [comps('Global business', (4, 4, 2))], ['Scheme: ' + S(17, 'A global business treats the world as one market.')])
cum(2, 3, 'dii', 'Q3(D)(ii)', brexit + '\n\n' + global_i + '\n' + L(2, 7, '(ii) Name two Global Businesses.'), (5, 5), 'business-6-15', 'global-businesses-named',
    7, [17], 'Scheme examples (page 17): ' + S(17, 'Coca Cola, Apple, Nike, Toyota, Microsoft, Intel, HP, Google, Nokia.'), noun='businesses')
add(2, 3, 'e', 'Q3(E)', brexit + '\n\n' + L(2, 7, '(E) Outline two challenges for Irish businesses operating in international markets.'), 10, 'business-6-13',
    'international-market-challenges', 7, [17], 'Two challenges at 5 marks each (3 + 2).', points('Challenge', 2, (3, 2)))

paul = L(2, 8, 'Sport Trips Ireland Ltd') + '\n' + L(2, 8, 'Paul McCarthy was a supporter of the Irish Soccer and Rugby teams. He identified an opportunity in the market to provide a service organising the travel, accommodation and match tickets for supporters travelling to sport matches abroad. He resigned from his job and set up his own business called Sport Trips Ireland Ltd. He hired a small team of staff and delegated responsibility to each team member. The demand was high for trips to the Rugby World Cup and the European Soccer Championships. Paul’s plan is to be the market leader for sports travel in Ireland by 2025.')
add(2, 4, 'a', 'Q4(A)', paul + '\n\n' + L(2, 8, '(A) Outline three entrepreneurial characteristics/skills displayed by Paul.') + '\n' + L(2, 8, '(Refer to the text in your answer.)'), 15,
    'business-1-5', 'paul-entrepreneurial-characteristics', 8, [18], 'Three at 5 marks each (3 + 2).', points('Characteristic', 3, (3, 2)),
    ['The scheme requires it: ' + S(18, 'Must have a reference to Paul') + '. Example: ' + S(18, 'Risk taker – Paul has taken a personal and financial risk.')])
add(2, 4, 'b', 'Q4(B)', paul + '\n\n' + L(2, 8, '(B) Name and explain one type of plan developed by management in a business.'), 10, 'business-2-13', 'plan-named-and-explained',
    8, [18], 'One plan: 10 marks (5 + 5).', [comps('Plan', (5, 5), ['Named', 'Explained'])],
    ['Scheme examples: ' + S(18, 'Contingency plan – plan for emergencies or unforeseen events.')])
deleg_i = L(2, 8, '(C) (i) Explain the term delegation.')
add(2, 4, 'ci', 'Q4(C)(i)', paul + '\n\n' + deleg_i, 7, 'business-2-11', 'delegation-explained', 8, [18], 'Explanation: 7 marks (4 + 3).', [comps('Delegation', (4, 3))],
    ['Scheme: ' + S(18, 'Delegation involves the assignment of authority to another person, generally from a manager to a subordinate, to undertake a specific work task or project.')])
add(2, 4, 'cii', 'Q4(C)(ii)', paul + '\n\n' + deleg_i + '\n' + L(2, 8, '(ii) Outline two advantages of delegation.'), 8, 'business-2-11', 'delegation-advantages',
    8, [18], 'Two advantages: 5 (3 + 2) and 3 (2 + 1).', unequal('Advantage', [(3, 2), (2, 1)], None), ['The 5-mark allowance is not tied to a particular advantage.'])
agm = L(2, 8, 'Sport Trips Ireland Ltd intends to hold an Annual General Meeting (AGM) in the G Hotel, Co. Galway. The meeting will begin at 2pm on the 30th September 2017. The company secretary Emma Butler is responsible for preparing the notice, the agenda and the minutes of this meeting.')
add(2, 4, 'd', 'Q4(D)', agm + '\n\n' + L(2, 8, '(D) Explain the following terms:', '(i) the agenda of a meeting', '(ii) the minutes of a meeting.'), 15, 'business-2-12',
    'agenda-and-minutes-explained', 8, [19], 'Two explanations: 8 (4 + 4) and 7 (4 + 3).', unequal('Explanation', [(4, 4), (4, 3)], None),
    ['The 8-mark allowance is not tied to either term.',
     'Scheme: ' + S(19, 'An agenda is a list of all the topics to be discussed at the meeting.') + ' ' + S(19, 'This is an account of a meeting written by the secretary.')])
flat(add(2, 4, 'e', 'Q4(E)', agm + '\n\n' + L(2, 8, '(E) Draft the Notice and Agenda for the AGM of Sport Trips Ireland Ltd.', 'The Agenda must contain at least five items.'), 20,
         'business-2-12', 'agm-notice-and-agenda', 8, [19], 'Notice 8 (4 @ 2), agenda 10 (5 @ 2: the three compulsory items and two others) and signature 2 (1 + 1).',
         seq(comps('Notice', (2, 2, 2, 2), ['Notice entry 1', 'Notice entry 2', 'Notice entry 3', 'Notice entry 4']),
             comps('Agenda', (2, 2, 2, 2, 2), ['Chairperson’s Report (compulsory)', 'Auditor’s Report (compulsory)', 'AOB (compulsory)', 'Another item', 'Another item']),
             comps('Signature', (1, 1), ['Signed (Emma Butler)', 'Title (Company Secretary)'])),
         ['Scheme (page 19): ' + S(19, 'The AGM of Sport Trips Ireland Ltd will take place in the G Hotel, Co. Galway on Saturday 30th September 2017 at 2.00 p.m.')
          + ' Agenda: ' + S(19, '1. Minutes of AGM 2016 2. Matters arising from minutes 3. Chairperson’s Report 4. Auditor’s Report 5. Declaration of Dividend 6. Appointment of Auditors 7. Election of Directors 8. AOB') + '.',
          'The scheme marks the agenda ' + S(19, '[Three bolded compulsory, + two others]') + '; the bold items are Chairperson’s Report, Auditor’s Report and AOB.']))

nuevo = L(2, 9, 'Restaurant Nuevo Ltd') + '\n' + L(2, 9, 'Restaurant Nuevo Ltd is a very successful restaurant located in Co. Wicklow employing both full-time and part-time staff. Based on their Trading, Profit and Loss Account and Balance Sheet for the year ending 2016, the owners have decided to expand the business. There is cash available in the company’s current account. However, the business will require a medium term source of finance for new kitchen equipment. The restaurant owners have completed a cashflow forecast.')
L(2, 9, '2017 January € February € March € Total €')
cash = '\n'.join([L(2, 9, 'Cashflow forecast of Restaurant Nuevo Ltd for the first 3 months of 2017'), 'Columns: January €, February €, March €, Total €',
                  L(2, 9, 'Total Receipts (A) 23,000 30,000 24,000 77,000'), L(2, 9, 'Total Payments (B) 31,000 25,000 22,000 78,000'),
                  L(2, 9, 'Net Cash (A-B) -8,000 5,000 2,000 -1,000'), L(2, 9, 'Opening Cash 7,000 -1,000 4,000 7,000'), L(2, 9, 'Closing Cash -1,000 4,000 6,000 6,000')])
item_i = L(2, 9, '(A) Name one item which Restaurant Nuevo Ltd might include under each of the following:', '(i) Receipts section')
add(2, 5, 'ai', 'Q5(A)(i)', nuevo + '\n\n' + cash + '\n\n' + item_i, 5, 'business-3-16', 'cashflow-receipts-item', 9, [20], 'One item: 5 marks.',
    [single('Receipts item', 5, 'Item named')], ['Scheme examples: ' + S(20, '(i) Receipts section: Cash Sales, Grant.')])
add(2, 5, 'aii', 'Q5(A)(ii)', nuevo + '\n\n' + cash + '\n\n' + item_i + '\n' + L(2, 9, '(ii) Payments section.'), 5, 'business-3-16', 'cashflow-payments-item', 9, [20],
    'One item: 5 marks.', [single('Payments item', 5, 'Item named')], ['Scheme examples: ' + S(20, '(ii) Payments section: Purchases of stock or equipment, Wages, Insurance.')])
pos_i = L(2, 9, '(B) (i) Does Restaurant Nuevo Ltd have a better cashflow position in January or March?')
add(2, 5, 'bi', 'Q5(B)(i)', nuevo + '\n\n' + cash + '\n\n' + pos_i, 8, 'business-3-16', 'better-cashflow-month', 9, [20], 'State the month for 8 marks.',
    [single('Better position', 8, 'Month stated')], ['Answer: ' + S(20, 'January or March? March').split('? ')[1] + '.'])
add(2, 5, 'bii', 'Q5(B)(ii)', nuevo + '\n\n' + cash + '\n\n' + pos_i + '\n' + L(2, 9, '(ii) Outline two possible reasons for your answer.'), 12, 'business-3-16',
    'better-cashflow-reasons', 9, [20], 'Two reasons at 6 marks each.', points('Reason', 2, (6,)),
    ['Scheme: ' + S(20, 'Total Receipts higher in March than in January, probably due to a planned increase in Sales.') + ' '
     + S(20, 'Total Payments much lower in March than in January, probably due to a planned reduction in costs in order to save for expansion.')])
src_i = L(2, 9, '(C) (i) Name a suitable medium term source of finance Restaurant Nuevo Ltd might use for the new kitchen equipment.')
add(2, 5, 'ci', 'Q5(C)(i)', nuevo + '\n\n' + src_i, 8, 'business-3-16', 'medium-term-source-named', 9, [20], 'Name the source for 8 marks.',
    [single('Source of finance', 8, 'Source named')], ['Scheme sources (page 20): ' + bullets(S(20, '• Medium term loans • Hire purchase • Leasing')) + '.'])
add(2, 5, 'cii', 'Q5(C)(ii)', nuevo + '\n\n' + src_i + '\n' + L(2, 9, '(ii) Outline two benefits of the source of finance you have chosen.'), 12, 'business-3-16',
    'chosen-source-benefits', 9, [20], 'Two benefits: 8 and 4.', unequal('Benefit', [(8,), (4,)], None),
    ['The 8-mark allowance is not tied to a particular benefit. Scheme example (leasing): ' + S(20, '• Immediate use of the asset • no capital costs • offers the option to easily upgrade the asset in the future.').replace('• ', '').replace(' no capital', '; no capital').replace(' offers', '; offers')])
add(2, 5, 'd', 'Q5(D)', nuevo + '\n\n' + L(2, 9, '(D) Explain the term current account.'), 10, 'business-3-16', 'current-account-explained', 9, [21],
    'Explanation: 10 marks (4 + 3 + 3).', [comps('Current account', (4, 3, 3))],
    ['Scheme: ' + S(21, 'A current account is a service offered by commercial banks and building societies. Money can be withdrawn without notice.')])
add(2, 5, 'e', 'Q5(E)', nuevo + '\n\n' + L(2, 9, '(E) Outline three types of insurance Restaurant Nuevo Ltd should have.'), 15, 'business-3-17', 'restaurant-insurance-types',
    9, [21], 'Three types: 6 (3 + 3), 6 (3 + 3) and 3 (2 + 1).', unequal('Type of insurance', [(3, 3), (3, 3), (2, 1)], None),
    ['The 6/6/3 sequence prices the three types, not particular types.'])

maire = (L(2, 10, 'Maire de Paor had an idea for an app which would help students set study goals, track their study progress and enable reminders for weekly study targets etc. She contacted the Local Enterprise Office (LEO) who provided advice on Prototype Development, Feasibility Study, Test Marketing and the Launch.')
         + '\n(Prototype Development, Feasibility Study, Test Marketing and Launch are underlined.)')
add(2, 6, 'a', 'Q6(A)', maire + '\n\n' + L(2, 10, '(A) Explain any three of the four underlined terms in the text above.'), 20, 'business-4-14', 'underlined-development-stages-choice',
    10, [22], 'Choose three of the four underlined terms and explain each: 12 (8 + 4), 4 (3 + 1) and 4 (3 + 1).',
    seq(comps('First term you chose', (8, 4)), comps('Second term you chose', (3, 1)), comps('Third term you chose', (3, 1))),
    ['You choose which three of the four underlined terms to answer. The scheme marks every choice alike, so this is one card whichever terms you choose.',
     'The 12-mark allowance is not tied to a particular term.',
     'Prototype Development (scheme PDF page 22): “' + S(22, 'This stage involves developing a sample or first model of a product (or app).') + '”',
     'Feasibility Study (scheme PDF page 22): “' + S(22, 'A Feasibility Study is carried out to assess the financial potential of a product or service.') + '”',
     'Test Marketing (scheme PDF page 22): “' + S(22, 'Test marketing involves assessing customer reaction.') + '”',
     'Launch (scheme PDF page 22): “' + S(22, 'The product is released to the market.') + '”'])
add(2, 6, 'b', 'Q6(B)', maire + '\n\n' + L(2, 10, '(B) Outline three ways entrepreneurs come up with ideas for new products/services.'), 15, 'business-4-14', 'idea-sources-three-ways',
    10, [23], 'Three ways at 5 marks each (2 + 3).', points('Way', 3, (2, 3)))
maire2 = L(2, 10, 'Maire’s business proved very successful. The app is the market leader amongst second-level students in Ireland and Maire needs to hire staff to cope with the increasing demand. Maire needs to prepare a Job Description for the new position of Sales Manager. Maire will offer an attractive financial rewards scheme to motivate her staff.')
jd_i = '(C) ' + L(2, 10, '(i) Explain the term Job Description.')
add(2, 6, 'ci', 'Q6(C)(i)', maire2 + '\n\n' + jd_i, 12, 'business-3-20', 'job-description-explained', 10, [24], 'Explanation: 12 marks (8 + 4).', [comps('Job description', (8, 4))],
    ['Scheme: ' + S(24, 'This document shows details of the position/vacancy to be filled, including the job title, work details, duties and responsibilities of the job, conditions of employment and place of work.')])
add(2, 6, 'cii', 'Q6(C)(ii)', maire2 + '\n\n' + jd_i + '\n' + L(2, 10, '(ii) Draft the Job Description Maire prepared for the new position of Sales Manager.'), 8, 'business-3-20',
    'job-description-drafted', 10, [24], 'Draft: 8 marks (4 + 4), at least two points.', [comps('Job description drafted', (4, 4))],
    ['The scheme asks for ' + S(24, '(at least 2 points)') + ' and prints a sample: job title Sales Manager; duties ' + S(24, 'Marketing and advertising our app throughout Ireland.')
     + ' contracted hours, salary, place of work and who the post is responsible to.'])
add(2, 6, 'd', 'Q6(D)', maire2 + '\n\n' + L(2, 10, '(D) In relation to the recruitment and selection process, explain the term shortlisting.'), 10, 'business-3-20', 'shortlisting-explained',
    10, [24], 'Explanation: 10 marks (6 + 4).', [comps('Shortlisting', (6, 4))],
    ['Scheme: ' + S(24, 'Shortlisting involves creating a reduced list of candidates for interview from the number of people who applied for the job.')])
add(2, 6, 'e', 'Q6(E)', maire2 + '\n\n' + L(2, 10, '(E) Explain two financial rewards that businesses offer to motivate staff.'), 10, 'business-3-20', 'financial-rewards-motivation',
    10, [24], 'Two rewards at 5 marks each (3 + 2).', points('Reward', 2, (3, 2)), extra=['business-2-11'])

aran = L(2, 11, 'Amazing Aran') + '\n' + L(2, 11, 'Maggie started knitting and selling Aran sweaters locally while still in secondary school. She studied textile technology in University in England. Maggie dreamed of establishing a leading Irish fashion house and went on to set up her own brand “Amazing Aran”. Amazing Aran provides “cosy, cool, wool-knitted products”. In the past year, various celebrities have been photographed wearing Amazing Aran wool sweaters, which has led to a major increase in online sales. Social Media has also been key to its marketing success with the hashtag “#AmazingAran” trending online when celebrities have been spotted in the brand’s sweaters. Maggie’s product is in the growth stage of its product life cycle.')
add(2, 7, 'a', 'Q7(A)', aran + '\n\n' + L(2, 11, '(A) Explain the term branding and outline one advantage of branding a product.'), 10, 'business-4-17', 'branding-and-advantage',
    11, [25], 'Explanation 5 (3 + 2) and one advantage 5.', seq(comps('Branding', (3, 2)), comps('Advantage', (5,), ['Advantage outlined'])),
    ['Scheme: ' + S(25, 'Branding involves creating an identity for a product/business that clearly distinguishes it from its competitors.')])
plc_i = L(2, 11, '(B) (i) Explain the term Product life cycle.')
add(2, 7, 'bi', 'Q7(B)(i)', aran + '\n\n' + plc_i, 5, 'business-4-17', 'product-life-cycle-explained', 11, [25], 'Explanation: 5 marks (3 + 2).',
    [comps('Product life cycle', (3, 2))], ['Scheme: ' + S(25, 'The Product life cycle refers to the life span of a product.')])
flat(add(2, 7, 'bii', 'Q7(B)(ii)', aran + '\n\n' + plc_i + '\n' + L(2, 11, '(ii) Draft and label the Product Life Cycle diagram.'), 15, 'business-4-17',
         'product-life-cycle-diagram', 11, [25], 'Title, sales axis and time axis 1 each; the curved line 2; five stage labels in order at 2 each.',
         [fixed('Product life cycle diagram', [('Title', 1), ('Sales axis', 1), ('Time axis', 1), ('Curved line', 2), ('Introduction/Launch', 2), ('Growth', 2),
                                              ('Maturity', 2), ('Saturation', 2), ('Decline', 2)])],
         ['Scheme (page 25): ' + S(25, 'Title: 1m Sales: 1m Time: 1m Curved Line: 2m Labels: (in order) 5 x 2m') + '; the allocation summary prints “'
          + S(7, '15 marks [(6 @ 2m) + (3 @ 1m)]') + '”.']))
online = L(2, 11, '(C) Outline one advantage of online selling for')
add(2, 7, 'ci', 'Q7(C)(i)', aran + '\n\n' + L(2, 11, '(C) Outline one advantage of online selling for (i) the Business'), 10, 'business-4-17', 'online-selling-advantage-business',
    11, [26], 'One advantage: 10 marks (5 + 5).', [comps('Advantage for the business', (5, 5))],
    ['Scheme examples: ' + S(26, 'Global Market – wider potential market') + '; ' + S(26, 'Reduced Costs – rent, insurance, operational costs') + '.'], extra=['business-2-12'])
add(2, 7, 'cii', 'Q7(C)(ii)', aran + '\n\n' + online + ' ' + L(2, 11, '(ii) the Consumer.'), 10, 'business-4-17', 'online-selling-advantage-consumer',
    11, [26], 'One advantage: 10 marks (5 + 5).', [comps('Advantage for the consumer', (5, 5))],
    ['Scheme examples: ' + S(26, 'Convenience – does not have to leave home') + '; ' + S(26, 'Wider choice of goods/services – many firms sell online') + '.'], extra=['business-2-12'])
add(2, 7, 'd', 'Q7(D)', aran + '\n\n' + L(2, 11, '(D) Outline the two types of market research and give one example of each type.'), 15, 'business-4-16', 'desk-and-field-research-2017',
    11, [26], 'Each type named 3, explained 3 and 2, and an example 2 each: 8 and 7.',
    unequal('Type of research', [(3, 3, 2), (3, 2, 2)], ['Type named', 'Explained', 'Example']),
    ['The 8-mark allowance is not tied to desk or field research.',
     'Scheme: ' + S(26, 'Desk research involves accessing or using information that has already been gathered.') + ' '
     + S(26, 'Field research involves going into the marketplace to gather first-hand or new business information.')])
add(2, 7, 'e', 'Q7(E)', aran + '\n\n' + L(2, 11, '(E) Apart from online selling, outline two ways in which developments in ICT (Information and Communications Technology) impact on a business.'), 10,
    'business-2-12', 'ict-impact-ways', 11, [26], 'Two ways: 6 (4 + 2) and 4 (2 + 2).', unequal('Way', [(4, 2), (2, 2)], None),
    ['The 6-mark allowance is not tied to a particular way.'])

coffee = L(2, 12, 'Billy and Bobby’s Boutique Coffee') + '\n' + L(2, 12, 'Billy and Bobby recognised the popularity of coffee in Ireland. They decided to develop an Irish brand that roasts and distributes speciality coffee for a niche market. They set up Billy and Bobby’s Coffee as a partnership. Their premium coffee beans are supplied by farmers throughout the world and then roasted/produced in batches at their “roastery” in Ireland. Costs are high but the partners believe consumers are willing to pay a premium price for superior quality coffee. Billy and Bobby’s Boutique Coffee is currently sold in over 100 cafes nationwide, at markets, festivals and online direct to their consumers.')
owners_i = L(2, 12, '(A) (i) Identify how many owners a partnership can have.')
add(2, 8, 'ai', 'Q8(A)(i)', coffee + '\n\n' + owners_i, 3, 'business-5-14', 'partnership-owners', 12, [27], 'Identify the number for 3 marks.',
    [single('Number of owners', 3, 'Number identified')], ['Answer: ' + S(27, 'Minimum of 2 to a maximum of 20.')])
add(2, 8, 'aii', 'Q8(A)(ii)', coffee + '\n\n' + owners_i + '\n' + L(2, 12, '(ii) Explain the term unlimited liability.'), 12, 'business-5-14', 'unlimited-liability-explained',
    12, [27], 'Explanation: 12 marks (6 + 6).', [comps('Unlimited liability', (6, 6))],
    ['Scheme: ' + S(27, 'They can also be personally sued for the debts of the business.') + ' ' + S(27, 'The owners’ private property might have to be sold to pay for the debts if the business fails.')])
batch = L(2, 12, '(B) Billy and Bobby’s Boutique Coffee use a batch production process.')
methods_i = L(2, 12, '(i) List two other methods of production.')
cum(2, 8, 'bi', 'Q8(B)(i)', coffee + '\n\n' + batch + '\n' + methods_i, (5, 5), 'business-4-15', 'other-production-methods-listed', 12, [27],
    'Answer key (scheme page 27): ' + bullets(S(27, '• Job Production • Mass Production'), ' and ') + '.', noun='methods')
add(2, 8, 'bii', 'Q8(B)(ii)', coffee + '\n\n' + batch + '\n' + methods_i + '\n' + L(2, 12, '(ii) Outline two features of any one of these methods of production.'), 10,
    'business-4-15', 'production-method-features', 12, [27], 'Two features of one method at 5 marks each.', points('Feature', 2, (5,)),
    ['You outline features of one of the methods you listed in (i); the scheme marks job and mass production alike.',
     'Job Production (scheme PDF page 27): “' + S(27, 'Firm produces one-off goods to order') + '”',
     'Mass Production (scheme PDF page 27): “' + S(27, 'Firms manufacture large numbers of an identical/standardised product in a continuously moving and highly automated process.') + '”'])
add(2, 8, 'c', 'Q8(C)', coffee + '\n\n' + L(2, 12, '(C) Explain two benefits of setting up your own business.'), 15, 'business-1-5', 'own-business-benefits',
    12, [27], EIGHT, eight_seven('Benefit'), [UNTIED], extra=['business-5-14'])
chan = add(2, 8, 'd', 'Q8(D)', coffee + '\n\n' + L(2, 12, '(D) Illustrate, using a diagram, one channel of distribution used by Billy and Bobby’s Boutique Coffee.'), 10,
           'business-4-17', 'coffee-channel-of-distribution', 12, [28],
           'Draw one channel: 10 marks, either 5 @ 2 (manufacturer, arrow, retailer, arrow, consumer) or 4 + 2 + 4 (manufacturer, arrow, consumer).',
           [comps('Channel diagram', (10,), ['Diagram marked on the scheme’s template'])],
           ['The scheme (page 28) prints two channels: ' + S(28, 'CAFES: MANUFACTURER RETAILER CONSUMER ONLINE: MANUFACTURER CONSUMER')
            + '. Through cafes: each stage and each arrow 2. Online: manufacturer 4, the arrow 2, consumer 4.',
            'The allocation summary prints “' + S(7, 'Illustration: 10 marks (5 @ 2m) or (4m + 2m +4m)') + '”. Whichever channel you draw, record the marks in steps of 2.'])
evens(chan)
add(2, 8, 'e', 'Q8(E)', coffee + '\n\n' + L(2, 12, '(E) Describe two sales promotions that Billy and Bobby’s Boutique Coffee could offer consumers to increase sales.'), 15, 'business-4-17',
    'coffee-sales-promotions', 12, [28], EIGHT, eight_seven('Sales promotion'), [UNTIED])

# ---------------------------------------------------------------- checks and write-out
qn = lambda c: c['questionRef'].split(' Q')[1].split('(')[0]
for section, count, total in [('1', 15, 10), ('2', 8, 75)]:
    for q in range(1, count + 1):
        got = sum(c['totalMarks'] for c in P.created if c['section'] == section and qn(c) == str(q))
        assert got == total, (section, q, got)
assert not [i for i in ORIGINAL if i.startswith('bus-2017-ol-')]
assert not P.pools

SELECTION = {
    1: 'No finite printed answer menu occurs in Section 1 (answer ten of fifteen at 10 marks). The word bank in Q7, the ticks in Q10 and Q11, TRUE/FALSE in Q14 and the matching rows in Q15 are required answer formats. Q3 (A) and (B) are both required. Support-note lists are open examples.',
    2: 'Two printed choices, each one card: Q1(A) any two of the three Consumer Protection Act provisions and Q6(A) any three of the four underlined terms (the scheme marks every choice alike). Q8(B)(ii) “any one of these methods” is the candidate’s own list from (i), and Q8(D) “one channel” is an open choice the scheme marks on two templates (5 @ 2 or 4 + 2 + 4). Sub-parts with their own published marks are separate cards. Support-note lists are open examples.',
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
    if m == 'any two' and own(w, m, 'Explain by means of examples any two of the following provisions'):
        return 'finite-choice', 'Section 2 Q1(A) asks for any two of the three printed Consumer Protection Act provisions. The scheme marks every choice alike, so one card carries all three with the scheme wording for each.', 'bus-2017-ol-s2-q1a'
    if m == 'any three' and own(w, m, 'Explain any three of the four underlined terms'):
        return 'finite-choice', 'Section 2 Q6(A) asks for any three of the four underlined terms. The scheme marks every choice alike, so one card carries all four with the scheme wording for each.', 'bus-2017-ol-s2-q6a'
    if m == 'any one' and own(w, m, 'Outline two features of any one of these methods of production'):
        return 'open-response', 'Section 2 Q8(B)(ii) asks for features of one of the methods the candidate listed in (i); no list is printed and the scheme marks job and mass production alike, so it is one card.', None
    if m == 'Choose' and own(w, m, 'Choose the appropriate words'):
        return 'required-headings', 'Section 1 Q7 is a word-bank completion: both blanks are required and the printed words are the answer options, not optional tasks.', None
    if m == 'or' and own(w, m, 'TRUE or FALSE'):
        return 'required-headings', 'TRUE/FALSE are answer labels for each of the five required statements in Section 1 Q14, not optional tasks.', None
    if m == 'or' and own(w, m, 'January or March'):
        return 'required-headings', 'Section 2 Q5(B)(i) asks which month has the better cashflow position; it is one required determination, not a choice of task.', None
    if m == 'or' and own(w, m, 'Prohibits false or misleading advertising'):
        return 'case-context', '“false or misleading advertising” is the name of one printed provision in Section 2 Q1(A), not a choice of task.', None
    if m == 'or' and own(w, m, 'false or misleading claims'):
        return 'case-context', '“false or misleading claims” is wording inside the Section 2 Q1 extract, not a choice of task.', None
    assert (fileid, page) in {('LC033GLP000EV', 1), ('LC033GLP000EV', 6)} and m in ('either', 'or'), (fileid, page, m, w)
    return 'exam-navigation', 'The cover and Section 2 rubrics set how many whole questions a candidate answers (one from Part 1, two from Part 2 and one other from either part). Every numbered question remains in the practice corpus as separate cards.', None


n = P.write([(1, range(1, 16)), (2, range(1, 9))], SELECTION, classify,
            'Every part of {year} Ordinary Section {section} Question {q} was visually checked against its SEC paper, allocation summary and expected responses. The single-booklet identity keeps the short (n) and long (S2Q) question numbering apart.')
print(f'Reviewed {len(P.created)} 2017 Ordinary tasks; classified {n} raw selection matches.')
