"""Review the 2010 Ordinary English paper (one booklet: Section 1 and Section 2).

2010: answer ten of fifteen short questions at 10 marks and four of eight
long questions at 75 (one from Part 1, two from Part 2 and one other), all in
one twelve-page booklet (LC033GLP000EV, the same file id as its scheme). No
Ordinary card existed for 2010, so every card is new. The allocation summary
(scheme pages 3-7) sets each boundary; printed sub-parts with their own
published marks are separate cards. No printed choice of task occurs.

One exception to the split: Section 2 Q8(A) prints "State (i) two advantages
AND (ii) two disadvantages of a sole trader business." as a single sentence.
A card for either sub-part alone could not quote the paper without splicing
it, so Q8(A) is one card whose two response groups carry the summary's two
published sub-totals (10 and 10).
"""
from bus_lib import (Paper, ORIGINAL, comps, points, seq, unequal, single, response, fixed, permit)

T = {(1, q): 3 for q in range(1, 16)}
T.update({(2, 1): 4, (2, 2): 4, (2, 3): 5, (2, 4): 5, (2, 5): 6, (2, 6): 6, (2, 7): 7, (2, 8): 7})
P = Paper(2010, 'ordinary', {1: 'LC033GLP000EV', 2: 'LC033GLP000EV'}, 'LC033GLP000EV', T)
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


# ---------------------------------------------------------------- Section 1 (10 marks each)
q1 = add(1, 1, '', 'Q1', L(1, 2, 'What do the following letters stand for? (Write each answer in the space provided.)', '(i) PR (ii) CV (iii) SWOT').replace(' (ii)', '\n(ii)').replace(' (iii)', '\n(iii)'),
         10, 'business-2-13', 'abbreviations-pr-cv-swot', 2, [9], '(i) 3 (2 + 1), (ii) 3 (2 + 1) and (iii) the four words at 1 each.',
         [comps('(i) PR', (3,), ['Words written in full'], 1), comps('(ii) CV', (3,), ['Words written in full'], 2),
          comps('(iii) SWOT', (1, 1, 1, 1), ['Strengths', 'Weaknesses', 'Opportunities', 'Threats'], 3)],
         ['Answer key: PR ' + S(9, 'Public Relations') + '; CV ' + S(9, 'Curriculum Vitae') + '; SWOT ' + S(9, 'Strengths, Weaknesses, Opportunities, Threats') + '.',
          'The allocation summary prints “' + S(3, '(i) 3marks (2m + 1m) (ii) 3marks (2m + 1m) (iii) 4 @ 1 mark each') + '”.'],
         extra=['business-4-17', 'business-3-20'])
for a in q1['rubric']['responses'][2]['allocations']:
    a['permittedMarks'] = [0, 1]
wc = add(1, 2, '', 'Q2', L(1, 2, 'The following information is available from the final accounts of Casey Ltd on 31/12/2009.') + '\nCurrent Assets € 500,000\nCurrent Liabilities € 200,000\n'
    + L(1, 2, 'Calculate: (i) The Working Capital') + '\n' + L(1, 2, '(ii) The Working Capital Ratio') + '\nWorkings:', 10, 'business-3-19', 'working-capital-casey',
    2, [9], 'Each answer 5 for the correct answer (up to 3 for workings if the answer is wrong).',
    [comps('Working Capital', (5,), ['Answer: €300,000'], 1), comps('Working Capital Ratio', (5,), ['Answer: 2.5 : 1'], 2)],
    ['The allocation summary prints “' + S(3, '(i) 5 marks for correct answer. If incorrect, up to 3 marks for workings') + '” for each part. Scheme answers (page 9): '
     + S(9, 'Working Capital = €500,000 - €200,000 = €300,000') + '; ' + S(9, 'Working Capital Ratio = €500,000 : €200,000 = 2.5 : 1') + '.'])
L(1, 2, 'Current Assets € 500,000 Current Liabilities € 200,000')
# 5 for the correct answer, otherwise up to 3 for workings: 4 is never awarded.
for r in wc['rubric']['responses']:
    r['allocations'][0]['permittedMarks'] = [0, 1, 2, 3, 5]
cum(1, 3, '', 'Q3', L(1, 2, 'Indicate, by means of a tick (✓) the category or sector of industry to which each of the five businesses listed belongs.') + '\nPrimary | Secondary | Tertiary/Services\n'
    + '\n'.join(['A A factory making candles', 'B A taxi company', 'C Insurance Brokers', 'D A dairy farmer', 'E A coal mining company']), (2, 2, 2, 2, 2), 'business-5-13',
    'sector-ticks-2010', 2, [9], 'Answer key (ticks on scheme page 9): A factory making candles Secondary; A taxi company Tertiary/Services; Insurance Brokers Tertiary/Services; A dairy farmer Primary; A coal mining company Primary.',
    noun='ticks')
L(1, 2, 'Primary Secondary Tertiary/Services A A factory making candles B A taxi company C Insurance Brokers D A dairy farmer E A coal mining company')
add(1, 4, '', 'Q4', L(1, 2, 'State two benefits of EU membership for Irish business:'), 10, 'business-6-14', 'eu-membership-benefits-2010', 2, [9],
    'Two benefits at 5 marks each (3 + 2).', points('Benefit', 2, (3, 2)),
    ['Scheme examples: ' + S(9, 'Common Currency – euro – makes trade/travel easier') + '; ' + S(9, 'Large market available to Irish firms for exporting/expansion') + '.'])
cum(1, 5, '', 'Q5', '\n'.join([L(1, 3, 'Column 1 is a list of business terms. Column 2 is a list of explanations for these terms. (One explanation has no match)'),
                               L(1, 3, '1. PAYE', '2. Value Added Tax (VAT)', '3. P45', '4. Self-Assessment Income Tax', '5. Deposit Interest Retention Tax (DIRT)'),
                               L(1, 3, 'A. Paid by a self-employed person.', 'B. Tax charged on interest earned on savings accounts.', 'C. Tax charged on the wages earned by an employee.',
                                 'D. Tax on gifts or inheritances received by people.', 'E. This is given to an employee if he or she leaves his or her job during the tax year.',
                                 'F. Tax charged on the sale of goods or services.'),
                               L(1, 3, 'Match the two lists by placing the letter of the correct explanation under the relevant number below.')]),
    (2, 2, 2, 2, 2), 'business-3-18', 'tax-terms-matching-2010', 3, [9], 'Answer key (scheme page 9): 1 C; 2 F; 3 E; 4 A; 5 B. Explanation D is unused.', noun='matches')
S(9, '1 2 3 4 5 C F E A B')
add(1, 6, '', 'Q6', L(1, 3, 'State two effects of high interest rates on business.'), 10, 'business-5-15', 'high-interest-rate-effects', 3, [9],
    'Two effects at 5 marks each.', points('Effect', 2, (5,)),
    ['Scheme examples: ' + S(9, 'Increases the cost of borrowing') + '; ' + S(9, 'Discourages expansion/borrowing') + '.'], extra=['business-3-16'])
add(1, 7, '', 'Q7', L(1, 3, 'Draft, using today’s date, a Memorandum (Memo) from Michelle Deasy, General Manager to all staff reminding them of the training day to be held on Friday the 2nd July.')
    + '\nMEMORANDUM To: / From: / Date: / Re: / Signed: / Title:', 10, 'business-2-12', 'training-day-memo', 3, [10],
    'Layout six items at 1 each (to, from, date, re, signed, title) and the subject matter 4.',
    seq(fixed('Memo layout', [('To', 1), ('From', 1), ('Date', 1), ('Re', 1), ('Signed', 1), ('Title', 1)]), comps('Subject matter', (4,))),
    ['The allocation summary prints “' + S(3, 'Memorandum layout: 6 items @ 1 mark each Subject matter: 4 marks') + '”.',
     'Scheme (page 10): ' + S(10, 'MEMORANDUM To: All members of staff From: Michelle Deasy Date: 15 June 2010 Re: Training Day The training day will be held on Friday, 2 July 2010. Signed: Michelle Deasy Title: General Manager')])
L(1, 3, 'MEMORANDUM To:')
cum(1, 8, '', 'Q8', L(1, 4, 'Write TRUE or FALSE after each of these statements:', '1. Job production is used to produce one-off unique products.', '2. Strategic Planning is long term planning.',
                      '3. A poor relationship between the sender and the recipient of the message is a barrier to effective communication.',
                      '4. Mass produced goods are generally very expensive and of very high quality.', '5. A Credit Union is a type of Co-operative.'),
    (2, 2, 2, 2, 2), 'business-4-15', 'true-false-2010', 4, [10], 'Answer key (scheme page 10): 1 True; 2 True; 3 True; 4 False; 5 True.',
    extra=['business-2-13', 'business-2-12', 'business-5-14'])
for snip in ['one-off unique products. True', 'long term planning. True', 'effective communication. True', 'very high quality. False', 'type of Co-operative. True']:
    S(10, snip)
cum(1, 9, '', 'Q9', L(1, 4, 'List three grounds on which Employment Discrimination is outlawed under the Employment Equality Act 1998:'), (4, 3, 3), 'business-0-14',
    'discrimination-grounds-2010', 4, [10], 'Scheme grounds (page 10): ' + S(10, '(i) Gender/Male/Female (ii) Marital status (iii) Family Status (iv) Sexual orientation (v) Religious beliefs (vi) Age (vii) Race (viii) Disability (ix) Membership of traveller community.'),
    noun='grounds')
add(1, 10, '', 'Q10', L(1, 4, 'State two benefits of a ‘Partnership’ as a type of business:'), 10, 'business-5-14', 'partnership-benefits-2010', 4, [10],
    'Two benefits at 5 marks each.', points('Benefit', 2, (5,)),
    ['Scheme examples: ' + S(10, 'More capital is available, as there are more owners/investors.') + ' ' + S(10, 'Better decision making as a result of combined effort.')])
add(1, 11, '', 'Q11', L(1, 4, 'Explain the term ‘stock control’:'), 10, 'business-2-13', 'stock-control-explained-2010', 4, [10],
    'A good explanation: 10 marks (5 + 5).', [comps('Stock control', (5, 5))],
    ['Scheme: ' + S(10, 'This ensures that you have enough stock to satisfy customer needs and at the same times keep stock holding costs to a minimum.')])
add(1, 12, '', 'Q12', L(1, 4, 'Outline two ways in which the Irish Government supports business:'), 10, 'business-5-15', 'government-supports-business-2010', 4, [11],
    'Two ways at 5 marks each (3 + 2).', points('Way', 2, (3, 2)),
    ['Scheme examples: ' + S(11, '(i) Grants through Enterprise Ireland/Údarás na Gaeltachta/IDA (ii) Advice/Mentoring – County Enterprise Boards/ Enterprise Ireland (iii) Training through FÁS') + '.'])
flat(add(1, 13, '', 'Q13', L(1, 5, '(i) Complete the three missing stages in the chain of distribution.') + '\n(Diagram: ' + L(1, 5, 'Manufacturer')
         + ' at the top, then three empty boxes, each below an arrow.)\n' + L(1, 5, '(ii) Give two examples of a ‘Manufacturer’:') + '\nExample 1:\nExample 2:', 10, 'business-4-17',
         'chain-of-distribution-2010', 5, [11], 'Three stages in the correct order at 2 each and two non-generic examples at 2 each.',
         seq(comps('Missing stages in order', (2, 2, 2), ['Second stage', 'Third stage', 'Fourth stage']), points('Example of a manufacturer', 2, (2,))),
         ['Answer key (scheme page 11): ' + S(11, 'Manufacturer ↓ Wholesaler ↓ Retailer ↓ Consumer') + '; examples: ' + S(11, 'Any valid examples e.g. Toyota, Philips, Jacobs.'),
          'The allocation summary prints “' + S(3, 'Three stages in correct order @ 2 marks each Two non-generic examples @ 2 marks each') + '”.']))
add(1, 14, '', 'Q14', L(1, 5, 'Explain the following needs in Maslow’s Hierarchy of Needs:') + '\n' + L(1, 5, '(i) Basic Needs:') + '\n' + L(1, 5, '(ii) Safety/Security Needs:'), 10,
    'business-2-11', 'basic-and-safety-needs', 5, [11], 'Each need 5 marks (3 + 2).', [comps('Basic Needs', (3, 2), None, 1), comps('Safety/Security Needs', (3, 2), None, 2)],
    ['Scheme: ' + S(11, 'Basic Needs – the need for food, clothing, shelter and warmth, pay/wage.') + ' ' + S(11, 'Safety/Security Needs – the need for job security/ safe working conditions.')])
cum(1, 15, '', 'Q15', L(1, 5, 'Identify three of the main headings in a business plan. (Example: Finance)'), (4, 3, 3), 'business-4-15', 'business-plan-headings-2010', 5, [11],
    'Scheme headings (page 11): ' + S(11, '(i) Business details / history / goals and objectives (ii) Details of owners / legal structure (iii) Management – how the business will be run / organised') + ' ...',
    noun='headings')

# ---------------------------------------------------------------- Section 2 (75 marks each)
burke = L(2, 6, 'Tom and Mary Burke purchased a washing machine for €600 from Murray’s electrical store. After one week they noticed that the machine did not spin the clothes properly and that water remained in the machine at the end of the washing cycle. They returned to the shop to complain.')
law = add(2, 1, 'ai', 'Q1(A)(i)', burke + '\n\n' + L(2, 6, '(A) (i) Name the law that protects the Burkes in this case.'), 10, 'business-0-13', 'law-protecting-burkes',
          6, [12], 'Four words and the year at 2 marks each.', [comps('Law named', (10,), ['Four words and the year'])],
          ['Scheme: ' + S(12, 'The Sale of Goods and Supply of Services Act 1980.') + ' The allocation summary prints “' + S(4, 'Four words + year @ 2 marks each') + '”.'])
permit(law, 0, [0, 2, 4, 6, 8, 10])
add(2, 1, 'aii', 'Q1(A)(ii)', burke + '\n\n' + L(2, 6, '(ii) Explain three legal rights of the Burke family and one duty of Murray’s electrical store under the law.'), 20, 'business-0-13',
    'burke-rights-and-store-duty', 6, [12], 'Three legal rights at 5 marks each (3 + 2) and one duty at 5 (3 + 2).',
    seq(points('Legal right', 3, (3, 2)), comps('Duty of the store', (3, 2))),
    ['The allocation summary adds “' + S(4, '(Family’s legal rights accepted as Retailer’s duty, but no repetition)') + '”.',
     'Scheme rights: ' + S(12, 'Goods should be of merchantable quality') + '; ' + S(12, 'Goods should be fit for the purpose intended') + '; ' + S(12, 'Goods should be as described') + '; '
     + S(12, 'Goods should be as per sample') + '. Duty: ' + S(12, 'The seller/retailer has the contract with the buyer/consumer and is responsible for putting things right / cannot pass responsibility to consumer.')])
add(2, 1, 'aiii', 'Q1(A)(iii)', burke + '\n\n' + L(2, 6, '(iii) Explain two advantages of taking a case to the Small Claims Court.'), 20, 'business-0-13', 'small-claims-advantages-2010',
    6, [12], 'Two advantages at 10 marks each (5 + 5).', points('Advantage', 2, (5, 5)),
    ['Scheme examples: ' + S(12, 'Provides a quick solution to consumer claims of up to €2,000') + '; ' + S(12, 'No solicitors involved, saving consumer extra cost') + '.'])
mark = L(2, 6, 'Mark is a public sector worker and a member of a trade union. He has been involved in picketing his workplace as part of a national day of protest.')
add(2, 1, 'bi', 'Q1(B)(i)', mark + '\n\n' + L(2, 6, '(B) (i) Explain the term ’picketing’.'), 15, 'business-0-14', 'picketing-explained',
    6, [12], 'Workers involved in a dispute 5, gather together outside the workplace 5, and one other point 5.',
    [comps('Picketing', (5, 5, 5), ['Workers involved in a dispute', 'Gather together outside the workplace', 'One other point'])],
    ['The allocation summary prints “' + S(4, '(Workers involved in a dispute 5marks gather together outside the workplace 5marks + One other point 5 marks)') + '”.',
     'Scheme: ' + S(12, 'This means that workers involved in a dispute gather together outside the workplace and carry placards giving information about their dispute / strike / protest.')])
add(2, 1, 'bii', 'Q1(B)(ii)', mark + '\n\n' + L(2, 6, '(ii) Outline two functions of a trade union.'), 10, 'business-0-14', 'trade-union-functions-2010',
    6, [12], 'Two functions at 5 marks each.', points('Function', 2, (5,)),
    ['Scheme examples: ' + S(12, 'Securing a fair wage for its members / engaging in National Agreements') + '; ' + S(12, 'Securing fair/improved working conditions for its members') + '.'])

whole = L(2, 7, 'Jim and Martina White own Wholefood Farm Products Ltd, an organic farming and food production business in Cork. They produce a range of fresh and frozen products in a small unit located near their farm. Up until now they have sold on the Irish market only. They have recently developed a website and have had a lot of enquiries from potential English and other European customers. They are considering expanding their business by exporting to other countries. Jim and Martina are very conscious of their ethical responsibilities and believe in treating customers and employees in an honest and fair way. They are aware of their environmental responsibilities and of the benefits their business brings to their local community.')
add(2, 2, 'a', 'Q2(A)', whole + '\n\n' + L(2, 7, '(A) State two advantages of a private limited company.'), 10, 'business-5-14', 'private-company-advantages-2010',
    7, [13], 'Two advantages at 5 marks each.', points('Advantage', 2, (5,)),
    ['Scheme examples: ' + S(13, '(i) Shareholders have limited liability – only their investment at risk') + '; ' + S(13, '(v) Continuity of existence in the event of death of a shareholder.')])
add(2, 2, 'b', 'Q2(B)', whole + '\n\n' + L(2, 7, '(B) Outline two environmental responsibilities of business.'), 15, 'business-5-17', 'environmental-responsibilities-2010',
    7, [13], EIGHT, eight_seven('Responsibility'), [UNTIED + ' Scheme examples: ' + S(13, '(ii) Proper waste disposal – no illegal dumping (iii) Energy consumption – conserve energy where possible') + '.'])
ethics = L(2, 7, '(C) Explain how Wholefood Farm Products Ltd can behave ethically towards:')
add(2, 2, 'ci', 'Q2(C)(i)', whole + '\n\n' + ethics + '\n' + L(2, 7, '(i) its customers;'), 10, 'business-5-17', 'ethical-towards-customers-2010',
    7, [13], 'Two points at 5 marks each.', points('Point', 2, (5,)),
    ['Scheme examples: ' + S(13, 'Provide good quality products • Charge reasonable prices • Ensure products are safe and healthy').replace(' • ', '; ') + '.'])
add(2, 2, 'cii', 'Q2(C)(ii)', whole + '\n\n' + ethics + '\n' + L(2, 7, '(ii) its employees.'), 10, 'business-5-17', 'ethical-towards-employees-2010',
    7, [13], 'Two points at 5 marks each.', points('Point', 2, (5,)),
    ['Scheme examples: ' + S(13, 'Pay a fair wage • Provide good conditions of employment • No discrimination in the workplace').replace(' • ', '; ') + '.'])
add(2, 2, 'd', 'Q2(D)', whole + '\n\n' + L(2, 7, '(D) State three challenges/difficulties Jim and Martina may have if they decide to export to other markets.'), 15, 'business-6-13',
    'export-challenges-2010', 7, [13], 'Three challenges at 5 marks each (3 + 2).', points('Challenge', 3, (3, 2)),
    ['The allocation summary adds “' + S(4, '(one or two-word answers get 3 marks)') + '”.',
     'Scheme examples: ' + S(13, '(iv) Risks of exchange rate fluctuations e.g. Sterling, Dollar') + '; ' + S(13, '(vii) Communication problems/different languages.')])
add(2, 2, 'e', 'Q2(E)', whole + '\n\n' + L(2, 7, '(E) Outline two possible benefits that Wholefoods Farm Products Ltd may bring to the local community.'), 15, 'business-5-16',
    'local-community-benefits-2010', 7, [13], EIGHT, eight_seven('Benefit'),
    [UNTIED + ' Scheme examples: ' + S(13, '(i) Employment – they employ local people') + '; ' + S(13, '(iii) Possible sponsorship and support for local events') + '.'])

table = (L(2, 7, 'The following table shows Unemployment Rates from November 2007 to May 2009.')
         + '\n| November 2007 | May 2008 | November 2008 | May 2009\nTotal persons on the Live Register | 150,000 | 200,000 | 250,000 | 400,000')
L(2, 7, 'November 2007 May 2008 November 2008 May 2009 Total persons on the Live Register 150,000 200,000 250,000 400,000')
add(2, 3, 'ai', 'Q3(A)(i)', table + '\n\n' + L(2, 7, '(A) (i) Draw a bar chart to represent the above information.'), 10, 'business-5-15', 'live-register-bar-chart',
    7, [14], 'Title 2 and each of the four bars 2.',
    [fixed('Bar chart', [('Title', 2), ('Bar: November 2007', 2), ('Bar: May 2008', 2), ('Bar: November 2008', 2), ('Bar: May 2009', 2)])],
    ['The allocation summary prints “' + S(5, 'Bar Chart: Title 2 marks 4 bars @ 2 marks each') + '”. The scheme’s chart (page 14) is titled “' + S(14, 'Unemployment Rates Nov 07 - May 09') + '”.'],
    extra=['business-2-12'])
add(2, 3, 'aii', 'Q3(A)(ii)', table + '\n\n' + L(2, 7, '(ii) Outline two effects of increasing unemployment on the Government’s income and expenditure.'), 20, 'business-5-15',
    'unemployment-government-effects', 7, [14], 'Two effects at 10 marks each (5 + 5).', points('Effect', 2, (5, 5)),
    ['Scheme examples: ' + S(14, 'More expenditure on unemployment benefit/assistance') + '; ' + S(14, 'Reduced income tax/PAYE receipts') + '.'])
add(2, 3, 'aiii', 'Q3(A)(iii)', table + '\n\n' + L(2, 7, '(iii) Outline two effects of increasing unemployment on business.'), 20, 'business-5-15',
    'unemployment-business-effects', 7, [14], 'Two effects at 10 marks each (5 + 5).', points('Effect', 2, (5, 5)),
    ['Scheme examples: ' + S(14, 'Reduced consumer spending leads to decrease in sales and profits') + '; ' + S(14, 'Easier to recruit new employees as many are available through unemployment') + '.'])
north = L(2, 7, 'In recent times there has been a large increase in the number of Irish consumers shopping in Northern Ireland.')
add(2, 3, 'bi', 'Q3(B)(i)', north + '\n\n' + L(2, 7, '(B) (i) State two effects of this situation for the Irish economy.'), 15, 'business-5-15', 'cross-border-shopping-effects',
    7, [14], EIGHT, eight_seven('Effect'), [UNTIED + ' Scheme examples: ' + S(14, 'Less expenditure in southern Irish business – decrease in sales and profits') + '; ' + S(14, 'Tax revenue (VAT/Corporation Tax) to Irish Government reduced') + '.'])
add(2, 3, 'bii', 'Q3(B)(ii)', north + '\n\n' + L(2, 7, '(ii) The Irish Government reduced VAT rates in its December 2009 budget. How can this measure help to reverse the above situation?'), 10,
    'business-5-15', 'vat-cut-reverses-cross-border', 7, [14], 'Effect of the VAT reduction: 10 marks (5 + 5).', [comps('How the VAT reduction helps', (5, 5))],
    ['Scheme: ' + S(14, 'Reduced prices south of the border will help business to be more competitive') + '; ' + S(14, 'Less incentive to shop in Northern Ireland.')], extra=['business-3-18'])

roisin = L(2, 8, 'Roisín Murphy worked as a hairdresser in her home town for six years. She left her job as a result of poor employer-employee relationships in the workplace. She believes her former boss Michael was an autocratic leader. Roisín is an enterprising person and has just opened her own hair salon employing three staff. She completed a start your own business course, planned her business well and organised the finance. She regularly consults with staff over business issues and values their opinions. She pays her staff well and praises the high standard and quality of their work. She is an excellent communicator and believes in McGregor’s Theory Y on motivation.')
add(2, 4, 'a', 'Q4(A)', roisin + '\n\n' + L(2, 8, '(A) Explain the term autocratic (authoritarian) leader.'), 10, 'business-2-11', 'autocratic-leader-2010',
    8, [15], 'Explanation: 10 marks (5 + 5).', [comps('Autocratic leader', (5, 5))],
    ['Scheme: ' + S(15, 'The autocratic leader has very little trust or confidence in his/her staff.') + ' ' + S(15, 'He/she makes all decisions and ignores the opinion of others.')])
add(2, 4, 'b', 'Q4(B)', roisin + '\n\n' + L(2, 8, '(B) Outline two effects that poor employer-employee relationships may have on a business.'), 15, 'business-0-14', 'poor-relations-effects',
    8, [15], EIGHT, eight_seven('Effect'), [UNTIED + ' Scheme examples: ' + S(15, 'High absenteeism due to poor atmosphere/poor job satisfaction') + '; ' + S(15, 'Industrial relations problems – strikes, work-to-rule.')])
add(2, 4, 'c', 'Q4(C)', roisin + '\n\n' + L(2, 8, '(C) Outline three enterprising skills/characteristics displayed by Roisín.'), 15, 'business-1-5', 'roisin-enterprising-skills',
    8, [15], 'Three at 5 marks each (3 + 2).', points('Characteristic', 3, (3, 2)),
    ['Scheme examples: ' + S(15, 'Innovative – able to see problems and opportunities and solve them') + '; ' + S(15, 'Decisive – set up her own business') + '.'])
add(2, 4, 'd', 'Q4(D)', roisin + '\n\n' + L(2, 8, '(D) Name two long-term sources of finance Roisín may have used to help start her business and explain one of them.'), 20, 'business-3-16',
    'long-term-sources-roisin', 8, [15], 'Two sources named at 5 each, and one of them explained 10 (5 + 5).',
    seq(single('Source 1', 5, 'Source named'), single('Source 2', 5, 'Source named'), comps('One source explained', (5, 5))),
    ['Scheme sources (page 15): ' + S(15, '(i) Mortgage – for purchase of property; amount, cost/interest, security. (ii) Long term loan – amount, cost/interest, security.') + ' ...'])
add(2, 4, 'e', 'Q4(E)', roisin + '\n\n' + L(2, 8, '(E) Explain McGregor’s Theory Y on Motivation, with reference to the above text.'), 15, 'business-2-11', 'theory-y-roisin',
    8, [15], 'Two points: 8 (explanation 4, reference to the text 4) and 7 (explanation 4, reference 3).',
    unequal('Point', [(4, 4), (4, 3)], ['Explanation', 'Reference to the text']),
    ['The allocation summary prints “' + S(5, 'First Point: (4m for explanation; 4m for reference to text) 2nd Point: (4m for explanation; 3m for reference to text)') + '”.',
     'Scheme: ' + S(15, 'Employers consult regularly with staff about the best way to do their work. She regularly consults with staff over business issues.')])

club = (L(2, 8, 'Glendarn Sports Club in Galway will hold its Annual General Meeting (AGM) in a local hotel next month. The Chairperson Joanne O Boyle and the Secretary Michael Brown are planning the meeting and discussing items for the agenda. Six months ago flooding caused damage to the clubhouse. Joanne checked the insurance policy and contacted the insurance company for a claim form.')
        + '\n(policy and claim form are underlined.)')
flat(add(2, 5, 'a', 'Q5(A)', club + '\n\n' + L(2, 8, '(A) Using today’s date draft the Notice and the Agenda for the Annual General Meeting of Glendarn Sports Club. (The Agenda should contain five items)'), 25,
         'business-2-12', 'glendarn-notice-and-agenda', 8, [16], 'Notice seven items at 2 each, the word Agenda 1, and five agenda items at 2 each.',
         seq(comps('Notice', (2, 2, 2, 2, 2, 2, 2), [f'Notice item {k}' for k in range(1, 8)]), comps('Agenda heading', (1,), ['Agenda']),
             comps('Agenda items', (2, 2, 2, 2, 2), [f'Agenda item {k}' for k in range(1, 6)])),
         ['The allocation summary prints “' + S(6, 'Notice format: 7 items @ 2m each The word “Agenda” @ 1 mark Agenda contents: 5 items @ 2m each (to include at least three of first four in Support Notes, plus any two other items)') + '”.',
          'Scheme (page 16): ' + S(16, 'Notice is hereby given that the Annual General Meeting of the Club will take place on 5 July 2010 at 7.30 p.m. in the Park Hotel Galway.') + ' '
          + S(16, 'Agenda: 1. Minutes of the last Annual General Meeting 2. Chairperson’s report 3. Treasurer’s report 4. Election of new officers 5. Repair of clubhouse/Funding/Insurance costs 6. A.O.B.')]))
add(2, 5, 'bi', 'Q5(B)(i)', club + '\n\n' + L(2, 8, '(B) (i) Outline two duties of a Chairperson at a meeting.'), 10, 'business-2-12', 'chairperson-duties-2010',
    8, [16], 'Two duties at 5 marks each.', points('Duty', 2, (5,)),
    ['Scheme examples: ' + S(16, 'Ensure that there is a quorum, open the meeting and run it in an orderly manner') + '; ' + S(16, 'Ensure that the agenda is followed / ensure compliance with standing orders') + '.'])
add(2, 5, 'bii', 'Q5(B)(ii)', club + '\n\n' + L(2, 8, '(ii) Outline two duties of a Secretary at a meeting.'), 10, 'business-2-12', 'secretary-duties-2010',
    8, [16], 'Two duties at 5 marks each.', points('Duty', 2, (5,)),
    ['Scheme examples: ' + S(16, 'Read the minutes of the last meeting') + '; ' + S(16, 'Take notes of discussions and decisions made in order to write the minutes.')])
add(2, 5, 'c', 'Q5(C)', club + '\n\n' + L(2, 8, '(C) State two advantages of meetings as a method of communication.'), 10, 'business-2-12', 'meetings-advantages-2010',
    8, [16], 'Two advantages at 5 marks each.', points('Advantage', 2, (5,)),
    ['Scheme examples: ' + S(16, 'They allow people to exchange ideas and information') + '; ' + S(16, 'They allow decisions to be made by voting on proposals') + '.'])
add(2, 5, 'di', 'Q5(D)(i)', club + '\n\n' + L(2, 8, '(D) (i) Explain the insurance terms underlined above.'), 10, 'business-3-17', 'policy-and-claim-form',
    8, [16], 'Each term 5 marks (3 + 2).', [comps('Policy', (3, 2), None, 1), comps('Claim form', (3, 2), None, 2)],
    ['Scheme: ' + S(16, 'A policy is a contract document between the insurance company and the insured – it contains details of the insured, the risks covered, length of cover and the conditions attached.')
     + ' ' + S(16, 'If an insured loss is suffered, the insured completes this document when seeking compensation, giving a description of what happened and stating the amount of loss suffered.')])
add(2, 5, 'dii', 'Q5(D)(ii)', club + '\n\n' + L(2, 8, '(ii) Outline how the flood damage may affect future insurance premiums for the club.'), 10, 'business-3-17', 'flood-and-future-premiums',
    8, [16], 'Effect on future premiums: 10 marks (5 + 5).', [comps('Effect on future premiums', (5, 5))],
    ['Scheme: ' + S(16, 'Insurance premiums may increase as premiums are based on risk.') + ' ' + S(16, 'Insurance companies may refuse to cover the risk, or could amend the insurance contract, as they consider that the risk is now greater.')])

cohan = L(2, 9, 'COHAN INFORMATION TECHNOLOGY SOLUTIONS Seeks WEB DESIGNER Cohan IT Solutions is a growing Dublin based company with a current staff of seven. We are looking for a web designer to join our web design team. The position: will involve meeting with clients to assess their requirements. Responsibilities include designing and developing unique websites and on-site training for clients. Rewards are negotiable. The ideal candidate: must have experience, an ability to work as part of a team, excellent communication skills and problem solving capability. Apply online: cohanitsolutions.com before 30th June 2010.')
cohan = cohan.replace(' Seeks ', '\nSeeks\n').replace(' Cohan IT', '\nCohan IT').replace(' The position:', '\nThe position:').replace(' The ideal', '\nThe ideal').replace(' Apply online', '\nApply online')
terms = L(2, 9, '(A) Explain the following terms with reference to the above advertisement:')
add(2, 6, 'ai', 'Q6(A)(i)', cohan + '\n\n' + terms + '\n' + L(2, 9, '(i) job description;'), 10, 'business-3-20', 'job-description-cohan',
    9, [17], 'Two points at 5 marks each (explanation 3, reference to the advertisement 2).', points('Point', 2, (3, 2), ['Explanation', 'Reference to the advertisement']),
    ['Scheme: ' + S(17, 'A JOB DESCRIPTION describes the vacancy that needs to be filled.') + ' It includes “' + S(17, 'the job title Web Designer') + '” and “' + S(17, 'details of work Involves meeting with clients to assess their requirements') + '”.'])
add(2, 6, 'aii', 'Q6(A)(ii)', cohan + '\n\n' + terms + '\n' + L(2, 9, '(ii) person specification.'), 10, 'business-3-20', 'person-specification-cohan',
    9, [17], 'Two points at 5 marks each (explanation 3, reference to the advertisement 2).', points('Point', 2, (3, 2), ['Explanation', 'Reference to the advertisement']),
    ['Scheme: ' + S(17, 'A PERSON SPECIFICATION describes the qualities that the successful candidate should have.') + ' It includes “' + S(17, 'other suitable characteristics/skills Excellent communication skills; problem solving capacity.') + '”'])
add(2, 6, 'b', 'Q6(B)', cohan + '\n\n' + L(2, 9, '(B) State three ways in which Cohan IT Solutions could reward its staff.'), 15, 'business-3-20', 'cohan-staff-rewards',
    9, [17], 'Three ways at 5 marks each.', points('Way', 3, (5,)),
    ['Scheme: ' + S(17, 'Financial: Salary/wage, Bonus, Profit-sharing scheme, Commission, Share ownership, Pension plan Non-financial: Benefits-in-kind e.g., club membership, health insurance, company car.')])
add(2, 6, 'c', 'Q6(C)', cohan + '\n\n' + L(2, 9, '(C) Outline two benefits of teamwork to a business.'), 15, 'business-3-20', 'teamwork-benefits-2010',
    9, [17], EIGHT, eight_seven('Benefit'), [UNTIED + ' Scheme examples: ' + S(17, '(ii) Improved decision making because of a wider range of views') + '; ' + S(17, '(iv) Support - team members share the responsibility and can help each other') + '.'])
add(2, 6, 'd', 'Q6(D)', cohan + '\n\n' + L(2, 9, '(D) State two ways, other than the newspaper, Cohan IT Solutions can use to recruit new staff.'), 10, 'business-3-20', 'recruitment-ways-2010',
    9, [17], 'Two ways at 5 marks each.', points('Way', 2, (5,)),
    ['Scheme: ' + S(17, '(i) Advertisements – local/national/radio/teletext/aertel (ii) Recruitment agencies (iii) Internet sites (iv) FÁS (v) Head-hunting (colleges)/contacts/networking/word of mouth.')])
add(2, 6, 'e', 'Q6(E)', cohan + '\n\n' + L(2, 9, '(E) Outline three advantages of Information Technology to a business, giving examples.'), 15, 'business-2-12', 'it-advantages-2010',
    9, [17], 'Three advantages at 5 marks each (advantage 3, example 2).', points('Advantage', 3, (3, 2), ['Advantage', 'Example']),
    ['The allocation summary adds “' + S(6, '(Maximum of 2 internet related examples acceptable)') + '”.',
     'Scheme examples: ' + S(17, '(ii) Instant and improved communication – e-mails, Facebook (iii) Quick decision making – budgets, cash flow forecasts on spreadsheets') + '.'])

mix = '(Diagram: ' + L(2, 10, 'The Marketing Mix') + ' at the centre, joined to ' + ', '.join(L(2, 10, w) for w in ['Product', 'Price', 'Place']) + ' and ' + L(2, 10, 'Promotion') + '.)'
L(2, 10, 'Place Promotion Price Product The Marketing Mix')
add(2, 7, 'a', 'Q7(A)', mix + '\n\n' + L(2, 10, '(A) State three factors which affect the price of a product.'), 15, 'business-4-17', 'price-factors-2010',
    10, [18], 'Three factors at 5 marks each (3 + 2).', points('Factor', 3, (3, 2)),
    ['Scheme examples: ' + S(18, 'Cost of production – costs must be calculated and recouped over the life of the product.') + ' ' + S(18, 'Competition – price must be similar to competitors to gain market share')])
plc = flat(add(2, 7, 'b', 'Q7(B)', mix + '\n\n' + L(2, 10, '(B) Draft and label the Product Life Cycle diagram.'), 15, 'business-4-17', 'product-life-cycle-2010',
               10, [18], 'Five stages in order at 2 each, the two axes at 1 each, and a correct diagram 3.',
               seq(comps('Stages in order', (2, 2, 2, 2, 2), ['Introduction', 'Growth', 'Maturity', 'Saturation', 'Decline']), comps('Axes', (1, 1), ['Sales', 'Time']),
                   comps('Correct diagram', (3,))),
               ['The allocation summary prints “' + S(7, 'Product Life Cycle 5 ordered stages @ 2 marks each 2 axes @ 1 mark each Correct diagram @ 3 marks') + '”.',
                'Scheme diagram labels (page 18): ' + S(18, 'Sales Introduction Growth Maturity Saturation Decline Time') + '.']))
plc['rubric']['responses'][2]['allocations'][0]['permittedMarks'] = [0, 1, 2, 3]
add(2, 7, 'c', 'Q7(C)', mix + '\n\n' + L(2, 10, '(C) State two reasons why a business would carry out market research.'), 15, 'business-4-16', 'market-research-reasons-2010',
    10, [18], EIGHT, eight_seven('Reason'), [UNTIED + ' Scheme: to find out ' + S(18, 'information about the target market/customers’ needs') + '; ' + S(18, 'if demand exists for a new product/service') + '; ' + S(18, 'to reduce risk of failure/producing unwanted products.')])
add(2, 7, 'di', 'Q7(D)(i)', mix + '\n\n' + L(2, 10, '(D) (i) State two benefits of using a brand name.'), 10, 'business-4-17', 'brand-name-benefits-2010',
    10, [18], 'Two benefits at 5 marks each.', points('Benefit', 2, (5,)),
    ['Scheme examples: ' + S(18, 'helps identify the product / it differentiates the product from other products') + '; ' + S(18, 'creates customer loyalty / easier for the customer to select the product') + '.'])
cum(2, 7, 'dii', 'Q7(D)(ii)', mix + '\n\n' + L(2, 10, '(ii) Give two examples of global brands.'), (3, 2), 'business-6-15', 'global-brand-examples-2010',
    10, [18], 'Scheme examples (page 18): ' + S(18, 'Nike, Rolex, Lacoste, Vodafone, etc.'), noun='examples')
add(2, 7, 'e', 'Q7(E)', mix + '\n\n' + L(2, 10, '(E) Explain the term ‘target market’. Give one example to illustrate your answer.'), 15, 'business-4-16', 'target-market-with-example-2010',
    10, [18], 'Explanation 10 (5 + 5) and one example 5.', seq(comps('Target market', (5, 5)), single('Example', 5, 'Example given')),
    ['Scheme: ' + S(18, 'The target market is the group of people at whom a particular product or service is aimed.') + ' ' + S(18, 'Example: Athletes would be the target market for energy drinks.')])

jack = L(2, 11, 'Jack Sullivan, a sole trader employing five staff, runs a small bakery and coffee shop in Ennis. He owns his premises and a van which is used to deliver his bread and cakes to local shops in the Ennis area. Jack has seen a decline in his sales and profits due to the downturn in the economy and he has decided to increase spending on advertising. He has also considered using sales promotion methods such as price reductions to increase sales. Jack has applied to the bank for an increase in his bank overdraft limit.')
add(2, 8, 'a', 'Q8(A)', jack + '\n\n' + L(2, 11, '(A) State (i) two advantages AND (ii) two disadvantages of a sole trader business.'), 20, 'business-5-14', 'sole-trader-pros-and-cons-2010',
    11, [19], '(i) Two advantages at 5 marks each and (ii) two disadvantages at 5 marks each.', seq(points('Advantage', 2, (5,)), points('Disadvantage', 2, (5,))),
    ['The paper prints (i) and (ii) inside one sentence, so this is one card; the summary’s two sub-totals (10 and 10) are its two response groups.',
     'Scheme examples: advantages ' + S(19, '(i) Formation – easy to set up (ii) Control – the sole trader can make all the decisions') + '; disadvantages '
     + S(19, '(ii) Liability – unlimited liability – could lose private possessions') + '.'])
ins_i = L(2, 11, '(B) (i) Name three types of insurance Jack should have for his business.')
cum(2, 8, 'bi', 'Q8(B)(i)', jack + '\n\n' + ins_i, (3, 3, 3), 'business-3-17', 'jack-insurance-types', 11, [19],
    'Scheme types (page 19): ' + '; '.join(S(19, t) for t in ['Public Liability', 'Employers Liability', 'Motor', 'Buildings and contents insurance']) + '.', noun='types')
add(2, 8, 'bii', 'Q8(B)(ii)', jack + '\n\n' + ins_i + '\n' + L(2, 11, '(ii) Give one reason for having each type of insurance.'), 11, 'business-3-17', 'jack-insurance-reasons',
    11, [19], 'Three reasons: 4, 4 and 3.', unequal('Reason', [(4,), (4,), (3,)], None),
    ['The 4-mark allowances are not tied to particular types. Scheme examples: ' + S(19, 'Public Liability – to protect against claims by members of the public (coffee shop)') + '; '
     + S(19, 'Motor – required by law for van') + '.'])
add(2, 8, 'c', 'Q8(C)', jack + '\n\n' + L(2, 11, '(C) Outline three advertising media that Jack could use to promote his business.'), 15, 'business-4-17', 'jack-advertising-media',
    11, [19], 'Three media at 5 marks each (3 + 2).', points('Medium', 3, (3, 2)),
    ['Scheme examples: ' + S(19, '(i) Radio – many listeners (ii) Newspapers – can illustrate all aspects (iii) Flyers/posters – local market') + '.'])
add(2, 8, 'd', 'Q8(D)', jack + '\n\n' + L(2, 11, '(D) Apart from price reductions, outline two other methods of sales promotion Jack could use to increase sales.'), 10, 'business-4-17',
    'jack-sales-promotion', 11, [19], 'Two methods at 5 marks each (3 + 2).', points('Method', 2, (3, 2)),
    ['Scheme examples: ' + S(19, '(i) Special Offers – buy one, get one free: three for the price of two (ii) Competitions – customers like to win prizes in shop') + '.'])
add(2, 8, 'e', 'Q8(E)', jack + '\n\n' + L(2, 11, '(E) Explain the term ‘bank overdraft’.'), 10, 'business-3-16', 'bank-overdraft-2010',
    11, [19], 'Explanation: 10 marks (5 + 5).', [comps('Bank overdraft', (5, 5))],
    ['Scheme: ' + S(19, 'bank allows the customer to withdraw more money from the account than the account holds') + '; ' + S(19, 'it is a short term source of finance') + '.'])

# ---------------------------------------------------------------- checks and write-out
qn = lambda c: c['questionRef'].split(' Q')[1].split('(')[0]
for section, count, total in [('1', 15, 10), ('2', 8, 75)]:
    for q in range(1, count + 1):
        got = sum(c['totalMarks'] for c in P.created if c['section'] == section and qn(c) == str(q))
        assert got == total, (section, q, got)
assert not [i for i in ORIGINAL if i.startswith('bus-2010-ol-')]
assert not P.pools

SELECTION = {
    1: 'No finite printed answer menu occurs in Section 1 (answer ten of fifteen at 10 marks). TRUE/FALSE in Q8 and the matching rows in Q5 are required answer formats; Q15 asks for three business-plan headings of the candidate’s own. Support-note lists are open examples.',
    2: 'No printed choice of task occurs in Section 2. Q4(D) asks the candidate to explain one of the two sources they named; the list is their own. Sub-parts with their own published marks are separate cards, except Q8(A), whose (i) and (ii) share one printed sentence. Support-note lists are open examples.',
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
    if m == 'one of' and own(w, m, 'explain one of them'):
        return 'open-response', 'Section 2 Q4(D) asks the candidate to explain one of the two long-term sources they named; the list is their own and the scheme marks any source alike, so it is one card.', None
    if m == 'three of' and own(w, m, 'Identify three of the main headings'):
        return 'open-response', 'Section 1 Q15 asks for three business-plan headings of the candidate’s own; no list is printed (Finance is given as an example), so it is one card.', None
    if m == 'or' and (own(w, m, 'TRUE or FALSE') or own(w, m, 'True or False')):
        return 'required-headings', 'TRUE/FALSE are answer labels for each of the five required statements in Section 1 Q8, not optional tasks.', None
    if m == 'or' and (own(w, m, 'category or sector') or own(w, m, 'gifts or inheritances') or own(w, m, 'he or she') or own(w, m, 'his or her') or own(w, m, 'goods or services')):
        return 'case-context', 'Wording inside a printed instruction or explanation (Section 1 Q3, Q5), not a choice of task.', None
    assert (fileid, page) in {('LC033GLP000EV', 1), ('LC033GLP000EV', 6)} and m in ('either', 'or'), (fileid, page, m, w)
    return 'exam-navigation', 'The cover and Section 2 rubrics set how many whole questions a candidate answers (one from Part 1, two from Part 2 and one other from either part). Every numbered question remains in the practice corpus as separate cards.', None


n = P.write([(1, range(1, 16)), (2, range(1, 9))], SELECTION, classify,
            'Every part of {year} Ordinary Section {section} Question {q} was visually checked against its SEC paper, allocation summary and support notes. The single-booklet identity keeps the short (n) and long (S2Q) question numbering apart.')
print(f'Reviewed {len(P.created)} 2010 Ordinary tasks; classified {n} raw selection matches.')
