"""Review the 2021 Higher English Section 1 and Section 3 tasks.

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

year = 2021
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

def evaluation(marks=2):
    return response(0, 'Evaluation', [('evaluate', 'Evaluation', marks)])

def unequal(label, splits, names):
    """Unequal published splits that the scheme does not tie to named items."""
    return seq([comps(f'{label} {i}', s, names) for i, s in enumerate(splits, 1)])

TARIFF = {1: 4, (3, 1): 6, (3, 2): 7, (3, 3): 8, (3, 4): 9, (3, 5): 10, (3, 6): 11, (3, 7): 12, (3, 8): 13}
created = []
REF_FIXES = set()
NEW_IDS = {'bus-2021-hl-s3-q6cii', 'bus-2021-hl-s3-q7b'}

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
        assert legacy['totalMarks'] == total, cid
        assert legacy['questionRef'] == c['questionRef'] or cid in REF_FIXES, (cid, legacy['questionRef'])
        if legacy['questionRef'] != c['questionRef']:
            fix = ((fix + '; ') if fix else '') + 'the reference is corrected from “' + legacy['questionRef'] + '”'
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
        assert cid in NEW_IDS, cid
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
    '', lift(S1, 3, 'Column 1: Terms', '1. Merger', '2. Economies of Scale', '3. Acquisition', '4. Diversification', '5. Strategic Alliance'),
    '', 'Column 2: Explanations\n' + lift(S1, 3, 'A This occurs when one company purchases more than 50% of the shares in another company.',
             'B Two businesses work together on a project but remain separate legal entities.',
             'C Purchasing a company and selling off its assets to increase return for investors.',
             'D Two or more businesses join together to create a new legal entity.',
             'E A business spreads risk by not being dependant on one market or one product.',
             'F The cost of producing each unit decreases due to an increase in production/bulk buying of raw materials.'),
    '', lift(S1, 3, 'Match the two lists by placing the letter of the correct explanation under the relevant number below.')]),
    'business-4-18', 'expansion-methods-matching', 3, [14],
    'Answer key: 1 D; 2 F; 3 A; 4 E; 5 B' + (' (scheme grid “1 2 3 4 5 D F A E B”).' if scheme(14, '1 2 3 4 5 D F A E B') else '') + ' Explanation C is unused.')
cumulative(2, lift(S1, 3, 'In the context of business, what do the following letters stand for? Write each answer in the space provided.', 'WTO', 'CAM', 'EDI', 'CAD', 'JIT'),
           'business-2-12', 'business-abbreviations', 3, [14],
           'Answer key: ' + '; '.join(scheme(14, s) for s in ['WTO World Trade Organisation', 'CAM Computer Aided Manufacturing', 'EDI Electronic Data Interchange',
                                                             'CAD Computer Aided Design', 'JIT Just in Time']) + '.',
           ['business-6-13', 'business-2-13'])
camile = lift(S1, 4, 'Camile Thai is a healthy, sustainable fast-casual restaurant franchise.')
add(1, 3, 'i', 'Q3(i)', camile + '\n\n' + lift(S1, 4, 'Explain the term franchising.'), 4, 'business-4-15', 'franchising', 4, [14],
    'Explain the term for 4 marks.', [comps('Franchising', (4,), ['Explanation'])])
add(1, 3, 'ii', 'Q3(ii)', camile + '\n\n' + lift(S1, 4, 'Outline one benefit of a franchise as a start-up option.'), 6, 'business-4-15',
    'franchise-start-up-benefit', 4, [14, 15], 'Outline one benefit for 6 marks (3 + 3).', [comps('Benefit', (3, 3))])
cumulative(4, lift(S1, 4, 'Circle the correct option in the case of each of the following statements.',
                   '(i) A larger policy excess will result in a higher / lower insurance premium.',
                   '(ii) The person who calculates the amount of compensation to be paid to a claimant is known as an Actuary / Assessor.',
                   '(iii) Indemnity / Utmost good faith means you cannot make a profit from an insurance claim.',
                   '(iv) Loadings on an insurance policy result in an increase / decrease in the premium.',
                   '(v) An insurance company who tries to reclaim any losses against a third party is using the principle of contribution / subrogation.'),
           'business-3-17', 'insurance-statements-options', 4, [15], 'Answer key (bold options on scheme page 15): (i) lower; (ii) Assessor; (iii) Indemnity; (iv) increase; (v) subrogation.')
c = add(1, 5, '', 'Q5', lift(S1, 5, 'Insert the correct state agency which corresponds with the explanations below.') + '\n'
    + lift(S1, 5, 'This state agency helps local entrepreneurs establish and grow a business.', 'This state agency helps existing indigenous firms to expand.',
           'This state agency supports the tourism industry and works to promote Ireland as a tourism destination.',
           'This state agency aims to attract foreign direct investment into Ireland.'),
    10, 'business-5-15', 'state-agencies', 5, [16], 'Each row has its own published mark: 3, 3, 2 and 2.',
    [response(1, 'State agencies', [('leo', 'Helps local entrepreneurs: ' + scheme(16, 'Local Enterprise Office (LEO)'), 3),
                                    ('ei', 'Helps indigenous firms expand: ' + scheme(16, 'Enterprise Ireland (EI)'), 3),
                                    ('tourism', 'Tourism: ' + scheme(16, 'Fáilte Ireland/ Tourism Ireland/ Bord Failte'), 2),
                                    ('ida', 'Foreign direct investment: ' + scheme(16, 'Industrial Development Authority/Agency (IDA)'), 2)])],
    extra=['business-5-16'])
for a in c['rubric']['responses'][0]['allocations']:
    a['permittedMarks'] = [0, a['maxMarks']]
add(1, 6, 'i', 'Q6(i)', lift(S1, 5, 'Explain the term invisible imports.'), 5, 'business-6-13', 'invisible-imports', 5, [16],
    'Explain the term for 5 marks (3 + 2).', [comps('Invisible imports', (3, 2))])
add(1, 6, 'ii', 'Q6(ii)', lift(S1, 5, 'Outline the impact of a decrease in invisible imports on the Balance of Payments.'), 5, 'business-6-13',
    'invisible-imports-decrease-impact', 5, [16], 'Outline the impact for 5 marks (3 + 2).', [comps('Impact', (3, 2))])
add(1, 7, '', 'Q7', lift(S1, 6, 'Distinguish between chain of command and span of control.'), 10, 'business-2-13', 'chain-of-command-versus-span-of-control',
    6, [17], 'Explain both required terms at 5 marks each (3 + 2).', [comps('Chain of command', (3, 2), i=1), comps('Span of control', (3, 2), i=2)])
stylish = lift(S1, 6, 'Stylish Tile & Bath Ltd provided the following financial information for 2020:') + '\n' + lift(
    S1, 6, 'Net Profit €72,000', 'Issued Ordinary Share Capital €450,000', 'Long Term Loan €100,000', 'Retained Earnings €26,000', 'Return on Investment 2019 = 7%')
add(1, 8, 'i', 'Q8(i)', stylish + '\n\n' + lift(S1, 6, '(i) Calculate the Return on Investment (ROI) for the owners of Stylish Tile & Bath Ltd for 2020. Show your formula and your workings.'),
    6, 'business-3-19', 'return-on-investment', 6, [17], 'Award the six published one-mark points (6@1m).',
    [response(1, 'Return on Investment', [('formula', 'Formula: Net Profit ÷ Capital employed × 100', 1), ('profit', 'Net profit: 72,000', 1),
                                          ('shares', 'Issued share capital: 450,000', 1), ('loan', 'Long term loan: 100,000', 1),
                                          ('retained', 'Retained earnings: 26,000', 1), ('answer', 'Answer: 12.5%', 1)])],
    ['Scheme working (read from the rendered page): 72,000 ÷ (450,000 + 100,000 + 26,000) × 100 = 72,000 ÷ 576,000 × 100 = 12.5%.'])
add(1, 8, 'ii', 'Q8(ii)', stylish + '\n\nStylish Tile & Bath Ltd’s Return on Investment for 2020, from the marking scheme: 12.5%.\n'
    + lift(S1, 6, '(ii) Analyse the significance of the change in the Return on Investment for Stylish Tile & Bath Ltd.'), 4, 'business-3-19',
    'roi-change-significance', 6, [17], 'Analyse the significance for 4 marks (2 + 2).', [comps('Significance', (2, 2))],
    fix='the 2020 result is supplied from the scheme so the analysis can be practised independently')
add(1, 9, 'i', 'Q9(i)', lift(S1, 7, 'Distinguish between enterprise and management.'), 6, 'business-1-5', 'enterprise-versus-management', 7, [18],
    'Explain both required terms at 3 marks each.', [comps('Enterprise', (3,), ['Explanation'], 1), comps('Management', (3,), ['Explanation'], 2)],
    extra=['business-2-13'])
add(1, 9, 'ii', 'Q9(ii)', lift(S1, 7, 'Suggest an example of enterprise in action in a school.'), 4, 'business-1-5', 'enterprise-in-school', 7, [18],
    'Suggest an example for 4 marks: 2 x 2 marks (1 + 1).', [comps('Example', (2, 2))],
    ['The scheme prints 2x2m (1+1) without naming the two components; its examples include a chess club, a soccer team and a green-school initiative.'])
add(1, 10, '', 'Q10', lift(S1, 7, 'Illustrate, using examples, the role of interest groups in business.'), 10, 'business-0-12', 'interest-groups-role',
    7, [18], 'Role 6 marks (3 + 3) and examples 4 marks (2 + 2).',
    [comps('Role of interest groups', (3, 3), i=1), comps('Examples', (2, 2), i=2)])
add(1, 11, '', 'Q11', lift(S1, 8, 'Many leading global pharmaceutical companies are located in Ireland.') + '\n\n'
    + lift(S1, 8, 'Outline two reasons why multinational companies locate in Ireland.'), 10, 'business-6-15', 'mncs-locate-in-ireland', 8, [19, 20],
    'Outline two reasons at 5 marks each (3 + 2).', points('Reason', 2, (3, 2)))
add(1, 12, '', 'Q12', lift(S1, 8, 'Outline two advantages in favour of privatisation for the Irish economy.'), 10, 'business-5-15', 'privatisation-advantages',
    8, [20], 'Outline two advantages at 5 marks each (3 + 2).', points('Advantage', 2, (3, 2)))

# ---------------------------------------------------------------- Section 3
house = lift(S23, 3, 'Louise and Cormac wanted to buy their first home. They visited the CCPC website for advice. They placed a bid on a house they liked, which was accepted. They signed their mortgage contract in their solicitor’s office and received the keys to their new property.')
add(3, 1, 'a', 'Q1(A)', house + '\n\n' + lift(S23, 3, 'Explain, using examples where appropriate, three essential elements of a valid contract.'), 20,
    'business-0-12', 'valid-contract-elements', 3, [27, 28], 'Explain three elements using 7 (2 + 3 + 2), 7 (2 + 3 + 2) and 6 (2 + 3 + 1) marks.',
    unequal('Element', [(2, 3, 2), (2, 3, 2), (2, 3, 1)], None),
    ['The allocation summary prints the third element as 6m (2+3+1); the support page prints (2+2+2). The card follows the summary. Scheme: “' + scheme(27, 'Example required for full marks') + '”.'])
add(3, 1, 'b', 'Q1(B)', house + '\n\n' + lift(S23, 3, 'Evaluate the role of the Competition and Consumer Protection Commission (CCPC).'), 20, 'business-0-13',
    'ccpc-role-evaluation', 3, [29], 'Evaluate three roles at 6 marks each (3 + 3), plus 2 marks for evaluation.',
    seq(points('Role', 3, (3, 3)), evaluation()), ['Scheme: “' + scheme(29, 'Evaluation required.') + '”'])
add(3, 1, 'c', 'Q1(C)', lift(S23, 3, 'Outline three types of redress available to employees who have been unfairly dismissed under the Unfair Dismissals Act 1977/2015.'),
    20, 'business-0-14', 'unfair-dismissal-redress', 3, [30], 'Outline three types using 7 (3 + 2 + 2), 7 (3 + 2 + 2) and 6 (2 + 2 + 2) marks.',
    unequal('Redress', [(3, 2, 2), (3, 2, 2), (2, 2, 2)], None),
    ['The scheme names reinstatement, re-engagement and compensation; the larger allowances are not tied to a particular type.'])

inflation = lift(S23, 4, 'Inflation hits 10 year low!')
add(3, 2, 'a', 'Q2(A)', inflation + '\n\n' + lift(S23, 4, 'Illustrate the impact of the following economic variables on Irish businesses:') + '\n'
    + lift(S23, 4, 'Interest rates Inflation rates Employment').replace(' Inflation', '\nInflation').replace(' Employment', '\nEmployment'), 20,
    'business-5-15', 'economic-variables-impact', 4, [31], 'All three named variables are required, using 7 (4 + 3), 7 (4 + 3) and 6 (3 + 3) marks.',
    unequal('Variable response', [(4, 3), (4, 3), (3, 3)], None), ['The larger allowances are not tied to a particular variable.'])
add(3, 2, 'b', 'Q2(B)', lift(S23, 4, 'Apart from taxation, discuss the different ways in which the Irish Government affects the labour force in Ireland.'), 20,
    'business-5-15', 'government-labour-force', 4, [32], 'Discuss three ways using 7 (4 + 3), 7 (4 + 3) and 6 (3 + 3) marks.',
    unequal('Way', [(4, 3), (4, 3), (3, 3)], None), ['Taxation is excluded by the question.'])
community = lift(S23, 4, 'Community development has never been more important.')
add(3, 2, 'ci', 'Q2(C)(i)', community + '\n\n' + lift(S23, 4, 'Explain the term ‘community development’.'), 6, 'business-5-16', 'community-development-term',
    4, [33], 'Explain the term for 6 marks (3 + 3).', [comps('Community development', (3, 3))])
add(3, 2, 'cii', 'Q2(C)(ii)', community + '\n\n' + lift(S23, 4, 'Describe the economic and social benefits of community development.'), 14, 'business-5-16',
    'community-development-benefits', 4, [33, 34], 'One economic and one social benefit are required at 7 marks each (4 + 3).',
    [comps('Economic benefit', (4, 3), i=1), comps('Social benefit', (4, 3), i=2)])

trade = lift(S23, 4, 'China and 14 Asia-Pacific countries agreed a historic free trade deal in November 2020. Trade barriers continue to impact trade between some countries.')
add(3, 3, 'a', 'Q3(A)', trade + '\n\n' + lift(S23, 4, 'Outline, using examples, the barriers to free trade used by some countries.'), 20, 'business-6-13',
    'free-trade-barriers', 4, [35], 'Outline three barriers using 7 (2 + 3 + 2), 7 (2 + 3 + 2) and 6 (2 + 2 + 2) marks.',
    unequal('Barrier', [(2, 3, 2), (2, 3, 2), (2, 2, 2)], None), ['The larger allowances are not tied to particular barriers.'])
add(3, 3, 'bi', 'Q3(B)(i)', lift(S23, 4, 'Explain the term globalisation.'), 5, 'business-6-15', 'globalisation', 4, [36],
    'Explain the term for 5 marks.', [comps('Globalisation', (5,), ['Explanation'])])
add(3, 3, 'bii', 'Q3(B)(ii)', lift(S23, 4, 'Analyse how changes in the international economy are impacting Irish businesses.'), 15, 'business-6-15',
    'international-economy-changes', 4, [36, 37, 38, 39], 'Analyse three changes at 5 marks each (2 + 3).', points('Change', 3, (2, 3)))

asti = lift(S23, 5, 'The ASTI conducted a ballot for industrial action in October 2020.')
add(3, 4, 'ai', 'Q4(A)(i)', asti + '\n\n' + lift(S23, 5, 'Outline two causes of industrial relations disputes.'), 10, 'business-0-14',
    'industrial-dispute-causes', 5, [42], 'Outline two causes at 5 marks each (2 + 3).', points('Cause', 2, (2, 3)))
add(3, 4, 'aii', 'Q4(A)(ii)', asti + '\n\n' + lift(S23, 5, 'Discuss two types of official industrial action available to employees involved in an industrial dispute with their employer.'),
    10, 'business-0-14', 'official-industrial-action', 5, [42, 43], 'Discuss two types at 5 marks each (2 + 3).', points('Type', 2, (2, 3)))
add(3, 4, 'b', 'Q4(B)', lift(S23, 5, 'Describe a co-operative relationship and a competitive relationship between two producers in the same line of business. Use appropriate examples to support your answer.'),
    20, 'business-0-12', 'producer-relationships', 5, [43], 'Both relationships are required at 10 marks each (4 + 3 + 3).',
    [comps('Co-operative relationship', (4, 3, 3), i=1), comps('Competitive relationship', (4, 3, 3), i=2)])
wilshere = lift(S23, 5, 'Premier League soccer player Jack Wilshere and his club West Ham Utd agree ‘mutual termination of midfielder’s contract’.')
add(3, 4, 'ci', 'Q4(C)(i)', wilshere + '\n\n' + lift(S23, 5, 'Explain the method of terminating a legal contract as referred to in the text above.'), 6,
    'business-0-12', 'termination-by-agreement', 5, [44], 'Explain the method for 6 marks (3 + 3).', [comps('Method', (3, 3))],
    ['The scheme’s answer is termination by agreement.'])
add(3, 4, 'cii', 'Q4(C)(ii)', wilshere + '\n\n' + lift(S23, 5, 'Outline other methods for terminating a legal contract. Provide an example in each case.'), 14,
    'business-0-12', 'other-termination-methods', 5, [44], 'Outline two other methods at 7 marks each (2 + 3 + 2), with an example for each.',
    points('Method', 2, (2, 3, 2), ['Method', 'Explain', 'Example']), ['Agreement, the method in the extract, is excluded.'])

farm = lift(S23, 6, 'Ballymakenny Farm Heritage & Speciality Potatoes Maria Flynn and her husband David are potato farmers. Maria saw a niche in the market to start growing their own speciality Purple Violetta Potatoes. Ballymakenny Farm now supply their speciality potatoes to leading chefs and restaurants.')
add(3, 5, 'a', 'Q5(A)', farm + '\n\n' + lift(S23, 6, 'Discuss the entrepreneurial skills and characteristics you would associate with entrepreneurs like Maria and David.'), 20,
    'business-1-5', 'entrepreneurial-skills', 6, [45], 'Discuss four skills or characteristics at 5 marks each (2 + 3).', points('Skill', 4, (2, 3)))
add(3, 5, 'b', 'Q5(B)', lift(S23, 6, 'Illustrate the factors that a business needs to consider when communicating with its various stakeholders.'), 20, 'business-2-12',
    'communication-factors', 6, [46], 'Illustrate four factors at 5 marks each (2 + 3).', points('Factor', 4, (2, 3)))
add(3, 5, 'ci', 'Q5(C)(i)', lift(S23, 6, 'Define the term delegation.'), 5, 'business-2-13', 'delegation', 6, [47],
    'Define the term for 5 marks (2 + 3).', [comps('Delegation', (2, 3))])
add(3, 5, 'cii', 'Q5(C)(ii)', lift(S23, 6, 'Describe the benefits of delegation for:') + '\n• management\n• the employees.', 15, 'business-2-13',
    'delegation-benefits', 6, [47], 'Describe three benefits at 5 marks each (2 + 3), covering management and the employees as the question names both.',
    points('Benefit', 3, (2, 3)))

kerry = lift(S23, 7, 'Kerry Group is a leading taste and nutrition company. Total Quality Management (TQM), reward schemes and teamwork are evident in many leading companies such as Kerry Group.')
add(3, 6, 'ai', 'Q6(A)(i)', kerry + '\n\n' + lift(S23, 7, 'Distinguish between forming and norming as stages in team development.'), 6, 'business-3-20',
    'forming-versus-norming', 7, [48], 'Explain both required stages at 3 marks each.', [comps('Forming', (3,), ['Explanation'], 1), comps('Norming', (3,), ['Explanation'], 2)],
    fix='teamwork is filed under human resource management')
add(3, 6, 'aii', 'Q6(A)(ii)', kerry + '\n\n' + lift(S23, 7, 'Outline two benefits of teamwork for the employees in a business.'), 14, 'business-3-20',
    'teamwork-benefits', 7, [48], 'Outline two benefits at 7 marks each (4 + 3).', points('Benefit', 2, (4, 3)),
    ['The support page header prints 10, but its 2 x 7m (4 + 3) and the allocation summary both give 14.'], fix='teamwork is filed under human resource management')
add(3, 6, 'b', 'Q6(B)', kerry + '\n\n' + lift(S23, 7, 'Discuss the benefits of adopting a Total Quality Management (TQM) system for a company such as Kerry Group.'), 15,
    'business-3-21', 'tqm-benefits', 7, [49], 'Discuss three benefits at 5 marks each (2 + 3).', points('Benefit', 3, (2, 3)))
rewards = lift(S23, 7, 'Businesses offer a range of rewards to attract high calibre staff.')
add(3, 6, 'ci', 'Q6(C)(i)', rewards + '\n\n' + lift(S23, 7, 'Explain the following types of financial and non-financial rewards.') + '\n'
    + lift(S23, 7, 'Commission Employee Share Purchase Plan Flexitime').replace(' Employee', '\nEmployee').replace(' Flexitime', '\nFlexitime'), 18,
    'business-3-20', 'reward-types', 7, [50], 'All three named rewards are required at 6 marks each (3 + 3).',
    [comps(name, (3, 3), None, i) for i, name in enumerate(['Commission', 'Employee Share Purchase Plan', 'Flexitime'], 1)])
add(3, 6, 'cii', 'Q6(C)(ii)', rewards + '\n\n' + lift(S23, 7, 'Describe one other type of reward that you believe motivates employees.'), 7, 'business-3-20',
    'other-motivating-reward', 7, [50], 'Describe one other reward for 7 marks (2 + 3 + 2).', [comps('Reward', (2, 3, 2))],
    ['Scheme: “' + scheme(50, 'Accept relevant reward') + '”. The three rewards in part (i) are excluded.'])

moon = lift(S23, 8, 'The entrepreneurs behind Moon Moods set up a business that produces soft, comfortable and beautiful bedding for children and babies.')
add(3, 7, 'a', 'Q7(A)', moon + '\n\n' + lift(S23, 8, 'Outline the internal and external sources of new product ideas for businesses.'), 20, 'business-4-14',
    'new-product-idea-sources', 8, [51], 'Outline four sources at 5 marks each (2 + 3), covering internal and external sources.',
    seq(points('Internal source', 2, (2, 3)), points('External source', 2, (2, 3))),
    ['The question requires both internal and external sources; the scheme prints 4@5(2+3) without fixing the split, so two of each is used.'])
chart_data = moon + '\n\n' + lift(S23, 8, 'Moon Moods has provided the following information for their new product line:') + '\n' + lift(
    S23, 8, 'Forecast Output (Sales) 30,000 units', 'Selling Price per unit €15', 'Fixed Costs €200,000', 'Variable Costs per unit €5')
chart_ask = lift(S23, 8, 'Illustrate the following by means of a breakeven chart:')
items = {'i': lift(S23, 8, '(i) Breakeven point'), 'ii': lift(S23, 8, '(ii) Margin of safety at the forecast output'), 'iii': lift(S23, 8, '(iii) Profit at forecast output.')}
CALC = ('Calculations only: break-even point 200,000 ÷ (15 − 5) = ' + scheme(53, '20,000 units') + '; margin of safety 30,000 − 20,000 = '
        + scheme(53, '10,000 units') + '; profit at forecast output €450,000 − €350,000 = ' + scheme(53, '€100,000') + '.')
add(3, 7, 'b', 'Q7(B)', chart_data + '\n\n' + chart_ask + '\n' + '\n'.join(items.values()), 25, 'business-3-19', 'breakeven-chart-complete', 8, [52, 53],
    ['Draw one labelled break-even chart: X axis 1, Y axis 1, title 1, FC line 2, TC and TR lines 4 each, and BEP, margin of safety and profit at forecast output 4 each.',
     'Calculations without a chart earn at most 12 (break-even point 4, profit 4, margin of safety 4).'],
    [response(1, 'Chart construction', [('x-axis', 'X axis: output in units', 1), ('y-axis', 'Y axis: revenue/costs €', 1), ('title', 'Title of chart', 1),
                                        ('fc', 'Fixed costs line', 2), ('tc', 'Total costs line', 4), ('tr', 'Total revenue line', 4)]),
     response(2, 'Indicators', [('bep', 'Break-even point', 4), ('mos', 'Margin of safety', 4), ('profit', 'Profit at forecast output', 4)])],
    [CALC, 'If there is no chart, leave every chart-construction allocation at zero. Do not award an indicator twice for illustrating and calculating it.'])
for suffix, key, label, calc in [('bi', 'i', 'Break-even point', '200,000 ÷ (15 − 5) = 20,000 units'),
                                 ('bii', 'ii', 'Margin of safety', '30,000 − 20,000 = 10,000 units'),
                                 ('biii', 'iii', 'Profit at forecast output', '€450,000 − €350,000 = €100,000')]:
    add(3, 7, suffix, f'Q7(B)({key})', chart_data + '\n\n' + chart_ask + '\n' + items[key], 4, 'business-3-19',
        f'breakeven-{label.lower().replace(" ", "-")}', 8, [52, 53],
        f'Show the {label.lower()} on a break-even chart or by calculation for 4 marks; the scheme accepts either route once. Practise the complete 25-mark chart on the Q7(B) card.',
        [response(1, label, [('indicator', label, 4)])], ['Calculation route: ' + calc + '.'],
        fix='the card is labelled as one published indicator of the single 25-mark chart')
add(3, 7, 'ci', 'Q7(C)(i)', lift(S23, 8, 'Define the term margin of safety.'), 5, 'business-3-19', 'margin-of-safety-term', 8, [54],
    'Define the term for 5 marks.', [comps('Margin of safety', (5,), ['Definition'])])
add(3, 7, 'cii', 'Q7(C)(ii)', lift(S23, 8, 'Discuss one limitation of a breakeven analysis when making business decisions.'), 10, 'business-3-19',
    'breakeven-limitation', 8, [54], 'Discuss one limitation for 10 marks (5 + 5).', [comps('Limitation', (5, 5))],
    ['The allocation summary prints 2@5m and the support page 2@10 (5+5); both total 10 for the one limitation.'])

aimee = lift(S23, 9, 'Aimee Connolly started working behind a makeup counter when she was a transition year student. While studying at university, Aimee decided to create her own makeup business and produce makeup products. ‘Sculpted by Aimee’ is now a very popular makeup brand. The products are sold nationally and internationally.')
add(3, 8, 'a', 'Q8(A)', aimee + '\n\n' + lift(S23, 9, 'Discuss the three challenges below that a new business start-up must address.') + '\n'
    + lift(S23, 9, 'Ownership structure Production Finance').replace(' Production', '\nProduction').replace(' Finance', '\nFinance'), 20, 'business-4-15',
    'start-up-challenges', 9, [55], 'All three named challenges are required, using 7 (2 + 3 + 2), 7 (2 + 3 + 2) and 6 (2 + 2 + 2) marks.',
    unequal('Challenge response', [(2, 3, 2), (2, 3, 2), (2, 2, 2)], None), ['The larger allowances are not tied to a particular challenge.'])
add(3, 8, 'b', 'Q8(B)', lift(S23, 9, 'Describe the first four stages involved in the development process of a new product.'), 20, 'business-4-14',
    'new-product-development-stages', 9, [56], 'Describe the first four stages at 5 marks each (2 + 3).',
    [comps(name, (2, 3), None, i) for i, name in enumerate(['Idea generation', 'Product screening', 'Concept development', 'Feasibility study'], 1)],
    ['The scheme’s first four stages are idea generation, product screening, concept development and feasibility study.'])
add(3, 8, 'ci', 'Q8(C)(i)', lift(S23, 9, 'Define the term market segmentation.'), 6, 'business-4-16', 'market-segmentation', 9, [57],
    'Define the term for 6 marks (3 + 3).', [comps('Market segmentation', (3, 3))])
add(3, 8, 'cii', 'Q8(C)(ii)', lift(S23, 9, 'Illustrate two different ways a market can be segmented.'), 14, 'business-4-16', 'segmentation-methods',
    9, [57, 58], 'Illustrate two ways at 7 marks each (2 + 3 + 2).', points('Way', 2, (2, 3, 2)))
# ---------------------------------------------------------------- finite pools
def legacy_route(cid, selected, page, schemes, note):
    legacy = original[cid]
    return dict(id=cid, selectedOptionIds=selected, correction=dict(
        originalQuestionText=legacy['questionText'], originalTotalMarks=legacy['totalMarks'],
        reason=f"Visually verified paper page {page} and scheme PDF pages {', '.join(map(str, schemes))}: {note} Retain the existing card ID and total marks for saved progress."))

def pool(pid, ref, page, schemes, choose, wording, prompt, options, total, requirement, guidance, topic, concept, selection, legacy, ordered=None):
    p = dict(id=pid, choose=choose, sourceWording=wording, routePrompt=prompt, options=options,
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

company_resp = dict(allocations=[dict(id=k, label=l, maxMarks=m, permittedMarks=list(range(m + 1))) for k, l, m in
                                 [('feature-1', 'Feature 1', 3), ('develop-1', 'Feature 1 developed', 3), ('feature-2', 'Feature 2', 3),
                                  ('develop-2', 'Feature 2 developed', 3), ('feature-3', 'Feature 3', 3), ('develop-3', 'Feature 3 developed', 3),
                                  ('evaluate', 'Evaluation', 2)]])
seven_seven_six = [response(1, 'Heading response 1', [('component-1', 'Component 1', 4), ('component-2', 'Component 2', 3)]),
                   response(2, 'Heading response 2', [('component-1', 'Component 1', 4), ('component-2', 'Component 2', 3)]),
                   response(3, 'Heading response 3', [('component-1', 'Component 1', 3), ('component-2', 'Component 2', 3)])]

policy_resp = dict(allocations=[dict(id=k, label=l, maxMarks=m, permittedMarks=list(range(m + 1))) for k, l, m in
                                [('point-1', 'Impact 1', 2), ('develop-1', 'Impact 1 developed', 2), ('point-2', 'Impact 2', 2),
                                 ('develop-2', 'Impact 2 developed', 2), ('evaluate', 'Evaluation', 2)]])
pools = [
    pool('bus-2021-hl-s3-q3c', '3(C)', 4, [8, 40, 41], 2,
         lift(S23, 4, 'Evaluate the impact on Ireland of any two of the following policies:'),
         trade + '\n\n' + 'Evaluate the impact on Ireland of the following two policies:',
         [opt('cap', lift(S23, 4, '(i) The Common Agricultural Policy'), policy_resp), opt('competition', lift(S23, 4, '(ii) The Competition Policy'), policy_resp),
          opt('social-charter', lift(S23, 4, '(iii) The European Union Social Charter.'), policy_resp)],
         20, 'Evaluate each selected policy for 10 marks: two impacts at 4 marks (2 + 2) and 2 marks for evaluation.',
         ['Scheme: “Evaluation required in each case”. Each policy carries its own 2-mark evaluation.'],
         'business-6-14', 'eu-policy-impact-evaluation',
         'The paper prints a closed list of three EU policies and asks for any two. All three unordered pairs are generated at 20 marks.',
         legacy_route('bus-2021-hl-s3-q3c', ['cap', 'competition'], 4, [8, 40, 41],
                      'the printed any-two-of-three choice is expanded into three routes; this ID becomes the Common Agricultural Policy and Competition Policy route, the first printed pair, with the published response allocation.')),
]
# ---------------------------------------------------------------- checks
s1 = [c for c in created if c['section'] == '1']
s3 = [c for c in created if c['section'] == '3']
assert sum(c['totalMarks'] for c in s1) == 120, sum(c['totalMarks'] for c in s1)
legacy_ids = {i for i, c in original.items() if c['year'] == year and c['level'] == 'higher' and c['section'] in ('1', '3')}
pool_legacy = {p['legacyRoute']['id'] for p in pools}
assert legacy_ids == ({c['id'] for c in created} - NEW_IDS) | pool_legacy, legacy_ids ^ ({c['id'] for c in created} | pool_legacy)
def qnum(c):
    return c['questionRef'].split(' Q')[1].split('(')[0].split(' ')[0]
pool_marks = {p['template']['questionRef'].split(' Q')[1].split('(')[0]: p['template']['totalMarks'] for p in pools}
COMPONENTS = {'bus-2021-hl-s3-q7bi', 'bus-2021-hl-s3-q7bii', 'bus-2021-hl-s3-q7biii'}
for q in range(1, 9):
    total = sum(c['totalMarks'] for c in s3 if qnum(c) == str(q) and c['id'] not in COMPONENTS) + pool_marks.get(str(q), 0)
    assert total == 60, (q, total)

path = Path('components/MarkBank/cards/business/rubric-authored.json')
d = json.loads(path.read_text())
ids = {c['id'] for c in created}
d['cards'] = [c for c in d['cards'] if c['id'] not in ids] + created
d['reviews'] = [r for r in d['reviews'] if not (r['year'] == year and r['section'] in ['1', '3'])]
SELECTION = {
    1: 'No finite printed answer menu occurs in Section 1. Slash-separated circled options and matching rows are required answer formats; the four state-agency rows are all required. Benefits, reasons and advantages in the support notes are open examples. Each split part keeps its printed prompt and data.',
    3: 'One finite printed pool is expanded separately: Q3(C) any two of three EU policies (three routes). The three named economic variables, rewards and start-up challenges, the first four product-development stages, both relationship types, and economic and social benefits are required and kept whole. Support-note lists elsewhere are open examples.',
}
for section, questions in [(1, range(1, 13)), (3, range(1, 9))]:
    for q in questions:
        cohort = [c for c in created if c['section'] == str(section) and qnum(c) == str(q)]
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
        cohort = [c for c in created if c['section'] == str(section) and qnum(c) == str(q)]
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
        if item['id'] in sel['reviews']:
            continue
        w, page, m = item['wording'], item['page'], item['matchedText']
        pid = None
        if m.lower().startswith('answer') or (m in ('either', 'or') and ('Part 1 or Part 2' in w or 'either Part 1' in w)):
            cat, why = 'exam-navigation', 'The rubric sets how many whole questions a candidate answers. Every numbered question remains in the practice corpus as separate cards; no combined sitting card is created.'
        elif m == 'any two':
            cat, why, pid = 'finite-pool', 'Section 3 Q3(C) asks for any two of three printed EU policies. All three pairs are generated at 20 marks; the legacy card ID is kept as the first printed pair.', 'bus-2021-hl-s3-q3c'
        elif 'Two or more businesses' in w or 'one market or one product' in w:
            cat, why = 'case-context', 'The wording is inside a matching explanation in Section 1 Q1; all five terms require a match and no optional task is created.'
        else:
            assert (doc['paperFileid'], page) in {(S1 + '.pdf', 2), (S1 + '.pdf', 9), (S1 + '.pdf', 36), (S23 + '.pdf', 1), (S23 + '.pdf', 12)}, item
            cat, why = 'exam-navigation', 'Cover instructions, pen/pencil instructions, answerbook supplies or copyright boilerplate. They do not create alternative task routes.'
        r = dict(wording=w, paperSha256=item['paperSha256'], classification=cat, reason=why)
        if pid:
            r['poolId'] = pid
        sel['reviews'][item['id']] = r
        counted += 1
path.write_text(json.dumps(sel, ensure_ascii=False, indent=2) + '\n')
print(f'Reviewed {len(created)} 2021 Higher base tasks ({len(s1)} Section 1, {len(s3)} Section 3; {sum("correction" in c for c in created)} corrected legacy IDs) and {len(pools)} route pools; classified {counted} raw selection matches.')
