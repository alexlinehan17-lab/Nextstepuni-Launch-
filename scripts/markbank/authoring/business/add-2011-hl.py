"""Review the 2011 Higher English paper outside its ABQ (Sections 1 and 3).

2011 Higher: answer eight of ten short questions at 10 marks (Section 1),
the compulsory Applied Business Question (Section 2, carded by
add-2011-abq.py and left untouched here) and four of seven long questions
at 60 (Section 3), all in one twelve-page booklet (LC033ALP000EV, the same
file id as its scheme). No card existed for Sections 1 and 3, so every card
is new. The allocation summary (scheme pages 5 and 7-12) sets each
boundary; printed sub-parts with their own published marks are separate
cards. One exception: Section 1 Q5(b) prints "calculate (i) Balance of
Trade, (ii) Balance of Payments" in one sentence over one answer box, so it
is one card whose two response groups carry the summary's 3 and 3. No
printed choice of task occurs.
"""
from bus_lib import (Paper, ORIGINAL, comps, points, seq, unequal, single, response, fixed, permit)

T = {(1, q): 5 for q in range(1, 11)}
T.update({(3, 1): 7, (3, 2): 7, (3, 3): 8, (3, 4): 9, (3, 5): 10, (3, 6): 11, (3, 7): 12})
P = Paper(2011, 'higher', {1: 'LC033ALP000EV', 3: 'LC033ALP000EV'}, 'LC033ALP000EV', T)
L, S, add, cum = P.lift, P.scheme, P.add, P.cumulative


def flat(card):
    for r in card['rubric']['responses']:
        for a in r['allocations']:
            a['permittedMarks'] = [0, a['maxMarks']]
    return card


# ---------------------------------------------------------------- Section 1 (10 marks each)
own_a = L(1, 2, '(a) Explain the meaning of the term ‘Own - brand products’.')
add(1, 1, 'a', 'Q1(a)', own_a, 4, 'business-4-17', 'own-brand-products', 2, [13], 'Explanation: 4 marks (2 + 2).', [comps('Own-brand products', (2, 2))],
    ['Scheme: ' + S(13, 'These are products sold by retailers/multiples under the retailer’s own name and logo.')])
add(1, 1, 'b', 'Q1(b)', own_a + '\n' + L(1, 2, '(b) Outline two reasons why retailers use ‘Own - brand products’:'), 6, 'business-4-17', 'own-brand-reasons',
    2, [13], 'Two reasons at 3 marks each (1 + 2).', points('Reason', 2, (1, 2)),
    ['Scheme examples: ' + S(13, 'The retailer can generally sell ‘own- brands’ at a cheaper price than the market leader and other brands/ ‘value for money’.') + ' '
     + S(13, 'Easily recognised and require very little advertising.')])
roi_a = L(1, 2, '(a) Explain the term ‘Return on Investment’ (ROI).')
add(1, 2, 'a', 'Q2(a)', roi_a, 4, 'business-3-19', 'roi-explained-2011', 2, [13], 'Explanation: 4 marks (2 + 2).', [comps('Return on Investment', (2, 2))],
    ['Scheme: ' + S(13, 'ROI is the net profit a business generates from the total finance used by the business (capital employed).')])
flat(add(1, 2, 'b', 'Q2(b)', roi_a + '\n' + L(1, 2, '(b) Using the figures below calculate the ROI for ‘Natural Options Ltd.’. (Show your workings.)')
         + '\nNet Profit € 57,000\nOrdinary Share Capital € 140,000\nReserves € 56,000\nLong Term Loan € 24,000\nWorkings:\nAnswer:', 6, 'business-3-19', 'roi-natural-options',
         2, [14], 'Formula 1, the four figures at 1 each and the answer 1 (it must include %).',
         [response(1, 'Return on Investment', [('formula', 'Formula: Net Profit x 100 / Capital Employed', 1), ('net-profit', '€57,000', 1), ('shares', '€140,000', 1),
                                               ('reserves', '€56,000', 1), ('loan', '€24,000', 1), ('answer', 'Answer: 25.91% or 26%', 1)])],
         ['The allocation summary prints “' + S(5, '(b) 6 marks (6 @ 1 mark) 1 for formula. 4 figures @1 mark. 1 mark for correct answer (must include %)') + '”.',
          'Scheme (page 14): Net Profit x 100 over Capital Employed, €57,000 over ' + S(14, '€140,000 + €56,000 + €24,000') + ' ' + S(14, '= 25.91% or 26%') + '.']))
L(1, 2, 'Net Profit € 57,000 Ordinary Share Capital € 140,000 Reserves € 56,000 Long Term Loan € 24,000')
meet_a = L(1, 2, '(a) Distinguish between two types of meetings which are common in a business.')
add(1, 3, 'a', 'Q3(a)', meet_a, 4, 'business-2-12', 'meeting-types-2011', 2, [14], 'Two types distinguished: 4 marks (2 + 2).', [comps('Types of meeting', (2, 2))],
    ['Scheme examples: ' + S(14, 'AGM (Annual General Meeting). This is a meeting of the shareholders of a company.') + ' '
     + S(14, 'EGM (Extraordinary General Meeting).')])
add(1, 3, 'b', 'Q3(b)', meet_a + '\n' + L(1, 2, '(b) Outline two benefits of meetings as a method of communication.'), 6, 'business-2-12', 'meeting-benefits-2011',
    2, [14], 'Two benefits at 3 marks each (1 + 2).', points('Benefit', 2, (1, 2)),
    ['Scheme examples: ' + S(14, 'Meeting allow for feedback to be given and received.') + ' ' + S(14, 'A written record (i.e. minutes) of decisions can be made for future reference.')])
span_a = L(1, 3, '(a) Explain the term ‘span of control’.')
add(1, 4, 'a', 'Q4(a)', span_a, 6, 'business-2-13', 'span-of-control-2011', 3, [15], 'Explanation: 6 marks (3 + 3).', [comps('Span of control', (3, 3))],
    ['Scheme: ' + S(15, 'It refers to the number of people / subordinates that report directly to one manager/ supervisor in a hierarchy.')])
add(1, 4, 'b', 'Q4(b)', span_a + '\n' + L(1, 3, '(b) Outline two factors that affect the width of the span of control in a business:'), 4, 'business-2-13', 'span-of-control-factors',
    3, [15], 'Two factors at 2 marks each.', points('Factor', 2, (2,)),
    ['Scheme examples: ' + S(15, 'Skill of manager/management style:') + ' ' + S(15, 'Skill of the workforce:') + ' ' + S(15, 'The nature of the work/type of product or service:')])
inv_a = L(1, 3, '(a) Illustrate what is meant by the term ‘invisible imports’, with reference to the Irish economy.')
add(1, 5, 'a', 'Q5(a)', inv_a, 4, 'business-6-13', 'invisible-imports-2011', 3, [15], 'Illustration: 4 marks (2 + 2).', [comps('Invisible imports', (2, 2))],
    ['Scheme: ' + S(15, 'Invisible imports are foreign services purchased by Irish customers/residents. e.g. financial services provided by foreign firms/ Irish residents holidaying abroad.')])
flat(add(1, 5, 'b', 'Q5(b)', inv_a + '\n' + L(1, 3, '(b) Using the following data, calculate (i) Balance of Trade, (ii) Balance of Payments. State in each case whether it is a surplus or deficit. (Show your workings.)')
         + '\nVisible Exports €50bn | Invisible Imports €40bn\nVisible Imports €30bn | Invisible Exports €35bn\nANSWER BOX: (i) Balance of Trade € | Surplus OR Deficit\n(ii) Balance of Payments € | Surplus OR Deficit',
         6, 'business-6-13', 'bot-and-bop-2011', 3, [15], 'Balance of Trade: three figures at 1 each; Balance of Payments: three figures at 1 each. The third mark in each needs the surplus stated.',
         seq(fixed('Balance of Trade', [('Figure: €50bn - €30bn', 1), ('Figure: €20bn', 1), ('Surplus stated', 1)]),
             fixed('Balance of Payments', [('Figure: €20bn + (€5bn) or €85bn - €70bn', 1), ('Figure: €15bn', 1), ('Surplus stated', 1)])),
         ['The paper prints (i) and (ii) inside one sentence over one answer box, so this is one card; the summary’s two sub-totals are its two response groups: “'
          + S(5, 'BOT 3 figures @ 1 mark To get the third mark you must state surplus. BOP 3 figures @ 1 mark To get the third mark you must state surplus.') + '”',
          'Scheme (page 15): ' + S(15, 'Balance of Trade = Visible Exports - Visible Imports = €50bn - €30bn = €20bn surplus') + '; '
          + S(15, 'Balance of Payments = Balance of Trade + Balance of Invisible Trade = €20bn + (€5bn) = €15bn surplus') + '.']))
L(1, 3, 'Visible Exports €50bn Invisible Imports €40bn Visible Imports €30bn Invisible Exports €35bn')
L(1, 3, 'ANSWER BOX Surplus OR Deficit (i)Balance of Trade € (ii)Balance of Payments €')
add(1, 6, '', 'Q6', L(1, 3, 'Outline two ways the Government could encourage business activity in Ireland.'), 10, 'business-5-15', 'government-encourages-business-2011',
    3, [16], 'Two ways at 5 marks each (3 + 2).', points('Way', 2, (3, 2)),
    ['Scheme examples: ' + S(16, 'Improved infrastructure such as roads, airports, ports, telecommunications and broadband allow business to operate efficiently and encourages business activity and job creation.')])
add(1, 7, '', 'Q7', L(1, 4, 'Outline two types of industrial action that employees could take in an attempt to get employers to meet their demands.'), 10, 'business-0-14',
    'industrial-action-types-2011', 4, [16], 'Two types at 5 marks each (3 + 2).', points('Type of industrial action', 2, (3, 2)),
    ['Scheme examples: ' + S(16, 'Work to rule where employees only undertake the exact jobs written in their job description/contract.') + ' ' + S(16, 'Overtime ban where workers refuse to do overtime.')])
cum(1, 8, '', 'Q8', L(1, 4, 'Write True or False after each of these sentences.',
                      '1. The role of the IDA is to attract foreign direct investment into Ireland.',
                      '2. Privatisation is the transfer of ownership from the private sector to the government owned public sector.',
                      '3. A code of ethics is a set of moral rules clarifying expected behavior of individuals in business.',
                      '4. An environmentally conscious business uses clean production processes and packaging which can be recycled.',
                      '5. An increase in the value of the euro € against the US dollar $ is good for Irish exporters to the US.'),
    (2, 2, 2, 2, 2), 'business-5-15', 'true-false-2011-hl', 4, [16], 'Answer key (scheme page 16): 1 True; 2 False; 3 True; 4 True; 5 False.',
    extra=['business-5-14', 'business-5-17', 'business-6-13'])
S(16, '1. 2. 3. 4. 5. True False True True False')
fin_a = L(1, 4, '(a) Explain the term ‘Short-term finance’.')
add(1, 9, 'a', 'Q9(a)', fin_a, 4, 'business-3-16', 'short-term-finance-2011', 4, [17], 'Explanation: 4 marks.', [comps('Short-term finance', (4,))],
    ['Scheme: ' + S(17, 'Short-term finance is finance that is available for a period of up to one year.')])
add(1, 9, 'b', 'Q9(b)', fin_a + '\n' + L(1, 4, '(b) Illustrate a business situation where ‘short-term finance’ would be appropriate.'), 6, 'business-3-16', 'short-term-finance-situation',
    4, [17], 'Illustration: 6 marks (3 + 3).', [comps('Business situation', (3, 3))], ['Scheme: ' + S(17, 'Trade credit could be used to purchase stock for resale.')])
add(1, 10, '', 'Q10', L(1, 4, 'Outline two strategies management could use to help employees adapt to change.'), 10, 'business-3-21', 'adapting-to-change-2011',
    4, [17], 'Two strategies at 5 marks each (3 + 2).', points('Strategy', 2, (3, 2)),
    ['Scheme examples: ' + S(17, 'Management needs to consult with the employees before introducing change so that employees will be more willing to accept the changes introduced')])

# ---------------------------------------------------------------- Section 3 (60 marks each)
people = L(3, 6, 'Business is primarily concerned with people and their interactions.')
add(3, 1, 'a', 'Q1(A)', people + '\n\n' + L(3, 6, '(A) Outline, using examples, the relationship that can exist between ‘Investors’ and ‘Entrepreneurs’ in business.'), 15, 'business-0-12',
    'investors-and-entrepreneurs', 6, [23], 'A co-operative or competitive relationship: 15 marks (3 + 6 + 6).', [comps('Relationship', (3, 6, 6))],
    ['The allocation summary prints “' + S(7, 'Co-operative OR Competitive relationship 15 marks (3+6+6)') + '”. Scheme: '
     + S(23, 'They rely on each other with the entrepreneur dependent on the investor for finance and the investor dependent on the entrepreneur for a return on his/her investment.')])
rights_i = L(3, 6, '(B) (i) Discuss the rights of consumers under the terms of the Sale of Goods and Supply of Services Act 1980.')
add(3, 1, 'b-i', 'Q1(B)(i)', people + '\n\n' + rights_i, 20, 'business-0-13', 'sogss-rights-2011', 6, [23, 24], 'Four rights at 5 marks each (2 + 3).', points('Right', 4, (2, 3)),
    ['Scheme examples: ' + S(23, 'Goods should be of merchantable quality – they should be of reasonable standard/quality taking into account what they are supposed to do, their durability and their price.') + ' '
     + S(24, 'Goods must be fit for the purpose intended.')])
add(3, 1, 'b-ii', 'Q1(B)(ii)', people + '\n\n' + rights_i + '\n' + L(3, 6, '(ii) Illustrate two forms of redress available to consumers for breach of the Act.'), 10, 'business-0-13',
    'sogss-redress-2011', 6, [24], 'Two forms of redress at 5 marks each (2 + 3).', points('Form of redress', 2, (2, 3)),
    ['Scheme: ' + S(24, 'If the complaint is valid the consumer is entitled to one of the three R’s – refund, replacement and repair.')])
add(3, 1, 'c', 'Q1(C)', people + '\n\n' + L(3, 6, '(C) Describe how conflict between an employer and an employee could be resolved in a non-legislative manner.'), 15, 'business-0-14',
    'non-legislative-resolution-2011', 6, [25], 'Three points at 5 marks each.', points('Point', 3, (5,)),
    ['Scheme examples: ' + S(25, 'Meet and talk.') + ' ' + S(25, 'Negotiation/agreement') + ' ' + S(25, 'Independent Third Party Intervention:')])

unemp = L(3, 6, 'The unemployment rate in the Irish Labour market increased from 4.3% in January 2005 to 14.7% in March 2011.')
add(3, 2, 'a', 'Q2(A)', unemp + '\n\n' + L(3, 6, '(A) Discuss the effects of increasing unemployment on the Irish economy.'), 20, 'business-5-15', 'unemployment-effects-2011-hl',
    6, [26], 'Four effects at 5 marks each (2 + 3).', points('Effect', 4, (2, 3)),
    ['Scheme examples: ' + S(26, 'The demand for goods and services is reduced and businesses may have to close down.') + ' '
     + S(26, 'Government current expenditure will increase as the unemployed will sign on and claim social welfare benefits.')])
add(3, 2, 'b', 'Q2(B)', unemp + '\n\n' + L(3, 6, '(B) Describe the steps involved in the formation of a ‘Private Limited Company’.'), 20, 'business-5-14', 'company-formation-steps-2011',
    6, [26, 27], 'Four steps at 5 marks each (2 + 3).', points('Step', 4, (2, 3)),
    ['Scheme examples: ' + S(26, 'The Memorandum of Association. This document sets out the relationship between the company and the general public.') + ' '
     + S(27, 'The Articles of Association. This document sets out the internal rules and regulations of the company.')])
cd_i = L(3, 6, '(C) (i) Explain the term ‘Community Development’.')
add(3, 2, 'c-i', 'Q2(C)(i)', unemp + '\n\n' + cd_i, 8, 'business-5-16', 'community-development-2011', 6, [27], 'Two points at 4 marks each (2 + 2).', points('Point', 2, (2, 2)),
    ['Scheme: ' + S(27, 'Community development refers to the development of local areas and local communities socially and economically through the efforts of local citizens and residents.')])
add(3, 2, 'c-ii', 'Q2(C)(ii)', unemp + '\n\n' + cd_i + '\n' + L(3, 6, '(ii) Evaluate the services provided by ‘County and City Enterprise Boards’ (CEBs).'), 12, 'business-5-16',
    'ceb-services-evaluated-2011', 6, [27, 28], 'Two services at 5 marks each (2 + 3) and an evaluation 2.', seq(points('Service', 2, (2, 3)), comps('Evaluation', (2,))),
    ['Scheme evaluation: ' + S(28, 'CEBs work well because they are uniquely positioned to understand local needs as they know the background and the track record of those applying for support and assistance.')])

exports = L(3, 7, 'A significant improvement in export performance is critical to the recovery of the Irish economy.')
add(3, 3, 'a', 'Q3(A)', exports + '\n\n' + L(3, 7, '(A) Discuss how the changing nature of the international economy affects Irish exporters.'), 20, 'business-6-13',
    'international-economy-and-exporters', 7, [28, 29], 'Four effects at 5 marks each (2 + 3).', points('Effect', 4, (2, 3)),
    ['Scheme examples: ' + S(28, 'Changes in technology have had a positive impact on Irish exporters making communications easier and instantaneous worldwide.') + ' '
     + S(29, 'Competition from new EU countries:')])
add(3, 3, 'b', 'Q3(B)', exports + '\n\n' + L(3, 7, '(B) Illustrate how foreign transnationals (i.e. foreign direct investment (FDI) companies) have impacted on the Irish Economy.'), 25, 'business-6-15',
    'transnational-impact-2011', 7, [29, 30], 'Five impacts at 5 marks each (1 + 2 + 2).', points('Impact', 5, (1, 2, 2)),
    ['Scheme examples: ' + S(29, 'Direct employment e.g. approximately 150,000 people are directly employed by foreign multinationals in Ireland.') + ' '
     + S(30, 'Repatriation of profits, which means wealth leaves the Irish economy.')])
add(3, 3, 'c', 'Q3(C)', exports + '\n\n' + L(3, 7, '(C) Evaluate the role of ‘special interest groups’ in the decision making process of the European Union (EU). Use examples to support your answer.'), 15,
    'business-6-14', 'eu-interest-groups-2011', 7, [30], 'Two points at 6 marks each (3 + 3) and an evaluation 3.', seq(points('Point', 2, (3, 3)), comps('Evaluation', (3,))),
    ['Scheme: ' + S(30, 'Special interest groups are groups which attempt to influence the political and decision-making process but are not part of the accepted political structures.') + ' Example: '
     + S(30, 'The IFA engaged in intense lobbying in Brussels to obtain greater flexibility on milk quotas in advance of their 2015 abolition.')])

colm = L(3, 8, '(A) Read the information supplied and answer the question which follows.') + '\n' + L(3, 8, 'Colm has decided to form a tidy towns committee in his local village and enter the ‘tidiest village’ category of the National Tidy Towns competition in 2013.')
add(3, 4, 'a', 'Q4(A)', colm + '\n\n' + L(3, 8, 'Discuss four entrepreneurial skills that Colm will require in developing this local community initiative.'), 20, 'business-1-5', 'colm-entrepreneurial-skills',
    8, [31], 'Four distinct skills at 5 marks each (2 + 2 + 1), each referred to the tidy towns initiative.', points('Skill', 4, (2, 2, 1)),
    ['The allocation summary prints “' + S(9, '(4 separate/distinct skills + ref. to tidy towns)') + '”. Scheme examples: ' + S(31, '1.Communication/feedback:') + ' ' + S(31, '2. Leadership/delegation/Human Relations')],
    extra=['business-5-16'])
maslow_i = L(3, 8, '(B) (i) Explain Maslow’s Theory of Motivation.')
add(3, 4, 'b-i', 'Q4(B)(i)', maslow_i, 10, 'business-2-11', 'maslow-theory-2011-hl', 8, [32], 'Explanation 5 (2 + 3) and the five needs at 1 each.',
    seq(comps('Theory explained', (2, 3)), fixed('The five needs', [('Need 1', 1), ('Need 2', 1), ('Need 3', 1), ('Need 4', 1), ('Need 5', 1)])),
    ['The allocation summary prints “' + S(9, '5 marks (2+3) 5 @ 1mark 5 @ 2marks') + '” across (i) and (ii).',
     'Scheme: ' + S(32, 'Maslow put forward a theory on motivation based on a hierarchy of needs.')])
add(3, 4, 'b-ii', 'Q4(B)(ii)', maslow_i + '\n' + L(3, 8, '(ii) Illustrate how a manager could motivate workers by applying Maslow’s Theory in the workplace.'), 10, 'business-2-11',
    'maslow-in-the-workplace-2011', 8, [32, 33], 'The five needs applied at 2 marks each.', points('Need applied', 5, (2,)),
    ['Scheme examples: ' + S(32, 'Physical Needs. A manager can motivate his workers by ensuring they receive a fair wage, bonuses, profit-sharing schemes') + '; '
     + S(33, 'Self-Actualisation Needs. Management offering workers a career plan, training and development opportunities, empowerment and promotion to positions of responsibility can meet these needs.')])
add(3, 4, 'c', 'Q4(C)', L(3, 8, '(C) Describe how ‘stock control’ and ‘quality control’ achieve efficiencies in business.'), 20, 'business-2-13', 'stock-and-quality-control-2011',
    8, [33], 'Each control 10 marks (2 + 4 + 4).', [comps('Stock control', (2, 4, 4), None, 1), comps('Quality control', (2, 4, 4), None, 2)],
    ['Scheme: ' + S(33, 'Is concerned with keeping optimum stock levels so that it doesn’t have too much stock or too little stock.') + ' '
     + S(33, 'Is concerned with checking/reviewing/inspecting work done to ensure it meets the required standards.')], extra=['business-3-21'])

add(3, 5, 'a', 'Q5(A)', L(3, 8, '(A) Outline the benefits of teamwork for the employees in a business.'), 15, 'business-3-20', 'teamwork-for-employees-2011',
    8, [34], 'Three benefits at 5 marks each (2 + 3).', points('Benefit', 3, (2, 3)),
    ['Scheme examples: ' + S(34, 'Employees experience greater job satisfaction as all members’ efforts are taken into account.')])
taxes = (L(3, 8, '(B) Pay As You Earn (PAYE), Value Added Tax (VAT), and Corporation Tax are examples of taxes relevant to a business.')
         + '\n(Pay As You Earn (PAYE), Value Added Tax (VAT) and Corporation Tax are underlined.)')
tax_i = L(3, 8, '(i) Explain each tax underlined above.')
add(3, 5, 'b-i', 'Q5(B)(i)', taxes + '\n' + tax_i, 18, 'business-3-18', 'paye-vat-corporation-tax', 8, [34, 35], 'Each tax 6 marks (3 + 3).',
    [comps('PAYE', (3, 3), None, 1), comps('VAT', (3, 3), None, 2), comps('Corporation Tax', (3, 3), None, 3)],
    ['Scheme: ' + S(34, 'PAYE is a direct tax on income earned from employment.') + ' ' + S(34, 'VAT is an indirect tax charged on the sale of goods and services.') + ' '
     + S(35, 'Corporation tax is a tax on the profits made by companies.')])
add(3, 5, 'b-ii', 'Q5(B)(ii)', taxes + '\n' + tax_i + '\n' + L(3, 8, '(ii) Evaluate the implications of each tax for a business.'), 7, 'business-3-18', 'tax-implications-2011',
    8, [34, 35], 'Implications for all three taxes: 7 marks (3 + 2 + 2).', unequal('Implication', [(3,), (2,), (2,)], None),
    ['The 3-mark allowance is not tied to a particular tax. Scheme example: ' + S(35, 'Corporation tax in Ireland is relatively low by international standards.')])
risk_i = L(3, 8, '(C) (i) Illustrate your understanding of the term ‘risk management’.')
add(3, 5, 'c-i', 'Q5(C)(i)', risk_i, 8, 'business-3-17', 'risk-management-2011', 8, [35], 'Illustration: 8 marks (4 + 4).', [comps('Risk management', (4, 4))],
    ['Scheme: ' + S(35, 'Risk Management is a planned approach to the handling of the risk that the individual or business is exposed to.')])
add(3, 5, 'c-ii', 'Q5(C)(ii)', risk_i + '\n' + L(3, 8, '(ii) Describe three methods a manager might consider to minimise risk within a business.'), 12, 'business-3-17', 'minimising-risk-2011',
    8, [35, 36], 'Three methods at 4 marks each (2 + 2).', points('Method', 3, (2, 2)),
    ['Scheme examples: ' + S(35, 'Insurance: Transfer the risk to an insurance company for a premium where the company will make good any loss suffered.')])

kilronan = L(3, 9, 'Kilronan Ltd produces a range of chilled food products. Made from natural ingredients, the firm’s award winning products have become household names. It is now one of the leading brands in Ireland and supplies all the major supermarket chains. Kilronan Ltd is considering either a ‘merger’ or a ‘takeover’ as a method of expansion within the Irish market. It is also considering how it will finance growth.')
mt_i = L(3, 9, '(A) (i) Illustrate the difference between a merger and a takeover as methods of business expansion.')
add(3, 6, 'a-i', 'Q6(A)(i)', kilronan + '\n\n' + mt_i, 10, 'business-4-18', 'merger-and-takeover-2011', 9, [36], 'Each method 5 marks (2 + 2 + 1), with an example of each.',
    [comps('Merger', (2, 2, 1), None, 1), comps('Takeover', (2, 2, 1), None, 2)],
    ['Scheme: ' + S(36, 'A merger is a friendly/voluntary amalgamation of two firms for their mutual benefit.') + ' '
     + S(36, 'A takeover on the other hand is where 51% of the shares in another company have been purchased in either a hostile or friendly manner.')])
add(3, 6, 'a-ii', 'Q6(A)(ii)', kilronan + '\n\n' + mt_i + '\n' + L(3, 9, '(ii) Discuss the benefits and risks of a merger as a method of expansion for Kilronan Ltd.'), 15, 'business-4-18',
    'merger-benefits-and-risks-2011', 9, [36, 37], 'Three points at 5 marks each (2 + 2 + 1), at least one benefit and one risk, referred to Kilronan Ltd.', points('Benefit or risk', 3, (2, 2, 1)),
    ['The allocation summary prints “' + S(11, 'At least one of each required. Must refer to Kilronan Ltd.') + '” Scheme example: '
     + S(37, 'Mergers can cause industrial relations problems.')])
add(3, 6, 'b', 'Q6(B)', kilronan + '\n\n' + L(3, 9, '(B) Distinguish between debt capital and equity capital as sources of finance for the expansion of Kilronan Ltd.'), 15, 'business-3-16',
    'debt-and-equity-2011', 9, [37], 'Three points of distinction at 5 marks each (2 + 3).', points('Point of distinction', 3, (2, 3)),
    ['Scheme headings: ' + S(37, 'Control') + '; ' + S(37, 'Interest Repayments/Dividends') + '; ' + S(37, 'Risk') + '.'])
add(3, 6, 'c', 'Q6(C)', kilronan + '\n\n' + L(3, 9, '(C) Outline internal and external sources of product innovation for Kilronan Ltd.'), 20, 'business-4-14', 'innovation-sources-2011',
    9, [38], 'Two internal and two external sources at 5 marks each (2 + 3).', seq(points('Internal source', 2, (2, 3)), points('External source', 2, (2, 3))),
    ['Scheme examples: ' + S(38, 'Ideas from employees through suggestion schemes/suggestion boxes.') + ' ' + S(38, 'Customer Complaints could result in changes/developments in products.')])

add(3, 7, 'a', 'Q7(A)', L(3, 10, '(A) Discuss two possible challenges associated with starting a new business.'), 10, 'business-4-15', 'start-up-challenges-2011',
    10, [39], 'Two challenges at 5 marks each (1 + 2 + 2).', points('Challenge', 2, (1, 2, 2)),
    ['Scheme examples: ' + S(39, 'Recruitment/Lack of expertise.') + ' ' + S(39, 'Production Method (Manufacturing Firm):')])
plc_i = L(3, 10, '(B) (i) Draw and label the ‘product life cycle’ diagram.')
flat(add(3, 7, 'b-i', 'Q7(B)(i)', plc_i, 10, 'business-4-17', 'product-life-cycle-2011-hl', 10, [39], 'Eight labels at 1 each and the curve 2.',
         [fixed('Diagram labels', [('Title', 1), ('Axis: Sales Volume', 1), ('Axis: Time', 1), ('Introduction', 1), ('Growth', 1), ('Maturity', 1), ('Saturation', 1), ('Decline', 1)]),
          comps('Curve', (2,), None, 2)],
         ['The allocation summary prints “' + S(12, '8@ 1 mark +2marks for curve') + '”. Scheme diagram (page 39): ' + S(39, 'The Product Life Cycle Sales Volume Introduction Growth Maturity Saturation Decline Time') + '.',
          'Scheme note: ' + S(39, 'Diagram requires title, axes correctly labelled and stages must be in correct order.')]))
add(3, 7, 'b-ii', 'Q7(B)(ii)', plc_i + '\n' + L(3, 10, '(ii) Illustrate the methods a business could use to extend a product’s life cycle.'), 15, 'business-4-17', 'extending-life-cycle-2011',
    10, [40], 'Three methods at 5 marks each (2 + 3).', points('Method', 3, (2, 3)),
    ['Scheme: ' + S(40, 'The business will have to change the marketing mix associated with the product in order to extend its life cycle.')])
moore = (L(3, 10, '(C) As part of its feasibility study for a new product, Moore Ltd supplies the following financial information:')
         + '\nForecast Output (Sales) | 40,000 units\nSelling Price per unit | €20\nFixed Costs | €300,000\nVariable Cost per unit | €10')
L(3, 10, 'Forecast Output (Sales) 40,000 units Selling Price per unit €20 Fixed Costs €300,000 Variable Cost per unit €10')
flat(add(3, 7, 'c-i', 'Q7(C)(i)', moore + '\n' + L(3, 10, '(i) Illustrate by means of a breakeven chart the following: (a) The Breakeven Point; (b) Profit at forecast output; (c) The Margin of Safety at forecast output.'),
         20, 'business-3-19', 'moore-breakeven-chart', 10, [41, 42], 'Chart: FC 2, TC 2, TR 2, BEP 3, forecast profit 3, margin of safety 3, both axis titles 2 each and a main heading 1.',
         [fixed('Break-even chart', [('Fixed Costs (FC) line', 2), ('Total Costs (TC) line', 2), ('Total Revenue (TR) line', 2), ('Break-even point: 30,000 units', 3),
                                     ('Profit at forecast output: €100,000', 3), ('Margin of safety: 10,000 units', 3), ('Axis title: Output in units ’000', 2),
                                     ('Axis title: Revenue and Costs €’000', 2), ('Main heading', 1)])],
         ['The allocation summary prints “' + S(12, 'Calculations only: (max 9 marks)') + '” for calculations without a chart.',
          'Scheme (page 41): ' + S(41, '(b) Profit at forecast output = €800,000 - €700,000 = €100,000 (c ) Margin of Safety = 40,000 - 30,000 = 10,000 Units') + '; break-even point 30,000 units.']))
S(41, '= 300,000 10 = 30,000 units')
add(3, 7, 'c-ii', 'Q7(C)(ii)', moore + '\n' + L(3, 10, '(ii) Outline one other function of a feasibility study for Moore Ltd.'), 5, 'business-4-14', 'feasibility-function-moore',
    10, [43], 'One function: 5 marks (2 + 3).', [comps('Function of a feasibility study', (2, 3))],
    ['Scheme examples: ' + S(43, 'Market feasibility i.e. is there a demand for the product/what is the best marketing mix for the product and what sales figures are likely to be?')])

# ---------------------------------------------------------------- checks and write-out
qn = lambda c: c['questionRef'].split(' Q')[1].split('(')[0]
for section, count, total in [('1', 10, 10), ('3', 7, 60)]:
    for q in range(1, count + 1):
        got = sum(c['totalMarks'] for c in P.created if c['section'] == section and qn(c) == str(q))
        assert got == total, (section, q, got)
assert not [i for i in ORIGINAL if i.startswith('bus-2011-hl-')]
assert not P.pools

SELECTION = {
    1: 'No finite printed answer menu occurs in Section 1 (answer eight of ten at 10 marks). True/False in Q8 and surplus/deficit in Q5(b) are required answer formats. Support-note lists are open examples.',
    3: 'No printed choice of task occurs in Section 3. Q5(B) underlines three taxes that are all required; Q6(A)(i) requires both a merger and a takeover. Sub-parts with their own published marks are separate cards. Support-note lists are open examples.',
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
    if m in ('or', 'OR') and (own(w, m, 'surplus or deficit') or own(w, m, 'Surplus OR Deficit')):
        return 'required-headings', 'Section 1 Q5(b) requires a surplus or deficit determination for each balance; it is a required answer label, not a choice of task.', None
    if m == 'or' and own(w, m, 'True or False'):
        return 'required-headings', 'True/False are answer labels for each of the five required sentences in Section 1 Q8, not optional tasks.', None
    if m == 'one of' and own(w, m, 'It is now one of the leading brands'):
        return 'case-context', '“one of the leading brands” is wording inside the Section 3 Q6 extract, not a choice of task.', None
    if m in ('either', 'or') and own(w, m, 'considering either a ‘merger’ or a ‘takeover’'):
        return 'case-context', 'The Section 3 Q6 extract states Kilronan’s options; Q6(A)(i) requires both a merger and a takeover, so this is not a choice of task.', None
    assert (fileid, page) in {('LC033ALP000EV', 1), ('LC033ALP000EV', 6)} and m in ('either', 'or'), (fileid, page, m, w)
    return 'exam-navigation', 'The cover and Section 3 rubrics set how many whole questions a candidate answers (one from Part 1, two from Part 2 and one other from either part). Every numbered question remains in the practice corpus as separate cards.', None


n = P.write([(1, range(1, 11)), (3, range(1, 8))], SELECTION, classify,
            'Every part of {year} Higher Section {section} Question {q} was visually checked against its SEC paper, allocation summary and support notes. The single-booklet identity keeps the short (n) and long (S3Q) question numbering apart.')
print(f'Reviewed {len(P.created)} 2011 Higher tasks; classified {n} raw selection matches.')
