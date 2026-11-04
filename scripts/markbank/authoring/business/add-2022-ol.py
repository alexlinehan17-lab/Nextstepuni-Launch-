"""Review the 2022 Ordinary English paper (Section 1 and Section 2).

2022 is the adjusted paper: answer five of fifteen short questions at 15 marks
and three of nine long questions at 75. Sixty-five legacy IDs keep their ID
and total with correction records; two legacy cards become the first printed
route of their finite pools; Section 2 Q9(A), Q9(C), Q9(D)(i) and Q9(D)(ii)
are new.
"""
from bus_lib import (Paper, ORIGINAL, comps, points, seq, unequal, single, ten_five, response,
                     fixed, legacy_route, opt_resp, permit)

T = {(1, q): 4 for q in range(1, 16)}
T.update({(2, 1): 5, (2, 2): 5, (2, 3): 5, (2, 4): 6, (2, 5): 6, (2, 6): 6, (2, 7): 7, (2, 8): 7, (2, 9): 7})
P = Paper(2022, 'ordinary', {1: 'LC033GLP032EV', 2: 'LC033GLP033EV'}, 'LC033GLP000EV', T)
L, S, add, cum = P.lift, P.scheme, P.add, P.cumulative
TWO = 'Two points are required: 10 (7 + 3) and 5 (4 + 1).'
UNTIED = 'The 10-mark allowance is not tied to a particular point.'
EIGHT = 'Two points are required: 8 (4 + 4) and 7 (4 + 3).'
UNTIED8 = 'The 8-mark allowance is not tied to a particular point.'


def eight_seven(label):
    return unequal(label, [(4, 4), (4, 3)], None)


# ---------------------------------------------------------------- Section 1 (15 marks each)
add(1, 1, '', 'Q1', L(1, 3, 'What do the following letters stand for? Write each answer in the space provided.', 'PLC', 'CEO', 'ICT'), 15,
    'business-2-12', 'abbreviations-plc-ceo-ict', 3, [8], 'Each term earns 5 marks (2 + 2 + 1).',
    [comps('PLC (first term)', (5,), ['Term written in full'], 1), comps('CEO (second term)', (5,), ['Term written in full'], 2),
     comps('ICT (third term)', (5,), ['Term written in full'], 3)],
    ['Answer key: PLC ' + S(8, 'Public Limited Company') + '; CEO ' + S(8, 'Chief Executive Officer') + '; ICT '
     + S(8, 'Information and Communications Technology') + '.'], extra=['business-5-14'])
add(1, 2, '', 'Q2', L(1, 3, 'Identify the category of industry most appropriate to each of the images shown below.')
    + '\n(i) Workers on a building site.\n(ii) A hairdresser styling a client’s hair.\n(iii) A tractor harvesting a crop.', 15, 'business-5-13',
    'categories-of-industry-images', 3, [8], 'Each image earns 5 marks.',
    seq(single('Image (i)', 5, 'Category identified'), single('Image (ii)', 5, 'Category identified'), single('Image (iii)', 5, 'Category identified')),
    ['Answer key: ' + S(8, '(i) Secondary (ii) Tertiary/Services (iii) Primary') + '.'])
cum(1, 3, '', 'Q3', L(1, 3, 'Identify which of McGregor’s Theory X or Theory Y corresponds with the following statements:',
                      '1. All employees are self-motivated and enjoy work.', '2. Employees are only motivated by money.', '3. Employees must be supervised closely.',
                      '4. Employees can work on their own initiative.'),
    (4, 4, 4, 3), 'business-2-11', 'mcgregor-theory-x-y', 3, [8], 'Answer key: 1. Theory Y; 2. Theory X; 3. Theory X; 4. Theory Y (scheme page 8).')
cum(1, 4, '', 'Q4', L(1, 4, 'Indicate by placing a tick (✓) in the correct box, the factor of production to which each statement relates.')
    + '\nLand / Labour / Capital / Enterprise (each statement opens with the Cadbury logo)\n'
    + L(1, 4, 'uses specialist equipment and machinery to produce their products.', 'uses cocoa beans in the production of their chocolate bars.',
        'employs thousands of people in their plants in Ireland and the UK.', 'was founded by the entrepreneur John Cadbury.'),
    (4, 4, 4, 3), 'business-1-5', 'factors-of-production-ticks', 4, [8],
    'Answer key (ticks on scheme page 8): equipment and machinery Capital; cocoa beans Land; employs thousands Labour; founded by John Cadbury Enterprise.',
    extra=['business-5-13'])
func = add(1, 5, '', 'Q5', L(1, 4, 'Complete the functional departments of a manufacturing company with four departments.')
           + '\nBoard of Directors; a blank box below it; four department boxes, one printed as Human Resources and three blank.',
           15, 'business-2-13', 'functional-structure-manufacturing', 4, [9], 'The box below the Board 4; the three departments 4 + 4 + 3, Production compulsory.',
           seq(fixed('Below the Board', [('CEO/MD', 4)]), comps('Three departments', (11,), ['Departments named'])),
           ['Answer key (chart on scheme page 9): ' + S(9, 'CEO/MD') + '; departments Finance, Marketing and Production (Human Resources is printed); '
            + S(9, 'Production Compulsory') + '.',
            'For 0, 1, 2 or 3 acceptable departments record 0, 4, 8 or 11 marks; a manufacturing company must include Production.'])
permit(func, 1, [0, 4, 8, 11])
for v in ['Board of Directors', 'Human Resources']:
    L(1, 4, v)
cum(1, 6, '', 'Q6', L(1, 5, 'Name two European Union (EU) institutions.'), (8, 7), 'business-6-14', 'eu-institutions-named', 5, [9],
    'Scheme examples: ' + S(9, 'European Parliament') + ', European Commission, European Council, the Council of the EU, Court of Auditors, Court of Justice, European Central Bank.',
    noun='institutions')
cum(1, 7, '', 'Q7', L(1, 5, 'Circle the correct option in each of the following statements.',
                      '(i) A state-owned enterprise is owned and controlled by private entrepreneurs / the government.',
                      '(ii) A partnership is owned by a minimum of one / two partners.',
                      '(iii) In a cooperative, voting rights for members are equal / dependent on share ownership.',
                      '(iv) Shareholders in a Private Limited Company have limited / unlimited liability.'),
    (4, 4, 4, 3), 'business-5-14', 'ownership-options', 5, [9], 'Answer key (circled on scheme page 9): (i) the government; (ii) two; (iii) equal; (iv) limited.')
cum(1, 8, '', 'Q8', L(1, 5, 'Choose the appropriate terms to complete the sentence below. (Two terms do not apply.)', 'Tactical Contingency Strategic Operational')
    + '\nA ______ plan is a plan for a business to be achieved over a 1 to 2 year period, while a ______ plan is used in the event of an emergency/unforeseen situation.',
    (8, 7), 'business-2-13', 'plans-word-bank', 5, [9], 'Answer key: A ' + S(9, 'Tactical') + ' plan ... a ' + S(9, 'Contingency') + ' plan. Strategic and Operational are not used.',
    noun='terms')
for v in ['plan is a plan for a business to be achieved over a 1 to 2 year period, while a', 'plan is used in the event of an emergency/unforeseen situation.']:
    L(1, 5, v)
add(1, 9, '', 'Q9', L(1, 6, 'Explain the difference between a Takeover and a Merger.'), 15, 'business-4-18', 'takeover-versus-merger', 6, [10],
    'Takeover 8 (4 + 4) and merger 7 (4 + 3).', [comps('Takeover', (4, 4), i=1), comps('Merger', (4, 3), i=2)])
add(1, 10, '', 'Q10', L(1, 6, 'The following information is available from the final accounts of Garvin Ltd on 31/12/2021. Calculate the Acid Test Ratio. (Show formula and workings)')
    + '\n' + L(1, 6, 'Current Assets: €160,000', 'Closing Stock: € 40,000', 'Current Liabilities: €100,000'), 15, 'business-3-19', 'acid-test-ratio',
    6, [10], 'Formula 4, calculation 6 (2 + 2 + 2) and answer 5.',
    [response(1, 'Acid test ratio', [('formula', 'Formula: ' + S(10, 'Current Assets – Closing Stock : Current Liabilities'), 4),
                                     ('workings', 'Workings: ' + S(10, '€160,000 – €40,000 : €100,000'), 6), ('answer', 'Answer: ' + S(10, '1.2 : 1'), 5)])])
permit(P.created[-1], 0, [0, 4], 0)
permit(P.created[-1], 0, [0, 2, 4, 6], 1)
permit(P.created[-1], 0, [0, 5], 2)
cum(1, 11, '', 'Q11', L(1, 7, 'Match the explanation with the relevant Barrier to Trade from the list below. One barrier is not explained.', 'Embargo Quota Subsidy Tariff',
                        'An import tax imposed on goods coming in from certain countries.', 'A complete ban on specific goods being imported into a country.',
                        'Money provided by the Government to help firms cover operating costs to keep prices competitive.'),
    (5, 5, 5), 'business-6-13', 'barriers-to-trade-matching', 7, [10], 'Answer key: import tax Tariff; complete ban Embargo; money from the Government Subsidy. Quota is not explained.')
cum(1, 12, '', 'Q12', L(1, 7, 'Write the word TRUE or FALSE after each of the following statements.', 'A loading is a reduction on a basic insurance premium.',
                        'The greater the risk, the higher your insurance premium will be.', 'An actuary calculates insurance premium.',
                        'Indemnity means you cannot make a profit from insurance.'),
    (4, 4, 4, 3), 'business-3-17', 'insurance-true-false', 7, [10], 'Answer key: False; True; True; True (scheme page 10).')
cum(1, 13, '', 'Q13', L(1, 7, 'Identify the three other elements of the marketing mix.') + '\n3. Promotion is printed; 1, 2 and 4 are blank.', (5, 5, 5),
    'business-4-17', 'marketing-mix-elements', 7, [10], 'Answer key (scheme page 10): 1. Product; 2. Price; 4. Place.')
cum(1, 14, '', 'Q14', L(1, 8, 'Identify the method of production used to manufacture the following products:')
    + '\n(i) A sliced pan of bread (Irish Pride).\n(ii) A tin of baked beans (Batchelors).\n(iii) A tiered wedding cake.', (5, 5, 5), 'business-4-15',
    'production-method-products', 8, [11], 'Answer key (scheme page 11): bread ' + S(11, 'BATCH PRODUCTION') + '; beans MASS PRODUCTION; wedding cake JOB PRODUCTION.')
cum(1, 15, '', 'Q15', '\n'.join([L(1, 8, 'In the following table, Column 1 is a list of business terms and Column 2 is a list of explanations.'),
                                 L(1, 8, '1. Inflation', '2. Interest rates', '3. Exchange rates', '4. Unemployment rate', '5. Taxation'),
                                 L(1, 8, 'A The price of one currency expressed in terms of another currency.',
                                   'B The increase in the value of goods and services produced in one year compared to the last.',
                                   'C The main source of revenue for the government.', 'D The increase in the general level of prices over time.',
                                   'E Percentage of the labour force that is not employed.', 'F The cost of borrowing money.'),
                                 L(1, 8, 'Match the two lists by placing the letter of the correct explanation under the number of the relevant business term below. One explanation has no match.')]),
    (3, 3, 3, 3, 3), 'business-5-15', 'economic-terms-matching', 8, [11], 'Answer key: 1 D; 2 F; 3 A; 4 E; 5 C. Explanation B is unused (scheme page 11).')

# ---------------------------------------------------------------- Section 2 (75 marks each)
jamie = L(2, 2, 'Sale No refunds or exchange on sale items') + '\n' + L(2, 2, 'Jamie purchased a sports jersey during a sale which was reduced from €80 to €50. After taking it home Jamie noticed a rip on the arm of the jersey. Jamie took it back to the shop but the manager refused to offer Jamie any kind of redress, as it was purchased during a sale and a sign in the shop clearly stated that there were no refunds or exchange on sale items.')
add(2, 1, 'a', 'Q1(A)', jamie + '\n\n' + L(2, 2, '(A) Name the consumer law that protects Jamie in this situation.'), 10, 'business-0-13', 'consumer-law-named',
    2, [12], 'Name the Act: five words at 2 marks each.', [comps('Consumer law', (10,), ['Act named'])],
    ['Answer: ' + S(12, 'The Sale of Goods and Supply of Services Act 1980') + '. For 0 to 5 correct words, record 0, 2, 4, 6, 8 or 10 marks.'])
permit(P.created[-1], 0, [0, 2, 4, 6, 8, 10])
add(2, 1, 'b', 'Q1(B)', jamie + '\n\n' + L(2, 2, '(B) Outline two provisions of the law you have named above which are relevant to Jamie’s situation.'), 15, 'business-0-13',
    'relevant-provisions', 2, [12], EIGHT, eight_seven('Provision'), [UNTIED8])
add(2, 1, 'c', 'Q1(C)', jamie + '\n\n' + L(2, 2, '(C) Explain two benefits to Jamie of taking his case to the Small Claims Procedure/Small Claims Court.'), 15, 'business-0-13',
    'small-claims-benefits', 2, [12], TWO, ten_five('Benefit'), [UNTIED])
katie = L(2, 2, 'Katie has worked in the accounts department of a large company for 6 years. She recently applied for the position of assistant manager. She was disappointed that the position was given to a male colleague who has only been employed in the company for two years and is less qualified than Katie. Katie feels she has been discriminated against based on her gender. She is considering contacting the Workplace Relations Commission.')
add(2, 1, 'd', 'Q1(D)', katie + '\n\n' + L(2, 2, '(D) Outline three grounds (other than gender) on which discrimination is outlawed under the Employment Equality Act 1998-2015.'), 15,
    'business-0-14', 'discrimination-grounds', 2, [13], 'Three grounds at 5 marks each (4 + 1).', points('Ground', 3, (4, 1)))
add(2, 1, 'ei', 'Q1(E)(i)', katie + '\n\n' + L(2, 2, '(i) Explain three reasons other than discrimination for an industrial relations dispute in the workplace.'), 15,
    'business-0-14', 'dispute-reasons', 2, [14], 'Three reasons: 6 (4 + 2), 6 (4 + 2) and 3 (2 + 1).', unequal('Reason', [(4, 2), (4, 2), (2, 1)], None),
    ['The 6/6/3 sequence prices the three reasons, not particular causes.'])
add(2, 1, 'eii', 'Q1(E)(ii)', katie + '\n\n' + L(2, 2, '(ii) Outline one type of industrial action available to employees involved in an industrial dispute with an employer.'), 5,
    'business-0-14', 'industrial-action-type', 2, [14], 'One type: 5 marks (4 + 1).', [comps('Type of industrial action', (4, 1))])

ctax = L(2, 3, 'CABINET APPROVES CHANGE TO THE IRISH CORPORATION TAX RATE')
add(2, 2, 'ai', 'Q2(A)(i)', ctax + '\n\n' + L(2, 3, '(i) Explain the term Corporation Tax.'), 8, 'business-3-18', 'corporation-tax-explained',
    3, [15], 'Explanation: 8 marks (4 + 4).', [comps('Corporation Tax', (4, 4))])
add(2, 2, 'aii', 'Q2(A)(ii)', ctax + '\n\n' + L(2, 3, '(ii) Outline one impact an increase in Corporation Tax may have on businesses/companies in Ireland.'), 7, 'business-3-18',
    'corporation-tax-increase-impact', 3, [15], 'One impact: 7 marks (4 + 3).', [comps('Impact', (4, 3))])
add(2, 2, 'b', 'Q2(B)', L(2, 3, '(B) The Government assists business in Ireland in many ways. Outline two impacts, other than taxation, the Government has on Irish businesses.'), 15,
    'business-5-15', 'government-impacts-business', 3, [15], EIGHT, eight_seven('Impact'), [UNTIED8])
aldi = L(2, 3, 'Aldi’s corporate responsibility plan is driven by 5 principles: customers, suppliers, environment, employees and community.')
add(2, 2, 'c', 'Q2(C)', aldi + '\n\n' + L(2, 3, '(C) Outline two ways that Aldi can behave ethically towards its employees.'), 15, 'business-5-17',
    'ethical-towards-employees', 3, [16], EIGHT, eight_seven('Way'), [UNTIED8])
add(2, 2, 'd', 'Q2(D)', aldi + '\n\n' + L(2, 3, '(D) Describe two ways that a supermarket can be environmentally responsible.'), 15, 'business-5-17',
    'supermarket-environmental-responsibility', 3, [16], EIGHT, eight_seven('Way'), [UNTIED8])
add(2, 2, 'e', 'Q2(E)', aldi + '\n\n' + L(2, 3, '(E) Explain two benefits to a local community of a new business such as Aldi setting up in the area.'), 15, 'business-5-16',
    'community-benefits-new-business', 3, [16], EIGHT, eight_seven('Benefit'), [UNTIED8])

imports = (L(2, 4, "IRELAND'S IMPORTS FOR 2021") + ' (pie chart): ' + L(2, 4, 'EU 36% UK 23% USA 15% China 7% Other 19%') + ' (www.cso.ie)')
add(2, 3, 'a', 'Q3(A)', imports + '\n\n' + L(2, 4, '(A) Imports can be both visible and invisible. Explain the term visible import and give one example of a visible import for Ireland.'), 10,
    'business-6-13', 'visible-import', 4, [17], 'Explanation 6 (3 + 3) and example 4.', seq(comps('Explanation', (3, 3)), single('Example', 4, 'Visible import example')))
add(2, 3, 'b', 'Q3(B)', imports + '\n\n' + L(2, 4, '(B) Outline two reasons why goods and services are imported into Ireland.'), 15, 'business-6-13',
    'reasons-for-imports', 4, [17], EIGHT, eight_seven('Reason'), [UNTIED8])
accounts = 'International Accounts April 2021: ' + L(2, 4, 'Visible Exports Visible Imports €12,706m €8,053m')
bot = add(2, 3, 'ci', 'Q3(C)(i)', accounts + '\n\n' + L(2, 4, '(i) Using the figures below calculate the Balance of Trade for April 2021. Show your workings.'), 10,
          'business-6-13', 'balance-of-trade-calculation', 4, [17], 'Formula 2, workings 2 + 2 + 2 and answer 1 + 1.',
          [response(1, 'Balance of trade', [('formula', 'Formula: Balance of Trade = Visible Exports – Visible Imports', 2),
                                            ('workings', 'Workings: €12,706m – €8,053m', 6), ('answer', 'Answer: €4,653m', 2)])],
          ['Scheme: ' + S(17, 'Balance of Trade = Visible Exports - Visible Imports') + ' = €12,706m – €8,053m = ' + S(17, '€4,653m') + '.'])
permit(bot, 0, [0, 2], 0)
permit(bot, 0, [0, 2, 4, 6], 1)
add(2, 3, 'cii', 'Q3(C)(ii)', accounts + '\n\n' + L(2, 4, '(ii) State whether it is a surplus or a deficit.'), 5, 'business-6-13', 'trade-surplus-or-deficit',
    4, [17], 'State it for 5 marks.', [single('Surplus or deficit', 5, 'Answer stated')], ['Answer: Surplus.'])
add(2, 3, 'd', 'Q3(D)', L(2, 4, '(D) Describe two challenges for Irish businesses involved in international trade.'), 15, 'business-6-13',
    'international-trade-challenges', 4, [18], EIGHT, eight_seven('Challenge'), [UNTIED8])
add(2, 3, 'e', 'Q3(E)', L(2, 4, '(E) Outline three benefits for Ireland of remaining part of the European Union.'), 20, 'business-6-14', 'eu-membership-benefits',
    4, [18], 'Three benefits: 7 (4 + 3), 7 (4 + 3) and 6 (4 + 2).', unequal('Benefit', [(4, 3), (4, 3), (4, 2)], None),
    ['The 7/7/6 sequence prices the three benefits, not particular benefits.'])

glenisk = L(2, 5, 'A fire at the Glenisk yoghurt manufacturing plant in Tullamore, Co. Offaly has had a huge impact on the business’ stakeholders. The fire destroyed the entire production facility.')
add(2, 4, 'ai', 'Q4(A)(i)', glenisk + '\n\n' + L(2, 5, '(i) Explain the term stakeholder.'), 5, 'business-0-12', 'stakeholder-explained',
    5, [19], 'Explanation: 5 marks (3 + 2).', [comps('Stakeholder', (3, 2))])
add(2, 4, 'aii', 'Q4(A)(ii)', glenisk + '\n\n' + L(2, 5, '(ii) Outline the impact of the fire at Glenisk factory on two of its stakeholders.'), 15, 'business-0-12',
    'fire-impact-stakeholders', 5, [19], EIGHT, eight_seven('Stakeholder impact'), [UNTIED8])
add(2, 4, 'b', 'Q4(B)', L(2, 5, '(B) Outline, using an example, the role of interest groups.'), 15, 'business-0-12', 'interest-groups-role',
    5, [19], 'Role 10 (5 + 5) and example 5.', seq(comps('Role', (5, 5)), single('Example', 5, 'Interest group example')))
house = L(2, 5, 'Sinead and Patrick Malone finally found the home they were looking for after a 2 year search. They put in an offer of €320,000 for the house and this was accepted by the seller. Sinead and Patrick are both aged 31 and want to buy the house.')
element = opt_resp([('component-1', 'Component 1', 3), ('component-2', 'Component 2', 2)])
P.pool(2, 4, 'c', '4(C)', 5, [6, 20], 3, L(2, 5, '(C) Explain, with reference to the text above, three of the following elements of a valid contract:'),
       house + '\n\nExplain, with reference to the text above, the following three elements of a valid contract:',
       [dict(id='offer-acceptance', label=L(2, 5, '(i) Offer and Acceptance (Agreement)'), response=element),
        dict(id='capacity', label=L(2, 5, '(ii) Capacity to Contract'), response=element),
        dict(id='consideration', label=L(2, 5, '(iii) Consideration'), response=element),
        dict(id='consent', label=L(2, 5, '(iv) Consent to Contract.'), response=element)],
       15, 'Explain each selected element with reference to the text at 5 marks (3 + 2).', [], 'business-0-12', 'valid-contract-elements',
       'The paper prints four elements of a valid contract and asks for three. All four selections are generated at 15 marks; the legacy card is the first three printed elements.',
       legacy=legacy_route('bus-2022-ol-s2-q4c', ['offer-acceptance', 'capacity', 'consideration'], 5, [6, 20],
                           'question text and the house-purchase extract lifted from the printed paper; the card becomes the first three printed elements of the expanded choose-three pool.'))
add(2, 4, 'd', 'Q4(D)', L(2, 5, '(D) Describe two methods of terminating (ending) a contract.'), 15, 'business-0-12', 'contract-termination-methods',
    5, [20], EIGHT, eight_seven('Method'), [UNTIED8])
add(2, 4, 'e', 'Q4(E)', L(2, 5, '(E) Outline one function of the Competition and Consumer Protection Commission (CCPC).'), 10, 'business-0-13', 'ccpc-function',
    5, [21], 'One function: 10 marks (5 + 5).', [comps('Function', (5, 5))])

pure = L(2, 6, 'Pure Clothing, based in Mayo, was founded by Peter Timlin and Richard Grimes in May 2020. The company quickly went viral on TikTok by posting videos which showcased the pair’s journey setting up the company and their sustainable model. Pure Clothing is a completely sustainable brand which uses organic cotton and recycled material for its vegan-friendly clothing, which is embroidered in a wind-powered unit in Co. Mayo.')
add(2, 5, 'a', 'Q5(A)', pure + '\n\n' + L(2, 6, '(A) Outline three enterprising characteristics/skills displayed by entrepreneurs such as Peter and Richard.'), 15, 'business-1-5',
    'enterprising-characteristics', 6, [22], 'Three at 5 marks each (3 + 2).', points('Characteristic', 3, (3, 2)))
add(2, 5, 'b', 'Q5(B)', pure + '\n\n' + L(2, 6, '(B) Explain two risks and two rewards for entrepreneurs like Peter and Richard setting up a new business.'), 20, 'business-1-5',
    'risks-and-rewards', 6, [22], 'Two risks and two rewards at 5 marks each (3 + 2).',
    seq(points('Risk', 2, (3, 2)), points('Reward', 2, (3, 2))))
add(2, 5, 'c', 'Q5(C)', pure + '\n\n' + L(2, 6, '(C) Discuss two reasons why quality control is important for a clothing business.'), 15, 'business-2-13',
    'quality-control-reasons', 6, [23], TWO, ten_five('Reason'), [UNTIED])
add(2, 5, 'd', 'Q5(D)', pure + '\n\n' + L(2, 6, '(D) Outline two benefits for a business of communicating with their customers using social media.'), 15, 'business-2-12',
    'social-media-communication', 6, [23], TWO, ten_five('Benefit'), [UNTIED])
add(2, 5, 'e', 'Q5(E)', pure + '\n\n' + L(2, 6, '(E) List two advantages to Peter and Richard of preparing a SWOT analysis for their business.'), 10, 'business-2-13',
    'swot-advantages', 6, [24], 'Two advantages at 5 marks each (3 + 2).', points('Advantage', 2, (3, 2)))

ryan = L(2, 7, 'Ryan’s Dog Groomers', 'Ryan Murphy runs a successful dog grooming business. In the last two years, he has noticed an increased demand for his services as pet ownership in Ireland increases. To continue to meet demand Ryan is planning to expand his business. As part of this expansion, he is planning to purchase a van so he can launch a mobile dog grooming service.', sep='\n')
sources = L(2, 7, '(A) Ryan has the option of three medium term sources of finance for the purchase of his van:', 'Medium Term Loan Hire Purchase Leasing')
source = opt_resp([('component-1', 'Component 1', 4), ('component-2', 'Component 2', 3)])
P.pool(2, 6, 'ai', '6(A)(i)', 7, [6, 25], 2, L(2, 7, '(i) Explain two of these sources of finance.'),
       ryan + '\n\n' + sources + '\n(i) Explain the following two sources of finance.',
       [dict(id='medium-term-loan', label='Medium Term Loan', response=source), dict(id='hire-purchase', label='Hire Purchase', response=source),
        dict(id='leasing', label='Leasing', response=source)],
       14, 'Explain each selected source at 7 marks (4 + 3).', ['Part (ii) asks for one advantage of each source chosen here and is its own card.'],
       'business-3-16', 'medium-term-finance-sources',
       'The paper prints three medium-term sources and asks for two. All three pairs are generated at 14 marks; the legacy card is the first printed pair.',
       legacy=legacy_route('bus-2022-ol-s2-q6ai', ['medium-term-loan', 'hire-purchase'], 7, [6, 25],
                           'question text and the Ryan’s Dog Groomers extract lifted from the printed paper; the card becomes the first printed pair of the expanded choose-two pool.'))
add(2, 6, 'aii', 'Q6(A)(ii)', ryan + '\n\n' + sources + '\n' + L(2, 7, '(i) Explain two of these sources of finance.', '(ii) Outline one advantage of each source chosen.'), 6,
    'business-3-16', 'medium-term-finance-advantages', 7, [25], 'One advantage of each chosen source at 3 marks.', points('Advantage', 2, (3,)),
    ['Answer for the two sources you chose in (i); the scheme gives advantages of a medium-term loan, hire purchase and leasing.'])
add(2, 6, 'b', 'Q6(B)', ryan + '\n\n' + L(2, 7, '(B) Outline three types of insurance you would expect Ryan’s Dog Groomers to have.'), 15, 'business-3-17',
    'business-insurance-types', 7, [26], 'Three types at 5 marks each (3 + 2).', points('Insurance', 3, (3, 2)))
add(2, 6, 'c', 'Q6(C)', ryan + '\n\n' + L(2, 7, '(C) Explain, with reference to Ryan, the principle of Utmost Good Faith in relation to insurance.'), 10, 'business-3-17',
    'utmost-good-faith-ryan', 7, [26], 'Explanation: 10 marks (5 + 5).', [comps('Utmost good faith', (5, 5))])
chart = add(2, 6, 'd', 'Q6(D)', ryan + '\n\n' + L(2, 7, '(D) The following are the net profit figures for Ryan’s business for the period 2017-2021:',
                                                 'Year 2017 2018 2019 2020 2021 Net Profit €35,000 €45,000 €40,000 €55,000 €60,000',
                                                 'Illustrate the above information on a bar chart. Use the graph paper provided on page 10 in the answerbook.'), 15,
            'business-2-12', 'net-profit-bar-chart', 7, [27], 'Title 1, labelled axes 2 + 2 and five bars at 2 marks each (1 each if not to scale).',
            [response(1, 'Bar chart', [('title', 'Title', 1), ('axis-1', 'Labelled axis 1', 2), ('axis-2', 'Labelled axis 2', 2), ('bar-2017', '2017: €35,000', 2),
                                       ('bar-2018', '2018: €45,000', 2), ('bar-2019', '2019: €40,000', 2), ('bar-2020', '2020: €55,000', 2), ('bar-2021', '2021: €60,000', 2)])],
            ['Scheme: “' + S(27, '5 Bars @ 2m each (1m each if not to scale)') + '”.'], extra=['business-3-16'])
for k in (1, 2):
    permit(chart, 0, [0, 2], k)
add(2, 6, 'e', 'Q6(E)', ryan + '\n\n' + L(2, 7, '(E) Outline two uses of ICT for Ryan’s business.'), 15, 'business-2-12', 'ict-uses',
    7, [27], EIGHT, eight_seven('Use'), [UNTIED8])

leah = L(2, 8, 'Value Insurance Ltd Leah Corcoran recently began a new job as an insurance sales agent at Value Insurance Ltd in Limerick city. Value Insurance Ltd is a growing company that sells a variety of insurance policies to individuals, families, and businesses. To prepare Leah for her role, she received induction training and on-the-job training. She is paid a basic wage of €400 per week plus a commission of 5% on all sales she makes. All employees work on sales teams. The business is currently seeking a new Claims Team Manager and the Human Resource Manager is considering internal recruitment.')
add(2, 7, 'a', 'Q7(A)', leah + '\n\n' + L(2, 8, '(A) Explain the terms induction training and on-the-job training.'), 10, 'business-3-20', 'induction-and-on-the-job-training',
    8, [28], 'Each required term at 5 marks (3 + 2).', [comps('Induction training', (3, 2), i=1), comps('On-the-job training', (3, 2), i=2)])
add(2, 7, 'b', 'Q7(B)', leah + '\n\n' + L(2, 8, '(B) Outline two benefits to the business of the employees working as part of a team.'), 15, 'business-3-20',
    'teamwork-benefits', 8, [28], EIGHT, eight_seven('Benefit'), [UNTIED8])
gross = add(2, 7, 'ci', 'Q7(C)(i)', leah + '\n\n' + L(2, 8, '(i) In Week 24 Leah achieved sales to the value of €20,000. Using the information supplied above calculate Leah’s Gross Pay for Week 24. Show your workings.'),
            10, 'business-3-20', 'gross-pay-commission', 8, [28], 'Five figures at 2 marks each.',
            [response(1, 'Gross pay', [('sales', 'Sales €20,000', 2), ('rate', '× 5%', 2), ('commission', 'Commission €1,000', 2), ('basic', 'Basic wage €400', 2),
                                       ('gross', 'Gross pay €1,400', 2)])],
            ['Scheme working: ' + S(28, '€20,000 × 5% = €1,000 + €400 = €1,400') + '.'], extra=['business-3-18'])
for k in range(5):
    permit(gross, 0, [0, 2], k)
cum(2, 7, 'cii', 'Q7(C)(ii)', leah + '\n\n' + L(2, 8, '(ii) List two statutory deductions that must be deducted from Leah’s pay.'), (5, 5), 'business-3-18',
    'statutory-deductions', 8, [28], 'Scheme: ' + S(28, 'PAYE – Pay As You Earn') + '; PRSI; USC.', noun='deductions')
add(2, 7, 'd', 'Q7(D)', leah + '\n\n' + L(2, 8, '(D) Outline two benefits to the business of internal recruitment.'), 15, 'business-3-20', 'internal-recruitment-benefits',
    8, [29], EIGHT, eight_seven('Benefit'), [UNTIED8])
add(2, 7, 'e', 'Q7(E)', leah + '\n\n' + L(2, 8, '(E) Explain two reasons why maintaining good Employer/Employee relations is an important role of the Human Resource Manager.'), 15,
    'business-3-20', 'employer-employee-relations', 8, [29], EIGHT, eight_seven('Reason'), [UNTIED8])

miriam = L(2, 9, 'Miriam Lloyd set up her business ‘Christening Generations’ in 2016 operating as a sole trader. Her business customises wedding dresses into unique handmade christening gowns. Miriam always had a passion for sewing and is an experienced dressmaker.',
           'She received support from her Local Enterprise Office (LEO) in Carlow.', sep=' ')
add(2, 8, 'ai', 'Q8(A)(i)', miriam + '\n\n' + L(2, 9, '(i) Explain the term sole trader.'), 5, 'business-5-14', 'sole-trader-explained',
    9, [30], 'Explanation: 5 marks (3 + 2).', [comps('Sole trader', (3, 2))])
add(2, 8, 'aii', 'Q8(A)(ii)', miriam + '\n\n' + L(2, 9, '(ii) Outline two benefits of operating as a sole trader.'), 15, 'business-5-14', 'sole-trader-benefits',
    9, [30], EIGHT, eight_seven('Benefit'), [UNTIED8])
add(2, 8, 'b', 'Q8(B)', miriam + '\n\n' + L(2, 9, '(B) Explain three sources of new product ideas for a business.'), 15, 'business-4-14', 'sources-of-ideas',
    9, [31], 'Three sources at 5 marks each (3 + 2).', points('Source', 3, (3, 2)))
cum(2, 8, 'ci', 'Q8(C)(i)', miriam + '\n\n' + L(2, 9, '(i) List two headings in a business plan.'), (3, 3), 'business-4-15', 'business-plan-headings',
    9, [32], 'Scheme examples: ' + S(32, 'Description of Business & Owners') + ', management and organisation structure, product or service, market analysis, marketing strategy, finance.',
    noun='headings')
add(2, 8, 'cii', 'Q8(C)(ii)', miriam + '\n\n' + L(2, 9, '(ii) Explain two benefits of preparing a business plan.'), 14, 'business-4-15', 'business-plan-benefits',
    9, [32], 'Two benefits at 7 marks each (4 + 3).', points('Benefit', 2, (4, 3)))
add(2, 8, 'd', 'Q8(D)', miriam + '\n\n' + L(2, 9, '(D) Explain the term USP with reference to Miriam’s business.'), 10, 'business-4-17', 'usp-miriam',
    9, [32], 'Explanation 6 (3 + 3) and reference to Miriam’s business 4.', seq(comps('USP explained', (3, 3)), single('Reference to Miriam’s business', 4, 'Her USP')),
    ['Scheme: ' + S(32, 'Miriam’s USP is that she customises wedding dresses into unique handmade christening gowns.')])
cum(2, 8, 'e', 'Q8(E)', miriam + '\n\n' + L(2, 9, '(E) List two services that the LEO could have provided to Miriam to assist when setting up her business.'), (5, 5),
    'business-5-16', 'leo-services', 9, [32], 'Scheme examples: Mentoring, Grant aid, Advice & assistance, Training.', noun='services')

kelloggs = L(2, 10, 'Kelloggs has a variety of products at different stages of the product life cycle')
promo = L(2, 10, 'Kellogg’s uses a variety of promotion methods including public relations to promote their brand to their target market.')
add(2, 9, '-a', 'Q9(A)', kelloggs + '\n\n' + L(2, 10, '(A) Draft and label the Product Life Cycle diagram showing all five stages.'), 15, 'business-4-17', 'plc-diagram',
    10, [33], 'Title 1, Sales 1, Time 1, curved line 2 and the five stages in order at 2 marks each.',
    [fixed('Product life cycle diagram', [('Title', 1), ('Sales axis', 1), ('Time axis', 1), ('Curved line', 2), ('Stage 1', 2), ('Stage 2', 2), ('Stage 3', 2),
                                          ('Stage 4', 2), ('Stage 5', 2)])],
    ['Scheme: ' + S(33, 'Title: 1m Sales: 1m Time: 1m Curved Line: 2m Stages: (in order) 5 x 2m') + ' (introduction, growth, maturity, saturation and decline).'], new=True)
permit(P.created[-1], 0, [0, 1, 2], 3)
add(2, 9, '-b', 'Q9(B)', kelloggs + '\n\n' + L(2, 10, '(B) Outline two benefits to a business of carrying out market research before launching a new product.'), 15, 'business-4-16',
    'market-research-benefits', 10, [33], EIGHT, eight_seven('Benefit'), [UNTIED8])
add(2, 9, '-c', 'Q9(C)', kelloggs + '\n\n' + L(2, 10, '(C) Explain, using an example, the term target market.'), 10, 'business-4-16', 'target-market-explained',
    10, [34], 'Explanation and example: 4 + 3 + 3.', [comps('Target market', (4, 3, 3), ['Explanation', 'Explanation developed', 'Example'])], new=True)
add(2, 9, '-d-i', 'Q9(D)(i)', promo + '\n\n' + L(2, 10, '(i) Explain the term Public Relations (PR).'), 5, 'business-4-17', 'public-relations-explained',
    10, [34], 'Explanation: 5 marks (3 + 2).', [comps('Public Relations', (3, 2))], new=True)
add(2, 9, '-d-ii', 'Q9(D)(ii)', promo + '\n\n' + L(2, 10, '(ii) Outline two methods of Public Relations other than sponsorship, a business could use.'), 15, 'business-4-17',
    'public-relations-methods', 10, [34], EIGHT, eight_seven('Method'), [UNTIED8], new=True)
add(2, 9, '-e', 'Q9(E)', promo + '\n\n' + L(2, 10, '(E) List two advertising media that a business could use and outline a reason for your choice in each case.'), 15,
    'business-4-17', 'advertising-media-reasons', 10, [35], EIGHT, eight_seven('Medium and reason'), [UNTIED8])

# ---------------------------------------------------------------- checks and write-out
qn = lambda c: c['questionRef'].split(' Q')[1].split('(')[0]
s1 = [c for c in P.created if c['section'] == '1']
for q in range(1, 16):
    assert sum(c['totalMarks'] for c in s1 if qn(c) == str(q)) == 15, q
pool_q = {}
for p in P.pools:
    k = p['template']['questionRef'].split(' Q')[1].split('(')[0]
    pool_q[k] = pool_q.get(k, 0) + p['template']['totalMarks']
for q in range(1, 10):
    tot = sum(c['totalMarks'] for c in P.created if c['section'] == '2' and qn(c) == str(q)) + pool_q.get(str(q), 0)
    assert tot == 75, (q, tot)
legacy = {i for i in ORIGINAL if i.startswith('bus-2022-ol-')}
covered = {c['id'] for c in P.created} | {p['legacyRoute']['id'] for p in P.pools if 'legacyRoute' in p}
assert legacy <= covered, sorted(legacy - covered)
new = sorted(c['id'] for c in P.created if c['id'] not in ORIGINAL)
assert new == ['bus-2022-ol-s2-q9-a', 'bus-2022-ol-s2-q9-c', 'bus-2022-ol-s2-q9-d-i', 'bus-2022-ol-s2-q9-d-ii'], new

SELECTION = {
    1: 'No finite printed answer menu occurs in Section 1 (answer five of fifteen at 15 marks). Theory X/Y and True/False labels, ticks, matching rows, circled options, the image tasks in Q2 and Q14 and the word bank in Q8 are required answer formats. Support-note lists are open examples.',
    2: 'Two finite printed pools are expanded: Q4(C) three of four contract elements (four routes) and Q6(A)(i) two of three medium-term sources (three routes), each with its legacy card as the first printed route; Q6(A)(ii) asks for one advantage of each source chosen and is its own card. Q4(A)(ii) stakeholders are the candidate’s choice. Sub-parts with their own published marks are separate cards. Support-note lists are open examples.',
}


def classify(fileid, page, m, w):
    if m.lower().startswith('answer'):
        return 'exam-navigation', 'The rubric sets how many whole questions a candidate answers. Every numbered question remains in the practice corpus as separate cards.', None
    if fileid == 'LC033GLP033EV' and m == 'three of' and 'elements of a valid contract' in w:
        return 'finite-pool', 'Section 2 Q4(C) asks for three of four printed elements of a valid contract; all four selections are generated at 15 marks.', 'bus-2022-ol-s2-q4c'
    if fileid == 'LC033GLP033EV' and m == 'two of' and 'two of these sources of finance' in w:
        return 'finite-pool', 'Section 2 Q6(A)(i) asks for two of three printed medium-term sources; all three pairs are generated at 14 marks, and (ii) asks for one advantage of each source chosen.', 'bus-2022-ol-s2-q6ai'
    if m == 'two of' and 'two of its stakeholders' in w:
        return 'open-response', 'Section 2 Q4(A)(ii) lets the candidate choose any two stakeholders; no closed list is printed, so the task stays whole.', None
    if m == 'or' and 'surplus or a deficit' in w:
        return 'required-headings', 'Section 2 Q3(C)(ii) requires a determination of surplus or deficit; it is one required answer, not a choice of task.', None
    if m == 'or' and 'refunds or exchange' in w:
        return 'case-context', 'The Section 2 Q1 sale sign reads “No refunds or exchange on sale items”; it is case context.', None
    if m == 'or' and 'Theory X or Theory Y' in w:
        return 'required-headings', 'Theory X/Theory Y are answer labels for each of the four required statements in Section 1 Q3, not optional tasks.', None
    if m == 'or' and ('TRUE or FALSE' in w or 'True or False' in w):
        return 'required-headings', 'True/False are answer labels for each of the four required statements in Section 1 Q12, not optional tasks.', None
    if m == 'Choose' and 'Choose the appropriate terms' in w:
        return 'required-headings', 'Section 1 Q8 is a word-bank completion: both blanks are required and the printed terms are the answer options, not optional tasks.', None
    assert (fileid, page) in {('LC033GLP032EV', 2), ('LC033GLP032EV', 9), ('LC033GLP032EV', 36), ('LC033GLP033EV', 1), ('LC033GLP033EV', 2)}, (fileid, page, m, w)
    return 'exam-navigation', 'Cover instructions, the question-choice rubric, pen/pencil instructions, answerbook supplies or copyright boilerplate. They do not create alternative task routes.', None


n = P.write([(1, range(1, 16)), (2, range(1, 10))], SELECTION, classify,
            'Every part of {year} Ordinary Section {section} Question {q} was visually checked against its SEC booklet, allocation summary and support notes. Booklet-specific p1/p2 identities keep the short and long question numbering apart.')
print(f'Reviewed {len(P.created)} 2022 Ordinary base tasks and {len(P.pools)} route pools; classified {n} raw selection matches.')
