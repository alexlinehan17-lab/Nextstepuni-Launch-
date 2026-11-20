"""Card the SEC's 2023 Higher Level deferred Business sitting.

Sources (deferredexams/2023 and deferredmarkingschemes/2023, filed by Paper Trail as "<fileid>-deferred"):
Section 1 and Answerbook LC033ALP032EV (40 pages), Sections 2 and 3 LC033ALP041EV (12 pages), marking scheme
LC033ALP000EV (44 pages). Every page was rendered and read on 2026-11-19: the Section 1 booklet's cover,
instructions, the twelve short questions on pages 3-8 (answer eight; Q3's industrial-relations matching table,
Q6's Casey LTD figures, Q9's Bake and Cake LTD figures, Q10's insurance-principles table), the answerbook
instructions, graph paper and ruled answer pages; the Sections 2 and 3 booklet's cover, the Better Skincare case
(p2), Section 3 Questions 1-8 on pages 3-10 (answer four) with their extracts and Q6's TouchData LTD cash flow
forecast, and the back pages; the scheme's cover, p2 note on deferred marking schemes, p3 notes, the allocation
tables (pp4-8) and the support notes (pp9-43; 44 blank). The scheme circles Section 1 Q8's options (p12); they were
read from the rendered page.

The scheme prints nothing for Section 3 Question 3 (International Environment): no allocation in its tables
(pp6-8, which run Q1, Q2, Q4-Q8) and no support notes. Its p2 note says the scheme "will only have been finalised
for the questions attempted by the candidates who sat these examinations". Q3's three printed parts are carded at
the paper's printed marks with the one row "The scheme prints no answer for this part." and that note as guidance
(coordinator ruling 1, 19 Nov: a scheme-omitted task gets a card with the general criteria cited).

Its ABQ table prints (A)(i) as "2 @ 8m (2+3+2)"; the support notes print "2@8 (2+3+3)", which sums to 8, and the
card uses it. Section 3 Q1(A)'s support notes head the pairs "Employer and employee" and "Investor and the manager
of a business" where the paper prints "Investor and Entrepreneur" and "Employer and Employee"; the card follows the
paper.

Run from the repo root; reproduce.py runs it in the chain.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from deferred_lib import Sitting, response, comps, points, seq, unequal, LINK_NOTE  # noqa: E402

D = Sitting(2023, 'higher', {1: 'LC033ALP032EV', 2: 'LC033ALP041EV', 3: 'LC033ALP041EV'}, 'LC033ALP000EV')
L, S = D.lift, D.sch
W = lambda page, *s, **k: L(1, page, *s, **k)
P = lambda page, *s, **k: L(3, page, *s, **k)
SEQ10 = [0, 3, 5, 7, 9, 10]
CUM = 'For 0, 1, 2, 3, 4 or 5 correct answers, record 0, 3, 5, 7, 9 or 10 marks (the published sequence 3,2,2,2,1).'

# ---------------------------------------------------------------- Section 1 (answer eight of twelve; 10 marks each)
D.cumulative(1, 'q1', 'Q1', W(3, 'In the context of business, what do the following letters stand for? Write each answer in the space provided.')
             + '\n' + W(3, 'DIRT CAT PRSI ISME FDI'), 10, None, 'business-3-18', 'business-abbreviations', 3, [4, 9],
             'Give all five in full. The published cumulative sequence is 3 + 2 + 2 + 2 + 1.', SEQ10,
             D.expected(9, 'DIRT Deposit Interest Retention Tax', 'CAT Capital Acquisitions Tax', 'PRSI Pay Related Social Insurance',
                        'ISME Irish Small and Medium Enterprises', 'FDI Foreign Direct Investment'),
             [CUM], extra=['business-0-12', 'business-6-15'])
D.add(1, 'q2', 'Q2', W(3, 'Outline two enterprising skills/characteristics of successful entrepreneurs.'), 10, 'business-1-5',
      'enterprising-skills', 3, [4, 9], 'Two skills at 5 marks each (3 + 2).', points('Skill', 2, (3, 2)),
      expected=D.split([(9, 'Risk taking:', ' 10m 2x 5(3+2)')],
                       ['Risk taking:', 'Innovative/Creative:', 'Decisive/Decision Making:', 'Confident:', 'Flexible:', 'Future focused:',
                        'Proactive/Have initiative:']))
D.cumulative(1, 'q3', 'Q3', W(4, 'Column 1 is a list of business terms. Column 2 is a list of possible explanations for these terms. (One explanation does not refer to any of these terms.)',
                               'Match the two lists by placing the letter of the correct explanation under the relevant number below.')
             + '\n\n' + W(4, '1. Productivity Claim', '2. Token Stoppage', '3. Relativity Claim', '4. Work to Rule', '5. Comparability Claim',
                          'A Employees cease work for a short period of time.', 'B Employees only carry out duties as per their contract and nothing more.',
                          'C Employees seek a pay rise in line with inflation.',
                          'D If one person in the public sector receives a pay increase, others may also seek one.',
                          'E Employees request a pay rise because of an increased workload or changes introduced by their employer.',
                          'F Employees ask for a pay rise as employees doing similar work in a different sector receive a pay rise.'),
             10, None, 'business-0-14', 'industrial-relations-terms-matching', 4, [4, 10],
             'Match all five. The published cumulative sequence is 3 + 2 + 2 + 2 + 1.', SEQ10,
             {'page': 10, 'items': [{'id': f'e{n}', 'text': f'{n} — {x}'} for n, x in enumerate(S(10, '3 E A D B F').split()[1:], 1)]},
             ['Answer key (scheme “' + S(10, '3 E A D B F') + '”): 1 E; 2 A; 3 D; 4 B; 5 F. Explanation C is unused.', CUM])
D.add(1, 'q4', 'Q4', W(4, 'Distinguish between strategic planning and tactical planning in a business environment. Use an example in each case to illustrate your answer.'),
      10, 'business-2-13', 'strategic-versus-tactical-planning', 4, [4, 10], 'Each plan at 5 marks (3 + 2).',
      [comps('Strategic planning', (3, 2), i=1), comps('Tactical planning', (3, 2), i=2)],
      expected=D.split([(10, 'Strategic Plan A strategic plan', ' 10m 2x5(3+2)')], ['Strategic Plan', 'Example: To increase market share', 'Tactical Plan',
                                                                                      'Example: Launch a new advertising campaign']))
D.cumulative(1, 'q5', 'Q5', W(5, 'Write TRUE or FALSE for each of the following statements:') + '\n' + W(
    5, '1. The EU Court of Justice is the body responsible for drafting and proposing legislation.',
    '2. When passed, an EU Regulation becomes enforceable immediately as law in all Member States.',
    '3. The European Court of Auditors is responsible for ensuring the EU budget is spent efficiently.',
    '4. Members of the EU Commission are directly elected by EU citizens.', '5. The EU Competition Policy can prevent mergers from taking place.'),
    10, None, 'business-6-14', 'eu-statements-true-false', 5, [4, 10], 'Mark all five statements. The published cumulative sequence is 3 + 2 + 2 + 2 + 1.', SEQ10,
    {'page': 10, 'items': [{'id': f'e{n}', 'text': f'{n} — {x}'} for n, x in enumerate(S(10, 'False True True False True').split(), 1)]},
    ['Answer key (scheme “' + S(10, 'False True True False True') + '”).', CUM])
casey = W(5, '(i) Using the figures below for Casey LTD, calculate the Acid Test Ratio for 2022. Show your workings') + '\n' + W(
    5, 'Current Assets €94,000', 'Current Liabilities €64,000', 'Closing Stock €62,000')
D.add(1, 'q6i', 'Q6(i)', casey, 6, 'business-3-19', 'acid-test-ratio-calculation', 5, [4, 10], 'The acid test ratio: 6 marks (formula 2, three figures at 1 and the answer 1).',
      [response(1, 'Acid test ratio', [('formula', 'Formula', 2), ('assets', '94,000', 1), ('stock', '62,000', 1), ('liabilities', '64,000', 1), ('answer', '0.5 : 1', 1)])],
      expected=D.expected(10, 'Formula: Current Assets – Closing Stock : Current Liabilities', '32,000 : 64,000', '0.5 : 1'),
      guidance=['The scheme marks its workings ❷ ❶ ❶ ❶ and ❶ (“' + S(10, '94,000❶ - 62,000❶: 64,000❶') + '”).'])
D.add(1, 'q6ii', 'Q6(ii)', casey + '\n\n' + W(5, '(ii) If the Acid Test Ratio for Casey LTD for 2021 was 1.2:1, comment on the trend.'), 4, 'business-3-19',
      'acid-test-ratio-trend', 5, [4, 10], 'Comment for 4 marks (2 + 2).', [comps('Comment', (2, 2))],
      expected=D.split([(10, 'The Acid test Ratio has disimproved', ' 10m 6m 4m')], ['The Acid test Ratio has disimproved from 1.2:1 in 2021 to 0.5:1 in 2022.']),
      guidance=['The paper’s own (i) gives the 2022 ratio; the scheme’s is 0.5 : 1.'])
D.add(1, 'q7i', 'Q7(i)', W(6, '(i) Identify one example of a community development organisation.'), 2, 'business-5-16', 'community-development-organisation', 6, [4, 11],
      'Identify one organisation: 2 marks.', [comps('Organisation', (2,), ['Organisation'])],
      expected=D.expected(11, '• Area Partnership Companies (APCs)', '• LEADER', '• Local Enterprise Office (LEOs)'))
D.add(1, 'q7ii', 'Q7(ii)', W(6, '(i) Identify one example of a community development organisation.', '(ii) Describe two services provided by the organisation you have named in part (i).'),
      8, 'business-5-16', 'community-development-services', 6, [4, 11], 'Two services at 4 marks each (2 + 2).', points('Service', 2, (2, 2)),
      expected=D.split([(11, 'Area Partnership Companies (APCs) • APCs identify', ' 10m 2m')],
                       ['Area Partnership Companies (APCs)', 'LEADER • LEADER is a jointly funded', 'Local Enterprise Office (LEOs) • LEO’s are situated']))
D.cumulative(1, 'q8', 'Q8', W(6, 'Circle the correct option in the case of each of the following statements.') + '\n' + W(
    6, '(i) The chairperson / secretary has the casting vote if a vote is tied.', '(ii) EGM stands for an Emergency / Extraordinary General Meeting.',
    '(iii) Quorum is the minimum / maximum number of people required to hold a meeting.',
    '(iv) A manager delegating work to an employee is an example of upward / downward communication.',
    '(v) A memorandum is an example of written / visual communication.'),
    10, None, 'business-2-12', 'meetings-and-communication-options', 6, [4, 12], 'Circle all five. The published cumulative sequence is 3 + 2 + 2 + 2 + 1.', SEQ10,
    {'page': 12, 'items': [{'id': f'e{n}', 'text': S(12, word), 'detail': [S(12, line)]} for n, (word, line) in enumerate([
        ('chairperson', '(i) The chairperson/secretary in a meeting has the casting vote if a vote is tied.'),
        ('Extraordinary', '(ii) EGM stands for Emergency/Extraordinary general meeting.'),
        ('minimum', '(iii) Quorum is the minimum/maximum number of people needed to hold a meeting.'),
        ('downward', '(iv) A manager delegating work to an employee is an example of upward/downward communication.'),
        ('written', '(v) A memorandum is an example of written/visual communication.')], 1)]},
    ['The scheme rings the correct option in each statement (read from the rendered page 12): chairperson; Extraordinary; minimum; downward; written.', CUM])
bake = W(7, '(i) Using the following information, calculate the Breakeven Point for Bake and Cake LTD. Show your workings.') + '\n' + W(
    7, 'Fixed Costs €200,000', 'Variable Costs per unit €55', 'Forecast Output (Sales) 10,000 units', 'Selling Price €80')
D.add(1, 'q9i', 'Q9(i)', bake, 6, 'business-3-19', 'breakeven-point', 7, [4, 12], 'Breakeven point: 6 marks (fixed costs 2, the two unit figures 1 each, answer 2).',
      [response(1, 'Breakeven point', [('fixed', '€200,000', 2), ('price', '€80', 1), ('variable', '€55', 1), ('answer', '8,000 units', 2)])],
      expected=D.expected(12, 'Break-even Point = Fixed Costs Selling Price per unit – Variable Costs', 'Break-even Point = €200,000 ❷ €80❶ - €55❶ = 8,000 units❷'))
D.add(1, 'q9ii', 'Q9(ii)', bake + '\n\n' + W(7, '(ii) Calculate the Margin of Safety at forecast sales of 10,000 units for Bake and Cake LTD.'), 4, 'business-3-19',
      'margin-of-safety', 7, [4, 12], 'Margin of safety: 4 marks (the two figures 1 each, answer 2).',
      [response(1, 'Margin of safety', [('forecast', '10,000', 1), ('bep', '8,000', 1), ('answer', '2,000 units', 2)])],
      expected=D.expected(12, 'Margin of Safety = Forecast Sales – Breakeven point', 'Margin of Safety = 10,000❶ – 8,000❶ = 2,000 units❷'))
D.add(1, 'q10', 'Q10', W(7, 'Identify the correct insurance principle which corresponds with the explanation below.') + '\n' + W(
    7, 'The policy holder must benefit by the continued existence of the item and suffer financially from its loss.',
    'The insured must declare all material facts about the item they wish to insure when completing the application form.',
    'A policy holder cannot make a profit from insurance.', 'The insured cannot take out two policies for the same risk and collect from both insurers.'),
      10, 'business-3-17', 'insurance-principles-identified', 7, [4, 13], 'Four principles at 3, 3, 2 and 2 marks.',
      [response(i, f'Explanation {i}', [('answer', 'Principle', m)]) for i, m in enumerate([3, 3, 2, 2], 1)],
      expected=D.expected(13, 'Insurable Interest', 'Utmost Good Faith', 'Indemnity', 'Contribution'),
      guidance=['The scheme prices the four “' + S(13, '3+3+2+2') + '”; the larger allowances are not tied to particular principles.'])
D.add(1, 'q11', 'Q11', W(8, '“ECB raises interest rates by record 0.75%, signals more to come” rte.ie') + '\n\n'
      + W(8, 'Outline two impacts an increase in interest rates will have on Irish businesses.'), 10, 'business-5-15', 'interest-rate-increase-impacts', 8, [4, 13],
      'Two impacts at 5 marks each (3 + 2).', points('Impact', 2, (3, 2)),
      expected=D.split([(13, 'Increasing the cost of capital:', ' 10m 2 x 5m')],
                       ['Increasing the cost of capital:', 'Reduction in sales revenue:', 'Increasing the cost of short-term finance:', 'Reduced profit:',
                        'More difficult to attract investors:']))
D.add(1, 'q12', 'Q12', W(8, 'Outline two functions of the Data Protection Commissioner (DPC).'), 10, 'business-2-12', 'data-protection-commissioner-functions', 8, [4, 14],
      'Two functions at 5 marks each (3 + 2).', points('Function', 2, (3, 2)),
      expected=D.split([(14, 'Investigates complaints:', ' 10m 2 x 5m')],
                       ['Investigates complaints:', 'Informs people of their rights:', 'Conducts investigations of its own:',
                        'Promotes awareness and compliance by Data Controllers:', 'Identifies risks:', 'Co-operates with other data protection authorities:']),
      extra=['business-0-13'])

# ---------------------------------------------------------------- Section 2: the Applied Business Question (Better Skincare)
CASE = dict(label='CASE STUDY', title='Better Skincare', pages=[2])


def abq(key, ref, prompt, total, topic, concept, schemes, requirement, responses, expected, guidance=(LINK_NOTE,)):
    return D.add(2, f'abq-{key}', f'ABQ{ref}', prompt, total, topic, concept, 2, schemes, requirement, responses, list(guidance), expected, **CASE)


abq('a-i', '(A)(i)', L(2, 2, 'Describe one internal and one external source of new product ideas used by Joanne and Donal.'), 16, 'business-4-14',
    'new-product-idea-sources', [5, 15], 'One internal and one external source at 8 marks each (2 + 3 + 3: Name, Explain, Link).',
    [response(i, f'{kind} source', [('name', 'Name', 2), ('explain', 'Explain', 3), ('link', 'Link', 3)]) for i, kind in ((1, 'Internal'), (2, 'External'))],
    D.split([(15, 'Internal Hobbies/interests/skills:', ' (ii) Outline the challenges')],
            ['Internal', 'Hobbies/interests/skills:', 'Experiences:', 'External', 'State Agencies:', 'Friends and Family:']),
    guidance=[LINK_NOTE, 'The scheme’s table prints (A)(i) “' + S(5, '(i) 2 @ 8m (2+3+2)') + '”; its support notes print “' + S(15, '2@8 (2+3+3)')
              + '”, which sums to 8.'])
abq('a-ii', '(A)(ii)', L(2, 2, 'Outline the challenges faced by Joanne and Donal as a new business start-up.'), 14, 'business-4-15', 'start-up-challenges',
    [5, 15, 16], 'Two challenges at 7 marks each (2 + 3 + 2: State, Explain, Link).',
    [response(i, f'Challenge {i}', [('name', 'State', 2), ('explain', 'Explain', 3), ('link', 'Link', 2)]) for i in (1, 2)],
    D.split([(15, 'Finance: New business start-ups', ' 2@8 (2+3+3)'), (16, 'Competitors: It is very difficult', ' B Evaluate the implications')],
            ['Finance:', 'Competitors:', 'Sourcing Suppliers:', 'Finding suitable employees:', 'Ownership Structure:']))
abq('b', '(B)', L(2, 2, 'Evaluate the implications for Better Skincare of changing its ownership structure from a partnership to a private limited company.'), 30,
    'business-5-14', 'partnership-to-private-company', [5, 16, 17], 'Three implications at 9 marks each (3 + 3 + 3: State, Explain, Link) and an evaluation 3 (0, 1 or 3).',
    seq([response(i, f'Implication {i}', [('name', 'State', 3), ('explain', 'Explain', 3), ('link', 'Link', 3)]) for i in (1, 2, 3)],
        response(0, 'Evaluation', [('evaluate', 'Evaluation', 3)])),
    D.split([(16, 'Limited Liability:', ' 30m 3@9'), (17, 'Credit rating:', ' Evaluation required')],
            ['Limited Liability:', 'Credit rating:', 'Continuity of Existence:', 'Taxation:', 'Separate legal entity:', 'Control:']),
    guidance=[LINK_NOTE, 'The scheme prices the evaluation “' + S(16, 'Evaluation (0,1,3)') + '”.'])
D.cards[-1]['rubric']['responses'][-1]['allocations'][0]['permittedMarks'] = [0, 1, 3]
abq('c', '(C)', L(2, 2, 'Discuss the challenges for Better Skincare LTD of exporting outside the EU.'), 20, 'business-6-13', 'exporting-outside-eu-challenges', [5, 18],
    'Three challenges at 7 (2 + 3 + 2), 7 (2 + 3 + 2) and 6 (2 + 2 + 2) marks: State, Discuss, Link.',
    unequal('Challenge', [(2, 3, 2), (2, 3, 2), (2, 2, 2)], ['State', 'Discuss', 'Link']),
    D.split([(18, 'By expanding to markets outside the EU', ' 20m 7+7+6')],
            ['By expanding to markets outside the EU,', 'Eurozone countries benefit from the same currency,', 'It may be more difficult for export businesses',
             'By selling products in non-EU countries,', 'A knowledge of customs and culture', 'The business may encounter communication problems']),
    guidance=[LINK_NOTE, 'The larger allowances are not tied to particular challenges.'])

# ---------------------------------------------------------------- Section 3 (answer four of eight; 60 marks each)
rel = P(3, 'Relationships between Stakeholders There are a variety of stakeholders involved in business. Relationships between these stakeholders are constantly changing. At times they can be co-operative and at other times they can be competitive.')
D.add(3, 'q1a', 'Q1(A)', rel + '\n\n' + P(3, 'Describe one example of a co-operative relationship and one example of a competitive relationship between each of the following stakeholders:')
      + '\n' + P(3, 'Investor and Entrepreneur', 'Employer and Employee'), 20, 'business-0-12', 'stakeholder-co-operation-and-competition', 3, [6, 19],
      'Each pair at 10 marks, as the scheme prints it: 2 + (3 + 1) + (3 + 1).',
      [comps(pair, (2, 3, 1, 3, 1), None, i) for i, pair in ((1, 'Investor and Entrepreneur'), (2, 'Employer and Employee'))],
      expected=D.split([(19, 'A co-operative relationship exists', ' 20m 2@10')],
                       ['A co-operative relationship exists where both parties work towards a common goal.', 'An employer and employee could have a cooperative relationship',
                        'The investor and the manager of a business might have a cooperative relationship', 'A competitive relationship exists',
                        'The employer and the employee might have a competitive relationship over pay increases.',
                        'The employee and employer may have a competitive relationship over changes to working conditions.',
                        'The investor and manager may have a competitive relationship']),
      guidance=['The scheme prices (A) “' + S(19, '2@10(2+(3+1)+(3+1))') + '” and heads the pairs “' + S(19, '(i) Employer and employee (ii) Investor and the manager of a business.')
                + '”; the card follows the paper’s pairs.'])
D.add(3, 'q1b', 'Q1(B)', P(3, 'Illustrate, using examples, the legal duties of service providers as set out in the Sale of Goods and Supply of Services Act 1980.'), 15,
      'business-0-13', 'service-provider-duties', 3, [6, 20], 'Three duties at 5 marks each (2 + 3); an example is required.', points('Duty', 3, (2, 3)),
      expected=D.split([(20, 'Services must be provided with due care', ' 15m 3 x 5m')],
                       ['Services must be provided with due care and attention', 'The service provider must have the necessary qualifications',
                        'All materials used in the provision of the service must be of merchantable quality']),
      guidance=['The scheme requires an example: “' + S(20, 'Example required') + '”.'])
dismissed = P(3, 'Woman unfairly dismissed receives €6,900 compensation Adapted from rte.ie')
D.add(3, 'q1ci', 'Q1(C)(i)', dismissed + '\n\n' + P(3, '(i) Under the terms of the Unfair Dismissals Act 1977-2021, explain three grounds for dismissal that are deemed to be unfair.'),
      15, 'business-0-14', 'unfair-dismissal-grounds', 3, [6, 20, 21], 'Three grounds at 5 marks each (2 + 3).', points('Ground', 3, (2, 3)),
      expected=D.split([(20, 'Race An employee cannot', ' 25m 3 x 5m'), (21, 'Sexual Orientation', ' (ii) Outline the procedures')],
                       ['Race', 'Age', 'Membership of the Traveling Community', 'Pregnancy', 'Sexual Orientation', 'Trade Union membership', 'Beliefs',
                        'Legal procedures against the employer', 'Personal Leave', 'Making a protected disclosure', 'Incorrect procedures followed', 'Constructive Dismissal.']))
D.add(3, 'q1cii', 'Q1(C)(ii)', dismissed + '\n\n' + P(3, '(ii) Outline the procedures for dismissing an employee under the Unfair Dismissals Act 1977-2021.'), 10,
      'business-0-14', 'dismissal-procedures', 3, [6, 21, 22], 'Two procedures at 5 marks each (2 + 3).', points('Procedure', 2, (2, 3)),
      expected=D.split([(21, 'Counselling –', ' 2 x 5m (2+3)'), (22, 'and the consequences of not improving.', None)],
                       ['Counselling –', 'Formal Verbal Warning –', 'Written Warning –', 'Dismissal –', 'Right of Appeal –']))

inflation = P(4, 'Inflation estimated to have hit 9.5% in October according to the Central Statistics Office. Adapted from rte.ie')
kerry = P(4, 'At our core, we are committed to the highest standards of ethical behaviour. Adapted from kerry.com')
D.add(3, 'q2a', 'Q2(A)', inflation + '\n\n' + P(4, 'Discuss the impact of high inflation rates on the following:') + '\n' + P(4, 'Consumers Businesses Government'), 20,
      'business-5-15', 'inflation-impacts', 4, [6, 23], 'Consumers, businesses and government: 7 (4 + 3), 7 (4 + 3) and 6 (3 + 3) marks.',
      unequal('Heading response', [(4, 3), (4, 3), (3, 3)]),
      expected=D.split([(23, 'Consumers: The cost of living', ' 20 7m')], ['Consumers:', 'Business:', 'Government:']),
      guidance=['All three headings are required; the larger allowances are not tied to a particular heading.'])
D.add(3, 'q2bi', 'Q2(B)(i)', kerry + '\n\n' + P(4, '(i) Define the term business ethics.'), 5, 'business-5-17', 'business-ethics-term', 4, [6, 23],
      'Define the term for 5 marks (2 + 3).', [comps('Business ethics', (2, 3))],
      expected=D.split([(23, 'Ethics are moral principles', ' (ii) Outline the methods')], ['Ethics are moral principles that guide how a business makes decisions,']))
D.add(3, 'q2bii', 'Q2(B)(ii)', kerry + '\n\n' + P(4, '(ii) Outline the methods a business could use to improve its business ethics.'), 15, 'business-5-17',
      'improving-business-ethics', 4, [6, 23, 24], 'Three methods at 5 marks each (2 + 3).', points('Method', 3, (2, 3)),
      expected=D.split([(23, 'Clear ethical leadership:', ' 20m 5m'), (24, 'Draw up a Code of Ethics:', ' 2C (i) Explain the term')],
                       ['Clear ethical leadership:', 'Draw up a Code of Ethics:', 'Information and Training:', 'Whistle blowing:', 'Reward System:', 'Accountability:',
                        'Conduct an ethical audit:']))
D.add(3, 'q2ci', 'Q2(C)(i)', P(4, '(i) Explain the term secondary sector.'), 5, 'business-5-13', 'secondary-sector-term', 4, [6, 24],
      'Explain the term for 5 marks (2 + 3).', [comps('Secondary sector', (2, 3))],
      expected=D.split([(24, 'The secondary sector involves', ' 20m 5m')], ['The secondary sector involves using raw materials']))
D.add(3, 'q2cii', 'Q2(C)(ii)', P(4, '(ii) Outline the current trends facing businesses in the secondary sector in Ireland.'), 15, 'business-5-13',
      'secondary-sector-trends', 4, [6, 25], 'Three trends at 5 marks each (2 + 3).', points('Trend', 3, (2, 3)),
      expected=D.split([(25, 'Increased Costs:', ' 3 x 5m')], ['Increased Costs:', 'Skills Shortage:', 'Increased competition:', 'Brexit:', 'Capital investment:',
                                                              'Over-reliance on MNCs:']))

# Question 3: the scheme prints nothing (see the docstring).
NOTE = ['The deferred scheme prints no allocation or answer for Section 3 Question 3. Its note (p2): “' + S(2, 'the marking scheme will only have been finalised for the questions attempted by the candidates who sat these examinations.')
        + '” The marks shown are the paper’s.',
        'Its general notes (p3): “' + S(3, 'The support notes presented are neither exclusive nor complete.') + '” “'
        + S(3, 'Further relevant points of information presented by candidates are marked and rewarded on their merits.') + '”']
enlarge = P(5, 'European Union (EU) leaders have formally granted Ukraine and Moldova candidate status to become a member of the bloc. Adapted from rte.ie')
for key, ref, prompt, topic, concept in [
        ('q3a', 'Q3(A)', P(5, 'Outline the opportunities and challenges for Irish businesses arising from an enlarged European Union.'), 'business-6-14', 'eu-enlargement-opportunities-and-challenges'),
        ('q3b', 'Q3(B)', P(5, 'Explain the following international trade terms.') + '\n' + P(5, '(i) Trading Bloc (ii) Subsidy (iii) Balance of Payments (iv) Open Economy'),
         'business-6-13', 'international-trade-terms'),
        ('q3c', 'Q3(C)', P(5, '(i) Illustrate, using an example the term Global Business.') + '\n' + P(5, '(ii) Describe how developments in technology have facilitated the growth of globalisation.'),
         'business-6-15', 'global-business-and-technology')]:
    D.add(3, key, ref, enlarge + '\n\n' + prompt, 20, topic, concept, 5, [2, 3],
          'The paper prints 20 marks; the scheme prints no allocation for this part.',
          [response(1, 'The scheme prints no answer for this part.', [('unprinted', 'The scheme prints no answer for this part.', 20)])], NOTE,
          marknote='The deferred scheme prints no answer for this question. Mark it against the general notes the scheme gives for every question.')

contract = P(6, 'Manchester United terminates contract with Cristiano Ronaldo with immediate effect. Adapted from rte.ie')
forsa = P(6, 'The executive of the Fórsa trade union recommends that its members back new public sector pay deal. Adapted from The Irish Times')
D.add(3, 'q4a', 'Q4(A)', contract + '\n\n' + P(6, 'Illustrate, using examples the methods of terminating a legal contract.'), 20, 'business-0-12', 'contract-termination-methods', 6, [7, 26],
      'Three methods using 7 (2 + 3 + 2), 7 (2 + 3 + 2) and 6 (2 + 2 + 2) marks.', unequal('Method', [(2, 3, 2), (2, 3, 2), (2, 2, 2)]),
      expected=D.split([(26, 'Performance: Both parties', ' 20m 3@7,7,6')], ['Performance:', 'Frustration:', 'Breach:', 'Agreement:']),
      guidance=['The larger allowances are not tied to particular methods.'])
D.add(3, 'q4bi', 'Q4(B)(i)', forsa + '\n\n' + P(6, '(i) Discuss one benefit for employers of trade union membership in the workplace.'), 4, 'business-0-14',
      'trade-union-benefit-to-employers', 6, [7, 26, 27], 'One benefit for 4 marks (2 + 2).', [comps('Benefit', (2, 2))],
      expected=D.split([(26, 'It is faster for employers to negotiate', ' 25m 1 x 4m'), (27, 'Trade Unions can help ensure workplaces are safe.', ' (ii) Outline the reasons')],
                       ['It is faster for employers to negotiate', 'Trade unions can help build trust among the workforce.', 'Trade Unions can help ensure workplaces are safe.',
                        'It is easier for the employer to introduce change,']))
D.add(3, 'q4bii', 'Q4(B)(ii)', forsa + '\n\n' + P(6, '(ii) Outline the reasons, other than pay, for an industrial relations dispute.'), 21, 'business-0-14',
      'industrial-dispute-reasons', 6, [7, 27, 28], 'Three reasons at 7 marks each (4 + 3).', points('Reason', 3, (4, 3)),
      expected=D.split([(27, 'Disputes over working conditions/duties:', ' 3 x 7m'), (28, 'Discrimination:', ' 4C Describe the role')],
                       ['Disputes over working conditions/duties:', 'New work practices/New Technology:', 'Redundancies:', 'Demarcation issue:', 'Unfair Dismissal:',
                        'Trade Union recognition:', 'Discrimination:']))
D.add(3, 'q4c', 'Q4(C)', P(6, 'Describe the role of the Workplace Relations Commission in dealing with industrial relations disputes.'), 15, 'business-0-14',
      'wrc-role-in-disputes', 6, [7, 28, 29], 'Three roles at 5 marks each (2 + 3).', points('Role', 3, (2, 3)),
      expected=D.split([(28, 'Advisory Service:', ' 15m 3 x 5m'), (29, 'Adjudication:', None)],
                       ['Advisory Service:', 'Conciliation:', 'Mediation:', 'Adjudication:', 'Compliance/Inspection Service:']))

tayto = P(7, 'Tayto was established by Joe Murphy in 1954. The company believes that cross-functional teamwork is essential to its success. Management at Tayto value a supportive environment where open communication help people to grow and learn. Adapted from taytosnacks.ie')
D.add(3, 'q5a', 'Q5(A)', P(7, 'Contrast the role of an Entrepreneur with that of a Manager under three of the following headings:') + '\n' + P(7, 'Risk Reward Innovation Responsibility'),
      15, 'business-1-5', 'entrepreneur-versus-manager', 7, [7, 30], 'Three headings at 5 marks each (2 + 3).', points('Heading', 3, (2, 3)),
      expected=D.split([(30, 'Risk An entrepreneur takes', ' 15m 3 x 5m')], ['Risk', 'Reward', 'Innovation', 'Responsibility']),
      guidance=['A printed choice of three of the four headings: one card, every heading marked alike.'])
D.add(3, 'q5b', 'Q5(B)', tayto + '\n\n' + P(7, 'Evaluate the benefits and challenges for a business of operating a matrix organisational structure when developing its products.'), 25,
      'business-2-13', 'matrix-structure-evaluation', 7, [7, 30, 31], 'Four points at 5 marks each (2 + 3), at least one benefit and one challenge, and an evaluation 5 (0, 3 or 5).',
      seq(points('Point', 4, (2, 3)), response(0, 'Evaluation', [('evaluate', 'Evaluation', 5)])),
      expected=D.split([(30, 'Benefits Coordination:', ' 25m 4 x 5m'), (31, 'Improved Decision-making:', ' Evaluation required')],
                       ['Benefits', 'Coordination:', 'Improved Decision-making:', 'Product Development:', 'Improved Moral:', 'Challenges', 'Two Bosses:', 'Training:',
                        'Conflict:', 'Decision making:']),
      guidance=['The scheme requires “' + S(30, 'At least 1 of each required.') + '” and prices the evaluation “' + S(30, 'Evaluation (0,3,5)') + '”.'])
D.cards[-1]['rubric']['responses'][-1]['allocations'][0]['permittedMarks'] = [0, 3, 5]
D.add(3, 'q5c', 'Q5(C)', tayto + '\n\n' + P(7, 'Outline the implications for a business of a manager adopting McGregor’s Theory X approach to managing.'), 20, 'business-2-11',
      'theory-x-implications', 7, [7, 32], 'Four implications at 5 marks each (2 + 3).', points('Implication', 4, (2, 3)),
      expected=D.split([(32, 'Unmotivated Employees:', ' 20m 4 x 5m')],
                       ['Unmotivated Employees:', 'High labour turnover:', 'Industrial Relations problems:', 'Low productivity:', 'Management burn-out:',
                        'Lack of intrapreneurship:']))

remote = P(8, 'Improving Employee Performance During Remote Work A study shows that 83% of employees prefer working remotely in some capacity. Managers who are supervising their teams remotely are trying to find ways to manage workforce performance. Adapted from forbes.com')
cash = P(8, 'Below is a copy of the cashflow forecast for TouchData LTD for the first quarter of 2023.') + '\n' + P(
    8, 'January € February € March € Total €', 'Total Receipts 90,500 126,000 80,500 297,000', 'Total Payments 78,000 120,000 115,000 313,000',
    'Net Cash 12,500 6,000 B (16,000)', 'Opening Cash 5,500 A 24,000 C', 'Closing Cash 18,000 24,000 (10,500) (10,500)')
D.add(3, 'q6a', 'Q6(A)', remote + '\n\n' + P(8, 'Apart from remote work, discuss the impact of new technology on employees.'), 15, 'business-3-21', 'technology-impact-employees', 8, [8, 33],
      'Three impacts at 5 marks each (2 + 3).', points('Impact', 3, (2, 3)),
      expected=D.split([(33, 'New technology can change how an employee', ' 15m 3 x 5m')],
                       ['New technology can change how an employee performs their duties.', 'New job opportunities may be created', 'Redundancies may occur',
                        'Employees’ productivity may improve', 'Employees’ health and well-being may be affected']))
D.add(3, 'q6bi', 'Q6(B)(i)', remote + '\n\n' + P(8, '(i) Explain what is meant by Performance Appraisal.'), 5, 'business-3-20', 'performance-appraisal-term', 8, [8, 33],
      'Explain the term for 5 marks (2 + 3).', [comps('Performance appraisal', (2, 3))],
      expected=D.split([(33, 'Performance Appraisal refers to a review', ' (ii) Analyse how')], ['Performance Appraisal refers to a review of an employees’ performance/progress']))
D.add(3, 'q6bii', 'Q6(B)(ii)', remote + '\n\n' + P(8, '(ii) Analyse how Performance Appraisal can contribute to the successful running of a business.'), 15, 'business-3-20',
      'performance-appraisal-contribution', 8, [8, 33, 34], 'Three points at 5 marks each (2 + 3).', points('Point', 3, (2, 3)),
      expected=D.split([(33, 'Increases Productivity:', ' 20m 5m'), (34, 'High Staff Morale/Motivation:', ' 6C (i) Explain the reasons')],
                       ['Increases Productivity:', 'High Staff Morale/Motivation:', 'Identifies Training Needs:', 'Identifies suitable candidates for promotion:',
                        'Used to set Rewards:']))
D.add(3, 'q6ci', 'Q6(C)(i)', cash + '\n\n' + P(8, '(i) Explain the reasons why TouchData LTD would prepare a cashflow forecast.'), 10, 'business-3-16',
      'cash-flow-forecast-reasons', 8, [8, 34, 35], 'Two reasons at 5 marks each (2 + 3).', points('Reason', 2, (2, 3)),
      expected=D.split([(34, 'It will identify the sources and timing', ' 25m 2 x 5m'), (35, 'It will help TouchData Ltd gain access to finance', ' (ii) Calculate the figures')],
                       ['It will identify the sources and timing of cash inflows and outflows.', 'It acts as a benchmark', 'It will help TouchData Ltd identify periods of time in the future when the business will have an excess of expenditure',
                        'It will help TouchData Ltd identify periods of time in the future when the business will have a surplus', 'It will help TouchData Ltd gain access to finance']))
D.add(3, 'q6cii', 'Q6(C)(ii)', cash + '\n\n' + P(8, '(ii) Calculate the figures represented by the letters A, B and C on the cashflow forecast. (Show your answers in your answer book.)'), 9,
      'business-3-16', 'cash-flow-forecast-figures', 8, [8, 35], 'A, B and C at 3 marks each.',
      [response(1, 'Figures', [('a', 'A 18,000', 3), ('b', 'B (34,500)', 3), ('c', 'C 5,500', 3)])],
      expected=D.expected(35, 'A 18,000', 'B (34,500)', 'C 5,500'),
      guidance=['The scheme prices (ii) “' + S(8, '(ii) 9m (3+3+3)') + '” and prints the three figures (p35).'])
D.add(3, 'q6ciii', 'Q6(C)(iii)', cash + '\n\n' + P(8, '(iii) Explain how TouchData LTD might deal with the financial situation in March.'), 6, 'business-3-16',
      'cash-flow-deficit-response', 8, [8, 35], 'One way for 6 marks (3 + 3).', [comps('Way', (3, 3))],
      expected=D.split([(35, 'Short term finance:', ' 3m+3m+3m')], ['Short term finance:', 'Increase receipts:', 'Credit Control:', 'Reduce payments:']))

brands = P(9, 'Irish Brands Forge Ahead In Checkout’s Top 100 Brands Coco-Cola named as Ireland’s biggest selling brand for the 18th year in a row. Irish brands featured in the top ten include Tayto, Avonmore, Brennans and Jacobs. Adapted from Checkout.ie')
D.add(3, 'q7a', 'Q7(A)', brands + '\n\n' + P(9, 'Illustrate, using examples, the benefits of branding as a marketing tool for business.'), 20, 'business-4-17', 'branding-benefits', 9, [8, 36],
      'Four benefits at 5 marks each (1 + 2 + 2).', points('Benefit', 4, (1, 2, 2)),
      expected=D.split([(36, 'Customer Loyalty:', ' 20m 4 x 5m')], ['Customer Loyalty:', 'Premium prices can be charged:', 'Brand recognition:', 'Easier to introduce new products:',
                                                                    'Aids advertising:']))
D.add(3, 'q7bi', 'Q7(B)(i)', brands + '\n\n' + P(9, '(i) Explain the pricing strategies a marketing manager may use when launching a new product.'), 15, 'business-4-17',
      'new-product-pricing-strategies', 9, [8, 37], 'Three strategies at 5 marks each (2 + 3).', points('Strategy', 3, (2, 3)),
      expected=D.split([(37, 'Penetration Pricing:', ' 25m 3 x 5m')],
                       ['Penetration Pricing:', 'Price Skimming:', 'Predatory Pricing:', 'Premium pricing:', 'Psychological pricing:', 'Bundle pricing:',
                        'Cost plus pricing (mark-up pricing):', 'Tiered pricing:', 'Price discrimination:']))
D.add(3, 'q7bii', 'Q7(B)(ii)', P(9, '(ii) Draft and label the product life cycle diagram.'), 10, 'business-4-17', 'product-life-cycle-diagram', 9, [8, 38],
      'The diagram: each of five stages 1, the curve 2, title 1, sales 1, time 1.',
      [response(1, 'Product life cycle diagram', [*[(f'stage-{k}', f'Stage {k}', 1) for k in range(1, 6)], ('curve', 'Curve', 2), ('title', 'Title', 1),
                                                  ('sales', 'Sales', 1), ('time', 'Time', 1)])],
      expected=D.expected(38, 'Diagram 10m', '5@1m: each stage', 'Curve -2m', 'Title -1m', 'Sales 1m', 'Time 1m'),
      guidance=['The scheme draws its diagram as an image on page 38 (read from the rendered page: the sales curve through Introduction, Growth, Maturity, Saturation and Decline, against Sales and Time, titled Product Life Cycle); its text layer holds the allocation only.'])
D.add(3, 'q7c', 'Q7(C)', brands + '\n\n' + P(9, 'Outline the factors Coca-Cola should consider before choosing an appropriate medium of advertising for their business.'), 15,
      'business-4-17', 'advertising-medium-factors', 9, [8, 38, 39], 'Three factors at 5 marks each (2 + 3).', points('Factor', 3, (2, 3)),
      expected=D.split([(38, 'Cost: The business must consider', ' 15m 3 x 5m'), (39, 'Message:', None)],
                       ['Cost:', 'Nature of the Product:', 'Target Market:', 'Message:', 'Competitors:']))

gym = P(10, 'Gym+Coffee to add four new outlets as expansion continues The Cork-based Gym+Coffee clothing retail business is enjoying significant growth in 2022 on the back of new store openings. The athleisure brand, which provides a range of activewear, currently operates 13 outlets and is aiming to open a further four in 2023. Adapted from irishexaminer.ie')
D.add(3, 'q8ai', 'Q8(A)(i)', gym + '\n\n' + P(10, '(i) Distinguish between organic growth and inorganic growth in a business.'), 10, 'business-4-18', 'organic-versus-inorganic-growth', 10, [8, 40],
      'Each at 5 marks (2 + 3).', [comps('Organic growth', (2, 3), i=1), comps('Inorganic growth', (2, 3), i=2)],
      expected=D.split([(40, 'Organic Growth (internal)', ' (ii) Discuss reasons')], ['Organic Growth (internal)', 'Inorganic Growth (external)']))
D.add(3, 'q8aii', 'Q8(A)(ii)', gym + '\n\n' + P(10, '(ii) Discuss the reasons, other than increasing profit, for expansion of a business.'), 15, 'business-4-18',
      'expansion-reasons', 10, [8, 40, 41], 'Three reasons at 5 marks each (2 + 3).', points('Reason', 3, (2, 3)),
      expected=D.split([(40, 'Defensive Reasons:', ' 25m 2 x 5m'), (41, 'Offensive Reasons:', ' 8B Describe the first four')],
                       ['Defensive Reasons:', 'Offensive Reasons:', 'Psychological Reasons:']),
      guidance=['The scheme restates (ii) as “' + S(40, 'Discuss reasons, other than increasing profit, why entrepreneurs expand their business.') + '”; the card follows the paper.'])
D.add(3, 'q8b', 'Q8(B)', gym + '\n\n' + P(10, 'Describe the first four stages involved in the development process of a new product.'), 20, 'business-4-14', 'new-product-development-first-stages',
      10, [8, 41, 42], 'Four stages at 5 marks each (2 + 3).', points('Stage', 4, (2, 3)),
      expected=D.split([(41, 'Idea Generation:', ' 20m 4 x 5m'), (42, 'Concept Development:', ' 8C Contrast Debt Capital')],
                       ['Idea Generation:', 'Product Screening:', 'Concept Development:', 'Feasibility Study:']))
D.add(3, 'q8c', 'Q8(C)', P(10, 'Contrast Debt Capital and Equity Capital as sources of finance for business expansion.'), 15, 'business-3-16', 'debt-versus-equity-capital',
      10, [8, 42, 43], 'Three points at 5 marks each (2 + 3).', points('Point', 3, (2, 3)),
      expected=D.split([(42, 'Interest: Debt capital', ' 15m 3 x 5m'), (43, 'Risk:', None)],
                       ['Interest:', 'Cost/Repayments:', 'Tax Implications:', 'Control:', 'Collateral:', 'Risk:']))

# ---------------------------------------------------------------- the sitting
for q in range(1, 13):
    D.atlas(1, q, 'p1', f'Every part of the 2023 Higher deferred Section 1 Question {q} was visually checked against the deferred booklet and scheme.')
D.atlas(2, 'ABQ', 'p2', 'Every part of the 2023 Higher deferred Applied Business Question was visually checked against the deferred booklet and scheme.')
for q in range(1, 9):
    D.atlas(3, q, 'p2', f'Every part of the 2023 Higher deferred Section 3 Question {q} was visually checked against the deferred booklet and scheme.')
D.emit({**{(1, str(q)): 10 for q in range(1, 13)}, (2, 'ABQ'): 80, **{(3, str(q)): 60 for q in range(1, 9)}},
       {1: 'No finite printed answer menu occurs in Section 1 (answer eight of twelve). The matching grid, True/False column, circled options, '
           'abbreviations and insurance principles are required answers for every row. Skills, impacts and functions in the support notes are open examples.',
        2: 'The Applied Business Question is compulsory and has no printed choice: (A)(i) asks for one internal and one external source; the '
           'challenges and implications are open examples drawn from the case.',
        3: 'Q5(A) asks for three of four printed headings: one card, every heading marked alike (choice is not a route). Q2(A) names three required '
           'headings. Question 3 is carded without scheme rows: the deferred scheme prints nothing for it. Other support-note lists are open examples.'},
       {1: list(range(1, 41)), 2: list(range(1, 13)), 3: list(range(1, 13)), 'scheme': list(range(1, 45))})
