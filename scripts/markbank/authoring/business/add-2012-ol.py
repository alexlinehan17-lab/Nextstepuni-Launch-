"""Review the 2012 Ordinary English paper (one booklet: Section 1 and Section 2).

2012: answer ten of fifteen short questions at 10 marks and four of eight
long questions at 75 (one from Part 1, two from Part 2 and one other), all in
one twelve-page booklet (LC033GLP000EV, the same file id as its scheme). No
Ordinary card existed for 2012, so every card is new. The allocation summary
(scheme pages 4-8) sets each boundary; printed sub-parts with their own
published marks are separate cards. Four printed choices are one card each
(the scheme marks every choice alike and files them under one topic):
Section 2 Q1(B) any three of four contract elements, Q5(B) any two of three
principles of insurance, Q5(E) term loan or leasing, and Q6(A) any two of
three HR functions.
"""
from bus_lib import (Paper, ORIGINAL, comps, points, seq, unequal, single, response, fixed, permit)

T = {(1, q): 4 for q in range(1, 16)}
T.update({(2, 1): 5, (2, 2): 5, (2, 3): 6, (2, 4): 6, (2, 5): 7, (2, 6): 7, (2, 7): 8, (2, 8): 8})
P = Paper(2012, 'ordinary', {1: 'LC033GLP000EV', 2: 'LC033GLP000EV'}, 'LC033GLP000EV', T)
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
add(1, 1, '', 'Q1', L(1, 2, 'What do the following letters stand for? (Write each answer in the space provided.)', 'VAT LRC ECB').replace(' LRC', '\nLRC').replace(' ECB', '\nECB'),
    10, 'business-3-18', 'abbreviations-vat-lrc-ecb', 2, [9], 'The first correct term earns 4 (2 + 1 + 1); the second and third 3 each (1 + 1 + 1).',
    [comps('First correct term', (4,), ['Words written in full'], 1), comps('Second correct term', (3,), ['Words written in full'], 2),
     comps('Third correct term', (3,), ['Words written in full'], 3)],
    ['Answer key: VAT ' + S(9, 'Value Added Tax') + '; LRC ' + S(9, 'Labour Relations Commission') + '; ECB ' + S(9, 'European Central Bank') + '.'],
    extra=['business-0-14', 'business-6-14'])
add(1, 2, '', 'Q2', L(1, 2, '(a) Explain the term ‘employer’.', '(b) Outline two responsibilities of an employer:'), 10, 'business-0-12', 'employer-and-responsibilities',
    2, [9], 'Explanation 4 and two responsibilities at 3 each.', seq(comps('Employer explained', (4,)), comps('Responsibility 1', (3,)), comps('Responsibility 2', (3,))),
    ['Scheme: ' + S(9, 'An employer is a person or business which hires employees/staff to produce goods or provide services and pays them agreed wages/salaries for their work.')
     + ' Responsibilities include ' + S(9, 'to provide a safe and healthy working environment') + '.'])
pie = L(1, 2, 'The following pie chart represents an extract of proposed Government expenditure.') + '\n(Pie chart: ' + L(1, 2, 'Health 13.65 Social Protection / Welfare 20.53 Education 8.6 Other 9.12 Government Expenditure (€ bn)') + ')'
add(1, 3, '', 'Q3', pie + '\n' + L(1, 2, '(i) List two examples of Government Expenditure on Health:') + '\nExample 1:\nExample 2:\n'
    + L(1, 2, '(ii) Outline two reasons for the high level of expenditure on Social Protection/Welfare:') + '\nReason 1:\nReason 2:', 10, 'business-5-15',
    'health-and-welfare-expenditure', 2, [9], '(i) Two examples at 3 each; (ii) two reasons at 2 each.',
    seq(points('Health example', 2, (3,)), points('Reason', 2, (2,))),
    ['Scheme examples: ' + bullets(S(9, '• Payment of wages/salaries to doctors/nurses/staff • Medical cards')) + '; reasons: ' + bullets(S(9, '• Increase in unemployment • Increase in birth rate – children’s allowances')) + '.'])
add(1, 4, '', 'Q4', L(1, 3, 'Outline two benefits of a good stock control system for a business:') + '\nBenefit 1:\nBenefit 2:', 10, 'business-2-13', 'stock-control-benefits-2012',
    3, [9], 'Two benefits at 5 marks each.', points('Benefit', 2, (5,)))
margins = add(1, 5, '', 'Q5', L(1, 3, 'The following information is available from the final accounts of Navona Ltd: Sales €420,000 Gross Profit €84,000 Net Profit €31,500').replace(' Sales', '\nSales').replace(' Gross Profit €', '\nGross Profit €').replace(' Net Profit', '\nNet Profit')
    + '\n' + L(1, 3, 'Calculate: (i) Gross Profit Margin Answer:') + ' %\n(ii) Net Profit Margin Answer: %', 10, 'business-3-19', 'profit-margins-navona',
    3, [10], 'Each margin 5 for the correct answer (up to 3 for workings if the answer is wrong).',
    [comps('Gross Profit Margin', (5,), ['Answer: 20%'], 1), comps('Net Profit Margin', (5,), ['Answer: 7.5%'], 2)],
    ['The allocation summary prints “' + S(4, '(i) 5 marks for correct answer (ii) 5 marks for correct answer (up to 3 marks for workings if incorrect)') + '”. Scheme answers: Gross Profit Margin 84,000 / 420,000 x 100 = 20%; Net Profit Margin 31,500 / 420,000 x 100 = 7.5% (page 10).'])
# 5 for the correct answer, otherwise up to 3 for workings: 4 is never awarded.
for r in margins['rubric']['responses']:
    r['allocations'][0]['permittedMarks'] = [0, 1, 2, 3, 5]
S(10, '= 20%')
S(10, '= 7.5%')
cum(1, 6, '', 'Q6', L(1, 3, 'Complete the missing Factors of Production.') + '\n______ | LABOUR | ______ | ENTERPRISE', (5, 5), 'business-1-5', 'missing-factors-2012', 3, [10],
    'Answer key (scheme page 10): Land and Capital (' + S(10, 'LAND LABOUR CAPITAL ENTERPRISE') + '; Labour and Enterprise are printed).', noun='factors')
L(1, 3, 'LABOUR ENTERPRISE')
add(1, 7, '', 'Q7', L(1, 3, 'Outline your understanding of a ‘Global Business’ and give one example.') + '\nExample:', 10, 'business-6-15', 'global-business-with-example',
    3, [10], 'Explanation 6 (3 + 3) and an example 4.', seq(comps('Global business', (3, 3)), single('Example', 4, 'Example named')),
    ['Scheme: ' + S(10, 'A Global Business sells a standardised product throughout the world using a standardised Marketing Mix.') + ' Examples: ' + S(10, 'Nike, Coca-Cola, Toyota, Apple etc.')])
cum(1, 8, '', 'Q8', L(1, 3, 'Write TRUE or FALSE after each of the following statements:', '1. The share of profits received by a Shareholder is known as a dividend.',
                      '2. Hire Purchase is an example of short term finance.', '3. Trade Credit is an example of long term finance.',
                      '4. Privatisation refers to the Government selling state-owned enterprises to private investors.', '5. Availing of a Bank Overdraft facility incurs an interest charge.'),
    (2, 2, 2, 2, 2), 'business-3-16', 'finance-true-false-2012', 3, [10], 'Answer key (scheme page 10): TRUE; FALSE; FALSE; TRUE; TRUE.', extra=['business-5-14', 'business-5-15'])
S(10, 'True or False: 1 TRUE 2 FALSE 3 FALSE 4 TRUE 5 TRUE')
add(1, 9, '', 'Q9', L(1, 4, 'Outline two characteristics of an autocratic leader:'), 10, 'business-2-11', 'autocratic-leader-characteristics', 4, [10],
    'Two characteristics at 5 marks each.', points('Characteristic', 2, (5,)),
    ['Scheme examples: ' + S(10, 'The autocratic leader has very little trust or confidence in his/her staff.')])
cum(1, 10, '', 'Q10', '\n'.join([L(1, 4, 'Column 1 is a list of business terms. Column 2 is a list of explanations for these terms. (One explanation has no match.)'),
                                 '1. Test Marketing\n' + L(1, 4, '2. Prototype Development', '3. Brainstorming', '4. Feasibility Study', '5. Break-even Point'),
                                 L(1, 4, 'A. A technique for coming up with new ideas for products.', 'B. Carried out to see if a product can be made at a reasonable cost.',
                                   'C. A firm’s revenue equals its expenditure.', 'D. A feature that distinguishes a product from its competitors.',
                                   'E. Making a ‘mock-up’ or sample of a product.', 'F. A new product is tried out on a small section of the market to get feedback and reaction.'),
                                 L(1, 4, 'Match the two lists by placing the letter of the correct explanation under the relevant number below.')]),
    (2, 2, 2, 2, 2), 'business-4-14', 'development-terms-matching', 4, [10], 'Answer key (scheme page 10): 1 F; 2 E; 3 A; 4 B; 5 C. Explanation D is unused.',
    extra=['business-3-19'], noun='matches')
L(1, 4, '1.Test Marketing')
S(10, '1. 2. 3. 4. 5. F E A B C')
add(1, 11, '', 'Q11', L(1, 4, 'Outline two reasons for fair dismissal and two reasons for unfair dismissal under the Unfair Dismissals Acts 1977-2007:') + '\nFair: (i) (ii)\nUnfair: (i) (ii)',
    10, 'business-0-14', 'fair-and-unfair-dismissal', 4, [10, 11], 'Two fair reasons 3 + 2 and two unfair reasons 3 + 2.',
    [comps('Fair dismissal', (3, 2), ['Reason 1', 'Reason 2'], 1), comps('Unfair dismissal', (3, 2), ['Reason 1', 'Reason 2'], 2)],
    ['Scheme examples: fair ' + bullets(S(10, '• Unsuitable qualifications for the post • Incompetence / incapable of carrying out required duties'), ', ') + ', misconduct, redundancy; unfair ' + bullets(S(11, '• Religious opinions • Political opinions • Race or colour'), ', ') + '.'])
flat(add(1, 12, '', 'Q12', L(1, 5, 'Draft, using today’s date, a Memorandum (Memo) from Jennifer King, Shop Steward, to all union members informing them of a trade union branch meeting to be held on Monday 18 June 2012 to discuss proposed redundancies.')
         + '\nMEMORANDUM To: / From: / Date: / Re: / Signed: / Title:', 10, 'business-2-12', 'branch-meeting-memo', 5, [11],
         'Layout six items at 1 each (to, from, date, re, signed, title) and content four at 1 each (venue, time, date, agenda).',
         [fixed('Memo', [('To', 1), ('From', 1), ('Date', 1), ('Re', 1), ('Signed', 1), ('Title', 1), ('Venue', 1), ('Time', 1), ('Meeting date', 1), ('Agenda (proposed redundancies)', 1)])],
         ['Scheme (page 11): ' + S(11, 'A (trade union) branch meeting will be held in (venue) the canteen at (time) 5.00 p.m. on (date) Monday 18 June 2012 to discuss (agenda) proposed redundancies.')
          + ' The allocation summary prints “' + S(4, 'Layout 6 items @ 1m each Content 4marks') + '”.']))
L(1, 5, 'MEMORANDUM To:')
add(1, 13, '', 'Q13', L(1, 5, 'Supermac’s fast food is an example of an Irish franchise. Explain the term ‘franchise’ and state one advantage of a franchise as a form of business ownership.') + '\nAdvantage:',
    10, 'business-5-14', 'franchise-with-advantage', 5, [11], 'Explanation 6 (3 + 3) and one advantage 4.', seq(comps('Franchise', (3, 3)), comps('Advantage', (4,))),
    ['Scheme: ' + S(11, 'This is the granting of a licence by the franchisor to the franchisee allowing the franchisee the right to supply and sell the franchisor’s established product or service.')])
add(1, 14, '', 'Q14', L(1, 5, 'Outline two advantages for a business of preparing a Cash Flow Forecast:'), 10, 'business-3-16', 'cash-flow-forecast-advantages',
    5, [11], 'Two advantages at 5 marks each (3 + 2).', points('Advantage', 2, (3, 2)))
cum(1, 15, '', 'Q15', L(1, 5, 'List three methods of external communication used in business:'), (4, 3, 3), 'business-2-12', 'external-communication-methods', 5, [11],
    'Scheme examples (page 11): ' + S(11, 'Verbal Telephone, meeting, radio, conference Written Letter, fax, newsletter, press release, brochure Electronic e-mail, video conference, EDI, website, text message.'),
    noun='methods')

# ---------------------------------------------------------------- Section 2 (75 marks each)
joe = (L(2, 6, 'Joe saw an advertisement in the local newspaper for a second-hand car which was for sale in Murray’s Garage. The advertisement stated that the car was four years old and had only 32,000 kilometres on the clock. He went to view the car, spoke to the garage owner Michael and took the car for a test drive. They agreed the price of € 9,000 and signed all the relevant documentation.')
       + '\n(Advertisement: ' + L(2, 6, 'Murray’s Garage 4 YEAR OLD CAR FOR SALE 32,000 Kilometres ONLY €9,000') + ')')
add(2, 1, 'a', 'Q1(A)', joe + '\n\n' + L(2, 6, '(A) Joe and Michael entered into a contract. What is a contract?'), 10, 'business-0-12', 'what-is-a-contract', 6, [12],
    'Explanation: 10 marks (4 + 3 + 3).', [comps('Contract', (4, 3, 3))], ['Scheme: ' + S(12, 'This is a legally binding agreement between two or more parties.')])
add(2, 1, 'b', 'Q1(B)', joe + '\n\n' + L(2, 6, '(B) Offer, Acceptance, Consideration, and Consent to Contract are elements of a valid contract. Explain any three of these elements. Illustrate your answer with reference to the above text.'),
    25, 'business-0-12', 'contract-elements-choice-2012', 6, [12], 'Choose three of the four elements: 10 (explanation 9, reference 1), 10 (9 + 1) and 5 (4 + 1).',
    seq(comps('First element you chose', (9, 1), ['Explanation', 'Reference to the text']), comps('Second element you chose', (9, 1), ['Explanation', 'Reference to the text']),
        comps('Third element you chose', (4, 1), ['Explanation', 'Reference to the text'])),
    ['You choose which three of the four printed elements to answer. The scheme marks every choice alike, so this is one card whichever elements you choose.',
     'The 10/10/5 sequence prices the three explanations, not particular elements.',
     'Offer (scheme PDF page 12): “' + S(12, 'A voluntary proposal/promise with conditions made by one party (offeror) to another (offeree) which must be accepted by the other party to be legally binding.') + '”',
     'Acceptance (scheme PDF page 12): “' + S(12, 'Assent / agreement / consent to the terms of the offer.') + '”',
     'Consideration (scheme PDF page 12): “' + S(12, 'Each party in a contract must give something of value to the other party / something of value must be exchanged.') + '”',
     'Consent to Contract (scheme PDF page 12): “' + S(12, 'Both parties in a contract must enter into a contract of their own free will – no undue pressure or duress') + '”'])
add(2, 1, 'c', 'Q1(C)', joe + '\n\n' + L(2, 6, '(C) A contract can be terminated (ended) by Performance or Frustration. Explain the underlined terms.') + '\n(Performance and Frustration are underlined.)', 15,
    'business-0-12', 'performance-and-frustration', 6, [12], 'Two explanations: 8 and 7.', unequal('Explanation', [(8,), (7,)], None),
    ['The 8-mark allowance is not tied to either term. Scheme: ' + S(12, 'Performance: Both parties to the contract fulfil their obligations and the contract is completed') + '; '
     + S(12, 'Frustration: An unforeseen event prevents the contract from being completed.')])
oliver = L(2, 6, 'Joe’s brother Oliver, a qualified mechanic, returned to Ireland on holidays from the USA three weeks later. He checked out Joe’s car and discovered that the reading on the clock was incorrect and that the car had actually travelled 62,000 kilometres. Joe went back to Murray’s Garage to complain about the incorrect clock reading, but did not receive any satisfaction. He decided to contact the National Consumer Agency.')
cpa_i = L(2, 6, '(D) (i) Explain how Murray’s Garage broke the terms of the Consumer Protection Act, 2007.')
add(2, 1, 'di', 'Q1(D)(i)', joe + '\n' + oliver + '\n\n' + cpa_i, 10, 'business-0-13', 'murrays-garage-breach', 6, [13], 'Explanation or reference to the text: 10 marks.',
    [comps('Breach explained', (10,), ['Explanation or reference to the text'])],
    ['Scheme: ' + S(13, 'Under the Act, it is illegal for an advertiser or business to make false or misleading claims about goods, services or prices.') + ' '
     + S(13, 'e.g. The car was advertised as having 32,000 km on the clock but it had actually travelled 62,000 km.')])
add(2, 1, 'dii', 'Q1(D)(ii)', oliver + '\n\n' + cpa_i + '\n' + L(2, 6, '(ii) Outline two functions of the National Consumer Agency.'), 15, 'business-0-13', 'nca-functions-2012',
    6, [13], 'Two functions: 12 and 3.', unequal('Function', [(12,), (3,)], None), ['The 12-mark allowance is not tied to a particular function.'])

solar = L(2, 7, 'Kevin Fitzpatrick, MD and his two brothers set up Solar Solutions Ltd in their home town of Kilduff, to produce solar panels for private and commercial buildings. They identified an increased market demand for renewable energy sources. They received a Government Grant of €90,000 to help set up the business. Kevin is a firm believer in running the business in an ethical manner, and hopes this will ensure its success in this sector.')
add(2, 2, 'a', 'Q2(A)', solar + '\n\n' + L(2, 7, '(A) What do the letters MD stand for? State one function of a MD.'), 10, 'business-2-13', 'md-letters-and-function',
    7, [14], 'The two letters at 2 each and one function 6 (3 + 3).', seq(comps('MD', (2, 2), ['Managing', 'Director']), comps('Function of a MD', (3, 3))),
    ['Scheme: ' + S(14, 'MD = Managing Director') + '; e.g. ' + S(14, 'Manages the company on a day-to-day basis.')])
add(2, 2, 'b', 'Q2(B)', solar + '\n\n' + L(2, 7, '(B) ‘Limited Liability’ and ‘Continuity of Existence’ are two advantages of a Private Limited Company. Explain these underlined terms.'), 20,
    'business-5-14', 'limited-liability-and-continuity', 7, [14], 'Each term 10 marks (5 + 5).',
    [comps('Limited Liability', (5, 5), i=1), comps('Continuity of Existence', (5, 5), i=2)],
    ['Scheme: ' + S(14, 'If a business fails / goes bankrupt, the shareholders can only lose the amount they have invested in the business.') + ' '
     + S(14, 'This means that if a shareholder dies or leaves, the company does not cease to operate.')])
add(2, 2, 'c', 'Q2(C)', solar + '\n\n' + L(2, 7, '(C) Describe two benefits for the town of Kilduff, of the Fitzpatrick brothers setting up Solar Solutions Ltd.'), 20, 'business-5-16',
    'kilduff-benefits', 7, [14], 'Two benefits at 10 marks each (5 + 5).', points('Benefit', 2, (5, 5)))
add(2, 2, 'd', 'Q2(D)', solar + '\n\n' + L(2, 7, '(D) Explain the term ‘Grant’ and state one advantage of a grant as a source of finance.'), 10, 'business-3-16', 'grant-and-advantage',
    7, [15], 'Explanation 6 (3 + 3) and one advantage 4.', seq(comps('Grant', (3, 3)), comps('Advantage', (4,))),
    ['Scheme: ' + S(15, 'A grant is a long term source of finance given by Government agencies')])
add(2, 2, 'e', 'Q2(E)', solar + '\n\n' + L(2, 7, '(E) Outline two ways in which Solar Solutions Ltd can behave ethically towards its customers.'), 15, 'business-5-17', 'ethical-towards-customers',
    7, [15], 'Two ways: 8 and 7.', unequal('Way', [(8,), (7,)], None), [UNTIED])

trade = L(2, 7, 'Irish Agricultural based exports have increased by almost 12%, highlighting the importance of this sector to the Irish economy.') + '\nVisible Exports €1,400 million\nVisible Imports €1,200 million'
L(2, 7, 'Visible Exports €1,400 million Visible Imports €1,200 million')
bot_i = L(2, 7, '(A) (i) Using the above information, calculate the Balance of Trade. (Show workings.)')
flat(add(2, 3, 'ai', 'Q3(A)(i)', trade + '\n\n' + bot_i, 10, 'business-6-13', 'balance-of-trade-2012', 7, [16], 'Calculation: 10 marks (3 + 3 + 4).',
         [response(1, 'Balance of trade', [('exports', 'Visible Exports €1,400m', 3), ('imports', 'minus Visible Imports €1,200m', 3), ('answer', '= €200m', 4)])],
         ['Scheme (page 16): ' + S(16, 'Balance of Trade = Visible Exports – Visible Imports = €1,400m – €1,200m = €200m') + '; the summary prints “' + S(6, 'Balance of Trade Calculation – 10marks (3m + 3m + 4m)') + '”.']))
add(2, 3, 'aii', 'Q3(A)(ii)', trade + '\n\n' + bot_i + '\n' + L(2, 7, '(ii) State whether it is a surplus or a deficit.'), 5, 'business-6-13', 'trade-surplus-or-deficit-2012',
    7, [16], 'State it for 5 marks.', [single('Surplus or deficit', 5, 'Answer stated')], ['Answer: Surplus (scheme page 16).'])
vis_i = L(2, 7, '(B) (i) Explain the term ‘visible export’.')
add(2, 3, 'bi', 'Q3(B)(i)', trade + '\n\n' + vis_i, 9, 'business-6-13', 'visible-export-explained', 7, [16], 'Explanation: 9 marks (5 + 4).', [comps('Visible export', (5, 4))],
    ['Scheme: ' + S(16, 'Visible exports are physical goods that are sold by Irish firms to customers in other countries.')])
cum(2, 3, 'bii', 'Q3(B)(ii)', trade + '\n\n' + vis_i + '\n' + L(2, 7, '(ii) Name two examples of Irish agricultural visible exports.'), (3, 3), 'business-6-13', 'agricultural-export-examples',
    7, [16], 'Scheme examples (page 16): ' + S(16, 'Beef, butter, cheese, mushrooms.'), noun='examples')
add(2, 3, 'c', 'Q3(C)', trade + '\n\n' + L(2, 7, '(C) Outline two benefits for Irish business engaged in International Trade.'), 15, 'business-6-13', 'international-trade-benefits-2012',
    7, [16], EIGHT, eight_seven('Benefit'), [UNTIED])
add(2, 3, 'd', 'Q3(D)', trade + '\n\n' + L(2, 7, '(D) Outline two effects on Irish households of reducing mortgage interest rates.'), 15, 'business-5-15', 'mortgage-rate-effects',
    7, [16], EIGHT, eight_seven('Effect'), [UNTIED], extra=['business-3-16'])
add(2, 3, 'e', 'Q3(E)', trade + '\n\n' + L(2, 7, '(E) Outline two effects on Irish retailers of increasing the VAT rate from 21% to 23%.'), 15, 'business-3-18', 'vat-increase-effects',
    7, [16], EIGHT, eight_seven('Effect'), [UNTIED], extra=['business-5-15'])

rathnew = L(2, 8, 'Renew Rathnew') + '\n' + L(2, 8, 'The people of Rathnew have come together to start a Renew Rathnew Campaign. High unemployment and a drop in tourist numbers has resulted in many business closures. The town is located in a scenic area and the people believe that better use could be made of the unused buildings and the local walking trails to attract tourists. They have formed a committee, led by Chairperson Margaret Lynch and Secretary Danny Kelly to plan the campaign. They are determined to improve their town and attract more business and tourism to the area. A committee meeting is to be held shortly.')
add(2, 4, 'a', 'Q4(A)', rathnew + '\n\n' + L(2, 8, '(A) Outline three enterprising skills/characteristics required for this plan to succeed.'), 15, 'business-1-5', 'rathnew-enterprising-skills',
    8, [17], 'Three at 5 marks each (3 + 2).', points('Characteristic', 3, (3, 2)), extra=['business-5-16'])
flat(add(2, 4, 'b', 'Q4(B)', rathnew + '\n\n' + L(2, 8, '(B) Using today’s date, draft the Notice and Agenda for the first meeting of the Renew Rathnew Committee. (The Agenda should contain at least four items.)'), 25,
         'business-2-12', 'rathnew-notice-and-agenda', 8, [17], 'Notice seven items at 2 each, the heading Agenda 1, and four agenda items 3 + 3 + 2 + 2.',
         seq(comps('Notice', (2, 2, 2, 2, 2, 2, 2), [f'Notice item {k}' for k in range(1, 8)]), comps('Agenda heading', (1,), ['Agenda']),
             comps('Agenda items', (3, 3, 2, 2), ['Agenda item 1', 'Agenda item 2', 'Agenda item 3', 'Agenda item 4'])),
         ['Scheme (page 17): ' + S(17, 'The first meeting of the Renew Rathnew Committee will take place in Rathnew Community Centre on Thursday 21 June 2012 at 8.00p.m.') + ' Agenda: '
          + S(17, '1. Introduction of committee members 2. Chairperson’s address 3. Plans/ideas for unused buildings 4. Plans/ideas for walking trails') + ' ...',
          'The allocation summary prints “' + S(6, 'Notice : 7 items @ 2m ‘Agenda’: 1m Agenda contents: 4 items (3m + 3m + 2m + 2m)') + '”.']))
add(2, 4, 'c', 'Q4(C)', rathnew + '\n\n' + L(2, 8, '(C) Outline two advantages of meetings as a method of communication.'), 10, 'business-2-12', 'meetings-advantages-2012',
    8, [18], 'Two advantages at 5 marks each.', points('Advantage', 2, (5,)))
add(2, 4, 'd', 'Q4(D)', rathnew + '\n\n' + L(2, 8, '(D) Describe two functions of the Chairperson at a meeting.'), 10, 'business-2-12', 'chairperson-functions',
    8, [18], 'Two functions at 5 marks each.', points('Function', 2, (5,)))
add(2, 4, 'e', 'Q4(E)', rathnew + '\n\n' + L(2, 8, '(E) Outline two benefits of planning for the Renew Rathnew Committee.'), 15, 'business-2-13', 'rathnew-planning-benefits',
    8, [18], EIGHT, eight_seven('Benefit'), [UNTIED])

elaine = (L(2, 8, 'Elaine McGrath works as an Assessor for Insure2Bsure Ltd. Her job includes processing claims from customers and deciding on compensation. She earns Gross Pay of €32,000 per annum. She pays PAYE at the standard rate of 20%. Assume PRSI is 4% and the Universal Social Charge (USC) is 3%, both calculated on her gross pay. Her annual Tax Credit is €3,600. Elaine is thinking of buying a car. She needs finance and cannot decide between a Term Loan or Leasing.')
          + '\n(PAYE, PRSI and Tax Credit are underlined.)')
add(2, 5, 'a', 'Q5(A)', elaine + '\n\n' + L(2, 8, '(A) Explain the three underlined terms.'), 15, 'business-3-18', 'paye-prsi-tax-credit',
    8, [19], 'Each term 5 marks.', [comps('PAYE', (5,), i=1), comps('PRSI', (5,), i=2), comps('Tax Credit', (5,), i=3)],
    ['Scheme: ' + S(19, 'PAYE Pay As You Earn – this is a direct tax paid by employees on their income /wages /salaries.') + ' '
     + S(19, 'A tax credit is a reduction in the amount of tax payable by the taxpayer and depends on the taxpayer’s personal circumstances.')])
add(2, 5, 'b', 'Q5(B)', elaine + '\n\n' + L(2, 8, '(B) Explain two of the following Principles of Insurance and give one example in each case:', '(i) Insurable Interest (ii) Indemnity (iii) Utmost Good Faith'),
    15, 'business-3-17', 'insurance-principles-choice-2012', 8, [19], 'Choose two of the three principles: 8 (explanation 3 + 2, example 3) and 7 (explanation 3 + 2, example 2).',
    seq(comps('First principle you chose', (3, 2, 3), ['Explained', 'Explanation developed', 'Example']),
        comps('Second principle you chose', (3, 2, 2), ['Explained', 'Explanation developed', 'Example'])),
    ['You choose which two of the three printed principles to answer. The scheme marks every choice alike, so this is one card whichever principles you choose.',
     'The 8-mark allowance is not tied to a particular principle.',
     'Insurable Interest (scheme PDF page 19): “' + S(19, 'A person seeking insurance must benefit financially from the continued existence of the item and suffer by its loss/damage.') + '”',
     'Indemnity (scheme PDF page 19): “' + S(19, 'A person cannot make a profit from an insurance claim.') + '”',
     'Utmost Good Faith (scheme PDF page 19): “' + S(19, 'When completing a proposal form for insurance, the insured must disclose truthfully all material facts to the insurer.') + '”'])
terms = L(2, 8, '(C) Explain the insurance terms:')
add(2, 5, 'ci', 'Q5(C)(i)', elaine + '\n\n' + terms + '\n' + L(2, 8, '(i) Claim'), 5, 'business-3-17', 'claim-explained', 8, [20], 'Explanation: 5 marks.',
    [comps('Claim', (5,))], ['Scheme: ' + S(20, 'When a risk which is covered by an insurance policy actually occurs the insured can apply to the insurance company to get money to cover the loss.')])
add(2, 5, 'cii', 'Q5(C)(ii)', elaine + '\n\n' + terms + '\n' + L(2, 8, '(ii) Compensation'), 5, 'business-3-17', 'compensation-explained', 8, [20], 'Explanation: 5 marks.',
    [comps('Compensation', (5,))], ['Scheme: ' + S(20, 'This is the amount of money paid by the insurer to the insured after a claim has been made for a loss which has occurred')])
pay = add(2, 5, 'd', 'Q5(D)', elaine + '\n\n' + L(2, 8, '(D) Calculate Elaine’s Net Annual take home pay.'), 20, 'business-3-18', 'elaine-net-take-home-pay', 8, [20],
          'Eight figures: four at 4 marks and four at 1 mark.',
          [response(1, 'Net annual take home pay', [('four-mark', 'Four figures at 4 marks each', 16), ('one-mark', 'Four figures at 1 mark each', 4)])],
          ['The allocation summary prints “' + S(7, 'Calculation of Net Pay Four figures @ 4m each Four figures @ 1m each') + '” without naming which four carry 4.',
           'Scheme figures (page 20): ' + S(20, 'Gross Income €32,000 Less Deductions: PAYE (20% of 32,000) 6,400 Less Tax Credit – 3,600 Net PAYE 2,800 PRSI (4% of 32,000) 1,280 USC (3% of 32,000) 960 Total Deductions € 5,040') + '; ' + S(20, 'Net Take Home Pay €26,960') + '.'])
permit(pay, 0, [0, 4, 8, 12, 16], 0)
permit(pay, 0, [0, 1, 2, 3, 4], 1)
add(2, 5, 'e', 'Q5(E)', elaine + '\n\n' + L(2, 8, '(E) Choose either Term Loan or Leasing and outline two advantages of your chosen source of finance.'), 15, 'business-3-16', 'term-loan-or-leasing-choice',
    8, [20], 'Choose one source and outline two advantages: 8 and 7.', unequal('Advantage', [(8,), (7,)], None),
    ['You choose one of the two printed sources. The scheme marks either alike (8 and 7) under one topic, so this is one card whichever source you choose.',
     'Term Loan (scheme PDF page 20): “' + S(20, 'Repayment is spread over a number of years') + '”; “' + S(20, 'Elaine does not have to wait to save up for the car – immediate ownership') + '”',
     'Leasing (scheme PDF page 20): “' + S(20, 'Elaine will have immediate use of the car') + '”; “' + S(20, 'She does not have to come up with a lump sum to purchase the car') + '”'])

water = L(2, 9, '‘White Water’ Department Store recently installed a new IT system to track its sales. Deirdre McDermott, the Human Resource Manager at ‘White Water’, organised training of the sales staff to use the new system. Deirdre also organised the sales staff into teams and they receive a basic wage, commission and benefit-in-kind.')
add(2, 6, 'a', 'Q6(A)', water + '\n\n' + L(2, 9, '(A) Explain two of the following functions of Deirdre’s job as a Human Resource Manager: (i) Training and Development (ii) Recruitment and Selection (iii) Employer/Employee Relations'),
    20, 'business-3-20', 'hr-functions-choice-2012', 9, [21], 'Choose two of the three functions: each 10 (two points at 5).',
    seq(comps('First function you chose', (5, 5)), comps('Second function you chose', (5, 5))),
    ['You choose which two of the three printed functions to answer. The scheme marks every choice alike (2 @ 5 each), so this is one card whichever functions you choose.',
     'Training and Development (scheme PDF page 21): “' + S(21, 'Training involves supplying the skills, knowledge and attitudes needed by employees to do their jobs better.') + '”',
     'Recruitment and Selection (scheme PDF page 21): “' + S(21, 'The process of attracting suitable candidates to apply for vacancies in a firm.') + '”',
     'Employer/Employee Relations (scheme PDF page 21): “' + S(21, 'It is essential to maintain good industrial relations in an organisation.') + '”'])
cum(2, 6, 'b', 'Q6(B)', water + '\n\n' + L(2, 9, '(B) Deirdre must prepare a Job Description when recruiting new staff. Outline three items included in a Job Description.'), (5, 5, 5), 'business-3-20',
    'job-description-items', 9, [22], 'Scheme items (page 22): ' + bullets(S(22, '• Job Title • Details of work • Place of work • Duties and responsibilities • Salary and conditions / hours of work')) + '.', noun='items')
add(2, 6, 'c', 'Q6(C)', water + '\n\n' + L(2, 9, '(C) Explain the terms ‘Commission’ and ‘Benefit-in-Kind’ and illustrate your answer with one example of each.'), 15, 'business-3-20',
    'commission-and-bik-2012', 9, [22], 'Commission: explanation 4 and example 4. Benefit-in-kind: explanation 4 and example 3.',
    [comps('Commission', (4, 4), ['Explained', 'Example'], 1), comps('Benefit-in-Kind', (4, 3), ['Explained', 'Example'], 2)],
    ['Scheme: ' + S(22, 'Payment based on sales – employee earns a percentage of value of sales made') + '; ' + S(22, 'Non-financial method of reward given to employees; also known as ‘perks’.')],
    extra=['business-3-18'])
add(2, 6, 'd', 'Q6(D)', water + '\n\n' + L(2, 9, '(D) Explain two benefits of teamwork.'), 10, 'business-3-20', 'teamwork-benefits-2012', 9, [22], 'Two benefits at 5 marks each.', points('Benefit', 2, (5,)))
add(2, 6, 'e', 'Q6(E)', water + '\n\n' + L(2, 9, '(E) Illustrate three other uses of Information Technology for ‘White Water’ Department Store.'), 15, 'business-2-12', 'it-uses-department-store',
    9, [22], 'Three uses at 5 marks each.', points('Use', 3, (5,)))

rory = L(2, 10, 'Rory Byrne, a trained chef, is considering setting up his own food business. He has no business experience so he approached his friend Sarah Dunne, a business graduate, for advice on a business start-up. He wants to find out what finance options he has, what type of production process he should use and what organisation structure would be most suitable. He also wants to decide on a target market.')
add(2, 7, 'a', 'Q7(A)', rory + '\n\n' + L(2, 10, '(A) Outline two reasons why a Business Plan should be prepared.'), 10, 'business-4-15', 'business-plan-reasons-2012',
    10, [23], 'Two reasons: 8 and 2.', unequal('Reason', [(8,), (2,)], None), ['The 8-mark allowance is not tied to a particular reason.'])
add(2, 7, 'b', 'Q7(B)', rory + '\n\n' + L(2, 10, '(B) Explain three factors Rory should consider before choosing a source of finance.'), 15, 'business-3-16', 'finance-choice-factors',
    10, [23], 'Three factors: 6, 6 and 3.', unequal('Factor', [(6,), (6,), (3,)], None), ['The 6/6/3 sequence prices the three factors, not particular factors.'])
prod = L(2, 10, '(C) Explain the following production options and give one example in each case.')
add(2, 7, 'ci', 'Q7(C)(i)', rory + '\n\n' + prod + '\n' + L(2, 10, '(i) Job Production'), 8, 'business-4-15', 'job-production-with-example', 10, [23],
    'Explanation 4 and an example 4.', [comps('Job Production', (4, 4), ['Explained', 'Example'])],
    ['Scheme: ' + S(23, 'Firm produces one-off goods to order') + '; e.g. ' + S(23, 'hand crafted furniture, tailored suits, cruise liners.')])
add(2, 7, 'cii', 'Q7(C)(ii)', rory + '\n\n' + prod + '\n' + L(2, 10, '(ii) Batch Production.'), 7, 'business-4-15', 'batch-production-with-example', 10, [23],
    'Explanation 4 and an example 3.', [comps('Batch Production', (4, 3), ['Explained', 'Example'])],
    ['Scheme: ' + S(23, 'A process whereby a certain amount or quantity of a product is produced at the same time and then production switches to a different batch/group.')])
add(2, 7, 'd', 'Q7(D)', rory + '\n\n' + L(2, 10, '(D) Outline two risks and two rewards of setting up a Sole Trader business.'), 20, 'business-5-14', 'sole-trader-risks-and-rewards',
    10, [24], 'Two risks and two rewards at 5 marks each.', seq(points('Risk', 2, (5,)), points('Reward', 2, (5,))), extra=['business-1-5'])
tm_i = L(2, 10, '(E) (i) Explain the term ‘target market’.')
add(2, 7, 'ei', 'Q7(E)(i)', rory + '\n\n' + tm_i, 8, 'business-4-16', 'target-market-explained-2012', 10, [24], 'Explanation: 8 marks.', [comps('Target market', (8,))],
    ['Scheme: ' + S(24, 'A target market is the group of people at whom a particular product or service is aimed.')])
cum(2, 7, 'eii', 'Q7(E)(ii)', rory + '\n\n' + tm_i + '\n' + L(2, 10, '(ii) Name two possible target markets that Rory might consider.'), (6, 1), 'business-4-16', 'rory-target-markets',
    10, [24], 'Scheme examples (page 24): ' + bullets(S(24, '• Early morning café for people on way to work • Low calorie foods for the health conscious/healthy options • Vegetarian food')) + '.', noun='target markets')

sweet = L(2, 11, 'Sweetdreams Ltd') + '\n' + L(2, 11, 'Sweetdreams Ltd, based in Dublin since 1997, is a large manufacturer of chocolate and confectionary. The company is continuously researching the market to ensure it maintains its market position for its brand.')
add(2, 8, 'a', 'Q8(A)', sweet + '\n\n' + L(2, 11, '(A) Explain Field Research and Desk Research and give one example in each case.'), 20, 'business-4-16', 'field-and-desk-research-2012',
    11, [25], 'Each type: explanation 5 (3 + 2) and an example 5.',
    [comps('Field Research', (3, 2, 5), ['Explained', 'Explanation developed', 'Example'], 1), comps('Desk Research', (3, 2, 5), ['Explained', 'Explanation developed', 'Example'], 2)],
    ['Scheme: ' + S(25, 'This involves going out to the public to find out new information directly from customers (Primary Research)') + '; '
     + S(25, 'This involves accessing information that is already available (gathered by others) within or outside the firm.')])
chan_i = L(2, 11, '(B) (i) Explain what is meant by the term ‘Channels of Distribution’.')
add(2, 8, 'bi', 'Q8(B)(i)', sweet + '\n\n' + chan_i, 8, 'business-4-17', 'channels-explained-2012', 11, [25], 'Explanation: 8 marks (4 + 4).', [comps('Channels of Distribution', (4, 4))],
    ['Scheme: ' + S(25, 'Refers to the various paths/methods by which goods are transferred from producer to consumer.')])
add(2, 8, 'bii', 'Q8(B)(ii)', sweet + '\n\n' + chan_i + '\n' + L(2, 11, '(ii) Illustrate, using a diagram, a suitable channel of distribution for Sweetdreams Ltd.'), 7, 'business-4-17',
    'sweetdreams-channel-diagram', 11, [25], 'Diagram: 7 marks.', [comps('Channel diagram', (7,))],
    ['Scheme (page 25): ' + S(25, 'PRODUCER / MANUFACTURER ↓ WHOLESALER ↓ RETAILER ↓ CONSUMER') + '.'])
add(2, 8, 'c', 'Q8(C)', sweet + '\n\n' + L(2, 11, '(C) Describe two Sales Promotion methods that Sweetdreams Ltd may use to increase sales.'), 10, 'business-4-17', 'sweetdreams-sales-promotions',
    11, [25], 'Two methods at 5 marks each.', points('Sales promotion', 2, (5,)))
add(2, 8, 'd', 'Q8(D)', sweet + '\n\n' + L(2, 11, '(D) Outline three factors Sweetdreams Ltd must consider when setting the price of its products.'), 15, 'business-4-17', 'sweetdreams-pricing-factors',
    11, [26], 'Three factors at 5 marks each (3 + 2).', points('Factor', 3, (3, 2)))
add(2, 8, 'e', 'Q8(E)', sweet + '\n\n' + L(2, 11, '(E) Outline three advantages of branding for Sweetdreams Ltd.'), 15, 'business-4-17', 'sweetdreams-branding-advantages',
    11, [26], 'Three advantages at 5 marks each (3 + 2).', points('Advantage', 3, (3, 2)))

# ---------------------------------------------------------------- checks and write-out
qn = lambda c: c['questionRef'].split(' Q')[1].split('(')[0]
for section, count, total in [('1', 15, 10), ('2', 8, 75)]:
    for q in range(1, count + 1):
        got = sum(c['totalMarks'] for c in P.created if c['section'] == section and qn(c) == str(q))
        assert got == total, (section, q, got)
assert not [i for i in ORIGINAL if i.startswith('bus-2012-ol-')]
assert not P.pools

SELECTION = {
    1: 'No finite printed answer menu occurs in Section 1 (answer ten of fifteen at 10 marks). TRUE/FALSE in Q8 and the matching rows in Q10 are required answer formats. Support-note lists are open examples.',
    2: 'Four printed choices are one card each (the scheme marks every choice alike under one topic): Q1(B) any three of four contract elements, Q5(B) any two of three principles of insurance, Q5(E) term loan or leasing, and Q6(A) any two of three HR functions. Q1(C) and Q5(A) underline terms that are all required. Sub-parts with their own published marks are separate cards. Support-note lists are open examples.',
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
    if m == 'any three' and own(w, m, 'Explain any three of these elements'):
        return 'finite-choice', 'Section 2 Q1(B) asks for any three of the four printed contract elements. The scheme marks every choice alike (10, 10 and 5), so one card carries all four with the scheme wording for each.', 'bus-2012-ol-s2-q1b'
    if m == 'two of' and own(w, m, 'Explain two of the following Principles of Insurance'):
        return 'finite-choice', 'Section 2 Q5(B) asks for any two of the three printed principles of insurance. The scheme marks every choice alike (8 and 7), so one card carries all three with the scheme wording for each.', 'bus-2012-ol-s2-q5b'
    if m == 'two of' and own(w, m, 'Explain two of the following functions'):
        return 'finite-choice', 'Section 2 Q6(A) asks for any two of the three printed HR functions. The scheme marks every choice alike (10 each), so one card carries all three with the scheme wording for each.', 'bus-2012-ol-s2-q6a'
    if m in ('Choose', 'either', 'or') and own(w, m, 'Choose either Term Loan or Leasing'):
        return 'finite-choice', 'Section 2 Q5(E) offers a term loan or leasing. The scheme marks either alike (8 and 7) under one topic, so one card carries both with the scheme wording for each.', 'bus-2012-ol-s2-q5e'
    if m == 'or' and own(w, m, 'decide between a Term Loan or Leasing'):
        return 'case-context', '“a Term Loan or Leasing” in the Section 2 Q5 extract states Elaine’s dilemma; the choice itself is the Q5(E) task, which is one card.', None
    if m == 'or' and (own(w, m, 'TRUE or FALSE') or own(w, m, 'True or False')):
        return 'required-headings', 'TRUE/FALSE are answer labels for each of the five required statements in Section 1 Q8, not optional tasks.', None
    if m == 'or' and own(w, m, 'surplus or a deficit'):
        return 'required-headings', 'Section 2 Q3(A)(ii) requires a determination of surplus or deficit; it is one required answer, not a choice of task.', None
    if m == 'or' and own(w, m, 'by Performance or Frustration'):
        return 'required-headings', 'Section 2 Q1(C) underlines both Performance and Frustration and asks the candidate to explain the underlined terms; both are required.', None
    if m == 'or' and own(w, m, 'a ‘mock-up’ or sample'):
        return 'case-context', 'Wording inside explanation E of the Section 1 Q10 matching table, not a choice of task.', None
    assert (fileid, page) in {('LC033GLP000EV', 1), ('LC033GLP000EV', 6)} and m in ('either', 'or'), (fileid, page, m, w)
    return 'exam-navigation', 'The cover and Section 2 rubrics set how many whole questions a candidate answers (one from Part 1, two from Part 2 and one other from either part). Every numbered question remains in the practice corpus as separate cards.', None


n = P.write([(1, range(1, 16)), (2, range(1, 9))], SELECTION, classify,
            'Every part of {year} Ordinary Section {section} Question {q} was visually checked against its SEC paper, allocation summary and support notes. The single-booklet identity keeps the short (n) and long (S2Q) question numbering apart.')
print(f'Reviewed {len(P.created)} 2012 Ordinary tasks; classified {n} raw selection matches.')
