"""Choice is not a route: collapse every choose-N (N >= 2) Business pool to ONE card.

When the candidate chooses N of M printed items and the scheme marks every
choice alike, the card prints the question verbatim with all M items,
criteria per chosen slot, and guidance quoting the scheme for every item. The
route pools for these 25 questions generated C(M, N) cards apiece (91 in all).

Each card keeps the legacy ID where one shipped (its correction reason is
rewritten); otherwise it takes the pool ID. Branch-only route IDs simply go:
none reached main. bus-2013-hl-s3-q1b stays routed because its scheme marks
the routes differently ([2,2,2,2,2] against [4,4,2]); the six choose-one pools
are outside this pass.
"""
import json, os, re, subprocess, sys
from pathlib import Path
import fitz
sys.path.insert(0, 'scripts/markbank')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bus_lib import norm
from glyph_ids import load_table, document_map

TABLE = load_table()
_text = {}


def page_text(kind, year, fileid, page):
    key = (kind, year, fileid)
    if key not in _text:
        d = fitz.open(f'paper-trail-corpus/{kind}/{year}/{fileid}.pdf')
        dm = document_map(d, TABLE)[0]
        _text[key] = [norm(''.join(dm.get(c, c) for c in pg.get_text())) for pg in d]
    return _text[key][page - 1]


WORDS = {2: 'two', 3: 'three', 4: 'four', 5: 'five'}
ORD = ['First', 'Second', 'Third', 'Fourth']

# pool id -> (noun, plural, directive mode, requirement, kept guidance, [(item, scheme page, quote)])
#   mode 'sw'       question text is the printed directive, which names the items itself
#   mode 'ctx+sw'   context lines, then the printed directive (items named in it or above)
#   mode 'ctx+sw+L' context lines, the printed directive, then every printed item
SPEC = {
    'bus-2014-hl-s3-q1c': ('heading', 'headings', 'sw',
        'Choose three of the four printed headings and outline the consumer’s rights under each: 7 (4 (2 + 2) + 3), 7 (4 + 3) and 6 (4 + 2).',
        ['The 7/7/6 allowance is not tied to a particular heading.', 'Use the historical Act specified in the examination.'],
        [('Merchantable Quality', 22, 'The consumer is entitled to goods which are of merchantable quality – they should be of reasonable standard/quality taking into account what they are supposed to do, their durability and the price paid.'),
         ('Guarantees', 22, 'Guarantees are seen as additional protection given to the consumer and they cannot limit the consumer’s rights under consumer law.'),
         ('Signs limiting consumer rights', 22, 'Consumers’ rights under the act cannot be taken away or limited by signs such as ‘Credit Notes Only’, ‘No Cash Refunds’, ‘No exchange’ etc.'),
         ('Unsolicited Goods', 22, 'These are goods that are sent to someone without having received an order.')]),
    'bus-2014-hl-s3-q3c': ('policy', 'policies', 'sw',
        'Choose two of the three printed policies and evaluate each for 10 marks: policy statement 4, impact 4 and evaluation 2.',
        ['Scheme: “Evaluation required in each case”. Use the context of the 2014 examination.'],
        [('European Monetary Union (EMU)', 27, 'The main perceived advantages of EMU are a reduction in transaction costs and end to destabilising currency shifts within Europe.'),
         ('European Union Competition Policy', 28, 'It restricts Irish businesses from forming anti-competitive cartels or keeping prices artificially high or preventing newcomers from entering the market.'),
         ('European Social Charter', 28, 'This EU Social Charter sets out basic principles that impact on Irish businesses: Free movement of Labour.')]),
    'bus-2015-hl-s3-q5b-ii': ('stage', 'stages', 'sw',
        'Choose three of the four printed stages and outline each at 5 marks (2 + 3).',
        ['The ordering task in Part (i) is marked separately.'],
        [('Feasibility Study', 39, 'This is carried out to assess if a product has potential.'),
         ('Test Marketing', 40, 'It involves doing a small-scale trial to identify possible faults and to assess customer reaction.'),
         ('Product Screening', 39, 'All ideas are vetted and the impractical and unworkable ideas are dropped, leaving the most viable ones for further examination and development.'),
         ('Prototype Development', 40, 'This stage involves developing a sample or model of a product.')]),
    'bus-2016-hl-s3-q2c': ('stakeholder', 'stakeholders', 'ctx16',
        'Choose four of the five stakeholders named in the extract and discuss each: 6 (3 + 3), 6 (3 + 3), 4 (2 + 2) and 4 (2 + 2).',
        ['The 6/6/4/4 sequence is not tied to particular stakeholders.'],
        [('Investors', 28, 'Do not conceal information – be honest and transparent with investors at all times'),
         ('Employees', 28, 'Pay fair wage – employees must be paid at least the minimum wage'),
         ('Suppliers', 29, 'Honour the contracts agreed. Prompt payments within the time agreed.'),
         ('Customers', 29, 'Provide quality products at reasonable prices'),
         ('Government', 29, 'Pay all taxes when due PAYE, VAT and Corporation Tax.')]),
    'bus-2020-hl-s3-q1b': ('heading', 'headings', 'sw',
        'Choose three of the four printed headings and explain the consumer’s rights under each: 7 (4 + 3), 7 (4 + 3) and 6 (3 + 3).',
        ['The 7/7/6 allowance is not tied to a particular heading. Use the historical Act specified in the 2020 examination.'],
        [('Services', 30, 'The service provider must have the necessary skill/qualification.'),
         ('Guarantees', 30, 'Guarantees are additional protection given to the consumer and they cannot limit the consumer’s rights under consumer law.'),
         ('Signs limiting consumer rights', 30, 'Signs such as ‘Credit Notes Only’, ‘No Cash Refunds’, ‘No exchange’ etc are prohibited under the Sale of Goods & Supply of Services Act.'),
         ('Merchantable Quality', 30, 'The consumer is entitled to goods which are of reasonable standard/quality considering what they are supposed to do, their durability and the price paid.')]),
    'bus-2024-hl-s3-q7ci': ('term', 'terms', 'ctx+sw+L',
        'Choose three of the four printed terms and explain each at 5 marks (2 + 3).', [],
        [('Liquidity', 55, 'Liquidity refers to the ability of a business to pay its short-term liabilities as they fall due.'),
         ('Profit and Loss Account', 55, 'Profit and Loss account records the sales less all the costs and expenses of the organisation for the financial year.'),
         ('Debtors', 55, 'Debtors are individuals or businesses that owe the business money after buying goods or services on credit.'),
         ('Dividends', 55, 'Dividend is the portion of profits paid to shareholders at the end of the year.')]),
    'bus-2024-hl-s3-q8biii': ('business', 'businesses', 'ctx+sw+L',
        'Choose two of the three printed businesses and recommend a medium with a reason for each: 6 (3 + 3) and 5 (3 + 2).',
        ['The larger allowance is not tied to a particular business.'],
        [('Rolex watches', 57, 'Rolex – Print/TV advertising aimed at high income earners.'),
         ('Adare Manor Hotel and Golf Resort', 57, 'Adare Manor Hotel and Golf Resort - might advertise in international golf magazines or on international tv coverage of golf events such as the US Masters, Ryder Cup etc.'),
         ('Prime Hydration drinks', 57, 'Prime Hydration drinks - Digital advertising on social media, YouTube etc.')]),
    'bus-2022-hl-s3-q6c': ('heading', 'headings', 'prompt+L',
        'Choose three of the four printed headings and compare businesses and households under each: 7 (4 + 3), 7 (4 + 3) and 6 (3 + 3).',
        ['The 7/7/6 allowance is not tied to a particular heading.'],
        [('Corporation Tax', 51, 'Certain business, limited companies, must pay corporation tax to revenue on their profits whereas households do not pay corporation tax.'),
         ('PAYE', 51, 'Households pay PAYE on their income if they are employees or self- employed.'),
         ('Capital Gains Tax', 51, 'Both households and business are liable to pay Capital Gains Tax on any profit made from the sale of the asset.'),
         ('Local Property Tax (LPT)', 51, 'Local Property Tax (LPT) is a self-assessed tax charged on the market value of residential properties in the State.')]),
    'bus-2022-hl-s3-q8c': ('type', 'types', 'prompt+L',
        'Choose three of the four printed types and outline each with an example: 7 (4 + 3), 7 (4 + 3) and 6 (3 + 3).',
        ['The 7/7/6 allowance is not tied to a particular advertising type.'],
        [('Persuasive advertising', 57, 'This advertising attempts to persuade the consumer that they need the product.'),
         ('Informative advertising', 57, 'Informative advertising conveys facts or data for the purposes of educating an audience, rather than increasing sales revenue.'),
         ('Generic advertising', 57, 'Generic advertising attempts to convey the importance of one particular type of good.'),
         ('Competitive advertising', 57, 'The brand or product is advertised as superior to those of other competitors based on the price comparisons, quality of the products etc.')]),
    'bus-2021-hl-s3-q3c': ('policy', 'policies', 'ctx+sw+L',
        'Choose two of the three printed policies and evaluate each for 10 marks: two impacts at 4 marks (2 + 2) and 2 marks for evaluation.',
        ['Scheme: “Evaluation required in each case”. Each policy carries its own 2-mark evaluation.'],
        [('The Common Agricultural Policy', 40, 'The Common Agricultural Policy gives grants farmers under the single payment scheme.'),
         ('The Competition Policy', 40, 'It restricts Irish businesses from forming anti-competitive cartels or keeping prices artificially high or preventing newcomers from entering the market.'),
         ('The European Union Social Charter', 41, 'Workers have the right to migrate freely which benefits employers in terms of recruitment and selection.')]),
    'bus-2026-ol-s2-q8b': ('stage', 'stages', 'ctx+sw+L',
        'Choose two of the three printed stages and explain each: 10 (7 + 3) and 5 (4 + 1).',
        ['The 10-mark allowance is not tied to a particular stage.'],
        [('Feasibility Study', 36, 'This is carried out to assess if the product is viable and can be successfully developed and brought to the market.'),
         ('Prototype Development', 36, 'This stage involves developing a sample or model of a product.'),
         ('Test Marketing', 36, 'The product is tested on a sample of potential consumers before going into full production.')]),
    'bus-2025-ol-s2-q1a': ('provision', 'provisions', 'ctx+sw+L',
        'Choose two of the four printed provisions and explain each with an example: 10 (7 + 3) and 5 (4 + 1).',
        ['The 10-mark allowance is not tied to a particular provision.'],
        [('Goods must be of merchantable quality', 13, 'The goods should be of reasonable standard, considering their durability and the price paid for them.'),
         ('Goods must be fit for purpose', 13, 'This means that goods must be able to do what they are meant to do and what they are designed for.'),
         ('Goods must be as described', 13, 'The goods must be the same as outlined on the packaging, in a brochure, or by a salesperson.'),
         ('Goods must conform to sample', 13, 'If a retailer sells a product using an example/small piece, the full product must be identical to this example.')]),
    'bus-2025-ol-s2-q2d': ('tax', 'taxes', 'ctx+sw',
        'Choose two of the three named taxes and explain each: 10 (7 + 3) and 5 (4 + 1).',
        ['The 10-mark allowance is not tied to a particular tax.'],
        [('Excise Duty', 18, 'Tax added to certain goods such as fuel, alcohol, and tobacco.'),
         ('VAT', 18, 'VAT is a regressive and indirect tax charged on the sale of goods and services.'),
         ('Carbon Tax', 18, 'A tax imposed on the carbon content of fossil fuels, aiming to reduce greenhouse gas emissions.')]),
    'bus-2025-ol-s2-q9d': ('term', 'terms', 'ctx+sw',
        'Choose three of the four underlined terms and explain each at 5 marks (4 + 1).', [],
        [('Insurance premiums', 42, 'The fee paid to the insurance company (insurer) for the insurance cover.'),
         ('Motor insurance', 42, 'Motor insurance is required by law.'),
         ('Public liability insurance', 42, 'Protects the business from claims made by members of the public for accidents or injuries on their premises'),
         ('Employer PRSI', 42, 'An employer must pay this compulsory Pay Related Social Insurance on behalf of each of their employees.')]),
    'bus-2025-ol-s2-q9e': ('principle', 'principles', 'tail',
        'Choose two of the three named principles and explain each: 10 (7 + 3) and 5 (4 + 1).',
        ['The 10-mark allowance is not tied to a particular principle.'],
        [('Insurable interest', 43, 'The person taking out insurance must have a financial interest in the item being insured – must gain from its existence and suffer financially from its loss.'),
         ('Indemnity', 43, 'A person cannot make a profit from insurance – the purpose of insurance is to leave the person in the same financial position as before the loss occurred.'),
         ('Utmost good faith', 43, 'A person taking out insurance must be truthful when completing proposal form – all material facts must be declared.')]),
    'bus-2024-ol-s2-q3c': ('barrier', 'barriers', 'ctx+sw+L',
        'Choose three of the four printed barriers and explain each: 7 (4 + 3), 7 (4 + 3) and 6 (4 + 2).',
        ['The 7/7/6 sequence prices the three explanations, not particular barriers.'],
        [('Quota', 18, 'a limit on the number of a certain good that can be imported into a country.'),
         ('Tariff', 18, 'a tax placed on foreign products.'),
         ('Embargo', 18, 'a government ban on imports from a particular country.'),
         ('Subsidies', 18, 'money that a government or the EU gives to its own indigenous businesses to allow them to sell their products and services more cheaply.')]),
    'bus-2024-ol-s2-q4c': ('practice', 'practices', 'ctx+sw+L',
        'Choose two of the three printed practices and explain each: 10 (7 + 3) and 5 (4 + 1).',
        ['The 10-mark allowance is not tied to a particular practice.'],
        [('False or misleading advertising', 22, 'A business cannot give wrong information to customers when comparing its goods with its competitors’ goods.'),
         ('False product descriptions', 22, 'A business cannot mislead customers about the origin of a product'),
         ('False pricing', 22, 'A business must be truthful about the actual price, the previous price and the recommended retail price to consumers.')]),
    'bus-2024-ol-s2-q4e': ('element', 'elements', 'ctx+sw+L',
        'Choose three of the four printed elements and explain each: 7 (4 + 3), 7 (4 + 3) and 6 (4 + 2).',
        ['The 7/7/6 sequence prices the three explanations, not particular elements.'],
        [('Consideration', 23, 'This is the item of value that passes between both parties in a legal contract'),
         ('Capacity to Contract', 23, 'A person entering into a legal contract must have the legal capacity to do so: over 18, of sound mind, not under the influence of alcohol/drugs.'),
         ('Consent to Contract', 23, 'All parties entering a contract must do so of their own free will – they cannot be forced or coerced into the contract.'),
         ('Legality of Purpose', 23, 'Contracts must be within the law – a contract cannot be made for illegal/criminal activities.')]),
    'bus-2024-ol-s2-q6c': ('principle', 'principles', 'ctx+sw+L',
        'Choose two of the three printed principles and explain each with an example: 10 marks each (explanation 6 + example 4).', [],
        [('Utmost good faith', 28, 'A person taking out insurance must be truthful when completing proposal form – all material facts must be declared.'),
         ('Insurable interest', 28, 'The person taking out insurance must have a financial interest in the item being insured – must gain from its existence and suffer financially from its loss.'),
         ('Indemnity', 28, 'A person cannot make a profit from insurance – the purpose of insurance is to leave the person in the same financial position as before the loss occurred.')]),
    'bus-2024-ol-s2-q7b': ('function', 'functions', 'ctx+sw+L',
        'Choose two of the three printed functions and explain each: 10 (7 + 3) and 5 (4 + 1).',
        ['The 10-mark allowance is not tied to a particular function.'],
        [('Manpower Planning', 30, 'This is making sure the business has the right number of staff with the right skills in the right place at the right time.'),
         ('Training and Development', 30, 'Training involves supplying the skills, knowledge and attitudes needed by employees to do their jobs better.'),
         ('Performance Appraisal', 30, "This is a review of an employee's progress over a specific period of time.")]),
    'bus-2024-ol-s2-q9e': ('source', 'sources', 'ctx+sw+L',
        'Choose two of the three printed sources and explain each: 8 (4 + 4) and 7 (4 + 3).',
        ['The 8-mark allowance is not tied to a particular source.'],
        [('Grant', 36, 'This is a non-repayable sum of money given to a business by government agencies such as Enterprise Ireland and Local Enterprise offices to fund expansion.'),
         ('Long-term Loan', 36, 'Borrowings of over five years are secured on the fixed assets of the business.'),
         ('Share Capital', 36, 'This is the money provided by investors, known as shareholders.')]),
    'bus-2023-ol-s2-q1e': ('method', 'methods', 'bullets',
        'Choose three of the four printed methods and explain each with an example: 7 (4 + 3), 7 (4 + 3) and 6 (4 + 2).',
        ['The 7/7/6 sequence prices the three explanations, not particular methods.'],
        [('Frustration', 15, 'An unforseen event makes it impossible for the contract to be completed.'),
         ('Breach', 15, 'One party in the contract breaks a condition of the contract, the contract is invalidated.'),
         ('Agreement', 15, 'Both parties agree to end the contract before its finish date.'),
         ('Performance', 15, 'Both parties fulfil the terms of the contract and the contract comes to its natural end.')]),
    'bus-2023-ol-s2-q9d': ('stage', 'stages', 'ctx+sw+L',
        'Choose two of the three printed stages and explain each: 8 (4 + 4) and 7 (4 + 3).',
        ['The 8-mark allowance is not tied to a particular stage.'],
        [('Feasibility Study', 33, 'This is carried out to assess if the product is viable and can be successfully developed and brought to the market.'),
         ('Prototype Development', 33, 'This stage involves developing a sample or model of a product.'),
         ('Test Marketing', 33, 'The product is tested on a sample of potential consumers before going into full production.')]),
    'bus-2022-ol-s2-q4c': ('element', 'elements', 'ctx+sw+L',
        'Choose three of the four printed elements and explain each with reference to the text at 5 marks (3 + 2).', [],
        [('Offer and Acceptance (Agreement)', 20, 'one party makes an offer to another party. This offer is accepted unconditionally by the other party.'),
         ('Capacity to Contract', 20, 'all parties entering into the contract must have the ability to do so.'),
         ('Consideration', 20, 'this is the item of value that must pass between both parties to a contract.'),
         ('Consent to Contract', 20, 'both parties must enter into the contract of their own free will, under no pressure.')]),
    'bus-2022-ol-s2-q6ai': ('source', 'sources', 'ctx+sw',
        'Choose two of the three printed sources and explain each at 7 marks (4 + 3).',
        ['Part (ii) asks for one advantage of each source chosen here and is its own card.'],
        [('Medium Term Loan', 25, 'a loan from financial institution taken out over a 1–5-year period, which must be repaid in equal instalments with interest.'),
         ('Hire Purchase', 25, 'allows a business to purchase an item/asset via a finance company.'),
         ('Leasing', 25, 'this involves renting/hiring an asset over a 1 to 5-year period and making monthly payments for the item.')]),
}

pools_path = Path('components/MarkBank/cards/business/route-pools.json')
rp = json.loads(pools_path.read_text())
routes = json.loads(subprocess.check_output(['node', 'scripts/markbank/authoring/business_routes.mjs'], text=True))
route_ids = {}
for r in routes:
    route_ids.setdefault(r['routePoolId'], []).append(r['id'])

collapse = [p for p in rp['pools'] if p['id'] in SPEC]
assert len(collapse) == 25 and all(p['choose'] >= 2 for p in collapse)
assert not [p for p in rp['pools'] if p['choose'] >= 2 and p['id'] not in SPEC and p['id'] != 'bus-2013-hl-s3-q1b']

cards, card_of = [], {}
for p in collapse:
    noun, plural, mode, requirement, kept, quotes = SPEC[p['id']]
    t, n, m = p['template'], p['choose'], len(p['options'])
    year, paper = t['year'], t['paperFileid']
    paper_text = ' '.join(page_text('exampapers', year, paper, pg) for pg in t['paperPages'])
    sw = norm(p['sourceWording'])
    assert sw in paper_text, (p['id'], sw)
    lines = [l for l in p['routePrompt'].split('\n')]
    ctx = '\n'.join(lines[:-1]).rstrip()
    # Everything above the rewritten directive, with its own paragraph spacing.
    prefix = p['routePrompt'][:p['routePrompt'].rfind('\n') + 1]
    labels = '\n'.join(o['label'] for o in p['options'])
    if mode == 'sw':
        text = sw
    elif mode == 'ctx16':
        printed = 'Corporate Social Responsibility refers to how businesses interact with their stakeholders on a daily basis including investors, employees, suppliers, customers, and government.'
        assert printed in paper_text
        text = printed + '\n\n' + sw
    elif mode == 'prompt+L':
        assert norm(p['routePrompt']) == sw, p['id']
        text = sw + '\n' + labels
    elif mode == 'ctx+sw':
        text = prefix + sw
    elif mode == 'ctx+sw+L':
        text = prefix + sw + '\n' + labels
    elif mode == 'tail':
        last = lines[-1]
        lead = last[:last.index('Explain the following')].rstrip()
        assert norm(lead) in paper_text, lead
        text = prefix + lead + ' ' + sw
    elif mode == 'bullets':
        assert ctx and ctx.endswith('the following methods:'), ctx
        text = ctx + '\n' + '\n'.join('• ' + o['label'] for o in p['options']) + '\n' + sw
    for o in p['options']:
        assert norm(o['label']).strip('. ').lower() in norm(text).lower(), (p['id'], o['label'])
    # The item names quoted in guidance are the printed ones, in printed order.
    assert len(quotes) == m, p['id']
    for (item, _, _), o in zip(quotes, p['options']):
        assert norm(item) in norm(o['label']), (p['id'], item, o['label'])
    scheme_pages = t['rubric']['schemePages']
    guidance = [f'You choose which {WORDS[n]} of the {WORDS[m]} printed {plural} to answer. The scheme marks every choice alike, so this is one card whichever {plural} you choose.'] + kept
    for item, page, quote in quotes:
        assert page in scheme_pages, (p['id'], page)
        assert quote in page_text('markingschemes', year, t['rubric']['schemeFileid'], page), (p['id'], item, quote)
        guidance.append(f'{item} (scheme PDF page {page}): “{quote}”')
    if p.get('orderedResponses'):
        base = p['orderedResponses']
    else:
        shapes = {json.dumps([(a['maxMarks'], a['permittedMarks']) for a in o['response']['allocations']]) for o in p['options']}
        assert len(shapes) == 1, p['id']
        base = [p['options'][0]['response']] * n
    responses = [dict(id=f'response-{i}', label=f'{ORD[i - 1]} {noun} you chose',
                      allocations=[dict(a) for a in r['allocations']]) for i, r in enumerate(base, 1)]
    assert sum(a['maxMarks'] for r in responses for a in r['allocations']) == t['totalMarks'], p['id']
    topics = list(dict.fromkeys(o['topicId'] for o in p['options']))
    legacy = p.get('legacyRoute')
    cid = legacy['id'] if legacy else p['id']
    card = dict(id=cid, year=year, level=t['level'], section=t['section'], paperFileid=paper, paperPages=t['paperPages'],
                sourceLabel=t['sourceLabel'], sourceTitle=t['sourceTitle'], questionRef=t['questionRef'], questionText=text,
                totalMarks=t['totalMarks'], topicId=topics[0], conceptId=t['conceptId'],
                rubric=dict(system='business', taskRequirements=[requirement], guidance=guidance, responses=responses,
                            schemeFileid=t['rubric']['schemeFileid'], schemePages=scheme_pages, markingGuideNote=t['rubric']['markingGuideNote']))
    if topics[1:]:
        card['additionalTopicIds'] = topics[1:]
    if legacy:
        head = legacy['correction']['reason'].split(': ', 1)[0]
        card['correction'] = dict(legacy['correction'], reason=head + f': question text lifted from the printed paper, with all {WORDS[m]} printed {plural}; the printed choice of {WORDS[n]} is ONE card (the scheme marks every choice alike), with criteria per chosen {noun} and the scheme’s wording for every {noun}. Retain the existing card ID and total marks for saved progress.')
    cards.append(card)
    card_of[p['id']] = dict(card=cid, routes=route_ids[p['id']], desc=f"Section {t['questionRef'].split(' Section ')[1]} {WORDS[n]} of {WORDS[m]} printed {plural}",
                            year=year, level=t['level'], section=t['section'], review=p['review'], ref=p['review']['question'])

# ---- route pools: only the differently-marked 2013 pool and the choose-one pools remain
rp['pools'] = [p for p in rp['pools'] if p['id'] not in SPEC]
pools_path.write_text(json.dumps(rp, ensure_ascii=False, indent=2) + '\n')

# ---- rubric-authored cards and question reviews
ra_path = Path('components/MarkBank/cards/business/rubric-authored.json')
ra = json.loads(ra_path.read_text())
ids = {c['id'] for c in cards}
# Idempotent: a re-run replaces the cards an earlier run produced.
ra['cards'] = sorted([c for c in ra['cards'] if c['id'] not in ids] + cards, key=lambda c: (c['year'], c['section'], c['id']))
remaining = {(p['template']['year'], p['template']['level'], p['template']['section']): [] for p in rp['pools']}
for p in rp['pools']:
    remaining[(p['template']['year'], p['template']['level'], p['template']['section'])].append('Section ' + p['template']['questionRef'].split(' Section ')[1])
by_section = {}
for info in card_of.values():
    by_section.setdefault((info['year'], info['level'], info['section']), []).append(info['desc'])


def rewrite(text, key):
    keep = [s for s in re.split(r'(?<=\.)\s+', text) if not re.search(r'pool|route', s, re.I)]
    add = 'Printed choices the scheme marks alike are one card each (choice is not a route): ' + '; '.join(sorted(by_section[key])) + '.'
    if remaining.get(key):
        add += ' Still routed because they are choose-one or marked differently: ' + ', '.join(sorted(remaining[key])) + ' (route-pools.json).'
    return ' '.join(keep + [add]).strip()


touched = set()
for pid, info in card_of.items():
    q = re.match(r'\d+', info['ref']).group()
    match = [r for r in ra['reviews'] if (r['year'], r['level'], r['section'], r['question']) == (info['year'], info['level'], info['section'], q)]
    card = next(c for c in cards if c['id'] == info['card'])
    if match:
        r = match[0]
        style_suffix = all('(' not in k for k in r['boundaries'])
        key = info['card'].split('-q', 1)[1] if style_suffix else info['ref']
        if info['card'] in r['cardIds']:
            continue
        r['cardIds'] = r['cardIds'] + [info['card']]
        r['boundaries'] = dict(r['boundaries'], **{key: card['totalMarks']})
        r['paperPagesReviewed'] = sorted(set(r['paperPagesReviewed']) | set(card['paperPages']))
        r['schemePagesReviewed'] = sorted(set(r['schemePagesReviewed']) | set(card['rubric']['schemePages']))
        r['sourceClarifications'] = r['sourceClarifications'] + card['rubric']['guidance']
    else:
        pr = info['review']
        ra['reviews'].append(dict(status=pr['status'], year=info['year'], level=info['level'], section=info['section'], question=q,
                                  cardIds=[info['card']], sources=pr['sources'], paperPagesReviewed=pr['paperPagesReviewed'],
                                  schemePagesReviewed=pr['schemePagesReviewed'], boundaries={info['ref']: card['totalMarks']},
                                  selectionAnalysis='', sourceClarifications=card['rubric']['guidance']))
    touched.add((info['year'], info['level'], info['section']))
for r in ra['reviews']:
    key = (r['year'], r['level'], r['section'])
    if key in touched:
        r['selectionAnalysis'] = rewrite(r['selectionAnalysis'], key)
ra['reviews'].sort(key=lambda r: (r['year'], r['section'], r['question']))
ra_path.write_text(json.dumps(ra, ensure_ascii=False, indent=2) + '\n')

# ---- selection reviews: the pool's directive now names its card
sel_path = Path('scripts/markbank/authored/business-selection-reviews.json')
sel = json.loads(sel_path.read_text())
moved = 0
for key, r in sel['reviews'].items():
    pid = r.get('poolId')
    if pid in card_of:
        info = card_of[pid]
        r.pop('poolId')
        r['classification'] = 'finite-choice'
        r['cardId'] = info['card']
        r['reason'] = f"{info['desc']}: the candidate chooses, and the scheme marks every choice alike, so one card carries every printed item."
        moved += 1
sel_path.write_text(json.dumps(sel, ensure_ascii=False, indent=2) + '\n')

# ---- full-paper reviews: route IDs out, the one card in
pr_path = Path('scripts/markbank/authored/business-paper-reviews.json')
prs = json.loads(pr_path.read_text())
for review in prs['reviews']:
    hit = [info for pid, info in card_of.items() if pid in review['finiteRoutePoolIds']]
    if not hit:
        continue
    gone = {rid for info in hit for rid in info['routes']}
    review['authoredCardIds'] = sorted((set(review['authoredCardIds']) - gone) | {info['card'] for info in hit})
    review['finiteRoutePoolIds'] = [pid for pid in review['finiteRoutePoolIds'] if pid not in card_of]
    review['finiteChoiceCardIds'] = sorted(set(review.get('finiteChoiceCardIds', [])) | {info['card'] for info in hit})
    notes = []
    for note in review['reviewNotes']:
        kept = [s for s in re.split(r'(?<=\.)\s+', note) if not re.search(r'pool|route', s, re.I)]
        if kept:
            notes.append(' '.join(kept))
    notes.insert(min(2, len(notes)), 'Choice is not a route: ' + '; '.join(sorted(info['desc'] for info in hit))
                 + (' are ONE card each' if len(hit) > 1 else ' is ONE card') + ', printing every item, with criteria per chosen item and the scheme’s wording for every item.'
                 + (f" Still routed: {', '.join(review['finiteRoutePoolIds'])}." if review['finiteRoutePoolIds'] else ''))
    review['reviewNotes'] = notes
pr_path.write_text(json.dumps(prs, ensure_ascii=False, indent=2) + '\n')

print(f'collapsed {len(cards)} pools into one card each, removing {sum(len(i["routes"]) for i in card_of.values())} route cards; '
      f'{moved} selection reviews now name their card; {len(rp["pools"])} pools remain')
