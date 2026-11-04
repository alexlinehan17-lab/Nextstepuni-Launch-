"""Review the 2014 Ordinary English paper (one booklet: Section 1 and Section 2).

2014: answer ten of fifteen short questions at 10 marks and four of eight
long questions at 75 (one from Part 1, two from Part 2 and one other), all in
one twelve-page booklet (LC033GLP000EV, the same file id as its scheme). No
Ordinary card existed for 2014, so every card is new. The allocation summary
(scheme pages 4-8) sets each boundary; printed sub-parts with their own
published marks are separate cards. No printed choice of task occurs: the
underlined terms in Section 2 Q1(D) and Q6(B) are all required.
"""
from bus_lib import (Paper, ORIGINAL, comps, points, seq, unequal, single, response, fixed, permit)

T = {(1, q): 4 for q in range(1, 16)}
T.update({(2, 1): 5, (2, 2): 5, (2, 3): 6, (2, 4): 6, (2, 5): 7, (2, 6): 7, (2, 7): 8, (2, 8): 8})
P = Paper(2014, 'ordinary', {1: 'LC033GLP000EV', 2: 'LC033GLP000EV'}, 'LC033GLP000EV', T)
L, S, add, cum = P.lift, P.scheme, P.add, P.cumulative
EIGHT = 'Two points are required: 8 (4 + 4) and 7 (4 + 3).'
UNTIED = 'The 8-mark allowance is not tied to a particular point.'
TEN5 = 'Two points are required: 10 (7 + 3) and 5 (4 + 1).'
UNTIED10 = 'The 10-mark allowance is not tied to a particular point.'


def eight_seven(label):
    return unequal(label, [(4, 4), (4, 3)], None)


def ten_five(label):
    return unequal(label, [(7, 3), (4, 1)], None)


def flat(card):
    for r in card['rubric']['responses']:
        for a in r['allocations']:
            a['permittedMarks'] = [0, a['maxMarks']]
    return card


def bullets(text, sep='; '):
    return sep.join(x.strip() for x in text.split('•') if x.strip())


# ---------------------------------------------------------------- Section 1 (10 marks each)
add(1, 1, '', 'Q1', L(1, 2, 'What do the following letters stand for? (Write each answer in the space provided.)', 'HRM CEO ICT').replace(' CEO', '\nCEO').replace(' ICT', '\nICT'),
    10, 'business-2-12', 'abbreviations-hrm-ceo-ict', 2, [9], 'The first correct term earns 4 (2 + 1 + 1); the second and third 3 each (1 + 1 + 1).',
    [comps('First correct term', (4,), ['Words written in full'], 1), comps('Second correct term', (3,), ['Words written in full'], 2),
     comps('Third correct term', (3,), ['Words written in full'], 3)],
    ['Answer key: HRM ' + S(9, 'Human Resource Management (Manager)') + '; CEO ' + S(9, 'Chief Executive Officer') + '; ICT ' + S(9, 'Information & Communications Technology') + '.'],
    extra=['business-3-20'])
add(1, 2, '', 'Q2', L(1, 2, '"Apple" is one of the world\'s leading brands. Outline two benefits of having a brand name.'), 10, 'business-4-17', 'brand-name-benefits-2014',
    2, [9], 'Two benefits at 5 marks each.', points('Benefit', 2, (5,)),
    ['Scheme examples: ' + bullets(S(9, '• Makes product more easily identifiable • Differentiates from competitors products • Aids advertising • Creates customer (brand) loyalty')) + '.'])
add(1, 3, '', 'Q3', L(1, 2, 'Explain the term ‘stakeholder’ and list two examples of stakeholders in a business.') + '\nExamples: (i) (ii)', 10, 'business-0-12',
    'stakeholder-explained-with-examples', 2, [9], 'Explanation 4 (2 + 2) and two examples at 3 each.',
    seq(comps('Stakeholder explained', (2, 2)), single('Example 1', 3, 'Stakeholder named'), single('Example 2', 3, 'Stakeholder named')),
    ['Scheme: ' + S(9, 'A stakeholder is anyone or any group of people that has an interest/involvement or is directly affected by how a business is run.') + ' Examples: '
     + S(9, 'Employees, entrepreneurs, investors, shareholders, customers, suppliers, service providers, local community, government, trade associations.')])
cum(1, 4, '', 'Q4', L(1, 2, 'Complete the three missing stages of the Product Life Cycle:') + '\nIntroduction | ______ | ______ | Saturation | ______', (4, 3, 3), 'business-4-17',
    'plc-missing-stages-2014', 2, [9], 'Answer key (scheme page 9): ' + S(9, 'Introduction Growth Maturity Saturation Decline') + ' (Growth, Maturity and Decline, in order).', noun='stages')
L(1, 2, 'Introduction Saturation')
cum(1, 5, '', 'Q5', L(1, 3, 'State whether the following are functions of the CHAIRPERSON or SECRETARY at an AGM.', '1. Opens and closes the AGM.', '2. Reads the minutes from the last AGM.',
                      '3. Ensures the Agenda is followed.', '4. Take notes during the meeting and writes up the minutes after the meeting.', '5. Has the casting vote if a vote is tied.'),
    (4, 2, 2, 1, 1), 'business-2-12', 'chairperson-or-secretary', 3, [9], 'Answer key (scheme page 9): 1 Chairperson; 2 Secretary; 3 Chairperson; 4 Secretary; 5 Chairperson.')
S(9, 'Opens and closes the AGM. Chairperson')
add(1, 6, '', 'Q6', L(1, 3, 'The ice-cream manufacturer, Ben & Jerry’s, is considered to be an ethical business. Explain the term ‘ethical business’.'), 10, 'business-5-17',
    'ethical-business-explained', 3, [10], 'Explanation: 10 marks (5 + 5).', [comps('Ethical business', (5, 5))],
    ['Scheme: ' + S(10, 'An ethical business is a business which conducts itself in a fair, just and honest manner in its dealings with all its stakeholders.')])
add(1, 7, '', 'Q7', L(1, 3, 'Explain the term ‘Breach of Contract’.'), 10, 'business-0-12', 'breach-of-contract-explained', 3, [10], 'Explanation: 10 marks (5 + 5).',
    [comps('Breach of contract', (5, 5))], ['Scheme: ' + S(10, 'Breach of contract means that one party to a contract did not fulfil his/her part of contract (breaks a condition of the contract)')])
cum(1, 8, '', 'Q8', L(1, 3, 'Write TRUE or FALSE after each of the following statements:', '1. Indemnity states that you must gain from the item’s existence and suffer financially from its loss.',
                      '2. Loading is an extra charge on the basic premium due to increased risk.', '3. An insurance policy is a contract.',
                      '4. Utmost Good Faith states that the insured must be truthful about all material facts when applying for insurance.',
                      '5. An Assessor calculates the premium the insured must pay.'),
    (4, 2, 2, 1, 1), 'business-3-17', 'insurance-true-false-2014', 3, [10], 'Answer key (scheme page 10): FALSE; TRUE; TRUE; TRUE; FALSE.')
S(10, 'suffer financially from its loss. FALSE 2. Loading is an extra charge on the basic premium due to increased risk. TRUE')
flat(add(1, 9, '', 'Q9', L(1, 4, '(i) Calculate the Balance of Trade, using the following information. (Show your workings)') + '\nVisible Imports €1500m\nVisible Exports €1300m\nBalance of Trade:\n'
         + L(1, 4, '(ii) Tick (✓) the correct box to state if the Balance of Trade is a surplus or a deficit:') + ' Surplus / Deficit', 10, 'business-6-13', 'balance-of-trade-deficit-2014',
         4, [10], 'Exports 2, imports 3 and the balance 3 (the minus must show), then Deficit 2.',
         [response(1, 'Balance of trade', [('exports', '€1,300m', 2), ('imports', 'minus €1,500m', 3), ('answer', '= –€200m', 3), ('deficit', '(ii) Deficit ticked', 2)])],
         ['Scheme (page 10): ' + S(10, 'BALANCE OF TRADE = €1,300m (2) – €1,500m (3) [must show minus] = – €200m (3) [must show minus]') + '; ' + S(10, 'Deficit (2)') + '.']))
L(1, 4, 'Visible Imports €1500m Visible Exports €1300m Balance of Trade:')
cum(1, 10, '', 'Q10', '\n'.join([L(1, 4, 'Column 1 is a list of business terms. Column 2 is a list of possible explanations for these terms. (One explanation has no match.)'),
                                 L(1, 4, '1. Strategic Plan', '2. Mission Statement', '3. Contingency Plan', '4. Tactical Plan', '5. Manpower Plan'),
                                 L(1, 4, 'A. A plan setting out expected cash inflows and cash outflows.', 'B. A plan to ensure the business has the right number of employees with the right skills at the right time.',
                                   'C. A specific plan to be achieved in a relatively short term.', 'D. The overall business aim to be achieved over the life of the business.',
                                   'E. A back-up plan to cover unexpected events.', 'F. A long term plan providing a focus for the whole business.'),
                                 L(1, 4, 'Match the two lists by placing the letter of the correct explanation under the relevant number below.')]),
    (4, 2, 2, 1, 1), 'business-2-13', 'plan-types-matching', 4, [10], 'Answer key (scheme page 10): 1 F; 2 D; 3 E; 4 C; 5 B. Explanation A is unused.', noun='matches')
S(10, '1 2 3 4 5 F D E C B')
add(1, 11, '', 'Q11', L(1, 4, 'Explain the following stages in the development of a new product/service:', '(i) Feasibility Study', '(ii) Prototype Development'), 10, 'business-4-14',
    'feasibility-and-prototype', 4, [11], 'Each stage 5 marks (3 + 2).', [comps('Feasibility Study', (3, 2), i=1), comps('Prototype Development', (3, 2), i=2)],
    ['Scheme: ' + S(11, 'A Feasibility Study is carried out to see if the product can actually be made and brought to the market.') + ' '
     + S(11, 'An original working example of a new product is produced and tested')])
cum(1, 12, '', 'Q12', L(1, 4, 'List two European Union (EU) institutions.'), (5, 5), 'business-6-14', 'eu-institutions-2014', 4, [11],
    'Scheme institutions (page 11): ' + bullets(S(11, '• European Parliament • European Commission • Council of EU (formerly Council of Ministers) • European Court of Auditors • European Court of Justice • European Central Bank.')),
    noun='institutions')
cum(1, 13, '', 'Q13', L(1, 5, 'Complete the following table which refers to the Sale of Goods & Supply of Services Act 1980, by placing a tick (✓) in the correct box for each statement.')
    + '\nColumns: Not of merchantable quality / Not fit for purpose / Not as described / Does not match the sample\n'
    + L(1, 5, 'Waterproof coat that allows the water in.', 'Curtains have a different pattern to that seen in the shop.', 'A black phone inside a box labelled silver phone.',
        'The water dispenser of a fridge is leaking.'),
    (3, 3, 2, 2), 'business-0-13', 'sale-of-goods-ticks', 5, [11],
    'Answer key (ticks on scheme page 11): waterproof coat Not fit for purpose; curtains Does not match the sample; black phone Not as described; fridge Not of merchantable quality.',
    noun='ticks')
L(1, 5, 'Not of merchantable quality Not fit for purpose Not as described Does not match the sample')
cum(1, 14, '', 'Q14', L(1, 5, 'List three grounds for which dismissal is deemed to be unfair under the Unfair Dismissals Act 1977/2007.'), (4, 3, 3), 'business-0-14',
    'unfair-dismissal-grounds-2014', 5, [12], 'Scheme examples (page 12): ' + bullets(S(12, '• Membership of a trade union or engaging in trade union activities • Religious or political beliefs/opinions')) + '; race or colour; pregnancy; unfair selection for redundancy.',
    noun='grounds')
add(1, 15, '', 'Q15', L(1, 5, 'Explain two benefits to a business of having highly motivated employees.'), 10, 'business-2-11', 'motivated-employees-benefits-2014',
    5, [12], 'Two benefits at 5 marks each.', points('Benefit', 2, (5,)))

# ---------------------------------------------------------------- Section 2 (75 marks each)
fotos = (L(2, 6, 'Funky Fotos') + '\n' + L(2, 6, 'Jenny spotted an offer from Funky Fotos on a daily deals website of 100 photos printed for just €5.99. Jenny signed up for the deal and went to Funky Fotos. She uploaded her 5’x7’ photos for printing and was told to come back the next day to collect them as they were extremely busy. Jenny returned the following day to collect the photos. She was told the price was €10.99. She referred to the ‘deal’ that she signed up for but the shop assistant told her that the deal was for 4’x 6’ photos only. Jenny contacted the National Consumer Agency, which had already received many similar complaints about the Funky Fotos offer.')
         + '\n(Advertisement: ' + L(2, 6, "TODAY'S DEAL Funky Fotos Photos printed immediately Special Offer 100 Photos Only €5.99") + ')')
add(2, 1, 'a', 'Q1(A)', fotos + '\n\n' + L(2, 6, '(A) Explain how Funky Fotos has broken the terms of the Consumer Protection Act 2007. (Refer to the text in your answer).'), 15, 'business-0-13',
    'funky-fotos-breaches', 6, [13], 'The terms broken with two references to Funky Fotos: 10 (7 + 3) and 5 (4 + 1).', ten_five('Breach'),
    [UNTIED10, 'Scheme examples: ' + S(13, 'It is illegal for a business to make false/misleading claims about prices:')])
add(2, 1, 'b', 'Q1(B)', fotos + '\n\n' + L(2, 6, '(B) Outline two courses of action the National Consumer Agency can take against Funky Fotos.'), 15, 'business-0-13', 'nca-courses-of-action',
    6, [13], TEN5, ten_five('Course of action'), [UNTIED10])
doctors = (L(2, 6, 'Junior Doctors Industrial Action') + '\n' + L(2, 6, 'In October 2013, junior doctors held a one-day strike action against the Health Service Executive (HSE) in relation to working hours and conditions. They were represented by their Trade Union, the Irish Medical Organisation (IMO), and they engaged in picketing outside public hospitals. Following the industrial action, the IMO and the HSE returned to the Labour Relations Commission (LRC).')
           + '\n(Trade Union and picketing are underlined.)')
add(2, 1, 'c', 'Q1(C)', doctors + '\n\n' + L(2, 6, '(C) List three reasons, other than working conditions, which may cause industrial relations disputes.'), 15, 'business-0-14',
    'dispute-reasons-listed', 6, [14], 'Three reasons: 10, 3 and 2.', unequal('Reason', [(10,), (3,), (2,)], None),
    ['The 10/3/2 sequence prices the three reasons, not particular reasons. Scheme examples: ' + bullets(S(14, '• Pay rates • New work practices')) + '; pensions, dismissal, redundancies.'])
add(2, 1, 'd', 'Q1(D)', doctors + '\n\n' + L(2, 6, '(D) Explain the terms underlined above.'), 15, 'business-0-14', 'trade-union-and-picketing',
    6, [14], 'Trade Union 8 (6 + 2) and picketing 7 (5 + 2).', [comps('Trade Union', (6, 2), i=1), comps('Picketing', (5, 2), i=2)],
    ['Scheme: ' + S(14, 'A Trade Union is an organisation that represents workers (employees) in their dealings with employers.') + ' '
     + S(14, 'Picketing involves workers engaged in industrial action (strike) who assemble outside employer’s premises with placards giving information about their dispute.')])
add(2, 1, 'e', 'Q1(E)', doctors + '\n\n' + L(2, 6, '(E) Explain two functions of the Labour Relations Commission (LRC).'), 15, 'business-0-14', 'lrc-functions',
    6, [14], 'Two functions: 12 (10 + 2) and 3 (2 + 1).', unequal('Function', [(10, 2), (2, 1)], None), ['The 12-mark allowance is not tied to a particular function.'])

glanbia = L(2, 7, 'Glanbia plc, one of Ireland’s top agri-businesses, produces food products for the Irish and international markets. It is based in Kilkenny, employs over 3,500 people in 14 countries, and had an annual turnover of €2.9 billion in 2012.')
sec_i = L(2, 7, '(A) (i) Glanbia plc operates in the secondary sector of the economy. Explain what is meant by the ‘secondary sector’.')
add(2, 2, 'ai', 'Q2(A)(i)', glanbia + '\n\n' + sec_i, 10, 'business-5-13', 'secondary-sector-explained-2014', 7, [15], 'Explanation: 10 marks (5 + 5).',
    [comps('Secondary sector', (5, 5))], ['Scheme: ' + S(15, 'The secondary sector includes the manufacturing and construction industries.')])
cum(2, 2, 'aii', 'Q2(A)(ii)', glanbia + '\n\n' + sec_i + '\n' + L(2, 7, '(ii) Name the two other sectors of the economy.'), (3, 2), 'business-5-13', 'two-other-sectors-named',
    7, [15], 'Answer key (scheme page 15): ' + S(15, 'Primary Sector (Extractive Industry) Tertiary Sector (Services)') + '.', noun='sectors')
add(2, 2, 'b', 'Q2(B)', glanbia + '\n\n' + L(2, 7, '(B) Explain two benefits to the people of Kilkenny and the wider community, of Glanbia plc being located there.'), 15, 'business-5-16',
    'glanbia-local-benefits', 7, [15], EIGHT, eight_seven('Benefit'), [UNTIED])
add(2, 2, 'c', 'Q2(C)', glanbia + '\n\n' + L(2, 7, '(C) Outline two benefits to Glanbia plc of being located in 14 different countries.'), 15, 'business-6-15', 'glanbia-fourteen-countries',
    7, [15], 'Two benefits: 8 and 7.', unequal('Benefit', [(8,), (7,)], None), [UNTIED])
add(2, 2, 'd', 'Q2(D)', glanbia + '\n\n' + L(2, 7, '(D) Glanbia is a Public Limited Company (plc). Explain two benefits of operating as a plc.'), 15, 'business-5-14', 'plc-benefits-2014',
    7, [15], EIGHT, eight_seven('Benefit'), [UNTIED])
add(2, 2, 'e', 'Q2(E)', glanbia + '\n\n' + L(2, 7, '(E) Outline two challenges that the agri-business sector in Ireland may face.'), 15, 'business-5-13', 'agri-business-challenges',
    7, [16], 'Two challenges: 10 (5 + 5) and 5 (3 + 2).', unequal('Challenge', [(5, 5), (3, 2)], None), [UNTIED10])

hospitality = L(2, 7, 'Employment levels in the hospitality sector in Ireland: 2005: 135,000 2007: 133,000 2009: 130,000 2011: 115,000 2013: 130,000')
vat = L(2, 7, 'The 2014 Budget retained the reduced 9% Value Added Tax (VAT) rate in the hospitality/tourism sector.')
q3 = hospitality + '\n' + vat
flat(add(2, 3, 'a', 'Q3(A)', q3 + '\n\n' + L(2, 7, '(A) Construct a Line Graph to represent the above employment levels in the hospitality sector in Ireland. (You may use graph paper)'), 15,
         'business-2-12', 'hospitality-line-graph', 7, [17], 'Heading 3, the two labels 1 each and five points at 2 each.',
         [fixed('Line graph', [('Title/heading', 3), ('Year label', 1), ('Number employed label', 1), ('2005: 135,000', 2), ('2007: 133,000', 2), ('2009: 130,000', 2),
                               ('2011: 115,000', 2), ('2013: 130,000', 2)])],
         ['Scheme (page 17): ' + S(17, 'Heading 3 Labels: Year 1 No.empl 1 Correct Points: 5 x 2m') + ' ' + S(17, '[Does not have to be scaled from ‘0’]')]))
add(2, 3, 'b', 'Q3(B)', q3 + '\n\n' + L(2, 7, '(B) Outline two benefits to the tourism/hospitality sector of the reduced 9% VAT rate.'), 15, 'business-5-15', 'reduced-vat-benefits',
    7, [17], EIGHT, eight_seven('Benefit'), [UNTIED], extra=['business-3-18'])
add(2, 3, 'c', 'Q3(C)', q3 + '\n\n' + L(2, 7, '(C) Outline two other ways the Government assists businesses in Ireland.'), 20, 'business-5-15', 'government-assists-business',
    7, [17], 'Two ways at 10 marks each (5 + 5).', points('Way', 2, (5, 5)))
cum(2, 3, 'd', 'Q3(D)', q3 + '\n\n' + L(2, 7, '(D) Name three taxes, other than VAT, which the Government collects.'), (5, 5, 5), 'business-3-18', 'taxes-other-than-vat',
    7, [18], 'Scheme examples (page 18): ' + bullets(S(18, '• Corporation Tax • PAYE (Income Tax) • Capital Gains Tax • Capital Acquisitions Tax • DIRT')) + '.', noun='taxes')
add(2, 3, 'e', 'Q3(E)', q3 + '\n\n' + L(2, 7, '(E) Explain the term ‘privatisation of a state-owned enterprise’.'), 10, 'business-5-14', 'privatisation-explained-2014',
    7, [18], 'Explanation: 10 marks (5 + 5).', [comps('Privatisation', (5, 5))],
    ['Scheme: ' + S(18, 'Privatisation involves the Government selling off state-owned enterprise to privately owned firms.')])

jordan = L(2, 8, 'West Coast Surf') + '\n' + L(2, 8, 'In 2013, Jordan Casey was made redundant from his job at a factory in Sligo town. He received a redundancy package and decided he would like to set up his own business in the seaside town of Castlemore. Jordan has enjoyed surfing as a hobby since he was in school. He realised that surfing was becoming a very popular sport and spotted a gap in the market to provide surfing lessons at his local beach. He carried out a SWOT analysis of the potential business idea. Jordan was aware of his limitations. He approached the County Enterprise Board, who provided a mentoring service to him.')
add(2, 4, 'a', 'Q4(A)', jordan + '\n\n' + L(2, 8, '(A) Outline three enterprising skills/characteristics displayed by Jordan. (Refer to the text in your answer).'), 15, 'business-1-5',
    'jordan-enterprising-skills', 8, [19], 'Three at 5 marks each (3 + 2).', points('Characteristic', 3, (3, 2)))
add(2, 4, 'b', 'Q4(B)', jordan + '\n\n' + L(2, 8, '(B) Jordan turned his hobby into a business opportunity. Outline two other sources of new business ideas.'), 15, 'business-4-14',
    'other-idea-sources-2014', 8, [19], TEN5, ten_five('Source'), [UNTIED10])
add(2, 4, 'c', 'Q4(C)', jordan + '\n\n' + L(2, 8, '(C) Explain two long-term sources of finance Jordan could use to set up his business.'), 15, 'business-3-16', 'jordan-long-term-finance',
    8, [20], TEN5, ten_five('Source'), [UNTIED10])
swot = add(2, 4, 'd', 'Q4(D)', jordan + '\n\n' + L(2, 8, '(D) Explain why Jordan should carry out a SWOT analysis.'), 15, 'business-2-13', 'why-swot-analysis',
           8, [20], 'The four SWOT terms at 3 each and one explanation 3.',
           seq(comps('SWOT terms', (12,), ['Strengths, Weaknesses, Opportunities and Threats']), comps('Explanation', (3,))),
           ['Scheme: ' + S(20, '15m 4 x 3m + 1 expl. @ 3m') + '. Example: ' + S(20, 'Jordan’s strength is his knowledge of and skills in surfing.')])
permit(swot, 0, [0, 3, 6, 9, 12])
add(2, 4, 'e', 'Q4(E)', jordan + '\n\n' + L(2, 8, '(E) Outline how the mentoring service provided by the County Enterprise Board works.'), 15, 'business-5-16', 'ceb-mentoring',
    8, [20], 'One outline: 15 marks (12 + 3).', [comps('Mentoring service', (12, 3))],
    ['Scheme: ' + S(20, 'An experienced businessperson acts as an advisor to a new business / entrepreneur during the start-up period.')], extra=['business-1-5'])

besto = L(2, 8, 'BestoPesto') + '\n' + L(2, 8, 'Maria Conlon is the manager of BestoPesto, a manufacturer of cooking sauces. BestoPesto produce sauces in five different flavours. Recently there has been an increase in consumer complaints about the products. Maria realises that her business needs to improve its quality control measures. Maria sent a memo to the staff informing them of a staff meeting to be held on Friday 27th June 2014 at 9.00am in the conference room to discuss quality control issues.')
add(2, 5, 'a', 'Q5(A)', besto + '\n\n' + L(2, 8, '(A) Explain two types of leadership styles.'), 15, 'business-2-11', 'two-leadership-styles',
    8, [21], 'Each style named 2 and explained: 6 (3 + 3) and 5 (3 + 2).', unequal('Leadership style', [(2, 3, 3), (2, 3, 2)], ['Named', 'Explained', 'Explanation developed']),
    ['The 6-mark explanation is not tied to a particular style.'])
add(2, 5, 'b', 'Q5(B)', besto + '\n\n' + L(2, 8, '(B) Explain why BestoPesto would use batch production methods for its sauces.'), 15, 'business-4-15', 'why-batch-production',
    8, [21], 'One explanation: 15 marks (8 + 7).', [comps('Batch production', (8, 7))],
    ['Scheme: ' + S(21, 'Producing a certain/limited amount/quantity of identical products at the same time or in one production run.')])
qc_i = L(2, 8, '(C) (i) Explain the term ‘Quality Control’.')
add(2, 5, 'ci', 'Q5(C)(i)', besto + '\n\n' + qc_i, 10, 'business-2-13', 'quality-control-explained', 8, [22], 'Explanation: 10 marks (5 + 5).', [comps('Quality control', (5, 5))],
    ['Scheme: ' + S(22, 'Quality Control is checking that the methods of production are the most efficient to ensure that the finished product consistently meets the standards set by law and required by customers.')])
add(2, 5, 'cii', 'Q5(C)(ii)', besto + '\n\n' + qc_i + '\n' + L(2, 8, '(ii) Outline one method that BestoPesto could use to improve quality control.'), 10, 'business-2-13',
    'quality-control-method', 8, [22], 'One method: 10 marks (5 + 5).', [comps('Method', (5, 5))],
    ['Scheme examples: ' + S(22, 'BestoPesto could appoint a Quality Controller to oversee all aspects of production')])
flat(add(2, 5, 'd', 'Q5(D)', besto + '\n\n' + L(2, 8, '(D) Using today’s date, draft the memo sent by Maria Conlon to the staff informing them of the upcoming staff meeting.'), 10,
         'business-2-12', 'besto-pesto-memo', 8, [22], 'Ten entries at 1 mark each: to, from, date, re, the meeting, its date, time and venue, signature and title.',
         [fixed('Memo', [('To', 1), ('From', 1), ('Date', 1), ('Re', 1), ('Meeting purpose', 1), ('Meeting date', 1), ('Meeting time', 1), ('Venue', 1), ('Signed', 1), ('Title', 1)])],
         ['Scheme (page 22): To ' + S(22, 'All Staff (1)') + '; From Maria Conlon, Manager; Re Staff Meeting; ' + S(22, 'will be held on Friday, 27th June 2014 (1) starting at 9.00 a.m. (1) in the conference room (1)')
          + '; Signed Maria Conlon; Title Manager (' + S(22, '10m (10 x 1m)') + ').']))
add(2, 5, 'e', 'Q5(E)', besto + '\n\n' + L(2, 8, '(E) Outline two advantages of meetings as a method of communication.'), 15, 'business-2-12', 'meetings-advantages-2014',
    8, [22], EIGHT, eight_seven('Advantage'), [UNTIED])

smart = (L(2, 9, 'SMARTSELL') + '\n' + L(2, 9, 'Smartsell is a technology enterprise providing software to retail stores. It is currently operating in the Irish market but sees an opportunity to expand into the UK market. It will require a number of new skilled employees to help develop its business in the UK market. The HR Manager is preparing a Job Description and a Person Specification for each position. All new employees will receive ‘on the job’ training and ‘off the job’ training when they join the business. Employees are rewarded by bonuses and they receive benefits-in-kind.')
         + '\n(Job Description, Person Specification, bonuses and benefits-in-kind are underlined.)')
add(2, 6, 'a', 'Q6(A)', smart + '\n\n' + L(2, 9, '(A) Outline two reasons for business expansion.'), 15, 'business-4-18', 'expansion-reasons-2014', 9, [23], EIGHT, eight_seven('Reason'), [UNTIED])
add(2, 6, 'b', 'Q6(B)', smart + '\n\n' + L(2, 9, '(B) Explain the four underlined terms.'), 20, 'business-3-20', 'four-underlined-hr-terms', 9, [23], 'Each term 5 marks (3 + 2).',
    [comps('Job Description', (3, 2), i=1), comps('Person Specification', (3, 2), i=2), comps('Bonuses', (3, 2), i=3), comps('Benefits-in-kind', (3, 2), i=4)],
    ['Scheme: ' + S(23, 'This describes the qualities that the successful candidate for the job should have.') + ' Bonuses: ' + S(23, 'Extra payments made to employees to reward them for reaching/achieving a specific target.')],
    extra=['business-3-18'])
add(2, 6, 'c', 'Q6(C)', smart + '\n\n' + L(2, 9, '(C) Explain the difference between ‘on the job’ training and ‘off the job’ training. (Refer to Smartsell in your answer).'), 10, 'business-3-20',
    'on-off-job-training-smartsell', 9, [24], 'Each type 5 marks (3 + 2).', [comps('On the job training', (3, 2), i=1), comps('Off the job training', (3, 2), i=2)])
cum(2, 6, 'd', 'Q6(D)', smart + '\n\n' + L(2, 9, '(D) List two methods of advertising the job vacancies.'), (5, 5), 'business-3-20', 'advertising-vacancies-2014',
    9, [24], 'Scheme examples (page 24): ' + bullets(S(24, '• National/local newspapers • Local radio • Online – Company website/Facebook/Twitter • Recruitment/employment agency')) + '.', noun='methods')
niall = L(2, 9, 'Niall will earn €60,000 Gross Pay per year. He pays PAYE at 20 % on the first €32,800 and 41% on the remainder. He has annual tax credits of €3,600. He pays PRSI at 4% and USC at 3%, both calculated on his gross pay.')
flat(add(2, 6, 'e', 'Q6(E)', L(2, 9, '(E) Niall Ryan was successful in his application to work as a Software Engineer at Smartsell. Calculate his Net Annual Take-home pay from the following information:') + '\n' + niall, 20,
         'business-3-18', 'niall-net-take-home-pay', 9, [24], 'Gross pay 2 and six figures at 3 each (workings must show).',
         [response(1, 'Net annual take-home pay', [('gross', 'Gross Pay €60,000', 2), ('paye-20', '20% of €32,800 = €6,560', 3), ('paye-41', '41% of €27,200 = €11,152', 3),
                                                   ('credit', 'Less Tax Credit €3,600', 3), ('prsi', 'PRSI 4% of €60,000 = €2,400', 3), ('usc', 'USC 3% of €60,000 = €1,800', 3),
                                                   ('net', 'Net Annual Take-home pay €41,688', 3)])],
         ['Scheme (page 24): ' + S(24, 'Net PAYE Payable = €14,112') + '; ' + S(24, 'Total Deductions: €18,312 Net Annual Take-home pay: €41,688 (3)') + '; ' + S(24, '20m 1 x 2m 6 x 3m Note: Must show workings') + '.']))

sanders = L(2, 10, 'Sanders Household') + '\n' + L(2, 10, 'Linda and Paul Sanders live in their own home with their two children. Linda works as an Office Manager in a large printing company. Paul is a Sales Representative for a furniture store. Linda prepares a household budget every year and must include the purchase of a second car in the expenditure section this year. The Sanders’ family are considering taking out a medium term bank loan to purchase the car. They currently have an overdraft facility on their current account.')
add(2, 7, 'a', 'Q7(A)', sanders + '\n\n' + L(2, 10, '(A) Outline two types of insurance the Sanders household might have.'), 15, 'business-3-17', 'household-insurance-types', 10, [25], EIGHT, eight_seven('Type'), [UNTIED])
add(2, 7, 'b', 'Q7(B)', sanders + '\n\n' + L(2, 10, '(B) Outline two reasons why the Sanders household would prepare a Household Budget.'), 15, 'business-3-16', 'household-budget-reasons', 10, [25], EIGHT, eight_seven('Reason'), [UNTIED])
add(2, 7, 'c', 'Q7(C)', sanders + '\n\n' + L(2, 10, '(C) Outline two factors the Sanders household must consider before taking out a medium term bank loan.'), 15, 'business-3-16', 'medium-term-loan-factors',
    10, [25], EIGHT, eight_seven('Factor'), [UNTIED])
add(2, 7, 'd', 'Q7(D)', sanders + '\n\n' + L(2, 10, '(D) Explain three features of a Current Account.'), 15, 'business-3-16', 'current-account-features', 10, [26],
    'Three features: 6 (3 + 3), 6 (3 + 3) and 3 (2 + 1).', unequal('Feature', [(3, 3), (3, 3), (2, 1)], None), ['The 6/6/3 sequence prices the three features, not particular features.'])
add(2, 7, 'e', 'Q7(E)', sanders + '\n\n' + L(2, 10, '(E) Outline one similarity and one difference for Linda between managing her office and managing her home.'), 15, 'business-3-16',
    'office-and-home-management', 10, [26], 'Similarity 10 (5 + 5) and difference 5 (3 + 2).', [comps('Similarity', (5, 5), i=1), comps('Difference', (3, 2), i=2)])

madra = L(2, 11, 'Madra Mia') + '\n' + L(2, 11, 'Madra Mia, located in Cork city since 2000, provides a dog grooming service and products for animal care. Business was booming for the first few years but has experienced a decline in customers since the economic downturn. The business is currently in a break-even situation but Niamh Murphy, its owner, is considering offering new products and services to customers. She plans to conduct market research. She will use the information gathered to set prices and develop sales promotion techniques. She will update her business plan following her research.')
field_i = L(2, 11, '(A) (i) List two methods of field research which Niamh could use.')
cum(2, 8, 'ai', 'Q8(A)(i)', madra + '\n\n' + field_i, (5, 5), 'business-4-16', 'field-research-methods', 11, [27],
    'Scheme methods (page 27): ' + bullets(S(27, '• Survey/Questionnaire • Consumer panel • Interview • Observation')) + '.', noun='methods')
add(2, 8, 'aii', 'Q8(A)(ii)', madra + '\n\n' + field_i + '\n' + L(2, 11, '(ii) Explain one advantage of each method.'), 10, 'business-4-16', 'field-research-advantages',
    11, [27], 'One advantage of each method at 5 marks.', points('Advantage', 2, (5,)), ['The scheme notes: ' + S(27, '[Note: Distinct advantage for each. Advantages of each method may overlap.]')])
add(2, 8, 'b', 'Q8(B)', madra + '\n\n' + L(2, 11, '(B) Explain the term ‘break-even’.'), 10, 'business-3-19', 'break-even-explained', 11, [27], 'Explanation: 10 marks (7 + 3).',
    [comps('Break-even', (7, 3))], ['Scheme: ' + S(27, 'Break-even means a business takes in enough revenue/has enough sales to cover all its costs')])
add(2, 8, 'c', 'Q8(C)', madra + '\n\n' + L(2, 11, '(C) Outline two factors Niamh must consider before setting the price of her products and services.'), 15, 'business-4-17', 'niamh-pricing-factors',
    11, [27], TEN5, ten_five('Factor'), [UNTIED10])
add(2, 8, 'd', 'Q8(D)', madra + '\n\n' + L(2, 11, '(D) Describe two sales promotion methods to increase sales for Madra Mia.'), 15, 'business-4-17', 'madra-mia-sales-promotions',
    11, [28], TEN5, ten_five('Sales promotion'), [UNTIED10, 'The scheme notes: ' + S(28, '[Note: Only accept one type of any Sales Promotion]')])
add(2, 8, 'e', 'Q8(E)', madra + '\n\n' + L(2, 11, '(E) Outline two benefits of preparing a business plan.'), 15, 'business-4-15', 'business-plan-benefits-2014',
    11, [28], 'Two benefits: 12 and 3.', unequal('Benefit', [(12,), (3,)], None), ['The 12-mark allowance is not tied to a particular benefit.'])

# ---------------------------------------------------------------- checks and write-out
qn = lambda c: c['questionRef'].split(' Q')[1].split('(')[0]
for section, count, total in [('1', 15, 10), ('2', 8, 75)]:
    for q in range(1, count + 1):
        got = sum(c['totalMarks'] for c in P.created if c['section'] == section and qn(c) == str(q))
        assert got == total, (section, q, got)
assert not [i for i in ORIGINAL if i.startswith('bus-2014-ol-')]
assert not P.pools

SELECTION = {
    1: 'No finite printed answer menu occurs in Section 1 (answer ten of fifteen at 10 marks). CHAIRPERSON/SECRETARY in Q5, TRUE/FALSE in Q8, the surplus/deficit tick in Q9, the matching rows in Q10 and the ticks in Q13 are required answer formats. Support-note lists are open examples.',
    2: 'No printed choice of task occurs in Section 2: the underlined terms in Q1(D) and Q6(B) are all required. Sub-parts with their own published marks are separate cards. Support-note lists are open examples.',
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
    if m == 'or' and own(w, m, 'CHAIRPERSON or SECRETARY'):
        return 'required-headings', 'CHAIRPERSON/SECRETARY are answer labels for each of the five required functions in Section 1 Q5, not optional tasks.', None
    if m == 'or' and own(w, m, 'TRUE or FALSE'):
        return 'required-headings', 'TRUE/FALSE are answer labels for each of the five required statements in Section 1 Q8, not optional tasks.', None
    if m == 'or' and own(w, m, 'surplus or a deficit'):
        return 'required-headings', 'Section 1 Q9(ii) requires a determination of surplus or deficit; it is one required answer, not a choice of task.', None
    if m == 'one of' and (own(w, m, 'is one of the world') or own(w, m, 'one of Ireland’s top')):
        return 'case-context', '“one of” here is wording inside a printed statement (Section 1 Q2, Section 2 Q2), not a choice of task.', None
    assert (fileid, page) in {('LC033GLP000EV', 1), ('LC033GLP000EV', 6)} and m in ('either', 'or'), (fileid, page, m, w)
    return 'exam-navigation', 'The cover and Section 2 rubrics set how many whole questions a candidate answers (one from Part 1, two from Part 2 and one other from either part). Every numbered question remains in the practice corpus as separate cards.', None


n = P.write([(1, range(1, 16)), (2, range(1, 9))], SELECTION, classify,
            'Every part of {year} Ordinary Section {section} Question {q} was visually checked against its SEC paper, allocation summary and expected responses. The single-booklet identity keeps the short (n) and long (S2Q) question numbering apart.')
print(f'Reviewed {len(P.created)} 2014 Ordinary tasks; classified {n} raw selection matches.')
