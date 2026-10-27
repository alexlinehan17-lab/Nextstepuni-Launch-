"""Review the 2025 Higher English Section 1 and Section 3 tasks.

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

year = 2025
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

TARIFF = {1: 5, (3, 1): 7, (3, 2): 8, (3, 3): 8, (3, 4): 9, (3, 5): 9, (3, 6): 10, (3, 7): 10, (3, 8): 11}
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
        assert cid == 'bus-2025-hl-s3-q8c', cid
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
    lift(S1, 3, 'Column 1 is a list of business terms. Column 2 is a list of possible explanations for these terms. (One explanation does not refer to any of the terms.)'),
    '', lift(S1, 3, 'Column 1: Terms', '1 European Central Bank', '2 European Court of Auditors', '3 European Parliament',
             '4 Council of the European Union', '5 European Commission'),
    '', lift(S1, 3, 'Column 2: Explanations', 'A Directly elected by citizens of all member states of the European Union.',
             'B Decides on disputes between member states, EU institutions, businesses and individuals.',
             'C Key decision-making body in the EU, meetings attended by relevant ministers of each state.',
             'D Manages the euro currency and the EU’s monetary policy.',
             'E Audits the spending of the EU budget and reports on EU finances.',
             'F Responsible for the day to day management of the EU and proposes new EU Laws.'),
    '', lift(S1, 3, 'Match the two lists by placing the letter of the correct explanation under the relevant number below.')]),
    'business-6-14', 'eu-institutions-matching', 3, [12],
    'Answer key (printed as an image grid on scheme page 12): 1 D; 2 E; 3 A; 4 C; 5 F. Explanation B is unused.')
add(1, 2, 'a', 'Q2(a)', lift(S1, 3, 'Explain the term Global Business.'), 6, 'business-6-15', 'global-business-term', 3, [12],
    'Explain the term for 6 marks (3 + 3).', [comps('Global business', (3, 3))])
add(1, 2, 'b', 'Q2(b)', lift(S1, 3, 'Name two examples of Global Businesses.'), 4, 'business-6-15', 'global-business-examples', 3, [12],
    'Name two examples at 2 marks each.', [comps('Example 1', (2,), ['Global business named'], 1), comps('Example 2', (2,), ['Global business named'], 2)],
    ['Scheme: “' + scheme(12, 'Examples of global businesses include Coca Cola, Dell, Nike, Toyota, Microsoft, Intel, HP, Google, Apple, McDonalds and Nokia.') + '” These are open examples.'])
cumulative(3, lift(S1, 4, 'In the context of business, what do the following letters stand for? Write your answers in the spaces provided.',
                   'DAC', 'MNC', 'IBEC', 'ICTU', 'CAP'),
           'business-0-14', 'business-abbreviations', 4, [12],
           'Answer key: ' + '; '.join(scheme(12, s) for s in ['DAC = Designated Activity Company', 'MNC = Multinational Company',
               'IBEC = Irish Business Employers Confederation', 'ICTU = Irish Congress of Trade Unions', 'CAP = Common Agricultural Policy']) + '.',
           ['business-5-14', 'business-6-15', 'business-6-14'])
cumulative(4, lift(S1, 4, 'Circle the correct option in the case of each of the following statements.',
                   '(i) The term economic growth does/does not refer to the growth of one business over a period of time.',
                   '(ii) The rate of employment/unemployment is the percentage of the labour force that do not currently have work.',
                   '(iii) An increase in interest rates will result in higher/lower loan repayments.',
                   '(iv) Taxation is a compulsory/voluntary payment made by households and businesses to the government.',
                   '(v) When the euro (€) increases in value against British pound sterling (£), imported goods from the United Kingdom (UK) become more/less expensive in Ireland.'),
           'business-5-15', 'economy-statements-options', 4, [13],
           'Answer key: (i) Does not; (ii) Unemployment; (iii) Higher; (iv) Compulsory; (v) Less.' if scheme(13, 'Does not Unemployment Higher Compulsory Less') else '')
add(1, 5, '', 'Q5', lift(S1, 4, 'Distinguish between Capital Gains Tax and Capital Acquisitions Tax.'), 10, 'business-3-18',
    'cgt-versus-cat', 4, [13], 'Explain both required taxes at 5 marks each (3 + 2).',
    [comps('Capital Gains Tax', (3, 2), i=1), comps('Capital Acquisitions Tax', (3, 2), i=2)])
add(1, 6, '', 'Q6', lift(S1, 5, 'Outline two methods a business may use to encourage ethical business practice.'), 10, 'business-5-17',
    'encouraging-ethical-practice', 5, [14], 'Outline two methods at 5 marks each (3 + 2).', points('Method', 2, (3, 2)))
gearing = lift(S1, 5, 'Gearing is an indicator of the financial risk associated with a company.')
add(1, 7, 'a', 'Q7(a)', gearing + '\n\n' + lift(S1, 5, 'Explain the term Gearing.'), 5, 'business-3-19', 'gearing-term', 5, [14],
    'Explain the term for 5 marks (3 + 2).', [comps('Gearing', (3, 2))])
add(1, 7, 'b', 'Q7(b)', gearing + '\n\n' + lift(S1, 5, 'The following are the figures relating to Korn Ltd for 2024.', 'Authorised Share Capital €900,000',
    'Issued Share Capital €550,000', 'Long Term Loan €300,000', 'Reserves/Retained Earnings €50,000') + '\n\n'
    + lift(S1, 5, 'Calculate the Debt/Equity Ratio. Show your workings.'), 5, 'business-3-19', 'debt-equity-ratio', 5, [14],
    'Award the five published one-mark points (5@1m).',
    [response(1, 'Debt/Equity ratio', [('formula', 'Formula: ' + scheme(14, 'Debt ÷ Equity'), 1), ('debt', 'Long term loan: 300,000', 1),
                                       ('shares', 'Issued share capital: 550,000', 1), ('reserves', 'Reserves/retained earnings: 50,000', 1),
                                       ('answer', 'Answer: 0.5 : 1', 1)])],
    ['Scheme working: 300,000 ÷ (550,000 + 50,000) = 0.5 : 1. Authorised share capital is not part of equity.'])
add(1, 8, '', 'Q8', lift(S1, 6, 'Outline two benefits for a business of developing a matrix organisation structure (team structure) to complete specific projects in a business.'),
    10, 'business-2-13', 'matrix-structure-benefits', 6, [15], 'Outline two benefits at 5 marks each (3 + 2).', points('Benefit', 2, (3, 2)))
add(1, 9, 'i', 'Q9(i)', lift(S1, 6, 'Explain, using an example, the term import substitution.'), 5, 'business-6-13', 'import-substitution',
    6, [16], 'Explain the term with an example for 5 marks (3 + 2).', [comps('Import substitution', (3, 2))])
add(1, 9, 'ii', 'Q9(ii)', lift(S1, 6, 'Outline the impact an increase in import substitution would have on the Balance of Payments.'), 5,
    'business-6-13', 'import-substitution-balance-of-payments', 6, [16], 'Outline the impact for 5 marks (3 + 2).', [comps('Impact', (3, 2))])
add(1, 10, '', 'Q10', lift(S1, 6, 'Describe two factors a business will consider when choosing an appropriate advertising medium.'), 10,
    'business-4-17', 'advertising-medium-factors', 6, [16], 'Describe two factors at 5 marks each (3 + 2).', points('Factor', 2, (3, 2)))
add(1, 11, 'a', 'Q11(a)', lift(S1, 7, 'Explain the term inflation.'), 6, 'business-5-15', 'inflation-term', 7, [17],
    'Explain the term for 6 marks (3 + 3).', [comps('Inflation', (3, 3))])
add(1, 11, 'b', 'Q11(b)', lift(S1, 7, 'List two causes of inflation.'), 4, 'business-5-15', 'inflation-causes', 7, [17],
    'List two causes at 2 marks each.', [comps('Cause 1', (2,), ['Cause listed'], 1), comps('Cause 2', (2,), ['Cause listed'], 2)])
add(1, 12, '', 'Q12', lift(S1, 7, 'Outline two functions of a Local Enterprise Office (LEO) in supporting small businesses in Ireland.'), 10,
    'business-5-16', 'leo-functions', 7, [17], 'Outline two functions at 5 marks each (3 + 2).', points('Function', 2, (3, 2)),
    ['The scheme develops Mentoring and Grants, then adds “' + scheme(17, 'Other answers may include:') + '” further functions; these are open examples.'])

# ---------------------------------------------------------------- Section 3
EXPLAIN_EXAMPLE = 'The scheme prints (4+1), (4+1), (3+2), (3+2) — Explain, Example — for the four required items without tying the larger split to any named item.'
add(3, 1, 'a', 'Q1(A)', lift(S23, 3, 'Illustrate your understanding of the following essential elements of a valid contract.') + '\n'
    + lift(S23, 3, 'Consideration', 'Capacity to Contract', 'Consent to Contract', 'Legality of form.'),
    20, 'business-0-12', 'valid-contract-elements', 3, [25], 'All four named elements are required, each with an example, using 5 marks each.',
    unequal('Element response', [(4, 1), (4, 1), (3, 2), (3, 2)], ['Explain', 'Example']),
    [EXPLAIN_EXAMPLE, 'Scheme: “' + scheme(25, 'Example required.') + '” for each element.'])
add(3, 1, 'b', 'Q1(B)', lift(S23, 3, 'Health unions to ballot members for industrial action over staff shortages') + '\n\n'
    + lift(S23, 3, 'Explain, using examples, the different types of industrial action.'), 20, 'business-0-14', 'industrial-action-types',
    3, [26], 'Explain four types at 5 marks each: Name 2, Explain 2, Example 1.', points('Type', 4, (2, 2, 1), ['Name', 'Explain', 'Example']))
bar = lift(S23, 3, '71 year old bar worker awarded €30,000 for age discrimination.')
add(3, 1, 'ci', 'Q1(C)(i)', bar + '\n\n' + lift(S23, 3, 'Define discrimination as set out in the Employment Equality Act 1998/2015.'), 12,
    'business-0-14', 'employment-equality-discrimination', 3, [27], 'Define the term for 12 marks (8 + 4).', [comps('Discrimination', (8, 4))])
c = add(3, 1, 'cii', 'Q1(C)(ii)', bar + '\n\n' + '(i) ' + lift(S23, 3, 'Define discrimination as set out in the Employment Equality Act 1998/2015.')
    + '\n(ii) ' + lift(S23, 3, 'List four grounds other than age and sexual orientation on which discrimination is outlawed under this act.'),
    8, 'business-0-14', 'discrimination-grounds', 3, [27],
    'List four grounds. The published sequence is 3, 3, 1, 1; part (i) is practised on its own card.',
    [comps('Grounds listed', (8,), ['Total from the published sequence'])],
    ['Scheme grounds: ' + '; '.join(scheme(27, g) for g in ['Civil (marital) status', 'Family status', 'Disability', 'Religion', 'Gender', 'Race',
                                                             'Membership of the Traveller community']) + '. Age and sexual orientation are excluded by the question.',
     'For 0, 1, 2, 3 or 4 correct grounds, record 0, 3, 6, 7 or 8 marks.',
     'The allocation summary on scheme page 7 prints “other than gender and sexual orientation”; the paper and support page 27 both exclude age, and the card follows the paper.'])
c['rubric']['responses'][0]['allocations'][0]['permittedMarks'] = [0, 3, 6, 7, 8]

add(3, 2, 'a', 'Q2(A)', lift(S23, 4, 'Illustrate your understanding of the following types of business organisations.') + '\n'
    + lift(S23, 4, 'Partnership', 'Sole Trader', 'Franchise', 'Public Limited Company'), 20, 'business-5-14', 'business-organisation-types',
    4, [28], 'All four named types are required, each with an example, using 5 marks each.',
    unequal('Organisation response', [(4, 1), (4, 1), (3, 2), (3, 2)], ['Explain', 'Example']),
    [EXPLAIN_EXAMPLE, 'Scheme: “' + scheme(28, 'Example required.') + '” for each type.'])
add(3, 2, 'b', 'Q2(B)', lift(S23, 4, "Recent Central Statistics Office figures show the country's unemployment rate stood at just 4.1% in November 2024 - signalling an economy which remains at full employment.")
    + '\n\n' + lift(S23, 4, 'Discuss the benefits and challenges of increasing employment for Irish businesses.'), 20, 'business-5-15',
    'increasing-employment-benefits-challenges', 4, [29, 30], 'Two benefits and two challenges are required at 5 marks each: Name 2, Explain 3.',
    seq(points('Benefit', 2, (2, 3), ['Name', 'Explain']), points('Challenge', 2, (2, 3), ['Name', 'Explain'])),
    ['Scheme: “' + scheme(29, '2 benefits and 2 challenges required') + '”.',
     'The support notes print “Limits the brain drain” after the challenges, although its explanation describes an advantage of higher employment.'])
add(3, 2, 'c', 'Q2(C)', lift(S23, 4, 'Hospitality, tourism and retail firms hold Dublin protest') + '\n\n'
    + lift(S23, 4, 'Outline how the Irish government could create a positive climate for business. Use examples to support your answer.'),
    20, 'business-5-15', 'government-positive-business-climate', 4, [31, 32], 'Outline four ways at 5 marks each: Name 2, Explain 2, Example 1.',
    points('Way', 4, (2, 2, 1), ['Name', 'Explain', 'Example']), ['Scheme: “' + scheme(31, 'Example required.') + '” for each way.'])

add(3, 3, 'ai', 'Q3(A)(i)', lift(S23, 5, 'Describe, with examples the difference between a directive and a regulation as forms of law in the European Union (EU).'),
    14, 'business-6-14', 'directive-versus-regulation', 5, [33], 'Describe both required forms at 7 marks each: Feature 4, Example 3.',
    [comps('Directive', (4, 3), ['Feature', 'Example'], 1), comps('Regulation', (4, 3), ['Feature', 'Example'], 2)])
add(3, 3, 'aii', 'Q3(A)(ii)', lift(S23, 5, 'Explain the impact of an established EU directive on Irish businesses.'), 6, 'business-6-14',
    'eu-directive-impact', 5, [33], 'Explain the impact for 6 marks (3 + 3).', [comps('Directive impact', (3, 3))],
    ['The directive is an open choice; the scheme’s WEEE and Renewable Energy Directive examples are not a menu.'])
add(3, 3, 'b', 'Q3(B)', lift(S23, 5, 'Outline the global marketing mix for a product of your choice.'), 20, 'business-6-15', 'global-marketing-mix',
    5, [34], 'All four elements are required at 5 marks each: Element 2, Explain 2, Example 1.',
    [comps(name, (2, 2, 1), ['Element', 'Explain', 'Example'], i) for i, name in
     enumerate(['Global Product', 'Global Price', 'Global Place', 'Global Promotion'], 1)],
    ['Scheme: “' + scheme(34, 'Reference to product of choice required.') + '” The product is an open choice.'])
add(3, 3, 'c', 'Q3(C)', lift(S23, 5, 'The goal of the World Trade Organisation (WTO) is to ensure that trade flows as smoothly and freely as possible.')
    + '\n\n' + lift(S23, 5, 'Illustrate the following barriers to free trade that can exist between countries.') + '\n'
    + lift(S23, 5, 'Embargo', 'Quota', 'Subsidy', 'Tariff'), 20, 'business-6-13', 'free-trade-barriers', 5, [35],
    'All four named barriers are required, each with an example, using 5 marks each.',
    unequal('Barrier response', [(4, 1), (4, 1), (3, 2), (3, 2)], ['Explain', 'Example']),
    [EXPLAIN_EXAMPLE, 'Scheme: “' + scheme(35, 'Example required.') + '” for each barrier.'])

add(3, 4, 'a', 'Q4(A)', lift(S23, 6, 'Illustrate each method of terminating a contract named below.') + '\n'
    + lift(S23, 6, 'Performance', 'Frustration', 'Breach of contract', 'Agreement'), 20, 'business-0-12', 'contract-termination-methods',
    6, [36], 'All four named methods are required, each with an example, using 5 marks each.',
    unequal('Method response', [(4, 1), (4, 1), (3, 2), (3, 2)], ['Explain', 'Example']),
    [EXPLAIN_EXAMPLE, 'Scheme: “' + scheme(36, 'Example required.') + '” for each method.'])
add(3, 4, 'b', 'Q4(B)', lift(S23, 6, 'A tech firm that admitted unfairly dismissing its Irish founder has been ordered to pay him a record €464,000 awards package by the Workplace Relations Commission (WRC).')
    + '\n\n' + lift(S23, 6, 'Explain, using an example, the grounds for dismissal that are deemed to be fair under the terms of the Unfair Dismissals Act 1977/2015.'),
    20, 'business-0-14', 'fair-dismissal-grounds', 6, [37, 38], 'Explain four grounds at 5 marks each: Ground 2, Explain 2, Example 1.',
    points('Ground', 4, (2, 2, 1), ['Ground', 'Explain', 'Example']))
add(3, 4, 'ci', 'Q4(C)(i)', lift(S23, 6, 'Explain the term a competitive relationship.'), 6, 'business-0-12', 'competitive-relationship-term',
    6, [39], 'Explain the term for 6 marks (3 + 3).', [comps('Competitive relationship', (3, 3))])
add(3, 4, 'cii', 'Q4(C)(ii)', lift(S23, 6, 'Explain the benefits to a business of competitive relationships between;') + '\n• '
    + lift(S23, 6, 'two suppliers') + '\n• ' + lift(S23, 6, 'two employees'), 14, 'business-0-12', 'competitive-relationship-benefits',
    6, [39], 'Both named relationships are required at 7 marks each (4 + 3).',
    [comps('Two suppliers', (4, 3), i=1), comps('Two employees', (4, 3), i=2)])

shaw = lift(S23, 7, '"The single biggest problem in communication is the illusion that it has taken place." — George Bernard Shaw')
add(3, 5, 'a', 'Q5(A)', shaw + '\n\n' + lift(S23, 7, 'Discuss the factors to consider when choosing an effective communication medium.'), 20,
    'business-2-12', 'communication-medium-factors', 7, [40], 'Discuss four factors at 5 marks each: Name 2, Explain 3.',
    points('Factor', 4, (2, 3), ['Name', 'Explain']))
add(3, 5, 'b', 'Q5(B)', lift(S23, 7, 'Conduct a SWOT analysis for a business of your choice.'), 20, 'business-2-13', 'swot-analysis',
    7, [41], 'All four SWOT elements are required at 5 marks each: Name 2, Reference 3.',
    [comps(name, (2, 3), ['Name', 'Reference'], i) for i, name in enumerate(['Strengths', 'Weaknesses', 'Opportunities', 'Threats'], 1)],
    ['The business is an open choice; each element needs a reference to it.'])
add(3, 5, 'ci', 'Q5(C)(i)', lift(S23, 7, 'Outline the implications of a manager adopting McGregor’s Theory X approach to management.'), 10,
    'business-2-11', 'theory-x-implications', 7, [42], 'Outline two implications at 5 marks each: Name 2, Explain 3.',
    points('Implication', 2, (2, 3), ['Name', 'Explain']))
add(3, 5, 'cii', 'Q5(C)(ii)', lift(S23, 7, 'Explain the factors that influence a manager to adopt a Theory X approach to management.'), 10,
    'business-2-11', 'theory-x-influencing-factors', 7, [42], 'Explain two factors at 5 marks each: Name 2, Explain 3.',
    points('Factor', 2, (2, 3), ['Name', 'Explain']))

royal = lift(S23, 8, 'The Royal Oak Hotel is a venue for evening functions such as Debs balls in the local area. There is also a restaurant and leisure centre in the hotel. They have requested a letter from their insurance provider, Super Insurance LTD, outlining the types of insurance they recommend a hotel should have in place.')
add(3, 6, 'a', 'Q6(A)', royal + '\n\n' + lift(S23, 8, 'Outline the different types of insurance that The Royal Oak Hotel should have in place.'), 20,
    'business-3-17', 'hotel-insurance-types', 8, [43], 'Outline four types at 5 marks each, using the published (4+1), (4+1), (3+2), (3+2) splits.',
    unequal('Insurance type', [(4, 1), (4, 1), (3, 2), (3, 2)], None),
    ['The scheme names the components Name and Explain without fixing which carries the larger share or which type earns the larger split.',
     'The scheme adds “' + scheme(43, 'Other types of insurance relevant to a hotel such as ‘Royal Oak’') + '”; all listed types are open examples.'])
add(3, 6, 'b', 'Q6(B)', lift(S23, 8, 'Discuss the strategies used to manage change in a business.'), 20, 'business-3-21', 'managing-change-strategies',
    8, [44], 'Discuss four strategies at 5 marks each (2 + 3).', points('Strategy', 4, (2, 3)))
gemma = lift(S23, 8, 'Gemma is a manager at The Royal Oak Hotel and earns a gross annual salary of €55,000. Her employer provides her with a Benefit in Kind worth €20,000. This is treated as income for tax purposes and is taxed accordingly.') \
    + '\n\n' + lift(S23, 8, 'PAYE', '20% on the first €44,000', '40% on the balance of her gross income.', 'Tax Credits',
                    'Single person Tax Credit €1,875 Employee Tax Credit €2,000', 'USC', '0.5% on the first €12,012', '2% on the next €9,281',
                    '3% on the balance', 'PRSI', '4% of her gross income') \
    + '\n\n' + lift(S23, 8, 'Calculate each of the following for Gemma. (show your workings)') + '\n'
OWN = 'The scheme marks its shaded figures on the candidate’s own figures (“' + scheme(45, 'Own figures are shaded.') + '”).'
add(3, 6, 'ci', 'Q6(C)(i)', gemma + lift(S23, 8, '(i) The PAYE which Gemma has to pay'), 10, 'business-3-18', 'paye-calculation', 8, [45],
    'Award the ten published PAYE marks.',
    [response(1, 'PAYE', [('taxable', 'Total taxable income: 75,000', 1), ('band1', '0·20 x 44,000 = 8,800', 1), ('balance', 'Balance: 31,000', 1),
                          ('band2', '0·40 x 31,000 = 12,400', 1), ('gross', 'Gross tax: 21,200', 1), ('single', 'Single Person Tax Credit: 1,875', 1),
                          ('employee', 'Employee Tax Credit: 2,000', 1), ('credits', 'Total credits: (3,875)', 1),
                          ('answer', 'PAYE which Gemma has to pay: ' + scheme(45, '17,325'), 2)])], [OWN],
    fix='the PAYE allocations follow the scheme’s ten printed marks')
add(3, 6, 'cii', 'Q6(C)(ii)', gemma + lift(S23, 8, '(ii) The total amount of USC paid.'), 6, 'business-3-18', 'usc-calculation', 8, [45],
    'Award the six published USC marks.',
    [response(1, 'USC', [('band1', '0·005 x 12,012 = ' + scheme(45, '60·06'), 1), ('band2', '0·02 x 9,281 = ' + scheme(45, '185·62'), 1),
                         ('balance', 'Balance: 53,707', 1), ('band3', '0·03 x 53,707 = ' + scheme(45, '1,611·21'), 1),
                         ('answer', 'Total USC paid: ' + scheme(45, '1,856·89'), 2)])], [OWN])
add(3, 6, 'ciii', 'Q6(C)(iii)', gemma + lift(S23, 8, '(iii) The total amount of PRSI paid'), 2, 'business-3-18', 'prsi-calculation', 8, [45],
    'Award the two published PRSI marks.', [response(1, 'PRSI', [('answer', 'Total PRSI paid: 0·04 x 75,000 = 3,000', 2)])], [OWN])
add(3, 6, 'civ', 'Q6(C)(iv)', gemma + 'Gemma’s results for parts (i)–(iii), from the marking scheme: PAYE ' + scheme(45, '17,325') + '; USC '
    + scheme(45, '1,856·89') + '; PRSI ' + scheme(45, '3,000') + '.\n' + lift(S23, 8, '(iv) Gemma’s net annual take-home pay.'), 2,
    'business-3-18', 'net-take-home-pay', 8, [45], 'Award 1 mark for total deductions and 1 for net annual take-home pay.',
    [response(1, 'Net take-home pay', [('deductions', 'Total deductions: ' + scheme(45, '22,181·89'), 1),
                                       ('answer', 'Net annual take-home pay: ' + scheme(45, '€32,818·11'), 1)])],
    ['Scheme working: gross salary 55,000 less total deductions 22,181·89. The Benefit in Kind is taxed but is not cash pay.', OWN],
    fix='parts (i)–(iii) results are supplied from the scheme so the two take-home marks can be practised independently')

glanbia = lift(S23, 9, 'Glanbia acquired The Optimum Nutrition brand in 2008. This was part of a shift in focus towards consumer nutrition products.')
add(3, 7, 'a', 'Q7(A)', glanbia + '\n\n' + lift(S23, 9, 'Discuss the advantages and disadvantages of an acquisition (takeover) as a method of business expansion.'),
    20, 'business-4-18', 'acquisition-advantages-disadvantages', 9, [46], 'Two advantages and two disadvantages are required at 5 marks each: Name 2, Explain 3.',
    seq(points('Advantage', 2, (2, 3), ['Name', 'Explain']), points('Disadvantage', 2, (2, 3), ['Name', 'Explain'])),
    ['Scheme: “' + scheme(46, '2 advantages and 2 disadvantages required') + '”.'])
add(3, 7, 'b', 'Q7(B)', glanbia + '\n\n' + lift(S23, 9, 'Illustrate four stages, apart from launch, that Glanbia may use for developing a new product.'), 20,
    'business-4-14', 'new-product-development-stages', 9, [47], 'Illustrate four stages at 5 marks each: Name 2, Explain 2, Reference/Example 1.',
    points('Stage', 4, (2, 2, 1), ['Name', 'Explain', 'Reference/Example']),
    ['Launch is excluded by the question. Scheme: “' + scheme(47, 'Reference/Example to Glanbia required.') + '”'])
add(3, 7, 'c', 'Q7(C)', lift(S23, 9, 'Anthem Transport Ltd is a large courier business with operations in Ireland. They purchased a small regional courier which has an aging fleet and outdated I.T. system.')
    + '\n\n' + lift(S23, 9, 'Discuss how Anthem Transport Ltd could use different medium-term sources of finance for their medium-term needs.'),
    20, 'business-3-16', 'medium-term-finance-sources', 9, [48],
    'Discuss three sources at 6 marks each (Source 3, Explain 3), plus 1 mark for each of two medium-term needs.',
    seq(points('Source', 3, (3, 3), ['Source', 'Explain']), response(0, 'Medium-term needs', [('need-1', 'Need 1', 1), ('need-2', 'Need 2', 1)])),
    ['Scheme medium-term needs: ' + scheme(48, 'Aging fleet') + '; ' + scheme(48, 'Outdated IT system') + '. Hire purchase, medium-term loan and leasing are the scheme’s sources; other valid medium-term sources are considered on their merits.'],
    fix='the three sources are open responses rather than fixed hire-purchase, loan and leasing rows')

pg = lift(S23, 10, 'Proctor and Gamble’s (P&G) brands include Pampers, Ariel, Gillette and Head & Shoulders.')
add(3, 8, 'ai', 'Q8(A)(i)', pg + '\n\n' + lift(S23, 10, 'Explain the term product portfolio.'), 6, 'business-4-17', 'product-portfolio',
    10, [49], 'Explain the term for 6 marks (3 + 3).', [comps('Product portfolio', (3, 3))])
add(3, 8, 'aii', 'Q8(A)(ii)', pg + '\n\n' + lift(S23, 10, 'Illustrate the different methods of market segmentation used by businesses such as Proctor and Gamble.'),
    14, 'business-4-16', 'market-segmentation-methods', 10, [49], 'Illustrate two methods at 7 marks each: Method 2, Explain 3, Reference 2.',
    points('Method', 2, (2, 3, 2), ['Method', 'Explain', 'Reference']), ['Scheme: “' + scheme(49, 'Example Required.') + '” for each method.'])
add(3, 8, 'b', 'Q8(B)', lift(S23, 10, 'Describe the reasons why a business conducts market research.'), 15, 'business-4-16', 'market-research-reasons',
    10, [50], 'Describe three reasons at 5 marks each: Name 3, Explain 2.', points('Reason', 3, (3, 2), ['Name', 'Explain']))
chart_data = pg + '\n\n' + lift(S23, 10, 'P&G have provided the following information for their new product line.') + '\n' + '\n'.join(
    lift(S23, 10, label) + ' ' + lift(S23, 10, value) for label, value in
    [('Forecast Output (Sales)', '200,000 units'), ('Selling Price per unit', '€10'), ('Fixed Costs', '€600,000'), ('Variable Costs per unit', '€5')])
chart_ask = lift(S23, 10, 'Illustrate the following by means of a breakeven chart:')
items = {'i': lift(S23, 10, '(i) Breakeven point'), 'ii': lift(S23, 10, '(ii) Margin of safety at the forecast output'),
         'iii': lift(S23, 10, '(iii) Profit at forecast output.')}
full = chart_data + '\n\n' + chart_ask + '\n' + '\n'.join(items.values())
CALC = ('Calculations only: ' + scheme(51, 'Break Even Point = 600,000 ÷ (10-5) = 120,000 units or €1,200,000 sales') + '; '
        + scheme(51, 'Margin of Safety = 200,000 – 120,000 = 80,000 units') + '; '
        + scheme(51, 'Profit at forecast output = 2,000,000 - (600,000 + 1,000,000) = €400,000') + '.')
add(3, 8, 'c', 'Q8(C)', full, 25, 'business-3-19', 'breakeven-chart-complete', 10, [51],
    ['Draw one labelled break-even chart: title 2, two axes 1 each, FC, TC and TR lines 3 each, and BEP, profit at forecast output and margin of safety 4 each.',
     'Calculations without a chart earn at most 12 (BEP 4, profit 4, margin of safety 4).'],
    [response(1, 'Chart construction', [('title', 'Title', 2), ('axis-1', 'Axis: Revenue and costs (€)', 1), ('axis-2', 'Axis: Units', 1),
                                        ('fc', 'Fixed costs line', 3), ('tc', 'Total costs line', 3), ('tr', 'Total revenue line', 3)]),
     response(2, 'Indicators', [('bep', 'Break-even point', 4), ('profit', 'Profit at forecast output', 4), ('mos', 'Margin of safety', 4)])],
    [CALC, 'If there is no chart, leave every chart-construction allocation at zero. Do not award an indicator twice for illustrating and calculating it.'])
add(3, 8, 'c1', 'Q8(C) — Break Even Chart: title and axes', full, 4, 'business-3-19', 'breakeven-chart-title-and-axes', 10, [51],
    'This card scores only the chart title (2) and the two axes (1 + 1) of the 25-mark chart. Practise the complete chart on the Q8(C) card.',
    [response(1, 'Title and axes', [('title', 'Title', 2), ('axis-1', 'Axis: Revenue and costs (€)', 1), ('axis-2', 'Axis: Units', 1)])],
    fix='the full printed task is shown and the card is labelled as one published component of the single 25-mark chart')
add(3, 8, 'c2', 'Q8(C) — chart lines', full, 9, 'business-3-19', 'breakeven-chart-lines', 10, [51],
    'This card scores only the fixed costs, total costs and total revenue lines (3 each) of the 25-mark chart. Practise the complete chart on the Q8(C) card.',
    [response(1, 'Chart lines', [('fc', 'Fixed costs line', 3), ('tc', 'Total costs line', 3), ('tr', 'Total revenue line', 3)])],
    fix='the full printed task is shown and the card is labelled as one published component of the single 25-mark chart')
for suffix, key, label, calc in [('ci', 'i', 'Break-even point', scheme(51, 'Break Even Point = 600,000 ÷ (10-5) = 120,000 units or €1,200,000 sales')),
                                 ('cii', 'ii', 'Margin of safety', scheme(51, 'Margin of Safety = 200,000 – 120,000 = 80,000 units')),
                                 ('ciii', 'iii', 'Profit at forecast output', scheme(51, 'Profit at forecast output = 2,000,000 - (600,000 + 1,000,000) = €400,000'))]:
    add(3, 8, suffix, f'Q8(C)({key})', chart_data + '\n\n' + chart_ask + '\n' + items[key], 4, 'business-3-19',
        f'breakeven-{label.lower().replace(" ", "-")}', 10, [51],
        f'Show the {label.lower()} on a break-even chart or by calculation for 4 marks; the scheme accepts either route once.',
        [response(1, label, [('indicator', label, 4)])], ['Calculation route: ' + calc + '.'])

# ---------------------------------------------------------------- checks
s1 = [c for c in created if c['section'] == '1']
s3 = [c for c in created if c['section'] == '3']
assert len(s1) == 16 and sum(c['totalMarks'] for c in s1) == 120
legacy_ids = {i for i, c in original.items() if c['year'] == year and c['level'] == 'higher' and c['section'] in ('1', '3')}
assert legacy_ids == {c['id'] for c in created} - {'bus-2025-hl-s3-q8c'}, legacy_ids ^ {c['id'] for c in created}
LEGACY_CHART = {f'bus-2025-hl-s3-q8{x}' for x in ['c1', 'c2', 'ci', 'cii', 'ciii']}
for q in range(1, 9):
    base = [c for c in s3 if c['questionRef'].split(' Q')[1].split('(')[0] == str(q) and c['id'] not in LEGACY_CHART]
    assert sum(c['totalMarks'] for c in base) == 60, (q, [(c['id'], c['totalMarks']) for c in base])

path = Path('components/MarkBank/cards/business/rubric-authored.json')
d = json.loads(path.read_text())
ids = {c['id'] for c in created}
d['cards'] = [c for c in d['cards'] if c['id'] not in ids] + created
d['reviews'] = [r for r in d['reviews'] if not (r['year'] == year and r['section'] in ['1', '3'])]
SELECTION = {
    1: 'No finite printed answer menu occurs in Section 1. Slash-separated circled options and matching rows are required answer formats for every row. The global businesses, causes, methods, factors and functions in the support notes are open examples. Each split part keeps its printed prompt and, for Q7(b), the Korn Ltd figures.',
    3: 'No finite printed choose-k pool occurs in Section 3. Named elements, organisation types, barriers and termination methods are all required headings. Benefits and challenges, advantages and disadvantages, Directive and Regulation, the two competitive relationships and the four SWOT elements are required, kept whole. Products, businesses, directives and the grounds, sources and stages in the support notes are open examples.',
}
for section, questions in [(1, range(1, 13)), (3, range(1, 9))]:
    for q in questions:
        cohort = [c for c in created if c['section'] == str(section) and c['questionRef'].split(' Q')[1].split('(')[0].split(' ')[0] == str(q)]
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

path = Path('data/examTopics/business-source-reviewed-topics.json')
t = json.loads(path.read_text())
t['questions'] = [r for r in t['questions'] if r['year'] != year]
for section, questions in [(1, range(1, 13)), (3, range(1, 9))]:
    for q in questions:
        cohort = [c for c in created if c['section'] == str(section) and c['questionRef'].split(' Q')[1].split('(')[0].split(' ')[0] == str(q)]
        topics = list(dict.fromkeys(x for c in cohort for x in [c['topicId']] + c.get('additionalTopicIds', [])))
        t['questions'].append(dict(year=year, level='higher', paperKey='p1' if section == 1 else 'p2', n=str(q), canonicalNodeIds=topics,
            reason=f'Every part of {year} Higher Section {section} Question {q} was visually checked against its SEC booklet, allocation summary and support notes. Booklet-specific p1/p2 identities keep the short and long question numbering apart.'))
abq = [c for c in d['cards'] if c['year'] == year and c['level'] == 'higher' and c['section'] == '2']
t['questions'].append(dict(year=year, level='higher', paperKey='p2', n='ABQ', abqTopicLabel='ABQ (Units 2, 3 & 4)',
    canonicalNodeIds=list(dict.fromkeys(c['topicId'] for c in abq)),
    reason='The paper names Units 2, 3 and 4 and assesses entrepreneurial skills, management control and HRM functions.'))
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
        w, page, m = item['wording'], item['page'], item['matchedText']
        if m.lower().startswith('answer'):
            cat, why = 'exam-navigation', 'The rubric sets how many whole questions a candidate answers. Every numbered question remains in the practice corpus as separate cards; no combined sitting card is created.'
        else:
            assert (doc['paperFileid'], page) in {(S1 + '.pdf', 2), (S1 + '.pdf', 8), (S1 + '.pdf', 40), (S23 + '.pdf', 12)}, item
            cat, why = 'exam-navigation', 'Pen/pencil instructions, answerbook supplies or copyright boilerplate. They do not create alternative task routes.'
        sel['reviews'][item['id']] = dict(wording=w, paperSha256=item['paperSha256'], classification=cat, reason=why)
        counted += 1
assert counted == 9, counted
path.write_text(json.dumps(sel, ensure_ascii=False, indent=2) + '\n')
print(f'Reviewed {len(created)} 2025 Higher tasks ({len(s1)} Section 1, {len(s3)} Section 3; {sum("correction" in c for c in created)} corrected legacy IDs); classified {counted} raw selection matches.')
