"""Review the 2015 Ordinary English paper (one booklet: Section 1 and Section 2).

2015: answer ten of fifteen short questions at 10 marks and four of eight
long questions at 75 (one from Part 1, two from Part 2 and one other), all in
one twelve-page booklet (LC033GLP000EV, the same file id as its scheme). No
Ordinary card existed for 2015, so every card is new. The allocation summary
(scheme pages 4-8) sets each boundary; printed sub-parts with their own
published marks are separate cards. One printed choice is one card: Section 2
Q5(B) any two of three principles of insurance (the scheme marks every choice
alike, 10 each).
"""
from bus_lib import (Paper, ORIGINAL, comps, points, seq, unequal, single, response, fixed, permit)

T = {(1, q): 4 for q in range(1, 16)}
T.update({(2, 1): 5, (2, 2): 5, (2, 3): 6, (2, 4): 6, (2, 5): 7, (2, 6): 7, (2, 7): 8, (2, 8): 8})
P = Paper(2015, 'ordinary', {1: 'LC033GLP000EV', 2: 'LC033GLP000EV'}, 'LC033GLP000EV', T)
L, S, add, cum = P.lift, P.scheme, P.add, P.cumulative
EIGHT = 'Two points are required: 8 (4 + 4) and 7 (4 + 3).'
UNTIED = 'The 8-mark allowance is not tied to a particular point.'


def eight_seven(label):
    return unequal(label, [(4, 4), (4, 3)], None)


def eight53(label):
    return unequal(label, [(5, 3), (5, 2)], None)


def flat(card):
    for r in card['rubric']['responses']:
        for a in r['allocations']:
            a['permittedMarks'] = [0, a['maxMarks']]
    return card


def evens(card, index=0):
    top = card['rubric']['responses'][index]['allocations'][0]['maxMarks']
    return permit(card, index, list(range(0, top + 1, 2)))


def bullets(text, sep='; '):
    return sep.join(x.strip() for x in text.split('•') if x.strip())


# ---------------------------------------------------------------- Section 1 (10 marks each)
add(1, 1, '', 'Q1', L(1, 2, 'What do the following letters stand for? (Write each answer in the space provided.)', 'ATM PIN DIRT').replace(' PIN', '\nPIN').replace(' DIRT', '\nDIRT'),
    10, 'business-3-16', 'abbreviations-atm-pin-dirt', 2, [9], 'The first and second correct terms earn 3 each (1 + 1 + 1); the third 4 (1 + 1 + 1 + 1).',
    [comps('First correct term', (3,), ['Words written in full'], 1), comps('Second correct term', (3,), ['Words written in full'], 2),
     comps('Third correct term', (4,), ['Words written in full'], 3)],
    ['Answer key: ATM ' + S(9, 'Automated Teller Machine') + '; PIN ' + S(9, 'Personal Identification Number') + '; DIRT ' + S(9, 'Deposit Interest Retention Tax') + '.'],
    extra=['business-3-18'])
add(1, 2, '', 'Q2', L(1, 2, 'Explain the following entrepreneurial characteristics:', '(i) Innovative:', '(ii) Risk taker:'), 10, 'business-1-5',
    'innovative-and-risk-taker', 2, [9], 'Each explanation 5 marks (3 + 2).', [comps('Innovative', (3, 2), i=1), comps('Risk taker', (3, 2), i=2)],
    ['Scheme: ' + S(9, 'Seeing new ways of doing things, coming up with new ideas, identifying solutions to problems.') + ' '
     + S(9, 'A person willing to take a chance in setting up a business.')])
cum(1, 3, '', 'Q3', L(1, 2, 'Complete the following table, which refers to examples of Promotion Techniques, by placing a tick (✓) in the correct box for each example.',
                      'Promotion Techniques Examples Advertising Sales Promotion Public Relations', 'Buy One Get One Free Billboards Press Conference Free Samples'),
    (3, 3, 2, 2), 'business-4-17', 'promotion-technique-ticks', 2, [9],
    'Answer key (ticks on scheme page 9): Buy One Get One Free Sales Promotion; Billboards Advertising; Press Conference Public Relations; Free Samples Sales Promotion.',
    noun='ticks')
add(1, 4, '', 'Q4', L(1, 2, 'Explain the term ‘Limited Liability’.'), 10, 'business-5-14', 'limited-liability-explained-2015', 2, [9], 'Explanation: 10 marks (5 + 5).',
    [comps('Limited liability', (5, 5))],
    ['Scheme: ' + S(9, 'Limited Liability means that if a company goes bankrupt the owners of the company are not responsible for all the debts of the company')])
cum(1, 5, '', 'Q5', L(1, 3, 'Name two European Union (EU) institutions:'), (5, 5), 'business-6-14', 'eu-institutions-2015', 3, [9],
    'Scheme institutions (page 9): European Parliament, European Commission, European Court of Justice, Council of the EU (Council of Ministers), European Court of Auditors, European Central Bank.',
    noun='institutions')
S(9, 'European Parliament European Commission European Court of Justice')
L(1, 3, 'Net Profit €110,000 Sales €880,000 Net Profit Margin Answer:')
flat(add(1, 6, '', 'Q6', L(1, 3, 'The following information is available from the final accounts of Brandon Ltd on 31/12/2014: Calculate the Net Profit Margin. (Show your workings.)')
         + '\nNet Profit €110,000\nSales €880,000\nNet Profit Margin Answer: ______%', 10, 'business-3-19', 'net-profit-margin-brandon', 3, [10],
         'Formula 4, the two figures 2 each and the answer 2.',
         [response(1, 'Net profit margin', [('formula', 'Formula: Net Profit / Sales x 100', 4), ('net-profit', '€110,000', 2), ('sales', '€880,000', 2), ('answer', '12.5%', 2)])],
         ['Scheme (page 10): ' + S(10, 'Net Profit Margin: NP x 100 = 110,000 x 100 = 12.5%') + ' (Net Profit over Sales, 110,000 over 880,000); ' + S(10, 'Formula: 4 Figures: 2 x 2 Answer: 2') + '.']))
cum(1, 7, '', 'Q7', L(1, 3, 'List two grounds under the Law of Contract, where a person has the Capacity to Contract (i.e. to enter into a legal contract).'), (5, 5), 'business-0-12',
    'capacity-to-contract-grounds', 3, [10], 'Scheme grounds (page 10): ' + bullets(S(10, '• over 18 • not under the influence of alcohol/drugs • of sound mind')) + '.', noun='grounds')
add(1, 8, '', 'Q8', L(1, 3, 'Choose the appropriate words to complete the sentence below (one word does not apply):', 'Standardised Strategic Single')
    + '\nGlobal businesses view the world as one ______ ' + L(1, 3, 'market and use a global or adapted marketing mix to sell a') + ' ______ product.', 10, 'business-6-15',
    'global-business-word-bank', 3, [10], 'Each blank earns 5 marks.', [fixed('Completed blanks', [('First blank', 5), ('Second blank', 5)])],
    ['Answer key (scheme page 10): ' + S(10, 'Global businesses view the world as one SINGLE market and use a global or adapted marketing mix to sell a STANDARDISED product.') + ' Strategic is not used.'])
L(1, 3, 'Global businesses view the world as one')
cum(1, 9, '', 'Q9', L(1, 3, 'State TRUE or FALSE after each of the following statements on Theories of Motivation:', 'McGregor’s Theory on motivation is known as Theory X and Theory Y.',
                      'Physiological/Physical needs relate to the need for a safe secure job.', 'Highly motivated employees lead to low productivity in the workplace.',
                      'Social/Acceptance needs relate to the need for food and shelter.', 'Maslow believed that as one need is satisfied the next becomes the motivator.'),
    (2, 2, 2, 2, 2), 'business-2-11', 'motivation-true-false', 3, [10], 'Answer key (scheme page 10): TRUE; FALSE; FALSE; FALSE; TRUE.')
S(10, 'McGregor’s Theory on motivation is known as Theory X and Theory Y. TRUE')
add(1, 10, '', 'Q10', L(1, 4, 'Outline the purpose of the following insurance forms:', '(i) Proposal Form:', '(ii) Claim Form:'), 10, 'business-3-17', 'proposal-and-claim-forms',
    4, [10], 'Each purpose 5 marks (3 + 2).', [comps('Proposal Form', (3, 2), i=1), comps('Claim Form', (3, 2), i=2)],
    ['Scheme: ' + S(10, 'This is an application form that must be completed by a person who wishes to take out an insurance policy.') + ' '
     + S(10, 'If an insured loss is suffered, the insured completes this document when seeking compensation')])
cum(1, 11, '', 'Q11', L(1, 4, 'Complete the break-even chart below by placing the following labels in the correct position on the chart:', 'Fixed Costs (FC) Total Revenue (TR) Break-even Point (BEP)')
    + '\n(Break-even chart: costs/revenue € on the vertical axis (100,000 and 25,000 marked) against output in units (0, 10,000, 20,000); a horizontal line at €25,000, a rising line from €25,000 labelled ' + L(1, 4, 'TC (Total Costs)')
    + ', and a steeper line rising from 0 that crosses it — see the printed page.)', (4, 3, 3), 'business-3-19', 'break-even-chart-labels', 4, [11],
    'Answer key (chart on scheme page 11): TR (Total Revenue) on the steeper line from 0; FC (Fixed Costs) on the horizontal line at €25,000; BEP where TR crosses TC.', noun='labels')
cum(1, 12, '', 'Q12', L(1, 4, 'List the three missing elements of the Marketing Mix:') + '\n(i) ______\n(ii) ______\n(iii) ______\n(iv) ' + L(1, 4, 'PLACE'), (4, 3, 3), 'business-4-17',
    'missing-marketing-mix-elements', 4, [11], 'Answer key (scheme page 11): ' + S(11, 'PRODUCT PRICE PROMOTION') + ' (Place is printed).', noun='elements')
cum(1, 13, '', 'Q13', '\n'.join([L(1, 5, 'Column 1 is a list of business terms. Column 2 is a list of possible explanations for these terms. (One explanation has no match.) Match the two lists by placing the letter of the correct explanation under the relevant number below.'),
                                 L(1, 5, '1. Shareholders', '2. Interest Groups', '3. Board of Directors', '4. Consumers', '5. Suppliers'),
                                 L(1, 5, 'A. Buy goods and services for their own use.', 'B. Is involved with planning, organising and controlling activities within a business on a daily basis.',
                                   'C. Provide raw materials required for the production of goods.', 'D. Represent people with a common interest and lobby business on their behalf.',
                                   'E. Oversees the operations/activities of a company.', 'F. Invest money in a business and become owners.')]),
    (2, 2, 2, 2, 2), 'business-0-12', 'stakeholder-terms-matching-2015', 5, [11], 'Answer key (scheme page 11): 1 F; 2 D; 3 E; 4 A; 5 C. Explanation B is unused.', noun='matches')
S(11, '1 2 3 4 5 F D E A C')
add(1, 14, '', 'Q14', L(1, 5, 'Tick the correct box (✓) to indicate the Act which governs how information is stored about people:', 'Consumer Protection Act 2007 Data Protection Act 1988/2003').replace(' Data Protection', '\nData Protection'),
    10, 'business-2-12', 'data-protection-act-tick', 5, [11], 'The correct box earns 10 marks.', [single('Correct box', 10, 'Act ticked')],
    ['Answer key (tick on scheme page 11): Data Protection Act 1988/2003.'], extra=['business-0-12'])
cum(1, 15, '', 'Q15', L(1, 5, 'Complete the functional organisation structure of a Private Limited Company with four departments:')
    + '\n(Chart: ' + L(1, 5, 'BOARD OF DIRECTORS') + ' at the top; one empty box below it; four department boxes below that, one printed ' + L(1, 5, 'PRODUCTION') + '.)',
    (3, 3, 2, 2), 'business-2-13', 'functional-structure-complete', 5, [11],
    'Answer key (chart on scheme page 11): ' + S(11, 'CEO / MD') + ' under the Board of Directors; departments ' + S(11, 'HR / ICT') + ', Production (printed), Marketing/Sales and ' + S(11, 'PURCHASING') + '.',
    noun='boxes')

# ---------------------------------------------------------------- Section 2 (75 marks each)
ava = L(2, 6, 'Headline') + '\n' + L(2, 6, 'Ava Darcy purchased headphones from Headline Electronic store for €195.99. After two weeks the speaker in her left ear started to skip and then stopped completely. She returned to the store to complain as the headphones were not of merchantable quality.')
law = add(2, 1, 'a', 'Q1(A)', ava + '\n\n' + L(2, 6, '(A) State the law that protects Ava in this case.'), 10, 'business-0-13', 'law-protecting-ava', 6, [12],
          'Name the Act: 5 @ 2 marks.', [comps('Consumer law', (10,), ['Act named'])],
          ['Answer: ' + S(12, 'Sale of Goods and Supply of Services Act 1980') + ' (scheme: ' + S(5, 'Sale (2) of Goods (2) and Supply (2) of Services (2) Act 1980 (2)') + ').'])
evens(law)
add(2, 1, 'b', 'Q1(B)', ava + '\n\n' + L(2, 6, '(B) Outline two forms of redress that Ava is entitled to in the above case.'), 15, 'business-0-13', 'ava-redress',
    6, [12], EIGHT, eight_seven('Form of redress'), [UNTIED])
add(2, 1, 'c', 'Q1(C)', ava + '\n\n' + L(2, 6, '(C) Explain two benefits of Ava taking her case to the Small Claims Court.'), 15, 'business-0-13', 'ava-small-claims-benefits',
    6, [12], EIGHT, eight_seven('Benefit'), [UNTIED])
ads = L(2, 6, 'Hotel Receptionist required - must be Irish and speak fluent English', 'Van driver needed to deliver goods across Ireland – male driver preferable')
add(2, 1, 'd', 'Q1(D)', L(2, 6, '(D) Outline two reasons why the advertisements below are unlawful under the Employment Equality Act 1998.') + '\n1. ' + ads.replace('\n', '\n2. '), 15,
    'business-0-14', 'unlawful-job-advertisements', 6, [12], EIGHT, eight_seven('Reason'),
    [UNTIED, 'Scheme: ' + S(12, 'It is illegal to discriminate against someone based on their race/nationality') + '; ' + S(12, 'It is illegal to discriminate on the basis of a person’s gender') + '.'])
union_i = L(2, 6, '(E) (i) Outline two benefits to an employee of being a member of a Trade Union.')
add(2, 1, 'ei', 'Q1(E)(i)', union_i, 15, 'business-0-14', 'trade-union-membership-benefits-2015', 6, [12], 'Two benefits: 8 and 7.', unequal('Benefit', [(8,), (7,)], None),
    ['The 8-mark allowance is not tied to a particular benefit.'])
add(2, 1, 'eii', 'Q1(E)(ii)', union_i + '\n' + L(2, 6, '(ii) State one example of a Trade Union in Ireland.'), 5, 'business-0-14', 'irish-trade-union-example',
    6, [12], 'One example: 5 marks.', [single('Trade union', 5, 'Union named')], ['Scheme examples: ' + S(12, 'SIPTU TUI INMO ASTI INTO Impact').replace(' ', ', ') + '.'])

mncs = L(2, 7, 'Google, Facebook, Twitter and many other large organisations in the Tertiary (Services) sector have set up European headquarters in Ireland. IDA Ireland is the state agency responsible for attracting Multinational Companies (MNCs) to Ireland.')
add(2, 2, 'a', 'Q2(A)', mncs + '\n\n' + L(2, 7, '(A) Name the two other sectors/categories of industry and state one example of each.'), 15, 'business-5-13', 'other-sectors-with-examples',
    7, [13], 'Each sector named 5; the examples 3 and 2.', unequal('Sector', [(5, 3), (5, 2)], ['Sector named', 'Example']),
    ['The 3-mark example is not tied to a particular sector. Scheme: ' + S(13, 'Primary Sector – Extractive industries') + '; ' + S(13, 'Secondary Sector – Manufacturing & Construction')])
factors = add(2, 2, 'b', 'Q2(B)', mncs + '\n\n' + L(2, 7, '(B) List the four factors of production and explain one of them.'), 15, 'business-1-5', 'factors-listed-one-explained',
              7, [13], 'Four factors at 2 marks each and one explained for 7 (4 + 3).',
              seq(comps('Factors of production listed', (8,), ['Land, labour, capital and enterprise']), comps('One factor explained', (4, 3))),
              ['Scheme: ' + S(13, 'Factors: 4 x 2m Explanation 7m (4 + 3)') + '. Example: ' + S(13, 'LAND: All natural resources used in the production process')])
evens(factors)
add(2, 2, 'c', 'Q2(C)', mncs + '\n\n' + L(2, 7, '(C) Outline three reasons why Multinational Companies (MNCs) locate in Ireland.'), 20, 'business-6-15', 'why-mncs-locate-2015',
    7, [13], 'Three reasons: 7 (5 + 2), 7 (5 + 2) and 6 (5 + 1).', unequal('Reason', [(5, 2), (5, 2), (5, 1)], None),
    ['The 7/7/6 sequence prices the three reasons, not particular reasons.'])
add(2, 2, 'd', 'Q2(D)', mncs + '\n\n' + L(2, 7, '(D) Explain one service provided by IDA Ireland to foreign MNCs.'), 10, 'business-5-15', 'ida-service-explained',
    7, [13], 'One service: 10 marks (6 + 4).', [comps('IDA service', (6, 4))],
    ['Scheme examples: ' + S(13, 'Provides funding (grants etc.) to MNCs locating in Ireland')], extra=['business-6-15'])
add(2, 2, 'e', 'Q2(E)', mncs + '\n\n' + L(2, 7, '(E) Outline two benefits MNCs bring to the Irish economy.'), 15, 'business-6-15', 'mnc-benefits-2015',
    7, [13], 'Two benefits: 8 (5 + 3) and 7 (5 + 2).', eight53('Benefit'), [UNTIED])

spend = (L(2, 7, 'Irish Government Expenditure in 2015', 'The pie chart below, shows the proposed Government expenditure for 2015 on the five largest areas of expenditure:')
         + '\n(Pie chart: ' + L(2, 7, 'Social Protection/ Welfare €19,400m') + '; Health €13,000m; Education & Skills €8,300m; Justice €2,100m; Agriculture €1,000m.)')
cum(2, 3, 'a', 'Q3(A)', spend + '\n\n' + L(2, 7, '(A) List two examples of Government expenditure on Education.'), (5, 5), 'business-5-15', 'education-expenditure-examples-2015',
    7, [14], 'Scheme examples (page 14): ' + bullets(S(14, '• Teachers’ salaries • Building schools • Extending schools • Education initiatives')) + '.', noun='examples')
add(2, 3, 'b', 'Q3(B)', spend + '\n\n' + L(2, 7, '(B) Outline two reasons for the high level of expenditure on Social Protection/Welfare.'), 15, 'business-5-15', 'social-protection-spending-reasons',
    7, [14], EIGHT, eight_seven('Reason'), [UNTIED])
cum(2, 3, 'c', 'Q3(C)', spend + '\n\n' + L(2, 7, '(C) List three taxes collected by the Government.'), (5, 5, 5), 'business-3-18', 'government-taxes-listed',
    7, [14], 'Scheme examples (page 14): ' + bullets(S(14, '• VAT • Income Tax (PAYE) • Corporation Tax • Motor Tax • Property Tax • Capital Gains Tax • Capital Acquisitions Tax • DIRT')) + '.', noun='taxes')
add(2, 3, 'd', 'Q3(D)', spend + '\n\n' + L(2, 7, '(D) Outline two effects on the Government’s Budget of a growth in employment.'), 15, 'business-5-15', 'employment-growth-budget-effects',
    7, [14], EIGHT, eight_seven('Effect'), [UNTIED])
add(2, 3, 'e', 'Q3(E)', spend + '\n\n' + L(2, 7, '(E) Explain two benefits increased employment brings to a local community.'), 20, 'business-5-16', 'employment-local-community-benefits',
    7, [14], 'Two benefits at 10 marks each (5 + 5).', points('Benefit', 2, (5, 5)))

ashfield = L(2, 8, 'Ashfield Tidy Towns') + '\n' + L(2, 8, 'The people of Ashfield Village have decided to enter the National Tidy Towns competition, after it was suggested by local entrepreneur Alice Fitzgerald. Due to her democratic leadership style, Alice was appointed Chairperson of the Tidy Towns Committee and she will lead all volunteer teams in achieving the committee’s objectives. The next monthly meeting of the committee will be held on Friday 26th June 2015 at 7.30 pm, in Ashfield Community Centre, to discuss sources of finance for improvements to the local park.')
add(2, 4, 'a', 'Q4(A)', ashfield + '\n\n' + L(2, 8, '(A) Outline the role of an entrepreneur.'), 10, 'business-1-5', 'entrepreneur-role', 8, [15], 'One outline: 10 marks (4 + 4 + 2).',
    [comps('Role of an entrepreneur', (4, 4, 2))], ['Scheme: ' + S(15, 'An Entrepreneur is a person who identifies a business opportunity (product or service) and undertakes the risks of establishing it.')])
add(2, 4, 'b', 'Q4(B)', ashfield + '\n\n' + L(2, 8, '(B) Outline how Alice’s enterprising skills/characteristics could benefit Ashfield Tidy Towns Committee.'), 15, 'business-1-5',
    'alice-enterprising-skills', 8, [15], 'Three at 5 marks each (3 + 2).', points('Skill', 3, (3, 2)))
add(2, 4, 'c', 'Q4(C)', ashfield + '\n\n' + L(2, 8, '(C) Explain the difference between a democratic and an autocratic leader.'), 15, 'business-2-11', 'democratic-versus-autocratic',
    8, [15], 'Two explanations: 8 (4 + 4) and 7 (4 + 3).', unequal('Explanation', [(4, 4), (4, 3)], None),
    ['The 8-mark allowance is not tied to either style. The allocation summary prints “' + S(6, '8 marks (2 @ 4m) 7 marks (1 @4m) + (1 @ 3m)') + '”.'])
flat(add(2, 4, 'd', 'Q4(D)', ashfield + '\n\n' + L(2, 8, '(D) Draft the Notice and Agenda of the Ashfield Tidy Towns Committee meeting, sent by the Secretary, Brian O’Donnell. (The Agenda must contain at least four items.)'), 20,
         'business-2-12', 'tidy-towns-notice-and-agenda', 8, [16], 'Notice 10 (the five bold terms at 2 each), agenda 8 (the two bold items and two others at 2 each), signature 1 and title 1.',
         seq(comps('Notice', (2, 2, 2, 2, 2), ['Ashfield Tidy Towns Committee', 'Monthly meeting', 'Friday 26th June 2015', '7.30 p.m.', 'Ashfield Community Centre']),
             comps('Agenda', (2, 2, 2, 2), ['Minutes of previous meeting', 'Sources of finance for improvement to the local park', 'Another item', 'Another item']),
             comps('Signature', (1, 1), ['Signed (Brian O’Donnell)', 'Title (Secretary)'])),
         ['Scheme (page 16): ' + S(16, 'The next monthly meeting of the Ashfield Tidy Towns Committee will take place on Friday 26th June 2015 at 7.30p.m. in Ashfield Community Centre.')
          + ' Agenda: ' + S(16, '1. Minutes of previous meeting 2. Matters arising from minutes / Correspondence') + ' ... ' + S(16, '4. Sources of finance for improvement to our local park') + ' ... AOB.',
          'The scheme marks ' + S(16, 'Notice 5 x 2m (2m for all bolded terms) Agenda 4 x 2m (2m for bolded items + 2 other agenda items) Sig. 1m Title 1m') + '.']))
add(2, 4, 'e', 'Q4(E)', ashfield + '\n\n' + L(2, 8, '(E) Explain two benefits of teamwork.'), 15, 'business-3-20', 'teamwork-benefits-2015', 8, [16], EIGHT, eight_seven('Benefit'), [UNTIED])

depot = L(2, 8, 'InsuranceDepot.com InsuranceDepot.com is an insurance broker based in Cork city. It employs 8 sales staff in the Cork office. Due to increased online demand they are currently recruiting 3 more sales staff. All sales staff are paid a basic wage plus commission and receive benefit-in-kind.').replace('InsuranceDepot.com InsuranceDepot.com', 'InsuranceDepot.com\nInsuranceDepot.com', 1)
add(2, 5, 'a', 'Q5(A)', depot + '\n\n' + L(2, 8, '(A) Explain two types of insurance that InsuranceDepot.com might sell to its customers.'), 15, 'business-3-17', 'insurance-types-sold',
    8, [17], 'Each type named 3 and explained: 8 (3 + 5) and 7 (3 + 4).', unequal('Type of insurance', [(3, 5), (3, 4)], ['Named', 'Explained']),
    ['The 8-mark allowance is not tied to a particular type.'])
add(2, 5, 'b', 'Q5(B)', depot + '\n\n' + L(2, 8, '(B) Explain two of the following Principles of Insurance and give one example in each case:', '(i) Indemnity (ii) Insurable Interest (iii) Utmost Good Faith'),
    20, 'business-3-17', 'insurance-principles-choice-2015', 8, [17, 18], 'Choose two of the three principles: each 10, explanation 7 (4 + 3) and an example 3.',
    seq(comps('First principle you chose', (4, 3, 3), ['Explained', 'Explanation developed', 'Example']),
        comps('Second principle you chose', (4, 3, 3), ['Explained', 'Explanation developed', 'Example'])),
    ['You choose which two of the three printed principles to answer. The scheme marks every choice alike (10 each), so this is one card whichever principles you choose.',
     'Indemnity (scheme PDF page 17): “' + S(17, 'A person cannot make a profit from insurance – the purpose of insurance is to leave the person in the same financial position as before the claim.') + '”',
     'Insurable Interest (scheme PDF page 17): “' + S(17, 'The person taking out insurance must have a financial interest in the item being insured') + '”',
     'Utmost Good Faith (scheme PDF page 18): “' + S(18, 'A person taking out insurance must be truthful when completing proposal form – all material facts must be declared.') + '”'])
add(2, 5, 'c', 'Q5(C)', depot + '\n\n' + L(2, 8, '(C) Outline the role of an assessor in Insurance.'), 10, 'business-3-17', 'assessor-role', 8, [18], 'One outline: 10 marks (5 + 5).',
    [comps('Assessor', (5, 5))], ['Scheme: ' + S(18, 'An assessor investigates the insurance claim on behalf of the insurance company')])
add(2, 5, 'd', 'Q5(D)', depot + '\n\n' + L(2, 8, '(D) Outline two methods/ways of recruiting new employees.'), 15, 'business-3-20', 'recruiting-methods',
    8, [18], EIGHT, eight_seven('Method'), [UNTIED])
add(2, 5, 'e', 'Q5(E)', depot + '\n\n' + L(2, 8, '(E) Explain the terms commission and benefit-in-kind, and give one example in each case.'), 15, 'business-3-20', 'commission-and-benefit-in-kind',
    8, [18], 'Commission 8 (explanation 6, example 2) and benefit-in-kind 7 (explanation 5, example 2).',
    [comps('Commission', (6, 2), ['Explained', 'Example'], 1), comps('Benefit-in-kind', (5, 2), ['Explained', 'Example'], 2)],
    ['Scheme: ' + S(18, 'Payment to employees based on the level of sales of each employee') + '; ' + S(18, 'Non-financial payment (also known as perks) given to employees') + '.'], extra=['business-3-18'])

mason = L(2, 9, 'Mason Motors Ltd.') + '\n' + L(2, 9, 'David Mason operates a car dealership in Co. Kildare. He sells both new and used cars and also provides mechanic services. He is currently thinking of expanding the business. He will require long term finance for the expansion. David has recently met with his local Bank Manager and presented his Business Plan.')
add(2, 6, 'a', 'Q6(A)', mason + '\n\n' + L(2, 9, '(A) Outline two reasons why David Mason might wish to expand his business.'), 15, 'business-4-18', 'mason-expansion-reasons',
    9, [19], EIGHT, eight_seven('Reason'), [UNTIED])
L(2, 9, 'Year 2010 2011 2012 2013 2014 Net Profit €90,000 €70,000 €60,000 €100,000 €120,000')
flat(add(2, 6, 'b', 'Q6(B)', mason + '\n\n' + L(2, 9, '(B) The following net profit figures are available for Mason Motors Ltd. for the period 2010-2014:')
         + '\n2010 €90,000; 2011 €70,000; 2012 €60,000; 2013 €100,000; 2014 €120,000\n' + L(2, 9, 'Illustrate the above information on a Bar Chart. (You may use graph paper.)'), 15,
         'business-2-12', 'mason-net-profit-bar-chart', 9, [19], 'Title 1, the profit (€) and year labels 2 each, and five bars to scale at 2 each.',
         [fixed('Bar chart', [('Title', 1), ('Profit € label', 2), ('Years label', 2), ('2010: €90,000', 2), ('2011: €70,000', 2), ('2012: €60,000', 2),
                              ('2013: €100,000', 2), ('2014: €120,000', 2)])],
         ['Scheme (page 19): ' + S(19, 'Title 1m Profit € 2m Years 2m Bars 5 x 2m') + '; the summary prints “' + S(7, 'Bar Chart: Title 1 mark Labels 4 marks Bars (to scale) 10 marks (5 @ 2m)') + '”.']))
add(2, 6, 'c', 'Q6(C)', mason + '\n\n' + L(2, 9, '(C) Outline two benefits of using visual communication, such as a bar chart, to present this information to the Bank Manager.'), 15,
    'business-2-12', 'visual-communication-benefits', 9, [19], 'Two benefits: 8 (5 + 3) and 7 (5 + 2).', eight53('Benefit'), [UNTIED])
add(2, 6, 'd', 'Q6(D)', mason + '\n\n' + L(2, 9, '(D) Explain two sources of long term finance David Mason could use to expand his business.'), 15, 'business-3-16',
    'long-term-finance-sources', 9, [20], EIGHT, eight_seven('Source'), [UNTIED])
add(2, 6, 'e', 'Q6(E)', mason + '\n\n' + L(2, 9, '(E) Explain two reasons why stock control is very important in Mason Motors Ltd.'), 15, 'business-2-13', 'mason-stock-control',
    9, [20], EIGHT, eight_seven('Reason'), [UNTIED])

amy = L(2, 9, 'babypressie.ie') + '\n' + L(2, 9, 'Amy McDonald set up her business after having her second child. She saw a gap in the market for personalised baby gifts. Having carried out market research, she decided to manufacture and sell online. She now works from home and distributes her products to customers throughout Ireland.')
add(2, 7, 'a', 'Q7(A)', amy + '\n\n' + L(2, 9, '(A) Explain the term target market.'), 10, 'business-4-16', 'target-market-explained-2015', 9, [21], 'Explanation: 10 marks (5 + 5).',
    [comps('Target market', (5, 5))], ['Scheme: ' + S(21, 'A target market is the group of people at whom a particular product or service is aimed.')])
add(2, 7, 'b', 'Q7(B)', amy + '\n\n' + L(2, 9, '(B) Explain two advantages to Amy of selling her products online.'), 15, 'business-4-17', 'online-selling-advantages-2015',
    9, [21], 'Two advantages: 8 (5 + 3) and 7 (5 + 2).', eight53('Advantage'), [UNTIED], extra=['business-2-12'])
add(2, 7, 'c', 'Q7(C)', amy + '\n\n' + L(2, 9, '(C) Outline three factors Amy must consider before setting the price of her products.'), 20, 'business-4-17', 'amy-pricing-factors',
    9, [21], 'Three factors: 7 (5 + 2), 7 (5 + 2) and 6 (5 + 1).', unequal('Factor', [(5, 2), (5, 2), (5, 1)], None),
    ['The 7/7/6 sequence prices the three factors, not particular factors.'])
add(2, 7, 'd', 'Q7(D)', amy + '\n\n' + L(2, 9, '(D) Outline two benefits of carrying out market research.'), 15, 'business-4-16', 'market-research-benefits-2015',
    9, [22], 'Two benefits: 8 (5 + 3) and 7 (5 + 2).', eight53('Benefit'), [UNTIED])
chan = add(2, 7, 'e', 'Q7(E)', amy + '\n\n' + L(2, 9, '(E) Explain the term channels of distribution and draft the channel used by babypressie.ie.'), 15, 'business-4-17',
           'channels-explained-and-drafted', 9, [22], 'Explanation 8 (4 + 4); the channel drafted 7 (3 + 3 and 1 for the link).',
           seq(comps('Channels of distribution explained', (4, 4)), comps('Channel drafted', (3, 3, 1), ['Manufacturer', 'Consumer', 'Link'])),
           ['Scheme (page 22): ' + S(22, 'This is the means by which the product gets from the manufacturer to the consumer.') + ' Channel: '
            + S(22, 'MANUFACTURER CONSUMER').replace(' ', ' to ') + '; ' + S(22, 'Explanation: 8m (4 + 4) Channel of Distribution: 7m (3 + 3) + 1m for link') + '.'])
for a in chan['rubric']['responses'][1]['allocations']:
    a['permittedMarks'] = [0, a['maxMarks']]

tech = L(2, 10, 'The market for mobile phones, tablets and PCs changes rapidly. The major technology companies, such as Apple, Samsung and Sony, are constantly coming up with new ideas for devices, resulting in older models becoming obsolete. Expensive research and development is carried out to create the devices which are then mass produced for the world market.')
add(2, 8, 'a', 'Q8(A)', tech + '\n\n' + L(2, 10, '(A) Explain what is meant by the term mass production and give one example.'), 10, 'business-4-15', 'mass-production-with-example',
    10, [23], 'Explanation 8 (4 + 4) and an example 2.', seq(comps('Mass production', (4, 4)), single('Example', 2, 'Example given')),
    ['Scheme: ' + S(23, 'Mass Production involves the manufacture of very large quantities of identical products on a continuous basis.') + ' Examples: ' + S(23, 'Ball-point pens, golf balls.')])
add(2, 8, 'b', 'Q8(B)', tech + '\n\n' + L(2, 10, '(B) Outline three benefits of branding for business.'), 20, 'business-4-17', 'branding-benefits-2015',
    10, [23], 'Three benefits: 7 (5 + 2), 7 (5 + 2) and 6 (5 + 1).', unequal('Benefit', [(5, 2), (5, 2), (5, 1)], None),
    ['The 7/7/6 sequence prices the three benefits, not particular benefits.'])
flat(add(2, 8, 'c', 'Q8(C)', tech + '\n\n' + L(2, 10, '(C) Draft and label a Product Life Cycle.'), 15, 'business-4-17', 'product-life-cycle-diagram-2015', 10, [23],
         'Title, sales axis and time axis 1 each; the curved line 2; five stages in order at 2 each.',
         [fixed('Product life cycle diagram', [('Title', 1), ('Sales axis', 1), ('Time axis', 1), ('Curved line', 2), ('Introduction', 2), ('Growth', 2),
                                              ('Maturity', 2), ('Saturation', 2), ('Decline', 2)])],
         ['Scheme (page 23): ' + S(23, 'Title: 1m Sales: 1m Time: 1m Curved Line: 2m Stages: (in order) 5 x 2m') + '.']))
add(2, 8, 'd', 'Q8(D)', tech + '\n\n' + L(2, 10, '(D) Explain the following two stages in the Product Development Process:') + '\n• product screening\n• prototype development.', 15,
    'business-4-14', 'screening-and-prototype', 10, [24], 'Product screening 8 (4 + 4) and prototype development 7 (4 + 3).',
    [comps('Product screening', (4, 4), i=1), comps('Prototype development', (4, 3), i=2)],
    ['Scheme: ' + S(24, 'Product Screening: This involves assessing all ideas for a new product') + '; ' + S(24, 'Prototype Development: An original working example or mock-up of a new product is produced and tested') + '.'])
L(2, 10, 'product screening', 'prototype development.')
add(2, 8, 'e', 'Q8(E)', tech + '\n\n' + L(2, 10, '(E) Outline two factors technology companies must consider before choosing a method of advertising their products.'), 15, 'business-4-17',
    'advertising-method-factors', 10, [24], 'Two factors: 8 (5 + 3) and 7 (5 + 2).', eight53('Factor'), [UNTIED])

# ---------------------------------------------------------------- checks and write-out
qn = lambda c: c['questionRef'].split(' Q')[1].split('(')[0]
for section, count, total in [('1', 15, 10), ('2', 8, 75)]:
    for q in range(1, count + 1):
        got = sum(c['totalMarks'] for c in P.created if c['section'] == section and qn(c) == str(q))
        assert got == total, (section, q, got)
assert not [i for i in ORIGINAL if i.startswith('bus-2015-ol-')]
assert not P.pools

SELECTION = {
    1: 'No finite printed answer menu occurs in Section 1 (answer ten of fifteen at 10 marks). The ticks in Q3 and Q14, the word bank in Q8, TRUE/FALSE in Q9, the chart labels in Q11, the matching rows in Q13 and the organisation chart in Q15 are required answer formats. Support-note lists are open examples.',
    2: 'One printed choice is one card: Q5(B) any two of the three principles of insurance (the scheme marks every choice alike, 10 each). Q8(D) names its two stages, both required. Sub-parts with their own published marks are separate cards. Support-note lists are open examples.',
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
        return 'required-headings', 'Section 1 Q8 is a word-bank completion: both blanks are required and the printed words are the answer options, not optional tasks.', None
    if m == 'or' and own(w, m, 'TRUE or FALSE'):
        return 'required-headings', 'TRUE/FALSE are answer labels for each of the five required statements in Section 1 Q9, not optional tasks.', None
    if m == 'or' and own(w, m, 'a global or adapted marketing mix'):
        return 'case-context', '“a global or adapted marketing mix” is wording inside the Section 1 Q8 sentence, not a choice of task.', None
    if m == 'one of' and own(w, m, 'List the four factors of production and explain one of them'):
        return 'open-response', 'Section 2 Q2(B) asks the candidate to explain one of the four factors they have just listed; the four are required in the list and the scheme marks any one explanation alike (7), so it is one card.', None
    if m == 'two of' and own(w, m, 'Explain two of the following Principles of Insurance'):
        return 'finite-choice', 'Section 2 Q5(B) asks for any two of the three printed principles of insurance. The scheme marks every choice alike (10 each), so one card carries all three with the scheme wording for each.', 'bus-2015-ol-s2-q5b'
    if m == 'following two' and own(w, m, 'Explain the following two stages'):
        return 'required-headings', 'Section 2 Q8(D) names the two stages to explain (product screening and prototype development); both are required, not a choice.', None
    assert (fileid, page) in {('LC033GLP000EV', 1), ('LC033GLP000EV', 6)} and m in ('either', 'or'), (fileid, page, m, w)
    return 'exam-navigation', 'The cover and Section 2 rubrics set how many whole questions a candidate answers (one from Part 1, two from Part 2 and one other from either part). Every numbered question remains in the practice corpus as separate cards.', None


n = P.write([(1, range(1, 16)), (2, range(1, 9))], SELECTION, classify,
            'Every part of {year} Ordinary Section {section} Question {q} was visually checked against its SEC paper, allocation summary and expected responses. The single-booklet identity keeps the short (n) and long (S2Q) question numbering apart.')
print(f'Reviewed {len(P.created)} 2015 Ordinary tasks; classified {n} raw selection matches.')
