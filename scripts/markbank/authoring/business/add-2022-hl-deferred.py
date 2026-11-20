"""Card the SEC's 2022 Higher Level deferred Business sitting.

Sources (deferredexams/2022 and deferredmarkingschemes/2022, filed by Paper Trail as "<fileid>-deferred"):
Section 1 and Answerbook LC033ALP032EV (36 pages), Sections 2 and 3 LC033ALP041EV (12 pages), marking scheme
LC033ALP000EV (42 pages, "V2"). Every page was rendered and read on 2026-11-19: the Section 1 booklet's cover,
instructions, the twelve short questions on pages 3-8 (Q10's tax table, Q12's break-even table with its printed
values), the answerbook instructions, graph paper and ruled answer pages; the Sections 2 and 3 booklet's cover,
the West Shore Adventure Centre case (p2), Section 3 Questions 1-8 on pages 3-9 with their extracts and Q7's
McCann Ltd figures and industry averages, two pages with no examination material (10, 11) and the back cover; the
scheme's cover, the p2 note on deferred marking schemes, Section 1 on pages 3-9, the ABQ on pages 10-17 and
Section 3 on pages 18-40 (41-42 blank).

The deferred scheme prints each part's allocation beside its responses (it has no summary table), and its
headings sometimes restate the paper: Q7(i) is headed "Explain the term free trade." but defines
protectionism, (ii) asks for "protectionist measures" where the paper asks for "barriers to trade"; Section 3
Q2(B) and Q5(B) are headed "(20 marks)" and Q5(C) "(20 marks)" where the paper prints 25, 25 and 15, and the
printed allocations sum to the paper's. Each card follows the paper and quotes the scheme as printed.

Run from the repo root; reproduce.py runs it in the chain.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from deferred_lib import Sitting, response, comps, points, seq, unequal, LINK_NOTE  # noqa: E402

D = Sitting(2022, 'higher', {1: 'LC033ALP032EV', 2: 'LC033ALP041EV', 3: 'LC033ALP041EV'}, 'LC033ALP000EV')
L, S = D.lift, D.sch


def cumulative_key(q, n):
    return f'For 0, 1, 2, 3, 4 or 5 correct answers, record 0, 3, 5, 7, 9 or 10 marks (the published sequence 3,2,2,2,1).'


SEQ10 = [0, 3, 5, 7, 9, 10]

# ---------------------------------------------------------------- Section 1
D.cumulative(1, 'q1', 'Q1', L(1, 3, 'In the context of business, what do the following letters stand for?',
                               'Write each answer in the space provided.') + '\n' + L(1, 3, 'PAYE', 'USC', 'PRSI', 'DIRT', 'CAT'),
             10, None, 'business-3-18', 'tax-abbreviations', 3, [3],
             'Give all five in full. The published cumulative sequence is 3 + 2 + 2 + 2 + 1.', SEQ10,
             D.expected(3, 'PAYE Pay As You Earn', 'USC Universal Social Charge', 'PRSI Pay Related Social Insurance',
                        'DIRT Deposit Interest Retention Tax', 'CAT Capital Acquisition Tax'),
             [cumulative_key(1, 5)])
D.add(1, 'q2i', 'Q2(i)', L(1, 3, 'Explain the function of Performance Appraisal in Human Resource Management.'), 4,
      'business-3-20', 'performance-appraisal-function', 3, [3], 'Explain the function for 4 marks (2, 2).',
      [comps('Performance appraisal', (2, 2))],
      expected=D.split([(3, 'Performance appraisal is an evaluation', ' (b) Outline two benefits')],
                       ['Performance appraisal is an evaluation/measurement of an employee’s performance']),
      guidance=['The scheme numbers the two parts (a) and (b); the paper prints (i) and (ii).'])
D.add(1, 'q2ii', 'Q2(ii)', L(1, 3, 'Outline two benefits to management of conducting performance appraisals.'), 6,
      'business-3-20', 'performance-appraisal-benefits', 3, [3], 'Outline two benefits at 3 marks each (2 + 1).',
      points('Benefit', 2, (2, 1)),
      expected=D.split([(3, '(i) Industrial Relations:', ' 4 (2,2)')], ['Industrial Relations:', 'Training needs:'],
                       drop=['(ii)']))
D.cumulative(1, 'q3', 'Q3', L(1, 4, 'Write True or False after each of the following statements.') + '\n' + L(
    1, 4, '1. The span of control refers to the number of employees reporting directly to a manager.',
    '2. Specialisation of work takes place in a matrix organisational structure.',
    '3. Delegation involves management giving tasks and responsibilities to employees.',
    '4. A mission statement is the overall business aim to be achieved over the life of the business.',
    '5. The chain of command involves people working alongside each other in specific departments.'),
    10, None, 'business-2-13', 'organisation-terms-true-false', 4, [4],
    'Mark all five statements. The published cumulative sequence is 3 + 2 + 2 + 2 + 1.', SEQ10,
    D.expected(4, '1. The span of control refers to the number of employees reporting directly to a manager. TRUE',
               '2. Specialisation of work takes place in a matrix organisation structure. FALSE',
               '3. Delegation involves management giving tasks and responsibilities to employees. TRUE',
               '4. A mission statement is the overall business aim to be achieved over the lift of the business TRUE',
               '5. The chain of command involves people working alongside each other in specific departments. FALSE'),
    [cumulative_key(3, 5)])
D.add(1, 'q4', 'Q4', L(1, 4, 'Explain the terms desk research and field research, in each case give an example to support your answer.'),
      10, 'business-4-16', 'desk-and-field-research', 4, [4], 'Each term: explanation 3 and example 2.',
      [comps('Desk research', (3, 2), ['Explanation', 'Example'], 1), comps('Field research', (3, 2), ['Explanation', 'Example'], 2)],
      expected=D.split([(4, '(i) Desk (Secondary) Research', None)],
                       ['Desk (Secondary) Research', 'Example: Government Publications:', 'Field (Primary) Research',
                        'Example: Surveys:'], drop=['3,2 3,2', '(ii)']))
D.cumulative(1, 'q5', 'Q5', L(1, 5, 'Column 1 is a list of types of Business Organisations.', 'Column 2 is a list of Business Characteristics.',
                               '(One characteristic does not refer to any of the business types.)',
                               'Match the two lists by placing the letter of the correct explanation under the relevant number below.')
             + '\n\n' + L(1, 5, 'Column 1 - Types of Business Organisations.', 'Column 2 - Characteristics', '1 Multinational Company',
                          '2 State-owned Enterprise', '3 A Franchise', '4 Private Limited Company', '5 Co-operative',
                          'A 1 to 149 shareholders.', 'B Uses a business name, logo and business idea in return for a fee and a percentage of the profits.',
                          'C Controlling headquarters in one country and branches in many countries.', 'D Owners have unlimited liability.',
                          'E Set up and financed by the Government.', 'F Must have a minimum of seven members, but there is no maximum.'),
             10, None, 'business-5-14', 'business-organisation-types-matching', 5, [5],
             'Match all five. The published cumulative sequence is 3 + 2 + 2 + 2 + 1.', SEQ10,
             {'page': 5, 'items': [{'id': f'e{n}', 'text': f'{n} — {x}'} for n, x in
                                   enumerate(S(5, '1 2 3 4 5 C E B A F').split()[5:], 1)]},
             ['Answer key (scheme grid “1 2 3 4 5 C E B A F”): 1 C; 2 E; 3 B; 4 A; 5 F. Characteristic D is unused.',
              cumulative_key(5, 5)])
D.add(1, 'q6', 'Q6', L(1, 5, 'Illustrate your understanding of the terms EU (European Union) Directive and EU Regulation in the context of EU decision making. Give an example in each case.'),
      10, 'business-6-14', 'eu-directive-and-regulation', 5, [5], 'Each term: explanation 3 marks and example 2 marks.',
      [comps('EU Directive', (3, 2), ['Explanation', 'Example'], 1), comps('EU Regulation', (3, 2), ['Explanation', 'Example'], 2)],
      expected=D.split([(5, 'A directive is a law', ' Explanation 3 marks')],
                       ['A directive is a law that applies to all EU member states', 'E.g. WEEE Directive',
                        'Regulations mean that laws are introduced and enforced', 'E.g. General Data Protection Regulation (GDPR) 2018.']))
D.add(1, 'q7i', 'Q7(i)', L(1, 6, 'Explain the term free trade.'), 4, 'business-6-13', 'free-trade-term', 6, [6],
      'Explain the term for 4 marks (2 + 2).', [comps('Free trade', (2, 2))],
      expected=D.split([(6, 'Protectionism refers to', ' (ii) Protectionist measures')],
                       ['Protectionism refers to government actions and policies']),
      guidance=['The scheme heads this part “' + S(6, '(i) Explain the term free trade.') + '” and prints the response beneath it as a definition of protectionism; it is shown as printed.'])
D.add(1, 'q7ii', 'Q7(ii)', L(1, 6, 'Outline two barriers to trade that are used by governments/trading blocs.'), 6,
      'business-6-13', 'barriers-to-trade', 6, [6], 'Outline two barriers at 3 marks each (2 + 1).', points('Barrier', 2, (2, 1)),
      expected=D.split([(6, 'Tariff:', ' 4 (2+2)')], ['Tariff:', 'Quota:']),
      guidance=['The scheme restates this part as “' + S(6, 'Outline two protectionist measures that are used by government/trading blocs.') + '”; the card follows the paper.'])
D.add(1, 'q8', 'Q8', L(1, 6, 'Outline two short-term implications for a business if their business expands quickly.'), 10,
      'business-4-18', 'short-term-expansion-implications', 6, [6], 'Outline two implications at 5 marks each (3 + 2).',
      points('Implication', 2, (3, 2)),
      expected=D.split([(6, '(i) Employment:', ' 2@5 marks')], ['Employment:', 'Profitability:', 'Organisational structure', 'Product mix'],
                       drop=['(ii)', '(iii)', '(iv)']))
D.add(1, 'q9i', 'Q9(i)', L(1, 7, 'In relation to business, explain the term code of ethics.'), 6, 'business-5-17', 'code-of-ethics-term', 7, [7],
      'Explain the term for 6 marks (3 + 3).', [comps('Code of ethics', (3, 3))],
      expected=D.split([(7, 'A code of ethics is a set', ' (ii) Outline one benefit')],
                       ['A code of ethics is a set of moral rules and standards']))
D.add(1, 'q9ii', 'Q9(ii)', L(1, 7, 'Outline one benefit for a business of introducing a code of ethics.'), 4, 'business-5-17',
      'code-of-ethics-benefit', 7, [7], 'Outline one benefit for 4 marks (2, 2).', [comps('Benefit', (2, 2))],
      expected=D.split([(7, 'Encourages whistleblowing:', ' 6 marks (3+3)')],
                       ['Encourages whistleblowing:', 'Good reputation/brand image:', 'Sets high standards/Encourages ethical behaviour:']))
tax = L(1, 7, 'The table below shows the earnings and tax details for Tadhg Flynn, a single person.', 'USC does not need to be calculated.') + '\n' + L(
    1, 7, 'Gross Pay €41,000', 'Standard Tax Rate 20%', 'Tax Credits € 3,400', 'Higher Tax Rate 40%', 'Standard Rate Cut-off Point €35,300',
    'Tadgh pays 4% PRSI on his gross income')
TAXNOTE = ('The scheme prices the two parts together: “' + S(8, '6 calculations@1mark 2 answers @2 marks') + '”, “'
           + S(8, 'Own figures shaded') + '”. Its workings give (i) four calculations and the PAYE answer, (ii) two calculations and the take-home answer.')
D.add(1, 'q10i', 'Q10(i)', tax + '\n\n' + L(1, 7, 'Using the information supplied calculate the PAYE which Tadgh has to pay.'), 6,
      'business-3-18', 'paye-calculation', 7, [8], 'Four calculations at 1 mark each and the answer 2.',
      [response(1, 'Calculations', [('standard', '35,300 X 20% =7,060', 1), ('higher', '5,700 X 40% = 2,280', 1), ('gross', '9,340', 1),
                                    ('credits', 'Less Tax Credits 3,400', 1)]),
       response(2, 'Answer', [('answer', 'Answer: €5,940', 2)])],
      expected=D.expected(8, '35,300 X 20% =7,060', '5,700 X 40% = 2,280', '9,340', 'Less Tax Credits 3,400', 'Answer: €5,940'),
      guidance=[TAXNOTE])
D.add(1, 'q10ii', 'Q10(ii)', tax + '\n\n' + L(1, 7, 'Using the information supplied above calculate Tadgh’s net annual take-home pay.'), 4,
      'business-3-18', 'net-take-home-pay', 7, [8], 'Two calculations at 1 mark each and the answer 2.',
      [response(1, 'Calculations', [('prsi', 'PRSI: 41,000 X 4% = 1,640', 1), ('deductions', 'PAYE = 5,940 7,580', 1)]),
       response(2, 'Answer', [('answer', 'Answer: €33,420', 2)])],
      expected=D.expected(8, 'PRSI: 41,000 X 4% = 1,640', 'PAYE = 5,940 7,580', '41,000 – 7,580 = 33,420', 'Answer: €33,420'),
      guidance=[TAXNOTE])
D.add(1, 'q11', 'Q11', L(1, 8, 'Read the extract below and answer the question which follows.') + '\n\n'
      + L(1, 8, 'The first Irish Amazon “fulfilment centre” is to create 500 jobs.', 'Adapted from rte.ie') + '\n\n'
      + L(1, 8, 'Distinguish between the purpose of a job description and a person specification when recruiting staff.'), 10,
      'business-3-20', 'job-description-versus-person-specification', 8, [8], 'Both required at 5 marks each (3 + 2).',
      [comps('Job description', (3, 2), i=1), comps('Person specification', (3, 2), i=2)],
      expected=D.split([(8, 'Job description:', ' 2@5 (3+2)')], ['Job description:', 'Person specification:']))
D.cumulative(1, 'q12', 'Q12', L(1, 8, 'Complete the following table for a break-even chart.', '(You are not required to draw the breakeven chart.) Show all your workings.')
             + '\n\n' + L(1, 8, 'Target Output in Units 0 20,000 50,000', 'Selling Price €20 €20 €20', 'Total Revenue €0 A = €1,000,000',
                          'Fixed Costs (FC) €160,000 €160,000 C =', 'Variable Costs (VC) (€12 per unit) 0 B = €600,000',
                          'Total Costs (TC) €160,000 €400,000 D =', 'Profit/Loss at Target Output -€160,000 €0 E ='),
             10, None, 'business-3-19', 'breakeven-table-complete', 8, [9],
             'Complete all five cells A-E. The published cumulative sequence is 3 + 2 + 2 + 2 + 1.', SEQ10,
             D.expected(9, 'A =€400,000', 'B = €240,000', 'C = €160,000', 'D = €760,000', 'E =€240,000'),
             [cumulative_key(12, 5)])

# ---------------------------------------------------------------- Section 2: the Applied Business Question
CASE = dict(label='CASE STUDY', title='West Shore Adventure Centre', pages=[2])


def abq(key, ref, prompt, total, topic, concept, schemes, requirement, responses, expected, guidance=(LINK_NOTE,)):
    return D.add(2, f'abq-{key}', f'ABQ{ref}', prompt, total, topic, concept, 2, schemes, requirement, responses,
                 list(guidance), expected, **CASE)


abq('a', '(A)', L(2, 2, 'Outline four types of insurance that West Shore Adventure Centre would be expected to have.'), 20,
    'business-3-17', 'adventure-centre-insurance', [10, 11], 'Four types at 5 marks each: Type 2, Explain 2, Link 1.',
    [response(i, f'Insurance type {i}', [('name', 'Type', 2), ('explain', 'Explain', 2), ('link', 'Link', 1)]) for i in (1, 2, 3, 4)],
    D.split([(10, 'Motor Insurance By law', None), (11, 'Product Liability:', None)],
            ['Motor Insurance', 'Third-Party Motor Insurance:', 'Third-party, fire and theft motor insurance:', 'Comprehensive Insurance:',
             'Buildings & Contents Insurance:', 'Public Liability Insurance', 'Product Liability:', 'Employer’s Liability:',
             'Pay Related Social Insurance (PRSI):', 'Key person insurance:', 'Fidelity guarantee insurance:', 'Consequential Loss Insurance:'],
            drop=['4@5 (2+2+1) Type Explain Link']))
abq('b-i', '(B)(i)', L(2, 2, 'Explain the term Public Relations (PR).'), 6, 'business-4-17', 'public-relations-term', [12],
    'Explain the term for 6 marks.', [comps('Public Relations (PR)', (6,), ['Explanation'])],
    D.split([(12, 'A marketing technique used', ' 2@12marks')],
            ['A marketing technique used to create a positive public image', 'It refers to all activities', 'Link:']),
    guidance=['The scheme prints the part at “' + S(12, '6 marks') + '” with no split.'])
abq('b-ii', '(B)(ii)', L(2, 2, 'Evaluate the methods West Shore Adventure Centre are using to develop good PR for their business.'), 24,
    'business-4-17', 'public-relations-methods', [12], 'Two methods at 12 marks each, as the scheme prints them: 5 + 2 + 4 + 1 (Name, Explain, Link, Evaluation).',
    [response(i, f'PR method {i}', [('name', 'Name', 5), ('explain', 'Explain', 2), ('link', 'Link', 4), ('evaluate', 'Evaluation', 1)]) for i in (1, 2)],
    D.split([(12, 'Sponsorship:', None)], ['Sponsorship:', 'Celebrity Endorsements:', 'Charitable work & donations:'],
            drop=['Name Explain Link Evaluation']),
    guidance=[LINK_NOTE, 'The scheme prints “' + S(12, '2@12marks') + '” and “' + S(12, '5+2+4+1') + '” beside the column heads Name, Explain, Link and Evaluation.'])
abq('c-i', '(C)(i)', L(2, 2, 'Explain the benefits of community development.'), 14, 'business-5-16', 'community-development-benefits', [13, 14],
    'Two benefits at 7 marks each: Benefit 5 and Link 2.',
    [response(i, f'Benefit {i}', [('explain', 'Benefit', 5), ('link', 'Link', 2)]) for i in (1, 2)],
    D.split([(13, 'Creates employment', None), (14, 'Improved services:', ' (ii) Analyse how')],
            ['Creates employment and thereby increases spending in the local economy:', 'Spin Off Jobs:',
             'Promotes an enterprise culture/encourages new ideas/new businesses in community', 'Community Spirit:',
             'Training opportunities:', 'Improved services:', 'Quality of Life:', 'Clean appearance:'],
            drop=['2@7 (5+2) Benefit and Link']))
abq('c-ii', '(C)(ii)', L(2, 2, 'Analyse how changes to economic variables in the economy have effected businesses like West Shore Adventure Centre.'), 16,
    'business-5-15', 'economic-variables-impact', [14, 15, 16, 17], 'Two variables at 8 marks each: Variable 4, Explain 2, Link 2.',
    [response(i, f'Economic variable {i}', [('name', 'Variable', 4), ('explain', 'Explain', 2), ('link', 'Link', 2)]) for i in (1, 2)],
    D.split([(14, 'Inflation:', None), (15, 'Business Confidence', None), (16, 'Unemployment Rate:', None), (17, 'Business Confidence:', None)],
            ['Inflation:', 'Interest Rates:', 'Unemployment Rate:', 'Taxation:'], drop=['2@8 marks (4+2+2) Variable Explain Link']))

# ---------------------------------------------------------------- Section 3
P = lambda page, *s: L(3, page, *s)
conflict = P(3, 'Conflict between entrepreneurs, suppliers, employees and customers affects operations and can contribute to business failures.')
pairs = P(3, 'Describe one example of a co-operative relationship and one example of a source of conflict that could exist between each of the following pairs of stakeholders:')
for key, roman, pair, start, end in [('q1ai', 'i', 'Government and entrepreneur', 'Government and entrepreneur Co-operative Relationship', ' Producer and consumer Cooperative'),
                                     ('q1aii', 'ii', 'Producer and consumer.', 'Producer and consumer Cooperative Relationship', ' 4@5 (2+3)')]:
    D.add(3, key, f'Q1(A)({roman})', conflict + '\n\n' + pairs + '\n' + P(3, f'({roman}) {pair}'), 10, 'business-0-12',
          'stakeholder-co-operation-and-conflict', 3, [18],
          'For this pair: one co-operative relationship and one source of conflict at 5 marks each (2 + 3).',
          [comps('Co-operative relationship', (2, 3), i=1), comps('Source of conflict', (2, 3), i=2)],
          ['The scheme prices (A) at “' + S(18, '4@5 (2+3)') + '”: two responses for each printed pair.'],
          D.split([(18, start, end)], [start.split(' Co')[0], 'Co-operative Relationship' if roman == 'i' else 'Cooperative Relationship',
                                       'Source of Conflict']))
D.add(3, 'q1b', 'Q1(B)', conflict + '\n\n' + P(3, 'Outline the process involved in resolving an industrial relations conflict using non-legislative methods of resolution.'),
      20, 'business-0-14', 'non-legislative-resolution-process', 3, [19], 'Outline four stages at 5 marks each (2 + 3).', points('Stage', 4, (2, 3)),
      expected=D.split([(19, 'Meeting and talking', ' 4@5 (2+3)')], ['Meeting and talking', 'Negotiation', 'Conciliation', 'Mediation', 'Arbitration']))
D.add(3, 'q1c', 'Q1(C)', conflict + '\n\n' + P(3, 'Evaluate the role of the Data Protection Commissioner (DPC) in protecting an individual’s personal data under the terms of the General Data Protection Regulation (GDPR) 2018.'),
      20, 'business-2-12', 'data-protection-commission-role', 3, [20], 'Three roles at 6 marks each (3 + 3) and an evaluation 2.',
      seq(points('Role', 3, (3, 3)), response(0, 'Evaluation', [('evaluate', 'Evaluation', 2)])),
      expected=D.split([(20, 'Monitors and enforces GDPR:', ' Plus Evaluation')],
                       ['Monitors and enforces GDPR:', 'Promotes public awareness of GDPR:', 'Prohibits data transfer:', 'Impose fines:', 'Data audits:']),
      extra=['business-0-13'])

lpt = P(4, 'Changes were announced for the Local Property Tax (LPT) for 2022. These apply to properties valued on 1 November, 2021. These changes widen the bands and lower the tax rate.', 'Adapted from www.gov.ie')
D.add(3, 'q2a', 'Q2(A)', lpt + '\n\n' + P(4, 'Outline the impact for the economy as a result of the government collecting LPT.'), 15, 'business-5-15',
      'local-property-tax-economic-impact', 4, [21], 'Outline three impacts at 5 marks each (2 + 3).', points('Impact', 3, (2, 3)),
      expected=D.split([(21, 'More disposable income:', ' (B) Explain two ways')], ['More disposable income:', 'GNP Increases', 'Less revenue raised by local authorities:']),
      extra=['business-3-18'])
D.add(3, 'q2b', 'Q2(B)', lpt + '\n\n' + P(4, 'Explain two ways the Irish Government could use the tax system to create a positive climate for business in Ireland. Use examples to illustrate your answer.'),
      25, 'business-5-15', 'tax-system-positive-business-climate', 4, [21],
      'Two ways at 10 marks each (4 + 3 + 3: Tax, explain, Irish business) and an evaluation 5 (0, 2 or 5).',
      seq(points('Way', 2, (4, 3, 3), ['Tax', 'Explain', 'Irish business']), response(0, 'Evaluation', [('evaluate', 'Evaluation', 5)])),
      expected=D.split([(21, '• PAYE – Reduction', ' 3@5 (2+3)')],
                       ['PAYE – Reduction in PAYE rates', 'PAYE - An increase in PAYE rates', 'Corporation Tax –', 'Stamp Duty –', 'Tax Credits –',
                        'VAT/Excise Duties –', 'Tax Incentive Schemes –'], drop=['•']),
      guidance=['The scheme heads (B) “' + S(21, '(20 marks)') + '” and prices it “' + S(21, '2@10 (4+3+3)') + '” with an evaluation “'
                + S(21, '(0,2,5)') + '”: 25 marks, as the paper prints.'],
      extra=['business-3-18'])
D.cards[-1]['rubric']['responses'][-1]['allocations'][0]['permittedMarks'] = [0, 2, 5]
D.add(3, 'q2c', 'Q2(C)', P(4, 'Evaluate the advantages and disadvantages of a partnership as a form of ownership structure.'), 20, 'business-5-14',
      'partnership-evaluation', 4, [22], 'Three points at 6 marks each (3 + 3) and an evaluation 2.',
      seq(points('Point', 3, (3, 3)), response(0, 'Evaluation', [('evaluate', 'Evaluation', 2)])),
      expected=D.split([(22, 'Advantages • Partnerships have access to greater', ' 3@6 (3+3)')],
                       ['Advantages', 'Partnerships have access to greater amounts of capital', 'Partnerships have access to different skill sets',
                        'Partnership can lead to more effective decision making', 'Ability to achieve economies of scale.',
                        'Financial information can remain confidential.', 'Disadvantages', 'Partners in the main have unlimited liability.',
                        'The partners are jointly and severally liable', 'Shared decision making could lead to differences of opinion',
                        'The profits of the business have to be shared', 'Not a separate legal entity', 'If one partner dies or resigns'],
                       drop=['•']))

ei = P(4, 'Enterprise Ireland’s key priority for 2021 is to continue to develop its people and organisation to respond to the rapidly changing external environment, driven by external shocks and structural changes; for example, Brexit, COVID-19, digitalisation and climate change.', 'Adapted from Enterprise Ireland’s Strategic Priorities 2021')
D.add(3, 'q3a', 'Q3(A)', ei + '\n\n' + P(4, 'Explain the function and the role of Enterprise Ireland.'), 15, 'business-5-15', 'enterprise-ireland-role', 4, [23],
      'Three points at 5 marks each (2 + 3).', points('Point', 3, (2, 3)),
      expected=D.split([(23, 'Funding:', ' 3@5(2+3)')], ['Funding:', 'International Offices:', 'Encouraging Research & Development (R&D):',
                                                          'Market Research Centres:', 'Events:']),
      extra=['business-6-13'])
D.add(3, 'q3b', 'Q3(B)', ei + '\n\n' + P(4, 'A business must choose the most appropriate channel of distribution to reach the largest number of consumers.',
                                         'Outline two channels of distribution which Irish businesses may consider when exporting globally.'),
      20, 'business-6-15', 'export-distribution-channels', 4, [24], 'Two channels at 10 marks each: Name 4, Explain 3, Explain 3.',
      points('Channel', 2, (4, 3, 3), ['Name', 'Explain', 'Explain']),
      expected=D.expected(24, '• Trade Missions', '• Trading Houses', '• Subcontracting', '• Trade Fairs', '• Licensing', '• Agents'),
      guidance=['The scheme prints the channels as a list and prices them “' + S(24, '2@4+3+3') + '”.'],
      extra=['business-4-17'])
D.add(3, 'q3c', 'Q3(C)', ei + '\n\n' + P(4, 'Discuss the possible opportunities and threats for small Irish export-led businesses operating in a globalised world.'),
      25, 'business-6-15', 'globalisation-opportunities-and-threats', 4, [24, 25],
      'Four points: one at 7 marks (4 + 3) and three at 6 marks (3 + 3).', unequal('Point', [(4, 3), (3, 3), (3, 3), (3, 3)]),
      expected=D.split([(24, 'Opportunities:', ' 2@4+3+3'), (25, 'Threats:', ' (A) (i) Outline the reasons')],
                       ['Opportunities:', 'Increased sales:', 'Economies of Scale:', 'Marketing:', 'Spreading Risk:', 'Threats:',
                        'Local consumers:', 'Local Customs', 'Environmental penalties:']),
      guidance=['The scheme prices (C) “' + S(24, '1@7(4+3)') + '” and “' + S(24, '3@6(3+3)') + '”; the larger allowance is not tied to a particular point.'])

dismiss = P(5, 'Workers who are unfairly dismissed are set for higher compensation awards due to the COVID-19 crisis.', 'Adapted from www.independent.ie')
D.add(3, 'q4ai', 'Q4(A)(i)', dismiss + '\n\n' + P(5, 'Outline the reasons for a fair dismissal, as set out under the Unfair Dismissals Acts 1977 to 2015.'),
      18, 'business-0-14', 'fair-dismissal-reasons', 5, [25, 26], 'Three reasons at 6 marks each (3 + 3: Name, Explain).',
      points('Reason', 3, (3, 3), ['Name', 'Explain']),
      expected=D.split([(25, 'Incapability:', ' 3@6(3+3)'), (26, 'Qualifications (misrepresentation', ' (ii) Explain, using an example')],
                       ['Incapability:', 'Incompetence:', 'Qualifications (misrepresentation by the employee):', 'Misconduct (improper and unacceptable behaviour):',
                        'Redundancy (due to closure, competition, decline in demand):', 'Contravening the law:']))
D.add(3, 'q4aii', 'Q4(A)(ii)', dismiss + '\n\n' + P(5, 'Explain, using an example, the term constructive dismissal.'), 7, 'business-0-14',
      'constructive-dismissal', 5, [26], 'Explain the term with an example for 7 marks (4 + 3).', [comps('Constructive dismissal', (4, 3), ['Explanation', 'Example'])],
      expected=D.split([(26, 'This occurs when an employee resigns', ' (4+3)')], ['This occurs when an employee resigns from their job', 'Example:']))
D.add(3, 'q4b', 'Q4(B)', dismiss + '\n\n' + P(5, 'Describe the impact trade disputes could have on any three stakeholders in a business.'), 15, 'business-0-14',
      'trade-dispute-stakeholder-impacts', 5, [27], 'Three stakeholders at 5 marks each (2 + 3).', points('Stakeholder', 3, (2, 3)),
      expected=D.split([(27, 'Government The government', ' (C) (i)Outline the rights')],
                       ['Government', 'Investors:', 'Consumers:', 'Suppliers:', 'Employer']),
      guidance=['The stakeholders are an open choice; the paper prints no list.'])
D.add(3, 'q4ci', 'Q4(C)(i)', dismiss + '\n\n' + P(5, 'Outline the rights of consumers under the Sale of Goods & Supply of Services Act 1980.'), 10, 'business-0-13',
      'sale-of-goods-consumer-rights', 5, [27, 28], 'Outline two rights at 5 marks each (2 + 3).', points('Right', 2, (2, 3)),
      expected=D.split([(28, 'Merchantable Quality:', ' (ii) Explain two forms')],
                       ['Merchantable Quality:', 'Guarantees:', 'Signs limiting consumer rights:', 'Unsolicited Goods:']),
      guidance=['The scheme prices each of (i) and (ii) at “' + S(27, '2@5 (2+3)') + '”.'])
D.add(3, 'q4cii', 'Q4(C)(ii)', dismiss + '\n\n' + P(5, 'Explain two forms of redress available to consumers for breach of the Act.'), 10, 'business-0-13',
      'consumer-redress-forms', 5, [27, 28], 'Explain two forms at 5 marks each (2 + 3).', points('Form of redress', 2, (2, 3)),
      expected=D.split([(28, 'Refund If a consumer', None)], ['Refund', 'Replacement', 'Repair']))

ryan = P(6, 'Ryan’s Pharmacy & Health Food Stores Chloe Taylor has recently been appointed Manager of Ryan’s Pharmacy & Health Food Stores. They provide pharmacy dispensing, medical services and they have also developed their own nutritional supplements to help meet the needs of their customers. Ryan’s Pharmacy & Health Food Stores have always fostered a culture of intrapreneurship.')
D.add(3, 'q5ai', 'Q5(A)(i)', ryan + '\n\n' + P(6, 'Explain the term intrapreneurship.'), 5, 'business-1-5', 'intrapreneurship', 6, [29],
      'Explain the term for 5 marks (2 + 3).', [comps('Intrapreneurship', (2, 3))],
      expected=D.split([(29, 'Intrapreneurship involves entrepreneurial activity', ' (ii) The following are the benefits')],
                       ['Intrapreneurship involves entrepreneurial activity within the business', 'E.g. Gmail']))
D.add(3, 'q5aii', 'Q5(A)(ii)', ryan + '\n\n' + P(6, 'Outline the benefits of intrapreneurship for Ryan’s Pharmacy & Health Food Stores.'), 15, 'business-1-5',
      'intrapreneurship-benefits', 6, [29], 'Outline three benefits at 5 marks each (2 + 3).', points('Benefit', 3, (2, 3)),
      expected=D.split([(29, 'Empowering employees:', ' 5 marks (2 + 3)')],
                       ['Empowering employees:', 'Creating an enterprise culture:', 'Improved morale', 'Improved industrial relations', 'Smaller labour turnover',
                        'Increased profits', 'Easier to recruit employees', 'Employees are more skilled at their job.'], drop=['•']))
D.add(3, 'q5bi', 'Q5(B)(i)', ryan + '\n\n' + P(6, 'Explain how a knowledge of Maslow’s Hierarchy of Needs theory may be used by a new manager such as Chloe Taylor to motivate their staff.'),
      20, 'business-2-11', 'maslow-motivating-staff', 6, [30], 'Five needs at 4 marks each (2 + 2: Name and Use).',
      points('Need', 5, (2, 2), ['Name', 'Use']),
      expected=D.split([(30, 'Physical Needs:', ' 5@4marks')],
                       ['Physical Needs:', 'Safety Needs:', 'Social Needs:', 'Esteem Needs:', 'Self-Actualisation Needs:'], drop=['•']))
D.add(3, 'q5bii', 'Q5(B)(ii)', ryan + '\n\n' + P(6, 'Outline two possible limitations of this theory of motivation.'), 5, 'business-2-11',
      'maslow-limitations', 6, [30, 31], 'Two limitations at 3 marks and 2 marks.', unequal('Limitation', [(3,), (2,)]),
      expected=D.split([(31, 'Individual Needs:', ' Discuss factors which influence')], ['Individual Needs:', 'Self-actualisation:', 'Value of Needs:']),
      guidance=['The scheme prices (ii) “' + S(30, '2 limitations 3marks 2marks') + '”; the larger allowance is not tied to a particular limitation. It heads (B) “(20 marks)”; the paper prints 25, as (i) and (ii) sum.'])
D.add(3, 'q5c', 'Q5(C)', ryan + '\n\n' + P(6, 'Discuss factors which influence a manager’s choice of communication methods with their stakeholders. Use examples to support your answer.'),
      15, 'business-2-12', 'communication-method-factors', 6, [31, 32], 'Three factors at 5 marks each (2 + 2 + 1).', points('Factor', 3, (2, 2, 1)),
      expected=D.split([(31, 'Accuracy All the facts', ' 3@5 (2+2+1)'), (32, 'Confidentiality', ' (A) Outline the stages')],
                       ['Accuracy', 'Appropriate language', 'Preparation', 'Confidentiality', 'Feedback']),
      guidance=['The scheme heads (C) “(20 marks)” and prices it “' + S(31, '3@5 (2+2+1)') + '”: 15 marks, as the paper prints.'])

switch = P(7, 'Nintendo Switch OLED: bigger, more vibrant screen Nintendo has updated its Switch Console with a new screen that is bigger and more vibrant than its predecessor. The Switch OLED Model boosts the display to seven inches. The updated Switch also increases its built-in storage, doubling it to 64GB. There is a new adjustable kickstand and its audio has also improved.', 'Adapted from The Irish Times')
D.add(3, 'q6a', 'Q6(A)', switch + '\n\n' + P(7, 'Outline the stages involved in the new product development process, following product screening, for this new Nintendo Switch OLED.'),
      20, 'business-4-14', 'new-product-development-stages', 7, [32, 33], 'Three stages using 7 (4 + 3), 7 (4 + 3) and 6 (3 + 3) marks.',
      unequal('Stage', [(4, 3), (4, 3), (3, 3)]),
      expected=D.split([(32, 'Concept Development This means', ' 3@7,7,6'), (33, 'Environmental feasibility:', ' (B) Discuss the factors')],
                       ['Concept Development', 'Feasibility Study', 'Prototype Development', 'Test Marketing', 'Launch']),
      guidance=['The larger allowances are not tied to particular stages.'])
D.add(3, 'q6b', 'Q6(B)', switch + '\n\n' + P(7, 'Discuss the factors a financial institution should consider when deciding to grant a business a loan.'), 20, 'business-3-16',
      'loan-decision-factors', 7, [33], 'Four factors at 5 marks each (2 + 3: Name, Explain).', points('Factor', 4, (2, 3), ['Name', 'Explain']),
      expected=D.split([(33, 'Amount/purpose/duration of the loan:', ' 4@5(2+3)')],
                       ['Amount/purpose/duration of the loan:', 'Ability to repay/business plan:', 'Credit History:', 'Security:']),
      guidance=['The scheme restates (B) as “' + S(33, 'whether to give a business a loan for a new or updated product.') + '”; the card follows the paper.'])
D.add(3, 'q6c', 'Q6(C)', switch + '\n\n' + P(7, 'Analyse the impact of new technology on business costs and on business opportunities. Provide examples to support your answer.'),
      20, 'business-3-21', 'new-technology-costs-and-opportunities', 7, [34], 'Four impacts at 5 marks each (2 + 2 + 1).', points('Impact', 4, (2, 2, 1)),
      expected=D.split([(34, 'Impact on staff', ' 4@5(2+2+1)')],
                       ['Impact on staff', 'Impact on communications', 'Impact on marketing', 'Impact on security', 'Other acceptable answers:']))

mccann = P(8, 'McCann Ltd is in the services industry, they provided the following financial information in 2021.') + '\n' + P(
    8, 'Sales €155,000', 'Current Assets (includes closing stock €21,360) €79,920', 'Current Liabilities €54,200', 'Long Term Loan €180,000',
    'Gross Profit €68,200', 'Net Profit €33,150', 'Ordinary Share Capital €300,000', 'Retained Earnings €30,000') + '\n\n' + P(
    8, 'Service Industry Average 2021', 'Net Profit Margin: 22%', 'Return on Investment: 10.1%', 'Current Ratio: 1.8:1', 'Acid Test Ratio: 1.2:1')
calc = P(8, 'Calculate the following for McCann Ltd:')
for key, roman, name, items in [
        ('q7ai', 'i', 'Net Profit Margin', ['Net Profit X 100 Sales 1', '= 21.4%']),
        ('q7aii', 'ii', 'Return on Investment', ['Net Profit X 100 Capital Employed', '(300,000 + 30,000 + 180,000) 1 = 6.5%']),
        ('q7aiii', 'iii', 'Current Ratio', ['Current Assets: Current Liabilities', '79,920: 54,200', '= 1.47:1']),
        ('q7aiv', 'iv', 'Acid Test Ratio', ['Current Assets – Closing Stock: Current Liabilities', '79,920 – 21,360: 54,200', '58,560: 54,200', '= 1.08:1'])]:
    D.add(3, key, f'Q7(A)({roman})', mccann + '\n\n' + calc + '\n' + P(8, f'({roman}) {name}'), 5, 'business-3-19',
          f"{name.lower().replace(' ', '-')}-calculation", 8, [35], f'Calculate the ratio for 5 marks.', [comps(name, (5,), ['Ratio'])],
          expected=D.expected(35, *items),
          guidance=['The scheme prints “' + S(35, '5 marks') + '” beside each of the four ratios, with no split.'])
D.add(3, 'q7b', 'Q7(B)', mccann + '\n\n' + P(8, 'Analyse the liquidity and profitability ratios for McCann Ltd for 2021, with reference to the industry average provided in the box above.'),
      20, 'business-3-19', 'liquidity-and-profitability-analysis', 8, [36],
      'Profitability and liquidity at 10 marks each: two trends at 3 marks and an implication 4 (2 + 2).',
      [response(i, area, [('trend-1', 'Trend 1', 3), ('trend-2', 'Trend 2', 3), ('implication', 'Implication', 4)])
       for i, area in ((1, 'Profitability'), (2, 'Liquidity'))],
      expected=D.split([(36, 'Profitability: Net Profit Margin:', ' 2 trends@')],
                       ['Profitability:', 'Net Profit Margin:', 'Return on Investment:', 'Liquidity:', 'The Current Ratio', 'The Acid Test Ratio']),
      guidance=['The scheme prints “' + S(36, '2 trends@ 3marks') + '” and “' + S(36, 'Implication 4 marks (2+2)') + '”.'])
D.add(3, 'q7c', 'Q7(C)', mccann + '\n\n' + P(8, 'Outline how implementing a credit control system may help the performance of a business.'), 20, 'business-3-16',
      'credit-control-benefits', 8, [37], 'Three points using 7 (4 + 3), 7 (4 + 3) and 6 (3 + 3) marks.', unequal('Point', [(4, 3), (4, 3), (3, 3)]),
      expected=D.split([(37, 'Lower risk of bankruptcy:', ' 7,7,6')],
                       ['Lower risk of bankruptcy:', 'Reduces bad debts:', 'Increased sales and profits:', 'Less borrowings:', 'Administration:']),
      guidance=['The larger allowances are not tied to particular points.'])

boyne = P(9, 'Michael Finegan is a third-generation farmer in Slane, Co. Meath. He is the brains behind Boyne Valley Cheese. He started milking goats on his farm in 2008. He uses the goat’s milk in the production of his award-winning varieties of cheese.', 'Adapted from the Irish Examiner')
D.add(3, 'q8ai', 'Q8(A)(i)', boyne + '\n\n' + P(9, 'Outline your understanding of the term unique selling point.'), 5, 'business-4-17', 'unique-selling-point', 9, [38],
      'Outline the term for 5 marks (3 + 2).', [comps('Unique selling point', (3, 2))],
      expected=D.split([(38, 'A unique selling point (USP)', ' (iii) The following are the implications')],
                       ['A unique selling point (USP) is the features that make a product stand out', 'For example, the USP of Audi']))
D.add(3, 'q8aii', 'Q8(A)(ii)', boyne + '\n\n' + P(9, 'Illustrate the implications for a business such as Boyne Valley Farmhouse Cheese when operating in a niche market.'),
      20, 'business-4-16', 'niche-market-implications', 9, [38, 39], 'Three implications using 7 (4 + 3), 7 (4 + 3) and 6 (3 + 3) marks.',
      unequal('Implication', [(4, 3), (4, 3), (3, 3)]),
      expected=D.split([(38, 'Lower Volume of Sales', None), (39, 'Less risk for the business:', ' (B) Discuss the factors')],
                       ['Lower Volume of Sales', 'Potential to Expand', 'Little or no competition:', 'High costs:', 'Less Investment:',
                        'Less risk for the business:', 'Loss of economies of scale:', 'Vulnerability:']),
      guidance=['The scheme numbers this response list “(iii)” and prices (ii) “' + S(38, '3@7,7,6 (4+3), (3+3)') + '”; the larger allowances are not tied to particular implications.'])
D.add(3, 'q8b', 'Q8(B)', boyne + '\n\n' + P(9, 'Discuss the factors that Michael Finegan should consider before deciding on the prices to charge consumers for his products.'),
      15, 'business-4-17', 'pricing-factors', 9, [39], 'Three factors at 5 marks each (2 + 3).', points('Factor', 3, (2, 3)),
      expected=D.split([(39, 'Input Costs', ' 3@5(2+3)')], ['Input Costs', 'Product Image', 'Consumers']))
D.add(3, 'q8ci', 'Q8(C)(i)', P(9, 'Name three sections of a business plan.'), 6, 'business-4-15', 'business-plan-sections', 9, [40],
      'Name three sections at 2 marks each.', [comps('Sections', (2, 2, 2), ['Section 1', 'Section 2', 'Section 3'])],
      expected=D.expected(40, '• Business Details', '• Objectives', '• Product Details', '• Market Details', '• Production Details', '• Financial Details'),
      guidance=['The scheme prices (i) “' + S(40, '3@2m') + '”.'])
D.add(3, 'q8cii', 'Q8(C)(ii)', P(9, 'Analyse the importance of creating and updating a business plan.'), 14, 'business-4-15', 'business-plan-importance', 9, [40],
      'Two reasons at 7 marks each (4 + 3).', points('Reason', 2, (4, 3)),
      expected=D.split([(40, 'To obtain finance:', ' 3@2m')], ['To obtain finance:', 'To measure performance:', 'To identify problems:', 'To formulate strategies:']),
      guidance=['The scheme prices (ii) “' + S(40, '2@7 (4+3)') + '”.'])

# ---------------------------------------------------------------- the sitting
for q in range(1, 13):
    D.atlas(1, q, 'p1', f'Every part of the 2022 Higher deferred Section 1 Question {q} was visually checked against the deferred booklet and scheme.')
D.atlas(2, 'ABQ', 'p2', 'Every part of the 2022 Higher deferred Applied Business Question was visually checked against the deferred booklet and scheme.')
for q in range(1, 9):
    D.atlas(3, q, 'p2', f'Every part of the 2022 Higher deferred Section 3 Question {q} was visually checked against the deferred booklet and scheme.')
D.emit({**{(1, str(q)): 10 for q in range(1, 13)}, (2, 'ABQ'): 80, **{(3, str(q)): 60 for q in range(1, 9)}},
       {1: 'No finite printed answer menu occurs in Section 1 (answer four of twelve). True/False labels, the matching grid, '
           'the abbreviations and the break-even cells are required answers for every row. Benefits, barriers, implications and '
           'the code-of-ethics benefit in the support notes are open examples. Each split part keeps its printed prompt and data.',
        2: 'The Applied Business Question is compulsory and has no printed choice: four insurance types, the PR methods, the '
           'community-development benefits and the economic variables are open examples drawn from the case.',
        3: 'No finite printed answer menu occurs in Section 3 (answer three of eight). Q1(A) names two required pairs, kept as one '
           'card each; Q4(B) asks for any three stakeholders and prints no list (open); Q2(B), Q3(B) and Q8(C)(i) ask for open '
           'ways, channels and sections. Support-note lists are open examples.'},
       {1: list(range(1, 37)), 2: list(range(1, 13)), 3: list(range(1, 13)), 'scheme': list(range(1, 43))})
