"""Author the 2026 Higher English Section 1 and Section 3 tasks.

Every question string is assembled from slices of the normalised SEC paper
text (asserted present); every answer-key or quoted scheme string is asserted
present in the normalised scheme page it cites. Run from the worktree root.
"""
from abq_authoring import response, notes
from pathlib import Path
import hashlib, json, re, unicodedata, fitz

year = 2026
S1, S23, MS = 'LC033ALP032EV', 'LC033ALP041EV', 'LC033ALP000EV'
docs = {S1: fitz.open(f'paper-trail-corpus/exampapers/{year}/{S1}.pdf'),
        S23: fitz.open(f'paper-trail-corpus/exampapers/{year}/{S23}.pdf'),
        MS: fitz.open(f'paper-trail-corpus/markingschemes/{year}/{MS}.pdf')}

def norm(s):
    s = unicodedata.normalize('NFKC', s)
    for a, b in {'Ɵ': 'ti', 'Ʃ': 'tt', 'Ō': 'ft', '‐': '-', '\xa0': ' ', ' ': ' '}.items():
        s = s.replace(a, b)
    return re.sub(r'\s+', ' ', s).strip()

text = {(f, i + 1): norm(p.get_text()) for f, d in docs.items() for i, p in enumerate(d)}

def lift(book, page, *snippets, sep='\n'):
    for s in snippets:
        assert s in text[(book, page)], (book, page, s)
    return sep.join(snippets)

def scheme(page, snippet):
    assert snippet in text[(MS, page)], (page, snippet)
    return snippet

def source(kind, f):
    return dict(fileid=f + '.pdf', sha256=hashlib.sha256(
        Path(f'paper-trail-corpus/{kind}/{year}/{f}.pdf').read_bytes()).hexdigest())

def sources(section):
    return dict(exampapers=source('exampapers', S1 if section == 1 else S23),
                markingschemes=source('markingschemes', MS))

def comps(label, marks, names=None, i=1):
    return response(i, label, [(f'component-{k}', names[k - 1] if names else f'Component {k}', m)
                               for k, m in enumerate(marks, 1)])

def points(label, n, marks, names=None):
    return [comps(f'{label} {i}', marks, names, i) for i in range(1, n + 1)]

def seq(*groups):
    out = []
    for g in groups:
        out.extend(g if isinstance(g, list) else [g])
    for i, r in enumerate(out, 1):
        r['id'] = f'response-{i}'
    return out

def evaluation(marks=2):
    return response(0, 'Evaluation', [('evaluate', 'Evaluation', marks)])

TARIFF = {1: 5, (3, 1): 7, (3, 2): 8, (3, 3): 8, (3, 4): 9, (3, 5): 10, (3, 6): 10, (3, 7): 11, (3, 8): 12}
created = []

def add(section, q, suffix, prompt, total, topic, concept, page, support, requirement, responses,
        guidance=None, extra=None, marknote=None, ref=None):
    part = ref if ref is not None else (''.join(
        f'({v.upper() if section == 3 and i == 0 else v})' for i, v in enumerate(suffix.split('-'))) if suffix else '')
    tariff = TARIFF[1] if section == 1 else TARIFF[(3, q)]
    c = dict(id=f'bus-{year}-hl-s{section}-q{q}{suffix}', year=year, level='higher', section=str(section),
             paperFileid=S1 if section == 1 else S23, paperPages=[page], sourceLabel='QUESTION PAPER',
             sourceTitle=f'{year} Business · Section {section} Question {q}',
             questionRef=f'{year} HL Section {section} Q{q}{part}', questionText=prompt, totalMarks=total,
             topicId=topic, conceptId=concept,
             rubric=dict(system='business', taskRequirements=requirement if isinstance(requirement, list) else [requirement],
                         guidance=guidance or [], responses=responses, schemeFileid=MS,
                         schemePages=[tariff] + support, markingGuideNote=marknote or notes))
    if extra:
        c['additionalTopicIds'] = extra
    marks = sum(a['maxMarks'] for r in responses for a in r['allocations'])
    assert marks == total, (c['id'], marks, total)
    assert len({r['id'] for r in responses}) == len(responses), c['id']
    created.append(c)
    return c

CUMULATIVE = 'For 0, 1, 2, 3, 4 or 5 correct answers, record 0, 3, 5, 7, 9 or 10 marks. The larger allowances are not tied to particular printed rows.'

def cumulative(q, prompt, topic, concept, page, support, key, extra=None):
    c = add(1, q, '', prompt, 10, topic, concept, page, support,
            'Complete all five answers. The published cumulative sequence is 3 + 2 + 2 + 2 + 1.',
            [comps('Correct answers', (10,), ['Total from the published sequence'])], [key, CUMULATIVE], extra,
            marknote='Use the official answer key and the published cumulative sequence. Each correct answer counts once.')
    c['rubric']['responses'][0]['allocations'][0]['permittedMarks'] = [0, 3, 5, 7, 9, 10]
    return c

# ---------------------------------------------------------------- Section 1
add(1, 1, '', lift(S1, 3, 'Describe two features of mass production.'), 10, 'business-4-15',
    'mass-production-features', 3, [13], 'Describe two features at 5 marks each (3 + 2).',
    points('Feature', 2, (3, 2)))
cumulative(2, lift(S1, 3, 'In the context of business, what do the following letters stand for? Write your answer in the spaces provided.',
                   'C.E.O.', 'E.D.I.', 'T.Q.M.', 'F.D.I.', 'S.E.M.'),
           'business-3-21', 'business-abbreviations', 3, [13],
           'Answer key: C.E.O.: ' + scheme(13, 'Chief Executive Officer') + '; E.D.I.: ' + scheme(13, 'Electronic Data Interchange')
           + '; T.Q.M.: ' + scheme(13, 'Total Quality Management') + '; F.D.I.: ' + scheme(13, 'Foreign Direct Investment')
           + '; S.E.M.: ' + scheme(13, 'Single European Market') + '.',
           ['business-2-13', 'business-2-12', 'business-6-15', 'business-6-14'])
add(1, 3, '', lift(S1, 4, 'Explain two differences between ad hoc meetings and Annual General Meetings.'), 10,
    'business-2-12', 'ad-hoc-versus-agm', 4, [14], 'Explain two differences at 5 marks each (3 + 2).',
    points('Difference', 2, (3, 2)))
add(1, 4, 'i', lift(S1, 4, 'Explain the term privatisation.'), 5, 'business-5-14', 'privatisation', 4, [15],
    'Explain the term for 5 marks (3 + 2).', [comps('Privatisation', (3, 2))])
add(1, 4, 'ii', lift(S1, 4, 'Outline one benefit of privatisation to the Irish economy.'), 5, 'business-5-14',
    'privatisation-benefit-economy', 4, [15], 'Outline one benefit for 5 marks (3 + 2).', [comps('Benefit', (3, 2))])
cumulative(5, lift(S1, 5, 'Indicate TRUE or FALSE after each of the following statements.',
                   '1. The European Court of Justice is responsible for ensuring the correct interpretation and application of EU laws by Member States.',
                   '2. The European Parliament draws up proposals for new EU laws.',
                   '3. The Council of the European Union (Council of Ministers) is the most important decision-making body in the EU.',
                   '4. The European Commission is responsible for the day-to-day management of the EU.',
                   '5. An EU regulation is not legally binding on Member States.'),
           'business-6-14', 'eu-institutions-true-false', 5, [16],
           'Answer key: ' + scheme(16, '1. True 2. False 3. True 4. True 5. False') + '.')
add(1, 6, 'i', lift(S1, 5, 'Describe the role of interest groups in business.'), 6, 'business-0-12',
    'interest-group-role', 5, [16], 'Describe the role for 6 marks (3 + 3).', [comps('Role of interest groups', (3, 3))])
add(1, 6, 'ii', lift(S1, 5, 'Explain using an example, an action an interest group of your choice has used.'), 4,
    'business-0-12', 'interest-group-action-example', 5, [16], 'Explain the action with an example for 4 marks (2 + 2).',
    [comps('Interest group action', (2, 2))],
    ['Scheme: “' + scheme(16, 'Interest group named and their specific activities explained.') + '” The interest group is an open choice, not a printed menu.'])
cumulative(7, lift(S1, 6, 'Circle the correct option in the case of each of the following statements.',
                   '(i) A Co-operative business is owned by members/shareholders.',
                   '(ii) In general, a Partnership business continues/ceases to exist if a partner leaves.',
                   '(iii) A Private Limited Company has limited/unlimited liability.',
                   '(iv) A State-owned Enterprise is known as a Public/Statutory company.',
                   '(v) A Strategic Alliance is a permanent/temporary business arrangement.'),
           'business-5-14', 'ownership-structures-options', 6, [17],
           'Answer key: ' + scheme(17, '(i) Members (ii) Ceases (iii) Limited Liability (iv) Statutory (v) Temporary') + '.',
           ['business-4-18'])
add(1, 8, '', lift(S1, 6, 'Outline two factors a business should consider before choosing to set up in a local community.'), 10,
    'business-5-16', 'local-community-location-factors', 6, [18], 'Outline two factors at 5 marks each (3 + 2).',
    points('Factor', 2, (3, 2)))
cumulative(9, '\n'.join([
    lift(S1, 7, 'Column 1 is a list of business terms. Column 2 is a list of possible explanations for these terms. (One explanation does not refer to any of these terms)'),
    '', lift(S1, 7, 'Column 1', '1. Risk Management', '2. Indemnity', '3. Contribution', '4. Insurance Broker', '5. Actuary'),
    '', lift(S1, 7, 'Column 2',
             'A. A person or business who sells insurance on behalf of several different insurance companies.',
             'B. Used by insurance firms to calculate compensation when an item is insured for less than its actual value.',
             'C. A planned approach used by businesses to identify potential risks that might occur.',
             'D. You cannot be better off after a loss has occurred than you were before the loss happened.',
             'E. The insured cannot insure an item with more than one insurance company.',
             'F. Calculates the premium to be paid by the insured.'),
    '', lift(S1, 7, 'Match the two lists by placing the letter of the correct explanation under the relevant number below.')]),
    'business-3-17', 'insurance-terms-matching', 7, [19],
    'Answer key: 1 C; 2 D; 3 E; 4 A; 5 F. Explanation B is unused.' if scheme(19, '1. 2. 3. 4. 5. C D E A F') else '')
breakeven = lift(S1, 7, 'The Finance Manager of Delectable Delights Ltd. has produced the following figures:',
                 'Forecast Output (Sales) 50,000 units', 'Selling Price per unit € 20', 'Fixed Costs € 300,000',
                 'Variable Cost per unit € 10') + '\n\n' + lift(S1, 7, 'Using the information provided calculate the:')
OWN = 'The scheme marks its shaded answers on the candidate’s own figures (“' + scheme(19, 'Own figures shaded') + '”).'
add(1, 10, 'i', breakeven + '\n' + lift(S1, 7, '(i) Break-Even Point in units'), 4, 'business-3-19', 'break-even-point-units', 7, [19],
    'Award the four published one-mark points (1 + 1 + 1 + 1).',
    [response(1, 'Break-even point', [('formula', 'Formula: Fixed Costs ÷ (Selling Price − Variable cost per unit)', 1),
                                      ('fixed', 'Fixed costs: ' + scheme(19, '300,000'), 1), ('contribution', 'Selling price − variable cost: 20 − 10', 1),
                                      ('answer', 'Answer: ' + scheme(19, '30,000 units'), 1)])], [OWN])
add(1, 10, 'ii', breakeven + '\n' + lift(S1, 7, '(ii) Profit at Forecast Output'), 3, 'business-3-19', 'profit-at-forecast-output', 7, [19],
    'Award the three published one-mark points (1 + 1 + 1).',
    [response(1, 'Profit at forecast output', [('revenue', 'Total revenue (50,000 × 20): ' + scheme(19, '1,000,000'), 1),
                                               ('costs', 'Total costs [300,000 + (50,000 × 10)]: ' + scheme(19, '800,000'), 1),
                                               ('answer', 'Profit: ' + scheme(19, '€200,000'), 1)])],
    ['Scheme working: ' + scheme(19, '(50,000 × 20) −[300,000 + (50,000 × 10)]') + '.', OWN])
add(1, 10, 'iii', breakeven + '\n' + lift(S1, 7, '(iii) Margin of Safety in units.'), 3, 'business-3-19', 'margin-of-safety-units', 7, [19],
    'Award the three published one-mark points (1 + 1 + 1).',
    [response(1, 'Margin of safety', [('forecast', 'Forecast output: ' + scheme(19, '50,000'), 1), ('breakeven', 'Break-even point: ' + scheme(19, '30,000'), 1),
                                      ('answer', 'Answer: ' + scheme(19, '20,000 units'), 1)])],
    ['Margin of safety = forecast output − break-even point. The break-even point is calculated from the same figures.', OWN])
add(1, 11, '', lift(S1, 8, 'Explain, using examples, the difference between Organic and Inorganic Growth.'), 10, 'business-4-18',
    'organic-versus-inorganic-growth', 8, [20], 'Explain both required terms at 5 marks each (3 + 2), with an example for each.',
    [comps('Organic growth', (3, 2), i=1), comps('Inorganic growth', (3, 2), i=2)],
    ['Scheme: “' + scheme(20, 'Example required') + '” for organic and for inorganic growth.'])
add(1, 12, '', lift(S1, 8, 'Explain two implications for a business of a manager adopting a McGregor Theory X approach to management.'), 10,
    'business-2-11', 'theory-x-implications', 8, [21], 'Explain two implications at 5 marks each (3 + 2).',
    points('Implication', 2, (3, 2)))

# ---------------------------------------------------------------- Section 3
add(3, 1, 'a-i', lift(S23, 3, 'Explain three elements of a legally binding contract, apart from ‘offer and acceptance’. Use an example in each case.'),
    15, 'business-0-12', 'contract-elements-with-examples', 3, [28, 29],
    'Explain three elements at 5 marks each: Element 2, Explain 2, Example 1.',
    points('Element', 3, (2, 2, 1), ['Element', 'Explain', 'Example']),
    ['Scheme: “' + scheme(28, 'Example required for full marks.') + '” Offer and acceptance are excluded by the question.'])
add(3, 1, 'a-ii', lift(S23, 3, 'Illustrate the difference between condition and warranty in relation to a contract.'),
    5, 'business-0-12', 'condition-versus-warranty', 3, [29], 'Illustrate the difference for 5 marks (2 + 3): Difference and Example.',
    [comps('Condition and warranty', (2, 3), ['Difference', 'Example'])],
    ['Scheme: “' + scheme(29, 'Example Required.') + '”'])
add(3, 1, 'b', lift(S23, 3, 'Describe one example of a co-operative relationship and one example of a competitive relationship that could arise between the following stakeholders:',
                    '• Business and a competitor', '• Government and a business'),
    20, 'business-0-12', 'stakeholder-cooperation-and-competition', 3, [30, 31],
    'Both stakeholder pairs and both relationship types are required: 10 marks per pair, 2 @ 5 marks (4 + 1).',
    seq(comps('Business and a competitor: co-operative', (4, 1)), comps('Business and a competitor: competitive', (4, 1)),
        comps('Government and a business: co-operative', (4, 1)), comps('Government and a business: competitive', (4, 1))))
add(3, 1, 'c', lift(S23, 3, "Brian O'Driscoll served with notice over 'misleading commercial practice' on social media posts.",
                    "This is the first time the CCPC have taken action against social media influencers, with O'Driscoll investigated over his Instagram social media account.")
    + '\n\n' + lift(S23, 3, 'Evaluate the powers of the Competition and Consumer Protection Commission in relation to breaches of Consumer Law.'),
    20, 'business-0-13', 'ccpc-powers-evaluation', 3, [32, 33],
    'Evaluate three powers at 6 marks each (3 + 3), plus 2 marks for evaluation.',
    seq(points('Power', 3, (3, 3)), evaluation()), ['Scheme: “' + scheme(33, 'Evaluation Required.') + '”'])

add(3, 2, 'a', lift(S23, 4, 'Describe the characteristics of an environmentally responsible business.'), 20, 'business-5-17',
    'environmentally-responsible-characteristics', 4, [34],
    'Describe three characteristics using 7 (4 + 3), 7 (4 + 3) and 6 (3 + 3) marks.',
    seq(comps('Characteristic 1', (4, 3)), comps('Characteristic 2', (4, 3)), comps('Characteristic 3', (3, 3))),
    ['The larger allowances are not fixed to particular characteristics.'])
add(3, 2, 'b', lift(S23, 4, 'Analyse how economic variables (factors) in the Irish economy have an impact on business.'), 20,
    'business-5-15', 'economic-variables-impact', 4, [35, 36, 37],
    'Analyse three variables using 7 (3 + 1 + 3), 7 (3 + 1 + 3) and 6 (3 + 1 + 2) marks: Variable, Development, Impact.',
    seq(comps('Variable 1', (3, 1, 3), ['Variable', 'Development', 'Impact']),
        comps('Variable 2', (3, 1, 3), ['Variable', 'Development', 'Impact']),
        comps('Variable 3', (3, 1, 2), ['Variable', 'Development', 'Impact'])),
    ['The larger allowances are not fixed to particular variables.'])
paddy = lift(S23, 4, 'The Paddy Box aims to connect those around the world to Ireland by allowing customers to create and ship a box of ‘Irishness’ around the globe.')
add(3, 2, 'c-i', paddy + '\n\n' + lift(S23, 4, 'Explain using an example other than the Paddy Box, the term Indigenous firm.'), 6,
    'business-5-13', 'indigenous-firm-example', 4, [37], 'Explain the term with an example for 6 marks (3 + 3).',
    [comps('Indigenous firm', (3, 3))], ['The Paddy Box is excluded as the example.'])
add(3, 2, 'c-ii', paddy + '\n\n' + lift(S23, 4, 'Outline the challenges facing Indigenous firms.'), 14, 'business-5-13',
    'indigenous-firm-challenges', 4, [38], 'Outline two challenges at 7 marks each (4 + 3).', points('Challenge', 2, (4, 3)))

trade = lift(S23, 5, 'INTERNATIONAL TRADE', 'Net Exports grew by 25.8% (€11.9bn) in Q4 2024')
wto = lift(S23, 5, 'The key objective of the World Trade Organisation (WTO) is to promote free trade.')
add(3, 3, 'a-i', trade + '\n\n' + wto + '\n\n' + lift(S23, 5, 'Explain the term free trade.'), 5, 'business-6-13', 'free-trade',
    5, [39], 'Explain the term for 5 marks (2 + 3).', [comps('Free trade', (2, 3))])
add(3, 3, 'a-ii', trade + '\n\n' + wto + '\n\n' + lift(S23, 5, 'Outline benefits of international trade for the Irish economy.'), 15,
    'business-6-13', 'international-trade-benefits-ireland', 5, [40], 'Outline three benefits at 5 marks each (2 + 3).',
    points('Benefit', 3, (2, 3)))
add(3, 3, 'b-i', trade + '\n\n' + lift(S23, 5, 'Illustrate what is meant by the term invisible export, with reference to the Irish economy.'), 6,
    'business-6-13', 'invisible-export', 5, [41], 'Illustrate the term for 6 marks (3 + 3). An example is required.',
    [comps('Invisible export', (3, 3))], ['Scheme: “' + scheme(41, 'Example Required') + '”'])
add(3, 3, 'b-ii', trade + '\n\n' + lift(S23, 5, 'Explain the impact ICT has had on Irish businesses engaged in international trade.'), 14,
    'business-2-12', 'ict-impact-international-trade', 5, [42, 43], 'Explain two impacts at 7 marks each (4 + 3).',
    points('ICT impact', 2, (4, 3)),
    ['The scheme names the two components Impact and Technology without fixing which carries 4 marks; both are needed for each point.'],
    extra=['business-6-13'])
add(3, 3, 'c', lift(S23, 5, 'Ireland should remain in the EU') + '\n\n'
    + lift(S23, 5, 'Do you agree with this statement?', 'Justify reasons for your answer, from the point of view of business owners.'),
    20, 'business-6-14', 'remain-in-eu-business-view', 5, [44, 45],
    'State your position for 2 marks, then justify three reasons at 6 marks each (3 + 3) from the point of view of business owners.',
    seq(response(1, 'Position', [('position', 'Agree or disagree', 2)]), points('Reason', 3, (3, 3))),
    ['The scheme lists Yes reasons and No reasons separated by “' + scheme(44, 'OR') + '”; either position is accepted when justified. The stance is an open answer, not a printed choice of tasks.'])
created[-1]['rubric']['responses'][0]['allocations'][0]['permittedMarks'] = [0, 2]

add(3, 4, 'a-i', lift(S23, 6, 'Define discrimination as set out in the Employment Equality Act 1998/2015.'), 12, 'business-0-14',
    'employment-equality-discrimination', 6, [46], 'Define the term for 12 marks (8 + 4).', [comps('Discrimination', (8, 4))])
add(3, 4, 'a-ii', lift(S23, 6, 'Distinguish between constructive dismissal and unfair dismissal.'), 8, 'business-0-14',
    'constructive-versus-unfair-dismissal', 6, [46], 'Explain both required terms at 4 marks each (2 + 2).',
    [comps('Constructive dismissal', (2, 2), i=1), comps('Unfair dismissal', (2, 2), i=2)])
ir = lift(S23, 6, 'Positive industrial relations are important to business success.')
add(3, 4, 'b-i', ir + '\n\n' + lift(S23, 6, 'Discuss the ways a business can promote and maintain good industrial relations.'), 10,
    'business-0-14', 'promoting-good-industrial-relations', 6, [47], 'Discuss two ways at 5 marks each (4 + 1).',
    points('Way', 2, (4, 1)))
add(3, 4, 'b-ii', ir + '\n\n' + lift(S23, 6, 'Outline the possible impact of strike action on each of the following:', '• Customers', '• Investors'),
    10, 'business-0-14', 'strike-impact-customers-investors', 6, [48],
    'Both named stakeholders are required at 5 marks each (4 + 1).',
    [comps('Customers', (4, 1), i=1), comps('Investors', (4, 1), i=2)])
add(3, 4, 'c', lift(S23, 6, 'The Workplace Relations Commission (WRC) is an independent body which was established on 1st October 2015 under the Workplace Relations Act 2015.')
    + '\n\n' + lift(S23, 6, 'Evaluate the role of the Workplace Relations Commission in dealing with industrial disputes.'),
    20, 'business-0-14', 'wrc-role-evaluation', 6, [49, 50], 'Evaluate three roles at 6 marks each (3 + 3), plus 2 marks for evaluation.',
    seq(points('Role', 3, (3, 3)), evaluation()), ['Scheme: “' + scheme(50, 'Evaluation Required.') + '”'])

add(3, 5, 'a-i', lift(S23, 7, 'Illustrate your understanding of the term Enterprise.'), 6, 'business-1-5', 'enterprise-term',
    7, [51], 'Illustrate the term for 6 marks (3 + 3): Explain and Example.', [comps('Enterprise', (3, 3), ['Explain', 'Example'])])
add(3, 5, 'a-ii', lift(S23, 7, 'Explain the benefits of enterprise to your local economy.'), 14, 'business-1-5',
    'enterprise-local-economy-benefits', 7, [51], 'Explain two benefits at 7 marks each (4 + 3).', points('Benefit', 2, (4, 3)))
add(3, 5, 'b', lift(S23, 7, 'Good communication is important because it helps people work well together, keeps employees involved, and helps a business succeed.')
    + '\n\n' + lift(S23, 7, 'Discuss the barriers to effective communication faced by a business.'), 20, 'business-2-12',
    'communication-barriers', 7, [52], 'Discuss four barriers at 5 marks each (2 + 3).', points('Barrier', 4, (2, 3)))
add(3, 5, 'c', lift(S23, 7, 'Evaluate factors that influence the leadership style adopted by business managers. Provide examples to support your answer.'),
    20, 'business-2-11', 'leadership-style-factors', 7, [53, 54],
    'Evaluate three factors at 6 marks each (Factor 2, Explain 2, Example 2), plus 2 marks for evaluation.',
    seq(points('Factor', 3, (2, 2, 2), ['Factor', 'Explain', 'Example']), evaluation()),
    ['Scheme: “' + scheme(54, 'Evaluation Required.') + '”'])

ballyfin = lift(S23, 8, 'Ballyfin Demesne Ltd is a 5-star luxury country house hotel in Co. Laois. This award-winning hotel offers the very best of Irish hospitality in the most beautiful surroundings imaginable. They have embarked on a major sustainability enhancement journey. They own a fleet of electric vehicles to maintain the grounds. Ballyfin has a well-stocked cellar with wine from all over the world. To maintain its award-winning reputation, management conducts periodic one-to-one meetings with team members.')
add(3, 6, 'a', ballyfin + '\n\n' + lift(S23, 8, 'Discuss the importance of three Human Resource Management functions for a business such as Ballyfin Demesne Ltd, apart from pay and rewards.'),
    20, 'business-3-20', 'hrm-functions-ballyfin', 8, [55, 56],
    'Discuss three functions using 7 (2 + 3 + 2), 7 (2 + 3 + 2) and 6 (2 + 2 + 2) marks: HR function, Explain, Reference.',
    seq(comps('HR function 1', (2, 3, 2), ['HR function', 'Explain', 'Reference']),
        comps('HR function 2', (2, 3, 2), ['HR function', 'Explain', 'Reference']),
        comps('HR function 3', (2, 2, 2), ['HR function', 'Explain', 'Reference'])),
    ['Pay and rewards are excluded by the question. The larger allowances are not fixed to particular functions.'])
add(3, 6, 'b', ballyfin + '\n\n' + lift(S23, 8, 'Illustrate the types of taxation that Ballyfin Demesne Ltd should be aware of.'), 20,
    'business-3-18', 'taxation-types-ballyfin', 8, [57, 58],
    'Illustrate four types of taxation at 5 marks each: Taxation 2, Explain 2, Reference 1.',
    points('Tax', 4, (2, 2, 1), ['Taxation', 'Explain', 'Reference']))
add(3, 6, 'c', lift(S23, 8, 'Discuss the strategies used to manage change in a business.'), 20, 'business-3-21',
    'managing-change-strategies', 8, [59, 60], 'Discuss four strategies at 5 marks each: Strategy 2, Explain 3.',
    points('Strategy', 4, (2, 3), ['Strategy', 'Explain']))

coke = lift(S23, 9, 'Coca-Cola has a range of popular products, including Coca-Cola Original, Diet Coke, Coca-Cola Zero Sugar and Sprite, which are widely recognised and enjoyed by consumers around the world.')
add(3, 7, 'a', coke + '\n\n' + lift(S23, 9, 'Draw the Product Life Cycle diagram for a product of your choice and describe the action a business may take at each stage.'),
    20, 'business-4-17', 'product-life-cycle-diagram-and-actions', 9, [61, 62],
    ['Diagram 10 marks: title (product) 1, two axis labels 1 each, curve 2 and five stages 1 each.',
     'Actions 10 marks: describe an action at each of the five stages, 2 marks each.'],
    [response(1, 'Diagram', [('title', 'Title (product)', 1), ('sales-axis', 'Axis: Sales', 1), ('time-axis', 'Axis: Time', 1),
                             ('curve', 'Curve', 2), ('introduction', 'Introduction', 1), ('growth', 'Growth', 1),
                             ('maturity', 'Maturity', 1), ('saturation', 'Saturation', 1), ('decline', 'Decline', 1)])]
    + [response(i, f'{stage}: action', [('action', 'Action described', 2)]) for i, stage in
       enumerate(['Introduction', 'Growth', 'Maturity', 'Saturation', 'Decline'], 2)],
    ['The product is an open choice. The diagram and the stage actions are both required parts of one printed task.'])
swift = lift(S23, 9, 'Businesses use ratio analysis to observe trends in their financial accounts. These trends are used to aid future decision making.', sep=' ') \
    + '\n\n' + lift(S23, 9, 'Swift Ltd is a company in the tech industry. They provided the following financial information for 2025:',
                    'Sales € 450,000', 'Net Profit € 33,750', 'Current assets (including closing stock € 90,000) € 174,375',
                    'Current liabilities € 93,750', 'Long term loan € 250,000', 'Ordinary share capital € 350,000',
                    'Retained earnings € 75,000')
calc = swift + '\n\n' + lift(S23, 9, 'Calculate the following for Swift Ltd.') + '\n'
OWN3 = 'The scheme marks its shaded figures on the candidate’s own figures (“' + scheme(63, 'Own figures shaded') + '”).'
add(3, 7, 'b-i', calc + lift(S23, 9, '(i) Net profit margin'), 4, 'business-3-19', 'net-profit-margin', 9, [63],
    'Award the four published one-mark points.',
    [response(1, 'Net profit margin', [('formula', 'Formula: Net profit ÷ Sales × 100', 1), ('profit', 'Net profit: ' + scheme(63, '33,750'), 1),
                                       ('sales', 'Sales: ' + scheme(63, '450,000'), 1), ('answer', 'Answer: ' + scheme(63, '7.5 %'), 1)])], [OWN3])
add(3, 7, 'b-ii', calc + lift(S23, 9, '(ii) Current ratio'), 4, 'business-3-19', 'current-ratio', 9, [63],
    'Award the four published one-mark points.',
    [response(1, 'Current ratio', [('formula', 'Formula: ' + scheme(63, 'Current Assets : Current liabilities'), 1),
                                   ('assets', 'Current assets: ' + scheme(63, '174,375'), 1), ('liabilities', 'Current liabilities: ' + scheme(63, '93,750'), 1),
                                   ('answer', 'Answer: ' + scheme(63, '1.86 : 1'), 1)])], [OWN3])
add(3, 7, 'b-iii', calc + lift(S23, 9, '(iii) Acid test ratio'), 5, 'business-3-19', 'acid-test-ratio', 9, [63],
    'Award the five published one-mark points.',
    [response(1, 'Acid test ratio', [('formula', 'Formula: ' + scheme(63, 'Current Assets – Closing stock : Current liabilities'), 1),
                                     ('assets', 'Current assets: 174,375', 1), ('stock', 'Closing stock: ' + scheme(63, '90,000'), 1),
                                     ('liabilities', 'Current liabilities: 93,750', 1), ('answer', 'Answer: ' + scheme(63, '0.90 : 1'), 1)])],
    ['Scheme working: ' + scheme(63, '174,375 – 90,000 : 93,750') + ' = ' + scheme(63, '84,375 : 93,750') + '.', OWN3])
add(3, 7, 'b-iv', calc + lift(S23, 9, '(iv) Return on investment'), 7, 'business-3-19', 'return-on-investment', 9, [64],
    'Award 1 for the formula, 1 for net profit, 4 for capital employed (2 + 1 + 1) and 1 for the answer.',
    [response(1, 'Return on investment', [('formula', 'Formula: Net profit ÷ Capital Employed × 100', 1),
                                          ('profit', 'Net profit: ' + scheme(64, '33,750'), 1), ('loan', 'Long term loan: 250,000', 2),
                                          ('shares', 'Ordinary share capital: 350,000', 1), ('retained', 'Retained earnings: 75,000', 1),
                                          ('answer', 'Answer: ' + scheme(64, '5 %'), 1)])],
    ['Scheme: ' + scheme(64, 'Capital Employed [= Long term loan + Ordinary share capital + retained earnings.]')
     + ' ' + scheme(64, '250,000+350,000+75,000') + ' = ' + scheme(64, '675,000') + '.', OWN3])
add(3, 7, 'c', swift + '\n\n' + lift(S23, 9, 'Industry average results for 2025:', 'Net profit margin 7.5%', 'Current ratio 2.1 : 1',
                                     'Acid test ratio 1.2 : 1', 'Return on investment 8%')
    + '\n\n' + 'Swift Ltd’s 2025 results, from the marking scheme’s part (B) solutions: net profit margin ' + scheme(63, '7.5 %').replace(' %', '%')
    + '; current ratio ' + scheme(63, '1.86 : 1') + '; acid test ratio ' + scheme(63, '0.90 : 1') + '; return on investment ' + scheme(64, '5 %').replace(' %', '%') + '.'
    + '\n\n' + lift(S23, 9, 'Analyse the profitability and liquidity of Swift Ltd for 2025, with reference to the industry average results shown. Make recommendations for Swift Ltd.'),
    20, 'business-3-19', 'swift-profitability-liquidity-analysis', 9, [65],
    'Profitability 2 @ 5 marks (3 + 2) and liquidity 2 @ 5 marks (3 + 2): Compare, recommendation.',
    seq(points('Profitability', 2, (3, 2), ['Compare', 'Recommendation']),
        points('Liquidity', 2, (3, 2), ['Compare', 'Recommendation'])),
    ['Swift Ltd’s own results are supplied from the part (B) solutions so this analysis can be practised independently. The scheme compares each with its industry average and recommends an improvement.'])

adidas = lift(S23, 10, 'Inspired by their heritage, the Adidas brand is rooted in sports and the culture born from it. Adidas is a global leader in the sporting goods industry.')
add(3, 8, 'a', adidas + '\n\n' + lift(S23, 10, 'Illustrate, with reference to Adidas, the benefits of branding for the consumer.'), 20,
    'business-4-17', 'adidas-branding-consumer-benefits', 10, [66],
    'Illustrate three benefits using 7 (4 + 2 + 1), 7 (4 + 2 + 1) and 6 (3 + 2 + 1) marks, with reference to Adidas.',
    seq(comps('Benefit 1', (4, 2, 1)), comps('Benefit 2', (4, 2, 1)), comps('Benefit 3', (3, 2, 1))),
    ['The larger allowances are not fixed to particular benefits.'])
add(3, 8, 'b-i', lift(S23, 10, 'Explain the term Channel of Distribution.'), 6, 'business-4-17', 'channel-of-distribution',
    10, [67], 'Explain the term for 6 marks (3 + 3).', [comps('Channel of distribution', (3, 3))])
add(3, 8, 'b-ii', adidas + '\n\n' + lift(S23, 10, 'Evaluate the benefits and challenges for Adidas of choosing a direct channel of distribution rather than selling through wholesalers and retailers.'),
    14, 'business-4-17', 'adidas-direct-channel-evaluation', 10, [67],
    'Evaluate three points at 4 marks each (Name 2, Explain 2), covering benefits and challenges, plus 2 marks for evaluation.',
    seq(points('Point', 3, (2, 2), ['Name', 'Explain']), evaluation()),
    ['Scheme: “' + scheme(67, 'Evaluation required') + '” The question requires both benefits and challenges.'])
add(3, 8, 'c', lift(S23, 10, 'Discuss the short-term and the long-term implications of expansion for a business.'), 20, 'business-4-18',
    'expansion-short-and-long-term-implications', 10, [68, 69, 70],
    ['Discuss four implications at 5 marks each (2 + 3), covering both short-term and long-term implications.',
     'Scheme: “' + scheme(68, 'At least one of each required') + '”.'],
    points('Implication', 4, (2, 3)))

# ---------------------------------------------------------------- checks
s1 = [c for c in created if c['section'] == '1']
s3 = [c for c in created if c['section'] == '3']
assert len(s1) == 16 and sum(c['totalMarks'] for c in s1) == 120, (len(s1), sum(c['totalMarks'] for c in s1))
for q in range(1, 9):
    cohort = [c for c in s3 if c['questionRef'].split(' Q')[1].split('(')[0] == str(q)]
    assert sum(c['totalMarks'] for c in cohort) == 60, (q, [c['totalMarks'] for c in cohort])
assert len(s3) == 35, len(s3)

path = Path('components/MarkBank/cards/business/rubric-authored.json')
d = json.loads(path.read_text())
ids = {c['id'] for c in created}
assert not any(c['id'] in ids for c in d['cards'] if c['section'] == '2'), 'ABQ ids collide'
d['cards'] = [c for c in d['cards'] if c['id'] not in ids] + created
d['reviews'] = [r for r in d['reviews'] if not (r['year'] == year and r['section'] in ['1', '3'])]

SELECTION = {
    1: 'No finite printed answer menu occurs in Section 1. True/False labels and the slash-separated circled options are required answer formats for every row, not optional tasks. Matching rows are all required. The interest group in Q6(ii) and the support-note features, factors and implications are open examples. Each split part keeps its own printed prompt and, for Q10, the full figure table.',
    3: 'No finite printed choose-k pool occurs in Section 3. Named pairs (condition/warranty, constructive/unfair dismissal, organic/inorganic), bulleted stakeholders (business and competitor, government and business; customers and investors), benefits and challenges, and short-term and long-term implications are required headings, kept whole. The product in Q7(A) and the agree/disagree position in Q3(C) are open answers. Support-note lists are open examples of possible responses, not menus.',
}
for section, questions in [(1, range(1, 13)), (3, range(1, 9))]:
    for q in questions:
        cohort = [c for c in created if c['section'] == str(section) and c['questionRef'].split(' Q')[1].split('(')[0] == str(q)]
        d['reviews'].append(dict(
            status='partial-subject-review', year=year, level='higher', section=str(section), question=str(q),
            cardIds=[c['id'] for c in cohort], sources=sources(section), paperPagesReviewed=sorted({p for c in cohort for p in c['paperPages']}),
            schemePagesReviewed=sorted({p for c in cohort for p in c['rubric']['schemePages']}),
            boundaries={c['id'].split('-q', 1)[1]: c['totalMarks'] for c in cohort},
            selectionAnalysis=SELECTION[section],
            sourceClarifications=[g for c in cohort for g in c['rubric']['guidance']]))
d['cards'].sort(key=lambda c: (c['year'], c['section'], c['id']))
d['reviews'].sort(key=lambda r: (r['year'], r['section'], r['question']))
path.write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n')

# Topic Atlas: booklet-specific identities, p1 short questions, p2 long questions and ABQ.
path = Path('data/examTopics/business-source-reviewed-topics.json')
t = json.loads(path.read_text())
t['questions'] = [r for r in t['questions'] if r['year'] != year]
for section, questions in [(1, range(1, 13)), (3, range(1, 9))]:
    for q in questions:
        cohort = [c for c in created if c['section'] == str(section) and c['questionRef'].split(' Q')[1].split('(')[0] == str(q)]
        topics = list(dict.fromkeys(x for c in cohort for x in [c['topicId']] + c.get('additionalTopicIds', [])))
        t['questions'].append(dict(year=year, level='higher', paperKey='p1' if section == 1 else 'p2', n=str(q), canonicalNodeIds=topics,
            reason=f'Every part of {year} Higher Section {section} Question {q} was visually checked against its SEC booklet, allocation summary and support notes. Booklet-specific p1/p2 identities keep the short and long question numbering apart.'))
abq = [c for c in d['cards'] if c['year'] == year and c['level'] == 'higher' and c['section'] == '2']
t['questions'].append(dict(year=year, level='higher', paperKey='p2', n='ABQ', abqTopicLabel='ABQ (Units 3, 4 & 5)',
    canonicalNodeIds=list(dict.fromkeys(c['topicId'] for c in abq)),
    reason='The ABQ assesses employee rewards, pricing strategies, management control techniques and an alternative sales promotion technique. Case details about trade credit and the budget meeting are context, not separately assessed tasks.'))
t['questions'].sort(key=lambda r: (r['year'], r['paperKey'], str(r['n'])))
path.write_text(json.dumps(t, ensure_ascii=False, indent=2) + '\n')

# Raw selection directives: every match in both 2026 Higher English booklets.
path = Path('scripts/markbank/authored/business-selection-reviews.json')
sel = json.loads(path.read_text())
inv = json.loads(Path('scripts/markbank/authored/business-corpus-inventory.json').read_text())
counted = 0
for doc in inv['documents']:
    if not (doc['year'] == year and doc['level'] == 'higher' and doc['language'] == 'ev'):
        continue
    for item in doc['selectionDirectives']:
        w, page, m = item['wording'], item['page'], item['matchedText']
        if m.lower().startswith('answer'):
            cat, why = 'exam-navigation', 'The rubric sets how many whole questions a candidate answers. Every numbered question remains in the practice corpus as separate cards; no combined sitting card is created.'
        elif 'TRUE or FALSE' in w or 'True or False' in w:
            cat, why = 'required-headings', 'True/False are answer labels for each of the five required statements in Section 1 Q5, not optional tasks. All five stay in one exercise with the shared 3+2+2+2+1 tariff.'
        elif 'A person or business who sells insurance' in w and doc['paperFileid'] == S1 + '.pdf':
            cat, why = 'case-context', '“Person or business” is wording inside matching explanation A of Section 1 Q9. All five terms require a match; it creates no optional task.'
        elif 'donate to a food bank' in w:
            cat, why = 'case-context', 'The ABQ case says staff take near-expiry products home or donate them to a food bank. It is case evidence for the rewards task, not an instruction to choose an answer.'
        else:
            assert (doc['paperFileid'], page) in {(S1 + '.pdf', 2), (S1 + '.pdf', 9), (S1 + '.pdf', 40), (S23 + '.pdf', 12)}, item
            cat, why = 'exam-navigation', 'Pen/pencil instructions, answerbook supplies or copyright boilerplate. They do not create alternative task routes.'
        sel['reviews'][item['id']] = dict(wording=w, paperSha256=item['paperSha256'], classification=cat, reason=why)
        counted += 1
assert counted == 13, counted
path.write_text(json.dumps(sel, ensure_ascii=False, indent=2) + '\n')
print(f'Authored {len(created)} 2026 Higher tasks ({len(s1)} Section 1, {len(s3)} Section 3); reviewed {counted} raw selection matches.')
