"""Review the 2024 Higher English Section 1 and Section 3 tasks.

All 52 existing card IDs keep their ID and total. Each moves to the reviewed
rubric renderer with a correction record that pins its original wording and
tariff. Question strings are slices of the normalised SEC paper text; quoted
scheme strings are asserted present in the cited scheme page. One new card
adds the complete 25-mark break-even chart beside the legacy component cards.
Run from the repo root; reproduce.py runs it in the chain.
"""
from abq_authoring import response, notes
from pathlib import Path
import hashlib, json, re, unicodedata, fitz

year = 2024
S1, S23, MS = 'LC033ALP032EV', 'LC033ALP041EV', 'LC033ALP000EV'
docs = {S1: fitz.open(f'paper-trail-corpus/exampapers/{year}/{S1}.pdf'),
        S23: fitz.open(f'paper-trail-corpus/exampapers/{year}/{S23}.pdf'),
        MS: fitz.open(f'paper-trail-corpus/markingschemes/{year}/{MS}.pdf')}
original = {c['id']: c for c in json.load(open('scripts/markbank/authored/business.json'))}

def norm(s):
    s = unicodedata.normalize('NFKC', s)
    for a, b in {'Ɵ': 'ti', 'Ʃ': 'tt', 'Ō': 'ft', '‐': '-', '\xa0': ' ', ' ': ' ', '': ' '}.items():
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

def unequal(label, splits, names):
    """Unequal published splits that the scheme does not tie to named items."""
    return seq([comps(f'{label} {i}', s, names) for i, s in enumerate(splits, 1)])

TARIFF = {1: 4, (3, 1): 6, (3, 2): 7, (3, 3): 8, (3, 4): 9, (3, 5): 10, (3, 6): 11, (3, 7): 12, (3, 8): 13}
created = []

def add(section, q, suffix, ref, prompt, total, topic, concept, page, support, requirement, responses,
        guidance=None, extra=None, marknote=None, fix=None):
    cid = f'bus-{year}-hl-s{section}-q{q}{suffix}'
    tariff = TARIFF[1] if section == 1 else TARIFF[(3, q)]
    c = dict(id=cid, year=year, level='higher', section=str(section),
             paperFileid=S1 if section == 1 else S23, paperPages=[page], sourceLabel='QUESTION PAPER',
             sourceTitle=f'{year} Business · Section {section} Question {q}',
             questionRef=f'{year} HL Section {section} {ref}', questionText=prompt, totalMarks=total,
             topicId=topic, conceptId=concept,
             rubric=dict(system='business', taskRequirements=requirement if isinstance(requirement, list) else [requirement],
                         guidance=guidance or [], responses=responses, schemeFileid=MS,
                         schemePages=[tariff] + support, markingGuideNote=marknote or notes))
    if extra:
        c['additionalTopicIds'] = extra
    marks = sum(a['maxMarks'] for r in responses for a in r['allocations'])
    assert marks == total, (cid, marks, total)
    assert len({r['id'] for r in responses}) == len(responses), cid
    legacy = original.get(cid)
    if legacy:
        assert legacy['totalMarks'] == total and legacy['questionRef'] == c['questionRef'], (cid, legacy['questionRef'])
        ticks = legacy['tariffModel'].get('kind') == 'bestNofParts' or any(
            r.get('kind') == 'anyN' or r.get('openList') for r in legacy['rows'])
        changes = ['question text lifted from the printed paper',
                   'the published response allocations replace the fixed example ticks' if ticks
                   else 'the published marks become rubric allocations, with the official answers kept in the scheme notes']
        if legacy['topicId'] != topic:
            changes.append(f"canonical topic corrected from {legacy['topicId']} to {topic}")
        if fix:
            changes.append(fix)
        c['correction'] = dict(originalQuestionText=legacy['questionText'], originalTotalMarks=legacy['totalMarks'],
            reason=f"Visually verified paper page {page} and scheme PDF pages {', '.join(map(str, c['rubric']['schemePages']))}: "
                   + '; '.join(changes) + '. Retain the existing card ID and total marks.')
    else:
        assert cid == 'bus-2024-hl-s1-q9i', cid
    created.append(c)
    return c

CUMULATIVE = 'For 0, 1, 2, 3, 4 or 5 correct answers, record 0, 3, 5, 7, 9 or 10 marks. The larger allowances are not tied to particular printed rows.'

def cumulative(q, prompt, topic, concept, page, support, key, extra=None, fix=None):
    c = add(1, q, '', f'Q{q}', prompt, 10, topic, concept, page, support,
            'Complete all five answers. The published cumulative sequence is 3 + 2 + 2 + 2 + 1.',
            [comps('Correct answers', (10,), ['Total from the published sequence'])], [key, CUMULATIVE], extra,
            marknote='Use the official answer key and the published cumulative sequence. Each correct answer counts once.', fix=fix)
    c['rubric']['responses'][0]['allocations'][0]['permittedMarks'] = [0, 3, 5, 7, 9, 10]
    return c


# ---------------------------------------------------------------- Section 1
cumulative(1, '\n'.join([
    lift(S1, 3, 'Column 1 is a list of business terms. Column 2 is a list of possible explanations for these terms. (One explanation does not refer to any of these terms.)'),
    '', lift(S1, 3, 'Column 1: Terms', '1. Partnership', '2. Co-operative', '3. Franchise', '4. Merger', '5. Takeover'),
    '', lift(S1, 3, 'Column 2: Explanations', 'A Two businesses join together to form a new legal entity.',
             'B A business with a minimum of 2 and a maximum of 20 owners.',
             'C A business owned, financed and controlled by the government.',
             'D A business set up, owned and controlled by its members for their mutual benefit.',
             'E A business taking control of another business by purchasing the majority of its voting shares.',
             'F The right to use a business model in exchange for a fee and a percentage of profits.'),
    '', lift(S1, 3, 'Match the two lists by placing the letter of the correct explanation under the relevant number below.')]),
    'business-5-14', 'ownership-and-expansion-matching', 3, [14],
    'Answer key (printed as a grid on scheme page 14): 1 B; 2 D; 3 F; 4 A; 5 E. Explanation C is unused.', ['business-4-18'])
cumulative(2, lift(S1, 3, 'In the context of business, what do the following letters stand for? Write each answer in the space provided.',
                   'IDA', 'CEO', 'ECB', 'CRO', 'WTO'),
           'business-5-15', 'business-abbreviations', 3, [14],
           'Answer key: IDA: ' + scheme(14, 'Industrial Development Agency') + '; CEO: ' + scheme(14, 'Chief Executive Officer')
           + '; ECB: ' + scheme(14, 'European Central Bank') + '; CRO: ' + scheme(14, 'Companies Registration Office')
           + '; WTO: ' + scheme(14, 'World Trade Organisation') + '.',
           ['business-2-13', 'business-6-14', 'business-5-14', 'business-6-13'])
add(1, 3, 'i', 'Q3(i)', lift(S1, 4, 'Explain the term Community Development.'), 4, 'business-5-16', 'community-development-term', 4, [15],
    'Explain the term for 4 marks (2 + 2).', [comps('Community development', (2, 2))])
add(1, 3, 'ii', 'Q3(ii)', lift(S1, 4, 'Outline one service offered by a community development organisation of your choice.'), 6, 'business-5-16',
    'community-development-service', 4, [15], 'Outline one service for 6 marks (3 + 3).', [comps('Service', (3, 3))],
    ['The organisation is an open choice. Scheme: “' + scheme(15, 'Accept relevant points on; Training workshops, Mentoring, Premises etc.') + '”'])
cumulative(4, lift(S1, 4, 'Circle the correct option in the case of each of the following statements.',
                   '(i) The difference between the target output in units and the breakeven point in units is referred to as the total revenue/margin of safety.',
                   '(ii) A breakeven chart does/does not consider economies of scale.',
                   '(iii) In a breakeven chart the fixed costs/total costs remain the same irrespective of an increase in the output of units.',
                   '(iv) The total revenue in a breakeven chart is calculated by multiplying the forecast output in units by the variable cost per unit/ selling price per unit.',
                   '(v) A product makes a profit/loss before it reaches the breakeven point on a breakeven chart.'),
           'business-3-19', 'breakeven-statements-options', 4, [16],
           'Answer key (bold options on scheme page 16): (i) margin of safety; (ii) does not; (iii) fixed costs; (iv) selling price per unit; (v) loss.',
           fix='break-even analysis is filed under monitoring the business, as on the other reviewed break-even cards')
add(1, 5, '', 'Q5', lift(S1, 4, 'Outline two functions of the European Parliament.'), 10, 'business-6-14', 'european-parliament-functions',
    4, [17], 'Outline two functions at 5 marks each (3 + 2).', points('Function', 2, (3, 2)))
add(1, 6, '', 'Q6', lift(S1, 5, 'Distinguish between an Embargo and a Quota.'), 10, 'business-6-13', 'embargo-versus-quota', 5, [18],
    'Explain both required terms at 5 marks each (3 + 2).', [comps('Embargo', (3, 2), i=1), comps('Quota', (3, 2), i=2)])
cumulative(7, lift(S1, 5, 'Write True or False after each of the following statements.',
                   '1. An example of a tactical plan is pharmaceutical firm Johnson and Johnson switching to source 100% of their electricity needs from renewable sources within the next 18 months.',
                   '2. Netflix offering 52 weeks of paid parental leave to staff is an example of a business meeting their social responsibilities to their suppliers.',
                   '3. State broadcaster RTE announcing targets to be achieved over the next five years is an example of a contingency plan.',
                   '4. By 2025, DHL aims to have more than 500 gas powered vehicles in its fleet. This is an example of a mission statement.',
                   '5. Nintendo planning for a new product launch in the next four weeks is an example of an operational plan.'),
           'business-2-13', 'planning-true-false', 5, [19],
           'Answer key (scheme page 19): 1 True; 2 False; 3 False; 4 False; 5 True.', ['business-5-17'])
add(1, 8, '', 'Q8', lift(S1, 6, 'Distinguish between two types of management control commonly used in a business.'), 10, 'business-2-13',
    'management-control-types', 6, [19], 'Explain two control types at 5 marks each (3 + 2).', points('Control type', 2, (3, 2)),
    ['The two types are an open choice; quality, credit, stock and financial control in the support notes are examples.'])
oliver = lift(S1, 6, 'Oliver Kiely owned a house worth €300,000. He insured this house for €250,000. A burst pipe in his attic caused damage of €60,000 to the house.')
add(1, 9, 'i', 'Q9(i)', oliver + '\n\n' + lift(S1, 6, 'Calculate the amount of compensation the insurance company will pay Oliver. Show your workings.'),
    6, 'business-3-17', 'average-clause-compensation', 6, [20], 'Award the six published calculation marks.',
    [response(1, 'Compensation', [('insured', 'Sum insured: 250,000', 1), ('value', 'Market value: 300,000', 1), ('loss', 'Loss: 60,000', 2),
                                  ('answer', 'Compensation: €50,000', 2)])],
    ['Scheme working: 250,000 ÷ 300,000 × 60,000 = €50,000.',
     'The scheme prints two one-mark ticks around the €50,000 result without naming them separately; they are kept together on the answer.'])
add(1, 9, 'ii', 'Q9(ii)', lift(S1, 6, 'Explain the role of the assessor in insurance.'), 4, 'business-3-17', 'insurance-assessor-role', 6, [20],
    'Explain the role for 4 marks (2 + 2).', [comps('Assessor', (2, 2))])
add(1, 10, '', 'Q10', lift(S1, 7, 'List three public relations methods commonly used by businesses. Provide an example for each method.'), 10,
    'business-4-17', 'public-relations-methods', 7, [21], 'List three methods with an example for each: 4 (2 + 2), 3 (2 + 1) and 3 (2 + 1).',
    unequal('Method and example', [(2, 2), (2, 1), (2, 1)], ['Method', 'Example']),
    ['The larger allowance is not tied to a particular method. The scheme also accepts “' + scheme(21, 'Other relevant methods with appropriate examples') + '”.'])
add(1, 11, '', 'Q11', lift(S1, 7, 'Illustrate your understanding of a Joint Labour Committee.'), 10, 'business-0-14', 'joint-labour-committee',
    7, [22], 'Illustrate the term for 10 marks (4 + 3 + 3).', [comps('Joint Labour Committee', (4, 3, 3))])
add(1, 12, 'i', 'Q12(i)', lift(S1, 7, 'Explain the term teamwork.'), 4, 'business-3-20', 'teamwork-term', 7, [22],
    'Explain the term for 4 marks (2 + 2).', [comps('Teamwork', (2, 2))], fix='teamwork is filed under human resource management')
c = add(1, 12, 'ii', 'Q12(ii)', lift(S1, 7, 'Name the four stages of team development.'), 6, 'business-3-20', 'team-development-stages', 7, [22],
    'Name all four stages. The published sequence is 2 + 2 + 1 + 1.',
    [comps('Stages named', (6,), ['Total from the published sequence'])],
    ['Answer key: ' + scheme(22, 'Forming Storming Norming Performing').replace(' ', '; ') + '.', 'For 0, 1, 2, 3 or 4 correct stages, record 0, 2, 4, 5 or 6 marks.'],
    fix='teamwork is filed under human resource management')
c['rubric']['responses'][0]['allocations'][0]['permittedMarks'] = [0, 2, 4, 5, 6]

# ---------------------------------------------------------------- Section 3
EXAMPLE = 'Scheme: example required for each.'
construction = lift(S23, 3, 'Construction developer seeks €3.4m from contractor for breach of contract. Construction developer claims a contractor left 65- unit social housing scheme in Dublin incomplete and overclaimed payments.')
add(3, 1, 'ai', 'Q1(A)(i)', construction + '\n\n' + lift(S23, 3, 'Explain the term breach of contract.'), 6, 'business-0-12', 'breach-of-contract',
    3, [31], 'Explain the term for 6 marks (4 + 2).', [comps('Breach of contract', (4, 2))])
add(3, 1, 'aii', 'Q1(A)(ii)', construction + '\n\n' + lift(S23, 3, 'Illustrate the remedies available for a breach of contract.'), 14, 'business-0-12',
    'breach-of-contract-remedies', 3, [31], 'Illustrate two remedies at 7 marks each (2 + 2 + 3).', points('Remedy', 2, (2, 2, 3)),
    ['Scheme: “' + scheme(31, 'Example Required') + '” for each remedy.'])
add(3, 1, 'bi', 'Q1(B)(i)', lift(S23, 3, 'Describe three features of the Small Claims Procedure for resolving conflict.'), 15, 'business-0-13',
    'small-claims-features', 3, [32], 'Describe three features at 5 marks each (2 + 3).', points('Feature', 3, (2, 3)))
add(3, 1, 'bii', 'Q1(B)(ii)', lift(S23, 3, 'Recommend one way you think the Small Claims Procedure could be improved. Provide a reason to support your answer.'),
    5, 'business-0-13', 'small-claims-improvement', 3, [32], 'Recommend one improvement with a reason for 5 marks (2 + 3).',
    [comps('Improvement and reason', (2, 3), ['Recommendation', 'Reason'])])
add(3, 1, 'ci', 'Q1(C)(i)', lift(S23, 3, 'List three grounds, under which a dismissal can be deemed unfair according to the Unfair Dismissals Act 1977/2015.'),
    6, 'business-0-14', 'unfair-dismissal-grounds', 3, [33], 'List three grounds at 2 marks each.',
    [comps(f'Ground {i}', (2,), ['Ground listed'], i) for i in range(1, 4)])
add(3, 1, 'cii', 'Q1(C)(ii)', lift(S23, 3, 'Outline three procedures an employer should follow when dismissing an employee, under the Unfair Dismissals Act 1977/2015.'),
    14, 'business-0-14', 'dismissal-procedures', 3, [33, 34], 'Outline three procedures: 5 (2 + 3), 5 (2 + 3) and 4 (2 + 2).',
    unequal('Procedure', [(2, 3), (2, 3), (2, 2)], None), ['The larger allowances are not tied to particular procedures.'])

recession = lift(S23, 4, 'The Irish economy is officially in technical recession as GDP shrinks more than expected in third quarter.')
add(3, 2, 'ai', 'Q2(A)(i)', recession + '\n\n' + lift(S23, 4, 'Distinguish between economic growth and interest rates.'), 10, 'business-5-15',
    'economic-growth-versus-interest-rates', 4, [35], 'Explain both required terms at 5 marks each (2 + 3).',
    [comps('Economic growth', (2, 3), i=1), comps('Interest rates', (2, 3), i=2)])
add(3, 2, 'aii', 'Q2(A)(ii)', recession + '\n\n' + lift(S23, 4, 'Outline the impacts of an increase in interest rates on Irish businesses.'), 10,
    'business-5-15', 'interest-rate-increase-impacts', 4, [35], 'Outline two impacts at 5 marks each (2 + 3).', points('Impact', 2, (2, 3)))
add(3, 2, 'bi', 'Q2(B)(i)', lift(S23, 4, 'Illustrate your understanding of the term the primary sector.'), 5, 'business-5-13', 'primary-sector-term',
    4, [36], 'Illustrate the term for 5 marks (2 + 3).', [comps('Primary sector', (2, 3))])
add(3, 2, 'bii', 'Q2(B)(ii)', lift(S23, 4, 'Discuss the current trends in the primary sector of the economy.'), 15, 'business-5-13', 'primary-sector-trends',
    4, [36], 'Discuss three trends at 5 marks each (2 + 3).', points('Trend', 3, (2, 3)))
records = lift(S23, 4, 'Some businesses manipulate their financial records to boost investment.')
add(3, 2, 'ci', 'Q2(C)(i)', records + '\n\n' + lift(S23, 4, 'Explain the term business ethics.'), 5, 'business-5-17', 'business-ethics-term',
    4, [37], 'Explain the term for 5 marks (2 + 3).', [comps('Business ethics', (2, 3))])
add(3, 2, 'cii', 'Q2(C)(ii)', records + '\n\n' + lift(S23, 4, 'Outline how a business may encourage their employees to be ethical.'), 15,
    'business-5-17', 'encouraging-ethical-employees', 4, [37], 'Outline three ways at 5 marks each (2 + 3).', points('Way', 3, (2, 3)))

FIGURES = ['72bn', '34bn', '93bn', '84bn']
for f in FIGURES:
    scheme(38, f)
infographic = (lift(S23, 5, 'Ireland 2023 Q3') + '\nGoods: Exports €72bn; Imports €34bn\nServices: Exports €93bn; Imports €84bn')
add(3, 3, 'ai', 'Q3(A)(i)', lift(S23, 5, 'Explain the term Balance of Payments.'), 6, 'business-6-13', 'balance-of-payments-term', 5, [38],
    'Explain the term for 6 marks (3 + 3).', [comps('Balance of Payments', (3, 3))])
add(3, 3, 'aii', 'Q3(A)(ii)', infographic + '\n\n' + lift(S23, 5, 'Calculate the Balance of Trade and the Balance of Payments using the data above. State whether your answer is a surplus or a deficit. Show your workings.'),
    14, 'business-6-13', 'balance-of-trade-and-payments', 5, [38],
    'Balance of Trade 6 and Balance of Payments 8: formula 1, each correct figure 1, € sign 1 and surplus/deficit 1.',
    [response(1, 'Balance of Trade', [('formula', 'Formula: ' + scheme(38, 'Visible Exports – Visible Imports'), 1), ('exports', 'Visible exports: €72bn', 1),
                                      ('imports', 'Visible imports: €34bn', 1), ('answer', 'Answer: €38bn', 1), ('euro', '€ sign', 1), ('surplus', 'Surplus', 1)]),
     response(2, 'Balance of Payments', [('formula', 'Formula: ' + scheme(38, 'Total Exports – Total Imports'), 1), ('goods-exports', 'Goods exports: €72bn', 1),
                                         ('services-exports', 'Services exports: €93bn', 1), ('goods-imports', 'Goods imports: €34bn', 1),
                                         ('services-imports', 'Services imports: €84bn', 1), ('answer', 'Answer: €47bn', 1), ('euro', '€ sign', 1), ('surplus', 'Surplus', 1)])],
    ['The figures are read from the printed CSO infographic. Scheme working: ' + scheme(38, '(72bn+93bn) - (34bn+84bn) = €47bn surplus') + ', or €165bn − €118bn; own figures allowed.'],
    fix='the infographic figures are supplied in the question')
add(3, 3, 'b', 'Q3(B)', lift(S23, 5, 'Apart from taxation, discuss the reasons why multinational companies locate in Ireland.'), 20, 'business-6-15',
    'mncs-locate-in-ireland', 5, [39], 'Discuss four reasons at 5 marks each (2 + 3).', points('Reason', 4, (2, 3)),
    ['Taxation is excluded by the question.'])
add(3, 3, 'ci', 'Q3(C)(i)', lift(S23, 5, 'Distinguish between the terms the standardised marketing mix and the adapted marketing mix.'), 10,
    'business-6-15', 'standardised-versus-adapted-mix', 5, [40], 'Explain both required terms at 5 marks each (2 + 3).',
    [comps('Standardised marketing mix', (2, 3), i=1), comps('Adapted marketing mix', (2, 3), i=2)])

firefighters = lift(S23, 6, 'Firefighters to escalate industrial action.')
add(3, 4, 'ai', 'Q4(A)(i)', firefighters + '\n\n' + lift(S23, 6, 'Define the term trade dispute as set out under the Industrial Relations Act 1990.'), 8,
    'business-0-14', 'trade-dispute-definition', 6, [43], 'Define the term for 8 marks (2 + 3 + 3).', [comps('Trade dispute', (2, 3, 3))])
add(3, 4, 'aii', 'Q4(A)(ii)', firefighters + '\n\n' + lift(S23, 6, 'Describe three types of official industrial action.'), 12, 'business-0-14',
    'official-industrial-action-types', 6, [43], 'Describe three types at 4 marks each (2 + 2).', points('Type', 3, (2, 2)))
add(3, 4, 'bi', 'Q4(B)(i)', lift(S23, 6, 'Illustrate the difference between lobbying and negotiation.'), 10, 'business-0-12', 'lobbying-versus-negotiation',
    6, [44], 'Explain both required terms at 5 marks each (3 + 2).', [comps('Lobbying', (3, 2), i=1), comps('Negotiation', (3, 2), i=2)],
    extra=['business-0-14'])
add(3, 4, 'bii', 'Q4(B)(ii)', lift(S23, 6, 'Outline two benefits of trade unions to an employee.'), 10, 'business-0-14', 'trade-union-benefits',
    6, [44], 'Outline two benefits at 5 marks each (3 + 2).', points('Benefit', 2, (3, 2)))
add(3, 4, 'c', 'Q4(C)', lift(S23, 6, 'Evaluate the role of the Competition and Consumer Protection Commission (CCPC).'), 20, 'business-0-13',
    'ccpc-role-evaluation', 6, [45], 'Evaluate four roles at 4 marks each (2 + 2), plus two evaluation allowances of 2 marks.',
    seq(points('Role', 4, (2, 2)), response(0, 'Evaluation', [('evaluation-1', 'Evaluation 1', 2), ('evaluation-2', 'Evaluation 2', 2)])),
    ['Scheme marks: ' + scheme(45, '4@4m(2+2) EV 2, Ev 2') + '.'])

ikea = lift(S23, 7, 'Ingvar Kamprad founded IKEA in 1943 at the age of 17, selling goods like pens and wallets. IKEA is now a market leader in affordable furniture.')
ikea2 = lift(S23, 7, 'IKEA has over 450 stores and operates in five continents. When expanding a business, management will often develop an organisational structure to clarify the span of control and chain of command.')
add(3, 5, 'a', 'Q5(A)', ikea + '\n\n' + lift(S23, 7, 'Explain reasons why an individual may become an entrepreneur.'), 15, 'business-1-5',
    'reasons-to-become-entrepreneur', 7, [46], 'Explain three reasons at 5 marks each (2 + 3).', points('Reason', 3, (2, 3)))
add(3, 5, 'bi', 'Q5(B)(i)', ikea2 + '\n\n' + lift(S23, 7, 'Distinguish between the terms span of control and chain of command.'), 10, 'business-2-13',
    'span-of-control-versus-chain-of-command', 7, [47], 'Explain both required terms at 5 marks each (2 + 3).',
    [comps('Span of control', (2, 3), i=1), comps('Chain of command', (2, 3), i=2)])
add(3, 5, 'bii', 'Q5(B)(ii)', ikea2 + '\n\n' + lift(S23, 7, 'Discuss the benefits of a matrix organisation structure for a business such as IKEA.'), 15,
    'business-2-13', 'matrix-structure-benefits-ikea', 7, [47], 'Discuss three benefits at 5 marks each (2 + 2 + 1).', points('Benefit', 3, (2, 2, 1)),
    ['Scheme: “' + scheme(47, 'Example Required') + '” for each benefit.'])
add(3, 5, 'c', 'Q5(C)', ikea + '\n\n' + lift(S23, 7, 'Outline, using an example, the impact of technology for management in a business such as IKEA in relation to;')
    + '\n' + lift(S23, 7, '(i) Design of products', '(ii) Manufacturing', '(iii) Marketing', '(iv) Human Resource Management.'),
    20, 'business-3-21', 'technology-impact-on-management', 7, [48], 'All four named areas are required at 5 marks each (2 + 2 + 1), with an example.',
    [comps(name, (2, 2, 1), None, i) for i, name in enumerate(['Design of products', 'Manufacturing', 'Marketing', 'Human Resource Management'], 1)],
    ['Scheme: “' + scheme(48, 'Example Required') + '” for each area.'])

cash = lift(S23, 8, 'The cash flow forecast for Jackson Ltd for Q4 in 2024 is set out below.') + '\n' + lift(
    S23, 8, '2024 Oct € Nov € Dec € Total €', 'Receipts 151,000 125,000 114,000 390,000', 'Payments 130,000 B 125,000 423,000',
    'Net Cash 21,000 (43,000) C (33,000)', 'Opening Cash A 26,000 (17,000) 5,000', 'Closing Cash 26,000 (17,000) (28,000) (28,000)')
add(3, 6, 'ai', 'Q6(A)(i)', cash + '\n\n' + lift(S23, 8, 'Explain the reasons Jackson Ltd would prepare a cashflow forecast.'), 10, 'business-3-16',
    'cashflow-forecast-reasons', 8, [49], 'Explain two reasons at 5 marks each (2 + 3).', points('Reason', 2, (2, 3)))
c = add(3, 6, 'aii', 'Q6(A)(ii)', cash + '\n\n' + lift(S23, 8, 'Calculate the figures represented by the letters A, B and C on the cashflow forecast. (Show answers in the answer book.)'),
    7, 'business-3-16', 'cashflow-missing-figures', 8, [50], 'Calculate all three figures. The published sequence is 3 + 2 + 2.',
    [comps('Figures calculated', (7,), ['Total from the published sequence'])],
    ['Answer key: A ' + scheme(50, '€5,000') + '; B ' + scheme(50, '€168,000') + '; C ' + scheme(50, '(€11,000) or -€11,000') + '.',
     'For 0, 1, 2 or 3 correct figures, record 0, 3, 5 or 7 marks.'])
c['rubric']['responses'][0]['allocations'][0]['permittedMarks'] = [0, 3, 5, 7]
add(3, 6, 'aiii', 'Q6(A)(iii)', cash + '\n\n' + lift(S23, 8, 'Outline two ways Jackson Ltd might deal with a problem identified in the above cashflow forecast.'),
    8, 'business-3-16', 'cashflow-problem-solutions', 8, [50], 'Outline two ways at 4 marks each (2 + 2).', points('Way', 2, (2, 2)))
add(3, 6, 'b', 'Q6(B)', lift(S23, 8, 'Discuss the differences in managing a household and managing a business in relation to taxation.'), 15,
    'business-3-18', 'household-versus-business-taxation', 8, [51], 'Discuss three differences at 5 marks each (2 + 3).', points('Difference', 3, (2, 3)))
premiums = lift(S23, 8, 'Insurance premiums in Ireland continue to rise.')
add(3, 6, 'ci', 'Q6(C)(i)', premiums + '\n\n' + lift(S23, 8, 'Explain, using examples, the following three principles of insurance;') + '\n'
    + lift(S23, 8, 'Utmost Good Faith', 'Indemnity', 'Insurable Interest'), 15, 'business-3-17', 'insurance-principles', 8, [52],
    'All three named principles are required at 5 marks each (2 + 3), with an example.',
    [comps(name, (2, 3), ['Explain', 'Example'], i) for i, name in enumerate(['Utmost Good Faith', 'Indemnity', 'Insurable Interest'], 1)],
    ['Scheme: “' + scheme(52, 'Example required') + '” for each principle.'])
add(3, 6, 'cii', 'Q6(C)(ii)', premiums + '\n\n' + lift(S23, 8, 'Identify one type of insurance policy and explain why the insurance company might deem the risk uninsurable.'),
    5, 'business-3-17', 'uninsurable-risk', 8, [52], 'Identify the policy and explain the uninsurable risk for 5 marks (2 + 3).',
    [comps('Policy and reason', (2, 3), ['Policy identified', 'Reason explained'])])

arq = lift(S23, 9, '4TH ARQ is an Irish clothing brand that produce unisex everyday streetwear. 4TH ARQ offer a range of clothing including tops, bottoms, jackets and fleeces. Their popular half-zip fleeces are available in a range of colours.')
add(3, 7, 'ai', 'Q7(A)(i)', lift(S23, 9, 'Explain the term batch production.'), 5, 'business-4-15', 'batch-production', 9, [53],
    'Explain the term for 5 marks (2 + 3).', [comps('Batch production', (2, 3))])
add(3, 7, 'aii', 'Q7(A)(ii)', arq + '\n\n' + lift(S23, 9, 'Discuss the implications for 4th ARQ of changing from batch production to mass production process.'),
    15, 'business-4-15', 'batch-to-mass-production-implications', 9, [53], 'Discuss three implications at 5 marks each (2 + 2 + 1).',
    points('Implication', 3, (2, 2, 1)))
add(3, 7, 'b', 'Q7(B)', lift(S23, 9, 'Contrast a Sole Trader and a Private Limited Company as forms of business ownership, using the following headings:') + '\n'
    + lift(S23, 9, 'Formation', 'Liability', 'Finance', 'Control'), 20, 'business-5-14', 'sole-trader-versus-private-company', 9, [54],
    'All four headings are required at 5 marks each (2 + 3), contrasting both forms of ownership.',
    [comps(name, (2, 3), None, i) for i, name in enumerate(['Formation', 'Liability', 'Finance', 'Control'], 1)])
companies = lift(S23, 9, 'The Companies Act 2014 requires directors of all companies to present a profit and loss account and a balance sheet annually.')
add(3, 7, 'cii', 'Q7(C)(ii)', companies + '\n\n' + lift(S23, 9, 'Outline one financial ratio used to measure the profitability of a business.'), 5,
    'business-3-19', 'profitability-ratio', 9, [55], 'Outline one profitability ratio for 5 marks (2 + 3).', [comps('Profitability ratio', (2, 3))])

premium = lift(S23, 10, 'Rolex watches, Adare Manor Hotel and Golf Resort and Prime Hydration Drinks are examples of businesses who use premium pricing.')
asai = lift(S23, 10, 'The ASAI published fresh guidance for Irish influencers on the clear labelling of ads on social media. For the avoidance of confusion, all commercial content should now be labelled #Ad (or #Fógra for Irish-language posts).')
add(3, 8, 'ai', 'Q8(A)(i)', premium + '\n\n' + lift(S23, 10, 'Explain the term premium pricing.'), 5, 'business-4-17', 'premium-pricing', 10, [56],
    'Explain the term for 5 marks (2 + 3).', [comps('Premium pricing', (2, 3))])
add(3, 8, 'aii', 'Q8(A)(ii)', premium + '\n\n' + lift(S23, 10, 'Outline the factors businesses may consider before deciding on a price for their product or service. Provide examples to support your answer.'),
    15, 'business-4-17', 'pricing-factors', 10, [56], 'Outline three factors at 5 marks each (2 + 2 + 1), with examples.', points('Factor', 3, (2, 2, 1)))
add(3, 8, 'bi', 'Q8(B)(i)', asai + '\n\n' + lift(S23, 10, 'What do the letters ASAI stand for?'), 4, 'business-4-17', 'asai-abbreviation', 10, [57],
    'Give the full name for 4 marks.', [comps('ASAI', (4,), ['Full name'])],
    ['Answer: ' + scheme(57, 'Advertising Standards Authority of Ireland') + '.'], extra=['business-0-13'])
add(3, 8, 'bii', 'Q8(B)(ii)', asai + '\n\n' + lift(S23, 10, 'Distinguish between generic advertising and persuasive advertising.'), 10, 'business-4-17',
    'generic-versus-persuasive-advertising', 10, [57], 'Explain both required terms at 5 marks each (2 + 3).',
    [comps('Generic advertising', (2, 3), i=1), comps('Persuasive advertising', (2, 3), i=2)])
add(3, 8, 'c', 'Q8(C)', lift(S23, 10, 'Describe different sales promotions techniques that a business could use to promote a new or existing product. Use examples to support your answer.'),
    15, 'business-4-17', 'sales-promotion-techniques', 10, [58], 'Describe three techniques at 5 marks each (2 + 2 + 1), with examples.',
    points('Technique', 3, (2, 2, 1)))

# ---------------------------------------------------------------- finite pools
def legacy_route(cid, selected, page, schemes, note):
    legacy = original[cid]
    return dict(id=cid, selectedOptionIds=selected, correction=dict(
        originalQuestionText=legacy['questionText'], originalTotalMarks=legacy['totalMarks'],
        reason=f"Visually verified paper page {page} and scheme PDF pages {', '.join(map(str, schemes))}: {note} Retain the existing card ID and total marks for saved progress."))

def pool(pid, ref, page, schemes, choose, wording, prompt, options, total, requirement, guidance, topic, concept, selection, legacy, ordered=None, extra_context=''):
    p = dict(id=pid, choose=choose, sourceWording=wording, routePrompt=(extra_context + '\n\n' if extra_context else '') + prompt, options=options,
             review=dict(status='partial-subject-review', year=year, level='higher', section='3', question=ref, sources=sources(3),
                         paperPagesReviewed=[page], schemePagesReviewed=schemes, boundaries={ref: total}, selectionAnalysis=selection,
                         sourceClarifications=guidance),
             template=dict(year=year, level='higher', section='3', paperFileid=S23, paperPages=[page], sourceLabel='QUESTION PAPER',
                           sourceTitle=f'{year} Business · Section 3 Question {ref.split("(")[0]}', questionRef=f'{year} HL Section 3 Q{ref}',
                           totalMarks=total, conceptId=concept,
                           rubric=dict(system='business', taskRequirements=[requirement], guidance=guidance, schemeFileid=MS,
                                       schemePages=schemes, markingGuideNote=notes)),
             legacyRoute=legacy)
    if ordered:
        p['orderedResponses'] = ordered
    for o in options:
        o.setdefault('topicId', topic)
    return p

def opt(i, label, resp=None):
    o = dict(id=i, label=label)
    if resp:
        o['response'] = resp
    return o

policy_resp = dict(allocations=[dict(id=k, label=l, maxMarks=m, permittedMarks=list(range(m + 1))) for k, l, m in
                                [('point-1', 'Importance 1', 2), ('explain-1', 'Importance 1 explained', 3),
                                 ('point-2', 'Importance 2', 2), ('explain-2', 'Importance 2 explained', 3)]])
term_resp = dict(allocations=[dict(id=k, label=l, maxMarks=m, permittedMarks=list(range(m + 1))) for k, l, m in
                              [('explain', 'Explain', 2), ('develop', 'Develop', 3)]])
pools = [
    pool('bus-2024-hl-s3-q3cii', '3(C)(ii)', 5, [8, 41, 42], 1,
         lift(S23, 5, 'Explain the importance for Ireland of any one of the following policies of the European Union.', sep=' '),
         'Explain the importance for Ireland of the following policy of the European Union:',
         [opt('cap', lift(S23, 5, 'Common Agricultural Policy'), policy_resp), opt('social', lift(S23, 5, 'EU Social Policy'), policy_resp),
          opt('competition', lift(S23, 5, 'EU Competition Policy'), policy_resp)],
         10, 'Explain two points of importance for Ireland at 5 marks each (2 + 3).',
         ['The scheme develops the Common Agricultural Policy, the EU Social Charter and the Competition Policy; each route keeps the same 2@5m(2+3) allocation.'],
         'business-6-14', 'eu-policy-importance',
         'The paper prints a closed list of three EU policies and asks for any one. Generate all three single-policy routes, each with the full 10-mark allocation.',
         legacy_route('bus-2024-hl-s3-q3cii', ['cap'], 5, [8, 41, 42],
                      'the printed any-one-of-three choice is expanded into three routes; this ID becomes the Common Agricultural Policy route, the first printed option, with the published response allocation.')),
    pool('bus-2024-hl-s3-q7ci', '7(C)(i)', 9, [12, 55], 3,
         lift(S23, 9, 'Explain any three of the following financial business terms.', sep=' '),
         'Explain the following three financial business terms.',
         [opt('liquidity', lift(S23, 9, 'Liquidity'), term_resp), opt('profit-and-loss', lift(S23, 9, 'Profit and Loss Account'), term_resp),
          opt('debtors', lift(S23, 9, 'Debtors'), term_resp), opt('dividends', lift(S23, 9, 'Dividends'), term_resp)],
         15, 'Explain each of the three terms at 5 marks each (2 + 3).', [],
         'business-3-19', 'financial-business-terms',
         'The paper prints a closed list of four terms and asks for any three. Generate all four unordered three-term routes, each with the full 15-mark allocation.',
         legacy_route('bus-2024-hl-s3-q7ci', ['liquidity', 'profit-and-loss', 'debtors'], 9, [12, 55],
                      'the printed any-three-of-four choice is expanded into four routes; this ID becomes the Liquidity, Profit and Loss Account and Debtors route, the first printed combination, with the published response allocation.'),
         extra_context=companies),
    pool('bus-2024-hl-s3-q8biii', '8(B)(iii)', 10, [13, 57], 2,
         lift(S23, 10, 'Outline an advertising medium you would recommend for two of the businesses listed below. Provide a reason to support each recommendation.', sep=' '),
         'Outline an advertising medium you would recommend for the following two businesses. Provide a reason to support each recommendation.',
         [opt('rolex', lift(S23, 10, 'Rolex watches')), opt('adare-manor', lift(S23, 10, 'Adare Manor Hotel and Golf Resort')),
          opt('prime', lift(S23, 10, 'Prime Hydration drinks'))],
         11, 'Recommend a medium with a reason for each business: 6 (3 + 3) and 5 (3 + 2).',
         ['The larger allowance is not tied to a particular business. Apply 6 (3 + 3) to one recommendation and 5 (3 + 2) to the other.'],
         'business-4-17', 'advertising-medium-recommendation',
         'The paper prints a closed list of three businesses and asks for two. Generate all three unordered pairs, each with the 11-mark allocation; the unequal 6/5 split is not tied to a business.',
         legacy_route('bus-2024-hl-s3-q8biii', ['rolex', 'adare-manor'], 10, [13, 57],
                      'the printed two-of-three choice is expanded into three routes; this ID becomes the Rolex watches and Adare Manor Hotel and Golf Resort route, the first printed pair, with the published 6/5 response allocation.'),
         ordered=[response(1, 'Recommendation 1', [('medium', 'Medium', 3), ('reason', 'Reason', 3)]),
                  response(2, 'Recommendation 2', [('medium', 'Medium', 3), ('reason', 'Reason', 2)])],
         extra_context=asai),
]

# ---------------------------------------------------------------- checks
s1 = [c for c in created if c['section'] == '1']
s3 = [c for c in created if c['section'] == '3']
assert len(s1) == 15 and sum(c['totalMarks'] for c in s1) == 120, (len(s1), sum(c['totalMarks'] for c in s1))
legacy_ids = {i for i, c in original.items() if c['year'] == year and c['level'] == 'higher' and c['section'] in ('1', '3')}
pool_legacy = {p['legacyRoute']['id'] for p in pools}
assert legacy_ids == ({c['id'] for c in created} - {'bus-2024-hl-s1-q9i'}) | pool_legacy, legacy_ids ^ ({c['id'] for c in created} | pool_legacy)
pool_marks = {p['template']['questionRef'].split(' Q')[1].split('(')[0]: p['template']['totalMarks'] for p in pools}
for q in range(1, 9):
    base = [c for c in s3 if c['questionRef'].split(' Q')[1].split('(')[0] == str(q)]
    total = sum(c['totalMarks'] for c in base) + pool_marks.get(str(q), 0)
    assert total == 60, (q, total)

path = Path('components/MarkBank/cards/business/rubric-authored.json')
d = json.loads(path.read_text())
ids = {c['id'] for c in created}
assert not (ids & pool_legacy)
d['cards'] = [c for c in d['cards'] if c['id'] not in ids] + created
d['reviews'] = [r for r in d['reviews'] if not (r['year'] == year and r['section'] in ['1', '3'])]
SELECTION = {
    1: 'No finite printed answer menu occurs in Section 1. True/False labels and slash-separated circled options are required answer formats for every row; matching rows are all required. The community development organisation, control types and PR methods are open examples. Each split part keeps its printed prompt and, for Q9, the house, sum insured and damage figures.',
    3: 'Three finite printed pools are expanded separately: Q3(C)(ii) any one of three EU policies, Q7(C)(i) any three of four financial terms, Q8(B)(iii) two of three businesses. Named pairs, the four IKEA technology areas, the three insurance principles and the four sole trader/private company headings are required and kept whole. Support-note lists elsewhere are open examples.',
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

path = Path('components/MarkBank/cards/business/route-pools.json')
rp = json.loads(path.read_text())
rp['pools'] = [p for p in rp['pools'] if p['id'] not in {x['id'] for x in pools}] + pools
path.write_text(json.dumps(rp, ensure_ascii=False, indent=2) + '\n')

path = Path('data/examTopics/business-source-reviewed-topics.json')
t = json.loads(path.read_text())
t['questions'] = [r for r in t['questions'] if not (r['year'] == year and r['n'] != 'ABQ')]
for section, questions in [(1, range(1, 13)), (3, range(1, 9))]:
    for q in questions:
        cohort = [c for c in created if c['section'] == str(section) and c['questionRef'].split(' Q')[1].split('(')[0] == str(q)]
        topics = list(dict.fromkeys(x for c in cohort for x in [c['topicId']] + c.get('additionalTopicIds', [])))
        for p in pools:
            if section == 3 and p['template']['questionRef'].split(' Q')[1].split('(')[0] == str(q):
                topics += [o['topicId'] for o in p['options'] if o['topicId'] not in topics]
        t['questions'].append(dict(year=year, level='higher', paperKey='p1' if section == 1 else 'p2', n=str(q), canonicalNodeIds=list(dict.fromkeys(topics)),
            reason=f'Every part of {year} Higher Section {section} Question {q} was visually checked against its SEC booklet, allocation summary and support notes. Booklet-specific p1/p2 identities keep the short and long question numbering apart.'))
t['questions'].sort(key=lambda r: (r['year'], r['paperKey'], str(r['n'])))
path.write_text(json.dumps(t, ensure_ascii=False, indent=2) + '\n')

path = Path('scripts/markbank/authored/business-selection-reviews.json')
sel = json.loads(path.read_text())
inv = json.loads(Path('scripts/markbank/authored/business-corpus-inventory.json').read_text())
counted = 0
for doc in inv['documents']:
    if not (doc['year'] == year and doc['level'] == 'higher' and doc['language'] == 'ev'):
        continue
    for item in doc['selectionDirectives']:
        if item['reviewStatus'] == 'reviewed' and item['id'] in sel['reviews']:
            continue
        w, page, m = item['wording'], item['page'], item['matchedText']
        pid = None
        if m.lower().startswith('answer') or (m in ('either', 'or') and ('Part 1 or Part 2' in w or 'either Part 1' in w)):
            cat, why = 'exam-navigation', 'The rubric sets how many whole questions a candidate answers. Every numbered question remains in the practice corpus as separate cards; no combined sitting card is created.'
        elif m == 'any one':
            cat, why, pid = 'finite-pool', 'Section 3 Q3(C)(ii) asks for any one of three printed EU policies. All three single-policy routes are generated at 10 marks; the legacy card ID is kept as the first route.', 'bus-2024-hl-s3-q3cii'
        elif m == 'any three':
            cat, why, pid = 'finite-pool', 'Section 3 Q7(C)(i) asks for any three of four printed financial terms. All four three-term routes are generated at 15 marks; the legacy card ID is kept as the first route.', 'bus-2024-hl-s3-q7ci'
        elif m == 'two of':
            cat, why, pid = 'finite-pool', 'Section 3 Q8(B)(iii) asks for two of three printed businesses. All three pairs are generated at 11 marks with the unequal 6/5 split kept off named businesses; the legacy card ID is kept as the first route.', 'bus-2024-hl-s3-q8biii'
        elif m == 'following three':
            cat, why = 'required-headings', 'Section 3 Q6(C)(i) names three principles of insurance and requires all three. They stay in one 15-mark task.'
        elif 'True or False' in w:
            cat, why = 'required-headings', 'True/False are answer labels for each of the five required statements in Section 1 Q7, not optional tasks. All five stay in one exercise with the shared 3+2+2+2+1 tariff.'
        elif 'surplus or a deficit' in w:
            cat, why = 'required-headings', 'Section 3 Q3(A)(ii) requires the candidate to state whether each balance is a surplus or a deficit. It is a required determination with its own mark, not a choice of task.'
        elif 'product or service' in w:
            cat, why = 'open-response', 'Product or service is open wording in Section 3 Q8(A)(ii); the pricing factors remain one task.'
        elif 'new or existing product' in w:
            cat, why = 'open-response', 'A new or existing product is open wording in Section 3 Q8(C); the sales promotion techniques remain one task.'
        elif '#Fógra' in w:
            cat, why = 'case-context', 'The ASAI extract notes the Irish-language label for ads. It is case context, not an instruction to choose an answer.'
        else:
            assert (doc['paperFileid'], page) in {(S1 + '.pdf', 2), (S1 + '.pdf', 8), (S1 + '.pdf', 40), (S23 + '.pdf', 12)}, item
            cat, why = 'exam-navigation', 'Pen/pencil instructions, answerbook supplies or copyright boilerplate. They do not create alternative task routes.'
        r = dict(wording=w, paperSha256=item['paperSha256'], classification=cat, reason=why)
        if pid:
            r['poolId'] = pid
        sel['reviews'][item['id']] = r
        counted += 1
path.write_text(json.dumps(sel, ensure_ascii=False, indent=2) + '\n')
print(f'Reviewed {len(created)} 2024 Higher base tasks ({len(s1)} Section 1, {len(s3)} Section 3; {sum("correction" in c for c in created)} corrected legacy IDs) and {len(pools)} route pools; classified {counted} raw selection matches.')
