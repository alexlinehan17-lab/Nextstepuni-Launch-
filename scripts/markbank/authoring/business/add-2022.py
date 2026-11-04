"""Review the 2022 Higher English Section 1 and Section 3 tasks.

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

year = 2022
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
NEW_IDS = set()

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
    '', lift(S1, 3, 'Column 1: Terms', '1. Gross Domestic Product', '2. Economic Recession', '3. Interest Rate', '4. Exchange Rate', '5. Unemployment Rate'),
    '', lift(S1, 3, 'Column 2: Explanations', 'A A decrease in the demand for goods and services in an economy for two consecutive quarters.',
             'B The price of one currency expressed in terms of another currency.',
             'C The sustained percentage increase in the price of goods and services in an economy from one period to the next.',
             'D The cost of borrowing money from a financial institution.', 'E Measures the value of goods and services produced in a country.',
             'F The percentage of people out of work but actively seeking employment.'),
    '', lift(S1, 3, 'Match the two lists by placing the letter of the correct explanation under the relevant number below.')]),
    'business-5-15', 'economic-terms-matching', 3, [14],
    'Answer key: 1 E; 2 A; 3 D; 4 B; 5 F' + (' (scheme grid “1 2 3 4 5 E A D B F”).' if scheme(14, '1 2 3 4 5 E A D B F') else '') + ' Explanation C is unused.')
cumulative(2, lift(S1, 3, 'In the context of business, what do the following letters stand for? Write each answer in the space provided.', 'WTO', 'EMU', 'IDA', 'FDI', 'CAP'),
           'business-6-13', 'business-abbreviations', 3, [14],
           'Answer key: ' + '; '.join(scheme(14, s) for s in ['WTO World Trade Organisation', 'EMU Economic & Monetary Union', 'IDA Industrial Development Agency/Authority',
                                                             'FDI Foreign Direct Investment', 'CAP Common Agricultural Policy']) + '.',
           ['business-6-14', 'business-5-15', 'business-6-15'])
add(1, 3, 'a', 'Q3(a)', lift(S1, 4, 'Explain the term Product Life Cycle.'), 4, 'business-4-17', 'product-life-cycle-term', 4, [14],
    'Explain the term for 4 marks (2 + 2).', [comps('Product Life Cycle', (2, 2))])
add(1, 3, 'b', 'Q3(b)', lift(S1, 4, 'Outline two methods firms such as Coca Cola could use to extend a Product Life Cycle.'), 6, 'business-4-17',
    'extending-product-life-cycle', 4, [14], 'Outline two methods at 3 marks each (2 + 1).', points('Method', 2, (2, 1)))
cumulative(4, lift(S1, 4, 'Circle the correct option in the case of each of the following statements.',
                   '(i) Maslow / McGregor believed that once a need is satisfied the need immediately above in the hierarchy becomes the dominant motivator.',
                   '(ii) Theory X / Theory Y managers believe workers are hardworking and self-motivated.',
                   '(iii) Workplace friendships satisfy social / safety needs.',
                   '(iv) There is a high / low staff turnover if managers trust and respect employees.',
                   '(v) Physiological / Self-actualisation needs are satisfied by challenging work.'),
           'business-2-11', 'motivation-statements-options', 4, [14],
           'Answer key: (i) Maslow; (ii) Theory Y; (iii) Social; (iv) Low; (v) Self-actualisation.' if scheme(14, 'i. Maslow ii. Theory Y iii. Social iv. Low v. Self-actualisation') else '')
c = add(1, 5, '', 'Q5', lift(S1, 5, 'Draft an email from Mike Hannon, Sales Manager to all staff at superstore.ie outlining two rights customers have under General Data Protection Regulation (GDPR).'),
    10, 'business-2-12', 'gdpr-rights-email', 5, [15], 'Email format 5 @ 1 mark; two GDPR rights at 3 and 2 marks.',
    [response(1, 'Email format', [('recipients', 'Recipients', 1), ('subject', 'Subject', 1), ('greeting', 'Greeting', 1), ('closing', 'Closing', 1), ('sender', 'Sender’s name', 1)]),
     response(2, 'GDPR rights', [('right-1', 'Right 1', 3), ('right-2', 'Right 2', 2)])],
    ['Scheme format marks (read from the rendered page): ' + scheme(15, 'staff@superstore.ie') + ', subject ' + scheme(15, 'GDPR') + ', a greeting, “Regards” and Mike Hannon. The larger right allowance is not tied to a particular right.'],
    extra=['business-0-13'])
add(1, 6, '', 'Q6', lift(S1, 5, 'The rate of inflation in Ireland is currently soaring as the cost of energy, transport and housing has accelerated on the back of pent-up demand and supply chain bottlenecks.')
    + '\n\n' + lift(S1, 5, 'Explain how the Consumer Price Index works.'), 10, 'business-5-15', 'consumer-price-index', 5, [16],
    'Explain how the index works for 10 marks (4 + 3 + 3).', [comps('Consumer Price Index', (4, 3, 3))])
cumulative(7, lift(S1, 6, 'Write True or False after each of the following statements.',
                   '1. The treasurer is responsible for taking the minutes of a meeting.',
                   '2. A disadvantage of meetings is that they allow for clarification and feedback.',
                   '3. An extraordinary general meeting of shareholders must take place annually.',
                   '4. AOB is usually listed at the top of a meeting agenda.',
                   '5. A quorum refers to the number of members/shareholders who must be present before a meeting can take place.'),
           'business-2-12', 'meetings-true-false', 6, [16], 'Answer key (scheme page 16): 1 False; 2 False; 3 False; 4 False; 5 True.')
add(1, 8, 'i', 'Q8(i)', lift(S1, 6, 'Explain the term protectionism.'), 4, 'business-6-13', 'protectionism', 6, [17],
    'Explain the term for 4 marks (2 + 2).', [comps('Protectionism', (2, 2))])
add(1, 8, 'ii', 'Q8(ii)', lift(S1, 6, 'Outline two protectionist measures that are used by governments/trading blocs.'), 6, 'business-6-13', 'protectionist-measures',
    6, [17], 'Outline two measures at 3 marks each (2 + 1).', points('Measure', 2, (2, 1)))
add(1, 9, '', 'Q9', lift(S1, 7, 'The following information is supplied by Fleming Ltd.') + '\n'
    + lift(S1, 7, 'Forecasted Output (Sales) 75,000 units', 'Fixed Costs €55,000', 'Selling price per unit €6', 'Variable Costs per unit €2.50') + '\n\n'
    + lift(S1, 7, 'Using the information provided above calculate the following:') + '\n'
    + lift(S1, 7, '(a) Total Revenue at forecasted output', '(b) Total Costs of Production at forecasted output', '(c) Profit at forecasted output',
           '(d) Breakeven point (BEP) in units (It is not necessary to draw a breakeven chart)'),
    10, 'business-3-19', 'fleming-breakeven-calculations', 7, [18], 'All four calculations are required: 3, 3, 2 and 2 marks.',
    [response(1, 'Calculations', [('revenue', 'Total revenue: €450,000', 3), ('costs', 'Total costs: €242,500', 3), ('profit', 'Profit: €207,500', 2),
                                  ('bep', 'Break-even point: 15,714.2 units', 2)])],
    ['Scheme workings: ' + scheme(18, '75000 x 6') + '; ' + scheme(18, '55,000 + (75,000x2.5)') + '; ' + scheme(18, '450,000-242,500') + '; 55,000 ÷ 3.5 = ' + scheme(18, '15,714.2') + '.'])
add(1, 10, '', 'Q10', lift(S1, 7, 'Distinguish between visible imports and import substitution. Provide examples to support your answer.'), 10, 'business-6-13',
    'visible-imports-versus-import-substitution', 7, [18], 'Explain both required terms with examples at 5 marks each (3 + 2).',
    [comps('Visible imports', (3, 2), i=1), comps('Import substitution', (3, 2), i=2)])
add(1, 11, '', 'Q11', lift(S1, 8, 'Outline two ways to minimise bad debts for a business.'), 10, 'business-3-16', 'minimising-bad-debts', 8, [19],
    'Outline two ways at 5 marks each (3 + 2).', points('Way', 2, (3, 2)))
c = add(1, 12, '', 'Q12', lift(S1, 8, 'Kellie Murphy started a new job. She registered her details on the revenue website my account.') + '\n'
    + lift(S1, 8, 'Calculate the amount of PAYE Kellie Murphy will pay annually. Show your workings.') + '\n\n'
    + lift(S1, 8, 'Kellie has a salary of €42,600.', 'PAYE is to be calculated as 20% on the first €36,800 and 40% on the balance.',
           'Kellie has the following tax credits; personal tax credit €1,700, employee tax credit €1,700.'),
    10, 'business-3-18', 'paye-calculation', 8, [20], 'Gross PAYE 4 (four one-mark figures), tax credits 4 and PAYE due 2.',
    [response(1, 'Gross PAYE', [('band1', '36,800 x 0.20 = 7,360', 1), ('balance', 'Balance: 42,600 − 36,800 = 5,800', 1),
                                ('band2', '5,800 x 0.40 = 2,320', 1), ('gross', 'Total gross PAYE: 9,680', 1)]),
     response(2, 'Tax credits', [('credits', 'Tax credits: 1,700 + 1,700 = 3,400', 4)]),
     response(3, 'PAYE due', [('answer', 'PAYE due: 9,680 − 3,400 = €6,280', 2)])],
    ['Scheme: “' + scheme(20, 'Award 2 marks if a candidate just uses ‘1700’') + '”. ' + scheme(20, 'Own figures shaded') + '.'])
c['rubric']['responses'][1]['allocations'][0]['permittedMarks'] = [0, 2, 4]

# ---------------------------------------------------------------- Section 3
unions = lift(S23, 3, 'Public service unions affiliated to the Irish Congress of Trade Unions overwhelmingly endorsed the new public service agreement.')
add(3, 1, 'ai', 'Q1(A)(i)', unions + '\n\n' + lift(S23, 3, 'Explain the term trade union.'), 5, 'business-0-14', 'trade-union', 3, [28],
    'Explain the term for 5 marks (2 + 3).', [comps('Trade union', (2, 3))])
add(3, 1, 'aii', 'Q1(A)(ii)', unions + '\n\n' + lift(S23, 3, 'Illustrate the impact of trade disputes on any three stakeholders.'), 15, 'business-0-14',
    'trade-dispute-stakeholder-impacts', 3, [28], 'Illustrate the impact on three stakeholders at 5 marks each (2 + 3).', points('Stakeholder', 3, (2, 3)),
    ['The stakeholders are an open choice; the paper prints no list. The support notes name suppliers, government, consumers, employees, investors and the employer as examples.'])
add(3, 1, 'b', 'Q1(B)', lift(S23, 3, 'Outline the non-legislative methods of resolving industrial relations disputes.'), 15, 'business-0-14',
    'non-legislative-dispute-resolution', 3, [29], 'Outline three methods at 5 marks each (2 + 3).', points('Method', 3, (2, 3)))
add(3, 1, 'ci', 'Q1(C)(i)', lift(S23, 3, 'Define the term discrimination as set out in the Employment Equality Act 1998-2015.'), 6, 'business-0-14',
    'employment-equality-discrimination', 3, [30], 'Define the term for 6 marks (3 + 3).', [comps('Discrimination', (3, 3))])
c = add(3, 1, 'cii', 'Q1(C)(ii)', lift(S23, 3, 'List five grounds on which discrimination is banned under the Employment Equality Act.'), 12, 'business-0-14',
    'discrimination-grounds', 3, [30], 'List five grounds. The published sequence is 3, 3, 2, 2, 2.',
    [comps('Grounds listed', (12,), ['Total from the published sequence'])],
    ['Scheme grounds: ' + '; '.join(scheme(30, g) for g in ['Civil (marital) status', 'Family status', 'Sexual orientation', 'Religion', 'Age', 'Race',
                                                         'Membership of the Traveller community', 'Gender', 'Disability']) + '.',
     'For 0, 1, 2, 3, 4 or 5 correct grounds, record 0, 3, 6, 8, 10 or 12 marks.'])
c['rubric']['responses'][0]['allocations'][0]['permittedMarks'] = [0, 3, 6, 8, 10, 12]
add(3, 1, 'ciii', 'Q1(C)(iii)', lift(S23, 3, 'Outline the role of the Workplace Relations Commission in resolving cases of discrimination.'), 7, 'business-0-14',
    'wrc-discrimination-role', 3, [30], 'Outline the role for 7 marks: 4 (2 + 2) and 3 (2 + 1).',
    [comps('Role 1', (2, 2), i=1), comps('Role 2', (2, 1), i=2)],
    ['The support notes place 4 (2+2) beside mediation and 3 (2+1) beside adjudication; other roles are considered on their merits.'])

braw = lift(S23, 4, 'Anna Coffey Lynch is an Irish artisan chocolatier. She started her own business, Braw Chocolates, in the middle of the Covid 19 pandemic.')
add(3, 2, 'b', 'Q2(B)', braw + '\n\n' + lift(S23, 4, 'Discuss how the Irish Government could create a positive climate for businesses like Braw Chocolate. Use examples to illustrate your answer.'),
    20, 'business-5-15', 'government-positive-business-climate', 4, [33, 34], 'Discuss three ways using 7 (3 + 3 + 1), 7 (3 + 3 + 1) and 6 (3 + 2 + 1) marks.',
    unequal('Way', [(3, 3, 1), (3, 3, 1), (3, 2, 1)], None), ['The larger allowances are not tied to particular ways.'])
add(3, 2, 'ci', 'Q2(C)(i)', lift(S23, 4, 'Distinguish between the primary sector and the tertiary sector of the economy.'), 10, 'business-5-13',
    'primary-versus-tertiary-sector', 4, [35], 'Explain both required sectors at 5 marks each (2 + 3).',
    [comps('Primary sector', (2, 3), i=1), comps('Tertiary sector', (2, 3), i=2)])
add(3, 2, 'cii', 'Q2(C)(ii)', lift(S23, 4, 'Outline the current trends affecting businesses in the tertiary sector of the Irish economy.'), 10, 'business-5-13',
    'tertiary-sector-trends', 4, [35, 36], 'Outline two trends at 5 marks each (2 + 3).', points('Trend', 2, (2, 3)),
    ['Use the 2022 examination context.'])

ei = lift(S23, 5, 'Enterprise Ireland is the government organisation responsible for the development and growth of Irish enterprises in world markets. It works in partnership with Irish enterprises to help them start, grow, innovate and win export sales in global markets.')
add(3, 3, 'a', 'Q3(A)', ei + '\n\n' + lift(S23, 5, 'Outline the challenges of global marketing that an Irish business may face when trading internationally.'), 20,
    'business-6-15', 'global-marketing-challenges', 5, [37], 'Outline three challenges using 7 (4 + 3), 7 (4 + 3) and 6 (3 + 3) marks.',
    unequal('Challenge', [(4, 3), (4, 3), (3, 3)], None), ['The larger allowances are not tied to particular challenges; the marketing-mix headings in the support notes are examples.'])
add(3, 3, 'bi', 'Q3(B)(i)', ei + '\n\n' + lift(S23, 5, 'Illustrate, by using an example, your understanding of the term an indigenous business.'), 5, 'business-5-13',
    'indigenous-business', 5, [38], 'Illustrate the term with an example for 5 marks (2 + 3).', [comps('Indigenous business', (2, 3))],
    ['Scheme: “Example Required.”'])
add(3, 3, 'bii', 'Q3(B)(ii)', ei + '\n\n' + lift(S23, 5, 'Discuss the benefits for large indigenous businesses of exporting to new markets.'), 15, 'business-6-13',
    'indigenous-exporting-benefits', 5, [38], 'Discuss three benefits at 5 marks each (2 + 3).', points('Benefit', 3, (2, 3)),
    ['The support notes restate the question as “opportunities ... of exporting internationally”; the card follows the paper.'])
add(3, 3, 'c', 'Q3(C)', lift(S23, 5, 'The 1st January 2023 will be the 50th anniversary of Ireland joining the EEC (which is now known as the European Union).') + '\n\n'
    + lift(S23, 5, 'Describe the role of the European Commission and the European Parliament in the decision making process of the European Union.'), 20,
    'business-6-14', 'commission-and-parliament-roles', 5, [39], 'Describe three roles using 7 (4 + 3), 7 (4 + 3) and 6 (3 + 3) marks, with at least one for each institution.',
    unequal('Role', [(4, 3), (4, 3), (3, 3)], None), ['Scheme: “At least one from each.” The larger allowances are not tied to a particular institution.'])

ucp = lift(S23, 6, 'The EU Directive on Unfair Commercial Practices became law in Ireland through the Consumer Protection Act 2007. Under the Act, a range of unfair, misleading, and aggressive trading practices are prohibited.')
add(3, 4, 'a', 'Q4(A)', ucp + '\n\n' + lift(S23, 6, 'Explain the provisions of the Consumer Protection Act 2007, with reference to the following:') + '\n'
    + lift(S23, 6, '1. Price display regulations.', '2. Providing misleading, false or inaccurate information.', '3. Enforcement of the act.'), 20,
    'business-0-13', 'consumer-protection-act-provisions', 6, [40, 41], 'All three named headings are required, using 7 (4 + 3), 7 (4 + 3) and 6 (3 + 3) marks.',
    unequal('Heading response', [(4, 3), (4, 3), (3, 3)], None), ['The larger allowances are not tied to a particular heading.'])
protected = lift(S23, 6, 'Consumers are protected when dealing with retailers and when using public services.')
add(3, 4, 'bi', 'Q4(B)(i)', protected + '\n\n' + lift(S23, 6, 'Outline the role of The Office of the Ombudsman.'), 8, 'business-0-13', 'ombudsman-role',
    6, [42], 'Outline the role for 8 marks (4 + 4).', [comps('Office of the Ombudsman', (4, 4))])
add(3, 4, 'bii', 'Q4(B)(ii)', protected + '\n\n' + lift(S23, 6, 'Describe two features of the Small Claims Procedure/Small Claims Court.'), 12, 'business-0-13',
    'small-claims-features', 6, [43], 'Describe two features at 6 marks each (3 + 3).', points('Feature', 2, (3, 3)))
add(3, 4, 'c', 'Q4(C)', lift(S23, 6, 'Breach of Contract occurs when one party in a legally binding contract does not honour/fulfil their part of the legal agreement.') + '\n\n'
    + lift(S23, 6, 'Outline three remedies for Breach of Contract.'), 20, 'business-0-12', 'breach-of-contract-remedies', 6, [44],
    'Outline three remedies using 7 (4 + 3), 7 (4 + 3) and 6 (3 + 3) marks.', unequal('Remedy', [(4, 3), (4, 3), (3, 3)], None),
    ['The larger allowances are not tied to particular remedies.'])

m6 = lift(S23, 7, 'Alan Naughton is an entrepreneur who set up M6 Motors in 2011. The business is now one of the leading car sourcing companies in Ireland. As the business grew Alan expanded his workforce. The company specialises in high specification cars at competitive prices.')
add(3, 5, 'a', 'Q5(A)', m6 + '\n\n' + lift(S23, 7, 'Evaluate two leadership styles the business manager at M6 Motors could adopt, provide reasons for your choice.'), 20,
    'business-2-11', 'leadership-styles-evaluation', 7, [45, 46], 'Evaluate two styles at 10 marks each: Name 2, Explain 3, Explain 3, Link 2.',
    points('Leadership style', 2, (2, 3, 3, 2), ['Name', 'Explain', 'Explain', 'Link']), ['The styles are an open choice; democratic, autocratic and laissez-faire in the support notes are examples.'])
add(3, 5, 'b', 'Q5(B)', m6 + '\n\n' + lift(S23, 7, 'Discuss how stock control and quality control achieve efficiencies for a business such as M6 Motors.'), 20,
    'business-2-13', 'stock-and-quality-control', 7, [46, 47], 'Both required controls at 10 marks each: Explain 4, Explain 4, Reference 2.',
    [comps('Stock control', (4, 4, 2), ['Explain', 'Explain', 'Reference'], 1), comps('Quality control', (4, 4, 2), ['Explain', 'Explain', 'Reference'], 2)])
add(3, 5, 'ci', 'Q5(C)(i)', lift(S23, 7, 'Explain the term intrapreneurship.'), 5, 'business-1-5', 'intrapreneurship', 7, [47],
    'Explain the term for 5 marks (2 + 3).', [comps('Intrapreneurship', (2, 3))])
add(3, 5, 'cii', 'Q5(C)(ii)', lift(S23, 7, 'Outline three methods a business could use to encourage intrapreneurship.'), 15, 'business-1-5',
    'encouraging-intrapreneurship', 7, [47], 'Outline three methods at 5 marks each (2 + 3).', points('Method', 3, (2, 3)))

remote = lift(S23, 8, 'The increase in the numbers of employees now working remotely from home has changed the traditional office beyond recognition. The role of the Human Resources (HR) Manager has never been more important.')
add(3, 6, 'ai', 'Q6(A)(i)', remote + '\n\n' + lift(S23, 8, 'Discuss any three functions of the HR Manager in a business.'), 15, 'business-3-20',
    'hr-manager-functions', 8, [48, 49], 'Discuss three functions at 5 marks each (2 + 3).', points('Function', 3, (2, 3)),
    ['The functions are an open choice; the paper prints no list.'])
add(3, 6, 'aii', 'Q6(A)(ii)', remote + '\n\n' + lift(S23, 8, 'Analyse the impact of remote working on one of the Human Resource Management functions.'), 5,
    'business-3-20', 'remote-working-hrm-impact', 8, [49], 'Analyse the impact for 5 marks (2 + 3).', [comps('Impact', (2, 3))])
add(3, 6, 'bi', 'Q6(B)(i)', lift(S23, 8, 'Explain the term risk management.'), 5, 'business-3-17', 'risk-management', 8, [50],
    'Explain the term for 5 marks (2 + 3).', [comps('Risk management', (2, 3))])
add(3, 6, 'bii', 'Q6(B)(ii)', lift(S23, 8, 'Outline the different ways a business can minimise risks.'), 15, 'business-3-17', 'minimising-risks',
    8, [50], 'Outline three ways at 5 marks each (2 + 3).', points('Way', 3, (2, 3)))

crew = lift(S23, 9, 'The Cleaning Crew, a home and industry cleaning company based in Wexford, has seen growth in demand for its services across the south. It is considering expanding the company across Ireland based on research undertaken. Management are considering all finance options to fund expansion.')
table = lift(S23, 9, 'The following figures are taken from the final accounts of The Cleaning Crew for 2021 and 2020.') + '\n' + lift(
    S23, 9, 'The Cleaning Crew 2021 2020', 'Authorised Share Capital €750,000 €750,000', 'Issued Share Capital €460,000 €300,000',
    'Long-term Loan €150,000 €250,000', 'Retained Earnings €140,000 €120,000')
add(3, 7, 'ai', 'Q7(A)(i)', crew + '\n\n' + lift(S23, 9, 'Explain the term Debt/Equity Ratio.'), 5, 'business-3-19', 'debt-equity-ratio-term', 9, [52],
    'Explain the term for 5 marks (2 + 3).', [comps('Debt/Equity Ratio', (2, 3))])
add(3, 7, 'aii', 'Q7(A)(ii)', crew + '\n\n' + table + '\n\n' + lift(S23, 9, 'Calculate the Debt/Equity Ratio for 2021 and 2020. Show your workings.'), 15,
    'business-3-19', 'debt-equity-ratio-two-years', 9, [52], 'Formula 3, then each year 6 (2 + 1 + 1 + 2).',
    seq(response(0, 'Formula', [('formula', 'Formula: Debt Capital : Equity Capital (long-term loan : issued share capital + reserves)', 3)]),
        response(0, '2021', [('debt', 'Long-term loan: €150,000', 2), ('shares', 'Issued share capital: €460,000', 1), ('retained', 'Retained earnings: €140,000', 1),
                             ('answer', '0.25 : 1', 2)]),
        response(0, '2020', [('debt', 'Long-term loan: €250,000', 2), ('shares', 'Issued share capital: €300,000', 1), ('retained', 'Retained earnings: €120,000', 1),
                             ('answer', '0.6 : 1', 2)])),
    ['Authorised share capital is not part of equity.'])
add(3, 7, 'aiii', 'Q7(A)(iii)', crew + '\n\nThe Cleaning Crew’s Debt/Equity Ratio, from the marking scheme: 0.25 : 1 in 2021 and 0.6 : 1 in 2020.\n'
    + lift(S23, 9, 'Comment as to whether the Debt/Equity Ratio has improved or disimproved?'), 5, 'business-3-19', 'debt-equity-ratio-comment', 9, [52],
    'Comment for 5 marks (2 + 3).', [comps('Comment', (2, 3))],
    ['Scheme: “' + scheme(52, 'The gearing ratio improved from 0.6:1 in 2020 to 0.25:1in 2021.') + '”'],
    fix='the two ratios are supplied from the scheme so the comment can be practised independently')
add(3, 7, 'b', 'Q7(B)', crew + '\n\n' + lift(S23, 9, 'Apart from the Debt/Equity Ratio, discuss the factors a business should consider when choosing a source of finance.'), 20,
    'business-3-16', 'finance-source-factors', 9, [53], 'Discuss four factors at 5 marks each (2 + 3).', points('Factor', 4, (2, 3)))
add(3, 7, 'c', 'Q7(C)', lift(S23, 9, 'Outline the importance of businesses engaging in market research.'), 15, 'business-4-16', 'market-research-importance',
    9, [54], 'Outline three points at 5 marks each (2 + 3).', points('Point', 3, (2, 3)))

spot = lift(S23, 10, 'Spotlight Oral Care, a Galway based company, was set up by sisters and dentists Dr Lisa & Dr Vanessa Creaven and Dr Barry Buckley in 2016. The company has developed a product portfolio for specific consumer oral care needs. Distribution channels include both online selling and the use of retailers in Europe, the UK and the US.')
add(3, 8, 'ai', 'Q8(A)(i)', spot + '\n\n' + lift(S23, 10, 'Explain the term channel of distribution.'), 5, 'business-4-17', 'channel-of-distribution', 10, [55],
    'Explain the term for 5 marks (2 + 3).', [comps('Channel of distribution', (2, 3))])
add(3, 8, 'aii', 'Q8(A)(ii)', spot + '\n\n' + lift(S23, 10, 'Draft a diagram of a channel of distribution that Spotlight Oral Care might use.'), 6, 'business-4-17',
    'distribution-channel-diagram', 10, [55], 'Draft the diagram for 6 marks (3 + 3).', [comps('Channel diagram', (3, 3))],
    ['The scheme’s model diagram shows Manufacturer, Retailer (e.g. Boots) and Consumer, linked by arrows; other channels Spotlight might use are accepted.'])
add(3, 8, 'aiii', 'Q8(A)(iii)', spot + '\n\n' + lift(S23, 10, 'Outline two implications of using this channel of distribution.'), 14, 'business-4-17',
    'distribution-channel-implications', 10, [55], 'Outline two implications at 7 marks each (4 + 3).', points('Implication', 2, (4, 3)))
add(3, 8, 'b', 'Q8(B)', lift(S23, 10, 'In relation to the product element of the marketing mix explain the factors a business must consider when designing a new or a revised product.'),
    15, 'business-4-17', 'product-design-factors', 10, [56], 'Explain three factors at 5 marks each (2 + 3).', points('Factor', 3, (2, 3)))

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
pools = [
    pool('bus-2022-hl-s3-q2a', '2(A)', 4, [7, 31, 32], 1,
         lift(S23, 4, 'Evaluate one of the following types of limited companies as a business ownership option.'),
         braw + '\n\n' + lift(S23, 4, 'Evaluate one of the following types of limited companies as a business ownership option.'),
         [opt('ltd', lift(S23, 4, '(i) A Private Company Limited by shares (LTD company).'), company_resp),
          opt('dac', lift(S23, 4, '(ii) A Designated Activity Company (DAC).'), company_resp)],
         20, 'Evaluate the selected company type: three features at 6 marks each (3 + 3) and 2 marks for evaluation.',
         ['The support notes compare both types and list features that apply to both; each route keeps the same 3 x 6 + 2 allocation.'],
         'business-5-14', 'limited-company-evaluation',
         'The paper prints a closed choice of two limited-company types (LTD or DAC) and asks for one. Both single-type routes are generated at 20 marks.',
         legacy_route('bus-2022-hl-s3-q2a', ['ltd'], 4, [7, 31, 32],
                      'the printed one-of-two choice is expanded into two routes; this ID becomes the LTD company route, the first printed option, with the published response allocation.')),
    pool('bus-2022-hl-s3-q6c', '6(C)', 8, [11, 51], 3,
         lift(S23, 8, 'Compare the similarities and differences for businesses and households in relation to taxation. Use any three of the following headings to structure your answer:'),
         lift(S23, 8, 'Compare the similarities and differences for businesses and households in relation to taxation. Use any three of the following headings to structure your answer:'),
         [opt('corporation-tax', 'Corporation Tax'), opt('paye', 'PAYE'), opt('capital-gains-tax', 'Capital Gains Tax'), opt('lpt', 'Local Property Tax (LPT)')],
         20, 'Compare businesses and households under each of the three headings using 7 (4 + 3), 7 (4 + 3) and 6 (3 + 3) marks.',
         ['The 7/7/6 allowance is not tied to a particular heading.'],
         'business-3-18', 'business-household-taxation',
         'The paper prints a closed list of four taxation headings and asks for any three. Generate all four unordered three-heading routes at 20 marks with the 7/7/6 split kept off named headings.',
         legacy_route('bus-2022-hl-s3-q6c', ['corporation-tax', 'paye', 'capital-gains-tax'], 8, [11, 51],
                      'the printed any-three-of-four choice is expanded into four routes; this ID becomes the Corporation Tax, PAYE and Capital Gains Tax route, the first printed combination, with the published 7/7/6 allocation.'),
         ordered=seven_seven_six),
    pool('bus-2022-hl-s3-q8c', '8(C)', 10, [13, 57], 3,
         lift(S23, 10, 'Outline your understanding of any three of the following types of advertising listed below. Provide an example in each case to support your answer.'),
         lift(S23, 10, 'Outline your understanding of any three of the following types of advertising listed below. Provide an example in each case to support your answer.'),
         [opt('persuasive', lift(S23, 10, '1. Persuasive advertising')), opt('informative', lift(S23, 10, '2. Informative advertising')),
          opt('generic', lift(S23, 10, '3. Generic advertising')), opt('competitive', '4. Competitive advertising')],
         20, 'Outline each of the three types with an example using 7 (4 + 3), 7 (4 + 3) and 6 (3 + 3) marks.',
         ['The 7/7/6 allowance is not tied to a particular advertising type.'],
         'business-4-17', 'advertising-types',
         'The paper prints a closed list of four advertising types and asks for any three. Generate all four unordered three-type routes at 20 marks with the 7/7/6 split kept off named types.',
         legacy_route('bus-2022-hl-s3-q8c', ['persuasive', 'informative', 'generic'], 10, [13, 57],
                      'the printed any-three-of-four choice is expanded into four routes; this ID becomes the persuasive, informative and generic advertising route, the first printed combination, with the published 7/7/6 allocation.'),
         ordered=seven_seven_six),
]
assert scheme(57, 'Competitive/Comparative advertising:') and lift(S23, 10, '4. Competitive advertising.')

# ---------------------------------------------------------------- checks
s1 = [c for c in created if c['section'] == '1']
s3 = [c for c in created if c['section'] == '3']
assert sum(c['totalMarks'] for c in s1) == 120, sum(c['totalMarks'] for c in s1)
legacy_ids = {i for i, c in original.items() if c['year'] == year and c['level'] == 'higher' and c['section'] in ('1', '3')}
pool_legacy = {p['legacyRoute']['id'] for p in pools}
assert legacy_ids == {c['id'] for c in created} | pool_legacy, legacy_ids ^ ({c['id'] for c in created} | pool_legacy)
def qnum(c):
    return c['questionRef'].split(' Q')[1].split('(')[0].split(' ')[0]
pool_marks = {p['template']['questionRef'].split(' Q')[1].split('(')[0]: p['template']['totalMarks'] for p in pools}
for q in range(1, 9):
    total = sum(c['totalMarks'] for c in s3 if qnum(c) == str(q)) + pool_marks.get(str(q), 0)
    assert total == 60, (q, total)

path = Path('components/MarkBank/cards/business/rubric-authored.json')
d = json.loads(path.read_text())
ids = {c['id'] for c in created}
d['cards'] = [c for c in d['cards'] if c['id'] not in ids] + created
d['reviews'] = [r for r in d['reviews'] if not (r['year'] == year and r['section'] in ['1', '3'])]
SELECTION = {
    1: 'No finite printed answer menu occurs in Section 1. True/False labels, slash-separated circled options and matching rows are required answer formats for every row. Methods, measures, ways and GDPR rights in the support notes are open examples. Each split part keeps its printed prompt and data.',
    3: 'Three finite printed pools are expanded separately: Q2(A) one of two limited-company types, Q6(C) any three of four taxation headings, Q8(C) any three of four advertising types. Stakeholders in Q1(A)(ii), HR functions in Q6(A) and leadership styles in Q5(A) are open choices (no printed list). Named pairs and the three Consumer Protection Act headings are required and kept whole. Support-note lists elsewhere are open examples.',
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
        elif 'True or False' in w:
            cat, why = 'required-headings', 'True/False are answer labels for each of the five required statements in Section 1 Q7, not optional tasks. All five stay in one exercise with the shared 3,2,2,2,1 tariff.'
        elif doc['paperFileid'] == S23 + '.pdf' and page == 4:
            cat, why, pid = 'finite-pool', 'Section 3 Q2(A) asks for one of two printed limited-company types (LTD or DAC). Both single-type routes are generated at 20 marks; the legacy card ID is kept as the LTD route.', 'bus-2022-hl-s3-q2a'
        elif m == 'any three' and 'stakeholders' in w and 'functions of the HR Manager' not in w:
            cat, why = 'open-response', 'Section 3 Q1(A)(ii) asks for any three stakeholders; the paper prints no list, so the choice is open and remains one task.'
        elif m == 'any three' and 'headings to structure' in w:
            cat, why, pid = 'finite-pool', 'Section 3 Q6(C) asks for any three of four printed taxation headings. All four three-heading routes are generated at 20 marks; the legacy card ID is kept as the first route.', 'bus-2022-hl-s3-q6c'
        elif m == 'any three' and 'functions of the HR Manager' in w:
            cat, why = 'open-response', 'Section 3 Q6(A)(i) asks for any three HR functions; the paper prints no list, so the choice is open and remains one task.'
        elif m == 'one of' and 'Human Resource Management functions' in w:
            cat, why = 'open-response', 'Section 3 Q6(A)(ii) asks about one HRM function of the candidate’s choice; no list is printed.'
        elif m == 'any three' and 'advertising' in w:
            cat, why, pid = 'finite-pool', 'Section 3 Q8(C) asks for any three of four printed advertising types. All four three-type routes are generated at 20 marks; the legacy card ID is kept as the first route.', 'bus-2022-hl-s3-q8c'
        elif m == 'one of' and 'leading car sourcing' in w:
            cat, why = 'case-context', 'The M6 Motors extract describes the business as one of the leading car sourcing companies. It is case context, not an instruction to choose.'
        elif 'misleading, false or inaccurate' in w:
            cat, why = 'required-headings', '“Misleading, false or inaccurate information” is the wording of required heading 2 in Section 3 Q4(A); all three headings are required.'
        elif 'improved or disimproved' in w:
            cat, why = 'required-headings', 'Section 3 Q7(A)(iii) requires a judgement on whether the ratio improved or disimproved; it is a required determination, not a choice of task.'
        elif 'new or a revised product' in w:
            cat, why = 'open-response', 'A new or a revised product is open wording in Section 3 Q8(B); the product design factors remain one task.'
        else:
            assert (doc['paperFileid'], page) in {(S1 + '.pdf', 2), (S1 + '.pdf', 9), (S1 + '.pdf', 36), (S23 + '.pdf', 1), (S23 + '.pdf', 12)}, item
            cat, why = 'exam-navigation', 'Cover instructions, pen/pencil instructions, answerbook supplies or copyright boilerplate. They do not create alternative task routes.'
        r = dict(wording=w, paperSha256=item['paperSha256'], classification=cat, reason=why)
        if pid:
            r['poolId'] = pid
        sel['reviews'][item['id']] = r
        counted += 1
path.write_text(json.dumps(sel, ensure_ascii=False, indent=2) + '\n')
print(f'Reviewed {len(created)} 2022 Higher base tasks ({len(s1)} Section 1, {len(s3)} Section 3; {sum("correction" in c for c in created)} corrected legacy IDs) and {len(pools)} route pools; classified {counted} raw selection matches.')
