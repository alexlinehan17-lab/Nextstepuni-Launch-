"""Review the 2011 Ordinary English paper (one booklet: Section 1 and Section 2).

2011: answer ten of fifteen short questions at 10 marks and four of eight
long questions at 75 (one from Part 1, two from Part 2 and one other), all in
one twelve-page booklet (LC033GLP000EV, the same file id as its scheme). No
Ordinary card existed for 2011, so every card is new. The allocation summary
(scheme pages 4-8) sets each boundary; printed sub-parts with their own
published marks are separate cards. Two printed choices are one card each
(the scheme marks every choice alike and files them under one topic):
Section 2 Q4(E) the purpose of two of three PAYE forms, and Q8(C)(ii) any
two of the five levels of Maslow's hierarchy.

Paper page 11 (Question 8, Brady's Hotel) is cut into vertical strips in its
text layer, each overlapping the next by one character, so get_text() reads
it as word fragments. Its lifts come from the page rebuilt from character
positions (scripts/markbank/authoring/strip_pages.py, the same reading the
census and the selection scan use); the result was checked line by line
against the rendered page before any lift.
"""
import re
import sys
from bus_lib import (Paper, ORIGINAL, norm, comps, points, seq, unequal, single, response, permit)
sys.path.insert(0, 'scripts/markbank/authoring')
from strip_pages import strip_cut, strip_lines

T = {(1, q): 4 for q in range(1, 16)}
T.update({(2, 1): 5, (2, 2): 5, (2, 3): 6, (2, 4): 6, (2, 5): 7, (2, 6): 7, (2, 7): 8, (2, 8): 8})
P = Paper(2011, 'ordinary', {1: 'LC033GLP000EV', 2: 'LC033GLP000EV'}, 'LC033GLP000EV', T)
L, S, add, cum = P.lift, P.scheme, P.add, P.cumulative


assert [n + 1 for n, page in enumerate(P.docs['LC033GLP000EV']) if strip_cut(page)] == [11]
P.text[('LC033GLP000EV', 11)] = norm('\n'.join(strip_lines(P.docs['LC033GLP000EV'][10])))
for line in ['Brady’s Hotel is a family run business situated in a seaside town. It provides accommodation, restaurant and bar services. Mark Brady has overall responsibility for managing the hotel.',
             '(C) Maslow’s Hierarchy of Needs is presented below. (i) List levels 2, 3 and 5 (in your answer book). (ii) Briefly explain two of the five levels. (20)',
             'Current Assets 900,000 800,000 Current Liabilities 500,000 400,000', 'Page 11 of 12']:
    assert line in P.text[('LC033GLP000EV', 11)], line

EIGHT = 'Two points are required: 8 (4 + 4) and 7 (4 + 3).'
UNTIED = 'The 8-mark allowance is not tied to a particular point.'


def eight_seven(label):
    return unequal(label, [(4, 4), (4, 3)], None)


def flat(card):
    for r in card['rubric']['responses']:
        for a in r['allocations']:
            a['permittedMarks'] = [0, a['maxMarks']]
    return card


def bullets(text, mark='•', sep='; '):
    """Join a support-note list; the scheme marks items with • or o."""
    return sep.join(x.strip() for x in re.split(rf'(?:^|\s){re.escape(mark)}\s', text) if x.strip())


# ---------------------------------------------------------------- Section 1 (10 marks each)
add(1, 1, '', 'Q1', L(1, 2, 'What do the following letters stand for? (Write each answer in the space provided.)', 'AGM PLC AOB').replace(' PLC', '\nPLC').replace(' AOB', '\nAOB'),
    10, 'business-2-12', 'abbreviations-agm-plc-aob', 2, [9], 'The first correct term earns 4 (2 + 1 + 1); the second and third 3 each (1 + 1 + 1).',
    [comps('First correct term', (4,), ['Words written in full'], 1), comps('Second correct term', (3,), ['Words written in full'], 2),
     comps('Third correct term', (3,), ['Words written in full'], 3)],
    ['Answer key: AGM ' + S(9, 'Annual General Meeting') + '; PLC ' + S(9, 'Public Limited Company') + '; AOB ' + S(9, 'Any Other Business') + '.'],
    extra=['business-5-14'])
add(1, 2, '', 'Q2', L(1, 2, 'Explain the term ‘investor’ and give two examples of investors.') + '\nExplanation:\nExamples: (i) (ii)', 10, 'business-0-12', 'investor-with-examples',
    2, [9], 'Explanation 6 (3 + 3) and two examples at 2 each.', seq(comps('Investor explained', (3, 3)), points('Example', 2, (2,))),
    ['Scheme: ' + S(9, 'Investors provide capital / funds / money / finance / grant needed for business / entrepreneur.') + ' Examples include '
     + S(9, 'Shareholders (with a view to profit/dividend)') + ' and ' + S(9, 'Lenders (banks) provide loan capital which must be repaid with interest') + '.'],
    extra=['business-3-16'])
cum(1, 3, '', 'Q3', L(1, 2, 'Indicate by means of a tick (✓) the appropriate source of finance for the following:') + '\nShort term | Medium term | Long term\n'
    + '\n'.join(['Delivery van', 'Purchase of stock', 'Extension to a factory', 'Payment of electricity bill']), (3, 3, 2, 2), 'business-3-16', 'finance-term-ticks-2011', 2, [9],
    'Answer key (ticks on scheme page 9): Delivery van Medium term; Purchase of stock Short term; Extension to a factory Long term; Payment of electricity bill Short term.', noun='ticks')
L(1, 2, 'Short term Medium term Long term Delivery van Purchase of stock Extension to a factory Payment of electricity bill')
add(1, 4, '', 'Q4', L(1, 2, 'Outline two reasons why Irish firms export goods and give two examples of Irish exports.') + '\nReasons: (i) (ii)\nExamples: (i) (ii)', 10,
    'business-6-13', 'export-reasons-and-examples', 2, [9], 'Two reasons at 3 each and two examples at 2 each.', seq(points('Reason', 2, (3,)), points('Example', 2, (2,))),
    ['Scheme reasons: ' + S(9, '(i) to increase sales and profits (ii) expertise (iii) domestic market too small (iv) earn money to pay for imports') + '; examples: '
     + S(9, 'Agricultural produce – meat, cheese, butter Pharmaceutical products Medical devices') + '.'])
cum(1, 5, '', 'Q5', L(1, 3, '‘Capacity to contract’ is the ability of a person to enter into a legal contract. List three situations where a person does not have capacity to contract.'),
    (4, 3, 3), 'business-0-12', 'no-capacity-to-contract', 3, [9],
    'Scheme situations (page 9): ' + bullets(S(9, 'o persons under 18 (except for everyday items such as food, clothes) o persons under the influence of alcohol/drugs o bankrupt persons o people of unsound mind o persons with diplomatic immunity'), 'o') + '.',
    noun='situations')
flat(add(1, 6, '', 'Q6', L(1, 3, 'The following information has been taken from the accounts of Dalton Ltd on 31/12/2010:') + '\nNet Profit: €40,000\nCapital Employed: €500,000\n'
         + L(1, 3, 'Calculate the Return on Capital Employed: (Show your workings.)') + '\nAnswer: %\nWorkings:', 10, 'business-3-19', 'roce-dalton', 3, [9],
         'Formula 2, the figures 4 and the answer 4.',
         [response(1, 'Return on Capital Employed', [('formula', 'Formula: Net Profit x 100 / Capital Employed', 2), ('figures', 'Figures: €40,000 x 100 / €500,000', 4), ('answer', 'Answer: 8%', 4)])],
         ['Scheme (page 9): ' + S(9, 'Net Profit x 100 = €40,000 x 100 = 8% Capital Employed €500,000') + ' (Net Profit x 100 over Capital Employed); the allocation summary prints “'
          + S(4, 'Workings: Formula @ 2 marks Figures @ 4 marks Answer @ 4 marks') + '”.']))
L(1, 3, 'Net Profit: €40,000 Capital Employed: €500,000')
cum(1, 7, '', 'Q7', L(1, 3, 'Write TRUE or FALSE after each of the following statements:',
                      '(i) Utmost Good Faith means that the insured must tell the truth and disclose all material facts.',
                      '(ii) Batch Production involves producing identical products continuously.',
                      '(iii) The Average Clause rule applies in insurance when an item is underinsured.',
                      '(iv) An Autocratic leader likes to involve employees in decision-making.',
                      '(v) Job Production involves producing a one-off single product to a customer’s specification.'),
    (2, 2, 2, 2, 2), 'business-3-17', 'true-false-2011', 3, [10], 'Answer key (scheme page 10): (i) True; (ii) False; (iii) True; (iv) False; (v) True.',
    extra=['business-4-15', 'business-2-11'])
for snip in ['disclose all material facts. True', 'continuously. False', 'underinsured. True', 'decision-making. False', 'specification. True']:
    S(10, snip)
add(1, 8, '', 'Q8', L(1, 3, 'Outline two advantages to Ireland of EU membership.'), 10, 'business-6-14', 'eu-membership-advantages-2011', 3, [10],
    'Two advantages at 5 marks each.', points('Advantage', 2, (5,)),
    ['Scheme examples: ' + S(10, 'Large market available to Irish firms for exporting/expansion') + '; ' + S(10, 'Free movement of capital and labour.')])
cum(1, 9, '', 'Q9', L(1, 4, 'List three methods of Written Communication a business might use:'), (4, 3, 3), 'business-2-12', 'written-communication-methods', 4, [10],
    'Scheme methods (page 10): ' + S(10, '(i) Letter (ii) Memorandum (iii) Business documents (iv) Fax (v) Report (vi) Newsletter (vii) E-mail (viii) Minutes (ix) Notices (x) Text messages') + '.',
    noun='methods')
add(1, 10, '', 'Q10', L(1, 4, 'Explain each of the following terms:') + '\n' + L(1, 4, '(i) On-the-job training:') + '\n' + L(1, 4, '(ii) Off-the-job training:'), 10,
    'business-3-20', 'on-and-off-the-job-training', 4, [10], 'Each term 5 marks (3 + 2).',
    [comps('On-the-job training', (3, 2), None, 1), comps('Off-the-job training', (3, 2), None, 2)],
    ['Scheme: ' + S(10, 'This means training and practical work experience carried out in the workplace.') + ' '
     + S(10, 'Any type of work related training that does not take place in the workplace.')])
add(1, 11, '', 'Q11', L(1, 4, 'Outline two functions of a Trade Union:'), 10, 'business-0-14', 'trade-union-functions-2011', 4, [10],
    'Two functions at 5 marks each (3 + 2).', points('Function', 2, (3, 2)),
    ['Scheme examples: ' + S(10, 'Securing a fair wage for its members / engaging in National Agreements') + '; ' + S(10, 'Securing fair/improved working conditions for its members') + '.'])
cum(1, 12, '', 'Q12', L(1, 4, 'List three sources of household income:'), (4, 3, 3), 'business-3-16', 'household-income-sources', 4, [11],
    'Scheme sources (page 11): ' + S(11, '(i) Wages/Salary/Overtime/Bonus (ii) Social Welfare / Unemployment/Jobseeker’s Benefit / State Pension (iii) Child benefit (iv) Interest on savings (v) Dividends.'),
    noun='sources')
cum(1, 13, '', 'Q13', '\n'.join([L(1, 5, 'Column 1 is a list of business terms. Column 2 is a list of explanations for these terms. (One explanation has no match.)'),
                                 L(1, 5, '1. Credit Control', '2. Benefit-in-kind', '3. Quality Control', '4. Profit-sharing', '5. Conciliation'),
                                 L(1, 5, 'A. Aims to reduce the number of faulty products in a business.', 'B. Shares in a business are given to employees at a preferential price.',
                                   'C. A third party listens to both sides of a dispute and suggests a solution.', 'D. Aims to ensure that customers pay on time.',
                                   'E. A non-monetary reward given to an employee.', 'F. A percentage of the profits is paid to the employees.'),
                                 L(1, 5, 'Match the two lists by placing the letter of the correct explanation under the relevant number below.')]),
    (2, 2, 2, 2, 2), 'business-3-20', 'business-terms-matching-2011', 5, [11], 'Answer key (scheme page 11): 1 D; 2 E; 3 A; 4 F; 5 C. Explanation B is unused.',
    extra=['business-3-16', 'business-3-21', 'business-0-14'], noun='matches')
S(11, '1 2 3 4 5 D E A F C')
add(1, 14, '', 'Q14', L(1, 5, 'Outline two advantages of the Small Claims Court for the consumer.'), 10, 'business-0-13', 'small-claims-court-advantages', 5, [11],
    'Two advantages at 5 marks each (3 + 2).', points('Advantage', 2, (3, 2)),
    ['Scheme examples: ' + S(11, 'Provides a quick solution to consumer claims of up to €2,000') + '; ' + S(11, 'Not expensive – a fee of €15') + '.'])
cum(1, 15, '', 'Q15', L(1, 5, 'If the euro (€) falls in value against the UK (£) Sterling, indicate whether each of the following would be expected to increase or decrease:')
    + '\n' + L(1, 5, '(i) Number of UK visitors coming to Ireland') + '\n' + L(1, 5, '(ii) Irish exports to the UK'), (5, 5), 'business-6-13', 'euro-falls-against-sterling', 5, [11],
    'Answer key (scheme page 11): (i) Increase; (ii) Increase.')
S(11, '(i) Number of UK visitors coming to Ireland Increase (ii) Irish exports to the UK Increase')

# ---------------------------------------------------------------- Section 2 (75 marks each)
paula = (L(2, 6, 'Paula McCarthy received a birthday present of a new mobile phone from her parents. After one week Paula discovered that the volume control on her mobile phone did not work properly and the phone had to be recharged several times a day. Her parents told her that they had bought the phone in FonesToGo and they gave her the receipt. Her friend Mike, who had studied Business at school, explained to Paula that under the law she had the right to get a phone that was of merchantable quality, fit for its purpose and that she was entitled to redress.')
         + '\n(merchantable quality, fit for its purpose and redress are underlined.)')
law = add(2, 1, 'ai', 'Q1(A)(i)', paula + '\n\n' + L(2, 6, '(A) (i) Name the law that protects Paula McCarthy in this case.'), 10, 'business-0-13', 'law-protecting-paula',
          6, [12], 'Four words and the year at 2 marks each.', [comps('Law named', (10,), ['Four words and the year'])],
          ['Scheme: ' + S(12, 'The Sale of Goods and Supply of Services Act 1980.') + ' The allocation summary prints “' + S(5, 'Four words + year @ 2 marks each') + '”.'])
permit(law, 0, [0, 2, 4, 6, 8, 10])
add(2, 1, 'aii', 'Q1(A)(ii)', paula + '\n\n' + L(2, 6, '(ii) Explain what Paula should do to try to solve the above situation.'), 15, 'business-0-13', 'paula-complaint-steps',
    6, [12], 'Three points at 5 marks each.', points('Point', 3, (5,)),
    ['Scheme: ' + bullets(S(12, 'o Paula should call/send letter of complaint to the FonesToGo shop o Bring/enclose the receipt o Explain the problem to the shop assistant/ manager o Request / insist on a new phone or a refund.'), 'o') + '.'])
add(2, 1, 'aiii', 'Q1(A)(iii)', paula + '\n\n' + L(2, 6, '(iii) Explain the three underlined terms ‘merchantable quality’, ‘fit for its purpose’ and ‘redress’, with reference to Paula’s situation.'), 25,
    'business-0-13', 'merchantable-fit-redress', 6, [12], 'Three explanations with reference to Paula’s situation: 9 (5 + 4), 8 (4 + 4) and 8 (4 + 4).',
    unequal('Term', [(5, 4), (4, 4), (4, 4)], ['Explanation', 'Reference to Paula’s situation']),
    ['The 9-mark allowance is not tied to a particular term.',
     'Merchantable quality: ' + S(12, 'Goods should be of merchantable quality – they should be of reasonable standard/quality taking into account what they are supposed to do, their durability and price.') + ' '
     + S(12, 'The volume control on Paula’s mobile phone did not work properly'),
     'Fit for its purpose: ' + S(12, 'Goods should be fit for the purpose intended – they must do what they are sold as being capable of doing.') + ' ' + S(12, 'The phone had to be recharged several times a day'),
     'Redress: ' + S(12, 'If goods do not fulfil any one of the above, the consumer is entitled to redress or compensation.') + ' ' + S(12, 'Paula is entitled to either a refund or replacement in this situation.')])
equality = L(2, 6, 'The Employment Equality Act 1998 outlawed discrimination in the workplace and established the Equality Authority.')
cum(2, 1, 'bi', 'Q1(B)(i)', equality + '\n\n' + L(2, 6, '(B) (i) List three grounds on which discrimination is unlawful under this Act.'), (5, 5, 5), 'business-0-14', 'discrimination-grounds-2011',
    6, [12], 'Scheme grounds (page 12): ' + S(12, '(i) Gender/Male/Female (ii) Marital status (iii) Family Status (iv) Sexual orientation (v) Religious beliefs (vi) Age (vii) Race (viii) Disability (ix) Membership of traveller community.'),
    noun='grounds')
add(2, 1, 'bii', 'Q1(B)(ii)', equality + '\n\n' + L(2, 6, '(ii) Outline the role of the Equality Authority.'), 10, 'business-0-14', 'equality-authority-role',
    6, [12], 'Outline of the role: 10 marks (7 + 3).', [comps('Role of the Equality Authority', (7, 3))],
    ['Scheme examples: ' + S(12, 'To work towards the elimination of discrimination in employment') + '; ' + S(12, 'To promote equality of opportunity in employment') + '.'])

carrig = L(2, 7, 'ShopLocal in Carrig') + '\n' + L(2, 7, 'The town of Carrig has been badly affected by the recession (downturn in the economy). Several shops in the town have closed down and the number of unemployed people has doubled since 2008. Martin Power Construction Ltd, a major employer in the town, made 46 of its 80 workers redundant two years ago. A group of local business people decided to work together to support each other and to try to keep jobs in the town. They met with a representative of the local County Enterprise Board. They launched a major promotion campaign ‘ShopLocal’ to encourage local people to shop in Carrig. Martin Power Construction Ltd recently won a contract to build part of the athletes’ village for the London Olympics 2012. Martin and 20 of his former employees will work in London for a year to complete the contract.')
add(2, 2, 'a', 'Q2(A)', carrig + '\n\n' + L(2, 7, '(A) Describe three effects of the recession on the town of Carrig, using examples from the above text.'), 20, 'business-5-15',
    'recession-effects-carrig', 7, [13], 'Three effects with examples from the text: 7 (4 + 3), 7 (4 + 3) and 6 (3 + 3).',
    unequal('Effect', [(4, 3), (4, 3), (3, 3)], None),
    ['The 7-mark allowances are not tied to particular effects. Scheme examples: ' + S(13, 'Shop closures Several shops in the town have closed down More unemployment The number of unemployed people has doubled') + '.'])
add(2, 2, 'b', 'Q2(B)', carrig + '\n\n' + L(2, 7, '(B) Explain two benefits of the ‘ShopLocal’ campaign to the town of Carrig.'), 20, 'business-5-16', 'shoplocal-benefits',
    7, [13], 'Two benefits at 10 marks each (5 + 5).', points('Benefit', 2, (5, 5)),
    ['Scheme examples: ' + S(13, '(i) Local business will benefit – sales and profits increase') + '; ' + S(13, '(iii) Employment is more secure and may increase') + '.'])
add(2, 2, 'c', 'Q2(C)', carrig + '\n\n' + L(2, 7, '(C) Outline two advantages for the Irish economy of Martin Power Construction Ltd winning the contract for London Olympics 2012.'), 20,
    'business-5-15', 'olympics-contract-advantages', 7, [13], 'Two advantages at 10 marks each (5 + 5).', points('Advantage', 2, (5, 5)),
    ['Scheme examples: ' + S(13, '(iii) Corporation Tax paid on profits made by Martin Power Construction Ltd will help the Irish economy') + '; ' + S(13, '(iv) Reduction in overall unemployment as 20 workers taken on.')],
    extra=['business-6-13'])
add(2, 2, 'd', 'Q2(D)', carrig + '\n\n' + L(2, 7, '(D) Explain two services that City/County Enterprise Boards provide for businesses.'), 15, 'business-5-16', 'enterprise-board-services-2011',
    7, [13], EIGHT, eight_seven('Service'),
    [UNTIED + ' Scheme examples: ' + S(13, 'Grants – capital grants/employment grants/feasibility study grants') + '; ' + S(13, 'Mentoring Programme – an experienced business owner helps an entrepreneur overcome challenges in starting up a new business') + '.'])

recovery = L(2, 7, 'Transnational Companies, Irish-owned firms and the agricultural industry have an important role to play in the recovery of the Irish economy.')
add(2, 3, 'a', 'Q3(A)', recovery + '\n\n' + L(2, 7, '(A) Explain two benefits of the agricultural industry for the Irish economy.'), 15, 'business-5-13', 'agriculture-benefits-2011',
    7, [14], EIGHT, eight_seven('Benefit'), [UNTIED + ' Scheme examples: ' + S(14, '(i) Creates employment – about 4% of labour force') + '; ' + S(14, '(ii) Provides raw materials for the food processing industry – agribusiness') + '.'])
add(2, 3, 'b', 'Q3(B)', recovery + '\n\n' + L(2, 7, '(B) Outline three ways in which the Irish Government could help Irish business.'), 25, 'business-5-15', 'government-helps-business-2011',
    7, [14], 'Three ways: 9 (5 + 4), 8 (4 + 4) and 8 (4 + 4).', unequal('Way', [(5, 4), (4, 4), (4, 4)], None),
    ['The 9-mark allowance is not tied to a particular way. Scheme examples: ' + S(14, '(i) Grants through agencies such as Enterprise Ireland / Údarás na Gaeltachta / IDA') + '; ' + S(14, '(iii) Low tax rates – Corporation Tax / VAT reductions') + '.'])
add(2, 3, 'c', 'Q3(C)', recovery + '\n\n' + L(2, 7, '(C) Explain two reasons why transnational companies (multinational companies) locate in Ireland.'), 15, 'business-6-15', 'tnc-locate-reasons-2011',
    7, [14], EIGHT, eight_seven('Reason'), [UNTIED + ' Scheme reasons: ' + S(14, '(i) Grants from IDA Ireland (ii) Educated and skilled labour force in Ireland (iii) Gateway into EU market (iv) Low rate of Corporation Tax (v) Low level of industrial unrest.')])
fuel = L(2, 7, '(D) The Government increased taxes on petrol and diesel in its 2011 Budget.')
add(2, 3, 'di', 'Q3(D)(i)', recovery + '\n\n' + fuel + '\n' + L(2, 7, '(i) Outline one reason for this increase in taxes.'), 6, 'business-5-15', 'fuel-tax-reason',
    7, [14], 'One reason: 6 marks (3 + 3).', [comps('Reason', (3, 3))],
    ['Scheme: ' + S(14, 'The Government needs to increase tax receipts and cut expenditure to reduce its Budget deficit.')], extra=['business-3-18'])
add(2, 3, 'dii', 'Q3(D)(ii)', recovery + '\n\n' + fuel + '\n' + L(2, 7, '(ii) Describe two effects of this increase in taxes.'), 14, 'business-5-15', 'fuel-tax-effects',
    7, [14], 'Two effects at 7 marks each (4 + 3).', points('Effect', 2, (4, 3)),
    ['Scheme examples: ' + S(14, 'Transport costs increase for the general public, reducing other disposable income') + '; ' + S(14, 'Haulage and distribution costs increase, thus increasing the cost of goods') + '.'],
    extra=['business-3-18'])

jason = L(2, 8, 'Jason saw a business opportunity in January 2010 when snow and bad weather hit the country. He recognised that there was a huge demand for snow to be cleared from housing estates, pavements and private driveways. He set up in partnership with his friend Gerry. They got financial help from their parents and a loan from the bank. They imported three mini road sweeper machines from Sweden, which could be used to clear snow and ice in winter. During the major snowfall before Christmas 2010, Jason and Gerry had to employ two part-time staff to help them with the extra workload. Jason decided to attend night classes to learn more about being an employer and about taxation.')
add(2, 4, 'a', 'Q4(A)', jason + '\n\n' + L(2, 8, '(A) Outline three enterprising characteristics/skills displayed by Jason.'), 15, 'business-1-5', 'jason-enterprising-skills',
    8, [15], 'Three at 5 marks each (3 + 2).', points('Characteristic', 3, (3, 2)),
    ['Scheme examples: ' + S(15, 'Innovative / opportunistic – able to see opening for a new business') + '; ' + S(15, 'Risk-taker – set up in business with his friend Gerry / took on new staff') + '.'])
add(2, 4, 'b', 'Q4(B)', jason + '\n\n' + L(2, 8, '(B) Explain two advantages of a partnership as a form of business.'), 15, 'business-5-14', 'partnership-advantages-2011',
    8, [15], EIGHT, eight_seven('Advantage'), [UNTIED + ' Scheme examples: ' + S(15, 'More capital is available, as there are more owners / investors.') + ' ' + S(15, 'Risk is shared')])
add(2, 4, 'c', 'Q4(C)', jason + '\n\n' + L(2, 8, '(C) Outline two factors that a bank would take into account before lending to a business.'), 15, 'business-3-16', 'bank-lending-factors-2011',
    8, [15], EIGHT, eight_seven('Factor'), [UNTIED + ' Scheme factors: ' + S(15, '(i) Ability to repay / profitability (ii) Credit Rating / history / creditworthiness (iii) Details of owners + management (iv) Collateral / security for the loan / guarantee (v) Business plan / purpose of the loan (vi) Duration of the loan.')])
add(2, 4, 'd', 'Q4(D)', jason + '\n\n' + L(2, 8, '(D) Describe three responsibilities of an employer towards employees.'), 20, 'business-0-12', 'employer-responsibilities-2011',
    8, [15], 'Three responsibilities: 7 (4 + 3), 7 (4 + 3) and 6 (3 + 3).', unequal('Responsibility', [(4, 3), (4, 3), (3, 3)], None),
    ['The 7-mark allowances are not tied to particular responsibilities. Scheme examples: ' + S(15, '(i) to provide a safe and healthy working environment (ii) to pay the agreed wage for the work done (at least MWR)') + '.'])
add(2, 4, 'e', 'Q4(E)', jason + '\n\n' + L(2, 8, '(E) The following forms are used in PAYE taxation: Form P60, Form P45 and Form P21. Outline the purpose of two of these.'), 10,
    'business-3-18', 'paye-forms-choice-2011', 8, [16], 'Choose two of the three forms: the purpose of each 5 marks (3 + 2).',
    seq(comps('First form you chose', (3, 2)), comps('Second form you chose', (3, 2))),
    ['You choose which two of the three printed forms to explain. The scheme marks every choice alike (2 @ 5 each), so this is one card whichever forms you choose.',
     'Form P60 (scheme PDF page 16): “' + S(16, 'must be given by the employer to the employee at the end of the tax year') + '”; “' + S(16, 'it shows the employee gross pay for the year') + '”',
     'Form P45 (scheme PDF page 16): “' + S(16, 'must be given by the employer to the employee if an employee leaves a job / or is made redundant during the tax year') + '”',
     'Form P21 (scheme PDF page 16): “' + S(16, 'a statement of total income, tax credit and tax paid for a particular tax year') + '”'])

doyle = L(2, 8, 'Jim and Susan Doyle and their two children live in Limerick. Susan, who works as a nurse, has had a reduction in her gross pay and her net pay. Jim, a painter/decorator, was recently made redundant. They realise that they must cut down on their expenditure and have decided to prepare a household budget for the next year. They also want to review their insurance cover. Using his redundancy money, Jim wants to set up his own painting/decorating business and is thinking of leasing a van.')
add(2, 5, 'a', 'Q5(A)', doyle + '\n\n' + L(2, 8, '(A) Outline two benefits of preparing a household budget.'), 15, 'business-3-16', 'household-budget-benefits-2011',
    8, [17], EIGHT, eight_seven('Benefit'), [UNTIED + ' Scheme examples: ' + S(17, 'Plan its spending in line with its income') + '; ' + S(17, 'Identify when cash flow problems will occur') + '.'])
add(2, 5, 'b', 'Q5(B)', doyle + '\n\n' + L(2, 8, '(B) Explain one advantage and one disadvantage of leasing.'), 15, 'business-3-16', 'leasing-advantage-disadvantage',
    8, [17], 'The advantage 8 (4 + 4) and the disadvantage 7 (4 + 3).', [comps('Advantage of leasing', (4, 4), None, 1), comps('Disadvantage of leasing', (4, 3), None, 2)],
    ['Scheme: advantage ' + S(17, 'The lessee does not have to save up, use capital or borrow to buy the asset, no lump sum required') + '; disadvantage '
     + S(17, 'Usually more expensive than purchasing an asset outright') + '.'])
ins_i = L(2, 8, '(C) (i) Name three types of insurance the Doyle household might have.')
cum(2, 5, 'ci', 'Q5(C)(i)', doyle + '\n\n' + ins_i, (1, 1, 1), 'business-3-17', 'doyle-insurance-types', 8, [17],
    'Scheme types (page 17): ' + '; '.join(S(17, t) for t in ['House/Buildings Insurance', 'Contents insurance', 'Motor insurance', 'Health Insurance', 'Life Assurance']) + '.',
    noun='types')
add(2, 5, 'cii', 'Q5(C)(ii)', doyle + '\n\n' + ins_i + '\n' + L(2, 8, '(ii) Explain two of them.'), 12, 'business-3-17', 'doyle-insurance-explained',
    8, [17], 'Two explanations at 6 marks each (3 + 3).', points('Type explained', 2, (3, 3)),
    ['You explain two of the types you named. Scheme examples: ' + S(17, 'House/Buildings Insurance – provides protection against loss or damage to the structure of the building – fire, flood, storm') + '; '
     + S(17, 'Contents insurance – provides protection against loss or damage to contents caused by burglary, fire, flood') + '.'])
add(2, 5, 'di', 'Q5(D)(i)', doyle + '\n\n' + L(2, 8, '(D) (i) Outline two advantages for Jim of setting up his own business.'), 10, 'business-4-15', 'jim-own-business-advantages',
    8, [18], 'Two advantages at 5 marks each.', points('Advantage', 2, (5,)),
    ['Scheme examples: ' + S(18, 'Can earn profits/income') + '; ' + S(18, 'Put his own ideas into operation / relies on his own decisions') + '.'])
add(2, 5, 'dii', 'Q5(D)(ii)', doyle + '\n\n' + L(2, 8, '(ii) Outline two difficulties Jim might face in setting up his own business.'), 10, 'business-4-15', 'jim-own-business-difficulties',
    8, [18], 'Two difficulties at 5 marks each.', points('Difficulty', 2, (5,)),
    ['Scheme examples: ' + S(18, 'Could mean loss of personal assets e.g. house – unlimited liability') + '; ' + S(18, 'Getting finance for expansion, e.g. bank loan difficult') + '.'])
add(2, 5, 'e', 'Q5(E)', doyle + '\n\n' + L(2, 8, '(E) Explain the terms ‘gross pay’ and ‘net pay’.'), 10, 'business-3-18', 'gross-and-net-pay-2011',
    8, [18], 'Each term 5 marks.', [comps('Gross pay', (5,), None, 1), comps('Net pay', (5,), None, 2)],
    ['Scheme: ' + S(18, 'This is the total wage/salary earned before any deductions are made.') + ' ' + S(18, 'This is the take-home pay of an employee after all deductions have been made from the Gross Pay.')])

maria = L(2, 9, 'Maria’s Design Knitwear Ltd') + '\n' + L(2, 9, 'Maria has always loved designing and knitting clothes for family and friends. Over the past two years she supplied local boutiques with some of her products and they are proving to be a great success. Maria now wants to turn her hobby into a business. She has received advice from local business consultant Dermot Jones. He advised her to set up a limited company which would give her the advantage of limited liability. He also advised her to conduct market research, to decide on her advertising media, to decide on her target market and to think about a brand name.')
add(2, 6, 'a', 'Q6(A)', maria + '\n\n' + L(2, 9, '(A) What is meant by ‘the advantage of limited liability’ as referred to above?'), 10, 'business-5-14', 'limited-liability-maria',
    9, [19], 'Explanation: 10 marks (5 + 5).', [comps('Limited liability', (5, 5))],
    ['Scheme: ' + S(19, 'If a business fails / goes bankrupt, the shareholders can only lose the amount they have invested in the business.') + ' '
     + S(19, 'If she sets up a limited company, Maria cannot lose her private property to pay for the debts if the business fails.')])
research = L(2, 9, '(B) Explain the following market research terms and give one example of each:')
add(2, 6, 'bi', 'Q6(B)(i)', maria + '\n\n' + research + '\n' + L(2, 9, '(i) Field research'), 10, 'business-4-16', 'field-research-with-example-2011',
    9, [19], 'Explanation 5 (3 + 2) and one example 5.', [comps('Field research', (3, 2, 5), ['Explained', 'Explanation developed', 'Example'])],
    ['Scheme: ' + S(19, 'This involves the firm going out into the marketplace to gather new business information directly from customers.') + ' '
     + S(19, 'Examples include customer surveys (questionnaires, interviews) and observation research.')])
add(2, 6, 'bii', 'Q6(B)(ii)', maria + '\n\n' + research + '\n' + L(2, 9, '(ii) Desk research.'), 10, 'business-4-16', 'desk-research-with-example-2011',
    9, [19], 'Explanation 5 (3 + 2) and one example 5.', [comps('Desk research', (3, 2, 5), ['Explained', 'Explanation developed', 'Example'])],
    ['Scheme: ' + S(19, 'This involves research which is based on information that is already available (gathered by others) within or outside the firm.') + ' '
     + S(19, 'Examples include company files and sales records, the Internet, Central Statistics Office, magazines and trade journals, Government and other reports.')])
add(2, 6, 'c', 'Q6(C)', maria + '\n\n' + L(2, 9, '(C) Outline two benefits to Maria of having a brand name for her knitwear.'), 10, 'business-4-17', 'brand-name-benefits-maria',
    9, [19], 'Two benefits at 5 marks each.', points('Benefit', 2, (5,)),
    ['Scheme examples: ' + S(19, 'helps identify the product / it differentiates the product from other products') + '; ' + S(19, 'creates customer loyalty / easier for the customer to select the product') + '.'])
add(2, 6, 'di', 'Q6(D)(i)', maria + '\n\n' + L(2, 9, '(D) (i) Explain one function of advertising.'), 5, 'business-4-17', 'advertising-function-2011',
    9, [19], 'One function: 5 marks.', [comps('Function of advertising', (5,))],
    ['Scheme functions: ' + bullets(S(19, '• To inform / give information to consumers about product/service • To persuade consumer to purchase products • To remind consumers of continued existence of products/services')) + '.'])
add(2, 6, 'dii', 'Q6(D)(ii)', maria + '\n\n' + L(2, 9, '(ii) Describe three advertising media that Maria might consider.'), 15, 'business-4-17', 'advertising-media-maria',
    9, [19], 'Three media at 5 marks each (2 + 3).', points('Medium', 3, (2, 3)),
    ['Scheme examples: ' + S(19, 'Local newspapers – cheaper but seen by a smaller audience') + '; ' + S(19, 'Internet – international market – immediate feedback') + '.'])
tm_i = L(2, 9, '(E) (i) What is meant by the term ‘target market’?')
add(2, 6, 'ei', 'Q6(E)(i)', maria + '\n\n' + tm_i, 10, 'business-4-16', 'target-market-meaning-2011', 9, [19], 'Explanation: 10 marks (5 + 5).', [comps('Target market', (5, 5))],
    ['Scheme: ' + S(19, 'The target market is the group of people at whom a particular product or service is aimed.')])
add(2, 6, 'eii', 'Q6(E)(ii)', maria + '\n\n' + tm_i + '\n' + L(2, 9, '(ii) Name one example of a target market.'), 5, 'business-4-16', 'target-market-example-2011',
    9, [19], 'One example: 5 marks.', [single('Example', 5, 'Example named')], ['Scheme: ' + S(19, 'Any valid example, e.g. energy drinks for athletes.')])

deli = L(2, 10, 'SuperDeli') + '\n' + L(2, 10, 'SuperDeli is a successful delicatessen café set up three years ago by Martina White, a qualified chef. She spotted a gap in the market for good quality fast food for both sit down and take away customers. SuperDeli’s unique selling point (USP) is that it uses locally sourced organically produced ingredients. Martina has prepared a Business Plan and a SWOT analysis for the business. She would like to expand the business and intends to develop a website.')
swot = add(2, 7, 'a', 'Q7(A)', deli + '\n\n' + L(2, 10, '(A) Explain the term ‘SWOT analysis’.'), 20, 'business-2-13', 'swot-analysis-superdeli',
           10, [20], 'Each of the four words 2 marks, and an explanation or example for each 3 marks.',
           [comps(name, (2, 3), ['Word', 'Explanation or example'], i) for i, name in enumerate(['Strengths', 'Weaknesses', 'Opportunities', 'Threats'], 1)],
           ['The allocation summary prints “' + S(8, 'SWOT analysis: Four words @ 2 marks each Explanation or example in each case @ 3 marks each') + '”.',
            'Scheme: ' + S(20, 'Strengths: The internal good points of the business which give it an advantage e.g. organising skills, USP.') + ' '
            + S(20, 'Threats: Factors which are external to the business and may pose problems in the future and reduce profits e.g. competition, costs of organic food, downturn in the economy.')])
for i in range(4):
    permit(swot, i, [0, 2], 0)
add(2, 7, 'b', 'Q7(B)', deli + '\n\n' + L(2, 10, '(B) Outline two benefits of preparing a business plan.'), 10, 'business-4-15', 'business-plan-benefits-2011',
    10, [20], 'Two benefits at 5 marks each.', points('Benefit', 2, (5,)),
    ['Scheme examples: ' + S(20, 'To obtain finance from lenders') + '; ' + S(20, 'To give documentary evidence of the viability of the business idea.')])
add(2, 7, 'ci', 'Q7(C)(i)', deli + '\n\n' + L(2, 10, '(C) (i) Outline two advantages for SuperDeli of having a website.'), 10, 'business-2-12', 'website-advantages-superdeli',
    10, [20], 'Two advantages at 5 marks each.', points('Advantage', 2, (5,)),
    ['Scheme examples: ' + bullets(S(20, 'Method of advertising/selling • Worldwide market 24/7 • Increased sales/profits')) + '.'])
add(2, 7, 'cii', 'Q7(C)(ii)', deli + '\n\n' + L(2, 10, '(ii) Explain two challenges of the internet for business.'), 10, 'business-2-12', 'internet-challenges-2011',
    10, [20], 'Two challenges at 5 marks each.', points('Challenge', 2, (5,)),
    ['Scheme examples: ' + bullets(S(20, 'Risks of viruses etc that can damage IT systems • Cost of setting up / maintaining website • Staff need to be trained in IT skills')) + '.'])
margaret = (L(2, 10, 'Margaret Moran is the Human Resource Manager at SuperDeli and her current task is to recruit a Marketing Manager. The ideal candidate must have a marketing degree and a minimum of three years management experience. SuperDeli would like suitably qualified persons with experience in internet selling to apply. Knowledge of the catering industry is desirable and the ability to work as part of a team is essential. Applications are to be returned by 30 June 2011 to:')
            + '\n' + L(2, 10, 'Ms. Margaret Moran Human Resource Manager SuperDeli 63 Main Street Cork.').replace(' Human', '\nHuman').replace(' SuperDeli', '\nSuperDeli').replace(' 63', '\n63').replace(' Cork', '\nCork'))
add(2, 7, 'di', 'Q7(D)(i)', deli + '\n\n' + margaret + '\n\n' + L(2, 10, '(D) (i) Draft a suitable newspaper advertisement seeking a Marketing Manager.'), 15, 'business-3-20',
    'marketing-manager-advertisement', 10, [21], 'Background 3 (set-up, fast food, organic), vacancy 1, qualifications 8 (degree, management experience, internet selling, knowledge, team player) and application 3 (deadline, name, address).',
    [response(1, 'Newspaper advertisement', [('background', 'Background: set-up, fast food, organic', 3), ('vacancy', 'Vacancy: Marketing Manager', 1),
                                             ('qualifications', 'Qualifications: degree, management experience, internet selling, knowledge, team player', 8),
                                             ('application', 'Application: deadline, name, address', 3)])],
    ['The allocation summary prints “' + S(8, 'Background: set-up, fast food, organic 3m Vacancy: Marketing Manager 1m Qualifications: degree, management experience, internet selling, knowledge, team player 8m Application: deadline, name, address. 3m') + '”.',
     'Scheme sample (page 21): ' + S(21, 'SuperDeli Vacancy for Marketing Manager SuperDeli is a successful delicatessen café established in Cork in 2008.') + ' ...'],
    extra=['business-2-12'])
L(2, 10, '(ii) Outline two advantages of teamwork in a business.')
add(2, 7, 'dii', 'Q7(D)(ii)', deli + '\n\n' + margaret + '\n\n' + L(2, 10, '(ii) Outline two advantages of teamwork in a business.'), 10, 'business-3-20', 'teamwork-advantages-2011',
    10, [21], 'Two advantages at 5 marks each (3 + 2).', points('Advantage', 2, (3, 2)),
    ['Scheme examples: ' + S(21, '(ii) Improved decision making because of a wider range of views') + '; ' + S(21, '(iv) Support – team members share the responsibility and can help each other') + '.'])

brady = L(2, 11, 'Brady’s Hotel') + '\n' + L(2, 11, 'Brady’s Hotel is a family run business situated in a seaside town. It provides accommodation, restaurant and bar services. Mark Brady has overall responsibility for managing the hotel. He wants to upgrade the hotel. Despite his plans for the hotel, Mark has noticed that some of the hotel staff lack motivation. His focus now is to try and improve staff motivation.')
add(2, 8, 'a', 'Q8(A)', brady + '\n\n' + L(2, 11, '(A) Explain two benefits of upgrading Brady’s hotel.'), 15, 'business-4-18', 'hotel-upgrade-benefits',
    11, [22], EIGHT, eight_seven('Benefit'), [UNTIED + ' Scheme examples: ' + S(22, '(ii) They can attract new customers and possibly target different markets') + '; ' + S(22, '(iii) Better able to compete with other hotels') + '.'])
add(2, 8, 'b', 'Q8(B)', brady + '\n\n' + L(2, 11, '(B) Outline three methods that Mark could use to improve staff motivation.'), 20, 'business-2-11', 'hotel-staff-motivation',
    11, [22], 'Three methods: 7, 7 and 6.', unequal('Method', [(7,), (7,), (6,)], None),
    ['The 7-mark allowances are not tied to particular methods. Scheme examples: ' + bullets(S(22, '• Look for opportunities to praise their work • Delegate greater authority to staff • Give them a financial reward – bonus, profit sharing scheme')) + '.'])
# The pyramid is an image (no text layer); its five printed labels, read from the rendered page, top to bottom.
maslow = L(2, 11, '(C) Maslow’s Hierarchy of Needs is presented below.') + '\n(Pyramid, top to bottom: 5 | Esteem Needs | 3 | 2 | Physical Needs)'
cum(2, 8, 'ci', 'Q8(C)(i)', brady + '\n\n' + maslow + '\n' + L(2, 11, '(i) List levels 2, 3 and 5 (in your answer book).'), (4, 3, 3), 'business-2-11', 'maslow-levels-two-three-five',
    11, [22], 'Answer key (scheme page 22): ' + S(22, 'Level 2: Safety/Security needs Level 3: Social needs Level 5: Self-actualisation needs') + '.', noun='levels')
add(2, 8, 'cii', 'Q8(C)(ii)', brady + '\n\n' + maslow + '\n' + L(2, 11, '(ii) Briefly explain two of the five levels.'), 10, 'business-2-11', 'maslow-levels-choice-2011',
    11, [22], 'Choose two of the five levels: each 5 marks (3 + 2).', seq(comps('First level you chose', (3, 2)), comps('Second level you chose', (3, 2))),
    ['You choose which two of the five levels to explain. The scheme marks every choice alike (2 @ 5 each), so this is one card whichever levels you choose.',
     'Physical Needs (scheme PDF page 22): “' + S(22, 'the need for food, clothing, shelter and warmth, fair pay/wage.') + '”',
     'Safety/Security Needs (scheme PDF page 22): “' + S(22, 'the need for job security / safe working conditions.') + '”',
     'Social Needs (scheme PDF page 22): “' + S(22, 'the need to be accepted by fellow workers / peers') + '”',
     'Esteem Needs (scheme PDF page 22): “' + S(22, 'the need to be respected and given recognition by superiors') + '”',
     'Self-actualisation Needs (scheme PDF page 22): “' + S(22, 'the need for people to achieve their potential and be the best they can be – self-fulfilment, job satisfaction.') + '”'])
balance = (L(2, 11, '(D) Use the information in the table below and answer the questions which follow:') + '\n' + L(2, 11, 'BALANCE SHEET – Brady’s Hotel (Extract)')
           + '\n| 2010 € | 2009 €\nCurrent Assets | 900,000 | 800,000\nCurrent Liabilities | 500,000 | 400,000')
L(2, 11, '2010 2009 € € Current Assets 900,000 800,000 Current Liabilities 500,000 400,000')
wcr_i = L(2, 11, '(i) Calculate the Working Capital Ratio for 2010 and 2009. (Show the formula and all your workings.)')
add(2, 8, 'di', 'Q8(D)(i)', brady + '\n\n' + balance + '\n' + wcr_i, 16, 'business-3-19', 'brady-working-capital-ratio',
    11, [22], 'Formula 4 and each of the two ratios 6.',
    [response(1, 'Working Capital Ratio', [('formula', 'Formula: Current Assets : Current Liabilities', 4), ('ratio-2010', '2010: 1.8 : 1', 6), ('ratio-2009', '2009: 2 : 1', 6)])],
    ['Scheme (page 22): ' + S(22, 'Formula: Current Assets : Current Liabilities Workings: 2010 2009 900,000 : 500,000 800,000 : 400.000 1.8 : 1 2 : 1') + '.',
     'The allocation summary prints “' + S(8, '(i) Formula @ 4 marks Two ratios @ 6 marks each') + '”.'])
add(2, 8, 'dii', 'Q8(D)(ii)', brady + '\n\n' + balance + '\n' + wcr_i + '\n' + L(2, 11, '(ii) Explain whether the ratio has improved or disimproved.'), 4, 'business-3-19',
    'brady-ratio-trend', 11, [22], 'One explanation: 4 marks.', [comps('Explanation', (4,))],
    ['Scheme: ' + S(22, 'The ratio has disimproved from a WCR of 2:1 (ideal ratio) in 2009 to 1.8:1 in 2010.')])

# ---------------------------------------------------------------- checks and write-out
qn = lambda c: c['questionRef'].split(' Q')[1].split('(')[0]
for section, count, total in [('1', 15, 10), ('2', 8, 75)]:
    for q in range(1, count + 1):
        got = sum(c['totalMarks'] for c in P.created if c['section'] == section and qn(c) == str(q))
        assert got == total, (section, q, got)
assert not [i for i in ORIGINAL if i.startswith('bus-2011-ol-')]
assert not P.pools

SELECTION = {
    1: 'No finite printed answer menu occurs in Section 1 (answer ten of fifteen at 10 marks). TRUE/FALSE in Q7, the matching rows in Q13 and increase/decrease in Q15 are required answer formats. Support-note lists are open examples.',
    2: 'Two printed choices are one card each (the scheme marks every choice alike under one topic): Q4(E) the purpose of two of three PAYE forms and Q8(C)(ii) any two of the five levels of Maslow’s hierarchy. Q5(C)(ii) asks the candidate to explain two of the insurance types they named; the list is their own. Sub-parts with their own published marks are separate cards. Support-note lists are open examples.',
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
    if m == 'two of' and own(w, m, 'Outline the purpose of two of these'):
        return 'finite-choice', 'Section 2 Q4(E) asks for the purpose of two of the three printed PAYE forms (P60, P45, P21). The scheme marks every choice alike (5 each), so one card carries all three with the scheme wording for each.', 'bus-2011-ol-s2-q4e'
    if m == 'two of' and own(w, m, 'Briefly explain two of the five levels'):
        return 'finite-choice', 'Section 2 Q8(C)(ii) asks for any two of the five levels of Maslow’s hierarchy. The scheme marks every choice alike (5 each), so one card carries all five with the scheme wording for each.', 'bus-2011-ol-s2-q8cii'
    if m in ('46 of', '20 of') and (own(w, m, 'made 46 of its 80 workers') or own(w, m, 'Martin and 20 of his former employees')):
        return 'case-context', 'Figures inside the Section 2 Q2 extract (46 of 80 workers made redundant; 20 former employees), not a choice of task.', None
    if m == 'or' and own(w, m, 'improved or disimproved'):
        return 'required-headings', 'Section 2 Q8(D)(ii) requires a determination of whether the ratio improved or disimproved; it is one required answer, not a choice of task.', None
    if m == 'two of' and own(w, m, 'Explain two of them'):
        return 'open-response', 'Section 2 Q5(C)(ii) asks the candidate to explain two of the three insurance types they named in (i); the list is their own and the scheme marks any type alike, so it is one card.', None
    if m == 'or' and (own(w, m, 'TRUE or FALSE') or own(w, m, 'True or False')):
        return 'required-headings', 'TRUE/FALSE are answer labels for each of the five required statements in Section 1 Q7, not optional tasks.', None
    if m == 'or' and (own(w, m, 'increase or decrease') or own(w, m, 'Increase or decrease')):
        return 'required-headings', 'Increase/decrease are answer labels for both required rows in Section 1 Q15, not optional tasks.', None
    assert (fileid, page) in {('LC033GLP000EV', 1), ('LC033GLP000EV', 6)} and m in ('either', 'or'), (fileid, page, m, w)
    return 'exam-navigation', 'The cover and Section 2 rubrics set how many whole questions a candidate answers (one from Part 1, two from Part 2 and one other from either part). Every numbered question remains in the practice corpus as separate cards.', None


n = P.write([(1, range(1, 16)), (2, range(1, 9))], SELECTION, classify,
            'Every part of {year} Ordinary Section {section} Question {q} was visually checked against its SEC paper, allocation summary and support notes. The single-booklet identity keeps the short (n) and long (S2Q) question numbering apart.')
print(f'Reviewed {len(P.created)} 2011 Ordinary tasks; classified {n} raw selection matches.')
