"""Review the 2023 Higher English Section 1 and Section 3 tasks.

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

year = 2023
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

TARIFF = {1: 6, (3, 1): 8, (3, 2): 9, (3, 3): 10, (3, 4): 11, (3, 5): 12, (3, 6): 13, (3, 7): 14, (3, 8): 15}
created = []
REF_FIXES = {'bus-2023-hl-s1-q5a', 'bus-2023-hl-s3-q1ai', 'bus-2023-hl-s3-q1aii', 'bus-2023-hl-s3-q8c1', 'bus-2023-hl-s3-q8c2', 'bus-2023-hl-s3-q8c3'}
NEW_IDS = {'bus-2023-hl-s1-q5a-diagram', 'bus-2023-hl-s3-q8c'}

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
elverys = lift(S1, 3, 'Sports retail chain InterSport Elverys is an Irish indigenous firm.')
add(1, 1, 'a', 'Q1(a)', elverys + ' ' + lift(S1, 3, 'Explain the term indigenous firm.'), 4, 'business-5-13', 'indigenous-firm', 3, [16],
    'Explain the term for 4 marks.', [comps('Indigenous firm', (4,), ['Explanation'])])
add(1, 1, 'b', 'Q1(b)', lift(S1, 3, 'Outline two challenges that may be experienced by an indigenous business in Ireland.'), 6, 'business-5-13',
    'indigenous-firm-challenges', 3, [16], 'Outline two challenges at 3 marks each (2 + 1).', points('Challenge', 2, (2, 1)))
cumulative(2, lift(S1, 3, 'In the context of business, what do the following letters stand for? Write each answer in the space provided.',
                   'TQM', 'ISME', 'JIT', 'EDI', 'ROI'),
           'business-3-21', 'business-abbreviations', 3, [17],
           'Answer key: TQM: ' + scheme(17, 'Total Quality Management') + '; ISME: ' + scheme(17, 'Irish Small and Medium Enterprise')
           + '; JIT: ' + scheme(17, 'Just in Time') + '; EDI: ' + scheme(17, 'Electronic Data Interchange') + '; ROI: ' + scheme(17, 'Return on Investment') + '.',
           ['business-0-12', 'business-2-13', 'business-2-12', 'business-3-19'])
add(1, 3, 'a', 'Q3(a)', lift(S1, 4, 'Explain, with an example, the term invisible exports.'), 4, 'business-6-13', 'invisible-exports', 4, [17],
    'Explain the term for 2 marks (1 + 1) and give an example for 2 marks.', [comps('Invisible exports', (1, 1, 2), ['Explanation', 'Development', 'Example'])],
    ['Scheme: “' + scheme(17, 'Example Required') + '”. The allocation summary prints 4 (1,1,2).'])
add(1, 3, 'b', 'Q3(b)', lift(S1, 4, 'Using the following data, calculate the following:', '(i) Balance of Trade (ii) Balance of Payments.',
                            'State in each case whether it is a surplus or deficit.') + '\n\n'
    + lift(S1, 4, 'Visible Exports €70bn', 'Invisible Imports €40bn', 'Total Exports €100bn', 'Total Imports €90bn'), 6, 'business-6-13',
    'trade-and-payments-calculation', 4, [17], 'Award the six published calculation marks.',
    [response(1, 'Balance of Trade and Balance of Payments', [('visible-imports', 'Visible imports: €90bn − €40bn = €50bn', 2),
                                                               ('trade', 'Balance of Trade: €70bn − €50bn = €20bn', 1), ('trade-surplus', 'Balance of Trade: surplus', 1),
                                                               ('payments', 'Balance of Payments: 100bn − 90bn = €10bn', 1), ('payments-surplus', 'Balance of Payments: surplus', 1)])],
    ['Scheme marks (read from the rendered page): visible imports 2, Balance of Trade 1 and surplus 1, Balance of Payments 1 and surplus 1; ' + scheme(17, 'Own figure') + '.'])
cumulative(4, '\n'.join([
    lift(S1, 5, 'Column 1 is a list of European Institutions. Column 2 is a list of possible explanations. (One explanation does not refer to any of the terms.)'),
    '', lift(S1, 5, 'Column 1: Institutions', '1 European Central Bank', '2 European Court of Auditors', '3 European Parliament',
             '4 Council of the European Union', '5 European Commission'),
    '', lift(S1, 5, 'Column 2: Explanations', 'A Directly elected by citizens of all member states of the European Union (EU).',
             'B Decides on disputes between member states, EU institutions, businesses and individuals.',
             'C Key decision-making body in the EU, meetings attended by relevant ministers of each state.',
             'D Manages the euro currency and the EU’s monetary policy.',
             'E Audits the spending of the EU budget and reports on EU finances.',
             'F Responsible for the day to day management of the EU and proposes new EU Laws.'),
    '', lift(S1, 5, 'Match the two lists by placing the letter of the correct explanation under the relevant number below.')]),
    'business-6-14', 'eu-institutions-matching', 5, [17],
    'Answer key: 1 D; 2 E; 3 A; 4 C; 5 F' + (' (scheme grid “1 2 3 4 5 D E A C F”).' if scheme(17, '1 2 3 4 5 D E A C F') else '') + ' Explanation B is unused.')
structure = lift(S1, 6, 'Draft and label a functional organisational structure for a manufacturing firm.')
add(1, 5, 'a-diagram', 'Q5(a)', structure, 6, 'business-2-13', 'functional-structure-diagram', 6, [18],
    'Draft and label the structure using the published 3 @ 2 marks.',
    [response(1, 'Functional structure', [(f'component-{k}', f'Component {k}', 2) for k in (1, 2, 3)])],
    ['Scheme: “' + scheme(18, 'Title: Functional Structure of a manufacturing firm.') + '” and “' + scheme(18, 'Production dept required.')
     + '” Its model chart shows a Managing Director over Production, Finance and Marketing departments, each with its employees. The scheme does not name the third 2-mark component, so the three are not tied to named boxes.'])
add(1, 5, 'a', 'Q5(a) — title and production department', structure, 4, 'business-2-13', 'functional-structure-title-production', 6, [18],
    'This card scores only the two components the scheme names, the title (2) and the production department (2), of the 6-mark structure. Practise the complete diagram on the Q5(a) card.',
    [response(1, 'Named components', [('title', 'Title', 2), ('production', 'Production department', 2)])],
    ['Scheme: “' + scheme(18, 'Title: Functional Structure of a manufacturing firm.') + '” and “' + scheme(18, 'Production dept required.') + '”'],
    fix='the full printed task is shown and the card is labelled as two named components of the 6-mark structure')
add(1, 5, 'b', 'Q5(b)', lift(S1, 6, 'Outline one impact of choosing this type of organisational structure.'), 4, 'business-2-13',
    'functional-structure-impact', 6, [18], 'Outline one impact for 4 marks (2, 2).', [comps('Impact', (2, 2))])
add(1, 6, '', 'Q6', lift(S1, 6, 'Distinguish between penetration pricing and price skimming.'), 10, 'business-4-17', 'penetration-versus-skimming',
    6, [19], 'Explain both required terms at 5 marks each (3 + 2).', [comps('Penetration pricing', (3, 2), i=1), comps('Price skimming', (3, 2), i=2)])
liquid = lift(S1, 7, 'Liquidity issues continue to be a cause of concern for many small businesses.')
add(1, 7, 'a', 'Q7(a)', liquid + '\n\n' + lift(S1, 7, 'Explain the term liquidity.'), 4, 'business-3-19', 'liquidity-term', 7, [19],
    'Explain the term for 4 marks (2 + 2).', [comps('Liquidity', (2, 2))])
add(1, 7, 'b', 'Q7(b)', liquid + '\n\n' + lift(S1, 7, 'The figures below are taken from Cahill’s newsagents.', 'Calculate the Acid Test Ratio for Cahill’s newsagents.')
    + '\n' + lift(S1, 7, 'Closing Stock 14,000', 'Current Assets 93,200', 'Current Liabilities 72,000'), 6, 'business-3-19', 'acid-test-ratio', 7, [19],
    'Award formula 2 and four one-mark calculation points.',
    [response(1, 'Acid test ratio', [('formula', 'Formula: (Current Assets − closing stock) : Current Liabilities', 2), ('assets', 'Current assets: €93,200', 1),
                                     ('stock', 'Closing stock: €14,000', 1), ('liabilities', 'Current liabilities: €72,000', 1), ('answer', 'Answer: 1.1:1', 1)])],
    ['Scheme working: (€93,200 − €14,000) : €72,000 = €79,200 : €72,000 = 1.1:1.'])
add(1, 8, 'a', 'Q8(a)', lift(S1, 8, 'Explain the term national minimum wage.'), 5, 'business-5-15', 'national-minimum-wage', 8, [20],
    'Explain the term for 5 marks (3 + 2).', [comps('National minimum wage', (3, 2))],
    ['The scheme quotes the 2023 rates; use the examination-year context.'])
add(1, 8, 'b', 'Q8(b)', lift(S1, 8, 'Describe one possible economic impact on Irish businesses of the increase in the national minimum wage.'), 5,
    'business-5-15', 'minimum-wage-increase-impact', 8, [20], 'Describe one impact for 5 marks (3 + 2).', [comps('Impact', (3, 2))])
cumulative(9, lift(S1, 8, 'Write TRUE or FALSE after each of the following statements.',
                   '1. The Aviva Stadium is an example of a company using the Public Relations method known as Celebrity Endorsements.',
                   '2. McDonalds selling a rice burger and teriyaki burger in Japan is an example of the need to adapt the Global Product element of the marketing mix.',
                   '3. An impact of moving from job production to batch production is that the business may lose their Unique Selling Point.',
                   '4. Capital Acquisitions Tax is a tax on the profits made on the sale of assets.',
                   '5. The Q Mark is a quality standard awarded by Excellence Ireland Quality Association.'),
           'business-4-17', 'business-statements-true-false', 8, [20],
           'Answer key: 1 False; 2 True; 3 True; 4 False; 5 True' + ('.' if scheme(20, 'False True True False True') else ''),
           ['business-6-15', 'business-4-15', 'business-3-18', 'business-2-13'])
add(1, 10, '', 'Q10', lift(S1, 9, 'Outline two characteristics/skills associated with entrepreneurs.'), 10, 'business-1-5', 'entrepreneur-characteristics',
    9, [21], 'Outline two characteristics at 5 marks each (3 + 2).', points('Characteristic', 2, (3, 2)))
add(1, 11, '', 'Q11', lift(S1, 9, 'Data Protection Commission Fines WhatsApp Further €5.5m Over GDPR Breach') + '\n\n'
    + lift(S1, 9, 'Explain two rights of the data subject (an individual) under data protection law.'), 10, 'business-2-12', 'data-subject-rights',
    9, [22], 'Explain two rights at 5 marks each (3 + 2).', points('Right', 2, (3, 2)))
add(1, 12, 'a', 'Q12(a)', lift(S1, 10, 'Distinguish between two types of meetings which are common in a business.'), 6, 'business-2-12', 'meeting-types',
    10, [23], 'Explain two meeting types at 3 marks each (1 + 2).', points('Meeting type', 2, (1, 2)),
    ['The two types are an open choice; AGM, EGM, board and ad-hoc meetings in the support notes are examples.'])
add(1, 12, 'b', 'Q12(b)', lift(S1, 10, 'Outline two benefits of meetings as a method of communication.'), 4, 'business-2-12', 'meeting-benefits',
    10, [23], 'Outline two benefits at 2 marks each.', [comps(f'Benefit {i}', (2,), ['Benefit outlined'], i) for i in (1, 2)])

# ---------------------------------------------------------------- Section 3
relq = lift(S23, 3, 'Describe one example of a co-operative relationship and one example of a competitive relationship that could arise between the following stakeholders:') \
    + '\n' + lift(S23, 3, '(i) Employer and employee', '(ii) Investor and the manager of a business.')
for suffix, kind, label in [('ai', 'co-operative', 'Co-operative relationship'), ('aii', 'competitive', 'Competitive relationship')]:
    add(3, 1, suffix, f'Q1(A) — {kind} relationship', relq, 10, 'business-0-12', f'{kind}-relationships', 3, [30, 31],
        f'The scheme marks (A) as 2 @ 10 (2, 2 @ 4 (3 + 1)): one 10-mark block per relationship type. This card is the {kind} block: definition 2, then one example for each stakeholder pair at 4 (3 + 1).',
        [response(1, label, [('definition', f'{label} defined', 2)]),
         response(2, 'Employer and employee', [('example', 'Example', 3), ('develop', 'Development', 1)]),
         response(3, 'Investor and manager', [('example', 'Example', 3), ('develop', 'Development', 1)])],
        ['Practise the other relationship type on its companion Q1(A) card; together they make the 20-mark task.'],
        fix='the full printed question is restored and the card is labelled as the published 10-mark relationship block')
rights = lift(S23, 3, 'The Consumer Rights Directive and EU regulations enhanced consumer rights in Ireland.') + ' ' + lift(S23, 3, 'EU regulations now clarify ‘Your right to cancel’.')
add(3, 1, 'bi', 'Q1(B)(i)', rights + '\n\n' + lift(S23, 3, 'Outline three provisions of the Sale of Goods and Supply of Services Act 1980 regarding a consumer’s statutory rights.'),
    18, 'business-0-13', 'sale-of-goods-provisions', 3, [32, 33], 'Outline three provisions at 6 marks each (3 + 3).', points('Provision', 3, (3, 3)))
add(3, 1, 'bii', 'Q1(B)(ii)', rights + '\n\n' + lift(S23, 3, 'Explain the ‘right to cancel’ (cooling off period) for consumers in Ireland.'), 2,
    'business-0-13', 'right-to-cancel', 3, [33], 'Explain the right for 2 marks.', [comps('Right to cancel', (2,), ['Explanation'])])
add(3, 1, 'c', 'Q1(C)', lift(S23, 3, 'Illustrate your understanding of the following essential elements of a valid contract.') + '\n'
    + lift(S23, 3, 'Consideration Legality of Form Intention to Contract').replace(' Legality', '\nLegality').replace(' Intention', '\nIntention'), 20,
    'business-0-12', 'valid-contract-elements', 3, [34], 'All three named elements are required, with examples, using 8 (4 + 4), 8 (4 + 4) and 4 (2 + 2) marks.',
    unequal('Element response', [(4, 4), (4, 4), (2, 2)], ['Explain', 'Example']),
    ['The larger allowances are not tied to a particular element. Scheme: “' + scheme(34, 'Example required for full marks') + '” for each.'])

boi = lift(S23, 4, 'The state completes sell down of Bank of Ireland stake.')
add(3, 2, 'ai', 'Q2(A)(i)', boi + '\n\n' + lift(S23, 4, 'Distinguish between nationalisation and privatisiation. Provide examples to support your answer.'), 10,
    'business-5-15', 'nationalisation-versus-privatisation', 4, [35], 'Explain both required terms with examples at 5 marks each.',
    [comps('Nationalisation', (3, 2), i=1), comps('Privatisation', (3, 2), i=2)],
    ['The allocation summary prints 2 x 5m (3+2); the support page prints 2@5(2+3). Both give two five-mark responses; the card keeps the summary sequence without naming the components.'],
    extra=['business-5-14'])
add(3, 2, 'aii', 'Q2(A)(ii)', boi + '\n\n' + lift(S23, 4, 'Describe one benefit and one challenge of privatisation for the government.'), 10, 'business-5-15',
    'privatisation-benefit-and-challenge', 4, [35, 36], 'One benefit and one challenge are required at 5 marks each.',
    [comps('Benefit', (2, 3), i=1), comps('Challenge', (2, 3), i=2)],
    ['The allocation summary prints 2 x 5m (2 + 3); the support page prints 2@5(3+2). The card keeps the summary sequence.',
     'Scheme: “' + scheme(36, 'Due to a mismatch between the Irish and English versions of the examination paper, accept answers describing one benefit and one challenge of privatisation from any stakeholder’s point of view.') + '”'],
    extra=['business-5-14'])
add(3, 2, 'b', 'Q2(B)', lift(S23, 4, 'Outline why a business, over time, might change their ownership structure. Provide examples to support your answer.'), 20,
    'business-5-14', 'changing-ownership-structure', 4, [37], 'Outline three reasons with examples using 7 (2 + 3 + 2), 7 (2 + 3 + 2) and 6 (2 + 2 + 2) marks.',
    unequal('Reason', [(2, 3, 2), (2, 3, 2), (2, 2, 2)], None), ['The larger allowances are not tied to particular reasons.'])
add(3, 2, 'c', 'Q2(C)', lift(S23, 4, 'During the pandemic, people have become more sensitive to the environmental impact of their shopping. Companies have responded to the rise of the eco-friendly consumer.')
    + '\n\n' + lift(S23, 4, 'Discuss the characteristics of an environmentally responsible business.'), 20, 'business-5-17',
    'environmentally-responsible-characteristics', 4, [38], 'Discuss four characteristics at 5 marks each (2 + 3).', points('Characteristic', 4, (2, 3)))

add(3, 3, 'a', 'Q3(A)', lift(S23, 5, 'Outline the importance of European Union (EU) membership for Ireland.'), 20, 'business-6-14', 'eu-membership-importance',
    5, [39], 'Outline four points at 5 marks each (2 + 3).', points('Point', 4, (2, 3)))
c = add(3, 3, 'b', 'Q3(B)', lift(S23, 5, 'Evaluate the role of special interest groups in the European Union (EU). Use an example to support your answer.'), 15,
    'business-6-14', 'eu-special-interest-groups', 5, [40], 'Two roles at 5 marks each (2 + 3), an example for 2 marks and an evaluation of 0, 1 or 3 marks.',
    seq(points('Role', 2, (2, 3)), response(0, 'Example', [('example', 'Example', 2)]), response(0, 'Evaluation', [('evaluate', 'Evaluation', 3)])),
    ['Scheme: “' + scheme(40, 'Example required for full marks') + '”. The evaluation is awarded as 0, 1 or 3.'])
c['rubric']['responses'][-1]['allocations'][0]['permittedMarks'] = [0, 1, 3]
add(3, 3, 'c', 'Q3(C)', lift(S23, 5, 'Discuss the positive and negative impacts of multinational companies (MNC’s) in Ireland. Use examples to support your answer.'), 25,
    'business-6-15', 'mnc-impacts-ireland', 5, [41, 42], 'Two positive and two negative impacts are required: one at 7 (2 + 3 + 2) and three at 6 (2 + 2 + 2).',
    unequal('Impact', [(2, 3, 2), (2, 2, 2), (2, 2, 2), (2, 2, 2)], None),
    ['Scheme: “Two of each required”. The 7-mark allowance is not tied to a positive or negative impact.'])

pay = lift(S23, 6, 'The Taoiseach says 6.5% public sector pay offer is fair.')
add(3, 4, 'ai', 'Q4(A)(i)', pay + '\n\n' + lift(S23, 6, 'Explain the term collective bargaining.'), 5, 'business-0-14', 'collective-bargaining',
    6, [43], 'Explain the term for 5 marks (2 + 3).', [comps('Collective bargaining', (2, 3))])
add(3, 4, 'aii', 'Q4(A)(ii)', pay + '\n\n' + lift(S23, 6, 'Outline three provisions of the Industrial Relations Act 1990.'), 15, 'business-0-14',
    'industrial-relations-act-provisions', 6, [43, 44], 'Outline three provisions at 5 marks each (2 + 3).', points('Provision', 3, (2, 3)))
add(3, 4, 'b', 'Q4(B)', lift(S23, 6, 'Under the terms of the Unfair Dismissals Act 1997 to 2021, explain the grounds for dismissal that are deemed to be fair.'), 20,
    'business-0-14', 'fair-dismissal-grounds', 6, [44, 45], 'Explain four grounds at 5 marks each (2 + 3).', points('Ground', 4, (2, 3)),
    ['The allocation summary names the Act “1997 to 2007”; the paper and support page say 1997 to 2021, and the card follows the paper.'])
add(3, 4, 'c', 'Q4(C)', lift(S23, 6, 'Discuss the services provided by the Workplace Relations Commission.'), 20, 'business-0-14', 'wrc-services',
    6, [46, 47], 'Discuss four services at 5 marks each (2 + 3).', points('Service', 4, (2, 3)))

gavin = lift(S23, 7, 'Jim Gavin, Director of People and Operations in the Irish Aviation Authority, is a speaker on leadership and motivation. He references motivational theorists such as Douglas McGregor and Abraham Maslow.')
add(3, 5, 'a', 'Q5(A)', gavin + '\n\n' + lift(S23, 7, 'Outline, giving an example, how a business manager could use each level of Maslow’s Hierarchy of Needs to motivate their staff.'),
    25, 'business-2-11', 'maslow-levels-motivation', 7, [48], 'All five levels are required at 5 marks each (2 + 2 + 1), each with an example.',
    [comps(name, (2, 2, 1), None, i) for i, name in enumerate(['Physical needs', 'Safety needs', 'Social needs', 'Esteem needs', 'Self-actualisation'], 1)])
add(3, 5, 'b', 'Q5(B)', gavin + '\n\n' + lift(S23, 7, 'Explain three implications for a manager of adopting a Theory Y approach to management.'), 15, 'business-2-11',
    'theory-y-implications', 7, [49], 'Explain three implications at 5 marks each (2 + 3).', points('Implication', 3, (2, 3)),
    ['Scheme: “' + scheme(49, 'Implications can be negative, such as:') + '”'])
add(3, 5, 'ci', 'Q5(C)(i)', lift(S23, 7, 'Distinguish between enterprise and management.'), 10, 'business-1-5', 'enterprise-versus-management',
    7, [50], 'Explain both required terms at 5 marks each (2 + 3).', [comps('Enterprise', (2, 3), i=1), comps('Management', (2, 3), i=2)],
    extra=['business-2-13'])
add(3, 5, 'cii', 'Q5(C)(ii)', lift(S23, 7, 'Discuss two benefits of planning as a management activity.'), 10, 'business-2-13', 'planning-benefits',
    7, [50], 'Discuss two benefits at 5 marks each (2 + 3).', points('Benefit', 2, (2, 3)))

utility = lift(S23, 8, 'Due to major increases in utility bills, business owners may cancel insurance premiums or under insure their risks.')
add(3, 6, 'ai', 'Q6(A)(i)', utility + '\n\n' + lift(S23, 8, 'Explain one implication of underinsurance.'), 5, 'business-3-17', 'underinsurance-implication',
    8, [51], 'Explain one implication for 5 marks (2 + 3).', [comps('Implication', (2, 3))])
add(3, 6, 'aii', 'Q6(A)(ii)', utility + '\n\n' + lift(S23, 8, 'Discuss two types of business insurance that you recommend a hotel business should have.'), 10,
    'business-3-17', 'hotel-insurance-types', 8, [51], 'Discuss two types at 5 marks each (2 + 3).', points('Insurance type', 2, (2, 3)),
    ['The allocation summary prints 2 x 5m (2+3), matching the two types asked; the support page header 3@5(2+3) is inconsistent with the question and the 15-mark part. Scheme: “'
     + scheme(51, 'Any relevant type of insurance for a hotel accepted.') + '”'])
flex = lift(S23, 8, 'New employees will seek flexible working conditions if pay demands are not met.')
add(3, 6, 'bi', 'Q6(B)(i)', flex + '\n\n' + lift(S23, 8, 'Explain the term flexible working conditions.'), 5, 'business-3-20', 'flexible-working-conditions',
    8, [52], 'Explain the term for 5 marks (2 + 3).', [comps('Flexible working conditions', (2, 3))])
add(3, 6, 'bii', 'Q6(B)(ii)', flex + '\n\n' + lift(S23, 8, 'Outline the different types of financial and non-financial rewards that businesses use to attract employees.'), 15,
    'business-3-20', 'financial-and-non-financial-rewards', 8, [52, 53], 'Outline three rewards at 5 marks each (2 + 3), with at least one financial and one non-financial reward.',
    points('Reward', 3, (2, 3)), ['Scheme: “At least one of each required.”'])
hr = lift(S23, 8, 'In 2022 recruitment companies noticed that Human Resource forecasts were adapted as the economy struggled with a cost of living crisis.')
add(3, 6, 'c', 'Q6(C)', hr + '\n\n' + lift(S23, 8, 'Explain the following terms in the context of human resource management.') + '\n'
    + lift(S23, 8, '● Job Description and Person Specification.', '● Internal and External Recruitment.', '● Interview and Selection.'), 25,
    'business-3-20', 'hrm-recruitment-terms', 8, [54], 'All five terms are required at 5 marks each (2 + 3).',
    [comps(name, (2, 3), None, i) for i, name in enumerate(['Job Description', 'Person Specification', 'Internal Recruitment', 'External Recruitment', 'Interview and Selection'], 1)],
    ['The scheme marks 5 @ 5m (2+3): job description, person specification, internal recruitment, external recruitment, and interview and selection.'])

parcs = lift(S23, 9, 'Centre Parcs Longford features 400 acres of beautiful forest, swimming pool, a range of restaurants, activities and accommodation types.')
add(3, 7, 'a', 'Q7(A)', parcs + '\n\n' + lift(S23, 9, 'Outline the internal and external sources of new product/service ideas for businesses such as Centre Parcs.'), 20,
    'business-4-14', 'new-idea-sources', 9, [55], 'Two internal and two external sources are required at 5 marks each (2 + 3).',
    seq(points('Internal source', 2, (2, 3)), points('External source', 2, (2, 3))), ['Scheme: “Two of each required”.'])
tommy = lift(S23, 9, 'Tommy is a manager at Centre Parcs Ireland and earns a gross annual salary of €85,000. His employer provides him with a company car worth €25,000. This is treated as income for tax purposes and is taxed accordingly.') \
    + '\n\n' + lift(S23, 9, 'Tommy’s tax information is shown below.') + '\n' + lift(S23, 9, 'PAYE', '20% on the first €40,000', '40% on the balance of his gross income',
    'TAX CREDITS', 'Single Person Tax Credit €1,700', 'PAYE Tax Credit €1,700', 'Dependent Relative Tax Credit €245', 'USC', '0.5% up to €12,012',
    '2% on the next €9,281', '4.5% on the balance', 'PRSI', 'Tommy pays employee PRSI at 4% of his gross income') + '\n\n' + lift(S23, 9, 'Calculate each of the following:') + '\n'
OWN = 'The scheme marks the bold figures on the candidate’s own figures (“' + scheme(56, 'Own figures are shown in bold.') + '”).'
add(3, 7, 'bi', 'Q7(B)(i)', tommy + lift(S23, 9, '(i) The PAYE which Tommy has to pay'), 10, 'business-3-18', 'paye-calculation', 9, [56],
    'Award the ten published PAYE marks.',
    [response(1, 'PAYE', [('taxable', 'Taxable income: 110,000', 2), ('band1', '40,000 x 0.20 = 8,000', 3), ('balance', 'Balance: 70,000', 1),
                          ('band2', '70,000 x 0.40 = 28,000', 1), ('gross', 'Gross PAYE: 36,000', 1), ('credits', 'Tax credits: (3,645)', 1),
                          ('answer', 'PAYE Tommy has to pay: €32,355', 1)])], [OWN])
add(3, 7, 'bii', 'Q7(B)(ii)', tommy + lift(S23, 9, '(ii) The total amount of USC'), 7, 'business-3-18', 'usc-calculation', 9, [56],
    'Award the seven published USC marks.',
    [response(1, 'USC', [('band1', '12,012 x 0.005 = 60.06', 3), ('band2', '9,281 x 0.02 = 185.62', 1), ('balance', 'Balance: 88,707', 1),
                         ('band3', '88,707 x 0.045 = 3,991.82', 1), ('answer', 'Total USC: €4,237.50', 1)])], [OWN])
add(3, 7, 'biii', 'Q7(B)(iii)', tommy + lift(S23, 9, '(iii) The total amount of PRSI'), 1, 'business-3-18', 'prsi-calculation', 9, [56],
    'Award the one published PRSI mark.', [response(1, 'PRSI', [('answer', 'Total PRSI: 110,000 x 0.04 = €4,400', 1)])], [OWN])
add(3, 7, 'biv', 'Q7(B)(iv)', tommy + 'Tommy’s results for parts (i)–(iii), from the marking scheme: PAYE €32,355; USC €4,237.50; PRSI €4,400.\n'
    + lift(S23, 9, '(iv) Tommy’s annual take-home pay'), 2, 'business-3-18', 'take-home-pay', 9, [56], 'Award the two published marks for annual net pay.',
    [response(1, 'Annual take-home pay', [('answer', 'Annual net pay: €44,007.50', 2)])],
    ['Scheme working: gross salary 85,000 less PAYE 32,355.00, USC 4,237.50 and PRSI 4,400.00 (40,992.50). The company car is taxed but is not cash pay.', OWN],
    fix='parts (i)–(iii) results are supplied from the scheme so the take-home marks can be practised independently')
add(3, 7, 'ci', 'Q7(C)(i)', lift(S23, 9, 'Explain the term employee empowerment.'), 5, 'business-2-11', 'employee-empowerment',
    9, [57], 'Explain the term for 5 marks (2 + 3).', [comps('Employee empowerment', (2, 3))])
add(3, 7, 'cii', 'Q7(C)(ii)', lift(S23, 9, 'Describe the benefits of employee empowerment for a business.'), 15, 'business-2-11', 'employee-empowerment-benefits',
    9, [57], 'Describe three benefits at 5 marks each (2 + 3).', points('Benefit', 3, (2, 3)),
    ['The allocation summary prints 3 x 5m (2+3), matching the 15 marks remaining in (C); the support page header 2@5(2+3) is inconsistent with that total.'])

epik = lift(S23, 10, 'EPIK Media produce, shoot and package behind the scenes content for movies, tv series and events. The business has worked on movies such as ‘Jurassic Park Dominion’ and ‘The Banshees of Inisherin’.')
add(3, 8, 'ai', 'Q8(A)(i)', epik + '\n\n' + lift(S23, 10, 'Illustrate your understanding of the term niche market.'), 7, 'business-4-16', 'niche-market',
    10, [58], 'Illustrate the term for 7 marks (3, 2, 2).', [comps('Niche market', (3, 2, 2))])
add(3, 8, 'aii', 'Q8(A)(ii)', epik + '\n\n' + lift(S23, 10, 'Outline two implications for a business of operating in a niche market.'), 8, 'business-4-16',
    'niche-market-implications', 10, [58], 'Outline two implications at 4 marks each (2 + 2).', points('Implication', 2, (2, 2)))
netflix = lift(S23, 10, 'Netflix and Sky, the two entertainment giants will continue their successful subscription package.')
add(3, 8, 'bi', 'Q8(B)(i)', netflix + '\n\n' + lift(S23, 10, 'Contrast a strategic alliance and a merger as methods of business expansion.'), 10, 'business-4-18',
    'strategic-alliance-versus-merger', 10, [59], 'Explain both required methods at 5 marks each (2 + 3).',
    [comps('Strategic alliance', (2, 3), i=1), comps('Merger', (2, 3), i=2)])
add(3, 8, 'bii', 'Q8(B)(ii)', netflix + '\n\n' + lift(S23, 10, 'Evaluate one benefit and one challenge for a business of forming a strategic alliance.'), 10, 'business-4-18',
    'strategic-alliance-benefit-challenge', 10, [59], 'One benefit and one challenge are required at 4 marks each (2 + 2), plus 2 marks for evaluation.',
    seq(comps('Benefit', (2, 2)), comps('Challenge', (2, 2)), evaluation()), ['Scheme: “' + scheme(59, 'Evaluation Required') + '”'])
mj = lift(S23, 10, 'MJ Sports produce products aimed at Hurling and Camogie players. MJ Sports have provided the following information for their new product line:') \
    + '\n' + lift(S23, 10, 'Forecast Output (Sales) 8,000 units', 'Selling Price per unit €20', 'Fixed Costs €40,000', 'Variable Costs per unit €10') \
    + '\n\n' + lift(S23, 10, 'Illustrate the following by means of a breakeven chart:') + '\n' + lift(S23, 10, '(i) Breakeven point', '(ii) Margin of safety at the forecast output', '(iii) Profit at forecast output.')
CALC = 'Calculations only: break-even point 40,000/10 = 4,000 units; margin of safety 8,000 − 4,000 = 4,000 units; profit at forecast output €160,000 − €120,000 = €40,000.'
add(3, 8, 'c', 'Q8(C)', mj, 25, 'business-3-19', 'breakeven-chart-complete', 10, [60],
    ['Draw one labelled break-even chart: X axis 1, Y axis 1, title 1, FC line 2, TC and TR lines 4 each, and BEP, margin of safety and profit at forecast output 4 each.',
     'Calculations without a chart earn at most 12 (break-even point 4, profit 4, margin of safety 4).'],
    [response(1, 'Chart construction', [('x-axis', 'X axis: output in units', 1), ('y-axis', 'Y axis: revenue/costs/sales €', 1), ('title', 'Title of chart', 1),
                                        ('fc', 'Fixed costs line', 2), ('tc', 'Total costs line', 4), ('tr', 'Total revenue line', 4)]),
     response(2, 'Indicators', [('bep', 'Break-even point', 4), ('mos', 'Margin of safety', 4), ('profit', 'Profit at forecast output', 4)])],
    [CALC, 'If there is no chart, leave every chart-construction allocation at zero. Do not award an indicator twice for illustrating and calculating it.'])
add(3, 8, 'c1', 'Q8(C) — calculations-only route', mj, 12, 'business-3-19', 'breakeven-calculations-only', 10, [60],
    'This card scores the calculations-only route, which the scheme caps at 12 (4 each). Practise the complete 25-mark chart on the Q8(C) card.',
    [response(1, 'Calculations', [('bep', 'Break-even point: 4,000 units', 4), ('mos', 'Margin of safety: 4,000 units', 4), ('profit', 'Profit at forecast output: €40,000', 4)])],
    [CALC], fix='the card is labelled as the published calculations-only route of the 25-mark chart')
add(3, 8, 'c2', 'Q8(C) — chart title, Y axis and fixed cost line', mj, 4, 'business-3-19', 'breakeven-chart-presentation', 10, [60],
    'This card scores only the chart title (1), Y axis (1) and fixed cost line (2) of the 25-mark chart. Practise the complete chart on the Q8(C) card.',
    [response(1, 'Chart components', [('y-axis', 'Y axis: revenue/costs/sales €', 1), ('title', 'Title of chart', 1), ('fc', 'Fixed costs line', 2)])],
    ['The X axis mark (1) is scored on the complete chart card.'], fix='the card is labelled as published components of the single 25-mark chart')
add(3, 8, 'c3', 'Q8(C) — chart lines and readings', mj, 20, 'business-3-19', 'breakeven-chart-lines-readings', 10, [60],
    'This card scores only the TC and TR lines and the three readings (4 each) of the 25-mark chart. Practise the complete chart on the Q8(C) card.',
    [response(1, 'Chart lines and readings', [('tc', 'Total costs line', 4), ('tr', 'Total revenue line', 4), ('bep', 'Break-even point', 4),
                                              ('mos', 'Margin of safety', 4), ('profit', 'Profit at forecast output', 4)])],
    [], fix='the card is labelled as published components of the single 25-mark chart')

# ---------------------------------------------------------------- checks
COMPONENTS = {'bus-2023-hl-s1-q5a', 'bus-2023-hl-s3-q8c1', 'bus-2023-hl-s3-q8c2', 'bus-2023-hl-s3-q8c3'}
s1 = [c for c in created if c['section'] == '1']
s3 = [c for c in created if c['section'] == '3']
assert sum(c['totalMarks'] for c in s1 if c['id'] not in COMPONENTS) == 120, sum(c['totalMarks'] for c in s1 if c['id'] not in COMPONENTS)
for q in range(1, 13):
    tot = sum(c['totalMarks'] for c in s1 if c['questionRef'].split(' Q')[1].split('(')[0].split(' ')[0] == str(q) and c['id'] not in COMPONENTS)
    assert tot == 10, (q, tot)
legacy_ids = {i for i, c in original.items() if c['year'] == year and c['level'] == 'higher' and c['section'] in ('1', '3')}
assert legacy_ids == {c['id'] for c in created} - NEW_IDS, legacy_ids ^ {c['id'] for c in created}
for q in range(1, 9):
    base = [c for c in s3 if c['questionRef'].split(' Q')[1].split('(')[0].split(' ')[0] == str(q) and c['id'] not in COMPONENTS]
    assert sum(c['totalMarks'] for c in base) == 60, (q, [(c['id'], c['totalMarks']) for c in base])

path = Path('components/MarkBank/cards/business/rubric-authored.json')
d = json.loads(path.read_text())
ids = {c['id'] for c in created}
d['cards'] = [c for c in d['cards'] if c['id'] not in ids] + created
d['reviews'] = [r for r in d['reviews'] if not (r['year'] == year and r['section'] in ['1', '3'])]
SELECTION = {
    1: 'No finite printed answer menu occurs in Section 1. True/False labels, the surplus-or-deficit determinations and matching rows are required answer formats. Meeting types, entrepreneurial characteristics, data-subject rights and challenges in the support notes are open examples. Each split part keeps its printed prompt and data.',
    3: 'No finite printed choose-k pool occurs in Section 3. Named elements, both stakeholder pairs, all five Maslow levels, the five HRM terms, benefits and challenges, internal and external sources, positive and negative impacts, and financial and non-financial rewards are required and kept whole. Insurance types, grounds, services and reasons in the support notes are open examples.',
}
def qnum(c):
    return c['questionRef'].split(' Q')[1].split('(')[0].split(' ')[0]
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

path = Path('data/examTopics/business-source-reviewed-topics.json')
t = json.loads(path.read_text())
t['questions'] = [r for r in t['questions'] if not (r['year'] == year and r['n'] != 'ABQ')]
for section, questions in [(1, range(1, 13)), (3, range(1, 9))]:
    for q in questions:
        cohort = [c for c in created if c['section'] == str(section) and qnum(c) == str(q)]
        topics = list(dict.fromkeys(x for c in cohort for x in [c['topicId']] + c.get('additionalTopicIds', [])))
        t['questions'].append(dict(year=year, level='higher', paperKey='p1' if section == 1 else 'p2', n=str(q), canonicalNodeIds=topics,
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
        if m.lower().startswith('answer'):
            cat, why = 'exam-navigation', 'The rubric sets how many whole questions a candidate answers. Every numbered question remains in the practice corpus as separate cards; no combined sitting card is created.'
        elif 'surplus or deficit' in w or 'Surplus or Deficit' in w:
            cat, why = 'required-headings', 'Section 1 Q3(b) requires the candidate to state whether each balance is a surplus or a deficit. It is a required determination with its own mark, not a choice of task.'
        elif 'TRUE or FALSE' in w:
            cat, why = 'required-headings', 'True/False are answer labels for each of the five required statements in Section 1 Q9, not optional tasks. All five stay in one exercise with the shared 3,2,2,2,1 tariff.'
        elif 'under insure their risks' in w:
            cat, why = 'case-context', 'The Section 3 Q6 extract says business owners may cancel premiums or under insure. It is case context for the underinsurance task, not an instruction to choose an answer.'
        else:
            assert (doc['paperFileid'], page) in {(S1 + '.pdf', 2), (S1 + '.pdf', 11), (S1 + '.pdf', 40), (S23 + '.pdf', 12)}, item
            cat, why = 'exam-navigation', 'Pen/pencil instructions, answerbook supplies or copyright boilerplate. They do not create alternative task routes.'
        sel['reviews'][item['id']] = dict(wording=w, paperSha256=item['paperSha256'], classification=cat, reason=why)
        counted += 1
path.write_text(json.dumps(sel, ensure_ascii=False, indent=2) + '\n')
print(f'Reviewed {len(created)} 2023 Higher tasks ({len(s1)} Section 1, {len(s3)} Section 3; {sum("correction" in c for c in created)} corrected legacy IDs); classified {counted} raw selection matches.')
