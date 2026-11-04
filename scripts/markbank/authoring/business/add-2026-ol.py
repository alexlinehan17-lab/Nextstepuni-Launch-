"""Review the 2026 Ordinary English paper (Section 1 and Section 2)."""
from bus_lib import Paper, comps, points, seq, unequal, single, ten_five, response

T = {(1, q): 4 for q in range(1, 16)}
T.update({(2, 1): 5, (2, 2): 5, (2, 3): 6, (2, 4): 6, (2, 5): 7, (2, 6): 7, (2, 7): 8, (2, 8): 8, (2, 9): 8})
P = Paper(2026, 'ordinary', {1: 'LC033GLP032EV', 2: 'LC033GLP033EV'}, 'LC033GLP000EV', T)
L, S, add, cum = P.lift, P.scheme, P.add, P.cumulative
TWO = 'Two points are required: 10 (7 + 3) and 5 (4 + 1).'
UNTIED = 'The 10-mark allowance is not tied to a particular point.'

# ---------------------------------------------------------------- Section 1
add(1, 1, '', 'Q1', L(1, 3, 'What do the following letters stand for? Write answers in spaces provided.', 'USP', 'BIK', 'USC'), 10,
    'business-4-17', 'business-abbreviations', 3, [9], 'Each term carries its own marks: 4 (2 + 1 + 1), 3 (1 + 1 + 1) and 3 (1 + 1 + 1).',
    [comps('USP (first term)', (4,), ['Term written in full'], 1), comps('BIK (second term)', (3,), ['Term written in full'], 2),
     comps('USC (third term)', (3,), ['Term written in full'], 3)],
    ['Answer key: USP ' + S(9, 'Unique Selling Point') + '; BIK ' + S(9, 'Benefit in Kind') + '; USC ' + S(9, 'Universal Social Charge') + '. Each word earns its share of the term’s marks.'],
    extra=['business-3-18'])
cum(1, 2, '', 'Q2', L(1, 3, 'Indicate True or False after each of the following statements.',
                         'A strategic plan is a long-term plan of the overall goal of the business.',
                         'A contingency plan is a plan put in place should something expected happen.',
                         'A tactical plan is for 5 to 10 years.', 'A mission statement is a summary of the vison, aims and values of a business.'),
    (3, 3, 2, 2), 'business-2-13', 'planning-true-false', 3, [9], 'Answer key: True; False; False; True (scheme page 9).')
cum(1, 3, '', 'Q3', L(1, 3, 'Identify the three other elements of the marketing mix.') + '\nProduct', (4, 3, 3), 'business-4-17', 'marketing-mix-elements',
    3, [9], 'Answer key: Price; Place; Promotion (shaded on scheme page 9).')
cum(1, 4, '', 'Q4', L(1, 4, 'Indicate, by placing a tick (✓) in the correct box, the European Institution that each statement best describes.')
    + '\nEuropean Parliament / European Commission / Council of the EU\n' + L(1, 4, '(i) Manage the day to day running of the EU', '(ii) Debate and approve EU law',
                                                                          '(iii) Adopt EU Law and co-ordinates EU Policy'),
    (4, 3, 3), 'business-6-14', 'eu-institutions-ticks', 4, [9], 'Answer key (ticks on scheme page 9): (i) European Commission; (ii) European Parliament; (iii) Council of the EU.')
cum(1, 5, '', 'Q5', L(1, 4, 'Match the example in the table with the most relevant type of international trade from the list below:') + '\n'
    + L(1, 4, '• Visible import • Invisible import • Visible export • Invisible export.').replace(' • ', '\n• ') + '\n'
    + '(i) ' + L(1, 4, 'Spanish student studying in Ireland') + '\n(ii) ' + L(1, 4, 'Kerrygold butter sold in France') + '\n(iii) '
    + L(1, 4, 'Bananas sold in Ireland') + '\n(iv) ' + L(1, 4, 'Irish citizen travelling to New York'),
    (3, 3, 2, 2), 'business-6-13', 'international-trade-types', 4, [10],
    'Answer key: (i) Invisible Export; (ii) Visible Export; (iii) Visible Import; (iv) Invisible Import (scheme page 10).')
add(1, 6, '', 'Q6', L(1, 5, 'Explain the difference between an Intrapreneur and an Entrepreneur.'), 10, 'business-1-5', 'intrapreneur-versus-entrepreneur',
    5, [10], 'Explain both required terms at 5 marks each (3 + 2).', [comps('Intrapreneur', (3, 2), i=1), comps('Entrepreneur', (3, 2), i=2)])
add(1, 7, '', 'Q7', L(1, 5, 'Complete levels 2 and 4 of Maslow’s Hierarchy of Needs pyramid.') + '\n'
    + L(1, 5, '5. Self - Actualisation', '4._______________________', '3. Social', '2._____________________', '1. Physiological'), 10,
    'business-2-11', 'maslow-levels-2-and-4', 5, [10], 'Each missing level earns 5 marks.',
    seq(single('Level 2', 5, 'Level 2 named'), single('Level 4', 5, 'Level 4 named')),
    ['Answer key: level 2 ' + S(10, 'Safety / Security') + '; level 4 ' + S(10, 'Esteem / Self Esteem') + '.'])
add(1, 8, '', 'Q8', L(1, 5, 'Outline the purpose of the following insurance forms.') + '\n' + L(1, 5, '1. Proposal Form:', '2. Claims Form:'), 10,
    'business-3-17', 'insurance-forms', 5, [11], 'Explain both forms at 5 marks each (3 + 2).',
    [comps('Proposal form', (3, 2), i=1), comps('Claims form', (3, 2), i=2)])
c = add(1, 9, '', 'Q9', L(1, 6, 'Choose the appropriate words to complete the sentences below. (One word does not apply)', 'Matrix Narrow Wide',
                         '(i) A team-based organisational structure is called a _____________________ organisational structure.',
                         '(ii) Directly supervising a large number of employees means a manager has a _______________ span of control.'), 10,
        'business-2-13', 'structure-and-span-words', 6, [11], 'Each completed sentence earns 5 marks.',
        seq(single('Sentence (i)', 5, 'Word chosen'), single('Sentence (ii)', 5, 'Word chosen')),
        ['Answer key: (i) ' + S(11, 'Matrix') + '; (ii) ' + S(11, 'Wide') + '. Narrow is not used.'])
cum(1, 10, '', 'Q10', L(1, 6, 'Indicate whether each of the following is an example of Direct or Indirect Tax by placing direct or indirect into the box.') + '\n'
    + L(1, 6, 'PAYE (Pay as you earn)', 'Local Property Tax', 'VAT (Value Added Tax)', 'Excise Duty'),
    (3, 3, 2, 2), 'business-3-18', 'direct-indirect-tax', 6, [11], 'Answer key: PAYE Direct; Local Property Tax Direct; VAT Indirect; Excise Duty Indirect.')
add(1, 11, '', 'Q11', L(1, 6, 'List two responsibilities a data controller has in relation to their ‘customers data’ under General Data Protection Regulation (GDPR).'),
    10, 'business-2-12', 'gdpr-data-controller-responsibilities', 6, [11], 'List two responsibilities at 5 marks each (3 + 2).', points('Responsibility', 2, (3, 2)),
    extra=['business-0-13'])
cum(1, 12, '', 'Q12', L(1, 7, 'Circle the correct option in each of the following statements:',
                          '(i) An increase in the cost of goods from one year to the next is called inflation/deflation.',
                          '(ii) Higher employment rates lead to an increase/decrease in government spending on social welfare.',
                          '(iii) Higher interest rates mean the total cost of borrowing will be higher/lower for consumers.',
                          '(iv) A recession will lead to an increase/decrease in spending amongst consumers.'),
    (3, 3, 2, 2), 'business-5-15', 'economy-statements-options', 7, [12], 'Answer key (circled on scheme page 12): (i) inflation; (ii) decrease; (iii) higher; (iv) decrease.')
plc = L(1, 7, 'The diagram below illustrates the product life cycle. Answer the questions which follow.') + '\nProduct Life Cycle: Launch, Growth, Maturity, Saturation, Stage 5 (sales against time).'
add(1, 13, 'i', 'Q13(i)', plc + '\n\n' + L(1, 7, '(i) Identify the stage above, labelled stage 5.'), 5, 'business-4-17', 'plc-stage-5', 7, [12],
    'Identify the stage for 5 marks.', [single('Stage 5', 5, 'Stage identified')], ['Answer: ' + S(12, 'Decline') + '.'])
add(1, 13, 'ii', 'Q13(ii)', plc + '\n\n' + L(1, 7, '(ii) Identify a stage of the product life cycle where sales increase.'), 5, 'business-4-17',
    'plc-sales-increase-stage', 7, [12], 'Identify one stage for 5 marks.', [single('Stage where sales increase', 5, 'Stage identified')],
    ['Scheme: ' + S(12, 'Launch / Growth / Maturity') + '.'])
add(1, 14, '', 'Q14', L(1, 8, 'The following information is available from the final accounts of Deacy Ltd on the 31/12/25. Calculate the Acid Test Ratio.') + '\n'
    + L(1, 8, 'Current Assets €110,000 (includes closing stock of €42,000)', 'Current Liabilities €136,000'), 10, 'business-3-19', 'acid-test-ratio',
    8, [12], 'Formula 3, workings 3 and answer 4.',
    [response(1, 'Acid test ratio', [('formula', 'Formula: ' + S(12, 'Current Assets – Closing Stock : Current Liabilities'), 3),
                                     ('workings', 'Workings: ' + S(12, '(110,000 – 42,000) : 136,000'), 3), ('answer', 'Answer: ' + S(12, '0.5 : 1'), 4)])])
cum(1, 15, '', 'Q15', '\n'.join([L(1, 8, 'In the following table, Column 1 is a list of stakeholders. Column 2 is a list of explanations.'),
                                 L(1, 8, '1. Government', '2. Consumer', '3. Investor', '4. Manager', '5. Supplier'),
                                 L(1, 8, 'A. Has the idea and the initiative to take the risk of setting up a business.',
                                   'B. Plan and control business activities to achieve organisational goals efficiently.',
                                   'C. Provide necessary materials or services required for business production.',
                                   'D. Provide funds to businesses with the expectation of earning returns on their investment.',
                                   'E. They regulate businesses through laws, taxes, and policies to ensure fair and legal operations.',
                                   'F. Purchase goods and services and influence business decisions through their needs and choices.'),
                                 L(1, 8, 'Match the two lists by placing the letter of the correct explanation under the number of the relevant stakeholders below. One explanation has no match.')]),
    (2, 2, 2, 2, 2), 'business-0-12', 'stakeholder-matching', 8, [12], 'Answer key: 1 E; 2 F; 3 D; 4 B; 5 C. Explanation A is unused (scheme page 12).')

# ---------------------------------------------------------------- Section 2
michael = L(2, 2, 'Michael purchased a reclining leather armchair online for €720. After only 3 months the leather began peeling and discolouring. Recognising that the chair was not of merchantable quality or fit for purpose, he contacted the retailer. They refused to help, insisting he must contact the manufacturer for a remedy.')
add(2, 1, 'a', 'Q1(A)', michael + '\n\n' + L(2, 2, 'Is the retailer responsible for providing a remedy to Michael’s problem? Explain your answer.'), 15,
    'business-0-13', 'retailer-responsibility', 2, [13], 'Answer 10 and explanation 5 (4 + 1).',
    seq(single('Answer', 10, 'Yes, the retailer is responsible'), comps('Explanation', (4, 1))))
add(2, 1, 'b', 'Q1(B)', michael + '\n\n' + L(2, 2, 'Explain the terms merchantable quality and fit for purpose.'), 15, 'business-0-13',
    'merchantable-quality-fit-for-purpose', 2, [13], 'Both required terms: merchantable quality 10 (7 + 3) and fit for purpose 5 (4 + 1).',
    [comps('Merchantable quality', (7, 3), i=1), comps('Fit for purpose', (4, 1), i=2)])
add(2, 1, 'ci', 'Q1(C)(i)', michael + '\n\n' + L(2, 2, '(i) Name a consumer agency that could assist Michael.'), 10, 'business-0-13', 'consumer-agency-name',
    2, [14], 'Name the agency for 10 marks.', [single('Consumer agency', 10, 'Agency named')],
    ['Scheme: ' + S(14, 'CCPC – Competition and Consumer Protection Commission') + ' or ' + S(14, 'CAI – Consumer Association of Ireland') + '.'])
add(2, 1, 'cii', 'Q1(C)(ii)', michael + '\n\n' + L(2, 2, '(i) Name a consumer agency that could assist Michael.', '(ii) Outline one function of the consumer agency you named.'),
    5, 'business-0-13', 'consumer-agency-function', 2, [14], 'Outline one function for 5 marks (4 + 1).', [comps('Function', (4, 1))],
    ['Answer for the agency you named in (i); the scheme gives functions for the CCPC and the Consumers’ Association of Ireland.'])
add(2, 1, 'd', 'Q1(D)', michael + '\n\n' + L(2, 2, 'Outline two forms of remedy/redress that Michael is entitled to.'), 15, 'business-0-13', 'consumer-redress',
    2, [14], TWO, ten_five('Form of redress'), [UNTIED])
add(2, 1, 'e', 'Q1(E)', michael + '\n\n' + L(2, 2, 'Explain two benefits to Michael of taking his case to the Small Claims Court/Procedure if his complaint is unresolved.'),
    15, 'business-0-13', 'small-claims-benefits', 2, [15], TWO, ten_five('Benefit'), [UNTIED])

farm = L(2, 3, 'Average farm income in Ireland hit a record €48,500 in 2025', 'According to Teagasc economists, this is a 39% increase from last year. The rise was mainly due to a strong performance in the livestock sector, especially dairy and beef.', sep=' ')
add(2, 2, 'ai', 'Q2(A)(i)', farm + '\n\n' + L(2, 3, '(i) Name the sector of the economy in which farmers operate.'), 10, 'business-5-13', 'primary-sector-name',
    3, [16], 'Name the sector for 10 marks.', [single('Sector', 10, 'Sector named')], ['Answer: ' + S(16, 'Primary Sector') + '.'])
add(2, 2, 'aii', 'Q2(A)(ii)', farm + '\n\n' + L(2, 3, '(ii) Explain one reason why this sector is important to the Irish economy.'), 5, 'business-5-13',
    'primary-sector-importance', 3, [16], 'Explain one reason for 5 marks (4 + 1).', [comps('Reason', (4, 1))])
add(2, 2, 'b', 'Q2(B)', L(2, 3, 'Land is one of the factors of production. Name the other three factors of production and explain one of them.'), 15,
    'business-1-5', 'factors-of-production', 3, [16], 'Name all three other factors at 4 marks each, and explain one for 3 marks (2 + 1).',
    seq(points('Factor named', 3, (4,)), comps('Factor explained', (2, 1))), ['Answer key: ' + S(16, 'Labour / Capital / Enterprise') + '.'],
    extra=['business-5-13'])
vat = L(2, 3, 'Ireland’s hospitality VAT cut to 9% from 13.5%')
add(2, 2, 'ci', 'Q2(C)(i)', vat + '\n\n' + L(2, 3, 'Outline one impact the lower VAT rate could have on each of the following:', '(i) Tourism and hospitality in Ireland.'),
    10, 'business-3-18', 'vat-cut-tourism-impact', 3, [17], 'Outline one impact for 10 marks (7 + 3).', [comps('Impact', (7, 3))], extra=['business-5-15'])
add(2, 2, 'cii', 'Q2(C)(ii)', vat + '\n\n' + L(2, 3, 'Outline one impact the lower VAT rate could have on each of the following:', '(ii) The Irish government.'),
    5, 'business-5-15', 'vat-cut-government-impact', 3, [17], 'Outline one impact for 5 marks (4 + 1).', [comps('Impact', (4, 1))], extra=['business-3-18'])
ai = L(2, 3, 'Unethical use of AI is among top concerns for businesses')
add(2, 2, 'd', 'Q2(D)', ai + '\n\n' + L(2, 3, 'Explain how a business can behave ethically towards its employees.'), 15, 'business-5-17', 'ethical-towards-employees',
    3, [18], TWO, ten_five('Way'), [UNTIED])
add(2, 2, 'e', 'Q2(E)', ai + '\n\n' + L(2, 3, 'Outline two consequences for a business of behaving unethically.'), 15, 'business-5-17', 'unethical-consequences',
    3, [18], TWO, ten_five('Consequence'), [UNTIED])

spend = L(2, 4, 'A sample of Government Expenditure 2026') + '\nSocial Protection €29 billion; Health €27 billion; Housing €11 billion; Education €13 billion; Transport €5 billion'
for v in ['Social Protection', 'Health', 'Housing', 'Education', 'Transport', '€29 billion', '€27 billion', '€11 billion', '€13 billion', '€5 billion']:
    L(2, 4, v)
chart_resp = dict(allocations=[dict(id=k, label=l, maxMarks=m, permittedMarks=list(range(m + 1))) for k, l, m in
                               [('title', 'Title', 1), ('axis-1', 'Labelled axis 1', 2), ('axis-2', 'Labelled axis 2', 2),
                                ('social', 'Social Protection €29bn', 2), ('health', 'Health €27bn', 2), ('housing', 'Housing €11bn', 2),
                                ('education', 'Education €13bn', 2), ('transport', 'Transport €5bn', 2)]])
P.pool(2, 3, 'a', '3(A)', 4, [6, 19], 1, L(2, 4, 'Draw a Bar Chart or Line Graph to represent the above information.'),
       spend + '\n\nRepresent the above information in the following form:',
       [dict(id='bar-chart', label='Bar Chart', response=chart_resp), dict(id='line-graph', label='Line Graph', response=chart_resp)],
       15, 'Title 1, labelled axes 2 + 2, and each of the five values plotted at 2 marks (1 each if not to scale).',
       ['Scheme: “' + S(19, '(1m each if not to scale)') + '” for each bar or point. The figures are read from the printed table.'],
       'business-5-15', 'government-expenditure-chart',
       'The paper offers a closed choice of a bar chart or a line graph. Both routes are generated at 15 marks with the same published allocation.')
add(2, 3, 'bi', 'Q3(B)(i)', L(2, 4, '(i) Explain the difference between capital expenditure and current expenditure.'), 10, 'business-5-15',
    'capital-versus-current-expenditure', 4, [20], 'Explain the difference for 10 marks (7 + 3).', [comps('Difference', (7, 3))], extra=['business-3-16'])
add(2, 3, 'bii', 'Q3(B)(ii)', L(2, 4, '(ii) Identify one example of capital and one example of current expenditure for the health sector.'), 5, 'business-5-15',
    'health-expenditure-examples', 4, [20], 'Capital example 4 and current example 1.',
    seq(single('Capital expenditure example', 4), single('Current expenditure example', 1)), extra=['business-3-16'])
fdi = L(2, 4, 'In early 2025, there has been 137 investments by global companies into Ireland. A 37% increase from the same time last year.')
add(2, 3, 'ci', 'Q3(C)(i)', fdi + '\n\n' + L(2, 4, '(i) List two examples of global companies.'), 9, 'business-6-15', 'global-company-examples',
    4, [20], 'List two examples: 7 and 2.', seq(single('Example 1', 7, 'Global company'), single('Example 2', 2, 'Global company')),
    ['The scheme lists examples such as Apple, Coca-Cola and Amazon; any genuine global company is accepted.'])
add(2, 3, 'cii', 'Q3(C)(ii)', fdi + '\n\n' + L(2, 4, '(ii) Outline two reasons why a global company might set up in Ireland.'), 6, 'business-6-15',
    'global-company-reasons-ireland', 4, [20], 'Outline two reasons at 3 marks each (2 + 1).', points('Reason', 2, (2, 1)))
add(2, 3, 'd', 'Q3(D)', fdi + '\n\n' + L(2, 4, 'Explain two benefits to Ireland of FDI (Foreign Direct Investment).'), 15, 'business-6-15', 'fdi-benefits',
    4, [21], TWO, ten_five('Benefit'), [UNTIED])
tariff = L(2, 4, 'The United States (US) have imposed a 15% tariff on most European Union (EU) exports')
add(2, 3, 'ei', 'Q3(E)(i)', tariff + '\n\n' + L(2, 4, '(i) Tariffs are a barrier to international trade. Name and explain one other barrier.'), 10,
    'business-6-13', 'other-trade-barrier', 4, [22], 'Name and explain one other barrier for 10 marks (7 + 3).', [comps('Barrier', (7, 3))])
add(2, 3, 'eii', 'Q3(E)(ii)', tariff + '\n\n' + L(2, 4, '(ii) Explain one effect this 15% tariff will have on Irish trade with the US.'), 5,
    'business-6-13', 'us-tariff-effect', 4, [22], 'Explain one effect for 5 marks (4 + 1).', [comps('Effect', (4, 1))])

forsa = L(2, 5, 'There will be strict work-to-rule in place for all Fórsa members in the HSE')
add(2, 4, 'ai', 'Q4(A)(i)', forsa + '\n\n' + L(2, 5, '(i) Apart from Fórsa, name one other trade union in Ireland.'), 7, 'business-0-14', 'trade-union-name',
    5, [23], 'Name one other union for 7 marks.', [single('Trade union', 7, 'Union named')],
    ['Scheme examples: ' + S(23, 'ASTI, SIPTU, INMO, IALPA, TUI, INTO, IBOA.')])
add(2, 4, 'aii', 'Q4(A)(ii)', forsa + '\n\n' + L(2, 5, '(ii) Explain the term work-to-rule.'), 8, 'business-0-14', 'work-to-rule', 5, [23],
    'Explain the term for 8 marks (4 + 4).', [comps('Work-to-rule', (4, 4))])
add(2, 4, 'b', 'Q4(B)', L(2, 5, 'Outline two causes of industrial disputes between employees and employers.'), 15, 'business-0-14', 'industrial-dispute-causes',
    5, [23], TWO, ten_five('Cause'), [UNTIED])
car = L(2, 5, 'John is selling his car and decides to post an advert online. Shane sees the advert and expresses an interest in viewing the car. However, Shane fails to show up for the viewing. John then calls Shane, asking for payment, as he believes they had an agreement.')
add(2, 4, 'ci', 'Q4(C)(i)', car + '\n\n' + L(2, 5, '(i) Do John and Shane have a valid contract? Explain your answer.'), 10, 'business-0-12', 'valid-contract-judgement',
    5, [24], 'Answer 7 and explanation 3.', seq(single('Answer', 7, 'No valid contract'), single('Explanation', 3)))
add(2, 4, 'cii', 'Q4(C)(ii)', L(2, 5, '(ii) List two elements of a valid contract.'), 5, 'business-0-12', 'valid-contract-elements-list', 5, [24],
    'List two elements: 4 and 1.', seq(single('Element 1', 4, 'Element listed'), single('Element 2', 1, 'Element listed')))
add(2, 4, 'd', 'Q4(D)', L(2, 5, 'Frustration is one of the ways a legal contract may be terminated. Explain, using an example the term Frustration.'), 15,
    'business-0-12', 'frustration', 5, [24], 'Explain the term for 5 (4 + 1) and give an example for 10.',
    seq(comps('Explanation', (4, 1)), single('Example', 10)))
wrc = L(2, 5, 'Workplace Relations Commission (WRC) supports employer’s decision to dismiss an employee')
add(2, 4, 'ei', 'Q4(E)(i)', wrc + '\n\n' + L(2, 5, '(i) State two reasons for fair dismissal.'), 10, 'business-0-14', 'fair-dismissal-reasons',
    5, [25], 'State two reasons: 7 and 3.', seq(single('Reason 1', 7, 'Reason stated'), single('Reason 2', 3, 'Reason stated')))
add(2, 4, 'eii', 'Q4(E)(ii)', wrc + '\n\n' + L(2, 5, '(ii) Outline one form of redress for employees who are unfairly dismissed.'), 5, 'business-0-14',
    'unfair-dismissal-redress', 5, [25], 'Outline one form for 5 marks (4 + 1).', [comps('Redress', (4, 1))])

ronan = L(2, 6, 'Ronan Perceval created a solution that transformed a local problem into an international business opportunity', sep=' ') + '\n' + L(
    2, 6, 'Noticing the challenges salon owners faced with bookings, client management, and marketing, Ronan founded Phorest, a software platform tailored to the salon and spa industry. Today, Phorest serves over 5,600 salons across six countries and is the market leader in the UK and Ireland.')
cum(2, 5, 'a', 'Q5(A)', ronan + '\n\n' + L(2, 6, 'List five skills/characteristics that entrepreneurs like Ronan display.'), (6, 3, 2, 2, 2), 'business-1-5',
    'entrepreneur-characteristics-list', 6, [26], 'Scheme examples include resilience, decision-making, confidence, risk-taking and innovation; any five valid skills or characteristics.',
    noun='skills or characteristics')
add(2, 5, 'b', 'Q5(B)', ronan + '\n\n' + L(2, 6, 'Ronan turned a problem into a successful business. Outline two other sources of new business ideas for entrepreneurs.'),
    15, 'business-4-14', 'new-business-idea-sources', 6, [26], TWO, ten_five('Source'), [UNTIED])
add(2, 5, 'c', 'Q5(C)', ronan + '\n\n' + L(2, 6, 'Explain two rewards for Ronan of setting up his own business.'), 15, 'business-1-5', 'entrepreneur-rewards',
    6, [27], TWO, ten_five('Reward'), [UNTIED])
add(2, 5, 'd', 'Q5(D)', L(2, 6, 'Leadership styles include Autocratic, Democratic and Laissez-faire. Describe two features of any one leadership style.'), 15,
    'business-2-11', 'leadership-style-features', 6, [28], TWO, ten_five('Feature'),
    [UNTIED, 'The style is an open choice: the paper says styles “include” the three named, and the scheme gives features for each of them.'])
add(2, 5, 'e', 'Q5(E)', L(2, 6, 'Outline two benefits of Information and Communication Technology (ICT) for businesses.'), 15, 'business-2-12', 'ict-benefits',
    6, [29], TWO, ten_five('Benefit'), [UNTIED])

style = L(2, 7, 'Style & Go – Bringing the Salon to You') + '\n' + L(2, 7, 'After working as a trained hair stylist for ten years, Alice noticed that traditional salon visits were challenging for many people. She set up a sole-trader business in January, called Style & Go. A mobile hairdressing service that brings professional haircuts to clients’ homes and appeals to a new target market.')
add(2, 6, 'ai', 'Q6(A)(i)', style + '\n\n' + L(2, 7, '(i) Explain the term Target Market.'), 10, 'business-4-16', 'target-market', 7, [30],
    'Explain the term for 10 marks (7 + 3).', [comps('Target market', (7, 3))])
add(2, 6, 'aii', 'Q6(A)(ii)', style + '\n\n' + L(2, 7, '(ii) Name a target market for Style & Go.'), 5, 'business-4-16', 'style-and-go-target-market',
    7, [30], 'Name a target market for 5 marks.', [single('Target market', 5, 'Target market named')])
add(2, 6, 'bi', 'Q6(B)(i)', style + '\n\n' + L(2, 7, '(i) Explain the term Sole Trader as a form of business ownership.'), 9, 'business-5-14', 'sole-trader',
    7, [30], 'Explain the term for 9 marks (7 + 2).', [comps('Sole trader', (7, 2))])
add(2, 6, 'bii', 'Q6(B)(ii)', style + '\n\n' + L(2, 7, '(ii) Outline two benefits of operating as a sole trader for Alice.'), 6, 'business-5-14',
    'sole-trader-benefits', 7, [30], 'Outline two benefits at 3 marks each (2 + 1).', points('Benefit', 2, (2, 1)))
add(2, 6, 'c', 'Q6(C)', style + '\n\n' + L(2, 7, 'Name and explain two types of Insurance that Style & Go should have.'), 15, 'business-3-17', 'business-insurance-types',
    7, [31], TWO, ten_five('Insurance type'), [UNTIED])
cash = L(2, 7, 'Cashflow forecast of Style & Go for the first 3 months of 2026') + '\n' + L(
    2, 7, '2026 January February March Total', 'Total Receipts (A) 10,000 12,000 14,000 36,000', 'Total Payments (B) 14,000 10,000 8,000 32,000',
    'Net Cash A-B (4,000) 2,000 6,000 4,000', 'Opening Cash 0 (4,000) (2,000) 0', 'Closing Cash (4,000) (2,000) 4,000 4,000')
add(2, 6, 'di', 'Q6(D)(i)', cash + '\n\n' + L(2, 7, '(i) Based on Style & Go’s cashflow forecast, are they in a better financial position in January or March?'), 9,
    'business-3-16', 'cashflow-better-month', 7, [32], 'Answer for 9 marks.', [single('Answer', 9, 'Month chosen')], ['Answer: ' + S(32, 'March') + '.'])
add(2, 6, 'dii', 'Q6(D)(ii)', cash + '\n\n' + L(2, 7, '(i) Based on Style & Go’s cashflow forecast, are they in a better financial position in January or March?',
                                                '(ii) Outline two possible reasons for your answer.'), 6, 'business-3-16', 'cashflow-better-month-reasons',
    7, [32], 'Outline two reasons at 3 marks each (2 + 1).', points('Reason', 2, (2, 1)),
    ['The scheme’s answer to (i) is March; its reasons include higher receipts, lower payments and the closing cash surplus.'])
add(2, 6, 'e', 'Q6(E)', style + '\n\n' + L(2, 7, 'Outline two benefits to Alice of preparing a Cashflow forecast for Style & Go.'), 15, 'business-3-16',
    'cashflow-forecast-benefits', 7, [32], TWO, ten_five('Benefit'), [UNTIED])

email = L(2, 8, 'Email To: All Staff From: Management CC: Human Resource Department Date: 13/04/26 Re: Internal Management Recruitment We are recruiting for a Sales Floor Supervisor to lead our team. The position has a basic wage of €645 per week plus an 8% commission on sales achieved. For further information, please contact the Human Resource (HR) Department. Best of luck to all candidates. Signed: John Murphy Director', sep=' ')
email = (email.replace(' To:', '\nTo:').replace(' From:', '\nFrom:').replace(' CC:', '\nCC:').replace(' Date:', '\nDate:').replace(' Re:', '\nRe:')
         .replace(' We are', '\n\nWe are').replace(' Signed:', '\n\nSigned:'))
hr = L(2, 8, 'The HR Manager must prepare a job description and person specification for the above position.')
add(2, 7, 'ai', 'Q7(A)(i)', email + '\n\n' + hr + '\n' + L(2, 8, '(i) List two items on a job description'), 10, 'business-3-20', 'job-description-items',
    8, [33], 'List two items: 7 and 3.', seq(single('Item 1', 7, 'Item listed'), single('Item 2', 3, 'Item listed')))
add(2, 7, 'aii', 'Q7(A)(ii)', email + '\n\n' + hr + '\n' + L(2, 8, '(ii) List two items on a person specification.'), 5, 'business-3-20', 'person-specification-items',
    8, [33], 'List two items: 4 and 1.', seq(single('Item 1', 4, 'Item listed'), single('Item 2', 1, 'Item listed')))
add(2, 7, 'b', 'Q7(B)', email + '\n\n' + L(2, 8, 'Outline two benefits for the business of internal recruitment.'), 15, 'business-3-20', 'internal-recruitment-benefits',
    8, [33], TWO, ten_five('Benefit'), [UNTIED])
add(2, 7, 'c', 'Q7(C)', email + '\n\n' + L(2, 8, 'Using the information above, calculate the Gross Pay (including commission) if sales were achieved to the value of €10,000. Show your workings.'),
    15, 'business-3-18', 'gross-pay-commission', 8, [34], 'Basic wage 4, commission 7 (2 + 2 + 3) and gross pay 4.',
    [response(1, 'Gross pay', [('basic', 'Basic wage: €645', 4), ('commission-sales', 'Commission: sales 10,000', 2), ('commission-rate', 'Commission: x 8%', 2),
                               ('commission', 'Commission: €800', 3), ('gross', 'Gross pay: €1,445', 4)])],
    ['Scheme working: ' + S(34, '10,000 x 8%') + ' = ' + S(34, '€800') + '; €645 + €800 = ' + S(34, '€1,445') + '.'])
coke = L(2, 8, 'Coca-Cola is the best-selling brand in Ireland for 21 successive years. They also announced a three-year sponsorship with the Premier League that began with the 2025/26 season.')
add(2, 7, 'd', 'Q7(D)', coke + '\n\n' + L(2, 8, 'Explain two advantages of branding for Coca-Cola.'), 15, 'business-4-17', 'branding-advantages',
    8, [34], TWO, ten_five('Advantage'), [UNTIED])
add(2, 7, 'e', 'Q7(E)', coke + '\n\n' + L(2, 8, 'Coca-Cola use sponsorship as a method of Public Relations. Outline two other methods Coca-Cola could use.'), 15,
    'business-4-17', 'public-relations-methods', 8, [34], TWO, ten_five('Method'), [UNTIED, 'Sponsorship is excluded by the question.'])

nike = L(2, 9, 'Nike is unveiling Project Amplify: The world’s first powered footwear', sep=' ') + '\n' + L(2, 9, 'A motorised shoe designed to help casual athletes and people with limited mobility move faster and more easily. The battery powered design is still in early testing and is expected to launch in the coming years.')
add(2, 8, 'a', 'Q8(A)', nike + '\n\n' + L(2, 9, 'Explain two benefits to Nike of carrying out market research before launching their new product.'), 15,
    'business-4-16', 'market-research-benefits', 9, [35], TWO, ten_five('Benefit'), [UNTIED])
P.pool(2, 8, 'b', '8(B)', 9, [8, 36], 2, L(2, 9, 'Explain two of the following stages of the new product development process for Nike.'),
       nike + '\n\nExplain the following two stages of the new product development process for Nike.',
       [dict(id='feasibility-study', label=L(2, 9, '(i) Feasibility Study')), dict(id='prototype-development', label=L(2, 9, '(ii) Prototype Development')),
        dict(id='test-marketing', label=L(2, 9, '(iii) Test Marketing.'))],
       15, 'Explain both selected stages: 10 (7 + 3) and 5 (4 + 1).', ['The 10-mark allowance is not tied to a particular stage.'],
       'business-4-14', 'new-product-development-stages',
       'The paper prints a closed list of three development stages and asks for two. All three pairs are generated at 15 marks with the 10/5 split unattached.',
       ordered=ten_five('Stage response'))
cum(2, 8, 'c', 'Q8(C)', nike + '\n\n' + L(2, 9, 'List three factors Nike should consider before setting the price of their new footwear.'), (10, 4, 1),
    'business-4-17', 'pricing-factors-list', 9, [36], 'Scheme examples include cost of production, target market and competitors’ prices; any three valid factors.', noun='factors')
add(2, 8, 'd', 'Q8(D)', nike + '\n\n' + L(2, 9, 'Job, Batch and Mass are production methods Nike could use when making the motorised shoe.',
                                          'What method of production would you recommend? Give one reason for your answer.'), 15, 'business-4-15',
    'production-method-recommendation', 9, [37], 'Method 10 and reason 5 (4 + 1).', seq(single('Method', 10, 'Method recommended'), comps('Reason', (4, 1))),
    ['The scheme recommends ' + S(37, 'batch production') + ' while demand is unknown.'])
add(2, 8, 'e', 'Q8(E)', nike + '\n\n' + L(2, 9, 'Outline two reasons why quality control is important when making this motorised shoe.'), 15, 'business-2-13',
    'quality-control-reasons', 9, [37], TWO, ten_five('Reason'), [UNTIED])

festivals = 'The 2026 Irish Festival Guide (a map of Irish festivals, including the Tradfest and Sea Sessions).'
add(2, 9, 'a', 'Q9(A)', festivals + '\n\n' + L(2, 10, 'Outline two ways how festivals like the Tradfest and Sea Sessions benefit community development in Ireland.'), 15,
    'business-5-16', 'festivals-community-development', 10, [38], TWO, ten_five('Way'), [UNTIED])
add(2, 9, 'b', 'Q9(B)', festivals + '\n\n' + L(2, 10, 'Outline two services that government agencies such as the Local Enterprise Office could provide to these festivals.'), 15,
    'business-5-16', 'agency-services-festivals', 10, [39], TWO, ten_five('Service'), [UNTIED])
sports = L(2, 10, 'Sports Direct opened its first store in 1982. Sports Direct officially acquired full control of the Irish retailer Heatons in 2016. There are currently 44 stores in the Republic of Ireland plus its online shop.')
add(2, 9, 'c', 'Q9(C)', sports + '\n\n' + L(2, 10, 'Explain two reasons why a business may choose to expand.'), 15, 'business-4-18', 'reasons-to-expand',
    10, [40], TWO, ten_five('Reason'), [UNTIED])
add(2, 9, 'd', 'Q9(D)', sports + '\n\n' + L(2, 10, 'Draw two channels of distribution that Sports Direct could use to distribute their products.'), 15, 'business-4-17',
    'distribution-channel-diagrams', 10, [41], 'Draw two channels using the published 4 (1 + 1 + 1 + 1) and 11 (4 + 4 + 3) marks.',
    [response(1, 'Channel diagrams', [(f'component-{k}', f'Component {k}', m) for k, m in enumerate([1, 1, 1, 1, 4, 4, 3], 1)])],
    ['The scheme’s model channels are Manufacturer/Producer → Retailer → Consumer (e.g. Sports Direct Galway) and Manufacturer/Producer → Consumer (e.g. online). It does not name which drawn elements carry which marks.'])
add(2, 9, 'e', 'Q9(E)', sports + '\n\n' + L(2, 10, 'Outline two sources of long-term finance that Sports Direct may have used to fund their expansion.'), 15, 'business-3-16',
    'long-term-finance-sources', 10, [41], TWO, ten_five('Source'), [UNTIED])

# ---------------------------------------------------------------- checks and write-out
qn = lambda c: c['questionRef'].split(' Q')[1].split('(')[0]
s1 = [c for c in P.created if c['section'] == '1']
for q in range(1, 16):
    assert sum(c['totalMarks'] for c in s1 if qn(c) == str(q)) == 10, q
pool_q = {p['template']['questionRef'].split(' Q')[1].split('(')[0]: p['template']['totalMarks'] for p in P.pools}
for q in range(1, 10):
    tot = sum(c['totalMarks'] for c in P.created if c['section'] == '2' and qn(c) == str(q)) + pool_q.get(str(q), 0)
    assert tot == 75, (q, tot)
assert not any('correction' in c for c in P.created)

SELECTION = {
    1: 'No finite printed answer menu occurs in Section 1. True/False labels, ticks, matching rows, circled options and the shared word bank in Q9 are required answer formats. Q13 splits at its two separately marked sub-parts. Responsibilities in the support notes are open examples.',
    2: 'Two finite printed pools are expanded separately: Q3(A) bar chart or line graph (two routes) and Q8(B) two of three development stages (three routes). Q5(D) names three leadership styles that styles “include”, so the style is an open choice. Q8(D) asks for a recommended method; the scheme accepts batch, so it is one task. Sub-parts with their own published marks are separate cards. Support-note lists are open examples.',
}

def classify(fileid, page, m, w):
    if m.lower().startswith('answer') or 'any other two questions' in w or 'any other Two questions' in w:
        return 'exam-navigation', 'The rubric sets how many whole questions a candidate answers. Every numbered question remains in the practice corpus as separate cards.', None
    if fileid == 'LC033GLP033EV' and 'Bar Chart or Line Graph' in w:
        return 'finite-pool', 'Section 2 Q3(A) offers a closed choice of a bar chart or a line graph; both routes are generated at 15 marks.', 'bus-2026-ol-s2-q3a'
    if fileid == 'LC033GLP033EV' and 'two of the following stages' in w:
        return 'finite-pool', 'Section 2 Q8(B) asks for two of three printed development stages; all three pairs are generated at 15 marks.', 'bus-2026-ol-s2-q8b'
    if 'any one leadership style' in w:
        return 'open-response', 'Section 2 Q5(D) says leadership styles “include” the three named; the style is an open choice and the task stays whole.', None
    if 'True or False' in w:
        return 'required-headings', 'True/False are answer labels for each of the four required statements in Section 1 Q2, not optional tasks.', None
    if 'Direct or Indirect' in w or 'direct or indirect' in w:
        return 'required-headings', 'Direct/indirect are answer labels for each of the four required taxes in Section 1 Q10.', None
    if 'merchantable quality or fit for purpose' in w:
        return 'case-context', 'The Section 2 Q1 extract describes the armchair as not of merchantable quality or fit for purpose; it is case context.', None
    if 'January or March' in w:
        return 'required-headings', 'Section 2 Q6(D)(i) requires a judgement between January and March; it is a required determination, not a choice of task.', None
    if 'Job, Batch and Mass' in w or 'motorised shoe' in w:
        return 'required-headings', 'Section 2 Q8(D) requires a recommended production method with a reason; the scheme accepts batch, so it is one task.', None
    if 'remedy/redress' in w or 'Court/Procedure' in w:
        return 'case-context', 'Slash wording within a single required task in Section 2 Q1; it creates no optional route.', None
    if 'levels 2 and 4 of' in w:
        return 'required-headings', 'Section 1 Q7 requires both named levels (2 and 4) of the pyramid; they are not alternatives.', None
    if 'Choose the appropriate words' in w:
        return 'required-headings', 'Section 1 Q9 is a word-bank completion: both sentences are required and the printed words are the answer options, not optional tasks.', None
    if 'materials or services' in w:
        return 'case-context', 'Wording inside matching explanation C of Section 1 Q15; all five stakeholders require a match.', None
    if 'Land is one of the factors' in w or 'explain one of them' in w:
        return 'open-response', 'Section 2 Q2(B) requires all three other factors to be named; the one factor explained is the candidate’s open choice from their own answer, so the task stays whole.', None
    if 'Frustration is one of the ways' in w:
        return 'case-context', 'Section 2 Q4(D) states that frustration is one way of terminating a contract before asking for it to be explained; it creates no choice of task.', None
    if 'choose to expand' in w:
        return 'case-context', 'Section 2 Q9(C) asks why a business may choose to expand; the word describes the business, not a candidate choice of task.', None
    assert (fileid, page) in {('LC033GLP032EV', 2), ('LC033GLP032EV', 9), ('LC033GLP032EV', 36)} or (fileid, page) == ('LC033GLP033EV', 12), (fileid, page, w)
    return 'exam-navigation', 'Cover instructions, pen/pencil instructions, answerbook supplies or copyright boilerplate. They do not create alternative task routes.', None

n = P.write([(1, range(1, 16)), (2, range(1, 10))], SELECTION, classify,
            'Every part of {year} Ordinary Section {section} Question {q} was visually checked against its SEC booklet, allocation summary and support notes. Booklet-specific p1/p2 identities keep the short and long question numbering apart.')
print(f'Reviewed {len(P.created)} 2026 Ordinary base tasks and {len(P.pools)} route pools; classified {n} raw selection matches.')
